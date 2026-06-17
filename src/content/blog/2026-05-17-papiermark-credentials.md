---
variant: post
title: "Papiermark Credentials"
tags: pageleft, reflecting
---

> In 1914, the German [Papiermark](https://en.wikipedia.org/wiki/Hyperinflation_in_the_Weimar_Republic) traded at 4.2 to the dollar. By November 1923, it took 4.2 trillion. A loaf of bread that cost a quarter mark before the war cost 200 billion. Workers were paid twice a day so they could spend their wages before lunch devalued them. Children built towers from bricks of cash. The Reichsbank ran 1,800 printing presses through 133 contracted firms to keep up. The notes were impeccable. The press couldn't print bread.

And neither do diplomas produce science.

As universities produce more scientists than science: PhDs, postdocs, h-indexes, named chairs; the output that pays the bills has decoupled from the output that justifies them. The university needs tuition, grant overhead, and prestige metrics; PhDs are how those bills get paid. Whether the PhD corresponds to a scientist who produces science is a second-order concern.

This is the Papiermark. More notes printed, same underlying wheat. The issuer had a budget constraint easier to solve by printing than by producing.

I publish under copyleft, ship code to repos I don't own, and built [PageLeft](/pageleft) to make timestamped prior art enforceable. I am long contribution and short credential. The position is self-serving in a specific way: those of us long merit and short credit are most incentivized to bootstrap the merit economy. The substrate gets built by the most qualified people who happen to need it.

The argument: AI pushes meritocracy back into the slot credential used to occupy, starting in fields where a verification agent can already check the receipts: software engineering, formal mathematics, open research, anything whose proof lives in public repos and signed commits. Wet-lab biology, surgical certification, and clinical psychology run on different substrates; I'm not arguing about those people. Papiermark dynamics apply there too, but the arbitrage window I'm naming is where verification has already gone digital and cheap.

## The data

The average paper in engineering [cited 8 references in 1972 and 25 in 2013](https://arxiv.org/abs/1306.4223). Across disciplines, the average rose from 29 in 2003 to 45 in 2019; the [PLOS One authors](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0255849) note "reference saturation is not yet in sight." [Author lists tripled between 1900 and 2015](https://academic.oup.com/gigascience/article/8/6/giz053/5506490). Per paper: three times the references, three times the names.

Real output per researcher went the other way. Cordero et al. tracked the [average publishable unit](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0156983) in life sciences and found it doubled in two decades: more figures, more authors, more pages per paper, more bar to clear. [Bloom et al.](https://www.aeaweb.org/articles?id=10.1257/aer.20180338) found research productivity itself declining across fields by orders of magnitude. More padding per loaf. Less wheat in the field.

Three-times reference inflation in forty years, with content per paper trending down. That is monetary base expanding while real output contracts. Textbook inflation.

The PLOS authors blame "political considerations during the process of writing, especially the selection of important references." People inside the system, writing in a journal, say out loud that citations are political tribute.

## The axis

Credential and contribution sort onto opposite sides of a line.

- issued → produced
- terminates at the body → forks
- verified by committee → verified by execution
- needs tribute (citations, coauthors, references, lit reviews) → needs use (merges, imports, dependencies, downstream forks)
- unfalsifiable → either runs or it doesn't
- cost rising → cost collapsing

Nobody checks if you read those references, whether they support the claim, whether the citation ring is mutual back-scratching. Someone bisects to your commit when it breaks them. That's the whole axis in one sentence each.

## Cost of verification

Checking merit used to be genuinely expensive. If you ran an operations research experiment optimizing a factory floor, nobody was going to rebuild the factory to confirm your numbers. The reviewer trusted the institution that trusted the methodology that trusted the data. Five layers of trust because the actual verification was uneconomic. That's where the proxy lived.

When the factory is [turning issues into PRs](https://github.com/kimjune01/sweep), the proof is in the pudding. Anyone can read the issue, read the PR, run the tests, check the merge. Then they can check the agent prompts and harnesses that produced them. An agent runs the whole audit in under a minute: GQL query, dependency graph, blame on the line, reviewer history, downstream import weight. Each hop is a query. The audit points the right way: what the code does and who depends on it, not surface metrics like stars.

Once verification is cheap, institutions that verified expensively lose their seigniorage. Journals, accreditation bodies, hiring pipelines existed because checking was hard. They charged rent on that cost. Agents arbitrage it away.

A cold PR to a repo with real maintainers is the gold redemption event in this picture. The maintainer didn't ask for it, has their own taste and their own time, and will read the diff. The repo has downstream users who bisect to your commit when it breaks. The merge is a public, timestamped signal from someone whose own reputation is on the line. You cannot spin up Linus accepting your kernel patch. You cannot prompt your way into his git log. The [provenance](/provenance-has-no-half-life) is held by parties who didn't consent to be your reference, which is exactly why it's worth something.

The credential isn't "I have N merged PRs." It's "I have merged PRs to repos whose maintainers are themselves gold-backed." Recursive, like [PageRank](https://en.wikipedia.org/wiki/PageRank), but with skin in the game at every node. An agent can compute it. A hiring committee reading a CV cannot.

## External receipts

A textual fingerprint won't save the audit. There's a slop floor and a slop ceiling. Below the floor, frontier models flag low-effort generated text, even text they wrote themselves. Above the floor, [detection is a wasting asset](/slop-detection): I ran this experiment; style cracks in one round of adversarial feedback, structure in two. Any textual signal an agent uses gets optimized against in the next draft.

What doesn't crack is external reference. A merged PR has a maintainer who actually reviewed it. An equation either checks or doesn't. A cited statute either exists with the holding you claimed or doesn't. The artifact has receipts held by parties the model can't prompt: GitHub's signed commits, the journal's published holding, the operator running the system in production.

Fake work in this regime defames the author forever. There is no "available upon request" deniability for a repo with timestamped commits. The Internet Archive doesn't forget. A retracted paper is a citation footnote. A fabricated contribution graph is a record anyone with five minutes and an agent can replay.

An agent verifying a CV inspects GPT-polished text. An agent verifying a contribution graph inspects the world wide web.

## The arms race

Employers and candidates are about to enter an arms race on peer verification, both sides optimizing against the same contribution-graph substrate. The deeper the candidate's verifiable provenance, the deeper the employer's auditing agent. Why are you still reading PDFs when your competitor's agent is reading the graph? The resume is the casualty. It can't be sharpened, only abandoned, because the cost of generating one fell faster than the cost of reading one.

Networking is the obvious objection: referrals always beat resumes anyway. But networking has its natural limits. One person can vouch for [a few dozen people at most](https://en.wikipedia.org/wiki/Dunbar%27s_number). The social graph is regional, biased toward whoever you already know, and the very property that makes a referral worth something (small trust circle) caps how far it reaches. A contribution graph has no such ceiling. A maintainer in Lagos can vouch for a contributor in Seoul by merging the patch, and the merge weighs the same as one from a maintainer at Google. Networking scales to your address book. Verifiable contribution scales to the open internet.

You either know people who will get you hired, or you show merit. Those are the two doors. Got merit but no graph? Start shipping. There's no other door. Everything else is either an address book or a Papiermark.

## The curves diverge

For the credentialed: the cost of producing a unit of credential-denominated output has stayed flat or risen. More coauthors needed. More references to manage. More reviewer politics, more grant overhead. The Papiermark gets more expensive to print even as each note is worth less.

For the non-credentialed: cost of producing actual research has collapsed by orders of magnitude in a decade. Compute is rented by the hour. Datasets are public. Preprint servers route around journals. LLMs collapse the cost of literature review, code scaffolding, math checking, formal verification. The work, if it works, is gold the moment it executes.

Research-per-dollar is up roughly an order of magnitude for someone with no institutional affiliation. That's my estimate; the underlying compute, dataset, and tooling costs each fell at least that much in a decade. Output follows. It lands wherever the publishing surface and the audit surface coincide. arXiv still gates; Substack still walls. The corner that's open on both sides is where the curve runs, and the corner is much bigger than the credential institutions noticed:

<div class="table-wrap">
<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col><col><col><col><col></colgroup>
<tr><td>GitHub</td><td>GitLab</td><td>Codeberg</td><td>Sourcehut</td><td>Bitbucket</td></tr>
<tr><td>npm</td><td>PyPI</td><td>crates.io</td><td>Maven Central</td><td>RubyGems</td></tr>
<tr><td>Hugging Face</td><td>Kaggle</td><td>Replicate</td><td>Modal</td><td>F-Droid</td></tr>
<tr><td>Mathlib</td><td>AFP</td><td>OpenReview</td><td>JOSS</td><td>OEIS</td></tr>
<tr><td>CVE</td><td>HackerOne</td><td>Bugcrowd</td><td>OpenStreetMap</td><td>Stack Overflow</td></tr>
</table>
</div>

Each cell is a surface where the work is shown, not told, and where a referee outside the author's control settles the question. Code that compiles, packages that get imported, models that hit a benchmark, proofs that type-check, bugs that vendors confirm, edits that survive the next reviewer's diff. The set isn't exhaustive. It's the visible floor of something that's still growing.

You may think of merit as inner virtue, deservingness, or the moral worth of the worker. Here, I mean merit to be auditable work that needs no proxy. Credentials are cached trust. Merit is a ratchet: auditable, fully legible to anyone, anywhere.

The divergence is structural. For a decade, hiring committees and grant panels will still be denominated in Papiermarks while the actual production of knowledge has already moved to gold.

That gap is the opportunity.

## The prophecy

Meritocracy is the only virtue that survives the AI cat-5 storm. Every other social currency rides on signals the storm shreds: provenance gets faked, references get prompted, prestige gets generated, gatekeeping gets bypassed. What survives is the artifact a stranger can inspect with their own eyes. The storm tears down everything that wasn't already essential. Merit is what's left when the wind stops.

## New Regime

Credentials die with the author. The science lives on without.

The PhD, the tenure, the h-index, the named chair. None of it forks, gets imported, or runs after the author stops. The credential is a life estate that reverts to nothing on death, while the contribution keeps executing. People depend on it without knowing the author's name. Value so liquid it has stopped tracking its origin.

As Papiermark accumulates to the person and dies with them, so does the credentialed researcher cling to their name. As gold accumulates away from the person and outlives them, so does the researcher release work into infrastructure where it gets used so heavily nobody needs to credit them.

[Ramanujan](https://en.wikipedia.org/wiki/Srinivasa_Ramanujan) filled his notebooks as an autodidact in Madras, before Hardy answered his letter. They are still being mined a century later. The Cambridge fellowship and the FRS came in the last four years of his life; he died at thirty-two. The Papiermark holders of 1920 are dust. The gold he minted is still circulating.

The exchange rate hasn't repriced yet. It will.
