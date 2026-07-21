# Standard library imports
import cv2
import gzip
import os
import pickle
from pathlib import Path

import hydra
import numpy as np
import open_clip
from line_profiler import profile
from omegaconf import DictConfig
import supervision as sv
import torch
from tqdm import trange
from ultralytics import SAM, YOLO

from conceptgraph.dataset.datasets_common import get_dataset
from conceptgraph.utils.general_utils import (
    ObjectClasses,
    get_det_out_path,
    get_exp_out_path,
    get_vis_out_path,
    measure_time,
    save_hydra_config,
)
from conceptgraph.utils.model_utils import compute_clip_features_batched
from conceptgraph.utils.vis import save_video_detections, vis_result_fast


@hydra.main(version_base=None, config_path="../hydra_configs/", config_name="streamlined_detections")
@profile
def main(cfg: DictConfig):
    dataset = get_dataset(
        dataconfig=cfg.dataset_config,
        start=cfg.start,
        end=cfg.end,
        stride=cfg.stride,
        basedir=cfg.dataset_root,
        sequence=cfg.scene_id,
        desired_height=cfg.desired_height,
        desired_width=cfg.desired_width,
        device="cpu",
        dtype=torch.float,
        # Keep public-dataset map boxes in the official world frame so they can
        # be compared with the dataset's GT boxes.
        relative_pose=False,
    )

    det_exp_path = get_exp_out_path(cfg.dataset_root, cfg.scene_id, cfg.exp_suffix)
    det_exp_pkl_path = get_det_out_path(det_exp_path)
    det_exp_vis_path = get_vis_out_path(det_exp_path)

    detection_model = measure_time(YOLO)("yolov8l-world.pt")
    sam_predictor = SAM("mobile_sam.pt")
    clip_checkpoint = os.environ.get(
        "SEMANTICSPLAT_OPENCLIP_CHECKPOINT", "laion2b_s32b_b79k"
    )
    clip_model, _, clip_preprocess = open_clip.create_model_and_transforms(
        "ViT-H-14", clip_checkpoint
    )
    clip_model = clip_model.to(cfg.device)
    clip_tokenizer = open_clip.get_tokenizer("ViT-H-14")

    obj_classes = ObjectClasses(cfg.classes_file, bg_classes=cfg.bg_classes, skip_bg=cfg.skip_bg)
    detection_model.set_classes(obj_classes.get_classes_arr())

    save_hydra_config(cfg, det_exp_path)

    for frame_idx in trange(len(dataset)):
        color_path = Path(dataset.color_paths[frame_idx])
        image = cv2.imread(str(color_path))
        if image is None:
            raise FileNotFoundError(f"Could not read color image: {color_path}")
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = detection_model.predict(color_path, conf=0.1, verbose=False)
        confidences = results[0].boxes.conf.cpu().numpy()
        detection_class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
        xyxy_tensor = results[0].boxes.xyxy
        xyxy_np = xyxy_tensor.cpu().numpy()

        if xyxy_tensor.numel() != 0:
            sam_out = sam_predictor.predict(color_path, bboxes=xyxy_tensor, verbose=False)
            masks_np = sam_out[0].masks.data.cpu().numpy()
        else:
            masks_np = np.empty((0, image_rgb.shape[0], image_rgb.shape[1]), dtype=np.bool_)

        curr_det = sv.Detections(
            xyxy=xyxy_np,
            confidence=confidences,
            class_id=detection_class_ids,
            mask=masks_np,
        )

        if len(curr_det.xyxy) == 0:
            image_crops = []
            image_feats = np.empty((0, 0), dtype=np.float32)
            text_feats = []
        else:
            image_crops, image_feats, text_feats = compute_clip_features_batched(
                image_rgb,
                curr_det,
                clip_model,
                clip_preprocess,
                clip_tokenizer,
                obj_classes.get_classes_arr(),
                cfg.device,
            )

        detection = {
            "xyxy": curr_det.xyxy,
            "confidence": curr_det.confidence,
            "class_id": curr_det.class_id,
            "mask": curr_det.mask,
            "classes": obj_classes.get_classes_arr(),
            "image_crops": image_crops,
            "image_feats": image_feats,
            "text_feats": text_feats,
        }

        vis_save_path = (det_exp_vis_path / color_path.name).with_suffix(".jpg")
        try:
            annotated_image, _ = vis_result_fast(image, curr_det, obj_classes.get_classes_arr())
        except Exception:
            annotated_image = image
        cv2.imwrite(str(vis_save_path), annotated_image)

        curr_detection_name = vis_save_path.stem + ".pkl.gz"
        with gzip.open(det_exp_pkl_path / curr_detection_name, "wb") as handle:
            pickle.dump(detection, handle)

    if cfg.save_video:
        save_video_detections(det_exp_path)


if __name__ == "__main__":
    measure_time(main)()
