# TwinWorld 2026 Article Compliance Audit

Status date: 2026-07-21
Paper: `papers/twinworld/main.tex`
Target: TwinWorld at ECCV 2026

## Verdict

The paper is a strong topical fit for TwinWorld: it studies queryable semantic
digital twins, hierarchical scene representations, 3D object grounding, and
evaluation on Replica and ScanNet. The local review manuscript now follows the
ECCV 2026 review format and is source-level anonymous.

No submission can be guaranteed acceptance. The expanded ID-free manuscript
has 13 content pages within 14 total pages; the conclusion is followed by
references on page 13. The Method workflow and hierarchy are placed on pages 3
and 4 without a float-only page. The tracked PDF remains ID-free until
OpenReview assigns the real numeric ID; review line numbering and header-ID
validation must be repeated on that final upload build.

Scientifically, the principal weakness is not formatting: SemanticSplat's
public-dataset experiments retrieve over oracle semantic maps and do not yet
evaluate semantic perception or reproduce BBQ under the same protocol. The
paper is therefore best submitted under ECCV's **Concept & Feasibility**
contribution type, with the present limitations retained.

## Requirement Matrix

| Requirement | Status | Evidence | Remaining action |
|---|---|---|---|
| TwinWorld topic fit | DONE | Semantic digital twins, scene hierarchy, 3D grounding, Replica/ScanNet | None |
| Official ECCV 2026 template | DONE | `papers/twinworld/eccv.sty`, `llncs.cls`, `splncs04.bst` match official kit commit `da8c09c...` | Recheck only if the kit changes before submission |
| Anonymous double-blind review PDF | DONE | `[review]`; anonymous author/institute; no author names in review source or PDF metadata | Run a final metadata inspection on the uploaded PDF |
| Review line numbering | DONE_VALIDATED | A temporary numeric-ID review build rendered blue marginal line numbers on every page | Keep for initial submission; remove for camera-ready |
| Paper ID on review pages | READY_PENDING_ASSIGNMENT | No placeholder in `main.tex`; `build_twinworld_review.ps1` accepts only an assigned numeric ID | Register the submission, then run the review builder with that ID |
| At most 14 content pages | DONE_LOCAL | Latest ID-free build has 13 content pages within 14 total pages; references begin after the conclusion on page 13 | Recheck after the final real-ID build |
| References only beyond content limit | DONE_LOCAL | No appendix or supplementary material appended to the PDF | Keep the PDF self-contained |
| No appendix | DONE | No `\appendix` or appendix section | None |
| No acknowledgements in review | DONE | No acknowledgement section in rendered paper | Add acknowledgements only camera-ready if desired |
| No external links that expand the paper | DONE | No URL, repository link, or external-results dependency in manuscript | Do not add a public project link during review |
| Claims supported by saved evidence | DONE_WITH_LIMITATIONS | Automated JSON number gate; explicit oracle/stub/baseline caveats | Preserve limitations and no-superiority wording |
| Contribution type | READY_TEAM_SELECTION | Evidence and claim scope fit **Concept & Feasibility** better than a full Algorithms paper | Select this category in OpenReview unless the call exposes a workshop-specific equivalent |
| Author list and order | PENDING_TEAM_INPUT | Review PDF must remain anonymous | Agree exact names, order, affiliations, emails, and OpenReview identities before registration |
| OpenReview profiles and conflicts | PENDING_EXTERNAL | Submission-portal requirement | Every author must complete profile/conflicts before deadline |
| Publicity/media embargo | ACTION_REQUIRED | Public repository/branches currently identify the work as an intended TwinWorld/ECCV submission | Make the repository private or perform an owner-approved publicity/history remediation before submission |
| Camera-ready form | NOT_YET_APPLICABLE | Review source is intentionally anonymous | Use `\usepackage{eccv}` and restore private author metadata after acceptance |

## Corrections Made

- Removed `Person 1+2`, `Person 2`, and other team-process language from the
  paper and paper-package headings.
- Removed ``Capture and semantic index'' from Method and moved input/index
  construction to Sec. 4, Datasets and Evaluation.
- Expanded Method into five implementation-backed components: hierarchy and
  candidates, captured-scene zone pruning, object/intent scoring,
  target-anchor geometry, and explicit fallback/variants/cost accounting.
- Removed dormant real author names from the anonymous review source.
- Corrected the five-scene count from 96 to 97 captured views.
- Distinguished serialized-context tokens from provider/API token billing.
- Renamed the heuristic from "calibrated fallback" to "thresholded fallback."
- Added the implemented branch threshold, lexical score, relation adjustment,
  fallback threshold, metric definitions, and token-count procedures.
- Added a real-artifact Method workflow built from captured RGB-D, ViewJSON,
  the checked-in hierarchy, and frozen query qv2_010; no generated imagery.
- Added a reproducible construction audit: 0 provider calls/tokens, 66,937
  source-record and 179,817 tree-record character/4 token-equivalents, and
  1.822 s summed per-scene median local rebuild time. Manual annotation remains
  explicitly N/A because it was not token-metered.
