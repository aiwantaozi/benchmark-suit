

## Docs

https://github.com/sgl-project/sglang/blob/main/docs/basic_usage/deepseek_v32.md

## Engine

vLLM: vllm-0.13.0rc2
Sglang: 0.5.6.post2

## Total Token Throughput Per Second Summary

| engine | base-sharegpt | base-random-128 | base-random-2k | base-random-4k | base-random-32k | base-ramdom-2k-output | mtp-sharegpt(step1/step3)) | disable-deepgemm-sharegpt |            cp |
| ------ | ------------: | --------------: | -------------: | -------------: | --------------: | --------------------: | -------------------------: | ------------------------: | ------------: |
| vllm   |          5247 |           11726 |          11260 |           9986 |            9858 |                  3106 |         5593(+6.6%)/Failed |               4884(-6.9%) | not supported |
| sglang |          3012 |           12950 |          20582 |          10946 |           10015 |                  3558 |                  1481/1720 |                    failed |        failed |
| diff   |        -42.6% |          +10.4% |         +82.8% |          +9.6% |           +1.6% |                +14.5% |              -73.5%/Failed |                    Failed |           N/A |


| engine               | base-sharegpt | base-random-128 | base-random-2k | base-random-4k | base-random-32k | base-ramdom-2k-output | mtp-sharegpt(step1/step3)) | disable-deepgemm-sharegpt |            cp |
| -------------------- | ------------: | --------------: | -------------: | -------------: | --------------: | --------------------: | -------------------------: | ------------------------: | ------------: |
| vllm-v0.11.0+dpr1    |          5482 |            5931 |          17690 |          15808 |           15514 |                       |                            |                           |               |
| vllm-0.13.0rc2+dp3.2 |          5247 |           11726 |          11260 |           9986 |            9858 |                  3106 |         5593(+6.6%)/Failed |               4884(-6.9%) | not supported |
| diff                 |         -4.3% |          +97.7% |         -36.4% |         -36.8% |          -36.5% |                       |                            |                           |               |


### 数据分析

#### sglang 的 2048 adaptive threshold
random_2k（2000 tokens prefill） 是整个表里最“戏剧性”的点，正好卡在 sglang 的 2048 adaptive threshold 下方。
- sglang：
    - 仍然是 MHA_ONE_SHOT
    - 1 次 kernel
    - H200 FlashAttention var-len

- vLLM：
    - 已经开始 chunked KV / paged attention
    - 多 kernel launch
    - 调度开销上来

#### sharegpt sglang 比 vllm慢

- ShareGPT 的真实分布（关键）
    - prefill 大多 < 2k ✔
    - 但 batch size / 序列长度高度不一致 ❌
    - 存在 tool / reasoning / template 分支 ❌
    - cached prefix 不稳定 ❌

这会导致：

在 sglang 里发生什么？

- one-shot MHA 需要：
    - prefill < 2048
    - prefix + new tokens 能一次性打包
    - batch 内长度相对一致

- ShareGPT 会频繁破坏这些条件：
    - tool call 插入
    - reasoning 分段
    - 多轮对话 KV reuse 不规则

- 结果
    - 👉 one-shot path 频繁 miss / fallback
    - 👉 NSA adaptive 的优势被 control-flow overhead 吃掉

## Latency

- Output TPS
- Total TPS
- Mean TTFT
- Mean TPOT

## 数据集

### ShareGPT
ShareGPT 数据集是目前大语言模型（LLM）指令微调（Instruction Tuning）领域中最著名、影响力最大的数据集之一。它主要由用户在 **ShareGPT.com** 网站上分享的与 ChatGPT 或 GPT-4 的真实对话记录组成。

#### 1. 极高的数据质量与复杂性

与早期通过人工构建（如 Self-Instruct）或简单问答对（如 Alpaca）的数据集不同，ShareGPT 包含了**真实的人机交互**。

* **长度**: 大量 短到中等 prompt（几百～1k token）
* **输出长度**: 很不稳定（有工具调用 / reasoning / 多轮）
* **贴近真实的请求分布特征**: ShareGPT 是真实对话数据，输入/输出长度极不规则，且通常包含较多短请求
* **多轮对话：** 数据集包含大量的多轮追问和引导，这对于训练模型处理上下文关联至关重要。
* **逻辑严密：** 由于原始输出大多来自 GPT-3.5 或 GPT-4，其回复在逻辑性、连贯性和知识准确度上处于顶尖水平。

#### 2. 覆盖场景极其广泛

因为数据源于全球真实用户的自发分享，它涵盖了几乎所有可能的 LLM 使用场景：

* **代码编写与调试：** 大量的编程问题和代码优化建议。
* **创意写作：** 诗歌、故事、周报模板等。
* **角色扮演：** 模拟特定的职业、性格或历史人物进行对话。
* **数学与科学推理：** 复杂的逻辑推导过程。

#### 3. 数据格式的标准性

