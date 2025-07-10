#!/usr/bin/env python3
"""
Generate updated research_table_with_citekeys.md from the latest HDM CSV file
"""

import pandas as pd
from pathlib import Path
import re

def clean_text(text):
    """Clean text for markdown table"""
    if pd.isna(text):
        return ""
    # Convert to string and clean
    text = str(text).strip()
    # Remove newlines and extra spaces
    text = re.sub(r'\s+', ' ', text)
    # Escape pipe characters
    text = text.replace('|', '\\|')
    return text

def truncate_text(text, max_length=500):
    """Truncate text to maximum length"""
    if len(text) > max_length:
        return text[:max_length-3] + "..."
    return text

def main():
    """Generate research table from latest CSV"""
    # Find the latest HDM CSV file
    base_dir = Path(__file__).parent.parent
    csv_files = list(base_dir.glob('hdm_research_papers_merged_*.csv'))
    
    if not csv_files:
        # Fall back to complete version
        csv_files = list(base_dir.glob('hdm_research_papers_complete_*.csv'))
    
    if not csv_files:
        print("Error: No HDM research papers CSV file found!")
        return
    
    # Use the most recent file
    csv_path = sorted(csv_files)[-1]
    print(f"Using CSV file: {csv_path}")
    
    # Read the CSV
    df = pd.read_csv(csv_path, encoding='utf-8')
    print(f"Loaded {len(df)} papers")
    
    # Sort by relevancy (High, Medium, Low) and then by year (descending)
    relevancy_order = {'SUPER': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    df['relevancy_sort'] = df['Relevancy'].str.upper().map(relevancy_order).fillna(4)
    df = df.sort_values(['relevancy_sort', 'year'], ascending=[True, False])
    
    # Create the markdown table
    output_path = base_dir / 'research_table_with_citekeys.md'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # Write header
        f.write("# HDM Research Papers - Complete Table with Cite Keys\n\n")
        f.write(f"Generated from: {csv_path.name}\n")
        f.write(f"Total papers: {len(df)}\n\n")
        
        # Statistics
        relevancy_counts = df['Relevancy'].str.upper().value_counts()
        f.write("## Statistics\n\n")
        for relevancy, count in relevancy_counts.items():
            f.write(f"- {relevancy}: {count} papers\n")
        f.write("\n")
        
        # Write table header
        headers = [
            'cite_key', 'Paper Title', 'Authors', 'Year', 'Downloaded', 
            'Relevancy', 'Relevancy Justification', 'Insights', 'TL;DR', 
            'Summary', 'Research Question', 'Methodology', 'Key Findings', 
            'Primary Outcomes', 'Limitations', 'Conclusion', 'Research Gaps', 
            'Future Work', 'Implementation Insights', 'url', 'DOI', 'Tags'
        ]
        
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join([":---"] * len(headers)) + " |\n")
        
        # Write each paper
        for idx, row in df.iterrows():
            row_data = []
            
            for header in headers:
                if header == 'Paper Title':
                    value = clean_text(row.get('title', ''))
                elif header == 'Authors':
                    value = clean_text(row.get('authors', ''))
                elif header == 'Year':
                    value = str(row.get('year', ''))
                elif header == 'Relevancy':
                    value = clean_text(row.get('Relevancy', '')).upper()
                elif header == 'url':
                    url = clean_text(row.get('url', ''))
                    if url:
                        value = f"[Link]({url})"
                    else:
                        value = ""
                elif header == 'DOI':
                    doi = clean_text(row.get('DOI', ''))
                    if doi and not doi.startswith('http'):
                        value = f"[{doi}](https://doi.org/{doi})"
                    elif doi:
                        value = f"[DOI]({doi})"
                    else:
                        value = ""
                elif header == 'Insights':
                    # Truncate insights to keep table readable
                    value = truncate_text(clean_text(row.get('Insights', '')), 300)
                elif header == 'Summary':
                    # Truncate summary
                    value = truncate_text(clean_text(row.get('Summary', '')), 400)
                else:
                    # Map header to column name
                    col_map = {
                        'Relevancy Justification': 'Relevancy Justification',
                        'TL;DR': 'TL;DR',
                        'Research Question': 'Research Question',
                        'Methodology': 'Methodology',
                        'Key Findings': 'Key Findings',
                        'Primary Outcomes': 'Primary Outcomes',
                        'Limitations': 'Limitations',
                        'Conclusion': 'Conclusion',
                        'Research Gaps': 'Research Gaps',
                        'Future Work': 'Future Work',
                        'Implementation Insights': 'Implementation Insights',
                        'Tags': 'Tags'
                    }
                    col_name = col_map.get(header, header)
                    value = clean_text(row.get(col_name, ''))
                    
                    # Truncate long fields
                    if header in ['Methodology', 'Key Findings', 'Primary Outcomes']:
                        value = truncate_text(value, 250)
            
            row_data.append(value)
            
            f.write("| " + " | ".join(row_data) + " |\n")
        
        f.write("\n---\n\n")
        f.write("*Note: Long text fields have been truncated for readability. ")
        f.write("Refer to the source CSV for complete content.*\n")
    
    print(f"\nGenerated: {output_path}")
    print(f"File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    main()