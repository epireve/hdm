#!/usr/bin/env python3
"""
Multiprocess image descriptor - uses multiple processes for maximum speed
Each process gets its own API key and processes papers independently
"""
import os
import re
import time
import json
from pathlib import Path
from datetime import datetime
from multiprocessing import Pool, Queue, Manager, cpu_count
import signal

# Load environment variables before importing genai
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

def init_worker(worker_id, api_key):
    """Initialize worker process with its own API key"""
    # Import in worker process
    global genai, Image
    import google.generativeai as genai
    from PIL import Image
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    
    # Configure API for this worker
    genai.configure(api_key=api_key)
    
    # Store worker info
    global WORKER_ID, MODEL
    WORKER_ID = worker_id
    MODEL = genai.GenerativeModel('gemini-1.5-flash')

def has_image_description(content, image_file):
    """Check if an image already has a description comment"""
    pattern = rf'!\[\]\({re.escape(image_file)}\)\s*\n\s*<!-- Image Description:.*?-->'
    return bool(re.search(pattern, content, re.DOTALL))

def process_paper(args):
    """Process a single paper - runs in worker process"""
    paper_idx, paper_name, total_papers = args
    start_time = time.time()
    
    try:
        paper_path = Path('markdown_papers') / paper_name / 'paper.md'
        
        if not paper_path.exists():
            return {
                'paper': paper_name,
                'worker': WORKER_ID,
                'success': False,
                'images': 0,
                'message': 'File not found',
                'time': time.time() - start_time
            }
        
        # Read the markdown content
        with open(paper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all images with empty alt text
        image_pattern = r'!\[\]\(([^)]+)\)'
        empty_images = re.findall(image_pattern, content)
        
        if not empty_images:
            return {
                'paper': paper_name,
                'worker': WORKER_ID,
                'success': True,
                'images': 0,
                'message': 'No images with empty alt text',
                'time': time.time() - start_time
            }
        
        # Filter out images that already have descriptions
        images_to_process = []
        for image_file in empty_images:
            if not has_image_description(content, image_file):
                images_to_process.append(image_file)
        
        if not images_to_process:
            return {
                'paper': paper_name,
                'worker': WORKER_ID,
                'success': True,
                'images': 0,
                'message': 'All images already have descriptions',
                'time': time.time() - start_time
            }
        
        # Process each image
        updated_content = content
        images_described = 0
        
        for image_file in images_to_process:
            image_path = paper_path.parent / image_file
            if not image_path.exists():
                continue
            
            try:
                # Load and describe the image
                img = Image.open(image_path)
                
                prompt = """Analyze this image from an academic paper and provide a concise description 
                focusing on the technical content. Describe any diagrams, charts, graphs, equations, 
                or technical illustrations. Be specific about what the image shows and its purpose 
                in the context of the paper. Keep the description under 100 words."""
                
                response = MODEL.generate_content([prompt, img])
                
                if response.text:
                    description = response.text.strip().replace('\n', ' ')
                    
                    # Find the image reference and add description comment after it
                    old_pattern = rf'(!\[\]\({re.escape(image_file)}\))'
                    new_text = f'![]({image_file})\n<!-- Image Description: {description} -->'
                    
                    # Replace only if not already has description
                    if not has_image_description(updated_content, image_file):
                        updated_content = re.sub(old_pattern, new_text, updated_content, count=1)
                        images_described += 1
                    
                    # Rate limiting
                    time.sleep(0.3)  # Shorter delay with multiple processes
                    
            except Exception as e:
                pass  # Continue with other images
        
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
        
        return {
            'paper': paper_name,
            'worker': WORKER_ID,
            'success': True,
            'images': images_described,
            'message': f'Described {images_described}/{len(images_to_process)} images',
            'time': time.time() - start_time
        }
        
    except Exception as e:
        return {
            'paper': paper_name,
            'worker': WORKER_ID,
            'success': False,
            'images': 0,
            'message': f'Error: {str(e)}',
            'time': time.time() - start_time
        }

def main():
    """Main function"""
    import sys
    
    # Check for required packages
    try:
        import google.generativeai
        from PIL import Image
    except ImportError:
        print("Error: Required packages not installed")
        print("Please run: pip install google-generativeai pillow")
        return
    
    # Get list of papers to process
    papers_to_process = []
    
    if len(sys.argv) > 1:
        papers_to_process = sys.argv[1:]
    else:
        papers_file = Path('papers_needing_image_descriptions.txt')
        if papers_file.exists():
            with open(papers_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('=') and not line.startswith('Papers'):
                        papers_to_process.append(line)
        
        # Exclude already processed papers
        processed = ['li_2022', 'xie_2024a']
        papers_to_process = [p for p in papers_to_process if p not in processed]
    
    if not papers_to_process:
        print("No papers to process")
        return
    
    # Determine number of processes
    num_processes = min(len(API_KEYS), cpu_count(), 4)  # Max 4 processes
    
    print(f"Multiprocess Image Descriptor")
    print(f"="*60)
    print(f"Papers to process: {len(papers_to_process)}")
    print(f"Available API keys: {len(API_KEYS)}")
    print(f"CPU cores: {cpu_count()}")
    print(f"Worker processes: {num_processes}")
    print(f"="*60)
    
    # Prepare work items
    work_items = [(i+1, paper, len(papers_to_process)) 
                  for i, paper in enumerate(papers_to_process)]
    
    # Stats
    stats = {
        'processed': 0,
        'failed': 0,
        'total_images': 0,
        'start_time': time.time()
    }
    
    try:
        # Create process pool with initializer
        with Pool(
            processes=num_processes,
            initializer=init_worker,
            initargs=[(i+1, API_KEYS[i % len(API_KEYS)]) for i in range(num_processes)]
        ) as pool:
            
            # Process papers asynchronously
            results = []
            for i in range(0, len(work_items), num_processes):
                batch = work_items[i:i+num_processes]
                
                # Assign each item to a specific worker
                for j, item in enumerate(batch):
                    worker_id = (j % num_processes) + 1
                    result = pool.apply_async(
                        process_paper,
                        args=(item,),
                        callback=lambda x: print_progress(x, stats, len(papers_to_process))
                    )
                    results.append(result)
            
            # Wait for all results
            pool.close()
            pool.join()
    
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        pool.terminate()
        pool.join()
    
    # Final summary
    elapsed = time.time() - stats['start_time']
    print("\n" + "="*60)
    print(f"PROCESSING COMPLETE")
    print(f"="*60)
    print(f"Total time: {int(elapsed//60)}m {int(elapsed%60)}s")
    print(f"Papers processed: {stats['processed']}")
    print(f"Papers failed: {stats['failed']}")
    print(f"Total images described: {stats['total_images']}")
    print(f"Average time per paper: {elapsed/len(papers_to_process):.1f}s")
    
    # Save report
    report_file = Path(f'multiprocess_image_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
    with open(report_file, 'w') as f:
        f.write(f"Multiprocess Image Description Report\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"="*60 + "\n")
        f.write(f"Papers processed: {stats['processed']}\n")
        f.write(f"Papers failed: {stats['failed']}\n")
        f.write(f"Total images described: {stats['total_images']}\n")
        f.write(f"Total time: {int(elapsed//60)}m {int(elapsed%60)}s\n")
        f.write(f"Worker processes: {num_processes}\n")
    
    print(f"\nReport saved to: {report_file}")

def print_progress(result, stats, total):
    """Print progress update"""
    stats['processed'] += 1
    if result['success'] and result['images'] > 0:
        stats['total_images'] += result['images']
    elif not result['success']:
        stats['failed'] += 1
    
    # Calculate ETA
    elapsed = time.time() - stats['start_time']
    avg_time = elapsed / stats['processed']
    remaining = total - stats['processed']
    eta = int(avg_time * remaining)
    
    print(f"[{stats['processed']}/{total}] Worker {result['worker']}: "
          f"{result['paper']} - {result['message']} "
          f"({result['time']:.1f}s) ETA: {eta//60}m {eta%60}s")

if __name__ == '__main__':
    main()