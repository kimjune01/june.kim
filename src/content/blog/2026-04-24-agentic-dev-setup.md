---
variant: post
title: "Agentic Dev Setup 2026"
tags: coding, projects
---

New machine for agentic work. The highest-leverage single change takes a few minutes.

## Why not just alias the classics to their modern rewrites?

Coding agents emit `grep`, `find`, and `sed` by reflex. Modern rewrites (ripgrep, bfs/fd, sd) are faster. But only two of the three alias cleanly: `ripgrep` handles most `grep` syntax natively, `bfs` is a drop-in `find` replacement, while `fd` and `sd` have incompatible CLIs and regex dialects. `find . -name "*.ts"` through `fd` errors out. `sed 's/foo/bar/g'` through `sd` silently produces wrong output when the pattern has BRE quantifiers or when the replacement uses `&` or backreferences.

The honest answer: alias the two that work, leave the third alone.

```bash
brew install ripgrep bfs

# in ~/.zshrc
alias grep='rg'          # ripgrep handles most grep syntax natively
alias find='bfs'         # bfs is a drop-in find replacement (breadth-first, faster)
```

- **[ripgrep](https://github.com/BurntSushi/ripgrep)**: aliasable. Recursive by default, respects `.gitignore`, handles the common `grep` flags agents emit.
- **[bfs](https://github.com/tavianator/bfs)**: aliasable. Advertises drop-in GNU/BSD `find` compatibility, verified on `-name`, `-type`, `-maxdepth`, `-exec`, boolean operators.
- **[sd](https://github.com/chmln/sd)** and **[fd](https://github.com/sharkdp/fd)**: worth installing, not worth aliasing. The speedups are real but the CLIs diverge too much from classic `sed`/`find` to be safe aliases. Use them by name when you want modern syntax.

I built a [sed dispatcher](https://github.com/kimjune01/classic-dispatch) that routes literal substitutions to `sd` and falls back to real `sed` for anything with regex; the repo stays up as reference for the pattern, but the safe subset is too narrow to earn its maintenance, so I don't alias it.

## Replace BSD coreutils with GNU

macOS ships BSD `date`, `ls`, `cp`, `readlink`, `stat`, `head`, `tail`, etc. Agents trained on GNU emit `date -d "yesterday"`, `readlink -f path`, `stat -c %Y file`, `head --lines=10`, none of which exist on BSD. Install `coreutils` and put the GNU versions on PATH:

```bash
brew install coreutils

# in ~/.zshrc, BEFORE any other PATH setup
export PATH="/opt/homebrew/opt/coreutils/libexec/gnubin:$PATH"
```

Same trick as the aliases above: classic names, modern (here, GNU) implementation. Unlike `fd`/`sd`, GNU coreutils is a superset-compatible drop-in. BSD scripts that use shared flags still work, and the GNU-only flags agents reach for now resolve.

Pairs naturally with `findutils` (GNU find/xargs/locate) and `gnu-sed`. For `sed` in particular, `brew install gnu-sed` + `alias sed=gsed` is the cleanest option if you don't need BSD portability.

## Disable AI attribution in commits

Claude Code adds `Co-Authored-By: Claude` to every commit by default. For open-source contributions this can trigger slop detectors and get your PRs rejected on style rather than substance. Disable it in `~/.claude/settings.json`:

```json
{
  "attribution": {
    "commit": "",
    "pr": ""
  }
}
```

## Block the destructive operations before they run

Agents move fast. A handful of Bash commands are catastrophic when the agent is wrong and the shell is permissive. Hooks block them first. Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "input=$(cat); cmd=$(echo \"$input\" | jq -r '.tool_input.command'); if echo \"$cmd\" | grep -qF 'rm -rf'; then echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"rm -rf is blocked for safety. Use mv /tmp/ instead.\"}}'; fi"
          },
          {
            "type": "command",
            "command": "input=$(cat); cmd=$(echo \"$input\" | jq -r '.tool_input.command'); if echo \"$cmd\" | grep -qE 'git[[:space:]]+push.*(--force|-f)'; then echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"Force push blocked. Use regular push or new branch.\"}}'; fi"
          },
          {
            "type": "command",
            "command": "input=$(cat); cmd=$(echo \"$input\" | jq -r '.tool_input.command'); if echo \"$cmd\" | grep -qE 'git[[:space:]]+commit.*--amend'; then echo '{\"systemMessage\":\"Warning: git commit --amend modifies history. Only use if commit hasn'\\''t been pushed.\"}'; fi"
          },
          {
            "type": "command",
            "command": "input=$(cat); cmd=$(echo \"$input\" | jq -r '.tool_input.command'); if echo \"$cmd\" | grep -qE 'gh[[:space:]]+(repo|issue)[[:space:]]+delete'; then echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"gh delete is irreversible. Run it yourself.\"}}'; fi"
          }
        ]
      }
    ]
  }
}
```

Three guards:

1. **Block `rm -rf`**. Denied; agent is nudged toward `mv /tmp/` instead. The point is undoability. /tmp sticks around long enough for you to notice the mistake. One subtlety once you move from the literal `grep -qF 'rm -rf'` above to a regex: a fixed-string match misses `rm -fr` and `rm -Rf`, but a regex loose enough to catch them (`rm.*-r.*f`) false-positives on quoted text, because a commit message containing "no-overfit" reads as `rm` ... `-r`...`f`. The safe form anchors `rm` to a command position (start of line, or after `|`, `;`, `&&`, `sudo`, `xargs`) instead of matching it as a substring of "perform" or "transform".
2. **Block force push**. Denied with reason.
3. **Block amend when pushed**. `git commit --amend` rewrites history. If HEAD is already on any remote, block: amending would force the next push to rewrite published history. If HEAD is local-only, allow silently (the pre-push fixup case). The sample JSON above only warns; the stricter version is a separate script that checks `git branch -r --contains HEAD`:

```bash
if echo "$cmd" | grep -qE 'git\s+commit\s+.*--amend'; then
  if git rev-parse --git-dir >/dev/null 2>&1; then
    head=$(git rev-parse HEAD 2>/dev/null)
    if [ -n "$head" ] && git branch -r --contains "$head" 2>/dev/null | grep -q .; then
      echo "Block: HEAD is on a remote. --amend would rewrite published history." >&2
      exit 2
    fi
  fi
