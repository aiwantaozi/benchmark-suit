
1. 
hf download deepseek-ai/DeepSeek-V3.2


python bench_serving.py --config ./config_deepseek_v3.2-1220.yaml --output-dir ./test/deepseek_v3.2-results-1220

## sglang

1. 

2. dataset

3. 
python -m sglang.launch_server --model deepseek-ai/DeepSeek-V3.2 --tp 8 --port 8000 --chat-template ./tool_chat_template_deepseekv32.jinja

4.
python bench_serving.py --config ./config_deepseek_v3.2-1219.yaml --output-dir ./.cache/deepseek_v3.2-results --run-names sglang-baseline



## vllm

1.
python bench_serving.py --config ./config_deepseek_v3.2-1220.yaml --output-dir ./test/deepseek_v3.2-results-1220 --run-names vllm-tp

2.

### TOOD

https://github.com/vllm-project/vllm/pull/29848
考虑这个tool call