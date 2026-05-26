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
│   ├── app.py              # FastAPI: POST /api/chat streams SSE
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

# 6. Wire frontend to the site origin / CloudFront behavior
echo "PUBLIC_JUNEBOT_URL=https://june.kim" >> .env.production
```

---

## Local dev

```bash
cd junebot/handler
uv sync
export ANTHROPIC_API_KEY=...   # bypasses SSM lookup
uv run uvicorn app:app --port 8080
```

Then hit `http://localhost:8080/api/chat`:

```bash
curl -N -X POST http://localhost:8080/api/chat \
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
- **Origin**: Production traffic goes through the site CloudFront distribution's `/api/*` behavior to the Lambda Function URL. The Function URL uses `AWS_IAM`; public browser traffic should not call it directly.
- **Secrets**: Anthropic key lives in SSM SecureString; Lambda reads at cold start. The IAM role grants `ssm:GetParameter` on exactly that one parameter.
- **Memory leakage**: the persona prompt forbids quoting internal notes; `about_june.md` is the distilled version anyway. If a visitor tries prompt injection, the model has nothing private to leak.

---

## Known gaps

- **No conversation persistence** — each question is one-shot, no history.
- **No logs** — by design. The Lambda execution role has no CloudWatch Logs permissions, so errors vanish. If you need to debug, re-attach `AWSLambdaBasicExecutionRole` temporarily, reproduce, then remove it.
- **No app-level rate limiting** — fine at current traffic; if abuse shows up, add CloudFront/WAF controls or a small Lambda-side token bucket.
- **Manifest freshness** — regenerated on every `deploy.sh`, never more than a deploy stale.
- **Reading-site pages** — bot sees raw `.astro` including imports. Clean up in `tools.py::read_reading` if output quality suffers.

## Gotchas (for the next Claude that works on this)

Everything below cost real time on the first pass. Read before you touch.

### 1. The Function URL is private behind CloudFront OAC

The current runtime uses `AuthorizationType: AWS_IAM` on the Lambda Function URL. CloudFront signs origin requests via OAC and routes site `/api/*` traffic to the function. Do not "fix" browser 403s by making the Function URL public unless you are intentionally rolling back to the old architecture.

CloudFront permissions were granted after the distribution was known; see `infra/junebot/README.md` for the setup shape.

### 2. Python Lambda needs linux x86_64 wheels

`pydantic_core`, which comes in with `anthropic`, is a Rust native extension. Installing deps on macOS arm produces wheels Lambda can't load — `ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'`. `build-zip.sh` already pins this, but if you replicate outside that script:

```bash
pip install --platform manylinux2014_x86_64 \
            --python-version 3.11 \
            --only-binary=:all: \
            --target .build \
            anthropic fastapi uvicorn boto3
```

### 3. Astro `<style>` scoping does not apply to `innerHTML`-created elements

The frontend component uses `innerHTML` to render streaming markdown and the Q/A pair. Astro's default scoped styles are keyed to `data-astro-cid-*` attributes that only exist on statically rendered elements — dynamically created nodes don't match. Symptom: CSS silently doesn't apply, and you spend a while debugging "why isn't this bold." Fix: `<style is:global>`. Keep class names prefixed (`.junebot-*`) to avoid collisions.

### 4. Duplicate CORS headers can still kill browser requests

Do not add FastAPI `CORSMiddleware` casually. CORS/same-origin behavior belongs at the CloudFront edge for production. Duplicate `Access-Control-Allow-Origin` headers make browsers hard-reject responses with a vague `NetworkError`.

### 5. CloudFront owns the production route

`PUBLIC_JUNEBOT_URL` should point at the site origin in production, not the raw Lambda URL. The component appends `/api/chat`, and CloudFront routes that path to the Function URL.

### 6. Some CloudFront/OAC wiring is still outside this Pulumi stack

`infra/junebot/main.go` creates the Lambda and `AWS_IAM` Function URL. The CloudFront distribution and origin-access permission are managed outside this stack. If you're reconciling infra, refresh first and verify the live CloudFront behavior before applying changes.

### 7. Manifest path split between zip and repo

`tools.py` resolves paths one way in the Lambda zip (flat: `content/blog/`, `content/reading/`) and a different way in local dev (repo-relative: `src/content/blog/`, `reading-src/pages/reading/`). The detection is in `tools.py`'s module-level block. Don't refactor it away unless you want to debug `(no post found)` in production.
