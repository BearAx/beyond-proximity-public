# Week 3 Plan: Reliability, Replica Batches, And Baseline Smoke

Scope: Replica and available pilot scenes only. ScanNet remains postponed.

## Exit Criteria

- Week 2 pipeline supports retries, resume, cache provenance, and deterministic reruns.
- Multiple Replica/pilot batches produce comparable canonical reports.
- Query set grows toward 100 only when expectations can be verified.
- At least one external baseline adapter completes a smoke run or records a precise blocker.
- Week 3 report separates stub, live, cached-live, measured, and unavailable evidence.

## Work Packages

| Package | Week 3 target |
|---|---|
| Batch reliability | Resume interrupted runs; preserve raw errors; avoid overwriting complete results. |
| Consistency | Compare repeated runs and mode provenance. |
| Query coverage | Add verified queries without inventing GT. |
| Baseline smoke | Normalize one baseline output to the canonical result schema. |
| Failure analysis | Track query parsing, traversal, semantic-index, view, bbox, depth, and adapter failures. |
| Reporting | Generate updated tables and honest blockers from commands. |

## Deferred

- ScanNet ingestion and evaluation.
- Full LangSplat plus ConceptGraphs head-to-head evaluation.
- Publication-level 3D IoU until reliable GT geometry exists.
- Large-scene scalability claims beyond available Replica/pilot evidence.
