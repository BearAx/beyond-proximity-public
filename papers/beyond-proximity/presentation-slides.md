# Presentation Slides: Beyond Proximity

## Slide 1: Title Slide
**Title:** Beyond Proximity: Two-Pass Geometric-Semantic Clustering for Hierarchical 3D Scene Understanding
**Subtitle:** A Rendering-First Paradigm for 3D Gaussian Splatting
**Visual:** A high-quality 3DGS render of a complex scene (e.g., the Conference Hall) next to a clean, hierarchical semantic tree.

## Slide 2: The Core Problem
**Header:** 3DGS is Beautiful, But "Dumb"
* Photorealistic real-time rendering.
* Purely geometric and photometric (point clouds).
* **Missing Link:** No semantic structure.
* **Why it matters:** Downstream tasks (robotics, VR, natural language querying) require the system to *understand* what it's looking at, not just render it.

## Slide 3: Existing Approaches & Their Flaws
**Header:** How are we doing this today?
* **Feature Distillation (e.g., LERF):** 
  * Embeds VLM features into 3D.
  * Good for point-wise keyword search.
  * *Flaw:* Smooths out boundaries, lacks compositional reasoning.
* **Explicit 3D Segmentation (e.g., ConceptGraphs):**
  * Lifts 2D segments to 3D graphs.
  * *Flaw:* Scales poorly to open-vocabulary, struggles with high-level architectural hierarchy.

## Slide 4: The Hierarchy Construction Dilemma
**Header:** Pure Geometry vs. Pure Semantics
* Attempting to build room-level hierarchies usually relies on one of two extremes:
* **Pure Geometry:** Splits contiguous spaces. (e.g., a ballroom stage and its audience get separated because the cameras are physically far apart).
* **Pure Semantics:** Merges disconnected spaces. (e.g., a lobby and a distant corridor get merged because they share the same carpet and lighting).

## Slide 5: Our Insight
**Header:** The Rendering-First Paradigm
* Stop forcing semantics into 3D primitives.
* Treat 3DGS as an ideal **rendering engine**.
* Generate noise-free, perfect 2D viewpoints.
* Leverage state-of-the-art 2D Vision-Language Models (VLMs) directly on the renders.

## Slide 6: The Two-Pass Solution
**Header:** Two-Pass Geometric-Semantic Clustering
* **Pass 1: Geometric Proximity Graph**
  * Adaptive thresholding based on camera distance.
  * Prevents cross-room hallucinations (solves the "Pure Semantics" flaw).
* **Pass 2: Semantic Merge Pass**
  * VLMs extract architectural metadata: *Room Type*, *Facing*, *Visible Landmarks*.
  * Stitches disjoint clusters that share physical space (solves the "Pure Geometry" flaw).
  * *Example:* Merges "Stage-facing" and "Audience-facing" clusters.

## Slide 7: Querying the Scene
**Header:** Top-Down Semantic Traversal
* User inputs natural language: *"Find the fire extinguisher near the exit"*
* LLM decomposes the query.
* System traverses the semantic tree top-down.
* **Efficiency:** Prunes irrelevant branches using 10-15 word node summaries, saving massive token costs.

## Slide 8: The Localization Problem
**Header:** VLMs Struggle with Spatial Precision
* We reached the correct leaf views, but...
* Off-the-shelf VLMs are great at identifying objects but terrible at drawing precise bounding boxes.
* Often misaligned by 10-20% of the image, especially for small objects.

## Slide 9: Crop-and-Requery
**Header:** Two-Stage Bounding Box Refinement
* **Stage 1: Spatial Chain-of-Thought (CoT)**
  * Force VLM to reason about horizontal/vertical thirds and sanity-check spatial relations. Yields a *rough* box.
* **Stage 2: Crop-and-Requery**
  * Aggressively crop the high-res image around the rough box.
  * Re-prompt the VLM on the zoomed-in crop.
  * Map coordinates back to the original image space.

## Slide 10: Results - Topology
**Header:** 100% Room-Level Topological Accuracy
* Evaluated on a challenging "Conference Hall" scene.
* **Baseline A (Geometric):** Fractured the ballroom.
* **Baseline B (Semantic):** Hallucinated a merged lobby/corridor.
* **Ours:** Perfectly isolated distinct rooms while maintaining the integrity of large contiguous spaces.

## Slide 11: Results - Localization
**Header:** 34% Improvement in Intersection-over-Union (IoU)
* Tested on 50 challenging "find" queries for small objects.
* Single-pass VLMs frequently missed tight boundaries.
* Our Crop-and-Requery tightened bounding boxes strictly to actual pixel boundaries.
* Added **Best-View Ranking** to automatically return the highest-confidence, most centralized perspective.

## Slide 12: Conclusion & Future Work
**Header:** Looking Forward
* **Conclusion:** Off-the-shelf 2D VLMs can drive precise 3D scene reasoning without complex 3D feature distillation.
* **Future Work 1:** 3D Depth Unprojection. Transitioning from refined 2D bounding boxes to exact 3D world coordinates.
* **Future Work 2:** Automated camera placement algorithms (e.g., NoField) to eliminate manual scene capture.
* **Thank You!**
