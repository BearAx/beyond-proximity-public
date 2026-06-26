# Baseline Status

Status date: 2026-06-26. LangSplat smoke executed; ConceptGraphs remains setup-only.

| Baseline | Smoke status | Native outputs | Canonical outputs | Main blocker |
|---|---|---:|---:|---|
| ConceptGraphs | partial setup, not executed | 0 | 0 | External checkout/checkpoints exist, but Docker/env/native output are not verified |
| LangSplat | official sofa smoke executed | 1 | 1 | Not yet adapted to the five captured SemanticSplat scenes; no GT accuracy |

## Local Capability Audit

| Capability | Result |
|---|---|
| Conda | available |
| Conda environments | `base`, `pcg`, `semanticsplat`; no `conceptgraph` or `langsplat` |
| GPU | NVIDIA GeForce RTX 3060 Laptop GPU |
| GPU memory | 6,144 MiB |
| Docker daemon | available for LangSplat smoke after starting Docker Desktop |
| ConceptGraphs checkout | missing in `external/baselines/`; external checkout exists at `C:/GitProjects/baseline-deps/concept-graphs` but Git revision check is blocked by `safe.directory` ownership protection |
| LangSplat checkout | missing in `external/baselines/`; external checkout exists at `C:/GitProjects/baseline-deps/LangSplat` but Git revision check is blocked by `safe.directory` ownership protection |
| ConceptGraphs checkpoints | partial: `yolov8l-world.pt` and `mobile_sam.pt` exist in `C:/GitProjects/baseline-deps/model-cache` |
| LangSplat assets | present: official sofa `data`, `ckpt`, `output`, and rendered `train/ours_None/renders_npy/00000.npy` |
| Baseline-native preprocessing outputs | LangSplat sofa smoke present; ConceptGraphs still missing |
| Strict canonical adapter scripts | implemented and fixture-tested; no project output without native evidence |

The captured scenes provide valid RGB-D, poses, and intrinsics, but they are not proven packaged in either baseline's official native layout. The GPU does not satisfy LangSplat's documented 24 GB paper-quality training recommendation, but it was sufficient for a pretrained official sofa render/query smoke.

Exact setup and result evidence:

- `docs/baselines/conceptgraphs/conceptgraphs_smoke_setup.md`
- `docs/baselines/conceptgraphs/conceptgraphs_smoke_result.md`
- `docs/baselines/conceptgraphs/status.md`
- `docs/baselines/langsplat/langsplat_smoke_setup.md`
- `docs/baselines/langsplat/langsplat_smoke_result.md`
- `docs/baselines/langsplat/status.md`

LangSplat now has native and canonical smoke evidence under `outputs/baselines/langsplat_smoke_v1/`. This is not a fair five-scene comparison and has no accuracy denominator because `baseline_smoke_queries_v1.json` intentionally has no GT. ConceptGraphs still has no native output to adapt.
