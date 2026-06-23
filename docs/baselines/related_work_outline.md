# Related Work Outline

This outline separates method families by their native task. It is not evidence that every method has been run in this repository. Citation metadata comes from `baseline_references.bib`; entries marked `TODO` must be verified before publication.

## 1. Language-Embedded Neural Fields

### LERF

- Establish LERF as the canonical NeRF language-field reference.
- Describe its multi-scale text relevancy output and open-vocabulary localization task.
- State that it has no native room hierarchy or graph traversal trace.
- Compare only on compatible localization queries and measured outputs.

### LangSplat

- Present LangSplat as the mandatory 3DGS language-field baseline.
- Explain its language feature distillation and text-query relevancy output.
- Distinguish native object localization from relational or hierarchy reasoning added by an external adapter.
- Report reconstruction/training cost separately from query latency.

### Semantic Gaussians and LEGS

- Use Semantic Gaussians as related work for semantics attached to 3D Gaussians.
- Use LEGS as related work for incremental, room-scale language-embedded mapping.
- Keep both optional for Week 2/3 because their native data and runtime requirements do not match the current pilot scene directly.
- Do not imply an experimental comparison until an adapter produces canonical records.

## 2. Open-Vocabulary 3D Scene Graphs

### ConceptGraphs

- Present ConceptGraphs as the mandatory graph-based baseline.
- Describe object detection/association, 3D object map construction, captions, and relations.
- Compare object and relational query behavior separately from room/zone hierarchy behavior.
- Track segmentation failures separately from query-reasoning failures.

### BBQ

- Describe BBQ as an optional object-centric graph method designed for complex referring expressions.
- Discuss metric and semantic relations plus deductive language reasoning.
- Use it to motivate a separate relational-query comparison if a runnable adapter becomes available.
- Do not combine its reported paper results with measurements from this repository.

## 3. SemanticSplat Positioning

- SemanticSplat consumes posed views and semantic descriptions, then exposes an explicit hierarchy and traversal trace.
- Its intended distinction is hierarchy-aware, interpretable query routing, not a claim of superior native segmentation.
- Language-field methods are strongest comparators for simple object and attribute grounding.
- Object-graph methods are strongest comparators for object and relational reasoning.
- Zone/hierarchy, functional, aggregation, and negative queries must be reported as separate buckets because support differs by method family.

## 4. Evidence Required Before Paper Claims

- Verify every `TODO` bibliography entry against an official source.
- Run all compared methods on the same source frames, poses, intrinsics, and query strings.
- Save native outputs and canonical adapter outputs.
- Separate preprocessing, map construction, and measured query latency.
- Mark unavailable localization metrics as `N/A`; do not convert missing geometry into zero accuracy.
- Report stub, simulated, cached-live, and live results in separate tables.
