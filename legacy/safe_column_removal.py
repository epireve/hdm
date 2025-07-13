#!/usr/bin/env python3
"""
Safely remove the downloaded column and update any dependent views.
"""

import sqlite3
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def remove_downloaded_column_safely():
    """Safely remove the downloaded column and handle dependent views."""
    
    conn = sqlite3.connect('hdm_papers.db')
    cursor = conn.cursor()
    
    try:
        # Step 1: Drop dependent views
        logger.info("Dropping dependent views...")
        cursor.execute("DROP VIEW IF EXISTS papers_summary")
        cursor.execute("DROP VIEW IF EXISTS papers_statistics")
        
        # Step 2: Get current table structure
        cursor.execute("PRAGMA table_info(papers)")
        columns_info = cursor.fetchall()
        
        # Build new table structure without 'downloaded' column
        new_columns = []
        for col_info in columns_info:
            col_name = col_info[1]
            if col_name != 'downloaded':
                new_columns.append(col_name)
        
        logger.info(f"Keeping {len(new_columns)} columns, removing 'downloaded'")
        
        # Step 3: Create new table without downloaded column
        new_columns_str = ', '.join(new_columns)
        cursor.execute(f"""
            CREATE TABLE papers_new AS 
            SELECT {new_columns_str} FROM papers
        """)
        
        # Step 4: Drop old table and rename new one
        cursor.execute("DROP TABLE papers")
        cursor.execute("ALTER TABLE papers_new RENAME TO papers")
        
        # Step 5: Recreate indexes
        logger.info("Recreating indexes...")
        cursor.execute("CREATE UNIQUE INDEX idx_cite_key ON papers(cite_key)")
        cursor.execute("CREATE INDEX idx_old_cite_key ON papers(old_cite_key)")
        cursor.execute("CREATE INDEX idx_year ON papers(year)")
        cursor.execute("CREATE INDEX idx_relevancy ON papers(relevancy)")
        cursor.execute("CREATE INDEX idx_tags ON papers(tags)")
        cursor.execute("CREATE INDEX idx_date_processed ON papers(date_processed)")
        
        # Step 6: Recreate trigger
        logger.info("Recreating trigger...")
        cursor.execute("""
            CREATE TRIGGER update_papers_timestamp 
            AFTER UPDATE ON papers
            BEGIN
                UPDATE papers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        """)
        
        # Step 7: Recreate views without downloaded column
        logger.info("Recreating views...")
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
        
        cursor.execute("""
            CREATE VIEW papers_statistics AS
            SELECT 
                COUNT(*) as total_papers,
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
        
        # Step 8: Commit all changes
        conn.commit()
        
        # Step 9: Verify the changes
        cursor.execute("PRAGMA table_info(papers)")
        final_columns = [row[1] for row in cursor.fetchall()]
        
        cursor.execute("SELECT COUNT(*) FROM papers")
        record_count = cursor.fetchone()[0]
        
        logger.info(f"Successfully removed 'downloaded' column")
        logger.info(f"Final table has {len(final_columns)} columns and {record_count} records")
        logger.info(f"Downloaded column present: {'downloaded' in final_columns}")
        
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error during column removal: {e}")
        conn.rollback()
        conn.close()
        return False

def main():
    """Main function to safely remove downloaded column."""
    logger.info("Starting safe removal of 'downloaded' column...")
    
    if remove_downloaded_column_safely():
        print("✅ Successfully removed 'downloaded' column and updated views")
        return True
    else:
        print("❌ Failed to remove 'downloaded' column")
        return False

if __name__ == "__main__":
    main()