---
name: log
description: Append a timestamped entry to the project work log. Rotates at 1000 lines.
argument-hint: <entry text, or empty to auto-summarize recent work>
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Log: Work Log Entry

Append a timestamped entry to the project's work log. When the active log exceeds 1000 lines, rotate it.

## Directory

All logs live in `worklog/` at the repo root.

- **Active log**: `worklog/WORK_LOG.md`
- **Rotated logs**: `worklog/WORK_LOG-{YYYY-MM-DD-HHMMSS}.md`

## Process

1. Check if `worklog/WORK_LOG.md` exists. If not, create it with a `# Work Log` header.
2. Count lines in the active log.
3. If the line count exceeds 1000:
   - Rename the current file to `worklog/WORK_LOG-{timestamp}.md` using the current datetime.
   - Create a fresh `worklog/WORK_LOG.md` with the `# Work Log` header.
4. **Determine entry content:**
   - If the user provides an argument, use it as the entry content.
   - If the user provides no argument, summarize the most recent work from the conversation: what was done, what was decided, what's next. Write it in the same voice as the conversation — concise, specific, no filler. Include file paths, commit messages, or prediction records if relevant.
5. Append the entry to `worklog/WORK_LOG.md` with this format:

```markdown

### {HH:MM} — {short summary of the action}

{entry content}
```

If the last `## {date}` header in the file matches today's date, append under it. Otherwise, add a new `## {YYYY-MM-DD}` header before the entry.

6. Report: line count after append, and whether rotation occurred.

## Session-persistent logging

Running this skill once activates logging for the rest of the session. After the initial entry:

- **Auto-log at natural milestones**: commits, deploys, significant decisions, task completions, direction changes. Don't wait for the user to invoke `/log` again.
- **Don't interrupt flow**: append the log entry silently (no "I've logged this" announcements). Just do it alongside whatever else you're doing.
- **Cadence**: log when something worth recording happens, not on a timer. A session with three commits gets three entries. A session that's all discussion might get one entry at the end.
- **Same format**: every auto-logged entry follows the same `### HH:MM — summary` format.

## Rules

- Entries are append-only. Never edit or remove previous entries.
- If the user provides an argument, log it as given — don't paraphrase.
- If the user provides no argument, auto-summarize from conversation context. Be specific: names, tickers, predictions, decisions, not vague summaries.
- Keep the `## date` / `### time — summary` hierarchy consistent.
