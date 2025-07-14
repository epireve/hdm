#!/bin/bash
"""
Image compression script using system tools (ImageMagick/sips).
Compresses PNG and JPEG images to reduce repository size.
"""

# Check if we're on macOS (has sips) or need ImageMagick
if command -v sips >/dev/null 2>&1; then
    COMPRESS_CMD="sips"
    echo "Using macOS sips for image compression"
elif command -v convert >/dev/null 2>&1; then
    COMPRESS_CMD="imagemagick"
    echo "Using ImageMagick for image compression"
else
    echo "No image compression tool found. Please install ImageMagick or use macOS sips"
    exit 1
fi

# Initialize counters
original_size=0
compressed_size=0
processed=0
failed=0

echo "Finding all images in markdown_papers..."
image_count=$(find markdown_papers -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" | wc -l)
echo "Found $image_count image files"

# Process each image
find markdown_papers -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" | while read -r image_file; do
    # Get original size
    orig_size=$(stat -f%z "$image_file" 2>/dev/null || stat -c%s "$image_file" 2>/dev/null)
    original_size=$((original_size + orig_size))
    
    # Skip small files (< 50KB)
    if [ "$orig_size" -lt 50000 ]; then
        continue
    fi
    
    # Compress based on available tool
    if [ "$COMPRESS_CMD" = "sips" ]; then
        # Use macOS sips
        if [[ "$image_file" == *.png ]]; then
            # Convert PNG to JPEG for better compression
            new_file="${image_file%.*}.jpg"
            sips -s format jpeg -s formatOptions 70 "$image_file" --out "$new_file" >/dev/null 2>&1
            if [ $? -eq 0 ]; then
                rm "$image_file"
                image_file="$new_file"
            fi
        else
            # Compress JPEG
            sips -s formatOptions 70 "$image_file" >/dev/null 2>&1
        fi
        
        # Resize if too large
        sips -Z 1200 "$image_file" >/dev/null 2>&1
        
    elif [ "$COMPRESS_CMD" = "imagemagick" ]; then
        # Use ImageMagick
        if [[ "$image_file" == *.png ]]; then
            # Convert PNG to JPEG
            new_file="${image_file%.*}.jpg"
            convert "$image_file" -quality 70 -resize 1200x1200\> "$new_file" 2>/dev/null
            if [ $? -eq 0 ]; then
                rm "$image_file"
                image_file="$new_file"
            fi
        else
            # Compress JPEG
            convert "$image_file" -quality 70 -resize 1200x1200\> "$image_file" 2>/dev/null
        fi
    fi
    
    # Get new size
    new_size=$(stat -f%z "$image_file" 2>/dev/null || stat -c%s "$image_file" 2>/dev/null)
    compressed_size=$((compressed_size + new_size))
    
    processed=$((processed + 1))
    
    # Progress update every 100 files
    if [ $((processed % 100)) -eq 0 ]; then
        echo "Processed $processed images..."
    fi
done

echo "Compression completed!"
echo "Images processed: $processed"