# Reproducibility — Windows (SemanticSplat / Beyond Proximity)

Status date: 2026-07-05. Maintainer: Person 4 (Telman).

This appendix documents **commands verified or aligned with repo scripts** on Windows. Five-scene graph-vs-flat reproduction is supported via `scripts/run_graph_vs_flat.py` (Person 1, merged on `week4/integration-article-sprint`).

## Prerequisites

```powershell
cd path\to\beyond-proximity
python -m venv .venv
.\.venv\Scripts\pip install -r backend\requirements.txt
cd frontend
npm install
cd ..
```

Optional: `winget install ffmpeg` (MP4 generation in benchmark docs pipeline).

For graph-vs-flat runner only (no frontend):

```powershell
$env:PYTHONPATH = "."
python -B -m pytest -q tests\backend\test_affordance.py tests\backend\test_graph_vs_flat.py
```

## Launch demo UI (3 services)

```powershell
.\start_all.cmd
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| API | http://127.0.0.1:8000 |
| MCP | http://127.0.0.1:8001/mcp |

Scene: `default` → Set → load `ConferenceHall.ply`.

## MCP in Cursor

Create `.cursor/mcp.json` in workspace root:

```json
{
  "mcpServers": {
    "semantic-splat": {
      "url": "http://127.0.0.1:8001/mcp"
    }
  }
}
```

## Offline benchmark (legacy graph-vs-flat on `default`)

```powershell
.\run_all_docs.ps1
```

Outputs: `docs/benchmarks/benchmark_graph_vs_flat.md`, `docs/benchmark_results/*`.

Raw JSON: `docs/benchmark_results/benchmark_default.json`.

## Five-scene graph-vs-flat (primary paper evidence)

Checked-in results: `outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/`.

```powershell
$env:PYTHONPATH = "."

# v1 efficiency baseline (40 queries)
python -B scripts\run_graph_vs_flat.py --config configs\graph_vs_flat_five_scenes.yaml

# v2 with Person 2 GT (150 queries, hit@1 / hit@3) — matches Table 1 in main.tex
python -B scripts\run_graph_vs_flat.py --config configs\graph_vs_flat_v2.yaml
```

Expected console summary (v2): ~71% view savings, ~65% token savings. Outputs land under `outputs/graph_vs_flat/<run_id>/` (`metrics_summary.json`, CSV, MD).

Gate tests:

```powershell
python -B -m pytest -q tests\backend\test_affordance.py tests\backend\test_graph_vs_flat.py
```

## Week 3 stub semantic gate (five captured scenes)

```powershell
$env:PYTHONPATH = "."
python -B scripts\validate_semantic_index.py `
  --scenes backend\data\scenes\ConferenceHall-capture-pilot `
           backend\data\scenes\Museume-capture `
           backend\data\scenes\Theater-capture `
           backend\data\scenes\outdoor-drone-capture `
           backend\data\scenes\outdoor-street-capture `
  --out docs\validation\semantic_index

python -B scripts\run_experiment.py `
  --config configs\week3_replica.yaml `
  --mode stub `
  --out outputs\week3\final_stub_semantic_gate_v1
```

## Evidence notebook (Person 4)

```powershell
.\.venv\Scripts\pip install -r notebooks\requirements.txt
.\.venv\Scripts\jupyter notebook notebooks\graph_vs_flat_evidence.ipynb
```

Notebook reads only checked-in JSON; no live API calls. Part A: `default` scene. Part B: five-scene v2.

## Article PDF (LaTeX)

LaTeX is not bundled with this repo. On a machine with TeX Live or MiKTeX:

```powershell
cd papers\beyond-proximity
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

See `papers/beyond-proximity/BUILD.md` for details.

## Full test suite (sprint gate)

```powershell
$env:PYTHONPATH = "."
$env:TEMP = "$PWD\.pytest_tmp"
$env:TMP = "$PWD\.pytest_tmp"
New-Item -ItemType Directory -Force -Path $env:TEMP | Out-Null
python -B -m pytest -q
```

## What is **not** reproducible yet

| Item | Reason |
|------|--------|
| Semantic accuracy at ScanNet scale | No independent GT at scale |
| Live / cached-live VLM runs | Out of scope for sprint |
| ConceptGraphs five-scene comparison | Smoke = 1 frame only |
| Full captured-scene LFS assets | Some LFS objects 404 on remote; use `GIT_LFS_SKIP_SMUDGE=1` for code-only checkout |

## Code revision

Record `git rev-parse HEAD` in every paper table footnote when freezing results. Frozen run ID for article: `five_scene_graph_vs_flat_v2`.
