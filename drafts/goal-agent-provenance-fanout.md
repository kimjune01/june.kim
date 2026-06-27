# Fan-out: Provenance of goal-based agents (purpose frames inquiry)

**Question.** Trace the lineage and the multiple historical attempts to describe goal-directed
action-and-inquiry loops — the idea that *purpose frames perception and action* (what to observe,
what to perturb). Converge on the strongest through-line. Extend toward June's contribution:
purpose as the cold-start that frames the variable basis; fractal goal/action trees; reasoning as
instrumental-to-action over a frame-compounding horizon.

**Blog anchors to connect:** tempus-doxa-praxis / "You Cannot Ring a Semiring" (agency = attention
that can act; doxa serves praxis), methodeutics textbook (diff/bi/tri-abduction; economy of
research; cold-start frame problem), history-is-a-lattice, truth-is-buildable, belief-is-the-edge.

---

## Cycle 1 — Diverge (k=4)

- H1: Cybernetic teleology (Rosenblueth–Wiener–Bigelow 1943, Wiener, Ashby, Powers PCT, control theory)
- H2: Pragmatist / biological inquiry (Peirce, Dewey, von Uexküll Umwelt)
- H3: Computational agent architectures (TOTE, Newell–Simon GPS, BDI, Russell–Norvig, Sutton–Barto RL, Friston)
- H4: OODA / decision-under-one-way-time (Boyd) and its bearing on tempus-doxa-praxis

---

### H3: Computational agent architectures — the mechanized goal hierarchy (opus, alive)

**Verdict:** This cluster contains the strongest *formal* statement of "purpose frames the basis"
(RL state abstraction) and the cleanest *structural* ancestor of June's fractal (TOTE), but every
member bottoms out by *assuming* the variable basis / generative model rather than deriving it.
The cold-start is universally pushed to the modeler.

**Claims:**

- **TOTE (Miller, Galanter & Pribram, *Plans and the Structure of Behavior*, 1960) is the bridge.**
  They replace the reflex arc with the **Test–Operate–Test–Exit** unit: test the present state
  against a goal-image, operate to reduce the incongruity, re-test, exit when congruent. This is
  the cybernetic negative-feedback loop (they cite Wiener/Ashby explicitly) imported into
  psychology as the atom of behavior. Crucially the **Plan is a *hierarchy* of TOTE units** — a
  high-level test ("hammer the nail flush") whose Operate phase *is* a lower-level TOTE
  ("lift–strike"). This is precisely June's fractal goal/action tree, stated in 1960. And the
  **Test sets what is observed**: the unit only measures the incongruity its goal defines. So
  "purpose frames the variable basis" is already implicit here — the test predicate *is* the
  basis. What MGP lack: any account of where the goal-image (hence the test, hence the basis)
  comes from. It is supplied by the experimenter. [H3, opus]

- **Newell & Simon — means-ends analysis / GPS (1959), problem spaces (*Human Problem Solving*,
  1972).** MEA computes the *difference* between current and goal state and selects an operator
  to reduce it — the diff primitive, but goal-relative: the difference table only ranges over
  differences the problem representation encodes. Newell-Simon are explicit that **the problem
  space (the representation) is given prior to search** and that choosing it is the hard,
  unformalized part (the "problem of representation"). Direct corroboration of codex's verdict:
  search is mechanized, framing is not. [H3, opus]

- **Russell & Norvig (AIMA) taxonomy:** simple-reflex → model-based → goal-based → utility-based.
  The textbook treats goals/utility as governing **action selection**, not perception. The
  percept-to-state function (the basis) is an architectural given in all four rungs. **The gap is
  exactly here**: AIMA never makes goals reach back to *frame what the agent senses*; that arrow
  is the one June is drawing. [H3, opus]

