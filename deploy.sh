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

# ─── sync ────────────────────────────────────────────────────────────────────
# No --size-only: jekyll rebuild changes timestamps on every file, but s3 sync
# default compares ETag (MD5) so only content-changed files actually upload.
# Dryrun first to collect what will change, then real sync.
#
# WHY DOES IT UPLOAD SO MANY FILES?
# Two separate issues:
# 1. Jekyll: incremental: false in _config.yml (incremental is unreliable).
#    Jekyll rebuilds every HTML, but most pages have static content so their
#    ETag doesn't change. S3 sync skips them. Only ~10-15 HTML files actually
#    re-upload per deploy (index, feed, tag pages, sitemap, new post).
# 2. Markdown: the second sync forces --content-type "text/plain; charset=utf-8".
#    S3 sync compares metadata too, not just ETag. If the stored content-type
#    doesn't match, every .md re-uploads even with identical content.
#    Fix: dryrun must use the same flags as the real sync (see below).

echo "==> Checking what changed (ETag compare)"
# Dryrun for non-md files (HTML, CSS, JS, images)
CHANGED_HTML=$(aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete --exclude "*.md" --dryrun 2>&1 \
  | grep -E "^(upload|delete):" \
  | sed 's|.*s3://[^/]*/|/|' \
  || true)
# Dryrun for md files (same flags as real sync to avoid false positives)
CHANGED_MD=$(aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete --exclude "*" --include "*.md" \
  --content-type "text/plain; charset=utf-8" --no-guess-mime-type --dryrun 2>&1 \
  | grep -E "^(upload|delete):" \
  | sed 's|.*s3://[^/]*/|/|' \
  || true)
CHANGED=$(printf '%s\n%s' "$CHANGED_HTML" "$CHANGED_MD" | sed '/^$/d' || true)

echo "==> Syncing to S3"
aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete --exclude "*.md"
aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete --exclude "*" --include "*.md" \
  --content-type "text/plain; charset=utf-8" --no-guess-mime-type

if [[ -z "$CHANGED" ]]; then
  NCHANGED=0
else
  NCHANGED=$(echo "$CHANGED" | wc -l | tr -d ' ')
fi
NCHANGED_CONTENT=$(echo "$CHANGED" | grep -v '\.md$' | grep -c . || true)
echo "    $NCHANGED files synced ($NCHANGED_CONTENT content, $((NCHANGED - NCHANGED_CONTENT)) metadata-only .md)"

if [[ "$NCHANGED_CONTENT" -eq 0 ]]; then
  echo "No content changes on S3."
fi

# Always upload feed.xml (gitignored but needed on S3)
aws s3 cp "$SITE_DIR/feed.xml" "s3://$BUCKET/feed.xml" --quiet
echo "    feed.xml synced"

# ─── CloudFront invalidation ────────────────────────────────────────────────
# Only invalidate non-.md files. Markdown uploads are metadata fixes (content-type),
# not content changes — they don't need cache busting or PageLeft indexing.

echo "==> Invalidating CloudFront cache"
PATHS=()
while IFS= read -r p; do
  [[ -z "$p" ]] && continue
  [[ "$p" == *.md ]] && continue
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
