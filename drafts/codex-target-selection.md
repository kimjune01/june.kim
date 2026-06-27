# Target selection for a differential-soundness bug-hunting method

I have a method and a paper. I need help picking a handful of *target projects* to contribute to, for risk management. Answer directly: which targets, ranked, and why. A handful is fine. Push back if my framing is wrong.

## The method

A cheap "separation oracle" for rewrite/derivative-rule soundness. For autodiff compilers: many algebraic rewrites are real-algebra identities applied to floats (`log(a*a)=2log(a)`, reassociation). Floats aren't a ring, so some are unsound. A static analyzer predicts the witnessing edge input from rule structure with no execution (domain(L)\domain(R)); a dynamic gate confirms against the real implementation. On a bounded elementwise fragment this is a decision procedure, not a search. Generalizes (more loosely) to any optimizer with declarative rewrite rules, and to differential testing where no algebra exists (the oracle becomes empirical).

The paper frames this as a "detect-and-refine ambiguous specifications" loop: a soundness bug = the optimizer reaching a faster point outside the correctness feasible region (a missing constraint); the fix = constraint generation (a guard); the artifact that lands = a generalizing regression test that reaches the edge the author's own test missed.

## Current evidence portfolio

- **EnzymeAD/Enzyme-JAX**: 2 confirmed soundness bugs (LogSimplify, CbrtOp), 2 fix PRs open, a closed sweep over the unary elementwise derivative table (12/12 decided, 1 flagged = a real bug, 11 proven sound).
- **EnzymeAD/Enzyme** (core C++/LLVM): 1 merged PR, 1 open — real standing here.
- **wild-linker/wild**: 1 PR fixing a reported `--compress-debug-sections` merge-string bug; built a generalizing regression test; warmly received, converging to merge. Different domain (linker), different org. This is the "empirical oracle" endpoint.

## Constraints I've learned

- **Concentration risk**: everything is EnzymeAD except wild. One maintainer relationship is load-bearing; the paper reads as "validated in one family." I want diversity across orgs/domains.
- **Receptivity is a hard filter, not etiquette.** I was banned from tinygrad — not for low quality, but because they run to a roadmap and don't want unsolicited/off-roadmap bug-hunting at all. wild, by contrast, explicitly welcomes "going out to look for these bugs." So the filter is: does the project's *stated culture* want a soundness/miscompile bug from an outsider?
- **I have zero standing outside EnzymeAD and wild.** Every other target is a cold approach. Cold + non-receptive = the tinygrad failure. So lowest-variance cold approach = project whose stated culture wants the artifact type.
- I use agent tooling and disclose it (worked at wild). Don't flood; one careful PR per repo.

## The question

Pick a handful of target projects to diversify into, ranked. For each: why it's method-fit (declarative rewrite rules / differential-soundness surface), why its culture is receptive to an outsider soundness bug, and how I'd warm up the cold approach. Candidates I'm weighing: Cranelift (bytecodealliance), JAX (google), ChainRules.jl (JuliaDiff), LLVM/Alive-adjacent, mold. Tell me if I'm missing better ones, or if diversifying now is premature vs. deepening Enzyme first.
