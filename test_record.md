
## Environement Set up steps

### vLLM

1. env

setup_envs.sh vllm 

2. apply change to prevent error

https://github.com/vllm-project/vllm/pull/30924
vllm-0.13.0rc2
with this commit
https://github.com/vllm-project/vllm/pull/30924/commits/194985d0cf63b0b19d85354940cbebe7447ac250

git clone https://github.com/neuralmagic/vllm
cd vllm
git checkout lwilkinson/fix-dsv32
git format-patch 194985d..HEAD --relative=vllm -o patches

pip show vllm
cd /root/miniconda3/envs/vllm/lib/python3.12/site-packages/vllm
git apply patches/*.patch

2. deepgemm
install_deepgemm.sh

3. dataset
download_dataset.sh

4. download model
hf download deepseek-ai/DeepSeek-V3.2

5. warmup
vllm serve deepseek-ai/DeepSeek-V3.2 \
--tensor-parallel-size 8 \
--tokenizer-mode deepseek_v32 \
--tool-call-parser deepseek_v32 \
--enable-auto-tool-choice \
--reasoning-parser deepseek_v3

这里花了 27分钟

6. simple test
mkdir -p ./.cache/vllm-simple-test
conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 4000 --random-output-len 200 --num-prompts 10 --seed 42 --result-filename ./cache/vllm-simple-test/vllm-simple-test.json --save-result

7. base line
mkdir -p ./.cache/deepseek_v3.2-results
python bench_serving.py --config ./config_deepseek_v3.2.yaml --output-dir ./.cache/deepseek_v3.2-results --run-names vllm-baseline

2025-12-18 12:01:35,604 - llm_benchmark - INFO - Skipping run sglang-baseline as it's not in specified run names
2025-12-18 12:01:35,604 - llm_benchmark - INFO - Skipping run sglang-speculative-decoding-eagle3-steps1 as it's not in specified run names
2025-12-18 12:01:35,604 - llm_benchmark - INFO - Skipping run sglang-context-parallel as it's not in specified run names
2025-12-18 12:01:35,604 - llm_benchmark - INFO - Skipping run sglang-deepgemm-diable as it's not in specified run names
2025-12-18 12:01:35,604 - llm_benchmark - INFO - Skipping run vllm-deepgemm-disable as it's not in specified run names
2025-12-18 12:01:35,604 - llm_benchmark - INFO - Starting test for vllm-baseline
2025-12-18 12:01:35,604 - llm_benchmark - INFO - Running benchmark: sharegpt
2025-12-18 12:01:35,604 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 1000 --result-filename .cache/deepseek_v3.2-results/vllm_baseline_sharegpt.json --save-result

2025-12-18 12:04:05,244 - llm_benchmark - INFO - Completed test case: sharegpt
2025-12-18 12:04:05,245 - llm_benchmark - INFO - Running benchmark: random_32k
2025-12-18 12:04:05,245 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 32000 --random-output-len 100 --num-prompts 100 --seed 42 --result-filename .cache/deepseek_v3.2-results/vllm_baseline_random_32k.json --save-result
2025-12-18 12:10:21,442 - llm_benchmark - INFO - Completed test case: random_32k
2025-12-18 12:10:21,442 - llm_benchmark - INFO - Running benchmark: random_4k
2025-12-18 12:10:21,442 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 4000 --random-output-len 200 --num-prompts 500 --seed 42 --result-filename .cache/deepseek_v3.2-results/vllm_baseline_random_4k.json --save-result
2025-12-18 12:14:31,632 - llm_benchmark - INFO - Completed test case: random_4k
2025-12-18 12:14:31,632 - llm_benchmark - INFO - Running benchmark: random_2k
2025-12-18 12:14:31,632 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 2000 --random-output-len 100 --num-prompts 500 --seed 42 --result-filename .cache/deepseek_v3.2-results/vllm_baseline_random_2k.json --save-result
2025-12-18 12:16:36,199 - llm_benchmark - INFO - Completed test case: random_2k
2025-12-18 12:16:36,199 - llm_benchmark - INFO - Running benchmark: random_128
2025-12-18 12:16:36,199 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 128 --random-output-len 4 --num-prompts 1000 --seed 42 --result-filename .cache/deepseek_v3.2-results/vllm_baseline_random_128.json --save-result
2025-12-18 12:17:12,808 - llm_benchmark - INFO - Completed test case: random_128
2025-12-18 12:17:12,809 - llm_benchmark - INFO - Running benchmark: random_2k_output
2025-12-18 12:17:12,809 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 1000 --random-output-len 2000 --num-prompts 100 --seed 42 --result-filename .cache/deepseek_v3.2-results/vllm_baseline_random_2k_output.json --save-result
2025-12-18 12:19:40,160 - llm_benchmark - INFO - Completed test case: random_2k_output
2025-12-18 12:19:45,161 - llm_benchmark - INFO - Successfully completed test: vllm-baseline
2025-12-18 12:19:45,163 - llm_benchmark - INFO - Report generated: .cache/deepseek_v3.2-results/benchmark_report_1766060385.json
2025-12-18 12:19:45,163 - llm_benchmark - INFO - All tests completed. Report: .cache/deepseek_v3.2-results/benchmark_report_1766060385.json

7. without tool 这次启动只花了4分钟
python bench_serving.py --config ./config_deepseek_v3.2.yaml --output-dir ./.cache/deepseek_v3.2-results --run-names vllm-without-tool
2025-12-18 12:28:09,740 - llm_benchmark - INFO - Skipping run vllm-baseline as it's not in specified run names
2025-12-18 12:28:09,740 - llm_benchmark - INFO - Skipping run sglang-baseline as it's not in specified run names
2025-12-18 12:28:09,740 - llm_benchmark - INFO - Skipping run vllm-speculative-decoding-mtp as it's not in specified run names
2025-12-18 12:28:09,740 - llm_benchmark - INFO - Skipping run sglang-speculative-decoding-eagle3-steps1 as it's not in specified run names
2025-12-18 12:28:09,740 - llm_benchmark - INFO - Skipping run sglang-context-parallel as it's not in specified run names
2025-12-18 12:28:09,740 - llm_benchmark - INFO - Skipping run sglang-deepgemm-diable as it's not in specified run names
2025-12-18 12:28:09,740 - llm_benchmark - INFO - Skipping run vllm-deepgemm-disable as it's not in specified run names
2025-12-18 12:28:09,740 - llm_benchmark - INFO - Starting test for vllm-without-tool
2025-12-18 12:28:09,740 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 -tp 8 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3 --port 8000
2025-12-18 12:28:09,746 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds
2025-12-18 12:31:09,747 - llm_benchmark - INFO - Checking service readiness...
2025-12-18 12:31:54,801 - llm_benchmark - INFO - Service is ready
2025-12-18 12:31:54,802 - llm_benchmark - INFO - Running benchmark: sharegpt
2025-12-18 12:31:54,802 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 1000 --result-filename .cache/deepseek_v3.2-results/vllm_without_tool_sharegpt.json --save-result
2025-12-18 12:33:35,195 - llm_benchmark - INFO - Completed test case: sharegpt
2025-12-18 12:33:35,195 - llm_benchmark - INFO - Stopping current service...
2025-12-18 12:33:35,211 - llm_benchmark - INFO - Successfully stopped current service
2025-12-18 12:33:40,251 - llm_benchmark - INFO - Successfully completed test: vllm-without-tool
2025-12-18 12:33:40,253 - llm_benchmark - INFO - Report generated: .cache/deepseek_v3.2-results/benchmark_report_1766061220.json
2025-12-18 12:33:40,253 - llm_benchmark - INFO - All tests completed. Report: .cache/deepseek_v3.2-results/benchmark_report_1766061220.json

8. only tp

9. vllm-without-tool-reason
2025-12-18 12:49:16,332 - llm_benchmark - INFO - Skipping run vllm-baseline as it's not in specified run names
2025-12-18 12:49:16,332 - llm_benchmark - INFO - Skipping run vllm-without-tool as it's not in specified run names
2025-12-18 12:49:16,333 - llm_benchmark - INFO - Skipping run sglang-baseline as it's not in specified run names
2025-12-18 12:49:16,333 - llm_benchmark - INFO - Skipping run vllm-speculative-decoding-mtp as it's not in specified run names
2025-12-18 12:49:16,333 - llm_benchmark - INFO - Skipping run sglang-speculative-decoding-eagle3-steps1 as it's not in specified run names
2025-12-18 12:49:16,333 - llm_benchmark - INFO - Skipping run sglang-context-parallel as it's not in specified run names
2025-12-18 12:49:16,333 - llm_benchmark - INFO - Skipping run sglang-deepgemm-diable as it's not in specified run names
2025-12-18 12:49:16,333 - llm_benchmark - INFO - Skipping run vllm-deepgemm-disable as it's not in specified run names
2025-12-18 12:49:16,333 - llm_benchmark - INFO - Starting test for vllm-without-tool-reason
2025-12-18 12:49:16,333 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 -tp 8 --tokenizer-mode deepseek_v32 --port 8000
2025-12-18 12:49:16,337 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds
2025-12-18 12:52:16,338 - llm_benchmark - INFO - Checking service readiness...
2025-12-18 12:52:46,368 - llm_benchmark - INFO - Service is ready
2025-12-18 12:52:46,368 - llm_benchmark - INFO - Running benchmark: sharegpt
2025-12-18 12:52:46,368 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 1000 --result-filename .cache/deepseek_v3.2-results/vllm_without_tool_reason_sharegpt.json --save-result
2025-12-18 12:54:28,118 - llm_benchmark - INFO - Completed test case: sharegpt
2025-12-18 12:54:28,119 - llm_benchmark - INFO - Stopping current service...
2025-12-18 12:54:28,134 - llm_benchmark - INFO - Successfully stopped current service
2025-12-18 12:54:33,135 - llm_benchmark - INFO - Successfully completed test: vllm-without-tool-reason
2025-12-18 12:54:33,137 - llm_benchmark - INFO - Report generated: .cache/deepseek_v3.2-results/benchmark_report_1766062473.json
2025-12-18 12:54:33,137 - llm_benchmark - INFO - All tests completed. Report: .cache/deepseek_v3.2-results/benchmark_report_1766062473.json

10. vllm-speculative-decoding-mtp
2025-12-18 13:07:14,951 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 -tp 8 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3 --speculative-config {"method":"mtp","num_speculative_tokens":1}
 --port 8000
2025-12-18 13:07:14,957 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds

2025-12-18 13:10:14,958 - llm_benchmark - INFO - Checking service readiness...
2025-12-18 13:11:25,014 - llm_benchmark - INFO - Service is ready
2025-12-18 13:11:25,015 - llm_benchmark - INFO - Running benchmark: sharegpt
2025-12-18 13:11:25,015 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 1000 --result-filename .cache/deepseek_v3.2-results/vllm_speculative_decoding_mtp_sharegpt.json --save-result
2025-12-18 13:13:06,460 - llm_benchmark - INFO - Completed test case: sharegpt
2025-12-18 13:13:06,460 - llm_benchmark - INFO - Stopping current service...
2025-12-18 13:13:06,475 - llm_benchmark - INFO - Successfully stopped current service
2025-12-18 13:13:11,476 - llm_benchmark - INFO - Successfully completed test: vllm-speculative-decoding-mtp
2025-12-18 13:13:11,477 - llm_benchmark - INFO - Report generated: .cache/deepseek_v3.2-results/benchmark_report_1766063591.json
2025-12-18 13:13:11,477 - llm_benchmark - INFO - All tests completed. Report: .cache/deepseek_v3.2-results/benchmark_report_1766063591.json

11. vllm-deepgemm-disable
Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 -tp 8 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3 --port 8000
2025-12-18 13:15:01,328 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds
2025-12-18 13:18:01,328 - llm_benchmark - INFO - Checking service readiness...
2025-12-18 13:19:16,464 - llm_benchmark - INFO - Service is ready
2025-12-18 13:19:16,465 - llm_benchmark - INFO - Running benchmark: sharegpt
2025-12-18 13:19:16,465 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 1000 --result-filename .cache/deepseek_v3.2-results/vllm_deepgemm_disable_sharegpt.json --save-result
2025-12-18 13:21:03,958 - llm_benchmark - INFO - Completed test case: sharegpt
2025-12-18 13:21:03,958 - llm_benchmark - INFO - Stopping current service...
2025-12-18 13:21:03,973 - llm_benchmark - INFO - Successfully stopped current service
2025-12-18 13:21:08,975 - llm_benchmark - INFO - Successfully completed test: vllm-deepgemm-disable
2025-12-18 13:21:08,977 - llm_benchmark - INFO - Report generated: .cache/deepseek_v3.2-results/benchmark_report_1766064068.json
2025-12-18 13:21:08,977 - llm_benchmark - INFO - All tests completed. Report: .cache/deepseek_v3.2-results/benchmark_report_1766064068.json

### SGLang


1. env
setup_envs.sh sglang

2. deepgemm

apt update
apt install -y libnuma1 libnuma-dev
pip install --upgrade sgl_kernel
python3 -m sglang.compile_deep_gemm --model deepseek-ai/DeepSeek-V3.2 --tp 8 --trust-remote-code
这里花了20分钟

3. warmup
python -m sglang.launch_server --model deepseek-ai/DeepSeek-V3.2 --tp 8 --port 8000 --chat-template ./tool_chat_template_deepseekv32.jinja
pip install torch-c-dlpack-ext

4. simple test

mkdir -p ./cache/test

conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 4000 --random-output-len 200 --num-prompts 10 --seed 42 --result-filename ./cache/test/sglang-simple-test.json --save-result

5. base line


python bench_serving.py --config ./config_deepseek_v3.2.yaml --output-dir ./.cache/deepseek_v3.2-results --run-names sglang-baseline
2025-12-18 14:16:42,826 - llm_benchmark - INFO - Completed test case: sharegpt
2025-12-18 14:16:42,827 - llm_benchmark - INFO - Running benchmark: random_32k
2025-12-18 14:16:42,827 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 32000 --random-output-len 100 --num-prompts 100 --seed 42 --result-filename .cache/deepseek_v3.2-results/sglang_baseline_random_32k.json --save-result
2025-12-18 14:22:57,312 - llm_benchmark - INFO - Completed test case: random_32k
2025-12-18 14:22:57,313 - llm_benchmark - INFO - Running benchmark: random_4k
2025-12-18 14:22:57,313 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 4000 --random-output-len 200 --num-prompts 500 --seed 42 --result-filename .cache/deepseek_v3.2-results/sglang_baseline_random_4k.json --save-result
2025-12-18 14:26:42,953 - llm_benchmark - INFO - Completed test case: random_4k
2025-12-18 14:26:42,954 - llm_benchmark - INFO - Running benchmark: random_2k
2025-12-18 14:26:42,954 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 2000 --random-output-len 100 --num-prompts 500 --seed 42 --result-filename .cache/deepseek_v3.2-results/sglang_baseline_random_2k.json --save-result
2025-12-18 14:27:58,293 - llm_benchmark - INFO - Completed test case: random_2k
2025-12-18 14:27:58,293 - llm_benchmark - INFO - Running benchmark: random_128
2025-12-18 14:27:58,293 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 128 --random-output-len 4 --num-prompts 1000 --seed 42 --result-filename .cache/deepseek_v3.2-results/sglang_baseline_random_128.json --save-result
2025-12-18 14:28:24,798 - llm_benchmark - INFO - Completed test case: random_128
2025-12-18 14:28:24,799 - llm_benchmark - INFO - Running benchmark: random_2k_output
2025-12-18 14:28:24,799 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name random --random-input-len 1000 --random-output-len 2000 --num-prompts 100 --seed 42 --result-filename .cache/deepseek_v3.2-results/sglang_baseline_random_2k_output.json --save-result
2025-12-18 14:30:32,346 - llm_benchmark - INFO - Completed test case: random_2k_output
2025-12-18 14:30:37,346 - llm_benchmark - INFO - Successfully completed test: sglang-baseline
2025-12-18 14:30:37,348 - llm_benchmark - INFO - Report generated: .cache/deepseek_v3.2-results/benchmark_report_1766068237.json
2025-12-18 14:30:37,348 - llm_benchmark - INFO - All tests completed. Report: .cache/deepseek_v3.2-results/benchmark_report_1766068237.json

6. sglang-speculative-decoding-eagle3-steps1
python bench_serving.py --config ./config_deepseek_v3.2.yaml --output-dir ./.cache/deepseek_v3.2-results --run-names sglang-speculative-decoding-eagle3-steps1
失败了

7.
python bench_serving.py --config ./config_deepseek_v3.2.yaml --output-dir ./.cache/deepseek_v3.2-results --run-names sglang-speculative-decoding-mtp  
2025-12-18 14:43:14,264 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n sglang python -m sglang.launch_server --model-path deepseek-ai/DeepSeek-V3.2 --host 0.0.0.0 --port 8000 --tensor-parallel-size 8 --speculative-algorithm EAGLE --speculative-num-steps 1 --speculative-eagle-topk 1 --speculative-num-draft-tokens 2
2025-12-18 14:43:14,271 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds

### tensor-rt

https://github.com/NVIDIA/TensorRT-LLM/blob/main/examples/models/core/deepseek_v3/README.md

trtllm-serve --tp_size 8 --tokens_per_block 64