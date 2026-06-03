---
to: Sazan Khalid <sk2153@georgetown.edu>, Amit Arora <amiarora@amazon.com>
from: June Kim <kimjune01@gmail.com>
subject: Heads-up — citing your Cognitive Memory Manager paper
date: 2026-05-28
---

Hi Sazan and Amit,

Reading your "From Observed Reasoning to Stable Skills" (https://openreview.net/forum?id=yCsHQnvvWY) on the day it dropped (2026-05-26) put me in an interesting spot; I had been working on a paper that lands in adjacent territory and was finalizing the draft 24 hours later. I wanted to send a heads-up before the preprint goes up.

What I'm citing. The paper is "The Methodeutic Harness on SWE-bench Pro: hypothesis graphs as agent semantic memory, grounded in Peircean methodeutics."
  Draft: https://june.kim/the-methodeutic-harness-on-swebench-pro
  PDF: https://june.kim/assets/methodeutic-harness-paper.pdf
It documents a runnable LLM-agent harness that types each pipeline stage by Peircean reasoning mode (recon = abduction, craft = deduction, audit = induction) and uses a persistent typed hypothesis graph as the semantic-memory substrate, on SWE-bench Verified (426/438) and Pro (in-flight).

Where you appear. CMM is named in the abstract as the closest SE-targeted precedent, in section 1 as one of three independent recent papers reaching for typed-reasoning primitives, and in section 8.2b with a structured comparison along five axes: prior requirement, when typing fires, edge semantics, write contracts, temporal scope. The comparison ends in a "complementary by construction" framing: the methodeutic harness produces hypothesis-graph traces; CMM's graduation algorithm could consume them to extract per-repo skills downstream.

Why I'm writing. Two reasons:

1. Correction window. If the comparison misframes your design (wrong axis, wrong reading of diagnose / pitfalls / search-memory, wrong characterization of the typing locus, anything), I'd rather hear it before the preprint settles. The 8.2b text is on the draft page linked above; any correction folds into the next versioned artifact.

2. Possible collaboration vector. The complementary-by-construction reading isn't rhetorical; the ~380 hypothesis-graph files we've publicly committed at github.com/kimjune01/sweep/tree/main/repo-hypotheses are exactly the corpus shape CMM's graduation algorithm could consume. If you'd be interested in a small chain-experiment (feed our traces through your graduation pipeline, see what SKILL.md falls out), I'd be game to coordinate.

The Pro run is still in flight; final numbers land in the next week or two. No rush on a reply; the preprint posts after Pro terminates.

Thank you for the work. Running into a paper that arrives at the same conceptual neighborhood from a different lineage is the best kind of surprise.

June


---

Notes (not for sending):
- Verified author names via OpenReview: Sazan Khalid (Georgetown), Amit Arora (Amazon).
- Tone: peer-to-peer, not gatekeeping or apologetic. They're senior researchers; we're not. The leverage is the receipt-density of our work, not the institutional standing.
- The "complementary by construction" framing is real; it's in section 8.2b verbatim and reads as collaborative even if they don't reply.
- If they reply and the comparison is wrong on a specific axis, fold the correction in immediately. This is the cheapest possible peer review.
- If they ignore the email entirely, no harm done; the cite stands either way.
- Don't send before reading their full paper carefully once more; the heads-up is only as credible as the 8.2b summary it points to.