- **RL state abstraction + the reward hypothesis — the strongest formal "purpose frames basis."**
  Sutton's reward hypothesis (goals = maximization of expected cumulative scalar reward) plus the
  state-abstraction theory (**Li, Walsh & Littman 2006**, "Towards a Unified Theory of State
  Abstraction for MDPs"): the right representation is the *coarsest partition that preserves the
  optimal policy/value* (model-irrelevance / bisimulation, Givan-Dean-Greig 2003; π*- and
  Q*-irrelevance). This is "basis relative to reward" as a theorem — distinctions that don't change
  optimal action are *provably* discardable. But the abstraction is defined **relative to a fixed
  reward and a fixed ground-state space**; it compresses a given basis, it doesn't invent one.
  Cold-start unsolved. [H3, opus]

- **Active inference / expected free energy (Friston 2010–2017).** Action and perception minimize
  *one* quantity (variational free energy); planning minimizes *expected* free energy, whose
  epistemic term is information gain (Lindley/Bayesian-experimental-design rediscovered) and whose
  pragmatic term is goal-attainment. This is the **unification June gestured at**: "what to
  perceive" and "what to do" fall out of the same optimization. **But** the generative model — the
  state factors, the variable basis — is *assumed given*; "structure learning" over it is an open
  add-on, not the core. Honest verdict: active inference unifies observe+perturb *given* a basis;
  it does not cold-start the basis. [H3, opus]

**Through-line of this cluster:** every architecture mechanizes the loop (test/diff → operate →
re-test) and several make it explicitly hierarchical (TOTE) or goal-relative in representation
(RL), but **all of them take the variable basis / generative model / problem space as exogenous
input.** The cold-start is the field's shared blind spot, not a gap specific to methodeutics.

**Tie to June:** TOTE = the fractal goal/action tree, 1960 vintage, but frozen (no growth of the
tree, no origin of the top test). RL state-abstraction = the rigorous form of "purpose supplies the
basis," but only as *compression* of a given basis, never *invention*. June's move — make the goal
*generate* the basis, make the tree *grow*, and fund frame-building reasoning the current goal
won't pay for (curiosity as long-horizon instrumentality) — is exactly the invention step every
member of this cluster brackets out. The reward hypothesis is also where reasoning-as-instrumental
lives natively: in RL all cognition is justified by return; June's frame-compounding horizon is the
amendment that lets representation-building reasoning be instrumental over a longer arc than the
current reward.

**Open questions for human:** (a) Is bisimulation-style state abstraction the right formal skeleton
to *cite* for June's claim, or does it mislead by being compression-only? (b) Hierarchical RL
(options, Sutton-Precup-Singh 1999; feudal/MAXQ Dietterich 2000) is the RL cousin of TOTE's nesting
— worth folding into the fractal thread. (c) Predictive-coding "the goal sets the prior that shapes
the percept" is the active-inference sentence closest to June; does it earn a place over RL?

**HANDOFF CLAIM:** The computational-agent tradition independently re-derived June's two core
structures — the *nested* goal/action loop (TOTE, 1960) and *purpose-relative representation* (RL
state abstraction, formally optimal-policy-preserving compression) — but every variant takes the
variable basis as exogenous, so June's contribution is precisely the unbracketed step: letting the
goal *invent and grow* the basis rather than only *compress a given one*.

---

### H1: Cybernetic teleology and control (opus, alive)

**Verdict:** The first rigorous account that purpose = negative feedback, and that the *controlled
(perceived) variable is the frame*. Powers' hierarchical PCT already encodes a fractal goal-tree;
the stack bottoms out in intrinsic/essential variables given by viability — cold-start relocated to
embodiment, never derived. Converges with H3: same loop, same blind spot.

**Claims:**
- Rosenblueth, Wiener & Bigelow 1943 ("Behavior, Purpose and Teleology," *Phil. Sci.* 10:18–24) define *teleological behavior* as "behavior controlled by negative feed-back." Rehabilitated purpose as mechanism, no vitalism. Bearing on the basis: the loop senses only the goal-relevant gap (the *error signal*); the goal selects what is sensed. [H1, opus]
- Wiener, *Cybernetics* (1948), subtitle "Control and Communication in the Animal and the Machine" — feedback/teleology generalized across machine and organism, information as common currency. Deep ancestor: Maxwell, "On Governors" (1868). [H1, opus]
- Ashby, *Design for a Brain* (1952) + the Homeostat: *ultrastability* — reconfigure to keep **essential variables** within survival bounds. "Essential variables" is cybernetics' nearest thing to a variable basis, and it is supplied by *viability*. [H1, opus]
- Ashby, *Introduction to Cybernetics* (1956), **Law of Requisite Variety** ("only variety can destroy variety"): a regulator needs at least as much variety as the disturbances it counters. About regulation *given* a basis — presupposes which variable is essential and which disturbances matter. Capacity, not cold-start. [H1, opus]
- Powers, *Behavior: The Control of Perception* (1973) — **PCT**, the load-bearing inversion: organisms control their *perceptions*, not behavior or the environment. "Behavior is the control of perception." The controlled perceptual signal **is** the frame: what the agent observes is exactly what it holds at reference. [H1, opus]
- **Hierarchical PCT** = the fractal goal-tree in cybernetic dress: a higher loop's *output sets the reference of the loop below*. Each level's set-point frames the basis beneath it. June's fractal action tree, 1973. Convergent with TOTE (H3, 1960) — two independent statements of the same nesting. [H1, opus]
- **Where it bottoms out:** reference signals are *given* — by design in engineering, by genes/viability in Ashby's essential variables and Powers' intrinsic reference levels. The one place a *new* basis is generated is Powers' **reorganization** (random restructuring when intrinsic error stays high) — a candidate cold-start *mechanism* rather than a punt, though it is undirected (closer to evolutionary search than to abductive framing). [H1, opus]

**Tie to June:** PCT "control of perception" = Semiring's "agency is attention that can act" (the
controlled perception is where the beam lands). Hierarchical references = the fractal goal/action
tree; set-points handed down = purpose framing the basis at each level; bottoming out at intrinsic
references = "terminal drives the agent didn't choose." One-way time: feedback correction runs
forward and cannot be un-corrected (tempus). Methodeutics: the controlled variable is figure
selected by the reference; requisite variety = how fine the figure/ground partition must be to
track the disturbance.

