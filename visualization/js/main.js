// Main application entry point
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Initializing HDM Knowledge Graph Visualization...');
    
    try {
        // Show loading state
        const graphContainer = document.getElementById('graph-container');
        graphContainer.innerHTML = '<div style="text-align: center; padding: 50px;">Loading knowledge graph data...</div>';
        
        // Load the graph data
        const response = await fetch('data/graph_data.json');
        if (!response.ok) {
            throw new Error(`Failed to load graph data: ${response.statusText}`);
        }
        
        const graphData = await response.json();
        console.log(`Loaded graph with ${graphData.nodes.length} nodes and ${graphData.links.length} links`);
        
        // Clear loading message
        graphContainer.innerHTML = '<svg id="graph"></svg><div id="tooltip" class="tooltip"></div>';
        
        // Initialize the graph
        const graph = new HDMGraph('#graph', graphData);
        
        // Initialize interactions
        const interactions = new GraphInteractions(graph, 'details-panel');
        
        // Initialize filters
        const filters = new GraphFilters(graph, graphData);
        
        // Update initial stats
        updateStats(graphData);
        
        // Make graph and filters globally accessible for debugging
        window.hdmGraph = graph;
        window.hdmFilters = filters;
        
        console.log('HDM Knowledge Graph visualization initialized successfully!');
        
    } catch (error) {
        console.error('Error initializing visualization:', error);
        document.getElementById('graph-container').innerHTML = 
            `<div style="text-align: center; padding: 50px; color: red;">
                Error loading visualization: ${error.message}<br>
                Please check that the data files exist in the data/ directory.
            </div>`;
    }
});

// Update statistics in the header
function updateStats(graphData) {
    // Count nodes by type
    const nodeCounts = graphData.nodes.reduce((counts, node) => {
        counts[node.node_type] = (counts[node.node_type] || 0) + 1;
        return counts;
    }, {});
    
    // Update UI
    document.getElementById('paper-count').textContent = nodeCounts.paper || 0;
    document.getElementById('author-count').textContent = nodeCounts.author || 0;
    
    // Load theme count from themes file
    fetch('data/themes.json')
        .then(response => response.json())
        .then(themeData => {
            document.getElementById('theme-count').textContent = themeData.themes.length;
        })
        .catch(() => {
            document.getElementById('theme-count').textContent = '0';
        });
}

// Handle window resize
let resizeTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        if (window.hdmGraph) {
            // Update graph dimensions
            const rect = document.getElementById('graph').getBoundingClientRect();
            window.hdmGraph.width = rect.width;
            window.hdmGraph.height = rect.height;
            
            // Re-center the simulation
            window.hdmGraph.simulation.force('center', 
                d3.forceCenter(rect.width / 2, rect.height / 2));
            window.hdmGraph.simulation.alpha(0.3).restart();
        }
    }, 250);
});

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + F: Focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        document.getElementById('search').focus();
    }
    
    // Escape: Clear search and filters
    if (e.key === 'Escape') {
        if (window.hdmFilters) {
            window.hdmFilters.reset();
        }
        if (window.hdmGraph) {
            window.hdmGraph.clearHighlight();
        }
    }
    
    // L: Toggle labels
    if (e.key === 'l' || e.key === 'L') {
        if (window.hdmGraph) {
            window.hdmGraph.toggleLabels();
        }
    }
    
    // R: Reset zoom
    if (e.key === 'r' || e.key === 'R') {
        if (window.hdmGraph) {
            window.hdmGraph.resetZoom();
        }
    }
});

// Performance optimization: Throttle intensive operations
function throttle(func, delay) {
    let lastCall = 0;
    return function(...args) {
        const now = new Date().getTime();
        if (now - lastCall < delay) {
            return;
        }
        lastCall = now;
        return func(...args);
    };
}

// Log version and build info
console.log('HDM Knowledge Graph Visualization v1.0');
console.log('Built with D3.js v7');
console.log('Data generated:', new Date().toISOString());