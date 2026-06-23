# Week 3 Failure Modes

Source run: `outputs/week3/week3_stub_five_scene_batch_v1/` in `stub` mode.

## Evaluator Categories

| Category | Count | Interpretation |
|---|---:|---|
| Wrong room / zone | 0 | Not measurable; no semantic query executed. |
| Wrong object | 0 | Not measurable; no semantic query executed. |
| Wrong view | 0 | Not measurable; no candidate views exist. |
| Missing object in semantic description | 0 | No semantic descriptions exist for the five scenes. |
| Bad query parsing | 0 | No model/stub semantic query path executed. |
| Bad traversal | 0 | No tree exists and no traversal was attempted. |
| Bad bbox | 0 | 3D localization was not eligible. |
| Invalid depth | 40 | Each unavailable record carries the scene-level missing-depth warning. |
| Ambiguous ground truth | 0 | Missing GT is explicit rather than treated as ambiguous. |
| Baseline adapter issue | 0 | No baseline execution occurred. |
| Missing GT | 40 | All five-scene benchmark records are excluded from accuracy metrics. |

The two nonzero counts are availability blockers, not 40 observed model failures. There were zero model calls and zero executable semantic predictions.

## Operational Blockers

| Blocker | Status | Evidence needed to clear it |
|---|---|---|
| Semantic scene inputs | blocked for all 5 | RGB frames, poses, semantic descriptions/tree, and independent GT |
| 3D evaluation | blocked for all 5 | reliable depth, matching intrinsics, poses, GT 3D boxes, and predicted boxes |
| View-selection comparison | blocked for all 5 | camera pose/frame records |
| Live provider gate | not run | configure `SEMANTICSPLAT_PROVIDER`, `SEMANTICSPLAT_MODEL`, and `SEMANTICSPLAT_API_KEY`, plus an installed provider adapter |
| Cached-live replay | not run | produce a verified raw live response cache with no secret material |
| ScanNet | postponed | separate ingestion and validation phase |

## Pipeline Behavior

- Missing provider configuration did not fail the stub gate.
- Canonical unavailable outputs were written instead of fabricated predictions.
- Missing GT records were excluded from every accuracy denominator, including negative correctness.
- 3D IoU remained `N/A` with denominator 0.
- No stub output was marked `live` or `cached_live`.
