---
variant: post-medium
title: "I tried to build null-flex"
tags: reflecting, methodology, projects
---

Replace the author's name in a citation with a single number: the fraction of their publications where the registered primary outcome was met. A null-flex ratio. [Science on Trial](/2026-04-19-science-on-trial) gestured at it. I wanted to build it.

A consistent 100% positive rate across many trials is either filtering or a specialty where nothing fails. A ratio that moves with the evidence reads honest. The move reweights trust toward track record and away from institution. Clean, simple, shippable.

So I opened a new directory and started.

### The setup

I wrote a preregistration before any code, because the post argued pre-registration is the thing. Eighty percent precision and recall on both `met` and `not_met` classes from a held-out RCT sample. Failure if any of the four marginals clearly missed 0.70. Sequential Bayesian design with adaptive batches and predictive-probability futility. I ran the prereg through [codex](/reading/codex) for six adversarial rounds and got it down to a document I couldn't easily find holes in.

Then I wrote the harness: a classifier runner with SHA-locked inputs, prompt and config hashes per row, parse-retry logic, drift quarantine, contiguous-resume enforcement, attempt-level audit trails. A scorer with Beta marginals, Dirichlet rows, joint success probability via Monte Carlo. A futility simulator that reapplied the decision rules inside each of ten thousand simulated continuations. An orchestrator that refused to advance past a terminal decision.

Eleven rounds of codex review. Forty-four findings. All addressed.

Meanwhile the data pull ran in the background. ClinicalTrials.gov returned 39,595 completed randomized trials with posted results. After prospective-registration, primary-outcome, PubMed-linkage, and abstract-retrievability filters, 1,938 trials survived. 867 met, 1,071 not met. 44.7% positive, a healthier class balance than I'd feared.

The instrument took a day and a half to build, two hours to run. All to produce a failure decision I didn't see coming.

### Batch 1

I ran the first batch on Claude. Thirty trials. The scorer printed this:

```
decision: failure
ambiguous_rate: 0.66
P(met_recall < 0.70): 0.9998
P(not_met_recall < 0.70): 0.9997
```

Two thirds of abstracts classified as `ambiguous`. Of the ten trials where the classifier committed, it was right eight times. Eighty percent on commits, right at the prereg bar for precision. But the commit rate collapsed. An abstract the classifier can't commit on counts as a recall miss, which caps recall near 33% no matter what. The Bayesian rule fired failure correctly and early.

I sat with that. A model that could read was refusing to read, two out of every three abstracts. It wouldn't say.

### What the classifier was actually doing

The auditor prompt was explicit: *if the abstract is unclear, hedged, or spin-heavy, prefer the `ambiguous` class. Do not try to infer what the authors meant if the abstract does not clearly say it.* The model followed instructions.

But for trials with posted results, the registry reports primary_outcome_X, p-value, CI, pass/fail on the pre-specified threshold. Far less ambiguous than the abstract. Same trial, same authors, same moment, and the structured record says the answer clearly where the abstract blurs it.

This is a known thing in the literature. [Boutron 2010](https://pubmed.ncbi.nlm.nih.gov/20501928/) found spin in 58% of RCT abstracts with non-significant primaries. [Yavchitz](https://pubmed.ncbi.nlm.nih.gov/26845744/), Lazarus, and others followed up. Authors frame. They emphasize the clinically interesting secondary, call a p-value of 0.07 a trend, foreground the post-hoc subgroup. Each move is individually defensible as craft. Aggregated over a literature, they produce a systematic gap between what the registries know and what the abstracts say.

My classifier wasn't broken. It was picking up the pattern Boutron measured by hand: abstract text that doesn't cleanly support classification of the registered primary. When the model said `ambiguous`, it was telling me the abstract itself wouldn't commit. That's diagnostic, not defective.

I'd been optimizing for a premise the literature doesn't cooperate with: that an LLM could read an abstract and tell me what the trial actually found. The abstract is what the author wanted me to see. The registry is what actually happened. They diverge. My tool was measuring the divergence and I was reading it as a failure.

### The pivot

I'd spent thirty-six hours of setup and two of runtime to build a Bayesian harness that detects a null from thirty trials. If I'd skipped it and run thirty abstracts through the classifier with an auditor prompt, I'd have learned the same thing in an afternoon. The instrumentation was ceremonial, not load-bearing. The signal was clear enough to see at N=30.

More importantly: if abstracts and registries diverge systematically, an abstract-derived author ratio inherits the divergence. Computing a null-flex ratio from abstracts means computing a ratio of what the authors told readers. The ratio would be a spin ratio, not a track record. Worse, the authors who spin are the ones it would most need to catch, and they're precisely the ones whose abstracts would read as ambiguous. The tool would be least accurate exactly where it mattered most.

The registry dodges this. For trials with posted results, CT.gov carries the primary-outcome status as structured fields, parseable by a script rather than a language model. I'd been trying to reconstruct from the abstract a signal the registry already contained. The cleaner architecture reverses that: compute ratios from the registry, then ask what the abstracts add.

And once I looked at the problem that way, the null-flex idea pivoted again. An author-level ratio still makes sense, but it's not the sharpest shape. If the abstract-registry gap is where the pathology lives, the venue that published the spun abstract is implicated in a way the anonymous author isn't. A per-trial divergence flag surfaces the gap at the point of reading. A per-venue representativeness score, measuring how far each journal's published RCT portfolio deviates from the registered-trial ecology in its specialty, aims at the filter rather than the filtered.

Codex pushed back when I framed this as moral. Authors are strategic, venues create incentives, "the real evil is the venue" is emotionally satisfying but analytically sloppy. Fair. The product narrowed into a cell-level score: journal × specialty × trial-type, observed versus expected registered-null rate, with explicit refusal to claim editorial intent. Five more rounds until codex called it clean.

I haven't built it yet. The [spec](https://github.com/kimjune01/null-flex/blob/master/VRI_SPEC.md) is eight weeks of work and needs a clinical trialist collaborator. Whether it ships depends on finding an institutional host for the political heat — journals don't like being measured. A personal repo is the wrong address for the first lawyer letter. [Bennett](https://www.bennett.ox.ac.uk/) or [ProPublica](https://www.propublica.org/) is the right one.

### What I actually learned

Three things the classifier run taught me, none of which I'd have bet on going in.

One: build the instrument that can kill the idea, not the one that can prove it. I spent thirty-six hours on a Bayesian harness for a signal that showed up in thirty trials. The sophisticated success machinery was for the 80% bar I didn't get near. For detecting failure, N=30 plus a confusion matrix would have been enough. Next time I'll start with the minimum falsifier.

Two: preregistration works when you don't want it to. The prereg rule fired failure earlier than I wanted, on evidence I would have talked myself past if I'd been eyeballing it. I'd have said "let's see what happens at 100 trials" and rationalized another fifty. The rule didn't care what I wanted.

Three: the instrument you build is usually telling you something about the question, not just the answer. My abstention rate wasn't a classifier quality metric. It was a measurement of how much of its own primary outcome an RCT abstract actually conveys. That's the same thing the Boutron literature has been saying for over a decade. My tool found it accidentally while trying to measure something else.

The null-flex attempt failed as a product. As a diagnostic, it worked better than anything else I'd built that week.

The repo is at [github.com/kimjune01/null-flex](https://github.com/kimjune01/null-flex), with the full audit trail: the thirty trials, the confusion matrix, the raw responses. The pivoted spec is the document I'm still staring at.
