# Anonymous workshop paper package

Status date: 2026-07-21. Publication/site branch: `codex/project-site-method-figure`.

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

## Evidence sources

- Dataset imports: `docs/datasets/replica_scannet_plan.md`
- Grounding results: `docs/experiments/public_datasets/person2_grounding_results.md`, `outputs/public_datasets/*_pilot_v1/`
- Baselines and related work: `docs/baselines/bbq_comparison.md`, `docs/baselines/baseline_status.md`
- Internal five-scene figures: `figures/`
- Graph-construction accounting: `docs/reports/final/graph_construction_cost.json`
- Project page source: `site/` (assembled by `scripts/build_project_site.py`)

## Review vs camera-ready

- Review: `scripts/build_twinworld_review.ps1 -PaperId <assigned numeric ID>` + anonymous authors
- Camera-ready: `\usepackage{eccv}` + restore the author list from a private source

The source contains no placeholder ID. OpenReview assigns the real ID, which is
kept in ignored `review_id.tex`. `scripts/build_twinworld_preprint.ps1` creates
an ID-free pre-submission PDF and refreshes `main.pdf`, but that PDF is not the
ECCV review upload until it is rebuilt with the assigned numeric ID.

The review PDF intentionally includes blue marginal line numbers. ECCV requires
line numbering for initial submissions and removes it for camera-ready papers.
The review source contains no author names, affiliations, acknowledgements,
appendix, or external links.

The repeated `Anonymous` labels are deliberate template output, not missing
project information. Put the real author list, in final order, into the private
OpenReview form. After acceptance, restore exact names, affiliations, and email
addresses in a private camera-ready source and compile without `[review]`.

Before portal registration, the team must agree:

- exact author spelling and order;
- affiliation(s) and corresponding-author email;
- each author's OpenReview identity and conflicts;
- whether the repository must be made private to satisfy the ECCV publicity
  policy.
