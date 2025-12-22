
1. image
nvcr.io/nvidia/tensorrt-llm/release:1.2.0rc5
sleep infinity

1. 
export HF_HOME=/workspace/trtllm_cache/huggingface
hf download deepseek-ai/DeepSeek-V3.2


1. 
git clone https://github.com/aiwantaozi/benchmark-suit
cd benchmark-suit/
git checkout test

2. 
./setup_envs.sh vllm

git config --global credential.helper store
git config --global user.email "xxx"
git config --global user.name "xxx"

3.
python bench_serving.py --config ./config_qwen3_0.6b-1221.yaml --output-dir ./test/qwen3_0.6b-results-1221 
python bench_serving.py --config ./config_deepseek_v3.2-1221.yaml --output-dir ./test/deepseek_v3.2-results-1221 