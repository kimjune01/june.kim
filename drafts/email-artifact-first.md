# Artifact-first contact (Layer 2)

The note to a person whose work you build on, test, or audit. Rules that make it survive the noise filter:
- Lead with the runnable/checkable thing, not with yourself.
- Prove it could only have come from you and could only have been sent to them (specificity = humanity).
- No ask in the first touch beyond "curious what you think." The relationship is the goal; funding/jobs
  come later, through it, not in line one.
- Short. One screen. A link they can verify in ten minutes beats three paragraphs of claim.

---

## Variant A — to the SWE-bench Pro team (you audited their benchmark)

Subject: I audited all 728 public SWE-bench Pro tasks for determinacy

Hi [name],

I ran a determinacy audit over all 728 public SWE-bench Pro tasks and found something you might want: a
large share are one-shot from the spec, and there's a ~15% floor that grades unstated author intent
undiscoverable from the materials. Repo with per-task classification and a regrade script here: [link].
Run it in a few minutes; I built it to be checked, not taken on my word.

Separately I resolved 694/728 under the official grader, but I'd disclaim that to you first: tests were
the solving oracle, so it measures translation, not discovery. That's actually the finding I care about,
that discovery is the part the benchmark can't isolate.

Not asking for anything, just thought the people who built Pro would want the audit. Curious whether the
determinacy split matches your intent for the set.

[June] · june.kim · github.com/kimjune01

---

## Variant B — to the DeepMind "verification crisis" authors (you built a mechanism for their problem)

Subject: A working mechanism for the verification crisis you named

Hi [name],

Your position paper named the verification crisis for epistemic agents cleanly, and I think I have a
running mechanism for one corner of it. The hypothesis graph records an agent's reasoning as claims bound
to executable trials, so a conclusion is checkable by re-running its recorded trial rather than trusting
the model's report. On a contamination-free, post-cutoff bug, externalizing that check carried a weaker
model past what the strongest released model reached alone. Preregistered and regradeable: [link].

I'd genuinely value your read on where it breaks. Writeups at june.kim if useful; happy to walk through
the experiment live.

[June] · june.kim · github.com/kimjune01

---

## Variant C — generic (adapt the first sentence to the specific work)

Subject: [the specific thing you did to their work]

Hi [name],

[One sentence: what of theirs you extended/tested/audited, and the one surprising result.] Repo you can
run: [link]. I built it to be checked rather than believed.

[One sentence on the broader work, with the honest caveat that makes it credible.]

Not after anything in particular, I just figured you'd want to see it. Curious what you think.

[June] · june.kim · github.com/kimjune01
