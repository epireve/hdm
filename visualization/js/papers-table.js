// Papers Table Component
export class PapersTable {
    constructor(container, options = {}) {
        this.container = container;
        this.papers = [];
        this.filteredPapers = [];
        this.currentPage = 1;
        this.pageSize = options.pageSize || 100;
        this.sortBy = options.sortBy || 'year';
        this.sortOrder = options.sortOrder || 'desc';
        
        this.onPaperClick = options.onPaperClick || null;
        
        // Available columns configuration
        this.availableColumns = {
            year: { label: 'Year', visible: true, sortable: true, width: '80px' },
            title: { label: 'Title', visible: true, sortable: true, width: '400px' },
            authors: { label: 'Authors', visible: true, sortable: true, width: '300px' },
            venue: { label: 'Venue', visible: true, sortable: true, width: '200px' },
            journal: { label: 'Journal', visible: false, sortable: true, width: '200px' },
            citation_count: { label: 'Citations', visible: true, sortable: true, width: '100px' },
            reference_count: { label: 'References', visible: false, sortable: true, width: '100px' },
            influential_citation_count: { label: 'Influential Citations', visible: false, sortable: true, width: '120px' },
            is_open_access: { label: 'Access', visible: true, sortable: true, width: '100px' },
            access_links: { label: 'Access Links', visible: true, sortable: false, width: '150px' },
            open_access_pdf: { label: 'Legacy PDF', visible: false, sortable: false, width: '80px' },
            fields_of_study: { label: 'Fields of Study', visible: true, sortable: false, width: '200px' },
            s2_fields_of_study: { label: 'S2 Fields', visible: false, sortable: false, width: '200px' },
            publication_types: { label: 'Pub Types', visible: false, sortable: false, width: '150px' },
            publication_date: { label: 'Pub Date', visible: false, sortable: true, width: '120px' },
            corpus_id: { label: 'Corpus ID', visible: false, sortable: true, width: '100px' },
            paper_id: { label: 'Paper ID', visible: false, sortable: false, width: '150px' },
            abstract: { label: 'Abstract', visible: false, sortable: false, width: '400px' },
            tldr: { label: 'TL;DR', visible: false, sortable: false, width: '300px' },
            first_seen: { label: 'First Seen', visible: false, sortable: true, width: '150px' },
            last_updated: { label: 'Last Updated', visible: false, sortable: true, width: '150px' },
            enrichment_timestamp: { label: 'Enrichment Time', visible: false, sortable: true, width: '150px' },
            unpaywall_best_oa_pdf_url: { label: 'Unpaywall PDF URL', visible: false, sortable: false, width: '200px' },
            unpaywall_best_oa_url: { label: 'Unpaywall OA URL', visible: false, sortable: false, width: '200px' }
        };
        
        // Load saved column preferences
        this.loadColumnPreferences();
    }

    setPapers(papers) {
        this.papers = papers;
        this.filteredPapers = [...papers];
        this.render();
    }

    filter(searchTerm, yearFilter, openAccessFilter) {
        this.filteredPapers = this.papers.filter(paper => {
            // Search filter
            if (searchTerm) {
                const search = searchTerm.toLowerCase();
                const searchIn = [
                    paper.title || '',
                    paper.abstract || '',
                    paper.authors || '',
                    paper.venue || '',
                    paper.journal || ''
                ].join(' ').toLowerCase();
                
                if (!searchIn.includes(search)) return false;
            }
            
            // Year filter
            if (yearFilter && paper.year != yearFilter) return false;
            
            // Open access filter
            if (openAccessFilter !== '') {
                const isOpenAccess = paper.is_open_access === 1;
                if (openAccessFilter === 'true' && !isOpenAccess) return false;
                if (openAccessFilter === 'false' && isOpenAccess) return false;
            }
            
            return true;
        });

        this.currentPage = 1;
        this.sort();
        this.render();
    }

    sort(column = null) {
        if (column) {
            if (this.sortBy === column) {
                this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
            } else {
                this.sortBy = column;
                this.sortOrder = 'desc';
            }
        }

        this.filteredPapers.sort((a, b) => {
            let aVal = a[this.sortBy];
            let bVal = b[this.sortBy];
            
            if (aVal == null) aVal = '';
            if (bVal == null) bVal = '';
            
            if (['year', 'citation_count', 'reference_count'].includes(this.sortBy)) {
                aVal = Number(aVal) || 0;
                bVal = Number(bVal) || 0;
            }
            
            if (typeof aVal === 'string') {
                aVal = aVal.toLowerCase();
                bVal = bVal.toLowerCase();
            }
            
            if (this.sortOrder === 'asc') {
                return aVal > bVal ? 1 : aVal < bVal ? -1 : 0;
            } else {
                return aVal < bVal ? 1 : aVal > bVal ? -1 : 0;
            }
        });
    }

