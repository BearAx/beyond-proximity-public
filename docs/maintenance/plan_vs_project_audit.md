# Plan vs Project Audit

Audit date: 2026-06-23
Auditor basis: `paper-publication-plan.md` (original Week 1–3 plan), adapted Week 2/3 docs under `docs/reports/` and `docs/project/`, and direct inspection of code, configs, outputs, validation artifacts, and tests.
Branch at audit time: `week2-week3-evaluation-pipeline` (dirty worktree with scene annotation / doc changes).

Non-destructive checks run during audit:

```text
pytest = 87 passed, 1 warning in 5.24s (TEMP redirected to user AppData; workspace `.pytest_tmp/audit` hit WinError 5)
git diff --check = passed (LF/CRLF warnings only)
git status = dirty; many modified capture-scene ViewJSON/tree files plus doc/config changes
```

---

## Executive Summary

- **Truly completed (with evidence):** Canonical evaluation contract (schemas, protocol, harness); headless stub experiment runner; 50-query stub gate on `default`; 90-query benchmark file (50 `default` + 40 five-scene); five manually captured RGB-D scenes (96 frames total); five manual semantic indexes (96 annotated views, 1,046 semantic items verified); five generated trees; 40/40 Week 3 stub semantic gate results; coverage-greedy view-selection script; geometry/capture/semantic validation reports; baseline adapter scripts + tests; 87 passing backend tests; honest final acceptance docs (`docs/project/final_week3_acceptance.md`).
- **Partially completed:** Dataset ingestion (PLY normalization + manual capture path, not official Replica/ScanNet); automatic view selection (implemented as script, not wired into eval pipeline — configs use `strategy: existing` manual views); query benchmark (90 queries, not 150–300; five-scene queries lack GT); failure-mode documentation; live model adapter (code + failed run, no successful result); documentation cleanup (reorg done, legacy README claims remain).
- **Blocked / partial baselines:** Live model evaluation (OpenAI HTTP 429 `insufficient_quota` in `outputs/week3/live_gate_v1/`); cached_live (no verified live cache / no `outputs/week3/model_cache/`); ConceptGraphs one-frame smoke now executed with one canonical result; LangSplat official sofa smoke executed with one canonical result; fair five-scene comparison remains blocked; 3D IoU / geometry accuracy remains blocked (no independent GT boxes); ScanNet explicitly postponed.
- **Not done (original plan scope):** Zero human-in-the-loop end-to-end pipeline; official Replica dataset experiments on ≥5 scenes; automatic view selection in production eval path; reproducible quantitative accuracy on independent GT; baseline head-to-head comparison; cross-dataset (Replica + ScanNet) results; ablations; publication-ready measured model results.
- **Incorrectly reported:** Several final docs label live evaluation as “blocked by missing provider credentials,” but `outputs/week3/live_gate_v1/run_config.json` shows configured `openai` / `gpt-5.5` and a provider HTTP 429 quota error — credentials were present, the call failed. README still foregrounds legacy simulated graph-vs-flat numbers without equally prominent “not live / not accuracy” labeling.
- **Week closure vs original plan:** Week 1 **not** fully closed. Week 2 **not** fully closed. Week 3 **not** fully closed on original exit criterion (baselines + 2 datasets). Week 3 **partially** closed on the adapted credential-independent stub gate only.
- **Week closure vs adapted manual/stub scope:** Week 1 **partially** closed (stub CLI + design docs, not unattended capture/index). Week 2 **partially** closed (50-query stub on one scene, not ≥5 Replica automatic runs). Week 3 **partially** closed (five-scene capture + semantic index + 40 stub results; live/cached_live blocked; ConceptGraphs one-frame smoke; LangSplat sofa smoke).

---

## Week 1 Audit

Original source: `paper-publication-plan.md` § Week 1 (Jun 5–11). Exit criterion: *one large scene runs end-to-end with zero human-in-the-loop and emits a tree + query answer.*

