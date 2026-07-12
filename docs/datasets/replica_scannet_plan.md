# Replica/ScanNet Dataset And GT Plan

Status date: 2026-07-12.

Owner role: Person 1, Public Dataset And GT Lead.

Current completion status: Person 1 is complete for the official Replica and
ScanNet object-grounding tracks. All 16 BBQ-aligned scenes are locally acquired,
imported, mapped to official 3D boxes, and validated. The ScanNet track also has
official Nr3D/Sr3D+ target and anchor mappings plus a completed 48-query run.

## Completion Plan

1. Audit local Replica, ScanNet, GT, and benchmark assets.
2. Acquire official Replica v1 data through the official Facebook Research
   release and record provenance.
3. Import the BBQ-aligned Replica scene subset:
   `room0`, `room1`, `room2`, `office0`, `office1`, `office2`, `office3`,
   `office4`.
4. Convert Replica official `habitat/info_semantic.json` oriented object boxes
   into project `ground_truth/object_boxes_3d.json` files.
5. Build backend scene trees and official-GT ViewJSON indexes for each Replica
   scene.
6. Create a GT-backed pilot query set with expected object IDs and 3D boxes.
7. Run the Replica benchmark and compute object-grounding plus 3D IoU metrics.
8. Acquire and verify the approved eight-scene ScanNet subset.
9. Extract real RGB-D, poses, and intrinsics from each official `.sens` stream.
10. Convert official ScanNet semantic vertices, aggregation instances, and 3D
    boxes into backend scenes and validate them.
11. Acquire official Nr3D/Sr3D+ annotations, verify the BBQ totals, and map every
    target and anchor ID to official ScanNet GT.
12. Freeze a deterministic 48-query pilot and run the GT-backed benchmark.

## Current Audit Result

| Asset | Status | Evidence | Consequence |
|---|---|---|---|
| Five internal captured scenes | `ready_internal` | `backend/data/scenes/*-capture*`, `docs/datasets/public_dataset_readiness.md` | Useful for system evidence and demos. |
| Official Replica v1 raw data | `ready` | `data/replica_official_raw/` plus `docs/datasets/replica_official_acquisition_manifest.json` | Legal local source exists for Replica import. |
| Official Replica BBQ backend scenes | `ready` | `backend/data/scenes/replica_*` and `docs/validation/public_datasets/replica_*.json` | Public-dataset object-grounding track is runnable. |
| Official Replica GT object boxes | `ready` | `ground_truth/object_boxes_3d.json` in each Replica scene | 3D object grounding and bbox IoU can be measured. |
| ScanNet raw and extracted scenes | `ready` | acquisition/import manifests and local gitignored data | All eight official scenes reproduce the backend import. |
| ScanNet backend scenes and GT boxes | `ready` | `backend/data/scenes/scannet_*`, validation reports | 392/392 official instances and 39 real RGB-D views are valid. |
| Nr3D and Sr3D+ labels | `ready` | `docs/datasets/scannet_grounding_annotations_manifest.json` | 699 Nr3D rows and 661 unique Sr3D+ triplets map with zero missing IDs. |
| ScanRefer labels | `optional_not_acquired` | Official ScanRefer release is separately form-gated | Not required after the completed Nr3D/Sr3D+ deliverable; add as a later track. |

Official context:

- Replica official repository: <https://github.com/facebookresearch/Replica-Dataset>
- ScanNet official data page: <https://www.scan-net.org/ScanNet/>

## BBQ-Aligned Scene Manifest

### Replica

| Dataset scene | Raw folder | Backend scene ID | Status | GT boxes | Validation |
|---|---|---|---|---:|---|
| `room0` | `data/replica_official_raw/room_0` | `replica_room0` | `ready` | 92 | `docs/validation/public_datasets/replica_room0.json` |
| `room1` | `data/replica_official_raw/room_1` | `replica_room1` | `ready` | 54 | `docs/validation/public_datasets/replica_room1.json` |
| `room2` | `data/replica_official_raw/room_2` | `replica_room2` | `ready` | 61 | `docs/validation/public_datasets/replica_room2.json` |
| `office0` | `data/replica_official_raw/office_0` | `replica_office0` | `ready` | 64 | `docs/validation/public_datasets/replica_office0.json` |
| `office1` | `data/replica_official_raw/office_1` | `replica_office1` | `ready` | 48 | `docs/validation/public_datasets/replica_office1.json` |
| `office2` | `data/replica_official_raw/office_2` | `replica_office2` | `ready` | 91 | `docs/validation/public_datasets/replica_office2.json` |
| `office3` | `data/replica_official_raw/office_3` | `replica_office3` | `ready` | 100 | `docs/validation/public_datasets/replica_office3.json` |
| `office4` | `data/replica_official_raw/office_4` | `replica_office4` | `ready` | 65 | `docs/validation/public_datasets/replica_office4.json` |

