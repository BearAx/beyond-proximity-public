# Article Readiness Checklist — Person 4

Status date: 2026-07-05. Branch: `week4/integration-article-sprint`.

Use this before opening a PR or submitting a PDF.

## Evidence frozen

- [x] Five-scene run ID documented: `five_scene_graph_vs_flat_v2`
- [x] Table 1 numbers match `metrics_summary.json`
- [x] Notebook Part B reads same JSON path
- [x] Tests pass: `test_graph_vs_flat.py`, `test_affordance.py`

## Text honesty

- [x] No 100% room accuracy claim
- [x] No 34% IoU claim
- [x] No "50 challenging find queries" claim
- [x] No external baseline superiority
- [x] Stub lexical mode stated in abstract and limitations
- [x] Manual labels framed as reference labels, not independent GT

## Documentation sync

- [x] `claim_audit.md` reflects merge state
- [x] `reproducibility_windows.md` includes `run_graph_vs_flat.py`
- [x] `paper_outline.md` no longer says "TBD Person 1"
- [x] Stale presentation files bannered

## Related work

- [x] Prose in `main.tex` §2 from P3 matrix
- [x] Full matrix remains in `docs/baselines/related_work_article_matrix.md`
- [x] Citations in `refs.bib` (verify metadata before camera-ready)

## Build & ship

- [ ] Install LaTeX and produce `main.pdf` (`papers/beyond-proximity/BUILD.md`)
- [ ] Team proofread (Person 1 numbers, Person 2 GT wording, Person 3 citations)
- [ ] Decide venue (arXiv tech report vs conference)
- [ ] Open PR: `week4/integration-article-sprint` → `main`

## Open questions for team

1. Venue and deadline?
2. English-only article OK?
3. Who opens PR to Leo `main`?
4. OK to call manual ViewJSON "reference labels" in camera-ready?
