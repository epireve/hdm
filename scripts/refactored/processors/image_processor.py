"""
Image processing and description generation for papers.
"""

import base64
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from ..core import BaseProcessor, ProcessingResult, ProcessingStatus
from ..core.config import Config
from ..core.exceptions import FileProcessingError, NetworkError


@dataclass
class ImageDescription:
    """Description of an image in a paper."""
    filename: str
    alt_text: str
    detailed_description: str
    figure_number: Optional[str] = None
    caption: Optional[str] = None
    image_type: str = "figure"  # figure, chart, diagram, screenshot, etc.


class ImageProcessor(BaseProcessor):
    """Processes images in papers and generates descriptions."""
    
    def __init__(self, config: Config, description_model: str = "gemini"):
        super().__init__(config, "ImageProcessor")
        self.description_model = description_model
        self.supported_formats = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg'}
        
    def process_item(self, paper_dir: Path, **kwargs) -> ProcessingResult:
        """Process all images in a paper directory."""
        try:
            if not paper_dir.exists() or not paper_dir.is_dir():
                raise FileProcessingError(f"Paper directory not found: {paper_dir}")
            
            # Find all image files
            image_files = self._find_image_files(paper_dir)
            
            if not image_files:
                return ProcessingResult(
                    status=ProcessingStatus.SKIPPED,
                    message="No images found",
                    data={'image_count': 0}
                )
            
            # Process each image
            descriptions = []
            for image_file in image_files:
                description = self._process_single_image(image_file, paper_dir)
                if description:
                    descriptions.append(description)
            
            # Save descriptions to file
            descriptions_file = paper_dir / "image_descriptions.json"
            self._save_descriptions(descriptions, descriptions_file)
            
            # Update markdown with image descriptions
            markdown_file = paper_dir / "paper.md"
            if markdown_file.exists():
                self._update_markdown_with_descriptions(markdown_file, descriptions)
            
            return ProcessingResult(
                status=ProcessingStatus.COMPLETED,
                message=f"Processed {len(descriptions)} images",
                data={
                    'image_count': len(image_files),
                    'descriptions_generated': len(descriptions),
                    'descriptions_file': str(descriptions_file),
                    'descriptions': [desc.__dict__ for desc in descriptions]
                }
            )
            
        except Exception as e:
            self.logger.error(f"Failed to process images in {paper_dir}: {str(e)}")
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=str(e),
                error=e
            )
    
    def _find_image_files(self, paper_dir: Path) -> List[Path]:
        """Find all image files in the paper directory."""
        image_files = []
        
        for file_path in paper_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                image_files.append(file_path)
        
        # Sort by filename for consistent processing order
        return sorted(image_files)
    
    def _process_single_image(self, image_file: Path, paper_dir: Path) -> Optional[ImageDescription]:
        """Process a single image file."""
        try:
            self.logger.info(f"Processing image: {image_file.name}")
            
            # Generate description based on model
            if self.description_model == "gemini":
                description_text = self._generate_gemini_description(image_file)
            else:
                description_text = self._generate_fallback_description(image_file)
            
            if not description_text:
                return None
            
            # Parse description and extract components
            return self._parse_description_response(image_file.name, description_text)
            
        except Exception as e:
            self.logger.warning(f"Failed to process image {image_file.name}: {e}")
            return None
    
    def _generate_gemini_description(self, image_file: Path) -> Optional[str]:
        """Generate image description using Gemini API."""
        try:
            import google.generativeai as genai
            
            # Configure Gemini
            api_key = self.config.api.gemini_api_key
            if not api_key:
                self.logger.warning("Gemini API key not configured")
                return None
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Read and encode image
            with open(image_file, 'rb') as f:
                image_data = f.read()
            
            # Create prompt for academic paper image description
            prompt = """Analyze this image from an academic research paper and provide:
1. A brief alt-text description (1-2 sentences)
2. A detailed description of the content, methodology, and findings shown
3. The type of visualization (figure, chart, diagram, screenshot, etc.)
4. Any figure number or caption if visible
5. Key insights or data presented

Format your response as JSON with fields: alt_text, detailed_description, image_type, figure_number, caption, insights."""
            
            # Generate description
            response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_data}])
            
            return response.text if response else None
            
        except ImportError:
            self.logger.warning("Gemini library not available")
            return None
        except Exception as e:
            self.logger.warning(f"Gemini API error: {e}")
            return None
    
    def _generate_fallback_description(self, image_file: Path) -> str:
        """Generate basic description when AI models are not available."""
        filename = image_file.name
        file_size = image_file.stat().st_size
        
        # Try to infer image type from filename
        image_type = "figure"
        if any(word in filename.lower() for word in ["chart", "graph", "plot"]):
            image_type = "chart"
        elif any(word in filename.lower() for word in ["diagram", "flowchart", "flow"]):
            image_type = "diagram"
        elif any(word in filename.lower() for word in ["screenshot", "screen"]):
            image_type = "screenshot"
        
        return json.dumps({
            "alt_text": f"Image from research paper: {filename}",
            "detailed_description": f"This is a {image_type} included in the research paper. The image file {filename} is {file_size} bytes in size.",
            "image_type": image_type,
            "figure_number": None,
            "caption": None,
            "insights": "Manual review needed to extract specific insights."
        })
    
    def _parse_description_response(self, filename: str, response_text: str) -> ImageDescription:
        """Parse AI response into structured description."""
        try:
            # Try to parse as JSON first
            if response_text.strip().startswith('{'):
                data = json.loads(response_text)
                return ImageDescription(
                    filename=filename,
                    alt_text=data.get('alt_text', ''),
                    detailed_description=data.get('detailed_description', ''),
                    figure_number=data.get('figure_number'),
                    caption=data.get('caption'),
                    image_type=data.get('image_type', 'figure')
                )
            else:
                # Parse free-form text response
                return ImageDescription(
                    filename=filename,
                    alt_text=response_text[:200] + "..." if len(response_text) > 200 else response_text,
                    detailed_description=response_text,
                    image_type="figure"
                )
                
        except json.JSONDecodeError:
            # Fallback for non-JSON responses
            return ImageDescription(
                filename=filename,
                alt_text=f"Image description for {filename}",
                detailed_description=response_text,
                image_type="figure"
            )
    
    def _save_descriptions(self, descriptions: List[ImageDescription], output_file: Path):
        """Save image descriptions to JSON file."""
        try:
            descriptions_data = [desc.__dict__ for desc in descriptions]
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(descriptions_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved {len(descriptions)} image descriptions to {output_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save descriptions: {e}")
    
    def _update_markdown_with_descriptions(self, markdown_file: Path, descriptions: List[ImageDescription]):
        """Update markdown file with image descriptions."""
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create descriptions mapping
            desc_map = {desc.filename: desc for desc in descriptions}
            
            # Replace image references with descriptive alt text
            import re
            
            def replace_image_ref(match):
                img_tag = match.group(0)
                filename = None
                
                # Extract filename from various markdown image formats
                if 'src=' in img_tag:
                    src_match = re.search(r'src=["\']([^"\']+)["\']', img_tag)
                    if src_match:
                        filename = Path(src_match.group(1)).name
                elif '![' in img_tag:
                    # Markdown format ![alt](filename)
                    md_match = re.search(r'!\\[[^\\]]*\\]\\(([^)]+)\\)', img_tag)
                    if md_match:
                        filename = Path(md_match.group(1)).name
                
                if filename and filename in desc_map:
                    desc = desc_map[filename]
                    # Update alt text with description
                    if '![' in img_tag:
                        return f"![{desc.alt_text}]({filename})\n\n*{desc.detailed_description}*"
                    else:
                        return img_tag.replace('alt=""', f'alt="{desc.alt_text}"')
                
                return img_tag
            
            # Replace image references
            content = re.sub(r'!\\[[^\\]]*\\]\\([^)]+\\)|<img[^>]+>', replace_image_ref, content)
            
            # Write updated content
            with open(markdown_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Updated {markdown_file} with image descriptions")
            
        except Exception as e:
            self.logger.warning(f"Failed to update markdown with descriptions: {e}")
    
    def batch_process_papers(self, papers_dir: Path, **kwargs) -> List[ProcessingResult]:
        """Process images for all papers in a directory."""
        if not papers_dir.exists():
            raise FileProcessingError(f"Papers directory not found: {papers_dir}")
        
        # Find all paper directories
        paper_dirs = [d for d in papers_dir.iterdir() if d.is_dir()]
        
        if not paper_dirs:
            self.logger.warning(f"No paper directories found in {papers_dir}")
            return []
        
        self.logger.info(f"Found {len(paper_dirs)} paper directories to process")
        
        # Process batch
        return self.process_batch(paper_dirs, **kwargs)
    
    def generate_image_index(self, papers_dir: Path, output_file: Optional[Path] = None) -> ProcessingResult:
        """Generate an index of all images across papers."""
        try:
            if output_file is None:
                output_file = papers_dir / "image_index.json"
            
            all_images = []
            
            for paper_dir in papers_dir.iterdir():
                if not paper_dir.is_dir():
                    continue
                
                descriptions_file = paper_dir / "image_descriptions.json"
                if descriptions_file.exists():
                    try:
                        with open(descriptions_file) as f:
                            descriptions = json.load(f)
                        
                        for desc in descriptions:
                            desc['paper_dir'] = paper_dir.name
                            all_images.append(desc)
                            
                    except Exception as e:
                        self.logger.warning(f"Failed to load descriptions from {descriptions_file}: {e}")
            
            # Create index
            index: Dict[str, Any] = {
                'total_images': len(all_images),
                'papers_with_images': len(set(img['paper_dir'] for img in all_images)),
                'image_types': {},
                'images': all_images
            }
            
            # Count image types
            for img in all_images:
                img_type = img.get('image_type', 'unknown')
                index['image_types'][img_type] = index['image_types'].get(img_type, 0) + 1
            
            # Save index
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
            
            return ProcessingResult(
                status=ProcessingStatus.COMPLETED,
                message=f"Generated image index with {len(all_images)} images",
                data={
                    'index_file': str(output_file),
                    'total_images': len(all_images),
                    'papers_with_images': len(set(img['paper_dir'] for img in all_images))
                }
            )
            
        except Exception as e:
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=f"Failed to generate image index: {str(e)}",
                error=e
            )