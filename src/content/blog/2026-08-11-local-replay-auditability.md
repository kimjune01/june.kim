---
variant: post-paper
title: "Replayable Claims: Epistemic Status Without Trusting the Sender"
tags: coding, epistemology, methodology
---

<!-- pdf-skip -->
[Download the runnable example and its complete inputs](/assets/replayable-claims-example.zip).
<!-- /pdf-skip -->

## Abstract

Knowledge can be accumulated as a quantifiable collection of replayable claims. This extends the proposition that knowledge is buildable: a claim whose grounds can be reconstructed can become a durable unit that another agent checks and builds upon. We propose local replay auditability as the communication requirement for that unit. A claim travels with what lets its receiver derive a verdict, distinguishing true, false, and untrue according to whether inquiry supports it, refutes it, or has earned no verdict. For identified inputs and a deterministic check that completes, replay replaces reliance on the sender's report with a local computation; the adequacy of the check remains open to challenge. The hypothesis graph adds dependencies and versions, allowing the collection to grow, retain refutations, and withdraw stale warrant. A self-contained example and a bounded benchmark-audit replay demonstrate the local checking step on which that accumulation depends.

## Entitlement loss at the boundary

An agent finishes an inquiry and reports a verdict. A second agent receives that verdict and must decide whether to use it. A score, label, or signed execution log can tell the receiver what the sender endorses. Without an independent check, it cannot settle whether the encoded result holds.

The communication problem persists even when the sender did excellent work. If the evidence and procedure are lost at the boundary, the recipient must trust the report or reconstruct the inquiry. The proposal is to preserve the means of checking at the granularity of the claim being reused. The sender transmits two things: **the claim, and whatever the receiver needs to derive its claim-level verdict**. We call this requirement *local replay auditability*. Local means that the sender's report is not the authority for the resulting verdict; it does not mean that every dependency resides on the receiver's machine.

[*Truth Is Buildable*](/truth-is-buildable) argues that knowing requires a build: a claim has grounds whose derivation can be inspected. The extension here is accumulation. **Knowledge can be accumulated as a quantifiable collection of replayable claims.** Each claim retains the means of establishing its status, so the collection can outlive the agents and conversations that produced it.

A replayable claim is the unit that makes this possible. Another agent can check it, add a result of its own, continue an unfinished investigation, or discover that a stored result no longer applies. Once the grounds survive the handoff, checked work can become someone else's premise.

The [hypothesis graph](/the-hypothesis-graph-semantic-memory-methodeutics) develops this into shared memory: claims carry trials, dependencies, and versions, so agents can divide an inquiry and revise its conclusions without reconstructing everything. This paper specifies the communication step that makes such reuse checkable. It asks what must travel with a claim, what verdict the receiver has earned, and how far that verdict entitles the receiver to proceed.

## What must cross the boundary

A replayable claim may carry a proof and checker, a test and software environment, or data with an analysis procedure. No single file schema fits all three. The receiver nevertheless needs answers to four questions.

| Obligation | What the receiver must be able to establish |
|---|---|
| Claim and scope | Which proposition is being checked, about which object and time? |
| Input identity | Which artifacts and dependencies does this particular check use? |
| Decision procedure | What operation yields support or refutation, and what counts as a valid completion? |
| Trust boundary | Which runtime, observations, assumptions, and access conditions remain outside that operation? |

These are information requirements, not mandatory fields. Shared context can supply an input or procedure. Conversely, a URL alone may fail to identify a changing artifact. A content hash fixes bytes relative to a declared identifier; it does not certify who collected those bytes or whether the collection was complete. A stored measurement permits replay of an analysis, not a repetition of the historical event that produced it.

The receiver first resolves the claim's scope and required inputs. It then checks the applicable identity and execution preconditions, inspects or accepts the proposed decision procedure, and runs it. Only a valid completion yields a verdict. Missing evidence, a different input version, a timeout, or a runtime error leaves the check unresolved. Such failures are not evidence against the claim unless the claim itself concerns that failure: a program crashing can refute a claim that it does not crash, but a broken test harness need not refute a claim about the program.

The procedure must expose an outcome that would count against the claim. Attaching a program that always returns success makes the output executable without making the intended claim answerable to evidence. Inspecting this connection remains a substantive part of verification.

## Receiver-relative status

