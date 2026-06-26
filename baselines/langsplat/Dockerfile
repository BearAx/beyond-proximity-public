FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-devel

ARG LANGSPLAT_REV=d70edb86df0fcbda19dc0d9739a3e5140a5e65fc

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TORCH_CUDA_ARCH_LIST=8.6 \
    TORCH_HOME=/models/torch \
    HF_HOME=/models/huggingface

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential git libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip "setuptools<81" wheel ninja && \
    python -m pip install \
        "numpy<2" \
        jaxtyping matplotlib open-clip-torch==2.20.0 \
        opencv-python-headless pillow plyfile==0.8.1 tensorboard tqdm

RUN git clone https://github.com/minghanqin/LangSplat.git /opt/langsplat && \
    cd /opt/langsplat && \
    git checkout "${LANGSPLAT_REV}" && \
    git submodule update --init --recursive && \
    python -m pip install --no-build-isolation ./submodules/langsplat-rasterization ./submodules/simple-knn

WORKDIR /opt/langsplat
