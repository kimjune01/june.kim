# Zenodo deposit — assurance-at-the-boundary

Paste-ready fields for https://zenodo.org/uploads/new. Mirrors the What Cannot Be False deposit (record 20754646): Publication / Preprint, creator with ORCID, abstract as description.

Status: DEPOSITED. DOI 10.5281/zenodo.21461148 (v3, PDF with subsections + disclosures; v2 21448999; v1 21448757 carried this draft file by mistake). Concept DOI 10.5281/zenodo.21448756.

v3 also corrected metadata that was wrong on v1 and v2: creator was "Kim, Jun" with no ORCID and no affiliation, now "Kim, June" with ORCID 0009-0005-3153-9396 and Independent Researcher; license was CC BY 4.0 while this file and the post both said CC BY-SA 4.0, now CC BY-SA 4.0.

Next: one more edit pass on the paper, then email AVERI authors (Brundage, plus whoever owns institutional design) pointing at the piece and Recommendation 5. After any post-edit, re-render the PDF and push a new Zenodo version so the archived copy matches the page.

## File

public/assets/assurance-at-the-boundary.pdf (arXiv-styled, rendered 2026-07-19, commit b8cb4763)

## Resource type

Publication / Preprint

## Title

Assurance at the Boundary: The Level Below AAL-1

## Publication date

2026-07-19

## Creator

Kim, June — ORCID 0009-0005-3153-9396 — Independent Researcher

## Description

Preprint. Frontier AI Auditing (Brundage et al., arXiv:2601.11699) proposes four AI Assurance Levels in which assurance deepens as auditors gain access to non-public information, at $300,000 to several million dollars annually by its authors' own estimates. That framework takes from financial auditing, engineering, and arms control their inspection rights and accreditation powers. Here we present the level below their first, adoptable immediately at the cost of an auditor's time: assurance attached to the artifact at the boundary, against a declared standard, under a named signature. The design is not novel. All but two of the problems their paper poses have solutions already running in one of those fields, yet none has been tried on AI. The stance we take is that entitlement to a claim comes from replay, so assurance can only attach where replay is possible, which is the boundary. The practice has already run from the public side. Audits of eight publicly accessible benchmarks surfaced severe defects, each with a re-runnable receipt, and no published audit shows internal access reaching anything boundary verification could not. What the receipts need now is a reader. AVERI could hold them today, without buying any access at all.

## Keywords

AI auditing, third-party audits, AI assurance levels, benchmark auditing, boundary verification, reproducibility, receipts, AI governance, evaluation integrity

## License

CC BY-SA 4.0

## Related identifiers

- isPublishedIn → https://june.kim/assurance-at-the-boundary

## After the DOI mints

Add the archive line under the title in the post (pattern from what-cannot-be-false-cannot-be-true):

*[Download PDF](/assets/assurance-at-the-boundary.pdf) · arxiv-shape preprint, rebuilt from this source. · Archived at [doi.org/10.5281/zenodo.NNNNNNNN](https://doi.org/10.5281/zenodo.NNNNNNNN) (CC BY-SA 4.0).*

Then commit and redeploy.
