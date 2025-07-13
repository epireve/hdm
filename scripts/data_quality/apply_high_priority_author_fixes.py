#!/usr/bin/env python3
"""
Apply high priority author fixes based on investigation findings.
"""

import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def apply_high_priority_fixes():
    """Apply the high priority author fixes recommended by Task agent."""
    
    # High priority author fixes from Task agent analysis
    high_priority_fixes = {
        'callahan_2024': 'Tifany J. Callahan, Ignacio J. Tripodi, Adrianne L. Stefanski, Luca Cappelletti, Sanya B. Taneja, Jordan M. Wyrwa, Elena Casiraghi, Nicolas A. Matentzoglu, Justin Reese, Jonathan C. Silverstein, Charles Tapley Hoyt, Richard D. Boyce, Scott A. Malec, Deepak R. Unni, Marcin P. Joachimiak, Peter N. Robinson, Christopher J. Mungall, Emanuele Cavalleri, Tommaso Fontana, Giorgio Valentini, Marco Mesiti, Lucas A. Gillenwater, Brook Santangelo, Nicole A. Vasilevsky, Robert Hoehndorf, Tellen D. Bennett, Patrick B. Ryan, George Hripcsak, Michael G. Kahn, Michael Bada, William A. Baumgartner Jr, Lawrence E. Hunter',
        'koutsoubis_2024': 'Nikolas Koutsoubis, Yasin Yilmaz, Ravi P. Ramachandran, Matthew Schabath, Ghulam Rasool',
        'wu_2022': 'Chuhan Wu, Fangzhao Wu, Yang Cao, Yongfeng Huang, Xing Xie',
        'carriero_2021': 'Valentina Anita Carriero, Aldo Gangemi, Maria Letizia Mancinelli, Ludovica Marinucci, Andrea Giovanni Nuzzolese, Valentina Presutti, Chiara Veninata',
        'science_2022': 'Li Gang, Wang Hong, Liu Hong',
        
        # Additional institutional contamination fixes
        'martínez-garcía_2022': 'Authors unknown',  # No clear authors in institutional text
        'xie_2022a': 'Xing Xie',  # Remove institutional contamination
        
        # Fix some obvious formatting issues
        'chen_2023': 'Xuemin Shen',  # Remove "(Sherman)" and "Fellow, IEEE"
        'shen_2020': 'Xuemin Shen',  # Same fix
        'plailly_2019': 'J. Plailly, M. Villalba, R. Vallat, A. Nicolas, P. Ruby',  # Remove &
        'zhanga_2024': 'Yang Zhang, Hanlei Jin, Dan Meng, Jun Wang, Jinghua Tan',  # Remove numbers/typos
        
        # Fix reference citation that's not authors
        'mohamed_2023': 'Saher Mohamed, Kirollos Farah, Abdelrahman Lotfy, Kareem Rizk',  # Extract from title
    }
    
    conn = sqlite3.connect('hdm_papers.db')
    cursor = conn.cursor()
    
    updated_count = 0
    
    print(f"\n🔧 APPLYING HIGH PRIORITY AUTHOR FIXES")
    print(f"=" * 70)
    
    for cite_key, correct_authors in high_priority_fixes.items():
        cursor.execute("SELECT id, authors FROM papers WHERE cite_key = ?", (cite_key,))
        result = cursor.fetchone()
        
        if result:
            paper_id, current_authors = result
            
            # Update the authors field
            cursor.execute("UPDATE papers SET authors = ? WHERE id = ?", (correct_authors, paper_id))
            updated_count += 1
            
            print(f"✅ {cite_key}")
            print(f"   Before: {current_authors[:80]}..." if current_authors and len(current_authors) > 80 else f"   Before: {current_authors}")
            print(f"   After:  {correct_authors[:80]}..." if len(correct_authors) > 80 else f"   After:  {correct_authors}")
        else:
            print(f"❌ {cite_key} - NOT FOUND IN DATABASE")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print(f"\n📊 HIGH PRIORITY FIXES SUMMARY:")
    print(f"   Papers updated: {updated_count}")
    
    return updated_count

