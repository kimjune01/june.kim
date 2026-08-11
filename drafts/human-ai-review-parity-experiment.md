# Human–AI review parity

## Question

When can AI review be said to meet the same quality standard as human review?

Review speed is not a productivity gain until review quality clears the same threshold. A faster reviewer that approves more consequential defects is producing a different, weaker product.

## Keep the layers separate

1. **Problem selection:** Is this a problem worth solving?
2. **Domain review:** Does the proposed behavior solve the real problem?
3. **Specification review:** Does the written task determine the intended behavior?
4. **Implementation:** Does the code realize that specification?
5. **Code review:** Is the implementation correct, safe, comprehensible, and maintainable?
6. **Field outcome:** Does the change survive later use, extension, and maintenance?

Code review cannot repair an invalid target. If the specification asks for the wrong behavior, an agent can implement it perfectly and still produce the wrong system. If decisive requirements exist only in hidden tests, the benchmark is underdetermined; neither human nor AI review has been given the evidence needed to recover the intended answer.

An autonomous-engineering claim may include detecting contradictions, recovering repository context, and asking for clarification. Those are broader capabilities than code review and should be measured separately.

## Identification problem

“The human read every line” measures exposure, not review efficacy. It does not establish what the reviewer understood, which defects they could detect, or whether their approval predicts future outcomes.

Likewise, agreement with historical review comments is not an independent quality oracle. Human comments are incomplete and sometimes wrong. Treating them as gold makes human review correct by construction.

The comparison needs to hold constant:

- the code under review;
- the validated problem and specification;
- repository and domain context;
- available tools, tests, and time budget;
- the acceptance standard;
- the independent outcome oracle.

Only the reviewer should vary.

## Conditions

Randomly assign the same candidate changes to:

1. Human review only.
2. AI review only.
3. Human review after AI review.
4. AI review after human review.
5. Independent human and AI review, with findings combined after both commit.

Preserve each reviewer's findings, approval decision, confidence, evidence, and time. Do not let later reviewers see earlier findings unless that information is the treatment.

The combined conditions test complementarity. Order matters: an initial review may anchor the second reviewer or replace independent inspection with verification of the first reviewer's claims.

## Ground truth

Use two sources of defects:

- **Seeded defects:** known, realistic faults inserted into otherwise acceptable changes. These provide a controlled denominator.
- **Natural defects:** faults found in real changes, adjudicated independently and backed by executable or field evidence where possible.

Include defects at different layers, but label them before analysis:

- domain mismatch;
- specification ambiguity or contradiction;
- functional defect;
- security or preservation failure;
- repository convention or integration failure;
- maintainability defect that affects a later change.

Code-review efficacy should be reported on implementation-layer defects. Domain and specification findings are valuable, but should not silently inflate the code-review score.

## Outcomes

Measure:

- recall by defect class and severity;
- false approvals and false alarms;
- precision of findings;
- review time and total remediation time;
- whether the finding identifies the cause, not merely a symptom;
- quality of the resulting fix;
- defects escaping into the next task;
- time and success on a blinded downstream extension;
- reviewer understanding, tested by predicting behavior or making a later change.

Immediate defect detection and downstream maintainability are different outcomes. Report both. Static code-shape metrics may be diagnostic features, but should not stand in for maintenance cost until validated against it.

## Parity gate

Define an acceptable non-inferiority margin before observing results. AI review clears the gate only if it is no worse than human review on consequential false approvals and downstream outcomes within that margin.

After parity is established, compare speed and cost. Weak dominance would require AI review to be no worse on every predeclared quality outcome and better on at least one outcome such as time or cost.

A scalar average can hide a fatal trade: catching more style issues does not compensate for missing a security or data-loss defect. Use severity-weighted reporting and hard gates for catastrophic classes.

## Relationship to existing benchmarks

The adjacent literature currently leaves a gap:

- Code-review benchmarks measure whether AI reproduces human comments or detects expert-labeled issues.
- Iterative coding benchmarks measure later task performance or static code-shape drift.
- Developer-productivity studies record review behavior and elapsed time.

The missing experiment connects review treatment to independently adjudicated defects and then to downstream code outcomes.

SlopCodeBench is relevant because it tries to operationalize the extension quality that review is supposed to preserve. It does not measure review efficacy, and the audit finds that its static metrics are not validated against future maintenance cost. It therefore exposes the missing bridge rather than supplying the answer.

## Smallest credible pilot

- Select changes with a validated specification and runnable repository.
- Construct a balanced set of seeded and natural defects.
- Recruit domain-competent human reviewers.
- Run one strong AI reviewer under matched context and tool access.
- Blindly adjudicate findings before revealing reviewer identity.
- Apply accepted fixes.
- Give a fresh agent or developer the same downstream extension on each resulting codebase.
- Compare defect detection, remediation cost, and downstream success.

The pilot should first establish that the oracle and adjudication process work. It should not begin by estimating productivity from review time.

## Open questions

- What is the right non-inferiority margin for consequential defects?
- Should the human baseline be one reviewer, a panel, or the repository's normal process?
- How should tacit domain knowledge be supplied without giving one condition an advantage?
- Does AI review complement human review because the two miss different defect classes?
- Does review order create anchoring or automation bias?
- Can an executable auditing agent produce evidence strong enough to reduce adjudication cost?
- Which downstream horizon is long enough to reveal maintainability costs without making the experiment impractical?
