# Issue draft — UKGovernmentBEIS/inspect_ai

**Title:** Detect out-of-scope sandbox file changes

---

> **FILED** as UKGovernmentBEIS/inspect_ai#4461 on 2026-07-10.


## Summary

Inspect grades an agentic sample by what the scorer inspects at the end and asserts nothing about the rest of the sandbox state the agent touched on the way. A sample can score 1 after the agent both completed its task and deleted, overwrote, or corrupted state the task never named. This is the frame condition from program verification, and SWE-bench's [PASS_TO_PASS](https://arxiv.org/abs/2310.06770) made the same guarantee routine. Inspect's agentic evals have the fail-to-pass half and nothing playing the pass-to-pass role, so two agents at the same score can differ without bound in what they wrecked getting there.

It is measurable on shipped benchmarks. A construct-validity audit of Terminal-Bench 2.1 ([writeup](https://june.kim/terminal-bench-frame), filed as [terminal-bench#1459](https://github.com/harbor-framework/terminal-bench/issues/1459)) found 40 of 83 gold-passing tasks still score 1 after a careless deletion inside their own workspace, and every one passing after off-task user assets are wiped. It generalizes to any eval that grades environment state, which is most agentic evals.

## Proposal

`scope_check(wrapped, roots, allowed, gate)` is an opt-in solver that snapshots the watched roots before and after the wrapped solver runs, and records the paths changed outside an allowed footprint (git-style globs) as a `scope_check` score. It is observational by default (an unscored diagnostic in the eval log, so no existing eval's score moves); with `gate=True` an out-of-scope change scores the sample INCORRECT.

The snapshot-and-diff pattern is already proven in-tree for checkpoint/resume (`util/_restic/ops.py`), and the sandbox lifecycle plus the `sandbox()` accessor give clean attachment points. A self-contained per-sandbox manifest keeps a first version dependency-light; a reusable snapshot API could be a later proposal.

## Related

#3770 (verifiable-task taxonomy on `@scorer`) and #4116 (completion proof for tool-using evals) concern what the scorer checks and whether the task ran; this concerns what the agent changed outside what the scorer checks.

I have a working implementation with tests and a Docker-sandbox receipt (an agent that completes its task and deletes a planted off-task file is scored INCORRECT, with the deleted path named), and I'd like to open it as a PR. Filing here first per CONTRIBUTING to get your read on whether the primitive belongs in core before I claim it.
