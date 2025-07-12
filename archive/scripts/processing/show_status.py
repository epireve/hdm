#!/usr/bin/env python3
"""
Show conversion status
"""

import json
from pathlib import Path

def main():
    print("="*70)
    print("PDF TO MARKDOWN CONVERSION STATUS")
    print("="*70)
    
    # Get total PDFs
    pdf_files = list(Path('papers').glob('*.pdf'))
    pdf_files = [p for p in pdf_files if p.stat().st_size >= 100 * 1024]
    total_pdfs = len(pdf_files)
    
    # Count actual conversions
    md_files = list(Path('markdown_papers').glob('**/*.md'))
    actual_converted = len(md_files)
    
    # Check checkpoint
    checkpoint_file = Path('reliable_checkpoint.json')
    if checkpoint_file.exists():
        with open(checkpoint_file) as f:
            checkpoint = json.load(f)
        
        recorded_completed = len(checkpoint.get('completed', []))
        recorded_failed = len(checkpoint.get('failed', {}))
        
        print(f"Total PDFs found: {total_pdfs}")
        print(f"Checkpoint shows:")
        print(f"  - Completed: {recorded_completed}")
        print(f"  - Failed: {recorded_failed}")
        print(f"  - Remaining: {total_pdfs - recorded_completed - recorded_failed}")
        print(f"\nActual markdown files created: {actual_converted}")
        
        # Progress bar
        percent = (recorded_completed / total_pdfs) * 100 if total_pdfs > 0 else 0
        bar_length = 50
        filled = int(bar_length * percent / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\nProgress: [{bar}] {percent:.1f}%")
        
        # Show recent conversions
        if md_files:
            print("\nRecent conversions:")
            recent = sorted(md_files, key=lambda p: p.stat().st_mtime, reverse=True)[:5]
            for md in recent:
                print(f"  - {md.parent.name}")
        
        # Show failed files
        if checkpoint.get('failed'):
            print("\nFailed conversions:")
            for pdf, error in checkpoint['failed'].items():
                print(f"  - {Path(pdf).name}: {error}")
    else:
        print("No checkpoint file found!")

if __name__ == "__main__":
    main()