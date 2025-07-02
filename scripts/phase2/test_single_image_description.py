#!/usr/bin/env python3
"""
Test image description on a single paper
This helps verify the setup before processing all papers
"""
import sys
import os
from pathlib import Path

# Try to load from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If dotenv not available, try to load manually
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"\'')

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from improved_author_extractor import extract_clean_authors, extract_title_from_markdown


def test_single_paper():
    """Test image description on a single paper"""
    
    # Check for API key
    api_keys = os.environ.get('GEMINI_API_KEYS')
    if not api_keys:
        print("❌ Error: GEMINI_API_KEYS not set in .env file")
        print("\nPlease set your API key in .env file:")
        print("GEMINI_API_KEYS='your-api-key-here'")
        return 1
    
    # Use the first API key from the list
    api_key = api_keys.split(',')[0].strip()
    
    print("✓ API key found")
    
    # Check if packages are installed
    try:
        import google.generativeai as genai
        print("✓ google-generativeai installed")
    except ImportError:
        print("❌ google-generativeai not installed")
        print("Run: pip install google-generativeai")
        return 1
    
    try:
        from PIL import Image
        print("✓ Pillow installed")
    except ImportError:
        print("❌ Pillow not installed")
        print("Run: pip install Pillow")
        return 1
    
    # Find a paper with images to test
    test_paper = Path("markdown_papers/1-s2.0-S0378778821011129-am/1-s2.0-S0378778821011129-am.md")
    
    if not test_paper.exists():
        # Try to find any paper with images
        print("\nLooking for a paper with images...")
        import json
        mapping_file = Path("cite_key_mapping.json")
        
        if mapping_file.exists():
            with open(mapping_file) as f:
                data = json.load(f)
            
            # Find first paper with images
            for folder, info in data['papers'].items():
                if info.get('images', {}).get('keep'):
                    paper_dir = Path("markdown_papers") / folder
                    if paper_dir.exists():
                        md_files = list(paper_dir.glob("*.md"))
                        if md_files:
                            test_paper = md_files[0]
                            break
    
    if not test_paper.exists():
        print("❌ No test paper found")
        return 1
    
    print(f"\n📄 Testing on: {test_paper}")
    
    # Extract paper info
    title = extract_title_from_markdown(test_paper)
    authors = extract_clean_authors(test_paper)
    
    print(f"📚 Title: {title}")
    print(f"👥 Authors: {authors}")
    
    # Count images
    with open(test_paper, 'r', encoding='utf-8') as f:
        content = f.read()
    
    import re
    images = re.findall(r'!\[.*?\]\((.+?)\)', content)
    print(f"🖼️  Images found: {len(images)}")
    
    if not images:
        print("No images to process in this paper")
        return 1
    
    # Test image description on first image
    print(f"\n🔍 Testing image description on: {images[0]}")
    
    try:
        # Initialize Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Try to describe first image
        image_path = test_paper.parent / images[0]
        if image_path.exists():
            print(f"📁 Image path: {image_path}")
            
            # Load image
            img = Image.open(image_path)
            print(f"📐 Image size: {img.size}")
            
            # Generate description
            prompt = """Analyze this image from an academic paper and provide a concise description 
            focusing on the technical content. Describe any diagrams, charts, graphs, equations, 
            or technical illustrations. Be specific about what the image shows and its purpose 
            in the context of the paper. Keep the description under 100 words."""
            
            print("\n🤖 Generating description...")
            response = model.generate_content([prompt, img])
            
            if response.text:
                print("\n✨ Generated description:")
                print("-" * 50)
                print(response.text.strip())
                print("-" * 50)
                print("\n✅ Test successful! The image descriptor is working correctly.")
                
                # Show how it would look in markdown
                print("\n📝 How it will appear in the markdown file:")
                print(f"![...]({images[0]})")
                print(f"<!-- Image Description: {response.text.strip()} -->")
                
                return 0
            else:
                print("❌ No description generated")
                return 1
                
        else:
            print(f"❌ Image file not found: {image_path}")
            return 1
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPossible issues:")
        print("1. Invalid API key")
        print("2. API quota exceeded")
        print("3. Network connection issues")
        print("4. Image format not supported")
        return 1


if __name__ == "__main__":
    print("=================================")
    print("Single Paper Image Description Test")
    print("=================================")
    
    result = test_single_paper()
    
    if result == 0:
        print("\n🎉 Test passed! You can now run the full image description process:")
        print("\nFor test mode (5 papers):")
        print("python scripts/phase2/run_phase2_csv.py --test --step describe-images")
        print("\nFor full mode (all papers):")
        print("python scripts/phase2/run_phase2_csv.py --full --step describe-images")
    else:
        print("\n⚠️  Please fix the issues above before running the full process.")
    
    sys.exit(result)