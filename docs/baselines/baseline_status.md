# Baseline Status

Status date: 2026-07-15.

This table describes only saved execution evidence. External rows use different
map-construction protocols from the SemanticSplat oracle-map pilots and do not
support a method-superiority claim.

| Baseline / method | Status | Scope | Main evidence | Main caveat |
|---|---|---|---|---|
| SemanticSplat graph | DONE_WITH_LIMITATIONS | 56 Replica + 48 ScanNet oracle-map queries | `outputs/public_datasets/replica_pilot_v1/`; `outputs/public_datasets/scannet_pilot_v1/` | Oracle semantic candidates, not semantic perception. |
| Graph + fallback | DONE_WITH_LIMITATIONS | Same public pilots | Same outputs | Fallback can approach flat-search cost. |
| Flat lexical / embedding | DONE | Same public pilots | Same outputs | Same-input internal baselines only. |
| ConceptGraphs ScanNet | DONE_WITH_LIMITATIONS | 8 scenes, 39 RGB-D views, 48 queries | `outputs/baselines/conceptgraphs_scannet_full_v1/`; `docs/baselines/conceptgraphs/conceptgraphs_scannet_full_result.md` | Predicted maps; protocol differs from oracle-map SemanticSplat. |
| ConceptGraphs Replica | DONE_WITH_LIMITATIONS | 8 scenes, 40 sampled RGB-D views, 56 queries | `outputs/baselines/conceptgraphs_replica_full_v1/`; `docs/baselines/conceptgraphs/conceptgraphs_replica_full_result.md` | Five frames/scene, not full 2,000-frame trajectories. |
| LangSplat ScanNet | DONE_WITH_LIMITATIONS | End-to-end scene0011_00, 4 views, 6 queries | `outputs/baselines/langsplat_scannet_full_v1/`; `docs/baselines/langsplat/langsplat_scannet_end_to_end_result.md` | Reduced 3k-iteration / 6 GB run, not the 30k / 24 GB paper setting. |
| BBQ official code | NOT_DONE | Literature only | `docs/baselines/bbq_comparison.md` | No saved official-code run. |

## Executed External Results

| Run | Coverage | Quality | Runtime | Local text tokens |
|---|---:|---:|---:|---:|
| ConceptGraphs ScanNet | 48 / 48 | Acc@0.25 0.0625; mean IoU 0.0696 | 0.3363 s/query | 627 |
| ConceptGraphs Replica | 56 / 56 | Acc@0.25 0.0625; mean IoU 0.0624 | 0.2743 s/query | 459 |
| LangSplat ScanNet | 6 / 6 | view hit 0.6667; 3D IoU N/A | 2.0365 s/query | 74 |

Tokens are measured local OpenCLIP text-encoder tokens, not provider billing
or cost. LangSplat 3D IoU is N/A because it emits a relevance point rather than
a predicted 3D extent.

## Safe Interpretation

- ConceptGraphs now has native public-data predicted-map evidence on every
  selected ScanNet and Replica scene.
- LangSplat now has a native end-to-end public-data execution, beyond its old
  pretrained-sofa smoke, but only on one ScanNet scene at reduced resources.
- Only SemanticSplat graph-vs-flat variants are directly comparable under the
  same map, queries, and scorer.
- BBQ remains a metric and related-work reference until its official code is
  run under a matched protocol.
