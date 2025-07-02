#!/usr/bin/env python3
"""
Monitor conversion progress
"""

import os
import json
import time
from pathlib import Path

def main():
    while True:
        # Count markdown files
        markdown_files = list(Path('markdown_papers').glob('**/*.md'))
        
        # Check checkpoints
        checkpoints = []
        for checkpoint_file in Path('.').glob('*checkpoint.json'):
            if checkpoint_file.exists():
                with open(checkpoint_file) as f:
                    data = json.load(f)
                    checkpoints.append({
                        'file': checkpoint_file.name,
                        'completed': len(data.get('completed', [])),
                        'failed': len(data.get('failed', {}))
                    })
        
        # Clear screen and show status
        os.system('clear')
        print("="*60)
        print("PDF TO MARKDOWN CONVERSION MONITOR")
        print("="*60)
        print(f"Markdown files created: {len(markdown_files)}")
        print()
        
        for cp in checkpoints:
            print(f"{cp['file']}:")
            print(f"  Completed: {cp['completed']}")
            print(f"  Failed: {cp['failed']}")
            print()
        
        print("Recent conversions:")
        recent = sorted(markdown_files, key=lambda p: p.stat().st_mtime, reverse=True)[:5]
        for md in recent:
            print(f"  - {md.parent.name}/{md.name}")
        
        print("\nPress Ctrl+C to exit")
        time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")