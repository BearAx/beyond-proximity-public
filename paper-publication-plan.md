# Paper Publication Plan — SemanticSplat
### Hierarchical VLM Scene Understanding over 3D Gaussian Splatting

**Planning window:** June 5, 2026 → July 14, 2026 (≈ 6 working weeks)
**Owner:** Project team
**Canonical references:**
- Design: `docs/superpowers/specs/2026-04-05-semantic-3dgs-navigator-design.md`
- Paper outline: `docs/superpowers/specs/2026-04-05-paper-design.md`
- Implementation: `backend/` (FastAPI + MCP) and `frontend/` (Spark.js viewer)

---

## 0. Goal

Produce a **submission-ready research paper** with:
1. A **reproducible, scriptable pipeline** (no human/Cursor-in-the-loop in the eval path).
2. **Quantitative results** vs. published baselines on standard datasets.
3. The **core ablation** (Geometry vs. Pure-LLM vs. Hybrid) proving each component contributes.
4. A **public repository** (clean, documented, reproducible) and a **project website** with very creative and highly professional interactive demos.
5. An **arXiv preprint** + submission to a target venue.

**Deliverables by July 14:** paper PDF (camera-ready-quality draft), public GitHub repo, project website, arXiv submission, and a packaged demo.

---

## 1. Current State Assessment (Honest Baseline)

### What already exists (prototype)
| Area | Status | Files |
|---|---|---|
| 3DGS viewer + manual view capture | Built | `frontend/src/components/Navigator/*` (Spark.js, FPS controls, depth capture) |
| Nerfstudio I/O, view store | Built | `backend/io/*` |
| Spatial proximity graph | Built | `backend/geometry/spatial_graph.py` |
| Depth → 3D bbox unprojection | Built + tested | `backend/geometry/unprojector.py`, `tests/backend/test_unprojector.py` |
| Tree nodes + storage | Built | `backend/tree/*` |
| Query pipeline + logging | Built | `backend/query/*` |
| MCP tools (scene/view/tree/query) | Built | `backend/mcp/tools/*` |
| Frontend tree visualizer + query flow | Built | `frontend/src/components/TreeVisualizer/*`, `QueryFlow/*` |

### What is missing for a publishable paper (the real work)
1. **Automatic view selection:** design claims **NoField** (automatic, coverage-optimal); implementation uses **manual R-press capture**. Must implement an automatic selection (NoField or a defensible coverage-greedy substitute) — it is a stated novelty. (Mahmoud is already working on it, will finish by mid of June)
3. **No quantitative experiments**, no benchmark query sets, no baselines run.
4. **No evaluation harness** for the metrics defined in the design (zone accuracy, retrieval IoU, tree coherence, scalability, context efficiency).

> **Implication:** Weeks 1–2 are dominated by turning the demo into a *scriptable experimental system*. This is the critical path; everything else depends on it.

---

## 2. Scope Decisions (to fit 6 weeks)

To stay realistic, we **fix scope now** and treat extras as stretch goals.

| Dimension | Committed scope | Stretch (if time) |
|---|---|---|
| Datasets | **Replica** (clean, GT rooms) + **ScanNet** (real, GT labels) | **HM3D** (scalability), 1 custom large scan |
| Baselines | **LangSplat** + **ConceptGraphs** (+ **LERF** if cheap) | Semantic Gaussians, BBQ |
| Core results | **Ablation A/B/C**, retrieval accuracy, query-type breakdown | Full scalability curve 15→2000 views |
| Query benchmark | **Auto-generated + human-verified** (~150–300 queries) | Crowd eval, inter-annotator study |
| Output types | 3D bbox + camera pose | Text-answer / count VQA |

**Target venue (decide Week 1):** arXiv preprint + submission to next open CV/ML deadline (e.g., **WACV 2027** round / **CVPR 2027** / a strong workshop). Pick based on deadline calendar in Day 1–2.

---

## 3. Timeline Overview

| Week | Dates | Theme | Primary exit criterion |
|---|---|---|---|
| **1** | Jun 5 – Jun 11 | Scope, scriptable pipeline foundation, datasets, metrics | Programmatic VLM pipeline runs end-to-end on 1 scene |
| **2** | Jun 12 – Jun 18 | First experiments + automatic view selection | First quantitative numbers on Replica; NoField/auto-select working |
| **3** | Jun 19 – Jun 25 | Baselines + benchmark + scale up | Baselines reproduced; full query benchmark; results on 2 datasets |
| **4** | Jun 26 – Jul 2 | Ablations, final experiments, freeze results | All core + ablation results frozen; figures generated |
| **5** | Jul 3 – Jul 9 | Paper writing, repo hardening | Full paper draft v1 + clean public repo |
| **6** | Jul 10 – Jul 14 | Polish, website, arXiv, submit | Final PDF + website live + arXiv posted |

