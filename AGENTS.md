# AGENTS.md — SemanticSplat / Beyond Proximity

This file is the operating guide for Codex/Cursor agents working in this repository.
Goal: reduce repeated context loading, avoid repeated explanations, and make every change evidence-based.

---

## 1. Project identity

**Working name:** SemanticSplat / Beyond Proximity
**Current role of the system:** reproducible semantic-map evaluation prototype, not a completed live/baseline research result.

The project builds a semantic layer over captured 3D/visual scenes:

```text
captured RGB-D views
  -> ViewJSON annotations
  -> scene tree / semantic index
  -> query pipeline
  -> result JSON
  -> evaluation reports
```

Current safest honest claim:

```text
The project has a reproducible, test-backed manual semantic-index + stub evaluation prototype on five captured scenes.
It does not yet have official Replica/ScanNet evaluation, successful live model results, baseline comparisons, independent accuracy, or 3D IoU.
```

---

## 2. Critical truth rules

Do not fake or overclaim results.

### Never claim

- live model evaluation succeeded unless there is at least one real `mode: live` output;
- `cached_live` succeeded unless replay used a verified live cache and avoided provider calls;
- ConceptGraphs or LangSplat ran unless their official/native command produced output or a logged execution attempt exists;
- semantic accuracy unless there is independent Ground Truth;
- 3D IoU/localization unless GT boxes/masks and predicted boxes exist;
- Replica/ScanNet results unless official dataset scenes are actually ingested and evaluated;
- automatic/headless pipeline if manual browser capture, manual ViewJSON, or manual tree building was required.

### Use these labels exactly

```text
stub = deterministic local mode, no real model call
live = real provider/API model call
cached_live = replay of verified real live output
manual semantic index = human/Cursor-assisted annotation, not independent GT
GT = Ground Truth, expected correct answer used for accuracy
```

---

## 3. Current project status

### Strong completed evidence

```text
5 captured scenes
96 RGB-D captured views
96 manual ViewJSON annotations
1,046 semantic items
5 semantic indexes
5 generated trees
40 five-scene stub benchmark outputs
50 default-scene stub benchmark outputs
90 total benchmark queries
87 passing backend tests
```

### Current scene set

```text
backend/data/scenes/ConferenceHall-capture-pilot
backend/data/scenes/Museume-capture
backend/data/scenes/Theater-capture
backend/data/scenes/outdoor-street-capture
backend/data/scenes/outdoor-drone-capture
```

Important: `Museume-capture` is intentionally spelled this way in current data/docs unless renamed globally.

### Current blocked work

```text
live model evaluation = blocked by OpenAI API quota/billing, latest error: 429 insufficient_quota
cached_live = blocked because no verified live cache exists
ConceptGraphs = blocked / not executed unless checkout/env/smoke logs prove otherwise
LangSplat = official sofa smoke executed; five-scene comparison still blocked
Replica = not official / not completed
ScanNet = postponed
semantic accuracy = unavailable without GT
3D IoU = unavailable without GT boxes/predicted boxes
```

---

## 4. Repository map

Expected high-value paths:

```text
backend/                  backend API, query code, scene data
backend/query/            model client, live/cached/stub query logic
backend/data/scenes/      captured scenes, images, depths, poses, views, trees

frontend/                 UI / viewer
scripts/                  experiment, validation, import, adapters
configs/                  experiment configs
tests/                    backend tests

docs/project/             high-level status, final acceptance, real evaluation status
docs/benchmarks/          benchmark queries, evaluation protocol/design
docs/schemas/             result/ViewJSON/schema docs
docs/datasets/            scene inventory, capture/annotation docs
docs/validation/          capture/geometry/semantic validation evidence
docs/baselines/           ConceptGraphs/LangSplat status and blockers
docs/experiments/         stub/live/cached_live/semantic retrieval notes
docs/reports/             week reports and final reports
docs/maintenance/         cleanup/audit docs

outputs/week2/            Week 2 stub/evaluation outputs
outputs/week3/            Week 3 final gate, live attempts, baseline logs
external/baselines/       optional external baseline repos; do not commit heavy repos/checkpoints
```

---

## 5. Important docs to read first

Before making substantial changes, inspect these if present:

```text
docs/maintenance/plan_vs_project_audit.md
docs/project/final_week3_acceptance.md
docs/project/week3_results.md
docs/project/real_evaluation_status.md
docs/benchmarks/evaluation_protocol.md
docs/benchmarks/benchmark_queries_v1.json
docs/datasets/scene_inventory.md
docs/baselines/baseline_status.md
docs/validation/semantic_index/
docs/validation/capture_quality/
```

