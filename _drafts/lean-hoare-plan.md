---
title: "Lean Hoare Layer Plan"
---

# Two Proofs, One Theorem

The existing Lean proof reasons **functionally**: monadic composition via `>>=`,
support reachability via `support_bind`, contracts as predicates on outputs.

The new layer reasons **imperatively**: weakest preconditions, Hoare triples,
rule-based composition where `support_bind` is hidden behind `wp_comp`.

Both prove the same pipeline properties. The bridge theorem shows they're
equivalent. That equivalence IS the Rosetta stone row — compiled.

Paper citations throughout this plan are for orientation, not dependency.
When in the proof trenches, the relevant object is `support_bind`, not an
arXiv link. If a citation stops being useful, ignore it.

## Architecture

```
NaturalFramework/
  -- Existing (functional proof)
  Support.lean           — possibilistic shadow
  Kleisli.lean           — Kernel, comp, id
  Contracts.lean         — Contract, ContractPreserving, handshakes
  Handshake.lean         — coupling lemma, info monotonicity
  Variational.lean       — MinimizesOn, optimality derivations
  ...

  -- New (imperative proof)
  Hoare/
    Core.lean            — Triple, consequence, comp, skip
    WP.lean              — wp, triple_iff_wp, wp_comp
    PipelineProof.lean   — reprove pipeline via Hoare rules only

  -- Bridge (equivalence)
  Bridge/
    Contracts.lean       — ContractPreserving ↔ Triple
    Handshakes.lean      — Handshake ↔ triple chain
```

## The key invariant

**Pipeline proofs in `Hoare/PipelineProof.lean` must NEVER unfold support
semantics directly.** All support reasoning lives in `wp_comp` (soundness).
The pipeline proof uses only: `triple_comp`, `triple_consequence`, `triple_skip`,
and `triple_iff_wp`. If it compiles without importing `Support.lean` directly,
the separation is real.

## Hoare/Core.lean (~60 lines)

