# Static Site Setup for GitHub Pages

This project now supports a fully static approach for GitHub Pages without requiring Flask or any server-side processing.

## Overview

The literature review page can now load data from pre-generated static JSON files instead of requiring a Flask API server. This makes it perfect for hosting on GitHub Pages or any static file hosting service.

## Files

- `literature_review_static.html` - Static version of the literature review page
- `data/` directory contains all JSON data files:
  - `papers.json` - All paper data
  - `statistics.json` - Aggregated statistics
  - `years.json` - List of all years
  - `relevancy.json` - Relevancy level counts
  - `index.json` - Index file with metadata

## Building Static Data

To regenerate the static JSON files from the SQLite database:

```bash
# Run the build script
./scripts/build_static_site.sh

# Or run the export script directly
python scripts/export_to_static_json.py
```

## Serving Locally

To test the static site locally:

```bash
# Using Python's built-in server
python -m http.server 8080

# Then open in browser
# http://localhost:8080/literature_review_static.html
```

## Workflow

1. **Update Database**: Make changes to the SQLite database using existing scripts
2. **Export to JSON**: Run `./scripts/build_static_site.sh` to export data
3. **Commit Changes**: Commit both the database and JSON files
4. **Push to GitHub**: The static site will work automatically on GitHub Pages

## Advantages

- **No server required**: Works on any static hosting (GitHub Pages, Netlify, etc.)
- **Fast loading**: JSON files are cached by browsers
- **Offline capable**: Once loaded, works without internet
- **Version controlled**: All data is in git
- **Simple deployment**: Just push to GitHub

## Data Size

Current data export size: ~0.9 MB (very reasonable for modern web)

## Updating from CSV

If you need to reimport from CSV:

```bash
# 1. Migrate CSV to SQLite
python scripts/migrate_csv_to_sqlite.py

# 2. Export to static JSON
python scripts/export_to_static_json.py
```

## Future Enhancements

- Add search functionality using client-side search libraries
- Implement data compression if size becomes an issue
- Add incremental updates to avoid regenerating all data
- Create automated GitHub Actions to rebuild on database changes