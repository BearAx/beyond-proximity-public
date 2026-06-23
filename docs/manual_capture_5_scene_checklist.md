# Five-Scene Manual Capture Checklist

Status date: 2026-06-22. Manual scaling is authorized by the successful ConferenceHall pilot. The five-scene benchmark remains paused until capture and validation are complete.

## Capture Targets

Use these Scene IDs exactly. Scene ID selects the backend output directory; the PLY selection controls what is rendered.

| PLY scene | PLY asset | Exact Scene ID | Current valid views | Minimum | Better target | Remaining to minimum/target |
|---|---|---|---:|---:|---:|---:|
| ConferenceHall | `scenes/ConferenceHall.ply` | `ConferenceHall-capture-pilot` | 5 | 10 | 20 | 5 / 15 |
| Museume | `scenes/Museume.ply` | `Museume-capture` | 0 | 10 | 20 | 10 / 20 |
| Theater | `scenes/Theater.ply` | `Theater-capture` | 0 | 10 | 20 | 10 / 20 |
| outdoor-drone | `scenes/outdoor-drone.ply` | `outdoor-drone-capture` | 0 | 10 | 20 | 10 / 20 |
| outdoor-street | `scenes/outdoor-street.ply` | `outdoor-street-capture` | 0 | 10 | 20 | 10 / 20 |

The naming rule for new capture directories is `<exact PLY stem>-capture`. `ConferenceHall-capture-pilot` is the deliberate existing exception and must be continued rather than renamed or duplicated.

## Start Services

Repository root, Terminal 1:

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

Open `http://localhost:5173` and use the **Navigator** tab.

## Exact Viewer Steps

Repeat this sequence for one row at a time:

1. Enter the exact target value in **Scene ID** and click **Set**. Wait for `Scene "<id>" ready`.
2. Select the matching filename in **3D Scene**. Selection starts loading immediately; click **Load** if using the text-input fallback.
3. Wait until the intended PLY is visibly stable. Do not capture a blank, loading, or wrong scene.
4. Click the canvas and navigate with mouse look, `W/A/S/D`, `Q/E`, and Shift for boost.
5. Stop moving, verify useful content is visible, and press `R` once. Wait for the capture to finish before moving or pressing `R` again.
6. Capture at least 10 distinct views. Prefer 20 when scene size and useful coverage justify it.
7. Run the single-scene checker before switching scenes. Do not continue if depth is constant, calibration mismatches, or any frame is missing.
8. After all five folders pass individually, run the batch command below and stop for semantic-index review.

For the existing ConferenceHall pilot, keep the browser/render size at 2340x1170. A different resolution conflicts with the stored calibration and the API correctly returns HTTP 409. New scene folders lock their calibration from their first accepted capture; keep each browser window and render resolution unchanged for the remainder of that scene.

## Capture Quality Rules

- Cover different sides and functional areas of the scene.
- Include wide overview views that establish room or zone context.
- Include closer views of meaningful objects, landmarks, and regions.
- Avoid repeated or nearly identical camera positions and angles.
- Avoid sets dominated by ceiling, floor, empty sky, or blank geometry.
- Keep the camera inside or near the reconstructed scene instead of far outside the splat.
- Stop movement before capture; do not capture unstable or visibly blurred frames.
- Keep recognizable overlap between neighboring views so spatial grouping is possible.
- Reject any frame whose RGB is blank, badly clipped, or clearly unrelated to the selected PLY.

## Per-Scene Check

Replace `<scene_id>` with the exact Scene ID:

```powershell
python -B scripts\check_capture_pilot.py `
  --scene backend\data\scenes\<scene_id> `
  --output docs\dataset_validation\<scene_id>_capture_check.json
```

Do not move to the next scene unless `scaling_allowed=true`, `depth_is_constant=false`, counts match, all poses are valid, and intrinsics match the canvas. `semantic_eval_allowed=false` and `geometry_eval_allowed=false` are expected until their separate requirements exist.

## Five-Scene Batch Check

```powershell
python -B scripts\check_capture_batch.py `
  --scenes `
    backend\data\scenes\ConferenceHall-capture-pilot `
    backend\data\scenes\Museume-capture `
    backend\data\scenes\Theater-capture `
    backend\data\scenes\outdoor-drone-capture `
    backend\data\scenes\outdoor-street-capture `
  --out docs\dataset_validation
```

Expected reports:

```text
docs/dataset_validation/ConferenceHall-capture-pilot_capture_check.json
docs/dataset_validation/Museume-capture_capture_check.json
docs/dataset_validation/Theater-capture_capture_check.json
docs/dataset_validation/outdoor-drone-capture_capture_check.json
docs/dataset_validation/outdoor-street-capture_capture_check.json
```

## Stop Conditions

Stop capture for the affected scene if the UI reports an error, HTTP 409, constant depth, mismatched RGB/depth dimensions, invalid pose, missing metadata, or more than 50% zero/invalid depth. Do not delete or overwrite evidence to force a pass. Do not create ViewJSON, tree, labels, boxes, or masks by hand unless they are genuine imported annotations or agent analyses.

## Return After Capture

Send back the batch command output and the five generated `*_capture_check.json` paths. Report any rejected captures or 409 responses, the final view count per scene, and whether every report says `scaling_allowed=true`. Do not run the benchmark or claim semantic/3D accuracy yet.
