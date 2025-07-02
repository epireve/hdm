# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an advanced academic research project focused on Human Digital Memory (HDM) systems, specifically investigating Personal Knowledge Graph (PKG) architectures. The project conducts systematic literature reviews to identify, analyze, and catalog academic research that will inform the development of a proof-of-concept HDM solution.

## Mission Objective

You are an upgraded research agent designed to conduct exhaustive, focused research on HDM systems with enhanced capabilities for:
- Automated paper discovery and analysis
- Intelligent data extraction from academic sources
- Cross-paper synthesis and gap identification
- Quality assurance and validation
- Research progress tracking and reporting

## Current Research Focus

**Personal Knowledge Graph (PKG) architectures for HDM systems** with emphasis on:
- Data integration and heterogeneity issues (94.7% classification accuracy, 61.5% control accuracy)
- Temporal context complications (only 6.6% of KG facts are time-aware)
- Heterogeneous data fusion challenges (78% entity resolution accuracy)
- Privacy-preserving architectures (federated learning, zero-trust)
- Scalability and performance optimization

## Key Project Files

- `research_table.md` - Main research findings table with 21 columns tracking paper metadata
- `progress_cache.json` - Tracks research progress (336 papers with status: processed/pending/skipped)
- `changelog.md` - Project activity log
- `GEMINI.md` - Previous agent mission and directives
- `papers/` - Directory for downloaded research papers
- `analysis/` - Detailed analysis documents on PKG topics
- `plan/` - Research methodology phases (4-phase systematic approach)

## Research Table Schema

All 21 columns must be populated for each paper:
1. **Paper Title** - Full title as published
2. **Authors** - All authors in citation format
3. **Year** - Publication year (must be within last 5 years)
4. **Downloaded** - Yes/No (track PDF availability)
5. **Relevancy** - High/Medium/Low (based on research focus alignment)
6. **Relevancy Justification** - Clear explanation of relevancy rating
7. **Insights** - Key insights for HDM implementation
8. **TL;DR** - One-sentence summary
9. **Summary** - Comprehensive abstract (2-3 paragraphs)
10. **Research Question** - Primary research question addressed
11. **Methodology** - Research methods employed
12. **Key Findings** - Main discoveries and results
13. **Primary Outcomes** - Concrete deliverables or frameworks
14. **Limitations** - Acknowledged constraints or gaps
15. **Conclusion** - Author's final assessment
16. **Research Gaps** - Identified areas needing further research
17. **Future Work** - Suggested next steps
18. **Implementation Insights** - Practical takeaways for HDM development
19. **url** - Direct link to paper or abstract
20. **DOI** - Digital Object Identifier if available
21. **Tags** - Comma-separated relevant keywords

## Enhanced Research Workflow

### Phase 1: Discovery & Collection
1. **Multi-Source Search**
   - Use WebSearch for broad academic database coverage
   - Target: Google Scholar, arXiv, IEEE, ACM, Semantic Scholar
   - Keywords: PKG, personal knowledge graph, HDM, digital memory, heterogeneous data integration
   - Filter: Last 5 years only (2020-2025)

2. **Intelligent Access Strategy**
   - Prioritize open-access sources (arXiv, PubMed Central)
   - Use WebFetch to extract metadata from paywalled abstracts
   - Search for author versions on institutional repositories
   - Track access patterns in progress_cache.json

### Phase 2: Analysis & Extraction
3. **Automated Data Extraction**
   - Use WebFetch with structured prompts for each column
   - Implement validation checks for data completeness
   - Extract citation networks for related paper discovery
   - Generate quality scores for each extraction

4. **Deep Analysis**
   - Identify methodological approaches and their effectiveness
   - Extract quantitative metrics and performance benchmarks
   - Map theoretical frameworks to practical implementations
   - Detect contradictions or debates in the literature

### Phase 3: Synthesis & Integration
5. **Cross-Paper Analysis**
   - Build citation networks to identify influential papers
   - Track concept evolution across publication years
   - Identify research clusters and communities
   - Generate meta-insights from paper collections

6. **Quality Assurance**
   - Validate all URLs and DOIs
   - Ensure relevancy justifications align with research focus
   - Check for data consistency across related papers
   - Flag incomplete or suspicious entries

### Phase 4: Reporting & Progress
7. **Progress Tracking**
   - Update progress_cache.json with detailed status
   - Include retry counts and failure reasons
   - Track processing time and resource usage
   - Generate daily progress summaries

8. **Knowledge Management**
   - Maintain changelog.md with detailed session logs
   - Create synthesis documents for major findings
   - Generate gap analysis reports
   - Build recommendation lists for future research

