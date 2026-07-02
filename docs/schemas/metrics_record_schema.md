# Metrics Record Schema

Schema ID: `semanticsplat.metrics_record.v1`

`metrics_summary.json` is an aggregate over canonical query results and benchmark expectations.

## Required Sections

```json
{
  "schema_version": "semanticsplat.metrics_record.v1",
  "run_id": "week2_stub_001",
  "benchmark_id": "default_semantic_index_v1",
  "generated_at": "2026-06-21T00:00:00+00:00",
  "coverage": {
    "benchmark_query_count": 50,
    "result_count": 0,
    "missing_result_count": 50,
    "schema_valid_result_count": 0
  },
  "mode_counts": {},
  "metrics": {
    "retrieval_success": {"value": null, "numerator": 0, "denominator": 0},
    "expected_view_hit": {"value": null, "numerator": 0, "denominator": 0},
    "expected_node_hit": {"value": null, "numerator": 0, "denominator": 0},
    "expected_zone_hit": {"value": null, "numerator": 0, "denominator": 0},
    "not_found_correctness": {"value": null, "numerator": 0, "denominator": 0},
    "runtime_seconds": {"mean": null, "total": null, "denominator": 0},
    "token_usage": {"input": null, "output": null, "total": null, "denominator": 0},
    "checked_view_count": {"mean": null, "total": 0, "denominator": 0},
    "visited_node_count": {"mean": null, "total": 0, "denominator": 0},
    "bbox_3d_iou": {"value": null, "status": "N/A", "reason": "No reliable GT 3D boxes"}
  },
  "failure_categories": {},
  "per_query": [],
  "warnings": []
}
```

## Aggregation Rules

- Rates use only records eligible for that metric.
- Missing result files reduce coverage but do not enter accuracy denominators.
- Invalid schema results are retained in `per_query` with errors and excluded from metric denominators.
- Runtime and token aggregates distinguish unavailable (`null`) from measured zero.
- `bbox_3d_iou.value` remains `null` unless reliable prediction and GT boxes are both present.
- Failure category counts may exceed failed-query count because one query can have multiple causes.
