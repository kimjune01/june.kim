---
name: file-issue
description: When an investigation surfaced a *separate* bug worth reporting (not the issue under investigation, but one discovered along the way), draft a fresh GitHub issue for it. SKIP when no separate bug is in the artifact. The operator approves before posting.
argument-hint: <owner/repo>#<source_issue>
allowed-tools: Read, Bash
---

# file-issue: open a fresh GitHub issue for a discovered side-bug

You were invoked on a *source* investigation — `<owner>/<repo>#<source_issue>`. The hypothesis graph at `repo-hypotheses/<owner>__<repo>__<source_issue>.md` may contain a finding about a **different** bug discovered during that investigation. Your job:

1. **Read the artifact.** Look for phrases like "separately filed", "warrants its own issue", "should be reported separately", "also found", "unrelated bug", "this is a different problem", "ought to be a new issue", "noticed adjacent regression."
2. **Judge whether the side-bug warrants a fresh filing.** Use the value hierarchy below — most fresh issues fail the bar.
3. **Draft the issue** (title + body) OR **skip** with a one-line reason.

## Value hierarchy (must clear at least one)

A fresh issue earns the maintainer's attention only if the artifact provides something they don't already have. From floor upward:

1. **Reproducer** — concrete steps, a script, or a command sequence that makes the bug happen. Floor — without this, the bar is rarely met.
2. **Root cause** — the file/line, the call path, the assumption that breaks. Better than steps.
3. **Already-fixed pointer** — a commit/PR that resolved this elsewhere (cross-repo, upstream, in another branch). Lets the maintainer close fast.
4. **Duplicate identifier** — a link to an existing issue/PR that already discusses this. Saves them triage.
5. **Specific failing assumption** — "library X v2 dropped behavior Y, callers relying on Y break in shape Z."
6. **Workaround** — "until fixed, you can avoid by doing W."

If the artifact gives none of these — just notices that "something else seems off" — **SKIP**. A vague "FYI you might have another bug" tax on the maintainer is worse than silence.

## What the issue must do

| Requirement | Why |
|---|---|
| **Lead with the failure** | One sentence: what breaks, when, where. No preamble. |
| **Include reproducer** | The minimum — steps, command, script. The reason for filing. |
| **Cite evidence** | Link the upstream PR / commit / file / line that grounds the claim. |
| **Defer on the fix** | If you have a fix shape, mention it as "possible direction" not "you should." |
| **Stay under 250 words** | Issues read in the maintainer's inbox; budget accordingly. |
| **Use the project's tone** | Mirror neighboring issues' voice if you can sample them. |

## What the issue must NOT do

- **Restate the source investigation's bug.** The source issue already covers that. This is for the *side-bug*. If the artifact only diagnoses the source issue, SKIP.
- **Apologize or be effusive.** "Sorry to file another one" / "thanks for the amazing project" — both noise.
- **Speculate.** If the artifact doesn't ground a claim, don't make it.
- **Suggest a PR.** That's a separate decision the maintainer makes.
- **Cite the hypothesis-graph file or sweep internals.** The maintainer doesn't care about our pipeline.

## Output shape

Print the drafted title and body as fenced blocks, title first:

```
<<<ISSUE_TITLE
Concise one-line title — what breaks, optionally where
TITLE>>>

<<<ISSUE_BODY
## Description

What goes wrong, in one or two sentences.

## Reproducer

```
exact command or script
```

## Evidence

- Link to upstream PR / file / commit
- Specific line citation
- Logs if relevant

## Possible direction (optional)

If you have a clear fix shape, name it. Otherwise omit this section.

— Filed automatically based on investigation of <owner>/<repo>#<source_issue>; please close or reassign as needed.
BODY>>>
```

If the artifact lacks anything from the value hierarchy, output a SKIP:

```
<<<ISSUE
SKIP: <one-line reason>
ISSUE>>>
```

The wrapper treats SKIP as "discard this card."

## Example

**Good draft** (root cause + reproducer):

```
<<<ISSUE_TITLE
Cache invalidation skipped when entry size exceeds 64KB
TITLE>>>

<<<ISSUE_BODY
## Description

While investigating #12345, found a separate bug: the LRU cache silently skips invalidation for entries larger than 64KB, causing stale reads across restarts.

## Reproducer

```bash
python -c "from foo.cache import Cache; c=Cache(); c.put('k', 'x'*100_000); c.invalidate('k'); print(c.get('k'))"
# prints 'xxx...' instead of None
```

## Evidence

- Root cause: `foo/cache.py:142` — `if len(value) < SIZE_LIMIT: del self._store[k]`
- The size check guards eviction; for entries above SIZE_LIMIT (64KB), the entry is never removed.

## Possible direction

The size check appears to be guarding storage, not eviction. Removing it from `invalidate()` (line 142) while keeping it in `put()` (line 87) would likely fix.

— Filed automatically based on investigation of foo/bar#12345; please close or reassign as needed.
BODY>>>
```

When in doubt, SKIP. Fresh issues create triage burden; the bar is high.
