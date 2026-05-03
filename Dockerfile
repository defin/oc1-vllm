FROM vllm/vllm-openai:latest

# Download model at build time
RUN pip install hf_transfer huggingface_hub --quiet
RUN mkdir -p /models && \
    HF_HUB_ENABLE_HF_TRANSFER=1 hf download \
        Qwen/Qwen2.5-Coder-3B-Instruct \
        --local-dir /models/qwen2.5-coder-3b

EXPOSE 3333

ENTRYPOINT []
CMD ["python", "-m", "vllm.entrypoints.openai.api_server", \
     "--model",              "/models/qwen2.5-coder-3b", \
     "--host",               "::", \
     "--port",               "3333", \
     "--served-model-name",  "qwen2.5-coder-3b", \
     "--max-model-len",      "8192", \
     "--gpu-memory-utilization", "0.40", \
     "--enable-prefix-caching"]
