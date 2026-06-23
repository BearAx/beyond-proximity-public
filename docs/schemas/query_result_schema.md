# Canonical Query Result Schema

Schema ID: `semanticsplat.query_result.v1`

Every saved Week 2 or Week 3 query result must use this shape. Legacy query-session and benchmark records are inputs for migration, not canonical results.

## Required Shape

```json
{
  "schema_version": "semanticsplat.query_result.v1",
  "run_id": "week2_stub_001",
  "method": "semantic_splat",
  "mode": "stub",
  "scene_id": "default",
  "query_id": "q001",
  "query": "Find the grand piano",
  "query_type": "simple_object",
  "structured_plan": {},
  "visited_nodes": [],
  "selected_views": [],
  "result": {
    "found": true,
    "matched_object": "grand piano",
    "selected_node_id": "leaf_lobby_foyer_prefunction",
    "selected_view_id": "v006",
    "bbox_2d": null,
    "bbox_3d": null,
    "camera_pose": null,
    "confidence": 0.0,
    "explanation": ""
  },
  "metrics_log": {
    "runtime_seconds": 0.0,
    "stage_runtime_seconds": {},
    "token_usage": null,
    "model_call_count": 0,
    "cache_hits": 0,
    "retry_count": 0,
    "failure_count": 0,
    "visited_node_count": 0,
    "checked_view_count": 0,
    "construction_cost": null
  },
  "warnings": []
}
```

## Mode Rules

- `stub`: deterministic fallback; token usage is normally `null`.
- `live`: new model calls occurred; provider/model/version belong in `run_config.json` and logs.
- `cached_live`: responses came from a documented live cache; cache provenance is required.
- Stub output may never be marked `live` or `cached_live`.

## Field Rules

- `visited_nodes` and `selected_views` are ordered lists of IDs.
- `metrics_log.visited_node_count` and `checked_view_count` must match those traces.
- Missing provider token usage is `null`, never a prompt-length estimate.
- `runtime_seconds` is measured wall time for this query.
- `retry_count` and `failure_count` record provider/cache execution attempts for this query.
- `bbox_2d` uses normalized `[x1, y1, x2, y2]` coordinates when present.
- `bbox_3d` must identify its representation and coordinate frame through the run/scene configuration.
- Warnings must identify deterministic fallback, unreliable depth, missing GT, or partial execution.