| Plan requirement | Status | Evidence path | What is actually done | Gap / problem |
| ---------------- | ------ | ------------- | --------------------- | ------------- |
| Finalize research questions / claims / target venue | PARTIALLY_DONE | `docs/project/claims.md`, `paper-publication-plan.md` §2 | Claims register with status vocabulary exists; paper plan lists venue options (WACV/CVPR/workshop) | No standalone 1-page claims sheet; target venue/deadline not locked in project docs |
| Define experimental design | DONE | `docs/benchmarks/experiment_design.md` | Canonical units, modes (`stub`/`live`/`cached_live`), Week 2–3 scope documented | Scope narrowed to pilot/manual scenes; ScanNet excluded |
| Define evaluation metrics and protocols | DONE | `docs/benchmarks/evaluation_protocol.md`, `docs/schemas/` | Versioned protocol, metric rules, 3D IoU gating, failure categories | Full metric set from design (tree coherence LLM-judge, scalability) not implemented |
| Stand up dataset ingestion (Replica + ScanNet) | PARTIALLY_DONE | `scripts/import_replica_scene.py`, `docs/datasets/scene_inventory.md`, `docs/datasets/dataset_validation_report.md` | PLY batch import to backend layout; geometry validator; manual capture pilot/batch | **No official Replica or ScanNet data.** Five “Replica” config names map to local SuperSplat PLY exports (0 RGB-D frames) plus separate manual capture dirs. ScanNet postponed |
| Reproduce pipeline on one scene fully unattended | PARTIALLY_DONE | `scripts/run_experiment.py`, `outputs/week2/week2_stub_default_gate_v1/` | Stub headless run: 50/50 schema-valid results on `default` without UI/Cursor | **Not unattended for real pipeline:** capture (R-key), ViewJSON, and tree for capture scenes are manual; UI uses `simulate_graph_search`. `default` depth is constant on 19/22 frames |
| Exit: zero human-in-the-loop tree + query | NOT_DONE | `docs/reports/week1/week1_status.md`, `docs/datasets/manual_capture_pilot.md`, `backend/query/live_session.py` | Stub CLI can answer queries deterministically from saved index | Full chain still requires manual browser capture, manual/Cursor-assisted annotation, and/or simulated UI path |

**Week 1 is not fully closed.**

Against the adapted stub/manual scope: design docs and a reproducible stub CLI on `default` exist, but the original unattended capture→index→query milestone is not met.

---

## Week 2 Audit

Original source: `paper-publication-plan.md` § Week 2 (Jun 12–18). Exit criterion: *reproducible quantitative result on ≥5 Replica scenes with the automatic pipeline.*
Adapted scope: `docs/reports/week2/week2_plan.md` (stub prototype, no ScanNet, no 3D IoU).

| Plan requirement | Status | Evidence path | What is actually done | Gap / problem |
| ---------------- | ------ | ------------- | --------------------- | ------------- |
| Implement automatic view selection (NoField or coverage-greedy) | PARTIALLY_DONE | `scripts/select_views_coverage_greedy.py`, `docs/validation/geometry/default_view_selection.json` | Deterministic coverage-greedy/random/trajectory comparison implemented and tested on pose-bearing scenes | **Not used in eval pipeline:** `configs/week2_replica.yaml` and `week3_replica.yaml` set `view_selection.strategy: existing` (manual captures). PLY-only scenes have 0 candidate views |
| First experiment batch on Replica subset (5–10 scenes) | NOT_DONE | `configs/week2_replica.yaml`, `docs/datasets/scene_inventory.md` | Config lists 5 PLY-only scene IDs; Week 2 gate actually ran on `default` only | Scenes are **not official Replica**; PLY dirs have 0 frames; no committed five-scene Week 2 quantitative run found |
| Build evaluation harness | DONE | `scripts/evaluate_results.py`, `tests/backend/test_evaluation_harness.py`, `outputs/week2/phase1_evaluator_smoke/` | Coverage-aware metrics, failure reports, schema validation | Harness works; accuracy denominators correctly gated when GT missing |
| Inspect failure cases / mitigations | PARTIALLY_DONE | `docs/reports/week3/week3_failure_modes.md`, `outputs/week2/week2_stub_default_gate_v1/failure_modes.md` | Failure taxonomy and stub-run failure counts on `default` | No live-model or multi-scene Replica failure analysis |
| Construct query benchmark v1 (~100 verified) | PARTIALLY_DONE | `docs/benchmarks/benchmark_queries_v1.json` | **90 queries total:** 50 scoped to `default` (ViewJSON/tree expectations), 40 scoped to five capture scene IDs (8 each, **no GT fields**) | Below ~100 verified target; five-scene queries not accuracy-verified |
| Exit: quantitative result on ≥5 Replica scenes, automatic pipeline | NOT_DONE | `outputs/week2/week2_stub_default_gate_v1/metrics_summary.json` | 50/50 stub completion on **one** scene; regression-style hit rates (e.g. expected_view_hit 34/43) | Metrics are **stub + ViewJSON-derived**, not independent Replica GT; single scene; not automatic capture/selection |
| Adapted exit: Cursor-independent stub CLI + mode separation | DONE | `docs/reports/week2/week2_results.md`, `outputs/week2/week2_stub_default_gate_v1/` | 50 stub results, all `mode: stub`, 3D IoU `N/A`, reproducible commands documented | This is infrastructure gate only, not scientific Replica result |

