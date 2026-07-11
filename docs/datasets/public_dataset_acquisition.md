# Public Dataset Acquisition Notes

Status date: 2026-07-11.

## Why This Exists

The current project has five captured pilot scenes, one local Replica-style
proxy folder, and an official Replica v1 object-box evaluation track. It still
does not have official ScanNet data. This note records the correct acquisition
path so future work does not accidentally present proxy data as public-dataset
evidence.

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

Required local extracted folders:

```text
data/scannet/<scene_id>/
  color/
  depth/
  pose/
  intrinsic/
```

Current converter status:

```text
scripts/prepare_scannet_scene.py = folder readiness skeleton only
```

Before claiming ScanNet results, complete the converter for:

- color frames,
- depth frames,
- camera poses,
- intrinsics,
- semantic/instance GT mapping,
- query GT mapping.

## Current Status

Run:

```powershell
python -B scripts\audit_public_dataset_readiness.py
```

Current expected result:

```text
official Replica scenes ready: 8
imported official Replica GT object boxes: 575
ScanNet scenes ready: 0
```

This supports a carefully scoped TwinWorld workshop public-dataset pilot for
Replica object grounding. It is still not enough for AAAI-main-level claims
without fair baselines, broader public-dataset coverage, and stronger metrics.
