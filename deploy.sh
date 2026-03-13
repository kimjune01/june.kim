#!/usr/bin/env bash
set -euo pipefail

BUCKET="www.june.kim"
DOMAIN_WWW="www.june.kim"
SITE_DIR="_site"
CF_DIST_ID="E1G9R7V0YY4VV1"

# ─── deploy: build + sync ───────────────────────────────────────────────────

# Install Ruby 3.3.3 via rbenv if missing
if ! ruby -v 2>/dev/null | grep -q "3.3.3"; then
  echo "==> Installing Ruby 3.3.3 via rbenv"
  if ! command -v rbenv &>/dev/null; then
    echo "ERROR: rbenv not found. Install it first: brew install rbenv"
    exit 1
  fi
  rbenv install -s 3.3.3
  rbenv local 3.3.3
  eval "$(rbenv init -)"
fi
echo "==> Ruby $(ruby -v)"

echo "==> bundle install"
bundle install

echo "==> Building site"
JEKYLL_ENV=production bundle exec jekyll build

echo "==> Creating .html aliases for directory index pages"
find "$SITE_DIR" -name index.html -mindepth 2 | while read -r f; do
  dir="$(dirname "$f")"
  cp "$f" "$dir.html"
done

echo "==> Syncing to S3"
aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete

echo "==> Invalidating CloudFront cache"
aws cloudfront create-invalidation \
  --distribution-id "$CF_DIST_ID" \
  --paths "/*" \
  --no-cli-pager
echo "    Invalidation created for distribution $CF_DIST_ID"

echo ""
echo "Deploy complete! Site is live at https://$DOMAIN_WWW"
