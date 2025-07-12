#!/bin/bash
# Simple batch converter using marker directly

# Load environment variables
source .env

# Set first API key
export GOOGLE_API_KEY="${GEMINI_API_KEYS%%,*}"

# Create batch directory
BATCH_DIR="current_batch_$$"
mkdir -p "$BATCH_DIR"

# Function to process a batch
process_batch() {
    local batch_num=$1
    shift
    local files=("$@")
    
    echo "========================================================================"
    echo "BATCH $batch_num: Processing ${#files[@]} files"
    echo "========================================================================"
    
    # Copy files to batch directory
    for file in "${files[@]}"; do
        cp "$file" "$BATCH_DIR/"
        echo "  - $(basename "$file")"
    done
    
    # Run marker
    echo "Running marker..."
    ./venv/bin/marker "$BATCH_DIR" \
        --output_dir markdown_papers \
        --max_files ${#files[@]} \
        --extract_images true \
        --format_lines
    
    # Clean batch directory
    rm -rf "$BATCH_DIR"/*
    
    echo "Batch $batch_num complete"
    echo ""
}

# Get all PDFs sorted by size
echo "Finding PDFs..."
PDF_FILES=()
while IFS= read -r file; do
    PDF_FILES+=("$file")
done < <(find papers -name "*.pdf" -size +100k -type f -exec ls -la {} \; | sort -k5 -n | awk '{print $NF}')

echo "Found ${#PDF_FILES[@]} PDFs (>= 100KB)"

# Process in batches of 10
BATCH_SIZE=10
BATCH_NUM=1

for ((i=0; i<${#PDF_FILES[@]}; i+=BATCH_SIZE)); do
    # Get batch files
    batch_files=("${PDF_FILES[@]:i:BATCH_SIZE}")
    
    # Process batch
    process_batch $BATCH_NUM "${batch_files[@]}"
    
    ((BATCH_NUM++))
    
    # Small delay between batches
    if [ $i -lt $((${#PDF_FILES[@]} - BATCH_SIZE)) ]; then
        echo "Waiting 2 seconds before next batch..."
        sleep 2
    fi
done

# Cleanup
rmdir "$BATCH_DIR" 2>/dev/null

echo "========================================================================"
echo "CONVERSION COMPLETE"
echo "Total files: ${#PDF_FILES[@]}"
echo "Output directory: markdown_papers"
echo "========================================================================"