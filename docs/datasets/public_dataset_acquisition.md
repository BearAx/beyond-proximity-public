# Public Dataset Acquisition Notes

Status date: 2026-07-12.

## Why This Exists

The current project has five captured pilot scenes, one local Replica-style
proxy folder, an official Replica v1 object-box evaluation track, and a complete
eight-scene official ScanNet Nr3D/Sr3D+ grounding pilot. This note keeps raw
data, GT-map retrieval, and semantic-perception claims separate.

## Replica First

Replica is the recommended first public-dataset target.

Why:

- It is smaller and closer to the indoor digital-twin setting.
- The original dataset contains high-quality indoor reconstructions with dense
  geometry, HDR textures, semantic class labels, and semantic instance labels.
- It is a better near-term match than ScanNet for a workshop-scale extension.

Completed official Replica deliverable:

```text
data/replica_official_raw/
backend/data/scenes/replica_room0
backend/data/scenes/replica_room1
backend/data/scenes/replica_room2
backend/data/scenes/replica_office0
backend/data/scenes/replica_office1
backend/data/scenes/replica_office2
backend/data/scenes/replica_office3
backend/data/scenes/replica_office4
```

Acquisition and import commands:

```powershell
python -B scripts\acquire_replica_official.py --workers 3 --extract
python -B scripts\import_replica_semantic_mesh.py --all-bbq-scenes --overwrite
```

Do not mark a scene as official Replica unless `metadata.json` records official
provenance and the source files came from the legal dataset package.

Current Replica evidence:

- `docs/datasets/replica_official_acquisition_manifest.json`
- `docs/datasets/replica_official_import_report.md`
- `docs/validation/public_datasets/replica_*.json`
- `outputs/public_datasets/replica_bbq_aligned_v3`

## ScanNet Second

ScanNet is the recommended second public-dataset target.

Why:

- It is much larger and more credible for main-conference evaluation.
- It also has stronger access and conversion requirements.

Completed official raw acquisition:

```text
data/scannet/scans/scene0011_00
data/scannet/scans/scene0030_00
data/scannet/scans/scene0046_00
data/scannet/scans/scene0086_00
data/scannet/scans/scene0222_00
data/scannet/scans/scene0378_00
data/scannet/scans/scene0389_00
data/scannet/scans/scene0435_00
```

Acquisition and verification command:

```powershell
python -B scripts\download_scannet_official.py --out-dir data\scannet --bbq-scenes --profile full --workers 8 --retries 8 --accept-tos
```

Completed extracted layout:

```text
data/scannet/extracted/<scene_id>/
  color/
  depth/
  pose/
  intrinsic/
```

Completed converter and query commands:

```powershell
python -B scripts\prepare_scannet_scene.py --all-bbq-scenes --max-views 24 --candidate-stride 5 --overwrite
python -B scripts\download_scannet_grounding_annotations.py --install-gdown --acknowledge-source-terms
python -B scripts\build_scannet_official_queries.py
python -B scripts\run_experiment.py --config configs\scannet_benchmark.yaml --mode stub
```

Completed ScanNet evidence:

- 39 selected real RGB-D views with official poses/intrinsics;
- 392/392 official aggregation instances mapped to 3D AABBs;
- 1,689,730 official semantic vertices summarized by class;
- 699 BBQ-subset Nr3D rows and 661 unique Sr3D+ triplets with zero missing IDs;
- a frozen 48-query pilot with object-ID, Acc@k, runtime, context, and token metrics.

## Current Status

Run:

```powershell
python -B scripts\audit_public_dataset_readiness.py
```

Current expected result:

```text
official Replica scenes ready: 8
imported official Replica GT object boxes: 575
ScanNet raw scenes available: 8
ScanNet imported scenes ready: 8
ScanNet official GT boxes: 392
ScanNet grounding pilot queries: 48
```

This supports a carefully scoped TwinWorld workshop public-dataset pilot for
Replica and ScanNet object grounding. It is still not enough for AAAI-main-level
claims without fair baselines, stronger relational reasoning, and semantic
predictions for segmentation metrics.
