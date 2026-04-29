---
name: gemini
description: Send content to Gemini 3.1 Pro Preview for review. Independent second opinion — different model family from codex. Especially good at tracing logic through decision trees and catching inverted boolean conditions.
argument-hint: [file_path(s) or leave blank for in-context content]
allowed-tools: Read, Bash, Glob, AskUserQuestion
---

# Gemini Review

Send content to Gemini 3.1 Pro Preview for an independent review. Uses the Generative Language API (not Vertex AI). Report the feedback verbatim. Don't change anything until the user approves.

## When to use

- As a third reviewer after codex, when you want a genuinely independent opinion from a different model family.
- For logic-heavy content (decision trees, classifier specs, boolean chains) where Gemini has shown stronger adversarial reasoning.
- When codex has approved but the stakes are high enough to warrant a second model's review.

## Process

1. **Resolve the content.** Same as /codex: file paths, in-context content, or ask the user.

2. **Build the prompt.** Same as /codex: direct review request + content.

3. **Send to Gemini.** Use the Generative Language API via python3/urllib. The gemini CLI (Vertex AI) does not have access to preview models.

```bash
TOKEN=$(gcloud auth print-access-token \
  --scopes=https://www.googleapis.com/auth/generative-language.retriever,https://www.googleapis.com/auth/cloud-platform \
  2>/dev/null)

python3 -c "
import json, urllib.request, sys

prompt = sys.stdin.read()
body = json.dumps({'contents': [{'parts': [{'text': prompt}]}]}).encode()
req = urllib.request.Request(
    'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent',
    data=body,
    headers={'Authorization': 'Bearer $TOKEN', 'Content-Type': 'application/json'}
)
try:
    resp = urllib.request.urlopen(req, timeout=180)
    data = json.loads(resp.read())
    for c in data.get('candidates', []):
        for p in c.get('content', {}).get('parts', []):
            if 'text' in p:
                print(p['text'])
except urllib.error.HTTPError as e:
    print(f'API error {e.code}: {e.read().decode()[:200]}', file=sys.stderr)
    sys.exit(1)
" <<< "PROMPT_CONTENT_HERE"
```

   Build the prompt string in the calling code, then pass it via heredoc or variable to the python3 stdin.

4. **Report the feedback** verbatim. Don't summarize or editorialize.
5. **Wait for the user** to say what to act on.

## Rules

- Same rules as /codex: no roleplay, no stacking your own review, research low-confidence flags.
- Two passes max.
- The access token comes from `gcloud auth print-access-token` using the service account in `$GOOGLE_APPLICATION_CREDENTIALS` (~`/atom.json`).
- If the token fails, check that `gcloud` is authenticated with the right service account.

## Complementary strengths

Codex (GPT-5.5) and Gemini 3.1 Pro have different blind spots. Observed pattern from the e-value trajectory experiment:

- **Codex** is better at: structural/architectural review, identifying overclaims, suggesting reframes, catching missing baselines.
- **Gemini 3.1** is better at: tracing logic through decision trees, catching inverted boolean conditions, verifying mathematical formulas, checking that code matches spec operationally.

Run codex first (faster, broader), Gemini second (slower, more adversarial on logic).

## Also update /codex

The codex skill description says "GPT-5.4" — it should say "GPT-5.5" to match the current model.