Total imported Replica GT object boxes: 575.

Replica acceptance rule:

```text
Ready means the backend scene has official_gt ViewJSON, a tree manifest,
source_metadata.json, scene_manifest.json, object_boxes_3d.json, and a public
dataset validation report with semantic_eval_allowed=true and
geometry_eval_allowed=true.
```

### ScanNet

| Dataset scene | Official folder | Backend scene | Status | RGB-D views | GT boxes | Validation |
|---|---|---|---|---:|---:|---|
| `0011_00` | `scene0011_00` | `scannet_0011_00` | `ready` | 4 | 33 | `docs/validation/public_datasets/scannet_0011_00.json` |
| `0030_00` | `scene0030_00` | `scannet_0030_00` | `ready` | 6 | 90 | `docs/validation/public_datasets/scannet_0030_00.json` |
| `0046_00` | `scene0046_00` | `scannet_0046_00` | `ready` | 4 | 57 | `docs/validation/public_datasets/scannet_0046_00.json` |
| `0086_00` | `scene0086_00` | `scannet_0086_00` | `ready` | 3 | 30 | `docs/validation/public_datasets/scannet_0086_00.json` |
| `0222_00` | `scene0222_00` | `scannet_0222_00` | `ready` | 5 | 43 | `docs/validation/public_datasets/scannet_0222_00.json` |
| `0378_00` | `scene0378_00` | `scannet_0378_00` | `ready` | 5 | 45 | `docs/validation/public_datasets/scannet_0378_00.json` |
| `0389_00` | `scene0389_00` | `scannet_0389_00` | `ready` | 5 | 30 | `docs/validation/public_datasets/scannet_0389_00.json` |
| `0435_00` | `scene0435_00` | `scannet_0435_00` | `ready` | 7 | 64 | `docs/validation/public_datasets/scannet_0435_00.json` |

ScanNet acceptance rule:

```text
Ready means official local data exists, real color/depth/pose/intrinsic records
are imported, official semantic/instance/object GT is mapped, and both semantic
and geometry validation pass. All eight rows above satisfy this rule.
```

## Import Contract

| Field | Replica current source | ScanNet implemented source | Required for |
|---|---|---|---|
| RGB frames | Placeholder only in current object-box import | JPEG decoded from official `.sens`, resized to depth resolution | visual evidence and scene context |
| Depth frames | Placeholder only in current object-box import | zlib/raw ushort decoded from official `.sens`, stored in meters | RGB-D validation |
| Camera intrinsics | Synthetic runner-compatible frame | official depth intrinsics from `.sens` | image/depth projection |
| Camera poses | Synthetic runner-compatible frame | official camera-to-world pose composed with `axisAlignment` | common aligned frame |
| Semantic labels | Replica semantic object labels from official metadata | official labeled-mesh vertices plus ScanNet label map | GT conversion; class metrics need predictions |
| Instance/object IDs | Replica official object IDs | official aggregation group/object IDs | object matching |
| 3D object boxes | Replica official `oriented_bbox` values | AABBs over official aggregation segments in the aligned mesh | Acc@k and 3D IoU |
| Query labels | 56 project queries mapped to official Replica boxes | official Nr3D targets and unique Sr3D+ target-anchor triplets | grounding metrics |
| Provenance | acquisition manifest plus scene source metadata | acquisition/import/annotation manifests with hashes | reproducibility |

Important scope note: the current Replica import is an object-box/semantic-GT
track. It is valid for object retrieval and 3D box IoU in Replica mesh
coordinates. It is not a rendered RGB-D or segmentation benchmark yet.

## GT Field Mapping