**Week 2 is not fully closed** on the original plan or on the original-adapted “≥5 scenes” quantitative bar. It **is partially closed** on the narrower Week 2 stub prototype gate (one scene, 50 queries).

---

## Week 3 Audit

Original source: `paper-publication-plan.md` § Week 3 (Jun 19–25). Exit criterion: *head-to-head numbers (ours vs. ≥2 baselines) on 2 datasets.*
Adapted / audit checklist scope from project docs and user request.

| Plan requirement | Status | Evidence path | What is actually done | Gap / problem |
| ---------------- | ------ | ------------- | --------------------- | ------------- |
| Five-scene captured / validated gate | DONE | `docs/validation/capture_quality/*_capture_check.json`, `backend/data/scenes/*-capture*/images/` | 5/5 scenes: 96 RGB + 96 depth + 96 poses; non-constant depth; valid intrinsics (2340×1170) | Capture is **manual browser R-key**, not automatic. `capture_quality` JSON for ConferenceHall still shows pre-annotation semantic_index state (stale vs current `semantic_index/` reports) |
| Semantic indexes | DONE | `docs/validation/semantic_index/*_semantic_index.json`, `backend/data/scenes/*/views/*.json` | 5/5 `semantic_eval_allowed=true`; 96 views; **1,046 semantic items** (207+225+226+169+219); complete trees | Annotations are **manual**, explicitly not independent GT |
| Benchmark / stub gate | DONE | `outputs/week3/final_stub_semantic_gate_v1/`, `docs/benchmarks/benchmark_queries_v1.json` | 40/40 available, schema-valid stub results; 0 model calls; mean runtime 0.0012 s | All 40 queries have `verification_status: missing_gt`; **0 accuracy-eligible** results |
| Live model evaluation | BLOCKED | `outputs/week3/live_gate_v1/run_config.json`, `outputs/week3/live_gate_v1/logs.json`, `backend/query/model_client.py` | Live run **attempted**: provider `openai`, model `gpt-5.5`, adapter initialized; run failed with HTTP 429 `insufficient_quota` | **No successful live query result.** Docs incorrectly say “missing credentials” — env vars were set for this run |
| cached_live replay | BLOCKED | `docs/experiments/cached_live/README.md`, no `outputs/week3/model_cache/` | Interface + tests exist (`CachedModelClient`) | No verified live cache; no cached_live output directory; provider-call avoidance not demonstrated |
| ConceptGraphs baseline smoke | BLOCKED | `docs/baselines/conceptgraphs/conceptgraphs_smoke_result.md`, `docs/baselines/baseline_status.md` | Official entrypoint shape documented; adapter script exists | No repo checkout, no `conceptgraph` conda env, no native outputs, no smoke execution |
| LangSplat baseline smoke | PARTIAL | `docs/baselines/langsplat/langsplat_smoke_result.md`, `outputs/baselines/langsplat_smoke_v1/` | Official pretrained sofa smoke executed through Docker; one native result and one canonical schema-valid result | Not run on the five captured SemanticSplat scenes; no GT-backed accuracy or 3D IoU |
| Final acceptance docs | DONE | `docs/project/final_week3_acceptance.md`, `docs/project/week3_results.md`, `docs/project/real_evaluation_status.md` | Honest counts for stub gate; explicit `N/A` for accuracy/3D IoU/baselines | Live blocker wording inaccurate (credentials vs quota) |
| No false claims about accuracy / 3D IoU / live / superiority | PARTIALLY_DONE | Final acceptance + Week 3 results docs | Final docs distinguish stub vs live and deny accuracy claims | README + legacy benchmark artifacts still present simulated latency/token/“room accuracy” charts prominently |
| Reproduce baselines (original Week 3) | PARTIALLY_DONE | `docs/baselines/baseline_status.md`, `outputs/baselines/langsplat_smoke_v1/`, `outputs/baselines/conceptgraphs_smoke_v1/` | LangSplat official sofa smoke and ConceptGraphs one-frame smoke each produced one native and one canonical result | No fair five-scene baseline comparison |
| Scale to ScanNet (original Week 3) | NOT_DONE | Multiple docs (“ScanNet postponed”) | Explicitly deferred | Not started |
| Enhance benchmark to 150–300 queries (original Week 3) | NOT_DONE | `benchmark_queries_v1.json` | 90 queries | Below target; five-scene block lacks verified expectations |

