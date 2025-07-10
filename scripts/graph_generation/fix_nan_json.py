#!/usr/bin/env python3
"""
Fix NaN values in JSON files by converting them to null
"""

import json
import numpy as np
from pathlib import Path

class NanEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles NaN values"""
    def encode(self, obj):
        if isinstance(obj, float):
            if np.isnan(obj):
                return "null"
        return super().encode(obj)
    
    def iterencode(self, obj, _one_shot=False):
        """Encode object while handling NaN values"""
        for chunk in super().iterencode(obj, _one_shot):
            yield chunk

def fix_nan_in_dict(obj):
    """Recursively fix NaN values in dictionary"""
    if isinstance(obj, dict):
        return {k: fix_nan_in_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [fix_nan_in_dict(item) for item in obj]
    elif isinstance(obj, float) and np.isnan(obj):
        return None
    else:
        return obj

def fix_json_file(file_path):
    """Fix NaN values in a JSON file"""
    print(f"Fixing {file_path}...")
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace literal NaN with null
    content = content.replace(': NaN,', ': null,')
    content = content.replace(': NaN\n', ': null\n')
    content = content.replace(': NaN}', ': null}')
    
    # Parse and re-encode to ensure valid JSON
    try:
        data = json.loads(content)
        
        # Fix any remaining NaN values
        data = fix_nan_in_dict(data)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Fixed {file_path}")
        return True
    except json.JSONDecodeError as e:
        print(f"  ❌ Error parsing {file_path}: {e}")
        return False

def main():
    """Fix all JSON files in visualization/data directory"""
    base_dir = Path(__file__).parent.parent.parent
    data_dir = base_dir / 'visualization' / 'data'
    
    json_files = list(data_dir.glob('*.json'))
    
    print(f"Found {len(json_files)} JSON files to fix")
    
    for json_file in json_files:
        fix_json_file(json_file)
    
    print("\nDone!")

if __name__ == "__main__":
    main()