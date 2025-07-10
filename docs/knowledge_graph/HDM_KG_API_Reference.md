# HDM Knowledge Graph API Reference

**Version**: 1.0.0  
**Last Updated**: January 2025  
**Status**: Implemented

## Table of Contents

1. [Python API Reference](#python-api-reference)
   - [HDMKnowledgeGraphBuilder](#hdmknowledgegraphbuilder)
   - [RelationshipExtractor](#relationshipextractor)
   - [ThemeClusterer](#themeclusterer)
2. [JavaScript API Reference](#javascript-api-reference)
   - [HDMGraph](#hdmgraph)
   - [GraphInteractions](#graphinteractions)
   - [GraphFilters](#graphfilters)
3. [Data Format Reference](#data-format-reference)
4. [Utility Functions](#utility-functions)

---

## Python API Reference

### HDMKnowledgeGraphBuilder

**Location**: `scripts/graph_generation/graph_builder.py`

**Purpose**: Constructs knowledge graph from research papers CSV data.

#### Class Definition

```python
class HDMKnowledgeGraphBuilder:
    def __init__(self, csv_path: str)
    def build_graph(self) -> nx.Graph
    def add_paper_relationships(self, similarity_matrix: Dict[Tuple[str, str], float], threshold: float = 0.3)
    def export_to_json(self, output_path: str) -> Dict
    def export_to_gexf(self, output_path: str)
    def get_subgraph_by_year(self, start_year: int, end_year: int) -> nx.Graph
    def get_author_collaboration_network(self) -> nx.Graph
```

#### Constructor

```python
__init__(self, csv_path: str)
```

**Parameters**:
- `csv_path` (str): Path to the research papers CSV file

**Example**:
```python
builder = HDMKnowledgeGraphBuilder('research_papers_complete.csv')
```

#### Methods

##### build_graph()

```python
def build_graph(self) -> nx.Graph
```

**Description**: Builds the knowledge graph from CSV data.

**Returns**: 
- `nx.Graph`: NetworkX graph with nodes and edges

**Example**:
```python
graph = builder.build_graph()
print(f"Created graph with {graph.number_of_nodes()} nodes")
```

##### add_paper_relationships()

```python
def add_paper_relationships(self, similarity_matrix: Dict[Tuple[str, str], float], threshold: float = 0.3)
```

**Description**: Adds similarity edges between papers.

**Parameters**:
- `similarity_matrix` (Dict[Tuple[str, str], float]): Paper pair similarities
- `threshold` (float): Minimum similarity to create edge (default: 0.3)

**Example**:
```python
similarities = {('paper1', 'paper2'): 0.75, ('paper1', 'paper3'): 0.45}
builder.add_paper_relationships(similarities, threshold=0.5)
```

##### export_to_json()

```python
def export_to_json(self, output_path: str) -> Dict
```

**Description**: Exports graph to D3.js compatible JSON format.

**Parameters**:
- `output_path` (str): Path for output JSON file

**Returns**:
- `Dict`: Graph data dictionary

**Example**:
```python
graph_data = builder.export_to_json('visualization/data/graph_data.json')
```

##### export_to_gexf()

```python
def export_to_gexf(self, output_path: str)
```

**Description**: Exports graph to GEXF format for Gephi.

**Parameters**:
- `output_path` (str): Path for output GEXF file

**Example**:
```python
builder.export_to_gexf('output/hdm_graph.gexf')
```

##### get_subgraph_by_year()

```python
def get_subgraph_by_year(self, start_year: int, end_year: int) -> nx.Graph
```

**Description**: Extracts subgraph for specific year range.

**Parameters**:
- `start_year` (int): Start year (inclusive)
- `end_year` (int): End year (inclusive)

**Returns**:
- `nx.Graph`: Subgraph containing papers from specified years

**Example**:
```python
recent_graph = builder.get_subgraph_by_year(2020, 2024)
```

##### get_author_collaboration_network()

```python
def get_author_collaboration_network(self) -> nx.Graph
```

**Description**: Creates author collaboration network.

**Returns**:
- `nx.Graph`: Graph with authors as nodes, collaborations as edges

**Example**:
```python
collab_network = builder.get_author_collaboration_network()
```

### RelationshipExtractor

**Location**: `scripts/graph_generation/relationship_extractor.py`

**Purpose**: Calculates various similarity metrics between papers.

#### Class Definition

```python
class RelationshipExtractor:
    def __init__(self, papers_df: pd.DataFrame)
    def calculate_tag_similarity(self) -> Dict[Tuple[str, str], float]
    def extract_keywords_from_summaries(self, max_features: int = 100) -> Dict[str, List[str]]
    def calculate_content_similarity(self) -> Dict[Tuple[str, str], float]
    def calculate_temporal_proximity(self, max_year_diff: int = 2) -> Dict[Tuple[str, str], float]
    def calculate_author_overlap(self) -> Dict[Tuple[str, str], float]
    def generate_similarity_matrix(self, weights: Dict[str, float] = None) -> Dict[Tuple[str, str], float]
    def get_top_similar_papers(self, paper_id: str, n: int = 5) -> List[Tuple[str, float]]
    def export_similarity_matrix(self, output_path: str, threshold: float = 0.2)
```

#### Constructor

```python
__init__(self, papers_df: pd.DataFrame)
```

**Parameters**:
- `papers_df` (pd.DataFrame): DataFrame containing paper data

**Example**:
```python
df = pd.read_csv('research_papers_complete.csv')
extractor = RelationshipExtractor(df)
```

#### Key Methods

##### calculate_tag_similarity()

```python
def calculate_tag_similarity(self) -> Dict[Tuple[str, str], float]
```

**Description**: Calculates Jaccard similarity based on tags.

**Returns**:
- `Dict[Tuple[str, str], float]`: Paper pairs with tag similarities

**Example**:
```python
tag_similarities = extractor.calculate_tag_similarity()
# Returns: {('paper1', 'paper2'): 0.6, ...}
```

##### extract_keywords_from_summaries()

```python
def extract_keywords_from_summaries(self, max_features: int = 100) -> Dict[str, List[str]]
```

**Description**: Extracts keywords using TF-IDF.

**Parameters**:
- `max_features` (int): Maximum number of features (default: 100)

**Returns**:
- `Dict[str, List[str]]`: Paper IDs mapped to keyword lists

**Example**:
```python
keywords = extractor.extract_keywords_from_summaries(max_features=50)
# Returns: {'paper1': ['knowledge', 'graph', 'learning'], ...}
```

##### generate_similarity_matrix()

```python
def generate_similarity_matrix(self, weights: Dict[str, float] = None) -> Dict[Tuple[str, str], float]
```

**Description**: Generates combined similarity matrix.

**Parameters**:
- `weights` (Dict[str, float]): Component weights (optional)
  - Default: `{'tags': 0.3, 'content': 0.3, 'temporal': 0.2, 'authors': 0.2}`

**Returns**:
- `Dict[Tuple[str, str], float]`: Combined similarities

**Example**:
```python
# Use default weights
similarities = extractor.generate_similarity_matrix()

# Custom weights
custom_weights = {'tags': 0.5, 'content': 0.3, 'temporal': 0.1, 'authors': 0.1}
similarities = extractor.generate_similarity_matrix(weights=custom_weights)
```

### ThemeClusterer

**Location**: `scripts/graph_generation/theme_clusterer.py`

**Purpose**: Identifies research themes through clustering and topic modeling.

#### Class Definition

```python
class ThemeClusterer:
    def __init__(self, graph: nx.Graph, papers_df: pd.DataFrame)
    def detect_communities(self) -> Dict[str, int]
    def identify_research_themes(self, n_topics: int = 10, top_words: int = 10) -> Dict[int, Dict[str, Any]]
    def analyze_temporal_trends(self) -> Dict[int, Dict[int, int]]
    def get_theme_summary(self) -> List[Dict[str, Any]]
    def export_themes(self, output_path: str)
    def get_theme_colors(self) -> Dict[int, str]
```

#### Constructor

```python
__init__(self, graph: nx.Graph, papers_df: pd.DataFrame)
```

**Parameters**:
- `graph` (nx.Graph): Knowledge graph
- `papers_df` (pd.DataFrame): Papers dataframe

**Example**:
```python
clusterer = ThemeClusterer(graph, df)
```

#### Key Methods

##### detect_communities()

```python
def detect_communities(self) -> Dict[str, int]
```

**Description**: Detects communities using Louvain algorithm.

**Returns**:
- `Dict[str, int]`: Paper IDs mapped to community IDs

**Example**:
```python
communities = clusterer.detect_communities()
# Returns: {'paper1': 0, 'paper2': 0, 'paper3': 1, ...}
```

##### identify_research_themes()

```python
def identify_research_themes(self, n_topics: int = 10, top_words: int = 10) -> Dict[int, Dict[str, Any]]
```

**Description**: Identifies themes using LDA topic modeling.

**Parameters**:
- `n_topics` (int): Number of topics to identify (default: 10)
- `top_words` (int): Top words per topic (default: 10)

**Returns**:
- `Dict[int, Dict[str, Any]]`: Theme data with keywords and papers

**Example**:
```python
themes = clusterer.identify_research_themes(n_topics=8)
# Returns: {0: {'name': 'knowledge_graph_learning', 'words': [...], ...}}
```

## JavaScript API Reference

### HDMGraph

**Location**: `visualization/js/graph.js`

**Purpose**: Main D3.js graph visualization class.

#### Class Definition

```javascript
class HDMGraph {
    constructor(containerId, data)
    init()
    createForceSimulation()
    render()
    filterByType(types)
    filterByYear(startYear, endYear)
    highlightNode(nodeId)
    clearHighlight()
    toggleLabels()
    resetZoom()
    exportSVG()
}
```

#### Constructor

```javascript
constructor(containerId, data)
```

**Parameters**:
- `containerId` (string): CSS selector for container element
- `data` (Object): Graph data with nodes and links

**Example**:
```javascript
const graph = new HDMGraph('#graph', graphData);
```

#### Methods

##### filterByType()

```javascript
filterByType(types)
```

**Description**: Shows only specified node types.

**Parameters**:
- `types` (Array<string>): Node types to show

**Example**:
```javascript
// Show only papers and authors
graph.filterByType(['paper', 'author']);
```

##### highlightNode()

```javascript
highlightNode(nodeId)
```

**Description**: Highlights a node and its connections.

**Parameters**:
- `nodeId` (string): ID of node to highlight

**Example**:
```javascript
graph.highlightNode('abdallah_2021');
```

##### toggleLabels()

```javascript
toggleLabels()
```

**Description**: Toggles node label visibility.

**Example**:
```javascript
graph.toggleLabels(); // Show/hide labels
```

##### exportSVG()

```javascript
exportSVG()
```

**Description**: Exports visualization as SVG file.

**Example**:
```javascript
document.getElementById('export-btn').onclick = () => graph.exportSVG();
```

### GraphInteractions

**Location**: `visualization/js/interactions.js`

**Purpose**: Handles user interactions with the graph.

#### Class Definition

```javascript
class GraphInteractions {
    constructor(graph, detailsPanelId)
    setupEventHandlers()
    showNodeDetails(node)
    clearDetails()
    findRelatedPapers(paperId, limit)
    findCollaborators(authorId)
}
```

#### Constructor

```javascript
constructor(graph, detailsPanelId)
```

**Parameters**:
- `graph` (HDMGraph): Graph instance
- `detailsPanelId` (string): ID of details panel element

**Example**:
```javascript
const interactions = new GraphInteractions(graph, 'details-panel');
```

#### Key Methods

##### showNodeDetails()

```javascript
showNodeDetails(node)
```

**Description**: Displays detailed information for a node.

**Parameters**:
- `node` (Object): Node data object

**Example**:
```javascript
// On node click
node.on('click', (event, d) => {
    interactions.showNodeDetails(d);
});
```

##### findRelatedPapers()

```javascript
findRelatedPapers(paperId, limit = 5)
```

**Description**: Finds papers related to given paper.

**Parameters**:
- `paperId` (string): Paper ID
- `limit` (number): Maximum results (default: 5)

**Returns**:
- `Array<Object>`: Related papers with scores

**Example**:
```javascript
const related = interactions.findRelatedPapers('paper123', 3);
// Returns: [{id: 'paper456', title: '...', score: 0.8}, ...]
```

### GraphFilters

**Location**: `visualization/js/filters.js`

**Purpose**: Implements filtering and search functionality.

#### Class Definition

```javascript
class GraphFilters {
    constructor(graph, data)
    init()
    applyFilters()
    reset()
    updateStats(visibleNodes)
}
```

#### Properties

```javascript
currentFilters = {
    search: '',
    year: null,
    relevancy: '',
    theme: '',
    nodeTypes: ['paper', 'author', 'tag']
}
```

#### Methods

##### applyFilters()

```javascript
applyFilters()
```

**Description**: Applies current filter state to graph.

**Example**:
```javascript
// After updating filters
filters.currentFilters.year = 2023;
filters.applyFilters();
```

##### reset()

```javascript
reset()
```

**Description**: Resets all filters to default state.

**Example**:
```javascript
document.getElementById('reset-filters').onclick = () => filters.reset();
```

## Data Format Reference

### Graph Data Format

```typescript
interface GraphData {
    nodes: Node[];
    links: Link[];
    stats: Statistics;
    metadata: Metadata;
}

interface Node {
    id: string;
    index: number;
    node_type: 'paper' | 'author' | 'tag' | 'year';
    // Type-specific properties
    [key: string]: any;
}

interface Link {
    source: number;  // Node index
    target: number;  // Node index
    source_id: string;
    target_id: string;
    edge_type: string;
    weight: number;
}
```

### Theme Data Format

```typescript
interface ThemeData {
    themes: Theme[];
    temporal_trends: TemporalTrends;
    communities: Communities;
    statistics: ThemeStatistics;
}

interface Theme {
    id: number;
    name: string;
    keywords: string[];
    paper_count: number;
    years_active: number[];
    peak_year: number | null;
    communities: Record<string, number>;
    example_papers: string[];
}
```

## Utility Functions

### Python Utilities

```python
# Clean text for processing
def clean_text(text: str) -> str:
    """Remove special characters and normalize text"""
    if pd.isna(text):
        return ""
    text = re.sub(r'[^\w\s]', ' ', str(text))
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()

# Calculate Jaccard similarity
def jaccard_similarity(set1: Set, set2: Set) -> float:
    """Calculate Jaccard similarity between two sets"""
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0

# Generate cite key
def generate_cite_key(authors: str, year: int) -> str:
    """Generate cite key from authors and year"""
    first_author = authors.split(',')[0].strip()
    last_name = first_author.split()[-1].lower()
    return f"{last_name}_{year}"
```

### JavaScript Utilities

```javascript
// Throttle function calls
function throttle(func, delay) {
    let lastCall = 0;
    return function(...args) {
        const now = new Date().getTime();
        if (now - lastCall < delay) return;
        lastCall = now;
        return func(...args);
    };
}

// Deep clone object
function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}

// Format large numbers
function formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
}

// Calculate node importance
function calculateImportance(node, links) {
    const connections = links.filter(l => 
        l.source === node.index || l.target === node.index
    );
    return connections.reduce((sum, link) => sum + link.weight, 0);
}
```

## Error Handling

### Python Error Handling

```python
class GraphBuilderError(Exception):
    """Custom exception for graph building errors"""
    pass

def safe_build_graph(csv_path):
    """Build graph with comprehensive error handling"""
    try:
        builder = HDMKnowledgeGraphBuilder(csv_path)
        return builder.build_graph()
    except FileNotFoundError:
        raise GraphBuilderError(f"CSV file not found: {csv_path}")
    except pd.errors.ParserError as e:
        raise GraphBuilderError(f"CSV parsing error: {e}")
    except Exception as e:
        raise GraphBuilderError(f"Unexpected error: {e}")
```

### JavaScript Error Handling

```javascript
// Wrap async operations
async function safeLoadData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Data loading error:', error);
        showErrorMessage('Failed to load visualization data');
        return null;
    }
}

// Global error handler
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    // Log to analytics if available
});
```

## Performance Considerations

### Python Performance

```python
# Use NumPy for vectorized operations
import numpy as np

def fast_cosine_similarity(matrix1, matrix2):
    """Optimized cosine similarity using NumPy"""
    dot_product = np.dot(matrix1, matrix2.T)
    norm1 = np.linalg.norm(matrix1, axis=1)
    norm2 = np.linalg.norm(matrix2, axis=1)
    return dot_product / (norm1[:, np.newaxis] * norm2)

# Use generators for memory efficiency
def process_large_dataset(csv_path, chunk_size=1000):
    """Process large CSV in chunks"""
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
        yield process_chunk(chunk)
```

### JavaScript Performance

```javascript
// Use requestAnimationFrame for smooth animations
let animationId;
function animate() {
    // Update positions
    simulation.tick();
    
    // Render changes
    updateNodePositions();
    
    // Continue animation
    animationId = requestAnimationFrame(animate);
}

// Debounce search input
const debouncedSearch = debounce((searchTerm) => {
    filters.currentFilters.search = searchTerm;
    filters.applyFilters();
}, 300);

// Virtual scrolling for large lists
class VirtualList {
    constructor(container, items, itemHeight) {
        this.container = container;
        this.items = items;
        this.itemHeight = itemHeight;
        this.render();
    }
    
    render() {
        const scrollTop = this.container.scrollTop;
        const startIndex = Math.floor(scrollTop / this.itemHeight);
        const endIndex = Math.min(
            startIndex + Math.ceil(this.container.clientHeight / this.itemHeight),
            this.items.length
        );
        
        // Render only visible items
        this.renderItems(startIndex, endIndex);
    }
}
```

---

**Document Control**  
- **Author**: HDM Development Team  
- **Review Cycle**: Quarterly  
- **Next Review**: April 2025  
- **Distribution**: Public