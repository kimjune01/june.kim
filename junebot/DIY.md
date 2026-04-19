# DIY: build your own junebot

A guide for a coding agent (Claude Code, Codex, Cursor, etc.) to replicate junebot for any personal site. Hand this file to the agent along with the repo you want to add a bot to, and it should be able to execute most steps autonomously — pausing for the handful of human-gated credentials and account decisions called out below.

junebot is a Lambda-hosted chat bot that answers visitor questions about a blog. Cached system prompt = persona + distilled profile + site manifest. Tools page in individual posts on demand. Streaming SSE to an inline frontend component. About $0.03 per question at Sonnet 4.6 prices with caching.

Read `README.md` in this same directory alongside this DIY. The README describes what junebot *is*. This file describes how to *rebuild* it for another site.

---

## Preconditions

Do NOT skip this section. Every item here has tripped us or someone replicating us.

### Human-gated (only the site owner can supply these)

1. **AWS account** with IAM permission to create: Lambda, IAM roles + policies, SSM parameters, optionally CloudFront + Origin Access Control. A personal account works. If an org account, confirm no SCP blocks public Lambda Function URLs.
2. **Anthropic API key** with access to Claude Sonnet (or Haiku if cost is a hard constraint). Put it in the local shell env as `ANTHROPIC_API_KEY`.
3. **Pulumi account** (free tier fine) or use Pulumi local backend. Log in with `pulumi login` before running the stack.
4. **AWS CLI** configured with a profile that has the above perms. `aws sts get-caller-identity` should return the expected account.
5. **A static blog** with content in a known directory (typically `src/content/*.md`, `content/posts/*.md`, etc.). The bot works with any static generator — Astro, Hugo, Jekyll, Next static export, plain HTML. If the site has no structured content directory, stop here and ask.
6. **Region choice**. Default us-east-1 if the site is CloudFront-hosted there; otherwise match the existing infra.

### Technical environment

7. **Python 3.11+** locally, with `pip`. The Lambda runtime is pinned to 3.11.
8. **Go 1.22+** for Pulumi (if using the Pulumi Go SDK). If the target site is TypeScript-heavy, the Pulumi TypeScript SDK works the same — translate the stack.
9. **uv** optional but recommended for local handler dev.

### Account-level gotchas (verify before you start)

10. **Lambda Function URL public invoke needs BOTH `lambda:InvokeFunctionUrl` AND `lambda:InvokeFunction`** as of AWS's October 2025 policy change. Most docs and IaC templates still add only the first. If you copy this stack, make sure the resource policy grants both, or you'll get an opaque `403 AccessDeniedException` with no useful logs and waste an hour.
11. **pydantic_core is a Rust native extension.** If you build the Lambda zip on macOS arm or any non-Linux-x86 host with default `pip install`, the Lambda will fail to boot with `ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'`. The build script pins `--platform manylinux2014_x86_64 --python-version 3.11 --only-binary=:all:`. Don't remove those flags.
12. **Astro scoped styles don't reach `innerHTML`-created elements.** If the frontend uses Astro: any `<style>` block that touches dynamically-rendered content must be `<style is:global>`, or the CSS will silently not apply. Costs about 20 minutes of "why isn't this bold" debugging.
13. **Duplicate CORS headers kill POST requests.** If you enable CORS both at the Lambda Function URL layer AND with FastAPI's `CORSMiddleware`, browsers reject responses with two `Access-Control-Allow-Origin` headers, throwing a useless `NetworkError`. Pick one layer. The Function URL config is fine alone.
14. **CloudFront OAC + Lambda Function URL is a dead end for POST bodies** as of mid-2026. GET works, POST fails with a SigV4 signature-mismatch that no origin-request-policy fiddling resolves. If you want same-origin, use an HTTP API Gateway in front (loses streaming) or just accept the `*.lambda-url.us-east-1.on.aws` domain. Don't spend hours on OAC.

---

## What you're building

```
/junebot/
├── handler/           # Lambda code (FastAPI under Lambda Web Adapter)
│   ├── app.py         # POST /api/chat streams SSE
│   ├── prompts.py     # persona + cacheable system blocks
│   ├── tools.py       # read_post / read_reading / search
│   └── pyproject.toml
├── build/
│   ├── manifest.py    # scans site content → data/manifest.json
│   └── distill.py     # (optional) private memory → public profile
├── data/
│   ├── about_june.md  # checked in, distilled
│   └── manifest.json  # gitignored, regenerated per build
├── build-zip.sh
├── deploy-code.sh
├── README.md
└── DIY.md             # this file

/infra/junebot/        # Pulumi stack (separate from day-to-day deploys)
```

