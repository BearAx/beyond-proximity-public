# Publication and Delivery Timeline

The schedule prioritizes a reproducible Replica-only evaluation path. ScanNet scaling is postponed and is not a Week 3 acceptance criterion.

## Week 2 Milestones

| Deadline | Deliverable | Acceptance evidence | Status |
|---|---|---|---|
| Mid-week | Canonical schemas and 50-query benchmark | Schema docs, unique query IDs, validated expected semantic-index IDs | Complete |
| Mid-week | Headless deterministic runner | Command-driven stub run with logs, config, canonical per-query outputs, resume behavior | Complete |
| End-week | Evaluator and report templates | Coverage-aware metrics/failure reports; 3D metrics gated to `N/A` | Complete |
| End-week | Replica ingestion and validation tools | Importer, geometry validator, scene inventory, validation evidence | Complete for available `default`; official Replica blocked |
| End-week | One baseline smoke setup | Pinned baseline revision, environment/config, adapter fixture, or explicit blocker | Blocked and documented: no local baseline assets or valid Replica geometry |

## Week 3 Milestones

| Deadline | Deliverable | Acceptance evidence | Status |
|---|---|---|---|
| Early week | Coverage-greedy view selection | K=10/20/50/100 report and random/trajectory comparison | Complete for `default` pose proxy |
| Mid-week | Improved reproducible batch | Full query batch with schema validation, retries/resume, and failure accounting | Stub prototype complete; live provider blocked |
| Mid-week | Live/cached-live provider path | Real provider adapter plus provenance-safe cache replay | Interface/cache implemented; provider adapter and credentials absent |
| End-week | Baseline smoke result if feasible | Native and adapted outputs for a compatible query subset | Conditional; must not block the main pipeline |
| End-week | Results/failure report refresh | Bucketed coverage, accuracy, timing, tokens, and explicit unavailable metrics | Stub report available; real comparative report pending |

## Baseline Milestones

| Order | Milestone | Exit condition |
|---:|---|---|
| 1 | Select smoke baseline | Prefer ConceptGraphs when reliable posed RGB-D Replica data exists; otherwise LangSplat if a compatible 3DGS is available. |
| 2 | Pin environment | Record repository URL/revision, environment lock/export, checkpoint identity, and hardware. |
| 3 | Implement adapter | Save native output and canonical schema output for the same query. |
| 4 | Run smoke subset | Use compatible simple-object queries first; record failures and measured times. |
| 5 | Expand comparison | Only after scene geometry and GT support the requested metrics. |

## Figure and Table Deadlines

| Deadline | Artifact | Data gate |
|---|---|---|
| Week 2 end | Pipeline/reproducibility diagram | Modes and stage boundaries verified against code. |
| Week 3 mid | Dataset/coverage table | Scene validation and K-selection JSON generated. |
| Week 3 end | Query-bucket/failure table | Live or clearly labeled stub results with coverage. |
| After first baseline smoke | Baseline compatibility table | Native/adapted outputs and measured timing exist. |
| After reliable GT | 3D localization table | Reliable depth, calibrated intrinsics, and independent object GT exist. |

## Risks

- Official Replica data is not present locally, so data-dependent baseline work is blocked.
- Constant `0.1` depth and intrinsics mismatch in `default` invalidate 3D localization metrics.
- Live provider execution lacks an installed provider adapter and credentials.
- Baseline GPU environments, checkpoints, and source revisions are absent.
- Expected semantic-index labels are not independent GT and cannot support final paper accuracy claims.
- Heavy baseline setup can consume Week 3 without improving the core evaluator; stop after a documented blocker when prerequisites are absent.

## Postponed Work

- ScanNet ingestion, scaling, and ScanNet acceptance criteria are postponed beyond Week 3.
- Full NoField view selection is optional future work; the current policy is a documented pose-coverage proxy.
- Full multi-scene baseline comparison and statistically reliable 3D localization wait for validated Replica scenes and GT.
