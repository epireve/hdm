// Handle user interactions with the graph
class GraphInteractions {
    constructor(graph, detailsPanelId) {
        this.graph = graph;
        this.detailsPanel = document.getElementById(detailsPanelId);
        this.detailsContent = document.getElementById('details-content');
        this.tooltip = document.getElementById('tooltip');
        
        this.setupEventHandlers();
    }
    
    setupEventHandlers() {
        // Node click - show details
        this.graph.nodes.on('click', (event, d) => {
            event.stopPropagation();
            this.showNodeDetails(d);
            this.graph.highlightNode(d.id);
        });
        
        // Node hover - show tooltip
        this.graph.nodes
            .on('mouseenter', (event, d) => {
                this.showTooltip(event, d);
            })
            .on('mouseleave', () => {
                this.hideTooltip();
            });
        
        // Background click - clear selection
        this.graph.container.on('click', () => {
            this.clearDetails();
            this.graph.clearHighlight();
        });
        
        // Control buttons
        document.getElementById('reset-zoom').addEventListener('click', () => {
            this.graph.resetZoom();
        });
        
        document.getElementById('toggle-labels').addEventListener('click', () => {
            this.graph.toggleLabels();
        });
        
        document.getElementById('export-svg').addEventListener('click', () => {
            this.graph.exportSVG();
        });
    }
    
    showTooltip(event, d) {
        const content = this.getTooltipContent(d);
        this.tooltip.innerHTML = content;
        this.tooltip.style.left = (event.pageX + 10) + 'px';
        this.tooltip.style.top = (event.pageY - 10) + 'px';
        this.tooltip.classList.add('visible');
    }
    
    hideTooltip() {
        this.tooltip.classList.remove('visible');
    }
    
    getTooltipContent(d) {
        switch (d.node_type) {
            case 'paper':
                return `<strong>${d.title}</strong><br/>
                        Year: ${d.year}<br/>
                        Relevancy: ${d.relevancy}`;
            case 'author':
                return `<strong>${d.id}</strong><br/>
                        Papers: ${d.papers?.length || 0}`;
            case 'tag':
                return `<strong>${d.name || d.id}</strong><br/>
                        Papers: ${d.papers?.length || 0}`;
            case 'year':
                return `<strong>Year ${d.value}</strong>`;
            default:
                return d.id;
        }
    }
    
    showNodeDetails(node) {
        let content = '';
        
        switch (node.node_type) {
            case 'paper':
                content = this.getPaperDetails(node);
                break;
            case 'author':
                content = this.getAuthorDetails(node);
                break;
            case 'tag':
                content = this.getTagDetails(node);
                break;
            case 'year':
                content = this.getYearDetails(node);
                break;
            default:
                content = '<p>No details available</p>';
        }
        
        this.detailsContent.innerHTML = content;
        
        // Add click handlers to linked items
        this.addDetailClickHandlers();
    }
    
    getPaperDetails(paper) {
        return `
            <div class="detail-section">
                <h3>${paper.title}</h3>
                <div class="detail-value">
                    <span class="detail-label">Year:</span> ${paper.year}
                </div>
                <div class="detail-value">
                    <span class="detail-label">Relevancy:</span> ${paper.relevancy}
                </div>
                <div class="detail-value">
                    <span class="detail-label">DOI:</span> ${paper.doi || 'N/A'}
                </div>
            </div>
            
            ${paper.tldr ? `
            <div class="detail-section">
                <h3>TL;DR</h3>
                <p>${paper.tldr}</p>
            </div>
            ` : ''}
            
            ${paper.insights ? `
            <div class="detail-section">
                <h3>Key Insights</h3>
                <p>${paper.insights}</p>
            </div>
            ` : ''}
            
            ${paper.summary ? `
            <div class="detail-section">
                <h3>Summary</h3>
                <p>${paper.summary}</p>
            </div>
            ` : ''}
            
            <div class="detail-section">
                <h3>Links</h3>
                ${paper.url ? `<a href="${paper.url}" target="_blank">View Paper</a>` : ''}
            </div>
            
            <div class="detail-section">
                <h3>Related Papers</h3>
                <ul class="detail-list" id="related-papers">
                    <!-- Will be populated dynamically -->
                </ul>
            </div>
        `;
    }
    
