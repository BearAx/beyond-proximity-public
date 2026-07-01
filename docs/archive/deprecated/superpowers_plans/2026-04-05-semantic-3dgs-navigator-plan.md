# SemanticSplat Implementation Plan (v2 — Spark.js + Cursor AI)

> **HISTORICAL ARTIFACT WARNING:** This plan was used for the initial implementation. It contains outdated schemas and prompt structures (e.g. missing `facing` and `visible_landmarks` fields in ViewJSON, missing the two-pass semantic merge, and missing the bounding-box refinement loop). **DO NOT** use the schemas or prompts in this file as a reference. The canonical source of truth for the current system architecture, prompts, and data structures is the Design Document: `docs/project/design/specs/2026-04-05-semantic-3dgs-navigator-design.md`.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete semantic query system over 3DGS scenes — the user navigates the scene in a professional Spark.js viewer, presses "R" to capture views, the system builds a hierarchical semantic tree entirely through Cursor AI (no external API), and answers natural language queries with 3D bounding box output.

**Architecture:** The backend is pure infrastructure (file I/O, spatial graph, depth unprojection) and exposes only MCP tools. The Cursor AI agent drives all intelligence: it calls MCP tools to get images, analyzes them with its own vision, groups views into a tree, and traverses the tree at query time. No external LLM API keys are required. The Spark.js frontend handles scene rendering and manual view capture; camera data is saved in Nerfstudio JSON format.

