---
name: hn
description: Filter recent Hacker News for live threads on June's topics and hand him the list. Separately, flag the rare subset where work he has already done settles a specific quoted claim, and draft that comment as a plain argument with no link to his own writing. Use when June asks to check HN or find threads worth reading or commenting on.
---

# HN: Find the Thread Where the Receipt Answers the Claim

A commenting opportunity is not a thread about a topic you write about. It is a specific claim, made by a specific person, that work you have already done bears on directly. The first kind is abundant and worthless. The second is rare, and the whole value of this skill is refusing to confuse them.

The comment carries no link to June's own writing. What the receipt buys is the right to state the finding plainly and defend it if challenged, so the output is an argument rather than a referral. Anyone reading it should get the whole value without ever learning he has a blog.

## Two outputs, and the first one is the job

**A. Topic hits.** Live threads on June's topics, whether or not an asset collides with them. This is the default deliverable and it should rarely be empty: five to fifteen on a normal day. One line each, no drafting, no gates beyond being on topic and alive. He reads the list and decides. Never suppress a topic hit because no receipt matches it, because that is his call and not the skill's.

**B. Opportunities.** The subset of A where a published receipt settles a specific quoted claim and the four gates below all hold. Default zero. Two is a good day. If a run produces five, the bar slipped and the run is wrong.

The gates in "What counts" govern **B only**. Applying them to A is the failure mode that produced a zero-item run across roughly 400 threads on 2026-07-21, several of which were squarely on topic. A is a filter; B is a recommendation to act.

## Input

`ARGUMENTS` is an optional lookback window (`24h`, `3d`; default `48h`) and optional focus (`evals`, `epistemology`). No arguments means the default sweep.

## What counts

Four gates. An item ships only if all four hold. Drop it the moment one fails and do not argue it back in.

**1. A named claim.** You can quote the sentence being answered, from the article or from a comment, with its author and permalink. "The thread is about benchmarks" is not a claim. "This benchmark shows agents can do real SWE work" is.

**2. An existing receipt.** The answer is in something already published, linkable, and re-runnable by the reader. If responding well would require new work, a fresh audit, or a number June has not already put behind a URL, the item fails. This skill never generates commitments.

**3. The comment is the argument, and carries no link.** Do not link June's own work unless someone asks. The comment states the finding in his own words and stands on whether the argument is good. This is not a test applied after drafting, it is the form: there is no URL to delete because none goes in.

The receipt has not stopped mattering, it has changed jobs. It is what makes the claim true and defensible rather than what the comment is selling. It sits in reserve, and the path to it is somebody asking. If a reply wants a source or doubts the number, that ask has been earned and the link is then the plain answer to a question, which is the only framing in which it costs nothing.

The point of a number is to be defensible, not to be impressive. First person is honest and needs no citation: "in an ablation I ran, six self-attested arms plateaued while the externally verified arm broke past" is a claim June can stand behind and defend if pressed.

**4. The thread is live.** Last comment within about 12 hours, thread under 48 hours old, not locked. A perfect comment on a dead thread is a diary entry.

Two disqualifiers that override everything: do not surface threads where June's piece merely agrees with the prevailing view, since a comment there adds nothing and reads as flag-planting; and do not surface a thread where the correct response is disagreement with a named individual's own work unless the receipt is decisive, because a half-decisive public disagreement costs more than the attention is worth.

**Check them cheapest first**, which is not the order they are numbered. Liveness is a single API call, so it goes first and it kills candidates for free. Then scan the thread for whether someone already made the point, since that is the most common way an item dies and finding it early saves the whole evaluation. Only then work out whether there is a named claim, whether an asset is decisive against it, and whether the argument is worth reading from a stranger. Running these in written order means doing the expensive reasoning on threads that were dead or answered before you started.

## Process

### 1. Load the asset list

