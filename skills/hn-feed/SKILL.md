---
name: hn-feed
description: Poll June's Hacker News feeds, report what is new since the last run, and idempotently arm a background watch for replies to his comments. State persists in ~/Documents/sweep/ so it survives across sessions. Use when June asks what is new on HN, whether anyone replied, or to start watching a thread.
---

# HN Feed: what changed since last time

`/hn` is a sweep you run and read. This is a diff you run and forget: it answers "what arrived since I last looked," and it keeps a watch running so a reply does not sit unseen for a day.

HN has no notifications by design. dang's position is that the missing activation energy is the moderation policy, and he is right that it keeps threads calm. It also means June found a reply 28 hours late on 2026-07-21. This skill supplies the return loop without touching the part that makes HN good.

## State

Everything lives in `~/Documents/sweep/`, next to the seen store `/hn` already keeps. Create the directory if missing.

- `feed-seen.json` — entry IDs already handled, so a repeat run is quiet. One object keyed by ID, value `{"date": ..., "feed": ..., "parent": ..., "reported": true|false}`.
- `hn-feed.heartbeat` — touched by the running monitor each cycle. This is how the setup stays idempotent.

Do **not** write feed entries into `hn-seen.json`. That file records threads judged against the four gates, and mixing "I have seen this" with "I have ruled on this" destroys both meanings.

## Feeds

Verified working on 2026-07-21. Re-check before trusting one that returns nothing, since hnrss is flaky.

| purpose | endpoint | status |
|---|---|---|
| replies to June | `https://hnrss.org/replies?id=kimjune01` | works |
| story keyword search | `https://hnrss.org/newest?q=<term>` | works |
| comment keyword search | `https://hnrss.org/newcomments?q=<term>` | **502, do not use** |

Because `newcomments` is down, keyword *comment* search goes through Algolia instead:

```
https://hn.algolia.com/api/v1/search_by_date?query=<term>&tags=comment&numericFilters=created_at_i%3E<cutoff>&hitsPerPage=30
```

Keyword terms are the named instruments from `/hn`'s asset list: DeepSWE, Datacurve, SWE-bench Pro, SWE-bench Verified, Terminal-Bench, MirrorCode, ProgramBench, FrontierCode. Query the instrument that was audited, never the codebase a demonstration ran on.

## Process

### 1. Diff the feeds

Parse with `feedparser` under `uv` (no install step needed):

```bash
uv run --quiet --with feedparser python - <<'PY'
import feedparser
d = feedparser.parse("https://hnrss.org/replies?id=kimjune01")
print(d.bozo == 0, len(d.entries))
PY
```

Load `feed-seen.json`, drop entries already present, report the rest, then write the file back. Report per new entry: who, which of June's comments it answers, the full text, and the permalink. A reply is short; paste it rather than summarizing it.

**Report anything unreported, not merely anything unseen.** Presence in the store means a poller *noticed* a reply, which is not the same as June having *read* it, and conflating the two loses replies permanently. That is what happened on 2026-07-21: two replies (`48995894`, `48995578`) were detected by pollers whose stdout went into a dead session, written to the store as handled, and never shown to anyone. They surfaced a day later only because someone went looking.

So every run must sweep for `reported` falsy or missing, and re-surface those alongside the genuinely new:

```python
pending = {k: v for k, v in seen.items()
           if v.get("feed") in ("monitor", "replies") and not v.get("reported")}
```

Set `reported: true` on an entry only in the same breath as putting it in front of June, then write the file back. The monitor sets it itself, because under the `Monitor` tool its stdout genuinely reaches him. Any other path that writes to this store must set it `false` and let a run do the surfacing.

The `feed` filter matters. The store also holds June's own comment IDs and keyword-hit IDs, and those are not replies waiting to be read, so an unfiltered sweep would re-report them forever.

### 2. Arm the watch, idempotently

The poller already exists at `~/Documents/sweep/bin/hn-feed-monitor.sh`. It reads June's recent comments from Algolia, checks each one's `kids` on Firebase, writes new reply IDs into `feed-seen.json`, prints one line per reply, and touches the heartbeat every cycle. Do not rewrite it, and do not inline a copy into a heredoc. Read it, and change the file if it needs changing.

**Arm it with the `Monitor` tool, never with `nohup` or `run_in_background`.**

```
Monitor(command: "bash ~/Documents/sweep/bin/hn-feed-monitor.sh",
        description: "replies to kimjune01's HN comments",
        persistent: true)
```

This is the whole point of the skill and it is easy to get wrong. A background bash job writes its stdout into the session that launched it, and that session ends, so replies print into a dead pipe and June sees nothing until he thinks to `cat` a log. Only `Monitor` turns each stdout line into a notification that reaches him. On 2026-07-21 a correct poller had been running for hours with its output going nowhere, and the fix was the launch mechanism rather than the script. If a run leaves June with a log file to check, the run failed.

**Idempotence, and the threshold trap.** Check the heartbeat before arming so two monitors never poll at once:

```bash
HB=~/Documents/sweep/hn-feed.heartbeat
if [ -f "$HB" ] && [ $(( $(date +%s) - $(stat -f %m "$HB") )) -lt 900 ]; then
  echo "monitor already live, skipping"
fi
```

**The threshold must exceed the poll interval, or the check lies.** The script sleeps 600 seconds between touches, so a 300-second threshold reports "dead" through the back half of every single cycle, and the next run dutifully arms a duplicate. That happened on 2026-07-21. 900 gives one full cycle plus slack. Change both together if you ever change the interval.

Fresh heartbeat means a monitor is live: say so and start nothing. Stale or missing means the previous one died with its session, so arm a new one. Confirm with `pgrep -fl hn-feed-monitor` when the heartbeat and the observed behavior disagree, since a file mtime cannot distinguish a healthy poller from a crashing one that touches the heartbeat before doing its work.

