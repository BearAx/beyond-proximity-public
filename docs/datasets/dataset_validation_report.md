# Dataset Validation Report

Status date: 2026-06-23. Updated for the revised Week 3 Phase A gate.

## Import Command

```powershell
python -B scripts/import_replica_scene.py `
  --batch scenes `
  --output backend/data/scenes
```

All five standalone PLY assets were copied byte-for-byte to the canonical `backend/data/scenes/<scene_id>/geometry/scene.ply` layout. Each output also contains `source_metadata.json` and `scene_manifest.json`. No RGB, depth, pose, intrinsics, semantic-label, instance-label, or GT-box files were generated.

## Command

```powershell
python -B scripts/validate_scene_geometry.py `
  --scenes `
    backend/data/scenes/ConferenceHall `
    backend/data/scenes/Museume `
    backend/data/scenes/outdoor-drone `
    backend/data/scenes/outdoor-street `
    backend/data/scenes/Theater `
  --out docs/validation/geometry/
```

Output:

```text
Wrote docs\validation\geometry\ConferenceHall_geometry.json
scene=ConferenceHall layout=ply_backend frames=0 semantic=False 3d=False
Wrote docs\validation\geometry\Museume_geometry.json
scene=Museume layout=ply_backend frames=0 semantic=False 3d=False
Wrote docs\validation\geometry\outdoor-drone_geometry.json
scene=outdoor-drone layout=ply_backend frames=0 semantic=False 3d=False
Wrote docs\validation\geometry\outdoor-street_geometry.json
scene=outdoor-street layout=ply_backend frames=0 semantic=False 3d=False
Wrote docs\validation\geometry\Theater_geometry.json
scene=Theater layout=ply_backend frames=0 semantic=False 3d=False
summary scenes=5 semantic_allowed=0 3d_allowed=0
```

## Coverage-Greedy View Selection

```powershell
python -B scripts/select_views_coverage_greedy.py `
  --scenes `
    backend/data/scenes/ConferenceHall `
    backend/data/scenes/Museume `
    backend/data/scenes/outdoor-drone `
    backend/data/scenes/outdoor-street `
    backend/data/scenes/Theater `
  --out docs/validation/geometry `
  --k 10 20 50 100 `
  --seed 42
```

The batch completed for all five scenes. Each normalized asset has zero frame or camera-pose records, so the selector used all zero available views for every requested K and emitted a warning. Coverage-greedy, random, and trajectory records are saved with `status: not_available` and `coverage_ratio: null`; no strategy comparison is claimed.

| scene_id | candidates | requested K | effective K | greedy | random | trajectory | report |
|---|---:|---|---|---|---|---|---|
| `ConferenceHall` | 0 | 10, 20, 50, 100 | 0, 0, 0, 0 | `N/A` | `N/A` | `N/A` | [`ConferenceHall_view_selection.json`](../validation/geometry/ConferenceHall_view_selection.json) |
| `Museume` | 0 | 10, 20, 50, 100 | 0, 0, 0, 0 | `N/A` | `N/A` | `N/A` | [`Museume_view_selection.json`](../validation/geometry/Museume_view_selection.json) |
| `outdoor-drone` | 0 | 10, 20, 50, 100 | 0, 0, 0, 0 | `N/A` | `N/A` | `N/A` | [`outdoor-drone_view_selection.json`](../validation/geometry/outdoor-drone_view_selection.json) |
| `outdoor-street` | 0 | 10, 20, 50, 100 | 0, 0, 0, 0 | `N/A` | `N/A` | `N/A` | [`outdoor-street_view_selection.json`](../validation/geometry/outdoor-street_view_selection.json) |
| `Theater` | 0 | 10, 20, 50, 100 | 0, 0, 0, 0 | `N/A` | `N/A` | `N/A` | [`Theater_view_selection.json`](../validation/geometry/Theater_view_selection.json) |

## Machine-Readable Reports

