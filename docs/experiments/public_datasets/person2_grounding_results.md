# Person 2 public-dataset grounding results

Status date: 2026-07-13.

## Scope

These are deterministic retrieval/grounding experiments over official
Replica and ScanNet GT object maps. They measure query-time search over oracle
semantic candidates; they are not semantic-perception accuracy, a BBQ
reproduction, or evidence of superiority over BBQ.

All variants use the same scene items, queries, GT, canonical output schema,
and evaluator. Construction cost is reported separately from per-query cost.

## Frozen runs

- `outputs/public_datasets/replica_pilot_v1/`: 56 queries, 8 official Replica
  scenes, 8 variants/ablations, 448 evaluated canonical result records.
- `outputs/public_datasets/scannet_pilot_v1/`: 48 official Nr3D/Sr3D+ queries,
  8 official ScanNet scenes, 8 variants/ablations, 384 evaluated canonical
  result records.
- Every variant has JSON/CSV/MD metrics and per-query failure output.
- Per-query result files are reproducible working artifacts and intentionally
  ignored; evaluated per-query records and aggregate evidence are retained in
  each tracked `grounding_summary.json`.
- Conditional segmentation mAcc/mIoU/fmIoU is `N/A`: there are GT semantic
  labels but no paired model-predicted segmentation arrays in this track.

## Main observations

Replica is an oracle-map sanity track: graph, graph+fallback, and flat lexical
all reach Recall@1 and Acc@0.1/0.25/0.5 of 1.0. This ceiling result must not be
presented as independent perception accuracy. Graph checks 12.11 objects and
about 303 estimated input tokens per query on average, versus 71.88 objects
and about 1,765 tokens for flat lexical.

On the harder 48-query ScanNet language pilot:

| Variant | Recall@1 | Acc@0.25 | Checked objects | Estimated tokens | Runtime (s) |
|---|---:|---:|---:|---:|---:|
| graph | 0.2708 | 0.2708 | 11.23 | 500.50 | 0.0008 |
| graph + fallback | 0.2708 | 0.2708 | 47.00 | 2027.23 | 0.0016 |
| flat lexical | 0.2708 | 0.2708 | 49.00 | 2116.77 | 0.0015 |
| flat embedding | 0.2500 | 0.2500 | 49.00 | 2116.77 | 0.1688 |
| no relation rerank | 0.2917 | 0.2917 | 47.71 | 2061.88 | 0.0013 |

The graph-only variant preserves the observed lexical quality while checking
about 77% fewer objects than flat lexical. Calibrated fallback expands often
on natural-language queries and therefore approaches flat-search cost. The
current relation reranker does not improve this pilot: disabling it recovers
one additional exact target. This is a measured limitation, not a positive
relation-reasoning claim.

## Reproduction

```bash
python -B scripts/download_scannet_official.py \
  --out-dir data/scannet --bbq-scenes --profile full \
  --workers 8 --retries 8 --accept-tos
python -B scripts/prepare_scannet_scene.py \
  --all-bbq-scenes --max-views 24 --candidate-stride 5 --overwrite
python -B scripts/download_scannet_grounding_annotations.py \
  --install-gdown --acknowledge-source-terms
python -B scripts/build_scannet_official_queries.py

python -B scripts/run_grounding_variants.py \
  --config configs/replica_benchmark.yaml \
  --out outputs/public_datasets/replica_pilot_v1
python -B scripts/run_grounding_variants.py \
  --config configs/scannet_benchmark.yaml \
  --out outputs/public_datasets/scannet_pilot_v1
```

The flat embedding run uses local CPU `fastembed` with
`BAAI/bge-small-en-v1.5`; model and cache provenance are saved in each run
configuration.
