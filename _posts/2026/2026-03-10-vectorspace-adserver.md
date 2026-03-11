---
layout: post
title: "Vectorspace Adserver"
tags: vector-space
---

The [Vector Space](/vector-space) series is the spec. The [source code](https://github.com/kimjune01/vectorspace-adserver) is the artifact — generated from those posts with a coding agent. This post covers the engineering decisions that didn't warrant their own post — the ones you'd only find by reading the code.

## Privacy by Architecture

The SDK extracts intent from the user's chat locally, embeds it, encrypts the embedding with the enclave's attested public key, and sends the ciphertext to the exchange. The exchange can't decrypt it — only the TEE can. The enclave decrypts, runs the auction with live budgets, returns `{winner_id, payment}`, then zeros the embedding ([`process.go`](https://github.com/kimjune01/vectorspace-enclave/blob/master/process.go)). The exchange logs the result as `"[tee-private]"` and never sees the query.

The ciphertext does pass through the exchange server on its way to the enclave. Nitro Enclaves have no IP networking — vsock is the only interface, so there's no direct path from the internet to the enclave. But the exchange can't decrypt the payload. The private key is generated inside the enclave and never leaves. Attestation binds the public key to the audited code: the SDK verifies the attestation document before encrypting, so the ciphertext can only be opened by the exact code that was audited.

What if a publisher's SDK sends the embedding unencrypted? The server rejects it. `POST /ad-request` returns `400 plaintext embeddings are not accepted` if the request contains a raw embedding vector instead of ciphertext. A badly implemented SDK gets a clear error, not a silent privacy leak. The exchange's guarantee is narrow but enforceable: if it reaches us, it must be encrypted.

The split matters: the SDK owns intent extraction (no chat text leaves the device), and the enclave owns the auction (no stale budgets, no cache invalidation with real money). The exchange pushes budget snapshots into the enclave, so it always has live state without the SDK needing to know about budgets at all. The exchange is just a pass-through for ciphertext it cannot read.

## Vendored Enclave with Drift Tests

The enclave can't import the main auction package. It runs in an isolated environment with its own build. So the auction math in `enclave/auction/` is a vendored copy of `auction/`. Same functions, same signatures, separate package.

This creates a drift risk. If someone updates the main auction logic and forgets the enclave copy, the two diverge silently. `auction_crosscheck_test.go` prevents this: it runs identical inputs through both packages and asserts bit-identical results.

Attestation works by hashing the enclave binary and comparing it to the attestation document. If the enclave source is buried in a larger repo, an auditor has to clone the whole thing and trust that the build context doesn't pull in code from outside `enclave/`. So the enclave lives in its own [standalone repo](https://github.com/kimjune01/vectorspace-enclave). Clone, `go build`, hash, compare. The package imports only Go stdlib (`math`, `crypto/*`, `encoding/*`, `sync`), so there's nothing to trust beyond the standard library.

See [Attested Attribution](/attested-attribution) for the attestation chain that makes TEE proofs useful to advertisers.

## Pay Per Click, Once

The auction computes VCG payment at auction time and stores it in `auctions.payment`. But the advertiser isn't charged then. Charge fires on first click only.

`handler/events.go` handles it: `HasClickEvent(auctionID)` checks whether this auction already recorded a click. If not, the handler pulls the stored payment and calls `h.Budgets.Charge(req.AdvertiserID, payment)`. If the user clicks the same ad twice, the second click is a no-op. One charge per auction.

The auction determines the price; the click triggers the charge. The advertiser's budget decrements by exactly the VCG payment, exactly once.

See [One-Shot Bidding](/one-shot-bidding) for why VCG pricing makes this clean: the advertiser's payment doesn't depend on their own bid.

## Creatives Decoupled from Position

Position and creative are separate concepts. Position is the advertiser's semantic location: intent embedding + σ (spread) + bid price. Creative is what the user sees: title + subtitle. An advertiser has one position but multiple creatives.

This separation enables A/B testing without moving your position. An advertiser can test "Licensed therapist specializing in anxiety" vs. "CBT-trained counselor for stress management" while their auction position stays fixed. Position changes cost a [relocation fee](/three-levers). Creative changes are free.

## Intent Extraction Prompt

The prompt that converts user chat into an advertiser-compatible semantic frame lives in `sdk-web/src/intent.ts`:

> Given a conversation, decide whether the person could benefit from a professional service. If yes, write a single sentence describing that service — as if the provider were writing their own position statement.

The key phrase is "as if the provider were writing their own position statement." This maps the user's need into the same semantic space as advertiser positioning. A user saying "my back has been killing me after sitting all day" becomes something like "Licensed physical therapist specializing in posture-related back pain." That sentence gets embedded and compared against advertiser positions using cosine similarity.

The prompt also has guardrails: it extracts no demographics or personal data, responds `"NONE"` for casual conversation, and matches the most obvious professional need. A health complaint maps to a health provider, not a lawyer.

See [Buying Space, Not Keywords](/buying-space-not-keywords) for why semantic matching replaces keyword targeting.

## SQLite as the Billing Ledger

VCG payment is computed at auction time but charged at click time. That temporal gap means the exchange needs a persistent record of what it owes whom. Without it, a click arrives and there's no way to know the price.

The `auctions` table is that record. Every auction logs the winner, the VCG payment, and the bid count. When a click comes in, the handler looks up the stored payment and charges the advertiser's budget. The `events` table deduplicates: one charge per auction, no matter how many times the user clicks. This isn't an audit trail bolted on for compliance — it's the billing system itself.

Both sides can pull their own records. Advertisers get `GET /portal/auctions` — every auction they won, what they paid, how many bidders competed, with CSV export. Publishers get `GET /portal/publisher/auctions` — every auction that ran on their inventory. Neither side has to trust the exchange's summary. Google's Performance Max gives [impression counts per placement with no clicks, cost, or conversions attached](https://www.searchenginejournal.com/google-ads-surfaces-pmax-search-partner-domains-in-placement-report/567922/). Here, every auction is individually queryable with the exact VCG payment.

`position_history` serves a similar role for [relocation fees](/three-levers). Every position move logs the distance and the fee. If an advertiser disputes a charge, the exact numbers are right there.

See [Receipts, Please](/receipts-please) for why this matters.

## Content-Addressed Positions

The SDK caches advertiser embeddings locally and needs to know when they change. The server computes a SHA-256 hash of all positions and returns it as an `ETag`. The SDK sends `If-None-Match` on subsequent requests and gets `304 Not Modified` if nothing changed. Any position mutation invalidates the hash. The SDK polls with negligible cost.

## Everything Else

Decisions that don't need their own section but would feel wrong if missing:

- **Pulumi in Go** for infrastructure. EC2 + Docker Compose + EBS for SQLite persistence + S3/CloudFront for the landing page + Route 53 + ACM cert. One command to stand up the whole stack.
- **Embedding service** as a separate container wrapping BGE-small-en-v1.5, or Hugging Face Inference API if you set `HF_TOKEN`. Swap the model without touching the auction server.
- **Multi-stage Docker builds**. Go server and Node portal compile in build stages, ship on Alpine. Sidecar pre-downloads the model at build time so cold starts don't hit a model registry.
- **Makefile** with `make dev`, `make test`, `make deploy`. Clone, one command, auctions running.
- **Frozen lockfiles** everywhere. `go.sum`, `pnpm-lock.yaml`, `uv.lock`. Builds are reproducible or they don't ship.
- **Caddy** for TLS termination and reverse proxy. Auto-renews certificates. Zero config beyond a Caddyfile.
- **Frequency capping**. 3 impressions per advertiser per user per 60-minute window. SDK gets 429 when capped.

---

*The blog series is the spec. The repo was built from it with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code).*

*Part of the [Vector Space](/vector-space) series.*