If files moved, search by name/keywords rather than guessing.

---

## 6. Original plan vs actual status

### Week 1 original goal

```text
Foundation + reproducibility.
Exit: one large scene runs end-to-end with zero human-in-the-loop and emits tree + query answer.
```

Actual status:

```text
PARTIAL.
Design docs and stub CLI exist.
Full unattended capture -> index -> tree -> query is not complete.
Manual capture and manual annotation are still required.
```

### Week 2 original goal

```text
First experiments + automatic view selection.
Exit: quantitative result on >=5 Replica scenes with automatic pipeline.
```

Actual status:

```text
PARTIAL.
Evaluation harness and benchmark exist.
Coverage-greedy view selection script exists.
But eval configs still use existing/manual views.
No official Replica >=5 scene automatic quantitative run.
No independent GT accuracy.
```

### Week 3 original goal

```text
Live/cached/baseline evaluation, ConceptGraphs + LangSplat, 2 datasets.
```

Actual status:

```text
PARTIAL.
Five manual captured scenes + semantic indexes + 40 stub outputs exist.
Live/cached are blocked; ConceptGraphs is blocked; LangSplat has only an official-sofa smoke result.
ScanNet postponed.
```

---

## 7. Ground Truth / metrics rules

GT means expected correct answer.

For a query like:

```text
Where is the staircase?
```

GT should include at least:

```json
{
  "expected_views": ["v001"],
  "expected_objects": ["stairs"],
  "expected_regions": ["stair area"],
  "expected_answer_contains": ["staircase", "left side"]
}
```

Without GT, do not report accuracy.
Report only:

```text
schema validity
availability
coverage
runtime
mode
model_call_count
cache_hit_count
```

Use `N/A` for:

```text
semantic accuracy
negative correctness
3D IoU
live token/latency/cost
baseline quality comparison
```

---

## 8. Modes and provider rules

### Environment variables for live mode

```powershell
$env:SEMANTICSPLAT_PROVIDER = "openai"
$env:SEMANTICSPLAT_MODEL = "gpt-5.5"
$env:SEMANTICSPLAT_API_KEY = "sk-..."
```

Do not commit keys.
Do not print full keys in logs.
Do not ask the user to paste keys into chat/code.
Read keys only from environment variables.

### Known live issue

Latest live attempt reached OpenAI but failed with:

```text
OpenAI HTTP 429 insufficient_quota
```

Therefore the correct status is:

```text
Live attempted but produced 0 successful results; blocked by API quota/billing.
```

Not:

```text
missing credentials
```

unless the current run actually lacks env variables.

### GPT-5-style model note

Some models do not support `temperature`.
For `gpt-5*`, `o1*`, `o3*`, `o4*`, do not send unsupported sampling params unless explicitly verified.

Avoid sending unless supported:

```text
temperature
top_p
presence_penalty
frequency_penalty
logprobs
top_logprobs
logit_bias
```

---

## 9. Common commands

### Run tests

```powershell
python -B -m pytest -q
```

If Windows temp permissions fail, use workspace-local or user AppData temp as documented in reports, but record the workaround.

### Check formatting / whitespace

```powershell
git diff --check
```

### Run Week 3 stub gate

```powershell
python -B scripts\run_experiment.py --config configs\week3_replica.yaml --mode stub --out outputs\week3\final_stub_semantic_gate_v1
python -B scripts\evaluate_results.py --benchmark docs\benchmarks\benchmark_queries_v1.json --results outputs\week3\final_stub_semantic_gate_v1\query_results --out outputs\week3\final_stub_semantic_gate_v1
```

### Run live gate after quota is available

```powershell
python -B scripts\run_experiment.py --config configs\week3_replica.yaml --mode live --limit 1 --out outputs\week3\live_gate_v1
```

### Run cached_live only after a verified live cache exists

```powershell
python -B scripts\run_experiment.py --config configs\week3_replica.yaml --mode cached_live --limit 1 --out outputs\week3\cached_live_gate_v1
```

### Validate scene geometry

```powershell
python -B scripts\validate_scene_geometry.py --scene backend\data\scenes\<scene_id> --output docs\validation\geometry\<scene_id>_geometry.json
```

### Validate semantic index

```powershell
python -B scripts\validate_semantic_index.py --scene backend\data\scenes\<scene_id> --out docs\validation\semantic_index\<scene_id>_semantic_index.json
```

