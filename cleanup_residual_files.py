#!/usr/bin/env python3
"""
Clean up residual test files and temporary directories that are causing GitHub Actions issues.
"""

import os
import shutil
import glob
from pathlib import Path

def cleanup_residual_files():
    """Remove all temporary, test, and backup files."""
    
    # Directories to remove
    dirs_to_remove = [
        # Test directories
        'test_*',
        'enhanced_reformatted_papers_*',
        'production_reformatted_*',
        'production_enhanced_*',
        'production_unique_*',
        'production_simple_*',
        'production_final_reformatted_*',
        
        # Cache directories
        '__pycache__',
        '.pytest_cache',
        '.mypy_cache',
        
        # Other temporary directories
        'paper_backups',
        'inbox',
        'output',
    ]
    
    # Files to remove
    files_to_remove = [
        # Log files
        '*.log',
        
        # Backup database files
        'hdm_papers_backup_*.db',
        
        # Temporary files
        '.DS_Store',
        
        # Sensitive files that shouldn't be in repo
        '.env',
        '.claude/settings.local.json',
        
        # Old files
        'research_table_old.md.bak',
        'Pesonalised PKG Paperguide compiled.xlsx',
        'paper_reformatter_plan.md',
        'REFORMATTER_STATUS.md',
        'reformatter_log_*.log',
        'yaml_frontmatter_analysis_report.md',
        'yaml_to_database_extraction.log',
    ]
    
    print("🧹 CLEANING UP RESIDUAL FILES")
    print("=" * 50)
    
    removed_dirs = 0
    removed_files = 0
    
    # Remove directories
    for pattern in dirs_to_remove:
        for path in glob.glob(pattern):
            if os.path.isdir(path):
                try:
                    shutil.rmtree(path)
                    print(f"🗂️  Removed directory: {path}")
                    removed_dirs += 1
                except Exception as e:
                    print(f"❌ Failed to remove {path}: {e}")
    
    # Remove files
    for pattern in files_to_remove:
        for path in glob.glob(pattern):
            if os.path.isfile(path):
                try:
                    os.remove(path)
                    print(f"📄 Removed file: {path}")
                    removed_files += 1
                except Exception as e:
                    print(f"❌ Failed to remove {path}: {e}")
    
    # Remove .claude directory if it exists
    claude_dir = Path('.claude')
    if claude_dir.exists():
        try:
            shutil.rmtree('.claude')
            print(f"🗂️  Removed directory: .claude")
            removed_dirs += 1
        except Exception as e:
            print(f"❌ Failed to remove .claude: {e}")
    
    print(f"\n📊 CLEANUP SUMMARY:")
    print(f"   Directories removed: {removed_dirs}")
    print(f"   Files removed: {removed_files}")
    
    return removed_dirs + removed_files

def update_gitignore():
    """Update .gitignore to prevent future issues."""
    
    additional_ignores = """

# Test and temporary directories
test_*/
production_*/
enhanced_*/
backups/
paper_backups/
output/
inbox/

# Log files
*.log

# Database backups
*_backup_*.db

# Sensitive files
.env
.claude/

# Cache directories
__pycache__/
.pytest_cache/
.mypy_cache/

# System files
.DS_Store
Thumbs.db

# IDE files
.vscode/
.idea/

# Temporary processing files
*_reformatted_*/
*_checkpoint.json
reformatter_log_*.log
yaml_to_database_extraction.log
yaml_frontmatter_analysis_report.md

# Large Excel files
*.xlsx
"""
    
    gitignore_path = Path('.gitignore')
    current_content = ""
    
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            current_content = f.read()
    
    # Only add if not already present
    if "# Test and temporary directories" not in current_content:
        with open(gitignore_path, 'a') as f:
            f.write(additional_ignores)
        print("✅ Updated .gitignore with additional exclusions")
    else:
        print("✅ .gitignore already contains necessary exclusions")

def check_large_files():
    """Check for large files that might cause upload issues."""
    
    print(f"\n🔍 CHECKING FOR LARGE FILES:")
    print("=" * 50)
    
    large_files = []
    
    for root, dirs, files in os.walk('.'):
        # Skip git directory
        if '.git' in root:
            continue
            
        for file in files:
            filepath = os.path.join(root, file)
            try:
                size = os.path.getsize(filepath)
                # Flag files larger than 10MB
                if size > 10 * 1024 * 1024:
                    large_files.append((filepath, size))
            except OSError:
                continue
    
    if large_files:
        print("⚠️  Large files found (>10MB):")
        for filepath, size in sorted(large_files, key=lambda x: x[1], reverse=True):
            size_mb = size / (1024 * 1024)
            print(f"   {filepath}: {size_mb:.1f}MB")
    else:
        print("✅ No large files found")
    
    return large_files

def main():
    """Main cleanup execution."""
    
    # Step 1: Clean up residual files
    total_removed = cleanup_residual_files()
    
    # Step 2: Update .gitignore
    update_gitignore()
    
    # Step 3: Check for large files
    large_files = check_large_files()
    
    print(f"\n🎯 CLEANUP COMPLETE!")
    print(f"   Total items removed: {total_removed}")
    print(f"   Large files found: {len(large_files)}")
    
    if large_files:
        print(f"\n💡 Consider moving large files to .gitignore or external storage")
    
    print(f"\n📝 NEXT STEPS:")
    print(f"1. Review changes: git status")
    print(f"2. Commit cleanup: git add . && git commit -m 'Clean up residual test files'")
    print(f"3. Push to GitHub: git push")
    print(f"4. GitHub Actions should work without artifact upload errors")

if __name__ == "__main__":
    main()