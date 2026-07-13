# BBQ Comparison And Baseline Claim Audit

Owner: Person 3, BBQ / baselines / related work lead  
Status date: 2026-07-13  
Scope: Week 6 article-facing comparison notes. This file is not a claim that BBQ official code was run.

## Evidence Index

| Evidence | Path | Use |
|---|---|---|
| BBQ local markdown, full conversion | `markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md` | BBQ datasets, method, tables, hardware, limitations. |
| BBQ local short note | `markdown-papers/new-papers/3d-scene-understanding/BBQ/BBQ.md` | Renamed paper provenance and sprint decision. |
| BBQ PDF | `papers/new-papers/3d-scene-understanding/BBQ.pdf` | Source paper artifact. |
| BBQ-aligned evaluator definition | `docs/benchmarks/bbq_aligned_metrics.md` | Our Acc@k / Recall@1 / segmentation metric definitions and claim limits. |
| Person 2 public-dataset results | `docs/experiments/public_datasets/person2_grounding_results.md` | Frozen Week 6 Replica and ScanNet pilot summary. |
| Replica variant comparison | `outputs/public_datasets/replica_pilot_v1/variant_comparison.md` | Same-input graph/flat/ablation metrics on Replica pilot. |
| ScanNet variant comparison | `outputs/public_datasets/scannet_pilot_v1/variant_comparison.md` | Same-input graph/flat/ablation metrics on ScanNet pilot. |
| ConceptGraphs full captured-scene run | `docs/baselines/conceptgraphs/conceptgraphs_full_result.md` | Last-week full five captured-scene external baseline status. |
| LangSplat smoke run | `docs/baselines/langsplat/langsplat_smoke_result.md` | Native execution smoke status only. |

## BBQ Facts To Use

| Topic | BBQ fact | Evidence path |
|---|---|---|
| Representation | BBQ builds an object-centric 3D scene graph with object IDs, captions, centers, extents, metric distances, and semantic spatial relations. | `markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md`, Sec. III-E. |
| Reasoning | BBQ uses deductive LLM reasoning: first select target and anchor IDs, then reason over a compact target-anchor subgraph. | `markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md`, Sec. III-E. |
| Dataset split | BBQ evaluates on 8 Replica scenes and 8 ScanNet scenes: Replica room0/room1/room2/office0-office4; ScanNet 0011_00, 0030_00, 0046_00, 0086_00, 0222_00, 0378_00, 0389_00, 0435_00. | `markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md`, Sec. IV. |
| Query sources | BBQ uses Sr3D+ and Nr3D over the selected ScanNet scenes and ScanRefer for an additional grounding table. | `markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md`, Sec. IV. |
| Segmentation metrics | BBQ reports mAcc, mIoU, and fmIoU for open-vocabulary 3D semantic segmentation on Replica and ScanNet. | `markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md`, Table I. |
| Grounding metrics | BBQ reports Recall@1 for graph-edge ablations and Acc@0.1/Acc@0.25/Acc@0.5 for 3D object grounding. | `markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md`, Tables II-V and Sec. IV-B. |
| Hardware | BBQ paper reports SensorBox/on-board PC experiments and V100/H100 LLM/GPU usage for experiments. | `markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md`, Sec. IV-C and Sec. IV. |
| Limitations | BBQ assumes static indoor scenes and notes tiny-object mapping and large/complex-form relation limits. | `markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md`, Sec. V. |

## Extracted BBQ Evaluation Tables

These are paper-reported BBQ values from the local markdown conversion. They are related-work evidence only. They are not measurements from this repository.

| BBQ table | Main content | Values needed in article | Evidence path |
|---|---|---|---|
| Table I | Replica/ScanNet open-vocabulary segmentation | BBQ-CLIP zero-shot: Replica mAcc 0.38, mIoU 0.27, fmIoU 0.48; ScanNet mAcc 0.56, mIoU 0.34, fmIoU 0.36. | `markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md`, Table I. |
| Table II | Nr3D graph-edge ablation using GT objects | GPT-4o Recall@1: no edges 61.8, metric 68.6, semantic 50.5, metric+semantic 68.4. Llama3-8B metric+semantic 45.5. | `markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md`, Table II. |
| Table III | Sr3D+/Nr3D grounding | Sr3D+ BBQ overall A@0.1/A@0.25: 34.2/22.7. Nr3D BBQ overall A@0.1/A@0.25: 28.3/19.0. | `markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md`, Table III. |
| Table IV | ScanRefer grounding | BBQ A@0.25/A@0.5: 19.4/11.6 on the ScanRefer subset reported in the paper. | `markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md`, Table IV. |
| Table V | Nr3D breakdown | BBQ overall A@0.1/A@0.25: 28.3/19.0; with spatial language 28.1/19.2; without target mention 14.8/11.5. | `markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md`, Table V. |
| Fig. 6 / mapping speed | Replica room0 RGB-D sequence, stride 10 | Paper reports 1.18 s/iteration and 7 min 52 s overall for the scene on the Zotac on-board PC. | `markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md`, Sec. IV-C / Fig. 6 text. |

## Our Week 6 Same-Input Evidence

