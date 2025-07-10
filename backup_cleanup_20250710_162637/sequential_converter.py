#!/usr/bin/env python3
"""
Sequential PDF to Markdown converter - processes one file at a time
"""

import os
import sys
import subprocess
import json
import logging
import time
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
PAPERS_DIR = Path('papers')
MARKDOWN_DIR = Path('markdown_papers')
CHECKPOINT_FILE = Path('sequential_checkpoint.json')
LOG_FILE = Path('logs') / f'sequential_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

# Ensure directories exist
MARKDOWN_DIR.mkdir(exist_ok=True)
LOG_FILE.parent.mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE)
    ]
)
logger = logging.getLogger(__name__)

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

def check_existing_conversion(pdf_path):
    """Check if PDF has already been converted"""
    output_dir = MARKDOWN_DIR / pdf_path.stem
    md_file = output_dir / f"{pdf_path.stem}.md"
    
    if output_dir.exists() and md_file.exists() and md_file.stat().st_size > 0:
        return True, md_file
    
    # Clean up empty directories
    if output_dir.exists() and (not md_file.exists() or md_file.stat().st_size == 0):
        shutil.rmtree(output_dir, ignore_errors=True)
    
    return False, md_file

def convert_single_pdf(pdf_path):
    """Convert a single PDF using marker directly"""
    # Check if already converted
    exists, md_path = check_existing_conversion(pdf_path)
    if exists:
        logger.info(f"✓ Already converted: {pdf_path.name}")
        return True, None
    
    # Create temp directory
    temp_dir = MARKDOWN_DIR / f"temp_{int(time.time())}"
    temp_input = temp_dir / "input"
    temp_input.mkdir(parents=True, exist_ok=True)
    
    try:
        # Copy PDF
        shutil.copy2(pdf_path, temp_input / pdf_path.name)
        
        # Run marker
        cmd = [
            './venv/bin/marker',
            str(temp_input),
            '--output_dir', str(MARKDOWN_DIR),
            '--max_files', '1',
            '--extract_images', 'true',
            '--format_lines'
        ]
        
        logger.info(f"Converting: {pdf_path.name} ({pdf_path.stat().st_size / 1024 / 1024:.1f}MB)")
        
        # Load env vars including API keys
        env = os.environ.copy()
        if os.path.exists('.env'):
            with open('.env') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        env[key] = value
        
        # Use first API key if available
        if 'GEMINI_API_KEYS' in env and env['GEMINI_API_KEYS']:
            env['GOOGLE_API_KEY'] = env['GEMINI_API_KEYS'].split(',')[0].strip()
        
        # Run conversion
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=300)
        duration = time.time() - start_time
        
        if result.returncode == 0:
            # Verify output
            exists, md_path = check_existing_conversion(pdf_path)
            if exists:
                logger.info(f"✓ Converted in {duration:.1f}s: {pdf_path.name}")
                return True, None
            else:
                error = "No output file created"
                logger.error(f"✗ Failed: {pdf_path.name} - {error}")
                return False, error
        else:
            error = result.stderr[:200] if result.stderr else "Unknown error"
            logger.error(f"✗ Failed: {pdf_path.name} - {error}")
            return False, error
            
    except subprocess.TimeoutExpired:
        error = "Timeout after 5 minutes"
        logger.error(f"✗ Timeout: {pdf_path.name}")
        return False, error
    except Exception as e:
        logger.error(f"✗ Error: {pdf_path.name} - {e}")
        return False, str(e)
    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    """Main conversion loop"""
    # Get PDFs
    pdf_files = list(PAPERS_DIR.glob('*.pdf'))
    pdf_files = [p for p in pdf_files if p.stat().st_size >= 100 * 1024]  # Min 100KB
    pdf_files.sort(key=lambda p: p.stat().st_size)  # Start with smaller files
    
    logger.info(f"Found {len(pdf_files)} PDFs to process")
    
    # Load checkpoint
    checkpoint = load_checkpoint()
    
    # Process files
    completed = 0
    failed = 0
    
    for i, pdf in enumerate(pdf_files):
        # Skip if already processed
        if str(pdf) in checkpoint['completed']:
            exists, _ = check_existing_conversion(pdf)
            if exists:
                completed += 1
                continue
            else:
                # Remove from checkpoint if file missing
                checkpoint['completed'].remove(str(pdf))
        
        if str(pdf) in checkpoint['failed']:
            logger.info(f"Skipping previously failed: {pdf.name}")
            failed += 1
            continue
        
        # Convert
        success, error = convert_single_pdf(pdf)
        
        if success:
            checkpoint['completed'].append(str(pdf))
            completed += 1
        else:
            checkpoint['failed'][str(pdf)] = error
            failed += 1
        
        # Save checkpoint
        save_checkpoint(checkpoint)
        
        # Progress
        total = completed + failed
        percent = (total / len(pdf_files)) * 100
        logger.info(f"Progress: {percent:.1f}% ({total}/{len(pdf_files)}) | ✓ {completed} | ✗ {failed}")
        logger.info("-" * 70)
    
    # Summary
    logger.info("="*70)
    logger.info(f"Conversion complete: {completed} succeeded, {failed} failed")
    logger.info(f"Output directory: {MARKDOWN_DIR}")

if __name__ == "__main__":
    main()