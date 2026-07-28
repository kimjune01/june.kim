---
variant: post
title: "Intent Extraction in the Wild"
tags: vector-space, methodology
---

[OpenAI's ad platform](https://help.openai.com/en/articles/20001047-ads-in-chatgpt) targets ads using conversational context, past chat history, and previous ad interactions. Call the targeting signal derived from past chats the dossier: what you've told the assistant before, brought to bear on which ad you see now. The assumption underneath is old and rarely stated: more data about the user means better targeting, so a profile must be worth building.

Chat is a medium where that assumption can be tested cheaply, because the user states their intent in the conversation itself. [Ask First](/ask-first) left the question open in February: how much of real chat traffic carries commercial intent at all, and how much does a profile add on top of what the user already said? I measured both on public data. In roughly 2,000 sampled conversations, an intent extractor produced a service-matchable description in about one in five. Among 78 users with prior conversations, attaching that history changed the extraction in 16.7% of cases; an identical rerun without history changed it in 14.1%. The 2.6-point difference is too imprecise to interpret as an effect. The dossier's measurable contribution failed to clear the instrument's own noise.

The results are directional, the sample is small, and the instrument broke four times before it produced a number I trust.

## The Extractor

The instrument is the [intent extraction](/intent-extraction) prompt that ships in the Vector Space SDK: given a conversation, produce a one-sentence provider-style position statement, or NONE. From a user troubleshooting a smoky stove, it produced "Sauna stove and chimney installation with draft diagnostics for homeowners building or troubleshooting bath heating systems"; from a casual conversation it produces NONE and no ad surface exists. The sentence is the whole interface: Vector Space matches it against position statements advertisers write about themselves. The prompt forbids demographics and personal data by construction, so whatever it extracts is the conversation-only signal.

## Corpus and Design

The corpus is [WildChat-1M](https://huggingface.co/datasets/allenai/WildChat-1M), a public release of real user conversations with ChatGPT, served row by row from a public API. Samples total about two thousand conversations; the extractor sees the first three user turns. Scripts, hashes, and per-run labels are in a [public repo](https://github.com/kimjune01/intent-sufficiency), and predictions were committed and pushed before either run launched.

I made two measurements. The first is yield: the share of conversations that produce a position sentence instead of NONE. The second is dossier redundancy: whether handing the extractor a user's history changes what it extracts, beyond how much it changes its own mind between two identical runs. The redundancy design takes 78 users (approximated by hashed IP), one randomly chosen non-first conversation each, and extracts intent from that conversation alone, then again with the user's strictly-prior conversations attached as background. Disagreement between two extractions is a binary outcome; the paired comparison uses exact [McNemar](https://en.wikipedia.org/wiki/McNemar%27s_test) on discordant pairs.

## A Fifth of Traffic

The extractor produced a service-position sentence in 20.2% of conversations (401 of 1,989 valid extractions, 95% CI 18.5 to 22.0%). The pre-registered prediction was 10 to 20%; the point estimate lands just above the band's top edge. The extractions read like inventory. IELTS coaching for band-8 test takers. Copyediting for academics writing to editorial boards. Flat-foot correction training. A German book-editing conversation extracted correctly into English.

This is prompt-specific service-matchable yield on conversation prefixes, on an opted-in corpus, behind an uncharacterized public-view filter. It is not a prevalence estimate for chat traffic overall. What it does answer, directionally, is Ask First's open worry: in the traffic I could see, service-matchable language was no rare corner case; the extractor found it in about one conversation in five.

## Under the Noise Floor

The first version of the redundancy experiment reported that history changed the extraction in 13.8% of cases, and I nearly wrote that up as the finding. Then the control arm arrived. Run the conversation-only extraction twice, with no history anywhere, and it disagrees with itself 14.1% of the time. That baseline run-to-run disagreement is the noise floor, and it is the size of the effect I was about to attribute to the dossier.

With the control in place, adding a dossier changed extracted intent 2.6 points more often than a repeat extraction without one: treatment disagreement 16.7%, control 14.1%, McNemar p = 0.774. At this sample size that difference is too imprecise to interpret as an effect. The asymmetry leans toward history surfacing intent on conversations that currently express none, 8 cases against the control's 6 at n=78.

One pair showed the dossier overriding the question: a user asking about Arabic translation whose history pulled the extraction to financial recovery planning, cosine 0.49 between the two sentences' BGE-small embeddings. That is one example of the kind of override history can produce, and it appeared once in 78 users.

## Four Broken Instruments

The numbers above survived four failed instruments, each caught by reading raw outputs before any rate escaped into a summary. It is the same discipline as [auditing a benchmark's grader](/how-to-audit-a-benchmark), pointed at my own.

A keyword screen flagged 5% of conversations as commercial, and on inspection the flags were mostly false positives: WildChat is full of essays, roleplay, and homework, so commercial words appear inside text the user is authoring rather than needs the user is expressing. A 3B local model flagged 79%, because it was doing the user's task rather than extracting, and echoing conversation text into output that would have been embedded and shipped. The prompt's privacy guardrail is not self-enforcing; at 3B it failed silently, a counterexample to "the model just needs to not be terrible" ([Marketing-Speak Is the Protocol](/marketing-speak-is-the-protocol)). A frontier model behind an agent CLI flagged 97%, because I had appended the extraction prompt to the agent's system prompt instead of replacing it, measuring the harness rather than the prompt.

The same model with a clean system prompt still hijacked on 8 of 60 conversations. The transcript arrives as the user message, so imperative text inside it competes with the extraction instruction, and in those 8 it won. I wrapped the transcript as data, explicitly marked as not-instructions. That eliminated all eight hijacks in the 60 inspected conversations, converted two into correct extractions, and is on its way back into the SDK.

## Scope

An external review (GPT-5.5, two rounds) shaped this study more than any design choice I made up front. The first round found temporal leakage, a self-contradictory prompt guard, and the missing control arm. The repo's worklog withdraws the first version's result, and an external timestamp on the pre-registration commit that preceded both runs lets anyone check what was predicted when. The second round found one more counting defect and the missing paired test, then had no further objections to what the scripts compute. The conservative wording of the result is the reviewer's.

This is a directional study on a selection-stacked corpus, with a noisy instrument, at n=78. It cannot say the dossier is worthless. It says the profile's measurable contribution to intent extraction failed to clear the instrument's own noise, on the traffic I could see, with the extractor the SDK ships. The conversation alone yielded matchable intent in a fifth of cases. Anyone claiming chat-history targeting earns its privacy cost now owes a number, because the first attempt to measure the dossier's effect on extracted intent couldn't separate it from the extractor's own instability.

If anything gets serious, the repo specifies the study that would settle it: live operator traffic, outcomes instead of text properties, blinded labels, session identity instead of hashed IPs, pinned models, and external registration. If an operator wants to run it, the door is open. Until then, the dossier lives under the noise floor.

---

*Written with Claude Fable 5 via [Claude Code](https://claude.ai/claude-code). I directed the argument and the review loop; Claude built the instruments and drafted prose. Part of the [Vector Space](/vector-space) series.*
