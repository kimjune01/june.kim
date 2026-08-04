#!/bin/bash
# De-sepia scaled to each image's measured warmth.
# Warmth = (VAVG-128)-(UAVG-128) from ffmpeg signalstats; sepia images score ~30-50.
# Treatment: gray-world colorcorrect (60%) + colortemperature + yellow/red desaturation,
# the latter two scaled linearly by warmth (no-op below warmth 12).
# Usage: desepia.sh <src_dir> <dst_dir>
# Last run: 2026-08-02, over all 84 images then in public/folk/art (originals -> in place).
set -euo pipefail
SRC=$1; DST=$2
while IFS= read -r -d '' f; do
  rel=${f#"$SRC"/}
  out="$DST/$rel"
  mkdir -p "$(dirname "$out")"
  uavg_vavg=$(ffprobe -v error -f lavfi "movie=$f,signalstats" \
    -show_entries frame_tags=lavfi.signalstats.UAVG,lavfi.signalstats.VAVG -of csv=p=0 | head -1)
  read -r warmth sat temp <<<"$(echo "$uavg_vavg" | awk -F, '{
    w = ($2-128)-($1-128)
    s = (w-12)*0.012; if (s<0) s=0; if (s>0.45) s=0.45
    t = 6500 + w*85;  if (t<6500) t=6500; if (t>11000) t=11000
    printf "%.1f %.3f %.0f", w, s, t }')"
  tmp=$(mktemp -t desepia).png
  ffmpeg -hide_banner -loglevel error -y -i "$f" -filter_complex \
    "[0:v]split[a][b];[b]colorcorrect=analyze=average[c];[a][c]blend=all_mode=normal:all_opacity=0.6,colortemperature=temperature=$temp:pl=0.9,huesaturation=saturation=-$sat:colors=y+r:strength=8" \
    "$tmp"
  cwebp -quiet -q 95 "$tmp" -o "$out"
  rm -f "$tmp"
  printf "warmth %5s  sat -%s  temp %sK  %s\n" "$warmth" "$sat" "$temp" "$rel"
done < <(find "$SRC" -name '*.webp' -not -path '* *' -print0 | sort -z)
