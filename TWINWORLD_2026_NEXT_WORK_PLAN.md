# TwinWorld 2026 Next Work Plan

Status date: 2026-07-09.

Scope: planning only. This document does not start implementation work.

Target venue: TwinWorld @ ECCV 2026 Workshop, "Visual Intelligence for Built
Environment Digital Twins".

Submission deadline from the official TwinWorld page: 2026-07-31.

Main objective:

```text
Turn SemanticSplat / Beyond Proximity into a workshop-ready digital-twin paper
with public-dataset evidence, BBQ-aligned metrics, honest baseline comparison,
strong visual grounding, and a reproducible artifact package.
```

## 1. Current Situation

The project is a strong workshop candidate, but not yet a 100/100 submission.
The current fit assessment in `PUBLICATION_VENUE_FIT_ASSESSMENT.md` rates
TwinWorld as the best immediate target because the workshop explicitly covers:

- built-environment digital twins;
- scalable 3D / 4D scene understanding;
- semantic modeling, scene graphs, and hierarchical segmentation;
- neural representations, including Gaussian splatting;
- benchmark-driven evaluation;
- robotics, mapping, and real-world deployment.

The latest local precision work also improves the internal five-scene benchmark:

| Metric | Earlier manual bbox GT run | Latest local run |
|---|---:|---:|
| retrieval_success | 0.9467 | 1.0000 |
| expected_view_hit | 0.7120 | 0.9200 |
| expected_node_hit | 0.5920 | 0.8160 |
| expected_zone_hit | 0.9040 | 0.9440 |
| not_found_correctness | 0.8800 | 1.0000 |
| wrong object count | 40 | 14 |
| wrong view count | 36 | 10 |
| wrong zone count | 12 | 7 |
| eligible null 3D boxes | 37 | 0 |

Important caveat: these are internal manual-reference results over five captured
pilot scenes. They are useful for regression and system evidence, but they are
not the official Replica public-dataset result. The official Replica object-box
pilot is tracked separately in `docs/datasets/replica_official_import_report.md`.

## 2. BBQ Paper Analysis To Guide Our Next Experiments

Source in repo:

```text
markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md
```

Additional local comparison note:

```text
C:\Users\bear_\Downloads\Telegram Desktop\semanticsplat_vs_bbq.md
```

BBQ is the closest paper we should continuously compare against. It is similar
because it uses a 3D scene graph and language reasoning for object grounding, but
it has stronger public-dataset evaluation.

BBQ method summary:

- input: posed RGB-D frames with calibration;
- representation: object-centric 3D graph;
- object construction: MobileSAMv2 masks, DINOv2 features, RGB-D fusion,
  DBSCAN cleanup;
- object description: projected best object view plus VLM captioning;
- relations: metric distances plus semantic spatial edges such as left, right,
  front, behind, above, below;
- reasoning: LLM first selects target and anchor IDs, then answers over a compact
  target-anchor subgraph;
- output: selected 3D object ID and 3D bbox.

BBQ datasets:

| Dataset family | BBQ usage | What we should copy |
|---|---|---|
| Replica | 8 scenes: room0, room1, room2, office0, office1, office2, office3, office4 | Use the same scenes first. |
| ScanNet | 8 scenes: 0011_00, 0030_00, 0046_00, 0086_00, 0222_00, 0378_00, 0389_00, 0435_00 | Use the same scenes first if available. |
| Sr3D+ | 661 template relation queries over the selected ScanNet scenes | Add relational grounding track. |
| Nr3D | 699 natural language queries over selected ScanNet scenes | Add natural language grounding track. |
| ScanRefer | paper table uses ScanRefer grounding; related subset is 14 ScanNet scenes / 998 expressions | Add if time permits after Sr3D+/Nr3D. |

BBQ metrics:

| Metric | BBQ meaning | Should SemanticSplat add it? |
|---|---|---|
| mAcc | mean class accuracy for 3D semantic segmentation | Yes, public-dataset track. |
| mIoU | mean semantic segmentation IoU | Yes, public-dataset track. |
| fmIoU | frequency-weighted mIoU | Yes, public-dataset track. |
| Recall@1 | top-1 object grounding recall in graph ablations | Yes. |
| Acc@0.1 | predicted 3D bbox IoU with GT > 0.1 | Yes. |
| Acc@0.25 | predicted 3D bbox IoU with GT > 0.25 | Yes, primary grounding metric. |
| Acc@0.5 | predicted 3D bbox IoU with GT > 0.5 | Yes, stricter metric. |
| Mapping time | object-map construction runtime | Yes, report construction cost separately. |

