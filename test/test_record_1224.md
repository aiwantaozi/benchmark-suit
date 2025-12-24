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

(vllm) root@25525aa48170:/workspace/benchmark-suit# python bench_serving.py --config ./config_deepseek_v3.2_vllm.yaml --output-dir ./test/deepseek_v3.2-results-1224
2025-12-24 10:28:07,669 - llm_benchmark - INFO - Starting test for vllm-tp-tokenizer-reason
2025-12-24 10:28:07,669 - llm_benchmark - INFO - Set env HF_HOME=/workspace/gpustack_cache
2025-12-24 10:28:07,670 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 -tp 8 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3 --port 8000
2025-12-24 10:28:07,672 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds
2025-12-24 10:31:07,672 - llm_benchmark - INFO - Checking service readiness...
2025-12-24 10:48:57,800 - llm_benchmark - INFO - Service is ready
2025-12-24 10:48:57,805 - llm_benchmark - INFO - Running benchmark: sharegpt
2025-12-24 10:48:57,805 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 1000 --result-filename test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_sharegpt.json --save-result
2025-12-24 10:51:04,058 - llm_benchmark - INFO - Completed test case: sharegpt
2025-12-24 10:51:04,058 - llm_benchmark - INFO - Stopping current service...
2025-12-24 10:51:04,065 - llm_benchmark - INFO - Successfully stopped current service
2025-12-24 10:51:09,066 - llm_benchmark - INFO - Successfully completed test: vllm-tp-tokenizer-reason
2025-12-24 10:51:09,066 - llm_benchmark - INFO - Starting test for vllm-tp-tokenizer-reason-max-model-len
2025-12-24 10:51:09,066 - llm_benchmark - INFO - Set env HF_HOME=/workspace/gpustack_cache
2025-12-24 10:51:09,067 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 -tp 8 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3 --max-model-len 32768 --port 8000
2025-12-24 10:51:09,070 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds
2025-12-24 10:54:09,070 - llm_benchmark - INFO - Checking service readiness...
2025-12-24 11:06:59,179 - llm_benchmark - INFO - Service is ready
2025-12-24 11:06:59,179 - llm_benchmark - INFO - Running benchmark: sharegpt
2025-12-24 11:06:59,179 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 1000 --result-filename test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_max_model_len_sharegpt.json --save-result

2025-12-24 11:08:29,983 - llm_benchmark - INFO - Completed test case: sharegpt
2025-12-24 11:08:29,983 - llm_benchmark - INFO - Stopping current service...
2025-12-24 11:08:29,991 - llm_benchmark - INFO - Successfully stopped current service
2025-12-24 11:08:34,991 - llm_benchmark - INFO - Successfully completed test: vllm-tp-tokenizer-reason-max-model-len
2025-12-24 11:08:34,991 - llm_benchmark - INFO - Starting test for vllm-tool-call
2025-12-24 11:08:34,991 - llm_benchmark - INFO - Set env HF_HOME=/workspace/gpustack_cache
2025-12-24 11:08:34,991 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 -tp 8 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3 --tool-call-parser deepseek_v32 --enable-auto-tool-choice --port 8000
2025-12-24 11:08:34,995 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds
2025-12-24 11:11:34,995 - llm_benchmark - INFO - Checking service readiness...
2025-12-24 11:19:05,049 - llm_benchmark - INFO - Service is ready
2025-12-24 11:19:05,050 - llm_benchmark - INFO - Running benchmark: sharegpt
2025-12-24 11:19:05,050 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 1000 --result-filename test/deepseek_v3.2-results-1224/vllm_tool_call_sharegpt.json --save-result
2025-12-24 11:20:35,686 - llm_benchmark - INFO - Completed test case: sharegpt
2025-12-24 11:20:35,686 - llm_benchmark - INFO - Stopping current service...
2025-12-24 11:20:35,693 - llm_benchmark - INFO - Successfully stopped current service
2025-12-24 11:20:40,694 - llm_benchmark - INFO - Successfully completed test: vllm-tool-call
2025-12-24 11:20:40,694 - llm_benchmark - INFO - Starting test for vllm-speculative-decoding-mtp
2025-12-24 11:20:40,694 - llm_benchmark - INFO - Set env HF_HOME=/workspace/gpustack_cache
2025-12-24 11:20:40,694 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 -tp 8 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3 --speculative-config {"method":"mtp","num_speculative_tokens":1}
 --port 8000
