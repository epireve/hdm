#!/usr/bin/env python3
"""
Smart PDF converter for new_papers folder with status display and file validation
"""

import os
import json
import time
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# Setup
PAPERS_DIR = Path('new_papers')  # Changed from 'papers' to 'new_papers'
MARKDOWN_DIR = Path('markdown_papers')
CHECKPOINT_FILE = Path('new_papers_checkpoint.json')  # Separate checkpoint for new papers

def load_checkpoint():
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE) as f:
            return json.load(f)
    return {'completed': [], 'failed': {}, 'skipped': []}

def save_checkpoint(checkpoint):
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(checkpoint, f, indent=2)

def check_converted(pdf_path):
    """Check if PDF already converted"""
    output_dir = MARKDOWN_DIR / pdf_path.stem
    md_file = output_dir / "paper.md"  # Changed to use standardized name
    return md_file.exists() and md_file.stat().st_size > 0

def is_valid_pdf(pdf_path):
    """Check if file is actually a PDF"""
    try:
        result = subprocess.run(['file', str(pdf_path)], capture_output=True, text=True)
        # Check if it's HTML or not a PDF
        if 'HTML' in result.stdout or 'PDF' not in result.stdout:
            return False
        return True
    except:
        # Try reading first few bytes
        try:
            with open(pdf_path, 'rb') as f:
                header = f.read(10)
                # PDF files start with %PDF
                return header.startswith(b'%PDF')
        except:
            return True  # Assume valid if can't check

def display_status(checkpoint, total_pdfs, current_pdf=None, current_status=None):
    """Display current status"""
    os.system('clear')
    
    completed = len(checkpoint['completed'])
    failed = len(checkpoint.get('failed', {}))
    skipped = len(checkpoint.get('skipped', []))
    remaining = total_pdfs - completed - failed - skipped
    percent = ((completed + skipped) / total_pdfs * 100) if total_pdfs > 0 else 0
    
    # Header
    print("="*70)
    print("PDF TO MARKDOWN CONVERTER - NEW PAPERS")
    print("="*70)
    
    # Stats
    print(f"Total PDFs: {total_pdfs}")
    print(f"Converted: {completed} ✓")
    print(f"Skipped (already done): {skipped} ⏭")
    print(f"Failed: {failed} ✗")
    print(f"Remaining: {remaining}")
    
    # Progress bar
    bar_length = 50
    filled = int(bar_length * percent / 100)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"\nProgress: [{bar}] {percent:.1f}%")
    
    # Speed estimate
    if completed > 0 and hasattr(display_status, 'start_time'):
        elapsed = time.time() - display_status.start_time
        rate = completed / elapsed
        if rate > 0:
            eta_seconds = remaining / rate
            eta_minutes = int(eta_seconds / 60)
            print(f"Speed: {rate:.1f} files/min | ETA: {eta_minutes} minutes")
    
    # Current file
    if current_pdf:
        print(f"\nCurrent: {current_pdf}")
        print(f"Status: {current_status}")
    
    # Recent activity
    if checkpoint['completed']:
        print("\nRecent conversions:")
        for pdf in checkpoint['completed'][-3:]:
            print(f"  ✓ {Path(pdf).name}")
    
    print("="*70)

def standardize_files(output_dir):
    """Standardize file names after conversion"""
    # Find the markdown file
    md_files = list(output_dir.glob('*.md'))
    if md_files:
        # Rename to paper.md
        md_file = md_files[0]
        new_md = output_dir / 'paper.md'
        if md_file != new_md:
            md_file.rename(new_md)
    
    # Find the metadata file
    json_files = list(output_dir.glob('*_meta.json'))
    if json_files:
        # Rename to metadata.json
        json_file = json_files[0]
        new_json = output_dir / 'metadata.json'
        json_file.rename(new_json)

