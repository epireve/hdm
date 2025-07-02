#!/usr/bin/env python3
"""
Thoroughly verify duplicates by checking both cite_key and title
"""
import os
import json
from pathlib import Path
from collections import defaultdict

def extract_metadata_from_markdown(md_file):
    """Extract YAML frontmatter from markdown file"""
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if content.startswith('---\n'):
            end_idx = content.find('\n---\n', 4)
            if end_idx != -1:
                yaml_content = content[4:end_idx]
                metadata = {}
                current_key = None
                
                for line in yaml_content.split('\n'):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    if line.startswith('- '):
                        if current_key and current_key not in metadata:
                            metadata[current_key] = []
                        if current_key and isinstance(metadata[current_key], list):
                            metadata[current_key].append(line[2:].strip())
                    elif ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        if value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        elif value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        
                        if value:
                            metadata[key] = value
                        else:
                            current_key = key
                            
                return metadata
    except Exception as e:
        print(f"Error reading {md_file}: {e}")
    return None

def get_all_folder_metadata():
    """Get metadata for all folders in markdown_papers"""
    markdown_papers_dir = Path('markdown_papers')
    all_metadata = {}
    
    for folder in markdown_papers_dir.iterdir():
        if folder.is_dir():
            md_files = list(folder.glob('*.md'))
            if md_files:
                metadata = extract_metadata_from_markdown(md_files[0])
                if metadata:
                    all_metadata[folder.name] = metadata
    
    return all_metadata

