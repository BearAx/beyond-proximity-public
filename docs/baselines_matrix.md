# Baseline Matrix

Week 1 owner: Literature / Baselines / Repo Notes Lead  
Purpose: identify which baselines are required, what they consume, what they produce, and how hard they will be to align with the SemanticSplat evaluation protocol.

## Common Evaluation Target

For Week 1 planning, every method should eventually be adapted to a shared output record:

```json
{
  "method": "method_name",
  "scene_id": "replica_pilot_scene_001",
  "query": "find the chair near the table",
  "found": true,
  "answer_text": "chair near the dining table",
  "view_id": "optional",
  "bbox_2d": [0.1, 0.2, 0.4, 0.7],
  "bbox_3d": {
    "center": [0.0, 0.0, 0.0],
    "dimensions": [0.0, 0.0, 0.0]
  },
  "confidence": 0.0,
  "trace": []
}
```

Not every baseline can fill every field natively. Missing fields should be recorded explicitly rather than silently inferred.

## Baseline Comparison

| Method | Mandatory? | Input | Native Output | 3D Localization? | BBox Obtainable? | Datasets Mentioned / Likely Fit | Run Difficulty | Notes |
|---|---:|---|---|---|---|---|---|---|
| SemanticSplat proposed | Yes | Pilot scene with RGB, depth, poses, intrinsics, VLM descriptions | Semantic tree, traversal trace, query result, optional 3D bbox | Yes, through depth unprojection | Yes, if VLM bbox + depth are available | Replica and ScanNet planned | Medium until headless pipeline exists | Week 1 exit target is one automatic scene. |
| LangSplat | Yes | Images, camera poses, trained or trainable 3DGS, CLIP/SAM features | 3D language Gaussian field, relevancy/localization, semantic segmentation | Yes | Approximate bbox may be derived from segmentation/relevancy threshold | LERF-style scenes, 3D-OVS, custom COLMAP/3DGS; needs adapter for Replica/ScanNet | High | Closest 3DGS-language baseline; no explicit semantic tree. |
| ConceptGraphs | Yes | Posed RGB-D sequence, intrinsics, segmentation/foundation model stack | Object-centric 3D scene graph with captions and relations | Yes, object map in 3D | Yes, from object point clusters or projected extents if exported | Replica support documented; ScanNet likely feasible with dataloader work | High | Closest graph baseline; object-centric rather than adaptive scene hierarchy. |
| LERF | Optional | Nerfstudio-compatible images/poses | NeRF language field and relevancy maps | Yes, via relevancy field | Approximate bbox from rendered relevancy map or 3D peak | LERF datasets; custom Nerfstudio data | High | Useful background; LangSplat is a stronger mandatory version for 3DGS. |
| Semantic Gaussians | Optional / related work | COLMAP, ScanNet, or custom 3DGS-compatible data; 2D semantic features | Semantic 3D Gaussians, semantic segmentation, localization-like outputs | Yes | Likely from semantic segmentation or point grouping | ScanNet explicitly relevant | High | Good additional 3DGS semantic feature baseline if time allows. |
| LEGS | Optional / related work | Robot trajectory images and poses; online Gaussian splat training | Language-embedded Gaussian splat and object-query localization | Yes | Point/region localization; bbox adapter needed | Room-scale robot scenes | High | Good related work for online 3DGS language mapping, not necessary for Week 1. |
| BBQ | Optional / strong future baseline | Posed RGB-D frames with known poses/calibration | Object-centric 3D map, spatial relations, deductive LLM reasoning | Yes | Yes, object-centric 3D map can support bbox-like outputs | Replica and ScanNet | High | Very relevant for complex relational queries; may be a better future graph baseline than ConceptGraphs alone. |
| Pure Geometry ablation | Yes, internal | Same views/poses as SemanticSplat | Geometric clusters/tree without semantic LLM grouping | Indirect | Yes only after normal query stage | Replica and ScanNet | Low | Needed to prove geometry alone is insufficient. |
| Pure LLM ablation | Yes, internal | Same VLM view summaries, no spatial prefilter | LLM-built groups/tree | Indirect | Yes only after normal query stage | Replica and ScanNet | Low to medium | Needed to show geometry prevents merging distant similar rooms. |
| Hybrid ablation | Yes, internal | Views, poses, VLM summaries | Geometry-assisted semantic tree | Yes | Yes | Replica and ScanNet | Medium | Proposed method condition. |

## Mandatory Baselines

### LangSplat

What it answers well:

| Query Type | Expected Fit |
|---|---|
| "find the chair" | Strong. |
| "find the red chair" | Strong if visual/text feature alignment is good. |
| "find the chair near the table" | Partial; relation may need post-processing over relevancy/object candidates. |
| "which zone contains the reception area?" | Weak; no native zone hierarchy. |
| "which room is closest to the kitchen?" | Weak unless room nodes are added externally. |

Adapter needed:

| Adapter | Description |
|---|---|
| Data adapter | Convert Replica/ScanNet pilot scene into LangSplat-compatible image/pose/3DGS training format. |
| Query adapter | Convert a natural-language query into LangSplat text prompt(s). |
| Output adapter | Convert relevancy/segmentation to `found`, `bbox_3d`, and confidence. |
| Trace adapter | Record no tree trace; use a flat "language-field query" trace entry. |

