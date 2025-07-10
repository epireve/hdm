#!/usr/bin/env python3
"""
Fix folders with conflicting cite_keys by renaming them and updating metadata
"""
import json
import os
from pathlib import Path
from datetime import datetime

def load_conflict_suggestions():
    """Load the conflict suggestions"""
    with open('cite_key_conflict_suggestions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def update_metadata_in_file(file_path, old_cite_key, new_cite_key):
    """Update cite_key in markdown file metadata"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update in YAML frontmatter
        if content.startswith('---\n'):
            end_idx = content.find('\n---\n', 4)
            if end_idx != -1:
                yaml_content = content[4:end_idx]
                rest_content = content[end_idx:]
                
                # Replace cite_key in YAML
                lines = yaml_content.split('\n')
                new_lines = []
                for line in lines:
                    if line.startswith('cite_key:'):
                        new_lines.append(f'cite_key: {new_cite_key}')
                    else:
                        new_lines.append(line)
                
                # Reconstruct file
                new_content = '---\n' + '\n'.join(new_lines) + rest_content
                
                # Write back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return True
    except Exception as e:
        print(f"Error updating metadata in {file_path}: {e}")
    return False

def rename_conflicting_folders():
    """Rename folders with conflicting cite_keys"""
    suggestions = load_conflict_suggestions()
    
    markdown_papers_dir = Path('markdown_papers')
    results = {
        'renamed': [],
        'failed': [],
        'timestamp': datetime.now().isoformat()
    }
    
    print(f"Processing {len(suggestions['suggestions'])} conflicting folders...\n")
    
    for suggestion in suggestions['suggestions']:
        old_folder = suggestion['folder']
        old_cite_key = suggestion['current_cite_key']
        new_cite_key = suggestion['suggested_cite_key']
        
        old_path = markdown_papers_dir / old_folder
        new_path = markdown_papers_dir / new_cite_key
        
        if not old_path.exists():
            print(f"✗ Folder not found: {old_folder}")
            results['failed'].append({
                'folder': old_folder,
                'reason': 'Folder not found'
            })
            continue
        
        if new_path.exists():
            print(f"✗ Target already exists: {new_cite_key}")
            results['failed'].append({
                'folder': old_folder,
                'reason': f'Target {new_cite_key} already exists'
            })
            continue
        
        try:
            # First update metadata in all markdown files
            md_files = list(old_path.glob('*.md'))
            metadata_updated = False
            
            for md_file in md_files:
                if update_metadata_in_file(md_file, old_cite_key, new_cite_key):
                    metadata_updated = True
                    print(f"  Updated metadata in: {md_file.name}")
            
            # Rename folder
            old_path.rename(new_path)
            
            print(f"✓ Renamed: {old_folder} → {new_cite_key}")
            print(f"  Title: {suggestion['title'][:60]}...")
            
            results['renamed'].append({
                'old_folder': old_folder,
                'new_folder': new_cite_key,
                'old_cite_key': old_cite_key,
                'new_cite_key': new_cite_key,
                'title': suggestion['title'],
                'metadata_updated': metadata_updated
            })
            
        except Exception as e:
            print(f"✗ Error renaming {old_folder}: {e}")
            results['failed'].append({
                'folder': old_folder,
                'reason': str(e)
            })
        
        print()
    
    # Save results
    with open('conflicting_folders_fix_report.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n=== Summary ===")
    print(f"Successfully renamed: {len(results['renamed'])}")
    print(f"Failed: {len(results['failed'])}")
    print(f"Report saved: conflicting_folders_fix_report.json")
    
    return results

def check_missing_metadata_folders():
    """Check folders that are missing metadata"""
    missing_folders = [
        "arxiv_arxiv_2112.08025_TLogic_Temporal_Logical_Rules_for_Explainable_Link_Forecasting_on_Temporal_Knowledge_Graphs",
        "arxiv_arxiv_2502.13412_Explore-Construct-Filter_An_Automated_Framework_for_Rich_and_Reliable_API_Knowle",
        "constructing_pkg_conversation_rl_2024",
        "jmir_2023_digital_health_coaching_hpv",
        "Local-Global_History-Aware_Contrastive_Learning_for_Temporal_Knowledge_Graph_Reasoning",
        "openreview_141b7821_Share_Your_Representation_Only_Guaranteed_Improvement_of_the_Privacy-Utility_Tradeoff_in_Federated_L",
        "precision_nutrition_pkg_2024",
        "Question_Answering_Over_Temporal_KG_ACL2021"
    ]
    
    markdown_papers_dir = Path('markdown_papers')
    report = []
    
    print("\n=== Checking Folders Missing Metadata ===\n")
    
    for folder in missing_folders:
        folder_path = markdown_papers_dir / folder
        
        if not folder_path.exists():
            report.append({
                'folder': folder,
                'status': 'not_found',
                'action': 'Already deleted or doesn\'t exist'
            })
            print(f"✗ Not found: {folder}")
            continue
        
        # Check folder contents
        files = list(folder_path.iterdir())
        md_files = list(folder_path.glob('*.md'))
        
        if not files:
            report.append({
                'folder': folder,
                'status': 'empty',
                'action': 'Recommend deletion - empty folder'
            })
            print(f"✗ Empty folder: {folder}")
        elif not md_files:
            report.append({
                'folder': folder,
                'status': 'no_markdown',
                'files': [f.name for f in files],
                'action': 'Recommend deletion - no markdown files'
            })
            print(f"✗ No markdown files in: {folder}")
            print(f"  Contains: {', '.join(f.name for f in files[:5])}...")
        else:
            report.append({
                'folder': folder,
                'status': 'has_markdown',
                'md_files': [f.name for f in md_files],
                'action': 'Check why metadata extraction failed'
            })
            print(f"? Has markdown files: {folder}")
            print(f"  Files: {', '.join(f.name for f in md_files)}")
    
    # Save report
    with open('missing_metadata_folders_report.json', 'w', encoding='utf-8') as f:
        json.dump({
            'folders_checked': len(missing_folders),
            'report': report,
            'timestamp': datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"\nReport saved: missing_metadata_folders_report.json")
    
    return report

if __name__ == "__main__":
    print("=== Fixing Conflicting Cite Keys ===\n")
    
    response = input("This will rename 14 folders with conflicting cite_keys. Continue? (yes/no): ")
    if response.lower() == 'yes':
        rename_results = rename_conflicting_folders()
        
        print("\n" + "="*50 + "\n")
        check_missing_metadata_folders()
    else:
        print("Operation cancelled.")