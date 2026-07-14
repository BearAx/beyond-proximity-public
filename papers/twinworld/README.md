# TwinWorld @ ECCV 2026 — Person 4 paper package

Status date: 2026-07-14. Integrated branch: `codex/week6-integration`.

## Files

| File | Purpose |
|------|---------|
| `main.tex` | Anonymous LNCS / ECCV workshop draft |
| `llncs.cls`, `eccv.sty`, `splncs04.bst` | Exact official ECCV 2026 author-kit files |
| `refs.bib` | Bibliography |
| `figures/` | Paper figures (shared with prior five-scene evidence) |
| `BUILD.md` | Build commands |

## Claim (frozen for this draft)

> SemanticSplat is a graph-pruned semantic search layer for queryable 3DGS
> digital twins. It reduces query-time context with a measured internal
> hit-at-k tradeoff, and matches flat lexical quality on the current
> BBQ-aligned oracle-map pilots while checking fewer objects. It does not claim
> superiority over BBQ.

## Evidence sources (team)

- Person 1: `docs/datasets/replica_scannet_plan.md`, official Replica/ScanNet imports
- Person 2: `docs/experiments/public_datasets/person2_grounding_results.md`, `outputs/public_datasets/*_pilot_v1/`
- Person 3: `docs/baselines/bbq_comparison.md`, `docs/baselines/baseline_status.md`
- Person 4 prior figures: internal five-scene charts in `figures/`

## Review vs camera-ready

- Review (default): `\usepackage[review,year=2026,ID=XXXXX]{eccv}` + anonymous authors
- Camera-ready: `\usepackage[final,year=2026]{eccv}` + restore author list

Replace `ID=XXXXX` when OpenReview assigns a paper ID.