**Week 3 is not fully closed** on the original plan (baselines + 2 datasets). It is **partially closed** on the adapted credential-independent infrastructure gate: five captured scenes, five semantic indexes, 40 stub results, validation reports, and honest (mostly) final docs.

---

## Incorrect or Overclaimed Statements

### 1. Live evaluation blocked by “missing credentials”

```text
File: docs/project/final_week3_acceptance.md, docs/project/week3_results.md, docs/project/real_evaluation_status.md, docs/reports/week3/week3_failure_modes.md
Current wording: "live model evaluation: blocked by missing provider credentials" / "Missing SEMANTICSPLAT_PROVIDER, SEMANTICSPLAT_MODEL, SEMANTICSPLAT_API_KEY"
Why it is wrong/too strong: outputs/week3/live_gate_v1/run_config.json shows mode=live, provider=openai, model=gpt-5.5, status=failed with OpenAI HTTP 429 insufficient_quota. Credentials were configured; the provider was reached; no query result was saved.
Suggested corrected wording: "Live model evaluation attempted but produced 0 successful results; latest run failed with OpenAI HTTP 429 insufficient_quota. No verified live query result or cache exists."
```

### 2. “Replica” configs and scene naming

```text
File: configs/week2_replica.yaml, configs/week3_replica.yaml, docs/datasets/scene_inventory.md
Current wording: Implicit/explicit "Replica" framing in config names and import script
Why it is wrong/too strong: Five canonical backend scenes are local SuperSplat PLY exports with unknown provenance and zero RGB-D frames. Capture scenes are custom manual captures, not Replica SDK rooms.
Suggested corrected wording: "Pilot / custom SuperSplat scenes with manual capture substitute; not official Replica dataset evaluation."
```

### 3. README Results section (legacy simulated demo)

```text
File: README.md § Results, graph-vs-flat table in header
Current wording: Presents 4.1× speedup, token counts, "Room disambiguation" chart as primary Results; methodology note is secondary
Why it is wrong/too strong: Values come from simulate_graph_search / estimated latency (docs/project/claims.md, benchmark_graph_vs_flat.md), not live model measurement or independent GT accuracy
Suggested corrected wording: Label entire section "Legacy simulated demo (not live evaluation)" and link first to final_week3_acceptance.md before any numeric table
```

### 4. Week 2 “quantitative result” interpretability

