# ProgramBench: an indictment of the grader. Sanity-check this.

Direct ask: is this argument sound, where does it overreach, and what is the strongest defense the authors could mount? Tell me what to cut and what to strengthen. Is "no human in the loop" a fair falsifiable claim or just ad hominem?

## The benchmark
ProgramBench (arXiv 2605.03546) gives a model a compiled, execute-only binary `B` and its docs, strips the source, and runs the container with no network. The model emits a program `P`; `P` is graded by a hidden suite `H` of generated tests, each asserting `P(x)` matches `B(x)`. The primary metric, Fully Resolved, credits a task only when `P` matches on *every* test. 200 tasks, 248,853 tests, median ~770/task. The system prompt tells the model: "even if you recognize what the executable is, you must reimplement it from behavioral observation alone."

## What a complete mechanical read of the test bodies finds (all 201 task tarballs, public on HF)
A deterministic regex classified every assertion into literal-match (exact `==` to a golden/literal, the recall-eligible set, 135,740 lines) vs benchable (substring/returncode/len/membership). Then per class:

1. **Recall floor ≥20 programs.** A graded test asserts, byte-for-byte against a bundled golden, the output of a function with no offline channel: hashes (BLAKE3, GOST, XXH64), ciphers (age = X25519+ChaCha20Poly1305+scrypt), non-stdlib compressors (zstd, brotli, lz4), codecs (LPC10, WebP, libjpeg), opaque binary formats (BAM, Parquet, Avro, ELF), embeddings (fastText). None are in the Python/Go/Rust standard library or fetchable offline. A source-blind solver cannot reconstruct them; the only channel is prior possession of the spec = recall, which the no-internet rule forbids and the prompt explicitly tries to suppress. Because Fully Resolved is conjunctive, one such test forecloses the task.

2. **Self-capturing goldens ≥14 programs (sweep ongoing).** Graded tests contain:
   `if not golden.exists(): golden.write_text(result.stdout)` then `assert result.stdout == golden.read_text()`.
   The oracle is the reference's own output, captured on first run. If the golden is bundled, the test grades byte-identity-to-the-reference (its incidental choices, not a contract). If the golden is ever absent, the test is a vacuous pass for any output. Several programs that self-capture are the same ones with recall witnesses (blake3 captures its digest golden; zstd, age, bedtools2 capture binary output).

3. **Implementation-detail pins (3+).** Exact-PDF-byte (typst), byte-exact PNG (ditaa), per-frame MD5 of generated frames (ffmpeg). Nondeterministic across builds; pins the reference's bytes, which no independent implementation reproduces. ffmpeg, the most codec-dense program, has *no* clean recall test — its codec fixtures are ffmpeg-generated then metadata-checked, and its only unreconstructable tests are framemd5 of its own pipeline.

## The argument
Two things are under test: the submitted program (the measurand, what we want to improve) and the bench (the instrument, whose determinism and validity is the question). A benchmark asks you to read the measurand and trust the instrument. Here the instrument fails calibration:

- A golden captured from the reference sets the zero-point at the reference's own output. A meter calibrated against itself measures nothing. The reference is judge and contestant; a contract-equivalent candidate that differs in incidental bytes fails, and a wrong output passes a vacuous golden.
- So Fully Resolved does not measure source-blind reconstruction (the advertised skill). On golden-gated tasks (199/201) it measures byte-identity-to-reference; on the recall subset that identity is also offline-impossible. The PM-analogy the paper offers ("query the binary like a product manager") describes a search; the grader admits exactly one answer, the reference's bytes.
- The artifacts bear no fingerprint of per-test human validation: templated "CATCHES: implementations that..." docstrings (auto-generated rationales), self-capture code left in graded tests, recall-gated tests that are unpassable under the benchmark's own no-internet rule. Each is a defect a single human read would catch. Inference: the test-generation pipeline ran without a human validating the generated oracles. Contrast SWE-bench Verified, whose "Verified" *is* a human validation pass (gold patch resolves, tests appropriate, spec sufficient).

Conclusion: the grader is invalid as a measurement instrument, independent of how good the submitted programs are. The fix is constructive and on the same team (everyone wants to know if AI writes better programs): a validation pass in the SWE-bench Verified spirit, plus mechanical repairs (roundtrip/contract oracles, observable constants, normalized comparators, recall scored on a separate track, never a self-captured golden).

## Where I might be wrong (engage these)
- "No human in the loop" infers process from artifacts; I cannot see their workflow. Is the cumulative artifact evidence enough, or is this overreach I should soften to "no evidence of a validation pass"?
- A self-captured golden can still encode a correct, even unique, output; capture provenance proves it is not a *contract*, not that it is *wrong*. Am I conflating "invalid oracle" with "wrong answer"?
- Recall (program unreconstructable) and invalid-oracle (grade uninterpretable) are different axes; is keeping them separate the right call, or does it dilute the punch?
- The benchable subset (roundtrip, observable constants) is validly measured; "the whole bench fails" may overreach. Should the claim be narrowed to "the headline metric is invalid because conjunctive scoring lets one bad test poison a task"?
