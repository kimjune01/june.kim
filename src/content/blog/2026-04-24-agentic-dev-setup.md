---
variant: post
title: "Agentic Dev Setup 2026"
tags: coding, projects
---

New machine for agentic work. The highest-leverage single change takes one minute.

## Alias the classic tools to their fast replacements

Agents run `grep`, `find`, and `sed` constantly. Those are the hot path. The BSD tools are slow. Their modern rewrites are 10–100× faster and handle `.gitignore` by default. Point the classic names at the rewrites in `.zshrc` and the agent never has to know.

```bash
brew install ripgrep fd sd parallel

# in ~/.zshrc
alias grep='rg'
alias find='fd'
alias sed='sd'
```

That's it. The agent emits `grep "useState" src/` by reflex; ripgrep runs. Across a 50k-file monorepo, search time drops from seconds to milliseconds. The original tools still live at `/usr/bin/grep` if you ever need them.

- **ripgrep (rg)**: respects `.gitignore`, runs parallel, 10–100× faster than `grep -r`.
- **fd**: simpler syntax, faster traversal, ignores `.git` by default.
- **sd**: clearer regex syntax than `sed`, parallel by default.
- **parallel**: GNU parallel for shell operations (no alias; call it directly).

The alias trick works because agents don't need retraining. Their built-in habits for `grep`/`find`/`sed` stay intact; only the implementation changes. It's the one-line version of making your machine faster at everything an agent does.

## Block the destructive operations before they run

Agents move fast. A handful of Bash commands are catastrophic if the agent is wrong and the shell is permissive. Hooks let you block them before they run. Add to `~/.claude/settings.json`:

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

1. **Block `rm -rf`**: Agents suggest `rm -rf node_modules` or `rm -rf dist`. Hook denies, suggests `mv /tmp/` instead.
2. **Block force push**: `git push --force` destroys remote history. Hook denies, suggests regular push or new branch.
3. **Warn on amend**: `git commit --amend` rewrites history. Hook warns but allows (needed for pre-push fixups).

Hooks run before the tool executes. Denial stops the command. Warning injects a system message into context.

## Gemini CLI with yolo mode

For agent-to-agent calls:

```bash
brew install gemini-cli google-cloud-sdk
```

Set credentials (service account JSON):

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/atom.json"
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="global"
export GOOGLE_GENAI_USE_VERTEXAI="true"
```

Make yolo mode default:

```bash
gemini() {
  /opt/homebrew/bin/gemini --yolo "$@"
}
```

Now `gemini "prompt"` auto-approves all tool calls. Useful when Claude invokes Gemini for second opinions or specialized tasks.

---

The rest is the standard new-machine stack. Skip if you know it; included here so the full setup reproduces from one page.

## Base layer

Homebrew first. Everything flows from it.

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

GitHub CLI for agent PR workflows — `gh auth login`, then the agent can `gh pr create`, `gh pr view 123`, `gh issue list`, `gh api`.

Git config (agents commit as you):

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

GitLab, if you use it:

```bash
export GITLAB_TOKEN="glpat-your-token-here"
export GITLAB_HOST="gitlab.yourcompany.com"
```

## Language toolchains

**Node / Astro**: node, pnpm, bun are installed above. For Astro projects the CLI needs to be global so the agent can run `astro dev`, `astro build`, `astro check`:

```bash
npm install -g astro
```

**Go**:

```bash
brew install go
```

Sets `GOPATH` and `GOROOT` on install. No extra config.

**Python** — `uv` for speed (Rust-based, 10× faster than pip) or `pyenv + poetry` for strict version control:

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

**Speed:**

- `grep "import.*React"` across a 50k-file monorepo: **2s → 200ms**
- `find . -name "*.test.ts"` in nested node_modules: **8s → 300ms**
- `sed 's/foo/bar/g' *.js` across 1000 files: **parallel by default with sd**
- `uv pip install requests`: **10s → 1s** vs `pip`

**Agent workflows:**

- `gh pr create` — create PR from command line
- `astro check` — type-check .astro files
- `go test ./...` — run all Go tests
- `uv run script.py` — run Python without manual venv activation

**Safety:**

- Agent suggests `rm -rf /`: **blocked** before execution
- Agent tries `git push --force origin main`: **denied** with reason

Cost: fifteen minutes of setup. Aliases preserve command syntax. Original tools still work at `/usr/bin/grep`, `/usr/bin/find` if needed.

## Full config

`.zshrc` additions:

```bash
# Performance: alias fast tools
alias grep='rg'
alias find='fd'
alias sed='sd'

# GitLab (if using)
export GITLAB_TOKEN="glpat-your-token-here"
export GITLAB_HOST="gitlab.yourcompany.com"

# Python (if using pyenv)
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Gemini CLI with yolo mode
gemini() {
  /opt/homebrew/bin/gemini --yolo "$@"
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

Git config:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

GitHub auth (interactive):

```bash
gh auth login
```

`~/.claude/settings.json` hooks section: see above.

Ship it.
