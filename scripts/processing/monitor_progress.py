#!/usr/bin/env python3
"""
Monitor the progress of the relevancy analysis script
"""

import json
import os
import time
import csv
from datetime import datetime
from pathlib import Path

def monitor_progress():
    checkpoint_file = "relevancy_checkpoint.json"
    project_root = Path(__file__).parent.parent.parent
    csv_file = project_root / "research_papers_complete.csv"
    
    # Count total papers needing processing
    total_needing_processing = 0
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rel = row.get('Relevancy', '').strip()
            just = row.get('Relevancy Justification', '').strip()
            if not rel or not just or just.lower() in ['', 'none', 'null', 'not available']:
                total_needing_processing += 1
    
    print(f"Total papers needing processing: {total_needing_processing}")
    print("Monitoring progress... (Press Ctrl+C to stop)\n")
    
    while True:
        try:
            if os.path.exists(checkpoint_file):
                with open(checkpoint_file, 'r') as f:
                    checkpoint = json.load(f)
                
                processed = len(checkpoint.get('processed', []))
                percentage = (processed / total_needing_processing * 100) if total_needing_processing > 0 else 0
                
                # Clear line and print progress
                print(f"\r[{datetime.now().strftime('%H:%M:%S')}] "
                      f"Progress: {processed}/{total_needing_processing} papers "
                      f"({percentage:.1f}%) "
                      f"[{'=' * int(percentage/2)}{' ' * (50 - int(percentage/2))}]", 
                      end='', flush=True)
            else:
                print("\rWaiting for processing to start...", end='', flush=True)
            
            time.sleep(5)  # Update every 5 seconds
            
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped.")
            break
        except Exception as e:
            print(f"\nError: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_progress()