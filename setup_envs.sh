#!/bin/bash
# Robust script to install Miniconda (if not installed) and set up conda environments
# Environments:
#   1. vllm -> installs vllm + flashinfer-python + hf_transfer
#   2. sglang -> installs sglang[all]
#   3. trtllm -> installs tensorrt_llm

set -e  # Exit immediately if a command exits with a non-zero status

# ===== 1. Check and install Miniconda =====
if command -v conda &> /dev/null; then
    echo "✅ Conda already installed. Skipping installation."
else
    echo "📥 Downloading Miniconda..."
    wget -O Miniconda3-latest-Linux-x86_64.sh \
        https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

    echo "📦 Installing Miniconda..."
    bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
    rm Miniconda3-latest-Linux-x86_64.sh

    echo "⚙️ Initializing Conda..."
    eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
    conda init bash

    # Accept Anaconda Terms of Service (needed for non-interactive scripts)
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main || true
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r || true
fi

# Ensure conda is available in this shell
eval "$(conda shell.bash hook)"

# Ensure dependencies
sudo apt-get update && apt-get -y install libopenmpi-dev numactl

# ===== 2. Create and configure environments =====
create_env_if_not_exists () {
    ENV_NAME=$1
    PY_VER=$2
    PKGS=$3

    if conda info --envs | grep -qE "^${ENV_NAME}\s"; then
        echo "✅ Environment '$ENV_NAME' already exists. Skipping creation."
    else
        echo "🌱 Creating environment '$ENV_NAME'..."
        conda create -n $ENV_NAME -y python=$PY_VER
        conda activate $ENV_NAME
        echo "📦 Installing packages: $PKGS"
        pip install $PKGS
        conda deactivate
    fi
}

# vllm env
create_env_if_not_exists "vllm" "3.12" "vllm[bench] flashinfer-python hf_transfer"

# sglang env
create_env_if_not_exists "sglang" "3.12" "sglang[all]"

# trtllm env
create_env_if_not_exists "trtllm" "3.12" "tensorrt_llm"

echo "🎉 All environments are ready!"
echo "👉 Use: conda activate vllm | sglang | trtllm"