2025-12-24 11:20:40,697 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds
2025-12-24 11:23:40,698 - llm_benchmark - INFO - Checking service readiness...
2025-12-24 11:26:30,726 - llm_benchmark - INFO - Service is ready
2025-12-24 11:26:30,726 - llm_benchmark - INFO - Running benchmark: sharegpt
2025-12-24 11:26:30,726 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 1000 --result-filename test/deepseek_v3.2-results-1224/vllm_speculative_decoding_mtp_sharegpt.json --save-result
2025-12-24 11:28:04,644 - llm_benchmark - INFO - Completed test case: sharegpt
2025-12-24 11:28:04,644 - llm_benchmark - INFO - Stopping current service...
2025-12-24 11:28:04,652 - llm_benchmark - INFO - Successfully stopped current service
2025-12-24 11:28:09,652 - llm_benchmark - INFO - Successfully completed test: vllm-speculative-decoding-mtp
2025-12-24 11:28:09,652 - llm_benchmark - INFO - Starting test for vllm-deepgemm-disable
2025-12-24 11:28:09,652 - llm_benchmark - INFO - Set env VLLM_USE_DEEP_GEMM=0
2025-12-24 11:28:09,652 - llm_benchmark - INFO - Set env HF_HOME=/workspace/gpustack_cache
2025-12-24 11:28:09,653 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 -tp 8 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3 --port 8000
2025-12-24 11:28:09,656 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds
2025-12-24 11:31:09,656 - llm_benchmark - INFO - Checking service readiness...
2025-12-24 11:31:39,664 - llm_benchmark - INFO - Service is ready
2025-12-24 11:31:39,665 - llm_benchmark - INFO - Running benchmark: sharegpt
2025-12-24 11:31:39,665 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 1000 --result-filename test/deepseek_v3.2-results-1224/vllm_deepgemm_disable_sharegpt.json --save-result
2025-12-24 11:33:10,286 - llm_benchmark - INFO - Completed test case: sharegpt
2025-12-24 11:33:10,286 - llm_benchmark - INFO - Stopping current service...
2025-12-24 11:33:10,293 - llm_benchmark - INFO - Successfully stopped current service
2025-12-24 11:33:15,294 - llm_benchmark - INFO - Successfully completed test: vllm-deepgemm-disable
2025-12-24 11:33:15,294 - llm_benchmark - INFO - Starting test for vllm-flashinfer
2025-12-24 11:33:15,294 - llm_benchmark - INFO - Set env VLLM_ATTENTION_BACKEND=FLASHINFER
2025-12-24 11:33:15,294 - llm_benchmark - INFO - Set env HF_HOME=/workspace/gpustack_cache
2025-12-24 11:33:15,295 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 -tp 8 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3 --port 8000
2025-12-24 11:33:15,298 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds
2025-12-24 11:36:15,298 - llm_benchmark - INFO - Checking service readiness...
2025-12-24 11:36:15,299 - llm_benchmark - ERROR - Service failed to start: None
2025-12-24 11:36:15,299 - llm_benchmark - ERROR - Error running test vllm-flashinfer: Service startup monitoring failed: Service process terminated unexpectedly
2025-12-24 11:36:15,299 - llm_benchmark - INFO - Stopping current service...
2025-12-24 11:36:15,299 - llm_benchmark - ERROR - Error stopping service: [Errno 3] No such process
2025-12-24 11:36:20,299 - llm_benchmark - ERROR - Failed to run test vllm-flashinfer: Service startup monitoring failed: Service process terminated unexpectedly
2025-12-24 11:36:20,299 - llm_benchmark - INFO - Starting test for vllm-xformers
2025-12-24 11:36:20,299 - llm_benchmark - INFO - Set env VLLM_ATTENTION_BACKEND=XFORMERS
2025-12-24 11:36:20,299 - llm_benchmark - INFO - Set env HF_HOME=/workspace/gpustack_cache
2025-12-24 11:36:20,304 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 -tp 8 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3 --port 8000
2025-12-24 11:36:20,307 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds
^C2025-12-24 11:37:24,166 - llm_benchmark - INFO - Stopping current service...
2025-12-24 11:37:24,166 - llm_benchmark - INFO - Successfully stopped current service


