The spec for what the user sees. [Ask First](/ask-first) makes the design argument. [spec.md](https://github.com/kimjune01/vectorspace-skills/blob/main/spec.md) has the config values and API contract. This post is the implementable UX spec: tight where certain, loose where the developer decides. All code belongs to the publisher. Use their existing patterns.

## Principles

Three rules for advertising inside a conversation: respect the user's attention, match the context, touch as little as possible. Every design decision below follows from these.

## The Glow

The user is chatting with a health chatbot. They mention their back has been hurting. A faint glow appears on the chatbot's avatar with a tooltip like "We found something relevant. Tap to see more." They tap it. A dialog asks if they'd like to see a recommendation from a sponsor. They say yes. A physical therapist's offer appears.

The glow is the entire ad surface. No banner, no interstitial, no injected message. Just a visual change on a UI element the user already looks at, tappable when they're curious, invisible when they're not.

Under the hood, it's a state machine. Visual style is the developer's choice (glowing dot, avatar ring, subtle shimmer, or something custom). Five states, same logic regardless of style.

### States

**Off.** First message. Nothing happens. Intent extraction runs in the background. No data leaves the publisher's server until the user taps and consents.

**Semiglow.** The chatbot returns a message. Intent extraction finds a match against an advertiser above tau. A faint glow appears. On the first occurrence ever, pair it with a one-line tooltip (default: "We found something relevant. Tap to see more."). After that, just the glow.

**Full glow.** The same advertiser matches on consecutive turns. The glow becomes obvious but not obnoxious. Two consecutive matches is the threshold. Intensity tracks repetition, not distance.

**Semiglow (different advertiser).** A different advertiser matches. The glow drops back to faint. The consecutive-match counter resets.

**Off (intent gone).** [Intent extraction](/intent-extraction) returns `NONE`. The conversation moved away from any commercial need. The glow disappears.

### Transitions

```
Off ──[match]──→ Semiglow
Semiglow ──[same advertiser]──→ Full glow
Semiglow ──[NONE]──→ Off
Full glow ──[same advertiser]──→ Full glow (stays)
Full glow ──[different advertiser]──→ Semiglow
Full glow ──[NONE]──→ Off
```

Both semiglow and full glow are tappable.

## Tap → Consent → Recommendation

**First tap ever:** Show a consent dialog. Suggested wording:

> "Would you like to see a recommendation from our sponsor?"
>
> **[Yes, show me]**  **[No thanks]**  **[Learn more]**

Adapt to match the chatbot's voice.

**Learn more** replaces the dialog content with two guarantees: (1) nothing about the conversation has left this server yet, and (2) the chatbot's answers are not affected by the recommendation engine. The LLM generating responses has no knowledge of sponsors or ads. The recommendation system is a [separate layer](/ask-first) that only activates on tap.

A back button returns to the Yes/No dialog. How this looks is up to the developer.

**No:** Dismiss the dialog. The glow disappears and stays off. The developer configures whether and when it reappears (default: next day).

**Yes:** Store permission as a boolean and a timestamp in whatever persistent local storage the publisher already has. That's the whole consent record. The [MyTerms](https://myterms.io) principle: users control their own consent, and it should be inspectable.

```json
{
  "consent_given": true,
  "consent_timestamp": "2026-03-08T14:30:00Z"
}
```

**After consent:** Cast the current intent into embedding space via [intent extraction](/intent-extraction), send the embedding to the exchange, fetch the winning advertiser's offer, render it as a recommendation card. The card floats over the chat as a dialog: title and subtext, tappable to click through. No image for MVP.

**Subsequent taps** skip the consent dialog. Permission is already stored.

## After the Recommendation

Clickthrough fires impression and click events per the [Publisher API](/publisher-api).

Both dismiss and clickthrough trigger a cooldown for that advertiser (default: 1 hour, developer-configurable). The difference is the event: impression-only vs. impression + click. During cooldown, that specific advertiser won't trigger glow even if intent matches. Other advertisers still can.

## Opt-Out

How users disable the recommendation engine entirely is an implementation detail: a settings toggle, long-press menu, whatever fits the app's existing patterns.

## The Contract

The spec pins down the state machine and the consent record. Visual style, cooldown duration, and opt-out mechanism belong to the developer. The user controls when the glow warms up, and whether it ever does.