- Removed the unsupported claim that a supplementary artifact is required to
  interpret the paper.
- Updated camera-ready instructions to match the official ECCV sample:
  `\usepackage{eccv}` with author metadata restored privately.
- Replaced the stale placeholder-ID workflow with an ID-free pre-submission
  build and a numeric-only review build.
- Added native ConceptGraphs runs on all eight ScanNet scenes / 48 queries and
  all eight Replica scenes / 56 queries, plus a one-scene / six-query
  reduced-resource end-to-end LangSplat ScanNet run.
- Rebuilt and visually inspected the expanded ID-free PDF: 14 pages total, 13
  content pages, references start after the conclusion on page 13, and there
  are no float-only pages, team-role labels, clipping, or overlapping
  figures/tables.

## Why ``Anonymous'' Appears Repeatedly

This is intentional. ECCV uses double-blind review, so the review PDF must not
identify its authors or institutions. `Anonymous Authors` appears below the
title and `Anonymous` appears in running page headers because that is how the
review template suppresses identity. It does not mean the team names are
unknown.

Real author information belongs in two places:

1. The private OpenReview submission form: exact author names/order,
   affiliations, emails, profiles, and conflicts.
2. The camera-ready source after acceptance: replace the anonymous author and
   institution fields and compile without review mode/line numbering.

Do not add real names, acknowledgements, personal repositories, or identifying
affiliations to the review PDF. The team should provide the final author list
only when preparing the private portal record and camera-ready metadata.

## Line-Number Question

The two supplied answers are relevant and essentially correct. TwinWorld says
to use the official ECCV guidelines/template. The ECCV review template requires
all lines to be numbered for initial submission; `eccv.sty` renders those blue
marginal numbers in review mode. A camera-ready paper removes them. Therefore,
the blue numbers are an ECCV review-format feature inherited by TwinWorld, not
a TwinWorld-specific decoration and not an error in the review PDF.

## Scientific Readiness

The current defensible claim is that hierarchy reduces checked context on the
same semantic map, with an internal hit-at-k tradeoff and matched flat-lexical
quality on the current oracle-map public pilots. ConceptGraphs now supplies
real eight-scene predicted-map references on ScanNet and sampled-frame Replica,
and LangSplat supplies a real reduced-resource end-to-end one-scene reference. Their protocols differ from
the oracle-map SemanticSplat track, so the paper still must not claim external
baseline superiority.

Highest-value additions before the deadline, if experiment time permits:

1. Add predicted semantic segmentation/object proposals so mAcc, mIoU, fmIoU,
   and non-oracle 3D grounding can be reported.
2. Expand the 48-query ScanNet pilot and report confidence intervals or
   per-query-family variance.
3. Add an explicit 3DGS reconstruction/integration experiment so the title's
   3DGS framing is demonstrated end to end rather than used mainly as system
   positioning.

These additions would strengthen acceptance odds, but they are not template
requirements. For the current evidence level, submit as Concept & Feasibility
and do not rewrite the paper to imply a completed perception benchmark.

## Submission Procedure

1. Agree the complete author list and order. Collect each author's affiliation,
   email, OpenReview profile, and conflict information.
2. Resolve the ECCV publicity risk before submission: make the repository
   private or perform an owner-approved remediation of public material that
   explicitly identifies the work as an ECCV/TwinWorld submission.
3. Open the TwinWorld 2026 OpenReview submission page from the workshop site,
   create the submission, and enter the title, abstract, keywords, anonymous
   PDF metadata, and all real authors in the private form.
4. Select **Concept & Feasibility** as the ECCV contribution type unless the
   TwinWorld form replaces it with a workshop-specific category.
5. After OpenReview assigns the numeric paper ID, run:

   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\build_twinworld_review.ps1 -PaperId <assigned-number>
   ```

6. Inspect `papers/twinworld/main.pdf`: real names must be absent, the real
   paper ID and blue line numbers must be present, and the manuscript must
   remain within the 14-content-page limit.
7. Upload and finalize by **2026-07-31**. Verify author profiles and conflicts
   before the portal deadline rather than waiting for PDF upload day.
8. If accepted, restore author metadata, compile camera-ready without review
   mode, complete registration, and arrange the required in-person
   presentation. Current published dates are notification **2026-08-09**,
   camera-ready **2026-08-15**, and workshop **2026-09-08**.

## Official Sources

- TwinWorld workshop and submission instructions: <https://twin-world.github.io/>
- ECCV 2026 submission policies: <https://eccv.ecva.net/Conferences/2026/SubmissionPolicies>
- ECCV 2026 contribution types: <https://eccv.ecva.net/Conferences/2026/AuthorContributionTypes>
- ECCV 2026 suggested practices: <https://eccv.ecva.net/Conferences/2026/AuthorPractices>
- ECCV 2026 FAQ: <https://eccv.ecva.net/Conferences/2026/FAQs>
- Official ECCV author kit: <https://github.com/paolo-favaro/paper-template>
