# Project Status And Scale-Up Report

Status date: 2026-06-28.

## Executive Summary

SemanticSplat / Beyond Proximity is currently a reproducible evaluation prototype, not a completed quantitative research evaluation. The strongest completed result is a test-backed manual semantic-index plus stub-mode evaluation pipeline over five captured RGB-D pilot scenes.

Current safe claim:

```text
The project has five manually captured and manually annotated RGB-D pilot scenes, canonical schemas, headless stub evaluation, baseline smoke evidence for ConceptGraphs and LangSplat, and honest metric gating. It does not yet have official Replica/ScanNet results, independent semantic accuracy, 3D IoU, or fair five-scene baseline comparisons.
```

## What We Did

### Week 1-3 Evaluation Infrastructure

- Created canonical documentation and schemas for claims, experiment design, evaluation protocol, benchmark queries, dataset ingestion, scene inventory, and reproducibility notes.
- Added a headless experiment runner and evaluator with explicit mode separation. The active evaluation plan now uses `stub` and baseline smoke paths; `live` and `cached_live` are not part of the next phase.
- Added compact evaluator metrics: total/runnable/GT-eligible/schema-valid counts and per-query-type coverage.
- Preserved mode separation so stub or simulated outputs are not reported as provider-backed model results.
- Added validation scripts for scene geometry, view selection, semantic index validation, and baseline adapters.
- Kept generated junk, raw archives, caches, and large raw files out of the committed evidence set.

Evidence:

- `scripts/run_experiment.py`
- `scripts/evaluate_results.py`
- `docs/benchmarks/evaluation_protocol.md`
- `docs/benchmarks/benchmark_status.md`
- `docs/project/final_week3_acceptance.md`

### Captured Scene Dataset

- Imported five PLY assets into a normalized backend layout.
- Audited the PLY-only scenes and confirmed they lack RGB/depth/pose/intrinsics/semantic GT/instance GT/GT boxes.
- Hardened the manual Spark.js viewer capture workflow.
- Captured five RGB-D pilot scenes manually.
- Validated 96 RGB-D/pose records across the five capture directories.
- Built and validated manual semantic indexes and trees for all five captured scenes.

Current captured-scene counts:

| Item | Count |
|---|---:|
| Captured scenes | 5 |
| RGB-D captured views | 96 |
| Manual ViewJSON annotations | 96 |
| Semantic items | 1,046 |
| Complete semantic trees | 5 |
| Semantic-index executable scenes | 5/5 |
| Geometry-evaluation-ready scenes | 0/5 |

Evidence:

- `docs/datasets/scene_inventory.md`
- `docs/datasets/dataset_validation_report.md`
- `docs/validation/semantic_index/`
- `backend/data/scenes/*-capture*/views/`

### Stub Evaluation

- Ran a five-scene stub semantic gate.
- Produced 40/40 available, schema-valid stub results for the five captured scenes.
- Confirmed zero model calls and zero cache hits in stub mode.
- Kept all five-scene benchmark queries outside accuracy denominators because they lack independent GT.

Current benchmark status:

| Item | Count |
|---|---:|
| Total benchmark queries | 90 |
| Verified queries | 50 |
| Five-scene missing-GT queries | 40 |
| Accuracy-eligible five-scene results | 0 |
| Plan target | 150-300 verified queries |

Evidence:

- `docs/benchmarks/benchmark_queries_v1.json`
- `docs/benchmarks/benchmark_status.md`
- `outputs/week3/final_stub_semantic_gate_v1/`

### Baseline Smokes

ConceptGraphs:

- Ran a one-frame Docker smoke on `ConferenceHall-capture-pilot`.
- Converted one captured RGB-D frame to ConceptGraphs-compatible layout.
- Ran native detection, native mapping, native CLIP retrieval query, and canonical adaptation.
- Produced one native output and one canonical schema-valid query result.
- Documented the remaining warning: ConceptGraphs writes the map artifact, then its internal report generation exits with `KeyError: 'Sort Key'`.

LangSplat:

- Built and ran a Docker smoke against official pretrained sofa assets.
- Rendered/queryed official LangSplat feature output.
- Produced one native output and one canonical schema-valid query result.

Baseline status:

