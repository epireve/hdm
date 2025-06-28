# Changelog

## 2025-06-28

- **Agent Init:** Initialized the research agent.
- **Setup:** Created `gemini.md` to define the agent's purpose and structure.
- **Artifacts:** Created `research_table.md` for data collection and the `/papers` directory for storing downloads.
- **Focus:** Defined the initial research focus on Personal Knowledge Graph (PKG) challenges in HDM systems.
- **Progress Cache:** Implemented `progress_cache.json` to store research progress and enable continuation across sessions.
- **Title Extraction:** Successfully extracted proper titles for 7 out of 9 papers that had URLs as titles in progress_cache.json. Used WebFetch and Puppeteer tools for extraction. Failed on 2 papers (BMJ Open - 404 error, Semantic Scholar - truncated URL). Created papers_title_extraction_report.csv for tracking.
- **ArXiv PKG/HDM Search (2024-2025):** Executed comprehensive arXiv searches for Personal Knowledge Graph and HDM papers:
  - Found 9 highly relevant new papers from 2024-2025 focused on PKG construction, temporal knowledge graphs, privacy-preserving approaches, and heterogeneous data integration
  - Added papers to progress_cache.json with "pending" status for detailed analysis
  - Key papers include: PersonalAI (digital twins), Zep (temporal KG for agent memory), AriGraph (episodic memory), Privacy-Preserving Synthetic KGs
  - Total papers in cache: 108 (9 new pending papers added)