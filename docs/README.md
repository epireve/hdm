# Human Digital Memory (HDM) Research Project

## Overview

This repository contains a comprehensive academic literature review and analysis project focused on Human Digital Memory (HDM) systems, specifically investigating Personal Knowledge Graph (PKG) architectures. The project systematically reviews, processes, and analyzes academic research to inform the development of HDM solutions.

## Project Statistics

- **358 Research Papers** processed and analyzed
- **2,705 Images** automatically described using AI
- **398 PDF Files** converted to structured markdown
- **22 Metadata Columns** standardized across all papers
- **10 Duplicate Papers** identified and removed
- **100% Data Coverage** for downloaded papers

## Repository Structure

```
hdm/
├── research_papers_complete.csv    # Main research dataset (358 papers)
├── papers_clean.csv               # Clean metadata subset
├── research_findings.html         # Interactive web interface
├── CLAUDE.md                     # Project instructions
├── missing_papers.json           # Additional metadata
│
├── markdown_papers/              # 358 structured paper folders
│   └── [cite_key]/              # Individual paper directories
│       ├── paper.md             # Structured markdown content
│       ├── metadata.json        # Paper metadata
│       └── *.jpeg              # Extracted images with descriptions
│
├── papers/                      # Original PDF files (398 files)
├── analysis/                    # Research analysis documents
├── plan/                       # Research methodology
├── docs/                       # Documentation
├── scripts/                    # Processing and analysis scripts
│   ├── processing/             # Data processing scripts
│   └── analysis/              # Analysis and reporting scripts
│
└── archive/                    # Archived files and logs
    ├── old_scripts/
    ├── old_reports/
    ├── old_csvs/
    └── old_checkpoints/
```

## Key Features

### 📊 Research Database
- **Comprehensive Dataset**: 358 papers with standardized metadata
- **Quality Metrics**: 77.1% papers with DOI, 40.8% with tags
- **Relevancy Scoring**: High/Medium/Low classification system
- **Multi-source Integration**: Combined data from CSV, JSON, and markdown sources

### 🔍 Interactive Web Interface
- **Filter by Relevancy**: High, Medium, Low categories
- **Tag-based Search**: Multiple tag filtering capabilities
- **Year Range Filtering**: Temporal analysis support
- **GitHub Pages Ready**: Direct deployment from repository

### 🤖 Automated Processing
- **PDF to Markdown Conversion**: Structured content extraction
- **Image Description**: AI-powered image analysis using Gemini API
- **Metadata Standardization**: YAML frontmatter consistency
- **Duplicate Detection**: Fuzzy matching and exact duplicate removal

### 📈 Data Quality Assurance
- **Cite Key Management**: Systematic naming (lastname_year format)
- **Content Standardization**: Professional markdown formatting
- **Error Recovery**: Robust processing with retry mechanisms
- **Backup Systems**: Comprehensive data protection

## Usage

### Viewing Research Findings
1. Open `research_findings.html` in a web browser
2. Use filters to explore papers by relevancy, tags, or year
3. Click DOI/URL links to access original papers

### Accessing Paper Content
- Navigate to `markdown_papers/[cite_key]/paper.md` for structured content
- Images are in the same folder with AI-generated descriptions
- Metadata available in both YAML frontmatter and `metadata.json`

### Data Analysis
- Primary dataset: `research_papers_complete.csv`
- Clean subset: `papers_clean.csv`
- Additional metadata: `missing_papers.json`

## Research Focus Areas

### Personal Knowledge Graph (PKG) Architecture
- Data integration and heterogeneous data challenges
- Temporal context modeling and time-aware facts
- Privacy-preserving architectures and federated learning
- Scalability and performance optimization

### Key Research Gaps Identified
- **Temporal Modeling**: Only 6.6% of KG facts are time-aware
- **Data Integration**: 78% entity resolution accuracy challenges
- **Heterogeneous Fusion**: Complex multi-modal data integration
- **Privacy Architectures**: Zero-trust and federated approaches

### Research Trends (2020-2025)
- LLM-KG integration for enhanced reasoning
- Privacy-first design with local differential privacy
- User control mechanisms and transparency
- Cross-modal data integration approaches

## Technical Implementation

### Processing Pipeline
1. **PDF Collection**: Automated download and organization
2. **Content Extraction**: Marker-based PDF to markdown conversion
3. **Image Processing**: AI-powered description generation
4. **Metadata Enhancement**: Content analysis and tag generation
5. **Quality Validation**: Multi-stage data verification
6. **Standardization**: Consistent formatting and structure

### Technology Stack
- **Python**: Primary processing language
- **Gemini API**: Image description and content analysis
- **Marker**: PDF to markdown conversion
- **JavaScript/HTML/CSS**: Interactive web interface
- **Git**: Version control and GitHub Pages deployment

## Data Columns (Research CSV)

| Column | Description |
|--------|-------------|
| cite_key | Unique identifier (lastname_year format) |
| title | Paper title |
| authors | Author list |
| year | Publication year |
| Downloaded | Availability status |
| Relevancy | High/Medium/Low rating |
| Relevancy Justification | Explanation of relevancy |
| Insights | Key technical insights |
| TL;DR | One-sentence summary |
| Summary | Comprehensive abstract |
| Research Question | Primary research question |
| Methodology | Research methods |
| Key Findings | Main discoveries |
| Primary Outcomes | Concrete deliverables |
| Limitations | Acknowledged constraints |
| Conclusion | Author's assessment |
| Research Gaps | Identified gaps |
| Future Work | Suggested next steps |
| Implementation Insights | Practical takeaways |
| url | Direct link to paper |
| DOI | Digital Object Identifier |
| Tags | Comma-separated keywords |

## Quality Metrics

- **Data Completeness**: 100% for core fields (title, authors, year)
- **DOI Coverage**: 77.1% of papers have valid DOIs
- **Tag Coverage**: 40.8% of papers have descriptive tags
- **Image Descriptions**: 100% coverage (2,705 images)
- **Download Status**: 100% of papers available locally
- **Relevancy Assessment**: 27.1% High, 45.8% Medium, 27.1% Low

## Contributing

### Adding New Papers
1. Add PDF to `papers/` directory
2. Run processing scripts from `scripts/processing/`
3. Update CSV with new metadata
4. Regenerate web interface

### Updating Metadata
1. Edit markdown frontmatter in `markdown_papers/[cite_key]/paper.md`
2. Run `scripts/analysis/update_research_papers_complete.py`
3. Verify changes in web interface

## Academic Citation

This repository represents a systematic literature review of HDM and PKG research. When citing this work, please reference the comprehensive analysis of 358 papers spanning Personal Knowledge Graph architectures, temporal modeling challenges, and privacy-preserving implementations in Human Digital Memory systems.

## License

This research compilation is intended for academic and research purposes. Individual papers remain under their respective copyrights. Please cite original sources when referencing specific research findings.

## Contact

For questions about this research compilation or collaboration opportunities, please refer to the project documentation and analysis reports in the `analysis/` directory.