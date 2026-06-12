# SemanticSplat — 3D Gaussian Splatting Semantic Navigator

Natural-language navigation over 3D Gaussian Splatting scenes. Fly through a `.ply` scene in the browser, capture views, build a **semantic tree** with Cursor AI (via MCP), and query objects with **graph-pruned search** — faster and more room-accurate than flat view-by-view search.

Repository: [github.com/Mousatat/beyond-proximity](https://github.com/Mousatat/beyond-proximity)

---

## What it does

| Layer | Role |
|-------|------|
| **Browser** (React + Spark.js) | 3D navigation, view capture (**R**), tree viz, query flow |
| **Backend** (FastAPI) | Saves images/depths, REST + WebSocket API |
| **MCP server** (FastMCP) | Infrastructure tools + prompt templates for Cursor |
| **Cursor AI** | VLM view analysis, tree building, query traversal (all reasoning) |

### Graph vs flat search

- **Graph** — decompose query → traverse semantic tree → confirm only relevant views (~4 views, ~50 s est.)
- **Flat** — check **every** view in order (~19 views, ~197 s est.)
- **Demo failure case:** *"Where is the screen in the conference room?"* — flat returns a screen in the **wrong room** (v012); graph returns the **stage screen** (v017).

Benchmark report: [`docs/benchmark_graph_vs_flat.md`](docs/benchmark_graph_vs_flat.md)

---

## Quick start — macOS / Linux

### 1. One command — run the app

```bash
chmod +x start_all.sh run_all_docs.sh
./start_all.sh
```

Opens **http://localhost:5173** automatically.

In the UI:
1. **Scene ID:** `default` → **Set**
2. **3D Scene:** choose a `.ply` (e.g. `ConferenceHall.ply`) → **Load**
3. Fly with WASD + mouse; press **R** to capture views

Services:

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://127.0.0.1:8000/api/health |
| MCP (Cursor only) | http://127.0.0.1:8001/mcp |

Put `.ply` files in `scenes/` or `scenes/input-data/`.

### 2. Python environment (first time)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..
```

### 3. MCP in Cursor

Create `.cursor/mcp.json` in the project root:

```json
{
  "mcpServers": {
    "semantic-splat": {
      "url": "http://127.0.0.1:8001/mcp"
    }
  }
}
```

Start `./start_all.sh`, then enable **semantic-splat** in Cursor → Settings → MCP.

---

## Quick start — Windows

See `start_all.cmd` / PowerShell scripts in the repo root, or the PDF guide:

`SemanticSplat_—_подробная_инструкция_по_запуску_Windows.pdf`

```powershell
conda create -n semanticsplat python=3.11 -y
conda activate semanticsplat
pip install -r backend/requirements.txt
start_all.cmd
```

---

## Benchmark & documentation (one command)

Regenerates metrics, charts, reasoning traces, demo video, and all markdown reports:

```bash
./run_all_docs.sh
```

At the end, the terminal prints **clickable `file://` links**. Start here:

| Document | Path |
|----------|------|
| **Docs hub** (main index) | [`docs/README.md`](docs/README.md) |
| Benchmark report | [`docs/benchmark_graph_vs_flat.md`](docs/benchmark_graph_vs_flat.md) |
| Latest run dashboard | `docs/project_log/runs/{timestamp}/README.md` |
| Project log | `docs/project_log/` |
| Demo video | [`docs/benchmark_results/failure_case_demo.mp4`](docs/benchmark_results/failure_case_demo.mp4) |

### What `./run_all_docs.sh` produces

```
docs/
├── README.md                      ← documentation hub
├── benchmark_graph_vs_flat.md     ← full report + embedded charts
├── benchmark_results/             ← JSON, PNG charts, MP4 video
└── project_log/
    ├── README.md                  ← run history
    ├── YYYY-MM-DD_HHMM_benchmark.md
    └── runs/{timestamp}/
        ├── README.md              ← links for this run
        └── reasoning/01–05_*.md   ← step-by-step graph vs flat reasoning
```

### Scripts

| Script | Purpose |
|--------|---------|
| `./run_all_docs.sh` | Full pipeline: benchmark + docs + video + reasoning |
| `scripts/run_full_benchmark.py` | Same (called by above) |
| `scripts/record_failure_demo.py` | Regenerate demo MP4 only |

---

## Usage workflow

1. **Navigate** — fly through the `.ply` scene (WASD + mouse)
2. **Capture** — press **R** to save RGB + depth + camera pose
3. **Analyse views** — in Cursor: *"Analyse all views in scene default using MCP tools"*
4. **Build tree** — *"Build the semantic tree for scene default"*
5. **Query** — enter query in UI (creates session) → Cursor runs §7 pipeline
6. **Inspect reasoning** — **Query Flow** tab in UI, or JSON in `backend/data/scenes/default/queries/`

### Where LLM reasoning is saved

Real query sessions (from Cursor + UI):

```
backend/data/scenes/{scene_id}/queries/{session_id}.json
```

Each step includes `reasoning` (traversal) and `explanation` (leaf checks).

Auto-generated benchmark reasoning:

```
backend/data/scenes/default/queries/auto_*_graph.json
backend/data/scenes/default/queries/auto_*_flat.json
```

---

## Project structure

```
beyond-proximity/
├── start_all.sh              ← run app (Mac/Linux)
├── run_all_docs.sh           ← benchmark + docs pipeline
├── backend/
│   ├── api/                  ← FastAPI REST + WebSocket
│   ├── mcp/                  ← MCP server + tools
│   ├── query/                ← pipeline, benchmark, reasoning logs
│   ├── tree/                 ← semantic tree nodes
│   └── data/scenes/default/  ← views, tree, query sessions
├── frontend/                 ← React + Spark.js viewer
├── docs/                     ← reports, charts, project log
├── scripts/                  ← benchmark CLI
├── scenes/                   ← .ply files (gitignored — add locally)
└── tests/backend/
```

---

## MCP tools (summary)

| Tool | Purpose |
|------|---------|
| `init_scene` | Create scene directory |
| `get_view_image` | Image + VLM prompt for Cursor |
| `save_view_analysis` | Persist ViewJSON |
| `build_spatial_clusters` | Spatial grouping prompt |
| `save_node` | Persist tree node |
| `get_children` | Traversal prompt for a node |
| `get_views_in_node` | Leaf confirmation prompt |
| `unproject_bbox` | 2D bbox → 3D via depth |

Full list: `backend/mcp/server.py`

---

## Tests

```bash
source .venv/bin/activate
export PYTHONPATH=.
pytest tests/backend/ -v
```

---

## Key results (scene `default`, 19 views)

| Metric | Graph | Flat |
|--------|------:|-----:|
| Avg time (est.) | ~48 s | ~197 s |
| Avg tokens | ~6.4k | ~26.6k |
| Views checked | ~4 | 19 |
| Wrong-room failures | 0/5 demo cases | 2/5 |

See [`docs/benchmark_graph_vs_flat.md`](docs/benchmark_graph_vs_flat.md) for per-query breakdown and scaling analysis.

---

## Related docs

- [**launch_guide_ru.md**](launch_guide_ru.md) — **полный путь запуска** (команды, output, Query Flow, benchmark)
- [`docs/repo_setup_notes.md`](docs/repo_setup_notes.md) — setup notes
- [`docs/baselines_matrix.md`](docs/baselines_matrix.md) — baseline comparison matrix
- [`docs/superpowers/specs/2026-04-05-semantic-3dgs-navigator-design.md`](docs/superpowers/specs/2026-04-05-semantic-3dgs-navigator-design.md) — design spec

---

## License

See repository license. `.ply` scene files are not included in git — add your own to `scenes/`.
