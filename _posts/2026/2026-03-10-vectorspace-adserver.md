---
layout: post
title: "Vectorspace Adserver"
tags: vector-space
---

The [Vector Space](/vector-space) series is the spec. The [source code](https://github.com/kimjune01/vectorspace-adserver) is the artifact, [live at vectorspace.exchange](https://vectorspace.exchange/) — generated from those posts with a coding agent. This post covers the engineering decisions that didn't warrant their own post — the ones you'd only find by reading the code.

Decisions that didn't warrant their own post but would feel wrong if missing:

- **Vendored enclave**. Auction math is vendored into a [standalone repo](https://github.com/kimjune01/vectorspace-enclave) so auditors can clone, build, and hash without ambiguity. `auction_crosscheck_test.go` asserts bit-identical results between copies. Auction mechanism from [CloudX OpenAuction](https://github.com/cloudx-io/openauction). See [Attested Attribution](/attested-attribution).
- **[Intent extraction prompt](/intent-extraction)**. "Write as if the provider were writing their own position statement." Maps user chat into the same semantic frame as advertiser positioning. Runs on the publisher's LLM, not the exchange's.
- **[Publisher skills](https://github.com/kimjune01/vectorspace-skills)** instead of an SDK. Four prompt documents a coding agent reads to evaluate, install, verify, and uninstall the integration. No package dependency. The agent writes code directly into the publisher's files and opens a PR.
- **Ciphertext pass-through**. The SDK encrypts the embedding with the enclave's attested public key. The server passes ciphertext it can't read to the TEE via vsock. Plaintext embeddings get rejected with `400`. The exchange never sees the query. See [process.go](https://github.com/kimjune01/vectorspace-enclave/blob/master/process.go).
- **CPC billing**. VCG payment computed at auction time, charged on first click. `events` table deduplicates — one charge per auction, no matter how many clicks. See [One-Shot Bidding](/one-shot-bidding).
- **Per-auction receipts**. Both sides pull their own records: `GET /portal/auctions` for advertisers, `GET /portal/publisher/auctions` for publishers. Every auction individually queryable with exact VCG payment. See [Receipts, Please](/receipts-please).
- **Creatives decoupled from position**. Position (embedding + σ + bid) is the auction identity. Creative (title + subtitle) is what the user sees. A/B test creatives without moving your position. Position changes cost a [relocation fee](/three-levers); creative changes are free.
- **Content-addressed positions**. SHA-256 hash of all positions returned as `ETag`. SDK sends `If-None-Match`, gets `304` if nothing changed. Negligible polling cost.
- **Pulumi in Go** for infrastructure. EC2 + Docker Compose + EBS for SQLite persistence + S3/CloudFront for the landing page + Route 53 + ACM cert. One command to stand up the whole stack.
- **Embedding service** as a separate container wrapping BGE-small-en-v1.5, or Hugging Face Inference API if you set `HF_TOKEN`. Swap the model without touching the auction server.
- **Multi-stage Docker builds**. Go server and Node portal compile in build stages, ship on Alpine. Embedding service pre-downloads the model at build time so cold starts don't hit a model registry.
- **Makefile** with `make dev`, `make test`, `make deploy`. Clone, one command, auctions running.
- **Frozen lockfiles** everywhere. `go.sum`, `pnpm-lock.yaml`, `uv.lock`. Builds are reproducible or they don't ship.
- **Caddy** for TLS termination and reverse proxy. Auto-renews certificates. Zero config beyond a Caddyfile.
- **Frequency capping**. 3 impressions per advertiser per user per 60-minute window. SDK gets 429 when capped.

---

*The blog series is the spec. The repo was built from it with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code).*

*Part of the [Vector Space](/vector-space) series.*
