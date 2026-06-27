---
variant: post-medium
title: "Science on Trial"
tags: reflecting, epistemology
---

When you ask scientists about their work, they cite their positive results. When you ask the public what makes science credible, they cite peer review. When you ask ChatGPT for its sources, it points to publications as if publication were truth. If that all sounds fine, your notion of science is broken.

Science is supposed to be the act of changing beliefs in response to evidence. Every claim stands trial forever. Science is also, now, a noun. A body of credentialed outputs. An institution. The institution was built to support the activity, and has become more rewarding to maintain than the activity itself.

Do you "trust the science"?

### The Scientific Process

Four centuries of arguing about what counts as knowledge produced a [protocol](/reading/scientific-method). Each step exists because someone proved it was necessary.

- *Pre-register.* Write your hypothesis and your analysis plan before you see the data. ([Popper](/reading/scientific-method/popper-1934/), [Mayo](/reading/scientific-method/mayo-2018/).)
- *Red-team to convergence.* Generate alternative hypotheses. Design experiments that discriminate. Keep going until you can't. ([Chamberlin](/reading/scientific-method/chamberlin-1890/), [Platt](/reading/scientific-method/platt-1964/).)
- *Work log frequently.* Record observations as they happen, version your drafts, tag your confidence. ([Bacon](/reading/scientific-method/bacon-1620/), [Gwern](/reading/scientific-method/integrity/).)
- *Publish all.* Positives, nulls, embarrassing stuff, code. A curated trail can be [Goodharted](https://en.wikipedia.org/wiki/Goodhart%27s_law); a complete one can't. ([Feynman](/reading/scientific-method/feynman-1974/), [Gwern](/reading/scientific-method/self-experiment/).)

Each step produces a public artifact: a registered prediction, an alternatives list, a timestamped log, a complete dataset. The trail is what counts as knowledge.

### The Scientific "Process"

Routinely conflated. The exhibits below turn on keeping them apart.

- *Publication.* A claim entered the record. The paper exists, the DOI resolves, the journal formatted it.
- *Peer review.* Two or three people saw no fatal flaw before entry. A grand jury indictment.
- *Replication.* The claim survived contact with fresh data, by hands unrelated to the original. Most published findings never reach this step.
- *Truth.* What remains when the record stops updating.

The institution trains the reader to recognize publication as truth. Is it?

Now the exhibits.

#### Exhibit A. Missing Pre-registration

[ClinicalTrials.gov](https://clinicaltrials.gov/) came online in 2000, and prospective registration entered the norm for NHLBI-funded cardiovascular trials around the same time. [Kaplan and Irvin (2015)](https://pubmed.ncbi.nlm.nih.gov/26244868/) compared 55 large NHLBI trials before and after. Pre-2000: *17 of 30 (57%)* reported positive primary outcomes. Post-2000: *2 of 25 (8%)*. Same question, same funder, chain of custody added.

Of the 25 post-2000 trials, 12 still reported significant *secondary* outcomes. Without the mandate, 48% would have told a positive story anyway.

[Scheel, Schijen, and Lakens (2021)](https://journals.sagepub.com/doi/10.1177/25152459211007467) found the same pathology in psychology reports against [Registered Reports](https://www.cos.io/initiatives/registered-reports) in the same field. Standard papers: *96% positive*. Registered Reports: *44%*. The baseline has been this high since Sterling reported 97% in 1959.

In that slice of high-stakes cardiovascular RCTs, the apparent success rate collapsed as soon as outcome declaration became visible. Those findings shaped treatment decisions for millions. Hormone replacement therapy (HRT) was prescribed to tens of millions of women on the strength of observational signals. The [Women's Health Initiative RCT (2002)](https://pubmed.ncbi.nlm.nih.gov/12117397/) was stopped early when its data safety monitoring board found combination HRT raised breast cancer and stroke risk. [Prescriptions for combination HRT fell roughly two-thirds within a year](https://pubmed.ncbi.nlm.nih.gov/14709575/).

#### Exhibit B. No Adversary

Under honest methodology, the published positive-result rate is capped by arithmetic. At α = 0.05 and 80% statistical power:

| If the tested hypotheses are... | Expectation | Reported (Scheel 2021, psychology) |
|---|---|---|
| 20% true | 20% positive | 96% positive |
| 50% true | 43% positive | 96% positive |
| 80% true | 65% positive | 96% positive |
| 100% true (impossible ceiling) | 80% positive | 96% positive |

Even the most generous assumption, that every tested hypothesis is true, cannot explain a 96% rate under honest methodology. The literature is not a discovery stream. There are three ways to produce the gap:

- *Nulls get buried.* Honest tests return nulls but the nulls don't publish, so the record sees only the positives.
- *Data gets sculpted.* Data gets massaged until it shows something promising. The survivor gets written as if preregistered.
- *Tests get picked to pass.* Researchers select experiments their hypothesis is already highly likely to win: large effect sizes, easy endpoints, populations where the effect is known to hold. Effective power approaches 1.

Burying nulls is fraud by omission. [HARKing](https://en.wikipedia.org/wiki/HARKing) is fraud by commission. And the third requires no fraud: it's career-preserving risk aversion. Of course a rational researcher operates under publish-or-perish. Regardless of which, all three produce the same rotten literature.

[Sterling (1959)](https://www.jstor.org/stable/2282137) found 97.3% positive in four psychology journals. The same journals, thirty-six years later: 93–99%. Across twenty disciplines, [Fanelli (2010)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0010068) measured economics at 88.5%, psychology and psychiatry at 91.5%. Between 1990 and 2007, the rate grew another 22% ([Fanelli 2012](https://link.springer.com/article/10.1007/s11192-011-0494-7)). [Ioannidis (2005)](/reading/scientific-method/ioannidis-2005/) gave the Bayesian version: given typical power and pre-study odds, the positive predictive value of a published biomedical finding is below 50%.

The system does not require red-teaming before publication. Everybody seems to be writing the positive papers that keeps the grant funding flowing.

If peer review was supposed to be adversarial, where's the accountability for the reviewers?

- A [2012 paper on signing honesty pledges at the top of a form](https://www.pnas.org/doi/10.1073/pnas.1209746109) (Shu, Mazar, Gino, Ariely, Bazerman) was cited in the [IRS Behavioral Insights Toolkit](https://www.irs.gov/pub/irs-soi/17rpirsbehavioralinsights.pdf) and absorbed into the nudge-unit literature before its data was shown to be fabricated by [Data Colada](https://datacolada.org/98).
- [Ego depletion](https://en.wikipedia.org/wiki/Ego_depletion), the claim that willpower is a finite resource, became the spine of Baumeister and Tierney's bestseller *Willpower* (2011) before the effect failed to replicate across labs ([Hagger et al. 2016](https://journals.sagepub.com/doi/10.1177/1745691616652873)).
- [Power posing](https://en.wikipedia.org/wiki/Power_posing) generated more than 70 million views for [Amy Cuddy](https://en.wikipedia.org/wiki/Amy_Cuddy)'s [TED talk](https://www.ted.com/talks/amy_cuddy_your_body_language_may_shape_who_you_are) and built a New York Times bestseller (*Presence*, 2015). Its first author, Dana Carney, later [publicly withdrew](http://faculty.haas.berkeley.edu/dana_carney/pdf_my%20position%20on%20power%20poses.pdf) in 2016, writing "I do not believe that 'power pose' effects are real." Cuddy did not.

#### Exhibit C. Work log

[Yoshitaka Fujii](https://en.wikipedia.org/wiki/Yoshitaka_Fujii) fabricated data across *183 papers* over nineteen years of peer review in anesthesiology. John Carlisle, a UK anaesthetist, [ran a distributional goodness-of-fit test](https://pubmed.ncbi.nlm.nih.gov/22404311/) on Fujii's published baseline statistics and reported the result in *Anaesthesia* (2012). The journals had no trail to audit.

- [Diederik Stapel](https://en.wikipedia.org/wiki/Diederik_Stapel): 58 retractions in social psychology. Detection came from three junior researchers in his own department who reported him to the department chair. Stapel was dean, so they had to go around him.
- Haruko Obokata's [STAP cells](https://en.wikipedia.org/wiki/Stimulus-triggered_acquisition_of_pluripotency): retracted within five months after [PubPeer](https://pubpeer.com/) commenters and a blog post analyzed the figures; *Nature*'s editorial [acknowledged](https://www.nature.com/articles/511005b) that "we and the referees could not have detected the problems that fatally undermined the papers."
- Francesca Gino: four papers retracted after [Data Colada](https://datacolada.org/) published a forensic analysis of the data files themselves.

What are the chances the caught fraudsters are the only ones frauding? A trial without a trail isn't a trial at all.

- Fujii's fabrications contaminated two decades of anesthesia meta-analyses. [Paolo Macchiarini](https://en.wikipedia.org/wiki/Paolo_Macchiarini)'s synthetic trachea transplants, [published in *The Lancet*](https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(11)61715-7/fulltext) and celebrated on television, killed most of their recipients before Swedish journalists forced the scandal open.
- [Wakefield](https://en.wikipedia.org/wiki/Andrew_Wakefield)'s 1998 MMR paper coincided with [UK vaccination rates falling from ~92% (1995–96) to 79.9% (2003–04)](https://researchbriefings.files.parliament.uk/documents/CBP-8556/CBP-8556.pdf), well below the 95% herd-immunity threshold, and seeded outbreaks in US pockets a decade later.

If there was evidence to support their claims, how did it suddenly disappear?

#### Exhibit D. The citation graph doesn't update

[Serra-Garcia and Gneezy (2021)](https://www.science.org/doi/10.1126/sciadv.abd1705) tracked citations in psychology and economics after replication failure. Papers that failed to replicate were cited *more* than papers that replicated, and only *12%* of post-failure citations mentioned the failure.

[Hsiao and Schneider (2021)](https://direct.mit.edu/qss/article/2/4/1144/107356) ran the same question across biomedicine. Of 13,252 citation contexts referencing 7,813 retracted PubMed papers, *5.4%* acknowledged the retraction.

The trail isn't just incomplete. The reader has no reliable way to tell whether the citation they just followed is still standing. Retraction is supposed to propagate, but the citation graph never grants it.

That matters because the reader is often a textbook, a policy brief, a clinical guideline, or an LLM. Claims enter downstream corpora and compound. When the original retracts, the downstream copies don't. The honesty-pledge result kept training students and shaping forms for years after its data was shown to be fabricated.

### The view from the inside

I once watched *The Act of Killing*, a documentary in which perpetrators of the Indonesian mass killings cheerfully [reenact their murders](https://www.youtube.com/watch?v=qenIrA0A4N8) for the camera. From inside the culture that celebrated them, the evil was invisible. They posed, they laughed, they corrected each other's technique.

The structure transfers even if the moral weight does not. A practice that looks pathological from outside is unremarkable from inside, because the local rituals make sense to the people performing them.

The invisibility runs to you, the LessWrong reader. Appeal to authority is a named fallacy. Did you ever believe someone because they studied at Harvard or Stanford? Did you find a paper more credible because it had many citations? If so, you're a part of the problem. That reflex, unnoticed and routine, is the symptom under diagnosis.

Not every appeal to authority is a fallacy. For a layperson deferring to expert consensus, it is a reasonable division of epistemic labor; you can't personally check every claim. But for one scientist citing another scientist's credence, that's when it becomes a fallacy.

The same invisibility produced eugenics. [R. A. Fisher](/reading/scientific-method/fisher-1935/), patron saint of statistical inference and inventor of the p-value, was an active eugenicist. Peer-reviewed journals published the work through the 1930s, and forced sterilizations continued into the 1970s. The institution now treats eugenics as an alien moral failure rather than as work once published, funded, taught, and credentialed from inside the house. Credentialed consensus, journals, and prestige launder ideology as knowledge. That is the mechanism.

PhD students aren't villains for wanting to be credentialed, nor are advisors for teaching them who to schmooze with. Nor are labs for pumping up those publication numbers. The institution is internally coherent. A discipline that can't discipline itself is a profession.

#### Who is the jury?

If the jury is other credentialed scientists, science is a priesthood with extra steps. The same people who wrote the papers gatekeep their temple.

The outside jury is already in session. [Retraction Watch](https://retractionwatch.com/) logged 140 retractions in 2000 and more than 10,000 in 2023. [Elisabeth Bik](https://en.wikipedia.org/wiki/Elisabeth_Bik) has surfaced image manipulation in more than 4,000 papers. Data Colada's forensic analyses took down Ariely's 2012 honesty paper and four of Gino's; [Harvard revoked Gino's tenure in May 2025](https://api.thecrimson.com/article/2025/5/27/gino-tenure-revoked/), apparently the first such revocation since at least the 1940s.

In March 2020, Bik [publicly criticized](https://scienceintegritydigest.com/2020/03/24/thoughts-on-the-gautret-et-al-paper-about-hydroxychloroquine-and-azithromycin-treatment-of-covid-19-infections/) Didier Raoult's hydroxychloroquine paper, flagging non-randomized controls and six omitted treated patients, including one who died. In April 2021, Raoult's IHU in Marseille [filed a criminal complaint](https://www.nature.com/articles/d41586-021-01430-z) against her for *harcèlement moral aggravé*, *tentative de chantage*, and *tentative d'extorsion*. The prosecutor [reportedly closed it](https://www.leparisien.fr/sciences/ils-traquent-les-etudes-bancales-ou-frauduleuses-la-croisade-des-chevaliers-blancs-de-la-science-02-06-2024-IO6WRR47XBBXJGTKRXYC3VHSIM.php) in March 2024. The paper was [retracted](https://www.nature.com/articles/d41586-024-04014-9) in December 2024.

The jury should be anyone who can read the evidence trail.

#### It's a club

Put in economic terms, the scientific community functions as a cartel. Peer review is the admissibility rule. Citation is the currency. Credentialing is the output the members license. When an outside auditor produces an inspectable claim (Bik, Wilmshurst, Data Colada), the club answers with criminal complaints, libel suits, and defamation claims. [George Carlin](https://en.wikipedia.org/wiki/George_Carlin) said it better than the auditors: *"It's a big club, and you ain't in it."*

You would think that the journal is a stream of discoveries, but if you look closer, it's a trophy case for grant applications. What can't be displayed isn't submitted, and what is submitted is written for the trophies.

The labor structure confirms the shape. [NIH predoctoral stipends](https://grants.nih.gov/grants/guide/notice-files/NOT-OD-25-105.html) work out to $13.84 an hour at forty hours. It's below the minimum wage in New York, San Francisco, or Boston. Research hours are rarely forty. Postdocs at the NIH scale approach or cross the line at 60–70 hour weeks. [14% of doctorate recipients self-finance out of personal resources](https://ncses.nsf.gov/pubs/nsf24336). Only [7–8% of 2024 research-doctorate recipients](https://ncses.nsf.gov/pubs/nsf25349/assets/data-tables/tables/nsf25349-tab006-001.pdf) had an immediate tenure-track job lined up. The lotto is negative EV.

The price of the ticket also rises. [Academic postdocs grew from 12,500 in 1979 to 70,000 in 2024](https://ncses.nsf.gov/pubs/nsf26308); multi-year postdoc chains are standard, and [assistant-professor candidates arrive at hiring with materially more publications than their predecessors](https://pmc.ncbi.nlm.nih.gov/articles/PMC9604874/). The cartel's temporal shape is a [pyramid](https://en.wikipedia.org/wiki/Pyramid_scheme). Early entrants already cashed in. Later cohorts are inflating credentials against diminishing real positions, and each new generation subsidizes the last with cheaper labor and heavier dues.

Despite this, good work still gets done inside the club, by people paying personal cost to do it right.

#### "But Gino and Ariely were outliers"

Three of the four exhibits above describe honest work. Exhibit A, where 49 percentage points of positive cardiovascular findings evaporated under pre-registration, involves no fraud. Exhibit B, the 96% positive-result rate persisting since 1959, requires no fabrication. [P-hacking](https://en.wikipedia.org/wiki/Data_dredging), HARKing, and selective outcome reporting are all within the rules. Exhibit D, citations that don't update when papers retract, is infrastructure.

Fraud is the one failure mode the institution acknowledges. The other three are what happens when the protocol is optional.

The 96% rate predates Ariely's first paper by half a century. When Sterling documented 97% positive in 1959, Gino was not yet alive.

#### "But science is self-correcting"

If self-correction means publishing a retraction, yes. If it means the update propagating through the literature, no.

Hsiao and Schneider found that *5.4%* of citations to retracted biomedical papers acknowledge the retraction. Serra-Garcia and Gneezy found that papers that failed to replicate are cited *more* than papers that did. Retractions are filed, not enforced.

A self-correcting system requires that the correction propagate faster than the original claim. The citation graph runs the other way.

The record also fails to carry the corrections the field already knows about. Replication failure is not a retraction criterion, so retractions alone won't match replication rates. But the literature should carry visible caution markers (failed-replication notices, effect-size revisions, boundary-condition warnings) on papers whose claims the field has stopped believing. It doesn't. A paper that stopped replicating a decade ago is still cited naked, indistinguishable from one that held up.

#### "But failed replication doesn't mean the original was false"

A result that does not transport has not earned the general claim built on top of it. [Pearl](/reading/scientific-method/pearl-2000/)'s point: transportability requires explicit assumptions about causal structure and context, assumptions usually unstated and untested. If your finding holds only for college sophomores on a Tuesday in 1998, you didn't discover a law of human nature. You recorded an anecdote. Publishing it as a law and citing it as such is the error.

#### "But pre-registration isn't appropriate for exploratory science"

It is, and especially then. A declared goal shapes the exploration. Science without a goal is philosophy. Registering the question is the courage to be publicly wrong, and it coordinates other scientists who can shake maximal surprise out of the data instead of settling for a 95%-confidence prior. And since when is p = 0.05 an arbiter of truth?

#### "But truthseeking happens despite the institution"

Yes. That is the argument. Real discovery is already routing around the credentialing mechanism, inside universities as much as outside them.

- *Physics and math on [arXiv](https://arxiv.org/) + community.* [LK-99](https://en.wikipedia.org/wiki/LK-99) was claimed as a room-temperature superconductor in July 2023. By mid-August, a global informal replication effort (preprints, Twitter, livestreamed syntheses) had produced consensus that it wasn't. No journal was involved until after the question was settled. [OPERA](https://en.wikipedia.org/wiki/Faster-than-light_neutrino_anomaly)'s 2011 faster-than-light neutrino claim was traced to a loose fiber-optic cable through the same mechanism.
- *Formal verification.* [Peter Scholze](https://en.wikipedia.org/wiki/Peter_Scholze) publicly invited the [Lean](https://en.wikipedia.org/wiki/Lean_(proof_assistant)) community to verify his [Liquid Tensor Experiment](https://xenaproject.wordpress.com/2020/12/05/liquid-tensor-experiment/) in 2020, conceding he wasn't fully sure the proof was right. The verification was completed in 2022. Scholze has since described the Lean version as the one he trusts.
- *Open-weight ML.* Models from Meta, DeepSeek, and Mistral ship with weights, code, and benchmarks. Auditability is materially better than journal-only publication. No journal acceptance is required and no one in the field is waiting for one.
- *Independent auditors.* Data Colada, Elisabeth Bik, Retraction Watch, Gwern, PubPeer. The actual epistemic labor of the field is happening in blogs, databases, and image-forensics tools: outside the journal process, often outside universities, always outside the original peer-review channel.

Science is happening, outside the sanctioned peer-reviewed journal process.

#### "But the outside jury can become a mob"

Yes, outside scrutiny can become performative or punitive. Online auditors can be wrong; reputational damage can run ahead of adjudication; selective outrage is real. That is why the standard has to be verifiable claims, not vibes. The checker checks, and the checker is checkable in return. The inside, by contrast, has been publishing mob verdicts, credentialed and peer-reviewed and catastrophically wrong, regardless. Eugenics, [recovered memory](https://en.wikipedia.org/wiki/Recovered-memory_therapy), [cold fusion](https://en.wikipedia.org/wiki/Cold_fusion), ego depletion.

Peter Wilmshurst, co-principal investigator of the MIST cardiac-device trial, publicly challenged the trial's handling at a 2007 conference and refused to sign off on the *Circulation* paper. NMT Medical, the sponsor, sued him for libel in English court. In December 2010 the High Court [ordered NMT to post £200,000 in security for costs](https://www.theguardian.com/science/2010/dec/01/company-suing-peter-wilmshurst-libel); [NMT went into liquidation in April 2011](https://www.theguardian.com/uk/2011/apr/21/us-company-suing-doctor-libel) and the case died with it.

A noisy but auditable process is already more accountable than the trust-me-bro peers.

#### "But without peer review, how am I supposed to trust anybody?"

Credentialed consensus is how geocentrism survived. For centuries, Europe's credentialed natural philosophers inherited a geocentric cosmology and defended it against heresy. The consensus broke not because of better review but because Kepler had data and Galileo refused to defer.

The standardized, journal-centered, anonymous external referee process now treated as the source of scientific trust is largely a twentieth-century consolidation. Darwin, Einstein, Newton, Maxwell, Mendel, Watson and Crick: none of their canonical work passed through today's referee regime. Was science untrustworthy until the mid-twentieth century?

The objection itself is an appeal to authority. "How do I trust anybody" asks for a credential to defer to. That's the lazy way out. Instead, verify. When verification was expensive, deferral is just what we happened to do. Now that verification and data analysis are 100x cheaper with AI, the excuses are running out.

To claim truth in science, implement:

- *Replicability.* A result with inspectable materials (data, code, protocol, independent replication) earns more trust than venue alone. A paper whose record cannot be reconstructed is not trustworthy regardless of where it appeared. "Here is the repo" is the modern peer review where the work is software; "here is the cohort" or "here is the apparatus" where it is not.
- *Public process.* A preprint with open comments, a GitHub repo with issues, a [Polymath](https://en.wikipedia.org/wiki/Polymath_Project) thread, a formal proof in Lean. Each gives the reader more audit surface than two anonymous referees.
- *Convergence.* Five independent replications beat one top-journal paper. [Many Labs](https://www.cos.io/initiatives/many-labs), [RPCB](https://www.cos.io/rpcb), and the [Camerer replication projects](https://www.science.org/doi/10.1126/science.aaf0918) turn journal acceptance into an input.
- *Track record.* Writers who publish under their name, maintain visible forecasts, archive their revisions, and get corrected in public carry more credibility than any single paper. Reputation built on auditable output outlasts one round of double-blind review.

Peer review catches errors before publication. Useful, not dispositive, insufficient. The institution lost the thread when it started treating it as a certificate of truth.

#### "But it's the best we can do"

The argument: reviewers have finite bandwidth, editors have deadlines, and scientists cannot be expected to document every false start while producing new work.

Every other industry that does serious work refutes this. Software engineers run version control, code reviews, and postmortems. Aviation maintains incident logs and black boxes. Pharmaceutical labs keep rigorous notebooks because patent law requires it. Finance runs on audit trails. Medicine runs on surgical checklists and [M&M conferences](https://en.wikipedia.org/wiki/Morbidity_and_mortality_conference). None publish externally. All maintain internal trails that survive the individual's departure.

Publishing the protocol does not mean announcing results to the world. It means committing to a trail the next person in your role can audit. The scope of that trail is whatever IP, regulation, or competitive position allows: private, classified, internal. The discipline is not optional.

### My own exhibit

I have run the protocol on myself. In a [preregistered experiment](/theory-is-load-bearing), the final posterior came in at 0.949, a thousandth below the 0.95 threshold I had committed to beforehand. By my own rule, the result does not confirm. I said so. Reporting a null I had every incentive to round up was harder than any positive result I have published.

### Your turn

If you read science: ask whether you can reproduce what you cite. Reject credence on credence alone; demand the evidence, the methodology, the thought process that led to the conclusion. If you write science: pre-register, publish the nulls, keep the log, release the data, write the replication. Run every draft through an LLM adversary first: every citation, every claim, every inference. If the LLM can find the hole, the replicator will. If you fund or hire: trail quality as the metric. Mandate data sharing. Require [Registered Reports](https://www.cos.io/initiatives/registered-reports) for confirmatory work.

The reforms exist. Will the incentives change in pursuit of truth?

---

*Written via the [double loop](/double-loop).*
