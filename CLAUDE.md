# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an advanced academic research project focused on Human Digital Memory (HDM) systems, specifically investigating **heterogeneous data integration within Personal Knowledge Graph (PKG) architectures**. The project conducts systematic literature reviews to identify, analyze, and catalog academic research that will inform the development of bespoke PKG systems with temporal-first architecture and upstream-focused schema design for seamless heterogeneous data fusion.

## Mission Objective

You are an upgraded research agent designed to conduct exhaustive, focused research on HDM systems with enhanced capabilities for:
- Automated paper discovery and analysis
- Intelligent data extraction from academic sources
- Cross-paper synthesis and gap identification
- Quality assurance and validation
- Research progress tracking and reporting

## Current Research Focus

**Heterogeneous Data Integration in Personal Knowledge Graph (PKG) Architectures** - Our research focuses on developing bespoke PKG systems that seamlessly integrate diverse upstream data sources through temporal-first architecture and advanced schema design. Based on comprehensive analysis of 98+ papers (2020-2025), we are advancing beyond general PKG implementations toward specialized systems optimized for heterogeneous data fusion.

### **Primary Research Pillars**

#### **1. Heterogeneous Data Integration & Schema Architecture**
- **Multi-Modal Data Fusion**: Integration patterns for structured (databases, APIs), semi-structured (JSON, XML), and unstructured (text, multimedia) data sources
- **Schema Harmonization**: Dynamic schema mapping and transformation techniques for disparate data formats and ontologies
- **Upstream Data Source Orchestration**: Early-stage data ingestion pipelines with real-time validation and quality assessment
- **Entity Resolution Across Domains**: Cross-source entity linking with 78% accuracy improvements through advanced schema integration

#### **2. Temporal-First Architecture Design**
- **Time-Centric Data Modeling**: Moving from traditional entity-centric to temporal-first PKG architectures achieving 94.8% performance with 90% latency reduction
- **Temporal Schema Evolution**: Dynamic schema adaptation over time to accommodate changing data source structures
- **Versioned Knowledge Representation**: Temporal versioning of entities, relationships, and schema definitions
- **Chronological Query Optimization**: Query engines optimized for temporal range operations and historical data analysis

#### **3. Bespoke System Design Patterns**
- **Domain-Specific PKG Architectures**: Customized designs for healthcare, education, enterprise, and personal productivity domains
- **Modular Integration Frameworks**: Pluggable components for different data source types and integration patterns
- **Adaptive Schema Management**: Self-evolving schemas that learn from data patterns and user interactions
- **Performance-Optimized Pipelines**: Custom data processing workflows tailored to specific heterogeneous data combinations

### **Research Maturity Assessment**
- **Geographic Leadership**: Asia-Pacific (temporal KG), North America (privacy), Europe (semantic integration)
- **Technology Readiness**: Moved from experimental to implementation-ready solutions
- **Performance Benchmarks**: 66.7% Hits@1 for temporal completion, 93% accuracy in healthcare applications
- **Industry Adoption**: Healthcare digital twins, educational technology, enterprise knowledge management

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
   - Keywords: heterogeneous data integration, PKG schema design, temporal-first architecture, bespoke PKG systems, upstream data fusion, multi-modal knowledge graphs, schema harmonization, temporal PKG
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

### Relevancy Assessment Criteria (Updated 2025 - Heterogeneous Data Focus)
- **High**: Heterogeneous data integration methodologies, temporal-first PKG architectures, schema harmonization techniques, upstream data orchestration, bespoke PKG system designs, multi-modal data fusion approaches
- **Medium**: Supporting technologies (graph databases, ETL frameworks, data quality tools), domain-specific integration patterns, schema evolution strategies
- **Low**: General knowledge graphs without heterogeneous data focus, static schema approaches, downstream-only processing

### Processing Priorities (Heterogeneous Data Integration 2025)
1. **Schema Design & Integration**: Papers on dynamic schema mapping, ontology alignment, multi-source data harmonization, temporal schema evolution
2. **Upstream Data Orchestration**: Early-stage data ingestion, real-time data validation, source quality assessment, data provenance tracking
3. **Temporal-First Architectures**: Time-centric modeling approaches, temporal query optimization, chronological data versioning, temporal entity resolution
4. **Bespoke System Patterns**: Domain-specific PKG architectures, modular integration frameworks, adaptive system designs, custom pipeline implementations
5. **Performance & Scalability**: Quantitative metrics on heterogeneous data processing, integration latency, schema adaptation efficiency, multi-source query performance
6. **Cross-Domain Integration**: Healthcare-education-enterprise data fusion, personal-professional knowledge integration, multi-organizational data sharing

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

- **Research Foundation**: 8 comprehensive analysis documents completed focusing on heterogeneous data integration in PKG systems
- **Papers Analyzed**: 98+ papers spanning 2020-2025 with emphasis on schema design, temporal architectures, and multi-source integration
- **Processing Status**: 144 out of 209 total in cache processed; 21 high-priority pending papers on heterogeneous data fusion identified
- **Research Convergence**: Clear consensus on temporal-first architectures with upstream-focused data orchestration
- **Key Breakthrough**: Bespoke PKG systems with heterogeneous data integration capabilities are implementation-ready
- **Current Priority**: Advanced schema harmonization techniques and upstream data quality frameworks
- **Domain Applications**: Healthcare multi-source integration, educational cross-platform data fusion, enterprise heterogeneous system unification
- **Technical Focus**: Dynamic schema evolution, temporal data versioning, and adaptive integration pipeline development

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

## Updated Research Strategy (2025-07-02): Heterogeneous Data Integration Phase

### **Research Focus Evolution**
Based on comprehensive analysis of 98+ papers across 8 detailed reports, we are transitioning from general PKG exploration to **specialized heterogeneous data integration architectures**. Our research emphasizes upstream data orchestration, temporal-first design principles, and bespoke system development for complex multi-source environments.

### **Key Research Domains for Heterogeneous Integration**
1. **Multi-Source Healthcare Data Fusion** (5 papers): Patient records, IoT sensors, clinical imaging, genomic data integration with 93% accuracy in temporal correlation
2. **Cross-Platform Educational Integration** (2 papers): LMS data, assessment systems, learning analytics, behavioral tracking with temporal learner modeling
3. **Enterprise Heterogeneous Systems**: ERP, CRM, document management, communication platforms with federated schema management
4. **Personal Multi-Device Data Unification**: Mobile, desktop, IoT, social media, productivity tools with privacy-preserving temporal aggregation

### **Core Technologies for Heterogeneous Data Integration**
- **Temporal-First Schema Design**: Native time-based data modeling achieving 94.8% performance with 90% latency reduction in multi-source queries
- **Dynamic Schema Harmonization**: Real-time ontology mapping and transformation with 78% entity resolution accuracy across heterogeneous sources
- **Upstream Data Quality Orchestration**: Early-stage validation, cleansing, and standardization pipelines with 97.5% data consistency rates
- **Adaptive Integration Frameworks**: Self-configuring connectors and transformation modules for diverse data source types and formats

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