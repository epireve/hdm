// Main Application Module for All Papers Page
import { TursoClient } from './turso-client.js';
import { PapersTable } from './papers-table.js';

class AllPapersApp {
    constructor() {
        this.tursoClient = new TursoClient();
        this.papersTable = null;
        this.allPapers = [];
        this.statistics = null;
        
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
            searchInput: document.getElementById('searchInput'),
            yearFilter: document.getElementById('yearFilter'),
            openAccessFilter: document.getElementById('openAccessFilter'),
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
            
            // Setup column selector
            this.setupColumnSelector();
            
            // Setup event listeners
            this.setupEventListeners();
            
            // Show controls and hide loading
            this.elements.controls.style.display = 'flex';
            this.elements.tableContainer.style.display = 'block';
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
    }

    populateFilters() {
        // Populate year filter
        this.statistics.years.forEach(year => {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            this.elements.yearFilter.appendChild(option);
        });
    }

    setupEventListeners() {
        // Search input with debounce
        let searchTimeout;
        this.elements.searchInput.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => this.applyFilters(), 300);
        });

        // Filter changes
        this.elements.yearFilter.addEventListener('change', () => this.applyFilters());
        this.elements.openAccessFilter.addEventListener('change', () => this.applyFilters());
        
        // Page size change
        this.elements.pageSize.addEventListener('change', () => {
            this.papersTable.setPageSize(parseInt(this.elements.pageSize.value));
        });

        // Pagination
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
        const yearFilter = this.elements.yearFilter.value;
        const openAccessFilter = this.elements.openAccessFilter.value;
        
        this.papersTable.filter(searchTerm, yearFilter, openAccessFilter);
    }

    updatePagination(detail) {
        this.elements.currentPage.textContent = detail.currentPage;
        this.elements.totalPages.textContent = detail.totalPages;
        this.elements.prevPage.disabled = detail.currentPage === 1;
        this.elements.nextPage.disabled = detail.currentPage === detail.totalPages;
        this.elements.pagination.style.display = detail.totalPages > 1 ? 'flex' : 'none';
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