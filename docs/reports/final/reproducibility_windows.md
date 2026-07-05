# Reproducibility — Windows (SemanticSplat / Beyond Proximity)

Status date: 2026-07-01. Maintainer: Person 4.

This appendix documents **commands that were verified or aligned with repo scripts** on Windows. It does not claim full five-scene graph-vs-flat reproduction until Person 1 lands the runner.

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
.\.venv\Scripts\pip install jupyter matplotlib pandas
.\.venv\Scripts\jupyter notebook notebooks\graph_vs_flat_evidence.ipynb
```

Notebook reads only checked-in JSON; no live API calls.

## Tests (sprint gate)

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
| Graph-vs-flat on 5 captured scenes | Runner pending (Person 1) |
| Semantic accuracy metrics | No independent GT at scale |
| Live / cached-live VLM runs | Out of scope |
| ConceptGraphs five-scene comparison | Smoke = 1 frame only |
| Full captured-scene LFS assets | Some LFS objects 404 on remote; use `GIT_LFS_SKIP_SMUDGE=1` for code-only checkout |

## Code revision

Record `git rev-parse HEAD` in every paper table footnote when freezing results.
