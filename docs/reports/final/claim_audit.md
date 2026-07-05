# Claim Audit — `papers/beyond-proximity/main.tex` vs Repository Evidence

Status date: 2026-07-05 (post integration merge). Owner: Person 4 (Telman).

## Integration branch

`week4/integration-article-sprint` merges:
- `week3/final-changes`
- `week3/person1` (graph-vs-flat five scenes)
- `codex/person2-gt-evaluation` (benchmark v2 GT)
- `feature-person-3-baselines-literature` (related work matrix)
- `week3/person4-article-evidence` (audit, notebook, reproducibility)

## Primary evidence (five-scene)

Source: `outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/metrics_summary.json`

| Metric | Flat | Graph | Notes |
|--------|------|-------|-------|
| Views checked (avg) | 19.2 | 5.39 | 71.4% savings |
| Input tokens (avg) | 3104 | 1061.6 | 65.1% savings |
| hit@1 | 0.768 | 0.792 | n=125 GT queries |
| hit@3 | 0.928 | 0.904 | n=125 GT queries |
| Queries total | 150 | 150 | 25 excluded from quality denom |

Mode: **stub lexical** — not live VLM.

## Claim status (updated)

| Claim | Verdict |
|-------|---------|
| Graph reduces views/tokens on five scenes | **supported** (same-input v2 run) |
| hit@1 comparable or slightly better | **supported_with_caveat** (manual GT, stub mode) |
| 8.5× token reduction | **default scene only** — separate subsection |
| 100% room accuracy / 34% IoU | **removed** from tex |
| ConceptGraphs/LangSplat superiority | **unsupported** — smokes only |
| Live VLM evaluation | **out of scope** |

## Article artifacts

- [x] `main.tex` rewritten (honest abstract + Table 1)
- [x] Notebook: default + five-scene sections
- [x] `reproducibility_windows.md`
- [ ] PDF build (needs LaTeX env)
- [ ] Related work full prose from P3 matrix (partial in tex)
