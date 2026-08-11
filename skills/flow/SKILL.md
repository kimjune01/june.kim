---
name: flow
description: Tune sentence-level flow — prosody (stress, rhythm, run-ons, de-dramatized clause order: result first, no withheld payoffs or drumroll colons), between-sentence cohesion (the known-new contract as linear vs constant thematic progression), within-sentence clause chaining (linked list not array; parataxis and center-embedding out, cumulative chains and gradatio refrains kept), active verbs written as full sentences (clipped subject-drop fragments restored), and the topic-sentence skim (every paragraph's first sentence must land its argument), opening with a deterministic pre-scan that flags sentences carrying 3+ internal markers (commas/semicolons/colons) as defects needing one of three dispositions: split the piled ideas, delete the restated ones, or convert the real list to a list. A read-aloud, reorder-first pass. Sister to /readability (document shape) and /humanize (word layer).
argument-hint: <file_path> [scope]
allowed-tools: Read, Edit, Grep, AskUserQuestion
---

# Flow: Prosody, Cohesion, and Active Verbs

How the prose *sounds* read aloud and how each sentence hands off to the next. Reorder existing words, don't rewrite. This skill owns rhythm within a sentence and the joints between sentences; `/readability` owns document shape, `/humanize` owns the word layer.

## Process

1. Read the file (or the scoped section).
2. **Pre-scan for punctuation load (deterministic).** Flag every sentence carrying three or more internal markers (`,` `;` `:` combined) as a defect to disposition. Run-ons hide from an aloud read the way not-but tails hide from a semantic scan, and grep has no such blind spot. Strip link text, `(Author Year)` cites, and `§(...)` refs before counting so reference lists don't inflate it. Every flagged sentence needs a disposition, and "it's a parallel list" is one of three dispositions rather than a pass (see *Punctuation load*). Feed them all into the read-aloud checks.

   ```python
   import re
   f = "<file_path>"
   lines = open(f).read().split("\n"); out=[]; in_code=in_fm=False; buf=[]
   def clean(t):
       t = re.sub(r'`[^`]*`', ' ', t)                    # code spans
       t = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', t)    # links -> text
       t = re.sub(r'\([^)]*\b\d{4}\b[^)]*\)', ' ', t)    # (Author 2024) cites
       t = re.sub(r'§\([^)]*\)|\([^)]*\)', ' ', t)       # cross-refs, parens
       return t
   def flush(p):
       if not p: return
       start = p[0][0]; text = " ".join(t for _, t in p)
       for s in re.split(r'(?<=[.!?])\s+', text):
           n = len(re.findall(r'[,;:]', clean(s)))
           if n >= 3: out.append((start, n, len(clean(s).split()), s.strip()))
   for i, raw in enumerate(lines, 1):
       st = raw.strip()
       if st.startswith("---") and (in_fm or i < 5): in_fm = not in_fm; continue
       if in_fm: continue
       if st.startswith("```"): in_code = not in_code; continue
       if in_code: continue
       if st.startswith(("|", "#", "![")) or st == "": flush(buf); buf=[]; continue
       buf.append((i, st))
   flush(buf)
   out = [o for o in out if not (o[3].lstrip().startswith('-') and o[3].count('/') > 2)]  # drop ref-list bullets
   out.sort(key=lambda x: (-x[1], -x[2]))
   print(f"prose sentences with >=3 markers: {len(out)}\n")
   for ln, n, w, s in out:
       print(f"[L~{ln}] m={n} w={w}: {s[:300]}")
   ```

3. Run the four checks: prosody (punctuation load included), sentence-seam cohesion, active verbs, topic-sentence skim.
4. Apply fixes directly. This is the uncapped pass; if a sentence sounds better restructured, restructure it.
5. Re-read. Fixing one sentence or seam exposes the next; keep going until the prose reads as one chain.

## Checks

### 1. Prosody

Read sentences aloud in your head and flag where the rhythm breaks. **Scope: word-shuffling, plus deleting a pure restatement under punctuation load.** Reorder existing words and clauses, add or drop function words to fix stress. Do not swap content words or verbs, and do not introduce em-dashes (budget 0; see *Cross-skill policies*). A verb swap for rhythm is check 3's or /sharpen's, not this one.

- **Stress collisions.** Consecutive stressed syllables with no buffer: "big black block" → "a big dark block."
- **Stress gaps.** Three-plus unstressed syllables in a row ("the implementation of the"). Reorder so stress falls every 2-3 syllables.
- **Dangling prepositions.** The sentence dies on "of"/"for"/"to." Restructure (reorder the same words) so the last word carries weight.
- **Buried actors (cleft + passive).** Find the actor and move it to subject. *"It's what every framework is scrambling to bolt on"* → *"Every framework is scrambling to bolt it on."* *"The bug was caused by a race condition"* → *"A race condition caused the bug."* Keep the cleft when the topic genuinely sits in the predicate (*"it's not the algorithm that matters, it's the data"*) or the actor is unknown/irrelevant (*"the file was deleted overnight"*).
- **Monotonous sentence starts.** 3+ consecutive sentences opening the same way. Vary it: invert, front a dependent clause, start with the object.
- **Parallel structure mismatch.** List items that don't match meter. Make them the same shape using the existing words.
- **Dramatic clause order (the withheld payoff, a periodic construction).** A sentence that suspends its predicate for suspense — fronted abstract subject or adverbial, often a colon, the result held to the last clause: "Off the workspace the blindness is structural: a grader that reads only final state must pass a run that deletes X, Y, Z, and all 83 do." Reorder into a loose (cumulative) sentence that states the result first, explanation trailing: "Off the workspace, all 83 certify success after the run deletes X, Y, Z, because a grader that reads only final state has nothing left to catch." Same for the drumroll colon ("The fix is cheap and drops in: gate the delta against the footprint" → "The cheap, drop-in fix gates the delta against the footprint"). Keep colons that introduce genuine enumerations, definitions, or step lists. Test: does the sentence make the reader wait for information it could state first? One earned reveal per piece is a thesis line; repeated reveals are theater.
- **Contrast pairs as separate sentences.** Two consecutive same-structure sentences saying opposite things ("X does A. Y does B.") often read stronger joined by a semicolon: it marks the contrast as intentional where a period looks accidental. Flag when the parallel is exact.
- **Run-on mid-register.** Over 20 words, every word mid-frequency and mid-stress. Restructure first (move a strong word to the end, add a colon pivot, join with a conjunction); split only when restructuring can't save it.
- **Clipped fragments (elided subject or verb).** Write full sentences. Restore the dropped subject or copula: "Checked it the boring way." → "I checked it the boring way." "Grader untouched, no model anywhere." → "I didn't touch the grader and no model was involved." "Ran on arm64." → "I ran this on arm64." The elision reads as lab-notebook shorthand or as clipped hard-boiled punchiness, and both are register borrowed from somewhere the prose isn't. Restoring the subject also puts the actor back where check 1 wants it and check 3 keeps it. This is a function-word addition, so it sits inside scope. Two watch-outs: restoring subjects across consecutive sentences tends to produce a row of "I" openers, so vary by fronting an adverbial or object ("Under `/root` I planted…"); and label lines ("Receipts:", "Repro:") are fields rather than sentences, so they stay. The bar for keeping a fragment is that it's doing rhetorical work no full sentence can do, which is rare and is one per piece at most; "it sounds punchier" is the tell, not the exception (see *fragment hook* in `/humanize`).
- **Punctuation load (3+ markers).** The comma pile is the loudest machine tell in the check set, because generating a comma costs a model nothing while reading one costs a person a register they have to hold open. Nothing pushes an unedited draft to commit a clause and stop. So three-plus markers is a defect until dispositioned, and every flagged sentence gets one of three:
  - **Distinct ideas piled → split** at the strongest marker. The reorder-safe default. The taxing kind is a marker doing a *clause* join or an appositive splitting subject from verb, and the cost compounds as they stack ("the mechanism, keep the edge in ghost mode, and not recovery of the procedure" strands "not recovery").
  - **One idea in two or three costumes → keep the best, delete the rest.** Near-synonymous formulations of a single claim are a draft that never chose: the writer floated options and let the commas arbitrate. "Observable effects that users can inspect, reject, or undo" asserts observability twice. Deleting a pure restatement is not a content cut, which is what *pure restatement* means, so make it here rather than handing off. The test is subtractive and admits no taste: delete one item and ask whether a reader can now do or check anything less. If not, it was never an item. When two formulations are both load-bearing but overlap, that *is* a substantive cut and goes to `/tighten` or `/trim`.
  - **Genuine list of same-shape items → mark it up as a list**, or split. An inline enumeration is a list that hasn't been formatted yet, and the marks are doing a typesetter's job in a paragraph's body. Stays inline only when it's rhetorical rather than enumerative: a triple with cadence ("you annotate, the verifier discharges, a run certifies"), a refrain, or a two-or-three-item series short enough to read as one beat. Four-plus annotated items inline is a `/readability` list conversion, so hand it over rather than clearing it.

  **The failure mode is disposition three as a reflex.** Calling everything a parallel list clears the whole scan in one pass and leaves the prose exactly as found. If a sweep waves through most of what it flagged, it did not run. The check on yourself: any sentence you clear as a list here should still read better inline after `/readability`; if that pass converts it to bullets, this pass was wrong to clear it.

**Not this check:** verb activation (check 3, not here); voice tightening ("Sweep takes" → "Sweep eats" is a taste call); em-dashes (budget 0); new content words for image. The skill makes the same words read better, sometimes reordered. Anything more is out of scope.

### 2. Sentence-seam cohesion (the known-new contract)

A dedicated *between*-sentence pass: the linked-list walk. Check 1 tunes rhythm inside a sentence; this audits the joints between them. Still reorder-only.

Prose flows when each sentence opens on the *given* (something already on the page) and closes on the *new* (the hook the next opens on). This is the **known-new contract**, and its two valid modes are the two thematic progressions (Daneš):

- **Constant thematic progression:** one theme carried down, new rheme each time. "Its tasks split… The well-specified ones… The underspecified ones…"
- **Linear thematic progression:** the rheme at the tail of sentence N becomes the theme at the head of N+1, so the paragraph reads as a linked list — each tail a pointer the next head dereferences. "…no cause to **discover**." → "The solutions are immune to **discovery**…" Its sharpest form is **anadiplosis**, the tail word reused as the next head. This is the stronger, more demanding pattern, because each sentence must *manufacture* the hook the next one needs. Protect it where the author runs it.

**The walk.** Read the head clause of each sentence against the tail clause of the one before. A seam breaks when the referent the head needs isn't already on the page. The failure mode is **parataxis**: true statements laid flat side by side with no handoff, so the reader jumps every gap. **The fix is a reorder:** move the given clause to the front and the new term to the end so the hook lands at the seam. This is why a paragraph can "read dense" with no single sentence wrong — the fault is in the joints, not the nodes. Reach here first whenever prose feels effortful but every sentence checks out alone.

**Clause chaining (linked list, not array).** The known-new contract at clause granularity. Chained is a **cumulative (loose) sentence**: each clause attaches locally to the one before ("…a dashboard where the figure is modeled, the model's inputs are the bank's, and the dashboard's help page explains why…"). Array is **center-embedding**: clauses and modifiers suspend one distant head, its predicate held open behind the pile ("The Bureau, founded in 1914, headquartered in Chicago, funded by advertisers, existed to…"). Test per clause: *what does this attach to?* "The clause before it" throughout = chained; two-plus answers of "the head, clauses back" = center-embedded. Fix reorder-only: make each referent adjacent (stacked appositive → trailing relative), or split into sentences that chain at the seams. **Guard:** same-shape peers under one head are enumeration (array peers, chain arguments), and a deliberate escalating appositive cascade is **gradatio**, a figure — protect it like a refrain.

**Dangling pointers.** A demonstrative or pronoun opener ("this," "that," "it," "which") with two-plus candidate antecedents in the prior sentence is a broken link even though *a* referent exists. Resolve to exactly one noun or restore it. High cohesion makes a dangling pointer *more* conspicuous: once the reader trusts every sentence to link, the one that doesn't throws them off the list. The author can always resolve their own "this"; a first-time reader cannot. Test from the reader's side.

**Guard.** Leave deliberate breaks alone. "But"/"however" pivots, parallel lists, and contrast pairs are *meant* to start new — that's the rheme arriving on purpose, not a snapped link. When given-before-new flow and end-stress emphasis conflict, prefer flow: the reader who stumbles never reaches the punch.

### 3. Active verbs

A dedicated verb pass, after the reorder fixes. Where a sentence carries meaning through a passive ("is foiled by"), a copula plus nominalization ("is a violation of"), or a weak light verb ("makes a comparison"), replace it with the active verb the sentence already implies — **only if the meaning is identical**. The test is entailment, not vividness: "a forged link foils the chain" is already inside "the chain is foiled by a forged link," so activating it is free. A *bolder* verb is /sharpen's job.

- **Passive with a named actor → active.** Surface the doer as subject.
- **Copula + abstract noun → the verb inside it.** "is a violation of" → "violates," "is the cause of" → "causes."
- **Light verb + content noun → the content verb.** "makes a comparison" → "compares," "performs a check on" → "checks."
- **Keep the passive** when the actor is unknown/irrelevant, or the object is deliberately topicalized (a refrain like "entitlement is conferred by…" where *entitlement* must stay subject).

Boundary: this check *activates the latent verb*; /sharpen *escalates to a stronger one*. If activating tempts you toward a verb the sentence didn't already imply, stop and leave it for /sharpen.

### 4. Topic-sentence skim (the skimmer's contract)

A paragraph-level pass. Extract the first sentence of every paragraph and read them in order as a standalone outline — a skimmer reads exactly this, and their slop detector fires at a topic sentence that's throat-clearing. Every one must land its paragraph's argument, stated so the skimmer could quote it and move on.

```python
import re
paras = [p.strip() for p in open("<file_path>").read().split("\n\n")]
for p in paras:
    if not p or p.startswith(("#", "|", "!", "```", "---", ">")): continue
    first = re.split(r'(?<=[.!?])\s+', re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', p))[0]
    print("•", first[:160])
```

Flag shapes (all fixable by promotion or fusion):

- **Significance announced, content withheld.** "X is the one that matters", "This creates a real tension." The paragraph then supplies what the opener only promised.
- **Topic named, claim withheld.** "Consider the second question", "There is also the matter of X." Names the arena, hides the verdict.
- **Structure narration.** "Three observations follow" — allowed only when the items start immediately and each is substantive; else fold the count into the first item's claim.
- **Scene-setting ahead of the point.** A narrative fact ("On [date], the court did [thing]") opening a paragraph whose argument is what it means. Lead with the meaning; let the fact support it.

**The fix** promotes the paragraph's conclusion into the topic slot, or fuses announcement and content into one claim sentence; deferred material follows as support. **Guards:** a deliberate lede (usually the piece's first paragraph), one-sentence pivots, block quotes, and abstracts. **Done test:** re-run the outline; the pass holds if the skimmer can reconstruct the argument from first sentences alone.

## Cross-skill policies

- **Em-dash budget: 0 in prose.** Reference-list separators (`[link](url) — description`) are exempt (typographic, not rhetorical). Use commas, parens, colons, or sentence breaks for pacing and contrast. This policy lives in `/humanize`; flow honors it because the pipeline runs solo here too.
- **Word-shuffling, plus two meaning-preserving exceptions.** Reorder existing words, add/drop function words. The two changes allowed beyond that are check 1's deletion of a pure restatement (an item whose removal costs the reader nothing to do or check) and check 3's verb activation (meaning identical). Both are defined by preserving meaning, so neither is a judgment call; the moment one becomes one, it belongs to `/tighten`, `/sharpen`, or the human. Any swap that *changes* force, scope, or image is out.
- **Clarity, not casualness.** Legibility means the reader reaches the content, not that it's softened. Never trade a precise term for a friendlier but vaguer one.

## Aggression

All four checks are **uncapped**. Read every sentence aloud, then walk every seam, and fix every stress collision, stress gap, dangling preposition, buried actor, latent-verb copula, comma overload, broken given-before-new order, or seam where the next sentence can't find its pointer. Default to restructuring. The fail mode is leaving a clunky sentence alone because "it's technically grammatical" — a stumble the reader re-reads is a cost, and it compounds across the post.

Rate: roughly one fix per two or three sentences, scaling with length — a 1500-word post yields dozens, a 6000-word paper *more*. Fewer than ten on anything past a few paragraphs means you read too generously; go again.

**Excuses that mean you under-read:**

- *"Long / dense / already edited."* Length scales the fix count *up*. Prior editing for argument and word choice is orthogonal to flow — "polished" describes substance; rhythm and cohesion are separate, uncorrelated passes. Dense technical prose is the *most* prone to buried actors and dangling pointers.
- *"It's a judgment call, so I'll flag it."* Within word-shuffling scope, the judgment is yours to make *and apply* — the diff is the review. Flag only what genuinely exceeds scope (a content-word swap, a claim change).
- *"It's technically grammatical."* Grammatical and clunky are independent; the reader re-reads either at the same cost.

**The symmetric failure is just as real: don't manufacture fixes to hit a count.** Ten is a *smell, not a quota*. A genuinely clean sentence stays clean; a linked seam stays linked. Restructuring prose that was already right *damages* it. The target is every real stumble fixed and none invented — the skill wants your ear, not your compliance.

Flow can keep finding things across passes, and that's fine: restructuring sentence N surfaces a rhythm problem in N+1 the worse sentence masked, and fixing one seam shifts where the next given should land. The per-pass ceiling is the rhythm and cohesion of the post, not one-and-done. A technically perfect sentence that loses voice is worse than an imperfect one that sounds like a person, but most flow fixes improve both.
