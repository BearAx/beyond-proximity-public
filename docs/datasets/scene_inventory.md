# Scene Inventory

Status date: 2026-06-23. Updated for the revised Week 3 Phase A gate.

## Canonical Layout

The five PLY-only scenes use this backend layout:

```text
backend/data/scenes/<scene_id>/
  geometry/
    scene.ply
  source_metadata.json
  scene_manifest.json
```

RGB-D files are not created because they were not supplied. The manifest sets `rgb`, `depth`, `poses`, `intrinsics`, and `semantic_index` paths to null. `source_metadata.json` is generated provenance for the import operation; it is not original dataset metadata or GT.

Reproduction:

```powershell
python -B scripts/import_replica_scene.py `
  --batch scenes `
  --output backend/data/scenes
```

Use `--overwrite` to repeat the command against existing normalized outputs. No manual file editing is required.

## Five-Scene Inventory

| scene_id | raw scene_path | normalized backend path | dataset/source | status | rgb_count | depth_count | pose_count | intrinsics_status | metadata_status | gt_room_labels | gt_instances | gt_3d_boxes | usable_for_semantic_eval | usable_for_3d_eval | warnings |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|---|---|---|---|
| `ConferenceHall` | `scenes/ConferenceHall.ply` | `backend/data/scenes/ConferenceHall` | Unknown original source; local SuperSplat 2.13.6 export | normalized PLY backend scene | 0 | 0 | 0 | missing | generated import metadata consistent; original metadata unavailable | `N/A` | `N/A` | `N/A` | no | no | 6,133,531 packed Gaussian vertices; no frames, cameras, semantic GT, or backend semantic index. |
| `Museume` | `scenes/Museume.ply` | `backend/data/scenes/Museume` | Unknown original source; local SuperSplat 2.13.6 export | normalized PLY backend scene | 0 | 0 | 0 | missing | generated import metadata consistent; original metadata unavailable | `N/A` | `N/A` | `N/A` | no | no | 7,389,888 packed Gaussian vertices; filename spelling remains unverified. |
| `outdoor-drone` | `scenes/outdoor-drone.ply` | `backend/data/scenes/outdoor-drone` | Unknown original source; local SuperSplat 2.13.6 export | normalized PLY backend scene | 0 | 0 | 0 | missing | generated import metadata consistent; original metadata unavailable | `N/A` | `N/A` | `N/A` | no | no | 3,185,436 packed Gaussian vertices; no frames, cameras, semantic GT, or backend semantic index. |
| `outdoor-street` | `scenes/outdoor-street.ply` | `backend/data/scenes/outdoor-street` | Unknown original source; local SuperSplat 2.13.6 export | normalized PLY backend scene | 0 | 0 | 0 | missing | generated import metadata consistent; original metadata unavailable | `N/A` | `N/A` | `N/A` | no | no | 10,450,440 packed Gaussian vertices; no frames, cameras, semantic GT, or backend semantic index. |
| `Theater` | `scenes/Theater.ply` | `backend/data/scenes/Theater` | Unknown original source; local SuperSplat 2.13.6 export | normalized PLY backend scene | 0 | 0 | 0 | missing | generated import metadata consistent; original metadata unavailable | `N/A` | `N/A` | `N/A` | no | no | 7,492,852 packed Gaussian vertices; no frames, cameras, semantic GT, or backend semantic index. |

`packed_color` is visual appearance, not semantic or instance GT.

## Canonical Asset Locations

| scene_id | Gaussian splat | RGB | depth | poses | intrinsics | metadata | semantic labels | instance labels | GT boxes | ViewJSON/tree |
|---|---|---|---|---|---|---|---|---|---|---|
| `ConferenceHall` | `backend/data/scenes/ConferenceHall/geometry/scene.ply` | missing | missing | missing | missing | `source_metadata.json`, `scene_manifest.json` | missing | missing | missing | missing |
| `Museume` | `backend/data/scenes/Museume/geometry/scene.ply` | missing | missing | missing | missing | `source_metadata.json`, `scene_manifest.json` | missing | missing | missing | missing |
| `outdoor-drone` | `backend/data/scenes/outdoor-drone/geometry/scene.ply` | missing | missing | missing | missing | `source_metadata.json`, `scene_manifest.json` | missing | missing | missing | missing |
| `outdoor-street` | `backend/data/scenes/outdoor-street/geometry/scene.ply` | missing | missing | missing | missing | `source_metadata.json`, `scene_manifest.json` | missing | missing | missing | missing |
| `Theater` | `backend/data/scenes/Theater/geometry/scene.ply` | missing | missing | missing | missing | `source_metadata.json`, `scene_manifest.json` | missing | missing | missing | missing |

## Import Integrity

| scene_id | size (bytes) | SHA-256 | source/canonical match |
|---|---:|---|---|
| `ConferenceHall` | 99,862,273 | `8B0944359404E91F7BEB1C4EAD241E914A3D82BF1159722CA7CBBB0306F0AFA7` | yes |
| `Museume` | 120,317,289 | `7B32AD32EE1453510B7A7F4AB3DB2942664FCD1D86C5FBBC03914F94D6E598BD` | yes |
| `outdoor-drone` | 51,863,601 | `71B35E03D66CDE8AA8C17F5B504AC64FA3F3D84CAC8BF3064611CC57031244F6` | yes |
| `outdoor-street` | 170,146,954 | `0D2F7C21A219415CE79D9102D7D9EA935709C24FA06E9C3FFF4BAA85F49084B5` | yes |
| `Theater` | 121,993,657 | `BB4458C7707F3E1523BA9AABB2F6CBA73377732FFA28EB552F72D3A7F2CE4C03` | yes |