Our current hit@1/hit@3 and token/view savings are still useful, but they are
not enough for a BBQ-level comparison. Object-level 3D grounding pilots now
exist for the eight BBQ Replica scenes and the same eight ScanNet scenes used by
BBQ. The ScanNet pilot adds mapped Nr3D/Sr3D+ targets and Acc@0.1/0.25/0.5.

## 3. Definition Of "100/100 TwinWorld Workshop Ready"

The submission is considered ready only when all items below are done.

| Requirement | Target status |
|---|---|
| ECCV/TwinWorld topic fit | Paper explicitly frames semantic 3DGS/digital-twin querying. |
| Venue format | ECCV workshop template, anonymized review PDF. |
| Public datasets | Replica completed; ScanNet completed or clearly marked as in-progress with at least one finished public-dataset track. |
| BBQ alignment | Same Replica/ScanNet scene choices where possible; same grounding metrics where possible. |
| Internal captured scenes | Keep five-scene benchmark as digital-twin pilot evidence. |
| Public-dataset metrics | Report mAcc/mIoU/fmIoU and/or Acc@0.1/0.25/0.5 depending on track readiness. |
| Efficiency metrics | Report views checked, nodes checked, context/token count, runtime, and construction cost separately. |
| Baselines | Flat lexical, flat embedding, graph lexical, graph + fallback, and at least one external baseline status. |
| BBQ positioning | Explain exactly what BBQ solves and how our method differs. No unfair superiority claim. |
| Visual evidence | Real scene screenshots, graph/tree visualization, query path figure, object/region bbox examples. |
| Reproducibility | One command per experiment, frozen run IDs, commit hash, environment notes, data-license notes. |
| Limitations | Clear statement about manual five-scene GT, public-dataset status, external baselines, and 3D bbox quality. |

## 4. Four-Person Work Plan

Recommended duration: 14 days for the first serious TwinWorld sprint, followed
by a final paper polish window before 2026-07-31.

### Person 1: Public Dataset And GT Lead

Mission:

```text
Move the project from five manual scenes to BBQ-aligned Replica/ScanNet evidence.
```

Tasks:

1. Confirm available local data and licensing for Replica and ScanNet.
2. Create a dataset manifest for the exact BBQ scene subset:
   - Replica: room0, room1, room2, office0, office1, office2, office3, office4.
   - ScanNet: 0011_00, 0030_00, 0046_00, 0086_00, 0222_00, 0378_00, 0389_00, 0435_00.
3. Define the import contract:
   - RGB path;
   - depth path;
   - camera intrinsics;
   - camera pose;
   - GT semantic labels;
   - GT object boxes or instance boxes where available.
4. Build the GT conversion spec for:
   - semantic segmentation labels for mAcc/mIoU/fmIoU;
   - object boxes for Acc@0.1/0.25/0.5;
   - query labels for Sr3D+/Nr3D/ScanRefer.
5. Produce a small pilot manifest first:
   - Replica room0;
   - one ScanNet scene;
   - 20-50 grounding queries.
6. Define failure labels:
   - wrong object;
   - wrong relation;
   - wrong view;
   - wrong room / zone;
   - missing GT;
   - bad bbox;
   - unavailable prediction.

Deliverables:

- `docs/datasets/replica_scannet_plan.md`
- `configs/replica_benchmark.yaml`
- `configs/scannet_benchmark.yaml`
- dataset availability table;
- GT field mapping table;
- pilot query subset for Replica and ScanNet.

Acceptance:

- Every planned scene has a clear status: `available`, `missing_data`,
  `license_blocked`, `conversion_blocked`, or `ready`.
- No metric is planned without an available GT source.

