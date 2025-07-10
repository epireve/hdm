#!/usr/bin/env python3
"""
Fix titles that are in all uppercase to proper title case
"""

import os
import re
import string

def to_title_case(text):
    """Convert text to proper title case, handling special cases"""
    
    # Articles, conjunctions, and prepositions that should be lowercase (unless at start)
    lowercase_words = {
        'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'in', 'nor', 'of', 'on', 
        'or', 'so', 'the', 'to', 'up', 'yet', 'with', 'from', 'into', 'onto', 'upon',
        'via', 'vs', 'vs.', 'versus'
    }
    
    # Words that should stay uppercase
    uppercase_words = {
        'AI', 'API', 'APIs', 'IoT', 'ML', 'NLP', 'LLM', 'LLMs', 'PKG', 'KG', 'EHR', 
        'HTTP', 'HTTPS', 'URL', 'URLs', 'XML', 'JSON', 'SQL', 'HTML', 'CSS', 'RDF',
        'GDP', 'CEO', 'CTO', 'PhD', 'MSc', 'BSc', 'USA', 'UK', 'EU', 'WHO', 'FDA',
        'COVID', 'COVID-19', 'SARS', 'HIV', 'DNA', 'RNA', 'GPS', 'GIS', 'TCP', 'UDP',
        'SPARQL', 'W3C', 'IEEE', 'ACM', 'ISBN', 'DOI', 'ISSN', 'ORCID'
    }
    
    # Split into words while preserving punctuation
    words = re.findall(r'\S+', text)
    result_words = []
    
    for i, word in enumerate(words):
        # Extract the actual word part (remove punctuation for analysis)
        word_clean = re.sub(r'[^\w\'-]', '', word)
        
        if not word_clean:
            result_words.append(word)
            continue
            
        # Check if it's an uppercase acronym that should stay uppercase
        if word_clean.upper() in uppercase_words:
            # Preserve the acronym but fix the punctuation case
            result_word = word_clean.upper()
            # Add back any punctuation
            punctuation = re.sub(r'[\w\'-]', '', word)
            result_words.append(result_word + punctuation)
        
        # Check if first word or after certain punctuation (always capitalize)
        elif i == 0 or any(p in words[i-1] for p in [':', '?', '!', '.']):
            result_words.append(word.capitalize())
        
        # Check if it's a small word that should be lowercase
        elif word_clean.lower() in lowercase_words:
            result_words.append(word.lower())
        
        # Default: capitalize first letter, lowercase the rest
        else:
            result_words.append(word.capitalize())
    
    return ' '.join(result_words)

def fix_title_case(content):
    """Fix title case in markdown content"""
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        if line.startswith('title:'):
            # Extract the title part
            title_part = line[6:].strip()
            
            # Check if title is mostly uppercase (more than 50% uppercase letters)
            alpha_chars = [c for c in title_part if c.isalpha()]
            if alpha_chars:
                uppercase_ratio = sum(1 for c in alpha_chars if c.isupper()) / len(alpha_chars)
                
                # If more than 70% uppercase, convert to title case
                if uppercase_ratio > 0.7:
                    fixed_title = to_title_case(title_part)
                    fixed_lines.append(f'title: {fixed_title}')
                    print(f"Fixed title: {title_part} -> {fixed_title}")
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def process_file(file_path):
    """Process a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed_content = fix_title_case(content)
        
        if fixed_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all markdown files"""
    base_dir = "/Users/invoture/dev.local/hdm/markdown_papers"
    
    if not os.path.exists(base_dir):
        print(f"Directory not found: {base_dir}")
        return
    
    print("=== UPPERCASE TITLE CASE FIX ===")
    print("Converting uppercase titles to proper title case...")
    print()
    
    files_processed = 0
    files_updated = 0
    
    # Find all markdown files
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                files_processed += 1
                
                if process_file(file_path):
                    files_updated += 1
                
                if files_processed % 50 == 0:
                    print(f"Processed {files_processed} files...")
    
    print(f"\n=== SUMMARY ===")
    print(f"Total files processed: {files_processed}")
    print(f"Files updated: {files_updated}")
    print(f"Files unchanged: {files_processed - files_updated}")

if __name__ == "__main__":
    main()