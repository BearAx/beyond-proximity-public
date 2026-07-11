# Limitations Resolution Status

Status date: 2026-07-11.

## Solved Locally

| Previous limitation | Status | Evidence |
|---|---|---|
| Missing tree-native zone traversal | SOLVED_FOR_MANUAL_REFERENCE_GT | `outputs/week3/benchmark_v2_stub_manual_bbox_gt_v4/metrics_summary.json` reports expected-zone hit `113/125 = 0.9040`; five trees contain stable `manual_zone_*` nodes. |
| Missing graph-vs-flat speed/token evidence | SOLVED_FOR_DETERMINISTIC_SAME_INPUT_BENCHMARK | `outputs/week3/graph_vs_flat_benchmark_v2/graph_vs_flat_metrics.json` reports graph `1.5865x` mean local latency speedup, `25.32%` fewer entries scanned, and `25.26%` fewer estimated input tokens with matching quality metrics. |
| Missing Person 2 GT package | SOLVED | `docs/benchmarks/final_benchmark_lock_v2.md` locks 150 verified manual-reference queries with objects, views, regions, zones, negative review, and bbox GT. |
| Missing denominator-safe evaluation reports | SOLVED | `docs/benchmarks/gt_coverage_report.md`, `docs/benchmarks/benchmark_v2_execution_report.md`, and graph-vs-flat outputs. |
| Missing official Replica object-box pilot | SOLVED_FOR_REPLICA_OBJECT_BOX_GT | `docs/datasets/replica_official_import_report.md` and `outputs/public_datasets/replica_bbq_aligned_v3/metrics_summary.json` report 8 official Replica scenes, 575 GT boxes, 56/56 evaluated mixed-type queries, measured `bbox_3d_iou=1.0`, and measured estimated input tokens. |

## Still External Or Out Of Scope

| Limitation | Why it remains | What would be needed |
|---|---|---|
| Independent semantic accuracy | The current labels are produced from the project manual semantic index; the same project cannot certify them as independent GT. | Separate reviewer sign-off or official dataset annotations. |
| Official/pixel-accurate segmentation or mask IoU | Replica object boxes are imported, but segmentation/mask evaluation is not implemented. | Segmentation evaluator over official Replica/ScanNet labels plus predicted masks/classes. |
| Freshness/change reasoning | The captured scenes have no temporal recapture or change labels. | A second capture pass or explicit temporal change annotations. |
| Official ScanNet claim | ScanNet official data requires Terms-of-Use approval before local download and conversion. | Approved ScanNet access, extracted scenes, converter, GT labels, and validation reports. |
| Fair external public-dataset baselines | Replica pilot runs only SemanticSplat stub mode so far. | Same-scene ConceptGraphs/LangSplat/BBQ or other baseline outputs. |

## Article-Safe Claim

On the five captured manual-reference scenes, the tree-enriched graph method
scans fewer semantic entries, uses smaller serialized context, uses fewer
estimated input tokens, and has lower measured local deterministic latency than
flat search over the same semantic map while matching flat quality metrics.
On official Replica, the current object-box pilot imports 8 BBQ-aligned scenes
with 575 official object boxes and evaluates 56 deterministic GT-backed mixed
query-type object queries.

Do not claim independent semantic accuracy, official 3D localization accuracy,
live-provider latency, freshness/change detection, ScanNet results, segmentation
metrics, or external-baseline superiority from this evidence.
