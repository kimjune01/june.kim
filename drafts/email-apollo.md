# Email — Apollo Research (customized, one-off)

Form-only contact: apolloresearch.ai/contact (no public inbox). Specificity carries it, not the greeting.
Cites Apollo's own first-party work: 2509.15541 (anti-scheming stress test, their causal eval-awareness
finding) and 2505.23836 (models know when they're being evaluated). Do NOT frame 2406.07358 (sandbagging)
or 2507.11473 (CoT monitorability) as theirs — multi-org/adjacent.

Subject: Scoring anti-scheming where the model can't game the grader

---

Hi Apollo team,

Your anti-scheming stress test (arXiv:2509.15541) shows part of the covert-action drop tracks the model knowing it's being evaluated, and eval-awareness predicts the behavior directly (arXiv:2505.23836). I came at that same gap from the harness side.

The instruments that catch scheming today still read something the model controls, its chain-of-thought or its behavior inside an environment it can learn to recognize as a test. I moved the verdict out of that loop. Each agent claim is bound to a re-runnable kill condition and passes only when an independent replay reproduces the effect, so a sandbagging or self-grading model has nothing to game: the check doesn't ask it anything. A worked example in The Hypothesis Graph (june.kim/the-hypothesis-graph-semantic-memory-methodeutics) shows a self-grading agent staying green on its own tests and still wrong, caught only when an external rerun regrades it.

For covert actions that are themselves externally checkable, a sabotaged output, a disabled oversight hook, a withheld result a test would catch, how much of your anti-scheming gain survives when the verdict is recomputed purely from an external replay, with the model's CoT and its eval/deploy awareness out of the grading path? Have you ever scored an intervention on an awareness-invariant metric, and did the reduction hold or collapse?

june.kim · github.com/kimjune01

June
