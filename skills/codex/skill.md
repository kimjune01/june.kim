---
name: codex
description: Send a file to codex (GPT-5.4) for review. Reports feedback — no changes until the user approves.
argument-hint: [file_path(s) or leave blank for in-context content]
allowed-tools: Read, Bash, Glob, AskUserQuestion
---

# Codex Review

Send content to codex for a second opinion. Report the feedback verbatim. Don't change anything until the user approves.

## Process

1. **Resolve the content.** Three modes:
   - **File path(s) given:** Read and concatenate them.
   - **Content in conversation context:** The user has been working on something in-context (e.g., a draft, a plan, a code block). Gather it.
   - **Nothing clear:** Ask the user what to send.

2. **Build the prompt.** Compose a single prompt that includes:
   - A direct review request tailored to the content type (prose, code, plan, etc.)
   - All the content, clearly delimited.

3. **Send to codex.** Pipe the prompt via stdin to avoid shell quoting issues:

```bash
cat <<'PROMPT_EOF' | codex exec -
Review the following. What works, what doesn't, what to cut, what to strengthen. Be direct — no preamble, no praise sandwich.

---

<content here>
PROMPT_EOF
```

   For multiple files, include each with a filename header:

```bash
cat <<'PROMPT_EOF' | codex exec -
Review the following files together. What works, what doesn't, what to cut, what to strengthen. Be direct — no preamble, no praise sandwich.

--- file: path/to/first.md ---
<contents>

--- file: path/to/second.md ---
<contents>
PROMPT_EOF
```

4. **Report the feedback** to the user exactly as codex returns it. Don't summarize, reframe, or editorialize.
5. **Wait for the user** to say what to act on. Don't apply changes unprompted.

## Rules

- Don't roleplay in the prompt. No "You are a senior editor." Just ask directly.
- Don't add your own review on top. The point is a second opinion, not two opinions stacked.
- If codex flags something with low confidence, research it before dismissing. Structural soundness is not a substitute for evidence.
- Two passes max. If the second pass has no structural notes, the content is ready.
- Always pipe via stdin (`| codex exec -`) rather than inline quoting, to avoid shell escaping issues with large content.
