#!/usr/bin/env bash
set -euo pipefail

# Guard: jekyll serve rebuilds _site/ on changes, wiping .html aliases (lesson 14)
JEKYLL_PID=$(lsof -ti:4000 2>/dev/null || true)
if [[ -n "$JEKYLL_PID" ]]; then
  echo "ERROR: jekyll serve is running (PID $JEKYLL_PID) on port 4000."
  echo "       It will wipe .html aliases during deploy. Stop it first:"
  echo "       kill $JEKYLL_PID"
  exit 1
fi

BUCKET="www.june.kim"
DOMAIN_WWW="june.kim"
SITE_DIR="_site"
CF_DIST_ID="E1G9R7V0YY4VV1"
APPS=(pinyin-chart jamdojo reading)

# ─── lessons learned ──────────────────────────────────────────────────────────
# Each lesson cost a deploy cycle.
#
#  1. Use --size-only for S3 sync. Jekyll rebuilds every file with new
#     timestamps, so default (size + mtime) re-uploads everything.
#
#  2. Dryrun flags must match real sync flags exactly. --content-type in the
#     real sync but not the dryrun = wrong change count.
#
#  3. --size-only ignores metadata-only diffs. Good — avoids re-uploading
#     every .md after a one-time content-type fix.
#
#  4. Exclude .md from invalidation counts. Otherwise they trigger wildcard
#     invalidation (>50 files) and drown out actual changes.
#
#  5. S3 sync doesn't invalidate CloudFront. Separate API call required.
#
#  6. Jekyll incremental builds are unreliable. Always do full rebuilds.
#
#  7. S3 can be current while CloudFront is stale. Use git diff for
#     invalidation, not just S3 dryrun.
#
#  8. Astro apps content-hash filenames. Sync them separately, gated on
#     git diff, to avoid re-uploading hundreds of unchanged files.
#
#  9. --size-only misses same-size content changes. For blog posts, pull
#     invalidation paths from git diff on _posts/ AND assets/. For Astro
#     apps, --size-only is fatal: HTML files can be the same size but
#     reference different content-hashed CSS/JS filenames. Don't use
#     --size-only for the reading sync — always sync without it.
#
# 10. CloudFront treats / and /index.html as separate cache keys.
#     Invalidate both. Same for /feed.xml and /reading/ vs /reading/*.
#
# 11. Always invalidate / and /index.html. The homepage lists recent posts;
#     a new post changes it even when --size-only doesn't detect it.
#
# 12. Don't accumulate PATHS before PATHS=() is declared — the app sync
#     loop runs first and would get wiped. Use flags, add paths later.
#
# 13. .html aliases (about/index.html → about.html) must be created AFTER
#     all builds complete and verified before sync. A find|while pipe can
#     silently produce zero aliases if _site isn't fully populated yet.
#     Use process substitution + count check.
#
# 14. Kill `jekyll serve` before deploying. Livereload watches _site/ and
#     rebuilds on any change — including the .html aliases this script
#     creates. The rebuild wipes the aliases before sync can upload them,
#     so they never reach S3. Guard at the top of the script.
#
# 15. App sync without --size-only re-uploads everything. Astro outputs
#     content-hashed filenames, so checksums change on every build even
#     when content is identical. Use --size-only for apps too.
#
# 16. Blog sync --delete removes app .html aliases. The exclude pattern
#     "reading/*" protects the directory but not "reading.html" at the
#     root. Since alias creation skips app dirs, _site/reading.html never
#     exists locally, so --delete removes it from S3. Exclude "$app.html"
#     alongside "$app/*" for all apps.
#
# 17. Reading sync must compare built output, not just git HEAD. Astro
#     content-hashes filenames, so a rebuild produces new CSS/JS hashes
#     even when the source repo HEAD is unchanged (e.g. local reading/
#     dir was manually updated or rebuilt). Checking only git HEAD skips
#     the sync, leaving S3 with HTML that references non-existent CSS.
#     Fix: also compare reading/_astro/ hashes, or always sync reading
#     when the local reading/ dir is fresher than .reading-deployed.
# ──────────────────────────────────────────────────────────────────────────────

# ─── build ────────────────────────────────────────────────────────────────────

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

# ─── build reading site ──────────────────────────────────────────────────────
READING_DIR="$HOME/Documents/junekim-reading"
if [[ -d "$READING_DIR" ]]; then
  echo "==> Building reading site"
  (cd "$READING_DIR" && pnpm install --frozen-lockfile && pnpm build)
  rm -rf reading
  cp -r "$READING_DIR/dist/" reading/
  echo "    reading site built"
fi

# ─── create .html aliases (lesson 13) ────────────────────────────────────────
# CloudFront + S3 serves /about/ → about/index.html, but /about 404s unless
# about.html exists at the root. Create aliases for every directory index page.
# Uses process substitution (not pipe) so failures aren't swallowed.
# Excludes app dirs — they're synced separately and may contain stale Jekyll copies.
echo "==> Creating .html aliases for directory index pages"
FIND_EXCLUDES=()
for app in "${APPS[@]}"; do
  FIND_EXCLUDES+=(-not -path "$SITE_DIR/$app/*")
