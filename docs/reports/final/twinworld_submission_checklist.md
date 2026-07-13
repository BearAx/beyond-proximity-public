# TwinWorld Submission Checklist (Person 4)

Deadline (workshop page): **2026-07-31**. Venue: TwinWorld @ ECCV 2026.

## Format

- [x] LNCS / ECCV-style template (`papers/twinworld/llncs.cls`, `eccv.sty`)
- [x] Anonymous review mode (`[review]` + Anonymous Authors)
- [ ] Replace `ID=XXXXX` with OpenReview paper ID
- [ ] Confirm against **official ECCV 2026 Author Kit** (template may differ from 2024 kit)
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

## Still blocked without others

| Check with | Question |
|---|---|
| OpenReview | Paper ID for `ID=XXXXX` |
| Venue | Official ECCV 2026 author kit confirmation |
| P1 | Final Replica/ScanNet availability statuses frozen? |
| P2 | Final run IDs for replica_pilot_v1 / scannet_pilot_v1? |
| P3 | Related-work paragraph OK to paste as-is? |
| All | Prioritize TwinWorld-by-deadline vs stronger later venue? |
