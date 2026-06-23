# Semantic Index Creation Plan

Status date: 2026-06-22. This documents supported repository behavior; it does not create ViewJSON or tree files.

## Current Answer

| Question | Answer |
|---|---|
| Can ViewJSON be generated from captured RGB? | Yes, semi-automatically. `get_view_image` returns each real captured PNG and the canonical analysis prompt; a vision-capable agent must inspect it and submit structured analysis. |
| Does it require MCP/agent? | The supported generation path requires the `semantic-splat` MCP server plus a vision-capable calling agent. MCP handles I/O, schemas, clustering, and persistence; the agent supplies visual/semantic reasoning. |
| Does it require live provider credentials? | Not inside this repository for the existing IDE-agent/MCP flow. The MCP server makes no model calls and reads no provider key. The calling agent must already have vision access. An autonomous headless VLM generator is not implemented and would require a configured provider/model/credentials. |
| Can existing ViewJSON/tree files be imported? | Yes if they are real, use the exact captured frame IDs, and conform to current `ViewJSON` and `TreeNode` schemas. There is no dedicated importer; use MCP save tools for validation, or copy a complete known-compatible index and run validation. |
| Is this automatic? | No. View iteration and file persistence are tool-assisted; image interpretation, grouping decisions, and node construction are agent-driven. |

## Implemented Path

Relevant code:

| Function | Location | Role |
|---|---|---|
| `get_unanalyzed_views` | `backend/mcp/tools/view_tools.py` | Lists captured frame IDs without ViewJSON. |
| `get_view_image` | `backend/mcp/tools/view_tools.py` | Returns the real PNG, MIME type, and canonical prompt. |
| `save_view_analysis` | `backend/mcp/tools/view_tools.py` | Validates with `ViewJSON` and writes `views/<view_id>.json`. |
| `build_spatial_clusters` | `backend/mcp/tools/tree_tools.py` | Combines poses and saved summaries into geometry/semantic cluster candidates. |
| `save_node` | `backend/mcp/tools/tree_tools.py` | Validates a `TreeNode`, computes spatial stats, writes a node, and updates the manifest. |
| `ViewJSON` schema/prompt | `backend/schemas/types.py` | Canonical semantic record and analysis instructions. |
| tree storage | `backend/tree/storage.py` | Writes `tree/node_<node_id>.json` and `tree/manifest.json`. |

The MCP tools are infrastructure only. They do not silently convert a missing result into `found=false`, do not call an external model, and do not provide semantic GT.

## Start MCP

From repository root in a separate terminal:

```powershell
$env:PYTHONPATH = "."
python -m backend.mcp.server
```

The endpoint is `http://127.0.0.1:8001/mcp`. Connect it in an MCP-capable IDE/agent client; the repository has no checked-in client-specific MCP configuration.

## Exact Agent Step

After RGB-D capture validation passes, give the connected vision-capable agent this instruction with the exact Scene ID:

```text
Using only the semantic-splat MCP tools and the actual captured images, analyze every
unanalyzed view in scene <scene_id> and build its semantic tree. First call
get_unanalyzed_views. For every returned view ID, call get_view_image, inspect the
image, produce schema-conforming ViewJSON without inventing hidden objects, and call
save_view_analysis. Then call build_spatial_clusters. Create leaf/region/zone nodes
that cover every captured view and a single root node using save_node. Preserve exact
view IDs. Do not create GT labels, boxes, masks, or negative findings from missing data.
```

Expected tool sequence:

```text
get_unanalyzed_views(scene_id)
for each view_id:
  get_view_image(scene_id, view_id)
  agent inspects returned real image
  save_view_analysis(scene_id, view_id, view_json_dict)
build_spatial_clusters(scene_id, geometry_assisted=true)
save_node(scene_id, leaf/region nodes)
save_node(scene_id, zone nodes)
save_node(scene_id, root node)
```

Save child nodes before the root and set explicit `parent_id`, `children_ids`, and `view_ids`. Every captured view must have one valid ViewJSON and be covered by the tree. Semantic index records are predictions/derived annotations, not independent GT.

## Expected Output

```text
backend/data/scenes/<scene_id>/
  views/
    v001.json
    v002.json
    ...
  tree/
    manifest.json
    node_<leaf_id>.json
    node_<zone_id>.json
    node_<root_id>.json
```

`manifest.json` must contain a valid `root_id` and all saved `node_ids`. Filenames and embedded IDs must agree with captured frame IDs and node IDs.

## Existing Index Import

Preferred import is through MCP so current schemas validate each record:

1. Read each genuine source ViewJSON and call `save_view_analysis(scene_id, view_id, view_json_dict)`.
2. Read each genuine source node and call `save_node(scene_id, node_dict)`, children first and root last.
3. Run the validation commands below.

For a previously validated index from this exact repository schema, direct copying is supported by the readers but does not validate during copy:

```powershell
Copy-Item -Recurse <source_scene>\views backend\data\scenes\<scene_id>\views
Copy-Item -Recurse <source_scene>\tree backend\data\scenes\<scene_id>\tree
```

Do not reuse `default` ViewJSON/tree for a different PLY or different camera frames. Matching filenames alone are not evidence that annotations belong to the scene.

## Completeness Validation

Single scene:

```powershell
python -B scripts\check_capture_pilot.py `
  --scene backend\data\scenes\<scene_id> `
  --output docs\dataset_validation\<scene_id>_capture_check.json
```

The checker validates every ViewJSON against the current Pydantic schema, validates manifest/node structure, checks dangling children, and requires tree coverage of all captured frame IDs. A complete index reports:

```text
semantic_index.invalid_view_json_count = 0
semantic_index.missing_view_ids = []
semantic_index.tree_valid = true
semantic_index.tree_covers_all_views = true
semantic_index.complete = true
```

Then verify API readability while API is running:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/tree/<scene_id>/viz
```

`semantic_index.complete=true` proves only index completeness. Final semantic accuracy still requires independent query/room/object GT. `geometry_eval_allowed` remains false without independent 3D GT boxes/masks and valid predictions.

## Blockers

- No autonomous/headless RGB-to-ViewJSON command exists.
- No repository-local MCP client configuration is checked in.
- Four capture target folders do not exist yet; only ConferenceHall has valid frames.
- No independent semantic GT exists for these five PLY assets.
- No independent 3D boxes/masks exist.
- ScanNet remains postponed.
