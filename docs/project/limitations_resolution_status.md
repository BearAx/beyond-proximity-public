# Limitations Resolution Status

Status date: 2026-07-01.

## Solved Locally

| Previous limitation | Status | Evidence |
|---|---|---|
| Missing tree-native zone traversal | SOLVED_FOR_MANUAL_REFERENCE_GT | `outputs/week3/benchmark_v2_stub_manual_bbox_gt_v4/metrics_summary.json` reports expected-zone hit `113/125 = 0.9040`; five trees contain stable `manual_zone_*` nodes. |
| Missing graph-vs-flat speed/token evidence | SOLVED_FOR_DETERMINISTIC_SAME_INPUT_BENCHMARK | `outputs/week3/graph_vs_flat_benchmark_v2/graph_vs_flat_metrics.json` reports graph `1.5865x` mean local latency speedup, `25.32%` fewer entries scanned, and `25.26%` fewer estimated input tokens with matching quality metrics. |
| Missing Person 2 GT package | SOLVED | `docs/benchmarks/final_benchmark_lock_v2.md` locks 150 verified manual-reference queries with objects, views, regions, zones, negative review, and bbox GT. |
| Missing denominator-safe evaluation reports | SOLVED | `docs/benchmarks/gt_coverage_report.md`, `docs/benchmarks/benchmark_v2_execution_report.md`, and graph-vs-flat outputs. |

## Still External Or Out Of Scope

| Limitation | Why it remains | What would be needed |
|---|---|---|
| Independent semantic accuracy | The current labels are produced from the project manual semantic index; the same project cannot certify them as independent GT. | Separate reviewer sign-off or official dataset annotations. |
| Official/pixel-accurate 3D IoU | Current boxes are coarse manual benchmark references, not official masks/tight boxes. | Independently reviewed tight boxes/masks plus predicted boxes. |
| Freshness/change reasoning | The captured scenes have no temporal recapture or change labels. | A second capture pass or explicit temporal change annotations. |
| Official Replica/ScanNet claim | The current benchmark uses five project-captured scenes, not official Replica/ScanNet ingestion. | Licensed dataset ingestion and GT-backed evaluation. |

## Article-Safe Claim

On the five captured manual-reference scenes, the tree-enriched graph method
scans fewer semantic entries, uses smaller serialized context, uses fewer
estimated input tokens, and has lower measured local deterministic latency than
flat search over the same semantic map while matching flat quality metrics.

Do not claim independent semantic accuracy, official 3D localization accuracy,
live-provider latency, freshness/change detection, or official Replica/ScanNet
results from this evidence.
