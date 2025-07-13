#!/usr/bin/env python3
"""
Batch script to update cite_keys non-interactively.
"""

import sqlite3
import json
import re
from pathlib import Path

def update_cite_keys():
    conn = sqlite3.connect('hdm_papers.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Find papers where the year in cite_key doesn't match actual year
    cursor.execute("""
        SELECT cite_key, year, title, authors, corrected_cite_key
        FROM papers
        WHERE cite_key LIKE '%_20%'
        ORDER BY cite_key
    """)
    
    papers = cursor.fetchall()
    corrections_needed = []
    
    for paper in papers:
        cite_key = paper['cite_key']
        actual_year = paper['year']
        
        # Extract year from cite_key
        match = re.search(r'(.+?)_(\d{4})([a-z]?)$', cite_key)
        if match:
            base_name = match.group(1)
            cite_key_year = int(match.group(2))
            suffix = match.group(3)
            
            if cite_key_year != actual_year:
                # Need to create new cite_key
                new_cite_key = f"{base_name}_{actual_year}{suffix}"
                
                # Check if this would create a duplicate
                cursor.execute(
                    "SELECT COUNT(*) FROM papers WHERE cite_key = ? OR corrected_cite_key = ?",
                    (new_cite_key, new_cite_key)
                )
                
                if cursor.fetchone()[0] > 0:
                    # Would create duplicate, add suffix
                    for letter in 'abcdefghijklmnopqrstuvwxyz':
                        test_key = f"{base_name}_{actual_year}{letter}"
                        cursor.execute(
                            "SELECT COUNT(*) FROM papers WHERE cite_key = ? OR corrected_cite_key = ?",
                            (test_key, test_key)
                        )
                        if cursor.fetchone()[0] == 0:
                            new_cite_key = test_key
                            break
                
                corrections_needed.append({
                    'cite_key': cite_key,
                    'new_cite_key': new_cite_key,
                    'year': actual_year,
                    'title': paper['title'][:60] + '...'
                })
    
    # Apply corrections
    updated_count = 0
    for correction in corrections_needed:
        cursor.execute("""
            UPDATE papers 
            SET corrected_cite_key = ? 
            WHERE cite_key = ?
        """, (correction['new_cite_key'], correction['cite_key']))
        
        if cursor.rowcount > 0:
            updated_count += 1
            print(f"✅ {correction['cite_key']} → {correction['new_cite_key']}")
    
    conn.commit()
    conn.close()
    
    print(f"\n📊 Updated {updated_count} corrected_cite_keys")
    return updated_count

if __name__ == "__main__":
    update_cite_keys()