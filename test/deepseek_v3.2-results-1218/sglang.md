
# SGLang

# 1️⃣ MHA（Multi-Head Attention）是什么？——基线形态

## 基本定义

**MHA = Multi-Head Attention**，Transformer 的核心算子。

对每一层、每一个 token：

[
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d}}\right)V
]

MHA 的意思是：

* 把 hidden dim 切成 **多个 head**
* 每个 head 独立算 attention
* 最后 concat

---

## 在推理时，MHA 被拆成两个阶段

### 🔹 Prefill（上下文阶段）

* 输入 prompt 的所有 token
* **Q/K/V 都是新的**
* 计算量大，但一次性

### 🔹 Decode（生成阶段）

* 每次只生成 1 token
* **Q 是新的，K/V 来自 KV cache**
* memory-bound + latency-sensitive

> 你 benchmark 里 random_* 和 ShareGPT 的差异，本质上就是 **prefill vs decode 占比不同**。

---

# 2️⃣ One-shot MHA：推理优化里的“理想状态”

## 什么是 one-shot MHA？

**One-shot MHA = 在一次 kernel 里，把 “全部需要参与 attention 的 token” 一次性算完。**

在推理中意味着：

* cached prefix tokens
* 当前新 tokens（prefill 或 decode）

👉 **一次 kernel invocation 完成 attention**

---

## 为什么 one-shot MHA 快？

### 对比普通（chunked）做法

### ❌ Chunked MHA（常规）

```
for each chunk:
    load K/V chunk
    compute partial attention
    reduce
```

* 多次 kernel launch
* KV cache 分段加载
* 调度 & sync 开销大

---

### ✅ One-shot MHA

```
load all K/V once
compute attention in one kernel
```

* 1 次 kernel
* 完全算子受限（compute-bound）
* 非常适合 **短序列**

---

## 关键限制（非常重要）

One-shot MHA 只有在以下条件成立时才可用：

| 条件                | 原因                      |
| ----------------- | ----------------------- |
| 总序列长度不太长          | K/V 必须一次放得下             |
| batch 内长度相对一致     | 避免 padding / divergence |
| 没有复杂 control-flow | tool / reasoning 会破坏连续性 |

👉 **这正是 sglang 在 ≤2048 token 才启用它的原因**

---

# 3️⃣ NSA backend：Non-Sequential Attention（sglang 的长上下文武器）

## NSA 是什么？

**NSA = Non-Sequential Attention**

它的目标是：

> 在 **prefill 阶段**，让 attention 不再“按 token 顺序扫描”，
> 而是 **并行处理不同位置 / 不同 chunk 的 attention**。

---

## NSA 解决了什么问题？

### 传统长上下文 attention 的瓶颈

* 序列长（32k / 64k）
* KV cache 很大
* Prefill 变成 **memory-bound**

NSA 的核心思想：

* 把长序列切成 chunk
* chunk 之间 **并行计算 attention**
* 减少 sequential dependency

---

## NSA 在 sglang 中的工作方式（结合你用的）

### 自动启用逻辑（你已经看过文档）

* **≤2048** → 直接 MHA one-shot
* **>2048** → NSA backend

### 在 H200 / B200 上的实现

| GPU          | 实现                           |
| ------------ | ---------------------------- |
| H200 (SM90)  | FlashAttention var-len + NSA |
| B200 (SM100) | TRT-LLM ragged MHA           |

---

## NSA 的 trade-off

| 优点                  | 代价           |
| ------------------- | ------------ |
| 长上下文 prefill 吞吐大幅提升 | kernel 复杂    |
| 并行度高                | launch /调度开销 |
| 对 32k+ 非常友好         | 对短序列不划算      |

👉 **这解释了你 random_32k 的表现**

---

# 4️⃣ Sparse MLA：DeepSeek-V3.x 的“模型侧加速器”

## MLA 是什么？

**MLA = Multi-Head Latent Attention**（DeepSeek 的架构特性）

核心思想：

* 不对所有 head / token 做 full attention
* 用 latent representation 压缩 KV

---

## Sparse MLA 是什么？

在推理时：

* 不是每个 token 都参与 attention
* 只对 **重要 token / latent slot** 做 attention
* attention 变稀疏（sparse）

---

## 为什么 sparse MLA 对长上下文很重要？

| 场景          | 普通 MHA | Sparse MLA |
| ----------- | ------ | ---------- |
| 32k prefill | O(N²)  | 近似 O(N)    |
| KV cache    | 巨大     | 压缩         |
| 带宽          | 爆      | 可控         |

---

## 和 NSA 的关系（关键）

> **NSA 是“怎么并行算 attention”，
> Sparse MLA 是“算哪些 attention”。**

在 sglang / TRT-LLM 上：

* NSA backend + sparse MLA
* FlashMLA / FlashAttention MLA kernel
* H200 上是当前最强组合

---

# 5️⃣ 三者放在一起：完整层级关系图

```
Attention family
│
├─ Standard MHA
│   ├─ chunked MHA (paged attention)
│   └─ one-shot MHA   ← 短序列最优
│
├─ NSA backend (sglang)
│   ├─ parallel chunk attention
│   └─ long-context prefill optimized
│
└─ Sparse MLA (DeepSeek-V3.x)
    ├─ reduced KV
    └─ long-context friendly
```

# Data Parallelism Attention For DeepSeek Models

https://lmsys.org/blog/2024-12-04-sglang-v0-4/#data-parallelism-attention-for-deepseek-models

## 先给一句话版结论（通俗版）

