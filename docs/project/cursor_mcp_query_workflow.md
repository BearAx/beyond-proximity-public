# Cursor Agent MCP Query Workflow

This workflow executes the original agent-driven method while producing an
auditable trace compatible with the local semantic benchmark.

## Required MCP Call Sequence

1. `start_agent_query_trace`
   - provide `scene_id`, `query`, Cursor model name, and optional `query_id`;
   - retain the returned `trace_id`.
2. `get_query_decomposition`
   - send the returned prompt to the active Cursor model;
   - record the tool response and model JSON with `record_agent_query_step`.
3. `get_root_node`
   - obtain the starting node.
4. `get_children`
   - pass the original query and decomposition JSON;
   - send its prompt to Cursor;
   - record the selected `descend_into` IDs, tokens, and latency;
   - repeat until candidate leaves are reached.
5. `get_leaf_confirmation_view`
   - inspect each candidate view conservatively;
   - record positive and negative checks, not only the final answer.
6. `rank_leaf_results`
   - select the best grounded evidence.
7. Use `unproject_bbox` when a valid 2D box and depth are available.
8. `finish_agent_query_trace`
   - store the final IDs, box, confidence, and any warnings.
9. `get_agent_query_trace`
   - reload the saved trace and confirm that it is complete.

## Recording Rules

- Record one trace step after every model decision.
- Use the exact Cursor model/version shown by the client.
- Store input and output tokens only when Cursor reports them.
- Use null rather than zero when usage is unavailable.
- Record wall-clock latency around the model decision, not the MCP file read.
- Never paste secrets, credentials, or unrelated conversation into a trace.
- Preserve all considered node/view IDs so pruning can be audited.

## Minimum Final Result

```json
{
  "found": true,
  "selected_node_id": "node_id",
  "selected_view_id": "v018",
  "selected_object_id": "object_id_or_null",
  "bbox_2d": null,
  "bbox_3d": null,
  "confidence": "high",
  "answer": "Grounded answer based only on recorded scene evidence."
}
```

The resulting file is written under:

```text
outputs/agent_traces/cursor_mcp/<trace_id>.json
```

Cursor execution and local BGE execution must be reported separately. A local
embedding trace is reproducible semantic evidence, but it is not a Cursor or
LLM trace.
