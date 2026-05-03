FROM nvidia/cuda:12.6.1-runtime-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV HF_HUB_ENABLE_HF_TRANSFER=1

RUN apt-get update -y && apt-get install -y \
    python3 python3-pip python3-venv git curl wget \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/vllm-env
RUN /opt/vllm-env/bin/pip install --upgrade pip --quiet && \
    /opt/vllm-env/bin/pip install vllm huggingface_hub hf_transfer --quiet

RUN mkdir -p /models && \
    /opt/vllm-env/bin/hf download \
        Qwen/Qwen2.5-Coder-3B-Instruct \
        --local-dir /models/qwen2.5-coder-3b

EXPOSE 3333

CMD ["/opt/vllm-env/bin/python", "-m", "vllm.entrypoints.openai.api_server", \
     "--model",              "/models/qwen2.5-coder-3b", \
     "--host",               "::", \
     "--port",               "3333", \
     "--served-model-name",  "qwen2.5-coder-3b", \
     "--max-model-len",      "8192", \
     "--gpu-memory-utilization", "0.40", \
     "--enable-prefix-caching"]
