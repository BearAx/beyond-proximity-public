# Hierarchy construction evaluation

The manual zones are a human/Cursor-assisted reference, not independent dataset GT. Cursor Agent used the project MCP server directly and was not shown the manual-zone file.

| Variant | Zones | Pairwise F1 | Weighted Jaccard | Hit@1 | Hit@3 | MRR | Views/query | Tokens/query |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| manual_reference | 26 | 1.0 | 1.0 | 0.68 | 0.808 | 0.742 | 4.766667 | 1014.26 |
| pose_only | 10 | 0.587981 | 0.526425 | 0.76 | 0.88 | 0.829467 | 6.066667 | 1780.066667 |
| pose_semantic_merge | 8 | 0.570476 | 0.50379 | 0.784 | 0.904 | 0.844933 | 5.8 | 1747.173333 |
| cursor_agent_mcp | 18 | 0.616174 | 0.609901 | 0.704 | 0.784 | 0.748667 | 5.533333 | 1193.186667 |

## Construction accounting

| Variant | Runtime status | Measured local seconds | Provider tokens | Serialized context tokens |
|---|---|---:|---:|---:|
| manual_reference | historical_human_time_unavailable | None | None | 8939 |
| pose_only | measured_local_deterministic | 0.041686 | 0 | 8939 |
| pose_semantic_merge | measured_local_deterministic | 0.042405 | 0 | 8939 |
| cursor_agent_mcp | unavailable_cursor_agent_ui_not_metered | None | None | 8939 |

Provider tokens remain `N/A` for the historical manual reference and Cursor UI run because neither exposes an auditable token counter. Deterministic variants make no provider calls, so their provider-token count is exactly 0.
