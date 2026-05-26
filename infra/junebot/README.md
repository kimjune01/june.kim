# junebot infra

Pulumi stack for junebot. Run `pulumi up` here only when changing infrastructure
(IAM, Function URL, layers, SSM). Day-to-day code updates go through
`junebot/deploy-code.sh`, which is called from the root `deploy.sh`.

The runtime shape is: browser request to `https://june.kim/api/*` → CloudFront
behavior → Lambda Function URL with `AuthorizationType: AWS_IAM` and response
streaming. CloudFront signs origin requests via OAC. The raw Function URL is
not a public browser endpoint.

## First-time setup

```bash
# 1. Create a placeholder zip so the Lambda can be created.
cd infra/junebot
zip -q seed.zip <(echo '#!/bin/sh\nexec python3 -c "print(\"seed\")"') && mv seed.zip.bak seed.zip 2>/dev/null || \
  (mkdir -p _seed && echo '#!/bin/sh' > _seed/run.sh && cd _seed && zip -q ../seed.zip run.sh && cd .. && rm -rf _seed)

# 2. Bring up the stack.
pulumi stack init prod
pulumi up

# 3. Seed the Anthropic key into SSM.
aws ssm put-parameter --name /junebot/anthropic-api-key \
  --type SecureString --value "$ANTHROPIC_API_KEY" --overwrite

# 4. Push real code.
cd ../../junebot && bash deploy-code.sh

# 5. Ensure CloudFront routes /api/* to the function URL origin using OAC.
cd ../infra/junebot && pulumi stack output functionUrl
```

Set `PUBLIC_JUNEBOT_URL` to the site origin in the production build environment,
for example `https://june.kim`. The component appends `/api/chat` itself (see
`src/components/JuneBot.astro`). For local handler development, set it to
`http://localhost:8080`.
