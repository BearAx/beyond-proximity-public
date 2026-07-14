# TwinWorld reproducibility freeze (Person 4)

Status date: 2026-07-14. Integrated branch: `codex/week6-integration`.

## Commit hash

Person 4 evidence tip audited by integration:

```
62cf94a179f2b9f42a1cb122e0106f5ac957bdf0
(short: 62cf94a on week6-person4)
```

Integration verification commit:

```
b23359a923ef3ede19e16bb35a0c1be6018087d9
(short: b23359a on codex/week6-integration)
```

The following documentation-only freeze commit records that immutable parent
hash without changing the experiment or paper evidence.

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

## External submission actions

- Replace `ID=XXXXX` in `main.tex` with the real OpenReview paper ID.
- Complete the final human author-profile, citation, and anonymity review.
- Upload the anonymous PDF by the TwinWorld deadline.
- Camera-ready: set `\twinworldcamerareadytrue` and fill affiliations.

The template files were checked byte-for-byte against the official ECCV 2026
author kit at upstream commit
`da8c09c40239d5665757527e77388f4716a6564a`. P1-P3 evidence and run IDs were
verified in the integration audit.
