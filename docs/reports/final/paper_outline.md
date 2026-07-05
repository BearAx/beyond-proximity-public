# Paper Outline (honest scope) — SemanticSplat Sprint

Status date: 2026-07-05. Person 4 draft. Branch: `week4/integration-article-sprint`.

## Working title

**SemanticSplat: Graph-Pruned Semantic Search over Captured 3D Gaussian Splatting Scenes**

Avoid title implying ScanNet-scale validation or baseline superiority.

## One-paragraph story

Indoor and outdoor 3DGS reconstructions provide geometry but weak semantic structure for natural-language queries. SemanticSplat builds a hierarchical semantic index from captured views and answers queries via top-down graph traversal instead of exhaustive flat search over the same semantic items. On five captured scenes (96 views, 1,046 items) and 150 benchmark queries, graph pruning reduces average views checked by 71.4% and input tokens by 65.1% relative to flat search, with hit@1 of 0.792 vs 0.768 on 125 queries with verified view labels. A legacy Conference Hall demo scene motivates room-disambiguation analysis with larger token reductions under a documented timing model.

## Section skeleton (mapped to `main.tex`)

### 1. Introduction
- Motivation: coordinates ≠ meaning.
- Gap: flat search scales poorly in context.
- Contribution bullets (supported only — see `claim_audit.md`).

### 2. Related Work
- Language fields (LERF, LangSplat, Semantic Gaussians).
- Open-vocabulary 3D scene graphs (ConceptGraphs, BBQ, HOV-SG, Hydra).
- Benchmark framing (OpenLex3D, ScanRefer — future metrics).
- Token/context efficiency (AttentionRAG, Provence, TeaRAG — metric framing only).
- Source matrix: `docs/baselines/related_work_article_matrix.md`.

### 3. Method
- Capture (browser + 3DGS PLY).
- ViewJSON semantic index.
- Tree construction and query traversal.
- Flat baseline (same semantic items).
- Affordance expansion layer.

### 4. Benchmark & Metrics
- Scenes: five captured + legacy `default`.
- Queries: `benchmark_queries_v2.json` (150 total, 125 with view GT).
- Efficiency: views, tokens, elapsed ms.
- Quality: hit@1, hit@3 with GT-aware denominators.

### 5. Experiments
- **5.1** Five-scene graph vs flat (Table 1 — primary).
- **5.2** Legacy demo scene (qualitative room failure + token model).
- **5.3** Baselines scope (smokes only, no superiority).

### 6. Limitations
- Manual reference labels; stub lexical mode; no 3D IoU; uneven graph benefit.

### 7. Reproducibility
- `reproducibility_windows.md`, notebook, run ID `five_scene_graph_vs_flat_v2`.

## Figures & tables (status)

| Priority | Asset | Status |
|----------|-------|--------|
| P0 | Table 1 five-scene graph vs flat | Done (`main.tex`) |
| P0 | Graph vs flat tokens (`default`) | Notebook Part A |
| P0 | Five-scene summary | Notebook Part B + `metrics_summary.json` |
| P1 | Per-query speedup chart | Notebook |
| P1 | Failure case diagram | Qualitative in tex; UI capture optional |
| P2 | Related work comparison table | Matrix in docs; prose in tex |
| P2 | PDF build | Needs LaTeX env (`BUILD.md`) |

## Removed / blocked claims

Do not restore: 100% room-level topological accuracy, 50 challenging find queries, 34% IoU improvement, "significantly more accurate" hierarchy superiority.
