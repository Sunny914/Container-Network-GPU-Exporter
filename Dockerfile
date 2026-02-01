FROM nvidia/cuda:12.3.0-runtime-ubuntu22.04

# ---- system deps ----
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    docker.io \
    iproute2 \
    util-linux \
    procps \
    && rm -rf /var/lib/apt/lists/*

# ---- python deps ----
WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# ---- app code ----
COPY . .

# ---- default exporter (network) ----
ENV EXPORTER_MODE=network

# ---- entrypoint wrapper ----
ENTRYPOINT ["bash", "-c"]
CMD ["if [ \"$EXPORTER_MODE\" = \"gpu\" ]; then python3 -m exporter.gpu_exporter; else python3 -m exporter.network_exporter; fi"]




















