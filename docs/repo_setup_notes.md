# Repo Setup Notes

Week 1 owner: Literature / Baselines / Repo Notes Lead  
Purpose: document the current repository state, install/launch path, and reproducibility issues to clean up after the smoke test.

## Current System Summary

SemanticSplat is currently a prototype with three major pieces:

| Area | Path | Role |
|---|---|---|
| Backend API | `backend/api/` | FastAPI app for scene management, capture saving, tree/query endpoints, and WebSocket query events. |
| MCP server | `backend/mcp/` | Exposes infrastructure tools to Cursor/LLM: scene I/O, view analysis storage, spatial clustering, tree storage, bbox unprojection. |
| Frontend | `frontend/` | React/Vite/Spark.js viewer for loading 3DGS scenes, manually capturing views, visualizing trees, and showing query flow. |

The architecture is intentionally split: the backend does file I/O and geometry, while Cursor/LLM supplies the VLM/LLM reasoning. This is useful for prototyping, but it is the main Week 1 reproducibility gap because the target smoke test must run without manual viewer actions or Cursor in the loop.

## Existing Data Layout

The backend stores scenes under:

```text
backend/data/scenes/<scene_id>/
```

Current code expects a Nerfstudio-style `transforms.json` plus generated folders:

```text
backend/data/scenes/<scene_id>/
  transforms.json
  images/
    v001.png
  depths/
    v001_depth.npy
  views/
    v001.json
  tree/
    node_*.json
```

Week 1 target scene format from the role plan is:

```text
scene/
  rgb/
  depth/
  poses.json
  intrinsics.json
  metadata.json
```

These two formats need an adapter or a final decision. The quickest path is to make `scripts/prepare_replica_scene.py` convert the Week 1 `rgb/depth/poses/intrinsics` format into the backend's current `images/depths/transforms.json` format, or to update backend I/O to accept the Week 1 format directly.

## Install Notes

Backend dependencies are listed in `backend/requirements.txt`:

```bash
conda create -n semanticsplat python=3.11 -y
conda activate semanticsplat
pip install -r backend/requirements.txt
```

Frontend dependencies are listed in `frontend/package.json`:

```bash
cd frontend
npm install
npm run dev
```

Current frontend stack:

| Package | Role |
|---|---|
| React + Vite + TypeScript | App shell and development server. |
| `@sparkjsdev/spark` | 3D Gaussian Splatting viewer. |
| Three.js | Rendering/camera support. |
| D3 | Tree visualization. |
| Zustand | Client state. |
| Axios | API calls. |

## Launch Notes

Backend API:

```bash
PYTHONPATH=. python -m backend.api.server
```

Expected API address:

```text
http://127.0.0.1:8000
```

MCP server:

```bash
PYTHONPATH=. python -m backend.mcp.server
```

Expected MCP address:

```text
http://127.0.0.1:8001/mcp
```

Frontend:

```bash
cd frontend
npm run dev
```

Expected frontend address:

```text
http://localhost:5173
```

Existing helper scripts are Windows-oriented:

| Script | Notes |
|---|---|
| `start_backend.cmd` | Hardcodes a Windows Miniconda env path. |
| `start_mcp.cmd` | Hardcodes a Windows Miniconda env path. |
| `start_all.cmd` | Starts API, MCP, and frontend on Windows. |
| `start_backend.ps1`, `start_frontend.ps1` | PowerShell helpers. |

For macOS/Linux reproducibility, add shell scripts or document the direct commands above.

## API Surface

Current FastAPI routes:

| Prefix | Purpose |
|---|---|
| `/api/health` | Health check and list served `.ply` files. |
| `/api/scenes` | List/init scenes through backend scene tools. |
| `/api/captures/save` | Save browser-captured RGB, depth, pose, and update `transforms.json`. |
| `/api/tree` | Tree visualization and node access. |
| `/api/query` | Query prompts, unprojection, bbox refinement, keyword demo, WebSocket stream. |
| `/api/query-log` | Query logging. |
| `/scenes` | Static serving for root-level `.ply`/splat files in `scenes/`. |

