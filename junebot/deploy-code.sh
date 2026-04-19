#!/usr/bin/env bash
# Update Lambda function code. Called from ../deploy.sh.
# Infra (IAM, Function URL, layers) is managed by Pulumi — don't touch here.
set -euo pipefail

cd "$(dirname "$0")"

FUNCTION_NAME="${JUNEBOT_FUNCTION_NAME:-junebot}"
REGION="${AWS_REGION:-us-east-1}"

bash build-zip.sh

echo "==> Updating Lambda function code: $FUNCTION_NAME"
aws lambda update-function-code \
  --function-name "$FUNCTION_NAME" \
  --zip-file "fileb://junebot.zip" \
  --region "$REGION" \
  --no-cli-pager >/dev/null

echo "==> junebot code deployed"
