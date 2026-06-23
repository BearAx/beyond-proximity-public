# Week 3 Failure Modes

Status date: 2026-06-23. Final credential-independent gate.

## Evaluator Outcome

| Category | Count | Interpretation |
|---|---:|---|
| Missing GT | 40 | All five-scene results are excluded from accuracy metrics. |
| Wrong room / zone | 0 | Not measurable without GT. |
| Wrong object | 0 | Not measurable without GT. |
| Wrong view | 0 | Not measurable without GT. |
| Bad query parsing | 0 | No accuracy GT exists; zero does not prove parsing correctness. |
| Bad traversal | 0 | No accuracy GT exists; zero does not prove traversal correctness. |
| Bad bbox | 0 | Geometry evaluation is ineligible. |
| Invalid depth | 0 | Capture depth is non-constant; geometry remains blocked by missing boxes/GT. |
| Baseline adapter issue | 0 | No baseline-native output reached the adapter stage. |

## Operational Blockers

| Phase | Status | Exact blocker |
|---|---|---|
| Phase C live | blocked | Missing `SEMANTICSPLAT_PROVIDER`, `SEMANTICSPLAT_MODEL`, and `SEMANTICSPLAT_API_KEY`. |
| Phase D cached-live | blocked | No verified `source_mode=live` response cache exists. |
| ConceptGraphs | blocked before execution | Missing checkout and `conceptgraph` Conda environment; checkpoints, GSA/LLaVA preprocessing, and native Replica layout are also absent. |
| LangSplat | blocked before execution | Missing checkout and `langsplat` Conda environment; pretrained 3DGS/language features/checkpoints and native layout are absent. |
| Geometry | blocked | Independent GT and predicted 3D boxes are absent. |
| ScanNet | postponed | Explicitly outside Week 3. |

## Baseline Errors

ConceptGraphs:

```text
conda run -n conceptgraph python slam/cfslam_pipeline_batch.py --help
EnvironmentLocationNotFound: Not a conda environment: C:\Users\bear_\miniconda3\envs\conceptgraph

python -B slam\cfslam_pipeline_batch.py --help
can't open file 'C:\GitProjects\beyond-proximity\slam\cfslam_pipeline_batch.py': [Errno 2] No such file or directory
```

LangSplat:

```text
conda run -n langsplat python render.py --help
EnvironmentLocationNotFound: Not a conda environment: C:\Users\bear_\miniconda3\envs\langsplat

python -B render.py --help
can't open file 'C:\GitProjects\beyond-proximity\render.py': [Errno 2] No such file or directory
```

These are setup blockers, not baseline quality failures. No result files were fabricated.
