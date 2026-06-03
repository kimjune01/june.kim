# Supervisor experiment — notes for sharpening the trilogy

Running log of findings from building + running the `supervise(spec)` higher-order
function against sweep's real classifiers (switch, remit, compose) and a public
contributor corpus (ljharb). Each entry flags what it implies for
Encoding Expertise / Supervisor / Asymptote Learning.

---

## THESIS — the finding to produce

**You can assemble an expert-level RL-classification policy with ZERO weight
training, and learn it ONLINE.** Same inputs a fine-tuning pipeline would consume
(labeled (state, action) samples from a frozen corpus), but no gradient step
anywhere. Stated the way the operator put it: *supplement an expert system and
resolve its residue via LLM calls.* The expert system is PRIMARY; the LLM occupies
only the residual cell where the rules bottom out.

The construct is two ingredients, neither trained:
1. an EXPERT SYSTEM grown from the frozen corpus via the encoding loop
   (preconditions, cli-tools, cache-keys, label-riding rules — #19), and
2. a general, off-the-shelf LLM resolving the residue (never fine-tuned on the
   task), plus distribution-matching for the social tail (#22).

The corpus is used for replay-gating and marginal-matching, NEVER for gradient
descent. "Training" is replaced by "encoding" (code accretion) + "a stock model
doing the residue." The output is a git-blameable program wrapping a stock model:
auditable, rollback-able, per-artifact adjudicable. This is the RL/SFT table's
promise, demonstrated rather than asserted — and sharper: not "different substrate
for the same learning," but NO LEARNING SUBSTRATE AT ALL for the encodable part,
and a general model for the rest. The framing inverts the default: not "an LLM
with tools" but "an expert system whose bottom-out case is an LLM call," with the
expert system subsuming the residue over passes (the asymptote) so the LLM's share
shrinks toward the irreducibly-fuzzy.

**CAVEAT (operator: "but all that is IF it works").** Every property above is a
property of the METHOD, not yet of the RESULT. Demonstrated: the procedure runs
(laptop, frozen corpus, four-case switch, blinded replay, catches overgeneralization,
proposes auditable artifacts, online, no training). NOT demonstrated: that the encoded
policy is GOOD. We are propose-only — nothing applied, no outcomes measured. Crucially,
the replay gate checks FAITHFULNESS (does the rule reproduce past actions?), NOT
GOODNESS (does the action produce a good outcome?). A faithfully-cloned rule can still
be a bad policy — especially when the expert's context != ours. Concrete instance:
respond-nikic's 47x "approved->close" proposal mislabeled the action as merge_pr, but
LLVM PRs are CLOSED (landing is via the monorepo), not merged; applied naively it would
try to merge PRs that should be closed-after-landing. The gate didn't catch it because
closing WAS the faithful action — the interpretation drifted. Efficacy requires closing
the loop: apply a proposal, run it, measure via the regret/outcome channel whether
decisions improve. We built that channel (#1-2) but have not run it in anger. The honest
status: the machine LEARNS a policy cheaply/online/auditably; whether the learned policy
is GOOD is a separate, unvalidated claim.

Evidence map (the 25 findings are the support):
- the encodable rind is real and grows: #5, #12, #19, switch/remit/nikic-actions.
- the residue is genuine and stays in the stock model: #17, respond-ljharb (#24).
- the boundary is principled and tunable: #20 (closed action space), #21 (decline
  the tail), #22 (match its marginal), #23 (judgment ⊆ behavior, coverage not
  competence), #24 (human/agent risk dial).
- it's learning, not just compression: #1-2 (regret/outcome = reward).
- it needs no prereg and approaches bit-reproducibility: #25 (frozen corpus +
  pinned model).

---

## 26. It is ONLINE learning — and online ENCODING beats online WEIGHTS on the things online learning is hard at