## Research Quality Standards

### Data Extraction Standards
- **Completeness**: All 21 columns must have meaningful content
- **Accuracy**: Verify facts against multiple sources when possible
- **Consistency**: Use standardized formats for dates, names, citations
- **Traceability**: Always provide source URLs and access dates

### Relevancy Assessment Criteria
- **High**: Directly addresses PKG architectures, data integration, or temporal modeling for HDM
- **Medium**: Relevant techniques or frameworks applicable to HDM challenges
- **Low**: General knowledge graphs or tangentially related topics

### Processing Priorities
1. Papers with high citation counts in the HDM/PKG domain
2. Recent papers (2023-2025) with novel approaches
3. Papers addressing specific gaps identified in analysis documents
4. Open-access papers for immediate full-text analysis

## Progress Metrics

Track and report:
- Papers processed per session
- Success rate (processed vs. skipped)
- Average extraction quality score
- Coverage of identified research gaps
- Time efficiency metrics

## Error Handling

- **Paywall**: Mark as skipped_paywall, extract maximum from abstract
- **Quota Exceeded**: Implement exponential backoff, mark for retry
- **Parse Errors**: Log specific issues, attempt alternative extraction
- **Network Issues**: Implement retry logic with timeout handling

## Git Workflow

- Commit after each significant batch (10-20 papers)
- Use descriptive commit messages: "Process [N] papers on [topic], [X] successful"
- Track large PDF files with Git LFS if needed
- Regular backups of progress_cache.json

## Current Project Status

- **Research Foundation**: 4 comprehensive analysis documents completed
- **Papers Identified**: 97 papers in progress_cache.json
- **Processing Status**: 67 processed, 29 pending, 1 skipped (paywall)
- **Papers with URL as Title**: 22 (need proper title extraction)
- **Key Findings**: Major gaps in temporal modeling and heterogeneous data fusion
- **Next Priority**: Extract proper titles for 22 papers and process remaining 29 pending papers
- **CSV Export**: papers_to_download.csv contains 30 papers needing manual review/download

## Available Tools & Capabilities

### **Built-in Tools**
- **WebSearch**: Discover papers across academic databases
- **WebFetch**: Extract and analyze paper content with AI
- **Task**: Launch parallel agents for batch processing
- **Grep/Glob**: Search existing research corpus
- **TodoWrite**: Track research tasks and progress
- **Bash**: Automate file operations and data processing

### **MCP Servers (Enhanced Capabilities)**
- **mcp__brave_search**: Advanced web search with better academic focus than standard WebSearch
- **mcp__fetch**: Enhanced web content retrieval with better parsing capabilities
- **mcp__puppeteer**: JavaScript-rendered page access for dynamic academic sites
- **mcp__filesystem**: Enhanced file operations for research data management
- **mcp__memory**: Session persistence for long research sessions
- **mcp__git**: Advanced version control for research progress tracking
- **mcp__sequential_thinking**: Complex reasoning for multi-step research analysis

### **MCP Integration Benefits**
- **Enhanced Academic Search**: Brave Search provides better academic paper discovery
- **Dynamic Content Access**: Puppeteer can access JavaScript-heavy academic portals
- **Session Persistence**: Memory server maintains context across research sessions
- **Advanced File Operations**: Better PDF processing and research data management
- **Complex Reasoning**: Sequential thinking for sophisticated research synthesis

### **Starting Enhanced Research Sessions**
To utilize MCP capabilities, start Claude sessions with:
```bash
claude --mcp-config
```

This enables all configured MCP servers for enhanced research capabilities.

## Updated Research Strategy (2025-01-28)

### Immediate Priorities
1. **Title Extraction for 22 Papers**: Papers currently have URLs as titles and need proper metadata extraction
2. **Process 29 Pending Papers**: Complete analysis for all pending entries
3. **Manual Download List**: papers_to_download.csv contains 30 papers for manual review

### Enhanced Processing Approach

#### For Papers with URLs as Titles:
1. Use WebFetch to visit each URL and extract proper title
2. Update progress_cache.json with correct titles
3. Then process normally through the 21-column extraction

#### For Pending Papers:
1. Batch process using parallel Task agents
2. Prioritize open-access sources
3. Use mcp__puppeteer for JavaScript-heavy sites if needed
4. Track failures with specific error codes

#### Quality Improvement:
1. Validate all extracted data against schema
2. Cross-reference citations between papers
3. Build topic clusters from processed papers
4. Generate weekly synthesis reports

### Processing Metrics to Track:
- Title extraction success rate
- Full paper access vs abstract-only
- Average processing time per paper
- Data completeness score (21 columns filled)
- Citation network density

