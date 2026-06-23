# Week 2/3 Delivery and Verification Guide

This document records what was implemented for Phases 1-7 and how to verify it from a clean repository checkout. All commands are run from the repository root.

## Delivered Work

### Evaluation Contract

- Added canonical scene manifest, benchmark query, query result, and metrics schemas under `docs/schemas/`.
- Added `docs/benchmark_queries_v1.json` with 50 unique queries.
- Added `scripts/evaluate_results.py` for coverage-aware metrics and failure reports.
- Added Week 2/3 plans, result reports, failure reports, claims, experiment design, and evaluation protocol.

### Headless Pipeline

- Added `backend/query/model_client.py` with explicit `stub`, `live`, and `cached_live` modes.
- Added `scripts/run_experiment.py` as the canonical config-driven headless runner.
- Added `scripts/run_pipeline.py` as a compatibility entry point.
- Added `configs/week2_replica.yaml` and `configs/week3_replica.yaml`.
- Stub mode is deterministic and never reported as live reasoning.
- Cached-live mode accepts only cache entries with verified live provenance.

### Dataset and Geometry

- Added `scripts/import_replica_scene.py` for Replica-style to backend scene conversion.
- Added `scripts/validate_scene_geometry.py` for depth, resolution, intrinsics, pose, and missing-frame validation.
- Added `scripts/select_views_coverage_greedy.py` with coverage-greedy, random, and trajectory comparison.
- Added scene inventory, manifest documentation, GT mapping notes, and dataset validation report.
- ScanNet is explicitly postponed beyond Week 3.

### Baselines and Reproducibility

- Added baseline references, adapter contracts, feasibility matrix, related-work outline, and query fairness review.
- Added explicit definitions for demo, simulated, stub, live, cached-live, estimated, measured, and unavailable results.
- Added a publication/delivery timeline with ScanNet excluded from Week 3 requirements.
- Baseline smoke execution is blocked honestly because runnable baseline repositories, checkpoints, and valid metric RGB-D are unavailable locally.

### Tests and Outputs

- Added backend tests for model modes, experiment outputs, evaluation, ingestion, geometry validation, and view selection.
- Added a small tracked evaluator fixture at `outputs/week2/phase1_evaluator_smoke/`.
- Full generated gate runs are ignored to avoid committing repetitive output files and can be reproduced using the commands below.

## Prerequisites

- Python environment with the repository's existing dependencies installed.
- Run commands from the repository root.
- No API credentials are required for stub verification.
- Do not install extra dependencies merely to force unavailable live or baseline runs.

## Verification Commands

### 1. Compile Python Entry Points

```powershell
python -m py_compile scripts\run_pipeline.py scripts\run_experiment.py scripts\evaluate_results.py scripts\import_replica_scene.py scripts\validate_scene_geometry.py scripts\select_views_coverage_greedy.py backend\query\model_client.py
```

Expected result: exit code `0` with no syntax errors.

### 2. Validate the Available Scene

```powershell
python -B scripts\validate_scene_geometry.py --scene backend\data\scenes\default
```

Expected result:

- 19 frames, RGB images, depth maps, and poses;
- 19 valid poses;
- constant depth detected in all 19 frames;
- intrinsics/RGB mismatch detected in all 19 frames;
- semantic evaluation allowed;
- 3D localization not allowed;
- `bbox_3d` and `iou_3d` reported as `N/A`.

Machine-readable evidence is stored in `docs/dataset_validation/default_geometry.json`.

### 3. Verify View Selection

```powershell
python -B scripts\select_views_coverage_greedy.py --scene backend\data\scenes\default --k 20
```

Expected result: the script uses all 19 available views, reports effective `K=19`, coverage `1.0`, and warns that the requested K exceeded the scene size.

To reproduce the full K comparison:

```powershell
python -B scripts\select_views_coverage_greedy.py --scene backend\data\scenes\default --k 10 20 50 100 --seed 42 --output docs\dataset_validation\default_view_selection.json
```

### 4. Run the Week 2 Gate

