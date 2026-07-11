# Replica/ScanNet Dataset And GT Plan

Status date: 2026-07-11.

Owner role: Person 1, Public Dataset And GT Lead.

Current completion status: Person 1 is complete for the official Replica track.
The BBQ-aligned Replica subset has been downloaded from the official release,
imported into backend scenes, mapped to official 3D object boxes, validated, and
run through the stub object-grounding benchmark. ScanNet is not fabricated: the
official dataset still requires ScanNet Terms-of-Use approval before the raw
scenes can be downloaded and converted.

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
8. Keep ScanNet separate unless official access is approved.

## Current Audit Result

| Asset | Status | Evidence | Consequence |
|---|---|---|---|
| Five internal captured scenes | `ready_internal` | `backend/data/scenes/*-capture*`, `docs/datasets/public_dataset_readiness.md` | Useful for system evidence and demos. |
| Official Replica v1 raw data | `ready` | `data/replica_official_raw/` plus `docs/datasets/replica_official_acquisition_manifest.json` | Legal local source exists for Replica import. |
| Official Replica BBQ backend scenes | `ready` | `backend/data/scenes/replica_*` and `docs/validation/public_datasets/replica_*.json` | Public-dataset object-grounding track is runnable. |
| Official Replica GT object boxes | `ready` | `ground_truth/object_boxes_3d.json` in each Replica scene | 3D object grounding and bbox IoU can be measured. |
| ScanNet raw scenes | `license_terms_required` | Official ScanNet site requires accepting Terms of Use before download. | Do not claim ScanNet results until approved data is present. |
| Sr3D+/Nr3D/ScanRefer labels | `not_present` | No local annotation files found. | Do not claim ScanNet language-grounding metrics yet. |

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

| Dataset scene | Expected official folder | Backend scene ID after import | Status | Required next step |
|---|---|---|---|---|
| `0011_00` | `scene0011_00` | `scannet_0011_00` | `license_terms_required` | Accept ScanNet Terms of Use and download official data. |
| `0030_00` | `scene0030_00` | `scannet_0030_00` | `license_terms_required` | Accept terms and download official data. |
| `0046_00` | `scene0046_00` | `scannet_0046_00` | `license_terms_required` | Accept terms and download official data. |
| `0086_00` | `scene0086_00` | `scannet_0086_00` | `license_terms_required` | Accept terms and download official data. |
| `0222_00` | `scene0222_00` | `scannet_0222_00` | `license_terms_required` | Accept terms and download official data. |
| `0378_00` | `scene0378_00` | `scannet_0378_00` | `license_terms_required` | Accept terms and download official data. |
| `0389_00` | `scene0389_00` | `scannet_0389_00` | `license_terms_required` | Accept terms and download official data. |
| `0435_00` | `scene0435_00` | `scannet_0435_00` | `license_terms_required` | Accept terms and download official data. |

ScanNet acceptance rule:

```text
Ready only after official local data exists, the converter imports
color/depth/pose/intrinsic plus semantic/instance/object GT, and validation
reports prove the backend scene is usable.
```

## Import Contract

| Field | Replica current source | ScanNet expected source | Required for |
|---|---|---|---|
| RGB frames | Placeholder only in current object-box import | `color/` | visual overlays and rendered-view metrics |
| Depth frames | Placeholder only in current object-box import | `depth/` | RGB-D unprojection and rendered-view geometry |
| Camera intrinsics | Synthetic runner-compatible frame | `intrinsic/` | image/depth projection |
| Camera poses | Synthetic runner-compatible frame | `pose/` | image/depth projection |
| Semantic labels | Replica semantic object labels from official metadata | ScanNet semantic labels | class metrics |
| Instance/object IDs | Replica official object IDs | ScanNet aggregation/object IDs | object matching |
| 3D object boxes | Replica official `oriented_bbox` values | derived from ScanNet object vertices | Acc@k, 3D IoU |
| Query labels | 56 project queries mapped to official Replica object IDs and boxes | Sr3D+/Nr3D/ScanRefer if supplied | grounding metrics |
| Provenance | acquisition manifest plus scene source metadata | ScanNet ToU status plus conversion command | reproducibility |

