---
name: trim
description: Argument-level compression by a strengthened absence test (does the argument stand with the same force, clarity, evidence, scope, pacing, and misreading-resistance?). Removes passages that fail it (self-referential cruft, cross-section restatement, self-recap, re-derivation, scaffolding, expired reader-orientation, stakes inflation, inert hedges, redundant examples); grafts good rhetoric onto an adjacent essential point rather than deleting. Idempotent. The structural cousin of /tighten (word-level) and /not-but (negation).
argument-hint: <file_path>
allowed-tools: Read, Edit, Grep, Bash, Agent
---

# Trim: Argument-Level Compression by the Absence Test

`/tighten` cuts words inside a sentence you are keeping. `/not-but` defuses one construction. `/trim` is the level above both: it removes whole clauses, sentences, and passages that the **argument** does not need, even when each is individually well-written. A paper gets long not only from wordy sentences but from sentences that should not be there at all.

## The absence test (the master rule)

> Remove the passage. Does the argument still stand *with the same force, clarity, evidence, scope, pacing, and resistance to misreading*?
>
> If yes, the passage is nonessential and excessive, and it goes.
> If the removed phrasing is *good* (vivid, memorable, sharp), do not just delete it. Graft its rhetoric onto an adjacent point that **is** essential.

The qualifier is the whole guard against over-cutting, and it is not optional. Plain "does the argument survive" is too weak: almost any one sentence can be removed while the gross thesis stays intelligible, yet still be doing real work, pacing the reader's inference, blocking a misreading, carrying evidentiary weight, marking stakes, or easing a transition. Logical survivability is not editorial dispensability. A passage earns its place by force, clarity, evidence, scope, pacing, or misreading-resistance, and audience is a parameter of all six: a derivation an expert can skip is one a general reader needs.

This is why *beauty* has to be split. Cut *ornament*, phrasing that decorates without doing any of that work, or relocate it. But *voice* that carries stance, precision, or authority is doing work, so it is a hard keep, not ornament. The question is never whether a line is pretty; it is whether the line carries a function.

## The invariant (what the test measures)

The patterns below are symptoms. The rule they are symptoms of is one predicate, and representing the rule matters more than memorizing the list, because a list catches only the cruft you have already seen:

> A passage is cruft when its **marginal information is zero** given the rest of the document and everything it references, across every dimension that carries value: propositional content, evidence, scope precision, pacing, misreading-resistance, and stance.

A passage earns its place by adding something the reader does not already have, on at least one of those dimensions. "Already have" is the whole game, and it has several sources: stated elsewhere in the document (cross-section restatement, self-recap), reachable through a citation (re-derivation), carried by the demonstration the passage merely asserts (stakes inflation), or needed only by the writer's path to the claim and not the reader's use of it (expired orientation). When the marginal contribution is zero on every dimension, the passage's absence has no test, which is exactly why it can go.

The same predicate explains the hard-keeps: each is a dimension where marginal information is usually nonzero (voice carries stance, a gradient carries generality, a content-hedge carries scope). Cut those and you destroy information, which is not trimming.

But the dimensions are weighed *under* argument, not beside it. Voice and pacing are not independent licenses: if the argument is lacking, the voicing is irrelevant. A sentence that sounds good yet advances no argument is filibuster, volume without information, cut however well it reads. So emphatic restatement gets a sharp test: does the repeat advance the argument, or only its loudness? Three sentences for two argument-points are two of argument and one of filler; the author who does not want to read as padding cuts the third. This is the skill's most over-protected cut, because "but it's the voice" is the easiest rationalization for keeping a line that earns nothing.

So represent the rule, do not tabulate the patterns. The patterns are the cruft already seen; the rule catches the cruft not yet on the list, any passage whose marginal information is zero in a shape no example has shown you. Measure that information against *the rest* of the document, including any *parallel* section: two "how to apply" sections for different audiences can each beat the descriptive section yet be redundant against *each other*, so keep the one matched to the document's audience and cut the other, unless the document deliberately serves *both* (a human explanation beside an agent checklist), where each carries audience-information the other lacks and both stay. (The prose form of holding out the answer key, as [abductor](https://github.com/kimjune01/abductor) does for code: the cut you can justify only by re-reading your own prose is the one to distrust.)

