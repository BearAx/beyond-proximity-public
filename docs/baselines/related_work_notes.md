# Related Work Notes

Week 1 owner: Literature / Baselines / Repo Notes Lead  
Scope: understand which baselines matter, what they output, and where SemanticSplat differs. These notes are not yet a polished paper section.

## Positioning Summary

SemanticSplat should be positioned as a rendering-first, hierarchy-first semantic scene system. Instead of distilling language features into 3D primitives or constructing an object-only graph from segmentation masks, it uses posed RGB-D views, VLM descriptions, geometry-assisted grouping, and LLM traversal to produce a semantic tree and answer natural-language queries.

The nearest baselines split into two groups:

| Family | Examples | What They Test Against Us |
|---|---|---|
| Language fields | LERF, LangSplat, Semantic Gaussians, LEGS | Whether direct 3D feature fields are enough for open-vocabulary localization. |
| Object/scene graphs | ConceptGraphs, BBQ | Whether explicit object-centric maps and relations are enough for compositional scene queries. |

The core claim should not be "we beat all semantic 3D methods at their native tasks." A fairer claim is: for complex spatial and compositional queries, a semantic hierarchy built from VLM descriptions plus geometry can provide more interpretable query traces and better context scaling than flat language fields or object-only graphs.

## LangSplat

Reference: Qin et al., "LangSplat: 3D Language Gaussian Splatting", CVPR 2024.

LangSplat extends 3D Gaussian Splatting with language features. It distills CLIP features into 3D language Gaussians and uses a scene-specific language autoencoder to reduce feature dimensionality. It also uses SAM-derived hierarchical semantics to improve object boundary precision. The method targets open-vocabulary 3D object localization and semantic segmentation, and reports a large speedup over LERF because language features are rendered through Gaussian splatting rather than NeRF volume rendering.

Inputs:

| Item | Notes |
|---|---|
| Images and camera poses | Usually COLMAP/Nerfstudio-style reconstruction inputs. |
| 3DGS training/reconstruction | The method learns language-enhanced Gaussians. |
| 2D foundation-model features | CLIP and SAM are central to the method. |

Outputs:

| Output | Usefulness for SemanticSplat Evaluation |
|---|---|
| Text-query relevancy in 3D | Strong baseline for object localization. |
| Semantic segmentation / localization results | Can be converted to point, mask, or approximate bbox depending on available code path. |
| No explicit room/zone hierarchy | Important limitation for tree coherence and context-efficiency comparison. |

Strengths:

| Strength | Why It Matters |
|---|---|
| 3DGS-native | Closest mandatory baseline because it shares the 3DGS representation family. |
| Open-vocabulary localization | Directly comparable on simple object-finding queries. |
| Faster than LERF | Avoids dismissing language fields as impractical only because LERF is slow. |

Limitations for our comparison:

| Limitation | Protocol Risk |
|---|---|
| Primarily CLIP-style text grounding | May be weak on relational, functional, and multi-hop language. |
| No explicit semantic tree | Cannot natively report tree coherence or traversal context. |
| Training/input format differs from our Week 1 RGB-D scene format | Needs adapter work before a fair run. |

Paper-section angle:

LangSplat is the main 3DGS-language baseline. It should be described as efficient and strong for open-vocabulary 3D localization, while SemanticSplat differs by treating rendered views as VLM-readable evidence and organizing the scene into an explicit, query-traversable hierarchy.

## ConceptGraphs

Reference: Gu et al., "ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning", 2023.

ConceptGraphs builds an object-centric, open-vocabulary 3D scene graph from posed RGB-D images. It uses 2D foundation models for instance segmentation, projects detections into 3D, associates observations across views, captions objects, and derives graph relations for planning and language reasoning.

Inputs:

| Item | Notes |
|---|---|
| Posed RGB-D sequence | Strong alignment with Replica/ScanNet-style Week 1 data. |
| Camera intrinsics/extrinsics | Required for projection and multi-view association. |
| 2D segmentation/model outputs | Object masks are a major dependency. |

Outputs:

| Output | Usefulness for SemanticSplat Evaluation |
|---|---|
| Object-centric 3D scene graph | Strong comparison for object and relation queries. |
| Object captions and spatial relations | Can be converted into text context for LLM planning. |
| 3D object geometry / point-cloud clusters | Can support bbox-like localization if exported. |

Strengths:

| Strength | Why It Matters |
|---|---|
| Works from RGB-D trajectories | Good fit for Replica/ScanNet pilot data. |
| Explicit relations | Better than flat language fields for relational queries. |
| Object-level graph is interpretable | Comparable to parts of our tree/query trace story. |

Limitations for our comparison:

| Limitation | Protocol Risk |
|---|---|
| Object-centric rather than zone/tree-centric | May not naturally answer room/zone hierarchy tasks. |
| Depends on segmentation and association quality | Errors in masks become graph errors. |
| Setup is heavier than our current repo | Running it in Week 1 is not necessary; adapter design is enough. |

