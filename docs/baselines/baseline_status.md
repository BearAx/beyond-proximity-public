# Baseline Status

Status date: 2026-07-13. Week 6 Person 3 audit.

This file summarizes what can be claimed from saved artifacts. It must be read together with `docs/baselines/bbq_comparison.md` and `docs/benchmarks/bbq_aligned_metrics.md`.

## Current Status Table

| Baseline / method | Status | Native outputs | Canonical outputs | Main evidence | Main blocker / caveat |
|---|---|---:|---:|---|---|
| SemanticSplat graph | DONE_WITH_LIMITATIONS | N/A, internal variant | 56 Replica + 48 ScanNet result records per variant | `outputs/public_datasets/replica_pilot_v1/variant_comparison.md`; `outputs/public_datasets/scannet_pilot_v1/variant_comparison.md` | Oracle semantic candidates; not semantic perception or BBQ reproduction. |
| SemanticSplat graph + fallback | DONE_WITH_LIMITATIONS | N/A, internal variant | 56 Replica + 48 ScanNet result records per variant | Same outputs as graph | Fallback can approach flat-search cost; report separately. |
| Flat lexical | DONE | N/A, internal variant | 56 Replica + 48 ScanNet result records per variant | Same outputs as graph | Same-input internal baseline only. |
| Flat embedding | DONE | N/A, internal variant | 56 Replica + 48 ScanNet result records per variant | Same outputs as graph; per-run configs record `fastembed` | Same-input internal baseline only. |
| ConceptGraphs | DONE_WITH_LIMITATIONS | 5 native result files | 150 | `docs/baselines/conceptgraphs/conceptgraphs_full_result.md`; `outputs/baselines/conceptgraphs_full_v1/metrics_summary.md` | Five captured scenes only; not official Replica/ScanNet; drone native map empty; internal coarse 3D boxes only. |
| LangSplat | PARTIALLY_DONE | 1 | 1 | `docs/baselines/langsplat/langsplat_smoke_result.md`; `outputs/baselines/langsplat_smoke_v1/metrics_summary.md` | Official sofa smoke only; no GT accuracy and no five-scene/public-dataset run. |
| BBQ official code | NOT_DONE | 0 | 0 | No saved `outputs/baselines/bbq_*` run exists | Use as related work and metric guide only. |

## Local Capability Audit

| Capability | Result |
|---|---|
| Conda | available |
| Conda environments | `base`, `pcg`, `semanticsplat`; no `conceptgraph` or `langsplat` |
| GPU | NVIDIA GeForce RTX 3060 Laptop GPU |
| GPU memory | 6,144 MiB |
| Docker daemon | available for LangSplat and ConceptGraphs smoke after starting Docker Desktop |
| ConceptGraphs checkout | missing in `external/baselines/`; Docker image `semanticsplat-conceptgraphs:72f5962` is the execution evidence |
| LangSplat checkout | missing in `external/baselines/`; external checkout exists at `C:/GitProjects/baseline-deps/LangSplat` but Git revision check is blocked by `safe.directory` ownership protection |
| ConceptGraphs checkpoints | present for smoke/full run evidence: `yolov8l-world.pt`, `mobile_sam.pt`, and downloaded HF CLIP cache |
| LangSplat assets | present: official sofa `data`, `ckpt`, and `output` folders |
| BBQ official-code run | not present in saved outputs |

## Safe Claims

- Same-input graph, graph+fallback, flat lexical, and flat embedding variants have saved Replica/ScanNet pilot outputs and can be compared directly within that protocol.
- ConceptGraphs has a full five captured-scene saved run, but it is not an official public-dataset result.
- LangSplat has native smoke execution and canonical adapter evidence only.
- BBQ has paper-reported metrics in local markdown, but no official-code run in this repo.

## Unsafe Claims

- Do not claim external baselines were run unless this table names saved native/canonical outputs.
- Do not claim Beyond Proximity beats BBQ, ConceptGraphs, LangSplat, or any external paper without same-dataset, same-query, same-protocol saved outputs.
- Do not claim token count is a standard 3D scene metric. Token/context counts support internal context-efficiency analysis only.
- Do not report mAcc/mIoU/fmIoU for our public-dataset pilots until paired model-predicted segmentation arrays exist.

## Exact Setup And Result Evidence

- `docs/baselines/bbq_comparison.md`
- `docs/baselines/conceptgraphs/conceptgraphs_smoke_setup.md`
- `docs/baselines/conceptgraphs/conceptgraphs_smoke_result.md`
- `docs/baselines/conceptgraphs/conceptgraphs_full_result.md`
- `docs/baselines/conceptgraphs/status.md`
- `docs/baselines/langsplat/langsplat_smoke_setup.md`
- `docs/baselines/langsplat/langsplat_smoke_result.md`
- `docs/baselines/langsplat/status.md`
- `docs/experiments/public_datasets/person2_grounding_results.md`
- `outputs/public_datasets/replica_pilot_v1/variant_comparison.md`
- `outputs/public_datasets/scannet_pilot_v1/variant_comparison.md`
