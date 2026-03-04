# Stanford Faculty: Relevant Paper Summaries

Reading notes for conversations with Stanford professors about embedding-based ad auctions.

---

## Michael Ostrovsky (GSB, Economics)

### "Internet Advertising and the Generalized Second-Price Auction" (AER 2007)
With Edelman, Schwarz. The foundational GSP paper.

- GSP is not a Vickrey auction despite surface resemblance. Truth-telling is not an equilibrium.
- Introduces "locally envy-free" equilibria: no advertiser prefers to swap slot-and-payment with an adjacent competitor. This refinement selects efficient, well-behaved outcomes.
- All stable GSP equilibria generate revenue >= VCG. Platforms get *more* money from GSP's strategic complexity, which explains why they prefer it over the cleaner VCG mechanism.
- Constructs a "generalized English auction" with a unique ex post equilibrium matching VCG payoffs, giving behavioral justification for locally envy-free equilibria as the natural resting point.

[AEA](https://www.aeaweb.org/articles?id=10.1257/aer.97.1.242) | [NBER](https://www.nber.org/papers/w11765)

### "Reserve Prices in Internet Advertising Auctions: A Field Experiment" (JPE 2023)
With Schwarz. Applies Myerson optimal auction theory to real search auctions.

- Large-scale field experiment on a major search platform. Treatment group got theory-guided reserve prices; control kept 10-cent defaults.
- Optimized reserves reduced ads shown by about one per query but increased revenue by ~3%.
- Validates that reserve prices are a major lever, not a rounding error.

[JPE](https://www.journals.uchicago.edu/doi/10.1086/725702)

### "Choice Screen Auctions" (AER 2023)
EU antitrust remedy: consumers choose default search engine on Android.

- Per-appearance vs. per-install pricing drastically changes which engines win.
- Per-install auctions distort incentives: alternative search engines extract maximum revenue from each install rather than growing user base. The distortion worsens as competition increases.

[AEA](https://www.aeaweb.org/articles?id=10.1257/aer.20220699)

---

## Vasilis Syrgkanis (MS&E, CS)

### "Econometrics for Learning Agents" (EC 2015, Best Paper)
With Nekipelov, Tardos.

- Replaces Nash equilibrium assumption with no-regret learning. Real bidders use algorithms and may never reach equilibrium; this paper gives you econometric tools that work anyway.
- Recovers true bidder valuations from observed bid data even when bidders are still learning.
- Validated on Microsoft's sponsored search data.
- Prerequisite for designing welfare-maximizing mechanisms when participants use auto-bidding.

[arXiv](https://arxiv.org/abs/1505.00720)

### "Composable and Efficient Mechanisms" (STOC 2013)
With Tardos. The smoothness framework for composed auctions.

- A mechanism is "smooth" if it generates approximately market-clearing prices. Smoothness at each individual mechanism implies efficiency of the composed global system.
- Robustness: guarantees hold across full-information equilibria, Bayesian equilibria, and learning dynamics.
- Theoretical foundation for why simple auction formats still produce good outcomes in messy, multi-auction programmatic environments.

[arXiv](https://arxiv.org/abs/1211.1325)

### "Oracle-Efficient Online Learning and Auction Design" (FOCS 2017)
With Dudik, Haghtalab, Luo, Schapire, Vaughan.

- Introduces "Generalized Follow-the-Perturbed-Leader" for learning optimal auction parameters online against adversarial bidders, with only an offline optimization oracle.
- Oracle-efficient algorithms for: VCG with bidder-specific reserves, envy-free item-pricing, level auctions.
- Extends to contextual learning (bidder demographics, query features).
- Algorithmic blueprint for a platform that learns optimal reserves from live data.

[arXiv](https://arxiv.org/abs/1611.01688)

---

## Gabriel Weintraub (GSB, Operations)

### "Bidders' Responses to Auction Format Change in Display Advertising" (2021)
With Goke, Mastromonaco, Seljan.

- Revenue per sold impression jumped 35-75% when exchanges switched from second-price to first-price, because bidders initially failed to bid-shade.
- The premium dissipated as bidders learned, consistent with revenue equivalence theorem.
- Bidder sophistication varied significantly; some adapted quickly, others did not.

[arXiv](https://arxiv.org/abs/2110.13814)

### "Repeated Auctions with Budgets in Ad Exchanges" (Management Science 2015)
With Balseiro, Besbes.

- Introduces "Fluid Mean Field Equilibrium" (FMFE) for budget-constrained repeated auctions. Sometimes admits closed-form solutions.
- Budget constraints create dynamic interactions that fundamentally change bidding landscapes vs. single-shot theory.
- Lets publishers backtest auction designs (especially reserve prices) while accounting for strategic advertiser responses.

[Management Science](https://pubsonline.informs.org/doi/10.1287/mnsc.2014.2022)

### DOJ Expert Testimony in *United States v. Google LLC* (Sept 2024)
Expert economic witness for DOJ Antitrust Division. Analyzed six Google practices using Google's own A/B test data.

- **First Look:** decreased rival exchange share by 24.6%.
- **Last Look:** diverted ~$473M/year to Google; reduced third-party impressions 14.25%, revenue 8.72%.
- **Project Poirot v1:** reduced third-party monthly spend by $59.5M. **v2:** by $267.9M.
- **Unified Pricing Rules + Exclusivity:** eliminated publishers' differential pricing options.
- April 2025: Judge Brinkema ruled Google illegally monopolized publisher ad server and ad exchange markets.

[DOJ ruling](https://www.justice.gov/opa/pr/department-justice-prevails-landmark-antitrust-case-against-google) | [AdExchanger trial coverage](https://www.adexchanger.com/antitrust/doj-vs-google-day-four-behind-the-scenes-on-the-fraught-rollout-of-unified-pricing-rules/)

---

## Susan Athey (GSB, Economics)

### "Position Auctions with Consumer Search" (QJE 2011)
With Ellison.

- Endogenizes advertiser values by modeling consumers who rationally infer quality from ad position and search optimally. Makes the auction a joint mechanism for bidding, search, and welfare.
- Reserve prices screen out low-quality advertisers, reducing wasteful consumer search. Exists a reserve price maximizing both consumer surplus and social welfare simultaneously.
- Provides welfare justification for quality scores (weighting bids by expected CTR).

[NBER](https://www.nber.org/papers/w15253)

### "A Structural Model of Sponsored Search Advertising Auctions" (2010)
With Nekipelov.

- Structural econometric model using 3 months of Bing data. Advertisers set standing bids across heterogeneous queries; competitive sets vary query-by-query.
- Estimated bidder values are 40-90% higher than cost-per-click payments (substantial demand reduction / bid shading).
- GSP is strictly less efficient than VCG for the keywords studied. Revenue/efficiency tradeoff is keyword-specific.

[Stanford GSB PDF](https://gsb-faculty.stanford.edu/susan-athey/files/2022/04/structural_sponsored_search.pdf)

### "The Impact of Targeting Technology on Advertising Markets and Media Competition" (AER 2010)
With Gans.

- Better targeting unambiguously increases social welfare (more efficient matching).
- But targeting disproportionately benefits large general-audience platforms, which can now segment audiences to match what niche publishers offered naturally. Can harm niche/local publishers.
- Theoretical framework for why digital advertising concentrated around a few platforms.

[AEA](https://www.aeaweb.org/articles?id=10.1257/aer.100.2.608)

**Policy:** Chief Economist of DOJ Antitrust Division (2022-2024). Led drafting of 2023 Merger Guidelines, introducing frameworks for platform competition, network effects, and conflicts when a platform operator competes on its own platform.

---

## Navdeep Sahni (GSB, Marketing)

### "Does Advertising Serve as a Signal?" (Review of Economic Studies 2020)
With Nair.

- Field experiment: ~200K users, 13 Asian cities, 600+ restaurants. Randomly varied whether users saw the "Sponsored" label.
- Disclosing that a listing is a paid ad **increased calls by 77%**. Consumers interpret "this business paid for placement" as a positive quality signal.
- Effect is stronger under greater uncertainty (unfamiliar city, fewer ratings, newer restaurants).
- Both consumers and advertisers benefit: consumers shift toward better-rated restaurants in the disclosure group.

[Oxford Academic](https://academic.oup.com/restud/article-abstract/87/3/1529/5583745) | [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2721468)

### "Advertising Spillovers" (JMR 2016, Paul Green Award, Weitz-Winer-O'Dell Award)

- Field experiments on a restaurant platform. When a restaurant advertises, competitors' sales also increase.
- Spillovers concentrate on same-cuisine, high-rated competitors. Ads category-prime consumers, not just brand-prime.
- At low frequency, spillovers are largest. As frequency increases, spillovers shrink and the advertiser captures more.

[SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2440907) | [JMR](https://journals.sagepub.com/doi/10.1509/jmr.14.0274)

### "Are Consumers Averse to Sponsored Messages?" (QME 2024)
With Zhang.

- 3.3M US users. Reduced ad prominence for treatment group. Users in the reduced-ad group **decreased their overall search engine usage**. Revealed preference for ads.
- Traffic to newest websites dropped ~10% when ads were sidelined. Ads serve as a discovery mechanism for sites lacking organic ranking signals.
- Search ads fill information gaps the organic algorithm cannot.

[Springer](https://link.springer.com/article/10.1007/s11129-023-09270-z) | [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3441786)

---

## Dan Boneh (CS, Applied Cryptography)

### "Adnostic: Privacy Preserving Targeted Advertising" (NDSS 2010)
With Toubiana, Narayanan, Nissenbaum, Barocas.

- Behavioral profiling and targeting happens entirely within the user's browser. The ad network remains "agnostic" to user interests.
- Cryptographic billing: advertisers can be charged correctly without the network knowing which ad was displayed.
- Implemented as a Firefox extension. Anticipated by a decade the architecture of Google's Privacy Sandbox and FLEDGE/Protected Audiences.
- The core insight (move targeting to client, keep exchange blind) is the template for on-device auction designs.

[Project page](https://crypto.stanford.edu/adnostic/)

### "Prio: Private, Robust, and Scalable Computation of Aggregate Statistics" (NSDI 2017)
With Corrigan-Gibbs.

- Servers compute statistical functions across client data while learning nearly nothing about individual values, as long as at least one server is honest.
- Introduces secret-shared non-interactive proofs (SNIPs): ~100x performance improvement over conventional zero-knowledge approaches.
- Can perform least-squares regression on high-dimensional data without seeing it in the clear.
- Adopted by Mozilla, Apple. Basis for IETF DAP standard used in Privacy Sandbox Attribution Reporting.

[arXiv](https://arxiv.org/abs/1703.06255) | [Project page](https://theory.stanford.edu/~dabo/abstracts/prio.html)

### "Divisible E-Cash for Billing in Private Ad Retargeting" (PoPETs 2024)
With Liao, Corrigan-Gibbs.

- Solves the billing gap: even with private ad selection and measurement, payment flows can leak user-level data. Uses divisible e-cash with zero-knowledge proofs so the exchange cannot link payer to payee.
- 250x faster than prior e-cash schemes. Adds <63ms latency, <3.2KB client communication. Operational costs <1% of ad spend.
- Completes the cryptographic toolkit for fully private ad systems (Adnostic for selection, Prio for measurement, e-cash for billing).

[PoPETs](https://petsymposium.org/popets/2024/popets-2024-0104.php)

---

## Ravi Jagadeesan (Economics)

### "The Limits of Auctions under Ex-Ante Collusion" (R&R at Econometrica, 2025)
With Segal, Tordjman.

- Even with private information about values, ex-ante collusion allows bidders to overcome information asymmetry and collude efficiently.
- Revenue ceiling = posted price. No auction mechanism beats a take-it-or-leave-it price when ex-ante collusion is possible.
- Optimal collusion-robust mechanism: posted price + seller-run first-price knockout auction. The seller internalizes the ring's coordination problem.

[SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5231187)

### "Auctions with Withdrawal Rights: A Foundation for Uniform Price" (R&R at AER; EC'25 Exemplary Theory Paper)
With Haberman.

- When bidders can withdraw after winning (ex-post exit), the class of implementable mechanisms shrinks dramatically.
- Withdrawal forces optimal mechanisms toward uniform pricing, even with correlated values.
- "Double deviations" (misreport then selectively withdraw) are the key threat. Complex price-discrimination mechanisms fail.
- If your platform cannot enforce commitment, you are constrained to uniform pricing.

[ACM](https://doi.org/10.1145/3736252.3742489)

---

## Ellen Vitercik (MS&E / CS)

### "Sample Complexity of Automated Mechanism Design" (NeurIPS 2016)
With Balcan, Sandholm.

- First sample complexity analysis for deterministic combinatorial auction classes used in automated mechanism design.
- Pseudo-dimension of the Affine Maximizer Auction class is Theta(d). Sample complexity ~O(d/epsilon^2).
- Revenue in these auctions is piecewise linear in mechanism parameters, which makes learning-theoretic analysis tractable.
- With enough bid data, the auction you find on training data will generalize to unseen bidders.

[arXiv](https://arxiv.org/abs/1606.04145) | [NeurIPS](https://proceedings.neurips.cc/paper/2016/hash/c667d53acd899a97a85de0c201ba99be-Abstract.html)

### "Generalization Guarantees for Multi-Item Profit Maximization" (EC 2018 / Operations Research 2025)
With Balcan, Sandholm.

- Unified theory covering pricing, auctions, and lottery mechanisms. The unifying property: profit is piecewise linear in parameters for any fixed buyer values.
- Covers item-pricing, bundle-pricing, multi-part tariffs, second-price with non-anonymous reserves, lotteries, and generalized VCG.
- Data-dependent guarantees: tighter bounds when the distribution is well-behaved.

[arXiv](https://arxiv.org/abs/1705.00243) | [Operations Research](https://pubsonline.informs.org/doi/10.1287/opre.2021.0026)

### "Estimating Approximate Incentive Compatibility" (EC 2019, Exemplary AI Track Paper)
With Balcan, Sandholm.

- Given samples from agents' types, estimates how far a mechanism is from incentive compatible.
- Constructs a finite subset of the type space where the maximum utility gain from misreporting nearly matches the true maximum over the full space.
- Application-agnostic: works on first-price, GSP, uniform-price, discriminatory auctions.
- Closes the loop: optimize for revenue, then check incentive violations on data, then re-optimize.

[arXiv](https://arxiv.org/abs/1902.09413) | [EC](https://dl.acm.org/doi/10.1145/3328526.3329628)
