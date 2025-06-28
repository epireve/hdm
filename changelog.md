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
- **Top-Tier Conference Mining (2023-2025):** Systematically searched 5 major conferences for PKG/HDM related papers:
  - **VLDB 2023-2024**: Found 4 papers on temporal graph systems (AeonG), privacy-preserving data management (PriPL-Tree, DPSUR), and trajectory privacy
  - **SIGMOD 2023-2024**: Found 3 papers on heterogeneous data integration, KG transformations, and accuracy estimation
  - **WWW 2023-2024**: Found 5 papers on privacy-preserving federated learning, machine unlearning, LinkGuard GNN privacy, and LLM-KG integration
  - **CHI 2023-2024**: Found 4 papers including Memoro (memory augmentation), synthetic personae, ThingPoll (IoT privacy), and LLMR
  - **KDD 2023-2024**: Found 3 workshop papers on temporal KG discovery, privacy-preserving temporal KGs, and personal analytics
  - Added 20 new papers to progress_cache.json (total now: 128 papers)
  - Created comprehensive conference_mining_report_2023_2025.md summarizing findings
  - Key trends: LLM-KG integration, privacy-first design with LDP, temporal capabilities, user control mechanisms
  - Identified gaps: Limited complete PKG systems, scalability for personal vs. enterprise use, cross-modal integration