# Manual Capture Pilot

Status: a clean five-view `ConferenceHall-capture-pilot` passed the capture-mechanics scale gate. Capture of the remaining scenes is paused for review.

## Successful Pilot: 2026-06-22

The second attempt was written to the intended scene and passed the pilot-specific checker:

| Check | Result |
|---|---|
| Scene directory | `backend/data/scenes/ConferenceHall-capture-pilot` |
| RGB/depth/pose counts | 5/5/5 |
| RGB/depth resolution | 2340x1170, matching |
| Depth min/max/mean | 0.1 / 100.0 / 15.0844 |
| Constant depth | false |
| Zero-depth ratio | 0.003443 |
| Poses | 5/5 valid |
| Intrinsics | valid and matched to the canvas |
| Per-frame capture metadata | complete |
| Capture scaling gate | passed |
| Semantic evaluation | not allowed |
| 3D evaluation | not allowed |

The general geometry validator also reports `geometry_inputs_valid=true`, with zero missing frames, resolution mismatches, constant-depth frames, excessive-zero-depth frames, or invalid poses. It still reports `three_d_localization_allowed=false` because independent 3D GT is absent. Its scene-level metadata check is unavailable because this capture-only directory has no `source_metadata.json` or `scene_manifest.json`; this is separate from the complete five per-frame files under `captures/`.

Saved report: `docs/validation/geometry/ConferenceHall_capture_pilot_geometry.json`.

## Failed First Attempt: 2026-06-22

The intended `ConferenceHall-capture-pilot` directory was not created. Captures were written into the existing `default` scene instead.

Observed result:

| Check | Result |
|---|---|
| Actual scene directory | `backend/data/scenes/default` |
| Total frame records after capture | 22 |
| Six reported captures | `v001`-`v006`, overwritten in `default` |
| Six-capture depth | constant `0.1` in every frame |
| Additional recent frames | `v020`-`v022`, non-constant renderer-derived depth |
| Intrinsics | stale `800x600`; all 22 RGB frames mismatch |
| Capture metadata | missing for all frames |
| Poses | 22/22 valid matrices |
| Semantic index | incomplete for 22-frame scene |
| Scaling | false |
| Semantic evaluation | false |
| Geometry evaluation | false |

Saved report: `docs/validation/geometry/ConferenceHall_capture_default_geometry.json`.

The mixed result indicates that the new frontend depth path was active for `v020`-`v022`, but the running backend was not restarted and therefore continued using the old persistence route without metadata or calibration replacement. The six requested captures are not a valid pilot.

## Scope

Capture only 3-5 views from `ConferenceHall.ply` into backend scene ID `ConferenceHall-capture-pilot`, validate them, and stop for review.

Do not create placeholder files. Do not capture the other four scenes. Do not create ViewJSON/tree until RGB-D capture passes. Do not change semantic or geometry eligibility flags.

## What Pressing R Does

1. Saves the visible drawing buffer as RGB PNG.
2. Renders a separate Spark depth-color pass using real view-space splat-center depth.
3. Decodes logarithmic depth to a top-left float32 array and rejects empty/constant output.
4. Exports the camera-to-world matrix in documented Three.js coordinates.
5. Derives intrinsics from the current projection matrix and actual drawing-buffer dimensions.
6. Posts one validated payload to `/api/captures/save`.

The API writes deterministic paths:

```text
backend/data/scenes/ConferenceHall-capture-pilot/
  images/v001.png
  depths/v001_depth.npy
  captures/v001.json
  transforms.json
```

`captures/v001.json` records `scene_id`, `frame_id`, image/depth paths, pose reference and convention, intrinsics reference, source PLY URL, depth source/range/statistics, and capture timestamp.

## Start the Pilot

From repository root, Terminal 1:

```powershell
$env:PYTHONPATH = "."
python -m backend.api.server
```

Terminal 2:

```powershell
Set-Location frontend
npm.cmd install
npm.cmd run dev
```

The frontend dynamically loads Spark.js and Three.js CDN modules, so browser network access is required.

## UI Steps

1. Open `http://localhost:5173`.
2. Set **Scene ID** to `ConferenceHall-capture-pilot` and click **Set**.
3. Select `ConferenceHall.ply` under **3D Scene** and click **Load** if needed.
4. Wait until the scene is visibly rendered. Never capture a loading, blank, or error canvas.
5. Click the canvas to lock the mouse.
6. Navigate with `W/A/S/D`, mouse look, `Q/E` vertically, and Shift for boost.
7. Press `R` at 3-5 diverse positions with useful scene content.
8. Confirm each capture appears in the sidebar. A rejected depth capture appears as a red error and writes no frame.
9. Stop after 3-5 successful captures. Do not switch to another PLY scene.

## Sanity Check

Run:

```powershell
python -B scripts\check_capture_pilot.py --scene backend\data\scenes\ConferenceHall-capture-pilot
```

The report prints:

```text
rgb_count
depth_count
pose_count
intrinsics_status
metadata_status
rgb_resolution
depth_resolution
depth_min
depth_max
depth_mean
depth_is_constant
zero_depth_ratio
pose_validity
intrinsics_match_canvas
semantic_eval_allowed
geometry_eval_allowed
scaling_allowed
warnings
```

Then run:

```powershell
python -B scripts\validate_scene_geometry.py `
  --scene backend\data\scenes\ConferenceHall-capture-pilot `
  --output docs\validation\geometry\ConferenceHall_capture_pilot_geometry.json
```

## Pass Criteria

Scaling is allowed only if all are true:

- `scaling_allowed = true`;
- depth is present and `depth_is_constant = false`;
- RGB, depth, pose, and metadata counts equal the frame count;
- RGB/depth resolutions match;
- `intrinsics_match_canvas = true`;
- every pose is valid;
- metadata status is complete;
- zero/invalid depth ratio is at most 0.5.

If any condition fails, stop. Do not capture all five scenes.

## Eligibility Interpretation

- Passing `scaling_allowed` means only that the manual capture mechanism is internally consistent enough to test on more scenes.
- `semantic_eval_allowed` remains false until complete real ViewJSON/tree and semantic GT exist.
- `geometry_eval_allowed` remains false until capture geometry is valid and independent 3D GT exists.
- Renderer-derived depth is not GT.

## Current Decision

The capture-mechanics gate passed, so the same manual workflow may be scaled to the other PLY scenes after review. Do not start that capture campaign yet. The pilot itself remains ineligible for semantic evaluation until a real ViewJSON/tree index and independent semantic GT exist, and ineligible for 3D evaluation until independent 3D GT and source-PLY coordinate/scale alignment are verified.