| GT target | Replica mapping | Metric enabled now | ScanNet mapping |
|---|---|---|---|
| Instance/object ID | official Replica object ID from `info_semantic.json` | object-ID hit and Recall@1 | official ScanNet aggregation object ID, exactly matched to ReferIt3D target IDs |
| 3D object bbox | official Replica `oriented_bbox` center and size | `bbox_3d_iou`, Acc@0.1/0.25/0.5 | official segment vertices transformed by `axisAlignment`, then min/max AABB |
| Semantic class | official Replica object class label | label/object checks | raw and NYU40 classes from the official ScanNet TSV label map |
| Segmentation pixels/points | official labels available | GT conversion complete; prediction metrics not enabled | 1,689,730 official labeled vertices; mAcc/mIoU/fmIoU need independent model predictions |
| Relational query target | mixed project query targets | object grounding | 699 valid Nr3D targets and 661 unique Sr3D+ target-anchor triplets fully mapped |
| Negative queries | included in Replica pilot | not-found correctness | not part of the selected ReferIt3D grounding protocol |

## Failure Label Contract

| Label | Definition | Current scoring rule |
|---|---|---|
| `wrong_object` | Selected object ID differs from the verified target ID. | Measured for every positive GT query. |
| `wrong_relation` | Selected target does not satisfy the annotated target-anchor relation. | Defined for Sr3D+; separate relation proof awaits a relation-aware method output, so current failures are conservatively counted as `wrong_object`. |
| `wrong_view` | Selected representative view differs from the imported object assignment. | Secondary diagnostic only; the assignment is frustum-derived, not official 2D visibility GT. |
| `wrong_room_or_zone` | Selected room/zone differs from official GT. | Defined but N/A for the single-scene ReferIt3D records, which provide no room/zone target. |
| `missing_gt` | Target, anchor, label, or box cannot be mapped. | Builder hard failure; current count is 0. |
| `bad_bbox` | No valid prediction box or 3D IoU is below the declared threshold. | Missing predictions count as IoU zero and remain in Acc@k denominators. |
| `unavailable_prediction` | No executable canonical result is produced. | Coverage failure; current count is 0/48. |

## Benchmark Artifacts

| Artifact | Status | Notes |
|---|---|---|
| `configs/replica_benchmark.yaml` | `ready` | Runs the 8 imported Replica scenes in stub mode. |
| `configs/scannet_benchmark.yaml` | `ready` | Runs all 8 imported ScanNet scenes and the 48-query ReferIt3D pilot. |
| `docs/datasets/scannet_pilot_import_report.json` | `ready_tracked` | One-scene scene0011_00 import pilot: 4 RGB-D views and 33/33 official boxes. |
| `docs/benchmarks/replica_scannet_pilot_queries.json` | `replica_ready` | Contains 56 verified official Replica GT queries across six raw query types. |
| `docs/benchmarks/scannet_bbq_grounding_pilot_v1.json` | `ready_local_generated` | 24 Nr3D plus 24 Sr3D+ GT-backed queries; generated after dataset terms acceptance and not distributed in Git. |
| `docs/benchmarks/replica_scannet_room0_scene0011_pilot_v1.json` | `ready_local_generated` | Exact acceptance pilot: Replica room0 plus ScanNet scene0011_00, 20 official-GT queries; not distributed in Git. |
| `docs/benchmarks/replica_scannet_person1_pilot_manifest_v1.json` | `ready_tracked` | Public-safe count, scene, source, builder, and GT-contract record for the exact 20-query pilot. |
| `docs/datasets/replica_scannet_availability_manifest.json` | `ready` | Structured status for Replica and ScanNet. |
| `docs/datasets/public_dataset_readiness.md` | `updated` | Generated audit of manual, Replica, and ScanNet readiness. |

## Commands Run

```powershell
python -B scripts\acquire_replica_official.py --workers 3 --extract
python -B scripts\import_replica_semantic_mesh.py --all-bbq-scenes --overwrite
python -B scripts\download_scannet_official.py --out-dir data\scannet --bbq-scenes --profile full --workers 8 --retries 8 --accept-tos
python -B scripts\download_scannet_grounding_annotations.py --install-gdown --acknowledge-source-terms
python -B scripts\prepare_scannet_scene.py --all-bbq-scenes --max-views 24 --candidate-stride 5 --overwrite
python -B scripts\build_scannet_official_queries.py
python -B scripts\build_replica_scannet_pilot.py
python -B scripts\audit_public_dataset_readiness.py
python -B scripts\build_replica_official_queries.py
python -B scripts\run_experiment.py --config configs\replica_benchmark.yaml --mode stub --out outputs\public_datasets\replica_bbq_aligned_v3
python -B scripts\run_experiment.py --config configs\scannet_benchmark.yaml --mode stub
```