Completion record, 2026-07-12: all Person 1 acceptance criteria are met. The
eight Replica and eight ScanNet scenes are `ready`; the ScanNet importer maps
392/392 official instances, and all 699 Nr3D plus 661 unique Sr3D+ records in
the BBQ subset map to official target/anchor IDs. A deterministic 48-query pilot
has complete saved metrics, and the exact room0 + scene0011_00 acceptance pilot
contains 20 official-GT queries. ScanRefer remains an optional later dataset
because the plan explicitly prioritized it only after Nr3D/Sr3D+.

### Person 2: Algorithm And Evaluation Lead

Mission:

```text
Make SemanticSplat produce BBQ-comparable object-level and 3D grounding metrics
while preserving our graph-pruned efficiency story.
```

Tasks:

1. Add an object-grounding evaluation mode separate from the current view-level
   evaluation.
2. Extend query outputs to always include:
   - selected object ID;
   - selected view ID;
   - selected node ID;
   - selected 3D bbox;
   - selected 2D bbox if available;
   - graph traversal path;
   - checked nodes/views/objects;
   - runtime;
   - context/token estimate.
3. Add metrics matching BBQ:
   - Acc@0.1;
   - Acc@0.25;
   - Acc@0.5;
   - Recall@1;
   - mAcc/mIoU/fmIoU if segmentation track is enabled.
4. Add a stronger graph search variant:
   - exact label scoring;
   - synonym/affordance scoring;
   - calibrated fallback expansion;
   - relation-aware reranking;
   - bbox quality gate.
5. Add a flat embedding baseline:
   - same scene items;
   - same queries;
   - same GT;
   - same metrics.
6. Keep construction cost separate from query-time cost.
7. Add per-query failure reports and aggregate failure tables.

Deliverables:

- `scripts/evaluate_grounding.py`
- `docs/benchmarks/bbq_aligned_metrics.md`
- `outputs/public_datasets/replica_pilot_v1/`
- `outputs/public_datasets/scannet_pilot_v1/`
- updated tests for Acc@k and bbox IoU.

Acceptance:

- One public-dataset pilot run produces schema-valid metrics.
- The same run reports both quality and efficiency.
- No `bbox_3d = null` for eligible positive object-grounding queries unless the
  result is explicitly marked unavailable with reason.

### Person 3: BBQ, Baselines, And Related Work Lead

Mission:

```text
Keep the paper scientifically honest against BBQ and turn BBQ from a threat into
a clear positioning anchor.
```

Tasks:

1. Maintain a living BBQ comparison:
   - datasets;
   - metrics;
   - query types;
   - baselines;
   - hardware;
   - limitations.
2. Extract exact BBQ evaluation tables into our related-work notes:
   - Replica/ScanNet segmentation table;
   - Sr3D+/Nr3D grounding table;
   - ScanRefer table;
   - graph-edge ablation table;
   - mapping speed result.
3. Define what we can compare directly and what we cannot:
   - direct: same public dataset, same query set, same object bbox metric;
   - partial: graph reasoning and context reduction;
   - not valid: internal hit@k vs BBQ Acc@0.25.
4. Run or document baselines:
   - flat lexical;
   - flat embedding;
   - ConceptGraphs status;
   - LangSplat status;
   - BBQ official code status if clone/setup is allowed.
5. Prepare article text that positions BBQ as:
   - closest object-centric scene-graph approach;
   - stronger public-dataset grounding benchmark;
   - different from our hierarchical 3DGS semantic tree and context-pruning
     evaluation.

Deliverables:

- `docs/baselines/bbq_comparison.md`
- updated `docs/baselines/baselines_matrix.md`
- related work paragraph for the paper;
- baseline status table with `DONE`, `PARTIALLY_DONE`, `BLOCKED`, `NOT_DONE`.

Acceptance:

- Every claim about BBQ has an evidence path to the local markdown paper or an
  official source.
- The paper never claims superiority over BBQ unless the same-dataset metrics
  prove it.

### Person 4: TwinWorld Paper, Figures, And Submission Lead

Mission:

```text
Turn the system and experiments into a clear, honest, attractive TwinWorld
workshop submission.
```

Tasks:

1. Convert the article to ECCV workshop format.
2. Create an anonymized review version.
3. Rewrite the main claim:

```text
SemanticSplat is a graph-pruned semantic search layer for queryable 3DGS digital
twins. It reduces query-time context while improving or preserving retrieval on
the internal benchmark, and it is being aligned with public 3D grounding metrics
used by BBQ-style object-graph methods.
```

