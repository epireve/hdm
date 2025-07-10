#!/usr/bin/env python3
"""
Batch PDF to Markdown converter - processes files in batches
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
CHECKPOINT_FILE = Path('batch_checkpoint.json')
LOG_FILE = Path('logs') / f'batch_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
BATCH_SIZE = 10  # Process 10 files at a time

# Ensure directories exist
MARKDOWN_DIR.mkdir(exist_ok=True)
LOG_FILE.parent.mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
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
        'batches_processed': 0,
        'started': datetime.now().isoformat()
    }

def save_checkpoint(checkpoint):
    """Save checkpoint"""
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(checkpoint, f, indent=2)

def check_existing_conversions(pdf_paths):
    """Check which PDFs have already been converted"""
    converted = []
    pending = []
    
    for pdf_path in pdf_paths:
        output_dir = MARKDOWN_DIR / pdf_path.stem
        md_file = output_dir / f"{pdf_path.stem}.md"
        
        if output_dir.exists() and md_file.exists() and md_file.stat().st_size > 0:
            converted.append(pdf_path)
        else:
            # Clean up empty directories
            if output_dir.exists():
                shutil.rmtree(output_dir, ignore_errors=True)
            pending.append(pdf_path)
    
    return converted, pending

def process_batch(batch_pdfs, batch_num):
    """Process a batch of PDFs"""
    if not batch_pdfs:
        return
    
    # Create batch directory
    batch_dir = Path(f"batch_{batch_num}_{int(time.time())}")
    batch_dir.mkdir(exist_ok=True)
    
    try:
        # Copy PDFs to batch directory
        logger.info(f"\n{'='*70}")
        logger.info(f"BATCH {batch_num}: Processing {len(batch_pdfs)} files")
        logger.info(f"{'='*70}")
        
        for pdf in batch_pdfs:
            shutil.copy2(pdf, batch_dir / pdf.name)
            logger.info(f"  - {pdf.name} ({pdf.stat().st_size / 1024 / 1024:.1f}MB)")
        
        # Load API keys from .env
        env = os.environ.copy()
        if os.path.exists('.env'):
            with open('.env') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        env[key] = value.strip('"').strip("'")
        
        # Use first API key if available
        if 'GEMINI_API_KEYS' in env and env['GEMINI_API_KEYS']:
            env['GOOGLE_API_KEY'] = env['GEMINI_API_KEYS'].split(',')[0].strip()
            logger.info(f"Using Gemini API key (first {4} chars): {env['GOOGLE_API_KEY'][:4]}...")
        
        # Run marker
        cmd = [
            './venv/bin/marker',
            str(batch_dir),
            '--output_dir', str(MARKDOWN_DIR),
            '--max_files', str(len(batch_pdfs)),
            '--extract_images', 'true',
            '--format_lines'
        ]
        
        logger.info(f"\nRunning marker...")
        start_time = time.time()
        
        # Execute marker
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout for batch
        )
        
        duration = time.time() - start_time
        
        if result.returncode == 0:
            logger.info(f"✓ Batch completed in {duration:.1f}s")
            
            # Verify conversions
            converted, still_pending = check_existing_conversions(batch_pdfs)
            logger.info(f"Converted: {len(converted)}, Failed: {len(still_pending)}")
            
            return converted, still_pending
        else:
            logger.error(f"✗ Batch failed: {result.stderr[:500]}")
            return [], batch_pdfs
            
    except subprocess.TimeoutExpired:
        logger.error(f"✗ Batch timeout after 10 minutes")
        return [], batch_pdfs
    except Exception as e:
        logger.error(f"✗ Batch error: {e}")
        return [], batch_pdfs
    finally:
        # Cleanup batch directory
        shutil.rmtree(batch_dir, ignore_errors=True)

def main():
    """Main conversion loop"""
    # Get PDFs
    pdf_files = list(PAPERS_DIR.glob('*.pdf'))
    pdf_files = [p for p in pdf_files if p.stat().st_size >= 100 * 1024]  # Min 100KB
    pdf_files.sort(key=lambda p: p.stat().st_size)  # Start with smaller files
    
    logger.info(f"Found {len(pdf_files)} PDFs (>= 100KB)")
    
    # Load checkpoint
    checkpoint = load_checkpoint()
    
    # Filter already processed
    pending_pdfs = []
    for pdf in pdf_files:
        if str(pdf) not in checkpoint['completed'] and str(pdf) not in checkpoint['failed']:
            pending_pdfs.append(pdf)
    
    logger.info(f"Pending: {len(pending_pdfs)} files")
    
    if not pending_pdfs:
        logger.info("All files already processed!")
        return
    
    # Process in batches
    total_completed = len(checkpoint['completed'])
    total_failed = len(checkpoint['failed'])
    
    for i in range(0, len(pending_pdfs), BATCH_SIZE):
        batch = pending_pdfs[i:i+BATCH_SIZE]
        batch_num = checkpoint['batches_processed'] + 1
        
        # Process batch
        converted, failed = process_batch(batch, batch_num)
        
        # Update checkpoint
        for pdf in converted:
            checkpoint['completed'].append(str(pdf))
            total_completed += 1
        
        for pdf in failed:
            checkpoint['failed'][str(pdf)] = "Batch conversion failed"
            total_failed += 1
        
        checkpoint['batches_processed'] = batch_num
        save_checkpoint(checkpoint)
        
        # Progress
        total_processed = total_completed + total_failed
        percent = (total_processed / len(pdf_files)) * 100
        logger.info(f"\nOverall Progress: {percent:.1f}% ({total_processed}/{len(pdf_files)}) | ✓ {total_completed} | ✗ {total_failed}")
        
        # Small delay between batches
        if i + BATCH_SIZE < len(pending_pdfs):
            logger.info("Waiting 2 seconds before next batch...")
            time.sleep(2)
    
    # Final summary
    logger.info("\n" + "="*70)
    logger.info(f"CONVERSION COMPLETE")
    logger.info(f"Total files: {len(pdf_files)}")
    logger.info(f"Succeeded: {total_completed}")
    logger.info(f"Failed: {total_failed}")
    logger.info(f"Output directory: {MARKDOWN_DIR}")
    logger.info("="*70)

if __name__ == "__main__":
    main()