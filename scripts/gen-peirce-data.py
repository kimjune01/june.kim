#!/usr/bin/env python3
"""Bake the Peirce viewer data for june.kim/peirce from the ~/Documents/peirce repo.

Reads: by-item page lists, the transcription .txt files, archive.org identifiers,
and clean titles from the Houghton finding-aid CSV. Emits public/peirce/data.json
(item index + page list + transcription text where it exists). Images are served
live from archive.org IIIF, so nothing binary is committed here.

Run from june.kim repo root:  python3 scripts/gen-peirce-data.py
"""
import os, re, csv, json

JK   = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PEI  = os.path.abspath(os.path.join(JK, "..", "peirce"))
BYI  = os.path.join(PEI, "houghton-export", "by-item")
TX   = os.path.join(PEI, "transcriptions")
OUT  = os.path.join(JK, "public", "peirce", "data.json")

# robin -> clean Houghton title
titles = {}
fa = os.path.join(PEI, "hollis", "hou02614-finding-aid.csv")
if os.path.exists(fa):
    rows = list(csv.reader(open(fa, newline="", encoding="utf-8")))
    hdr = rows[5]; idx = {c: i for i, c in enumerate(hdr)}
    for r in rows[6:]:
        ident = r[idx["Component Identifier"]] if idx["Component Identifier"] < len(r) else ""
        m = re.search(r"\((\d+[a-z]?)\)", ident)
        if m:
            t = (r[idx["Component Title"]] if idx["Component Title"] < len(r) else "").strip()
            t = re.sub(r"\s+", " ", t)
            t = re.sub(r"^Peirce, Charles S\. \(Charles Sanders\), 1839-1914\.\s*", "", t)
            t = re.split(r"\s+:\s+", t)[0].strip().strip(".")
            titles[m.group(1)] = t

# robin -> ia identifier
ia = {}
ref = os.path.join(PEI, "references", "archive-org-items.tsv")
if os.path.exists(ref):
    for row in csv.DictReader(open(ref), delimiter="\t"):
        ia[row["robin"]] = row["ia_identifier"]

def pretty(robin, folder):
    if titles.get(robin): return titles[robin]
    slug = re.sub(r"^\d+_?", "", folder).replace("-", " ").strip()
    return slug[:1].upper() + slug[1:] if slug else f"R{robin}"

items = []
for folder in sorted(os.listdir(BYI)):
    m = re.match(r"^(\d+|L\d+|REF)", folder)
    if not m: continue
    raw = m.group(1)
    robin = raw
    ident = ia.get(robin)
    if not ident:   # REF (Ketner bibliography) is not on archive.org -> skip
        continue
    d = os.path.join(BYI, folder)
    pages = []
    for x in sorted(f for f in os.listdir(d) if f.lower().endswith(".jpg")):
        img = os.path.splitext(x)[0]
        p = {"f": img}
        tp = os.path.join(TX, f"R{robin}", img + ".txt")
        if os.path.exists(tp):
            txt = open(tp, encoding="utf-8").read().strip()
            if txt: p["t"] = txt
        pages.append(p)
    if pages:
        items.append({"r": robin, "ia": ident,
                      "title": pretty(robin, folder), "pages": pages})

items.sort(key=lambda x: (0, int(x["r"])) if x["r"].isdigit() else (1, 0))
data = {
    "note": "Machine-assisted draft transcriptions, under correction. Page images "
            "are public-domain manuscripts hosted on the Internet Archive (CC0).",
    "items": items,
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
npages = sum(len(i["pages"]) for i in items)
ntx = sum(1 for i in items for p in i["pages"] if "t" in p)
print(f"wrote {OUT}: {len(items)} items, {npages} pages, {ntx} transcribed "
      f"({os.path.getsize(OUT)//1024} KB)")