Notable implementation detail: `/api/query` mostly builds prompts and geometry outputs. It does not itself call an LLM/VLM to complete decomposition, traversal, or leaf confirmation.

## MCP Tool Surface

The MCP server is named `semantic-splat` and exposes infrastructure tools.

| Tool Group | Tools |
|---|---|
| Scene | `list_scenes`, `get_scene_info`, `init_scene` |
| View | `get_unanalyzed_views`, `get_view_image`, `save_view_analysis`, `get_view_full_json`, `list_view_summaries`, `get_view_camera_pose` |
| Tree | `build_spatial_clusters`, `save_node`, `get_node`, `get_root_node`, `get_children`, `get_query_decomposition`, `get_leaf_confirmation_view`, `get_views_in_node`, `get_tree_for_viz`, `search_summaries` |
| Bbox refinement | `get_bbox_refinement`, `finalize_refined_bbox`, `rank_leaf_results` |
| Geometry | `unproject_bbox`, `merge_bboxes`, `get_capture_intrinsics`, `compute_inter_node_distances` |

The MCP tools deliberately return prompts/instructions for Cursor/LLM. For the Week 1 headless pipeline, Telman will need either:

| Option | Description |
|---|---|
| Headless runner in `scripts/run_experiment.py` | Canonical config-driven runner; `scripts/run_pipeline.py` is a compatibility alias. |
| Local stub mode for smoke test | Script uses deterministic view descriptions on a pilot scene to prove end-to-end I/O before model integration. |
| MCP client orchestration | Script talks to MCP tools, but still needs a model client outside Cursor. |

## Current Manual Workflow

The README describes the prototype workflow:

1. Open frontend viewer.
2. Navigate manually with WASD/mouse.
3. Press `R` to capture RGB, depth, and camera pose.
4. Ask Cursor AI to analyze views through MCP.
5. Ask Cursor AI to build the tree through MCP.
6. Ask Cursor AI to answer a query through tree traversal.

This does not satisfy the Week 1 smoke-test criterion because it requires manual camera movement, keypress capture, and Cursor-mediated reasoning.

## Current Test Notes

There are backend tests under `tests/backend/`, including:

| Test File | Coverage |
|---|---|
| `test_nerfstudio.py` | Read/write of `transforms.json`, frame camera pose helpers. |
| `test_unprojector.py` | 2D bbox to 3D unprojection logic. |

Recommended command:

```bash
PYTHONPATH=. pytest tests/backend/ -v
```

The README mentions 29 passing backend tests, but this should be re-run on the current machine before reporting.

## Cleanup Items

| Priority | Item | Why |
|---:|---|---|
| P0 | Add a headless pipeline entry point | Complete for deterministic stub mode through `scripts/run_experiment.py`; live provider execution remains blocked. |
| P0 | Decide final scene format adapter | Dataset Lead and Pipeline Lead need one contract. |
| P0 | Remove Cursor/manual viewer dependency from smoke path | The Week 1 criterion explicitly forbids human-in-the-loop. |
| P1 | Add cross-platform launch docs/scripts | Existing helper scripts are Windows-specific. |
| P1 | Separate prompt templates from MCP-only flow | Headless script needs the same prompts without Cursor. |
| P1 | Add output manifest under `outputs/<run_id>/` | Needed for reproducibility and status report. |
| P2 | Normalize terminology: `images/depths/transforms` vs `rgb/depth/poses/intrinsics` | Reduces confusion between dataset and backend formats. |
| P2 | Add small fixture scene for CI | Lets tests cover the full pipeline without large datasets. |

## Suggested Week 1 Smoke Output

The launch command should be:

```bash
python scripts/run_pipeline.py --config configs/week2_replica.yaml
```

Expected files:

```text
outputs/week1_smoke_test/
  views.json
  tree.json
  query_result.json
  logs.json
```

Recommended additional files if easy:

```text
outputs/week1_smoke_test/
  run_config.json
  scene_manifest.json
  errors.json
```

These extra files will make the run easier to debug and cite in `docs/week1_status.md`.
