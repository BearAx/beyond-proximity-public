# Beyond Proximity Project Site

This directory contains the static GitHub Pages source. Repository artifacts
are copied into a clean deployment directory by:

```powershell
python -B scripts\build_project_site.py
python -m http.server 4173 --directory site-dist
```

Open `http://localhost:4173`. The GitHub Pages workflow runs the same build and
publishes `site-dist/`.

The builder intentionally excludes licensed ScanNet/Replica images and raw
scene data. It publishes exact scene IDs, official access links, team-owned
captures, derived figures, curated metric summaries, and the named-author
academic preprint PDF. Values rendered in the page are refreshed from
`data/evidence-summary.json`, which the builder derives from frozen experiment
outputs.
