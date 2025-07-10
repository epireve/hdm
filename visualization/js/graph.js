// Main graph visualization using D3.js force-directed layout
class HDMGraph {
    constructor(containerId, data) {
        this.container = d3.select(containerId);
        this.data = data;
        
        // Get container dimensions
        const rect = this.container.node().getBoundingClientRect();
        this.width = rect.width;
        this.height = rect.height;
        
        // Color scales for different node types
        this.colorScale = {
            'paper': '#4A90E2',
            'author': '#7ED321',
            'tag': '#F5A623',
            'year': '#BD10E0',
            'theme': '#E74C3C'
        };
        
        // Size scales
        this.sizeScale = {
            'paper': d => 8 + Math.sqrt(d.importance || 1) * 5,
            'author': d => 6 + Math.sqrt(d.papers?.length || 1) * 2,
            'tag': d => 5 + Math.sqrt(d.papers?.length || 1) * 1.5,
            'year': d => 6,
            'theme': d => 10
        };
        
        this.showLabels = false;
        this.simulation = null;
        this.nodes = null;
        this.links = null;
        this.labels = null;
        
        this.init();
    }
    
    init() {
        // Clear any existing content
        this.container.selectAll("*").remove();
        
        // Create zoom behavior
        this.zoom = d3.zoom()
            .scaleExtent([0.1, 10])
            .on('zoom', (event) => {
                this.g.attr('transform', event.transform);
            });
        
        // Apply zoom to SVG
        this.container.call(this.zoom);
        
        // Create main group for zooming/panning
        this.g = this.container.append('g');
        
        // Create groups for different elements (order matters for layering)
        this.linkGroup = this.g.append('g').attr('class', 'links');
        this.nodeGroup = this.g.append('g').attr('class', 'nodes');
        this.labelGroup = this.g.append('g').attr('class', 'labels');
        
        // Create force simulation
        this.createForceSimulation();
        
        // Render the graph
        this.render();
    }
    
    createForceSimulation() {
        // Create force simulation
        this.simulation = d3.forceSimulation(this.data.nodes)
            .force('link', d3.forceLink(this.data.links)
                .id(d => d.index)
                .distance(d => {
                    // Vary link distance based on edge type
                    if (d.edge_type === 'similar_to') return 100;
                    if (d.edge_type === 'authored_by') return 50;
                    if (d.edge_type === 'tagged_with') return 60;
                    return 80;
                })
                .strength(d => {
                    // Vary link strength based on weight
                    return d.weight || 0.5;
                })
            )
            .force('charge', d3.forceManyBody()
                .strength(d => {
                    // Stronger repulsion for larger nodes
                    const size = this.getNodeSize(d);
                    return -100 - size * 10;
                })
                .distanceMax(300)
            )
            .force('center', d3.forceCenter(this.width / 2, this.height / 2))
            .force('collision', d3.forceCollide()
                .radius(d => this.getNodeSize(d) + 2)
            );
        
        // Run simulation
        this.simulation.on('tick', () => this.ticked());
    }
    
    render() {
        // Render links
        this.links = this.linkGroup
            .selectAll('.link')
            .data(this.data.links)
            .enter()
            .append('line')
            .attr('class', 'link')
            .attr('stroke-width', d => Math.sqrt(d.weight || 1));
        
        // Render nodes
        this.nodes = this.nodeGroup
            .selectAll('.node')
            .data(this.data.nodes)
            .enter()
            .append('circle')
            .attr('class', d => `node ${d.node_type}`)
            .attr('r', d => this.getNodeSize(d))
            .attr('fill', d => this.colorScale[d.node_type] || '#999')
            .call(this.createDragBehavior());
        
        // Add labels (initially hidden)
        this.labels = this.labelGroup
            .selectAll('.node-label')
            .data(this.data.nodes.filter(d => d.node_type === 'paper' || d.node_type === 'theme'))
            .enter()
            .append('text')
            .attr('class', 'node-label')
            .text(d => this.getNodeLabel(d))
            .style('display', this.showLabels ? 'block' : 'none');
        
        // Add titles (tooltips) to nodes
        this.nodes.append('title')
            .text(d => this.getNodeTooltip(d));
    }
    
    getNodeSize(d) {
        const sizeFn = this.sizeScale[d.node_type];
        return sizeFn ? sizeFn(d) : 5;
    }
    
