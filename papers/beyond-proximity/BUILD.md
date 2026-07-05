# Building `main.pdf`

The article source is `main.tex`. LaTeX is not required for repo development but is needed to produce the PDF.

## Windows (MiKTeX)

1. Install [MiKTeX](https://miktex.org/download) or TeX Live.
2. From repo root:

```powershell
cd papers\beyond-proximity
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Output: `main.pdf`.

## macOS / Linux

```bash
cd papers/beyond-proximity
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

## Notes

- Uses `cvpr.sty` and `refs.bib` in this directory.
- Frozen evidence run ID for Table 1: `five_scene_graph_vs_flat_v2`.
- If `bibtex` warns on arXiv-only entries, metadata is draft-quality from Person 3 matrix — verify before submission.
