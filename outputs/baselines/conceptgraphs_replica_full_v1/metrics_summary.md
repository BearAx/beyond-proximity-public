# Metrics Summary

- Run: `conceptgraphs_replica_full_v1`
- Benchmark: `replica_bbq_aligned_official_gt_pilot_v2`
- Results: 56/56
- Schema-valid results: 56
- Evaluated results: 56
- Unavailable results: 0
- Accuracy-eligible results: 56
- Queries excluded by scene scope: 0
- Modes: `{"live": 56}`

## Gate Coverage

| Gate metric | Status | Value |
|---|---|---:|
| result output coverage | measured | 56 / 56 |
| canonical schema validity | measured | 56 / 56 |

## Query Type Coverage

| Query type | Total | Runnable | GT-eligible | Schema-valid | Retrieval hit rate |
|---|---:|---:|---:|---:|---:|
| simple | 24 | 24 | 24 | 24 | 0.6667 |
| compound | 8 | 8 | 8 | 8 | 1.0000 |
| relational | 8 | 8 | 8 | 8 | 1.0000 |
| multi_hop | 8 | 8 | 8 | 8 | 1.0000 |
| functional | 8 | 8 | 8 | 8 | 1.0000 |

## Raw Query Type Coverage

| Query type | Total | Runnable | GT-eligible | Schema-valid | Retrieval hit rate | Object-ID hit rate | Not-found correctness |
|---|---:|---:|---:|---:|---:|---:|---:|
| attribute | 8 | 8 | 8 | 8 | 1.0000 | 0.0000 | N/A |
| functional | 8 | 8 | 8 | 8 | 1.0000 | 0.0000 | N/A |
| multi_hop | 8 | 8 | 8 | 8 | 1.0000 | 0.0000 | N/A |
| negative | 8 | 8 | 8 | 8 | 0.0000 | N/A | 0.0000 |
| relational | 8 | 8 | 8 | 8 | 1.0000 | 0.0000 | N/A |
| simple_object | 16 | 16 | 16 | 16 | 1.0000 | 0.0000 | N/A |

## Source Dataset Metrics

Missing or invalid 3D-box predictions count as IoU 0 and remain in every Acc@k denominator.

| Source | Queries | Object-ID hit | Acc@0.1 | Acc@0.25 | Acc@0.5 | Runtime mean (s) | Estimated input tokens mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| Replica | 56 | 0.0000 | 0.1667 | 0.0625 | 0.0417 | 0.2743 | N/A |

## Metrics

`measured` means the denominator contains applicable records. `unavailable` means no executable or GT-eligible record exists. `N/A` is reserved for metrics whose required modality or GT is absent.

| Metric | Status | Value | Numerator / denominator |
|---|---|---:|---:|
| retrieval_success | measured | 0.8571 | 48 / 56 |
| expected_view_hit | measured | 0.0000 | 0 / 48 |
| expected_node_hit | unavailable | N/A | 0 / 0 |
| expected_zone_hit | unavailable | N/A | 0 / 0 |
| expected_object_hit | measured | 0.1458 | 7 / 48 |
| expected_object_id_hit | measured | 0.0000 | 0 / 48 |
| not_found_correctness | measured | 0.0000 | 0 / 8 |
| runtime_seconds mean | measured | 0.2743 | 56 records |
| checked_view_count mean | measured | 1.3036 | 56 records |
| visited_node_count mean | measured | 1.0000 | 56 records |
| context_size_chars mean | unavailable | N/A | 0 records |
| estimated_input_tokens mean | unavailable | N/A | 0 records |
| bbox_3d_iou | measured | 0.0624 | 48 records |
| Acc@0.1 | measured | 0.1667 | 8 / 48 |
| Acc@0.25 | measured | 0.0625 | 3 / 48 |
| Acc@0.5 | measured | 0.0417 | 2 / 48 |

## Measured Token Usage

Token semantics are recorded below. `provider_billing_tokens: false` means local tokenizer/model tokens, not API usage or cost.

```json
{
  "input": 459,
  "output": 0,
  "total": 459,
  "denominator": 56,
  "status": "measured",
  "tokenizers": [
    "open_clip:ViT-H-14"
  ],
  "token_count_types": [
    "non_padding_text_encoder_tokens"
  ],
  "provider_billing_tokens": false
}
```

## Estimated Context And Tokens

```json
{
  "context_size_chars": {
    "mean": null,
    "total": null,
    "denominator": 0,
    "status": "unavailable"
  },
  "prompt_size_chars": {
    "mean": null,
    "total": null,
    "denominator": 0,
    "status": "unavailable"
  },
  "estimated_input_tokens": {
    "mean": null,
    "total": null,
    "denominator": 0,
    "status": "unavailable"
  }
}
```

## Warnings

- None
