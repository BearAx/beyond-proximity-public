# Project Status And Scale-Up Report

Status date: 2026-07-05.

## Executive Summary

SemanticSplat / Beyond Proximity is a reproducible semantic-map evaluation
prototype. It is strongest as a TwinWorld-style workshop project: a captured
3DGS semantic-search system with same-input graph-vs-flat evaluation,
ablation/scaling evidence, and external baseline smokes.

Current safe claim:

```text
On five manually captured pilot scenes, graph-pruned semantic search scans far
fewer views and uses fewer input tokens than flat lexical search over identical
semantic items. In the current reproducible lexical run, this efficiency comes
with lower hit@k than flat search, so the result should be framed as a
cost/quality trade-off rather than quality parity.
```

## Current Captured-Scene Counts

| Item | Count |
|---|---:|
| Captured pilot scenes | 5 |
| Captured pilot ViewJSON annotations | 97 |
| Semantic items | 1,066 |
| Complete semantic trees | 5 |
| Semantic-index executable scenes | 5/5 |
| Geometry-evaluation-ready scenes | 0/5 |

The legacy `default` scene remains separate demo evidence and is not part of the
five-scene paper averages.

## Primary Graph-vs-Flat Result

Source:

```text
outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/
```

| Metric | Flat | Graph |
|---|---:|---:|
| Views checked, average | 19.4 | 4.77 |
| Input tokens, average | 3168.2 | 1014.3 |
| hit@1 | 0.768 | 0.680 |
| hit@3 | 0.928 | 0.808 |

Valid claim:

```text
75.5% fewer views checked and 68.2% fewer input tokens in stub lexical mode.
```

Invalid claim:

```text
Graph search preserves or improves hit@k.
```

## Baseline Smokes

| Baseline | Status | Evidence | Caveat |
|---|---|---|---|
| LangSplat | Rerun successful | `outputs/baselines/langsplat_smoke_v1/` | Official sofa scene only |
| ConceptGraphs | Rerun successful with native warning | `outputs/baselines/conceptgraphs_smoke_v1/` | One captured frame only |

Neither baseline is a fair five-scene comparison yet.

## New Research-Upgrade Evidence

| Artifact | Purpose |
|---|---|
| `outputs/graph_vs_flat/ablations_v1/` | Pruning/affordance ablations |
| `outputs/graph_vs_flat/scaling_stress_v1/` | In-memory query-time scaling stress test |
| `docs/datasets/public_dataset_readiness.md` | Replica/ScanNet readiness gate |
| `docs/reports/final/research_upgrade_status.md` | TwinWorld vs AAAI roadmap |

## Current Limitations

- Manual reference labels are not independent GT.
- The five-scene benchmark uses lexical stub matching, not live VLM calls.
- The current graph ranker loses hit@k relative to flat search.
- No independent 3D boxes or masks are available, so 3D IoU is unavailable.
- LangSplat and ConceptGraphs are smoke/adapted only.
- Official Replica and ScanNet evaluation are not done.

## Scale-Up Plan

### P0: Calibrated Pruning

Recover quality while keeping most of the graph cost reduction:

- node-score confidence calibration;
- fallback expansion when confidence is low;
- learned or embedding-based node scoring;
- explicit recall/cost objective.

### P1: Official Replica Track

Replica should be the first public-dataset target:

- acquire legal official scene data;
- import RGB/depth/poses/intrinsics;
- map semantic/instance labels to query GT;
- rerun graph-vs-flat and at least ConceptGraphs on the same scene.

### P2: ScanNet Track

ScanNet is a larger main-conference target:

- accept/download official data outside git;
- finish the ScanNet converter;
- validate labels, instances, poses, intrinsics, and boxes;
- create GT-backed query splits.

### P3: Fair External Baselines

For publication-grade comparison:

- run ConceptGraphs on the same public scenes and queries;
- run LangSplat if the paper keeps a 3DGS-centered title;
- report construction cost separately from per-query cost;
- use identical query strings and GT denominators.

## Claims We Still Must Not Make

- No official Replica result exists yet.
- No official ScanNet result exists yet.
- No independent semantic accuracy exists yet.
- No 3D IoU result exists yet.
- No fair external baseline head-to-head result exists yet.
- No live/cached-live provider result is in scope.
