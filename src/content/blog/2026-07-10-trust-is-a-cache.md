---
variant: post-medium
title: "Trust Is a Cache"
subtitle: "Trust is a lossy code whose error-correction was local. Compartmentalization broke the locality, and cheaper verification has eaten the frontier ever since."
tags: reflecting, epistemology
keywords: trust, verification, certification, cold start, credentials, compartmentalization, division of labor, Reflections on Trusting Trust, diverse double-compiling, idempotence, stakes, reproducibility, verifiable knowledge
---

*A reflection on [Verifiable Knowledge](/verifiable-knowledge), from the side where the cache goes cold.*

A maintainer closes your pull request without reading it. The code is fine, but that was never the deciding factor. Reading it closely costs more attention than they have this month, and *unknown contributor, faint smell of generated code* is a cheap enough reason to skip the cost. You were not rejected on the merits. You never reached the merits.

Look at that reflex as a systems person and it has a familiar shape. The maintainer is a cache, and you were a miss.

## A credential is a cached check

[Verifiable Knowledge](/verifiable-knowledge) already says what a credential is: a cached pointer to a replayable check. A degree, a review stamp, a trusted-maintainer badge means *this passed checks I verified*, so deferring to it is running a package you did not compile yourself, rational under cost because a check still sits underneath. The credential caches one expensive computation, *is this worth my attention*, so nobody reruns it. A hit is trust without re-evaluation; a miss is paying full price to grade a stranger. An overwhelmed maintainer is that cache under memory pressure, where the only affordable eviction policy is *reject the miss*. Most of what reads as gatekeeping is a cache doing triage it cannot afford to skip.

The pathology has a name in that paper too: the *detached credential*, an attestation with no check under it, a dangling pointer where the evidence should sit. A credential is worth exactly the check behind it and nothing once detached. The rest of this is what that costs, and why it was fine for most of history and stopped being fine now.

## The village had the codec

Trust is lossy compression of verification, and for most of human history the codec worked, because two things bounded the loss.

The first was stakes. In a family or a village, everyone who vouched had skin in the game, so a false vouch cost the voucher: reputation, reciprocity, a place at the table. That consequence disciplined the channel, and a disciplined channel is nearly lossless per hop. The second was the savings. Verifying your cousin's work is wasteful and faintly insulting, so the fidelity you gave up by trusting was cheaper than the fidelity you would have bought by checking. Lossy, and worth it.

Push on the word *trust* and it hides a verification rather than replacing one. In the village, *nobody checks* never meant nobody checked. It meant checking was delegated to the staked local, the person closest to the work, cheapest to make check it, most punished for skipping. The stake is the receipt that the delegate actually ran the check instead of waving it through. A village vouch does not stand in for verification. It relocates verification onto whoever has skin in the game and forwards the result. That is why the loss stayed small: someone who would pay for being wrong had already paid the verification cost, once, locally.

## Compartmentalization breaks the locality

Now fragment the chain. Specialization, globalization, a value chain so compartmentalized that no one sees the whole and nobody can make a pencil alone. The count of strangers you depend on explodes, and each is opaque, sealed behind a compartment wall.

Two things break at once. The staked local disappears, because across a compartment wall the voucher is a stranger with no skin in your game, so the delegation loses its enforcement: nobody with stakes checked, and nothing tells you so. And the loss stops being bounded and can turn adversarial, because a stakeless voucher can *profit* from a false vouch. That is the whole modern bestiary in a line: the fake review, the inflated degree, the poisoned dependency, the AI slop. Each is a stakeless vouch you inherited across a wall you could not see through.

The loss does not just return, it compounds. Trust has to traverse the linkages of the chain, losing at each hop, at rates you cannot read because each rate is sealed in its compartment. So trust across an N-link chain carries loss that grows with N and, worse, is unpriceable: not a lossy estimate but an estimate with an unknown, unbounded error bar. This is why the newcomer is stuck. You are an empty cache with no staked local to vouch for you, at the far end of a chain whose every hop the maintainer already distrusts because other stakeless strangers poisoned it. Cold-start is trust's compounding loss, met the moment you have nothing cached and no stake to offer.

## Verification crosses no linkages

Verification does the one thing trust cannot: it crosses no linkages. You re-run the check locally, against the artifact, and the verdict is the artifact's own, independent of how many compartments sit between you and its origin. A failing test that now passes, committed. A benchmark's own grader run against its own gold. A proof a checker accepts. The reader trusts the artifact, not the author, and never walks the chain to do it.

