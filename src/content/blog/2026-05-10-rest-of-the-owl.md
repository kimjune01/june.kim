---
variant: post
title: "The Rest of the Owl"
tags: pageleft, methodology
---

*Part of the [cognition](/cognition) series. Sequel to [Vibelogging](/vibelogging).*

A [pipeline](/sweep-and-triage) reads GitHub issues, investigates them, implements fixes, and submits pull requests. The code passes CI. The maintainer reviews the diff, not the contributor. It merges.

Who authored the fix?

## The tool

The pipeline is a tool. It doesn't claim authorship any more than Photoshop claims authorship of a photograph. The photographer composed the shot. Photoshop adjusted the levels. The pipeline read the issue, investigated the codebase, chose a hypothesis, killed the alternatives, wrote the fix, and committed. Mechanically.

[Vibelogging](/vibelogging) established that prose compiles to code. A blog post specifies an auction mechanism. A coding agent reads the post and produces a working implementation. The prose is the source. The repo is the artifact. Nobody disputes that the author of the prose authored the system.

But a GitHub issue isn't a blog post. Some issues are spec-grade: the maintainer describes the expected behavior, the failure mode, the acceptance criteria, the approach. Others are two sentences: "it crashes when I click save." The authorship question has different answers depending on which one the pipeline read.

## The landscape

The [US Copyright Office](https://www.copyright.gov/ai/) reaffirmed in 2025 that human authorship is required for copyright. The [Supreme Court denied cert](https://www.carltonfields.com/insights/publications/2026/ai-makes-securing-copyright-protection-for-software-code-tricky-bloomberg-law) in March 2026 on AI authorship. [Techdirt](https://www.techdirt.com/2026/04/03/can-agentic-ai-coding-tools-finally-end-copyright-for-software-while-re-inventing-open-source/) argues that AI-generated code has no copyright at all. [Vorys](https://www.vorys.com/publication-vibe-coding-the-diminishing-role-of-copyright-in-ai-generated-software) warns that vibe coding "hollows out" open source by producing uncopyrightable code that leaks value from GPL-licensed projects.

Everyone is asking the wrong question. "Who authored the code?" assumes the code is the work. But the code is a compiler output. The work is upstream.

In July 2026 Judge Martínez-Olguín [approved](https://publishers.org/news/aap-welcomes-courts-final-settlement-approval-in-bartz-v-anthropic/) the $1.5B settlement in *Bartz v. Anthropic*, $3,000 per work across some 500,000 books. Alsup's [summary judgment order](https://fingfx.thomsonreuters.com/gfx/legaldocs/jnvwbgqlzpw/ANTHROPIC%20fair%20use.pdf) had already split the conduct three ways. Training the models on copyrighted text was fair use, "exceedingly transformative." Buying print books, scanning them, and destroying the originals was fair use too, a format shift that added no copies to the world. Downloading seven million books from pirate sites and keeping them in a permanent library was a third use, held open for whatever might prove useful later, and Alsup refused to excuse it as part of the training it fed. He denied Anthropic summary judgment there and set it for trial. The settlement arrived first. No infringing output was ever alleged. That decomposition is the move this post wants one layer up.

[Marc Brooker](https://brooker.co.za/blog/2026/04/09/waterfall-vs-spec.html) wrote in April 2026 that specs now "stay in sync with implementation by being upstream." [Thoughtworks](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices) called 2025 the pivot year when specs became "active drivers of implementation." An [FSE 2025 industry paper](https://conf.researchr.org/details/fse-2025/fse-2025-industry-papers/13/Natural-Language-Outlines-for-Code-Literate-Programming-in-the-LLM-Era) demonstrated bidirectional sync: change the prose, the LLM updates the code; change the code, the LLM updates the prose. Knuth's [literate programming](https://byteiota.com/literate-programming-ai-agents-solve-maintenance/) from 1984, vindicated by the thing that killed its maintenance burden.

The right question is: who authored the spec?

## Prompts are speech. Specs are expression.

A prompt — "make me a website" — is a desire. An idea. Uncopyrightable under [*Feist*](https://supreme.justia.com/cases/federal/us/499/340/). No selection, no arrangement, no creative judgment. It's speech: transient, unrecorded, gone when the session ends.

A spec — "the auction uses power-diagram scoring, privacy is TEE-attested, billing is one-shot, the publisher UX shows a single toggle" — is expression. Nobody was forced to combine those elements. The selection is creative. The arrangement is original. It's a published work with a commit history, a license, and a URL that resolves.

The mechanical distinction is whether it's on the record. A prompt lives in a chat window. A vibelog lives at a URL. A GitHub issue with acceptance criteria lives in a public tracker with timestamps. One is a log. The other is a publication.

## The gradient

"It crashes when I click save" is a problem report. Two circles on a page. No creative expression.

"The crash occurs because `handleSave` doesn't guard against concurrent writes. Use a mutex on the file handle, not a retry loop, because retries compound under load. Acceptance: `test_concurrent_save.py` passes with 100 parallel writers." That's a spec. That's the owl.

The difference between two circles and the owl is the specification that it should be an owl. The rest of the drawing is mechanical.

Most issues fall somewhere in between. The authorship gradient is the creative distance between the problem description and the solution space. If the issue fully constrains the implementation — one hypothesis, confirmed immediately, the fix falls out mechanically — then the issue is the expression. The pipeline is the tool. The issue writer is the author.

If the issue is vague and the pipeline runs a deep investigation — fan-out hypotheses, three killed, one split, the surviving fix emerged from two iterations — then the creative work happened in the investigation. The [hypothesis graph](/the-hypothesis-graph) documents every decision: which hypotheses to test, which to kill, which approach survives, which perturbation generated the next question. That's expression. The methodology is the authored work.

The hypothesis graph is the provenance record. It measures exactly how much creative judgment bridged the gap between problem and solution. A court doesn't have to understand the code. It reads the graph. Did the solution require creative choices beyond what the problem description dictated?

Shallow graph: the issue was the spec. Deep graph: the investigation was the spec. The depth is the answer.

## The word

Perspective drawing was creative in the Renaissance. It's a technique now — first semester, art school. Compilers were creative acts in the 1950s. They're infrastructure now. The hypothesis graph — perturb, classify, follow the edge, kill what doesn't survive — is creative judgment today.

Give it a generation. It'll be a checkbox in an IDE.

Every expression eventually becomes a tool. The boundary between creative work and mechanical execution isn't fixed. It moves with the tools. "Creative" has always meant "the part the tools can't do yet." Not a property of the work. A property of the gap.

When the gap was between idea and code, programmers were creative. When the gap closed (prose compiles, agents implement), the creative work moved to specification: what to build, what constraints to impose, what to reject. When that gap closes too — when agents can read a vague problem report and produce spec-grade investigations autonomously — the creative work moves again. To whatever sits above specification that we don't have a name for yet.

The word will follow the gap. It always has. We will re-derive "creative" the way every generation re-derives it: by discovering what the new tools can't do, and calling that the thing that matters.

The owl was always the hard part. We just keep learning that the owl was higher up than we thought.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*
