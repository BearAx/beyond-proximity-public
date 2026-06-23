# Query Flow — usable view images (2026-06-12)

## What was done

- **Problem:** Query Flow showed annotated images from dark placeholder PNGs (`v001`–`v003`, mean luminance ~77) while JSON analysis claimed a match — user saw a black box, not a sofa.
- **Fix:** Skip placeholder images when picking the best leaf view; rank by confidence, bbox, centrality, and **PNG brightness** (`view_image_usable`, threshold mean ≥ 100).
- **Graph/flat search:** Check all views in a leaf, collect candidates, pick best usable view (not first JSON match).
- **`backend/query/live_session.py`:** Reusable `run_query_session(scene_id, session_id)` for Cursor live Query Flow logging.
- **Re-ran session `68b30f74`:** result **v004** (real lounge photo, sofa bbox) instead of v001.

## Files changed

- `backend/io/annotator.py` — `view_image_usable`, `view_image_mean_luminance`
- `backend/query/pipeline.py` — image quality in `score_view_result` / `rank_leaf_results`
- `backend/query/benchmark.py` — `_pick_best_leaf_match`, leaf candidate helpers
- `backend/query/live_session.py` — new
- `backend/mcp/tools/tree_tools.py` — `rank_leaf_results_tool(scene_id, …)`
- `tests/backend/test_benchmark.py` — `test_find_sofa_picks_usable_view`

## Next steps

- Replace stub PNGs for `v001`–`v003` with real captures from Navigator (**R**) if those views matter for demos.
- Optional: show annotated image on RESULT card too (not only leaf_check).
