---
name: implement-spec
description: Implementation phase for feature-request (PRD-shaped) tasks (DeepSWE / Harbor). Builds the feature from the design doc, runs the proxy gate build-tools authored, and lets the adversary model (default Flash; configurable via $DSR_ADVERSARY_MODEL) challenge the diff against the acceptance criteria. Features are large (median ~840 LOC / 6 files) — completeness over minimalism. Proxy-green is the stopping signal available, NOT a certified grade-pass.
argument-hint: <task-id>
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Implement-spec: build the feature from the design doc

build-tools already wrote the proxy gate at `$PROXY_GATE_DIR`. You read the design doc, implement the feature across every edit site, volley the diff with the adversary model (`$DSR_ADVERSARY_MODEL` — default `gemini-3.5-flash` under the role-split; the craft model `$DSR_CRAFT_MODEL` writes the diff, a different-family adversary critiques it), and loop the proxy gate + existing suite until proxy-green + regression-clean.

## Rules (read first)

- **No real gate. Proxy-green is necessary, not sufficient.** Never report grade-certainty.
- **Completeness over minimalism — but the safe invariant is MONOTONICITY against the grader's observable contract.** Extra is safe only when it cannot change an observable the grader can assert (existing output, defaults, accepted types, matching/suppression sets, error behavior, canonical format). Classify by *effect on the existing/residual set*, not "what's added."
- **Source-only deliverable. Proxy gate persists.** Source edits in the tracked tree; proxy gate stays at `$PROXY_GATE_DIR` (outside tracked tree, driver excludes from diff). Never delete the gate — verify-spec runs it. Never edit existing tests to go green.
- **You generate, the adversary filters.** Never reverse. The adversary (`$DSR_ADVERSARY_MODEL`, different family from `$DSR_CRAFT_MODEL`) sees every diff and every red proxy run.
- **Enumerate with `grep -rn` before applying any N-site change. Re-grep after to confirm zero remaining.**
- **8 implementation iterations max; re-design at 3** if the approach is wrong.
- **Never violate a PRD-stated hard negative.**

## Decision tree (apply BEFORE coding — sets the build bias)

**Precedence rule:** classify by the feature's PURPOSE, not its SURFACE. If the new feature's *job* is in branch 2's verb list — regardless of implementation (new methods, keywords, flags) — **branch 2 wins over branch 3.**

1. **Changes existing behavior for existing inputs?** → preserve residual first; minimal targeted change.
2. **Purpose is** suppress / select / remove / simplify / optimize / validate / type-check / rank / order / canonicalize → **narrow implementation; preserved/residual set IS the spec;** exhaust *combinational* rules (nested resolution, precedence, dominance). Over-removal / over-suppression / over-protection is graded failure.
3. **Isolated new method / flag / input** with no default-path effect AND purpose is not branch 2 → **implement the full stated surface plus mechanically-implied adjacent cases.**
4. **Crosses a PRD hard negative, a compile-negative (`@ts-expect-error`), a security boundary, or an exact-output format** → no extra across that boundary; keep types as narrow as the spec allows.

## Environment

- Repo in offline Docker container; reach via `box-sh '<cmd>'` (already `cd`s to repo root).
- The proxy gate from build-tools lives at `$PROXY_GATE_DIR` (persistent scratch).
- The project's existing test suite is real and visible — run it for regression guard. Hidden feature tests are NOT in the tree.
- The adversary CLI (default `gemini`; see `$DSR_ADVERSARY_MODEL`) runs locally; bridge by pulling file contents via the box helper.

## Input

- The design doc (inline in adapter prompt): acceptance criteria, approach, edit sites, design alternatives, risks.
- The proxy gate file path + `proxy_gate.run` cmd, from the manifest.
- On re-entry: a **VERIFY KILL REPORT**.

## Output

- Source edits in the container that persist for verify-spec. Feature source only.
- Append nodes to the hypothesis graph.

## Process

### Phase 0 — Convergence read (monoidal contract for LLM skills)

LLM output is not bit-stable. The contract is **convergence under iteration**, not strict identity. But implement-spec's *outcome* IS deterministically checkable (proxy gate is a binary test), so the convergence test reduces cleanly to: re-running on a green state should be a no-op.

Before any edits, run `proxy_gate.run` + the existing suite once.

