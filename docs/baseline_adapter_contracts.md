# Baseline Adapter Contracts

All adapters must emit one record per query conforming to `docs/schemas/query_result_schema.md`. Native outputs must remain available beside adapted outputs. Missing capabilities are represented as `null` plus a warning, not inferred or fabricated.

## Shared Contract

| Item | Requirement |
|---|---|
| Scene identity | Use the canonical `scene_id` from the scene manifest. |
| Query identity | Preserve `query_id`, exact query text, and benchmark bucket. |
| Mode | Use `live` for a real baseline run and `cached_live` only when replaying a saved real run. Never label an adapter fixture as live. |
| Provenance | Save baseline repository revision, config, checkpoint, environment, adapter revision, and source artifact paths. |
| Timing | Measure preprocessing, map/training, and per-query latency separately. |
| Geometry | Emit 2D/3D localization only when it is derived from a native output under a documented rule. |
| Unsupported data | Use `null`/`N/A` and add a structured warning. |
| Failure | Distinguish setup, preprocessing, detection, mapping, query, and adaptation failures. |

## LangSplat (Mandatory)

| Contract field | Definition |
|---|---|
| Input format | RGB images, calibrated camera poses, intrinsics, and a trainable or trained 3DGS scene in the baseline's supported layout. |
| Required preprocessing | Convert the canonical scene to the official LangSplat layout; train/load 3DGS; compute the required language features and masks. |
| Native output | Text relevancy rendered from language Gaussians, semantic masks/localization, and baseline-specific confidence scores. |
| Adapter output | `found`, selected view if rendered, optional `bbox_2d`, optional `bbox_3d` derived by a fixed threshold rule, confidence, timing, and a one-step language-field trace. |
| Supported queries | Simple object and visual attribute queries. |
| Unsupported queries | Native zone/hierarchy, aggregation, functional reasoning, and explicit multi-hop relations. Relational post-processing is an additional method variant. |
| Runtime expectations | GPU-heavy scene preprocessing/training; query rendering should be timed separately and is expected to be cheaper than training. No estimate is reported as measured. |
| Main blocker | No local LangSplat checkout/checkpoint, compatible 3DGS reconstruction, or official Replica scene. |
| Owner | Literature / Baselines / Repo Notes Lead; data conversion support from Dataset / 3D Ingestion Lead. |

## ConceptGraphs (Mandatory)

| Contract field | Definition |
|---|---|
| Input format | Posed RGB-D sequence with aligned depth, intrinsics, and valid metric camera poses. |
| Required preprocessing | Run the official segmentation, feature extraction, object association, map construction, captioning, and relation stages. |
| Native output | Object-centric 3D map/scene graph, object descriptions, point clusters or extents, and relation edges. |
| Adapter output | `found`, selected object/node identifier, answer text, optional 3D bbox from native geometry, confidence if native, graph-node trace, and timing. |
| Supported queries | Simple object, attribute where captions contain the attribute, and object-relational queries. |
| Unsupported queries | Native adaptive room/zone hierarchy and whole-scene aggregation unless explicitly implemented and named as an adapter extension. |
| Runtime expectations | GPU-heavy segmentation and map construction; optional LLM query cost. Construction and query time must be reported separately. |
| Main blocker | Current default scene has constant depth and intrinsics mismatch; no official Replica data or local ConceptGraphs environment/checkpoints are available. |
| Owner | Literature / Baselines / Repo Notes Lead; geometry gate owned by Dataset / 3D Ingestion Lead. |

## LERF (Optional)

| Contract field | Definition |
|---|---|
| Input format | Nerfstudio-compatible images, poses, and camera calibration. |
| Required preprocessing | Convert scene, train/load NeRF and language field, and preserve the training config. |
| Native output | Rendered text relevancy maps and language-field scores. |
| Adapter output | `found`, selected render/view, optional thresholded 2D region, optional 3D peak/region, confidence, and timing. |
| Supported queries | Simple object and visual attribute localization. |
| Unsupported queries | Native graph relations, zone/hierarchy, aggregation, and deductive functional reasoning. |
| Runtime expectations | GPU training plus rendering; all timing must be measured if run. |
| Main blocker | Optional scope, no local environment/checkpoint, and no compatible validated scene. |
| Owner | Literature / Baselines / Repo Notes Lead. |

## Semantic Gaussians (Optional)

| Contract field | Definition |
|---|---|
| Input format | Existing 3D Gaussians plus calibrated views and supported 2D semantic features, or another layout accepted by the official implementation. |
| Required preprocessing | Produce/load the baseline 3DGS, project or predict semantic features, and store feature/model settings. |
| Native output | Open-vocabulary semantic components, segmentation, and localization-like scores. |
| Adapter output | `found`, semantic region/object identifier, optional bbox from native segmentation, confidence, and timing. |
| Supported queries | Simple object, attribute when represented by the text encoder, and segmentation/localization prompts. |
| Unsupported queries | Native graph relations, room hierarchy, aggregation, and functional reasoning. |
| Runtime expectations | GPU preprocessing and inference; projection/prediction paths must be named separately. |
| Main blocker | Optional scope, unverified citation metadata, no local code/checkpoint, and no validated 3DGS scene. |
| Owner | Literature / Baselines / Repo Notes Lead. |

## BBQ (Optional)

| Contract field | Definition |
|---|---|
| Input format | Posed, calibrated RGB-D frames with reliable metric depth. |
| Required preprocessing | Build the object-centric map, select caption views, create metric/semantic relations, and configure its LLM reasoning path. |
| Native output | Object map, scene graph relations, selected target object, and deductive reasoning artifacts. |
| Adapter output | `found`, selected object, answer text, native/derived 3D bbox, graph trace, model provenance, tokens, and timing. |
| Supported queries | Simple object, attribute, relational, and complex referring-expression queries. |
| Unsupported queries | Adaptive zone hierarchy and aggregation unless an explicit extension is evaluated. |
| Runtime expectations | GPU mapping plus model-dependent query cost; no local measured runtime exists. |
| Main blocker | Optional scope, no local implementation/checkpoint, unreliable pilot geometry, and missing official Replica data. |
| Owner | Literature / Baselines / Repo Notes Lead. |

## LEGS (Optional)

| Contract field | Definition |
|---|---|
| Input format | Mobile-robot RGB/RGB-D streams, calibrated cameras, poses or bundle-adjustment inputs, and baseline-specific online mapping configuration. |
| Required preprocessing | Adapt an offline Replica sequence to the expected stream only if the official code supports it; otherwise do not claim comparability. |
| Native output | Incremental language-embedded Gaussian scene and open-vocabulary query localization. |
| Adapter output | `found`, selected region/view, optional bbox under a documented rule, confidence, map/query timing, and provenance. |
| Supported queries | Open-vocabulary simple object and long-tail object localization. |
| Unsupported queries | Native room hierarchy, graph relations, aggregation, and deductive functional reasoning. |
| Runtime expectations | GPU online reconstruction/training; map update and query latency must be separated. |
| Main blocker | Different acquisition assumptions, optional scope, and no local code/checkpoint or robot-stream data. |
| Owner | Literature / Baselines / Repo Notes Lead. |

## Adapter Acceptance Gate

An adapter is runnable only when it has a command, pinned source revision, machine-readable config, native output fixture, canonical output fixture, schema validation, measured timing, and an explicit geometry-validity decision. Until then its status is `blocked`, not `failed` and not `completed`.
