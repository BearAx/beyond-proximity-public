FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

ARG CONCEPTGRAPHS_REV=72f5962822b5e8678a446f367a06df1a977d2a4d

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TORCH_HOME=/models/torch \
    HF_HOME=/models/huggingface

RUN apt-get update && apt-get install -y --no-install-recommends \
        git libgl1 libglib2.0-0 libgomp1 libsm6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install \
        "numpy<2" \
        hydra-core==1.3.2 \
        imageio==2.31.1 \
        line-profiler==4.1.2 \
        natsort==8.4.0 \
        open-clip-torch==2.20.0 \
        open3d==0.18.0 \
        opencv-python-headless==4.8.1.78 \
        PyQt5==5.15.10 \
        rerun-sdk==0.15.1 \
        scipy==1.10.1 \
        supervision==0.14.0 \
        ultralytics==8.1.0 \
        wandb==0.15.11 \
        distinctipy dill faiss-cpu h5py kornia openai pillow pypng scikit-learn tyro && \
    python -m pip install \
        git+https://github.com/facebookresearch/segment-anything.git \
        git+https://github.com/ultralytics/CLIP.git

# The current public YOLO-World checkpoint serializes WorldModel, added after 8.1.0.
RUN python -m pip install --no-deps ultralytics==8.2.0

RUN git clone https://github.com/concept-graphs/concept-graphs.git /opt/conceptgraphs && \
    cd /opt/conceptgraphs && \
    git checkout "${CONCEPTGRAPHS_REV}" && \
    sed -i \
        -e 's/ColorPalette\.DEFAULT/ColorPalette.default()/g' \
        -e 's/Color\.BLACK/Color.black()/g' \
        conceptgraph/utils/vis.py && \
    python -m pip install -e .

WORKDIR /opt/conceptgraphs/conceptgraph
