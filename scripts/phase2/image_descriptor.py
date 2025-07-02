"""
Generates descriptions for images in markdown files using Gemini Vision API
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

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import (
    MARKDOWN_PAPERS, OUTPUT_DIR, TEST_MODE, TEST_PAPERS,
    BATCH_SIZE, BACKUP_DIR
)
from utils import (
    setup_logging, read_json, write_json,
    ProgressTracker
)


class ImageDescriptor:
    """Handles image description generation"""
    
    def __init__(self, logger, api_key: str):
        self.logger = logger
        self.api_key = api_key
        self.stats = {
            "papers_processed": 0,
            "images_described": 0,
            "images_skipped": 0,
            "errors": 0
        }
        
        # Import Google Generative AI
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.logger.info("Initialized Gemini Vision API")
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
            for image_file in images_to_keep:
                content = self._add_image_description(content, image_file, markdown_path.parent)
            
            # Write back if changed
            if content != original_content:
                # Create backup
                backup_path = BACKUP_DIR / "image_descriptor" / markdown_path.parent.name
                backup_path.mkdir(parents=True, exist_ok=True)
                shutil.copy2(markdown_path, backup_path / markdown_path.name)
                
                # Write updated content
                with open(markdown_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.logger.info(f"Added image descriptions to: {markdown_path.name}")
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
        # Find the image reference in markdown
        image_pattern = re.compile(
            r'(!\[[^\]]*\]\(' + re.escape(image_file) + r'\))',
            re.MULTILINE
        )
        
        matches = list(image_pattern.finditer(content))
        if not matches:
            self.logger.warning(f"Image reference not found: {image_file}")
            return content
        
        # Check if description already exists
        for match in matches:
            # Look for existing description after the image
            after_image = content[match.end():match.end() + 200]
            if re.search(r'^\s*\\?\s*Image.*description:', after_image, re.MULTILINE):
                self.logger.debug(f"Description already exists for: {image_file}")
                self.stats["images_skipped"] += 1
                continue
            
            # Generate description
            image_path = folder_path / image_file
            if not image_path.exists():
                self.logger.warning(f"Image file not found: {image_path}")
                continue
            
            description = self._generate_image_description(image_path)
            if description:
                # Insert description after the image
                insert_pos = match.end()
                
                # Format the description
                formatted_desc = f"\n\\\nImage description: {description}\n"
                
                # Insert into content
                content = content[:insert_pos] + formatted_desc + content[insert_pos:]
                self.stats["images_described"] += 1
                self.logger.debug(f"Added description for: {image_file}")
                
                # Add delay to avoid rate limiting
                time.sleep(0.5)
        
        return content
    
    def _generate_image_description(self, image_path: Path) -> Optional[str]:
        """Generate description for an image using Gemini"""
        try:
            # Read and encode image
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Create prompt
            prompt = """Describe this image from an academic paper in 1-2 sentences. 
            Focus on the main content, structure, and any text or data shown. 
            Be concise and technical. If it's a diagram, describe the components and relationships.
            If it's a chart or graph, describe what data is being presented."""
            
            # Generate description
            import PIL.Image
            image = PIL.Image.open(image_path)
            response = self.model.generate_content([prompt, image])
            
            if response.text:
                # Clean up the description
                description = response.text.strip()
                # Remove any line breaks
                description = description.replace('\n', ' ')
                # Ensure it ends with a period
                if not description.endswith('.'):
                    description += '.'
                
                return description
            
        except Exception as e:
            self.logger.error(f"Error generating description for {image_path}: {e}")
            self.stats["errors"] += 1
        
        return None


def main():
    """Main function to generate image descriptions"""
    logger = setup_logging("image_descriptor")
    logger.info("Starting image description generation")
    
    # Check for API key
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        logger.error("GOOGLE_API_KEY environment variable not set")
        logger.info("Please set: export GOOGLE_API_KEY='your-api-key'")
        return
    
    # Load paper analysis
    mapping_file = Path("cite_key_mapping.json")
    if not mapping_file.exists():
        logger.error("cite_key_mapping.json not found. Run paper_analyzer.py first.")
        return
    
    paper_mapping = read_json(mapping_file)
    papers = paper_mapping.get("papers", {})
    
    # Filter papers with images to process
    papers_with_images = {
        folder: info for folder, info in papers.items()
        if info.get("images", {}).get("keep", [])
    }
    
    logger.info(f"Found {len(papers_with_images)} papers with images to describe")
    
    # Initialize descriptor
    descriptor = ImageDescriptor(logger, api_key)
    
    # Process papers
    papers_to_process = list(papers_with_images.items())
    if TEST_MODE:
        papers_to_process = papers_to_process[:TEST_PAPERS]
        logger.info(f"Test mode: Processing only {TEST_PAPERS} papers")
    
    # Progress tracker
    tracker = ProgressTracker(len(papers_to_process), logger)
    
    for folder_name, paper_info in papers_to_process:
        markdown_path = MARKDOWN_PAPERS / folder_name / paper_info["markdown_file"]
        
        if not markdown_path.exists():
            logger.warning(f"Markdown file not found: {markdown_path}")
            tracker.update("File not found")
            continue
        
        # Process images
        descriptor.describe_images_in_paper(markdown_path, paper_info)
        tracker.update(f"Processed {paper_info['cite_key']}")
    
    # Log summary
    logger.info("\nImage Description Summary:")
    logger.info(f"Papers processed: {descriptor.stats['papers_processed']}")
    logger.info(f"Images described: {descriptor.stats['images_described']}")
    logger.info(f"Images skipped: {descriptor.stats['images_skipped']}")
    logger.info(f"Errors: {descriptor.stats['errors']}")
    
    # Save stats
    stats_file = OUTPUT_DIR / "image_description_stats.json"
    write_json(descriptor.stats, stats_file)
    logger.info(f"Stats saved to: {stats_file}")


if __name__ == "__main__":
    main()