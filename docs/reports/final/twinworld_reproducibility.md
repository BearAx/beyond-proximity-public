# TwinWorld reproducibility freeze (Person 4)

Status date: 2026-07-14. Branch: `week6-person4`.

## Commit hash

Recorded at freeze time (update after each intentional push):

```
PLACEHOLDER_WILL_BE_FILLED
```

Paper path: `papers/twinworld/main.tex`  
PDF: `papers/twinworld/main.pdf`

## Evidence sources (do not invent)

| Track | Path |
|---|---|
| Internal five-scene v2 | `outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/metrics_summary.json` |
| Per-query | `.../per_query_results.json` |
| Replica pilot | `outputs/public_datasets/replica_pilot_v1/` |
| ScanNet pilot | `outputs/public_datasets/scannet_pilot_v1/` |
| Claim audit | `docs/reports/final/twinworld_claim_audit.md` |
| Number gate | `docs/reports/final/twinworld_number_check.md` |

## Frozen internal numbers (from metrics_summary.json)

| Metric | Flat | Graph |
|---|---:|---:|
| Views checked (avg) | 19.4 | 4.77 |
| Input tokens (avg) | 3168.2 | 1014.26 |
| Savings | — | 75.5% views / 68.2% tokens |
| hit@1 (n=125 GT) | 0.768 | 0.68 |
| hit@3 (n=125 GT) | 0.928 | 0.808 |
| Cumulative tokens (150 q) | 475230 | 152139 |

Note: older `PERSON1_DELIVERABLE.md` roundings (19.2→5.39, hit@1 0.792) are **superseded** by the JSON above. Always prefer the JSON.

## Commands

```bash
# Figures
python -B scripts/export_paper_figures.py --out-dir papers/twinworld/figures
python -B scripts/export_twinworld_figures.py

# Cross-check numbers vs main.tex
python -B scripts/check_twinworld_numbers.py

# PDF (MiKTeX / pdflatex)
cd papers/twinworld
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Scene PNGs for qualitative/gallery figures may require:

```bash
git lfs pull --include="backend/data/scenes/*/images/v001.png,backend/data/scenes/default/images/v0*.png"
```

## Still needs team / OpenReview

- Replace `ID=XXXXX` in `main.tex` with the real OpenReview paper ID.
- Confirm ECCV 2026 author kit vs current 2024-style `eccv.sty`.
- P1/P2/P3 freeze sign-off on pilot run IDs and BBQ wording.
- Camera-ready: set `\twinworldcamerareadytrue` and fill affiliations.
