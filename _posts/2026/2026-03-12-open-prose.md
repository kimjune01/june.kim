---
layout: post
title: "Open Prose"
tags: cognition pageleft
image: "/assets/open-prose.jpg"
---

![A spiral of handwritten pages curling inward toward a bright core, like an accretion disk of prose against deep space](/assets/open-prose.jpg)

*Part of the [cognition](/cognition) and [pageleft](/pageleft) series.*

The cognition series built the intake: [perceive](/caret-recorder), [structure](/moments), [filter](/perception-pipe), [attend](/salience). The pageleft series built the release: [index by meaning](/pageleft-manifesto), [license irrevocably](/free-as-in-fire), [compile to code](/vibelogging). Connect them and writing becomes a one-way valve. Attention goes in. Canon comes out. Every pass adds mass.

Open prose is writing precise enough for a coding agent to compile, licensed so anyone can fork it, and reviewable by machine. The rest of this post is the argument for each property.

## Prose is reviewable

[Slop detection](/slop-detection) tested whether a SOTA model could distinguish human-written prose from generated text by structure alone. It scored on argument dependency chains, falsifiable claim density, specificity ratio, and interchangeability. The experiment went 30/31 before an adversary trained against the rubric pushed the classifier below confidence.

If prose is reviewable, it gets the same workflow as code: draft, review, revise, merge. A [humanizer](/writing-with-claude) strips generation artifacts. An arc checker verifies structure. A slop detector catches fingerprints. Three automated passes before a human reads the first word.

## Prose is source code

