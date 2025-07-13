#!/bin/bash
# Build static site data from SQLite database

echo "🔧 Building static site data..."

# Export database to JSON files
echo "📊 Exporting database to static JSON..."
python scripts/export_to_static_json.py

# Check if export was successful
if [ $? -eq 0 ]; then
    echo "✅ Static data built successfully!"
    echo "📁 JSON files saved to: data/"
    echo ""
    echo "🌐 To serve the site locally, run:"
    echo "   python -m http.server 8080"
    echo ""
    echo "Then open: http://localhost:8080/literature_review_static.html"
else
    echo "❌ Failed to export data!"
    exit 1
fi