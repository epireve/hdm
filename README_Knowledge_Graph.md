# HDM Knowledge Graph Visualization 🕸️

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/hdm)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![D3.js](https://img.shields.io/badge/d3.js-v7-orange.svg)](https://d3js.org)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)

> An interactive knowledge graph visualization system for exploring relationships between research papers in the Human Digital Memory (HDM) project, featuring heterogeneous data integration and temporal-first architecture insights.

## 🎯 Overview

The HDM Knowledge Graph Visualization transforms 342+ research papers into an interactive, explorable network that reveals hidden connections, research themes, and temporal trends. Built with Python for data processing and D3.js for visualization, it provides researchers with powerful tools to navigate the complex landscape of HDM-related research.

### ✨ Key Features

- **🔍 Multi-Entity Graph**: Visualize papers, authors, tags, and temporal relationships
- **🎨 Interactive Force-Directed Layout**: Dynamic, physics-based graph rendering
- **🔎 Advanced Search & Filtering**: Find papers by content, year, relevancy, or theme
- **📊 Research Theme Discovery**: Automatically identified research clusters using LDA
- **🤝 Collaboration Networks**: Explore author relationships and co-authorship patterns
- **📈 Temporal Analysis**: Track research evolution over time
- **💾 Multiple Export Formats**: Save as SVG, JSON, or GEXF

### 📸 Screenshots

![HDM Knowledge Graph Overview](docs/knowledge_graph/images/overview.png)
*Interactive force-directed graph showing 300+ papers and their relationships*

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Modern web browser (Chrome, Firefox, Safari, Edge)
- 4GB RAM minimum (8GB recommended for large graphs)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hdm.git
   cd hdm
   ```

2. **Install Python dependencies**
   ```bash
   pip install pandas networkx scikit-learn python-louvain
   ```

3. **Generate the knowledge graph data**
   ```bash
   python scripts/graph_generation/process_hdm_data.py
   ```

4. **Launch the visualization**
   ```bash
   python launch_visualization.py
   ```

   The visualization will open automatically in your default browser at `http://localhost:8080`

### 🎮 Basic Usage

- **Click** nodes to view detailed information
- **Drag** nodes to reposition them
- **Scroll** to zoom in/out
- **Search** for papers using the search box
- **Filter** by year, relevancy, or research theme
- Press **L** to toggle labels, **R** to reset zoom

## 📚 Documentation

Comprehensive documentation is available in the `docs/knowledge_graph/` directory:

| Document | Description |
|----------|-------------|
| [📋 Visualization Specification](docs/knowledge_graph/HDM_Knowledge_Graph_Visualization_Spec.md) | Project requirements, goals, and success criteria |
| [🏗️ Architecture Guide](docs/knowledge_graph/HDM_KG_Architecture.md) | System design, components, and data flow |
| [📊 Data Schema Reference](docs/knowledge_graph/HDM_KG_Data_Schema.md) | Input/output formats and transformations |
| [🛠️ Implementation Guide](docs/knowledge_graph/HDM_KG_Implementation_Guide.md) | Step-by-step development instructions |
| [📖 API Reference](docs/knowledge_graph/HDM_KG_API_Reference.md) | Complete API documentation for all components |
| [🗺️ Development Roadmap](docs/knowledge_graph/HDM_KG_Development_Roadmap.md) | Future features and enhancement plans |
| [👤 User Guide](docs/knowledge_graph/HDM_KG_User_Guide.md) | End-user documentation and tutorials |
| [🚢 Deployment Guide](docs/knowledge_graph/HDM_KG_Deployment_Guide.md) | Production deployment instructions |

## 🏗️ Project Structure

```
hdm/
├── scripts/
│   └── graph_generation/         # Python data processing
│       ├── graph_builder.py      # Graph construction
│       ├── relationship_extractor.py  # Similarity calculation
│       ├── theme_clusterer.py    # Theme identification
│       └── process_hdm_data.py   # Main processing script
├── visualization/                # Frontend application
│   ├── index.html               # Main HTML
│   ├── css/                     # Stylesheets
│   ├── js/                      # JavaScript modules
│   │   ├── graph.js            # D3.js visualization
│   │   ├── interactions.js     # User interactions
│   │   ├── filters.js          # Search/filter logic
│   │   └── main.js            # Application entry
│   └── data/                    # Generated JSON data
├── docs/knowledge_graph/        # Documentation
└── launch_visualization.py      # Quick launcher
```

## 🛠️ Technology Stack

### Backend (Data Processing)
- **Python 3.8+**: Core processing language
- **pandas**: Data manipulation and CSV processing
- **NetworkX**: Graph construction and analysis
- **scikit-learn**: TF-IDF and topic modeling (LDA)
- **python-louvain**: Community detection algorithm

### Frontend (Visualization)
- **D3.js v7**: Force-directed graph visualization
- **HTML5/CSS3**: Modern web standards
- **Vanilla JavaScript**: No framework dependencies

### Data Formats
- **Input**: CSV with 21 columns of paper metadata
- **Processing**: NetworkX graph structure
- **Output**: JSON for web visualization, GEXF for Gephi

## 📊 Features in Detail

### 🔍 Entity Types
- **Papers** (Blue nodes): Research papers with full metadata
- **Authors** (Green nodes): Researchers and their collaborations
- **Tags** (Orange nodes): Keywords and research topics
- **Years** (Purple nodes): Temporal organization

### 🎯 Relationship Types
- **Authorship**: Papers connected to their authors
- **Tagging**: Papers connected to their tags/keywords
- **Similarity**: Papers connected by content similarity
- **Temporal**: Papers connected by publication year

### 🧠 Research Theme Identification
- Automatic discovery of 8 major research themes
- LDA topic modeling on abstracts and summaries
- Community detection using Louvain algorithm
- Temporal trend analysis showing theme evolution

### ⚡ Performance
- Handles 300+ papers smoothly
- Optimized force simulation for responsive interaction
- Lazy loading for large datasets
- Progressive rendering for better UX

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python -m pytest tests/`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Coding Standards
- Python: Follow PEP 8
- JavaScript: Use ESLint configuration
- Documentation: Update relevant .md files
- Tests: Add tests for new features

## 📈 Performance Metrics

Current implementation performance:
- **Data Processing**: ~5 seconds for 342 papers
- **Graph Rendering**: <1 second initial render
- **Interaction Response**: <16ms (60 FPS)
- **Memory Usage**: ~200MB for full dataset

## 🐛 Known Issues

- GEXF export may fail with complex node attributes
- Large graphs (>1000 nodes) may experience performance degradation
- Some citation relationships not yet implemented

See [Issues](https://github.com/yourusername/hdm/issues) for full list.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **HDM Research Team**: For providing the research corpus
- **D3.js Community**: For the excellent visualization library
- **NetworkX Developers**: For the powerful graph analysis tools
- **scikit-learn Team**: For machine learning algorithms

## 📞 Contact

- **Project Lead**: [Your Name](mailto:your.email@example.com)
- **Issues**: [GitHub Issues](https://github.com/yourusername/hdm/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/hdm/discussions)

---

<p align="center">
  Made with ❤️ for the HDM Research Community
</p>