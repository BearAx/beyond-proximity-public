# TwinWorld 2026 Submission Checklist

Deadline (workshop page): **2026-07-31**. Venue: TwinWorld @ ECCV 2026.

## Format

- [x] LNCS / ECCV-style template (`papers/twinworld/llncs.cls`, `eccv.sty`)
- [x] Anonymous review mode (`[review]` + Anonymous Authors)
- [x] Review line numbering enabled (blue marginal numbers are required)
- [x] Review source contains no dormant author names or team-role labels
- [x] No placeholder paper ID in tracked source
- [ ] Register in OpenReview and run the numeric-only review builder with the assigned ID
- [x] Confirmed against the **official ECCV 2026 Author Kit**: `eccv.sty`,
  `llncs.cls`, and `splncs04.bst` are exact matches to upstream commit
  `da8c09c40239d5665757527e77388f4716a6564a`
- [x] <=14 pages content excluding references (latest ID-free build: 14 pages
  total, content through page 13, and references continuing to page 14)
- [x] No appendix in main PDF (reproducibility is a short section + external md)
- [x] No acknowledgements in the review PDF
- [x] No external links in the paper

## Claims

- [x] TwinWorld-framed digital-twin story in abstract/intro
- [x] BBQ paragraph + no superiority claim
- [x] Public-dataset pilot tables with oracle caveats
- [x] Limitations section (includes internal hit@k tradeoff)
- [x] Complete 150-query instruction-agent execution with prompts, calls,
  exact native tokens, latency, traces, and quality
- [x] Original Cursor-Agent/MCP construction path: five direct calls, frozen
  decisions, no manual-zone access, and a 150-query comparison
- [x] Raw RGB-D/pose-to-hierarchy construction with zero manual ViewJSON reads,
  followed by a frozen comparison with manual zones
- [x] Paired bootstrap wording: hit@1 is inconclusive; hit@3 declines
  significantly
- [x] View-reduction arithmetic defines 75.5% as a mean of per-query reductions
  and separately reports 75.4% from the displayed means
- [x] Calibrated v3 ScanNet/Replica results replace the superseded v1 values
- [x] Numbers cross-checked against frozen JSON (`scripts/check_twinworld_numbers.py`)
- [x] No stale absolute "1,046 items" without a source path
- [x] Superseded PERSON1 roundings (71.4% / 0.792) removed from TwinWorld PDF

## Artifacts

- [x] `papers/twinworld/main.tex` with evidence-backed, JSON-synced numbers
- [x] Figures folder (internal + system/tree/gallery/qualitative + public pilots)
- [x] Real-data Method workflow + controlled evaluation protocol figures
- [x] Graph-construction token/runtime audit (`graph_construction_cost.json`)
- [x] Instruction-agent ledger and 150 validated traces
  (`outputs/instruction_agent/five_scene_qwen25_05b_graph_v1/`)
- [x] Cursor-Agent/MCP decisions and four-variant construction evaluation
  (`docs/experiments/hierarchy_construction/`)
- [x] Raw RGB-D hierarchy, three-way retrieval comparison, and validation
  (`outputs/raw_rgbd_hierarchy/five_scene_clip_v1/`)
- [x] Static GitHub Pages source and reproducible site builder
- [x] `twinworld_claim_audit.md`
- [x] `twinworld_figure_checklist.md`
- [x] `twinworld_reproducibility.md` + commit hash freeze
- [x] Anonymized `main.pdf` builds (local MiKTeX)
- [x] Review source is source-level anonymous; camera-ready metadata stays private
- [x] Number gate report: `twinworld_number_check.md`
- [x] Every page rendered at 120 DPI; all figure labels and table placements
  inspected (`tmp/pdfs/twinworld-customer-final-v6/`)

## External submission actions

| Action | Status |
|---|---|
| Agree exact author names, order, affiliations, emails, and OpenReview identities | Team action |
| Select ECCV contribution type: **Concept & Feasibility** is recommended | Team action in portal |
| Register submission and build with the assigned numeric OpenReview ID | Pending portal assignment |
| Complete and verify every author's OpenReview profile/conflicts | Team action |
| Perform final human authorship, citation, and anonymity review | Team action |
| Upload the anonymous PDF by 2026-07-31 | Team action |
| Register an author and arrange in-person presentation if accepted | Post-acceptance action |
| Resolve public repository/branch material that explicitly advertises an intended ECCV 2026 submission | **Urgent team action before submission** |

Dataset, evaluation, baseline, and paper artifacts were verified during the
Week 6 integration audit. The repository-publicity item is a policy risk, not a
formatting detail; it requires a repository visibility/history decision by the
owners.

`Anonymous Authors` below the title and `Anonymous` in the running headers are
intentional double-blind review formatting. Real identities belong in the
private OpenReview form and, after acceptance, the camera-ready source. Do not
put names or affiliations in the review PDF.

## Portal sequence

1. Start from <https://twin-world.github.io/> and follow its submission link to
   the TwinWorld OpenReview venue.
2. Register the title/abstract and all real authors in the private portal form.
3. Complete every author's profile and conflicts.
4. Build with the assigned numeric ID:
   `scripts\build_twinworld_review.ps1 -PaperId <assigned-number>`.
5. Verify anonymity, ID, blue line numbers, and the <=14-content-page limit.
6. Upload and finalize by **2026-07-31**.
