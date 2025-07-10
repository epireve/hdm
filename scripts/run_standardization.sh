#!/bin/bash

# Script to run standardization in small batches to avoid timeouts

echo "Starting batch standardization process..."
echo "This will process all papers in batches of 5"
echo ""

# Get total papers to process
total_papers=$(ls -d markdown_papers/*/ | wc -l)
echo "Total paper directories: $total_papers"

# Check current progress
if [ -f "standardization_progress.json" ]; then
    completed=$(grep -o '"completed"' standardization_progress.json | wc -l)
    echo "Already completed: check standardization_progress.json"
fi

echo ""
echo "Processing in batches of 5 papers..."
echo "Press Ctrl+C to stop at any time (progress is saved)"
echo ""

# Process in batches
batch_num=1
while true; do
    echo "=========================================="
    echo "Batch $batch_num starting..."
    echo "=========================================="
    
    # Run batch of 5
    python scripts/standardize_papers_batch.py --limit 5
    
    # Check if there are more papers to process
    if grep -q '"completed"' standardization_progress.json; then
        completed_count=$(python -c "import json; print(len(json.load(open('standardization_progress.json'))['completed']))")
        echo ""
        echo "Progress: $completed_count papers completed"
        
        # Check if we've processed all papers (rough estimate)
        if [ "$completed_count" -ge "$((total_papers - 10))" ]; then
            echo "Batch processing appears to be complete or nearly complete!"
            echo "Check standardization_progress.json for details"
            break
        fi
    fi
    
    echo ""
    echo "Waiting 5 seconds before next batch..."
    sleep 5
    
    batch_num=$((batch_num + 1))
done

echo ""
echo "Batch processing finished!"
echo "Final report:"
python -c "
import json
with open('standardization_progress.json') as f:
    data = json.load(f)
    print(f'Completed: {len(data[\"completed\"])} papers')
    print(f'Failed: {len(data[\"failed\"])} papers')
    if data['failed']:
        print('\\nFailed papers:')
        for k, v in data['failed'].items():
            print(f'  - {k}: {v}')
"