4. 
 python bench_serving.py --config ./config_deepseek_v3.2_vllm.yaml --output-dir ./test/deepseek_v3.2-results-1224 --run-names vllm-tp-tokenizer-reason,vllm-tp-tokenizer-reason-second,vllm-flashmla,vllm-cutlass-mla,vllm-triton-mla
2025-12-24 11:52:41,040 - llm_benchmark - INFO - Skipping run vllm-tp-tokenizer-reason-max-model-len as it's not in specified run names
2025-12-24 11:52:41,040 - llm_benchmark - INFO - Skipping run vllm-tool-call as it's not in specified run names
2025-12-24 11:52:41,040 - llm_benchmark - INFO - Skipping run vllm-speculative-decoding-mtp as it's not in specified run names
2025-12-24 11:52:41,040 - llm_benchmark - INFO - Skipping run vllm-deepgemm-disable as it's not in specified run names
2025-12-24 11:52:41,040 - llm_benchmark - INFO - Skipping run vllm-flashinfer as it's not in specified run names
2025-12-24 11:52:41,040 - llm_benchmark - INFO - Skipping run vllm-xformers as it's not in specified run names
2025-12-24 11:52:41,040 - llm_benchmark - INFO - Starting test for vllm-tp-tokenizer-reason
2025-12-24 11:52:41,040 - llm_benchmark - INFO - Set env HF_HOME=/workspace/gpustack_cache
2025-12-24 11:52:41,040 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 -tp 8 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3 --port 8000
2025-12-24 11:52:41,042 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds
2025-12-24 11:55:41,043 - llm_benchmark - INFO - Checking service readiness...
2025-12-24 12:12:01,159 - llm_benchmark - INFO - Service is ready
2025-12-24 12:12:01,159 - llm_benchmark - INFO - Running benchmark: sharegpt
2025-12-24 12:12:01,159 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 1000 --result-filename test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_sharegpt.json --save-result
2025-12-24 12:13:27,435 - llm_benchmark - INFO - Completed test case: sharegpt
2025-12-24 12:13:27,435 - llm_benchmark - INFO - Stopping current service...
2025-12-24 12:13:27,442 - llm_benchmark - INFO - Successfully stopped current service
2025-12-24 12:13:32,442 - llm_benchmark - INFO - Successfully completed test: vllm-tp-tokenizer-reason
2025-12-24 12:13:32,442 - llm_benchmark - INFO - Starting test for vllm-tp-tokenizer-reason-second
2025-12-24 12:13:32,442 - llm_benchmark - INFO - Set env HF_HOME=/workspace/gpustack_cache
2025-12-24 12:13:32,443 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 -tp 8 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3 --port 8000
2025-12-24 12:13:32,446 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds
2025-12-24 12:16:32,446 - llm_benchmark - INFO - Checking service readiness...
2025-12-24 12:30:02,540 - llm_benchmark - INFO - Service is ready
2025-12-24 12:30:02,540 - llm_benchmark - INFO - Running benchmark: sharegpt
2025-12-24 12:30:02,541 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 1000 --result-filename test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_second_sharegpt.json --save-result
2025-12-24 12:31:30,982 - llm_benchmark - INFO - Completed test case: sharegpt
2025-12-24 12:31:30,982 - llm_benchmark - INFO - Running benchmark: random_32k
2025-12-24 12:31:30,982 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 32000 --random-output-len 100 --num-prompts 100 --seed 42 --result-filename test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_second_random_32k.json --save-result
2025-12-24 12:37:39,083 - llm_benchmark - INFO - Completed test case: random_32k
2025-12-24 12:37:39,083 - llm_benchmark - INFO - Running benchmark: random_4k
2025-12-24 12:37:39,083 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 4000 --random-output-len 200 --num-prompts 500 --seed 42 --result-filename test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_second_random_4k.json --save-result
2025-12-24 12:41:39,649 - llm_benchmark - INFO - Completed test case: random_4k
2025-12-24 12:41:39,649 - llm_benchmark - INFO - Running benchmark: random_2k
2025-12-24 12:41:39,649 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 2000 --random-output-len 100 --num-prompts 500 --seed 42 --result-filename test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_second_random_2k.json --save-result
2025-12-24 12:43:32,978 - llm_benchmark - INFO - Completed test case: random_2k
2025-12-24 12:43:32,978 - llm_benchmark - INFO - Running benchmark: random_128
2025-12-24 12:43:32,978 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 128 --random-output-len 4 --num-prompts 1000 --seed 42 --result-filename test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_second_random_128.json --save-result
2025-12-24 12:43:56,164 - llm_benchmark - INFO - Completed test case: random_128
2025-12-24 12:43:56,165 - llm_benchmark - INFO - Running benchmark: random_2k_output
2025-12-24 12:43:56,165 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 1000 --random-output-len 2000 --num-prompts 100 --seed 42 --result-filename test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_second_random_2k_output.json --save-result
2025-12-24 12:46:17,371 - llm_benchmark - INFO - Completed test case: random_2k_output
2025-12-24 12:46:17,371 - llm_benchmark - INFO - Running benchmark: random_128k
2025-12-24 12:46:17,371 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 128000 --random-output-len 100 --num-prompts 50 --seed 42 --result-filename test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_second_random_128k.json --save-result

