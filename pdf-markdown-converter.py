#!/usr/bin/env python3
"""
HDM PDF to Markdown Converter - Ultimate Edition
Consolidates all conversion functionality with dual mode as default
"""

import os
import sys
import argparse
import subprocess
import shutil
import json
import logging
import time
import signal
from pathlib import Path
from datetime import datetime
from multiprocessing import Pool, cpu_count
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
BASE_DIR = Path(__file__).parent
PAPERS_DIR = BASE_DIR / 'papers'

class HDMPDFConverter:
    """Ultimate PDF to Markdown converter with all features"""
    
    def __init__(self, args):
        self.args = args
        self.setup_paths()
        self.setup_logging()
        self.checkpoint = self.load_checkpoint()
        self.stats = {
            'total': 0,
            'completed': 0,
            'failed': 0,
            'skipped': 0,
            'start_time': time.time()
        }
        
    def setup_paths(self):
        """Setup directory paths based on conversion mode"""
        # Determine output directory name based on mode
        if self.args.output_dir:
            self.output_dir = Path(self.args.output_dir)
        else:
            # Build directory name from mode
            mode_parts = []
            if self.args.mode == 'dual':
                mode_parts.append('dual')
            elif self.args.mode == 'images':
                mode_parts.append('images')
            elif self.args.mode == 'descriptions':
                mode_parts.append('descriptions')
            
            if self.args.fast:
                mode_parts.append('fast')
            
            self.output_dir = BASE_DIR / f"markdown_{'_'.join(mode_parts)}"
        
        self.output_dir.mkdir(exist_ok=True)
        
        # Log file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = BASE_DIR / 'logs' / f"conversion_{timestamp}.log"
        self.log_file.parent.mkdir(exist_ok=True)
        
        # Checkpoint file
        self.checkpoint_file = BASE_DIR / f"checkpoint_{self.output_dir.name}.json"
    
    def setup_logging(self):
        """Setup logging configuration"""
        level = logging.DEBUG if self.args.debug else logging.INFO
        
        handlers = [logging.StreamHandler(sys.stdout)]
        if not self.args.no_log:
            handlers.append(logging.FileHandler(self.log_file))
        
        logging.basicConfig(
            level=level,
            format='%(asctime)s - [%(levelname)s] - %(message)s',
            handlers=handlers
        )
        self.logger = logging.getLogger(__name__)
    
    def load_checkpoint(self) -> Dict:
        """Load or create checkpoint"""
        if self.checkpoint_file.exists() and not self.args.reset:
            with open(self.checkpoint_file, 'r') as f:
                return json.load(f)
        return {
            'completed': [],
            'failed': {},
            'started': datetime.now().isoformat(),
            'config': vars(self.args)
        }
    
    def save_checkpoint(self):
        """Save checkpoint"""
        if not self.args.no_checkpoint:
            with open(self.checkpoint_file, 'w') as f:
                json.dump(self.checkpoint, f, indent=2)
    
    def convert_pdf_dual_mode(self, pdf_path: Path, worker_id: int) -> Dict:
        """Convert PDF in dual mode (both images and descriptions)"""
        result = {
            'pdf': str(pdf_path),
            'success': False,
            'error': None,
            'duration': 0,
            'images_extracted': 0,
            'size_mb': pdf_path.stat().st_size / 1024 / 1024
        }
        
        # Create temp directories for dual processing
        temp_base = self.output_dir / f"temp_{worker_id}"
        temp_desc_dir = temp_base / "descriptions"
        temp_img_dir = temp_base / "images"
        
        for d in [temp_base, temp_desc_dir, temp_img_dir]:
            d.mkdir(exist_ok=True)
        
        try:
            start_time = time.time()
            self.logger.info(f"[DUAL] Converting: {pdf_path.name} ({result['size_mb']:.1f}MB)")
            
            # Create input directories
            desc_input = temp_desc_dir / "input"
            img_input = temp_img_dir / "input"
            desc_input.mkdir(exist_ok=True)
            img_input.mkdir(exist_ok=True)
            
            # Copy PDF to both
            shutil.copy2(pdf_path, desc_input / pdf_path.name)
            shutil.copy2(pdf_path, img_input / pdf_path.name)
            
            # Step 1: Generate descriptions
            desc_cmd = self.build_marker_command(desc_input, temp_desc_dir, mode='descriptions')
            desc_success, desc_output = self.run_marker(desc_cmd, "descriptions")
            
            # Step 2: Extract images
            img_cmd = self.build_marker_command(img_input, temp_img_dir, mode='images')
            img_success, img_output = self.run_marker(img_cmd, "images")
            
            if desc_success and img_success:
                # Merge results
                merged = self.merge_dual_outputs(pdf_path, temp_desc_dir, temp_img_dir)
                if merged:
                    result['success'] = True
                    result['images_extracted'] = merged['images_count']
                else:
                    result['error'] = "Failed to merge outputs"
            else:
                result['error'] = f"Conversion failed - Desc: {desc_success}, Img: {img_success}"
            
            result['duration'] = time.time() - start_time
            
        except Exception as e:
            result['error'] = str(e)
            self.logger.error(f"Exception in dual mode: {e}")
        finally:
            # Cleanup
            shutil.rmtree(temp_base, ignore_errors=True)
        
        return result
    
    def convert_pdf_single_mode(self, pdf_path: Path, worker_id: int) -> Dict:
        """Convert PDF in single mode (images OR descriptions)"""
        result = {
            'pdf': str(pdf_path),
            'success': False,
            'error': None,
            'duration': 0,
            'size_mb': pdf_path.stat().st_size / 1024 / 1024
        }
        
        # Create temp directory
        temp_dir = self.output_dir / f"temp_{worker_id}"
        temp_dir.mkdir(exist_ok=True)
        
        try:
            start_time = time.time()
            mode = self.args.mode.upper()
            self.logger.info(f"[{mode}] Converting: {pdf_path.name} ({result['size_mb']:.1f}MB)")
            
            # Copy PDF to temp directory
            temp_pdf = temp_dir / pdf_path.name
            shutil.copy2(pdf_path, temp_pdf)
            
            # Build and run command
            cmd = self.build_marker_command(temp_dir, self.output_dir, mode=self.args.mode)
            success, output = self.run_marker(cmd, self.args.mode)
            
            if success:
                # Check output
                output_dir = self.output_dir / pdf_path.stem
                md_file = output_dir / f"{pdf_path.stem}.md"
                
                if md_file.exists():
                    result['success'] = True
                    
                    # Post-process if needed
                    if self.args.mode == 'descriptions' and self.args.enhance:
                        self.enhance_descriptions(md_file)
                    
                    # Count images if extracted
                    if self.args.mode == 'images':
                        images = list(output_dir.glob('*.jpeg')) + list(output_dir.glob('*.png'))
                        result['images_extracted'] = len(images)
                else:
                    result['error'] = "No output file created"
            else:
                result['error'] = f"Marker command failed: {output[:200]}"
            
            result['duration'] = time.time() - start_time
            
        except Exception as e:
            result['error'] = str(e)
            self.logger.error(f"Exception in single mode: {e}")
        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
        
        return result
    
    def convert_pdf(self, args: Tuple[Path, int]) -> Dict:
        """Main PDF conversion dispatcher"""
        pdf_path, worker_id = args
        
        # Skip if already completed
        if str(pdf_path) in self.checkpoint['completed'] and not self.args.force:
            self.logger.debug(f"Skipping completed: {pdf_path.name}")
            return {
                'pdf': str(pdf_path),
                'success': True,
                'error': 'already_completed',
                'duration': 0
            }
        
        # Skip large files in fast mode
        size_mb = pdf_path.stat().st_size / 1024 / 1024
        if self.args.fast and size_mb > self.args.max_size_fast:
            return {
                'pdf': str(pdf_path),
                'success': False,
                'error': f"Too large for fast mode: {size_mb:.1f}MB",
                'duration': 0
            }
        
        # Route to appropriate converter
        if self.args.mode == 'dual':
            result = self.convert_pdf_dual_mode(pdf_path, worker_id)
        else:
            result = self.convert_pdf_single_mode(pdf_path, worker_id)
        
        # Update checkpoint
        if result['success'] and result.get('error') != 'already_completed':
            self.checkpoint['completed'].append(str(pdf_path))
            self.logger.info(f"✓ Completed: {pdf_path.name} in {result['duration']:.1f}s")
        elif not result['success']:
            self.checkpoint['failed'][str(pdf_path)] = result['error']
            self.logger.error(f"✗ Failed: {pdf_path.name} - {result['error']}")
        
        # Save checkpoint periodically
        if len(self.checkpoint['completed']) % 5 == 0:
            self.save_checkpoint()
        
        return result
    
    def build_marker_command(self, input_dir: Path, output_dir: Path, mode: str) -> List[str]:
        """Build marker command based on mode and options"""
        cmd = [
            'marker' if shutil.which('marker') else './venv/bin/marker',
            str(input_dir),
            '--output_dir', str(output_dir),
            '--max_files', '1'
        ]
        
        # Add mode-specific options
        if mode == 'images':
            cmd.extend(['--extract_images', 'True'])
            if not self.args.no_llm:
                cmd.append('--use_llm')
        elif mode == 'descriptions':
            cmd.extend(['--use_llm', '--disable_image_extraction'])
        
        # Common options
        if self.args.format_lines:
            cmd.append('--format_lines')
        
        if self.args.fast:
            cmd.append('--disable_multiprocessing')
        
        return cmd
    
    def run_marker(self, cmd: List[str], mode: str) -> Tuple[bool, str]:
        """Run marker command with proper timeout and error handling"""
        try:
            env = os.environ.copy()
            if GOOGLE_API_KEY:
                env['GOOGLE_API_KEY'] = GOOGLE_API_KEY
            
            timeout = self.args.timeout
            if self.args.fast:
                timeout = min(timeout, 120)
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env
            )
            
            if process.returncode == 0:
                return True, process.stdout
            else:
                return False, process.stderr
                
        except subprocess.TimeoutExpired:
            return False, f"Timeout after {timeout}s"
        except Exception as e:
            return False, str(e)
    
    def merge_dual_outputs(self, pdf_path: Path, desc_dir: Path, img_dir: Path) -> Optional[Dict]:
        """Merge description and image outputs"""
        try:
            # Find markdown files
            desc_md = list(desc_dir.rglob(f"{pdf_path.stem}.md"))
            img_md = list(img_dir.rglob(f"{pdf_path.stem}.md"))
            
            if not desc_md or not img_md:
                self.logger.error("Could not find markdown files to merge")
                return None
            
            desc_md_path = desc_md[0]
            img_md_path = img_md[0]
            img_output_dir = img_md_path.parent
            
            # Read both files
            with open(desc_md_path, 'r', encoding='utf-8') as f:
                desc_content = f.read()
            
            with open(img_md_path, 'r', encoding='utf-8') as f:
                img_content = f.read()
            
            # Create final output directory
            final_dir = self.output_dir / pdf_path.stem
            final_dir.mkdir(exist_ok=True)
            
            # Copy images
            image_files = []
            for pattern in ['*.jpeg', '*.jpg', '*.png', '*.gif', '*.svg']:
                for img_file in img_output_dir.glob(pattern):
                    shutil.copy2(img_file, final_dir / img_file.name)
                    image_files.append(img_file.name)
            
            # Create enhanced content
            enhanced_content = self.create_enhanced_markdown(desc_content, img_content, image_files)
            
            # Write final markdown
            final_md = final_dir / f"{pdf_path.stem}.md"
            with open(final_md, 'w', encoding='utf-8') as f:
                f.write(enhanced_content)
            
            return {'images_count': len(image_files), 'output_path': str(final_md)}
            
        except Exception as e:
            self.logger.error(f"Error merging outputs: {e}")
            return None
    
    def create_enhanced_markdown(self, desc_content: str, img_content: str, image_files: List[str]) -> str:
        """Create enhanced markdown with both images and descriptions"""
        # This is a sophisticated merge that matches image references with descriptions
        img_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
        
        # Parse both contents
        desc_lines = desc_content.split('\n')
        img_lines = img_content.split('\n')
        
        # Build enhanced content
        enhanced_lines = []
        desc_idx = 0
        
        for img_line in img_lines:
            img_match = img_pattern.search(img_line)
            
            if img_match:
                # Found an image reference
                alt_text = img_match.group(1)
                img_path = img_match.group(2)
                
                # Add the image reference
                enhanced_lines.append(img_line)
                
                # Find corresponding description
                description = self.find_image_description(desc_lines, desc_idx, alt_text)
                if description:
                    enhanced_lines.append("")
                    enhanced_lines.append(f"**[Image Description]** {description}")
                    enhanced_lines.append("")
                    desc_idx += 1
            else:
                # Regular text line
                enhanced_lines.append(img_line)
        
        return '\n'.join(enhanced_lines)
    
    def find_image_description(self, desc_lines: List[str], start_idx: int, alt_text: str) -> Optional[str]:
        """Find image description in description content"""
        # Look for descriptive text that likely corresponds to this image
        keywords = ['figure', 'image', 'diagram', 'chart', 'graph', 'table', 'illustration']
        
        for i in range(start_idx, min(start_idx + 20, len(desc_lines))):
            line = desc_lines[i].strip().lower()
            
            # Check if line contains image-related keywords and substantial text
            if any(kw in line for kw in keywords) and len(line) > 50:
                # Extract the description
                desc_start = i
                desc_lines_collected = []
                
                # Collect lines until we hit another image or empty lines
                for j in range(i, min(i + 10, len(desc_lines))):
                    current_line = desc_lines[j].strip()
                    if not current_line or any(kw in current_line.lower() for kw in keywords[1:]):
                        break
                    desc_lines_collected.append(current_line)
                
                if desc_lines_collected:
                    return ' '.join(desc_lines_collected)
        
        return None
    
    def enhance_descriptions(self, md_file: Path):
        """Add enhanced formatting for image descriptions"""
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add visual markers for better LLM understanding
            patterns = [
                (r'(Figure \d+)', r'**[\1 - Visual Element]**'),
                (r'(Table \d+)', r'**[\1 - Data Table]**'),
                (r'(Diagram \d+)', r'**[\1 - Diagram]**'),
                (r'(Chart \d+)', r'**[\1 - Chart]**'),
                (r'(Graph \d+)', r'**[\1 - Graph]**'),
            ]
            
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            self.logger.warning(f"Could not enhance {md_file}: {e}")
    
    def get_pdf_files(self) -> List[Path]:
        """Get list of PDFs to process"""
        input_dir = Path(self.args.input_dir)
        if not input_dir.exists():
            self.logger.error(f"Input directory not found: {input_dir}")
            return []
        
        # Get all PDFs
        all_pdfs = list(input_dir.glob('*.pdf'))
        
        # Filter by size if specified
        if self.args.min_size > 0:
            all_pdfs = [p for p in all_pdfs if p.stat().st_size >= self.args.min_size * 1024]
        
        if self.args.max_size > 0:
            all_pdfs = [p for p in all_pdfs if p.stat().st_size <= self.args.max_size * 1024 * 1024]
        
        # Sort by size
        all_pdfs.sort(key=lambda p: p.stat().st_size)
        
        # Apply limit
        if self.args.limit:
            all_pdfs = all_pdfs[:self.args.limit]
        
        return all_pdfs
    
    def convert_all(self):
        """Main conversion process"""
        # Get PDFs
        pdf_files = self.get_pdf_files()
        if not pdf_files:
            self.logger.error("No PDF files found matching criteria!")
            return
        
        # Filter completed if not forcing
        if not self.args.force:
            pending = [p for p in pdf_files if str(p) not in self.checkpoint['completed']]
        else:
            pending = pdf_files
        
        self.stats['total'] = len(pdf_files)
        
        self.logger.info(f"Total PDFs: {len(pdf_files)}, Pending: {len(pending)}")
        
        if not pending:
            self.logger.info("All PDFs already converted! Use --force to reconvert.")
            return
        
        # Show mode info
        self.logger.info(f"Conversion mode: {self.args.mode.upper()}")
        self.logger.info(f"Workers: {self.args.workers}")
        self.logger.info(f"Output: {self.output_dir}")
        
        # Prepare worker arguments
        worker_args = [(pdf, i % self.args.workers) for i, pdf in enumerate(pending)]
        
        # Process
        results = []
        
        try:
            if self.args.workers == 1:
                # Sequential processing
                for args in worker_args:
                    if self.args.progress:
                        self.show_progress(len(results), len(pending))
                    result = self.convert_pdf(args)
                    results.append(result)
            else:
                # Parallel processing
                with Pool(processes=self.args.workers) as pool:
                    for i, result in enumerate(pool.imap_unordered(self.convert_pdf, worker_args)):
                        results.append(result)
                        if self.args.progress:
                            self.show_progress(i + 1, len(pending))
        
        except KeyboardInterrupt:
            self.logger.warning("\nConversion interrupted by user")
        finally:
            # Final save
            self.save_checkpoint()
        
        # Calculate final stats
        self.stats['completed'] = sum(1 for r in results if r['success'] and r.get('error') != 'already_completed')
        self.stats['failed'] = sum(1 for r in results if not r['success'])
        self.stats['skipped'] = sum(1 for r in results if r.get('error') == 'already_completed')
        
        # Show summary
        self.show_summary(results)
    
    def show_progress(self, current: int, total: int):
        """Show progress bar"""
        percent = (current / total) * 100
        bar_length = 50
        filled = int(bar_length * current / total)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        elapsed = time.time() - self.stats['start_time']
        rate = current / elapsed if elapsed > 0 else 0
        eta = (total - current) / rate if rate > 0 else 0
        
        print(f'\r[{bar}] {percent:.1f}% | {current}/{total} | {rate:.1f} PDFs/s | ETA: {int(eta)}s', end='', flush=True)
    
    def show_summary(self, results: List[Dict]):
        """Show conversion summary"""
        duration = time.time() - self.stats['start_time']
        
        print("\n\n" + "="*70)
        print("CONVERSION COMPLETE")
        print("="*70)
        print(f"Mode: {self.args.mode.upper()}")
        print(f"Total PDFs: {self.stats['total']}")
        print(f"Newly converted: {self.stats['completed']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Skipped (already done): {self.stats['skipped']}")
        print(f"Total time: {int(duration)}s ({duration/60:.1f} minutes)")
        
        if self.stats['completed'] > 0:
            print(f"Average: {duration/self.stats['completed']:.1f}s per PDF")
            
            # Mode-specific stats
            if self.args.mode in ['dual', 'images']:
                total_images = sum(r.get('images_extracted', 0) for r in results if r['success'])
                print(f"Total images extracted: {total_images}")
        
        print(f"\nOutput directory: {self.output_dir}")
        print(f"Checkpoint: {self.checkpoint_file}")
        
        # Show failures
        if self.stats['failed'] > 0:
            print(f"\nFailed PDFs:")
            for pdf, error in list(self.checkpoint['failed'].items())[-10:]:
                print(f"  - {Path(pdf).name}: {error}")
    
    def show_status(self):
        """Show current conversion status"""
        if not self.checkpoint_file.exists():
            print("No checkpoint found. No conversions in progress.")
            return
        
        checkpoint = self.load_checkpoint()
        
        print("="*70)
        print("CONVERSION STATUS")
        print("="*70)
        print(f"Output directory: {self.output_dir}")
        print(f"Started: {checkpoint.get('started', 'Unknown')}")
        print(f"Mode: {checkpoint.get('config', {}).get('mode', 'Unknown')}")
        print(f"Completed: {len(checkpoint['completed'])}")
        print(f"Failed: {len(checkpoint['failed'])}")
        
        if checkpoint['failed']:
            print("\nRecent failures:")
            for pdf, error in list(checkpoint['failed'].items())[-5:]:
                print(f"  - {Path(pdf).name}: {error}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='HDM PDF to Markdown Converter - Ultimate Edition',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default dual mode (images + descriptions)
  %(prog)s
  
  # Images only mode
  %(prog)s --mode images
  
  # Descriptions only mode  
  %(prog)s --mode descriptions
  
  # Fast conversion with 8 workers
  %(prog)s --fast --workers 8
  
  # Convert specific number of PDFs
  %(prog)s --limit 10
  
  # Convert PDFs larger than 1MB
  %(prog)s --min-size 1024
  
  # Show status
  %(prog)s --status
  
  # Full production run with progress
  %(prog)s --workers 8 --progress
        """
    )
    
    # Mode selection
    parser.add_argument('--mode', choices=['dual', 'images', 'descriptions'],
                       default='dual',
                       help='Conversion mode (default: dual - both images and descriptions)')
    
    # Input/Output options
    parser.add_argument('--input-dir', default=str(PAPERS_DIR),
                       help='Input directory with PDFs')
    parser.add_argument('--output-dir',
                       help='Output directory (auto-generated if not specified)')
    
    # Processing options
    parser.add_argument('--workers', type=int, default=4,
                       help='Number of parallel workers (default: 4)')
    parser.add_argument('--limit', type=int,
                       help='Limit number of PDFs to convert')
    parser.add_argument('--timeout', type=int, default=300,
                       help='Timeout per PDF in seconds (default: 300)')
    
    # Filtering options
    parser.add_argument('--min-size', type=int, default=0,
                       help='Minimum file size in KB (default: 0)')
    parser.add_argument('--max-size', type=int, default=0,
                       help='Maximum file size in MB (default: unlimited)')
    
    # Performance options
    parser.add_argument('--fast', action='store_true',
                       help='Fast mode - no LLM, basic conversion')
    parser.add_argument('--max-size-fast', type=int, default=20,
                       help='Max file size for fast mode in MB (default: 20)')
    
    # Enhancement options
    parser.add_argument('--format-lines', action='store_true', default=True,
                       help='Format lines for better readability (default: True)')
    parser.add_argument('--enhance', action='store_true',
                       help='Enhance descriptions for better LLM understanding')
    parser.add_argument('--no-llm', action='store_true',
                       help='Disable LLM usage (for images mode)')
    
    # Control options
    parser.add_argument('--reset', action='store_true',
                       help='Reset checkpoint and start fresh')
    parser.add_argument('--force', action='store_true',
                       help='Force reconversion of completed PDFs')
    parser.add_argument('--status', action='store_true',
                       help='Show conversion status and exit')
    parser.add_argument('--progress', action='store_true',
                       help='Show progress bar during conversion')
    
    # Debugging options
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug logging')
    parser.add_argument('--no-log', action='store_true',
                       help='Disable file logging')
    parser.add_argument('--no-checkpoint', action='store_true',
                       help='Disable checkpoint saving')
    
    args = parser.parse_args()
    
    # Create converter
    converter = HDMPDFConverter(args)
    
    # Show status if requested
    if args.status:
        converter.show_status()
        return
    
    # Show configuration
    print("="*70)
    print("HDM PDF TO MARKDOWN CONVERTER - ULTIMATE EDITION")
    print("="*70)
    print(f"Mode: {args.mode.upper()} {'(Fast)' if args.fast else ''}")
    print(f"Workers: {args.workers}")
    print(f"Input: {args.input_dir}")
    print(f"Output: {converter.output_dir}")
    
    if args.limit:
        print(f"Limit: {args.limit} PDFs")
    if args.min_size > 0:
        print(f"Min size: {args.min_size} KB")
    if args.max_size > 0:
        print(f"Max size: {args.max_size} MB")
    
    print("")
    
    # Handle interrupt gracefully
    def signal_handler(sig, frame):
        print("\n\nInterrupted! Saving checkpoint...")
        converter.save_checkpoint()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Run conversion
    converter.convert_all()

if __name__ == "__main__":
    main()