### ConceptGraphs

What it answers well:

| Query Type | Expected Fit |
|---|---|
| "find the chair" | Strong if segmentation and object association work. |
| "find the chair near the table" | Stronger than flat language fields because object relations are explicit. |
| "find the room with both a sofa and a TV" | Partial; possible through object graph, but room grouping may need extra logic. |
| "describe the building hierarchy" | Weak; object graph is not an adaptive zone tree. |

Adapter needed:

| Adapter | Description |
|---|---|
| Data adapter | Use posed RGB-D frames from Replica/ScanNet pilot scene. |
| Graph export adapter | Extract object captions, object geometry, and relation edges into a stable JSON format. |
| Query adapter | Route query through its LLM/text graph reasoning path or a local equivalent. |
| Output adapter | Convert selected graph node geometry to `bbox_3d` and answer text. |

## Internal Ablation Matrix

| Condition | View Inputs | Pose Inputs | VLM Summaries | Geometry Used? | LLM Grouping Used? | Expected Failure Mode |
|---|---|---|---|---|---|---|
| Pure Geometry | Yes | Yes | No or ignored | Yes | No | Splits large open spaces; cannot name zones semantically. |
| Pure LLM | Yes | No or ignored | Yes | No | Yes | Merges visually similar but physically separate rooms; context grows with view count. |
| Hybrid | Yes | Yes | Yes | Yes | Yes | Proposed condition; remaining errors likely from VLM hallucination or bad coverage. |

## Output Compatibility Checklist

Before running any baseline, define:

| Field | Required For | Notes |
|---|---|---|
| `scene_id` | All methods | Must map to the same source scene. |
| `query` | All methods | Use identical query strings. |
| `found` | Retrieval accuracy | Boolean must be based on shared success rule. |
| `bbox_3d` | 3D IoU | Can be absent for methods that cannot localize; absence counts separately from wrong bbox. |
| `answer_text` | Qualitative report | Keep concise and method-generated where possible. |
| `trace` | Context efficiency / interpretability | For flat methods, trace may be one step. For graph/tree methods, include visited nodes. |
| `runtime_seconds` | Scalability | Split construction time and query time. |
| `token_count` | Context efficiency | Only meaningful for LLM/VLM-driven stages. |

## Week 1 Recommendation

Do not try to run LangSplat or ConceptGraphs during Week 1 unless the headless SemanticSplat smoke test is already done. The useful Week 1 deliverable is the adapter plan above plus a saved baseline-risk list. Running baselines fairly requires normalized data, normalized queries, and normalized output JSON; otherwise results will be hard to defend.

## Week 2/3 Feasibility

| Baseline | Can run Week 2? | Can run Week 3? | Required input | Output type | Main blocker | Required adapter | Owner |
|---|---|---|---|---|---|---|---|
| LangSplat | No | Conditional smoke only | Calibrated RGB views, poses, compatible 3DGS, language features/checkpoints | Language-field relevancy and semantic localization | No local checkout/checkpoint, compatible 3DGS, or official Replica scene | Scene format, text query, relevancy-to-canonical localization | Literature / Baselines / Repo Notes Lead |
| ConceptGraphs | No | Conditional smoke only | Reliable posed RGB-D, intrinsics, segmentation/features/checkpoints | Object-centric 3D graph and geometry | `default` depth is constant; intrinsics mismatch; no local checkout/checkpoints or official Replica | RGB-D loader, graph export, query, canonical output | Literature / Baselines / Repo Notes Lead |
| LERF | No | No, optional only | Nerfstudio scene and trained language NeRF | Text relevancy field | Optional scope; no environment/checkpoint or validated scene | Nerfstudio data and relevancy-to-canonical localization | Literature / Baselines / Repo Notes Lead |
| Semantic Gaussians | No | No, optional only | Validated 3DGS and supported semantic features/models | Semantic Gaussians and segmentation/localization | Optional scope; no code/checkpoint or validated 3DGS | 3DGS/feature preparation and canonical output | Literature / Baselines / Repo Notes Lead |
| BBQ | No | No, optional only | Reliable posed RGB-D and model dependencies | Object graph, relations, selected target | Optional scope; no code/checkpoints and invalid pilot geometry | RGB-D loader, graph export, reasoning provenance, canonical output | Literature / Baselines / Repo Notes Lead |
| LEGS | No | No, optional only | Mobile robot streams/calibration and online mapping stack | Incremental language Gaussian map and localization | Different acquisition assumptions; no code/checkpoint or stream data | Stream adapter and canonical localization output | Literature / Baselines / Repo Notes Lead |

Dataset and pipeline owners support the baseline owner at their respective data and execution gates. Ownership of the comparison protocol remains with Team Lead / Metrics.

## Baseline Smoke Status

No baseline smoke result is claimed. Repository audit found local paper copies and planning notes, but no runnable baseline checkout, pinned environment, checkpoint, or official Replica scene. The available `backend/data/scenes/default` scene is suitable for semantic plumbing only: its depth is constant `0.1` and its intrinsics do not match RGB resolution, so it cannot support a valid 3D baseline smoke comparison.

Week 3 may run one compatible smoke subset only after prerequisites exist. It must save native output, canonical adapter output, source revision, config, and measured timing. Heavy setup must not block the main pipeline. ScanNet is explicitly postponed beyond Week 3.
