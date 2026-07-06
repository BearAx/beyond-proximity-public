# Research Upgrade Status

Status date: 2026-07-05.

This note records what was added after the Week 4 integration branch and what
still separates the current project from a strong workshop or main-conference
submission.

## What Was Executed

### External baseline smokes

Both mandatory external baselines were rerun locally. ConceptGraphs was then
expanded from smoke scope to all five captured scenes:

| Baseline | Status | Evidence | Valid claim |
|---|---|---|---|
| LangSplat | DONE smoke | `outputs/baselines/langsplat_smoke_v1/` | Official sofa smoke executes and adapts to canonical output. |
| ConceptGraphs | DONE five captured scenes with limitations | `outputs/baselines/conceptgraphs_full_v1/` | Native Docker run produces 150 canonical outputs; drone native map is empty. |

LangSplat remains setup/adapters-only evidence. ConceptGraphs is now a
same-captured-scene baseline artifact, but it is not an official public-dataset
result and does not provide 3D IoU, independent semantic accuracy, or superiority
evidence.

### Current graph-vs-flat evidence

The primary five-scene run was regenerated from the current repository state:

```text
outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/
```

Current reproducible result:

```text
97 captured views
1,066 semantic items
150 queries
125 queries with verified expected view labels
75.5% fewer views checked
68.2% fewer input tokens
hit@1: graph 0.680 vs flat 0.768
hit@3: graph 0.808 vs flat 0.928
```

Interpretation: the current hierarchy is a strong cost-control mechanism, but
the lexical graph ranker sacrifices retrieval quality relative to flat search.
The paper must describe this as a cost/quality trade-off, not quality parity.

### Ablations

New ablation outputs:

```text
outputs/graph_vs_flat/ablations_v1/
```

Variants now measured:

```text
flat_lexical
flat_affordance
graph_tight
graph_default
graph_broad
graph_affordance
```

The main useful evidence is that stricter pruning greatly reduces cost but
hurts hit@k, while broad traversal recovers some recall but loses most token
efficiency. This gives the next algorithmic target: calibrated pruning.

### Scaling stress test

New scaling outputs:

```text
outputs/graph_vs_flat/scaling_stress_v1/
```

This duplicates captured semantic indexes in memory to estimate query-time
growth. It is a stress test, not public-dataset accuracy. It shows graph cost
grows much more slowly than flat scan under duplicated indexes, but Replica or
ScanNet is still required for a publication-grade scaling claim.

### Public dataset readiness

New audit:

```text
docs/datasets/public_dataset_readiness.md
docs/datasets/public_dataset_readiness.json
```

Current status:

```text
official Replica scenes ready: 0
ScanNet scenes ready: 0
local data/replica/pilot_scene_001: proxy only, not official Replica
```

## What We Need For TwinWorld ECCV 2026

TwinWorld is realistic if the paper is framed as a digital-twin semantic-search
prototype with honest scope.

Required before submission:

1. Keep the current five-scene captured benchmark.
2. Keep LangSplat and ConceptGraphs as smoke/adapted baselines, not superiority
   claims.
3. Include ablation and scaling-stress results only with clear guardrails.
4. Use the updated paper language: graph pruning reduces cost but currently
   trades off hit@k under lexical stub ranking.
5. Add one small official Replica scene if legal/local data is available before
   the deadline.

Recommended title for TwinWorld:

```text
SemanticSplat: Graph-Pruned Semantic Search over Captured 3D Gaussian Splatting Scenes
```

## What We Need For AAAI 2027 Main

The current project is not yet AAAI-main ready.

Minimum required additions:

1. Official public dataset evaluation on Replica and/or ScanNet.
2. Independent GT labels or dataset-provided semantic/instance mappings.
3. Fair same-scene baseline comparison against at least ConceptGraphs.
4. A LangSplat comparison if the title keeps Gaussian Splatting central.
5. A stronger algorithm than fixed lexical pruning:
   - calibrated node pruning,
   - fallback expansion when confidence is low,
   - learned or embedding-based node scoring,
   - explicit recall/cost objective.
6. Statistical reporting across scenes/query types.
7. Separate construction cost from per-query cost.

Recommended AAAI-level title direction:

```text
Calibrated Hierarchical Semantic Search for Queryable 3D Digital Twins
```

This title would fit only after the calibrated-pruning and public-dataset work
exists.

## Do We Need Replica And ScanNet?

Yes, but in order:

1. Replica first. It is the best next public-dataset target because it is
   smaller and closer to the indoor semantic-map setting.
2. ScanNet second. It is more credible but heavier and requires accepted data
   terms plus a completed converter.

Do not replace the five captured scenes. Use them as the system/capture pilot
and add public datasets as the reproducibility track.

## Do We Need LangSplat And ConceptGraphs?

Yes.

LangSplat is the mandatory 3DGS-language baseline. ConceptGraphs is the
mandatory scene-graph baseline. For the current sprint, smoke execution is
enough for honest workshop positioning. For a main-conference paper, both need
same-scene evaluation or a clear explanation for why one is infeasible.
