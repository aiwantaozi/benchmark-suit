
#!/bin/bash

download_shareGPT() {
    local url="https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/resolve/main/ShareGPT_V3_unfiltered_cleaned_split.json"
    local file="ShareGPT_V3_unfiltered_cleaned_split.json"

    if [[ -f "$file" ]]; then
        echo "ShareGPT dataset already exists, skip downloading: $file"
        return 0
    fi

    echo "Downloading ShareGPT dataset..."
    wget -O "$file" "$url" || {
        echo "Failed to download ShareGPT dataset" >&2
        return 1
    }
}

download_shareGPT
