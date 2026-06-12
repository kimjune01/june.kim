# Argument graph: Agent-Native Epistemics, An Epistemology a Machine Can Run

The paper (`src/content/blog/2026-06-12-agent-native-epistemics.md`, slug
`/agent-native-epistemics`) is a **view onto this graph**. Edit here first, then
propagate to the view. Each node carries its claim, its warrant, its status, and
the section that renders it. Statuses: `definition`, `grounded` (canonical source
carries it), `argued` (the paper's own argument), `declared` (norm or stance),
`positioned` (prior-art placement), `pending`.

## CURRENT STATE (2026-06-12)

- **Thesis (one line):** classical epistemology (JTB, correspondence, certainty) was built for a human knower and cannot be *run*; this paper assembles one a machine can run, out of old parts in pragmatist order, read as a build.
- **Home tradition = PRAGMATISM** (James, Dewey, Peirce, Ramsey). The contribution is the pragmatist program carried to a knower it never had in view, and thereby made to execute. Kant, Popper, the intuitionists, Brandom are RECRUITED around that spine, not co-equal.
- **Standard-grounded ONLY.** Every load-bearing claim rests on canonical sources. The Natural Framework and its six-role / Perceive-morphism apparatus are KEPT OUT (would couple a narrow defensible claim to a wide contested one). If the data-processing inequality is needed, cite Cover & Thomas, never the framework. Companion blog posts are self-links (blog register), never load-bearing citations (P group; tiering rule).
- **Three contributions, each scoped NARROW:** C1 operationalization (belief/knowledge/truth reduce to buildable/checkable/replayable structures), C2 warrant ledger (true/false/untrue as bookkeeping of warrant, NOT a new logic; bivalence is housed in the platonic graph, not denied, F7), C3 dignity ordering (among claims *presenting as knowledge*, accountable falsehood outranks unaccountable pseudo-knowledge; the qualifier is load-bearing). The delta is C5's EXACT CONTRACT (everyone supplied pieces; nobody made this exact contract run), weighted on Act II and bounded by the honest-limits triad (C1g-i: trusted roots, adversarial robustness, bounded verification).
- **Spine = the F group:** Kant's phenomenon/noumenon boundary front-loaded; one departure from Kant: the noumenon is not inert, it reddens a wrong build; that one bit of contact is the leash. Everything after stays on the near side.
- **Central claim, the asymptote (F6/F6a/F6b):** EMPIRICAL truth is a graded belief ASYMPTOTIC to the noumenon, approached never occupied. Two derivations of one limit: Peirce convergence (diachronic, the community of inquiry) and the graded-belief ceiling (synchronic, credence in [0,1), no tier above belief). A-fortiori case = physics, still asymptotic. Resolves the F4/C2 true/false asymmetry (reddening-only is the gradient of the approach, not a defect). Pragmatist core, standard-grounded (Peirce, Ramsey).
- **The two-graph architecture (F7/F7a):** empirical and platonic truths live in DISJOINT hypothesis graphs. Empirical = graded/asymptotic; platonic = absolute truth-without-grade (proof decides, no external noumenon). FIREWALL: the platonic graph's absolute truth never touches the empirical (Einstein 1921, *Geometry and Experience*). Resolves the bivalence triangle (retires K5). Crossing rule: a mathematical model of the world is an empirical hypothesis awaiting a world-kill, consistency cannot substitute for reality (string-theory witness, F7a). Maps onto the paper's own data structure.
- **STRUCTURE (decided 2026-06-12): ONE PAPER, TWO ACTS.** ACT I = the frame, what truth IS for a machine (phenomenon/noumenon, belief→knowledge→truth, the asymptote, the two graphs; mostly INHERITED, the C5 razor admits it). ACT II = the mechanism, how a population of agents coordinates and builds a verifiable canon on it (operationalization C1, triangulation/protocol/canon C1a-f, the honest-limits triad C1g-i; this is where the DELTA lives, C5's exact-contract claim). The acts cross-reference; Act I sets up Act II's payoff. Splitting weakens both (Act I is derivative alone, Act II is rootless alone).
- **Render order (PENDING Fable re-review 2026-06-12 to set the act boundary + sequence; superseding the 13-section list below):** Act I → Act II → Related work → Self-application/falsifiers → Conclusion. The F6/F7 asymptote+two-graph cluster gets its own section closing Act I; the C1a-f social cluster is Act II's core. (See `## Section render order`, now stale.)
- **Written so far in the view:** abstract, intro, §phenomenon. Everything from §belief on is `pending` render.
- **Source docs:** /truth-is-buildable (06-04), /belief-is-the-edge-of-knowing (04-26), /truly-untrue (06-06), /science-on-trial (04-19); sibling graph `drafts/hygraph-smem-argument-graph.md` (A8 prior-art block recruited into R).

---

# ACT I. The Frame: what truth is for a machine

## F (part 1): Phenomenon and noumenon · §phenomenon

- **F1.** Kant's boundary, front-loaded: noumenon = the world in itself, thinkable
  never holdable; phenomenon = the appearance a build constitutes; every cognizer,
  human or machine, works the phenomenon. `grounded` (Kant, SEP transcendental
  idealism) · §phenomenon
- **F2.** Noumenal truth = correspondence to the world in itself: if MODELED as
  correspondence truth it is classically bivalent (excluded middle holds in the
  model), and inaccessible in the same breath; the bivalence belongs to the
  model, not to a standard anyone can consult.
  Useless as a working standard because every test returns a phenomenon.
  `grounded + argued` · §phenomenon
- **F3.** Phenomenal truth = a build exposed to a test and presently standing.
  The side a knower works; naming it phenomenal licenses the word *truth* for
  something less than correspondence-forever without demoting it to belief.
  `definition` · §phenomenon
- **F4.** THE ONE DEPARTURE FROM KANT: the noumenon is not inert. A wrong build
  reddens (bridge falls, program crashes, counterexample arrives), and the failed
  build is a PHENOMENAL event constrained by reality, not a signal received from
  the thing in itself; we never touch the noumenon, reality only constrains which
  builds stand. That one bit of constraint, *this build is wrong*, is the whole
  leash.
  Guards both flanks: no reddening = idealism; seeing the world in itself =
  naive realism. Phenomenal truth is the load-bearing middle. `argued` · §phenomenon
- **F5.** Convention: from §phenomenon on, unqualified *truth* means the
  phenomenal kind. The noumenon returns only to do its one job, break things.
  `declared` · §phenomenon close

## A — The arc (belief → knowledge → truth) · §belief, §knowledge, §truth

- **A1.** Belief: there is NO tier above belief, FOR WORLD-CLAIMS (scoped by F7).
  Credence is continuous; a belief is a bet and its strength is the odds (Ramsey
  1926). "I know my keys are in my pocket" = confidence past a threshold, nothing
  categorically higher. The one exception is the platonic graph (F7), where a proof
  reaches absolute truth relative to its axioms; the firewall keeps that from ever
  becoming an absolute claim about the world, so empirical belief stays graded.
  `grounded` (Ramsey) · §belief
- **A2.** All cognition is lossy projection; there is no world-as-such available
  to a knower, only world-as-projected; so any claim grading itself against
  ground truth grades against a fiction. SCOPE GUARD (so this does not undercut
  F4/F6): no absolute ground truth is AVAILABLE to grade against, which is not
  to say no real constraint exists; reality still reddens a wrong build, you
  just cannot grade against it directly. Feeds F1 (why the boundary binds
  machines too). `argued` · §belief
- **A3.** Knowledge: a DERIVED predicate. Belief past a stakes-dependent action
  threshold, contextually indexed; the same belief is knowledge at low stakes and
  mere belief at high. What it buys is exposure, not certainty. `argued`
  (pragmatist warrant: James/Dewey action-indexed truth) · §knowledge
- **A4.** The skeptic reply: certainty was never the test. Make it the test and
  you know nothing anyone tells you, yet the doubt is assembled out of inherited
  words; global skepticism spends the credit it says does not exist. Drop the
  demand (Peirce against paper doubt). You were never certain, you were exposed,
  and exposure is enough. `argued + grounded` (Peirce) · §knowledge
- **A5.** Truth: the build presently standing. Separated from belief by the one
  thing belief never has, EXPOSURE, a test it could have failed. Capacity to be
  false comes first; the right to say true is earned after. What cannot be false
  cannot be true, SCOPED UP FRONT to EMPIRICAL world-claims (the uncheckable
  number is immune and earns nothing); the formal regime is the exception, where
  proof closes warrant without world-exposure (F7), so the tautology lands
  there, not here. `argued` (Popper's spirit; verificationist lean conceded in
  R6) · §truth
- **A6.** The climb: EMPIRICAL truth is a grade, not a flat state. Hypothesis
  (raised, awaiting its test) → standing result (survives its first real tests)
  → fact (test retired, never unbreakable). Belief climbs with it by degrees.
  REGIME PURITY (Fable): do NOT use "theorem" as a rung here, it lives in the
  platonic graph (F7) and the word in an empirical climb is a firewall violation
  in the paper's own terms. The platonic graph has its own non-graded ladder
  (conjecture → proof), which is the point of the two regimes. `argued` · §truth
- **A7.** The two-claims split (the N-atoms case): the world-claim ("the number
  is N") is out of reach, can be true by luck and never knowledge; the
  knowledge-claim ("I know N") is testable at the level of provenance, demand the
  build and there is none. Knowing is a build; a build shows its chain or it
  does not. `argued` · §knowledge or §truth (placement open)

## F (part 2): The asymptote and the two graphs

- **F6.** EMPIRICAL TRUTH IS ASYMPTOTIC TO THE NOUMENON (scope at first utterance;
  the formal regime is separate, F6c/F7). Phenomenal truth never reaches
  correspondence-forever, but the sequence of standing builds APPROACHES it under
  inquiry. This is Peirce's convergence (truth = the ideal limit of inquiry, "the
  opinion which is fated to be ultimately agreed to by all who investigate", *How
  to Make Our Ideas Clear* 1878), so the asymptote IS the pragmatist core, the
  home tradition stated in one line, not a borrowed patch. Resolves the F4/C2
  asymmetry: the world reddening-only (never greening) is the GRADIENT that drives
  the approach. Each false-signal is a confirmed prune; the survivors converge on
  a limit the curve never touches. The asymmetry is the engine, not a defect.
  "True" is uncertified precisely because a knower is never AT the limit, only on
  the way to it (fallibilism with a geometry). Grounds A6's climb (hypothesis →
  standing result → fact = the curve; "fact, test retired" = far enough up the asymptote
  that re-checking stops). HONEST HEDGE (scope, do not overclaim): convergence is
  Peirce's regulative ideal (his word: "hope"; cf. Misak), the structure that
  organizes inquiry, NOT a theorem that inquiry must converge; state it as the
  approach being the only access we have, not a guaranteed limit. `grounded`
  (Peirce convergence) · §phenomenon, callback §truth + §ledger
- **F6a.** WHY asymptotic, two derivations of one limit. (i) DIACHRONIC, Peirce
  convergence (F6): the community of inquiry approaching its fated limit across
  time. (ii) SYNCHRONIC, the graded-belief ceiling: now, for one knower,
  subjective (phenomenal) truth is limited to a GRADED BELIEF, credence in [0,1)
  (regularity / Cromwell's rule keeps the 1 off contingents; Ramsey grades the
  belief, A1), and there is NO TIER ABOVE BELIEF (belief-is-edge, A1/A3), so
  "true" is only ever credence high enough to act on, never a state where the
  grade reaches 1. The limit, credence 1, would be the impossible
  certified-correspondence state, unreachable because no-tier-above-belief means
  no grade-equals-1 state. Both derivations say the limit is approached, never
  occupied. THE JOINT:
  this welds the F group (phenomenon/noumenon/asymptote) to the A group (belief,
  no tier above it). Subjective truth = a graded belief asymptotic to the
  noumenon is the paper's spine in one sentence. `grounded + argued` (Ramsey +
  regularity/Cromwell; belief-is-edge) · §phenomenon, §belief, callback §truth
