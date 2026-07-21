# LangSplat ScanNet End-to-End Result

Status date: 2026-07-15.

## Status

`DONE_WITH_LIMITATIONS`

LangSplat completed its native end-to-end pipeline on ScanNet scene
`scene0011_00`: RGB 3DGS training, SAM/CLIP feature preprocessing, autoencoder
training and encoding, language-field training, rendering, six-query batch
retrieval, canonical adaptation, and GT-backed evaluation.

## Protocol

- Repository: `minghanqin/LangSplat`
- Revision: `d70edb86df0fcbda19dc0d9739a3e5140a5e65fc`
- Scene: `scannet_0011_00`
- RGB-D views: 4
- Queries: 6 / 6 for this scene
- RGB 3DGS optimization: 3,000 iterations
- Language field: feature level 3, 3,000 iterations
- Autoencoder: 100 epochs, best epoch 99, evaluation loss 0.22350024
- Preprocessing: SAM ViT-B, OpenCLIP ViT-B-16, width 320; discrete maps
  nearest-neighbor aligned to the 640x480 cameras
- Hardware: RTX 3060 Laptop GPU, 6 GB VRAM

Run command:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_langsplat_scannet_full.ps1
```

## Results

| Metric | Result |
|---|---:|
| Canonical/schema-valid outputs | 6 / 6 |
| Expected view hit | 4 / 6 = 0.6667 |
| Thresholded retrieval success | 1 / 6 = 0.1667 |
| Exact GT object-ID hit | 0 / 6 = 0.0000 |
| Mean native batch-query runtime | 2.0365 s/query |
| Views checked | 4 per query |
| Measured text tokens | 74 total |
| 3D IoU / Acc@k | N/A |

3D IoU is N/A because native LangSplat emits a language-relevancy peak, not a
predicted 3D box. A depth-grounded peak point is retained only as a diagnostic;
it is not converted into a fabricated extent.

## Resource Qualification

This is a reduced-resource end-to-end execution, not the paper's recommended
30,000-iteration / 24 GB configuration and not an eight-scene benchmark. The
native algorithmic stages all ran, but its quality values must be labeled as a
one-scene pilot.

Primary evidence:

- `outputs/baselines/langsplat_scannet_full_v1/run_config.json`
- `outputs/baselines/langsplat_scannet_full_v1/metrics_summary.json`
- `outputs/baselines/langsplat_scannet_full_v1/native_results.json`
- `outputs/baselines/langsplat_scannet_full_v1/native_*.log`
