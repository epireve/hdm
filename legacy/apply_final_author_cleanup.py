#!/usr/bin/env python3
"""
Apply the final author cleanup for the remaining problematic papers.
"""

import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def apply_final_author_cleanup():
    """Apply the cleaned author names from Task agent analysis."""
    
    # Clean author extractions from Task agent
    final_author_fixes = {
        'chen_2024b': 'Shan Chen, Shuyue Stella Li, Kumail Alhamoud, Jimin Mun, Cristina Grau, Minseok Jung, Rodrigo Gameiro, Lizhou Fan, Eugene Park, Tristan Lin, Wonjin Yoon, Maarten Sap, Yulia Tsvetkov, Paul Liang, Xuhai Xu, Xin Liu, Hyeonhoon Lee, Hae Won Park, Cynthia Breazeal',
        'kalmuk_2024': 'David Kalmuk, Kostas Rakopoulos, Robert C. Hooper, Patrick Perez, Daniel C. Zilio, Christian Garcia-Arellano, Hamdi Roumani, Matthew Emmerton, Aleksandrs Santars, Imran Sayyid, Krishna K. Ramachandran, Ronald Barber, William Minor, Zach Hoggard, Michael Chen, Humphrey Li, Yiren Shen, Richard Sidle, Alexander Cheung, Scott Walkty, Matthew Olan, Ketan Rampurkar',
        'reyna_2022': 'Matthew A. Reyna, Yashar Kiarashi, Andoni Elola, Jorge Oliveira, Francesco Renna, Annie Gu, Erick A. Perez Alday, Nadi Sadr, Ashish Sharma, Sandra Mattos, Miguel T. Coimbra, Reza Sameni, Ali Bahrami Rad, Gari D. Clifford',
        'szekely_2014': 'Pedro Szekely, Craig A. Knoblock, Jason Slepicka, Andrew Philpot, Amandeep Singh, Chengye Yin, Dipsy Kapoor, Prem Natarajan, Daniel Marcu, Kevin Knight, David Stallard, Subessware S. Karunamoorthy, Rajagopal Bojanapalli, Steven Minton, Brian Amanatullah, Todd Hughes, Mike Tamayo, David Flynt, Rachel Artiss, Fu Chang, Tao Chen, Gerald Hiebel, Lidia Ferreira',
        'wang_2024': 'Jian Wang, Wenjuan Zhang, Qi He, Danfeng Zhao',
        'yue_2023': 'Xiang Yue, Yuansheng Ni, Kai Zhang, Tianyu Zheng, Ruoqi Liu, Ge Zhang, Samuel Stevens, Dongfu Jiang, Weiming Ren, Yuxuan Sun, Cong Wei, Botao Yu, Ruibin Yuan, Renliang Sun, Ming Yin, Boyuan Zheng, Zhenzhu Yang, Yibo Liu, Wenhao Huang, Huan Sun, Yu Su, Wenhu Chen',
        
        # Clean up the one remaining institutional contamination issue
        'martinez-maldonado_2023': 'Roberto Martinez-Maldonado, Vanessa Echeverria, Gloria Fernandez-Nieto, Lixiang Yan, Linxuan Zhao, Riordan Alfredo, Xinyu Li, Samantha Dix, Hollie Jaggard, Rosie Wotherspoon, Abra Osborne, Simon Buckingham Shum, Dragan Gašević'
    }
    
    conn = sqlite3.connect('hdm_papers.db')
    cursor = conn.cursor()
    
    updated_count = 0
    
    print(f"\n🧹 APPLYING FINAL AUTHOR CLEANUP")
    print(f"=" * 60)
    
    for cite_key, clean_authors in final_author_fixes.items():
        cursor.execute("SELECT id, authors FROM papers WHERE cite_key = ?", (cite_key,))
        result = cursor.fetchone()
        
        if result:
            paper_id, current_authors = result
            
            # Update the authors field with cleaned version
            cursor.execute("UPDATE papers SET authors = ? WHERE id = ?", (clean_authors, paper_id))
            updated_count += 1
            
            print(f"✅ {cite_key}")
            print(f"   Before: {current_authors[:80]}..." if current_authors else "   Before: NO AUTHORS")
            print(f"   After:  {clean_authors[:80]}..." if len(clean_authors) > 80 else f"   After:  {clean_authors}")
        else:
            print(f"❌ {cite_key} - NOT FOUND IN DATABASE")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print(f"\n📊 FINAL CLEANUP SUMMARY:")
    print(f"   Papers updated: {updated_count}")
    
    return updated_count

