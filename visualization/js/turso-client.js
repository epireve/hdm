// Turso Database Client Module
export class TursoClient {
    constructor() {
        this.client = null;
        this.config = null;
    }

    async initialize() {
        // Check for configuration
        if (window.TURSO_CONFIG && window.TURSO_CONFIG.DATABASE_URL && window.TURSO_CONFIG.AUTH_TOKEN) {
            this.config = window.TURSO_CONFIG;
        } else {
            throw new Error('Database configuration not found');
        }

        // Dynamically import the client library
        const { createClient } = await import('https://cdn.jsdelivr.net/npm/@libsql/client@0.4.3/+esm');
        
        // Create client instance
        this.client = createClient({
            url: this.config.DATABASE_URL,
            authToken: this.config.AUTH_TOKEN
        });

        return this.client;
    }

    async fetchAllPapers() {
        if (!this.client) {
            throw new Error('Client not initialized');
        }

        const query = `
            SELECT 
                paper_id,
                title,
                abstract,
                venue,
                year,
                reference_count,
                citation_count,
                influential_citation_count,
                is_open_access,
                url,
                authors,
                fields_of_study,
                s2_fields_of_study,
                publication_types,
                journal,
                open_access_pdf,
                publication_date,
                external_ids,
                corpus_id,
                tldr,
                first_seen,
                last_updated,
                enrichment_timestamp,
                unpaywall_best_oa_pdf_url,
                unpaywall_best_oa_url,
                unpaywall_doi
            FROM papers 
            ORDER BY year DESC
        `;

        const result = await this.client.execute(query);
        return result.rows;
    }

    async getStatistics(papers) {
        const openAccessCount = papers.filter(p => p.is_open_access).length;
        const years = papers.map(p => p.year).filter(y => y);
        const minYear = Math.min(...years);
        const maxYear = Math.max(...years);

        // Count unique authors
        const authorSet = new Set();
        papers.forEach(paper => {
            try {
                if (paper.authors) {
                    const authors = JSON.parse(paper.authors);
                    authors.forEach(a => authorSet.add(a.name));
                }
            } catch (e) {
                // Handle parse error silently
            }
        });

        return {
            totalPapers: papers.length,
            openAccessCount,
            uniqueAuthors: authorSet.size,
            yearRange: `${minYear}-${maxYear}`,
            years: [...new Set(years)].sort((a, b) => b - a)
        };
    }

    close() {
        if (this.client) {
            this.client.close();
        }
    }
}