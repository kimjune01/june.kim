---
variant: post
title: "Precisely Wrong"
tags: epistemology, methodology, reflecting
---

I spent a week and almost a thousand dollars measuring the wrong thing, carefully.

The setup was a benchmark. I had a coding agent resolving 94% of a hard set of GitHub issues, against a published baseline near 58%. I did everything you are supposed to do. I preregistered. I froze the sample. I graded with the official evaluator, committed per-instance receipts, and built a failure taxonomy that separated real losses from infrastructure faults. I wrote an objections file and a for-skeptics file and answered both. The number held under every test I aimed at it.

The number was real. It was also meaningless, because my harness handed the agent the held-out tests and let it iterate until they passed. The published baseline sees the problem description and nothing else. I had measured an easier task and compared it to theirs as if the two were the same. The paper said as much on page four. I had read summaries, not the paper.

A week is the part I keep flinching at. Not an afternoon's slip at a whiteboard. Seven days end to end, watching verdicts land one at a time, the result hardening each morning into something I trusted more. Almost a thousand dollars of compute, every dollar of it spent sharpening a number I had already gotten wrong before the first run finished. The premise was free to get wrong. Everything after, I paid for in days and dollars, and all the paying did was make it look right.

There is a name for this. Kimball called it a Type III error, and Tukey put it best: an exact answer to the wrong question. Statistics is built to keep you from getting the wrong answer to your question. It has nothing to say about choosing the wrong question. Every safeguard I owned worked within the question. None could see one level down.

What I keep turning over is not that I made the error. It is that the error felt like rigor the whole way through. Three things, named separately.

The rigor made it worse. Precision and accuracy sit on different axes. Everything I built drove variance toward zero: the frozen sample, the official grader, the taxonomy, the paired statistics. None of it touched bias. The wrong premise was a fixed offset baked into the target, so the harder I measured, the more confidently I converged on a wrong number. Tight grouping, wrong bullseye. The care was real, and it was aimed at the spread, never at the center.

The skepticism failed all at once. I had two skeptic documents. Redundant safeguards help only when they fail independently, and mine did not. Every objection inherited the same unstated premise, that the comparison was valid, so the objections were correlated, and a correlated set of checks goes down together. Reliability engineers call this a common-mode failure. Three skeptics sharing one blind spot are one skeptic in three fonts.

And I could not doubt it from the inside. This is the part that stays with me. The felt sense of evidence is identical whether you measure the right question or the wrong one. The runs happened. The verdicts landed in real time. Watching the number assemble felt like witnessing truth, because I was witnessing a true result, only to a question nobody had asked. You cannot feel the difference between measuring the right thing precisely and measuring the wrong thing precisely. The phenomenology is the same on both sides, so the feeling can never be the check. A Type III error, lived from the inside, feels exactly like knowing.

Peirce had the word for what my skeptic files were doing. Paper doubt. *Let us not pretend to doubt in philosophy what we do not doubt in our hearts.* I went through the motions of doubt without doubting the load-bearing belief. Real inquiry needs a live doubt, one that puts the belief at genuine risk. A doubt whose answer you have already settled is theater, and it reads as rigor precisely because it performs every motion.

What got me out was not skepticism. I could not doubt the evidence; it felt real. A different feeling broke through. The number was too good. Too unbelievable, I wrote at the time, to run without a control. That alarm is not disbelief in what you are seeing. It is a separate sense that fires on too-clean, and it slips past the immersion exactly because it never asks you to distrust the vivid thing in front of you. Then I did the one move the immersion had made feel pointless. I closed the session and read the paper.

So the lesson is not to doubt harder. You lose that fight against vivid evidence every time, because vividness is what the error feels like. The lesson is to wire the one feeling that does get through, *this is too good*, straight to a reflex that breaks frame: stop, read the cold source, before you scale.

This is the whole reason method exists. You externalize the doubt into a ritual because the psychology will not hand it to you in a moment built to suppress it. I could not make myself feel a doubt I did not have. I can make *suspiciously clean* route to *read the source first*. The doubt I cannot summon, I replace with a step I do not have to.

The reflex is the reactive half. There is a structural half I had to learn next. I had thrown the whole harness at the benchmark at once: the agent, the held-out tests, the gate, the loop that ran until they passed, fused into a single number. Duhem and Quine named the trap decades apart. You never test one assumption in isolation, only the entire bundle, so when the bundle returns a verdict, nothing in it can tell you which part produced it. A holistic test cannot assign blame. The 94% was not unreadable because I measured it carelessly. It was underdetermined by construction, because a number from a bundle never points at the broken piece. So the structural fix is not to doubt the bundle harder. It is to stop testing bundles. Pull one part, hold the rest fixed, let the difference name the cause. When I finally did, the held-out tests accounted for the entire gap. I had been running confirmation. I needed isolation.
