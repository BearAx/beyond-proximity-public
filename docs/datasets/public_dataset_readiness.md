# Public Dataset Readiness Audit

Generated: 2026-07-11T10:23:22.572966+00:00

## Summary

- Captured pilot scenes: 5
- Captured pilot ViewJSON annotations: 97
- Legacy demo scenes: 1
- Legacy demo ViewJSON annotations: 19
- Replica-style local folders: 1
- Official/public Replica scenes ready: 8
- Imported official Replica BBQ scenes ready: 8
- Imported official Replica GT object boxes: 575
- ScanNet local folders: 0
- ScanNet folders ready for conversion: 0

## Decision

- Keep the five captured scenes as pilot/system evidence.
- Use the eight imported official Replica BBQ scenes as the first public-dataset workshop extension.
- Add ScanNet after official ScanNet Terms-of-Use approval; ScanNet still requires licensed data access and a completed converter.
- Do not call local `data/replica/pilot_scene_001` an official Replica result unless its source metadata changes to an official dataset scene.

## Manual Captured Scenes

| Scene | Category | ViewJSON | Frames | Tree | Manual bbox GT v2 |
|---|---|---:|---:|---|---|
| `ConferenceHall-capture-pilot` | `captured_pilot` | 20 | 20 | True | True |
| `default` | `legacy_demo` | 19 | 22 | True | False |
| `Museume-capture` | `captured_pilot` | 20 | 20 | True | True |
| `outdoor-drone-capture` | `captured_pilot` | 16 | 16 | True | True |
| `outdoor-street-capture` | `captured_pilot` | 21 | 21 | True | True |
| `replica_office0` | `other` | 1 | 1 | True | False |
| `replica_office1` | `other` | 1 | 1 | True | False |
| `replica_office2` | `other` | 1 | 1 | True | False |
| `replica_office3` | `other` | 1 | 1 | True | False |
| `replica_office4` | `other` | 1 | 1 | True | False |
| `replica_room0` | `other` | 1 | 1 | True | False |
| `replica_room1` | `other` | 1 | 1 | True | False |
| `replica_room2` | `other` | 1 | 1 | True | False |
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

| Scene | Status | Missing |
|---|---|---|
| N/A | `NOT_PRESENT` | color, depth, pose, intrinsic |

## What Must Be Supplied For Public-Dataset Claims

- For Replica object-grounding claims: the imported `backend/data/scenes/replica_*` scenes and their official GT object boxes are ready.
- For Replica segmentation claims: add a semantic/instance segmentation evaluator over the official mesh labels.
- For ScanNet claims: provide official ScanNet extracted scene folders after accepting ScanNet terms.
- For ScanNet language-grounding claims: add Sr3D+, Nr3D, and/or ScanRefer labels mapped to ScanNet object IDs.
- Baseline outputs generated on the same public scenes, not only smoke scenes.
