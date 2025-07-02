#!/bin/bash

# Script to run image descriptor with API key setup

echo "==================================="
echo "Image Description Generator Setup"
echo "==================================="

# Check if API key is provided as argument
if [ -n "$1" ]; then
    export GOOGLE_API_KEY="$1"
    echo "✓ API key provided"
else
    # Check if already set in environment
    if [ -z "$GOOGLE_API_KEY" ]; then
        echo "❌ GOOGLE_API_KEY not found"
        echo ""
        echo "Please provide your Gemini API key:"
        echo "1. Get key from: https://makersuite.google.com/app/apikey"
        echo "2. Run: ./run_image_descriptor.sh YOUR_API_KEY"
        echo ""
        echo "Or set it in your environment:"
        echo "export GOOGLE_API_KEY='your-api-key-here'"
        exit 1
    else
        echo "✓ Using existing GOOGLE_API_KEY from environment"
    fi
fi

# Estimate cost
echo ""
echo "Estimating processing scope..."
python3 -c "
import json
from pathlib import Path

mapping_file = Path('cite_key_mapping.json')
if mapping_file.exists():
    with open(mapping_file) as f:
        data = json.load(f)
    
    total_images = data['statistics']['images_to_keep']
    papers_with_images = sum(1 for p in data['papers'].values() if p.get('images', {}).get('keep'))
    
    print(f'Papers with images: {papers_with_images}')
    print(f'Total images to describe: {total_images}')
    print(f'Estimated cost: ~\${total_images * 0.0001:.2f} (at ~\$0.0001 per image)')
    print(f'Estimated time: ~{total_images * 0.5 / 60:.1f} minutes (with rate limiting)')
else:
    print('cite_key_mapping.json not found. Run paper analysis first.')
"

echo ""
echo "Choose processing mode:"
echo "1. Test mode (5 papers)"
echo "2. Full mode (all papers)"
echo ""
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "Running in TEST mode..."
        python scripts/phase2/run_phase2_csv.py --test --step describe-images
        ;;
    2)
        echo ""
        echo "Running in FULL mode..."
        echo "This will process all images. Continue? (y/n)"
        read -p "> " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            python scripts/phase2/run_phase2_csv.py --full --step describe-images
        else
            echo "Cancelled."
        fi
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac