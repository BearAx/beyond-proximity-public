# ConceptGraphs Smoke Result

Status date: 2026-06-23. Result: blocked before baseline execution.

Commands attempted:

```powershell
conda run -n conceptgraph python slam/cfslam_pipeline_batch.py --help
python -B slam\cfslam_pipeline_batch.py --help

python -B scripts\adapt_conceptgraphs_output.py --native outputs\baselines\conceptgraphs_smoke_v1\native_results.json --benchmark docs\benchmarks\benchmark_queries_v1.json --scene-id ConferenceHall-capture-pilot --benchmark-scene-id ConferenceHall --mode live --out outputs\baselines\conceptgraphs_smoke_v1
```

Errors:

```text
EnvironmentLocationNotFound: Not a conda environment: C:\Users\bear_\miniconda3\envs\conceptgraph

can't open file 'C:\GitProjects\beyond-proximity\slam\cfslam_pipeline_batch.py': [Errno 2] No such file or directory

ConceptGraphs adapter blocked: Missing native input: outputs\baselines\conceptgraphs_smoke_v1\native_results.json
```

Outcome:

```text
baseline process executed = false
native outputs = 0
canonical query results = 0
output directory created = false
measured baseline latency = N/A
baseline accuracy = N/A
```

The next action is to create a separate pinned ConceptGraphs checkout/environment, acquire required checkpoints, and implement a documented captured-scene-to-native data adapter. No result was fabricated.
