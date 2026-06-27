# Canonical demo video — spec

One demo, shot once, reused everywhere. The customization goes in the per-target email framing, not in the
video. Terminal-first; the un-fakeable signal is the live regrade, not a talking head.

## The 5-minute cut

### Cold open (0:00–0:20) — result before method, so they keep watching
- On screen: "A weaker model, given an external check, fixed a bug the strongest released model couldn't."
- Stakes in a breath: contamination-free, post-cutoff (Verus #2219), so no memorization.
- No intro, no "hi I'm." The claim is the hook.

### The bug in one breath (0:20–1:00)
- Two Rust snippets side by side: identical at the `!` token, opposite correct verdicts (one unsound, one sound).
- Say the point once: a surface-token fix passes the project's own tests and is still wrong. This is why output-checking fails.

### The artifact, not you (1:00–1:30)
- Terminal, not a talking head. Show the repo tree and the one command that runs `abductor`.
- "Everything you're about to see is in this repo. You don't have to believe any of it."

### Run abductor — the mechanism (1:30–3:00)
- It enumerates a space of cases wider than one hypothesis.
- It calibrates each against the known-good baseline (the comparator the model can't author).
- The single pass/fail gate fires, answer key held outside the model's view.
- Thin narration. Let the output scroll; the tool does the talking.

### The un-fakeable moment (3:00–4:00) — this is the whole video
- Run the committed `regrade` script against the held-out oracle. Hands off the keyboard while it runs.
- On screen: the same verdict the paper reports, reproduced live, by the script, not by you.
- One line: "I didn't grade this. The script did, against an oracle I can't see. That's the point."

### The recorded search (4:00–4:30)
- Open `HYPOTHESIS_GRAPH.md` for that inquiry: typed nodes, kill edges, the trial each node replays from.
- "The reasoning persisted. A stranger replays any node instead of trusting it."

### Close — drive them to run it (4:30–5:00)
- On screen: the regrade command, the repo URL, the Zenodo DOI.
- CTA: "Don't take my word for it. Clone it, run the regrade, you'll get the same verdict in about ten minutes."
- End on the command, not your face.

## Production notes
- **Terminal-first, no webcam.** The un-fakeable signal is the live regrade.
- **One real take of the regrade.** No edit, no speed-up there, or it stops being proof. Show the wait.
- **Captions**, so it survives muted autoplay on X and the Forum.
- **Two cuts from one recording**: the full 5-min, and a 60–90s version (cold open → regrade moment → CTA)
  for social and for prepending a custom intro to top targets.

## Reuse map
- Layer 1 (be seen): embed the 60–90s cut in the Forum/LessWrong post and the X thread.
- Layer 2 (the one human): link the 5-min cut in the artifact-first email; offer a live walkthrough to top targets.
- Layer 4 (the close): link in the LTFF/Manifund/Cooperative AI applications as the inspectable artifact.

## TODO before recording
- [ ] Confirm the regrade script runs clean from a fresh clone (the demo dies if it doesn't).
- [ ] Time the regrade; if it's longer than ~60s, prep a "still running" beat rather than cutting.
- [ ] Decide the one terminal theme / font size that's legible at social-video resolution.
