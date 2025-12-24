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
./install_deepgemm.sh

eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
conda activate vllm
pip install uv
./setup_ep_env.sh

2.
git clone https://github.com/vllm-project/vllm
cd ./tools/ep_kernels/elastic_ep
./install_eep_libraries.sh

3.
export HF_HOME=/workspace/gpustack_cache
python bench_serving.py --config ./config_deepseek_v3.2_vllm.yaml --output-dir ./test/deepseek_v3.2-results-1224