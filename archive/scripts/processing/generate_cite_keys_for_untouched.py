#!/usr/bin/env python3
"""
Generate proper cite_keys for untouched folders based on author names and year
"""
import json
import re
from pathlib import Path

def extract_last_name(author_string):
    """Extract the last name from an author string"""
    # Clean the author string
    author = author_string.strip()
    
    # Remove any ORCID or other identifiers
    author = re.sub(r'\(https?://[^)]+\)', '', author)
    author = re.sub(r'\[https?://[^\]]+\]', '', author)
    
    # Split by common separators
    parts = author.split(',')
    if len(parts) > 1:
        # Format: "Last, First"
        return parts[0].strip().lower()
    
    # Try splitting by spaces
    parts = author.split()
    if parts:
        # Take the last word as last name
        return parts[-1].strip().lower()
    
    return author.lower()

def generate_cite_key(metadata):
    """Generate a cite_key from metadata following lastname_year format"""
    authors = metadata.get('authors', '')
    year = metadata.get('year', '')
    
    if not authors or not year:
        return None
    
    # Handle different author formats
    if isinstance(authors, list):
        first_author = authors[0] if authors else ''
    else:
        # Split by common separators
        author_list = re.split(r'[;,](?![^()]*\))', str(authors))
        first_author = author_list[0].strip() if author_list else ''
    
    # Extract last name
    last_name = extract_last_name(first_author)
    
    # Clean up the last name
    last_name = re.sub(r'[^a-z0-9]', '', last_name)
    
    # Create cite_key
    if last_name and year:
        return f"{last_name}_{year}"
    
    return None

def process_untouched_folders():
    """Process untouched folders and generate proper cite_keys"""
    # Load analysis results
    with open('untouched_folders_analysis.json', 'r', encoding='utf-8') as f:
        analysis = json.load(f)
    
    # Load existing papers to check for conflicts
    existing_cite_keys = set()
    csv_files = ['research_papers_clean.csv', 'research_table_with_citekeys.csv']
    
    for csv_file in csv_files:
        if Path(csv_file).exists():
            with open(csv_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if ',' in line:
                        cite_key = line.split(',')[0].strip()
                        if cite_key and cite_key != 'cite_key':
                            existing_cite_keys.add(cite_key)
    
    # Process folders
    cite_key_mapping = {}
    duplicates_to_delete = []
    folders_to_rename = {}
    
    for folder_name, metadata in analysis['folder_metadata'].items():
        current_cite_key = metadata.get('cite_key', '')
        
        # Check if this is a duplicate
        if current_cite_key in analysis['duplicates_by_cite_key']:
            # This is a duplicate - mark for deletion (keep the first one)
            duplicate_folders = analysis['duplicates_by_cite_key'][current_cite_key]
            if folder_name != duplicate_folders[0]:
                duplicates_to_delete.append(folder_name)
                continue
        
        # Generate proper cite_key if needed
        if not current_cite_key or current_cite_key == 'unknown':
            generated_key = generate_cite_key(metadata)
            if generated_key:
                # Handle conflicts
                base_key = generated_key
                counter = 2
                while generated_key in existing_cite_keys:
                    generated_key = f"{base_key}{counter}"
                    counter += 1
                
                folders_to_rename[folder_name] = generated_key
                existing_cite_keys.add(generated_key)
            else:
                print(f"Could not generate cite_key for {folder_name}")
        else:
            # Use existing cite_key
            folders_to_rename[folder_name] = current_cite_key
    
    # Create action plan
    action_plan = {
        'duplicates_to_delete': duplicates_to_delete,
        'folders_to_rename': folders_to_rename,
        'folders_missing_metadata': analysis['missing_metadata']
    }
    
    # Save action plan
    with open('untouched_folders_action_plan.json', 'w', encoding='utf-8') as f:
        json.dump(action_plan, f, indent=2)
    
    # Create summary report
    create_action_report(action_plan, analysis)
    
    return action_plan

def create_action_report(action_plan, analysis):
    """Create a markdown report of actions to take"""
    report = []
    report.append("# Untouched Folders Action Plan\n")
    
    report.append("## Summary")
    report.append(f"- Folders to delete (duplicates): {len(action_plan['duplicates_to_delete'])}")
    report.append(f"- Folders to rename: {len(action_plan['folders_to_rename'])}")
    report.append(f"- Folders missing metadata: {len(action_plan['folders_missing_metadata'])}\n")
    
    if action_plan['duplicates_to_delete']:
        report.append("## Duplicates to Delete\n")
        for folder in sorted(action_plan['duplicates_to_delete']):
            metadata = analysis['folder_metadata'].get(folder, {})
            cite_key = metadata.get('cite_key', 'unknown')
            title = metadata.get('title', 'No title')
            report.append(f"- **{folder}**")
            report.append(f"  - Cite key: {cite_key}")
            report.append(f"  - Title: {title}")
            report.append(f"  - Reason: Duplicate of another folder with same cite_key\n")
    
    if action_plan['folders_to_rename']:
        report.append("## Folders to Rename\n")
        for folder, new_name in sorted(action_plan['folders_to_rename'].items()):
            metadata = analysis['folder_metadata'].get(folder, {})
            title = metadata.get('title', 'No title')
            authors = metadata.get('authors', 'No authors')
            year = metadata.get('year', 'No year')
            report.append(f"- **{folder}** → **{new_name}**")
            report.append(f"  - Title: {title}")
            report.append(f"  - Authors: {authors}")
            report.append(f"  - Year: {year}\n")
    
    if action_plan['folders_missing_metadata']:
        report.append("## Folders Missing Metadata\n")
        report.append("These folders have no markdown files and cannot be processed:\n")
        for folder in sorted(action_plan['folders_missing_metadata']):
            report.append(f"- {folder}")
    
    # Save report
    with open('untouched_folders_action_plan.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print("Action plan created:")
    print("- untouched_folders_action_plan.json (data)")
    print("- untouched_folders_action_plan.md (report)")

if __name__ == "__main__":
    process_untouched_folders()