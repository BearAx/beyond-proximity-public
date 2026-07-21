# ConceptGraphs Full Baseline

- Mode: `live`
- Scenes: 8
- Canonical results: 48
- Native input directory: `C:\GitProjects\beyond-proximity\outputs\baselines\conceptgraphs_scannet_full_v1`
- Scope: `scannet` scenes with native ConceptGraphs maps and batch CLIP object retrieval.
- GT: official `scannet` object boxes from the benchmark.
- Empty-scene handling: if a native map has zero objects, outputs are explicit `found=false` misses.

Token usage is measured as OpenCLIP `ViT-H-14` non-padding text-tokenizer tokens, not provider/API billing tokens.

3D IoU uses official public-dataset GT boxes in the dataset world frame.

## Per-Scene Native Map Status

| Scene | Queries | Found outputs | Native map objects | Status |
|---|---:|---:|---:|---|
| scannet_0011_00 | 6 | 6 | 36 | available |
| scannet_0030_00 | 6 | 6 | 69 | available |
| scannet_0046_00 | 6 | 6 | 43 | available |
| scannet_0086_00 | 6 | 6 | 19 | available |
| scannet_0222_00 | 6 | 6 | 73 | available |
| scannet_0378_00 | 6 | 6 | 70 | available |
| scannet_0389_00 | 6 | 6 | 37 | available |
| scannet_0435_00 | 6 | 6 | 56 | available |
