[`market-position.json`](/market-position-json) defined what the advertiser declares. This post defines what the exchange is allowed to ask for.

The publisher-exchange boundary is a contract. OpenAPI makes it auditable and enforceable by the same [coding agents](/skills-over-sdks) that integrate it. Every field that doesn't exist is a promise.

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
                                                  POST /event/serve
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
  /catalog:
    get:
      summary: Fetch advertiser catalog for local caching
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

  /auction:
    post:
      summary: Run auction on conversation embedding
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
            enum: [serve, click, conversion]
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

Three event types: `serve`, `click`, `conversion`. Each is a POST to `/event/{type}` with the `auction_id` and `advertiser_id` from the auction response.

`serve` fires when the creative renders. `click` when the user taps it. `conversion` when the advertiser confirms a downstream action via [blind-signed coupons](/croupier).

These events feed three systems:

1. **Billing.** The VCG price from the auction, matched to a serve event.
2. **Sigma auto-tuning.** Distance histograms with minimum bin sizes feed the [sigma controller](/set-it-and-forget-it). The exchange sees aggregate patterns, not individual users.
3. **Verified conversions.** [Attested attribution](/attested-attribution) proves a sale happened without linking it to a user.

## What's Not in the Spec

No user targeting endpoint. No retargeting. No remarketing. No frequency capping by user ID (the publisher handles that locally). No lookalike audiences. No user profile sync.

Relevance comes from [embedding proximity](/power-diagrams-ad-auctions). Frequency is the publisher's decision. Lookalikes are meaningless when targeting is geometric. The [go-to-market](/the-playbook) doesn't need them either.

The spec is intentionally narrow. Everything not listed is the publisher's domain. The surface area is the promise.

## Skills Read This

The [`install.md`](https://github.com/kimjune01/vectorspace-skills/blob/main/install.md) skill reads this OpenAPI spec and generates integration code into the publisher's codebase. The [`verify.md`](https://github.com/kimjune01/vectorspace-skills/blob/main/verify.md) skill audits compliance against it.

---

The surface area is the promise.

*Part of the [Vector Space](/vector-space) series.*
