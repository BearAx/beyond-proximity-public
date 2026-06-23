# PLY-to-Scene Conversion Plan

Status date: 2026-06-22

## Current Decision

The hardened manual capture path produced a clean five-view `ConferenceHall-capture-pilot`. The pilot-specific checker reports `scaling_allowed=true`, and the general validator reports `geometry_inputs_valid=true`. Scaling readiness has passed, but capture of the remaining scenes is paused for review.

No RGB, depth, pose, intrinsics, ViewJSON, tree, labels, instances, or GT were fabricated. The five existing PLY scene manifests remain semantically and geometrically ineligible.

## Scene Asset Status

| scene_id | PLY | RGB/depth/poses/intrinsics | ViewJSON/tree | labels/instances/GT | semantic eval | 3D eval |
|---|---|---|---|---|---|---|
| `ConferenceHall` | available | missing | missing | missing | not allowed | not allowed |
| `Museume` | available | missing | missing | missing | not allowed | not allowed |
| `Theater` | available | missing | missing | missing | not allowed | not allowed |
| `outdoor-drone` | available | missing | missing | missing | not allowed | not allowed |
| `outdoor-street` | available | missing | missing | missing | not allowed | not allowed |

## Available Conversion Path

The implemented path remains manual/semi-automatic:

```text
scenes/<name>.ply
  -> Spark.js viewer
  -> manual camera navigation
  -> R-key RGB + renderer-depth + pose + intrinsics capture
  -> backend validation and deterministic persistence
  -> optional MCP/agent ViewJSON analysis
  -> optional MCP/agent tree construction
```

Capture code locations:

| Output | Implementation |
|---|---|
| RGB PNG | `frontend/src/components/Navigator/useViewCapture.ts` calls `canvas.toDataURL`; `backend/api/routes/captures.py` validates and writes it. |
| Depth NPY | `DepthCapture.ts` uses Spark 0.1.10 `modifiers.setDepthColor`, decodes logarithmic view-space splat depth, flips WebGL rows, and sends float32 data; the API rejects empty or constant depth. |
| Pose | `useViewCapture.ts` exports `camera.matrixWorld`; metadata documents right-handed Three.js world, Y-up, camera forward -Z. |
| Intrinsics | `useViewCapture.ts` derives focal lengths and principal point from the actual projection matrix and drawing-buffer resolution. The first capture replaces scene-init defaults. |
| Frame metadata | `backend/api/routes/captures.py` writes `captures/<view_id>.json`. |
| Frame index | `backend/api/routes/captures.py` writes/updates `transforms.json`. |

The backend validates PNG dimensions, depth shape/statistics, camera pose, and calibration before writing. It rejects changing calibration after the first frame. Existing frame IDs are loaded when a scene is selected, preventing browser reload from silently overwriting `v001`.

## Real Depth Status

Renderer-derived depth export is now implemented; it is not a constant placeholder. Spark's official depth-color modifier encodes each splat center's view-space depth logarithmically. The capture path decodes alpha-weighted grayscale into positive float scene-unit depth and sets unobserved pixels to zero.

The pilot confirmed:

- non-constant renderer depth with range 0.1-100.0 and mean 15.0844;
- matching 2340x1170 RGB/depth dimensions;
- zero-depth ratio 0.003443;
- valid projection-derived intrinsics and 5/5 valid pose matrices.

Source-PLY metric scale and coordinate alignment remain unverified for geometry metrics.

Renderer-derived splat-center depth is not independent GT and does not by itself make 3D evaluation valid.

## Missing Conversion Path

The repository still has no:

- automatic/headless PLY-to-RGB-D renderer;
- automatic camera trajectory generator/executor;
- automatic ViewJSON or persistent semantic-tree generator from PLY;
- independent room/object/instance labels or GT 3D boxes for the five assets;
- verified metric scale/provenance for these SuperSplat exports;
- automatic generation of scene-level capture provenance/manifest files.

## Manual Capture

Follow `docs/datasets/manual_capture_pilot.md`. Capture only `ConferenceHall-capture-pilot`, 3-5 views, then stop.

Start API:

```powershell
$env:PYTHONPATH = "."
python -m backend.api.server
```

Start frontend:

```powershell
Set-Location frontend
npm.cmd install
npm.cmd run dev
```

Open `http://localhost:5173`, set Scene ID `ConferenceHall-capture-pilot`, load `ConferenceHall.ply`, navigate with WASD/mouse, and press `R` at 3-5 diverse positions.

## Expected Canonical Scene Structure

Pilot capture output:

```text
backend/data/scenes/ConferenceHall-capture-pilot/
  images/
    v001.png
  depths/
    v001_depth.npy
  captures/
    v001.json
  transforms.json
```

Future complete semantic scene:

```text
backend/data/scenes/<scene_id>/
  geometry/scene.ply
  images/v001.png
  depths/v001_depth.npy
  captures/v001.json
  transforms.json
  views/v001.json
  tree/manifest.json
  tree/node_<node_id>.json
  source_metadata.json
  scene_manifest.json
```

No canonical independent GT annotation files exist for these assets yet.

## Validation Commands

Run the pilot-specific checker:

```powershell
python -B scripts\check_capture_pilot.py --scene backend\data\scenes\ConferenceHall-capture-pilot
```

Run the general validator:

```powershell
python -B scripts\validate_scene_geometry.py `
  --scene backend\data\scenes\ConferenceHall-capture-pilot `
  --output docs\validation\geometry\ConferenceHall_capture_pilot_geometry.json
```

The general validator now prefers actual `transforms.json` frame records when a canonical directory contains both `geometry/scene.ply` and captures. It also requires complete ViewJSON/tree before reporting semantic evaluation allowed, and independent 3D GT before reporting 3D evaluation allowed.

## Scale Gate

Scaling is allowed only when `check_capture_pilot.py` reports:

```text
scaling_allowed = true
depth_is_constant = false
RGB/depth/pose counts equal the frame count
RGB and depth resolutions match
intrinsics_match_canvas = true
pose_validity.all_valid = true
metadata_status = complete
```

`semantic_eval_allowed` may remain false after the capture gate because ViewJSON/tree and semantic GT are separate requirements. `geometry_eval_allowed` remains false without independent 3D GT even if capture geometry is internally valid.

## Blockers

- Pose-to-source-PLY metric alignment and scene scale remain unverified.
- The pilot has complete per-frame metadata, but no scene-level `source_metadata.json` or `scene_manifest.json`.
- No semantic index exists for the five scenes.
- No independent labels, instances, GT boxes, or real semantic predictions exist.
- No automatic capture path exists.
- ScanNet remains out of scope.

## Next Recommended Action

Review the successful pilot report and inspect a sample RGB/depth pair for visual alignment. If approved, plan a controlled manual capture of the remaining four PLY scenes using the same fixed frontend/backend versions and validation after each scene. Do not run the five-scene evaluation gate until each captured scene has passed its capture checks; semantic and 3D eligibility must remain false without the required index and independent GT.
