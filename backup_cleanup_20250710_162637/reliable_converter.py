#!/usr/bin/env python3
"""
Reliable one-by-one PDF converter that actually works
"""

import os
import json
import time
import shutil
from pathlib import Path
from datetime import datetime

# Setup
PAPERS_DIR = Path('papers')
MARKDOWN_DIR = Path('markdown_papers')
CHECKPOINT_FILE = Path('reliable_checkpoint.json')

def load_checkpoint():
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE) as f:
            return json.load(f)
    return {'completed': [], 'failed': {}}

def save_checkpoint(checkpoint):
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(checkpoint, f, indent=2)

def check_converted(pdf_path):
    """Check if PDF already converted"""
    output_dir = MARKDOWN_DIR / pdf_path.stem
    md_file = output_dir / f"{pdf_path.stem}.md"
    return md_file.exists() and md_file.stat().st_size > 0

def main():
    print("="*60)
    print("RELIABLE PDF CONVERTER")
    print("="*60)
    
    # Load API key from .env
    if os.path.exists('.env'):
        print("Loading .env...")
        os.system('source .env && export GOOGLE_API_KEY=${GEMINI_API_KEYS%%,*}')
        # Manually load for Python
        with open('.env') as f:
            for line in f:
                if 'GEMINI_API_KEYS=' in line:
                    keys = line.split('=')[1].strip().split(',')
                    if keys:
                        os.environ['GOOGLE_API_KEY'] = keys[0].strip()
                        print(f"API key set: {keys[0][:8]}...")
    
    # Get PDFs
    pdfs = sorted([p for p in PAPERS_DIR.glob('*.pdf') if p.stat().st_size >= 100*1024], 
                  key=lambda x: x.stat().st_size)
    print(f"Found {len(pdfs)} PDFs")
    
    # Load checkpoint
    checkpoint = load_checkpoint()
    completed = 0
    failed = 0
    
    # Process each file
    for i, pdf in enumerate(pdfs, 1):
        # Skip if already done
        if str(pdf) in checkpoint['completed'] and check_converted(pdf):
            print(f"[{i}/{len(pdfs)}] ✓ Already done: {pdf.name}")
            completed += 1
            continue
            
        print(f"\n[{i}/{len(pdfs)}] Converting: {pdf.name} ({pdf.stat().st_size/1024/1024:.1f}MB)")
        
        # Create temp dir
        temp_dir = Path(f"temp_{int(time.time())}")
        temp_dir.mkdir()
        
        try:
            # Copy PDF
            shutil.copy2(pdf, temp_dir)
            
            # Run marker directly
            cmd = f"./venv/bin/marker {temp_dir} --output_dir {MARKDOWN_DIR} --max_files 1"
            print("Running marker...")
            
            start = time.time()
            result = os.system(cmd)
            duration = time.time() - start
            
            if result == 0 and check_converted(pdf):
                print(f"✓ Success in {duration:.1f}s")
                checkpoint['completed'].append(str(pdf))
                completed += 1
            else:
                print(f"✗ Failed")
                checkpoint['failed'][str(pdf)] = f"Exit code: {result}"
                failed += 1
                
        except Exception as e:
            print(f"✗ Error: {e}")
            checkpoint['failed'][str(pdf)] = str(e)
            failed += 1
        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
            save_checkpoint(checkpoint)
        
        # Progress
        print(f"Progress: {completed + failed}/{len(pdfs)} (✓{completed} ✗{failed})")
        
        # Small delay
        time.sleep(1)
    
    # Summary
    print("\n" + "="*60)
    print(f"COMPLETE: ✓{completed} ✗{failed} Total:{len(pdfs)}")
    print("="*60)

if __name__ == "__main__":
    main()