**Tech Stack:** Python 3.11 (Anaconda conda env `semanticsplat`), FastAPI, numpy, scipy, Pillow; React 18, TypeScript, Vite, `@sparkjsdev/spark` ([github.com/sparkjsdev/spark](https://github.com/sparkjsdev/spark)), Three.js, D3.js, Tailwind CSS, Zustand; MCP via fastmcp (tools are pure infrastructure — intelligence supplied by Cursor AI).

---

## Key Architecture Decisions vs. Previous Plan

| Aspect | Previous Plan | This Plan |
|---|---|---|
| 3DGS rendering | Python gsplat | **Spark.js** (`@sparkjsdev/spark`) in browser |
| View selection | NoField (automatic) | **Manual navigator** — user flies through scene, presses R |
| RGB capture | Python render | **WebGL canvas** `.toDataURL()` in browser |
| Depth capture | gsplat depth channel | **WebGL depth render target** → linearized metres |
| Camera format | custom JSON | **Nerfstudio `transforms.json`** |
| LLM calls | OpenAI API from Python | **Cursor AI only** — MCP tools are pure infrastructure |
| VLM image analysis | `AsyncOpenAI` client | Cursor AI vision via MCP tool `get_view_image` |
| Tree grouping decision | Python LLM call | Cursor AI reads summaries and calls `save_node` |
| Query traversal | Python async traversal | Cursor AI calls `traversal_step` tool step by step |

---

## Project File Structure

```
semantic-gaussian-splatting/
├── backend/
│   ├── io/
│   │   ├── __init__.py
│   │   ├── nerfstudio.py        # Read/write Nerfstudio transforms.json
│   │   └── view_store.py        # Save/load ViewJSON files per scene
│   ├── geometry/
│   │   ├── __init__.py
│   │   ├── spatial_graph.py     # Camera proximity graph + connected components
│   │   └── unprojector.py       # bbox_2d + depth_map → 3D bbox
│   ├── tree/
│   │   ├── __init__.py
│   │   ├── nodes.py             # TreeNode dataclass + NodeType enum
│   │   └── storage.py           # Persist/load tree nodes to/from JSON
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── types.py             # Pydantic: ViewJSON, ObjectEntry, QueryPlan, BBox3D, etc.
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── server.py            # fastmcp server entry point
│   │   └── tools/
│   │       ├── __init__.py
│   │       ├── scene_tools.py   # list_scenes, get_scene_info, init_scene
│   │       ├── view_tools.py    # save_captured_view, get_view_image, save_view_analysis
│   │       │                    # list_view_summaries, get_view_full_json
│   │       ├── tree_tools.py    # save_node, get_node, get_children, get_root,
│   │       │                    # get_subtree_summaries, get_tree_for_viz,
│   │       │                    # search_summaries, build_spatial_clusters
│   │       └── query_tools.py   # decompose_query_schema, traversal_step,
│   │                            # confirm_match_schema, unproject_bbox,
│   │                            # merge_bboxes, synthesize_canonical_pose
│   ├── api/
│   │   ├── __init__.py
│   │   ├── server.py            # FastAPI app
│   │   └── routes/
│   │       ├── scenes.py        # POST /scenes/init, GET /scenes/{id}
│   │       ├── captures.py      # POST /captures/save (from browser R-press)
│   │       ├── tree.py          # GET /tree/{scene_id}/viz, /node/{id}
│   │       └── query.py         # POST /query/{scene_id}, WS /query/{id}/stream
│   ├── data/
│   │   └── scenes/
│   │       └── {scene_id}/
│   │           ├── transforms.json      # Nerfstudio format
│   │           ├── images/              # v001.png, v002.png ...
│   │           ├── depths/              # v001_depth.npy ...
│   │           ├── views/               # v001.json (VLM analysis)
│   │           └── tree/                # manifest.json, node_*.json
│   ├── config.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navigator/
│   │   │   │   ├── Navigator.tsx          # Main Spark.js + FPS navigator
│   │   │   │   ├── useSparkScene.ts       # Spark.js load + animation loop hook
│   │   │   │   ├── useFPSControls.ts      # WASD+QE+Shift+Mouse controls
│   │   │   │   ├── useViewCapture.ts      # R key: RGB + depth capture + POST to API
│   │   │   │   ├── DepthCapture.ts        # WebGL depth render target + linearize
│   │   │   │   ├── HUD.tsx                # Crosshair, position, capture flash
│   │   │   │   └── CapturedViewList.tsx   # Sidebar: thumbnails of captured views
│   │   │   ├── TreeVisualizer/
│   │   │   │   ├── TreeVisualizer.tsx
│   │   │   │   └── useTreeLayout.ts
│   │   │   ├── QueryFlow/
│   │   │   │   ├── QueryFlow.tsx
│   │   │   │   └── useQueryStream.ts
│   │   │   └── ControlPanel/
│   │   │       └── ControlPanel.tsx
│   │   ├── store/
│   │   │   ├── sceneStore.ts
│   │   │   ├── treeStore.ts
│   │   │   └── queryStore.ts
│   │   ├── api/
│   │   │   └── client.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── package.json
└── tests/
    ├── backend/
    │   ├── test_nerfstudio.py
    │   ├── test_spatial_graph.py
    │   └── test_unprojector.py
    └── fixtures/
        ├── sample_transforms.json
        └── sample_view.json
```

---

## Task 1: Project Scaffold and Configuration

**Files:**
- Create: `backend/config.py`
- Create: `backend/requirements.txt`
- Create: `frontend/package.json` (via npm)
- Create: `frontend/vite.config.ts`

- [ ] **Step 1: Create backend config**

```python
# backend/config.py
from pathlib import Path

BASE_DIR  = Path(__file__).parent
DATA_DIR  = BASE_DIR / "data" / "scenes"

# Spatial graph
SPATIAL_SCALE_FACTOR = 3.5   # × median nearest-neighbour distance

# MCP
MCP_HOST = "127.0.0.1"
MCP_PORT = 8001

# API
API_HOST = "127.0.0.1"
API_PORT = 8000

# Depth capture
DEPTH_NEAR = 0.1    # metres, must match THREE.js camera near
DEPTH_FAR  = 100.0  # metres, must match THREE.js camera far
```

- [ ] **Step 2: Create requirements.txt**

```
# backend/requirements.txt
fastapi==0.115.0
uvicorn[standard]==0.30.6
pydantic==2.7.1
numpy==1.26.4
scipy==1.13.0
Pillow==10.3.0
fastmcp==0.1.0
python-multipart==0.0.9
websockets==12.0
pytest==8.2.0
pytest-asyncio==0.23.6
```

Note: **no openai, no gsplat, no plyfile** — all rendering happens in the browser via Spark.js.

- [ ] **Step 3: Create Conda environment and install backend dependencies**

```bash
# Create a dedicated conda environment (Python 3.11)
conda create -n semanticsplat python=3.11 -y
conda activate semanticsplat

# Install backend dependencies
cd backend
pip install -r requirements.txt
```

> **Note**: All subsequent terminal commands that run backend code assume the `semanticsplat` conda environment is active. Run `conda activate semanticsplat` at the start of every new terminal session before starting the backend or MCP server.

- [ ] **Step 4: Scaffold frontend**

```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install
npm install three @types/three @sparkjsdev/spark
npm install d3 @types/d3 zustand axios tailwindcss @tailwindcss/vite
npx tailwindcss init
```

- [ ] **Step 5: Configure vite.config.ts**

```ts
// frontend/vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/ws':  { target: 'ws://127.0.0.1:8000',  ws: true }
    }
  },
  optimizeDeps: {
    exclude: ['@sparkjsdev/spark']  // Spark uses dynamic imports internally
  }
})
```

- [ ] **Step 6: Create data directory**

```bash
mkdir -p backend/data/scenes
mkdir -p tests/fixtures
```

- [ ] **Step 7: Verify conda environment is active, then commit scaffold**

```bash
# Confirm you are in the right environment before committing
conda activate semanticsplat
python --version   # should print Python 3.11.x

git init
git add .
git commit -m "feat: project scaffold — conda env semanticsplat, backend config, requirements (no external LLM API), spark.js frontend"
```

---

## Task 2: Nerfstudio JSON Format Handler

**Files:**
- Create: `backend/io/nerfstudio.py`
- Create: `tests/backend/test_nerfstudio.py`
- Create: `tests/fixtures/sample_transforms.json`

Nerfstudio `transforms.json` format stores camera intrinsics globally and per-frame 4×4 camera-to-world matrices in OpenGL convention.

- [ ] **Step 1: Write failing test**

```python
# tests/backend/test_nerfstudio.py
import json, pytest
from pathlib import Path
from backend.io.nerfstudio import NerfstudioScene, FrameEntry, save_transforms, load_transforms

def test_frame_entry_has_required_fields():
    f = FrameEntry(
        file_path="images/v001.png",
        depth_file_path="depths/v001_depth.npy",
        transform_matrix=[
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 3],
            [0, 0, 0, 1],
        ],
        view_id="v001"
    )
    assert f.view_id == "v001"
    assert len(f.transform_matrix) == 4

def test_save_and_load_roundtrip(tmp_path):
    scene = NerfstudioScene(
        fl_x=800.0, fl_y=800.0, cx=640.0, cy=360.0, w=1280, h=720
    )
    scene.frames.append(FrameEntry(
        file_path="images/v001.png",
        depth_file_path="depths/v001_depth.npy",
        transform_matrix=[[1,0,0,0],[0,1,0,0],[0,0,1,3],[0,0,0,1]],
        view_id="v001"
    ))
    out = tmp_path / "transforms.json"
    save_transforms(scene, str(out))

    loaded = load_transforms(str(out))
    assert loaded.fl_x == 800.0
    assert len(loaded.frames) == 1
    assert loaded.frames[0].view_id == "v001"

def test_get_frame_by_view_id(tmp_path):
    scene = NerfstudioScene(fl_x=800, fl_y=800, cx=640, cy=360, w=1280, h=720)
    scene.frames.append(FrameEntry(
        file_path="images/v001.png",
        transform_matrix=[[1,0,0,0],[0,1,0,0],[0,0,1,3],[0,0,0,1]],
        view_id="v001"
    ))
    frame = scene.get_frame("v001")
    assert frame is not None
    assert frame.file_path == "images/v001.png"
```

- [ ] **Step 2: Run to verify it fails**

```bash
pytest tests/backend/test_nerfstudio.py -v
```

Expected: `ImportError: cannot import name 'NerfstudioScene'`

- [ ] **Step 3: Implement nerfstudio.py**

```python
# backend/io/nerfstudio.py
"""
Nerfstudio transforms.json format handler.

Format reference:
  https://docs.nerf.studio/quickstart/custom_dataset.html

The transform_matrix is a 4×4 camera-to-world matrix in OpenGL convention
(right-handed, Y-up, Z-back from camera):

  [right.x   up.x   -fwd.x   pos.x]
  [right.y   up.y   -fwd.y   pos.y]
  [right.z   up.z   -fwd.z   pos.z]
  [0         0       0        1   ]

THREE.js camera.matrixWorld gives the camera-to-world transform directly.
Convert from THREE.js column-major elements to row-major on the frontend.
"""
import json
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class FrameEntry:
    file_path:        str                    # relative: "images/v001.png"
    transform_matrix: List[List[float]]      # 4×4 row-major camera-to-world
    view_id:          str = ""
    depth_file_path:  Optional[str] = None  # relative: "depths/v001_depth.npy"

    def camera_position(self) -> List[float]:
        """Extract [x, y, z] world position from the transform matrix."""
        m = self.transform_matrix
        return [m[0][3], m[1][3], m[2][3]]

    def rotation_matrix_3x3(self) -> List[List[float]]:
        """Extract the 3×3 rotation block (world-to-camera = transpose of upper-left)."""
        m = self.transform_matrix
        return [[m[r][c] for c in range(3)] for r in range(3)]

    def to_dict(self) -> dict:
        d = {
            "file_path":        self.file_path,
            "transform_matrix": self.transform_matrix,
        }
        if self.depth_file_path:
            d["depth_file_path"] = self.depth_file_path
        if self.view_id:
            d["view_id"] = self.view_id
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "FrameEntry":
        return cls(
            file_path=d["file_path"],
            transform_matrix=d["transform_matrix"],
            view_id=d.get("view_id", ""),
            depth_file_path=d.get("depth_file_path"),
        )


@dataclass
class NerfstudioScene:
    fl_x: float              # focal length x (pixels)
    fl_y: float              # focal length y (pixels)
    cx:   float              # principal point x
    cy:   float              # principal point y
    w:    int                # image width
    h:    int                # image height
    camera_model: str = "OPENCV"
    frames: List[FrameEntry] = field(default_factory=list)

    def add_frame(self, frame: FrameEntry):
        # Replace if view_id already exists
        for i, f in enumerate(self.frames):
            if f.view_id == frame.view_id and frame.view_id:
                self.frames[i] = frame
                return
        self.frames.append(frame)

    def get_frame(self, view_id: str) -> Optional[FrameEntry]:
        return next((f for f in self.frames if f.view_id == view_id), None)

    def to_dict(self) -> dict:
        return {
            "camera_model": self.camera_model,
            "fl_x": self.fl_x,
            "fl_y": self.fl_y,
            "cx":   self.cx,
            "cy":   self.cy,
            "w":    self.w,
            "h":    self.h,
            "frames": [f.to_dict() for f in self.frames],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "NerfstudioScene":
        scene = cls(
            fl_x=d["fl_x"], fl_y=d["fl_y"],
            cx=d["cx"],     cy=d["cy"],
            w=d["w"],       h=d["h"],
            camera_model=d.get("camera_model", "OPENCV"),
        )
        scene.frames = [FrameEntry.from_dict(f) for f in d.get("frames", [])]
        return scene


def save_transforms(scene: NerfstudioScene, path: str):
    import json
    from pathlib import Path
    Path(path).write_text(json.dumps(scene.to_dict(), indent=2))


def load_transforms(path: str) -> NerfstudioScene:
    import json
    from pathlib import Path
    return NerfstudioScene.from_dict(json.loads(Path(path).read_text()))


def get_or_create_transforms(scene_dir: str, w: int = 1280, h: int = 720,
                              fl_x: float = 800.0, fl_y: float = 800.0,
                              cx: float = 640.0,   cy: float = 360.0) -> NerfstudioScene:
    """Load existing transforms.json or create a new one."""
    from pathlib import Path
    path = Path(scene_dir) / "transforms.json"
    if path.exists():
        return load_transforms(str(path))
    return NerfstudioScene(fl_x=fl_x, fl_y=fl_y, cx=cx, cy=cy, w=w, h=h)
```

- [ ] **Step 4: Run test**

```bash
pytest tests/backend/test_nerfstudio.py -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/io/nerfstudio.py tests/backend/test_nerfstudio.py
git commit -m "feat: Nerfstudio transforms.json reader/writer with FrameEntry + NerfstudioScene"
```

---

## Task 3: VLM Schemas and View Store

**Files:**
- Create: `backend/schemas/types.py`
- Create: `backend/io/view_store.py`

- [ ] **Step 1: Create schemas**

```python
# backend/schemas/types.py
"""
All Pydantic data models.
These types flow:
  Browser → API (CapturePayload)
  Cursor AI → MCP → disk (ViewJSON, TreeNode variants)
  MCP → Cursor AI (summaries, images, tree data)
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any


class ObjectAttributes(BaseModel):
    color:     Optional[str] = None
    material:  Optional[str] = None
    size:      Optional[Literal["small", "medium", "large"]] = None
    condition: Optional[str] = None


class ObjectEntry(BaseModel):
    label:                  str
    bbox_2d:                List[int]   # [x1, y1, x2, y2] pixel coords
    confidence:             Literal["high", "medium", "low"] = "medium"
    attributes:             ObjectAttributes = Field(default_factory=ObjectAttributes)
    functional_description: Optional[str] = None


class ViewJSON(BaseModel):
    """Analysis of a single captured view, produced by Cursor AI vision."""
    view_id:            str
    one_line_summary:   str
    space_type:         str
    object_list:        List[str]
    objects:            List[ObjectEntry]
    spatial_relations:  List[str] = Field(default_factory=list)
    notable_features:   Optional[str] = None
    visibility_quality: Literal["clear", "partial", "obstructed"] = "clear"
    # Set by the system from nerfstudio transforms.json
    camera_position:    Optional[List[float]] = None
    camera_rotation:    Optional[List[List[float]]] = None


class CapturePayload(BaseModel):
    """Sent by browser on 'R' keypress."""
    scene_id:         str
    view_id:          str                  # e.g. "v001"
    transform_matrix: List[List[float]]    # 4×4 camera-to-world, row-major
    fl_x: float = 800.0
    fl_y: float = 800.0
    cx:   float = 640.0
    cy:   float = 360.0
    w:    int   = 1280
    h:    int   = 720
    rgb_b64:   str  # base64 PNG
    depth_b64: str  # base64 float32 array (width*height floats, little-endian)


class BBox3D(BaseModel):
    center:     List[float]
    dimensions: List[float]
    bbox_min:   List[float]
    bbox_max:   List[float]


class QueryPlan(BaseModel):
    """Produced by Cursor AI from a natural language query."""
    original_query:        str
    target:                str
    location_constraints:  Optional[str] = None
    attribute_constraints: Dict[str, Any] = Field(default_factory=dict)
    relational_constraints: List[str] = Field(default_factory=list)
    functional_constraints: Optional[str] = None
    query_type: Literal[
        "object_finding", "descriptive", "aggregation",
        "cross_zone_geometric", "spatial_relation", "comparative"
    ]
    output_type: Literal["3d_bbox", "camera_pose", "text_answer", "count"]


class QueryResult(BaseModel):
    query:          str
    found:          bool
    view_id:        Optional[str] = None
    matched_object: Optional[str] = None
    confidence:     Optional[Literal["high", "medium", "low"]] = None
    bbox_2d:        Optional[List[int]] = None
    bbox_3d:        Optional[BBox3D] = None
    traversal_path: List[str] = Field(default_factory=list)
    text_answer:    Optional[str] = None


# ── Prompt strings for Cursor AI ────────────────────────────────────────────
# These are NOT used by Python code — they are returned by MCP tools so that
# Cursor AI knows exactly what to analyze and what format to produce.

VIEW_ANALYSIS_PROMPT = """You are analyzing a rendered view from a 3D Gaussian Splatting scene.
Describe everything you see in complete, structured detail.

Return ONLY a valid JSON object — no markdown, no extra keys:

{{
  "one_line_summary": "<15-word max: most salient objects and space type>",
  "space_type": "<type of space: kitchen / museum gallery / corridor / etc>",
  "object_list": ["<every visible object, one string each>"],
  "objects": [
    {{
      "label": "<specific object name>",
      "bbox_2d": [x1, y1, x2, y2],
      "confidence": "high|medium|low",
      "attributes": {{"color": "...", "material": "...", "size": "small|medium|large", "condition": "..."}},
      "functional_description": "<what this is used for>"
    }}
  ],
  "spatial_relations": ["<subject> is <relation> <object>"],
  "notable_features": "<anything unusual or prominent>",
  "visibility_quality": "clear|partial|obstructed"
}}

Image dimensions: width={width}, height={height}.
Include every visible object. Do not invent objects. Confidence "low" if uncertain."""

TREE_GROUPING_PROMPT = """You are organizing {n} visual observations into a semantic hierarchy.

View summaries:
{summaries}

Decide:
1. Should these views be organized into distinct sub-groups? YES or NO.
   YES if views span different locations, subjects, or semantic contexts.
   NO if all views are about the same thing at the same level of detail.

2. If YES: create the groups.
   - Name each group based on what you observe (no predefined categories).
   - Assign EVERY view to exactly one group.
   - A group can have 1 to many views.

Return ONLY valid JSON:
{{
  "split": true | false,
  "reason": "<one sentence>",
  "groups": [{{"name": "<name>", "summary": "<one sentence>", "view_ids": ["v001", ...]}}]
}}"""

TRAVERSAL_STEP_PROMPT = """You are navigating a semantic scene hierarchy to answer: "{query}"

Current node: "{node_name}" — {node_summary}
Children:
{children_list}

Which children MIGHT contain the answer?
- Include if it could possibly contain the answer (be conservative).
- Exclude ONLY if clearly irrelevant.
- If none are relevant, return empty list.

Return ONLY valid JSON:
{{"descend_into": ["node_id_A", ...], "reasoning": "<one sentence>"}}"""

LEAF_CONFIRMATION_PROMPT = """Query: "{query}"

Full view description:
{view_json}

Does this view contain the queried object? Return ONLY valid JSON:
{{"found": true|false, "bbox_2d": [x1,y1,x2,y2] or null, "confidence": "high|medium|low", "matched_object": "<label or null>"}}"""
```

- [ ] **Step 2: Create view store**

```python
# backend/io/view_store.py
"""Simple file-based store for per-view VLM analysis JSONs."""
import json
from pathlib import Path
from typing import List, Optional
from backend.schemas.types import ViewJSON


class ViewStore:
    def __init__(self, scene_dir: str):
        self.views_dir = Path(scene_dir) / "views"
        self.views_dir.mkdir(parents=True, exist_ok=True)

    def save(self, view: ViewJSON):
        path = self.views_dir / f"{view.view_id}.json"
        path.write_text(view.model_dump_json(indent=2))

    def load(self, view_id: str) -> Optional[ViewJSON]:
        path = self.views_dir / f"{view_id}.json"
        if not path.exists():
            return None
        return ViewJSON.model_validate_json(path.read_text())

    def exists(self, view_id: str) -> bool:
        return (self.views_dir / f"{view_id}.json").exists()

    def all_view_ids(self) -> List[str]:
        return sorted(p.stem for p in self.views_dir.glob("*.json"))

    def all_summaries(self) -> List[dict]:
        """Return compact summary for all analyzed views (used by Cursor AI for tree building)."""
        result = []
        for vid in self.all_view_ids():
            v = self.load(vid)
            if v:
                result.append({
                    "view_id": v.view_id,
                    "one_line_summary": v.one_line_summary,
                    "space_type": v.space_type,
                    "camera_position": v.camera_position,
                })
        return result
```

- [ ] **Step 3: Commit**

```bash
git add backend/schemas/ backend/io/view_store.py
git commit -m "feat: Pydantic schemas (ViewJSON, CapturePayload, QueryPlan) + ViewStore + all prompt strings"
```

---

## Task 4: Spatial Graph and 3D Unprojector

**Files:**
- Create: `backend/geometry/spatial_graph.py`
- Create: `backend/geometry/unprojector.py`
- Create: `tests/backend/test_spatial_graph.py`
- Create: `tests/backend/test_unprojector.py`

- [ ] **Step 1: Write spatial graph test**

```python
# tests/backend/test_spatial_graph.py
import pytest
from backend.geometry.spatial_graph import SpatialGraph

def test_nearby_cameras_same_component():
    positions = {"v1": [0,0,0], "v2": [0.5,0,0]}
    g = SpatialGraph(positions)
    comps = g.connected_components()
    assert len(comps) == 1
    assert set(comps[0]) == {"v1", "v2"}

def test_far_cameras_different_components():
    positions = {"v1": [0,0,0], "v2": [100,0,0]}
    g = SpatialGraph(positions)
    comps = g.connected_components()
    assert len(comps) == 2

def test_adaptive_threshold():
    positions = {"v1": [0,0,0], "v2": [1,0,0], "v3": [50,0,0]}
    g = SpatialGraph(positions)
    comps = g.connected_components()
    flat = [set(c) for c in comps]
    assert {"v3"} in flat
```

- [ ] **Step 2: Implement spatial graph**

```python
# backend/geometry/spatial_graph.py
from typing import Dict, List, Set
import numpy as np
from scipy.spatial.distance import cdist
from backend.config import SPATIAL_SCALE_FACTOR


class SpatialGraph:
    def __init__(self, positions: Dict[str, List[float]], scale_factor: float = SPATIAL_SCALE_FACTOR):
        self.view_ids  = list(positions.keys())
        self._positions = np.array([positions[v] for v in self.view_ids])
        self.scale_factor = scale_factor
        self.threshold    = self._compute_threshold()
        self._adj         = self._build_adj()

    def _compute_threshold(self) -> float:
        if len(self._positions) < 2:
            return float("inf")
        D = cdist(self._positions, self._positions)
        np.fill_diagonal(D, np.inf)
        return float(np.median(D.min(axis=1))) * self.scale_factor

    def _build_adj(self) -> Dict[str, Set[str]]:
        adj: Dict[str, Set[str]] = {v: set() for v in self.view_ids}
        D = cdist(self._positions, self._positions)
        K = len(self.view_ids)
        for i in range(K):
            for j in range(i + 1, K):
                if D[i, j] < self.threshold:
                    adj[self.view_ids[i]].add(self.view_ids[j])
                    adj[self.view_ids[j]].add(self.view_ids[i])
        return adj

    def connected_components(self) -> List[List[str]]:
        visited: Set[str] = set()
        components: List[List[str]] = []
        for vid in self.view_ids:
            if vid not in visited:
                comp: List[str] = []
                stack = [vid]
                while stack:
                    node = stack.pop()
                    if node in visited:
                        continue
                    visited.add(node)
                    comp.append(node)
                    stack.extend(self._adj[node] - visited)
                components.append(comp)
        return components

    def cluster_centroids(self) -> Dict[int, List[float]]:
        comps = self.connected_components()
        by_id = {v: pos.tolist() for v, pos in zip(self.view_ids, self._positions)}
        return {
            i: np.mean([by_id[v] for v in comp], axis=0).tolist()
            for i, comp in enumerate(comps)
        }
```

- [ ] **Step 3: Write unprojector test**

```python
# tests/backend/test_unprojector.py
import numpy as np
import pytest
from backend.geometry.unprojector import unproject_bbox_to_3d

# Identity camera (looking down -Z) at origin, f=500
INTRINSICS = {"fx": 500.0, "fy": 500.0, "cx": 320.0, "cy": 240.0}
# transform_matrix = identity (camera at origin, aligned with world)
TRANSFORM = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

def test_flat_depth_gives_correct_z():
    depth = np.full((480, 640), 5.0, dtype=np.float32)
    result = unproject_bbox_to_3d([270, 190, 370, 290], depth, TRANSFORM, INTRINSICS)
    assert result is not None
    assert abs(result["center"][2] - 5.0) < 0.2

def test_zero_depth_returns_none():
    depth = np.zeros((480, 640), dtype=np.float32)
    result = unproject_bbox_to_3d([100, 100, 200, 200], depth, TRANSFORM, INTRINSICS)
    assert result is None
```

- [ ] **Step 4: Implement unprojector**

```python
# backend/geometry/unprojector.py
"""
Converts a 2D bounding box + depth map to a 3D bounding box in world coordinates.
The depth map is in metres (linear), produced by the browser WebGL depth capture.
The transform_matrix is the 4×4 camera-to-world matrix from Nerfstudio format.
"""
from typing import Dict, List, Optional
import numpy as np


def unproject_bbox_to_3d(
    bbox_2d:      List[int],
    depth_map:    np.ndarray,          # (H, W) float32, metres; 0 = no surface
    transform_matrix: List[List[float]],  # 4×4 camera-to-world (Nerfstudio)
    intrinsics:   Dict[str, float],    # {"fx":..., "fy":..., "cx":..., "cy":...}
    subsample:    int   = 4,
    max_depth:    float = 50.0,
) -> Optional[dict]:
    """
    Returns {"center", "dimensions", "bbox_min", "bbox_max"} in world coords,
    or None if insufficient valid depth pixels.
    """
    x1, y1, x2, y2 = bbox_2d
    fx = intrinsics["fx"]; fy = intrinsics["fy"]
    cx = intrinsics["cx"]; cy = intrinsics["cy"]

    # Extract camera-to-world rotation (3×3) and translation
    M = np.array(transform_matrix, dtype=np.float64)
    R_c2w = M[:3, :3]   # columns are camera axes in world frame
    t_c2w = M[:3,  3]   # camera position in world

    points_world: List[np.ndarray] = []
    for y in range(y1, y2, subsample):
        for x in range(x1, x2, subsample):
            if y >= depth_map.shape[0] or x >= depth_map.shape[1]:
                continue
            d = float(depth_map[y, x])
            if d <= 0.0 or d > max_depth:
                continue
            # Ray in camera space
            X_cam = (x - cx) * d / fx
            Y_cam = (y - cy) * d / fy
            Z_cam = d
            p_cam = np.array([X_cam, Y_cam, Z_cam])
            # Camera-to-world: p_world = R_c2w @ p_cam + t_c2w
            p_world = R_c2w @ p_cam + t_c2w
            points_world.append(p_world)

    if len(points_world) < 4:
        return None

    pts = np.stack(points_world)
    bbox_min   = pts.min(axis=0)
    bbox_max   = pts.max(axis=0)
    center     = (bbox_min + bbox_max) / 2.0
    dimensions = bbox_max - bbox_min

    return {
        "center":     center.tolist(),
        "dimensions": dimensions.tolist(),
        "bbox_min":   bbox_min.tolist(),
        "bbox_max":   bbox_max.tolist(),
    }


def merge_3d_bboxes(bboxes: List[dict], iou_threshold: float = 0.5) -> List[dict]:
    """Merge overlapping 3D bboxes — used for aggregation query deduplication."""
    if not bboxes:
        return []
    merged = [dict(bboxes[0])]
    for bbox in bboxes[1:]:
        absorbed = False
        for existing in merged:
            if _iou_3d(existing, bbox) > iou_threshold:
                new_min = np.minimum(existing["bbox_min"], bbox["bbox_min"]).tolist()
                new_max = np.maximum(existing["bbox_max"], bbox["bbox_max"]).tolist()
                ctr = ((np.array(new_min) + np.array(new_max)) / 2).tolist()
                dim = (np.array(new_max) - np.array(new_min)).tolist()
                existing.update({"bbox_min": new_min, "bbox_max": new_max, "center": ctr, "dimensions": dim})
                absorbed = True
                break
        if not absorbed:
            merged.append(dict(bbox))
    return merged


def _iou_3d(a: dict, b: dict) -> float:
    inter_min = np.maximum(a["bbox_min"], b["bbox_min"])
    inter_max = np.minimum(a["bbox_max"], b["bbox_max"])
    inter = np.maximum(0, inter_max - inter_min).prod()
    vol_a = np.prod(np.array(a["dimensions"]))
    vol_b = np.prod(np.array(b["dimensions"]))
    union = vol_a + vol_b - inter
    return float(inter / union) if union > 0 else 0.0
```

- [ ] **Step 5: Run all tests**

```bash
pytest tests/backend/ -v
```

Expected: all PASS

- [ ] **Step 6: Commit**

```bash
git add backend/geometry/ tests/backend/test_spatial_graph.py tests/backend/test_unprojector.py
git commit -m "feat: spatial proximity graph + 3D depth unprojector (no external dependencies)"
```

---

## Task 5: Tree Node Storage

**Files:**
- Create: `backend/tree/nodes.py`
- Create: `backend/tree/storage.py`

- [ ] **Step 1: Implement tree nodes**

```python
# backend/tree/nodes.py
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
import numpy as np


class NodeType(str, Enum):
    INTERNAL = "internal"
    CLUSTER  = "cluster"
    LEAF     = "leaf"


@dataclass
class TreeNode:
    node_id:          str
    node_type:        NodeType
    name:             str
    summary:          str
    depth:            int                   = 0
    parent_id:        Optional[str]         = None
    children_ids:     List[str]             = field(default_factory=list)
    view_ids:         List[str]             = field(default_factory=list)
    camera_positions: List[List[float]]     = field(default_factory=list)
    spatial_centroid: Optional[List[float]] = None
    spatial_radius:   Optional[float]       = None
    spatial_bbox_min: Optional[List[float]] = None
    spatial_bbox_max: Optional[List[float]] = None

    def compute_spatial_stats(self):
        if not self.camera_positions:
            return
        pts = np.array(self.camera_positions)
        self.spatial_centroid = pts.mean(axis=0).tolist()
        self.spatial_radius   = float(np.linalg.norm(pts - pts.mean(axis=0), axis=1).max())
        self.spatial_bbox_min = pts.min(axis=0).tolist()
        self.spatial_bbox_max = pts.max(axis=0).tolist()

    def to_dict(self) -> dict:
        return {
            "node_id":          self.node_id,
            "node_type":        self.node_type.value,
            "name":             self.name,
            "summary":          self.summary,
            "depth":            self.depth,
            "parent_id":        self.parent_id,
            "children_ids":     self.children_ids,
            "view_ids":         self.view_ids,
            "camera_positions": self.camera_positions,
            "spatial_centroid": self.spatial_centroid,
            "spatial_radius":   self.spatial_radius,
            "spatial_bbox_min": self.spatial_bbox_min,
            "spatial_bbox_max": self.spatial_bbox_max,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "TreeNode":
        d = dict(d)
        d["node_type"] = NodeType(d["node_type"])
        return cls(**d)
```

```python
# backend/tree/storage.py
import json
from pathlib import Path
from typing import Dict, Optional, Tuple
from backend.tree.nodes import TreeNode


class TreeStorage:
    def __init__(self, scene_dir: str):
        self.tree_dir = Path(scene_dir) / "tree"
        self.tree_dir.mkdir(parents=True, exist_ok=True)

    def save_node(self, node: TreeNode):
        (self.tree_dir / f"{node.node_id}.json").write_text(
            json.dumps(node.to_dict(), indent=2)
        )
        # Update manifest
        manifest = self._load_manifest()
        manifest["node_ids"] = list(set(manifest.get("node_ids", []) + [node.node_id]))
        if node.parent_id is None:
            manifest["root_id"] = node.node_id
        self._save_manifest(manifest)

    def get_node(self, node_id: str) -> Optional[TreeNode]:
        path = self.tree_dir / f"{node_id}.json"
        if not path.exists():
            return None
        return TreeNode.from_dict(json.loads(path.read_text()))

    def node_exists(self, node_id: str) -> bool:
        return (self.tree_dir / f"{node_id}.json").exists()

    def all_nodes(self) -> Dict[str, TreeNode]:
        manifest = self._load_manifest()
        nodes = {}
        for nid in manifest.get("node_ids", []):
            n = self.get_node(nid)
            if n:
                nodes[nid] = n
        return nodes

    def get_root(self) -> Optional[TreeNode]:
        manifest = self._load_manifest()
        root_id = manifest.get("root_id")
        return self.get_node(root_id) if root_id else None

    def _load_manifest(self) -> dict:
        path = self.tree_dir / "manifest.json"
        return json.loads(path.read_text()) if path.exists() else {}

    def _save_manifest(self, manifest: dict):
        (self.tree_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))

    def to_d3_tree(self) -> Optional[dict]:
        """Return full tree in D3.js hierarchical nested format."""
        root = self.get_root()
        if not root:
            return None
        all_nodes = self.all_nodes()

        def recurse(node: TreeNode) -> dict:
            d = {
                "id":      node.node_id,
                "name":    node.name,
                "summary": node.summary,
                "node_type": node.node_type.value,
                "depth":   node.depth,
                "num_views": len(node.view_ids),
                "spatial_centroid": node.spatial_centroid,
            }
            if node.children_ids:
                d["children"] = [
                    recurse(all_nodes[cid])
                    for cid in node.children_ids
                    if cid in all_nodes
                ]
            return d

        return recurse(root)
```

- [ ] **Step 2: Commit**

```bash
git add backend/tree/
git commit -m "feat: TreeNode + TreeStorage with D3 serialization and manifest tracking"
```

---

## Task 6: MCP Server — Infrastructure Tools (No LLM Calls)

**Files:**
- Create: `backend/mcp/server.py`
- Create: `backend/mcp/tools/scene_tools.py`
- Create: `backend/mcp/tools/view_tools.py`
- Create: `backend/mcp/tools/tree_tools.py`
- Create: `backend/mcp/tools/query_tools.py`

**Critical principle**: Every MCP tool here is **pure infrastructure**. None of them call any LLM or external API. Cursor AI supplies all intelligence by calling these tools, reading the results, and calling other tools with the result of its reasoning.

- [ ] **Step 1: MCP server entry point**

```python
# backend/mcp/server.py
from fastmcp import FastMCP

mcp = FastMCP(
    name="SemanticSplat",
    description=(
        "Infrastructure tools for 3DGS semantic scene understanding. "
        "All intelligence is supplied by the calling AI agent (Cursor). "
        "No LLM API keys required."
    )
)

import backend.mcp.tools.scene_tools  # noqa: F401
import backend.mcp.tools.view_tools   # noqa: F401
import backend.mcp.tools.tree_tools   # noqa: F401
import backend.mcp.tools.query_tools  # noqa: F401

if __name__ == "__main__":
    from backend.config import MCP_HOST, MCP_PORT
    mcp.run(host=MCP_HOST, port=MCP_PORT)
```

- [ ] **Step 2: Scene tools**

```python
# backend/mcp/tools/scene_tools.py
"""
Scene lifecycle tools.
Cursor AI calls these to initialize and inspect scenes.
"""
import json
from pathlib import Path
from backend.mcp.server import mcp
from backend.config import DATA_DIR
from backend.io.nerfstudio import get_or_create_transforms, save_transforms


@mcp.tool()
def init_scene(scene_id: str, ply_filename: str = "scene.ply") -> dict:
    """
    Initialize a new scene directory structure.
    The PLY file must already be placed at data/scenes/{scene_id}/{ply_filename}.

    Returns:
        Scene metadata with directory paths ready for use.
    """
    scene_dir = DATA_DIR / scene_id
    for sub in ["images", "depths", "views", "tree"]:
        (scene_dir / sub).mkdir(parents=True, exist_ok=True)

    ply_path = scene_dir / ply_filename
    transforms = get_or_create_transforms(str(scene_dir))
    save_transforms(transforms, str(scene_dir / "transforms.json"))

    return {
        "scene_id":    scene_id,
        "scene_dir":   str(scene_dir),
        "ply_exists":  ply_path.exists(),
        "images_dir":  str(scene_dir / "images"),
        "depths_dir":  str(scene_dir / "depths"),
        "views_dir":   str(scene_dir / "views"),
        "tree_dir":    str(scene_dir / "tree"),
    }


@mcp.tool()
def get_scene_info(scene_id: str) -> dict:
    """
    Get current status of a scene: how many views captured, analyzed, tree built?

    Returns:
        Scene status dict.
    """
    scene_dir = DATA_DIR / scene_id
    if not scene_dir.exists():
        return {"error": f"Scene '{scene_id}' not found. Run init_scene first."}

    transforms_path = scene_dir / "transforms.json"
    num_captured = 0
    if transforms_path.exists():
        data = json.loads(transforms_path.read_text())
        num_captured = len(data.get("frames", []))

    views_dir = scene_dir / "views"
    num_analyzed = len(list(views_dir.glob("*.json"))) if views_dir.exists() else 0

    tree_manifest = scene_dir / "tree" / "manifest.json"
    tree_built = tree_manifest.exists() and bool(
        json.loads(tree_manifest.read_text()).get("root_id")
    ) if tree_manifest.exists() else False

    return {
        "scene_id":      scene_id,
        "num_captured":  num_captured,
        "num_analyzed":  num_analyzed,
        "tree_built":    tree_built,
        "status": (
            "complete"     if tree_built else
            "analyzing"    if num_analyzed > 0 else
            "capturing"    if num_captured > 0 else
            "initialized"
        )
    }


@mcp.tool()
def list_scenes() -> dict:
    """List all scenes in the data directory with their status."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    scenes = []
    for d in DATA_DIR.iterdir():
        if d.is_dir():
            scenes.append(get_scene_info(d.name))
    return {"scenes": scenes}
```

- [ ] **Step 3: View tools — the bridge between browser captures and Cursor AI vision**

```python
# backend/mcp/tools/view_tools.py
"""
View management tools.

Workflow for Cursor AI to analyze views:
  1. Call get_view_image(scene_id, view_id)
     → returns base64 PNG that Cursor AI can see with its vision
  2. Cursor AI describes what it sees (using VIEW_ANALYSIS_PROMPT)
  3. Call save_view_analysis(scene_id, view_id, analysis_json)
     → saves the analysis to disk
  4. Repeat for all views via: get_unanalyzed_views → analyze each → save
"""
import json
import base64
from pathlib import Path
from typing import Any, Dict, List
from backend.mcp.server import mcp
from backend.config import DATA_DIR
from backend.schemas.types import ViewJSON, VIEW_ANALYSIS_PROMPT
from backend.io.view_store import ViewStore
from backend.io.nerfstudio import load_transforms


@mcp.tool()
def get_unanalyzed_views(scene_id: str) -> dict:
    """
    Return the list of captured view IDs that have NOT yet been analyzed.
    Use this to know which views Cursor AI still needs to describe.

    Returns:
        {"to_analyze": ["v001", "v002", ...], "already_done": ["v003", ...]}
    """
    scene_dir = DATA_DIR / scene_id
    transforms_path = scene_dir / "transforms.json"
    if not transforms_path.exists():
        return {"error": "No transforms.json found. Capture some views first."}

    data = json.loads(transforms_path.read_text())
    captured = {f["view_id"] for f in data.get("frames", []) if f.get("view_id")}

    store = ViewStore(str(scene_dir))
    analyzed = set(store.all_view_ids())

    return {
        "to_analyze":   sorted(captured - analyzed),
        "already_done": sorted(captured & analyzed),
        "total_captured": len(captured),
    }


@mcp.tool()
def get_view_image(scene_id: str, view_id: str) -> dict:
    """
    Return the captured RGB image for a view as a base64-encoded PNG string.
    Cursor AI uses this to visually analyze the view with its vision capability.

    Also returns the analysis prompt that Cursor AI should use.

    Returns:
        {
          "view_id": str,
          "image_b64": str,       ← base64 PNG — Cursor AI can see this
          "image_path": str,      ← absolute path for reference
          "analysis_prompt": str, ← exact prompt Cursor AI should use
          "width": int,
          "height": int
        }
    """
    scene_dir = DATA_DIR / scene_id
    img_path  = scene_dir / "images" / f"{view_id}.png"

    if not img_path.exists():
        return {"error": f"Image not found: {img_path}"}

    img_bytes = img_path.read_bytes()
    img_b64   = base64.b64encode(img_bytes).decode()

    # Get dimensions from transforms.json
    w, h = 1280, 720
    tf_path = scene_dir / "transforms.json"
    if tf_path.exists():
        data = json.loads(tf_path.read_text())
        w = data.get("w", 1280)
        h = data.get("h", 720)

    return {
        "view_id":        view_id,
        "image_b64":      img_b64,
        "image_path":     str(img_path),
        "analysis_prompt": VIEW_ANALYSIS_PROMPT.format(width=w, height=h),
        "width":          w,
        "height":         h,
    }


@mcp.tool()
def save_view_analysis(scene_id: str, view_id: str, analysis: Dict[str, Any]) -> dict:
    """
    Save the VLM analysis that Cursor AI produced for a view.
    Call this after Cursor AI has described the image returned by get_view_image.

    Args:
        scene_id: Scene identifier.
        view_id:  View identifier (e.g. "v001").
        analysis: The structured JSON dict Cursor AI produced (matching ViewJSON schema).

    Returns:
        {"saved": true, "view_id": str}
    """
    scene_dir = DATA_DIR / scene_id
    store     = ViewStore(str(scene_dir))

    # Inject camera pose from transforms.json
    tf_path = scene_dir / "transforms.json"
    cam_pos  = None
    cam_rot  = None
    if tf_path.exists():
        transforms = load_transforms(str(tf_path))
        frame = transforms.get_frame(view_id)
        if frame:
            cam_pos = frame.camera_position()
            cam_rot = frame.rotation_matrix_3x3()

    analysis["view_id"]         = view_id
    analysis["camera_position"] = cam_pos
    analysis["camera_rotation"] = cam_rot

    view_json = ViewJSON(**analysis)
    store.save(view_json)

    return {"saved": True, "view_id": view_id, "space_type": view_json.space_type}


@mcp.tool()
def get_view_analysis(scene_id: str, view_id: str) -> dict:
    """
    Get the full stored VLM analysis JSON for a view.
    Used during query traversal leaf confirmation.

    Returns:
        ViewJSON dict, or {"error": ...} if not yet analyzed.
    """
    scene_dir = DATA_DIR / scene_id
    store     = ViewStore(str(scene_dir))
    view      = store.load(view_id)
    if view is None:
        return {"error": f"View '{view_id}' not analyzed. Run get_view_image then save_view_analysis."}
    return view.model_dump()


@mcp.tool()
def list_view_summaries(scene_id: str) -> dict:
    """
    Return compact one-line summaries for ALL analyzed views.
    Cursor AI uses this as input to start building the semantic tree.

    Returns:
        {"summaries": [{"view_id": str, "one_line_summary": str, "space_type": str, "camera_position": [...]}]}
    """
    scene_dir = DATA_DIR / scene_id
    store     = ViewStore(str(scene_dir))
    return {"summaries": store.all_summaries()}
```

- [ ] **Step 4: Tree tools — Cursor AI builds the tree by calling these**

```python
# backend/mcp/tools/tree_tools.py
"""
Tree construction and navigation tools.

Cursor AI builds the tree by:
  1. get_spatial_clusters(scene_id) → get spatially grouped view_id lists
  2. For each cluster: call get_subtree_summaries(view_ids)
     → read summaries, decide groupings (using TREE_GROUPING_PROMPT)
     → call save_node() for each group
  3. Recurse into each child group
  4. Call finalize_tree(scene_id, root_id)

At query time, Cursor AI navigates by:
  1. get_root_node(scene_id) → root summary
  2. get_children(scene_id, node_id) → child summaries
  3. Decide which to descend (using TRAVERSAL_STEP_PROMPT)
  4. Repeat until leaf
"""
import json
from pathlib import Path
from typing import List, Optional
from backend.mcp.server import mcp
from backend.config import DATA_DIR
from backend.tree.nodes import TreeNode, NodeType
from backend.tree.storage import TreeStorage
from backend.geometry.spatial_graph import SpatialGraph
from backend.io.view_store import ViewStore
from backend.schemas.types import TREE_GROUPING_PROMPT, TRAVERSAL_STEP_PROMPT, LEAF_CONFIRMATION_PROMPT


@mcp.tool()
def get_spatial_clusters(scene_id: str) -> dict:
    """
    Use spatial proximity to group view IDs into candidate clusters.
    Each cluster contains views that are physically close to each other.
    Cursor AI should build one sub-tree per cluster, then merge at the root level.

    Returns:
        {
          "clusters": [["v001", "v002", ...], ["v010", ...], ...],
          "threshold_metres": float,
          "grouping_prompt_template": str   ← TREE_GROUPING_PROMPT for Cursor AI to use
        }
    """
    scene_dir = DATA_DIR / scene_id
    store     = ViewStore(str(scene_dir))
    summaries = store.all_summaries()

    if not summaries:
        return {"error": "No analyzed views found. Analyze views first."}

    positions = {
        s["view_id"]: s["camera_position"]
        for s in summaries
        if s.get("camera_position")
    }

    if len(positions) < 2:
        return {"clusters": [[s["view_id"] for s in summaries]],
                "threshold_metres": 0.0,
                "grouping_prompt_template": TREE_GROUPING_PROMPT}

    graph = SpatialGraph(positions)
    components = graph.connected_components()

    return {
        "clusters":               components,
        "threshold_metres":       graph.threshold,
        "total_views":            len(summaries),
        "grouping_prompt_template": TREE_GROUPING_PROMPT,
    }


@mcp.tool()
def get_summaries_for_views(scene_id: str, view_ids: List[str]) -> dict:
    """
    Return one-line summaries for a specific subset of views.
    Cursor AI uses this at each recursion level to get the input for a grouping decision.

    Returns:
        {"summaries": [{"view_id": str, "one_line_summary": str, ...}]}
    """
    scene_dir = DATA_DIR / scene_id
    store     = ViewStore(str(scene_dir))
    results   = []
    for vid in view_ids:
        v = store.load(vid)
        if v:
            results.append({
                "view_id":          v.view_id,
                "one_line_summary": v.one_line_summary,
                "space_type":       v.space_type,
                "camera_position":  v.camera_position,
            })
    return {"summaries": results}


@mcp.tool()
def save_node(scene_id: str, node: dict) -> dict:
    """
    Save a tree node that Cursor AI has constructed.
    Cursor AI calls this after deciding how to group a set of views.

    Args:
        scene_id: Scene identifier.
        node: Dict matching TreeNode structure:
          {
            "node_id":      str,       ← generate a unique ID (e.g. "node_living_room")
            "node_type":    "internal|cluster|leaf",
            "name":         str,       ← descriptive name Cursor AI chose
            "summary":      str,       ← one-sentence summary Cursor AI wrote
            "depth":        int,
            "parent_id":    str | null,
            "children_ids": [str, ...],
            "view_ids":     [str, ...]
          }

    Returns:
        {"saved": true, "node_id": str}
    """
    scene_dir = DATA_DIR / scene_id
    store     = ViewStore(str(scene_dir))
    storage   = TreeStorage(str(scene_dir))

    # Inject camera positions from view store
    positions = []
    for vid in node.get("view_ids", []):
        v = store.load(vid)
        if v and v.camera_position:
            positions.append(v.camera_position)

    tree_node = TreeNode.from_dict({
        **node,
        "camera_positions": positions,
    })
    tree_node.compute_spatial_stats()
    storage.save_node(tree_node)

    return {"saved": True, "node_id": tree_node.node_id, "name": tree_node.name}


@mcp.tool()
def get_node(scene_id: str, node_id: str) -> dict:
    """Get full details of a specific tree node."""
    scene_dir = DATA_DIR / scene_id
    storage   = TreeStorage(str(scene_dir))
    node      = storage.get_node(node_id)
    if not node:
        return {"error": f"Node '{node_id}' not found"}
    return node.to_dict()


@mcp.tool()
def get_root_node(scene_id: str) -> dict:
    """
    Get the root node of the semantic tree.
    Cursor AI calls this to start a query traversal.
    """
    scene_dir = DATA_DIR / scene_id
    storage   = TreeStorage(str(scene_dir))
    root      = storage.get_root()
    if not root:
        return {"error": "No root node found. Build the tree first using save_node calls."}
    return root.to_dict()


@mcp.tool()
def get_children(scene_id: str, node_id: str) -> dict:
    """
    Get the children of a node with their summaries.
    Cursor AI reads these summaries to decide which branches to traverse.

    Also returns the traversal prompt template for Cursor AI to use.

    Returns:
        {
          "node_id": str,
          "children": [{"node_id": str, "name": str, "summary": str, "node_type": str}],
          "traversal_prompt_template": str
        }
    """
    scene_dir = DATA_DIR / scene_id
    storage   = TreeStorage(str(scene_dir))
    node      = storage.get_node(node_id)
    if not node:
        return {"error": f"Node '{node_id}' not found"}

    children = []
    for cid in node.children_ids:
        child = storage.get_node(cid)
        if child:
            children.append({
                "node_id":   child.node_id,
                "name":      child.name,
                "summary":   child.summary,
                "node_type": child.node_type.value,
                "num_views": len(child.view_ids),
                "spatial_centroid": child.spatial_centroid,
            })

    return {
        "node_id":   node_id,
        "node_name": node.name,
        "node_summary": node.summary,
        "children":  children,
        "traversal_prompt_template": TRAVERSAL_STEP_PROMPT,
    }


@mcp.tool()
def get_views_in_node(scene_id: str, node_id: str) -> dict:
    """
    Get all view IDs (and their summaries) under a node.
    Used when Cursor AI reaches a leaf or cluster node during traversal.
    """
    scene_dir = DATA_DIR / scene_id
    storage   = TreeStorage(str(scene_dir))
    store     = ViewStore(str(scene_dir))
    node      = storage.get_node(node_id)
    if not node:
        return {"error": f"Node '{node_id}' not found"}

    views = []
    for vid in node.view_ids:
        v = store.load(vid)
        if v:
            views.append({"view_id": v.view_id, "one_line_summary": v.one_line_summary})

    return {
        "node_id":   node_id,
        "node_name": node.name,
        "views":     views,
        "leaf_confirmation_prompt_template": LEAF_CONFIRMATION_PROMPT,
    }


@mcp.tool()
def search_summaries(scene_id: str, keywords: str) -> dict:
    """
    Keyword search across all tree node summaries.
    Quick exploration tool — does not require full query traversal.

    Returns:
        {"matches": [{"node_id": str, "name": str, "summary": str, "score": int}]}
    """
    scene_dir = DATA_DIR / scene_id
    storage   = TreeStorage(str(scene_dir))
    all_nodes = storage.all_nodes()
    kws       = [k.lower() for k in keywords.split()]

    matches = []
    for node in all_nodes.values():
        text  = f"{node.name} {node.summary}".lower()
        score = sum(1 for kw in kws if kw in text)
        if score > 0:
            matches.append({
                "node_id": node.node_id,
                "name":    node.name,
                "summary": node.summary,
                "depth":   node.depth,
                "score":   score,
            })
    matches.sort(key=lambda x: -x["score"])
    return {"matches": matches[:20]}


@mcp.tool()
def get_tree_for_viz(scene_id: str) -> dict:
    """
    Return the full tree in D3.js nested format for the frontend visualizer.
    """
    scene_dir = DATA_DIR / scene_id
    storage   = TreeStorage(str(scene_dir))
    d3_tree   = storage.to_d3_tree()
    if not d3_tree:
        return {"error": "Tree not built yet."}
    return d3_tree
```

- [ ] **Step 5: Query tools — geometry only, Cursor AI supplies all reasoning**

```python
# backend/mcp/tools/query_tools.py
"""
Query infrastructure tools.
Cursor AI drives the full query loop by calling these tools and applying
its own reasoning at each step. No LLM calls inside these tools.
"""
import json
import numpy as np
from pathlib import Path
from typing import List
from backend.mcp.server import mcp
from backend.config import DATA_DIR
from backend.geometry.unprojector import unproject_bbox_to_3d, merge_3d_bboxes
from backend.io.nerfstudio import load_transforms
from backend.schemas.types import BBox3D


def _get_intrinsics(scene_id: str) -> dict:
    tf_path = DATA_DIR / scene_id / "transforms.json"
    data = json.loads(tf_path.read_text())
    return {"fx": data["fl_x"], "fy": data["fl_y"], "cx": data["cx"], "cy": data["cy"]}


def _get_frame(scene_id: str, view_id: str):
    tf_path = DATA_DIR / scene_id / "transforms.json"
    transforms = load_transforms(str(tf_path))
    return transforms.get_frame(view_id)


@mcp.tool()
def unproject_bbox(scene_id: str, view_id: str, bbox_2d: List[int]) -> dict:
    """
    Convert a 2D bounding box detected in a view to a 3D bounding box in world coordinates.
    Cursor AI calls this after finding the object's bbox_2d in the view analysis JSON.

    Args:
        scene_id: Scene identifier.
        view_id:  View where the object was found.
        bbox_2d:  [x1, y1, x2, y2] pixel coordinates.

    Returns:
        {"center": [x,y,z], "dimensions": [w,h,d], "bbox_min": [...], "bbox_max": [...]}
        or {"error": ...}
    """
    depth_path = DATA_DIR / scene_id / "depths" / f"{view_id}_depth.npy"
    if not depth_path.exists():
        return {"error": f"Depth map not found for view '{view_id}'"}

    depth_map  = np.load(str(depth_path))
    intrinsics = _get_intrinsics(scene_id)
    frame      = _get_frame(scene_id, view_id)
    if not frame:
        return {"error": f"Camera frame not found for view '{view_id}'"}

    result = unproject_bbox_to_3d(bbox_2d, depth_map, frame.transform_matrix, intrinsics)
    if result is None:
        return {"error": "Insufficient valid depth pixels in the bounding box region."}
    return result


@mcp.tool()
def merge_bboxes(bboxes: List[dict], iou_threshold: float = 0.5) -> dict:
    """
    Merge overlapping 3D bounding boxes into unique instances.
    Used for aggregation queries (e.g., "how many chairs?") to deduplicate.

    Args:
        bboxes: List of bbox dicts from unproject_bbox calls.
        iou_threshold: 3D IoU above which two boxes are considered the same object.

    Returns:
        {"merged_bboxes": [...], "count": int}
    """
    merged = merge_3d_bboxes(bboxes, iou_threshold)
    return {"merged_bboxes": merged, "count": len(merged)}


@mcp.tool()
def get_capture_intrinsics(scene_id: str) -> dict:
    """
    Return camera intrinsics for this scene (focal length, principal point).
    Useful context for Cursor AI when reasoning about scale and field of view.
    """
    tf_path = DATA_DIR / scene_id / "transforms.json"
    if not tf_path.exists():
        return {"error": "transforms.json not found"}
    data = json.loads(tf_path.read_text())
    return {
        "fl_x": data["fl_x"], "fl_y": data["fl_y"],
        "cx":   data["cx"],   "cy":   data["cy"],
        "w":    data["w"],    "h":    data["h"],
    }


@mcp.tool()
def get_view_camera_pose(scene_id: str, view_id: str) -> dict:
    """
    Get the camera pose (position and transform matrix) for a specific view.
    Cursor AI can use this for spatial reasoning about query results.

    Returns:
        {"view_id": str, "position": [x,y,z], "transform_matrix": [[...4x4...]]}
    """
    frame = _get_frame(scene_id, view_id)
    if not frame:
        return {"error": f"View '{view_id}' not found in transforms.json"}
    return {
        "view_id":          view_id,
        "position":         frame.camera_position(),
        "transform_matrix": frame.transform_matrix,
    }


@mcp.tool()
def compute_inter_node_distances(scene_id: str, node_ids_a: List[str], node_ids_b: List[str]) -> dict:
    """
    Compute spatial distance between two groups of nodes (by their spatial centroids).
    Used for cross-zone geometric queries like "nearest bathroom to master bedroom".

    Returns:
        {"min_distance_metres": float, "closest_pair": ["node_a_id", "node_b_id"]}
    """
    from backend.tree.storage import TreeStorage
    storage = TreeStorage(str(DATA_DIR / scene_id))

    centroids_a = {}
    for nid in node_ids_a:
        n = storage.get_node(nid)
        if n and n.spatial_centroid:
            centroids_a[nid] = n.spatial_centroid

    centroids_b = {}
    for nid in node_ids_b:
        n = storage.get_node(nid)
        if n and n.spatial_centroid:
            centroids_b[nid] = n.spatial_centroid

    if not centroids_a or not centroids_b:
        return {"error": "One or both node groups have no spatial centroid data"}

    min_dist  = float("inf")
    best_pair = None
    for na, ca in centroids_a.items():
        for nb, cb in centroids_b.items():
            d = float(np.linalg.norm(np.array(ca) - np.array(cb)))
            if d < min_dist:
                min_dist  = d
                best_pair = [na, nb]

    return {"min_distance_metres": min_dist, "closest_pair": best_pair}
```

- [ ] **Step 6: Commit**

```bash
git add backend/mcp/
git commit -m "feat: MCP server with 20 pure-infrastructure tools — zero LLM API calls, all intelligence via Cursor AI"
```

---

## Task 7: FastAPI REST + WebSocket Bridge

**Files:**
- Create: `backend/api/server.py`
- Create: `backend/api/routes/scenes.py`
- Create: `backend/api/routes/captures.py`
- Create: `backend/api/routes/tree.py`
- Create: `backend/api/routes/query.py`

- [ ] **Step 1: API server**

```python
# backend/api/server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import scenes, captures, tree, query

app = FastAPI(title="SemanticSplat API", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

app.include_router(scenes.router,   prefix="/api/scenes",   tags=["scenes"])
app.include_router(captures.router, prefix="/api/captures", tags=["captures"])
app.include_router(tree.router,     prefix="/api/tree",     tags=["tree"])
app.include_router(query.router,    prefix="/api/query",    tags=["query"])
```

- [ ] **Step 2: Capture endpoint — receives R-keypress data from browser**

```python
# backend/api/routes/captures.py
"""
Receives captured views from the Spark.js navigator frontend.
On R-keypress the browser sends: RGB (PNG base64) + depth (float32 base64) + camera matrix.
"""
import base64
import json
import numpy as np
from pathlib import Path
from fastapi import APIRouter
from backend.schemas.types import CapturePayload
from backend.config import DATA_DIR
from backend.io.nerfstudio import get_or_create_transforms, save_transforms, FrameEntry

router = APIRouter()


@router.post("/save")
async def save_capture(payload: CapturePayload) -> dict:
    """
    Save a captured view from the browser to disk.
    Creates:
      - images/{view_id}.png
      - depths/{view_id}_depth.npy
      - updates transforms.json (nerfstudio format)
    """
    scene_dir = DATA_DIR / payload.scene_id
    for sub in ["images", "depths"]:
        (scene_dir / sub).mkdir(parents=True, exist_ok=True)

    # Decode and save RGB image
    rgb_bytes = base64.b64decode(payload.rgb_b64)
    img_path  = scene_dir / "images" / f"{payload.view_id}.png"
    img_path.write_bytes(rgb_bytes)

    # Decode and save depth map (float32 array, row-major, metres)
    depth_bytes  = base64.b64decode(payload.depth_b64)
    depth_array  = np.frombuffer(depth_bytes, dtype=np.float32).reshape(payload.h, payload.w)
    depth_path   = scene_dir / "depths" / f"{payload.view_id}_depth.npy"
    np.save(str(depth_path), depth_array)

    # Update Nerfstudio transforms.json
    transforms = get_or_create_transforms(
        str(scene_dir),
        w=payload.w, h=payload.h,
        fl_x=payload.fl_x, fl_y=payload.fl_y,
        cx=payload.cx, cy=payload.cy
    )
    frame = FrameEntry(
        file_path=f"images/{payload.view_id}.png",
        depth_file_path=f"depths/{payload.view_id}_depth.npy",
        transform_matrix=payload.transform_matrix,
        view_id=payload.view_id,
    )
    transforms.add_frame(frame)
    save_transforms(transforms, str(scene_dir / "transforms.json"))

    return {
        "saved":      True,
        "view_id":    payload.view_id,
        "img_path":   str(img_path),
        "depth_path": str(depth_path),
        "total_captured": len(transforms.frames),
    }


@router.get("/{scene_id}")
async def list_captures(scene_id: str) -> dict:
    """List all captured views for a scene."""
    tf_path = DATA_DIR / scene_id / "transforms.json"
    if not tf_path.exists():
        return {"frames": [], "total": 0}
    data = json.loads(tf_path.read_text())
    return {"frames": data.get("frames", []), "total": len(data.get("frames", []))}
```

- [ ] **Step 3: Remaining routes**

```python
# backend/api/routes/scenes.py
from fastapi import APIRouter
from backend.mcp.tools.scene_tools import init_scene, get_scene_info, list_scenes

router = APIRouter()

@router.post("/{scene_id}/init")
async def api_init_scene(scene_id: str, ply_filename: str = "scene.ply"):
    return init_scene(scene_id, ply_filename)

@router.get("/{scene_id}")
async def api_get_scene(scene_id: str):
    return get_scene_info(scene_id)

@router.get("/")
async def api_list_scenes():
    return list_scenes()
```

```python
# backend/api/routes/tree.py
from fastapi import APIRouter
from backend.mcp.tools.tree_tools import get_tree_for_viz, get_node, get_children, search_summaries

router = APIRouter()

@router.get("/{scene_id}/viz")
async def api_get_tree_viz(scene_id: str):
    return get_tree_for_viz(scene_id)

@router.get("/{scene_id}/node/{node_id}")
async def api_get_node(scene_id: str, node_id: str):
    return get_node(scene_id, node_id)

@router.get("/{scene_id}/node/{node_id}/children")
async def api_get_children(scene_id: str, node_id: str):
    return get_children(scene_id, node_id)

@router.get("/{scene_id}/search")
async def api_search(scene_id: str, keywords: str):
    return search_summaries(scene_id, keywords)
```

```python
# backend/api/routes/query.py
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from backend.mcp.tools.query_tools import unproject_bbox as _unproject
from backend.mcp.tools.tree_tools import get_root_node, get_children, get_views_in_node
from backend.mcp.tools.view_tools import get_view_analysis
from backend.config import DATA_DIR

router = APIRouter()

class UnprojectRequest(BaseModel):
    view_id: str
    bbox_2d: list[int]

@router.post("/{scene_id}/unproject")
async def api_unproject(scene_id: str, req: UnprojectRequest):
    return _unproject(scene_id, req.view_id, req.bbox_2d)

@router.websocket("/{scene_id}/stream")
async def api_query_stream(ws: WebSocket, scene_id: str):
    """
    Streams tree node data as Cursor AI traverses it.
    Browser connects, sends {"query": "..."}.
    Server sends node data as Cursor AI visits each node.
    This route is driven by the frontend displaying progress —
    actual traversal reasoning is done by Cursor AI via MCP tools.
    """
    await ws.accept()
    try:
        data  = await ws.receive_json()
        query = data.get("query", "")
        await ws.send_json({"event": "received", "query": query,
                            "message": "Use Cursor AI MCP tools to traverse the tree. This WebSocket shows live progress."})
        await ws.send_json({"event": "ready"})
    except WebSocketDisconnect:
        pass
```

- [ ] **Step 4: Start API server and test**

```bash
uvicorn backend.api.server:app --reload --port 8000
```

```bash
# Quick smoke test
curl -X POST http://localhost:8000/api/scenes/test_scene/init
```

Expected: `{"scene_id": "test_scene", "scene_dir": "...", ...}`

- [ ] **Step 5: Commit**

```bash
git add backend/api/
git commit -m "feat: FastAPI REST bridge — scene init, capture save (nerfstudio), tree and query routes"
```

---

## Task 8: Frontend Types, Stores, and API Client

**Files:**
- Create: `frontend/src/types/index.ts`
- Create: `frontend/src/api/client.ts`
- Create: `frontend/src/store/sceneStore.ts`
- Create: `frontend/src/store/treeStore.ts`
- Create: `frontend/src/store/queryStore.ts`

- [ ] **Step 1: TypeScript types**

```typescript
// frontend/src/types/index.ts
export interface FrameEntry {
  view_id: string;
  file_path: string;
  depth_file_path?: string;
  transform_matrix: number[][];  // 4×4 row-major camera-to-world
}

export interface CapturedView {
  view_id: string;
  thumbnail: string;  // object URL of canvas snapshot
  position: [number, number, number];
}

export interface ObjectEntry {
  label: string;
  bbox_2d: [number, number, number, number];
  confidence: 'high' | 'medium' | 'low';
  attributes: { color?: string; material?: string; size?: string; condition?: string };
  functional_description?: string;
}

export interface ViewJSON {
  view_id: string;
  one_line_summary: string;
  space_type: string;
  object_list: string[];
  objects: ObjectEntry[];
  spatial_relations: string[];
  notable_features?: string;
  visibility_quality: 'clear' | 'partial' | 'obstructed';
  camera_position?: [number, number, number];
}

export type NodeType = 'internal' | 'cluster' | 'leaf';

export interface TreeNode {
  id: string;
  name: string;
  summary: string;
  node_type: NodeType;
  depth: number;
  num_views: number;
  spatial_centroid?: [number, number, number];
  children?: TreeNode[];
}

export interface BBox3D {
  center: [number, number, number];
  dimensions: [number, number, number];
  bbox_min: [number, number, number];
  bbox_max: [number, number, number];
}

export interface SceneInfo {
  scene_id: string;
  num_captured: number;
  num_analyzed: number;
  tree_built: boolean;
  status: 'initialized' | 'capturing' | 'analyzing' | 'complete';
}

export interface TraversalEvent {
  event: 'visit' | 'descend' | 'pruned' | 'selected' | 'result' | 'done';
  node_id?: string;
  name?: string;
  view_ids?: string[];
  bbox_2d?: [number, number, number, number];
  bbox_3d?: BBox3D;
  confidence?: string;
  matched_object?: string;
}
```

- [ ] **Step 2: API client**

```typescript
// frontend/src/api/client.ts
import axios from 'axios';
import type { SceneInfo, TreeNode, FrameEntry, BBox3D } from '../types';

const api = axios.create({ baseURL: '/api' });

export const sceneApi = {
  init:    (scene_id: string) => api.post<SceneInfo>(`/scenes/${scene_id}/init`),
  getInfo: (scene_id: string) => api.get<SceneInfo>(`/scenes/${scene_id}`),
  list:    () => api.get<{ scenes: SceneInfo[] }>('/scenes/'),
};

export const captureApi = {
  save: (payload: {
    scene_id: string; view_id: string; transform_matrix: number[][];
    fl_x: number; fl_y: number; cx: number; cy: number; w: number; h: number;
    rgb_b64: string; depth_b64: string;
  }) => api.post('/captures/save', payload),
  list: (scene_id: string) => api.get<{ frames: FrameEntry[] }>(`/captures/${scene_id}`),
};

export const treeApi = {
  getViz:      (scene_id: string) => api.get<TreeNode>(`/tree/${scene_id}/viz`),
  getNode:     (scene_id: string, node_id: string) => api.get(`/tree/${scene_id}/node/${node_id}`),
  getChildren: (scene_id: string, node_id: string) => api.get(`/tree/${scene_id}/node/${node_id}/children`),
  search:      (scene_id: string, keywords: string) => api.get(`/tree/${scene_id}/search`, { params: { keywords } }),
};

export const queryApi = {
  unproject: (scene_id: string, view_id: string, bbox_2d: number[]) =>
    api.post<{ center: number[]; dimensions: number[] }>(`/query/${scene_id}/unproject`, { view_id, bbox_2d }),
};
```

- [ ] **Step 3: Zustand stores**

```typescript
// frontend/src/store/sceneStore.ts
import { create } from 'zustand';
import type { SceneInfo, CapturedView } from '../types';

interface SceneState {
  sceneId: string | null;
  plyUrl:  string | null;
  info:    SceneInfo | null;
  capturedViews: CapturedView[];
  viewCounter: number;
  setScene: (id: string, plyUrl: string) => void;
  setInfo:  (info: SceneInfo) => void;
  addCapturedView: (view: CapturedView) => void;
  nextViewId: () => string;
}

export const useSceneStore = create<SceneState>((set, get) => ({
  sceneId: null, plyUrl: null, info: null,
  capturedViews: [], viewCounter: 0,
  setScene: (sceneId, plyUrl) => set({ sceneId, plyUrl }),
  setInfo:  (info) => set({ info }),
  addCapturedView: (view) => set(s => ({ capturedViews: [...s.capturedViews, view] })),
  nextViewId: () => {
    const n = get().viewCounter + 1;
    set({ viewCounter: n });
    return `v${String(n).padStart(3, '0')}`;
  },
}));
```

```typescript
// frontend/src/store/treeStore.ts
import { create } from 'zustand';
import type { TreeNode } from '../types';

interface TreeState {
  treeData:        TreeNode | null;
  selectedNode:    TreeNode | null;
  highlightedIds:  Set<string>;
  prunedIds:       Set<string>;
  setTreeData:     (t: TreeNode) => void;
  selectNode:      (n: TreeNode | null) => void;
  highlightNodes:  (ids: string[]) => void;
  pruneNodes:      (ids: string[]) => void;
  resetHighlights: () => void;
}

export const useTreeStore = create<TreeState>((set) => ({
  treeData: null, selectedNode: null,
  highlightedIds: new Set(), prunedIds: new Set(),
  setTreeData:     (treeData)    => set({ treeData }),
  selectNode:      (selectedNode) => set({ selectedNode }),
  highlightNodes:  (ids) => set(s => ({ highlightedIds: new Set([...s.highlightedIds, ...ids]) })),
  pruneNodes:      (ids) => set(s => ({ prunedIds:      new Set([...s.prunedIds,      ...ids]) })),
  resetHighlights: () => set({ highlightedIds: new Set(), prunedIds: new Set() }),
}));
```

```typescript
// frontend/src/store/queryStore.ts
import { create } from 'zustand';
import type { TraversalEvent, BBox3D } from '../types';

interface QueryState {
  query:     string;
  isRunning: boolean;
  events:    TraversalEvent[];
  resultBbox3d: BBox3D | null;
  resultViewId: string | null;
  setQuery:     (q: string) => void;
  setRunning:   (r: boolean) => void;
  addEvent:     (e: TraversalEvent) => void;
  setResult:    (bbox: BBox3D, viewId: string) => void;
  reset:        () => void;
}

export const useQueryStore = create<QueryState>((set) => ({
  query: '', isRunning: false, events: [],
  resultBbox3d: null, resultViewId: null,
  setQuery:   (query)    => set({ query }),
  setRunning: (isRunning) => set({ isRunning }),
  addEvent:   (e)        => set(s => ({ events: [...s.events, e] })),
  setResult:  (resultBbox3d, resultViewId) => set({ resultBbox3d, resultViewId }),
  reset:      () => set({ events: [], resultBbox3d: null, resultViewId: null, isRunning: false }),
}));
```

- [ ] **Step 4: Commit**

```bash
git add frontend/src/types/ frontend/src/api/ frontend/src/store/
git commit -m "feat: TypeScript types, axios API client, Zustand stores"
```

---

## Task 9: Depth Capture from WebGL

**Files:**
- Create: `frontend/src/components/Navigator/DepthCapture.ts`

This is the most technically nuanced piece. Spark.js builds on THREE.js, so we use `THREE.WebGLRenderTarget` with a depth texture to read pixel-accurate depth values from the rendered 3DGS scene.

- [ ] **Step 1: Implement depth capture utility**

```typescript
// frontend/src/components/Navigator/DepthCapture.ts
/**
 * Captures a linear depth map from a THREE.js renderer.
 *
 * Approach:
 *   1. Create a WebGLRenderTarget with a DepthTexture
 *   2. Render the Spark.js scene to this target
 *   3. Read depth texture pixels (r channel contains normalized depth [0,1])
 *   4. Convert to linear metres using camera near/far planes
 *
 * Note on Gaussian Splatting depth:
 *   Spark.js renders splats as sorted, alpha-blended point sprites.
 *   The depth buffer contains the depth of the last-written (nearest opaque-ish)
 *   splat at each pixel — a reasonable approximation for our purposes.
 */
import * as THREE from 'three';

export const CAMERA_NEAR = 0.1;   // Must match THREE.PerspectiveCamera near
export const CAMERA_FAR  = 100.0; // Must match THREE.PerspectiveCamera far

/**
 * Linearize a WebGL depth value (in [0,1]) to metres.
 * Uses the standard OpenGL linearization formula.
 */
function linearizeDepth(depthNdc: number, near: number, far: number): number {
  if (depthNdc >= 1.0) return 0.0;   // background / no surface
  const zNdc = depthNdc * 2.0 - 1.0;
  return (2.0 * near * far) / (far + near - zNdc * (far - near));
}

export class DepthCapture {
  private renderTarget: THREE.WebGLRenderTarget;
  private width:  number;
  private height: number;

  constructor(width: number, height: number) {
    this.width  = width;
    this.height = height;

    this.renderTarget = new THREE.WebGLRenderTarget(width, height, {
      depthTexture: new THREE.DepthTexture(width, height, THREE.FloatType),
      depthBuffer:  true,
      format:       THREE.RGBAFormat,
      type:         THREE.UnsignedByteType,
    });
  }

  /**
   * Render scene to depth target and return a Float32Array
   * of shape (width * height) with linearized depth in metres.
   */
  capture(renderer: THREE.WebGLRenderer, scene: THREE.Scene, camera: THREE.Camera): Float32Array {
    // Render to offscreen target
    renderer.setRenderTarget(this.renderTarget);
    renderer.render(scene, camera);
    renderer.setRenderTarget(null);

    // Read raw depth pixels (each pixel r,g,b,a — depth in the buffer)
    // THREE.js reads back RGBA even with a depth texture; the depth
    // value is packed into the components depending on FloatType.
    const rawBuffer = new Float32Array(this.width * this.height);
    renderer.readRenderTargetPixels(
      this.renderTarget, 0, 0, this.width, this.height, rawBuffer
    );

    // Linearize: rawBuffer[i] is the normalized [0,1] depth
    const depthMetres = new Float32Array(this.width * this.height);
    for (let i = 0; i < rawBuffer.length; i++) {
      depthMetres[i] = linearizeDepth(rawBuffer[i], CAMERA_NEAR, CAMERA_FAR);
    }

    return depthMetres;  // row-major, top-left origin
  }

  /**
   * Encode Float32Array depth map as base64 for POST to backend.
   * Backend does: np.frombuffer(base64.b64decode(s), dtype=np.float32).reshape(H, W)
   */
  static encodeDepth(depthData: Float32Array): string {
    const bytes = new Uint8Array(depthData.buffer);
    let binary  = '';
    for (let i = 0; i < bytes.length; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
  }

  dispose() {
    this.renderTarget.dispose();
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/components/Navigator/DepthCapture.ts
git commit -m "feat: WebGL depth capture from THREE.js render target → linear metres float32"
```

---

## Task 10: Spark.js Scene Loading Hook

**Files:**
- Create: `frontend/src/components/Navigator/useSparkScene.ts`

- [ ] **Step 1: Implement Spark.js loading hook**

```typescript
// frontend/src/components/Navigator/useSparkScene.ts
/**
 * Loads a 3DGS PLY file using @sparkjsdev/spark (SplatMesh) into a THREE.js scene.
 * Returns the renderer, THREE scene, camera, and a ready flag.
 *
 * Spark.js GitHub: https://github.com/sparkjsdev/spark
 * Install: npm install @sparkjsdev/spark
 */
import { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { SplatMesh } from '@sparkjsdev/spark';
import { CAMERA_NEAR, CAMERA_FAR } from './DepthCapture';

export interface SparkScene {
  renderer: THREE.WebGLRenderer;
  scene:    THREE.Scene;
  camera:   THREE.PerspectiveCamera;
  splat:    SplatMesh | null;
  ready:    boolean;
}

export function useSparkScene(
  canvasRef: React.RefObject<HTMLCanvasElement>,
  plyUrl:   string | null,
): SparkScene {
  const [ready, setReady]   = useState(false);
  const rendererRef         = useRef<THREE.WebGLRenderer | null>(null);
  const sceneRef            = useRef(new THREE.Scene());
  const cameraRef           = useRef(
    new THREE.PerspectiveCamera(60, 16 / 9, CAMERA_NEAR, CAMERA_FAR)
  );
  const splatRef            = useRef<SplatMesh | null>(null);

  // Initialise renderer once canvas is available
  useEffect(() => {
    if (!canvasRef.current) return;
    const renderer = new THREE.WebGLRenderer({
      canvas:      canvasRef.current,
      antialias:   false,
      powerPreference: 'high-performance',
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(canvasRef.current.clientWidth, canvasRef.current.clientHeight);
    rendererRef.current = renderer;

    cameraRef.current.position.set(0, -1, 3);
    cameraRef.current.lookAt(0, 0, 0);

    return () => {
      renderer.dispose();
      rendererRef.current = null;
    };
  }, [canvasRef]);

  // Load PLY scene via Spark.js SplatMesh
  useEffect(() => {
    if (!plyUrl || !rendererRef.current) return;
    setReady(false);

    // Remove previous splat
    if (splatRef.current) {
      sceneRef.current.remove(splatRef.current);
      splatRef.current.dispose?.();
    }

    const splat = new SplatMesh({ url: plyUrl });
    splat.quaternion.set(0, 0, 0, 1);  // upright orientation
    sceneRef.current.add(splat);
    splatRef.current = splat;

    // Spark.js SplatMesh emits 'loaded' when geometry is ready
    (splat as any).addEventListener?.('loaded', () => setReady(true));
    // Fallback: mark ready after a short delay
    const timer = setTimeout(() => setReady(true), 3000);
    return () => {
      clearTimeout(timer);
      sceneRef.current.remove(splat);
    };
  }, [plyUrl]);

  return {
    renderer: rendererRef.current!,
    scene:    sceneRef.current,
    camera:   cameraRef.current,
    splat:    splatRef.current,
    ready,
  };
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/components/Navigator/useSparkScene.ts
git commit -m "feat: Spark.js scene loading hook with SplatMesh, THREE.js camera setup"
```

---

## Task 11: FPS Controls Hook (WASD + QE + Shift + Mouse)

**Files:**
- Create: `frontend/src/components/Navigator/useFPSControls.ts`

- [ ] **Step 1: Implement FPS controls**

```typescript
// frontend/src/components/Navigator/useFPSControls.ts
/**
 * First-person camera controls for the Spark.js navigator.
 *
 * Controls:
 *   W / S       - move forward / backward (along camera look direction)
 *   A / D       - strafe left / right
 *   Q / E       - move down / up (world Y axis — height control)
 *   Shift       - hold to move 3× faster
 *   Mouse drag  - click+drag to look around (yaw + pitch)
 *   Pointer Lock - click canvas to enter immersive mode (Escape to exit)
 */
import { useEffect, useRef } from 'react';
import * as THREE from 'three';

const BASE_SPEED   = 2.0;   // units/second
const SHIFT_MULT   = 3.0;
const MOUSE_SENS_X = 0.002; // radians per pixel
const MOUSE_SENS_Y = 0.002;
const PITCH_LIMIT  = Math.PI / 2 - 0.05;

interface Keys {
  w: boolean; s: boolean; a: boolean; d: boolean;
  q: boolean; e: boolean; shift: boolean;
}

export function useFPSControls(
  camera:    THREE.PerspectiveCamera,
  canvas:    HTMLCanvasElement | null,
  enabled:   boolean = true,
) {
  const keys    = useRef<Keys>({ w:false, s:false, a:false, d:false, q:false, e:false, shift:false });
  const yaw     = useRef(0);   // radians, horizontal rotation
  const pitch   = useRef(0);   // radians, vertical rotation
  const isDragging = useRef(false);
  const lastX   = useRef(0);
  const lastY   = useRef(0);
  const lastTime = useRef(performance.now());

  // Apply yaw+pitch to camera quaternion
  const applyRotation = () => {
    const q = new THREE.Quaternion();
    const qY = new THREE.Quaternion();
    const qX = new THREE.Quaternion();
    qY.setFromAxisAngle(new THREE.Vector3(0, 1, 0), yaw.current);
    qX.setFromAxisAngle(new THREE.Vector3(1, 0, 0), pitch.current);
    q.multiplyQuaternions(qY, qX);
    camera.quaternion.copy(q);
  };

  useEffect(() => {
    if (!canvas || !enabled) return;

    // ── Key handlers ────────────────────────────────────────────
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.target !== document.body && e.target !== canvas) return;
      switch (e.code) {
        case 'KeyW':     keys.current.w     = true; break;
        case 'KeyS':     keys.current.s     = true; break;
        case 'KeyA':     keys.current.a     = true; break;
        case 'KeyD':     keys.current.d     = true; break;
        case 'KeyQ':     keys.current.q     = true; break;
        case 'KeyE':     keys.current.e     = true; break;
        case 'ShiftLeft':
        case 'ShiftRight': keys.current.shift = true; break;
      }
    };
    const onKeyUp = (e: KeyboardEvent) => {
      switch (e.code) {
        case 'KeyW':     keys.current.w     = false; break;
        case 'KeyS':     keys.current.s     = false; break;
        case 'KeyA':     keys.current.a     = false; break;
        case 'KeyD':     keys.current.d     = false; break;
        case 'KeyQ':     keys.current.q     = false; break;
        case 'KeyE':     keys.current.e     = false; break;
        case 'ShiftLeft':
        case 'ShiftRight': keys.current.shift = false; break;
      }
    };

    // ── Mouse look (drag or pointer lock) ───────────────────────
    const onMouseDown = (e: MouseEvent) => {
      if (e.button !== 0) return;
      isDragging.current = true;
      lastX.current = e.clientX;
      lastY.current = e.clientY;
      // Request pointer lock for immersive mode
      canvas.requestPointerLock?.();
    };
    const onMouseUp = () => { isDragging.current = false; };
    const onMouseMove = (e: MouseEvent) => {
      let dx = 0, dy = 0;
      if (document.pointerLockElement === canvas) {
        dx = e.movementX; dy = e.movementY;
      } else if (isDragging.current) {
        dx = e.clientX - lastX.current; dy = e.clientY - lastY.current;
        lastX.current = e.clientX; lastY.current = e.clientY;
      } else return;

      yaw.current   -= dx * MOUSE_SENS_X;
      pitch.current -= dy * MOUSE_SENS_Y;
      pitch.current  = Math.max(-PITCH_LIMIT, Math.min(PITCH_LIMIT, pitch.current));
      applyRotation();
    };

    document.addEventListener('keydown',   onKeyDown);
    document.addEventListener('keyup',     onKeyUp);
    canvas.addEventListener('mousedown',   onMouseDown);
    document.addEventListener('mouseup',   onMouseUp);
    document.addEventListener('mousemove', onMouseMove);

    return () => {
      document.removeEventListener('keydown',   onKeyDown);
      document.removeEventListener('keyup',     onKeyUp);
      canvas.removeEventListener('mousedown',   onMouseDown);
      document.removeEventListener('mouseup',   onMouseUp);
      document.removeEventListener('mousemove', onMouseMove);
    };
  }, [canvas, enabled, camera]);

  // Animation loop tick — moves camera based on held keys
  const tick = () => {
    const now  = performance.now();
    const dt   = Math.min((now - lastTime.current) / 1000, 0.05); // seconds, capped at 50ms
    lastTime.current = now;

    if (!enabled) return;

    const speed  = BASE_SPEED * (keys.current.shift ? SHIFT_MULT : 1.0) * dt;
    const fwd    = new THREE.Vector3(0, 0, -1).applyQuaternion(camera.quaternion);
    const right  = new THREE.Vector3(1, 0,  0).applyQuaternion(camera.quaternion);
    const up     = new THREE.Vector3(0, 1,  0); // world up — always vertical

    // Flatten forward/right to horizontal plane for WASD
    fwd.y = 0; fwd.normalize();
    right.y = 0; right.normalize();

    if (keys.current.w) camera.position.addScaledVector(fwd,    speed);
    if (keys.current.s) camera.position.addScaledVector(fwd,   -speed);
    if (keys.current.a) camera.position.addScaledVector(right, -speed);
    if (keys.current.d) camera.position.addScaledVector(right,  speed);
    if (keys.current.e) camera.position.addScaledVector(up,     speed);  // rise
    if (keys.current.q) camera.position.addScaledVector(up,    -speed);  // descend
  };

  return { tick };
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/components/Navigator/useFPSControls.ts
git commit -m "feat: FPS controls — WASD+QE+Shift movement, mouse look, pointer lock"
```

---

## Task 12: View Capture Hook ("R" Key)

**Files:**
- Create: `frontend/src/components/Navigator/useViewCapture.ts`

- [ ] **Step 1: Implement capture hook**

```typescript
// frontend/src/components/Navigator/useViewCapture.ts
/**
 * Captures the current view when the user presses "R".
 *
 * On capture:
 *   1. Read RGB from canvas via toDataURL() → base64 PNG
 *   2. Read depth from WebGL via DepthCapture → float32 base64
 *   3. Read camera pose from THREE.js camera.matrixWorld → 4×4 row-major
 *   4. POST to /api/captures/save
 *   5. Store thumbnail in Zustand for the sidebar list
 *   6. Flash animation on screen
 */
import { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { DepthCapture } from './DepthCapture';
import { captureApi } from '../../api/client';
import { useSceneStore } from '../../store/sceneStore';

function getTransformMatrix(camera: THREE.PerspectiveCamera): number[][] {
  // camera.matrixWorld is camera-to-world in THREE.js column-major order
  camera.updateMatrixWorld();
  const e = camera.matrixWorld.elements;
  // Convert column-major to row-major 4×4
  return [
    [e[0], e[4], e[8],  e[12]],
    [e[1], e[5], e[9],  e[13]],
    [e[2], e[6], e[10], e[14]],
    [e[3], e[7], e[11], e[15]],
  ];
}

function canvasToBase64Png(canvas: HTMLCanvasElement): string {
  const dataUrl = canvas.toDataURL('image/png');
  return dataUrl.split(',')[1];  // strip "data:image/png;base64,"
}

export function useViewCapture(
  camera:   THREE.PerspectiveCamera | null,
  renderer: THREE.WebGLRenderer | null,
  scene:    THREE.Scene | null,
  canvas:   HTMLCanvasElement | null,
  enabled:  boolean,
) {
  const [isFlashing, setIsFlashing] = useState(false);
  const depthCaptureRef = useRef<DepthCapture | null>(null);
  const { sceneId, nextViewId, addCapturedView } = useSceneStore();

  // Initialize depth capture when renderer is ready
  useEffect(() => {
    if (!renderer || !canvas) return;
    const w = canvas.width;
    const h = canvas.height;
    depthCaptureRef.current = new DepthCapture(w, h);
    return () => { depthCaptureRef.current?.dispose(); };
  }, [renderer, canvas]);

  useEffect(() => {
    if (!enabled) return;

    const onKeyDown = async (e: KeyboardEvent) => {
      if (e.code !== 'KeyR') return;
      if (!camera || !renderer || !scene || !canvas || !sceneId) return;
      if (!depthCaptureRef.current) return;

      e.preventDefault();

      // 1. RGB
      const rgb_b64 = canvasToBase64Png(canvas);

      // 2. Depth
      const depthData  = depthCaptureRef.current.capture(renderer, scene, camera);
      const depth_b64  = DepthCapture.encodeDepth(depthData);

      // 3. Camera pose
      const transform_matrix = getTransformMatrix(camera);
      const fov  = camera.fov;
      const w    = canvas.width;
      const h    = canvas.height;
      // Focal lengths from FOV: fl = (h/2) / tan(fov_y/2)
      const fl_y = (h / 2) / Math.tan((fov * Math.PI / 180) / 2);
      const fl_x = fl_y;  // square pixels
      const cx   = w / 2;
      const cy   = h / 2;

      // 4. View ID
      const view_id = nextViewId();

      // 5. Flash
      setIsFlashing(true);
      setTimeout(() => setIsFlashing(false), 300);

      // 6. POST to backend
      try {
        await captureApi.save({
          scene_id: sceneId, view_id, transform_matrix,
          fl_x, fl_y, cx, cy, w, h, rgb_b64, depth_b64,
        });
        // 7. Store thumbnail
        addCapturedView({
          view_id,
          thumbnail: `data:image/png;base64,${rgb_b64}`,
          position:  [transform_matrix[0][3], transform_matrix[1][3], transform_matrix[2][3]],
        });
        console.log(`[Navigator] Captured ${view_id} at`, transform_matrix.map(r => r[3].toFixed(2)));
      } catch (err) {
        console.error('[Navigator] Capture failed:', err);
      }
    };

    document.addEventListener('keydown', onKeyDown);
    return () => document.removeEventListener('keydown', onKeyDown);
  }, [camera, renderer, scene, canvas, enabled, sceneId, nextViewId, addCapturedView]);

  return { isFlashing };
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/components/Navigator/useViewCapture.ts
git commit -m "feat: R-key view capture — RGB+depth+pose → base64 POST → Nerfstudio JSON"
```

---

## Task 13: Professional Navigator UI Component

**Files:**
- Create: `frontend/src/components/Navigator/HUD.tsx`
- Create: `frontend/src/components/Navigator/CapturedViewList.tsx`
- Create: `frontend/src/components/Navigator/Navigator.tsx`

- [ ] **Step 1: HUD overlay**

```tsx
// frontend/src/components/Navigator/HUD.tsx
import * as THREE from 'three';

interface HUDProps {
  camera:      THREE.PerspectiveCamera | null;
  isFlashing:  boolean;
  captureCount: number;
  isReady:     boolean;
}

export function HUD({ camera, isFlashing, captureCount, isReady }: HUDProps) {
  const pos = camera?.position;
  const rot = camera ? new THREE.Euler().setFromQuaternion(camera.quaternion) : null;

  return (
    <>
      {/* Capture flash */}
      {isFlashing && (
        <div className="absolute inset-0 bg-white/30 pointer-events-none z-30 animate-pulse" />
      )}

      {/* Crosshair */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none z-20">
        <div className="relative w-6 h-6">
          <div className="absolute top-1/2 left-0 right-0 h-px bg-white/70" />
          <div className="absolute left-1/2 top-0 bottom-0 w-px bg-white/70" />
          <div className="absolute inset-0 w-2 h-2 m-auto border border-white/50 rounded-full" />
        </div>
      </div>

      {/* Top bar */}
      <div className="absolute top-0 left-0 right-0 px-4 py-2 flex items-center justify-between
                      bg-gradient-to-b from-black/60 to-transparent pointer-events-none z-20">
        <div className="flex items-center gap-3">
          <div className={`w-2 h-2 rounded-full ${isReady ? 'bg-green-400' : 'bg-yellow-400 animate-pulse'}`} />
          <span className="text-white text-xs font-mono">
            {isReady ? 'Scene ready' : 'Loading 3DGS scene...'}
          </span>
        </div>
        <div className="text-white/80 text-xs font-mono">
          {captureCount} view{captureCount !== 1 ? 's' : ''} captured
        </div>
      </div>

      {/* Bottom status bar */}
      <div className="absolute bottom-0 left-0 right-0 px-4 py-2 flex items-end justify-between
                      bg-gradient-to-t from-black/70 to-transparent pointer-events-none z-20">
        {/* Camera position */}
        <div className="font-mono text-xs text-white/70 space-y-0.5">
          {pos && (
            <div>pos [{pos.x.toFixed(2)}, {pos.y.toFixed(2)}, {pos.z.toFixed(2)}]</div>
          )}
          {rot && (
            <div>rot [{(rot.x * 180/Math.PI).toFixed(1)}°, {(rot.y * 180/Math.PI).toFixed(1)}°, {(rot.z * 180/Math.PI).toFixed(1)}°]</div>
          )}
        </div>

        {/* Controls reference */}
        <div className="text-right font-mono text-xs text-white/50 space-y-0.5">
          <div><span className="text-white/80">W A S D</span> move  <span className="text-white/80">Q E</span> height</div>
          <div><span className="text-white/80">SHIFT</span> fast  <span className="text-white/80">DRAG</span> look</div>
          <div><span className="text-green-400 font-bold">R</span> capture view</div>
        </div>
      </div>

      {/* Capture confirmation badge */}
      {isFlashing && (
        <div className="absolute top-12 right-4 bg-green-500 text-white text-xs font-mono px-3 py-1 rounded-full z-30">
          View captured ✓
        </div>
      )}
    </>
  );
}
```

- [ ] **Step 2: Captured view list sidebar**

```tsx
// frontend/src/components/Navigator/CapturedViewList.tsx
import type { CapturedView } from '../../types';

interface CapturedViewListProps {
  views:          CapturedView[];
  onSelectView?:  (view: CapturedView) => void;
}

export function CapturedViewList({ views, onSelectView }: CapturedViewListProps) {
  if (views.length === 0) {
    return (
      <div className="p-3 text-xs text-slate-500 text-center">
        Press <kbd className="bg-slate-700 text-green-400 px-1 rounded">R</kbd> to capture views
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-1 p-2 overflow-y-auto max-h-64">
      <div className="text-xs text-slate-400 px-1 mb-1">Captured views ({views.length})</div>
      {views.map((view) => (
        <button
          key={view.view_id}
          onClick={() => onSelectView?.(view)}
          className="flex items-center gap-2 p-1.5 rounded hover:bg-slate-700 text-left transition-colors"
        >
          <img
            src={view.thumbnail}
            alt={view.view_id}
            className="w-14 h-8 object-cover rounded border border-slate-600 shrink-0"
          />
          <div className="min-w-0">
            <div className="text-xs text-white font-mono">{view.view_id}</div>
            <div className="text-xs text-slate-500 truncate font-mono">
              [{view.position.map(v => v.toFixed(1)).join(', ')}]
            </div>
          </div>
        </button>
      ))}
    </div>
  );
}
```

- [ ] **Step 3: Main Navigator component**

```tsx
// frontend/src/components/Navigator/Navigator.tsx
/**
 * Professional 3DGS Navigator.
 * Loads a PLY via Spark.js, provides FPS controls, captures views on R-press.
 *
 * Reference: https://github.com/sparkjsdev/spark
 */
import { useRef, useEffect, useCallback } from 'react';
import { useSparkScene } from './useSparkScene';
import { useFPSControls } from './useFPSControls';
import { useViewCapture } from './useViewCapture';
import { HUD } from './HUD';
import { CapturedViewList } from './CapturedViewList';
import { useSceneStore } from '../../store/sceneStore';

interface NavigatorProps {
  plyUrl:   string | null;
  sceneId:  string | null;
  onReady?: () => void;
}

export function Navigator({ plyUrl, sceneId, onReady }: NavigatorProps) {
  const canvasRef     = useRef<HTMLCanvasElement>(null);
  const animFrameRef  = useRef<number>(0);
  const capturedViews = useSceneStore(s => s.capturedViews);

  const { renderer, scene, camera, ready } = useSparkScene(canvasRef, plyUrl);
  const { tick }        = useFPSControls(camera, canvasRef.current, !!plyUrl && ready);
  const { isFlashing }  = useViewCapture(
    camera    ? camera    : null,
    renderer  ? renderer  : null,
    scene,
    canvasRef.current,
    !!plyUrl && ready,
  );

  // Animation loop
  const animate = useCallback(() => {
    tick();
    if (renderer && scene && camera) {
      renderer.render(scene, camera);
    }
    animFrameRef.current = requestAnimationFrame(animate);
  }, [tick, renderer, scene, camera]);

  useEffect(() => {
    animFrameRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animFrameRef.current);
  }, [animate]);

  // Resize handler
  useEffect(() => {
    const handleResize = () => {
      if (!canvasRef.current || !renderer || !camera) return;
      const w = canvasRef.current.clientWidth;
      const h = canvasRef.current.clientHeight;
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    };
    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, [renderer, camera]);

  useEffect(() => {
    if (ready) onReady?.();
  }, [ready, onReady]);

  return (
    <div className="relative w-full h-full bg-black select-none overflow-hidden">
      {/* 3DGS Canvas */}
      <canvas
        ref={canvasRef}
        className="w-full h-full block cursor-crosshair"
        tabIndex={0}
      />

      {/* HUD Overlay */}
      <HUD
        camera={camera ?? null}
        isFlashing={isFlashing}
        captureCount={capturedViews.length}
        isReady={ready}
      />

      {/* No scene loaded state */}
      {!plyUrl && (
        <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-950 z-10">
          <div className="text-4xl mb-4">✦</div>
          <div className="text-white text-lg font-semibold mb-2">SemanticSplat Navigator</div>
          <div className="text-slate-400 text-sm">Load a PLY scene to begin</div>
        </div>
      )}

      {/* Captured views floating panel */}
      {capturedViews.length > 0 && (
        <div className="absolute top-14 right-3 w-52 bg-slate-900/95 backdrop-blur border border-slate-700
                        rounded-lg overflow-hidden z-20 shadow-xl">
          <CapturedViewList views={capturedViews} />
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/Navigator/
git commit -m "feat: professional Spark.js Navigator — FPS controls, HUD, R-capture, captured view sidebar"
```

---

## Task 14: Tree Visualizer (D3.js)

**Files:**
- Create: `frontend/src/components/TreeVisualizer/useTreeLayout.ts`
- Create: `frontend/src/components/TreeVisualizer/TreeVisualizer.tsx`

- [ ] **Step 1: D3 layout hook**

```typescript
// frontend/src/components/TreeVisualizer/useTreeLayout.ts
import { useEffect } from 'react';
import * as d3 from 'd3';
import type { TreeNode } from '../../types';

const NODE_COLORS: Record<string, string> = {
  internal: '#8b5cf6',
  cluster:  '#3b82f6',
  leaf:     '#64748b',
};

export function useTreeLayout(
  svgRef:         React.RefObject<SVGSVGElement>,
  data:           TreeNode | null,
  width:          number,
  height:         number,
  highlightedIds: Set<string>,
  prunedIds:      Set<string>,
  onNodeClick:    (node: TreeNode) => void,
) {
  useEffect(() => {
    if (!svgRef.current || !data) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const margin = { top: 30, right: 220, bottom: 30, left: 180 };
    const W = width  - margin.left - margin.right;
    const H = height - margin.top  - margin.bottom;

    // Zoom + pan
    const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`);
    svg.call(
      d3.zoom<SVGSVGElement, unknown>()
        .scaleExtent([0.05, 4])
        .on('zoom', (e) => g.attr('transform', e.transform))
    );

    const root = d3.hierarchy<TreeNode>(data, d => d.children);
    const treeLayout = d3.tree<TreeNode>().size([H, W]).nodeSize([22, W / (root.height + 1)]);
    treeLayout(root);

    // Links
    g.selectAll<SVGPathElement, d3.HierarchyPointLink<TreeNode>>('.link')
      .data(root.links())
      .join('path')
      .attr('class', 'link')
      .attr('fill', 'none')
      .attr('stroke-width', d =>
        highlightedIds.has(d.target.data.id) ? 2.5 : 0.8
      )
      .attr('stroke', d => {
        const id = d.target.data.id;
        if (highlightedIds.has(id)) return '#22d3ee';
        if (prunedIds.has(id))      return '#f87171';
        return '#334155';
      })
      .attr('d', d3.linkHorizontal<
        d3.HierarchyPointLink<TreeNode>,
        d3.HierarchyPointNode<TreeNode>
      >().x(d => d.y).y(d => d.x));

    // Node groups
    const node = g.selectAll<SVGGElement, d3.HierarchyPointNode<TreeNode>>('.node')
      .data(root.descendants())
      .join('g')
      .attr('class', 'node')
      .attr('transform', d => `translate(${d.y},${d.x})`)
      .style('cursor', 'pointer')
      .on('click', (_, d) => onNodeClick(d.data));

    // Node circle
    node.append('circle')
      .attr('r', d => d.data.node_type === 'internal' ? 9 : 6)
      .attr('fill', d => {
        const id = d.data.id;
        if (highlightedIds.has(id)) return '#22d3ee';
        if (prunedIds.has(id))      return '#f87171';
        return NODE_COLORS[d.data.node_type] ?? '#64748b';
      })
      .attr('stroke', '#0f172a')
      .attr('stroke-width', 2)
      .attr('filter', d => highlightedIds.has(d.data.id) ? 'url(#glow)' : '');

    // Glow filter for highlighted nodes
    const defs = svg.append('defs');
    const filter = defs.append('filter').attr('id', 'glow');
    filter.append('feGaussianBlur').attr('stdDeviation', '3').attr('result', 'coloredBlur');
    const feMerge = filter.append('feMerge');
    feMerge.append('feMergeNode').attr('in', 'coloredBlur');
    feMerge.append('feMergeNode').attr('in', 'SourceGraphic');

    // Label
    node.append('text')
      .attr('dy', '0.31em')
      .attr('x', d => d.children ? -13 : 10)
      .attr('text-anchor', d => d.children ? 'end' : 'start')
      .attr('fill', d => highlightedIds.has(d.data.id) ? '#22d3ee' : '#cbd5e1')
      .attr('font-size', '10px')
      .attr('font-family', 'ui-monospace, monospace')
      .text(d => d.data.name.slice(0, 28));

    // View count badge
    node.filter(d => d.data.num_views > 0).append('text')
      .attr('dy', '0.31em')
      .attr('x', d => d.children ? -13 : 10 + d.data.name.slice(0, 28).length * 6 + 8)
      .attr('text-anchor', d => d.children ? 'end' : 'start')
      .attr('fill', '#475569')
      .attr('font-size', '9px')
      .text(d => `(${d.data.num_views})`);

    // Tooltip
    node.append('title').text(d => `${d.data.name}\n${d.data.summary}`);

  }, [data, width, height, highlightedIds, prunedIds, onNodeClick, svgRef]);
}
```

- [ ] **Step 2: TreeVisualizer component**

```tsx
// frontend/src/components/TreeVisualizer/TreeVisualizer.tsx
import { useRef, useEffect, useState } from 'react';
import { useTreeStore } from '../../store/treeStore';
import { useTreeLayout } from './useTreeLayout';
import type { TreeNode } from '../../types';

