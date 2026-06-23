# Baseline Risks

Week 1 owner: Literature / Baselines / Repo Notes Lead  
Purpose: list risks that could make baseline comparisons unfair, slow, or unreproducible.

## Highest-Risk Issues

| Risk | Severity | Why It Matters | Mitigation |
|---|---:|---|---|
| Baseline output mismatch | High | LangSplat outputs language-field relevancy, ConceptGraphs outputs object graphs, SemanticSplat outputs a tree/query answer. Direct metric comparison will be ambiguous. | Define shared `query_result.json` schema before running baselines. Track missing fields explicitly. |
| Dataset format mismatch | High | Week 1 target format is `rgb/depth/poses/intrinsics`, while current backend uses `images/depths/transforms.json`; baselines may expect COLMAP/Nerfstudio/Replica-specific layouts. | Create one canonical scene manifest and per-method adapters. |
| Human-in-the-loop prototype path | High | The UI query flow remains simulated and does not provide reproducible model evaluation. | Use canonical `scripts/run_experiment.py`; `scripts/run_pipeline.py` is a compatibility alias. Keep deterministic stub and real model modes separate. |
| Unfair query selection | High | Simple object queries favor LangSplat; relational graph queries favor ConceptGraphs; hierarchy queries favor SemanticSplat. | Use query buckets: simple object, attribute, spatial relation, zone, functional, aggregation. Report per bucket. |
| Missing ground truth for 3D IoU | High | Retrieval accuracy with IoU > 0.5 requires object annotations or a reliable proxy. | For Week 1, report qualitative smoke result. For experiments, choose scenes with labels or manually annotate a small query set. |

## Reproducibility Risks

| Risk | Severity | Notes | Mitigation |
|---|---:|---|---|
| Windows-specific helper scripts | Medium | `.cmd` scripts hardcode a Windows Miniconda path. | Add POSIX commands/scripts and avoid hardcoded user paths. |
| LLM/VLM nondeterminism | Medium | Tree construction and leaf confirmation may vary across runs. | Use temperature 0, save all prompts/responses, and version the model/provider. |
| External model/API dependency | Medium | Baselines and SemanticSplat may depend on different model APIs. | Log provider, model, parameters, request IDs if available, and all raw responses. |
| Large baseline setup burden | Medium | LangSplat and ConceptGraphs may require GPU dependencies, checkpoints, or dataset preprocessing. | Do not block Week 1 smoke test on full baseline runs. Write adapter docs first. |
| Dependency drift | Medium | Current requirements use lower bounds, not locked versions. | Create a lockfile or environment export after smoke test succeeds. |
| Generated outputs not versioned consistently | Medium | `outputs/` may become hard to compare across runs. | Use timestamped or named run folders with `run_config.json` and `logs.json`. |

## Baseline-Specific Risks

### LangSplat

| Risk | Severity | Notes | Mitigation |
|---|---:|---|---|
| Requires language-enhanced 3DGS training | High | Not a drop-in query over current SemanticSplat scene folders. | Budget separate setup time; start from official repo examples before adapting pilot scene. |
| Query semantics are flat | Medium | CLIP-like text grounding may not represent "near", "inside", "functional use", or multi-hop constraints reliably. | Evaluate simple and compositional query buckets separately. |
| Bbox extraction may be non-native | Medium | It may return relevancy/segmentation rather than a clean bbox. | Define thresholding/projected bbox adapter and report adapter assumptions. |
| Different reconstruction quality | Medium | If LangSplat trains its own 3DGS, geometry may differ from SemanticSplat's input. | Use the same source images/poses where possible and document reconstruction differences. |

### ConceptGraphs

| Risk | Severity | Notes | Mitigation |
|---|---:|---|---|
| Segmentation dependency | High | Missed or merged masks directly corrupt graph nodes. | Log segmentation outputs; separate "not detected" from "reasoning failed." |
| Object graph is not a room hierarchy | Medium | It may not produce room/zone tree outputs comparable to SemanticSplat. | Compare object/relations directly; do not force tree-coherence metric unless adding a hierarchy adapter. |
| Heavy preprocessing | Medium | Replica path may depend on Nice-SLAM-style Replica scans or specific dataloaders. | Choose pilot scene format with ConceptGraphs in mind; document exact adapter. |
| LLM graph reasoning differences | Medium | Its downstream query path may use a different LLM and context format. | Log prompts and normalize query set; report model differences. |

### LERF

| Risk | Severity | Notes | Mitigation |
|---|---:|---|---|
| Less direct than LangSplat | Medium | It is NeRF-based, not 3DGS-native. | Treat as related work or optional baseline. |
| Slow training | Medium | Running it may consume time without adding much beyond LangSplat. | Only run if mandatory baselines are already aligned. |
| Relevancy-map thresholding | Medium | Success depends on thresholding and projection choices. | Fix a threshold protocol or use peak-in-ground-truth metric. |

### Semantic Gaussians / LEGS / Other 3DGS Methods

| Risk | Severity | Notes | Mitigation |
|---|---:|---|---|
| Scope creep | Medium | Many related 3DGS semantic methods exist; running all is unrealistic. | Keep as related work unless a reviewer specifically expects one. |
| Different tasks | Medium | Some focus on semantic segmentation or online robot mapping, not query-answering. | Use only metrics that match native outputs. |

## Metric Risks

| Metric | Risk | Mitigation |
|---|---|---|
| Retrieval accuracy | Needs ground-truth query answers and a rule for partial matches. | Define query set with expected target object/zone. |
| 3D IoU > 0.5 | Needs object-level 3D boxes or masks. | Use labeled datasets or manually annotated pilot objects. |
| Zone accuracy | Replica/ScanNet room labels may not match our semantic zones. | Map tree nodes to room labels with a documented matching rule. |
| Tree coherence | LLM-as-judge can be subjective. | Use blinded pairwise comparison plus fixed rubric. |
| Context efficiency | Token accounting differs across methods. | Count prompt tokens for SemanticSplat/graph methods; use "not applicable" for non-LLM query paths. |
| Scalability | Construction time and query time are different costs. | Report separately: preprocessing, construction, query latency. |

## Limitations To Include Early

The paper and Week 1 status should be honest about:

| Limitation | Reason |
|---|---|
| The headless runner exists, but the UI query flow remains simulated and live provider execution is not installed. | Stub orchestration is reproducible; it is not live VLM/LLM reasoning. |
| Baselines may require adapters that affect measured outputs. | LangSplat, ConceptGraphs, and SemanticSplat do not share a native output format. |
| VLM descriptions can hallucinate or miss small objects. | Errors propagate into the tree and query answers. |
| 3D bbox quality depends on depth quality and 2D bbox quality. | Thin, reflective, or occluded objects may fail IoU even when the semantic answer is right. |
| Hierarchy metrics are less standardized than segmentation metrics. | Need a clear rubric and possibly human or LLM judging. |

## Week 1 Decision Points For Aleksander

| Decision | Recommended Default |
|---|---|
| What is the primary baseline comparison? | LangSplat for language-field localization; ConceptGraphs for object graph reasoning. |
| What is the primary success result? | One headless SemanticSplat run producing `views.json`, `tree.json`, `query_result.json`, and `logs.json`. |
| What should not be promised yet? | Full baseline execution, large-scale statistical significance, and final 3D IoU results. |
| What should the protocol require from every method? | Shared query set, shared scene IDs, shared output schema, logged runtime, logged failure reason. |
