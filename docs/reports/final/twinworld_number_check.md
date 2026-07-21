# TwinWorld number cross-check

Source of truth: `outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/metrics_summary.json`

Checks: 91 - mismatches: 0

| Name | Got | Expected | OK |
|---|---:|---:|:---:|
| `five.views_flat` | 19.4 | 19.4 | yes |
| `five.views_graph` | 4.77 | 4.77 | yes |
| `five.tok_flat` | 3168.2 | 3168.2 | yes |
| `five.tok_graph` | 1014.26 | 1014.26 | yes |
| `five.sav_views` | 75.5 | 75.5 | yes |
| `five.sav_tok` | 68.2 | 68.2 | yes |
| `five.hit1_flat` | 0.768 | 0.768 | yes |
| `five.hit1_graph` | 0.68 | 0.68 | yes |
| `five.hit3_flat` | 0.928 | 0.928 | yes |
| `five.hit3_graph` | 0.808 | 0.808 | yes |
| `five.tok_sum_flat` | 475230.0 | 475230 | yes |
| `five.tok_sum_graph` | 152139.0 | 152139 | yes |
| `five.captured_view_count` | 97 | 97 | yes |
| `construction.provider_calls` | 0 | 0 | yes |
| `construction.provider_tokens` | 0 | 0 | yes |
| `construction.views` | 97 | 97 | yes |
| `construction.items` | 1066 | 1066 | yes |
| `construction.nodes` | 1064 | 1064 | yes |
| `construction.source_token_equivalent` | 66937 | 66937 | yes |
| `construction.tree_token_equivalent` | 179817 | 179817 | yes |
| `replica_pilot_v1.n` | 56 | 56 | yes |
| `replica_pilot_v1.acc025_graph` | 1.0 | 1.0 | yes |
| `replica_pilot_v1.acc025_flat` | 1.0 | 1.0 | yes |
| `replica_pilot_v1.obj_graph` | 12.107143 | 12.107143 | yes |
| `replica_pilot_v1.obj_flat` | 71.875 | 71.875 | yes |
| `scannet_pilot_v1.n` | 48 | 48 | yes |
| `scannet_pilot_v1.acc025_graph` | 0.270833 | 0.270833 | yes |
| `scannet_pilot_v1.acc025_flat` | 0.270833 | 0.270833 | yes |
| `scannet_pilot_v1.obj_graph` | 11.229167 | 11.229167 | yes |
| `scannet_pilot_v1.obj_flat` | 49.0 | 49.0 | yes |
| `conceptgraphs_scannet.n` | 48 | 48 | yes |
| `conceptgraphs_scannet.acc025` | 0.0625 | 0.0625 | yes |
| `conceptgraphs_scannet.mean_iou` | 0.0696 | 0.0696 | yes |
| `conceptgraphs_scannet.runtime` | 0.3363 | 0.3363 | yes |
| `conceptgraphs_scannet.tokens` | 627 | 627 | yes |
| `conceptgraphs_replica.n` | 48 | 48 | yes |
| `conceptgraphs_replica.acc025` | 0.0625 | 0.0625 | yes |
| `conceptgraphs_replica.mean_iou` | 0.0624 | 0.0624 | yes |
| `conceptgraphs_replica.runtime` | 0.2743 | 0.2743 | yes |
| `conceptgraphs_replica.tokens` | 459 | 459 | yes |
| `langsplat_scannet.n` | 6 | 6 | yes |
| `langsplat_scannet.view_hit` | 0.6667 | 0.6667 | yes |
| `langsplat_scannet.runtime` | 2.0365 | 2.0365 | yes |
| `langsplat_scannet.tokens` | 74 | 74 | yes |
| `langsplat_scannet.iou_na` | 0 | 0 | yes |
| `tex_free_of:71.4\%` | 1 | 1 | yes |
| `tex_free_of:65.1\%` | 1 | 1 | yes |
| `tex_free_of:0.792` | 1 | 1 | yes |
| `tex_free_of:19.2 to 5.39` | 1 | 1 | yes |
| `tex_free_of:from 19.2` | 1 | 1 | yes |
| `tex_free_of:3104 to 1062` | 1 | 1 | yes |
| `tex_free_of:96 views` | 1 | 1 | yes |
| `tex_free_of:Person 1` | 1 | 1 | yes |
| `tex_free_of:Person 2` | 1 | 1 | yes |
| `tex_free_of:Person 3` | 1 | 1 | yes |
| `tex_free_of:Person 4` | 1 | 1 | yes |
| `tex_free_of:Person~` | 1 | 1 | yes |
| `tex_free_of:calibrated fallback` | 1 | 1 | yes |
| `tex_free_of:\subsection{Capture and semantic index}` | 1 | 1 | yes |
| `tex_free_of:XXXXX` | 1 | 1 | yes |
| `tex_has:97 views` | 1 | 1 | yes |
| `tex_has:75.5\%` | 1 | 1 | yes |
| `tex_has:68.2\%` | 1 | 1 | yes |
| `tex_has:0.68` | 1 | 1 | yes |
| `tex_has:19.4` | 1 | 1 | yes |
| `tex_has:4.77` | 1 | 1 | yes |
| `tex_has:Acc@.25 $=.063$` | 1 | 1 | yes |
| `tex_has:view hit $=.667$` | 1 | 1 | yes |
| `tex_has:0.0696` | 1 | 1 | yes |
| `tex_has:0.0624` | 1 | 1 | yes |
| `tex_has:CG--Replica` | 1 | 1 | yes |
| `tex_has:& .274 & 459` | 1 | 1 | yes |
| `tex_has:[73.2,77.7]` | 1 | 1 | yes |
| `tex_has:[65.3,71.0]` | 1 | 1 | yes |
| `tex_has:[-0.184,0.008]` | 1 | 1 | yes |
| `tex_has:20,260,715` | 1 | 1 | yes |
| `tex_has:\subsection{Hierarchical query representation}` | 1 | 1 | yes |
| `tex_has:Hierarchical semantic tree used at query time` | 1 | 1 | yes |
| `tex_has:through zone, region, object, and view-observation levels` | 1 | 1 | yes |
| `tex_has:c_i=(\mathrm{id}_i,\tau_i,A_i,y_i,x_i,R_i,B_i,V_i)` | 1 | 1 | yes |
| `tex_has:\subsection{Captured-scene zone pruning}` | 1 | 1 | yes |
| `tex_has:\subsection{Object-level lexical and intent scoring}` | 1 | 1 | yes |
| `tex_has:\subsection{Target--anchor spatial reasoning}` | 1 | 1 | yes |
| `tex_has:\subsection{Fallback, variants, and measured cost}` | 1 | 1 | yes |
| `tex_has:\subsection{Input representation and index construction}` | 1 | 1 | yes |
| `tex_has:figures/fig_method_workflow.pdf` | 1 | 1 | yes |
| `tex_has:provider calls and zero provider input/output tokens` | 1 | 1 | yes |
| `tex_has:66,937` | 1 | 1 | yes |
| `tex_has:179,817` | 1 | 1 | yes |
| `tex_has:1.822\,s` | 1 | 1 | yes |
| `tex_has:annotation is unmetered and therefore` | 1 | 1 | yes |