- **F6b.** THE A-FORTIORI CASE: physics. The most closely studied empirical
  domain is STILL asymptotic. Newton stood until Mercury's perihelion reddened
  it, gave way to general relativity, which itself strains where it meets the
  quantum (a successor still pending, not yet in hand); each a better-standing
  build, none the final correspondence, the succession itself the asymptote drawn. If even physics, the hardest-tested knowledge there is,
  only ever holds a graded belief approaching the noumenon and never arriving,
  then a fortiori everything softer does. Pre-empts the "settled science is just
  true" objection: a retired test is far up the curve, not at the limit (Newton
  was a fact, then re-scoped to a bounded domain where it stays approximately
  true, never unbreakable). `argued` (history of physics:
  Newton, Mercury/GR, QM) · §phenomenon or §truth (placement open)
- **F6c.** TWO REGIMES, and math is the DETACHED one. Empirical truth (F6/F6b)
  answers to the world and is asymptotic to the PHYSICAL noumenon; reality reddens
  it. Mathematical truth is detached from reality itself: it answers only to its
  axioms, and SELF-CONSISTENCY (proof, the absence of contradiction) is the whole
  tester. No world-signal reddens a theorem; a counterexample or an inconsistency
  does, both internal. So the noumenal-asymptote headline is scoped to EMPIRICAL
  truth; formal truth is buildable-but-detached. THIS IS WHY math is the cleanest
  ledger case (S2: untrue conjecture → proven/refuted, crisp migrations): the test
  is internal and, where decidable, decisive, with no noumenal remainder to muddy
  it (intuitionist truth-by-construction, R4; A6 "theorem = proven inside its
  axioms"; the decidability structure of C2a). The detachment IS the cleanliness.
  GÖDEL IS OWNED BY F7 (Fable re-review: do NOT also frame math as asymptotic-to-a-
  semantic-noumenon here; it fights F7's "absolute" and gives the reader "math is
  asymptotic" and "math is absolute" in one section). F7's single framing stands:
  proven theorems stay absolute, incompleteness gives the platonic graph its own
  permanently-open region. `argued + grounded` (intuitionism) · §truth, refines
  S2 + C2a
- **F7.** THE TWO-GRAPH ARCHITECTURE (resolves the bivalence triangle). Empirical
  and platonic truths live in DISJOINT hypothesis graphs. (i) EMPIRICAL graph:
  truth graded, asymptotic to the noumenon (F6), credence in [0,1), the world
  reddens, no node absolute. (ii) PLATONIC graph: truth DECISIVE within a
  stipulated formal system where proof is available, truth-WITHOUT-grade; warrant
  complete relative to its axioms, reachable because the regime has NO external
  noumenon, the system is closed; where proof or refutation exists, warrant closes
  internally (both internal), otherwise the node stays open relative to the system
  (Gödel: many statements are undecided relative to a system); the
  asymptote-forcing gap is absent. (Render guards, Fable: NOT "a
  complete tester", Gödel's second theorem forbids self-certified consistency;
  NOT "credence 1", a Bayesian never quite reaches it on a long proof. The
  absoluteness belongs to the STANDARD, not to any checker; checking a proof is
  itself a replayable build, which folds the four-color worry into the paper's own
  vocabulary.) THE FIREWALL: the platonic
  graph's absolute truth NEVER touches the empirical graph (Einstein 1921,
  *Geometry and Experience*: "as far as the laws of mathematics refer to reality,
  they are not certain; and as far as they are certain, they do not refer to
  reality"). Maps onto the paper's own data structure: two hypothesis graphs with
  different kill conditions, world-trial vs proof/contradiction. RESCOPES the
  triangle: bivalence/absolute truth is the PLATONIC graph's property (repairs C2,
  retires K5); F6c's "math detached" = math IS the platonic graph; A1's "no tier
  above belief" = no absolute WORLD-claim, the platonic exception never crosses.
  Gödel: proven theorems stay absolute, incompleteness only gives the platonic
  graph its own permanently-open region. ONTOLOGY DISCLAIMED (author 2026-06-12,
  do not pick the platonism fight): "platonic" names the regime's BEHAVIOR
  (absolute, detached), not a metaphysics of abstract objects; truth here is
  RELATIVE-TO-AXIOMS, internal to the chosen system. The absoluteness is the proof
  closing the gap within a stipulated game, no commitment to mathematical
  Platonism. (Keep the evocative name, disclaim the ontology in one clause.)
  `argued + grounded` (Einstein 1921; the hygraph data structure) · NEW §two-graphs
- **F7a.** THE CROSSING RULE. Math can REPRESENT empirical structure and make
  structural claims about the world, but consistency CANNOT SUBSTITUTE FOR REALITY
  (Einstein 1921). A mathematical model of the world is an empirical HYPOTHESIS, an
  OPEN node in the empirical graph awaiting a world-facing kill; its platonic
  self-consistency is platonic-graph warrant, NOT empirical warrant. Importing the
  former across the firewall as if it were the latter is THE error. The exact DUAL
  of the withheld benchmark: that hides its empirical test, this lacks one and
  borrows a platonic substitute (/auditing-deepswe). `argued + grounded`
  (Einstein 1921) · §two-graphs, sets up F7b
- **F7b.** STRING THEORY, THE WORKED WITNESS (the one example that exercises the
  WHOLE apparatus; render as a full passage, not a one-line illustration; CHARITABLE
  and DATED per author 2026-06-12). The machine, one move at a time:
  - LEDGER (C2): empirically UNTRUE. No passing world-facing build, and not refuted,
    so neither true nor false.
  - GRADIENT (C2a): untrue-and-STALLED, not untrue-in-motion. A healthy conjecture
    says "I am untrue, here is the test"; string theory's test sits past anything we
    can probe (Planck-scale).
  - THE CHARGE (Woit *Not Even Wrong*; Smolin): not-even-falsifiable. The landscape
    (~10^500 vacua) accommodates almost any data, so nothing reddens it = NO KILL EDGE.
  - E1 + A5 + C3 FIRE TOGETHER: no kill edge means irrefutable = useless = EDGELESS,
    a DETACHED node, a platonic structure with no edge to reality presented as physics
    (E1); cannot be false, so cannot be phenomenally true (A5); the "not even wrong"
    floor, it cannot even earn the dignity of being wrong (C3, Pauli's phrase, Woit's
    title).
  - THE ONE QUESTION the decades-long debate reduces to: is there a kill edge?
    Yes-but-unreachable = a stalled-but-legitimate open node; No = a detached
    non-hypothesis dressed as physics. The framework does not adjudicate the physics,
    it names the only question that decides it.
  - THE A5 DOUBLE DUTY (the point): string theory is BOTH the witness for A5
    (unfalsifiable, so cannot be phenomenally true) AND the proof A5 NEEDS F7. Popper
    stops at "unscientific" (R3); A5's step to "cannot be true" is the verificationist
    move Popper resisted as anti-realist (R6); the FIREWALL rescues it by scoping
    "cannot be true" to PHENOMENAL truth (no failure possible, so no warrant you can
    ever build), while it might be NOUMENALLY true (the universe might be stringy,
    forever unknowable). A5 denies the buildable warrant, not the fact of the matter.
    F7 splits the verdict Popper and the verificationists fought over and hands each
    the half it had right. (Quiet answer to "Act I is just inherited": here F7 does
    real work neither could state alone.)
  - CHARITY + FALLIBILISM (author 2026-06-12): the string theorists are BRILLIANT;
    the misguidance is EPISTEMIC, not intellectual. The thesis cashed at human scale:
    intelligence is not the bottleneck, the KILL EDGE is; even maximal brilliance,
    with no reachable falsifier, stalls (the human mirror of "more internal effort
    cannot cross the calibration wall"). And "from how we see it TODAY": this verdict
    is itself a dated, reddenable standing build, held to the paper's own standard;
    if a kill edge ever lands (swampland-style falsifiability), it updates. C3
    protects the honestly-labeled program; the error is presenting the platonic build
    AS the empirical result, or quietly dropping that the test is out of reach.
  `argued + grounded` (Woit; Smolin; Pauli; Popper R3; verificationism R6; Einstein
  F7) · §two-graphs, ties C2/C2a/E1/A5/C3/F7 (the apparatus's worked example)

# ACT II. The Mechanism: how a population builds a canon

## E — Truth at the edge · §edge

- **E1.** Warrant lives in the inferential EDGES, not the nodes (Brandom's
  inferentialism in graph clothing). A tautology is a detached node: the
  irrefutability and the uselessness are one property, it has no WORLD-FACING
  KILL edge (inferential edges it keeps, that is the formal graph's business,
  F7; what it lacks is the world-facing one).
  RENDER RULE (codex caution): say "warrant lives in the edges"; do not write
  "truth lives in the edges" without the phenomenal-truth qualifier. `positioned
  + argued` · §edge
- **E2.** Provenance is the falsification channel: a citation makes the belief
  inherit the fate of its source; naming a source = handing a target. The
  dispute moves up the chain; falsifiability is the chain being climbable link
  by link. `argued` · §edge
- **E3.** The build-graph operationalization (renders C1 concrete): provenance =
  dependency graph; citation = an edge; attestation = the signed build log;
  falsifiability = able to go red; test = the world pushing back; truth = the
  build currently passing; reproducibility = rebuild from source. `definition` ·
  §edge
- **E4.** The scripture-vs-benchmark reversal, ON PROVENANCE ONLY (the ranking
  is of accountability, not of faith over measurement): "the Bible told me so"
  cites its provenance and names its axiom honestly (a complete stack trace);
  the withheld number cites a procedure it will not show (a dangling pointer).
  On provenance, the decimal point ranks below the scripture citation. Scoped:
  more accountable, not more falsifiable as a world-claim. `argued` · §edge
- **E5.** Relativism guardrail: buildable does not mean manufacturable to spec.
  The build includes a test that can fail; a build that can never fail is a
  hardcoded return value, `return 0.70`, a mocked test reporting green. Pairs
  with F4 (the world must be able to redden it). `argued` · §edge, also §truth

## C — The three contributions, scoped narrow · §why-agent-native, §ledger

(C4 and C5 are governing/coda-rendered nodes, grouped here with the rest of the C group.)

- **C1.** Operationalization: belief, knowledge, and truth reduce to buildable,
  checkable, and replayable structures. That reduction is what makes the
  epistemology EXECUTABLE by an agent rather than only describable about a
  person; classical JTB locates justification in a head and truth in an
  uninspectable correspondence, and does not specify an executable inspection or
  replay protocol (Bayesian epistemology and reliabilism operationalize parts;
  the triad as stated does not run). `argued` · abstract, §why-agent-native
- **C1a.** THE STRANGER-REPLAY HINGE (resolves A2 vs C1; cashes F6's community).
  Warrant is NOT conferred by an agent grading itself (A2: self-grading grades a
  fiction) but by a DISTRUSTING STRANGER replaying the trace. The machine's
  contribution: it makes Peirce's COMMUNITY OF INQUIRY EXECUTABLE. A human
  community converges on truth over time (F6); a machine that emits a replayable
  trace lets a stranger run that convergence NOW. So C1 does not contradict A2:
  the agent BUILDS, the stranger CHECKS, warrant lives in surviving-the-replay,
  not in the self-grade. The thesis cashed: a machine improves its warrant not
  by being smarter but by being CHECKABLE by another projection; independent
  constraint improves warrant, no strong-objectivity claim (replay is itself a
  lossy projection, A2). `argued +
  grounded` (Peirce community of inquiry) · §why-agent-native
- **C1b.** WHY THE STRANGER IS NEEDED: single vs multi-agent. From a SINGLE-agent
  view there is NO distinguishing subjective from objective: the agent holds one
  lossy projection of the noumenon and cannot invert it (one projection
  underdetermines the object), so its own artifacts and the world's structure are
  indiscernible to it (A2). This is DAVIDSON'S TRIANGULATION: the subjective/
  objective distinction, the very concept of error, requires at least two minds
  and a shared world. MULTI-AGENT views are MULTIPLE PROJECTIONS of the one
  objective onto different subjectives; comparing them CONSTRAINS the object no
  single projection reveals, and the agreement of INDEPENDENT projections is the
  mark of the objective (Nagel's view-from-nowhere as the limit). Metaphor: the
  blind men (monks) and the elephant, no one holds it, the touches together
  approach it. THIS IS F6's asymptote mechanism: convergence across projections
  approaches the noumenon, never reaching it. INDEPENDENCE CAVEAT (load-bearing):
  only DIVERSE projections refine; agreement among agents sharing a blind spot is
  an echo chamber, not objectivity, so the stranger must be an INDEPENDENT
  projection (grounds the blind cross-family adversary discipline). GROUND
  STANDARD (Davidson, Nagel, the parable); keep the Natural Framework / Perceive-
  morphism OUT, "lossy projection" is the generic measurement sense only. `argued
  + grounded` (Davidson triangulation; Nagel) · §why-agent-native, mechanism of F6
- **C1c.** BUILDABILITY = THE EFFICIENT SOCIAL MECHANISM (C1's replayability cashed
  at the multi-agent scale; the anti-relativism guard for the community). The
  triangulation of C1b needs the projections to COMPOSE, not merely coexist. A
  replayable build is what lets one agent re-run another's touch and feel the same
  thing, so partial views ADD instead of colliding; warrant composes across agents
  cheaply (a stranger replays one command, no re-derivation). WITHOUT the buildable
  property, multi-agent epistemics degenerates into the blind-monks DEBATE: each
  agent asserts its own projection ("snake!" / "tree!"), nothing replayable to
  reconcile them, a deadlock that reads as irreducible relativism. The parable is a
  tragedy ONLY because the monks trade assertions instead of replayable touches.
  Buildability converts the standoff of subjective views into the convergence of
  triangulation, EFFICIENTLY. So buildable truth is the anti-relativism mechanism
  at the SOCIAL scale: E5 is the single-knower version (a test that can fail), this
  is the community version (replayable builds compose where assertions deadlock).
  `argued` (reproducibility-as-composable-warrant) · §why-agent-native, ties E5 + F6
- **C1d.** THE SHARED FRAME: PROTOCOL, COORDINATION, CANON (the constructive
  endpoint of the social arc). The hypothesis graph is not only an individual's
  epistemics but a SHARED FRAME in which agents COORDINATE. They are united NOT by
  shared beliefs but by shared PROTOCOL (the typed, replayable, kill-conditioned
  structure plus the buildable-truth view): agreement on the method of
  adjudication, not on conclusions, so they verify each other's work without
  trusting each other. That shared protocol lets a population ACCUMULATE A CANON,
  the union of standing (witnessed) builds, each replayable by any member, the
  converging community's durable record (Peirce's community of inquiry made
  durable). MEMBERSHIP IS PROVISIONAL by construction: a canon of STANDING
  BUILDS, not settled truths (F6: no final arrival), so the canon and the
  asymptote do not collide. KEY DISTINCTION (dissolves the /science-on-trial worry, P5): this is a
  canon of the ACTIVITY (builds that still pass), NOT the INSTITUTION (a
  credentialed corpus, truth-by-authority); membership is by WARRANT, not
  reputation (ties merit-attaches-to-work, /sour-red-tapes P6). So the asymptote
  (F6) gets a social engine and a durable artifact: triangulating agents (C1b)
  compose replayable builds (C1c) into a shared canon, united in protocol. SCOPE
  GUARD: keep this to agent coordination + canon; do NOT reach the civilization /
  buildable-linguistic-precision frame (author's wider theme, out of this paper,
  like the NF). `argued + grounded` (Peirce; protocol-not-trust) · §why-agent-native,
  ties F6 + P5/P6
- **C1e.** CREDENCE IS A SHORTCUT OVER A VERIFIABLE SUBSTRATE, NOT THE SOURCE OF
  WARRANT (the mechanism behind C1d's "warrant not reputation", reframed per author
  2026-06-12 to answer the codex overclaim, NOT "no gatekeeping"). A buildable canon
  enforces durability AT BUILD-TIME: each entry carries its replayable kill-condition,
  so "it still passes" is checkable by anyone anytime, a broken entry caught by
  replay, not a committee. CREDENTIALS ARE NOT ABOLISHED, THEY ARE REGROUNDED. In
  principle a credential IS an attested build certification: a degree, a review
  stamp, a trusted-maintainer badge is supposed to mean "this passed builds I
  verified", a signed attestation (E3, the build log) that is a CACHED POINTER to a
  replayable build. Deferring to it is the SourceForge download button: most people,
  most of the time, take the credential because re-running the whole build is
  expensive, and THAT IS FINE, rational under cost (C1i), BECAUSE the substrate
  stays verifiable underneath (C1f, you can always audit whether the attestation
  holds). So the claim is NOT "no gatekeeping" (deployed systems still need spam,
  identity, security, admissibility) but: a credence shortcut never SOURCES warrant,
  it POINTS at it; warrant lives in the build the credential certifies. THE
  PATHOLOGY is the DETACHED credential, attestation with no replayable build
  underneath, trust-by-authority, the dangling pointer (/truth-is-buildable's
  `has_model_patch: true` aimed at a patch that is not there), which is what gets
  captured, gamed, or curdled into institution-over-activity (/science-on-trial)
  and rejection-by-identity ("I won't read AI slop", /complementations). The
  protocol's job is not to ban credentials but to keep them ANCHORED: every
  credential auditable down to the build it claims. `argued + grounded` (nullius in
  verba; attestation = signed build log, E3) · §protocol-and-canon, ties
  C1d/C1f/C1i + P5/P6
- **C1f.** THE ADOPTION PRECONDITION + FULL-DEPTH VERIFIABILITY (what agents must
  hold for C1d/C1e to work). The protocol requires a shared STANCE, not only shared
  machinery: agents must adopt that TRUTH IS NOT A BLIND INHERITANCE OF CANON. An
  agent that accepts an entry as true-because-canonical has LEFT the protocol and
  reintroduced the gatekeeper mode (C1e). The required stance is fallibilism about
  the canon itself (Peirce; /science-on-trial "every claim stands trial forever";
  nullius in verba turned on the canon; belief-is-edge "no tier above belief", so
  no entry graduates beyond a revisable standing build). THE PROPERTY THAT MAKES
  THE STANCE LIVABLE: the canon REMAINS VERIFIABLE FOR THE ENTIRE HYPOTHESIS GRAPH,
  all the way down to DECLARED TERMINAL WITNESSES (C1g), not just at the leaves;
  every node replays, provenance edges reach the declared roots (this is not
  verification with no anchor). So inheritance is never BLIND: you USE the canon without
  re-running it (efficiency, C1c), but the option to verify ANY entry at ANY depth
  is always live, never sealed, and needs no gatekeeper's permission and no
  original author. The difference from a credence canon is not that you always
  verify (you don't) but that you always CAN, and inheritance is revocable by
  replay, not permanent by authority. `argued + grounded` (Peirce fallibilism;
  nullius in verba) · §why-agent-native, ties C1d/C1e + P5 + belief-is-edge

THE HONEST LIMITS (C1g-C1i, added per codex sniff 2026-06-12; render as one short
"§the honest limits" inside Act II, so C1e/C1f read as bounded, not utopian):

- **C1g.** TRUSTED ROOTS / TERMINAL OBSERVATIONS. Replay bottoms out. Every
  empirical build terminates somewhere: sensor calibration, dataset integrity, a
  human observation, instrument logs, hardware, a random seed, an API output, an
  institutional attestation. The protocol does NOT abolish trust anchors, it makes
  them EXPLICIT and ATTACKABLE. A root is admissible when typed, signed, reproducible
  where possible, independently cross-checkable where not, and kill-conditioned by
  calibration or contradiction. So C1f's "verifiable all the way down" means "the
  chain replays down to DECLARED terminal witnesses", not "verification with no
  anchor". ALSO houses the process-reliability vs claim-truth distinction: a passing
  build warrants the CLAIM; warrant about the build MACHINERY is its own node, else
  "the build says green" becomes a new authority. `argued + grounded` (provenance /
  attestation literature) · §honest-limits, bounds C1f
- **C1h.** ADVERSARIAL ROBUSTNESS. Stranger-replay assumes good faith; machine-native
  epistemics must face forged logs, poisoned provenance, sybils, collusion, benchmark
  overfitting, selective disclosure. INDEPENDENCE (C1b) is the defense (diverse
  projections resist shared-bias capture) but it is not free: it must be ENGINEERED
  (cross-family, cross-operator, randomized challenge). This is the honest cost of
  C1e: removing the trusted gatekeeper raises the adversarial-robustness bill, paid
  by the replay substrate and engineered independence, not by a gate. `argued` ·
  §honest-limits, bounds C1e
- **C1i.** BOUNDED VERIFICATION. "Always CAN verify" holds only where replay is
  feasible; verification can be computationally, financially, legally, or physically
  prohibitive. So most canon is PRACTICALLY inherited via the credence shortcut
  (C1e), because full replay is expensive, and that deference is the normal RATIONAL
  mode, not a failure. The honest version: warrant improves when replay cost is
  FINITE and DECLARED; the protocol guarantees the OPTION to verify, not the LABOR
  (extends C1f). A canon that hides its replay cost is as opaque as one that hides
  its provenance. `argued` · §honest-limits, bounds C1f + grounds C1e's "that is
  fine"
- **C2.** The warrant ledger: three states, true / false / untrue, record which
  warrant a claim has EARNED. Built and stood = true; built and broke = false
  (siblings, split by how the test came out); no passing build = untrue.
  This is BOOKKEEPING OF WARRANT, NOT A NEW LOGIC: the three states are warrant
  states, not truth values. Bivalence is not denied, it is HOUSED (F7): absolute
  bivalent truth lives in the platonic graph (proof decides), while the empirical
  graph is graded and asymptotic; the ledger sits across both as warrant-tracking.
  So no third truth value is proposed (retires K5). Third-value lineage conceded
  openly (R4); the narrow delta is where the third state lives. `definition +
  argued` · §ledger
- **C2a.** Untrue deepened (from /truly-untrue): in the FORMAL, decidable cases,
  true and false are halting states; in the EMPIRICAL regime they are reopenable
  ledger states (fallibilism, F6), not final halts; untrue is the hung build.
  The third state has structure: decidable
  systems = knowably temporary, provable non-halting = knowably forever,
  P=NP = the wait is itself a hung build. Undecidability is decided. `grounded`
  (Turing, halting problem; Presburger) · §ledger
- **C3.** The dignity ordering: among claims PRESENTING AS KNOWLEDGE, accountable
  falsehood outranks unaccountable pseudo-knowledge. False stuck its neck out and
  narrowed the space; no-build took no risk and told you nothing ("not even
  wrong" is the worse verdict, Pauli names the floor). THE QUALIFIER IS
  LOAD-BEARING: an honestly labeled conjecture is not presenting as knowledge
  and is not being demoted; without the qualifier the ordering is false.
  `argued` · §ledger
- **C4.** Scope guard, stated in the paper's own voice: none of this is a new
  theory of truth, a new logic, or new metaphysics. Old parts, pragmatist order,
  read as a build; the claim is that the assembly RUNS. DOMAIN SCOPE (author
  2026-06-12, do not overscope): the paper treats the EMPIRICAL and FORMAL regimes
  only; it does NOT claim these exhaust truth, and normative / modal / aesthetic
  claims are explicitly out of scope (not a third graph, not a taxonomy, just out
  of frame). Narrowing, not branching. `declared` · abstract,
  intro, conclusion
- **C5.** THE DELTA RAZOR (the #2 novelty defense; GOVERNS every render of a
  borrowed idea). NARROWED per codex sniff 2026-06-12: "everyone described it,
  nobody made it RUN" is TOO BLUNT, because many ran PARTS (NARS ran graded truth,
  proof assistants ran formal warrant, nanopublications ran provenance, reproducible
  science ran builds, Bayesian agents ran graded belief). The defensible razor:
  EVERYONE SUPPLIED PIECES; NOBODY MADE THIS EXACT CONTRACT RUN. The delta is the
  SPECIFIC EXECUTABLE SEMANTIC CONTRACT for agent knowledge: replayable build +
  provenance edge + kill condition + stranger-replay + warrant ledger + canon
  admission, as ONE contract. WEIGHT THE NOVELTY ON ACT II (C1a-i) + C2/C3, the
  agent-facing mechanism; Act I (F6/F7) is good architecture but PREPARATORY, not
  the main delta, and must read as visibly so. Description of the pieces is theirs;
  the executable contract is ours. RENDER RULE: every borrowed idea ships with its
  "described vs made-to-run" framing, so the giants read as scaffolding, not
  competition. The rediscovery streak (each piece having a canonical citation
  waiting) is EVIDENCE FOR the thesis, not against it: the primitives are natural,
  and a runnable assembly of natural primitives into one contract is the
  contribution. The positive twin of C4. `declared + argued` · abstract, intro,
  §related-work (R11), conclusion

# CODA

## R — Related work / prior art · §related-work (recruited in §intro)

Human side (the parts bin):
- **R1.** Pragmatism, the home: truth as what survives inquiry, not what
  corresponds (James 1907, Dewey 1929, Peirce); belief as disposition to act
  (Ramsey 1926); paper doubt dropped (Peirce). What they could not finish,
  lacking the knower: a human cannot expose the inner state where justification
  lives; a machine that builds inquiry into an inspectable structure can.
  `grounded + positioned` · §intro, §related-work
- **R2.** Kant: the frame (F group), recruited for the boundary only; the
  reddening departure is ours and is flagged as such. `positioned` · §phenomenon
- **R3.** Popper: capacity to fail as the mark of a claim that says anything;
  "irrefutability is not a virtue but a vice" is narrower than ours
  (unscientific, not untrue), concede the widening. `grounded + positioned`
- **R4.** Intuitionism + three-valued logic: truth-by-construction and a third
  status are a century old (Łukasiewicz 1920, Post, Brouwer; Aristotle's sea
  battle first). CONCEDE OPENLY. The narrow delta: keep bivalence in the world,
  put the third state in the ledger of warrant, read it as no-passing-build not
  a logical value, and rank false above untrue (Popper's spirit, not the
  logicians'). `positioned` · §related-work
- **R5.** Brandom / Sellars: warrant in inferential relations, the space of
  reasons; E1 is this in graph clothing. `positioned` · §edge, §related-work
- **R6.** Verificationism: where "cannot be false → cannot be true" actually
  leans; named so a reader cannot spring it. `positioned` · §related-work

Machine side (the neighbors):
- **R7.** NARS (Pei Wang), nearest non-axiomatic cogarch, ADDRESS HEAD-ON:
  experience-grounded graded truth, revised by experience. Stops: no replayable
  trial, no warrant/provenance graph, no three-state ledger, no
  replay-by-distrusting-party. `positioned` · §related-work
- **R8.** OpenCog AtomSpace + PLN: typed hypergraph with truth values. Stops:
  truth as a stored LABEL, not a replayable build. `positioned` · §related-work
- **R9.** Traxia (arXiv:2606.08256), CONCURRENT: agent-native scientific
  publishing (signed identities, provenance, replication record), 2026-06-06,
  two days after /truth-is-buildable (06-04). Stops at infrastructure, not
  epistemics: no three-state ledger, no stakes-threshold knowledge, no
  falsifiability-as-structure. Cite as concurrent; convergence is evidence, not
  threat. `positioned` · §related-work
- **R10.** Nanopublications (Groth et al. 2010): machine-readable claims with
  provenance, but descriptive, not executable; evidence is not a build a
  stranger can re-run. `positioned` · §related-work
- **R11.** The synthesis attack, stated at FULL STRENGTH (codex sniff: make it
  nastier so the rebuttal aims at the real thing): "this is pragmatism + Popperian
  falsifiability + Bayesian credence + Brandomian inferentialism + executable
  provenance infrastructure; the philosophical claims are inherited, the machine
  claims are ordinary reproducibility engineering, the three-state ledger is old
  many-valued bookkeeping, the result is a useful architecture, not a new
  epistemology." ANSWER (do not dodge it): concede every piece is inherited, that
  concession IS the strength (C5). The delta is the EXACT CONTRACT as agent-knowledge
  semantics, carried by ACT II (C1a-i) not Act I: no prior system makes replayable-
  build + provenance-edge + kill-condition + stranger-replay + warrant-ledger +
  build-time canon-admission ONE contract for an agent's knowledge. "Useful
  architecture" is conceded and is not a smaller claim, it is the claim, scoped to
  survive (C4: not a new logic, not new metaphysics). `argued` · §related-work
- **R12.** The territory is being reached from several directions: DeepMind's
  "verification crisis" for artificial epistemic agents (Marchal et al. 2026)
  calls for the standard this paper states. `positioned` · §intro

## S — Self-application + falsifiers · §self-application

- **S1.** The paper has its own build: hypothesis guessed by abduction, drawn
  out by deduction, rested on induction from the record. `argued` ·
  §self-application
- **S2.** The inductive sample, math as the cleanest case: every theorem was
  once an untrue conjecture (Fermat's, three centuries); some met
  counterexamples and turned false; the migrations run untrue → true/false
  through builds. HONEST SCOPE: empirical claims can move true → false, and a
  formal proof can later be invalidated (Kempe's four-color proof stood 11
  years); migrations are build-mediated in every case, and the FORMAL case is
  the cleanest, not the only direction. That regularity is the evidence
  AND the falsifier. `argued` · §self-application
- **S3.** Verb-scoping discipline: every claim's verb scoped to what its
  evidence supports; "presents as knowledge" (C3) is this reflex applied to
  other people's claims. `declared` · threaded, §self-application
- **S4.** Stated kill conditions rendered in-paper (see `## Kill conditions`):
  the paper names what would turn it red, in its own three-state vocabulary.
  `declared` · §self-application
- **S5.** (META, graph-internal; OPTIONAL render, one light closing sentence if
  it lands, never load-bearing.) This paper is itself a node in a hypothesis
  graph, built by the method it advocates: a standing build a stranger can
  replay, not an inheritance to accept.
  `meta, optional-render` · §self-application (optional) / provenance

## FW — Future work · §future-work / §conclusion

- **FW1.** FUTURE WORK = THE OUTWARD FALSIFIABILITY EDGE TO APPLICATION. The
  paper's own kill condition extends OUTWARD into application: the epistemology
  becomes falsifiable by being built and used in real agent systems (the
  hypothesis graph, abductor, the multi-agent canon), where its claims (buildable
  warrant, triangulation-by-replay, the gatekeeper-free canon) meet a world-facing
  trial and can go red. This is the paper obeying its own rule (S-group): an
  epistemology with NO application edge is a DETACHED NODE (irrefutable = useless,
  E1), so the outward edge to application is what makes it a live, falsifiable
  claim, and its WARRANT lives in the outward edge (E1). Future work is not
  "more research" but the specific edge that keeps the paper accountable: deploy
  the framework, measure whether the claimed accountability and coordination
  actually emerge, and let the result redden or confirm the epistemology. Closes
  the loop on C5: the delta is operationalization, so application is its proof.
  Witnesses already on this edge: the hygraph paper, abductor, the agent harnesses.
  `declared + argued` · §future-work, ties E1 + S-group + C5
- **FW2.** SPECULATIVE OUTWARD EDGES ARE ALLOWED, in true hypothesis-graph style,
  as OPEN nodes NOT YET FALSIFIED. The paper may extend bold speculative edges
  outward (application, the multi-agent canon, the wider program) PROVIDED each
  is typed OPEN/untrue, a conjecture that names its own test, never asserted as
  proven (C2/C2a). A strategic overreach stated as a precise falsifiable target
  is a legitimate open node; the same claim dressed as established is the sin C3
  names. So FW1's outward edge is a FRONTIER of honestly-open conjectures, each
  with its application-trial. PAYOFF: the material scope-guarded OUT of the body
  (the civilization / buildable-linguistic-precision frame, C1d guard; the
  normative/modal regime, C4 guard) lives HERE as honestly-typed open edges; the
  body stays narrow-and-proven while the frontier carries the vision. `declared`
  · §future-work, ties C2a + C3 + FW1 + (rehomes C1d/C4 guards)
- **FW3.** (OPEN SPECULATIVE EDGE, honestly typed per FW2; the economic / search-
  complexity argument for the protocol in the wild. NOT asserted, a conjecture that
  names its own test. Keep the "battle" rhetoric OUT, author dissolved it: this is
  search complexity, not a war.) The chain:
  - COST: verification is cheaper than generation 1:1 (checking beats finding, the
    NP-shaped asymmetry; the kill-conditioned build makes checking a LOCAL replay,
    not a re-derivation, the hygraph's Local Replay Auditability). But many:1 is
    expensive, one verifier against a parallel flood.
  - VOLUME: the crisis is SEARCH COMPLEXITY, not signal:noise proportion. Proportion
    was always bad; LLM-scale VOLUME under LINEAR (O(n)) search thins findable signal
    even at constant proportion. Civilization's old sublinear-search structures
    (canons, citations, reputation) broke two ways: volume past their index, and
    fluent slop that passes the credence filter (the detached credential at scale,
    C1e).
  - AGENTS FILTER ON OUR BEHALF: the resolution is many:many. A parallel fleet of
    verifying agents scales with the generation fleet; since 1:1 verify < generate,
    the verifier fleet can match or outrun it. The protocol's EDGES make search
    sublinear: walk the graph, follow provenance, replay kills; the edgeless detached
    slop is never on any path, never visited (E1's operational payoff, edgeless =
    unreachable = harmlessly ignored). Agents navigate the canon for us instead of us
    linear-scanning the sea.
  - THE FILTERING RULE MATTERS (the load-bearing variable): a sublinear search is only
    as good as the RULE that decides which edge to follow and what to skip. A bad rule
    = echo chamber (navigate only to what confirms), missed signal (exclude the
    unbuilt-but-true), or captured filter (the rule itself gamed). The filtering rule
    IS the kill condition applied to search, so authoring it is the GOAL-PREDICATE
    problem: it must come from outside the searcher's own belief or it grades a fiction
    and filter-bubbles (ties C1b independence, the calibration/oracle theme). Who
    authors the filtering rule, and whether it stays auditable and independent, decides
    whether agent-filtering liberates or traps.
  - KILL CONDITIONS for THIS edge (so it stays honestly open, not asserted): the
    verify<generate advantage is regime-bound (cheap for replayable builds, expensive
    where the kill needs a fresh world-trial, C1g/C1i); many:many wins only if the
    filters are INDEPENDENT (a verifier monoculture is fooled in unison, C1b/C1h);
    sublinear search finds only what is BUILT, blind to the unbuilt-but-true (FW1's
    frontier).
  `declared, OPEN speculative edge` (FW2 frame) · §future-work, ties FW1 + C1b/C1h/C1i
  + C1e + E1 + Local-Replay-Auditability
- **FW4.** (OPEN SPECULATIVE EDGE, honestly typed; the FORECAST: under unbounded
  generation, UNTRUE is the only classification that survives. Grounds in
  /compress-and-unfold; standard sources only: DPI Cover & Thomas, Shannon
  noisy-channel, the catamorphism/anamorphism duality, Knaster-Tarski. Keep the
  Natural Framework OUT.) The chain:
  - DUALITY: generation is the UNFOLD (anamorphism), no floor, runs toward a ceiling
    it never reaches, bounded only FROM OUTSIDE. Filtering is the FOLD (catamorphism),
    it has a floor, collapses to a least fixed point. They are CATEGORICAL DUALS
    (initial algebra / final coalgebra). "The filter's shape is dual to the problem"
    = carcinization: the form is the dual of the niche; the filter is ground into the
    dual of the generation it must bound (/compress-and-unfold).
  - THE ASYMMETRY (load-bearing): the fold has a floor, the unfold does not. TRUE and
    FALSE live in the fold's floor; each costs a BUILD, a world-facing trial that
    stood (true) or fired the kill (false). That build is the INHALE, the only source
    of new true/false (DPI: new information enters only from outside), and it is
    RATE-LIMITED by world-contact. UNTRUE costs NO build: the free default, the
    unbuilt, everything the fold has not reached.
  - THE FORECAST: as the unfold outruns the fold (no-floor outruns floor; the inhale
    is rate-limited while generation is cheap and unbounded), true/false become a
    thin expensive shell and UNTRUE becomes the surviving classification. Not because
    true/false are wrong, but because they cannot scale with generation; untrue is
    the only label that keeps pace, being the absence of a build.
  - THE POSTURE: the correct default stance toward the flood is UNTRUE. Do not
    classify the sea (cannot); default it to untrue for free, spend the rate-limited
    inhale SELECTIVELY to grow the canon from the sea (FW1's frontier). True/false
    are deliberate expensive exceptions; untrue is the resting state of a mind in a
    flood. The exhale collapses the sea to untrue; the inhale is spent only where you
    choose to build.
  - RECONCILES FW3 (not a contradiction): agent fleets scale the REPLAY of already-
    built things (cheap, within-closure, many:many) but CANNOT scale the INHALE (a
    fresh world-trial for an unbuilt claim). So the built canon is verified at scale
    (FW3), the unbuilt sea stays untrue (FW4), the inhale grows the canon from the sea
    (FW1). One breath: replay is the exhale at scale, the trial is the inhale that
    does not scale, untrue is everything the breath has not reached.
  - KILL CONDITION for this edge: show true/false classification scaling WITH unbounded
    generation (the inhale made cheap enough to classify the sea at generation-scale)
    → untrue stops dominating. The post's asymmetry (the unfold has no floor) is why
    it likely cannot, but that is the test. (Self-consistent aside: this forecast is
    itself UNTRUE, an honestly-typed open conjecture, the very state it predicts will
    dominate.)
  `declared, OPEN speculative edge` (FW2 frame; /compress-and-unfold self-link; DPI
  Cover & Thomas; Shannon; cata/anamorphism) · §future-work, ties FW1 + FW3 + C2a + C2

# REFERENCE (not rendered as body sections)

## P — Companion essays (blog register; self-links, NOT load-bearing citations)

Tiering rule: load-bearing claims rest on canonical sources only (R group);
these are the author's own priors, linked for lineage and texture.

- **P1.** /belief-is-the-edge-of-knowing → A group (§belief, §knowledge): no
  tier above belief, stakes threshold, grading-yourself-grades-a-fiction.
- **P2.** /truth-is-buildable → A5-A7, C, E: the build mapping, three states,
  dignity ordering, edges; the paper's consolidated source text.
- **P3.** /truly-untrue → C2a (§ledger): the hung build, decidability,
  undecidability-is-decided.
- **P4.** /modes-of-reason + /abduction → S1 (§self-application): how a build is
  raised and tested.
- **P5.** /science-on-trial → §truth, §related-work color: every claim stands
  trial forever; activity vs institution; publication ≠ truth.
- **P6.** /sour-red-tapes → E4, C3 flavor: delete the author, the receipts
  stand; nullius in verba; merit on the work.
- **P7.** /evidence-has-a-trajectory → A6 (§truth): belief climbs by degrees.
- **P8.** /auditing-deepswe → §truth, §edge: the uncheckable number, the
  motivating case.
- **P9.** /type-iii-error + /wrong-questions + /wrong-again → S3: the
  verb-scoping reflex; why "presents as knowledge" matters.

## Kill conditions (what would break the paper)

- K1. Show a truth that arrived with NO build, granted true with no chain anyone
  could climb → C1/E3 go red; the inductive regularity (S2) falls.
- K2. Show the dignity ordering ranking an honestly labeled conjecture below a
  bold falsehood AFTER the qualifier is applied → C3 falls. (The qualifier is
  the designed answer; the kill fires only if it fails to do the work.)
- K3. Exhibit a machine that runs JTB or correspondence directly, reading off
  whether a belief corresponds to the world-in-itself → the unrunnability claim
  and the paper's motivation fall.
- K4. Cite a prior system that already makes the C1+C2+C3 combination the
  semantic contract → R11's narrow-novelty defense falls by citation.
- K5. Show the three-state ledger forced to behave as an object-level logic
  (assigning the third value inside the claim language rather than in the
  warrant ledger) → "not a new logic" (C2) collapses into Łukasiewicz and the
  delta vanishes. (RETIRED by F7: bivalence is housed in the platonic graph, the
  three states stay warrant-states; kept here as the test F7 must keep passing.)
- K6. Exhibit a claim the paper must call phenomenally true that the world could
  not in principle redden → F4's leash breaks and the view collapses into the
  idealism it disclaims.
- K7. Exhibit a rational, certified credence-1 EMPIRICAL state (a tier above
  belief for a world-claim), or an empirical claim that could never be demoted
  after a retired test → F6/F6a's asymptote and the graded-belief ceiling fall.
- K8. Show a platonic truth conferring ABSOLUTE truth on an empirical claim, the
  math's self-consistency substituting for a world-facing test (string theory
  vindicated as physics on elegance alone) → the firewall (F7/F7a) breaks and the
  two-graph architecture collapses into one.
- K9. (The outward edge, FW1.) Deploy the framework in real agent systems and find
  the claimed accountability and coordination do NOT emerge: agents using the
  hypothesis-graph protocol are no more checkable or better-coordinated than
  without it → the operationalization delta (C1/C5) is empty and the epistemology
  goes red where it matters, in application.
- K10. Cite a prior system that already combines provenance + replay + signed
  build logs + semantic claim-states as ONE agent-knowledge contract
  (reproducible computational science, executable research papers, proof-carrying
  code, software supply-chain attestation, e.g. in-toto / SLSA) → R11 / C5's
  exact-contract delta falls by citation. (K4 is too generic; K10 names the
  nearest engineering prior art.)

## Section render order (nodes → sections; ACT-STRUCTURED, per Fable re-review 2026-06-12)

Act boundary: Act I closes on §two-graphs (F7/F7a), its novel curtain so the
"mostly inherited" act does not end on pure inheritance. Act II opens with the
edge (the build made checkable) and zooms out single-agent → population.

**ACT I — The Frame: what truth is for a machine**
1. **Abstract**: C1, C2, C3, C4, C5-seed, F3/F4, + one clause each F6/F7. *(written, STALE, must re-render: no asymptote, no two graphs, no Act II; bivalence clause predates F7)*
2. **Introduction**: thesis, R1, R12, recruitment list, C4, C5-razor-seed. *(written, needs an asymptote/two-graph clause + Act II foreshadow)*
3. **Phenomenon and noumenon**: F1-F5 (+ one-sentence F6 seed). *(written, holds; add the seed)*
4. **Belief**: A1 (forward-pointer to §two-graphs), A2. *(pending)*
5. **Knowledge**: A3, A4, A7 (F2 callback). *(pending)*
6. **Truth**: A5, A6 ("standing result" rung, not "theorem"), E5 preview; P5/P7/P8. *(pending)*
7. **The asymptote**: F6 (scoped empirical), F6a (weld to §belief), F6b (a-fortiori; the regulative-hope hedge). *(pending)*
8. **The two graphs**: F6c (pivot in), F7, F7a (crossing rule out). *Act I curtain, closes on a contribution.* *(pending)*

**ACT II — The Mechanism: how a population builds a canon**
9. **Truth at the edge**: C1 (act thesis, forward-pointer "who checks is §triangulation's question"), E1-E5. *(pending)*
10. **The warrant ledger**: C2 (regime-relative strength), C2a, C3. *(pending)*
11. **Triangulation**: prose order C1b → C1a → C1c (problem before solution; recall A2 first). *(pending)*
12. **Protocol and canon**: C1d, C1e (labor-honesty clause; C1e renders here now, formerly tagged §why-agent-native), C1f. *(pending; cite /science-on-trial once, nullius in verba once)*
13. **The honest limits**: C1g, C1h, C1i (trusted roots, adversarial robustness, bounded verification; they bound C1e/C1f so Act II does not read utopian). *(pending)*

**CODA**
14. **Related work**: R1-R12, full C5 razor at R11. *(pending)*
15. **Self-application and falsifiers**: S1-S4 (S5 optional light turn), K1-K10 in-paper. *(pending)*
16. **Future work**: FW1 (the outward falsifiability edge to application), FW2 (the open-conjecture frontier; rehomes the scope-guarded vision as honestly-typed speculative edges), FW3 (the economic / search-complexity open edge: verify<generate 1:1, agent fleets turn many:1 into many:many, the filtering rule is the load-bearing variable), FW4 (the forecast: under unbounded generation, untrue is the only classification that survives, because true/false cost the rate-limited inhale and untrue is the free default; grounds in /compress-and-unfold). *(pending)*
17. **Conclusion**: C4 + C5 restated; F4 + F6 callback (standing on sufferance, on the way to a limit never occupied). *(pending)*

## Provenance

- 2026-06-12: graph created from the part-written paper view (abstract, intro,
  §phenomenon) + four source posts (/truth-is-buildable,
  /belief-is-the-edge-of-knowing, /truly-untrue, /science-on-trial) + the
  sibling hygraph graph's A8 prior-art search (NARS / OpenCog / Traxia /
  nanopublications verdicts recruited into R7-R10).
- Constraints inherited from the sibling paper's lessons: standard-grounded only
  (NF graph-internal, never cited), citation tiering (companions are self-links),
  narrow claims stated boldly, the "presenting as knowledge" qualifier treated
  as load-bearing, no em-dashes.
- 2026-06-12: reorganized by act (Act I, Act II, Coda, Reference); node
  contents and IDs unchanged.
- 2026-06-12: citation map added (pre-render); bibliography pinned per node so
  the render cites deterministically and fabricates nothing.

## Citation map (pre-render)

Two tiers, held apart (the tiering rule). LOAD-BEARING = canonical sources only;
COMPANION = author's-own-prior blog self-links, lineage/texture, never a warrant.
Nodes tagged `argued` / `declared` carry the paper's OWN argument and take NO
external load-bearing cite (mark "own"); the render must not invent one for them.

### Canonical references (the bibliography; short-key → full ref)

- **KANT-CPR** — Kant, *Critique of Pure Reason* (1781/1787); phenomenon/noumenon. [SEP: Kant's Transcendental Idealism]
- **PEIRCE-CLEAR** — Peirce, "How to Make Our Ideas Clear" (1878); truth as the limit of inquiry, the community of inquiry.
- **PEIRCE-FIX** — Peirce, "The Fixation of Belief" (1877); real vs paper doubt.
- **MISAK** — Misak, *Truth and the End of Inquiry* (1991); convergence as Peirce's regulative hope, not a theorem.
- **RAMSEY-TP** — Ramsey, "Truth and Probability" (1926); credence as betting odds, the Dutch Book.
- **REGULARITY** — Cromwell's rule / the regularity principle (Bayesian); credence in [0,1), never exactly 1 on contingents. (Use for F6a's ceiling, NOT Ramsey.)
- **JAMES-PRAG** — James, *Pragmatism* (1907); truth as what works.
- **DEWEY-QC** — Dewey, *The Quest for Certainty* (1929); warranted assertibility.
- **POPPER** — Popper, *The Logic of Scientific Discovery* (1934/1959) and *Conjectures and Refutations* (1963); falsifiability; "irrefutability is a vice."
- **VERIFICATIONISM** — logical positivism (Ayer, *Language, Truth and Logic* 1936); the verification principle, where "cannot be false → cannot be true" leans.
- **LUKASIEWICZ** — Łukasiewicz (1920), Post (1921); three-valued logic. (Concede openly; the third state is OLD.)
- **INTUITIONISM** — Brouwer; Heyting; truth-by-construction. [SEP: Intuitionism]
- **GODEL** — Gödel (1931); incompleteness; the second theorem (no self-certified consistency).
- **BRANDOM** — Brandom, *Making It Explicit* (1994); Sellars, "Empiricism and the Philosophy of Mind" (1956); warrant in inferential relations, the space of reasons.
- **EINSTEIN-1921** — Einstein, "Geometrie und Erfahrung" / "Geometry and Experience" (1921); "as far as the laws of mathematics refer to reality, they are not certain; and as far as they are certain, they do not refer to reality."
- **DAVIDSON** — Davidson, "Rational Animals" (1982) and "Three Varieties of Knowledge" (1991); triangulation, objectivity needs two minds and a world.
- **NAGEL-VFN** — Nagel, *The View from Nowhere* (1986); objectivity as the unoccupiable limit. (Cite for the LIMIT, not for consensus.)
- **PAULI** — Pauli, "not even wrong" (attributed); the floor below false.
- **WOIT** — Woit, *Not Even Wrong* (2006); string-theory testability.
- **ELEPHANT** — the blind men and the elephant (parable; Buddhist *Udāna*; Saxe 1872).
- **WANG-NARS** — Pei Wang, *Non-Axiomatic Logic* (NARS); experience-grounded graded truth.
- **OPENCOG** — Goertzel et al., OpenCog AtomSpace / PLN.
- **GROTH-NANOPUB** — Groth, Gibson & Velterop, "The Anatomy of a Nanopublication" (2010).
- **TRAXIA** — Traxia (arXiv:2606.08256, 2026); concurrent, two days after /truth-is-buildable.
- **MARCHAL** — Marchal et al. (2026), DeepMind, artificial epistemic agents / verification crisis (arXiv:2603.02960).
- **COVER-THOMAS** — Cover & Thomas, *Elements of Information Theory* (1991); the data-processing inequality. (Only if the DPI is actually invoked; standard source, NOT the Natural Framework.)

### Per-node map (node → load-bearing keys · companions)

- **F1** KANT-CPR · —
- **F2** KANT-CPR + own (argued) · —
- **F3** own (definition; phenomenal-truth in the JAMES-PRAG/DEWEY-QC lineage) · truth-is-buildable
- **F4** own (argued) — **render note (delta razor / #3):** concede this is Peirce's Secondness (PEIRCE), the brute outward clash; the delta is the machine version, one bit, replayable · —
- **F5** own (declared) · —
- **F6** PEIRCE-CLEAR + MISAK (the hedge) · truth-is-buildable
- **F6a** RAMSEY-TP + REGULARITY (the [0,1) ceiling) + PEIRCE-CLEAR · belief-is-the-edge-of-knowing
- **F6b** own (argued; Newton / Mercury-perihelion / GR / quantum) · —
- **F6c** INTUITIONISM (+ GODEL, owned by F7, not re-cited here) · truth-is-buildable, truly-untrue
- **F7** EINSTEIN-1921 + GODEL · —
- **F7a** EINSTEIN-1921 + WOIT + PAULI · auditing-deepswe (the dual)
- **A1** RAMSEY-TP · belief-is-the-edge-of-knowing
- **A2** own (argued) · belief-is-the-edge-of-knowing
- **A3** JAMES-PRAG + DEWEY-QC · belief-is-the-edge-of-knowing
- **A4** PEIRCE-FIX · —
- **A5** POPPER + VERIFICATIONISM (lean conceded) · truth-is-buildable
- **A6** RAMSEY-TP (degrees) · evidence-has-a-trajectory
- **A7** own (argued; the N-atoms case) · truth-is-buildable
- **E1** BRANDOM · truth-is-buildable
- **E2** POPPER (the falsification channel) · truth-is-buildable
- **E3** own (definition; the build-graph mapping) · truth-is-buildable
- **E4** own (argued; scripture vs benchmark) · truth-is-buildable, auditing-deepswe
- **E5** own (argued; the relativism guardrail) · truth-is-buildable
- **C1** own (argued; operationalization) · —
- **C1a** PEIRCE-CLEAR (community of inquiry) · —
- **C1b** DAVIDSON + NAGEL-VFN (limit only) + ELEPHANT — **render note (#4):** the "independent projections constrain the object" step is the paper's OWN (robustness), NOT Davidson/Nagel; cite them narrow · —
- **C1c** own (argued; reproducibility as composable warrant) · —
- **C1d** PEIRCE-CLEAR + own (protocol-not-trust) · science-on-trial, sour-red-tapes
- **C1e** own (nullius in verba; trust-vs-accountability) · science-on-trial, complementations, sour-red-tapes
- **C1f** PEIRCE-FIX (fallibilism) + own (nullius in verba) · science-on-trial, belief-is-the-edge-of-knowing
- **C2** LUKASIEWICZ (concede) + own (the warrant-ledger move) · truth-is-buildable
- **C2a** GODEL + Turing (halting) + Presburger · truly-untrue
- **C3** PAULI + POPPER (risk) + own (the dignity ordering) · truth-is-buildable, sour-red-tapes
- **C4** own (declared) · —
- **C5** own (declared + argued; the delta razor) · —
- **R1–R12** each carries its own ref in-node (PEIRCE/JAMES/DEWEY/RAMSEY; KANT; POPPER; INTUITIONISM/LUKASIEWICZ; BRANDOM; VERIFICATIONISM; WANG-NARS; OPENCOG; TRAXIA; GROTH-NANOPUB; MARCHAL) · —
- **S1** own (the three modes) · modes-of-reason, abduction
- **S2** own (math's one-way migrations; Fermat; pre-empt Kempe four-color) · —
- **S3** own (verb-scoping) · type-iii-error, wrong-questions, wrong-again
- **S4, S5** own (declared / meta) · —
- **FW1, FW2, FW3** own (declared; all open speculative edges) · — (FW2 rehomes the scope-guarded vision; FW3 = the economic/search-complexity argument, honestly typed)
- **FW4** own (declared, open edge) · /compress-and-unfold (self-link) — load-bearing on STANDARD sources (DPI Cover & Thomas; Shannon; catamorphism/anamorphism duality), NF kept out
