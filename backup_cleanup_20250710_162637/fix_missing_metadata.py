#!/usr/bin/env python3
"""
Fix papers with missing tags, DOIs, or URLs
"""
import re
import csv
from pathlib import Path
from datetime import datetime

def extract_yaml_frontmatter(content):
    """Extract YAML frontmatter from markdown content"""
    yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not yaml_match:
        return None, content
    
    yaml_str = yaml_match.group(1)
    yaml_data = {}
    
    # Parse YAML manually
    current_key = None
    tags_list = []
    in_tags = False
    
    for line in yaml_str.split('\n'):
        if line.strip():
            if line.strip() == 'tags:':
                in_tags = True
                current_key = 'tags'
                continue
            elif in_tags and line.startswith('  -'):
                tag = line.replace('  -', '').strip().strip('"').strip("'")
                tags_list.append(tag)
            elif ':' in line and not line.startswith(' ') and not line.startswith('-'):
                in_tags = False
                parts = line.split(':', 1)
                current_key = parts[0].strip()
                value = parts[1].strip().strip('"').strip("'")
                yaml_data[current_key] = value
    
    if tags_list:
        yaml_data['tags'] = tags_list
    
    # Get rest of content
    rest_content = content[yaml_match.end():]
    
    return yaml_data, rest_content

def analyze_content_for_metadata(content):
    """Analyze paper content to extract missing metadata"""
    metadata = {
        'tags': [],
        'url': None,
        'doi': None,
        'relevancy': None
    }
    
    # Extract tags from content
    tags_set = set()
    
    # Look for common keywords in title and content
    title_keywords = ['knowledge graph', 'personal', 'temporal', 'privacy', 'federated', 
                      'heterogeneous', 'healthcare', 'digital twin', 'memory', 'semantic',
                      'ontology', 'integration', 'machine learning', 'AI', 'LLM']
    
    content_lower = content.lower()
    for keyword in title_keywords:
        if keyword.lower() in content_lower:
            tags_set.add(keyword.replace(' ', '_').lower())
    
    # Look for specific patterns
    if 'sustainable development goal' in content_lower:
        tags_set.add('sdg')
        tags_set.add('medicine_access')
    
    if 'children' in content_lower or 'pediatric' in content_lower:
        tags_set.add('pediatric')
        tags_set.add('children')
    
    if 'availability' in content_lower and 'affordability' in content_lower:
        tags_set.add('availability')
        tags_set.add('affordability')
    
    # Look for methodology keywords
    if 'survey' in content_lower or 'case study' in content_lower:
        tags_set.add('survey')
    
    if 'who' in content_lower and 'essential medicines' in content_lower:
        tags_set.add('who')
        tags_set.add('essential_medicines')
    
    metadata['tags'] = sorted(list(tags_set))
    
    # Extract URL from DOI if available
    doi_match = re.search(r'doi:\s*([^\s]+)', content_lower)
    if doi_match:
        doi = doi_match.group(1).strip()
        if doi.startswith('10.'):
            metadata['doi'] = doi
            metadata['url'] = f"https://doi.org/{doi}"
    
    # Determine relevancy based on content
    hdm_keywords = ['personal knowledge graph', 'human digital memory', 'digital twin',
                    'knowledge management', 'personal data', 'memory system']
    
    relevancy_score = 0
    for keyword in hdm_keywords:
        if keyword in content_lower:
            relevancy_score += 2
    
    if relevancy_score >= 4:
        metadata['relevancy'] = 'High'
    elif relevancy_score >= 2:
        metadata['relevancy'] = 'Medium'
    else:
        metadata['relevancy'] = 'Low'
    
    return metadata

def update_yaml_frontmatter(yaml_data, metadata_updates):
    """Update YAML data with new metadata"""
    updated = yaml_data.copy()
    
    # Update tags if missing
    if not updated.get('tags') and metadata_updates.get('tags'):
        updated['tags'] = metadata_updates['tags']
    
    # Update URL if missing
    if not updated.get('url') and metadata_updates.get('url'):
        updated['url'] = metadata_updates['url']
    
    # Update relevancy if missing
    if not updated.get('relevancy') and metadata_updates.get('relevancy'):
        updated['relevancy'] = metadata_updates['relevancy']
    
    # Update relevancy_justification if relevancy was added
    if metadata_updates.get('relevancy') and not updated.get('relevancy_justification'):
        if metadata_updates['relevancy'] == 'High':
            updated['relevancy_justification'] = "Directly addresses HDM/PKG concepts with focus on personal data management"
        elif metadata_updates['relevancy'] == 'Medium':
            updated['relevancy_justification'] = "Contains relevant concepts applicable to HDM systems"
        else:
            updated['relevancy_justification'] = "Tangentially related to knowledge management or data systems"
    
    return updated

