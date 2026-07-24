# Boundary assurance — response to AVERI's Frontier AI Auditing

Status: skeleton, 2026-07-19. Goal: DOI'd document on the record responding to arXiv:2601.11699.

## Target

Brundage et al., "Frontier AI Auditing: Toward Rigorous Third-Party Assessment of Safety and Security Practices at Leading AI Companies," arXiv:2601.11699, Jan 2026. ~28 authors (AVERI, GovAI, Oxford Martin, MIT CSAIL, Stanford). Launch paper of AVERI (AI Verification and Evaluation Research Institute).

Their framework: AI Assurance Levels. AAL-1 = auditors rely on company-provided information. AAL-2 = deeper access to non-public information, less dependence on company statements. AAL-3/4 = rule out materially significant deception; admitted "not yet technically and organizationally feasible."

The ladder's axis is access depth. That axis is the thing this response disputes.

They do NOT specify liability mechanisms or reputation-based accountability (confirmed against the paper page 2026-07-19). The stakes section here fills a gap they name, not text they defend.

## Thesis

Assurance scales with boundary integrity and stakes, not access depth.

One invariant recursing across layers: preserve provenance at the boundary. Every layer has the same failure mode (provenance dropped at the crossing, so the claim on the far side can't be checked against the near side) and the same fix.

- Benchmark → eval: preserve what the instrument measured and under what conditions.
- Eval → dev: preserve what was run and on what artifact.
- Dev → deployment: preserve what shipped.
- Audit → public: preserve the record and the decisions.

Anti-truism guard: at each layer, name the specific artifact currently dropped, a documented failure it caused, and the enforcement move. Receipts exist for the bottom two layers; upper layers are argued, and the paper says so.

## Structure decision (from the source conversation)

- Not commentary. An alternative architecture that happens to disagree; Brundage becomes the foil in section two, not the organizing principle.
- The falsifiable-claims corpus measurement is a SEPARATE paper (empirical companion). Don't merge.
- State the invariant once, then show it holding at each layer with the same enforcement move.

## Empirical spine

Seven audits, all conducted at zero access, all finding real defects before any model ran: [/how-to-audit-a-benchmark](https://june.kim/how-to-audit-a-benchmark) (the seven-clause table). This is the only part of the argument that isn't assertion; lead with it.

The ablation receipt: [/an-epistemic-ablation](https://june.kim/an-epistemic-ablation). OpenAI audited SWE-bench Pro with maximum access and produced an unreconstructible ~30%; the zero-access audit produced a re-runnable 15.0% floor. The party with the most access produced the least checkable audit. This is the thesis in one anecdote-with-receipts: access depth did not buy checkability; boundary records did.

Access disposal (from the conversation, keep this framing): access asks to see the interior because provenance wasn't preserved at the boundary. Preserve it and the interior stops mattering — everything that crosses is already on the record. Internal-only deployment is not a counterexample but the case where the boundary wasn't drawn: a completeness problem, not an access problem.

## Stakes section

Reputational stakes first, liability later — a claim about sequence, not a hedge. The mechanism has to be adoptable before it's enforceable; reputation is the only stake available without legislation, a forum, or permission. PE licensure precedent: voluntary professional association first, statutory seal decades after. Named stamps make stakes attach to persons.

Costs to state plainly (not hide): reputation erodes rather than revokes (needs a reading community — the recognition function); asymmetric against first movers; capturable by the industry that sets it. Liability at least routes through an outside party.

## Named gaps (state them ourselves)

- Manifest completeness is a promissory note: undisclosed training runs and internal-only deployment are where no boundary was drawn. Boundary enforcement can't reach what never crosses one.
- Upper-layer claims (dev → deployment) have no receipts yet; the bottom-layer receipts are the existence proof that boundary-side auditing finds real defects.

## Venue for the DOI

DECIDED (2026-07-19): Zenodo. arXiv queue is months long; the point is to be on the record now. Zenodo assigns the DOI instantly, supports versioned DOIs (v2 can follow without losing the citation), takes the md2arxiv PDF as-is, CC BY-SA 4.0 per standing practice. Upload type: publication / preprint.

Site rendering: variant post-paper, autonumber: true.

## Open decisions

- Title. Working: "Assurance at the Boundary". Needs the counterclaim audible in the title.
- Whether the stamps/recognition mechanism (named signatures, AVERI-as-reader) gets its own section or folds into stakes.
- Which upper-layer dropped-artifact examples are citable vs asserted.
