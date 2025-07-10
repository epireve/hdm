"""
Identify research themes through clustering
- Community detection
- Topic modeling
- Trend analysis
"""

import pandas as pd
import numpy as np
import networkx as nx
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Any
import community as community_louvain


class ThemeClusterer:
    def __init__(self, graph: nx.Graph, papers_df: pd.DataFrame):
        """Initialize with graph and papers dataframe."""
        self.graph = graph
        self.papers = papers_df
        self.communities = {}
        self.themes = {}
        self.temporal_trends = {}
        
    def detect_communities(self) -> Dict[str, int]:
        """Detect communities using Louvain algorithm."""
        print("Detecting communities in the graph...")
        
        # Create a subgraph with only papers and their relationships
        paper_nodes = [n for n, d in self.graph.nodes(data=True) 
                      if d.get('node_type') == 'paper']
        
        # Create paper-to-paper graph based on shared attributes
        paper_graph = nx.Graph()
        paper_graph.add_nodes_from(paper_nodes)
        
        # Add edges between papers that share tags or authors
        for paper1 in paper_nodes:
            for paper2 in paper_nodes:
                if paper1 >= paper2:  # Avoid duplicates
                    continue
                
                # Check for shared tags
                paper1_tags = set(n for n in self.graph.neighbors(paper1) 
                                 if self.graph.nodes[n].get('node_type') == 'tag')
                paper2_tags = set(n for n in self.graph.neighbors(paper2) 
                                 if self.graph.nodes[n].get('node_type') == 'tag')
                
                shared_tags = len(paper1_tags & paper2_tags)
                
                # Check for shared authors
                paper1_authors = set(n for n in self.graph.neighbors(paper1) 
                                    if self.graph.nodes[n].get('node_type') == 'author')
                paper2_authors = set(n for n in self.graph.neighbors(paper2) 
                                    if self.graph.nodes[n].get('node_type') == 'author')
                
                shared_authors = len(paper1_authors & paper2_authors)
                
                # Add edge if papers share attributes
                weight = shared_tags + (shared_authors * 2)  # Authors weighted more
                if weight > 0:
                    paper_graph.add_edge(paper1, paper2, weight=weight)
        
        # Apply Louvain community detection
        if paper_graph.number_of_edges() > 0:
            self.communities = community_louvain.best_partition(paper_graph)
            
            # Count papers per community
            community_counts = Counter(self.communities.values())
            print(f"Found {len(community_counts)} communities")
            for comm_id, count in community_counts.most_common():
                print(f"  Community {comm_id}: {count} papers")
        else:
            print("No edges in paper graph, cannot detect communities")
            self.communities = {paper: 0 for paper in paper_nodes}
        
        return self.communities
    
    def identify_research_themes(self, n_topics: int = 10, top_words: int = 10) -> Dict[int, Dict[str, Any]]:
        """Identify research themes using LDA topic modeling."""
        print(f"Identifying {n_topics} research themes using topic modeling...")
        
        # Prepare documents
        documents = []
        paper_ids = []
        
        for idx, row in self.papers.iterrows():
            # Combine relevant text fields
            text_parts = []
            for field in ['Summary', 'TL;DR', 'Insights', 'Research Question', 'Tags']:
                if pd.notna(row[field]):
                    text_parts.append(str(row[field]))
            
            combined_text = ' '.join(text_parts)
            if combined_text:
                documents.append(combined_text)
                paper_ids.append(row['cite_key'])
        
        if len(documents) < n_topics:
            n_topics = max(2, len(documents) // 2)
            print(f"Reduced topics to {n_topics} due to limited documents")
        
        # Vectorize documents
        vectorizer = CountVectorizer(
            max_features=500,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
        
        doc_term_matrix = vectorizer.fit_transform(documents)
        feature_names = vectorizer.get_feature_names_out()
        
        # Apply LDA
        lda = LatentDirichletAllocation(
            n_components=n_topics,
            random_state=42,
            max_iter=100
        )
        
        doc_topics = lda.fit_transform(doc_term_matrix)
        
        # Extract themes
        self.themes = {}
        for topic_idx in range(n_topics):
            # Get top words for this topic
            top_indices = lda.components_[topic_idx].argsort()[-top_words:][::-1]
            top_words_list = [feature_names[i] for i in top_indices]
            
            # Find papers most associated with this topic
            paper_scores = [(paper_ids[i], doc_topics[i, topic_idx]) 
                           for i in range(len(paper_ids))]
            paper_scores.sort(key=lambda x: x[1], reverse=True)
            top_papers = [p[0] for p in paper_scores[:5]]
            
            # Generate theme name from top words
            theme_name = '_'.join(top_words_list[:3])
            
            self.themes[topic_idx] = {
                'name': theme_name,
                'words': top_words_list,
                'top_papers': top_papers,
                'paper_count': sum(1 for score in doc_topics[:, topic_idx] if score > 0.1)
            }
            
            # Assign theme to papers in graph
            for i, paper_id in enumerate(paper_ids):
                if doc_topics[i, topic_idx] > 0.1 and paper_id in self.graph:
                    if 'themes' not in self.graph.nodes[paper_id]:
                        self.graph.nodes[paper_id]['themes'] = []
                    self.graph.nodes[paper_id]['themes'].append(topic_idx)
        
        print(f"Identified {len(self.themes)} themes")
        return self.themes
    
    def analyze_temporal_trends(self) -> Dict[int, Dict[int, int]]:
        """Analyze how themes evolve over time."""
        print("Analyzing temporal trends...")
        
        # Initialize trend data
        self.temporal_trends = defaultdict(lambda: defaultdict(int))
        
        # Count papers per theme per year
        for idx, row in self.papers.iterrows():
            if pd.notna(row['year']):
                year = int(row['year'])
                paper_id = row['cite_key']
                
                # Get themes for this paper
                if paper_id in self.graph and 'themes' in self.graph.nodes[paper_id]:
                    for theme_idx in self.graph.nodes[paper_id]['themes']:
                        self.temporal_trends[theme_idx][year] += 1
        
        # Convert to regular dict
        self.temporal_trends = {theme: dict(years) 
                               for theme, years in self.temporal_trends.items()}
        
        # Identify growing themes
        growing_themes = []
        for theme_idx, years in self.temporal_trends.items():
            if len(years) >= 3:  # Need at least 3 years of data
                years_sorted = sorted(years.items())
                recent_avg = np.mean([count for year, count in years_sorted[-2:]])
                early_avg = np.mean([count for year, count in years_sorted[:2]])
                
                if recent_avg > early_avg * 1.5:  # 50% growth
                    growing_themes.append({
                        'theme': theme_idx,
                        'name': self.themes[theme_idx]['name'],
                        'growth_rate': recent_avg / max(early_avg, 1)
                    })
        
        if growing_themes:
            print(f"Found {len(growing_themes)} growing themes:")
            for theme in sorted(growing_themes, key=lambda x: x['growth_rate'], reverse=True)[:5]:
                print(f"  {theme['name']}: {theme['growth_rate']:.1f}x growth")
        
        return self.temporal_trends
    
    def get_theme_summary(self) -> List[Dict[str, Any]]:
        """Get summary of all themes with statistics."""
        theme_summaries = []
        
        for theme_idx, theme_data in self.themes.items():
            # Get temporal data
            years_data = self.temporal_trends.get(theme_idx, {})
            
            # Get community distribution
            theme_communities = defaultdict(int)
            for paper in theme_data['top_papers']:
                if paper in self.communities:
                    theme_communities[self.communities[paper]] += 1
            
            summary = {
                'id': theme_idx,
                'name': theme_data['name'],
                'keywords': theme_data['words'][:5],
                'paper_count': theme_data['paper_count'],
                'years_active': list(years_data.keys()),
                'peak_year': max(years_data.items(), key=lambda x: x[1])[0] if years_data else None,
                'communities': dict(theme_communities),
                'example_papers': theme_data['top_papers'][:3]
            }
            
            theme_summaries.append(summary)
        
        # Sort by paper count
        theme_summaries.sort(key=lambda x: x['paper_count'], reverse=True)
        
        return theme_summaries
    
    def export_themes(self, output_path: str):
        """Export themes data to JSON."""
        import json
        
        theme_data = {
            'themes': self.get_theme_summary(),
            'temporal_trends': self.temporal_trends,
            'communities': {str(k): v for k, v in self.communities.items()},
            'statistics': {
                'total_themes': len(self.themes),
                'total_communities': len(set(self.communities.values())),
                'papers_with_themes': sum(1 for n, d in self.graph.nodes(data=True) 
                                         if d.get('node_type') == 'paper' and 'themes' in d)
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(theme_data, f, indent=2)
        
        print(f"Exported theme data to {output_path}")
    
    def get_theme_colors(self) -> Dict[int, str]:
        """Generate distinct colors for each theme."""
        # Use a color palette
        colors = [
            '#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00',
            '#ffff33', '#a65628', '#f781bf', '#999999', '#66c2a5',
            '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f'
        ]
        
        theme_colors = {}
        for i, theme_idx in enumerate(self.themes.keys()):
            theme_colors[theme_idx] = colors[i % len(colors)]
        
        return theme_colors