**Open questions:** Is "essential variable = viability" a real answer to the cold-start or the same
embodiment punt? Powers' *reorganization* is the strongest cold-start candidate in the whole
fan-out — undirected basis-generation driven by intrinsic error — worth pulling forward in the
extend cycle and contrasting with June's *directed* (goal-framed) basis invention.

**HANDOFF CLAIM:** Cybernetics is the first mechanized account that purpose is negative feedback and
that the controlled perception *is* the frame; Powers' hierarchical PCT already encodes the fractal
goal-tree (each level's set-point frames the basis below) and bottoms out in viability-given
intrinsic references — so, like H3, it supplies the structure and brackets the origin, with
*reorganization* as the lone (undirected) gesture at where a new basis comes from.

---

### H2: Pragmatist / biological inquiry — purpose frames perception, organism-relative (opus, alive)

**Verdict:** The closest *ancestor* to June's framing and the one most uncited by the cybernetics/AI
agent literature. Dewey (1896) and von Uexküll (1909/1934) state "purpose frames the variable basis"
a half-century before TOTE/PCT, in psychology and biology rather than control theory. Peirce supplies
the economy-of-research + musement tension June is resolving. Bottoms out in the organism's
constitution (drives/Bauplan) — same cold-start floor, relocated to evolution.

**Claims:**
- **Dewey, "The Reflex Arc Concept in Psychology" (1896, *Psychological Review* 3:357–370) — the gem.**
  Dewey dissolves the stimulus→response arc: the "stimulus" is not given prior to the act. In the
  child-and-candle example, the seeing *is already* a reaching-and-grasping; the act of looking
  determines what becomes the stimulus. Sensation, idea, and movement are phases of one coordinated
  *circuit*, not a linear chain. This is "the activity selects what counts as a stimulus" = purpose
  frames the variable basis, stated in 1896. The percept is constituted by the ongoing goal-directed
  coordination, not received before it. [H2, opus]
- **Dewey, *Logic: The Theory of Inquiry* (1938).** Inquiry = "the controlled or directed
  transformation of an indeterminate situation into one that is so determinate... as to convert the
  elements of the original situation into a unified whole." Inquiry is driven by a *felt need* (an
  indeterminate, troubled situation), and the "problem" is not given — *framing* the problem is the
  first and hardest act of inquiry ("a problem well put is half-solved"). Direct pragmatist statement
  that the frame precedes and conditions the contrast. The methodeutics cold-start in Dewey's idiom. [H2, opus]
