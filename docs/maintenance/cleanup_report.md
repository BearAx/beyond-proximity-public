# Repository Cleanup Report

Date: 2026-06-23

Status: documentation reorganization complete; code/config references validated; generated-cache deletion not executed because the workspace safety approval rejected the recursive delete operation.

## Completed Work

- Created a categorized documentation layout under `docs/project`, `docs/schemas`, `docs/datasets`, `docs/validation`, `docs/benchmarks`, `docs/baselines`, `docs/experiments`, `docs/reports`, `docs/maintenance`, and `docs/archive`.
- Moved current Week 1-3 project, benchmark, baseline, dataset, validation, and report documents without deleting their contents.
- Split machine-readable validation evidence into `geometry`, `capture_quality`, and `semantic_index` directories.
- Archived historical demo project logs and deprecated implementation plans. Current design specifications remain active under `docs/project/design/specs`.
- Replaced the generated documentation hub with a curated `docs/README.md` index.
- Redirected future simulated demo logs to `docs/experiments/stub/demo_runs/`; `run_all_docs.sh` no longer overwrites the curated docs index.
- Updated README links, config paths, script defaults, tests, benchmark generator paths, and archived internal links.
- Narrowed the broad `*.ply` ignore rule to the two known local scene-storage paths and added standard Python/build cache ignores.
- Preserved all captured RGB-D scenes, manual ViewJSON annotations, generated semantic trees, PLY assets, ignored evaluation outputs, papers, and publication assets.

## Important Final Paths

- `docs/project/final_week3_acceptance.md`
- `docs/project/week3_results.md`
- `docs/benchmarks/benchmark_queries_v1.json`
- `docs/baselines/baselines_matrix.md`
- `docs/baselines/baseline_status.md`
- `docs/validation/geometry/`
- `docs/validation/capture_quality/`
- `docs/validation/semantic_index/`
- `configs/week3_replica.yaml`
- `scripts/run_experiment.py`
- `scripts/evaluate_results.py`
- `backend/query/model_client.py`

## Changed Areas

| Area | Main changes |
| --- | --- |
| Repository entry points | `.gitignore`, root `README.md`, `docs/README.md` |
| Evaluation paths | `configs/week2_replica.yaml`, `configs/week3_replica.yaml`, `configs/week3_phase_b_semantic_smoke.yaml` |
| Evaluation scripts | `scripts/run_experiment.py`, `scripts/evaluate_results.py`, `scripts/select_views_coverage_greedy.py` |
| Legacy demo generator | `scripts/run_full_benchmark.py`, `backend/query/benchmark_report.py`, `benchmark_reasoning.py`, `project_log.py`, `docs_hub.py` |
| Tests | Benchmark fixture path in `tests/backend/test_evaluation_harness.py` |
| Documentation | Files moved into the categorized directories listed above; links updated in active and archived material. |

Pre-existing dirty-worktree changes in scene annotations, semantic trees, live adapter work, baseline adapters, and their tests were retained. This cleanup did not revert or replace them.

## Cleanup Safety

Both dry runs demonstrated that broad cleanup commands are unsafe:

```powershell
git clean -ndX
git clean -nd
```

They include valuable ignored PLY scene data, Week 2/3 outputs, and untracked semantic-index files. Do not run `git clean -fd` or `git clean -fdX` on this worktree.

The following generated paths remain because the environment rejected the approved-list recursive deletion command before it executed:

| Path | Observed size/status |
| --- | ---: |
| `.matplotlib/` | exists, empty |
| `.pytest_cache/` | 8,983 bytes |
| `.pytest_tmp/` | 1,912,649 bytes |
| Python `__pycache__/` | 13 directories after compile/tests |
| `frontend/dist/` | 320,746 bytes |
| `frontend/node_modules/` | 163,376,339 bytes |

No deletion occurred. These paths are ignored and reproducible, but they still occupy local disk space.

## Validation

Commands run:

```powershell
python -m py_compile scripts\run_experiment.py scripts\evaluate_results.py backend\query\model_client.py backend\query\docs_hub.py backend\query\project_log.py backend\query\benchmark_reasoning.py backend\query\benchmark_report.py scripts\run_full_benchmark.py
python -B -m pytest -q
git diff --check
git status --short
```

Results:

- Python compilation: passed.
- Tests: `87 passed in 4.09s`.
- `git diff --check`: passed; Git emitted only LF-to-CRLF working-copy warnings.
- Documentation local-link check: 0 broken links.
- Required final paths: all present.
- Search for active references to `docs/dataset_validation`, `docs/benchmark_queries_v1.json`, `docs/project_log`, and `docs/superpowers`: no matches outside the maintenance records that document old paths.
- No commit or push was performed.

## Review Required

- Decide whether duplicate local PLY pairs should use Git LFS, external storage, or one canonical local copy. The pairs are byte-for-byte identical, but neither copy was deleted.
- Decide whether root delivery PDFs should move under docs; they remain in place to avoid breaking external references.
- Decide whether tracked publication build products should remain versioned.
- Select small representative Week 2/3 output artifacts explicitly rather than committing ignored full output trees.
- Remove the generated cache/build paths manually only after confirming their resolved paths; do not use broad `git clean` commands.
