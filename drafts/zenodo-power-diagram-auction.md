# Zenodo deposit — power-diagram-auction

Paste-ready fields for https://zenodo.org/uploads/new. Mirrors the assurance-at-the-boundary deposit (record 21461148): Publication / Preprint, creator with ORCID, abstract as description.

Status: DEPOSITED 2026-07-31. DOI 10.5281/zenodo.21723924 (v1). Concept DOI 10.5281/zenodo.21723923. The four artifacts already had DOIs (Lean proof 21214697, adserver 21365911, simulator 21366035, demo 21365798); this deposit makes the paper their parent node via isSupplementedBy.

arXiv submit/7827411 has been on hold since 2026-07-15; MOD-97590 confirmed on 2026-07-27 that no deadline can be given. This deposit does not affect that submission. If it clears, the arXiv version can cite this DOI as the prior deposit.

Metadata was correct on v1: creator "Kim, June" with ORCID and Independent Researcher, license CC BY-SA 4.0. Both are the fields that were wrong on the first two versions of the assurance-at-the-boundary record; the Zenodo form defaults the license to CC BY, so it has to be changed by hand every time.

## PDF re-render (done before upload)

`public/assets/power-diagram-auction.pdf` had been rendered 2026-07-14 (commit 95fa9da1) while the source was edited 2026-07-15 (commit a347f88c, "correct OT budget claim; restructure Discussion as causal chain"), so the PDF on disk predated a corrected claim. Re-rendered with `md2arxiv/bin/build-pdf.sh` before depositing: 13 pages, compile gate and arXiv checks pass, md5 43b06f4ea4d036cd579749671b75e681.

## File

public/assets/power-diagram-auction.pdf (arXiv-styled, re-rendered from `src/content/blog/2026-07-06-power-diagram-auction.md`)

## Resource type

Publication / Preprint

## Title

The Power Diagram Auction: A Formally Verified VCG Mechanism for LLM Advertising

## Publication date

2026-07-06

## Creator

Kim, June — ORCID 0009-0005-3153-9396 — Independent Researcher

## Description

Preprint. Large language model chat assistants are becoming an advertising surface. The previous surface, keyword search, shipped with broken incentives, and an industry grew to monetize the breakage; the new surface is a chance to get the incentives provably right on day one. The conversation embeds as a point x in a continuous space of hundreds of dimensions, and each advertiser declares a center c (their customer). The conceptual distance between them measures how closely they match. A reach sigma (how widely they serve) and a bid b (what a conversion is worth) compare that distance against a willingness to pay. The slot beside the reply goes to the advertiser with the highest log(b) - ||x-c||^2 / sigma^2. The mechanism involves no model training or response modification. We prove in Lean 4, with zero sorry, that the rule's argmax allocation with Clarke payments forms a VCG mechanism. Truthful reporting is weakly dominant, the allocation maximizes welfare at every query point, and its territories form a power diagram with keyword auctions as the degenerate case. This mechanism allows an auction to sell regions of embedding space.

## Keywords

VCG mechanism, ad auctions, LLM advertising, power diagram, embedding space, Lean 4, formal verification, mechanism design, truthful bidding, Clarke pivot

## License

CC BY-SA 4.0

## Related identifiers

- isPublishedIn → https://june.kim/power-diagram-auction
- isSupplementedBy → 10.5281/zenodo.21214697 (auction-proof, the Lean formalization)
- isSupplementedBy → 10.5281/zenodo.21365911 (vectorspace-adserver, the exchange)
- isSupplementedBy → 10.5281/zenodo.21366035 (openauction/cmd/simulate, the simulations)
- isSupplementedBy → 10.5281/zenodo.21365798 (vectorspace-ads, the interactive explorer)

## After the DOI mints

DONE: the byline in `src/content/blog/2026-07-06-power-diagram-auction.md` now carries the standard archive line pointing at 10.5281/zenodo.21723924. Not yet committed or deployed.