## What to hunt (each subject to the absence test)

These are passage-level patterns. Where one blurs into word-level wordiness, that part is `/tighten`'s job, not trim's; the boundary is noted where it matters.

1. **Self-referential cruft.** Meta-commentary that *performs* the thesis instead of advancing it: "this paper is itself a node," "typed open and untrue," "the paper obeying its own rule." Enacting the worldview is not the same as clarifying the content. Keep only the self-application that *does* clarify, e.g. a falsifier list that states what would break the paper, because that is content, not performance.

2. **Cross-section restatement.** A claim already made in another section, restated. Keep the strongest instance; cut the echoes. Abstracts and conclusions restate to help a reader locate the contribution, so test sharply: does the restatement add an *angle* (new framing, sharper word, a way in for a different reader), or is it the same point again with nothing added? If nothing added, cut. Two structural cases. A "pitfalls" section mirroring a "conventions" section, restating each rule as its violation: keep a violation that adds a failure-detail, cut the pure mirror. The inverse: a "how to apply" or decision section restating *descriptive* sections as *imperatives* is synthesis, not echo, because turning observation into a rule is a new angle; keep it.

3. **Self-recap.** The local twin of #2: a clause that restates its own sentence, or a list re-given in another register a line later (e.g. "true, false, untrue" then "green, red, hung"). The distinction is scale, within or adjacent to a sentence, not across sections. Keep the register that does the most work; cut the recap.

4. **Re-derivation.** Re-explaining what a citation or a companion work already establishes. The "explains where it should cite" failure: the passage rebuilds an argument the reader can be *pointed* to. Replace the re-derivation with the reference.

5. **Scaffolding / framing moves.** Whole sentences that *announce* a move instead of making it: "The question is X, and the answer is Y," "Having established A, we turn to B," "What is interesting here is." Trim removes the framing sentence; the phrase-level version ("it is worth noting that") is `/tighten`'s. State the conclusion and the frame falls away.

6. **Expired reader-orientation.** Setup that helped the *writer* reach the claim but the reader no longer needs once the claim is on the page: historical throat-clearing, "before we can see X we must understand Y," procedural roadmaps, a problem restated after its solution is clear, background that traces the author's path rather than the reader's need. Distinct from scaffolding: scaffolding announces a move; expired orientation preserves a discovery process. Cut what oriented the *writing*; keep what orients *this* reader (audience-dependent).

7. **Stakes inflation.** Sentences that *say* the point is important, radical, surprising, foundational, or urgent instead of *showing* why. Importance-language is a promissory note the argument should pay in cash. Cut the claim of significance; keep the demonstration of it. Carve-out: when the importance-claim is the *topic sentence* the following lines immediately substantiate, it is structure and stance, not an unpaid note; keep it. The cut is for significance asserted and then left uncashed.

8. **Inert hedges.** Qualifiers whose removal leaves the claim's scope unchanged, but only when they are clause- or sentence-sized; a single stray qualifier is `/tighten`'s. CRITICAL EXCEPTION: do not cut *content* hedges. Fallibilism, scoped conditionals, and calibrated uncertainty are often the argument itself ("held while it stands, never certified," "a credence strictly below one"). Cutting those degrades the claim; that is not trimming.

9. **Redundant examples.** A second or third example that lands the same point as the first. Keep the strongest, or one that also does extra work (introduces a term, sets up the next section). But a *gradient* (loose to strict, cheap to expensive) is not redundant, and accumulation that establishes *generality across cases* changes the claim's weight, not just its illustration, so it stays. Boundary case with #3: a claim restated in a more abstract register (concrete, then general) is a gradient to keep only if the abstract version carries new generality; if it merely re-says the concrete point at altitude, the marginal information is zero and it is self-recap, cut. The invariant is the tiebreaker, not the surface shape.

## Hard keeps (never propose cutting)

