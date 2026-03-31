---
layout: post
title: "market-position.json"
tags: vector-space
description: "v0.1.0"
---

[`robots.txt`](https://datatracker.ietf.org/doc/html/rfc9309) told crawlers what to index. [`ads.txt`](https://iabtechlab.com/ads-txt/) told exchanges who could sell inventory. `market-position.json` tells exchanges what the advertiser sells and who they serve.

The file has been mentioned in passing since [Transparency Is Irreversible](/transparency-is-irreversible): *"The spec writes itself: `example.com/market-position.json`."* This post is the spec.

## The Spec

A climbing physical therapist in Brooklyn who specializes in sports injury rehab:

```json
{
  "version": "0.1.0",
  "positions": [
    {
      "positioning": "Sports injury rehab and return-to-play training for competitive athletes who need to keep training through recovery",
      "sigma": 0.15,
      "geocoordinates": {
        "lat": 40.6782,
        "lng": -73.9442
      }
    }
  ]
}
```

| Field | Type | Required | What it does |
|---|---|---|---|
| `version` | string | yes | Spec version. [Semver](https://semver.org/). Determines the embedding model. `0.1.0` uses [bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5). |
| `positions` | array | yes | One or more declared positions. |
| `positioning` | string | yes | Natural-language [positioning statement](/marketing-speak-is-the-protocol). |
| `embedding` | float[] | no | Pre-computed vector. If omitted, exchange embeds `positioning`. Model is determined by `version`. |
| `sigma` | float | no | Reach parameter. If omitted, estimated or [auto-tuned](/set-it-and-forget-it). |
| `geocoordinates` | object | no | Geographic position. See next section. |
| `geocoordinates.lat` | float | conditional | Latitude. Required if `geocoordinates` present. |
| `geocoordinates.lng` | float | conditional | Longitude. Required if `geocoordinates` present. |

**Not in the file:** bid, budget, pacing. These are between the advertiser and the exchange. The JSON is public. Anyone can curl it. Bid reveals margin. Budget reveals scale. Private channel only.

`positioning` is required even when `embedding` is provided. [The public map](/transparency-is-irreversible) needs to be human-readable.

The minimum viable declaration is just `positioning`. Everything else is derived.

## Geocoordinates

Optional but structured. National brands omit them. Local businesses include them.

Geographic filtering is the publisher's decision. The publisher already knows the user's approximate location (IP geolocation, explicit sharing). If an advertiser declares geocoordinates, the publisher filters locally, only entering that advertiser into the [auction](/power-diagrams-ad-auctions) when the user is within range. User location never leaves the publisher. The exchange never sees it.

Examples:

- **Nike**: no `geocoordinates`. National brand, irrelevant where the user is.
- **Climbing PT in Brooklyn**: `geocoordinates` with lat/lng. Publisher filters by proximity.
- **Telehealth therapist**: no `geocoordinates`. Serves anyone with an internet connection.
- **McDonald's**: one domain, thousands of `positions`, each with its own `geocoordinates`. The publisher filters to the nearest locations. A franchise with 30 locations declares 30 positions in one file.

A business with multiple positions posts a [bond](/bondage-and-tenure) per position. The bond scales with the number of territories claimed, preventing a single entity from blanketing the space cheaply.

## Resolution

The file lives at a well-known URL, the same pattern as `robots.txt` and `ads.txt`:

| | `robots.txt` | `ads.txt` | `market-position.json` |
|---|---|---|---|
| **Who publishes** | Site owner | Publisher | Advertiser |
| **Who consumes** | Crawlers | Buy-side platforms | Ad exchanges |
| **What it declares** | Crawl permissions | Authorized sellers | Market positioning |
| **Location** | `/robots.txt` | `/ads.txt` | `/market-position.json` |
| **Authority signal** | Domain ownership | Domain ownership | Domain ownership |

Resolution flow: check `robots.txt` first. If it exists and doesn't disallow the exchange's crawler, fetch `market-position.json`. Cache it, re-resolve on a schedule. Standard HTTP caching headers apply. If the file returns 200, use it. If it returns 404, there is no declaration.

The advertiser updates the file whenever they want. The exchange picks up changes on the next crawl. For faster updates, the advertiser can notify the exchange directly through its API. Same as pinging Google after updating a sitemap.

Domain verification is implicit. The file is on the domain. The domain has an HTTPS certificate. That's the same trust chain as `robots.txt` and `ads.txt` --- if you control the domain, you control the declaration. For higher assurance, an optional [DNS TXT record](/how-to-trust-advertisers) can cross-reference the declaration, the same mechanism [DMARC](https://datatracker.ietf.org/doc/html/rfc7489) uses for email authentication.

## Portability

[Transparency Is Irreversible](/transparency-is-irreversible) argued that transparent declarations eliminate switching costs. Here's what that looks like concretely.

A Google Ads campaign is not portable. Keywords, match types, quality scores, bid strategies, ad extensions, audience segments. All proprietary, all locked inside Google's platform. The advertiser's accumulated knowledge is the moat.

`market-position.json` is a URL. Any exchange resolves the same URL. Gets the same declaration. The version pins the embedding model, so every exchange on the same spec version computes the same vector. The advertiser updates once, every exchange sees the change. Zero switching cost. Zero lock-in.

Same pattern as `ads.txt`, opposite side of the market. Both work because they put the declaration on the entity's own domain, outside any platform's control.

## Minimal Viable Declaration

The absolute minimum:

```json
{
  "version": "0.1.0",
  "positions": [
    {
      "positioning": "Emergency roof repair and storm damage restoration for homeowners dealing with active leaks"
    }
  ]
}
```

No embedding (the exchange computes it). No sigma (the exchange [estimates it](/set-it-and-forget-it) and refines from [conversion data](/croupier)). No geocoordinates (the roofer serves wherever they serve; geo can be added later). No bid or budget (those go through the exchange's private API).

Compare this to Google Ads onboarding: keyword research, campaign structure, ad groups, match types, bid strategy selection, negative keywords, ad copy variations, landing page optimization, conversion tracking setup, audience targeting.

This takes five minutes. The advertiser already has the positioning statement. It's on their homepage. Copy it into the JSON, drop the file on your domain, done.

Or paste this into your coding agent:

> Read my homepage. Write a `market-position.json` at the site root following this spec:
>
> ```json
> {
>   "version": "0.1.0",
>   "positions": [
>     {
>       "positioning": "single natural sentence: what we offer, who it's for, what makes us the right fit",
>       "sigma": 0.15,
>       "geocoordinates": { "lat": 0.0, "lng": 0.0 }
>     }
>   ]
> }
> ```
>
> Write `positioning` the way we'd describe our own practice. `sigma` and `geocoordinates` are optional. Include `geocoordinates` if the business has a physical location.

---

`robots.txt` gave site owners a voice. `ads.txt` gave publishers one. `market-position.json` gives it to advertisers. The bid, the budget, the pacing --- those stay between you and the exchange. Identity is public, strategy is private.

*Part of the [Vector Space](/vector-space) series.*
