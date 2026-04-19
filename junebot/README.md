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

- **No conversation persistence** — each question is one-shot, no history.
- **No logs** — by design. The Lambda execution role has no CloudWatch Logs permissions, so errors vanish. If you need to debug, re-attach `AWSLambdaBasicExecutionRole` temporarily, reproduce, then remove it.
- **No rate limiting** — Function URL has no throttle. Fine at current traffic; if abuse shows up, put CloudFront + WAF in front.
- **Manifest freshness** — regenerated on every `deploy.sh`, never more than a deploy stale.
- **Reading-site pages** — bot sees raw `.astro` including imports. Clean up in `tools.py::read_reading` if output quality suffers.

## Gotchas (for the next Claude that works on this)

Everything below cost real time on the first pass. Read before you touch.

### 1. Lambda Function URL needs BOTH `InvokeFunctionUrl` AND `InvokeFunction` (Oct 2025 rule)

AWS quietly changed the resource-policy requirement in October 2025: a public Function URL now rejects every request with a vague 403 "AccessDeniedException" unless the resource policy grants *both* actions. Most docs, CDK constructs, and Pulumi examples still only add `lambda:InvokeFunctionUrl`. If you see a blanket 403 with auth type NONE and a correct-looking policy, add this:

```bash
aws lambda add-permission --function-name junebot \
  --statement-id PublicUrlInvokeFn \
  --action lambda:InvokeFunction \
  --principal '*' \
  --region us-east-1
```

Note: `--function-url-auth-type NONE` is only valid for `InvokeFunctionUrl`; for `InvokeFunction` you pass principal `*` unconditionally.

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

### 4. Duplicate CORS headers kill browser requests

Lambda Function URL CORS config and FastAPI `CORSMiddleware` each add `Access-Control-Allow-Origin`. Browsers hard-reject responses with two, throwing `NetworkError` with no useful message. Pick one. We let the Function URL handle CORS; FastAPI has no middleware.

### 5. CloudFront OAC + Lambda Function URL POST is a dead end

Attempting to front the Function URL with CloudFront OAC (to get same-origin + hide the Lambda URL) signs requests with SigV4. GET works. POST with a JSON body fails with "signature does not match" — a known, unfixed AWS gotcha. Nothing in the origin request policy recovers it reliably. If you want same-origin, put an HTTP API Gateway in front instead (loses streaming) or just keep the public Function URL.

### 6. Pulumi stack has drift from manual CLI changes

`infra/junebot/main.go` creates the Lambda, but the permissions + Function URL auth were adjusted by hand during debugging. `pulumi up` against a fresh clone would revert to AuthType NONE without the correct permission pair. If you're reconciling the stack, `pulumi refresh` first, then align `main.go` with actual state before applying.

### 7. Manifest path split between zip and repo

`tools.py` resolves paths one way in the Lambda zip (flat: `content/blog/`, `content/reading/`) and a different way in local dev (repo-relative: `src/content/blog/`, `src/pages/reading/`). The detection is in `tools.py`'s module-level block. Don't refactor it away unless you want to debug `(no post found)` in production.
