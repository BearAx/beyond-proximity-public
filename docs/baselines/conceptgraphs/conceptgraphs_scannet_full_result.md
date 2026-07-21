# ConceptGraphs ScanNet Full Benchmark Result

Status date: 2026-07-15.

## Status

`DONE_WITH_LIMITATIONS`

Native ConceptGraphs detection, mapping, and CLIP object-map retrieval completed
on all eight BBQ-aligned ScanNet scenes. The run evaluated all 48 frozen
Nr3D/Sr3D+ queries against official ScanNet object-box GT.

## Protocol

- Repository: `concept-graphs/concept-graphs`
- Revision: `72f5962822b5e8678a446f367a06df1a977d2a4d`
- Scenes: 8
- Input RGB-D views: 39
- Queries: 48 / 48
- Mapping: absolute official ScanNet camera-to-world poses
- Detection: YOLO-World + MobileSAM
- Retrieval: OpenCLIP ViT-H-14 over native ConceptGraphs objects
- Token semantics: local non-padding OpenCLIP text tokens, not API billing

Run command:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_conceptgraphs_public.ps1 -Dataset scannet
```

## Results

| Metric | Result |
|---|---:|
| Canonical/schema-valid outputs | 48 / 48 |
| Native maps with objects | 8 / 8 |
| Expected object-label hit | 8 / 48 = 0.1667 |
| Exact GT object-ID hit | 0 / 48 = 0.0000 |
| Mean 3D IoU | 0.0696 |
| Acc@0.1 | 14 / 48 = 0.2917 |
| Acc@0.25 | 3 / 48 = 0.0625 |
| Acc@0.5 | 0 / 48 = 0.0000 |
| Mean batch-query runtime | 0.3363 s/query |
| Measured text tokens | 627 total |

`retrieval_success=1.0` only means the unthresholded native retriever emitted a
top object for every query. It is not an accuracy score.

## Interpretation

This is a real public-dataset baseline execution, but not a direct superiority
comparison with SemanticSplat. ConceptGraphs builds its own predicted object
map from RGB-D, whereas the current SemanticSplat public pilot searches oracle
GT semantic candidates. The inputs and construction assumptions differ.

Primary evidence:

- `outputs/baselines/conceptgraphs_scannet_full_v1/run_config.json`
- `outputs/baselines/conceptgraphs_scannet_full_v1/metrics_summary.json`
- `outputs/baselines/conceptgraphs_scannet_full_v1/baseline_summary.md`
- `outputs/baselines/conceptgraphs_scannet_full_v1/native_results_*.json`
