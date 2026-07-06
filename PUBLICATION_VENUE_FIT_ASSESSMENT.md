# SemanticSplat Publication Venue Fit Assessment

Status date: 2026-07-06.

Current article checked:

```text
papers/beyond-proximity/main.tex
papers/beyond-proximity/main.pdf
```

Current strongest evidence:

```text
outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/
outputs/graph_vs_flat/ablations_v1/
outputs/graph_vs_flat/scaling_stress_v1/
outputs/baselines/langsplat_smoke_v1/
outputs/baselines/conceptgraphs_smoke_v1/
docs/datasets/public_dataset_readiness.md
docs/reports/final/claim_audit.md
docs/reports/final/research_upgrade_status.md
```

Important correction: the requirements file still says 1,046 semantic items in
its header and a few requirement notes. The current repository and article
evidence say **97 captured views and 1,066 semantic items**. Use 97 / 1,066 in
any submission.

## Executive Decision

Best immediate target: **TwinWorld @ ECCV 2026 Workshop**.

Best main-conference target after one more research sprint: **WACV 2027 Round 2,
Evaluations & Datasets Track or Applications Track**.

Do not target **AAAI 2027 Main Track** with the current paper unless the team can
add a stronger algorithmic result, public-dataset evaluation, and fair baseline
comparison before 2026-07-28. That is too risky from the current state.

Recommended strategy:

1. Submit a focused TwinWorld version by 2026-07-31 if the team wants a fast,
   topical workshop publication.
2. Keep the TwinWorld version either short, or make the later WACV/3DV version
   substantially extended with new experiments, public datasets, and stronger
   baselines.
3. Use August to prepare a stronger WACV/3DV version.

## Current Article Truth State

The article is now honest and internally consistent, but its result is not yet a
"graph is better" result. The correct current claim is:

```text
SemanticSplat reduces query-time search/context cost by graph pruning over the
same semantic items, but the current lexical stub ranker has lower hit@k than
flat search.
```

Current main numbers:

| Metric | Current result |
|---|---:|
| Captured pilot scenes | 5 |
| Captured views | 97 |
| Semantic items | 1,066 |
| Benchmark queries | 150 |
| Queries with verified view labels | 125 |
| Graph view reduction vs flat | 75.5% |
| Graph token reduction vs flat | 68.2% |
| Flat hit@1 | 0.768 |
| Graph hit@1 | 0.680 |
| Flat hit@3 | 0.928 |
| Graph hit@3 | 0.808 |

This is a good workshop result and a promising systems/evaluation result. It is
not yet a strong main-conference algorithmic result because quality decreases.

## Venue Ranking

| Rank | Venue | Current fit | Fit after realistic 2-6 week improvements | Recommendation |
|---:|---|---:|---:|---|
| 1 | TwinWorld @ ECCV 2026 Workshop | 78/100 | 88/100 | Submit first if fast publication is desired. |
| 2 | WACV 2027 | 66/100 | 84/100 | Best main-conference path after strengthening experiments. |
| 3 | 3DV 2027 | 61/100 | 80/100 | Good if the 3D grounding and public-data story are improved. |
| 4 | NeurIPS 2026 Workshops | 55/100 | 75/100 | Good opportunistic route if the right workshop appears. |
| 5 | ICRA 2027 | 43/100 | 70/100 | Only after adding robotics/navigation evaluation. |
| 6 | AAAI 2027 Main Track | 38/100 | 68/100 | Too risky for the current deadline and evidence level. |

## Requirement Coverage Summary

| Requirement from venue notes | Current status | Evidence | What to change |
|---|---|---|---|
| Clear research claim | PARTIALLY_DONE | `main.tex` abstract and intro | Keep cost-control claim; do not say quality is preserved. |
| 3-4 contribution bullets | DONE | `main.tex` introduction | Make bullets venue-specific. |
| Graph-vs-flat benchmark | DONE | `five_scene_graph_vs_flat_v2` | Freeze run ID and commit hash in paper. |
| Same-input comparison | DONE | `claim_audit.md` | Explain same scenes/items/queries more explicitly. |
| Query-type breakdown | DONE | `fig_by_query_type.*`, `main.tex` | Add small interpretation paragraph per venue. |
| Ablation study | PARTIALLY_DONE | `ablations_v1` | Add table to paper; current paper mentions results only lightly. |
| Scaling analysis | PARTIALLY_DONE | `scaling_stress_v1` | State it is synthetic duplication, not public-dataset scale. |
| Error/failure analysis | PARTIALLY_DONE | `fig_failure_cases.*`, `main.tex` | Add current five-scene failure cases, not only legacy demo cases. |
| Flat embedding baseline | NOT_DONE | No evidence found | Add embedding retrieval baseline before WACV/3DV/AAAI. |
| External baselines | PARTIALLY_DONE | LangSplat/ConceptGraphs smoke outputs | For main conferences, convert to fair same-scene comparisons. |
| Public dataset evaluation | NOT_DONE | `public_dataset_readiness.md` | Add official Replica first; ScanNet second. |
| Independent GT / 3D boxes | NOT_DONE | `claim_audit.md` | Need dataset GT or independent annotation. |
| 3D visual grounding | PARTIALLY_DONE | Paper figures are mostly metric charts | Add scene screenshots, graph overlays, query-flow figure. |
| Reproducible code/data package | PARTIALLY_DONE | Tests and scripts exist | Add anonymized submission package and reproduction README. |
| Venue formatting | NOT_DONE | Current paper uses `cvpr` style | Convert to selected venue template. |
| Anonymization | NOT_DONE | Current paper has author names | Create double-blind submission version. |

