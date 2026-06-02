---
name: depth-check
description: A blind-spot checker for arguments. Finds where a piece doesn't earn a sophisticated reader — across novelty, depth, rhetoric — applies the obvious subtractive fixes (reversibly), and elicits the rest via Socratic loop. Never authors new substance.
argument-hint: <file_path> [audience]
allowed-tools: Read, Grep, Bash, WebSearch, WebFetch, AskUserQuestion
---

# Depth-check

A blind-spot checker for arguments. Find where the piece doesn't earn its sophisticated reader, along three axes — **novelty, depth, rhetoric**. Cut and scope the obvious wrongs yourself (subtractively, reversibly); elicit the rest. Never author new substance.

The governing idea: **the writing is a vessel for the ideas, a pointer to the frontier of shared understanding.** The vessel is judged by carriage, never by how closely its shape matches the other vessels in the room. The three axes are the three ways carriage fails: the pointer aimed too short of the frontier (novelty), carrying nothing that bears weight (depth), or arriving corrupted because the vessel leaked (rhetoric). In the Natural Framework this is Transmit — the idea is what crosses the boundary; the frontier of shared understanding is the substrate the next cycle reads from. Craft is the *integrity* of the vessel, not ornament on it.

Two phases. Phase 1: a fast pass that flags where the piece doesn't earn its reader, per claim. Phase 2: a **Socratic elicitation loop** — the skill asks the question that draws the missing substance out of you; your answers become the material you write in. The skill filters and asks; the human keeps the Attend and supplies every answer.

It probes rather than pattern-matches because surface features don't track substance, and any surface rubric becomes a style guide for the thing it meant to catch (the rule it enforces is the rule an author games once named). See [feedback_skills_as_compression.md](~/.claude/projects/-Users-junekim-Documents-june-kim/memory/feedback_skills_as_compression.md) and [feedback_narrow_and_bold.md](~/.claude/projects/-Users-junekim-Documents-june-kim/memory/feedback_narrow_and_bold.md).

## The three axes

- **Novelty** — does it land *at the frontier* of what this reader shares? The frontier is a band with two edges. Well inside it is **boring**: restating what the reader already holds. Outside it is **whacko**: a claim so far out it has no pointers back to the corpus prior, so the reader can't anchor it, evaluate it, or update on it — novelty with no tether reads as crankery, not contribution. The target is the straddle: one foot just past shared understanding, the other planted in the established corpus, so the reader can update from what they already hold.
- **Depth** — does each load-bearing claim survive the objection that reader would raise? Mechanism shown, not just the conclusion asserted; strongest counterargument engaged; references and coinages load-bearing, not decorative; no smuggled premise, no overclaim, no circularity.
- **Rhetoric** — is the case *made* so it lands? The strongest version of the argument actually stated; the key move given its weight instead of buried; an arc that turns (pledge → turn → prestige) rather than a flat list. This is argument-level delivery, not sentence prosody — that boundary matters (see Composes).

The axes are independent. Score each; a piece can pass two and fail the third, and the verdict says which.

## Principles

**Via negativa.** Name only what the writing is *not* yet, never what it should be. That's the method: exhaust the negations and they fence the room where the writing can be, and you walk in and write it. A flag is a wall, not a blueprint; a Socratic question is a negation in disguise ("what's the mechanism?" = "not yet mechanized"), so the affirmative is always yours.

**Filter at the meaning level; prescribe only via negativa.** Like humanize/tighten/sharpen it filters, but on *meaning*, not regex-findable surface, so it must probe (and may reach outside the text for light research). It *may apply* the fixes that are pure via negativa — **subtract, narrow, relocate, mark** — because those remove or scope what's wrong without asserting anything new: cut a dead reference, narrow an overclaim to the scope the text already supports, mark an unmarked projection, move a buried lede up. It *must not* author the fixes that need new substance — a missing mechanism, the answer to an objection, the delta over prior work — those it elicits (Phase 2). Two gates, both required to auto-apply: the fix must *remove or scope* (not assert) **and** you must be confident. An ambiguous subtraction (is this reference really dead? is the scope really that narrow?) surfaces to confirm, never a silent edit. Confidence never licenses assertion — feeling sure you know the missing mechanism is the curse-of-knowledge trap, not a warrant, and still elicits. Applied fixes ship as a reversible earn-back batch (line, before→after), separate from the elicited threads. Subtraction the skill can do; assertion is yours.

