#!/usr/bin/env python3
"""
Simple PDF to Markdown converter using marker
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

# Configuration
PAPERS_DIR = Path('papers')
MARKDOWN_DIR = Path('markdown_papers')
CHECKPOINT_FILE = Path('simple_checkpoint.json')

def load_checkpoint():
    """Load checkpoint"""
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE, 'r') as f:
            return json.load(f)
    return {'completed': [], 'failed': {}}

def save_checkpoint(checkpoint):
    """Save checkpoint"""
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(checkpoint, f, indent=2)

def check_converted(pdf_path):
    """Check if PDF already converted"""
    output_dir = MARKDOWN_DIR / pdf_path.stem
    md_file = output_dir / f"{pdf_path.stem}.md"
    return md_file.exists() and md_file.stat().st_size > 0

def convert_one_by_one(pdf_files):
    """Convert PDFs one by one"""
    checkpoint = load_checkpoint()
    
    # Load API key from environment
    if os.path.exists('.env'):
        with open('.env') as f:
            for line in f:
                if 'GEMINI_API_KEYS=' in line and '=' in line:
                    keys = line.split('=', 1)[1].strip().strip('"').strip("'").split(',')
                    if keys and keys[0]:
                        os.environ['GOOGLE_API_KEY'] = keys[0].strip()
                        print(f"Using API key: {keys[0][:8]}...")
    
    pending = []
    for pdf in pdf_files:
        if str(pdf) not in checkpoint['completed'] or not check_converted(pdf):
            pending.append(pdf)
    
    print(f"Found {len(pending)} pending PDFs to convert")
    
    completed = len(checkpoint['completed'])
    failed = len(checkpoint.get('failed', {}))
    
    for i, pdf in enumerate(pending, 1):
        print(f"\n[{i}/{len(pending)}] Converting: {pdf.name} ({pdf.stat().st_size / 1024 / 1024:.1f}MB)")
        
        # Create temp directory for this single file
        import time
        temp_dir = MARKDOWN_DIR / f"temp_{int(time.time())}"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Copy PDF to temp directory
            import shutil
            shutil.copy2(pdf, temp_dir / pdf.name)
            
            # Run marker on single file
            cmd = f"./venv/bin/marker {temp_dir} --output_dir {MARKDOWN_DIR} --max_files 1 --extract_images true --format_lines"
            
            print(f"Running marker...")
            
            start_time = time.time()
            result = os.system(cmd)
            duration = time.time() - start_time
            
            if result == 0 and check_converted(pdf):
                print(f"✓ Converted successfully in {duration:.1f}s")
                checkpoint['completed'].append(str(pdf))
                completed += 1
            else:
                print(f"✗ Failed with exit code: {result}")
                if 'failed' not in checkpoint:
                    checkpoint['failed'] = {}
                checkpoint['failed'][str(pdf)] = f"Exit code: {result}"
                failed += 1
        
        except Exception as e:
            print(f"✗ Error: {e}")
            if 'failed' not in checkpoint:
                checkpoint['failed'] = {}
            checkpoint['failed'][str(pdf)] = str(e)
            failed += 1
        
        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
            save_checkpoint(checkpoint)
            
        # Progress
        total_processed = completed + failed
        percent = (total_processed / len(pdf_files)) * 100
        print(f"Progress: {percent:.1f}% ({total_processed}/{len(pdf_files)}) | ✓ {completed} | ✗ {failed}")
        
        # Small delay between files
        if i < len(pending):
            time.sleep(1)

def main():
    """Main entry point"""
    print("="*70)
    print("Simple One-by-One PDF Converter")
    print("="*70)
    
    # Get all PDFs
    pdf_files = list(PAPERS_DIR.glob('*.pdf'))
    pdf_files = [p for p in pdf_files if p.stat().st_size >= 100 * 1024]  # Min 100KB
    pdf_files.sort(key=lambda p: p.stat().st_size)  # Start with smaller files
    
    print(f"Found {len(pdf_files)} PDFs to convert")
    
    # Convert one by one
    convert_one_by_one(pdf_files)

if __name__ == "__main__":
    main()