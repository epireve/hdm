"""
Build knowledge graph from research_papers_complete.csv
- Extract entities (papers, authors, tags, years)
- Create relationships between entities
- Calculate graph metrics
- Export to multiple formats
"""

import pandas as pd
import networkx as nx
import json
from collections import defaultdict
import re
from typing import Dict, List, Tuple, Any
import numpy as np


class HDMKnowledgeGraphBuilder:
    def __init__(self, csv_path: str):
        """Initialize the knowledge graph builder with research papers data."""
        # Read CSV with better handling of quoted fields
        self.df = pd.read_csv(csv_path, quoting=1, on_bad_lines='skip')
        self.graph = nx.Graph()
        self.stats = {}
        self.node_types = defaultdict(list)
        
    def clean_authors(self, authors_str: str) -> List[str]:
        """Clean and split author names."""
        if pd.isna(authors_str):
            return []
        # Remove quotes and split by comma
        authors_str = str(authors_str).strip('"')
        authors = [a.strip() for a in authors_str.split(',')]
        return [a for a in authors if a and a.lower() not in ['unavailable', 'unknown']]
    
    def clean_tags(self, tags_str: str) -> List[str]:
        """Clean and split tags."""
        if pd.isna(tags_str):
            return []
        # Remove quotes and split by comma
        tags_str = str(tags_str).strip('"')
        tags = [t.strip() for t in tags_str.split(',')]
        return [t for t in tags if t]
    
    def build_graph(self) -> nx.Graph:
        """Build the knowledge graph from the research papers data."""
        print(f"Building knowledge graph from {len(self.df)} papers...")
        
        # Add paper nodes
        for idx, row in self.df.iterrows():
            paper_id = row['cite_key']
            
            # Add paper node with attributes
            self.graph.add_node(paper_id, 
                node_type='paper',
                title=row['title'],
                year=int(row['year']) if pd.notna(row['year']) else None,
                relevancy=row['Relevancy'],
                tldr=row['TL;DR'],
                summary=row['Summary'],
                insights=row['Insights'],
                url=row['url'],
                doi=row['DOI']
            )
            self.node_types['paper'].append(paper_id)
            
            # Add author nodes and relationships
            authors = self.clean_authors(row['authors'])
            for author in authors:
                if author not in self.graph:
                    self.graph.add_node(author, 
                        node_type='author',
                        papers=[]
                    )
                    self.node_types['author'].append(author)
                
                # Update author's paper list
                self.graph.nodes[author]['papers'].append(paper_id)
                
                # Add authored_by edge
                self.graph.add_edge(paper_id, author, 
                    edge_type='authored_by',
                    weight=1.0
                )
            
            # Add year node
            if pd.notna(row['year']):
                year = int(row['year'])
                year_node = f"year_{year}"
                if year_node not in self.graph:
                    self.graph.add_node(year_node,
                        node_type='year',
                        value=year
                    )
                    self.node_types['year'].append(year_node)
                
                self.graph.add_edge(paper_id, year_node,
                    edge_type='published_in',
                    weight=1.0
                )
            
            # Add tag nodes and relationships
            tags = self.clean_tags(row['Tags'])
            for tag in tags:
                tag_node = f"tag_{tag}"
                if tag_node not in self.graph:
                    self.graph.add_node(tag_node,
                        node_type='tag',
                        name=tag,
                        papers=[]
                    )
                    self.node_types['tag'].append(tag_node)
                
                # Update tag's paper list
                self.graph.nodes[tag_node]['papers'].append(paper_id)
                
                # Add tagged_with edge
                self.graph.add_edge(paper_id, tag_node,
                    edge_type='tagged_with',
                    weight=1.0
                )
        
        # Calculate statistics
        self._calculate_statistics()
        
        print(f"Graph built with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges")
        return self.graph
    
    def _calculate_statistics(self):
        """Calculate graph statistics and metrics."""
        self.stats = {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'papers': len(self.node_types['paper']),
            'authors': len(self.node_types['author']),
            'tags': len(self.node_types['tag']),
            'years': len(self.node_types['year']),
            'avg_degree': np.mean([d for n, d in self.graph.degree()]),
            'density': nx.density(self.graph)
        }
        
        # Calculate centrality for papers
        paper_subgraph = self.graph.subgraph(self.node_types['paper'])
        if paper_subgraph.number_of_nodes() > 0:
            # Degree centrality
            degree_centrality = nx.degree_centrality(self.graph)
            for node, centrality in degree_centrality.items():
                self.graph.nodes[node]['degree_centrality'] = centrality
            
            # Calculate paper importance based on connections
            for paper in self.node_types['paper']:
                connections = len(list(self.graph.neighbors(paper)))
                self.graph.nodes[paper]['importance'] = connections / max(1, self.stats['avg_degree'])
    
    def add_paper_relationships(self, similarity_matrix: Dict[Tuple[str, str], float], threshold: float = 0.3):
        """Add edges between similar papers based on similarity scores."""
        added_edges = 0
        for (paper1, paper2), similarity in similarity_matrix.items():
            if similarity >= threshold and paper1 in self.graph and paper2 in self.graph:
                self.graph.add_edge(paper1, paper2,
                    edge_type='similar_to',
                    weight=similarity
                )
                added_edges += 1
        
        print(f"Added {added_edges} similarity edges between papers")
    
    def export_to_json(self, output_path: str):
        """Export graph to D3.js compatible JSON format."""
        # Prepare nodes data
        nodes = []
        node_to_idx = {}
        
        for idx, (node_id, data) in enumerate(self.graph.nodes(data=True)):
            node_to_idx[node_id] = idx
            
            node_data = {
                'id': node_id,
                'index': idx,
                **data
            }
            
            # Add additional computed properties
            if data.get('node_type') == 'paper':
                node_data['size'] = 10 + data.get('importance', 1) * 20
            elif data.get('node_type') == 'author':
                node_data['size'] = 5 + len(data.get('papers', [])) * 2
            elif data.get('node_type') == 'tag':
                node_data['size'] = 3 + len(data.get('papers', [])) * 1
            else:
                node_data['size'] = 5
            
            nodes.append(node_data)
        
        # Prepare links data
        links = []
        for source, target, data in self.graph.edges(data=True):
            links.append({
                'source': node_to_idx[source],
                'target': node_to_idx[target],
                'source_id': source,
                'target_id': target,
                **data
            })
        
        # Create final JSON structure
        graph_data = {
            'nodes': nodes,
            'links': links,
            'stats': self.stats,
            'metadata': {
                'total_papers': len(self.df),
                'date_created': pd.Timestamp.now().isoformat(),
                'version': '1.0'
            }
        }
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
        print(f"Graph exported to {output_path}")
        return graph_data
    
    def export_to_gexf(self, output_path: str):
        """Export graph to GEXF format for Gephi."""
        nx.write_gexf(self.graph, output_path)
        print(f"Graph exported to {output_path} in GEXF format")
    
    def get_subgraph_by_year(self, start_year: int, end_year: int) -> nx.Graph:
        """Get subgraph containing papers from specific year range."""
        papers_in_range = []
        for paper in self.node_types['paper']:
            year = self.graph.nodes[paper].get('year')
            if year and start_year <= year <= end_year:
                papers_in_range.append(paper)
        
        # Get all nodes connected to these papers
        nodes_to_include = set(papers_in_range)
        for paper in papers_in_range:
            nodes_to_include.update(self.graph.neighbors(paper))
        
        return self.graph.subgraph(nodes_to_include)
    
    def get_author_collaboration_network(self) -> nx.Graph:
        """Create a graph showing author collaborations."""
        collab_graph = nx.Graph()
        
        # Add all authors
        for author in self.node_types['author']:
            papers = self.graph.nodes[author].get('papers', [])
            collab_graph.add_node(author, papers_count=len(papers))
        
        # Add edges between co-authors
        for paper in self.node_types['paper']:
            authors = [n for n in self.graph.neighbors(paper) 
                      if self.graph.nodes[n].get('node_type') == 'author']
            
            # Create edges between all pairs of authors on this paper
            for i, author1 in enumerate(authors):
                for author2 in authors[i+1:]:
                    if collab_graph.has_edge(author1, author2):
                        collab_graph[author1][author2]['weight'] += 1
                        collab_graph[author1][author2]['papers'].append(paper)
                    else:
                        collab_graph.add_edge(author1, author2, weight=1, papers=[paper])
        
        return collab_graph