- **von Uexküll, *Umwelt und Innenwelt der Tiere* (1909); "A Stroll Through the Worlds of Animals and
  Men" (1934).** The *Umwelt* is the organism-specific perceptual world carved out by its needs; the
  *Funktionskreis* (functional cycle) couples perception (Merkwelt) and action (Wirkwelt) so that the
  animal perceives only the cues its functional circle makes relevant. The **tick** perceives just
  three signals — butyric acid (mammal sweat), 37°C warmth, hairless skin texture — out of the entire
  electromagnetic and chemical world. The variable basis *is* the functional cycle. This is the
  biological statement of relevance-realization and of "the cold-start is solved by embodiment +
  purpose." [H2, opus]
- **Peirce.** Pragmaticism: the meaning of a concept is its conceivable practical effects (1878,
  "How to Make Our Ideas Clear") — meaning is action-relative. Economy of research (1879) budgets
  inquiry by value-to-action. But *musement* (1908, "A Neglected Argument") is protected as free,
  purposeless play — the apparent exception. The tension June resolves: musement is **long-horizon
  instrumentality** (frame-compounding), not an exception to "reasoning serves action." [H2, opus]
- **Where it bottoms out:** Dewey grounds the basis in the organism's *needs* and the troubled
  situation; Uexküll in the species *Bauplan*. Those needs/plans are given by biology/evolution.
  Same cold-start floor, relocated to the organism's constitution — but note this is *less* of a punt
  than cybernetics' "reference signal," because the functional cycle gives a concrete mechanism for
  how purpose carves perception (the Merkwelt/Wirkwelt coupling). [H2, opus]

**Tie to June:** Uexküll's Funktionskreis = the methodeutics loop with the frame supplied by purpose
(Merkwelt = what to observe, Wirkwelt = what to perturb, coupled by the organism's drive). Dewey's
"the act selects the stimulus" = Semiring's "the pointing is you" (attention-that-acts constitutes
its own object). Peirce's musement-vs-economy = June's frame-compounding horizon. This cluster is the
*conceptual* home of June's thesis; the cybernetic (H1) and computational (H3) clusters are the
*mechanized* re-derivations that lost the pragmatist origin.

**Open questions:** (a) Is the right citation spine for June's piece *pragmatist* (Dewey/Uexküll/Peirce)
with cybernetics/RL as the mechanization, or the reverse? (b) Uexküll → Merleau-Ponty / enactivism
(Varela-Thompson-Rosch, *The Embodied Mind*, 1991) is the modern continuation — worth a line as the
bridge from Umwelt to relevance-realization (Vervaeke).

**HANDOFF CLAIM:** The pragmatist/biological line (Dewey 1896 "the act selects the stimulus";
von Uexküll's Funktionskreis carving the Umwelt; Peirce's action-relative meaning) is the earliest
and most direct statement that purpose frames the variable basis — the conceptual ancestor that
cybernetics and AI later re-mechanized and stripped of its origin, and the home of the
musement-as-long-horizon-instrumentality tension June resolves.

---

### H4: OODA and decision under one-way time (Boyd) (opus, alive)

