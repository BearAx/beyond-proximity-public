# Workshop Paper Claim Audit

Status date: 2026-07-15.
Paper: `papers/twinworld/main.tex`.

## Central claim (allowed)

> SemanticSplat is a graph-pruned semantic search layer over structured 3D scene evidence. It reduces query-time context on the internal benchmark (with a stub-lexical hit@$k$ tradeoff) and is aligned with BBQ-style public grounding metrics — **without** claiming superiority over BBQ.

## Evidence map

| Claim in paper | Verdict | Evidence |
|---|---|---|
| Internal: −75.5% views, −68.2% tokens (19.4→4.77; 3168→1014) | **supported** | `outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/metrics_summary.json` |
| Internal hit@1 0.68 graph vs 0.768 flat (n=125); hit@3 0.808 vs 0.928 | **supported** | same JSON (`quality`) |
| Cumulative tokens 475k flat vs 152k graph | **supported** | sum of `per_query_results.json` → `queries[*].{flat,graph}.input_tokens` |
| Replica oracle Acc@k / Recall@1 = 1.0 for graph & flat lexical | **supported_with_caveat** (ceiling / oracle candidates) | `outputs/public_datasets/replica_pilot_v1/`; `docs/experiments/public_datasets/person2_grounding_results.md` |
| Replica: graph checks ~12.1 objects vs ~71.9 flat | **supported** | same |
| ScanNet: Recall@1 = Acc@0.25 = 0.271 for graph & flat lexical | **supported** | `outputs/public_datasets/scannet_pilot_v1/` |
| ScanNet: graph checks ~11.2 vs ~49.0 objects (~77% fewer) | **supported** | same |
| Relation rerank does not help this pilot | **supported** | no-relation Acc@0.25 = 0.292 > 0.271 |
| mAcc/mIoU/fmIoU | **N/A** — must stay N/A | bbq_aligned_metrics.md |
| BBQ superiority | **forbidden** | no `outputs/baselines/bbq_*` |
| ConceptGraphs ScanNet predicted-map run (8 scenes / 48 queries) | **supported_with_limits** | `outputs/baselines/conceptgraphs_scannet_full_v1/` |
| ConceptGraphs Replica sampled-map run (8 scenes / 56 queries) | **supported_with_limits** | `outputs/baselines/conceptgraphs_replica_full_v1/` |
| LangSplat end-to-end ScanNet pilot (1 scene / 6 queries) | **supported_with_limits** | `outputs/baselines/langsplat_scannet_full_v1/` |
| Live VLM evaluation | **out of scope** | — |
| Stale “1,046 semantic items” as current absolute truth | **avoid** | outdoor-street recheck can differ; use the verified 97-view count or freeze an item count with a path |
| Superseded PERSON1 roundings (71.4% / 0.792 hit@1) | **forbidden in TwinWorld PDF** | prefer frozen JSON; see note below |

## Superseded note

`docs/experiments/graph_vs_flat/PERSON1_DELIVERABLE.md` lists v2 as 19.2→5.39 (−71.4%) and hit@1 0.792 vs 0.768. The **checked-in** `five_scene_graph_vs_flat_v2/metrics_summary.json` instead reports 19.4→4.77 (−75.5%) and hit@1 0.68 vs 0.768. TwinWorld paper + `check_twinworld_numbers.py` follow the JSON.

## Unsafe wording (never use)

- “We outperform BBQ / ConceptGraphs / LangSplat”
- “Official Replica/ScanNet perception accuracy”
- “mIoU improved by …”
- “100% room accuracy / 34% IoU” (legacy SemanticSplat overclaims)
- Presenting internal hit@k as Acc@0.25
- “preserving retrieval quality” on the internal five-scene track without mentioning the hit@k tradeoff

## Evidence pointers

| Area | Artifact |
|---|---|
| Datasets | `docs/datasets/replica_scannet_plan.md`, availability manifests, configs |
| Evaluation | `docs/experiments/public_datasets/person2_grounding_results.md`, `scripts/evaluate_grounding.py` |
| Baselines | `docs/baselines/bbq_comparison.md`, `baseline_status.md` |
| Paper | `papers/twinworld/`, this audit, figure/submission checklists, `twinworld_reproducibility.md` |
