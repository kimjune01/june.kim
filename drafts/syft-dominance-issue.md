# Draft: syft design issue — dominance, not ordered rules, for overlap precedence

Status: FILED 2026-07-20 as anchore/syft#5083 (https://github.com/anchore/syft/issues/5083), before PR merge per June's two-clocks call. This file is now the archive copy; edits go to the live issue.

Repo: anchore/syft. Suggested labels: enhancement, discussion.

---

Title: **An alternative to the ordered rule list for overlap precedence: dominance**

Context: in #4905 I added the language-package overlap exclusion behind another boolean flag. The PR is a bounded step while the config design will take rounds of discussion to resolve, so the two run on different clocks. Therefore the discussion is worth starting now.

While that PR was under review, kzantow sketched the future config for overlap exclusions on the [July 16 stream from 8:30 to 17:00](https://www.youtube.com/watch?v=oB0I7ePP_e0&t=510s). The sketch composes package types and cataloger names and selection tags into ordered rules that read "this supersedes this supersedes that", with syft-shipped defaults. He also named the fear driving it, a boolean flag added for every case where someone wants to express such an exclusion. I realized my PR is evidence for that fear. It is another boolean flag, and the cases that will want the next flag are already visible. This issue is about the config that comes after the flags.

So I went looking for prior art on the proposed shape, an ordered rule list over overlapping predicates. This issue is what I found. The failure modes are already catalogued. An order-free alternative also exists, and it extends the single derived source of truth that #4905 just established from the type list to precedence itself.

| | Ordered rule list (current trajectory) | Dominance (this proposal) |
|---|---|---|
| **Properties** | Per-case booleans growing into "this supersedes that" entries; meaning depends on rule order; can express any preference, including intransitive ones | Evidence attributes with preference directions plus a small non-comparability list; pairwise and order-free; can express only consistent preferences |
| **Effects** | Shadowing and correlation defects arrive with scale; ambiguous cases each need a ruling; worst case silently deletes the wrong package; eventually needs advisor tooling | Config meaning survives reordering; ambiguity defaults to keeping both; every survivor explains itself in one line; worst case keeps a duplicate |

Firewalls have run ordered rules over overlapping predicates for decades. [Al-Shaer and Hamed](https://doi.org/10.1007/978-0-387-35674-7_2) found the defects systematic enough to build a taxonomy of shadowing and generalization and correlation and redundancy. The nouns from the stream reproduce the preconditions. A selector tag matches many catalogers and a cataloger emits many types, so one package matches all three granularities at once. Write `os supersedes language` above `trust my-custom-cataloger over everything` and the second rule silently never fires for language-typed packages. Users will ship that config and file bugs about the cataloger. Diagnosing these configs needed a tool of its own, so the paper is titled "Firewall Policy Advisor".

The alternative is dominance. [The skyline operator](https://doi.org/10.1109/ICDE.2001.914855) of Börzsönyi and Kossmann and Stocker (ICDE 2001) keeps every point that no other point dominates. Dominance means at least as good on every dimension and strictly better on one. In syft the dimensions are evidence attributes packages already half-carry, and a package is removed only when a dominating rival exists within its ownership-overlap group.

Both papers speak foreign vocabulary, so this table translates their terms into syft's.

| Paper concept | In syft |
|---|---|
| Point (skyline) | Package asserted by a cataloger |
| Dimension | Evidence attribute: DB record vs lockfile vs binary heuristic, version precision, distro file claim |
| Dominates | Supersedes on every attribute, strictly on one; checkable per pair, no weights |
| Skyline (non-dominated set) | Packages that survive into the SBOM |
| Incomparable points (both kept) | Ambiguous overlap: neither package deleted |
| Firewall rule (ordered list) | `os supersedes language`, `trust cataloger X` precedence entry |
| Match predicate | Package type, cataloger name, selector tag |
| Shadowing | Broad early rule makes a user's specific rule unreachable, silently |
| Correlation | Two partially overlapping rules whose outcome depends on their order |
| Policy advisor tooling | The config linter syft would eventually need to ship |
| (no analogue: non-comparability declaration) | The binary-extracted exception list: embedded components are a different subject, so they never compete |

Three properties fall out:

1. **Order-independence.** Dominance is pairwise, so the shadowing family has nothing to attach to. The config surface becomes which attributes matter and which direction is better.
2. **Ambiguity resolves structurally.** On the stream Dan asked whether a bidirectional or ambiguous overlap case exists, and the candidates that came up were acknowledged as hand-waving. Dominance makes the question unnecessary to answer in advance, because two non-dominated packages both survive. That default matches syft's existing instinct to keep the data when unsure.
3. **The shipped behavior is already a special case.** #4905 hardwires one dominance judgment, that OS installed-file evidence dominates language discrete-unit evidence. The binary-extracted exception list is a non-comparability declaration, because the Go modules inside an OS-owned binary are a different subject than the rpm that owns the binary. The existing binary exclusion reads the same way. A dominance config would subsume both flags instead of joining them.

Dominance already runs in production at national scale. [OpenTripPlanner 2](https://docs.opentripplanner.org/en/latest/Bibliography/) computes Pareto-optimal journey sets over arrival time and transfers and generalized cost via the RAPTOR family. [Entur deploys it as Norway's national journey planner](https://medium.com/entur/opentripplanner-2-0-is-here-67a3baeb0dc6). The user-facing behavior is the one this issue proposes for SBOMs. When the fast-with-transfers journey and the slow-direct journey don't dominate each other, the app shows both. Riders resolve the ambiguity with context the system doesn't have. That is the position an SBOM consumer is in when two packages carry incomparable evidence, and the transit implementation is open source.

The UX aligns the same way, because a dominance result shows users a choice they already understand. Each survivor explains itself in one line like "fastest" or "fewest transfers". Millions of riders consume Pareto sets daily without knowing the word, while the firewall world needed an advisor tool just to explain ordered configs back to their own authors.

The cost sits in the table's first row. Ordered lists can express preferences dominance cannot, like A over B over C over A. My claim is that this surplus is the exact part users deploy by accident. Trading it away buys the worst case an SBOM tool should want, a kept duplicate instead of a silent deletion.

If this direction survives scrutiny, the future config names evidence dimensions and preference directions plus a small non-comparability list. Syft ships defaults reproducing today's binary and language exclusions, and the per-case booleans deprecate into derived special cases.

---

Notes to self (not part of the issue):

- Citations re-verified via web 2026-07-20: Börzsönyi, Kossmann & Stocker, "The Skyline Operator," ICDE 2001, pp. 421–430, doi:10.1109/ICDE.2001.914855. Al-Shaer & Hamed, "Firewall Policy Advisor for Anomaly Discovery and Rule Editing," Integrated Network Management VIII (2003), doi:10.1007/978-0-387-35674-7_2. Anomaly taxonomy confirmed: shadowing, generalization, correlation, redundancy.
- Real-world impl verified 2026-07-20: OpenTripPlanner 2 docs state RAPTOR with "true Pareto optimized results," multi-criteria via McRAPTOR; deployed by Entur (Norway national journey planner). Underlying algorithm: Delling, Pajor & Werneck, "Round-Based Public Transit Routing" (RAPTOR). If challenged, the OTP2 raptor package and its pareto-set implementation are open source and inspectable.
- Stream verified: "Live SBOM & Security Fixes: Anchore Devs Improve Syft & Grype," July 16, youtube.com/watch?v=oB0I7ePP_e0; t=510s ≈ start of the overlap discussion. Quotes "this supersedes this supersedes that" and "an ordered list of these rules" checked against the local transcript (~/Downloads/anchore-livestream-oB0I7ePP_e0.txt); the boolean-flag fear and Dan's unanswered bidirectional question likewise.
- Do NOT claim skyline matches ordered-list expressiveness; concede it and argue the surplus is the hazard.
- Strongest single line: under a partial order, two non-dominated packages both survive; ambiguity needs no advance enumeration.
- If filed, update the H26 node in ~/Documents/sweep/repo-hypotheses/anchore-syft.md with whether the one-sentence hook or this issue drove the engagement.
