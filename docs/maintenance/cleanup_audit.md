# Repository Cleanup Audit

Date: 2026-06-23

Scope: documentation reorganization and safe generated-file cleanup. This audit was written before any move or deletion in this cleanup pass.

## Safety findings

- `git clean -ndX` is unsafe for this repository. It proposes deleting ignored PLY scene assets, canonical `backend/data/scenes/*/geometry/` directories, Week 2/3 outputs, and ordinary caches.
- `git clean -nd` is also unsafe. It proposes deleting the user-authored/generated five-scene semantic trees, query files, baseline adapters, baseline docs, and tests that are not tracked yet.
- The five files under `scenes/*.ply` are byte-for-byte SHA-256 matches for the corresponding `backend/data/scenes/<scene>/geometry/scene.ply` files. Both copies are ignored by the current `*.ply` rule. They are valuable data and are not deletion candidates in this pass.
- The worktree already contains substantial Week 2/3 changes. Cleanup must preserve all existing modifications and untracked semantic-index evidence.

## Classification

### KEEP

| Path | Reason |
| --- | --- |
| `backend/`, `frontend/`, `scripts/`, `tests/`, `configs/` | Product code, evaluation code, tests, and reproducible configuration. |
| `backend/data/scenes/` | Captured RGB-D scenes, metadata, manual ViewJSON, semantic trees, and query files. These are current evaluation inputs. |
| `data/` | Dataset delivery and ingestion inputs. |
| `papers/`, `markdown-papers/` | Tracked publication source, references, and extracted research notes. Review separately before any pruning. |
| `docs/assets/` | README and documentation assets. |
| `outputs/week2/phase1_evaluator_smoke/` | Small tracked reproducibility sample. |
| Root `README.md`, `CITATION.cff`, launch scripts, `.github/` | Repository entry points and operational tooling. |
| All existing user changes and untracked Week 2/3 implementation files | Active work; no cleanup action may discard them. |

### MOVE

The following map organizes active documents by meaning. Filenames remain unchanged unless noted.

| Current path | Destination |
| --- | --- |
| `docs/final_week3_acceptance.md` | `docs/project/final_week3_acceptance.md` |
| `docs/week3_results.md` | `docs/project/week3_results.md` |
| `docs/claims.md` | `docs/project/claims.md` |
| `docs/publication_timeline.md` | `docs/project/publication_timeline.md` |
| `docs/real_evaluation_status.md` | `docs/project/real_evaluation_status.md` |
| `docs/repo_reproducibility_notes.md` | `docs/project/repo_reproducibility_notes.md` |
| `docs/repo_setup_notes.md` | `docs/project/repo_setup_notes.md` |
| `docs/launch_guide_ru.md` | `docs/project/launch_guide_ru.md` |
| `docs/benchmark_queries_v1.json` | `docs/benchmarks/benchmark_queries_v1.json` |
| `docs/benchmark_graph_vs_flat.md` | `docs/benchmarks/benchmark_graph_vs_flat.md` |
| `docs/benchmark_scene_coverage.md` | `docs/benchmarks/benchmark_scene_coverage.md` |
| `docs/evaluation_protocol.md` | `docs/benchmarks/evaluation_protocol.md` |
| `docs/experiment_design.md` | `docs/benchmarks/experiment_design.md` |
| `docs/query_fairness_review.md` | `docs/benchmarks/query_fairness_review.md` |
| `docs/baseline_*.md`, `docs/baselines_matrix.md` | `docs/baselines/` |
| `docs/related_work_notes.md`, `docs/related_work_outline.md`, `docs/baseline_references.bib` | `docs/baselines/` |
| `docs/baselines/conceptgraphs_smoke_*.md` | `docs/baselines/conceptgraphs/` |
| `docs/baselines/langsplat_smoke_*.md` | `docs/baselines/langsplat/` |
| `docs/dataset_validation/*_geometry.json`, `*_view_selection.json` | `docs/validation/geometry/` |
| `docs/dataset_validation/*_semantic_index.json` | `docs/validation/semantic_index/` |
| `docs/dataset_validation/*_capture_check.json` | `docs/validation/capture_quality/` |
| `docs/dataset_validation_report.md`, `docs/scene_inventory.md`, capture/conversion/annotation docs | `docs/datasets/` |
| `docs/week1_status.md` | `docs/reports/week1/week1_status.md` |
| `docs/week2_*.md` | `docs/reports/week2/` |
| `docs/week3_failure_modes.md`, `docs/week3_plan.md` | `docs/reports/week3/` |
| `docs/week3_phase_*.md`, `docs/week2_week3_delivery_verification.md` | `docs/validation/week3_verification/` |

All moved path references in README files, Markdown, configs, scripts, and tests must be updated in the same pass.

### ARCHIVE

| Path | Destination | Reason |
| --- | --- | --- |
| `docs/superpowers/plans/` | `docs/archive/deprecated/superpowers_plans/` | Historical implementation plans; one explicitly warns that its schemas are outdated. |
| `docs/project_log/` | `docs/archive/old_notes/project_log/` | Historical demo benchmark logs. The active log generator must be redirected before the move. |
| `docs/scene_manifest_schema.md` | `docs/archive/deprecated/scene_manifest_schema_pointer.md` | Duplicate pointer; the normative schema already exists under `docs/schemas/`. |

The design specifications under `docs/superpowers/specs/` are not deprecated. They will move to `docs/project/design/`, with links updated.

### DELETE_SAFE

Only these explicit generated paths are approved for deletion after absolute-path verification:

- `.matplotlib/`
- `.pytest_cache/`
- `.pytest_tmp/`
- Python `__pycache__/` directories and `*.pyc` files
- `frontend/dist/`
- `frontend/node_modules/`

No `git clean -fd`, `git clean -fdX`, wildcard scene deletion, or output-directory deletion is approved.

### REVIEW_REQUIRED

| Path | Reason |
| --- | --- |
| `scenes/*.ply` and `backend/data/scenes/*/geometry/scene.ply` | Exact duplicate pairs, but both are valuable untracked source/canonical data. Decide storage policy and Git LFS/external-data policy before deleting either copy. |
| `PROJECT_REPORT.pdf` | Tracked publication/delivery artifact at repository root. Its canonical destination is not clear. |
| `SemanticSplat_*Windows.pdf` | Tracked launch documentation at repository root; moving it may break external links. |
| `docs/benchmark_results/` | Tracked legacy demo output and media still used by README and generator code. Reorganization requires coordinated generator/output migration and is deferred to avoid rewriting historical evidence. |
| `papers/beyond-proximity/main.{aux,bbl,blg,log,out,pdf}` | Tracked publication build products. They may be intentional delivery artifacts; do not delete in a generic cleanup. |
| Ignored `outputs/week2/` and `outputs/week3/` | Reproducibility evidence. Keep locally; only small representative outputs should be selected for version control deliberately. |

## Implementation order

1. Create the target documentation directories.
2. Move active documents and validation reports using the map above.
3. Redirect the project-log generator, then archive existing historical logs.
4. Move design specs and deprecated plans separately.
5. Update code, config, tests, README links, and documentation references.
6. Re-run reference searches and repository validation.
7. Delete only the explicit cache/build paths after checking each resolved path is inside this repository.
8. Record results and unresolved review items in `docs/maintenance/cleanup_report.md`.
