#!/usr/bin/env bash
set -euo pipefail

BUCKET="www.june.kim"
DOMAIN_WWW="june.kim"
SITE_DIR="_site"
CF_DIST_ID="E1G9R7V0YY4VV1"
APPS=(pinyin-chart jamdojo)

# ─── lessons learned ──────────────────────────────────────────────────────────
# Static site deploy sounds simple. It isn't. Each lesson cost a deploy cycle.
#
# 1. S3 sync compares size + last-modified time by default, NOT ETag.
#    Jekyll rebuilds every file with new timestamps, so every file looks
#    newer. Use --size-only for HTML: identical content = identical size.
#
# 2. Dryrun flags must match real sync flags exactly. The .md sync forces
#    --content-type, which makes S3 compare metadata too. A dryrun without
#    those flags reports 0 changes while the real sync uploads 298 files.
#
# 3. S3 sync compares ETag AND metadata. Identical content with different
#    content-type = "changed" file. Every .md re-uploads until the stored
#    metadata matches. This is a one-time cost per flag change, not a bug.
#
# 4. .md uploads are metadata-only — exclude them from invalidation and
#    change counts. Otherwise they trigger wildcard invalidation (>50 files)
#    and drown out the actual new post.
#
# 5. CloudFront invalidation is a separate API call. S3 sync doesn't
#    trigger it. If the change list is wrong, the new post stays cached.
#
# 6. Jekyll incremental builds (incremental: true) are unreliable and
#    disabled. Every build regenerates all HTML. Most pages don't change
#    content, so ETag comparison handles it. Don't re-enable incremental.
#
# 7. S3 dryrun can report "0 changes" when the content is already uploaded
#    but CloudFront still caches the old version. Use git diff to find changed
#    posts and force-invalidate them regardless of what S3 says.
#
# 8. Astro apps (jamdojo, pinyin-chart) content-hash filenames. Copying them
#    into _site and running one global sync means every deploy re-uploads
#    ~581 files even when the apps haven't changed. Fix: sync apps separately,
#    gated on git diff.
# ──────────────────────────────────────────────────────────────────────────────

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

# ─── blog sync (excludes app dirs) ──────────────────────────────────────────

# Build exclude flags for apps
APP_EXCLUDES=()
for app in "${APPS[@]}"; do
  APP_EXCLUDES+=(--exclude "$app/*")
done

echo "==> Checking what changed (ETag compare)"
# Dryrun for non-md, non-app files
CHANGED_HTML=$(aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete --size-only \
  --exclude "*.md" "${APP_EXCLUDES[@]}" --dryrun 2>&1 \
  | grep -E "^(upload|delete):" \
  | sed 's|.*s3://[^/]*/|/|' \
  || true)
# Dryrun for md files (same flags as real sync to avoid false positives)
CHANGED_MD=$(aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete \
  --exclude "*" --include "*.md" "${APP_EXCLUDES[@]}" \
  --content-type "text/plain; charset=utf-8" --no-guess-mime-type --dryrun 2>&1 \
  | grep -E "^(upload|delete):" \
  | sed 's|.*s3://[^/]*/|/|' \
  || true)
CHANGED=$(printf '%s\n%s' "$CHANGED_HTML" "$CHANGED_MD" | sed '/^$/d' || true)

echo "==> Syncing blog to S3"
aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete --size-only --exclude "*.md" "${APP_EXCLUDES[@]}"
aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete --exclude "*" --include "*.md" \
  "${APP_EXCLUDES[@]}" --content-type "text/plain; charset=utf-8" --no-guess-mime-type

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

# ─── app sync (only if changed) ────────────────────────────────────────────
# Apps use content-hashed filenames (Astro). Syncing them every deploy uploads
# hundreds of files. Only sync when git shows changes in the app dir.

LAST_DEPLOYED=$(git rev-parse HEAD~1 2>/dev/null || echo "")

for app in "${APPS[@]}"; do
  if [[ ! -d "$app" ]]; then
    continue
  fi
  if [[ -n "$LAST_DEPLOYED" ]] && git diff --quiet "$LAST_DEPLOYED" -- "$app/"; then
    echo "==> $app unchanged, skipping sync"
  else
    echo "==> Syncing $app to S3"
    aws s3 sync "$app/" "s3://$BUCKET/$app/" --delete
    echo "    $app synced"
  fi
done

# ─── CloudFront invalidation ────────────────────────────────────────────────
# Two sources of invalidation paths:
# 1. S3 dryrun (what actually changed on S3)
# 2. Git diff (what changed in the commit — catches the case where S3 already
#    has the new content from a prior deploy but CloudFront still caches the old)

echo "==> Invalidating CloudFront cache"
PATHS=()
while IFS= read -r p; do
  [[ -z "$p" ]] && continue
  [[ "$p" == *.md ]] && continue
  PATHS+=("${p// /%20}")
done <<< "$CHANGED"

# Add paths from git diff for changed posts (slug.md → /slug)
if [[ -n "$LAST_DEPLOYED" ]]; then
  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    # Extract slug from _posts/YYYY/YYYY-MM-DD-slug.md
    slug=$(basename "$f" .md | sed 's/^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}-//')
    [[ -z "$slug" ]] && continue
    PATHS+=("/$slug" "/$slug.html")
  done < <(git diff --name-only "$LAST_DEPLOYED" -- '_posts/' 2>/dev/null || true)
fi
# Deduplicate
PATHS=($(printf '%s\n' "${PATHS[@]}" | sort -u))

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
