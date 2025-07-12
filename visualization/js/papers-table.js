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
        
        // Create table HTML
        let html = `
            <table id="papersTable">
                <thead>
                    <tr>
                        ${this.createHeader('year', 'Year')}
                        ${this.createHeader('title', 'Title')}
                        ${this.createHeader('authors', 'Authors')}
                        ${this.createHeader('venue', 'Venue')}
                        ${this.createHeader('citation_count', 'Citations')}
                        ${this.createHeader('is_open_access', 'Access')}
                        <th>Fields of Study</th>
                    </tr>
                </thead>
                <tbody>
        `;

        if (this.filteredPapers.length === 0) {
            html += `
                <tr>
                    <td colspan="7" class="empty-state">
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
        // Parse fields of study
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
        
        // Parse authors
        let authorsDisplay = '';
        try {
            if (paper.authors) {
                const authors = JSON.parse(paper.authors);
                authorsDisplay = authors.map(a => a.name).join(', ');
            }
        } catch (e) {
            authorsDisplay = paper.authors || '';
        }

        const accessBadge = paper.is_open_access 
            ? '<span class="access-badge open-access">✓ Open Access</span>' 
            : '<span class="access-badge closed-access">Closed</span>';

        return `
            <tr data-paper-id="${paper.paper_id}">
                <td>${paper.year || 'N/A'}</td>
                <td>
                    <span class="paper-title" data-url="${paper.url || '#'}" title="${this.escapeHtml(paper.title || '')}">
                        ${this.escapeHtml(paper.title || 'Untitled')}
                    </span>
                </td>
                <td>
                    <div class="authors" title="${this.escapeHtml(authorsDisplay)}">
                        ${this.escapeHtml(authorsDisplay)}
                    </div>
                </td>
                <td class="venue">${this.escapeHtml(paper.venue || paper.journal || 'N/A')}</td>
                <td class="citation-count">${paper.citation_count || 0}</td>
                <td>${accessBadge}</td>
                <td>
                    <div class="tags">${fieldsOfStudy}</div>
                </td>
            </tr>
        `;
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
}