fi
```

## Keep the AI tells out of GitHub

Disabling the attribution trailer (above) kills the default `Co-Authored-By: Claude`. It does not stop the model from writing "Generated with Claude Code" into the commit body, or an em dash into a PR comment. Both are tells slop detectors key on, and both ship to a durable public artifact. Two more `PreToolUse` hooks catch what the setting misses.

The first blocks any `git commit` whose message mentions Claude or carries a co-author trailer:

```bash
# block-claude-mentions.sh
input=$(cat); command=$(printf '%s' "$input" | jq -r '.tool_input.command // empty')
printf '%s' "$command" | grep -qE '(^|[|;&]\s*)git\s+commit\b' || exit 0
if printf '%s' "$command" | grep -qiE 'claude code|generated with[^"]*claude|co-authored-by:[^"]*claude|🤖'; then
  echo "no Claude mentions in commit messages; rewrite without the attribution." >&2
  exit 2
fi
```

The second fires on `git` or `gh` and blocks an em or en dash anywhere in the command line. A commit message is as durable and as scannable as a PR comment, so the rule covers git in general, not just GitHub. Hyphen-minus is fine; only the dash glyphs are caught:

```bash
# block-em-dashes.sh
input=$(cat); command=$(printf '%s' "$input" | jq -r '.tool_input.command // empty')
printf '%s' "$command" | grep -qE '(^|[|;&]\s*)(git|gh)\s' || exit 0
if printf '%s' "$command" | grep -qF '—' || printf '%s' "$command" | grep -qF '–'; then
  echo "no em or en dashes in commit messages, comments, or descriptions!" >&2
  exit 2
fi
```

Scope is the whole trick. Both hooks read only `git` and `gh` invocations, so local edits, tests, and ordinary shell work pass untouched. The false-positive surface stays near zero, which is what lets the dash rule stay strict.

Beyond these, the hook layer is where project-specific discipline lives: a kanban pipeline blocking spawn prompts that say "process all" to hold a worker at WIP=1, a release repo refusing commits that touch a frozen path. Those don't generalize, but the shape does: a few lines of `grep` on the tool input, exit 2 to deny.

## [Gemini CLI](https://github.com/google-gemini/gemini-cli) with approval-mode=yolo

For agent-to-agent calls:

```bash
brew install gemini-cli google-cloud-sdk
```

Credentials (Vertex AI):

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/atom.json"
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="global"
export GOOGLE_GENAI_USE_VERTEXAI="true"
```

Auto-approve tool calls:

```bash
gemini() {
  /opt/homebrew/bin/gemini --approval-mode=yolo "$@"
}
```

(`--yolo` is the older deprecated flag; `--approval-mode=yolo` is current.) Now `gemini "prompt"` auto-approves, useful when Claude invokes Gemini for second opinions or specialized tasks.

The audience here is agents helping humans, so I won't write out what the agent already knows. For a checklist the agent can run against a fresh machine, verify these:

- Homebrew installed, `brew shellenv` on PATH
- `git` configured with `user.name` and `user.email`
- `gh` authenticated (`gh auth status`)
- SSH key generated and added to GitHub
- Node (via nvm/volta or brew) + a package manager (pnpm/bun/yarn)
- Python: `uv` for greenfield, `pyenv` + `poetry` if the project requires pinned versions
- Go (if the project uses it)
- `jq` on PATH (the hooks depend on it)
- `~/.claude/settings.json` exists and references the hooks
- Repo directory convention established (e.g. `~/Documents/`, `~/code/`)

Read the hook scripts before relying on them. Any code you put in your shell is code that runs when you type.
