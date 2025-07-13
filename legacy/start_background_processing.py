#!/usr/bin/env python3
"""
Background processing launcher for paper reformatting
Runs reformatting in background and provides progress monitoring
"""

import os
import sys
import time
import signal
import subprocess
from pathlib import Path
from datetime import datetime

def run_background_processing():
    """Start background processing and monitor progress"""
    
    print("🚀 Starting Background Paper Reformatting")
    print("="*50)
    
    # Configuration
    output_dir = f"production_reformatted_batch_{int(time.time())}"
    max_papers = 50
    max_workers = 2
    
    # Create command
    cmd = [
        sys.executable, "scripts/simple_reformatter.py",
        "--max-papers", str(max_papers),
        "--max-workers", str(max_workers), 
        "--output-dir", output_dir
    ]
    
    print(f"📚 Processing: {max_papers} papers")
    print(f"⚡ Workers: {max_workers}")
    print(f"📁 Output: {output_dir}")
    print(f"🤖 Model: google/gemini-2.5-flash")
    print()
    
    # Start background process
    log_file = f"reformatter_log_{int(time.time())}.log"
    print(f"📝 Logs: {log_file}")
    print(f"🔄 Starting background process...")
    
    try:
        with open(log_file, 'w') as f:
            process = subprocess.Popen(
                cmd,
                stdout=f,
                stderr=subprocess.STDOUT,
                cwd=os.getcwd()
            )
        
        print(f"✅ Background process started (PID: {process.pid})")
        print(f"📊 Monitor progress with: tail -f {log_file}")
        print(f"🛑 Stop with: kill {process.pid}")
        print()
        
        # Monitor for initial startup
        print("⏳ Initial startup monitoring (60 seconds)...")
        for i in range(12):
            time.sleep(5)
            
            # Check if process is still running
            if process.poll() is not None:
                print(f"❌ Process exited with code: {process.returncode}")
                break
                
            # Show log tail
            try:
                result = subprocess.run(
                    ["tail", "-n", "3", log_file],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.stdout.strip():
                    print(f"📄 Latest: {result.stdout.strip().split()[-1] if result.stdout.strip() else 'Starting...'}")
            except:
                pass
        
        if process.poll() is None:
            print()
            print("🎯 Background processing is running successfully!")
            print(f"📊 Monitor: tail -f {log_file}")
            print(f"📁 Output: {output_dir}")
            print(f"🛑 Stop: kill {process.pid}")
            return True
        
    except Exception as e:
        print(f"❌ Failed to start background process: {e}")
        return False
    
    return False

def main():
    """Main function"""
    try:
        success = run_background_processing()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        return 1

if __name__ == "__main__":
    exit(main())