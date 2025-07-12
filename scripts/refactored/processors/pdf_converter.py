"""
PDF to Markdown conversion processor.
"""

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from ..core import BaseProcessor, ProcessingResult, ProcessingStatus
from ..core.config import Config
from ..core.exceptions import FileProcessingError


@dataclass
class ConversionResult:
    """Result of PDF conversion."""
    success: bool
    markdown_path: Optional[Path] = None
    error_message: str = ""
    extracted_metadata: Dict[str, Any] = None
    image_count: int = 0
    page_count: int = 0


class PDFConverterProcessor(BaseProcessor):
    """Converts PDF papers to markdown format with metadata extraction."""
    
    def __init__(self, config: Config, conversion_tool: str = "marker"):
        super().__init__(config, "PDFConverter")
        self.conversion_tool = conversion_tool
        self.checkpoint_file = config.paths.output_dir / "pdf_conversion_checkpoint.json"
        
    def process_item(self, pdf_path: Path, **kwargs) -> ProcessingResult:
        """Convert a single PDF to markdown."""
        try:
            # Validate input
            if not pdf_path.exists():
                raise FileProcessingError(f"PDF file not found: {pdf_path}")
            
            if not pdf_path.suffix.lower() == '.pdf':
                raise FileProcessingError(f"Not a PDF file: {pdf_path}")
            
            # Generate output paths
            markdown_dir = self._get_output_directory(pdf_path)
            markdown_file = markdown_dir / "paper.md"
            
            # Check if already converted
            if markdown_file.exists() and not kwargs.get('force_reconvert', False):
                self.logger.info(f"Markdown already exists for {pdf_path.name}")
                return ProcessingResult(
                    status=ProcessingStatus.SKIPPED,
                    message="Already converted",
                    data={'markdown_path': str(markdown_file)}
                )
            
            # Perform conversion
            conversion_result = self._convert_pdf(pdf_path, markdown_dir)
            
            if conversion_result.success:
                # Move PDF to processed location
                self._move_processed_pdf(pdf_path)
                
                return ProcessingResult(
                    status=ProcessingStatus.COMPLETED,
                    message=f"Successfully converted {pdf_path.name}",
                    data={
                        'markdown_path': str(conversion_result.markdown_path),
                        'image_count': conversion_result.image_count,
                        'page_count': conversion_result.page_count,
                        'metadata': conversion_result.extracted_metadata
                    }
                )
            else:
                raise FileProcessingError(
                    f"Conversion failed: {conversion_result.error_message}",
                    file_path=str(pdf_path),
                    operation="pdf_conversion"
                )
                
        except Exception as e:
            self.logger.error(f"Failed to convert {pdf_path}: {str(e)}")
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=str(e),
                error=e
            )
    
    def _convert_pdf(self, pdf_path: Path, output_dir: Path) -> ConversionResult:
        """Perform the actual PDF conversion."""
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            
            if self.conversion_tool == "marker":
                return self._convert_with_marker(pdf_path, output_dir)
            elif self.conversion_tool == "pypdf":
                return self._convert_with_pypdf(pdf_path, output_dir)
            else:
                raise FileProcessingError(f"Unknown conversion tool: {self.conversion_tool}")
                
        except Exception as e:
            return ConversionResult(
                success=False,
                error_message=str(e)
            )
    
    def _convert_with_marker(self, pdf_path: Path, output_dir: Path) -> ConversionResult:
        """Convert PDF using marker library."""
        try:
            from marker.convert import convert_single_pdf
            from marker.models import load_all_models
            
            # Load models (cache them for efficiency)
            if not hasattr(self, '_marker_models'):
                self.logger.info("Loading marker models...")
                self._marker_models = load_all_models()
            
            # Convert PDF
            full_text, images, out_meta = convert_single_pdf(
                fname=str(pdf_path),
                model_lst=self._marker_models,
                max_pages=None,
                langs=None,
                batch_multiplier=1
            )
            
            # Save markdown
            markdown_path = output_dir / "paper.md"
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(full_text)
            
            # Save images
            image_count = 0
            if images:
                for img_name, img_data in images.items():
                    img_path = output_dir / img_name
                    with open(img_path, 'wb') as f:
                        f.write(img_data)
                    image_count += 1
            
            return ConversionResult(
                success=True,
                markdown_path=markdown_path,
                extracted_metadata=out_meta,
                image_count=image_count,
                page_count=out_meta.get('page_count', 0) if out_meta else 0
            )
            
        except ImportError:
            self.logger.warning("Marker not available, falling back to pypdf")
            return self._convert_with_pypdf(pdf_path, output_dir)
        except Exception as e:
            return ConversionResult(
                success=False,
                error_message=f"Marker conversion failed: {str(e)}"
            )
    
    def _convert_with_pypdf(self, pdf_path: Path, output_dir: Path) -> ConversionResult:
        """Convert PDF using pypdf as fallback."""
        try:
            import pypdf
            
            with open(pdf_path, 'rb') as file:
                reader = pypdf.PdfReader(file)
                text_content = []
                
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text.strip():
                        text_content.append(f"## Page {page_num + 1}\n\n{text}\n\n")
                
                full_text = "".join(text_content)
                
                # Save markdown
                markdown_path = output_dir / "paper.md"
                with open(markdown_path, 'w', encoding='utf-8') as f:
                    f.write(full_text)
                
                return ConversionResult(
                    success=True,
                    markdown_path=markdown_path,
                    page_count=len(reader.pages),
                    image_count=0
                )
                
        except ImportError:
            return ConversionResult(
                success=False,
                error_message="No PDF conversion libraries available (marker, pypdf)"
            )
        except Exception as e:
            return ConversionResult(
                success=False,
                error_message=f"PyPDF conversion failed: {str(e)}"
            )
    
    def _get_output_directory(self, pdf_path: Path) -> Path:
        """Generate output directory path for converted markdown."""
        # Use PDF filename (without extension) as directory name
        dir_name = pdf_path.stem.replace(' ', '_').replace('-', '_').lower()
        return self.config.paths.markdown_dir / dir_name
    
    def _move_processed_pdf(self, pdf_path: Path):
        """Move processed PDF to papers directory."""
        if not self.config.processing.backup_enabled:
            return
        
        papers_dir = self.config.paths.papers_dir
        papers_dir.mkdir(parents=True, exist_ok=True)
        
        destination = papers_dir / pdf_path.name
        
        try:
            shutil.move(str(pdf_path), str(destination))
            self.logger.info(f"Moved processed PDF to {destination}")
        except Exception as e:
            self.logger.warning(f"Failed to move PDF {pdf_path}: {e}")
    
    def batch_convert(self, pdf_directory: Path, **kwargs) -> List[ProcessingResult]:
        """Convert all PDFs in a directory."""
        if not pdf_directory.exists():
            raise FileProcessingError(f"Directory not found: {pdf_directory}")
        
        # Find all PDF files
        pdf_files = list(pdf_directory.glob("*.pdf")) + list(pdf_directory.glob("*.PDF"))
        
        if not pdf_files:
            self.logger.warning(f"No PDF files found in {pdf_directory}")
            return []
        
        self.logger.info(f"Found {len(pdf_files)} PDF files to convert")
        
        # Process batch
        return self.process_batch(pdf_files, **kwargs)
    
    def get_conversion_status(self) -> Dict[str, Any]:
        """Get status of PDF conversions."""
        if not self.checkpoint_manager:
            return {"error": "Checkpoint manager not available"}
        
        total_completed = len(self.checkpoint_manager.data.get('completed', []))
        total_failed = len(self.checkpoint_manager.data.get('failed', []))
        
        return {
            'completed': total_completed,
            'failed': total_failed,
            'total_processed': total_completed + total_failed
        }