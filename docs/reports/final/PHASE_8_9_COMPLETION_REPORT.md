# Phase 8 and 9 Completion Report

Status date: 2026-07-24
Overall status: **DONE**

## Scope Completed

Phase 8 rewrote the academic manuscript around the actual agent/MCP research
protocol and the saved Phase 1, 3, 4, 5, 6, and 7 evidence. Phase 9 added
scientific, reproducibility, and visual QA and produced a final checked PDF.

The release manuscript is:

`papers/beyond-proximity/main.pdf`

Its submission-facing title is:

**Agent-Guided Hierarchical Semantic Search over 3D Scene Records**

The named authors are preserved. The paper is an eight-page, two-column
academic preprint, not a TwinWorld review-template submission.

## Phase 8: Paper Rewrite

### Method

The method now begins with the agent-MCP query protocol:

1. decompose the natural-language request;
2. inspect compact hierarchy summaries;
3. traverse only supported branches;
4. rank and validate candidate evidence;
5. return grounded evidence with a replayable trace.

Cursor Agent is described accurately as the interactive client and a direct
hierarchy-construction agent. The pinned local BGE model supplies reproducible
query metrics. Lexical matching is retained as a controlled baseline.

Section 3 also defines:

- deterministic hierarchy assembly;
- pose-only and pose-plus-semantic construction;
- direct Cursor Agent + MCP construction;
- top-down semantic traversal and fallback;
- trace schema and token accounting;
- validated target-anchor relation reasoning.

### Evaluation Evidence

The paper distinguishes all map and reference types:

| Track | Evidence type | Role |
|---|---|---|
| Five captured scenes | manual semantic records and verified expected views | same-input internal query benchmark |
| Replica | official oracle object IDs and boxes | lexical sanity ceiling |
| ScanNet | official oracle IDs/boxes with Nr3D/Sr3D+ queries | discriminative object-grounding protocol |
| ConceptGraphs | predicted object maps | native external execution |
| LangSplat | learned language field | native external execution |

Denominators are explicit: total, positive, verified negative, and box-eligible
queries are never mixed.

### Corrected Findings

- Lexical graph vs. flat: 75.43% fewer checked views and 67.99% fewer input
  tokens.
- Lexical hit@1 difference: inconclusive, CI `[-0.184, 0.008]`.
- Lexical hit@3 difference: significant decline, CI `[-0.184, -0.056]`.
- Semantic graph vs. flat: 79.90% fewer checked views and 32.50% fewer native
  input tokens.
- Semantic hit@1 difference: inconclusive, CI `[-0.096, 0.064]`.
- Semantic hit@3 and MRR: significant declines under hard pruning.
- ScanNet calibrated fallback exactly preserves flat lexical R@1/R@3/R@5/MRR
  on the frozen original and extended protocols while reducing objects and
  local context.
- Relation validation improves hit@1 from .550 to .675 on 40 relation queries,
  with five beneficial and zero harmful top-1 changes.

The paper no longer says that graph search generally matches flat quality.

### New Figures and Tables

Evidence-linked generation now produces:

- `fig_agent_mcp_protocol`: agent request, MCP traversal, evidence, and trace;
- `fig_agent_semantic_results`: four query variants with cost and quality;
- `fig_hierarchy_comparison`: query quality and structural agreement across
  four construction variants.

The manuscript contains seven organized tables covering denominators, metric
prerequisites, query variants, hierarchy construction, public protocols,
relation reasoning, and external execution evidence.

All five quantitative result-table bodies are generated from frozen JSON by
`scripts/export_academic_tables.py`. A SHA-256 source manifest is saved under
`papers/beyond-proximity/tables/table_data_manifest.json`; the paper checker
fails when a source changes without regenerating its table rows. The two
remaining tables define protocol denominators and metric prerequisites rather
than experimental results.

### Related Work and Naming

SayPlan and Search3D were added alongside ConceptGraphs, LangSplat, OpenScene,
OpenLex3D, ScanRefer, and context-pruning work.

The colliding former working name is absent from the academic source and PDF.
Repository-wide renaming remains outside this phase because it requires a team
decision and coordinated migration of URLs and compatibility identifiers.

## Phase 9: Scientific and Artifact QA

### Automated Claim Audit

`scripts/check_academic_paper.py` checks the manuscript against frozen JSON. It
rejects stale arithmetic, obsolete wording, unsupported quality claims,
missing required method/statistics language, absent figures, and forbidden
submission placeholders.

### Reproducibility Audit

`scripts/audit_phase89_paper.py` records:

- source and figure checks;
- model and seed provenance;
- one-command build availability;
- PDF metadata and page count;
- rendered page dimensions and nonblank ratios;
- manual page-review status.

Machine-readable and reader-facing results:

- `docs/reports/final/phase89_paper_artifact_qa.json`
- `docs/reports/final/PHASE_8_9_PAPER_ARTIFACT_QA.md`

### Visual Audit

The final PDF was rendered page by page. The audit found:

- eight nonblank letter-size pages;
- consistent page dimensions;
- no overlapping labels;
- no clipped tables;
- no displaced section;
- no stale workflow figure;
- no anonymous/Paper ID/TwinWorld placeholders;
- no use of the colliding former paper name;
- no unresolved reference marker.

The final page contains the public-data tables, conclusion, and a balanced
two-column bibliography without a spill page.

## Representative Trace Package

The query `Find the piano` has a 13-step local semantic trace with:

- query encoding;
- branch scores and retained nodes;
- leaf/view scores;
- final object ranking;
- native input-token accounting;
- per-step latency;
- selected view `v011` and object `piano`.

Path:

`outputs/agent_semantic/five_scene_four_variant_v1/traces/graph_semantic_embedding/ConferenceHall__qv2_001.json`

Direct Cursor Agent hierarchy construction is independently recorded at:

`docs/experiments/hierarchy_construction/cursor_agent_mcp_v1/agent_hierarchy_decisions.json`

These artifacts are intentionally separated: the first proves reproducible
semantic query execution; the second proves direct Cursor/MCP participation.

## Verification Results

```text
Agent semantic validation:
  150 queries
  4 methods
  600 per-query rows
  300 semantic traces
  0 errors
  0 warnings

Academic claim checker:
  PASS

Paper/artifact audit:
  PASS

Repository tests:
  167 passed in 14.47 s

Whitespace check:
  PASS (line-ending conversion warnings only)
```

Commands:

```powershell
papers\beyond-proximity\build_paper.cmd
python -B scripts\export_academic_tables.py
python -B scripts\check_academic_paper.py
python -B scripts\audit_phase89_paper.py
python -B scripts\validate_agent_semantic_benchmark.py `
  --output outputs\agent_semantic\five_scene_four_variant_v1
python -B -m pytest -q -p no:cacheprovider tests
git diff --check
```

## Honest Remaining Boundaries

These are research boundaries, not incomplete Phase 8/9 tasks:

- the 150-query benchmark uses a pinned embedding model, not an
  instruction-tuned LLM or Cursor query client;
- provider tokens and Cursor wall-clock construction time were not exposed and
  remain unavailable rather than zero;
- captured-scene semantic records remain manually authored;
- Replica and ScanNet retrieval is over oracle semantic maps;
- native ConceptGraphs and LangSplat runs use different map/resource
  protocols, so they are execution evidence rather than a fair leaderboard;
- LangSplat has one complete reduced-resource ScanNet run;
- no official BBQ execution artifact is included;
- a repository/package rename requires explicit team approval.

The next research phase should evaluate an instruction-tuned agent over
predicted public maps under one same-scene, same-query, same-resource protocol
and calibrate pruning to preserve top-3 quality.
