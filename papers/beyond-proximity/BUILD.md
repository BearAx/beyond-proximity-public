# Paper PDF

Current source: `main.tex`.

Current checked PDF: `main.pdf`, rebuilt on 2026-07-05 after regenerating the
five-scene graph-vs-flat evidence and paper figures.

## Quick Build (Windows)

From repo root:

```powershell
cd papers\beyond-proximity
.\build_paper.cmd
```

Or step by step:

```powershell
cd beyond-proximity
$env:PYTHONPATH = "."
python -B scripts\export_paper_figures.py `
  --run-dir outputs\graph_vs_flat\five_scene_graph_vs_flat_v2 `
  --out-dir papers\beyond-proximity\figures
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

The Codex LaTeX plugin can also build with bundled Tectonic:

```powershell
python scripts\compile_latex.py C:\GitProjects\beyond-proximity\papers\beyond-proximity\main.tex `
  --compiler tectonic `
  --output-directory C:\GitProjects\beyond-proximity\papers\beyond-proximity `
  --json
```

## Figures Included In PDF

| File | Content |
|---|---|
| `figures/fig_five_scene_summary.pdf` | Views / tokens / runtime + hit@1 / hit@3 |
| `figures/fig_cumulative.pdf` | Cumulative input-token cost over 150 queries |
| `figures/fig_by_query_type.pdf` | Token savings by query type |
| `figures/fig_by_scene.pdf` | Per-scene view/token savings |
| `figures/fig_failure_cases.pdf` | Legacy demo case studies, if generated |

Regenerate figures only:

```powershell
python -B scripts\export_paper_figures.py `
  --run-dir outputs\graph_vs_flat\five_scene_graph_vs_flat_v2 `
  --out-dir papers\beyond-proximity\figures
```
