# Bootstrap render prompt: Agent-Native Epistemics

A self-contained prompt to render the paper from its argument graph, by composing
the already-warranted rhetoric of the prior blog posts. Hand this to a renderer
(a fresh agent, Fable, or the main loop). It boots the render from the graph and
nothing else needs to be explained. (Refreshed 2026-06-12 for the F7a/F7b split,
the honest-limits triad, the narrowed C5, and the codex hardening.)

**On-theme, by construction.** The paper argues truth is built by composing prior
builds. This render IS that: the blog posts are the paper's provenance edges, and
rendering reuses their warranted prose rather than re-deriving it. Do not write
from scratch what a prior post already says well. Compose, cite the edge, move on.

---

## Inputs (read in this order)

1. `drafts/what-cannot-be-false-cannot-be-true-argument-graph.md` — THE SOURCE OF TRUTH. Read
   `## CURRENT STATE`, then the act-structured nodes (ACT I / ACT II / CODA /
   REFERENCE), then `## Section render order` (the AUTHORITATIVE section sequence +
   per-section node manifest + render notes), then `## Citation map (pre-render)`
   (what each node may cite, with `own` = no external cite).
2. `src/content/blog/2026-06-12-what-cannot-be-false-cannot-be-true.md` — the paper view. The
   abstract, intro, and §phenomenon are WRITTEN (but the abstract and intro are
   STALE, see Procedure); everything from §belief is to render. Match its frontmatter
   (`variant: post-paper`, `autonumber: true`) and the §(id) cross-reference tokens.
3. The prior posts to MINE for rhetoric (the provenance edges), read for voice and
   for lines to reuse: `/truth-is-buildable`, `/belief-is-the-edge-of-knowing`,
   `/truly-untrue`, `/science-on-trial`, `/sour-red-tapes`, `/modes-of-reason`,
   `/auditing-deepswe`, `/complementations`. Files in `src/content/blog/`.
4. `src/content/blog/2026-05-28-the-hypothesis-graph-semantic-memory-methodeutics.md`
   — the sibling paper, for the post-paper register (section depth, citation style,
   how the author runs a formal argument without going stiff).

## Voice and rhetoric (reuse, do not reinvent)

The register is the author's: aphoristic, declarative, short sentences that land, a
formal spine carried in plain words. The prior posts already contain the best
phrasings of half these ideas. Reuse them, lightly adapted. Signature moves to lift:

- "What cannot be false cannot be true." / "a tautology wearing a decimal point." /
  "the edges are what you grip." / "untrue, but in motion." (truth-is-buildable)
- "There is no tier above belief." / "I know my keys are in my pocket." / belief as a
  bet, the odds. (belief-is-the-edge-of-knowing)
- "not even wrong" as the floor below false; Pauli's phrase, Woit's title. (C3, F7b)
- the N-atoms example (world-claim out of reach, knowledge-claim refuted at
  provenance). (truth-is-buildable, A7)
- "every claim stands trial forever." (science-on-trial, C1f)
- "delete my submission and every receipt still stands." / *nullius in verba*.
  (sour-red-tapes, C1e)
- the dangling pointer (`has_model_patch: true` aimed at a patch that is not there)
  = the detached credential. (truth-is-buildable, C1e)

When a prior post carries a passage in full, prefer POINTER-FIRST: state the move in
one line and link the post. The paper is the consolidation, not a longer retelling.

## Hard rules (non-negotiable)

1. **No em-dashes.** Periods, commas, restructure. (Detect: grep `—`.)
2. **Citations only from the citation map.** Load-bearing claims cite the canonical
   short-key's full ref. Nodes marked **own** take NO external cite. NEVER invent a
   citation, year, or work. Companion blog posts are self-links, never a warrant.
3. **The C5 delta razor, NARROWED, governs every giant.** The line is NOT "nobody
   made it run" (many ran parts: NARS, proof assistants, nanopubs, reproducible
   science). It is: everyone supplied PIECES, nobody made THIS EXACT CONTRACT run,
   the specific executable semantic contract for agent knowledge (replayable build +
   provenance edge + kill condition + stranger-replay + warrant ledger + canon
   admission, as one). Weight the novelty on ACT II (C1a-i + C2/C3); render ACT I as
   visibly PREPARATORY, mostly inherited. Every borrowed idea ships its "described vs
   made-to-run" framing, so the giants read as scaffolding.
4. **Render ACT II honest about its limits.** The honest-limits triad (C1g trusted
   roots, C1h adversarial robustness, C1i bounded verification) must render, so
   C1e/C1f do not read as utopian. Replay bottoms out in declared terminal witnesses
   (C1g), not view-from-nowhere; "always CAN verify" is the option, not the labor
   (C1i).
