# Five-Scene Semantic Index Workflow

Status date: 2026-06-23. Capture and semantic-index validation pass for all five scenes. All 96 ViewJSON files are annotated and all five trees are complete.

## Scene Set

| Scene ID | Templates | Template directory |
|---|---:|---|
| `ConferenceHall-capture-pilot` | 20 | `backend/data/scenes/ConferenceHall-capture-pilot/views/` |
| `Museume-capture` | 20 | `backend/data/scenes/Museume-capture/views/` |
| `Theater-capture` | 20 | `backend/data/scenes/Theater-capture/views/` |
| `outdoor-drone-capture` | 16 | `backend/data/scenes/outdoor-drone-capture/views/` |
| `outdoor-street-capture` | 20 | `backend/data/scenes/outdoor-street-capture/views/` |

## Step 1: Ensure Templates Exist

These commands are idempotent. Existing files, including partially completed annotations, are skipped unless the destructive `--overwrite` option is explicitly supplied. Do not use `--overwrite` during annotation.

```powershell
python -B scripts\create_manual_viewjson_templates.py --scene backend\data\scenes\ConferenceHall-capture-pilot --out backend\data\scenes\ConferenceHall-capture-pilot\views
python -B scripts\create_manual_viewjson_templates.py --scene backend\data\scenes\Museume-capture --out backend\data\scenes\Museume-capture\views
python -B scripts\create_manual_viewjson_templates.py --scene backend\data\scenes\Theater-capture --out backend\data\scenes\Theater-capture\views
python -B scripts\create_manual_viewjson_templates.py --scene backend\data\scenes\outdoor-drone-capture --out backend\data\scenes\outdoor-drone-capture\views
python -B scripts\create_manual_viewjson_templates.py --scene backend\data\scenes\outdoor-street-capture --out backend\data\scenes\outdoor-street-capture\views
```

## Step 2: Fill Manual Semantic Content

Follow `docs/datasets/manual_semantic_annotation_guide.md`. Inspect each referenced `images/vNNN.png` and fill:

- `summary`;
- real visible regions;
- real visible objects;
- visible landmarks, signs, or facilities;
- factual free-text notes and warnings when needed.

Keep `semantic_index_mode=manual`, every entry `source=manual`, manual `confidence=null`, and `bbox_3d=null` unless a documented real computation exists. Manual annotations are semantic-index inputs, not independent GT.

## Step 3: Build All Five Trees

Run only after every template in the corresponding scene has a factual summary.

```powershell
python -B scripts\build_scene_tree_from_viewjson.py --scene backend\data\scenes\ConferenceHall-capture-pilot --views backend\data\scenes\ConferenceHall-capture-pilot\views --out backend\data\scenes\ConferenceHall-capture-pilot\tree
python -B scripts\build_scene_tree_from_viewjson.py --scene backend\data\scenes\Museume-capture --views backend\data\scenes\Museume-capture\views --out backend\data\scenes\Museume-capture\tree
python -B scripts\build_scene_tree_from_viewjson.py --scene backend\data\scenes\Theater-capture --views backend\data\scenes\Theater-capture\views --out backend\data\scenes\Theater-capture\tree
python -B scripts\build_scene_tree_from_viewjson.py --scene backend\data\scenes\outdoor-drone-capture --views backend\data\scenes\outdoor-drone-capture\views --out backend\data\scenes\outdoor-drone-capture\tree
python -B scripts\build_scene_tree_from_viewjson.py --scene backend\data\scenes\outdoor-street-capture --views backend\data\scenes\outdoor-street-capture\views --out backend\data\scenes\outdoor-street-capture\tree
```

The builder creates only nodes supported by filled ViewJSON. It does not infer missing labels. Empty content produces a root-only tree with `complete=false`.

## Step 4: Validate Each Scene

```powershell
python -B scripts\validate_semantic_index.py --scene backend\data\scenes\ConferenceHall-capture-pilot --out docs\validation\semantic_index\ConferenceHall-capture-pilot_semantic_index.json
python -B scripts\validate_semantic_index.py --scene backend\data\scenes\Museume-capture --out docs\validation\semantic_index\Museume-capture_semantic_index.json
python -B scripts\validate_semantic_index.py --scene backend\data\scenes\Theater-capture --out docs\validation\semantic_index\Theater-capture_semantic_index.json
python -B scripts\validate_semantic_index.py --scene backend\data\scenes\outdoor-drone-capture --out docs\validation\semantic_index\outdoor-drone-capture_semantic_index.json
python -B scripts\validate_semantic_index.py --scene backend\data\scenes\outdoor-street-capture --out docs\validation\semantic_index\outdoor-street-capture_semantic_index.json
```

## Batch Validation

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

All five reports must have:

```text
invalid_view_json_count = 0
missing_view_ids = []
semantic_item_count > 0
tree_complete = true
tree_valid = true
query_runner_loadable = true
query_runner_schema_compatible = true
semantic_eval_allowed = true
geometry_eval_allowed = false
```

`geometry_eval_allowed=false` remains correct without independent GT boxes/masks and validated predicted boxes.

## Config Gate

`configs/week3_replica.yaml` points to the five capture scene IDs and maps their legacy benchmark scopes through `benchmark_scene_id`. All five `semantic_eval_allowed` flags are true and match the generated validation reports. All five `geometry_eval_allowed` flags remain false.

Do not edit reports or flags to force agreement. Rebuild and revalidate after any annotation change before changing config eligibility.

## Phase B Smoke

The following separate smoke was run after validation:

```powershell
python -B scripts\run_experiment.py --config configs\week3_phase_b_semantic_smoke.yaml --mode stub
```

It produced five available, schema-valid `stub` records with zero model calls. The benchmark records lack independent GT, so no semantic accuracy was measured. The final five-scene semantic gate using `configs/week3_replica.yaml` has not run.
