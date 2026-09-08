# TEAC manuscript package

This is the review manuscript for ACM Transactions on Economics and Computation.

Build from this directory:

```sh
tectonic -k main.tex
```

`main.tex` supplies the ACM journal metadata and includes `body.tex`; the five `vcg-fig*.pdf` files are the manuscript figures. `SUBMISSION.md` contains copy-ready portal fields, and `COVER_LETTER.md` contains the proposed cover letter.

The canonical prose source remains `src/content/blog/2026-07-06-power-diagram-auction.md`. If that source changes, regenerate `body.tex` before submitting rather than editing two manuscripts independently.

Figure 1 is generated with `uv run scripts/render-vcg-surface.py` from the repository root. The standalone SVG, PDF, and PNG are written to `tmp/pdfs/vcg-surface/`; copy the approved SVG to `public/assets/vcg-fig1.svg` and PDF to this directory before rebuilding.
