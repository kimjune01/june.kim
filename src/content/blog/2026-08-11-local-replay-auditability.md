---
variant: post-paper
title: "Replayable Claims: Epistemic Status Without Trusting the Sender"
tags: coding, epistemology, methodology
---

## Abstract

A receiving agent should be able to determine the epistemic status of another agent's output without trusting the sender's self-attestation. Scores, labels, and Boolean verdicts cannot provide that guarantee because they separate a conclusion from whatever made it answerable. This paper proposes a two-part protocol for epistemic communication: transmit the claim and whatever another agent needs to re-derive its claim-level verdict deterministically. The receiving agent acquires one of three statuses toward that output: the claim is **true** when replay completes and the claim survives, **false** when replay refutes it, and **untrue** when the receiver cannot run it by any available route. Replay clears testimonial uncertainty while specification uncertainty remains: a replayable check may still test the wrong property. We illustrate the distinction through two agent-assisted audits of [SWE-bench Pro](https://arxiv.org/abs/2509.16941). One published a self-attested estimate of roughly 30 percent broken tasks; the other published a 15.0 percent floor through 109 claim-level receipts. The substantive conclusions agree in direction. Only the receipt-backed claims let another agent derive their epistemic status. A compact replay of one task demonstrates the protocol directly.

## Agent output loses its entitlement at the boundary

An agent finishes an inquiry and reports a verdict. The verdict steers the current run. It cannot carry the inquiry's entitlement to the next agent. A confidence score says how strongly the sender endorses its answer. A Boolean says which side the sender chose. Neither gives the receiver a way to find out.

This is a communication failure before it is a verification failure. The sender may have run excellent tests, consulted several reviewers, and reached the right conclusion. If only the verdict crosses the boundary, the receiver inherits the sender's self-assessment. More internal deliberation may improve the hidden process while its output keeps the same epistemic form.

A trustless protocol changes what crosses. The sender transmits two things:

1. the claim;
2. whatever another agent needs to re-derive its claim-level verdict deterministically.

The second part has no fixed schema; its function defines it. A mathematical claim may carry a proof. A software claim may carry a test, commit, and environment. An empirical claim may point to an instrument record or a live service. Proof is one species of replay among many.

The protocol is trustless in one sense: the receiver need not trust the sender's report. The replay may still depend on a compiler, dataset, sensor, or service. Those dependencies belong inside the replay path, where the receiver can see what the claim requires.

## Epistemic status describes the receiver's relation to agent output

A transmitted claim carries no globally authoritative status. Each receiver establishes the epistemic status supported by what it can replay from the agent's output. Reality remains fixed across those relations.

| The receiver's relation to the agent's claim | Epistemic status |
|---|---|
| Runs it; the claim survives | **True** |
| Runs it; the claim is refuted | **False** |
| Cannot run it by any available route | **Untrue** |

The trichotomy comes from [*What Cannot Be False Cannot Be True*](/what-cannot-be-false-cannot-be-true). This paper applies it to agent output. A passing replay gives its receiver entitlement to the claim and emits no transferable truth bit.

Ordinary observations need no bundled check. If the receiver can already check a claim from shared context, the context supplies the replay. For an agent able to observe the sky or consult a common source, “The daytime sky is blue when it is not cloudy” carries nothing extra.

Time matters when replay makes it matter. A claim about a pinned artifact remains true for any receiver who can still replay its evidence. A claim about the artifact's current state must run against the current artifact. If a required service later disappears, the claim is untrue for a new knower who cannot run it. A later opposing verdict makes the claim false.

## Replay preserves one guarantee under misspecification

Replay clears testimonial uncertainty while specification uncertainty remains. A check can return deterministically and still measure the wrong property. It can miss relevant cases, encode a bad oracle, or depend on a poisoned artifact. Local replay guarantees only that the receiver can derive the encoded claim-level verdict without trusting the sender.

That narrow guarantee keeps the failure visible. A self-attested verdict compresses two questions into one:

1. Did the sender report the result faithfully?
2. Did the procedure test what the claim says?

Replay removes the first question. The second stays open, where another agent can inspect, challenge, and replace the procedure. A replayable mistake is still a mistake, but it has a surface on which inquiry can continue.

A replayable claim needs no confidence score to stand in for entitlement. When the receiver can run the procedure and find out, it need not estimate whether the sender is likely to be right. Probability can remain the content of a claim, such as a weather forecast. Probability no longer has to stand in for the missing path from claim to evidence.

## An epistemic ablation on SWE-bench Pro

Picture two otherwise identical audit agents. Both inspect the same benchmark and reach the same conclusions. The self-attesting agent returns labels and a headline rate. The trustless agent returns each claim with its replay. Their discovery capability is held fixed; only the epistemic form of their output changes. The first leaves the receiver with an attestation. The second lets the receiver find out.

Two real audits approximate this contrast. Both employed agents against the same benchmark under opposite communication protocols. Their different methods, scopes, categories, and denominators preclude a controlled performance estimate.

[OpenAI's audit of SWE-bench Pro](https://openai.com/index/separating-signal-from-noise-coding-evaluations/) used an automated filter and repeated investigator-agent passes. A researcher and five software engineers reviewed the results. The post reports 200 tasks labeled broken by the agent pipeline, 249 by the human campaign, and a headline estimate of roughly 30 percent. The post does not publish the pipeline, the per-task labels, the annotations, or the disagreements. The author is “OpenAI,” so its agents and reviewers attest their own work.

The [public determinacy audit of SWE-bench Pro](/a-determinacy-audit-of-swebench-pro) used agents under the trustless protocol. It reports a smaller, deliberately conservative floor. The audit mechanically witnesses 83 cases, and another 26 survive adversarial cross-family review. Together they make 109 of 728 public tasks, or 15.0 percent.

Each claimed task links to its case materials and witness. Beside them the audit publishes twelve proposed cases that adversarial review killed. A reader can reject the headline, enter at one row, and derive that row's verdict without trusting the auditor.

The ablation concerns epistemic output. OpenAI may be right about every one of its 249 labels. The protocol leaves them untrue for an outside knower until their checks become replayable.

The diagnostic applies claim by claim. OpenAI publishes one detailed OpenLibrary example whose prompt and test conflict by one leading space. SWE-bench Pro's public artifacts let a reader cross-examine that example, so the example can acquire a status the unpublished aggregate cannot. One document can contain true, false, and untrue claims at once.

## One claim, replayed

The audit classifies `ansible_20ef733e` as underdetermined. Its requirements ask the password-hashing filter to accept a bcrypt identifier and make the result visibly begin with that identifier. The hidden test requires more. For one fixed secret and salt, the implementation must return this exact digest:

```text
$2$12$123456789012345678901ufd3hZRrev.WXCbemqGIV/gmWaTGLImm
```

The receipt's claim is narrow: this exact graded constant appears in the hidden test but nowhere in the specification or base-commit source available to the solver. From the materialized case, the decisive search is compact:

```sh
DIGEST='$2$12$123456789012345678901ufd3hZRrev.WXCbemqGIV/gmWaTGLImm'

rg -n -F "$DIGEST" spec.md
# no match

rg -n -F "$DIGEST" hidden_test.diff
# 201:+    assert_hash("$2$12$123456789012345678901ufd3hZRrev.WXCbemqGIV/gmWaTGLImm",

git -C ansible-at-base grep -n -F "$DIGEST"
# no match
```

The [`ansible_20ef733e` receipt](https://github.com/kimjune01/swebench-pro-audit/tree/main/data/cases/ansible_20ef733e) pins the instance and supplies the complete case bundle and witness. The audit agent proposes what to inspect; the search produces the verdict. A receiving agent can replay the claim without the producing agent, its trajectory, or its confidence.

That replay establishes the receipt's local claim. Other interpretations of the task remain open. The claim reaches exactly as far as the check.

## Limits and scope

Forged inputs and selective disclosure can corrupt the record; evaluation awareness and collusion remain possible. Artifact integrity and semantic adequacy remain claims of their own.

Replay also costs time, compute, and access. A live service may vanish. A physical experiment may be too expensive to repeat. In each case the protocol exposes the limit in the agent's output. A confidence score would only price it in.

The audit's 109 receipts show the protocol operating at benchmark scale. Agent capability and audit speed stay outside its claim. Other applications appear in the broader [benchmark-audit method](/how-to-audit-a-benchmark). Population-level accumulation belongs to [*Verifiable Knowledge*](/verifiable-knowledge), and the graph that composes replayable claims belongs to [*The Hypothesis Graph*](/the-hypothesis-graph-semantic-memory-methodeutics). This paper isolates the act between them: one agent sends a claim, and another derives its epistemic status.

## Conclusion

An agent should transmit more than its answer when another agent must decide what to know. The replayable-claims protocol sends the claim and whatever re-derives its claim-level verdict. The receiver runs it and acquires a relational status: true, false, or untrue.

The protocol changes epistemic communication without requiring the receiver to trust the sender. In the SWE-bench Pro ablation, agents outside the protocol produced an opaque institutional estimate; agents under the protocol produced claims a stranger can rerun one at a time. The substantive findings point in the same direction while their epistemic outputs diverge.

Show the claim. Show how to find out.

## Availability

- [SWE-bench Pro determinacy audit](https://github.com/kimjune01/swebench-pro-audit) · [Zenodo](https://doi.org/10.5281/zenodo.20738219)
- [What Cannot Be False Cannot Be True](/what-cannot-be-false-cannot-be-true)
- [Verifiable Knowledge](/verifiable-knowledge)
- [The Hypothesis Graph](/the-hypothesis-graph-semantic-memory-methodeutics)