- [`ConferenceHall_geometry.json`](../validation/geometry/ConferenceHall_geometry.json)
- [`Museume_geometry.json`](../validation/geometry/Museume_geometry.json)
- [`outdoor-drone_geometry.json`](../validation/geometry/outdoor-drone_geometry.json)
- [`outdoor-street_geometry.json`](../validation/geometry/outdoor-street_geometry.json)
- [`Theater_geometry.json`](../validation/geometry/Theater_geometry.json)

The existing [`default_geometry.json`](../validation/geometry/default_geometry.json) remains the report for the older backend `default` scene and is not counted among the five new scenes.

## Five-Scene Results

| scene_id | asset/header | RGB | depth | poses | RGB/depth resolution | intrinsics/resolution | constant depth | zero-depth ratio | invalid poses | missing frames | metadata consistency | semantic eval | 3D eval |
|---|---|---:|---:|---:|---|---|---|---|---|---|---|---|---|
| `ConferenceHall` | valid PLY | 0 | 0 | 0 | `N/A` | `N/A` - intrinsics missing | `N/A` - depth missing | `N/A` - depth missing | `N/A` - poses missing | detected | consistent generated metadata | invalid | invalid |
| `Museume` | valid PLY | 0 | 0 | 0 | `N/A` | `N/A` - intrinsics missing | `N/A` - depth missing | `N/A` - depth missing | `N/A` - poses missing | detected | consistent generated metadata | invalid | invalid |
| `outdoor-drone` | valid PLY | 0 | 0 | 0 | `N/A` | `N/A` - intrinsics missing | `N/A` - depth missing | `N/A` - depth missing | `N/A` - poses missing | detected | consistent generated metadata | invalid | invalid |
| `outdoor-street` | valid PLY | 0 | 0 | 0 | `N/A` | `N/A` - intrinsics missing | `N/A` - depth missing | `N/A` - depth missing | `N/A` - poses missing | detected | consistent generated metadata | invalid | invalid |
| `Theater` | valid PLY | 0 | 0 | 0 | `N/A` | `N/A` - intrinsics missing | `N/A` - depth missing | `N/A` - depth missing | `N/A` - poses missing | detected | consistent generated metadata | invalid | invalid |

`invalid` means invalid for that evaluation family, not that the PLY file is corrupt. All five PLY headers are readable SuperSplat exports. They are blocked because the evaluation pipeline has no frame/camera/GT inputs for them.

## Required Check Behavior

The batch reports use explicit availability states so unavailable measurements cannot look like successful checks:

| Required check | PLY-only report behavior |
|---|---|
| RGB count | `0`, `measured_absent` |
| depth count | `0`, `measured_absent` |
| pose count | `0`, `measured_absent` |
| RGB/depth resolution match | `N/A` because both modalities are absent |
| intrinsics/resolution match | `N/A` because intrinsics and RGB are absent |
| constant depth | `N/A`, not zero failures/passed |
| zero-depth ratio | `N/A`, not zero failures/passed |
| invalid pose matrices | `N/A` because no matrices exist |
| missing frames | detected with `checks.missing_frames = 1` |
| metadata consistency | `consistent` for generated import manifest/provenance; original metadata remains unavailable |

The numeric `checks.constant_depth`, `checks.excessive_zero_depth`, and mismatch counters remain `0` because there are no samples to count. Their corresponding `check_availability` fields are `N/A`, which prevents those zeros from being interpreted as passes.

## Validator Changes

The importer and validator now support:

- PLY-only single and batch import into a canonical backend path.
- Generated source provenance that explicitly records original metadata as unavailable.
- Manifest paths with null unavailable modalities instead of fabricated files.
- Backward-compatible single-scene validation with `--scene` and `--output`.
- Batch validation with `--scenes ... --out <directory>`.
- Standalone `.ply` header validation without reading the full binary payload.
- Explicit PLY-only blocked reports when RGB-D and camera inputs are absent.
- Metadata discovery and consistency checks for scene ID, frame count, and declared paths.
- Duplicate scene-ID protection to prevent batch output overwrites.
- Relative scene paths in reports when assets are inside the repository.
- Canonical PLY scene input detection for downstream view-selection tooling.

