# LangSplat Smoke Result

Status date: 2026-06-23. Result: blocked before baseline execution.

Commands attempted:

```powershell
conda run -n langsplat python render.py --help
python -B render.py --help

python -B scripts\adapt_langsplat_output.py --native outputs\baselines\langsplat_smoke_v1\native_results.json --benchmark docs\benchmarks\benchmark_queries_v1.json --scene-id ConferenceHall-capture-pilot --benchmark-scene-id ConferenceHall --mode live --out outputs\baselines\langsplat_smoke_v1
```

Errors:

```text
EnvironmentLocationNotFound: Not a conda environment: C:\Users\bear_\miniconda3\envs\langsplat

can't open file 'C:\GitProjects\beyond-proximity\render.py': [Errno 2] No such file or directory

LangSplat adapter blocked: Missing native input: outputs\baselines\langsplat_smoke_v1\native_results.json
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

The next action is to create a separate pinned LangSplat checkout/environment and obtain a compatible pretrained 3DGS/language-feature package before attempting adaptation. No result was fabricated.
