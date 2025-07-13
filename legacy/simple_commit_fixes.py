#!/usr/bin/env python3
"""
Simple commit of author fixes without complex duplicate handling.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fix_critical_issues import CriticalIssuesFixer
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def simple_commit_fixes():
    """Simply commit the author fixes."""
    logger.info("Committing author fixes...")
    
    fixer = CriticalIssuesFixer()
    
    # Apply author fixes
    results = fixer.fix_author_extractions(commit_changes=True)
    
    print(f"✅ AUTHOR FIXES COMMITTED")
    print(f"=" * 50)
    print(f"Fixes applied: {results['fixes_applied']}/{results['total_fixes_available']}")
    
    # Show what was fixed
    print(f"\n🔧 FIXED PAPERS:")
    for cite_key, fix_data in fixer.fixes.items():
        print(f"   {cite_key}: {fix_data['correct_authors']}")
    
    return True

if __name__ == "__main__":
    simple_commit_fixes()