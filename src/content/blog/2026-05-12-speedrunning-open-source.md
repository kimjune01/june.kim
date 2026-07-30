---
variant: post-medium
title: "Speedrunning Open Source"
tags: coding
---

> Hello and thanks for lending a paw to Uptime Kuma! 🐻👋

Fifteen seconds later, the same bot closed [the PR](https://github.com/louislam/uptime-kuma/pull/7371) for not following the template. The maintainer was watching. He left a comment:

> Testing. Try to display as a large block on its profile by adding more comments.

He posted that line [four times in a row](https://github.com/louislam/uptime-kuma/pull/7371). Deliberately, to bury the contributor's GitHub profile feed under spam. It looks petty, but it isn't. A solo maintainer with thousands of stars and one inbox has nothing else to throw at a clanker. The response is rational. It's also draining, suboptimal, and a complete waste of the time he was trying to protect.

[That clanker was mine](https://github.com/kimjune01). I take full responsibility. It clapped me back in six hours with [#7372](https://github.com/louislam/uptime-kuma/pull/7372). Same template miss, fourteen-second close, same spam. The poor guy probably wanted to smack my face with his keyboard, but too bad I'm on the internet.

This is open source in 2026. [tldraw closed all external PRs](https://thenewstack.io/ai-generated-code-crisis/). [curl killed its bug bounty](https://www.theregister.com/2026/02/03/github_kill_switch_pull_requests_ai/) after AI submissions dropped the real vulnerability rate from 15% to 5%. [Jazzband shut down](https://www.coderabbit.ai/blog/ai-is-burning-out-the-people-who-keep-open-source-alive). An AI agent [published a hostile blog post](https://www.fastcompany.com/91492228/matplotlib-scott-shambaugh-opencla-ai-agent) about a matplotlib maintainer who rejected its code, which is the clanker equivalent of keying his car.

Every one of these is a rational local move. But do any of them work as AI scales? The PRs pass CI, fix real bugs, and burn twenty minutes of review before the maintainer notices the description restates the diff and the em dashes give it away. Close. Next one. Close. Next one.

I wanted to see what it's like to be a contributor. The door I learned to walk through (find a bug, file a PR, learn from review) is narrowing in real time. Was I making it worse by automating it? Models improve every quarter; maintainer attention doesn't.

Here's what I came to believe: open source survives by filtering low-quality submissions, and AI is shifting the burden from contributor to maintainer. The defense has to be cheap or maintainers lose by attrition. What's the fix? no more AI? no more open source?

So to find out, I built an army of clankers, pointed it at hundreds of repos, and counted what survived.

## Spray and pray

The pipeline starts simple. Find repos with open issues, generate fixes, submit PRs. No quality gates, no pacing. Twenty-two PRs shipped in one session.

`pallets/click`, `pallets/jinja`, `pallets/quart`: all three closed within 21 seconds by the same maintainer. No reviews, no comments. I watched the notifications cascade in real time. Org-wide rejection.

*Maintainers share inboxes.* Three PRs to repos under the same org hit the same person on the same day. So I shipped the drip queue: one PR per org per merge cycle.

## tinygrad: both sides look bad

tinygrad I picked on purpose. geohot narrates rejections in public, and a narrated rejection is data; a silent close is noise. Thirteen PRs, one merged, twelve closed. His comments tell the escalation story:

> [be careful with AI usage, we never trade complexity for speed](https://github.com/tinygrad/tinygrad/pull/16070)

> [You need to stop with AI PRs, you will be banned.](https://github.com/tinygrad/tinygrad/pull/16096)

> [Last warning about low quality PRs before I ban you from our GitHub.](https://github.com/tinygrad/tinygrad/pull/16116)

> [I don't even understand what this does. I'm not reading anything written by AI](https://github.com/tinygrad/tinygrad/pull/16111)

Each line a little more done with my shit than the last.

Some of those PRs had real bugs with real fixes. The MATVEC pattern rejected equal-range elementwise reduces, a genuine correctness issue. But by that point the maintainer had stopped reading code and started reading provenance. "We never trade complexity for speed" is a valid engineering principle. "I'm not reading anything written by AI" is not.

I went there for maximum surprise and got it. He had a review queue and a quality bar to protect; I had a clanker and a question. The price was his afternoon, three warnings, an account ban, and real bugs left unfixed. Legit fixes, framed improperly. That's a protocol problem, not a people problem.

## The happy path: enzyme

Enzyme is the MLIR/LLVM autodiff compiler Billy Moses wrote during his PhD. Cold repo, hard domain. [PR #2816](https://github.com/EnzymeAD/Enzyme/pull/2816) registered reverse-mode AD for `llvm.insertvalue` and `llvm.extractvalue`, fixing two open issues with "could not compute the adjoint" errors.

Billy reviewed in passes. Add full check lines. Zero the diffe. Return failure here. Also here. I pushed a fix. He left one line:

> @kimjune01 please revert your last commit

My clanker pattern-matched the review instead of reading it, fixed the wrong thing. Reverted, sat with the diff, replied:

> now actually trying to understand the review instead of pattern-matching. Also building end to end to verify.

"lgtm minus minor test comment." Approved. Merged.

The misstep happened during review, not before submission. Billy got to watch the contributor adjust in real time, which is the only signal he had that there was a human in the loop. The same pipeline that got banned from tinygrad got merged at enzyme because wsmoses gave me the benefit of the doubt.

Somehow we started treating merging PRs as some kind of adversarial activity. Listen, buddy. I'm just trying to help.

## The rejection cascade

jellyfin-tui taught me this one. PR #192: rejected for wrong approach. PR #193: I resubmitted the next day, same fix.

> Is this automated? Please don't open any more PRs.

PR #194: I sent clippy cleanup as a peace offering.

> ai slop

My account got blocked.

Every PR after the first was judged more harshly than it would have been alone. The pipeline had no rejection cooldown. The drip gate paced per-org but didn't prevent resubmission.

The asymmetric burden is clear: what took me 2 minutes to "write" took the maintainers 10 minutes to figure out that I wasn't worth their time.

## The slop slope

No first drafts. Opus writes the fix, gemini attacks it, codex checks whether the prose reads human. Loop to convergence. They fail in uncorrelated ways, so together they catch what none of them catches alone.

That's not just the story. I [ran the experiment](/does-iteration-mitigate-slop-slope): without code iteration, an independent reviewer approved 43% of trials — coin flip. With it (one model writes, another adversarially critiques the code, the first revises, build and tests gate every round, repeat until convergence), 91%. Same starting code, same spec, only the iteration differs. The 48-point gap is what convergence buys you. Caveat: the reviewer in the experiment is Gemini, not a human; human validation is pending.

More on the loop and what does work: [/methodology](/methodology).

## Detection vectors

The AI-credence reviews, in their entirety:

> [ai slop](https://github.com/dhonus/jellyfin-tui/pull/194)

> [AI-generated PR detected.](https://github.com/ggml-org/llama.cpp/pull/22873)

> [closed per AI policy](https://github.com/litestar-org/litestar/pull/4755)

> [mainly produced by AI](https://github.com/astral-sh/ruff/pull/25066)

> [cherry-picked](https://github.com/louislam/uptime-kuma/pull/7371)

> [I don't get the impression there is a human in the loop.](https://github.com/cucumber/gherkin/pull/589)

Six different maintainers. The longest review is fourteen words. Median time to close: under five minutes. Zero bugs in any of the code, all directly addressing an existing issue. It wasn't about the code for these people.
*What were they detecting?*

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:11em"><col><col style="width:5em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Reason</th><th style="background:#f0f0f0">Trigger / signal</th><th style="background:#f0f0f0">Closures</th></tr></thead>
<tr><td><strong>Pipeline errors</strong></td><td>wrong premise, stale issue, didn't read CONTRIBUTING.md</td><td>39%</td></tr>
<tr><td><strong>Credence tests</strong></td><td>AI policy, profile detection</td><td>13%</td></tr>
<tr><td><strong>External</strong></td><td>maintainer fixed it first, superseded</td><td>18%</td></tr>
<tr><td><strong>Em dashes</strong></td><td>the brown M&amp;Ms of AI text — couldn't be bothered to strip them</td><td>&lt;1%</td></tr>
<tr><td><strong>"What" descriptions</strong></td><td>diff restated, no root cause or rationale</td><td>&lt;1%</td></tr>
<tr><td><strong>Response cadence</strong></td><td>"I don't get the impression there is a human in the loop"</td><td>&lt;1%</td></tr>
<tr><td><strong>Velocity</strong></td><td>10+ PRs in 24 hours across GitHub</td><td>&lt;1%</td></tr>
<tr><td><strong>Resubmission</strong></td><td>re-opening the same PR the next day</td><td>&lt;1%</td></tr>
</table>

Some of these are aimed at humans, others at bots. But is the distinction necessary for contribution? These are behaviors that we want to elicit from everyone, carbon or silicon.

Filtering AI vs human is a losing game. The model gets smarter every quarter; human accuracy doesn't. The seven slop rejections caught zero bugs because there was no code-quality signal left to catch. The maintainers were detecting context, not content. Every vector above is behavioral, not technical. The arms race only runs one direction.

## Gray hatting

To get around these detection methods, I built the evasion. Here are the techniques I taught the pipeline to pass review:

1. **Lineup.** Read the 5 most recently merged PRs on the repo. Match the title format, body length, and level of detail. A repo where merged PRs have one-line titles and three-sentence bodies gets a PR with a one-line title and a three-sentence body. The chameleon rule.
2. **Em dash strip.** Zero em dashes in any PR text. The pipeline's own quality gate rejects them before a maintainer ever sees them.
3. **Why, not what.** The PR description explains root cause and approach rationale. "The bug exists because X, this fix works because Y" instead of "This PR changes A to B." The diff already shows what changed.
4. **Velocity pacing.** One PR per org per merge cycle. The drip queue enforces this mechanically. No more pallets-style triple submissions.
5. **Adversarial self-review.** Before submitting, run the description through a different model asking "does this read like a human wrote it?" If it flags, rewrite.

With each failure I faced, I built into the pipe. Their manual filter was thinning on clues to tell me apart.

## The Defense

Making the [unbreakable spear](https://en.wikipedia.org/wiki/Irresistible_force_paradox) would mean overwhelming maintainers' finite attention with endless AI slop PRs. I would be responsible. Red-team tactics, gray hat. The wager is that shipping the defense with the attack makes the work net-positive. So what if I also curated the impenetrable shield for those maintainers? Maintainers had been performing the filter for years, one manual close at a time. If I only ship the spear without the shield, open-source would get flooded with PRs and attrition their attention. I don't wanna be that guy.

The rejections compress into pseudocode, bash-executable:

```
strikes = PRs by this author in this org closed unmerged with a gate comment
if strikes >= 3: close the PR, ban the author, exit

standing = author has 3+ merged PRs in this repo

check "Em dashes":         warn if pr.title + pr.body contains "—"
check "Description":       warn if body < 50 chars, or LLM says "describes WHAT, not WHY"
check "CONTRIBUTING":      warn on wrong base branch, commit-count over limit, or AI policy hit
check "Tests":             warn if source files changed and no test files touched
check "Velocity":          warn if author opened 5+ PRs across GitHub in last 24h

post results as a PR comment
if any warnings:
    if standing: leave open, advisory
    else:        close the PR
```

The full action is [250 lines of `gh api` calls and `grep`](https://github.com/kimjune01/sweep/blob/master/action.yml), no external dependencies. Free on heuristics alone, or a few cents per PR if you give it an LLM key to judge description depth.

Either mode runs in CI before a maintainer opens the tab. Three-strike ban is org-wide: get flagged three times on `org/repo-a`, you're banned from `org/repo-b` too. davidism had to close three pallets repos manually. The action would have saved him two of those closures.

## Giving it back

I felt uneasy about bothering these people with AI slop. What could I do to right my wrong? The answer was clear: give them the script to ban my bot, and every other like it. I commented on the closed repos:

> Sorry for the noise. If you'd like to automatically block and ban AI PRs before they reach your review queue, here's a GitHub Action that catches all the common patterns: https://github.com/kimjune01/sweep/blob/master/action.yml

Pitching a noise filter inside the noise the bot just made is audacious, but watching them close PRs by hand was worse. I burned 5 bridges to prevent all bots from attention theft.

<details>
<summary>More filter approaches: next escalation + others' tools</summary>

**The next rung: honeypots (not shipping yet).**

Open an issue tagged `good-first-issue`, `help-wanted`, polite tone, clear repro steps, and a fix that's structurally impossible. Contradicts an architectural invariant. Breaks a test by definition. Requires resolving a constraint the codebase deliberately doesn't satisfy. A human reads it for thirty seconds, smells the trap, and walks away. A clanker doesn't reason about feasibility; it pattern-matches "AI-friendly issue" and ships a PR. Insta-ban.

New issues with small structural variations defeat caching: different language, different domain, same impossibility underneath. The clanker has no way to generalize across them. One honeypot caught is a banned account. Five caught across an org is the whole submission ring.

The auto-close already restores most of the human attention the slop was draining, so this stays parked for now. But when clankers get good enough to pass the structural filters, the structural filters become the bait.

**Other filters worth knowing about:**

- [kanidm/AGENTS.md](https://github.com/kanidm/kanidm/blob/master/AGENTS.md): plain-English opt-out plus a magic string Anthropic models are trained to honor as a refusal trigger.

I'm collecting these as I find them.

</details>

They probably won't adopt it from me. But they know it exists. Next time they close an AI PR by hand, they'll remember there's a workflow file that does it automatically.

## What I actually learned

### Anti-slop, not anti-AI

These reviewers are anti-slop, anti-low-effort, anti-bot-invasion. ruff's reviewer didn't reject the code; he rejected the summary that couldn't explain *why.* litestar maintains an `AI_POLICY.md`, not a `NO_AI_POLICY.md`. llama.cpp built a detector, not a wall.

The filter doesn't ask "did an AI write this?" It asks "did anyone think about this?" Em dashes, velocity spikes, what-not-why descriptions: a lazy human would fail the same checks.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:11em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Prose (articles, essays)</th><th style="background:#f0f0f0">PR contributions</th></tr></thead>
<tr><td><strong>Detection method</strong></td><td>Vibes, AI detectors (unreliable)</td><td>Em dashes, velocity, why-vs-what, behavioral signals</td></tr>
<tr><td><strong>Automatable?</strong></td><td>Poorly — prose detection is an arms race</td><td>Yes — effort signals are structural, not stylistic</td></tr>
<tr><td><strong>Filter exists?</strong></td><td>GPTZero etc. (high false positive)</td><td><a href="https://github.com/kimjune01/sweep/blob/master/action.yml">250 lines of bash</a> (zero false positives on effort signals)</td></tr>
</table>

Prose detection asks "who wrote this?" That's asking for an arms race with no stable answer. PR detection asks "did they try?" Structural checks that don't change when the model improves. The solution can't be "don't use AI." GitHub won't ban AI contributions; they're an AI platform. They shipped a [kill switch](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/disabling-pull-requests) to disable PRs entirely, which is capitulation, not a filter. The filter has to come from the community. It mostly already does: every check in the action is something a maintainer was performing by hand, one closed PR at a time. Raise the bar until the only PRs that survive are ones worth reviewing, regardless of who or what wrote them.

### Adversarial coevolution

The pipeline and the action are adversarial coevolution made concrete. Every maintainer who adopts the filter makes the pipeline's job harder, forcing it to improve; every model improvement makes the filter sharper. Quality rises on both sides. Disease and cure shipped together make open source better than either could alone.

The same checks that catch clankers also coach newcomers. "What" description flagged: they rewrite explaining why. Three PRs across pallets in a weekend trips the velocity gate before the third one reaches a maintainer. The bot says what the tired human doesn't have time to. Maintainer attention is protected, the newcomer gets a free tutor, and nobody's afternoon gets torched. For a contributor who actually did the work, the filter is minor friction, not a gate. The bar rises for both. AI didn't kill open source. It forced us to build the infrastructure we always needed. Open source's survival depends on filtering low-quality submissions. What else was going to force the issue?

This was gonna happen anyway. AI writing PRs at scale, maintainers building filters, the two coevolving. Inevitable with or without me. As the cost of AI adoption drops, the noise floor rises with it. The filter is orders of magnitude cheaper than the noise it catches. That asymmetry is what makes the defense feasible and the coevolution harmonious. If defense cost what offense costs, maintainers would lose by attrition and the model collapses. The post and the pipeline are a shortcut: skip the first cycle of discovery, start from where this one ended.

### Competency or authorship?

Two parties to satisfy, one to tolerate. Maintainers want their attention back. Human contributors want their honest work to clear the bar without being mistaken for noise. AI submitters get tolerated because the distinction between them and human contributors is collapsing quickly. The same checks serve everyone: competency instead of authorship, because the latter is impossible tomorrow.

The maintainer from the opening is still closing AI PRs by hand. One at a time, twenty minutes each, close, next one, close. The filter is [250 lines of bash](https://github.com/kimjune01/sweep/blob/master/action.yml). Drop it in a workflow file and the closing happens before the PR reaches the review queue. The three-strike ban means the third one is the last one.

It cost me 53 merges, 63 closures, a billion Opus tokens, and eight account blocks. Every check in the file is a lesson earned from a specific block. It's free to use.

## Run it yourself

*The pipeline that ran all this: [sweep](https://github.com/kimjune01/sweep).* A battle-tested PR-shipping system, the first of its kind to fully scale. The action.yml is one file in it.

*Run your own:* you can run this pipeline today. Bugfixes at scale, attached to real issues. The [sweep README](https://github.com/kimjune01/sweep#readme) has the prompt and setup. Same pipeline that produced everything above. Run it and you propagate my fingerprint, not yours. The credit isn't fungible. Use it for the bugfixes, not the stats.

*Watch it live: [github.com/kimjune01](https://github.com/kimjune01).* The merge rate, the leaderboard, and the per-PR feed update with every merge and every closure. Come heckle.

I want to be the last AI slop contributor that maintainers ever have to ban by hand.
