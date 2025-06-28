# Systematic Search Strategy & Query Development

## Advanced Search Query Database

### Core PKG Concept Queries

**Primary Boolean Queries:**
```sql
-- Core Personal Knowledge Graph Terms
("personal knowledge graph*" OR "individual knowledge graph*" OR "user knowledge graph*" OR "personalized knowledge graph*") 
AND (construction OR management OR reasoning OR completion OR population)
AND year:2020..2025

-- HDM and Digital Twin Integration
("human digital memory" OR "digital human twin*" OR "personal digital twin*" OR "individual digital representation")
AND ("knowledge graph*" OR "data integration" OR "semantic representation")
AND year:2020..2025

-- Temporal Knowledge Graphs with Personal Focus
("temporal knowledge graph*" OR "dynamic knowledge graph*" OR "evolving knowledge graph*" OR "time-aware knowledge graph*")
AND ("personal" OR "individual" OR "user" OR "personalized" OR "private")
AND year:2020..2025

-- Privacy-Preserving Personal Data
("privacy-preserving" OR "federated" OR "private" OR "secure" OR "decentralized") 
AND ("knowledge graph*" OR "personal data" OR "individual data" OR "user data")
AND (integration OR management OR processing)
AND year:2020..2025

-- Cross-Platform Data Integration
("heterogeneous data integration" OR "multimodal data fusion" OR "cross-platform integration")
AND ("personal" OR "individual" OR "user" OR "private")
AND ("knowledge graph*" OR "semantic representation")
AND year:2020..2025
```

**Application Domain Queries:**
```sql
-- Healthcare Applications
("personal health knowledge graph*" OR "patient knowledge graph*" OR "health digital twin*")
OR ("digital health" AND "knowledge graph*" AND ("personal" OR "patient" OR "individual"))
AND year:2020..2025

-- Personal Assistant & AI
("personal assistant" OR "conversational AI" OR "chatbot" OR "virtual assistant")
AND ("knowledge graph*" OR "personal data" OR "user modeling")
AND year:2020..2025

-- Productivity & Learning
("personal productivity" OR "personal learning" OR "knowledge management" OR "personal information management")
AND ("knowledge graph*" OR "semantic representation")
AND year:2020..2025

-- Lifelogging & Quantified Self
("lifelogging" OR "quantified self" OR "personal analytics" OR "self-tracking")
AND ("knowledge graph*" OR "data integration" OR "personal data")
AND year:2020..2025
```

### Database-Specific Search Strategies

#### arXiv Systematic Search
**Categories to Cover:**
- cs.AI (Artificial Intelligence)
- cs.DB (Databases)
- cs.HC (Human-Computer Interaction)  
- cs.CL (Computation and Language)
- cs.IR (Information Retrieval)
- cs.CY (Computers and Society)

**Search Commands:**
```bash
# arXiv API queries for each category
curl "http://export.arxiv.org/api/query?search_query=cat:cs.AI+AND+%28%22personal+knowledge+graph%22+OR+%22individual+knowledge+graph%22%29&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending"

curl "http://export.arxiv.org/api/query?search_query=cat:cs.DB+AND+%28%22temporal+knowledge+graph%22+OR+%22dynamic+knowledge+graph%22%29+AND+%28personal+OR+individual%29&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending"
```

#### IEEE Xplore Advanced Search
**Targeted Conferences (2020-2025):**
- ICDE (International Conference on Data Engineering)
- ICDM (International Conference on Data Mining)
- TKDE (Transactions on Knowledge and Data Engineering)
- TCYB (Transactions on Cybernetics)
- TPAMI (Transactions on Pattern Analysis and Machine Intelligence)

**Search Strategy:**
```
Advanced Search Fields:
- Document Title: "personal knowledge graph" OR "temporal knowledge graph"
- Abstract: ("individual data" OR "user data") AND ("integration" OR "management")
- Author Keywords: "knowledge graph" AND ("personal" OR "temporal" OR "privacy")
- Publication Year: 2020-2025
- Content Type: Conference Publications, Journal Articles
```

#### ACM Digital Library Search
**Targeted Venues:**
- SIGMOD (Management of Data)
- SIGKDD (Knowledge Discovery and Data Mining)
- CHI (Computer-Human Interaction)
- UIST (User Interface Software and Technology)
- WWW (World Wide Web Conference)

**Advanced Search Syntax:**
```
Title:("personal knowledge graph" OR "individual knowledge graph") 
OR Abstract:("temporal knowledge graph" AND (personal OR individual))
OR Keywords:("privacy-preserving" AND "knowledge graph")
Published:[2020 TO 2025]
```

#### PubMed/MEDLINE Search
**MeSH Terms and Keywords:**
```
("Personal Health Records"[MeSH] OR "Health Information Systems"[MeSH])
AND ("Knowledge Bases"[MeSH] OR "Data Integration"[MeSH])
AND ("knowledge graph*" OR "semantic representation")
AND ("2020"[PDAT] : "2025"[PDAT])

("Digital Health"[MeSH] OR "Precision Medicine"[MeSH])
AND ("knowledge graph*" OR "personal data integration")
AND ("2020/01/01"[PDAT] : "2025/12/31"[PDAT])
```

### Citation Network Analysis Strategy

#### Backward Citation Mining
**Process:**
1. Extract all references from top 20 most relevant papers in current corpus
2. Apply relevance filtering based on title/abstract screening
3. Prioritize papers published 2020-2025
4. Cross-reference with existing corpus to avoid duplicates

