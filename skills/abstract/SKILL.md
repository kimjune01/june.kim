---
name: abstract
description: Diagnose and fix an abstract that is a "condensed argument" instead of a real abstract. An abstract is problem / approach / result with the result STATED (the number, the finding), not the reasoning marched step by step. From John Laird's reviewer feedback on June's arXiv papers.
argument-hint: <file_path>
allowed-tools: Read, Edit, Grep, AskUserQuestion
---

# Abstract: problem / approach / result

An abstract is **not a condensed argument.** That is the most common failure (John Laird, reviewing June's papers: "rewrite the abstract as a real abstract, problem/approach/result, instead of a condensed argument"). The bad abstract marches the reasoning step by step, problem then *because* then *so* then *therefore*, and never states the result. A reader finishes it knowing what you *argue about*, not what you *found*.

It is also not an introduction, not a teaser that withholds the result to make them read on, and not a table of contents ("we discuss X, then Y, then Z").

It is three moves: **problem, approach, result.**

## The three moves

- **Problem.** The gap and why it matters, in one or two sentences. Crisp, not a literature review. Name the thing your work is about and the hole in it.
- **Approach.** One sentence that is, in effect, *"This paper introduces / reads / recasts / builds X."* Name the contribution as an act. If this sentence is missing, the abstract has no approach, only assertion.
- **Result.** The concrete finding, **stated, with its number.** The headline figure (N programs, the falsifiable bet, the artifact you deliver) goes in the abstract, not buried in the body. A reader should be able to repeat your finding from the abstract alone.

## The diagnostic

Read the abstract, then run three tests. Any fail means rewrite.

1. **Can you state the result, with the number?** If the abstract says "we show that …" or "success measures X" but never gives the count, the magnitude, the bet, or the artifact, the result is *promised, not stated.* Fail.
2. **Is there a "this paper does X" sentence?** If the contribution appears only as a chain of "because … so …", there is no approach. Fail.
3. **Does it march the argument?** Count the inferential connectives (because, so, therefore, thus, hence). A real abstract has few; a condensed argument is built from them. Three or more in a short abstract is the tell. Fail.

## Process

1. Read the abstract, and the paper body if needed to recover the headline result and its number.
2. Run the diagnostic. Report which tests fail, quoting the abstract.
3. If it passes all three, say so and stop. Do not rewrite a working abstract.
4. If it fails, rewrite to problem / approach / result:
   - Lead with the problem and the gap.
   - Add the explicit "This paper …" approach sentence.
   - State the result with its number; pull the figure from the body if the abstract omits it.
   - Restructure, do not retone: keep the author's voice and any one iconic line.
5. Length discipline: one paragraph, roughly 150 to 250 words. An abstract that needs more is carrying body material.

## Calibration

Laird-approved (problem / approach / result, result stated), on june.kim:
- *What Cannot Be False Cannot Be True* and *Verifiable Knowledge*: each opens on the problem, has a "This paper recasts / introduces …" sentence, and ends on the stated result (the two disjoint graphs; the one falsifiable bet).

The failure mode, before fixing:
- *ProgramBench Measures Recall* once opened "ProgramBench asks an agent to … We grant … Because … Some behaviors … Reproducing these requires … so success measures recall." A compressed section one, with the headline number (21 recall-gated programs) never stated. The fix put the number in the abstract and added the "This paper reads the suites and classifies every assertion" approach sentence.

## Rules

- State the result. If you cannot state it, the work is unfinished, not the abstract.
- Numbers go in the abstract. The reader decides whether to read on from the finding, not from the promise of one.
- Do not withhold for suspense; an abstract is not a trailer.
- Stay above the introduction. The abstract carries the *result*; section one carries the *mechanism*. A sentence that re-derives why (the reasoning chain, the finite-sample argument, the step-by-step), or any detail that also appears in the intro, belongs there, not in the abstract. Cut the overlap.
- Restructure, do not retone. Keep the voice and the one iconic line.
- Honor the project's writing invariants (em-dash budget and the rest); run /copyedit after if the rewrite needs polishing.