**Socratic, not prescriptive.** Phase 2 asks the question that draws the answer out, never supplies it ("what's the mechanism?" not "here's the mechanism"). A stuck answer is the finding: it's where the piece is actually thin, and it's yours to resolve, not the skill's to paper over.

**Keep your own seat.** You run the skill, not the reverse. Keep the freedom to react as a reader ("this framing is the strongest thing here") and to opine on the exercise itself ("this flag feels forced"; "wrong lens for this draft"). Fenced: mark it your own, separate from the flags, never folded into the prose, the writer's to ignore. Opine and judge; don't author. Your read is information a pure automaton would discard.

**Adversarial, never pattern-based.** Judge each load-bearing claim by trying to *dismiss, refute, or out-bore* it from the reader's chair, ideally via a different model family (codex/gemini) so the probe doesn't share the author's blind spots. Surface scans only *locate* candidates; the verdict is the probe. No feature checklist as a gate — a checklist is a surface, gamed once named.

**Substance ≠ style ≠ length.** A short concrete sentence can be deep, novel, and land; a long jargon-dense one can be none of the three. Never reward abstraction/jargon/word-count; never penalize concreteness/plainness/brevity. Doing so measures conformity, not substance.

**Every target is a band; flag both edges.** Each axis/calibration is an interval with two failure edges, not a quantity to maximize: novelty boring ↔ whacko, precision vague ↔ false-precise, rigor blog ↔ journal, accuracy lossy ↔ redundant. The two-sided fencing is *why it converges*: a one-sided "more is better" gate never terminates, but a band has a non-empty interior, so once the writing is inside it there's nothing left to flag. `depth-check(depth-check(x)) == depth-check(x)`; the fixed point is the band interiors, a non-zero floor. Driving the count to zero invents nitpicks; flag only what the reader would actually reject, skip, or already know.

## The genre gate (run this first)

Before audience, before probing: what is the piece *for*? The three axes are not uniformly applicable. Which ones fire depends on the genre, and running the wrong axis on the wrong genre is how the skill misfires.

- **Contribution** — an argument that makes a forward claim (an essay, a design rationale, a thesis). **Run all three axes**; novelty is load-bearing. This is depth-check's home, and its highest yield.
- **Defense** — a rebuttal or FAQ that answers objections (an objections doc, a limitations section). **Run the depth axis only.** Novelty is moot: the job is completeness and honest concession, not contribution, and a sound rebuttal passes depth by construction. Don't reach for novelty here or you will invent flags. Low yield is the *correct* result, not a failed run.
- **Presentation** — a doc that orients or reports rather than argues (a README, a landing page, release notes). **Don't run depth-check at all.** None of the three axes fit; its defect, if it has one, is *legibility*, which is humanize and readability's opening-orientation check, not substance-probing. Route there instead.

The tell for genre is structure. A defense is *externally structured*: the objections set the outline, so there is little room to bury a lede or over-argue, and little for the skill to find. A contribution is *open-structured*: the author chose the sections, which is where redundancy, over-argument, and buried theses live, and where the skill earns its keep. Spend the run on open-structured contribution docs; on externally-structured defenses, expect to confirm, not to find.

If a doc is mixed (an essay with a defensive section), gate per section, not per document.

## The audience step

Resolve the target reader before any probing:

1. If the piece names or implies its audience (a LessWrong post, a paper for a subfield, a memo for maintainers), use that.
2. Else infer it from venue and vocabulary, and state your inference.
3. If genuinely ambiguous and it changes the verdict, ask via AskUserQuestion: "Who is the sophisticated reader I should hold this to?"

Write the resolved audience at the top of the report. Every verdict is relative to it — especially novelty, which is entirely a function of what this reader already knows.

## The rigor band

Hold the piece to a target rigor that sits **strictly between a casual blog post and a peer-reviewed journal article — excluding both ends.** The exact point inside that interval is still being tuned (treat it as a dial, not a fixed line); what's fixed is that neither boundary is the target.

**Above the floor (not a casual blog).** A blog post may assert and move on, run on vibes, overclaim for effect, skip the obvious objection. Depth-check presses past that: it wants the mechanism shown, the strongest objection engaged, claims calibrated, and a real contribution. Bare assertion, unearned universals, and "trust me" do not clear the band.

