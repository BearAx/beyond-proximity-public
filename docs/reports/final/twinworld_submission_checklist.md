# TwinWorld Submission Checklist (Person 4)

Deadline (workshop page): **2026-07-31**. Venue: TwinWorld @ ECCV 2026.

## Format

- [x] LNCS / ECCV-style template (`papers/twinworld/llncs.cls`, `eccv.sty`)
- [x] Anonymous review mode (`[review]` + Anonymous Authors)
- [ ] Replace `ID=XXXXX` with OpenReview paper ID
- [x] Confirmed against the **official ECCV 2026 Author Kit**: `eccv.sty`,
  `llncs.cls`, and `splncs04.bst` are exact matches to upstream commit
  `da8c09c40239d5665757527e77388f4716a6564a`
- [x] ≤14 pages content excluding references (current draft ~9–11pp; recheck after final figures)
- [x] No appendix in main PDF (reproducibility is a short section + external md)

## Claims

- [x] TwinWorld-framed digital-twin story in abstract/intro
- [x] BBQ paragraph + no superiority claim
- [x] Public-dataset pilot tables with oracle caveats
- [x] Limitations section (includes internal hit@k tradeoff)
- [x] Numbers cross-checked against frozen JSON (`scripts/check_twinworld_numbers.py`)
- [x] No stale absolute “1,046 items” without a source path
- [x] Superseded PERSON1 roundings (71.4% / 0.792) removed from TwinWorld PDF

## Artifacts

- [x] `papers/twinworld/main.tex` with P1–P3 numbers (JSON-synced)
- [x] Figures folder (internal + system/tree/gallery/qualitative + public pilots)
- [x] `twinworld_claim_audit.md`
- [x] `twinworld_figure_checklist.md`
- [x] `twinworld_reproducibility.md` + commit hash freeze
- [x] Anonymized `main.pdf` builds (local MiKTeX)
- [x] Camera-ready author toggle (`\twinworldcamerareadytrue`; review mode leaves Anonymous)
- [x] Number gate report: `twinworld_number_check.md`

## External submission actions

| Action | Status |
|---|---|
| Replace `ID=XXXXX` with the assigned OpenReview paper ID | Pending portal assignment |
| Complete and verify every author's OpenReview profile/conflicts | Team action |
| Perform final human authorship, citation, and anonymity review | Team action |
| Upload the anonymous PDF by 2026-07-31 | Team action |
| Register an author and arrange in-person presentation if accepted | Post-acceptance action |

P1-P3 artifacts and run IDs were verified during the Week 6 integration audit.
These remaining items require the submission portal or author decisions; they
are not code or evidence blockers.
