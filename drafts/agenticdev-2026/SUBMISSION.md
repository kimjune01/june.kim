# AgenticDev 2026 submission — state and remaining steps

**SUBMITTED 2026-07-10 as #14** (hotcrp: https://agenticdev2026.hotcrp.com/paper/14).
PDF replaceable until Jul 15 6AM UTC+2 (= Jul 14 9PM Pacific). Notification Aug 21; camera-ready Aug 28; workshop Oct 12, Munich.
On acceptance: email organizers about remote presentation before booking anything.
Anonymous mirrors live: comparator-DA10 (abductor), hymech-117E (hygraph-mechanism), wepro-3D87 (swebench-pro), weaudit-901E (swebench-pro-audit) — keep them alive through review (~6mo expiry set).

Venue: AgenticDev @ ASE 2026, Munich.
Submission site: https://agenticdev2026.hotcrp.com/paper/new (HotCRP, not OpenReview — HotCRP accounts activate instantly with gmail).

## What's here

- `main.tex` — anonymized 5-page short paper (`sigconf,review,anonymous`), compressed from
  `src/content/blog/2026-05-28-the-hypothesis-graph-semantic-memory-methodeutics.md`.
- `main.pdf` — 6 pages total: body + refs start ≤ p5, p6 references-only. Within 5pp + 2pp-refs limit.
- `hypothesis-graph-anatomy.pdf`, `verus-2219-lift-mechanism.pdf` — figures converted from site SVGs.
  Fig 2 label "abductor gate" → "comparator gate" (tool name is googleable to kimjune01/abductor).
- Rebuild: `tectonic main.tex`.

## Anonymization decisions (reverse for camera-ready)

- Tool renamed "the comparator tool" throughout; `abductor` name removed.
- All artifact links → `\anonurl{}` placeholder "[link anonymized for review]".
- Cut: acknowledgments (Laird), funding line, blog-provenance posts, companion-essay self-refs
  (*Verifiable Knowledge*, *What Cannot Be False Cannot Be True*), Zenodo DOIs.
- LLM disclosure kept, one sentence.

## Remaining human steps

1. **Anonymous artifact links** (~5 min/repo): log in with GitHub at https://anonymous.4open.science,
   paste each repo URL, and give the terms to scrub: `june`, `kim`, `kimjune01`, `june.kim`,
   `abductor` (in the non-tool repos). Repos: abductor, hygraph-mechanism, swebench-pro,
   swebench-pro-audit. Then replace the four `\anonurl{...}` markers in main.tex (tool, mechanism,
   benchrun, audit) with the generated links and rebuild (`tectonic main.tex`).
   Caveat: the tool README/paths mention "abductor" heavily — set that as a scrub term so the
   mirror doesn't undo the paper's rename.
2. **HotCRP account + registration by ~July 13**: https://agenticdev2026.hotcrp.com/paper/new,
   gmail is fine, activates instantly. Enter title + abstract (paste-ready below), tick short-paper
   track if asked. PDF re-uploadable until July 15 AoE.
3. Read the compression pass — check nothing load-bearing died (cut-list below).
4. If also submitting verifiable-knowledge as a 5pp vision paper, that's a separate port (not started).

## Paste-ready HotCRP fields

**Title**: The Hypothesis Graph: A Verifiable Semantic Memory for Coding Agents

**Abstract** (plain text):
The hypothesis graph is a data structure for coding agents that deepens their reasoning and makes them accountable. Implemented at the harness layer, its nodes are testable claims, its edges the refutations that name the next claim. It updates by inquiry, Peirce's typed loop of abduction, deduction, and induction. What is new is running that loop as mechanical harness operations around the one step no procedure reaches. That step, the abductive leap, stays in the model; the harness manufactures the surprise, fires the kill, and records the trail, instead of leaving the loop to a model's undifferentiated prose. We demonstrate the mechanism on one contamination-free bugfix. Six self-attested arms plateau at a narrow fix; an externally verified comparator, the one input a context-bound agent cannot author for itself, carries a weaker model (Sonnet 4.6) to the behavior of the merged human fix that the strongest released model (Fable 5) does not reach without it. This buys verifiable accountability and reasoning that persists past the context window, at no additional training cost, usable by any coding-agent harness that can run pinned trials and read their verdicts.

**Keywords**: hypothesis graph; agent memory; abductive inference; LLM agents; provenance; auditability; falsifiability; post-cutoff evaluation

## Cut-list (what the 5pp version dropped from the full paper)

Full sections dropped: Actionable epistemology, Semantic memory subsection detail, Discussion
(verifiable agents essays), Future work, Availability detail, both appendices, Tables 1–2 of
related work, in-flight inquiry trace, four-model verdict-source table (kept as prose), diagnosis
climb H0–H4 (kept as prose summary), Rust code listing.
