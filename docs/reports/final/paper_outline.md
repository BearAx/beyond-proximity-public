# Paper Outline - SemanticSplat Sprint

Status date: 2026-07-05. Branch: `codex/research-upgrade-baselines-datasets`.

## Working Title

**SemanticSplat: Graph-Pruned Semantic Search over Captured 3D Gaussian Splatting Scenes**

This is still a good TwinWorld-style title. Avoid any title implying ScanNet
scale, live VLM success, or superiority over external baselines.

## One-Paragraph Story

Indoor and outdoor 3DGS reconstructions provide geometry but weak semantic
structure for natural-language queries. SemanticSplat builds a hierarchical
semantic index from captured views and answers queries via top-down graph
traversal instead of exhaustive flat search over the same semantic items. On
five captured scenes (97 views, 1,066 semantic items) and 150 benchmark queries,
graph pruning reduces average views checked by 75.5% and input tokens by 68.2%
relative to flat search. The current lexical graph ranker trades off retrieval
quality: hit@1 is 0.680 (graph) vs 0.768 (flat), and hit@3 is 0.808 vs 0.928
on 125 queries with verified view labels. This frames the project honestly as a
cost-control result and motivates calibrated pruning as the next algorithmic
step.

## Section Skeleton

### 1. Introduction

- Motivation: coordinates are not meaning.
- Gap: flat search scales poorly in context and views checked.
- Research question: cost removed by hierarchy, and quality trade-off introduced
  by pruning.

### 2. Related Work

- Language fields: LERF, LangSplat, Semantic Gaussians, LEGS.
- Open-vocabulary 3D scene graphs: ConceptGraphs, BBQ, OpenScene,
  ConceptFusion.
- Hierarchical graphs and benchmarks: HOV-SG, Hydra, OpenLex3D, ScanRefer.
- Token/context efficiency: AttentionRAG, Provence, TeaRAG, S-Path-RAG.

### 3. Method

- Capture: browser + 3DGS PLY.
- ViewJSON semantic index.
- Hierarchical tree construction and query traversal.
- Flat baseline over identical semantic items.
- Affordance expansion layer.

### 4. Dataset And Benchmark

- Scenes: five captured pilot scenes.
- Current count: 97 ViewJSON annotations and 1,066 semantic items.
- Queries: `benchmark_queries_v2.json` (150 total, 125 with verified view
  labels).
- Efficiency metrics: views checked, input tokens, elapsed ms.
- Quality metrics: hit@1, hit@3 with verified-view denominators.

### 5. Experiments

- Five-scene graph vs flat from `outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/`.
- Per-query-type and per-scene efficiency analysis.
- Ablations from `outputs/graph_vs_flat/ablations_v1/`.
- Scaling stress from `outputs/graph_vs_flat/scaling_stress_v1/`.
- Baseline smokes for LangSplat and ConceptGraphs, without superiority claims.

### 6. Limitations

- Manual reference labels, not independent GT.
- Stub lexical mode, not live VLM.
- No 3D IoU.
- Graph hit@k is lower than flat in the current reproducible run.
- External baselines are smoke/adapted only.
- Replica/ScanNet are not official yet.

### 7. Reproducibility

- `docs/reports/final/reproducibility_windows.md`
- `docs/reports/final/claim_audit.md`
- `docs/datasets/public_dataset_readiness.md`

## Removed Or Blocked Claims

Do not restore:

- 100% room-level topological accuracy.
- 50 challenging find queries.
- 34% IoU improvement.
- "Significantly more accurate" hierarchy superiority.
- Quality parity with flat search.
- ConceptGraphs/LangSplat superiority.
- Official Replica/ScanNet evaluation.