If prose passes structural review, it can be trusted as build input. [Vibelogging](/vibelogging) showed that blog posts are build instructions. The vector-space series compiled to a [working ad exchange](https://github.com/kimjune01/vectorspace-adserver): auction math, privacy architecture, billing model, publisher UX. [Canon](/canon) argues the legal case: each step from prose to plan to spec to code to binary is a derivative without creative human intervention.

Prose is the densest interpretable medium. Code rots. Papers sit behind paywalls. Model weights are opaque. Point the next decade's coding agent at these posts and the code rebuilds. The spec outlasts every artifact it produces.

## The bottleneck moves

The cognition series solved transcription: the cost of going from noticing something to writing about it. [Caret Recorder](/caret-recorder) captures what's on screen and [Moments](/moments) structures it into semantic units. [Perception Pipe](/perception-pipe) runs competitive inhibition so winners suppress losers. [Salience](/salience) caches what survives.

With transcription solved, the bottleneck moves upstream from code to perception. Whoever turns lived attention into clean prose fastest will [mint the raw material](/canon) that future systems compile from. The pipeline alone is a diary. Connected to [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/) and indexed by [PageLeft](/pageleft-manifesto), it's the printing press. Private cognition becomes public leverage.

## A third category

Academia writes papers that get cited but not built. A paper nobody implements can still be a successful paper.

Open source starts with code. The README explains what it does. The writing serves the artifact.

Open prose starts with ideas. The writing *is* the artifact. Readable by a stranger, compilable by a machine, reviewable by a model, licensed so anyone can build on it. Papers inform. Code executes. Open prose does both. That's what we're proprosing.

Not all prose compiles. Some writing is just for fun, or for thinking out loud, or for persuading someone of something. That's fine. Open prose is the subset that's precise enough to serve as build input. The rest is still writing. It just doesn't compound the same way.

## Who owns it

Copyleft requires copyright. Copyright requires human authorship. If a cognition pipeline generates prose and a human only approves or rejects the output, who is the author?

The U.S. Copyright Office [addressed this in January 2025](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf). Their position: prompts alone don't provide sufficient human control. Selection of a single output is not itself a creative act. Wholly AI-generated works get no copyright protection.

Take that literally and a growing share of AI-assisted code has questionable copyright status. Every Copilot autocomplete, every Claude Code session, every Cursor tab-complete. The software industry ships AI-assisted code, claims ownership, licenses it, sells it. Nobody treats that code as uncopyrightable. Industry practice does not settle the law, but it shows the current rule is unstable in application. No court has resolved the gap.

The same legal framework applies to prose and code. The human's involvement in directing prose — choosing the topic, sequencing the argument, rejecting alternatives, rewriting passages, making editorial choices the model wouldn't make on its own — is the same kind of control a developer exercises when directing code. The Copyright Office's test is whether the human "determined sufficient expressive elements." [*Zarya of the Dawn*](https://www.copyright.gov/docs/zarya-of-the-dawn.pdf) drew the line: human-written text and human selection/arrangement were protected. The AI-generated images were not.

For this post: I chose the topic. I directed the argument. I iterated with Claude on specific sentences. I made editorial choices the model wouldn't have made on its own. That likely clears the bar, though the boundary is still unsettled.

But there's a harder question. The more the cognition pipeline automates, the thinner the human contribution looks. If the pipeline eventually generates publishable prose from raw attention with no human editing, does the copyright claim weaken?

Consider photography. [*Burrow-Giles v. Sarony*](https://www.law.cornell.edu/supremecourt/text/111/53) settled authorship for photographs in 1884. The photographer's creative choices — subject, angle, lighting, timing — are the authorship. The camera is mechanical. But a modern digital camera does enormous computational work between capture and storage: sensor conversion, demosaicing, auto-exposure, white balance, HDR compositing, computational bokeh. The photographer never determines a single pixel. They click one button. The output is copyrightable because the photographer directed the composition, not because they controlled the rendering.

Now compare: operating a laptop with a cognition pipeline involves thousands of deliberate inputs. Typing search queries. Clicking specific links. Scrolling past content, stopping at other content. Navigating to specific sites. Highlighting text. Every keystroke and click is a compositional choice that shapes what [Caret Recorder](/caret-recorder) captures. The recorder is the camera. The human's inputs are the composition.

The objection is that a camera renders the photographer's choices faithfully, while the pipeline generates new prose the human didn't write. The camera is a renderer. The pipeline is a transformer. Current doctrine draws the line there: the Copyright Office asks who determined the wording, syntax, structure, and phrasing, not who determined the inputs.

But that line is already blurring. A camera with portrait mode hallucinates bokeh. Night mode composites dozens of exposures into a scene no human eye saw. Computational photography is transformation, not rendering. Nobody argues that makes iPhone photos uncopyrightable. The distinction between "faithful renderer" and "creative transformer" is a spectrum, and the pipeline sits on the same spectrum as the camera. The law just hasn't caught up.

Vibe coding and the cognition pipeline should face the same authorship test: whether the human determined sufficient expressive elements in the final work. A vibe coder types prompts, reviews suggestions, accepts or rejects, iterates, edits. A cognition pipeline operator types searches, clicks links, highlights text, reviews drafts, accepts or rejects, iterates, edits. The activities are structurally equivalent. The same human-authorship standard applies to both, regardless of whether the output is code or prose.

If a court ever rules that operating a cognition pipeline doesn't constitute authorship, that ruling would apply equally to vibe coding. The precedent can't distinguish between them without inventing a new test that treats prose and code differently — which the Copyright Act doesn't do. Vibe coding would have to fail first.

The honest position: under current doctrine, the human needs to shape expression at the level of the output, not just the input. Directing the argument and editing sentences clears that bar today. A fully automated pipeline probably doesn't yet. But the doctrine was written for a world where cameras were mechanical and writing was manual. That world is already gone. The question is when the law notices.

Either way, the work stays open. If copyright attaches, CC BY-SA enforces copyleft and derivatives must stay open. If copyright doesn't attach, the output is not protected by copyright and free to copy and reuse by default. Lack of authorship is not a threat to openness. It only changes the mechanism. Viva copyleft.

## Gravity

Cognition produces prose. Prose [compiles to code](/vibelogging). [Copyleft](/free-as-in-fire) keeps it open. [PageLeft](/pageleft-manifesto) makes it findable. Someone else discovers it, builds on it, publishes the derivative under the same license. The derivative enters [Canon](/canon).

Canon compounds while closed work decays in isolation. Attention becomes Canon, and Canon becomes gravity.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*
