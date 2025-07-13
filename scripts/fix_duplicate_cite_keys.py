#!/usr/bin/env python3
"""
Fix duplicate cite keys in the database by adding alphabetic suffixes
"""

import sqlite3
from pathlib import Path

def fix_duplicates(db_path="hdm_papers.db"):
    """Fix duplicate cite keys by adding suffixes"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # First, let's identify all the duplicates from the original CSV
    cursor.execute("""
        SELECT old_cite_key, COUNT(*) as count
        FROM papers
        WHERE old_cite_key IS NOT NULL
        GROUP BY old_cite_key
        HAVING count > 1
        ORDER BY count DESC
    """)
    
    duplicate_old_keys = cursor.fetchall()
    print(f"Found {len(duplicate_old_keys)} duplicate old cite keys")
    
    # Get all unique cite keys that are causing conflicts
    cursor.execute("""
        SELECT cite_key, COUNT(*) as count
        FROM papers
        GROUP BY cite_key
        HAVING count > 1
        ORDER BY count DESC
    """)
    
    duplicate_new_keys = cursor.fetchall()
    print(f"Found {len(duplicate_new_keys)} duplicate new cite keys in database")
    
    # For each duplicate, we need to add suffixes
    for cite_key, count in duplicate_new_keys:
        print(f"\nProcessing duplicate: {cite_key} (appears {count} times)")
        
        # Get all papers with this cite_key
        cursor.execute("""
            SELECT id, title, authors, year, old_cite_key
            FROM papers
            WHERE cite_key = ?
            ORDER BY id
        """, (cite_key,))
        
        papers = cursor.fetchall()
        
        # Keep the first one as is, add suffixes to others
        for i, (paper_id, title, authors, year, old_key) in enumerate(papers):
            if i == 0:
                print(f"  Keeping: {cite_key} - {title[:50]}...")
                continue
            
            # Generate suffix (a, b, c, etc.)
            suffix = chr(ord('a') + i - 1)
            new_cite_key = f"{cite_key}{suffix}"
            
            # Update the paper
            cursor.execute("""
                UPDATE papers
                SET cite_key = ?, 
                    folder_path = REPLACE(folder_path, ?, ?)
                WHERE id = ?
            """, (new_cite_key, cite_key, new_cite_key, paper_id))
            
            print(f"  Updated: {cite_key} → {new_cite_key} - {title[:50]}...")
    
    conn.commit()
    
    # Verify no more duplicates
    cursor.execute("""
        SELECT cite_key, COUNT(*) as count
        FROM papers
        GROUP BY cite_key
        HAVING count > 1
    """)
    
    remaining = cursor.fetchall()
    if remaining:
        print(f"\n⚠️  Still have {len(remaining)} duplicates!")
    else:
        print(f"\n✅ All duplicates resolved!")
    
    # Show final statistics
    cursor.execute("SELECT COUNT(*) FROM papers")
    total = cursor.fetchone()[0]
    print(f"\n📊 Total papers in database: {total}")
    
    conn.close()

if __name__ == "__main__":
    base_dir = Path("/Users/invoture/dev.local/hdm")
    db_path = base_dir / "hdm_papers.db"
    fix_duplicates(db_path)