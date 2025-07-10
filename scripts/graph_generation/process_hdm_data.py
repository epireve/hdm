"""
Main script to process CSV and generate visualization data
"""

import pandas as pd
import json
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph_generation.graph_builder import HDMKnowledgeGraphBuilder
from graph_generation.relationship_extractor import RelationshipExtractor
from graph_generation.theme_clusterer import ThemeClusterer


def main():
    """Process HDM research papers and generate knowledge graph visualization data."""
    
    # Define paths
    base_dir = Path(__file__).parent.parent.parent
    
    # Look for the latest hdm_research_papers file
    csv_files = list(base_dir.glob('hdm_research_papers_merged_*.csv'))
    if not csv_files:
        # Fall back to complete version if merged doesn't exist
        csv_files = list(base_dir.glob('hdm_research_papers_complete_*.csv'))
    
    if csv_files:
        # Use the most recent file
        csv_path = sorted(csv_files)[-1]
    else:
        # Legacy filename fallback
        csv_path = base_dir / 'research_papers_complete.csv'
    
    output_dir = base_dir / 'visualization' / 'data'
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("HDM Knowledge Graph Generation")
    print("=" * 80)
    
    # 1. Load CSV data
    print(f"\n1. Loading data from {csv_path}")
    try:
        df = pd.read_csv(csv_path, quoting=1, on_bad_lines='skip')
        print(f"   Loaded {len(df)} papers")
    except FileNotFoundError:
        print(f"Error: Could not find {csv_path}")
        print("Please ensure one of these files exists in the project root:")
        print("  - hdm_research_papers_merged_YYYYMMDD.csv (preferred)")
        print("  - hdm_research_papers_complete_YYYYMMDD.csv")
        return
    
    # 2. Build knowledge graph
    print("\n2. Building knowledge graph...")
    builder = HDMKnowledgeGraphBuilder(csv_path)
    graph = builder.build_graph()
    
    # 3. Extract relationships
    print("\n3. Extracting relationships between papers...")
    extractor = RelationshipExtractor(df)
    similarity_matrix = extractor.generate_similarity_matrix()
    
    # Add paper relationships to graph
    builder.add_paper_relationships(similarity_matrix, threshold=0.3)
    
    # 4. Identify themes
    print("\n4. Identifying research themes...")
    try:
        clusterer = ThemeClusterer(graph, df)
        communities = clusterer.detect_communities()
        themes = clusterer.identify_research_themes(n_topics=8)
        temporal_trends = clusterer.analyze_temporal_trends()
    except ImportError:
        print("Warning: python-louvain not installed. Skipping community detection.")
        print("Install with: pip install python-louvain")
        clusterer = None
        communities = {}
        themes = {}
        temporal_trends = {}
    
    # 5. Generate visualization data
    print("\n5. Generating visualization data...")
    
    # Export main graph data
    graph_data = builder.export_to_json(str(output_dir / 'graph_data.json'))
    
    # Export similarity data
    extractor.export_similarity_matrix(str(output_dir / 'similarities.json'))
    
    # Export theme data
    if clusterer:
        clusterer.export_themes(str(output_dir / 'themes.json'))
    
    # Generate additional statistics
    stats = generate_detailed_statistics(df, graph, communities, themes)
    with open(output_dir / 'statistics.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    # Export GEXF for Gephi (optional)
    try:
        builder.export_to_gexf(str(output_dir / 'hdm_graph.gexf'))
    except Exception as e:
        print(f"Warning: Could not export GEXF file: {e}")
    
    # 6. Create index file for easy access
    create_index_file(output_dir, graph_data, themes)
    
    print("\n" + "=" * 80)
    print("✅ Knowledge graph generation complete!")
    print(f"📁 Output files saved to: {output_dir}")
    print("\nGenerated files:")
    print("  - graph_data.json: Main graph data for D3.js visualization")
    print("  - similarities.json: Paper similarity relationships")
    print("  - themes.json: Identified research themes and communities")
    print("  - statistics.json: Detailed graph statistics")
    print("  - hdm_graph.gexf: Graph file for Gephi")
    print("  - index.json: Quick access index")
    print("=" * 80)


def generate_detailed_statistics(df, graph, communities, themes):
    """Generate detailed statistics about the knowledge graph."""
    
    # Basic counts
    node_types = {}
    for node, data in graph.nodes(data=True):
        node_type = data.get('node_type', 'unknown')
        node_types[node_type] = node_types.get(node_type, 0) + 1
    
    # Year distribution
    year_dist = df['year'].value_counts().to_dict() if 'year' in df else {}
    
    # Relevancy distribution
    relevancy_dist = df['Relevancy'].value_counts().to_dict() if 'Relevancy' in df else {}
    
    # Top tags
    all_tags = []
    for tags_str in df['Tags'].dropna():
        tags = [t.strip() for t in str(tags_str).strip('"').split(',') if t.strip()]
        all_tags.extend(tags)
    
    from collections import Counter
    tag_counts = Counter(all_tags)
    top_tags = dict(tag_counts.most_common(20))
    
    # Author statistics
    all_authors = []
    for authors_str in df['authors'].dropna():
        authors = [a.strip() for a in str(authors_str).strip('"').split(',') 
                  if a.strip() and a.strip().lower() not in ['unavailable', 'unknown']]
        all_authors.extend(authors)
    
    author_counts = Counter(all_authors)
    top_authors = dict(author_counts.most_common(10))
    
    # Network statistics
    import networkx as nx
    paper_nodes = [n for n, d in graph.nodes(data=True) if d.get('node_type') == 'paper']
    paper_subgraph = graph.subgraph(paper_nodes)
    
    stats = {
        'overview': {
            'total_papers': len(df),
            'total_nodes': graph.number_of_nodes(),
            'total_edges': graph.number_of_edges(),
            'node_types': node_types
        },
        'temporal': {
            'year_distribution': {str(k): v for k, v in sorted(year_dist.items())},
            'year_range': [int(df['year'].min()), int(df['year'].max())] if 'year' in df else None
        },
        'content': {
            'relevancy_distribution': relevancy_dist,
            'top_tags': top_tags,
            'total_unique_tags': len(tag_counts)
        },
        'authors': {
            'total_unique_authors': len(author_counts),
            'top_authors': top_authors,
            'avg_authors_per_paper': round(len(all_authors) / len(df), 2)
        },
        'network_metrics': {
            'avg_degree': round(sum(dict(graph.degree()).values()) / graph.number_of_nodes(), 2),
            'density': round(nx.density(graph), 4),
            'communities': len(set(communities.values())) if communities else 0,
            'themes': len(themes) if themes else 0
        }
    }
    
    return stats


def create_index_file(output_dir, graph_data, themes):
    """Create an index file for quick lookups."""
    
    # Create paper lookup
    paper_index = {}
    for node in graph_data['nodes']:
        if node.get('node_type') == 'paper':
            paper_index[node['id']] = {
                'title': node.get('title', ''),
                'year': node.get('year', ''),
                'relevancy': node.get('relevancy', ''),
                'node_index': node['index']
            }
    
    # Create author lookup
    author_index = {}
    for node in graph_data['nodes']:
        if node.get('node_type') == 'author':
            author_index[node['id']] = {
                'papers': node.get('papers', []),
                'node_index': node['index']
            }
    
    # Create theme lookup
    theme_index = {}
    for theme_id, theme_data in themes.items():
        theme_index[str(theme_id)] = {
            'name': theme_data['name'],
            'keywords': theme_data['words'][:5],
            'paper_count': theme_data['paper_count']
        }
    
    index_data = {
        'papers': paper_index,
        'authors': author_index,
        'themes': theme_index,
        'metadata': {
            'total_papers': len(paper_index),
            'total_authors': len(author_index),
            'total_themes': len(theme_index)
        }
    }
    
    with open(output_dir / 'index.json', 'w') as f:
        json.dump(index_data, f, indent=2)


if __name__ == "__main__":
    main()