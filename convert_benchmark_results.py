#!/usr/bin/env python3
import json
import argparse
from pathlib import Path

TEMPLATE = """============ Serving Benchmark Result ============
Successful requests:                     {completed}
Benchmark duration (s):                  {duration:.2f}
Total input tokens:                      {total_input_tokens}
Total generated tokens:                  {total_output_tokens}
Request throughput (req/s):              {request_throughput:.2f}
Output token throughput (tok/s):         {output_throughput:.2f}
Peak output token throughput (tok/s):    {max_output_tokens_per_s:.2f}
Peak concurrent requests:                {max_concurrent_requests:.2f}
Total Token throughput (tok/s):          {total_token_throughput:.2f}
---------------Time to First Token----------------
Mean TTFT (ms):                          {mean_ttft_ms:.2f}
Median TTFT (ms):                        {median_ttft_ms:.2f}
P99 TTFT (ms):                           {p99_ttft_ms:.2f}
-----Time per Output Token (excl. 1st token)------
Mean TPOT (ms):                          {mean_tpot_ms:.2f}
Median TPOT (ms):                        {median_tpot_ms:.2f}
P99 TPOT (ms):                           {p99_tpot_ms:.2f}
---------------Inter-token Latency----------------
Mean ITL (ms):                           {mean_itl_ms:.2f}
Median ITL (ms):                         {median_itl_ms:.2f}
P99 ITL (ms):                            {p99_itl_ms:.2f}
==================================================
"""

def convert_file(json_path: Path, output_dir: Path):
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    text = TEMPLATE.format(
        completed=data.get("completed", 0),
        duration=data.get("duration", 0.0),
        total_input_tokens=data.get("total_input_tokens", 0),
        total_output_tokens=data.get("total_output_tokens", 0),
        request_throughput=float(data.get("request_throughput", 0.0)),
        output_throughput=float(data.get("output_throughput", 0.0)),
        max_output_tokens_per_s=float(data.get("max_output_tokens_per_s", 0.0)),
        max_concurrent_requests=float(data.get("max_concurrent_requests", 0.0)),
        total_token_throughput=float(data.get("total_token_throughput", 0.0)),
        mean_ttft_ms=float(data.get("mean_ttft_ms", 0.0)),
        median_ttft_ms=float(data.get("median_ttft_ms", 0.0)),
        p99_ttft_ms=float(data.get("p99_ttft_ms", 0.0)),
        mean_tpot_ms=float(data.get("mean_tpot_ms", 0.0)),
        median_tpot_ms=float(data.get("median_tpot_ms", 0.0)),
        p99_tpot_ms=float(data.get("p99_tpot_ms", 0.0)),
        mean_itl_ms=float(data.get("mean_itl_ms", 0.0)),
        median_itl_ms=float(data.get("median_itl_ms", 0.0)),
        p99_itl_ms=float(data.get("p99_itl_ms", 0.0)),
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / (json_path.stem + ".txt")
    out_path.write_text(text, encoding="utf-8")
    print(f"[OK] {json_path} -> {out_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert vLLM benchmark JSON files to Serving Benchmark Result text format"
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Input JSON file paths"
    )
    parser.add_argument(
        "-o", "--output-dir",
        required=True,
        help="Output directory for .txt files"
    )

    args = parser.parse_args()
    output_dir = Path(args.output_dir)

    for inp in args.inputs:
        convert_file(Path(inp), output_dir)

if __name__ == "__main__":
    main()

# Example usage:
# python convert_benchmark.py \
#   vllm_tp_sharegpt.json \
#   vllm_tp_short.json \
#   -o converted_results
