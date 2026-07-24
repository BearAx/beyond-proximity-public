# Anonymous workshop paper package

Status date: 2026-07-24. Publication/site branch: `codex/project-site-method-figure`.

## Files

| File | Purpose |
|------|---------|
| `main.tex` | Anonymous LNCS / ECCV workshop draft |
| `llncs.cls`, `eccv.sty`, `splncs04.bst` | Exact official ECCV 2026 author-kit files |
| `refs.bib` | Bibliography |
| `figures/` | Paper figures (shared with prior five-scene evidence) |
| `BUILD.md` | Build commands |

## Claim (frozen for this draft)

> Agent-guided hierarchical search controls the scene evidence presented at
> query time. The complete 150-query Qwen run is fully metered; five direct
> Cursor-Agent/MCP calls evaluate the original agent construction path; and a
> separate frozen CLIP pipeline builds a predicted hierarchy from raw RGB-D and
> poses without reading manual ViewJSON. Calibrated Replica/ScanNet oracle-map
> pilots isolate retrieval efficiency. The paper does not claim superiority
> over BBQ, ConceptGraphs, or LangSplat.

## Evidence sources

- Dataset imports: `docs/datasets/replica_scannet_plan.md`
- Grounding results: `docs/experiments/public_datasets/person2_grounding_results.md`, `outputs/public_datasets/*_pilot_v1/`
- Baselines and related work: `docs/baselines/bbq_comparison.md`, `docs/baselines/baseline_status.md`
- Internal five-scene figures: `figures/`
- Complete instruction agent:
  `outputs/instruction_agent/five_scene_qwen25_05b_graph_v1/`
- Cursor-Agent/MCP construction:
  `docs/experiments/hierarchy_construction/cursor_agent_mcp_v1/`
- Four hierarchy-construction variants:
  `docs/experiments/hierarchy_construction/four_variant_v1/`
- Raw RGB-D hierarchy:
  `outputs/raw_rgbd_hierarchy/five_scene_clip_v1/`
- New generated figures/macros:
  `scripts/export_twinworld_agent_figures.py`, `tables/new_experiment_macros.tex`
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
