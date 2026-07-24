# Phase 8/9 Paper and Artifact QA

Overall status: **PASS**

| Audit | Status | Evidence |
|---|---:|---|
| Scientific claims | PASS | `scripts/check_academic_paper.py`; frozen result JSON |
| Reproducibility | PASS | one-command build, model/seed metadata, figure generator |
| PDF structure | PASS | 8 pages; 612 x 792 pts (letter) |
| Render and visual review | PASS | all pages rendered at 90 DPI and manually reviewed |

## Page Audit

| Page | Render size | Ink ratio | Nonblank |
|---:|---:|---:|---:|
| 1 | 765 x 990 | 0.12687 | PASS |
| 2 | 765 x 990 | 0.13115 | PASS |
| 3 | 765 x 990 | 0.17796 | PASS |
| 4 | 765 x 990 | 0.13187 | PASS |
| 5 | 765 x 990 | 0.11347 | PASS |
| 6 | 765 x 990 | 0.14722 | PASS |
| 7 | 765 x 990 | 0.14402 | PASS |
| 8 | 765 x 990 | 0.13222 | PASS |

## Reproducibility

```powershell
papers\beyond-proximity\build_paper.cmd
python -B scripts\check_academic_paper.py
python -B scripts\validate_agent_semantic_benchmark.py --output outputs\agent_semantic\five_scene_four_variant_v1
python -B -m pytest -q -p no:cacheprovider tests
```

The paper names the pinned model `BAAI/bge-small-en-v1.5`, seed `20260715`,
software versions, protocol denominators, map/evidence types, and limitations.
Provider token usage unavailable from Cursor is reported as unavailable, never
as zero.
