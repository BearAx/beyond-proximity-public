# Real Evaluation Status

Status date: 2026-06-28. Final credential-independent Week 3 status.

## Evidence Summary

| Evidence | Status | Result |
|---|---|---|
| RGB-D capture | measured | 5/5 scenes, 96 matched RGB/depth/pose records |
| Intrinsics and poses | measured | 5/5 valid; intrinsics match 2340x1170 captures |
| Depth variation | measured | non-constant for all five scenes |
| Manual semantic index | measured validation | 5/5 executable; 96 views and 1,046 items; manual, not independent ground truth |
| Stub semantic gate | measured | 40/40 available schema-valid results; 0 model calls |
| Live model evaluation | out of scope | 0 successful live results; not planned for the next phase |
| Cached-live replay | out of scope | 0 cached-live results; no verified live cache exists |
| Baseline smoke | partial | 1 ConceptGraphs one-frame native/canonical result and 1 LangSplat official-sofa native/canonical result, both with no GT-backed accuracy |
| Semantic accuracy | unavailable | no independent semantic GT |
| 3D IoU | `N/A` | no independent GT/predicted 3D boxes |

## Scene Status

| Scene | Views | Semantic items | Tree nodes | Semantic execution | Geometry evaluation |
|---|---:|---:|---:|---|---|
| `ConferenceHall-capture-pilot` | 20 | 207 | 201 | allowed | unavailable |
| `Museume-capture` | 20 | 225 | 222 | allowed | unavailable |
| `Theater-capture` | 20 | 226 | 221 | allowed | unavailable |
| `outdoor-drone-capture` | 16 | 169 | 159 | allowed | unavailable |
| `outdoor-street-capture` | 20 | 219 | 216 | allowed | unavailable |

`semantic_eval_allowed=true` means the manual index is structurally valid and executable. It does not make those annotations accuracy ground truth.

## Reproduction

```powershell
python -B scripts\run_experiment.py --config configs\week3_replica.yaml --mode stub --out outputs\week3\final_stub_semantic_gate_v1
```

Live and cached-live are no longer part of the next evaluation plan. No provider-backed result or verified live cache exists, so no live/cached-live metric is reported.

## Remaining Work

- Resolve ConceptGraphs' post-map internal report crash, then expand from one-frame smoke to multi-frame/multi-query captured-scene runs.
- Convert/train/load the five captured scenes in LangSplat native SfM/3DGS format before any fair comparison.
- Add independent semantic GT before reporting accuracy.
- Add independent and predicted 3D boxes before reporting 3D IoU.
- Keep ScanNet postponed.