**Verdict:** Boyd states "orientation frames observation" more bluntly than anyone — Orient is not a
stage but the controller, with an explicit feedback arrow onto Observe — and ties it to acting under
irreversible time (tempo). The strongest *temporal* statement of June's thesis, and the one most
isolated from the abduction/cybernetics literature. Bottoms out the same way (orientation = genetic
+ cultural + experiential heritage), but uniquely treats *re-framing* as a continuous act
(Destruction & Creation), which is the closest prior to "frames compound / musement as reframing."

**Claims:**
- **Boyd, "The Essence of Winning and Losing" (1995, briefing slides) — the real OODA diagram.**
  The popular "loop" (Observe→Orient→Decide→Act, round and round) is a flattening. Boyd's own sketch
  makes **Orient the large central box with feedforward AND feedback arrows reaching back to Observe,
  Decide, and Act.** Orientation is "shaped by genetic heritage, cultural traditions, previous
  experiences, and unfolding circumstances," and it runs "analysis & synthesis" continuously.
  Boyd's text: orientation "shapes the way we observe, the way we decide, the way we act." That
  sentence is *purpose/frame governs the variable basis*, stated in 1995 in a military idiom and
  almost never cited by cognitive science or AI. Observation is not raw intake; it is already
  oriented. [H4, opus]
