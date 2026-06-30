# ProgramBench critique — durable resume notes

## 1. The paper (DONE except submission links)
`/Users/junekim/Documents/june.kim/src/content/blog/2026-06-27-programbench-measures-recall.md`
Builds clean (`pnpm run build:blog`), em-dash invariant = 0. variant post-paper, autonumber.
Spine = **recall-only / identifiability**: a graded behavior is recall-only when its value is the output of a function NOT learnable from finite oracle I/O AND not in the offline stdlib; the only feasible channel is prior possession of the spec = recall, not reconstruction. "impossible" used only in controlled feasibility sense (computable != feasible; Go/reality). NOT an "impossible to pass" claim — it's construct-validity (measures recall, not reconstruction).
Sections: abstract, §claim, §setup (no-internet + no-installs + "even if you recognize…" system-prompt quote), §strengths, Terms (discoverable / brute-searchable / recall-only / benchable), identifiability section ("Why running the reference is not enough"), §asymmetry, §audit (+ §A.2.4 counter: their feasibility review audits *discoverability* not *reconstructability*), §pm (PM-analogy vs golden-grader fork + deadline reading), §contamination, §evidence (corroboration only; 79–95% lookup self-own), §claims-examined (5 claims), §examples (blake3/jp2a/zoxide), §close (+ determinism open-problem scope), §prescribe (TWO audiences: runner cites program list / maker triage rule), agent-feedable 5-way triage rule.
Appendix FILLED: Table A1 (15 recall / 185 no-witness-found / 1 unread, framed as floor), Table A2 (the 15 witnesses below), contestable-tier note. Table A3 (pinned) REMOVED — htmlq/peco flipped benchable.
ONLY remaining: `[issue link]`, `[Zenodo DOI]` (submission-time) + one final /copyedit pass.

