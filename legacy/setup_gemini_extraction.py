#!/usr/bin/env python3
"""
Setup script for Gemini-based author extraction.
"""

import subprocess
import sys
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def install_required_packages():
    """Install required packages for Gemini API."""
    packages = [
        'google-generativeai',
    ]
    
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
            logger.info(f"✅ {package} already installed")
        except ImportError:
            logger.info(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            logger.info(f"✅ {package} installed")

def setup_api_key():
    """Setup API key for Gemini."""
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if api_key:
        logger.info("✅ GOOGLE_API_KEY found in environment")
        return True
    
    print("\n🔑 GOOGLE_API_KEY not found in environment")
    print("To use Gemini Flash for author extraction, you need to:")
    print("1. Get a Google AI API key from: https://makersuite.google.com/app/apikey")
    print("2. Set it as an environment variable:")
    print("   export GOOGLE_API_KEY='your-api-key-here'")
    print("3. Or create a .env file with: GOOGLE_API_KEY=your-api-key-here")
    
    # Try to load from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key:
            logger.info("✅ Loaded GOOGLE_API_KEY from .env file")
            return True
    except ImportError:
        print("4. Or install python-dotenv: pip install python-dotenv")
    
    return False

def check_papers_directory():
    """Check if markdown_papers directory exists."""
    papers_dir = "markdown_papers"
    
    if os.path.exists(papers_dir):
        # Count paper directories
        paper_count = len([d for d in os.listdir(papers_dir) 
                          if os.path.isdir(os.path.join(papers_dir, d))])
        logger.info(f"✅ Found {papers_dir} with {paper_count} paper directories")
        return True
    else:
        logger.warning(f"❌ {papers_dir} directory not found")
        print(f"Expected directory structure: {papers_dir}/paper_cite_key/paper.md")
        return False

def main():
    """Run setup checks."""
    print("🔧 SETTING UP GEMINI AUTHOR EXTRACTION")
    print("=" * 50)
    
    # Install packages
    print("\n1. Installing required packages...")
    install_required_packages()
    
    # Check API key
    print("\n2. Checking API key...")
    api_key_ok = setup_api_key()
    
    # Check papers directory
    print("\n3. Checking papers directory...")
    papers_ok = check_papers_directory()
    
    print("\n📊 SETUP STATUS:")
    print(f"   Packages installed: ✅")
    print(f"   API key configured: {'✅' if api_key_ok else '❌'}")
    print(f"   Papers directory: {'✅' if papers_ok else '❌'}")
    
    if api_key_ok and papers_ok:
        print("\n✅ Ready to run author extraction!")
        print("   Run: python extract_authors_from_papers.py")
    else:
        print("\n⚠️  Setup incomplete - please address the issues above")

if __name__ == "__main__":
    main()