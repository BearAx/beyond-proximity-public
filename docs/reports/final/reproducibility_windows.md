# Reproducibility - Windows

Status date: 2026-07-05. Maintainer: Person 4 (Telman), updated by Codex.

This appendix documents commands verified or aligned with repository scripts on
Windows. The primary paper evidence is generated without live API calls.

## Prerequisites

```powershell
cd path\to\beyond-proximity
$env:PYTHONPATH = "."
python -B -m pytest -q tests\backend\test_affordance.py tests\backend\test_graph_vs_flat.py
```

For figure export, install plotting support if the active Python lacks it:

```powershell
python -B -m pip install matplotlib
```

## Launch Demo UI

```powershell
.\start_all.cmd
```

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| API | http://127.0.0.1:8000 |
| MCP | http://127.0.0.1:8001/mcp |

## Primary Five-Scene Graph-vs-Flat Run

Checked-in results:

```text
outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/
```

Regenerate:

```powershell
$env:PYTHONPATH = "."
python -B scripts\run_graph_vs_flat.py --config configs\graph_vs_flat_v2.yaml
```

Expected current summary:

```text
queries = 150
verified-view-label queries = 125
view savings ~= 75.5%
token savings ~= 68.2%
hit@1 graph = 0.680, flat = 0.768
hit@3 graph = 0.808, flat = 0.928
```

Interpretation: current graph pruning is a cost-control result with a measured
quality trade-off under lexical stub matching.

## Ablation Study

```powershell
python -B scripts\run_graph_ablation_study.py `
  --benchmark docs\benchmarks\benchmark_queries_v2.json `
  --out outputs\graph_vs_flat\ablations_v1
```

Outputs:

```text
outputs/graph_vs_flat/ablations_v1/ablation_summary.md
outputs/graph_vs_flat/ablations_v1/ablation_summary.csv
outputs/graph_vs_flat/ablations_v1/ablation_results.json
```

## Scaling Stress Test

```powershell
python -B scripts\run_graph_scaling_study.py `
  --benchmark docs\benchmarks\benchmark_queries_v2.json `
  --out outputs\graph_vs_flat\scaling_stress_v1 `
  --multipliers 1,2,5,10 `
  --limit 60
```

This duplicates captured semantic indexes in memory. It measures query-time
scaling behavior, not public-dataset accuracy.

## Public Dataset Readiness

```powershell
python -B scripts\audit_public_dataset_readiness.py
```

Outputs:

```text
docs/datasets/public_dataset_readiness.md
docs/datasets/public_dataset_readiness.json
```

Current expected status:

```text
official Replica scenes ready = 0
ScanNet scenes ready = 0
local data/replica/pilot_scene_001 = proxy only
```

## External Baseline Smokes

Docker Desktop and an NVIDIA GPU are required.

LangSplat:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_langsplat_smoke.ps1
python -B scripts\evaluate_results.py `
  --benchmark docs\benchmarks\baseline_smoke_queries_v1.json `
  --run-dir outputs\baselines\langsplat_smoke_v1
```

ConceptGraphs:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_conceptgraphs_smoke.ps1
python -B scripts\evaluate_results.py `
  --benchmark docs\benchmarks\benchmark_queries_v1.json `
  --run-dir outputs\baselines\conceptgraphs_smoke_v1
```

Valid claim: native execution plus canonical adapter compatibility. These are
not fair five-scene baseline comparisons.

## Article PDF

```powershell
$env:PYTHONPATH = "."
python -B scripts\export_paper_figures.py `
  --run-dir outputs\graph_vs_flat\five_scene_graph_vs_flat_v2 `
  --out-dir papers\beyond-proximity\figures
cd papers\beyond-proximity
.\build_paper.cmd
```

In this Codex session, the PDF was also rebuilt with bundled Tectonic:

```powershell
python scripts\compile_latex.py C:\GitProjects\beyond-proximity\papers\beyond-proximity\main.tex `
  --compiler tectonic `
  --output-directory C:\GitProjects\beyond-proximity\papers\beyond-proximity `
  --json
```

## Full Test Suite

```powershell
$env:PYTHONPATH = "."
python -B -m pytest -q -p no:cacheprovider
```

## What Is Not Reproducible Yet

| Item | Reason |
|---|---|
| Official Replica evaluation | No official Replica scene is present locally |
| ScanNet evaluation | No extracted ScanNet scene is present locally |
| Fair LangSplat five-scene comparison | Requires converting/training compatible 3DGS assets |
| Fair ConceptGraphs five-scene comparison | Requires multi-frame native run and GT-backed adapter |
| Live / cached-live VLM runs | Out of current scope |
| 3D IoU | No independent GT boxes/masks and predicted boxes |

## Code Revision

Record `git rev-parse HEAD` in every paper table footnote when freezing results.
Frozen run ID for the current article: `five_scene_graph_vs_flat_v2`.