## Confirmed Replica Pilot Result

Output directory:

```text
outputs/public_datasets/replica_bbq_aligned_v3
```

| Metric | Value | Denominator |
|---|---:|---:|
| result output coverage | 56/56 | 56 |
| schema-valid results | 56/56 | 56 |
| accuracy-eligible results | 56/56 | 56 |
| retrieval_success | 1.0000 | 56 |
| expected_view_hit | 1.0000 | 48 |
| expected_object_id_hit | 1.0000 | 48 |
| not_found_correctness | 1.0000 | 8 |
| bbox_3d_iou | 1.0000 | 48 |
| Acc@0.1 | 1.0000 | 48 |
| Acc@0.25 | 1.0000 | 48 |
| Acc@0.5 | 1.0000 | 48 |
| estimated_input_tokens mean | 10644.8571 | 56 |
| classified failures | 0 | 56 |

This is a deterministic stub run over official Replica GT semantic boxes. It is
not live model reasoning, not ConceptGraphs/LangSplat, and not yet a fair
external baseline comparison.

## Confirmed ScanNet Pilot Result

Run: `scannet_bbq_grounding_official_gt_v2` over 24 Nr3D and 24 Sr3D+ queries.

| Metric | Value | Denominator |
|---|---:|---:|
| result/schema/GT coverage | 48/48 | 48 |
| retrieval success | 0.9375 | 48 |
| exact object-ID hit | 0.2500 | 48 |
| bbox 3D IoU, missing predictions as zero | 0.2616 | 48 |
| Acc@0.1 | 0.2917 | 48 |
| Acc@0.25 | 0.2708 | 48 |
| Acc@0.5 | 0.2500 | 48 |
| mean query runtime | 0.0025 seconds | 48 |
| mean checked views | 4.8750 | 48 |
| mean estimated input tokens | 8,889.6875 | 48 |
| total estimated input tokens | 426,705 | 48 |
| one-time eight-scene conversion runtime | 15.9741 seconds | 8 scenes |

This is an oracle-GT-map retrieval track: official ScanNet instances are the
semantic-map input and the grounding target. The low exact-object score is valid
evidence that the current lexical stub does not resolve target-anchor geometry;
it is not a semantic perception or predicted-box-localization result.

## Person 1 Acceptance Check

| Requirement | Status | Evidence | Gap |
|---|---|---|---|
| Confirm local data/licensing | DONE | Replica and ScanNet acquisition manifests, readiness audit | None for raw acquisition. |
| Exact BBQ subset manifest | DONE | scene manifest above and availability JSON | None. |
| Import contract | DONE | import contract table and both importers | None. |
| GT conversion spec | DONE | GT mapping table, official boxes, semantic label summaries | Predictions are a method/evaluation task, not missing GT. |
| Pilot manifest | DONE | exact 20-query room0 + scene0011_00 lock, plus 56-query Replica and 48-query ScanNet full pilots | None. |
| Mixed query pilot | DONE | `docs/benchmarks/replica_scannet_pilot_queries.json` | Covers simple, attribute, relational, multi-hop, functional, and negative raw query types. |
| Failure labels | DONE | failure contract table plus frozen benchmark metadata | None. |
| ScanNet language GT | DONE | exact 699 Nr3D and 661 unique Sr3D+ counts; zero missing target/anchor IDs | ScanRefer is optional and separately gated. |
| No metric without GT | DONE | reported ScanNet grounding metrics use official target IDs and boxes | mAcc/mIoU/fmIoU remain N/A without predictions. |

## Needed From The Team

No external input is needed to complete Person 1. The next work belongs to the
algorithm/evaluation and baseline roles: improve relational grounding beyond the
0.25 exact-object baseline, run fair same-query methods, and add segmentation
predictions before reporting mAcc/mIoU/fmIoU. ScanRefer can be added later after
its separate official access form; it is not required by the Person 1 acceptance
criteria once Nr3D/Sr3D+ are complete.
