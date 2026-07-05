# Graph Scaling Stress Study

- Generated: 2026-07-05T12:43:59.265362+00:00
- Benchmark: `C:\GitProjects\beyond-proximity\docs\benchmarks\benchmark_queries_v2.json`
- Query count per multiplier: 60

| Multiplier | Avg indexed views | Flat views | Graph views | View savings | Flat tokens | Graph tokens | Token savings |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 20.0 | 20.0 | 4.3167 | 78.42% | 3240.5 | 933.3333 | 71.2% |
| 2 | 40.0 | 40.0 | 7.4333 | 81.42% | 6481.0 | 1595.6333 | 75.38% |
| 5 | 100.0 | 100.0 | 16.7833 | 83.22% | 16202.5 | 3582.5333 | 77.89% |
| 10 | 200.0 | 200.0 | 32.3667 | 83.82% | 32405.0 | 6894.0333 | 78.73% |

## Interpretation Guardrails

- This duplicates existing semantic views in memory; it measures query-time scaling behavior, not new scene accuracy.
- The current captured tree is shallow and object-heavy, so this is a conservative stress test rather than a deep hierarchy showcase.
- Public Replica/ScanNet scaling remains required for a main-conference claim.