| Baseline | Current result | Main caveat |
|---|---|---|
| ConceptGraphs | 1 one-frame captured-scene smoke result | Not a multi-frame/five-scene comparison; no GT accuracy |
| LangSplat | 1 official-sofa smoke result | Not run on captured SemanticSplat scenes; no GT accuracy |

Evidence:

- `outputs/baselines/conceptgraphs_smoke_v1/native_results.json`
- `outputs/baselines/conceptgraphs_smoke_v1/query_results/q051.json`
- `outputs/baselines/langsplat_smoke_v1/native_results.json`
- `outputs/baselines/langsplat_smoke_v1/query_results/ls001.json`
- `docs/baselines/baseline_status.md`

### Git Delivery

- Pushed Week 3 metrics and LangSplat smoke evidence to `BearAx/beyond-proximity` on branch `week2-week3-evaluation-pipeline`.
- Pushed ConceptGraphs smoke evidence on branch `week3-conceptgraphs-smoke`.

Recent pushed commits:

```text
026ac69 feat: add week3 metrics and baseline smoke evidence
453c18d feat: add conceptgraphs smoke evidence
```

## Current Limitations

### Scientific / Metric Limitations

- No independent semantic GT exists for the five captured scenes.
- Manual ViewJSON and tree annotations are semantic-index inputs, not independent ground truth.
- No 3D GT boxes, masks, or independent object instances exist.
- No predicted 3D boxes from the main SemanticSplat query pipeline are validated.
- Therefore semantic accuracy, negative-query correctness, 3D localization, and 3D IoU remain unavailable.
- Current five-scene results are stub-mode coverage/schema/runtime results, not provider-backed model reasoning results.

### Out-Of-Scope: Live / Cached-Live

- There is no successful verified `mode: live` query result in the project.
- There is no verified live response cache, so `cached_live` replay cannot be claimed.
- Live and cached-live evaluation are no longer planned for the next phase.
- Future work should focus on verified GT, fair baselines, ScanNet readiness, and 3D box evaluation instead of provider-backed live execution.

### Dataset Limitations

- The five PLY assets are local SuperSplat-style exports with unknown original provenance.
- The PLY-only scene folders have no frames, cameras, semantic labels, instance labels, or GT boxes.
- The captured scenes are manual viewer captures, not official Replica or ScanNet dataset scenes.
- Outdoor drone has a high zero-depth ratio and should be treated cautiously for any future geometry work.
- Coordinate alignment between PLY space, renderer depth, and potential dataset GT is not independently verified.

### Baseline Limitations

- ConceptGraphs has only one captured frame/query smoke result.
- ConceptGraphs still has an internal post-map report crash that should be fixed or bypassed cleanly.
- LangSplat has only an official sofa smoke, not a run on our five captured scenes.
- Neither baseline has a fair five-scene, same-query, same-GT comparison.

## What We Should Do Next

### P0: Fix Evaluation Truth Sources

1. Decide the benchmark target: 150 or 300 verified queries.
2. Create independent GT for the current five captured scenes.
3. Add a canonical GT schema and validators.
4. Separate three concepts in reports:
   `manual semantic index`, `candidate GT`, and `verified independent GT`.
5. Do not promote any existing manual ViewJSON/tree label to GT without separate review.

### P1: Build Verified Benchmark And GT

1. Expand the benchmark toward 150-300 verified queries.
2. Add independent semantic GT for the current five captured scenes or the first official dataset scene.
3. Add a canonical GT schema and validator before reporting accuracy.
4. Keep `missing_gt` and `candidate_unverified` entries outside accuracy denominators.
5. Use manual semantic indexes only as retrieval/index inputs, not as independent GT.

### P2: Expand Baselines

ConceptGraphs:

- Fix the `KeyError: 'Sort Key'` internal report crash or make the report step optional upstream in a documented way.
- Run all frames for one captured scene.
- Run 5-10 queries for that scene.
- Convert every result to the canonical schema.
- Then expand to all five captured scenes only if the one-scene run is stable.

LangSplat:

- Convert the five captured scenes into LangSplat-compatible SfM/3DGS layout.
- Train or load compatible 3DGS/LangSplat assets for each captured scene.
- Run the same query set as SemanticSplat.
- Convert relevancy/segmentation outputs to canonical result records.

### P3: Improve Main Pipeline