- **Boyd, "Destruction and Creation" (1976, essay).** Orientation is built by two opposed operations:
  *analysis* (break existing mental models into parts) and *synthesis* (recombine the parts into a
  new model). Boyd argues from **Gödel** (no model is complete from within), **Heisenberg** (observing
  perturbs), and the **2nd law of thermodynamics** (a closed model's match to reality decays) that
  you *must* periodically destroy your frame and build a new one — a model held too long loses
  fidelity. This is *re-framing as an ongoing, forced act*, not a one-time cold-start. It is the
  closest prior in the whole fan-out to June's "frames compound" and "musement = reframing": Boyd
  gives a thermodynamic *reason* the agent must keep building new bases rather than only refining the
  current one. [H4, opus]
- **Tempo / one-way time.** OODA's strategic payload: get inside the opponent's decision cycle — act
  faster than the adversary (or the world) can re-resolve, so your action lands before their
  orientation updates. This is decision under *irreversible* time: you must commit to a branch before
  it resolves, and speed of re-orientation is the weapon. Direct hit on tempus-doxa-praxis: agency as
  the push-forward dual to a future you cannot read (Semiring); Boyd is the operational/military
  statement of "you act before the branch resolves, and the acting is what makes it real." Boyd even
  prized *implicit* guidance (acting without explicit deliberation) to shorten the loop — doxa over
  episteme, the bet over the proof, because the proof arrives too late. [H4, opus]
- **Where it bottoms out:** Boyd does *not* derive orientation; it is the accumulated residue of
  genetic + cultural + experiential history. Same cold-start floor as H1/H2/H3, relocated to
  *personal/cultural history*. BUT Destruction & Creation is a partial answer to the *update* problem
  (how a new basis is forged from an old one under entropy pressure) that the other clusters lack —
  it is a mechanism for *re*-framing, even if not for the first frame. [H4, opus]

**Tie to June:** Orient→Observe feedback = "purpose frames the variable basis." Destruction & Creation
= the frame-compounding / reorganization mechanism (converges with Powers' *reorganization*, H1 —
two independent accounts of forced re-framing). Tempo/one-way-time = Semiring's whole thesis in
operational dress. Boyd is the bridge between the methodeutics cold-start and tempus-doxa-praxis: he
puts re-framing *and* irreversible-time-action in one loop.

**Open questions:** (a) Boyd's slides are primary but informal; for citation, pair with Osinga,
*Science, Strategy and War: The Strategic Theory of John Boyd* (2007), the rigorous secondary source
that traces Boyd's Gödel/Polanyi/cybernetics reading. (b) Boyd read Polanyi (*tacit knowing*) and
Kuhn (paradigm shift) — both reinforce "the frame precedes and conditions observation"; worth a line.

**HANDOFF CLAIM:** Boyd's OODA — read correctly, with Orient as the framing controller that feeds back
onto Observe, and Destruction & Creation as a thermodynamically-forced re-framing engine — is the
sharpest prior statement that *orientation frames the variable basis* and that re-framing is a
continuous act under irreversible time, making Boyd the missing bridge between the methodeutics
cold-start and tempus-doxa-praxis.

---

### H2: Pragmatist / biological inquiry — Dewey, von Uexküll, Peirce (opus, alive)

**Verdict:** This cluster holds the *cleanest pre-cybernetic statement* that purpose constitutes
the perceptual basis (Dewey 1896; von Uexküll's Umwelt). It is the philosophical/biological root
the engineering traditions (H1, H3) later mechanized. All three bottom out by grounding the frame
in something *supplied* — the ongoing act, the organism's biological function, instinct/musement —
matching codex's "bias/embodiment/prior ontology."

**Claims:**

- **Dewey, "The Reflex Arc Concept in Psychology" (1896, *Psychological Review*) is the sharpest
  historical statement of "praxis frames doxa."** Dewey attacks the stimulus→response sequence: the
  reflex arc is not a sequence but a *circuit*. The "stimulus" is **not given prior to the
  response** — what counts as stimulus is *constituted by the act in progress*. His example: the
  child sees the bright flame, reaches (seeing-for-grasping), gets burned, withdraws. The
  light becomes "stimulus-to-withdrawal" only *through* the act. Exact: "we begin not with a
  sensory stimulus, but with a sensori-motor coordination"; the response is not *to* the stimulus
  but *into* it. This is "purpose frames the variable basis" stated in 1896 — the act selects what
  registers as a stimulus. The direct ancestor of enactivism (Varela–Thompson–Rosch, *The Embodied
  Mind*, 1991: perception is *for* action). [H2, opus]

- **Von Uexküll's Umwelt + Funktionskreis (1909; *Streifzüge durch die Umwelten von Tieren und
  Menschen*, 1934) = "the variable basis is supplied by what the creature is FOR."** The
  *Funktionskreis* (functional cycle) binds receptor-world (*Merkwelt*) and effector-world
  (*Wirkwelt*) into a closed loop through the organism's needs; a perceptual cue (*Merkmal*) exists
  for the animal only if its action-cycle assigns it *functional tone* (*Bedeutung*). **The tick**:
  its entire Umwelt is ~three cues — butyric acid (mammalian sweat) → drop; 37°C warmth → seek
  skin; hairless texture → bore and feed. The whole forest is *absent* for the tick; only what its
  feeding/reproduction cycle marks exists perceptually. The basis is carved by function, not read
  off the world. This is *exactly* June's "the eye builds the depth a grabbing creature needs"
  (tempus-doxa-praxis), with the biology made explicit. [H2, opus]

- **Peirce has the economy but punts the frame.** *Economy of research* (1879) governs **what to
  TEST** — hypothesis selection by cost/utility, reasoning subordinate to economy (this is the part
  methodeutics ch7 already formalizes). *Pragmaticism* (1878, "How to Make Our Ideas Clear":
  meaning = conceivable practical effects) makes meaning action-relative *in principle*. But Peirce
  never operationalizes "purpose carves the perceptual basis." The **origin** of abductive
  hypotheses he hands to *instinct* / *il lume naturale* and, late, to **musement** (1908, "A
  Neglected Argument"). So Peirce leaves *what to OBSERVE* / the frame to musement — the precise
  gap June fills. Dewey and von Uexküll do the work Peirce declines. [H2, opus]

**Where it bottoms out (cold-start):** Dewey grounds the frame in the ongoing *act* and, later, in
the *indeterminate situation*'s pre-cognitive "pervasive quality" (*Logic: The Theory of Inquiry*,
1938 — inquiry = controlled transformation of an indeterminate situation into a determinate one).
Von Uexküll grounds it in the species' biological *Bauplan*/needs (given, not derived). Peirce in
instinct/musement. All three: **supplied**, not bootstrapped — the same termination codex named.

**Tie to June:** This cluster is the philosophical root of June's move. Dewey 1896 = the
pre-cybernetic "praxis frames doxa"; von Uexküll = the biology of "doxa serves praxis." Methodeutics'
missing *Chapter 0* (purpose supplies the frame) has its best historical home here: the pragmatist
*indeterminate situation* and the *functional tone* are prior names for "purpose selects the
variable basis." June's fractal goal/action tree is Dewey's *nested coordinations* (acts within
acts) made structural; June's contribution over Peirce is to replace **musement** with **the goal
stack** as the explicit frame-supplier — closing the loop Peirce left open.