Read `assets.md` in this skill directory. That file is the set of things June can already settle, each with the claim it answers and the URL. It is the interest model. If a thread matches a topic but no asset, there is no opportunity, only interest, and interest is not the output of this skill.

**Sync it against the blog first.** A stale asset list is invisible from inside a run: a thread whose claim only a missing asset answers never becomes a candidate at all, so the gap never shows up as a near-miss. June publishes faster than this file gets updated, so check for new posts every run.

```bash
cd /Users/junekim/Documents/june.kim/src/content/blog
python3 - <<'PY'
import os,re,glob,datetime
A=open(os.path.expanduser('~/.claude/skills/hn/assets.md')).read()
TAGS={'epistemology','methodology','cognition','coding','pageleft','reflecting','vector-space'}
cut=(datetime.date.today()-datetime.timedelta(days=60)).isoformat()
for f in sorted(glob.glob('*.md')+glob.glob('*.mdx')):
    m=re.match(r'^(\d{4}-\d{2}-\d{2})-(.+)\.(md|mdx)$',f)
    if not m or m.group(1)<cut or f'/{m.group(2)}' in A: continue
    h=open(f).read(700); t=re.search(r'^tags:\s*(.+)$',h,re.M)
    if t and {x.strip() for x in t.group(1).split(',')} & TAGS: print(m.group(1), m.group(2))
PY
```

That yields a handful, not a backlog. Read each one before deciding, and file it as Tier 1 only when a number or run **June himself produced** stands behind it. Most posts are not assets: series-internal pieces, project writeups, and reflections all fail, and "not an asset" is the common answer. Never write a row from a title, since a row with an invented or rounded number is worse than a missing row.

When a post is not an asset, record it in the "Reviewed, not assets" section with its one-line reason. The check suppresses any slug named anywhere in the file, so filing it there is what stops the same post being proposed and re-argued every run.

Beyond 60 days the same check returns hundreds of posts and stops being actionable. Treat that as a separate backlog to work through deliberately, not as part of a sweep. As of 2026-07-21 that backlog is real: roughly 140 tagged posts older than the window have never been triaged.

If a match fails only because an asset is missing, note it under "assets that would have matched" at the end of the run.

### 2. Build the candidate slate

**Fetch through the cache, never with bare `curl`.** `hnfetch.py` in this skill directory wraps Algolia with a disk cache in `/tmp/hn-cache`, ten minutes on items and thirty on searches. Within one run the same thread gets opened repeatedly, by the slate builder, by the liveness check, and by two or three subagents that happen to share a candidate, and every one of those is the same fetch. Writes are atomic, so parallel subagents reading the same thread is safe. Pass the path to subagents and tell them to use it.

```bash
python3 ~/.claude/skills/hn/hnfetch.py "https://hn.algolia.com/api/v1/items/<objectID>"
# or from Python: from hnfetch import get, item, search
```

The TTLs are short deliberately. A stale thread is the one failure this skill cannot tolerate, since gate 4 is liveness and gate 3 is whether someone already made the point, and both read the newest comments. Do not raise them to make a rerun cheaper. `--purge` drops expired entries when `/tmp` needs it.

Algolia's API needs `>` URL-encoded as `%3E` or it returns non-JSON. Compute the epoch cutoff first.

```bash
CUTOFF=$(python3 -c "import time;print(int(time.time())-48*3600)")

# front page and near-front, any topic
curl -s "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=50"

# recent stories above a floor, broad
curl -s "https://hn.algolia.com/api/v1/search_by_date?tags=story&numericFilters=points%3E20,created_at_i%3E${CUTOFF}&hitsPerPage=100"

# targeted relevance queries, one per asset cluster below
curl -s "https://hn.algolia.com/api/v1/search?query=<terms>&tags=story&numericFilters=created_at_i%3E${CUTOFF}&hitsPerPage=30"
```

Run the targeted queries against comments too (`tags=comment`), because the claim worth answering is usually in a thread whose title looks unrelated. This is the highest-yield source and the one a title-only scan misses.

