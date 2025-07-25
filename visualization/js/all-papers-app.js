// Main Application Module for All Papers Page
import { TursoClient } from './turso-client.js';
import { PapersTable } from './papers-table.js';

class AllPapersApp {
    constructor() {
        this.tursoClient = new TursoClient();
        this.papersTable = null;
        this.allPapers = [];
        this.statistics = null;
        this.allFields = [];
        this.selectedFields = new Set();
        
        // DOM elements
        this.elements = {
            controls: document.getElementById('controls'),
            loading: document.getElementById('loading'),
            error: document.getElementById('error'),
            errorMessage: document.getElementById('errorMessage'),
            helpBox: document.getElementById('helpBox'),
            tableContainer: document.getElementById('tableContainer'),
            pagination: document.getElementById('pagination'),
            totalPapers: document.getElementById('totalPapers'),
            openAccessCount: document.getElementById('openAccessCount'),
            yearRange: document.getElementById('yearRange'),
            mainStats: document.getElementById('main-stats'),
            searchInput: document.getElementById('searchInput'),
            yearMin: document.getElementById('yearMin'),
            yearMax: document.getElementById('yearMax'),
            openAccessFilter: document.getElementById('openAccessFilter'),
            fieldFilterToggle: document.getElementById('fieldFilterToggle'),
            fieldFilterText: document.getElementById('fieldFilterText'),
            fieldFilterDropdown: document.getElementById('fieldFilterDropdown'),
            fieldSearchInput: document.getElementById('fieldSearchInput'),
            fieldFilterList: document.getElementById('fieldFilterList'),
            fieldSelectAll: document.getElementById('fieldSelectAll'),
            fieldClearAll: document.getElementById('fieldClearAll'),
            pageSize: document.getElementById('pageSize'),
            prevPage: document.getElementById('prevPage'),
            nextPage: document.getElementById('nextPage'),
            currentPage: document.getElementById('currentPage'),
            totalPages: document.getElementById('totalPages'),
            columnToggle: document.getElementById('columnToggle'),
            columnSelector: document.getElementById('columnSelector'),
            columnList: document.getElementById('columnList'),
            columnSelectorClose: document.getElementById('columnSelectorClose'),
            pdfModal: document.getElementById('pdfModal'),
            pdfFrame: document.getElementById('pdfFrame'),
            pdfModalClose: document.getElementById('pdfModalClose'),
            pdfOpenExternal: document.getElementById('pdfOpenExternal')
        };

        this.init();
    }

    async init() {
        try {
            // Show loading state
            this.showLoading(true);
            
            // Initialize Turso client
            await this.tursoClient.initialize();
            
            // Fetch all papers
            this.allPapers = await this.tursoClient.fetchAllPapers();
            
            // Calculate statistics
            this.statistics = await this.tursoClient.getStatistics(this.allPapers);
            
            // Update UI with statistics
            this.updateStatistics();
            
            // Initialize papers table
            this.papersTable = new PapersTable(this.elements.tableContainer, {
                pageSize: 100,
                sortBy: 'year',
                sortOrder: 'desc',
                onPaperClick: (paper) => this.handlePaperClick(paper)
            });
            
            this.papersTable.setPapers(this.allPapers);
            
            // Populate filters
            this.populateFilters();
            
            // Setup field filter
            this.setupFieldFilter();
            
            // Setup column selector
            this.setupColumnSelector();
            
            // Setup event listeners
            this.setupEventListeners();
            
            // Show controls and hide loading
            this.elements.controls.style.display = 'flex';
            this.elements.mainStats.style.display = 'block';
            this.elements.tableContainer.style.display = 'block';
            this.elements.pagination.style.display = 'flex';
            this.showLoading(false);
            
        } catch (error) {
            console.error('Initialization error:', error);
            this.showError(error.message);
        }
    }

    updateStatistics() {
        this.elements.totalPapers.textContent = this.statistics.totalPapers.toLocaleString();
        this.elements.openAccessCount.textContent = this.statistics.openAccessCount.toLocaleString();
        this.elements.yearRange.textContent = this.statistics.yearRange;
        
        // Initial main stats display
        this.updateMainStats();
    }
    
