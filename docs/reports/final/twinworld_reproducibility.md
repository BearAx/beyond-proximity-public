# Workshop paper reproducibility freeze

Status date: 2026-07-24. Publication/site branch: `codex/project-site-method-figure`.

## Commit hash

Paper evidence tip audited by integration:

```
62cf94a179f2b9f42a1cb122e0106f5ac957bdf0
(short: 62cf94a on week6-person4)
```

Integration verification commit:

```
b23359a923ef3ede19e16bb35a0c1be6018087d9
(short: b23359a on codex/week6-integration)
```

The following documentation-only freeze commit records that immutable parent
hash without changing the experiment or paper evidence.

Paper path: `papers/twinworld/main.tex`  
PDF: `papers/twinworld/main.pdf`

Latest ID-free local PDF check: 14 pages total, with content through page 13
and references continuing to page 14. Every page was rendered at 120 DPI and
reviewed. There are no float-only pages, placeholder paper IDs, team-role
labels, clipped figures, misplaced result floats, or overlapping tables.

## Evidence sources (do not invent)

| Track | Path |
|---|---|
| Internal five-scene v2 | `outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/metrics_summary.json` |
| Complete Qwen instruction agent | `outputs/instruction_agent/five_scene_qwen25_05b_graph_v1/` |
| Cursor-Agent/MCP hierarchy construction | `docs/experiments/hierarchy_construction/cursor_agent_mcp_v1/` |
| Four construction variants | `docs/experiments/hierarchy_construction/four_variant_v1/` |
| Automatic RGB-D hierarchy | `outputs/raw_rgbd_hierarchy/five_scene_clip_v1/` |
| Four deterministic/embedding controls | `outputs/agent_semantic/five_scene_four_variant_v1/` |
| Per-query | `.../per_query_results.json` |
| Replica calibrated v3 | `outputs/public_datasets/phase6_replica_calibrated_v3/` |
| ScanNet calibrated v3 | `outputs/public_datasets/phase6_scannet_calibrated_v3/` |
| ScanNet extended v3 | `outputs/public_datasets/phase6_scannet_extended_v3/` |
| ConceptGraphs ScanNet | `outputs/baselines/conceptgraphs_scannet_full_v1/` |
| ConceptGraphs Replica | `outputs/baselines/conceptgraphs_replica_full_v1/` |
| LangSplat ScanNet | `outputs/baselines/langsplat_scannet_full_v1/` |
| Paired bootstrap intervals | `docs/reports/final/twinworld_bootstrap_ci.json` |
| Graph construction tokens/runtime | `docs/reports/final/graph_construction_cost.json` |
| Claim audit | `docs/reports/final/twinworld_claim_audit.md` |
| Number gate | `docs/reports/final/twinworld_number_check.md` |

## Frozen internal numbers (from metrics_summary.json)

| Metric | Flat | Graph |
|---|---:|---:|
| Views checked (avg) | 19.4 | 4.77 |
| Input tokens (avg) | 3168.2 | 1014.26 |
| Mean per-query savings | - | 75.5% views / 68.2% tokens |
| hit@1 (n=125 GT) | 0.768 | 0.68 |
| hit@3 (n=125 GT) | 0.928 | 0.808 |
| Cumulative tokens (150 q) | 475230 | 152139 |

Note: older `PERSON1_DELIVERABLE.md` roundings (19.2 to 5.39, hit@1
0.792) are **superseded** by the JSON above. Always prefer the JSON.

The ratio of displayed mean view counts is 75.4%. The 75.5% primary estimate
is the mean of the 150 per-query reductions; this distinction is explicit in
the paper.

## New measured tracks

| Track | Main result |
|---|---|
| Qwen2.5-0.5B instruction agent | 150 queries; 300 calls; 239,893 exact tokens; hit@1 0.368; hit@3 0.696; 9.63 views/query |
| Cursor Agent + MCP construction | 5 direct calls; 18 zones; pairwise F1 0.616; hit@1 0.704; hit@3 0.784; 5.53 views/query |
| Pose + semantic construction | Pairwise F1 0.570; hit@1 0.784; hit@3 0.904; 5.80 views/query |
| Raw RGB-D hierarchy construction | 97 RGB + 97 depth + 97 poses; 15 model calls; 151 label tokens; 0 manual ViewJSON reads; 14.15 s |
| Raw hierarchy structure | Macro pairwise F1 0.487 and Rand index 0.637 against manual overlapping zones |
| Raw hierarchy retrieval | hit@1 0.368; hit@3 0.528; 10.0 views/query vs. 19.4 flat CLIP |
| ScanNet calibrated v3 | Recall@1 / Acc@0.25 0.604; 4.73 objects and 219 estimated tokens/query |

## Commands

```bash
# Figures
python -B scripts/export_paper_figures.py --out-dir papers/twinworld/figures
python -B scripts/export_twinworld_figures.py
python -B scripts/export_twinworld_agent_figures.py

# Complete measured runs and validators
python -B scripts/run_instruction_agent_benchmark.py --methods graph_instruction
python -B scripts/validate_instruction_agent_benchmark.py
python -B scripts/run_raw_rgbd_hierarchy_benchmark.py
python -B scripts/validate_raw_rgbd_hierarchy_benchmark.py
python -B scripts/evaluate_hierarchy_construction.py --config configs/hierarchy_construction_v1.json --out docs/experiments/hierarchy_construction/four_variant_v1

# Cross-check numbers vs main.tex
python -B scripts/check_twinworld_numbers.py
python -B scripts/compute_twinworld_bootstrap.py
python -B scripts/measure_graph_construction.py --repeats 7

# Static project page
python -B scripts/build_project_site.py
python -m http.server 4173 --directory site-dist

# ID-free pre-submission PDF
powershell -ExecutionPolicy Bypass -File scripts/build_twinworld_preprint.ps1

# Anonymous review PDF after OpenReview assigns the numeric ID
powershell -ExecutionPolicy Bypass -File scripts/build_twinworld_review.ps1 -PaperId <assigned-number>
```

Scene PNGs for qualitative/gallery figures may require:

```bash
git lfs pull --include="backend/data/scenes/*/images/v001.png,backend/data/scenes/default/images/v0*.png"
```

## External submission actions

- Register the paper, then run `build_twinworld_review.ps1` with the assigned
  numeric OpenReview paper ID. Do not edit a placeholder into `main.tex`.
- Complete the final human author-profile, citation, and anonymity review.
- Upload the anonymous PDF by the TwinWorld deadline.
- Camera-ready: use `\usepackage{eccv}` and restore authors/affiliations from a
  private source.

The template files were checked byte-for-byte against the official ECCV 2026
author kit at upstream commit
`da8c09c40239d5665757527e77388f4716a6564a`. Dataset, evaluation, and baseline
evidence and run IDs were verified in the integration audit.