def format_yaml_frontmatter(yaml_data):
    """Format YAML data back to string"""
    lines = ['---']
    
    # Order fields consistently
    field_order = ['cite_key', 'title', 'authors', 'year', 'doi', 'url', 
                   'relevancy', 'relevancy_justification', 'tags', 
                   'date_processed', 'phase2_processed', 'original_folder']
    
    for field in field_order:
        if field in yaml_data:
            value = yaml_data[field]
            if field == 'tags' and isinstance(value, list):
                if value:  # Only add tags section if there are tags
                    lines.append('tags:')
                    for tag in value:
                        lines.append(f'  - {tag}')
            else:
                # Handle multiline values
                if isinstance(value, str) and '\n' in value:
                    lines.append(f'{field}: |')
                    for line in value.split('\n'):
                        lines.append(f'  {line}')
                else:
                    lines.append(f'{field}: {value}')
    
    # Add any fields not in the standard order
    for field, value in yaml_data.items():
        if field not in field_order:
            if isinstance(value, list):
                lines.append(f'{field}:')
                for item in value:
                    lines.append(f'  - {item}')
            else:
                lines.append(f'{field}: {value}')
    
    lines.append('---')
    return '\n'.join(lines) + '\n'

def main():
    """Main function to fix missing metadata"""
    markdown_papers = Path('markdown_papers')
    
    report = []
    report.append("FIXING MISSING METADATA")
    report.append(f"Generated: {datetime.now().isoformat()}")
    report.append("=" * 70)
    
    # Read the papers needing attention
    papers_to_fix = []
    if Path('papers_needing_attention.csv').exists():
        with open('papers_needing_attention.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                warnings = row.get('warnings', '')
                if any(missing in warnings for missing in ['Missing tags', 'Missing URL', 'Missing relevancy']):
                    papers_to_fix.append(row)
    
    report.append(f"\nPapers to analyze: {len(papers_to_fix)}")
    report.append("-" * 40)
    
    fixed_count = 0
    fixes_by_type = {
        'tags': 0,
        'url': 0,
        'relevancy': 0
    }
    
    # Process each paper
    for i, paper_info in enumerate(papers_to_fix[:50], 1):  # Process first 50 for now
        folder = paper_info['folder']
        paper_path = markdown_papers / folder / 'paper.md'
        
        if not paper_path.exists():
            report.append(f"\n{i}. {folder}: Paper file not found")
            continue
        
        try:
            # Read the paper
            with open(paper_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract YAML and content
            yaml_data, rest_content = extract_yaml_frontmatter(content)
            if not yaml_data:
                report.append(f"\n{i}. {folder}: No YAML frontmatter found")
                continue
            
            # Analyze content for metadata
            metadata_updates = analyze_content_for_metadata(content)
            
            # Check what needs updating
            needs_update = False
            updates_made = []
            
            if not yaml_data.get('tags') and metadata_updates.get('tags'):
                needs_update = True
                updates_made.append(f"tags: {', '.join(metadata_updates['tags'][:5])}")
                fixes_by_type['tags'] += 1
            
            if not yaml_data.get('url') and metadata_updates.get('url'):
                needs_update = True
                updates_made.append(f"url: {metadata_updates['url']}")
                fixes_by_type['url'] += 1
            
            if not yaml_data.get('relevancy') and metadata_updates.get('relevancy'):
                needs_update = True
                updates_made.append(f"relevancy: {metadata_updates['relevancy']}")
                fixes_by_type['relevancy'] += 1
            
            if needs_update:
                # Update YAML data
                updated_yaml = update_yaml_frontmatter(yaml_data, metadata_updates)
                
                # Reconstruct the file
                new_content = format_yaml_frontmatter(updated_yaml) + rest_content
                
                # Write back
                with open(paper_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                report.append(f"\n{i}. {folder}: FIXED")
                for update in updates_made:
                    report.append(f"   - {update}")
                fixed_count += 1
            else:
                report.append(f"\n{i}. {folder}: No automatic fixes possible")
        
        except Exception as e:
            report.append(f"\n{i}. {folder}: Error - {str(e)}")
    
    # Summary
    report.append(f"\n\nSUMMARY")
    report.append("-" * 40)
    report.append(f"Papers analyzed: {min(50, len(papers_to_fix))}")
    report.append(f"Papers fixed: {fixed_count}")
    report.append(f"Tags added: {fixes_by_type['tags']}")
    report.append(f"URLs added: {fixes_by_type['url']}")
    report.append(f"Relevancy added: {fixes_by_type['relevancy']}")
    
    if len(papers_to_fix) > 50:
        report.append(f"\nNote: Only processed first 50 papers. {len(papers_to_fix) - 50} papers remaining.")
    
    # Save report
    report_path = Path('missing_metadata_fixes.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print('\n'.join(report))
    print(f"\nReport saved to: {report_path}")

if __name__ == '__main__':
    main()