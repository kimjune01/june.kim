"""Build data/manifest.json — the 'directory listing' june-bot sees eagerly.

Each entry: {slug|path, kind, title, tags, summary, date}. Full bodies are
not included; the bot pages them in via read_post / read_reading tools."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BLOG = ROOT / "src" / "content" / "blog"
READING = ROOT / "src" / "pages" / "reading"
OUT = Path(__file__).resolve().parents[1] / "data" / "manifest.json"

FM_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FM_RE.match(text)
    if not m:
        return {}, text
    fm_raw, body = m.group(1), m.group(2)
    fm: dict = {}
    for line in fm_raw.splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip().strip('"')
    return fm, body


def first_prose_line(body: str, limit: int = 220) -> str:
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "import ", "<", "---", "```", "![")):
            continue
        s = re.sub(r"[*_`\[\]]", "", s)
        return s[:limit]
    return ""


def build_blog() -> list[dict]:
    out = []
    for f in sorted(BLOG.glob("*.md")) + sorted(BLOG.glob("*.mdx")):
        fm, body = parse_frontmatter(f.read_text())
        slug = f.stem
        tags = [t.strip() for t in re.split(r"[,\s]+", fm.get("tags", "")) if t.strip()]
        out.append(
            {
                "kind": "post",
                "slug": slug,
                "title": fm.get("title", slug),
                "tags": tags,
                "date": slug[:10] if re.match(r"\d{4}-\d{2}-\d{2}", slug) else None,
                "summary": first_prose_line(body),
            }
        )
    return out


def build_reading() -> list[dict]:
    out = []
    if not READING.exists():
        return out
    for f in sorted(READING.rglob("index.astro")):
        rel = f.parent.relative_to(READING).as_posix()
        if not rel:
            continue
        text = f.read_text()
        title = rel
        tm = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.DOTALL)
        if tm:
            title = re.sub(r"<[^>]+>", "", tm.group(1)).strip()
        out.append(
            {
                "kind": "reading",
                "path": rel,
                "title": title,
                "summary": first_prose_line(re.sub(r"<[^>]+>", " ", text)),
            }
        )
    return out


def main() -> None:
    manifest = build_blog() + build_reading()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2))
    print(f"wrote {len(manifest)} entries → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
