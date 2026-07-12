---
variant: post-medium
title: "Trust Is a Cache"
tags: reflecting, epistemology
keywords: trust, verification, certification, cold start, credentials, compartmentalization, division of labor, meritocracy, Reflections on Trusting Trust, diverse double-compiling, idempotence, stakes, arms verification, verifiable knowledge
---

*A reflection on [Verifiable Knowledge](/verifiable-knowledge), from the side where the cache goes cold.*

For most of human history, a village trusted its blacksmith for a ploughshare that would not crack in hard soil, and nobody tested each one before buying it. They did not need to. The smith was one of them, his maker's mark was on the work, and a tool that failed at harvest would cost him more than the sale. From smith to soil, the chain was one link.

Now we let an AI agent open a pull request while we sleep, and strangers we will never meet pour into the open source projects everything runs on. Do we trust them the way the village trusted its smith, and on what mark?

## Cached checks

[Verifiable Knowledge](/verifiable-knowledge) already says what a credential is: a cached pointer to a replayable check. A guild's mark, a degree, a review stamp, a trusted-maintainer badge means *this passed checks I verified*. Deferring to it runs a package you did not compile yourself. The credential caches one expensive computation, *is this worth my attention*, so nobody reruns it. Carry a mark it recognizes and you are trusted on sight; carry none and someone pays full price to grade you from scratch. An overwhelmed maintainer, with no budget for that, falls back on the only rule that scales: trust the marked, turn the rest away.

I have been turned away. I filed two safe programs a Rust verifier wrongly rejects, as failing tests anyone could re-run, and noted that an agent had written them. The maintainer closed it the same day as AI noise. He could not cheaply tell my receipt from the slop, so he rejected the class. What reads as gatekeeping is often a cache doing the triage it cannot afford to skip.

A credential is worth exactly the check behind it and nothing once detached. Trust stays useful as that cache. What follows is why its range keeps shrinking.

## The village codec

Trust is lossy compression of verification, and for most of human history the codec worked, because two things bounded the loss. Stakes: everyone who vouched had skin in the game, reputation, reciprocity, a place at the table, and that stake disciplined the link; a disciplined link loses almost nothing. Savings: verifying your cousin's work is wasteful and faintly insulting, so the fidelity you gave up by trusting was cheaper than the fidelity checking would have bought. In the village, *nobody checks* never meant nobody checked; it meant checking was delegated to the staked local, the person closest to the work and most punished for skipping. Trust was lossy, and worth it.

## Broken locality

