# Dataset Ingestion Notes

## Current status

The uploaded archive contains one usable project scene: `data/scenes/default`.

Converted output:

```text
data/replica/pilot_scene_001/
├── rgb/
├── depth/
├── poses.json
├── intrinsics.json
└── metadata.json
```

## RGB / RGBA decision

The source PNG files are RGBA. The unified dataset output uses RGB.

Reason: the alpha channel is only transparency. For normal VLM / RGB-D / camera geometry pipelines, the expected image tensor is usually RGB with 3 channels. Keeping RGBA can break loaders that expect `[H, W, 3]`.

## Intrinsics decision

Source `transforms.json` contains intrinsics for 800x600, but the actual RGB images are 1722x733.

For the prepared scene, we preserve the original RGB resolution and scale the intrinsics:

```text
fx' = fx * 1722 / 800
fy' = fy * 733 / 600
cx' = cx * 1722 / 800
cy' = cy * 733 / 600
```

This avoids losing image information. If the pipeline strictly requires 800x600, run the script with:

```bash
python scripts/prepare_replica_scene.py   --input data/scenes/default   --output data/replica/pilot_scene_001   --image-policy resize_to_intrinsics
```

## Depth warning

Depth files exist, but all checked depth values are constant at 0.1. This means the files are valid arrays, but they do not contain meaningful geometry. They are useful only for loader smoke tests, not for real 3D reconstruction or bbox unprojection.

## ScanNet status

The eight BBQ-aligned official ScanNet scenes are complete. Raw files live under
`data/scannet/scans/`, extracted RGB-D under `data/scannet/extracted/`, and
backend scenes under `backend/data/scenes/scannet_*`. The converter decodes the
official `.sens` streams, maps poses/intrinsics, converts semantic labels and
aggregation instances, builds 392 official AABBs, and validates all scenes.

## Recommended next step

Use the imported official Replica scenes for the Replica object-box track and
the ScanNet scenes for the Nr3D/Sr3D+ grounding track. Reproduce ScanNet with:

```powershell
python -B scripts\prepare_scannet_scene.py --all-bbq-scenes --max-views 24 --candidate-stride 5 --overwrite
python -B scripts\build_scannet_official_queries.py
python -B scripts\run_experiment.py --config configs\scannet_benchmark.yaml --mode stub
```
