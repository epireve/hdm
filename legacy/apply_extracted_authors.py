#!/usr/bin/env python3
"""
Apply the extracted author information from Task agent to the database.
"""

import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def apply_extracted_authors():
    """Apply the extracted authors to the database."""
    
    # Author extractions from Task agent analysis
    extracted_authors = {
        'cinti_2024': 'Caterina Cinti, Maria Giovanna Trivella, Michael Joulie, Hussein Ayoub, Monika Frenzel',
        'charles_2022': 'Charles W., Aussenac-Gilles N., Hernandez N.',
        'chen_2024b': 'Shan Chen, Shuyue Stella Li, Kumail Alhamoud, Jimin Mun, Cristina Grau, Minseok Jung, Rodrigo Gameiro, Lizhou Fan, Eugene Park, Tristan Lin, Wonjin Yoon, Maarten Sap, Yulia Tsvetkov, Paul Liang, Xuhai Xu, Xin Liu, Hyeonhoon Lee, Hae Won Park, Cynthia Breazeal',
        'kalmuk_2024': 'David Kalmuk, Kostas Rakopoulos, Robert C. Hooper, Patrick Perez, Daniel C. Zilio, Christian Garcia-Arellano, Hamdi Roumani, Matthew Emmerton, Aleksandrs Santars, Imran Sayyid, Krishna K. Ramachandran, Ronald Barber, William Minor, Zach Hoggard, Michael Chen, Humphrey Li, Yiren Shen, Richard Sidle, Alexander Cheung, Scott Walkty, Matthew Olan, Ketan Rampurkar',
        'li_2022': 'Zhiding Li, Chenqi Shang, Jianjie Wu, Yuan Li',
        'martinez_2022': 'Roberto Martinez-Maldonado, Vanessa Echeverria, Gloria Fernandez-Nieto, Lixiang Yan, Linxuan Zhao, Riordan Alfredo, Xinyu Li, Samantha Dix, Hollie Jaggard, Rosie Wotherspoon, Abra Osborne, Simon Buckingham Shum, Dragan Gašević',
        
        # Additional fixes from our previous analysis
        'challenges_2021': 'Xin Peng, Chong Wang, Mingwei Li',
        'isws_2019': 'ISWS Technical Report Team',
        'chen_2023c': 'Li Yitong',
        'fu_2023': 'Weihao Fu',
        'hendawi_2024': 'Rasha Hendawi',
        'geng_2014': 'Rushan Geng, Cuicui Luo',
        'driskell_2021': 'Tripp Driskell, Eduardo Salas, C. Shawn Burke, James E. Driskell',
        'papachristou_2024': 'Panagiotis Papachristou',
        'chang_2025': 'Jee Suk Chang',
        'kessel_2024': 'Marcus Kessel',
        'buzi_2024': 'Authors unknown',  # Since file not found
    }
    
    conn = sqlite3.connect('hdm_papers.db')
    cursor = conn.cursor()
    
    updated_count = 0
    not_found_count = 0
    
    print(f"\n🔧 APPLYING EXTRACTED AUTHORS TO DATABASE")
    print(f"=" * 60)
    
    for cite_key, authors in extracted_authors.items():
        # Try to find the paper by cite_key
        cursor.execute("SELECT id, authors FROM papers WHERE cite_key = ?", (cite_key,))
        result = cursor.fetchone()
        
        if result:
            paper_id, current_authors = result
            
            # Update the authors field
            cursor.execute("""
                UPDATE papers 
                SET authors = ?
                WHERE id = ?
            """, (authors, paper_id))
            
            updated_count += 1
            print(f"✅ {cite_key}")
            print(f"   Before: {current_authors[:80]}..." if current_authors else "   Before: NO AUTHORS")
            print(f"   After:  {authors}")
        else:
            not_found_count += 1
            print(f"❌ {cite_key} - NOT FOUND IN DATABASE")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print(f"\n📊 AUTHOR UPDATE SUMMARY:")
    print(f"   Papers updated: {updated_count}")
    print(f"   Papers not found: {not_found_count}")
    print(f"   Total processed: {len(extracted_authors)}")
    
    return updated_count

def verify_author_improvements():
    """Verify the improvements made to author data."""
    conn = sqlite3.connect('hdm_papers.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check for remaining problematic authors
    cursor.execute("""
        SELECT cite_key, title, authors
        FROM papers 
        WHERE 
            -- Still problematic patterns
            authors LIKE '%check for updates%' OR
            authors LIKE '%additional key words%' OR
            authors LIKE '%.edu.%' OR
            authors LIKE '%@%' OR
            authors LIKE '%university%' OR
            authors LIKE '%institute%' OR
            authors LIKE '%systems group%' OR
            authors LIKE '%digital humanities%' OR
            authors LIKE '%mechatronic engineering%' OR
            authors LIKE '%his majesty%' OR
            authors LIKE '%.surnam%' OR
            LENGTH(authors) > 200 OR
            -- Very short/suspicious authors
            (authors IS NOT NULL AND LENGTH(TRIM(authors)) < 3)
        ORDER BY cite_key
    """)
    
    remaining_problems = cursor.fetchall()
    
    print(f"\n🔍 VERIFICATION RESULTS:")
    print(f"   Remaining problematic papers: {len(remaining_problems)}")
    
    if remaining_problems:
        print(f"\n⚠️  STILL NEED ATTENTION:")
        for paper in remaining_problems[:10]:  # Show first 10
            cite_key = paper['cite_key']
            title = paper['title'][:50] + "..." if paper['title'] else "NO TITLE"
            authors = paper['authors'][:60] + "..." if paper['authors'] else "NO AUTHORS"
            print(f"   {cite_key}: {authors}")
    else:
        print(f"✅ All major author extraction issues resolved!")
    
    # Overall statistics
    cursor.execute("SELECT COUNT(*) FROM papers WHERE authors IS NOT NULL AND authors != ''")
    papers_with_authors = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM papers")
    total_papers = cursor.fetchone()[0]
    
    author_coverage = (papers_with_authors / total_papers) * 100
    
    print(f"\n📈 OVERALL AUTHOR STATISTICS:")
    print(f"   Papers with authors: {papers_with_authors}/{total_papers} ({author_coverage:.1f}%)")
    
    conn.close()
    
    return len(remaining_problems)

def main():
    """Execute author extraction application."""
    logger.info("Applying extracted authors to database...")
    
    # Apply the extracted authors
    updated_count = apply_extracted_authors()
    
    # Verify improvements
    remaining_issues = verify_author_improvements()
    
    print(f"\n✅ AUTHOR EXTRACTION APPLICATION COMPLETE")
    print(f"   Papers updated: {updated_count}")
    print(f"   Remaining issues: {remaining_issues}")
    
    if remaining_issues == 0:
        print(f"🎉 All major author extraction issues have been resolved!")
    else:
        print(f"📝 {remaining_issues} papers still need manual review")

if __name__ == "__main__":
    main()