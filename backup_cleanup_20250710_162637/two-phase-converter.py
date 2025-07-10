#!/usr/bin/env python3
"""
HDM Two-Phase PDF Converter
Phase 1: Convert PDFs to Markdown with images
Phase 2: Generate descriptions for images and append to Markdown
"""

import os
import sys
import argparse
import subprocess
import shutil
import json
import logging
import time
from pathlib import Path
from datetime import datetime
from multiprocessing import Pool, cpu_count, Manager
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv
import re
import threading

# Load environment variables
load_dotenv()

# Configuration
GEMINI_API_KEYS = os.getenv('GEMINI_API_KEYS', '').split(',') if os.getenv('GEMINI_API_KEYS') else []
BASE_DIR = Path(__file__).parent
PAPERS_DIR = BASE_DIR / 'papers'
MARKDOWN_DIR = BASE_DIR / 'markdown_papers'

class TwoPhaseConverter:
    """Two-phase PDF to Markdown converter"""
    
    def __init__(self, args):
        self.args = args
        self.setup_paths()
        self.setup_logging()
        self.api_keys = GEMINI_API_KEYS
        self.validate_api_keys()
        
    def validate_api_keys(self):
        """Validate API keys are available"""
        if not self.api_keys:
            self.logger.error("No API keys found! Set GEMINI_API_KEYS in .env")
            sys.exit(1)
        
        self.api_keys = [key.strip() for key in self.api_keys if key.strip()]
        
        if not self.api_keys:
            self.logger.error("No valid API keys found!")
            sys.exit(1)
            
        self.logger.info(f"Loaded {len(self.api_keys)} API key(s)")
    
    def get_api_key_for_worker(self, worker_id: int) -> str:
        """Get API key for a specific worker using round-robin distribution"""
        return self.api_keys[worker_id % len(self.api_keys)]
        
    def setup_paths(self):
        """Setup directory paths"""
        self.output_dir = MARKDOWN_DIR
        self.output_dir.mkdir(exist_ok=True)
        
        # Phase-specific checkpoints
        self.phase1_checkpoint = BASE_DIR / "phase1_checkpoint.json"
        self.phase2_checkpoint = BASE_DIR / "phase2_checkpoint.json"
        
        # Log file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = BASE_DIR / 'logs' / f"two_phase_{timestamp}.log"
        self.log_file.parent.mkdir(exist_ok=True)
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [%(levelname)s] - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(self.log_file)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_checkpoint(self, phase: int) -> Dict:
        """Load checkpoint for specific phase"""
        checkpoint_file = self.phase1_checkpoint if phase == 1 else self.phase2_checkpoint
        
        if checkpoint_file.exists():
            with open(checkpoint_file, 'r') as f:
                return json.load(f)
        
        return {
            'completed': [],
            'failed': {},
            'started': datetime.now().isoformat(),
            'phase': phase
        }
    
    def save_checkpoint(self, checkpoint: Dict, phase: int):
        """Save checkpoint for specific phase"""
        checkpoint_file = self.phase1_checkpoint if phase == 1 else self.phase2_checkpoint
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)
    
    def display_detailed_progress(self, phase: int, worker_tasks: Dict, completed: int, failed: int, 
                                  total: int, start_time: float, extra_info: str = ""):
        """Display detailed progress with per-worker status"""
        elapsed = time.time() - start_time
        rate = (completed + failed) / elapsed if elapsed > 0 else 0
        eta = (total - (completed + failed)) / rate if rate > 0 else 0
        percent = ((completed + failed) / total * 100) if total > 0 else 0
        
        # Clear screen for update
        print("\033[2J\033[H", end='')  # Clear screen and move cursor to top
        
        print(f"{'='*70}")
        print(f"PHASE {phase} PROGRESS - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*70}")
        print(f"Overall: {percent:.1f}% ({completed + failed}/{total}) | ✓{completed} ✗{failed}")
        print(f"Speed: {rate:.1f} files/s | ETA: {int(eta)}s | Elapsed: {int(elapsed)}s")
        if extra_info:
            print(f"Details: {extra_info}")
        print(f"{'='*70}")
        print("Worker Status:")
        
        for worker_id in sorted(worker_tasks.keys()):
            task = worker_tasks[worker_id]
            status = task.get('status', 'idle')
            current_file = task.get('current_file', 'None')
            processed = task.get('processed', 0)
            api_key = task.get('api_key', worker_id % len(self.api_keys) + 1)
            
            # Truncate filename if too long
            if len(current_file) > 40:
                current_file = current_file[:37] + "..."
            
            status_icon = "⚡" if status == "processing" else "💤"
            print(f"  Worker {worker_id} (API #{api_key}): {status_icon} {status:<10} | Files: {processed:<3} | Current: {current_file}")
        
        print(f"{'='*70}")
    
    def phase1_convert_pdf(self, args: Tuple[Path, int, Optional[Dict]]) -> Dict:
        """Phase 1: Convert PDF to Markdown with images"""
        if len(args) == 3:
            pdf_path, worker_id, worker_tasks = args
        else:
            pdf_path, worker_id = args
            worker_tasks = None
        
        # Ensure we have the API keys in this process
        if not hasattr(self, 'api_keys') or not self.api_keys:
            self.api_keys = GEMINI_API_KEYS
        
        result = {
            'pdf': str(pdf_path),
            'success': False,
            'error': None,
            'duration': 0,
            'images_extracted': 0,
            'size_mb': pdf_path.stat().st_size / 1024 / 1024
        }
        
        # Create unique temp directory for this worker and PDF
        import uuid
        temp_id = f"{worker_id}_{uuid.uuid4().hex[:8]}"
        temp_dir = self.output_dir / f"temp_{temp_id}"
        temp_dir.mkdir(exist_ok=True)
        
        try:
            start_time = time.time()
            api_key_index = worker_id % len(self.api_keys)
            self.logger.info(f"[PHASE 1] Worker {worker_id} (API key #{api_key_index + 1}/{len(self.api_keys)}) converting: {pdf_path.name} ({result['size_mb']:.1f}MB)")
            
            # Update worker status if tracking
            if worker_tasks is not None:
                worker_tasks[worker_id] = {
                    'status': 'processing',
                    'current_file': pdf_path.name,
                    'processed': worker_tasks.get(worker_id, {}).get('processed', 0),
                    'api_key': api_key_index + 1
                }
            
            # Create input directory for marker
            input_dir = temp_dir / "input"
            input_dir.mkdir(exist_ok=True)
            
            # Copy PDF to input directory
            temp_pdf = input_dir / pdf_path.name
            shutil.copy2(pdf_path, temp_pdf)
            
            # Build marker command for fast image extraction
            cmd = [
                'marker' if shutil.which('marker') else './venv/bin/marker',
                str(input_dir),
                '--output_dir', str(self.output_dir),
                '--max_files', '1',
                '--disable_multiprocessing',  # Fast mode
                '--skip_existing',  # Skip if already converted
                '--extract_images', 'true',  # Extract images
                '--format_lines'  # Better formatting
            ]
            
            # Run marker
            env = os.environ.copy()
            env['GOOGLE_API_KEY'] = self.get_api_key_for_worker(worker_id)
            
            self.logger.debug(f"Worker {worker_id} running marker command: {' '.join(cmd)}")
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,  # Increased timeout for larger PDFs
                env=env
            )
            
            if process.returncode == 0:
                # Check output
                output_dir = self.output_dir / pdf_path.stem
                md_file = output_dir / f"{pdf_path.stem}.md"
                
                if md_file.exists():
                    result['success'] = True
                    # Count images
                    images = list(output_dir.glob('*.jpeg')) + list(output_dir.glob('*.png'))
                    result['images_extracted'] = len(images)
                    result['output_path'] = str(md_file)
                else:
                    result['error'] = "No output file created"
            else:
                result['error'] = f"Marker command failed: {process.stderr[:200]}"
            
            result['duration'] = time.time() - start_time
            
        except subprocess.TimeoutExpired:
            result['error'] = f"Timeout after 600s - PDF too large/complex"
        except Exception as e:
            result['error'] = str(e)
        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            # Update worker status to idle
            if worker_tasks is not None:
                worker_tasks[worker_id] = {
                    'status': 'idle',
                    'current_file': 'None',
                    'processed': worker_tasks.get(worker_id, {}).get('processed', 0) + 1,
                    'api_key': api_key_index + 1
                }
        
        return result
    
    def phase2_process_markdown(self, args: Tuple[Path, int, Optional[Dict]]) -> Dict:
        """Phase 2: Process markdown file to add image descriptions"""
        if len(args) == 3:
            md_path, worker_id, worker_tasks = args
        else:
            md_path, worker_id = args
            worker_tasks = None
        
        result = {
            'markdown': str(md_path),
            'success': False,
            'error': None,
            'duration': 0,
            'descriptions_added': 0
        }
        
        try:
            start_time = time.time()
            api_key_index = worker_id % len(self.api_keys)
            self.logger.info(f"[PHASE 2] Worker {worker_id} (API key #{api_key_index + 1}/{len(self.api_keys)}) processing: {md_path.name}")
            
            # Update worker status if tracking
            if worker_tasks is not None:
                worker_tasks[worker_id] = {
                    'status': 'processing',
                    'current_file': md_path.name,
                    'processed': worker_tasks.get(worker_id, {}).get('processed', 0),
                    'api_key': api_key_index + 1
                }
            
            # Read markdown content
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all image references
            img_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
            images = img_pattern.findall(content)
            
            if not images:
                self.logger.info(f"No images found in {md_path.name}")
                result['success'] = True
                result['duration'] = time.time() - start_time
                return result
            
            # Generate descriptions for each image
            enhanced_content = content
            descriptions_added = 0
            
            for alt_text, img_path in images:
                # Get full image path
                full_img_path = md_path.parent / img_path
                
                if full_img_path.exists():
                    # Generate description using Gemini
                    description = self.generate_image_description(full_img_path, worker_id)
                    
                    if description:
                        # Find the image reference in content and add description after it
                        img_ref = f"![{alt_text}]({img_path})"
                        replacement = f"{img_ref}\n\n**[Image Description]** {description}\n"
                        enhanced_content = enhanced_content.replace(img_ref, replacement)
                        descriptions_added += 1
            
            # Write enhanced content back
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(enhanced_content)
            
            result['success'] = True
            result['descriptions_added'] = descriptions_added
            result['duration'] = time.time() - start_time
            
        except Exception as e:
            result['error'] = str(e)
            self.logger.error(f"Error in phase 2: {e}")
        finally:
            # Update worker status to idle
            if worker_tasks is not None:
                worker_tasks[worker_id] = {
                    'status': 'idle',
                    'current_file': 'None',
                    'processed': worker_tasks.get(worker_id, {}).get('processed', 0) + 1,
                    'api_key': api_key_index + 1
                }
        
        return result
    
    def generate_image_description(self, img_path: Path, worker_id: int) -> Optional[str]:
        """Generate description for an image using Gemini"""
        try:
            # Create a temporary Python script to call Gemini
            script = f'''
import google.generativeai as genai
from PIL import Image
import sys

genai.configure(api_key="{self.get_api_key_for_worker(worker_id)}")
model = genai.GenerativeModel('gemini-1.5-flash')

try:
    img = Image.open("{img_path}")
    response = model.generate_content([
        "Describe this image in detail for someone who cannot see it. Focus on academic content, diagrams, charts, or data shown.",
        img
    ])
    print(response.text)
except Exception as e:
    print(f"Error: {{e}}", file=sys.stderr)
    sys.exit(1)
'''
            
            # Run the script
            process = subprocess.run(
                [sys.executable, '-c', script],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if process.returncode == 0:
                return process.stdout.strip()
            else:
                self.logger.warning(f"Failed to generate description for {img_path.name}: {process.stderr}")
                return None
                
        except Exception as e:
            self.logger.warning(f"Error generating description for {img_path.name}: {e}")
            return None
    
    def run_phase1(self):
        """Run Phase 1: Convert all PDFs to Markdown with images"""
        self.logger.info("="*70)
        self.logger.info("PHASE 1: Converting PDFs to Markdown with images")
        self.logger.info("="*70)
        
        # Clean up any old temp directories
        for temp_dir in self.output_dir.glob("temp_*"):
            if temp_dir.is_dir():
                shutil.rmtree(temp_dir, ignore_errors=True)
                self.logger.debug(f"Cleaned up old temp directory: {temp_dir}")
        
        # Get PDFs to process
        pdf_files = list(PAPERS_DIR.glob('*.pdf'))
        
        # Apply size filter (min 100KB as requested)
        pdf_files = [p for p in pdf_files if p.stat().st_size >= 100 * 1024]
        
        self.logger.info(f"Found {len(pdf_files)} PDFs (>= 100KB)")
        
        # Load checkpoint
        checkpoint = self.load_checkpoint(1)
        pending = [p for p in pdf_files if str(p) not in checkpoint['completed']]
        
        if not pending:
            self.logger.info("Phase 1 already complete!")
            return
        
        self.logger.info(f"Processing {len(pending)} pending PDFs with {self.args.workers} workers")
        
        # Prepare worker arguments
        if self.args.detailed_progress:
            manager = Manager()
            worker_tasks = manager.dict()
            for i in range(self.args.workers):
                worker_tasks[i] = {'status': 'idle', 'current_file': 'None', 'processed': 0, 'api_key': i % len(self.api_keys) + 1}
            worker_args = [(pdf, i % self.args.workers, worker_tasks) for i, pdf in enumerate(pending)]
        else:
            worker_tasks = None
            worker_args = [(pdf, i % self.args.workers) for i, pdf in enumerate(pending)]
        
        # Process
        results = []
        completed = 0
        failed = 0
        worker_status = {i: {'current': 'idle', 'processed': 0} for i in range(self.args.workers)}
        start_time = time.time()
        
        # Start detailed progress display thread if needed
        if self.args.detailed_progress:
            stop_display = threading.Event()
            def update_display():
                while not stop_display.is_set():
                    self.display_detailed_progress(1, dict(worker_tasks), completed, failed, 
                                                   len(pending), start_time, f"Images: {sum(r.get('images_extracted', 0) for r in results)}")
                    time.sleep(0.5)
            
            display_thread = threading.Thread(target=update_display)
            display_thread.start()
        
        try:
            # Set multiprocessing start method for Python 3.13 compatibility
            import multiprocessing
            try:
                multiprocessing.set_start_method('spawn', force=True)
            except RuntimeError:
                pass  # Already set
            
            with Pool(processes=self.args.workers) as pool:
                for i, result in enumerate(pool.imap_unordered(self.phase1_convert_pdf, worker_args)):
                    results.append(result)
                    
                    # Update worker status
                    worker_id = next((w for w, (pdf, w_id) in enumerate(worker_args) if str(pdf) == result['pdf'] and w_id % self.args.workers == w_id), 0)
                    worker_status[worker_id % self.args.workers]['processed'] += 1
                    
                    if result['success']:
                        checkpoint['completed'].append(result['pdf'])
                        completed += 1
                        self.logger.info(f"✓ Completed: {Path(result['pdf']).name} ({result['images_extracted']} images, {result['duration']:.1f}s)")
                    else:
                        checkpoint['failed'][result['pdf']] = result['error']
                        failed += 1
                        self.logger.error(f"✗ Failed: {Path(result['pdf']).name} - {result['error']}")
                    
                    # Show enhanced progress (only if not using detailed progress)
                    if self.args.progress and not self.args.detailed_progress:
                        elapsed = time.time() - start_time
                        rate = (i + 1) / elapsed if elapsed > 0 else 0
                        eta = (len(pending) - (i + 1)) / rate if rate > 0 else 0
                        
                        # Build worker status string
                        worker_info = " | Workers: " + " ".join([f"W{w}:{s['processed']}" for w, s in worker_status.items()])
                        
                        percent = ((i + 1) / len(pending)) * 100
                        print(f"\rPhase 1: {percent:.1f}% ({i+1}/{len(pending)}) | ✓{completed} ✗{failed} | {rate:.1f}/s | ETA: {int(eta)}s{worker_info}", end='', flush=True)
                    
                    # Save checkpoint periodically
                    if (i + 1) % 10 == 0:
                        self.save_checkpoint(checkpoint, 1)
        
        except KeyboardInterrupt:
            self.logger.warning("\nPhase 1 interrupted by user")
        finally:
            if self.args.detailed_progress:
                stop_display.set()
                display_thread.join()
            self.save_checkpoint(checkpoint, 1)
            if not self.args.detailed_progress:
                print()  # New line after progress
        
        # Summary
        total_images = sum(r.get('images_extracted', 0) for r in results if r['success'])
        total_time = time.time() - start_time
        avg_time = total_time / len(results) if results else 0
        self.logger.info(f"\nPhase 1 Complete: {completed} succeeded, {failed} failed, {total_images} total images extracted")
        self.logger.info(f"Total time: {total_time:.1f}s, Average: {avg_time:.1f}s/PDF")
    
    def run_phase2(self):
        """Run Phase 2: Add descriptions to all markdown files"""
        self.logger.info("\n" + "="*70)
        self.logger.info("PHASE 2: Adding image descriptions to Markdown files")
        self.logger.info("="*70)
        
        # Get all markdown files with images
        markdown_files = []
        for md_file in self.output_dir.rglob('*.md'):
            # Check if markdown has images
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            if '![' in content:  # Has image references
                markdown_files.append(md_file)
        
        self.logger.info(f"Found {len(markdown_files)} Markdown files with images")
        
        # Load checkpoint
        checkpoint = self.load_checkpoint(2)
        pending = [m for m in markdown_files if str(m) not in checkpoint['completed']]
        
        if not pending:
            self.logger.info("Phase 2 already complete!")
            return
        
        self.logger.info(f"Processing {len(pending)} pending files with {self.args.workers} workers")
        
        # Prepare worker arguments
        if self.args.detailed_progress:
            manager = Manager()
            worker_tasks = manager.dict()
            for i in range(self.args.workers):
                worker_tasks[i] = {'status': 'idle', 'current_file': 'None', 'processed': 0, 'api_key': i % len(self.api_keys) + 1}
            worker_args = [(md, i % self.args.workers, worker_tasks) for i, md in enumerate(pending)]
        else:
            worker_tasks = None
            worker_args = [(md, i % self.args.workers) for i, md in enumerate(pending)]
        
        # Process
        results = []
        completed = 0
        failed = 0
        total_descriptions = 0
        worker_status = {i: {'current': 'idle', 'processed': 0, 'descriptions': 0} for i in range(self.args.workers)}
        start_time = time.time()
        
        # Start detailed progress display thread if needed
        if self.args.detailed_progress:
            stop_display = threading.Event()
            def update_display():
                while not stop_display.is_set():
                    self.display_detailed_progress(2, dict(worker_tasks), completed, failed, 
                                                   len(pending), start_time, f"Descriptions: {total_descriptions}")
                    time.sleep(0.5)
            
            display_thread = threading.Thread(target=update_display)
            display_thread.start()
        
        try:
            with Pool(processes=self.args.workers) as pool:
                for i, result in enumerate(pool.imap_unordered(self.phase2_process_markdown, worker_args)):
                    results.append(result)
                    
                    # Update worker status
                    worker_id = next((w for w, (md, w_id) in enumerate(worker_args) if str(md) == result['markdown'] and w_id % self.args.workers == w_id), 0)
                    worker_status[worker_id % self.args.workers]['processed'] += 1
                    
                    if result['success']:
                        checkpoint['completed'].append(result['markdown'])
                        completed += 1
                        total_descriptions += result['descriptions_added']
                        worker_status[worker_id % self.args.workers]['descriptions'] += result['descriptions_added']
                        self.logger.info(f"✓ Enhanced: {Path(result['markdown']).name} ({result['descriptions_added']} descriptions, {result['duration']:.1f}s)")
                    else:
                        checkpoint['failed'][result['markdown']] = result['error']
                        failed += 1
                        self.logger.error(f"✗ Failed: {Path(result['markdown']).name} - {result['error']}")
                    
                    # Show enhanced progress (only if not using detailed progress)
                    if self.args.progress and not self.args.detailed_progress:
                        elapsed = time.time() - start_time
                        rate = (i + 1) / elapsed if elapsed > 0 else 0
                        eta = (len(pending) - (i + 1)) / rate if rate > 0 else 0
                        
                        # Build worker status string
                        worker_info = " | Workers: " + " ".join([f"W{w}:{s['processed']}({s['descriptions']})" for w, s in worker_status.items()])
                        
                        percent = ((i + 1) / len(pending)) * 100
                        print(f"\rPhase 2: {percent:.1f}% ({i+1}/{len(pending)}) | ✓{completed} ✗{failed} | Desc: {total_descriptions} | {rate:.1f}/s | ETA: {int(eta)}s{worker_info}", end='', flush=True)
                    
                    # Save checkpoint periodically
                    if (i + 1) % 10 == 0:
                        self.save_checkpoint(checkpoint, 2)
        
        except KeyboardInterrupt:
            self.logger.warning("\nPhase 2 interrupted by user")
        finally:
            if self.args.detailed_progress:
                stop_display.set()
                display_thread.join()
            self.save_checkpoint(checkpoint, 2)
            if not self.args.detailed_progress:
                print()  # New line after progress
        
        # Summary
        total_time = time.time() - start_time
        avg_time = total_time / len(results) if results else 0
        self.logger.info(f"\nPhase 2 Complete: {completed} succeeded, {failed} failed, {total_descriptions} descriptions added")
        self.logger.info(f"Total time: {total_time:.1f}s, Average: {avg_time:.1f}s/file")
    
    def run(self):
        """Run both phases"""
        start_time = time.time()
        
        if self.args.phase in [1, 0]:  # Phase 1 or both
            self.run_phase1()
        
        if self.args.phase in [2, 0]:  # Phase 2 or both
            self.run_phase2()
        
        # Final summary
        total_time = time.time() - start_time
        self.logger.info("\n" + "="*70)
        self.logger.info("TWO-PHASE CONVERSION COMPLETE")
        self.logger.info("="*70)
        self.logger.info(f"Total time: {int(total_time)}s ({total_time/60:.1f} minutes)")
        self.logger.info(f"Output directory: {self.output_dir}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='HDM Two-Phase PDF Converter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run both phases with 8 workers and simple progress
  %(prog)s --workers 8 --progress
  
  # Run both phases with detailed per-worker progress
  %(prog)s --workers 8 --detailed-progress
  
  # Run phase 1 only (PDF to Markdown with images)
  %(prog)s --phase 1 --workers 8 --progress
  
  # Run phase 2 only (add descriptions to existing Markdown)
  %(prog)s --phase 2 --workers 8 --detailed-progress
  
  # Show status
  %(prog)s --status
        """
    )
    
    parser.add_argument('--phase', type=int, choices=[0, 1, 2], default=0,
                       help='Phase to run: 0=both, 1=PDF to Markdown, 2=Add descriptions (default: 0)')
    parser.add_argument('--workers', type=int, default=8,
                       help='Number of parallel workers (default: 8)')
    parser.add_argument('--progress', action='store_true',
                       help='Show progress during conversion')
    parser.add_argument('--detailed-progress', action='store_true',
                       help='Show detailed per-worker progress during conversion')
    parser.add_argument('--status', action='store_true',
                       help='Show conversion status and exit')
    
    args = parser.parse_args()
    
    if args.status:
        # Show status of both phases
        for phase in [1, 2]:
            checkpoint_file = BASE_DIR / f"phase{phase}_checkpoint.json"
            if checkpoint_file.exists():
                with open(checkpoint_file, 'r') as f:
                    checkpoint = json.load(f)
                print(f"\nPhase {phase} Status:")
                print(f"  Completed: {len(checkpoint['completed'])}")
                print(f"  Failed: {len(checkpoint['failed'])}")
        return
    
    # Create converter
    converter = TwoPhaseConverter(args)
    
    # Run conversion
    converter.run()

if __name__ == "__main__":
    main()