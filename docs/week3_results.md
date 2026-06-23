# Week 3 Results

Status date: 2026-06-22. Final mode: five-scene `stub` gate. Live and cached-live were not run.

## Final Counts

| Question | Answer |
|---|---|
| Scenes added and normalized | 5 |
| Scenes passing semantic-evaluation validation | 0/5 |
| Scenes passing 3D-evaluation validation | 0/5 |
| Benchmark queries | 90 total: 50 legacy `default` with ViewJSON/tree expectations and 40 five-scene records without GT |
| Queries in the Week 3 run scope | 40 |
| Canonical query outputs written | 40/40, eight per scene |
| Queries with GT in the Week 3 run scope | 0/40 |
| Executable semantic queries | 0/40 because all five scenes have no views or semantic index |
| Run mode | `stub` |
| Live mode | not run; provider environment is absent |
| Cached-live mode | not run; no verified live response cache exists |
| ScanNet | postponed and excluded |

## Stub Gate

```powershell
python -B scripts/run_experiment.py --config configs/week3_replica.yaml --mode stub

python -B scripts/evaluate_results.py `
  --benchmark docs/benchmark_queries_v1.json `
  --results outputs/week3/week3_stub_five_scene_batch_v1/query_results `
  --out outputs/week3/week3_stub_five_scene_batch_v1
```

Output: `outputs/week3/week3_stub_five_scene_batch_v1/`.

| Gate metric | Status | Value |
|---|---|---:|
| Scoped output coverage | measured | 40/40 |
| Canonical schema validity | measured | 40/40 |
| Per-scene output coverage | measured | 8/8 for each of five scenes |
| Stub provenance | measured | 40 `stub`, 0 `live`, 0 model calls |
| Semantic accuracy | unavailable | denominator 0; no GT and no executable semantic views |
| Token usage | unavailable | `null`; no provider call occurred |
| 3D IoU | `N/A` | denominator 0; depth, cameras, GT boxes, and predictions are unavailable |

The 40 result files use the canonical query-result schema and `availability_status: unavailable`. Their `result.found: false` field is a schema placeholder accompanied by an explicit no-prediction warning; it is not scored as a negative prediction.

## Live Gate

The following required environment variables were checked without reading or recording their values:

| Variable | Present |
|---|---|
| `SEMANTICSPLAT_PROVIDER` | no |
| `SEMANTICSPLAT_MODEL` | no |
| `SEMANTICSPLAT_API_KEY` | no |

Per the live-gate rule, missing configuration did not fail the stub pipeline. No live request was attempted, no cached-live replay was attempted, no raw response cache was created, and no provider secret was saved.

## Real Evidence

- Real measured evidence: five local PLY assets imported byte-for-byte, readable PLY headers, generated metadata consistency, output-file coverage, canonical schema validity, scene/query counts, and stub provenance.
- Unavailable semantic evidence: retrieval, object, view, node, zone, relational, functional, negative, and multi-hop accuracy for the five new scenes.
- `N/A` geometry evidence: depth quality measurements, coverage from camera views, predicted 3D boxes, and 3D IoU.
- No live or cached-live quality, token, latency, or cost result is claimed.

## Remaining Blockers

- The five scenes have no RGB/depth frames, poses, intrinsics, semantic ViewJSON/tree, labels, instances, or GT 3D boxes.
- All 40 five-scene benchmark records therefore have `verification_status: missing_gt`.
- Live provider/model/key environment variables are absent, and no provider adapter or verified live cache is available.
- Numeric greedy/random/trajectory coverage comparisons require camera poses.
- Semantic and 3D accuracy require valid modalities plus independent GT.
- ScanNet remains postponed.

## Verification and Cleanup

- The required `py_compile` command passed for all seven pipeline/model scripts.
- The exact pytest command first encountered a Windows ACL error in the user-level pytest temp directory; the same command passed `57/57` after `TEMP` and `TMP` were redirected to an isolated workspace directory.
- `git diff --check` passed; Git printed only line-ending conversion warnings for pre-existing modified files.
- No tracked path is under `.venv/`, `node_modules/`, `__pycache__/`, `.pytest_cache/`, temporary extraction directories, or `outputs/`; no tracked ZIP exists.
- The retained local Week 3 gate contains 45 files totaling 113.17 KiB. It remains untracked and is reproducible from the commands above.
