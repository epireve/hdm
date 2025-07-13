#!/usr/bin/env python3
"""
Real-time progress monitor for paper reformatting
"""

import os
import time
import re
from pathlib import Path
from datetime import datetime

def parse_log_file(log_file):
    """Parse log file for progress information"""
    if not Path(log_file).exists():
        return {}
    
    progress = {
        "completed": [],
        "processing": [],
        "total_found": 0,
        "start_time": None,
        "last_update": None
    }
    
    try:
        with open(log_file, 'r') as f:
            content = f.read()
        
        # Extract total papers found
        total_match = re.search(r'📚 Found (\d+) papers to process', content)
        if total_match:
            progress["total_found"] = int(total_match.group(1))
        
        # Extract start time
        first_line = content.split('\n')[0] if content else ""
        if first_line:
            try:
                time_str = first_line.split(' - ')[0]
                progress["start_time"] = datetime.fromisoformat(time_str)
            except:
                pass
        
        # Extract completed papers
        completed_pattern = r'✅ (\w+): Completed in ([\d.]+)s \((\d+) chars/sec\)'
        completed_matches = re.findall(completed_pattern, content)
        for match in completed_matches:
            cite_key, time_taken, chars_per_sec = match
            progress["completed"].append({
                "cite_key": cite_key,
                "time_taken": float(time_taken),
                "chars_per_sec": int(chars_per_sec)
            })
        
        # Extract currently processing
        processing_pattern = r'🔄 (\w+): Processing ([\d,]+) chars'
        processing_matches = re.findall(processing_pattern, content)
        
        # Get the latest processing entries
        latest_processing = {}
        for match in processing_matches:
            cite_key, chars = match
            latest_processing[cite_key] = int(chars.replace(',', ''))
        
        # Remove completed papers from processing
        completed_keys = {p["cite_key"] for p in progress["completed"]}
        for cite_key, chars in latest_processing.items():
            if cite_key not in completed_keys:
                progress["processing"].append({
                    "cite_key": cite_key,
                    "chars": chars
                })
        
        progress["last_update"] = datetime.now()
        
    except Exception as e:
        print(f"Error parsing log: {e}")
    
    return progress

def format_duration(seconds):
    """Format duration in human readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds//60:.0f}m {seconds%60:.0f}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours:.0f}h {minutes:.0f}m"

def display_progress(log_file, output_dir):
    """Display real-time progress"""
    print("📊 Paper Reformatting Progress Monitor")
    print("="*50)
    
    while True:
        try:
            progress = parse_log_file(log_file)
            
            # Clear screen (simple version)
            os.system('clear' if os.name == 'posix' else 'cls')
            
            print("📊 Paper Reformatting Progress Monitor")
            print("="*50)
            print(f"🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}")
            print()
            
            if progress.get("start_time"):
                elapsed = (datetime.now() - progress["start_time"]).total_seconds()
                print(f"⏱️  Running time: {format_duration(elapsed)}")
            
            completed_count = len(progress.get("completed", []))
            processing_count = len(progress.get("processing", []))
            total_found = progress.get("total_found", 0)
            
            print(f"📚 Progress: {completed_count}/{total_found} papers completed")
            print(f"🔄 Currently processing: {processing_count} papers")
            print()
            
            # Show completed papers
            if progress.get("completed"):
                print("✅ Completed Papers:")
                total_time = sum(p["time_taken"] for p in progress["completed"])
                avg_speed = sum(p["chars_per_sec"] for p in progress["completed"]) / len(progress["completed"])
                
                for paper in progress["completed"][-5:]:  # Show last 5
                    print(f"   {paper['cite_key']:<20} {paper['time_taken']:>6.1f}s  {paper['chars_per_sec']:>5} chars/sec")
                
                print(f"   📊 Average speed: {avg_speed:.0f} chars/sec")
                print(f"   ⏱️  Total processing time: {format_duration(total_time)}")
                print()
            
            # Show currently processing
            if progress.get("processing"):
                print("🔄 Currently Processing:")
                for paper in progress["processing"]:
                    print(f"   {paper['cite_key']:<20} {paper['chars']:>8,} chars")
                print()
            
            # Show output directory status
            if Path(output_dir).exists():
                output_folders = [d for d in Path(output_dir).iterdir() if d.is_dir()]
                print(f"📁 Output folder: {len(output_folders)} papers saved")
                print(f"   Location: {output_dir}")
                print()
            
            # Calculate ETA if we have data
            if completed_count > 0 and total_found > 0:
                if progress.get("start_time"):
                    elapsed = (datetime.now() - progress["start_time"]).total_seconds()
                    rate = completed_count / elapsed if elapsed > 0 else 0
                    remaining = total_found - completed_count
                    eta_seconds = remaining / rate if rate > 0 else 0
                    
                    if eta_seconds > 0:
                        print(f"🎯 Estimated completion: {format_duration(eta_seconds)}")
                        print()
            
            print("Press Ctrl+C to exit monitor")
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\n👋 Monitor stopped")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Monitor paper reformatting progress")
    parser.add_argument("--log-file", default="reformatter_log_1752361694.log", help="Log file to monitor")
    parser.add_argument("--output-dir", default="production_reformatted_batch_1752361694", help="Output directory to check")
    
    args = parser.parse_args()
    
    if not Path(args.log_file).exists():
        print(f"❌ Log file not found: {args.log_file}")
        return 1
    
    display_progress(args.log_file, args.output_dir)
    return 0

if __name__ == "__main__":
    exit(main())