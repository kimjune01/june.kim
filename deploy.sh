#!/usr/bin/env bash
set -euo pipefail

BUCKET="www.june.kim"
CF_DIST_ID="E1G9R7V0YY4VV1"

echo "==> Building site"
pnpm build

# junebot Lambda is the heaviest step (manifest rebuild + pip wheels + ~29 MB
# zip + upload) and has nothing to do with a post edit. Only repackage+upload it
# when junebot/ actually changed since it was last deployed (marker tag
# `junebot-deployed`), or when forced with DEPLOY_JUNEBOT=1. Kept non-fatal so a
# Lambda upload hiccup never aborts the site deploy.
if [ -x junebot/deploy-code.sh ]; then
  deploy_junebot=skip
  if [ "${DEPLOY_JUNEBOT:-}" = "1" ]; then
    deploy_junebot=forced
  elif git rev-parse -q --verify refs/tags/junebot-deployed >/dev/null 2>&1; then
    git diff --quiet refs/tags/junebot-deployed -- junebot/ || deploy_junebot=changed
  else
    echo "==> junebot: no baseline marker; skipping (run DEPLOY_JUNEBOT=1 to deploy and set baseline)"
  fi

  if [ "$deploy_junebot" != skip ]; then
    echo "==> Deploying junebot Lambda code ($deploy_junebot)"
    if bash junebot/deploy-code.sh; then
      git tag -f junebot-deployed HEAD >/dev/null
      echo "    junebot deployed; baseline marker -> $(git rev-parse --short HEAD)"
    else
      echo "    WARNING: junebot deploy failed; continuing with site deploy (marker unchanged)" >&2
    fi
  elif [ "${DEPLOY_JUNEBOT:-}" != "1" ] && git rev-parse -q --verify refs/tags/junebot-deployed >/dev/null 2>&1; then
    echo "==> junebot unchanged since last deploy; skipping Lambda code update"
  fi
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

# ─── HTML content sync ──────────────────────────────────────────────────────
# Lessons learned:
# - Never mutate `dist` just to make a deploy tool notice a change. The old
#   pad-byte workaround solved one missed-update bug but created a new
#   deploy-churn bug: every fresh build removed the padding, so the next deploy
#   saw hundreds of artificial size changes.
# - HTML is not a content-addressed artifact in this build. It can change while
#   staying the same byte length, especially when hashed asset names rotate to
#   another hash of equal length. Therefore HTML must be compared by content,
#   not by size.
# - Non-HTML assets are different: generated asset filenames are content-hashed,
#   so `--size-only` remains a pragmatic fast path for those files.
# - A one-time normalization deploy may upload many HTML files to remove the old
#   padding state. After that, unchanged HTML should produce zero uploads. If a
#   future edit breaks that invariant, fix the comparison logic; do not bring
#   back padding or timestamp-based HTML sync.
#
# `aws s3 sync --size-only` is good for hashed assets, but not HTML:
# an Astro asset hash can rotate from one same-length filename to another,
# changing the HTML without changing byte length.
#
# The old workaround appended a byte to same-sized HTML files. That forced
# uploads, but also made deploys alternate between padded and unpadded output:
# build regenerates clean HTML, deploy pads it, next build removes the padding,
# and `--size-only` uploads most pages again.
#
# Instead, compare HTML by content hash against the S3 ETag. HTML files are
# small single-part uploads, so their ETag is the MD5 of the uploaded body.
# Non-HTML files still use size-only sync; content-hashed asset filenames make
# that safe and fast.
echo "==> Listing S3 objects for HTML sync"
aws s3api list-objects-v2 --bucket "$BUCKET" \
  --query 'Contents[].[Key,Size,ETag]' --output text --no-cli-pager > /tmp/s3-objects.tsv

md5_file() {
  if command -v md5sum >/dev/null 2>&1; then
    md5sum "$1" | awk '{print $1}'
  else
    md5 -q "$1"
  fi
}

echo "==> Syncing HTML by content"
HTML_UPLOAD_COUNT=0
find dist -name '*.html' | sed 's#^dist/##' | sort > /tmp/local-html-keys.txt
awk -F'\t' '$1 ~ /\.html$/ {print $1}' /tmp/s3-objects.tsv | sort > /tmp/remote-html-keys.txt

while IFS= read -r f; do
  rel="${f#dist/}"
  local_md5=$(md5_file "$f")
  s3_etag=$(awk -F'\t' -v k="$rel" '$1==k {gsub(/"/, "", $3); print $3; exit}' /tmp/s3-objects.tsv)
  if [ "$s3_etag" != "$local_md5" ]; then
    aws s3 cp "$f" "s3://$BUCKET/$rel" --only-show-errors
    HTML_UPLOAD_COUNT=$((HTML_UPLOAD_COUNT + 1))
  fi
done < <(find dist -name '*.html')
echo "    $HTML_UPLOAD_COUNT HTML files uploaded"

echo "==> Deleting stale HTML"
HTML_DELETE_COUNT=0
while IFS= read -r key; do
  aws s3 rm "s3://$BUCKET/$key" --only-show-errors
  HTML_DELETE_COUNT=$((HTML_DELETE_COUNT + 1))
done < <(comm -23 /tmp/remote-html-keys.txt /tmp/local-html-keys.txt)
echo "    $HTML_DELETE_COUNT stale HTML files deleted"

echo "==> Syncing non-HTML to S3"
aws s3 sync dist/ "s3://$BUCKET/" --delete --size-only --exclude "*.html" --exclude "*.DS_Store" --exclude "*.pytest_cache/*"

echo "==> Invalidating CloudFront"
aws cloudfront create-invalidation \
  --distribution-id "$CF_DIST_ID" \
  --paths "/*" \
  --no-cli-pager

echo ""
echo "Deploy complete! Site is live at https://june.kim"
