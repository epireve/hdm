#!/usr/bin/env python3
"""
Dual Mode PDF to Markdown Converter
Generates BOTH image descriptions AND extracts image files
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import re
import json
import time

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def run_marker_command(cmd, description):
    """Run a marker command and return success status"""
    print(f"\n{description}")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, 
                              capture_output=True, 
                              text=True, 
                              timeout=300,  # 5 minutes max
                              env={**os.environ, 'GOOGLE_API_KEY': GOOGLE_API_KEY})
        
        if result.returncode == 0:
            print("✓ Success")
            return True, result.stdout
        else:
            print(f"✗ Failed: {result.stderr}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print("✗ Timeout")
        return False, "Timeout"
    except Exception as e:
        print(f"✗ Error: {e}")
        return False, str(e)

def dual_mode_conversion(pdf_path, output_dir):
    """
    Perform dual-mode conversion:
    1. Generate descriptions with LLM
    2. Extract images
    3. Merge results
    """
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Create temp directories
    temp_desc_dir = output_dir / "temp_descriptions"
    temp_img_dir = output_dir / "temp_images"
    temp_desc_dir.mkdir(exist_ok=True)
    temp_img_dir.mkdir(exist_ok=True)
    
    # Create temp input directories with single PDF
    desc_input = temp_desc_dir / "input"
    img_input = temp_img_dir / "input"
    desc_input.mkdir(exist_ok=True)
    img_input.mkdir(exist_ok=True)
    
    # Copy PDF to both temp directories
    shutil.copy2(pdf_path, desc_input / pdf_path.name)
    shutil.copy2(pdf_path, img_input / pdf_path.name)
    
    print(f"\n{'='*60}")
    print(f"DUAL MODE CONVERSION: {pdf_path.name}")
    print(f"{'='*60}")
    
    # Step 1: Generate descriptions with LLM (no images)
    desc_cmd = [
        './venv/bin/marker',
        str(desc_input),
        '--output_dir', str(temp_desc_dir),
        '--use_llm',
        '--format_lines',
        '--disable_image_extraction',  # This makes LLM generate descriptions
        '--max_files', '1'
    ]
    
    success1, _ = run_marker_command(desc_cmd, "Step 1: Generating image descriptions with LLM...")
    
    # Step 2: Extract images (no LLM)
    img_cmd = [
        './venv/bin/marker',
        str(img_input),
        '--output_dir', str(temp_img_dir),
        '--format_lines',
        '--extract_images', 'True',
        '--max_files', '1'
    ]
    
    success2, _ = run_marker_command(img_cmd, "Step 2: Extracting images...")
    
    if not (success1 and success2):
        print("\n❌ Conversion failed")
        return False
    
    # Step 3: Merge results
    print("\nStep 3: Merging descriptions and images...")
    
    # Find generated files
    desc_md = list(temp_desc_dir.rglob(f"{pdf_path.stem}.md"))
    img_md = list(temp_img_dir.rglob(f"{pdf_path.stem}.md"))
    
    if not desc_md or not img_md:
        print("❌ Could not find generated markdown files")
        return False
    
    desc_md_path = desc_md[0]
    img_md_path = img_md[0]
    img_dir = img_md_path.parent
    
    # Read both markdown files
    with open(desc_md_path, 'r', encoding='utf-8') as f:
        desc_content = f.read()
    
    with open(img_md_path, 'r', encoding='utf-8') as f:
        img_content = f.read()
    
    # Create final output directory
    final_dir = output_dir / pdf_path.stem
    final_dir.mkdir(exist_ok=True)
    
    # Copy all images to final directory
    image_files = []
    for ext in ['*.jpeg', '*.jpg', '*.png', '*.gif', '*.svg']:
        for img_file in img_dir.glob(ext):
            shutil.copy2(img_file, final_dir / img_file.name)
            image_files.append(img_file.name)
    
    print(f"✓ Copied {len(image_files)} images")
    
    # Process markdown to merge descriptions with image references
    final_content = merge_markdown_content(desc_content, img_content, image_files)
    
    # Write final markdown
    final_md_path = final_dir / f"{pdf_path.stem}.md"
    with open(final_md_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"✓ Created enhanced markdown: {final_md_path}")
    
    # Cleanup temp directories
    shutil.rmtree(temp_desc_dir, ignore_errors=True)
    shutil.rmtree(temp_img_dir, ignore_errors=True)
    
    print(f"\n✅ Dual mode conversion complete!")
    print(f"Output: {final_dir}")
    
    return True

def merge_markdown_content(desc_content, img_content, image_files):
    """
    Merge description content with image content
    Replace image placeholders with enhanced format
    """
    # Extract image descriptions from desc_content
    # These appear as plain text where images would be
    desc_lines = desc_content.split('\n')
    img_lines = img_content.split('\n')
    
    # Find image references in img_content
    img_pattern = r'!\[(.*?)\]\((.*?)\)'
    
    # Build a mapping of image positions to descriptions
    # This is a simplified approach - in production you'd want more sophisticated matching
    final_lines = []
    desc_idx = 0
    
    for img_line in img_lines:
        img_match = re.search(img_pattern, img_line)
        
        if img_match:
            # This line has an image reference
            alt_text = img_match.group(1)
            img_path = img_match.group(2)
            
            # Find corresponding description in desc_content
            # Look for descriptive text that might replace this image
            description = ""
            
            # Simple heuristic: find non-empty lines in desc_content 
            # at similar positions that aren't in img_content
            while desc_idx < len(desc_lines):
                desc_line = desc_lines[desc_idx].strip()
                desc_idx += 1
                
                # If this line looks like a description (has substantial text)
                # and doesn't appear in img_content
                if (len(desc_line) > 50 and 
                    desc_line not in img_content and
                    'figure' in desc_line.lower() or 'image' in desc_line.lower() or
                    'chart' in desc_line.lower() or 'diagram' in desc_line.lower()):
                    description = desc_line
                    break
            
            # Create enhanced image reference
            if description:
                # Format: image with description
                enhanced_line = f"![{alt_text}]({img_path})\n\n**Image Description:** {description}\n"
            else:
                # Keep original if no description found
                enhanced_line = img_line
            
            final_lines.append(enhanced_line)
        else:
            # Regular text line
            final_lines.append(img_line)
    
    return '\n'.join(final_lines)

def test_dual_mode():
    """Test dual mode conversion with a sample PDF"""
    papers_dir = Path('papers')
    output_dir = Path('dual_mode_output')
    
    # Get a PDF to test - use a specific one we know has content
    test_pdf = papers_dir / "1-s2.0-S0010027720302353-main.pdf"
    if not test_pdf.exists():
        # Fallback to any PDF with reasonable size
        pdf_files = [p for p in papers_dir.glob('*.pdf') if p.stat().st_size > 100000]
        if not pdf_files:
            print("No valid PDF files found!")
            return
        test_pdf = sorted(pdf_files, key=lambda p: p.stat().st_size)[0]
    
    print(f"PDF size: {test_pdf.stat().st_size / 1024 / 1024:.1f} MB")
    
    print(f"Testing dual mode conversion with: {test_pdf.name}")
    success = dual_mode_conversion(test_pdf, output_dir)
    
    if success:
        # Show sample of result
        result_dir = output_dir / test_pdf.stem
        result_md = result_dir / f"{test_pdf.stem}.md"
        
        if result_md.exists():
            with open(result_md, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print("\nSample output (first 1000 chars):")
            print("-" * 60)
            print(content[:1000])
            print("-" * 60)
            
            # Count images
            img_count = len(list(result_dir.glob('*.jpeg')) + list(result_dir.glob('*.png')))
            print(f"\nImages extracted: {img_count}")

if __name__ == "__main__":
    test_dual_mode()