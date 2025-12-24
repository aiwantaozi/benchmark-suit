
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

python bench_serving.py --config ./config_deepseek_v3.2-1221.yaml --output-dir ./test/deepseek_v3.2-results-1221 --run-names trt-deepgemm-disabled,trt-mtp

python quickstart_advanced.py --model_dir /workspace/trtllm_cache/huggingface/hub/models--deepseek-ai--DeepSeek-V3.2/snapshots/a7e62ac04ecb2c0a54d736dc46601c5606cf10a6/ --host localhost --port 8000 --tp_size 8 --ep_size 8 --pp_size 1 --spec_decode_algo MTP --spec_decode_max_draft_len 2


python quickstart_advanced.py --model_dir /workspace/trtllm_cache/huggingface/hub/models--deepseek-ai--DeepSeek-V3.2/snapshots/a7e62ac04ecb2c0a54d736dc46601c5606cf10a6/ --tp_size 8 --pp_size 1 --spec_decode_algo MTP --spec_decode_max_draft_len 2

## convert results

python convert_benchmark_results.py \
  ./test/deepseek_v3.2-results-1221/trt_baseline_sharegpt.json \
  ./test/deepseek_v3.2-results-1221/trt_deepgemm_disabled_sharegpt.json \
  -o ./test/deepseek_v3.2-results-1221/converted_results