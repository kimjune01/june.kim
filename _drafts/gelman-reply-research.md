# Gelman reply research log

### H2: Economic/sociological structural view (opus, needs-verification)

**Verdict:** Science on Trial diagnoses the symptom (96% positive rate) as an epistemic failure of reviewers and authors. The economics-of-science literature predicts that rate from first principles about tournament funding, priority rules, and selection pressure on labs. If the reply to Gelman stays in the "hypotheses are vague" frame, it cedes the stronger argument: the problem isn't that scientists reason badly, it's that the ones who reason carefully get outcompeted.

**Key claims from the literature:**
- **Priority rule creates winner-take-all publication.** Dasgupta & David ("Toward a New Economics of Science," *Research Policy* 1994) model science as a reputation economy where only the first publisher of a result captures credit. Null results and replications earn near-zero priority rent, so rational agents underproduce them. The 96% positive rate is the equilibrium, not a deviation.
- **Tournament funding amplifies risk-aversion at early career, risk-seeking at tenure.** Stephan (*How Economics Shapes Science*, Harvard 2012) documents that grant-dependent labs (postdocs, pre-tenure PIs) face convex payoffs: a positive result funds the next cycle, a null doesn't. This matches your Exhibit 2 "third option" — but Stephan frames it as structural, not as individual timidity.
- **Selection, not reasoning, explains declining quality.** Smaldino & McElreath ("The natural selection of bad science," *Royal Society Open Science* 2016) show via agent-based model that even with no individual cheating, labs with lower methodological standards produce more publications, attract more students, and propagate their methods. Rigor is selected against at the population level.
- **Replication is a public good with no private producer.** Heesen ("Why the reward structure of science makes reproducibility problems inevitable," *J. Phil* 2018) formalizes this: replicating others' work is dominated by doing novel work under any priority-based credit scheme. The crisis is a coordination failure, not an ethical one.
- **Well-ordered science requires institutional design, not better reviewers.** Kitcher (*Science, Truth, and Democracy*, 2001) argues the allocation of scientific effort is a social choice problem; expecting individual reviewers to correct it is category-mistaken.

**Interventions Science on Trial doesn't consider:**
- **Lottery grants above a quality threshold** (proposed by Fang & Casadevall; piloted by NZ Health Research Council, SNSF). Removes tournament dynamics once minimum bar is met.
- **Registered Reports / results-blind review** (Chambers, Nosek). Funds/publishes on design quality before outcome known. Directly attacks the 96% selection filter.
- **Funding nulls and replications as first-class outputs** (Munafò et al., "A manifesto for reproducible science," *Nat Hum Behav* 2017).
- **Post-publication review markets** (e.g., Prediction markets on replication — Dreber et al. 2015 showed markets outperform experts at predicting which findings replicate).
- **Tournament redesign:** cap publications per year per author (Nelson); staggered/rolling grants; team-science credit allocation.

**Smaldino & McElreath's argument, compressed:**
Model labs as reproducing entities. Each lab has a "methodological rigor" trait that lowers false-positive rate but also lowers publication rate. Students inherit methods from advisors. Hiring/funding selects on publication count. Simulation: rigor declines monotonically across generations even when no individual is dishonest and peer review catches some fraction of bad work. **The mechanism is evolutionary, not epistemic.** Implication: telling scientists to reason better is like telling bacteria to stop evolving resistance. You have to change the selection environment.

**Where user's framing is epistemic when it should be structural:**
- "Reviewers approve vague hypotheses" → reviewers are selected by the same process; the vague-hypothesis equilibrium is stable because vague-hypothesis labs outreproduce precise-hypothesis labs.
- "Career-preserving risk aversion" (Exhibit 2 third option) is framed as individual psychology. Stephan/Smaldino would frame it as the *only* surviving strategy after decades of selection — not a choice scientists make but a trait filter they passed through.
- "96% positive rate is suspicious" treats the rate as evidence of malpractice. Priority-rule economics predicts ~100% positive rate at equilibrium; any deviation downward would be the surprise.
- The "credentialed publishing" critique personifies the system (journals as gatekeepers). The structural view: journals are also selected — rigorous journals lose citations and fold.