```text
File: docs/reports/week2/week2_results.md, outputs/week2/week2_stub_default_gate_v1/metrics_summary.json
Current wording: Tables include expected_view_hit 34/43, expected_zone_hit 42/43 alongside "Pass" acceptance rows
Why it is wrong/too strong: Denominators are ViewJSON/tree regression labels on one pilot scene, not Replica GT; stub lexical matcher drives hits. Easy to misread as semantic accuracy.
Suggested corrected wording: Always prefix with "stub regression against manual index expectations (not independent GT accuracy)."
```

### 5. Stale capture-quality report vs current semantic state

```text
File: docs/validation/capture_quality/ConferenceHall-capture-pilot_capture_check.json
Current wording: semantic_eval_allowed=false, "ViewJSON/tree semantic index is incomplete or missing"
Why it is wrong/too strong: docs/validation/semantic_index/ConferenceHall-capture-pilot_semantic_index.json shows 20/20 annotated views, tree complete, semantic_eval_allowed=true
Suggested corrected wording: Regenerate capture_quality batch after Phase E annotation, or add note that semantic_index/ reports supersede capture_check semantic fields
```

### 6. dataset_validation_report mixed narrative

```text
File: docs/datasets/dataset_validation_report.md (§ Selector and Config Changes)
Current wording: Describes Week 3 stub run with "five skipped_ineligible" and "40 unavailable records" alongside later Phase A–E success narrative
Why it is wrong/too strong: Document merges PLY-only gate run (configs pointing at PLY dirs) with later capture-scene gate without clear chronology; reader may think final 40 results were "unavailable"
Suggested corrected wording: Split into "PLY-only import gate (0/5 executable)" vs "Capture-scene stub gate (40/40 available)" with separate output paths
```

---

## What Is Actually Strong

| Achievement | Evidence |
| ----------- | -------- |
| Five captured RGB-D scenes | `backend/data/scenes/{ConferenceHall-capture-pilot,Museume-capture,Theater-capture,outdoor-drone-capture,outdoor-street-capture}/` — 20+20+20+16+20 = 96 images/depths/poses |
| Capture validation reports | `docs/validation/capture_quality/*_capture_check.json` (5 files) |
| 96 annotated ViewJSON files | `backend/data/scenes/*-capture*/views/*.json` — 96 files counted |
| 1,046 semantic items | Sum of `semantic_item_count` in `docs/validation/semantic_index/*_semantic_index.json` |
| Five complete semantic trees | Same validation reports: `tree_complete=true`, `tree_valid=true` for all 5 |
| 90 benchmark queries (40 five-scene + 50 default) | `docs/benchmarks/benchmark_queries_v1.json` |
| 40 five-scene stub gate outputs | `outputs/week3/final_stub_semantic_gate_v1/query_results/q051.json`–`q090.json` |
| 50 default-scene stub gate outputs | `outputs/week2/week2_stub_default_gate_v1/` (50 JSON results) |
| Evaluation harness + schemas | `scripts/evaluate_results.py`, `docs/schemas/`, `tests/backend/test_evaluation_harness.py` |
| Headless stub runner | `scripts/run_experiment.py`, `configs/week3_replica.yaml` |
| Coverage-greedy selector (library) | `scripts/select_views_coverage_greedy.py`, tests in `test_dataset_ingestion.py` |
| Live adapter code (provider reached) | `backend/query/model_client.py`, failed run log in `outputs/week3/live_gate_v1/logs.json` |
| Baseline adapter contracts + tests | `scripts/adapt_*_output.py`, `tests/backend/test_baseline_adapters.py` |
| Test suite | **87 passed** (`python -B -m pytest -q`, TEMP under user AppData) |
| Documentation cleanup / index | `docs/maintenance/cleanup_report.md`, categorized `docs/` layout |
| Honest final acceptance (mostly) | `docs/project/final_week3_acceptance.md` — stub measured, accuracy 0, ConceptGraphs 0, LangSplat sofa smoke 1 |

---

## What Must Be Done Next

### P0 — must fix for honest submission

