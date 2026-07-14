---
variant: post
title: "Publisher API"
tags: vector-space
description: "v0.1.0"
---

[`market-position.json`](/market-position-json) defined what the advertiser declares. This post defines what the exchange is allowed to ask for.

The publisher-exchange boundary is a contract. OpenAPI makes it auditable and enforceable by the same [coding agents](/skills-over-sdks) that integrate it. Every field that doesn't exist is a promise.

*This post is the design-level view: the privacy-preserving core, three calls. The shipped server exposes a larger surface and the authoritative, machine-readable spec is [`openapi.yaml`](https://github.com/kimjune01/vectorspace-adserver/blob/master/apidocs/openapi.yaml) in the adserver repo. Where the two differ, the repo spec is the truth; the endpoint names below have been reconciled to it.*

## The Flow

A user is chatting with a health chatbot. The chatbot interprets intent locally, computes an embedding, and checks it against a cached advertiser catalog. A candidate matches. The UI surfaces a prompt: "Can I make a recommendation?" The user taps yes. The publisher sends the embedding to the exchange. The exchange runs the auction, returns a winner. The publisher renders the creative. The user taps it. They land on the advertiser's page.

Three API calls touched the exchange. Everything else happened on the publisher's side.

```
chat → intent embedding → catalog lookup → UI prompt → user tap
                             (local)         (local)     ↓
                                                    POST /auction
                                                         ↓
                                              render creative (local)
                                                         ↓
                                                  POST /event/impression
                                                         ↓
                                                    user taps ad
                                                         ↓
                                                  POST /event/click
                                                         ↓
                                                   destination URL
                                                      (local)
```

## The Spec

Three endpoints. None accepts a user ID, a session ID, raw text, an IP address, or conversation history.

```yaml
openapi: 3.1.0
info:
  title: Vector Space Publisher API
  version: 0.1.0
  description: Publisher-exchange boundary contract.

paths:
  /embeddings:
    get:
      summary: Fetch advertiser catalog (embeddings + bids) for local caching
      parameters:
        - name: If-None-Match
          in: header
          schema:
            type: string
      responses:
        '200':
          description: Full catalog
          headers:
            ETag:
              schema:
                type: string
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Catalog'
        '304':
          description: Not modified

  # Conceptual auction call. Shipped as the encrypted POST /ad-request (production,
  # privacy-preserving) and the plaintext POST /simulate + POST /openrtb2/auction
  # (dev/interop). See openapi.yaml for the exact request bodies of each.
  /auction:
    post:
      summary: Run auction on conversation embedding (conceptual; see note above)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AuctionRequest'
      responses:
        '200':
          description: Auction result
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuctionResponse'
        '204':
          description: No candidate met the relevance threshold

  /event/{type}:
    post:
      summary: Report ad event
      parameters:
        - name: type
          in: path
          required: true
          schema:
            type: string
            enum: [impression, click, viewable]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Event'
      responses:
        '200':
          description: Event recorded

security:
  - publisherToken: []

components:
  securitySchemes:
    publisherToken:
      type: http
      scheme: bearer

  schemas:
    Catalog:
      type: object
      required: [positions]
      properties:
        positions:
          type: array
          items:
            $ref: '#/components/schemas/Position'

    Position:
      type: object
      required: [id, embedding, sigma, creative_url, destination_url]
      properties:
        id:
          type: string
        name:
          type: string
        embedding:
          type: array
          items:
            type: number
            format: float
        sigma:
          type: number
          format: float
          description: Reach parameter
        creative_url:
          type: string
          format: uri
        destination_url:
          type: string
          format: uri

    AuctionRequest:
      type: object
      required: [embedding, candidate_ids, tau]
      properties:
        embedding:
          type: array
          items:
            type: number
            format: float
        candidate_ids:
          type: array
          items:
            type: string
          minItems: 1
          description: Position IDs pre-filtered by local proximity
        tau:
          type: number
          format: float
          description: Publisher relevance threshold

    AuctionResponse:
      type: object
      required: [auction_id, winner_id, price]
      properties:
        auction_id:
          type: integer
        winner_id:
          type: string
        price:
          type: number
          format: float
          description: VCG second price

    Event:
      type: object
      required: [auction_id, advertiser_id]
      properties:
        auction_id:
          type: integer
        advertiser_id:
          type: string
```

## Catalog

The catalog is the set of [`market-position.json`](/market-position-json) declarations the exchange has crawled. Advertiser positions are [public by design](/transparency-is-irreversible). The publisher caches the catalog locally and re-syncs via standard HTTP `ETag`.

Phase 1 runs entirely against this cache. Cosine distance between the conversation embedding and every cached position. The exchange doesn't know the user exists until the user taps.

Catalog size is bounded by the number of advertisers. A health chatbot caches hundreds of positions, not millions. This is a set of [positioning statements](/marketing-speak-is-the-protocol) with precomputed vectors.

The catalog carries embeddings, sigma, creative URL, destination URL. Bid prices stay between the advertiser and the exchange. The publisher handles relevance. The exchange handles pricing.

## The Auction Call

Only fires after user consent. The publisher sends the conversation embedding, the candidate IDs that passed local proximity filtering, and a [relevance threshold](/three-levers) tau.

The exchange runs [`score = log(bid) - distance² / σ²`](/power-diagrams-ad-auctions) against each candidate, selects the winner by [VCG](/one-shot-bidding), and returns three fields: auction ID, winner ID, price.

The publisher already has the winner's creative URL and destination URL from the cached catalog.

Pre-filtering is the publisher's responsibility. If a health chatbot has 500 positions cached and only 12 pass proximity filters, the auction request carries 12 IDs, not 500.

## Events

Three event types: `impression`, `click`, `viewable`. Each is a POST to `/event/{type}` (see [`openapi.yaml`](https://github.com/kimjune01/vectorspace-adserver/blob/master/apidocs/openapi.yaml) for the exact body).

`impression` fires when the creative renders (frequency-capped). `click` when the user taps it, which triggers the CPC charge on first click. `viewable` when the creative meets the viewability threshold. Downstream conversions are tracked off this path via [blind-signed coupons](/croupier) — see [attested attribution](/attested-attribution).

These events feed three systems:

1. **Billing.** The VCG price from the auction, matched to an impression event.
2. **Sigma auto-tuning.** Distance histograms with minimum bin sizes feed the [sigma controller](/set-it-and-forget-it). The exchange sees aggregate patterns, not individual users.
3. **Verified conversions.** [Attested attribution](/attested-attribution) proves a sale happened without linking it to a user.

## What's Not in the Spec

No user targeting endpoint. No retargeting. No remarketing. No frequency capping by user ID (the publisher handles that locally). No lookalike audiences. No user profile sync.

Relevance comes from [embedding proximity](/power-diagrams-ad-auctions). Frequency is the publisher's decision. Lookalikes are meaningless when targeting is geometric. The [go-to-market](/the-playbook) doesn't need them either.

The spec is intentionally narrow. Everything not listed is the publisher's domain. The surface area is the promise.

## Agents Read This

The authoritative [`openapi.yaml`](https://github.com/kimjune01/vectorspace-adserver/blob/master/apidocs/openapi.yaml) is what a coding agent reads to generate an integration client and to audit compliance against the wired routes. Packaged `install` / `verify` skills that wrap this flow are planned; today the spec itself is the interface.

---

The surface area is the promise.

*Part of the [Vector Space](/vector-space) series.*
