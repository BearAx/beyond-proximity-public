# Claim Audit — TwinWorld Week 6 (Person 4)

Status date: 2026-07-13. Owner: Person 4 (Telman).  
Branch: `week6-person4` (base: `week6-person3` = P1+P2+P3).  
Paper: `papers/twinworld/main.tex`.

## Central claim (allowed)

> SemanticSplat is a graph-pruned semantic search layer for queryable 3DGS digital twins. It reduces query-time context while preserving retrieval on the internal benchmark, and is aligned with BBQ-style public grounding metrics — **without** claiming superiority over BBQ.

## Evidence map

| Claim in paper | Verdict | Evidence |
|---|---|---|
| Internal: −71.4% views, −65.1% tokens; hit@1 0.792 vs 0.768 | **supported** | `outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/metrics_summary.json` |
| Replica oracle Acc@k / Recall@1 = 1.0 for graph & flat lexical | **supported_with_caveat** (ceiling / oracle candidates) | `outputs/public_datasets/replica_pilot_v1/`; `docs/experiments/public_datasets/person2_grounding_results.md` |
| Replica: graph checks ~12.1 objects vs ~71.9 flat | **supported** | same |
| ScanNet: Recall@1 = Acc@0.25 = 0.271 for graph & flat lexical | **supported** | `outputs/public_datasets/scannet_pilot_v1/`; person2_grounding_results.md |
| ScanNet: graph checks ~11.2 vs ~49.0 objects (~77% fewer) | **supported** | same |
| Relation rerank does not help this pilot | **supported** | no-relation Acc@0.25 = 0.292 > 0.271 |
| mAcc/mIoU/fmIoU | **N/A** — must stay N/A | bbq_aligned_metrics.md |
| BBQ superiority | **forbidden** | no `outputs/baselines/bbq_*` |
| ConceptGraphs five-scene full run | **supported_with_limits** (captured only) | conceptgraphs_full_result.md |
| LangSplat five-scene accuracy | **unsupported** (smoke only) | langsplat_smoke_result.md |
| Live VLM evaluation | **out of scope** | — |
| Stale “1,046 semantic items” as current absolute truth | **avoid** | outdoor-street recheck can differ; use 96 views + “~1k items” or freeze a count with a path |

## Unsafe wording (never use)

- “We outperform BBQ / ConceptGraphs / LangSplat”
- “Official Replica/ScanNet perception accuracy”
- “mIoU improved by …”
- “100% room accuracy / 34% IoU” (legacy Beyond Proximity overclaims)
- Presenting internal hit@k as Acc@0.25

## Team freeze pointers

| Role | Artifact |
|---|---|
| P1 | `docs/datasets/replica_scannet_plan.md`, availability manifests, configs |
| P2 | `docs/experiments/public_datasets/person2_grounding_results.md`, `scripts/evaluate_grounding.py` |
| P3 | `docs/baselines/bbq_comparison.md`, `baseline_status.md` |
| P4 | `papers/twinworld/`, this audit, figure/submission checklists |