## 1. TwinWorld @ ECCV 2026 Workshop

Current fit: **78/100**.

Why it fits:

- TwinWorld is explicitly about built-environment digital twins, semantic 3D
  understanding, hierarchical representations, Gaussian splatting, robotics, and
  benchmark-driven evaluation.
- The current title and abstract already speak directly to captured 3DGS scenes
  and graph-pruned semantic search.
- The five-scene graph-vs-flat result is enough for a workshop if it is framed
  honestly as cost reduction with a quality trade-off.

What currently satisfies the requirements:

- Digital-twin / 3DGS framing.
- Semantic graph and affordance-aware query story.
- Same-input graph-vs-flat benchmark.
- Quantitative results on 150 queries.
- Baseline smoke evidence for LangSplat and ConceptGraphs.
- Honest limitations section.

What is missing or weak:

- The paper is not in ECCV LNCS format.
- The current paper has author names, so it is not anonymized.
- The current result does not preserve retrieval quality; graph hit@k is lower.
- Visual evidence is too chart-heavy. TwinWorld will benefit from real scene
  screenshots, semantic overlays, and a query-flow diagram.
- LangSplat and ConceptGraphs are smoke baselines only, not comparisons.

Required changes before submission:

1. Convert `main.tex` from CVPR style to ECCV 2026 LNCS workshop style.
2. Prepare an anonymized review PDF.
3. Add a system overview figure and at least one real captured-scene figure.
4. Add an ablation table from `outputs/graph_vs_flat/ablations_v1/`.
5. Replace any "preserving retrieval quality" wording with "cost/quality
   trade-off" unless a new calibrated ranker closes the hit@k gap.
6. Decide page strategy:
   - 4-page short version if you want to protect future WACV/3DV submissions.
   - 8-10 page full workshop version if TwinWorld is the primary target.

Verdict: **Submit here first if the team accepts workshop scope.** This is the
best match for the project as it exists today.

## 2. WACV 2027

Current fit: **66/100**.

Best track: **Evaluations & Datasets Track** or **Applications Track**.

Why it fits:

- WACV welcomes practical vision systems, 3D computer vision, robotics, AR/VR,
  visualization, and evaluation/dataset papers.
- The project has a real system and a reproducible benchmark protocol.
- WACV's Evaluation & Dataset track is friendly to careful benchmark and
  failure-mode papers, including negative or trade-off results.

What currently satisfies the requirements:

- 8-page style is realistic after compression.
- The paper already has method, benchmark, experiments, limitations, and related
  work.
- There is a reproducible test-backed codebase and generated outputs.
- The ablation and scaling stress outputs are good WACV material.

What is missing or weak:

- No public dataset result yet.
- No flat embedding baseline.
- No fair five-scene LangSplat or ConceptGraphs comparison.
- Current benchmark uses manual/reference labels, not independent GT.
- The paper needs a clearer evaluation contribution if submitted to E&D.

Required changes before WACV:

1. Add a `flat_embedding` baseline and report it next to `flat_lexical`.
2. Add official Replica evaluation if possible.
3. Add an annotation/evaluation protocol section: how labels were created,
   verified, and used.
4. Add a public release plan for queries, schemas, and semantic JSONs.
5. Add current five-scene error analysis, especially where graph pruning loses
   hit@k.
6. Convert to WACV 2027 template and anonymize.
7. Prepare supplementary ZIP with code/data instructions.

Verdict: **Best main-conference target after one more research sprint.** If the
team wants a stronger publication than a workshop, WACV Round 2 should be the
main plan.

## 3. 3DV 2027

Current fit: **61/100**.

Why it fits:

- The topic touches 3D scene representation, semantic 3D search, captured views,
  and Gaussian splatting.
- 3DV is a natural place if the paper convincingly shows that the graph is
  grounded in 3D scene structure rather than only text/JSON search.