**Key references:**
- Smaldino & McElreath 2016, *Royal Society Open Science*: https://royalsocietypublishing.org/doi/10.1098/rsos.160384
- Stephan 2012, *How Economics Shapes Science*, Harvard UP
- Dasgupta & David 1994, *Research Policy* 23(5): https://doi.org/10.1016/0048-7333(94)01002-1
- Heesen 2018, "Why the Reward Structure of Science Makes Reproducibility Problems Inevitable," *Journal of Philosophy*
- Munafò et al. 2017, "A manifesto for reproducible science," *Nature Human Behaviour*
- Dreber et al. 2015, "Using prediction markets to estimate the reproducibility of scientific research," *PNAS*
- Fang & Casadevall 2016, "Research funding: the case for a modified lottery," *mBio*

**Open questions for user:**
- Do you want the reply to Gelman to stay epistemic (where he's strongest) or pivot structural (where the argument is stronger but he's not the ideal interlocutor)?
- Is Science on Trial arguing "science reasons badly" or "science is selected for bad reasoning"? These require different remedies and different opponents.
- Smaldino & McElreath is the single most-cited structural paper and isn't in your post. Adding it reframes the whole piece — worth a dedicated exhibit?

### H4: Contra-replicationist minority (opus, needs-verification)

**Verdict:** The strongest contra-crisis arguments are not denials of the crisis but constraints on its scope: moderator effects are real, "failed replication" is a noisier signal than reformers admit, and the replication movement has its own methodological monoculture. Science on Trial is mostly right about the base rates but may overgeneralize from social psychology to "science" writ large.

**Steelman arguments against the crisis narrative:**
- **Moderator variables and hidden auxiliaries** (Stroebe & Strack, 2014, *Perspectives on Psychological Science*, "The Alleged Crisis and the Illusion of Exact Replication"). Their argument: in psychology, "direct replication" is a category error because stimulus materials, cultural context, demand characteristics, and subject pool demographics are part of the manipulation. A failed replication across populations is evidence about generalizability, not about whether the original effect exists. This is a real epistemological point, not a dodge — it maps to Cartwright's "nomological machines" in philosophy of science.
- **Reverse p-hacking in replications** (Bem-Utts-Johnson 2011 response; also gestured at by Schwarz). Pre-registered replications can be underpowered against the original effect size while being advertised as definitive. If the replication's power is 50% against the true effect, a null finding is a coin flip, not a refutation. Many Many Labs replications used sample sizes chosen for the *expected* effect, not the *published* effect, guaranteeing asymmetric conclusions.
- **The "crisis" is localized** (Fanelli, 2018, *PNAS*, "Is science really facing a reproducibility crisis, and do we need it to?"). Fanelli's bibliometric review argues the empirical case for a systemic crisis across science is weak; social psychology and parts of cancer biology are real hot spots, but physics, chemistry, and much of biomedicine show stable base rates of retraction and error correction. Generalizing "science is in crisis" from OSC 2015 is itself a sampling error.
- **Reform-movement biases** (Vazire 2020, "Do We Want to Be Credible or Incredible?"; also Devezer et al. 2021, "The case for formal methodology in scientific reform"). Even reform-sympathetic voices have noted that the reform camp treats "replicates" as binary, underweights theoretical progress, and has a selection bias toward findings that are easy to replicate (simple priming paradigms) versus findings that are hard to replicate but true (complex field effects).
- **Kahneman's 2017 letter** (comment on Schimmack's R-index blog, Feb 2017): conceded that priming results he cited in *Thinking, Fast and Slow* Ch. 4 were built on sand, but argued the *mechanism* (automatic associative activation) survives — the specific paradigms were fragile, the theory wasn't. The distinction between paradigm-fragility and theory-falsehood is real and Science on Trial may elide it.