**Standing query clusters.** Run all four every time, not the ones the day's front page suggests. The measurement cluster is the easy one to remember and the epistemology cluster is the easy one to skip, because its threads rarely carry a benchmark word in the title. Skipping it means sweeping the epistemology assets only through their measurement cousins, which finds contamination arguments and misses the trust argument entirely.

- *Measurement and benchmarks:* benchmark contamination, SWE-bench, eval harness, leaderboard, agent benchmark, benchmark is saturated, grader rubric, ground truth labels, training data leak, coding agent evaluation.
- *Named instruments, queried literally:* DeepSWE, Datacurve, SWE-bench Pro, SWE-bench Verified, Terminal-Bench, MirrorCode, ProgramBench, FrontierCode, plus the runners whose harnesses the audits bear on: Inspect, `metr.org`, Epoch AI, Artificial Analysis. Generic queries do not reach these.

  Query the instrument that was **audited**, never the codebase a demonstration happened to run on. Verus and Enzyme-JAX are substrates, chosen because one had a post-cutoff unsoundness and the other a declarative derivative table, and June has nothing to say about either project on its own terms. A thread about the Verus verifier is a thread about Verus. Commenting there would mean speaking as a formal-methods contributor rather than as the person who ran the ablation, which is a claim the assets do not support. On 2026-07-21 a story titled "DeepSWE – Best Benchmark for Evaluating AI Coding Agents?" never entered the slate, on the one benchmark audited twice, because no query contained the word. It was dead by the time it surfaced, which is its own lesson: these stories are low-traffic and short-lived, so a name query is the only way to catch one while it is still alive.

  Algolia matches fuzzily, so short names return near-pure noise. Bare `Verus` matched "versus" and "various" and returned zero true hits in eight; bare `METR` matched "metrics" and surfaced a story about metrics rather than the org. Use `verus-lang` and `metr.org`, and when adding a name shorter than about six characters, check what fraction of hits actually contain the literal string before trusting the query.
- *Verification and trust:* attestation, trust but verify, why should anyone trust, chain of trust, provenance signature, verify the claims, trusted source, independent verification, reproducible build, how do you know it's true, replication, sign the artifact.
- *Method and inference:* replication crisis, more rigorous methodology, statistical significance causal, feedback loop metric, A/B test, peer review broken, measure productivity developers, what counts as evidence.
- *Credentials and selection:* hiring false negatives, interview process broken, credential degree signal, gatekeeping affiliation, resume screening.
- *Open source and maintainers:* maintainer burnout, AI slop PRs, drive-by contributions, pull request ignored, review backlog, curl hackerone, contributing to open source, unpaid maintainer, my PR was closed.

Two API notes that cost a run each. Encode the query with `urllib.parse.quote`, since a bare space or slash in a `for` loop produces a filename like `c_A/B_test.json` and the write fails silently. And a story's Algolia `created_at_i` is its submission time, so check liveness against the newest comment in `items/<id>`, not against the story age.

Union the results, dedupe on `objectID`, and drop anything already in the seen store (step 5).

### 3. Triage

Cut the slate to plausible candidates on title, URL, domain, and comment count. Then fan out subagents over the survivors, batched, each holding the asset list and the four gates. A subagent's job is to reject. Instruct it that returning nothing is a correct and common result, and that it must quote the candidate claim verbatim or drop the item.

For anything that survives, pull the full thread and read it, through the cache:

```bash
python3 ~/.claude/skills/hn/hnfetch.py "https://hn.algolia.com/api/v1/items/<objectID>"
```

Read the actual comments, and read them looking for the point *before* looking for the claim. A claim that looks answerable from the title is usually already answered by comment four, and posting the fifth version of it is worse than silence. This is the single most common way a candidate dies, so spending it first is what makes the rest of the read cheap.

