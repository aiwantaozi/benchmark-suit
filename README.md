# benchmark-suit

## Environment

### Setup deepgemm

- **DeepGEMM**: The [DeepGEMM](https://github.com/deepseek-ai/DeepGEMM) kernel library optimized for FP8 matrix multiplications.

#### SGLang

apt update
apt install -y libnuma1 libnuma-dev
pip install --upgrade sgl_kernel

**Usage**: The activation and weight optimization above are turned on by default for DeepSeek V3 models. DeepGEMM is enabled by default on NVIDIA Hopper/Blackwell GPUs and disabled by default on other devices. DeepGEMM can also be manually turned off by setting the environment variable `SGLANG_ENABLE_JIT_DEEPGEMM=0`.

```{tip}
Before serving the DeepSeek model, precompile the DeepGEMM kernels to improve first-run performance. The precompilation process typically takes around 10 minutes to complete.
```

```bash
python3 -m sglang.compile_deep_gemm --model deepseek-ai/DeepSeek-V3 --tp 8 --trust-remote-code
```

#### vLLM

```bash
install_deepgemm.sh
```

#### tensorRT

deepgemm
https://github.com/NVIDIA/TensorRT-LLM/blob/main/examples/models/core/deepseek_v3/README.md#deepgemm

####
tensortt