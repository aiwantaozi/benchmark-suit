
1. 
hf download deepseek-ai/DeepSeek-V3.2


## vllm

0.13.0

1.
chmod +x setup_envs.sh
./setup_envs.sh vllm

2. 
./setup_ep_env.sh

## sglang

1. 
./setup_env.sh sglang

2. dataset
download_dataset.sh

3. 
python -m sglang.launch_server --model deepseek-ai/DeepSeek-V3.2 --tp 8 --port 8000 --chat-template ./tool_chat_template_deepseekv32.jinja
如果遇到这个错误：https://github.com/sgl-project/sglang/issues/10354
pip3 install sgl-kernel --force-reinstall
16分钟

4. sglang-no-chat-template
python bench_serving.py --config ./config_deepseek_v3.2-1219.yaml --output-dir ./.cache/deepseek_v3.2-results --run-names sglang-baseline

2025-12-19 12:32:37,192 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n sglang python -m sglang.launch_server --model-path deepseek-ai/DeepSeek-V3.2 --host 0.0.0.0 --port 8000 --tensor-parallel-size 8
2025-12-19 12:32:37,198 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds

2025-12-19 12:35:37,199 - llm_benchmark - INFO - Checking service readiness...
2025-12-19 12:38:27,382 - llm_benchmark - INFO - Service is ready
2025-12-19 12:38:27,383 - llm_benchmark - INFO - Running benchmark: sharegpt
2025-12-19 12:38:27,383 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 1000 --result-filename test/deepseek_v3.2-results-1219/sglang_no_chat_template_sharegpt.json --save-result
2025-12-19 12:41:11,054 - llm_benchmark - INFO - Completed test case: sharegpt
2025-12-19 12:41:11,054 - llm_benchmark - INFO - Stopping current service...
2025-12-19 12:41:11,258 - llm_benchmark - INFO - Successfully stopped current service
2025-12-19 12:41:16,259 - llm_benchmark - INFO - Successfully completed test: sglang-no-chat-template
2025-12-19 12:41:16,261 - llm_benchmark - INFO - Report generated: test/deepseek_v3.2-results-1219/benchmark_report_1766148076.json
2025-12-19 12:41:16,261 - llm_benchmark - INFO - All tests completed. Report: test/deepseek_v3.2-results-1219/benchmark_report_1766148076.json


5. sglang-dp-attention 
2025-12-19 12:43:21,281 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n sglang python -m sglang.launch_server --model-path deepseek-ai/DeepSeek-V3.2 --host 0.0.0.0 --port 8000 --tensor-parallel-size 8 --chat-template ./tool_chat_template_deepseekv32.jinja --enable-dp-attention
2025-12-19 12:43:21,287 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds
2025-12-19 12:46:21,287 - llm_benchmark - INFO - Checking service readiness...
2025-12-19 12:47:51,440 - llm_benchmark - INFO - Service is ready
2025-12-19 12:47:51,441 - llm_benchmark - INFO - Running benchmark: sharegpt
2025-12-19 12:47:51,441 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 1000 --result-filename test/deepseek_v3.2-results-1219/sglang_dp_attention_sharegpt.json --save-result
2025-12-19 12:49:54,294 - llm_benchmark - INFO - Completed test case: sharegpt
2025-12-19 12:49:54,294 - llm_benchmark - INFO - Stopping current service...
2025-12-19 12:49:54,511 - llm_benchmark - INFO - Successfully stopped current service
2025-12-19 12:49:59,515 - llm_benchmark - INFO - Successfully completed test: sglang-dp-attention
2025-12-19 12:49:59,517 - llm_benchmark - INFO - Report generated: test/deepseek_v3.2-results-1219/benchmark_report_1766148599.json
2025-12-19 12:49:59,517 - llm_benchmark - INFO - All tests completed. Report: test/deepseek_v3.2-results-1219/benchmark_report_1766148599.json

6. sglang-official-recommended-tp-dp

7. sglang-speculative-decoding-mtp-step3-env-max-req-256


pip install nvidia-nvshmem-cu12


## vllm

Name: vllm
Version: 0.13.0
Summary: A high-throughput and memory-efficient inference and serving engine for LLMs
Home-page: https://github.com/vllm-project/vllm
Author: vLLM Team
Author-email: 
License-Expression: Apache-2.0
Location: /root/miniconda3/envs/vllm/lib/python3.12/site-packages
Requires: aiohttp, anthropic, blake3, cachetools, cbor2, cloudpickle, compressed-tensors, depyf, diskcache, einops, fastapi, filelock, flashinfer-python, gguf, ijson, lark, llguidance, lm-format-enforcer, mcp, mistral_common, model-hosting-container-standards, msgspec, ninja, numba, numpy, openai, openai-harmony, opencv-python-headless, outlines_core, partial-json-parser, pillow, prometheus-fastapi-instrumentator, prometheus_client, protobuf, psutil, py-cpuinfo, pybase64, pydantic, python-json-logger, pyyaml, pyzmq, ray, regex, requests, scipy, sentencepiece, setproctitle, setuptools, six, tiktoken, tokenizers, torch, torchaudio, torchvision, tqdm, transformers, typing_extensions, watchfiles, xgrammar


1.
vllm serve deepseek-ai/DeepSeek-V3.2 \
--tensor-parallel-size 1 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3 -dp 8 --enable-expert-parallel 
起不来

2.

vllm serve deepseek-ai/DeepSeek-V3.2 \
--tensor-parallel-size 1 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3 -dp 8 --enable-expert-parallel --max-num-seqs 128 --max-model-len 122880 \
--port 8000

total --max-model-len is 163840

3.

(vllm) root@77ace2f29454:~/benchmark-suit# python bench_serving.py --config ./config_deepseek_v3.2-1219.yaml --output-dir ./test/deepseek_v3.2-results-1219 --run-names vllm-tp

2025-12-19 16:00:58,723 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm serve deepseek-ai/DeepSeek-V3.2 --tensor-parallel-size 8 --tokenizer-mode deepseek_v32 --reasoning-parser deepseek_v3
 --port 8000
2025-12-19 16:00:58,729 - llm_benchmark - INFO - Waiting for initial delay of 180 seconds
2025-12-19 16:03:58,736 - llm_benchmark - INFO - Checking service readiness...
2025-12-19 16:23:41,261 - llm_benchmark - INFO - Service is ready
2025-12-19 16:23:41,262 - llm_benchmark - INFO - Running benchmark: sharegpt
2025-12-19 16:23:41,262 - llm_benchmark - INFO - Running command: conda run --no-capture-output -n vllm vllm bench serve --model deepseek-ai/DeepSeek-V3.2 --backend openai-chat --endpoint /v1/chat/completions --dataset-name sharegpt --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --num-prompts 1000 --result-filename test/deepseek_v3.2-results-1219/vllm_tp_sharegpt.json --save-result

## convert result

python convert_benchmark_results.py \
  ./test/deepseek_v3.2-results-1219/sglang_dp_attention_sharegpt.json \
  ./test/deepseek_v3.2-results-1219/sglang_official_recommended_tp_dp_sharegpt.json \
  ./test/deepseek_v3.2-results-1219/sglang_official_recommended_tp_dp_ep_sharegpt.json \
  -o ./test/deepseek_v3.2-results-1219/converted_results


### TOOD

https://github.com/vllm-project/vllm/pull/29848
考虑这个tool call