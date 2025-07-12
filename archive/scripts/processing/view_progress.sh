#!/bin/bash

echo "Real-time Progress Monitor for Relevancy Analysis"
echo "================================================="
echo ""

while true; do
    # Get the last 10 lines from the log that show progress
    progress_lines=$(grep -E "Progress|Processing paper.*\[.*%.*\]|=== Progress Update ===" scripts/processing/relevancy_analysis.log | tail -15)
    
    # Clear screen and show progress
    clear
    echo "Real-time Progress Monitor for Relevancy Analysis"
    echo "================================================="
    echo ""
    echo "Latest activity:"
    echo "$progress_lines"
    echo ""
    echo "Last update: $(date)"
    echo ""
    echo "Press Ctrl+C to stop monitoring"
    
    sleep 5
done