Now fragment the chain. Specialization and globalization compartmentalize the value chain until nobody can [make a pencil alone](https://en.wikipedia.org/wiki/I,_Pencil), and the strangers you depend on multiply, each sealed behind a compartment wall. Across that wall the staked local disappears: the voucher is a stranger with no skin in your game, so nobody with stakes checked, and nothing tells you so. Trust stops being merely lossy; the loss can turn adversarial, because a stakeless voucher can *profit* from a false vouch. And it compounds: trust loses at every link, at rates sealed inside the compartments, so loss across an N-link chain grows with N and, worse, is unpriceable, an estimate with an unknown, unbounded error bar.

## How caches break

The failure modes that break a cache are the ones that break trust, one for one.

- *Poisoned entry.* An adversary writes a false value and readers keep hitting it. The [XZ Utils backdoor](https://en.wikipedia.org/wiki/XZ_Utils_backdoor) was a poisoned write years in the making: "Jia Tan" spent two years earning a maintainer's mark with patient, helpful commits, then spent the mark to slip a backdoor into a library that sits under `sshd`. Every distribution downstream read the entry and pulled it; [one engineer](https://en.wikipedia.org/wiki/Andres_Freund) noticed half a second of latency while it was still in beta releases, and that accident is all that stopped it.
- *Stale entry.* The value was right when written and the world moved. Trust ships with no TTL and no invalidation protocol, so a credential outlives its check silently. The FAA's entry for Boeing was written across decades of sound airframes, and certification authority was progressively [delegated to the manufacturer](https://en.wikipedia.org/wiki/Boeing_737_MAX_groundings); nobody re-ran the check as the incentives underneath it changed, and 346 people were dead before the entry got flushed.
- *Dangling pointer.* The *detached credential*, as [Verifiable Knowledge](/verifiable-knowledge) names it: the mark survives, the evidence is gone, and dereferencing it returns whatever now squats at the old address. When [DigiNotar](https://en.wikipedia.org/wiki/DigiNotar) was breached, its certificates kept validating in every browser for weeks, and what squatted at the address was Iranian state surveillance wearing Gmail's padlock.
- *Cold miss.* The newcomer with no entry. Nothing false, nothing stale, just absent, and the full verification price due on first contact. [Ramanujan](https://en.wikipedia.org/wiki/Srinivasa_Ramanujan) mailed his theorems to two Cambridge mathematicians and got nothing back; the third, Hardy, paid the price the cache exists to avoid, re-ran the mathematics, and the miss everyone dropped held a genius.
- *Write flood.* Cheap generation swamps the cache with unauthenticated entries, and the overwhelmed cache turns read-only: trust the marked, turn the rest away. [Clarkesworld](https://en.wikipedia.org/wiki/Clarkesworld_Magazine), a magazine famous for reading every submission, closed submissions in 2023 under a flood of machine-generated stories; the editors could no longer afford to check, so nobody got checked.

And the modes compound. The newcomer is an empty cache with no staked local to vouch for him, at the far end of a chain whose every hop the maintainer already distrusts because other stakeless strangers poisoned it. The first four are old. The flood is new, and it is why the cache is failing everywhere at once.

## No linkages

Verification does the one thing trust cannot: it crosses no linkages. You re-run the check locally, against the artifact, and the verdict is the artifact's own, independent of how many compartments sit between you and its origin. A patch that turns a failing test green. A benchmark's own grader run against its own gold. A proof a checker accepts. The reader trusts the artifact and never walks the chain to do it.

That is the asymmetry. Verification's cost does not grow with the number of linkages, because it teleports past every one to a local re-run, while trust compounds its loss across them. Lengthen the chain and the gap only widens.

<svg viewBox="0 0 720 300" role="img" aria-label="Two rows over the same five nodes, origin on the left and you on the right. Top row, trust: a linked list where an arrow passes from the origin through three intermediaries to you, and each hop and node fades more than the last, so the origin reaches you faint. Bottom row, verify: every node has its own solid arrow reaching straight back to the origin, one hop regardless of distance, nothing faded." xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;max-width:720px;display:block;margin:1.9rem auto;font-family:inherit;color:inherit">
  <defs>
    <marker id="tc-arrow" markerWidth="9" markerHeight="9" refX="6.5" refY="3" orient="auto">
      <path d="M0,0 L7,3 L0,6 Z" fill="currentColor"/>
    </marker>
  </defs>
  <text x="24" y="84" fill="currentColor" font-size="14" font-style="italic" opacity="0.9">trust</text>
  <text x="24" y="214" fill="currentColor" font-size="14" font-style="italic" opacity="0.9">verify</text>
  <g opacity="0.85"><line x1="144" y1="80" x2="226" y2="80" stroke="currentColor" stroke-width="1.6" marker-end="url(#tc-arrow)"/></g>
  <g opacity="0.55"><line x1="274" y1="80" x2="356" y2="80" stroke="currentColor" stroke-width="1.6" marker-end="url(#tc-arrow)"/></g>
  <g opacity="0.32"><line x1="404" y1="80" x2="486" y2="80" stroke="currentColor" stroke-width="1.6" marker-end="url(#tc-arrow)"/></g>
  <g opacity="0.18"><line x1="534" y1="80" x2="621" y2="80" stroke="currentColor" stroke-width="1.6" marker-end="url(#tc-arrow)"/></g>
  <rect x="96" y="65" width="48" height="30" rx="8" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.6"/>
  <rect x="226" y="65" width="48" height="30" rx="8" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
  <rect x="356" y="65" width="48" height="30" rx="8" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.4"/>
  <rect x="486" y="65" width="48" height="30" rx="8" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.28"/>
  <rect x="621" y="65" width="48" height="30" rx="8" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <text x="120" y="55" fill="currentColor" font-size="13" text-anchor="middle">origin</text>
  <text x="645" y="55" fill="currentColor" font-size="13" text-anchor="middle" opacity="0.45">you</text>
  <text x="382" y="120" fill="currentColor" font-size="12.5" font-style="italic" text-anchor="middle" opacity="0.6">loss compounds at every link</text>
  <path d="M226,210 Q185,244 144,210" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.55" marker-end="url(#tc-arrow)"/>
  <path d="M356,210 Q250,252 144,210" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.55" marker-end="url(#tc-arrow)"/>
  <path d="M486,210 Q315,260 144,210" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.55" marker-end="url(#tc-arrow)"/>
  <path d="M621,210 Q382,270 144,210" fill="none" stroke="currentColor" stroke-width="2.1" marker-end="url(#tc-arrow)"/>
  <rect x="96" y="195" width="48" height="30" rx="8" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.6"/>
  <rect x="226" y="195" width="48" height="30" rx="8" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <rect x="356" y="195" width="48" height="30" rx="8" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <rect x="486" y="195" width="48" height="30" rx="8" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <rect x="621" y="195" width="48" height="30" rx="8" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <text x="120" y="188" fill="currentColor" font-size="13" text-anchor="middle">origin</text>
  <text x="645" y="188" fill="currentColor" font-size="13" text-anchor="middle">you</text>
  <text x="382" y="292" fill="currentColor" font-size="12.5" font-style="italic" text-anchor="middle" opacity="0.6">one hop to the origin, however far</text>
</svg>

Underneath, it is the idempotence. `verify(verify) = verify`: with the artifact, procedure, environment, and terminal witnesses pinned, re-running recovers the same verdict instead of adding another layer of belief. That is what *crosses no linkages* means. `trust(trust) ≠ trust` has no such fixed point, because trusting a voucher adds a dependence on that voucher's judgment. The origin verdict is not recoverable locally, so you chain back through every hop, paying at each. Turtles all the way down is a crisis only for the trust stack, which needs a bottom turtle to rest on. The verify stack descends whichever turtle it doubts, re-runs it, and stops.

## Trusting trust

None of it is new. Ken Thompson's [Reflections on Trusting Trust](https://dl.acm.org/doi/10.1145/358198.358210) is the classic case of `trust(trust) ≠ trust`. He builds a compiler backdoored to insert a backdoor into any program it compiles, and into future versions of itself, with no trace in any source you could read. The attack lives at the meta-level, in trusting the thing that certifies trust, and it propagates for free because the meta-level is unverifiable. He concluded you cannot trust code you did not totally create yourself.

The field's answer, decades later, is David A. Wheeler's [diverse double-compiling](https://dwheeler.com/trusting-trust/): defeat the self-perpetuating backdoor by compiling the source through an independent compiler, recompiling through the result, and checking that the suspect binary reappears bit for bit. Independent verification, crossing no linkages. The antidote to `trust(trust)` was `verify` the whole time.

## Five centuries

Every trust-minimizing institution is the same event at a different price point: verification got cheaper and displaced a trust chain. Double-entry bookkeeping and the audit displaced trusting the merchant's word. The scientific method displaced *ipse dixit*. The Royal Society's *[nullius in verba](https://en.wikipedia.org/wiki/Nullius_in_verba)*, "take no one's word for it," made experimental verification the rule and the eminent name no longer the proof. Metrology and interchangeable parts displaced trusting the craftsman. Reproducible builds displaced trusting the vendor's binary. Each cheaper check did the same social thing underneath: it widened the set of people who could transact or contest a verdict without first entering the incumbent's trust network.

The same reflex runs through the professions. Each verifies wherever it is affordable: the accountant's audit, the engineer's load check, the doctor's second opinion, the lawyer's discovery. And the frontier keeps dropping. A DoorDash driver now photographs the order at your door, a receipt that displaced trusting the driver's word the day a camera got cheap enough to carry.

Two curves cross under all of it. Compartmentalization lengthens the chains, so trust loses more. Technology cheapens the check, so verification costs less. They have crossed, domain by domain, for centuries, and the pressure runs one way, because chains do not reliably shorten and checks do not reliably get dearer. AI is the steepest segment of the old curve, dropping the verification cost and lengthening the software supply chain at once, which is why the crossing feels sudden.

## Deleting the author

Run the crossing forward and it stops being about one village smith. When acceptance travels with the artifact instead of the author, the admission rule of every institution changes, and the changes stack.

First, entitlement attaches to the work, not the name. The test of a meritocracy is whether deleting the author changes the verdict: if it passes the same checks with no name attached, its standing came from the work; if revealing the name admits or rejects it, reputation is still the source. Checks grade the artifact; credentials grade the person. The [Quebec Bridge](https://en.wikipedia.org/wiki/Quebec_Bridge) fell in 1907 because Theodore Cooper was too eminent to overrule. He had lengthened the span, the dead load ran past what the design carried, and when a site engineer flagged the buckling chords the call waited on Cooper's word. 75 men died where trusting his name stood in for re-running his numbers. The mark graded the smith; a share that bends under load grades the steel, and it cannot tell whether a man or a machine forged it.

It is not hypothetical. An anonymous poster's lower bound on [superpermutations](https://en.wikipedia.org/wiki/Superpermutation) was verified, formalized, and published with "Anonymous 4chan Poster" credited as the author. A financial network that has moved trillions of dollars was founded by [someone whose identity is still unknown](https://en.wikipedia.org/wiki/Satoshi_Nakamoto), because anyone can validate the blocks without trusting him. Zero credential, zero identity, full admission.

The objection is that a check can be captured too. Whoever writes the benchmark can define merit to flatter the incumbent, and whoever owns the oracle reinstalls the gatekeeper one level down. That is real, and it is why the check itself has to stay a claim under verification: inspectable, its scope explicit, its roots independently challengeable, and cheap enough that a rival can run a competing check and expose what it omits. A check only the incumbent can afford is replayable in syntax and gatekept in practice. Entitlement by check buys nothing unless the check is contestable.

Grant that, and strangers who share no trust can still build on each other, because they agree on a method. What one establishes and any other can re-check is kept once and built on, a canon with no owner, every entry revocable by a failed replay. Compartmentalization stops forcing distrust: you no longer have to be inside someone's network to inherit their work, only able to re-run it. Nation, tribe, and the wall between human and machine were partly trust boundaries, drawn where trust could not cross. A check does not care which side of the wall authored it.

The hardest case is where the chain's two ends actively distrust each other. Two sides that share no trust chain can still settle a dispute, because the verdict is the check's and not either side's word. That is not utopian. "[Trust but verify](https://en.wikipedia.org/wiki/Trust,_but_verify)" was Reagan quoting a Russian proverb back at Gorbachev, and the [INF treaty](https://en.wikipedia.org/wiki/Intermediate-Range_Nuclear_Forces_Treaty) held for thirty years between two blocs that trusted nothing, because on-site inspection, portal monitoring, and satellite surveillance made *we destroyed the missiles* re-runnable by the adversary. Verification crossed the one wall trust never could, the wall between enemies. It settles nothing overnight, and nothing about values or power; it removes one fuel from conflicts of fact and compliance, the need to decide whose word rules. Peace here is not universal agreement. It is the territory on which disagreement can settle without submission, and cheaper verification keeps enlarging it.

## The move

Trust stays wherever it is the cheapest codec that still delivers: the fast path where you cannot re-run every hop live, and the empirical roots no one can re-run at all, the drug trial, the climate model, the terminal witness that needs fresh world-contact. There it holds, re-anchored on stakes. What changes is its range. Verification displaces trust exactly as fast as the check becomes locally re-runnable, so the frontier of the not-yet-cheaply-checkable recedes year over year.

So the move, up and down the stack, is one move. Every chain has one linkage the whole thing trusts on faith because verifying it is expensive and nobody has the time. Go re-run that linkage and leave the receipt. It is how a stranger gets past a cold cache, how a lab gets past a rival lab, and how a bloc gets past an enemy bloc, because a replayable check is the one oracle that needs no shared side. Show your work, make it checkable, and the wall the empty cache put up comes down.
