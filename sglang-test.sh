#!/bin/bash

./setup_envs.sh sglang

CONDA_BASE=$(conda info --base)
source "$CONDA_BASE/etc/profile.d/conda.sh"
conda activate sglang

# warmup
python3 -m sglang.compile_deep_gemm --model deepseek-ai/DeepSeek-V3.2 --tp 8 --trust-remote-code

# run
python bench_serving.py --config ./config_deepseek_v3.2-1220.yaml --output-dir ./test/deepseek_v3.2-results-1220 --run-names sglang-official-recommended-tp-dp