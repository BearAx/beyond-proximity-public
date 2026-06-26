# ConceptGraphs Status

Status date: 2026-06-26. Status: `PARTIAL`.

## Evidence

| Check | Status | Evidence |
|---|---|---|
| In-repo checkout | missing | `external/baselines/concept-graphs/` does not exist |
| External checkout | present but not trusted in this sandbox | `C:/GitProjects/baseline-deps/concept-graphs` exists; `git rev-parse` is blocked by Git `safe.directory` ownership protection |
| Conda env | missing | `conda env list` shows `base`, `pcg`, `semanticsplat`; no `conceptgraph` env |
| Docker runtime | available for LangSplat, not verified for ConceptGraphs | Docker Desktop was available during the LangSplat smoke; no ConceptGraphs container/image has been built or run |
| Checkpoints/assets | partial | `C:/GitProjects/baseline-deps/model-cache/yolov8l-world.pt` and `mobile_sam.pt` exist |
| Official smoke entrypoint | partially known | `docs/baselines/conceptgraphs/conceptgraphs_smoke_setup.md` and `scripts/run_conceptgraphs_smoke.ps1` |
| Native output | missing | `outputs/baselines/conceptgraphs_smoke_v1/native_results.json` does not exist |
| Canonical adapter | present | `scripts/adapt_conceptgraphs_output.py` |
| Adapter tests | present | `tests/backend/test_baseline_adapters.py` |

## Exact Missing Item

ConceptGraphs is not run yet because there is no verified executable environment in the current repo context and no native smoke output. The ConceptGraphs checkout is outside the project, Git revision evidence is blocked by ownership checks, the `conceptgraph` Conda environment is missing, and no `native_results.json` exists for the adapter.

## Next Command

After the external checkout is intentionally trusted by the user/team and the ConceptGraphs environment is created, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_conceptgraphs_smoke.ps1
```

If native output is produced, adapt it with:

```powershell
python -B scripts\adapt_conceptgraphs_output.py `
  --native outputs\baselines\conceptgraphs_smoke_v1\native_results.json `
  --benchmark docs\benchmarks\benchmark_queries_v1.json `
  --scene-id ConferenceHall-capture-pilot `
  --benchmark-scene-id ConferenceHall `
  --mode live `
  --out outputs\week3\baselines\conceptgraphs
```

Do not mark this baseline as executed until native logs and at least one canonical query result exist.
