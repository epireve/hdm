# HDM Knowledge Graph User Guide

**Version**: 1.0.0  
**Last Updated**: January 2025  
**For**: End Users and Researchers

## Table of Contents

1. [Getting Started](#getting-started)
2. [Interface Overview](#interface-overview)
3. [Navigation & Controls](#navigation--controls)
4. [Search & Filter Features](#search--filter-features)
5. [Understanding the Visualization](#understanding-the-visualization)
6. [Common Use Cases](#common-use-cases)
7. [Tips & Tricks](#tips--tricks)
8. [Frequently Asked Questions](#frequently-asked-questions)

---

## Getting Started

### 🚀 Quick Start Guide

1. **Launch the Visualization**
   ```bash
   python launch_visualization.py
   ```
   Your browser will automatically open to `http://localhost:8080`

2. **Wait for Loading**
   - The graph will load in 2-3 seconds
   - You'll see nodes appear and arrange themselves
   - The force simulation will stabilize after ~5 seconds

3. **Start Exploring**
   - Click any node to see details
   - Drag nodes to rearrange
   - Use mouse wheel to zoom
   - Type in search box to find papers

### 🎯 First-Time User Checklist

- [ ] Click on a blue node (paper) to see its details
- [ ] Try searching for a keyword like "knowledge"
- [ ] Filter by year using the dropdown
- [ ] Zoom in/out with your mouse wheel
- [ ] Drag the background to pan around
- [ ] Press 'L' to toggle labels
- [ ] Click an author node (green) to see their papers

## Interface Overview

### 🖼️ Main Components

```
┌─────────────────────────────────────────────────────────┐
│                    Header (Stats)                        │
├─────────────────────────────────────────────────────────┤
│                    Controls Bar                          │
│  [Search Box] [Year ▼] [Relevancy ▼] [Theme ▼] [✓□□□]  │
├───────────────────────┬─────────────────────────────────┤
│                       │                                 │
│                       │          Details Panel         │
│    Graph Canvas       │                                 │
│                       │    (Paper/Author/Tag Info)     │
│                       │                                 │
│  [Legend]             │                                 │
└───────────────────────┴─────────────────────────────────┘
```

### 📊 Header Statistics

- **Papers**: Total number of research papers
- **Authors**: Unique authors in the dataset
- **Themes**: Identified research themes

### 🎛️ Control Bar Elements

1. **Search Box**: Find papers, authors, or keywords
2. **Year Filter**: Show papers from specific year
3. **Relevancy Filter**: Filter by High/Medium/Low
4. **Theme Filter**: Focus on research themes
5. **Node Type Toggles**: Show/hide different node types

### 🎨 Node Types and Colors

| Color | Type | Description |
|-------|------|-------------|
| 🔵 Blue | Paper | Research papers with metadata |
| 🟢 Green | Author | Paper authors |
| 🟡 Orange | Tag | Keywords and topics |
| 🟣 Purple | Year | Publication years |

## Navigation & Controls

### 🖱️ Mouse Controls

| Action | Effect |
|--------|--------|
| **Click node** | View details in side panel |
| **Drag node** | Reposition node |
| **Drag background** | Pan the view |
| **Scroll wheel** | Zoom in/out |
| **Hover node** | See tooltip |
| **Double-click background** | Center view |

### ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `L` | Toggle node labels |
| `R` | Reset zoom to default |
| `Escape` | Clear filters and selection |
| `Ctrl/Cmd + F` | Focus search box |
| `Space` | Pause/resume animation |
| `+/-` | Zoom in/out |

### 🎯 Selection and Highlighting

When you click a node:
1. The node is highlighted with a red border
2. Connected nodes remain visible
3. Unconnected nodes fade out
4. Details appear in the right panel

## Search & Filter Features

### 🔍 Search Functionality

**What You Can Search**:
- Paper titles
- Author names
- Keywords/tags
- Paper summaries (TL;DR)
- Insights text

**Search Tips**:
- Case-insensitive
- Partial matches work
- No special operators needed
- Results highlight in real-time

**Example Searches**:
- `knowledge graph` - Find papers about knowledge graphs
- `Smith` - Find papers by authors named Smith
- `2023` - Find papers from 2023
- `machine learning` - Find ML-related papers

### 🎚️ Filtering Options

#### Year Filter
- Select specific publication year
- Shows papers and their connections
- Other nodes fade but remain visible

#### Relevancy Filter
- **High**: Core papers for HDM project
- **Medium**: Related but not central
- **Low**: Peripheral interest

#### Theme Filter
- Shows papers belonging to selected theme
- Themes identified by machine learning
- Each theme has characteristic keywords

#### Node Type Toggles
- **Papers**: Show/hide paper nodes
- **Authors**: Show/hide author nodes
- **Tags**: Show/hide tag nodes
- **Years**: Show/hide year nodes

### 🔗 Combining Filters

Filters work together:
1. Search for "temporal"
2. Filter by year 2023
3. Show only High relevancy
→ Results: High-relevancy 2023 papers about temporal topics

## Understanding the Visualization

### 📐 Graph Layout

**Force-Directed Layout**:
- Nodes repel each other
- Connected nodes attract
- Creates natural clusters
- Reveals hidden patterns

**Visual Encodings**:
- **Node Size**: Importance (papers), paper count (authors/tags)
- **Link Thickness**: Relationship strength
- **Node Color**: Entity type
- **Position**: Emerges from relationships

### 🔗 Relationship Types

1. **Paper → Author** (Authorship)
   - Shows who wrote the paper
   - Multiple authors possible

2. **Paper → Tag** (Topics)
   - Keywords and subjects
   - Multiple tags per paper

3. **Paper → Year** (Publication)
   - When published
   - One year per paper

4. **Paper ↔ Paper** (Similarity)
   - Content similarity
   - Shared tags/authors
   - Temporal proximity

### 📊 Reading the Details Panel

**For Papers**:
- Full title and year
- Relevancy assessment
- TL;DR summary
- Key insights
- Full abstract
- Links to source

**For Authors**:
- Total paper count
- List of papers
- Collaboration network
- Click papers to navigate

**For Tags**:
- Papers with this tag
- Tag frequency
- Related tags
- Research themes

## Common Use Cases

### 📚 Use Case 1: Literature Review

**Goal**: Find key papers on a specific topic

1. Search for your topic (e.g., "PKG")
2. Click the most connected papers
3. Read summaries in details panel
4. Follow author links to find more
5. Export list of relevant papers

**Pro Tip**: Look for papers with many connections - they're often influential

### 🔬 Use Case 2: Research Gap Analysis

**Goal**: Identify under-researched areas

1. Select a theme filter
2. Look for sparse areas in the graph
3. Check year distribution
4. Note topics with few recent papers
5. Cross-reference with high-relevancy papers

**Pro Tip**: Isolated clusters often indicate niche topics

### 👥 Use Case 3: Finding Collaborators

**Goal**: Identify potential research partners

1. Find papers in your area
2. Click on author nodes
3. See their other papers
4. Look for complementary expertise
5. Note frequent collaborators

**Pro Tip**: Authors bridging different clusters often have diverse expertise

### 📈 Use Case 4: Tracking Research Trends

**Goal**: Understand topic evolution over time

1. Select a tag or theme
2. Filter by year sequentially
3. Observe how clusters change
4. Note emerging connections
5. Identify growing topics

**Pro Tip**: New connections between previously separate clusters indicate convergence

### 🎯 Use Case 5: Paper Discovery

**Goal**: Find papers you didn't know about

1. Start with a known paper
2. Click to see details
3. Explore connected papers
4. Follow similarity links
5. Check author's other work

**Pro Tip**: Papers 2-3 hops away often contain surprising connections

## Tips & Tricks

### 💡 Power User Tips

1. **Rapid Exploration**
   - Hold Shift while clicking to open multiple details
   - Use Tab to cycle through recent selections
   - Middle-click to open paper links in new tabs

2. **Visual Optimization**
   - Toggle labels (L) for cleaner view
   - Adjust zoom for different perspectives
   - Drag important nodes to center

3. **Efficient Filtering**
   - Start broad, then narrow
   - Use search to highlight, not hide
   - Remember filter combinations

4. **Pattern Recognition**
   - Dense clusters = hot topics
   - Bridge nodes = interdisciplinary
   - Isolated nodes = unique research

### 🎨 Visual Interpretation Guide

**Cluster Patterns**:
- **Tight Cluster**: Strong thematic coherence
- **Loose Cluster**: Related but diverse
- **Star Pattern**: Central influential paper
- **Chain Pattern**: Sequential development
- **Island**: Disconnected research area

**Node Patterns**:
- **Large Blue Node**: Important paper
- **Green Hub**: Prolific author
- **Orange Cloud**: Popular tags
- **Connected Years**: Research continuity

### ⚡ Performance Tips

**For Smooth Interaction**:
1. Hide year nodes if not needed
2. Limit visible nodes with filters
3. Close other browser tabs
4. Let simulation settle before interacting
5. Refresh if performance degrades

## Frequently Asked Questions

### ❓ General Questions

**Q: How do I save my current view?**
A: Use the "Export SVG" button to save the current visualization as an image.

**Q: Can I download the data?**
A: The processed data is available in the `visualization/data/` folder as JSON files.

**Q: Why are some nodes moving?**
A: The force simulation continues to optimize positions. Press Space to pause.

**Q: How are themes identified?**
A: Using machine learning (LDA topic modeling) on paper abstracts and summaries.

### 🔧 Troubleshooting

**Q: The graph won't load**
A: Check that the server is running and refresh the page. Look for errors in browser console.

**Q: Nodes are overlapping**
A: Let the simulation run longer, or manually drag nodes apart.

**Q: Search isn't working**
A: Ensure you're using complete words. Partial matching is limited.

**Q: Performance is slow**
A: Try hiding some node types or filtering to show fewer nodes.

### 📊 Data Questions

**Q: How recent is the data?**
A: Check the statistics panel for the date range of papers.

**Q: What does "relevancy" mean?**
A: Papers are rated High/Medium/Low based on their importance to the HDM project.

**Q: Can I add my own papers?**
A: Edit the CSV file and rerun the processing script.

**Q: What are the similarity metrics?**
A: Combined score from tags, content, temporal proximity, and authors.

### 🎯 Usage Questions

**Q: How do I find papers by a specific author?**
A: Type the author's name in the search box or click on their green node.

**Q: Can I see only papers from 2024?**
A: Yes, use the year filter dropdown.

**Q: How do I export a list of papers?**
A: Currently, you need to manually note them or access the JSON data files.

**Q: Can multiple people use this?**
A: Yes, but each person needs their own browser session.

### 🚀 Advanced Questions

**Q: Can I customize the colors?**
A: Edit the color configuration in `js/graph.js`.

**Q: How do I add new relationship types?**
A: This requires modifying the Python processing scripts.

**Q: Can I integrate this with Zotero?**
A: Not directly, but you can export/import via CSV.

**Q: Is there an API?**
A: No, but the JSON files can be accessed programmatically.

---

## 📞 Getting Help

### Resources
- **Documentation**: See other guides in `docs/knowledge_graph/`
- **GitHub Issues**: Report bugs or request features
- **Data Files**: Check `visualization/data/` for raw data

### Quick Troubleshooting Checklist
1. ✓ Is the server running?
2. ✓ Using a modern browser?
3. ✓ Cleared browser cache?
4. ✓ Checked browser console?
5. ✓ Data files exist?

### Contact
For additional help, please:
1. Check existing documentation
2. Search closed GitHub issues
3. Create a new issue with details
4. Include browser and OS info

---

**Happy Exploring! 🎉**

Remember: The best way to learn is by clicking around and discovering connections you didn't expect!