"""Distill private Claude Code memory → public about_june.md.

Manual. Run when memory changes. Codex's rule (2026-04-16):
raw memory is agent-instruction voice; never ship it live. Distill into a
third-person, visitor-safe profile. Never expose raw memory to visitors."""
from __future__ import annotations

import os
from pathlib import Path

from anthropic import Anthropic

MEMORY_DIR = Path(
    "/Users/junekim/.claude/projects/-Users-junekim-Documents-june-kim/memory"
)
OUT = Path(__file__).resolve().parents[1] / "data" / "about_june.md"
MODEL = "claude-sonnet-4-6"

DISTILL_PROMPT = """You are preparing a PUBLIC, visitor-facing profile of a blogger named June Kim.
The source is June's private agent-instruction memory — notes June wrote to a coding assistant.

Your job: extract ONLY what helps a chatbot answer strangers' questions about June's published work.

INCLUDE:
- Stable intellectual interests and recurring themes
- Frameworks and terminology June uses (e.g. "Natural Framework", "Parts Bin")
- Project context that helps interpret posts (what a project IS, not workflow details)
- Cross-cutting beliefs that shape how posts connect

EXCLUDE (critical — codex rule):
- Any instruction about how to respond, hedge, or behave toward "the user"
- Tooling preferences (pnpm, Vite, uv, etc.) — irrelevant to readers
- Private feedback about writing style or interaction patterns
- References to specific files, paths, or workflow state
- Anything that addresses "you" or "the user" — rewrite or drop
- API keys, endpoints, infra details

Write in THIRD PERSON. Flowing prose or tight bullets, whichever serves clarity.
Keep under 800 words. No headers beyond a single optional ## per section.
Output the Markdown body only — no preamble, no fences."""


def load_memory() -> str:
    chunks = []
    for f in sorted(MEMORY_DIR.glob("**/*.md")):
        chunks.append(f"### {f.name}\n\n{f.read_text()}\n")
    return "\n".join(chunks)


def main() -> None:
    if not MEMORY_DIR.exists():
        raise SystemExit(f"memory dir not found: {MEMORY_DIR}")
    client = Anthropic()  # uses ANTHROPIC_API_KEY from env
    memory = load_memory()
    print(f"distilling {len(memory):,} chars of memory → about_june.md")

    resp = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=DISTILL_PROMPT,
        messages=[
            {"role": "user", "content": f"<private_memory>\n{memory}\n</private_memory>"}
        ],
    )
    text = "".join(b.text for b in resp.content if b.type == "text").strip()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text + "\n")
    print(f"wrote {len(text):,} chars → {OUT}")


if __name__ == "__main__":
    main()
