// Pulumi stack for junebot:
//   - SSM SecureString for the Anthropic API key (seeded manually or by deploy.sh)
//   - IAM role allowing Lambda to read the SSM param and write CloudWatch logs
//   - Lambda function (python3.11, Web Adapter layer, streaming)
//   - Function URL with RESPONSE_STREAM invoke mode and CORS locked to june.kim
//
// Day-to-day code updates go through `junebot/deploy-code.sh`, not this stack.
// Re-run `pulumi up` only for infra changes.
package main

import (
	"encoding/json"

	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/iam"
	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/lambda"
	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/ssm"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

// us-east-1 ARN for the Lambda Web Adapter layer (public, maintained by AWS).
// x86_64 build. If we switch to arm64, use the arm64 variant.
const webAdapterLayerArn = "arn:aws:lambda:us-east-1:753240598075:layer:LambdaAdapterLayerX86:23"

func main() {
	pulumi.Run(func(ctx *pulumi.Context) error {
		// Placeholder value — overwrite after first `pulumi up` by running:
		//   aws ssm put-parameter --name /junebot/anthropic-api-key \
		//     --type SecureString --value "$ANTHROPIC_API_KEY" --overwrite
		apiKeyParam, err := ssm.NewParameter(ctx, "anthropic-api-key", &ssm.ParameterArgs{
			Name:        pulumi.String("/junebot/anthropic-api-key"),
			Type:        pulumi.String("SecureString"),
			Value:       pulumi.String("placeholder-overwrite-via-cli"),
			Description: pulumi.String("Anthropic API key for junebot"),
		}, pulumi.IgnoreChanges([]string{"value"}))
		if err != nil {
			return err
		}

		assumeRole, _ := json.Marshal(map[string]any{
			"Version": "2012-10-17",
			"Statement": []map[string]any{{
				"Action":    "sts:AssumeRole",
				"Effect":    "Allow",
				"Principal": map[string]string{"Service": "lambda.amazonaws.com"},
			}},
		})
		role, err := iam.NewRole(ctx, "junebot-role", &iam.RoleArgs{
			AssumeRolePolicy: pulumi.String(string(assumeRole)),
		})
		if err != nil {
			return err
		}

		_, err = iam.NewRolePolicyAttachment(ctx, "junebot-logs", &iam.RolePolicyAttachmentArgs{
			Role:      role.Name,
			PolicyArn: pulumi.String("arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"),
		})
		if err != nil {
			return err
		}

		_, err = iam.NewRolePolicy(ctx, "junebot-ssm-read", &iam.RolePolicyArgs{
			Role: role.ID(),
			Policy: apiKeyParam.Arn.ApplyT(func(arn string) (string, error) {
				p, e := json.Marshal(map[string]any{
					"Version": "2012-10-17",
					"Statement": []map[string]any{{
						"Effect":   "Allow",
						"Action":   []string{"ssm:GetParameter"},
						"Resource": arn,
					}},
				})
				return string(p), e
			}).(pulumi.StringOutput),
		})
		if err != nil {
			return err
		}

		// Seed zip so `pulumi up` can create the function before the first
		// real build. deploy-code.sh replaces the code on every blog deploy.
		fn, err := lambda.NewFunction(ctx, "junebot", &lambda.FunctionArgs{
			Name:        pulumi.String("junebot"),
			Role:        role.Arn,
			Runtime:     pulumi.String("python3.11"),
			Handler:     pulumi.String("run.sh"),
			Timeout:     pulumi.Int(60),
			MemorySize:  pulumi.Int(1024),
			Layers:      pulumi.StringArray{pulumi.String(webAdapterLayerArn)},
			Code:        pulumi.NewFileArchive("./seed.zip"),
			Environment: &lambda.FunctionEnvironmentArgs{
				Variables: pulumi.StringMap{
					"ANTHROPIC_KEY_PARAM":   pulumi.String("/junebot/anthropic-api-key"),
					"AWS_LAMBDA_EXEC_WRAPPER": pulumi.String("/opt/bootstrap"),
					"AWS_LWA_INVOKE_MODE":     pulumi.String("response_stream"),
					"PORT":                    pulumi.String("8080"),
				},
			},
		}, pulumi.IgnoreChanges([]string{"code"}))
		if err != nil {
			return err
		}

		// Function URL is fronted by CloudFront (/api/* behavior on the june.kim
		// distribution) with Origin Access Control. Auth type is AWS_IAM — only
		// CloudFront can invoke. CORS is handled by the CF behavior, not here.
		url, err := lambda.NewFunctionUrl(ctx, "junebot-url", &lambda.FunctionUrlArgs{
			FunctionName:      fn.Name,
			AuthorizationType: pulumi.String("AWS_IAM"),
			InvokeMode:        pulumi.String("RESPONSE_STREAM"),
		})
		if err != nil {
			return err
		}

		// Permission granted manually via `aws lambda add-permission` after the
		// CloudFront distribution was known. See infra/junebot/README.md.

		ctx.Export("functionUrl", url.FunctionUrl)
		ctx.Export("functionName", fn.Name)
		return nil
	})
}