def verify_improvements():
    """Verify the improvements made."""
    conn = sqlite3.connect('hdm_papers.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check for remaining institutional contamination
    cursor.execute("""
        SELECT COUNT(*) FROM papers 
        WHERE (authors LIKE '%university%' 
           OR authors LIKE '%institute%'
           OR authors LIKE '%corporation%'
           OR authors LIKE '%research%'
           OR authors LIKE '%center%'
           OR authors LIKE '%laboratory%') 
        AND authors != 'Authors unknown'
        AND LENGTH(authors) < 150  -- Exclude very long author lists
    """)
    institutional_issues = cursor.fetchone()[0]
    
    # Check for formatting issues
    cursor.execute("""
        SELECT COUNT(*) FROM papers 
        WHERE (authors LIKE '%fellow%'
           OR authors LIKE '%IEEE%'
           OR authors LIKE '%editors%'
           OR authors LIKE '%review%'
           OR authors LIKE '%URL:%'
           OR authors LIKE '%@%'
           OR authors LIKE '%&%')
        AND authors != 'Authors unknown'
    """)
    formatting_issues = cursor.fetchone()[0]
    
    # Overall quality check
    cursor.execute("SELECT COUNT(*) FROM papers")
    total_papers = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM papers WHERE authors = 'Authors unknown'")
    unknown_authors = cursor.fetchone()[0]
    
    real_authors = total_papers - unknown_authors
    quality_percentage = (real_authors / total_papers) * 100
    
    print(f"\n📊 POST-FIX VERIFICATION:")
    print(f"   Total papers: {total_papers}")
    print(f"   Papers with real authors: {real_authors} ({quality_percentage:.1f}%)")
    print(f"   Papers marked 'Authors unknown': {unknown_authors}")
    print(f"   Remaining institutional contamination: {institutional_issues}")
    print(f"   Remaining formatting issues: {formatting_issues}")
    
    total_remaining_issues = institutional_issues + formatting_issues
    
    if total_remaining_issues == 0:
        print(f"\n🎉 EXCELLENT! All high priority issues have been resolved!")
    else:
        print(f"\n⚠️  {total_remaining_issues} minor issues remain")
    
    # Show some examples of remaining issues if any
    if institutional_issues > 0:
        cursor.execute("""
            SELECT cite_key, authors FROM papers 
            WHERE (authors LIKE '%university%' 
               OR authors LIKE '%institute%'
               OR authors LIKE '%corporation%') 
            AND authors != 'Authors unknown'
            AND LENGTH(authors) < 150
            LIMIT 3
        """)
        remaining = cursor.fetchall()
        
        if remaining:
            print(f"\n🔍 EXAMPLES OF REMAINING INSTITUTIONAL ISSUES:")
            for paper in remaining:
                cite_key = paper['cite_key']
                authors = paper['authors'][:80] + "..." if len(paper['authors']) > 80 else paper['authors']
                print(f"   {cite_key}: {authors}")
    
    conn.close()
    
    return {
        'total_papers': total_papers,
        'quality_percentage': quality_percentage,
        'institutional_issues': institutional_issues,
        'formatting_issues': formatting_issues,
        'total_remaining': total_remaining_issues
    }

def main():
    """Execute high priority author fixes."""
    logger.info("Applying high priority author fixes...")
    
    # Apply fixes
    updated_count = apply_high_priority_fixes()
    
    # Verify improvements
    stats = verify_improvements()
    
    print(f"\n✅ HIGH PRIORITY AUTHOR FIXES COMPLETE!")
    print(f"   Papers updated: {updated_count}")
    print(f"   Final quality: {stats['quality_percentage']:.1f}%")
    print(f"   Remaining issues: {stats['total_remaining']}")
    
    if stats['total_remaining'] <= 5:
        print(f"🏆 EXCELLENT! Author data is now at very high quality!")
    elif stats['total_remaining'] <= 15:
        print(f"👍 GOOD! Most issues resolved, minor cleanup remaining")
    else:
        print(f"📝 Progress made, but more work needed")

if __name__ == "__main__":
    main()