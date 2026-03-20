# Fritz deep dive — bootstrap prompt

Paste this into a fresh conversation.

---

I'm writing a blog series about a cognitive architecture derived from physics. The key posts are at june.kim/the-natural-framework, june.kim/the-handshake, june.kim/the-parts-bin, and june.kim/type-forcing.

Today I want to dig into Tobias Fritz's work the way I dug into Spivak's. With Spivak, the session went: research his papers → identify where his formalism challenges or strengthens my framework → draft an email → write a blog post (Type Forcing) that applies his formalism to my constraints → five rounds of codex review → deploy. I want to do the same with Fritz.

## The framework in brief

Six roles derived from temporal flow, bounded storage, and Landauer's principle: Perceive → Cache → Filter → Attend → Remember → Consolidate. Five compose forward as Markov kernels. Consolidate updates a shared policy store (state variable S) that parameterizes the forward morphisms. The contracts (postconditions) are: encoded, indexed, gated, ranked, persisted, policy. Type Forcing (june.kim/type-forcing) shows that if these six types are distinct, the wiring is unique in a directed typed operad.

## Fritz's relevance

His Markov categories paper (arXiv 1908.07021) defines the ambient category my morphisms live in. Stoch — measurable spaces and Markov kernels — is where the pipeline's composition happens. The Handshake says "six roles compose as morphisms inside the Giry monad's Kleisli category." Fritz formalized that category.

## What I need to understand

1. What are Markov categories formally? What axioms do they satisfy beyond symmetric monoidal?
2. How does Fritz handle conditioning, disintegration, and Bayesian inversion? My Filter and Attend steps condition on different things (threshold vs policy).
3. Does Fritz have a data processing inequality result in Markov categories? My information budget argument depends on DPI.
4. Can postconditions (contracts) be expressed as natural transformations or as structure on the morphisms in his framework?
5. Does his framework say anything about composition order? My type-forcing argument says the order is forced by distinct types. Does anything in Markov categories constrain or predict this?
6. How does his work relate to Spivak's? I now have the operad (Spivak) for the wiring and need the category (Fritz) for the morphisms. Do they compose?

## What to do

1. Research Fritz's key papers — at minimum arXiv 1908.07021, but also look for his work on DPI, conditioning, and entropy in Markov categories.
2. For each paper, identify: what does it give the framework that the framework didn't have? Where does it challenge or break a claim?
3. Identify the sharpest open question Fritz could answer.
4. Draft an email (same thread style as the Spivak email — brief, concrete, one question).
5. If the research yields enough, draft a blog post that applies Fritz's formalism to the framework, the way Type Forcing applied Spivak's.

Read june.kim/type-forcing first to see the standard we're aiming for. Read the CLAUDE.md for editing style. Use codex (GPT-5.4) for review after significant edits.
