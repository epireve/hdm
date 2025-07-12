#!/bin/bash

echo "==================================="
echo "Image Description Progress Monitor"
echo "==================================="

# Get latest log file
LOG_FILE=$(ls -t logs/phase2/image_descriptor_csv_*.log | head -1)

if [ -z "$LOG_FILE" ]; then
    echo "No log file found"
    exit 1
fi

echo "Monitoring: $LOG_FILE"
echo ""

# Function to get latest stats
get_stats() {
    # Get latest progress line
    PROGRESS=$(tail -1000 "$LOG_FILE" | grep "Progress:" | tail -1)
    
    # Get totals
    TOTAL_PAPERS=$(echo "$PROGRESS" | grep -oE "Progress: [0-9]+/([0-9]+)" | cut -d'/' -f2)
    CURRENT=$(echo "$PROGRESS" | grep -oE "Progress: ([0-9]+)/" | cut -d':' -f2 | cut -d'/' -f1)
    PERCENT=$(echo "$PROGRESS" | grep -oE "\([0-9.]+%\)" | tr -d '(%)')
    ETA=$(echo "$PROGRESS" | grep -oE "ETA: [0-9]+:[0-9]+" | cut -d' ' -f2)
    
    # Count images described
    IMAGES_DESCRIBED=$(tail -1000 "$LOG_FILE" | grep "Added.*image descriptions" | \
                      grep -oE "Added [0-9]+" | awk '{sum+=$2} END {print sum}')
    
    if [ -z "$IMAGES_DESCRIBED" ]; then
        IMAGES_DESCRIBED=0
    fi
    
    echo "Progress: $CURRENT / $TOTAL_PAPERS papers ($PERCENT)"
    echo "Images described so far: ~$IMAGES_DESCRIBED"
    echo "ETA: $ETA"
    echo ""
    
    # Show last 5 processed papers
    echo "Recently processed:"
    tail -1000 "$LOG_FILE" | grep "Added.*image descriptions" | tail -5 | \
        sed 's/.*Added \([0-9]*\) image descriptions to: \(.*\)/  - \2 (\1 images)/'
}

# Initial display
get_stats

# Monitor continuously
echo ""
echo "Press Ctrl+C to stop monitoring"
echo "-----------------------------------"

while true; do
    sleep 30
    clear
    echo "==================================="
    echo "Image Description Progress Monitor"
    echo "==================================="
    echo "Updated: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    get_stats
done