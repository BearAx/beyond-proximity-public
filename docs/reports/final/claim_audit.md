# Claim Audit — `papers/beyond-proximity/main.tex` vs Repository Evidence

Status date: 2026-07-01. Owner: Person 4 (Telman).

Purpose: honest mapping from article claims to measurable evidence. **No claim may appear in the final article without a row marked `supported` or `supported_with_caveat`.**

## Evidence sources used

| Source | Scope | Trust level |
|--------|-------|-------------|
| `docs/benchmark_results/benchmark_default.json` | Scene `default`, 12 queries, graph vs flat | Measured infra + estimated LLM timing |
| `docs/benchmarks/benchmark_graph_vs_flat.md` | Same as above, human-readable report | Derived from JSON |
| `docs/project/final_week3_acceptance.md` | 5 captured scenes, stub gate, baselines | Team acceptance doc |
| `docs/benchmarks/benchmark_queries_v1.json` | 90 queries, mixed GT | Verified on `default` only |
| Query Flow session JSONs | Live Cursor pipeline demos | Qualitative, not benchmark |

## Claim table

| # | Claim in `main.tex` | Evidence today | Verdict | Action for article |
|---|---------------------|----------------|---------|-------------------|
| 1 | Two-Pass Geometric-Semantic clustering builds accurate hierarchies | Demo tree on `default` (15 nodes, depth 2); qualitative failure-case narrative in benchmark report | **partial** | Reframe as method design + demo scene; remove "100% room-level topological accuracy" unless ablation log exists |
| 2 | Pure geometric over-segments ballroom | Narrative in benchmark failure section | **qualitative** | Keep as motivating example; label as case study not large-scale ablation |
| 3 | Pure semantic over-merges rooms | Same | **qualitative** | Same |
| 4 | Graph search uses fewer tokens than flat | `benchmark_default.json`: avg ~6.4k vs ~26.6k tokens (12 queries, `default`) | **supported_with_caveat** | Scope: **legacy `default` scene only**; disclose timing model |
| 5 | Graph checks fewer views than flat | Avg ~4 vs 19 views (report); per-query varies 1–13 | **supported_with_caveat** | Same scope; note projector query checks 13 graph views |
| 6 | Graph ~4× faster (estimated) | Timing formula in benchmark report, not wall-clock live LLM | **supported_with_caveat** | Say "estimated latency under documented model" |
| 7 | Crop-and-Requery improves 2D IoU by 34% | No saved IoU evaluation in repo | **unsupported** | Remove number or move to future work |
| 8 | Tested 50 challenging find queries for bbox | No dataset of 50 with IoU in repo | **unsupported** | Remove or replace with Query Flow qualitative examples |
| 9 | MCP + LLM agent orchestration | Code exists (`backend/mcp/`, Query Flow) | **supported** | Describe architecture honestly |
| 10 | Five-scene evaluation | 5 scenes captured, 40 stub queries, **no graph-vs-flat on captured scenes** | **misleading if implied** | Separate "dataset status" from "graph efficiency result" |
| 11 | Semantic accuracy / hit@k on 5 scenes | `accuracy-eligible results = 0` per Week 3 acceptance | **unsupported** | Do not claim until `benchmark_queries_v2` + Person 1 run |
| 12 | 3D bbox / metric navigation | `bbox_3d` null in pilot; 3D IoU N/A | **unsupported** | Limitations section |
| 13 | Superior to ConceptGraphs / LangSplat | One-frame / one-asset smokes only, no same-input comparison | **unsupported** | Literature context only until Person 3 expands |
| 14 | Live / cached-live VLM evaluation | Out of scope per Week 3 acceptance | **out_of_scope** | Do not mention as evaluated |

## Recommended paper story (honest)

1. **Problem:** 3DGS gives geometry; NL environment queries need semantic structure and context control.
2. **Method:** Capture views → manual/VLM ViewJSON → hierarchical tree → top-down graph traversal vs flat scan.
3. **Prototype evidence (default):** Graph pruning reduces tokens, views checked, and estimated latency vs flat on 12 documented queries.
4. **Dataset progress:** Five additional captured scenes with 1,046 manual semantic items and stub-executable queries.
5. **Open gap:** Same-input graph-vs-flat on five captured scenes — sprint target for Person 1.
6. **Limitations:** Manual index, estimated timing, no independent GT accuracy at scale, no 3D IoU, baseline smokes only.

## Figures/tables checklist (article)

| Item | Data ready? | Owner | Blocker |
|------|-------------|-------|---------|
| Graph vs flat token bar chart | Yes (`default` only) | P4 notebook | None |
| Per-query speedup chart | Yes | P4 notebook | Label as estimated time |
| Failure case (wrong room) | Yes (narrative + sessions) | P4 | Optional screenshot |
| Five-scene dataset table | Yes (acceptance counts) | P4 | None |
| Graph vs flat on 5 scenes | **No** | P1 | Runner not on captured indexes |
| hit@1 / hit@3 table | **No** | P1 + P2 | `benchmark_queries_v2` |
| Related work matrix | **No** | P3 | — |
| Baseline comparison table | **No** | P3 | Fair same-input run |

## Next edits to `main.tex` (when drafting)

- [ ] Rewrite abstract: remove unverified IoU and 100% accuracy claims.
- [ ] Add subsection "Scope of reported results" separating `default` benchmark from five-scene dataset.
- [ ] Replace Experiments with benchmark-backed numbers or mark TBD placeholders.
- [ ] Expand Limitations per Week 3 acceptance wording.
