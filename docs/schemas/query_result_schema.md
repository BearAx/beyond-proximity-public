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
  "availability_status": "available",
  "availability_reason": null,
  "scene_id": "default",
  "query_id": "q001",
  "query": "Find the grand piano",
  "query_type": "simple_object",
  "structured_plan": {},
  "visited_nodes": [],
  "traversal_path": [],
  "selected_views": [],
  "checked_node_ids": [],
  "checked_view_ids": [],
  "checked_object_ids": [],
  "search_variant": "deterministic_lexical_v1",
  "fallback_used": true,
  "fallback_reason": "stub_mode_uses_deterministic_semantic_index_fallback",
  "result": {
    "found": true,
    "matched_object": "grand piano",
    "selected_object_id": "piano_01",
    "selected_node_id": "leaf_lobby_foyer_prefunction",
    "selected_view_id": "v006",
    "bbox_2d": null,
    "bbox_3d": null,
    "bbox_availability_status": "not_eligible",
    "bbox_unavailable_reason": "geometry_evaluation_not_eligible",
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
    "checked_node_count": 0,
    "checked_view_count": 0,
    "checked_object_count": 0,
    "context_size_chars": 0,
    "prompt_size_chars": 0,
    "estimated_input_tokens": 0,
    "estimated_token_method": "ceil(prompt_size_chars / 4)",
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

- `visited_nodes`, `traversal_path`, and `selected_views` are ordered lists of IDs.
- `checked_node_ids`, `checked_view_ids`, and `checked_object_ids` explicitly
  record the searched index entities. `checked_object_count` includes checked
  records that have no safe explicit ID, so it may exceed
  `len(checked_object_ids)`.
- `metrics_log.visited_node_count`, `checked_node_count`, and
  `checked_view_count` must match their ID traces.
- `selected_object_id` is copied only from an explicit object/instance ID on
  the matched object or its bbox; labels are never treated as object IDs.
- `search_variant`, `fallback_used`, and `fallback_reason` identify the search
  implementation and whether a fallback produced the answer.
- Missing provider token usage is `null`, never an unlabeled prompt-length
  estimate.
- Native non-provider baselines may report tokenizer-counted local model tokens
  in `token_usage` only when the tokenizer and counting method are labeled, for
  example `provider_billing_tokens=false` and `tokenizer=open_clip:ViT-H-14`.
- `runtime_seconds` is measured wall time for this query.
- `retry_count` and `failure_count` record provider/cache execution attempts for this query.
- `bbox_2d` uses normalized `[x1, y1, x2, y2]` coordinates when present.
- `bbox_3d` must identify its representation and coordinate frame through the run/scene configuration.
- A present `bbox_3d` must have three finite center values and three finite,
  strictly positive `size` or `dimensions` values.
- For a found positive object query with scene `geometry_eval_allowed=true`
  (or an explicit query-level `geometry_eval_allowed=true`),
  `bbox_availability_status` is `available` only when the bbox passes that
  quality gate. A missing, malformed, non-finite, degenerate, or depth-disabled
  box is `unavailable` and requires a non-null `bbox_unavailable_reason`.
- Negative/not-found queries use `not_applicable`; queries or scenes without
  geometry eligibility use `not_eligible`. Their null bboxes are legitimate
  and still require an explicit reason.
- `availability_status=unavailable` requires a non-null
  top-level `availability_reason`; available query answers use `null`.
- Per-query `metrics_log.construction_cost` remains `null`. View-description
  and tree-construction runtime/token cost is recorded separately once in
  `run_config.json.construction_cost`, not duplicated into each query.
- Warnings must identify deterministic fallback, unreliable depth, missing GT, or partial execution.
