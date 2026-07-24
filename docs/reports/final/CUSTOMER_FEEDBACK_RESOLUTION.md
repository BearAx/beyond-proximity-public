# Customer Feedback Resolution: TwinWorld 2026

Status date: 2026-07-24.

Paper:

```text
papers/twinworld/main.tex
papers/twinworld/main.pdf
papers/twinworld/main_preprint.pdf
```

## Verdict

Every concrete item in `feedback.md` is addressed in the TwinWorld manuscript
and checked against saved evidence. This means the requested corrections are
complete; it does not guarantee acceptance or remove the scientific
limitations stated in Section 6.

## Major Feedback

| Feedback | Status | Resolution | Evidence |
|---|---|---|---|
| No actual semantic model | DONE | Qwen2.5-0.5B-Instruct executes all 150 queries. The run saves 150 traces, 300 model calls, 239,893 exact native tokens, latency, prompts, responses, branch decisions, and quality. It is explicitly not described as a stub or as Cursor. | Sections 3.4 and 5.1; Table 1; Fig. 4; `outputs/instruction_agent/five_scene_qwen25_05b_graph_v1/` |
| Hierarchy construction unexplained | DONE | Section 3.2 now defines the adaptive pose threshold, connected components, deterministic semantic merge, and direct Cursor-Agent/MCP construction. Five saved Cursor calls construct 18 zones without access to manual zones. Cursor differs from the manual reference by only +0.024 hit@1 and -0.024 hit@3 in the controlled retrieval test. Sections 3.5 and 5.2 separately evaluate raw RGB-D/pose construction with zero ViewJSON reads. | Sections 3.2, 3.5, 5.2, and 5.3; Table 2; Figs. 2, 5, and 6; `docs/experiments/hierarchy_construction/`; `outputs/raw_rgbd_hierarchy/five_scene_clip_v1/` |
| Public pilots cannot distinguish variants | DONE | Replica is labeled only as an oracle-map sanity ceiling. ScanNet now distinguishes relation-aware graph search from no-relation scoring (Acc@0.25 0.604 vs. 0.500) and reports the graph-vs-flat R@3 difference (0.812 vs. 0.833). Equality at R@1 is not described as universal quality preservation. | Section 5.5; Table 3; `outputs/public_datasets/phase6_scannet_calibrated_v3/` |
| Colliding paper name | DONE | The submission title is `Agent-Guided Hierarchical Semantic Search over 3D Scene Records`. The former working name is absent from the TwinWorld manuscript source, rendered PDF, build variables, and paper figures. | `papers/twinworld/`; `scripts/check_twinworld_numbers.py` |

## Minor Feedback

| Feedback | Status | Resolution | Evidence |
|---|---|---|---|
| SayPlan and Search3D missing | DONE | Both are cited and positioned against the contribution. | Section 2; `papers/twinworld/refs.bib` |
| hit@1 significance overstated | DONE | The manuscript reports graph-minus-flat hit@1 = -0.088 with 95% CI [-0.184, 0.008] as inconclusive. It separately reports hit@3 = -0.120 with CI [-0.184, -0.056] as a significant decline. | Section 5.4; `docs/reports/final/twinworld_bootstrap_ci.json` |
| Replica denominator inconsistent | DONE | The paper distinguishes 56 total queries, 48 positive retrieval queries, and 8 verified negatives in text and table labels. | Sections 4.2 and 5.5; Table 3 |
| 19.4 to 4.77 arithmetic | DONE | The primary 75.5% estimate is defined as the mean of per-query reductions. The paper also states that the ratio of displayed means is `1 - 4.77 / 19.40 = 75.4%`. | Section 5.4; `twinworld_bootstrap_ci.json` |
| Whitespace and unreadable labels | DONE | The workflow, tree, Qwen, raw-hierarchy, and construction-variant figures were redrawn at print scale. All 14 pages were rendered at 120 DPI and inspected. No figure/table is clipped, displaced above its subsection, or placed on an otherwise empty page. | `papers/twinworld/figures/`; `tmp/pdfs/twinworld-customer-final-v6/` |
| Relation reranking unexplained | DONE | The paper states the current controlled result: relation-aware ScanNet Acc@0.25 is 0.604 versus 0.500 without relation scoring. It also explains that the superseded reranker applied low-confidence tie breaks and frame-dependent predicates without geometry/margin gates; v3 abstains when those checks fail. | Section 5.5; Table 3 |

## Why Qwen and Cursor Both Appear

They have different measured roles.

- Qwen is the query-time language model. Its model revision is pinned, and its
  complete 150-query run has exact tokenizer, call, latency, and quality
  accounting.
- Cursor Agent is the original MCP orchestration surface for hierarchy
  construction. It calls `build_spatial_clusters` once per scene, then
  semantically partitions and labels the geometric candidates.
- Cursor's UI did not expose provider-token or stable construction-time
  telemetry. Those values remain unavailable and are not replaced with zeros
  or Qwen counts.
- The raw CLIP track is a stricter construction experiment: it reads RGB,
  depth, and poses, but zero manual ViewJSON or manual-zone files.

The paper never attributes Qwen query metrics to Cursor and never presents
Cursor as a frozen reproducible model.

## Verification

```text
TwinWorld number and wording gate: PASS
Instruction-agent validator: PASS
Raw RGB-D hierarchy validator: PASS
Hierarchy construction evidence: 5 direct Cursor MCP calls, 150-query comparison
Backend and experiment tests: 172 passed
Paper build: PASS
Rendered PDF: 14 pages total; content through page 13; references continue to page 14
Final visual audit: 14 pages at 120 DPI in `tmp/pdfs/twinworld-customer-final-v6/`
Temporary review-mode validation: anonymous, blue line numbers, numeric ID, 14 pages
Official template: exact ECCV 2026 author-kit files at da8c09c40239d5665757527e77388f4716a6564a
```

## External Actions Before Upload

These are submission-owner actions, not unresolved customer-feedback items:

1. Confirm the final author list, order, affiliations, emails, and OpenReview
   profiles privately.
2. Register the TwinWorld submission and obtain the numeric paper ID.
3. Build the anonymous review PDF with:

   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\build_twinworld_review.ps1 -PaperId <assigned-number>
   ```

4. Verify names are absent, the assigned ID and blue line numbers are present,
   and the PDF remains within the 14-content-page limit.
5. Resolve repository publicity/anonymity policy with the repository owners
   before upload.
