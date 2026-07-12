# SemanticSplat Claims Register

Status date: 2026-07-12
Scope: current manual, Replica, and ScanNet evidence; historical Week 2/3 mode
labels remain where applicable.

## Status Vocabulary

| Status | Meaning |
|---|---|
| `implemented` | Code exists and is exercised by tests or a reproducible command. |
| `stub/simulated` | Deterministic local logic substitutes for model inference or ground truth. |
| `live` | A configured external model produced the saved result. |
| `cached_live` | A saved response from a prior live call was replayed without a new model call. |
| `measured` | The value was observed directly during the recorded run. |
| `planned` | Committed Week 2 or Week 3 work that is not complete. |
| `future work` | Explicitly outside Week 2 and Week 3. |

## Claim Register

| Claim | Current status | Evidence | Allowed wording |
|---|---|---|---|
| SemanticSplat stores posed views, semantic ViewJSON records, and a hierarchy. | `implemented` | `backend/io/`, `backend/tree/`, scene `default` | The prototype stores a semantic hierarchy over analyzed views. |
| Geometry utilities support spatial clustering and 2D-to-3D unprojection. | `implemented` | `backend/geometry/`, backend tests | Geometry utilities are implemented and unit-tested. |
| The current UI query flow performs live LLM/VLM reasoning. | `stub/simulated` | `backend/query/live_session.py` calls `simulate_graph_search` | The UI replays a deterministic simulated graph-search path. |
| Graph pruning reduces prompt context versus a flat scan. | `stub/simulated`, partially `measured` | Prompt token counts are computed; branch choices are simulated | On the pilot semantic index, simulated graph traversal assembles fewer prompt tokens than flat scanning. |
| Reported graph-vs-flat latency is measured model latency. | `stub/simulated` | Latency uses a formula in `backend/query/timing.py` | Reported latency is an estimate, not measured live latency. |
| Query outputs follow one canonical schema. | `implemented` for Week 2/3 runner | `scripts/run_experiment.py`, evaluator tests | New Week 2/3 outputs use `semanticsplat.query_result.v1`; legacy sessions remain legacy. |
| A Cursor-independent headless model pipeline exists. | `implemented` for `stub` and OpenAI live adapter; live run blocked on credentials | `scripts/run_experiment.py`, `backend/query/model_client.py` | The headless pipeline supports deterministic stub execution and a credential-gated OpenAI live path without Cursor/UI; no project live result exists yet. |
| Cached live model replay is reproducible. | `implemented` interface; no project cache | `CachedModelClient` tests | Verified-live cache replay is implemented, but no project cached-live result is claimed. |
| Retrieval accuracy is validated on Replica ground truth. | `measured` for oracle GT map | official 8-scene/56-query Replica pilot | Replica object retrieval is measured over official GT boxes supplied as the semantic map. |
| 3D localization is validated. | `measured` for GT-map retrieval only | Replica and ScanNet Acc@k summaries | 3D box IoU measures selection of official map boxes, not localization predicted from RGB-D. |
| SemanticSplat outperforms external baselines. | `planned` | No executable baseline comparison exists | No baseline superiority claim is allowed. |
| ScanNet grounding evaluation exists. | `measured` for oracle GT map | 8 scenes, 392 boxes, 48 Nr3D/Sr3D+ queries | Report exact object-ID hit 0.2500 and Acc@0.25 0.2708 for the lexical stub; do not call it semantic perception. |

## Publication Rule

Every table, chart, and saved result must state its mode. Simulated or cached outputs must never be presented as new live model measurements. Missing metrics are recorded as `null` or `N/A`, with a reason.