    setPage(page) {
        const totalPages = Math.ceil(this.filteredPapers.length / this.pageSize);
        if (page >= 1 && page <= totalPages) {
            this.currentPage = page;
            this.render();
            window.scrollTo(0, 0);
        }
    }

    setPageSize(size) {
        this.pageSize = size;
        this.currentPage = 1;
        this.render();
    }

    render() {
        const totalPages = Math.ceil(this.filteredPapers.length / this.pageSize);
        const startIndex = (this.currentPage - 1) * this.pageSize;
        const endIndex = Math.min(startIndex + this.pageSize, this.filteredPapers.length);
        
        const visibleColumns = this.getVisibleColumns();
        const colCount = visibleColumns.length;
        
        // Create table HTML
        let html = `
            <table id="papersTable">
                <thead>
                    <tr>
        `;
        
        // Add headers for visible columns
        visibleColumns.forEach(col => {
            if (col.sortable) {
                html += this.createHeader(col.key, col.label);
            } else {
                html += `<th>${col.label}</th>`;
            }
        });
        
        html += `
                    </tr>
                </thead>
                <tbody>
        `;

        if (this.filteredPapers.length === 0) {
            html += `
                <tr>
                    <td colspan="${colCount}" class="empty-state">
                        <div class="empty-state-icon">📚</div>
                        <h3>No papers found</h3>
                        <p>Try adjusting your search or filters</p>
                    </td>
                </tr>
            `;
        } else {
            for (let i = startIndex; i < endIndex; i++) {
                html += this.createRow(this.filteredPapers[i]);
            }
        }

        html += `
                </tbody>
            </table>
        `;

        this.container.innerHTML = html;

        // Add event listeners
        this.attachEventListeners();

        // Update pagination info
        this.updatePagination(totalPages);
    }

    createHeader(column, label) {
        const isActive = this.sortBy === column;
        const arrow = isActive && this.sortOrder === 'asc' ? '▲' : '▼';
        const activeClass = isActive ? 'active' : '';
        
        return `
            <th data-sort="${column}">
                ${label} <span class="sort-arrow ${activeClass}">${arrow}</span>
            </th>
        `;
    }

    createRow(paper) {
        const visibleColumns = this.getVisibleColumns();
        let row = `<tr data-paper-id="${paper.paper_id}">`;
        
        visibleColumns.forEach(col => {
            row += this.createCell(paper, col.key);
        });
        
        row += '</tr>';
        return row;
    }
    
