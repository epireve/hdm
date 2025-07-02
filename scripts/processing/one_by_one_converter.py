#!/usr/bin/env python3
"""
One-by-one PDF to Markdown converter
Processes files sequentially for maximum reliability
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
CHECKPOINT_FILE = Path('one_by_one_checkpoint.json')
LOG_FILE = Path('logs') / f'one_by_one_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

# Ensure directories exist
MARKDOWN_DIR.mkdir(exist_ok=True)
LOG_FILE.parent.mkdir(exist_ok=True)

def log(message):
    """Simple logging to both console and file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"{timestamp} - {message}"
    print(log_line)
    with open(LOG_FILE, 'a') as f:
        f.write(log_line + '\n')

def load_checkpoint():
    """Load checkpoint"""
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE, 'r') as f:
            return json.load(f)
    return {
        'completed': [],
        'failed': {},
        'started': datetime.now().isoformat()
    }

def save_checkpoint(checkpoint):
    """Save checkpoint"""
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(checkpoint, f, indent=2)

def check_conversion(pdf_path):
    """Check if PDF has been converted successfully"""
    output_dir = MARKDOWN_DIR / pdf_path.stem
    md_file = output_dir / f"{pdf_path.stem}.md"
    
    if output_dir.exists() and md_file.exists() and md_file.stat().st_size > 0:
        return True, md_file
    
    # Clean up empty directories
    if output_dir.exists() and (not md_file.exists() or md_file.stat().st_size == 0):
        shutil.rmtree(output_dir, ignore_errors=True)
    
    return False, None

def convert_single_pdf(pdf_path, pdf_number, total_pdfs):
    """Convert a single PDF file"""
    log(f"\n[{pdf_number}/{total_pdfs}] Processing: {pdf_path.name} ({pdf_path.stat().st_size / 1024 / 1024:.1f}MB)")
    
    # Check if already converted
    exists, md_path = check_conversion(pdf_path)
    if exists:
        log(f"✓ Already converted: {md_path}")
        return True, None
    
    # Create temp directory for this file
    temp_dir = Path(f"temp_convert_{int(time.time())}")
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # Copy PDF to temp directory
        temp_pdf = temp_dir / pdf_path.name
        shutil.copy2(pdf_path, temp_pdf)
        
        # Build marker command
        cmd = f"./venv/bin/marker {temp_dir} --output_dir {MARKDOWN_DIR} --max_files 1 --extract_images true --format_lines"
        
        log(f"Running marker...")
        start_time = time.time()
        
        # Execute marker using os.system
        result = os.system(cmd)
        duration = time.time() - start_time
        
        if result == 0:
            # Verify conversion
            exists, md_path = check_conversion(pdf_path)
            if exists:
                log(f"✓ Converted successfully in {duration:.1f}s")
                return True, None
            else:
                error = "Output file not created"
                log(f"✗ Failed: {error}")
                return False, error
        else:
            error = f"Marker exited with code {result}"
            log(f"✗ Failed: {error}")
            return False, error
            
    except Exception as e:
        error = str(e)
        log(f"✗ Error: {error}")
        return False, error
    finally:
        # Cleanup temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    """Main conversion process"""
    log("="*70)
    log("One-by-One PDF to Markdown Converter")
    log("="*70)
    
    # Load environment variables from .env
    if os.path.exists('.env'):
        log("Loading environment from .env")
        with open('.env') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"').strip("'")
    
    # Set API key
    if 'GEMINI_API_KEYS' in os.environ and os.environ['GEMINI_API_KEYS']:
        api_keys = os.environ['GEMINI_API_KEYS'].split(',')
        api_key = api_keys[0].strip()
        os.environ['GOOGLE_API_KEY'] = api_key
        log(f"Using Gemini API key: {api_key[:8]}...")
    else:
        log("No API keys found - proceeding without Gemini features")
    
    # Get all PDFs
    pdf_files = list(PAPERS_DIR.glob('*.pdf'))
    pdf_files = [p for p in pdf_files if p.stat().st_size >= 100 * 1024]  # Min 100KB
    pdf_files.sort(key=lambda p: p.stat().st_size)  # Start with smaller files
    
    log(f"Found {len(pdf_files)} PDFs (>= 100KB)")
    
    # Load checkpoint
    checkpoint = load_checkpoint()
    log(f"Checkpoint: {len(checkpoint['completed'])} completed, {len(checkpoint['failed'])} failed")
    
    # Process each file
    completed = len(checkpoint['completed'])
    failed = len(checkpoint['failed'])
    
    for i, pdf in enumerate(pdf_files, 1):
        # Skip if already processed
        if str(pdf) in checkpoint['completed']:
            exists, _ = check_conversion(pdf)
            if exists:
                log(f"[{i}/{len(pdf_files)}] Skipping completed: {pdf.name}")
                continue
            else:
                # Remove from checkpoint if file doesn't exist
                checkpoint['completed'].remove(str(pdf))
                save_checkpoint(checkpoint)
        
        if str(pdf) in checkpoint['failed']:
            log(f"[{i}/{len(pdf_files)}] Retrying previously failed: {pdf.name}")
        
        # Convert the file
        success, error = convert_single_pdf(pdf, i, len(pdf_files))
        
        if success:
            checkpoint['completed'].append(str(pdf))
            completed += 1
            # Remove from failed if it was there
            if str(pdf) in checkpoint['failed']:
                del checkpoint['failed'][str(pdf)]
                failed -= 1
        else:
            checkpoint['failed'][str(pdf)] = error or "Unknown error"
            if str(pdf) not in checkpoint['failed']:
                failed += 1
        
        # Save checkpoint after each file
        save_checkpoint(checkpoint)
        
        # Progress summary
        total_processed = completed + failed
        percent = (total_processed / len(pdf_files)) * 100
        log(f"Progress: {percent:.1f}% | Completed: {completed} | Failed: {failed}")
        log("-" * 70)
        
        # Small delay between files to avoid overloading
        if i < len(pdf_files):
            time.sleep(1)
    
    # Final summary
    log("\n" + "="*70)
    log("CONVERSION COMPLETE")
    log(f"Total files: {len(pdf_files)}")
    log(f"Successfully converted: {completed}")
    log(f"Failed: {failed}")
    log(f"Output directory: {MARKDOWN_DIR}")
    log("="*70)
    
    # List failed files if any
    if checkpoint['failed']:
        log("\nFailed conversions:")
        for pdf_path, error in checkpoint['failed'].items():
            log(f"  - {Path(pdf_path).name}: {error}")

if __name__ == "__main__":
    main()