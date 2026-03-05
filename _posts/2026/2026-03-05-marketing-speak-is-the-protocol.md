---
layout: post
title: "Marketing-Speak Is the Protocol"
tags: vector-space
image: "/assets/positioning.jpg"
---

Keywords were an artificial shared language. Neither side of the ad market naturally thinks in keywords.

Advertisers think in positioning. "We do sports injury rehab for competitive athletes." "We handle custody arrangements for divorcing parents." Every marketer writes a positioning statement: what we offer, who it's for. It's the first thing a CMO drafts and the last thing they'd give up.

Users think in problems. "My lower back has been hurting for two weeks." "I got rear-ended and the other driver's insurance won't pay." No one wakes up thinking in keyword fragments.

Keywords were the middle ground both sides had to learn. Advertisers compressed "licensed physical therapist specializing in sports injury rehabilitation for climbers" into "sports injury PT near me." Users compressed "my knee started clicking after I increased my mileage" into "knee pain running." Both sides lost most of the meaning. Google authored the shared vocabulary, and charged rent for the translation.

## Positioning Is Already a Protocol

What if advertisers just submitted their positioning statements directly? No keyword translation. The descriptions would look like this:

> "Sports injury rehab and return-to-play training for competitive athletes"
>
> "Divorce mediation and child custody negotiation for separating parents"
>
> "Startup fundraising strategy and venture capital pitch coaching for early-stage founders"
>
> "Emergency roof repair and storm damage restoration for homeowners with leaks"

Each one follows the same structure: [what we do] for [who we serve]. The same format on every marketer's website hero section and LinkedIn headline. It goes straight into the auction. No keyword mapping, no category taxonomy, no bid on a list of terms.

## The Prompt Bridges the Gap

The user side is messier. Users don't describe their needs in positioning format. They describe symptoms and frustrations. The system needs to translate.

Here's the intent extraction prompt from the publisher SDK:

> Given a conversation, describe what kind of professional service would help this person — as a single natural sentence **in the style an advertiser would use to describe their own practice**.
>
> Focus on the service, its value proposition, and who it serves.

That's the entire coordination mechanism. A conversation on an LLM chatbot:

<div style="border-left: 3px solid #6b9bd2; padding-left: 1em; margin: 1.2em 0; color: #444;">
<strong>User:</strong> my knee has been killing me on long runs lately. i'm training for a marathon in april<br>
<strong>Bot:</strong> Where does it hurt exactly?<br>
<strong>User:</strong> outside of the knee. usually hits around mile 10, especially downhill. i've been icing it but it's not getting better
</div>

The prompt rewrites this into positioning-speak:

<div style="border-left: 3px solid #d4a843; padding-left: 1em; margin: 1.2em 0; color: #444;">
"Lateral knee pain management and training modifications for a marathon runner"
</div>

That matches against an advertiser who wrote:

<div style="border-left: 3px solid #6aab73; padding-left: 1em; margin: 1.2em 0; color: #444;">
"Sports injury rehab and return-to-play training for competitive athletes"
</div>

The user never said "physical therapist." The user never said "sports injury rehab." The prompt inferred the service from the problem. And the keyword version of this query — "knee pain running" — would have lost the marathon context, the chronicity, the downhill specificity. The positioning statement preserves all of it.

## What Didn't Need to Be Invented

The advertiser submitted a positioning statement. A prompt rewrote user language into advertiser language. The [scoring function](/2026/03/04/three-levers) compared the two and picked a winner.

No new taxonomy. No category tree (IAB has 698 categories; nobody uses them correctly). No negative keyword lists to maintain. The only genuinely new concept is [σ](/2026/02/09/keywords-are-tiny-circles) — the reach parameter that controls how broadly an advertiser matches around their positioning.

Compare to the keyword setup flow: research keywords with a planning tool, organize into ad groups, write ads per keyword cluster, set match types per keyword, add negative keywords, adjust bids per keyword, review search term reports weekly. All of that overhead exists because keywords are an impoverished representation of what the advertiser actually means. When the representation is a natural-language positioning statement, most of the overhead disappears.

## Why the Prompt Matters More Than the Model

The specific model that measures similarity barely matters. What matters is that both sides speak the same language before the comparison happens.

Without the prompt, you're comparing apples to oranges. "I got rear-ended and the other driver's insurance won't pay" sounds like a complaint. "Personal injury representation for accident victims seeking compensation" sounds like a brochure. Same need, opposite ends. Problem versus solution. The match is poor even though the fit is perfect.

The prompt collapses that gap. Both sides become solution descriptions. The model just needs to not be terrible.

This is the opposite of the keyword era, where the matching algorithm was the moat. Google's keyword matching was the secret sauce: broad match, phrase match, Quality Score. Here, the matching is commodity. The coordination mechanism is the prompt. And the prompt's output format is borrowed from marketing.

## Piggybacking, Not Inventing

The last thirty years of ad tech kept inventing shared vocabularies: keywords, IAB categories, contextual segments, audience taxonomies, interest graphs. Each one required both sides to learn a new language.

Marketing-speak isn't the sharpest possible representation. A system trained on conversion data would be sharper. But it captures most of the signal keywords threw away, and nobody has to learn it. The best protocol isn't the most precise one. It's the one that's already spoken on both sides of the market.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*

*Part of the [Vector Space](/vector-space) series. june@june.kim*
