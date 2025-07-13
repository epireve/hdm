#!/usr/bin/env python3
"""
Fix duplicate targets in cite_key_corrections.json
"""

import json
from pathlib import Path
from collections import defaultdict

def fix_corrections(corrections_file):
    """Fix duplicate target cite_keys by adding suffixes"""
    
    # Load corrections
    with open(corrections_file, 'r') as f:
        corrections = json.load(f)
    
    print(f"Loaded {len(corrections)} corrections")
    
    # Find duplicate targets
    target_sources = defaultdict(list)
    for source, target in corrections.items():
        target_sources[target].append(source)
    
    duplicates = {k: v for k, v in target_sources.items() if len(v) > 1}
    print(f"Found {len(duplicates)} duplicate target cite_keys")
    
    # Fix duplicates
    fixed_corrections = corrections.copy()
    fixes_made = 0
    
    for target, sources in duplicates.items():
        print(f"\nTarget '{target}' has {len(sources)} sources:")
        
        # Keep first source as-is, add suffixes to others
        for i, source in enumerate(sorted(sources)):
            if i == 0:
                print(f"  {source} -> {target} (keep)")
            else:
                suffix = chr(ord('a') + i - 1)  # a, b, c, etc.
                new_target = f"{target}{suffix}"
                fixed_corrections[source] = new_target
                fixes_made += 1
                print(f"  {source} -> {new_target} (fixed)")
    
    # Save fixed corrections
    output_file = corrections_file.parent / "cite_key_corrections_fixed.json"
    with open(output_file, 'w') as f:
        json.dump(fixed_corrections, f, indent=2, sort_keys=True)
    
    print(f"\n✅ Fixed {fixes_made} duplicate targets")
    print(f"📁 Saved to: {output_file}")
    
    # Backup original
    backup_file = corrections_file.parent / "cite_key_corrections_backup.json"
    corrections_file.rename(backup_file)
    output_file.rename(corrections_file)
    print(f"📁 Original backed up to: {backup_file}")
    
    return fixed_corrections

def verify_fix(corrections_file):
    """Verify no duplicates remain"""
    with open(corrections_file, 'r') as f:
        corrections = json.load(f)
    
    # Check for duplicate targets
    target_counts = defaultdict(int)
    for target in corrections.values():
        target_counts[target] += 1
    
    duplicates = [k for k, v in target_counts.items() if v > 1]
    
    if duplicates:
        print(f"\n⚠️  Still have {len(duplicates)} duplicate targets!")
    else:
        print(f"\n✅ No duplicate targets found - all {len(corrections)} corrections are unique!")

if __name__ == "__main__":
    corrections_file = Path("/Users/invoture/dev.local/hdm/production_final_reformatted_1752365947/cite_key_corrections.json")
    
    print("🔧 Fixing duplicate targets in cite_key_corrections.json...")
    fix_corrections(corrections_file)
    
    print("\n🔍 Verifying fix...")
    verify_fix(corrections_file)