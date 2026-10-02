# How does your agent know it’s done?

Bullet-point talk draft for BIOS SPHERE, Science World, Vancouver, November 2, 2026.

- **Length:** 20 minutes, including demonstration and transitions; Q&A separate.
- **Editorial direction:** Adopt GPT-6 Astra’s seven-part structure: durable inquiry is the main story; Junebot makes it concrete.
- **Central claim:** Knowledge can accumulate as a quantifiable collection of replayable claims.
- **Through-line:** Keep the procedure for finding out, including when the inquiry has not produced a verdict. The next agent can continue the work.
- **One running example:** Junebot’s public post identifiers and dated source filenames.
- **Audience takeaway:** Ask an agent to leave a scoped claim, its check, its result or reason for remaining unresolved, and what the check depends on.
- **Evidence status:** The filename mismatch and repair are documented in repository history. The receipt handoff, paused inquiry, and illustrated ledger below are proposed reconstructions, not recordings of the original agents’ behavior.

## 0:00–3:00 — Two green checks, one broken bot

- Introduce Junebot in one sentence: a chatbot that answers questions about my blog.
- Show one task: “Find this post and read it before answering.”
- Put three names on screen:
  - Public address: `/the-parts-bin`.
  - Packaged source: `2026-03-14-the-parts-bin.md`.
  - Old reader’s attempted filename: `the-parts-bin.md`.
- Reveal the old reader’s response: `(no post found for slug 'the-parts-bin')`.
- The directory used the public identifier; packaged files retained their date prefixes. The reader did not connect the two.
- Illustrate how a handoff could lose this distinction: “Links fixed.” “Deployment succeeded.” Label these as illustrative messages.
- **Say:** “The link works. The upload succeeded. What have we actually established about the bot reading the post?”
- **Visual:** One post, one reader call, one failure. Keep cloud architecture off this slide.

## 3:00–5:00 — Replace “done” with a claim

- State the thesis: **“Knowledge can accumulate as a quantifiable collection of replayable claims.”** A result becomes reusable when its grounds survive the handoff.
- Give the claim a precise scope: “This public identifier retrieves the expected source from this package using this reader version.”
- Show its check in plain language:
  - Take the identifier from the directory.
  - Invoke the packaged reader with that identifier.
  - Compare the returned body with the expected source bytes.
- Keep the package identity, reader version, expected source, and decision rule attached.
- Explain the difference from merely calling the claim falsifiable: a possible failure must be turned into a procedure another agent can actually take up.
- **Say:** “Don’t just tell the next agent what would prove you wrong. Leave it the means to check.”
- Introduce **receipt** as the claim’s record of the trial and observed result. Before execution, retain the trial as pending.
- State the scope once: retrieving the right source does not establish that the model’s eventual answer interprets it correctly.
- **Visual:** A single claim card with four labels: Claim / Inputs / Check / State.

## 5:00–8:00 — Three inquiry states

- Make the perspective shift explicit: **“Now put yourself in the receiving agent’s position: you have the report, but not package B.”** The audience has seen the historical outcome; this receiver has not independently earned it.
- Present three possible states of the inquiry:
  - The check completes and returns the expected source: **true under this check**.
  - The check completes and the source does not match, including the observed “no post found” response: **false under this check**.
  - The exact package is unavailable, or the trial has not run: **untrue**.
- **Say:** “Untrue means no verdict has been earned by this receiver. It does not mean false.”
- A missing package does not show that the reader is broken. An unrun test does not show that it works.
- Use the staged unresolved record:
  - Checked: the directory’s identifier and the local source’s name and contents, at their recorded versions.
  - Hypothesis: the packaged reader may be looking for a filename without the date.
  - Pending trial: extract the identified package, invoke the reader, compare the returned source.
  - Blocker: that package is not available to this investigator yet.
- This record gives the next investigator a place to resume. It also explains what would make another attempt possible.
- **Visual:** The same claim card in three states. An unresolved card includes the blocker and pending check, not just a question mark.

## 8:00–11:00 — Let another agent resume

- Use a short prepared recording or static walkthrough, explicitly labeled a reconstruction.
- End the first agent’s context. Give a second agent only the retained claim record and its prerequisites. The producer’s conversation is absent.
- **Say:** “I want the next agent to inherit the work, including the part we haven’t settled.”
- Make the previously missing package available.
- Execute the pending check against the old reader: the read fails to return the expected source. The previously untrue claim now has a false verdict for that version.
- Apply the historical repair: resolve the public identifier to the dated source filename.
- Run the same checking procedure on the newly identified reader R1 and package B1: it returns the expected source. This establishes a new versioned claim.
- Preserve both records. The repaired version’s pass does not overwrite the earlier version’s refutation.
- **Say:** “We didn’t have a verdict, but we had already built the way to get one.”
- Name the saved work concretely: the receiver need not rediscover the source, reconstruct the candidate explanation, or invent the test. It can replay prerequisite checks rather than repeating the original investigation.
- Do not turn that walkthrough into a measured speedup claim. It shows the information carried across the boundary.
- **Timing:** Allow at most 60–75 seconds for the recording; use the remaining time to explain the changing states.

## 11:00–14:00 — Connect the records

- The record grows beyond one claim. Draw a small graph:
  - The directory identifies this post.
  - The named package contains the expected source.
  - Old reader R0 retrieves the expected source from B — refuted.
  - Repaired reader R1 retrieves it from B1 — supported.
  - The deployed route uses that checked package.
  - The route-level retrieval check returns the expected source.
