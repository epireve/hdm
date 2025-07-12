"""
Metadata extraction and YAML frontmatter processor.
"""

import re
import yaml
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from ..core import BaseProcessor, ProcessingResult, ProcessingStatus
from ..core.config import Config
from ..core.exceptions import FileProcessingError, ValidationError


@dataclass
class PaperMetadata:
    """Structured paper metadata."""
    cite_key: str
    title: str
    authors: str
    year: int
    doi: Optional[str] = None
    url: Optional[str] = None
    relevancy: str = "Medium"
    tldr: str = ""
    insights: str = ""
    summary: str = ""
    tags: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class MetadataExtractorProcessor(BaseProcessor):
    """Extracts metadata and adds YAML frontmatter to markdown files."""
    
    def __init__(self, config: Config, metadata_sources: Optional[List[str]] = None):
        super().__init__(config, "MetadataExtractor")
        self.metadata_sources = metadata_sources or ["missing_papers.json", "research_papers_complete.csv"]
        self._metadata_cache: Dict[str, Any] = {}
        self._load_metadata_sources()
    
    def _load_metadata_sources(self):
        """Load metadata from various sources."""
        self.logger.info("Loading metadata sources...")
        
        for source in self.metadata_sources:
            source_path = self.config.paths.base_dir / source
            if source_path.exists():
                try:
                    if source_path.suffix == '.json':
                        with open(source_path) as f:
                            data = json.load(f)
                            self._process_json_metadata(data)
                    elif source_path.suffix == '.csv':
                        self._process_csv_metadata(source_path)
                    
                    self.logger.info(f"Loaded metadata from {source}")
                except Exception as e:
                    self.logger.warning(f"Failed to load metadata from {source}: {e}")
        
        self.logger.info(f"Loaded metadata for {len(self._metadata_cache)} papers")
    
    def _process_json_metadata(self, data: Dict[str, Any]):
        """Process JSON metadata source."""
        for paper_id, metadata in data.items():
            self._metadata_cache[paper_id] = metadata
    
    def _process_csv_metadata(self, csv_path: Path):
        """Process CSV metadata source."""
        import pandas as pd
        try:
            df = pd.read_csv(csv_path)
            for _, row in df.iterrows():
                cite_key = row.get('cite_key', '')
                if cite_key:
                    self._metadata_cache[cite_key] = row.to_dict()
        except Exception as e:
            self.logger.warning(f"Failed to process CSV {csv_path}: {e}")
    
    def process_item(self, markdown_path: Path, **kwargs) -> ProcessingResult:
        """Add metadata to a markdown file."""
        try:
            if not markdown_path.exists():
                raise FileProcessingError(f"Markdown file not found: {markdown_path}")
            
            # Extract paper identifier
            paper_id = self._extract_paper_id(markdown_path)
            
            # Get metadata
            metadata = self._get_metadata_for_paper(paper_id, markdown_path)
            
            # Add YAML frontmatter
            success = self._add_yaml_frontmatter(markdown_path, metadata)
            
            if success:
                return ProcessingResult(
                    status=ProcessingStatus.COMPLETED,
                    message=f"Added metadata to {markdown_path.name}",
                    data={'metadata': metadata.__dict__ if isinstance(metadata, PaperMetadata) else metadata}
                )
            else:
                return ProcessingResult(
                    status=ProcessingStatus.FAILED,
                    message=f"Failed to add metadata to {markdown_path.name}"
                )
                
        except Exception as e:
            self.logger.error(f"Failed to process metadata for {markdown_path}: {str(e)}")
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                message=str(e),
                error=e
            )
    
    def _extract_paper_id(self, markdown_path: Path) -> str:
        """Extract paper identifier from path or content."""
        # Try folder name first (cite_key format)
        folder_name = markdown_path.parent.name
        if folder_name != 'markdown_papers':
            return folder_name
        
        # Try filename
        return markdown_path.stem
    
    def _get_metadata_for_paper(self, paper_id: str, markdown_path: Path) -> PaperMetadata:
        """Get metadata for a paper from various sources."""
        # Check cache first
        if paper_id in self._metadata_cache:
            cached_data = self._metadata_cache[paper_id]
            return self._create_metadata_from_dict(cached_data, paper_id)
        
        # Try to extract from existing YAML frontmatter
        existing_metadata = self._extract_existing_metadata(markdown_path)
        if existing_metadata:
            return existing_metadata
        
        # Generate basic metadata
        return self._generate_basic_metadata(paper_id, markdown_path)
    
    def _create_metadata_from_dict(self, data: Dict[str, Any], paper_id: str) -> PaperMetadata:
        """Create PaperMetadata from dictionary data."""
        return PaperMetadata(
            cite_key=data.get('cite_key', paper_id),
            title=self._clean_title(data.get('title', data.get('Paper Title', ''))),
            authors=self._clean_authors(data.get('authors', data.get('Authors', ''))),
            year=int(data.get('year', data.get('Year', 2024))),
            doi=data.get('doi', data.get('DOI')),
            url=data.get('url'),
            relevancy=data.get('relevancy', data.get('Relevancy', 'Medium')),
            tldr=data.get('tldr', data.get('TL;DR', '')),
            insights=data.get('insights', data.get('Insights', '')),
            summary=data.get('summary', data.get('Summary', '')),
            tags=self._parse_tags(data.get('tags', data.get('Tags', '')))
        )
    
    def _extract_existing_metadata(self, markdown_path: Path) -> Optional[PaperMetadata]:
        """Extract metadata from existing YAML frontmatter."""
        try:
            with open(markdown_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content.startswith('---\n'):
                end_idx = content.find('\n---\n', 4)
                if end_idx != -1:
                    yaml_content = content[4:end_idx]
                    metadata_dict = yaml.safe_load(yaml_content)
                    
                    if metadata_dict:
                        return self._create_metadata_from_dict(
                            metadata_dict, 
                            markdown_path.parent.name
                        )
        except Exception as e:
            self.logger.warning(f"Failed to extract existing metadata from {markdown_path}: {e}")
        
        return None
    
    def _generate_basic_metadata(self, paper_id: str, markdown_path: Path) -> PaperMetadata:
        """Generate basic metadata when none is available."""
        # Try to extract title from content
        title = self._extract_title_from_content(markdown_path)
        
        return PaperMetadata(
            cite_key=paper_id,
            title=title or f"Paper {paper_id}",
            authors="Unknown",
            year=2024,
            tags=["HDM", "Knowledge Graph"]
        )
    
    def _extract_title_from_content(self, markdown_path: Path) -> Optional[str]:
        """Extract title from markdown content."""
        try:
            with open(markdown_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for first heading
            lines = content.split('\n')
            for line in lines[:20]:  # Check first 20 lines
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip()
                elif line.startswith('## '):
                    return line[3:].strip()
                elif line and not line.startswith('---') and len(line) > 10:
                    # Take first substantial line as potential title
                    return line[:100] + "..." if len(line) > 100 else line
        
        except Exception:
            pass
        
        return None
    
    def _add_yaml_frontmatter(self, markdown_path: Path, metadata: PaperMetadata) -> bool:
        """Add or update YAML frontmatter in markdown file."""
        try:
            with open(markdown_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove existing frontmatter if present
            if content.startswith('---\n'):
                end_idx = content.find('\n---\n', 4)
                if end_idx != -1:
                    content = content[end_idx + 5:]  # Remove frontmatter and separator
            
            # Create YAML frontmatter
            yaml_data = {
                'cite_key': metadata.cite_key,
                'title': metadata.title,
                'authors': metadata.authors,
                'year': metadata.year,
            }
            
            # Add optional fields if they have values
            if metadata.doi:
                yaml_data['doi'] = metadata.doi
            if metadata.url:
                yaml_data['url'] = metadata.url
            if metadata.relevancy:
                yaml_data['relevancy'] = metadata.relevancy
            if metadata.tldr:
                yaml_data['tldr'] = metadata.tldr
            if metadata.insights:
                yaml_data['insights'] = metadata.insights
            if metadata.summary:
                yaml_data['summary'] = metadata.summary
            if metadata.tags:
                yaml_data['tags'] = metadata.tags
            
            # Create new content with frontmatter
            yaml_str = yaml.dump(yaml_data, default_flow_style=False, allow_unicode=True)
            new_content = f"---\n{yaml_str}---\n\n{content}"
            
            # Write back to file
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add YAML frontmatter to {markdown_path}: {e}")
            return False
    
    def _clean_title(self, title: str) -> str:
        """Clean and normalize title."""
        if not title:
            return ""
        
        # Remove quotes, brackets, normalize whitespace
        title = re.sub(r'^["\'\[\]]+|["\'\[\]]+$', '', title)
        title = re.sub(r'\s+', ' ', title).strip()
        
        # Remove "Article" prefix if present
        if title.lower().startswith('article '):
            title = title[8:]
        
        return title
    
    def _clean_authors(self, authors: str) -> str:
        """Clean and normalize authors list."""
        if not authors:
            return ""
        
        # Handle different separators
        authors = authors.replace(' & ', ', ').replace(' and ', ', ')
        
        # Remove "et al."
        authors = re.sub(r',?\s*et al\.?', '', authors)
        
        # Clean up whitespace
        authors = re.sub(r'\s+', ' ', authors).strip()
        
        return authors
    
    def _parse_tags(self, tags_str: str) -> List[str]:
        """Parse tags string into list."""
        if not tags_str:
            return []
        
        if isinstance(tags_str, list):
            return tags_str
        
        # Split on common separators
        tags = re.split(r'[,;|]', str(tags_str))
        return [tag.strip() for tag in tags if tag.strip()]
    
    def batch_process_directory(self, markdown_dir: Path, **kwargs) -> List[ProcessingResult]:
        """Process all markdown files in a directory."""
        if not markdown_dir.exists():
            raise FileProcessingError(f"Directory not found: {markdown_dir}")
        
        # Find all paper.md files
        markdown_files = []
        for paper_dir in markdown_dir.iterdir():
            if paper_dir.is_dir():
                paper_md = paper_dir / "paper.md"
                if paper_md.exists():
                    markdown_files.append(paper_md)
        
        if not markdown_files:
            self.logger.warning(f"No paper.md files found in {markdown_dir}")
            return []
        
        self.logger.info(f"Found {len(markdown_files)} markdown files to process")
        
        # Process batch
        return self.process_batch(markdown_files, **kwargs)