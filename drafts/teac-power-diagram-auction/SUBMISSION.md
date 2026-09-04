# TEAC submission sheet

Portal: https://mc.manuscriptcentral.com/acmteac

The former Editorial Manager site now directs all new submissions here. Use Editorial Manager only for manuscripts already under review or revision there.

## Article details

Article type: Research Article

Title: The Power Diagram Auction: A Formally Verified VCG Mechanism for LLM Advertising

Abstract:

Large language model (LLM) chat assistants are becoming an advertising surface. The previous surface, keyword search, shipped with broken incentives, and an industry grew to monetize the breakage; the new surface is a chance to get the incentives provably right on day one. The conversation embeds as a point x in a continuous space of hundreds of dimensions, and each advertiser declares a center c (their customer). The conceptual distance between them measures how closely they match. A reach sigma (how widely they serve) and a bid b (what a conversion is worth) compare that distance against a willingness to pay. The slot beside the reply goes to the advertiser with the highest log(b) - ||x-c||^2 / sigma^2. The mechanism involves no model training or response modification. We prove in Lean 4, with zero sorry, that the rule's argmax allocation with Clarke payments forms a VCG mechanism. Truthful reporting is weakly dominant, the allocation maximizes welfare at every query point, and its territories form a power diagram with keyword auctions as the degenerate case. This mechanism allows an auction to sell regions of embedding space.

Keywords: VCG mechanism; computational advertising; power diagram; embedding space; formal verification; Lean 4

Suggested ACM classifications:

- Theory of computation > Algorithmic game theory and mechanism design
- Information systems > Computational advertising
- Software and its engineering > Formal methods

## Author

Given name: June

Family name: Kim

Email: june@june.kim

ORCID: 0009-0005-3153-9396

Institution: Independent Researcher

City: Vancouver

State/province: British Columbia

Country: Canada

Corresponding author: Yes

## Declarations

- Sole author; no coauthors.
- Original work; not under review elsewhere.
- Prior dissemination: preprint, Zenodo DOI 10.5281/zenodo.21723924.
- Conflicts of interest: none.
- Funding: self-funded independent research; no external funding.
- Human participants or personally identifiable data: none.
- Generative AI: disclosed in the manuscript. Claude Code was used to produce Lean proofs, figures, and prose; the author directed the research, reviewed every claim, and accepts responsibility for the work.
- Data availability: no empirical dataset underlies the principal claims. Proof and implementation artifacts are openly archived.

## Related artifacts

- Paper preprint: https://doi.org/10.5281/zenodo.21723924
- Lean formalization: https://doi.org/10.5281/zenodo.21214697
- Exchange implementation: https://doi.org/10.5281/zenodo.21365911
- Simulations: https://doi.org/10.5281/zenodo.21366035
- Interactive explorer: https://doi.org/10.5281/zenodo.21365798

## Files to upload

1. `power-diagram-auction-teac-submission.pdf` — manuscript
2. `power-diagram-auction-teac-source.zip` — LaTeX source and figures, if requested
3. `COVER_LETTER.md` — paste its text into the cover-letter field or export it if the portal requires a file

## Stop before submission

- Confirm the portal's selected article type and declarations match this sheet.
- Preview the portal-generated PDF and confirm all 15 pages are present and legible.
- Review any open-access fee notice. No payment is due at initial submission, but an APC or waiver decision may arise if the paper is accepted.
- Do not click the final Submit button until the complete generated proof has been reviewed.