A check that refutes a claim and a check that yields no verdict require different protocol outcomes. Calling an unchecked claim false would turn missing evidence into a refutation; calling it true would award entitlement without a check. The protocol therefore needs a third status.

**Untrue means no verdict has been earned by this receiver. It does not mean false.** True and false record the two verdicts of a completed check; untrue records the absence of either, including a check not yet run. These statuses describe the receiver's entitlement under the declared check and context, rather than three intrinsic truth values of the world.

| Receiver's inquiry | Status under the declared check |
|---|---|
| Preconditions hold; the check supports the claim | **True** |
| Preconditions hold; the check refutes the claim | **False** |
| No valid verdict is available | **Untrue** |

The terminology follows [*What Cannot Be False Cannot Be True*](/what-cannot-be-false-cannot-be-true): entitlement is warrant earned through inquiry, conditional on the check's scope and assumptions. The third status preserves that requirement even when an unchecked claim happens to be correct. It also preserves unfinished inquiry: an untested hypothesis remains open to investigation, while a refuted hypothesis records an alternative already ruled out under the declared check.

Two receivers can have different statuses because one can run the check and the other cannot. They need not disagree about reality. A previous passing result remains a record of that earlier inquiry; a changed artifact or unavailable service does not retroactively refute it. A claim about the current state requires a current check. For a historical claim, the evidence must continue to identify the historical object.

Status therefore needs its scope attached. “True under this check on these inputs” must not silently become “the broader claim is correct.” Conflicting checks must retain their separate procedures, contexts, and results; this three-way status does not adjudicate between them.

## The guarantee and its boundary

Two questions are compressed into a bare verdict:

1. Does the declared procedure yield the reported result on the identified inputs?
2. Does that procedure adequately test the substantive claim?

Replay can answer the first locally. It leaves the second available for inspection and dispute.

The conditional argument is simple. Fix a check, its identified inputs, and the execution assumptions needed for a deterministic verdict. If a receiver obtains those inputs and the check completes validly, its verdict follows from that computation. Changing the sender's name, confidence, or reported result does not change it. Two conforming receivers obtain the same verdict under these assumptions. The verdict follows the declared computation across the agent boundary.

The independence is limited to the sender's report of this result. Replay does not establish that the sender actually ran the procedure earlier, that the inputs faithfully represent an external event, or that the sender disclosed all relevant cases. It also does not remove trust in the receiver's runtime or in declared terminal observations. Rather than proving the report honest, the receiver no longer needs that report to determine this result.

Specification uncertainty remains even after a pass. The check may encode the wrong property, omit relevant cases, or rely on a mistaken model of the task. An identical error can reproduce indefinitely. A receiver must either justify the connection between predicate and proposition or state the narrower claim that the predicate actually establishes. Confidence estimates remain useful for uncertain measurements, statistical conclusions, and adequacy judgments; replay replaces their use as a substitute for an available computation.

## Knowledge that can accumulate

A collection grows when an inquiry contributes a claim with grounds another agent can replay. The record identifies the proposition, its scope, its check, and the dependencies under which its verdict holds. Repeating an assertion does not create another result. Replaying an existing claim can renew its warrant; establishing a distinct claim adds something the collection did not contain before.

That makes accumulation quantifiable. For a declared collection, receiver, and context, one can count the distinct claims with current passing checks, the recorded refutations, and the claims still awaiting a verdict. One can also identify which results survive a changed premise and which require renewed inquiry. A refutation contributes a checked result about what failed; the refuted proposition does not become an accepted premise. **Untrue keeps the inventory of proposed claims separate from the inventory of earned results.**

These counts require an explicit rule for claim identity and granularity. Splitting one proposition into ten sentences must not silently become ten units of added knowledge. Counts describe the chosen collection at its stated granularity; the claims retain their different scope, importance, and evidential strength. The measurable object is the collection and its checked state, with every counted result open to inspection.

Accumulation therefore includes revision. The historical record can keep growing while the set of currently warranted claims shrinks after a dependency changes. Preserving both lets an agent distinguish what was learned, what can still be used, and what needs to be checked again. The hypothesis graph supplies the dependency structure for maintaining that distinction.

## From a checked claim to shared inquiry

