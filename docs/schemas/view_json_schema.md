# Captured-Scene ViewJSON Schema

Schema ID: `semanticsplat.captured_view_json.v1`

This contract describes semantic annotations attached to real manually captured RGB-D frames. It distinguishes provenance (`manual`, `live`, `cached_live`, or `stub`) and does not treat semantic-index annotations as independent ground truth.

## Required Shape

```json
{
  "schema_version": "semanticsplat.captured_view_json.v1",
  "view_id": "v001",
  "scene_id": "ConferenceHall-capture-pilot",
  "image_path": "images/v001.png",
  "depth_path": "depths/v001_depth.npy",
  "pose_ref": "transforms.json#/frames/0/transform_matrix",
  "intrinsics_ref": "transforms.json",
  "semantic_index_mode": "manual",
  "summary": "",
  "visible_regions": [],
  "visible_objects": [],
  "landmarks": [],
  "free_text_notes": "",
  "warnings": [
    "Manual annotation template only; semantic content must be filled from the referenced image."
  ]
}
```

All top-level fields are required. `schema_version` makes this captured-scene contract explicit and prevents accidental interpretation as an older repository ViewJSON shape.

## Semantic Index Mode

`semantic_index_mode` must be one of:

| Value | Meaning |
|---|---|
| `manual` | A person inspected the referenced real image and wrote the semantic content. |
| `live` | A configured live model inspected the image during this run. |
| `cached_live` | Content is reproduced from a preserved response originally produced by a live model. |
| `stub` | Synthetic/test-only semantic content; never report it as a real prediction. |

The mode describes provenance, not accuracy. Empty generated templates use `manual` because they are intended for manual completion, but they are not complete semantic annotations.

## Visible Regions

Each `visible_regions` entry should use:

```json
{
  "label": "conference table area",
  "approx_location": "center of the room",
  "source": "manual"
}
```

`label`, `approx_location`, and `source` are required. `source` uses the same four provenance values as `semantic_index_mode`.

## Visible Objects

Each `visible_objects` entry must use:

```json
{
  "label": "chair",
  "attributes": ["black", "near table"],
  "approx_location": "left side of the conference table",
  "confidence": null,
  "bbox_2d": null,
  "bbox_3d": null,
  "source": "manual"
}
```

Rules:

- `label` must describe an object actually visible in the referenced RGB frame.
- `attributes` is an array of short observed attributes; use `[]` when none are recorded.
- `approx_location` is natural-language image/scene location and may be an empty string in an unfinished template.
- `confidence` is `null` for manual annotations unless a documented manual confidence protocol exists. Live/cached-live confidence must come from the real provider output, not an invented default.
- `bbox_2d` may be `null`. When present, it is `[x1, y1, x2, y2]` in normalized top-left image coordinates with values in `[0, 1]` and `x1 < x2`, `y1 < y2`.
- `bbox_3d` must remain `null` unless it is computed from valid depth for a real identified target and its provenance is retained. A guessed box is forbidden.
- `source` is required for every object and must be `manual`, `live`, `cached_live`, or `stub`.

## Landmarks, Signs, And Facilities

Each `landmarks` entry should use:

```json
{
  "label": "exit sign",
  "kind": "sign",
  "approx_location": "above the right doorway",
  "source": "manual"
}
```

`kind` must be `landmark`, `sign`, or `facility`. Only visible evidence may be recorded.

## Path And Reference Rules

- `scene_id` must exactly equal the capture directory name.
- `view_id` must exactly match the corresponding `transforms.json` frame ID and output filename.
- `image_path` and `depth_path` are safe scene-relative paths and must resolve to existing captured files.
- `pose_ref` points to that frame's `transform_matrix` in `transforms.json` using a JSON-pointer-like fragment.
- `intrinsics_ref` points to `transforms.json`, whose top-level calibration applies to every captured frame.
- `warnings` must retain unresolved provenance, visibility, depth, or annotation limitations.

## Completeness And Eligibility

A generated empty template is structurally valid but semantically incomplete. It must not enable semantic evaluation. At minimum, a completed scene index requires real filled summaries plus at least one supported semantic region, object, or landmark and a valid tree covering the captured views.

Manual annotations may enable semantic query execution, but they are derived semantic-index data, not independent accuracy GT. Stub records must remain isolated from manual/live/cached-live results.

## Legacy Compatibility

The existing `backend.schemas.types.ViewJSON` used by the original `default` scene has legacy fields such as `scene_summary`, `room_type`, and `objects`. Phase H added captured-scene loading and lexical matching without removing that legacy path. The original MCP save tool still validates the legacy schema, while the headless runner and captured `live_session` branch read this v1 contract directly. Do not rename fields or copy legacy `default` records to make templates appear complete.