ShareGPT 的数据格式（通常为 JSON）已成为开源社区的一种**事实标准**。
许多主流的微调框架（如 LLaMA-Factory, FastChat）都原生支持 ShareGPT 格式。其基本结构通常如下：

```json
{
  "conversations": [
    {"from": "human", "value": "你好，请解释什么是量子纠缠。"},
    {"from": "gpt", "value": "量子纠缠是量子力学中一种奇特的现象..."}
  ]
}
```


### 4. 开源模型的“催化剂”

ShareGPT 是许多顶级开源模型的“秘密武器”：

* **Vicuna 的诞生：** 最早让开源模型（基于 LLaMA）达到 ChatGPT 90% 以上能力的 Vicuna 模型，核心就是使用了约 7 万条 ShareGPT 对话进行微调。
* **指令遵循能力：** 它极大地提升了开源模型理解复杂指令和拒绝不当请求的能力。


## 其他人的测试数据

### Michaelvll/llm-ie-benchmarks
https://github.com/Michaelvll/llm-ie-benchmarks?utm_source=chatgpt.com

#### 用vllm的benchmark脚本

- DeepSeek-R1
- **CPU**: Intel(R) Xeon(R) Platinum 8468
- **GPU**: 8x NVIDIA H200

| Input Tokens | Output Tokens | vLLM v0.8.4 | SGLang v0.4.5.post1 |
| ------------ | ------------- | ----------- | ------------------- |
| 1000         | 2000          | 1136.92     | 1041.14             |
| 5000         | 1000          | 857.13      | 821.40              |
| 10000        | 500           | 441.53      | 389.84              |
| 30000        | 100           | 37.07       | 33.94               |
| sharegpt     | sharegpt      | 1330.60     | 981.47              |

#### 用sglang的benchmark脚本

| Input Tokens | Output Tokens | vLLM v0.8.4 (2025-04-14) | SGLang v0.4.5.post3 (2025-04-21) |
| ------------ | ------------- | ------------------------ | -------------------------------- |
| 1000         | 2000          | 1042.17                  | 1329.14                          |
| 5000         | 1000          | 794.54                   | 951.64                           |
| 10000        | 500           | 436.08                   | 479.69                           |
| 30000        | 100           | 37.76                    | 47.38                            |

## 推理引擎

### vLLM

vLLM-0.13.0rc2 针对 DeepSeek-V3 做了非常深度的算子对齐（特别是 FP8 的 DeepGEMM 结合）。在处理变长、高并发的真实请求时，vLLM 的 Continuous Batching 调度器非常成熟，对于这种“杂乱”流量的显存利用率和 Slot 回收效率通常更高。

### SGLang

Sglang 的优势在于 RadixAttention（前缀缓存）。但在 ShareGPT 这种多样化、前缀重合度可能不高的测试中，RadixAttention 带来的收益有限。此外，Sglang 在处理某些复杂 Chat Template 时的 Python 层开销有时会拖累小 batch 的吞吐。

请求分布特征：Random 数据集（2k, 4k, 32k）通常是 固定长度、重 Prefill 的。

Sglang 的优势：Sglang 针对 DeepSeek 的 MLA (Multi-head Latent Attention) 架构做了极极致的 Kernel 优化。

Sglang 的执行后端（基于 FlashInfer 或自定义 Kernel）在处理长文本 Prefill 时，其算子融合度往往高于 vLLM。

#### 针对dp 3.2的优化

- DP Attention (Recommended) 推荐：--dp 8 --enable-dp-attention 推荐配置
- Short-sequence MHA prefill (adaptive)：sglang 在 prefill ≤ 2048 token 时，会自动切回“单次 one-shot MHA kernel”，避免走分块 / NSA / MLA 路径。One-shot MHA = 在一次 kernel 里，把 “全部需要参与 attention 的 token” 一次性算完。
- Choices of Attention Kernels: DeepSeek V3.2 的 attention backend 用 `nsa`. In this backend, different kernels for sparse prefilling/decoding are implemented, which can be specified by `--nsa-prefill-backend` and `--nsa-decode-backend` server arguments. 
  - H200: `flashmla_sparse` prefill attention (short-seq prefill uses MHA via FlashAttention varlen), `fa3` decode attention, `bf16` kv cache dtype.

- [Doc](https://github.com/sgl-project/sglang/blob/main/docs/basic_usage/deepseek_v32.md)

### 总结

| 场景                  | 性能领先者 | 原因                                         |
| --------------------- | ---------- | -------------------------------------------- |
| 高并发 Prefill (吞吐) | Sglang     | MLA 算子优化更深，FlashInfer 集成度高        |
| 低延迟 / 复杂调度     | vLLM       | 调度算法成熟，DeepGEMM 集成早                |
| 长文本 (128k+)        | Sglang     | RadixAttention 节省显存，支持并行策略多      |
| R1 推理 (Thinking)    | vLLM       | 对 Reasoning 过程中的变长 Token 产生处理更稳 |