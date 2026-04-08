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

# ─── Cache-bust HTML byte length ────────────────────────────────────────────
# `aws s3 sync --size-only` (below) compares files by byte length, not by
# content. When an Astro asset hash rotates (e.g. blog.BJesYFMI.css →
# blog.DR86DZLT.css), the HTML <link> tag changes but stays the same length,
# so every static page silently keeps the stale reference and 404s the CSS.
# Workaround: append a random run of spaces to each .html so the byte length
# varies across deploys, forcing sync to upload it. `pnpm build` rewrites
# dist/ from scratch each run, so the padding doesn't accumulate.
# Asset files under _astro/ are content-hashed, so --size-only is still
# correct (and efficient) for them.
echo "==> Padding HTML to bust --size-only"
while IFS= read -r f; do
  pad=$((RANDOM % 64 + 1))
  printf '%*s' "$pad" '' >> "$f"
done < <(find dist -name '*.html')

echo "==> Syncing to S3"
aws s3 sync dist/ "s3://$BUCKET/" --delete --size-only

echo "==> Invalidating CloudFront"
aws cloudfront create-invalidation \
  --distribution-id "$CF_DIST_ID" \
  --paths "/*" \
  --no-cli-pager

echo ""
echo "Deploy complete! Site is live at https://june.kim"
