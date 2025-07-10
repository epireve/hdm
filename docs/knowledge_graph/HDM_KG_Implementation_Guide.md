# HDM Knowledge Graph Implementation Guide

**Version**: 1.0.0  
**Last Updated**: January 2025  
**Status**: Implemented

## Table of Contents

1. [Prerequisites & Setup](#prerequisites--setup)
2. [Step-by-Step Implementation](#step-by-step-implementation)
3. [Configuration Options](#configuration-options)
4. [Customization Guide](#customization-guide)
5. [Testing Procedures](#testing-procedures)
6. [Performance Optimization](#performance-optimization)
7. [Troubleshooting Guide](#troubleshooting-guide)

---

## Prerequisites & Setup

### System Requirements

- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 1GB free space
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, or Edge 90+

### Python Environment Setup

1. **Create Virtual Environment**
   ```bash
   # Navigate to project directory
   cd hdm
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   # Core dependencies
   pip install pandas==2.3.0
   pip install networkx==3.5
   pip install scikit-learn==1.7.0
   pip install python-louvain==0.16
   pip install numpy==2.3.1
   
   # Or use requirements file
   pip install -r requirements.txt
   ```

3. **Verify Installation**
   ```python
   # test_imports.py
   import pandas
   import networkx
   import sklearn
   import community
   import numpy
   
   print("All imports successful!")
   print(f"pandas: {pandas.__version__}")
   print(f"networkx: {networkx.__version__}")
   print(f"scikit-learn: {sklearn.__version__}")
   ```

### Project Structure Setup

```bash
# Create necessary directories
mkdir -p scripts/graph_generation
mkdir -p visualization/{data,js,css}
mkdir -p docs/knowledge_graph/diagrams
mkdir -p papers
mkdir -p logs
```

## Step-by-Step Implementation

### Phase 1: Data Preparation

#### Step 1.1: Validate Input Data

```python
# validate_csv.py
import pandas as pd
import sys

def validate_csv(filepath):
    """Validate the research papers CSV file"""
    try:
        # Load CSV
        df = pd.read_csv(filepath, encoding='utf-8')
        
        # Check required columns
        required_columns = [
            'cite_key', 'title', 'authors', 'year', 'Relevancy',
            'Tags', 'Summary', 'TL;DR', 'Insights'
        ]
        
        missing = set(required_columns) - set(df.columns)
        if missing:
            print(f"❌ Missing columns: {missing}")
            return False
        
        # Check for duplicate cite_keys
        duplicates = df[df.duplicated('cite_key', keep=False)]
        if not duplicates.empty:
            print(f"❌ Duplicate cite_keys found: {duplicates['cite_key'].tolist()}")
            return False
        
        # Basic statistics
        print(f"✅ CSV validation passed!")
        print(f"📊 Total papers: {len(df)}")
        print(f"📅 Year range: {df['year'].min()} - {df['year'].max()}")
        print(f"🏷️  Unique tags: {df['Tags'].str.split(',').explode().nunique()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error validating CSV: {e}")
        return False

if __name__ == "__main__":
    validate_csv("research_papers_complete.csv")
```

#### Step 1.2: Clean and Preprocess Data

```python
# preprocess_data.py
def clean_authors(authors_str):
    """Clean author names"""
    if pd.isna(authors_str):
        return []
    
    # Remove quotes
    authors_str = authors_str.strip('"')
    
    # Split by comma and clean
    authors = [a.strip() for a in authors_str.split(',')]
    
    # Filter invalid entries
    valid_authors = []
    for author in authors:
        if author and author.lower() not in ['unavailable', 'unknown', 'et al.']:
            valid_authors.append(author)
    
    return valid_authors

def clean_tags(tags_str):
    """Clean and normalize tags"""
    if pd.isna(tags_str):
        return []
    
    # Remove quotes and split
    tags_str = tags_str.strip('"')
    tags = [t.strip() for t in tags_str.split(',')]
    
    # Remove empty tags
    return [t for t in tags if t]
```

### Phase 2: Graph Construction

#### Step 2.1: Initialize Graph Builder

```python
# build_graph.py
from scripts.graph_generation.graph_builder import HDMKnowledgeGraphBuilder

# Initialize builder
builder = HDMKnowledgeGraphBuilder('research_papers_complete.csv')

# Build the graph
graph = builder.build_graph()

print(f"Graph built with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
```

#### Step 2.2: Calculate Relationships

```python
# calculate_relationships.py
from scripts.graph_generation.relationship_extractor import RelationshipExtractor

# Load data
df = pd.read_csv('research_papers_complete.csv')

# Initialize extractor
extractor = RelationshipExtractor(df)

# Calculate similarities
similarity_matrix = extractor.generate_similarity_matrix()

# Add relationships to graph
builder.add_paper_relationships(similarity_matrix, threshold=0.3)
```

#### Step 2.3: Identify Themes

```python
# identify_themes.py
from scripts.graph_generation.theme_clusterer import ThemeClusterer

# Initialize clusterer
clusterer = ThemeClusterer(graph, df)

# Detect communities
communities = clusterer.detect_communities()

# Identify themes
themes = clusterer.identify_research_themes(n_topics=8)

# Analyze trends
temporal_trends = clusterer.analyze_temporal_trends()
```

### Phase 3: Data Export

#### Step 3.1: Generate JSON Files

```python
# export_data.py
import json
from pathlib import Path

# Create output directory
output_dir = Path('visualization/data')
output_dir.mkdir(parents=True, exist_ok=True)

# Export graph data
graph_data = builder.export_to_json(str(output_dir / 'graph_data.json'))

# Export similarities
extractor.export_similarity_matrix(str(output_dir / 'similarities.json'))

# Export themes
clusterer.export_themes(str(output_dir / 'themes.json'))

# Generate statistics
stats = generate_statistics(df, graph, communities, themes)
with open(output_dir / 'statistics.json', 'w') as f:
    json.dump(stats, f, indent=2)
```

### Phase 4: Visualization Setup

#### Step 4.1: Launch Visualization

```python
# launch.py
import http.server
import socketserver
import webbrowser
import threading

PORT = 8080

def start_server():
    os.chdir('visualization')
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        httpd.serve_forever()

# Start server in background
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Open browser
webbrowser.open(f"http://localhost:{PORT}")
```

## Configuration Options

### Backend Configuration

```python
# config.py
class Config:
    # Data processing
    CSV_ENCODING = 'utf-8'
    CSV_DELIMITER = ','
    
    # Graph construction
    MIN_PAPER_CONNECTIONS = 1
    MAX_NODE_SIZE = 50
    
    # Similarity thresholds
    TAG_SIMILARITY_THRESHOLD = 0.2
    CONTENT_SIMILARITY_THRESHOLD = 0.3
    COMBINED_SIMILARITY_THRESHOLD = 0.3
    
    # Theme identification
    NUM_THEMES = 8
    MIN_THEME_SIZE = 3
    LDA_ITERATIONS = 100
    
    # Performance
    ENABLE_CACHING = True
    PARALLEL_PROCESSING = True
    MAX_WORKERS = 4
```

### Frontend Configuration

```javascript
// config.js
const CONFIG = {
    // Force simulation
    FORCE: {
        CHARGE_STRENGTH: -100,
        LINK_DISTANCE: 80,
        COLLISION_RADIUS: 2,
        ALPHA_DECAY: 0.02
    },
    
    // Visual settings
    COLORS: {
        paper: '#4A90E2',
        author: '#7ED321',
        tag: '#F5A623',
        year: '#BD10E0'
    },
    
    // Interaction
    ZOOM: {
        MIN: 0.1,
        MAX: 10,
        DURATION: 750
    },
    
    // Performance
    RENDER_THRESHOLD: 1000,
    LABEL_THRESHOLD: 100
};
```

## Customization Guide

### Adding New Node Types

1. **Define Node Type in Backend**:
   ```python
   # In graph_builder.py
   def add_custom_node_type(self, data):
       for item in data:
           node_id = f"custom_{item['id']}"
           self.graph.add_node(node_id,
               node_type='custom',
               name=item['name'],
               # Add custom attributes
           )
           self.node_types['custom'].append(node_id)
   ```

2. **Add Visual Style in Frontend**:
   ```javascript
   // In graph.js
   this.colorScale['custom'] = '#YOUR_COLOR';
   this.sizeScale['custom'] = d => 10; // Size function
   ```

### Customizing Similarity Calculations

```python
# custom_similarity.py
def custom_similarity(paper1, paper2):
    """Add custom similarity metric"""
    # Your similarity logic
    score = 0.0
    
    # Example: keyword overlap
    keywords1 = set(extract_keywords(paper1))
    keywords2 = set(extract_keywords(paper2))
    
    if keywords1 and keywords2:
        overlap = len(keywords1 & keywords2)
        total = len(keywords1 | keywords2)
        score = overlap / total
    
    return score

# Add to relationship extractor
extractor.add_similarity_metric('custom', custom_similarity, weight=0.2)
```

### Modifying Theme Detection

```python
# custom_themes.py
from sklearn.decomposition import NMF

def custom_theme_detection(documents, n_topics=10):
    """Use NMF instead of LDA"""
    vectorizer = TfidfVectorizer(max_features=1000)
    doc_term_matrix = vectorizer.fit_transform(documents)
    
    nmf = NMF(n_components=n_topics, random_state=42)
    doc_topics = nmf.fit_transform(doc_term_matrix)
    
    return doc_topics, nmf.components_, vectorizer.get_feature_names_out()
```

### Customizing Visualizations

```javascript
// custom_viz.js
// Add new visual encoding
graph.nodes
    .attr('stroke', d => {
        // Custom stroke based on theme
        if (d.themes && d.themes.length > 0) {
            return themeColors[d.themes[0]];
        }
        return '#999';
    })
    .attr('stroke-width', d => {
        // Variable stroke width
        return d.importance > 0.8 ? 3 : 1;
    });

// Add custom interactions
graph.nodes.on('dblclick', (event, d) => {
    // Double-click to expand node connections
    expandNodeConnections(d);
});
```

## Testing Procedures

### Unit Tests

```python
# test_graph_builder.py
import unittest
from scripts.graph_generation.graph_builder import HDMKnowledgeGraphBuilder

class TestGraphBuilder(unittest.TestCase):
    def setUp(self):
        self.test_csv = 'test_data.csv'
        self.builder = HDMKnowledgeGraphBuilder(self.test_csv)
    
    def test_node_creation(self):
        graph = self.builder.build_graph()
        
        # Check node counts
        paper_nodes = [n for n, d in graph.nodes(data=True) 
                      if d.get('node_type') == 'paper']
        self.assertGreater(len(paper_nodes), 0)
    
    def test_edge_creation(self):
        graph = self.builder.build_graph()
        
        # Check edges exist
        self.assertGreater(graph.number_of_edges(), 0)
    
    def test_data_export(self):
        graph = self.builder.build_graph()
        data = self.builder.export_to_json('test_output.json')
        
        # Verify structure
        self.assertIn('nodes', data)
        self.assertIn('links', data)
        self.assertIn('stats', data)

if __name__ == '__main__':
    unittest.main()
```

### Integration Tests

```python
# test_integration.py
def test_full_pipeline():
    """Test complete processing pipeline"""
    # 1. Load data
    df = pd.read_csv('test_papers.csv')
    assert len(df) > 0
    
    # 2. Build graph
    builder = HDMKnowledgeGraphBuilder('test_papers.csv')
    graph = builder.build_graph()
    assert graph.number_of_nodes() > 0
    
    # 3. Calculate relationships
    extractor = RelationshipExtractor(df)
    similarities = extractor.generate_similarity_matrix()
    assert len(similarities) > 0
    
    # 4. Identify themes
    clusterer = ThemeClusterer(graph, df)
    themes = clusterer.identify_research_themes()
    assert len(themes) > 0
    
    print("✅ All integration tests passed!")
```

### Frontend Testing

```javascript
// test_graph.js
// Manual testing checklist
const tests = [
    {
        name: "Graph renders",
        test: () => document.querySelectorAll('.node').length > 0
    },
    {
        name: "Nodes are draggable",
        test: () => {
            const node = document.querySelector('.node');
            const event = new MouseEvent('mousedown');
            node.dispatchEvent(event);
            return true;
        }
    },
    {
        name: "Search works",
        test: () => {
            document.getElementById('search').value = 'knowledge';
            const event = new Event('input');
            document.getElementById('search').dispatchEvent(event);
            return true;
        }
    }
];

// Run tests
tests.forEach(test => {
    try {
        const result = test.test();
        console.log(`✅ ${test.name}: ${result ? 'PASS' : 'FAIL'}`);
    } catch (e) {
        console.log(`❌ ${test.name}: ERROR - ${e.message}`);
    }
});
```

## Performance Optimization

### Backend Optimizations

1. **Parallel Processing**:
   ```python
   from concurrent.futures import ThreadPoolExecutor
   
   def parallel_similarity_calculation(papers):
       with ThreadPoolExecutor(max_workers=4) as executor:
           futures = []
           for i, paper1 in enumerate(papers):
               for j, paper2 in enumerate(papers[i+1:], i+1):
                   future = executor.submit(calculate_similarity, paper1, paper2)
                   futures.append((i, j, future))
           
           # Collect results
           results = {}
           for i, j, future in futures:
               results[(i, j)] = future.result()
       
       return results
   ```

2. **Caching**:
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=1000)
   def cached_tfidf_calculation(text):
       """Cache expensive TF-IDF calculations"""
       return calculate_tfidf(text)
   ```

3. **Memory Optimization**:
   ```python
   # Use generators for large datasets
   def process_papers_in_batches(csv_file, batch_size=100):
       for chunk in pd.read_csv(csv_file, chunksize=batch_size):
           yield process_chunk(chunk)
   ```

### Frontend Optimizations

1. **Render Optimization**:
   ```javascript
   // Use viewport culling
   function cullNodes(nodes, viewport) {
       return nodes.filter(d => {
           return d.x > viewport.left - 50 &&
                  d.x < viewport.right + 50 &&
                  d.y > viewport.top - 50 &&
                  d.y < viewport.bottom + 50;
       });
   }
   ```

2. **Throttle Updates**:
   ```javascript
   // Throttle expensive operations
   const throttledUpdate = throttle(() => {
       updateGraph();
   }, 16); // 60 FPS
   
   simulation.on('tick', throttledUpdate);
   ```

3. **Progressive Loading**:
   ```javascript
   // Load data progressively
   async function loadGraphProgressive() {
       // Load core nodes first
       const coreData = await fetch('data/core_graph.json');
       renderGraph(coreData);
       
       // Load additional data
       const fullData = await fetch('data/graph_data.json');
       updateGraph(fullData);
   }
   ```

## Troubleshooting Guide

### Common Issues and Solutions

#### Issue: ImportError for python-louvain
```bash
# Error: No module named 'community'
# Solution:
pip uninstall community
pip install python-louvain
```

#### Issue: CSV parsing errors
```python
# Error: ParserError: Error tokenizing data
# Solution:
df = pd.read_csv(filepath, 
    encoding='utf-8',
    quoting=csv.QUOTE_MINIMAL,
    on_bad_lines='skip'
)
```

#### Issue: Graph not rendering
```javascript
// Check console for errors
console.log('Nodes:', graph.nodes.size());
console.log('Links:', graph.links.size());

// Verify data loaded
fetch('data/graph_data.json')
    .then(r => r.json())
    .then(data => console.log('Data loaded:', data));
```

#### Issue: Performance degradation
```python
# Profile the code
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here
process_data()

profiler.disable()
stats = pstats.Stats(profiler).sort_stats('cumulative')
stats.print_stats(10)  # Top 10 time consumers
```

### Debug Mode

```python
# Enable debug logging
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hdm_debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Health Checks

```python
# health_check.py
def check_system_health():
    checks = {
        'csv_exists': os.path.exists('research_papers_complete.csv'),
        'output_dir_writable': os.access('visualization/data', os.W_OK),
        'dependencies_installed': check_dependencies(),
        'memory_available': psutil.virtual_memory().percent < 80,
        'disk_space': psutil.disk_usage('/').percent < 90
    }
    
    for check, result in checks.items():
        status = '✅' if result else '❌'
        print(f"{status} {check}")
    
    return all(checks.values())
```

---

**Document Control**  
- **Author**: HDM Development Team  
- **Review Cycle**: Quarterly  
- **Next Review**: April 2025  
- **Distribution**: Public