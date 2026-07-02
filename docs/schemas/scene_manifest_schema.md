# Scene Manifest Schema

Schema ID: `semanticsplat.scene_manifest.v1`

The scene manifest records data provenance and whether geometry-dependent metrics are valid. It does not claim that files are Replica merely because they use a Replica-like directory layout.

## Required Shape

```json
{
  "schema_version": "semanticsplat.scene_manifest.v1",
  "scene_id": "replica_room_0",
  "dataset": "replica | pilot | custom | unknown_supersplat_export",
  "source_description": "Human-readable provenance",
  "paths": {
    "gaussian_splat": null,
    "rgb": "rgb",
    "depth": "depth",
    "poses": "poses.json",
    "intrinsics": "intrinsics.json",
    "semantic_index": null
  },
  "frame_count": 0,
  "coordinate_frame": "camera_to_world",
  "intrinsics": {
    "width": 0,
    "height": 0,
    "fx": 0.0,
    "fy": 0.0,
    "cx": 0.0,
    "cy": 0.0
  },
  "depth_validation": {
    "status": "reliable | unreliable | missing | unchecked",
    "unit": "meters | millimeters | unknown",
    "scale_to_meters": null,
    "checked_frame_count": 0,
    "constant_frame_count": 0,
    "invalid_value_fraction": null,
    "reason": ""
  },
  "ground_truth": {
    "zone_labels_available": false,
    "object_labels_available": false,
    "bbox_3d_available": false,
    "source": null
  },
  "warnings": []
}
```

## PLY-Only Variant

A normalized PLY-only scene uses:

```json
{
  "paths": {
    "gaussian_splat": "geometry/scene.ply",
    "rgb": null,
    "depth": null,
    "poses": null,
    "intrinsics": null,
    "semantic_index": null
  },
  "frame_count": 0,
  "coordinate_frame": "unknown",
  "intrinsics": {
    "present": false,
    "width": 0,
    "height": 0,
    "fx": 0.0,
    "fy": 0.0,
    "cx": 0.0,
    "cy": 0.0
  },
  "depth_validation": {
    "status": "missing"
  },
  "evaluation_eligibility": {
    "semantic_evaluation_allowed": false,
    "three_d_evaluation_allowed": false
  }
}
```

The zero-valued intrinsics are placeholders required by the manifest shape and are explicitly invalid because `present=false`. They must never be used as camera calibration.

## Rules

- Paths are relative to the manifest unless explicitly marked absolute.
- `depth_validation.status=reliable` requires non-constant finite depth, documented units, and matching resolution/intrinsics.
- Geometry metrics are forbidden when depth status is not `reliable`.
- Ground-truth flags describe independent annotations, not ViewJSON predictions.
- Dataset-native frames are allowed; 3DGS rendering is not required for Week 2 or Week 3.
- A PLY-only scene may be normalized for viewing and provenance while remaining invalid for semantic and 3D evaluation.
- Generated `source_metadata.json` describes the import operation; it is not original dataset metadata or GT.
