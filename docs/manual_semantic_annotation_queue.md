# Manual Semantic Annotation Queue

Status date: 2026-06-23. Revised Week 3 Phase B is blocked on real image-based annotation.

## Exact Files To Fill

| Scene | ViewJSON files | Referenced images | Count |
|---|---|---|---:|
| `ConferenceHall-capture-pilot` | `backend/data/scenes/ConferenceHall-capture-pilot/views/v001.json` through `v020.json` | `backend/data/scenes/ConferenceHall-capture-pilot/images/v001.png` through `v020.png` | 20 |
| `Museume-capture` | `backend/data/scenes/Museume-capture/views/v001.json` through `v020.json` | `backend/data/scenes/Museume-capture/images/v001.png` through `v020.png` | 20 |
| `Theater-capture` | `backend/data/scenes/Theater-capture/views/v001.json` through `v020.json` | `backend/data/scenes/Theater-capture/images/v001.png` through `v020.png` | 20 |
| `outdoor-drone-capture` | `backend/data/scenes/outdoor-drone-capture/views/v001.json` through `v016.json` | `backend/data/scenes/outdoor-drone-capture/images/v001.png` through `v016.png` | 16 |
| `outdoor-street-capture` | `backend/data/scenes/outdoor-street-capture/views/v001.json` through `v020.json` | `backend/data/scenes/outdoor-street-capture/images/v001.png` through `v020.png` | 20 |

Total: 96 ViewJSON files. All currently have an empty `summary`, empty semantic arrays, and a template warning.

## Required Content Per File

Open the referenced PNG and fill only visible evidence:

- `summary`: short factual description; must not remain empty.
- `visible_regions`: real visible regions, each with `label`, `approx_location`, and `source: manual`.
- `visible_objects`: real visible objects with `source: manual`.
- `landmarks`: visible landmarks, signs, or facilities with `source: manual`.
- `free_text_notes`: optional factual context or uncertainty.
- `warnings`: remove the template warning only after genuine annotation; retain real limitations.

Keep manual `confidence` as `null`. Keep `bbox_2d` and `bbox_3d` as `null` unless they were deliberately measured/computed from the real target. Manual annotations are semantic-index inputs, not independent GT.

## List Every Pending File

```powershell
$scenes = @(
  "ConferenceHall-capture-pilot",
  "Museume-capture",
  "Theater-capture",
  "outdoor-drone-capture",
  "outdoor-street-capture"
)

foreach ($scene in $scenes) {
  Get-ChildItem "backend\data\scenes\$scene\views\*.json" | Sort-Object Name
}
```

## After Annotation

Run the build and validation commands in `docs/five_scene_semantic_index_workflow.md`. Minimum revised Week 3 acceptance requires at least 3/5 reports with:

```text
semantic_item_count > 0
tree_complete = true
tree_valid = true
query_runner_loadable = true
query_runner_schema_compatible = true
semantic_eval_allowed = true
```

Do not enable config flags manually before the corresponding report passes.