Two things that look like a match and are not. A commenter who reaches June's conclusion in plainer words with a concrete example has made the point, and an asset adds vocabulary rather than a distinction. And a claim invoking a human role is usually about division of labor (distinct checkers cover distinct blind spots, seniors supervise juniors) rather than about warrant, which the assets do not contradict at all. See the symmetric-standard section of `assets.md` for that test in full, and for which rung of the ladder to reach for.

Read the whole comment before judging either one. Both failure modes are invisible in the one-line quote that made you open the thread.

### 4. Draft

For each survivor, draft the comment June would post.

Register: HN, not blog and not email. Lead with the substance, not with credentials or with who you are. No "I wrote a post about this," and no URL to June's work at all. State the finding plainly, in his own words, as a person who did the work and is reporting what he found.

Say what was measured and what came out, in first person where that is what happened. Give the reader enough of the setup to judge the claim: the control that rules out the obvious alternative explanation is usually worth more than the headline number. Do not describe your own methodology as careful, rigorous, or independent, since the reader will judge that from the argument. No thread-starting rhetorical questions.

Length: three to eight sentences. If it runs longer, the material wants to be a post and this is the wrong venue.

The comment has to be worth reading by someone who will never look up who wrote it. That is the whole bar now, and the honest check is whether you would post it under a name with no blog behind it.

### 5. Record and report

Append every surfaced `objectID` to `~/Documents/sweep/hn-seen.json` with a date, so repeat runs never resurface the same thread. Create the directory if it is not there. One object keyed by `objectID`, each value carrying `date`, `result`, and a `note` naming the slug and the gate it failed, so the same near-miss is not re-litigated every run.

One exception to permanent burial. A thread read in its first hour is not the thread it will be at fifty comments, and burying it there throws away a candidate that had not been written yet. When a candidate dies young, say so in the note and allow exactly one re-read after it matures. Anything rejected on the merits at full size stays buried.

Output to the terminal, not a file. Lead with **A, the topic hits**, since that is the deliverable: one line each, giving title, permalink, points, comment count, age, and a short clause on why it is on topic. Group by cluster. Mark any that also qualify as an opportunity.

Then **B, the opportunities**, if there are any. Per item:

- title, HN permalink, points, comment count, age
- the claim, quoted, with its author
- which asset answers it and why that asset is decisive rather than merely relevant
- the drafted comment, with no link in it
- the reserve: which URL to give if someone asks for a source, so it is at hand rather than hunted for mid-thread
- the sentence in the comment most likely to draw "source?", since that is the one that has to be exactly right

Then a closing line: how many threads were scanned, how many became topic hits, and for the opportunities, how many died at each gate. Zero opportunities alongside a healthy topic list is a normal run. Zero topic hits means the queries failed, not that HN was quiet, so treat it as a bug and check the clusters.

The seen store suppresses repeats in **B only**. A topic hit may recur across runs while a thread stays alive, since a growing thread is new information.

## Calibration

The failure mode is generosity. Every gate exists because some plausible-sounding item wants through it, and the cost of a bad comment is not zero.

Removing the link removes one cost and adds another. The drive-by self-linking penalty is gone, so a marginal comment no longer risks the work by association, and the bar on *whether to post at all* relaxes a little. What replaces it is that an unlinked finding is a bare assertion, and a number stated without a source will be doubted by someone. That is the correct outcome and the design intent: the doubt is the invitation. But it means every number in a comment must be exactly right, because there is no citation absorbing the error, only June saying he measured it. A misremembered figure is now a personal claim that failed rather than a bad link.

Two gates do not relax at all. A point already made in the thread stays worthless without a link, and agreeing with the room stays worthless without a link. Those killed most of the 2026-07-21 candidates and they were never about self-promotion.

Related: this produces attention, which is not the same as demand. Attention is worth having and is how an argument travels. It is not a pipeline, and a run of good HN comments should not be read as progress on anything that requires a paying counterparty. If HN starts feeling like the only venue, that is a fact about venue inventory and not a reason to lower the bar here.
