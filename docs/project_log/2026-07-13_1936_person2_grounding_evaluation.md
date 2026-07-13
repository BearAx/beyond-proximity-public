# Person 2 grounding and evaluation

## What was done

- Extended canonical query results with object IDs, traversal/check traces,
  search/fallback metadata, object counts, and explicit bbox availability.
- Added object-level graph, graph+fallback, flat lexical, and local CPU
  embedding search over identical candidates.
- Added exact/synonym/affordance scoring, relation reranking, calibrated
  fallback, bbox validation, and no-hierarchy/no-relation/no-fallback/flat-only
  ablations.
- Added a standalone BBQ-aligned evaluator for 3D IoU, Acc@0.1/0.25/0.5,
  Recall@1, efficiency, strata, and failures. Segmentation metrics remain
  conditional and explicitly `N/A` without paired predictions.
- Downloaded and converted the authorized eight-scene ScanNet subset:
  39 selected RGB-D frames and 392/392 official objects passed validation.
- Built 48 official Nr3D/Sr3D+ pilot queries.
- Froze eight Replica and eight ScanNet variant/ablation runs.

## Why

Person 2's sprint responsibility is to provide BBQ-comparable object grounding
metrics while preserving and measuring graph-pruned query efficiency. The
previous evaluation was primarily view-level and could not support this claim.

## Evidence

- Replica: 56 queries over eight official scenes. Graph and flat lexical both
  reached 1.0 Recall@1/Acc thresholds on the oracle GT map; graph checked 12.11
  objects on average versus 71.88 for flat lexical.
- ScanNet: 48 official Nr3D/Sr3D+ queries over eight scenes. Graph and flat
  lexical both reached 0.2708 Recall@1/Acc@0.25; graph checked 11.23 objects
  versus 49.00 for flat lexical.
- Relation reranking did not improve this ScanNet pilot: no-relation reached
  0.2917. This is reported as a limitation.
- Frozen outputs are under `outputs/public_datasets/replica_pilot_v1/` and
  `outputs/public_datasets/scannet_pilot_v1/`.

## Token/cost notes

- No provider/API model calls were made.
- Flat embedding uses local CPU `fastembed` with
  `BAAI/bge-small-en-v1.5`; its one-time model download is cached locally.
- Estimated tokens are labeled `chars_div_4`, not provider billing tokens.
- Candidate construction cost is separated from per-query runtime.

## Files changed

- `backend/query/grounding.py`
- `backend/query/model_client.py`
- `backend/requirements.txt`
- `scripts/run_experiment.py`
- `scripts/evaluate_grounding.py`
- `scripts/run_grounding_variants.py`
- `docs/schemas/query_result_schema.md`
- `docs/benchmarks/bbq_aligned_metrics.md`
- `docs/experiments/public_datasets/person2_grounding_results.md`
- ScanNet provenance/validation reports and focused tests
- frozen public-dataset output directories

## Known failures and limits

- The runs query official GT object maps and are not semantic-perception
  accuracy or a fair BBQ reproduction.
- Replica's 1.0 score is an oracle-map sanity result, not superiority evidence.
- ScanNet relation reranking currently hurts one exact target in this pilot.
- mAcc/mIoU/fmIoU remain `N/A` because no paired model-predicted segmentation
  arrays were produced.
- The full suite is 141 passed / 3 failed because this worktree contains Git
  LFS pointer text instead of default-scene PNG payloads and `git-lfs` is not
  installed. All 22 Person 2 focused tests pass; the three failures are
  inherited image-fixture failures in `tests/backend/test_benchmark.py`.
- The required full documentation benchmark pipeline was attempted through
  `scripts/run_full_benchmark.py` with the project environment and failed for
  the same missing Git LFS image payload (`default/images/v003.png`). Person 2
  public-dataset reports were generated independently by the new runner.

## Next steps

- Improve relation parsing/reranking using ReferIt3D relation labels and
  target-anchor constraints.
- Add a non-oracle perception track before reporting semantic accuracy.
- Run a fair external BBQ baseline only under matched split and candidate
  construction conditions.
