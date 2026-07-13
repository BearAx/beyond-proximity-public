# Grounding variant comparison

| Variant | Recall@1 | Acc@0.1 | Acc@0.25 | Acc@0.5 | Checked objects | Runtime (s) |
|---|---:|---:|---:|---:|---:|---:|
| graph | 1.0 | 1.0 | 1.0 | 1.0 | 12.107143 | 0.000903 |
| graph_fallback | 1.0 | 1.0 | 1.0 | 1.0 | 41.75 | 0.001257 |
| flat_lexical | 1.0 | 1.0 | 1.0 | 1.0 | 71.875 | 0.008785 |
| flat_embedding | 0.833333 | 0.875 | 0.875 | 0.833333 | 71.875 | 0.137096 |
| ablation_no_hierarchy | 1.0 | 1.0 | 1.0 | 1.0 | 71.875 | 0.008952 |
| ablation_no_relation | 1.0 | 1.0 | 1.0 | 1.0 | 41.75 | 0.001087 |
| ablation_no_fallback | 1.0 | 1.0 | 1.0 | 1.0 | 12.107143 | 0.000936 |
| ablation_flat_only | 1.0 | 1.0 | 1.0 | 1.0 | 71.875 | 0.001026 |
