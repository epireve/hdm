#!/usr/bin/env python3
"""
Image compression script for markdown_papers directory.
Compresses PNG and JPEG images to reduce repository size.
"""

import os
import sys
from PIL import Image
import concurrent.futures
from pathlib import Path
import logging

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('image_compression.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def compress_image(image_path, quality=70, max_width=1200):
    """
    Compress a single image file.
    
    Args:
        image_path (Path): Path to the image file
        quality (int): JPEG quality (1-100)
        max_width (int): Maximum width in pixels
    
    Returns:
        tuple: (original_size, new_size, success)
    """
    try:
        original_size = os.path.getsize(image_path)
        
        # Skip if file is already small
        if original_size < 50000:  # 50KB
            return original_size, original_size, True
            
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Resize if too large
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # Save with compression
            if image_path.suffix.lower() in ['.png']:
                # Convert PNG to JPEG for better compression
                new_path = image_path.with_suffix('.jpg')
                img.save(new_path, 'JPEG', quality=quality, optimize=True)
                os.remove(image_path)
                image_path = new_path
            else:
                # Compress existing JPEG
                img.save(image_path, 'JPEG', quality=quality, optimize=True)
        
        new_size = os.path.getsize(image_path)
        return original_size, new_size, True
        
    except Exception as e:
        logger.error(f"Error compressing {image_path}: {e}")
        return original_size, original_size, False

def find_images(directory):
    """Find all image files in directory."""
    image_extensions = {'.png', '.jpg', '.jpeg'}
    image_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if Path(file).suffix.lower() in image_extensions:
                image_files.append(Path(root) / file)
    
    return image_files

def compress_images_parallel(image_files, max_workers=4):
    """Compress images using parallel processing."""
    total_original = 0
    total_compressed = 0
    successful = 0
    failed = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(compress_image, img_file): img_file 
                         for img_file in image_files}
        
        for i, future in enumerate(concurrent.futures.as_completed(future_to_file)):
            img_file = future_to_file[future]
            try:
                original_size, new_size, success = future.result()
                total_original += original_size
                total_compressed += new_size
                
                if success:
                    successful += 1
                    if i % 100 == 0:  # Progress update every 100 files
                        logger.info(f"Processed {i+1}/{len(image_files)} images")
                else:
                    failed += 1
                    
            except Exception as e:
                logger.error(f"Error processing {img_file}: {e}")
                failed += 1
    
    return total_original, total_compressed, successful, failed

def main():
    """Main compression function."""
    global logger
    logger = setup_logging()
    
    markdown_papers_dir = Path("markdown_papers")
    
    if not markdown_papers_dir.exists():
        logger.error("markdown_papers directory not found!")
        return 1
    
    logger.info("Finding all images in markdown_papers...")
    image_files = find_images(markdown_papers_dir)
    logger.info(f"Found {len(image_files)} image files")
    
    if not image_files:
        logger.info("No images found to compress")
        return 0
    
    logger.info("Starting compression...")
    original_total, compressed_total, successful, failed = compress_images_parallel(image_files)
    
    # Calculate savings
    saved_bytes = original_total - compressed_total
    saved_mb = saved_bytes / (1024 * 1024)
    compression_ratio = (saved_bytes / original_total) * 100 if original_total > 0 else 0
    
    logger.info("=" * 50)
    logger.info("COMPRESSION RESULTS")
    logger.info("=" * 50)
    logger.info(f"Total images processed: {len(image_files)}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Original size: {original_total / (1024*1024):.1f} MB")
    logger.info(f"Compressed size: {compressed_total / (1024*1024):.1f} MB")
    logger.info(f"Space saved: {saved_mb:.1f} MB ({compression_ratio:.1f}%)")
    logger.info("=" * 50)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())