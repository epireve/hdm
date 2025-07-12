# Paper Reformatter Plan

## Overview
This document outlines the comprehensive plan for reformatting all paper.md files in the markdown_papers directory to address formatting issues, standardize content, and ensure proper cite_key naming conventions.

## Identified Issues

### 1. HTML Elements
- `<sup>`, `<sub>`, `<span>` tags throughout content
- HTML entities like `&lt;`, `&gt;`, `&amp;`
- Inline styles and HTML formatting

### 2. Broken References
- Malformed citation links: `[\[23\]](#page-5-0)`, `[[1]](#page-27-0)`
- Undefined references with escaped brackets
- Double bracketed references
- Page-specific anchors that don't exist

### 3. Formatting Issues
- Incorrect strikethrough formatting
- Broken italic/bold formatting
- Inconsistent heading levels
- Mixed markdown and HTML syntax

### 4. Logo/Image Issues
- Logo references in image descriptions
- Unnecessary logo mentions in content
- Image comments that should be removed

### 5. Cite Key Issues
- Incorrect format (should be lastname_year)
- Not matching actual first author's last name
- Missing or incorrect year
- Folder names not matching cite_keys

## Solution Architecture

### 1. Paper Reformatter Script (`paper_reformatter.py`)

#### Core Components:

1. **Gemini 2.5 Pro Integration**
   - Use Google's Generative AI API
   - Leverage Gemini 2.5 Pro's advanced understanding
   - Batch process to manage API limits

2. **Content Processing Pipeline**
   - Extract YAML frontmatter
   - Process main content through Gemini
   - Validate and update cite_key
   - Merge reformatted content
   - Save with proper structure

3. **Cite Key Validation**
   - Extract actual first author from content
   - Parse publication year
   - Generate correct lastname_year format
   - Handle duplicates with a/b/c suffixes
   - Rename folders to match cite_keys

4. **Reference Fixing**
   - Convert all HTML-style references to markdown
   - Fix double brackets and escaped characters
   - Remove page-specific anchors
   - Ensure consistent citation format

5. **HTML to Markdown Conversion**
   - Convert all HTML tags to markdown equivalents
   - Handle superscript/subscript appropriately
   - Clean up HTML entities
   - Preserve mathematical notation

6. **Logo Removal**
   - Remove logo descriptions from images
   - Clean up logo references in text
   - Preserve actual content images

### 2. Processing Strategy

#### Phase 1: Analysis
1. Scan all paper.md files
2. Identify papers with issues
3. Create processing queue
4. Generate initial report

#### Phase 2: Reformatting
1. Process papers in batches (10-20 per batch)
2. Use Gemini 2.5 Pro for intelligent reformatting
3. Validate each reformatted paper
4. Create backups before modification

#### Phase 3: Cite Key Correction
1. Extract author information from paper content
2. Validate against frontmatter
3. Generate correct cite_key
4. Update frontmatter
5. Rename folder if needed

#### Phase 4: Quality Assurance
1. Verify all references are fixed
2. Ensure no HTML remains
3. Validate markdown syntax
4. Check cite_key consistency
5. Generate final report

### 3. Gemini Prompt Engineering

```python
REFORMATTING_PROMPT = """
You are reformatting an academic paper from mixed HTML/Markdown to pure Markdown.

REQUIREMENTS:
1. Convert ALL HTML tags to Markdown equivalents:
   - <sup>text</sup> → ^text^
   - <sub>text</sub> → ~text~
   - <span> tags → remove tags, keep content
   - &lt;, &gt;, &amp; → <, >, &

2. Fix ALL broken references:
   - [[1]](#page-x-y) → [1]
   - [\[1\]](#page-x-y) → [1]
   - Remove all #page-x-y anchors
   - Ensure consistent [N] format

3. Standardize formatting:
   - Use proper Markdown headers (# ## ###)
   - Fix broken italic/bold formatting
   - Ensure consistent list formatting
   - Preserve mathematical notation

4. Remove logo references:
   - Remove any image descriptions mentioning logos
   - Remove logo references in text
   - Keep actual research content images

5. Extract first author information:
   - Identify the first author's full name
   - Extract their last name for cite_key
   - Note the publication year

IMPORTANT:
- Preserve ALL academic content
- Maintain paper structure
- Keep all citations and references
- Preserve tables and figures
- Do not add any new content

Paper content to reformat:
{paper_content}
"""
```

### 4. Implementation Details

```python
class PaperReformatter:
    def __init__(self, api_key: str):
        self.genai = configure_genai(api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        
    def process_paper(self, paper_path: Path) -> ReformattingResult:
        # Extract frontmatter and content
        # Send to Gemini for reformatting
        # Validate cite_key
        # Update and save
        
    def validate_cite_key(self, frontmatter: dict, content: str) -> str:
        # Extract first author from content
        # Generate correct cite_key
        # Handle duplicates
        
    def rename_folder_if_needed(self, old_path: Path, new_cite_key: str):
        # Rename folder to match cite_key
        # Update all references
```

### 5. Error Handling

1. **API Errors**
   - Implement exponential backoff
   - Save progress regularly
   - Resume from checkpoints

2. **Content Errors**
   - Log papers that fail processing
   - Manual review queue
   - Partial success handling

3. **File System Errors**
   - Backup before modification
   - Atomic operations
   - Rollback capability

### 6. Reporting

Generate comprehensive reports including:
- Papers processed successfully
- Papers with errors
- Cite key changes
- Folder renames
- Reference fixes applied
- HTML conversions performed

### 7. Testing Strategy

1. **Test on Sample Papers**
   - Select 5-10 papers with various issues
   - Manually verify results
   - Refine prompts based on output

2. **Validation Checks**
   - No HTML remains
   - All references properly formatted
   - Cite keys match convention
   - Content preservation verified

3. **Performance Metrics**
   - Processing time per paper
   - API usage statistics
   - Success/failure rates

## Implementation Timeline

1. **Day 1: Script Development**
   - Core reformatter class
   - Gemini integration
   - Basic processing pipeline

2. **Day 2: Testing & Refinement**
   - Test on sample papers
   - Refine prompts
   - Add error handling

3. **Day 3-4: Bulk Processing**
   - Process all papers in batches
   - Monitor and handle errors
   - Generate reports

4. **Day 5: Quality Assurance**
   - Review processed papers
   - Fix any remaining issues
   - Final report generation

## Success Criteria

1. **100% HTML Removal**: No HTML tags remain in any paper
2. **Reference Consistency**: All citations use [N] format
3. **Cite Key Accuracy**: All papers have correct lastname_year format
4. **Content Preservation**: No academic content lost
5. **Folder Organization**: All folders match their cite_keys

## Risk Mitigation

1. **API Limits**: Process in batches with delays
2. **Content Loss**: Create backups before processing
3. **Incorrect Parsing**: Manual review queue for edge cases
4. **Breaking Changes**: Test thoroughly before bulk processing

## Next Steps

1. Implement the paper_reformatter.py script
2. Configure Gemini 2.5 Pro API access
3. Create test suite with sample papers
4. Begin incremental processing with monitoring
5. Generate comprehensive processing report