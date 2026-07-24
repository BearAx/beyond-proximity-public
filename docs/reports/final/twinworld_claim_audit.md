# TwinWorld 2026 Claim Audit

Status date: 2026-07-24.
Paper: `papers/twinworld/main.tex`.

## Allowed Central Claim

> Agent-guided hierarchical search can control the scene evidence presented to
> a semantic reasoner. The hierarchy is evaluated both as an input to query
> traversal and as an output of Cursor/MCP and raw RGB-D construction tracks.
> The current methods reduce context but do not universally preserve flat-search
> quality.

## Evidence Map

| Claim | Status | Evidence |
|---|---|---|
| Qwen executes all 150 queries | SUPPORTED | 150 traces and a complete ledger under `outputs/instruction_agent/five_scene_qwen25_05b_graph_v1/` |
| Qwen uses 300 calls and 239,893 exact native tokens | SUPPORTED | `metrics_summary.json` plus validator |
| Cursor directly constructs five hierarchies through MCP | SUPPORTED | Five saved calls in `docs/experiments/hierarchy_construction/cursor_agent_mcp_v1/` |
| Cursor construction pairwise F1 is 0.616 | SUPPORTED_WITH_CAVEAT | Manual zones are an overlapping project reference, not independent GT |
| Raw constructor reads 97 RGB, 97 depth, and 97 poses with zero ViewJSON reads | SUPPORTED | `outputs/raw_rgbd_hierarchy/five_scene_clip_v1/` |
| Raw hierarchy pairwise F1 is 0.487 | SUPPORTED_WITH_CAVEAT | Comparison is against manual overlapping zones |
| Mean per-query view reduction is 75.5% | SUPPORTED | Per-query mean, 95% CI [73.2, 77.7] |
| Ratio of displayed means 19.4 to 4.77 is 75.4% | SUPPORTED | `1 - 4.77 / 19.40` |
| hit@1 graph-minus-flat is inconclusive | SUPPORTED | -0.088, 95% CI [-0.184, 0.008] |
| hit@3 graph-minus-flat declines significantly | SUPPORTED | -0.120, 95% CI [-0.184, -0.056] |
| Replica is a lexical sanity ceiling | SUPPORTED_WITH_CAVEAT | 48 positive and 8 negative oracle-map queries |
| ScanNet relation-aware Acc@0.25 is 0.604 vs. 0.500 without relations | SUPPORTED | Calibrated v3 output |
| ConceptGraphs has native eight-scene ScanNet and Replica runs | SUPPORTED_WITH_LIMITS | Predicted-map protocols differ from the oracle-map track |
| LangSplat has a complete hardware-adapted one-scene run | SUPPORTED_WITH_LIMITS | 3,000 iterations on a 6 GB GPU; not paper-scale reproduction |

## Forbidden Claims

- Cursor produced the Qwen query metrics or exact token ledger.
- The Cursor UI used zero provider tokens.
- The automatic hierarchy matches or exceeds the manual hierarchy.
- Graph pruning universally preserves flat-search quality.
- Replica ceiling results establish semantic perception accuracy.
- Native ConceptGraphs or LangSplat values form a fair leaderboard against the
  oracle-map experiments.
- The project outperforms BBQ.
- Segmentation mIoU is available.

## Number Gate

Run:

```powershell
python -B scripts\check_twinworld_numbers.py
```

The gate checks all major paper values, required feedback wording, forbidden
legacy wording, figure references, model revisions, denominators, and frozen
validation reports.
