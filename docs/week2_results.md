# Week 2 Results

Status: Week 2 execution gate passed for the deterministic stub prototype. No live-model, baseline, or final 3D localization result is claimed.

## Gate Run

| Field | Value |
|---|---|
| Run ID | `week2_stub_default_gate_v1` |
| Mode | `stub` |
| Scene | `default` |
| Saved query results | 50 |
| Schema-valid coverage | 50/50 |
| Output path | `outputs/week2/week2_stub_default_gate_v1/` |
| Committed representative fixture | `outputs/week2/phase1_evaluator_smoke/` (6 queries) |

The full gate output is generated and intentionally ignored to avoid committing repetitive run artifacts. It is reproduced from the tracked config and command below.

## Measured Stub Metrics

| Metric | Value | Interpretation |
|---|---:|---|
| Retrieval status | 50/50 | Deterministic stub completion, not independent-GT accuracy. |
| Negative correctness | 7/7 | Stub no-match behavior over semantic-index expectations. |
| Expected view hit | 34/43 | Existing ViewJSON-derived expectations. |
| Expected node hit | 35/43 | Existing-tree expectations. |
| Expected zone hit | 42/43 | Existing-tree expectations. |
| Mean query runtime | 0.001 s | Local deterministic code only. |
| Token usage | `N/A` | Stub mode makes no model calls. |
| 3D IoU | `N/A` | Constant depth, intrinsics mismatch, and missing independent 3D GT. |

## Commands

```powershell
python -B scripts\validate_scene_geometry.py --scene backend\data\scenes\default
python -B scripts\select_views_coverage_greedy.py --scene backend\data\scenes\default --k 20
python -B scripts\run_experiment.py --config configs\week2_replica.yaml
python -B scripts\evaluate_results.py --benchmark docs\benchmark_queries_v1.json --results outputs\week2\week2_stub_default_gate_v1\query_results --out outputs\week2\week2_stub_default_gate_v1
```

## Acceptance

| Requirement | Status | Evidence |
|---|---|---|
| Honest usable scene | Pass for semantic evaluation only | `default`: 19 frames; semantic allowed; 3D disallowed. |
| Inventory and geometry validation | Pass | `scene_inventory.md`; validator detects 19 constant-depth frames. |
| At least 50 benchmark queries | Pass | 50 unique queries in `benchmark_queries_v1.json`. |
| End-to-end CLI stub | Pass | Fresh gate run completed without UI/Cursor. |
| Saved query results and reports | Pass | 50 JSON results, metrics summary, and failure report generated. |
| Stub/live separation | Pass | All 50 records and run config say `stub`; no live result exists. |
| Honest 3D claims | Pass | 3D metrics are explicitly `N/A`. |

## Blockers

- No official Replica scene or second evaluation scene is available locally.
- Live execution lacks a provider adapter and credentials; no live response exists to cache.
- No external baseline checkout, pinned environment, checkpoint, or valid metric RGB-D input is available.
- View/node/zone expectations are semantic-index regression labels, not independent dataset GT.
