FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    wget curl git sudo bzip2 \
    libopenmpi-dev numactl \
    && rm -rf /var/lib/apt/lists/*

COPY setup_envs.sh /opt/setup_envs.sh
RUN chmod +x /opt/setup_envs.sh

RUN /opt/setup_envs.sh

WORKDIR /workspace

RUN wget https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/resolve/main/ShareGPT_V3_unfiltered_cleaned_split.json

CMD ["/bin/bash"]
