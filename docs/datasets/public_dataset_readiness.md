# Public Dataset Readiness Audit

Generated: 2026-07-05T12:31:27.469928+00:00

## Summary

- Captured pilot scenes: 5
- Captured pilot ViewJSON annotations: 97
- Legacy demo scenes: 1
- Legacy demo ViewJSON annotations: 19
- Replica-style local folders: 1
- Official/public Replica scenes ready: 0
- ScanNet local folders: 0
- ScanNet folders ready for conversion: 0

## Decision

- Keep the five captured scenes as pilot/system evidence.
- Add official Replica first for a public-dataset workshop extension.
- Add ScanNet only after Replica is reproducible; ScanNet requires licensed data access and a completed converter.
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

## ScanNet Inputs

| Scene | Status | Missing |
|---|---|---|
| N/A | `NOT_PRESENT` | color, depth, pose, intrinsic |

## What Must Be Supplied For Public-Dataset Claims

- Official Replica scene folders or a documented legal download path.
- Official ScanNet extracted scene folders after accepting ScanNet terms.
- Independent labels or dataset-provided instance/semantic annotations mapped to query GT.
- Baseline outputs generated on the same public scenes, not only smoke scenes.
