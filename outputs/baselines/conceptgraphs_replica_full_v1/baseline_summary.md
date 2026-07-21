# ConceptGraphs Full Baseline

- Mode: `live`
- Scenes: 8
- Canonical results: 56
- Native input directory: `C:\GitProjects\beyond-proximity\outputs\baselines\conceptgraphs_replica_full_v1`
- Scope: `replica` scenes with native ConceptGraphs maps and batch CLIP object retrieval.
- GT: official `replica` object boxes from the benchmark.
- Empty-scene handling: if a native map has zero objects, outputs are explicit `found=false` misses.

Token usage is measured as OpenCLIP `ViT-H-14` non-padding text-tokenizer tokens, not provider/API billing tokens.

3D IoU uses official public-dataset GT boxes in the dataset world frame.

## Per-Scene Native Map Status

| Scene | Queries | Found outputs | Native map objects | Status |
|---|---:|---:|---:|---|
| replica_office0 | 7 | 7 | 29 | available |
| replica_office1 | 7 | 7 | 27 | available |
| replica_office2 | 7 | 7 | 44 | available |
| replica_office3 | 7 | 7 | 61 | available |
| replica_office4 | 7 | 7 | 60 | available |
| replica_room0 | 7 | 7 | 66 | available |
| replica_room1 | 7 | 7 | 32 | available |
| replica_room2 | 7 | 7 | 54 | available |
