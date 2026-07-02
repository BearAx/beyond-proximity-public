# Person 1 — graph-vs-flat five-scene benchmark

## What was done

- Audited legacy `benchmark.py` vs captured semantic-index format (`docs/experiments/graph_vs_flat/README.md`).
- Implemented same-input runners: `flat_lexical`, `graph_lexical`, `graph_affordance` over five captured scenes.
- Added affordance/intent expansion (`sit`, `exit`, `reception`, `restroom`, …).
- Ran 40 five-scene queries from `benchmark_queries_v1.json`.
- Exported paper-ready tables to `outputs/graph_vs_flat/five_scene_graph_vs_flat_v1/` (JSON, MD, CSV).

## Results (efficiency only — no verified GT on five-scene v1 queries)

| Metric | Flat avg | Graph avg | Savings |
|---|---:|---:|---:|
| Views checked | 19.2 | 4.35 | 77.1% |
| Input tokens | 3104 | 854 | 72.2% |
| Runtime ms | 16.1 | 10.7 | 33.4% |

Quality hit@1/hit@3 await `benchmark_queries_v2.json` from Person 2.

## Files

- `backend/query/affordance.py`, `backend/query/graph_vs_flat.py`
- `scripts/run_graph_vs_flat.py`, `configs/graph_vs_flat_five_scenes.yaml`
- `tests/backend/test_affordance.py`, `tests/backend/test_graph_vs_flat.py`
- `docs/experiments/graph_vs_flat/README.md`
- `outputs/graph_vs_flat/five_scene_graph_vs_flat_v1/`

## Command

```bash
python -B scripts/run_graph_vs_flat.py --config configs/graph_vs_flat_five_scenes.yaml
```
