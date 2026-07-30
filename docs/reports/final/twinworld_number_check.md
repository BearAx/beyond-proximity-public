# TwinWorld number cross-check

The anonymous TwinWorld manuscript is checked against the frozen instruction-agent, raw RGB-D hierarchy, and calibrated public-dataset outputs.

Checks: 109; mismatches: 0.

| Check | Got | Expected | Pass |
|---|---|---|:---:|
| `agent.status` | `complete` | `complete` | yes |
| `agent.queries` | `150` | `150` | yes |
| `agent.quality_denominator` | `125` | `125` | yes |
| `agent.hit1` | `0.368` | `0.368` | yes |
| `agent.hit3` | `0.696` | `0.696` | yes |
| `agent.mrr` | `0.509333` | `0.509333` | yes |
| `agent.views` | `9.626667` | `9.626667` | yes |
| `agent.calls` | `300` | `300` | yes |
| `agent.tokens` | `239893` | `239893` | yes |
| `agent.valid` | `1.0` | `1.0` | yes |
| `agent.trace_count` | `150` | `150` | yes |
| `raw.status` | `complete` | `complete` | yes |
| `raw.rgb` | `97` | `97` | yes |
| `raw.depth` | `97` | `97` | yes |
| `raw.poses` | `97` | `97` | yes |
| `raw.model_calls` | `15` | `15` | yes |
| `raw.label_tokens` | `151` | `151` | yes |
| `raw.manual_viewjson_reads` | `0` | `0` | yes |
| `raw.manual_zone_reads` | `0` | `0` | yes |
| `raw.pairwise_f1` | `0.486673` | `0.486673` | yes |
| `raw.rand` | `0.637318` | `0.637318` | yes |
| `raw.hit1` | `0.368` | `0.368` | yes |
| `raw.hit3` | `0.528` | `0.528` | yes |
| `raw.views` | `10.0` | `10.0` | yes |
| `cursor.direct_mcp_calls` | `True` | `True` | yes |
| `cursor.mcp_calls` | `5` | `5` | yes |
| `cursor.provider_tokens` | `None` | `None` | yes |
| `cursor.zones` | `18` | `18` | yes |
| `cursor.pairwise_f1` | `0.616174` | `0.616174` | yes |
| `cursor.hit1` | `0.704` | `0.704` | yes |
| `cursor.hit3` | `0.784` | `0.784` | yes |
| `cursor.views` | `5.533333` | `5.533333` | yes |
| `semantic.hit1` | `0.784` | `0.784` | yes |
| `semantic.hit3` | `0.904` | `0.904` | yes |
| `bootstrap.samples` | `10000` | `10000` | yes |
| `bootstrap.view_savings` | `75.4887` | `75.4887` | yes |
| `bootstrap.hit1_low` | `-0.184` | `-0.184` | yes |
| `bootstrap.hit1_high` | `0.008` | `0.008` | yes |
| `bootstrap.hit3_low` | `-0.184` | `-0.184` | yes |
| `bootstrap.hit3_high` | `-0.056` | `-0.056` | yes |
| `phase6_replica_calibrated_v3.queries` | `56` | `56` | yes |
| `phase6_replica_calibrated_v3.acc025` | `1.0` | `1.0` | yes |
| `phase6_replica_calibrated_v3.objects` | `12.107143` | `12.107143` | yes |
| `phase6_replica_calibrated_v3.tokens` | `302.678571` | `302.678571` | yes |
| `phase6_scannet_calibrated_v3.queries` | `48` | `48` | yes |
| `phase6_scannet_calibrated_v3.acc025` | `0.604167` | `0.604167` | yes |
| `phase6_scannet_calibrated_v3.objects` | `4.729167` | `4.729167` | yes |
| `phase6_scannet_calibrated_v3.tokens` | `219.3125` | `219.3125` | yes |
| `phase6_scannet_extended_v3.queries` | `64` | `64` | yes |
| `phase6_scannet_extended_v3.acc025` | `0.589286` | `0.589286` | yes |
| `phase6_scannet_extended_v3.objects` | `4.375` | `4.375` | yes |
| `phase6_scannet_extended_v3.tokens` | `200.0625` | `200.0625` | yes |
| `scannet.no_relation_acc025` | `0.5` | `0.5` | yes |
| `tex_has:\title{SemanticSplat: Graph-Pruned Semantic Search}` | `True` | `True` | yes |
| `tex_has:\author{Anonymous Authors}` | `True` | `True` | yes |
| `tex_has:\subsection{Instruction-agent traversal}` | `True` | `True` | yes |
| `tex_has:\subsection{Agent/MCP hierarchy construction}` | `True` | `True` | yes |
| `tex_has:\subsection{Automatic raw RGB-D hierarchy}` | `True` | `True` | yes |
| `tex_has:\subsection{Local instruction-model stress test}` | `True` | `True` | yes |
| `tex_has:\subsection{Raw RGB-D hierarchy versus manual reference}` | `True` | `True` | yes |
| `tex_has:\subsection{Semantic-record construction variants}` | `True` | `True` | yes |
| `tex_has:figures/fig_instruction_agent.pdf` | `True` | `True` | yes |
| `tex_has:figures/fig_raw_rgbd_hierarchy.pdf` | `True` | `True` | yes |
| `tex_has:figures/fig_hierarchy_construction_variants.pdf` | `True` | `True` | yes |
| `tex_has:figures/fig_agent_mcp_workflow.pdf` | `True` | `True` | yes |
| `tex_has:SayPlan~\cite{rana2023sayplan}` | `True` | `True` | yes |
| `tex_has:Search3D~\cite{takmaz2025search3d}` | `True` | `True` | yes |
| `tex_has:reads zero manual ViewJSON or zone` | `True` | `True` | yes |
| `tex_has:\AgentTotalCalls{} model calls` | `True` | `True` | yes |
| `tex_has:\CursorMcpCalls{} direct tool calls` | `True` | `True` | yes |
| `tex_has:Cursor changes hit@1 by $+0.024$ and hit@3` | `True` | `True` | yes |
| `tex_has:1-4.77/19.40=75.4\%` | `True` | `True` | yes |
| `tex_has:\HitOneLow{}, \HitOneHigh{}` | `True` | `True` | yes |
| `tex_has:\HitThreeLow{}, \HitThreeHigh{}` | `True` | `True` | yes |
| `tex_has:inconclusive` | `True` | `True` | yes |
| `tex_has:significant decline` | `True` | `True` | yes |
| `tex_has:Replica (56; 48+)` | `True` | `True` | yes |
| `tex_has:ScanNet (48; 48+)` | `True` | `True` | yes |
| `tex_has:Replica's exact-match ceiling is only a protocol sanity check` | `True` | `True` | yes |
| `tex_has:relation scoring reduces Acc@0.25 to 0.500` | `True` | `True` | yes |
| `tex_has:The superseded reranker underperformed because it applied low-confidence` | `True` | `True` | yes |
| `tex_has:Qwen/Qwen2.5-0.5B-Instruct` | `True` | `True` | yes |
| `tex_has:openai/clip-vit-base-patch32` | `True` | `True` | yes |
| `tex_free_of:Paper ID #XXXXX` | `True` | `True` | yes |
| `tex_free_of:XXXXX` | `True` | `True` | yes |
| `tex_free_of:Person 1` | `True` | `True` | yes |
| `tex_free_of:Person 2` | `True` | `True` | yes |
| `tex_free_of:Person 3` | `True` | `True` | yes |
| `tex_free_of:Person 4` | `True` | `True` | yes |
| `tex_free_of:ScanNet oracle-map pilot, graph search matches flat lexical Recall@1 / Acc@0.25 ($0.271$)` | `True` | `True` | yes |
| `tex_free_of:Relation reranking does not help` | `True` | `True` | yes |
| `tex_free_of:Stub / deterministic lexical matching is not live provider-backed VLM evaluation` | `True` | `True` | yes |
| `macro:AgentHitOne` | `0.368` | `0.368` | yes |
| `macro:AgentHitThree` | `0.696` | `0.696` | yes |
| `macro:AgentTotalCalls` | `300` | `300` | yes |
| `macro:AgentTotalTokens` | `239893` | `239893` | yes |
| `macro:RawConstructionCalls` | `15` | `15` | yes |
| `macro:RawConstructionTokens` | `151` | `151` | yes |
| `macro:RawPairwiseFOne` | `0.487` | `0.487` | yes |
| `macro:RawHitThree` | `0.528` | `0.528` | yes |
| `macro:CursorMcpCalls` | `5` | `5` | yes |
| `macro:CursorPairwiseFOne` | `0.616` | `0.616` | yes |
| `macro:CursorHitThree` | `0.784` | `0.784` | yes |
| `macro:ViewSavingsPerQuery` | `75.5` | `75.5` | yes |
| `macro:HitOneLow` | `-0.184` | `-0.184` | yes |
| `macro:HitOneHigh` | `0.008` | `0.008` | yes |
| `macro:HitThreeHigh` | `-0.056` | `-0.056` | yes |
| `validation:five_scene_qwen25_05b_graph_v1` | `passed` | `passed` | yes |
| `validation:five_scene_clip_v1` | `passed` | `passed` | yes |
