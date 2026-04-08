#!/usr/bin/env python3
"""Drain the PageLeft frontier: claim URLs, submit to /api/contribute/page,
and reject failures via /api/frontier/reject so dead links stop cycling.

Usage:
    python3 -u scripts/drain-frontier.py              # run until frontier is exhausted
    python3 -u scripts/drain-frontier.py --batches 5  # run 5 batches then stop

Use -u for unbuffered output when redirecting to a file or running in background.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
import urllib.error
from urllib.parse import urlparse

API = "https://pageleft.cc"
BATCH_SIZE = 100
MAX_RETRIES_ON_EMPTY = 3

# Extensions the server already blocks, but we skip client-side to avoid
# wasting a round-trip on URLs that will always 422.
BINARY_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".ico",
    ".tiff", ".tif", ".avif", ".mp3", ".mp4", ".wav", ".ogg", ".webm",
    ".flac", ".avi", ".mov", ".mkv", ".zip", ".tar", ".gz", ".bz2",
    ".xz", ".rar", ".7z", ".exe", ".dll", ".so", ".dylib", ".bin",
    ".dmg", ".iso", ".deb", ".rpm", ".doc", ".docx", ".xls", ".xlsx",
    ".ppt", ".pptx", ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".css", ".js",
}


def is_binary(url: str) -> bool:
    path = urlparse(url).path.lower()
    return any(path.endswith(ext) for ext in BINARY_EXT)


def fetch_frontier(limit: int):
    try:
        resp = urllib.request.urlopen(f"{API}/api/frontier?limit={limit}", timeout=15)
        return json.loads(resp.read())
    except Exception:
        return None


def submit_page(url: str) -> tuple[bool, str]:
    """Submit a URL. Returns (success, error_reason)."""
    try:
        req = urllib.request.Request(
            f"{API}/api/contribute/page",
            data=json.dumps({"url": url}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=30)
        return True, ""
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        return False, body
    except Exception as e:
        return False, str(e)[:200]


def reject_urls(items: list[dict]):
    """Report failed URLs to /api/frontier/reject."""
    if not items:
        return
    try:
        req = urllib.request.Request(
            f"{API}/api/frontier/reject",
            data=json.dumps(items).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read())
        deleted = result.get("deleted", 0)
        learned = result.get("domains_learned", 0)
        if learned > 0:
            print(f"  reject: {deleted} deleted, {learned} domains learned")
    except urllib.error.HTTPError:
        # Endpoint not deployed yet — silently skip
        pass
    except Exception:
        pass


def run(max_batches: int | None = None):
    total_ok = 0
    total_fail = 0
    empty_runs = 0
    batch_num = 0

    while True:
        if max_batches is not None and batch_num >= max_batches:
            break

        batch_num += 1
        data = fetch_frontier(BATCH_SIZE)

        if not data:
            empty_runs += 1
            if empty_runs >= MAX_RETRIES_ON_EMPTY:
                print(f"Frontier empty or unavailable after {MAX_RETRIES_ON_EMPTY} retries.")
                break
            print(f"Batch {batch_num}: frontier empty, retrying in 3s...")
            time.sleep(3)
            continue

        empty_runs = 0
        ok = 0
        rejects = []

        for item in data:
            url = item["url"]

            if is_binary(url):
                rejects.append({"url": url, "reason": "binary extension"})
                continue

            success, reason = submit_page(url)
            if success:
                ok += 1
            else:
                # Only reject transient failures — "no copyleft license found"
                # is already handled server-side (domain learned + URL deleted).
                if "no copyleft license found" not in reason and "domain non-permissive" not in reason:
                    rejects.append({"url": url, "reason": reason[:100]})

        # Report rejects in a single batch
        reject_urls(rejects)

        total_ok += ok
        total_fail += len(data) - ok
        print(f"Batch {batch_num}: {ok} ok, {len(data) - ok} fail/skip (total: {total_ok} ok)")

        time.sleep(1)  # be polite

    print(f"\nDone: {total_ok} submitted, {total_fail} failed/skipped")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Drain the PageLeft frontier")
    parser.add_argument("--batches", type=int, default=None, help="Max batches to run (default: unlimited)")
    args = parser.parse_args()
    run(max_batches=args.batches)