| State | Action |
|---|---|
| proxy green + suite clean (mod `$BASELINE_FAILS`) | **fixed point** — implementation already satisfies the proxy bar. Print `IMPLEMENT-SPEC: converged (proxy green on entry)`; do not edit. Driver routes to verify-spec for confirmation. |
| proxy red (feature absent) | proceed to Phase 1 — full implementation |
| proxy partially green (some criteria pass) | proceed to Phase 1 but with **dampener**: only edit code paths attached to the *failing* criteria. Do not touch sites already passing — those tests already discriminate. Each iteration shrinks the failing set; convergence is when failing set = ∅. |
| suite regressed (no implement-spec patch applied yet) | task is malformed — print `REJECTED — baseline regression not in $BASELINE_FAILS`; do not edit |

The dampener prevents implement-spec from rewriting code it already got right — the cause of cycling around fixed points and re-introducing bugs across iterations. Each pass acts on the diff between current state and the proxy bar, leaving everything else alone.

### Phase 1 — Read the design doc
Resolve any ambiguous edit site by reading the file. For design alternatives, pick the reading the doc bet on; note the risk.

### Phase 2 — Verify the proxy gate is in place
Run `proxy_gate.run`. It should FAIL (feature absent) for the right reasons. If a test passes pre-implementation, that criterion is mis-written or already satisfied — investigate before continuing.

### Phase 3 — Enumerate, then implement every edit site
- `grep -rn "<pattern>" .` to confirm each site from the design doc.
- Implement the full feature across all sites. Large multi-file diffs expected.
- Leave no scratch generators in the tracked source.

### Phase 4 — Adversary volley
Before running the proxy gate, volley the diff with the adversary model (different family from the craft model — under the role-split default, craft=Composer 2.5 on Kimi K2.5, adversary=Gemini 3.5 Flash on Google PaLM/Gemini family):

```bash
cat <<'PROMPT_EOF' | $DSR_GEMINI_CMD -
This diff implements a feature spec. Be direct — which acceptance criteria are unmet, what is missing, what breaks. No preamble.

ACCEPTANCE CRITERIA (must all hold):
<numbered criteria>

APPROACH:
<from design doc>

RELEVANT SOURCE (pulled from repo):
<file contents>

PROPOSED DIFF:
<unified diff>
PROMPT_EOF
```

Fold in load-bearing catches (missed criterion, wrong branch, broken invariant). Gate the rest against the proxy. Volley again on every proxy failure. Converges in 2-3 rounds.

**Note on the role-split (added 2026-05-28).** The adversary slot is now Flash, not codex (GPT-5.5). H₉'s blind-spot complementarity was measured on Claude↔GPT-5.5; the Composer↔Flash pair is unmeasured. If the partial-run measurements (HG §Transfer Risks) show the overlap is high, swap back to `codex exec` here — the cross-family adversary slot is what matters, not the specific model.

### Phase 5 — Proxy loop + regression guard

Run the proxy gate; then the project's existing suite (excluding `$BASELINE_FAILS`).

| Signal | Next move |
|---|---|
| Proxy criterion still failing | implementation missed that path — follow it |
| Existing test regressed (not in `$BASELINE_FAILS`) | change too broad — narrow the source; never edit the test |
| Proxy passes, suite clean | stop. Record as **proxy-green, not grade-green** |

Volley every proxy failure. **8 iterations max.** Leave the proxy gate at `$PROXY_GATE_DIR`.

### Phase 6 — Reopen design when the approach is wrong
After 3 iterations on the same criterion's path with no progress: stop, write `DESIGN WRONG: <what the code actually requires>` to the graph, print `NOT-RESOLVED — re-design`. Driver routes back to design-doc.

## Verify re-entry (kill report)
- **Regression** (existing suite broke): feature right but too broad — narrow source on the regressed path. Do NOT re-design.
- **Criterion's proxy test failed**: missed that criterion — fix that path.
- **Coverage hole** (criterion w/ no proxy test): add the proxy test; if behavior wasn't implemented, implement it.

## Notes
The decision-tree precedence rule (purpose over surface) is corpus-validated (HYPOTHESIS_GRAPH.md H₁ᵦ — bandit blind run misclassified surface-shaped subtractive feature as ADDITIVE; targeted mutants confirmed branch 3 mismatching loses preservation-semantics emphasis). The monotonicity framing (extra is free only when it cannot change a grader-asserted observable) came from a codex adversarial pass on a flat "bias to overbuild" rule that doesn't hold corpus-wide.
