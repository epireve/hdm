"""
Pytest configuration and shared fixtures.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator

from scripts.refactored.core import Config


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    temp_path = Path(tempfile.mkdtemp())
    try:
        yield temp_path
    finally:
        shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_config(temp_dir: Path) -> Config:
    """Create a sample configuration for testing."""
    config = Config()
    
    # Override paths to use temp directory
    config.paths.base_dir = temp_dir
    config.paths.markdown_dir = temp_dir / "markdown_papers"
    config.paths.backup_dir = temp_dir / "backups"
    config.paths.output_dir = temp_dir / "output"
    config.paths.logs_dir = temp_dir / "logs"
    
    # Create directories
    for path in [config.paths.markdown_dir, config.paths.backup_dir, 
                 config.paths.output_dir, config.paths.logs_dir]:
        path.mkdir(parents=True, exist_ok=True)
    
    return config


@pytest.fixture
def sample_paper_data() -> dict:
    """Sample paper metadata for testing."""
    return {
        "title": "Test Paper: Advanced Knowledge Graphs",
        "authors": "John Doe, Jane Smith",
        "year": 2024,
        "doi": "10.1234/test.2024.001",
        "url": "https://example.com/paper.pdf",
        "relevancy": "High",
        "tldr": "A comprehensive study on advanced knowledge graph techniques.",
        "insights": "Novel approach to graph-based knowledge representation.",
        "summary": "This paper presents innovative methods for knowledge graph construction and querying.",
        "tags": ["Knowledge Graph", "AI", "Data Science"]
    }


@pytest.fixture
def sample_csv_data() -> list:
    """Sample CSV data for testing."""
    return [
        {
            "title": "Paper 1",
            "authors": "Author 1, Author 2",
            "year": "2024",
            "relevancy": "High"
        },
        {
            "title": "Paper 2", 
            "authors": "Author 3",
            "year": "2023",
            "relevancy": "Medium"
        }
    ]