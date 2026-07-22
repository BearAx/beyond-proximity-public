# SemanticSplat — Updated Research Direction

## 1. Main Direction

The next phase should focus on **adapting the existing legacy graph system to the five captured scenes and evaluating graph-vs-flat reasoning for environment understanding**.

The important correction is that the project already contains a **working graph system in the main/legacy path**. It includes a real hierarchical structure, traversal helpers, Query Flow UI, and graph-vs-flat benchmark code. Therefore, we do **not** need to build a graph engine from scratch.

The current gap is different:

> The five Week 3 captured scenes are validated as manual semantic indexes, but they are not yet fully represented in the same rich graph model as the main/legacy system.

So the research direction is:

> Bridge the existing graph pipeline with the five captured scenes and 1,046 semantic items, enrich them with zone-region-object-affordance relations, and run a fair graph-vs-flat benchmark on the same inputs.

## 2. Why This Direction

This is the strongest direction because it connects both parts of the project:

1. **The project already has a working graph system** in the main/default path.
2. **The project also has five captured scenes** with manual ViewJSON semantic indexes, generated trees, and 1,046 semantic items.
3. The missing step is to make the captured-scene data use the full graph reasoning pipeline.

This gives us a realistic research claim:

> Given the same semantic map and the same natural-language queries, graph-based reasoning should scan fewer entries, use less context/tokens, and answer faster than flat search while preserving useful target quality.

This direction also keeps the key product idea: the system should understand the environment, not only search object names. For example, a query like:

```text
Find a place where I can sit.
```

should map to:

```text
intent = find_sittable_place
acceptable targets = chair, sofa, armchair, bench, seating area, lounge area
```

Then the graph can prune irrelevant zones, regions, and objects before ranking candidates.

## 3. Current Honest Status

The correct current status is:

- The **main/legacy version** has a working graph system.
- The **five captured scenes** currently use manual ViewJSON semantic indexes and generated tree JSON files.
- For the captured scenes, the generated tree is still mostly flat: `root -> region/object/landmark`.
- Captured-scene objects have `view_ids`, `label`, `attributes`, and `approx_location`, but usually no explicit `region_id` / `zone_id`.
- `bbox_2d` and `bbox_3d` are mostly null, so precise object-level 3D navigation is not available yet.
- Query execution over the captured scenes currently relies on stub/lexical matching over the semantic index.
- Therefore, search examples such as `find a piano` demonstrate working semantic search, but they are not yet enough to prove graph-vs-flat efficiency on the captured dataset.

This is good news: the project does not lack a graph system. The next task is to **adapt the existing graph pipeline to the new validated semantic data**.

## 4. Research Question

The main research question should be:

> Can an existing hierarchical semantic graph pipeline answer natural-language environment-understanding queries faster and with less context than flat search when both methods operate over the same captured semantic items?

Secondary question:

> Can affordance-aware graph reasoning support intent queries such as “where can I sit?”, “where can I charge my phone?”, or “where is the nearest exit?”?

## 5. Core Technical Plan

### Step 1 — Reuse the Existing Legacy Graph Pipeline

Inspect and reuse the main/default graph system:

- tree node structures
- traversal helpers
- Query Flow logic
- existing graph-vs-flat benchmark code
- existing benchmark documentation

The goal is not to rewrite this system, but to make it work with the five captured scenes.

### Step 2 — Convert Captured Scene Data into the Full Graph Model

For each captured scene, convert the current ViewJSON semantic index into a richer graph structure:

```text
root -> zone -> region -> object / landmark / facility / sign / exit
```

Add explicit fields where possible:

- `zone_id`
- `region_id`
- `view_ids`
- `affordances`
- `belongs_to`
- `contains`
- `visible_from`
- `near`
- `connected_to`

Example:

