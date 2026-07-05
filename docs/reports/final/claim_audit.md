# Claim Audit - `papers/beyond-proximity/main.tex` vs Repository Evidence

Status date: 2026-07-05 (post research-upgrade rerun). Owner: Person 4 (Telman), updated by Codex.

## Integration Branch

`week4/integration-article-sprint` merged the four team branches. The current
research-upgrade work continues from that branch on
`codex/research-upgrade-baselines-datasets`.

## Primary Evidence

Source:

```text
outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/metrics_summary.json
```

Current reproducible five-scene run:

| Metric | Flat | Graph | Notes |
|---|---:|---:|---|
| Views checked, average | 19.4 | 4.77 | 75.5% savings |
| Input tokens, average | 3168.2 | 1014.3 | 68.2% savings |
| hit@1 | 0.768 | 0.680 | n=125 verified-view queries |
| hit@3 | 0.928 | 0.808 | n=125 verified-view queries |
| Queries total | 150 | 150 | 25 excluded from quality denominator |

Mode: **stub lexical**, not live VLM.

Dataset count in current repo:

```text
5 captured pilot scenes
97 captured pilot ViewJSON annotations
1,066 semantic items
```

The legacy `default` scene is separate demo evidence and is not included in the
five-scene averages.

## Claim Status

| Claim | Verdict | Evidence |
|---|---|---|
| Graph reduces views/tokens on five captured scenes | DONE | `five_scene_graph_vs_flat_v2` |
| Graph preserves or improves hit@k | NOT_DONE | Current rerun has lower graph hit@1 and hit@3 than flat |
| Graph exposes a cost/quality trade-off | DONE | Table in `main.tex`, ablations in `outputs/graph_vs_flat/ablations_v1/` |
| Same-input protocol | DONE | Same scenes, semantic items, query strings |
| ConceptGraphs superiority | NOT_DONE | Smoke only |
| LangSplat superiority | NOT_DONE | Official sofa smoke only |
| Live VLM evaluation | OUT_OF_SCOPE | No successful live outputs in current scope |
| Replica official evaluation | NOT_DONE | `docs/datasets/public_dataset_readiness.md` |
| ScanNet evaluation | NOT_DONE | No local ScanNet scene and converter still skeletal |
| 3D IoU / metric localization | NOT_DONE | No independent GT boxes/masks |

## Artifact Checklist

- [x] `papers/beyond-proximity/main.tex` uses current 97-view numbers.
- [x] `papers/beyond-proximity/main.pdf` rebuilt from current source.
- [x] Paper figures regenerated from `five_scene_graph_vs_flat_v2`.
- [x] LangSplat smoke rerun: `outputs/baselines/langsplat_smoke_v1/`.
- [x] ConceptGraphs smoke rerun: `outputs/baselines/conceptgraphs_smoke_v1/`.
- [x] Ablation outputs: `outputs/graph_vs_flat/ablations_v1/`.
- [x] Scaling stress outputs: `outputs/graph_vs_flat/scaling_stress_v1/`.
- [x] Public dataset readiness audit: `docs/datasets/public_dataset_readiness.md`.
- [ ] Official Replica scene imported and evaluated.
- [ ] ScanNet scene imported and evaluated.
- [ ] Fair same-scene baseline comparison.

## Reviewer FAQ

**Q: Can we call ViewJSON labels "ground truth"?**
A: Use "reference labels" or "verified view labels"; they are not independent
annotator GT.

**Q: Does the current graph preserve quality?**
A: No. The current reproducible lexical run is a strong cost-reduction result
with lower hit@k than flat search. The paper should frame this as a cost/quality
trade-off and motivate calibrated pruning.

**Q: Do LangSplat and ConceptGraphs prove our method is faster or better?**
A: No. They prove local smoke execution and canonical adapter compatibility.
They do not provide five-scene accuracy or efficiency comparison.

**Q: Are Replica or ScanNet done?**
A: No. The local Replica-style pilot is a project proxy, not an official Replica
scene. ScanNet is absent locally.