Frontend: one `<JuneBot slug={slug}>` component (Astro or equivalent) mounted at the bottom of each post.

---

## Build order

Execute these sequentially. Each step should succeed before moving to the next.

### 1. Scaffold

```bash
mkdir -p junebot/{handler,build,data} infra/junebot
```

### 2. Write the handler

- `handler/app.py`: FastAPI app with `POST /api/chat`. Reads `ANTHROPIC_API_KEY` from env or SSM SecureString. Runs a bounded tool-use loop (max 6 rounds) streaming Anthropic tokens as Server-Sent Events. Accepts `{slug, messages: [...]}`.
- `handler/prompts.py`: assembles the system prompt as a list of `{type: "text", text: ..., cache_control: {type: "ephemeral"}}` blocks. Four blocks: (1) persona + source-priority rules, (2) distilled profile, (3) manifest, (4) tool schemas (done via `tools=[...]` with cache_control on the last tool).
- `handler/tools.py`: three tools. `read_post(slug)` loads one post body. `read_reading(path)` loads one reading-site page. `search(query)` does fuzzy match over the manifest.

Critical detail in `tools.py`: path resolution must handle BOTH local dev (repo-relative, e.g. `src/content/blog/*.md`) AND the Lambda zip layout (flat, e.g. `/var/task/content/blog/*.md`). Detect with `if (Path(__file__).parent / "content").exists()`.

### 3. Write the manifest builder

`build/manifest.py`: walks the content directories, parses frontmatter, produces `data/manifest.json` with one entry per post:

```json
{"kind": "post", "slug": "...", "title": "...", "tags": ["..."], "date": "...", "summary": "first prose line"}
```

Keep entries small (~200 bytes each). Manifest totals ~50k tokens for a few hundred posts.

### 4. Write the distillation script (optional but recommended)

If the site owner has a private "agent memory" or CLAUDE.md that shapes their voice, `build/distill.py` runs a one-shot Sonnet call that reads the private memory and emits a public-safe third-person profile. Strip anything addressing "the user," workflow preferences, or Claude-specific instructions. Manual, run when memory changes. Writes `data/about_june.md` (checked in).

Skip this step if the site has no such memory. The persona alone is enough.

### 5. Write the build + deploy scripts

- `build-zip.sh`: runs manifest.py, copies handler code + data + content snapshot into `.build/`, installs deps with `pip --platform manylinux2014_x86_64 --python-version 3.11 --only-binary=:all:`, writes a `run.sh` that launches uvicorn, zips the result.
- `deploy-code.sh`: runs build-zip.sh, then `aws lambda update-function-code`.

### 6. Write the Pulumi stack

`infra/junebot/main.go` (or `.ts`): creates

- SSM SecureString parameter `/junebot/anthropic-api-key` with placeholder value and `IgnoreChanges([]string{"value"})` so manual updates aren't clobbered.
- IAM role with trust policy for `lambda.amazonaws.com`.
- Inline role policy granting `ssm:GetParameter` on that one parameter.
- **No** `AWSLambdaBasicExecutionRole` attachment — junebot runs without CloudWatch Logs by design. Skip this unless you want logs.
- Lambda function: python3.11 runtime, handler `run.sh`, 1024 MB, 60 s timeout, Lambda Web Adapter layer (`arn:aws:lambda:us-east-1:753240598075:layer:LambdaAdapterLayerX86:23` in us-east-1 — check ARN for other regions), env vars for `AWS_LAMBDA_EXEC_WRAPPER=/opt/bootstrap`, `AWS_LWA_INVOKE_MODE=response_stream`, `PORT=8080`. Seed code with a placeholder zip and `IgnoreChanges([]string{"code"})`.
- Lambda Function URL: `AuthorizationType: NONE`, `InvokeMode: RESPONSE_STREAM`, CORS with `AllowOrigins` set to the site domains and `AllowMethods: ["*"]`. Do NOT list `OPTIONS` explicitly; AWS rejects that string.

**After `pulumi up` completes**, grant the two permissions manually — Pulumi doesn't handle both cleanly:

```bash
aws lambda add-permission --function-name junebot \
  --statement-id PublicUrlInvokeUrl --action lambda:InvokeFunctionUrl \
  --principal '*' --function-url-auth-type NONE --region us-east-1
aws lambda add-permission --function-name junebot \
  --statement-id PublicUrlInvokeFn --action lambda:InvokeFunction \
  --principal '*' --region us-east-1
```

### 7. Seed the SSM parameter

