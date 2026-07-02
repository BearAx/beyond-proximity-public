# Graph vs flat — five-scene run

- Generated: 2026-07-02T15:09:39.290403+00:00
- Queries: 150
- GT queries with view labels: 125

## Average savings (graph lexical vs flat lexical)

- `flat_views_checked`: 19.2
- `graph_views_checked`: 5.39
- `savings_views_pct`: 71.4
- `flat_input_tokens`: 3104.0
- `graph_input_tokens`: 1061.6
- `savings_tokens_pct`: 65.1
- `flat_elapsed_ms`: 14.11
- `graph_elapsed_ms`: 12.46

## Quality (GT-aware denominator only)

- hit@1 graph: 0.792
- hit@1 flat: 0.768
- hit@3 graph: 0.904
- hit@3 flat: 0.928
- Quality metrics use only queries with verified expected_view_ids (125 of 150 queries).
