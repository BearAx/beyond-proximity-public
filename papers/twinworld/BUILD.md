# Build TwinWorld anonymized PDF

From this directory:

```powershell
$env:Path = "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64;" + $env:Path
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Or from repo root after regenerating shared five-scene figures:

```powershell
$env:PYTHONPATH = "."
python -B scripts\export_paper_figures.py --out-dir papers\twinworld\figures
cd papers\twinworld
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Output: `main.pdf` (anonymous review build).

## Notes

- Template follows ECCV LNCS / `eccv.sty` review mode (line numbers, anonymous).
- `eccv.sty`, `llncs.cls`, and `splncs04.bst` match the official ECCV 2026
  author-kit repository at commit
  `da8c09c40239d5665757527e77388f4716a6564a` (verified 2026-07-14).
- `silence.sty` is a tiny local compatibility stub because the official kit does
  not vendor that CTAN dependency. The paper also compiles successfully with
  Tectonic 0.16.9.
- Replace `ID=XXXXX` only after OpenReview assigns the submission ID.
