"""
Generates descriptions for images in markdown files using Gemini Vision API
CSV version of image_descriptor.py
"""
import sys
import os
import re
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import shutil
import base64

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
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value.strip('"\'')

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import (
    MARKDOWN_DIR, CITE_KEY_MAPPING_FILE, TEST_MODE, TEST_PAPERS,
    BATCH_SIZE, BACKUP_DIR, GEMINI_API_KEY_ENV
)
from utils import (
    setup_logging, load_json, ProgressTracker
)

# Check for environment override
EFFECTIVE_TEST_MODE = TEST_MODE
if os.environ.get('PHASE2_TEST_MODE', '').lower() == 'false':
    EFFECTIVE_TEST_MODE = False


class ImageDescriptor:
    """Handles image description generation"""
    
    def __init__(self, logger, api_key: str):
        self.logger = logger
        self.api_key = api_key
        self.stats = {
            "papers_processed": 0,
            "images_described": 0,
            "images_skipped": 0,
            "images_failed": 0,
            "papers_skipped": 0,
            "errors": 0
        }
        
        # Import Google Generative AI
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.logger.info("Initialized Gemini Vision API")
        except ImportError:
            self.logger.error("google-generativeai package not installed. Install with: pip install google-generativeai")
            self.model = None
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini API: {e}")
            self.model = None
    
    def describe_images_in_paper(self, markdown_path: Path, paper_info: Dict) -> bool:
        """Add descriptions to all images in a markdown file"""
        if not self.model:
            self.logger.error("Gemini API not initialized")
            return False
        
        try:
            # Read markdown content
            with open(markdown_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Find all images to keep
            images_to_keep = paper_info.get("images", {}).get("keep", [])
            if not images_to_keep:
                self.logger.debug(f"No images to describe in {markdown_path.name}")
                return True
            
            # Process each image
            images_processed = 0
            for image_file in images_to_keep:
                try:
                    new_content = self._add_image_description(content, image_file, markdown_path.parent)
                    if new_content != content:
                        content = new_content
                        images_processed += 1
                        self.stats["images_described"] += 1
                    else:
                        self.stats["images_skipped"] += 1
                except Exception as e:
                    self.logger.warning(f"Failed to describe image {image_file}: {e}")
                    self.stats["images_failed"] += 1
                
                # Rate limiting
                time.sleep(0.5)  # Be respectful of API limits
            
            # Write back if changed
            if content != original_content and images_processed > 0:
                # Create backup
                backup_path = BACKUP_DIR / "image_descriptor" / markdown_path.parent.name
                backup_path.mkdir(parents=True, exist_ok=True)
                backup_file = backup_path / f"{markdown_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                shutil.copy2(markdown_path, backup_file)
                
                # Write updated content
                with open(markdown_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.logger.info(f"Added {images_processed} image descriptions to: {markdown_path.name}")
                self.stats["papers_processed"] += 1
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error processing {markdown_path}: {e}")
            self.stats["errors"] += 1
            return False
    
    def _add_image_description(self, content: str, image_file: str, 
                              folder_path: Path) -> str:
        """Add description for a single image"""
        # Check if description already exists
        description_pattern = re.compile(
            r'(!\[[^\]]*\]\(' + re.escape(image_file) + r'\))\s*\n\s*<!--\s*Image\s*Description:.*?-->'
        )
        if description_pattern.search(content):
            self.logger.debug(f"Description already exists for {image_file}")
            return content
        
        # Find the image reference in markdown
        image_pattern = re.compile(
            r'(!\[[^\]]*\]\(' + re.escape(image_file) + r'\))',
            re.MULTILINE
        )
        
        match = image_pattern.search(content)
        if not match:
            self.logger.warning(f"Image reference not found for {image_file}")
            return content
        
        # Get image path
        image_path = folder_path / image_file
        if not image_path.exists():
            self.logger.warning(f"Image file not found: {image_path}")
            return content
        
        # Generate description
        description = self._generate_description(image_path)
        if not description:
            return content
        
        # Add description after image
        image_ref = match.group(1)
        description_comment = f"\n<!-- Image Description: {description} -->"
        
        # Replace image reference with image + description
        new_content = content.replace(
            image_ref,
            image_ref + description_comment
        )
        
        return new_content
    
    def _generate_description(self, image_path: Path) -> Optional[str]:
        """Generate description using Gemini Vision API"""
        try:
            # Read and encode image
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Prepare prompt
            prompt = """Analyze this image from an academic paper and provide a concise description 
            focusing on the technical content. Describe any diagrams, charts, graphs, equations, 
            or technical illustrations. Be specific about what the image shows and its purpose 
            in the context of the paper. Keep the description under 100 words."""
            
            # Import PIL for image handling
            try:
                from PIL import Image
                img = Image.open(image_path)
            except ImportError:
                self.logger.error("PIL not installed. Install with: pip install Pillow")
                return None
            
            # Generate description
            response = self.model.generate_content([prompt, img])
            
            if response.text:
                # Clean up the description
                description = response.text.strip()
                # Remove newlines and excessive spaces
                description = ' '.join(description.split())
                return description
            else:
                self.logger.warning(f"No description generated for {image_path.name}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error generating description for {image_path.name}: {e}")
            return None


def main():
    """Main function to add image descriptions to markdown files"""
    logger = setup_logging("image_descriptor_csv")
    logger.info("Starting image description generation with CSV data")
    
    # Check for API key - first try GEMINI_API_KEYS from .env, then fallback to GOOGLE_API_KEY
    api_keys = os.environ.get('GEMINI_API_KEYS')
    if api_keys:
        # Use the first API key from the list
        api_key = api_keys.split(',')[0].strip()
    else:
        api_key = os.environ.get(GEMINI_API_KEY_ENV)
    
    if not api_key:
        logger.error("Please set GEMINI_API_KEYS in your .env file or GOOGLE_API_KEY environment variable")
        logger.info("Get your API key from: https://makersuite.google.com/app/apikey")
        return 1
    
    # Check if cite key mapping exists
    if not CITE_KEY_MAPPING_FILE.exists():
        logger.error(f"Cite key mapping not found at: {CITE_KEY_MAPPING_FILE}")
        logger.info("Please run paper_analyzer_csv.py first")
        return 1
    
    # Load cite key mapping
    logger.info("Loading cite key mappings...")
    mapping_data = load_json(CITE_KEY_MAPPING_FILE)
    papers_info = mapping_data.get('papers', {})
    
    if not papers_info:
        logger.error("No papers found in cite key mapping")
        return 1
    
    # Filter papers with images
    papers_with_images = {
        folder: info for folder, info in papers_info.items()
        if info.get("images", {}).get("keep")
    }
    
    logger.info(f"Found {len(papers_with_images)} papers with images to process")
    
    # Initialize descriptor
    descriptor = ImageDescriptor(logger, api_key)
    
    if not descriptor.model:
        logger.error("Failed to initialize image descriptor")
        return 1
    
    # Process limit based on mode
    process_limit = TEST_PAPERS if EFFECTIVE_TEST_MODE else len(papers_with_images)
    
    # Create progress tracker
    progress = ProgressTracker(min(process_limit, len(papers_with_images)), logger)
    
    # Process each paper
    processed = 0
    for folder_name, paper_info in papers_with_images.items():
        if processed >= process_limit:
            logger.info(f"{'Test' if EFFECTIVE_TEST_MODE else 'Full'} mode: Processed {processed} papers")
            break
        
        cite_key = paper_info.get("cite_key")
        
        # Find paper directory
        possible_dirs = [
            MARKDOWN_DIR / cite_key,  # Renamed folder
            MARKDOWN_DIR / folder_name,  # Original folder
        ]
        
        paper_dir = None
        for possible_dir in possible_dirs:
            if possible_dir.exists():
                paper_dir = possible_dir
                break
        
        if not paper_dir:
            logger.warning(f"Paper directory not found: {folder_name} or {cite_key}")
            descriptor.stats["papers_skipped"] += 1
            processed += 1
            continue
        
        # Find markdown file
        markdown_file = None
        if paper_info.get("markdown_file"):
            markdown_file = paper_dir / paper_info["markdown_file"]
        
        if not markdown_file or not markdown_file.exists():
            # Try to find any markdown file
            md_files = list(paper_dir.glob("*.md"))
            if md_files:
                markdown_file = md_files[0]
            else:
                logger.warning(f"No markdown file found in: {paper_dir}")
                descriptor.stats["papers_skipped"] += 1
                processed += 1
                continue
        
        # Process images
        progress.update(f"Processing {paper_dir.name}")
        descriptor.describe_images_in_paper(markdown_file, paper_info)
        
        processed += 1
    
    # Print summary
    stats = descriptor.stats
    logger.info("\n" + "="*50)
    logger.info("IMAGE DESCRIPTION SUMMARY")
    logger.info("="*50)
    logger.info(f"Papers processed: {stats['papers_processed']}")
    logger.info(f"Papers skipped: {stats['papers_skipped']}")
    logger.info(f"Images described: {stats['images_described']}")
    logger.info(f"Images skipped: {stats['images_skipped']}")
    logger.info(f"Images failed: {stats['images_failed']}")
    logger.info(f"Errors: {stats['errors']}")
    logger.info("="*50)
    
    if stats['images_described'] > 0:
        logger.info(f"\nEstimated API cost: ~${stats['images_described'] * 0.0001:.2f}")
    
    return 0 if stats['errors'] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())