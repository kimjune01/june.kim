---
name: depth-check
description: Pass a piece through to quickly find where it doesn't earn a sophisticated reader — across novelty, depth, rhetoric — then dig deeper via Socratic elicitation that keeps the writing yours. Flags by adversarial probing; asks rather than answers; never rewrites.
argument-hint: <file_path> [audience]
allowed-tools: Read, Grep, Bash, WebSearch, WebFetch, AskUserQuestion
---

# Depth-check

Find the places where the piece doesn't earn its sophisticated reader, along three axes — **novelty, depth, rhetoric** — and flag them. Do not fix them.

The governing idea: **the writing is a vessel for the ideas, a pointer to the frontier of shared understanding.** The vessel is judged by carriage, never by how closely its shape matches the other vessels in the room. The three axes are the three ways carriage fails: the pointer aimed too short of the frontier (novelty), carrying nothing that bears weight (depth), or arriving corrupted because the vessel leaked (rhetoric). In the Natural Framework this is Transmit — the idea is what crosses the boundary; the frontier of shared understanding is the substrate the next cycle reads from. Craft is the *integrity* of the vessel, not ornament on it.

A piece earns a sophisticated reader when it tells them something they didn't have (novelty), backs every load-bearing claim against the objection they'd raise (depth), and makes the case so it lands (rhetoric). Each can fail on its own: a novel claim with no support, a rigorous restatement of what they already knew, a true and new argument buried so the point never arrives.

The skill runs in **two phases**. Phase 1 is a fast pass that flags where the piece doesn't earn its reader, per claim. Phase 2 takes the flags you choose to pursue into a **Socratic elicitation loop** — the skill asks the question that draws the missing substance out of you, you answer, and your answers become the raw material you write in. The skill does the Filter and asks the questions; the human keeps the Attend and supplies every answer.

("Depth-check" is shorthand. The check is substance in the round — depth is the load-bearing axis, but novelty and rhetoric ride with it.)

Why it probes instead of pattern-matching: surface features do not track substance, and any surface rubric becomes a style guide for the thing it was meant to catch — the rule it would enforce is the rule an author games the moment it's named. So depth-check never pattern-matches style. It asks the only questions that don't collapse under that — *is this new, is it load-bearing, does it land, for this reader?* — and answers them by adversarial probe, not by counting markers. See [feedback_skills_as_compression.md](~/.claude/projects/-Users-junekim-Documents-june-kim/memory/feedback_skills_as_compression.md) and [feedback_narrow_and_bold.md](~/.claude/projects/-Users-junekim-Documents-june-kim/memory/feedback_narrow_and_bold.md).

## The three axes

- **Novelty** — does it land *at the frontier* of what this reader shares? The frontier is a band with two edges. Well inside it is **boring**: restating what the reader already holds. Outside it is **whacko**: a claim so far out it has no pointers back to the corpus prior, so the reader can't anchor it, evaluate it, or update on it — novelty with no tether reads as crankery, not contribution. The target is the straddle: one foot just past shared understanding, the other planted in the established corpus, so the reader can update from what they already hold.
- **Depth** — does each load-bearing claim survive the objection that reader would raise? Mechanism shown, not just the conclusion asserted; strongest counterargument engaged; references and coinages load-bearing, not decorative; no smuggled premise, no overclaim, no circularity.
- **Rhetoric** — is the case *made* so it lands? The strongest version of the argument actually stated; the key move given its weight instead of buried; an arc that turns (pledge → turn → prestige) rather than a flat list. This is argument-level delivery, not sentence prosody — that boundary matters (see Composes).

The axes are independent. Score each; a piece can pass two and fail the third, and the verdict says which.

## Principles

**Via negativa.** The skill only ever names what the writing is *not* yet — not novel, not load-bearing, not accurate, not landed. It never names what it should be. This isn't a limitation worked around; it's the method. By learning what the writing is not, you're forced into the place where the writing can be. Exhaust enough negations and they fence a space; the writing that survives every "not" is cornered into the one room left, and you walk in and write it. A flag is a wall, not a blueprint — and a Socratic question is a negation in disguise ("what's the mechanism?" means "this is not yet mechanized"), which is why the answer, the only affirmative act, has to be yours. The skill carves the negative space; you cast the positive.

**Filter, not generator.** The skill reports weaknesses along the three axes. It never rewrites the argument — supplying the missing novelty, depth, or force requires knowing what's true and what to say, which is Attend, which stays human. A successful run is "flagged 5 claims this reader would reject and 1 buried lede, left the sound ones alone," not a revised draft.

**Filter, but beyond surface.** It sits at the same Filter level as humanize, tighten, and sharpen — it rejects what's weak; it does not produce what's right. But those skills filter on *surface patterns* a regex can locate. Depth-check filters on *meaning*: whether a claim is new, load-bearing, and well-delivered. That's why it can't pattern-match and must probe — and why it may reach outside the text (light research) to settle whether a novelty claim is actually new. Deeper reach, same contract: it flags, the human fixes.

**Socratic, not prescriptive.** In phase 2 the skill asks the question that draws the answer out of you; it never supplies the answer. "What's the mechanism here?" not "here's the mechanism." "What would Wentworth say to this?" not "Wentworth would say X." This is the mechanism that keeps Attend human: an answer handed over is the skill doing the thinking; a question well-aimed is the skill doing the Filter and leaving the thinking to you. If you're stuck on a question, that stuck place is the finding — it's where the piece is actually thin, and it's yours to resolve, not the skill's to paper over.