- The thesis and its load-bearing gloss.
- Load-bearing precise terms. Never swap a precise term for a vaguer-but-shorter one; that is degrading, not trimming.
- The deliberate concession or posture (e.g. "every primitive is borrowed" when the synthesis is the contribution); concessions and modesty also carry credibility, which is a function.
- Falsifiers, kill conditions, and the evidence/examples that make a claim checkable.
- Content hedges (the fallibilism exception above).
- Voice that carries stance, precision, or authority, distinct from ornament *and from volume*. Emphatic repetition that adds no argument is filibuster, not voice; cut it (the invariant has the full test).
- Reader-orientation the *target audience* actually needs. Audience is a parameter: a derivation an expert skips is one a general reader requires. Conversely, for a machine- or spec-facing document with no human reader, this keep relaxes and trimming can be aggressive.
- Accumulation that changes weight, not just content: a second example that establishes generality, repetition that builds emphasis the argument uses. Mere duplication still goes; this is the case where the repetition *does* something.

## Process

1. Read the file. Note the word count.
2. For each section, scan for the patterns and run the absence test on every candidate. On a long document, dispatch a subagent (Agent) to return proposals rather than reading the whole thing inline; pass it this skill's test, the patterns, and the hard-keep list.
3. **Apply**, with a separation of authority borrowed from `/not-but`:
   - **Cut decision** follows the absence test. Once a passage fails it, the passage goes. Do not re-litigate from attachment to the prose.
   - **Graft phrasing** is orchestrator discretion. Where a cut passage had good rhetoric, the orchestrator decides where and how to relocate it onto an adjacent essential point, with the full-document context the test-runner lacked.
   - **Re-classification as essential** is the user's call, not the orchestrator's. If you believe a failed passage should survive, surface it in the report; do not quietly keep it.
4. **Report**: word count before/after; cuts grouped by the patterns; for each, the one-line "argument survives because ___"; any rhetoric grafted, and where to. Mark cuts you had reservations about with `⚠` so the user sees them first.
5. **Verify**: re-render / re-read the touched passages. A cut that orphaned a pronoun, a transition, a setup, or a cross-reference is a miss, not a trim; fix the seam. Watch the half-cut hazard with self-scoping that pairs with a sibling link ("this post covers X, the sibling covers Y"): cutting the self-scoping half can leave a dangling link with no stated reason to be there. Cut the whole contrast or keep it whole, never half.

## The contract: idempotent and monoidal

`/trim` satisfies the same contract as the other pipeline skills, and here the contract is a safety rail as much as a guarantee.

**Idempotent.** `trim(trim(x)) == trim(x)`. A second pass over trimmed prose should find nothing, because cruft, once removed, stays removed. Convergence in one or two rounds is normal.

**Non-convergence is the over-cut alarm.** A third pass that still finds cuts means trim has stopped removing cruft and started eating connective tissue, examples, or emphasis the argument needs: the test is being run too loosely. So stop *automatic* cutting at the third pass; treat any further candidate as a review-only proposal justified against force, clarity, evidence, scope, and reader-orientation, never on bare argument-survival. (A long, repetitive draft can genuinely hide cruft that deep, so slow down and justify, do not cut on reflex.) Idempotence is thus both the proof a pass converged and the rail that catches over-cutting, the failure mode the hard-keeps and strengthened test exist to prevent.

**Monoidal.** Because each pass is idempotent, `/trim` composes with `/tighten` and `/not-but` to a stable fixed point: run them in any order, repeatedly, and the prose stops changing. The pipeline converges regardless of path, so trim slots anywhere in it without ordering hazards beyond the efficiency note below.

## Composability

- **Standalone**: `/trim <file>` for any prose where length is the problem and the cause is structural, not wordy sentences.
- **Order with siblings**: run `/trim` *before* `/tighten`. Trim removes whole passages; tightening the survivors is cheaper than tightening sentences you are about to delete. `/not-but` can run any time.
- **Inside `/copyedit`**: slot `/trim` as an argument-level pass ahead of the word-level `tighten` step when a draft is long because it says too much, not because it says it in too many words.
