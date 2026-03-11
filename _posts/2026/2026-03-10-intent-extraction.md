---
layout: post
title: "Intent Extraction"
tags: vector-space
---

[Buying Space, Not Keywords](/buying-space-not-keywords) explains how advertisers position themselves in embedding space. A therapist writes "Licensed therapist specializing in anxiety and stress management," embeds it, and that embedding becomes their auction position. But the user's side of the match is a chat conversation, not a position statement. Someone says "my back has been killing me after sitting all day." How does that become a point in the same space?

## The Prompt

The intent extraction prompt in `sdk-web/src/intent.ts`:

> Given a conversation, decide whether the person could benefit from a professional service. If yes, write a single sentence describing that service — as if the provider were writing their own position statement.

The key phrase is "as if the provider were writing their own position statement." The user's need gets rephrased into provider language. "My back has been killing me" becomes something like "Licensed physical therapist specializing in posture-related back pain." That sentence gets embedded with the same model (BGE-small-en-v1.5) and compared against advertiser positions using cosine similarity.

Skip this step and the match falls apart. Embed "my back has been killing me" directly and it lands in a different region of embedding space than "physical therapist specializing in posture-related back pain," even though they're about the same thing. The prompt forces both sides into the same semantic frame.

## Need, Not Identity

The prompt has explicit guardrails:

- No demographics or personal data about the user
- `"NONE"` for casual conversation, so there are no false matches
- Match the most obvious professional need. A health complaint maps to a health provider, not a lawyer.

The output is a single sentence describing a service, phrased as the provider would phrase it. That sentence gets embedded and the embedding gets encrypted. The exchange never sees the sentence itself.

## Prompt It Into Shape

The exact wording matters less than the frame. The output should follow the same structure advertisers use to position themselves: value prop + ICP + qualifier. "Sports injury knee rehab for competitive endurance athletes recovering from overuse." The closer it matches advertiser phrasing, the tighter the cosine match.

## Where It Runs

Intent extraction runs on the publisher's own LLM. The [install skill](https://github.com/kimjune01/vectorspace-adserver/blob/master/skill/install.md) makes this explicit at Checkpoint 2: "call the publisher's existing LLM with the intent extraction system prompt." Conversation text never leaves the publisher's infrastructure. Only the 384-dimensional embedding crosses the API boundary, and even that gets [encrypted](/vectorspace-adserver) before it hits the wire.

Claude, GPT, Llama, a fine-tuned model. Whatever already powers the chatbot can extract intent. The prompt is model-agnostic.

The prompt ships as a [skill, not an SDK](/skills-over-sdks). The publisher's coding agent reads the install document and writes it into their existing code. No package to import. One prompt turns a user's conversation into a point in the same space where advertisers already live.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). Part of the [Vector Space](/vector-space) series.*
