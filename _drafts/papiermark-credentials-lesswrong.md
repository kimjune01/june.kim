# Papiermark Credentials

A credential is cached trust: a compressed claim that someone, somewhere,
checked the work. Merit is a ratchet: auditable, fully legible to anyone,
anywhere.

Goodhart starts when the cache becomes the target. More citations, longer author
lists, more credentials, more prestige markers. The proxy expands because the
thing it measures is expensive to inspect.

AI changes the cost curve. If an agent can unfold a repository, trace a
citation, check a proof, replay a benchmark, inspect a contribution graph, or
read the review trail in minutes, then the old cache has to be revalidated. Some
of it will survive. Much of it will not.

In 1914, the German Papiermark traded at 4.2 to the dollar. By November 1923, it
took 4.2 trillion. A loaf of bread that cost a quarter mark before the war cost
200 billion. Workers were paid twice a day so they could spend their wages
before lunch devalued them. Children built towers from bricks of cash. The
Reichsbank ran 1,800 printing presses through 133 contracted firms to keep up.

The notes were impeccable. The press could not print bread.

And neither do diplomas produce science.

## The Proxy

A credential is useful when direct verification is expensive. If you ran an
operations research experiment optimizing a factory floor, nobody was going to
rebuild the factory to confirm your numbers. The reviewer trusted the
institution that trusted the methodology that trusted the data. Five layers of
trust because the actual verification was uneconomic.

That is where the proxy lived.

But proxies have a failure mode. Once the proxy becomes the target, the system
learns to print more proxy. The credential supply expands faster than the thing
the credential was meant to measure.

In academic science, the symptoms are visible. The average paper in engineering
cited 8 references in 1972 and 25 in 2013. Across disciplines, the average rose
from 29 in 2003 to 45 in 2019; one PLOS One study notes that "reference
saturation is not yet in sight." Author lists tripled between 1900 and 2015.
Per paper: roughly three times the references, three times the names.

Real output per researcher moved the other way. Cordero et al. tracked the
average publishable unit in life sciences and found it doubled in two decades:
more figures, more authors, more pages per paper, more bar to clear. Bloom et
al. found research productivity declining across fields by orders of magnitude.

More padding per loaf. Less wheat in the field.

This is the Papiermark. More notes printed, same underlying wheat. The issuer
had a budget constraint easier to solve by printing than by producing.

## Cache Invalidation

You may think of merit as inner virtue, deservingness, or the moral worth of the
worker. Here, I mean merit to be auditable work that needs no proxy. Credentials
are cached trust. Merit is what survives cache invalidation.

Cache invalidation used to be expensive. A hiring committee reading a CV could
not replay a contribution graph. A journal reviewer could not cheaply inspect
every cited dependency. A department could not re-audit every line behind every
publication. The system needed compressed trust because decompression cost too
much.

AI lowers the decompression cost.

This does not mean "no proxies." It means proxies become audit prompts instead
of final judgments. A GitHub star count becomes a hypothesis: do real users
depend on this, or was it a demo that went viral? A citation count becomes a
hypothesis: was the result used, criticized, copied into introductions, or
actually replicated? A benchmark score becomes a hypothesis: was the task
contaminated, overfit, or meaningful?

The proxy does not disappear. It loses its epistemic excuse.

## External Receipts

Textual fingerprints will not save the audit. Style is a wasting asset. Any
textual signal an agent can use gets optimized against in the next draft. The
new proxy becomes the next target.

What does not crack as easily is external reference.

A merged PR has a maintainer who actually reviewed it. An equation either
checks or does not. A cited statute either exists with the holding you claimed
or does not. A model either reproduces on a held-out benchmark or it does not.
The artifact has receipts held by parties the model cannot prompt: signed
commits, type checkers, package registries, issue threads, downstream users,
reviewer comments, production incidents.

A cold PR to a repo with real maintainers is the gold redemption event in this
picture. The maintainer did not ask for it, has their own taste and their own
time, and will read the diff. The repo has downstream users who bisect to your
commit when it breaks. The merge is a public, timestamped signal from someone
whose own reputation is on the line.

You cannot spin up Linus accepting your kernel patch. You cannot prompt your way
into his git log.

The provenance is held by parties who did not consent to be your reference,
which is exactly why it is worth something.

## Contribution Graphs

Credential and contribution sort onto opposite sides of a line.

- issued -> produced
- terminates at the body -> forks
- verified by committee -> verified by execution
- needs tribute -> needs use
- unfalsifiable -> either runs or it does not
- cost rising -> cost collapsing

Nobody checks whether you read those references, whether they support the
claim, whether the citation ring is mutual back-scratching. Someone bisects to
your commit when it breaks them.

That is the axis.

The credential is not "I have N merged PRs." It is "I have merged PRs to repos
whose maintainers are themselves gold-backed." Recursive, like PageRank, but
with skin in the game at every node. An agent can compute it. A hiring committee
reading a CV cannot.

This works wherever the work has an audit surface: software engineering, formal
mathematics, open research, reproducible benchmarks, public datasets,
well-specified legal claims, operational systems with logs. It works poorly
where verification is still embodied, local, tacit, or high-stakes in ways the
web cannot replay: wet-lab practice, surgery, therapy, fieldwork, much of
management.

Papiermark dynamics may apply there too, but the arbitrage window opens first
where verification has already gone digital and cheap.

## The Repricing

For the credentialed, the cost of producing a unit of
credential-denominated output has stayed flat or risen. More coauthors needed.
More references to manage. More reviewer politics, more grant overhead. The
Papiermark gets more expensive to print even as each note is worth less.

For the non-credentialed, the cost of producing actual research has collapsed by
orders of magnitude in a decade. Compute is rented by the hour. Datasets are
public. Preprint servers route around journals. LLMs collapse the cost of
literature review, code scaffolding, math checking, and formal verification.
The work, if it works, is gold the moment it executes.

The divergence is structural. For a while, hiring committees and grant panels
will still be denominated in Papiermarks while the actual production of
knowledge has already moved to gold.

That gap is the opportunity.

## The Prophecy

Meritocracy is the only virtue that survives the AI storm. Every other social
currency rides on signals the storm shreds: provenance gets faked, references
get prompted, prestige gets generated, gatekeeping gets bypassed.

What survives is the artifact a stranger can inspect with their own eyes.

Credentials die with the author. The science lives on without.

The PhD, the tenure, the h-index, the named chair. None of it forks, gets
imported, or runs after the author stops. The credential is a life estate that
reverts to nothing on death, while the contribution keeps executing. People
depend on it without knowing the author's name. Value so liquid it has stopped
tracking its origin.

As Papiermark accumulates to the person and dies with them, so does the
credentialed researcher cling to their name. As gold accumulates away from the
person and outlives them, so does the researcher release work into
infrastructure where it gets used so heavily nobody needs to credit them.

Ramanujan filled his notebooks as an autodidact in Madras, before Hardy answered
his letter. They are still being mined a century later. The Cambridge fellowship
and the FRS came in the last four years of his life; he died at thirty-two. The
Papiermark holders of 1920 are dust. The gold he minted is still circulating.

The exchange rate has not repriced yet. It will.
