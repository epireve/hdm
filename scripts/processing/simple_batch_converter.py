#!/usr/bin/env python3
"""
Simple batch converter using os.system to call marker
"""

import os
import sys
import json
import time
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
PAPERS_DIR = Path('papers')
MARKDOWN_DIR = Path('markdown_papers')
BATCH_SIZE = 5  # Process 5 files at a time
CHECKPOINT_FILE = Path('simple_batch_checkpoint.json')

def load_checkpoint():
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE, 'r') as f:
            return json.load(f)
    return {'completed': [], 'failed': {}}

def save_checkpoint(checkpoint):
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(checkpoint, f, indent=2)

def check_conversion(pdf_path):
    """Check if PDF has been converted"""
    output_dir = MARKDOWN_DIR / pdf_path.stem
    md_file = output_dir / f"{pdf_path.stem}.md"
    return output_dir.exists() and md_file.exists() and md_file.stat().st_size > 0

def main():
    print(f"{'='*70}")
    print("PDF to Markdown Batch Converter")
    print(f"{'='*70}")
    
    # Load environment
    if os.path.exists('.env'):
        with open('.env') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"').strip("'")
    
    # Set API key
    if 'GEMINI_API_KEYS' in os.environ:
        api_key = os.environ['GEMINI_API_KEYS'].split(',')[0].strip()
        os.environ['GOOGLE_API_KEY'] = api_key
        print(f"Using API key: {api_key[:8]}...")
    
    # Get PDFs
    pdf_files = list(PAPERS_DIR.glob('*.pdf'))
    pdf_files = [p for p in pdf_files if p.stat().st_size >= 100 * 1024]
    pdf_files.sort(key=lambda p: p.stat().st_size)  # Start with smaller files
    
    print(f"Found {len(pdf_files)} PDFs (>= 100KB)")
    
    # Load checkpoint
    checkpoint = load_checkpoint()
    
    # Filter pending files
    pending = []
    for pdf in pdf_files:
        if str(pdf) not in checkpoint['completed']:
            if not check_conversion(pdf):
                pending.append(pdf)
            else:
                # Add to completed if already converted
                checkpoint['completed'].append(str(pdf))
    
    save_checkpoint(checkpoint)
    print(f"Pending: {len(pending)} files")
    
    if not pending:
        print("All files already converted!")
        return
    
    # Process in batches
    batch_num = 1
    total_converted = len(checkpoint['completed'])
    
    for i in range(0, len(pending), BATCH_SIZE):
        batch = pending[i:i+BATCH_SIZE]
        
        print(f"\n{'='*70}")
        print(f"BATCH {batch_num}: Processing {len(batch)} files")
        print(f"{'='*70}")
        
        # Create batch directory
        batch_dir = Path(f"batch_{batch_num}_{int(time.time())}")
        batch_dir.mkdir(exist_ok=True)
        
        try:
            # Copy files
            for pdf in batch:
                shutil.copy2(pdf, batch_dir / pdf.name)
                print(f"  - {pdf.name} ({pdf.stat().st_size / 1024 / 1024:.1f}MB)")
            
            # Run marker using os.system
            cmd = f"./venv/bin/marker {batch_dir} --output_dir {MARKDOWN_DIR} --max_files {len(batch)} --extract_images true --format_lines"
            print(f"\nRunning: {cmd}")
            
            start_time = time.time()
            result = os.system(cmd)
            duration = time.time() - start_time
            
            if result == 0:
                print(f"✓ Batch completed in {duration:.1f}s")
                
                # Check conversions
                for pdf in batch:
                    if check_conversion(pdf):
                        checkpoint['completed'].append(str(pdf))
                        total_converted += 1
                        print(f"  ✓ {pdf.name}")
                    else:
                        checkpoint['failed'][str(pdf)] = "Conversion failed"
                        print(f"  ✗ {pdf.name}")
            else:
                print(f"✗ Batch failed with code {result}")
                for pdf in batch:
                    checkpoint['failed'][str(pdf)] = f"Batch failed with code {result}"
            
            save_checkpoint(checkpoint)
            
        finally:
            # Cleanup
            shutil.rmtree(batch_dir, ignore_errors=True)
        
        # Progress
        percent = (total_converted / len(pdf_files)) * 100
        print(f"\nProgress: {percent:.1f}% ({total_converted}/{len(pdf_files)})")
        
        batch_num += 1
        
        # Small delay
        if i + BATCH_SIZE < len(pending):
            print("Waiting 2 seconds...")
            time.sleep(2)
    
    # Summary
    print(f"\n{'='*70}")
    print(f"CONVERSION COMPLETE")
    print(f"Total: {len(pdf_files)} files")
    print(f"Converted: {len(checkpoint['completed'])}")
    print(f"Failed: {len(checkpoint['failed'])}")
    print(f"Output: {MARKDOWN_DIR}")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()