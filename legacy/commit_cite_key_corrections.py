#!/usr/bin/env python3
"""
Commit the cite_key corrections to database after review.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hybrid_cite_key_corrector import HybridCiteKeyCorrector
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def commit_corrections():
    """Commit the cite_key corrections to database."""
    logger.info("Committing cite_key corrections to database...")
    
    corrector = HybridCiteKeyCorrector()
    
    # Apply corrections with commit=True
    results = corrector.apply_hybrid_corrections(commit_changes=True)
    
    # Verify the changes
    conn = sqlite3.connect('hdm_papers.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM papers WHERE corrected_cite_key IS NOT NULL")
    corrected_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM papers WHERE cite_key != corrected_cite_key")
    different_count = cursor.fetchone()[0]
    
    # Sample some corrections for verification
    cursor.execute("""
        SELECT cite_key, corrected_cite_key, authors 
        FROM papers 
        WHERE cite_key != corrected_cite_key 
        ORDER BY cite_key 
        LIMIT 10
    """)
    sample_corrections = cursor.fetchall()
    
    conn.close()
    
    print(f"\n✅ CITE_KEY CORRECTIONS COMMITTED")
    print(f"="*50)
    print(f"Total papers with corrected_cite_key: {corrected_count}")
    print(f"Papers with different cite_keys: {different_count}")
    print(f"Manual overrides: {results['manual_corrections']}")
    print(f"Algorithmic corrections: {results['algorithmic_corrections']}")
    
    print(f"\n📋 SAMPLE COMMITTED CORRECTIONS:")
    for cite_key, corrected, authors in sample_corrections:
        print(f"   {cite_key} → {corrected}")
        print(f"     {authors[:60]}...")
    
    return True

if __name__ == "__main__":
    commit_corrections()