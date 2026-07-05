# Graph vs flat — five-scene run

- Generated: 2026-07-05T12:43:49.725243+00:00
- Queries: 150
- GT queries with view labels: 125

## Average savings (graph lexical vs flat lexical)

- `flat_views_checked`: 19.4
- `graph_views_checked`: 4.77
- `savings_views_pct`: 75.5
- `flat_input_tokens`: 3168.2
- `graph_input_tokens`: 1014.26
- `savings_tokens_pct`: 68.2
- `flat_elapsed_ms`: 6.61
- `graph_elapsed_ms`: 6.05

## Quality (GT-aware denominator only)

- hit@1 graph: 0.68
- hit@1 flat: 0.768
- hit@3 graph: 0.808
- hit@3 flat: 0.928
- Quality metrics use only queries with verified expected_view_ids (125 of 150 queries).
