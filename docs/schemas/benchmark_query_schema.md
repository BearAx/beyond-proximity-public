# Benchmark Query Schema

Schema ID: `semanticsplat.benchmark_queries.v1`

## File Shape

```json
{
  "schema_version": "semanticsplat.benchmark_queries.v1",
  "benchmark_id": "default_semantic_index_v1",
  "status": "verified_semantic_index",
  "queries": []
}
```

## Query Record

```json
{
  "query_id": "q001",
  "scene_id": "default",
  "query": "Find the grand piano",
  "query_type": "simple_object",
  "expected_output_type": "object",
  "expected_zone_ids": ["zone_lobby_reception"],
  "expected_node_ids": ["leaf_lobby_foyer_prefunction"],
  "expected_view_ids": ["v006", "v007"],
  "expected_object_labels": ["grand piano"],
  "acceptance_rule": "found=true and selected view is v006 or v007",
  "notes": "Verified from existing ViewJSON and tree; not independent dataset GT.",
  "verification_status": "verified_from_view_json",
  "verification_source": ["backend/data/scenes/default/views/v006.json"]
}
```

## Enumerations

- `query_type`: `simple_object`, `attribute`, `relational`, `multi_hop`, `functional`, `negative`.
- `expected_output_type`: `node`, `view`, `object`, `region`, `not_found`.
- `verification_status`: `verified_dataset_gt`, `verified_manual`, `verified_from_view_json`, `ambiguous`, `missing_gt`.

## Optional 3D Ground Truth

A record may include `expected_bbox_3d` and `gt_3d_reliable=true`. The box must use the same coordinate frame as the scene manifest. Without both fields, 3D IoU is `N/A`.

## Rules

- Unknown expected IDs remain empty and the reason is written in `notes`.
- Use `notes: "GT unavailable; excluded from accuracy metrics"`, `verification_status: "missing_gt"`, and an empty `verification_source` when no GT exists.
- `missing_gt` queries are excluded from retrieval, negative, view, node, zone, object, and 3D accuracy denominators.
- ViewJSON-derived expectations test semantic-index behavior, not visual/dataset accuracy.
- Negative-query absence must state its verification scope.
- Query IDs are stable and never reused for different text.
