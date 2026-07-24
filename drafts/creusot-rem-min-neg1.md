# Creusot rem MIN%-1 finding — NULL (benign), with a reframed audit surface

Date: 2026-07-22. Stack built locally (opam + Why3 1.8.2 + Alt-Ergo 2.6.2 / Z3 4.15.3 / CVC4 1.8 / CVC5 1.3.1). Repo at commit 8d73ab6.

## Verdict

The hypothesized bug does **not** exist. `Int$bits_count$BW::rem` is indeed missing the `signed division overflow` precondition that its sibling `div` carries, but the omission is **benign**: nothing that reaches that prelude op can smuggle `iN::MIN % -1` past the front end.

## What the prelude looked like (finding, as stated)

`prelude-generator/int.in.coma`, module `Int$bits_count$BW`, `let rem` (~line 291) carries only `remainder by zero`. Sibling `div` (~line 286) additionally carries `signed division overflow check` rejecting `min_sint / -1`. The non-BW `Int$bits_count$::rem` (~line 230) also carries it. So BW::rem is a real outlier. That part held up.

## Why it is benign (the reframe)

The overflow guard for `MIN % -1` does not come only from the prelude. It also comes from **rustc's own MIR**, which Creusot faithfully translates (`creusot/src/translation/function/terminator.rs:227`, `AssertKind::Overflow(op, ..) -> "expl:{op} overflow"`). The generated Coma for `a % b` under `#[bitwise_proof]` carries, *before* the `Int32BW.rem` call:

```
| s6 = [ &_12 <- Bool.bw_and (b == -1) (a == MIN) ]
| s7 = {[@expl:Rem overflow] not _12} s8      // program-level obligation
| s8 = Int32BW.rem {a} {b} ...
```

So `rem` is **double-gated**. Two exhaustive cases:

- **Variable operands** (`fn f(a,b){ a % b }`, pinned to MIN/-1 by preconditions): rustc emits the runtime `Rem overflow` assert, Creusot turns it into the `s7` obligation, and it is false under the preconditions. Empirically: `why3find prove` returns `vc_rem_min_neg1: ✘ (2/3)` — the `Rem overflow` subgoal is unprovable. The `should_fail` test does not verify **even on today's buggy prelude**.
- **Constant operands** (`fn f() -> i32 { i32::MIN % -1 }`, the #2190 shape): hard compile error — `error: this operation will panic at runtime ... #[deny(unconditional_panic)]`. Does not compile, so no program reaches the prelude.

Either way the prelude precondition is never the *sole* gate. Weakening or dropping it does not admit a false proof.

## Why #2190 (shifts) was different

`int-shift-full.rs` used `1u8 >> 8` — a **constant** shift. The generated Coma goes straight to `UInt8.shr` with **no** program-level guard. Shift overflow is `arithmetic_overflow`, a **suppressible** lint (`#[allow(arithmetic_overflow)]` compiles and yields a value); it is *not* the hard `unconditional_panic` error that arithmetic overflow is. So a constant out-of-range shift both (a) compiles and (b) has its runtime assert elided — leaving the prelude bound as the **sole** gate. That is exactly why the `<=`/`<` off-by-one was a live soundness hole.

## Reframed audit surface

A prelude boundary precondition is load-bearing (sole gate) only where rustc's runtime `Assert` is **elided** *and* the program still compiles. That requires a compile-time-constant operand whose overflow is a **suppressible** lint. Across the integer ops that is essentially **shifts only**:

| op | constant-operand overflow | variable operand |
|---|---|---|
| add/sub/mul/neg/div/rem | hard error (`unconditional_panic`) — won't compile | runtime `Overflow` assert — double-gated |
| shl/shr | `arithmetic_overflow` — suppressible, compiles, assert elided → **sole-gated** | runtime `Overflow` assert — double-gated |
| index | hard error (const OOB) / runtime `BoundsCheck` | `BoundsCheck` |

The shift bounds were the sole-gated arithmetic surface, and #2190 already fixed the off-by-one in all four modules (UInt, UInt BW, Int, Int BW). The redundant arithmetic preconditions (add/sub/mul/div/rem overflow) are belt-and-suspenders; a wrong constant there is masked by the MIR assert and does not produce a false proof in any compiling program.

Implication for the sweep: don't grep every `@expl:` precondition. Target preconditions that are the **only** thing standing between a compiling Rust program and a panic — i.e. where Creusot emits no corresponding MIR `Assert`. For integers that pointer lands back on shifts (done) and on non-panicking ops whose prelude *postconditions* (result values, e.g. `srem`/`mod`/cast semantics) could be wrong — a different bug class (wrong result, not missing panic) worth a separate pass.

## Housekeeping

No PR, no Zulip note (nothing to report). Repo left clean; prelude untouched; test artifacts removed. Local prover stack remains installed for the next sweep.
