#!/usr/bin/env python3
"""
Robust PDF to Markdown converter with concurrent processing
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
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple

# Configuration
PAPERS_DIR = Path('papers')
MARKDOWN_DIR = Path('markdown_papers')  # Changed to markdown_papers
CHECKPOINT_FILE = Path('robust_converter_checkpoint.json')
LOG_FILE = Path('logs') / f'robust_converter_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

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

def load_checkpoint() -> Dict:
    """Load checkpoint"""
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE, 'r') as f:
            return json.load(f)
    return {
        'completed': [],
        'failed': {},
        'started': datetime.now().isoformat()
    }

def save_checkpoint(checkpoint: Dict):
    """Save checkpoint"""
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(checkpoint, f, indent=2)

def check_existing_conversion(pdf_path: Path) -> Tuple[bool, Path]:
    """Check if PDF has already been converted and the markdown file exists"""
    # Expected output directory name
    output_dir = MARKDOWN_DIR / pdf_path.stem
    md_file = output_dir / f"{pdf_path.stem}.md"
    
    if output_dir.exists() and md_file.exists():
        # Verify the markdown file is not empty
        if md_file.stat().st_size > 0:
            return True, md_file
        else:
            logger.warning(f"Found empty markdown file: {md_file}")
            # Remove empty directory
            shutil.rmtree(output_dir, ignore_errors=True)
    
    return False, md_file

def convert_single_pdf(pdf_path: Path, worker_id: int, api_keys: List[str]) -> Dict:
    """Convert a single PDF to markdown"""
    result = {
        'pdf': str(pdf_path),
        'success': False,
        'error': None,
        'duration': 0,
        'output_path': None,
        'size_mb': pdf_path.stat().st_size / 1024 / 1024
    }
    
    start_time = time.time()
    
    # Check if already converted
    exists, md_path = check_existing_conversion(pdf_path)
    if exists:
        logger.info(f"✓ Already converted: {pdf_path.name} -> {md_path}")
        result['success'] = True
        result['output_path'] = str(md_path)
        result['duration'] = 0
        return result
    
    # Create temporary directory for this conversion
    temp_dir = MARKDOWN_DIR / f"temp_convert_{worker_id}_{int(time.time())}"
    temp_input = temp_dir / "input"
    temp_input.mkdir(parents=True, exist_ok=True)
    
    try:
        # Copy PDF to temp directory
        temp_pdf = temp_input / pdf_path.name
        shutil.copy2(pdf_path, temp_pdf)
        
        # Select API key for this worker
        api_key = api_keys[worker_id % len(api_keys)] if api_keys else None
        
        logger.info(f"[Worker {worker_id}] Converting: {pdf_path.name} ({result['size_mb']:.1f}MB)")
        
        # Build marker command
        cmd = [
            './venv/bin/marker',
            str(temp_input),
            '--output_dir', str(MARKDOWN_DIR),
            '--max_files', '1',
            '--skip_existing',
            '--extract_images', 'true',
            '--format_lines'
        ]
        
        # Setup environment
        env = os.environ.copy()
        if api_key:
            env['GOOGLE_API_KEY'] = api_key
        
        # Run marker
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            env=env
        )
        
        if process.returncode == 0:
            # Verify output was created
            exists, md_path = check_existing_conversion(pdf_path)
            if exists:
                result['success'] = True
                result['output_path'] = str(md_path)
                logger.info(f"✓ Converted successfully: {pdf_path.name}")
            else:
                result['error'] = "Output file not created"
                logger.error(f"✗ No output created for: {pdf_path.name}")
        else:
            result['error'] = f"Marker failed: {process.stderr[:200]}"
            logger.error(f"✗ Conversion failed: {pdf_path.name} - {process.stderr[:200]}")
    
    except subprocess.TimeoutExpired:
        result['error'] = "Timeout after 5 minutes"
        logger.error(f"✗ Timeout: {pdf_path.name}")
    except Exception as e:
        result['error'] = str(e)
        logger.error(f"✗ Error converting {pdf_path.name}: {e}")
    finally:
        # Cleanup temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)
        result['duration'] = time.time() - start_time
    
    return result

def convert_pdfs_concurrent(pdf_files: List[Path], max_workers: int = 4):
    """Convert PDFs using concurrent processing"""
    # Load checkpoint
    checkpoint = load_checkpoint()
    
    # Get API keys
    api_keys = os.getenv('GEMINI_API_KEYS', '').split(',') if os.getenv('GEMINI_API_KEYS') else []
    api_keys = [key.strip() for key in api_keys if key.strip()]
    
    if api_keys:
        logger.info(f"Loaded {len(api_keys)} API key(s)")
    else:
        logger.warning("No API keys found - proceeding without Gemini features")
    
    # Filter out already completed files
    pending = []
    for pdf in pdf_files:
        if str(pdf) in checkpoint['completed']:
            # Double-check the file actually exists
            exists, _ = check_existing_conversion(pdf)
            if exists:
                logger.info(f"✓ Skipping completed: {pdf.name}")
                continue
            else:
                # Remove from completed if file doesn't exist
                checkpoint['completed'].remove(str(pdf))
                logger.warning(f"Removed missing conversion from checkpoint: {pdf.name}")
        pending.append(pdf)
    
    logger.info(f"Found {len(pending)} PDFs to convert (out of {len(pdf_files)} total)")
    
    if not pending:
        logger.info("All PDFs already converted!")
        return
    
    # Process concurrently
    completed = 0
    failed = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_pdf = {
            executor.submit(convert_single_pdf, pdf, i % max_workers, api_keys): pdf
            for i, pdf in enumerate(pending)
        }
        
        # Process completed tasks
        for future in as_completed(future_to_pdf):
            pdf = future_to_pdf[future]
            try:
                result = future.result()
                
                if result['success']:
                    checkpoint['completed'].append(result['pdf'])
                    completed += 1
                else:
                    checkpoint['failed'][result['pdf']] = result['error']
                    failed += 1
                
                # Save checkpoint after each file
                save_checkpoint(checkpoint)
                
                # Progress update
                total_done = completed + failed
                percent = (total_done / len(pending)) * 100
                logger.info(f"Progress: {percent:.1f}% ({total_done}/{len(pending)}) | ✓ {completed} | ✗ {failed}")
                
            except Exception as e:
                logger.error(f"Failed to process {pdf.name}: {e}")
                checkpoint['failed'][str(pdf)] = str(e)
                failed += 1
                save_checkpoint(checkpoint)
    
    # Final summary
    logger.info("="*70)
    logger.info(f"Conversion complete: {completed} succeeded, {failed} failed")
    logger.info(f"Output directory: {MARKDOWN_DIR}")
    
    # List failed files if any
    if checkpoint['failed']:
        logger.info("\nFailed conversions:")
        for pdf, error in checkpoint['failed'].items():
            logger.info(f"  - {Path(pdf).name}: {error}")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Robust PDF to Markdown converter')
    parser.add_argument('--workers', type=int, default=4, help='Number of concurrent workers (default: 4)')
    parser.add_argument('--min-size', type=int, default=100, help='Minimum file size in KB (default: 100)')
    parser.add_argument('--verify', action='store_true', help='Only verify existing conversions')
    args = parser.parse_args()
    
    # Get all PDFs
    pdf_files = list(PAPERS_DIR.glob('*.pdf'))
    pdf_files = [p for p in pdf_files if p.stat().st_size >= args.min_size * 1024]
    
    logger.info(f"Found {len(pdf_files)} PDFs (>= {args.min_size}KB)")
    
    if args.verify:
        # Verification mode
        logger.info("Running in verification mode...")
        valid = 0
        missing = 0
        for pdf in pdf_files:
            exists, md_path = check_existing_conversion(pdf)
            if exists:
                valid += 1
                logger.info(f"✓ Valid: {pdf.name} -> {md_path.name}")
            else:
                missing += 1
                logger.warning(f"✗ Missing: {pdf.name}")
        
        logger.info(f"\nVerification complete: {valid} valid, {missing} missing")
    else:
        # Conversion mode
        convert_pdfs_concurrent(pdf_files, max_workers=args.workers)

if __name__ == "__main__":
    main()