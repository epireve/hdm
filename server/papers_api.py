#!/usr/bin/env python3
"""
Flask API to serve papers data from SQLite database
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from pathlib import Path
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database path
DB_PATH = Path(__file__).parent.parent / "hdm_papers.db"

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

@app.route('/api/papers', methods=['GET'])
def get_papers():
    """Get all papers with optional filtering"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build query with filters
    query = "SELECT * FROM papers WHERE 1=1"
    params = []
    
    # Filter by relevancy
    relevancy = request.args.get('relevancy')
    if relevancy:
        query += " AND UPPER(relevancy) = UPPER(?)"
        params.append(relevancy)
    
    # Filter by year
    year = request.args.get('year')
    if year:
        query += " AND year = ?"
        params.append(int(year))
    
    # Filter by tags (contains search)
    tags = request.args.get('tags')
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',')]
        for tag in tag_list:
            query += " AND LOWER(tags) LIKE ?"
            params.append(f"%{tag.lower()}%")
    
    # Sort by year descending by default
    sort_by = request.args.get('sort', 'year')
    sort_order = request.args.get('order', 'desc')
    
    if sort_by in ['year', 'title', 'relevancy', 'cite_key']:
        query += f" ORDER BY {sort_by} {sort_order.upper()}"
    
    cursor.execute(query, params)
    papers = cursor.fetchall()
    
    # Convert to list of dicts
    result = []
    for paper in papers:
        paper_dict = dict(paper)
        # Add markdown and viewer links
        if paper_dict['cite_key']:
            paper_dict['markdown_link'] = f"markdown_papers/{paper_dict['cite_key']}/paper.md"
            paper_dict['viewer_link'] = f"paper_viewer.html?id={paper_dict['cite_key']}"
        result.append(paper_dict)
    
    conn.close()
    
    return jsonify({
        'papers': result,
        'count': len(result)
    })

@app.route('/api/papers/<cite_key>', methods=['GET'])
def get_paper(cite_key):
    """Get a specific paper by cite_key"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM papers WHERE cite_key = ?", (cite_key,))
    paper = cursor.fetchone()
    
    if paper:
        paper_dict = dict(paper)
        if paper_dict['cite_key']:
            paper_dict['markdown_link'] = f"markdown_papers/{paper_dict['cite_key']}/paper.md"
            paper_dict['viewer_link'] = f"paper_viewer.html?id={paper_dict['cite_key']}"
        conn.close()
        return jsonify(paper_dict)
    else:
        conn.close()
        return jsonify({'error': 'Paper not found'}), 404

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get paper statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM papers_statistics")
    stats = cursor.fetchone()
    
    # Get year distribution
    cursor.execute("""
        SELECT year, COUNT(*) as count 
        FROM papers 
        WHERE year IS NOT NULL 
        GROUP BY year 
        ORDER BY year
    """)
    year_dist = cursor.fetchall()
    
    # Get tag cloud data
    cursor.execute("""
        SELECT tags FROM papers WHERE tags IS NOT NULL AND tags != ''
    """)
    all_tags = cursor.fetchall()
    
    # Process tags
    tag_counts = {}
    for row in all_tags:
        tags = row['tags'].split(',')
        for tag in tags:
            tag = tag.strip()
            if tag:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    # Sort tags by count
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    
    conn.close()
    
    return jsonify({
        'statistics': dict(stats),
        'year_distribution': [dict(row) for row in year_dist],
        'top_tags': top_tags
    })

@app.route('/api/years', methods=['GET'])
def get_years():
    """Get all unique years"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT year 
        FROM papers 
        WHERE year IS NOT NULL 
        ORDER BY year DESC
    """)
    years = [row['year'] for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify(years)

@app.route('/api/export', methods=['GET'])
def export_papers():
    """Export papers in various formats"""
    format_type = request.args.get('format', 'json')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM papers ORDER BY year DESC, cite_key")
    papers = cursor.fetchall()
    
    if format_type == 'csv':
        # Generate CSV
        import csv
        import io
        
        output = io.StringIO()
        
        if papers:
            writer = csv.DictWriter(output, fieldnames=papers[0].keys())
            writer.writeheader()
            for paper in papers:
                writer.writerow(dict(paper))
        
        conn.close()
        
        response = app.response_class(
            output.getvalue(),
            mimetype='text/csv',
            headers={"Content-disposition": "attachment; filename=hdm_papers_export.csv"}
        )
        return response
    
    else:
        # Default to JSON
        result = [dict(paper) for paper in papers]
        conn.close()
        return jsonify(result)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM papers")
        count = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'papers_count': count
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    print(f"📚 HDM Papers API Server")
    print(f"📁 Database: {DB_PATH}")
    print(f"🌐 Starting server on http://localhost:5000")
    print(f"\nEndpoints:")
    print(f"  GET /api/papers - Get all papers with filtering")
    print(f"  GET /api/papers/<cite_key> - Get specific paper")
    print(f"  GET /api/statistics - Get statistics")
    print(f"  GET /api/years - Get all years")
    print(f"  GET /api/export?format=json|csv - Export data")
    print(f"  GET /api/health - Health check")
    
    app.run(debug=True, port=5000)