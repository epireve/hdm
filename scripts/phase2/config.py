"""
Configuration for Phase 2 processing
"""
from pathlib import Path

# Directories
BASE_DIR = Path(__file__).parent.parent.parent
MARKDOWN_DIR = BASE_DIR / "markdown_papers"
MARKDOWN_PAPERS = MARKDOWN_DIR  # Alias for compatibility
OUTPUT_DIR = BASE_DIR / "standardized_papers"
RESEARCH_TABLE = BASE_DIR / "research_table.md"
RESEARCH_TABLE_CSV = BASE_DIR / "research_table.csv"
BACKUP_DIR = BASE_DIR / "backup_phase2"
LOG_DIR = BASE_DIR / "logs" / "phase2"

# Image patterns
REMOVE_IMAGE_PATTERNS = [
    "*logo*", "*Logo*", "*LOGO*",
    "*Picture_0.jpeg", "*Picture_1.jpeg",
    "*page_0_Picture_0*", "*page_0_Picture_1*",
    "*watermark*", "*Watermark*"
]

KEEP_IMAGE_PATTERNS = [
    "*Figure*", "*figure*", "*FIGURE*",
    "*Table*", "*table*", "*TABLE*",
    "*Chart*", "*chart*", "*CHART*",
    "*Diagram*", "*diagram*", "*DIAGRAM*",
    "*Graph*", "*graph*", "*GRAPH*",
    "*Plot*", "*plot*", "*PLOT*"
]

# Processing options
BATCH_SIZE = 10
TEST_MODE = True  # Process only first 5 papers for testing
TEST_PAPERS = 5

# API Keys
GEMINI_API_KEY_ENV = "GOOGLE_API_KEY"

# Output files
CITE_KEY_MAPPING_FILE = BASE_DIR / "cite_key_mapping.json"
UPDATED_RESEARCH_TABLE = BASE_DIR / "research_table_with_citekeys.md"
UPDATED_RESEARCH_TABLE_CSV = BASE_DIR / "research_table_with_citekeys.csv"

# Logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"