What currently satisfies the requirements:

- 3DGS framing in title/abstract.
- Five captured scenes with RGB-D/view annotations.
- Semantic graph/tree structure.
- Same-input benchmark and chart figures.

What is missing or weak:

- The current evaluation is mostly semantic-index retrieval, not strong 3D
  vision evidence.
- No official Replica/ScanNet evaluation.
- No 3D IoU, object boxes, masks, or metric localization.
- External 3D baselines are smokes only.
- Few visual 3D examples in the article.

Required changes before 3DV:

1. Add real scene screenshots/renders with semantic overlays.
2. Add graph-to-view grounding examples: query -> region -> view -> visual
   evidence.
3. Add official Replica or ScanNet results, even if small.
4. Add stronger spatial relations: `visible_from`, `near`, `connected_to`,
   region/zone constraints.
5. Add fairer comparison to at least one external 3D semantic method, or clearly
   position against flat retrieval only.
6. Convert to 3DV style and fit 8 pages.

Verdict: **Promising but not ready yet.** 3DV becomes realistic if the team adds
more visual/3D grounding and public-dataset evidence.

## 4. AAAI 2027 Main Technical Track

Current fit: **38/100**.

Why it is risky:

- AAAI needs a broader AI contribution, not just a 3D system demo.
- The current dataset is too small for a strong general AI claim.
- The main result has lower graph hit@k than flat search.
- Deadline is very close: abstract due 2026-07-21, full paper due 2026-07-28.

What currently satisfies the requirements:

- The paper can be framed as graph-based semantic search / reasoning.
- It reports efficiency and quality trade-offs.
- It has reproducible scripts and benchmark outputs.

What is missing or weak:

- No strong new algorithm beyond deterministic/lexical graph pruning.
- No public dataset.
- No embedding/learned/calibrated retrieval baseline.
- No formal graph-search objective.
- No statistical significance or broader generalization.
- External baselines are not fair comparisons.

Required changes before AAAI would be credible:

1. Add calibrated graph pruning or confidence-based fallback expansion.
2. Add embedding-based node scoring and flat embedding baseline.
3. Add official public dataset evaluation.
4. Add fair ConceptGraphs/LangSplat comparison or remove any implication of
   superiority.
5. Formalize the task, graph operations, pruning policy, and cost/recall
   objective.
6. Add statistical reporting across scenes/query types.
7. Rewrite into 7-page AAAI style with a general AI framing.

Verdict: **Do not submit the current version to AAAI main.** It is not impossible
as a future direction, but it is not ready for the 2026-07-28 full-paper
deadline.

## 5. ICRA 2027

Current fit: **43/100**.

Why it is conditional:

- The project can become robotics-relevant, but the current paper is offline
  semantic search over captured scenes.
- ICRA reviewers will look for robot/agent tasks, navigation, actionability,
  runtime in a decision loop, and ideally video/system evidence.

What currently satisfies the requirements:

- Affordance queries such as sitting, exits, facilities, and environment
  understanding are robotics-adjacent.
- Query-time efficiency is relevant to embodied agents.
- Captured indoor/outdoor scenes can support robot-style framing.

What is missing or weak:

- No robot or embodied-agent evaluation.
- No navigation/path-planning experiment.
- No action success metric.
- No metric localization or path feasibility.
- No ROS/simulator integration.

Required changes before ICRA:

1. Add a navigation or embodied-query task: current view -> target region/view.
2. Add actionability metrics: correct usable region/object, wrong-room rate,
   wrong-zone rate, failure-to-act rate.
3. Add a simple simulator or robot-agent loop, even if lightweight.
4. Add a short demo video.
5. Avoid claiming metric navigation unless geometry/path evidence exists.
6. Convert to IEEE/PaperPlaza style and fit the stricter page budget.

Verdict: **Not the right first target.** Consider ICRA only after adding an
embodied-agent evaluation.

## 6. NeurIPS 2026 Workshops

Current fit: **55/100**.

Why it can fit:

- The project can be framed as spatial memory, semantic environment reasoning,
  graph retrieval, or world-model querying for agents.
- Workshop expectations can be more flexible than main conferences.

What currently satisfies the requirements:

- Natural-language environment query benchmark.
- Graph/context-efficiency result.
- Honest limitations.
- Reproducible local pipeline.

What is missing or uncertain:

- There is no single NeurIPS workshop requirement; the team must choose a
  specific accepted workshop and CFP.
- Current paper is too computer-vision-system oriented for many NeurIPS
  workshops.
- If the workshop is archival or full-length, it may conflict with later
  submissions.

Required changes before NeurIPS workshop submission:

1. Wait for accepted workshop list/CFPs and choose one on embodied AI, spatial
   intelligence, world models, graph reasoning, or agent memory.
