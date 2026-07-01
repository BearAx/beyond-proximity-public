# Final Week 3 Acceptance

Status date: 2026-06-28.

## Required Final Wording

- live model evaluation: out of scope for the next phase;
- cached_live replay: out of scope for the next phase because no verified live response cache exists;
- stub semantic gate: measured;
- manual semantic index: manual, not independent ground truth;
- baseline smoke: ConceptGraphs one-frame smoke executed with warning; LangSplat official sofa smoke executed without GT-backed accuracy;
- ScanNet: postponed.

## Acceptance Table

| Requirement | Status | Evidence |
|---|---|---|
| Five captured scenes | pass | 5/5 capture reports valid |
| Five semantic indexes | pass | 5/5 reports have `semantic_eval_allowed=true` |
| Executable semantic queries | pass for stub | 40/40 available schema-valid outputs |
| Stub semantic gate | measured | `outputs/week3/final_stub_semantic_gate_v1/` |
| Live model evaluation | out of scope | 0 successful provider-backed results; not planned for the next phase |
| Cached-live replay | out of scope | No project cache with verified live provenance; not planned for the next phase |
| ConceptGraphs smoke | one-frame smoke executed with warning | One native and one canonical result under `outputs/baselines/conceptgraphs_smoke_v1/`; five-scene comparison still blocked |
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
ConceptGraphs results = 1 canonical one-frame smoke result
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
| How many live results exist? | 0; live model evaluation is out of scope for the next phase. |
| How many cached_live results exist? | 0; no verified live response cache exists and cached-live is out of scope. |
| Did cached_live replay avoid provider calls? | `N/A`; replay is not part of the next plan. |
| Did ConceptGraphs run? | Yes, as a minimal Docker smoke on one captured ConferenceHall frame. It produced one native result and one canonical schema-valid result. It did not run as a five-scene comparison and has no GT-backed accuracy. |
| Did LangSplat run? | Yes, as a minimal Docker smoke on official pretrained sofa assets. It produced one native result and one canonical schema-valid result. It did not run on the five captured SemanticSplat scenes and has no GT-backed accuracy. |
| Which metrics are measured? | Capture/frame counts, semantic-index counts, result/schema/availability coverage, stub runtime, model-call count, cache-hit count for the stub gate, and one-query baseline runtimes for ConceptGraphs/LangSplat smoke runs. |
| Which metrics are `N/A`? | Semantic accuracy, negative correctness, 3D IoU, ConceptGraphs accuracy/3D IoU, and LangSplat accuracy/3D IoU. |
| Which claims are not made? | No provider-backed live reasoning, cached replay, semantic accuracy, 3D localization, baseline comparison, or superiority claim. |
| What remains for next week? | Expanding baselines beyond one-query smoke runs, independent semantic/3D GT, stronger query verification, and ScanNet preparation after GT tooling is stable. |

## Scope Decision

Live and cached-live gates are not part of the next phase. Keep existing code paths honest if they remain in the repository, but do not spend project time on provider credentials, live calls, or cached-live replay.

## Final Decision

The credential-independent Week 3 pipeline gate passes: five scenes are capture-valid and semantically executable, and the full stub batch is reproducible. Live and cached-live are out of scope for the next phase. ConceptGraphs only has a one-frame smoke, and LangSplat only has an official-sofa smoke rather than a fair five-scene comparison. No stub, manual annotation, or setup error is reported as provider-backed model accuracy evidence.

## Verification

```text
py_compile = passed for all required pipeline scripts
pytest = 87 passed in 4.36s with workspace-local temp storage
git diff --check = passed
push = not performed
```

The first exact `python -B -m pytest -q` attempt hit `PermissionError: [WinError 5]` in `C:\Users\bear_\AppData\Local\Temp\pytest-of-bear_`. The same full suite passed after redirecting `TEMP` and `TMP` into `.pytest_tmp/phase_g_final`; dependencies were not changed.
