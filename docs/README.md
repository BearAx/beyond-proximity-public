# SemanticSplat Documentation

This index separates current evaluation evidence from the older simulated product-demo benchmark. Start with the Week 3 acceptance report for the current project status.

## Project Status

| Document | Purpose |
| --- | --- |
| [Final Week 3 acceptance](project/final_week3_acceptance.md) | Acceptance status, measured results, blocked work, and claims not made. |
| [Week 3 results](project/week3_results.md) | Five-scene semantic-index and stub-gate results. |
| [Real evaluation status](project/real_evaluation_status.md) | Stub, live, cached-live, semantic, and geometry status. |
| [Claims](project/claims.md) | Allowed and unsupported research claims. |
| [Reproducibility notes](project/repo_reproducibility_notes.md) | Execution modes and reproducibility boundaries. |
| [Publication timeline](project/publication_timeline.md) | Current milestones and postponed work. |
| [Launch guide (RU)](project/launch_guide_ru.md) | Local application and demo instructions. |

## Evaluation

| Area | Documents |
| --- | --- |
| Benchmark | [Queries v1](benchmarks/benchmark_queries_v1.json), [protocol](benchmarks/evaluation_protocol.md), [experiment design](benchmarks/experiment_design.md), [query fairness](benchmarks/query_fairness_review.md) |
| Schemas | [Query result](schemas/query_result_schema.md), [benchmark query](schemas/benchmark_query_schema.md), [metrics](schemas/metrics_record_schema.md), [scene manifest](schemas/scene_manifest_schema.md), [ViewJSON](schemas/view_json_schema.md) |
| Dataset | [Scene inventory](datasets/scene_inventory.md), [validation report](datasets/dataset_validation_report.md), [capture workflow](datasets/manual_capture_5_scene_checklist.md), [semantic-index workflow](datasets/five_scene_semantic_index_workflow.md) |
| Validation evidence | [Geometry](validation/geometry/), [capture quality](validation/capture_quality/), [semantic indexes](validation/semantic_index/), [Week 3 verification](validation/week3_verification/) |
| Headless retrieval | [Evaluation guide](experiments/semantic_retrieval/headless_evaluation.md) |

## Baselines

| Document | Purpose |
| --- | --- |
| [Baseline status](baselines/baseline_status.md) | Current ConceptGraphs and LangSplat blockers. |
| [Feasibility matrix](baselines/baselines_matrix.md) | Inputs, adapters, blockers, and ownership. |
| [Adapter contracts](baselines/baseline_adapter_contracts.md) | Canonical baseline output requirements. |
| [ConceptGraphs smoke](baselines/conceptgraphs/conceptgraphs_smoke_result.md) | Attempted command and exact blockers. |
| [LangSplat smoke](baselines/langsplat/langsplat_smoke_result.md) | Attempted command and exact blockers. |

## Reports

- [Week 1](reports/week1/week1_status.md)
- [Week 2 plan](reports/week2/week2_plan.md), [results](reports/week2/week2_results.md), and [failure modes](reports/week2/week2_failure_modes.md)
- [Week 3 plan](reports/week3/week3_plan.md) and [failure modes](reports/week3/week3_failure_modes.md)

## Legacy Demo Evidence

The [graph-vs-flat report](benchmarks/benchmark_graph_vs_flat.md), [charts and videos](benchmark_results/), and [archived run logs](archive/old_notes/project_log/) are simulated demo evidence. Their estimated latency and keyword-oracle behavior are not live-model evaluation results. New demo runs are written under `docs/experiments/stub/demo_runs/` and do not overwrite this index.

## Maintenance And Archive

- [Cleanup audit](maintenance/cleanup_audit.md)
- `docs/maintenance/cleanup_report.md` records the completed cleanup validation.
- [Deprecated material](archive/deprecated/)
- [Review-required material](archive/review_required/)

## Core Commands

```powershell
python -B scripts\run_experiment.py --config configs\week3_replica.yaml --mode stub --out outputs\week3\final_stub_semantic_gate_v1
python -B scripts\evaluate_results.py --benchmark docs\benchmarks\benchmark_queries_v1.json --results outputs\week3\final_stub_semantic_gate_v1\query_results --out outputs\week3\final_stub_semantic_gate_v1
python -B -m pytest -q
```