4. Add figures:
   - system overview;
   - captured-scene visual examples;
   - graph/tree traversal;
   - query -> node/view/object/bbox example;
   - public-dataset pilot result figure;
   - failure cases.
5. Add tables:
   - internal five-scene metrics;
   - public-dataset pilot metrics;
   - BBQ-aligned metrics table;
   - ablations;
   - baseline status.
6. Add limitations:
   - manual five-scene GT is not independent public GT;
   - public Replica/ScanNet tracks use official GT semantic maps as input and do
     not measure semantic perception;
   - external baselines must be labeled as smoke, blocked, or fair comparison;
   - coarse predicted boxes are not GT.
7. Prepare final checklist:
   - no author names in review PDF;
   - no stale 1,046 semantic item count;
   - all run IDs and commit hashes frozen;
   - all figures render;
   - references compile;
   - reproducibility appendix ready.

Deliverables:

- TwinWorld-formatted paper source;
- anonymized PDF;
- figure folder;
- final claim audit;
- submission checklist.

Acceptance:

- Paper can be read as a complete workshop contribution even if not all
  main-conference experiments are finished.
- Claims match saved outputs exactly.

## 5. Two-Week Schedule

### Days 1-2: Lock Scope And Data

| Person | Work |
|---|---|
| Person 1 | Verify Replica/ScanNet availability and create manifests. |
| Person 2 | Freeze output schema for object grounding and BBQ metrics. |
| Person 3 | Finalize BBQ metric/dataset comparison table. |
| Person 4 | Create TwinWorld paper skeleton and figure checklist. |

Go/no-go decision:

```text
Replica and ScanNet official data are imported for the exact BBQ-aligned scene
subsets. The ScanNet Nr3D/Sr3D+ pilot is complete, so the paper may report both
public-dataset tracks while clearly labeling them oracle-GT-map retrieval.
```

### Days 3-5: Public-Dataset Pilot

| Person | Work |
|---|---|
| Person 1 | DONE: all Replica/ScanNet scenes, GT conversion, ReferIt3D mappings, 48-query ScanNet pilot, and manifests are frozen. |
| Person 2 | Run object-grounding pilot and compute Acc@0.1/0.25/0.5. |
| Person 3 | Prepare baseline command/status table. |
| Person 4 | Draft method and evaluation sections. |

### Days 6-8: Full Evaluation Sprint

| Person | Work |
|---|---|
| Person 1 | DONE: expanded to all eight BBQ Replica and eight BBQ ScanNet scenes. |
| Person 2 | Run graph, flat lexical, flat embedding, and fallback variants. |
| Person 3 | Compare against BBQ tables and write caveats. |
| Person 4 | Add result tables and visual examples. |

### Days 9-11: Quality And Ablations

| Person | Work |
|---|---|
| Person 1 | DONE: 392/392 ScanNet objects and all ReferIt3D target/anchor IDs validated. |
| Person 2 | Run ablations: no hierarchy, no relation rerank, no fallback, flat-only. |
| Person 3 | Audit all baseline claims. |
| Person 4 | Add failure analysis and limitations. |

### Days 12-14: Paper Freeze Candidate

| Person | Work |
|---|---|
| Person 1 | DONE: dataset inventory, GT reports, validation, and reproduction commands frozen. |
| Person 2 | Freeze metrics outputs and reproduction commands. |
| Person 3 | Freeze related work and baseline status. |
| Person 4 | Build anonymized PDF and final checklist. |

Required freeze artifacts:

- final paper PDF;
- final metrics JSON/CSV/MD;
- final figure files;
- final claim audit;
- reproduction README.

## 6. What Must Change In The Article

High priority:

1. Replace the current venue-generic story with a TwinWorld-specific story:
   digital twins, hierarchical semantics, 3DGS, scene graphs, benchmark-driven
   evaluation.
2. Add a BBQ paragraph in related work and experiments.
3. Add public-dataset plan/results:
   - Replica first;
   - ScanNet second;
   - Sr3D+/Nr3D/ScanRefer if enough time.
4. Add object-level 3D grounding metrics:
   - Acc@0.1;
   - Acc@0.25;
   - Acc@0.5;
   - Recall@1.
5. Keep our unique metrics:
   - views checked;
   - nodes checked;
   - context size;
   - estimated input tokens;
   - runtime.