**Below the ceiling (not a journal).** A journal demands formal citation for every claim, an exhaustive related-work survey, statistical-significance apparatus, reproducibility appendices, and hedged-to-mush phrasing. Depth-check requires **none** of these, and must not flag their absence. Do not flag a claim merely for lacking a citation if the argument carries it. Do not demand the piece survey all prior work — only that it name the prior art its *novelty* claim stands against (the light-research step). Do not push toward hedging; the fix for an overclaim is narrow-and-bold, not a thicket of qualifiers.

In short: the claim must be *argued and checkable*, not *formally apparatus'd*. When a flag would only be true at journal rigor, drop it. When a weakness would pass at blog rigor but not essay rigor, keep it. This band, together with the resolved audience, sets how hard every axis presses.

Two measurement targets pin the band:

- **Precision — a range, not a maximum.** Claims are specified tightly enough to be useful and no tighter. A vague gesture underspecifies and fails low; false hairline precision — exactness the evidence doesn't support — overspecifies and fails high. Narrow-and-bold lands inside the range; over-narrowing into invented significant figures overshoots it. Flag both ends.
- **Accuracy — enough to reconstruct.** The vessel carries the idea faithfully enough that a reader can rebuild the argument from a single load-bearing paragraph (the reconstruction test, below). Precision is how tightly the pointer locates the frontier; accuracy is whether it points at the real frontier and arrives intact.

## Phase 1 — scan and flag (fast)

1. **Extract the load-bearing claims.** Read the piece. List the claims the argument rests on — the ones that, if false or stale, sink it. Ignore connective tissue and asides. Grep locates; the judgment of "load-bearing" is yours.

2. **Probe each claim adversarially, on all three axes.** For the claims that matter most, run codex and gemini (different families); a single family is fine for a quick pass. The probe asks:
   - **Novelty:** would this reader already know or assume this? What, if anything, here is new to them?
   - **Depth:** what's the strongest objection, and is it engaged? Is the mechanism shown or only asserted?
   - **Rhetoric:** is the strongest version of this claim the one on the page? Is the key move buried, flattened, or delivered with its weight?

   ```bash
   codex exec --skip-git-repo-check "Hold this claim to a [AUDIENCE] reader. Three questions, answer each: (1) Novel — would they already know this? (2) Deep — name the strongest objection it leaves unanswered or the mechanism it asserts without showing. (3) Rhetoric — is the strongest version on the page, or is the point buried/flat? Be specific; quote the line. If it's sound on an axis, say so."
   ```

3. **Run the structural tests** (cheap, deterministic, every claim):
   - **Deletion test (depth).** Remove the author — the feelings, the anecdote, the "I think." Do the receipts still stand? If the claim holds only because the author vouches for it, it's shallow. (From [Sour Red Tapes](https://june.kim/sour-red-tapes): "delete my submission from the story and every receipt still stands.")
   - **Delete-the-reference test (depth).** Remove each citation, named thinker, or coined term. If the argument is unchanged, it was decoration. (Appended Peirce/Lakatos read as name-dropping; the "Call it X" coinage passed because removing the verb removed the move.)
   - **Already-said test (novelty).** Could the target reader have written this sentence before reading? If yes, it carries no novelty — it may still earn its place as setup, but it isn't the contribution.
   - **Reconstruction test (accuracy).** Take a load-bearing paragraph on its own. Can the target reader rebuild the argument it makes — its claim, its move, how it connects — from the paragraph itself? If not, it's lossy carriage: leaning on context it never carried, or ornament with no argument inside. Scope to the paragraph's own share of the argument, not the whole essay — every paragraph restating the thesis is redundancy (a rhetoric failure), not accuracy.
   - **Light research (novelty and novelty-adjacent claims).** When a claim *asserts* novelty ("no one has," "the first," "a new") or its weight depends on a fact the reader would check (a named prior result, a who-said-it-first, a "this is established"), run a few targeted WebSearch/WebFetch queries to see whether it already exists in the literature or the community. Bounded — a handful of searches to confirm or puncture, not a survey. If the claim turns out to need a real lit review to settle, don't fake it: flag it as "novelty unverified — needs `/deep-research`" and move on. Verification rigor: don't let a novelty claim stand on the author's assumption that it's new (see [feedback_verification_rigor.md](~/.claude/projects/-Users-junekim-Documents-june-kim/memory/feedback_verification_rigor.md)).