---

## 10. Baseline rules

### ConceptGraphs

Do not mark as executed unless there is evidence of:

```text
repo checkout
environment setup attempt
official/demo entrypoint identified
smoke command attempted
logs saved
native or canonical output produced, or exact blocker logged
```

Expected places:

```text
external/baselines/concept-graphs/
docs/baselines/conceptgraphs/
outputs/week3/baselines/conceptgraphs/
```

### LangSplat

Do not mark as executed unless there is evidence of:

```text
repo checkout
environment setup attempt
official/demo entrypoint identified
smoke command attempted
logs saved
native or canonical output produced, or exact blocker logged
```

Expected places:

```text
external/baselines/LangSplat/
docs/baselines/langsplat/
outputs/week3/baselines/langsplat/
```

If checkout/env/checkpoints/native layout are missing, status is:

```text
blocked before successful smoke execution
```

Not:

```text
baseline ran
```

---

## 11. Documentation wording rules

### Prefer

```text
manual captured scenes
manual semantic index
stub semantic gate
schema-valid outputs
credential-independent pipeline gate
blocked by provider quota/billing
blocked because no verified live cache exists
baseline smoke attempted / blocked with exact error
not independent GT
accuracy unavailable
3D IoU unavailable
```

### Avoid unless proven

```text
fully automatic
zero human-in-the-loop
Replica evaluation
ScanNet evaluation
live reasoning result
cached_live verified
baseline comparison
semantic accuracy
3D localization
superiority
production-ready
publication-ready result
```

---

## 12. Expected audit / reporting style

When asked “what is done?”, classify requirements as:

```text
DONE
PARTIALLY_DONE
BLOCKED
NOT_DONE
DONE_BUT_INCORRECTLY_REPORTED
UNCLEAR_NEEDS_REVIEW
```

Use evidence paths.

Preferred response format:

```text
Requirement | Status | Evidence | Gap | Needed from user
```

Keep answers short unless asked for a report.

---

## 13. User-dependent decisions

Ask the user only for decisions that cannot be solved from code:

```text
API billing/quota available? -> needed for live/cached_live
Allow external repo clone? -> needed for ConceptGraphs/LangSplat
GPU/CUDA available? -> may be needed for baselines
Official Replica/ScanNet data available? -> needed for original dataset plan
Manual GT annotation allowed? -> needed for accuracy
Should scope remain manual/stub? -> needed for honest final wording
```

Do not ask the user to do code-level work unless it requires credentials, external downloads, licensing, or manual annotation.

---

## 14. Cleanup rules

Keep docs organized. Do not leave 40 unrelated files flat under `docs/`.

Preferred layout:

```text
docs/project/
docs/schemas/
docs/datasets/
docs/validation/geometry/
docs/validation/semantic_index/
docs/validation/capture_quality/
docs/benchmarks/
docs/baselines/conceptgraphs/
docs/baselines/langsplat/
docs/experiments/stub/
docs/experiments/live/
docs/experiments/cached_live/
docs/reports/week1/
docs/reports/week2/
docs/reports/week3/
docs/reports/final/
docs/maintenance/
docs/archive/
```

Before deleting:

```powershell
git clean -ndX
git clean -nd
```

Do not delete evidence files, validation reports, benchmark queries, final docs, scene data, or outputs needed for reproducibility.

Move uncertain old docs to:

```text
docs/archive/review_required/
```

---

## 15. Final safe project claim

Use this when generating reports/status summaries:

```text
SemanticSplat currently provides a reproducible, test-backed evaluation prototype over five manually captured and manually annotated RGB-D pilot scenes. It includes canonical schemas, semantic indexes, generated trees, benchmark queries, and stub-mode query evaluation. Live model evaluation was attempted but produced no successful result because the provider returned insufficient quota. cached_live replay is blocked because no verified live cache exists. ConceptGraphs is not yet a successful baseline; it requires external repo/env/checkpoint/native-layout setup. LangSplat has an official-sofa smoke result, but no five-scene SemanticSplat comparison or GT-backed accuracy. The project does not yet provide official Replica/ScanNet results, independent semantic accuracy, 3D IoU, or baseline head-to-head comparison.
```

---

## 16. Before finishing any agent task

Run or document why you cannot run:

```powershell
python -B -m pytest -q
git diff --check
git status --short
```

In the final response/report include:

```text
what changed
what evidence was produced
what remains blocked
commands run
test result
whether push was performed
```

Default: do not push.