2. Prepare a 4-page extended abstract to preserve future main-conference
   options.
3. Reframe as agent spatial memory / efficient semantic context selection.
4. Include the cost/quality trade-off as the main lesson.
5. Avoid heavy 3DGS claims unless the workshop is explicitly spatial/3D.

Verdict: **Good backup/opportunistic route.** Do not make it the primary plan
until a matching workshop CFP is selected.

## Paper Changes Needed Regardless of Venue

Must fix before any submission:

1. Create an anonymized review version.
2. Convert to the selected venue template.
3. Replace stale 1,046-item references with 1,066 everywhere.
4. Freeze the experiment commit hash and run ID.
5. Add explicit statement that LangSplat and ConceptGraphs are smoke baselines,
   not fair comparisons.
6. Add a stronger system overview figure.
7. Add real captured-scene visual examples.
8. Add the ablation table from `outputs/graph_vs_flat/ablations_v1/`.
9. Add a reproducibility paragraph with commands and artifacts.
10. Add a submission-specific limitations paragraph.

Strongly recommended before WACV/3DV/main-conference submission:

1. Add `flat_embedding`.
2. Add calibrated graph pruning or fallback expansion to recover hit@k.
3. Add official Replica evaluation.
4. Add current five-scene failure-case analysis.
5. Add independent GT or at least independent review of reference labels.
6. Add a project page/demo video.
7. Prepare anonymized supplementary code/data.

## Recommended Submission Plan

### Plan A: Fast And Honest

Target: TwinWorld @ ECCV 2026.

Timeline:

| Date range | Work |
|---|---|
| 2026-07-06 to 2026-07-12 | Convert to ECCV LNCS, anonymize, add visuals and ablation table. |
| 2026-07-13 to 2026-07-20 | Add system diagram, query-flow figure, and stronger limitations. |
| 2026-07-21 to 2026-07-27 | Final proofread, reproduce tables, prepare supplementary/demo. |
| 2026-07-28 to 2026-07-31 | Submit. |

Use this title:

```text
SemanticSplat: Graph-Pruned Semantic Search over Captured 3D Gaussian Splatting Scenes
```

### Plan B: Stronger Main-Conference Route

Target: WACV 2027 Round 2.

Timeline:

| Date range | Work |
|---|---|
| 2026-07-06 to 2026-07-20 | Add embedding baseline and current failure analysis. |
| 2026-07-21 to 2026-08-04 | Add Replica scene ingestion/evaluation if data is available. |
| 2026-08-05 to 2026-08-14 | Add calibrated graph pruning/fallback and rerun experiments. |
| 2026-08-15 to 2026-08-21 | Convert to WACV style, anonymize, package supplementary. |
| 2026-08-21 | Enroll paper. |
| 2026-08-28 | Submit. |

Use this framing:

```text
An Evaluation of Graph-Pruned Semantic Search for Queryable 3D Environments
```

### Plan C: Do Not Do Unless The Team Can Sprint Hard

Target: AAAI 2027 Main.

Only choose this if by 2026-07-21 the team has:

- calibrated graph method,
- improved graph hit@k close to flat,
- embedding baseline,
- stronger algorithmic formalization,
- clean 7-page AAAI draft.

Otherwise, skip AAAI main and protect the stronger WACV/3DV path.

## Final Recommendation

Submit to **TwinWorld @ ECCV 2026** if the team wants the best realistic match
for the current article. Prepare it honestly as a digital-twin workshop paper
about graph-pruned semantic search and cost/quality trade-offs.

For a serious main-conference paper, aim for **WACV 2027 Round 2** after adding
embedding retrieval, calibrated pruning, current failure analysis, and at least
one public-dataset evaluation.

## Official Sources Checked

- TwinWorld @ ECCV 2026: https://twin-world.github.io/
- ECCV 2026 Submission Policies: https://eccv.ecva.net/Conferences/2026/SubmissionPolicies
- WACV 2027 Call for Papers: https://wacv.thecvf.com/Conferences/2027/CallForPapers
- WACV 2027 Author Guidelines: https://wacv.thecvf.com/Conferences/2027/AuthorGuides
- 3DV 2027 official page: https://3dvconf.github.io/2027/
- 3DV 2026 Author Guidelines as page-limit reference: https://3dvconf.github.io/2026/author-guidelines/
- ICRA official IEEE RAS page: https://www.ieee-ras.org/conferences-workshops/fully-sponsored/icra/
- ICRA 2027 site: https://2027.ieee-icra.org/
- AAAI-27 Main Technical Track CFP: https://aaai.org/conference/aaai/aaai-27/main-technical-track-call/
- NeurIPS 2026 Dates: https://neurips.cc/Conferences/2026/Dates
