# Scene Manifest Schema

Canonical schema ID: `semanticsplat.scene_manifest.v1`.

The normative field definition is maintained in [`docs/schemas/scene_manifest_schema.md`](../../schemas/scene_manifest_schema.md). Dataset ingestion scripts write `scene_manifest.json` inside each imported backend scene.

## Week 2/3 Dataset Rules

- Scope is Replica, Replica-like pilots, and the existing `default` pilot only.
- A Replica-like directory name does not prove official Replica provenance.
- `dataset` and `source_description` must identify the actual source honestly.
- Depth reliability is established only by `scripts/validate_scene_geometry.py`.
- ViewJSON room/object labels are predictions, not dataset ground truth.
- ScanNet is postponed and is not a Week 3 acceptance criterion.

## Supported Input Layouts

The importer accepts:

```text
RGB-D directory:
  scene/
    rgb/
    depth/
    poses.json
    intrinsics.json
    metadata.json        # optional

PLY-only asset:
  <scene_id>.ply
```

It writes one of two canonical backend layouts:

```text
RGB-D:
backend/data/scenes/<scene_id>/
  images/
  depths/
  transforms.json
  source_metadata.json
  scene_manifest.json

PLY-only:
backend/data/scenes/<scene_id>/
  geometry/
    scene.ply
  source_metadata.json
  scene_manifest.json
```

PLY-only manifests set unavailable RGB, depth, pose, intrinsics, and semantic-index paths to null. They never create empty transforms or synthetic camera data.

## Reproduction

```powershell
python scripts/import_replica_scene.py `
  --input <replica-style-scene> `
  --scene-id <scene-id> `
  --backend-root . `
  --dataset replica

python scripts/import_replica_scene.py `
  --batch scenes `
  --output backend/data/scenes

python scripts/validate_scene_geometry.py `
  --scene backend/data/scenes/<scene-id> `
  --output outputs/<scene-id>_geometry.json
```

The importer does not download data, infer dataset identity from filenames, or create synthetic RGB-D/GT data.
