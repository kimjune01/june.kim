#!/usr/bin/env bash
# Package junebot Lambda zip: handler code + data (manifest, about_june.md)
# + content snapshot (blog posts, reading pages) + pip deps.
set -euo pipefail

cd "$(dirname "$0")"
ROOT="$(cd .. && pwd)"
BUILD=".build"
ZIP="junebot.zip"

echo "==> Rebuilding manifest"
python3 build/manifest.py

if [ ! -f data/about_june.md ]; then
  echo "WARN: data/about_june.md missing. Run: python3 junebot/build/distill.py"
fi

echo "==> Assembling zip staging dir"
rm -rf "$BUILD" "$ZIP"
mkdir -p "$BUILD/content/blog" "$BUILD/content/reading" "$BUILD/data"

cp handler/*.py "$BUILD/"
cp -r data/* "$BUILD/data/" 2>/dev/null || true

# Content snapshot — bot loads these via tool calls
cp "$ROOT/src/content/blog/"*.md "$BUILD/content/blog/" 2>/dev/null || true
cp "$ROOT/src/content/blog/"*.mdx "$BUILD/content/blog/" 2>/dev/null || true
if [ -d "$ROOT/src/pages/reading" ]; then
  rsync -a --include='*/' --include='index.astro' --exclude='*' \
    "$ROOT/src/pages/reading/" "$BUILD/content/reading/"
fi

echo "==> Installing deps into staging dir (linux x86_64 wheels)"
python3 -m pip install --quiet --target "$BUILD" \
  --platform manylinux2014_x86_64 \
  --python-version 3.11 \
  --only-binary=:all: \
  --upgrade \
  -r <(
  cat <<EOF
anthropic>=0.40
fastapi>=0.115
uvicorn>=0.32
boto3>=1.35
EOF
)

# Lambda Web Adapter reads AWS_LWA_* env vars; bootstrap launches uvicorn.
cat > "$BUILD/run.sh" <<'EOF'
#!/bin/sh
exec python3 -m uvicorn app:app --host 0.0.0.0 --port 8080
EOF
chmod +x "$BUILD/run.sh"

echo "==> Zipping"
cd "$BUILD"
zip -qr "../$ZIP" .
cd ..
SIZE=$(du -h "$ZIP" | cut -f1)
echo "==> Built $ZIP ($SIZE)"
