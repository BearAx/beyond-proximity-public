# Final Week 3 Acceptance

Status date: 2026-06-23.

## Required Final Wording

- live model evaluation: blocked by missing provider credentials;
- cached_live replay: blocked because no verified live response cache exists;
- stub semantic gate: measured;
- manual semantic index: manual, not independent ground truth;
- baseline smoke: ConceptGraphs blocked before execution; LangSplat official sofa smoke executed without GT-backed accuracy;
- ScanNet: postponed.

## Acceptance Table

| Requirement | Status | Evidence |
|---|---|---|
| Five captured scenes | pass | 5/5 capture reports valid |
| Five semantic indexes | pass | 5/5 reports have `semantic_eval_allowed=true` |
| Executable semantic queries | pass for stub | 40/40 available schema-valid outputs |
| Stub semantic gate | measured | `outputs/week3/final_stub_semantic_gate_v1/` |
| Live model evaluation | blocked by missing provider credentials | Missing `SEMANTICSPLAT_PROVIDER`, `SEMANTICSPLAT_MODEL`, `SEMANTICSPLAT_API_KEY` |
| Cached-live replay | blocked because no verified live response cache exists | No project cache with verified live provenance |
| ConceptGraphs smoke | blocked with exact error | Environment and checkout missing |
| LangSplat smoke | official sofa smoke executed | One native and one canonical result under `outputs/baselines/langsplat_smoke_v1/`; five-scene comparison still blocked |
| Semantic accuracy | unavailable | Manual index is not independent ground truth |
| 3D localization | `N/A` | Independent GT/predicted boxes missing |
| ScanNet | postponed | Not a Week 3 milestone |

## Counts

```text
captured scenes = 5
scenes with executable manual semantic index = 5
five-scene benchmark queries = 40
stub results = 40
live results = 0
cached_live results = 0
ConceptGraphs results = 0
LangSplat results = 1 canonical official-sofa smoke result
accuracy-eligible results = 0
3D-IoU-eligible results = 0
```

## Final Questions

| Question | Answer |
|---|---|
| How many scenes were captured? | 5. |
| How many scenes have semantic index? | 5, with 96 annotated views and 1,046 semantic items. |
| How many executable semantic queries exist? | 40 in the five-scene benchmark scope. |
| How many stub results exist? | 40 final-gate results. |
| How many live results exist? | 0; live model evaluation is blocked by missing provider credentials. |
| How many cached_live results exist? | 0; no verified live response cache exists. |
| Did cached_live replay avoid provider calls? | `N/A`; replay did not run, so provider-call avoidance is not measured. |
| Did ConceptGraphs run? | No. The checkout and `conceptgraph` environment are missing; checkpoints, preprocessing outputs, and native input layout are also missing. Official entrypoint and adapter attempts are documented with errors. |
| Did LangSplat run? | Yes, as a minimal Docker smoke on official pretrained sofa assets. It produced one native result and one canonical schema-valid result. It did not run on the five captured SemanticSplat scenes and has no GT-backed accuracy. |
| Which metrics are measured? | Capture/frame counts, semantic-index counts, result/schema/availability coverage, stub runtime, model-call count, and cache-hit count for the stub gate. |
| Which metrics are `N/A`? | Semantic accuracy, negative correctness, 3D IoU, live token/latency/cost, cached replay equivalence, ConceptGraphs quality/runtime, and LangSplat accuracy/3D IoU. |
| Which claims are not made? | No live reasoning, cached replay, semantic accuracy, 3D localization, baseline comparison, or superiority claim. |
| What remains for next week? | Credentialed live/cached gates, one pinned baseline setup with native outputs, independent semantic/3D GT, and stronger query verification. ScanNet remains postponed. |

## Commands To Clear Blocked Phases

Configure all three provider variables, then run:

```powershell
python -B scripts\run_experiment.py --config configs\week3_replica.yaml --mode live --limit 1 --out outputs\week3\live_gate_v1
```

Only after that produces a verified live cache:

```powershell
python -B scripts\run_experiment.py --config configs\week3_replica.yaml --mode cached_live --limit 1 --out outputs\week3\cached_live_gate_v1
```

## Final Decision

The credential-independent Week 3 pipeline gate passes: five scenes are capture-valid and semantically executable, and the full stub batch is reproducible. Week 3 is not complete as a live evaluation milestone because live and cached-live remain blocked, ConceptGraphs remains blocked, and LangSplat only has an official-sofa smoke rather than a fair five-scene comparison. No stub, manual annotation, or setup error is reported as live/model accuracy evidence.

## Verification

```text
py_compile = passed for all required pipeline scripts
pytest = 87 passed in 4.36s with workspace-local temp storage
git diff --check = passed
push = not performed
```

The first exact `python -B -m pytest -q` attempt hit `PermissionError: [WinError 5]` in `C:\Users\bear_\AppData\Local\Temp\pytest-of-bear_`. The same full suite passed after redirecting `TEMP` and `TMP` into `.pytest_tmp/phase_g_final`; dependencies were not changed.
