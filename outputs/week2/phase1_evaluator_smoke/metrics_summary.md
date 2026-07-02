# Metrics Summary

- Run: `phase1_evaluator_smoke`
- Benchmark: `default_semantic_index_v1`
- Results: 6/50
- Schema-valid results: 6
- Modes: `{"stub": 6}`

## Metrics

| Metric | Value | Numerator / denominator |
|---|---:|---:|
| retrieval_success | 1.0000 | 6 / 6 |
| expected_view_hit | 0.8000 | 4 / 5 |
| expected_node_hit | 1.0000 | 5 / 5 |
| expected_zone_hit | 1.0000 | 5 / 5 |
| not_found_correctness | 1.0000 | 1 / 1 |
| runtime_seconds mean | N/A | 0 records |
| checked_view_count mean | 0.8333 | 6 records |
| visited_node_count mean | 3.0000 | 6 records |
| bbox_3d_iou | N/A | N/A |

## Token Usage

```json
{
  "input": null,
  "output": null,
  "total": null,
  "denominator": 0
}
```

## Warnings

- 44 benchmark queries have no saved result
- 3D IoU is N/A because run_config does not confirm reliable depth