4. **Triage, split, and report.** Keep only weaknesses the target reader would actually reject, skip, or already know; drop nitpicks. Then split the survivors: **auto** (the fix is pure via negativa — cut a dead reference, narrow an overclaim to the text's own supported scope, mark a projection, reorder a buried lede) and **elicit** (the fix needs new substance — mechanism, objection-answer, prior-art delta; or an overclaim whose true scope you can't tell from the text). Apply the auto fixes as a reversible earn-back batch; route the elicit ones to Phase 2.

## Failure modes (the finite set)

Each flag names one, tagged by axis. Every one is an argument-level judgment confirmed by probe — not a surface pattern.

**Novelty** (the frontier band — flag both edges)
- **No news (boring edge).** Sound and well-supported, but the reader already knew it. Both feet inside the frontier.
- **Untethered (whacko edge).** A claim past the frontier with no pointers back to the corpus prior — it connects to nothing the reader already holds, so they can't anchor, evaluate, or update on it. The mirror of *no news*: new, but un-bridged. A novel claim must point back to the prior to be evaluable — and that's a substance question (does the claim connect to the established corpus?), never a style one.
- **Uncredited reinvention.** A known idea presented as new, without naming the prior work it extends or breaks from. (A special case of missing-tether: the pointer back exists in the world but not on the page.)
- **Missing "so what."** The contribution is real but the reader can't locate what changes downstream of it.

**Depth**
- **Assertion without mechanism.** The conclusion is stated; the gears are missing.
- **Unaddressed strongest objection.** The best counterargument isn't engaged. (Done right: the networking-objection passage in [Papiermark Credentials](https://june.kim/papiermark-credentials).)
- **Decorative reference.** A citation, name, or jargon term that fails the delete-the-reference test.
- **Dead coinage.** A coined term that does no argumentative work.
- **Smuggled premise.** A load-bearing step assumed rather than argued.
- **Overclaim beyond evidence.** A universal claim where only a narrow one holds. Fix is narrow-and-bold: the narrow claim stated boldly is deeper than the hedged-universal one.
- **Author-dependence.** Fails the deletion test — rests on the author's feeling, not on receipts a stranger can check.
- **Abstraction without instance.** A general claim that never touches a concrete case the reader can test.
- **Circularity.** The conclusion is baked into the premises.

**Rhetoric**
- **Buried lede.** The strongest or most novel point is hidden mid-paragraph or arrives too late.
- **Flat delivery.** A claim that should be dramatized is asserted in passing, so its weight never registers.
- **Strawman of own case.** A weaker version of the argument is the one on the page; the strongest form was available and skipped.
- **No turn.** The piece lists rather than argues — no pledge/turn/prestige, no "therefore" or "but," just "and then."
- **Anticlimax.** The structure promises a payoff the ending doesn't deliver.

## Calibration example

A Feynman-flavored essay on cargo cult science: rhetoric STRONG (the voice lands, the arc turns), depth STRONG (a real concept with a real mechanism), novelty **FAILS** — it's Feynman's own 1974 talk, and the target reader already has it. One search confirms non-novelty. Verdict: FAILS, "interesting and sound, but no news for this reader." This is the case the novelty axis exists for: rhetoric and depth can both be high and the piece still shouldn't ship.

The flag is not "don't write this." It's "restating it isn't the contribution — what do you add?" The same essay clears novelty the moment it *extends* the idea somewhere non-obvious (cargo cult science applied to ML benchmark validity, say). Flag the homage; pass the extension.

## Not a problem (leave alone)

Concreteness, plainness, brevity, short aphoristic sentences, first-person anecdote that earns its place by carrying a receipt, genuine scoped hedges, deliberate setup that isn't meant to be novel, and any claim that is new to the reader, survives its strongest objection, and is delivered with its weight — even in three sentences. None of these are weak. The skill that flags them is measuring conformity, not substance.

## Output

A report, no edits. For the whole piece:

- **Audience:** the resolved reader (named, inferred, or confirmed).
- **Load-bearing claims:** the list the argument rests on.
- **Flags, rank-ordered by actionability** — most actionable first, each tagged **[auto]** (applied, see below) or **[elicit]** (to Phase 2). One block per weakness:
  - location (quote the line)
  - axis + failure mode (from the taxonomy)
  - the gap, in the reader's voice ("an expert in X already assumes this" / "asks: where's the mechanism?" / "the real point is the last clause, and it's thrown away")
  - whether codex/gemini/both surfaced it
