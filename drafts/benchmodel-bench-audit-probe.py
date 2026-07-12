#!/usr/bin/env python3
"""Boilerplate probe for benchmodel-bench (see benchmodel-bench-audit.md).

Scores 20 generic, answer-key-blind code-review findings against every
suites/*/bug_index*.json with the repo's own scorer.py. Run from a clone root:

    python3 benchmodel-bench-audit-probe.py /path/to/benchmodel-bench

Expected at the audited HEAD (2026-07-10): 107/167 bugs detected (64%),
positive raw score on 17/41 keys.
"""
import glob
import importlib.util
import json
import sys
from pathlib import Path

repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
spec = importlib.util.spec_from_file_location("scorer", repo / "scorer.py")
scorer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scorer)

BOILERPLATE = [
    "Possible race condition around shared state; concurrent access is not synchronized and a global variable may be mutated without a lock, causing a permission or consistency issue.",
    "Missing None/null check: a value can be None and is used without validation, leading to NULL dereference or incorrect IN/comparison behavior.",
    "SQL injection risk: user input appears to reach a query without parameterization; use parameterized statements.",
    "Cross-site scripting (XSS): output is not escaped/sanitized before rendering; escape HTML entities.",
    "Authentication/authorization gap: an endpoint may not verify the user is authorized (IDOR); check ownership and is_superuser/admin flags.",
    "Token/session expiration not enforced: exp claim or session timeout may be missing or not validated.",
    "Off-by-one or boundary error in a limit/offset/pagination computation; verify limit handling.",
    "Resource/memory leak: a file handle, connection, or listener is not closed/removed (missing close/removeEventListener).",
    "Unhandled error path: exceptions are swallowed or not logged; add error handling and avoid bare except.",
    "Missing await on an async call; the coroutine result is not awaited, so the operation may not complete.",
    "Hardcoded secret or credential committed in configuration; move to environment variables.",
    "Path traversal risk: file paths built from user input without normalization (..) checks; use safe path join.",
    "Insecure deserialization: untrusted data passed to a loader (yaml.load/pickle); use safe_load.",
    "Weak hashing (MD5/SHA1) used where a strong hash or HMAC comparison (compare_digest) is required; timing attack possible.",
    "CSRF protection may be missing on state-changing endpoints.",
    "Input validation missing on request parameters; validate types and ranges.",
    "Sensitive data (passwords, tokens) may be logged; redact before logging.",
    "Improper certificate/TLS verification could be disabled (verify=False).",
    "Integer overflow or unit conversion error in an arithmetic computation (seconds vs milliseconds).",
    "Uncaught promise rejection / missing .catch on an async chain.",
]
record = {
    "reviewer_ai": "boilerplate-spam",
    "writer_ai": "n/a",
    "result": {"findings": [
        {"file": "general", "severity": "high", "issue": t, "suggested_fix": ""}
        for t in BOILERPLATE
    ]},
}

tot_d = tot_b = positive = keys = 0
for p in sorted(glob.glob(str(repo / "suites/*/bug_index*.json"))):
    if "_template" in p:
        continue
    r = scorer.score_record(record, scorer.load_bug_index(Path(p)))
    t = r["totals"]
    keys += 1
    tot_d += t["bugs_detected"]
    tot_b += t["bugs_total"]
    positive += t["raw_score"] > 0
    rel = p.split("suites/")[1]
    print(f"{rel:48s} {t['bugs_detected']}/{t['bugs_total']} detected, "
          f"{t['false_positive_count']} FPs, score {t['raw_score']}/{t['max_possible_score']} ({t['score_pct']}%)")

print(f"\nAGGREGATE: {tot_d}/{tot_b} detected ({tot_d / tot_b * 100:.0f}%), "
      f"positive raw score on {positive}/{keys} keys")
