# HOV-SG

PDF: `papers/new-papers/3d-scene-understanding/HOV-SG.pdf`  
Source file added from: `2403.17846v2.pdf`  
arXiv: `2403.17846v2`  
Title: Hierarchical Open-Vocabulary 3D Scene Graphs for Language-Grounded Robot Navigation  
Authors: Abdelrhman Werby, Chenguang Huang, Martin Buchner, Abhinav Valada, Wolfram Burgard  
Year: 2024

## Relevance To Beyond Proximity

HOV-SG is a close conceptual comparison for hierarchical open-vocabulary 3D scene graphs. It constructs floor, room, and object concepts for robot navigation, making it important for positioning our explicit hierarchy claims.

## Comparison Notes

| Dimension | Notes |
|---|---|
| Input | Open-vocabulary segment-level 3D maps and robot/navigation data. |
| Output | Hierarchical 3D scene graph with floor, room, and object concepts. |
| Strength | Directly addresses hierarchy and language-grounded navigation. |
| Gap For Our Work | Different construction path; not a rendering-first VLM-over-3DGS tree. |
| Use In Article | Mandatory hierarchy/scene-graph related work. |

## Baseline Feasibility

Literature-only for this sprint. A fair comparison would require adapting our captured scenes into the method's expected map inputs or reporting only conceptual differences.