**Target Papers for Reference Mining:**
- PKG survey papers (Balog & Kenter 2019, Skjæveland et al. 2024)
- Temporal KG papers (Saxena et al. 2021, Chen et al. 2023)
- Privacy-preserving papers (PRIVAFRAME, blockchain health KG)
- Healthcare applications (CONNECTED, digital twin papers)

#### Forward Citation Tracking
**Tools and Methods:**
1. **Google Scholar**: "Cited by" feature for each core paper
2. **Semantic Scholar**: Citation tracking with relevance scoring
3. **Connected Papers**: Visual citation network exploration
4. **Web of Science**: Citation analysis (if available)

**Automated Citation Extraction:**
```python
# Pseudo-code for citation analysis
core_papers = get_top_papers_from_corpus(relevance_score > 4.0)
for paper in core_papers:
    citations = get_citing_papers(paper.doi, since_year=2020)
    filtered_citations = filter_by_relevance(citations)
    candidate_papers.extend(filtered_citations)
```

#### Author Following Strategy
**Key Researchers Identified:**
- Krisztian Balog (University of Stavanger) - PKG foundations
- Martin G. Skjæveland (University of Oslo) - PKG ecosystems
- Luigi Asprino (University of Bologna) - SPARQL Anything, data integration
- Qiang Sun (University of Western Australia) - Docs2KG, TimelineKGQA
- Researchers from healthcare digital twin papers

**Author Tracking Methods:**
1. Google Scholar author profiles with alert setup
2. ORCID profile monitoring
3. DBLP author page tracking
4. ResearchGate activity monitoring
5. Conference program committee participation

### Cross-Disciplinary Search Expansion

#### Human-Computer Interaction Venues
**Conferences:**
- CHI (Computer-Human Interaction)
- UIST (User Interface Software and Technology)
- UbiComp (Ubiquitous Computing)
- IUI (Intelligent User Interfaces)
- DIS (Designing Interactive Systems)

**Search Terms:**
```
"personal information management" OR "personal data organization"
OR "individual data integration" OR "user data management"
OR "digital memory" OR "personal computing"
AND ("interface" OR "interaction" OR "user experience")
```

#### Cognitive Science & Psychology
**Journals:**
- Cognitive Science
- Memory & Cognition
- Psychological Science
- Journal of Memory and Language
- Applied Cognitive Psychology

**Search Terms:**
```
("autobiographical memory" OR "personal memory" OR "episodic memory")
AND ("digital" OR "computational" OR "artificial" OR "technology")
OR ("memory augmentation" OR "cognitive assistance" OR "memory support")
```

#### Healthcare Informatics
**Venues:**
- JAMIA (Journal of the American Medical Informatics Association)
- JBI (Journal of Biomedical Informatics)
- AMIA Symposium Proceedings
- Applied Clinical Informatics
- International Journal of Medical Informatics

**Search Terms:**
```
("personal health record*" OR "patient data integration" OR "health data management")
AND ("knowledge graph*" OR "semantic representation" OR "data integration")
OR ("digital health twin*" OR "personalized medicine" OR "precision health")
```

### Quality Filtering and Relevance Assessment

#### First-Pass Filtering (Automated)
**Title-Based Filtering:**
- Must contain at least one core term: "knowledge graph", "personal data", "individual data", "digital memory", "temporal", "privacy-preserving"
- Exclude obvious false positives: "social media", "recommendation system" (unless combined with personal KG terms)
- Prioritize papers with multiple relevant terms

#### Second-Pass Filtering (Abstract Review)
**Relevance Scoring (1-5):**
- **5 (Directly Relevant)**: Explicitly about PKG, temporal KG with personal focus, or HDM systems
- **4 (Highly Relevant)**: Personal data integration with KG methods, privacy-preserving personal data
- **3 (Moderately Relevant)**: General KG methods applicable to personal data, related temporal/privacy work
- **2 (Potentially Relevant)**: Broader data integration or KG work with potential personal applications
- **1 (Not Relevant)**: General KG work without clear personal/individual focus

#### Third-Pass Filtering (Full-Text Assessment)
**Detailed Evaluation Criteria:**
1. **Technical Contribution**: Novel methods, frameworks, or significant improvements
2. **Personal Data Focus**: Clear connection to individual/personal data scenarios
3. **Implementation Evidence**: Prototype, evaluation, or real-world application
4. **Research Quality**: Rigorous methodology, proper evaluation, clear limitations

### Search Progress Tracking

#### Metrics to Track
1. **Search Coverage**: Databases searched, queries executed, results obtained
2. **Candidate Pipeline**: Papers identified → screened → included
3. **Quality Distribution**: Relevance scores, venue prestige, citation impact
4. **Gap Coverage**: Progress toward target numbers for each research area
5. **Temporal Distribution**: Papers by publication year 2020-2025

#### Weekly Progress Reports
**Template:**
```markdown
## Week [X] Search Progress Report

### Searches Completed
- arXiv: [X] queries, [Y] papers identified
- IEEE Xplore: [X] conferences searched, [Y] papers found  
- ACM DL: [X] venues covered, [Y] relevant papers
- Citation Analysis: [X] papers processed, [Y] new citations

### Screening Results
- Total Candidates: [X]
- Abstract Screened: [Y] 
- Full-Text Reviewed: [Z]
- Added to Corpus: [N]

### Gap Coverage Progress
- Temporal KG: [X]/50 target
- Privacy-Preserving: [Y]/30 target
- Multimodal: [Z]/25 target
- Evaluation: [N]/20 target

### Quality Metrics
- Average Relevance Score: [X.X]/5.0
- High-Impact Papers (Score ≥4): [Y]%
- Recent Papers (2024-2025): [Z]%
```

This systematic search strategy ensures comprehensive coverage while maintaining quality and relevance standards for our exhaustive systematic review.