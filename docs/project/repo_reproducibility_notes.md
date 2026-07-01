# Repository Reproducibility Notes

This document defines labels that must not be combined in reports.

| Label | Current implementation | What may be claimed | What may not be claimed |
|---|---|---|---|
| Demo mode | UI/API demonstration paths, including the keyword demo and graph-vs-flat visual artifacts. | The interface and saved demonstration behavior work as shown. | Reproducible live model evaluation or measured model accuracy. |
| Stub mode | `scripts/run_experiment.py` with `mode: stub` and `StubModelClient`. | Deterministic orchestration, schema, resume, logging, and semantic-index regression behavior. | Live VLM/LLM reasoning, model token cost, or final accuracy. |
| Live mode | Legacy provider-backed path. | Historical adapter code exists. | That live evaluation is part of the active plan. |
| Cached live mode | Legacy replay path for verified live envelopes. | Historical replay code exists. | That cached-live evaluation is part of the active plan or available without a verified live cache. |
| Simulated benchmark | `backend/query/benchmark.py`, including `simulate_graph_search` and `simulate_flat_search`; `live_session.py` currently calls the simulated graph path. | Deterministic comparison of the repository's simulation rules. | Real headless model performance. |
| Estimated latency | Existing graph-vs-flat reports model latency from call/token estimates. | A modeled estimate under the documented assumptions. | Wall-clock model latency. |
| Real measured latency | `run_experiment.py` records local wall-clock stage/query duration. In stub mode this measures local stub orchestration only. | Local elapsed time for the labeled mode and machine. | Provider/model latency in the current plan. |
| Real metrics | Metrics from schema-valid baseline/model outputs and independent GT under a valid scene geometry gate. | Only the exact measured metric with coverage and provenance. | Current stub semantic-index scores as final accuracy. |
| Unavailable metrics | `null`/`N/A` with a reason, including 3D IoU on constant-depth data. | The metric was gated correctly. | Zero, failure, or success inferred from missing evidence. |

## Reproduction Commands

Run the deterministic Week 2 and Week 3 prototypes from the repository root:

```powershell
python -B scripts\run_experiment.py --config configs\week2_replica.yaml
python -B scripts\run_experiment.py --config configs\week3_replica.yaml
```

Validate the available scene and view-selection policy:

```powershell
python -B scripts\validate_scene_geometry.py --scene backend\data\scenes\default --output docs\validation\geometry\default_geometry.json
python -B scripts\select_views_coverage_greedy.py --scene backend\data\scenes\default --k 10 20 50 100 --output docs\validation\geometry\default_view_selection.json
```

## Environment and Provenance Requirements

- Never store provider keys in configs, outputs, docs, or source control.
- Live/cached-live runs are out of scope for the next phase unless the scope is explicitly reopened.
- Preserve canonical query results, logs, run config, failure records, model cache provenance, and evaluator output per run.
- Keep generated full experiment outputs ignored unless a narrow reviewed fixture is intentionally tracked.
- A baseline smoke requires a pinned baseline revision and native output; a documentation-only adapter contract is not a smoke result.

## Current Limitations

- The UI query flow remains simulated and is not the headless provider pipeline.
- Live and cached-live are not part of the next evaluation phase.
- Baseline smokes exist for ConceptGraphs and LangSplat, but fair five-scene comparisons are not complete.
- Five capture scenes have valid RGB-D/camera inputs and executable manual semantic indexes, but no independent semantic or 3D GT is present locally.
- ScanNet ingestion and scaling are postponed beyond Week 3.
