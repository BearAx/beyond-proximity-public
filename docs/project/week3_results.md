# Week 3 Results

Status date: 2026-06-23. Final credential-independent gate complete. Live and cached-live remain blocked.

## Final Status

| Item | Status | Evidence |
|---|---|---|
| Captured scenes | measured | 5 scenes, 96 RGB-D frames/poses with matching intrinsics |
| Manual semantic index | measured validation | 5/5 scenes, 96/96 views, 1,046 semantic items; manual, not independent ground truth |
| Stub semantic gate | measured | 40/40 available and schema-valid results, eight per scene |
| Live model evaluation | blocked by missing provider credentials | Requires `SEMANTICSPLAT_PROVIDER`, `SEMANTICSPLAT_MODEL`, `SEMANTICSPLAT_API_KEY` |
| Cached-live replay | blocked because no verified live response cache exists | Zero verified project cache entries |
| ConceptGraphs smoke | blocked with attempted command | Missing checkout, Conda environment, checkpoints, preprocessing outputs, and native dataset layout |
| LangSplat smoke | blocked with attempted command | Missing checkout, Conda environment, pretrained 3DGS/language features/checkpoints, and compatible dataset layout |
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

## Live And Cached-Live

Phase C is `blocked: missing SEMANTICSPLAT_PROVIDER, SEMANTICSPLAT_MODEL, SEMANTICSPLAT_API_KEY`.

```powershell
python -B scripts\run_experiment.py --config configs\week3_replica.yaml --mode live --limit 1 --out outputs\week3\live_gate_v1
```

GPT-5/o-series payload compatibility is implemented and tested, but no successful credentialed project result exists. Phase D is blocked because no verified live response cache exists.

```powershell
python -B scripts\run_experiment.py --config configs\week3_replica.yaml --mode cached_live --limit 1 --out outputs\week3\cached_live_gate_v1
```

Do not run cached-live until the live command produces a `source_mode=live` cache entry.

## Baseline Smoke

ConceptGraphs and LangSplat were attempted using the official entrypoint shapes. Both stopped before baseline execution. Exact commands and errors are recorded in `docs/baselines/conceptgraphs/conceptgraphs_smoke_result.md` and `docs/baselines/langsplat/langsplat_smoke_result.md`. No native or canonical baseline result is claimed.

## Claims Not Made

- Manual annotations are not independent semantic ground truth.
- Stub outputs are not live model outputs.
- No live or cached-live evaluation result exists.
- No baseline comparison or superiority result exists.
- No 3D localization metric is available.
- ScanNet was not evaluated.
