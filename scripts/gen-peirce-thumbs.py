#!/usr/bin/env python3
"""Self-host Peirce filmstrip thumbnails.

Downloads each page's small `_thumb.jpg` from the Internet Archive once and
re-encodes it to WebP under public/peirce/thumbs/{ia}/{f}.webp, so the viewer's
filmstrip no longer depends on archive.org (whose IIIF resizer 504s and whose
plain _thumb is an unoptimised 18KB JPEG). Idempotent: skips files already made.

Usage:
  python3 scripts/gen-peirce-thumbs.py            # all items
  python3 scripts/gen-peirce-thumbs.py R475       # one or more items by Robin no.
"""
import json, os, sys, subprocess, tempfile, urllib.request, concurrent.futures as cf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "public/peirce/data.json")
OUT  = os.path.join(ROOT, "public/peirce/thumbs")
DL   = "https://archive.org/download/{ia}/{f}_thumb.jpg"

def jobs(filt):
    d = json.load(open(DATA))
    for it in d["items"]:
        if filt and str(it["r"]) not in filt:
            continue
        for p in it["pages"]:
            yield it["ia"], p["f"]

def one(job):
    ia, f = job
    dst = os.path.join(OUT, ia, f + ".webp")
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        return ("skip", ia, f)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    url = DL.format(ia=ia, f=f)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "june.kim-peirce/1.0"})
        with urllib.request.urlopen(req, timeout=40) as r:
            raw = r.read()
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(raw); src = tmp.name
        # -q 78 is visually lossless at this size; -resize caps width at 200 (never upscales past source)
        subprocess.run(["cwebp", "-quiet", "-q", "78", "-resize", "200", "0", src, "-o", dst],
                       check=True)
        os.unlink(src)
        return ("ok", ia, f)
    except Exception as e:
        return ("err:" + type(e).__name__, ia, f)

def main():
    filt = set(a.lstrip("R") if a.upper().startswith("R") else a for a in sys.argv[1:])
    todo = list(jobs(filt))
    print(f"{len(todo)} thumbnails to consider -> {OUT}")
    ok = skip = err = 0
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
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
