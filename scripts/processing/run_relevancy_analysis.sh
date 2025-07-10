#!/bin/bash

# Script to run relevancy analysis on research papers

echo "Relevancy Analysis Script for HDM Research Papers"
echo "================================================"
echo ""

# Check if KiloCode token is set
if [ -z "$KILOCODE_TOKEN" ]; then
    # Check if .env file exists
    if [ -f "../../.env" ] && grep -q "KILOCODE_TOKEN" "../../.env"; then
        echo "KiloCode token found in .env file"
    else
        echo "Error: KILOCODE_TOKEN not found."
        echo ""
        echo "To set up KiloCode:"
        echo "1. Create a .env file in the project root"
        echo "2. Add: KILOCODE_TOKEN='your-token-here'"
        echo "3. Get your token from: https://kilocode.ai/auth/signin"
        echo ""
        exit 1
    fi
fi

# Display options
echo "Options:"
echo "  1. Run test mode (process only 5 papers)"
echo "  2. Run full processing (all papers with missing values)"
echo "  3. Show statistics only"
echo ""

# Function to show statistics
show_stats() {
    echo "Analyzing current CSV file..."
    python3 -c "
import csv

with open('../../research_papers_complete.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

total = len(rows)
missing_rel = sum(1 for r in rows if not r.get('Relevancy', '').strip() or r.get('Relevancy', '').lower() in ['', 'none', 'null'])
missing_just = sum(1 for r in rows if not r.get('Relevancy Justification', '').strip() or r.get('Relevancy Justification', '').lower() in ['', 'none', 'null', 'not available'])

print(f'Total papers: {total}')
print(f'Missing Relevancy: {missing_rel}')
print(f'Missing Relevancy Justification: {missing_just}')
print(f'Total needing processing: {max(missing_rel, missing_just)}')
"
}

# Read user choice
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Running in TEST MODE..."
        cd ../../
        python3 scripts/processing/complete_relevancy_analysis.py --test
        ;;
    2)
        echo ""
        echo "Running FULL processing..."
        echo "This will process all papers with missing relevancy data."
        read -p "Are you sure? (y/n): " confirm
        if [ "$confirm" == "y" ]; then
            cd ../../
            python3 scripts/processing/complete_relevancy_analysis.py
        else
            echo "Cancelled."
        fi
        ;;
    3)
        echo ""
        show_stats
        ;;
    *)
        echo "Invalid choice."
        exit 1
        ;;
esac

echo ""
echo "Done!"