Important scope note: the current Replica import is an object-box/semantic-GT
track. It is valid for object retrieval and 3D box IoU in Replica mesh
coordinates. It is not a rendered RGB-D or segmentation benchmark yet.

## GT Field Mapping

| GT target | Replica mapping | Metric enabled now | ScanNet mapping |
|---|---|---|---|
| Instance/object ID | official Replica object ID from `info_semantic.json` | `retrieval_success`, `expected_view_hit`, object hit | ScanNet aggregation/object ID after access |
| 3D object bbox | official Replica `oriented_bbox` center and size | `bbox_3d_iou`, Acc-style thresholds after threshold report is added | derived from ScanNet instance vertices |
| Semantic class | official Replica object class label | label/object checks | ScanNet semantic labels after conversion |
| Segmentation pixels/points | not evaluated by current importer | not enabled yet | ScanNet/Replica segmentation evaluator needed |
| Relational query target | simple object targets only in current pilot | not enabled yet | Sr3D+/Nr3D/ScanRefer labels needed |
| Negative queries | not included in current official Replica pilot | not enabled yet | dataset-verified absence needed |

## Benchmark Artifacts

| Artifact | Status | Notes |
|---|---|---|
| `configs/replica_benchmark.yaml` | `ready` | Runs the 8 imported Replica scenes in stub mode. |
| `configs/scannet_benchmark.yaml` | `template_terms_required` | Keep until official ScanNet access and converter are ready. |
| `docs/benchmarks/replica_scannet_pilot_queries.json` | `replica_ready` | Contains 56 verified official Replica GT queries across six raw query types. |
| `docs/datasets/replica_scannet_availability_manifest.json` | `ready_for_replica` | Structured status for Replica and ScanNet. |
| `docs/datasets/public_dataset_readiness.md` | `updated` | Generated audit of manual, Replica, and ScanNet readiness. |

## Commands Run

```powershell
python -B scripts\acquire_replica_official.py --workers 3 --extract
python -B scripts\import_replica_semantic_mesh.py --all-bbq-scenes --overwrite
python -B scripts\audit_public_dataset_readiness.py
python -B scripts\build_replica_official_queries.py
python -B scripts\run_experiment.py --config configs\replica_benchmark.yaml --mode stub --out outputs\public_datasets\replica_bbq_aligned_v3
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

## Person 1 Acceptance Check

| Requirement | Status | Evidence | Gap |
|---|---|---|---|
| Confirm local data/licensing | DONE | acquisition manifest, readiness audit | ScanNet Terms-of-Use approval still external. |
| Exact BBQ subset manifest | DONE | scene manifest above and availability JSON | None for Replica. |
| Import contract | DONE | import contract table | ScanNet converter pending. |
| GT conversion spec | DONE | GT mapping table plus importer | Segmentation evaluator still pending. |
| Pilot manifest | DONE | 56 verified Replica queries | ScanNet query labels pending. |
| Mixed query pilot | DONE | `docs/benchmarks/replica_scannet_pilot_queries.json` | Covers simple, attribute, relational, multi-hop, functional, and negative raw query types. |
| Failure labels | DONE | evaluator failure categories | None. |
| No metric without GT | DONE | Replica metrics use official boxes; ScanNet metrics not claimed | None. |

## Needed From The Team

1. Official ScanNet Terms-of-Use approval and extracted scenes if ScanNet must
   be included.
2. Sr3D+, Nr3D, and/or ScanRefer annotation files if direct ScanNet
   language-grounding metrics are required.
3. A decision on whether the next sprint prioritizes Replica segmentation
   metrics or fair external baseline comparisons first.