**Silence must mean "no replies," never "the monitor broke."** The script prints `MONITOR ERROR` and exits when it cannot reach the comment list, because a watch that fails quietly is worse than no watch: June stops checking manually *and* stops being told. Preserve that behavior in any edit.

### 3. Draft, if a keyword hit earns it

Most runs skip this. The named-instrument queries exist to catch a thread while it is still alive, so occasionally one returns a comment that a published audit answers, and then the draft is the deliverable rather than the link.

**Gates first, and they are `/hn`'s, not looser ones.** Read the four gates and the asset list in `/hn`'s `SKILL.md` and `assets.md` before drafting anything. A keyword match is not a gate pass. The one that kills most feed hits is gate 3: benchmark threads are full of people who already distrust benchmarks, so an audit that merely joins the skepticism adds nothing. The hit is worth drafting when someone recommends or defends a specific instrument, because then the audit qualifies a live claim instead of seconding the room.

**Gate 4 needs a second clause here, because keyword search breaks its assumption.** `/hn`'s liveness gate asks whether the thread's newest comment is under 6 hours old, which works for a sweep because sweep candidates surface from active subthreads. Keyword search does the opposite by construction: it finds *old comments inside live threads*, since a matching comment stays matchable long after anyone is reading it. On 2026-07-22 the WASDx hit passed gate 4 on a thread active 0.9 hours earlier while the comment itself was 15.2 hours cold and buried under 451 others.

So require both: the thread's newest comment under 6 hours, **and** the comment being answered under 6 hours old. A reply to a cold comment in a warm thread is written for the archive, and if that is the intent then say so when reporting it rather than presenting it as a live opportunity.

**Then write it short.** The failure mode here is the wall of text, and it comes from the draft trying to do three jobs at once: state the finding, pre-empt every objection, and summarize itself at the end. Do the first one.

- **One claim per paragraph, two paragraphs at the outside.** Four sentences total is a normal length. If it runs past six, it is carrying material that belongs in a reply to a question nobody asked yet.
- **Do not pre-empt the caveat.** Scope limits, denominators, and sample enrichment are what you say when challenged, and saying them unprompted reads as flinching. They also double the length. Keep them in the reserve with the URL, so the answer is at hand when the ask comes.
- **Cut the closing summary.** A four-sentence comment does not need its own recap, and a final "so X measures A and Y measures B" sentence is the tell that the draft was written as an essay.
- **No link.** Same rule as `/hn`, for the same reason: the comment is the argument, and the receipt is what makes it defensible if someone doubts it.
- **Numbers exact, denominators exact.** With no citation absorbing the error, a wrong figure is June personally claiming something that did not happen. Check the asset row rather than recalling the number.

**Then run the flow checks over it before showing it.** A short comment stumbles the same way prose does, and these four catch nearly all of it:

- *Split at punctuation load.* Three or more internal markers in one sentence, especially chained independent clauses plus a colon, means split at the strongest joint. Let the number land in its own sentence.
- *Kill not-but tails.* "is a boolean, not a link to the graded patch" becomes two positive facts joined by *and*. Same content, no contrastive.
- *Join contrast pairs on a semicolon.* When two figures share a denominator and an exact parallel ("decisive in 3", "outside the rubric in 52"), a semicolon lands the opposition in one breath; a period makes it look like two unrelated observations.
- *Walk the seams.* Each sentence should open on something already on the page. If a topic sentence hands off to a method sentence before the claim that picks it up, reorder so the handoff is direct, which usually collapses three sentences into two.

Report the draft with the quoted claim, the asset, the reserve URL, and the one sentence most likely to draw "source?". That last one is where an exact denominator matters most.

### 4. Report

Lead with new replies, since that is the thing with a clock on it. Then new keyword hits, with any draft attached to the hit that earned it. Then one line on what is being watched and whether the monitor was already live. If nothing is new, say so in a sentence; a quiet run is the common case and is not a failure.

## Gotchas

Each of these cost a retry on 2026-07-21.

**Use absolute paths.** A pyenv shim shadowed `curl` mid-session and `command not found` came back for a command that had worked minutes earlier. `/usr/bin/curl`, or set `PATH=/usr/bin:/bin:$PATH` first.

**Firebase for anything time-sensitive.** `https://hacker-news.firebaseio.com/v0/item/<id>.json` is realtime. Algolia lags several minutes on indexing, and the first reply of the session surfaced on Firebase well before Algolia had it. Use Algolia for search, Firebase for "did this specific thing change."

**Clear the output file between curl calls.** Writing to a fixed temp path and then counting `<item>` lines reports the *previous* feed's contents when the request fails, which reads as success. `rm -f` first, or check the HTTP code before parsing.

**news.ycombinator.com rate-limits.** Scraping the HTML pages returns 429 under repeated access. The API hosts do not, so prefer them.

**`/replies` needs a login.** The URL is session-based, so without a cookie it returns "No such user." The public equivalent is `https://news.ycombinator.com/threads?id=kimjune01`.

**Never nest a heredoc inside a quoted `sh -c`.** Writing the poller inline as `sh -c '... <<"PY" ... PY'` lets the outer shell interpolate `$(...)` and `{}` before Python sees the script, and the resulting `SyntaxError` fires every cycle while the heartbeat keeps reporting healthy. This is the argument for keeping the poller in a file under `bin/` and pointing `Monitor` at the path.

**Touch the heartbeat after the work, not before.** Touching first means a poller that crashes on every cycle still looks alive to the idempotence check, which is how a broken watch survives a whole afternoon.
