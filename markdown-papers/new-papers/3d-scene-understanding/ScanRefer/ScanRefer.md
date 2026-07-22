# ScanRefer

PDF: `papers/new-papers/3d-scene-understanding/ScanRefer.pdf`  
Source file added from: `1912.08830v3.pdf`  
arXiv: `1912.08830v3`  
Title: ScanRefer: 3D Object Localization in RGB-D Scans using Natural Language  
Authors: Dave Zhenyu Chen, Angel X. Chang, Matthias Niessner  
Year: 2020

## Relevance To SemanticSplat

ScanRefer is a grounding benchmark and method for localizing an object in an RGB-D scan from a free-form natural-language referring expression. It is useful for our article as a reference point for language-conditioned 3D localization and for clarifying what our current benchmark is not yet claiming.

## Comparison Notes

| Dimension | Notes |
|---|---|
| Input | RGB-D scan / point cloud plus a language description. |
| Output | Target object localization, including 3D box prediction. |
| Strength | Strong task definition for language-to-3D object grounding. |
| Gap For Our Work | It does not address semantic hierarchy, context pruning, or open-ended scene traversal. |
| Use In Article | Cite as grounding context; do not treat as a direct same-input baseline unless ScanNet-style labels are available. |

## Baseline Feasibility

Literature-only for the current sprint. A fair run would require ScanNet-style object proposals or annotated 3D targets, which the current five captured scenes do not provide.