```bash
aws ssm put-parameter --name /junebot/anthropic-api-key \
  --type SecureString --value "$ANTHROPIC_API_KEY" --overwrite \
  --region us-east-1
```

### 8. First code deploy

```bash
bash junebot/deploy-code.sh
```

### 9. Smoke test

```bash
URL=$(cd infra/junebot && pulumi stack output functionUrl)
curl -sS "$URL/api/health"                    # should be {"ok":true}
curl -N -X POST "$URL/api/chat" -H 'content-type: application/json' \
  -d '{"slug":"any-real-slug","messages":[{"role":"user","content":"hi"}]}'
# should stream `data: {"type":"text",...}` events
```

If you get `403 AccessDeniedException`, you hit gotcha #10. Add the `InvokeFunction` permission.

### 10. Frontend component

One component, inline at the bottom of each post. Must:

- Hide itself entirely if `PUBLIC_JUNEBOT_URL` is unset (`{endpoint && (<section>...</section>)}`).
- Render a tight Q/A pair. One-shot — no history accumulated client-side.
- Stream SSE by parsing `data: {...}` lines from `fetch().body.getReader()`.
- Render streaming markdown with a small injection-safe inline renderer (escape first, transform second). Don't pull in `marked`/`markdown-it` — bundle bloat unwarranted.
- Reserve space on submit (`min-height: 60vh`) so streaming tokens don't cause layout shift; release on `done`.
- Show an animated three-dot pulse in the A: slot until the first token arrives, then fade it out.
- On error, render a `mailto:` link with the post slug and question pre-filled.
- If using Astro: `<style is:global>`.

Wire in BlogPost layout: `<JuneBot slug={slug} />`, replacing any existing chat widget.

### 11. Add the env var

```
# .env.production
PUBLIC_JUNEBOT_URL=https://xxx.lambda-url.us-east-1.on.aws
```

And `.env` for local dev, so `pnpm dev`/`astro dev` hits the prod Lambda.

### 12. Hook into existing deploy script

Example for an S3+CloudFront Astro site:

```bash
echo "==> Building site" && pnpm build
[ -x junebot/deploy-code.sh ] && bash junebot/deploy-code.sh
echo "==> Syncing to S3" && aws s3 sync dist/ s3://SITE_BUCKET/ --delete --size-only
aws cloudfront create-invalidation --distribution-id DIST_ID --paths '/*'
```

Adapt to Hugo/Jekyll/Netlify/Vercel as needed. Key invariant: rebuild manifest and update Lambda code whenever content changes.

---

## Verification checklist

Run through these before calling it done:

- [ ] `curl $URL/api/health` returns `{"ok":true}` in < 2s cold
- [ ] `curl -N -X POST $URL/api/chat ...` streams SSE events end-to-end
- [ ] Reload a post in a real browser, type a question, see Q: render immediately, three-dot pulse animate, tokens stream, disclaimer appear on completion
- [ ] Error case: set `PUBLIC_JUNEBOT_URL=https://invalid.example` in `.env`, reload, confirm mailto fallback renders correctly
- [ ] Component hides when `PUBLIC_JUNEBOT_URL` is empty
- [ ] No CloudWatch Logs group exists at `/aws/lambda/junebot` (if you followed the no-logs recipe)
- [ ] Lambda resource policy has BOTH `InvokeFunctionUrl` AND `InvokeFunction` statements for public principal

## What to adjust per site

- **Model**: replace `claude-sonnet-4-6` with whatever's current and affordable for the target site's traffic.
- **Persona voice**: rewrite `prompts.py::PERSONA` to match the site owner's voice, source-priority rules, and domain language.
- **Tool set**: if the site has extra content types (podcasts, videos, notes), add parallel `read_*` tools.
- **Distillation scope**: decide what goes into `about_XYZ.md`. Exclude private workflow prefs and agent-instruction voice. Include themes, terminology, project context.
- **Region**: match the site's primary region. Update the Lambda Web Adapter layer ARN.
- **CORS origins**: update to the site's actual domains.
- **Rate limiting**: junebot ships without any. If the site is high-traffic, add a token bucket in Lambda or put CloudFront + WAF in front.

## When to stop

You're done when the checklist passes and the site owner can see junebot answering questions about a real post. Don't over-engineer:

- No vector DB. The manifest fits in the cached system prompt.
- No conversation history. One-shot is the right UX at post bottom.
- No CloudWatch Logs. Errors go to a mailto fallback.
- No CloudFront OAC. The public URL works.
- No authentication. The bot is read-only and visitor-facing.

If the site owner asks for any of those later, they're a different post.