    createCell(paper, columnKey) {
        switch (columnKey) {
            case 'year':
                return `<td>${paper.year || 'N/A'}</td>`;
                
            case 'title':
                return `
                    <td>
                        <span class="paper-title" data-url="${paper.url || '#'}" title="${this.escapeHtml(paper.title || '')}">
                            ${this.escapeHtml(paper.title || 'Untitled')}
                        </span>
                    </td>
                `;
                
            case 'authors':
                let authorsDisplay = '';
                try {
                    if (paper.authors) {
                        const authors = JSON.parse(paper.authors);
                        authorsDisplay = authors.map(a => a.name).join(', ');
                    }
                } catch (e) {
                    authorsDisplay = paper.authors || '';
                }
                return `
                    <td>
                        <div class="authors" title="${this.escapeHtml(authorsDisplay)}">
                            ${this.escapeHtml(authorsDisplay)}
                        </div>
                    </td>
                `;
                
            case 'venue':
                return `<td class="venue">${this.escapeHtml(paper.venue || 'N/A')}</td>`;
                
            case 'journal':
                return `<td class="venue">${this.escapeHtml(paper.journal || 'N/A')}</td>`;
                
            case 'citation_count':
                return `<td class="citation-count">${paper.citation_count || 0}</td>`;
                
            case 'reference_count':
                return `<td class="citation-count">${paper.reference_count || 0}</td>`;
                
            case 'influential_citation_count':
                return `<td class="citation-count">${paper.influential_citation_count || 0}</td>`;
                
            case 'is_open_access':
                const accessBadge = paper.is_open_access 
                    ? '<span class="access-badge open-access">✓ Open Access</span>' 
                    : '<span class="access-badge closed-access">Closed</span>';
                return `<td>${accessBadge}</td>`;
                
            case 'fields_of_study':
                let fieldsOfStudy = '';
                try {
                    if (paper.fields_of_study) {
                        const fields = JSON.parse(paper.fields_of_study);
                        fieldsOfStudy = fields.slice(0, 3).map(field => 
                            `<span class="tag">${this.escapeHtml(field)}</span>`
                        ).join('');
                        if (fields.length > 3) {
                            fieldsOfStudy += ` <span class="tag">+${fields.length - 3}</span>`;
                        }
                    }
                } catch (e) {
                    // Handle parse error
                }
                return `<td><div class="tags">${fieldsOfStudy}</div></td>`;
                
            case 'publication_date':
                return `<td>${paper.publication_date || 'N/A'}</td>`;
                
            case 'corpus_id':
                return `<td>${paper.corpus_id || 'N/A'}</td>`;
                
            case 'paper_id':
                return `<td class="paper-id">${paper.paper_id}</td>`;
                
            case 'access_links':
                const buttons = [];
                
                // Primary: Unpaywall PDF URL
                if (paper.unpaywall_best_oa_pdf_url) {
                    const pdfUrl = paper.unpaywall_best_oa_pdf_url.trim();
                    if (pdfUrl && (pdfUrl.startsWith('http://') || pdfUrl.startsWith('https://'))) {
                        buttons.push(`
                            <button class="pdf-btn" data-pdf-url="${this.escapeHtml(pdfUrl)}" title="Direct PDF (Unpaywall)">
                                📄 PDF
                            </button>
                        `);
                    }
                }
                
                // Secondary: Unpaywall OA URL
                if (paper.unpaywall_best_oa_url) {
                    const oaUrl = paper.unpaywall_best_oa_url.trim();
                    if (oaUrl && (oaUrl.startsWith('http://') || oaUrl.startsWith('https://'))) {
                        buttons.push(`
                            <a href="${this.escapeHtml(oaUrl)}" target="_blank" class="oa-link-btn" title="Open Access Page (Unpaywall)">
                                🔗 OA
                            </a>
                        `);
                    }
                }
                
                // Tertiary: DOI URL
                if (paper.external_ids) {
                    try {
                        const externalIds = JSON.parse(paper.external_ids);
                        if (externalIds.DOI) {
                            const doiUrl = `https://doi.org/${externalIds.DOI}`;
                            buttons.push(`
                                <a href="${this.escapeHtml(doiUrl)}" target="_blank" class="doi-link-btn" title="DOI Link">
                                    🔍 DOI
                                </a>
                            `);
                        }
                    } catch (e) {
                        // Handle parse error
                    }
                }
                
                return `<td class="access-links-cell">${buttons.length > 0 ? buttons.join(' ') : '-'}</td>`;
                
            case 'open_access_pdf':
                // Legacy column - hidden by default
                if (paper.open_access_pdf) {
                    let pdfUrl = paper.open_access_pdf.trim();
                    if (pdfUrl && (pdfUrl.startsWith('http://') || pdfUrl.startsWith('https://'))) {
                        return `<td><button class="pdf-btn" data-pdf-url="${this.escapeHtml(pdfUrl)}" title="Legacy PDF">📄 PDF</button></td>`;
                    }
                }
                return '<td>-</td>';
                
            case 'abstract':
                if (paper.abstract) {
                    const truncated = paper.abstract.length > 100 
                        ? paper.abstract.substring(0, 100) + '...' 
                        : paper.abstract;
                    return `
                        <td>
                            <div class="abstract" title="${this.escapeHtml(paper.abstract)}">
                                ${this.escapeHtml(truncated)}
                            </div>
                        </td>
                    `;
                }
                return '<td>-</td>';
                
            case 'tldr':
                if (paper.tldr) {
                    try {
                        const tldrObj = JSON.parse(paper.tldr);
                        const tldrText = tldrObj.text || tldrObj;
                        return `<td class="tldr">${this.escapeHtml(tldrText)}</td>`;
                    } catch (e) {
                        return `<td class="tldr">${this.escapeHtml(paper.tldr)}</td>`;
                    }
                }
                return '<td>-</td>';
                
            case 's2_fields_of_study':
                let s2Fields = '';
                try {
                    if (paper.s2_fields_of_study) {
                        const fields = JSON.parse(paper.s2_fields_of_study);
                        s2Fields = fields.slice(0, 2).map(field => 
                            `<span class="tag">${this.escapeHtml(field.category)}</span>`
                        ).join('');
                    }
                } catch (e) {}
                return `<td><div class="tags">${s2Fields || '-'}</div></td>`;
                
            case 'publication_types':
                let pubTypes = '';
                try {
                    if (paper.publication_types) {
                        const types = JSON.parse(paper.publication_types);
                        pubTypes = types.map(type => 
                            `<span class="tag">${this.escapeHtml(type)}</span>`
                        ).join('');
                    }
                } catch (e) {}
                return `<td><div class="tags">${pubTypes || '-'}</div></td>`;
                
            case 'first_seen':
            case 'last_updated':
            case 'enrichment_timestamp':
                if (paper[columnKey]) {
                    const date = new Date(paper[columnKey]);
                    return `<td>${date.toLocaleDateString()}</td>`;
                }
                return '<td>-</td>';
                
            case 'unpaywall_best_oa_pdf_url':
                if (paper.unpaywall_best_oa_pdf_url) {
                    const url = paper.unpaywall_best_oa_pdf_url.trim();
                    return `<td><a href="${this.escapeHtml(url)}" target="_blank" class="link-url">${this.escapeHtml(url.substring(0, 50))}...</a></td>`;
                }
                return '<td>-</td>';
                
            case 'unpaywall_best_oa_url':
                if (paper.unpaywall_best_oa_url) {
                    const url = paper.unpaywall_best_oa_url.trim();
                    return `<td><a href="${this.escapeHtml(url)}" target="_blank" class="link-url">${this.escapeHtml(url.substring(0, 50))}...</a></td>`;
                }
                return '<td>-</td>';
                
            default:
                return `<td>${paper[columnKey] || 'N/A'}</td>`;
        }
    }

