# SemanticSplat Interactive Demo Script

Target duration: 6:30-7:00. Hard limit: 8:00.

## Open Before Recording

1. Interactive application: <http://127.0.0.1:5173/>
2. Latest local research page: <http://127.0.0.1:4173/>
3. Final report: `C:\GitProjects\beyond-proximity\output\pdf\semanticsplat_final_project_journey_report_2026-07-22.pdf`
4. Academic paper: `C:\GitProjects\beyond-proximity\papers\beyond-proximity\main.pdf`
5. Repository root: `C:\GitProjects\beyond-proximity`
6. Frozen main metrics: `C:\GitProjects\beyond-proximity\outputs\graph_vs_flat\five_scene_graph_vs_flat_v2\metrics_summary.json`

For the stable live demonstration, set:

- Scene ID: `default`, then click **Set**.
- 3D Scene: `ConferenceHall.ply`, then click **Load**.
- Query: `Find the piano`.

The scene is about 100 MB and may need 15-25 seconds to decode. Wait until the
loading message disappears before recording.

## 0:00-0:35 - Goal

### Say

"This is SemanticSplat, our graph-pruned semantic search system for captured 3D
scenes. We began with a visual 3D Gaussian Splatting navigator and one research
question: can a semantic hierarchy answer natural-language queries while
examining much less scene context than flat search? The final project combines
an interactive system, controlled evaluation, public-dataset experiments,
external baselines, and an academic paper."

### Show

- Open `http://127.0.0.1:5173/`.
- Keep the loaded Conference Hall scene visible.

## 0:35-1:15 - Starting Point And Development

### Say

"The first version was mainly a viewer with manual captures and a small scene
tree. We then added canonical ViewJSON records, five complete captured scenes,
ground-truth query labels, graph-versus-flat evaluation, ScanNet and Replica
pilots, ConceptGraphs and LangSplat executions, automated checks, and the final
release package. The four planned roles were completed and integrated."

### Show

- Open the final report PDF.
- Show page 3, then page 4, and briefly page 5.

## 1:15-2:10 - Interactive 3D Viewer

### Say

"The frontend loads a real Gaussian-splat scene rather than a static screenshot.
The camera can move through the reconstructed environment, and the same scene
can be connected to captured observations and semantic records. The viewer also
supports view capture for extending the semantic index."

### Show

- Return to `http://127.0.0.1:5173/` and select **Navigator**.
- Click inside the scene.
- Fly briefly with `W`, `A`, `S`, `D`; use the mouse to look around.
- Mention `Q/E` for vertical movement and `Shift` for faster movement.
- Do not press `R` during the recording unless you want to save a new capture.

## 2:10-2:50 - Semantic Hierarchy

### Say

"Instead of treating every view as an independent candidate, SemanticSplat
organizes evidence into a hierarchy. A query first chooses likely scene and
zone branches, then regions, objects, and supporting views. This is the source
of the reduction in checked views and serialized context."

### Show

- Confirm Scene ID is `default`.
- Click **Semantic Tree**.
- Click **Refresh Tree** if needed.
- Point to the Conference Hall root and its branches.

## 2:50-3:45 - Live Query

### Say

"Now I will execute a query through the application. The Ask button creates a
session and the backend runs the deterministic graph traversal. Query Flow
records decomposition, visited branches, checked leaves, and the final grounded
view. This local mode is reproducible and makes no external model call."

### Show

- Enter `Find the piano` in the top Query field.
- Click **Ask**.
- The app opens **Query Flow** automatically.
- Wait until the newest session changes from zero to seven steps.
- Open the newest session and show the final result in view `v007`.

Optional natural functional query:

1. Change Scene ID to `ConferenceHall-capture-pilot` and click **Set**.
2. Keep `ConferenceHall.ply` selected.
3. Ask `Find a place where I can sit`.
4. The captured-index query returns view `v002` in five steps.
5. Do not open **Semantic Tree** in this optional mode; return Scene ID to
   `default` before demonstrating the tree again.

## 3:45-4:45 - Main Metrics

### Say

"The main controlled benchmark contains 150 queries over identical semantic
records. Graph search checks 4.77 views per query instead of 19.4, which is
75.5 percent fewer. Estimated context decreases from 3,168 to 1,014 tokens per
query, a reduction of 68.2 percent. On 125 verified-view queries, graph hit at
one is 0.680 versus 0.768 for flat search, so the result is a measured
quality-cost trade-off rather than a claim of universal superiority."

### Show

- Open `http://127.0.0.1:4173/#results`.
- Keep the **Internal** result tab selected.
- Point to the view, token, hit@1, and hit@3 values.
- Optionally open `outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/metrics_summary.json`.

## 4:45-5:35 - ScanNet, Replica, And Baselines

### Say

"We expanded beyond the five manual scenes to eight Replica and eight ScanNet
scenes aligned with the closest BBQ work. Replica contributes 575 official 3D
boxes and 56 queries; ScanNet contributes 392 boxes and 48 queries. We also ran
ConceptGraphs on both eight-scene sets and completed the full LangSplat pipeline
on one ScanNet scene. Their protocols differ, so they are reported as native
executions and diagnostic evidence, not as an unfair leaderboard."

### Show

- On the research page, select **Public datasets** and then **External baselines**.
- In the repository, briefly show:
  - `outputs/public_datasets/`
  - `outputs/baselines/`
  - `docs/baselines/`

## 5:35-6:15 - Repository And Reproducibility

### Say

"The repository preserves the implementation, exact query sets, schemas,
per-query outputs, aggregate metrics, figure generators, and validation checks.
The final suite contains 145 passing tests, and manuscript numbers are checked
against frozen JSON so the paper and released evidence stay synchronized."

### Show

- Open `C:\GitProjects\beyond-proximity`.
- Show these paths:
  - `backend/query/live_session.py`
  - `backend/data/scenes/ConferenceHall-capture-pilot/`
  - `scripts/evaluate_grounding.py`
  - `outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/`
  - `papers/beyond-proximity/`

## 6:15-6:50 - Paper And Conclusion

### Say

"The resulting manuscript is SemanticSplat: Graph-Pruned Semantic Search. It
contains the complete method, evaluation contract, public pilots, baseline
boundaries, qualitative failure analysis, limitations, and reproduction
commands. The current evidence shows that hierarchy can remove most query
context, while calibrated pruning and shared predicted-map evaluation remain
the next research steps."

### Show

- Open `papers/beyond-proximity/main.pdf`.
- Show page 1, the method workflow, the main results, and the limitations.
- End on `http://127.0.0.1:4173/#paper`.

## Short Ending

"SemanticSplat now connects a working 3D application with controlled metrics,
public-dataset evidence, external executions, and a reproducible academic
release. Its strongest current result is substantial context reduction with an
explicitly measured quality trade-off."
