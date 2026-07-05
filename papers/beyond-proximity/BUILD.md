# Paper PDF

**If your PDF still says "Beyond Proximity" with 100% room accuracy — it is stale.**  
Current source: `main.tex` → title **SemanticSplat**, with 3 figures in `figures/`.

`main.pdf` on disk is only updated when you run the build below (last manual check: old PDF from June).

## Quick build (Windows)

From repo root:

```powershell
cd papers\beyond-proximity
.\build_paper.cmd
```

Or step by step:

```powershell
cd beyond-proximity
$env:PYTHONPATH = "."
python -B scripts\export_paper_figures.py
cd papers\beyond-proximity
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Requires `pdflatex` on PATH (MiKTeX / TeX Live). If missing:

```powershell
winget install MiKTeX.MiKTeX
```

Then run `.\build_paper.cmd` again (script auto-finds MiKTeX even before terminal restart).

## Figures included in PDF

| File | Content |
|------|---------|
| `figures/fig_five_scene_summary.pdf` | Views / tokens / runtime + hit@1 / hit@3 |
| `figures/fig_by_query_type.pdf` | Token savings by query type (6 types) |
| `figures/fig_by_scene.pdf` | Views checked per scene |
| `figures/fig_default_average.pdf` | Legacy demo scene (12 queries) |

Regenerate figures only:

```powershell
python -B scripts\export_paper_figures.py
```
