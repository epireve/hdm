# HDM Papers Database Export Guide

## Overview

The HDM Papers Database provides four distinct export formats, each optimized for different use cases. All exports are automatically generated and kept current through GitHub Actions.

## Available Export Formats

### 1. CSV Export (`hdm_papers_current.csv`)
**Size**: ~799KB | **Format**: Comma-separated values | **Best for**: Spreadsheet analysis, R/Python data science

**Structure**:
- 358 rows (one per paper)
- 25 columns in optimized order for analysis
- Clean, standardized data ready for Excel/R/Python/Pandas

**Column Order**:
```
cite_key, corrected_cite_key, title, authors, year, doi, url, 
relevancy, relevancy_justification, tldr, insights, summary, 
research_question, methodology, key_findings, primary_outcomes, 
limitations, conclusion, research_gaps, future_work, 
implementation_insights, tags, folder_path, csv_original_authors, 
date_processed
```

**Use Cases**:
- Statistical analysis in R or Python
- Excel pivot tables and data exploration
- Machine learning feature extraction
- Citation analysis and bibliometrics

### 2. JSON Export (`hdm_papers_current.json`)
**Size**: ~1.1MB | **Format**: Nested JSON structure | **Best for**: Programmatic access, APIs, web applications

**Structure**:
```json
{
  "metadata": {
    "total_papers": 358,
    "export_date": "2025-07-14T07:10:58",
    "date_range": "2019-2025",
    "version": "20250714_071058"
  },
  "papers": [
    {
      "metadata": { /* Technical information */ },
      "content": { /* Title, authors, summary */ },
      "research": { /* Academic details */ },
      "relevance": { /* HDM-specific insights */ }
    }
  ]
}
```

**Nested Organization**:
- `metadata`: cite_key, year, DOI, URL, processing info
- `content`: title, authors, TL;DR, summary
- `research`: methodology, findings, limitations, future work
- `relevance`: HDM insights, relevancy rating, tags

**Use Cases**:
- Web application backends
- Search engines and indexing
- API responses
- JavaScript/TypeScript applications

### 3. SQLite Backup (`hdm_papers_current.db`)
**Size**: ~2.5MB | **Format**: SQLite database | **Best for**: Complex queries, relational analysis

**Features**:
- Complete database replica with all relationships
- Ready for SQL queries and joins
- Maintains original data types and constraints
- Supports full-text search capabilities

**Sample Queries**:
```sql
-- High relevancy papers from 2024
SELECT title, authors, year FROM papers 
WHERE relevancy = 'HIGH' AND year = 2024;

-- Papers by research methodology
SELECT methodology, COUNT(*) FROM papers 
GROUP BY methodology;

-- Full-text search
SELECT title FROM papers 
WHERE title MATCH 'knowledge graph';
```

**Use Cases**:
- Complex analytical queries
- Data mining and research
- Report generation
- Academic research analysis

### 4. Markdown Documentation (`hdm_papers_current.md`)
**Size**: ~1.6KB | **Format**: GitHub-flavored Markdown | **Best for**: Human-readable overview, documentation

**Contents**:
- Database statistics and metrics
- Year distribution table
- Top 20 high-relevancy papers with descriptions
- Data quality indicators
- Export information

**Use Cases**:
- Project documentation
- GitHub README integration
- Research overviews
- Quality assessment reports

## Automated Export System

### GitHub Actions Workflow

The export system runs automatically on:
- **Push to main branch** (when database or scripts change)
- **Manual trigger** (workflow_dispatch)
- **Version tags** (creates releases)

### Versioning Strategy

Each export creates two versions:
1. **Current version**: `hdm_papers_current.*` (always latest)
2. **Timestamped archive**: `hdm_papers_YYYYMMDD_HHMMSS.*` (historical)

### Export Manifest

Each export generates `export_manifest.json` containing:
```json
{
  "timestamp": "20250714_071058",
  "date": "2025-07-14T07:10:58",
  "exports": {
    "csv": "exports/hdm_papers_current.csv",
    "json": "exports/hdm_papers_current.json",
    "sqlite": "exports/hdm_papers_current.db",
    "markdown": "exports/hdm_papers_current.md"
  },
  "statistics": { /* Database stats */ }
}
```

## Usage Examples

### Python (CSV)
```python
import pandas as pd

# Load the CSV
df = pd.read_csv('hdm_papers_current.csv')

# Filter high relevancy papers from 2024
high_2024 = df[(df['relevancy'] == 'HIGH') & (df['year'] == 2024)]

# Analyze by research methodology
methodology_counts = df['methodology'].value_counts()
```

### Python (JSON)
```python
import json

# Load the JSON
with open('hdm_papers_current.json', 'r') as f:
    data = json.load(f)

# Access papers
papers = data['papers']

# Filter by tags
pkg_papers = [p for p in papers if 'Knowledge Graph' in p['relevance']['tags']]
```

### R (CSV)
```r
# Load the CSV
papers <- read.csv('hdm_papers_current.csv')

# Create summary statistics
summary(papers$year)

# Filter and analyze
high_relevancy <- papers[papers$relevancy == 'HIGH', ]
table(high_relevancy$year)
```

### SQL (SQLite)
```sql
-- Connect to database and run queries
.open hdm_papers_current.db

-- Top authors by paper count
SELECT authors, COUNT(*) as paper_count 
FROM papers 
GROUP BY authors 
ORDER BY paper_count DESC 
LIMIT 10;

-- Research gaps analysis
SELECT research_gaps, COUNT(*) 
FROM papers 
WHERE research_gaps IS NOT NULL 
GROUP BY research_gaps;
```

## Data Quality Indicators

Each export includes quality metrics:
- **Author Quality**: 98.6% (353/358 with verified authors)
- **Year Accuracy**: 100% (all years verified)
- **DOI Coverage**: 81.6% (292/358 papers)
- **Tag Coverage**: Varies by paper relevancy

## File Locations

All exports are available in the `exports/` directory:
```
exports/
├── hdm_papers_current.csv     # Latest CSV
├── hdm_papers_current.json    # Latest JSON  
├── hdm_papers_current.db      # Latest SQLite
├── hdm_papers_current.md      # Latest documentation
├── export_manifest.json       # Export metadata
└── hdm_papers_YYYYMMDD_*.     # Timestamped archives
```

## Integration Tips

### For Researchers
- Use CSV for statistical analysis and visualization
- Use SQLite for complex queries and data mining
- Reference the Markdown for project overviews

### For Developers
- Use JSON for web applications and APIs
- Use SQLite for backend data storage
- Check the manifest for export metadata

### For Data Scientists
- CSV provides clean, analysis-ready data
- JSON offers nested structure for complex modeling
- SQLite enables advanced analytical queries

## Updates and Freshness

Exports are automatically refreshed when:
1. The main database is updated
2. Export scripts are modified
3. Manual export is triggered

Check the `export_date` in JSON metadata or manifest for last update timestamp.

---

*For technical details on export generation, see `scripts/data_export/export_data.py`*