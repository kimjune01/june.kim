---
variant: post
title: "Copyleft Is Copyrighted"
tags: pageleft
---

<figure style="text-align:center; margin:1.5em 0;">
<img src="/assets/gnu-head.svg" alt="GNU head" style="width:120px;">
<figcaption style="font-size:0.85em; color:#666;">
<a href="https://www.gnu.org/graphics/agnuhead.html">Etienne Suvasa</a>, CC BY-SA 2.0
</figcaption>
</figure>

The GPL is copyrighted. All rights reserved. By the Free Software Foundation.

Read the [preamble](https://www.gnu.org/licenses/gpl-3.0.en.html): "Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed." That's not copyleft — it's a traditional copyright notice with a narrow distribution grant. You may copy the text but not change a word. The license that guarantees your freedom to modify code prohibits you from modifying the license.

This is defensible engineering. If anyone could edit the GPL and still call it the GPL, the term would mean nothing. License integrity requires fixity. But the mechanism that enforces it is copyright — the same legal tool the GPL exists to constrain.

## The metadata gap

I tried to index the GNU [copyleft explainer](https://www.gnu.org/licenses/copyleft.en.html) into [PageLeft](/pageleft), a search engine that only indexes copyleft-licensed pages. The API rejected it: no machine-readable license detected.

The page describes copyleft. It does not signal copyleft. No `<link rel="license">`, no CC meta tag, no RDFa, no structured data. The FSF's footer says the site content is under the [GFDL](https://en.wikipedia.org/wiki/GNU_Free_Documentation_License), but that's prose buried in HTML, invisible to any system that checks licensing programmatically.

The organization that wrote the licenses never adopted the tooling to declare them.

## Three layers

The license text is copyrighted. You can distribute it but not modify it.

The FSF controls the version numbering. Any project licensed "GPL v3 or later" is subject to whatever the FSF puts in v4. Linus Torvalds keeps Linux at "GPL v2 only" [for this reason](https://lkml.org/lkml/2006/1/25/273): "or later" is a blank check on terms he can't review in advance. Different risk tolerance, same codebase.

For GNU projects, contributors [assign copyright to the FSF](https://www.gnu.org/licenses/why-assign.en.html). The FSF owns the code outright. They could relicense it entirely. No "or later" needed. GCC [dropped this requirement in 2021](https://softwarefreedom.org/blog/2021/jun/02/gcc-statement/) and switched to a sign-off model. Emacs still requires it.

| Foundation | Model | Can relicense? |
|---|---|---|
| FSF (GNU) | Full copyright assignment | Yes — they own it |
| Apache | CLA (contributor keeps copyright) | No — license grant only |
| Linux Foundation | DCO (sign-off) | No — no legal agreement |
| Mozilla | No assignment | No |

Copyright over the text. Version authority over the ecosystem. Ownership of the code itself. None of them are copyleft; copyleft requires all of them.

## What could they do?

The FSF won't do any of this. But legally, nothing stops them.

With copyright assignment:

- *Dual-license for revenue.* Sell commercial licenses to companies that don't want GPL obligations, the way Oracle does with MySQL.
- *Go permissive.* Relicense Emacs as MIT. Every corporation closes their fork. Contributors who assigned copyright have no recourse.

With "or later":

- *Narrow "derivative work."* GPL v4 says linking against a GPL library no longer triggers copyleft. Every "or later" project becomes effectively LGPL overnight.
- *Carve out SaaS.* GPL v4 excludes network use from distribution. Cloud companies serve GPL code without sharing source. The AGPL loophole, baked into the GPL itself.

Imagine a new FSF board publishes GPL v4. Buried in section 6: a revised definition of derivative work that excludes API-level integration. A cloud provider's legal team reads v4 on a Friday, elects it for every "or later" dependency by Monday, forks the GNU toolchain behind a proprietary build system. Patches flow one way. The fork gets hardware optimizations the community branch can't match. Distro maintainers adopt it because their users need the performance. A year later, a student tries to compile a kernel on commodity hardware. The toolchain that works is the one she can't read. Nobody revoked the license. The code just aged out. And it only takes one tool in the toolchain — a compiler, a linker, libc — to drag the rest with it.

Linux survives this scenario. GPL v2 only, no copyright assignment — both levers miss it. Linux being v2 is load-bearing for the whole ecosystem. Any FSF board that tried to weaken copyleft would have to explain why Linux opted out twenty years in advance. The copyleft commons hangs on two words one person chose thirty-five years ago. Linus wrote "v2 only" and meant it. If he'd followed the FSF's recommendation and written "or later," every scenario above becomes live.

And the FSF itself? A nonprofit with a modest budget. It only takes one megacorp's legal department to make the right donation to the right board at the right time. The whole copyleft commons depends on one organization staying honest.

## The fixed point

This isn't a bug. Copyleft is a hack on copyright that uses the monopoly grant to enforce openness, but the hack only works if the license text stays under traditional copyright. If the GPL were itself copyleft, anyone could fork it into something that negates its terms. The freedom of the code requires the unfreedom of the license.

Copyleft can't be copyleft all the way down. The base case is copyright. All rights reserved.

Or is it? Nobody forks the license because forked code can't touch the GPL pool. The real fixed point is compatibility, not copyright.

---

*See also: [Licenses Are Functors](/licenses-are-functors), [CC BY-SA-NS](/cc-by-sa-ns).*