    getAuthorDetails(author) {
        const paperCount = author.papers?.length || 0;
        return `
            <div class="detail-section">
                <h3>${author.id}</h3>
                <div class="detail-value">
                    <span class="detail-label">Total Papers:</span> ${paperCount}
                </div>
            </div>
            
            <div class="detail-section">
                <h3>Papers</h3>
                <ul class="detail-list">
                    ${author.papers ? author.papers.map(paperId => 
                        `<li data-node-id="${paperId}" class="clickable-node">${paperId}</li>`
                    ).join('') : '<li>No papers found</li>'}
                </ul>
            </div>
            
            <div class="detail-section">
                <h3>Collaborators</h3>
                <ul class="detail-list" id="collaborators">
                    <!-- Will be populated dynamically -->
                </ul>
            </div>
        `;
    }
    
    getTagDetails(tag) {
        const paperCount = tag.papers?.length || 0;
        return `
            <div class="detail-section">
                <h3>${tag.name || tag.id}</h3>
                <div class="detail-value">
                    <span class="detail-label">Total Papers:</span> ${paperCount}
                </div>
            </div>
            
            <div class="detail-section">
                <h3>Papers with this tag</h3>
                <ul class="detail-list">
                    ${tag.papers ? tag.papers.slice(0, 10).map(paperId => 
                        `<li data-node-id="${paperId}" class="clickable-node">${paperId}</li>`
                    ).join('') : '<li>No papers found</li>'}
                    ${paperCount > 10 ? `<li>... and ${paperCount - 10} more</li>` : ''}
                </ul>
            </div>
            
            <div class="detail-section">
                <h3>Related Tags</h3>
                <div id="related-tags">
                    <!-- Will be populated dynamically -->
                </div>
            </div>
        `;
    }
    
    getYearDetails(year) {
        // Find papers from this year
        const papers = this.graph.data.nodes.filter(n => 
            n.node_type === 'paper' && n.year === year.value
        );
        
        return `
            <div class="detail-section">
                <h3>Year ${year.value}</h3>
                <div class="detail-value">
                    <span class="detail-label">Total Papers:</span> ${papers.length}
                </div>
            </div>
            
            <div class="detail-section">
                <h3>Papers from ${year.value}</h3>
                <ul class="detail-list">
                    ${papers.slice(0, 10).map(paper => 
                        `<li data-node-id="${paper.id}" class="clickable-node">${paper.title}</li>`
                    ).join('')}
                    ${papers.length > 10 ? `<li>... and ${papers.length - 10} more</li>` : ''}
                </ul>
            </div>
        `;
    }
    
    addDetailClickHandlers() {
        // Add click handlers to all clickable nodes in details
        document.querySelectorAll('.clickable-node').forEach(element => {
            element.addEventListener('click', (e) => {
                const nodeId = e.target.getAttribute('data-node-id');
                const node = this.graph.data.nodes.find(n => n.id === nodeId);
                if (node) {
                    this.showNodeDetails(node);
                    this.graph.highlightNode(nodeId);
                }
            });
        });
    }
    
    clearDetails() {
        this.detailsContent.innerHTML = '<p class="details-placeholder">Click on a node to view details</p>';
    }
    
    // Find related papers based on shared connections
    findRelatedPapers(paperId, limit = 5) {
        const relatedScores = {};
        
        // Find all connections of the paper
        this.graph.data.links.forEach(link => {
            if (link.source_id === paperId || link.target_id === paperId) {
                const otherId = link.source_id === paperId ? link.target_id : link.source_id;
                const otherNode = this.graph.data.nodes.find(n => n.id === otherId);
                
                if (otherNode && otherNode.node_type === 'paper') {
                    relatedScores[otherId] = (relatedScores[otherId] || 0) + (link.weight || 1);
                }
            }
        });
        
        // Sort by score and return top papers
        return Object.entries(relatedScores)
            .sort((a, b) => b[1] - a[1])
            .slice(0, limit)
            .map(([id, score]) => {
                const paper = this.graph.data.nodes.find(n => n.id === id);
                return { id, title: paper.title, score };
            });
    }
    
    // Find collaborators for an author
    findCollaborators(authorId) {
        const collaborators = new Set();
        const authorNode = this.graph.data.nodes.find(n => n.id === authorId);
        
        if (!authorNode || !authorNode.papers) return [];
        
        // For each paper by this author
        authorNode.papers.forEach(paperId => {
            // Find other authors of the same paper
            this.graph.data.links.forEach(link => {
                if (link.edge_type === 'authored_by' && link.source_id === paperId) {
                    const otherAuthorId = link.target_id;
                    if (otherAuthorId !== authorId) {
                        collaborators.add(otherAuthorId);
                    }
                }
            });
        });
        
        return Array.from(collaborators);
    }
}