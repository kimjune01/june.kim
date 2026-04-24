---
variant: post
title: "Agentic Dev Setup 2026"
tags: coding, projects
---

New machine for agentic work. The highest-leverage single change takes a few minutes.

## Why not just alias the classics to their modern rewrites?

Coding agents emit `grep`, `find`, and `sed` by reflex. Modern rewrites (ripgrep, bfs/fd, sd) are faster. But only two of the three alias cleanly: `ripgrep` handles most `grep` syntax natively, `bfs` is a drop-in `find` replacement, while `fd` and `sd` have incompatible CLIs and regex dialects. `find . -name "*.ts"` through `fd` errors out. `sed 's/foo/bar/g'` through `sd` silently produces wrong output when the pattern has BRE quantifiers or when the replacement uses `&` or backreferences.

So the honest answer is: alias the two that work, leave the third alone.

```bash
brew install ripgrep bfs

# in ~/.zshrc
alias grep='rg'          # ripgrep handles most grep syntax natively
alias find='bfs'         # bfs is a drop-in find replacement (breadth-first, faster)
```

- **[ripgrep](https://github.com/BurntSushi/ripgrep)** — aliasable. Recursive by default, respects `.gitignore`, handles the common `grep` flags agents emit.
- **[bfs](https://github.com/tavianator/bfs)** — aliasable. Advertises drop-in GNU/BSD `find` compatibility, verified on `-name`, `-type`, `-maxdepth`, `-exec`, boolean operators.
- **[sd](https://github.com/chmln/sd)** and **[fd](https://github.com/sharkdp/fd)** — worth installing, not worth aliasing. The speedups are real but the CLIs diverge too much from classic `sed`/`find` to be safe aliases. Use them by name when you want modern syntax.

I built a [compatibility dispatcher](https://github.com/kimjune01/classic-dispatch) for `sed` that routes fully-literal `sed 's/X/Y/g'` to `sd -F` and falls back to `/usr/bin/sed` for anything more complex — regex metacharacters, addresses, non-`s` commands, backreferences. 25 parity tests against real sed. It works, but I ripped it out of my setup. The safe-subset fast path (pure literals, `/g` flag only) is too narrow: most real `sed` invocations have at least one regex character and land on the fallback path, where nothing is gained. Stock `sed` is already fast enough for typical file sizes. 120 lines of bash wrapping every `sed` call, for maybe five seconds saved a month, wasn't worth the maintenance. Repo stays live as a reference for the dispatcher-with-fallback pattern; don't install it.

## Replace BSD coreutils with GNU

macOS ships BSD `date`, `ls`, `cp`, `readlink`, `stat`, `head`, `tail`, etc. Agents trained on GNU emit `date -d "yesterday"`, `readlink -f path`, `stat -c %Y file`, `head --lines=10` — none of which exist on BSD. Install `coreutils` and put the GNU versions on PATH:

```bash
brew install coreutils

# in ~/.zshrc, BEFORE any other PATH setup
export PATH="/opt/homebrew/opt/coreutils/libexec/gnubin:$PATH"
```

Same trick as the aliases above: classic names, modern (here, GNU) implementation. Unlike `fd`/`sd`, GNU coreutils is a superset-compatible drop-in — BSD scripts that use shared flags still work, and the GNU-only flags agents reach for now resolve.

Pairs naturally with `findutils` (GNU find/xargs/locate) and `gnu-sed`. For `sed` in particular, `brew install gnu-sed` + `alias sed=gsed` is the cleanest option if you don't need BSD portability.

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
          }
        ]
      }
    ]
  }
}
```

Three guards:

1. **Block `rm -rf`**. Denied; agent is nudged toward `mv /tmp/` instead. The point isn't safety-by-destination; it's undoability. /tmp sticks around long enough for you to notice the mistake.
2. **Block force push**. Denied with reason.
3. **Block amend when pushed**. `git commit --amend` rewrites history. If HEAD is already on any remote, block — amending would force the next push to rewrite published history. If HEAD is local-only, allow silently (the pre-push fixup case). The sample JSON above only warns; the stricter version is a separate script that checks `git branch -r --contains HEAD`:

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

The rest is ordinary new-machine setup — Homebrew, node/git/gh, the language toolchain of choice, `gh auth login`, git config. The audience for this post is agents helping humans set up; all of that is territory the agent already knows. The part worth writing down is above: what the aliases really cost, what the coreutils trick buys, and which destructive commands the hooks actually stop.

Read the hook scripts before relying on them. Any code you put in your shell is code that runs when you type.