export function TreeVisualizer() {
  const svgRef       = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [dims, setDims] = useState({ width: 900, height: 500 });

  const { treeData, selectedNode, highlightedIds, prunedIds, selectNode } = useTreeStore();

  useEffect(() => {
    if (!containerRef.current) return;
    const ro = new ResizeObserver(([e]) =>
      setDims({ width: e.contentRect.width, height: e.contentRect.height })
    );
    ro.observe(containerRef.current);
    return () => ro.disconnect();
  }, []);

  useTreeLayout(svgRef, treeData, dims.width, dims.height,
    highlightedIds, prunedIds, (n: TreeNode) => selectNode(n));

  return (
    <div ref={containerRef} className="relative w-full h-full bg-slate-950 overflow-hidden">

      {/* Legend */}
      <div className="absolute top-2 left-2 z-10 flex gap-3 text-xs text-slate-400 bg-slate-900/80 px-2 py-1 rounded">
        {[
          { color: '#8b5cf6', label: 'Zone' },
          { color: '#3b82f6', label: 'Cluster' },
          { color: '#64748b', label: 'View' },
          { color: '#22d3ee', label: 'Visited' },
          { color: '#f87171', label: 'Pruned' },
        ].map(({ color, label }) => (
          <span key={label} className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full inline-block" style={{ background: color }} />
            {label}
          </span>
        ))}
      </div>

      {!treeData && (
        <div className="absolute inset-0 flex items-center justify-center text-slate-600 text-sm">
          Tree not built yet — use Cursor AI to build the semantic tree via MCP tools
        </div>
      )}

      <svg ref={svgRef} width={dims.width} height={dims.height} />

      {/* Node detail panel */}
      {selectedNode && (
        <div className="absolute bottom-2 right-2 w-72 bg-slate-800/95 backdrop-blur border border-slate-700
                        rounded-lg p-3 text-xs shadow-xl">
          <div className="flex items-center gap-2 mb-1">
            <span className={`px-1.5 py-0.5 rounded text-xs font-mono ${
              selectedNode.node_type === 'internal' ? 'bg-violet-900 text-violet-300' :
              selectedNode.node_type === 'cluster'  ? 'bg-blue-900 text-blue-300' :
                                                      'bg-slate-700 text-slate-300'
            }`}>{selectedNode.node_type}</span>
            <span className="font-semibold text-white">{selectedNode.name}</span>
          </div>
          <p className="text-slate-300 mb-2 leading-relaxed">{selectedNode.summary}</p>
          <div className="text-slate-500 font-mono">
            depth: {selectedNode.depth} · views: {selectedNode.num_views}
            {selectedNode.spatial_centroid && (
              <> · centroid [{selectedNode.spatial_centroid.map(v => v.toFixed(1)).join(', ')}]</>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/TreeVisualizer/
git commit -m "feat: D3.js tree visualizer — glow on visited, red for pruned, node detail panel"
```

---

## Task 15: Query Flow Panel

**Files:**
- Create: `frontend/src/components/QueryFlow/QueryFlow.tsx`

- [ ] **Step 1: Implement query flow panel**

```tsx
// frontend/src/components/QueryFlow/QueryFlow.tsx
/**
 * Query input + real-time traversal event log.
 *
 * Note: The actual query traversal intelligence is performed by Cursor AI
 * using MCP tools. This panel displays events that Cursor AI emits as it
 * traverses the tree, and shows the final 3D result.
 *
 * Cursor AI workflow for a query:
 *   1. Call get_root_node(scene_id)
 *   2. Call get_children(scene_id, root_id) → read summaries
 *   3. Decide which children to descend (TRAVERSAL_STEP_PROMPT)
 *   4. Repeat until leaf reached
 *   5. Call get_view_analysis(scene_id, view_id) → confirm match
 *   6. Call unproject_bbox(scene_id, view_id, bbox_2d) → 3D bbox
 */
import { useState } from 'react';
import { useQueryStore } from '../../store/queryStore';
import { useTreeStore } from '../../store/treeStore';

const EVENT_ICON: Record<string, string> = {
  visit:        '👁',
  descend:      '↘',
  pruned:       '✕',
  selected:     '✓',
  result:       '📍',
};

const EVENT_COLOR: Record<string, string> = {
  visit:        'text-cyan-400',
  descend:      'text-blue-400',
  pruned:       'text-red-400',
  selected:     'text-green-400',
  result:       'text-green-300 font-semibold',
};

export function QueryFlow() {
  const [input, setInput] = useState('');
  const { isRunning, events, resultBbox3d, resultViewId } = useQueryStore();
  const { resetHighlights } = useTreeStore();
  const { reset } = useQueryStore();

  const handleReset = () => {
    reset();
    resetHighlights();
    setInput('');
  };

  return (
    <div className="flex flex-col h-full gap-3">
      {/* Instruction banner */}
      <div className="bg-slate-800 border border-slate-700 rounded-lg p-2 text-xs text-slate-400">
        Ask Cursor AI to search the scene using the MCP tools:
        <code className="block mt-1 text-cyan-400 font-mono">
          query_scene("{'{your query}'}")
        </code>
      </div>

      {/* Manual query input (for display / future WebSocket integration) */}
      <div className="flex gap-2">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder='e.g. "find the red chair near the window"'
          className="flex-1 px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white text-xs
                     placeholder:text-slate-500 focus:outline-none focus:border-cyan-500"
        />
        <button
          onClick={handleReset}
          className="px-3 py-2 bg-slate-700 hover:bg-slate-600 text-slate-300 text-xs rounded-lg transition-colors"
        >
          Reset
        </button>
      </div>

      {/* Result card */}
      {resultBbox3d && (
        <div className="bg-green-950/60 border border-green-700 rounded-lg p-3 text-xs">
          <div className="text-green-300 font-semibold mb-1">
            ✓ Found — View: {resultViewId}
          </div>
          <div className="text-green-200 font-mono space-y-0.5">
            <div>center: [{resultBbox3d.center.map(v => v.toFixed(2)).join(', ')}] m</div>
            <div>size:   [{resultBbox3d.dimensions.map(v => v.toFixed(2)).join(', ')}] m</div>
          </div>
        </div>
      )}

      {/* Traversal event log */}
      <div className="flex-1 overflow-y-auto bg-slate-900 rounded-lg border border-slate-800 p-2 space-y-0.5 font-mono">
        {events.length === 0 && (
          <div className="text-slate-600 text-xs text-center py-6">
            Traversal events will appear here as Cursor AI navigates the tree
          </div>
        )}
        {events.map((event, i) => (
          <div key={i} className={`flex items-start gap-2 text-xs ${EVENT_COLOR[event.event] ?? 'text-slate-400'}`}>
            <span className="shrink-0 w-4 text-center">{EVENT_ICON[event.event] ?? '·'}</span>
            <span className="opacity-50">[{event.event}]</span>
            <span className="truncate">{event.name ?? event.matched_object ?? ''}</span>
            {event.confidence && <span className="ml-auto opacity-50 shrink-0">{event.confidence}</span>}
          </div>
        ))}
        {isRunning && (
          <div className="flex items-center gap-2 text-cyan-500 text-xs">
            <span className="w-3 h-3 border border-cyan-500 border-t-transparent rounded-full animate-spin" />
            Traversing...
          </div>
        )}
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/components/QueryFlow/
git commit -m "feat: QueryFlow panel — Cursor AI instruction banner, event log, 3D result card"
```

---

## Task 16: Control Panel and Main App Layout

**Files:**
- Create: `frontend/src/components/ControlPanel/ControlPanel.tsx`
- Modify: `frontend/src/App.tsx`
- Modify: `frontend/src/main.tsx`

- [ ] **Step 1: Control panel**

```tsx
// frontend/src/components/ControlPanel/ControlPanel.tsx
import { useState } from 'react';
import { sceneApi, treeApi } from '../../api/client';
import { useSceneStore } from '../../store/sceneStore';
import { useTreeStore } from '../../store/treeStore';
import type { TreeNode } from '../../types';

export function ControlPanel() {
  const [plyUrl,    setPlyUrl]    = useState('');
  const [sceneId,   setSceneId]   = useState('');
  const [status,    setStatus]    = useState('');
  const [loading,   setLoading]   = useState(false);
  const { setScene, setInfo }     = useSceneStore();
  const { setTreeData }           = useTreeStore();

  const handleInitScene = async () => {
    if (!sceneId) { setStatus('Enter a scene ID first'); return; }
    setLoading(true);
    setStatus('Initializing scene...');
    try {
      const { data } = await sceneApi.init(sceneId);
      setInfo(data as any);
      setScene(sceneId, plyUrl);
      setStatus(`Scene initialized. Start navigating and press R to capture views.`);
    } catch (e: any) {
      setStatus(`Error: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleLoadTree = async () => {
    if (!sceneId) return;
    setStatus('Loading tree from disk...');
    try {
      const { data } = await treeApi.getViz(sceneId);
      setTreeData(data as TreeNode);
      setStatus('Tree loaded into visualizer.');
    } catch (e: any) {
      setStatus(`Tree not built yet. Use Cursor AI MCP tools to build it.`);
    }
  };

  return (
    <div className="flex flex-col gap-3 text-sm">
      <div className="text-white font-semibold text-sm border-b border-slate-700 pb-2">Scene Setup</div>

      <div className="space-y-2">
        <label className="text-xs text-slate-400">Scene ID</label>
        <input
          value={sceneId} onChange={e => setSceneId(e.target.value)}
          placeholder="e.g. apartment_01"
          className="w-full px-2 py-1.5 bg-slate-800 border border-slate-600 rounded text-white text-xs
                     placeholder:text-slate-500 focus:outline-none focus:border-blue-500"
        />
      </div>

      <div className="space-y-2">
        <label className="text-xs text-slate-400">PLY URL (served locally or remote)</label>
        <input
          value={plyUrl} onChange={e => setPlyUrl(e.target.value)}
          placeholder="http://localhost:8080/scene.ply"
          className="w-full px-2 py-1.5 bg-slate-800 border border-slate-600 rounded text-white text-xs
                     placeholder:text-slate-500 focus:outline-none focus:border-blue-500"
        />
      </div>

      <button
        onClick={handleInitScene} disabled={loading}
        className="py-2 bg-blue-700 hover:bg-blue-600 disabled:opacity-40 text-white rounded text-xs transition-colors"
      >
        {loading ? 'Initializing...' : 'Init Scene + Load Navigator'}
      </button>

      <div className="border-t border-slate-700 pt-2 space-y-2">
        <div className="text-xs text-slate-400">After capturing views + building tree via Cursor AI:</div>
        <button
          onClick={handleLoadTree}
          className="w-full py-1.5 bg-slate-700 hover:bg-slate-600 text-white rounded text-xs transition-colors"
        >
          Load Tree Visualizer
        </button>
      </div>

      {status && (
        <div className="text-xs text-slate-400 bg-slate-800/50 rounded p-2 leading-relaxed">
          {status}
        </div>
      )}

      {/* MCP workflow guide */}
      <div className="border-t border-slate-700 pt-2">
        <div className="text-xs text-slate-500 space-y-1">
          <div className="text-slate-400 font-medium mb-1">Cursor AI Workflow</div>
          <div>1. Capture views (R key)</div>
          <div>2. AI: <code className="text-cyan-400">get_unanalyzed_views</code></div>
          <div>3. AI: <code className="text-cyan-400">get_view_image</code> → analyze → <code className="text-cyan-400">save_view_analysis</code></div>
          <div>4. AI: <code className="text-cyan-400">get_spatial_clusters</code></div>
          <div>5. AI: build tree → <code className="text-cyan-400">save_node</code></div>
          <div>6. AI: <code className="text-cyan-400">query_scene</code></div>
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Main App**

```tsx
// frontend/src/App.tsx
import { useSceneStore } from './store/sceneStore';
import { useTreeStore } from './store/treeStore';
import { Navigator } from './components/Navigator/Navigator';
import { TreeVisualizer } from './components/TreeVisualizer/TreeVisualizer';
import { QueryFlow } from './components/QueryFlow/QueryFlow';
import { ControlPanel } from './components/ControlPanel/ControlPanel';
import { useQueryStore } from './store/queryStore';

export default function App() {
  const { sceneId, plyUrl, capturedViews, info } = useSceneStore();
  const { treeData } = useTreeStore();
  const { resultBbox3d } = useQueryStore();

  return (
    <div className="h-screen w-screen bg-slate-950 text-white flex flex-col overflow-hidden font-sans">

      {/* Top bar */}
      <header className="flex items-center gap-3 px-4 h-11 border-b border-slate-800 shrink-0 bg-slate-900">
        <span className="text-white font-bold tracking-tight">SemanticSplat</span>
        <span className="text-slate-500 text-xs">3DGS Semantic Navigator</span>
        <div className="ml-auto flex items-center gap-4 text-xs text-slate-400">
          {sceneId && <span>Scene: <span className="text-blue-400 font-mono">{sceneId}</span></span>}
          {capturedViews.length > 0 && <span>{capturedViews.length} captured</span>}
          {treeData && <span className="text-green-400">Tree ✓</span>}
        </div>
      </header>

      {/* Main layout */}
      <div className="flex flex-1 overflow-hidden">

        {/* Left sidebar — scene setup */}
        <aside className="w-60 border-r border-slate-800 p-3 overflow-y-auto shrink-0 bg-slate-900/50">
          <ControlPanel />
        </aside>

        {/* Center — navigator (top 60%) + tree (bottom 40%) */}
        <main className="flex-1 flex flex-col overflow-hidden">
          <div className="flex-1 min-h-0">
            <Navigator
              plyUrl={plyUrl}
              sceneId={sceneId}
            />
          </div>
          <div className="h-56 border-t border-slate-800 min-h-0 bg-slate-950">
            <TreeVisualizer />
          </div>
        </main>

        {/* Right sidebar — query flow */}
        <aside className="w-72 border-l border-slate-800 p-3 flex flex-col overflow-hidden shrink-0 bg-slate-900/50">
          <div className="text-xs font-semibold text-white mb-2 pb-2 border-b border-slate-700">
            Semantic Query
          </div>
          <QueryFlow />
        </aside>
      </div>
    </div>
  );
}
```

- [ ] **Step 3: Update main.tsx**

```tsx
// frontend/src/main.tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

- [ ] **Step 4: Start services and verify**

```bash
# Terminal 1: Backend API
conda activate semanticsplat
cd backend
uvicorn backend.api.server:app --reload --port 8000

# Terminal 2: MCP Server (for Cursor AI)
conda activate semanticsplat
cd backend
python -m backend.mcp.server

# Terminal 3: Frontend
cd frontend
npm run dev
```

Open `http://localhost:5173`. You should see the 3-panel layout.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/
git commit -m "feat: complete frontend — Navigator + TreeVisualizer + QueryFlow + App layout"
```

---

## Task 17: End-to-End Integration Test

- [ ] **Step 1: Verify R-key capture flow**

```
1. Open http://localhost:5173
2. Enter scene_id: "test_scene", PLY URL: "http://localhost:8080/scene.ply"
   (serve your PLY with: python -m http.server 8080 --directory /path/to/ply)
3. Click "Init Scene"
4. Navigate with WASD+QE+Shift+Mouse
5. Press R — see flash, thumbnail appears in sidebar
6. Check backend: GET http://localhost:8000/api/captures/test_scene
   Expected: {"frames": [{"view_id": "v001", ...}], "total": 1}
7. Check disk: backend/data/scenes/test_scene/images/v001.png should exist
8. Check disk: backend/data/scenes/test_scene/transforms.json should have the frame
```

- [ ] **Step 2: Verify MCP tools in Cursor AI**

In Cursor with the MCP server running, type in chat:

```
Call the MCP tool: list_scenes()
```
Expected: `{"scenes": [{"scene_id": "test_scene", "num_captured": N, ...}]}`

```
Call: get_unanalyzed_views("test_scene")
```
Expected: `{"to_analyze": ["v001", "v002", ...], "already_done": []}`

```
Call: get_view_image("test_scene", "v001")
```
Expected: Returns base64 image + analysis_prompt. Cursor AI should then describe the image.

- [ ] **Step 3: Verify full tree build via Cursor AI**

Ask Cursor AI:
> "Analyze all views in test_scene and build the semantic tree using MCP tools"

Cursor AI will:
1. `get_unanalyzed_views("test_scene")` → get list
2. For each view: `get_view_image` → analyze with vision → `save_view_analysis`
3. `get_spatial_clusters("test_scene")` → get components
4. For each cluster: `get_summaries_for_views` → decide groupings → `save_node`
5. Recurse until tree is complete

Then: `GET http://localhost:8000/api/tree/test_scene/viz` — tree should appear in the visualizer.

- [ ] **Step 4: Commit final state**

```bash
git add .
git commit -m "feat: complete SemanticSplat system — Spark.js navigator, Nerfstudio format, Cursor AI MCP pipeline"
```

---

## Self-Review Against Spec

### Spec Coverage Check

| Requirement | Task |
|---|---|
| PLY loading in browser | Task 10 (Spark.js SplatMesh) |
| Professional FPS navigation | Task 11 (WASD+QE+Shift+Mouse) |
| R-key view capture | Task 12 (useViewCapture) |
| RGB from WebGL canvas | Task 12 (toDataURL) |
| Depth from WebGL | Task 9 (DepthCapture, render target) |
| Nerfstudio JSON format | Tasks 2, 7 |
| No external LLM API | All MCP tools (zero API calls) |
| Cursor AI drives intelligence | Tasks 6, MCP tools return prompts |
| Spatial proximity graph | Task 4 |
| 3D unprojection | Task 4 |
| Tree node storage | Task 5 |
| MCP tools: scene lifecycle | Task 6 (init, info, list) |
| MCP tools: view analysis pipeline | Task 6 (get_view_image, save_analysis) |
| MCP tools: tree construction | Task 6 (get_spatial_clusters, save_node, get_children) |
| MCP tools: query infrastructure | Task 6 (unproject, merge, distances) |
| D3.js tree visualizer | Task 14 |
| Query flow panel | Task 15 |
| HUD overlay | Task 13 |
| Captured view thumbnails | Task 13 |
| End-to-end integration test | Task 17 |

### MCP Tool Count: 20 pure-infrastructure tools ✓
### No OpenAI imports anywhere ✓
### Spark.js used for all 3DGS rendering ✓
### Nerfstudio transforms.json is the camera data format ✓

---

**Plan complete and saved to `docs/archive/deprecated/superpowers_plans/2026-04-05-semantic-3dgs-navigator-plan.md`.**

Two execution options:

**1. Subagent-Driven (recommended)** — fresh subagent per task, review between tasks

**2. Inline Execution** — execute in this session with checkpoints

Which approach?
