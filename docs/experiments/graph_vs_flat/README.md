# Graph vs flat — Person 1 implementation notes

Status date: 2026-06-30.

## Audit summary (Day 1)

### Legacy `default` assumptions

- `backend/query/benchmark.py` uses `backend/tree/storage.load_all_nodes()` and `TreeNode` types (`root`, `zone`, `region`, `leaf`).
- Token accounting reuses §7 prompt builders (`build_decomposition_prompt`, `build_traversal_step`, `build_leaf_confirmation_for_view`).
- The legacy benchmark is wired to `backend/data/scenes/default` ViewJSON + tree, not the five captured indexes.

### Captured five-scene format

- ViewJSON lives under `backend/data/scenes/<scene>/views/*.json` with schema `semanticsplat.captured_view_json.v1`.
- Tree nodes use schema `semanticsplat.semantic_tree_node.v1` with extra types `object` and `landmark` (not present in legacy `NodeType`).
- `load_all_nodes()` fails on captured scenes (`'object' is not a valid NodeType`) — graph-vs-flat for captured data must use `load_captured_scene_index()` dict trees instead of legacy `TreeNode` loading.

### Model client (`backend/query/model_client.py`)

- `StubModelClient.answer_query()` already performs deterministic lexical scoring over the same semantic index used in headless experiments.
- Synonym expansion exists for a small set of terms; affordance/intent expansion for sprint queries lives in `backend/query/affordance.py`.

## Same-input contract

| Field | Rule |
|---|---|
| Scenes | Five captured directories mapped from benchmark scene ids |
| Semantic items | Same ViewJSON objects/regions/landmarks for both modes |
| Query strings | Identical text from benchmark JSON |
| GT labels | Same `expected_view_ids` when Person 2 verifies `benchmark_queries_v2.json` |
| Modes | `flat_lexical`, `graph_lexical`, optional `graph_affordance` |

## Implementation

| Component | Path |
|---|---|
| Affordance map | `backend/query/affordance.py` |
| Runners + metrics | `backend/query/graph_vs_flat.py` |
| CLI | `scripts/run_graph_vs_flat.py` |
| Config | `configs/graph_vs_flat_five_scenes.yaml` |
| Tests | `tests/backend/test_affordance.py`, `tests/backend/test_graph_vs_flat.py` |

## Commands

```bash
python -B -m pytest -q tests/backend/test_affordance.py tests/backend/test_graph_vs_flat.py
python -B scripts/run_graph_vs_flat.py --config configs/graph_vs_flat_five_scenes.yaml
```

Outputs land in `outputs/graph_vs_flat/<run_id>/`:

- `metrics_summary.json`
- `metrics_summary.md`
- `metrics_summary.csv`, `per_query_summary.csv`
- `per_query_results.json`
- `run_config.json`

## Known limits

- Five-scene queries in `benchmark_queries_v1.json` have empty GT; hit@1 / hit@3 remain `N/A` until `benchmark_queries_v2.json` from Person 2.
- Captured tree is shallow/wide (root → many object/landmark nodes); graph savings come from branch pruning, not deep zone hierarchy yet.
- No live/cached-live LLM calls in this benchmark — lexical same-input efficiency only.
