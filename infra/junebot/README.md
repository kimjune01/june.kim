# junebot infra

Pulumi stack for junebot. Run `pulumi up` here only when changing infrastructure
(IAM, Function URL, layers, SSM). Day-to-day code updates go through
`junebot/deploy-code.sh`, which is called from the root `deploy.sh`.

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

# 5. Grab the function URL and wire the frontend.
cd ../infra/junebot && pulumi stack output functionUrl
```

Set the URL on the frontend via `PUBLIC_JUNEBOT_URL` in the build environment
(see `src/components/JuneBot.astro`).
