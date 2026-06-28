# Week 3 Results

Status date: 2026-06-28. Final credential-independent gate complete. Live and cached-live are out of scope for the next phase.

## Final Status

| Item | Status | Evidence |
|---|---|---|
| Captured scenes | measured | 5 scenes, 96 RGB-D frames/poses with matching intrinsics |
| Manual semantic index | measured validation | 5/5 scenes, 96/96 views, 1,046 semantic items; manual, not independent ground truth |
| Stub semantic gate | measured | 40/40 available and schema-valid results, eight per scene |
| Live model evaluation | out of scope | No successful result exists; not planned for the next phase |
| Cached-live replay | out of scope | No verified live cache exists; not planned for the next phase |
| ConceptGraphs smoke | one-frame smoke executed with warning | `outputs/baselines/conceptgraphs_smoke_v1/native_results.json` and `query_results/q051.json`; five-scene comparison still blocked |
| LangSplat smoke | official sofa smoke executed | `outputs/baselines/langsplat_smoke_v1/native_results.json` and `query_results/ls001.json`; five-scene comparison still blocked |
| 3D IoU | `N/A` | Independent GT and predicted 3D boxes are unavailable |
| ScanNet | postponed | Excluded from Week 3 |

## Stub Semantic Gate

```powershell
python -B scripts\validate_semantic_index.py --scenes backend\data\scenes\ConferenceHall-capture-pilot backend\data\scenes\Museume-capture backend\data\scenes\Theater-capture backend\data\scenes\outdoor-drone-capture backend\data\scenes\outdoor-street-capture --out docs\validation\semantic_index
python -B scripts\run_experiment.py --config configs\week3_replica.yaml --mode stub --out outputs\week3\final_stub_semantic_gate_v1
```

| Metric | Result |
|---|---:|
| Scene indexes valid | 5/5 |
| Query results | 40/40 |
| Schema-valid results | 40/40 |
| Available results | 40/40 |
| Stub results | 40 |
| Model calls / cache hits | 0 / 0 |
| Results with `found=true` | 26 |
| Results with `found=false` | 14 |
| Accuracy-eligible results | 0 |
| Results excluded for missing GT | 40 |
| Mean measured stub query runtime | 0.0012 seconds |
| 3D IoU | `N/A` |

The `found` split is measured stub behavior, not correctness. Every five-scene benchmark query has `verification_status: missing_gt`, so no retrieval, negative-query, object, view, node, or zone accuracy is claimed.

## Out-Of-Scope: Live And Cached-Live

No successful provider-backed live result exists, and no verified live cache exists. The current plan intentionally drops live and cached-live work; the next phase should focus on independent GT, verified benchmark expansion, stronger baseline comparisons, and 3D box evaluation.

## Baseline Smoke

ConceptGraphs executed a minimal Docker smoke on one captured `ConferenceHall-capture-pilot` frame. It produced one native result and one canonical schema-valid result under `outputs/baselines/conceptgraphs_smoke_v1/`. This is not a five-scene comparison and not an accuracy result because `q051` has `verification_status: missing_gt`.

LangSplat executed a minimal Docker smoke on the official pretrained sofa assets. It produced one native result and one canonical schema-valid result under `outputs/baselines/langsplat_smoke_v1/`. This is not a five-scene SemanticSplat comparison and not an accuracy result because the smoke query has `verification_status: missing_gt`.

## Claims Not Made

- Manual annotations are not independent semantic ground truth.
- Stub outputs are not provider-backed model outputs.
- No live or cached-live evaluation result exists or is planned for the next phase.
- No five-scene baseline comparison or superiority result exists.
- No 3D localization metric is available.
- ScanNet was not evaluated.
