# HDM Research Knowledge Graph Visualization

An interactive knowledge graph visualization for Human Digital Memory (HDM) research papers, built with D3.js.

## Features

- **Interactive Force-Directed Graph**: Explore relationships between papers, authors, tags, and years
- **Multiple Node Types**: 
  - 🔵 Papers (blue) - Research papers with full metadata
  - 🟢 Authors (green) - Paper authors with collaboration networks
  - 🟡 Tags (orange) - Keywords and research topics
  - 🟣 Years (purple) - Temporal organization
- **Advanced Filtering**:
  - Search by title, author, or content
  - Filter by year, relevancy, or research theme
  - Toggle visibility of different node types
- **Rich Details Panel**: Click any node to see detailed information
- **Zoom & Pan**: Navigate large graphs easily
- **Export**: Save the visualization as SVG

## Usage

### Viewing the Visualization

1. **Start a local web server** in the visualization directory:
   ```bash
   cd visualization
   python -m http.server 8000
   # or
   npx http-server
   ```

2. **Open in browser**: Navigate to `http://localhost:8000`

### Interacting with the Graph

- **Click** on nodes to view details
- **Drag** nodes to reposition them
- **Scroll** to zoom in/out
- **Drag background** to pan

### Keyboard Shortcuts

- `Ctrl/Cmd + F`: Focus search box
- `L`: Toggle node labels
- `R`: Reset zoom
- `Escape`: Clear filters and selection

### Filtering Options

- **Search**: Find papers by title, content, or author names
- **Year**: Filter to specific publication year
- **Relevancy**: Show only High/Medium/Low relevancy papers
- **Theme**: Filter by identified research themes
- **Node Types**: Toggle visibility of papers, authors, tags, or years

## Data Generation

To regenerate the visualization data from updated CSV:

```bash
cd scripts/graph_generation
python process_hdm_data.py
```

This will update all JSON files in `visualization/data/`.

## File Structure

```
visualization/
├── index.html          # Main HTML file
├── css/
│   └── style.css      # Styling
├── js/
│   ├── graph.js       # D3.js graph implementation
│   ├── interactions.js # User interaction handlers
│   ├── filters.js     # Filtering logic
│   └── main.js        # Application entry point
└── data/
    ├── graph_data.json    # Main graph structure
    ├── themes.json        # Research themes
    ├── similarities.json  # Paper relationships
    ├── statistics.json    # Graph statistics
    └── index.json         # Quick lookup index
```

## Deployment to GitHub Pages

1. Ensure all files are committed to your repository
2. Go to Settings → Pages in your GitHub repository
3. Select source branch and `/visualization` folder
4. Your visualization will be available at:
   `https://[username].github.io/[repository]/`

## Customization

### Colors
Edit the color scheme in `js/graph.js`:
```javascript
this.colorScale = {
    'paper': '#4A90E2',
    'author': '#7ED321',
    'tag': '#F5A623',
    'year': '#BD10E0'
};
```

### Node Sizes
Adjust node sizing logic in `js/graph.js`:
```javascript
this.sizeScale = {
    'paper': d => 8 + Math.sqrt(d.importance || 1) * 5,
    'author': d => 6 + Math.sqrt(d.papers?.length || 1) * 2,
    // ...
};
```

### Force Simulation
Modify physics parameters in `createForceSimulation()` method.

## Performance Notes

- The visualization handles 300+ papers smoothly
- For larger graphs (1000+ nodes), consider:
  - Implementing node clustering
  - Using WebGL renderer
  - Progressive loading

## Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- Mobile: Basic support (touch events for pan/zoom)

## Troubleshooting

**Graph not loading?**
- Check browser console for errors
- Ensure all data files exist in `data/` directory
- Verify JSON files are valid

**Performance issues?**
- Try filtering to show fewer nodes
- Disable labels (press 'L')
- Use a modern browser

**Nodes overlapping?**
- Let the simulation run longer
- Drag nodes to better positions
- Adjust force parameters

## Future Enhancements

- [ ] Citation network visualization
- [ ] Time-based animation
- [ ] Advanced search with regex
- [ ] Collaborative filtering
- [ ] Export to other formats (GraphML, etc.)
- [ ] Integration with paper PDFs
- [ ] Real-time data updates

## Turso Database Integration

The `all-papers-direct.html` page provides direct access to all papers from the Turso database with advanced search, filtering, and sorting capabilities.

### Features

- **1,430+ papers** loaded directly from Turso database
- **Real-time search** across title, abstract, and authors
- **Advanced filtering** by year and open access status
- **Column sorting** - click any header to sort
- **Pagination** with configurable page sizes (50-1000 papers per page)
- **Statistics dashboard** showing total papers, open access count, and year range

### Local Setup

1. **Copy the configuration template**:
   ```bash
   cp js/config.template.js js/config.js
   ```

2. **Edit `js/config.js`** and add your Turso credentials:
   ```javascript
   window.TURSO_CONFIG = {
       DATABASE_URL: 'libsql://your-database.turso.io',
       AUTH_TOKEN: 'your-auth-token'
   };
   ```

3. **Access the page** at `http://localhost:8000/all-papers-direct.html`

Note: The `js/config.js` file is gitignored and won't be committed to the repository.

### GitHub Pages Deployment

For GitHub Pages deployment:

1. **Add repository secrets**:
   - `TURSO_DATABASE_URL`: Your Turso database URL
   - `TURSO_AUTH_TOKEN`: Your Turso authentication token

2. **Use the provided workflow**: The GitHub Actions workflow in `.github/workflows/deploy-pages-example.yml` will automatically inject these secrets during deployment.

3. **Manual configuration**: If not using Actions, you can still manually enter credentials through the UI.

### Security Notes

- Credentials are stored in browser localStorage after first use
- For production, use environment secrets rather than hardcoded values
- The auth token provides read-only access to the database