**Open questions for human:** (a) Enactivism / 4E cognition (Varela 1991; Noë 2004; Di Paolo) is the
living heir of Dewey+von Uexküll and the closest contemporary ally — cite it as the modern bridge to
the engineering threads? (b) Dewey's "indeterminate situation" vs. June's "goal" — are they the same
frame-supplier, or is the *situation* pre-purposive (the quality comes before the goal)? This is a
real fork worth attending.

**HANDOFF CLAIM:** Dewey (1896) and von Uexküll (1934) state, a half-century before cybernetics,
that the act/organism-function *constitutes* the perceptual basis rather than receiving it — the
philosophical root of "purpose frames the variable basis" — while Peirce supplies only the *economy*
of testing and leaves the *origin of the frame* to musement, which is exactly the slot June fills
with the goal stack.

---

## Cycle 1 — Converge (codex adversarial) + Prune

**Codex verdict (gpt-5.5):** through-line real as a *relevance/framing lineage*, false if pushed to
architectural identity. Most of June's "contribution" is synthesis/relabeling. One kernel survives as
candidate-novel. Several spine lineages are missing and their absence is fatal.

**PRUNED (died or demoted):**
- **"Same loop across all four"** — DEMOTED to "analogous, not identical." Cybernetics = controlled
  variables/feedback (no semantic purpose); Dewey/Uexküll = organism-situation transaction (no
  goal-stack architecture); RL = reward-relative *optimization*; Friston = purpose collapses into
  inference (priors), a different metaphysics; Boyd = adversarial epistemology about *tempo/deception*,
  not basis construction. Keep the analogy, drop the identity claim. [codex]
- **"Every tradition brackets the cold-start"** — TOO STRONG, replaced by: *nobody gets basis
  invention for free; all mechanisms presuppose a prior search space, bias, body, grammar,
  sensorimotor envelope, or viability constraint.* And there ARE partial basis-INVENTION mechanisms
  that must be acknowledged, not lumped with the compressors: constructive induction / predicate
  invention (ILP), Lenat's **AM/Eurisko**, genetic programming / program synthesis, **Schmidhuber**
  (PowerPlay, Gödel machine), developmental robotics (**Oudeyer–Kaplan** intrinsic motivation),
  active-inference *structure learning*, causal representation learning, open-ended evolution. [codex]
- **June-claim (1) "purpose frames the variable basis"** — NOT NOVEL. Dewey, Uexküll, Gibson, PCT,
  pragmatism, enactivism, relevance realization, active inference, affordances, RL abstraction. The
  Peircean/methodeutic *packaging* is distinctive; the content is known. [codex]
- **June-claim (2) "fractal goal/action tree"** — NOT NOVEL. Hierarchical control, TOTE, hierarchical
  RL/options, ACT-R/SOAR subgoaling, predictive-processing hierarchies, PCT. Novel *only if* the
  diff-primitive does real cross-level work that these don't. [codex]
- **June-claim (4) "cold-start dissolved (always already a goal)"** — NOT NOVEL philosophically.
  Pragmatism, Heidegger, Merleau-Ponty, Gadamer, enactivism, "no view from nowhere." Clean synthesis,
  not a discovery. [codex]