    getNodeLabel(d) {
        if (d.node_type === 'paper') {
            return d.title ? d.title.substring(0, 30) + '...' : d.id;
        }
        if (d.node_type === 'theme') {
            return d.name || d.id;
        }
        return d.id;
    }
    
    getNodeTooltip(d) {
        switch (d.node_type) {
            case 'paper':
                return `${d.title} (${d.year})`;
            case 'author':
                return `${d.id} (${d.papers?.length || 0} papers)`;
            case 'tag':
                return `${d.name || d.id} (${d.papers?.length || 0} papers)`;
            case 'year':
                return `Year ${d.value}`;
            default:
                return d.id;
        }
    }
    
    createDragBehavior() {
        return d3.drag()
            .on('start', (event, d) => {
                if (!event.active) this.simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            })
            .on('drag', (event, d) => {
                d.fx = event.x;
                d.fy = event.y;
            })
            .on('end', (event, d) => {
                if (!event.active) this.simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            });
    }
    
    ticked() {
        // Update link positions
        this.links
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);
        
        // Update node positions
        this.nodes
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);
        
        // Update label positions
        this.labels
            .attr('x', d => d.x)
            .attr('y', d => d.y - this.getNodeSize(d) - 5);
    }
    
    // Filter methods
    filterByType(types) {
        this.nodes.style('display', d => types.includes(d.node_type) ? 'block' : 'none');
        
        // Hide links connected to hidden nodes
        this.links.style('display', d => {
            const sourceVisible = types.includes(this.data.nodes[d.source.index].node_type);
            const targetVisible = types.includes(this.data.nodes[d.target.index].node_type);
            return sourceVisible && targetVisible ? 'block' : 'none';
        });
    }
    
    filterByYear(startYear, endYear) {
        if (!startYear && !endYear) {
            this.nodes.style('opacity', 1);
            this.links.style('opacity', 1);
            return;
        }
        
        // Find papers within year range
        const validPapers = new Set();
        this.data.nodes.forEach(node => {
            if (node.node_type === 'paper' && node.year >= startYear && node.year <= endYear) {
                validPapers.add(node.index);
            }
        });
        
        // Fade out nodes not connected to valid papers
        this.nodes.style('opacity', d => {
            if (d.node_type === 'paper') {
                return validPapers.has(d.index) ? 1 : 0.2;
            }
            // Check if connected to any valid paper
            const connected = this.data.links.some(link => {
                return (link.source.index === d.index && validPapers.has(link.target.index)) ||
                       (link.target.index === d.index && validPapers.has(link.source.index));
            });
            return connected ? 1 : 0.2;
        });
        
        this.links.style('opacity', d => {
            return validPapers.has(d.source.index) || validPapers.has(d.target.index) ? 1 : 0.1;
        });
    }
    
    highlightNode(nodeId) {
        // Find the node
        const targetNode = this.data.nodes.find(n => n.id === nodeId);
        if (!targetNode) return;
        
        // Get connected nodes
        const connectedNodes = new Set([targetNode.index]);
        this.data.links.forEach(link => {
            if (link.source.index === targetNode.index) {
                connectedNodes.add(link.target.index);
            }
            if (link.target.index === targetNode.index) {
                connectedNodes.add(link.source.index);
            }
        });
        
        // Update node styles
        this.nodes
            .classed('highlighted', d => d.index === targetNode.index)
            .classed('faded', d => !connectedNodes.has(d.index));
        
        // Update link styles
        this.links
            .classed('highlighted', d => 
                d.source.index === targetNode.index || d.target.index === targetNode.index)
            .classed('faded', d => 
                d.source.index !== targetNode.index && d.target.index !== targetNode.index);
    }
    
    clearHighlight() {
        this.nodes.classed('highlighted', false).classed('faded', false);
        this.links.classed('highlighted', false).classed('faded', false);
    }
    
    toggleLabels() {
        this.showLabels = !this.showLabels;
        this.labels.style('display', this.showLabels ? 'block' : 'none');
    }
    
    resetZoom() {
        this.container.transition()
            .duration(750)
            .call(this.zoom.transform, d3.zoomIdentity);
    }
    
    exportSVG() {
        // Get the SVG element
        const svgElement = this.container.node();
        const svgData = new XMLSerializer().serializeToString(svgElement);
        
        // Create a blob and download
        const blob = new Blob([svgData], { type: 'image/svg+xml' });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = 'hdm_knowledge_graph.svg';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }
}