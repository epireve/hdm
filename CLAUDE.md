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
- **Papers Identified**: 336 potential papers discovered
- **Processing Status**: 5 processed, 331 pending/skipped
- **Key Findings**: Major gaps in temporal modeling and heterogeneous data fusion
- **Next Priority**: Process high-relevancy papers on temporal knowledge graphs

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