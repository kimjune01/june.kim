---
variant: post-medium
title: "Contract by label"
tags: coding, methodology
---

Nobody picks MIT vs GPL by reading the legal mechanism. They pick by what they're licensed to do — use commercially, fork freely, keep derivatives proprietary. The mechanism (copyleft enforcement, patent grants, redistribution conditions) is the receipt; the license name is the product.

We got this right for distributing code. We got it wrong for annotating it.

## Receipts named where licenses should be

A type-checker accepts `const` on a C++ method. The annotation tells the *next* prover the method won't mutate `this`. It tells the *caller* almost nothing. Can I share the object across threads? Can I cache the return value? Can I call it on a temporary? Each is a separate license. `const` is the proof technique; the licenses are downstream.

Same with database isolation. [`SERIALIZABLE`, `REPEATABLE_READ`, `READ_COMMITTED`](https://en.wikipedia.org/wiki/Isolation_(database_systems)). Every developer guesses wrong because the names tell you what the *prover* did, not what *you* are licensed to assume. If they were named `phantom-safe`, `compose-with-parallel-writers`, `snapshot-stable`, callers would pick correctly the first time.

Same with `volatile`, Java's `synchronized`, Rust's `unsafe`. Receipts dressed as interfaces.

## The proof artifact is a cache

The notarization (proof, audit report, type-checker output, cert record) is a **cache**; the license label is the **key**; the proof contents are the **value** the consumer never reads.

That's why labels exist: **verify-every-time is too expensive**. Past trivial cost, you can't re-prove a property at every callsite. You prove once, label the result, and let consumers query by label forever. The label is the amortization protocol.

This works at every scale.

| scale | label | proof artifact | who computes once |
|---|---|---|---|
| repo | `license: MIT` | LICENSE text + legal mechanism | maintainer |
| service | [`SOC 2 Type II`](https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2) | full audit report | auditor |
| module | `Apache-2.0` | NOTICE + patent grants | committer |
| function | `const`, `volatile` | type-checker proof obligation | compiler |
| node | `safe-to-retry`, `loop-safe` | runtime cert + statistical credence | the verification ladder |
| call | [HTTP idempotent semantics](https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods) | RFC + caller convention | spec author |

Same shape every time: prove once, query forever.

## The failure mode is scale-invariant too

Labels are cheap on the happy path, catastrophic when the cache lies. Someone edits the LICENSE file and downstreams keep the cached badge. A SOC 2 attestation expires and nobody rotates the audit. A `@thread_safe` function quietly calls into a non-thread-safe dependency after a refactor. A cert ladder trusts a node after an engine upgrade silently changed its postcondition.

Same failure shape: stale label, world drifted, nobody re-checked.

This is why the boring engineering (drift detection, TTLs, re-validation policy, background sampling) is the load-bearing engineering. Without invalidation, the label lies the moment the world moves. Cache miss becomes a first-class third state: "we haven't proven you can," distinct from "you can't." Most systems collapse this into default-deny or default-allow, losing the signal that tells them what to verify next.

## Two rules

1. **Name labels by what the consumer is licensed to do, not by what the prover did.** The math is the receipt; the license is the product.
2. **Treat the labeled artifact as a cache.** Plan for invalidation before you publish.

When you find yourself naming things by the proof technique, you've exposed cache values where the keys should be. The consumer is reading your receipts to figure out what they bought.