- Replace or supplement manual semantic-index construction with a reproducible headless VLM/LLM pipeline.
- Keep `stub` mode for regression tests, but report it separately.
- Wire coverage-greedy view selection into evaluation configs instead of relying only on existing manual views.
- Add predicted 2D boxes and depth-unprojected 3D boxes with documented coordinate conventions.

## What We Need To Scale To ScanNet

ScanNet should be treated as a new dataset integration phase, not a small config edit.

### Data And Licensing

- Confirm ScanNet license/access and store raw data outside git.
- Select an initial small subset before scaling, for example 2-5 scenes.
- Record official scene IDs and dataset version.
- Keep raw scans, videos, meshes, labels, and generated preprocessing artifacts out of git unless intentionally small.

### Required ScanNet Modalities

For each selected ScanNet scene we need:

- RGB frames.
- Depth frames.
- Camera intrinsics.
- Camera poses.
- Official mesh or point cloud.
- Semantic labels.
- Instance labels.
- Axis-aligned object boxes if available, or a reproducible derivation from instance meshes/segments.
- Room/region labels if the planned queries require room/zone answers.

### Canonical Import Adapter

Create a dedicated ScanNet importer, likely:

```text
scripts/import_scannet_scene.py
```

It should produce a canonical scene layout:

```text
backend/data/scenes/scannet/<scene_id>/
  rgb/
  depth/
  poses.json or transforms.json
  intrinsics.json
  metadata.json
  labels/
  instances/
  gt_boxes.json
  scene_manifest.json
```

The importer must:

- Preserve official scene IDs.
- Normalize paths and coordinate conventions.
- Convert depth units explicitly.
- Validate RGB/depth/pose frame alignment.
- Write provenance: source files, commands, dataset version, checksums, and frame sampling.
- Avoid fabricating missing labels or boxes.

### ScanNet Validation

Extend validators to check:

- RGB/depth counts match.
- Intrinsics match frame resolution.
- Pose matrices are finite and valid.
- Depth has usable nonzero coverage.
- Mesh/point cloud coordinate frame matches camera poses.
- Semantic labels and instance labels load correctly.
- GT boxes match scene coordinate frame and label vocabulary.
- Sampled frames cover the annotated scene.

### ScanNet Benchmark Design

For ScanNet, we need a new benchmark split:

```text
docs/benchmarks/benchmark_queries_scannet_v1.json
```

The benchmark should include query strata:

- simple object;
- attribute;
- relational;
- multi-hop;
- functional;
- negative.

Each query should have:

- scene_id;
- query string;
- query_type;
- expected object/instance ids;
- expected labels;
- expected room/region if available;
- expected 3D box ids if applicable;
- verification status;
- annotator/reviewer provenance.

### Compute And Baseline Requirements

ScanNet scale-up needs:

- Enough disk for raw ScanNet data and derived RGB-D/mesh/label artifacts.
- GPU capacity for VLM/LLM indexing and baseline preprocessing.
- Batch scripts that run without UI/Cursor.
- Baseline-specific adapters:
  - ConceptGraphs: ScanNet/posed RGB-D loader, segmentation preprocessing, graph export.
  - LangSplat: ScanNet-to-SfM/3DGS conversion or compatible trained scene assets.
- Runtime logging for construction time, query time, memory, and failures.

### Minimum ScanNet Acceptance Gate

Do not claim ScanNet evaluation until:

- At least one official ScanNet scene imports successfully.
- Geometry validation passes.
- Labels/instances/boxes are loaded and validated.
- At least 10-20 GT-backed queries exist.
- Stub, baseline, and evaluator outputs are reproducible from commands.
- Metrics clearly separate semantic accuracy from 3D localization/IoU.

## What We Need To Create GT Boxes

GT boxes must be independent of the SemanticSplat predictions and manual semantic-index text. They can come from official dataset annotations or from a separate manual annotation process.

### Preferred Source: Official Dataset Boxes

For ScanNet, prefer official or derivable object instances:

- Use official semantic and instance labels.
- Derive per-instance 3D boxes from instance meshes/point clouds if official boxes are unavailable.
- Store both axis-aligned and, if needed later, oriented boxes.
- Preserve ScanNet label ids, instance ids, and scene coordinates.

