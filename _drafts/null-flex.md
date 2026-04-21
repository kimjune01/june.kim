---
variant: post-medium
title: "I tried to build null-flex"
tags: reflecting, methodology, projects
---

After finishing [Science on Trial](/2026-04-19-science-on-trial), I wanted to build one of the fixes it gestured at. The idea sat cleanest in my head so I started with that one. Replace the author name in a citation with a single number: the fraction of that author's publications where the registered primary outcome was met. A null-flex ratio.

A scientist with a 100% positive rate is filtering or omniscient. A scientist at 0.58 is publishing what they find. A reader gets something calibrated where they currently get credentials. The move reweights trust toward track record and away from institution. Clean, simple, shippable.

So I opened a new directory and started.

### The setup

I wrote a preregistration before any code, because the post argued pre-registration is the thing. Eighty percent precision and recall on both `met` and `not_met` classes from a held-out RCT sample. Failure if any of the four marginals clearly missed 0.70. Sequential Bayesian design with adaptive batches and predictive-probability futility. I ran the prereg through [codex](/reading/codex) for six adversarial rounds and got it down to a document I couldn't easily find holes in.

Then I wrote the harness. A classifier runner with SHA-locked inputs, prompt and config hashes per row, parse-retry logic, drift quarantine, contiguous-resume enforcement, attempt-level audit trails. A scorer with Beta marginals, Dirichlet rows, joint success probability via Monte Carlo. A futility simulator that reapplied the decision rules inside each of ten thousand simulated continuations. An orchestrator that refused to advance past a terminal decision.

Eleven rounds of codex review. Forty-four findings. All addressed.

Meanwhile the data pull ran in the background. ClinicalTrials.gov returned 39,595 completed randomized trials with posted results. After prospective-registration, primary-outcome, PubMed-linkage, and abstract-retrievability filters, 1,938 trials survived. 867 met, 1,071 not met. 44.7% positive, a healthier class balance than I'd feared.

The whole instrument took about a day and a half to build and two hours to run. All of it to produce a failure decision I didn't see coming.

### Batch 1

I ran the first batch on Claude Sonnet 4.6. Thirty trials. The scorer printed this:

```
decision: failure
ambiguous_rate: 0.53
P(met_recall < 0.70): 0.99
P(not_met_recall < 0.70): 0.9997
```

Fifty-three percent of abstracts classified as `ambiguous`. Of the trials where the classifier committed, it was right ten times out of fourteen. That's 71% accuracy on commits, which isn't great, but isn't the killer either. The killer was the abstention. An abstract that the classifier can't commit on counts as a recall miss. Half the trials being in that bucket means recall is structurally capped near 47% no matter what. The Bayesian rule fired failure correctly and early.

My first thought was that Sonnet was being lazy.

I re-ran on Opus 4.7 expecting the stronger model to push the abstention rate down. It did the opposite.

```
decision: failure
ambiguous_rate: 0.66
```

Opus hedged on two thirds of abstracts. On the ten trials where it committed, it was right eight times. Eighty percent, exactly at the prereg bar. But the commit rate collapsed. Stronger model, more abstention, less data.

I sat with that for a minute. It's counterintuitive in the wrong direction. The whole AI industry's pitch is that the bigger model sees more, and here the bigger model was refusing to say more. Better at being unwilling.

### What the classifier was actually doing

The auditor prompt told Opus: *if the abstract is unclear, hedged, or spin-heavy, prefer the `ambiguous` class. Do not try to infer what the authors meant if the abstract does not clearly say it.* Opus followed instructions.

But the registry knows what happened. The registry is structured. The posted results table says primary_outcome_X, p-value, CI, pass/fail on the pre-specified threshold. No ambiguity in the registry. Same trial, same authors, same moment, and the registry says the answer clearly while the abstract doesn't.

