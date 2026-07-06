# ConceptGraphs Status

Status date: 2026-07-06. Status: `FULL_FIVE_SCENE_DONE_WITH_LIMITATIONS`.

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
| Full five-scene output | present with limitations | `outputs/baselines/conceptgraphs_full_v1/` |
| Full five-scene result note | present | `docs/baselines/conceptgraphs/conceptgraphs_full_result.md` |
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

This smoke is superseded by the five-scene captured-scene run below for
ConceptGraphs execution evidence. Query `q051` has `verification_status:
missing_gt`, so smoke accuracy, retrieval success, and 3D IoU are unavailable.

## Full Five-Scene Result

ConceptGraphs was run through Docker image `semanticsplat-conceptgraphs:72f5962`
over the five captured scenes and adapted to the 150-query v2 benchmark.

Observed canonical result:

```text
run_id = conceptgraphs_full_v1
canonical results = 150 / 150
schema-valid results = 150 / 150
retrieval_success = 0.7000
expected_view_hit = 0.2240
expected_node_hit = 0.0000
expected_zone_hit = 0.0000
bbox_3d_iou = N/A
```

Native map object counts:

```text
ConferenceHall-capture-pilot = 313
Museume-capture = 150
Theater-capture = 183
outdoor-street-capture = 43
outdoor-drone-capture = 0
```

The drone scene is an explicit baseline miss case: native detection/mapping
produced a saved map artifact with zero serialized objects, so all 30 drone
query outputs are `found=false`.

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

The smoke proves native ConceptGraphs execution and canonical adaptation for one
captured frame/query. The full run proves five captured-scene native execution
and canonical adaptation, but it still does not prove official Replica/ScanNet
performance, independent semantic accuracy, or 3D IoU.