| Track | Scope | Best supported claim | Evidence path |
|---|---|---|---|
| Replica pilot | 56 queries, 8 official Replica scenes, official GT object boxes, oracle semantic candidates | Graph, graph+fallback, and flat lexical all reach Recall@1 and Acc@0.1/0.25/0.5 of 1.0 on this oracle-map pilot; graph checks fewer objects than flat lexical. | `docs/experiments/public_datasets/person2_grounding_results.md`; `outputs/public_datasets/replica_pilot_v1/variant_comparison.md`. |
| ScanNet pilot | 48 official Nr3D/Sr3D+ queries, 8 official ScanNet scenes, oracle semantic candidates | Graph-only and flat lexical both score Recall@1/Acc@0.25 of 0.2708; graph-only checks about 11.23 objects vs 49.00 for flat lexical. Relation reranking currently needs improvement. | `docs/experiments/public_datasets/person2_grounding_results.md`; `outputs/public_datasets/scannet_pilot_v1/variant_comparison.md`. |
| Segmentation metrics | Replica/ScanNet pilots | mAcc, mIoU, and fmIoU are N/A because this track has no paired model-predicted segmentation arrays. | `docs/benchmarks/bbq_aligned_metrics.md`; `docs/experiments/public_datasets/person2_grounding_results.md`. |
| ConceptGraphs | Five captured SemanticSplat scenes, 150 canonical outputs | ConceptGraphs has a saved full five captured-scene native/canonical run with limitations. It is not an official Replica/ScanNet result. | `docs/baselines/conceptgraphs/conceptgraphs_full_result.md`; `outputs/baselines/conceptgraphs_full_v1/metrics_summary.md`. |
| LangSplat | Official pretrained sofa smoke, one canonical output | LangSplat native execution and adapter compatibility are proven for the smoke only; no five-scene or public-dataset accuracy claim. | `docs/baselines/langsplat/langsplat_smoke_result.md`; `outputs/baselines/langsplat_smoke_v1/metrics_summary.md`. |

## Direct, Partial, And Invalid Comparisons

| Comparison type | Allowed? | Explanation |
|---|---|---|
| Same-input graph vs flat lexical/embedding on our Replica/ScanNet pilots | Direct | Same scenes, query strings, GT, canonical schema, and evaluator. |
| Our ScanNet pilot Acc@k vs BBQ paper Sr3D+/Nr3D/ScanRefer tables | Partial only | Similar metric family and overlapping scene intent, but not the same candidate construction, model pipeline, query subset size, or official BBQ execution. |
| Our context-size / estimated-token savings vs BBQ paper accuracy | Invalid | Token/context metrics are internal efficiency metrics, not standard 3D grounding quality metrics. |
| Our captured five-scene ConceptGraphs run vs our captured five-scene SemanticSplat run | Direct only within captured-scene protocol | It uses same benchmark query family, but manual GT and coarse boxes are internal regression evidence, not public-dataset proof. |
| Our public-dataset pilot vs LangSplat smoke | Invalid | LangSplat smoke uses official sofa assets with missing GT; it is not a public-dataset SemanticSplat comparison. |
| Any claim that Beyond Proximity beats BBQ | Not allowed now | The repo has no saved BBQ official-code run under the same dataset/query/protocol. |

## Baseline Status Table

| Baseline / method | Week 6 status | Evidence | Paper-safe wording |
|---|---|---|---|
| SemanticSplat graph | DONE_WITH_LIMITATIONS | `outputs/public_datasets/replica_pilot_v1/`, `outputs/public_datasets/scannet_pilot_v1/` | Measured same-input graph variant on Replica/ScanNet pilot oracle maps. |
| SemanticSplat graph + fallback | DONE_WITH_LIMITATIONS | Same output directories as above | Measured fallback variant; fallback can recover coverage but approaches flat cost. |
| Flat lexical | DONE | Same output directories as above | Required same-input flat baseline. |
| Flat embedding | DONE | Same output directories as above | Required same-input embedding baseline using local CPU fastembed. |
| ConceptGraphs | DONE_WITH_LIMITATIONS | `docs/baselines/conceptgraphs/conceptgraphs_full_result.md` | Full five captured-scene run exists; not official Replica/ScanNet and no publication-grade public-dataset comparison. |
| LangSplat | PARTIALLY_DONE | `docs/baselines/langsplat/langsplat_smoke_result.md` | Native smoke and adapter evidence only; no fair SemanticSplat-scene accuracy. |
| BBQ official code | NOT_DONE | No saved `outputs/baselines/bbq_*` run exists | Use BBQ as closest related work and metric guide, not as a run baseline. |
| BBQ paper tables | DONE_AS_RELATED_WORK | `markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md` | Can cite reported BBQ metrics as literature context, not as our experimental result. |

## Paper-Ready Related Work Paragraph

BBQ is the closest object-centric scene-graph reference for our current public-dataset alignment. It builds an RGB-D object graph with captions, 3D extents, metric distances, and semantic spatial relations, then uses deductive LLM calls to select target and anchor objects before grounding over a compact subgraph. BBQ reports stronger public grounding evidence than our current paper draft, including Replica/ScanNet segmentation metrics and Sr3D+/Nr3D/ScanRefer Acc@k tables. Our Week 6 evidence should therefore position Beyond Proximity differently: as a hierarchical semantic-tree and context-pruning layer for queryable 3DGS digital twins, evaluated against same-input flat graph-search baselines and aligned with BBQ-style object-grounding metrics. We do not claim superiority over BBQ because the repository does not contain a same-dataset, same-query BBQ official-code run.

## Remaining TODOs

| TODO | Owner / blocker |
|---|---|
| Run BBQ official code under the same Replica/ScanNet query protocol, if setup is allowed. | Baselines lead; external code/dependency time. |
| Add paired predicted segmentation arrays before reporting mAcc/mIoU/fmIoU for our method. | Dataset/evaluation leads. |
| Improve ScanNet relation reranking: current no-relation ablation slightly outperforms the relation-aware variant. | Algorithm lead. |
| Decide whether article results should include oracle-map public-dataset pilots or only present them as alignment/protocol pilots. | Paper lead + team. |
| Convert the paper-ready paragraph into the final workshop paper once Person 4 freezes section structure. | Paper lead. |
