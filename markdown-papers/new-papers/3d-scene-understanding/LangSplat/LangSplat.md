# LangSplat

PDF: `papers/new-papers/3d-scene-understanding/LangSplat.pdf`  
Source file added from: `2312.16084v2.pdf`  
arXiv: `2312.16084v2`  
Title: LangSplat: 3D Language Gaussian Splatting  
Authors: Minghan Qin, Wanhua Li, Jiawei Zhou, Haoqian Wang, Hanspeter Pfister  
Year: 2024

## Relevance To Beyond Proximity

LangSplat is the most important language-field baseline for this project because it shares the 3D Gaussian Splatting representation family. It supports efficient open-vocabulary querying through a 3D language field, but it does not provide an explicit semantic hierarchy comparable to our graph/tree query route.

## Comparison Notes

| Dimension | Notes |
|---|---|
| Input | Images, camera poses, 3DGS reconstruction, CLIP/SAM-style features. |
| Output | 3D language Gaussian field and query relevancy/localization. |
| Strength | Strong simple object and attribute queries over 3DGS scenes. |
| Gap For Our Work | No native zone-region-object tree or graph traversal context accounting. |
| Use In Article | Mandatory related work and strongest future external baseline. |

## Baseline Feasibility

High setup cost in the current sprint. Treat as literature-only unless a Person 1/3 follow-up creates a scene-format adapter and a fixed output schema.
