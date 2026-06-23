# Week 2 Failure Modes

Source run: `outputs/week2/week2_stub_default_gate_v1/` in `stub` mode.

| Category | Count | Interpretation |
|---|---:|---|
| Wrong room / zone | 1 | Stub result disagreed with an existing-tree zone expectation. |
| Wrong object | 10 | Stub result disagreed with expected semantic-index node/object evidence. |
| Wrong view | 9 | Stub selected no expected view. |
| Missing object in semantic description | 0 | Not independently measurable with current GT. |
| Bad query parsing | 0 | Stub lexical path completed; this does not validate live parsing. |
| Bad traversal | 0 | Canonical stub path completed; UI remains separately simulated. |
| Bad bbox | 0 | Not evaluated because geometry is invalid. |
| Invalid depth | 50 | Every result is geometry-gated by constant depth and intrinsics mismatch. |
| Ambiguous ground truth | 0 | Evaluator count; independent GT is nevertheless unavailable. |
| Baseline adapter issue | 0 | No baseline run was attempted. |
| Missing GT | 0 | Evaluator count; final object-level/3D GT remains unavailable at run level. |

These counts diagnose deterministic stub behavior and data eligibility only. They are not live-model failure rates. `invalid depth` is a run-level metric gate repeated on each query, not 50 independent depth defects.

The six-query `phase1_evaluator_smoke` remains a small tracked evaluator fixture and intentionally contains one wrong-view/wrong-object record. The full generated source of truth is `outputs/week2/week2_stub_default_gate_v1/failure_modes.md`.
