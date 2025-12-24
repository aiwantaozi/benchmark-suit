# common

export HF_HOME=/workspace/gpustack_cache
pip install "huggingface_hub[hf_xet]"
hf download deepseek-ai/DeepSeek-V3.2


git clone https://github.com/aiwantaozi/benchmark-suit/
cd benchmark-suit/
git checkout test

# vllm

1.
./setup_envs.sh vllm
eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
conda activate vllm
./install_deepgemm.sh

eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
conda activate vllm
pip install uv
./setup_ep_env.sh

2.
git clone https://github.com/vllm-project/vllm
cd ./tools/ep_kernels/elastic_ep
./install_eep_libraries.sh 希望跑pplx的，安装失败，没有权限，在容器环境无法测试

3.
export HF_HOME=/workspace/gpustack_cache
python bench_serving.py --config ./config_deepseek_v3.2_vllm.yaml --output-dir ./test/deepseek_v3.2-results-1224

# sglang

1.
./setup_envs.sh vllm

2. 
CONDA_BASE=$(conda info --base)
source "$CONDA_BASE/etc/profile.d/conda.sh"
conda activate sglang

3.
python3 -m sglang.compile_deep_gemm --model deepseek-ai/DeepSeek-V3.2 --tp 8 --trust-remote-code

4.
python bench_serving.py --config ./config_deepseek_v3.2-1220.yaml --output-dir ./test/deepseek_v3.2-results-1220 --run-names sglang-official-recommended-tp-dp