- Keep these six nodes identical to the ledger in the next section. An inquiry edge connects the old reader’s failure to the repaired candidate.
- The shared package identity connects the local check to the deployment claim. A check on package B does not establish behavior of package A.
- Distinguish the two kinds of edge:
  - **Dependency:** what a conclusion relies on.
  - **Inquiry:** how a failed hypothesis led to the next trial.
- Introduce the **hypothesis graph**: claims, their trials and states, the dependencies they use, and the path of revision.
- Change the deployment identity. Mark the affected live claims as needing fresh checks; keep historical results and independent checks intact.
- Explain concurrent inquiry briefly: agents can work on independent open nodes; dependent work waits for its required checks.
- **Say:** “The graph tells the next agent what it can reuse, what changed, and where to continue.”
- **Visual:** Build one graph incrementally. Use an outlined node for the unverified deployment claim. Do not run a live deployment on stage.

## 14:00–17:00 — Accumulation becomes inspectable

- Show an illustrative ledger with six declared claims. Explain that these are teaching records, not measured conference-demo results:
  - Directory emits this post’s public identifier — true at the named directory version.
  - Package B contains the expected source bytes — true for B.
  - Old reader R0 retrieves those bytes from B — false for R0/B.
  - Repaired reader R1 retrieves them from B1 — true for R1/B1.
  - The live route runs B1 — untrue until deployment identity is checked.
  - Retrieval through that live route returns the expected source — untrue until the route check runs.
- We can inspect and count this collection: three supported claims, one refutation, two unresolved claims, with their scopes attached.
- Those are counts of recorded claim states. Which results remain usable now also depends on their versions and dependencies.
- A refutation records something learned; an unresolved claim preserves work toward a result. Neither should disappear merely because it cannot be reported as a success.
- Address the counting objection in one sentence: **“We can count the claims in this collection; one claim is not a standard unit of understanding.”** Fix claim identity and granularity before comparing counts. Dividing a sentence or adding duplicate claims does not establish more knowledge.
- Explain the larger payoff: as people and agents contribute checked claims, the collection can grow across sessions and contributors while retaining the means to challenge its entries.
- **Say:** “The inventory can tell us what stands, what failed, and what still needs a verdict.”
- **Visual:** Six short rows beside the same graph, with versions visible but no hash strings to read aloud.

## 17:00–20:00 — Answer “done”

- Return to the opening “done” message and replace it with one claim card.
- Answer the title: **“For this task, done means the declared completion conditions have current supporting checks. Any unresolved requirement remains visible.”**
- Ask for:
  - The exact claim and its scope.
  - The inputs and procedure needed to check it.
  - The observed result, or why no verdict was obtained.
  - The dependencies that would require rechecking if they changed.
- Keep unresolved inquiries with their pending checks. Keep refutations with what they ruled out. Let checked results become premises under their stated conditions.
- Give the practical first step: choose one recurring agent task and make this record part of its completion or handoff output.
- Address “Isn’t this testing plus dependency tracking?” directly: those ingredients are familiar. The contract keeps the claim, scope, check, dependencies, and inquiry state together across handoffs, including work with no verdict yet.
- Acknowledge the boundary once: the procedure can test the wrong property. Keeping it explicit allows the next person to inspect and improve it; replay does not settle adequacy by itself.
- **Closing:** “Finish the task. Keep what lets the next agent check it—and what lets it continue.”
- **Final screen:** Links to Replayable Claims, The Hypothesis Graph, and the eventual demo artifact. Invite discussion about which recurring checks people wish their agents retained.

## Preparation notes — outside the spoken 20 minutes

- The public programme lists the talk; the exact slot remains TBC. This draft uses the requested 20-minute duration.
- Prepare one isolated, version-pinned fixture for the historical filename mismatch. The record should use the actual pre-repair and repaired reader code.
- Write the directory-to-source check before constructing the repaired fixture. Compare complete source bytes, not a nonempty answer.
- Deliberately withhold the package for the unresolved stage; label that staging clearly. Keep the existing “no post found” output as a refutation of retrieval, not an example of no verdict.
- Rehearse the handoff with a fresh context and retain its inputs and outputs. Do not claim the demonstration has happened until it has.
- Record a short fallback. The draft works with screenshots and static cards if the demo is not ready.
- Do not require cloud credentials, a production deployment, or identical generated prose. Deployment composition can be explained with package identities and an unresolved node.
- Keep detailed protocol guarantees, the atom-count example, philosophical lineage, and model-checking statistics for Q&A. Keep “untrue” and accumulation in the main talk.
- If time slips, shorten the historical repair explanation and concurrency discussion. Preserve the unresolved handoff and the accumulation section.

## Source anchors

- Public programme and audience: https://biossphere.dev/ . Talk listed as “How does your agent know it’s done?”; date November 2, 2026.
- Existing outline: `drafts/bios-sphere-talk-notes.md` (preserved).
- Directory identifier change: repository commit `99aad3c59d334a5b2c8117bd3f4d26b0b47b43ad`.
- Reader fallback repair: repository commit `40ac43f7c10a5787eb8772b689a9d792d64df00b`; its message and diff explicitly document the date-prefix mismatch.
- Actual example post: `src/content/blog/2026-03-14-the-parts-bin.md`.
- Conceptual sources: `/truth-is-buildable`, `/what-cannot-be-false-cannot-be-true`, `/local-replay-auditability`, `/verifiable-knowledge`, `/the-hypothesis-graph-semantic-memory-methodeutics`.
- Consultation: GPT-6 Astra, high reasoning, independently reviewed the local sources and earlier outline. Its opinion is recorded in `drafts/bios-sphere-astra-opinion.md`.
