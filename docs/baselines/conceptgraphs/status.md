# ConceptGraphs Status

Status date: 2026-06-26. Status: `READY_WITH_WARNINGS`.

## Evidence

| Check | Status | Evidence |
|---|---|---|
| In-repo checkout | not used | Smoke uses Docker image `semanticsplat-conceptgraphs:72f5962` built from the official repository revision |
| External checkout | present but not required for smoke | `C:/GitProjects/baseline-deps/concept-graphs` exists; Docker image is the execution evidence |
| Conda env | not required | Smoke runs in Docker, not the missing local `conceptgraph` Conda env |
| Docker runtime | available | Docker Desktop and GPU passthrough were used for ConceptGraphs |
| Checkpoints/assets | present for smoke | `C:/GitProjects/baseline-deps/model-cache/yolov8l-world.pt`, `mobile_sam.pt`, and HF CLIP cache were used |
| Official smoke entrypoint | present | `scripts/run_conceptgraphs_smoke.ps1` |
| Native output | present | `outputs/baselines/conceptgraphs_smoke_v1/native_results.json` |
| Canonical output | present | `outputs/baselines/conceptgraphs_smoke_v1/query_results/q051.json` |
| Metrics summary | present | `outputs/baselines/conceptgraphs_smoke_v1/metrics_summary.json` |
| Canonical adapter | present | `scripts/adapt_conceptgraphs_output.py` |
| Adapter tests | present | `tests/backend/test_baseline_adapters.py` |

## Smoke Result

ConceptGraphs executed a one-frame native smoke on `ConferenceHall-capture-pilot`. The run converted one captured RGB-D frame to the ConceptGraphs Azure-style layout, ran native detection, augmented missing caption metadata required by the pinned mapping script, wrote a ConceptGraphs map, queried it with CLIP retrieval, and adapted one canonical result.

Observed canonical result:

```text
query_id = q051
mode = live
schema_valid_result_count = 1
native object count = 16
matched_object = sofa chair
confidence = 0.2810319662094116
accuracy_eligible_result_count = 0
```

This is a baseline smoke, not a fair five-scene comparison. Query `q051` has `verification_status: missing_gt`, so accuracy, retrieval success, and 3D IoU are unavailable.

Known warning: `streamlined_mapping.py` writes the map artifact and then exits non-zero while generating its internal report (`KeyError: 'Sort Key'`). The wrapper continues only when the expected native map file exists.

## Reproduction Command

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_conceptgraphs_smoke.ps1
```

Then evaluate:

```powershell
python -B scripts\evaluate_results.py `
  --benchmark docs\benchmarks\benchmark_queries_v1.json `
  --run-dir outputs\baselines\conceptgraphs_smoke_v1
```

## Remaining Gap

The smoke proves native ConceptGraphs execution and canonical adaptation for one captured frame/query. It does not prove fair multi-query or five-scene performance. That still requires running more frames/queries, resolving the internal mapping report crash cleanly, and adding independent GT.