The PLY parser records format, comments, element counts, properties, and whether any semantic/instance-like property exists. All five files contain only packed position, rotation, scale, and color properties; packed color is not treated as semantic GT.

## Selector and Config Changes

The selector now supports both `--scene/--output` and `--scenes/--out`. Pose-bearing scenes still run deterministic coverage-greedy, seeded random, and trajectory comparisons. Empty scenes complete with explicit unavailable records, requested/effective K values, candidate and covered counts, warnings, and aggregate coverage statistics.

Both `configs/week2_replica.yaml` and `configs/week3_replica.yaml` use JSON-compatible YAML and list the five canonical scene paths. Their active mode is `stub`; `cached_live` and `live` remain selectable modes when verified cache/provider support is configured. Every scene references its geometry and view-selection reports and is marked `semantic_eval_allowed: false` and `geometry_eval_allowed: false`, matching validation.

The headless runner validates structured scene entries against their geometry reports. Ineligible scenes are loaded, depth/view availability is checked, and then they are logged as `skipped_ineligible`. It writes canonical `availability_status: unavailable` query records for gate coverage without creating synthetic views or semantic predictions.

```powershell
python -B scripts/run_experiment.py --config configs/week3_replica.yaml --mode stub
```

The Week 3 run completed in `stub` mode with five configured scenes and five `skipped_ineligible` statuses. It wrote 40/40 canonical unavailable records, eight per scene, with zero model calls and zero accuracy-eligible records.

## Regression Validation

```powershell
python -m py_compile scripts/select_views_coverage_greedy.py scripts/validate_scene_geometry.py scripts/run_experiment.py
python -B -m pytest -q tests/backend/test_dataset_ingestion.py
python -B -m pytest -q tests/backend/test_experiment_outputs.py
python -B -m pytest -q
```

Result:

```text
9 passed in 0.44s
3 passed in 0.44s
57 passed in 2.93s
```

The relevant tests include:

- Constant-depth detection.
- Excessive zero-depth detection.
- RGB/depth resolution mismatch detection.
- Intrinsics/RGB resolution mismatch detection.
- Invalid pose detection.
- Missing-frame detection.
- PLY-only scenes remaining blocked with depth checks marked `N/A`.
- Metadata scene-ID/frame-count inconsistency detection.
- Pose-bearing greedy/random/trajectory comparison and K reduction.
- Zero-view reports with null coverage instead of fabricated scores.
- Structured ineligible-scene batches completing with explicit skip status.
- Missing-GT queries remaining outside every accuracy denominator.
- Canonical unavailable outputs retaining stub provenance and zero model calls.

The existing failure fixture still asserts `constant_depth = 1`, `excessive_zero_depth = 1`, and `intrinsics_resolution_mismatch = 2`, so those conditions remain detected and are not ignored.

## Eligibility Summary

| Item | Count |
|---|---:|
| New scene reports generated | 5 |
| New view-selection reports generated | 5 |
| Scenes processed by the view-selection batch | 5 |
| Scenes with candidate camera views | 0 |
| Scenes with strategy comparisons available | 0 |
| Structurally readable PLY assets | 5 |
| Scenes valid for semantic evaluation | 0 |
| Scenes valid for 3D evaluation | 0 |
| Scenes with measurable depth quality | 0 |
| Scenes with generated import metadata consistency available | 5 |
| Five-scene benchmark queries processed | 40 |
| Five-scene benchmark queries with GT | 0 |
| Canonical stub outputs | 40 |
| Semantic predictions produced | 0 |
| Live/cached-live runs | 0 |

## Final Evaluation Status

| Question | Answer |
|---|---|
| How many scenes were added? | 5 |
| How many passed semantic validation? | 0/5 |
| How many passed 3D validation? | 0/5 |
| How many queries were run through the gate? | 40 scoped records; 0 executable semantic queries |
| How many scoped queries had GT? | 0/40; the separate legacy `default` benchmark has 50 ViewJSON/tree-derived expectations |
| Which metrics are real? | PLY/import integrity, validation outcomes, output coverage 40/40, schema validity 40/40, per-scene counts, and stub provenance |
| Which metrics are unavailable? | semantic retrieval/view/node/zone/object/negative accuracy, token usage, live latency, and cost |
| Which metrics are `N/A`? | camera-view coverage statistics, predicted 3D boxes, and 3D IoU |
| Which mode ran? | `stub`; live and cached-live were not run |
| Was ScanNet postponed? | yes |

