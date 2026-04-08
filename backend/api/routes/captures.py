"""API routes: view capture from browser R-press."""
import base64
import struct
from pathlib import Path

import numpy as np
from fastapi import APIRouter, HTTPException

from backend.config import DATA_DIR
from backend.io.nerfstudio import FrameEntry, get_or_create_transforms, save_transforms
from backend.schemas.types import CapturePayload

router = APIRouter()


@router.post("/save")
def save_capture(payload: CapturePayload):
    scene_dir = DATA_DIR / payload.scene_id
    if not scene_dir.exists():
        raise HTTPException(status_code=404, detail=f"Scene '{payload.scene_id}' not found")

    # ── Save RGB image ────────────────────────────────────────────────────────
    images_dir = scene_dir / "images"
    images_dir.mkdir(exist_ok=True)
    img_filename = f"{payload.view_id}.png"
    img_path = images_dir / img_filename
    img_bytes = base64.b64decode(
        payload.rgb_b64.split(",", 1)[-1]  # strip "data:image/png;base64," prefix
    )
    with open(img_path, "wb") as fh:
        fh.write(img_bytes)

    # ── Save depth map ────────────────────────────────────────────────────────
    depths_dir = scene_dir / "depths"
    depths_dir.mkdir(exist_ok=True)
    depth_filename = f"{payload.view_id}_depth.npy"
    depth_path = depths_dir / depth_filename
    depth_raw = base64.b64decode(payload.depth_b64)
    n_floats = len(depth_raw) // 4
    depth_arr = np.array(struct.unpack(f"<{n_floats}f", depth_raw), dtype=np.float32)
    expected = payload.width * payload.height
    if len(depth_arr) != expected:
        raise HTTPException(
            status_code=400,
            detail=f"Depth size mismatch: got {len(depth_arr)}, expected {expected}",
        )
    depth_arr = depth_arr.reshape(payload.height, payload.width)
    np.save(str(depth_path), depth_arr)

    # ── Update transforms.json ───────────────────────────────────────────────
    tf_path = str(scene_dir / "transforms.json")
    ns_scene = get_or_create_transforms(
        tf_path,
        fl_x=payload.fl_x,
        fl_y=payload.fl_y,
        cx=payload.cx,
        cy=payload.cy,
        w=payload.width,
        h=payload.height,
    )
    # Remove existing frame with same view_id (re-capture)
    ns_scene.frames = [f for f in ns_scene.frames if f.view_id != payload.view_id]
    ns_scene.add_frame(FrameEntry(
        file_path=f"images/{img_filename}",
        transform_matrix=payload.transform_matrix,
        view_id=payload.view_id,
        depth_file_path=f"depths/{depth_filename}",
    ))
    save_transforms(ns_scene, tf_path)

    return {
        "status": "saved",
        "view_id": payload.view_id,
        "image_path": str(img_path),
        "depth_path": str(depth_path),
        "total_frames": len(ns_scene.frames),
    }
