#!/usr/bin/env bash
set -euo pipefail

BUCKET="www.june.kim"
CF_DIST_ID="E1G9R7V0YY4VV1"

echo "==> Building site"
pnpm build

if [ -x junebot/deploy-code.sh ]; then
  echo "==> Deploying junebot Lambda code"
  bash junebot/deploy-code.sh
fi

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

# ─── Cache-bust HTML byte length (S3-aware) ─────────────────────────────────
# `aws s3 sync --size-only` (below) compares files by byte length, not by
# content. When an Astro asset hash rotates (e.g. blog.BJesYFMI.css →
# blog.DR86DZLT.css), the HTML <link> tag changes but stays the same length,
# so the file gets silently skipped and visitors 404 the CSS.
#
# Approach: list S3 sizes once, then pad ONLY the HTML files whose local
# size happens to equal their S3 size. One-byte pad is enough to break the
# tie. Cost is ~1 byte per colliding file (~hundreds of bytes per deploy);
# no avg-page bloat. Asset files under _astro/ are content-hashed so
# --size-only is sound for them.
echo "==> Listing S3 sizes for collision check"
aws s3api list-objects-v2 --bucket "$BUCKET" \
  --query 'Contents[].[Key,Size]' --output text --no-cli-pager > /tmp/s3-sizes.tsv

echo "==> Pad-busting HTML on size collisions"
PAD_COUNT=0
while IFS= read -r f; do
  rel="${f#dist/}"
  local_size=$(wc -c < "$f" | tr -d ' ')
  s3_size=$(awk -F'\t' -v k="$rel" '$1==k {print $2; exit}' /tmp/s3-sizes.tsv)
  if [ -n "$s3_size" ] && [ "$s3_size" = "$local_size" ]; then
    printf ' ' >> "$f"
    PAD_COUNT=$((PAD_COUNT + 1))
  fi
done < <(find dist -name '*.html')
echo "    $PAD_COUNT files pad-busted"

echo "==> Syncing to S3"
aws s3 sync dist/ "s3://$BUCKET/" --delete --size-only

echo "==> Invalidating CloudFront"
aws cloudfront create-invalidation \
  --distribution-id "$CF_DIST_ID" \
  --paths "/*" \
  --no-cli-pager

echo ""
echo "Deploy complete! Site is live at https://june.kim"