done
ALIAS_COUNT=0
while IFS= read -r f; do
  dir="$(dirname "$f")"
  cp "$f" "$dir.html"
  ALIAS_COUNT=$((ALIAS_COUNT + 1))
done < <(find "$SITE_DIR" -name index.html -mindepth 2 "${FIND_EXCLUDES[@]}")
echo "    $ALIAS_COUNT aliases created"
if [[ "$ALIAS_COUNT" -eq 0 ]]; then
  echo "WARNING: No aliases created — directory index pages may 404 without trailing slash"
fi

# ─── blog sync (excludes app dirs) ──────────────────────────────────────────

APP_EXCLUDES=()
for app in "${APPS[@]}"; do
  APP_EXCLUDES+=(--exclude "$app/*" --exclude "$app.html")
done

echo "==> Checking what changed (dryrun)"
CHANGED_HTML=$(aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete --size-only \
  --exclude "*.md" "${APP_EXCLUDES[@]}" --dryrun 2>&1 \
  | grep -E "^(upload|delete):" \
  | sed 's|.*s3://[^/]*/|/|' \
  || true)
CHANGED_MD=$(aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete --size-only \
  --exclude "*" --include "*.md" "${APP_EXCLUDES[@]}" \
  --content-type "text/plain; charset=utf-8" --no-guess-mime-type --dryrun 2>&1 \
  | grep -E "^(upload|delete):" \
  | sed 's|.*s3://[^/]*/|/|' \
  || true)
CHANGED=$(printf '%s\n%s' "$CHANGED_HTML" "$CHANGED_MD" | sed '/^$/d' || true)

echo "==> Syncing blog to S3"
aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete --size-only --exclude "*.md" "${APP_EXCLUDES[@]}"
aws s3 sync "$SITE_DIR/" "s3://$BUCKET/" --delete --size-only --exclude "*" --include "*.md" \
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

# Always upload feed.xml and sitemap (gitignored but needed on S3)
aws s3 cp "$SITE_DIR/feed.xml" "s3://$BUCKET/feed.xml" --quiet
aws s3 cp "$SITE_DIR/sitemap.xml" "s3://$BUCKET/sitemap.xml" --quiet 2>/dev/null || true
echo "    feed.xml synced"

# ─── app sync (only if changed) ──────────────────────────────────────────────

LAST_DEPLOYED=$(git rev-parse HEAD~1 2>/dev/null || echo "")
READING_SYNCED=false

for app in "${APPS[@]}"; do
  if [[ ! -d "$app" ]]; then
    continue
  fi
  if [[ "$app" == "reading" ]]; then
    # Gate on built output hash, not git HEAD (lesson 17)
    READING_BUILD_HASH=$(find reading/_astro -type f 2>/dev/null | sort | xargs cat | shasum -a 256 | cut -d' ' -f1)
    READING_DEPLOYED_HASH=$(cat .reading-deployed-hash 2>/dev/null || echo "")
    if [[ "$READING_BUILD_HASH" == "$READING_DEPLOYED_HASH" ]]; then
      echo "==> reading unchanged (build hash match), skipping sync"
    else
      echo "==> Syncing $app to S3"
      aws s3 sync "$app/" "s3://$BUCKET/$app/" --delete  # no --size-only (lesson 9)
      aws s3 cp "$app/index.html" "s3://$BUCKET/$app.html" --content-type "text/html; charset=utf-8" --quiet
      echo "$READING_BUILD_HASH" > .reading-deployed-hash
      echo "    $app synced"
      READING_SYNCED=true
    fi
  elif [[ -n "$LAST_DEPLOYED" ]] && git diff --quiet "$LAST_DEPLOYED" -- "$app/"; then
    echo "==> $app unchanged, skipping sync"
  else
    echo "==> Syncing $app to S3"
    aws s3 sync "$app/" "s3://$BUCKET/$app/" --delete --size-only
    echo "    $app synced"
  fi
done

# ─── CloudFront invalidation ────────────────────────────────────────────────

echo "==> Invalidating CloudFront cache"
PATHS=()
[[ "$READING_SYNCED" == true ]] && PATHS+=("/reading/" "/reading/*")
while IFS= read -r p; do
  [[ -z "$p" ]] && continue
  [[ "$p" == *.md ]] && continue
  PATHS+=("${p// /%20}")
done <<< "$CHANGED"

# Add paths from git diff for changed posts (slug.md → /slug)
if [[ -n "$LAST_DEPLOYED" ]]; then
  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    slug=$(basename "$f" .md | sed 's/^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}-//')
    [[ -z "$slug" ]] && continue
    PATHS+=("/$slug" "/$slug.html")
  done < <(git diff --name-only "$LAST_DEPLOYED" -- '_posts/' 2>/dev/null || true)

  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    PATHS+=("/$f")
  done < <(git diff --name-only "$LAST_DEPLOYED" -- 'assets/' 2>/dev/null || true)
fi

# Always invalidate homepage and feed
PATHS+=("/feed.xml" "/" "/index.html")

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

# ─── index on PageLeft ───────────────────────────────────────────────────────

echo "==> Indexing changed posts on PageLeft"
while IFS= read -r p; do
  [[ -z "$p" ]] && continue
  [[ "$p" != *.html ]] && continue
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