- **Applied (subtractive, reversible):** the [auto] fixes as an earn-back list — line, before→after — so the writer can undo any. Only cut / narrow / relocate / mark; never an additive rewrite.
- **Verdict, per axis:** for each of novelty / depth / rhetoric — STRONG / THIN (addressable in revision) / FAILS (the central claim is stale, unsupported, or never lands). The headline verdict is the weakest axis.
- **Your own take (free-form, non-binding):** your reaction as a colleague, separate from the flags — what's strongest in the piece, what you genuinely doubt, and whether this exercise served the draft or was the wrong lens. The writer weighs it or ignores it; it's a view, not a verdict.

This report is fast and disposable — it exists to tell you *where* to dig. It is the handoff into phase 2, not the end.

## Phase 2 — Socratic elicitation (deep, human-paced)

Now dig, one flag at a time, in whatever order you choose. For each flag you pursue, the skill asks the question that draws out the missing substance. You answer; your answer is the material you'll write in. The skill captures what you said and asks the next question — it does not write the prose.

The question is shaped by the failure mode:

- **Assertion without mechanism** → "Walk me through *why* X causes Y. What's the step a skeptic would stop you on?"
- **Unaddressed objection** → "The strongest objection a [reader] has is ___. What's your answer? If you don't have one, is the claim still true?"
- **No news / uncredited reinvention** → "What does this add that [prior work] didn't already say? Name the delta." (Light research first, so the question names the real prior art.)
- **Overclaim** → "Where exactly does this stop being true? Name the boundary, then we state the narrow version boldly."
- **Buried lede / flat delivery** → "What's the one sentence here you'd keep if you could keep only one? Why isn't it first / why is it thrown away?"
- **Decorative reference / dead coinage** → "Delete this name/term. What breaks? If nothing, why is it here?"

Rules of the loop:

- **One thread at a time.** Don't fan out questions; follow the one you're on until it resolves or you park it. Depth comes from staying, not from breadth.
- **Ask, capture, ask — never answer.** If you ask the skill to just tell you, it can offer *options to react to* (a menu, not a verdict) and hand the choice back. The judgment stays yours.
- **A stuck answer is the finding.** If you can't answer "what's the mechanism," the piece doesn't have one yet. Mark it; that's the realest output of the run.
- **You set the depth and the exit.** The loop ends when you've drawn out what you need — not on a flag count. Park the rest.

## Phase 3 — compile (the fold-back list)

When you've run enough rounds — your call, not a flag count — the skill compiles everything elicited into a single ordered improvement list. This is the only thing that outlives the session. Each item:

- **Location** — the line or section it lands in.
- **The improvement** — in *your own words from the loop*, not the skill's paraphrase. The skill is transcribing your Attend, not adding to it.
- **Axis + move** — novelty / depth / rhetoric, and the action (add the mechanism you gave, state the narrow boundary you named, move the kept sentence to the front, cut the dead reference).
- **Open** — flags you parked and stuck answers, listed honestly as unresolved. These are real findings, not omissions.

Ordered by what most costs the reader, so you fold from the top.

Then stop. **Folding the list back into the writing is yours** — it's the line-level Consolidate the skill deliberately doesn't automate. If you want drafting help on a specific item, that's the [double-loop](https://june.kim/double-loop) (you direct, Claude drafts) as a separate step — not depth-check reaching into the prose. The skill compiled the labor; the writing stays your hand.

## Composes

| Step | Skill | Notes |
|------|-------|-------|
| 2 | `/codex` | Three-axis skeptic probe, structural |
| 2 | `/gemini` | Same probe, different family — logic and inverted-claim catch |

Boundary with the prose skills: depth-check's **rhetoric** axis is *argument-level* — is the strongest case made, in an order that lands. It does **not** touch sentence prosody, pacing, or AI tics; that's `/readability` and `/humanize`. Sequence: depth-check decides *whether the piece is worth saying to this reader and whether the case lands*; humanize/tighten/sharpen/readability/copyedit decide *how it reads* once it is. Run depth-check first — there's no point polishing prose whose central claim is stale or unsupported.

## The one invariant

If anything here is forgotten, keep this: **conformity is not substance, and surface features track neither.** Depth-check only ever asks whether the writing carries a new, load-bearing, well-delivered idea to its reader — by probing the claims, never by scoring the surface. Every rule above is that sentence, unfolded.
