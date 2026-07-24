# Academic Preprint Build

`main.tex` is the named-author academic/arXiv-style manuscript. It is separate
from the anonymous workshop source under `papers/twinworld/`.

## Build On Windows

From the repository root:

```powershell
papers\beyond-proximity\build_paper.cmd
```

The command regenerates all quantitative table rows and evidence figures, runs
LaTeX/BibTeX, and checks manuscript numbers against the frozen JSON results.

Run the complete Phase 9 scientific, reproducibility, and rendered-page audit:

```powershell
python -B scripts\audit_phase89_paper.py
```

## Manual Build

```powershell
$env:PYTHONPATH = "."
python -B scripts\export_academic_tables.py `
  --out-dir papers\beyond-proximity\tables
python -B scripts\export_academic_figures.py `
  --out-dir papers\beyond-proximity\figures
cd papers\beyond-proximity
pdflatex -halt-on-error -interaction=nonstopmode main.tex
bibtex main
pdflatex -halt-on-error -interaction=nonstopmode main.tex
pdflatex -halt-on-error -interaction=nonstopmode main.tex
cd ..\..
python -B scripts\check_academic_paper.py
```

The bundled Codex Tectonic runtime can compile the TeX source when a system
LaTeX installation is unavailable, but a BibTeX-capable build is preferred for
the checked release PDF.

## Evidence Boundaries

- Internal token values are deterministic serialized-context estimates.
- Semantic-model token values use the native
  `BAAI/bge-small-en-v1.5` tokenizer.
- Cursor Agent provider/model token usage remains unavailable because the
  client UI did not expose an auditable counter.
- Construction token-equivalents are canonical character counts divided by
  four per record.
- ConceptGraphs and LangSplat token values are local tokenizer counts.
- The LangSplat result is a complete native end-to-end execution on one ScanNet
  scene under the saved 3,000-iteration, 6 GB hardware-adapted profile. It is
  not a smoke test and not an eight-scene, paper-scale reproduction.
- BBQ provides dataset and metric alignment only; this release contains no
  official BBQ execution artifact.
- Licensed ScanNet and Replica raw scenes are never copied into the paper or
  project-site artifact.
- The paper uses a descriptive research title because the former working name
  collides with an existing 2025 paper. Repository-wide renaming remains a
  separate team-approval task.