2025-12-24 13:04:34,880 - llm_benchmark - INFO - Completed test case: random_128k
2025-12-24 13:04:34,880 - llm_benchmark - INFO - Stopping current service...
2025-12-24 13:04:34,888 - llm_benchmark - INFO - Successfully stopped current service
2025-12-24 13:04:39,888 - llm_benchmark - INFO - Successfully completed test: vllm-tp-tokenizer-reason-second
2025-12-24 13:04:39,888 - llm_benchmark - INFO - Starting test for vllm-flashmla
2025-12-24 13:04:39,888 - llm_benchmark - INFO - Set env VLLM_ATTENTION_BACKEND=FLASHMLA
2025-12-24 13:04:39,888 - llm_benchmark - INFO - Set env HF_HOME=/workspace/gpustack_cache
2025-12-24 13:04:39,888 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 -tp 8 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3 --port 8000

## convert results

python convert_benchmark_results.py \
  ./test/deepseek_v3.2-results-1224/vllm_deepgemm_disable_sharegpt.json \
  ./test/deepseek_v3.2-results-1224/vllm_speculative_decoding_mtp_sharegpt.json \
  ./test/deepseek_v3.2-results-1224/vllm_tool_call_sharegpt.json \
  ./test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_max_model_len_sharegpt.json \
  ./test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_second_random_128.json \
  ./test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_second_random_128k.json \
  ./test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_second_random_2k.json \
  ./test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_second_random_2k_output.json \
  ./test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_second_random_32k.json \
  ./test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_second_random_4k.json \
  ./test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_second_sharegpt.json \
  ./test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_sharegpt-1.json \
  ./test/deepseek_v3.2-results-1224/vllm_tp_tokenizer_reason_sharegpt.json \
  -o ./test/deepseek_v3.2-results-1224/converted_results


# sglang

1.
./setup_envs.sh vllm

2. 
CONDA_BASE=$(conda info --base)
source "$CONDA_BASE/etc/profile.d/conda.sh"
conda activate sglang

3.
python3 -m sglang.compile_deep_gemm --model deepseek-ai/DeepSeek-V3.2 --tp 8 --trust-remote-code

mkdir -p logs

CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
nohup python3 -m sglang.compile_deep_gemm \
  --model deepseek-ai/DeepSeek-V3.2 \
  --tp 8 \
  --trust-remote-code \
  > logs/compile_deep_gemm.log 2>&1 &

4.
python bench_serving.py --config ./config_deepseek_v3.2_sglang-1224.yaml --output-dir ./test/deepseek_v3.2-results-1224 

python bench_serving.py --config ./config_deepseek_v3.2_sglang-1224.yaml --output-dir ./test/deepseek_v3.2-results-1224 --run-names sglang-official-tp-dp-context-length-32k,sglang-official-tp-dp-context-length-32k-kv-cache-type,sglang-official-tp-dp-context-length-32k-backend-flashmla-sparse-kv,sglang-official-tp-dp-context-length-32k-backend-fa3-fa3