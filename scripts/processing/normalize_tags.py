#!/usr/bin/env python3
"""
Normalize and standardize Tags column:
1. Remove array formatting
2. Standardize tag names (consistent casing and separators)
"""

import csv
import re
from pathlib import Path

# Tag normalization mappings
TAG_MAPPINGS = {
    # Knowledge graph variations
    'knowledge graph': 'knowledge-graph',
    'knowledge graphs': 'knowledge-graph',
    'knowledge_graph': 'knowledge-graph',
    'knowledge_graphs': 'knowledge-graph',
    'kg': 'knowledge-graph',
    'kgs': 'knowledge-graph',
    
    # Data integration variations
    'data integration': 'data-integration',
    'data_integration': 'data-integration',
    'dataintegration': 'data-integration',
    
    # Machine learning variations
    'machine learning': 'machine-learning',
    'machine_learning': 'machine-learning',
    'ml': 'machine-learning',
    
    # AI variations
    'artificial intelligence': 'ai',
    'artificial_intelligence': 'ai',
    
    # Temporal variations
    'temporal data': 'temporal-data',
    'temporal_data': 'temporal-data',
    'time series': 'time-series',
    'time_series': 'time-series',
    'temporal knowledge graph': 'temporal-knowledge-graph',
    'temporal knowledge graphs': 'temporal-knowledge-graph',
    
    # Personal variations
    'personal knowledge': 'personal-knowledge',
    'personal_knowledge': 'personal-knowledge',
    'personal knowledge graph': 'personal-knowledge-graph',
    'personal knowledge graphs': 'personal-knowledge-graph',
    'pkg': 'personal-knowledge-graph',
    'pkgs': 'personal-knowledge-graph',
    
    # Healthcare variations
    'health care': 'healthcare',
    'health-care': 'healthcare',
    'medical': 'healthcare',
    
    # Educational variations
    'educational technology': 'educational-technology',
    'educational_technology': 'educational-technology',
    'edtech': 'educational-technology',
    'education': 'educational-technology',
    
    # GNN variations
    'graph neural network': 'graph-neural-networks',
    'graph neural networks': 'graph-neural-networks',
    'gnn': 'graph-neural-networks',
    'gnns': 'graph-neural-networks',
    
    # LLM variations
    'large language model': 'llm',
    'large language models': 'llm',
    'large_language_model': 'llm',
    'large_language_models': 'llm',
    
    # Semantic variations
    'semantic web': 'semantic-web',
    'semantic_web': 'semantic-web',
    
    # Federated variations
    'federated learning': 'federated-learning',
    'federated_learning': 'federated-learning',
    
    # Privacy variations
    'privacy preserving': 'privacy-preserving',
    'privacy_preserving': 'privacy-preserving',
}

def normalize_tag(tag):
    """Normalize individual tag"""
    tag = tag.strip()
    if not tag:
        return None
    
    # Convert to lowercase for matching
    tag_lower = tag.lower()
    
    # Check if we have a mapping for this tag
    if tag_lower in TAG_MAPPINGS:
        return TAG_MAPPINGS[tag_lower]
    
    # Standard normalization if no specific mapping
    # Replace underscores and spaces with hyphens
    normalized = re.sub(r'[\s_]+', '-', tag_lower)
    
    # Remove any special characters except hyphens
    normalized = re.sub(r'[^\w\-]', '', normalized)
    
    # Remove duplicate hyphens
    normalized = re.sub(r'-+', '-', normalized)
    
    # Remove leading/trailing hyphens
    normalized = normalized.strip('-')
    
    return normalized if normalized else None

def standardize_tags(tags_value):
    """Convert various tag formats to normalized comma-separated string"""
    if not tags_value:
        return ""
    
    # Remove array brackets and quotes
    tags = tags_value.strip()
    
    # Handle array format like ['tag1', 'tag2'] or ["tag1", "tag2"]
    if tags.startswith('[') and tags.endswith(']'):
        # Remove brackets
        tags = tags[1:-1]
        
        # Remove quotes around individual tags
        tags = re.sub(r"['\"]", '', tags)
    
    # Split by comma
    tag_list = [t.strip() for t in tags.split(',') if t.strip()]
    
    # Normalize each tag
    normalized_tags = []
    seen_tags = set()  # To avoid duplicates
    
    for tag in tag_list:
        normalized = normalize_tag(tag)
        if normalized and normalized not in seen_tags:
            normalized_tags.append(normalized)
            seen_tags.add(normalized)
    
    # Sort tags for consistency
    normalized_tags.sort()
    
    # Join with comma and space
    return ', '.join(normalized_tags)

def process_file(input_file, output_file):
    """Process CSV file to normalize Tags column"""
    
    print(f"Reading {input_file}...")
    
    # Read the CSV
    papers = []
    fieldnames = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        papers = list(reader)
    
    print(f"Loaded {len(papers)} papers")
    
    # Process Tags column
    print("\nNormalizing Tags column...")
    
    tags_changed = 0
    sample_changes = []
    
    for paper in papers:
        if 'Tags' in paper and paper['Tags']:
            original = paper['Tags']
            normalized = standardize_tags(original)
            
            if original != normalized:
                tags_changed += 1
                if len(sample_changes) < 10:
                    sample_changes.append({
                        'original': original[:100] + '...' if len(original) > 100 else original,
                        'normalized': normalized[:100] + '...' if len(normalized) > 100 else normalized
                    })
            
            paper['Tags'] = normalized
    
    print(f"Normalized {tags_changed} tag entries")
    
    if sample_changes:
        print("\n=== Sample Changes ===")
        for i, change in enumerate(sample_changes, 1):
            print(f"\n{i}. Original: {change['original']}")
            print(f"   Normalized: {change['normalized']}")
    
    # Write the updated CSV
    print(f"\nWriting to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(papers)
    
    print(f"Saved {len(papers)} papers with normalized tags")
    
    # Show tag statistics
    print("\n=== Tag Statistics ===")
    
    tag_counts = {}
    papers_with_tags = 0
    
    for paper in papers:
        if 'Tags' in paper and paper['Tags']:
            papers_with_tags += 1
            tags = [t.strip() for t in paper['Tags'].split(',') if t.strip()]
            
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    print(f"Papers with tags: {papers_with_tags}")
    print(f"Unique tags: {len(tag_counts)}")
    
    # Show most common tags
    if tag_counts:
        print("\nTop 20 most common tags:")
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        for tag, count in sorted_tags[:20]:
            print(f"  {tag}: {count}")

def main():
    project_root = Path(__file__).parent.parent.parent
    
    # Process the merged file
    input_file = project_root / "research_papers_merged_final.csv"
    output_file = project_root / "research_papers_merged_final_normalized_tags.csv"
    
    print("=== Processing Merged File ===")
    process_file(input_file, output_file)
    
    print("\n" + "="*60 + "\n")
    
    # Also process the original complete file
    original_file = project_root / "research_papers_complete_FINAL.csv"
    if original_file.exists():
        print("=== Processing Original Complete File ===")
        output_original = project_root / "research_papers_complete_FINAL_normalized_tags.csv"
        process_file(original_file, output_original)

if __name__ == "__main__":
    main()