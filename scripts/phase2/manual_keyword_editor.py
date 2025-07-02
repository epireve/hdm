#!/usr/bin/env python3
"""
Script to help manually edit keywords in markdown files
Opens files one by one for manual editing
"""
import sys
import os
from pathlib import Path
import subprocess
import time

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import MARKDOWN_DIR
from utils import setup_logging


def open_file_in_editor(file_path: Path) -> None:
    """Open a file in the default editor"""
    # Try different methods to open the file
    if sys.platform == "darwin":  # macOS
        subprocess.run(["open", str(file_path)])
    elif sys.platform == "win32":  # Windows
        os.startfile(str(file_path))
    else:  # Linux and others
        subprocess.run(["xdg-open", str(file_path)])


def main():
    """Main function"""
    logger = setup_logging("manual_keyword_editor")
    
    # Find all markdown files
    markdown_files = []
    for folder in MARKDOWN_DIR.iterdir():
        if folder.is_dir():
            for md_file in folder.glob("*.md"):
                markdown_files.append(md_file)
    
    logger.info(f"Found {len(markdown_files)} markdown files")
    
    print("\n" + "="*60)
    print("MANUAL KEYWORD EDITOR")
    print("="*60)
    print(f"Total files to process: {len(markdown_files)}")
    print("\nInstructions:")
    print("1. Each file will be opened for you to edit")
    print("2. Look for the 'keywords:' section in the YAML frontmatter")
    print("3. Edit the keywords based on the abstract content")
    print("4. Save and close the file")
    print("5. Press Enter to proceed to the next file")
    print("6. Type 'skip' to skip a file")
    print("7. Type 'quit' to exit")
    print("="*60)
    
    input("\nPress Enter to start...")
    
    for i, md_file in enumerate(markdown_files, 1):
        print(f"\n[{i}/{len(markdown_files)}] Opening: {md_file.parent.name}/{md_file.name}")
        
        # Open the file
        try:
            open_file_in_editor(md_file)
            logger.info(f"Opened {md_file.name} for editing")
        except Exception as e:
            logger.error(f"Error opening {md_file}: {e}")
            print(f"Error: Could not open file. {e}")
            continue
        
        # Wait for user input
        while True:
            user_input = input("\nPress Enter when done (or 'skip' to skip, 'quit' to exit): ").strip().lower()
            
            if user_input == "":
                logger.info(f"Completed editing {md_file.name}")
                break
            elif user_input == "skip":
                logger.info(f"Skipped {md_file.name}")
                break
            elif user_input == "quit":
                logger.info("User requested exit")
                print("\nExiting...")
                return
            else:
                print("Invalid input. Press Enter, type 'skip', or type 'quit'")
    
    print("\n" + "="*60)
    print("All files processed!")
    print("="*60)


if __name__ == "__main__":
    main()