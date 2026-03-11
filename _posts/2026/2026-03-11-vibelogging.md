---
layout: post
title: "Vibelogging"
tags: coding
---

A blog specifies an entire ad exchange: the [auction math](/power-diagrams-ad-auctions), the [privacy architecture](/ask-first), the [billing model](/one-shot-bidding), the [publisher UX](/publisher-ux), the [go-to-market sequence](/the-playbook). The [source code](https://github.com/kimjune01/vectorspace-adserver) is the artifact, generated from those posts with Claude Code. Prose as source. Repos as artifact.

Andrej Karpathy [coined "vibe coding"](https://x.com/kaborsky/status/1894093141153653180) in February 2025: describe what you want in natural language, let an agent produce the code. By March 2026, CNBC reporters with zero coding experience were [rebuilding Monday.com](https://www.cnbc.com/2026/02/05/how-exposed-are-software-stocks-to-ai-tools-we-tested-vibe-coding.html) in under an hour. The [Vector Space](/vector-space) series is that idea applied to technical writing. I'm calling it vibelogging, short for vibe blogging.

## Prose All the Way Down

[Skills over SDKs](/skills-over-sdks) argued that instructions are the new executable. A skill is a text file that a coding agent reads and turns into working code. The vector-space series is that idea taken to its conclusion: the blog *is* the skill. Every post is a specification document written for two audiences simultaneously. A human reads it as an argument. An agent reads it as a build instruction.

Every previous layer of abstraction invented a new language. Assembly, C, Python: each one was a notation humans learned in order to talk to machines, letting you say more with less and pushing implementation details down a level. Blog posts push the details all the way down to the agent. For the first time, the human and the machine share a language they're both native to. No translation layer, no syntax to learn, no compiler errors to decipher. You manipulate the system directly with words you dictate, not code you "write."

This is the first full layer of abstraction over code that I've witnessed.

I'll update this post the moment I find prior art. If you know of someone who published a blog series that an agent can build from end to end before this one, tell me. I want to credit them.

## Build This

Don't take my word for it. Run the experiment yourself.

1. Open Claude Code, Codex, or whatever agentic coding tool you use.
2. Point it at [june.kim/vector-space](/vector-space).
3. Say "build this."

The posts contain everything the agent needs: the scoring function, the encryption scheme, the API surface, the infrastructure layout, the UX spec. What used to require a 200-page PRD, a Figma file, and six months of engineering meetings is a blog a machine can read in seconds.

If the agent can build a working ad exchange from the blog alone, the blog is source code. If it can't, I have more writing to do.

## Specificity, Rigor, Readability

Not every blog post is a build instruction. Most aren't. The difference is specificity. A blog post about "why privacy matters in ad tech" is an opinion. A blog post that specifies [which embedding model to use, how the ciphertext passes through the server, and what HTTP status code to return when plaintext is rejected](/vectorspace-adserver) is a spec.

The vector-space posts work as source because they're written at the level of detail where a competent engineer (or agent) can implement without guessing. Every design decision is a post. Every post is a decision.

Specificity is necessary but not sufficient. The posts also have to be *right*. The [auction math](/power-diagrams-ad-auctions) works because the scoring function is derived from mechanism design literature, not because it's described clearly. The [privacy architecture](/ask-first) holds up because the threat model accounts for real adversaries, not because the prose is clean. A slopped-out blog produces even sloppier code. The agent amplifies whatever you give it: rigor in, rigor out; slop in, slop squared.

A solo builder can't be an expert in mechanism design, cryptographic attestation, and go-to-market strategy simultaneously. But a solo builder with research agents can ask "what does the literature say about VCG auctions in position settings" and get a cited, accurate answer in seconds. The same tool that turns the blog into code also turns questions into knowledge. The rigor doesn't have to come from one person's head. It has to end up in the writing.

The writing constraint is the same one that makes good engineering docs: if you can't explain the decision clearly enough for someone else to implement it, you haven't finished deciding. And if you can't defend the decision to someone who pushes back, you haven't finished thinking.

That's why this works better than a traditional spec. A PRD is written once, maintained by committee, and read by nobody. A blog post is written to be read. The act of making the argument legible to a stranger forces clarity that an internal document never demands.

Programmers already know that code should be optimized for readability over cleverness. A well-written essay is that principle at its ceiling. The same reasons you name variables clearly, extract functions, and delete dead code apply to prose: say what you mean, structure it so the next reader can follow, cut everything that doesn't serve the argument. Every post in the series went through [two quality gates](/writing-with-claude): /humanize strips AI writing tics, /arc-check verifies the argument structure. The result is prose that's readable by humans and parseable by agents. Not because I optimized for both. Because clear writing *is* both.

## Write First, Ship Second

A traditional startup writes code first, then writes about what they built. The writing is marketing.

Vibelogging inverts this. The writing is the product; the code is a side effect. The blog series took five weeks. The working codebase took a weekend (first commit to deploy). The agent just had to read and execute.

## "But Now Anyone Can Build It"

Yes. That's the point. [The Paradox of Open Competition](/the-paradox-of-open-competition) explains why publishing the spec is the strongest competitive position, not the weakest. If your moat is "they can't see the code," you're already dead: Claude can infer a working replica from a product's UI without ever reading the source. Hiding the spec protects nothing that isn't already inferrable.

Publishing it does something hiding never can. The commit timestamps prove who designed the system, in what order, and when. A competitor who forks the repo is visible as a fork. A competitor who reads the blog and rebuilds from scratch still arrives second, with receipts showing exactly how second. The blog is the chain of custody for every decision.

Vibelogging makes this automatic. The spec is public because the spec *is* the blog. Anyone with a coding agent can attempt to replicate it. The person who wrote it will always have written it first.

And if that person gets hit by a bus tomorrow, the blog still builds. The economic value doesn't depend on the author being alive to maintain a codebase. The spec survives independently of the person who wrote it.

Code rots. Prose that specifies code can be rebuilt by the next agent, on the next framework, for the next decade's infrastructure. This isn't a vision statement that has to be interpreted, discussed, and fanboyed over for decades. It compiles. An agent reads the blog, produces code, and that code compiles to a binary you can deploy. The writing is the durable artifact. The code never was.

## Try It

The entire vector-space series is at [june.kim/vector-space](/vector-space). The code is at [github.com/kimjune01/vectorspace-adserver](https://github.com/kimjune01/vectorspace-adserver). Compare what the blog says to what the code does. Or better yet, don't look at the code. Point your agent at the blog and see what comes out.

If it builds, the blog is the source. If it doesn't, I'll keep writing until it does.

Now write yours. Pick the thing you know better than anyone. Blog it at spec depth. Point your agent at it. See if it compiles. If you can build a working system from a blog you wrote, you're a vibelogger. Send it to me at [june@june.kim](mailto:june@june.kim); I want to see what compiles.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I named the concept; Claude built the argument.*