---

## 4. Week-by-Week Plan

### Week 1 — Foundation & Reproducibility (Jun 5 – Jun 11)
**Theme:** Convert the demo into a scriptable research system; lock the experimental design.

**Tasks**
- Finalize **research questions, claims, and target venue/deadline**; write a 1-page claims sheet.
- Define **experimental design**: datasets, metrics, baselines, ablation matrix (lift directly from design §10, prune to committed scope).
- Define **evaluation metrics + protocols**: example zone boundary accuracy, retrieval accuracy (3D IoU > 0.5), tree coherence (LLM-judge rubric), context efficiency, scalability.
- Stand up **dataset ingestion**: Replica + ScanNet → posed RGB(-D); decide 3DGS-render vs. dataset-native-frame path; reconstruct 1–2 pilot scenes.
- Reproduce the **existing pipeline on one scene fully unattended** (capture → view JSON → tree → query) as the smoke test.

**Deliverables:** claims sheet; experiment-design doc; working headless pipeline on 1 scene; dataset loaders; literature/related-work notes.
**Exit criterion:** one large scene runs end-to-end with zero human-in-the-loop and emits a tree + query answer.

---

### Week 2 — First Experiments & Automatic View Selection (Jun 12 – Jun 18)
**Theme:** Get the first real numbers; remove the manual-capture dependency.

**Tasks**
- Implement **automatic view selection** (NoField integration or coverage-greedy substitute); validate coverage on pilot scenes.
- Run **first experiment batch** on a **Replica subset** (5–10 scenes): build trees, run a small query set, log retrieval accuracy + tree coherence.
- Build the **evaluation harness** (metrics computed automatically from logged outputs + ground truth).
- **Fallback review #1:** inspect failure cases (VLM hallucination, bad zones, depth/bbox errors). Decide mitigations (multi-view confirmation, confidence gating, deterministic LLM settings).
- **Construct the query benchmark v1**: auto-generate queries from tree/GT + human verification; target ~100 queries across query types.
- Plan next dev stage (baselines + scale) based on observed bottlenecks.

**Deliverables:** auto view-selection module; first Replica metrics table; eval harness; query benchmark v1; failure-mode log.
**Exit criterion:** reproducible quantitative result on ≥5 Replica scenes with the automatic pipeline.

---

### Week 3 — Baselines, Benchmark & Scale-Up (Jun 19 – Jun 25)
**Theme:** Make results comparable and broader.

**Tasks**
- **Reproduce baselines:** LangSplat + ConceptGraphs (LERF if time) on the same scenes/queries; align evaluation protocol for fairness.
- **Enhance metrics & benchmark:** finalize query benchmark to ~150–300 verified queries; add query-complexity strata (simple/compound/relational/multi-hop/functional).
- **Scale to ScanNet** (real-world scenes); run our pipeline + baselines.
- **Second experiment batch:** full retrieval + zone accuracy on Replica **and** ScanNet; begin scalability probe (vary K).
- Refine prompts / tree construction from Week-2 failures; re-run affected scenes.
- Plan final ablation runs.

**Deliverables:** baseline results reproduced; finalized benchmark; cross-dataset results table; scalability pilot.
**Exit criterion:** head-to-head numbers (ours vs. ≥2 baselines) on 2 datasets.

---

### Week 4 — Ablations, Final Experiments & Result Freeze (Jun 26 – Jul 2)
**Theme:** Prove the contribution; lock numbers.

**Tasks**
- Run the **core ablation A/B/C** (Pure-Geometry vs. Pure-LLM vs. Hybrid) — the central claim.
- Run **secondary ablations:** tree-depth vs. accuracy; VLM description quality (rendered vs. raw); query-complexity breakdown.
- Complete **scalability curve** (stretch: toward HM3D / large scene).
- **Final experiment pass**; fix any reproducibility gaps; set random seeds / temperature=0; log everything.
- **Freeze results**; generate all **figures and tables** (qualitative tree visualizations, retrieved 3D bboxes, comparison charts).
- Start **paper writing**: methods + experiments sections from frozen results.

**Deliverables:** complete results (main + ablations); all final figures/tables; methods + experiments draft.
**Exit criterion:** **results frozen** — no further experiment changes barring fatal bugs.

---

### Week 5 — Paper Writing & Repository Hardening (Jul 3 – Jul 9)
**Theme:** Turn results into a paper; make the code public-quality.

