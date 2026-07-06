# Metrics Summary

- Run: `conceptgraphs_full_v1`
- Benchmark: `five_capture_manual_semantic_index_v2`
- Results: 150/150
- Schema-valid results: 150
- Evaluated results: 150
- Unavailable results: 0
- Accuracy-eligible results: 150
- Queries excluded by scene scope: 0
- Modes: `{"live": 150}`

## Gate Coverage

| Gate metric | Status | Value |
|---|---|---:|
| result output coverage | measured | 150 / 150 |
| canonical schema validity | measured | 150 / 150 |

## Query Type Coverage

| Query type | Total | Runnable | GT-eligible | Schema-valid | Retrieval hit rate |
|---|---:|---:|---:|---:|---:|
| simple | 50 | 50 | 50 | 50 | 0.5000 |
| compound | 25 | 25 | 25 | 25 | 0.8000 |
| relational | 25 | 25 | 25 | 25 | 0.8000 |
| multi_hop | 25 | 25 | 25 | 25 | 0.8000 |
| functional | 25 | 25 | 25 | 25 | 0.8000 |

## Metrics

`measured` means the denominator contains applicable records. `unavailable` means no executable or GT-eligible record exists. `N/A` is reserved for metrics whose required modality or GT is absent.

| Metric | Status | Value | Numerator / denominator |
|---|---|---:|---:|
| retrieval_success | measured | 0.7000 | 105 / 150 |
| expected_view_hit | measured | 0.2240 | 28 / 125 |
| expected_node_hit | measured | 0.0000 | 0 / 125 |
| expected_zone_hit | measured | 0.0000 | 0 / 125 |
| not_found_correctness | measured | 0.2000 | 5 / 25 |
| runtime_seconds mean | measured | 0.0747 | 150 records |
| checked_view_count mean | measured | 0.8333 | 150 records |
| visited_node_count mean | measured | 0.8000 | 150 records |
| bbox_3d_iou | N/A | N/A | 0 records |

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

- 3D IoU is N/A because run_config does not confirm reliable depth
