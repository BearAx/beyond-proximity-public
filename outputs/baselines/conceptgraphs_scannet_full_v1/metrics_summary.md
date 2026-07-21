# Metrics Summary

- Run: `conceptgraphs_scannet_full_v1`
- Benchmark: `scannet_bbq_aligned_referit3d_official_gt_pilot_v1`
- Results: 48/48
- Schema-valid results: 48
- Evaluated results: 48
- Unavailable results: 0
- Accuracy-eligible results: 48
- Queries excluded by scene scope: 0
- Modes: `{"live": 48}`

## Gate Coverage

| Gate metric | Status | Value |
|---|---|---:|
| result output coverage | measured | 48 / 48 |
| canonical schema validity | measured | 48 / 48 |

## Query Type Coverage

| Query type | Total | Runnable | GT-eligible | Schema-valid | Retrieval hit rate |
|---|---:|---:|---:|---:|---:|
| simple | 6 | 6 | 6 | 6 | 1.0000 |
| compound | 2 | 2 | 2 | 2 | 1.0000 |
| relational | 40 | 40 | 40 | 40 | 1.0000 |
| multi_hop | 0 | 0 | 0 | 0 | N/A |
| functional | 0 | 0 | 0 | 0 | N/A |

## Raw Query Type Coverage

| Query type | Total | Runnable | GT-eligible | Schema-valid | Retrieval hit rate | Object-ID hit rate | Not-found correctness |
|---|---:|---:|---:|---:|---:|---:|---:|
| attribute | 2 | 2 | 2 | 2 | 1.0000 | 0.0000 | N/A |
| relational | 40 | 40 | 40 | 40 | 1.0000 | 0.0000 | N/A |
| simple_object | 6 | 6 | 6 | 6 | 1.0000 | 0.0000 | N/A |

## Source Dataset Metrics

Missing or invalid 3D-box predictions count as IoU 0 and remain in every Acc@k denominator.

| Source | Queries | Object-ID hit | Acc@0.1 | Acc@0.25 | Acc@0.5 | Runtime mean (s) | Estimated input tokens mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| Nr3D | 24 | 0.0000 | 0.2917 | 0.0417 | 0.0000 | 0.3363 | N/A |
| Sr3D+ | 24 | 0.0000 | 0.2917 | 0.0833 | 0.0000 | 0.3363 | N/A |

## Metrics

`measured` means the denominator contains applicable records. `unavailable` means no executable or GT-eligible record exists. `N/A` is reserved for metrics whose required modality or GT is absent.

| Metric | Status | Value | Numerator / denominator |
|---|---|---:|---:|
| retrieval_success | measured | 1.0000 | 48 / 48 |
| expected_view_hit | measured | 0.5625 | 27 / 48 |
| expected_node_hit | measured | 0.0000 | 0 / 48 |
| expected_zone_hit | unavailable | N/A | 0 / 0 |
| expected_object_hit | measured | 0.1667 | 8 / 48 |
| expected_object_id_hit | measured | 0.0000 | 0 / 48 |
| not_found_correctness | unavailable | N/A | 0 / 0 |
| runtime_seconds mean | measured | 0.3363 | 48 records |
| checked_view_count mean | measured | 1.0833 | 48 records |
| visited_node_count mean | measured | 1.0000 | 48 records |
| context_size_chars mean | unavailable | N/A | 0 records |
| estimated_input_tokens mean | unavailable | N/A | 0 records |
| bbox_3d_iou | measured | 0.0696 | 48 records |
| Acc@0.1 | measured | 0.2917 | 14 / 48 |
| Acc@0.25 | measured | 0.0625 | 3 / 48 |
| Acc@0.5 | measured | 0.0000 | 0 / 48 |

## Measured Token Usage

Token semantics are recorded below. `provider_billing_tokens: false` means local tokenizer/model tokens, not API usage or cost.

```json
{
  "input": 627,
  "output": 0,
  "total": 627,
  "denominator": 48,
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
