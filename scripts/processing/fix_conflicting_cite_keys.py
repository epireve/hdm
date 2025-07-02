#!/usr/bin/env python3
"""
Fix conflicting cite_keys for papers with same cite_key but different titles
"""
import json
from pathlib import Path

def analyze_conflicts():
    """Analyze the false positives and suggest new cite_keys"""
    # Load verification results
    with open('duplicate_verification_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    false_positives = results['verification_results']['false_positives']
    
    print("=== Conflicting Cite Keys Analysis ===\n")
    print("These folders have the same cite_key but different titles:")
    print("They need unique cite_keys to avoid confusion.\n")
    
    suggestions = []
    
    for fp in false_positives:
        old_folder = fp['old_folder']
        cite_key = fp['old_cite_key']
        old_title = fp['old_title']
        target_title = fp['target_title']
        
        print(f"Conflict: {cite_key}")
        print(f"  Folder 1: {fp['target_folder']}")
        print(f"    Title: {target_title[:80]}...")
        print(f"  Folder 2: {old_folder}")
        print(f"    Title: {old_title[:80]}...")
        
        # Suggest new cite_key based on folder name or title
        if 'arxiv' in old_folder.lower():
            # Extract arxiv ID
            parts = old_folder.split('_')
            for part in parts:
                if part.startswith('2') and len(part) >= 4:
                    suggested_key = f"{cite_key}_arxiv{part[:4]}"
                    break
            else:
                suggested_key = f"{cite_key}_2"
        else:
            suggested_key = f"{cite_key}_2"
        
        print(f"  Suggested new cite_key for {old_folder}: {suggested_key}")
        print()
        
        suggestions.append({
            'folder': old_folder,
            'current_cite_key': cite_key,
            'suggested_cite_key': suggested_key,
            'title': old_title,
            'reason': 'Conflicting with existing paper of same cite_key but different title'
        })
    
    # Save suggestions
    with open('cite_key_conflict_suggestions.json', 'w', encoding='utf-8') as f:
        json.dump({
            'conflicts_found': len(false_positives),
            'suggestions': suggestions
        }, f, indent=2)
    
    print(f"\nTotal conflicts found: {len(false_positives)}")
    print("Suggestions saved to: cite_key_conflict_suggestions.json")
    print("\nThese folders should be renamed with unique cite_keys to avoid confusion.")

if __name__ == "__main__":
    analyze_conflicts()