
#!/bin/bash

download_shareGPU() {
    echo "Downloading ShareGPU dataset..."
    wget https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/resolve/main/ShareGPT_V3_unfiltered_cleaned_split.json
}

download_shareGPU