    updateMainStats() {
        if (!this.papersTable) return;
        
        const filteredCount = this.papersTable.filteredPapers.length;
        const totalCount = this.allPapers.length;
        const filteredOpenAccess = this.papersTable.filteredPapers.filter(p => p.is_open_access === 1).length;
        
        // Calculate year range from filtered papers
        const years = this.papersTable.filteredPapers
            .map(p => parseInt(p.year))
            .filter(year => !isNaN(year));
        const yearRange = years.length > 0 ? 
            `${Math.min(...years)}-${Math.max(...years)}` : 'N/A';
        
        // Get access type filter
        const accessFilter = this.elements.openAccessFilter.value;
        const accessText = accessFilter === 'true' ? 'Open Access Only' : 
                          accessFilter === 'false' ? 'Closed Access Only' : 'All Access Types';
        
        // Get field filter info
        const selectedFieldsCount = this.selectedFields.size;
        const totalFieldsCount = this.allFields.length;
        const fieldText = selectedFieldsCount === totalFieldsCount ? 'All Fields' :
                         selectedFieldsCount === 0 ? 'No Fields' :
                         `${selectedFieldsCount} Fields`;
        
        this.elements.mainStats.innerHTML = `
            Showing ${filteredCount.toLocaleString()} of ${totalCount.toLocaleString()} papers | 
            Open Access: ${filteredOpenAccess.toLocaleString()} | 
            Year Range: ${yearRange} | 
            Access: ${accessText} | 
            Fields: ${fieldText}
        `;
    }

    populateFilters() {
        // Set default year range values
        if (this.statistics.years.length > 0) {
            const minYear = Math.min(...this.statistics.years);
            const maxYear = Math.max(...this.statistics.years);
            this.elements.yearMin.placeholder = minYear.toString();
            this.elements.yearMax.placeholder = maxYear.toString();
            // Set min/max attributes based on data
            this.elements.yearMin.min = minYear.toString();
            this.elements.yearMax.max = maxYear.toString();
        }
    }
    
    setupFieldFilter() {
        // Extract all unique fields of study with counts
        const fieldCounts = new Map();
        
        this.allPapers.forEach(paper => {
            if (paper.fields_of_study) {
                try {
                    const fields = JSON.parse(paper.fields_of_study);
                    fields.forEach(field => {
                        fieldCounts.set(field, (fieldCounts.get(field) || 0) + 1);
                    });
                } catch {
                    // Handle parse error
                }
            }
        });
        
        // Convert to array and sort by count
        this.allFields = Array.from(fieldCounts.entries())
            .sort((a, b) => b[1] - a[1])
            .map(([field, count]) => ({ field, count, selected: true }));
        
        // Store selected fields
        this.selectedFields = new Set(this.allFields.map(f => f.field));
        
        // Render field list
        this.renderFieldList();
    }
    
