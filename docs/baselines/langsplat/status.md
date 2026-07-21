# LangSplat Status

Status date: 2026-07-15. Status: `END_TO_END_SCANNET_DONE_WITH_LIMITATIONS`.

LangSplat now has a native end-to-end public-dataset execution beyond the old
pretrained-sofa smoke. The run completed on ScanNet `scene0011_00` with four
official RGB-D views and all six scene queries.

## Native Stages Completed

1. RGB 3D Gaussian Splatting optimization, 3,000 iterations.
2. SAM ViT-B and OpenCLIP ViT-B-16 feature preprocessing.
3. Autoencoder training for 100 epochs and feature encoding.
4. Level-3 language-field optimization, 3,000 iterations.
5. Rendering, six-query native retrieval, canonical adaptation, and evaluation.

## Results

| Metric | Result |
|---|---:|
| Schema-valid outputs | 6 / 6 |
| Expected view hit | 4 / 6 (0.6667) |
| Thresholded retrieval success | 1 / 6 (0.1667) |
| Exact GT object-ID hit | 0 / 6 |
| Mean query runtime | 2.0365 s |
| Local text tokens | 74 |
| 3D IoU / Acc@k | N/A |

3D IoU is unavailable because native LangSplat emits a language-relevance peak,
not a predicted 3D box. No artificial extent is constructed from that point.

## Reproduction

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_langsplat_scannet_full.ps1
```

Primary evidence:

- `outputs/baselines/langsplat_scannet_full_v1/`
- `docs/baselines/langsplat/langsplat_scannet_end_to_end_result.md`
- `scripts/run_langsplat_scannet_full.ps1`

## Resource Qualification

This is a reduced-resource execution on an RTX 3060 Laptop GPU with 6 GB VRAM,
using 3,000 instead of the paper's 30,000 iterations. It proves every native
stage runs on project data; it is not a paper-equivalent eight-scene LangSplat
benchmark or a matched comparison with SemanticSplat.
