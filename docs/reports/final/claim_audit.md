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

Legacy `default` scene: separate subsection only (8.5× token reduction under documented timing model — not merged into five-scene averages).

## Claim status

| Claim | Verdict | Where in tex |
|-------|---------|--------------|
| Graph reduces views/tokens on five scenes | **supported** | Table 1, abstract |
| hit@1 comparable or slightly better | **supported_with_caveat** | Table 1 (manual GT, stub mode) |
| 8.5× token reduction on demo scene | **supported** (scene-specific) | §5.2 legacy demo |
| 100% room accuracy | **removed** | — |
| 50 challenging find queries | **removed** | — |
| 34% IoU improvement | **removed** | — |
| "Significantly more accurate" hierarchy | **removed** | — |
| ConceptGraphs/LangSplat superiority | **unsupported** | §5.3 smokes only |
| Live VLM evaluation | **out of scope** | Limitations |

## Stale materials (not article source of truth)

| File | Issue | Action |
|------|-------|--------|
| `speaker-script.md` | Overclaims topology/IoU | STALE banner added; use `main.tex` |
| `presentation/slides.md` | Same | STALE banner added |
| `presentation-slides.md` | Same | STALE banner added |

## Person 4 artifact checklist

- [x] `main.tex` — honest abstract, Table 1, expanded Related Work
- [x] `refs.bib` — key P3 citations added
- [x] `claim_audit.md` — this file
- [x] `paper_outline.md` — updated post five-scene merge
- [x] `reproducibility_windows.md` — runner commands, no "pending"
- [x] `article_readiness_checklist.md` — sprint gate
- [x] `notebooks/graph_vs_flat_evidence.ipynb` — Part A + Part B
- [x] Presentation stale notices
- [ ] `main.pdf` — blocked: LaTeX not installed on dev machine (see `BUILD.md`)
- [ ] PR to `main` — team decision (Leo remote ready)

## Reviewer FAQ

**Q: Is five-scene graph-vs-flat missing?**  
A: No. Results are in `outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/` and Table 1.

**Q: Is the runner pending?**  
A: No. `scripts/run_graph_vs_flat.py` with `configs/graph_vs_flat_v2.yaml`.

**Q: Can we call ViewJSON labels "ground truth"?**  
A: Use "reference labels" or "verified view labels" — not independent annotator GT.
