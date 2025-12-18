#!/bin/bash
# Robust script to install Miniconda (if not installed) and set up conda environments
# Environments:
#   1. vllm -> installs vllm + flashinfer-python + hf_transfer
#   2. sglang -> installs sglang[all]
#   3. trtllm -> installs tensorrt_llm

set -e  # Exit immediately if a command exits with a non-zero status

# ===== 1. Check and install Miniconda =====
install_cuda(){
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
}


# Ensure dependencies
install_dependencies(){
    echo "🔧 Installing system dependencies..."
    sudo apt-get update && apt-get -y install libopenmpi-dev numactl
}

# ===== 2. Create and configure environments =====
create_env_if_not_exists () {
    ENV_NAME=$1
    PY_VER=$2
    PKGS=$3

    if conda info --envs | grep -qE "^${ENV_NAME}\s"; then
        echo "✅ Environment '$ENV_NAME' already exists. Skipping creation."
    else
        conda init
        echo "🌱 Creating environment '$ENV_NAME'..."
        conda create -n $ENV_NAME -y python=$PY_VER

        CONDA_BASE=$(conda info --base)
        source "$CONDA_BASE/etc/profile.d/conda.sh"

        conda activate $ENV_NAME
        echo "📦 Installing packages: $PKGS"
        pip install $PKGS

        echo "🧩 Ensuring modern libstdc++ runtime..."
        conda install -c conda-forge -y libstdcxx-ng>=12

        conda deactivate
    fi
}

install_vllm() {
  echo "🚀 Installing vllm env..."
  create_env_if_not_exists "vllm" "3.12" \
    "vllm[bench] flashinfer-python hf_transfer"
}

install_sglang() {
  echo "🚀 Installing sglang env..."
  create_env_if_not_exists "sglang" "3.12" \
    "sglang[all]"
}

install_trtllm() {
  echo "🚀 Installing trtllm env..."
  create_env_if_not_exists "trtllm" "3.12" \
    "tensorrt_llm"
}

install_deepgemm() {
    echo "TODO"
    # https://github.com/sgl-project/sglang/issues/9710
    # https://blog.csdn.net/gitblog_00617/article/details/151436824
}

usage() {
  cat <<EOF
Usage:
  $0 [vllm] [sglang] [trtllm]

Examples:
  $0 vllm sglang     # install vllm and sglang only
  $0 trtllm          # install trtllm only
  $0                 # install all envs
EOF
}

ALL_ENVS=("vllm" "sglang" "trtllm")

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

# If no args provided, install all
if [[ "$#" -eq 0 ]]; then
  TARGET_ENVS=("${ALL_ENVS[@]}")
else
  TARGET_ENVS=("$@")
fi

# Dispatch
for env in "${TARGET_ENVS[@]}"; do
  case "$env" in
    vllm)
      install_vllm
      ;;
    sglang)
      install_sglang
      ;;
    trtllm)
      install_trtllm
      ;;
    *)
      echo "❌ Unknown env: $env"
      usage
      exit 1
      ;;
  esac
done

echo "🎉 All requested environments are ready!"
echo "👉 Use: conda activate vllm | sglang | trtllm"
