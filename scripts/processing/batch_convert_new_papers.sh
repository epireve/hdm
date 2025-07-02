#\!/bin/bash

echo "Starting batch conversion of new papers..."

# Run the converter multiple times with timeout
for i in {1..10}; do
    echo "Run $i - Starting converter..."
    timeout 120 python convert_new_papers.py
    
    # Check remaining papers
    python -c "
import json
with open('new_papers_checkpoint.json') as f:
    checkpoint = json.load(f)
total = 55
done = len(checkpoint['completed']) + len(checkpoint.get('failed', {})) + len(checkpoint.get('skipped', []))
print(f'Progress: {done}/{total}')
if done >= total:
    exit(1)
"
    if [ $? -eq 1 ]; then
        echo "All papers processed\!"
        break
    fi
    sleep 2
done

# Show final status
python -c "
import json
from pathlib import Path
with open('new_papers_checkpoint.json') as f:
    checkpoint = json.load(f)
print(f'\\nTotal converted: {len(checkpoint[\"completed\"])}')
print(f'Failed: {len(checkpoint.get(\"failed\", {}))}')
if checkpoint['completed']:
    print('\\nLast 10 converted:')
    for pdf in checkpoint['completed'][-10:]:
        print(f'  - {Path(pdf).stem}')
"
EOF < /dev/null