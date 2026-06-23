# Baseline Status

Status date: 2026-06-23. Smoke attempts only; no baseline result is claimed.

| Baseline | Smoke status | Native outputs | Canonical outputs | Main blocker |
|---|---|---:|---:|---|
| ConceptGraphs | blocked before execution | 0 | 0 | Missing checkout/environment/checkpoints/preprocessing/native layout |
| LangSplat | blocked before execution | 0 | 0 | Missing checkout/environment/pretrained model/language features/native layout |

## Local Capability Audit

| Capability | Result |
|---|---|
| Conda | available |
| Conda environments | `base`, `pcg`, `semanticsplat`; no `conceptgraph` or `langsplat` |
| GPU | NVIDIA GeForce RTX 3060 Laptop GPU |
| GPU memory | 6,144 MiB |
| ConceptGraphs checkout | missing |
| LangSplat checkout | missing |
| Baseline checkpoints | missing |
| Baseline-native preprocessing outputs | missing |
| Strict canonical adapter scripts | implemented and fixture-tested; no project output without native evidence |

The captured scenes provide valid RGB-D, poses, and intrinsics, but they are not packaged in either baseline's official native layout. The GPU does not satisfy LangSplat's documented 24 GB paper-quality training recommendation. A pretrained rendering smoke could still be considered later, but no compatible model is present.

Exact setup and result evidence:

- `docs/baselines/conceptgraphs/conceptgraphs_smoke_setup.md`
- `docs/baselines/conceptgraphs/conceptgraphs_smoke_result.md`
- `docs/baselines/langsplat/langsplat_smoke_setup.md`
- `docs/baselines/langsplat/langsplat_smoke_result.md`

No adapter output was created because no native baseline output exists to adapt. This is a setup blocker, not evidence that either baseline fails semantically.
