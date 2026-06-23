# Week 1 Status

Status date: 2026-06-21 retrospective.

## Completed

- Backend scene I/O, semantic ViewJSON storage, tree storage, geometry utilities, and query prompt builders exist.
- The pilot `default` scene contains 19 images, semantic descriptions, and tree records.
- A graph-vs-flat benchmark, report generator, charts, reasoning-style logs, and demo assets exist.
- Baseline planning and repository notes exist in `docs/baseline_*.md`, `docs/related_work_notes.md`, and `docs/repo_setup_notes.md`.
- Backend unit tests cover Nerfstudio I/O, spatial graph logic, unprojection, and simulated benchmark behavior.

## Stub / Simulated

- The UI auto-query path calls `simulate_graph_search`.
- Graph and flat branch choices in the generated benchmark are keyword-based simulations.
- Reported LLM latency is estimated from calls and prompt tokens.
- Auto-generated reasoning logs are explanatory traces, not new model responses.

## Live / Cached Live

- No provider-independent live model client is implemented.
- No canonical live or cached-live result is available.
- Existing saved sessions must not be relabelled as live without provenance.

## Measured

- Local code execution time and prompt token counts are measured by existing tools.
- Model latency, provider output tokens, and Replica retrieval accuracy are not measured.

## Dataset Limitation

The current `default` depth maps are constant-valued at `0.1`. They are loader fixtures, not reliable geometry. Real 3D localization and 3D IoU remain unvalidated.

## Transition To Week 2

Week 2 begins with canonical schemas, benchmark v1, evaluation tooling, and explicit mode separation. The implementation must preserve the demo while preventing simulated results from being reported as live evidence.
