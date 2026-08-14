---
variant: post-paper
title: "Replayable Claims: Epistemic Status Without Trusting the Sender"
tags: coding, epistemology, methodology
---

## Abstract

The epistemic status of an agent's output should be checkable without trusting the sender's self-attestation. Scores, labels, and Boolean verdicts cannot provide that guarantee on their own because they present the conclusion without the procedure. We propose a protocol that attaches verifiability to the claim: transmit the claim alongside its deterministic re-derivation. Replay clears testimonial uncertainty; specification uncertainty remains. We illustrate an epistemic ablation on two independent audits of [SWE-bench Pro](https://arxiv.org/abs/2509.16941) using opposite protocols. One published a self-attested estimate of roughly 30 percent broken tasks; the other, a 15.0 percent floor through 109 claim-level receipts.

## Agent output loses its entitlement at the boundary

An agent finishes an inquiry and reports a verdict; a second agent receives that verdict and must decide whether to trust it, but the verdict is all it receives. A confidence score says how strongly the sender endorses its answer, but it doesn't give the receiver a way to find out.

This is a communication failure as much as it is a verification failure. The sender may have run excellent tests, consulted several reviewers, and reached the right conclusion. But if only the verdict crosses the boundary, the receiver inherits the sender's self-assessment; the inquiry's entitlement never crosses. So internal deliberation may improve output quality, but its epistemic form is unchanged: the receiver must still take the sender's word.

A trustless protocol therefore changes what crosses. The sender transmits two things:

1. The claim;
2. Whatever another agent needs to re-derive its claim-level verdict deterministically.

The second part is a procedure. A mathematical claim may carry a proof. A software claim may carry a test, commit, and environment. An empirical claim may point to an instrument record or a live service. If the claim is obvious in a shared context, the procedure may be implied.

The protocol is trustless in one sense: the receiver need not trust the sender's report. But the replay may still depend on a compiler, dataset, sensor, or service. Those dependencies belong inside the replay path, where the receiver can see what the claim requires.

## Epistemic status describes the receiver's relation to agent output

A transmitted claim carries no globally authoritative status. Instead, each receiver establishes knowledge by checking the agent's output. Hence, the epistemic status of a claim is relative to the receiver.

| The receiver's relation to the agent's claim | Epistemic status |
|---|---|
| Runs it; the claim survives | **True** |
| Runs it; the claim is refuted | **False** |
| Cannot run it by any available route | **Untrue** |

The trichotomy comes from [*What Cannot Be False Cannot Be True*](/what-cannot-be-false-cannot-be-true). We apply it here to agent output. A passing replay gives its receiver entitlement to the claim but emits no transferable truth bit.

But ordinary observations need no bundled check. If the receiver can already check a claim from shared context, the context supplies the replay. Therefore, the rigor of a check depends on context boundaries. For example, the rules of integer addition need not be accompanied by their derivation.

Time matters when replay makes it matter. A claim about a pinned artifact remains true for any receiver who can still replay its evidence, but a claim about the artifact's current state must run against the current artifact. So if a required service later disappears, the claim is untrue for a new knower who cannot run it; a later opposing verdict makes it false. A claim about the current weather is the everyday case.

## Replay preserves one guarantee under misspecification

Replay clears testimonial uncertainty while specification uncertainty remains. A check can return deterministically and still measure the wrong property. It can miss relevant cases, encode a bad oracle, or depend on a poisoned artifact. So local replay guarantees only that the receiver can derive the encoded claim-level verdict without trusting the sender.

That narrow guarantee keeps the failure visible. A self-attested verdict compresses two questions into one:

1. Did the sender report the result faithfully?
2. Did the procedure test what the claim says?

Replay removes the first question but leaves the second open, where another agent can inspect, challenge, and replace the procedure. A replayable mistake is still a mistake, but it has a surface on which inquiry can continue.

A replayable claim needs no confidence score to stand in for entitlement. When the receiver can run the procedure and find out, it need not estimate whether the sender is likely to be right. Probability can remain the content of a claim, such as a weather forecast; it no longer has to stand in for the missing path from claim to evidence.

## An epistemic ablation on SWE-bench Pro

Picture two otherwise identical audit agents. Both inspect the same benchmark and reach the same conclusions. The self-attesting agent returns labels and a headline rate. The trustless agent returns each claim with its replay. Their discovery capability is held fixed; only the epistemic form of their output changes. The first leaves the receiver with an attestation. The second lets the receiver find out.

Two real audits approximate this contrast. Both employed agents against the same benchmark under opposite communication protocols, but their different methods, scopes, categories, and denominators preclude a controlled performance estimate.

[OpenAI's audit of SWE-bench Pro](https://openai.com/index/separating-signal-from-noise-coding-evaluations/) used an automated filter and repeated investigator-agent passes. A researcher and five software engineers reviewed the results. The post reports 200 tasks labeled broken by the agent pipeline, 249 by the human campaign, and a headline estimate of roughly 30 percent. But the post does not publish the pipeline, the per-task labels, the annotations, or the disagreements. The author is “OpenAI,” so its agents and reviewers attest their own work.

The [public determinacy audit of SWE-bench Pro](/a-determinacy-audit-of-swebench-pro) used agents under the trustless protocol. It reports a smaller, deliberately conservative floor. The audit mechanically witnesses 83 cases, and another 26 survive adversarial cross-family review. Together they make 109 of 728 public tasks, or 15.0 percent. Three more of the 731 public tasks fail their own grader on the gold patch and sit outside that denominator.

Each claimed task links to its case materials and witness. Beside them the audit publishes twelve proposed cases that adversarial review killed. So a reader can reject the headline, enter at one row, and derive that row's verdict without trusting the auditor.

The ablation concerns epistemic output. OpenAI may be right about every one of its 249 labels, but the protocol leaves them untrue for an outside knower until their checks become replayable.

The diagnostic applies claim by claim. OpenAI publishes one detailed OpenLibrary example whose prompt and test conflict by one leading space. SWE-bench Pro's public artifacts let a reader cross-examine that example, so the example can acquire a status the unpublished aggregate cannot. One document can contain true, false, and untrue claims at once.

## One claim, replayed

The audit classifies `ansible_20ef733e` as underdetermined. Its requirements ask the password-hashing filter to accept a bcrypt identifier and make the result visibly begin with that identifier. But the hidden test requires more. For one fixed secret and salt, the implementation must return this exact digest:

```text
$2$12$123456789012345678901ufd3hZRrev.WXCbemqGIV/gmWaTGLImm
```

The receipt's claim: this exact graded constant appears in the hidden test but nowhere in the specification or base-commit source available to the solver. From the materialized case, its search is compact:

```sh
DIGEST='$2$12$123456789012345678901ufd3hZRrev.WXCbemqGIV/gmWaTGLImm'

rg -n -F "$DIGEST" spec.md
# no match

rg -n -F "$DIGEST" hidden_test.diff
# 201:+    assert_hash("$2$12$123456789012345678901ufd3hZRrev.WXCbemqGIV/gmWaTGLImm",

git -C ansible-at-base grep -n -F "$DIGEST"
# no match
```

The [`ansible_20ef733e` receipt](https://github.com/kimjune01/swebench-pro-audit/tree/main/data/cases/ansible_20ef733e) pins the instance and supplies the complete case bundle and witness. The audit agent proposes what to inspect; the search produces the verdict. So a receiving agent can replay the claim without the producing agent, its trajectory, or its confidence.

That replay establishes the receipt's local claim. But other interpretations of the task remain open: the claim reaches exactly as far as the check.

## Limits and scope

Forged inputs and selective disclosure can corrupt the record; evaluation awareness and collusion remain possible. So artifact integrity and semantic adequacy are claims of their own, to be transmitted with checks of their own.

Replay also costs time, compute, and access. A live service may vanish. A physical experiment may be too expensive to repeat. In each case the protocol exposes the limit in the agent's output; a confidence score would only price it in and remain static.

The audit's 109 receipts show the protocol operating at benchmark scale, but agent capability and audit speed stay outside its claim. Other applications appear in the broader [benchmark-audit method](/how-to-audit-a-benchmark). Population-level accumulation belongs to [*Verifiable Knowledge*](/verifiable-knowledge), and the graph that composes replayable claims belongs to [*The Hypothesis Graph*](/the-hypothesis-graph-semantic-memory-methodeutics). Here we isolate the act between them: one agent sends a claim, and another derives its epistemic status.

## Conclusion

An agent should transmit more than its answer when another agent must decide what to know. The replayable-claims protocol sends the claim and whatever re-derives its claim-level verdict. The receiver runs it and acquires a relational status: true, false, or untrue.

The protocol changes epistemic communication without requiring the receiver to trust the sender. In the SWE-bench Pro ablation, agents outside the protocol produced an opaque institutional estimate; agents under the protocol produced claims a stranger can rerun one at a time. The substantive findings point in the same direction while their epistemic outputs diverge.

Show the claim. Also show how to find out.

## References

1. Xiang Deng, Jeff Da, Edwin Pan, et al. *SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?* [arXiv:2509.16941](https://arxiv.org/abs/2509.16941), 2025.
2. OpenAI. *Separating signal from noise in coding evaluations.* [openai.com](https://openai.com/index/separating-signal-from-noise-coding-evaluations/), July 2026.
3. June Kim. *A Determinacy Audit of SWE-bench Pro.* [doi:10.5281/zenodo.20738219](https://doi.org/10.5281/zenodo.20738219), June 2026. Live artifact: [github.com/kimjune01/swebench-pro-audit](https://github.com/kimjune01/swebench-pro-audit); web version: [june.kim](https://june.kim/a-determinacy-audit-of-swebench-pro).
4. June Kim. *What Cannot Be False Cannot Be True.* [doi:10.5281/zenodo.20754645](https://doi.org/10.5281/zenodo.20754645), June 2026. Web version: [june.kim](https://june.kim/what-cannot-be-false-cannot-be-true).
5. June Kim. *Verifiable Knowledge.* [doi:10.5281/zenodo.20754823](https://doi.org/10.5281/zenodo.20754823), June 2026. Web version: [june.kim](https://june.kim/verifiable-knowledge).
6. June Kim. *The Hypothesis Graph: A Verifiable Semantic Memory for Coding Agents.* [doi:10.5281/zenodo.21939861](https://doi.org/10.5281/zenodo.21939861), May 2026. Web version: [june.kim](https://june.kim/the-hypothesis-graph-semantic-memory-methodeutics).
7. June Kim. *How to Audit a Benchmark.* [doi:10.5281/zenodo.21939914](https://doi.org/10.5281/zenodo.21939914), July 2026. Web version: [june.kim](https://june.kim/how-to-audit-a-benchmark).
