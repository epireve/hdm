"""
Extract and score relationships between papers
- Tag similarity
- Author overlap
- Temporal proximity
- Keyword extraction from summaries
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple, Set
import re
from collections import defaultdict


class RelationshipExtractor:
    def __init__(self, papers_df: pd.DataFrame):
        """Initialize with papers dataframe."""
        self.papers = papers_df
        self.similarity_matrix = {}
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        
    def clean_text(self, text: str) -> str:
        """Clean text for processing."""
        if pd.isna(text):
            return ""
        # Remove special characters and extra spaces
        text = re.sub(r'[^\w\s]', ' ', str(text))
        text = re.sub(r'\s+', ' ', text)
        return text.lower().strip()
    
    def get_tag_set(self, tags_str: str) -> Set[str]:
        """Convert tag string to set."""
        if pd.isna(tags_str):
            return set()
        tags = str(tags_str).strip('"').split(',')
        return {tag.strip().lower() for tag in tags if tag.strip()}
    
    def calculate_tag_similarity(self) -> Dict[Tuple[str, str], float]:
        """Calculate Jaccard similarity between tag sets of papers."""
        print("Calculating tag-based similarities...")
        tag_similarities = {}
        
        # Get tags for each paper
        paper_tags = {}
        for idx, row in self.papers.iterrows():
            paper_tags[row['cite_key']] = self.get_tag_set(row['Tags'])
        
        # Calculate pairwise similarities
        papers_list = list(paper_tags.keys())
        for i, paper1 in enumerate(papers_list):
            tags1 = paper_tags[paper1]
            if not tags1:  # Skip papers without tags
                continue
                
            for j in range(i + 1, len(papers_list)):
                paper2 = papers_list[j]
                tags2 = paper_tags[paper2]
                
                if not tags2:  # Skip papers without tags
                    continue
                
                # Jaccard similarity
                intersection = len(tags1 & tags2)
                union = len(tags1 | tags2)
                
                if union > 0:
                    similarity = intersection / union
                    if similarity > 0:  # Only store non-zero similarities
                        tag_similarities[(paper1, paper2)] = similarity
        
        print(f"Found {len(tag_similarities)} tag-based relationships")
        return tag_similarities
    
    def extract_keywords_from_summaries(self, max_features: int = 100) -> Dict[str, List[str]]:
        """Extract keywords from summaries and TL;DR using TF-IDF."""
        print("Extracting keywords from summaries...")
        
        # Combine summary, TL;DR, and insights for better keyword extraction
        documents = []
        cite_keys = []
        
        for idx, row in self.papers.iterrows():
            # Combine multiple text fields
            text_parts = []
            for field in ['Summary', 'TL;DR', 'Insights', 'Research Question']:
                if pd.notna(row[field]):
                    text_parts.append(self.clean_text(row[field]))
            
            combined_text = ' '.join(text_parts)
            if combined_text:
                documents.append(combined_text)
                cite_keys.append(row['cite_key'])
        
        if not documents:
            return {}
        
        # Fit TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words='english',
            ngram_range=(1, 2),  # Include bigrams
            min_df=2,  # Ignore terms that appear in less than 2 documents
            max_df=0.8  # Ignore terms that appear in more than 80% of documents
        )
        
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(documents)
        feature_names = self.tfidf_vectorizer.get_feature_names_out()
        
        # Extract top keywords for each paper
        keywords_dict = {}
        for i, cite_key in enumerate(cite_keys):
            # Get TF-IDF scores for this document
            scores = self.tfidf_matrix[i].toarray().flatten()
            # Get top 10 keywords
            top_indices = scores.argsort()[-10:][::-1]
            keywords = [feature_names[idx] for idx in top_indices if scores[idx] > 0]
            keywords_dict[cite_key] = keywords
        
        return keywords_dict
    
    def calculate_content_similarity(self) -> Dict[Tuple[str, str], float]:
        """Calculate content similarity between papers using TF-IDF and cosine similarity."""
        print("Calculating content-based similarities...")
        
        if self.tfidf_matrix is None:
            self.extract_keywords_from_summaries()
        
        if self.tfidf_matrix is None:
            return {}
        
        # Calculate cosine similarity between all documents
        similarity_matrix = cosine_similarity(self.tfidf_matrix)
        
        # Convert to dictionary format
        content_similarities = {}
        cite_keys = [row['cite_key'] for idx, row in self.papers.iterrows() 
                    if pd.notna(row['Summary']) or pd.notna(row['TL;DR'])]
        
        for i in range(len(cite_keys)):
            for j in range(i + 1, len(cite_keys)):
                similarity = similarity_matrix[i, j]
                if similarity > 0.1:  # Threshold to reduce noise
                    content_similarities[(cite_keys[i], cite_keys[j])] = similarity
        
        print(f"Found {len(content_similarities)} content-based relationships")
        return content_similarities
    
    def calculate_temporal_proximity(self, max_year_diff: int = 2) -> Dict[Tuple[str, str], float]:
        """Calculate temporal proximity between papers (published in same/adjacent years)."""
        print("Calculating temporal proximities...")
        temporal_similarities = {}
        
        # Group papers by year
        year_groups = defaultdict(list)
        for idx, row in self.papers.iterrows():
            if pd.notna(row['year']):
                year = int(row['year'])
                year_groups[year].append(row['cite_key'])
        
        # Calculate similarities based on year proximity
        years = sorted(year_groups.keys())
        for i, year1 in enumerate(years):
            papers1 = year_groups[year1]
            
            # Papers from same year have high proximity
            for j, paper1 in enumerate(papers1):
                for paper2 in papers1[j+1:]:
                    temporal_similarities[(paper1, paper2)] = 1.0
            
            # Papers from adjacent years have lower proximity
            for year_diff in range(1, max_year_diff + 1):
                year2 = year1 + year_diff
                if year2 in year_groups:
                    papers2 = year_groups[year2]
                    proximity = 1.0 - (year_diff / (max_year_diff + 1))
                    
                    for paper1 in papers1:
                        for paper2 in papers2:
                            temporal_similarities[(paper1, paper2)] = proximity
        
        print(f"Found {len(temporal_similarities)} temporal relationships")
        return temporal_similarities
    
    def calculate_author_overlap(self) -> Dict[Tuple[str, str], float]:
        """Calculate similarity based on shared authors."""
        print("Calculating author-based similarities...")
        author_similarities = {}
        
        # Get authors for each paper
        paper_authors = {}
        for idx, row in self.papers.iterrows():
            if pd.notna(row['authors']):
                authors = set(a.strip() for a in str(row['authors']).strip('"').split(',') 
                            if a.strip() and a.strip().lower() not in ['unavailable', 'unknown'])
                if authors:
                    paper_authors[row['cite_key']] = authors
        
        # Calculate pairwise similarities
        papers_list = list(paper_authors.keys())
        for i, paper1 in enumerate(papers_list):
            authors1 = paper_authors[paper1]
            
            for j in range(i + 1, len(papers_list)):
                paper2 = papers_list[j]
                authors2 = paper_authors[paper2]
                
                # Check for shared authors
                shared_authors = len(authors1 & authors2)
                if shared_authors > 0:
                    # Normalize by minimum author count
                    similarity = shared_authors / min(len(authors1), len(authors2))
                    author_similarities[(paper1, paper2)] = similarity
        
        print(f"Found {len(author_similarities)} author-based relationships")
        return author_similarities
    
    def generate_similarity_matrix(self, weights: Dict[str, float] = None) -> Dict[Tuple[str, str], float]:
        """Generate combined similarity matrix with weighted components."""
        if weights is None:
            weights = {
                'tags': 0.3,
                'content': 0.3,
                'temporal': 0.2,
                'authors': 0.2
            }
        
        print("Generating combined similarity matrix...")
        
        # Calculate individual similarity components
        tag_sim = self.calculate_tag_similarity()
        content_sim = self.calculate_content_similarity()
        temporal_sim = self.calculate_temporal_proximity()
        author_sim = self.calculate_author_overlap()
        
        # Combine all similarities
        all_pairs = set()
        all_pairs.update(tag_sim.keys())
        all_pairs.update(content_sim.keys())
        all_pairs.update(temporal_sim.keys())
        all_pairs.update(author_sim.keys())
        
        combined_similarities = {}
        for pair in all_pairs:
            score = 0
            components = 0
            
            if pair in tag_sim:
                score += weights['tags'] * tag_sim[pair]
                components += 1
            if pair in content_sim:
                score += weights['content'] * content_sim[pair]
                components += 1
            if pair in temporal_sim:
                score += weights['temporal'] * temporal_sim[pair]
                components += 1
            if pair in author_sim:
                score += weights['authors'] * author_sim[pair]
                components += 1
            
            # Normalize by number of components
            if components > 0:
                combined_similarities[pair] = score
        
        # Sort by similarity score
        sorted_similarities = dict(sorted(combined_similarities.items(), 
                                        key=lambda x: x[1], reverse=True))
        
        print(f"Generated {len(sorted_similarities)} total relationships")
        return sorted_similarities
    
    def get_top_similar_papers(self, paper_id: str, n: int = 5) -> List[Tuple[str, float]]:
        """Get top N most similar papers to a given paper."""
        if not self.similarity_matrix:
            self.similarity_matrix = self.generate_similarity_matrix()
        
        similar_papers = []
        for (paper1, paper2), score in self.similarity_matrix.items():
            if paper1 == paper_id:
                similar_papers.append((paper2, score))
            elif paper2 == paper_id:
                similar_papers.append((paper1, score))
        
        # Sort by score and return top N
        similar_papers.sort(key=lambda x: x[1], reverse=True)
        return similar_papers[:n]
    
    def export_similarity_matrix(self, output_path: str, threshold: float = 0.2):
        """Export similarity matrix to JSON format."""
        import json
        
        if not self.similarity_matrix:
            self.similarity_matrix = self.generate_similarity_matrix()
        
        # Filter by threshold and convert to list format
        similarities = []
        for (paper1, paper2), score in self.similarity_matrix.items():
            if score >= threshold:
                similarities.append({
                    'source': paper1,
                    'target': paper2,
                    'similarity': round(score, 3)
                })
        
        with open(output_path, 'w') as f:
            json.dump(similarities, f, indent=2)
        
        print(f"Exported {len(similarities)} relationships to {output_path}")