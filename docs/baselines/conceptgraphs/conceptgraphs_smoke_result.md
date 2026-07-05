# ConceptGraphs Smoke Result

Status date: 2026-07-05. Result: native one-frame smoke rerun with warnings.

## Commands Run

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_conceptgraphs_smoke.ps1
python -B scripts\evaluate_results.py --benchmark docs\benchmarks\benchmark_queries_v1.json --run-dir outputs\baselines\conceptgraphs_smoke_v1
```

## Compatibility Fixes Required

- `scripts/augment_conceptgraphs_detections.py` adds `captions` and `detection_class_labels` to the native detection pickle because the pinned detection script does not emit them but the pinned mapping script requires them.
- `scripts/run_conceptgraphs_smoke.ps1` now continues past the native mapping report crash only when `pcd_semanticsplat_mapping_v1.pkl.gz` exists.

## Evidence

| Artifact | Status |
|---|---|
| Docker image | `semanticsplat-conceptgraphs:72f5962` available |
| Native detection log | `outputs/baselines/conceptgraphs_smoke_v1/native_detection.log` |
| Native mapping log | `outputs/baselines/conceptgraphs_smoke_v1/native_mapping.log` |
| Native query log | `outputs/baselines/conceptgraphs_smoke_v1/native_query.log` |
| Native result | `outputs/baselines/conceptgraphs_smoke_v1/native_results.json` |
| Canonical result | `outputs/baselines/conceptgraphs_smoke_v1/query_results/q051.json` |
| Metrics summary | `outputs/baselines/conceptgraphs_smoke_v1/metrics_summary.json` |

## Result

```text
baseline process executed = true
native outputs = 1
canonical query results = 1
schema-valid results = 1
matched object = sofa chair
native object count = 16
native query runtime = 69.8745 seconds
confidence = 0.2810319662094116
accuracy = N/A, no GT
3D IoU = N/A, no reliable GT 3D box
```

## Warning

```text
streamlined_mapping.py writes the map artifact, then exits non-zero during internal metrics report generation:
KeyError: 'Sort Key'
```

The wrapper records this warning and continues only when the expected native map artifact exists. This run is not an accuracy result because `q051` has `verification_status: missing_gt`.