```powershell
python -B scripts\run_experiment.py --config configs\week2_replica.yaml
python -B scripts\evaluate_results.py --benchmark docs\benchmark_queries_v1.json --results outputs\week2\week2_stub_default_gate_v1\query_results --out outputs\week2\week2_stub_default_gate_v1
```

Expected output directory:

```text
outputs/week2/week2_stub_default_gate_v1/
  query_results/             50 JSON files
  model_cache/
  run_config.json
  logs.json
  metrics_summary.json
  metrics_summary.md
  failure_modes.md
```

Expected gate values:

| Check | Expected value |
|---|---:|
| Query files | 50 |
| Schema-valid coverage | 50/50 |
| Mode | `stub` for all records |
| Expected view hit | 34/43 |
| Expected node hit | 35/43 |
| Expected zone hit | 42/43 |
| Negative correctness | 7/7 |
| Token usage | `N/A` |
| 3D IoU | `N/A` |

### 5. Run the Week 3 Gate

```powershell
python -B scripts\run_experiment.py --config configs\week3_replica.yaml
python -B scripts\evaluate_results.py --benchmark docs\benchmark_queries_v1.json --results outputs\week3\week3_stub_default_gate_v1\query_results --out outputs\week3\week3_stub_default_gate_v1
```

Expected output directory:

```text
outputs/week3/week3_stub_default_gate_v1/
  query_results/             50 JSON files
  model_cache/
  run_config.json
  logs.json
  metrics_summary.json
  metrics_summary.md
  failure_modes.md
```

Expected values match Week 2 because both runs use the same deterministic stub, scene, and benchmark. This confirms repeatability, not model accuracy improvement.

### 6. Run Tests

```powershell
python -B -m pytest -q
```

Last verified result:

```text
48 passed in 2.69s
```

Timing can vary by machine. The required condition is that all tests pass.

### 7. Check Repository Cleanliness

```powershell
git diff --check
git status --short
git ls-files | Select-String -Pattern '(^|/)(\.venv|node_modules|__pycache__|\.pytest_cache|\.pytest_tmp)(/|$)|\.zip$|repo_tree\.txt$'
```

Expected result:

- `git diff --check` reports no whitespace errors;
- no archive, virtual environment, cache, or generated-junk path is tracked;
- full Week 2/3 gate outputs remain ignored;
- `outputs/week2/phase1_evaluator_smoke/` remains the small reviewable output fixture.

## Acceptance Status

### Week 2

All required minimum checks pass for the stub prototype:

- one honestly validated semantic scene;
- scene inventory and geometry validation;
- 50 benchmark queries;
- end-to-end CLI execution;
- 50 saved canonical query results;
- generated metrics and failure reports;
- explicit stub/live separation;
- no invalid 3D localization claim.

### Week 3

Required minimum checks pass with documented external blockers:

- repeatable 50-query batch;
- canonical results, metrics, and failure reports;
- improved dataset validation and query fairness documentation;
- provenance-safe cached-live interface;
- baseline adapter setup and exact blocker documentation;
- updated Week 3 reports;
- ScanNet remains postponed.

## Known Blockers

- The only usable local scene is `default`; official Replica scenes are absent.
- `default` has constant `0.1` depth and an intrinsics/RGB mismatch, so final 3D localization metrics are unavailable.
- Independent object, room, and 3D ground truth are absent.
- `SEMANTICSPLAT_PROVIDER`, `SEMANTICSPLAT_MODEL`, and `SEMANTICSPLAT_API_KEY` are not configured.
- A concrete live provider adapter is not installed, so no real live response cache exists.
- Runnable LangSplat/ConceptGraphs repositories, pinned environments, checkpoints, and compatible scene assets are absent.

## Manual Work Still Required

1. Obtain a licensed official Replica scene and import it with `scripts/import_replica_scene.py`.
2. Validate metric depth, calibration, poses, and GT before enabling 3D metrics.
3. Implement and configure a real model provider adapter, run at least one live query, then verify cached-live replay.
4. Pin one mandatory baseline environment and run a small compatible smoke subset.
5. Review the final diff before committing. Do not push without approval.
