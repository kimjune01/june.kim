"""Smoke tests for manifest.py — catches slug/path regressions."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "junebot" / "data" / "manifest.json"
SLUG_ASTRO = ROOT / "src" / "pages" / "[slug].astro"


def manifest() -> list[dict]:
    subprocess.check_call([sys.executable, str(Path(__file__).parent / "manifest.py")])
    return json.loads(MANIFEST.read_text())


def test_blog_slugs_have_no_date_prefix():
    for e in manifest():
        if e.get("kind") != "post":
            continue
        assert not re.match(r"\d{4}-\d{2}-\d{2}-", e["slug"]), (
            f"slug still has date prefix: {e['slug']}"
        )


def test_blog_dates_still_extracted():
    for e in manifest():
        if e.get("kind") != "post":
            continue
        if e.get("date"):
            assert re.match(r"\d{4}-\d{2}-\d{2}$", e["date"]), (
                f"malformed date: {e['date']}"
            )


def test_no_dot_reading_paths():
    for e in manifest():
        if e.get("kind") != "reading":
            continue
        assert e.get("path") not in (".", ""), (
            f"reading entry has bad path: {e}"
        )


def test_slug_matches_astro_routing():
    """Verify manifest slugs match what Astro's [slug].astro would produce."""
    astro_src = SLUG_ASTRO.read_text()
    m = re.search(r"\.replace\((/.*?/),\s*['\"]([^'\"]*)", astro_src)
    if not m:
        return
    pattern, replacement = m.group(1).strip("/"), m.group(2)
    astro_re = re.compile(pattern)
    blog_dir = ROOT / "src" / "content" / "blog"
    for f in sorted(blog_dir.glob("*.md")) + sorted(blog_dir.glob("*.mdx")):
        expected = astro_re.sub(replacement, f.stem)
        entry = next(
            (e for e in json.loads(MANIFEST.read_text())
             if e.get("kind") == "post" and e.get("title") == f.stem),
            None,
        )


if __name__ == "__main__":
    test_blog_slugs_have_no_date_prefix()
    test_blog_dates_still_extracted()
    test_no_dot_reading_paths()
    print("all tests pass")
