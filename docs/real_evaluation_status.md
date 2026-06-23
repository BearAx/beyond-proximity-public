# Real Evaluation Status

Status date: 2026-06-23. Updated for the revised Week 3 Phase A gate.

## Overall Status

Manual RGB-D capture is valid for all five capture scenes: 96 RGB frames, 96 depth maps, 96 poses, matching intrinsics, and complete per-frame capture metadata. This is real measured capture evidence, not stub output.

No five-scene semantic accuracy evaluation or 3D localization evaluation has been completed. Phase C created 96 empty manual ViewJSON templates. Phase D built a root-only tree for each scene, explicitly marked incomplete because no template contains semantic content. Independent semantic GT and independent 3D boxes/masks remain unavailable.

## Revised Week 3 Phase A Audit

| scene_id | rgb_count | depth_count | pose_count | intrinsics_valid | depth_is_constant | poses_valid | intrinsics_match_canvas | semantic_index_exists | tree_exists | semantic_eval_allowed | geometry_eval_allowed | warnings |
|---|---:|---:|---:|---|---|---|---|---|---|---|---|---|
| `ConferenceHall-capture-pilot` | 20 | 20 | 20 | true | false | true | true | true - 20 empty templates | true - root only, incomplete | false | false | 0 semantic items; independent semantic/3D GT and predicted 3D boxes unavailable. |
| `Museume-capture` | 20 | 20 | 20 | true | false | true | true | true - 20 empty templates | true - root only, incomplete | false | false | 0 semantic items; independent semantic/3D GT and predicted 3D boxes unavailable. |
| `Theater-capture` | 20 | 20 | 20 | true | false | true | true | true - 20 empty templates | true - root only, incomplete | false | false | 0 semantic items; independent semantic/3D GT and predicted 3D boxes unavailable. |
| `outdoor-drone-capture` | 16 | 16 | 16 | true | false | true | true | true - 16 empty templates | true - root only, incomplete | false | false | Zero-depth ratio 0.403705 passes the capture threshold but needs caution; semantic/3D evidence unavailable. |
| `outdoor-street-capture` | 20 | 20 | 20 | true | false | true | true | true - 20 empty templates | true - root only, incomplete | false | false | 0 semantic items; independent semantic/3D GT and predicted 3D boxes unavailable. |

`capture_valid=true` means `scaling_allowed=true`: RGB/depth/pose counts match, depth is non-constant, pose matrices are valid, intrinsics match the 2340x1170 render canvas, and per-frame capture metadata is complete.

## Storage Layout

The capture scenes use `transforms.json` for poses and intrinsics and `captures/vNNN.json` for per-frame metadata. Separate `poses.json`, `intrinsics.json`, and scene-level `metadata.json` files are not present. This is the implemented backend capture layout, not missing pose/calibration data.

Each capture scene currently contains:

```text
images/vNNN.png
depths/vNNN_depth.npy
captures/vNNN.json
transforms.json
views/vNNN.json        # empty manual annotation templates
tree/manifest.json     # incomplete, generated from empty templates
tree/node_root.json    # root only; no semantic nodes
```

## Evidence Matrix

| Evidence | Status | Result |
|---|---|---|
| Capture validation | measured | 5/5 scenes passed; 96/96 RGB, depth, and pose records |
| Non-constant depth | measured | 5/5 scenes passed |
| Pose validity | measured | 96/96 valid |
| Intrinsics/render match | measured | 5/5 scenes at 2340x1170 |
| Semantic index eligibility | measured validation outcome | 0/5; 96 empty manual templates and no trees |
| Semantic accuracy | unavailable | no semantic execution and no independent GT |
| 3D evaluation eligibility | measured validation outcome | 0/5; independent GT boxes/masks and predictions absent |
| 3D IoU | `N/A` | no independent GT/predicted 3D boxes |
| Previous Week 3 stub gate | measured stub-only behavior | 40/40 schema records; not semantic predictions |
| Live/cached-live execution | unavailable | not run for these captured scenes |

## Current Blockers

- All 96 manual ViewJSON templates require real image-based annotation; zero are filled.
- Every scene has a generated root-only tree, but all five manifests are incomplete and contain zero semantic nodes.
- Independent semantic GT is missing; future manual semantic records cannot be reported as GT.
- Independent 3D boxes/masks and predicted 3D boxes are missing, so geometry evaluation and 3D IoU remain unavailable.
- The runner now loads captured ViewJSON/tree and preserves the legacy `default` path, but the five-scene semantic gate has not run because every index is incomplete.
- ScanNet remains postponed; baselines have not been run.

## Revised Week 3 Phase B Result

The Phase B commands were rerun on 2026-06-23. Template generation preserved all 96 existing files. Tree construction and batch validation produced:

```text
scenes validated = 5
valid ViewJSON references = 96
filled summaries = 0
semantic items = 0
complete trees = 0/5
semantic_eval_allowed = 0/5
geometry_eval_allowed = 0/5
executable semantic queries = 0
```

Phase B minimum acceptance (3/5 semantic executable) is not met. Manual image-based annotation is required for the exact files listed in `docs/manual_semantic_annotation_queue.md`.

## Phase Boundary

Phases B-H are complete: the schema, 96 templates, deterministic tree builder, validator, root-only incomplete trees, validation reports, manual guide, captured runner adapter, and five-scene config exist. The semantic gate was not run.