A receipt makes one claim checkable. The [hypothesis graph](/the-hypothesis-graph-semantic-memory-methodeutics) adds the structure that makes many such claims maintainable. A node binds a claim to its trial and outcome; dependency edges record the premises used; versions identify when that warrant applies. Publication rules admit checked work and reject stale or unsupported updates. Replay supplies the checkable unit, while these additional rules govern its reuse.

Consider a software task with two branches. One agent checks that a parser handles a specified date format. Another checks that an authorization rule rejects an unauthenticated request. An integration claim depends on both. A later agent can enter at the integration node, inspect its prerequisites, and replay the relevant trials without inheriting either worker's whole conversation. Independent branches can proceed concurrently, while the integration step waits for their results.

Now change the date-format requirement. The parser result and the dependent integration claim lose their entitlement for the new requirement; the independent authorization result remains usable under its own conditions. Their earlier receipts still describe what was checked. The update withdraws current reuse without asserting that the historical results were false. Versioned dependencies make that distinction actionable.

The three statuses matter throughout this inquiry. **True** supplies a checked premise within its scope. **False** preserves a refutation that can guide the next hypothesis. **Untrue** keeps a proposed claim from entering as an established premise while allowing the inquiry to retain it. The reason for an unresolved status matters too: an unrun trial, missing evidence, and an unavailable service call for different next steps. The status records the lack of a verdict; the accompanying record tells the next agent what remains to be done.

This also preserves useful failures. The graph records how a refuted hypothesis motivated its successor, so a new worker can see why the inquiry changed direction instead of proposing the same dead branch again. Handoff carries the current frontier of the inquiry together with the checks that produced it.

The hypothesis-graph paper reports a bounded implementation in which receipts, dependency versions, and atomic publication kept stale or unsupported output from becoming current shared knowledge. It demonstrates concurrent work and selective invalidation, without establishing a general speedup. [*Verifiable Knowledge*](/verifiable-knowledge) develops the population-level consequence: a shared canon whose entries remain available for challenge and revision. Extending the collection across many inquiries requires retrieval, root admission, and maintenance. The pairwise protocol supplies the replayable unit; the graph organizes its dependencies; the canon is the accumulated collection.

## One claim, with and without its check

Hold the claim and intended artifacts fixed:

> The byte string `DIGEST` occurs in `hidden_test.diff` and does not occur in `spec.md`.

The filenames refer to the same declared content hashes in each message. A message containing this sentence and “true” leaves a receiver with only the sender's assertion, unless it already has an independent route to the inputs and check. Adding an execution log supplies more detail but still reports someone else's execution. Adding the identified files and the predicate below lets the receiver derive the result. This is an analytical contrast between messages, not an experiment comparing agent populations.

The full decision procedure is small. `pins` is the ordered pair of expected SHA-256 digests for the two files; `None` denotes unavailable bytes.

```python
from hashlib import sha256

DIGEST = b'$2$12$123456789012345678901ufd3hZRrev.WXCbemqGIV/gmWaTGLImm'

def verify(spec, test, pins):
    if spec is None or test is None:
        return 'untrue'
    actual = (sha256(spec).hexdigest(), sha256(test).hexdigest())
    if actual != pins:
        return 'untrue'
    return 'true' if DIGEST in test and DIGEST not in spec else 'false'
```

For a completely self-contained fixture, set `spec = b'Choose a variant.\n'`, `test = DIGEST + b'\n'`, and `pins = (sha256(spec).hexdigest(), sha256(test).hexdigest())`. The result is `true`. These invented inputs demonstrate the predicate; they make no claim about a real benchmark. The literal-occurrence proposition and the code agree by inspection: membership is a byte-substring search over both complete inputs. In this small case, the receiver can also check the result directly from the printed bytes.

| Change to the fixture or its availability | Expected status |
|---|---|
| Supply both original inputs and their pins | True |
| Withhold either input | Untrue |
| Alter an input but retain its original pin | Untrue |
| Put `DIGEST` in both files and pin the new inputs | False |
| Remove `DIGEST` from the test and pin the new inputs | False |

The last two rows are negative controls for newly identified artifacts. They are not valid replays of the original artifact after an undetected change. This distinction prevents an identity failure from masquerading as a refutation. A receiver can obtain true or false only after resolving which object is being checked.