| Action | Expected evidence | Needs |
| ------ | ----------------- | ----- |
| Correct live-evaluation status docs to reflect quota failure vs missing credentials | Updated `final_week3_acceptance.md`, `week3_results.md`, `real_evaluation_status.md` with `live_gate_v1` error text | API billing / quota only if re-running live |
| Regenerate or annotate stale `capture_quality` reports after semantic annotation | Capture reports consistent with `semantic_index/` (5/5 `semantic_eval_allowed=true`) | Local script rerun |
| Ensure all public-facing docs/README distinguish **simulated demo** vs **stub gate** vs **live** | README Results reframed; no chart without mode label | Doc edit |
| Do not claim Replica/ScanNet evaluation until official data + GT exist | Scene inventory wording; config rename or explicit disclaimer | Official Replica/ScanNet download + ingestion |

### P1 — important for stronger Week 3 / original plan alignment

| Action | Expected evidence | Needs |
| ------ | ----------------- | ----- |
| Complete ≥1 successful live query + save verified cache | `outputs/week3/live_gate_v1/query_results/*.json` with `mode: live`, `model_call_count ≥ 1`; cache entry with `source_mode=live` | API quota/credentials |
| Run cached_live replay with 0 provider calls | `outputs/week3/cached_live_gate_v1/` results + logs showing cache hits | Prior live cache |
| Wire coverage-greedy (or NoField) into experiment pipeline for new captures | `run_config.json` showing `view_selection.strategy: coverage_greedy` and selection report referenced | Pose-bearing scenes |
| Add verified query expectations for five-scene benchmark (or independent GT) | Benchmark JSON with non-empty expected IDs; metrics with `accuracy_eligible_result_count > 0` | Human verification labor |
| One baseline smoke with native output → canonical adapter | `outputs/baselines/*/native_results.json` + adapted canonical results | GPU, conda env, baseline repo clone, checkpoints |
| Official Replica subset (≥5 rooms) with dataset-native RGB-D + GT | Scene inventory with official provenance; semantic/3D eval flags true against independent GT | Replica download |

### P2 — future work (Week 4+ original plan)

| Action | Expected evidence | Needs |
| ------ | ----------------- | ----- |
| ScanNet ingestion and evaluation | ScanNet scenes in inventory + results tables | ScanNet access, preprocessing |
| Ablation A/B/C runs | Frozen results under `outputs/week4/` | Live model + compute |
| 3D IoU with independent boxes | Non-null `bbox_3d_iou` in metrics summaries | GT boxes + reliable predicted boxes |
| Expand benchmark toward 150–300 verified queries | Versioned `benchmark_queries_v2.json` | Annotation effort |
| Automatic unattended capture + VLM indexing | Headless capture + provider-driven ViewJSON without Cursor | NoField/auto-capture + API |

---

## Final Verdict

```text
Are Week 1 and Week 2 fully completed according to the original plan? No.
Are they completed according to the adapted manual/stub pipeline scope? Partially — Week 1 design/stub foundation yes; unattended/automatic/Replica quantitative bars no. Week 2 stub gate on one scene yes; ≥5-scene automatic Replica quantitative bar no.
Is Week 3 complete? No — on the original plan (baselines + 2 datasets) or on live/cached_live/fair baseline comparison. Partially for the narrow adapted gate: five manual captures, five semantic indexes, forty stub results, validation artifacts, test-backed infrastructure, and one LangSplat official-sofa smoke.
What is the safest honest project claim right now?
```

**Safest honest claim:** SemanticSplat has a **reproducible, test-backed evaluation prototype** with canonical schemas, a headless **stub** query runner, **five manually captured and manually annotated** RGB-D pilot scenes (96 views, 1,046 semantic index items), a **40-query stub semantic gate** (schema-valid, zero model calls, zero accuracy-eligible GT), **blocked** live evaluation (provider reached once; failed on quota; no verified cache), **blocked** cached_live replay, **blocked** ConceptGraphs smoke, and one **LangSplat official-sofa smoke** with a canonical schema-valid result but no GT-backed accuracy. It does **not** yet have official Replica/ScanNet results, automatic unattended capture/view selection in the eval path, live model measurements, fair five-scene baseline comparisons, independent semantic accuracy, or 3D localization metrics.

---

*End of audit. No implementation, doc fixes, or git push were performed as part of this report.*
