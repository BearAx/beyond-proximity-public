# Manual Semantic Annotation Queue

Status date: 2026-06-23. Queue complete; retained as an audit record.

## Completion

| Scene | ViewJSON files | Annotated | Semantic items | Validation |
|---|---:|---:|---:|---|
| `ConferenceHall-capture-pilot` | 20 | 20 | 207 | passed |
| `Museume-capture` | 20 | 20 | 225 | passed |
| `Theater-capture` | 20 | 20 | 226 | passed |
| `outdoor-drone-capture` | 16 | 16 | 169 | passed |
| `outdoor-street-capture` | 20 | 20 | 219 | passed |

All 96 files have a non-empty image-based summary and semantic entries. The trees were rebuilt and all five reports now have:

```text
semantic_item_count > 0
tree_complete = true
tree_valid = true
query_runner_loadable = true
query_runner_schema_compatible = true
semantic_eval_allowed = true
geometry_eval_allowed = false
```

## Annotation Provenance

The records remain `semantic_index_mode: manual`, with semantic entries marked `source: manual`. Manual annotations are semantic-index inputs, not independent GT. Null boxes and confidences remain null unless deliberately measured; none should be inferred from text.

Landmark `kind` values were mechanically normalized to the schema value `landmark` after annotation. Labels, descriptions, regions, objects, and notes were not inferred or rewritten by that normalization.

## Revalidation

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

Do not rerun template generation with `--overwrite`; that would replace completed annotations.