5. **Honor every per-node render note** (read them in the graph). The load-bearing ones:
   - **F4**: a wrong build is a PHENOMENAL event constrained by reality, NOT a signal
     from the thing-in-itself; concede the reddening is Peirce's Secondness.
   - **A5**: scope "what cannot be false cannot be true" to EMPIRICAL world-claims at
     first utterance, forward-pointing to F7 for the formal exception.
   - **F6** headline scoped to EMPIRICAL truth; **F6** climb rung is "standing result,"
     never "theorem" (firewall purity). **F6c** Gödel is owned by F7, do not double it.
   - **F7**: "decisive within a stipulated formal system where proof is available,"
     never bare "absolute," "credence 1," or "complete tester." Ontology disclaimed:
     "platonic" names behavior, truth is relative-to-axioms, no Platonism commitment.
   - **F7a**: the crossing rule (consistency cannot substitute for reality, Einstein).
   - **C1**: classical JTB "does not specify an executable inspection/replay protocol,"
     not "cannot be run."
   - **C1a**: "independent constraint improves warrant," not "objective purchase."
   - **C1b**: cite Davidson and Nagel NARROW; the "independent projections constrain
     the object" step is the paper's OWN (robustness). The blind-men/elephant parable
     ILLUSTRATES; the machinery carries the argument (author: the audience is
     sophisticated, the parable just keeps it from going dry).
   - **C1e**: credence is a SHORTCUT over a verifiable substrate, NOT "no gatekeeping."
     Credentials are attested build certifications (cached pointers to replayable
     builds); deferring to them is fine and rational (the SourceForge download button);
     the pathology is the DETACHED credential (the dangling pointer). The protocol
     anchors credentials, does not ban them.
   - **C1d**: canon = STANDING BUILDS, not settled truths (provisional membership).
6. **F7b renders as a WORKED PASSAGE, not a bullet list.** String theory is the one
   example that exercises the whole apparatus, walked one move at a time: empirically
   untrue (the ledger) → untrue-and-stalled not in-motion (C2a) → if unfalsifiable,
   detached / not-even-wrong (E1 + A5 + C3) → the whole debate reduces to one question,
   is there a kill edge → the A5 double duty (witness for A5, AND the proof A5 needs
   F7's phenomenal/noumenal scoping to be more than verificationist overreach; Popper
   stops at "unscientific," the firewall rescues "cannot be true" from anti-realism).
   CHARITABLE (the error is epistemic, not intellectual; intelligence is not the
   bottleneck, the kill edge is) and DATED ("from how we see it today," a reddenable
   standing build). Do NOT call string theory "detached from physics" (it is an
   empirical hypothesis); say detached from TESTING. Keep the "fun math exercise /
   tragedy" framing OUT (author's margin comment, not for the paper).
7. **Act structure visible; standard-grounded only.** Acts cross-reference. The
   Natural Framework, the six roles, and the Perceive-morphism stay OUT; "lossy
   projection" (C1b) is the generic measurement sense.

## Procedure

Render section by section, IN the graph's `## Section render order` (authoritative),
body first, abstract and intro LAST (they are stale: they predate the asymptote, the
two graphs, and all of Act II, and the abstract's "bivalence preserved in the
noumenon" clause must become the F7 housing). For each section: pull its node
manifest, draft in the author's voice reusing prior-post rhetoric, cite per the map,
honor the render notes, keep `§(id)` tokens. Checkpoint after each ACT, not each
section: stop, report, let the author steer voice before continuing.

Act summary (the graph carries the exact per-section manifest and numbering):
- **ACT I — the frame**: §phenomenon (add F6 seed) · §belief · §knowledge · §truth ·
  §the-asymptote · §the-two-graphs (F6c, F7, F7a, **F7b worked passage**; Act I curtain).
- **ACT II — the mechanism**: §truth-at-the-edge (opens with C1) · §the-warrant-ledger ·
  §triangulation (prose order C1b → C1a → C1c) · §protocol-and-canon (C1d, C1e, C1f) ·
  §the-honest-limits (C1g, C1h, C1i).
- **CODA**: §related-work (full C5 razor + R11 at strength) · §self-application-and-
  falsifiers (S1-S4, S5 one light optional sentence, K1-K10) · §future-work, the
  honestly-typed open frontier (FW1 the outward edge to application; FW2 the
  open-conjecture license that rehomes the scope-guarded vision; FW3 the economic /
  search-complexity edge, verify<generate 1:1, agent fleets turn many:1 into
  many:many, the filtering rule is the load-bearing variable; FW4 the forecast,
  under unbounded generation untrue is the only surviving classification because
  true/false cost the rate-limited inhale and untrue is free, grounded in
  /compress-and-unfold on standard DPI/Shannon/cata-anamorphism, NF out). Each FW
  node renders as an OPEN edge that names its own kill condition, never asserted.
  · §conclusion. Then RE-RENDER §abstract and §introduction to match the body.

## Done when

Every section from §belief through §conclusion is rendered, the abstract and intro
re-rendered to match, no em-dashes, every load-bearing claim carries a real citation
from the map (and every `own` node carries none invented), every borrowed giant
carries its made-to-run framing, Act II renders its honest limits, F7b reads as a
worked passage, and the paper reads as one argument in two acts that practices the
epistemology it states.