## 2. Verified recall floor = 16 (each a real surfaced witness, hand-adjudicated)
NEW (DB batch 1, alphabet a–figlet, 31 programs): **bedtools2** — test_bamtobed_* / multicov, BAM binary codec decode (non-stdlib htslib; same class as samtools). Floor 15→16.
Batch-1 non-witnesses of note: walk = BENCHABLE (Go stdlib `image/jpeg` decodes the preview — language matters: jp2a stays recall because it's C/libjpeg, no stdlib JPEG). figlet → contestable (bundled FIGlet font glyph data, like ascii-image-converter). All else (help/error/version constants, csv ops, regex subst, bedtools interval arithmetic, chroma syntax highlight, shell completions, zip brute-force) = derivable/stdlib → no witness.
The original 15:
blake3 (test_chunk_boundary_1024_bytes_exact, b3sum vs golden); php-src (test_phpt_file[gost], GOST hash); 7zip (test_scrc_hash_functions_xxh64, XXH64); age (test_decrypt_existing, X25519/ChaCha20Poly1305/scrypt); brotli (test_binary_data_decompression); zstd (test_golden_decompression); ffmpeg (test_subtitle_to_video_conversion_basic, framemd5); sox (test_lpc10_statistical_properties, LPC10); jp2a (test_ext_width_default_palette, libjpeg); pixterm (test_webp_format_support, WebP); ditaa (test_no_shadows_flag_accepted, PNG); typst (test_emphasis_basic, PDF bytes); fasttext (test_print_sentence_vectors_basic); gdal (test_raster_info_checksum, GDALChecksumImage); samtools (test_depth_basic_output_format, BAM).
CONTESTABLE (excluded from floor): proj (projection math, tolerance tests), tinycc/quickjs/luajit (codegen/bytecode — derivable), ascii-image-converter (likely recall, witness not captured).
CONFIRMED BENCHABLE (notable, were false-positives): handlr (full MIME table = one-run constant), htmlq (panic string observable), peco (tmux snapshot observable + tmux not in image), zoxide (version byte observable), lz4/pigz/xz (roundtrip or stdlib lzma).

## 3. What's been tried (so future sessions don't repeat dead-ends)
- **Broad census** (6 shards, find-one-witness, early-exit): task IDs wgi5p09rx wybgjqnep wx66iq8gr wjptslvpo w1j7xudau w78fms3ef. DONE, but UNDER-FLAGGED (sampled tests, quit early). Outputs persist.
- **Strict re-run** (anti-over-flag): wep3500at wqm3t70om. DONE. Correctly flipped handlr/htmlq/peco to benchable.
- **Deep-28 suspect pass** (exhaustive read of codec/hash cores): wp2sa0syo wtd571mtd. DONE. Agents read whole suites but UNDER-FLAGGED 8/14 — found witnesses then talked themselves out ("input fixed→hardcode", "pre-compute the hash", "both files bundled", "tests external binary", "public/well-known"). I hand-adjudicated → the recall set.
- **Sharp anti-escape census (all 201)**: launched 3 times, killed each: (1) credits ran out, (2) DISK FULL — agents extracted FULL tarballs (incl. huge assets) into scratchpad, 19 GB; (3) tokens. Scripts cen-shard{1-6}.js.
- **Extractor pass** (subagents EXTRACT candidates, I adjudicate): ext-shard{1-6}.js over the 184 unconfirmed; launched, killed for tokens. THIS IS THE RIGHT NEXT STEP.

## 4. KEY LESSONS (durable)
- Subagents are reliable EXTRACTORS, unreliable JUDGES of recall (escape reasoning). Pattern: agents list every exact-output/golden/digest test + the algorithm; **I** adjudicate by the identifiability lens. Never trust their benchable/unbenchable verdict.
- ADJUDICATION CRITERION: recall iff the asserted value is produced by an algorithm (a) not in Python/Go/Rust stdlib or base ubuntu .so, (b) not learnable from finite I/O, (c) not a derivable structured transform (codegen/projection/language-semantics are NOT recall). The solver never sees the hidden tests and must implement generally, so "fixed input→hardcode" / "pre-compute" / "both bundled" / "public spec" are all INVALID escapes (knowing the algorithm IS the recall channel).
- The verdict is one-sided: a witness proves unbenchable; absence of a found witness does NOT prove benchable. Report "no witness found", not "benchable". Floor only grows.
- DISK-SAFE extraction (mandatory): stream only .py to stdout, never save tarballs/assets, no temp dirs, no shell vars:
  `curl -sL ".../$H.tar.gz" | tar xzO --wildcards --no-anchored '*.py' 2>/dev/null`  (filenames via `| tar tz | grep '\.py$'`).
- OPERATIONAL: subagent bash triggers CLI permission popups unless **bypass permissions is ON** (shift+tab). Turn it on before launching fleets. Use /tmp not mktemp -d. Heavy fleets burn ~3-4M tokens/shard and GBs of transfer — size accordingly.

## 4b. CRASH-PROOF AUDIT DB (current approach, replaces fragile serial)
`/Users/junekim/Documents/june.kim/.pb-audit/` (gitignored). SQLite `audit.db`, WAL.
- `programs(task PK, program, repo, commit_sha, lang, status, extracted, prior_signal)`. status ∈ settled_recall|settled_benchable|contestable|unconfirmed. extracted=1 once its suite was fully read. Keyed on TASK (the two `bat`s share program name).
- `tests(id, program, test_name, assertion, algorithm, adjudication, is_witness, source)`. adjudication ∈ unbenchable|benchable|no_witness_found|pending. **Subagents only ever write `pending`; I adjudicate by UPDATE.** is_witness=1 ⇒ proves recall-only.
- Seeded by `seed.py` (idempotent): 201 programs, 15 settled_recall (+their witness rows), 7 settled_benchable, 5 contestable, 174 unconfirmed, 179 extracted=0.
- `put.py` = recorder: an extractor agent pipes one-line JSON on stdin; parameterized inserts, WAL+busy_timeout for concurrent agents, bad input → `recorder.err` (never crashes the agent). **Each agent commits on completion → a kill loses only in-flight agents, never the batch; reruns skip extracted=1.**
- Workflow `extract-batch.js` (in scripts dir): takes a batch via `args=[{task,program,lang}]`, runs `parallel()` (failed agent → null, no retry-storm), each agent extracts disk-safe + calls put.py. Build a batch: `sqlite3 -json audit.db "SELECT task,program,lang FROM programs WHERE extracted=0 ORDER BY task LIMIT 31"`. Pass that array as the Workflow `args`.
- ADJUDICATE after a batch: read `SELECT program,test_name,assertion,algorithm FROM tests WHERE adjudication='pending'`, apply §4 criterion, `UPDATE tests SET adjudication=..., is_witness=...`; set `programs.status='settled_recall'` for any with a witness. Floor = `SELECT count(DISTINCT program) FROM tests WHERE is_witness=1` (currently 15).

## 4c. VERIFIABLE-KNOWLEDGE STANDARD (binding, per blog post 2026-06-13)
A witness is a HYPOTHESIS with a replayable kill condition, NOT my attestation. Entitlement comes from re-running, not from grading my own read. So each witness must ship re-fetchable + check each root, not be asserted.
- `witnesses` table in audit.db: program, test_name, task, branch_hash, test_file, assertion(verbatim incl. how `expected` is built), input_prov (how the graded input reaches the SOLVER), recall_channel, root_a_exact / root_b_fromalg / root_c_nostdlib / root_d_unlearnable (each = checked|declared|fail), kill_condition, retrieval_cmd, status (verified|hypothesis).
- The 4 roots: (a) assertion is exact equality; (b) `expected` is produced by the named algorithm; (c) algorithm absent from THAT language's offline stdlib (the walk killer: Go has image/jpeg); (d) not identifiable from the suite's finite I/O. Roots a–c are mechanically checkable; (d) is a DECLARED terminal witness (paper's first limitation) — own it, don't dress it as proven.
- STATUS (verify fleet wkwnt20t8 DONE, all 16 re-fetched + root-checked, 0 self-attested left). The verification split the witnesses into TWO mechanisms (a `mechanism` column on `witnesses`):
  - **RECALL FLOOR = 13** (class A, clean thesis support — asserted value = output of a PUBLISHED non-stdlib codec/hash/cipher, recallable-but-not-reconstructable): bedtools2(BAM), samtools(BAM), 7zip(xxh64), blake3, brotli, zstd, php-src(gost), age(AEAD decrypt gate), pixterm(WebP), jp2a(libjpeg), sox(LPC10), fasttext(model+inference), gdal(GDALChecksumImage). Each: root a/b/c checked, root d declared terminal. REPLAYABLE.
  - **BRITTLE-RENDER = 3** (class B, SEPARATE critique — exact byte/md5 golden on IDIOSYNCRATIC rendering, neither recallable nor reconstructable; belongs in the determinism open-problem, NOT the recall claim): ditaa(exact PNG), typst(exact PDF), ffmpeg(framemd5 of libass frames).
  - Verify lesson: subagent facts were INCOMPLETE (pixterm agent truncated before the exact `assert output==expected`; I'd have wrongly failed it). Always re-fetch the comparator/exact-assert myself. ditaa/typst/ffmpeg moved OUT of recall — counting them as recall would be the self-serving conflation the standard exists to stop.
- Paper update needed: Table A2 recall floor = 13 (was framed as 15); add bedtools2; MOVE ditaa/typst/ffmpeg into the determinism/brittle-golden discussion, not the recall table. Total unbenchable-by-reconstruction = 16.

## 4d. FULL-SWEEP GREPPABLE ADJUDICATION (all 201 extracted, DONE)
Sweep w58aq7cvs DONE (148 programs, 10.7M tok). All 201 now in DB. Adjudicated by DETERMINISTIC GREP over the DB (replayable, no agent judgment), two classes:
- **Render/font grep** (`find_render_witnesses.sh`; signature = exact-content compare vs raster/PDF binary: `read_bytes()==`, `framemd5`, `==…\.{png,pdf,ppm,…}`, `hexdigest()==`, minus `-o out.png` filename noise). Across all 201 → NO new witnesses. codesnap/svgbob/ascii-image-converter/caesium-clt/mdbook/html-to-markdown all BENCHABLE (no exact-pixel assert — authors avoided it). Font-render witness class = just typst/ditaa/ffmpeg. Font lesson: exact text-render is benchable ONLY if the font is HANDED to the program at runtime (figlet: standard.flf is input) AND the renderer is documented; embedded font (typst NCM) or idiosyncratic rasterizer (ditaa/ffmpeg) ⇒ witness. You cannot discover a typeface from finite renders.
- **Codec/hash/cipher grep** over the 148-program pending set → TWO new recall witnesses: **dsq** (test_parquet_type_preservation `==58655724`; test_avro_union_type_handling `=='{"long":...}'` — exact decoded values from non-stdlib Go parquet/avro) and **ov** (test_zstd_decompression `screen==zstd_display.golden` — zstd decode required, consistent w/ zstd=recall). Verified + recorded in `witnesses`. Others benchable (caesium magic-byte header; monolith base64 data-URI).

## FINAL TALLY (verified, replayable)
- **RECALL FLOOR = 15**: bedtools2, 7zip, age, blake3, brotli, fasttext, gdal, jp2a, php-src, pixterm, samtools, sox, zstd, dsq, ov.
- bundled_font_data = 1 (typst); brittle_render = 2 (ditaa, ffmpeg). TOTAL unbenchable-by-reconstruction = 18.
- Paper: Table A2 = 15 recall (add bedtools2, dsq, ov; drop ditaa/typst/ffmpeg→determinism section). The 13→15 came from the full sweep; ffmpeg/ditaa/typst stay OUT of recall.
- Subagents EXTRACT replayable coordinates (branch_hash + test_file + verbatim expected-line), never verdicts. extract-batch.js prompt updated to demand provenance. The running sweep (w58aq7cvs) used the OLD prompt → backfill the coordinate per surfaced witness via re-fetch.

## 4e. COMPLETE RAW INVENTORY (fixes the lossiness; 18 was a 5%-sample artifact)
The `tests` table held only ~12k extractor-SELECTED candidates of 248,853 total — a lossy 5% slice. `raw_sweep.py` re-read EVERY raw test body → `raw_assertions` table = **92,524 exact-output assertions** (program, task, branch, file, line, assertion, bin_exts). Exact-output asserts are the only recall-eligible tests, so this is the complete relevant denominator. Resumable/crash-safe; replayable (pure regex). `raw_swept` tracks per-task counts.
Adjudicating the BINARY-FORMAT class over the complete inventory added 4 recall witnesses beyond the 15:
- **parqeye** (TUI screen golden of bundled .parquet → parquet decode, non-stdlib Rust)
- **elfcat** (`html==sections32.golden.html` → ELF binary-layout decode, non-stdlib Rust; same class as BAM)
- **chafa** (ANSI render golden of decoded image → C has NO stdlib image decode at all, like jp2a)
- **duckdb** (`import_parquet_missing.golden` → Parquet decode, non-stdlib)
NOT clean recall (contestable): pandoc (.docx = stdlib-zip + derivable OOXML-XML, not opaque binary); tree-sitter (.wasm.golden = compiler codegen, brittle like tinycc). Benchable false-alarms: trdsql/miller/lightningcss (compressed-fixture exts were noise, no format-specific exact assert).

## 4f. LITERAL-MATCH REGEX + COMPLETE INVENTORY (the audit backbone)
The recall-eligible denominator = LITERAL-MATCH assertions (exact `==` to a literal/golden/fixture), vs BENCH (substring/returncode/len/membership/`!=`/`== <int>` = benchable by construction). Validated regex in `litmatch_sweep.py` (LIT positive + BENCH negative). `litmatch` table = **135,740 LIT asserts** across all 201 (vs the lossy 12k extractor sample, ~11x). `lit_swept` = per-task LIT/BENCH counts. Recall witnesses = the SUBSET of LIT whose value needs a non-recoverable function. All adjudication now MECHANICAL (SQL/regex over litmatch+raw_assertions; no LLM/fleets — token-saving).
Mechanical class passes: codec/binary (added parqeye/elfcat/chafa/duckdb/dsq/ov), compression — **lz4 CORRECTED benchable→RECALL** (golden-decompress; no lz4 in Python/Go/Rust stdlib; the clean line = Python stdlib has zlib/gzip/bz2/lzma so gzip/bz2/XZ benchable, but zstd/lz4/brotli/snappy NOT stdlib = recall). Hash + crypto passes: NO new witnesses (all false positives: PNG magic, fn-signatures, fixture JWT) — confirms codec pass was complete.

## 4h. DISPLAY-WIDTH CLASS confirmed by search (floor 20→21)
Fetched the goldens for the contestable Unicode-width class. **csview = RECALL** (test_cjk_emoji_with_padding: box-aligned CSV table pads CJK + emoji to 2 display columns; golden depends on the East Asian Width + emoji-width table; Rust has no stdlib display-width, glibc wcwidth disagrees on emoji). Added to Table A2. REFUTED (benchable, reverted to unconfirmed): tuc (emoji_char_1 input is single-codepoint emoji → Rust `.chars().nth(0)` suffices, no grapheme table), solar (--diagnostic-width 80 truncates ASCII → plain column count), fzf/fx (matching/base64/JSON, not width). LESSON: width class is NARROW — only CJK/emoji COLUMN-ALIGNERS (csview-style) are recall; char-cutting and ASCII-truncation pass with stdlib. Discriminator confirmed by reading goldens, not assumed.

## 4i. FORMAT-CLASS SWEEP = DRY (checked, recorded so runners don't repeat)
Grepped litmatch for protobuf/msgpack/cbor/sqlite-file/ml-model/font/jvm/wasm/pcap among unadjudicated programs. NO new witnesses:
- sqlite-file (sqlite, atlas, gdu, tui-journal, trdsql): BENCHABLE — Python stdlib `sqlite3` reads a bundled .db (same line as xz/lzma).
- font (lightningcss, mdbook, monolith, hashcards): BENCHABLE — fonts are CSS data-URI / file passthrough / stub fixtures (hashcards asserts literal `b'PNG data\n'`), not glyph-rendered (contrast typst, which embeds + renders).
- jvm/.class, ml-model/.npy, pcap: NOISE — test-data files scanned/counted by linters/searchers (rumdl, ast-grep, gron, onefetch, ctags, bat), not decoded.
- wasm (tree-sitter): already contestable (codegen).
LESSON (confirmed again): tempting format classes mostly don't yield on inspection; clean witnesses are codec/hash/cipher/opaque-binary-decode + the one width-table case. Floor stays 21.

## FINAL AUDIT TALLY (all 201, mechanical, replayable)
- **RECALL FLOOR = 21** (csview added): bedtools2,7zip,age,blake3,brotli,fasttext,gdal,jp2a,php-src,pixterm,samtools,sox,zstd,dsq,ov,parqeye,elfcat,chafa,duckdb,lz4.
- bundled_font_data = 1 (typst); brittle_render = 2 (ditaa,ffmpeg). **TOTAL VERIFIED UNBENCHABLE = 23.**
- CONTESTABLE = 11 (proj,tinycc,quickjs,luajit,ascii-image-converter,pandoc,tree-sitter + Unicode-width/grapheme class: solar,fx,csview,tuc,fzf,pipr,ov — non-stdlib Rust/Go width table, can't confirm mechanically w/o fetching goldens).
- CONFIRMED BENCHABLE = 7 (handlr,htmlq,peco,zoxide,pigz,xz,figlet); the rest = no-witness-found.
- Paper: report ≥20 recall (was 13/15), total ≥23 unbenchable, with the literal-match regex + complete inventory as the replayable method. Number limited by adjudication effort + the contestable tier, not by witnesses. 18 was a 5%-sample artifact.

## 4g. SECOND AXIS: oracle provenance / self-capturing goldens (paper §capture)
Distinct from recall (codex confirmed: keep separate axes). `capture_sweep.py` → `capture_smell` table. Finding: **29 programs** ship GRADED tests that write their own oracle from the reference run: `if not golden.exists(): golden.write_text(result.stdout)` then `assert == golden.read_text()`. 307 such lines; **12 in the conditional (`if not exists`) form = latent vacuous-pass** (passes ANY output if golden absent); **7 overlap recall witnesses** (age, bedtools2, blake3, chafa, lz4, samtools, zstd — the digest/blob IS the captured reference output). Self-capture (29) > recall floor (20): the oracle-provenance defect is the BROADER axis.
Codex review of the indictment (file PROGRAMBENCH-INDICTMENT.md): sound as measurement-validity critique; narrow per its notes — softened "no human in loop" → "no evidence of an effective per-test validation pass" (in paper); keep recall vs invalid-oracle separate; don't claim "whole bench fails" (→ conjunctive headline metric uninterpretable); taxonomy of 4 oracle kinds; codex's "defense #4" (no-internet≠no-pretraining) is self-defeating (using memorized BLAKE3 IS the recall the prompt forbids). Paper §capture + §prescribe 4th rec ADDED, builds clean.

## 5. Data sources
- HF test bodies: `programbench/ProgramBench-Tests` (public). List: `curl -s "https://huggingface.co/api/datasets/programbench/ProgramBench-Tests/tree/main/<task>/tests?recursive=true"`. Each `tests/<hash>.tar.gz` = one branch; inside, `eval/tests/*.py` + harvested `tests/*.py` = assertions.
- Task metadata: `/tmp/pb` (shallow clone of facebookresearch/ProgramBench) → `src/programbench/data/tasks/<task>/{task.yaml,tests.json}`. `/tmp/all201.json` = [{program,task,repo,commit,lang}].
- Merged prior verdicts: `/tmp/all_passes.json` (200 programs, all passes). `/tmp/bench_final.json`.
- PDF text of the paper: `/tmp/pb_paper.txt`.

## 6. What remains
1. (optional, raises floor>15) Re-run extractor pass ext-shard{1-6}.js with bypass-permissions ON; adjudicate the candidates JIT by the criterion in §4; add confirmed recall rows to Table A2 and bump Table A1 counts.
2. Final /copyedit --script pass on the paper.
3. Fill [issue link] (open a ProgramBench GitHub issue for right-of-reply) + [Zenodo DOI].

## 7. Paper facts
Meta FAIR/Stanford/Harvard, lead John Yang (johnby@meta.com), 12 authors (Synnaeve, Diyi Yang, Ofir Press). arXiv 2605.03546. 200 tasks (paper)/201 dirs. 248,853 tests, median 770, max 14,645. No-internet + no-installs (DNS blackhole; base ubuntu22.04 + Rust/Py/Go). §A.2.4 = their feasibility defense (discoverability, not reconstructability). System prompt: "even if you recognize what the executable is, you must reimplement it from behavioral observation alone." Lookup = 79–95% of flagged runs (Table 3); 20–36% tasks flagged. Build cost $3/step ~$9/task (distinct from grading cost).
