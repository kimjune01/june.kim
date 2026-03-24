---
layout: post
title: "CC BY-SA-NS"
tags: pageleft methodology
---

Creative Commons has six licenses. None of them have a network clause.

AGPL solved this for code. If you run AGPL software as a service, users who interact with it over a network can request the source. The "network use is distribution" clause closes the SaaS loophole that GPL left open.

Prose has no equivalent. CC BY-SA requires derivatives to stay open, but "distribution" means giving someone a copy. Running a derivative as a service isn't giving anyone a copy. A company can read CC BY-SA prose, compile it to code, serve the code as a SaaS product, and argue they never distributed the derivative.

## The compilation chain

A blog post describes an auction mechanism. A coding agent reads the post and produces a working implementation. The implementation is a derivative work of the post. The post was published CC BY-SA. The code inherits the obligation.

But what if the company never publishes the code? They run it internally. Users interact with the service over HTTP. The derivative exists, but it was never distributed. CC BY-SA's share-alike clause never triggers.

This is the same loophole AGPL closed for code in 2007. The only difference is that the source is prose, not code.

## The license

CC BY-SA-NS is CC BY-SA 4.0 with one additional condition:

> This work is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/), with the following additional condition:
>
> **Network Services.** If you use a Derivative Work to provide a service over a computer network, you must make the Corresponding Source of the Derivative Work available to users of the service, under the terms of this license or a Compatible License, at no charge.

Two definitions:

**Corresponding Source** means the complete source material from which the Derivative Work can be regenerated: the original prose, any modifications to it, and any build instructions (prompts, configuration, scripts) used in the compilation.

**Compatible License** means CC BY-SA 4.0, AGPL 3.0, or any later version of either.

That's it. One paragraph on top of 4,000 words of existing legal text.

## What this does

A researcher publishes a paper explanation under CC BY-SA-NS. A company's coding agent reads it and builds an internal tool. If the tool stays internal, nothing changes. If the tool is served to users over a network, those users can request the source: the original prose, plus whatever the company modified.

The prose is the source. The code is the compiled output. The service is the distribution trigger. Same structure as AGPL, different medium.

## What this does not do

It does not cover model training. If an LLM is trained on CC BY-SA-NS text, the weights are not a derivative work under current copyright doctrine. This license does not attempt to change that. The question of whether training produces a derivative is unsettled law. This license sidesteps it entirely.

It covers the compilation chain: prose → code → service. Not the training chain: prose → weights → inference.

## Why not just use AGPL for the code?

You can. If the code derived from the prose is published under AGPL, the network clause already applies. CC BY-SA-NS is for the case where the prose author wants the network clause to propagate through the compilation chain without relying on the code author to choose AGPL.

CC BY-SA says: derivatives must stay CC BY-SA. But CC BY-SA has no network clause, so a derivative served as a SaaS product has no sharing obligation. CC BY-SA-NS says: derivatives must stay CC BY-SA-NS, and serving a derivative over a network triggers the sharing obligation.

The obligation flows from the prose license, not from the code license. The prose author controls it.

## Status

This is a draft. It is not a real license. It has not been reviewed by a lawyer. It has not been endorsed by Creative Commons or the Free Software Foundation.

The question it asks: can four words — "network use is distribution" — close the SaaS loophole for prose the same way AGPL closed it for code?

If the answer is yes, this becomes the missing piece in the copyleft stack. If the answer is no, the reasons why will be more instructive than the draft itself.

Comments, objections, and legal analysis welcome.

---

*Draft. Not legal advice. Published CC BY-SA 4.0 because irony would be worse.*