That is the asymmetry, and it is a scaling law. Trust's loss compounds across the chain, so it is unbounded and unpriceable in the number of linkages. Verification is O(1) in that number, because it teleports past them to a local re-run. Lengthen the chain and one detonates while the other stays flat.

Underneath, it is the idempotence. `verify(verify) = verify` is a fixed point, which is exactly what *crosses no linkages* means: re-running recovers the origin verdict, so you regenerate it in place instead of walking back for it. `trust(trust) ≠ trust` is why trust must traverse: the origin verdict is not recoverable locally, so you chain back through every voucher and pay at each. Turtles all the way down is a crisis only for the trust stack, which needs a bottom turtle to rest on. The verify stack descends whichever turtle it doubts, re-runs it, and stops, needing no foundation because every turtle is climbable. In a poisoned cache this stops being the principled move and becomes the only move that works: slop carries no check, so slop forces the expensive trust-lookup that fails cold, while a warranted claim self-computes its own acceptance. It is the one instrument that gets an unknown trusted with an empty cache.

## Thompson already proved it

None of it is new. Ken Thompson's [Reflections on Trusting Trust](https://dl.acm.org/doi/10.1145/358198.358210) is the theorem that `trust(trust) ≠ trust`. He builds a compiler backdoored to insert a backdoor into any program it compiles, and into future versions of itself, invisibly, with no trace in any source you could read. The attack lives at the meta-level, in trusting the thing that certifies trust, and it propagates for free because the meta-level is unverifiable. The compiler is the ultimate stakeless voucher: it vouches for every binary and bears no consequence, so the loss it can inject is unbounded. His conclusion was that you cannot trust code you did not totally create yourself.

The field's answer, decades later, is David A. Wheeler's [diverse double-compiling](https://dwheeler.com/trusting-trust/): defeat the self-perpetuating backdoor by recompiling with an independent, unrelated compiler and checking the outputs converge. Independent verification, crossing no linkages. The antidote to `trust(trust)` was `verify` the whole time.

## Five centuries of the frontier moving

This is a trend, not a mood. Every trust-minimizing institution is the same event at a different price point: verification got cheaper and displaced a trust chain. Double-entry bookkeeping and the audit displaced trusting the merchant's word. The scientific method displaced *ipse dixit*, and *[nullius in verba](https://en.wikipedia.org/wiki/Nullius_in_verba)*, the Royal Society's "take no one's word for it," is a verification norm installed the moment reproducibility got cheap enough to run. Metrology and interchangeable parts displaced trusting the craftsman. Cryptographic settlement displaced trusting the clearinghouse. Reproducible builds displaced trusting the vendor's binary.

Two curves cross under all of it. Compartmentalization lengthens the chains, raising trust's compounding loss. Technology cheapens the check, lowering verification's flat cost. They have crossed domain by domain for five centuries, always in the same direction, because nothing pushes them back: chains do not spontaneously shorten, and verification does not spontaneously get dearer. AI is not a new phenomenon here. It is the steepest segment of the old curve, dropping the verification cost and lengthening the software supply chain at once, which is why the crossing feels sudden and personal.

## The move

None of this abolishes trust, and the piece would be a dunk if it tried. Verification displaces trust exactly as fast as the check becomes locally re-runnable, and no faster. Where the terminal witness cannot be cheaply re-run, the drug trial, the climate model, the empirical root that needs fresh world-contact, verification cannot teleport, so trust stays, re-anchored on stakes rather than faith. And the stake at a distance needs the very thing this argument is about: a claim that settles by replay is the only thing a stranger's bond can pay out against. So verification is how you get stakes back across a compartment wall. Trust does not vanish. It retreats to the frontier of the not-yet-cheaply-checkable, and the frontier recedes as verification cheapens.

So the move, up and down the stack, is one move. Every chain has a load-bearing linkage the whole thing is trusting on faith because verifying it is expensive and nobody has the time. Go re-run that linkage and leave the receipt. It is also how you cold-start: a warranted contribution is the one thing an overwhelmed cache can accept from a stranger, because it crosses no linkages and asks for no stake it cannot verify. The village had stakes and needed no receipts. We lost the stakes, and mint receipts to re-earn them. Show your work, make it checkable, and the empty cache stops being a wall.
