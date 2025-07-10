#!/usr/bin/env python3
"""
PDF converter with live status display
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

def display_status(checkpoint, total_pdfs, current_pdf=None, current_status=None):
    """Display current status"""
    os.system('clear')  # Clear screen
    
    completed = len(checkpoint['completed'])
    failed = len(checkpoint.get('failed', {}))
    remaining = total_pdfs - completed - failed
    percent = (completed / total_pdfs * 100) if total_pdfs > 0 else 0
    
    # Header
    print("="*70)
    print("PDF TO MARKDOWN CONVERTER - LIVE STATUS")
    print("="*70)
    
    # Overall progress
    print(f"Total PDFs: {total_pdfs}")
    print(f"Completed: {completed} ✓")
    print(f"Failed: {failed} ✗")
    print(f"Remaining: {remaining}")
    
    # Progress bar
    bar_length = 50
    filled = int(bar_length * percent / 100)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"\nProgress: [{bar}] {percent:.1f}%")
    
    # Current file
    if current_pdf:
        print(f"\nCurrently processing: {current_pdf}")
        print(f"Status: {current_status}")
    
    # Recent conversions
    if checkpoint['completed']:
        print("\nLast 5 conversions:")
        for pdf in checkpoint['completed'][-5:]:
            print(f"  ✓ {Path(pdf).name}")
    
    # Failed files
    if checkpoint.get('failed'):
        print(f"\nFailed ({len(checkpoint['failed'])}):")
        for pdf in list(checkpoint['failed'].keys())[-3:]:
            print(f"  ✗ {Path(pdf).name}")
    
    print("="*70)

def main():
    # Load API key from .env
    if os.path.exists('.env'):
        with open('.env') as f:
            for line in f:
                if 'GEMINI_API_KEYS=' in line:
                    keys = line.split('=')[1].strip().split(',')
                    if keys:
                        os.environ['GOOGLE_API_KEY'] = keys[0].strip()
    
    # Get PDFs
    pdfs = sorted([p for p in PAPERS_DIR.glob('*.pdf') if p.stat().st_size >= 100*1024], 
                  key=lambda x: x.stat().st_size)
    total_pdfs = len(pdfs)
    
    # Load checkpoint
    checkpoint = load_checkpoint()
    
    # Initial display
    display_status(checkpoint, total_pdfs)
    time.sleep(2)
    
    # Process each file
    for pdf in pdfs:
        # Skip if already converted (check actual file existence)
        if check_converted(pdf):
            # Add to checkpoint if not already there
            if str(pdf) not in checkpoint['completed']:
                checkpoint['completed'].append(str(pdf))
                save_checkpoint(checkpoint)
            continue
            
        # Update display
        display_status(checkpoint, total_pdfs, pdf.name, "Preparing...")
        
        # Create temp dir
        temp_dir = Path(f"temp_{int(time.time())}")
        temp_dir.mkdir()
        
        try:
            # Copy PDF
            shutil.copy2(pdf, temp_dir)
            
            # Update display
            display_status(checkpoint, total_pdfs, pdf.name, "Converting with marker...")
            
            # Run marker
            cmd = f"./venv/bin/marker {temp_dir} --output_dir {MARKDOWN_DIR} --max_files 1 2>&1"
            
            start = time.time()
            result = os.system(cmd)
            duration = time.time() - start
            
            if result == 0 and check_converted(pdf):
                checkpoint['completed'].append(str(pdf))
                status = f"✓ Success in {duration:.1f}s"
            else:
                if 'failed' not in checkpoint:
                    checkpoint['failed'] = {}
                checkpoint['failed'][str(pdf)] = f"Exit code: {result}"
                status = f"✗ Failed"
                
        except Exception as e:
            if 'failed' not in checkpoint:
                checkpoint['failed'] = {}
            checkpoint['failed'][str(pdf)] = str(e)
            status = f"✗ Error: {e}"
        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
            save_checkpoint(checkpoint)
            
        # Show status briefly
        display_status(checkpoint, total_pdfs, pdf.name, status)
        time.sleep(1)
    
    # Final display
    display_status(checkpoint, total_pdfs, None, "COMPLETE!")
    print(f"\nConversion finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()