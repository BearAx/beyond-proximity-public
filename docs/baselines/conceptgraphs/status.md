# ConceptGraphs Status

Status date: 2026-07-15. Status: `PUBLIC_DATA_RUNS_DONE_WITH_LIMITATIONS`.

## Completed Native Runs

| Dataset | Scenes | RGB-D views | Queries | Native maps | Acc@0.25 | Evidence |
|---|---:|---:|---:|---:|---:|---|
| ScanNet | 8 | 39 | 48 / 48 | 8 / 8 nonempty | 0.0625 | `outputs/baselines/conceptgraphs_scannet_full_v1/` |
| Replica | 8 | 40 | 56 / 56 | 8 / 8 nonempty | 0.0625 | `outputs/baselines/conceptgraphs_replica_full_v1/` |

Both runs use official RGB-D, metric depth, absolute camera poses, native
YOLO-World + MobileSAM detection, ConceptGraphs object mapping, and OpenCLIP
ViT-H-14 retrieval. They execute in Docker image
`semanticsplat-conceptgraphs:72f5962`, pinned to official repository revision
`72f5962822b5e8678a446f367a06df1a977d2a4d`.

The ScanNet run uses 39 selected views. The Replica run uses five evenly spaced
frames from each 2,000-frame trajectory (40 total), so it is a full-scene and
full-query sampled-map run, not full-trajectory mapping.

## Results

| Metric | ScanNet | Replica |
|---|---:|---:|
| Schema-valid outputs | 48 / 48 | 56 / 56 |
| Positive-query label hit | 8 / 48 | 7 / 48 |
| Exact object-ID hit | 0 / 48 | 0 / 48 |
| Mean 3D IoU | 0.0696 | 0.0624 |
| Acc@0.1 | 0.2917 | 0.1667 |
| Acc@0.25 | 0.0625 | 0.0625 |
| Acc@0.5 | 0.0000 | 0.0417 |
| Mean query runtime | 0.3363 s | 0.2743 s |
| Local text tokens | 627 | 459 |

## Reproduction

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_conceptgraphs_public.ps1 -Dataset scannet
powershell -ExecutionPolicy Bypass -File scripts\run_conceptgraphs_public.ps1 -Dataset replica -ReplicaFramesPerScene 5
```

The pinned mapper has a known post-save `KeyError: Sort Key` while generating
its internal report. The wrapper accepts this only after verifying that the
native map artifact exists.

## Interpretation Boundary

These are real predicted-map public-dataset executions, but they are not fair
rankings against SemanticSplat's oracle-map public pilots. Returning a top
object is not accuracy, and the local token counts are not API billing tokens.