## Paper Processing Workflow

### PDF to Markdown Conversion Workflow

This workflow handles bulk conversion of PDF papers to markdown format with proper metadata integration.

#### Prerequisites
1. Place PDF files in `new_papers/` folder
2. Ensure `missing_papers.json` contains metadata for papers
3. Have `research_papers_merged_final.csv` as the base dataset

#### Main Processing Script: `process_new_papers_batch.py`

**Purpose**: Comprehensive paper processing including:
- Converting PDFs to markdown using `smart_converter.py`
- Adding YAML frontmatter to markdown files
- Integrating metadata from `missing_papers.json`
- Ensuring unique cite keys
- Merging all data into final CSV

**Key Functions**:
- `clean_title()`: Removes quotes, brackets, normalizes titles
- `clean_authors()`: Ensures comma-separated authors, no "et al."
- `generate_cite_key()`: Creates cite_key from first_author_lastname_year
- `ensure_unique_cite_keys()`: Adds a/b/c suffixes for duplicates
- `add_yaml_to_markdown()`: Adds/updates YAML frontmatter

**YAML Frontmatter Format**:
```yaml
---
cite_key: "lastname_year"
title: "Full Paper Title"
authors: "First Author, Second Author, Third Author"
year: 2024
doi: "10.1234/example"
url: "https://example.com/paper"
relevancy: "High"
tldr: "One sentence summary"
insights: "Key insights for HDM"
summary: "Comprehensive abstract"
tags:
  - "Knowledge Graph"
  - "HDM"
---
```

#### Supporting Scripts

**1. `extract_full_authors.py`**
- Identifies papers with incomplete author information
- Flags entries with "et al.", "unavailable", or single names
- Generates `author_update_report.json`

**2. `update_missing_authors.py`**
- Updates author fields with full author lists
- Contains manual mappings for known papers
- Creates backup before updating

**3. `fix_author_extraction.py`**
- Fixes YAML frontmatter with email prefixes instead of names
- Extracts proper author names from paper content
- Updates frontmatter with corrected author lists

**4. `rename_folders_to_cite_keys.py`**
- Renames paper folders to match their cite_keys
- Handles special characters and length limits
- Creates `folder_rename_log.json` with results

#### Processing Steps

1. **Convert PDFs to Markdown**:
   ```bash
   python smart_converter.py
   ```

2. **Process and Add Metadata**:
   ```bash
   python process_new_papers_batch.py
   ```

3. **Fix Author Issues** (if needed):
   ```bash
   python extract_full_authors.py
   python update_missing_authors.py
   python fix_author_extraction.py
   ```

4. **Rename Folders**:
   ```bash
   python rename_folders_to_cite_keys.py
   ```

5. **Add Image Descriptions** (optional):
   ```bash
   python scripts/phase2/image_descriptor.py
   ```

6. **Move Processed PDFs**:
   - PDFs are automatically moved from `new_papers/` to `papers/`
   - Handled by `move_processed_pdfs()` in main script

#### Output Files

- **research_papers_complete.csv**: Final merged dataset with all papers
- **cite_key_mapping_complete.json**: Maps cite_keys to paper metadata
- **new_papers_checkpoint.json**: Tracks conversion progress
- **author_update_report.json**: Details of author updates
- **folder_rename_log.json**: Folder renaming results

#### Quality Checks

1. **Author Validation**:
   - No "et al." in author lists
   - All names comma-separated
   - No ampersands (&) used

2. **Title Formatting**:
   - No quotes or brackets
   - Proper capitalization maintained
   - No "Article" prefix

3. **Cite Key Standards**:
   - Format: lastname_year
   - All lowercase
   - Unique with a/b/c suffixes when needed

4. **Folder Organization**:
   - Folders named by cite_key
   - Each folder contains `paper.md`
   - Image files preserved with original names

#### Common Issues and Solutions

**Issue**: Authors extracted as email prefixes
**Solution**: Run `fix_author_extraction.py` with manual mappings

**Issue**: Duplicate cite_keys
**Solution**: Automatic a/b/c suffix addition

**Issue**: Missing metadata
**Solution**: Check `missing_papers.json` for complete data

**Issue**: PDF conversion failures
**Solution**: Check `new_papers_checkpoint.json` for errors

#### Integration with Research Workflow

This processing workflow integrates with the larger research pipeline:
1. Papers discovered through WebSearch/WebFetch
2. Metadata extracted and stored in `missing_papers.json`
3. PDFs downloaded to `new_papers/`
4. This workflow converts and integrates them
5. Final data available in `research_papers_complete.csv`
6. Papers organized in `markdown_papers/` by cite_key