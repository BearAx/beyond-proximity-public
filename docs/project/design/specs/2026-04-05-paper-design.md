# Paper Design Document: Beyond Proximity

**Date**: April 5, 2026
**Target Venue**: CVPR / ICCV / ECCV (Top-tier Computer Vision)
**Status**: Design — Awaiting Implementation Planning

---

## 1. Problem Statement and Motivation

**Context:** 
3D Gaussian Splatting (3DGS) has revolutionized photorealistic scene rendering, but it natively lacks semantic structure. It is a purely geometric and photometric representation.

**The Bottleneck:** 
Current approaches to semantic 3D scene understanding typically rely on 3D feature distillation (e.g., baking CLIP embeddings into Gaussians, as in LERF) or explicit 3D segmentation (like ConceptGraphs). These methods are fundamentally limited by the low resolution of distilled features, struggle with open-vocabulary or compositional queries, and fail to construct meaningful hierarchical relationships between rooms, zones, and objects. Furthermore, when building scene hierarchies, existing methods typically use purely geometric clustering, which arbitrarily splits large open spaces (e.g., a stage and its audience), or purely semantic clustering, which falsely merges identical but physically distant rooms.

**Our First-Principles Approach:** 
Instead of forcing semantics into the 3D primitives, we treat 3DGS as a perfect, photorealistic rendering engine. We offload all semantic understanding to state-of-the-art 2D Vision-Language Models (VLMs). We introduce a novel two-pass clustering framework that combines geometric proximity with deep VLM spatial reasoning to construct highly accurate, scene-agnostic hierarchical semantic graphs.

---

## 2. Core Contributions

1. **Two-Pass Geometric-Semantic Clustering:** We propose a novel algorithm for hierarchical scene construction. Pass 1 uses camera proximity to build conservative spatial clusters (preventing cross-room hallucinations). Pass 2 introduces a VLM-driven semantic merge, utilizing explicit `facing` directions and `visible_landmarks` to stitch geometrically disjoint clusters that share complementary physical space (e.g., an audience facing a stage).
2. **LLM-Driven Hierarchical Reasoning:** We demonstrate that LLMs, when prompted with structured view summaries, can dynamically determine optimal tree depth and zone granularity without hardcoded heuristics, adapting seamlessly to different scene scales (single room vs. large venue).
3. **Two-Stage Crop-and-Requery BBox Refinement:** We address the inherent spatial inaccuracies of standard VLMs. By utilizing a spatial Chain-of-Thought (CoT) for rough localization followed by an automated crop-and-requery pipeline, we drastically improve 2D bounding box precision for object retrieval.

---

## 3. Paper Structure and Outline

### Abstract
Summarizes the limitation of pure 3D feature distillation and the failure of existing clustering methods on complex spaces. Introduces our two-pass framework and the two-stage bounding box refinement. Highlights quantitative improvements in hierarchy accuracy and localization precision.

### 1. Introduction
- The success of 3DGS in rendering vs. its semantic gap.
- Why 3D distillation (LERF) and 3D segmentation (ConceptGraphs) are insufficient for complex, open-vocabulary, hierarchical queries.
- Introduction of our rendering-first paradigm: using 3DGS purely to generate ideal viewpoints for 2D VLMs.
- Explicit statement of the three core contributions.

### 2. Related Work
- **Semantic 3D Scene Understanding:** Contrast our rendering-first approach with feature distillation (LERF, Semantic Gaussians) and explicit 3D graph building (OpenScene, ConceptGraphs).
- **Hierarchical Scene Graphs:** Discuss existing methods that rely on 3D heuristics vs. our LLM-driven adaptive depth approach.
- **Vision-Language Models for Spatial Reasoning:** Contrast standard single-pass VLM localization with our CoT + Crop-and-Requery refinement.

### 3. Methodology
- **3.1 System Overview:** High-level pipeline from 3DGS PLY input to the hierarchical tree and query execution.
- **3.2 VLM View Analysis:** Detailing the extraction of structured semantics (`room_type`, `facing`, `visible_landmarks`, objects) from 2D renders.
- **3.3 Two-Pass Hierarchical Tree Construction:**
  - *Phase 1 (Geometric):* Adaptive thresholding on camera proximity to prevent cross-room merging.
  - *Phase 2 (Semantic Merge):* Using complementary facings (e.g., stage↔audience) and shared landmarks to correct geometric over-segmentation.
  - *Phase 3 (LLM Tree Grouping):* The "Step 0 Same-Room Check" and subsequent dynamic naming/sub-grouping.
- **3.4 Top-Down Semantic Query Traversal:**
  - LLM query decomposition into structured plans.
  - Hierarchical pruning during traversal.
  - *Two-Stage BBox Refinement:* Spatial CoT for rough estimation → Crop → Requery VLM → Map to original coordinates.
  - *Best-View Ranking:* Scoring based on confidence, bbox area, and centrality.

### 4. Experimental Setup & Ablation Studies
- **4.1 Implementation Details:** Briefly note the orchestration via MCP tools to isolate LLM reasoning from spatial infrastructure.
- **4.2 Hierarchy Construction Accuracy (Ablation 1):**
  - Compare tree structures generated by:
    - Baseline A: Pure Geometric Clustering (fails on large, sparse rooms).
    - Baseline B: Pure Semantic Clustering (fails on repetitive identical rooms).
    - Ours: Two-Pass Hybrid (succeeds).
- **4.3 2D Localization Precision (Ablation 2):**
  - Compare bounding box Intersection-over-Union (IoU) and success rates:
    - Baseline: Standard single-pass VLM bounding box.
    - Ours: Spatial CoT + Two-Stage Crop-and-Requery.
- **4.4 Qualitative Results:** Visualizations of the generated semantic tree and retrieved object bounding boxes on test scenes.

### 5. Limitations and Future Work
- **Limitations:** The current system operates entirely in 2D space for querying (2D bounding boxes) and relies on manual or randomized camera placement.
- **Future Work:** Integrating automated optimal camera placement (e.g., NoField) and utilizing the exact depth maps inherent to 3DGS to unproject the refined 2D bounding boxes into precise 3D world coordinates.

### 6. Conclusion
Summary of how the two-pass clustering and crop-and-requery refinement bridge the gap between photorealistic 3DGS and robust, open-vocabulary semantic understanding.

---

## 4. Required Assets for LaTeX Generation
To successfully compile this paper, the following assets/sections will be required during implementation:
1. **Figures:** 
   - Fig 1: Teaser/Overview showing the input 3DGS, the two-pass tree, and a query result.
   - Fig 2: Visual comparison of Geometric vs. Semantic vs. Two-Pass clustering.
   - Fig 3: The Two-Stage Crop-and-Requery pipeline.
2. **Tables:**
   - Tab 1: Ablation on clustering accuracy.
   - Tab 2: Ablation on bounding box localization IoU.
3. **Bibliography:** Standard BibTeX file (`.bib`) containing references to 3DGS, LERF, ConceptGraphs, OpenScene, GPT-4V/Claude 3.5, etc.

---
*End of Spec*