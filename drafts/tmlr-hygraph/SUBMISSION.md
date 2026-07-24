# TMLR submission: The Hypothesis Graph

State as of 2026-07-20. **`main.pdf` is submission-ready** (32 pp, TMLR format, anonymized, mirror links live). Rebuild: `tectonic main.tex` (needs figure PDFs from a fresh md2arxiv run; the sty has a one-line XeTeX guard on `[T1]{fontenc}`, byte-identical under pdfLaTeX).

## Anonymization (v2, done)

- Official tmlr.sty preamble, anonymous author block (hidden until `[accepted]`/`[preprint]`)
- The four artifact repos link their existing anonymous.4open.science mirrors (same ones as the AgenticDev 2026 submission, all verified live 2026-07-20): comparator-DA10 (abductor), hymech-117E (hygraph-mechanism), weaudit-901E (swebench-pro-audit), wepro-3D87 (swebench-pro) — 24 mirror links in the PDF
- Tool renamed abductor → "comparator" throughout (matches the mirrors' scrub term and the AgenticDev naming), including inside the verus-2219-lift-mechanism figure (patched SVG copy in this dir; site SVG untouched)
- 16 remaining redactions: june.kim blog posts, personal Zenodo DOIs, sweep/swebench-verified/determinacy/md2arxiv repos (no mirrors; peripheral to the ablation)
- Verified: pdftotext + raw strings contain zero june / kimjune / abductor; 0 compile errors, 0 missing glyphs

## Waiting on

**OpenReview profile moderation** (submitted 2026-07-18 with june@june.kim, homepage + ORCID attached; up to 2 weeks). Watch the june@june.kim inbox (Namecheap PrivateEmail, not gmail).

## When the profile activates

1. openreview.net → TMLR venue → Submit, upload `main.pdf`
2. Disclosure prompts: competing interests none, IRB n/a, funding none
3. Optional pre-submit: re-verify mirrors still resolve (4open mirrors can expire)

## Camera-ready later

`\usepackage[accepted]{tmlr}`, restore author block, swap mirrors/redactions back to real links (md2arxiv regenerates the unredacted bundle any time), revert figure to the site SVG. Author guide: https://jmlr.org/tmlr/author-guide.html