Paper-section angle:

ConceptGraphs is the main graph baseline. SemanticSplat should be contrasted as less dependent on explicit instance segmentation and more focused on adaptive spatial hierarchy, while acknowledging that ConceptGraphs has stronger native object-map machinery.

## LERF

Reference: Kerr et al., "LERF: Language Embedded Radiance Fields", ICCV 2023.

LERF grounds CLIP embeddings inside a NeRF, producing a dense multi-scale language field. It supports interactive text queries by rendering relevancy maps for natural-language prompts.

Inputs:

| Item | Notes |
|---|---|
| Nerfstudio-compatible scene data | Images, poses, camera calibration. |
| NeRF training | Different representation from 3DGS. |
| CLIP/DINO preprocessing | Used to supervise language field features. |

Outputs:

| Output | Usefulness for SemanticSplat Evaluation |
|---|---|
| 2D/3D relevancy maps | Useful for object localization. |
| No explicit object graph or tree | Weak for compositional hierarchy evaluation. |

Strengths:

| Strength | Why It Matters |
|---|---|
| Canonical language-field baseline | Many later 3D language works compare to it. |
| Multi-scale language features | Handles object scale better than single-resolution feature fields. |

Limitations for our comparison:

| Limitation | Protocol Risk |
|---|---|
| NeRF-based, not 3DGS-native | Less directly comparable than LangSplat. |
| Slower training/rendering | Should not be the only language-field baseline. |
| CLIP grounding is mostly flat | Expected weakness on compositional and functional queries. |

Paper-section angle:

LERF is useful background and optional baseline. It supports the argument that language fields are strong for open-vocabulary relevance but do not solve hierarchy, context scaling, or compositional reasoning by themselves.

## Semantic Gaussians and Related 3DGS Language Methods

Reference: "Semantic Gaussians: Open-Vocabulary Scene Understanding with 3D Gaussian Splatting", 2024/2026 project line.

Semantic Gaussians distills 2D semantic features from pretrained models into 3D Gaussian components and explores semantic segmentation, object part segmentation, scene editing, and related tasks. It can use COLMAP, ScanNet, or custom formats depending on the implementation path.

Related methods in local notes:

| Method | One-Line Note |
|---|---|
| LEGS | Online language-embedded Gaussian splats for robot-scale open-vocabulary object queries. |
| OpenGaussian / LEGaussian / GOI | Additional 3DGS language-feature methods; useful as related work, not mandatory Week 1 baselines. |
| BBQ | RGB-D object-centric scene graph with deductive reasoning for relational object queries. |

Why these matter:

| Point | Implication |
|---|---|
| The field is moving quickly toward 3DGS semantic features | Related work must not pretend LangSplat is the only 3DGS-language method. |
| Most methods optimize or distill features into the 3D representation | SemanticSplat's rendering-first VLM path is a real methodological distinction. |
| Many methods evaluate segmentation/localization, not semantic hierarchy | Our metrics must include localization plus hierarchy/query-context metrics. |

## Suggested Related Work Structure

1. Semantic language fields in 3D: LERF, LangSplat, Semantic Gaussians, LEGS.
2. Open-vocabulary 3D object graphs: ConceptGraphs, BBQ, ConceptFusion/OpenScene as context.
3. LLM/VLM scene reasoning: methods that convert visual evidence into text/graphs for planning.
4. Semantic hierarchy and context scaling: emphasize the gap our tree aims to fill.

## Week 1 Takeaways

| Takeaway | Action |
|---|---|
| LangSplat and ConceptGraphs are the mandatory baselines. | Prepare adapters later; no need to run them in Week 1. |
| LERF is useful as background and optional baseline. | Include in related work and possibly a small localization comparison if time permits. |
| Baseline output formats are mismatched. | Aleksander's evaluation protocol should define a common query-result JSON. |
| Our strongest distinction is not just "3DGS + language." | Emphasize automatic semantic tree construction, query traversal, and context efficiency. |

## Week 6 BBQ Positioning Paragraph

BBQ is the closest object-centric scene-graph reference for the current public-dataset alignment. It builds an RGB-D object graph with captions, 3D extents, metric distances, and semantic spatial relations, then uses deductive LLM calls to select target and anchor objects before grounding over a compact subgraph. BBQ reports stronger public grounding evidence than the current Beyond Proximity paper draft, including Replica/ScanNet segmentation metrics and Sr3D+/Nr3D/ScanRefer Acc@k tables. Our Week 6 evidence should therefore position Beyond Proximity differently: as a hierarchical semantic-tree and context-pruning layer for queryable 3DGS digital twins, evaluated against same-input flat graph-search baselines and aligned with BBQ-style object-grounding metrics. We do not claim superiority over BBQ because the repository does not contain a same-dataset, same-query BBQ official-code run.

Evidence for this paragraph is consolidated in `docs/baselines/bbq_comparison.md`.