**Where Science on Trial may overclaim:**
- The "96%" figure (if it's the Ioannidis-style claim or the OSC 39% replication rate inverted into a failure rate) is not stable across subfields. OSC 2015: ~39% replicated. Camerer et al. 2018 (Nature Human Behaviour, social science in *Nature*/*Science*): ~62% replicated. Cancer Biology Reproducibility Project (2021): ~46% of effects replicated but with much smaller effect sizes. These are different numbers for different questions.
- "Replication failure" is often operationalized as "p > .05 in the replication" which inherits all the problems of NHST the reform movement is supposed to be critiquing. Effect-size-based replication criteria give meaningfully different numbers.
- If Science on Trial frames the crisis as evidence that *science itself* is broken rather than that *significance-testing-driven subfields with small samples and flexible measurement* are broken, it's proving too much. Gelman's own position is the narrower one.

**Gelman's position in intra-reform disputes:**
- Gelman is reform-aligned but is *not* a "p-curve" or "p < .005" partisan. He disagreed with Benjamin et al. 2018 ("Redefine Statistical Significance") — his view is that the p-value threshold is the wrong lever; the problem is the dichotomization itself ("The Difference Between 'Significant' and 'Not Significant' Is Not Itself Statistically Significant," 2006).
- Gelman vs. Simonsohn on p-curve: Gelman has argued p-curve analyses are sensitive to model assumptions that Simonsohn underweights.
- Gelman vs. Ioannidis: sympathetic but has pushed back on the "most published findings are false" framing as rhetorically strong but mathematically sensitive to prior specification.
- Gelman engaged Fiske directly (blog post, Sept 2016, "What has happened down here is the winds have changed") — measured, not contemptuous. Worth reading before replying to him; his tone is a model.

**Key references:**
- Stroebe & Strack 2014, *Perspectives on Psychological Science* 9(1): 59-71.
- Fanelli 2018, *PNAS* 115(11): 2628-2631.
- Fiske 2016, APS Observer, "A Call to Change Science's Culture of Shaming."
- Gelman 2016 blog, "What has happened down here..." (statmodeling.stat.columbia.edu).
- Vazire 2020, *Perspectives on Psychological Science* 15(1): 17-26.
- Devezer, Navarro, Vandekerckhove, Buzbas 2021, *Royal Society Open Science* 8: 200805.
- Camerer et al. 2018, *Nature Human Behaviour* 2: 637-644.
- Kahneman 2017 comment on Schimmack, "Reconstruction of a Train Wreck."

**Open questions for user:**
- Does your reply to Gelman need to concede *any* ground to the contra side, or is it scoped tightly enough (your own subfield, your own evidence) that the intra-reform debate is off-topic?
- Do you want to cite the 39% vs. 62% vs. 46% numbers to show subfield variance, or does that muddy the argument?
- Is the Stroebe/Strack "exact replication is impossible" point worth engaging as a partial concession, or does it play into the evasion pattern Gelman critiques?

### H1: Mayo severity framework (opus, needs-verification)

**Verdict:** If the user engages Mayo, the Science on Trial argument shifts from "credentialed publishing is broken" to "reform proposals must satisfy a severity requirement or they reproduce the same failure under new labels." Mayo is the reason Gelman's "hypothesis vagueness" charge has real teeth: vague hypotheses can't be severely tested, period, regardless of whether the test is frequentist or Bayesian.

**Key claims from Mayo:**
- **Severity requirement (strong):** "We have evidence for claim C just to the extent C survives a stringent scrutiny." If a test had high capability to find flaws in C and found none, passing is evidence for C. (Mayo 2018, *SIST*, Excursion 1.)
- **Weak severity (BENT — "bad evidence, no test"):** "If data x agree with C but the method was practically incapable of finding flaws with C even if they exist, then x is poor evidence for C." The minimum bar any reform must clear.
- **Replication-crisis diagnosis:** failures come from selection effects — data dredging, optional stopping, multiple testing, HARKing — all of which destroy the error probabilities that make a test severe. The villain is not p-values; the villain is practices that break the sampling distribution (SIST Excursion 4).
- **Anti-reform warning:** "Statistical reforms intended to improve credibility will do the opposite if they violate the weak severity requirement." Targets: naive Bayes factors, "estimation instead of testing" when the estimate inherits the same selection bias, and "redefine significance" moves that don't address selection effects.
- **Error probabilities ≠ long-run betting frequencies.** They are properties of the testing procedure that license the specific inference at hand. This distinguishes her from both Neyman-Pearson behaviorism and subjective Bayes.

**Where Mayo and Gelman differ:**
- Gelman + Shalizi (2013) recast Bayesian workflow as hypothetico-deductive: fit model, do posterior predictive checks, falsify, revise. Mayo's 2013 reply argues their PPC is severity-*flavored* but lacks explicit error probabilities — a PPC p-value is conditional on the model and doesn't control error rates across the model-space actually searched.
- Gelman rejects the primacy of error rates ("Mayo doesn't get to dictate that frequency of errors is all that matters"). Mayo insists that without error probabilities you cannot say how severely a claim was tested.
- Gelman is comfortable with flexible model expansion after seeing data; Mayo treats unaccounted-for expansion as a biasing selection effect.
- On priors: Gelman uses weakly informative priors as regularization; Mayo is skeptical that any prior-based account captures "what the data were capable of ruling out."

**Where Mayo would press on Science on Trial:**
- The post treats the failure as sociological (credentialing, gatekeeping). Mayo would say the failure is **methodological**: selection effects break severity, and no governance reform (open review, post-publication critique, LLM pre-review) fixes that unless it restores error control.
- "LLM pre-review" as an exhibit: what error probabilities does the LLM reviewer have? If it accepts/rejects on surface features, it's a weak-severity tool at best — and might make things worse by laundering BENT evidence through a new gatekeeper.
- The "trophy case / citation count" framing rewards attention. Severity cuts orthogonally — a highly cited claim never severely tested is still BENT.
- Gelman's "hypothesis vagueness" flag is a severity complaint in disguise. A vague hypothesis cannot be severely probed because no data pattern counts as a flaw. The user should concede this is a real methodological defect, not just stylistic.
- Mayo would resist the implicit frame that Bayesian workflow is the cure. Both frequentist-NHST-as-practiced and casual Bayesian workflow fail severity; the fix is pre-designated tests with stated error probabilities, whichever school.

**Key references:**
- Mayo (2013), "The error-statistical philosophy and the practice of Bayesian statistics: comments on Gelman and Shalizi" — https://errorstatistics.files.wordpress.com/2020/10/mayo-2013-comments-gelman-shalizi.pdf
- Gelman + Shalizi (2013), "Philosophy and the practice of Bayesian statistics," *BJMSP* — https://sites.stat.columbia.edu/gelman/research/published/philosophy.pdf (paper Mayo is replying to)
- Gelman's blog: "Philosophy of Bayes and non-Bayes: dialogue with Deborah Mayo" (2010) — https://statmodeling.stat.columbia.edu/2010/09/22/philosophy_of_b/
- Gelman's multi-reviewer symposium on *SIST* (2019) — https://sites.stat.columbia.edu/gelman/research/unpublished/mayo_reviews.pdf
- Mayo (2018), *Statistical Inference as Severe Testing*, Cambridge — https://www.cambridge.org/core/books/statistical-inference-as-severe-testing/D9DF409EF568090F3F60407FF2B973B2
- errorstatistics.com, "Severity: Strong vs Weak" — https://errorstatistics.com/2019/10/10/severity-strong-vs-weak-excursion-1-continues/

**Terminology to deploy:**
- *Severity requirement* (weak vs strong) / *BENT*
- *Error probabilities* (properties of the procedure, not long-run frequencies)
- *Pre-designated tests* (vs researcher degrees of freedom)
- *Biasing selection effects* (Mayo's umbrella: data dredging, optional stopping, multiple testing, HARKing)

**Open questions for user:**
- Do you want to concede Gelman's vagueness point by reframing Science on Trial as "credentialing fails because it doesn't enforce severity," or hold the sociological frame and argue severity is downstream of incentives?
- Willing to admit the LLM pre-review exhibit is weak-severity by construction? That's the honest read.
- Should the reply cite Mayo 2013 directly? Signals you've read the other side of Gelman's own debate and raises the ceiling of the exchange.

### H3: Measurement/construct critique (opus, needs-verification)

**Verdict:** Science on Trial diagnoses a filtering/spin pathology downstream of NHST; Meehl + the modern construct-validity school argue the pathology is upstream — the null is ~never literally true, constructs don't map cleanly onto measures, so the significance-testing apparatus is a category error in soft science. Citing Ioannidis/Sterling/Fanelli without Meehl is a real gap, especially given that Gelman himself re-read Meehl 1967 on his blog in January 2026.

**Meehl's core argument:**
- 1967 "Theory-testing in psychology and physics: A methodological paradox" (*Philosophy of Science* 34:103–115): in physics, sharper instruments make theories harder to corroborate (narrower tolerance = stricter test). In psychology, higher statistical power makes directional-difference nulls easier to reject — prior probability of "significant in predicted direction" approaches ½. Success corroborates very weakly, and weaker as N grows. A structural inversion, not a craft failing.
- The "crud factor": Meehl's Minnesota data (n≈55,000 high-schoolers, 45 miscellaneous variables) showed ~91% of pairwise associations significant, many at p<10⁻⁶. Everything correlates with everything at some level. The nil null is essentially never true in observational soft science, so rejecting it carries almost zero information about a substantive theory.
- 1990 "Why summaries of research on psychological theories are often uninterpretable" (*Psychological Reports* 66:195–244) hardens this: NHST in soft psych is "a potent but sterile intellectual rake." Meta-analyses inherit the uninterpretability.
- 1997 "The problem is epistemology, not statistics": fiddling with Bayes factors, CIs, preregistration addresses symptoms. The disease is that verbal theories in soft science don't entail point predictions, so no statistical apparatus can do the corroboration work it's asked to do.

**Modern construct-validity critique:**
- Flake & Fried 2020, "Measurement Schmeasurement" (*Advances in Methods and Practices in Psychological Science*): ad-hoc scales, unvalidated measures, silent modifications ("questionable measurement practices") are a hidden layer of researcher degrees of freedom beneath the QRPs Simmons et al. named. "Neither rigorous research design, nor advanced statistics, nor large samples can correct such false inferences" when constructs are undefined.
- Yarkoni 2020, "The generalizability crisis" (*BBS*): verbal theories in psychology are radically under-constrained by their statistical models. Stimuli, tasks, operationalizations are treated as fixed when inferences are meant to generalize over them. Under realistic random-effects modeling, nominal α=.05 tests can carry true false-positive rates above 60%. The fix isn't better stats; it's either narrowing claims to the specific operationalization or building measurement models that earn the generalization.
- Loken & Gelman 2017, "Measurement error and the replication crisis" (*Science* 355:584–5): the folk intuition that a significant effect found under noisy measurement must be "really strong" is backward. Significance-filtering + measurement error inflates effect sizes (Type M) and flips signs (Type S). Gelman's own position is closer to Meehl than the 2014 reply suggested.

**How this reframes the 96% diagnosis:**
- Science on Trial reads 96% positive as a spin/filter artifact: authors frame ambiguous results as wins, peer review waves them through, the registry would show something different. The null-flex pivot empirically found exactly that (abstract↔registry divergence).
- The construct-validity read: in soft science, ~100% positive is what you'd expect *even without spin*, because the crud factor guarantees directional effects on nearly any plausible comparison, and because "supports the hypothesis" has many escape hatches when the construct↔measure link is loose. Spin is one mechanism; crud + construct slack is the other. They compound.
- Implication for the post: the binary "primary outcome met / not met" frame is cleanest in clinical trials (mortality, HbA1c, tumor volume) and degrades as you move to psychology/education/econ, where the "primary outcome" is itself a contested operationalization. Gelman's 2014 complaint that the original paper's measurements weren't obviously probing the hypothesis is a special case of this.

**How this is narrower than Gelman's 2014 reply:**
- Gelman treats measurement quality as one concern among many and stays inside the significance-testing paradigm to critique it. Meehl says the paradigm is misapplied. The construct-validity school (Flake, Fried, Yarkoni) sits between: measurement can be reformed, but only if you first admit you haven't been measuring what you claimed.
- Gelman's "hypothesis vagueness" point is about underspecified verbal hypotheses. Meehl's point is stronger: even precisely-stated hypotheses over soft constructs test something other than the theory, because the construct↔measure link is the load-bearing assumption and it isn't defended.

**What this implies for null-flex / VRI:**
- VRI (journal × specialty × trial-type representativeness vs. registered-null rate) is robust to Meehl in clinical-trials territory, because the primary outcome is a physical measurement with a pre-specified threshold. The registry field carries construct validity roughly for free.
- Extend VRI off clinical trials — to social/behavioral registries (AsPredicted, OSF), education RCTs, econ field experiments — and "primary outcome met" inherits construct slack. "Met" becomes renegotiable downstream of the registration.
- Concretely: VRI is a measurement of measurement integrity, which only works where measurement exists. Ship first on ClinicalTrials.gov. Document explicitly that extension to softer registries requires a per-field construct-validity audit, not just ratio computation.
- The null-flex post already surfaces this implicitly ("the registry is what actually happened"). Worth naming that this holds because clinical endpoints are physical, and flagging it as the boundary condition for the tool. Lesson three in that post ("the instrument tells you about the question") is structurally Meehlian — the tool discovered it was measuring the measurement rather than the phenomenon.

**Key references:**
- Meehl 1967, "Theory-testing in psychology and physics": https://meehl.umn.edu/sites/meehl.umn.edu/files/files/074theorytestingparadox.pdf
- Meehl 1990, "Why summaries of research on psychological theories are often uninterpretable": *Psychological Reports* 66:195–244 (meehl.umn.edu publications archive)
- Meehl 1997, "The problem is epistemology, not statistics": in Harlow, Mulaik & Steiger, *What If There Were No Significance Tests?* (meehl.umn.edu publications archive)
- Flake & Fried 2020, "Measurement Schmeasurement": https://journals.sagepub.com/doi/10.1177/2515245920952393
- Yarkoni 2020, "The generalizability crisis" (*BBS*): https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/generalizability-crisis/AD386115BA539A759ACB3093760F4824
- Loken & Gelman 2017, "Measurement error and the replication crisis" (*Science*): https://www.science.org/doi/10.1126/science.aal3618
- Gelman 2026-01-28 re-read of Meehl 1967: https://statmodeling.stat.columbia.edu/2026/01/28/ok-i-reread-that-classic-paper-by-paul-meehl-and/

**Open questions for user:**
- Does the reply name Meehl explicitly? Failing to, while Gelman just re-read him in Jan 2026, is an easy strike. Clean move: one-line acknowledgment that Meehl is upstream of the Science on Trial diagnosis — you're naming the filter, he's arguing the filter can't be fixed by stats alone.
- Is VRI scoped to clinical trials on purpose, or is the intent to generalize? If former, say so; if latter, construct validity needs addressing before extension.
- Worth a paragraph in the Science on Trial follow-up on "why clinical trials are the easy case"? Reads as intellectual honesty and pre-empts the Meehl objection.
- The third null-flex lesson ("the instrument tells you about the question") is structurally Meehlian. Naming Meehl there would tighten the arc without changing the argument.

---

## Codex convergence pass (GPT-5.4, adversarial)

**Overall strength ranking:** H3 > H2 > H1 > H4.

### H3 — SURVIVED (strongest)

Genuine blind spot. Strongest citation bundle. Connects directly to Gelman's hypothesis-vagueness complaint (Meehl is upstream of it). Gelman himself re-read Meehl 1967 on 2026-01-28, which makes this a live topic for him.

Corrections to apply before citing:
- "91% of pairwise associations significant" — pin the exact Meehl source; the anecdote is famous but the writeup is too confident.
- Yarkoni "false-positive rates above 60%" — soften; his point is about alignment/generalization failure, not a single headline number.
- "Clinical endpoints give construct validity roughly for free" — too strong; say "better than soft constructs" and stop.

Additions the H3 subagent missed: **Cronbach & Meehl 1955** (canonical construct validity paper) and **Borsboom-style measurement theory**. A Gelman reply that invokes Meehl and omits Cronbach & Meehl 1955 reads unread.

### H2 — SURVIVED with caveats

Partial blind spot. The genuinely novel claim is **bad science is selected for, not tolerated** (Smaldino & McElreath's evolutionary argument). Incentive/structural view itself is standard reform territory.

Corrections:
- "Priority-rule economics predicts ~100% positive rate at equilibrium" — high-severity overclaim; none of the cited works warrant this strength.
- Dasgupta & David 1994 is being used too specifically; the paper is broad institutional economics, not a derivation of 96%.
- Stephan gloss on "risk-aversion at early career, risk-seeking at tenure" reads like reconstruction; needs securer source or softer framing.
- Kitcher is ornamental; drop or anchor to specific claim.

Additions missed: Merton on priority-rule sociology, Campbell's Law, empirical grant-review/payline literature.

### H1 — SURVIVED but 3rd rank

Genuine but adjacent to Gelman's own long-running stats-foundations debates. Mayo's 2013 reply to Gelman-Shalizi is the right citation. Sharpens a reply; doesn't transform the frame like H3 would.

Corrections:
- The Mayo writeup overstates how directly she targets specific reform memes ("estimation instead of testing," "redefine significance"); soften or source.
- "Gelman's vagueness complaint is a severity complaint in disguise" is our inference, not Mayo's or Gelman's framing. Flag accordingly.

Additions missed: one concrete worked example of what a *severe* test of the blog's target claims would look like. Without that, H1 stays philosophical. Stephen Senn / Mayo-Spanos distinctions between error control, model checking, and flexible model revision would add teeth.

### H4 — PRUNED

Not a genuine blind spot. Standard intra-reform debate Gelman knows cold. Useful for scope calibration but not a new angle.

Reasons for pruning:
- **Citation defect (high):** Vazire "Do We Want to Be Credible or Incredible?" is a 2019 APS Observer piece, not a 2020 *Perspectives on Psychological Science* article. Citing it wrong to Gelman would be an own-goal.
- **Weak support (medium):** Many Labs sample-size complaint is not well supported; those projects were typically high-powered. The asymmetric-conclusion claim needs better sourcing or removal.
- **Weak frame (medium):** "Bem-Utts-Johnson 2011 response" is too vague to be a usable citation.
- **Fanelli mischaracterized (low):** his 2018 target is the overblown *crisis narrative*, not a clean all-clear for most fields.

H4's one legitimate contribution (subfield variance in replication numbers — OSC 39%, Camerer 62%, RPCB 46%) can be salvaged as a scope note in the Science on Trial piece without needing the full contra-replicationist framework. Move that one fact; drop the rest.

## What's missing across all four

Codex flag: the four hypotheses blur four distinct levels. The reply strategy should separate them:
1. **Scientific hypothesis precision** (Gelman's 2014 point; H1 formalizes, H3 goes upstream)
2. **Measurement validity** (H3)
3. **Selection incentives** (H2)
4. **Replication metrics** (H4 residual)

Gelman's specific complaint lives at level 1, upstream-extended to level 2. H3 hits his complaint most directly.

**Reply-craft note:** if the goal is to answer Gelman specifically rather than write a broader manifesto, H3 + selected parts of H1 are the highest-yield materials. H2 is the strongest frame for a separate post.
