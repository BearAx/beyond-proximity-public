# ConceptGraphs Full Baseline

- Mode: `live`
- Scenes: 5
- Canonical results: 150
- Native input directory: `outputs\baselines\conceptgraphs_full_v1`
- Scope: full five captured scenes with native ConceptGraphs maps and batch CLIP object retrieval.
- Important limitation: this is not an official Replica/ScanNet run and has no independent 3D IoU GT.
- Empty-scene handling: if a native map has zero objects, outputs are explicit `found=false` misses.

Token usage is measured as OpenCLIP `ViT-H-14` non-padding text-tokenizer tokens, not provider/API billing tokens.

3D IoU, when evaluated, uses Person 2 manual coarse depth-projected GT boxes from `docs/benchmarks/manual_bbox_gt_v2.json`; it is an internal regression signal, not official dataset localization GT.

## Per-Scene Native Map Status

| Scene | Queries | Found outputs | Native map objects | Status |
|---|---:|---:|---:|---|
| ConferenceHall-capture-pilot | 30 | 30 | 313 | available |
| Museume-capture | 30 | 30 | 150 | available |
| outdoor-drone-capture | 30 | 0 | 0 | native_map_empty |
| outdoor-street-capture | 30 | 30 | 43 | available |
| Theater-capture | 30 | 30 | 183 | available |
