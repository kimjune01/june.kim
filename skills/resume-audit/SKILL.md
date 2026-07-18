---
name: resume-audit
description: >
  Audit a technical candidate's resume/CV by verifying its claims against the public
  contribution graph instead of taking the text at face value. Sorts every claim onto the
  self/peer/world attestation lattice, applies a cost-and-stake filter so cheap proxies
  (stars, downloads, backlinks) don't count, runs LIVE checks (GitHub, arXiv, package
  registries, CVEs), and reports two separate axes — merit (staked acceptance of the
  candidate's specific work) and attention (timestamped output) — plus a verifiability
  score in [0,1]. For technical recruiters and hiring managers. Invoke when given a
  candidate — a GitHub handle, a resume/CV, an arXiv author, a personal site — and asked
  to verify, audit, vet, or check their claims. Runs at two depths — a quick triage scan or a
  deep per-claim audit — and elicits which. Checks the provenance of a personal site or
  self-hosted resume (Internet Archive + git history) as an un-backdatable anti-tailoring
  anchor. Needs tool access (Bash/curl or WebFetch).
---

# Resume Audit

An agent verifying a CV inspects GPT-polished text. An agent verifying a contribution graph
inspects the world wide web. This skill does the second thing: it settles a candidate's
claims against receipts held by parties they cannot prompt. The prose is optimizable
against; the receipts are not.

Report what checks out and what doesn't, each with a link the recruiter can re-run. Do not
editorialize about the person.

## Depth — quick scan or deep audit; elicit it

The first move is knowing how deep to go. A recruiter triaging 200 applicants wants a *scan*;
one deciding on a finalist wants a *deep audit*. If the request doesn't say, infer from
context, and when genuinely ambiguous run the scan and offer to go deeper — never silently
spend an hour triaging, or one-line a finalist.

- **Scan (minutes).** Run any shipped warrant (Procedure step 1), compute the verifiability
  score from classification alone, spot-check one or two headline claims live, and surface the
  obvious gold and the obvious Papiermark. Output: the score, a one-line verdict, the top few
  receipts and flags. No per-atom decomposition, no recursion.
- **Deep audit (thorough).** Everything below in full: decompose every line, classify and
  cost/stake-filter each atom, verify each live, resolve peers recursively, check provenance,
  reproduce papers, ship a per-claim ledger. The depth is the point — reserve it for candidates
  worth the spend, and actually go all the way down.

Depth is a dial, not a switch: escalate mid-scan when something must be resolved (a headline
claim that won't verify, a too-good aggregate), and stop early when the scan already answers
the question.

## Report two axes — never conflate them

- **Merit** — an external bar was met: an identifiable party *paid a cost or risked a stake*
  on the candidate's *specific* work. This is gold.
- **Attention / effort** — sustained, directed, *timestamped* output (writing, published
  artifacts, a body of work). A real and verifiable signal of where the person put their
  time, and hard to fake retroactively — but it is **not** a quality claim. Label it
  attention; never launder volume into merit.

## The governing filter — cost and stake

For any *merit* signal, ask one question: **did an identifiable party pay a cost or risk a
stake on THIS candidate's SPECIFIC work?**

- **Passes (gold):** a maintainer merging your diff (review time + the repo's reputation on
  the line); a dependency on *your own* published artifact (their build breaks if yours
  does); someone building on / extending your work; a bisect-to-your-commit; your merge
  *surviving* in HEAD, not reverted.
- **Fails (proxy / vanity — exclude):** stars, a host repo's download count, backlinks,
  mentions, tribute citations. Cheap to emit, no stake — summing them measures *reach*, not
  judgment, and a candidate can farm them. More of a cheap signal is still a cheap signal.

Two gold tiers inside the filter (how *strong* the act is):

- **accepted** — a staked party *took* your work (a merge, a dependency). Gold.
- **selected / survived** — a staked party *chose* your work over real alternatives, or it
  *persisted* under competitive/adversarial pressure. **Stronger gold** — competition is the
  multiplier; you can't fake beating a rival that lost. Receipts: a duplicate PR closed "in
  favor of #yours", a leaderboard rank among submissions, a dedup'd bounty, a design chosen
  over competing proposals, code still in HEAD when a better version could have replaced it.

## Three tiers of claim — staked ≠ public

Staking and public-visibility are different axes. A signal can be staked yet not agent-
auditable. Classify every merit claim into one:

- **public-staked** — an identifiable party paid a cost / risked a stake on the candidate's
  specific work, AND it is publicly re-runnable: a merge, a graded benchmark submission, a
  merged correction, a dependency on their artifact. An agent verifies it at a distance. Gold.
- **private-staked** — an identifiable, *verifiable* party risks their reputation on the
  candidate, but the attestation is not re-runnable: a named reference, an ex-manager who'll
  take the call, a colleague willing to vouch. The *voucher* is checkable (they exist, their
  own record is real); the *content* needs a trusted channel. **Above self-attestation** —
  do NOT flatten "not publicly re-runnable" into Papiermark. Report it as private-staked,
  pending a reference check; verify the voucher, don't fabricate the vouch.
- **self-attested** — only the candidate asserts it. Papiermark.

Absence of a public-staked record is NOT absence of merit. Private/proprietary/NDA'd/
classified/hardware and most non-code work is *involuntarily illegible* to a public audit —
it reverts to private-staked (references) or the hiring manager's own evaluation. Report
"merit not publicly verifiable → requires reference-based verification," never a zero. The
audit's edge is making public-staked merit cheap to check; it does not license scoring the
publicly-invisible as merit-less.

## Contributor attribution ≠ repo attribution

Never credit a contributor with the **host repo's** aggregate reputation — its stars,
downloads, or dependents belong to the *repo*, not the individual. A one-line fix to a famous
crate does not earn that crate's usage. What *is* attributable to the candidate: the merge
event, the specific diff, and **who merged it**. The recursion rides on the *merger's* own
gold-backing (their record), never on the host repo's popularity.

## Attestation lattice (composes with the cost/stake filter)

- **world** — an objective external referee settles it (public API/registry/record). Gold
  only if it's a *staked act* (a merge, a graded benchmark submission, a confirmed CVE), not
  a vanity count.
- **peer** — a specific identifiable party with skin in the game. Resolve **recursively**: is
  that maintainer/repo itself gold-backed?
- **self** — only the candidate asserts it ("led," "passionate," private metrics). Papiermark.

## The one number — verifiability score

`verifiability = (peer + world attestable claims) / all claims`, in [0, 1] — structural, how
*audit-able* the resume is. Then the **gold fraction**: of the checkable claims, how many pass
*both* the live check *and* the cost/stake filter. A verified vanity metric is verified but
not gold.

## Procedure

1. **Run what they ship, first.** If the resume/profile carries its own re-runnable check —
   a GraphQL query, a `verify the numbers yourself` block, a receipts file — run THAT and
   treat its output as the primary oracle. NEVER override a shipped warrant with a narrower
   ad-hoc sample; a biased slice (their *newest, still-open* PRs) yields false negatives
   against an *aggregate* claim ("112 merged all-time"). Sample only to spot-check.
2. **Gather inputs**: GitHub handle, resume/CV, arXiv author, personal site, registry
   handles, employer list (from the resume itself), and any shipped verification queries.
3. **Decompose** compound lines into atomic claims; the compound inherits the *weakest* atom.
   ("Contributed to 80+ repos I don't own or work at, in 2026" → contributed-to [world],
   not-owned [world], not-an-employer-of [cross-check the resume's own employer list —
   self-referential, sound only up to that list's completeness], in-2026 [world], count>80.)
4. **Classify** each atom self / peer / world.
5. **Apply the cost/stake filter** — is the peer/world signal a *staked act* or a cheap
   proxy? Tier the staked ones accepted vs selected/survived.
6. **Verify** with live tools; never assert a verdict on a live fact without running the
   check. Can't check it now → NEED_TO_CHECK, never a guess.
7. **Resolve peer recursively** on the *merger*, not the host repo.
8. **Prefer receipts over a computed score** for the deep signals (recursion, survival,
   contested selection). They don't reduce to a clean aggregate; ship the raw receipts and
   let the auditor weight. A single "gold score" is gameable — receipts + a runnable query
   aren't.

## Live-check recipes (Bash/curl + jq, or WebFetch)

- **Merges to non-owned repos** (the gold event), aggregate & attributable:
  `gh api graphql -f query='{ x: search(query:"is:pr is:merged author:HANDLE -user:HANDLE", type:ISSUE){issueCount} }'`
- **Merge rate** (with closed-unmerged in the same query) — quality of the funnel, self-reported honestly.
- **Contested selection**: the losing rival PR / leaderboard row / dedup'd bounty — receipt-shaped, ship the link, don't try to scrape it.
- **Dependency on the candidate's OWN artifact** (not the host repo): crates.io `reverse_dependencies` / npm dependents / PyPI usage of *their* package.
- **arXiv authorship**: `curl "http://export.arxiv.org/api/query?search_query=au:AUTHOR"` — confirm the author string, not just that an id resolves.
- **CVE credit**: the CVE record / advisory names the reporter.
- **Attention ledger** (label attention, not merit): post count, cadence, topic focus, and
  timestamps from the blog's git history / frontmatter — hard to backdate, weak on quality.
- **Provenance of a personal site / self-hosted resume** (deep tier; first-seen date is cheap
  enough for a scan): check the *history*, not just the contents. The Internet Archive gives an
  UN-BACKDATABLE chain — `web.archive.org/cdx/search/cdx?url=SITE&output=json&collapse=digest`
  returns distinct-content captures with crawl timestamps the candidate does not control. A
  capture predating the posting is pre-commitment (the resume couldn't have been tailored to a
  job that didn't exist yet); a decade-deep chain is provenance no fresh account can fake. Git
  history adds the version chain and the commit-vs-application tailoring gap. The sibling
  `presume` tool does both (`presume wayback URL`, `presume verify OWNER/REPO SHA --path FILE`).
  Longevity is un-fakeable *attention* + an anti-tailoring anchor — **not** merit; don't launder
  it into quality. But depth is a bonus, not the threshold: what actually defeats tailoring is
  a version that **predates the posting**, at any depth. A *single* public, timestamped version
  committed months before the job existed is already pre-commitment — it couldn't have been
  tailored to a posting that didn't exist yet — and beats a private, per-application-tailorable
  PDF. So report shallow-but-old provenance as weak-but-real positioning, never zero. The
  disqualifier is not shallowness, it's **recency relative to the posting**: a version committed
  at application time is the tailored case (presume's `apply` flags exactly this via the commit-
  vs-application gap), no matter how it looks. Predates the posting → positioning; same-day →
  tailored. Depth only adds strength on top of an already-predating anchor.
- **Do NOT** use stars, host-repo downloads, or backlinks as merit — they fail the cost/stake filter.
- Giant repos (linux-scale) can 500 on author-filtered commit queries; fall back to PR search
  or GraphQL, and if unresolved report NEED_TO_CHECK, never a guessed verdict.

## Paper claims (if the candidate has papers/preprints)

- **Reproduce the headline number** — run the shipped artifact, confirm the abstract's figure
  falls out. Strongest; the paper's own re-runnable warrant.
- **Citation audit** — each cite: does it resolve, and does the cited work *support* the claim
  (not just exist)? The most underused check.
- **statcheck-style consistency** — recompute reported stats; confirm abstract/text match tables.
- **Claim-to-evidence mapping** — is each abstract/conclusion claim backed by a specific result?
- Not scannable: novelty (flag overlap you find, never certify originality), significance,
  and "we ran X" with no artifact (self-attested). **"Couldn't reproduce" ≠ "fabricated"** —
  NEED_TO_CHECK until the environment (deps, seed) is ruled out.

## Discipline

- **Uncheckable = untrue**, not probably-true.
- **Verifying X is not verifying Y** — a key proves identity not intent; a coauthorship proves
  the paper not the contribution share; a merge into a repo doesn't inherit the repo's fame.
- **A shipped warrant beats your improvised sample** — match the scope of the claim, not the
  convenience of your query.
- **Cost/stake, or it doesn't count** — never sum cheap pointers (stars, downloads, backlinks,
  tribute citations); count only acts where an identifiable party paid or risked something on
  the candidate's specific work, weighted higher when chosen against real alternatives.
- **Contributor ≠ repo** — never credit the individual with the host repo's aggregate.
- **Receipts over scores** — ship the raw evidence for the deep signals; a computed aggregate
  is gameable and mis-attributes.
- **Staked ≠ public; illegible ≠ merit-less** — a checkable reference from a reputable party
  is private-staked, above self-attestation; don't flatten it to Papiermark, and don't score
  a publicly-invisible candidate as zero-merit. A thin public record is an illegibility
  finding ("verify by reference"), not a merit verdict. Verify the voucher, never the vouch.
- **Every verdict ships its evidence** — the URL/query the recruiter can re-run. A verdict
  without a re-runnable check is itself Papiermark.

## Output (recruiter-facing)

Scale the output to the depth. A **scan** returns just the verifiability score, the one-line
verdict, and the top few receipts and flags — resist producing the full ledger on a triage. A
**deep audit** returns the whole structure below. Same skill, same rigor per claim checked;
the tiers differ in how many claims get checked, not in how honestly each is reported.

- **Verifiability**: X.XX  (world N · peer N · self N, of TOTAL) — how audit-able.
- **Public-staked merit (gold)** — staked acts on their specific work an agent verified,
  each with a receipt; split *accepted* (merges, dependencies) and *selected / survived*
  (chosen over rivals, persisted).
- **Private-staked** — named references / vouchers whose *own* record checks out; verify the
  voucher, flag as pending a reference call. Above Papiermark, not agent-confirmable.
- **Attention** — timestamped body of work (volume · cadence · focus), labeled *not merit*.
- **Papiermark** — self-attested claims (private metrics, credentials); take on faith or not.
- **Flagged** — claims that failed verification or couldn't be checked, each with why.
- **One line**: is this candidate's strength *publicly-staked contribution*, *privately-staked
  (reference-dependent)*, or *self-asserted output and credentials* — and note that a thin
  public record is not itself a merit verdict, only an illegibility one.
