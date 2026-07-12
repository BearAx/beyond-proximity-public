# Official Replica Import Report

Status date: 2026-07-11.

## What Was Completed

- Downloaded official Replica v1 release assets from the Facebook Research
  Replica repository.
- Extracted the official dataset locally under `data/replica_official_raw/`.
- Imported the BBQ-aligned Replica subset into backend scenes:
  `replica_room0`, `replica_room1`, `replica_room2`, `replica_office0`,
  `replica_office1`, `replica_office2`, `replica_office3`, `replica_office4`.
- Converted official Replica `habitat/info_semantic.json` object IDs, labels,
  and oriented boxes into `ground_truth/object_boxes_3d.json`.
- Created official-GT ViewJSON indexes, scene manifests, source metadata, and
  tree manifests for all eight imported scenes.
- Created 56 GT-backed Replica pilot queries with expected object IDs and
  expected 3D boxes across simple, attribute, relational, multi-hop, functional,
  and negative query types.
- Ran and evaluated the official Replica object-box benchmark.

## Evidence Paths

| Evidence | Path |
|---|---|
| Acquisition manifest | `docs/datasets/replica_official_acquisition_manifest.json` |
| Readiness audit | `docs/datasets/public_dataset_readiness.md` |
| Dataset plan | `docs/datasets/replica_scannet_plan.md` |
| Availability manifest | `docs/datasets/replica_scannet_availability_manifest.json` |
| Benchmark config | `configs/replica_benchmark.yaml` |
| Pilot queries | `docs/benchmarks/replica_scannet_pilot_queries.json` |
| Imported scenes | `backend/data/scenes/replica_*` |
| Validation reports | `docs/validation/public_datasets/replica_*.json` |
| Latest local run | `outputs/public_datasets/replica_bbq_aligned_v3` |
| Tracked metrics summary | `docs/experiments/public_datasets/replica_bbq_aligned_v3_metrics_summary.md` |

Raw official data and downloaded archives are intentionally ignored by git:

```text
data/replica_official_raw/
data/replica_official_downloads/
```

## Imported Scene Counts

| Scene | GT boxes |
|---|---:|
| `replica_room0` | 92 |
| `replica_room1` | 54 |
| `replica_room2` | 61 |
| `replica_office0` | 64 |
| `replica_office1` | 48 |
| `replica_office2` | 91 |
| `replica_office3` | 100 |
| `replica_office4` | 65 |
| Total | 575 |

## Latest Benchmark Result

Run:

```powershell
python -B scripts\build_replica_official_queries.py
python -B scripts\run_experiment.py --config configs\replica_benchmark.yaml --mode stub --out outputs\public_datasets\replica_bbq_aligned_v3
```

Summary from `outputs/public_datasets/replica_bbq_aligned_v3/metrics_summary.json`:

| Metric | Status | Value |
|---|---|---:|
| result output coverage | measured | 56/56 |
| schema-valid results | measured | 56/56 |
| accuracy-eligible results | measured | 56/56 |
| retrieval_success | measured | 1.0000 |
| expected_view_hit | measured | 1.0000 |
| expected_object_id_hit | measured | 1.0000 |
| not_found_correctness | measured | 1.0000 |
| bbox_3d_iou | measured | 1.0000 |
| Acc@0.1 | measured | 1.0000 |
| Acc@0.25 | measured | 1.0000 |
| Acc@0.5 | measured | 1.0000 |
| estimated_input_tokens mean | measured | 10644.8571 |
| classified failures | measured | 0 |

## Scope Limits

- This is official Replica object-level GT, not rendered RGB-D evaluation.
- This is deterministic stub mode, not live provider reasoning.
- This is not a fair ConceptGraphs/LangSplat baseline comparison yet.
- Replica segmentation metrics such as mAcc, mIoU, and fmIoU still need a
  segmentation evaluator over the official semantic mesh labels.
- ScanNet remains outside this Replica-specific report, but its separate
  eight-scene Nr3D/Sr3D+ grounding track is complete and documented in
  `docs/experiments/public_datasets/scannet_bbq_grounding_v2_metrics_summary.md`.
