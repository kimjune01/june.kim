#!/usr/bin/env bash
set -euo pipefail

BUCKET="www.june.kim"
CF_DIST_ID="E1G9R7V0YY4VV1"

echo "==> Building site"
pnpm build

# ─── .html aliases ──────────────────────────────────────────────────────────
# S3 serves /foo/ → foo/index.html, but /foo 404s unless foo.html exists.
# Create aliases so both /foo and /foo/ work.
echo "==> Creating .html aliases"
ALIAS_COUNT=0
while IFS= read -r f; do
  dir="$(dirname "$f")"
  cp "$f" "$dir.html"
  ALIAS_COUNT=$((ALIAS_COUNT + 1))
done < <(find dist -name index.html -mindepth 2)
echo "    $ALIAS_COUNT aliases created"

echo "==> Syncing to S3"
aws s3 sync dist/ "s3://$BUCKET/" --delete

echo "==> Invalidating CloudFront"
aws cloudfront create-invalidation \
  --distribution-id "$CF_DIST_ID" \
  --paths "/*" \
  --no-cli-pager

echo ""
echo "Deploy complete! Site is live at https://june.kim"