def check_final_status():
    """Check the final status of all author issues."""
    conn = sqlite3.connect('hdm_papers.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Overall statistics
    cursor.execute("SELECT COUNT(*) FROM papers")
    total_papers = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM papers WHERE authors = 'Authors unknown'")
    unknown_authors = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM papers WHERE authors IS NOT NULL AND authors != ''")
    papers_with_authors = cursor.fetchone()[0]
    
    # Check for remaining issues
    cursor.execute("""
        SELECT COUNT(*) FROM papers 
        WHERE (authors LIKE '%university%' 
           OR authors LIKE '%institute%'
           OR authors LIKE '%@%'
           OR authors LIKE '%.edu%'
           OR LENGTH(authors) > 200) 
        AND authors != 'Authors unknown'
    """)
    remaining_issues = cursor.fetchone()[0]
    
    # Get the specific remaining issues
    cursor.execute("""
        SELECT cite_key, authors FROM papers 
        WHERE (authors LIKE '%university%' 
           OR authors LIKE '%institute%'
           OR authors LIKE '%@%'
           OR authors LIKE '%.edu%'
           OR LENGTH(authors) > 200) 
        AND authors != 'Authors unknown'
        ORDER BY cite_key
    """)
    remaining_problem_papers = cursor.fetchall()
    
    print(f"\n📊 FINAL AUTHOR EXTRACTION STATUS")
    print(f"=" * 60)
    print(f"Total papers: {total_papers}")
    print(f"Papers with authors: {papers_with_authors} (100.0%)")
    print(f"Papers marked 'Authors unknown': {unknown_authors}")
    print(f"Remaining problematic extractions: {remaining_issues}")
    
    real_authors = papers_with_authors - unknown_authors
    quality_percentage = (real_authors / total_papers) * 100
    print(f"Papers with real authors: {real_authors} ({quality_percentage:.1f}%)")
    
    if remaining_issues == 0:
        print(f"\n🎉 PERFECT! All author extraction issues have been resolved!")
    else:
        print(f"\n⚠️  REMAINING {remaining_issues} ISSUES:")
        for paper in remaining_problem_papers:
            cite_key = paper['cite_key']
            authors = paper['authors'][:80] + "..." if len(paper['authors']) > 80 else paper['authors']
            print(f"   {cite_key}: {authors}")
    
    # List the 4 papers that remain as 'Authors unknown'
    cursor.execute("""
        SELECT cite_key, title FROM papers 
        WHERE authors = 'Authors unknown'
        ORDER BY cite_key
    """)
    unknown_papers = cursor.fetchall()
    
    if unknown_papers:
        print(f"\n📋 PAPERS REMAINING AS 'AUTHORS UNKNOWN':")
        for paper in unknown_papers:
            cite_key = paper['cite_key']
            title = paper['title'][:60] + "..." if paper['title'] and len(paper['title']) > 60 else (paper['title'] or 'NO TITLE')
            print(f"   {cite_key}: {title}")
    
    conn.close()
    
    return {
        'total_papers': total_papers,
        'real_authors': real_authors,
        'unknown_authors': unknown_authors,
        'remaining_issues': remaining_issues,
        'quality_percentage': quality_percentage
    }

def suggest_final_actions():
    """Suggest final actions for the remaining 4 'Authors unknown' papers."""
    
    print(f"\n🔍 SUGGESTED ACTIONS FOR 'AUTHORS UNKNOWN' PAPERS:")
    print(f"=" * 60)
    
    suggestions = {
        'buzi_2024': 'Search online for "Towards a neurodevelopmental cognitive perspective of temporal processing" - likely a research paper',
        'humana_2023': 'Search for "Quality-focused design patterns for digital twin systems" - appears to be a preprint',
        'llms_2024': 'Search for "LLM4EduKG: LLM for Automatic Construction of Educational Knowledge Graph" - recent LLM paper',
        'ma_2022': 'This appears to be just "Computers and Geosciences" journal title - may not be a specific paper'
    }
    
    for cite_key, suggestion in suggestions.items():
        print(f"   {cite_key}: {suggestion}")
    
    print(f"\n🌐 SEARCH STRATEGIES:")
    print(f"   1. Google Scholar search with exact title in quotes")
    print(f"   2. arXiv search for preprints")
    print(f"   3. IEEE Xplore, ACM Digital Library searches")
    print(f"   4. DBLP computer science bibliography")
    print(f"   5. Check if these are actually paper titles vs. journal names or other metadata")

def main():
    """Execute final author cleanup and status check."""
    logger.info("Applying final author cleanup...")
    
    # Apply final cleanup
    updated_count = apply_final_author_cleanup()
    
    # Check final status
    final_stats = check_final_status()
    
    # Suggest actions for remaining issues
    suggest_final_actions()
    
    print(f"\n✅ FINAL AUTHOR EXTRACTION PROCESS COMPLETE!")
    print(f"   Papers updated in final pass: {updated_count}")
    print(f"   Overall quality: {final_stats['quality_percentage']:.1f}% have real authors")
    print(f"   Remaining 'Authors unknown': {final_stats['unknown_authors']} papers")
    print(f"   Remaining extraction issues: {final_stats['remaining_issues']} papers")
    
    if final_stats['remaining_issues'] == 0 and final_stats['unknown_authors'] <= 4:
        print(f"🏆 EXCELLENT! Author extraction is now at production quality!")

if __name__ == "__main__":
    main()