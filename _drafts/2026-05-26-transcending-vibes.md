---
variant: post-wide
title: "Transcending Vibes"
tags: coding, methodology, llm, recommendations, epistemology
draft: true
---

> ROUGH DRAFT. Notes, not prose. Over-cited on purpose: more pointers to
> artifacts and data than the finished piece needs, so they are here to pick
> from later. Through-line not chosen yet. Each bullet is one bullet now;
> some become sections, some get cut.

Premise to state cleanly first (steal the framing from
[Encoding Expertise](https://june.kim/encoding-expertise)): once you have a
*prose compiler* (issue or spec in, attested code change out), a pile of
recommendations fall out that were not obvious a year ago. They are not
opinions. They are what the existence of a verifier forces. This is the dump.

## Recommendations (each one falls out of the verifier existing)

- **Recommend Rust/Go over Python/TS for LLM-assisted projects.** Last
  year's advice (reach for dynamic languages, for model fluency) inverts
  once a verifier exists: pick the language that gives the prose compiler
  the most to check. Strong types plus a build that fails loudly gate LLM
  slop at compile time; dynamic languages let it through to merge. The
  fluency advantage that made Python/TS the default shrank (models got
  fluent in Rust/Go too) while the verification advantage of typed
  languages became decisive once a machine is doing the verifying.
  *Receipt:* our own merge rates by language. Go 69%, C++ 67%, C 67%,
  Rust 61%; JS 33%, TS 19%. [data: sweep language prior, ~111-merge
  corpus snapshot 2026-05-19; typed allowlist `{C, C++, Go, Rust}` lives
  in `sift.ALLOWED_LANGUAGES`.]

- [STUB] **Don't pitch the gate; run it inward.** A tool that filters AI
  slop is worth more pointed at your own output than sold to maintainers
  who would rather complain than install it. *Receipt:* 23 "Protect X
  from AI slop PRs" outreach issues; ~0 conversions; closed by the very
  maintainers targeted (sharkdp, sindresorhus, obra, bartlomieju, mdo,
  zanieb, ...). An AI-authored "protect yourself from AI" pitch reads as
  slop itself. Doer's lane, not pitch lane.

- [STUB] **Merit, not credence.** Spend cycles where the interaction
  carries a legible signal, held to the same bar you hold yourself to.
  *Receipt:* `fail-on-master / pass-on-fix` as the only honest test; a
  PR closed in silence with no explanation is a zero-merit interaction.

- [STUB] **Fix at the consuming layer, not the shared output.** Narrowest
  correct fix wins review. *Receipt:* bat #3737 (fix the zsh completion)
  beat our #3741 (mutate `--list-languages` output).

- [STUB] **Old issues are public-service work; freshness is not a goal.**
  Neglected work is the niche. *Receipt:* Ohno / make-problems-visible;
  backlog is an andon, not a mess to hide.

- [STUB] **Make problems visible; never hide inventory with TTLs.**
  Auto-expiring stale work masks overproduction. Fix it at the source
  (pull, WIP limits), not by sweeping the queue.

- [STUB] **Don't reinvent garbage collection.** One source of truth;
  derived views as projections, not second writable stores.

- [STUB] more fall out... (TODO: enumerate; many are downstream of the
  same prose-compiler premise)

## Pointers / receipts to weave in (DUMP, prune later)

- **The prose compiler** = the sweep pipeline: triage -> investigate
  (hypothesis graph) -> switch (classify) -> qa (adversarial) -> attest
  (`fail-on-master`/`pass-on-fix`) -> compose -> submit. Link
  [Encoding Expertise](https://june.kim/encoding-expertise) for the
  classifier-as-actor build.
- **Merge-rate corpus:** Go 69 / C++ 67 / C 67 / Rust 61 / JS 33 / TS 19
  (%). Source: language prior in the roll search die / `sift.py`
  ALLOWED_LANGUAGES rationale. (VERIFY exact n before publishing; this is
  the load-bearing receipt for the Rust/Go claim.)
- **Typed allowlist** `{C, C++, Go, Rust}` and the evictions that prove
  the gate bites: C# (fancywm), Go Template / Helm YAML (VictoriaMetrics
  helm-charts), Python (prowler, OpenHands). Non-allowlist = can't gate
  merit machine-legibly.
- **PR Quality Gate** action (the thing nobody installed):
  `github.com/kimjune01/sweep/action.yml`.
- **Campaign reception data:** 23 outreach issues, all now closed, mostly
  by maintainers within a comment or two; thin reactions; zero installs.
  `mitchellh/vouch` (suggested by a bystander) is an auth/credential gate,
  not a quality gate, i.e. a category error, worth a footnote on "gate"
  the overloaded noun.
- **Inflection-point thesis:** in ~3 months slop volume forces in-house
  credence-gates (platform-built or per-project bots). You will not own
  the gate (commodity infra accrues to platforms), but the people who
  build it re-derive merit-not-credence, fail-on-master/pass-on-fix, the
  verification-surface argument. Influence without ownership = write it
  down while ahead of the curve. (This post is that.)
- **Verification-surface argument** (the core of the Rust/Go bullet): a
  verifier is only as strong as what the language hands it to check.
  rustc/go build + types + tests + attestation = a deep surface; Python/TS
  leave it thin, so more slop survives to merge.
- **Related posts to link:** Encoding Expertise, Make No Mistakes, Memory
  Compression, Remediation. (asymptote-learning, supervisor drafts may
  share the through-line.)
- **Example fixes (receipts of the doer's lane):** DataFramesMeta #420
  (byrow-aware literal handling, consistency-with-the-function as the
  review-winning move); the bat consuming-layer story.
- TODO: pick ONE through-line. Candidates: (a) "what a verifier forces,"
  (b) "too early is the same as wrong, except for the record," (c) "the
  language recommendation inverted and nobody noticed." Probably (a).
