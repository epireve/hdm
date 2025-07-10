// Handle filtering functionality for the graph
class GraphFilters {
    constructor(graph, data) {
        this.graph = graph;
        this.data = data;
        this.currentFilters = {
            search: '',
            year: null,
            relevancy: '',
            theme: '',
            nodeTypes: ['paper', 'author', 'tag']
        };
        
        this.init();
    }
    
    init() {
        this.populateFilters();
        this.setupEventListeners();
    }
    
    populateFilters() {
        // Populate year filter
        const years = [...new Set(this.data.nodes
            .filter(n => n.node_type === 'paper' && n.year)
            .map(n => n.year))]
            .sort((a, b) => b - a);
        
        const yearFilter = document.getElementById('year-filter');
        years.forEach(year => {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            yearFilter.appendChild(option);
        });
        
        // Populate theme filter if themes exist
        fetch('data/themes.json')
            .then(response => response.json())
            .then(themeData => {
                const themeFilter = document.getElementById('theme-filter');
                themeData.themes.forEach(theme => {
                    const option = document.createElement('option');
                    option.value = theme.id;
                    option.textContent = theme.name;
                    themeFilter.appendChild(option);
                });
            })
            .catch(err => console.log('No themes data available'));
    }
    
    setupEventListeners() {
        // Search input
        const searchInput = document.getElementById('search');
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.currentFilters.search = e.target.value.toLowerCase();
                this.applyFilters();
            }, 300);
        });
        
        // Year filter
        document.getElementById('year-filter').addEventListener('change', (e) => {
            this.currentFilters.year = e.target.value ? parseInt(e.target.value) : null;
            this.applyFilters();
        });
        
        // Relevancy filter
        document.getElementById('relevancy-filter').addEventListener('change', (e) => {
            this.currentFilters.relevancy = e.target.value;
            this.applyFilters();
        });
        
        // Theme filter
        document.getElementById('theme-filter').addEventListener('change', (e) => {
            this.currentFilters.theme = e.target.value;
            this.applyFilters();
        });
        
        // Node type checkboxes
        const nodeTypeCheckboxes = {
            'show-papers': 'paper',
            'show-authors': 'author',
            'show-tags': 'tag',
            'show-years': 'year'
        };
        
        Object.entries(nodeTypeCheckboxes).forEach(([checkboxId, nodeType]) => {
            const checkbox = document.getElementById(checkboxId);
            if (checkbox) {
                checkbox.addEventListener('change', (e) => {
                    if (e.target.checked) {
                        if (!this.currentFilters.nodeTypes.includes(nodeType)) {
                            this.currentFilters.nodeTypes.push(nodeType);
                        }
                    } else {
                        this.currentFilters.nodeTypes = this.currentFilters.nodeTypes
                            .filter(t => t !== nodeType);
                    }
                    this.applyFilters();
                });
            }
        });
    }
    
    applyFilters() {
        // Start with all nodes visible
        const visibleNodes = new Set();
        const hiddenNodes = new Set();
        
        this.data.nodes.forEach(node => {
            let visible = true;
            
            // Filter by node type
            if (!this.currentFilters.nodeTypes.includes(node.node_type)) {
                visible = false;
            }
            
            // Filter by search
            if (visible && this.currentFilters.search) {
                const searchTerm = this.currentFilters.search;
                let matches = false;
                
                if (node.node_type === 'paper') {
                    matches = node.title?.toLowerCase().includes(searchTerm) ||
                             node.id?.toLowerCase().includes(searchTerm) ||
                             node.summary?.toLowerCase().includes(searchTerm) ||
                             node.tldr?.toLowerCase().includes(searchTerm);
                } else if (node.node_type === 'author') {
                    matches = node.id.toLowerCase().includes(searchTerm);
                } else if (node.node_type === 'tag') {
                    matches = (node.name || node.id).toLowerCase().includes(searchTerm);
                }
                
                visible = matches;
            }
            
            // Filter by year (only for papers)
            if (visible && this.currentFilters.year && node.node_type === 'paper') {
                visible = node.year === this.currentFilters.year;
            }
            
            // Filter by relevancy (only for papers)
            if (visible && this.currentFilters.relevancy && node.node_type === 'paper') {
                visible = node.relevancy === this.currentFilters.relevancy;
            }
            
            // Filter by theme (only for papers)
            if (visible && this.currentFilters.theme && node.node_type === 'paper') {
                visible = node.themes && node.themes.includes(parseInt(this.currentFilters.theme));
            }
            
            if (visible) {
                visibleNodes.add(node.index);
            } else {
                hiddenNodes.add(node.index);
            }
        });
        
        // If filtering papers, also show their direct connections
        if (this.currentFilters.search || this.currentFilters.year || 
            this.currentFilters.relevancy || this.currentFilters.theme) {
            
            const additionalVisible = new Set();
            
            this.data.links.forEach(link => {
                if (visibleNodes.has(link.source.index) && !hiddenNodes.has(link.target.index)) {
                    additionalVisible.add(link.target.index);
                }
                if (visibleNodes.has(link.target.index) && !hiddenNodes.has(link.source.index)) {
                    additionalVisible.add(link.source.index);
                }
            });
            
            additionalVisible.forEach(idx => visibleNodes.add(idx));
        }
        
        // Apply visibility to nodes
        this.graph.nodes
            .style('display', d => visibleNodes.has(d.index) ? 'block' : 'none')
            .style('opacity', d => {
                // If we're filtering, fade non-matching nodes
                if (this.hasActiveFilters() && !this.matchesFilters(d)) {
                    return 0.3;
                }
                return 1;
            });
        
        // Apply visibility to links
        this.graph.links.style('display', d => {
            const sourceVisible = visibleNodes.has(d.source.index);
            const targetVisible = visibleNodes.has(d.target.index);
            return sourceVisible && targetVisible ? 'block' : 'none';
        });
        
        // Update stats
        this.updateStats(visibleNodes);
    }
    
    hasActiveFilters() {
        return this.currentFilters.search || 
               this.currentFilters.year || 
               this.currentFilters.relevancy || 
               this.currentFilters.theme;
    }
    
    matchesFilters(node) {
        if (node.node_type !== 'paper') return true;
        
        if (this.currentFilters.year && node.year !== this.currentFilters.year) {
            return false;
        }
        
        if (this.currentFilters.relevancy && node.relevancy !== this.currentFilters.relevancy) {
            return false;
        }
        
        if (this.currentFilters.theme && 
            (!node.themes || !node.themes.includes(parseInt(this.currentFilters.theme)))) {
            return false;
        }
        
        if (this.currentFilters.search) {
            const searchTerm = this.currentFilters.search;
            return node.title?.toLowerCase().includes(searchTerm) ||
                   node.id?.toLowerCase().includes(searchTerm) ||
                   node.summary?.toLowerCase().includes(searchTerm) ||
                   node.tldr?.toLowerCase().includes(searchTerm);
        }
        
        return true;
    }
    
    updateStats(visibleNodes) {
        // Count visible nodes by type
        const counts = {
            paper: 0,
            author: 0,
            tag: 0
        };
        
        this.data.nodes.forEach(node => {
            if (visibleNodes.has(node.index) && counts.hasOwnProperty(node.node_type)) {
                counts[node.node_type]++;
            }
        });
        
        // Update UI
        document.getElementById('paper-count').textContent = counts.paper;
        document.getElementById('author-count').textContent = counts.author;
        
        // Theme count from original data
        fetch('data/themes.json')
            .then(response => response.json())
            .then(themeData => {
                document.getElementById('theme-count').textContent = themeData.themes.length;
            })
            .catch(() => {
                document.getElementById('theme-count').textContent = '0';
            });
    }
    
    reset() {
        // Reset all filters
        document.getElementById('search').value = '';
        document.getElementById('year-filter').value = '';
        document.getElementById('relevancy-filter').value = '';
        document.getElementById('theme-filter').value = '';
        
        // Reset checkboxes
        document.getElementById('show-papers').checked = true;
        document.getElementById('show-authors').checked = true;
        document.getElementById('show-tags').checked = true;
        document.getElementById('show-years').checked = false;
        
        // Reset internal state
        this.currentFilters = {
            search: '',
            year: null,
            relevancy: '',
            theme: '',
            nodeTypes: ['paper', 'author', 'tag']
        };
        
        this.applyFilters();
    }
}