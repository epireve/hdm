#!/usr/bin/env python3
"""
Updated concurrent image descriptor that processes multiple papers in parallel
Uses the updated list of papers needing descriptions
"""
import os
import re
import time
import json
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import queue

# Import required packages
try:
    import google.generativeai as genai
    from PIL import Image
except ImportError:
    print("Error: Required packages not installed")
    print("Please run: pip install google-generativeai pillow")
    exit(1)

# Load environment variables
env_path = Path('.env')
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"\'')

# Get API keys
API_KEYS = os.environ.get('GEMINI_API_KEYS', '').split(',')
API_KEYS = [key.strip() for key in API_KEYS if key.strip()]

if not API_KEYS:
    print("Error: No API keys found in .env file")
    exit(1)

# Thread-safe locks
print_lock = Lock()
stats_lock = Lock()

# Global stats
global_stats = {
    'processed_papers': 0,
    'total_images': 0,
    'failed_papers': 0,
    'errors': []
}

def thread_print(message):
    """Thread-safe printing"""
    with print_lock:
        print(message)

def escape_description(description):
    """Escape special characters in description for regex replacement"""
    # Escape backslashes and other special regex characters
    description = description.replace('\\', '\\\\')
    description = description.replace('$', r'\$')
    description = description.replace('^', r'\^')
    description = description.replace('.', r'\.')
    description = description.replace('*', r'\*')
    description = description.replace('+', r'\+')
    description = description.replace('?', r'\?')
    description = description.replace('[', r'\[')
    description = description.replace(']', r'\]')
    description = description.replace('{', r'\{')
    description = description.replace('}', r'\}')
    description = description.replace('(', r'\(')
    description = description.replace(')', r'\)')
    description = description.replace('|', r'\|')
    return description

def has_image_description(content, image_file):
    """Check if an image already has a description comment"""
    pattern = rf'!\[\]\({re.escape(image_file)}\)\s*\n\s*<!-- Image Description:.*?-->'
    return bool(re.search(pattern, content, re.DOTALL))

