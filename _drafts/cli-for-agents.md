---
variant: post-wide
title: "CLIs for agents"
tags: design
---

*Sequel to [JIT CLI](https://june.kim/jit-cli) and [Skill actors](https://june.kim/skill-actor-tricks).*

[clig.dev](https://clig.dev) is the closest thing the field has to a CLI design standard. Help text examples, exit codes, stdout/stderr split, `--json` on read commands, confirmation prompts on destructive ops, `NO_COLOR`, tab completion, `--version`, `-q/--quiet`, misuse-vs-traceback messages. All correct. All necessary. All aimed at a human user with eyes, hands, a terminal, and the slack to read prose.

The other user is the agent. It reads bytes. It has no eyes. It cannot ask, "did that work?" — it has to know from what came back. It cannot scroll. It cannot tell two failure modes apart by feel. It retries. It runs in parallel. It composes your CLI with three other CLIs you don't control. clig.dev is silent on every one of these.

So is everything else.

The conventional response — "we'll just add a Python SDK / MCP server / typed bindings" — moves the problem. The CLI surface is the contract anyway, because the SDK shells out to it and because every other agent in the wild calls the CLI directly. You don't get to bypass it. You have to make the CLI itself callable by something without eyes.

What follows is ten patterns this distinction forces. Each is *invariant + mechanism + failure-prevented*, no language. Written first for agents that build CLIs other agents will call; written second for humans who'll review the diffs.

## 1. Exit codes route, not announce

**Invariant:** every distinct outcome that needs distinct caller action has a distinct exit code.
**Mechanism:** 0 = success. 1 = user error (the caller should fix the inputs). 2 = system error (the caller should retry or escalate). 3+ = domain-specific outcomes the caller routes on (timeout, partial, dry-run-only, etc.). Document the table next to `--help`.
**Prevents:** the agent's standard "if rc != 0: panic" pattern collapsing distinct cases into one. With routed codes, the agent's loop has somewhere to branch.

## 2. Failure must arrive before success

**Invariant:** the bytes a caller reads sequentially must let it tell failure from success at the first opportunity.
**Mechanism:** flush stderr before raising. Never print "done" or "built" on a path that might have failed; print the failure first, with `flush=True`, then exit nonzero. Don't trust the implicit ordering — the OS buffers and the agent reads the tail.
**Prevents:** the silent-success-on-failed-job pattern. A CLI that prints "✓ built sweep-tester" after docker exited 1 has lied to its caller — and a human might catch it from the surrounding terminal context, but an agent reading only the trailing bytes won't.

## 3. Idempotency by default, opt-out for the rare case

**Invariant:** running the same command twice with the same inputs is safe.
**Mechanism:** writes are upsert. Sinks deduplicate. Drafts skip when already-draft. Adds skip when already-present. State stores last-value-wins. Reserve `--force` for the rare case where re-execution actually has to do something different.
**Prevents:** the agent's natural retry-and-resume pattern producing duplicate PRs, double-counted events, mid-edit corruption. Agents re-run things on transient errors; if the second run isn't safe, your CLI isn't agent-callable.

## 4. Dry-run is universal, not optional

**Invariant:** every write-side command has a `--dry` mode that exercises the same code path without external effect.
**Mechanism:** the dry path prints, line-by-line, every external action it *would* take, in the order it would take them. No "would do approximately N things" summaries. Each line names the resource + the action.
**Prevents:** the agent committing to a maintainer-visible action it can't preview. Dry mode caught a CLI that would have drafted an approved PR — the most expensive possible action — by listing it among the "would" rows.

## 5. Structured output for the read-half

**Invariant:** every read command emits structured output behind a `--json` flag (or by default if the output is purely data).
**Mechanism:** JSON lines for streams, JSON objects for snapshots. Field names stable across versions. Never embed prose in fields the caller needs to parse.
**Prevents:** the agent regex-parsing prose. Regex-parsed prose is the largest single source of agent-side flakiness in CLI piping; structured output collapses an entire failure class.

## 6. Discoverability with enumerated alternatives

**Invariant:** when the agent names a subcommand / flag / resource that doesn't exist, the error tells the agent the valid set.
**Mechanism:** `unknown actor 'attest'; known: ['investigate_cycle', 'qa', 'respond_cycle', 'triage_cycle']`. Print the sorted list of valid names. Bonus: print the levenshtein-closest match, prefixed as a guess.
**Prevents:** the agent guessing again. A "did you mean X?" prompt is for humans; an enumerated list is for the agent's next attempt. Agents will not browse `--help`; they will read the error and act.

## 7. Errors name the verbatim fix command

**Invariant:** when the CLI tells the agent *what's wrong*, it also tells the agent *what to type next* — as a shell-callable string.
**Mechanism:** `"test_env defaulted to 'native' on 'darwin' host. Choose one: sweep retro set <repo> test_env docker:<image> (for linux-only repos), OR sweep retro set <repo> test_env native (to confirm cross-platform). Then sweep andon clear."` The remediation is a sequence of literal commands. The agent copy-pastes.
**Prevents:** the agent diagnosing the substrate from prose. If the next step is a single command, name it. Don't make the agent reason about your internals to figure out which flag to flip.

## 8. Pointer to artifact, never blob in stdout

**Invariant:** when the command's output is more than a few hundred bytes, write it to a file and print the path.
**Mechanism:** generate the artifact at a deterministic path. Print the absolute path. Print a one-line summary. Done. The agent reads the file when it needs to.
**Prevents:** stdout truncation, context-window blowout when an agent shells the command from inside another agent's pipeline, and the structural mistake of treating stdout as a persistence layer. Artifact existence is binary; stdout always parses into *something*.

## 9. Witness IDs in every interesting error

**Invariant:** every error or skip surfaces a stable handle the caller can grep upstream evidence with.
**Mechanism:** `"no_tests_in_pr — PR changed 2 files but none look like tests. Witness msg_id attest-20260518T034553-jasonish-evebox-369 at ~/.sweep/events.jsonl."` The msg_id is the join key into the event log. The path is where to grep.
**Prevents:** the agent having to reconstruct what produced the error. With a witness ID, the next CLI in the pipe just greps that ID and gets the full upstream context. Errors stop being terminal; they become referents into a richer state the agent can read with one more command.

## 10. CLIs that emit prompts for other agents

**Invariant:** when a CLI detects a fix-class shape that has a known remediation, it emits a *self-contained* spec a fresh agent (no prior context) can execute.
**Mechanism:** the spec is a markdown file with **Symptom** (witness event), **Diagnosis** (which code with line numbers), **Remediation** (numbered steps as shell-callable commands). One file per detected shape. Filename slug is repo + msg-id-tail. The CLI prints the paths.
**Prevents:** the operator being the bottleneck on every recurring fix. The recurrence becomes a queue; any agent (in any session) can pick a file and execute. The CLI is no longer just a tool the agent calls — it's a tool that hands the agent its next instruction set. The boundary blurs.

## What's missing from clig.dev that's missing on purpose

clig.dev's confirmation prompts on destructive ops, NO_COLOR, tab completion, --version — all still correct, just orthogonal. The agent doesn't care about those; it also doesn't break on them. The ten above are the patterns that *would* break an agent's pipeline if missing.

There's also a pattern clig.dev names that needs inverting: clig.dev wants human-readable error messages. Agents want *machine-routable* errors. Both are true — the message should be both, structured-then-prose: `code: detail`. The agent reads the code; the human reads the detail.

## Why this stops being CLI design

Notice the drift. Tricks 1–5 are recognizably CLI design. Tricks 6–7 cross into linguistic design (errors as a protocol). Trick 8 is filesystem-as-contract. Trick 9 is observability-as-CLI. Trick 10 isn't CLI design at all — it's CLI as an outbound channel for instructions to other agents.

The convergence point: when both the caller and the user-of-the-output are agents, the CLI stops being a thin layer over the substrate and becomes the substrate's primary self-describing surface. clig.dev assumes the human is the substrate's apex consumer. Agents are not, structurally. They are intermediaries — each CLI call is a step in a longer chain another agent (or operator) will need to read, understand, retry, or compose with. The design pressure is different. The design moves are different.

This post isn't the last word; it's a starter ten that this work surfaced. If you build something that catches a failure class the ten above don't cover, write it down. Agents are unreliable parts; the CLIs they call are the boundary that makes the unreliability composable.
