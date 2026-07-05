# Person 1 — graph-vs-flat five-scene benchmark

## What was done

- Audited legacy `benchmark.py` vs captured semantic-index format (`docs/experiments/graph_vs_flat/README.md`).
- Implemented same-input runners: `flat_lexical`, `graph_lexical`, `graph_affordance` over five captured scenes.
- Added affordance/intent expansion (`sit`, `exit`, `reception`, `restroom`, …).
- Ran 40 five-scene queries from `benchmark_queries_v1.json` (efficiency baseline).
- Integrated Person 2 `benchmark_queries_v2.json` (150 queries, 125 with verified view GT).
- Added ranked top-k views for hit@1 / hit@3 with GT-aware denominators.
- Exported paper-ready tables to `outputs/graph_vs_flat/` (JSON, MD, CSV).

## Results v1 (40 queries, efficiency only)

| Metric | Flat avg | Graph avg | Savings |
|---|---:|---:|---:|
| Views checked | 19.2 | 4.35 | 77.1% |
| Input tokens | 3104 | 854 | 72.2% |
| Runtime ms | 16.1 | 10.7 | 33.4% |

## Results v2 (150 queries, Person 2 GT)

| Metric | Flat avg | Graph avg | Savings |
|---|---:|---:|---:|
| Views checked | 19.2 | 5.39 | 71.4% |
| Input tokens | 3104 | 1062 | 65.1% |
| Runtime ms | 14.1 | 12.5 | 11.7% |

### Quality (125 queries with `expected_view_ids`)

| Metric | Graph | Flat |
|---|---:|---:|
| hit@1 | 0.792 | 0.768 |
| hit@3 | 0.904 | 0.928 |

25 queries excluded from quality denominator (verified labels but no matching view GT, e.g. negatives).

## Files

- `backend/query/affordance.py`, `backend/query/graph_vs_flat.py`
- `scripts/run_graph_vs_flat.py`
- `configs/graph_vs_flat_five_scenes.yaml`, `configs/graph_vs_flat_v2.yaml`
- `tests/backend/test_affordance.py`, `tests/backend/test_graph_vs_flat.py`
- `docs/experiments/graph_vs_flat/README.md`
- `outputs/graph_vs_flat/five_scene_graph_vs_flat_v1/`, `five_scene_graph_vs_flat_v2/`

## Commands

```bash
# v1 efficiency baseline (40 queries)
python -B scripts/run_graph_vs_flat.py --config configs/graph_vs_flat_five_scenes.yaml

# v2 with Person 2 GT (150 queries, hit@1/hit@3)
python -B scripts/run_graph_vs_flat.py --config configs/graph_vs_flat_v2.yaml

python -B -m pytest -q tests/backend/test_affordance.py tests/backend/test_graph_vs_flat.py
```
