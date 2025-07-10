"""
Quick script to create the index.json file from existing data
"""

import json
from pathlib import Path

# Load existing data
base_dir = Path(__file__).parent.parent.parent
data_dir = base_dir / 'visualization' / 'data'

with open(data_dir / 'graph_data.json', 'r') as f:
    graph_data = json.load(f)

with open(data_dir / 'themes.json', 'r') as f:
    theme_data = json.load(f)

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
for theme in theme_data['themes']:
    theme_index[str(theme['id'])] = {
        'name': theme['name'],
        'keywords': theme['keywords'],
        'paper_count': theme['paper_count']
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

with open(data_dir / 'index.json', 'w') as f:
    json.dump(index_data, f, indent=2)

print(f"Created index.json with {len(paper_index)} papers, {len(author_index)} authors, and {len(theme_index)} themes")