**Tasks**
- Write **full paper draft v1**: abstract, intro, related work, method, experiments, ablations, limitations, conclusion (use `paper-design.md` as skeleton).
- Internal **review pass**; tighten novelty statement and claims to match evidence; add limitations honestly.
- **Repository hardening:** clean structure, README, install/repro instructions, config files, scripts to reproduce each table/figure, license.
- Prepare **reproducibility package** (configs, seeds, prompts, eval scripts, sample data).
- Begin **website scaffold** (hero, abstract, method figure, video/demo, results, BibTeX).

**Deliverables:** paper draft v1; public-ready repo; reproducibility scripts; website scaffold.
**Exit criterion:** a complete, self-consistent paper draft and a repo a stranger could run.

---

### Week 6 — Polish, Website, arXiv & Submit (Jul 10 – Jul 14)
**Theme:** Ship.

**Tasks**
- Incorporate review feedback; **finalize paper** (proofread, figures, formatting to venue template).
- **Build the project website** (epic): interactive tree-viz demo, query examples, qualitative galleries, paper/PDF/arXiv/code links.
- **Finalize public repo:** tag release, archive (Zenodo DOI optional), demo notebook.
- **Post arXiv preprint**; prepare and submit to the chosen venue (or schedule for its deadline).
- Prepare **launch assets** (social thread, short demo video via the Spark.js viewer).

**Deliverables:** final paper PDF; live website; tagged public repo; arXiv ID; submission package.
**Exit criterion:** arXiv live + website live + repo public + submission filed/scheduled.

---

## 5. Milestones & Gates

| Milestone | Target date | Gate |
|---|---|---|
| M1 — Headless pipeline on 1 scene | Jun 11 | No human-in-loop |
| M2 — First quantitative result (Replica) | Jun 18 | Auto view-selection + eval harness work |
| M3 — Baselines + cross-dataset results | Jun 25 | Fair head-to-head numbers |
| M4 — Results frozen + figures | Jul 2 | All ablations done |
| M5 — Paper draft v1 + repo | Jul 9 | Reproducible by a stranger |
| M6 — Submit + website + arXiv | Jul 14 | Public + filed |

---

## 6. Risks & Contingencies

| Risk | Likelihood | Impact | Mitigation / Fallback |
|---|---|---|---|
| Headless VLM pipeline slips | Med | High (critical path) | Start Day 1; keep model adapter simple; fall back to one hosted VLM |
| Baseline reproduction is slow | High | High | Cap at 2 baselines; cite published numbers where protocols match; clearly scope comparison |
| 3DGS reconstruction per scene too costly | Med | Med | Use dataset-native posed RGB-D frames instead of rendering; reserve 3DGS for a qualitative subset |
| Query benchmark labor-heavy | Med | Med | Auto-generate + spot-verify; reduce to 150 queries |
| Real-image / hard-scene accuracy weak | Med | Med | Report honestly as limitation; emphasize Replica clean-render strength |
| VLM cost/rate limits | Med | Med | Batch + cache all VLM outputs; temperature=0 for determinism |
| Venue deadline mismatch | Low | Low | Default to arXiv now; submit to next open deadline |

**Global fallback:** if experiments compress, prioritize **arXiv preprint + strong workshop** with the **core ablation + one solid dataset**, and frame full benchmark as ongoing.

---

## 7. Deliverables Checklist

- [ ] Claims sheet + experimental-design doc
- [ ] Automatic view-selection module
- [ ] Evaluation harness (all committed metrics)
- [ ] Query benchmark (versioned, verified)
- [ ] Main results + ablations (frozen)
- [ ] All figures and tables
- [ ] Paper PDF (venue-formatted)
- [ ] Public GitHub repo + README + repro scripts
- [ ] Project website with interactive demo
- [ ] arXiv preprint posted
- [ ] Submission filed / scheduled

---

## 8. Notes on Further Development & Design (Paper-Relevant)

These emerged from reviewing the design + implementation and should be reflected in the paper's *method* and *future work*:

1. **Reproducible intelligence path** — the headless VLM pipeline is not just plumbing; it is required for scientific validity and should be described as the experimental system. (important to check this)
2. **Automatic view selection** — NoField (or substitute) must be real to support the novelty claim of coverage-optimal, scene-agnostic input.
3. **Determinism & hallucination control** — temperature=0, multi-view confirmation, confidence gating; report consistency (tree edit distance across runs) as in design §14.1.
4. **Depth-reliability handling** — glass/thin-surface depth noise (design §14.4); report 3D-bbox confidence and fallbacks.
5. **Incremental re-indexing** — position as future work (design §14.6): change-localized updates rather than full rebuilds.
6. **Downstream applications** — change detection, accessibility descriptions, VQA-data generation, embodied navigation (design §12) make strong "impact"/future-work content.

---

*End of plan.*
