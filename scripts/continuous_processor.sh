#!/bin/bash

# Continuous processor for all papers
# Runs batch processor repeatedly until all papers are processed

echo "🚀 Starting continuous paper processing..."
echo "This will process all remaining papers automatically"
echo "Press Ctrl+C to stop at any time"
echo ""

completed_count=0
iteration=1

while true; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔄 Iteration $iteration"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Get current count
    completed_count=$(python3 -c "import json; print(len(json.load(open('standardization_progress.json'))['completed']))")
    failed_count=$(python3 -c "import json; print(len(json.load(open('standardization_progress.json'))['failed']))")
    
    echo "📊 Current Status: $completed_count/359 completed"
    echo "📋 Remaining: $failed_count papers to process"
    
    if [ "$failed_count" -eq 0 ]; then
        echo "🎉 ALL PAPERS PROCESSED!"
        break
    fi
    
    # Run batch processor
    timeout 300 python3 scripts/batch_process_large_papers.py
    
    # Check new count
    new_count=$(python3 -c "import json; print(len(json.load(open('standardization_progress.json'))['completed']))")
    processed=$((new_count - completed_count))
    
    echo "✅ Processed $processed papers in this iteration"
    
    # Brief pause
    echo "⏸️  Pausing 5 seconds..."
    sleep 5
    
    iteration=$((iteration + 1))
    
    # Safety check - stop after 100 iterations
    if [ "$iteration" -gt 100 ]; then
        echo "⚠️  Safety limit reached (100 iterations)"
        break
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🏁 PROCESSING COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Final status
python3 -c "
import json
with open('standardization_progress.json') as f:
    data = json.load(f)
completed = len(data['completed'])
failed = len(data['failed'])
print(f'✅ Total Completed: {completed}/359 papers ({(completed/359)*100:.1f}%)')
print(f'❌ Failed: {failed} papers')
"