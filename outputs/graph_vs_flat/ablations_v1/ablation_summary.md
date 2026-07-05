# Graph Ablation Study

- Generated: 2026-07-05T12:44:01.187046+00:00
- Benchmark: `C:\GitProjects\beyond-proximity\docs\benchmarks\benchmark_queries_v2.json`
- Queries: 150
- Queries with verified view labels: 125

## Variant Summary

| Variant | Views | View savings vs flat | Tokens | Token savings vs flat | hit@1 | hit@3 |
|---|---:|---:|---:|---:|---:|---:|
| `flat_lexical` | 19.4 | 0.0% | 3168.2 | 0.0% | 0.768 | 0.928 |
| `flat_affordance` | 19.4 | 0.0% | 3168.2 | 0.0% | 0.784 | 0.944 |
| `graph_tight` | 2.0733 | 89.31% | 450.9333 | 85.77% | 0.6 | 0.72 |
| `graph_default` | 4.7667 | 75.43% | 1014.26 | 67.99% | 0.68 | 0.808 |
| `graph_broad` | 19.4 | 0.0% | 6346.8 | -100.33% | 0.728 | 0.92 |
| `graph_affordance` | 4.9933 | 74.26% | 1062.4267 | 66.47% | 0.68 | 0.816 |

## Interpretation Guardrails

- These are deterministic lexical/stub ablations, not live VLM results.
- Manual view labels are reference labels, not independent dataset ground truth.
- `graph_broad` is a recall-oriented stress setting; `graph_tight` is a cost-oriented stress setting.
