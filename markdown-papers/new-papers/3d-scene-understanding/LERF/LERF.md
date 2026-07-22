# LERF

PDF: `papers/new-papers/3d-scene-understanding/LERF.pdf`  
Source file added from: `2303.09553v1.pdf`  
arXiv: `2303.09553v1`  
Title: LERF: Language Embedded Radiance Fields  
Authors: Justin Kerr, Chung Min Kim, Ken Goldberg, Angjoo Kanazawa, Matthew Tancik  
Year: 2023

## Relevance To SemanticSplat

LERF is the canonical language-field comparison: it distills open-vocabulary language features into a NeRF and supports text-query relevancy maps. It motivates why flat language-field retrieval is strong for open-vocabulary object lookup but insufficient by itself for explicit hierarchy and query-trace control.

## Comparison Notes

| Dimension | Notes |
|---|---|
| Input | Nerfstudio-style posed images and a trained NeRF. |
| Output | Relevancy maps for language prompts. |
| Strength | Open-vocabulary text grounding across a continuous 3D field. |
| Gap For Our Work | No native room/zone graph and no tree traversal trace. |
| Use In Article | Background and optional baseline; LangSplat is the closer 3DGS-language baseline. |

## Baseline Feasibility

Literature-only unless the team budgets a separate NeRF training path and output adapter. Do not compare LERF runtime directly to our graph-vs-flat runner without a same-scene, same-query run.
