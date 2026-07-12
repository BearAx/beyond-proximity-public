# ScanNet BBQ-Aligned Grounding V2 Metrics Summary

Status date: 2026-07-12.

This tracked report freezes the paper-facing evidence from the local run:

```text
outputs/public_datasets/scannet_bbq_grounding_v1/scannet_bbq_grounding_official_gt_v2
```

The public aggregate machine-readable summary is
`docs/experiments/public_datasets/scannet_bbq_grounding_v2_metrics_summary_compact.json`.
Licensed raw, extracted, backend, and per-query ScanNet-derived GT remain local
and gitignored; the checked-in builders reproduce them after terms acceptance.

## Reproduction

```powershell
python -B scripts\download_scannet_official.py --out-dir data\scannet --bbq-scenes --profile full --workers 8 --retries 8 --accept-tos
python -B scripts\download_scannet_grounding_annotations.py --install-gdown --acknowledge-source-terms
python -B scripts\prepare_scannet_scene.py --all-bbq-scenes --max-views 24 --candidate-stride 5 --overwrite
python -B scripts\build_scannet_official_queries.py
python -B scripts\audit_public_dataset_readiness.py
python -B scripts\run_experiment.py --config configs\scannet_benchmark.yaml --mode stub
```

## Scope And GT Integrity

| Field | Value |
|---|---:|
| Official ScanNet scenes | 8 |
| Raw files verified | 49 / 49, including the shared label map |
| Selected real RGB-D views | 39 |
| Official aggregation instances | 392 |
| Instances indexed | 392 / 392 |
| Official semantic vertices converted | 1,689,730 |
| Nr3D `correct_guess=True` rows in the BBQ subset | 699 |
| Unique Sr3D+ target-relation-anchor triplets | 661 |
| Missing ReferIt3D target IDs | 0 |
| Missing ReferIt3D anchor IDs | 0 |
| Frozen pilot | 24 Nr3D + 24 Sr3D+ = 48 queries |
| Mode | deterministic `stub` |
| Provider calls | 0 |

The eight-scene extraction, GT conversion, backend import, tree construction,
and validation took 15.9741 seconds in the recorded local rebuild. This is a
one-time map-construction cost and is separate from query runtime.

## Coverage

| Metric | Value |
|---|---:|
| Result output coverage | 48 / 48 |
| Canonical schema validity | 48 / 48 |
| Accuracy-eligible results | 48 / 48 |
| Missing or unavailable results | 0 |
| Reliable depth scenes | 8 / 8 |
| Semantic and geometry validation | 8 / 8 |

## Dataset-Stratified Quality

Missing or invalid predictions remain in each Acc@k denominator with IoU zero.

| Source | Queries | Retrieval success | Exact object-ID hit | Mean 3D IoU | Acc@0.1 | Acc@0.25 | Acc@0.5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Nr3D | 24 | 0.8750 | 0.2500 | 0.2572 | 0.2500 | 0.2500 | 0.2500 |
| Sr3D+ | 24 | 1.0000 | 0.2500 | 0.2660 | 0.3333 | 0.2917 | 0.2500 |
| Combined | 48 | 0.9375 | 0.2500 | 0.2616 | 0.2917 | 0.2708 | 0.2500 |

The exact combined counts are 12/48 object-ID hits, 14/48 at IoU 0.1,
13/48 at IoU 0.25, and 12/48 at IoU 0.5. Three queries returned no valid box
and correctly count as zero-IoU failures.

## Efficiency

| Metric | Mean | Total | Denominator |
|---|---:|---:|---:|
| Query runtime, seconds | 0.0025 | 0.1223 | 48 |
| Checked views | 4.8750 | 234 | 48 |
| Visited nodes | 4.7292 | 227 | 48 |
| Context size, characters | 35,377.0625 | 1,698,099 | 48 |
| Prompt size, characters | 35,557.0625 | 1,706,739 | 48 |
| Estimated input tokens | 8,889.6875 | 426,705 | 48 |

Actual provider token usage is unavailable by definition because this is a
local deterministic stub with no provider request. Estimated tokens are
measured from the serialized prompt using `ceil(prompt_size_chars / 4)` and are
the valid token-cost metric for this run.

## Interpretation

This is an oracle-GT-map retrieval benchmark. Official ScanNet instances and
boxes are supplied as the semantic map, and the algorithm must select the
ReferIt3D target. Therefore:

- the result measures object retrieval and relational grounding;
- it does not measure semantic perception or box generation from RGB-D;
- mAcc, mIoU, and fmIoU remain N/A until independent model predictions exist;
- the low 0.2500 exact-object score is a real limitation of the lexical stub,
  which often matches an anchor or the wrong same-class instance;
- no superiority over BBQ, ConceptGraphs, LangSplat, or another baseline is
  claimed without a same-input run.

The next algorithmic task is explicit target-anchor relation scoring or spatial
graph reranking, evaluated on this unchanged query and GT lock.