    renderFieldList(searchTerm = '') {
        const filteredFields = searchTerm 
            ? this.allFields.filter(f => f.field.toLowerCase().includes(searchTerm.toLowerCase()))
            : this.allFields;
            
        this.elements.fieldFilterList.innerHTML = filteredFields.map(({ field, count, selected }) => `
            <div class="multi-select-item">
                <input type="checkbox" 
                       id="field-${this.sanitizeId(field)}" 
                       value="${this.escapeHtml(field)}" 
                       ${selected ? 'checked' : ''}>
                <label for="field-${this.sanitizeId(field)}">${this.escapeHtml(field)}</label>
                <span class="count">(${count})</span>
            </div>
        `).join('');
        
        // Add change listeners
        this.elements.fieldFilterList.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const field = e.target.value;
                const fieldObj = this.allFields.find(f => f.field === field);
                
                if (e.target.checked) {
                    this.selectedFields.add(field);
                    if (fieldObj) fieldObj.selected = true;
                } else {
                    this.selectedFields.delete(field);
                    if (fieldObj) fieldObj.selected = false;
                }
                
                this.updateFieldFilterText();
                this.applyFilters();
            });
        });
    }
    
    updateFieldFilterText() {
        const total = this.allFields.length;
        const selected = this.selectedFields.size;
        
        if (selected === 0) {
            this.elements.fieldFilterText.textContent = 'No fields selected';
        } else if (selected === total) {
            this.elements.fieldFilterText.textContent = 'All Fields';
        } else if (selected === 1) {
            this.elements.fieldFilterText.textContent = Array.from(this.selectedFields)[0];
        } else {
            this.elements.fieldFilterText.textContent = `${selected} fields selected`;
        }
    }
    
    sanitizeId(str) {
        return str.replace(/[^a-zA-Z0-9]/g, '-');
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    setupEventListeners() {
        // Search input with debounce
        let searchTimeout;
        this.elements.searchInput.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => this.applyFilters(), 300);
        });

        // Filter changes
        let yearTimeout;
        this.elements.yearMin.addEventListener('input', () => {
            clearTimeout(yearTimeout);
            yearTimeout = setTimeout(() => this.applyFilters(), 300);
        });
        this.elements.yearMax.addEventListener('input', () => {
            clearTimeout(yearTimeout);
            yearTimeout = setTimeout(() => this.applyFilters(), 300);
        });
        this.elements.openAccessFilter.addEventListener('change', () => this.applyFilters());
        
        // Field filter controls
        this.elements.fieldFilterToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            const isVisible = this.elements.fieldFilterDropdown.style.display === 'block';
            this.elements.fieldFilterDropdown.style.display = isVisible ? 'none' : 'block';
        });
        
        // Field search
        let fieldSearchTimeout;
        this.elements.fieldSearchInput.addEventListener('input', () => {
            clearTimeout(fieldSearchTimeout);
            fieldSearchTimeout = setTimeout(() => {
                this.renderFieldList(this.elements.fieldSearchInput.value);
            }, 200);
        });
        
        // Select/Clear all buttons
        this.elements.fieldSelectAll.addEventListener('click', () => {
            this.allFields.forEach(f => {
                f.selected = true;
                this.selectedFields.add(f.field);
            });
            this.renderFieldList(this.elements.fieldSearchInput.value);
            this.updateFieldFilterText();
            this.applyFilters();
        });
        
        this.elements.fieldClearAll.addEventListener('click', () => {
            this.allFields.forEach(f => {
                f.selected = false;
                this.selectedFields.clear();
            });
            this.renderFieldList(this.elements.fieldSearchInput.value);
            this.updateFieldFilterText();
            this.applyFilters();
        });
        
        // Click outside to close field dropdown
        document.addEventListener('click', (e) => {
            if (!this.elements.fieldFilterToggle.contains(e.target) && 
                !this.elements.fieldFilterDropdown.contains(e.target)) {
                this.elements.fieldFilterDropdown.style.display = 'none';
            }
        });
        
        // Page size change
        this.elements.pageSize.addEventListener('change', () => {
            this.papersTable.setPageSize(parseInt(this.elements.pageSize.value));
        });

        // Pagination - Bottom
        this.elements.prevPage.addEventListener('click', () => {
            const currentPage = this.papersTable.currentPage;
            this.papersTable.setPage(currentPage - 1);
        });

        this.elements.nextPage.addEventListener('click', () => {
            const currentPage = this.papersTable.currentPage;
            this.papersTable.setPage(currentPage + 1);
        });
        

        // Listen for pagination updates
        document.addEventListener('pagination-update', (e) => {
            this.updatePagination(e.detail);
        });
        
        // Column selector toggle
        this.elements.columnToggle.addEventListener('click', () => {
            const isVisible = this.elements.columnSelector.style.display === 'block';
            this.elements.columnSelector.style.display = isVisible ? 'none' : 'block';
        });
        
        // Close column selector
        this.elements.columnSelectorClose.addEventListener('click', () => {
            this.elements.columnSelector.style.display = 'none';
        });
        
        // Click outside to close
        document.addEventListener('click', (e) => {
            if (!this.elements.columnSelector.contains(e.target) && 
                !this.elements.columnToggle.contains(e.target)) {
                this.elements.columnSelector.style.display = 'none';
            }
        });
        
        // PDF modal handlers
        document.addEventListener('show-pdf', (e) => {
            this.showPdfModal(e.detail.url);
        });
        
        this.elements.pdfModalClose.addEventListener('click', () => {
            this.closePdfModal();
        });
        
        this.elements.pdfModal.addEventListener('click', (e) => {
            if (e.target === this.elements.pdfModal) {
                this.closePdfModal();
            }
        });
        
        // Escape key to close PDF modal
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.elements.pdfModal.style.display === 'block') {
                this.closePdfModal();
            }
        });
    }
    
    setupColumnSelector() {
        const columns = this.papersTable.getAvailableColumns();
        
        // Update the header to show column count
        document.querySelector('#columnSelector h4').textContent = `Show/Hide Columns (${columns.length} total)`;
        
        this.elements.columnList.innerHTML = columns.map(col => `
            <div class="column-item">
                <input type="checkbox" 
                       id="col-${col.key}" 
                       value="${col.key}" 
                       ${col.visible ? 'checked' : ''}>
                <label for="col-${col.key}">${col.label}</label>
            </div>
        `).join('');
        
        // Add change listeners
        this.elements.columnList.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                this.papersTable.toggleColumn(e.target.value);
            });
        });
        
        console.log(`Column selector setup with ${columns.length} columns:`, columns.map(c => c.label));
    }

    applyFilters() {
        const searchTerm = this.elements.searchInput.value;
        const yearMin = this.elements.yearMin.value ? parseInt(this.elements.yearMin.value) : null;
        const yearMax = this.elements.yearMax.value ? parseInt(this.elements.yearMax.value) : null;
        const openAccessFilter = this.elements.openAccessFilter.value;
        const fieldFilter = Array.from(this.selectedFields);
        
        this.papersTable.filter(searchTerm, { min: yearMin, max: yearMax }, openAccessFilter, fieldFilter);
        
        // Update the main stats display
        this.updateMainStats();
    }

    updatePagination(detail) {
        // Update bottom pagination
        this.elements.currentPage.textContent = detail.currentPage;
        this.elements.totalPages.textContent = detail.totalPages;
        this.elements.prevPage.disabled = detail.currentPage === 1;
        this.elements.nextPage.disabled = detail.currentPage === detail.totalPages;
        
        // Always show pagination
        this.elements.pagination.style.display = 'flex';
        
        // Update page info to include result count
        const startIndex = (detail.currentPage - 1) * this.papersTable.pageSize + 1;
        const endIndex = Math.min(detail.currentPage * this.papersTable.pageSize, detail.totalResults);
        
        const pageInfoHTML = `
            Showing <strong>${startIndex}-${endIndex}</strong> of <strong>${detail.totalResults}</strong> papers | 
            Page <strong>${detail.currentPage}</strong> of <strong>${detail.totalPages}</strong>
        `;
        
        // Update pagination
        this.elements.pagination.querySelector('.page-info').innerHTML = pageInfoHTML;
    }

    handlePaperClick(paper) {
        console.log('Paper clicked:', paper);
        // Future: Show paper details modal or navigate to paper page
    }

    showLoading(show) {
        this.elements.loading.style.display = show ? 'flex' : 'none';
    }

    showError(message) {
        this.elements.errorMessage.textContent = message;
        this.elements.error.style.display = 'block';
        this.showLoading(false);
        
        // Show help box for configuration errors
        if (message.includes('configuration')) {
            this.elements.helpBox.style.display = 'block';
        }
    }
    
    showPdfModal(url) {
        // Clean up the URL
        const cleanUrl = url.trim();
        
        console.log('Opening PDF:', cleanUrl);
        
        // Update the external link
        this.elements.pdfOpenExternal.href = cleanUrl;
        
        // Always show the modal for PDF viewing attempt
        this.elements.pdfModal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        
        // Set the iframe source
        this.elements.pdfFrame.src = cleanUrl;
        
        // Add error handling for iframe
        this.elements.pdfFrame.onerror = () => {
            console.error('Failed to load PDF:', cleanUrl);
        };
        
        // Add load handler to check if PDF loaded
        this.elements.pdfFrame.onload = () => {
            console.log('PDF loaded successfully:', cleanUrl);
        };
    }
    
    closePdfModal() {
        this.elements.pdfModal.style.display = 'none';
        this.elements.pdfFrame.src = '';
        document.body.style.overflow = 'auto'; // Restore scrolling
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new AllPapersApp();
});