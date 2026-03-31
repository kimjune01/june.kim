#!/usr/bin/env bash
set -euo pipefail

# Deploy the email-to-post Lambda and wire SES receiving.
#
# Prerequisites:
#   - AWS CLI configured
#   - GITHUB_TOKEN stored in SSM Parameter Store at /agent/github-token
#   - Domain agent.june.kim MX records pointing to SES (see setup below)
#
# MX record setup (Namecheap, one-time):
#   Host: agent    Type: MX    Value: 10 inbound-smtp.us-east-1.amazonaws.com
#
# SES domain verification (one-time):
#   Run this script once, then add the TXT record it prints for domain verification.
#
# SES must be in us-east-1 for receiving (only supported region).

REGION="us-east-1"
FUNCTION_NAME="post-agent-june-kim"
S3_BUCKET="agent-june-kim-incoming"
ROLE_NAME="post-agent-lambda-role"
RULE_SET_NAME="agent-june-kim-rules"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "=== Packaging Lambda ==="
cd "$(dirname "$0")"
rm -f lambda.zip
zip lambda.zip handler.py

echo "=== Ensuring S3 bucket ==="
if ! aws s3api head-bucket --bucket "$S3_BUCKET" --region "$REGION" 2>/dev/null; then
  aws s3api create-bucket --bucket "$S3_BUCKET" --region "$REGION"
  echo "Created bucket $S3_BUCKET"
fi

# Bucket policy: allow SES to write (per AWS docs, use aws:SourceAccount)
aws s3api put-bucket-policy --bucket "$S3_BUCKET" --region "$REGION" --policy "$(cat <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "ses.amazonaws.com"},
    "Action": "s3:PutObject",
    "Resource": "arn:aws:s3:::${S3_BUCKET}/*",
    "Condition": {"StringEquals": {"AWS:SourceAccount": "${ACCOUNT_ID}"}}
  }]
}
POLICY
)"

echo "=== Ensuring IAM role ==="
# Always update inline policy (idempotent)
if ! aws iam get-role --role-name "$ROLE_NAME" 2>/dev/null; then
  aws iam create-role --role-name "$ROLE_NAME" \
    --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
  aws iam attach-role-policy --role-name "$ROLE_NAME" \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
  echo "Waiting for role propagation..."
  sleep 10
fi

aws iam put-role-policy --role-name "$ROLE_NAME" --policy-name "post-agent-access" \
  --policy-document "$(cat <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::${S3_BUCKET}/*"
    },
    {
      "Effect": "Allow",
      "Action": ["ssm:GetParameter"],
      "Resource": "arn:aws:ssm:${REGION}:${ACCOUNT_ID}:parameter/agent/github-token"
    }
  ]
}
POLICY
)"

ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${ROLE_NAME}"

echo "=== Deploying Lambda ==="
if aws lambda get-function --function-name "$FUNCTION_NAME" --region "$REGION" 2>/dev/null; then
  aws lambda update-function-code \
    --function-name "$FUNCTION_NAME" \
    --zip-file fileb://lambda.zip \
    --region "$REGION"
  # Also update config on redeploy
  aws lambda update-function-configuration \
    --function-name "$FUNCTION_NAME" \
    --timeout 30 \
    --memory-size 128 \
    --runtime python3.12 \
    --handler handler.handler \
    --role "$ROLE_ARN" \
    --environment "Variables={S3_BUCKET=${S3_BUCKET},GITHUB_TOKEN_SSM=/agent/github-token,ALLOWED_SENDERS=${ALLOWED_SENDERS:-june@june.kim}}" \
    --region "$REGION"
else
  aws lambda create-function \
    --function-name "$FUNCTION_NAME" \
    --runtime python3.12 \
    --handler handler.handler \
    --role "$ROLE_ARN" \
    --zip-file fileb://lambda.zip \
    --timeout 30 \
    --memory-size 128 \
    --region "$REGION" \
    --environment "Variables={S3_BUCKET=${S3_BUCKET},GITHUB_TOKEN_SSM=/agent/github-token,ALLOWED_SENDERS=${ALLOWED_SENDERS:-june@june.kim}}"
fi

echo "=== Wiring SES ==="
# Verify domain — print the TXT record needed
VERIFICATION_TOKEN=$(aws ses verify-domain-identity --domain agent.june.kim --region "$REGION" --query VerificationToken --output text)
echo "  DNS TXT record needed: _amazonses.agent.june.kim → ${VERIFICATION_TOKEN}"

# Create receipt rule set if needed
aws ses describe-receipt-rule-set --rule-set-name "$RULE_SET_NAME" --region "$REGION" 2>/dev/null \
  || aws ses create-receipt-rule-set --rule-set-name "$RULE_SET_NAME" --region "$REGION"

RULE_JSON="$(cat <<RULE
{
  "Name": "post-agent-rule",
  "Enabled": true,
  "Recipients": ["post@agent.june.kim"],
  "Actions": [
    {
      "S3Action": {
        "BucketName": "${S3_BUCKET}",
        "ObjectKeyPrefix": "incoming/"
      }
    },
    {
      "LambdaAction": {
        "FunctionArn": "arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:${FUNCTION_NAME}",
        "InvocationType": "Event"
      }
    }
  ],
  "ScanEnabled": true
}
RULE
)"

# Allow SES to invoke Lambda (must be set before creating receipt rule)
aws lambda add-permission \
  --function-name "$FUNCTION_NAME" \
  --statement-id ses-invoke \
  --action lambda:InvokeFunction \
  --principal ses.amazonaws.com \
  --source-account "$ACCOUNT_ID" \
  --region "$REGION" 2>/dev/null || true

# Create or update receipt rule
if aws ses describe-receipt-rule --rule-set-name "$RULE_SET_NAME" --rule-name "post-agent-rule" --region "$REGION" 2>/dev/null; then
  aws ses update-receipt-rule --region "$REGION" \
    --rule-set-name "$RULE_SET_NAME" \
    --rule "$RULE_JSON"
  echo "Updated receipt rule"
else
  aws ses create-receipt-rule --region "$REGION" \
    --rule-set-name "$RULE_SET_NAME" \
    --rule "$RULE_JSON"
  echo "Created receipt rule"
fi

# Activate rule set
aws ses set-active-receipt-rule-set --rule-set-name "$RULE_SET_NAME" --region "$REGION"

rm -f lambda.zip
echo "=== Done ==="
echo ""
echo "Next steps:"
echo "  1. Add MX record on Namecheap: Host=agent  Type=MX  Value=10 inbound-smtp.us-east-1.amazonaws.com"
echo "  2. Add TXT record on Namecheap: Host=_amazonses.agent  Type=TXT  Value=${VERIFICATION_TOKEN}"
echo "  3. Store GitHub token: aws ssm put-parameter --name /agent/github-token --type SecureString --value ghp_YOUR_TOKEN --region $REGION"
echo "  4. Send a test email to post@agent.june.kim"
