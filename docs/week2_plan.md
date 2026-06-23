# Week 2 Plan: First Reproducible Evaluation Prototype

Scope: Replica and available pilot scenes only. ScanNet is postponed.

## Exit Criteria

- Canonical scene, query, result, and metrics schemas are versioned.
- Benchmark v1 contains at least 50 evidence-checked queries.
- One command runs a full stub experiment without Cursor or UI.
- Stub, live, and cached-live modes cannot be confused in outputs.
- Evaluation reports are generated from saved canonical results.
- 3D IoU is `N/A` until reliable depth and GT boxes exist.

## Work Packages

| Package | Status at start | Week 2 target |
|---|---|---|
| Evaluation contract | `implemented` | Schemas, protocol, benchmark, evaluator implemented. |
| Model client | `implemented` for stub/cache | Provider interface, deterministic stub, verified-live cache replay; live adapter blocked. |
| Headless CLI | `implemented` | Config-driven experiment command and output layout. |
| Replica ingestion | `planned` | Available pilot scenes imported and validated. |
| Query batch | `implemented` in stub mode | 50 canonical pilot results generated reproducibly. |
| Reporting | `implemented` | Metrics and failure reports generated automatically. |

## Non-Goals

- No ScanNet work.
- No baseline superiority claim.
- No full NoField integration requirement.
- No 3D metric based on constant or synthetic depth.
