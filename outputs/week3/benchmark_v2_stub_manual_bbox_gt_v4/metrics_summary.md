# Metrics Summary

- Run: `benchmark_v2_stub_manual_bbox_gt_v4`
- Benchmark: `five_capture_manual_semantic_index_v2`
- Results: 150/150
- Schema-valid results: 150
- Evaluated results: 150
- Unavailable results: 0
- Accuracy-eligible results: 150
- Queries excluded by scene scope: 0
- Modes: `{"stub": 150}`

## Gate Coverage

| Gate metric | Status | Value |
|---|---|---:|
| result output coverage | measured | 150 / 150 |
| canonical schema validity | measured | 150 / 150 |

## Query Type Coverage

| Query type | Total | Runnable | GT-eligible | Schema-valid | Retrieval hit rate |
|---|---:|---:|---:|---:|---:|
| simple | 50 | 50 | 50 | 50 | 0.9400 |
| compound | 25 | 25 | 25 | 25 | 1.0000 |
| relational | 25 | 25 | 25 | 25 | 1.0000 |
| multi_hop | 25 | 25 | 25 | 25 | 1.0000 |
| functional | 25 | 25 | 25 | 25 | 0.8000 |

## Metrics

`measured` means the denominator contains applicable records. `unavailable` means no executable or GT-eligible record exists. `N/A` is reserved for metrics whose required modality or GT is absent.

| Metric | Status | Value | Numerator / denominator |
|---|---|---:|---:|
| retrieval_success | measured | 0.9467 | 142 / 150 |
| expected_view_hit | measured | 0.7120 | 89 / 125 |
| expected_node_hit | measured | 0.5920 | 74 / 125 |
| expected_zone_hit | measured | 0.9040 | 113 / 125 |
| not_found_correctness | measured | 0.8800 | 22 / 25 |
| runtime_seconds mean | measured | 0.0015 | 150 records |
| checked_view_count mean | measured | 19.4000 | 150 records |
| visited_node_count mean | measured | 3.8800 | 150 records |
| bbox_3d_iou | measured | 0.5592 | 88 records |

## Token Usage

```json
{
  "input": null,
  "output": null,
  "total": null,
  "denominator": 0,
  "status": "unavailable"
}
```

## Warnings

- None
