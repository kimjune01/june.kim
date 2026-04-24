---
variant: post
title: "Agentic Dev Setup 2026"
tags: coding, projects
---

New machine. Install the tools that make agents faster, then guard the destructive operations.

## The base layer

Homebrew first. Everything else flows from it.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
```

Core runtimes:

```bash
brew install node git gh
npm install -g pnpm
curl -fsSL https://bun.sh/install | bash  # Bun for speed
```

## Git and remote hosting

GitHub CLI for agent PR workflows:

```bash
gh auth login
```

Agent can now:
- `gh pr create --title "Fix" --body "Details"`
- `gh pr view 123`
- `gh issue list`
- `gh api` for custom queries

GitLab setup (if using):

```bash
export GITLAB_TOKEN="glpat-your-token-here"
export GITLAB_HOST="gitlab.yourcompany.com"
```

Git config (agents commit as you):

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Language toolchains

### Node.js / Astro

Node + pnpm + bun are installed. For Astro projects, agents need the CLI:

```bash
npm install -g astro
```

Now `astro dev`, `astro build`, `astro check` work globally.

### Go

```bash
brew install go
```

Sets `GOPATH` and `GOROOT` automatically. Agent can `go run`, `go build`, `go test`. No extra config needed.

### Python

Modern Python: `uv` (fast, Rust-based) or `pyenv` + `poetry` (traditional).

**Option 1: uv (recommended)**

```bash
brew install uv
```

- `uv venv` — create virtualenv
- `uv pip install <package>` — 10x faster than pip
- `uv run script.py` — auto-manages env

**Option 2: pyenv + poetry**

```bash
brew install pyenv poetry
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

- `pyenv install 3.13 && pyenv global 3.13` — set Python version
- `poetry add requests` — dependency management

Pick `uv` for speed. Pick `pyenv + poetry` for strict version control.

## Performance: modern CLI tools

`grep`, `find`, and `sed` are slow. Agents search and transform code constantly. Replace them.

```bash
brew install ripgrep fd sd parallel
```

Alias as defaults in `.zshrc`:

```bash
alias grep='rg'
alias find='fd'
alias sed='sd'
```

- **ripgrep (rg)**: Respects `.gitignore`, runs parallel, 10-100x faster than `grep -r`
- **fd**: Simpler syntax, faster traversal, ignores `.git` by default
- **sd**: Clearer regex syntax than `sed`, parallel by default
- **parallel**: GNU parallel for shell operations (use directly, no alias needed)

When an agent runs `grep "pattern" .` or `find . -name "*.ts"` or `sed 's/foo/bar/g'`, it now uses the fast versions. Search time drops from seconds to milliseconds on large repos.

## Safety: Claude pre-tool-use hooks

Agents move fast. Block the destructive operations before they run.

Add to `~/.claude/settings.json`:

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
