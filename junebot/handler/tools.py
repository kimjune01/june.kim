from __future__ import annotations

from pathlib import Path, PurePosixPath
import json
import re

_HERE = Path(__file__).parent

# Data and content layout differs between Lambda zip (flat) and local dev (repo):
#   Lambda:    /var/task/{data,content/blog,content/reading}
#   Local dev: junebot/data, src/content/blog, reading-src/pages/reading
if (_HERE / "content").exists():
    DATA = _HERE / "data"
    BLOG_DIR = _HERE / "content" / "blog"
    READING_DIR = _HERE / "content" / "reading"
else:
    DATA = _HERE.parent / "data"
    _REPO = _HERE.parents[2]
    BLOG_DIR = _REPO / "src" / "content" / "blog"
    READING_DIR = _REPO / "reading-src" / "pages" / "reading"


TOOL_SCHEMAS = [
    {
        "name": "read_post",
        "description": "Read the full body of a blog post by slug (e.g. '2026-03-14-the-parts-bin').",
        "input_schema": {
            "type": "object",
            "properties": {"slug": {"type": "string"}},
            "required": ["slug"],
        },
        "cache_control": {"type": "ephemeral"},
    },
    {
        "name": "read_reading",
        "description": "Read a reading-site page by its relative path (e.g. 'natural-breadcrumbs/kura-2026').",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
    {
        "name": "search",
        "description": "Fuzzy search the manifest by title, tag, or keyword. Returns matching entries.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
]

SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,160}$")


def _load_manifest() -> list[dict]:
    p = DATA / "manifest.json"
    return json.loads(p.read_text()) if p.exists() else []


def _safe_reading_path(path: str) -> PurePosixPath | None:
    rel = PurePosixPath(path)
    if rel.is_absolute() or not rel.parts or any(part in ("", ".", "..") for part in rel.parts):
        return None
    return rel


def read_post(slug: str) -> str:
    if not SLUG_RE.match(slug):
        return f"(invalid post slug '{slug}')"
    for ext in (".md", ".mdx"):
        f = BLOG_DIR / f"{slug}{ext}"
        if f.exists():
            return f.read_text()
        for f in BLOG_DIR.glob(f"????-??-??-{slug}{ext}"):
            return f.read_text()
    return f"(no post found for slug '{slug}')"


def read_reading(path: str) -> str:
    rel = _safe_reading_path(path)
    if rel is None:
        return f"(invalid reading path '{path}')"
    f = READING_DIR.joinpath(*rel.parts) / "index.astro"
    if f.exists():
        return f.read_text()
    return f"(no reading page at '{path}')"


def search(query: str) -> str:
    q = query.lower()
    if not q.strip():
        return "[]"
    hits = []
    for entry in _load_manifest():
        hay = " ".join(
            [
                entry.get("title", ""),
                entry.get("summary", ""),
                " ".join(entry.get("tags", []) or []),
                entry.get("slug", ""),
                entry.get("path", ""),
            ]
        ).lower()
        if all(tok in hay for tok in q.split()):
            hits.append(entry)
    return json.dumps(hits[:20], indent=2)


def dispatch(name: str, args: dict) -> str:
    try:
        if name == "read_post":
            return read_post(str(args["slug"]))
        if name == "read_reading":
            return read_reading(str(args["path"]))
        if name == "search":
            return search(str(args["query"])[:200])
        return f"(unknown tool: {name})"
    except Exception as exc:
        return f"(tool error in {name}: {type(exc).__name__})"
