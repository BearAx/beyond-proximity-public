# Manual Semantic Annotation Guide

Status date: 2026-06-22. This guide applies to `semanticsplat.captured_view_json.v1` templates generated from real captured RGB-D frames.

## Scope And Provenance

Manual annotation means a person inspected the exact image referenced by `image_path` and recorded only visible evidence. Keep `semantic_index_mode` and every entry's `source` set to `manual`.

Manual annotations can enable semantic query execution after the captured-scene adapter is integrated, but they are derived semantic-index data. They are not independent ground truth and must not be used as final accuracy GT. They also do not enable 3D IoU.

## Open The Correct Evidence

For each `views/vNNN.json`, inspect the corresponding `images/vNNN.png` in the same scene directory. Use `depths/vNNN_depth.npy` and `transforms.json` only as referenced capture data; do not infer hidden objects from depth or another view.

Do not edit these identity/reference fields:

```text
schema_version
view_id
scene_id
image_path
depth_path
pose_ref
intrinsics_ref
semantic_index_mode
```

## Required Manual Edits

For every view:

1. Replace the empty `summary` with a short factual description of what is visible.
2. Add visible functional/spatial areas to `visible_regions` when identifiable.
3. Add clearly visible objects to `visible_objects`.
4. Add signs, landmarks, and facilities to `landmarks` using the correct `kind`.
5. Use `free_text_notes` for uncertainty or context that does not fit a structured entry.
6. Remove the template-only warning after the view is genuinely annotated; retain or add real uncertainty warnings.

Do not force every category to be non-empty. An empty array is correct when no item in that category can be identified from the image.

## Region Example

```json
{
  "label": "conference table area",
  "approx_location": "center of the room",
  "source": "manual"
}
```

Use a stable, concise label across views when they show the same region. Do not claim two views belong to the same physical region unless the visual evidence supports it.

## Object Example

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

- Record only an object visibly present in this image.
- Keep attributes short and directly observable.
- Describe approximate location in natural language relative to visible scene content.
- Keep `confidence: null` for manual annotation. Do not invent numeric confidence.
- Keep `bbox_2d: null` unless a real normalized image box was deliberately annotated.
- Keep `bbox_3d: null` unless a real target was localized using valid depth and documented computation. A guessed box is forbidden and is never GT.
- Keep `source: manual`.

## Landmark, Sign, And Facility Example

```json
{
  "label": "exit sign",
  "kind": "sign",
  "approx_location": "above the doorway on the right",
  "source": "manual"
}
```

Allowed `kind` values:

| Kind | Use for |
|---|---|
| `landmark` | Distinctive visible structure or feature useful for orientation. |
| `sign` | Visible sign, label, directional marker, or notice. |
| `facility` | Visible functional facility such as reception, restroom entrance, or service point. |

Do not infer a facility from expected building layout when it is not visible.

## What Not To Do

- Do not copy annotations from the `default` scene or another PLY.
- Do not use filenames, scene names, or expectations as evidence for invisible objects.
- Do not convert an empty template into a negative `found=false` result.
- Do not label model-generated or stub text as manual.
- Do not change `semantic_index_mode` to `live` or `cached_live` without a real provider response and provenance.
- Do not treat manual ViewJSON, tree nodes, or derived boxes as independent GT.

## Build The Tree

After all views in one scene have factual summaries and any visible semantic entries, run:

```powershell
python -B scripts\build_scene_tree_from_viewjson.py `
  --scene backend\data\scenes\<scene_id> `
  --views backend\data\scenes\<scene_id>\views `
  --out backend\data\scenes\<scene_id>\tree
```

The builder is deterministic. It creates region nodes by exact normalized region label and per-view object/landmark/sign/facility nodes. It never invents missing semantic nodes. Empty semantic content produces only `node_root.json` and an incomplete manifest.

## Validate The Index

```powershell
python -B scripts\validate_semantic_index.py `
  --scene backend\data\scenes\<scene_id> `
  --out docs\validation\semantic_index\<scene_id>_semantic_index.json
```

Review these fields:

```text
valid_view_json_count
invalid_view_json_count
visible_region_count
visible_object_count
landmark_count
sign_count
facility_count
tree_complete
tree_valid
query_runner_loadable
query_runner_schema_compatible
semantic_eval_allowed
errors
warnings
```

After Phase H, `query_runner_schema_compatible=true` is expected. This does not override content checks: empty summaries, zero semantic items, or an incomplete tree still force `semantic_eval_allowed=false`.

## Completion Checklist

- Every captured frame has one schema-valid ViewJSON file.
- Every ViewJSON has a non-empty factual summary based on its referenced image.
- All semantic entries have `source: manual`.
- Manual confidence values are `null`.
- No guessed 2D/3D boxes were added.
- The tree builder reports semantic items and no empty-summary warning.
- The validator has zero ViewJSON/tree errors.
- Manual annotations are documented as semantic-index inputs, not GT.