**Keep your own seat.** This skill is a scaffold, not a straitjacket, and you are running it, not being run by it. Keep a degree of freedom to (1) give your own genuine reaction to the content — as a reader, not only a flag-emitter ("the cargo-cult framing is the strongest thing here; I wouldn't cut it") — and (2) opine on the exercise itself ("this flag feels forced"; "the rigor band reads too strict for this piece"; "this may be the wrong lens for this draft"). The agency is fenced, not free rein: mark your view as your own, keep it separate from the structured flags, never fold it into the prose, and leave it the writer's to ignore. Opine and judge; do not author — the replacement text is the writer's Attend, not yours. The reason for the seat: your read is information, and a skill that grinds you into a pure automaton discards the one perspective that might notice the skill is wrong *here*. A standard leaves room for judgment; only a bad gate forbids it — and this skill came from respecting that difference.

**Adversarial, never pattern-based.** Each load-bearing claim is judged by trying to *dismiss, refute, or out-bore* it from the target reader's chair, using a different model family (codex GPT-5.5, gemini) so the probe doesn't share the author's blind spots. Surface scans only *locate* candidate claims; the verdict is always the probe. Do not build or consult a feature checklist as the gate — a checklist is a surface, and a surface is gamed the moment it's named.

**Audience-relative.** "Novel," "the strongest objection," and "lands" all mean nothing without a reader. Pin the audience before probing. The same paragraph is novel to a generalist and stale to the subfield.

**Substance ≠ style ≠ length.** A short concrete sentence can be deep, novel, and land; a long jargon-dense paragraph can be none of the three. Never reward abstraction, jargon density, or word count; never penalize concreteness, plainness, or brevity. If the skill starts doing that, it has stopped measuring substance and started measuring conformity.

**Every target is a band; flag both edges.** Each axis and calibration is an interval with two failure edges, not a quantity to maximize. Novelty: boring ↔ whacko. Precision: vague ↔ false-precise. Rigor: blog ↔ journal. Accuracy: lossy ↔ redundant. This two-sided fencing is *why the skill converges*: a one-sided "more is better" gate never terminates — it always finds one more citation to want, one more marker to add — but a band has a non-empty interior, and once the writing is inside it there is nothing left to flag. The negations close from both directions and corner the writing into a bounded room rather than chasing it toward an unreachable maximum.

**Converges under repeated application.** Same monoidal contract as humanize, tighten, sharpen, and it falls out of the band structure above. On unchanged text the report is idempotent: `depth-check(depth-check(x)) == depth-check(x)`. As the writer addresses flags, the flag set shrinks monotonically. The fixed point is a non-zero floor — the interior of the bands — some claims are as deep, novel, and well-delivered as they can be without becoming a different piece. Driving the count to zero forces invented nitpicks; don't.

**If unsure, leave alone.** Flag only what the target reader would *actually* reject, skip, or already know. Borderline is what the writer is for. Over-flagging trains the writer to ignore the skill.

## The audience step (do this first)

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

4. **Triage and report.** Keep only weaknesses the target reader would actually reject, skip, or already know. Drop nitpicks.

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
- **Flags:** one block per weakness —
  - location (quote the line)
  - axis + failure mode (from the taxonomy)
  - the gap, in the reader's voice ("an expert in X already assumes this" / "asks: where's the mechanism?" / "the real point is the last clause, and it's thrown away")
  - whether codex/gemini/both surfaced it
- **Verdict, per axis:** for each of novelty / depth / rhetoric — STRONG / THIN (addressable in revision) / FAILS (the central claim is stale, unsupported, or never lands). The headline verdict is the weakest axis.
- **The one thing to fix first:** the single weakness that most costs this reader.
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

## Rules

- **Pin the audience before probing.** All three axes are undefined without a reader; novelty most of all.
- **Probe; don't pattern-match.** No surface-feature rubric as a gate, ever. A named surface rule is a rule the author games.
- **Report; don't rewrite.** Supplying novelty, depth, or force is Attend. The skill stops at the flag.
- **Different model family for the probe.** Codex/gemini, not a same-family echo of the author.
- **Flag only what the reader would reject, skip, or already know.** Over-flagging breaks convergence and trust. The fixed point is a non-zero floor.
- **Never reward length, jargon, or abstraction; never penalize concreteness or brevity.** A gate that does the opposite is measuring conformity, not carriage.
- **One pass per invocation.** Don't loop to drive flags to zero; that invents nitpicks (the slop-detection convergence-collapse pattern).
- **Research is light and bounded.** A few searches to confirm or puncture a novelty claim. The moment a claim needs a real survey to settle, flag "needs `/deep-research`" rather than half-doing it. Depth-check screens; it is not the research harness.

## Composes

| Step | Skill | Notes |
|------|-------|-------|
| 2 | `/codex` | Three-axis skeptic probe, structural |
| 2 | `/gemini` | Same probe, different family — logic and inverted-claim catch |

Boundary with the prose skills: depth-check's **rhetoric** axis is *argument-level* — is the strongest case made, in an order that lands. It does **not** touch sentence prosody, pacing, or AI tics; that's `/readability` and `/humanize`. Sequence: depth-check decides *whether the piece is worth saying to this reader and whether the case lands*; humanize/tighten/sharpen/readability/copyedit decide *how it reads* once it is. Run depth-check first — there's no point polishing prose whose central claim is stale or unsupported.

## The one invariant

If anything here is forgotten, keep this: **conformity is not substance, and surface features track neither.** Depth-check only ever asks whether the writing carries a new, load-bearing, well-delivered idea to its reader — by probing the claims, never by scoring the surface. Every rule above is that sentence, unfolded.
