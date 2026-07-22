# Academic Article Evidence Freshness Audit

Status date: 2026-07-22.

Paper: `papers/beyond-proximity/main.tex`.

## Verdict

The academic manuscript is synchronized with the checked-in result artifacts.
The previous LangSplat wording was technically accurate about resource scale
but easy to misread as an incomplete or smoke-only launch. It now distinguishes
two facts explicitly:

1. LangSplat completed every native stage and evaluated all six queries for
   ScanNet `scene0011_00`.
2. The run used a hardware-adapted 3,000-iteration configuration on a 6 GB GPU,
   so it is not an eight-scene, paper-scale reproduction.

## Claim Audit

| Manuscript claim | Status | Primary evidence |
|---|---|---|
| Five captured scenes, 97 views, 1,066 items, 150 queries | Supported | `outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/metrics_summary.json`; `docs/reports/final/graph_construction_cost.json` |
| 75.5% fewer checked views and 68.2% fewer estimated context tokens | Supported | `outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/metrics_summary.json` |
| Internal graph hit@1/hit@3 = 0.680/0.808; flat = 0.768/0.928 | Supported | Same frozen internal summary |
| Replica oracle-map pilot: 8 scenes, 575 boxes, 56 queries | Supported | `outputs/public_datasets/replica_pilot_v1/` |
| ScanNet oracle-map pilot: 8 scenes, 392 boxes, 48 queries | Supported | `outputs/public_datasets/scannet_pilot_v1/` |
| ConceptGraphs native predicted-map runs: 8 ScanNet and 8 Replica scenes | Supported with protocol caveat | `outputs/baselines/conceptgraphs_scannet_full_v1/`; `outputs/baselines/conceptgraphs_replica_full_v1/` |
| LangSplat complete native pipeline: 1 ScanNet scene, 6 queries, expected-view hit 4/6, 74 local text tokens | Supported with resource caveat | `outputs/baselines/langsplat_scannet_full_v1/run_config.json`; `metrics_summary.json`; native logs and checkpoints |
| LangSplat 3D IoU / Acc@k | N/A | Native output is a depth-grounded relevance point, not a predicted 3D extent |
| Official BBQ result from this repository | Not available and not claimed | No `outputs/baselines/bbq_*` execution artifact exists |

## Current LangSplat Qualification

The run includes RGB 3DGS optimization, SAM/CLIP preprocessing, autoencoder
training and encoding, language-field optimization, rendering, batch retrieval,
canonical adaptation, and GT-backed evaluation. Its saved profile is 3,000 RGB
iterations, 3,000 language iterations, SAM ViT-B, OpenCLIP ViT-B-16, and 6 GB
VRAM. The correct paper label is therefore **complete hardware-adapted
end-to-end execution**, not **smoke test** and not **paper-scale reproduction**.

## Automated Guard

`python -B scripts/check_academic_paper.py` now checks the manuscript wording
and the LangSplat run status, native-execution flag, scene/query coverage,
iteration counts, expected-view numerator/denominator, and local token total
against the frozen JSON artifacts.
