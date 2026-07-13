# BBQ-aligned grounding summary

- Benchmark: `replica_bbq_aligned_official_gt_pilot_v2`
- Queries: 56
- Canonical / legacy-adapted results: 56 / 0

Missing, unavailable, and invalid predictions remain in GT-eligible 3D-box denominators as IoU 0.

| Metric | Value | Numerator / denominator |
|---|---:|---:|
| 3D bbox IoU | 0.8461 | 48 eligible |
| Acc@0.1 | 0.8750 | 42 / 48 |
| Acc@0.25 | 0.8750 | 42 / 48 |
| Acc@0.5 | 0.8333 | 40 / 48 |
| Recall@1 exact object ID | 0.8333 | 40 / 48 |

## Segmentation

| Metric | Status | Value |
|---|---|---:|
| mAcc | N/A | N/A |
| mIoU | N/A | N/A |
| fmIoU | N/A | N/A |

## Failure taxonomy

| Failure | Count |
|---|---:|
| wrong object | 8 |
| wrong relation | 0 |
| invalid/unavailable prediction | 0 |
| bad bbox | 0 |
| missing GT | 8 |

## Efficiency

| Measure | Mean | Total | Records |
|---|---:|---:|---:|
| runtime_seconds | 0.1371 | 7.6774 | 56 |
| checked_nodes | 2.0000 | 112.0000 | 56 |
| checked_views | 1.0000 | 56.0000 | 56 |
| checked_objects | 71.8750 | 4025.0000 | 56 |
| context_chars | 7030.7500 | 393722.0000 | 56 |
| estimated_tokens | 1765.1786 | 98850.0000 | 56 |

Construction cost is reported separately because it is a one-time indexing/map cost.

- Construction cost status: `reported`
