# Week 3 Phase B Report

Status date: 2026-06-23. Phase B complete; later phases and the final Week 3 gate were not run.

## Work Completed

- Validated all 96 manually annotated ViewJSON files across five capture scenes.
- Normalized 220 landmark `kind` fields to the schema value `landmark`; semantic labels and descriptions were preserved.
- Rebuilt five deterministic semantic trees from 1,046 annotated semantic items.
- Enabled semantic execution for all five scenes in `configs/week3_replica.yaml`; geometry remains disabled.
- Fixed metrics evaluation for captured scene IDs mapped through `benchmark_scene_id` and added regression coverage.
- Ran a separate five-query stub smoke without starting the final five-scene gate.

## Validation Result

| Scene | Valid views | Semantic items | Tree nodes | Semantic execution | Geometry evaluation |
|---|---:|---:|---:|---|---|
| `ConferenceHall-capture-pilot` | 20 | 207 | 201 | allowed | unavailable |
| `Museume-capture` | 20 | 225 | 222 | allowed | unavailable |
| `Theater-capture` | 20 | 226 | 221 | allowed | unavailable |
| `outdoor-drone-capture` | 16 | 169 | 159 | allowed | unavailable |
| `outdoor-street-capture` | 20 | 219 | 216 | allowed | unavailable |

## Reproduce

Rebuild trees after any annotation change, using the commands in `docs/datasets/five_scene_semantic_index_workflow.md`, then validate:

```powershell
python -B scripts\validate_semantic_index.py `
  --scenes `
    backend\data\scenes\ConferenceHall-capture-pilot `
    backend\data\scenes\Museume-capture `
    backend\data\scenes\Theater-capture `
    backend\data\scenes\outdoor-drone-capture `
    backend\data\scenes\outdoor-street-capture `
  --out docs\validation\semantic_index
```

Run the Phase B smoke:

```powershell
python -B scripts\run_experiment.py --config configs\week3_phase_b_semantic_smoke.yaml --mode stub
```

Run verification:

```powershell
python -B -m py_compile scripts\evaluate_results.py scripts\run_experiment.py scripts\build_scene_tree_from_viewjson.py scripts\validate_semantic_index.py
python -B -m pytest tests\backend -q --basetemp .pytest_tmp\phase_b_complete
git diff --check
```

Expected: 5/5 semantic reports pass, the smoke writes five available schema-valid stub results with zero model calls, and 71 backend tests pass.

## Limits

The manual semantic index is an input to retrieval, not independent GT. The benchmark has no verified GT for these scenes, so semantic accuracy is unavailable. Independent GT/predicted 3D boxes are missing, so geometry metrics remain `N/A`. Live/cached-live execution, the final five-scene gate, baselines, and ScanNet were not run.
