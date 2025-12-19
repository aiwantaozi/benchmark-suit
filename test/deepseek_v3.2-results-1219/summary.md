
## (1218)Total Token Throughput Per Second Summary

vLLM: vllm-0.13.0rc2
Sglang: 0.5.6.post2

| engine | base-sharegpt | base-random-128 | base-random-2k | base-random-4k | base-random-32k | base-ramdom-2k-output | mtp-sharegpt(step1/step3)) | disable-deepgemm-sharegpt |            cp |
| ------ | ------------: | --------------: | -------------: | -------------: | --------------: | --------------------: | -------------------------: | ------------------------: | ------------: |
| vllm   |          5247 |           11726 |          11260 |           9986 |            9858 |                  3106 |         5593(+6.6%)/Failed |               4884(-6.9%) | not supported |
| sglang |          3012 |           12950 |          20582 |          10946 |           10015 |                  3558 |                  1481/1720 |                    failed |        failed |
| diff   |        -42.6% |          +10.4% |         +82.8% |          +9.6% |           +1.6% |                +14.5% |              -73.5%/Failed |                    Failed |           N/A |

## (1219) 

vLLM: vllm-0.13.0
Sglang: 0.5.6.post2