```json
{
  "object_id": "sofa_01",
  "label": "sofa",
  "canonical_category": "furniture",
  "affordances": ["sittable"],
  "region_id": "lounge_seating_area_01",
  "zone_id": "conference_hall_lobby",
  "view_ids": ["v010"],
  "relations": [
    {"type": "belongs_to", "target": "lounge_seating_area_01"},
    {"type": "visible_from", "target": "v010"}
  ]
}
```

### Step 3 — Add Affordance-Aware Query Expansion

Add a small deterministic intent/affordance layer:

```text
sit -> sittable -> chair, sofa, armchair, bench, seating area
charge phone -> chargeable -> outlet, charging station, desk area
exit / leave -> exit, door, corridor, exit sign
ask for help -> reception, information desk, staff area
```

This is important because environment understanding is not only object matching. The system should understand what type of place or object satisfies the user’s intent.

### Step 4 — Build a Verified Captured-Scene Benchmark

Create a benchmark with 100–150 verified queries over the five captured scenes.

Each query should include:

- `query_id`
- `scene_id`
- `query`
- `query_type`
- `expected_affordance`
- `expected_object_categories`
- `expected_region_ids`
- `expected_zone_ids`
- `expected_view_ids`
- optional `current_view_id` for view-relative navigation

Main query types:

- simple semantic search
- affordance / intent navigation
- relational search
- multi-hop search
- repetitive-space ambiguity
- small map freshness pilot

### Step 5 — Run Fair Graph-vs-Flat Comparison

Compare methods on the same captured semantic items and the same verified queries:

| Method | Description |
|---|---|
| `flat_lexical` | Search over all semantic entries using text matching. |
| `flat_embedding` | Embedding search over all semantic entries, if available. |
| `legacy_graph_adapted` | Existing graph traversal adapted to captured scenes. |
| `graph_affordance_pruned` | Intent/affordance expansion + graph pruning + ranking. |

The key point is fairness: all methods must use the same scenes, same semantic items, and same query set.

### Step 6 — Measure Efficiency and Quality

Efficiency metrics:

- `latency_ms`
- `semantic_entries_scanned`
- `objects_checked`
- `regions_checked`
- `views_checked`
- `context_size_chars`
- `estimated_input_tokens`
- `speedup_vs_flat`
- `token_reduction_vs_flat`

Quality metrics:

- `hit@1`
- `hit@3`
- `expected_object_hit`
- `expected_region_hit`
- `expected_zone_hit`
- `expected_view_hit`
- `wrong_zone_rate`

The main result should show whether graph reasoning reduces search cost while preserving useful target retrieval quality.

## 6. What We Should Not Claim Yet

We should avoid claiming:

- full automatic environment understanding
- full production-ready VLM pipeline
- precise metric object navigation
- complete ScanNet-scale validation
- superiority over ConceptGraphs or LangSplat
- 3D IoU accuracy without ground-truth 3D boxes

These can remain future work or secondary validation.

## 7. Expected Paper Story

The final paper can be framed as:

1. Indoor maps and 3D reconstructions provide geometry, but not enough semantic meaning.
2. SemanticSplat adds a semantic understanding layer above captured visual/3D observations.
3. The project already has a working graph system in the main/legacy path.
4. The new five-scene dataset provides validated manual semantic indexes and 1,046 semantic items.
5. We adapt the existing graph pipeline to this captured dataset.
6. We enrich the captured semantic items with zone-region-object-affordance relations.
7. We evaluate natural-language environment-understanding queries.
8. We compare flat search against graph-based reasoning on the same scenes and queries.
9. We measure latency, scanned entries, context/tokens, and target retrieval quality.

## 8. Immediate Next Milestone

The next milestone should be:

> Adapt the existing legacy graph system to the five captured scenes, enrich the captured semantic items with explicit relations and affordances, and run a fair graph-vs-flat benchmark on verified environment-understanding queries.

This is stronger and more realistic than building a new graph system from scratch. It uses what already works in the project and turns it into measurable evidence for a research-oriented arXiv preprint.
