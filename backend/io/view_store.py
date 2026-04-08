"""Save / load ViewJSON analysis files for a scene."""
import json
from pathlib import Path
from typing import List, Optional

from backend.schemas.types import ViewJSON


def _views_dir(scene_dir: str) -> Path:
    return Path(scene_dir) / "views"


def save_view_analysis(scene_dir: str, view_id: str, view_json: ViewJSON) -> None:
    d = _views_dir(scene_dir)
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{view_id}.json"
    with open(path, "w") as fh:
        json.dump(view_json.model_dump(), fh, indent=2)


def load_view_analysis(scene_dir: str, view_id: str) -> Optional[ViewJSON]:
    path = _views_dir(scene_dir) / f"{view_id}.json"
    if not path.exists():
        return None
    with open(path) as fh:
        return ViewJSON.model_validate(json.load(fh))


def view_analysis_exists(scene_dir: str, view_id: str) -> bool:
    return (_views_dir(scene_dir) / f"{view_id}.json").exists()


def list_view_ids(scene_dir: str) -> List[str]:
    d = _views_dir(scene_dir)
    if not d.exists():
        return []
    return sorted(p.stem for p in d.glob("*.json"))


def list_view_summaries(scene_dir: str) -> List[dict]:
    """Return a summary record for every analyzed view.

    Includes the new semantic-boundary fields (facing, visible_landmarks)
    required by the semantic merge pass in spatial_graph.py.
    """
    result = []
    for vid in list_view_ids(scene_dir):
        v = load_view_analysis(scene_dir, vid)
        if v:
            result.append({
                "view_id": vid,
                "summary": v.scene_summary,
                "object_count": len(v.objects),
                "room_type": v.room_type,
                "facing": v.facing,
                "visible_landmarks": v.visible_landmarks,
            })
    return result