### Manual GT Box Workflow For Captured Pilot Scenes

If we need GT boxes for the current five captured scenes, create an explicit annotation workflow:

1. Choose an annotation tool that can display the scene point cloud/mesh/splat-derived point sample plus camera views.
2. Export boxes in a documented coordinate frame.
3. Annotate only visible, stable objects relevant to benchmark queries.
4. Record object label, instance id, box center, extents, orientation if available, annotator, reviewer, and source views.
5. Require a second-pass review before marking a box verified.
6. Validate each box against projected views and depth.
7. Keep uncertain boxes as `candidate_unverified`, not GT.

### Proposed GT Box Schema

Create:

```text
docs/schemas/gt_boxes_schema.md
```

Canonical JSON:

```json
{
  "schema_version": "semanticsplat.gt_boxes.v1",
  "scene_id": "scene_id",
  "coordinate_frame": "scene_world",
  "source": "official_dataset|manual_annotation|derived_from_instance_mesh",
  "verification_status": "candidate_unverified|verified|rejected",
  "boxes": [
    {
      "box_id": "scene_object_001",
      "label": "chair",
      "instance_id": "optional_dataset_instance_id",
      "center": [0.0, 0.0, 0.0],
      "dimensions": [1.0, 1.0, 1.0],
      "rotation": [1.0, 0.0, 0.0, 0.0],
      "box_type": "axis_aligned|oriented",
      "visible_in_views": ["v001"],
      "annotator": "name_or_id",
      "reviewer": "name_or_id",
      "notes": ""
    }
  ]
}
```

### Required GT Box Validator

Create:

```text
scripts/validate_gt_boxes.py
```

It should check:

- Schema version.
- Unique `box_id`.
- Valid scene id.
- Finite numeric center/dimensions/rotation.
- Positive dimensions.
- Known coordinate frame.
- Valid label vocabulary.
- Referenced view ids exist.
- Box extents are plausible for the scene scale.
- Verification status is not promoted without reviewer metadata.

### Predicted Boxes Are Also Required

GT boxes alone are not enough for 3D IoU. The pipeline also needs predicted boxes:

- Generate a 2D bbox or mask for the selected object/view.
- Use valid depth and intrinsics to unproject to 3D.
- Transform into the same scene coordinate frame as GT.
- Save predicted `bbox_3d` in each `query_result.json`.
- Validate predicted box coordinate frame and dimensions.

Only then can `scripts/evaluate_results.py` compute or accept 3D IoU.

## Next Milestone Proposal

### Milestone A: GT-Backed Pilot Accuracy

Goal: report first real semantic accuracy on current captured scenes.

Acceptance:

- 50-100 verified GT-backed queries across the five captured scenes.
- No 3D IoU claim yet unless boxes exist.
- Stub and baseline results are reported separately.

### Milestone B: 3D Box Pilot

Goal: enable first 3D localization metric.

Acceptance:

- `gt_boxes.json` for at least one captured scene.
- Predicted `bbox_3d` in canonical query results.
- Validator passes.
- Evaluator reports non-null 3D IoU for eligible queries only.

### Milestone C: ScanNet Pilot

Goal: import and evaluate official dataset scenes.

Acceptance:

- 1-2 official ScanNet scenes imported.
- Official labels/instances/boxes validated.
- 10-20 verified queries.
- Reproducible command-only run.
- No manual UI/Cursor dependency in the evaluation path.

## Claims We Still Must Not Make

- No official ScanNet result exists yet.
- No independent semantic accuracy exists for the five captured scenes yet.
- No 3D localization / 3D IoU metric exists yet.
- Live and cached-live evaluation are out of scope for the next phase.
- No fair baseline head-to-head comparison exists yet.
- Manual semantic indexes are not independent GT.

## Immediate Action Checklist

1. Add `gt_boxes_schema.md` and `validate_gt_boxes.py`.
2. Choose GT target: current captured scenes first, or ScanNet official boxes first.
3. Verify 40 five-scene queries manually and promote defensible entries from `missing_gt` to `candidate_unverified`, then `verified`.
4. Expand ConceptGraphs beyond one frame/query.
5. Convert one captured scene into LangSplat-native format.
6. Start ScanNet only after GT schema/validator and one local GT-backed pilot are stable.
