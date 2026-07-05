# Graph Vs Flat Benchmark V2

Status date: 2026-07-01.

This is a same-input deterministic benchmark over `benchmark_queries_v2.json`. Both methods use the same captured-scene semantic entries and the same manual reference GT.

## Scope

- Mode: deterministic local lexical retrieval, no live model calls.
- Graph: select tree-native manual zones, then scan entries under those zones.
- Flat: scan every semantic entry in the scene.
- GT: manual semantic-index reference labels, not independent dataset GT.

## Efficiency Summary

| Metric | Graph mean | Flat mean | Graph improvement |
|---|---:|---:|---:|
| latency_ms | 0.2492 | 0.2976 | 1.5865x speedup |
| semantic_entries_scanned | 154.2267 | 206.6 | 25.32% fewer |
| context_size_chars | 33682.24 | 45084.3133 | 25.29% smaller |
| estimated_input_tokens | 8420.5467 | 11271.1 | 25.26% fewer |
| views_checked | 14.96 | 19.4 | 22.89% fewer |

## Quality Summary

| Metric | Graph | Flat |
|---|---:|---:|
| retrieval_success | 143/150 = 0.9533 | 143/150 = 0.9533 |
| expected_view_hit | 78/125 = 0.624 | 78/125 = 0.624 |
| expected_node_hit | 62/125 = 0.496 | 62/125 = 0.496 |
| expected_zone_hit | 105/125 = 0.84 | 105/125 = 0.84 |
| expected_object_hit | 73/125 = 0.584 | 73/125 = 0.584 |
| not_found_correctness | 22/25 = 0.88 | 22/25 = 0.88 |

## Evidence

```text
outputs/week3/graph_vs_flat_benchmark_v2/graph_vs_flat_metrics.json
outputs/week3/graph_vs_flat_benchmark_v2/per_query_results.json
docs/experiments/graph_vs_flat/graph_vs_flat_benchmark_v2.md
```

## Limitations

- This proves deterministic same-input graph pruning efficiency, not live provider speed.
- Token counts are estimated from serialized context size.
- Manual labels are reference GT, not independent dataset GT.
