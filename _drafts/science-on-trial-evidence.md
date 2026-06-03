# Science on Trial — Evidence Log

Research log for fan-out: marshaling concrete evidence for the post "Science on Trial."

Each subagent reads this log before starting, appends their findings, and notes convergence/contradiction with prior entries.

## Hypotheses

- **H1:** Major fraud cases where peer review failed and outside forensics succeeded. Peer review as pre-trial screening cannot catch perjury.
- **H2:** Replication crisis numbers across fields. Quantify the gap between published and replicable.
- **H3:** Citation-graph failures. Retracted or failed-to-replicate papers continue to be cited as evidence.
- **H4:** Pre-registration natural experiments. Where mandatory chain-of-custody collapsed positive-result rates.
- **H5:** Post-publication review as a functioning outside jury. Data Colada, Bik, PubPeer, Retraction Watch.

---

## Findings

(subagents append below)

### H2: Replication crisis numbers across fields (opus, complete)

**Verdict:** The gap between published and replicable is not a rumor. Across six independent, pre-registered, high-powered projects spanning psychology, cancer biology, pharma, economics, and social science, replication rates cluster between 11% and 62%. Effect sizes, when they do replicate, shrink to roughly half. No field systematically tested has come back clean.

**Claims:**

- **Psychology — 36% / 39%.** Open Science Collaboration (Nosek et al. 2015) attempted to replicate 100 experimental and correlational studies from three top psychology journals (2008 issues of *Psychological Science*, *JPSP*, *JEP:LMC*). 97% of originals reported p<.05; only **36% of replications** reached p<.05; **39%** were subjectively judged to have replicated; mean replication effect size was about half the original. [Science paper](https://www.science.org/doi/10.1126/science.aac4716) · [PubMed](https://pubmed.ncbi.nlm.nih.gov/26315443/)

- **Cancer biology (industry) — 11%.** Begley & Ellis 2012 (*Nature*) reported Amgen oncology scientists could confirm findings in **only 6 of 53** "landmark" preclinical cancer papers (~11%). Methodology and paper identities were not disclosed due to confidentiality agreements — a caveat that has been criticized. [Nature comment](https://www.nature.com/articles/483531a)

- **Cancer biology (academic) — ~40% of positive effects; 5 of 17 "mostly replicated".** Reproducibility Project: Cancer Biology (Errington et al. 2021, *eLife*) tried to replicate experiments from 53 high-impact cancer papers (2010–2012). Scope collapsed: only **50 of 193 planned experiments** (26%) were completed — many were abandoned because original methods were missing. Of 158 comparable effects, original positive results replicated **40%** of the time vs 80% for null results. Editors' holistic assessment of 17 completed replication studies: **5 reproduced important parts**, 6 partial/mixed, 2 uninterpretable, 4 failed. Raw data publicly accessible for just **2%** of experiments. [eLife summary](https://elifesciences.org/articles/71601)

- **Pharma preclinical — ~21–25%.** Prinz, Schlange & Asadullah 2011 (*Nature Reviews Drug Discovery*). Bayer reviewed 67 internal in-house target-validation projects against published literature: data fully reproduced in **14**, partially in 10, major inconsistencies in 43. Translates to ~20–25% full reproducibility. Caveat: commentary, not a formal project; papers not named. [Nature Rev Drug Discov](https://www.nature.com/articles/nrd3439-c1)

- **Experimental economics — 61%.** Camerer et al. 2016 (*Science*). 18 lab experiments from *AER* and *QJE* (2011–2014), pre-registered replications at ≥90% power. **11 of 18 (61%)** showed a significant same-direction effect. Replicated effects averaged **66%** of the original magnitude. [Science paper](https://www.science.org/doi/10.1126/science.aaf0918)

- **Social science (Nature/Science) — 62%.** Camerer et al. 2018 (*Nature Human Behaviour*). 21 social-science experiments from *Nature* and *Science* (2010–2015), pre-registered, sample sizes ~5× originals. **13 of 21 (62%)** replicated with same-direction significant effect; average effect size ~**50%** of original. [Nat Hum Behav](https://www.nature.com/articles/s41562-018-0399-z)

- **Many Labs projects — mixed; replication rate depends on effect.** ML1 (Klein et al. 2014): **10/13 (77%)** effects replicated across 36 labs. ML2 (Klein et al. 2018): **14/28 (50%)** effects replicated across 125 samples, 15,305 participants. ML3 (Ebersole et al. 2016): **3/10 (30%)** across 21 samples; strongest finding was stability of effects *within* labs — variation across labs was small. Caveat: ML projects largely test classic/textbook effects, not fresh literature. [ML2 paper](https://journals.sagepub.com/doi/10.1177/2515245918810225)

- **Nutrition — everything is associated with cancer.** Schoenfeld & Ioannidis 2013 (*AJCN*). Picked 50 common ingredients from random cookbook recipes; **40 of 50 (80%)** had published studies claiming cancer association (39% increased risk, 33% decreased, 5% borderline). Effect sizes in meta-analyses were typically weak or null. Methodology: not a replication count but a claim-inflation demonstration — nutritional epidemiology produces findings faster than it produces truth. [AJCN](https://ajcn.nutrition.org/article/S0002-9165(23)05381-9/fulltext)

- **Medicine broadly — theoretical ceiling.** Ioannidis 2005 (*PLoS Medicine*), "Why Most Published Research Findings Are False." Not an empirical replication count; a Bayesian argument that given typical power, pre-study odds, bias, and multiple testing in biomedicine, the **positive predictive value of a published finding is often <50%**. Most-cited paper in PLoS Medicine history. Caveat: contested by statisticians (Goodman & Greenland 2007) as overstated, but the qualitative claim — that underpowered fields produce mostly false positives — has held up. [PLoS Med](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0020124)

- **AI/ML — no systematic replication rate yet; checklist compliance instead.** Pineau et al. 2021 (*JMLR*, NeurIPS 2019 Reproducibility Program). After introducing a Reproducibility Checklist, **>75% of accepted NeurIPS papers submitted reproducibility materials** (code, data, configs). This is an inputs metric, not an outputs metric — no large-scale study has yet attempted to re-run a random sample of NeurIPS/ICML papers and report a pass/fail rate. Separate work (Gundersen & Kjensmo 2018) reviewing 400 AI papers found only ~6% shared code and ~30% shared data at the time. [JMLR paper](https://jmlr.org/papers/v22/20-303.html)

**Convergence:** Independent projects using different methods converge on two numbers:
1. **Replication rate for positive effects lands in the 30–60% band** for psychology, social science, and economics; drops to ~11–25% in preclinical biomedicine.
2. **When effects do replicate, magnitudes shrink to ~50% of original.** This shows up in OSC 2015, Camerer 2016, Camerer 2018, and RPCB 2021 independently. The "winner's curse" of published literature is quantifiable.

**Strongest single number for the post:** **OSC 2015: 97% of originals significant → 36% of replications significant.** One field, 100 papers, one pre-registered protocol, published in *Science*. The gap between 97 and 36 is the entire thesis in two numbers. Begley's 6/53 is more dramatic but weakened by the undisclosed-paper-list caveat; OSC 2015 is fully open.

**Untested territory:**
- **Clinical trials (RCTs):** No systematic replication project on published positive RCTs. Relevant but different: Ioannidis 2005b showed 16% of highly-cited clinical findings were contradicted by later studies, but that's observational drift, not pre-registered replication.
- **Chemistry:** No organized replication project. A 2016 *Nature* survey (Baker) reported ~87% of chemists had failed to reproduce someone else's experiment, but no systematic sampling.
- **Physics, astronomy, earth science:** No cross-field replication projects. Anecdotal (OPERA neutrino, LK-99 superconductor) but not systematic.
- **Ecology and evolution:** Kelly 2019 and Fraser et al. 2018 surveyed p-hacking and HARKing prevalence; no formal replication count.
- **Neuroscience (human imaging):** Botvinik-Nezer et al. 2020 (*Nature*) showed 70 teams analyzing the same fMRI dataset reached materially different conclusions — a *multi-analyst* finding adjacent to replication. No systematic redo-the-experiment project.
- **Political science, sociology, anthropology:** Scattered replications; no Many Labs equivalent.
- **Machine learning:** As above — inputs tracked, outputs not.

The untested fields are themselves evidence: a century-old institution whose core epistemic claim is "our results are true" has produced *zero* pre-registered, high-powered, systematic replication audits for most of its own sub-disciplines.

**Open questions / caveats:**
- What counts as "replication" differs across projects: p<.05 same direction, effect-size overlap in CI, subjective holistic judgment, or meta-analytic pooling. OSC 2015 reports all four and gets 36%/47%/39%/68% respectively — the number shifts with the metric.
- Begley 2012 and Prinz 2011 are commentary pieces with undisclosed paper lists; the headline numbers are from industry memory, not a formal protocol. Still the only large-sample estimates available for preclinical pharma.
- Selection effects cut both ways: OSC 2015 picked papers by feasibility, which may overrepresent simple (and therefore more replicable) designs, *or* may have avoided the flashiest overclaims.
- Ioannidis 2005 is a model, not a measurement. Its frequent citation as "most research is false" elides that it's a conditional-probability argument.

### H4: Pre-registration natural experiments (opus, complete)

**Verdict:** Strong convergent evidence. Pre-registration collapses positive-result rates by roughly half to seven-eighths across independent natural experiments in cardiovascular trials, psychology, and FDA-regulated drug trials. The Kaplan & Irvin numbers check out exactly.

**Claims:**

- **Kaplan & Irvin 2015 (PLOS ONE):** 55 large NHLBI-funded RCTs (direct costs >$500k/year) on drugs or dietary supplements for cardiovascular disease, 1970–2012. Split at year 2000. Pre-2000: **17 of 30 (57%)** showed significant benefit on the pre-declared primary outcome. Post-2000: **2 of 25 (8%)**. χ²=12.2, p=0.0005. The mandate: prospective registration in ClinicalTrials.gov. Pre-2000, 0% of the trials were prospectively registered; post-2000, 100% were. Null was defined as CI for RR including 1.0 at α=0.05 two-tailed. Authors note that among post-2000 trials, 12 of 25 still reported significant effects on *secondary* outcomes — i.e., nearly half would likely have reported "positive" results had they not been forced to declare a primary outcome in advance. [https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0132382]

- **Scheel, Schijen & Lakens 2021 (AMPPS):** Compared 71 published Registered Reports (as of Nov 2018) against 152 random hypothesis-testing studies from standard psychology literature. Looked at the first hypothesis of each paper. Standard literature: **96% positive results.** Registered Reports: **44% positive results.** The gap (~52 points) is too large to explain by file-drawer alone; implies both publication bias and Type I inflation in standard reports. [https://journals.sagepub.com/doi/10.1177/25152459211007467]

- **Allen & Mehler 2019 (PLOS Biology):** Reported that ~61% of published Registered Reports in their sample had null results — roughly 5× the null-result rate observed in conventional articles across similar fields. Framed as evidence that RR format removes incentive to p-hack toward publishable positives. [https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3000246]

- **FDAAA 2007 (neuropsychiatric drugs cohort, Trials 2017):** Pre-FDAAA trials supporting FDA approval: FDA reviewers interpreted 76% as positive, but 98% were published as positive (22-point gap — the signature of selective reporting). Post-FDAAA: reviewers interpreted 91% as positive, 93% published as positive (2-point gap). Registration jumped from 70% to 100%. The gap between FDA's interpretation and published framing essentially closed. [https://trialsjournal.biomedcentral.com/articles/10.1186/s13063-017-2068-3]

**Convergent finding:** Across three independent domains (NHLBI cardiovascular trials, academic psychology, FDA drug approvals), imposing pre-registration reduces the published positive-result rate by roughly 50 percentage points or more. The effect is too large and too consistent to be drift in underlying science — the interventions studied post-mandate were not suddenly 7× less effective than pre-mandate. What changed is the chain of custody on the outcome.

**Strongest single exhibit for the post:**
1. **Kaplan & Irvin 2015** — cleanest natural experiment. Same funder (NHLBI), same disease area (cardiovascular), same trial-size threshold, single hard cutoff (year 2000), stark effect (57% → 8%). Numbers match the post brief exactly.
2. **Scheel et al. 2021** — best cross-check because it's a different field, different mechanism (journal-level RR policy rather than funder mandate), and matches the direction and rough magnitude (96% → 44%).

**Open questions / limitations:**
- *Kaplan & Irvin is correlational, not causal.* The year 2000 also coincides with improved trial conduct standards, DSMB practices, and statistical rigor. Authors acknowledge this. But their proposed mechanism — loss of ability to select the most successful outcome post-hoc — is supported by the finding that ~half of post-2000 trials still had a significant *secondary* outcome.
- Kaplan & Irvin sample is small (N=55) and restricted to large NHLBI cardiovascular trials; generalization to smaller trials or other funders is not tested.
- Scheel et al.'s RR sample is self-selected (authors who chose to submit RRs); possible that RR authors run more conservative hypotheses. Authors discuss and largely rule this out by matching design types.
- Allen & Mehler 2019 is a review/commentary — its "60%" figure is a summary of the earlier RR literature, not an original comparative dataset. For the post, prefer citing Scheel et al. directly.
- FDAAA result is a *publication-bias gap closing*, not a positive-rate collapse — the right frame for that exhibit is "reported results match reviewer interpretation," which is chain-of-custody talk, not effect-size talk.


### H1: Fraud cases where outside forensics succeeded (opus, complete)

**Verdict:** Strong exhibit. In virtually every marquee fraud case of the last 25 years, detection came from outside the formal peer-review channel — from lab insiders turned whistleblowers, independent bloggers, forensic statisticians, or journalists. Peer reviewers, when later asked, typically respond that they assumed data were real. That is exactly the pre-trial-screening vs. perjury distinction the post argues.

**Claims:**

- **Jan Hendrik Schön** (condensed-matter physics, Bell Labs, 1998–2002). Fabricated data across ~16 papers in Nature, Science, PRL during a "miracle year" run. Detected by Lydia Sohn (Princeton) and Paul McEuen (Cornell), who noticed *identical noise traces* in graphs from experiments run at wildly different temperatures — i.e. outside physicists reading published figures forensically, not reviewers. Bell Labs convened an external committee (Beasley report, Sep 2002); Schön fired Sep 24 2002; PhD later revoked. Peer reviewers at Nature/Science never caught the duplicated panels. [https://en.wikipedia.org/wiki/Sch%C3%B6n_scandal] [https://www.aps.org/apsnews/2022/08/september-2002-schon-scandal-report]

- **Diederik Stapel** (social psychology, Tilburg, ~1996–2011, ~15 years). 58 retractions (per Retraction Watch); Levelt/Noort/Drenth committees found fraud in 55 papers and 10 supervised PhD theses. Detected by three junior researchers in his own lab who noticed data too-clean-to-be-real and found identical score rows across unrelated studies. Pure whistleblower case — peer reviewers waved through impossibly tidy effects for a decade and a half. [https://en.wikipedia.org/wiki/Diederik_Stapel] [https://www.science.org/content/article/final-report-stapel-affair-points-bigger-problems-social-psychology]

- **Dan Ariely / Shu et al. 2012 PNAS** (behavioral economics, "sign-at-top" honesty paper). Fabricated auto-insurance field experiment data. Detected 2021 by anonymous tipsters plus Data Colada (Simonsohn, Nelson, Simmons) — distribution of miles-driven was uniform where it should have been right-skewed; The Hartford confirmed it supplied ~3,700 policies, not the ~13,000 in the paper. Retracted Sep 2021. Paper had been cited hundreds of times and was adopted by government agencies as actual policy nudge before retraction. Peer reviewers never checked the raw distribution. [https://datacolada.org/98] [https://retractionwatch.com/2021/09/14/highly-criticized-paper-on-dishonesty-retracted/]

- **Francesca Gino** (Harvard Business School, behavioral science, 2012–2020s). Data Colada's 2023 "Data Falsificada" four-part series documented manipulation across at least four papers (including the same Shu et al. 2012 paper — a second, independent fabrication on top of Ariely's). Harvard report (unsealed 2024) found intentional misconduct; tenure revoked May 2025 — first at Harvard in decades. Gino sued Data Colada for $25M; suit dismissed. Detection was entirely forensic blog work on posted datasets (sort-order anomalies, Excel calcChain metadata proving row edits). [https://datacolada.org/109] [https://datacolada.org/118] [https://www.science.org/content/article/honesty-researcher-committed-research-misconduct-according-newly-unsealed-harvard]

- **Paolo Macchiarini** (regenerative medicine / trachea transplants, Karolinska, 2008–2014). Synthetic-trachea transplants published in The Lancet and NEJM; most patients died. Detected by four clinical colleagues at Karolinska (Grinnemo, Corbascio, Simonson, Fux) who compared patient charts against published outcomes and found the papers misrepresented patient conditions. KI initially sided against the whistleblowers and reported them to police; only after an NYT leak and the Swedish documentary *Experimenten* did KI act. Macchiarini fired 2016; convicted of bodily harm in Sweden 2023. Papers misrepresented live patient outcomes — something peer review structurally cannot verify. [https://www.science.org/content/article/macchiarini-guilty-misconduct-whistleblowers-share-blame-new-karolinska-institute] [https://retractionwatch.com/2024/05/17/how-the-karolinska-protected-paolo-macchiarini-and-whistleblowers-paid-the-price/]

- **Hwang Woo-suk** (stem cells, Seoul National University, 2004–2005). Claimed patient-specific hESC lines in Science 2004 and 2005. Detected by a lab insider (Ryu Young-joon) who tipped the Korean MBC show *PD Notebook*; MBC's investigative episode plus Korean BRIC forum commenters spotted duplicated DNA fingerprint panels. Science retracted both papers Jan 2006. Indicted for fraud and embezzlement 2006. Detection was investigative journalism + lab whistleblower, zero peer review. [https://en.wikipedia.org/wiki/Hwang_affair] [https://www.nature.com/news/2005/051219/full/news051219-3.html]

- **STAP cells / Haruko Obokata** (stem cells, RIKEN, Jan 2014 publication). Two Nature papers claiming acid-bath pluripotency. Detected within *days* by readers of Paul Knoepfler's stem-cell blog and anonymous PubPeer commenters flagging image duplication and spliced gel lanes. Fully retracted July 2014 — five months end-to-end. Coauthor Yoshiki Sasai died by suicide. Nature explicitly conceded peer review "couldn't have detected" the fabricated images. Strongest case for "outside post-publication jury." [https://retractionwatch.com/2014/07/02/stap-stem-cell-papers-officially-retracted-as-nature-argues-peer-review-couldnt-have-detected-fatal-problems/] [https://www.science.org/content/article/evidence-mounts-against-reprogrammed-stem-cell-papers]

- **Yoshitaka Fujii** (anesthesiology, Japan, 1993–2011, ~19 years). 183 retractions — single-author record, ~7% of all retracted papers 1980–2011. Detected by John Carlisle, a British anesthetist who applied a chi-square-style distribution test to the baseline patient characteristics across Fujii's trials; the joint probability of the reported balance arising from real randomization was on the order of 1 in 10^30. Carlisle's test is now a standard forensic tool for journals. Pure statistical post-hoc forensics on already-peer-reviewed papers. [https://en.wikipedia.org/wiki/Yoshitaka_Fujii] [https://retractionwatch.com/2012/07/02/does-anesthesiology-have-a-problem-final-version-of-report-suggests-fujii-will-take-retraction-record-with-172/]

- **Brian Wansink** (food psychology, Cornell, ~2005–2017). ~18 retractions including 6 JAMA papers. Detected by Tim van der Zee, Jordan Anaya, Nick Brown after Wansink himself wrote a blog post praising a student for producing five papers from one dataset in six months — the trio reverse-engineered ~150 statistical inconsistencies from the published PDFs alone. Cornell found misconduct 2018; Wansink resigned 2019. Detection used only published tables, which is what peer review already had in hand. [https://www.buzzfeednews.com/article/stephaniemlee/brian-wansink-cornell-p-hacking] [https://retractionwatch.com/2018/09/19/jama-journals-retract-six-papers-by-food-marketing-researcher-brian-wansink/]

**Patterns across cases:**

- *Detection mechanisms recurring:* (1) lab-insider whistleblowers (Stapel, Macchiarini, Hwang); (2) forensic readers of *already-published* figures — duplicated panels, reused noise traces, impossible distributions (Schön, Obokata, Gino, Ariely); (3) statistical post-mortems on reported summary stats (Fujii/Carlisle, Wansink). None of these are peer review. All operate on the public record *after* the journal accepted.
- *Peer-review failure mode recurring:* reviewers assess reasoning, novelty, and whether the claimed methods would (if performed as described) support the conclusions. They do not and cannot audit whether the underlying data exist, were collected as described, or were copy-pasted from another experiment. That is the screening-vs.-perjury gap.
- *Institutional failure recurring:* home institutions (Karolinska, Harvard initially, Cornell initially, Bell Labs until forced) tend to protect the star before investigating; external pressure — journalists, bloggers, lawsuits, leaked documents — is what converts private suspicion into retraction.
- *Citation damage:* retractions do not halt citation. Shu/Ariely 2012 was cited hundreds of times and embedded in government nudge policy before retraction. Hauser, Stapel, Wakefield papers continued to be cited years after retraction (see H3).

**Strongest exhibits for the post:**

1. **Fujii (Carlisle's statistical forensics).** Rhetorically perfect: one outsider, armed with nothing but a chi-square and the published tables, did in weeks what hundreds of peer reviewers over 19 years could not. Literally "the defense brought in a forensic accountant."
2. **Ariely + Gino on the same 2012 paper.** Two *independent* fabrications in one five-author paper, both caught by Data Colada after a decade. The paper was real-world policy. Best single-case showcase for post-publication jury and downstream damage.
3. **STAP / Obokata.** Fastest and cleanest: PubPeer and a lab blog unwound two Nature papers in five months, and Nature publicly conceded peer review couldn't have caught it. The rare case of a journal explicitly admitting the screening/perjury distinction.

**Open questions:**

- Exact pre-retraction citation count for Shu et al. 2012 would sharpen the "policy damage" line — I have "hundreds" but did not pin a Google Scholar number.
- Wakefield (MMR/autism) is a different shape: journalist Brian Deer exposed it over years, plus epidemiological replication failures. Usable but less clean as "outside forensics" — deferred.
- Marc Hauser and Eric Poehlman fit the pattern but add little beyond the eight above; cut for space.

### H3: Citation-graph failures after retraction (opus, complete)

**Verdict:** Overwhelming evidence. Retracted and non-replicable papers keep accumulating citations, and the overwhelming majority of post-retraction citations fail to acknowledge the retraction — the citation graph does not update.

**Claims:**
- **Wakefield et al. 1998 (Lancet, MMR/autism):** partial retraction 2004, full retraction Feb 2010. Identified in a 2012 PNAS study as the most cited retracted paper with 758 citations at that point; a 2019 JAMA Network Open bibliographic analysis found 1,153 analyzable citing works. Of citing works published 2005–2010, only 38.2% acknowledged even the partial retraction; 2011–2018 acknowledgement rose to 71.7% — meaning ~28% of post-retraction citations still did not flag the retraction years later. [https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2755486] [https://retractionwatch.com/2019/11/18/andrew-wakefields-fraudulent-paper-on-vaccines-and-autism-has-been-cited-more-than-a-thousand-times-these-researchers-tried-to-figure-out-why/]
- **Shu/Mazar/Gino/Ariely 2012 (PNAS, "sign at top"):** retracted Sept 2021 after Data Colada exposed fabricated data. Had been cited 400+ times (Google Scholar) / 180 times (Web of Science) at retraction; deployed by insurance companies and governments. A 2020 preregistered replication (n=1,235) with the original authors found no effect — one year before retraction. [https://retractionwatch.com/2021/09/14/highly-criticized-paper-on-dishonesty-retracted/] [https://www.pnas.org/doi/10.1073/pnas.2115397118]
- **Hwang Woo-suk 2004 & 2005 (Science, stem cells):** both unconditionally retracted Jan 2006. Retracted papers were subsequently cited in a US cloning patent without any retraction note; broader pattern of continued citation documented. [https://retractionwatch.com/2014/02/16/fraud-retractions-no-barrier-to-us-cloning-patent-for-woo-suk-hwang/] [https://en.wikipedia.org/wiki/Hwang_affair]
- **Brian Wansink (Cornell food lab):** 18+ retractions (one paper retracted twice) plus 15 corrections by end of 2018; resigned Sept 2018 after Cornell found scientific misconduct. Total Google Scholar citations to his work: ~26,700. [https://en.wikipedia.org/wiki/Brian_Wansink] [https://retractionwatch.com/2018/09/19/jama-journals-retract-six-papers-by-food-marketing-researcher-brian-wansink/]
- **Scott Reuben (anesthesiology):** 21 fabricated studies, some with invented patients; pled guilty 2010. Papers averaged ~200 citations/year between 2002–2009; ~2,600 career citations. Nearly half his retracted papers were still being cited five years after retraction, and only ~25% of post-retraction citations noted the retraction. [https://www.scientificamerican.com/article/a-medical-madoff-anesthestesiologist-faked-data/] [https://pubmed.ncbi.nlm.nih.gov/30144024/]
- **Bohannon 2015 chocolate-weight-loss hoax:** deliberately bad study, retracted June 2015. Of 8 subsequent publications that cite it for a scientific claim, none acknowledged the retraction — all treated it as a legitimate peer-reviewed source, including a 2017 review claiming cocoa has anti-obesity effects in humans. [https://retractionwatch.com/2023/12/27/a-closer-look-at-the-chocolate-with-high-cocoa-content-hoax/]

**Systematic studies:**
- **Serra-Garcia & Gneezy 2021 (Science Advances):** non-replicable papers in top psychology/economics/general journals are cited *more* than replicable ones. The citation gap does not shrink after the failure-to-replicate is published, and **only 12% of post-replication-failure citations acknowledge the replication failure.** For Nature/Science specifically, the effect is extreme (reported as ~300× more citations for non-replicable — likely paper-level, verify before quoting). [https://www.science.org/doi/10.1126/sciadv.abd1705]
- **Hsiao & Schneider 2021 (Quantitative Science Studies, MIT Press):** across 7,813 retracted PubMed papers with 169,434 total citations, of 13,252 post-retraction citation *contexts*, only **722 (5.4%) acknowledged the retraction.** Case study of one retracted Nature paper: 2 of 57 post-retraction citations (3.5%) showed awareness. [https://direct.mit.edu/qss/article/2/4/1144/107356/Continued-use-of-retracted-papers-Temporal-trends]
- **Genetics field study (2020, Accountability in Research):** of 460 retracted genetics articles cited 34,487 times total, **7,945 (23%) of citations occurred post-retraction.** [https://www.tandfonline.com/doi/full/10.1080/08989621.2020.1835479]

**Strongest exhibit for the post:**
- Case: **Wakefield 1998** — retracted 2010, cited >1,000 times total, and as recently as 2011–2018 roughly 28% of citing works still failed to note the retraction. A fraudulent paper whose public-health cost is measured in measles outbreaks keeps appearing in reference lists as ordinary evidence.
- Aggregate: **5.4% (Hsiao & Schneider 2021)** — across ~170k citations to retracted biomedical papers, only 5.4% of post-retraction citation contexts acknowledge the retraction. Pair with **12% (Serra-Garcia & Gneezy 2021)** for the replication-failure analogue. The citation graph is structurally unaware of retraction and non-replication.

**Open questions:**
- Exact pre-vs-post by-year citation split for Ariely 2012 not located.
- Total citations to Hwang 2004/2005 Science papers pre- vs post-retraction: qualitative pattern clear, specific bibliometric study not found this pass.
- Serra-Garcia "300×" figure for Nature/Science non-replicable papers — may be extremum or per-paper; verify direction and magnitude before using in post.
- 2012 PNAS "758 citations" for Wakefield is a decade-old count; current Google Scholar total likely substantially higher.

### H5: The outside jury that already operates (opus, status: complete)

**Verdict:** Strong enough to close the post on. The outside jury is not hypothetical — it has a decade-plus track record, aggregate numbers in the tens of thousands, and has successfully withstood legal retaliation from the credentialed side.

**Claims:**

- **Data Colada** (Uri Simonsohn, Leif Nelson, Joe Simmons): blog founded 2013; forensic data analysis (spreadsheet metadata, Calibri-font anomalies, sort-order artifacts, Excel `calcChain` traces). Surfaced fraud in Dan Ariely's 2012 PNAS paper (retracted 2021) and four Francesca Gino papers. Harvard's own 1,288-page investigation concluded Gino "committed research misconduct intentionally, knowingly, or recklessly"; three additional retractions 2023; tenure revoked May 2025 — a Harvard tenure revocation that had "not occurred for decades." [https://datacolada.org/109] [https://www.science.org/content/article/honesty-researcher-committed-research-misconduct-according-newly-unsealed-harvard] [https://api.thecrimson.com/article/2025/5/27/gino-tenure-revoked/]

- **Elisabeth Bik:** image-duplication forensics starting with a 2016 screen of 20,621 papers (found 3.8% with problematic figures, ~half suggestive of deliberate manipulation). Career total to date: **951 retractions, 122 expressions of concern, 956 corrections** attributed to her reports; she has identified over 4,000 potential misconduct cases. Flagged 63 of Didier Raoult's papers on PubPeer; Raoult filed a criminal complaint (blackmail/harassment) April 2021 that went nowhere; >1,000 scientists signed a support letter. [https://en.wikipedia.org/wiki/Elisabeth_Bik] [https://www.science.org/content/article/scientists-rally-around-misconduct-consultant-facing-legal-threat-after-challenging]

- **PubPeer:** founded October 2012 by Brandon Stell + Richard and George Smith; anonymous-by-default commenting architecture. >35,000 comments by August 2015; ~300,000 pageviews/month by then. A 2021 study found >2/3 of comments report some form of misconduct (mostly image manipulation). The anonymity architecture is what lets junior researchers flag senior ones without career suicide. [https://en.wikipedia.org/wiki/PubPeer] [https://www.science.org/content/article/pubpeer-s-secret-out-founder-controversial-website-reveals-himself]

- **Retraction Watch** (Ivan Oransky + Adam Marcus, founded 2010): database acquired by Crossref in 2023 and made fully free. ~55,000 entries end of 2024; **61,645 retraction-related records as of March 2025**. Historical funding: MacArthur ($400K, 2015), Helmsley, Arnold Foundation. Retraction trend is a hockey stick: 140 retractions in 2000 → >11,000 in 2022 → >14,000 in 2023 (22% CAGR, far outpacing paper-growth CAGR). [https://en.wikipedia.org/wiki/Retraction_Watch] [http://retractiondatabase.org/]

- **Nick Brown & James Heathers** ("data thugs"): developed **GRIM** (2016) — checks whether reported means are arithmetically possible given sample size and integer responses — and **SPRITE** — reconstructs possible data sets from reported stats. Credited with dozens of corrections and ~10 full retractions (including 5 of Wansink's). Tools are public and runnable by anyone with a calculator. [https://www.science.org/content/article/meet-data-thugs-out-expose-shoddy-and-questionable-research]

- **Leonid Schneider (For Better Science) + "Smut Clyde":** pseudonymous blogger collaboration since 2017 exposing Chinese paper mills, papermilling rings in Germany, image-manipulation clusters in top immunology labs. Schneider has lost German libel suits — illustrates legal risk, not epistemic wrongness. [https://forbetterscience.com/]

- **OSF / Center for Open Science:** infrastructure side of the outside jury. **500,000+ registered users** (August 2022); 100,000+ registered studies; **300+ journals** now offer Registered Reports (peer review before results are known, removing the incentive to p-hack). [https://www.cos.io/about/news/open-science-framework-reaches-500000-registered-users-worldwide] [https://www.cos.io/initiatives/registered-reports]

**Scale:**
- Retractions per year: 140 (2000) → 11,000+ (2022) → 14,000+ (2023) → 9,000+ (2024). 61,645 records in the Retraction Watch DB as of March 2025.
- Bik alone: ~1,000 retractions, ~1,000 corrections, 4,000+ flagged cases.
- PubPeer: 35,000+ comments by 2015, still growing.
- Registered Reports adopted by 300+ journals.

**Institutional resistance:**
- **Gino v. Data Colada + Harvard** (2023): Gino sued the three bloggers and Harvard for defamation, seeking $25M. September 2024: judge dismissed the defamation claims against Data Colada on First Amendment grounds — fraud assertions are protected "subjective interpretation of the evidence." July 2025: judge declined to make Gino pay the bloggers' legal fees. August 2025: Harvard counter-sued Gino for defamation, alleging she submitted a backdated falsified dataset *to the misconduct investigation itself*. [https://www.science.org/content/article/honesty-researcher-s-lawsuit-against-data-sleuths-dismissed] [https://www.thecrimson.com/article/2025/9/12/harvard-sues-gino/]
- **Raoult v. Bik**: criminal complaint for blackmail/harassment April 2021; no action resulted, but the doxxing and harassment campaign were real.
- **Schneider**: multiple libel convictions in German courts.
- **Journal/institution response rates are low:** Bik's 700+ reports to editors → ~6% retraction rate on image duplication (vs. ~42% on plagiarism she'd seen previously). Clusters of duplications reported to ~10 institutions yielded only six retractions. Institutions systematically slow-walk.

**Strongest exhibit for the post:** **Data Colada + Gino**. Cleanest dramatic arc: three outside bloggers, using forensic spreadsheet analysis on files the subject herself had submitted, produced evidence strong enough that (a) Harvard's internal investigation concurred, (b) tenure was revoked for the first time in decades, (c) the subject's own defamation lawsuit was dismissed on First Amendment grounds, and (d) Harvard then sued *her* for submitting a falsified dataset to the investigation. Every part of the outside-jury thesis is there: evidence accessible to any careful reader, verdict institutions eventually ratified, legal retaliation that failed because the record was public.

**Open questions / weakest coverage:**
- **What the outside jury cannot do:** cannot compel document production, cannot subpoena raw data, cannot interview lab members under oath. Forensics works on what's already published. Fabricated data that never touches a public record is invisible.
- **Selection bias:** outside jury catches *detectable* fraud — image duplication, statistical impossibilities, sort-order metadata. Sophisticated fraud (wholly fabricated data from plausible distributions) is harder to detect.
- **Rate-limit:** Bik, Brown, Heathers, Schneider are a handful of individuals carrying enormous load. The system is not professionalized or well-funded. Retraction Watch only survived by being acquired by Crossref.
- **Response latency:** even when outside jury is right, institutions take 2–10 years to act. The Ariely/Shu 2012 PNAS paper was flagged years before its 2021 retraction.
- OSF adoption numbers are from 2022; firm 2024–2025 preregistration counts not located.

**Convergence with prior entries:** H1 already establishes that *detection* of marquee fraud came from outside channels (Fujii, Obokata, Gino, Ariely, Wansink, Stapel). H5 extends that: the detection wasn't one-off — it's an ongoing, institutionalized-outside-the-academy jury whose throughput is now measured in tens of thousands of retraction records per year and rising 22% CAGR. Same actors (Data Colada, Bik, Brown, Heathers) recur across both hypotheses, which is itself the finding: a small outside bench is doing a large share of the work peer review was expected to do.

### H6: Reflexive exhibit — positive-result rates in soc/econ (opus, complete)

**Verdict:** Strong enough to be load-bearing. The "~95% positive rate in socioeconomic fields" claim is supported by multiple independent samples across 60+ years (Sterling 1959 at 97%; Sterling/Rosenbaum/Weinkam 1995 at 93–99% across four psych journals; Fanelli 2010 at 88.5% economics/91.5% psychology; Scheel et al. 2021 at 96% standard psychology). The a priori argument — that this rate implies implausible statistical power or perfect prior intuition — is articulated most crisply by Sterling et al. 1995 and formalized in the Ioannidis/Gelman/Simonsohn tradition. The exact field-level number drifts between 88% and 97% depending on journal, decade, and how "positive" is coded, but the ≥90% band is robust and the inference is the same.

**Claims:**

- **Sterling 1959 (JASA):** 294 articles across four major psychology journals (*JASA*, *JAP*, *JCPP*, *JXP*) from 1955–1956 using significance tests. **286 of 294 (97.3%)** rejected the null hypothesis at conventional α. Sterling's original observation: "a tendency on the part of investigators and editors to publish experiments that yielded 'significant' results." The paper identified the screening problem at the start of postwar experimental psychology and was essentially ignored for 30 years. [https://gwern.net/doc/statistics/bias/publication/1959-sterling.pdf]

- **Sterling, Rosenbaum & Weinkam 1995 (*The American Statistician*):** 30-year follow-up. Examined four psychology journals for years 1986–1987 vs. 1958. Rejection rates essentially unchanged. By journal (1987 / 1958): *Journal of Experimental Psychology* 93% / 99%; *Comparative & Physiological Psychology* 97% / 97%; *Consulting & Clinical Psychology* 98% / 95%; *Personality and Social Psychology* 96% / 97%. Authors' inferential argument: if published rejection rate ≈ average statistical power (under the generous assumption that every tested null is false), 95%+ rates demand ≥95% average power — a standard nobody claims psychology achieves. The gap between claimed and plausible power is the publication-bias signal. [https://www.tandfonline.com/doi/abs/10.1080/00031305.1995.10476125]

- **Fanelli 2010 (PLOS ONE), "'Positive' results increase down the Hierarchy of the Sciences":** N = 2,434 papers stratified random-sampled from Essential Science Indicators across 20 disciplines; coded by whether authors "concluded to have found a 'positive' (full or partial) or 'negative' (no or null) support for the tested hypothesis." Only the first hypothesis per paper counted. Full rank order (lowest→highest positive rate): Space Science 70.2% · Geosciences 75.3% · Physics 78.5% · Chemistry 80.1% · Plant/Animal Sciences 80.3% · Environment/Ecology 81.0% · Materials Science 82.1% · Biology & Biochemistry 83.0% · Engineering 83.2% · Computer Science 83.9% · Microbiology 84.1% · Agricultural Sciences 84.4% · Molecular Biology & Genetics 85.0% · Neuroscience & Behaviour 85.2% · Pharmacology & Toxicology 85.5% · Immunology 85.9% · Clinical Medicine 86.1% · **Sociology 87.3%** · **Economics & Business 88.5%** · **Psychology & Psychiatry 91.5%**. Odds of a positive result in Psychology/Psychiatry and Economics/Business were ~5× those in Space Science after controlling for pure-vs-applied and number of hypotheses. [https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0010068] [https://pmc.ncbi.nlm.nih.gov/articles/PMC2850928/]

- **Fanelli 2012 (Scientometrics), "Negative results are disappearing":** Longitudinal sample of ~4,600 papers, 1990–2007, across all disciplines. Frequency of "positive" conclusions grew by **>22%** over the period, with social/behavioral fields leading the trend. Establishes that the bias is getting worse, not self-correcting. [https://link.springer.com/article/10.1007/s11192-011-0494-7]

- **Scheel, Schijen & Lakens 2021 (AMPPS), "An Excess of Positive Results":** Compared 71 published psychology Registered Reports (as of Nov 2018) against a random sample of 152 standard hypothesis-testing psychology articles. Coded the first hypothesis of each paper as positive/null. Standard literature: **146 of 152 (96%)** positive. Registered Reports: **31 of 71 (44%)** positive. The ~52-point gap is the direct quantification of what the chain-of-custody intervention catches. Already cited in H4; confirmed here with exact numerator/denominator. [https://journals.sagepub.com/doi/10.1177/25152459211007467]

- **Brodeur et al. 2016 (AEJ: Applied), "Star Wars: The Empirics Strike Back":** Analyzed ~50,000 test statistics from *AER*, *JPE*, *QJE*. Distribution of reported z-statistics shows a "two-humped camel" — a missing mass in the 1.2–1.6 z range and a bulge just above 1.96. **10–20% of marginally significant tests are "misallocated" p-values** consistent with p-hacking/selection toward significance in top economics journals. Not a headline positive-rate number but direct empirical evidence that the apparent rate is partly manufactured. [https://www.aeaweb.org/articles?id=10.1257/app.20150044]

- **Brodeur, Cook & Heyes 2020 (AER), "Methods Matter":** Same methodology extended to 21,000+ tests stratified by causal-inference method (IV, DiD, RCT, RDD). **Inflation of just-significant results is worst for IV and DiD, milder for RCT and RDD.** Concentrates the p-hacking finding on the specific methods that drive modern applied microeconomics. [https://www.aeaweb.org/articles?id=10.1257/aer.20190687]

- **Ioannidis, Stanley & Doucouliagos 2017 (*Economic Journal*), "The Power of Bias in Economics Research":** Meta-meta-analysis of 6,700 empirical-economics estimates across 159 research areas. **Median statistical power ≈ 18%;** nearly 80% of reported effects are underpowered. Given that power, the observed ~90% positive rate in published economics is mathematically impossible under honest reporting — a result at the stated power should turn up positive less than one time in five. Effect magnitudes are typically inflated by **~100%**, with a third inflated **4× or more**. [https://onlinelibrary.wiley.com/doi/10.1111/ecoj.12461]

- **Stanley, Jarrell & Doucouliagos 2010:** Publication selection in economics is severe enough that "we are likely to be better off discarding 90% of the research results than to take them at face value." Quoted in the MAER-Net meta-regression literature. [https://www.sea-stat.com/wp-content/uploads/2021/11/Meta-Regression-Analysis-in-Economics-and-Business-by-T.D.-Stanley-Hristos-Doucouliagos-.pdf]

**The a priori argument — why ~95% is pathology:**

The cleanest version is Sterling et al. 1995's observation: *under honest testing, the rate at which published studies reject the null cannot exceed the average statistical power of the field.* Power is the probability a true effect will clear the significance threshold. If every hypothesis tested is true and power is 80%, you should see ~80% positive. If half the hypotheses tested are true and power is 80%, you should see ~40% positive plus a few percent false positives — call it 45%. To get to 95% published positives, a field needs either (a) near-100% power (ruled out by Ioannidis/Stanley/Doucouliagos 2017 putting median economics power at 18%), or (b) near-perfect prior intuition so almost every tested hypothesis is true (equivalent to claiming researchers know the answer before running the study — which makes the study ceremonial, not epistemic), or (c) selective reporting. The Bayesian extension (Ioannidis 2005, "Why Most Published Research Findings Are False") formalizes this: positive predictive value of a published finding is a function of power, prior, α, and bias; at plausible socioeconomic values, PPV can fall below 50%. Gelman's "garden of forking paths" (2013) and Simmons/Nelson/Simonsohn "False-Positive Psychology" (2011) describe the *mechanism* (researcher degrees of freedom) by which honest-feeling analysis produces the pathological rate. Scheel et al. 2021 is the cleanest empirical test: remove the forking paths (pre-registered analysis plan, peer review before results) and the rate collapses from 96% to 44% in the same field.

**Convergence with H2 and H4:**

- **With H2 (replication):** If 96% of published psychology findings report significant effects but only 36% replicate at p<.05 (OSC 2015), the gap is 60 points — precisely what selection and flexibility would predict. The two numbers are independent measurements of the same distortion: one at the publication gate, one at the replication gate.
- **With H4 (pre-registration):** H4's Kaplan & Irvin (57% → 8% when prospective registration became mandatory for NHLBI cardiovascular trials) and FDAAA (98% → 93% published positive, plus reviewer-published gap closing from 22 points to 2) show the same collapse in biomedicine that Scheel et al. show in psychology. Three independent chain-of-custody interventions, three collapses. The consistency is itself evidence that the 95% baseline was not measuring nature.
- **Combined story:** H2 and H4 measure the size of the leak; H6 shows the leak has been visible in plain statistics since 1959. It took 50+ years and replication/pre-registration infrastructure to turn "obvious in hindsight" into institutional response.

**Strongest single exhibit:**

**Scheel, Schijen & Lakens 2021: 96% vs 44%, same field, same type of hypothesis test, the only thing that changed is whether analysis was pre-specified.** This is the reflexive exhibit — a controlled comparison within psychology showing the honest-methodology rate is roughly half the published rate. Pair with Sterling 1959's 97% as the "we have known this since Eisenhower" anchor: the pattern was named the year Fidel Castro took Havana, and the published rate has not moved since.

**Open questions / precision notes:**

- *Is "95% in socioeconomic fields" precisely right?* The honest range is **88–97% depending on sample**. Fanelli 2010 gives 88.5% (economics/business) and 91.5% (psychology/psychiatry) across broad ESI samples. Sterling 1959/1995 get 93–99% across specific high-status psychology journals. Scheel et al. 2021 get 96% for standard psychology. For the post, "well above 90%" is safer than "95%"; "roughly 90% in economics, 95%+ in top psychology journals" is the most accurate short form.
- *Fanelli's "positive" is author-reported,* not reanalyzed p-values. A paper where the author claims "partial support" from mixed results is coded positive. This probably *under*states the rate for strict null-rejection reads and overstates it for strict full-support reads. Sterling's coding (H0 rejected at α) is the stricter one and gives the higher numbers.
- *Economics has no single "Sterling for econ" paper* giving one headline rate. The econ evidence is indirect: Brodeur's p-curve anomalies plus Ioannidis/Stanley/Doucouliagos's power-vs-published mismatch. Fanelli 2010's 88.5% is the best single number for economics/business.
- *The "perfect prior intuition" framing is the user's;* nobody in the literature phrases it that literally. Closest articulations: Sterling et al. 1995 (power argument), Ioannidis 2005 (PPV model), Gelman 2014 ("piranha problem" — a field cannot have as many large, robust effects as it claims). Safe to present the framing as the author's synthesis.

### Substantiation mop-up (opus, complete)

**1. Stapel retraction count + detection mechanism.**
- **Claim (draft):** "Diederik Stapel: 58 retractions in social psychology, detected by students who finally compared notes."
- **Verified:** 58 retractions confirmed by Retraction Watch as of Dec 2015, the last count on file: "Diederik Stapel now has 58 retractions" (<https://retractionwatch.com/2015/12/08/diederik-stapel-now-has-58-retractions/>). Detection: three junior researchers under Stapel's supervision found irregularities in published data in late August 2011 and notified Marcel Zeelenberg, head of social psychology at Tilburg; Stapel was suspended in early September 2011. The Levelt committee's Flawed Science report (<https://www.tilburguniversity.edu/sites/default/files/download/Final%20report%20Flawed%20Science_2.pdf>) documents this. Scientific American: <https://www.scientificamerican.com/article/massive-fraud-uncovered-in-work/>. Stapel was himself the *dean* of the Tilburg School of Social and Behavioral Sciences; the junior researchers went above him in the chain, not to him.
- **Correction needed:** Minor. "Students who finally compared notes" is romanticized — the actual mechanism was three junior researchers under his direct supervision spotting duplicated score rows and unrealistic effects in his data, then escalating to the department head. Suggested rewrite: "Diederik Stapel: 58 retractions in social psychology, detected by three junior researchers in his own lab who escalated to the department head." Or keep the students framing but drop "finally compared notes" (which overstates the collective-epiphany character).
- **Confidence:** High.

**2. STAP / Nature editors' concession.**
- **Claim (draft):** *Nature*'s editors conceded that peer review "could not have been expected to detect" the fabrication.
- **Verified:** The actual phrasing, from Nature's July 2014 editorial "STAP retracted" (<https://www.nature.com/articles/511005b>), is: **"We have concluded that we and the referees could not have detected the problems that fatally undermined the papers. The referees' rigorous reports quite rightly took on trust what was presented in the papers."** Retraction Watch's contemporaneous headline: "STAP stem cell papers officially retracted as Nature argues peer review couldn't have detected fatal problems" (<https://retractionwatch.com/2014/07/02/stap-stem-cell-papers-officially-retracted-as-nature-argues-peer-review-couldnt-have-detected-fatal-problems/>).
- **Correction needed:** The draft's paraphrase ("could not have been expected to detect") is close but not a direct quote. Tighten to: *Nature*'s editors conceded that "we and the referees could not have detected the problems." Keeping quotes around the exact eight words gives the paragraph its teeth without risking a pull-quote mismatch.
- **Confidence:** High.

**3. Fujii detection — Carlisle, chi-square, count.**
- **Claim (draft):** "The detection was a chi-square test on his published summary statistics, run by a single statistician."
- **Verified:** John Carlisle, a UK anaesthetist (not statistician by training, though doing statistical forensics), published "The analysis of 168 randomised controlled trials to test data integrity" in *Anaesthesia* in March 2012 (<https://pubmed.ncbi.nlm.nih.gov/22404311/>). Method: compared distributions of baseline continuous and categorical variables against expected distributions; 28 of 33 variables were inconsistent, with likelihoods ranging from 1 in 25 to <1 in 10^33. Final retraction tally on Fujii: **183 retractions**, currently the single-author world record (per Retraction Watch Leaderboard and Wikipedia). The 2012 interim report found data falsification in **172 of 212** papers (<https://retractionwatch.com/2012/07/02/does-anesthesiology-have-a-problem-final-version-of-report-suggests-fujii-will-take-retraction-record-with-172/>). 183 is the lifetime count; 172 is the 2012 interim figure.
- **Correction needed:** "Chi-square test" is slightly imprecise — Carlisle tested whether reported baseline distributions were consistent with expected distributions under randomization; it's a distributional/goodness-of-fit family of tests, with chi-square components. "A single statistician" is also imprecise — Carlisle is an anaesthetist. Suggested rewrite: "The detection was a distributional test on his published baseline statistics, run by a single anaesthetist (John Carlisle) working alone." Current "183" number is correct for present-day lifetime total.
- **Confidence:** High.

**4. "First such tenure revocation in decades" (Gino).**
- **Claim (evidence log):** Harvard revoked Gino's tenure May 2025, "first in decades."
- **Verified:** Confirmed. Multiple outlets say no Harvard professor has lost tenure since the 1940s — so roughly 80 years, not merely "decades." The Hill's headline: "Harvard revokes Francesca Gino's tenure, a first in decades" (<https://thehill.com/homenews/education/5320925-harvard-revokes-professors-tenure/>). WGBH: "In extremely rare move, Harvard revokes tenure and cuts ties with star business professor" (<https://www.wgbh.org/news/education-news/2025-05-25/in-extremely-rare-move-harvard-revokes-tenure-and-cuts-ties-with-star-business-professor>). Boston Globe and NBC News note the 1940s precedent; specific prior case is not named in these sources (the search did not surface an individual named precedent — the claim is "none since the 1940s," not "X was the last one"). The claim is about Harvard specifically, not all US research universities.
- **Correction needed:** The post's "first such revocation in decades" is defensible but timid — the sourced claim is stronger: **first at Harvard since the 1940s, i.e., ~80 years**. Consider: "Harvard revoked Gino's tenure in May 2025, the first such revocation at Harvard since the 1940s." If you want to stay cautious (in case a fact-checker finds a 1960s case not widely reported), "the first in roughly eighty years" matches the sourced framing without naming a specific prior case.
- **Confidence:** High on "decades / ~80 years since 1940s"; medium on whether a specific named precedent from the 1940s is documented (sources assert the 1940s cutoff without naming a person).

**5. *Act of Killing* characterization.**
- **Claim (draft):** "perpetrators of the Indonesian mass killings cheerfully reenact their murders for the camera."
- **Verified:** Joshua Oppenheimer, 2012. Anwar Congo and associates, former death-squad members from the 1965–66 anti-communist killings in Indonesia, are invited by the filmmakers to reenact their murders in the style of their favorite Hollywood genres — gangster films, westerns, musicals (<https://en.wikipedia.org/wiki/The_Act_of_Killing>, <https://www.npr.org/2013/07/26/198439933/in-indonesia-a-genocide-restaged-for-the-camera>). PBS NewsHour headline: "In Oscar-nominated 'The Act of Killing,' mass murderers boastfully reenact their war crimes." "Cheerfully" matches the early-film register — Congo demonstrates his garrote-wire method on a rooftop smiling, participants laugh and joke throughout the gangster reenactments. The film's arc is that Congo's cheer breaks down late in the film (he retches on the rooftop where he killed); the *early* reenactments are the cheerful ones, which is what the draft's sentence invokes.
- **Correction needed:** None. "Cheerfully" is accurate for the scenes the analogy evokes. Optional: "boastfully" (per PBS) is slightly stronger and more defensible against a reader who would object that Congo clearly suffers by the end of the film — but "cheerfully" fits the rhetorical move the paragraph makes (evil invisible from inside the culture that celebrates it). Keep as written.
- **Confidence:** High.

### Substantiation: causal-impact claims (opus, complete)

Adversarial fact-check of each specific causal-impact claim in the draft. "Confidence" rates how publishable-as-is the sentence is after this pass.

---

**1. Hormone Replacement Therapy / WHI**

- **Claim (draft):** "Hormone replacement therapy was prescribed to tens of millions of women based on observational signals; the pre-registered Women's Health Initiative RCT (2002) found it raised breast cancer and stroke risk, and prescriptions collapsed by about 40% the next year."
- **Verified:**
  - WHI estrogen+progestin arm published in *JAMA* July 17, 2002 (Writing Group, Rossouw et al.). Trial stopped early May 31, 2002 because invasive breast cancer crossed the pre-specified stopping boundary. Per-10,000-person-year excess: +8 invasive breast cancers, +8 strokes, +7 CHD events, +8 pulmonary embolisms. [https://pubmed.ncbi.nlm.nih.gov/12117397/]
  - Was it "pre-registered"? The WHI had a **published protocol** (Hays et al., 1998, *Controlled Clinical Trials*) with pre-specified primary outcomes (CHD as primary benefit, invasive breast cancer as primary harm) and a formal DSMB stopping rule. ClinicalTrials.gov launched Feb 2000; WHI's NCT record is essentially retrospective. "Pre-registered" is colloquially defensible; the stronger technical form is "protocol-published with DSMB-enforced stopping rules."
  - Prescriptions: Hersh et al. 2004 (*JAMA*): U.S. prescriptions for combination HRT (Prempro) fell **~66% from Jan–Jun 2002 to Jan–Jun 2003**; Premarin fell ~33%. Total menopausal-hormone visits fell from 26.5M (2001) to 16.9M (2003), roughly **38%**. NHANES: MHT use among women ≥40 fell from 22.4% (1999–2002) to 11.9% (2003–04), ~47% relative drop. [https://pubmed.ncbi.nlm.nih.gov/14709575/] [https://pubmed.ncbi.nlm.nih.gov/16816053/]
  - "Tens of millions" over the multi-decade prescribing era is defensible. At the time of WHI, ~5–6M U.S. women were on combined HRT; broader menopausal-hormone use was considerably higher; cumulative users across the 1980s–1990s run into tens of millions.
- **Correction needed:** "About 40%" is in the right neighborhood for total visits (~38%) and understates combination-HRT drop (~66%) and overall use (~47%). Safer phrasing: **"prescriptions for combination HRT fell by roughly two-thirds within a year."** Consider softening "pre-registered" to "protocol-published with pre-specified stopping rules." "Breast cancer and stroke" is correct but incomplete (CHD and PE also).
- **Confidence:** High on direction and order of magnitude. Medium on the exact "~40%" figure — recommend replacement.

---

**2. Ariely / Shu 2012 adoption by IRS and insurers**

- **Claim (draft):** "Ariely, Mazar, and Amir's 2012 paper on signing honesty pledges at the top of a form was adopted by insurers and the IRS before the underlying data was shown to be fabricated."
- **Verified:**
  - Authorship: the 2012 PNAS paper is **Shu, Mazar, Gino, Ariely, and Bazerman** — not "Ariely, Mazar, and Amir." Amir is not an author. [https://www.pnas.org/doi/10.1073/pnas.1209746109]
  - Insurers: Experiment 3 of the paper was run with The Hartford auto-insurance company — this is the specific experiment Data Colada (post [98], Aug 2021) showed was fabricated: The Hartford supplied ~13,488 policies but the miles-driven distribution was forged. I found no independent evidence that other insurers operationally adopted sign-at-top on the basis of the paper.
  - IRS: the **IRS Behavioral Insights Toolkit (2017)** cites Shu et al. 2012 as evidence for signature-placement nudges, as does the Taxpayer Advocate Service literature review. The authors publicly stated they would share findings with the IRS. I did *not* find evidence that the IRS actually restructured Form 1040 to place the signature at the top. The operational-adoption trail is weaker than the phrase "adopted by the IRS" implies. [https://www.irs.gov/pub/irs-soi/17rpirsbehavioralinsights.pdf] [https://datacolada.org/98]
  - Fabrication exposed: Data Colada post [98], Aug 17 2021; PNAS retraction Sept 2021.
- **Correction needed:** **Mandatory:** fix authorship to "Shu, Mazar, Gino, Ariely, and Bazerman" (or "Shu et al."). Narrow operational-adoption language: recommend **"was cited as evidence in the IRS's Behavioral Insights Toolkit and embedded in government nudge-unit literature; its headline insurance-company field experiment turned out to be fabricated."**
- **Confidence:** Medium. Authorship fix is non-negotiable.

---

**3. Ego depletion in teacher-training curricula and self-help programs**

- **Claim (draft):** "Ego depletion — the claim that willpower is a finite resource — entered teacher-training curricula and self-help programs before the effect failed to replicate across labs."
- **Verified:**
  - Replication failure: Hagger et al. 2016 (*Perspectives on Psychological Science*), 23 labs, ~2,000 participants, d = 0.04. Solid. [https://journals.sagepub.com/doi/10.1177/1745691616652873]
  - Self-help: Baumeister & Tierney, *Willpower: Rediscovering the Greatest Human Strength* (Penguin, 2011) is a mass-market self-help book built explicitly on ego-depletion theory. Defensible. [https://www.amazon.com/Willpower-Rediscovering-Greatest-Human-Strength/dp/0143122231]
  - Teacher training: **I could not find concrete evidence that ego depletion specifically was adopted into teacher-training curricula as a named construct.** Self-regulation/self-control ideas broadly (Mischel's marshmallow test, Duckworth's grit, Dweck's growth mindset) are widely taught; ego depletion as such is not clearly traceable into curricula.
- **Correction needed:** **Drop "teacher-training curricula"** unless a specific citation can be produced. Recommended replacement: **"Ego depletion — the claim that willpower is a finite resource — anchored a bestselling self-help book (Baumeister and Tierney's *Willpower*, 2011) and hundreds of derivative popular articles before a 23-lab registered replication came back null."** Preserves the rhetorical beat.
- **Confidence:** Low on draft as written. High on the replacement.

---

**4. Power posing — TED views, bestseller, author withdrawal**

- **Claim (draft):** "Power posing generated 70+ million TED-talk views and a bestselling book before its lead author publicly withdrew support for the core claim."
- **Verified:**
  - TED views: Amy Cuddy's TED Global 2012 talk "Your body language may shape who you are" — publicly reported at **over 71 million** across TED.com and YouTube. [https://www.ted.com/speakers/amy_cuddy]
  - Bestseller: Cuddy's *Presence: Bringing Your Boldest Self to Your Biggest Challenges* (Little, Brown, 2015) — **NYT, WSJ, Washington Post, USA Today bestseller**, 35 languages, >500k copies. [https://www.amycuddy.com/books]
  - Withdrawal — **this is the attribution error in the draft.** Dana Carney was **first author** of the original 2010 *Psychological Science* paper (Carney, Cuddy, Yap). In Sept 2016, Carney posted "My position on 'Power Poses'" at Berkeley: *"I do not believe that 'power pose' effects are real... I do not teach power poses in my classes anymore... I discourage others from studying power poses."* **Cuddy did not withdraw.** She continued to defend a narrowed version of the claim (subjective feelings of power) and the TED framing. [https://faculty.haas.berkeley.edu/dana_carney/pdf_my%20position%20on%20power%20poses.pdf] [https://retractionwatch.com/2016/09/26/]
- **Correction needed:** **Mandatory precision fix.** "Its lead author publicly withdrew" reads as if Cuddy withdrew — she did not. Rewrite to name Carney and ideally quote her: **"...before its first author, Dana Carney, publicly withdrew support in 2016: 'I do not believe that "power pose" effects are real.'"** Cuddy is the face of the talk and book; Carney ran the original experiment and walked away. Naming the split *strengthens* the rhetorical point.
- **Confidence:** High on 70M+ TED views and bestseller. High on Carney's withdrawal statement and date. Mandatory fix on "lead author" phrasing.

---

**5. Fujii anesthesia practice impact**

- **Claim (draft):** "Fujii's fake trials shaped anesthesia practice for two decades."
- **Verified:**
  - Scale: 183 retractions, 1993–2011. 110 of 122 PONV RCTs fabricated per the Japanese Society of Anesthesiologists investigation. [H1 sources.]
  - Loadsman & McCulloch 2013 (*Anesthesia & Analgesia*): Fujii's fabricated data *was* absorbed into multiple PONV (postoperative nausea and vomiting) meta-analyses, particularly concerning ondansetron, granisetron, ramosetron, and droperidol. Sensitivity analyses after retractions shifted some point estimates (e.g., ramosetron's apparent edge weakened). [https://journals.lww.com/anesthesia-analgesia/fulltext/2013/03000/scientific_fraud__impact_of_fujii_s_data_on_our.4.aspx]
  - **But:** major consensus guidelines — SAMBA PONV guidelines, French and German expert recommendations — did not materially depend on Fujii's studies. Frontline clinical practice was not fundamentally rewritten by his fraud.
  - Broader downstream: BJA 2023 narrative review — "only 5% of systematic reviews or clinical guidelines correct or retract results that used retracted data." So contamination in the literature persists even where frontline guidelines escaped it.
- **Correction needed:** "Shaped anesthesia practice for two decades" is stronger than the evidence supports. Recommended replacement: **"Fujii's 183 fabricated papers contaminated two decades of anesthesia meta-analyses; the forensic takedown came from a single outsider, John Carlisle, running a chi-square test on published summary statistics in 2012."** Preserves the outside-forensics-beat-peer-review rhetorical move.
- **Confidence:** Medium on draft as written. High on narrowed "contaminated meta-analyses" replacement.

---

**6. Macchiarini — journal, patient count, detection mechanism**

- **Claim (draft):** "Paolo Macchiarini's synthetic trachea transplants — published in *The Lancet* and celebrated on television — killed seven of the nine patients who received them before Swedish journalists forced the story open."
- **Verified:**
  - Journal: *The Lancet* published Macchiarini's 2008 tissue-engineered trachea paper and the 2011 synthetic-scaffold paper (Jungebluth et al.). NEJM rejected at least two Macchiarini submissions. "Published in *The Lancet*" is correct for the headline cases. [https://en.wikipedia.org/wiki/Paolo_Macchiarini]
  - Patient count: the synthetic-trachea series was **eight patients, of whom seven died** (one survivor as of mid-2010s). The draft's "seven of the nine" is off by one — should be **"seven of the eight."** [https://www.science.org/content/article/transplant-surgeon-gets-prison-sentence-failed-stem-cell-treatments]
  - Detection: a *shared* story. Four Karolinska clinical colleagues (Grinnemo, Corbascio, Simonson, Fux) filed detailed misconduct complaints in August 2014. External reviewer Bengt Gerdin found misconduct May 2015. Karolinska initially sided with Macchiarini and even reported whistleblowers to police. **SVT's three-part documentary *Experimenten* (Bosse Lindquist) aired January 13, 2016** and forced the reopening. So "Swedish journalists forced the story open" compresses a two-stage story: whistleblowers first (and punished for it), journalists second (and decisive for reversal). [https://news.ki.se/news-archive/the-macchiarini-case-timeline]
- **Correction needed:** **Mandatory:** "seven of the nine" → **"seven of the eight."** Optional expansion on detection: "...before Karolinska whistleblowers, at first dismissed, were vindicated by Swedish public television's *Experimenten* in January 2016." Short form as drafted is defensible for pacing.
- **Confidence:** High on *Lancet*. High on "seven of eight." Medium-high on short detection phrasing.

---

**7. Wakefield / MMR vaccination rates, measles, herd immunity**

- **Claim (draft):** "Wakefield's 1998 MMR paper drove vaccination rates below herd-immunity thresholds in parts of the UK and US; measles cases have followed the citation count, not the retraction."
- **Verified:**
  - Herd-immunity threshold for measles: **~95% two-dose coverage** (WHO). [https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(22)00169-4/fulltext]
  - UK first-dose MMR at 24 months: **~92% in 1995–96 → 79.9% in 2003–04** nadir, recovering past 90% only by ~2011. London and inner-city areas went considerably lower. Well below 95% threshold. [https://www.ncbi.nlm.nih.gov/books/NBK545996/] [https://researchbriefings.files.parliament.uk/documents/CBP-8556/CBP-8556.pdf]
  - U.S.: national MMR coverage stayed relatively high (~91–94% at age 2). But **specific communities** dropped below herd-immunity threshold and drove outbreaks: Somali-American community in Minneapolis (Wakefield visited 2010–2011; coverage fell to ~36% by 2014, driving the 2017 Minnesota outbreak); Orthodox Jewish communities in Brooklyn/Rockland (2018–19 outbreak, pocket coverage <80%); Clark County, Washington (2019). "Parts of the US" is defensible via these named clusters.
  - Measles: UK had WHO elimination status in 2017, lost it 2019; 2023–24 saw England's largest outbreak in 30 years. U.S. lost its 2000 elimination status repeatedly. Consistent hockey-stick pattern tied to undervaccinated pockets.
  - "Followed the citation count" is rhetorical flourish, not a measured correlation — fine as rhetoric, not as a data claim.
- **Correction needed:** Claim stands. Optional tightening: "drove UK first-dose uptake from 92% to 80% by 2003, and pushed communities in Minneapolis, Brooklyn, and Clark County below the 95% measles threshold."
- **Confidence:** High on UK numbers, herd-immunity threshold, and named U.S. outbreak clusters. Rhetorical closing phrase is fine as written.

---

**Summary of required fixes (prioritized):**

1. **Power posing attribution — MANDATORY.** "Lead author publicly withdrew" misattributes to Cuddy. The withdrawer was Dana Carney, first author of the original 2010 paper; Cuddy did not withdraw. Name Carney, quote Sept 2016 statement.
2. **Ariely authorship — MANDATORY.** "Ariely, Mazar, and Amir" → "Shu, Mazar, Gino, Ariely, and Bazerman" (or "Shu et al."). Amir isn't an author.
3. **Macchiarini arithmetic — MANDATORY.** "Seven of the nine" → "seven of the eight."
4. **HRT percentage — recommended.** "About 40%" understates combination HRT and overall use; "roughly two-thirds" for combination HRT is cleaner. Also consider "protocol-published with pre-specified stopping rules" over "pre-registered."
5. **Ariely operational adoption — recommended.** "Adopted by insurers and the IRS" overclaims; narrow to "cited as evidence in the IRS's Behavioral Insights Toolkit and governmental nudge-unit literature."
6. **Ego depletion — recommended.** Drop "teacher-training curricula" (unsupported); replace with the Baumeister/Tierney *Willpower* book (2011).
7. **Fujii — recommended.** "Shaped anesthesia practice" → "contaminated two decades of anesthesia meta-analyses."
8. **Wakefield — optional.** Stands as written; could sharpen with 92% → 80% UK figure and named U.S. outbreak locations.