def main():
    print("Initializing PDF Converter for new_papers folder...")
    
    # Check if new_papers directory exists
    if not PAPERS_DIR.exists():
        print(f"Error: {PAPERS_DIR} directory not found!")
        return
    
    # Load API key
    if os.path.exists('.env'):
        with open('.env') as f:
            for line in f:
                if 'GEMINI_API_KEYS=' in line:
                    keys = line.split('=')[1].strip().split(',')
                    if keys:
                        os.environ['GOOGLE_API_KEY'] = keys[0].strip()
    
    # Get PDFs
    pdfs = sorted([p for p in PAPERS_DIR.glob('*.pdf')], 
                  key=lambda x: x.stat().st_size)
    total_pdfs = len(pdfs)
    
    print(f"Found {total_pdfs} PDF files in {PAPERS_DIR}")
    
    # Load checkpoint
    checkpoint = load_checkpoint()
    
    # Set start time for speed calculation
    display_status.start_time = time.time()
    
    # First pass: skip already converted files
    print("Scanning for existing conversions...")
    for pdf in pdfs:
        if check_converted(pdf):
            if str(pdf) not in checkpoint['completed'] and str(pdf) not in checkpoint.get('skipped', []):
                checkpoint['skipped'].append(str(pdf))
    
    save_checkpoint(checkpoint)
    
    # Process remaining files
    for pdf in pdfs:
        # Skip if already done
        if str(pdf) in checkpoint['completed'] or str(pdf) in checkpoint.get('skipped', []):
            continue
        
        # Check if it's a real PDF
        if not is_valid_pdf(pdf):
            display_status(checkpoint, total_pdfs, pdf.name, "HTML file (not PDF) - skipping")
            if 'html_files' not in checkpoint:
                checkpoint['html_files'] = []
            checkpoint['html_files'].append(str(pdf))
            save_checkpoint(checkpoint)
            time.sleep(1)
            continue
        
        # Update display
        display_status(checkpoint, total_pdfs, pdf.name, "Starting conversion...")
        
        # Create temp dir with unique name
        import random
        temp_dir = Path(f"temp_{int(time.time())}_{random.randint(1000, 9999)}")
        temp_dir.mkdir(exist_ok=True)
        
        try:
            # Copy PDF
            shutil.copy2(pdf, temp_dir)
            
            # Run marker (suppress output)
            cmd = f"./venv/bin/marker {temp_dir} --output_dir {MARKDOWN_DIR} --max_files 1 >/dev/null 2>&1"
            
            start = time.time()
            result = os.system(cmd)
            duration = time.time() - start
            
            # Check if conversion succeeded
            output_dir = MARKDOWN_DIR / pdf.stem
            if result == 0 and output_dir.exists():
                # Standardize file names
                standardize_files(output_dir)
                
                # Verify standardized files exist
                if (output_dir / 'paper.md').exists():
                    checkpoint['completed'].append(str(pdf))
                    status = f"✓ Converted in {duration:.1f}s"
                else:
                    checkpoint['failed'][str(pdf)] = "Conversion succeeded but standardization failed"
                    status = f"✗ Standardization failed"
            else:
                checkpoint['failed'][str(pdf)] = f"Conversion failed (code: {result})"
                status = f"✗ Failed"
                
        except Exception as e:
            checkpoint['failed'][str(pdf)] = str(e)
            status = f"✗ Error: {e}"
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
            save_checkpoint(checkpoint)
            
        display_status(checkpoint, total_pdfs, pdf.name, status)
        time.sleep(0.5)
    
    # Final display
    display_status(checkpoint, total_pdfs, None, "COMPLETE!")
    
    # Summary
    print(f"\nConversion complete at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Successfully converted: {len(checkpoint['completed'])} files")
    print(f"Already existed: {len(checkpoint.get('skipped', []))} files")
    print(f"Failed: {len(checkpoint.get('failed', {}))} files")
    
    if checkpoint.get('failed'):
        print("\nFailed files:")
        for pdf, error in list(checkpoint['failed'].items())[:10]:
            print(f"  - {Path(pdf).name}: {error}")
    
    # List successfully converted folders
    if checkpoint['completed']:
        print("\nNewly converted papers (folders created):")
        for pdf_path in checkpoint['completed'][-10:]:  # Show last 10
            folder_name = Path(pdf_path).stem
            print(f"  - markdown_papers/{folder_name}/")

if __name__ == "__main__":
    main()