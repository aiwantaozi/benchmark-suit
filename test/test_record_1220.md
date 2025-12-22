
1. 
hf download deepseek-ai/DeepSeek-V3.2
python bench_serving.py --config ./config_deepseek_v3.2-1220.yaml --output-dir ./test/deepseek_v3.2-results-1220

2. 

git config --global credential.helper store
git config --global user.email "xxx"
git config --global user.name "xxx"

## sglang

1. 

2. dataset

3. 
python -m sglang.launch_server --model deepseek-ai/DeepSeek-V3.2 --tp 8 --port 8000 --chat-template ./tool_chat_template_deepseekv32.jinja

4.
python bench_serving.py --config ./config_deepseek_v3.2-1219.yaml --output-dir ./.cache/deepseek_v3.2-results --run-names sglang-baseline



## vllm

(vllm) root@5f9d99f47ac3:~/benchmark-suit# python bench_serving.py --config ./config_deepseek_v3.2-1220.yaml --output-dir ./test/deepseek_v3.2-results-1220
2025-12-20 08:29:41,753 - llm_benchmark - INFO - Starting test for vllm-tp
2025-12-20 08:29:41,754 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 --tensor-parallel-size 8 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3
 --port 8000
2025-12-20 08:29:41,756 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds
2025-12-20 08:32:41,756 - llm_benchmark - INFO - Checking service readiness...
2025-12-20 08:51:51,891 - llm_benchmark - INFO - Service is ready
2025-12-20 08:51:51,892 - llm_benchmark - INFO - Running benchmark: sharegpt
2025-12-20 08:51:51,892 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 1000 --result-filename test/deepseek_v3.2-results-1220/vllm_tp_sharegpt.json --save-result
2025-12-20 08:53:50,601 - llm_benchmark - INFO - Completed test case: sharegpt
2025-12-20 08:53:50,601 - llm_benchmark - INFO - Running benchmark: random_32k
2025-12-20 08:53:50,601 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 32000 --random-output-len 100 --num-prompts 100 --seed 42 --result-filename test/deepseek_v3.2-results-1220/vllm_tp_random_32k.json --save-result
2025-12-20 08:59:55,817 - llm_benchmark - INFO - Completed test case: random_32k
2025-12-20 08:59:55,817 - llm_benchmark - INFO - Running benchmark: random_4k
2025-12-20 08:59:55,817 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 4000 --random-output-len 200 --num-prompts 500 --seed 42 --result-filename test/deepseek_v3.2-results-1220/vllm_tp_random_4k.json --save-result
2025-12-20 09:04:11,371 - llm_benchmark - INFO - Completed test case: random_4k
2025-12-20 09:04:11,371 - llm_benchmark - INFO - Running benchmark: random_2k
2025-12-20 09:04:11,371 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 2000 --random-output-len 100 --num-prompts 500 --seed 42 --result-filename test/deepseek_v3.2-results-1220/vllm_tp_random_2k.json --save-result
2025-12-20 09:06:09,000 - llm_benchmark - INFO - Completed test case: random_2k
2025-12-20 09:06:09,000 - llm_benchmark - INFO - Running benchmark: random_128
2025-12-20 09:06:09,000 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 128 --random-output-len 4 --num-prompts 1000 --seed 42 --result-filename test/deepseek_v3.2-results-1220/vllm_tp_random_128.json --save-result
2025-12-20 09:06:31,622 - llm_benchmark - INFO - Completed test case: random_128
2025-12-20 09:06:31,622 - llm_benchmark - INFO - Running benchmark: random_128k
2025-12-20 09:06:31,622 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 128000 --random-output-len 100 --num-prompts 100 --seed 42 --result-filename test/deepseek_v3.2-results-1220/vllm_tp_random_128k.json --save-result
2025-12-20 09:42:28,020 - llm_benchmark - INFO - Completed test case: random_128k
2025-12-20 09:42:28,020 - llm_benchmark - INFO - Running benchmark: random_2k_output
2025-12-20 09:42:28,020 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 1000 --random-output-len 2000 --num-prompts 100 --seed 42 --result-filename test/deepseek_v3.2-results-1220/vllm_tp_random_2k_output.json --save-result
2025-12-20 09:44:52,668 - llm_benchmark - INFO - Completed test case: random_2k_output
2025-12-20 09:44:52,668 - llm_benchmark - INFO - Stopping current service...
2025-12-20 09:44:52,675 - llm_benchmark - INFO - Successfully stopped current service
2025-12-20 09:44:57,675 - llm_benchmark - INFO - Successfully completed test: vllm-tp
2025-12-20 09:44:57,675 - llm_benchmark - INFO - Starting test for vllm-dp-ep-half-ctx
2025-12-20 09:44:57,675 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 --tensor-parallel-size 1 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3 -dp 8 --enable-expert-parallel --max-model-len 81920
 --port 8000
2025-12-20 09:44:57,678 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds
2025-12-20 09:47:57,678 - llm_benchmark - INFO - Checking service readiness...
2025-12-20 09:56:17,739 - llm_benchmark - INFO - Service is ready
2025-12-20 09:56:17,739 - llm_benchmark - INFO - Running benchmark: sharegpt
2025-12-20 09:56:17,739 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 1000 --result-filename test/deepseek_v3.2-results-1220/vllm_dp_ep_half_ctx_sharegpt.json --save-result
2025-12-20 09:57:41,437 - llm_benchmark - INFO - Completed test case: sharegpt
2025-12-20 09:57:41,437 - llm_benchmark - INFO - Stopping current service...
2025-12-20 09:57:41,445 - llm_benchmark - INFO - Successfully stopped current service
2025-12-20 09:57:46,445 - llm_benchmark - INFO - Successfully completed test: vllm-dp-ep-half-ctx
2025-12-20 09:57:46,445 - llm_benchmark - INFO - Starting test for vllm-tp-dcp
2025-12-20 09:57:46,445 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3 -tp 8 -dcp 8
 --port 8000


## tensorrt

1. image
nvcr.io/nvidia/tensorrt-llm/release:1.2.0rc5

2. serve to download model
trtllm-serve "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
trtllm-serve deepseek-ai/DeepSeek-V3.2 --tp_size 8 --tokens_per_block 64

3. clone
git clone https://github.com/aiwantaozi/benchmark-suit
cd benchmark-suit
git checkout test

git clone
https://github.com/NVIDIA/TensorRT-LLM

4. 
cd examples/llm-api
python quickstart_advanced.py --model_dir <YOUR_MODEL_DIR> --tp_size 8 --tokens_per_block 64

5. mtp
cd examples/llm-api
python quickstart_advanced.py --model_dir <YOUR_MODEL_DIR> --spec_decode_algo MTP --spec_decode_max_draft_len N


### TOOD

https://github.com/vllm-project/vllm/pull/29848
考虑这个tool call

