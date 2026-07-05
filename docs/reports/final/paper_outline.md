# Paper Outline (honest scope) — SemanticSplat Sprint

Status date: 2026-07-01. Person 4 draft.

## Working title options

1. **SemanticSplat: Graph-Pruned Semantic Search over Captured 3D Gaussian Splatting Views**
2. **Beyond Flat Search: Hierarchical Semantic Traversal for 3DGS Scene Understanding**

Avoid title implying ScanNet-scale validation or baseline superiority.

## One-paragraph story

Indoor 3D reconstructions and 3DGS models provide geometry but weak semantic structure for natural-language queries. We present SemanticSplat, a rendering-first pipeline that builds a hierarchical semantic index from captured views and answers queries via top-down graph traversal instead of exhaustive flat search. On the legacy Conference Hall demo scene (`default`), graph pruning reduces input tokens and views checked compared to a flat baseline under a documented timing model. We further report a five-scene captured dataset with 1,046 manual semantic items and stub-executable queries, and define the remaining step—same-input graph-vs-flat evaluation on that dataset—as the active research milestone.

## Section skeleton

### 1. Introduction
- Motivation: coordinates ≠ meaning.
- Gap: flat search scales poorly in context.
- Contribution bullets (only supported claims — see `claim_audit.md`).

### 2. Related Work
- Placeholder for Person 3 matrix.
- Families: language fields, 3DGS semantics, object graphs, hierarchical scene graphs.

### 3. Method
- Capture (browser + 3DGS PLY).
- ViewJSON semantic index.
- Tree construction (two-pass — design level).
- Query: decompose → traverse → leaf check.
- Flat baseline definition (same semantic items).

### 4. Benchmark & Metrics
- Scenes: `default` (full tree) + five captured (dataset status).
- Query types from `benchmark_queries_v1` / future v2.
- Efficiency: tokens, views, llm_calls, estimated latency.
- Quality: hit@k only where `verification_status` is verified.

### 5. Experiments
- **5.1** Graph vs flat on `default` (notebook + JSON).
- **5.2** Failure case: wrong-room flat vs graph (qualitative).
- **5.3** Five-scene dataset statistics (no efficiency claim yet).
- **5.4** TBD: captured-scene graph-vs-flat (Person 1).

### 6. Limitations
- Manual ViewJSON; not independent GT.
- Estimated LLM timing on default benchmark.
- No 3D IoU.
- Live VLM out of scope.
- Baseline smokes not comparable.

### 7. Reproducibility
- Pointer to `reproducibility_windows.md` + Mac `start_all.sh`.

## Figures & tables (priority)

| Priority | Asset | Status |
|----------|-------|--------|
| P0 | Graph vs flat tokens (default) | Notebook |
| P0 | Dataset summary table (5 scenes) | Can draft now |
| P1 | Per-query speedup | Notebook |
| P1 | Failure case diagram | Needs UI capture |
| P2 | hit@k table | Blocked on P1+P2 |
| P2 | Related work table | Blocked on P3 |
