# Design Document: SemanticSplat — Hierarchical VLM Scene Understanding over 3D Gaussian Splatting

**Date**: April 5, 2026
**Status**: Design — Awaiting Implementation Planning
**Target Venue**: CVPR / ICCV / NeurIPS (Top-tier CV / AI)

---

## Table of Contents

1. [Problem Statement and Motivation](#1-problem-statement-and-motivation)
2. [System Overview](#2-system-overview)
3. [Background and Key Technologies](#3-background-and-key-technologies)
4. [Component 1: NoField-Guided View Synthesis](#4-component-1-nofield-guided-view-synthesis)
5. [Component 2: VLM Per-View JSON Generation](#5-component-2-vlm-per-view-json-generation)
6. [Component 3: Hierarchical Tree Construction](#6-component-3-hierarchical-tree-construction)
7. [Component 4: Query Traversal and Retrieval](#7-component-4-query-traversal-and-retrieval)
8. [Component 5: 3D Output Generation](#8-component-5-3d-output-generation)
9. [System Architecture](#9-system-architecture)
10. [Experimental Design and Ablations](#10-experimental-design-and-ablations)
11. [Scalability Analysis](#11-scalability-analysis)
12. [Downstream Applications](#12-downstream-applications)
13. [Novelty Statement](#13-novelty-statement)
14. [Open Questions and Risks](#14-open-questions-and-risks)

---

## 1. Problem Statement and Motivation

### 1.1 The Core Problem

A 3D Gaussian Splatting (3DGS) model of a scene is a densely packed PLY file of millions of Gaussian primitives. It is excellent at photorealistic rendering but carries **no semantic information whatsoever**. Given a natural language query — *"find the painting with the crying woman near the entrance of Wing B"* or *"which room has a desk with a laptop near a window?"* — there is currently no principled way to answer it using 3DGS alone.

Existing approaches to semantic 3D scene understanding typically:

1. **Distill 2D features into 3D** (LERF, Semantic Gaussians): Attach CLIP/DINO embeddings to each Gaussian, then query by embedding similarity. Limited to short, keyword-like queries. Cannot handle compositional, multi-hop, or relational queries.

2. **Build explicit scene graphs from segmentation** (ConceptGraphs, BBQ): Detect 2D instances → lift to 3D → build graph. Depends heavily on segmentation quality; fails on novel or ambiguous object categories. Scene graph is shallow (typically 2 levels).

3. **Navigation-focused systems** (GaussNav, BEINGS): Use 3DGS as a background map for robot navigation goals. Not designed for open-ended semantic retrieval or complex linguistic queries.

**None of these systems:**
- Build a scene-agnostic, open-depth hierarchical semantic representation
- Use pure VLM understanding without explicit segmentation, clustering, or feature distillation
- Handle compositional queries (multi-constraint, spatial relations, functional reasoning) at scale
- Automatically determine the appropriate hierarchy depth and zone granularity from the scene itself

### 1.2 What We Want

A system that:

- Takes **any PLY file** as input (a single room, an apartment, a museum, an industrial site, a medical scan environment)
- Builds a **hierarchical semantic tree** of the scene offline, entirely from VLM understanding of rendered views
- Answers **arbitrary natural language queries** at inference time by traversing the tree with bounded context
- Outputs a **3D bounding box and/or camera pose** for spatial queries, or a **text answer** for descriptive queries
- **Scales gracefully** from 15 views (a small room) to 2,000+ views (a large building), with no change in algorithm

### 1.3 Why 3DGS Specifically?

3DGS has two unique properties that make it the ideal backend for this system:

1. **Photorealistic rendering**: Unlike raw point clouds, 3DGS renders images that VLMs can understand and describe just as they would describe a real photograph. This enables pure VLM understanding without explicit 3D feature extraction.

2. **Exact depth maps**: 3DGS can render pixel-accurate depth maps for any camera pose. This enables precise 3D localization from 2D VLM outputs — a 2D bounding box in a rendered view can be unprojected to a 3D bounding box in world coordinates with geometric exactness.

---

## 2. System Overview

### 2.1 Two Phases

The system operates in two distinct phases:

**Offline Construction Phase** (done once per scene):
```
PLY file
  → NoField: select K optimal camera poses
  → 3DGS: render K × (RGB image + depth map)
  → VLM: generate structured JSON description for each view
  → Tree Builder: recursively construct hierarchical semantic tree
  → Storage: persist tree as nested JSON / graph database
```

**Online Query Phase** (done per query, real-time):
```
Natural language query
  → LLM: decompose into structured query plan
  → Tree Traversal: top-down, pruning irrelevant branches
  → Leaf retrieval: read full JSON of selected views
  → 3D output: depth-unproject 2D bbox → 3D bbox
  → (Optional) Novel view synthesis: render canonical view of found object
```

### 2.2 Key Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Scene representation | PLY (3DGS) | Photorealistic rendering + exact depth maps |
| View selection | NoField | Optimal scene coverage, no manual camera placement |
| Semantic extraction | Pure VLM (no DINO, SAM, clustering) | Open-vocabulary, zero-shot, scene-agnostic |
| Structure determination | Fully LLM-driven recursion | No hardcoded rules, adapts to any scene type |
| Spatial pre-filtering | Camera proximity graph | Efficiency + prevents cross-room confusion |
| Query handling | Top-down tree traversal | Bounded context, compositional reasoning |
| 3D localization | Depth map unprojection | Geometrically exact, no 3D network needed |
| LLM integration | MCP server (Cursor IDE) | Local, no external API dependency |

---

## 3. Background and Key Technologies

### 3.1 3D Gaussian Splatting (3DGS)

3DGS represents a scene as a set of 3D Gaussian primitives, each defined by:
- **Position** μ ∈ ℝ³ (world coordinates)
- **Covariance** Σ ∈ ℝ³ˣ³ (shape and orientation)
- **Opacity** α ∈ [0,1]
- **Color** (spherical harmonics coefficients, view-dependent)

Rendering is done via differentiable rasterization: Gaussians are projected to 2D, sorted by depth, and alpha-composited. This renders at 100+ FPS and produces photorealistic images.

**Key capability for this system**: For any arbitrary camera pose (not necessarily one used during training), 3DGS can render:
- An RGB image indistinguishable from a real photograph
- A pixel-accurate depth map where `depth[x,y]` gives the world-space distance to the nearest Gaussian at pixel `(x,y)`

### 3.2 NoField (Neural Observation Field)

NoField is a camera placement optimization method that, given a 3DGS scene, finds a set of K camera poses that:
- Maximize **coverage**: every part of the scene is visible from at least one camera
- Maximize **observation quality**: avoid grazing angles, prefer frontal views
- Minimize **redundancy**: neighboring cameras don't see the exact same content

For our system, NoField serves as the automated viewpoint selection engine. We do not manually place cameras. NoField outputs K camera poses `{(p_i, R_i)}` where `p_i ∈ ℝ³` is the camera center and `R_i ∈ SO(3)` is the orientation.

**Importantly**: the output camera poses carry their 3D world positions. This geometric information is used by our spatial proximity graph (Section 6.2).

### 3.3 Vision-Language Models (VLMs)

VLMs (e.g., GPT-4V, Gemini 1.5, Claude 3.5) take an image and a text prompt as input and generate structured natural language descriptions. For our system, we prompt the VLM to:
- Identify all visible objects with approximate 2D bounding boxes
- Describe the type of space depicted
- Articulate spatial relationships between objects
- Provide a one-line summary of the entire view

The VLM receives **rendered 3DGS images** — photorealistic, clean, ideal viewing angles — rather than real captured images that may be blurry, poorly lit, or occluded. This improves VLM description quality.

### 3.4 MCP Server (Model Context Protocol)

The system uses an MCP server running locally to interface with the LLM. All LLM calls are routed through this server:
- No external API keys exposed in application code
- Consistent model configuration across all system components
- Can be swapped to a different LLM by changing only the server configuration

---

## 4. Component 1: NoField-Guided View Synthesis

### 4.1 Purpose

Select K camera poses from the 3DGS scene that provide maximum semantic coverage — every semantically meaningful part of the scene is seen clearly by at least one camera.

### 4.2 Input/Output

- **Input**: PLY file (3DGS model)
- **Output**: K camera poses `{(p_i, R_i, f_i)}` where `f_i` is the focal length

### 4.3 Process

NoField internally builds a "Neural Observation Field" that scores any camera pose by:
- How much unobserved scene volume it would cover
- The quality of observation (angle to surfaces, distance to objects)

It then runs an iterative greedy optimization:
1. Start with an empty camera set
2. Repeatedly add the camera pose with highest marginal coverage gain
3. Stop when coverage plateaus or K cameras are selected

For our system, K is not a fixed hyperparameter — it is determined by the scene:
- K ≈ 15–30 for a single room
- K ≈ 80–150 for an apartment
- K ≈ 500–2,000 for a museum or building

We set a **coverage threshold** (e.g., 95% of scene volume must be observed) and let NoField determine K automatically.

### 4.4 Depth Map Rendering

For each selected camera pose, 3DGS renders both:

**RGB image**: Standard 3DGS rasterization. Photorealistic, used by VLM.

**Depth map**: For each pixel `(x,y)`, the depth is computed as:
```
depth[x,y] = Σ_i (α_i · d_i · Π_{j<i}(1 - α_j))
```
where `d_i` is the distance from camera center to the i-th Gaussian's mean along the ray, and `α_i` is the blended opacity. This gives a **continuous, sub-pixel-accurate depth** map — not a discretized depth as from a RGBD sensor.

**Why exact depth maps matter**: When the VLM identifies an object at pixel `(x₁,y₁,x₂,y₂)` (2D bbox), we need to recover its 3D position precisely. The exact depth map enables this without any learned depth estimator or 3D neural network.

### 4.5 Example

For a museum PLY file, NoField might place:
- 45 cameras in the main hall (high object density)
- 12 cameras per gallery room × 8 rooms = 96 cameras
- 8 cameras in connecting corridors
- 15 cameras for large sculpture installations (need multiple angles)

Total: ~165 cameras for a medium-sized museum. All placed automatically.

---

## 5. Component 2: VLM Per-View JSON Generation

### 5.1 Purpose

For each rendered view, generate a richly structured JSON description containing all semantic information that will later power the tree and query system.

### 5.2 The VLM Prompt

```
You are analyzing a rendered view from a 3D scene. The image was rendered from 
a known camera position. Describe what you see in complete, structured detail.

Return a JSON object with exactly this structure:

{
  "view_id": "<view_id>",
  "scene_summary": "<one or two sentence description of what is visible>",
  "room_type": "<living_room|bedroom|kitchen|bathroom|corridor|ballroom|bar|reception|foyer|stage|back_of_house|service_area|lounge|outdoor|unknown>",
  "lighting": "<bright|dim|dark|natural|artificial|unknown>",
  "facing": "<stage|audience|entrance|exit|bar|reception|screen|wall|ceiling|window|unknown>",
  "visible_landmarks": ["<landmark name>", ...],
  "objects": [
    {
      "label": "<specific object name>",
      "bbox_2d": [x1, y1, x2, y2],   // pixel coordinates, normalized 0-1
      "confidence": 0.9, // 0.0 to 1.0
      "attributes": {
        "color": "<dominant color>",
        "material": "<material if discernible>",
        "size": "small|medium|large",
        "state": "<open|closed|on|off>",
        "location_description": "<e.g. on the table, near the window>"
      }
    }
  ],
  "spatial_relations": [
    "<subject> is <relation> <object>",
    // e.g., "lamp is to the left of the sofa"
    // e.g., "keys are on top of the coffee table"
  ],
  "functional_context": "<what this space is used for>"
}

Be exhaustive. Include every visible object, no matter how small.
For bbox_2d, use a step-by-step spatial reasoning process:
1. Horizontal: divide image into thirds (left/center/right).
2. Vertical: divide image into thirds (top/middle/bottom).
3. Refine to nearest 0.05.
4. Sanity check against spatial relations (e.g. "above the door" means y2 <= door's y1).
```

### 5.3 Example Output

For a living room view:

```json
{
  "view_id": "v042",
  "camera_pose": {"position": [2.1, 0.9, 1.4], "rotation_euler": [0, 0, -15]},
  "one_line_summary": "Wide living room shot, silver keys on glass coffee table near grey sofa",
  "space_type": "living room",
  "object_list": ["sofa", "coffee table", "keys", "remote control", "TV", "bookshelf", "lamp", "rug"],
  "objects": [
    {
      "label": "car keys",
      "bbox_2d": [340, 280, 380, 310],
      "confidence": "high",
      "attributes": {
        "color": "silver",
        "material": "metal",
        "size": "small",
        "condition": "normal"
      },
      "functional_description": "vehicle access and ignition keys"
    },
    {
      "label": "glass coffee table",
      "bbox_2d": [180, 310, 520, 480],
      "confidence": "high",
      "attributes": {
        "color": "transparent with chrome legs",
        "material": "glass and metal",
        "size": "medium",
        "condition": "clean"
      },
      "functional_description": "central surface for placing items in a seating area"
    },
    {
      "label": "grey fabric sofa",
      "bbox_2d": [10, 200, 640, 520],
      "confidence": "high",
      "attributes": {
        "color": "dark grey",
        "material": "fabric",
        "size": "large",
        "condition": "normal"
      },
      "functional_description": "seating for 3-4 people"
    }
  ],
  "spatial_relations": [
    "car keys are on top of the coffee table",
    "coffee table is in front of the sofa",
    "TV is mounted on the wall opposite the sofa",
    "lamp is to the right of the bookshelf",
    "rug is under the coffee table and sofa"
  ],
  "notable_features": "Silver car keys prominently visible on coffee table center",
  "visibility_quality": "clear"
}
```

### 5.4 Parallel Execution

All K VLM calls are independent and run in parallel. For K=200 views, with an average VLM call taking 3 seconds, parallel execution completes in ~3 seconds total (bounded by API rate limits, not computation). Serial execution would take 10 minutes.

### 5.5 The Scene Summary and Semantic Fields

The `scene_summary`, `room_type`, `facing`, and `visible_landmarks` fields are the most critical for tree construction. They must be:
- **Informative**: mention the most salient objects, architectural features, and functional type
- **Distinctive**: allow the LLM to distinguish this view from neighboring views

The tree construction algorithm (Section 6) operates almost entirely on these high-level semantic fields, combined with geometric proximity, to build the tree. Full object JSONs are primarily used at query time. This keeps the tree construction cost bounded and highly accurate.

---

## 6. Component 3: Hierarchical Tree Construction

### 6.1 Overview

Given K views with their VLM JSONs and camera positions, construct a hierarchical semantic tree where:
- **Leaf nodes** = individual views (with full JSON)
- **Internal nodes** = LLM-named semantic clusters (with aggregate summary)
- **Root node** = scene-level summary

The tree depth, node labels, grouping boundaries, and cluster sizes are **all determined by the LLM**. No hardcoded rules govern any of these.

### 6.2 Geometry Pre-Filtering: Two-Pass Spatial Clustering

Before any LLM call to build the tree, we group views into clusters. This prevents the LLM from confusing visually similar but physically distant areas (e.g., two identical bedrooms in different wings).

We use a two-pass clustering algorithm:

**Pass 1 — Geometric Proximity:**
```python
# Build K×K distance matrix from camera positions
D[i,j] = euclidean_distance(camera_pose[i].position, camera_pose[j].position)

# Adaptive threshold: scale with scene density
median_nn_dist = median([min(D[i, j!=i]) for i in range(K)])
threshold = median_nn_dist * scale_factor   # scale_factor ≈ 3.5

# Build proximity graph and find connected components
spatial_clusters = connected_components(proximity_graph)
```

**Pass 2 — Semantic Merge:**
Geometric clustering is fast but can artificially split a single large room (like a ballroom) if cameras are placed far apart (e.g., stage vs. audience). Pass 2 inspects the `room_type`, `facing`, and `visible_landmarks` fields of each view and merges geometrically separate clusters that belong to the same room.
A merge happens if:
- **Complementary facing:** One cluster faces "stage" and the other faces "audience".
- **Shared room_type + landmark:** Both clusters have the same dominant `room_type` and share at least one `visible_landmark` (e.g., both see the "projection screen").

### 6.3 The LLM Tree Grouping Pass

Instead of recursive calls, the LLM makes a single, comprehensive pass over the pre-computed clusters to determine names and hierarchy.

The LLM is prompted with the clusters and their view summaries, and instructed to perform three steps:

**Step 0 — Same-Room Check (Final Semantic Merge):**
The LLM applies a final layer of reasoning. Before naming any zones, it inspects cluster pairs. If they belong to the same physical space (e.g., a stage inside a ballroom), the LLM explicitly merges them.

**Step 1 — Naming & Summarizing Zones:**
For each final cluster, the LLM assigns a concise, human-readable name using real-world venue vocabulary (e.g., "Ballroom", "Lobby & Bar") and a one-sentence summary.

**Step 2 — Optional Sub-Grouping:**
If a zone is large and contains genuinely distinct functional sub-areas (e.g., a large ballroom with a distinct stage platform and audience seating), the LLM can create `region` sub-nodes. Otherwise, the zone directly contains the leaf views.

### 6.4 Why the LLM Has Final Say

While geometric and semantic heuristics do the heavy lifting of clustering, the LLM's final reasoning pass ensures that the resulting tree matches human expectations of spatial organization. No hardcoded rule can perfectly capture when a "bar" and "reception" should be combined into a "Lobby", but an LLM understands these architectural relationships effortlessly.

### 6.5 Detailed Tree Examples

**Example 1: Single Room (Office)**

```
K=18 views
Spatial proximity graph: 1 connected component (all cameras in same room)

build_tree(18 views):
  LLM: "YES — split into: Desk Area, Bookshelf Wall, Seating Area, Window Area"
  
  build_tree(Desk Area, 6 views):
    LLM: "YES — split into: Full Desk Overview (3 views), Monitor Close-up (2 views), Keyboard Detail (1 view)"
    
    build_tree(Full Desk Overview, 3 views):
      LLM: "NO — all three views show the same desk from left, center, right angles"
      → ClusterNode: "Full Desk Overview"
    
    build_tree(Monitor Close-up, 2 views):
      LLM: "NO — front and slight-angle view of same monitor"
      → ClusterNode: "Monitor Close-up"
    
    build_tree(Keyboard Detail, 1 view):
      → LeafNode: v_012
    
    → InternalNode: "Desk Area" (3 children)
  
  build_tree(Bookshelf Wall, 4 views):
    LLM: "YES — Top Shelves (2 views), Bottom Shelves (2 views)"
    ... recurse ...
    → InternalNode: "Bookshelf Wall"
  
  build_tree(Seating Area, 5 views):
    LLM: "NO — all views cover the same armchair and side table"
    → ClusterNode: "Seating Area"
  
  build_tree(Window Area, 3 views):
    LLM: "NO"
    → ClusterNode: "Window Area"
  
→ Root: "Office room with central desk, bookshelf wall, seating area, and window"
```

Final depth: 3 levels. LLM-determined.

---

**Example 2: Museum**

```
K=800 views
Spatial proximity graph: 12 connected components
  Component 1: Main Hall (80 views)
  Component 2: Wing A — Ancient Art (200 views)
  Component 3: Wing B — Modern Art (200 views)
  ... etc.

build_tree(Wing A — Ancient Art, 200 views):
  LLM: "YES — Egyptian Room (60v), Greek Room (70v), Roman Room (50v), Connecting Corridor (20v)"
  
  build_tree(Egyptian Room, 60 views):
    LLM: "YES — Sarcophagi Section (20v), Wall Paintings (25v), Artifact Cases (15v)"
    
    build_tree(Sarcophagi Section, 20 views):
      LLM: "YES — Ramesses II Sarcophagus (7v), Nefertiti Sarcophagus (6v), 
                   Unidentified Sarcophagus (4v), Room Overview (3v)"
      
      build_tree(Ramesses II Sarcophagus, 7 views):
        LLM: "YES — Full View (2v), Hieroglyphics Detail Left (2v), 
                     Lid Detail (2v), Base Inscription (1v)"
        
        build_tree(Full View, 2 views):
          LLM: "NO — same sarcophagus from front and slight angle"
          → ClusterNode: "Ramesses II Full View"
        
        ... etc.
      
      → InternalNode: "Ramesses II Sarcophagus" (4 children)
    
    → InternalNode: "Sarcophagi Section" (4 children)
  
  → InternalNode: "Egyptian Room" (4 children)

→ InternalNode: "Wing A — Ancient Art" (4 children)

Top-level build:
  12 spatial cluster subtrees
  LLM: "YES — combine into: Main Halls (1 component), 
               Wing A (components 2-3), Wing B (components 4-5),
               Wing C (components 6-8), Staff/Admin (components 9-12)"

→ Root: "Four-wing art museum with ancient, modern, and photography collections"
```

Final depth: 6 levels (Root → Wings → Rooms → Sections → Objects → Views). LLM-determined.

---

**Example 3: Single Object (Medical Imaging Context)**

```
K=12 views (close-up views of a knee joint model)
1 spatial component

build_tree(12 views):
  LLM: "YES — Anterior Region (3v), Posterior Region (3v), 
               Medial Region (3v), Lateral Region (3v)"
  
  build_tree(Anterior Region, 3 views):
    LLM: "YES — Patellar Area (2v), Quadriceps Tendon (1v)"
    
    build_tree(Patellar Area, 2 views):
      LLM: "NO — same structure from slightly different angles"
      → ClusterNode

→ Root: "Knee joint model, four anatomical regions"
```

Final depth: 3 levels. Same algorithm, smaller scale.

### 6.6 Node Data Structure

Every node in the tree stores:

```json
{
  "node_id": "node_0042",
  "node_type": "internal | cluster | leaf",
  "name": "Egyptian Room",
  "summary": "Room containing sarcophagi, wall paintings, and artifact cases from ancient Egypt",
  "depth": 2,
  "parent_id": "node_0010",
  "children_ids": ["node_0043", "node_0044", "node_0045"],

  // For leaf and cluster nodes only:
  "view_ids": ["v201", "v202"],
  "camera_positions": [[x,y,z], [x,y,z]],

  // For leaf nodes only:
  "full_json_ref": "views/v201.json",

  // Geometric properties (auto-computed from camera positions)
  "spatial_centroid": [x, y, z],
  "spatial_radius": 2.3,  // meters, bounding sphere of cameras in this node
  "spatial_bbox": [[xmin,ymin,zmin], [xmax,ymax,zmax]]
}
```

### 6.7 LLM Call Count Analysis

For a museum with K=800 views and depth=6:

| Level | Nodes processed | LLM calls |
|---|---|---|
| Top-level grouping | 1 call over 12 component summaries | 1 |
| Wing level | ~4 calls | 4 |
| Room level | ~16 calls | 16 |
| Section level | ~60 calls | 60 |
| Object level | ~200 calls | 200 |
| View cluster level | ~400 calls | 400 |
| **Total** | | **~681 calls** |

Each call uses ~500-2000 tokens (summaries only). Total: ~500K–1.4M tokens for tree construction.

This is a **one-time offline cost**, amortized over all queries ever run against this scene.

At $0.003 per 1K tokens (GPT-4o-mini), total construction cost ≈ **$1.50–$4.20 for an 800-view museum**.

---

## 7. Component 4: Query Traversal and Retrieval

### 7.1 Overview

Given a natural language query, traverse the semantic tree top-down, pruning irrelevant branches at each level, to reach the 1-3 most relevant leaf views. Then read their full JSONs to extract the precise answer.

**Total LLM calls at query time**: `depth + 2` (one per level + decomposition + leaf confirmation).
For depth=3 (apartment): **5 calls**.
For depth=6 (museum): **8 calls**.

### 7.2 Step 1: Query Decomposition

Before traversal, the LLM analyzes the query to produce a structured plan:

```
LLM prompt:
  "Analyze this query for a 3D scene search system.
   Query: '{query}'
   
   Extract:
   - target: the primary object or subject being sought
   - location_constraints: explicit spatial scope mentioned in the query
   - attribute_constraints: color, size, material, style, etc.
   - relational_constraints: spatial relationships (near X, on top of Y, to the left of Z)
   - functional_constraints: what the object is used for
   - query_type: one of [object_finding, descriptive, aggregation, cross_zone_geometric, spatial_relation]
   - output_type: one of [3d_bbox, camera_pose, text_answer, count]
   
   Return JSON."
```

**Examples**:

Query: `"find the silver keys on the coffee table in the living room"`
```json
{
  "target": "silver keys",
  "location_constraints": "living room, on coffee table",
  "attribute_constraints": {"color": "silver"},
  "relational_constraints": ["on top of coffee table"],
  "functional_constraints": null,
  "query_type": "object_finding",
  "output_type": "3d_bbox"
}
```

Query: `"which room has a natural light source?"`
```json
{
  "target": "natural light source (window, skylight, glass door)",
  "location_constraints": null,
  "attribute_constraints": null,
  "relational_constraints": null,
  "functional_constraints": "admits natural daylight",
  "query_type": "descriptive",
  "output_type": "text_answer"
}
```

Query: `"find the painting with the crying woman near the entrance of Wing B"`
```json
{
  "target": "painting depicting a crying or grieving woman",
  "location_constraints": "Wing B, near entrance",
  "attribute_constraints": {"subject": "crying woman", "medium": "painting"},
  "relational_constraints": ["near entrance of Wing B"],
  "functional_constraints": null,
  "query_type": "object_finding",
  "output_type": "3d_bbox"
}
```

### 7.3 Step 2: Top-Down Traversal

At each level, the LLM reads the **summaries of all children** of the current node and decides which to descend into.

**Traversal prompt** (applied at every internal node):

```
You are navigating a scene hierarchy to answer:
  "{original_query}"

Query plan: {structured_plan}

Current node: "{current_node_name}"
Summary: "{current_node_summary}"

Children nodes:
  [node_A]: {summary_A}
  [node_B]: {summary_B}
  [node_C]: {summary_C}
  ...

Which children are potentially relevant to answering this query?
- Include a child if it MIGHT contain the answer (be conservative — don't prune if uncertain)
- Exclude a child only if it is CLEARLY irrelevant
- If NO children are relevant, return an empty list (the target does not exist in this branch)

Return JSON: {"descend_into": ["node_A", "node_C"], "reasoning": "<one sentence>"}
```

**Example traversal** for `"find the silver keys on the coffee table in the living room"`:

```
Level 0 — Root
  Children: [Ground Floor, Upper Floor]
  Summaries:
    Ground Floor: "Open-plan kitchen-living area and hallway"
    Upper Floor: "Two bedrooms and study"
  → Descend into: [Ground Floor]
  → Reasoning: "Query specifies living room, which is on ground floor"

Level 1 — Ground Floor
  Children: [Kitchen Zone, Living Room Zone, Hallway Zone]
  Summaries:
    Kitchen Zone: "Countertops, fridge, microwave, cooking area"
    Living Room Zone: "Sofa, coffee table, TV, bookshelf; keys noted on table"
    Hallway Zone: "Corridor connecting rooms, coat rack, shoe rack"
  → Descend into: [Living Room Zone]
  → Reasoning: "Query explicitly mentions living room; keys visible in summary"

Level 2 — Living Room Zone
  Children: [v042, v047, v053, v061, v065]
  Summaries:
    v042: "Wide shot, sofa central, silver keys on coffee table, TV visible"
    v047: "Bookshelf corner, lamp, books, no coffee table"
    v053: "Sofa side angle, partial coffee table, no keys visible"
    v061: "Coffee table close-up, keys and remote clearly visible"
    v065: "TV wall view, no coffee table"
  → Descend into: [v042, v061]
  → Reasoning: "v042 has full context; v061 has clearest close-up of the keys"
```

### 7.4 Step 3: Leaf Confirmation and Extraction

At the selected leaf views, read the full JSON and confirm the match using a spatial reasoning Chain-of-Thought (CoT). Depending on the `query_type`, the system either stops after a few matches (`object_finding`) or checks every view (`aggregation`).

```
LLM prompt:
  "Query: '{query}'
  
  Here is the full description of view {view_id}:
  {full_json}
  
  1. Does this view contain the queried object/subject? (yes/no/partial)
  2. If yes: derive a PRECISE bbox_2d using spatial reasoning.
     DO NOT blindly copy bbox_2d numbers from the JSON.
     a) Identify matched object and location_description.
     b) Horizontal thirds (left/center/right) -> x1, x2
     c) Vertical thirds (top/middle/bottom) -> y1, y2
     d) Sanity check against spatial_relations (e.g. 'above door' -> y2 <= door's y1)
  3. Rate confidence: high/medium/low
  
  Return JSON: {"found": bool, "bbox_2d": [x1,y1,x2,y2], "confidence": str, "matched_object": str, "bbox_reasoning": str}"
```

### 7.5 Step 4: Two-Stage Bbox Refinement and Ranking

For any view where the object is found, the system performs a **Crop-and-Requery Refinement** (Step C2):
1. The image is cropped around the rough CoT `bbox_2d` (with padding).
2. The cropped image and a refinement prompt are sent to the VLM.
3. The VLM returns a tight bounding box within the crop.
4. The coordinates are mapped back to the original full image.
5. The pipeline logs this final, refined `bbox_2d`.

Finally, the results from all checked views are **Ranked** (Step C4):
The system scores each positive result based on:
- Confidence level (50%)
- BBox area (30%, preferring objects that fill a reasonable portion of the frame)
- BBox centrality (20%, preferring well-framed objects)

For `object_finding` queries, only the single best-ranked view is presented to the user. For `aggregation` queries, all positive views are presented, sorted by score.

### 7.6 Handling All Query Types

#### Type A: Simple Object Finding
> "Find the red chair"

Standard traversal. At leaf: match `label` and `attributes.color` in JSON.

---

#### Type B: Attribute-Based Queries
> "Find the worn leather armchair"

Query plan attributes: `{material: leather, condition: worn, type: armchair}`.
At each traversal level, prune zones whose summaries don't mention leather furniture.
At leaf level: match `objects[].attributes.material == "leather"` and `condition == "worn"`.

---

#### Type C: Spatial Relation Queries
> "Find the object to the left of the sofa"

Two-pass process:
1. First traversal: find views where sofa is visible and well-centered
2. In those views' JSONs: scan `spatial_relations` for `"<X> is to the left of sofa"`
3. If not found in `spatial_relations`: use bounding box geometry — find objects whose `bbox_2d` center_x < sofa `bbox_2d` center_x

---

#### Type D: Multi-Constraint Zone Queries
> "Find a room with both a fireplace and a piano"

At each zone-level node, the traversal prompt checks both constraints simultaneously:
- Prune zones whose summaries mention neither
- Keep zones whose summaries mention at least one (might contain both)
- At leaf level: confirm both are present in the same view JSON's `object_list`

---

#### Type E: Cross-Zone Geometric Queries
> "Find the nearest bathroom to the master bedroom"

1. Traverse tree to find all nodes named "bathroom" → collect their `spatial_centroid`
2. Traverse tree to find node named "master bedroom" → get its `spatial_centroid`
3. Compute Euclidean distance between centroids in 3D world space (pure geometry, no LLM)
4. Return bathroom with smallest distance
5. Output: camera pose of the bathroom's best overview view

---

#### Type F: Functional/Contextual Queries
> "Where can I charge my phone?"

LLM query expansion before traversal:
`→ ["power outlet", "USB charging port", "wireless charging pad", "extension cord", "laptop dock", "charging station"]`

Traversal proceeds with expanded term set. Zone-level summaries are checked for any of these terms. Broader descent due to lower precision of functional queries.

---

#### Type G: Aggregation Queries
> "How many chairs are in this apartment?"

Full tree scan (no pruning):
1. Collect all leaf views where `"chair"` appears in `object_list`
2. For each matching view, get the `bbox_2d` of all chairs → unproject to 3D bbox
3. Merge overlapping 3D bboxes (IoU > 0.5 in 3D) → unique instances
4. Return count + list of unique instance locations

This is the one O(K) query type. The IoU deduplication is geometric, adding no extra LLM calls.

---

#### Type H: Comparative Queries
> "Which room is brighter?"

For each zone node: read the `visibility_quality` and `notable_features` fields of child view JSONs. Aggregate lighting descriptors. LLM compares across zones and returns ranking.

---

### 7.6 Ambiguity Resolution

When multiple candidates are found:

```
Query: "find the keys"
Found: 
  - silver car keys on coffee table (Living Room, v042, confidence: high)
  - apartment key bundle on kitchen hook (Kitchen, v011, confidence: high)

Response to user:
  "Found 2 matches:
   (1) Silver car keys on glass coffee table in the Living Room
   (2) Apartment key bundle on hook in the Kitchen
   
   Which one? (e.g., 'the car keys', 'the kitchen keys')"
```

Follow-up query `"the car keys"` → re-traversal with refined plan descending directly into Living Room zone (cached from first traversal).

---

## 8. Component 5: 3D Output Generation

### 8.1 3D Bounding Box via Depth Unprojection

Given:
- `bbox_2d = [x1, y1, x2, y2]` from VLM JSON
- `depth_map[x, y]` from 3DGS render
- Camera intrinsics `K = [[fx, 0, cx], [0, fy, cy], [0, 0, 1]]`
- Camera extrinsics `[R | t]` (world-to-camera transform)

**Algorithm**:

```python
def unproject_bbox_to_3d(bbox_2d, depth_map, K, R, t):
    x1, y1, x2, y2 = bbox_2d
    
    # Sample pixels within the bounding box
    points_3d = []
    for x in range(x1, x2, step=4):  # subsample for efficiency
        for y in range(y1, y2, step=4):
            d = depth_map[y, x]
            if d <= 0 or d > max_depth:
                continue
            
            # Unproject to camera space
            X_cam = (x - cx) * d / fx
            Y_cam = (y - cy) * d / fy
            Z_cam = d
            
            # Transform to world space
            p_cam = np.array([X_cam, Y_cam, Z_cam])
            p_world = R.T @ (p_cam - t)
            points_3d.append(p_world)
    
    if not points_3d:
        return None
    
    points = np.array(points_3d)
    
    # Axis-aligned bounding box in world coordinates
    bbox_3d_min = points.min(axis=0)
    bbox_3d_max = points.max(axis=0)
    center = (bbox_3d_min + bbox_3d_max) / 2
    dimensions = bbox_3d_max - bbox_3d_min
    
    return {
        "center": center.tolist(),
        "dimensions": dimensions.tolist(),
        "bbox_min": bbox_3d_min.tolist(),
        "bbox_max": bbox_3d_max.tolist()
    }
```

**Multi-view fusion**: If the same object is found in multiple views (v042 and v061), compute 3D bboxes from both and return the intersection (tighter) or union (more conservative), depending on confidence levels.

### 8.2 Camera Pose Output

For navigation or viewpoint queries, return the camera pose of the best matching view:

```json
{
  "output_type": "camera_pose",
  "view_id": "v061",
  "position": [2.1, 0.9, 1.4],
  "rotation_matrix": [[...], [...], [...]],
  "fov": 60.0,
  "description": "Close-up view of coffee table, keys clearly visible at center"
}
```

This camera pose can be used directly by a robot, a virtual tour system, or a 3DGS viewer to navigate to the relevant location.

### 8.3 Novel View Synthesis (Optional)

After finding the target object, synthesize an optimal "object portrait" using 3DGS:

1. Compute the object's 3D bbox center `c` from unprojection
2. Place a new camera at `c + offset_direction * view_distance`, looking at `c`
3. Render an RGB image from this new pose using 3DGS
4. Return this rendered image as visual confirmation to the user

This is the "canonical view" of the found object — an ideal, unoccluded, well-lit view that may not correspond to any camera in the original NoField set.

---

## 9. System Architecture

### 9.1 Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                      OFFLINE CONSTRUCTION                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PLY File                                                        │
│     │                                                            │
│     ▼                                                            │
│  ┌─────────┐   K camera poses   ┌──────────────┐                │
│  │ NoField │──────────────────▶ │  3DGS Render │                │
│  └─────────┘                    └──────────────┘                │
│                                        │                         │
│                              K × (RGB + depth_map)              │
│                                        │                         │
│                                        ▼                         │
│                              ┌─────────────────┐                │
│                              │  VLM (parallel) │                │
│                              │  via MCP server │                │
│                              └─────────────────┘                │
│                                        │                         │
│                              K × view JSON (one_line_summary,   │
│                              object_list, objects[], relations)  │
│                                        │                         │
│                                        ▼                         │
│                ┌──────────────────────────────────────┐         │
│                │        Tree Builder                  │         │
│                │  1. Build spatial proximity graph    │         │
│                │  2. Find connected components        │         │
│                │  3. Recursive LLM grouping           │         │
│                │  4. Bottom-up summary generation     │         │
│                └──────────────────────────────────────┘         │
│                                        │                         │
│                              Hierarchical Semantic Tree          │
│                              (JSON / graph DB)                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                        ONLINE QUERY                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Natural Language Query                                          │
│     │                                                            │
│     ▼                                                            │
│  ┌──────────────────┐                                           │
│  │ LLM: Decompose   │  → structured query plan                  │
│  └──────────────────┘                                           │
│     │                                                            │
│     ▼                                                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │               Top-Down Tree Traversal                    │   │
│  │  Level 0: Root → prune irrelevant super-zones            │   │
│  │  Level 1: Zones → prune irrelevant zones                 │   │
│  │  Level 2: Sub-zones → prune irrelevant sub-zones         │   │
│  │  Level N: Leaf clusters → select best 1-3 views          │   │
│  └──────────────────────────────────────────────────────────┘   │
│     │                                                            │
│     ▼                                                            │
│  Read full JSON of selected views                               │
│     │                                                            │
│     ▼                                                            │
│  ┌──────────────────┐                                           │
│  │ LLM: Confirm     │  → bbox_2d of target object              │
│  │ match + extract  │                                           │
│  └──────────────────┘                                           │
│     │                                                            │
│     ▼                                                            │
│  ┌──────────────────┐   ┌──────────────────────────────────┐   │
│  │ Depth unproject  │   │ (Optional) Novel view synthesis  │   │
│  │ bbox_2d → 3D bbox│   │ via 3DGS from optimal pose       │   │
│  └──────────────────┘   └──────────────────────────────────┘   │
│     │                                                            │
│     ▼                                                            │
│  Output: {3D bbox, camera pose, confidence, visual confirmation} │
└──────────────────────────────────────────────────────────────────┘
```

### 9.2 Storage Layout

```
scene_database/
├── scene.ply                           # Original 3DGS model
├── cameras/
│   ├── poses.json                      # K camera poses from NoField
│   └── intrinsics.json                 # Camera intrinsics
├── renders/
│   ├── v001_rgb.png
│   ├── v001_depth.npy                  # Float32 depth map
│   ├── v002_rgb.png
│   ├── v002_depth.npy
│   └── ...
├── views/
│   ├── v001.json                       # Full VLM JSON per view
│   ├── v002.json
│   └── ...
└── tree/
    ├── tree.json                       # Full hierarchical tree
    ├── nodes/
    │   ├── node_0001.json              # Per-node data
    │   ├── node_0002.json
    │   └── ...
    └── spatial_graph.json              # Camera proximity graph
```

### 9.3 MCP Server Interface

The MCP server exposes the LLM to all system components via a consistent interface:

```json
{
  "mcp_tools": [
    {
      "name": "describe_view",
      "description": "Generate structured VLM JSON for a rendered view",
      "input": {"image_path": "str", "depth_path": "str"},
      "output": "view_json"
    },
    {
      "name": "tree_grouping_decision",
      "description": "Decide whether a set of views should be split and how",
      "input": {"view_summaries": "list[str]"},
      "output": "grouping_response"
    },
    {
      "name": "traversal_step",
      "description": "Decide which children to descend into during query traversal",
      "input": {"query": "str", "query_plan": "dict", "children": "list[node_summary]"},
      "output": "traversal_response"
    },
    {
      "name": "leaf_confirmation",
      "description": "Confirm object match in a leaf view and extract bbox",
      "input": {"query": "str", "view_json": "dict"},
      "output": "confirmation_response"
    }
  ]
}
```

---

## 10. Experimental Design and Ablations

### 10.1 The Core Ablation: Geometry vs. Pure LLM vs. Hybrid

**Motivation**: We claim that combining spatial proximity pre-filtering with LLM semantic grouping outperforms both in isolation. This must be proven empirically.

**Three Conditions**:

| Condition | Description |
|---|---|
| **A — Pure Geometry** | Zones = connected components of spatial proximity graph. No LLM. Labels = auto-generated from centroid coordinates. |
| **B — Pure LLM** | All K view summaries fed to LLM in one pass. No spatial pre-filtering. LLM decides all groupings. |
| **C — Geometry + LLM (Proposed)** | Spatial proximity graph pre-filters. LLM decides semantic groupings within spatial clusters and across adjacent ones. |

**Datasets**:
- ScanNet (indoor rooms, apartments): ground-truth room labels for zone evaluation
- Replica (photo-realistic indoor): diverse room types
- HM3D (large multi-room scenes): tests scalability
- Custom museum scan (if available): tests extreme depth

**Metrics**:

| Metric | How Measured |
|---|---|
| **Zone boundary accuracy** | % of views assigned to correct ground-truth room label |
| **Tree coherence score** | GPT-4 judge: "Does this tree accurately represent the scene structure?" (1-5) |
| **Retrieval accuracy** | % of queries answered correctly (3D bbox IoU > 0.5 with ground truth) |
| **Construction cost** | Total LLM calls, total tokens, wall-clock time |
| **Context efficiency** | Tokens consumed per query at inference time |
| **Scalability** | Accuracy degradation as K increases from 15 to 2000 |

**Expected findings**:
- A fails on open-plan spaces (no semantic understanding of zones)
- B fails on scenes with two visually similar but spatially separate rooms (identical bedrooms in different wings)
- C achieves best retrieval accuracy with lowest inference-time cost
- B has lower construction cost than C for small scenes but scales poorly

### 10.2 Ablation: Tree Depth vs. Retrieval Performance

Test retrieval accuracy as a function of tree depth allowed:
- Depth 1 (flat): no hierarchy, all views at root level
- Depth 2: one level of zones
- Depth 3: zones + sub-zones
- Depth N: LLM-determined depth (proposed)

**Expected finding**: LLM-determined depth outperforms all fixed-depth baselines because it adapts to scene complexity.

### 10.3 Ablation: Query Complexity

Compare retrieval accuracy across query types:
- Simple (single attribute): "find the red chair"
- Compound (multiple attributes): "find the worn leather armchair near the window"
- Relational (spatial): "find the object to the left of the sofa"
- Multi-hop (cross-zone): "find the nearest bathroom to the master bedroom"
- Functional: "where can I charge my phone?"

**Expected finding**: The tree traversal system maintains high accuracy across all types, while flat embedding retrieval (LERF, Semantic Gaussians) degrades significantly on relational and functional queries.

### 10.4 Ablation: VLM Description Quality

Compare VLM descriptions generated from:
- Raw captured training images (blurry, occluded, varying lighting)
- NoField-selected rendered 3DGS images (clean, optimal angles)
- Random rendered views from 3DGS

**Expected finding**: NoField-selected rendered views produce richer, more accurate VLM descriptions, confirming the value of our view selection strategy.

### 10.5 Baseline Comparisons

| Baseline | Paper | Why it's a fair comparison |
|---|---|---|
| LERF | Kerr et al., 2023 | Direct embedding retrieval in 3DGS/NeRF |
| Semantic Gaussians | Guo et al., 2024 | Feature distillation into 3DGS |
| ConceptGraphs | Gu et al., 2023 | Scene graph from RGBD, open-vocab |
| BBQ | Linok et al., 2024 | LLM-based scene graph + complex query reasoning |
| LangSplat | Qin et al., 2024 | Language feature fields in 3DGS |

---

## 11. Scalability Analysis

### 11.1 Construction Time

| Scene Size | K views | Tree depth | Construction LLM calls | Estimated time (parallel VLM) |
|---|---|---|---|---|
| Single room | 15 | 2 | ~20 | ~2 min |
| Apartment | 80 | 3 | ~80 | ~5 min |
| House | 300 | 4 | ~300 | ~15 min |
| Museum | 800 | 5-6 | ~700 | ~40 min |
| Building | 2000 | 6 | ~1800 | ~2 hours |

Construction is one-time and offline. These times are acceptable for any real-world deployment.

### 11.2 Query Time

| Tree depth | LLM calls at query time | Estimated latency |
|---|---|---|
| 2 | 4 | ~4 seconds |
| 3 | 5 | ~5 seconds |
| 4 | 6 | ~6 seconds |
| 6 | 8 | ~8 seconds |

**Query time is O(depth), not O(K).** As the scene grows from 15 to 2000 views, query latency increases from 4 to 8 seconds — a 2× increase for a 133× increase in scene size. This is the central scalability result.

### 11.3 Context Size Per Query

At each traversal level, the LLM reads summaries of immediate children only:

- Average node children: 4-8
- Average summary length: 15 words ≈ 20 tokens
- Context per traversal call: 8 × 20 = 160 tokens of summaries + prompt overhead ≈ 500 tokens total

**Maximum context at any single LLM call**: ~500-1000 tokens, regardless of scene size. This is the key advantage over flat retrieval (which would require reading all K view summaries).

---

## 12. Downstream Applications

### 12.1 Scene Change Detection

Build two trees from the same scene at T1 and T2. Compare trees node-by-node:
- Nodes in T1 not in T2 → objects removed
- Nodes in T2 not in T1 → objects added
- Same node, changed summary → object state changed

Applications: retail shelf monitoring, construction progress tracking, museum conservation, insurance assessment.

### 12.2 Multi-Scale Scene Documentation

The tree directly encodes multi-scale descriptions:
- Root → one-paragraph overview (real estate listing, museum catalogue)
- Zone nodes → room descriptions (interior design report)
- Object nodes → item inventory (insurance, asset management)

This documentation is free — the tree IS the documentation.

### 12.3 Cross-Scene Retrieval

Given a database of trees from many scenes, answer:
- "Find all museum rooms containing Egyptian sarcophagi"
- "Find apartments with open-plan kitchen-living areas"

Query against tree summaries, not raw 3DGS data. Enables semantic search over large databases of scanned environments.

### 12.4 Accessibility Scene Descriptions

Convert 3D spaces to structured text descriptions for visually impaired users:
- "The living room: entering from the hallway, the sofa is directly ahead, the coffee table is in front of the sofa with a glass surface. Keys and a remote control are on the table. The TV is mounted on the wall to the right. A bookshelf is in the far left corner."

Generated entirely from tree node summaries and spatial_relations fields.

### 12.5 VQA Training Data Generation

The tree + rendered images + ground-truth depth constitute a richly annotated dataset. Automatically generate QA pairs:
- "What is on the coffee table?" → from spatial_relations: "car keys and remote control"
- "How many chairs are in this scene?" → aggregation traversal
- "Which room contains the fireplace?" → zone-level query

Large-scale VQA dataset generation from any PLY file at near-zero marginal cost.

### 12.6 Embodied Agent Navigation

A robot or virtual agent can use the tree as its semantic map:
1. Query: "navigate to the room with the whiteboard"
2. Traversal finds the correct zone node
3. Camera pose of the best overview view = navigation goal
4. 3D bbox of whiteboard = fine-grained manipulation target

The system's primary output (camera pose + 3D bbox) is already a robot-ready goal specification.

---

## 13. Novelty Statement

### 13.1 What Has Been Done Before

| Prior Work | What They Do | What's Missing |
|---|---|---|
| LERF, LangSplat | Embed CLIP features per Gaussian, cosine similarity retrieval | Short queries only, no hierarchy, no compositional reasoning |
| Semantic Gaussians | Distill 2D model (CLIP, SAM) features into 3DGS | Open-vocab but flat, relies on explicit segmentation |
| ConceptGraphs, BBQ | RGBD scene graph, 2-level hierarchy | Fixed 2 levels, segmentation-dependent, not 3DGS |
| Hydra, SceneGraph++ | Layered scene graphs for robotics | Hardcoded ontology (object/room/floor), robotics-specific |
| GaussNav, BEINGS | 3DGS for robot navigation | Navigation-focused, not open retrieval |

### 13.2 What Is New in This Work

1. **Pure VLM scene understanding**: No DINO, no SAM, no clustering, no feature distillation. The VLM reads rendered images and produces all semantic information from scratch.

2. **LLM-determined hierarchy**: Depth, labels, granularity, and boundaries are all determined by the LLM analyzing the scene. No predefined ontology.

3. **Geometry + LLM hybrid construction**: Spatial proximity eliminates impossible comparisons; LLM handles semantic decisions. The ablation proves each component contributes.

4. **Scene-type agnosticism**: Same algorithm works for rooms, museums, medical environments, industrial sites. No scene-specific engineering.

5. **Logarithmic context scaling**: Query-time LLM context is O(depth), not O(K). A 2000-view scene requires the same context budget as a 15-view scene at each traversal step.

6. **3DGS-native 3D localization**: Exact depth maps from 3DGS enable geometrically precise 3D bbox output from 2D VLM detections, without any learned 3D network.

7. **NoField-optimal view selection**: Views are not random; they are information-theoretically optimal for scene coverage, producing the best possible inputs to the VLM.

---

## 14. Open Questions and Risks

### 14.1 LLM Consistency

**Risk**: Two runs of tree construction produce different trees (different groupings, different names), making the system non-reproducible.

**Mitigation**:
- Use temperature=0 for all LLM calls during construction
- Store the tree once and use it for all queries
- Evaluate consistency by building 3 trees and measuring structural similarity (tree edit distance)

### 14.2 VLM Hallucination

**Risk**: VLM describes objects that aren't in the image, or misidentifies objects. This would corrupt the tree with false information.

**Mitigation**:
- Set `confidence: "low"` for uncertain detections; traversal can optionally ignore low-confidence items
- Multi-view validation: an object asserted in one view but absent from neighboring views is flagged
- At query time, the leaf confirmation step provides a second VLM check

### 14.3 NoField Coverage Gaps

**Risk**: Some parts of the scene are not well-covered by any NoField camera, meaning objects in those regions will not be captured in any view JSON.

**Mitigation**:
- Set a high coverage threshold (95%+ of scene volume) for NoField
- Include a "coverage verification" step: render depth maps and check for large unobserved regions
- For gaps, add supplementary cameras manually or via random sampling

### 14.4 Depth Map Accuracy in Thin/Transparent Objects

**Risk**: Glass surfaces, transparent objects, or thin structures may produce noisy or incorrect depth values from 3DGS, leading to incorrect 3D bbox computation.

**Mitigation**:
- Filter out depth values with high variance in a local neighborhood (indicates unstable geometry)
- Fall back to camera pose output (localization without precise 3D bbox) when depth quality is low
- Report depth confidence alongside 3D bbox output

### 14.5 Scalability of Tree Construction Cost

**Risk**: At K=2000 views, tree construction requires ~1800 LLM calls, which may take 2+ hours and incur meaningful API costs.

**Mitigation**:
- Use a fast, cheap LLM (GPT-4o-mini, Gemini Flash) for tree construction; reserving the expensive model only for view description
- Construction is fully offline and one-time; 2 hours for a building-scale scene is acceptable
- Parallelism: all view description VLM calls run in parallel; tree construction is inherently sequential but each call is fast (summaries only)

### 14.6 Scene Update / Incremental Re-indexing

**Risk**: If the scene changes (objects moved, new furniture added), the entire tree must be rebuilt.

**Future work**: Incremental tree updates — detect changed views via image similarity, re-run VLM only on changed views, re-run tree construction only for affected subtrees. Not in scope for initial paper.

---

*End of Design Document*

**Next Steps**:
1. User reviews and approves this spec
2. Invoke writing-plans skill to create detailed implementation plan
3. Implement components in order: NoField integration → VLM pipeline → Tree builder → Query traversal → 3D output
