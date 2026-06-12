# SemanticSplat — Documentation Hub

> **Latest run:** `2026-06-12_1829` · 2026-06-12 18:29 UTC · scene `default`

---

## Start here

| What you need | Open |
|---------------|------|
| **Latest full report** (metrics, charts, failure cases) | [benchmark_graph_vs_flat.md](benchmark_graph_vs_flat.md) |
| **Latest run dashboard** (one page, all links) | [project_log/runs/2026-06-12_1829/README.md](project_log/runs/2026-06-12_1829/README.md) |
| **Latest project log** (tokens, decisions, next steps) | [project_log/2026-06-12_1829_benchmark.md](project_log/2026-06-12_1829_benchmark.md) |
| **Demo video** (conference room screen failure) | [failure_case_demo.mp4](benchmark_results/failure_case_demo.mp4) |
| **All past runs** | [project_log/README.md](project_log/README.md) |

---

## Latest results

| | Graph | Flat | Advantage |
|--|------:|-----:|----------:|
| Time | 48.65 s | 197.04 s | 4.1× faster |
| Tokens | 6,430 | 26,604 | 8.5× less |
| Flat wrong-room cases | — | 2/5 | graph wins 2 |

---

## Reasoning traces (latest run)

| # | Case | Graph | Flat | |
|--:|------|-------|------|---|
| 1 | where is the screen in the conference r… | ✅ | ❌ | [trace](project_log/runs/2026-06-12_1829/reasoning/01_where_is_the_screen_in_the_c.md) |
| 2 | where is the screen in the conference r… | ✅ | ❌ | [trace](project_log/runs/2026-06-12_1829/reasoning/02_where_is_the_screen_in_the_c.md) |
| 3 | where is the projection screen in the b… | ✅ | ✅ | [trace](project_log/runs/2026-06-12_1829/reasoning/03_where_is_the_projection_scre.md) |
| 4 | find the projector in the ballroom | ✅ | ✅ | [trace](project_log/runs/2026-06-12_1829/reasoning/04_find_the_projector_in_the_ba.md) |
| 5 | where is the exit sign in the lobby | ⚠️ | ⚠️ | [trace](project_log/runs/2026-06-12_1829/reasoning/05_where_is_the_exit_sign_in_th.md) |

---

## Folder structure

```
docs/
├── README.md                    ← you are here
├── benchmark_graph_vs_flat.md   ← main report + charts
├── benchmark_results/           ← JSON, PNG, MP4
└── project_log/
    ├── README.md                ← history of all runs
    └── runs/{timestamp}/
        ├── README.md            ← run dashboard
        └── reasoning/*.md       ← step-by-step traces
```

---

## Regenerate everything

```bash
./run_all_docs.sh
```

**Полный путь запуска (RU):** [launch_guide_ru.md](launch_guide_ru.md) — что делает каждая команда, ожидаемый output, Query Flow vs benchmark.
