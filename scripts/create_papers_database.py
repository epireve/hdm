#!/usr/bin/env python3
"""
Create SQLite database for HDM papers with comprehensive schema
"""

import sqlite3
from pathlib import Path
from datetime import datetime

def create_database(db_path="hdm_papers.db"):
    """Create SQLite database with papers schema"""
    
    # Remove existing database if it exists
    db_file = Path(db_path)
    if db_file.exists():
        print(f"⚠️  Removing existing database: {db_path}")
        db_file.unlink()
    
    # Create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create papers table with all fields from CSV
    cursor.execute("""
    CREATE TABLE papers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cite_key TEXT UNIQUE NOT NULL,
        old_cite_key TEXT,
        title TEXT NOT NULL,
        authors TEXT,
        year INTEGER,
        downloaded TEXT,
        relevancy TEXT,
        relevancy_justification TEXT,
        insights TEXT,
        tldr TEXT,
        summary TEXT,
        research_question TEXT,
        methodology TEXT,
        key_findings TEXT,
        primary_outcomes TEXT,
        limitations TEXT,
        conclusion TEXT,
        research_gaps TEXT,
        future_work TEXT,
        implementation_insights TEXT,
        url TEXT,
        doi TEXT,
        tags TEXT,
        date_processed DATE,
        folder_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create indexes for better performance
    indexes = [
        "CREATE INDEX idx_cite_key ON papers(cite_key)",
        "CREATE INDEX idx_old_cite_key ON papers(old_cite_key)",
        "CREATE INDEX idx_year ON papers(year)",
        "CREATE INDEX idx_relevancy ON papers(relevancy)",
        "CREATE INDEX idx_tags ON papers(tags)",
        "CREATE INDEX idx_downloaded ON papers(downloaded)",
        "CREATE INDEX idx_date_processed ON papers(date_processed)"
    ]
    
    for index in indexes:
        cursor.execute(index)
        print(f"✅ Created index: {index.split(' ')[2]}")
    
    # Create trigger to update timestamp
    cursor.execute("""
    CREATE TRIGGER update_papers_timestamp 
    AFTER UPDATE ON papers
    BEGIN
        UPDATE papers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;
    """)
    
    # Create a view for easy querying
    cursor.execute("""
    CREATE VIEW papers_summary AS
    SELECT 
        id,
        cite_key,
        old_cite_key,
        title,
        authors,
        year,
        relevancy,
        downloaded,
        tldr,
        tags,
        folder_path,
        CASE 
            WHEN url IS NOT NULL AND url != '' THEN 1 
            ELSE 0 
        END as has_url,
        CASE 
            WHEN doi IS NOT NULL AND doi != '' THEN 1 
            ELSE 0 
        END as has_doi,
        created_at,
        updated_at
    FROM papers
    """)
    
    # Create statistics view
    cursor.execute("""
    CREATE VIEW papers_statistics AS
    SELECT 
        COUNT(*) as total_papers,
        COUNT(CASE WHEN downloaded = 'Yes' THEN 1 END) as downloaded_count,
        COUNT(CASE WHEN relevancy = 'SUPER' THEN 1 END) as super_relevancy_count,
        COUNT(CASE WHEN relevancy = 'HIGH' THEN 1 END) as high_relevancy_count,
        COUNT(CASE WHEN relevancy = 'MEDIUM' THEN 1 END) as medium_relevancy_count,
        COUNT(CASE WHEN relevancy = 'LOW' THEN 1 END) as low_relevancy_count,
        MIN(year) as min_year,
        MAX(year) as max_year,
        COUNT(DISTINCT LOWER(relevancy)) as relevancy_levels,
        COUNT(CASE WHEN url IS NOT NULL AND url != '' THEN 1 END) as papers_with_url,
        COUNT(CASE WHEN doi IS NOT NULL AND doi != '' THEN 1 END) as papers_with_doi,
        COUNT(CASE WHEN tags IS NOT NULL AND tags != '' THEN 1 END) as papers_with_tags
    FROM papers
    """)
    
    # Commit changes
    conn.commit()
    
    print(f"\n✅ Database created successfully: {db_path}")
    print(f"📊 Tables created: papers")
    print(f"👁️  Views created: papers_summary, papers_statistics")
    print(f"🔧 Trigger created: update_papers_timestamp")
    
    # Show database info
    cursor.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table', 'view', 'index')")
    objects = cursor.fetchall()
    
    print(f"\n📋 Database objects:")
    for name, obj_type in objects:
        if not name.startswith('sqlite_'):
            print(f"   - {obj_type}: {name}")
    
    conn.close()
    return db_path

if __name__ == "__main__":
    create_database()