## Blockers

- The five assets contain no RGB/depth frames, poses, intrinsics, or original dataset metadata.
- The five assets contain no independent semantic labels, instance labels, or GT 3D boxes.
- Original dataset/source provenance is unknown beyond the SuperSplat generator comment.
- Numeric coverage-greedy/random/trajectory comparisons remain unavailable until camera poses and frame records exist.
- Semantic evaluation remains blocked until canonical frame and index data exist.
- 3D metrics remain `N/A` until valid depth, cameras, GT, and predicted 3D boxes exist.
- `SEMANTICSPLAT_PROVIDER`, `SEMANTICSPLAT_MODEL`, and `SEMANTICSPLAT_API_KEY` are absent; no live cache exists.
- ScanNet remains postponed and was not added.

## Initial Manual Capture Pilot Gate (2026-06-22)

The initial single-scene browser capture path was validated on five views in `ConferenceHall-capture-pilot`. At that historical gate, the other scenes had not yet been captured.

Implemented checks:

- Spark renderer-derived logarithmic splat depth instead of the previous color-buffer placeholder path;
- top-left RGB/depth row alignment;
- actual drawing-buffer intrinsics from the camera projection matrix;
- valid camera-to-world pose enforcement;
- constant/no-positive depth rejection before files are saved;
- deterministic `images/`, `depths/`, `captures/`, and `transforms.json` paths;
- per-frame capture metadata and calibration consistency;
- pilot checker at `scripts/check_capture_pilot.py`;
- semantic eligibility requires ViewJSON/tree;
- 3D eligibility requires valid geometry inputs and independent 3D GT.

Pilot measurements:

```text
rgb/depth/pose counts=5/5/5
rgb/depth resolution=2340x1170
depth min/max/mean=0.1/100.0/15.0844
depth_is_constant=false
zero_depth_ratio=0.003443
valid_poses=5/5
intrinsics_match_canvas=true
per_frame_metadata=complete
scaling_allowed=true
```

The general validator reports `geometry_inputs_valid=true` and zero frame, depth, resolution, intrinsics, or pose failures. It reports semantic evaluation false because ViewJSON/tree and independent semantic GT are missing, and 3D localization false because independent 3D GT is missing. It also warns that scene-level metadata consistency is unavailable; the pilot has complete per-frame capture metadata but no `source_metadata.json` or `scene_manifest.json`.

At that gate, five-scene eligibility remained 0/5 semantic and 0/5 3D, and capture mechanics were approved for scaling. The current capture audit appears below.

Capture-hardening regression result: frontend production build passed; full backend suite passed with `60 passed in 3.33s`. Frontend lint was not run because the configured `eslint` executable is not declared/installed in `frontend/package.json`.

### First Manual Attempt

The 2026-06-22 attempt was written to `backend/data/scenes/default`, not `ConferenceHall-capture-pilot`. The general validator reported:

```text
frames=22
rgb=22
depth=22
valid_poses=22
constant_depth_frames=19
intrinsics_resolution_mismatch=22
semantic_evaluation_allowed=false
geometry_inputs_valid=false
three_d_localization_allowed=false
```

The six reported captures `v001`-`v006` are constant at `0.1`. Three later frames `v020`-`v022` are non-constant, showing the new frontend renderer-depth path can produce varying values, but they have no capture metadata and use stale 800x600 intrinsics because the running API was not restarted. This mixed scene is not a valid pilot and does not permit scaling.

Evidence: `docs/validation/geometry/ConferenceHall_capture_default_geometry.json`.

### Successful Pilot Evidence

The clean second attempt is recorded in `docs/validation/geometry/ConferenceHall_capture_pilot_geometry.json`. It supersedes the failed `default` attempt as capture-mechanics evidence, but it does not make the pilot or any of the five source scenes eligible for semantic or 3D evaluation.