Mirrors [Bonchi, Di Lavore, Roman, Staton (2025)](https://arxiv.org/abs/2507.18238) assertion-correctness triples (Def 77, Thm 79). Their `{p} c {q}` is `assert p ; c ≤ c ; assert q` in a posetal imperative category. Ours is the semantic version: if P holds on input, Q holds on all outputs.

Ungraded — following [Gaboardi et al. (ESOP 2021)](https://doi.org/10.1007/978-3-030-72019-3_9) at grade = 1. Graded extension deferred to Phase 2.

```lean
/-- Ungraded Hoare triple. -/
def Triple [Monad M] [Support M]
    (P : α → Prop) (f : Kernel M α β) (Q : β → Prop) : Prop :=
  ∀ a : α, P a → ∀ b : β, Support.support (f a) b → Q b

/-- Consequence: weaken precondition, strengthen postcondition. -/
theorem triple_consequence [Monad M] [Support M]
    {P P' : α → Prop} {Q Q' : β → Prop} {f : Kernel M α β}
    (h : Triple P f Q)
    (hpre : ∀ a, P' a → P a)
    (hpost : ∀ b, Q b → Q' b)
    : Triple P' f Q'

/-- Sequential composition via Kleisli. -/
theorem triple_comp [Monad M] [LawfulMonad M] [Support M]
    {P : α → Prop} {Q : β → Prop} {R : γ → Prop}
    {f : Kernel M α β} {k : Kernel M β γ}
    (hf : Triple P f Q)
    (hk : Triple Q k R)
    : Triple P (Kernel.comp f k) R

/-- Skip: identity kernel preserves any predicate. -/
theorem triple_skip [Monad M] [Support M]
    {P : α → Prop}
    : Triple P (Kernel.id (M := M)) P
```

## Hoare/WP.lean (~80 lines)

Follows [Jacobs (2014)](https://www.cambridge.org/core/journals/mathematical-structures-in-computer-science/article/abs/weakest-preconditions-in-fibrations/657A41FD194D8CC5E4662B71F2E1454E) — wp-semantics from order-enriched Kleisli categories via poset fibrations. Jacobs instantiated this for Kleisli(D) = FinStoch without calling it a Markov category.

`wp_comp` is the **one place** in the Hoare layer that touches `support_bind` directly. It IS the monad multiplication diagram from [Fritz, Perrone, Rezagholi (MSCS 2021)](https://arxiv.org/abs/1910.03752), reframed as a predicate transformer composition law.

```lean
/-- Weakest precondition: the strongest P such that {P} f {Q}. -/
def wp [Monad M] [Support M] (f : Kernel M α β) (Q : β → Prop) : α → Prop :=
  fun a => ∀ b, Support.support (f a) b → Q b

/-- Triple is equivalent to P ≤ wp f Q (pointwise). -/
theorem triple_iff_wp [Monad M] [Support M]
    {P : α → Prop} {Q : β → Prop} {f : Kernel M α β}
    : Triple P f Q ↔ ∀ a, P a → wp f Q a

/-- WP composition: wp(k ∘ f) = wp(f) ∘ wp(k).
    The ONLY place in the Hoare layer that touches support_bind. -/
theorem wp_comp [Monad M] [LawfulMonad M] [Support M]
    {f : Kernel M α β} {k : Kernel M β γ} {Q : γ → Prop}
    : wp (Kernel.comp f k) Q = wp f (wp k Q) := by
  funext a
  simp only [wp, Kernel.comp]
  apply propext
  constructor
  · intro h b hb c hc
    exact h c ((Support.support_bind _ _ _).mpr ⟨b, hb, hc⟩)
  · intro h c hc
    obtain ⟨b, hb, hk⟩ := (Support.support_bind _ _ _).mp hc
    exact h b hb c hk
```

## Bridge/Contracts.lean (~40 lines)

The bridge theorem. Shows the functional proof (ContractPreserving) and the imperative proof (Triple) are equivalent. Trivially true by definition — that's the point.

`handshake_enables_comp` connects to [Kura, Gaboardi, Sekiyama, Unno (2026)](https://arxiv.org/abs/2601.14846) — their restricted pointwise order (Def 7) says the ordering holds where the predicate is non-⊥. Our handshake says post implies pre. Same structural role: the side condition that lets two adjacent triples chain.

```lean
/-- ContractPreserving IS a Triple with trivial precondition. -/
theorem contract_is_triple [Monad M] [Support M]
    {f : Kernel M α β} {Q : β → Prop}
    : ContractPreserving f Q ↔ Triple (fun _ => True) f Q := by
  constructor
  · intro h a _ b hb; exact h a b hb
  · intro h a b hb; exact h a trivial b hb

/-- A Handshake is a triple_comp side condition.
    post(N) implies pre(N+1) is exactly what triple_comp needs. -/
theorem handshake_enables_comp [Monad M] [LawfulMonad M] [Support M]
    {f : Kernel M α β} {k : Kernel M β γ}
    {h : Handshake β}
    (hf : Triple P f h.post)
    (hk : Triple h.pre k R)
    : Triple P (Kernel.comp f k) R :=
  triple_comp
    (triple_consequence hf (fun _ h => h) h.compatible)
    hk
```

## Hoare/PipelineProof.lean (~100 lines)

Reproves the pipeline using ONLY Hoare rules. Does NOT import Support.lean.

This is where the proof skeleton differs from the existing one. The existing proof (Handshake.lean) unfolds `Pipeline.forward`, rewrites `support_bind` three times, and extracts existential witnesses. This proof chains five triples via `handshake_enables_comp`. No witness extraction.

Mirrors [Bonchi, Di Lavore, Roman, Staton (2025)](https://arxiv.org/abs/2507.18238) Thm 79 COMP rule: `{p} c₁ {q}` and `{q} c₂ {r}` gives `{p} c₁;c₂ {r}`.

```lean
/-- Five-stage forward pipeline via triple chaining. -/
theorem forward_triple [Monad M] [LawfulMonad M] [Support M]
    (p : Pipeline M I) (h : PipelineHandshake I)
    (h_perceive : Triple (fun _ => True) p.perceive h.perceive_cache.post)
    (h_cache    : Triple h.perceive_cache.pre p.cache h.cache_filter.post)
    (h_filter   : Triple h.cache_filter.pre p.filter h.filter_attend.post)
    (h_attend   : Triple h.filter_attend.pre (p.attend policy) h.attend_remember.post)
    (h_remember : Triple h.attend_remember.pre p.remember persisted)
    : Triple (fun _ => True) (Pipeline.forward p policy) persisted :=
  -- Chain via handshake_enables_comp at each junction
  sorry -- to be filled

/-- The coupling lemma reproved via Hoare.
    Same theorem as cycle_preserves_policy, different proof method.
    The forward+backward structure mirrors Smithe's Bayesian lens:
    forward pass (inference) composed with backward pass (learning).
    See: https://arxiv.org/abs/2109.04461 -/
theorem coupling_via_hoare [Monad M] [LawfulMonad M] [Support M]
    (p : Pipeline M I) (h : PipelineHandshake I)
    (h_con : Triple persisted (p.consolidate policy) h.consolidate_attend.post)
    : True := sorry -- placeholder
```

## Guardrails

```lean
/-- Nontriviality: a kernel that violates a contract. -/
example : ¬ Triple (fun _ => True) (fun _ => pure 42) (fun n => n < 10) := by
  intro h
  have := h () trivial 42 (by rw [Support.support_pure]; rfl)
  omega

/-- wp of identity is identity on predicates. -/
theorem wp_id [Monad M] [Support M] {Q : α → Prop}
    : wp (Kernel.id (M := M)) Q = Q := by
  funext a; simp [wp, Kernel.id, Support.support_pure]
```

## What makes this NOT a relabeling

1. **PipelineProof.lean never imports Support.lean.** It uses only Triple, wp,
   and the Hoare rules. The support semantics are encapsulated.
2. **The bridge theorem is bidirectional.** ContractPreserving ↔ Triple proves
   the two proof methods reach the same conclusions.
3. **wp_comp is the ONLY lemma that uses support_bind.** Everything above it
   is rule-based. The existing proof uses support_bind in every composition.
4. **The proof skeleton is different.** Existing: unfold forward, rewrite
   support_bind three times, extract witnesses. New: chain five triples via
   triple_comp and handshake_enables_comp. No witness extraction.

## Graded extension (Phase 2, future)

Only after choosing a real semantic grade. Following [Gaboardi et al. (ESOP 2021)](https://doi.org/10.1007/978-3-030-72019-3_9) graded Freyd category semantics and [Kura et al. (2026)](https://arxiv.org/abs/2601.14846) indexed preordered monoids:

- Grade = InfoMeasure values, with InfoBounded f g as a predicate
- Composition: InfoBounded f g₁ → InfoBounded k g₂ → InfoBounded (comp f k) (g₁ + g₂)
- This connects to existing NonExpanding and StrictlyLossy
- NOT a phantom grade — the grade constrains the morphism

The connection to [Sato-Katsumata (MSCS 2023)](https://arxiv.org/abs/2206.05716) divergences on monads: their Thm 2 shows divergences = Kleisli enrichments. If the grade is a divergence bound, the graded Triple becomes a quantitative Hoare triple with information-theoretic content.

## Order of implementation

1. Core.lean — Triple, consequence, comp, skip (half day)
2. WP.lean — wp, triple_iff_wp, wp_comp (half day)
3. Bridge/Contracts.lean — contract_is_triple, handshake_enables_comp (half day)
4. PipelineProof.lean — forward_triple, coupling_via_hoare (2 days)
5. Guardrails — counterexample, wp_id (half day)

Total: ~4 days, ~300 lines.
