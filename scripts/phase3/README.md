# PKG/HDM Research Explorer

An interactive visualization tool for exploring the Personal Knowledge Graph (PKG) and Human Digital Memory (HDM) research landscape.

## Overview

This tool provides three visualization modes to explore 100 key technical concepts extracted from PKG/HDM research papers:

1. **Network Graph** - Interactive force-directed graph showing concept relationships
2. **Hierarchical Tree** - Category-based organization of concepts
3. **Co-occurrence Matrix** - Heatmap showing concept relationships

## Usage

### Quick Start

1. Generate the visualization data:
   ```bash
   python scripts/phase3/prepare_visualization_data.py
   ```

2. Open the visualization in your browser:
   ```bash
   python scripts/phase3/start_server.py
   ```
   
   Or manually navigate to:
   ```
   http://localhost:8080/visualization/pkg_research_explorer/
   ```

### Features

#### Interactive Controls
- **View Mode**: Switch between Network, Hierarchy, and Matrix views
- **Category Filter**: Focus on specific concept categories (e.g., algorithms, methodologies)
- **Frequency Slider**: Filter concepts by minimum occurrence frequency
- **Reset View**: Return to default settings
- **Export Selection**: Download selected concepts and notes as JSON

#### Network Graph Features
- **Drag nodes** to reposition them
- **Click nodes** to select/deselect for export
- **Hover** over nodes to see details
- **Zoom and pan** using mouse/trackpad
- Node size indicates concept frequency
- Edge thickness shows relationship strength

#### Research Notes
- Add personal notes about your research exploration
- Notes are saved locally in your browser
- Export notes along with selected concepts

### Data Structure

The visualization is powered by `visualization/pkg_research_explorer/data/visualization_data.json` which contains:
- **100 technical concepts** with frequencies and categories
- **Concept relationships** (edges) based on co-occurrence
- **Hierarchical groupings** by category
- **Filter options** for exploration

### Categories

Concepts are organized into 8 main categories:
- **knowledge_graph**: PKG, temporal KG, reasoning, etc.
- **hdm_specific**: HDM, heterogeneous data integration, temporal-first
- **algorithms**: GNN, transformers, NLP, etc.
- **methodologies**: Privacy-preserving, temporal modeling, etc.
- **performance_metrics**: Accuracy, scalability, latency
- **architectures**: Temporal-first, lambda, microservices
- **frameworks_tools**: Neo4j, GraphDB, Cassandra
- **data_integration**: Data lakes, standardization, security

### Export Format

Exported data includes:
```json
{
  "selectedConcepts": [
    {
      "name": "temporal knowledge graph",
      "category": "knowledge_graph",
      "frequency": 75
    }
  ],
  "notes": {
    "2024-01-10T...": "Research note text..."
  },
  "timestamp": "2024-01-10T..."
}
```

## Technical Details

- Built with D3.js v7 for visualizations
- Pure JavaScript (no build process required)
- Local storage for research notes
- Responsive design for various screen sizes

## Customization

To add more concepts or modify the visualization:
1. Edit the data extraction in `scripts/phase3/prepare_visualization_data.py`
2. Regenerate the data file
3. Modify visualization parameters in `visualization/pkg_research_explorer/index.html`

## Tips for Research Planning

1. **Start with high-frequency concepts** to understand the core research areas
2. **Use category filters** to focus on specific technical aspects
3. **Look for sparse connections** in the network to identify research gaps
4. **Export concept clusters** that align with your research interests
5. **Add notes** about potential research directions as you explore