def describe_images_in_paper(paper_path, api_key, worker_id):
    """Describe images in a single paper using HTML comments"""
    paper_name = paper_path.parent.name
    
    try:
        # Configure Gemini for this thread
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Read the markdown content
        with open(paper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all images with empty alt text
        image_pattern = r'!\[\]\(([^)]+)\)'
        empty_images = re.findall(image_pattern, content)
        
        if not empty_images:
            return paper_name, 0, "No images with empty alt text"
        
        # Filter out images that already have descriptions
        images_to_process = []
        for image_file in empty_images:
            if not has_image_description(content, image_file):
                images_to_process.append(image_file)
        
        if not images_to_process:
            return paper_name, 0, "All images already have descriptions"
        
        # Process each image
        updated_content = content
        images_described = 0
        
        for image_file in images_to_process:
            image_path = paper_path.parent / image_file
            if not image_path.exists():
                thread_print(f"[Worker {worker_id}] Warning: Image not found: {image_path}")
                continue
            
            try:
                # Load and describe the image
                img = Image.open(image_path)
                
                prompt = """Analyze this image from an academic paper and provide a concise description 
                focusing on the technical content. Describe any diagrams, charts, graphs, equations, 
                or technical illustrations. Be specific about what the image shows and its purpose 
                in the context of the paper. Keep the description under 100 words."""
                
                response = model.generate_content([prompt, img])
                
                if response.text:
                    description = response.text.strip().replace('\n', ' ')
                    
                    # Escape the description for safe regex replacement
                    escaped_description = escape_description(description)
                    
                    # Find the image reference and add description comment after it
                    old_pattern = rf'(!\[\]\({re.escape(image_file)}\))'
                    new_text = f'![]({image_file})\n<!-- Image Description: {description} -->'
                    
                    # Replace only if not already has description
                    if not has_image_description(updated_content, image_file):
                        updated_content = re.sub(old_pattern, new_text, updated_content, count=1)
                        images_described += 1
                        thread_print(f"[Worker {worker_id}] Described {image_file} in {paper_name}")
                    
                    # Rate limiting per worker
                    time.sleep(0.5)  # Shorter delay since we have parallel workers
                    
            except Exception as e:
                error_msg = f"Error with image {image_file} in {paper_name}: {str(e)}"
                thread_print(f"[Worker {worker_id}] {error_msg}")
                with stats_lock:
                    global_stats['errors'].append(error_msg)
        
        # Save if any images were described
        if images_described > 0:
            # Backup original if not already exists
            backup_path = paper_path.parent / f"{paper_path.stem}_backup{paper_path.suffix}"
            if not backup_path.exists():
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Write updated content
            with open(paper_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
        
        return paper_name, images_described, f"Described {images_described}/{len(images_to_process)} images"
        
    except Exception as e:
        error_msg = f"Error processing {paper_name}: {str(e)}"
        with stats_lock:
            global_stats['errors'].append(error_msg)
        return paper_name, 0, f"Error: {str(e)}"

def worker(worker_id, api_key, work_queue, progress_queue):
    """Worker thread that processes papers"""
    thread_print(f"[Worker {worker_id}] Started with API key ending in ...{api_key[-4:]}")
    
    while True:
        try:
            # Get next paper to process (timeout after 5 seconds of no work)
            paper_info = work_queue.get(timeout=5)
            if paper_info is None:  # Poison pill
                break
            
            paper_idx, paper_name, total_papers = paper_info
            paper_path = Path('markdown_papers') / paper_name / 'paper.md'
            
            if not paper_path.exists():
                result = (paper_name, 0, "File not found")
                progress_queue.put((paper_idx, total_papers, worker_id, result))
                continue
            
            # Process the paper
            result = describe_images_in_paper(paper_path, api_key, worker_id)
            
            # Report progress
            progress_queue.put((paper_idx, total_papers, worker_id, result))
            
            # Small delay between papers for the same worker
            time.sleep(1)
            
        except queue.Empty:
            break
        except Exception as e:
            thread_print(f"[Worker {worker_id}] Error: {e}")
    
    thread_print(f"[Worker {worker_id}] Finished")

def progress_reporter(progress_queue, total_papers):
    """Thread that reports progress"""
    start_time = time.time()
    processed = 0
    
    while processed < total_papers:
        try:
            paper_idx, total, worker_id, result = progress_queue.get(timeout=30)
            paper_name, images_count, message = result
            
            processed += 1
            
            # Update global stats
            with stats_lock:
                if images_count > 0:
                    global_stats['processed_papers'] += 1
                    global_stats['total_images'] += images_count
                elif "Error" in message or "not found" in message:
                    global_stats['failed_papers'] += 1
            
            # Calculate ETA
            elapsed = time.time() - start_time
            if processed > 0:
                avg_time = elapsed / processed
                remaining = total_papers - processed
                eta_seconds = avg_time * remaining
                eta_str = f" ETA: {int(eta_seconds//60)}m {int(eta_seconds%60)}s"
            else:
                eta_str = ""
            
            # Print progress
            thread_print(f"[{processed}/{total_papers}]{eta_str} Worker {worker_id}: {paper_name} - {message}")
            
        except queue.Empty:
            thread_print("Progress reporter timeout - workers might be stuck")
            break
    
    return processed

def main():
    """Main function"""
    import sys
    
    # Get list of papers to process
    papers_to_process = []
    
    if len(sys.argv) > 1:
        # Specific papers provided
        papers_to_process = sys.argv[1:]
    else:
        # Get papers from the updated list
        papers_file = Path('papers_for_concurrent_processing.txt')
        if papers_file.exists():
            with open(papers_file, 'r') as f:
                papers_to_process = [line.strip() for line in f if line.strip()]
        else:
            print("No papers list found. Please run update_papers_needing_descriptions.py first")
            return
    
    if not papers_to_process:
        print("No papers to process")
        return
    
    num_workers = min(len(API_KEYS), len(papers_to_process), 3)  # Use up to 3 workers
    
    print(f"Concurrent Image Descriptor (Updated)")
    print(f"="*60)
    print(f"Papers to process: {len(papers_to_process)}")
    print(f"Available API keys: {len(API_KEYS)}")
    print(f"Worker threads: {num_workers}")
    print(f"Format: ![](image) <!-- Image Description: ... -->")
    print(f"="*60)
    
    # Create work queue
    work_queue = queue.Queue()
    progress_queue = queue.Queue()
    
    # Add all papers to work queue
    for idx, paper in enumerate(papers_to_process):
        work_queue.put((idx + 1, paper, len(papers_to_process)))
    
    # Start workers
    with ThreadPoolExecutor(max_workers=num_workers + 1) as executor:
        # Start worker threads
        worker_futures = []
        for i in range(num_workers):
            api_key = API_KEYS[i % len(API_KEYS)]
            future = executor.submit(worker, i + 1, api_key, work_queue, progress_queue)
            worker_futures.append(future)
        
        # Start progress reporter
        reporter_future = executor.submit(progress_reporter, progress_queue, len(papers_to_process))
        
        # Wait for progress reporter to finish
        processed_count = reporter_future.result()
        
        # Send poison pills to workers
        for _ in range(num_workers):
            work_queue.put(None)
        
        # Wait for all workers to finish
        for future in worker_futures:
            future.result()
    
    # Final summary
    print("="*60)
    print(f"PROCESSING COMPLETE")
    print(f"="*60)
    print(f"Papers processed successfully: {global_stats['processed_papers']}")
    print(f"Papers failed: {global_stats['failed_papers']}")
    print(f"Total images described: {global_stats['total_images']}")
    
    if global_stats['errors']:
        print(f"\nErrors encountered:")
        for error in global_stats['errors'][:5]:  # Show first 5 errors
            print(f"  - {error}")
        if len(global_stats['errors']) > 5:
            print(f"  ... and {len(global_stats['errors']) - 5} more errors")
    
    # Save report
    report_file = Path(f'concurrent_image_description_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
    with open(report_file, 'w') as f:
        f.write(f"Concurrent Image Description Report\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"="*60 + "\n")
        f.write(f"Papers to process: {len(papers_to_process)}\n")
        f.write(f"Worker threads: {num_workers}\n")
        f.write(f"Papers processed successfully: {global_stats['processed_papers']}\n")
        f.write(f"Papers failed: {global_stats['failed_papers']}\n")
        f.write(f"Total images described: {global_stats['total_images']}\n")
        if global_stats['errors']:
            f.write(f"\nErrors:\n")
            for error in global_stats['errors']:
                f.write(f"  - {error}\n")
    
    print(f"\nReport saved to: {report_file}")

if __name__ == '__main__':
    main()