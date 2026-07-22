#!/usr/bin/env python3
"""Cached Algolia HN fetcher. Import it, or call it from the shell.

Cache lives in /tmp/hn-cache/ keyed by URL hash. TTLs are short on purpose:
the point is to stop refetching the same thread five times inside one run,
and to make a rerun ten minutes later nearly free, not to serve stale threads.

    python3 hnfetch.py <url>            # print JSON, using cache
    python3 hnfetch.py --ttl 60 <url>   # override TTL in seconds
    python3 hnfetch.py --purge          # drop expired entries

    from hnfetch import get, item, search
"""
import hashlib, json, os, sys, time, urllib.parse, urllib.request

CACHE = os.environ.get("HN_CACHE_DIR", "/tmp/hn-cache")
# items churn as comments arrive; searches churn slower.
TTL_ITEM = 600
TTL_SEARCH = 1800


def _path(url):
    return os.path.join(CACHE, hashlib.sha256(url.encode()).hexdigest()[:24] + ".json")


def get(url, ttl=None):
    if ttl is None:
        ttl = TTL_ITEM if "/items/" in url else TTL_SEARCH
    os.makedirs(CACHE, exist_ok=True)
    p = _path(url)
    if ttl > 0 and os.path.exists(p) and time.time() - os.path.getmtime(p) < ttl:
        try:
            return json.load(open(p))
        except Exception:
            pass
    d = json.load(urllib.request.urlopen(url, timeout=30))
    tmp = p + ".tmp"
    json.dump(d, open(tmp, "w"))
    os.replace(tmp, p)  # atomic, so parallel subagents never read a half-written file
    return d


def item(object_id, ttl=None):
    return get(f"https://hn.algolia.com/api/v1/items/{object_id}", ttl)


def search(query, tags="story", cutoff_hours=48, hits=30, ttl=None):
    cut = int(time.time()) - cutoff_hours * 3600
    q = urllib.parse.quote(query)
    return get(
        f"https://hn.algolia.com/api/v1/search?query={q}&tags={tags}"
        f"&numericFilters=created_at_i%3E{cut}&hitsPerPage={hits}",
        ttl,
    )


def purge():
    if not os.path.isdir(CACHE):
        return 0
    n = 0
    for f in os.listdir(CACHE):
        p = os.path.join(CACHE, f)
        if time.time() - os.path.getmtime(p) > max(TTL_ITEM, TTL_SEARCH):
            os.remove(p)
            n += 1
    return n


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--purge":
        print(f"purged {purge()}")
        sys.exit()
    ttl = None
    if a and a[0] == "--ttl":
        ttl = int(a[1])
        a = a[2:]
    print(json.dumps(get(a[0], ttl)))