This is a known thing in the literature. [Boutron 2010](https://pubmed.ncbi.nlm.nih.gov/20501928/) found spin in 58% of RCT abstracts with non-significant primaries. Yavchitz, Lazarus, and others followed up. Authors frame. They emphasize the clinically interesting secondary. They call a p-value of 0.07 a trend. They foreground the post-hoc subgroup. Each move is individually defensible as craft. Aggregated over a literature, they produce a systematic gap between what the registries know and what the abstracts say.

My classifier wasn't broken. It was a spin detector. Opus saw the same thing Boutron saw, except at scale and in real time. When it said `ambiguous`, it was telling me the abstract text didn't support the registry's structured claim. That's diagnostic, not defective.

I'd been optimizing for a premise the literature doesn't cooperate with: that an LLM could read an abstract and tell me what the trial actually found. The abstract is what the author wanted me to see. The registry is what actually happened. They diverge. My tool was measuring the divergence and I was reading it as a failure.

### The pivot

I'd spent thirty-six hours of setup and two hours of runtime to build a Bayesian harness that could detect a null result from thirty trials. If I'd skipped the harness and just run thirty abstracts through Opus with an auditor prompt, I'd have learned exactly the same thing in an afternoon. The instrumentation was ceremonial, not load-bearing. The signal was enormous and obvious.

More importantly: if abstracts and registries diverge systematically, an abstract-derived author ratio inherits the divergence. Computing a null-flex ratio from abstracts means computing a ratio of *what the authors told readers*, not of *what the registries know*. The ratio would be a spin ratio, not a track record. Worse, the authors who spin are the ones it would most need to catch, and they're precisely the ones whose abstracts would read as ambiguous. The tool would be least accurate exactly where it mattered most.

The registry dodges this. CT.gov has the met/not_met status already, structured, for every trial with posted results. No classifier needed. I'd been trying to reconstruct from the abstract a signal the registry already contained — because the *Science on Trial* framing had trained me to think about authors first. The cleaner architecture reverses that: compute ratios from the registry, then ask what the abstracts add.

And once I looked at the problem that way, the null-flex idea pivoted again. An author-level ratio still makes sense, but it's not the sharpest shape. If the abstract-registry gap is where the pathology lives, the venue that published the spun abstract is implicated in a way the anonymous author isn't. A per-trial divergence flag surfaces the gap at the point of reading. A per-venue representativeness score, measuring how far each journal's published RCT portfolio deviates from the registered-trial ecology in its specialty, aims at the filter rather than the filtered.

I ran the venue hypothesis past codex and got told, legitimately, that "the real evil is the venue" is emotionally satisfying and analytically sloppy. Authors are strategic; venues create incentives; the venue didn't move their fingers. Correct. So the product became narrower: a Venue Representativeness Index, a per-`journal × specialty × trial-type` cell-level deviation between observed and expected registered-null rates, with explicit refusal to claim editorial intent. Dry arithmetic. Hierarchical Bayesian model, covariate adjustment, direction-of-bias on every limitation. Five more rounds of codex review until I couldn't find a hole.

I haven't built it yet. The [spec](https://github.com/kimjune01/null-flex/blob/master/VRI_SPEC.md) is eight weeks of work, including a clinical trialist for the 50-trial manual audit. Whether I ship it depends on finding an institutional host willing to take the political heat; journals don't like being measured, and the kind of legal response that lands in a personal inbox lands differently at Bennett Institute or ProPublica.

### What I actually learned

Three things the classifier run taught me, none of which I'd have bet on going in.

One: the stronger model was more honest. I expected Opus to commit where Sonnet hedged. Opus hedged more, and was more accurate when it did commit. The capability was always there to read the abstract. What Opus added was the willingness to say "this text doesn't tell me." That's a real property of models as they get better. They understand the difference between what's said and what's meant, and they refuse to pretend otherwise.

Two: preregistration works when you don't want it to. The prereg rule fired failure earlier than I wanted, on evidence I would have talked myself past if I'd been eyeballing it. I'd have said "let's see what happens at 100 trials" and rationalized another fifty. The rule didn't care what I wanted.

Three: the instrument you build is usually telling you something about the question, not just the answer. My abstention rate wasn't a classifier quality metric. It was a measurement of how much of its own primary outcome an RCT abstract actually conveys. Which is the same thing the Boutron literature has been saying for over a decade. My tool found it accidentally while trying to measure something else.

The null-flex attempt failed as a product. As a diagnostic, it worked better than anything else I'd built that week.

The repo is at [github.com/kimjune01/null-flex](https://github.com/kimjune01/null-flex), with the full audit trail including the thirty trials and both models' confusion matrices. The pivoted spec is the document I'm still staring at.
