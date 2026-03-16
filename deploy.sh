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

# ─── diff-only sync ─────────────────────────────────────────────────────────

echo "==> Staging _site/ for diff"
git add "$SITE_DIR/"

CHANGED=$(git diff --cached --name-only --diff-filter=ACMR -- "$SITE_DIR/")
DELETED=$(git diff --cached --name-only --diff-filter=D -- "$SITE_DIR/")

if [[ -z "$CHANGED" && -z "$DELETED" ]]; then
  echo "Nothing to deploy."
  git reset HEAD -- "$SITE_DIR/" >/dev/null 2>&1
  exit 0
fi

NCHANGED=$(echo "$CHANGED" | grep -c . || true)
NDELETED=$(echo "$DELETED" | grep -c . || true)
echo "    $NCHANGED changed, $NDELETED deleted"

if [[ $((NCHANGED + NDELETED)) -gt 50 ]]; then
  echo "==> Bulk sync to S3 (many files changed)"
  aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete --exclude "*.md"
  aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete --exclude "*" --include "*.md" \
    --content-type "text/plain; charset=utf-8" --no-guess-mime-type
else
  echo "==> Uploading changed files"
  while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    s3key="${file#$SITE_DIR/}"
    if [[ "$file" == *.md ]]; then
      aws s3 cp "$file" "s3://$BUCKET/$s3key" \
        --content-type "text/plain; charset=utf-8" --no-guess-mime-type --quiet
    else
      aws s3 cp "$file" "s3://$BUCKET/$s3key" --quiet
    fi
    echo "  + $s3key"
  done <<< "$CHANGED"

  if [[ -n "$DELETED" ]]; then
    echo "==> Deleting removed files"
    while IFS= read -r file; do
      [[ -z "$file" ]] && continue
      s3key="${file#$SITE_DIR/}"
      aws s3 rm "s3://$BUCKET/$s3key" --quiet
      echo "  - $s3key"
    done <<< "$DELETED"
  fi
fi

# Always upload feed.xml (gitignored but needed on S3)
aws s3 cp "$SITE_DIR/feed.xml" "s3://$BUCKET/feed.xml" --quiet
echo "    feed.xml synced"

# ─── CloudFront invalidation ────────────────────────────────────────────────

echo "==> Invalidating CloudFront cache"
PATHS=()
while IFS= read -r file; do
  [[ -z "$file" ]] && continue
  p="/${file#$SITE_DIR/}"
  PATHS+=("${p// /%20}")
done <<< "$CHANGED"
while IFS= read -r file; do
  [[ -z "$file" ]] && continue
  p="/${file#$SITE_DIR/}"
  PATHS+=("${p// /%20}")
done <<< "$DELETED"

if [[ ${#PATHS[@]} -gt 50 ]]; then
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
while IFS= read -r file; do
  [[ -z "$file" ]] && continue
  [[ "$file" != *.html ]] && continue
  # Only root-level .html files that have a matching .md (i.e. posts)
  [[ "$file" == */* && "${file#$SITE_DIR/}" == */* ]] && continue
  slug="${file#$SITE_DIR/}"
  slug="${slug%.html}"
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

# ─── commit _site/ ──────────────────────────────────────────────────────────

echo "==> Committing _site/"
git commit -m "Deploy _site" --no-verify -- "$SITE_DIR"

echo ""
echo "Deploy complete! Site is live at https://$DOMAIN_WWW"
