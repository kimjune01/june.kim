---
variant: post
title: "Agentic Dev Setup 2026"
tags: coding, projects
---

New machine for agentic work. The highest-leverage single change takes a few minutes.

## Why not just alias the classics to their modern rewrites?

Coding agents emit `grep`, `find`, and `sed` by reflex. Modern rewrites (ripgrep, bfs/fd, sd) are faster on the hot path. But the naive aliases only work for one of the three: `ripgrep` handles most `grep` syntax natively, `bfs` is a drop-in `find` replacement by design, but `fd` and `sd` have incompatible CLIs and different regex dialects. Routing `find . -name "*.ts"` through `fd` errors out. Routing `sed 's/foo/bar/g'` through `sd` silently produces wrong output when the pattern has BRE quantifiers or when the replacement uses `&` or backreferences.

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

For `sed` specifically: I built a [compatibility dispatcher](https://github.com/kimjune01/classic-dispatch) that routes fully-literal `sed 's/X/Y/g'` substitutions to `sd -F` and falls back to `/usr/bin/sed` for everything else — regex metacharacters, addresses, non-`s` commands, backreferences. 25 parity tests against real sed. It works. But I ripped it out of my own setup after building it. The safe-subset fast path (pure literals, no metacharacters either side, `/g` flag only) is too narrow: most real `sed` invocations have at least one regex character, so they land on the fallback path where nothing is gained. Stock `sed` is already fast enough for the file sizes that go through it. 120 lines of bash wrapping every `sed` call on the machine, for maybe five seconds saved a month, wasn't worth the maintenance surface. Repo stays live as a reference for the dispatcher-with-fallback pattern; don't install it.

## Replace BSD coreutils with GNU

macOS ships BSD `date`, `ls`, `cp`, `readlink`, `stat`, `head`, `tail`, etc. Agents trained on GNU emit `date -d "yesterday"`, `readlink -f path`, `stat -c %Y file`, `head --lines=10` — none of which exist on BSD. Install `coreutils` and put the GNU versions on PATH:

```bash
brew install coreutils

# in ~/.zshrc, BEFORE any other PATH setup
export PATH="/opt/homebrew/opt/coreutils/libexec/gnubin:$PATH"
```

Same trick as the aliases above: classic names, modern (here, GNU) implementation. Unlike `fd`/`sd`, GNU coreutils is a superset-compatible drop-in — BSD scripts that use shared flags still work, and the GNU-only flags agents reach for now resolve.

Pairs naturally with `findutils` (GNU find/xargs/locate) and `gnu-sed` (GNU sed) if you want to replace those too. For `sed` in particular, `brew install gnu-sed` + `alias sed=gsed` is the cleanest option if all your work is GNU-native.

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

1. **Block `rm -rf`**. Agents suggest `rm -rf node_modules` or `rm -rf dist`. The hook denies and suggests `mv /tmp/` instead.
2. **Block force push**. `git push --force` destroys remote history. Denied with reason.
3. **Warn on amend**. `git commit --amend` rewrites history. Shows a warning to the user; doesn't block (needed for pre-push fixups).

The denial path stops the command; the warning path shows a message to the user without blocking.

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

---

The rest is the standard Apple-Silicon macOS new-machine stack. Skip if you know it; it's here so the whole setup reproduces from one page.

## Base layer

Homebrew first. Paths below assume Apple Silicon (`/opt/homebrew`); swap to `/usr/local` on Intel.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
```

Core:

```bash
brew install node git gh
npm install -g pnpm
curl -fsSL https://bun.sh/install | bash
```

GitHub CLI for agent PR workflows. Run `gh auth login`, then the agent can `gh pr create`, `gh pr view 123`, `gh issue list`, `gh api`.

Git config (agents commit as you):

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Language toolchains

**Node**: already installed above. Most projects manage their own CLIs via `package.json` scripts (`pnpm dev`, `pnpm build`); agents invoke them via scripts, no global install needed.

**Go**:

```bash
brew install go
```

Modern Go infers `GOPATH` and `GOROOT` from defaults. No extra config.

**Python**: [`uv`](https://github.com/astral-sh/uv) for speed (10× faster than pip per its own benchmarks) or [`pyenv`](https://github.com/pyenv/pyenv) + [`poetry`](https://python-poetry.org) for strict version control:

```bash
brew install uv
# or
brew install pyenv poetry
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

With `uv`: `uv venv`, `uv pip install <pkg>`, `uv run script.py`. With pyenv + poetry: `pyenv install 3.13 && pyenv global 3.13`, then `poetry add <pkg>`.

## What this buys you

**Speed on common agent commands**: ripgrep and bfs replace the BSD originals on the search hot path. GNU coreutils on PATH means `date -d`, `readlink -f`, `stat -c` work.

**Agent workflows**: `gh pr create` from the command line, `go test ./...`, `uv run script.py`, project-local `pnpm dev` — all work directly.

**Safety**: `rm -rf` and `git push --force` blocked before execution. `git commit --amend` blocked when HEAD is already on a remote; allowed silently on local-only commits.

Cost: about fifteen minutes.

## Full config

`.zshrc` additions:

```bash
# Aliases: fast tool replacements where CLI-compatible
alias grep='rg'
alias find='bfs'

# GitLab (if using)
export GITLAB_TOKEN="glpat-your-token-here"
export GITLAB_HOST="gitlab.yourcompany.com"

# Python (if using pyenv)
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Gemini CLI with approval-mode=yolo
gemini() {
  /opt/homebrew/bin/gemini --approval-mode=yolo "$@"
}

# Google Cloud / Vertex AI
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/atom.json"
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="global"
export GOOGLE_GENAI_USE_VERTEXAI="true"

# gcloud CLI
source /opt/homebrew/share/google-cloud-sdk/path.zsh.inc
source /opt/homebrew/share/google-cloud-sdk/completion.zsh.inc
```

Read the hook scripts in `~/.claude/hooks/` before relying on them. Any code you put in your shell or your agent's tool chain is code that runs when you type.

Git config:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

GitHub auth: `gh auth login`.

`~/.claude/settings.json` hooks section: see above.

Ship it.