6. Add a visual system overview and at least two real qualitative query
   examples.
7. Add a hard limitations section.

Do not claim:

- official Replica/ScanNet results before those runs exist. Current official
  Replica claims must be limited to the imported object-box pilot;
- semantic segmentation mIoU before segmentation GT conversion exists;
- superiority over BBQ without same-dataset evidence;
- live/cached-live model evaluation unless real verified live outputs exist;
- fully automatic pipeline if manual annotation or manual data conversion was
  used.

## 7. Extra Improvements To Bring The Project Closer To Perfection

Recommended technical improvements:

1. Relation-aware graph search:
   - parse target-anchor relations;
   - add metric distance edges;
   - add semantic spatial edges: left, right, front, behind, above, below;
   - rerank with relation satisfaction.
2. Calibrated fallback:
   - start with graph-pruned search;
   - expand to sibling zones if confidence is low;
   - keep token savings while recovering quality.
3. Object-centric export:
   - export a BBQ-style object graph alongside the current hierarchical tree;
   - include object ID, caption/label, center, extent, relations.
4. Flat embedding baseline:
   - CLIP/SigLIP/EVA-style object/view embeddings;
   - compare against graph traversal on the same items.
5. Public-dataset visual grounding:
   - project selected 3D boxes back into camera views;
   - save qualitative overlays for paper figures.
6. Statistical reporting:
   - per-scene means;
   - per-query-type means;
   - bootstrap confidence intervals if time allows.
7. Project page:
   - short demo video;
   - representative query examples;
   - download links for non-restricted artifacts.
8. Claim audit automation:
   - script that checks paper numbers against saved metrics JSON;
   - prevents stale counts and overclaims.

## 8. Risks And Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| ScanNet relational grounding is weak | Low public-dataset quality | Treat the 0.25 exact-object result as the lexical baseline and add target-anchor spatial reranking. |
| Oracle GT map could be mistaken for perception | Overclaim risk | State that official instances are the map input and keep segmentation metrics N/A without predictions. |
| BBQ official code is hard to run | No fair BBQ baseline | Use BBQ as related work and metric guide; do not claim direct comparison. |
| Graph quality drops on public data | Weak result | Report cost/quality trade-off and add fallback expansion. |
| Paper too broad | Reviewer confusion | Make one central claim: graph-pruned semantic search for queryable digital twins. |
| Deadline pressure | Bad submission | Freeze a smaller honest TwinWorld paper rather than inventing incomplete results. |

## 9. Needed From The Team

These are decisions or resources, not coding tasks:

1. Confirm whether the team wants to prioritize:
   - strongest TwinWorld workshop submission by 2026-07-31; or
   - stronger WACV/3DV follow-up after TwinWorld.
2. Confirm available GPU/CUDA resources for public-dataset and baseline runs.
3. Decide whether external repo clones are allowed for BBQ/ConceptGraphs
   expansion.

## 10. Final Recommendation

For TwinWorld 2026, the most credible path is:

```text
Use the current five-scene system as the digital-twin prototype evidence,
use the official Replica and ScanNet object-grounding pilots with BBQ-style metrics,
compare honestly to BBQ as the closest related object-graph approach,
and make the paper visually strong, reproducible, and limitation-aware.
```

Do not present the completed public-dataset ingestion as a solved algorithm. The
ScanNet lexical baseline reaches only 0.25 exact object-ID hit, and fair external
baselines are still unfinished. A clean workshop paper centered on this measured
quality-efficiency problem is stronger than an overclaimed benchmark story.

## Sources Checked

Local project sources:

- `PUBLICATION_VENUE_FIT_ASSESSMENT.md`
- `markdown-papers/beyond_bare_query/beyond_bare_query/beyond_bare_query.md`
- `C:\Users\bear_\Downloads\Telegram Desktop\semanticsplat_vs_bbq.md`
- `outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/metrics_summary.md`
- latest local benchmark: `outputs/week3/benchmark_v2_stub_bbox_enriched_v16/metrics_summary.json`

Official web sources checked on 2026-07-09:

- TwinWorld official page: https://twin-world.github.io/
- ECCV 2026 workshops list: https://eccv.ecva.net/Conferences/2026/Workshops
