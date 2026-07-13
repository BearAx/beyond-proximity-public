# BBQ-aligned grounding summary

- Benchmark: `scannet_bbq_aligned_referit3d_official_gt_pilot_v1`
- Queries: 48
- Canonical / legacy-adapted results: 48 / 0

Missing, unavailable, and invalid predictions remain in GT-eligible 3D-box denominators as IoU 0.

| Metric | Value | Numerator / denominator |
|---|---:|---:|
| 3D bbox IoU | 0.2937 | 48 eligible |
| Acc@0.1 | 0.2917 | 14 / 48 |
| Acc@0.25 | 0.2917 | 14 / 48 |
| Acc@0.5 | 0.2917 | 14 / 48 |
| Recall@1 exact object ID | 0.2917 | 14 / 48 |

## Segmentation

| Metric | Status | Value |
|---|---|---:|
| mAcc | N/A | N/A |
| mIoU | N/A | N/A |
| fmIoU | N/A | N/A |

## Failure taxonomy

| Failure | Count |
|---|---:|
| wrong object | 30 |
| wrong relation | 0 |
| invalid/unavailable prediction | 4 |
| bad bbox | 4 |
| missing GT | 0 |

## Efficiency

| Measure | Mean | Total | Records |
|---|---:|---:|---:|
| runtime_seconds | 0.0009 | 0.0453 | 48 |
| checked_nodes | 1.8333 | 88.0000 | 48 |
| checked_views | 4.8750 | 234.0000 | 48 |
| checked_objects | 49.0000 | 2352.0000 | 48 |
| context_chars | 8414.6250 | 403902.0000 | 48 |
| estimated_tokens | 2116.7708 | 101605.0000 | 48 |

Construction cost is reported separately because it is a one-time indexing/map cost.

- Construction cost status: `reported`