    attachEventListeners() {
        // Sort headers
        this.container.querySelectorAll('th[data-sort]').forEach(th => {
            th.addEventListener('click', () => {
                const column = th.getAttribute('data-sort');
                this.sort(column);
                this.render();
            });
        });

        // Paper titles
        this.container.querySelectorAll('.paper-title').forEach(title => {
            title.addEventListener('click', (e) => {
                const url = title.getAttribute('data-url');
                if (url && url !== '#') {
                    window.open(url, '_blank');
                }
                
                if (this.onPaperClick) {
                    const row = title.closest('tr');
                    const paperId = row.getAttribute('data-paper-id');
                    const paper = this.papers.find(p => p.paper_id === paperId);
                    if (paper) {
                        this.onPaperClick(paper);
                    }
                }
            });
        });
        
        // PDF buttons
        this.container.querySelectorAll('.pdf-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const pdfUrl = btn.getAttribute('data-pdf-url');
                if (pdfUrl) {
                    this.showPdfModal(pdfUrl);
                }
            });
        });
    }
    
    showPdfModal(pdfUrl) {
        // Dispatch event for the app to handle
        const event = new CustomEvent('show-pdf', {
            detail: { url: pdfUrl }
        });
        document.dispatchEvent(event);
    }

    updatePagination(totalPages) {
        const event = new CustomEvent('pagination-update', {
            detail: {
                currentPage: this.currentPage,
                totalPages: totalPages,
                totalResults: this.filteredPapers.length
            }
        });
        document.dispatchEvent(event);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Column management methods
    loadColumnPreferences() {
        const saved = localStorage.getItem('hdm-papers-columns');
        if (saved) {
            try {
                const preferences = JSON.parse(saved);
                Object.keys(preferences).forEach(key => {
                    if (this.availableColumns[key]) {
                        this.availableColumns[key].visible = preferences[key];
                    }
                });
            } catch (e) {
                console.error('Failed to load column preferences:', e);
            }
        }
    }
    
    saveColumnPreferences() {
        const preferences = {};
        Object.keys(this.availableColumns).forEach(key => {
            preferences[key] = this.availableColumns[key].visible;
        });
        localStorage.setItem('hdm-papers-columns', JSON.stringify(preferences));
    }
    
    toggleColumn(columnKey) {
        if (this.availableColumns[columnKey]) {
            this.availableColumns[columnKey].visible = !this.availableColumns[columnKey].visible;
            this.saveColumnPreferences();
            this.render();
        }
    }
    
    getVisibleColumns() {
        return Object.entries(this.availableColumns)
            .filter(([key, config]) => config.visible)
            .map(([key, config]) => ({ key, ...config }));
    }
    
    getAvailableColumns() {
        return Object.entries(this.availableColumns)
            .map(([key, config]) => ({ key, ...config }));
    }
}