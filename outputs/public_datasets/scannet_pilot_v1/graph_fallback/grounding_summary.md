# BBQ-aligned grounding summary

- Benchmark: `scannet_bbq_aligned_referit3d_official_gt_pilot_v1`
- Queries: 48
- Canonical / legacy-adapted results: 48 / 0

Missing, unavailable, and invalid predictions remain in GT-eligible 3D-box denominators as IoU 0.

| Metric | Value | Numerator / denominator |
|---|---:|---:|
| 3D bbox IoU | 0.2728 | 48 eligible |
| Acc@0.1 | 0.2708 | 13 / 48 |
| Acc@0.25 | 0.2708 | 13 / 48 |
| Acc@0.5 | 0.2708 | 13 / 48 |
| Recall@1 exact object ID | 0.2708 | 13 / 48 |

## Segmentation

| Metric | Status | Value |
|---|---|---:|
| mAcc | N/A | N/A |
| mIoU | N/A | N/A |
| fmIoU | N/A | N/A |

## Failure taxonomy

| Failure | Count |
|---|---:|
| wrong object | 32 |
| wrong relation | 2 |
| invalid/unavailable prediction | 3 |
| bad bbox | 3 |
| missing GT | 0 |

## Efficiency

| Measure | Mean | Total | Records |
|---|---:|---:|---:|
| runtime_seconds | 0.0016 | 0.0785 | 48 |
| checked_nodes | 1.8750 | 90.0000 | 48 |
| checked_views | 4.7917 | 230.0000 | 48 |
| checked_objects | 47.0000 | 2256.0000 | 48 |
| context_chars | 8056.4167 | 386708.0000 | 48 |
| estimated_tokens | 2027.2292 | 97307.0000 | 48 |

Construction cost is reported separately because it is a one-time indexing/map cost.

- Construction cost status: `reported`