**SURVIVOR (candidate-novel, needs formal teeth):**
- **June-claim (3) FRAME-COMPOUNDING instrumentality.** The promising kernel: *curiosity/musement is
  valuable because it expands the agent's future relevance-bases and action-bases — not merely because
  it reduces uncertainty (Lindley/active-inference epistemic value) or improves compression
  (Schmidhuber).* This is the one place June is adjacent-to but not identical-with the known work.
  Schmidhuber rewards compression *progress*; active inference rewards *information gain*; Oudeyer
  rewards *learning progress*. June's claim is about **basis expansion** — option value over the space
  of future frames, not over the current model's parameters. If formalized (a value-of-a-new-basis
  that the current goal won't pay for but a distribution of future goals will), that's a real
  contribution. Without teeth, it's a reframing of intrinsic motivation. [codex, survivor]

**WHAT BREAKS THE THESIS (objections the essay must absorb):**
1. **Goal conflict** — multiple incompatible goals don't select *one* basis; they induce a *contest*
   among bases. (This is June's own "where the fan gets interesting" — the terminal-drive multiplicity.)
2. **Bottom-up capture** — startle, pain, salience, affect, novelty, raw sensory organization hijack
   goal-framing. Perception is not *only* top-down. Purpose frames *much*, not *all*.
3. **Unfalsifiability risk** — "always already has a goal" + goals being inferred/socially-installed/
   retrospectively-rationalized can make the thesis unfalsifiable. Needs a falsification condition.
4. **Adversarial inversion** — deception targets the relevance filter, so "purpose frames perception"
   becomes "purpose *blinds* perception" (Boyd's whole point). The frame is an attack surface.
5. **The generator's hypothesis space** — "the goal generates the basis" still owes an account of the
   generator's space. Relocates the cold-start; doesn't abolish it (codex's central correction).

**MISSING SPINE (fatal omissions to fold in):** Gibson **affordances** (mandatory — action-relative
perception, no representation-first framing); **enactivism/autopoiesis** (Maturana, Varela, Thompson
& Rosch *The Embodied Mind* 1991 — belongs in the spine, not as a worry); Heidegger/Merleau-Ponty
(readiness-to-hand, already-in-a-world); the **frame problem / relevance realization** spine (Fodor,
Dennett, Shanahan, Vervaeke — this IS the problem); **Piaget** constructivism (assimilation/
accommodation = basis change, pre-AI); predictive processing (Clark, Hohwy, Rao-Ballard — Friston
alone too narrow); social scaffolding (Vygotsky, Wittgenstein, Hutchins — purpose is often installed,
not endogenous).

**Verdict (codex):** publishable as a *synthesis* only if it (a) stops claiming discovery,
(b) explicitly positions against relevance realization / enactivism / affordances / constructive
induction, and (c) adds either a crisp formal primitive (the frame-compounding value) OR a
historical-philosophical payoff those lineages don't already give. As a blog essay it's strong as-is;
as a contribution it lives or dies on claim (3) getting teeth.

## Convergent findings (cross-cluster, stronger for it)

- **Forced re-framing under entropy** appears TWICE independently: Powers' *reorganization* (H1) and
  Boyd's *Destruction & Creation* (H4). Two traditions, same idea — a frame decays and must be rebuilt.
  This is the real historical anchor for June's "frames compound / musement = reframing." Strongest
  convergence in the fan-out.
- **The nested loop** appears in H1 (PCT 1973), H3 (TOTE 1960, hierarchical RL) — independent
  re-derivations of the fractal goal tree. June's fractal claim is corroborated as a *recurring
  structure*, which also means it is not novel.
- **The cold-start floor** is unanimous across H1–H4: viability/genes (H1), drives/Bauplan (H2),
  reward/model/problem-space (H3), genetic+cultural+experiential heritage (H4). The agreement is the
  finding: the field has a shared blind spot, and it bottoms out in something *given*.
