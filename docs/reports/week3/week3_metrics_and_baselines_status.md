# Week 3 Metrics And Baselines Status

Status date: 2026-06-26.

## 1. Benchmark Status

Current benchmark: 90 queries. Verified: 50. Candidate unverified: 0. Missing GT: 40. Plan target: 150-300 verified queries, so the current gap is 100 to reach 150 and 250 to reach 300.

The benchmark has legacy query labels. The evaluator now normalizes them into Week 3 complexity strata for reporting: `simple`, `compound`, `relational`, `multi_hop`, and `functional`. No new GT was inferred or fabricated.

Details: `docs/benchmarks/benchmark_status.md`.

## 2. Metrics Status

`scripts/evaluate_results.py` now writes compact metrics with:

- `total_queries`
- `runnable_queries`
- `gt_eligible_queries`
- `schema_valid_count`
- `per_query_type` counts and hit rates when GT exists

Accuracy-style hit rates remain unavailable for `missing_gt` queries. 3D IoU remains N/A without reliable GT boxes and compatible predicted boxes.

## 3. ConceptGraphs Status

Status: `READY_WITH_WARNINGS`, one-frame smoke executed.

ConceptGraphs was run through Docker image `semanticsplat-conceptgraphs:72f5962` against one captured `ConferenceHall-capture-pilot` RGB-D frame. The run wrote native evidence, adapted one canonical result, and generated a metrics summary.

Evidence:

- `outputs/baselines/conceptgraphs_smoke_v1/native_results.json`
- `outputs/baselines/conceptgraphs_smoke_v1/query_results/q051.json`
- `outputs/baselines/conceptgraphs_smoke_v1/metrics_summary.json`
- `docs/baselines/conceptgraphs/conceptgraphs_smoke_result.md`

Result summary:

```text
native outputs = 1
canonical outputs = 1
schema-valid results = 1
accuracy-eligible results = 0
matched_object = sofa chair
confidence = 0.2810319662094116
```

This is not a five-scene SemanticSplat comparison and not an accuracy result. Query `q051` has `verification_status: missing_gt`.

Re-run command:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_conceptgraphs_smoke.ps1
```

Details: `docs/baselines/conceptgraphs/status.md`.

## 4. LangSplat Status

Status: `READY`, official sofa smoke executed.

LangSplat was run through Docker image `semanticsplat-langsplat:d70edb8` against the official pretrained sofa assets. The run rendered feature maps, wrote native evidence, adapted one canonical result, and generated a metrics summary.

Evidence:

- `outputs/baselines/langsplat_smoke_v1/native_results.json`
- `outputs/baselines/langsplat_smoke_v1/query_results/ls001.json`
- `outputs/baselines/langsplat_smoke_v1/metrics_summary.json`
- `docs/baselines/langsplat/langsplat_smoke_result.md`

Result summary:

```text
native outputs = 1
canonical outputs = 1
schema-valid results = 1
accuracy-eligible results = 0
native relevancy score = 0.4495883882045746
```

This is not a five-scene SemanticSplat comparison and not an accuracy result. The smoke query has `verification_status: missing_gt`.

Re-run command:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_langsplat_smoke.ps1
```

Details: `docs/baselines/langsplat/status.md`.

## 5. What Is Blocked

- ConceptGraphs five-scene comparison: blocked by missing multi-frame/multi-query baseline run and independent GT.
- LangSplat five-scene comparison: blocked by missing conversion/training/loading of captured scenes into LangSplat native SfM/3DGS format.
- Verified benchmark expansion: blocked by manual GT verification.
- Independent accuracy and 3D IoU: blocked by independent GT and reliable boxes/predictions.

## 6. What Is Needed From User

- Permission to clone external repos into the repo path if the team wants in-repo ConceptGraphs evidence instead of `C:/GitProjects/baseline-deps`.
- Disk/GPU availability and Docker Desktop running for future ConceptGraphs smoke and any LangSplat five-scene conversion.
- Checkpoint and dataset paths if different from the current `baseline-deps` locations.
- Manual GT verification for captured scenes.
- Decision whether the benchmark target is 150 or 300 verified queries.