def verify_duplicates():
    """Thoroughly verify duplicates by cite_key and title"""
    # Load the action plan with folders that couldn't be renamed
    with open('untouched_folders_action_plan.json', 'r', encoding='utf-8') as f:
        action_plan = json.load(f)
    
    # Get metadata for all folders
    print("Scanning all folders in markdown_papers...")
    all_metadata = get_all_folder_metadata()
    
    # Group folders by cite_key
    cite_key_groups = defaultdict(list)
    for folder_name, metadata in all_metadata.items():
        cite_key = metadata.get('cite_key', 'no_cite_key')
        cite_key_groups[cite_key].append((folder_name, metadata))
    
    # Group folders by title (normalized)
    title_groups = defaultdict(list)
    for folder_name, metadata in all_metadata.items():
        title = metadata.get('title', '').lower().strip()
        if title:
            title_groups[title].append((folder_name, metadata))
    
    # Load processing report if it exists to get rename failures
    rename_failed = []
    if os.path.exists('untouched_folders_processing_report.json'):
        with open('untouched_folders_processing_report.json', 'r', encoding='utf-8') as f:
            processing_report = json.load(f)
            rename_failed = processing_report.get('rename_failed', [])
    
    # Analyze potential duplicates from the rename failures
    verification_results = {
        'confirmed_duplicates': [],
        'false_positives': [],
        'missing_targets': []
    }
    
    for failure_info in rename_failed:
        old_folder, target_cite_key, reason = failure_info
        if reason != "Target exists":
            continue
            
        # Check if the old folder still exists
        if old_folder not in all_metadata:
            print(f"Warning: {old_folder} no longer exists")
            continue
            
        old_metadata = all_metadata[old_folder]
        old_title = old_metadata.get('title', '').lower().strip()
        old_cite_key = old_metadata.get('cite_key', '')
        
        # Find the target folder
        target_found = False
        for folder_name, metadata in all_metadata.items():
            if folder_name == target_cite_key or metadata.get('cite_key', '') == target_cite_key:
                target_metadata = metadata
                target_title = target_metadata.get('title', '').lower().strip()
                
                # Verify it's a true duplicate
                if old_title == target_title and old_cite_key == target_cite_key:
                    verification_results['confirmed_duplicates'].append({
                        'old_folder': old_folder,
                        'target_folder': folder_name,
                        'cite_key': target_cite_key,
                        'title': old_metadata.get('title', ''),
                        'match_type': 'exact'
                    })
                else:
                    verification_results['false_positives'].append({
                        'old_folder': old_folder,
                        'target_folder': folder_name,
                        'old_cite_key': old_cite_key,
                        'target_cite_key': target_cite_key,
                        'old_title': old_metadata.get('title', ''),
                        'target_title': target_metadata.get('title', ''),
                        'reason': 'Title or cite_key mismatch'
                    })
                target_found = True
                break
        
        if not target_found:
            verification_results['missing_targets'].append({
                'old_folder': old_folder,
                'expected_target': target_cite_key
            })
    
    # Find all duplicate groups (folders with same cite_key AND title)
    true_duplicate_groups = []
    for cite_key, folders in cite_key_groups.items():
        if len(folders) > 1:
            # Group by title within same cite_key
            title_subgroups = defaultdict(list)
            for folder_name, metadata in folders:
                title = metadata.get('title', '').lower().strip()
                title_subgroups[title].append((folder_name, metadata))
            
            # Find true duplicates (same cite_key AND title)
            for title, title_folders in title_subgroups.items():
                if len(title_folders) > 1:
                    true_duplicate_groups.append({
                        'cite_key': cite_key,
                        'title': title_folders[0][1].get('title', ''),
                        'folders': [f[0] for f in title_folders]
                    })
    
    # Save detailed results
    results = {
        'verification_results': verification_results,
        'all_duplicate_groups': true_duplicate_groups,
        'total_folders_scanned': len(all_metadata),
        'statistics': {
            'confirmed_duplicates': len(verification_results['confirmed_duplicates']),
            'false_positives': len(verification_results['false_positives']),
            'missing_targets': len(verification_results['missing_targets']),
            'duplicate_groups': len(true_duplicate_groups)
        }
    }
    
    with open('duplicate_verification_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    # Create detailed report
    create_verification_report(results)
    
    return results

def create_verification_report(results):
    """Create a detailed verification report"""
    report = []
    report.append("# Duplicate Verification Report\n")
    
    stats = results['statistics']
    report.append("## Summary Statistics")
    report.append(f"- Total folders scanned: {results['total_folders_scanned']}")
    report.append(f"- Confirmed duplicates: {stats['confirmed_duplicates']}")
    report.append(f"- False positives: {stats['false_positives']}")
    report.append(f"- Missing targets: {stats['missing_targets']}")
    report.append(f"- Duplicate groups found: {stats['duplicate_groups']}\n")
    
    # Confirmed duplicates
    if results['verification_results']['confirmed_duplicates']:
        report.append("## Confirmed Duplicates (Safe to Delete)\n")
        report.append("These folders have matching cite_key AND title:\n")
        for dup in results['verification_results']['confirmed_duplicates']:
            report.append(f"### {dup['old_folder']} → {dup['target_folder']}")
            report.append(f"- **Cite Key**: {dup['cite_key']}")
            report.append(f"- **Title**: {dup['title']}")
            report.append(f"- **Status**: ✓ Safe to delete {dup['old_folder']}\n")
    
    # False positives
    if results['verification_results']['false_positives']:
        report.append("## FALSE POSITIVES - DO NOT DELETE\n")
        report.append("These folders have different titles or cite_keys:\n")
        for fp in results['verification_results']['false_positives']:
            report.append(f"### ⚠️ {fp['old_folder']} vs {fp['target_folder']}")
            report.append(f"- **Old Cite Key**: {fp['old_cite_key']}")
            report.append(f"- **Target Cite Key**: {fp['target_cite_key']}")
            report.append(f"- **Old Title**: {fp['old_title']}")
            report.append(f"- **Target Title**: {fp['target_title']}")
            report.append(f"- **Status**: ❌ DO NOT DELETE - {fp['reason']}\n")
    
    # All duplicate groups
    if results['all_duplicate_groups']:
        report.append("## All Duplicate Groups in Database\n")
        report.append("Groups of folders with identical cite_key AND title:\n")
        for group in results['all_duplicate_groups']:
            report.append(f"### Group: {group['cite_key']}")
            report.append(f"- **Title**: {group['title']}")
            report.append(f"- **Folders**: {', '.join(group['folders'])}")
            report.append(f"- **Recommendation**: Keep the folder named '{group['cite_key']}', delete others\n")
    
    # Save report
    with open('duplicate_verification_report.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print("Verification complete!")
    print("- duplicate_verification_results.json (detailed data)")
    print("- duplicate_verification_report.md (human-readable report)")

if __name__ == "__main__":
    verify_duplicates()