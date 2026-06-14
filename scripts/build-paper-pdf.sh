#!/usr/bin/env bash
# Build an arxiv-shape PDF from any paper's markdown source.
#
# One-time setup:
#   brew install pandoc tectonic librsvg
#
# Usage:
#   bash scripts/build-paper-pdf.sh <source.md> [output.pdf]
#
#   e.g. bash scripts/build-paper-pdf.sh \
#          src/content/blog/2026-05-28-the-hypothesis-graph-semantic-memory-methodeutics.md
#
# Output defaults to public/assets/<slug>.pdf, where <slug> is the source
# basename with any leading YYYY-MM-DD- date prefix stripped. Title, subtitle,
# and date are read from the source's YAML frontmatter / filename, so the script
# is paper-agnostic: point it at any of the papers in the pipeline.

set -euo pipefail

SRC="${1:?usage: build-paper-pdf.sh <source.md> [output.pdf]}"
[ -f "$SRC" ] || { echo "source not found: $SRC" >&2; exit 1; }

base="$(basename "$SRC" .md)"
slug="${base#[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-}"   # strip leading date
OUT="${2:-public/assets/$slug.pdf}"

TMPDIR="$(mktemp -d -t paper-pdf.XXXXXX)"
trap 'rm -rf "$TMPDIR"' EXIT
mkdir -p "$(dirname "$OUT")"

# --- read title / subtitle / date from the source itself ---
FM="$(awk 'NR==1 && $0=="---"{f=1;next} f && $0=="---"{exit} f{print}' "$SRC")"
fmval(){ printf '%s\n' "$FM" | sed -n "s/^$1: *//p" | head -1 | sed -e 's/^"//' -e 's/"$//'; }
TITLE="$(fmval title)";    TITLE="${TITLE:-$slug}"
SUBTITLE="$(fmval subtitle)"
DATE="$(printf '%s' "$base" | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2}' || true)"

echo "==> Building '$TITLE'"
echo "    source: $SRC"
echo "    output: $OUT"

echo "==> Rasterizing the SVG figures this paper references (3600px wide)"
grep -oE '/assets/[a-z0-9-]+\.svg' "$SRC" | sort -u | while read -r ref; do
  svg="public$ref"; bn="$(basename "$ref" .svg)"
  [ -f "$svg" ] || { echo "    missing $svg, skipping" >&2; continue; }
  rsvg-convert -f png -w 3600 "$svg" -o "$TMPDIR/$bn.png"
done

echo "==> Preprocessing markdown"
# Strip Astro YAML frontmatter; rewrite /assets/*.svg -> tempdir PNGs; turn the
# raw-HTML <figure>/<img> blocks into markdown images so pandoc actually embeds
# the rasterized figures; convert inline-math backticks for common math
# identifiers; fold glyphs the PDF font lacks (arrows, >=, check/cross) to ASCII.
sed '1{/^---$/!q;};1,/^---$/d' "$SRC" \
  | sed -E "s|/assets/([a-z0-9-]+)\.svg|$TMPDIR/\1.png|g" \
  | sed -E 's#<img[^>]*src="([^"]+)"[^>]*>#\n![](\1)\n#g' \
  | sed -E 's#</?figure[^>]*>##g; s#</?figcaption[^>]*>##g' \
  | sed -E 's/`(S_n|p_0|p_1|p₀|p₁|ε|X_i|FAIL_TO_PASS|PASS_TO_PASS|H|T|N|K)`/$\1$/g' \
  | sed 's/✓/Y/g; s/✗/N/g; s/◐/~/g; s/·/—/g; s/→/->/g; s/⇒/=>/g; s/≥/>=/g; s/≤/<=/g' \
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
  -V title="$TITLE" \
  ${SUBTITLE:+-V subtitle="$SUBTITLE"} \
  -V author="June Kim" \
  ${DATE:+-V date="$DATE"} \
  --toc \
  --toc-depth=2 \
  --number-sections \
  -o "$OUT"

echo "==> Wrote $OUT"
ls -lh "$OUT"
