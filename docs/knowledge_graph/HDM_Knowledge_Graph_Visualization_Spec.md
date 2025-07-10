# HDM Knowledge Graph Visualization Specification

**Version**: 1.0.0  
**Last Updated**: January 2025  
**Status**: Implemented  

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Goals & Objectives](#project-goals--objectives)
3. [Functional Requirements](#functional-requirements)
4. [Non-Functional Requirements](#non-functional-requirements)
5. [User Stories & Use Cases](#user-stories--use-cases)
6. [Success Metrics](#success-metrics)
7. [Constraints & Assumptions](#constraints--assumptions)
8. [Glossary of Terms](#glossary-of-terms)

---

## Executive Summary

The HDM Knowledge Graph Visualization project transforms the Human Digital Memory research corpus into an interactive, explorable network visualization. By processing 342+ academic papers through advanced natural language processing and graph algorithms, the system reveals hidden relationships, identifies research themes, and provides researchers with powerful tools to navigate the complex landscape of heterogeneous data integration in Personal Knowledge Graph (PKG) architectures.

### Key Deliverables

1. **Automated Knowledge Graph Generation**: Python-based pipeline that extracts entities and relationships from research papers
2. **Interactive Web Visualization**: D3.js-powered force-directed graph with rich interactions
3. **Research Theme Discovery**: Machine learning-driven identification of research clusters
4. **Multi-faceted Search & Filter**: Advanced querying capabilities across multiple dimensions
5. **Comprehensive Documentation**: Full technical and user documentation

### Target Audience

- **Primary**: HDM researchers and project team members
- **Secondary**: Academic researchers in knowledge graphs and PKG systems
- **Tertiary**: Students and practitioners interested in heterogeneous data integration

## Project Goals & Objectives

### Primary Goals

1. **Knowledge Discovery**
   - Enable researchers to discover non-obvious connections between papers
   - Identify emerging research themes and trends
   - Reveal collaboration networks and influential authors

2. **Research Navigation**
   - Provide intuitive exploration of 300+ research papers
   - Support multiple navigation paradigms (search, filter, browse)
   - Enable deep-dive into specific research areas

3. **Gap Identification**
   - Highlight under-researched areas in the HDM landscape
   - Show temporal evolution of research topics
   - Identify potential collaboration opportunities

### Specific Objectives

| Objective | Description | Success Criteria |
|-----------|-------------|------------------|
| Entity Extraction | Extract papers, authors, tags, years from CSV | 100% of valid entries processed |
| Relationship Discovery | Identify connections between entities | >1000 meaningful relationships |
| Theme Identification | Discover research clusters using ML | 5-10 coherent themes |
| Performance | Smooth interaction with 300+ nodes | <16ms frame time |
| Usability | Intuitive interface requiring no training | <5min to productive use |

## Functional Requirements

### FR1: Data Processing Pipeline

**FR1.1**: CSV Data Ingestion
- Load research_papers_complete.csv with 21 columns
- Handle malformed entries gracefully
- Support incremental updates

**FR1.2**: Entity Extraction
- Extract paper metadata (title, year, DOI, URL)
- Parse author names handling various formats
- Extract and normalize tags/keywords
- Identify temporal information

**FR1.3**: Relationship Calculation
- Calculate tag-based similarity (Jaccard coefficient)
- Compute content similarity (TF-IDF + cosine)
- Identify temporal proximity relationships
- Detect co-authorship patterns

**FR1.4**: Theme Discovery
- Apply LDA topic modeling to abstracts
- Perform community detection on paper network
- Track theme evolution over time
- Generate theme keywords and summaries

### FR2: Interactive Visualization

**FR2.1**: Graph Rendering
- Force-directed layout using D3.js
- Node sizing based on importance metrics
- Color coding by entity type
- Smooth animations and transitions

**FR2.2**: User Interactions
- Click nodes for detailed information
- Drag nodes to reposition
- Zoom and pan capabilities
- Hover for quick previews

**FR2.3**: Search Functionality
- Full-text search across titles and content
- Author name search
- Tag/keyword search
- Real-time result highlighting

**FR2.4**: Filtering System
- Filter by publication year
- Filter by relevancy (High/Medium/Low)
- Filter by research theme
- Toggle entity type visibility

### FR3: Information Display

**FR3.1**: Node Details Panel
- Display complete paper information
- Show author publication lists
- List related papers
- Display relevancy and insights

**FR3.2**: Statistics Dashboard
- Total counts by entity type
- Theme distribution
- Temporal statistics
- Network metrics

**FR3.3**: Visual Indicators
- Node size indicates importance
- Edge thickness shows relationship strength
- Color coding for entity types
- Highlighting for selections

### FR4: Data Export

**FR4.1**: Visualization Export
- Export as SVG image
- Export visible subgraph
- Include current filter state

**FR4.2**: Data Export
- Export to GEXF for Gephi
- Export filtered data as JSON
- Generate statistics reports

## Non-Functional Requirements

### NFR1: Performance

| Metric | Requirement | Current Status |
|--------|-------------|----------------|
| Initial Load Time | <3 seconds | ✅ ~2 seconds |
| Graph Render Time | <1 second | ✅ <1 second |
| Interaction Response | 60 FPS (16ms) | ✅ Achieved |
| Memory Usage | <500MB | ✅ ~200MB |
| Concurrent Users | 10+ | ✅ Client-side |

### NFR2: Usability

- **Intuitive Interface**: Users productive within 5 minutes
- **Responsive Design**: Works on screens 1024px and wider
- **Keyboard Shortcuts**: Common actions accessible via keyboard
- **Clear Visual Hierarchy**: Important elements prominently displayed
- **Helpful Feedback**: Loading states and error messages

### NFR3: Compatibility

- **Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Operating Systems**: Windows 10+, macOS 10.15+, Ubuntu 20.04+
- **Python**: 3.8+ for data processing
- **Screen Resolution**: Minimum 1024x768

### NFR4: Scalability

- **Nodes**: Handle up to 1000 nodes smoothly
- **Edges**: Support 5000+ relationships
- **Data Size**: Process CSVs up to 100MB
- **Themes**: Identify 5-20 research themes

### NFR5: Maintainability

- **Modular Architecture**: Separate concerns clearly
- **Documentation**: Comprehensive inline and external docs
- **Code Quality**: Follow style guides (PEP 8, ESLint)
- **Version Control**: Git with semantic versioning

## User Stories & Use Cases

### User Stories

**US1**: As a **research lead**, I want to **identify gaps in current research** so that **I can direct future research efforts**.

**US2**: As a **PhD student**, I want to **find seminal papers in a specific area** so that **I can build my literature review**.

**US3**: As a **project manager**, I want to **track research progress over time** so that **I can report on project evolution**.

**US4**: As a **researcher**, I want to **discover potential collaborators** so that **I can form research partnerships**.

**US5**: As a **data scientist**, I want to **explore research themes** so that **I can understand the field landscape**.

### Use Cases

#### UC1: Exploring a Research Theme

**Actor**: Researcher  
**Precondition**: Visualization loaded with data  
**Main Flow**:
1. User selects a theme from filter dropdown
2. System highlights papers in that theme
3. User clicks on central paper node
4. System displays paper details and relationships
5. User explores connected papers
6. User exports subgraph for further analysis

**Alternative Flows**:
- 2a. No papers match theme → System shows message
- 4a. Paper has no relationships → Show standalone

#### UC2: Finding Author Collaborations

**Actor**: Research Coordinator  
**Precondition**: Author data available  
**Main Flow**:
1. User searches for specific author
2. System highlights author node
3. User clicks author node
4. System shows all papers and co-authors
5. User identifies frequent collaborators
6. User explores collaboration network

## Success Metrics

### Quantitative Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| User Adoption | 80% of team using within 1 month | Usage logs |
| Discovery Rate | 5+ new insights per user | User surveys |
| Performance | 95% of interactions <16ms | Performance monitoring |
| Data Coverage | 95% of papers with relationships | Graph statistics |
| Theme Coherence | 80% agreement on theme relevance | Expert evaluation |

### Qualitative Metrics

- **User Satisfaction**: Positive feedback in surveys
- **Research Impact**: Citations of discoveries made using tool
- **Time Savings**: Reduced time to find relevant papers
- **Collaboration**: New partnerships formed
- **Knowledge Sharing**: Increased cross-team awareness

## Constraints & Assumptions

### Technical Constraints

1. **Browser Limitations**: Complex graphs may slow older browsers
2. **Memory Constraints**: Client-side processing limits data size
3. **Network Dependency**: Requires local server or web hosting
4. **Data Format**: Input must be properly formatted CSV

### Organizational Constraints

1. **Resource Availability**: Limited development resources
2. **Time Constraints**: 6-week development timeline
3. **Skill Requirements**: JavaScript/Python expertise needed
4. **Maintenance**: Ongoing updates required

### Assumptions

1. **Data Quality**: CSV data is reasonably clean and complete
2. **User Technical Skill**: Basic computer literacy assumed
3. **Browser Availability**: Users have modern browsers
4. **Network Access**: Local network or internet available
5. **Data Growth**: Corpus grows at manageable rate

### Dependencies

1. **External Libraries**: D3.js, NetworkX, scikit-learn
2. **Data Source**: research_papers_complete.csv
3. **Python Environment**: Required packages installed
4. **Web Server**: HTTP server for visualization

## Glossary of Terms

| Term | Definition |
|------|------------|
| **Force-Directed Graph** | Graph layout where nodes repel and edges attract |
| **LDA** | Latent Dirichlet Allocation - topic modeling algorithm |
| **Jaccard Similarity** | Measure of set similarity (intersection/union) |
| **TF-IDF** | Term Frequency-Inverse Document Frequency |
| **Community Detection** | Algorithm to find clusters in graphs |
| **Node** | Entity in graph (paper, author, tag, year) |
| **Edge** | Relationship between nodes |
| **Degree Centrality** | Number of connections a node has |
| **PKG** | Personal Knowledge Graph |
| **HDM** | Human Digital Memory |

---

**Document Control**  
- **Author**: HDM Development Team  
- **Review Cycle**: Quarterly  
- **Next Review**: April 2025  
- **Distribution**: Public