## Revised Week 3 Phase A Audit

Capture validation evidence was generated on 2026-06-22 and re-audited with current semantic reports on 2026-06-23:

```powershell
python -B scripts\check_capture_batch.py `
  --scenes `
    backend\data\scenes\ConferenceHall-capture-pilot `
    backend\data\scenes\Museume-capture `
    backend\data\scenes\Theater-capture `
    backend\data\scenes\outdoor-drone-capture `
    backend\data\scenes\outdoor-street-capture `
  --out docs\validation\capture_quality
```

| scene_id | rgb_count | depth_count | pose_count | intrinsics_valid | depth_is_constant | poses_valid | intrinsics_match_canvas | semantic_index_exists | tree_exists | semantic_eval_allowed | geometry_eval_allowed | warnings |
|---|---:|---:|---:|---|---|---|---|---|---|---|---|---|
| `ConferenceHall-capture-pilot` | 20 | 20 | 20 | true | false | true | true | true - 20 annotated views | true - complete | true | false | 207 semantic items; independent semantic/3D GT unavailable. |
| `Museume-capture` | 20 | 20 | 20 | true | false | true | true | true - 20 annotated views | true - complete | true | false | 225 semantic items; independent semantic/3D GT unavailable. |
| `Theater-capture` | 20 | 20 | 20 | true | false | true | true | true - 20 annotated views | true - complete | true | false | 226 semantic items; independent semantic/3D GT unavailable. |
| `outdoor-drone-capture` | 16 | 16 | 16 | true | false | true | true | true - 16 annotated views | true - complete | true | false | 169 semantic items; zero-depth ratio 0.403705 needs caution; independent GT unavailable. |
| `outdoor-street-capture` | 20 | 20 | 20 | true | false | true | true | true - 20 annotated views | true - complete | true | false | 219 semantic items; independent semantic/3D GT unavailable. |

Machine-readable capture reports are `docs/validation/capture_quality/<scene_id>_capture_check.json`. Summary: 5 scenes checked, 5 capture scale gates passed, 5 semantic-index gates passed after annotation, and 0 geometry gates passed.

All captures use 2340x1170 RGB/depth, non-constant renderer depth, valid poses, matching intrinsics, and complete per-frame metadata. Poses and intrinsics are embedded in `transforms.json`; metadata is stored as `captures/vNNN.json`. Separate `poses.json`, `intrinsics.json`, and scene-level `metadata.json` files are absent by design in the current capture path.

Phase C populated `views/` with 96 `manual` templates. These files now contain image-based annotations. Rebuilding generated five complete trees from 1,046 semantic items without inventing labels.

Phase E validation reports confirm 96 valid annotated views, zero invalid files, five complete trees, and `semantic_eval_allowed=true` for all scenes. Phase H captured ViewJSON v1 matching preserves the legacy path; all reports have `query_runner_loadable=true` and `query_runner_schema_compatible=true`. Geometry evaluation remains false because independent GT boxes/masks and predicted 3D boxes are absent.

## Revised Week 3 Phase B Attempt

On 2026-06-23, template generation was rerun without `--overwrite`, so all 96 existing files were preserved. The five trees and semantic reports were regenerated from actual template contents.

| scene_id | templates | filled summaries | semantic items | tree complete | semantic eval | geometry eval |
|---|---:|---:|---:|---|---|---|
| `ConferenceHall-capture-pilot` | 20 | 20 | 207 | true | true | false |
| `Museume-capture` | 20 | 20 | 225 | true | true | false |
| `Theater-capture` | 20 | 20 | 226 | true | true | false |
| `outdoor-drone-capture` | 16 | 16 | 169 | true | true | false |
| `outdoor-street-capture` | 20 | 20 | 219 | true | true | false |

All five semantic indexes pass validation and exceed the revised Phase B minimum of 3/5 executable scenes. A separate five-query stub smoke produced five available, schema-valid results with zero model calls. Manual annotations are index inputs rather than independent GT, so accuracy remains unavailable; geometry remains disabled.
