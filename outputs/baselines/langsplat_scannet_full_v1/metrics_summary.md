# Metrics Summary

- Run: `langsplat_scannet_full_v1`
- Benchmark: `scannet_bbq_aligned_referit3d_official_gt_pilot_v1`
- Results: 6/6
- Schema-valid results: 6
- Evaluated results: 6
- Unavailable results: 0
- Accuracy-eligible results: 6
- Queries excluded by scene scope: 42
- Modes: `{"live": 6}`

## Gate Coverage

| Gate metric | Status | Value |
|---|---|---:|
| result output coverage | measured | 6 / 6 |
| canonical schema validity | measured | 6 / 6 |

## Query Type Coverage

| Query type | Total | Runnable | GT-eligible | Schema-valid | Retrieval hit rate |
|---|---:|---:|---:|---:|---:|
| simple | 1 | 1 | 1 | 1 | 1.0000 |
| compound | 0 | 0 | 0 | 0 | N/A |
| relational | 5 | 5 | 5 | 5 | 0.0000 |
| multi_hop | 0 | 0 | 0 | 0 | N/A |
| functional | 0 | 0 | 0 | 0 | N/A |

## Raw Query Type Coverage

| Query type | Total | Runnable | GT-eligible | Schema-valid | Retrieval hit rate | Object-ID hit rate | Not-found correctness |
|---|---:|---:|---:|---:|---:|---:|---:|
| relational | 5 | 5 | 5 | 5 | 0.0000 | 0.0000 | N/A |
| simple_object | 1 | 1 | 1 | 1 | 1.0000 | 0.0000 | N/A |

## Source Dataset Metrics

Missing or invalid 3D-box predictions count as IoU 0 and remain in every Acc@k denominator.

| Source | Queries | Object-ID hit | Acc@0.1 | Acc@0.25 | Acc@0.5 | Runtime mean (s) | Estimated input tokens mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| Nr3D | 3 | 0.0000 | N/A | N/A | N/A | 2.0365 | N/A |
| Sr3D+ | 3 | 0.0000 | N/A | N/A | N/A | 2.0365 | N/A |

## Metrics

`measured` means the denominator contains applicable records. `unavailable` means no executable or GT-eligible record exists. `N/A` is reserved for metrics whose required modality or GT is absent.

| Metric | Status | Value | Numerator / denominator |
|---|---|---:|---:|
| retrieval_success | measured | 0.1667 | 1 / 6 |
| expected_view_hit | measured | 0.6667 | 4 / 6 |
| expected_node_hit | measured | 0.0000 | 0 / 6 |
| expected_zone_hit | unavailable | N/A | 0 / 0 |
| expected_object_hit | measured | 0.0000 | 0 / 6 |
| expected_object_id_hit | measured | 0.0000 | 0 / 6 |
| not_found_correctness | unavailable | N/A | 0 / 0 |
| runtime_seconds mean | measured | 2.0365 | 6 records |
| checked_view_count mean | measured | 4.0000 | 6 records |
| visited_node_count mean | measured | 3.0000 | 6 records |
| context_size_chars mean | unavailable | N/A | 0 records |
| estimated_input_tokens mean | unavailable | N/A | 0 records |
| bbox_3d_iou | N/A | N/A | 0 records |
| Acc@0.1 | N/A | N/A | 0 / 0 |
| Acc@0.25 | N/A | N/A | 0 / 0 |
| Acc@0.5 | N/A | N/A | 0 / 0 |

## Measured Token Usage

Token semantics are recorded below. `provider_billing_tokens: false` means local tokenizer/model tokens, not API usage or cost.

```json
{
  "input": 74,
  "output": 0,
  "total": 74,
  "denominator": 6,
  "status": "measured",
  "tokenizers": [
    "open_clip:ViT-B-16"
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

- 3D IoU is N/A because the run does not emit predicted 3D boxes
