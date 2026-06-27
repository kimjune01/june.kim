# Junebot receptionist — build spec

A second entry point to the existing Junebot Lambda. Not new infra — the same
agent (Sonnet 4.6, `search`/`read_post`/`read_reading` tools over the 866-entry
manifest), reached from a dedicated page in a new "receptionist" framing.

## What it is

A dedicated page, linked by a subtle button next to the homepage logo. Junebot
greets the visitor, asks what brought them here, draws out the interest over a
short back-and-forth, then routes them to the right posts / reading pages / apps.
A front desk, not a tutorial. Elicit, then route.

The routing itself is the bot's *existing* capability: the base PERSONA already
closes answers with `### Related` links. Guide mode only adds the elicitation.

## Reuse vs. new

Reuse, untouched:
- The Lambda agent loop, tools, manifest, prompt caching.
- The `JuneBot` frontend class (streaming SSE + markdown render).

New:
- A `mode` parameter on `/api/chat` (`"post"` | `"guide"`), explicit.
- A guide-mode system block (receptionist brief), appended LAST so the cached
  persona/profile/manifest prefix stays byte-identical across both surfaces.
- A dedicated page mounting Junebot in guide mode, no slug.
- A logo-adjacent button on the homepage linking to it.
- Multi-turn: bump `MAX_INCOMING_MESSAGES` 4 → 16; frontend accumulates history.

## Backend changes

`app.py`
- `ChatIn` gains `mode: Literal["post", "guide"] | None = None`.
- Default: `mode = body.mode or ("post" if body.slug else "guide")`.
- Pass `mode` into `system_blocks(mode)`.
- `MAX_INCOMING_MESSAGES = 16`.

`prompts.py`
- `system_blocks(mode)` appends a 4th text block after the manifest block:
  - `post`: no extra block (today's behavior).
  - `guide`: the receptionist brief (below), with `cache_control` ephemeral.

Receptionist brief (draft):
> You are at the front desk of june.kim. The visitor just arrived and likely
> doesn't know the lay of the land. Your job: find out what they're curious
> about, then point them at the right posts.
> - Open by asking what brought them here. One question at a time.
> - Elicit before routing. Don't dump a reading list on turn one.
> - Once you know the interest, name 1–3 specific posts or reading pages and
>   say why each fits. Use search() / read_post to ground the picks.
> - Warm but terse. Same voice as June's posts. You are a guide, not a greeter
>   reading a script.

## Frontend changes

`JuneBot.astro`
- Split the `JuneBot` class into a shared script importable by both surfaces,
  OR add a `variant: "inline" | "page"` prop. Keep the inline post-bottom
  behavior identical.
- Send `mode` in the POST body. Accumulate `messages` across turns in page mode
  (inline stays one-shot).

New page (route: `/junebot` — CONFIRM)
- Full-width container, mounts Junebot in page/guide mode, no slug.
- Hardcoded opening line client-side (Junebot greets first), so a page load
  doesn't fire a cold Lambda call before the visitor speaks. The real agent
  starts on their first reply.

Homepage (`src/pages/index.astro`)
- Subtle "Talk to Junebot" affordance next to `<aside class="logo">`,
  `<a href="/junebot">`.

## Open

- Route name: default `/junebot`. (alts: `/talk`, `/front-desk`, `/start`)
- Receptionist opening line copy.

## Out of scope (for now)

- Conversation persistence across page loads.
- Rate limiting (current traffic doesn't need it).
- Logging (Lambda has no CloudWatch perms by design).
