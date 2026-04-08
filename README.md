# SemanticSplat — 3D Gaussian Splatting Semantic Navigator

A semantic query system over 3DGS scenes: navigate the scene in a Spark.js viewer, capture views with **R**, Cursor AI builds a hierarchical semantic tree (zero external API calls), and answers natural language queries with 3D bounding box output.

## Architecture

```
Browser (React + Spark.js)
  │  WASD/QE/mouse navigation
  │  R → capture RGB + depth + camera pose
  │  POST /api/captures/save
  ▼
FastAPI Backend (pure infrastructure)
  │  Saves images, depths, transforms.json (Nerfstudio format)
  │  Exposes REST + WebSocket API
  ▼
MCP Server (fastmcp)
  │  21 infrastructure tools (file I/O, spatial graph, geometry)
  │  Returns prompt templates for Cursor AI
  ▼
Cursor AI (all intelligence)
  ├── VLM: describes each captured view (get_view_image → save_view_analysis)
  ├── LLM: groups views into zones (build_spatial_clusters → save_node)
  └── LLM: traverses tree at query time (get_children → get_views_in_node)
```

## Quick Start

### Backend

```powershell
# 1. Create the semanticsplat conda environment (Python 3.11)
conda create -n semanticsplat python=3.11 -y
conda activate semanticsplat

# 2. Install backend dependencies
pip install -r backend/requirements.txt

# 3. Start servers — use .cmd if PowerShell blocks .ps1 (see below)
start_all.cmd        # opens 3 windows: API + MCP + frontend (recommended)
# Or individually:
start_backend.cmd    # terminal 1
start_mcp.cmd        # terminal 2
start_frontend.cmd   # terminal 3
# Or: .\start_backend.ps1 and .\start_mcp.ps1
```

### PowerShell: “running scripts is disabled”

`.ps1` files are blocked when execution policy is `Restricted`. Either:

- Use **`start_backend.cmd`**, **`start_mcp.cmd`**, **`start_frontend.cmd`** (no policy change), or
- Allow scripts for your user only (one time):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Frontend

Node.js is available in the `pcg` conda environment at:
`C:\Users\m.mousatat\AppData\Local\miniconda3\envs\pcg`

```powershell
start_frontend.cmd
# Or: .\start_frontend.ps1
# Or manually:
$env:PATH = "C:\Users\m.mousatat\AppData\Local\miniconda3\envs\pcg;$env:PATH"
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

### MCP server in Cursor

Starting `start_mcp.cmd` only runs the server on your machine. **Cursor must be configured to connect to it.**

1. Start the MCP process: `start_mcp.cmd` (or `start_all.cmd`). Leave it running — you should see `http://127.0.0.1:8001/mcp` in the log.
2. This repo includes **`.cursor/mcp.json`** registering `semantic-splat` at `http://127.0.0.1:8001/mcp` (FastMCP `streamable-http`).
3. In Cursor: **Settings → MCP** (or restart Cursor after adding the file). Ensure **semantic-splat** is enabled. If you prefer a global config, add the same `url` entry under `mcpServers` in your user **`%USERPROFILE%\.cursor\mcp.json`**.

A `GET /` on port 8001 returning **404** is normal — the MCP endpoint is **`/mcp`**, not `/`.

### Run Tests

```powershell
$env:PYTHONPATH = "."
C:\Users\m.mousatat\AppData\Local\miniconda3\envs\semanticsplat\Scripts\pytest.exe tests/backend/ -v
```

## Usage Workflow

1. **Navigate** — fly through your `.ply` Gaussian Splatting scene with WASD+mouse
2. **Capture** — press **R** to save RGB + depth + camera pose for the current view
3. **Analyse** — ask Cursor AI: *"Analyse all views in scene X using MCP tools"*
4. **Build Tree** — ask Cursor AI: *"Build the semantic tree for scene X using build_spatial_clusters and save_node"*
5. **Query** — ask Cursor AI: *"Find the red sofa in scene X"*

## Project Structure

```
backend/              Python backend (FastAPI + MCP)
  config.py           Paths, ports, depth constants
  io/                 Nerfstudio I/O + ViewJSON storage
  geometry/           Spatial graph + 3D unprojection
  tree/               TreeNode + disk persistence
  schemas/types.py    Pydantic models + prompt templates
  mcp/server.py       fastmcp MCP server (21 tools)
  api/server.py       FastAPI REST + WebSocket server

frontend/             React + TypeScript + Vite
  src/components/
    Navigator/        Spark.js 3DGS viewer + FPS controls + R-capture
    TreeVisualizer/   D3.js interactive semantic tree
    QueryFlow/        Real-time traversal event stream
    ControlPanel/     Scene/PLY/query controls

tests/backend/        Pytest unit tests (29 tests, 100% pass)
```

## MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `init_scene` | Create scene directory |
| `get_unanalyzed_views` | Find views needing VLM analysis |
| `get_view_image` | Return base64 image + analysis prompt |
| `save_view_analysis` | Persist Cursor AI's VLM JSON |
| `build_spatial_clusters` | Group cameras by proximity + grouping prompt |
| `save_node` | Persist a tree node (Cursor AI creates these) |
| `get_children` | Children summaries + traversal prompt |
| `get_views_in_node` | View JSONs + leaf confirmation prompt |
| `unproject_bbox` | 2D bbox → 3D BBox3D via depth map |
| `search_summaries` | Keyword search over all nodes/views |
| … 11 more | See `backend/mcp/server.py` |
