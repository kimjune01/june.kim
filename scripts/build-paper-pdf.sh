#!/usr/bin/env bash
# Build an arxiv-shape PDF from the methodeutic-harness paper.
#
# One-time setup:
#   brew install pandoc tectonic librsvg
#
# Usage:
#   bash scripts/build-paper-pdf.sh [source.md] [output.pdf]
# Defaults to the methodeutic-harness paper.

set -euo pipefail

SRC="${1:-src/content/blog/2026-05-28-the-methodeutic-harness-on-swebench-pro.md}"
OUT="${2:-public/assets/methodeutic-harness-paper.pdf}"
TMPDIR="$(mktemp -d -t paper-pdf.XXXXXX)"
trap 'rm -rf "$TMPDIR"' EXIT

mkdir -p "$(dirname "$OUT")"

echo "==> Rasterizing SVG figures to PNG (3600px wide)"
for svg in public/assets/methodeutic-harness.svg; do
  [ -f "$svg" ] || continue
  base="$(basename "$svg" .svg)"
  rsvg-convert -f png -w 3600 "$svg" -o "$TMPDIR/$base.png"
done

echo "==> Preprocessing markdown"
# Strip Astro YAML frontmatter; rewrite /assets/*.svg → tempdir PNGs;
# convert inline-math backticks for known math identifiers so pandoc renders LaTeX math.
sed '1{/^---$/!q;};1,/^---$/d' "$SRC" \
  | sed -E "s|/assets/([a-z0-9-]+)\.svg|$TMPDIR/\1.png|g" \
  | sed -E 's/`(S_n|p_0|p_1|p₀|p₁|ε|X_i|FAIL_TO_PASS|PASS_TO_PASS|H|T|N|K)`/$\1$/g' \
  | sed 's/✓/Y/g; s/·/—/g' \
  > "$TMPDIR/paper.md"

echo "==> Compiling with pandoc + tectonic"
pandoc "$TMPDIR/paper.md" \
  --from markdown+raw_html+pipe_tables+yaml_metadata_block \
  --to pdf \
  --pdf-engine=tectonic \
  --pdf-engine-opt=--keep-logs \
  -V documentclass=article \
  -V geometry:margin=1in \
  -V fontsize=10pt \
  -V mainfont="STIX Two Text" \
  -V monofont="Menlo" \
  -V linkcolor=blue \
  -V urlcolor=blue \
  -V title="The Methodeutic Harness on SWE-bench Pro" \
  -V subtitle="Hypothesis graphs as agent semantic memory, grounded in Peircean methodeutics" \
  -V author="June Kim" \
  -V date="2026-05-28" \
  --toc \
  --toc-depth=2 \
  --number-sections \
  -o "$OUT"

echo "==> Wrote $OUT"
ls -lh "$OUT"
