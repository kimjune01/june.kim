Target repo: https://github.com/Gloriaameng/Awesome-Agent-Harness
(post via: gh issue create -R Gloriaameng/Awesome-Agent-Harness --title "..." --body-file ...)

---

Title: A model-free determinacy audit for the V-layer "evaluation validity" open question

Body:

Thanks for the survey. The Verification-and-evaluation layer framing, turning tasks and traces into evaluation, failure attribution, and regression feedback, is the part I had been working on from the outside, and your open questions there line up with an artifact worth pointing at.

You flag the validity crisis directly: benchmark-pass diverging from real-world outcomes (the METR ~24.2pp merge-rate gap) and automated evaluation producing false negatives (OSWorld ~28%). Those are symptoms. A measurable part of the cause sits upstream of the harness, in the benchmark itself.

A determinacy audit of SWE-bench Pro: https://github.com/kimjune01/swebench-pro-audit (archived at https://doi.org/10.5281/zenodo.20738219). It classifies all 728 public Pro tasks by whether the materials a solver receives (problem statement, requirements, interface, and the repository at the base commit) determine the behavior the hidden test grades. A conservative proven floor of 15.0% is underdetermined, 11.4% of it provable by grep alone with no model in the loop: the hidden test silently resolves a spec that admits more than one faithful reading, so a correct fix scores zero. Every case is a re-runnable receipt, and the mechanical tier reproduces from gold, test, and prompt without trusting me.

Why it fits the V layer: benchmark-pass diverges from task-solved not only because the eval is noisy, but because a measurable fraction of tasks do not pin their own answer. That is a construct-validity defect, and it puts a number on the gap your survey names.

One connected point for the "compositional verification" question: a deterministic checker is feasible exactly when the task is determinate, so the determinacy rate is also the ceiling on how much of a benchmark a sound automated checker can cover. The remainder falls to an independent agent checker, fallible for the reasons your V-layer already catalogs. The two open questions meet at one measurable quantity.

Flagging in case it is useful for the V section or future work, not asking to be listed. Happy to discuss.

— June Kim, june.kim
