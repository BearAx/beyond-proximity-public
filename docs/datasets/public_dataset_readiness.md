# Public Dataset Readiness Audit

Generated: 2026-07-12T06:25:39.518374+00:00

## Summary

- Captured pilot scenes: 5
- Captured pilot ViewJSON annotations: 97
- Legacy demo scenes: 1
- Legacy demo ViewJSON annotations: 19
- Replica-style local folders: 1
- Official/public Replica scenes ready: 8
- Imported official Replica BBQ scenes ready: 8
- Imported official Replica GT object boxes: 575
- ScanNet local folders: 8
- ScanNet raw scenes available: 8
- ScanNet extracted folders available: 8
- Imported official ScanNet BBQ scenes ready: 8
- Imported official ScanNet GT object boxes: 392
- Imported official ScanNet RGB-D views: 39

## Decision

- Keep the five captured scenes as pilot/system evidence.
- Use the eight imported official Replica and eight imported official ScanNet BBQ scenes as public-dataset workshop evidence.
- ScanNet Nr3D/Sr3D+ grounding is runnable over official GT object IDs and boxes; the current lexical-stub result is a method-quality baseline, not a semantic-perception result.
- Do not call local `data/replica/pilot_scene_001` an official Replica result unless its source metadata changes to an official dataset scene.

## Manual Captured Scenes

| Scene | Category | ViewJSON | Frames | Tree | Manual bbox GT v2 |
|---|---|---:|---:|---|---|
| `ConferenceHall-capture-pilot` | `captured_pilot` | 20 | 20 | True | True |
| `default` | `legacy_demo` | 19 | 22 | True | False |
| `Museume-capture` | `captured_pilot` | 20 | 20 | True | True |
| `outdoor-drone-capture` | `captured_pilot` | 16 | 16 | True | True |
| `outdoor-street-capture` | `captured_pilot` | 21 | 21 | True | True |
| `Theater-capture` | `captured_pilot` | 20 | 20 | True | True |

## Replica-Style Inputs

| Scene | Status | Source dataset | Missing | Independent GT |
|---|---|---|---|---|
| `pilot_scene_001` | `PROXY_OR_NOT_READY` | `provided_data_converted_as_replica_pilot` | rgb, depth | False |

## Imported Official Replica Scenes

| Scene | Source scene | Status | GT boxes | Semantic eval | Geometry eval |
|---|---|---|---:|---|---|
| `replica_office0` | `office0` | `READY_PUBLIC` | 64 | True | True |
| `replica_office1` | `office1` | `READY_PUBLIC` | 48 | True | True |
| `replica_office2` | `office2` | `READY_PUBLIC` | 91 | True | True |
| `replica_office3` | `office3` | `READY_PUBLIC` | 100 | True | True |
| `replica_office4` | `office4` | `READY_PUBLIC` | 65 | True | True |
| `replica_room0` | `room0` | `READY_PUBLIC` | 92 | True | True |
| `replica_room1` | `room1` | `READY_PUBLIC` | 54 | True | True |
| `replica_room2` | `room2` | `READY_PUBLIC` | 61 | True | True |

## ScanNet Inputs

| Scene | Status | Raw files | Missing extracted folders |
|---|---|---:|---|
| `scene0011_00` | `READY_FOR_CONVERSION` | 6/6 | none |
| `scene0030_00` | `READY_FOR_CONVERSION` | 6/6 | none |
| `scene0046_00` | `READY_FOR_CONVERSION` | 6/6 | none |
| `scene0086_00` | `READY_FOR_CONVERSION` | 6/6 | none |
| `scene0222_00` | `READY_FOR_CONVERSION` | 6/6 | none |
| `scene0378_00` | `READY_FOR_CONVERSION` | 6/6 | none |
| `scene0389_00` | `READY_FOR_CONVERSION` | 6/6 | none |
| `scene0435_00` | `READY_FOR_CONVERSION` | 6/6 | none |

## Imported Official ScanNet Scenes

| Scene | Source scene | Status | RGB-D views | GT boxes | Indexed boxes | Semantic eval | Geometry eval |
|---|---|---|---:|---:|---:|---|---|
| `scannet_0011_00` | `scene0011_00` | `READY_PUBLIC` | 4 | 33 | 33 | True | True |
| `scannet_0030_00` | `scene0030_00` | `READY_PUBLIC` | 6 | 90 | 90 | True | True |
| `scannet_0046_00` | `scene0046_00` | `READY_PUBLIC` | 4 | 57 | 57 | True | True |
| `scannet_0086_00` | `scene0086_00` | `READY_PUBLIC` | 3 | 30 | 30 | True | True |
| `scannet_0222_00` | `scene0222_00` | `READY_PUBLIC` | 5 | 43 | 43 | True | True |
| `scannet_0378_00` | `scene0378_00` | `READY_PUBLIC` | 5 | 45 | 45 | True | True |
| `scannet_0389_00` | `scene0389_00` | `READY_PUBLIC` | 5 | 30 | 30 | True | True |
| `scannet_0435_00` | `scene0435_00` | `READY_PUBLIC` | 7 | 64 | 64 | True | True |

## What Must Be Supplied For Public-Dataset Claims

- For Replica object-grounding claims: the imported `backend/data/scenes/replica_*` scenes and their official GT object boxes are ready.
- For Replica segmentation claims: add a semantic/instance segmentation evaluator over the official mesh labels.
- For ScanNet object-grounding claims: the eight scenes, official boxes, Nr3D/Sr3D+ labels, validation reports, and 48-query pilot are ready.
- For ScanNet semantic-segmentation claims: add independent predicted per-vertex classes; GT labels alone cannot produce mAcc/mIoU/fmIoU.
- For ScanRefer claims: obtain its separately gated official annotation release and add a frozen subset; it is optional after the completed Nr3D/Sr3D+ track.
- Baseline outputs generated on the same public scenes, not only smoke scenes.
