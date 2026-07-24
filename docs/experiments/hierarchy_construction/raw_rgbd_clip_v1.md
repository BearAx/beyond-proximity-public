# Automatic Raw RGB-D Hierarchy Benchmark

Status: **DONE_AND_VALIDATED**
Run date: 2026-07-24

## Construction Boundary

The automatic constructor reads only:

- five `transforms.json` files;
- 97 RGB images;
- 97 depth arrays;
- 97 camera poses.

It reads **zero** manual ViewJSON files, manual zone files, or checked-in tree
records during construction. The raw hierarchy is serialized before
`manual_zone_gt_v2.json` is opened for evaluation.

Frozen CLIP ViT-B/32 image features are concatenated with standardized pose and
depth statistics. Deterministic k-means selects the cluster count by silhouette
score. A fixed 20-label, scene-agnostic CLIP vocabulary assigns predicted
semantic branch labels.

## Construction Results

| Metric | Result |
|---|---:|
| Scenes | 5 |
| RGB / depth / pose records | 97 / 97 / 97 |
| Construction model calls | 15 |
| Exact semantic-label tokens | 151 |
| CPU construction latency | 14.151 s |
| Manual ViewJSON reads | 0 |
| Manual zone reads | 0 |
| Pairwise F1 vs. manual zones | 0.487 |
| Rand index vs. manual zones | 0.637 |

## Retrieval Comparison

All variants use the same frozen CLIP query/image scorer.

| Variant | hit@1 | hit@3 | MRR | Views checked |
|---|---:|---:|---:|---:|
| Flat CLIP | 0.432 | 0.624 | 0.571 | 19.40 |
| Manual-zone CLIP | 0.424 | 0.592 | 0.537 | 10.76 |
| Raw RGB-D hierarchy CLIP | 0.368 | 0.528 | 0.480 | 10.00 |

The automatic hierarchy cuts checked views by 48.5% relative to flat CLIP but
loses retrieval quality. This is the measured cost of removing manual semantic
records, not a hidden limitation.

## Evidence

- `outputs/raw_rgbd_hierarchy/five_scene_clip_v1/raw_hierarchy.json`
- `outputs/raw_rgbd_hierarchy/five_scene_clip_v1/metrics_summary.json`
- `outputs/raw_rgbd_hierarchy/five_scene_clip_v1/per_query_results.json`
- `outputs/raw_rgbd_hierarchy/five_scene_clip_v1/per_query_metrics.csv`
- `outputs/raw_rgbd_hierarchy/five_scene_clip_v1/validation_report.json`

## Reproduce

```powershell
python -m pip install -r backend\requirements-experiments.txt
python -B scripts\run_raw_rgbd_hierarchy_benchmark.py `
  --out outputs\raw_rgbd_hierarchy\five_scene_clip_v1
python -B scripts\validate_raw_rgbd_hierarchy_benchmark.py `
  --output outputs\raw_rgbd_hierarchy\five_scene_clip_v1
```
