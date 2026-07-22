# OpenLex3D

PDF: `papers/new-papers/3d-scene-understanding/OpenLex3D.pdf`  
Source file added from: `2503.19764v2.pdf`  
arXiv: `2503.19764v2`  
Title: OpenLex3D: A Tiered Evaluation Benchmark for Open-Vocabulary 3D Scene Representations  
Authors: Christina Kassab, Sacha Morin, Martin Buchner, Matias Mattamala, Kumaraditya Gupta, Abhinav Valada, Liam Paull, Maurice Fallon  
Year: 2025

## Relevance To SemanticSplat

OpenLex3D is evaluation-focused. It is useful for shaping our benchmark language: object retrieval and open-vocabulary segmentation should be separated from hierarchy traversal and context-efficiency claims.

## Comparison Notes

| Dimension | Notes |
|---|---|
| Input | Open-vocabulary 3D scene representations over Replica, ScanNet++, and HM3D scenes. |
| Output | Tiered evaluation labels for open-set segmentation and object retrieval. |
| Strength | Strong benchmark framing for open-vocabulary 3D representations. |
| Gap For Our Work | Does not directly evaluate adaptive semantic tree traversal. |
| Use In Article | Cite for evaluation framing and to motivate careful query buckets. |

## Baseline Feasibility

Potential future evaluation target, not a sprint baseline. Use it now to avoid overclaiming and to align our benchmark buckets with open-vocabulary evaluation practice.