The whole construction is online (Supervisor post's two-axis sense): cards flow down
the cascade at runtime, lessons flow up as encoding updates; each attention-channel
event produces one incremental artifact applied to the LIVE substrate (dynamic-
substrate / hot-swap), no epochs, no retrain. The decisive contrast: online ENCODING-
learning cannot catastrophically forget; online WEIGHT-learning (SGD) can. Three
properties SGD-online lacks:
1. no catastrophic forgetting — the idempotence wall is a regression test against the
   ENTIRE prior decision history; a new artifact ships only if it preserves every
   past decision.
2. per-update reversibility — roll back one artifact.
3. per-update provenance — each artifact git-blameable.
Convergence isn't hand-waved: it's the monoidal contract (Make No Mistakes) — the
policy has a fixed point because the substrate is a monoid under composition.

**Trilogy implication:** the asymptote post's "generalized online learning" line
should foreground the no-forgetting guarantee as the differentiator. Online weight
methods trade plasticity against forgetting; online encoding escapes the tradeoff
because updates are discrete, replay-gated, and reversible. The idempotence wall is
not just a safety check — it is what MAKES online learning safe here.

## 27. Two update operators: it ADAPTS old policies AND creates new ones

Online improvement here is not monotonic accretion. The supervisor has two operators:
- CREATE — a net-new artifact for an unseen pattern (additive; exploration into a new
  state region).
- ADAPT — revise an EXISTING artifact when evidence contradicts the old policy
  (corrective; policy improvement on a visited state whose value changed). The REGRET
  signal (#1-2) is the TD error that drives adaptation: an outcome that contradicts a
  previously-encoded rule triggers its revision, not just a new rule alongside it.
Both operators are gated (idempotence wall + goal gradient) and reversible, so
adaptation can't silently corrupt old decisions — the revised artifact must replay-pass
against the corrected understanding.

**Trilogy implication:** the old hand-built expert system was write-once and human-
maintained; this one SELF-REVISES from the stream. State the two operators explicitly
and map them to RL (CREATE = exploration, ADAPT = improvement via TD error = regret).
This is the difference between an expert system that ossifies and one that stays at its
fixed point as the world drifts: it doesn't only grow the shell, it CORRECTS it when
the outcome channel says a past rule was wrong. Capstone property list now: no-training
+ online + adapts-and-creates + no-forgetting + reversible + auditable + no-prereg +
convergent (monoid).

---

## 28. No H100 — inference-only, and the marginal cost DECREASES

No weight training means no training hardware. The construction is inference-only:
no GPU cluster, no fine-tuning run — the entire experiment ran on a laptop + API
access. Even the LEARNING step is inference (the supervisor's classify + replay are
LLM calls, not backprop); there is NO gradient anywhere in the system. And the cost
curve is INVERTED relative to weight-learning:
- SGD/RL: large fixed training cost upfront, RE-paid for every update (retrain).
- encoding loop: only inference, and it SHRINKS — every hoisted rule retires future
  LLM calls (deterministic strata + cache pay no model freight), so marginal cost per
  decision trends toward zero as the shell grows. Online adaptation is editing a file,
  not GPU-hours.

**Trilogy implication:** add a COST row to the RL/SFT vs encoding table.
| | RL / SFT | encoding loop |
| training compute | H100-hours, upfront + per-update | none (no gradient) |
| inference compute | full model every call | only the residue; shrinks as shell grows |
| update cost | retrain + redeploy | edit one file |
| hardware | GPU cluster | laptop + API |
The economic asymptote: as the expert system subsumes the residue, the per-decision
cost falls toward the cost of a file read. The expensive part of "AI" (training) is
absent by construction; the remaining cost is a decreasing tail of inference on the
shrinking fuzzy core.

---

## 29. New policy subsumes old WITHOUT decay factors — the stabilization apparatus is absent

Online weight-learning needs an apparatus to balance new vs old knowledge: learning-
rate schedules (alpha), discount (gamma), experience-replay weighting, EWC/
regularization. All of it exists to control HOW FAST new knowledge overwrites old,
because gradient updates are CONTINUOUS and ENTANGLED — every step nudges all weights.

Here that apparatus is ABSENT, because updates are DISCRETE, COMPOSITIONAL, and
replay-gated:
- a new policy subsumes an old one by LOGICAL SPECIFICITY + explicit versioning (the
  precondition cascade fires the more-specific rule first), not by magnitude tug-of-war.
- structural artifacts don't FADE; they persist until explicitly superseded — so there
  is no decay constant to tune.
- monoid composition (Make No Mistakes) makes the update SCHEDULE irrelevant to the
  fixed point — composition is associative, so you don't need decay to stabilize
  convergence; any order of updates reaches the same shell.

**Trilogy implication:** this is the precise reason #26's no-forgetting holds — name
it. Subsumption-by-specificity replaces decay-by-magnitude. The whole hyperparameter
surface of online weight-learning (alpha, gamma, replay ratio, regularization strength)
collapses to zero knobs, because the algebra does the stabilizing. State it as: the
monoidal contract is not just a convergence proof, it is what lets you DROP the decay
schedule — the thing practitioners spend the most time tuning in online RL is simply
not present. Capstone property list: no-training + online + adapts-and-creates +
no-forgetting + no-decay-knobs + reversible + auditable + no-prereg + cheap (no H100) +
convergent (monoid).

---

## 30. EMPIRICAL (actions-nikic, 150 samples): reviewing is judgment regardless of archetype; the blinded gate caught a real overgeneralization at scale

Prediction (that the bug-squashing/test-leaning archetype would yield a bigger
encodable rind) was HALF WRONG, instructively. actions-nikic: 150 obs, 3 clusters
(APPROVED/CHANGES_REQUESTED/COMMENTED), expert=0. The one proposed rule (an APPROVED
feature-rule) was REJECTED by the blinded replay gate — it would have predicted
APPROVED on PRs nikic actually COMMENTED (e.g. "[SCEV] Canonicalise round-up idiom",
"[BasicAA] Don't look through llvm.ptrmask"). A genuine conflict, not verifier-down.

Two findings:
(a) REVIEWING is judgment regardless of contributor archetype — even a terse
    bug-squasher reviews by READING THE CODE. The "code does the talking" trait is
    about AUTHORING (commits, tests), not reviewing. So archetype-driven encodability
    should appear in respond- (authoring responses: push-fix vs argue), NOT actions-
    (review verdicts). The corpus AXIS (review vs authoring) matters more than the
    contributor.
(b) the blinded idempotence wall WORKS AT SCALE: on 150 frozen samples it caught an
    overgeneralized rule via held-out prediction, with concrete conflicts. This is the
    method's central safety mechanism, demonstrated, not asserted.

**Trilogy implication:** corpus AXIS dominates contributor IDENTITY for encodability.
And the blinded replay (#3) is the load-bearing component — show this rejection as the
worked example of the idempotence wall doing its job.

## 31. ALIGNMENT: every change is moderatable per-artifact, pre-deployment

Because each policy update is a discrete, human-readable artifact through a propose-only
gate, alignment is enforced PER-CHANGE and PRE-DEPLOYMENT: a human or an automated
goal-check can inspect, edit, approve, or VETO one rule before it enters the policy.
RLHF/Constitutional-AI bake values into weights you cannot selectively inspect or
revert; here alignment operates at the granularity of the artifact, and the goal
sentence (the gradient) is the automated filter while HITL is the manual one — both
per-artifact.

**Trilogy implication:** extend the Supervisor post's "goal as alignment lever" — it's
not only that values are an explicit spec instead of buried in weights; it's that
EVERY UPDATE passes an alignment checkpoint at artifact granularity. You can align (or
correct misalignment) one rule at a time, with provenance, reversibly. Combined with
#26-#29: the same discreteness that gives no-forgetting and no-decay gives
per-change alignment moderation. Final capstone property list: no-training + online +
adapts-and-creates + no-forgetting + no-decay-knobs + reversible + auditable + no-prereg
+ cheap (no H100) + convergent (monoid) + per-change alignment-moderatable.

---

## 32. EMPIRICAL (respond-nikic, 124 samples): the archetype/axis hypothesis CONFIRMED — 6 expert rules vs ljharb's 0

Same spec, same loop, opposite contributor: respond-nikic produced 6 EXPERT trigger->
action rules where respond-ljharb produced 0.
- review:approved->close_own_pr (47x), review:commented->push_commit (18x),
  review:approved->push_commit (16x), maintainer_comment->push_commit (9x),
  maintainer_comment->close_own_pr (8x, cli-tool), review:approved->comment_reply (4x).
- 1 agent, 1 genuine replay-rejection (maintainer_comment->close would mispredict a
  comment_reply case — gate working again).

"Code does the talking" is real and MEASURABLE: nikic responds to feedback with COMMITS
and CLOSES, not discussion (comment->push_commit = don't argue, fix). The encodable rind
is large precisely because his action distribution is action-dominant, not discussion-
dominant. Confirms #30(a): the corpus AXIS (authoring responses) is where archetype
encodability shows, and the contributor STYLE (action- vs discussion-dominant) sets the
rind size. ljharb-author=0, nikic-author=6: encodability is a property of the
contributor, demonstrated by a 6x delta on the same machinery.

BUT (ties to the thesis caveat): part of this rind encodes PROJECT WORKFLOW, not personal
judgment — "approved->close" in LLVM is the monorepo landing convention, not nikic's
taste. That is consistent with #19 (the rind rides crystallized structure; here the
project's workflow IS the structure) — but it also means the rule is only as portable as
the workflow it rides. Lift "approved->close" into a repo that merges via GitHub and it
inverts. The encodable rind is real AND context-bound.

**Trilogy implication:** the cleanest empirical pair in the whole experiment — two
contributors, one loop, 0 vs 6 encodable rules — makes "encodability is a property of
the policy's action-distribution, not the task" concrete. Pair it with the caveat: the
rind that encodes WORKFLOW is portable only with the workflow; the rind that encodes
JUDGMENT-CONSEQUENCE (#19 labels) is portable with the label schema. Neither encodes the
live judgment.

## 33. THE EXISTENCE PROOF: remit's hand-built ruleset IS the thesis, in production

The operator's original remit classifier (pr_state.py:532-656) is the thesis already
running and WORKING on live PRs — the concrete answer to the "if it works" caveat.
Anatomy:
- ONE LLM call (_classify_pr_thread) resolves the fuzzy residue into TWO booleans:
  maintainer_question (= question_unaddressed), maintainer_raised_concern (=
  concern_unaddressed). (Its own comment: "replaces three older Opus-bound judges" —
  residue-shrinking consolidation in the wild.)
- everything else is DETERMINISTIC: review_decision/ci/mergeable/state/failing_check
  from gh (CLI-tool facts); member_approved_over_cr, has_non_author_lgtm derived.
- ~4 judgment-bearing rules route on them: concern->reinvestigate; CR/question+¬green
  ->reinvestigate; CR/question+green->human; CI-failing->split(sign/reqa/reinvestigate);
  plus structural terminal->done, conflict->rebase, approved->done, else->wait.

TWO big implications:

(a) TOPOLOGY: the LLM is an UPSTREAM FEATURE-EXTRACTOR, not a bottom-of-cascade
fallback. It resolves prose -> 2 booleans at INTAKE; the deterministic cascade routes
DOWNSTREAM on those booleans. This is a DIFFERENT (and cleaner) placement than Encoding
Expertise's "LLM occupies the residual cell where rules bottom out." Both are valid: the
residue can be resolved at INPUT (fuzzy->feature) or at FALLBACK (rules bottom out into a
model call). remit does the former: one Sonnet call extracts 2 bits of judgment, pure
rules decide the rest. The trilogy should name both placements — feature-extractor vs
terminal-cell — because the feature-extractor placement is what makes the deterministic
shell a clean function of booleans (maximally auditable, the LLM's surface area is
exactly 2 bits).

(b) ROLE ASSIGNMENT (operator correction: "I was playing supervisor, not llm"): when
the operator hand-wrote the remit ruleset, they were the SUPERVISOR (the encoder), NOT
the LLM. The LLM (_classify_pr_thread) was already the residue-resolver. The proof is in
the provenance comments — wild-linker/wild#1924, feldera/feldera#6219 — each rule names
the WITNESS case (an andon, or a PR stuck in `human`) that motivated it. That is the
supervisor's loop run by hand: observe a misclassification -> encode a structural rule ->
ship it. The rule comments are the visible AUDIT TRAIL of a human-run encoding loop:
(attention-event -> artifact), exactly what supervise(spec) automates.

So the experiment is NOT reproducing the LLM's job — it is automating the OPERATOR's.
respond-nikic's proposals are the same SHAPE as remit's hand-written rules because both
are supervisor output; one supervisor was a human reading andons, the other is the loop
reading a corpus. The human-supervisor validated the shape by shipping remit to
production; the automated supervisor proposes more of the same.

**Trilogy implication:** lead with this as the existence proof, with the roles correct.
The thesis isn't speculative — a 4-rule expert system, encoded BY A HUMAN SUPERVISOR
from witnessed misroutes, fed by one 2-bit LLM residue judge, routes real PRs in
production today, with a git-blameable provenance trail on every rule. The contribution
is automating the SUPERVISOR (the human who wrote those rules), not the LLM (which was
always the residue). Pair (a) feature-extractor topology and (b) the role assignment: the
experiment closes the circle by having the MACHINE supervisor propose the same kind of
rule the HUMAN supervisor already validated by shipping it. remit is what the output
looks like; the operator's commit history on pr_state.py is what the manual loop looks
like; supervise(spec) is the loop, automated.

## 34. THE ABLATION (operator's idea): does the supervisor RE-ASSEMBLE remit from the operator's own trajectory?

The cleanest validation in the whole experiment, because it has GROUND TRUTH. The
operator already hand-encoded their response policy as the remit cascade (#33). So run
respond-kimjune01 over the PRs the operator actually responded to, and ask: does the
supervisor assemble trigger->action rules of the SAME SHAPE as the hand-written remit
cascade? If yes, the machine supervisor re-derived the human supervisor's deliberately-
authored policy FROM THE HUMAN'S OWN BEHAVIORAL TRACE.

Why this is stronger than everything prior: faithfulness-replay only checks "does a
proposed rule match past actions." This checks "does the ASSEMBLED RULESET match an
INDEPENDENTLY HAND-AUTHORED RULESET" — CONVERGENT validation against a known target, not
self-consistency. It is the closest thing to an efficacy test short of deployment: two
encoders (human-from-andons, machine-from-corpus) should converge on the same policy if
the method works.

Caveat (honest): kimjune01's PR responses are partly SWEEP-AUTOMATED (the bot posts under
that identity, and remit already drives some responses). So recovery may be partly
CIRCULAR — if remit produced the responses, the supervisor recovering remit is a
consistency check, not an independent one. Mitigate by flagging which responses look
manual (operator intervention) vs automated. Either way informative: circular recovery
confirms the loop is self-consistent; independent recovery (on manual responses) is the
real convergent-validation win.

Expected comparison targets (remit cascade, pr_state.py:532-656):
- concern -> reinvestigate; CR/question + ¬green -> reinvestigate; CR/question + green ->
  human; CI-failing -> split; approved+green+mergeable -> done; conflict -> rebase;
  else -> wait.
respond-kimjune01's assembled (trigger->action) rules will be matched against these.
[RESULT PENDING — pass running.]

**Trilogy implication (if it converges):** this is the figure that sells the whole
trilogy — two independent encoders (a human reading incident andons over months, a
machine reading a frozen corpus in one afternoon) converging on the same policy. It would
demonstrate that the encoding loop is not just a plausible construction but RECOVERS a
known-good hand-built expert system from behavioral data alone. If it does NOT converge,
the DELTA is the finding: where the machine and the human supervisor disagree localizes
exactly what the corpus-driven loop misses that incident-driven hand-encoding caught (or
vice versa).

## 35. Compound actions hide latent sub-trajectories — "push_commit" is an option, not a primitive (POMDP)

Operator: "'push another commit' is basically admitting that another investigation had
happened" / "the extra commit doesn't come out of nowhere." Decisive observation about
the action space.

"push_commit" is NOT a primitive action. To produce it, the contributor read the
comment, located the code, diagnosed, wrote the fix, tested it. The corpus records only
the COMMIT — the investigation that produced it happened off-camera and got compressed
into one action token. In RL terms push_commit is an OPTION (a temporally-extended
action / sub-policy), and the trajectory is PARTIALLY OBSERVED (POMDP): the observable
action collapses a hidden sub-trajectory.

Consequences:
- imitation from the corpus can clone OPTION-SELECTION (when to fire "investigate-and-
  fix") but NOT OPTION-EXECUTION (the investigation), because execution isn't in the
  data — only its per-case output (the diff) is, and that diff is specific to one PR,
  not a rule. You encode the decision to RUN the computation; you cannot encode the
  computation's RESULT, because it is a fresh computation every case.
- this LOCALIZES the residue precisely: the residue lives in the LATENT SUB-TRAJECTORIES
  behind compound actions. The encoding loop hoists option-selection; option-execution
  stays in the agent, observable only by its output, re-run not cloned.

Ties respond-nikic back to remit: nikic's atomic comment->push_commit is exactly what
remit DECOMPOSES — remit's concern->reinvestigate is the encodable routing, and the
reinvestigate actor runs the investigation that produces the commit. The HUMAN collapses
(route + investigate + implement) into one observable push_commit; the SUBSTRATE splits
it into actor stages. That is why remit has no push_commit bucket — it has reinvestigate/
reqa, which route INTO the investigation sub-loop. For the ablation (#34) the mapping is
push_commit <-> reinvestigate: the shapes match once you account for the option being a
hidden sub-pipeline.

**Trilogy implication:** the action partition (#20) is FRACTAL on the action side too —
an action can be a whole sub-policy. State the options framing explicitly: the encodable
policy is hierarchical (high-level option-selection over low-level option-execution), the
encoding loop hoists the SELECTOR, and each option is recursively the same (state->action)
problem one level down — its own expert-shell + residue. "Encode expertise" means encode
the option-selection cascade; the options themselves bottom out in either deterministic
sub-shells or fresh agent computation. The commit is the tip; the investigation is the
iceberg; only the tip is in the corpus, so only the selector is cloneable.

## 36. Squash-merge / force-push-amend erases the commit-level trajectory (observability is workflow-dependent)

Operator: "sometimes in OSS commits get squashed so it's hard to tell." Compounds #35 at
the COMMIT level, not just the investigation level. Squash-merge and force-push-amend
cultures (LLVM/Phabricator-style — exactly nikic's world) collapse the "push fix ->
review -> push fix" iteration history into one commit, and amended force-pushes may not
register as distinct `committed` events. So both the investigation behind each commit
(latent, #35) AND the commit-level trajectory itself can be erased.

Consequences:
- the ->push_commit support counts are NOISY LOWER-BOUNDS, not exact. respond-nikic's
  numbers (18x comment->push etc.) are especially suspect BECAUSE LLVM is an amend-force-
  push project — worst case for observing this option. The structural regularity
  (comment -> fix, not argue) survives; the magnitudes don't. (Consistent with #25.)
- corpus fidelity for an option is PROJECT-WORKFLOW-DEPENDENT: GitHub-merge repos
  preserve the iteration trajectory; squash/amend repos erase it. Ties to #32 — not only
  does the rind ride workflow, the OBSERVABILITY of the option rides workflow.

## 37. Therefore: corpus intake needs a LEGIBILITY PRECONDITION (the method's data hygiene IS the method)

Operator: "we gotta make sure to select samples where the data is legible." The fix for
#36 is a precondition on the CORPUS: select only samples where the (state, action)
trajectory is observable and unambiguous — for push_commit, GitHub-merge repos with
preserved history, clean timeline `committed` events, unambiguous trigger->response
pairing. Reject illegible samples BEFORE mining, or you get phantom patterns (#16) and
noisy support (#36).

This is the supervisor's OWN Identity-precondition stratum (#6) applied to corpus INTAKE
rather than to the live stream. Cheap, deterministic: filter by repo merge-style, require
clean timeline events, drop ambiguous trajectories. The method's data hygiene is the
method — the five strata apply to the DATASET, not just the running classifier.

**Trilogy implication:** the corpus-bootstrap (asymptote post) needs an explicit intake
precondition, and it's the SAME precondition stratum the runtime uses. State it: garbage-
in is a data-LEGIBILITY failure, and legibility is checkable deterministically (workflow
style, event cleanliness) — so the first stratum (identity/precondition) governs not just
which inputs the classifier accepts but which SAMPLES the encoder learns from. The
construction is self-applying: you precondition the corpus the same way you precondition
the stream. This also reframes #9 (top-percentile SOURCE): pick a top-percentile expert
AND a legible corpus — source quality and sample legibility are independent intake gates,
both required.

## 38. ABLATION RESULT: it CONVERGED — the machine re-derived remit's structure from the operator's own trajectory, both halves

respond-kimjune01 (32 obs, 3 recurring): the convergent-validation test of #34, and it
landed. Two independent encoders agree on the policy SHAPE — what to encode AND what to
leave fuzzy:

ENCODABLE half (converges under #35's push_commit<->reinvestigate mapping):
- machine (from corpus): review:changes_requested -> push_commit (+ postcondition
  re_request_review).
- human (remit, hand-built): CHANGES_REQUESTED + ¬green -> reinvestigate (which runs
  investigate -> produces commit).
Both = "on changes-requested, route to fix-and-resubmit." The machine RE-DERIVED the
operator's core CR rule from behavioral data alone.

RESIDUE half (converges, and this half is NOT circular):
- machine: maintainer_comment -> comment_reply -> AGENT (content-determined, can't hoist;
  rationale explicitly cited the maintainer-comment-register and said the FORMAT is
  encoded but the action-SELECTION is not).
- human (remit): maintainer comment/question handled by the LLM thread judge, not a
  deterministic rule.
Both put comment-CONTENT handling in the residue. remit has no comment_reply bucket, so
this convergence is independent of remit's structure — a genuine (non-circular) match on
the encode/residue BOUNDARY.

Honest caveats: thin sample (32 obs, 3 recurring, one cluster lost to verifier_down);
kimjune01 PRs partly sweep-automated (the encodable half is therefore partly a
consistency check, though the corpus is external OSS bug-fixes). The residue half is the
clean, independent win.

THE DELTA IS A CANDIDATE IMPROVEMENT: the machine's rule went FURTHER than the human's —
it added a postcondition `re_request_review(prior_reviewers)` after the fix push, which
remit does NOT do. So the loop didn't merely recover the hand-built policy; it proposed an
enhancement the operator hadn't encoded. Unvalidated ("if it works" stands), but exactly
the delta-as-finding #34 predicted: where machine and human supervisors differ localizes
either a machine over-reach or a real improvement the human missed.

**Trilogy implication (this is the closing figure):** two independent encoders — a human
reading incident andons over MONTHS, a machine reading a frozen corpus in one AFTERNOON —
converged on the same policy: encode "changes-requested -> fix-and-resubmit," leave
comment-content to the model. The encoding loop RECOVERS a known-good, production,
hand-built expert system from behavioral data, AND proposes a delta worth reviewing. That
is the empirical core of the trilogy: not "this could encode expertise" but "here are two
encoders, run independently, agreeing — and the machine even found one more rule." The
human's months of incident-driven hand-encoding and the machine's afternoon of corpus
mining produced the same shell. Caveat-bounded, sample-thin, but directionally decisive.

## 1. The third face of being wrong: silent regret

The trilogy names TWO attention channels: humble (inbox = "I don't know") and
cocky-loud (andon = "I was sure and something tripped"). The experiment surfaced
a THIRD that neither post makes explicit:

- **silent regret** — the agent was confident, *nothing tripped*, and only the
  later OUTCOME (merged / abandoned / stale) reveals the action was wrong.

The andon is **synchronous** regret (reward at the instant of defect). The
outcome channel is **asynchronous** regret (reward only when the world resolves).
The andon catches wrong answers that announce themselves; silent regret catches
the ones that don't. Operator's own framing: "andon cord was a kind of regret
learning" — yes, the trip-gated synchronous kind.

**Trilogy implication:** add the silent/asynchronous channel explicitly. The
two-channel picture (humble/cocky) is incomplete; there are three faces, split by
latency-of-reward.

## 2. (before, action, outcome) = the ML triple, named plainly

- before = state/features
- action = the bucket chosen (the policy's output)
- outcome = the reward/label (merged/abandoned)

This is **online interpretable policy learning**. Two DISTINCT gates that are
easy to conflate:
- **idempotence wall** validates a proposed rule against past *actions* —
  guards against drift ("don't change what we did").
- **regret detector** validates past *action* against the *outcome* — guards
  against silent error ("don't repeat what hurt us"). Where they disagree, the
  recorded action was a misclassification and the training signal is to encode
  the OPPOSITE.

The posts have the idempotence wall but NOT the regret/outcome gate. Asymptote
Learning's RL/SFT table gets sharper if the regret signal is named as literally
the reward — "same data, different substrate" lands harder when the reward
channel is explicit.

## 3. Blinding the verifier — a real, teachable bug

First implementation of the replay gate handed the checker the full
(before, action) pairs and asked "would the rule differ." That LEAKS the answer:
the model rationalizes the recorded action instead of predicting it
(writer-naive-of-verifier). Fix: show before-state only, predict the action,
compare in CODE against the withheld action. A held-out prediction, not a
circular check.

**Trilogy implication:** concrete instance of writer/verifier separation worth a
sentence — the idempotence wall only works if the thing being graded can't see
the grader's key. The blinding is not optional polish; without it the gate is a
no-op that always passes.

## 4. A too-helpful supervisor HIDES interface dirt

An investigate-owned andon leaked into switch's gather (loose channel scoping).
The supervisor didn't flag the leak — it wrote a *genuinely good* proposal for
investigate's budget gate, which MASKED the scoping bug instead of surfacing it.

**Trilogy implication:** strengthens the Supervisor post's "clean interfaces"
section with a failure mode it doesn't state: the danger of a dirty channel isn't
just lost corrections — it's that a capable supervisor papers over the dirt with
a plausible proposal, so the interface bug never gets seen. Clean interfaces
matter *because* the supervisor is good enough to hide their absence.

## 5. The supervisor can fix the DETECTOR, not just the classifier

ghost_branch (123×): I expected "verify branch before shipping." The supervisor
reframed it — the andon is usually a FALSE POSITIVE (branch missing because the
PR already merged and the branch was deleted). The proposed encoding suppresses
the bad andon, not the verdict.

**Trilogy implication:** a category the posts don't name — not every andon is a
real defect; some are detector miscalibration. The encoding loop can target the
*detector* (the andon-emitter) as well as the classifier. "Remediation" includes
fixing the alarm that cried wolf.

## 6. The supervisor has its own precondition: the clustering key

switch's inbox channel clustered on first-N-words of free-text summaries →
collisions and noise (fragments of investigation prose grouped as if they were a
stable failure shape). The supervisor's OWN "Identity (precondition)" stratum —
how it groups observations — is load-bearing. A bad clustering key produces
phantom clusters and wastes the model budget on non-distinctions.

**Trilogy implication:** the five strata apply recursively to the supervisor, and
the FIRST one (identity/clustering) is where a supervisor most easily fools
itself. The grid in the Supervisor post should note that the supervisor's
precondition is a clustering key, and its quality bounds everything downstream.

## 7. You can't crystallize a production over features you never logged

remit logs its full before-state (review, ci, mergeable, ...) → clean (before,
action) pairs, expert rules form easily. switch logs only the action + a POINTER
to the artifact; the before-state features aren't in the event → expert rules
can't form over features that were never recorded. A precursor hoist is required:
*featurize the before-state into the log* before any rule over it can exist.

**Trilogy implication:** the posts assume the before-state is available to the
encoder. In practice the first supervisor move is often "enrich the logging," and
that's a real rung on the ladder. "The shell can't learn what it can't see"
(Supervisor post) extends to: it can't learn over features the log never captured.

## 8. Convergence is across passes, not within one

Bounded attention budget (max_clusters per pass): a pass triages the loudest
clusters; the rest wait for the next pass after these proposals land. The expert
shell grows pass by pass — "starts trivial, grows to subsume the rest" is
literally iterative, with each pass's applied proposals shrinking the next pass's
recurring-cluster set.

**Trilogy implication:** the asymptote is approached in discrete pass-sized steps,
gated by operator approval (propose-only). Worth stating that the fixed point is
reached by iteration with a per-step attention budget, not in one sweep.

## 9. Top-percentile SOURCE matters more than coverage

Operator stance: "as long as the expert we're aiming for is top percentile, I'm
not too concerned about which part of the percentile we're missing out on." The
corpus exists to transfer a top-percentile expert's policy/register; partial
extraction from a top-percentile source beats full extraction from a median one.
Missing some of the expert's behavior is fine — it's the residue/tail.

**Trilogy implication:** Asymptote Learning's "replay-gated transfer from public
decision corpora" should say the SOURCE QUALITY bounds the ceiling, while
coverage of the source does not. You are importing a fixed point reached by a
top expert; you don't need all of it, just that what you import came from the
top. Sharpens the corpus-bootstrap argument: pick the best demonstrator, not the
most complete record.

## 10. One actor per corpus — the higher-order form pays off, and it enforces clean interfaces

Operator: "one actor developed for each corpus?" Yes — and this is what the
higher-order `supervise(spec)` buys: bind a spec, get an actor. Each
classifier/corpus gets a dedicated supervisor actor with its own inbox, cadence,
budget, and proposal stream. The factory grows one supervisor per production
line (Supervisor^2, same shape one level up).

Crucially, per-corpus actors STRUCTURALLY FIX finding #4: a supervisor that reads
only its own actor's channel can't have another actor's andon leak in, so it
can't paper over a cross-actor scoping bug. The clean interface stops being a
discipline you maintain and becomes a property of the topology.

**Trilogy implication:** the Supervisor post's grid (rows = recursion levels)
should show the horizontal multiplicity too: at each level there is one
supervisor PER classifier, not one global supervisor. The actor model's
"one actor, one concern" is what makes the encoding loop's interfaces stay clean
as the system scales — and the higher-order function is the mechanism that makes
spinning up a per-corpus supervisor free.

## 11. Occurrence count must distinguish N cases from 1 case surfaced N times

switch clusters showed 9 identical inbox summaries (e.g. "Global SAM unaffected",
"aioresult scope creep"). Some are genuinely 9 distinct events (a leak firing 9x);
others are likely ONE card re-surfaced 9x by reclassify passes. The N>=3 support
threshold is fooled by duplicates: a single re-emitted card clears the bar and
looks like a pattern. Fix: dedup within a cluster by case identity (repo, pr)
before counting support.

**Trilogy implication:** the supervisor's "Identity (precondition)" stratum has a
second job beyond clustering — deduping by case so support reflects *distinct*
evidence. "Recurring" must mean "happened to many cases," not "logged many times."
A re-surfaced card is not a second data point.

## 12. The supervisor distinguishes "fuzzy judgment" from "guessed fact" — and that line is the agent/cli-tool boundary

Predicted these prose-y clusters would be left to the agent (fuzzy). Wrong: the
supervisor saw they were FACTS the agent was guessing (is this dep new? does the
cache predate the fix?) and proposed cli-tool inside-clamps. The agent/cli-tool
boundary is exactly: "is the thing the agent is unsure about a JUDGMENT or a
LOOKUP?" Judgment stays in the nucleus (agent); lookup becomes a tool (inside
clamp). The supervisor drew this line correctly and unprompted.

**Trilogy implication:** sharpens the inside-clamp argument. The test for "build a
tool" vs "leave it to the model" is whether the uncertainty is over a fact
(deterministically knowable) or a judgment (not). Most "the model hedged" cases
are guessed facts, not real judgment — so the cli-tool stratum absorbs more than
you'd expect, and the agent residue is smaller than it looks. Encoding Expertise
undersells how much of the apparent residue is just un-looked-up facts.

## 13. Distinguish "verifier unavailable" from "genuine rejection"

3 of 8 switch clusters hit Sonnet timeouts/rc failures. Fail-closed is correct
(don't ship an unverified hoist), but the summary logged them as "replay-rejected"
(empty conflicts) and "human" (classifier_unavailable) — conflating a FLAKY
VERIFIER with a genuine idempotence conflict or a real escalation. An operator
reading the summary can't tell "the wall caught a drift" from "the wall was down."

**Trilogy implication:** the attention channels must report verifier-liveness
separately from verdicts. A down verifier is an availability event, not a
classification outcome; merging them corrupts the very signal the supervisor
exists to produce. (Also a plain reliability note: the LLM calls need retry, as
the classifiers themselves already have.)

## 14. A fleet of per-corpus actors IS the experimental apparatus

Operator: per-corpus actors "would give us ablations and more deltas and more
learnings" and "an engineering artifact that can be generalized." Right on both:
running one supervisor per classifier turns the deployment into a controlled
experiment — each actor is an ablation (same loop, different channel/goal), and
the deltas between them (what each hoists, what each leaves to the agent, how fast
each converges) are the learnings. The higher-order `supervise(spec)` is the
generalizable artifact: the apparatus and the product are the same code.

**Trilogy implication:** worth a closing note that the construction is
self-instrumenting — because every level is the same primitive, deploying N of
them yields N comparable runs for free. The generalization isn't claimed, it's
demonstrated by the fact that one function served switch, remit, compose, and a
public corpus unchanged.

## 15. "Supervised learning" — the pun is load-bearing (and the words converge)

Operator: "it is a kind of supervised learning, because we have a supervisor in
there!" Three converging senses of supervised:
- the OTP/Erlang SUPERVISOR (watches actors, restarts on failure),
- ML supervised learning (labeled (before, action) pairs from operator decisions),
- learning from DEMONSTRATIONS (the corpus = a top expert's labels).
Plus the regret/outcome channel = reward, edging toward RL. It straddles
supervised + RL, but the learned artifact is a PROGRAM, not weights.

**Trilogy implication:** a genuinely good closing move — the OTP supervisor (the
actor that keeps the line running) and the supervised-learning supervisor (the
actor that learns from the line's labels) are the SAME WORD doing both jobs, and
in this construction the same actor. The trilogy can land that the fault-tolerance
supervisor and the learning supervisor coincide: keeping the system alive and
teaching it are one role. Reframes "Make No Mistakes" (the wrapper/jidoka) and
this trilogy (the encoder) as two faces of one supervisor.

---

## 16. Free-text corpora don't cluster on regex — the free-clustering precondition breaks on prose

ljharb corpus: 41 comments -> 38 signatures. The register signature (hardcoded
prefixes: nit/lgtm/can-you/should-be) caught almost nothing; everything fell into
unique `register-other:<first-words>` buckets. Clustering structured events
(event kinds, bucket labels) is free and deterministic; clustering NATURAL
LANGUAGE is not — it needs semantic grouping (embeddings or an LLM tagger), which
is no longer a free precondition.

**Trilogy implication:** the "Identity (precondition) costs zero tokens" claim
holds only for already-structured inputs. For a free-text corpus the clustering
step itself needs a model, so the cheapest stratum stops being free. Worth a
caveat in Encoding Expertise: the precondition is free when the input is
structured; on prose it is itself a classification problem.

## 17. THE BIG ONE: a top-percentile reviewer's corpus is mostly JUDGMENT, not encodable register

We picked ljharb because his comments seemed "legible enough for a robot to copy"
— terse, formulaic. The corpus says otherwise. His actual high-value comments are
reasoned design judgments:
  - "The default behavior should always be the most verbose - it should identify
     the maximum possible..."
  - "Most users won't even run into negative zeroes in the first place..."
  - "disposition isn't a word that evokes clarity imo..."
The templatable part (lgtm / thanks / suggestion-block) is the TRIVIAL TAIL. What
makes him top-percentile is judgment — which is exactly the irreducibly-fuzzy
`agent` residue the encoding loop CANNOT hoist.

So the post-III corpus bootstrap behaves CATEGORICALLY DIFFERENTLY by corpus type:
- structured decision corpus (bucket routing, merged/abandoned outcomes —
  switch/remit): yields encodable preconditions/cli-tools/cache-keys. The loop
  works as advertised.
- code-review register corpus (a human expert's prose): surfaces almost nothing
  to encode, because the expertise IS the judgment. The loop correctly finds
  there's nothing to hoist.

This is the asymptote post's own boundary ("the radiologist's eye, the violinist's
hands, the novelist's chapter run on substrates the encoding loop does not reach")
showing up EMPIRICALLY. ljharb's design sense sits closer to the novelist than to
KYC screening. The experiment didn't just illustrate the boundary — it located a
specific expert on the wrong side of it, and the loop's near-empty output is the
measurement.

**Trilogy implication (load-bearing):** Asymptote Learning should distinguish
corpus types explicitly. The in-category list (KYC, claims, triage, helpdesk) all
have STRUCTURED decision corpora with replayable outcomes. A corpus of expert
PROSE is not the same thing — it mostly transfers agent-residue, not structure.
The honest claim is sharper: the bootstrap encodes from corpora of DECISIONS WITH
OUTCOMES, not corpora of expert commentary. The mistake the experiment almost made
(treating "copy the reviewer's register" as encodable) is the exact mistake the
post should warn against. The clustering near-failure (#16) and the judgment-residue
finding (#17) compound: even the part that LOOKED templatable was mostly one-off
reasoning.

Corollary: to actually run the post-III bootstrap on review behavior, the right
corpus is not "ljharb's comments" but "(PR before-state, ljharb's
merge/request-changes DECISION, eventual outcome)" — the structured triple, where
his JUDGMENT is the label and the encodable part is whatever deterministic
features predict it. The prose is the residue; the decision is the signal.

---

## 18. Action corpora CLUSTER; prose corpora don't

Same expert (ljharb), two corpus types, opposite clustering:
- comments: 41 obs -> 38 clusters (shattered; nothing recurred).
- review ACTIONS: 30 obs -> 3 clusters (APPROVED x22, CHANGES_REQUESTED x5,
  COMMENTED x3; all recurring).
The action corpus clusters for free because the verdict is a FINITE ENUM — the
same reason the local classifiers' buckets cluster. Prose has no finite partition,
so the free-clustering precondition can't grip it.

**Trilogy implication:** the precondition that makes the bootstrap cheap is a
FINITE ACTION PARTITION on the corpus. "Decisions with outcomes" (the in-category
list) all have this; expert commentary does not. State it as the gating property:
the corpus must expose the expert's decision as a label from a finite set, or the
loop has nothing to cluster.

## 19. THE refinement of #17: the encodable rind is the CONSEQUENCE of crystallized prior judgment

On the decision corpus the loop carved exactly the right line, and the slice it
could encode was THIN and revealing. Proposed rule: `labels ∩ {invalid, wontfix,
as-designed} -> CHANGES_REQUESTED`. Of 5 CHANGES_REQUESTED cases, 2 had such a
label (caught); 3 had empty labels and were rejected for CONTENT reasons (correctly
NOT claimed — the rule fires only on the labeled subset). COMMENTED and unlabeled
CHANGES_REQUESTED were left to the agent.

The subtle part: WHY is the label encodable? Because the `invalid` label is itself
a CRYSTALLIZED PRIOR JUDGMENT — some human already triaged the PR and recorded
their decision as structured data. The supervisor is NOT encoding ljharb's
judgment; it's encoding the downstream CONSEQUENCE of someone else's
already-structured judgment. The actual judgment ("is this PR invalid?") stays in
the agent/human; the rule only rides the recorded label.

**Trilogy implication (sharpens the whole thesis):** the encodable rind of a
decision is the part DETERMINED BY STRUCTURED SIGNALS THAT ARE THEMSELVES PRIOR
CRYSTALLIZED JUDGMENTS (labels, CI state, flags, prior rulings). This is exactly
why KYC / claims / triage / loan adjudication encode well — those domains are
DENSE with structured prior-decision fields. A raw code review is sparse in them
until a human labels it. So the asymptote isn't "judgment becomes code"; it's
"each judgment, once crystallized into a structured field, lets the NEXT decision
that depends on it become code." The expert system grows by consuming the
structured exhaust of prior judgments — including its own. The loop encodes
consequences-of-recorded-judgment, never the live judgment itself. That is the
precise boundary the trilogy should draw, and the two ljharb corpora (prose:
nothing; actions: a thin label-driven rind) bracket it empirically.

Corollary for the in-category list: the jobs that encode well aren't the ones with
"simpler judgment" — they're the ones whose pipelines already RECORD judgment as
structured fields the next step can key on. The prerequisite for encodability is
upstream crystallization, not simplicity.

---

## 20. The action space is CLOSED by the platform — and the open action nests a classifier

GitHub affords a FINITE action set to a contributor: push commit, comment, close,
reopen, approve, request-changes, request-review, label, assign, merge. You don't
have to discover the action partition — the platform defines it. That is what
makes this clean RL-classification: pi: state -> finite_github_action.

The one seemingly-open action, COMMENT, is itself classifiable into a finite
intent set (concede / push-back / clarify / explain / acknowledge). So the free-
text escape hatch closes into a partition too — and that sub-classifier is the
SAME supervisor problem one level down (encodable intents like "ack/thanks" vs
judgment like "here is why your concern is wrong"). The comment action is where
the agent-residue concentrates; it is a nested classifier, not an atom.

**Trilogy implication:** name the closed-action-space as the precondition that
makes a domain RL-classifiable: the action partition must be finite and known.
Platforms (GitHub, Stripe, a CRM) hand you this for free — the UI affordances ARE
the action enum. And the apparently-unbounded action (free text) recurses into the
same shell/residue structure, so the construction is fractal: every level is
shell + residue, and the open action at one level is a classifier at the next.

## 21. The bot is MORE encodable than the human expert — because it can decline the tail

The comment-intent classifier has its own long tail that escapes any task
partition: jokes, apologies, trash talk, social/relational performance. That is
the genuine irreducible residue — where the policy stops being task-classification
and becomes the novelist's-chapter side of the asymptote boundary.

But a key asymmetry: a HUMAN expert uses the full action space including the social
tail; an automated contributor does NOT need to. Sweep deliberately restricts to
the task-intent partition (its maintainer-comment-register rule already forbids
apology ceremony and chatty hedges). By opting OUT of the open-ended tail, the
bot's action space shrinks to the classifiable subset, and its policy converges
where the human's never would. The residue that is irreducible for the human is
simply OUT OF SCOPE for the machine.

**Trilogy implication (a genuinely new claim):** the encodability of a policy is
not fixed by the task — it depends on how much of the action space the agent
chooses to occupy. A machine that declines the social/expressive tail is more
encodable than the human it imitates, not less capable at the task. This flips the
usual framing: the automated contributor isn't a lossy approximation of the human
expert; it's a deliberately-truncated policy on a smaller action space, and the
truncation is what lets the encoding loop reach a fixed point. Encoding expertise
partly means CHOOSING the closed subset of actions worth being expert at.

---

## 22. The social tail isn't binary decline/occupy — the bot can distribution-match the RATE (chameleon)

Refines #21. The bot need not fully decline the social/expressive tail. It can
MEASURE the expert's (or the community's) rate of social comments from the corpus
and deploy at that same rate — "playing chameleon" to blend into local norms —
even though it cannot encode the joke CONTENT. The split:
- RATE / when / how-often to emit a social comment = an ENCODABLE parameter,
  learned from the corpus (a learned marginal, like a hyperparameter). Deterministic.
- WHAT the comment says = agent residue (generated or sampled).

In RL terms: encode the MARGINAL probability of the social action, not its high-
entropy conditional content. Chameleon = matching the observable statistics of the
register (rate, timing, length) to pass as a community member. This also serves the
goal directly — a bot that never jokes in a jokey repo reads as robotic and earns
less benefit of the doubt, lowering acceptance.

**Trilogy implication:** even the irreducible content-residue has an ENCODABLE
SHADOW — its frequency/timing distribution. The encoding loop can hoist the
marginal of an action whose conditional it can never capture. So "the part no
further encoding could compress" (asymptote) is narrower than it looks: the
CONTENT is incompressible, but the RATE is a parameter. Encoding expertise includes
calibrating the marginals of the actions you can't author from rules — matching the
distribution without modeling the draw. The chameleon move is distribution-matching
layered over an agent-generated core.

## 23. Given enough samples -> behavioral mimicry, but behavioral mimicry != judgment mimicry

With enough trajectory samples the policy converges to behavioral mimicry: the
encodable rind reproduced as rules, the unencodable actions' MARGINALS matched by
distribution (chameleon), only the high-entropy content sampled. Mimicry quality
scales with sample count. This IS the asymptote post's "expertise is a complicated
policy at its fixed point" — reconstructed from samples.

But a sharp, cautionary line: samples give you the policy's OUTPUTS (which action,
at what rate) = behavior cloning. They do NOT give you the VALUE FUNCTION behind
the judgment core. A bot can pass as the expert behaviorally — right actions, right
rates, right register — while its decision QUALITY is the agent's own, not the
expert's. You imitate what they did, not why it was right.

**CORRECTION (operator): judgment mimicry is a SUBSET of behavioral mimicry.**
Judgment is only ever OBSERVABLE as behavior — the expert's "this is invalid"
reaches anyone (including the expert) only as a verdict-action. There is no
separate value-function channel to mimic. So judgment mimicry is not a different
KIND; it is the subset of behavioral mimicry over the DECISION actions, conditioned
on the full content — the highest-dimensional, longest-tail, most sample-hungry
region of the behavior. The "competence gap" I first wrote is really a COVERAGE
gap: matching behavior on the judgment-laden input subset, where samples are sparse
and the input space (the diff content) is enormous. Given enough samples covering
that subset, judgment mimicry is achievable; it is simply the hardest region to
cover. A "behaviorally perfect but judgment-worse" bot is just INCOMPLETE
behavioral mimicry — it matches sampled contexts and diverges on held-out
judgment-laden ones.

**Trilogy implication (revised):** there is no categorical wall between behavior
and judgment — it is one behavioral-cloning problem, and judgment is its
sample-hungriest sub-region. This sharpens (and partly challenges) the asymptote
post's "substrates the encoding loop does not reach": the radiologist/novelist
boundary may be a matter of SAMPLE COMPLEXITY and input dimensionality, not a
different substrate. The honest asymptote: mimic the expert's behavior to arbitrary
fidelity GIVEN ENOUGH SAMPLES OF THE RIGHT SUBSET; the encodable rind is the cheap
low-dimensional part, the judgment core is the expensive high-dimensional part, and
both are behavior. The only detector of incomplete coverage on the judgment subset
is the OUTCOME (regret channel, #1-2), never the behavioral signature itself —
because by construction the signature is what was matched.

## 24. respond-ljharb result + the human touch: the human/agent boundary is a TUNABLE risk dial

respond-ljharb (author-response trajectories): 25 obs, 8 clusters, 2 recurring,
BOTH routed to agent (maintainer_comment->comment_reply x12; review:commented->
comment_reply x3), ZERO encodable. The supervisor reasoned that replying to a
comment is content-driven, that the nested comment-intent classifier (#20) is
"itself too fuzzy to encode," and that the outcome is orthogonal to whether a reply
was appropriate. The author-response policy's recurring mass IS the judgment core.

Operator's framing: "if we were using this supervisor for training a customer-
satisfaction bot, it would certainly be nice to have a human touch in there."
Exactly — and the architecture already has the slot: the 4th case (human) and the
inbox channel ARE the human touch. The point generalizes: the human/agent boundary
is not fixed by the task, it is a TUNABLE RISK DIAL. For a low-stakes domain you
let the agent cover more of the judgment subset (cheap, occasional miss tolerable).
For a high-stakes domain (CSAT, medical, legal) you move the dial toward HUMAN —
escalate more of the judgment-laden residue — precisely because a behaviorally-
convincing-but-wrong response (the #23 coverage gap) carries reputational/customer
harm. The chameleon (rate-matched warmth, #22) makes the bot read as caring; but
matching the SIGNATURE of empathy is where the #23 risk bites hardest, so for CSAT
you keep a human on the high-consequence draws.

**Trilogy implication:** the four-case switch's human branch is the explicit knob
for "human touch." Where you set the agent/human threshold encodes your RISK
TOLERANCE for behavioral-mimicry coverage gaps. The supervisor's goal sentence (the
gradient) is where this is specified: a CSAT goal would read "maximize genuine
resolution, escalate any affect-laden or unresolved case to a human" — and that one
sentence shifts the whole policy's agent/human partition. Encoding expertise
includes encoding HOW MUCH JUDGMENT YOU'RE WILLING TO LET THE MACHINE FAKE. The
human touch isn't a missing feature; it's a setting of the dial the architecture
already exposes.

## 25. Methodology: replication subsumes pre-registration (same provenance argument as the artifact)

Operator: "everything we're doing here is repeatable and verifiable so no prereg
required." Pre-registration is a COMMITMENT DEVICE you need when a claim cannot be
independently re-derived — it ties your hands against HARKing/p-hacking on private
data. Here the opposite holds: the pipeline is code, the corpus is public (gh), every
proposal carries its own evidence + replay log (git-blameable provenance), and the
command IS the spec (`sweep supervisor run actions-nikic` re-runs everything). So
REPLICATION SUBSUMES PREREG — you don't pre-commit a hypothesis when anyone can
re-execute and check.

This is the SAME argument as the RL/SFT table (provenance/auditability over opaque
weights), turned on the methodology: the artifact's auditability and the experiment's
no-prereg status are one fact. The construction studies itself with the epistemic
property it advocates.

Caveat, now TIGHTENED (operator): the corpus is effectively FROZEN. A closed/merged
PR is immutable in practice — its reviews, comments, timeline events, and final state
are settled history; nobody re-edits review comments on closed PRs (GitHub allows it,
but for a public contributor's review history it's vanishingly rare; even a force-push
rewrites branch commits, not PR timeline events). So "corpus drift" applies only to
OPEN PRs; restrict the corpus to closed/merged (respond- already does --state closed)
and the drift axis collapses. What remains is a FROZEN LABELED DATASET — benchmark-
grade, exactly the frozen issue/PR pairs SWE-bench is built on (which the asymptote
post already cites).

That leaves ONE source of non-determinism: the LLM (Sonnet verdicts vary run-to-run).
Pin model version + temperature=0 and the whole pipeline approaches BIT-
REPRODUCIBILITY. So the claim is stronger than "method-repeatable": with a closed-PR
corpus and a pinned model, it is a re-executable benchmark, not just a re-runnable
procedure. And the STRUCTURAL findings (#16/#17/#19) are robust even without the
pins.

**Trilogy implication:** a clean methodological coda — the provenance property the
trilogy sells (structural artifact, source/date/validation on every object) is what
lets the WORK that produced the trilogy skip prereg. Auditable artifacts are
self-verifying claims. Worth stating that the difference between "trust my prereg" and
"re-run my command" is the same difference as "trust my weights" vs "read my code."
The prereg/replication split mirrors the SFT/encoding split exactly.

---

_(experiment complete across 6 corpora: switch, remit, compose [empty], ljharb
prose [nothing encodable — judgment], ljharb actions [thin label rind + judgment],
ljharb author-responses [trigger->action policy, RL-classification]. The arc:
local classifiers encode well; expert PROSE encodes nothing; expert DECISIONS
encode a structured-signal rind; and the action space is a closed partition whose
one open action (comment) nests a classifier with an irreducible social tail the
bot can decline.)_
