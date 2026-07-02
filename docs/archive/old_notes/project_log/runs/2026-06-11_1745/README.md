# Run `2026-06-11_1745`

**Scene:** `default` · **Queries:** 12 efficiency · 5 failure cases

## Navigation

| | Link |
|--|------|
| 🏠 Docs hub | [../../README.md](../../../../../README.md) |
| 📊 Benchmark report | [benchmark_graph_vs_flat.md](../../../../../benchmarks/benchmark_graph_vs_flat.md) |
| 📝 Project log | [2026-06-11_1745_benchmark.md](../../2026-06-11_1745_benchmark.md) |
| 🎬 Demo video | [benchmark_results/failure_case_demo.mp4](../../../../../benchmark_results/failure_case_demo.mp4) |
| 📦 Raw JSON | [benchmark_results/benchmark_default.json](../../../../../benchmark_results/benchmark_default.json) |

## Results summary

| Metric | Graph | Flat |
|--------|------:|-----:|
| Time (est.) | 48.44 s | 197.04 s |
| Tokens | 6,430 | 26,604 |
| Flat wrong-room | — | **2/5** |

## Reasoning traces

Click a case to see step-by-step graph vs flat reasoning:

| # | Query | Graph | Flat | Trace |
|--:|-------|-------|------|-------|
| 1 | where is the screen in the conference room | ✅ `correct_room` | ❌ `wrong_room` | [open](reasoning/01_where_is_the_screen_in_the_c.md) |
| 2 | where is the screen in the conference roo… | ✅ `correct_room` | ❌ `wrong_room` | [open](reasoning/02_where_is_the_screen_in_the_c.md) |
| 3 | where is the projection screen in the bal… | ✅ `correct_room` | ✅ `correct_room` | [open](reasoning/03_where_is_the_projection_scre.md) |
| 4 | find the projector in the ballroom | ✅ `correct_room` | ✅ `correct_room` | [open](reasoning/04_find_the_projector_in_the_ba.md) |
| 5 | where is the exit sign in the lobby | ⚠️ `miss` | ⚠️ `miss` | [open](reasoning/05_where_is_the_exit_sign_in_th.md) |

## Charts

| Chart | |
|-------|---|
| Tokens | [tokens_comparison.png](../../../../../benchmark_results/tokens_comparison.png) |
| Time | [time_seconds.png](../../../../../benchmark_results/time_seconds.png) |
| Failure cases | [failure_room_accuracy.png](../../../../../benchmark_results/failure_room_accuracy.png) |
| Scaling | [scaling_curve.png](../../../../../benchmark_results/scaling_curve.png) |
