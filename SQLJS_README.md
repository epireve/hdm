# SQLite on GitHub Pages with sql.js

This solution allows you to use SQLite databases directly on GitHub Pages without any server-side processing.

## How It Works

The `literature_review_sqljs.html` page uses **sql.js**, a JavaScript implementation of SQLite compiled to WebAssembly. This allows the browser to read and query SQLite database files directly.

## Features

- **Pure Client-Side**: Everything runs in the browser - no server needed
- **Full SQL Support**: Run any SQLite query directly in JavaScript
- **GitHub Pages Compatible**: Works perfectly on static hosting
- **Performance**: SQLite is fast, and sql.js is optimized for browser use
- **No Build Step**: Just commit your `.db` file and HTML

## Files

- `literature_review_sqljs.html` - The main page that loads and queries the SQLite database
- `hdm_papers.db` - Your SQLite database file (served as static file)
- Uses sql.js from CDN (no local dependencies needed)

## Usage

1. **Access the page**:
   ```
   http://localhost:8080/literature_review_sqljs.html
   ```

2. **How it works**:
   - The page loads sql.js from CDN
   - Fetches `hdm_papers.db` as a binary file
   - Loads it into sql.js
   - Runs SQL queries directly in the browser
   - All filtering and sorting happens client-side

## Updating the Database

When you need to update the data:

1. Update your SQLite database using existing Python scripts
2. Commit the updated `hdm_papers.db` file
3. Push to GitHub - the changes are immediately live

```bash
# Example workflow
python scripts/migrate_csv_to_sqlite.py
git add hdm_papers.db
git commit -m "Update papers database"
git push
```

## Performance Considerations

- **Initial Load**: The entire database is loaded into memory (currently ~1-2MB)
- **Caching**: Browsers cache the .db file, so repeat visits are fast
- **Query Speed**: SQL queries run at native speed in WebAssembly

## Advantages Over JSON

1. **No Build Step**: No need to export to JSON files
2. **Full SQL Power**: Complex queries, joins, aggregations work naturally
3. **Single Source**: The .db file is the single source of truth
4. **Smaller Size**: SQLite files are often smaller than equivalent JSON

## Browser Compatibility

sql.js works in all modern browsers that support WebAssembly:
- Chrome 57+
- Firefox 52+
- Safari 11+
- Edge 16+

## Advanced Usage

You can run any SQL query directly:

```javascript
// Example: Get papers by year with author count
const result = db.exec(`
    SELECT year, COUNT(*) as count, 
           GROUP_CONCAT(DISTINCT authors) as all_authors
    FROM papers 
    WHERE year >= 2020
    GROUP BY year 
    ORDER BY year DESC
`);
```

## Limitations

- **Read-Only**: Changes made in the browser aren't saved back to the file
- **File Size**: Larger databases (>10MB) may be slow to load initially
- **No Server Features**: Can't use server-side features like user authentication

## Security

- The database is publicly accessible (like any file on GitHub Pages)
- Don't store sensitive data in the database
- sql.js runs in a sandboxed environment

## Future Enhancements

- Add client-side full-text search using SQLite FTS
- Implement IndexedDB caching for faster repeat loads
- Add export functionality (to CSV, JSON)
- Create a query builder UI for advanced searches