> **DeepSeek 的注意力（MLA）结构很特殊，用传统的“每张卡分一半模型”的 TP 方式，会白白把 KV cache 复制很多份，浪费显存；
> sglang 改成“注意力阶段用 DP（分请求），后面的 MoE 再合起来算”，
> 这样显存省很多，可以同时服务更多请求，所以吞吐更高。**

## 1.1 什么是 Tensor Parallelism（TP）？（类比）

想象你有一本**很厚的书（模型）**：

* TP = **把每一页撕开**
* 8 张 GPU：每张负责 1/8 的页
* 每个请求：**8 张卡一起算一个请求**

这是现在最常见的推理方式。

---

## 1.2 问题来了：DeepSeek 的 MLA 很“怪”

DeepSeek 的注意力不是普通 MHA，而是 **MLA**，它有两个关键特性：

1️⃣ **KV head 非常少（甚至只有 1 个）**
2️⃣ KV cache 是共享 latent 的，不是每个 head 一份

### 这在 TP 下会发生什么？

假设：

* 你有 **1 份 KV cache**
* TP=8

👉 **这 1 份 KV cache 会被复制 8 份**

```
GPU0: KV
GPU1: KV
GPU2: KV
...
GPU7: KV
```

⚠️ 但其实：

* 每张卡用的 KV 是**一模一样的**
* 复制只是因为 TP 的计算方式

> **这就是“unwanted memory usage”**

---

### 一个直观比喻

就像：

* 一个会议室只有 **1 份会议纪要**
* 你却给 8 个人 **各复印一份**
* 结果打印机（显存）爆了

---

# 2️⃣ 新思路：注意力阶段，不用 TP，用 DP

## 2.1 Data Parallelism（DP）在这里是什么意思？

不是训练里的 DP。

这里的 DP 意思是：

> **不同 GPU 处理不同请求，而不是一起处理同一个请求**

也就是：

| 模式 | 每张卡在干嘛          |
| -- | --------------- |
| TP | 8 张卡一起算 *同一个请求* |
| DP | 每张卡算 *不同请求*     |

---

## 2.2 把注意力阶段换成 DP，会发生什么？

### 对 MLA 来说，这是“天作之合”

* MLA 的 KV cache：

  * 本来就是 **一份就够**
* DP 后：

  * **每个请求只存 1 份 KV**
  * 不再因为 TP 被复制

结果：

✅ **KV cache 直接缩小 ~TP 倍（比如 8×）**
✅ 显存省出来
✅ 能同时跑 **更多请求（更大 batch）**

---

## 3️⃣ 那模型后半部分怎么办？（MoE 怎么算？）

你可能会问一个很关键的问题：

> “注意力用 DP 分开算了，那后面的 MoE 层不是乱了吗？”

这正是这段话后半段在说的。

---

## 4️⃣ sglang 的做法（一步步走）

我用流程图式语言讲：

---

### 🔹 Step 1：Attention 阶段（DP）

* GPU0：处理一批请求（prefill / decode）
* GPU1：处理另一批请求
* …
* GPU7：处理自己的请求

👉 **每张卡都有自己的一批 KV cache**
👉 **没有重复**

---

### 🔹 Step 2：进入 MoE 之前 → All-Gather

MoE 的特点是：

* expert 分布在不同 GPU 上
* 一个 token 可能要去“别的 GPU 的 expert”

所以 sglang 做：

> **把 attention 算完的结果，先 all-gather 到所有 GPU**

就像：

> “大家先把各自的作业抄一份，发给所有人”

---

### 🔹 Step 3：MoE 层（正常工作）

* 各个 GPU 上的 expert 各自处理该处理的 token
* 这是 MoE 天然擅长的部分

---

### 🔹 Step 4：MoE 结束后 → 再分发回去

* 把 token 的结果：

  * 再发回原来处理这个请求的 GPU

于是：

* 请求还是回到“原来的卡”
* decode / 下一个 step 继续走 DP attention

---

## 5️⃣ 关键点：为什么这能提升吞吐？

### 原因 1：KV cache 大幅减少

* TP：KV × 8
* DP：KV × 1

👉 显存省下来 = **batch size 可以变大**

---

### 原因 2：attention 本身更容易 scale

* Attention 是 memory-heavy
* DP 更适合 memory-heavy 算子
* 不用频繁 all-reduce

---

### 原因 3：MoE 本来就需要通信

* MoE 的 all-gather 是“必须的”
* attention 阶段顺便借用这个通信点
* 整体通信次数 **反而更少**

---

## 6️⃣ 一句话把整段话“翻译成人话”

我帮你把原文翻译成工程师能听懂的一句话：

> DeepSeek 的 MLA 注意力 KV 很小，用 TP 会被无意义复制。
> sglang 把注意力阶段改成 DP，每张卡处理不同请求，KV 只存一份；
> 到 MoE 前再统一通信，这样显存占用更低、batch 更大、吞吐更高。

---

## 7️⃣ 你在 benchmark 里已经“间接看到”这个效果了

你之前的数据里：

* sglang 在：

  * random
  * 长 prefill
  * batch 稳定

吞吐明显更高

👉 **这正是“KV cache 省出来 → batch 变大”的直接体现**

---

## 如果你愿意，我可以下一步帮你：

1️⃣ 用一张**对比表**：TP attention vs DP attention（显存/吞吐）
2️⃣ 结合你 **8×H200** 算一个「理论最大 batch 提升倍数」
3️⃣ 解释为什么 **vLLM 目前很难做同样的事情**

你选一个，我继续。
