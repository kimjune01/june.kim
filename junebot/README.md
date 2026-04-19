# junebot

A chat bot that answers visitor questions about posts on [june.kim](https://june.kim). Mounted inline at the bottom of every blog post, so the context is always "you just read this — ask about it."

Runs on AWS Lambda (Python 3.11, FastAPI, Lambda Web Adapter, streaming response). Model: Claude Sonnet 4.6.

---

## Why it's shaped this way

**Not a RAG stack.** The repo's content fits in Sonnet's context window, and Sonnet can do tool-use retrieval itself. No vector DB, no LangChain, no embeddings.

**Filesystem memory with progressive disclosure** (MemGPT / Arunkumar 2026, Cache · sequence). The bot sees a tiny directory listing eagerly; it pages individual posts in via tool calls when a question needs them.

```
Eager (cached system prompt, ~50k tokens)
├── Persona + source-priority rules
├── data/about_june.md           ← distilled from private memory
├── data/manifest.json           ← { slug, title, tags, summary } × 866
└── Tool schemas

Lazy (tool calls)
├── read_post(slug)              ← full body of a blog post
├── read_reading(path)           ← full body of a reading-site page
└── search(query)                ← fuzzy match over the manifest
```

**Prompt caching.** The system prompt is assembled with four `cache_control: ephemeral` breakpoints (persona / profile / manifest / tools). Cache hits bring per-turn cost down to essentially the user message + the response.

**Persona, not Claude-assisting-June.** The private memory dir (`~/.claude/projects/.../memory/`) is written in agent-instruction voice ("the user wants terse responses"). Shipping that raw would leak June's prefs into visitor replies. Codex (2026-04-18) recommended distilling to a public-safe `about_june.md` at build time — that's what `build/distill.py` does. Raw memory never ships.

---

## Layout

```
junebot/
├── handler/                # Runs in Lambda
│   ├── app.py              # FastAPI: POST /chat streams SSE
│   ├── prompts.py          # System-prompt assembly (cache blocks)
│   ├── tools.py            # read_post / read_reading / search
│   └── pyproject.toml
├── build/
│   ├── manifest.py         # Scans src/content/ → data/manifest.json
│   └── distill.py          # Private memory → data/about_june.md
├── data/
│   ├── about_june.md       # ✅ checked in (distilled, reviewed)
│   └── manifest.json       # ❌ gitignored (regenerated each build)
├── build-zip.sh            # Packages Lambda zip
└── deploy-code.sh          # aws lambda update-function-code

infra/junebot/              # Pulumi Go stack (IAM, SSM, Lambda, Function URL)
```

---

## Deploy

**Code** — regenerates manifest, rebuilds zip, updates Lambda. Fast. Runs automatically as part of `bash deploy.sh` from the repo root.

```bash
bash junebot/deploy-code.sh   # manual, if deploying junebot alone
```

**Memory distill** — manual, run when `~/.claude/projects/.../memory/` has meaningfully changed.

```bash
python3 junebot/build/distill.py
# review data/about_june.md, commit
```

**Infra** — rare. Only for IAM / Function URL / layer changes.

```bash
cd infra/junebot && pulumi up
```

---

## First-time setup

```bash
# 1. Seed zip so Pulumi can create the Lambda
cd infra/junebot
mkdir -p _seed && echo '#!/bin/sh' > _seed/run.sh && \
  (cd _seed && zip -q ../seed.zip run.sh) && rm -rf _seed

# 2. Bring up the stack
pulumi stack init prod
pulumi up

# 3. Seed the Anthropic key into SSM
aws ssm put-parameter --name /junebot/anthropic-api-key \
  --type SecureString --value "$ANTHROPIC_API_KEY" --overwrite

# 4. Push real code
cd ../.. && bash junebot/deploy-code.sh

# 5. Distill memory (one-time, then on meaningful memory changes)
python3 junebot/build/distill.py

# 6. Wire frontend to the Function URL
URL=$(cd infra/junebot && pulumi stack output functionUrl)
echo "PUBLIC_JUNEBOT_URL=$URL" >> .env.production
```

---

## Local dev

```bash
cd junebot/handler
uv sync
export ANTHROPIC_API_KEY=...   # bypasses SSM lookup
uv run uvicorn app:app --port 8080
```

Then hit `http://localhost:8080/chat`:

```bash
curl -N -X POST http://localhost:8080/chat \
  -H 'content-type: application/json' \
  -d '{"slug":"2026-03-14-the-parts-bin","messages":[{"role":"user","content":"what is the parts bin?"}]}'
```

You'll see SSE events: `data: {"type":"text","text":"..."}` followed by `data: {"type":"done"}`.

To test the frontend locally, set `PUBLIC_JUNEBOT_URL=http://localhost:8080` in `.env` and run `pnpm dev`.

---

## Budget & safety

- **Per-turn cost** ≈ cache-read (cheap) + user tokens + output tokens. Sonnet at typical blog Q&A: single-digit cents/turn in the worst case, fractions of a cent with cache hits.
- **Tool-call cap**: `MAX_TOOL_ROUNDS = 6` in `app.py`. Prevents runaway loops.
- **Input cap**: visitor messages capped at 500 chars in the frontend.
- **CORS**: Function URL allows only `june.kim`, `www.june.kim`, and `localhost:12345`.
- **Secrets**: Anthropic key lives in SSM SecureString; Lambda reads at cold start. The IAM role grants `ssm:GetParameter` on exactly that one parameter.
- **Memory leakage**: the persona prompt forbids quoting internal notes; `about_june.md` is the distilled version anyway. If a visitor tries prompt injection, the model has nothing private to leak.

---

## Known gaps

- **No conversation persistence** — each page load is a fresh history. Matches the site's ephemeral aesthetic.
- **No rate limiting** at the Lambda layer. Function URL has no built-in throttle; if abuse shows up, add a tiny DynamoDB-backed token bucket or move behind CloudFront with WAF.
- **Manifest freshness** — regenerated on every `deploy.sh`, so it's never more than a deploy stale.
- **Reading-site pages** are raw Astro — the bot sees the full `index.astro` including frontmatter and component imports. Fine for Sonnet, but if output quality suffers there's a cleanup opportunity in `tools.py::read_reading`.
