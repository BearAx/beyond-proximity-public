# SemanticSplat Demo Video Script

Target duration: 7 minutes 20 seconds. Hard limit: 8 minutes.

Local website: <http://127.0.0.1:4173/>

Public website: <https://leopython2006.github.io/beyond-proximity-public/>

Repository: <https://github.com/LeoPython2006/beyond-proximity>

Latest public-source branch:
<https://github.com/BearAx/beyond-proximity-public/tree/codex/project-site-method-figure>

Upstream deployment compare link:
<https://github.com/LeoPython2006/beyond-proximity-public/compare/codex/project-site-method-figure...BearAx:codex/project-site-method-figure?expand=1>

## Before Recording

Open these tabs/windows in advance:

1. Local project page: `http://127.0.0.1:4173/`
2. Public GitHub Pages URL.
3. Repository root: `C:\GitProjects\beyond-proximity`
4. Academic paper PDF: `C:\GitProjects\beyond-proximity\papers\beyond-proximity\main.pdf`
5. Final report PDF: `C:\GitProjects\beyond-proximity\output\pdf\semanticsplat_final_project_journey_report_2026-07-22.pdf`
6. A terminal opened in `C:\GitProjects\beyond-proximity`.

Before recording the final GitHub Pages segment, ask Leo to merge the upstream
compare link above. The latest branch is pushed and locally verified, but the
Leo-owned Pages URL is currently serving the previous deployment. Until that
merge finishes, use the local site for the current method, paper, and metrics.

Use browser zoom around 90%-100%. Keep the mouse still while speaking and scroll
only at the points marked below.

## 0:00-0:35 - Opening And Research Goal

### Say

"This is SemanticSplat, our graph-pruned semantic search system for captured 3D
scenes. We started with a small 3D Gaussian Splatting query prototype and one
main question: can we answer natural-language scene queries without scanning
every captured view? We ended with a reproducible research package containing
captured scenes, public-dataset evaluation, external baseline executions, an
academic paper, and a public project page."

### Show

- Open `http://127.0.0.1:4173/`.
- Keep the hero and the five headline metrics visible.
- Briefly point at `97 views`, `1,066 semantic items`, `150 queries`, `75.5%`,
  and `68.2%`.

## 0:35-1:15 - Where We Started And How The Work Evolved

### Say

"The early version already had a viewer, a query interface, and a small semantic
tree, but the evidence was mainly a demo. We then built a controlled benchmark,
manual reference labels, canonical result schemas, public dataset importers,
BBQ-aligned metrics, and automated checks. The work was divided across four
roles: public data and ground truth, algorithm and evaluation, baselines and
related work, and finally the paper and release package. All four repository-side
acceptance records were completed and integrated."

### Show

- Open the final report PDF.
- Show page 3, `Where the project started`, then page 4, the milestone timeline.
- Move briefly to page 5, `Four-person plan completion`.

## 1:15-2:10 - Method

### Say

"The method begins with posed RGB-D evidence and normalized semantic ViewJSON
records. We build a deterministic hierarchy from scene to zone, region, object,
and supporting view. At query time we parse the target, attributes, intent, and
optional spatial anchor. Graph search keeps likely branches and prunes the rest.
The flat baseline uses exactly the same records, labels, queries, and scorer, so
the controlled difference is candidate selection. The result preserves the
selected object and view, traversal path, geometry when available, runtime, and
context or token counts."

### Show

- Return to the local site.
- Click `Method` in the navigation.
- Show the full workflow figure.
- Scroll slightly to the hierarchy and controlled evaluation figures.
- Click the workflow image once to demonstrate the full-size viewer, then close
  it.

## 2:10-2:55 - Datasets And Ground Truth

### Say

"We kept five team-captured scenes as the digital-twin system track: 97 views and
1,066 semantic items. We then added the same eight Replica and eight ScanNet
scenes used by the closest related BBQ work. Replica provides 575 official
boxes and 56 queries. ScanNet provides 392 official boxes and 48 selected Nr3D
and Sr3D-plus queries. Licensed raw scenes are not redistributed; the project
publishes scene IDs, manifests, access links, code, and derived metrics."

### Show

- Click `Datasets` on the local site.
- Show the three dataset rows/cards: internal captures, ScanNet, and Replica.
- Point to the counts and the official-access links.

## 2:55-3:55 - Main Graph-Versus-Flat Result

### Say