The PLY files remain ignored by the repository-wide `*.ply` rule. The small manifests and provenance files document how to recreate canonical local copies from the ignored raw assets.

## Existing Reference Scene

`backend/data/scenes/default/` remains the existing backend reference scene and is not one of the five additions. After the failed manual pilot attempt it contains 22 frame records. Nineteen depth maps are constant, all 22 frames mismatch the stale 800x600 intrinsics, capture metadata is absent, and the semantic index covers only the earlier 19 views. It remains invalid for semantic and 3D evaluation at this expanded frame count.

## Evaluation Linkage

| Item | Count/status |
|---|---|
| Added scenes | 5 |
| Semantic-evaluation eligible | 0/5 |
| 3D-evaluation eligible | 0/5 |
| Five-scene benchmark records | 40, all without GT |
| Week 3 canonical gate outputs | 40/40 in `stub` mode |
| Executable semantic predictions | 0 |
| Live/cached-live execution | not run; provider environment and verified cache unavailable |
| ScanNet | 8 official BBQ-aligned scenes imported; 39 RGB-D views, 392 GT boxes, 48-query Nr3D/Sr3D+ run complete |

The gate outputs prove output/schema handling only. They do not convert these PLY-only assets into semantic or 3D evaluation scenes.

## Summary and Blockers

- Newly added scene assets found: 5.
- Newly added scenes normalized for the backend: 5.
- Imports requiring manual file editing: 0.
- Newly added scenes usable for semantic evaluation: 0.
- Newly added scenes usable for 3D evaluation: 0.
- Original dataset provenance and independent GT: unavailable for all 5.
- RGB/depth frames, poses, and intrinsics: unavailable for all 5.
- Raw ZIP files or temporary extraction directories: none.
- ScanNet: this historical five-scene gate remains separate, but the public
  track is now complete under `backend/data/scenes/scannet_*` with validation in
  `docs/validation/public_datasets/scannet_*.json`.

Normalization makes paths and provenance consistent; it does not create missing evaluation evidence. Semantic and 3D eligibility remain blocked honestly.

## Initial Manual Capture Pilot Evidence (2026-06-22)

The initial `ConferenceHall-capture-pilot` gate used five valid views before the capture set was expanded:

| scene_id | status | rgb_count | depth_count | pose_count | intrinsics | per-frame metadata | ViewJSON/tree | independent semantic GT | independent 3D GT | semantic eval | 3D eval |
|---|---|---:|---:|---:|---|---|---|---|---|---|---|
| `ConferenceHall-capture-pilot` | capture scale gate passed | 5 | 5 | 5 | valid, 2340x1170 | complete, 5/5 | missing | missing | missing | no | no |

Depth is renderer-derived and non-constant (`min=0.1`, `max=100.0`, `mean=15.0844`, zero ratio `0.003443`). All five poses are valid and RGB/depth resolutions match. The general validator reports `geometry_inputs_valid=true`, but scene-level import provenance/manifest metadata is absent and source-PLY coordinate/scale alignment remains unverified.

This historical pilot did not alter the separate canonical PLY-only directories. The current capture-directory status is reported in the table below.

The pilot checker reported `scaling_allowed=true`, which authorized the completed manual capture campaign. See `docs/datasets/manual_capture_pilot.md` for the original gate.

## Revised Week 3 Phase A Audit

This table tracks the actual capture directories, not the separate canonical PLY-only directories above. It supersedes the earlier one-scene readiness table.

| scene_id | rgb_count | depth_count | pose_count | intrinsics_valid | depth_is_constant | poses_valid | intrinsics_match_canvas | semantic_index_exists | tree_exists | semantic_eval_allowed | geometry_eval_allowed | warnings |
|---|---:|---:|---:|---|---|---|---|---|---|---|---|---|
| `ConferenceHall-capture-pilot` | 20 | 20 | 20 | true | false | true | true | true - 20 annotated views | true - 201 nodes, complete | true | false | 207 semantic items; independent semantic/3D GT unavailable. |
| `Museume-capture` | 20 | 20 | 20 | true | false | true | true | true - 20 annotated views | true - 222 nodes, complete | true | false | 225 semantic items; independent semantic/3D GT unavailable. |
| `Theater-capture` | 20 | 20 | 20 | true | false | true | true | true - 20 annotated views | true - 221 nodes, complete | true | false | 226 semantic items; independent semantic/3D GT unavailable. |
| `outdoor-drone-capture` | 16 | 16 | 16 | true | false | true | true | true - 16 annotated views | true - 159 nodes, complete | true | false | 169 semantic items; zero-depth ratio 0.403705 needs caution; independent GT unavailable. |
| `outdoor-street-capture` | 20 | 20 | 20 | true | false | true | true | true - 20 annotated views | true - 216 nodes, complete | true | false | 219 semantic items; independent semantic/3D GT unavailable. |

All 96 poses are stored in `transforms.json`, which also stores the valid 2340x1170 intrinsics. All 96 per-frame metadata records are stored under `captures/`. Separate `poses.json`, `intrinsics.json`, and `metadata.json` files are not required by this backend layout and are absent.

Batch result: 5/5 capture-valid, 5/5 semantic-index executable, and 0/5 geometry-evaluation-ready. All 96 `manual` ViewJSON files are annotated and all five generated trees are complete. Manual descriptions are semantic-index inputs, not independent GT, so semantic accuracy remains unavailable.

Phase E reports are stored as `docs/validation/semantic_index/<scene_id>_semantic_index.json`. All 96 views pass structural/reference validation; every report has `tree_valid=true`, `query_runner_loadable=true`, `query_runner_schema_compatible=true`, and `semantic_eval_allowed=true`. Geometry remains false because independent GT boxes/masks and predicted 3D boxes are absent.