A small accompanying implementation adds file loading and reports an unreadable input as unresolved. All eight implementation checks passed: the original audit case below, a synthetic pass, two synthetic refutations, unavailable bytes, altered bytes, missing files, and a directory supplied in place of a file. These checks establish the illustrated implementation behavior; effects on audit accuracy, time, and agents' decisions remain separate evaluation questions.

## A bounded replay from SWE-bench Pro

The companion determinacy audit of [SWE-bench Pro](https://arxiv.org/abs/2509.16941) reports 109 retained cases across 728 tasks in [*A Determinacy Audit of SWE-bench Pro*](/a-determinacy-audit-of-swebench-pro), combining mechanical evidence and adversarial reading judgments. Those results motivate claim-level evidence, but they are not an evaluation of the communication protocol. Replaying an artifact query, reconsidering a reading judgment, and validating an aggregate defect rate are different tasks.

We use only one artifact-level claim from `ansible_20ef733e`. Its supplied requirements concern selecting a bcrypt identifier in a password-hashing filter. Line 201 of its hidden-test diff contains the exact digest printed above. The complete supplied specification does not contain that byte string. Applying the displayed verifier to the two pinned files returns `true`.

The supplemental bundle contains both complete files, the checker, and its controls. The files are unchanged copies from audit commit `354b3c02a2e055fcd332488600d251338c841380`. Their sizes are 3,102 bytes (`spec.md`) and 13,921 bytes (`hidden_test.diff`). The full content identifiers are:

```text
spec.md:
fae1311400dbefa18a6bddfeb7714786e714da902d39c42b6c79dcb57b98cc07
hidden_test.diff:
667326cd33774402904c22131a3c8ed59e54ab7c118b9eeae6cea20f83d3d0c4
```

This check establishes literal occurrence and absence in these two files. It does **not** establish absence from the base repository, inability to compute the digest, or underdetermination of the benchmark task. A result can be determined by an algorithm without appearing literally in its specification. Establishing underdetermination requires a further argument that the solver's full materials permit alternatives the grader distinguishes. That argument is not supplied by the substring search.

This is the practical value of keeping entitlement attached to a bounded claim: the receiver can accept the byte-level result while withholding judgment on the audit's interpretation. A replayable receipt makes the boundary inspectable; it does not make every inference drawn from the receipt sound. The same burden applies to this audit and to any institutional report. Different audits' headline rates cannot isolate the effect of their communication protocols.

## Relationship to existing verification practices

[Proof-carrying code](https://dl.acm.org/doi/10.1145/263699.263712) already lets a consumer check a producer's artifact against a stated policy. [Verifiable computation](https://doi.org/10.1007/978-3-642-14623-7_25) supplies cryptographic techniques for checking outsourced computation. These establish precedents for verification without accepting a producer's verdict. Local replay does not compete with their formal guarantees or claim a cheaper verification algorithm; either can implement a claim's checking step.

[Reproducible builds](https://reproducible-builds.org/) and [artifact review](https://www.acm.org/publications/policies/artifact-review-and-badging-current) likewise provide concrete ways to check outputs. [W3C PROV](https://www.w3.org/TR/prov-dm/) and [in-toto](https://in-toto.io/) help identify derivations and dependencies. These mechanisms can supply the proposed contract. The emphasis here is on keeping a particular proposition, its decision procedure, and the receiver's resulting status together. Providing provenance is useful even when replay is impossible; it should not be mistaken for a locally derived verdict.

Claim-level auditability is also an explicit objective of [Rasheed et al. (2026)](https://arxiv.org/abs/2602.13855), who propose provenance coverage, provenance soundness, contradiction transparency, and audit effort as evaluation dimensions. [Hans and Bilionis (2026)](https://arxiv.org/abs/2607.02134) make paper claims replication targets tied to evidence and validation checks. Our proposal complements these approaches by specifying what a receiver may carry forward from a check: a supported claim, a refutation, or an unresolved inquiry. That distinction connects claim-level validation to the admission and revision of shared memory.

The epistemology of testimony asks when another's report warrants belief [Hardwig (1991)](https://doi.org/10.2307/2027007). Here the question is narrower: which reliance on a report becomes unnecessary when the receiver can perform the relevant check? The companion [*Verifiable Knowledge*](/verifiable-knowledge) develops the broader contract and its social implications; [*The Hypothesis Graph*](/the-hypothesis-graph-semantic-memory-methodeutics) concerns composition and revision of claim dependencies. The pairwise contract developed here is the point at which a sender's result becomes a receiver's checkable premise. The worked case stands on its own; the graph shows why preserving that contract matters beyond a single verification.

## Limits and evaluation agenda

The protocol is most directly applicable when a claim admits a feasible check over accessible, identified inputs. For nondeterministic procedures, a seed alone may not fix the verdict: the execution context or a statistical acceptance rule must also be specified. Repeating an analysis on a historical record checks that analysis, not the original measurement. A live service introduces access and timing conditions. The guarantee must be weakened whenever the conditions for the declared replay do not hold.

Selective disclosure, forged observations, and a bad predicate can survive every replay. A hash supplied alongside fabricated data binds the claim to those bytes without authenticating their origin. An adequate deployment therefore needs its own policy for accepting roots and running supplied code. Such policies remain within the receiver's trusted boundary. The protocol exposes these dependencies; it does not settle them recursively by assertion.

Cost also matters. Re-running an expensive computation may be wasteful, and an inaccessible artifact can make a correct claim unresolved. A cached or certified verdict may be a reasonable operational choice. The distinction to preserve is whether the receiver has performed the check, could perform it, or is proceeding on an attestation.

A future efficacy study should hold claims, artifacts, and decision tasks fixed while varying the evidence supplied to receivers. It should include incorrect claims, inadequate checks, unavailable inputs, and valid refutations, then measure classification accuracy and verification cost under a specified resource budget. The communication contract and worked replay establish the local step. Its consequences for shared inquiry also call for evaluations of resumption, repeated work, and inheritance of stale claims against equally informative handoffs.

## Conclusion

If knowledge is buildable, its results can be kept as a collection of replayable claims. Local replay auditability preserves the grounds of each claim as it crosses an agent boundary. A receiver can establish a result, retain a refutation, or leave a claim untrue until a verdict is earned. The collection then has an inspectable state: what stands, what failed, and what remains open.

The hypothesis graph makes that collection maintainable. Dependencies and versions let agents resume, divide, and revise the work; a changed premise withdraws dependent warrant, and a failed trial informs the next hypothesis. Knowledge accumulates through results whose grounds survive their authors and whose current standing can still be checked.

## References

1. Deng, X., Da, J., Pan, E., et al. (2025). *SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?* arXiv:2509.16941.
2. Kim, J. (2026). *A Determinacy Audit of SWE-bench Pro.* [Companion article](/a-determinacy-audit-of-swebench-pro).
3. Kim, J. (2026). *What Cannot Be False Cannot Be True.* [Companion article](/what-cannot-be-false-cannot-be-true).
4. Kim, J. (2026). *Verifiable Knowledge.* [Companion article](/verifiable-knowledge).
5. Kim, J. (2026). *The Hypothesis Graph: A Verifiable Semantic Memory for Coding Agents.* [Companion article](/the-hypothesis-graph-semantic-memory-methodeutics).
6. Necula, G. C. (1997). *Proof-Carrying Code.* POPL '97.
7. Gennaro, R., Gentry, C., and Parno, B. (2010). *Non-interactive Verifiable Computing: Outsourcing Computation to Untrusted Workers.* CRYPTO 2010.
8. Lamb, C., and Zacchiroli, S. (2022). *Reproducible Builds: Increasing the Integrity of Software Supply Chains.* IEEE Software 39(2).
9. ACM (2020). *Artifact Review and Badging*, version 1.1.
10. Moreau, L., and Missier, P., eds. (2013). *PROV-DM: The PROV Data Model.* W3C Recommendation.
11. Torres-Arias, S., et al. (2019). *in-toto: Providing Farm-to-Table Guarantees for Bits and Bytes.* USENIX Security.
12. Hardwig, J. (1991). *The Role of Trust in Knowledge.* The Journal of Philosophy 88(12).
13. Rasheed, R. A., Banerjee, S., Mukherjee, A., and Hazra, R. (2026). *From Fluent to Verifiable: Claim-Level Auditability for Deep Research Agents.* arXiv:2602.13855.
14. Hans, A., and Bilionis, I. (2026). *Coding-agents can replicate scientific machine learning papers.* arXiv:2607.02134.
15. Kim, J. (2026). *Truth Is Buildable.* [Foundational essay](/truth-is-buildable).
