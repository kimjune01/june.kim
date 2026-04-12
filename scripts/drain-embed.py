#!/usr/bin/env python3
"""Drain the PageLeft embed work queue.

Claims chunks needing embeddings, computes them via PageLeft's HF-backed
/api/embed endpoint, and submits them back via /api/contribute/embeddings.

Stop conditions:
- Queue returns 0 items twice in a row (drained)
- Total chunks embedded reaches MAX_TOTAL
- 50 consecutive batches with no progress
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
import urllib.error

API = "https://pageleft.cc/api"
WORK_LIMIT = 10          # /work/embed returns up to 32 at a time; use 10 to reduce HF load
EMBED_BATCH = 10         # /api/embed max 32 per request; use 10 to avoid 502s under load
SUBMIT_BATCH = 100       # /api/contribute/embeddings max 100 per request
MAX_TOTAL = 10_000_000   # effectively unlimited — stop on drain, not cap
MAX_EMPTY = 2            # consecutive empty pulls before stop
MAX_NO_PROGRESS = 50     # consecutive batches with no accepted submissions
EMBED_RETRIES = 5        # retries on embed 502/timeout before giving up on batch


def http_json(url: str, data: bytes | None = None, timeout: int = 120):
    headers = {"Content-Type": "application/json"} if data else {}
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def fetch_work(n: int):
    for attempt in range(5):
        try:
            print(f"work fetch attempt {attempt+1}...", flush=True)
            result = http_json(f"{API}/work/embed?limit={n}", timeout=300)
            print(f"work fetch ok: {len(result.get('items', []))} items", flush=True)
            return result
        except Exception as e:
            if attempt == 4:
                raise
            wait = 2 ** attempt
            print(f"work fetch attempt {attempt+1} failed ({e}), retrying in {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError("unreachable")


def embed_texts(texts):
    body = json.dumps({"texts": texts}).encode()
    for attempt in range(EMBED_RETRIES):
        try:
            print(f"embedding {len(texts)} texts (attempt {attempt+1})...", flush=True)
            resp = http_json(f"{API}/embed", data=body, timeout=180)
            vecs = resp["embeddings"]
            print(f"embed ok: {len(vecs)} vectors", flush=True)
            return vecs
        except Exception as e:
            if attempt == EMBED_RETRIES - 1:
                raise
            wait = 2 ** attempt
            print(f"embed attempt {attempt+1} failed ({e}), retrying in {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError("unreachable")


def submit_embeddings(batch):
    body = json.dumps(batch).encode()
    return http_json(f"{API}/contribute/embeddings", data=body, timeout=60)


def get_stats():
    try:
        return http_json(f"{API}/stats", timeout=30)
    except Exception as e:
        return {"error": str(e)}


def chunked(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def main() -> int:
    total_accepted = 0
    consecutive_empty = 0
    consecutive_no_progress = 0
    errors = []

    while True:
        if total_accepted >= MAX_TOTAL:
            print(f"reached cap {MAX_TOTAL}", flush=True)
            break
        if consecutive_empty >= MAX_EMPTY:
            print("queue drained (two empty pulls in a row)", flush=True)
            break
        if consecutive_no_progress >= MAX_NO_PROGRESS:
            print(f"{MAX_NO_PROGRESS} batches with no progress, stopping", flush=True)
            break

        # 1. claim work
        try:
            work = fetch_work(WORK_LIMIT)
        except Exception as e:
            msg = f"work fetch failed: {e}"
            print(msg, flush=True)
            errors.append(msg)
            consecutive_no_progress += 1
            time.sleep(2)
            continue

        items = work.get("items", [])
        if not items:
            consecutive_empty += 1
            time.sleep(1)
            continue
        consecutive_empty = 0

        # 2. embed (chunk to EMBED_BATCH = 32)
        all_vectors = []
        embed_failed = False
        for group in chunked(items, EMBED_BATCH):
            texts = [it["text"] for it in group]
            try:
                vecs = embed_texts(texts)
            except Exception as e:
                msg = f"embed failed: {e}"
                print(msg, flush=True)
                errors.append(msg)
                embed_failed = True
                break
            all_vectors.extend(vecs)
        if embed_failed:
            consecutive_no_progress += 1
            time.sleep(2)
            continue

        # 3. submit (chunk to SUBMIT_BATCH = 100)
        payload = [
            {"chunk_id": it["chunk_id"], "embedding": vec}
            for it, vec in zip(items, all_vectors)
        ]

        batch_accepted = 0
        submit_failed = False
        for group in chunked(payload, SUBMIT_BATCH):
            try:
                result = submit_embeddings(group)
            except Exception as e:
                msg = f"submit failed: {e}"
                print(msg, flush=True)
                errors.append(msg)
                submit_failed = True
                break
            batch_accepted += result.get("accepted", 0)

        if submit_failed and batch_accepted == 0:
            consecutive_no_progress += 1
            time.sleep(2)
            continue

        total_accepted += batch_accepted
        if batch_accepted == 0:
            consecutive_no_progress += 1
        else:
            consecutive_no_progress = 0

    # final report
    stats = get_stats()
    print("---- DRAIN COMPLETE ----", flush=True)
    print(f"total_accepted: {total_accepted}", flush=True)
    print(f"stats: {json.dumps(stats, indent=2)}", flush=True)
    if errors:
        print(f"errors ({len(errors)}):", flush=True)
        for e in errors[-10:]:
            print(f"  {e}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
