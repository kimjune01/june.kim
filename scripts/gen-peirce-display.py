#!/usr/bin/env python3
"""Self-host Peirce main-pane (1400px) display images.

The viewer's main pane loaded a 1400px derivative from archive.org's IIIF
resizer, which 504s at 60s and is the page's worst dependency. This script
re-encodes the local full-res captures (4032px JPEGs under the Houghton export)
to 1400px-wide WebP under public/peirce/display/{ia}/{f}.webp, so the reading
pane no longer touches archive.org. Idempotent: skips files already made.

Source is the local export, not S3/Glacier: originals live decoded as JPEGs at
  ~/Documents/peirce/houghton-export/by-item/{robin}_{slug}/IMG_####.jpg
and every page in data.json is present there (basenames are globally unique).

These images are large (~400MB) and are NOT committed. They are gitignored and
pushed straight to s3://www.june.kim/peirce/display/ (see deploy.sh, which
excludes that prefix from its --delete sync so it survives redeploys).

Usage:
  python3 scripts/gen-peirce-display.py            # all items
  python3 scripts/gen-peirce-display.py R475       # one or more items by Robin no.
"""
import json, os, sys, subprocess, concurrent.futures as cf

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA   = os.path.join(ROOT, "public/peirce/data.json")
OUT    = os.path.join(ROOT, "public/peirce/display")
SRCDIR = os.path.expanduser("~/Documents/peirce/houghton-export/by-item")
WIDTH  = "1400"   # cwebp -resize {WIDTH} 0 never upscales past the source

def build_index():
    """Map each capture basename (IMG_####) to its full-res JPEG path."""
    idx = {}
    for root, _, files in os.walk(SRCDIR):
        for f in files:
            if f.lower().endswith(".jpg"):
                idx[os.path.splitext(f)[0]] = os.path.join(root, f)
    return idx

def jobs(filt):
    d = json.load(open(DATA))
    for it in d["items"]:
        if filt and str(it["r"]) not in filt:
            continue
        for p in it["pages"]:
            yield it["ia"], p["f"]

def one(job):
    ia, f, src = job
    dst = os.path.join(OUT, ia, f + ".webp")
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        return ("skip", ia, f)
    if not src:
        return ("err:no-source", ia, f)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    try:
        # -q 80 is a clean read at 1400px; -resize caps width, height auto (0)
        subprocess.run(["cwebp", "-quiet", "-q", "80", "-resize", WIDTH, "0", src, "-o", dst],
                       check=True)
        return ("ok", ia, f)
    except Exception as e:
        return ("err:" + type(e).__name__, ia, f)

def main():
    filt = set(a.lstrip("R") if a.upper().startswith("R") else a for a in sys.argv[1:])
    idx = build_index()
    todo = [(ia, f, idx.get(f)) for ia, f in jobs(filt)]
    print(f"{len(todo)} display images to consider -> {OUT}")
    ok = skip = err = 0
    with cf.ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as ex:
        for i, (status, ia, f) in enumerate(ex.map(one, todo), 1):
            if status == "ok": ok += 1
            elif status == "skip": skip += 1
            else:
                err += 1
                print(f"  ! {status}  {ia}/{f}")
            if i % 100 == 0:
                print(f"  ...{i}/{len(todo)}  ok={ok} skip={skip} err={err}")
    print(f"done: ok={ok} skip={skip} err={err}")

if __name__ == "__main__":
    main()
