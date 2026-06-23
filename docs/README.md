# Documentation

<p align="center">
  <a href="../README.md"><b>Repository home</b></a>
  &nbsp;&middot;&nbsp;
  <a href="benchmark_graph_vs_flat.md">Benchmark report</a>
  &nbsp;&middot;&nbsp;
  <a href="launch_guide_ru.md">Launch guide (RU)</a>
</p>

---

**Latest run:** `2026-06-12_1829` · scene `default` · 19 views · 15 nodes

## Start here

| Need | Open |
|:-----|:-----|
| Full benchmark (metrics, charts, failure cases) | [benchmark_graph_vs_flat.md](benchmark_graph_vs_flat.md) |
| Headless Week 2/3 evaluation | [headless_evaluation.md](headless_evaluation.md) |
| Canonical evaluation protocol | [evaluation_protocol.md](evaluation_protocol.md) |
| Dataset validation and scene inventory | [dataset_validation_report.md](dataset_validation_report.md) |
| Baseline contracts and feasibility | [baseline_adapter_contracts.md](baseline_adapter_contracts.md) |
| Query fairness review | [query_fairness_review.md](query_fairness_review.md) |
| Reproducibility mode definitions | [repo_reproducibility_notes.md](repo_reproducibility_notes.md) |
| Week 2/3 publication timeline | [publication_timeline.md](publication_timeline.md) |
| Week 2/3 delivery verification | [week2_week3_delivery_verification.md](week2_week3_delivery_verification.md) |
| Latest run dashboard | [project_log/runs/2026-06-12_1829/README.md](project_log/runs/2026-06-12_1829/README.md) |
| Demo video | [failure_case_demo.mp4](benchmark_results/failure_case_demo.mp4) |
| Run history | [project_log/README.md](project_log/README.md) |

## Latest results

| | Graph | Flat | Advantage |
|:--|--:|--:|--:|
| Time (est.) | 48.65 s | 197.04 s | **4.1×** |
| Tokens | 6,430 | 26,604 | **8.5×** |
| Wrong-room cases | 0 | 2 | graph |

## Regenerate

```bash
./run_all_docs.sh
```

See also [launch_guide_ru.md](launch_guide_ru.md) for a full Russian walkthrough.