"Our central experiment contains 150 same-input queries. Graph search checks
4.77 views per query instead of 19.4, a reduction of 75.5 percent. Estimated
context falls from 3,168 to 1,014 tokens per query, a reduction of 68.2 percent.
On the 125 queries with verified expected views, graph hit at one is 0.680 versus
0.768 for flat search, and hit at three is 0.808 versus 0.928. So our honest
conclusion is a strong context reduction with a measurable quality trade-off,
not universal superiority."

### Show

- Click `Results` and keep the `Internal` tab selected.
- Point to graph versus flat views and token values.
- Show the internal chart.
- Open `data/internal-metrics.json` only if the transition is smooth; otherwise
  point to the `Inspect the frozen metrics JSON` link without opening it.

## 3:55-4:45 - Replica And ScanNet Results

### Say

"The public pilots evaluate retrieval over official semantic maps. On Replica,
graph and flat lexical both reach the oracle-candidate ceiling, while graph
checks 12.1 objects instead of 71.9. On ScanNet, graph and flat lexical both
reach Acc at 0.25 of 0.271, while graph checks 11.2 objects instead of 49. The
no-relation ablation reaches 0.292, showing that relation confidence is one of
the next algorithmic improvements. These are object-retrieval results, not
automatic segmentation accuracy."

### Show

- Select the `Public datasets` result tab.
- Show the ScanNet and Replica figures.
- Point to the explicit oracle-map warning.

## 4:45-5:30 - ConceptGraphs And LangSplat

### Say

"We also completed native external executions. ConceptGraphs builds predicted
object maps on all eight ScanNet and all eight Replica scenes. LangSplat
completes its full native pipeline on one ScanNet scene under a hardware-adapted
3,000-iteration, 6-gigabyte profile. We measured runtime, local tokenizer usage,
and compatible quality fields. Because their map construction, geometry, and
resource protocols differ from ours, we report them as diagnostic executions,
not as a fair leaderboard."

### Show

- Select the `External baselines` result tab.
- Show all three rows in the baseline table.
- Point to the comparison-boundary column.

## 5:30-6:20 - Repository And Reproducibility

### Say

"The repository contains the backend query implementation, dataset adapters,
evaluation scripts, schemas, frozen outputs, figures, paper source, and release
documentation. Construction is measured separately: 97 annotation records,
1,066 items, a 179,817-token-equivalent tree representation, and 1.822 seconds
for the sum of scene median rebuilds. The current suite has 145 passing tests,
and automated checks keep the paper and website synchronized with frozen JSON."

### Show

- Open the repository in GitHub or the local folder.
- Show these paths in order:
  - `backend/query/`
  - `scripts/evaluate_grounding.py`
  - `outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/`
  - `outputs/public_datasets/`
  - `outputs/baselines/`
  - `papers/beyond-proximity/`
- In the terminal run, or show the completed output of:

```powershell
python -B -m pytest -q tests -p no:cacheprovider
```

## 6:20-7:00 - Academic Paper

### Say

"The final academic manuscript is titled SemanticSplat: Graph-Pruned Semantic
Search. It contains the expanded method, the hierarchy and evaluation contract,
all main metrics, public dataset results, baseline boundaries, qualitative
failure cases, limitations, and reproducibility commands. The named-author
version is intended as the public academic or arXiv-style manuscript, separate
from the anonymous workshop source."

### Show

- Open `papers/beyond-proximity/main.pdf`.
- Show page 1 with the title and authors.
- Jump to the method workflow figure.
- Jump to pages 6-8 to show the result tables, Figures 6-9, and limitations.

## 7:00-7:20 - Public Release And Closing

### Say

"Finally, the public GitHub Pages site brings the method, datasets, exact
metrics, code, and paper together while respecting dataset licenses. Our final
result is not only a demo: it is a test-backed research artifact with explicit
claim boundaries. The next step is calibrated pruning and predicted-map
evaluation under a shared protocol, so that we can recover quality while
keeping most of the context savings."

### Show

- Open `https://leopython2006.github.io/beyond-proximity-public/`.
- Scroll once from the hero to the paper/reproducibility area.
- End on the paper download and GitHub links.

## Short Backup Ending

Use this if you are close to the eight-minute limit:

"SemanticSplat now combines a working system, controlled metrics, official
public-dataset pilots, native baseline evidence, an academic paper, and a public
release. The result is substantial context reduction with clearly measured
quality limits and a concrete path to the next research version."
