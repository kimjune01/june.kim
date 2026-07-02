---
variant: post-paper
autonumber: true
title: "What Cannot Be False Cannot Be True"
subtitle: "Truth is verifiable. The unverifiable is untrue."
tags: epistemology, cognition, methodology
keywords: epistemology, machine knowledge, agent epistemics, falsifiability, pragmatism, intuitionism, entitlement, bivalence, verifiable truth, phenomenon and noumenon
---

<!-- pdf-skip -->
*The epistemology behind [The Hypothesis Graph](/the-hypothesis-graph-semantic-memory-methodeutics), and the frame its companion paper [Verifiable Knowledge](/verifiable-knowledge) runs as a protocol.*

*[Download PDF](/assets/what-cannot-be-false-cannot-be-true.pdf) · arxiv-shape preprint, rebuilt from this source. · Archived at [doi.org/10.5281/zenodo.20754645](https://doi.org/10.5281/zenodo.20754645) (CC BY-SA-NS).*
<!-- /pdf-skip -->

## Abstract {-}

Classical epistemology defines knowledge for a human seeking certainty: justified true belief, with truth as correspondence to a world no knower can step outside to check. As a procedure it is underspecified, never saying how to inspect the justification or replay the correspondence, and an AI that now makes claims passing for knowledge inherits the gap. This paper recasts belief, knowledge, and truth as acts a knower performs and can see refuted, redrawing the trichotomy so a claim's third state is an entitlement that can be checked rather than a truth value it carries. A claim not yet tested is **untrue**, neither false nor true, and terminally so if nothing could falsify it. The world makes contact only by refutation, so truth is a claim that could have fallen and has not, graded by how much it has survived. Empirical and formal knowledge split into two disjoint graphs, one tethered to the world and graded, one sealed and decided by proof, and they never convert; the split decides where a claim like string theory belongs. Bivalence holds only after a verdict, and what cannot be false cannot be true. Dewey seated the knower inside the world, Ramsey made belief a bet, Popper demanded it risk falsehood, Dummett tied truth to verification; together, knowing becomes an act of verification through inquiry.

## Introduction {#introduction}

An AI now makes claims that pass for knowledge. It answers a question, fixes a defect, reports a number. Each time, it asserts the result confidently, sometimes hallucinating. You can see why it cannot know for certain. But how about yourself? How do you know what you know for certain?

Classical epistemology takes the knower to be a person and the prize to be certainty. Knowledge is justified true belief (the lineage from [Plato](https://plato.stanford.edu/entries/plato/) to its breakage in [Gettier 1963](https://en.wikipedia.org/wiki/Gettier_problem)): a belief that is true, and justified, where justification is a state of the believer's mind and truth is correspondence to a world the believer cannot step outside of to check. As a description of what a human cognizer is doing this has its merits and its long list of problems. As a *procedure*, it is underspecified: it never says how to inspect the justification or replay the correspondence. No knower can read off whether its belief corresponds to a world it only ever meets through its own representations, and no knower can certify the inner justification of another.

The alternative is an epistemology whose every stage is a structure a knower can construct and could see refuted. It specifies belief, knowledge, and truth as things a knower does, and redraws the trichotomy so the third state is an entitlement that can be checked rather than a truth value carried inside the claim. The boundary it draws is plain: before a claim can be called true, it must first be capable of being false. That boundary splits knowledge into two disjoint graphs, one the world can refute and one proof decides, with the not-yet-verified third state sitting across both.

The home tradition is pragmatism wed to verificationism ([C.I. Lewis](https://en.wikipedia.org/wiki/C._I._Lewis) 1929), the two dividing a claim's life in time: pragmatism faces forward into inquiry, verificationism back over what a verdict has settled. Each is the other's missing half, and here both are carried to a knower neither had in view. Neither could make the frame *run*, for want of a knower whose workings could be inspected. A human cannot expose the inner state where their justification is supposed to live; a knower whose justification is a chain of verified claims ready for inspection can. The rest of the tradition is recruited where these two leave a part unspecified, and §(related-work) names each borrowing; the point is not any one of them but that, assembled, they compose into a memory that serves as *procedure*.

## Working the phenomenon {#phenomenon}

What separates reality from experience? [Kant](https://plato.stanford.edu/entries/kant-transcendental-idealism/) drew the line. The **noumenon** is the thing in itself, the world as it is independent of any knower, which a knower can think but never hold. The **phenomenon** is the appearance, the world as a construction constitutes it for a knower who only ever meets it through representation. Every cognizer works the phenomenon. No experience or instrument reaches the noumenon: an instrument returns a representation, and the noumenon is what representation is *of*. Then how do we know what's real from our experience?

The [map and the territory](https://en.wikipedia.org/wiki/Map%E2%80%93territory_relation) (Korzybski 1933) is the familiar shorthand, but its imagery smuggles a cartographer: a surveyor standing outside both, holding them up to read the match. There is no such position. [Dewey](https://en.wikipedia.org/wiki/The_Quest_for_Certainty) saw why. The knower is not a mere spectator, it is a participant inside the world it inquires into, and inquiry is something the knower does to the world it resides in. This is the old [regress of justification](https://en.wikipedia.org/wiki/M%C3%BCnchhausen_trilemma): who maps the cartographer? The lack of resolution lies less in the mapping than in the dependence on the promise to map, the present phenomenon left waiting on a cartographer still to come. Verification meets its precondition in the past, and there the regress stops. But the cartographer model is irrefutable, untrue: a deferred map yields no knowledge now. A model of knowledge must commit to turning a phenomenon into knowledge in the present, or defer its conversion to a promised future in flux.

**Phenomenal truth** is the one a knower works: in contrast to correspondence with the unreachable, a claim that has been exposed to a test and is presently standing. Naming it phenomenal licenses the word *truth* for something less than correspondence-forever without demoting it to mere belief. It is still truth, because it is still answerable to the world; it is phenomenal truth, because the world answers only by refuting claims, never by showing its face.

When a claim is wrong, the world refutes it: the bridge falls, the program crashes, the rocket explodes, the counterexample arrives. We never see the world in itself, but a wrong claim clashes and reality says *this claim is wrong*. That clash is Peirce's Secondness; the failed claim is a phenomenal event constrained by reality. Ours is only the reduced version, one bit, replayable. Knowledge's contact with reality is the leash that ties phenomenal truth to something outside the knower, and it is what keeps the view from collapsing into either relativism or idealism. A view on which the world could not refute a claim would be idealism, truth manufactured by the knower. A view on which the knower reaches the noumenon would be naive realism, the correspondence nobody can run. Phenomenal truth is the middle that holds: made by the knower, refuted by the world.

With the boundary in place, everything that follows stays on the near side of it. *Truth* without qualification, from here on, means the phenomenal kind, the claim that could have fallen and hasn't. The world returns only to do its one job, which is to refute. And because it only ever refutes and never confirms, the truths a knower holds are ordered by how much refutation they have survived, never finished (§(truth)).

## Belief {#belief}

A knower never holds the world, only its representation. So even the surest claim is a statement of credence, and this we call belief. Belief grades into knowledge, then to truth, subjectively. So what does calling it *knowing* add? The plainest case answers.

Suppose I say that *I know my keys are in my pocket*. The word *know* here means I am confident enough to reach in without bracing for absence, and if the keys are gone I update my priors without fuss. The knowledge was belief past a threshold the whole time. Raise the stakes and the threshold rises with it: stake a life on the answer and I downgrade to *let me check*. To an actor, nothing categorical sits above the confidence. There is only confidence, varying by degree, and a line for calling it knowledge that the stakes adjust.

Putting knowledge in its own tier is what [justified true belief](https://en.wikipedia.org/wiki/Justified_true_belief) is, and its *true* is correspondence, an abstraction promised for later that no knower ever cashes, its meaning left up for interpretation and re-interpretation. The sixty years of repair after Gettier are that re-interpretation in motion: each proposed analysis patched against an invented counterexample and undone by the next, the intuitions it runs on unstable once tested empirically (Weinberg, Nichols and Stich 2001), the form itself shown to admit a fresh Gettier case for any repair (Zagzebski 1994). A verifiable claim names the test that would change it. This one names no test, and says only that some next counterexample will force a change, never how, a revision with no rule and no end. The same drift reaches a single knower: justification is a present state of mind, and a present state gets overwritten, so the very same belief about the very same unchanged fact slides out of knowledge and back as the reasons behind it turn over, its title hostage to the one part that will not hold still. A survived test does not turn over; a claim that met a trial that could have killed it stays met, and entitlement of that kind only accumulates (§(trichotomy)). A model of knowledge that nothing could refute cannot become true, and is therefore useless.

[Ramsey](https://en.wikipedia.org/wiki/Frank_Ramsey_(mathematician)) made belief operational, in contact with the world. A belief is what you would bet on, and its strength is the odds you would take. That strength is what makes it actionable, and the threshold for promoting it to knowledge is the odds at which you would act, given the stakes. Stepping onto ice judged thick enough is the same act, a bet placed on the odds rather than a thing known apart from them. This is the whole of the distinction, and it is continuous, never a jump to a different kind of thing. There is one domain where the climb does reach a top, the formal one, where a proof settles a claim against its axioms with nothing left to bet on. A type boundary keeps that formal ceiling from ever lowering onto a claim about the world (§(the-two-graphs)), so empirical belief stays graded all the way up.

Belief stays graded for any cognizer, not only a person, because all cognition runs on lossy projection ([Marr 1982](https://en.wikipedia.org/wiki/David_Marr_(neuroscientist))): retina to spike trains, characters to vectors, every modality stripping dimensions with no exit to a view that keeps them, a loss the [data processing inequality](https://en.wikipedia.org/wiki/Data_processing_inequality) makes irreversible (Cover and Thomas 2006). Plato's prisoners had the shape right; the modern update only seals off the exit. So no knower holds a world-as-such, only world-as-projected, and a claim that grades itself against ground truth bases itself on its own projection, a fiction. Reality still refutes a wrong fiction. So a knower must earn entitlement by verification.

## Knowledge {#knowledge}

Knowledge, then, is a derived predicate rather than a separate substance: belief past a stakes-dependent action threshold (Ramsey 1926), indexed to a context. The same belief is knowledge at low stakes and mere belief at high, the keys in the pocket promoted or demoted by nothing but what rides on being wrong. To call a belief knowledge is to say you will act on it, and acting on it exposes it, handing the world a chance to refute it. The pragmatists fixed truth to action for exactly this reason: a claim either works or it does not, and warranted assertion is the assertion you have earned the right to act on ([James 1907](https://en.wikipedia.org/wiki/Pragmatism_(book)); Dewey 1938).

A skeptic challenges this claim. You said knowledge is belief you act on, but I can never be *sure* the belief is right, so by your own lights I never have knowledge at all. The skeptic demands certainty. So what happens when we make certainty a prerequisite for knowledge? If I only know what I am sure of, and can never be sure of anything else, then how do I learn? How can I be sure of what to be sure of? Global skepticism spends the credit it says does not exist. So drop the demand for certainty, the [oldest pragmatist move there is](https://en.wikipedia.org/wiki/Charles_Sanders_Peirce): real doubt has a motive and a target, paper doubt has neither. You were never certain.

The precise split is between a claim about the world and a claim about your entitlement for it. Suppose I tell you that I know the exact number of atoms in the universe. Call it N. Two claims hide in the one sentence. *The number is N* is about the world. *I know* is about me. The two fail at different levels: you cannot verify the fact, and you cannot verify the inquiry. The world-claim is unverifiable, because no inquiry can reach it. Neither true nor false: untrue. Luck does not enter, because there is no entitlement either way. Checking the knowledge-claim needs no atom-counting. You demand the verification chain with a root you can verify, and there is none, so *I know N* is false. Knowing is a claim to be checked, so show me its provenance.

## Truth {#truth}

Knowledge exposes a claim to the world, and what the world cannot kill earns the name true. It is a subjective label more than an objective property: it has outlived a test that could have killed it. That exposure fixes the order: the capacity to be false comes first, the right to say true only after. The N-atoms case (§(knowledge)) ran this in miniature: luck runs no risk, so the lucky-correct number is never knowledge, while the claim to *know* it stuck its neck out. A claim that runs no risk of being wrong never reaches the question of truth at all. *Cannot be false* means just this: no test could expose it as false, so no test could establish it either. *What cannot be false cannot be true.*

A tautology cannot be false, and says nothing for it: true to its axioms, untrue of the world. Conjectures relative to established axioms can be proven wrong, and that risk grants them uberty, a rightful surprise (§(the-two-graphs)). An empirical claim can be true if it can be tested to a false verdict. Some possibility of a negative result makes the positive one useful. Both stand or fall by verification, which is why the unverifiable is untrue: the move from *cannot be false* to *cannot be true* is the one the [verificationists](https://en.wikipedia.org/wiki/Verificationism) made, [Dummett](https://en.wikipedia.org/wiki/Michael_Dummett) gave its rigorous modern form by tying truth to what can be verified and withholding bivalence from the rest, and [Popper](https://en.wikipedia.org/wiki/Falsifiability) circled without quite making.

Truth is a story of survival: a hypothesis newborn, deduced and waiting on a test it has not yet faced, untrue but already in motion; a standing result that has survived its first real trials; a fact that has survived so many the test is retired and the claim taken whole, as if nothing could kill it. The grade of a truth, and the arbitrary labels we give it, indicate only how much it has survived.

Verifying once does not crown a claim true. Its test still has to be able to fail. A test that cannot is a gauge glued to *pass*, an instrument reporting the same reading whatever the world does, not a true claim at all. This is the single-knower version of the reality leash from §(phenomenon): the world has to be able to refute it.

Subjective truth stops at a graded belief: a credence [strictly below one](https://en.wikipedia.org/wiki/Cromwell%27s_rule). However many sunsets you have logged, the next evening remains a test the claim could fail. Only tests it could have failed improve a belief, pruning it for good. That same exposure also keeps it at risk: a claim gains only by being able to lose, and one secured against loss would have nothing to gain. Watching more sunsets makes you more certain of tomorrow.

Take physics: the most closely studied empirical knowledge there is still stands only on sufferance. [Newton stood until Mercury's perihelion refuted it](https://en.wikipedia.org/wiki/Tests_of_general_relativity#Perihelion_precession_of_Mercury) and gave way to general relativity, which itself strains where it meets the quantum, a successor still pending. Each was a claim standing under wider trial than the last, none the final correspondence. If even physics holds only a graded belief, everything softer does all the more, and the objection that settled science is simply true answers itself: a retired test means a claim has survived so wide a trial that re-checking stops. It does not mean the claim reached a limit.

## Disjoint graphs {#the-two-graphs}

Unlike physics, mathematics has no empirical tests. Its truth is relative to its axioms, conditional only on self-consistency: no world-signal refutes a theorem, only a counterexample or an inconsistency does, and both of those are internal to the system. So the graded headline applies only to empirical truth, and formal truth is verifiable but detached. The detachment makes mathematics the cleanest case for the trichotomy to come. [Truth-by-construction](https://plato.stanford.edu/entries/intuitionism/) was the intuitionists' insight a century ago: a claim is neither true nor false in mathematics until it is constructed or refuted.

[String theory](https://en.wikipedia.org/wiki/String_theory) mistook math for physics. It is empirically untrue, with no world-facing test passed and no refutation either, so neither true nor false. A healthy conjecture says *I am untrue, here is the test*, and string theory's test sits past anything we can probe, out at the Planck scale. The charge its own critics press is sharper, that it is [not even falsifiable](https://en.wikipedia.org/wiki/Not_even_wrong). Its [landscape](https://en.wikipedia.org/wiki/String_theory_landscape) of possible universes, some ten-to-the-five-hundred of them, fits nearly any data, so nothing could refute it. It has no strings to reality, presented as physics. It cannot be false, so it cannot be phenomenally true, the [*not even wrong*](https://en.wikipedia.org/wiki/Not_even_wrong) that [Pauli named](https://en.wikipedia.org/wiki/Wolfgang_Pauli) and [Woit took for a title](https://en.wikipedia.org/wiki/Not_Even_Wrong), unable to earn even the dignity of being wrong. The decades-long argument reduces to a single question: can anything refute it? Yes-but-unreachable makes it a deferred open hypothesis. No makes it a detached non-hypothesis dressed as physics. The framework does not adjudicate the physics. It names the one question that decides the matter.

String theory both bears witness for *what cannot be false cannot be true* and shows the line needs a boundary under it. [Popper](https://en.wikipedia.org/wiki/Falsifiability) stops at *unscientific*; the step on to *cannot be true* makes the verificationist move he resisted as anti-realist. Scoping that step to phenomenal truth rescues it. With no failure possible, no one could ever establish entitlement. And yet the claim might still hold in fact, the universe simply stringy in a way forever beyond reach. The line denies the verifiable entitlement while leaving the fact of the matter untouched, splitting the verdict Popper and the verificationists fought over and handing each side the half it had right. Neither could state that alone.

What divides experimental from theoretical physics? Less than the names suggest. One proposes the structure, the other tests it, and both answer to the world. Mathematics does not. So the architecture that keeps physics and mathematics apart is two graphs: sets of claims, internally connected, disjoint. The empirical graph holds truth that is graded, credence below one, the world refuting, no node ever absolute. The formal graph holds truth that is decisive: where proof is available it carries no grade, entitlement complete relative to its axioms, reachable precisely because the closed graph has no external world to answer to. Where a proof or a refutation exists, the entitlement closes internally; otherwise the node stays open relative to the system, since [many statements are undecidable within it](https://en.wikipedia.org/wiki/G%C3%B6del%27s_incompleteness_theorems). Incompleteness gives the formal graph its own permanently-open region, and what is proven stays absolute. The absoluteness belongs to the standard, never to any checker: Gödel's second theorem blocks a system from certifying its own consistency, and a Bayesian checking a long proof never quite reaches credence one on having checked it.

![The two graphs as transposes, the same graph read two ways. The empirical graph (left) is tethered to the world by an experiment edge, the one place a claim meets a test that can refute it, and its nodes stay hollow because no empirical claim is ever absolute. The formal graph (right) is the identical structure sealed: no edge reaches the world, nothing outside can refute it, and its nodes fill solid, decided absolutely where proof is available. The wall between them is a boundary of type.](/assets/two-graphs-light.svg)

When the experiment edge reports a failure, it indicts the whole path from claim to test, not the claim alone: the hypothesis, an auxiliary, or the instrument could each be the culprit. Re-running the sibling edges localizes which node fell, so the graph turns a blind refutation into a placed one.

Between the two graphs lies a boundary of type: absolute truth in the platonic graph is a different kind of entitlement from anything the empirical graph can hold. *Platonic* here names the formal graph's behavior, absolute and detached, and nothing more; truth in it is relative to the chosen axioms, internal to a stipulated game, and the absoluteness is just the proof closing the gap inside it. No commitment to mathematical Platonism is being made or needed.

The two domains never convert. Empirical entitlement is bought by surviving a world-facing test; platonic entitlement is a proof closing against its axioms. So a mathematical model of the world is an empirical hypothesis, an open node still awaiting its test, and its platonic self-consistency is entitlement in the platonic graph. Consistency cannot substitute for reality, and confusing one for the other is the characteristic error, a type mismatch: formal entitlement passed off where only the empirical kind counts. That is the wall, and [Einstein put it best](https://en.wikipedia.org/wiki/Geometry_and_Experience):

> As far as the laws of mathematics refer to reality, they are not certain, and as far as they are certain, they do not refer to reality.

If the platonic graph is sealed off, why is mathematics so [unreasonably effective](https://en.wikipedia.org/wiki/The_Unreasonable_Effectiveness_of_Mathematics_in_the_Natural_Sciences) at physics? Because empirical hypotheses are modeled from formal structures, and the entitlement still comes from the test. That the world is compressible enough for any physics to work is itself an empirical fact, an open node.

Kant drew the boundary, Dewey put the knower inside the world, Einstein drew the wall between the two graphs. The parts are inherited; they assemble into the third status of being not-yet-verified.

## Trichotomy {#trichotomy}

An edge that can be refuted at any step gives a claim its verdict, and it comes back one of three ways.

| State | Test | Tells you |
|---|---|---|
| *True* | tested, stood | it holds |
| *False* | tested, failed | a definite no |
| *Untrue* | not yet tested | nothing yet |

True and false are not opposites but siblings, split only by how the test came out. Entitlement only accumulates and never inverts, so untrue is its zero, the plain absence of a verdict, while false is a verdict of its own. Why *untrue* and not *unfalse*, when the zero falls short of either verdict? Because a claim is put forward as a candidate for truth, never for falsehood; the name negates the status it reaches for. It keeps the title's line too: the unfalsifiable comes out untrue, denied the truth it reached for, not *unfalse* and thereby flattered toward it. This is bookkeeping of entitlement, and the books are not subjective: the grade of belief is internal to the knower, but a claim's verification is grounded externally. How do you know which news to trust? Decide an event's [truthiness](https://en.wikipedia.org/wiki/Truthiness) by which channel it aired on; it either happened or it didn't. The three are entitlement states: absolute bivalent truth lives in the platonic graph where proof decides (§(the-two-graphs)), the empirical graph stays graded, and the trichotomy sits across both. The [third value is a century old](https://en.wikipedia.org/wiki/Three-valued_logic), Łukasiewicz and Post; the narrow reading is to see null as not-yet-verified.

The third state has structure. In the formal graph it can be terminal; in the empirical graph it reopens, since fallibilism keeps every node revisable (§(truth)). And the wait itself comes in knowable shapes. In a decidable system it is knowably temporary, a statement of [Presburger arithmetic](https://en.wikipedia.org/wiki/Presburger_arithmetic) settled before you run anything; a [provably non-halting](https://en.wikipedia.org/wiki/Halting_problem) search is knowably forever hung; an open conjecture like [P versus NP](https://en.wikipedia.org/wiki/P_versus_NP_problem) is a wait whose own provability is itself unsettled. A kindred conjecture underwrites the digital economy: public-key cryptography rests on hardness assumptions no one has proven, acted on as knowledge only because no scalable algorithm has yet broken them. So undecidability is itself decided.

From the three states falls an ordering of dignity. Among claims *presenting as knowledge*, accountable falsehood outranks unaccountable pseudo-knowledge. A false claim stuck its neck out and reality took the swing; it narrowed the space and told you something, even if the something was no. An unverifiable claim risked nothing and told you nothing.

Asked whether the work is done, one answer is *yes* and another is *go check*. The first asks to be taken on trust; the second hands over the test and invites refutation. Epistemically the second is the stronger, the only one that could earn a verdict at all.

## Meeting reality {#meeting-reality}

Engineering is a full-contact sport: a build carries real weight and the world collects without appeal. A specification is a conjecture the world can break, and failure is the name engineering gives the refutation ([Blockley and Henderson 1980](https://doi.org/10.1680/iicep.1980.2208); [Staples 2015](https://doi.org/10.1007/s11229-014-0571-6)). The organizations that cannot afford to be wrong already mandate it: NASA's systems-engineering handbook requires every requirement to be verifiable and its acceptance test named before anything is built ([NASA Systems Engineering Handbook 2016](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf)).

Its thinkers reached the test as truth's proxy from every direction:

- [Vincenti](https://en.wikipedia.org/wiki/What_Engineers_Know_and_How_They_Know_It), from aeronautical history: engineers generate what they know by variation and selection.
- [Petroski](https://en.wikipedia.org/wiki/Henry_Petroski), from structural failure: a standing structure only fails to refute its design, while a collapse teaches what no success can.
- Koen, from the engineering method itself: every rule is a fallible heuristic, justified by nothing but the change it causes.
- [Oreskes and colleagues](https://doi.org/10.1126/science.263.5147.641), from numerical modeling: validation is impossible, the model broken by data and never confirmed by it.

Each reached from practice what Popper reached from logic.

When the standard lapses, the failure reports name the same root cause:

- [*Challenger*](https://en.wikipedia.org/wiki/Space_Shuttle_Challenger_disaster): the agency that had mandated a named test for every requirement overrode its own engineers, whose cold-weather warning was pressed until the no-launch call reversed to *go*; the booster failed the next morning as the unrun test would have shown ([Rogers Commission 1986](https://www.nasa.gov/history/rogersrep/genindex.htm); [Feynman](https://www.nasa.gov/history/rogersrep/v2appf.htm): *nature cannot be fooled*).
- [Hyatt Regency](https://en.wikipedia.org/wiki/Hyatt_Regency_walkway_collapse): a walkway connection redesigned and approved with the load never re-run ([NBS BSS 143, 1982](https://doi.org/10.6028/NBS.BSS.143)).
- [Chernobyl](https://en.wikipedia.org/wiki/Chernobyl_disaster): a reactor instability known to its designers and withheld from the operators, who trusted a machine no one had let them verify ([INSAG-7, 1992](https://www-pub.iaea.org/MTCD/Publications/PDF/Pub913e_web.pdf)).

The flag over each was different; the regime was the same, trust standing in for a test.

*What cannot be false cannot be true* is no axiom held above its own rule. Earlier verificationism foundered right here: its own principle was neither analytic nor verifiable, so meaningless by its own lights (Ayer 1936). This thesis takes that hit instead of ducking it. As a theory of knowledge it is refutable, and so can be true, and the falsifier is concrete: a field that has lived under verification reverts to trust as its standard of truth and is the better for it. Engineering trading the named test back for authority, or any verificationist discipline doing the same once it has known both, would break it. None has. The thesis is untrue until tested.

## Related work {#related-work}

[Pragmatism](https://en.wikipedia.org/wiki/Pragmatism_(book)) is the home, led by Dewey: the knower a participant in the world it inquires into, so inquiry has no external limit to approach, and truth is what survives it rather than what corresponds (Dewey 1929; James 1907). Belief is a disposition to act whose strength is the odds (Ramsey 1926); paper doubt is dropped and Secondness kept, from Peirce, whose convergence is declined as spectator residue (Misak 1991). [Kant](https://plato.stanford.edu/entries/kant-transcendental-idealism/) supplies the phenomenon/noumenon boundary, and the refuting that crosses it is Peirce's Secondness reduced to one replayable bit. What pragmatism could not finish, for want of a knower whose workings could be inspected, is make the program run: a human cannot expose the inner state where the justification is supposed to live.

[Verificationism](https://en.wikipedia.org/wiki/Verificationism) does the real work here: *cannot be false, therefore cannot be true* leans on it. [Schlick](https://en.wikipedia.org/wiki/Moritz_Schlick) stated the principle, meaning as the method of verification (1936); [Carnap](https://en.wikipedia.org/wiki/Rudolf_Carnap) softened it to testability, which is why a universal law or an open conjecture can stand graded rather than nonsense (1936-37); and the tautology that says nothing is Wittgenstein's ([*Tractatus*](https://en.wikipedia.org/wiki/Tractatus_Logico-Philosophicus) 4.461). Its sharpest modern form is [Dummett's](https://en.wikipedia.org/wiki/Michael_Dummett) anti-realism, truth tied to verification and bivalence withheld from the undecidable. *Entitlement* throughout is this lineage's: warrant earned by verification, Dewey's warranted assertibility (1938) carried to a knower that can show its work. [Wright's](https://en.wikipedia.org/wiki/Crispin_Wright) entitlement (2004) runs the other way, a warrant a cognitive project may assume without that work; here nothing is entitled until the world has had its chance to refute it.

[Popper](https://en.wikipedia.org/wiki/Falsifiability) supplies the capacity to fail as the mark of a claim that says anything, his "irrefutability is a vice" narrower than the line here, unscientific rather than untrue. Truth-by-construction and a [third status](https://en.wikipedia.org/wiki/Three-valued_logic) are a century old (Brouwer; Łukasiewicz 1920; Aristotle's sea battle first).

Everything above is inherited. Dummett drew the line between the knowable and the real, then collapsed it onto the knowable: truth became verification, the real beyond it dropped, the logic intuitionistic to match. Here the line stays open. The third value is that gap held wide, a status in the knower's ledger of entitlement, not-yet-verified and ranked below false, the indeterminacy in the knowing and not the world.

## Conclusion {#conclusion}

Bivalence rules where a verdict is laid down, the unverifiable is untrue, and what cannot be false cannot be true, across the empirical and formal domains. Truth expands by linking new knowledge to old.

We are already running on one standard or another, whether or not we ever chose it. Trust and test are the two: one asserted bona fide, the other handed over to refutation. They cannot both settle the same claim. To run on verification is to stop letting some other people decide what is true for us. The choice falls before any verdict. It is ours, and it is a commitment.

A knower works only the phenomenon, and the world makes contact only by refutation. So every truth a knower holds is a claim that could have fallen but has not yet, still standing without ever being certified, because the knower's limit is at untruth, ever expanding. It's all we can do as knowers, to act on the untrue.

We can assemble every structure in the universe on our own, but by acting we expose truth by sharing tests, verifying and refuting. So how can you be sure of what you're sure of? You have to go and check.

## References {-}

Canonical sources the argument rests on. The author's companion essays, which work out several of these moves first and informally, are listed separately under *Provenance* below as lineage, not as entitlement.

- Ayer, A. J. (1936). *Language, Truth and Logic*. Gollancz.
- Blockley, D. I., & Henderson, J. R. (1980). "Structural Failures and the Growth of Engineering Knowledge." *Proceedings of the Institution of Civil Engineers* 68 (4). [doi:10.1680/iicep.1980.2208](https://doi.org/10.1680/iicep.1980.2208)
- Carnap, R. (1936/1937). "Testability and Meaning." *Philosophy of Science* 3 (4): 419-471; 4 (1): 1-40.
- Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Wiley.
- Dewey, J. (1929). *The Quest for Certainty*. Minton, Balch & Co.
- Dewey, J. (1938). *Logic: The Theory of Inquiry*. Henry Holt & Co.
- Dummett, M. (1978). *Truth and Other Enigmas*. Harvard University Press.
- Einstein, A. (1921). "Geometry and Experience" (*Geometrie und Erfahrung*). Prussian Academy of Sciences.
- Gettier, E. (1963). "Is Justified True Belief Knowledge?" *Analysis* 23.
- Gödel, K. (1931). "On Formally Undecidable Propositions of *Principia Mathematica* and Related Systems I."
- Heyting, A. (1956). *Intuitionism: An Introduction*. North-Holland. (the constructivist program founded by L. E. J. Brouwer)
- International Nuclear Safety Advisory Group (1992). *The Chernobyl Accident: Updating of INSAG-1* (INSAG-7). IAEA Safety Series 75-INSAG-7. [www-pub.iaea.org](https://www-pub.iaea.org/MTCD/Publications/PDF/Pub913e_web.pdf)
- James, W. (1907). *Pragmatism: A New Name for Some Old Ways of Thinking*.
- Kant, I. (1781/1787). *Critique of Pure Reason*.
- Koen, B. V. (2003). *Discussion of the Method: Conducting the Engineer's Approach to Problem Solving*. Oxford University Press.
- Korzybski, A. (1933). *Science and Sanity*.
- Lewis, C. I. (1929). *Mind and the World-Order: Outline of a Theory of Knowledge*. Charles Scribner's Sons.
- Łukasiewicz, J. (1920). "On Three-Valued Logic"; and Post, E. (1921). "Introduction to a General Theory of Elementary Propositions."
- Marr, D. (1982). *Vision: A Computational Investigation into the Human Representation and Processing of Visual Information*. W. H. Freeman.
- Marshall, R. D., et al. (1982). *Investigation of the Kansas City Hyatt Regency Walkways Collapse*. NBS Building Science Series 143, National Bureau of Standards. [doi:10.6028/NBS.BSS.143](https://doi.org/10.6028/NBS.BSS.143)
- Misak, C. (1991). *Truth and the End of Inquiry: A Peircean Account of Truth*. Oxford University Press.
- NASA (2016). *NASA Systems Engineering Handbook*, NASA/SP-2016-6105 Rev2. [nasa.gov](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf)
- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences." *Science* 263 (5147): 641-646. [doi:10.1126/science.263.5147.641](https://doi.org/10.1126/science.263.5147.641)
- Peirce, C. S. (1877). "The Fixation of Belief"; and (1878) "How to Make Our Ideas Clear." *Popular Science Monthly*.
- Petroski, H. (1985). *To Engineer Is Human: The Role of Failure in Successful Design*. St. Martin's Press.
- Popper, K. (1959). *The Logic of Scientific Discovery*; and (1963) *Conjectures and Refutations*.
- Ramsey, F. P. (1926). "Truth and Probability." In *The Foundations of Mathematics* (1931).
- Rogers Commission (1986). *Report of the Presidential Commission on the Space Shuttle Challenger Accident*; incl. R. P. Feynman, Appendix F, "Personal Observations on the Reliability of the Shuttle." [nasa.gov/history/rogersrep](https://www.nasa.gov/history/rogersrep/genindex.htm)
- Schlick, M. (1936). "Meaning and Verification." *The Philosophical Review* 45 (4).
- Staples, M. (2015). "Critical Rationalism and Engineering: Methodology." *Synthese* 192 (1). [doi:10.1007/s11229-014-0571-6](https://doi.org/10.1007/s11229-014-0571-6)
- Vincenti, W. G. (1990). *What Engineers Know and How They Know It: Analytical Studies from Aeronautical History*. Johns Hopkins University Press.
- Weinberg, J. M., Nichols, S., & Stich, S. (2001). "Normativity and Epistemic Intuitions." *Philosophical Topics* 29 (1-2).
- Wittgenstein, L. (1921/1922). *Tractatus Logico-Philosophicus*. Trans. C. K. Ogden. Kegan Paul.
- Woit, P. (2006). *Not Even Wrong*. Basic Books.
- Wright, C. (2004). "Warrant for Nothing (and Foundations for Free?)." *Aristotelian Society Supplementary Volume* 78 (1): 167-212.
- Zagzebski, L. (1994). "The Inescapability of Gettier Problems." *The Philosophical Quarterly* 44 (174).

## Provenance {-}

This paper consolidates arguments first worked out informally on the author's blog. Each is reproduced here in full, so the paper stands on its own; the posts are listed as lineage, not as entitlement, so a reader can trace any move back to where it was first made and rerun it there.

- **[Belief Is the Edge of Knowing](/belief-is-the-edge-of-knowing)** (2026-04-26): no tier above belief, the stakes-indexed threshold, belief as a bet, all cognition as lossy projection, grading-yourself-grades-a-fiction, Plato's cave with the exit dropped.
- **[Truth Is Buildable](/truth-is-buildable)** (2026-06-04): truth as the build exposed to a test, the three states, the dignity ordering, and the consolidated source text.
- **[Truly Untrue?](/truly-untrue)** (2026-06-06): untrue as the hung wait, the decidability structure of the third state, undecidability-is-decided.
- **[You Cannot Ring a Semiring](/tempus-doxa-praxis)** (2026-06-12): entitlement as a semiring with a zero and no inverse, so untrue is the zero and false a verdict of its own; the sea-battle and future contingents.
- **[Evidence Has a Trajectory](/evidence-has-a-trajectory)** (2026-04-27): belief climbing and slipping by degrees.
- **[The Hypothesis Graph](/the-hypothesis-graph-semantic-memory-methodeutics)** (2026-05-28) and **[Verifiable Knowledge](/verifiable-knowledge)**: the data structure this epistemology is the node semantics for, and the protocol that runs the frame between agents.

## License {-}

© 2026 June Kim. Licensed under **CC BY-SA-NS**: the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/) plus a Network Services clause. Serving a Derivative Work over a computer network counts as distribution, so the Corresponding Source must be made available to users of the service, under this license or a Compatible License, at no charge. Full terms: [june.kim/cc-by-sa-ns](https://june.kim/cc-by-sa-ns).
