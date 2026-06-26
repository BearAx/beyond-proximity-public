# Metrics Summary

- Run: `conceptgraphs_smoke_v1`
- Benchmark: `six_scene_mixed_gt_v1`
- Results: 1/8
- Schema-valid results: 1
- Evaluated results: 1
- Unavailable results: 0
- Accuracy-eligible results: 0
- Queries excluded by scene scope: 82
- Modes: `{"live": 1}`

## Gate Coverage

| Gate metric | Status | Value |
|---|---|---:|
| result output coverage | measured | 1 / 8 |
| canonical schema validity | measured | 1 / 1 |

## Query Type Coverage

| Query type | Total | Runnable | GT-eligible | Schema-valid | Retrieval hit rate |
|---|---:|---:|---:|---:|---:|
| simple | 3 | 1 | 0 | 1 | N/A |
| compound | 2 | 0 | 0 | 0 | N/A |
| relational | 1 | 0 | 0 | 0 | N/A |
| multi_hop | 1 | 0 | 0 | 0 | N/A |
| functional | 1 | 0 | 0 | 0 | N/A |

## Metrics

`measured` means the denominator contains applicable records. `unavailable` means no executable or GT-eligible record exists. `N/A` is reserved for metrics whose required modality or GT is absent.

| Metric | Status | Value | Numerator / denominator |
|---|---|---:|---:|
| retrieval_success | unavailable | N/A | 0 / 0 |
| expected_view_hit | unavailable | N/A | 0 / 0 |
| expected_node_hit | unavailable | N/A | 0 / 0 |
| expected_zone_hit | unavailable | N/A | 0 / 0 |
| not_found_correctness | unavailable | N/A | 0 / 0 |
| runtime_seconds mean | measured | 65.4509 | 1 records |
| checked_view_count mean | measured | 1.0000 | 1 records |
| visited_node_count mean | measured | 1.0000 | 1 records |
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

- 7 benchmark queries have no saved result
- 3D IoU is N/A because run_config does not confirm reliable depth
- 1 query results lack GT and are excluded from accuracy metrics
