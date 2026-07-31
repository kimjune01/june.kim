---
variant: post-medium
title: "Borrowed Vocabulary for the Hypothesis Edge"
tags: epistemology, methodology
---

[The hypothesis graph](/the-hypothesis-graph) typed the nodes: hypotheses, each begging for evidence. It typed the trajectories: [e-values](https://en.wikipedia.org/wiki/E-values) with provenance. The edge it left undefined. "Reason," the causal linkage one node claims over another, is the relation the whole structure leans on, and the spec never says what one is. This post is the patch.

Philosophy has pieces. [Toulmin](https://en.wikipedia.org/wiki/The_Uses_of_Argument) gives the warrant, the license connecting data to claim. [Peirce](https://plato.stanford.edu/entries/peirce/) had it seventy years earlier as the leading principle. [Pollock](https://en.wikipedia.org/wiki/John_L._Pollock) split the attacks: rebutting defeaters hit the conclusion; undercutting defeaters hit the linkage itself.

[Woodward](https://plato.stanford.edu/entries/causation-mani/) says only intervention earns the causal reading, which is why a hypothesis graph works on bug-fixing and stalls on strategy. Wiggle X, read Y, or you have correlation wearing a costume.

All of these terms were forged in seminars, where a wrong definition costs nothing. We crave the precision that [jurisprudence](https://en.wikipedia.org/wiki/Jurisprudence) established in production. The common law has run the evidence graph for [seven centuries](https://en.wikipedia.org/wiki/Year_Books), under adversarial load, with losses on every wrong edge, and [Holmes](https://en.wikipedia.org/wiki/The_Common_Law_(Holmes)) explained in 1881 what that does to vocabulary. I looked it up:

> The life of the law has not been logic: it has been experience.

Terms distilled from experience are precise exactly where terms distilled from seminars go vague, because every one was forged by someone getting burned. So the patch is a borrowing. The crosswalk maps their vocabulary onto the edge.

### Crosswalk

| Governs | Legal term | Hypothesis edge |
|---------|-----------|-----------------|
| Admission | [Burden of production](https://www.law.cornell.edu/wex/burden_of_production) | Edge must show evidence or drops out by default |
| | [Prima facie](https://www.law.cornell.edu/wex/prima_facie) | Enough support to stand unless attacked |
| | [Presumption](https://www.law.cornell.edu/wex/presumption) | Default edge; burden shifts to whoever wants it deleted |
| | [Admissibility](https://www.law.cornell.edu/wex/admissible_evidence) | Entry gate on evidence, separate from its weight |
| | [Judicial notice](https://www.law.cornell.edu/wex/judicial_notice) | Axiom admitted without proof; nobody contests it |
| Strength | [Standards of proof](https://www.law.cornell.edu/wex/burden_of_proof) | Threshold for treating a node as established, set by the cost of a wrong edge |
| | [Probative value](https://www.law.cornell.edu/wex/probative_value) | How far one datum actually moves an edge |
| | [Materiality](https://www.law.cornell.edu/wex/materiality) | Whether the node is of consequence to the question being decided |
| Causation | [But-for cause](https://www.law.cornell.edu/wex/but-for_test) | Counterfactual test on the edge |
| | [Proximate cause](https://www.law.cornell.edu/wex/proximate_cause) | Policy cutoff on chain traversal |
| | [Superseding cause](https://www.law.cornell.edu/wex/superseding_cause) | Intervening event that breaks the chain; upstream edge stops carrying |
| Settlement | [Issue preclusion](https://www.law.cornell.edu/wex/collateral_estoppel) | Subgraph actually litigated to verdict; the parties bound can't reopen it |
| | [Stare decisis](https://www.law.cornell.edu/wex/stare_decisis) | Settled warrants bind future traversals |
| | [Ratio decidendi](https://www.law.cornell.edu/wex/ratio_decidendi) vs [obiter dicta](https://www.law.cornell.edu/wex/obiter_dictum) | Reusable warrant vs side commentary |
| | [Standard of review](https://www.law.cornell.edu/wex/standard_of_review) | Deference each kind of verdict is owed when retro re-examines it |
| Provenance | [Chain of custody](https://en.wikipedia.org/wiki/Chain_of_custody) | Attestation receipts |
| | [Hearsay](https://www.law.cornell.edu/wex/hearsay) | Edge quoting an out-of-loop assertion for its truth; warrant can't be cross-examined |
| | [Impeachment](https://www.law.cornell.edu/rules/fre/rule_607) | Attack on the source, not the claim |
| | [Spoliation](https://en.wikipedia.org/wiki/Spoliation_of_evidence) | Deliberate deletion draws the adverse inference |

*Proximate cause* is honest typing: the law admitting out loud that but-for chains run to infinity and the cutoff is policy, no fact of the matter. *Issue preclusion* is the norm debates lack: outside courtrooms, every argument rebuilds the graph from zero because nothing forbids reopening settled nodes. And *dicta*: every two-page meeting summary is dicta. The eight lines you wanted are the ratio.

### The borrow

Jurisprudence has pieces too. The crosswalk borrows them a term at a time; the assembly stays ours. And laying them out exposed where the vagueness came from. "Reason" was one edge type doing three jobs: `supports(evidence, node)` settles by severity, `causes(event, outcome)` settles by intervention, `constrains(settled, pending)` settles by authority. Jurisprudence never collapses them. Evidence law governs the first, causation doctrine the second, precedent the third, and the crosswalk's groupings follow the same seams.

The borrowing also names what an edge is over its lifetime. A forward edge is a causal claim held at conjecture strength, a bet with a promissory note attached. Intervene here and the verdict will read thus. Evidence doesn't make the edge causal. It cashes the warrant. The graph becomes a ledger of bets in various states of settlement, and a reason is a settled bet you're allowed to reuse.

I set out to design that ledger. The law already shipped it: the [Federal Rules of Evidence](https://www.law.cornell.edu/rules/fre) are its operations manual, debugged one adversarial appeal at a time, and [Levi's](https://en.wikipedia.org/wiki/Edward_H._Levi) *An Introduction to Legal Reasoning* is the architecture doc.

One edge stays open. Whether `supports`, `causes`, and `constrains` earn separate types in the schema is itself a forward edge, drawn at conjecture strength, begging for its evidence. It settles when a graph runs typed. Borrow the vocabulary. Don't give it back.
