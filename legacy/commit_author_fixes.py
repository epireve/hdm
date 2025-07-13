#!/usr/bin/env python3
"""
Commit the author fixes and handle duplicates.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fix_critical_issues import CriticalIssuesFixer
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def commit_author_fixes_and_handle_duplicates():
    """Commit author fixes and handle duplicate papers."""
    logger.info("Committing author fixes and handling duplicates...")
    
    fixer = CriticalIssuesFixer()
    
    # 1. Apply author fixes
    print(f"🔧 APPLYING AUTHOR FIXES...")
    results = fixer.fix_author_extractions(commit_changes=True)
    print(f"✅ Applied {results['fixes_applied']} author fixes")
    
    # 2. Handle the shen_2020 duplicate specifically
    print(f"\n🔄 HANDLING SHEN_2020 DUPLICATE...")
    handle_shen_duplicate()
    
    # 3. Mark other obvious duplicates for review
    print(f"\n🔍 MARKING OTHER DUPLICATES...")
    mark_duplicate_papers()
    
    print(f"\n✅ Author fixes committed and duplicates handled")

def handle_shen_duplicate():
    """Handle the specific shen_2020 duplicate case."""
    conn = sqlite3.connect('hdm_papers.db')
    cursor = conn.cursor()
    
    # Get the two shen papers
    cursor.execute("""
        SELECT id, cite_key, title, authors, doi, url
        FROM papers 
        WHERE cite_key IN ('chen_2023', 'shen_2020')
        ORDER BY cite_key
    """)
    
    papers = cursor.fetchall()
    
    if len(papers) == 2:
        # Keep the one with better metadata (chen_2023 has DOI)
        keep_paper = papers[0]  # chen_2023
        remove_paper = papers[1]  # shen_2020
        
        logger.info(f"Keeping {keep_paper[1]} (has DOI), marking {remove_paper[1]} for removal")
        
        # Add a note about the duplicate
        cursor.execute("""
            UPDATE papers 
            SET yaml_notes = 'DUPLICATE: Same paper as chen_2023 - marked for removal'
            WHERE id = ?
        """, (remove_paper[0],))
        
        conn.commit()
        print(f"   ✅ Marked {remove_paper[1]} as duplicate of {keep_paper[1]}")
    
    conn.close()

def mark_duplicate_papers():
    """Mark other clear duplicate papers."""
    conn = sqlite3.connect('hdm_papers.db')
    cursor = conn.cursor()
    
    # Find papers with identical titles
    cursor.execute("""
        SELECT title, GROUP_CONCAT(cite_key) as cite_keys, COUNT(*) as count
        FROM papers 
        WHERE title IS NOT NULL AND title != ''
        GROUP BY LOWER(TRIM(title))
        HAVING COUNT(*) > 1
        ORDER BY count DESC
        LIMIT 10
    """)
    
    duplicates = cursor.fetchall()
    marked_count = 0
    
    for title, cite_keys_str, count in duplicates:
        cite_keys = cite_keys_str.split(',')
        
        if count == 2:  # Handle simple pairs first
            # Keep the first one alphabetically, mark the second
            keep_key = cite_keys[0]
            remove_key = cite_keys[1]
            
            cursor.execute("""
                UPDATE papers 
                SET yaml_notes = COALESCE(yaml_notes || '; ', '') || 'DUPLICATE: Same title as ' || ?
                WHERE cite_key = ?
            """, (keep_key, remove_key))
            
            marked_count += 1
            print(f"   📋 Marked {remove_key} as duplicate of {keep_key}")
    
    conn.commit()
    conn.close()
    
    print(f"   ✅ Marked {marked_count} duplicate papers")

if __name__ == "__main__":
    commit_author_fixes_and_handle_duplicates()