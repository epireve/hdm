#!/usr/bin/env python3
"""
Fix the last remaining author extraction issue.
"""

import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_last_issue():
    """Fix the last remaining author issue."""
    
    conn = sqlite3.connect('hdm_papers.db')
    cursor = conn.cursor()
    
    # Fix the posillico_2024 paper
    cursor.execute("SELECT id, authors FROM papers WHERE cite_key = 'posillico_2024'")
    result = cursor.fetchone()
    
    if result:
        paper_id, current_authors = result
        clean_authors = "John J. Posillico"  # Remove "His Majesty"
        
        cursor.execute("UPDATE papers SET authors = ? WHERE id = ?", (clean_authors, paper_id))
        
        print(f"✅ Fixed posillico_2024:")
        print(f"   Before: {current_authors}")
        print(f"   After:  {clean_authors}")
        
        conn.commit()
        logger.info("Fixed last remaining author issue")
    else:
        print("❌ posillico_2024 not found")
    
    conn.close()

def final_verification_after_fix():
    """Run final verification after the fix."""
    
    conn = sqlite3.connect('hdm_papers.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check for any remaining actual problems
    cursor.execute("""
        SELECT COUNT(*) FROM papers 
        WHERE (authors LIKE '%check for updates%' 
           OR authors LIKE '%additional key words%'
           OR authors LIKE '%@%'
           OR authors LIKE '%.edu%'
           OR authors LIKE '%his majesty%'
           OR authors LIKE '%systems group%'
           OR authors LIKE '%.surnam%'
           OR (authors LIKE '%university%' AND LENGTH(authors) < 100))
        AND authors != 'Authors unknown'
    """)
    actual_problems = cursor.fetchone()[0]
    
    # Overall stats
    cursor.execute("SELECT COUNT(*) FROM papers")
    total_papers = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM papers WHERE authors = 'Authors unknown'")
    unknown_authors = cursor.fetchone()[0]
    
    real_authors = total_papers - unknown_authors
    quality_score = (real_authors / total_papers) * 100
    
    print(f"\n🏆 FINAL VERIFICATION AFTER FIX:")
    print(f"=" * 60)
    print(f"Total papers: {total_papers}")
    print(f"Papers with real authors: {real_authors} ({quality_score:.1f}%)")
    print(f"Papers marked 'Authors unknown': {unknown_authors}")
    print(f"ACTUAL problematic extractions: {actual_problems}")
    
    # Success criteria
    all_good = (
        quality_score >= 98.0 and
        actual_problems == 0 and
        unknown_authors <= 5 and
        total_papers == 358
    )
    
    print(f"\n🎯 SUCCESS CRITERIA:")
    print(f"   ✅ 100% coverage: {'PASS' if total_papers == 358 else 'FAIL'}")
    print(f"   ✅ ≥98% real authors: {'PASS' if quality_score >= 98.0 else 'FAIL'}")
    print(f"   ✅ No extraction problems: {'PASS' if actual_problems == 0 else 'FAIL'}")
    print(f"   ✅ ≤5 'Authors unknown': {'PASS' if unknown_authors <= 5 else 'FAIL'}")
    
    if all_good:
        print(f"\n🎉 🎉 🎉 MISSION ACCOMPLISHED! 🎉 🎉 🎉")
        print(f"🏆 PERFECT AUTHOR EXTRACTION ACHIEVED!")
        print(f"📊 Final Stats: {quality_score:.1f}% quality, 0 issues, {unknown_authors} unknown")
        print(f"🚀 Database is ready for production research use!")
    else:
        print(f"\n⚠️  Still have issues to resolve")
    
    conn.close()
    return all_good

def main():
    """Fix last issue and verify."""
    logger.info("Fixing last author extraction issue...")
    
    fix_last_issue()
    success = final_verification_after_fix()
    
    if success:
        print(f"\n✅ Author extraction project SUCCESSFULLY COMPLETED!")
    else:
        print(f"\n❌ Still have work to do")

if __name__ == "__main__":
    main()