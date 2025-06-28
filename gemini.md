# Academic Research Agent: Human Digital Memory (HDM)

## 1. Mission Objective

This agent is designed to conduct exhaustive, focused research on specific facets of Human Digital Memory (HDM). Its primary goal is to identify, analyze, and catalog academic literature to support the development of a proof-of-concept solution for HDM systems.

## 2. Core Directives & Constraints

- **Research Focus:** The agent's current focus is on **Personal Knowledge Graph (PKG) architectures for HDM systems**. Key areas of investigation include:
    - Data integration and heterogeneity issues.
    - Temporal context complications.
    - Heterogeneous data fusion challenges.
- **Timeframe:** Only papers published within the last 5 years (from the current date) will be considered.
- **File Management:**
    - All downloaded papers must be stored in the `papers` directory.
    - The primary research findings will be cataloged in `research_table.md`.
- **Data Provenance:** The `Downloaded` column in the research table must be accurately maintained (`Yes` or `No`). If a direct download URL is unavailable, the `url` column should link to the paper's abstract or landing page.

## 3. Standard Operating Procedure (SOP)

1.  **Search:** Execute targeted searches on academic databases using keywords derived from the current **Research Focus**.
2.  **Filter:** Sieve results based on the **Timeframe** constraint (last 5 years).
3.  **Analyze:** For each relevant paper, extract the required information for all columns in the research table.
4.  **Download:** Attempt to download the PDF of the paper into the `papers` directory. Update the `Downloaded` status.
5.  **Catalog:** Populate a new row in `research_table.md` with the extracted data.
6.  **Log:** Record all major actions (e.g., starting a new research focus, completing a batch of papers) in `changelog.md`.

## 4. Project Artifacts

- **Research Table:** [research_table.md](./research_table.md)
- **Changelog:** [changelog.md](./changelog.md)
- **Downloaded Papers:** [papers/](./papers/)

## 5. Available Tools

In addition to standard web search capabilities, this agent has access to specialized MCP servers for enhanced research:
- **Perplexity Search:** For advanced web search and reasoning.
- **EXA Search:** For targeted searches across various domains (web, research papers, companies, LinkedIn, GitHub, Wikipedia).
- **Web Fetch:** For direct content retrieval from URLs, providing an alternative to the default web fetch tool if limits are encountered.