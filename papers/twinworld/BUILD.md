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
- TwinWorld requires official ECCV workshop formatting; if the 2026 author kit differs, swap `llncs.cls` / `eccv.sty` for the kit files before camera-ready.
- `silence.sty` here is a tiny stub to avoid a hard MiKTeX dependency; replace with the real CTAN package when available.
