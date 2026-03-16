Suppose you're convinced that [open sourcing everything](/paradox-of-open-competition) means no moat. And no moat means the business is uninvestable. So be it.

## Why Firms Exist

[Ronald Coase](https://doi.org/10.2307/2626876) asked in 1937: why do firms exist at all? If markets are efficient, why isn't everyone a freelancer? His answer: because using the market is expensive. "The main reason why it is profitable to establish a firm would seem to be that there is a cost of using the price mechanism." Finding prices, negotiating contracts, monitoring compliance. These transaction costs justify putting people under one roof and one authority. The firm expands "until the costs of organising an extra transaction within the firm become equal to the costs of carrying out the same transaction by means of an exchange on the open market."

[Oliver Williamson](https://www.nobelprize.org/uploads/2018/06/williamson_lecture.pdf) (Nobel 2009) made this precise. What makes market transactions expensive? Three things: *bounded rationality* (people can't write contracts for every contingency), *opportunism* (people cheat when they can), and *asset specificity* (once you've invested in a relationship, you're vulnerable to renegotiation). When all three are high, you bring the activity inside the firm. When they're low, you use the market.

AI is driving all three toward zero. Bounded rationality? AI drafts contracts covering contingencies humans would miss. Opportunism is harder when code is auditable, contributions are timestamped, and reputation is public. Asset specificity dissolves when anyone can be onboarded in minutes and codebases are self-documenting. No single contributor creates a holdup problem.

Yochai Benkler saw this coming in 2002 with "[Coase's Penguin](https://yalelawjournal.org/article/coases-penguin-or-linux-and-the-nature-of-the-firm)," arguing that open source represents a third mode of production beyond firms and markets: commons-based peer production. It works when the object is information, capital (computers) is distributed, and the best person for each task can self-select. All three conditions are now met at a scale Benkler couldn't have imagined.

MIT and Harvard economists coined the term "[Coasean Singularity](https://www.nber.org/books-and-chapters/economics-transformative-ai/coasean-singularity-demand-supply-and-market-design-ai-agents)" in 2025: the tipping point where AI agents reduce transaction costs to near-zero. If market transaction costs approach zero, the optimal firm size approaches one.

This isn't speculative. [GitLab](https://handbook.gitlab.com/handbook/values/) runs a [2,300-person company](https://stockanalysis.com/stocks/gtlb/employees/) with a [public handbook](https://handbook.gitlab.com/handbook/company/culture/all-remote/handbook-first/) over 2,000 pages long that replaces managers as information brokers. Everything is [public by default](https://handbook.gitlab.com/handbook/security/transparency-by-default/); if something is private, there must be a documented justification. Even their security team operates transparently: "This openness keeps GitLab honest. When someone is honest, people are more likely to trust them." Over [4,000 external contributors](https://about.gitlab.com/community/contribute/) work alongside employees without employment contracts. The firm boundary is explicitly porous. They ship a new version every month, [160 months in a row](https://handbook.gitlab.com/handbook/company/stewardship/). The handbook replaces hierarchy. The default is open. The burden of proof is on secrecy, not transparency.

## What AI Doesn't Eliminate

What transaction costs does AI *not* eliminate? [Trust](https://pubsonline.informs.org/doi/10.1287/orsc.14.1.57.12806). [Judgment](https://www.london.edu/think/good-news-for-human-beings-ai-doesnt-do-judgement). Taste. Reputation. The things that make someone want to work with *you* specifically. Those aren't transaction costs. Those are the product.

And the Williamson conditions don't actually hit zero. Bounded rationality shifts rather than disappears. AI drafts better contracts for known contingencies, but the most valuable work happens in novel territory where you don't even know what to contract over. When you're figuring out what the product should be, the hard part isn't writing the agreement. It's knowing what question to ask. Opportunism gets subtler, not eliminated. Auditable code catches blatant cheating. It doesn't catch strategic information withholding, or someone who knows what you need and slow-plays sharing it because they're hedging their own position. The most costly opportunism was never someone stealing code. It was misaligned incentives that nobody could see.

There's also something AI can't replace that Coase never accounted for: generative proximity. People working closely together produce ideas that wouldn't exist otherwise. Coase explained why firms *coordinate* work. He didn't explain why co-presence is *generative*. The offsite vision later in this post acknowledges this. You still want people in a room together, not because coordination requires it, but because collision produces things that solo work doesn't.

So the firm doesn't shrink to one for everyone. The prediction is bimodal. Solo founders and duo ventures flourish at the creative edge. Platform mega-firms (Anthropic, AWS) get bigger because they own the coordination infrastructure. What hollows out is the middle: the 50-person SaaS company with a moat made of features that Claude can rebuild in an afternoon.

## What Falls Away

If the firm boundary dissolves, so do the signals that proved you belonged inside it.

[Michael Spence](https://doi.org/10.2307/1882010) won a Nobel for formalizing why credentials exist. Employers can't observe ability directly, so workers acquire costly signals: degrees, brand-name employers, accelerator badges. The signal works because it's differentially expensive. Getting into Stanford is harder if you're less capable. That cost differential is what makes it informative. Remove the information asymmetry and the signal is just an expense.

Direct observation removes it. Open source contributions, public repos, and weekend [vibelogging](/vibelogging) sessions let you inspect the work before you commit to the person. [Phillip Nelson](https://doi.org/10.1086/259630) distinguished search goods (quality visible before purchase) from experience goods (quality visible only after). Workers were experience goods. You hired, waited, and found out. When the work is public, workers become search goods. The credential was the cost of not being able to look. Now you can look.

[Farber and Gibbons](https://doi.org/10.2307/2946706) showed that as employers accumulate performance observations, the credential's informational content approaches zero. The credential is a prior. Direct observation is the posterior. Enough data and the prior washes out. Near-zero onboarding costs compress this from years to hours. Bring someone to an offsite. Watch them work. Part ways if it doesn't fit. The trial is cheaper than the signal. [David Autor](https://academic.oup.com/qje/article-abstract/116/4/1409/1903245) documented this exact dynamic in temp agencies: they offer free training not as charity but as screening. The training period is the evaluation.

Stanford, Google, YC, Thiel Fellow. These are [pooling equilibria](https://doi.org/10.2307/1885326). Everyone in the bucket looks the same. The signal tells you "probably capable" but not which kind or how. Direct observation collapses the pool. What replaces it is separation by revealed ability: what you built, how you built it, whether you'd be good to build with again.

People are wondering how to evaluate candidates now that AI writes the take-home and aces the interview. That's the wrong question. Evaluation was solving for a firm boundary that no longer holds. It's guards at the bouncy castle.

## The Banquet

If credentials fall, so does the funding model built on them. Venture capital is a signaling market. Founders signal quality through pedigree. VCs signal judgment through brand. They match through relationship networks that function as costly signals. When founder quality is directly observable, the intermediary's gatekeeping function evaporates. [Anne Krueger](https://doi.org/10.2307/1808883) named the pattern in 1974: rent-seeking. Intermediaries capture income not by creating value but by controlling access. The rent is propped up by the [bridge troll](https://youtu.be/Wpx6XnankZ8?t=144). *No bridge, no toll.*

[J.P. Morgan](https://en.wikipedia.org/wiki/Pujo_Committee) personally decided which companies got funded. His partners held 341 directorships across 112 corporations controlling $22 billion. The [SEC](https://en.wikipedia.org/wiki/Pecora_Commission) broke this by mandating disclosure. The relationship banker's edge was that nobody else could look at the books. The SEC made everyone look. Under [Regulation Q](https://www.federalreservehistory.org/essays/regulation-q), banks monopolized deposits because the government capped interest rates. When [money market funds](https://www.federalreservehistory.org/essays/money-market-mutual-funds) offered market rates in 1971, [747 savings and loans collapsed](https://www.federalreservehistory.org/essays/savings-and-loan-crisis) within fifteen years. The monopoly rested on a structural constraint. A new channel removed it.

[Britain's landed gentry](https://www.jstor.org/stable/j.ctt1ww3txs) followed the same arc. In 1825, nearly all of the country's 200 wealthiest were landowners. By 1914, two-thirds were not. Corn Law repeal collapsed agricultural returns. The Benthamite reforms replaced aristocratic appointment with competitive examinations. Then the war taxed what remained. The families persisted through property and social connections, but their gatekeeping power was gone. [Barry Lyndon](https://www.youtube.com/watch?v=9lzSoKOs1fc) is the story of a man acquiring the trappings of status just as the rents sustaining it were being legislated away.

The VC's judgment was the prior. The public repo is the posterior. The [vector space](/vector-space) work on this blog proved one class of transaction costs, [keyword-based ad auctions](/keyword-tax), can be replaced by a mechanism that eliminates the intermediary's information advantage. If capital allocation follows the same pattern, the wine-tasting clubs and ski-trip deal flow will look, in retrospect, like the Medici throwing banquets to maintain a lending network that public markets had already made obsolete. [Florence's banking families from 1427](https://qz.com/694340/the-richest-families-in-florence-in-1427-are-still-the-richest-families-in-florence) are still wealthy in 2011, but as landlords, not gatekeepers. The power shifts from active allocation to passive preservation.

## Ephemeral Businesses

If the castle is crumbling, the businesses inside it are temporary.

[Jasper AI](https://research.contrary.com/company/jasper) peaked at a $1.5 billion valuation in January 2023, projecting $250 million ARR. Then OpenAI improved ChatGPT's content generation. Revenue plummeted from $120M to $55M. Both co-founders left. An entire category of PDF chat startups, [ChatPDF](https://getlatka.com/companies/chatpdf.com) and dozens like it, went from premium products to redundant overnight when ChatGPT added native document understanding. [Tome](https://tome.app/) was a viral AI presentation tool with millions of users until Microsoft embedded Copilot into PowerPoint; they sunsetted their slides product entirely. When OpenAI launched [AgentKit](https://max-productive.ai/blog/openai-devday-2025-agentkit-apps-sdk-gpt5-pro/) in October 2025, it threatened the entire $6.65 billion workflow automation market that Zapier and a thousand startups had built.

[90% of AI wrapper startups](https://www.machinebrief.com/news/death-of-ai-wrapper-startups-wont-survive-2026) shut down within 18 months. An anonymous founder [posted on OpenAI's forum](https://community.openai.com/t/openai-why-are-you-killing-my-startup-for-the-second-time/1355491): "OpenAI, why are you killing my startup — for the second time?"

## The Facade

It's increasingly looking less like a salary and a 4-year vest. Who gets paid and who doesn't? I don't know, this is all new to me too. How do you distribute credit for one cool idea that helps billions of people in a small way?

People do build real relationships at startups. The friendships are genuine. The late nights shipping something together are real. I'm not dismissing that.

What I'm calling a facade is the *institutional promise*. Founders pitch the company as a place you'll grow your career for years. They talk about professional development, advancement tracks, lasting culture. The honest version of a startup pitch is: "We'll exist for as long as this is the best thing we can be doing, and then we won't." Most startups last a few years at best. Employee tenure at tech companies averages around two. Everyone knows this. The pitch pretends otherwise because admitting that the company is a temporary vehicle makes it hard to hire people who want stability. But stability was always the institutional lie. The four-year vest was the mechanism for maintaining it long enough to find out if the business works.

If I ever have enough money to support development, I wouldn't spend it on payroll. Payroll means I'm responsible for someone's future income, which means I need a moat to protect the source. I'd spend it on offsites. [Vibelogging](/vibelogging) sessions where contributors meet as peers, work on the thing together in person, and go home when it's done. No equity grants. No four-year cliffs. No promises about the company's finances that I can't keep because Anthropic might announce a side feature next Tuesday.

We'd meet as collaborators to the same vision. Some would come once. Some might stay for years. And those minds will mingle to magistrate their own solo or duo venture. That's the point. The best outcome of an open project isn't that it becomes a unicorn. It's that it becomes a greenhouse. Great companies form as a result of people working together on something they believe in, not as a result of locking them into a cap table. The bouncy castle deflates either way. Better to have been the greenhouse next door.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude researched citations and drafted prose.*
