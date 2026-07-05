# Public Dataset Acquisition Notes

Status date: 2026-07-05.

## Why This Exists

The current project has five captured pilot scenes and one local
Replica-style proxy folder. It does not yet have official Replica or ScanNet
evaluation data. This note records the correct acquisition path so future work
does not accidentally present proxy data as public-dataset evidence.

## Replica First

Replica is the recommended first public-dataset target.

Why:

- It is smaller and closer to the indoor digital-twin setting.
- The original dataset contains high-quality indoor reconstructions with dense
  geometry, HDR textures, semantic class labels, and semantic instance labels.
- It is a better near-term match than ScanNet for a workshop-scale extension.

Required local deliverable:

```text
data/replica/<official_scene_id>/
  rgb/
  depth/
  poses.json
  intrinsics.json
  metadata.json
```

Then import with:

```powershell
python -B scripts\import_replica_scene.py `
  --input data\replica\<official_scene_id> `
  --scene-id replica_<official_scene_id> `
  --overwrite
```

Do not mark a scene as official Replica unless `metadata.json` records official
provenance and the source files came from the legal dataset package.

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
official Replica scenes ready: 0
ScanNet scenes ready: 0
```

This is not a blocker for a carefully scoped TwinWorld workshop submission. It
is a blocker for AAAI-main-level claims.
