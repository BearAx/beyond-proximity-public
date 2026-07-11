# Replica BBQ-Aligned Official GT V3 Metrics Summary

Status date: 2026-07-11.

This is the tracked summary for the local run stored under:

```text
outputs/public_datasets/replica_bbq_aligned_v3
```

The `outputs/` directory is intentionally ignored by git, so this document
records the paper-facing metrics needed from that run.

## Run Command

```powershell
python -B scripts\build_replica_official_queries.py
python -B scripts\run_experiment.py --config configs\replica_benchmark.yaml --mode stub --out outputs\public_datasets\replica_bbq_aligned_v3
```

## Scope

| Field | Value |
|---|---|
| Benchmark | `replica_bbq_aligned_official_gt_pilot_v2` |
| Scenes | 8 official Replica scenes |
| GT boxes | 575 official Replica object boxes |
| Queries | 56 |
| Mode | `stub` |
| Provider calls | 0 |

Actual provider token usage is unavailable because this is a deterministic
stub run. Estimated token and context metrics are measured from the serialized
query context.

## Coverage

| Metric | Value |
|---|---:|
| Result output coverage | 56 / 56 |
| Schema-valid results | 56 / 56 |
| Evaluated results | 56 |
| Accuracy-eligible results | 56 |
| Missing results | 0 |
| Unavailable results | 0 |
| Ground-truth unavailable results | 0 |

## Query Type Coverage

| Query type | Total | Retrieval hit rate | Object-ID hit rate | Not-found correctness |
|---|---:|---:|---:|---:|
| `simple_object` | 16 | 1.0000 | 1.0000 | N/A |
| `attribute` | 8 | 1.0000 | 1.0000 | N/A |
| `relational` | 8 | 1.0000 | 1.0000 | N/A |
| `multi_hop` | 8 | 1.0000 | 1.0000 | N/A |
| `functional` | 8 | 1.0000 | 1.0000 | N/A |
| `negative` | 8 | 1.0000 | N/A | 1.0000 |

## Main Metrics

| Metric | Value | Denominator |
|---|---:|---:|
| Retrieval success | 1.0000 | 56 |
| Expected view hit | 1.0000 | 48 |
| Expected object hit | 1.0000 | 48 |
| Expected object-ID hit | 1.0000 | 48 |
| Not-found correctness | 1.0000 | 8 |
| BBox 3D IoU | 1.0000 | 48 |
| Acc@0.1 | 1.0000 | 48 |
| Acc@0.25 | 1.0000 | 48 |
| Acc@0.5 | 1.0000 | 48 |
| Classified failures | 0 | 56 |

## Efficiency Metrics

| Metric | Mean | Total | Denominator |
|---|---:|---:|---:|
| Runtime seconds | 0.0043 | N/A | 56 |
| Checked view count | 1.0000 | 56 | 56 |
| Visited node count | 12.2679 | 687 | 56 |
| Context size chars | 42398.0357 | 2374290 | 56 |
| Prompt size chars | 42578.0357 | 2384370 | 56 |
| Estimated input tokens | 10644.8571 | 596112 | 56 |

## Important Wording

Safe claim:

```text
On eight official Replica scenes, SemanticSplat's deterministic stub retrieval
completed 56 GT-backed object-box queries with full schema coverage, 1.0
object-ID hit on positive queries, 1.0 not-found correctness on negative
queries, and measured estimated input-token/context costs.
```

Do not claim:

```text
actual provider token usage
live model reasoning
ScanNet results
semantic segmentation mIoU/fmIoU
fair external-baseline superiority
```
