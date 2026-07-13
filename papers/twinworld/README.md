# TwinWorld @ ECCV 2026 — Person 4 paper package

Status date: 2026-07-13. Branch: `week6-person4` (from `week6-person3`).

## Files

| File | Purpose |
|------|---------|
| `main.tex` | Anonymous LNCS / ECCV workshop draft |
| `llncs.cls`, `eccv.sty`, `splncs04.bst` | ECCV-style template (from public ECCV template + LNCS) |
| `refs.bib` | Bibliography |
| `figures/` | Paper figures (shared with prior five-scene evidence) |
| `BUILD.md` | Build commands |

## Claim (frozen for this draft)

> SemanticSplat is a graph-pruned semantic search layer for queryable 3DGS digital twins. It reduces query-time context while preserving retrieval on the internal benchmark, and is aligned with BBQ-style Acc@k / Recall@1 on Replica/ScanNet pilots — without claiming superiority over BBQ.

## Evidence sources (team)

- Person 1: `docs/datasets/replica_scannet_plan.md`, official Replica/ScanNet imports
- Person 2: `docs/experiments/public_datasets/person2_grounding_results.md`, `outputs/public_datasets/*_pilot_v1/`
- Person 3: `docs/baselines/bbq_comparison.md`, `docs/baselines/baseline_status.md`
- Person 4 prior figures: internal five-scene charts in `figures/`

## Review vs camera-ready

- Review (default): `\usepackage[review,year=2026,ID=XXXXX]{eccv}` + anonymous authors
- Camera-ready: `\usepackage[final,year=2026]{eccv}` + restore author list

Replace `ID=XXXXX` when OpenReview assigns a paper ID.
