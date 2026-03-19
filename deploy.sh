#!/usr/bin/env bash
set -euo pipefail

BUCKET="www.june.kim"
DOMAIN_WWW="june.kim"
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

# Copy static app builds into _site (excluded from Jekyll to preserve _astro dirs)
for app in pinyin-chart jamdojo; do
  if [[ -d "$app" ]]; then
    cp -r "$app" "$SITE_DIR/$app"
    echo "==> Copied $app into $SITE_DIR"
  fi
done

echo "==> Creating .html aliases for directory index pages"
find "$SITE_DIR" -name index.html -mindepth 2 | while read -r f; do
  dir="$(dirname "$f")"
  cp "$f" "$dir.html"
done

# ─── size-only sync ──────────────────────────────────────────────────────────

echo "==> Syncing to S3 (size-only, skip unchanged)"
aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete --exclude "*.md" --size-only
aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete --exclude "*" --include "*.md" \
  --content-type "text/plain; charset=utf-8" --no-guess-mime-type --size-only

# Collect what actually changed for CloudFront invalidation
CHANGED=$(aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete --size-only --dryrun 2>&1 \
  | grep -E "^(upload|delete):" \
  | sed 's|.*s3://[^/]*/|/|' \
  || true)

NCHANGED=$(echo "$CHANGED" | grep -c . 2>/dev/null || echo 0)
echo "    $NCHANGED files synced"

if [[ "$NCHANGED" -eq 0 ]]; then
  echo "Nothing changed on S3."
fi

# Always upload feed.xml (gitignored but needed on S3)
aws s3 cp "$SITE_DIR/feed.xml" "s3://$BUCKET/feed.xml" --quiet
echo "    feed.xml synced"

# ─── CloudFront invalidation ────────────────────────────────────────────────

echo "==> Invalidating CloudFront cache"
PATHS=()
while IFS= read -r p; do
  [[ -z "$p" ]] && continue
  PATHS+=("${p// /%20}")
done <<< "$CHANGED"

if [[ ${#PATHS[@]} -eq 0 ]]; then
  echo "    No paths to invalidate"
elif [[ ${#PATHS[@]} -gt 50 ]]; then
  aws cloudfront create-invalidation \
    --distribution-id "$CF_DIST_ID" \
    --paths "/*" \
    --no-cli-pager
  echo "    Invalidated /* (${#PATHS[@]} files changed)"
else
  aws cloudfront create-invalidation \
    --distribution-id "$CF_DIST_ID" \
    --paths "${PATHS[@]}" \
    --no-cli-pager
  echo "    Invalidated ${#PATHS[@]} path(s)"
fi

# ─── index on PageLeft ─────────────────────────────────────────────────────

echo "==> Indexing changed posts on PageLeft"
while IFS= read -r p; do
  [[ -z "$p" ]] && continue
  [[ "$p" != *.html ]] && continue
  # Only root-level .html files that have a matching .md (i.e. posts)
  slug="${p#/}"
  slug="${slug%.html}"
  [[ "$slug" == */* ]] && continue
  [[ -d "$SITE_DIR/$slug" ]] && continue
  [[ ! -f "$SITE_DIR/$slug.md" ]] && continue
  url="https://$DOMAIN_WWW/$slug"
  status=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST https://pageleft.cc/api/contribute/page \
    -H "Content-Type: application/json" \
    -d "{\"url\":\"$url\"}")
  echo "  $status $url"
  if [[ "$status" -lt 200 || "$status" -ge 300 ]]; then
    echo "ERROR: PageLeft indexing failed for $url (HTTP $status). Aborting deploy."
    git reset HEAD -- "$SITE_DIR/" >/dev/null 2>&1
    exit 1
  fi
done <<< "$CHANGED"


echo ""
echo "Deploy complete! Site is live at https://$DOMAIN_WWW"
