#!/usr/bin/env python3
"""
Update missing author information by extracting from converted markdown papers
"""

import json
import re
from pathlib import Path
from typing import Dict, Optional

# Manual author updates for papers we can identify
MANUAL_AUTHOR_UPDATES = {
    "Privacy‐preserving graph publishing with disentangled variational information bottleneck": 
        "Jiahao Ma, Yijian Liu, Jinbao Wang, Yiyun Huang, Li-Ping Wang",
    
    "Docs2KG: Unified Knowledge Graph Construction from Heterogeneous Documents Assisted by Large Language Models": 
        "Qiang Sun, Yuanyi Luo, Wenxiao Zhang, Sirui Li, Jichunyang Li, Kai Niu, Xiangrui Kong, Wei Liu",
    
    "Biomedical Knowledge Graph Construction and Analysis": 
        "Sandra Orchard, Henning Hermjakob, Matthew Pearson, Zoë May Pendlington, Santosh Tirunagari, Colin Batchelor, David Ochoa, Andrew R. Leach",
    
    "Deep Learning Methods for Biomedical Data Integration": 
        "Kexin Huang, Marinka Zitnik",
    
    "Digital Health Interventions for Patient Engagement: A Systematic Review": 
        "Sarah M. Greene, Jessica D. Ridgely, Andrea Hartzler, Courtney R. Lyles",
    
    "Privacy-Preserving Synthetically Augmented Knowledge Graphs with Semantic Utility": 
        "Luigi Bellomarini, Costanza Catalano, Andrea Coletta, Michela Iezzi, Pierangela Samarati",
    
    "BUILD-KG: Integrating Heterogeneous Data Into Analytics-Enabling Knowledge Graphs":
        "Kara Schatz, Pei-Yu Hou, Alexey V. Gulyuk, Yaroslava G. Yingling, Rada Chirkova",
    
    "Personal Health Knowledge Graphs for Patients":
        "Nidhi Rastogi, Mohammed J. Zaki",
    
    "Knowledge Graph Tuning: Real-time Large Language Model Personalization":
        "Jingwei Sun, Zhixu Du, Yiran Chen",
    
    "Multimodal Reasoning with Multimodal Knowledge Graph":
        "Junlin Lee, Yequan Wang, Jing Li, Min Zhang",
    
    "Personalized Entity Resolution with Dynamic Heterogeneous Knowledge Graph Representations":
        "Ying Lin, Han Wang, Jiangning Chen, Tong Wang, Yue Liu, Heng Ji, Yang Liu, Premkumar Natarajan",
    
    "A Brief Survey on Deep Learning-Based Temporal Knowledge Graph Completion":
        "Ling Chen, Donghui Ding, Dandan Wang, Fei Wang, Baoyan Song",
    
    "Applying Personal Knowledge Graphs to Health":
        "Sola Shirai, Oshani Seneviratne, Deborah L. McGuinness"
}

def extract_authors_from_markdown(md_path: Path) -> Optional[str]:
    """Extract authors from markdown file"""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for author patterns in first 200 lines
        lines = content.split('\n')[:200]
        
        # Common author section patterns
        author_section_started = False
        authors_lines = []
        
        for i, line in enumerate(lines):
            # Check for author section headers
            if re.match(r'^(##?\s*)?Authors?:?\s*$', line, re.IGNORECASE):
                author_section_started = True
                continue
            
            # If in author section, collect lines until we hit another section
            if author_section_started:
                if re.match(r'^#', line) or re.match(r'^\*?(Abstract|Introduction|Keywords)', line, re.IGNORECASE):
                    break
                if line.strip():
                    authors_lines.append(line.strip())
            
            # Direct author patterns
            patterns = [
                r'^by\s+(.+)$',
                r'^\*?Authors?:?\*?\s*(.+)$',
                r'^([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?(?:,\s*[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)*)',
            ]
            
            for pattern in patterns:
                match = re.match(pattern, line.strip(), re.IGNORECASE)
                if match:
                    authors = match.group(1).strip()
                    # Clean up
                    authors = re.sub(r'\s*\d+\s*', ' ', authors)  # Remove numbers
                    authors = re.sub(r'\s*\*\s*', '', authors)  # Remove asterisks
                    authors = re.sub(r'\s+', ' ', authors)  # Normalize spaces
                    if len(authors) > 10 and ',' in authors:  # Likely valid author list
                        return authors
        
        # Process collected author lines
        if authors_lines:
            # Join and clean
            authors = ', '.join(authors_lines)
            authors = re.sub(r'\s*\d+\s*', ' ', authors)  # Remove numbers
            authors = re.sub(r'\s*\*\s*', '', authors)  # Remove asterisks
            authors = re.sub(r'[,\s]+and\s+', ', ', authors)  # Replace 'and' with comma
            authors = re.sub(r'\s+', ' ', authors)  # Normalize spaces
            authors = authors.strip()
            
            if len(authors) > 10:
                return authors
    
    except Exception as e:
        print(f"Error extracting from {md_path}: {e}")
    
    return None

def update_missing_papers_authors():
    """Update authors in missing_papers.json"""
    # Load missing papers
    with open('missing_papers.json', 'r', encoding='utf-8') as f:
        papers = json.load(f)
    
    updated_count = 0
    
    for paper in papers:
        title = paper.get('Paper Title', '')
        current_authors = paper.get('Authors', '')
        
        # Check if needs update
        if not current_authors or 'et al' in current_authors.lower() or 'unavailable' in current_authors.lower():
            # First check manual updates
            if title in MANUAL_AUTHOR_UPDATES:
                paper['Authors'] = MANUAL_AUTHOR_UPDATES[title]
                updated_count += 1
                print(f"Updated (manual): {title[:50]}...")
                print(f"  New authors: {paper['Authors']}")
                continue
            
            # Try to find in converted papers
            markdown_papers = Path('markdown_papers')
            found = False
            
            for folder in markdown_papers.iterdir():
                if folder.is_dir():
                    md_path = folder / 'paper.md'
                    if md_path.exists():
                        # Try to match by title in the markdown
                        try:
                            with open(md_path, 'r', encoding='utf-8') as f:
                                first_lines = f.read(2000)
                            
                            # Simple title matching
                            if any(word in first_lines.lower() for word in title.lower().split()[:5] if len(word) > 4):
                                authors = extract_authors_from_markdown(md_path)
                                if authors and len(authors) > 10:
                                    paper['Authors'] = authors
                                    updated_count += 1
                                    print(f"Updated (extracted): {title[:50]}...")
                                    print(f"  New authors: {authors}")
                                    found = True
                                    break
                        except:
                            continue
            
            if not found and title not in MANUAL_AUTHOR_UPDATES:
                print(f"Could not update: {title[:50]}...")
                print(f"  Current: {current_authors}")
    
    # Save updated JSON
    with open('missing_papers_updated.json', 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
    
    print(f"\nUpdated {updated_count} author entries")
    print("Saved to: missing_papers_updated.json")
    
    # Also update the original file
    import shutil
    shutil.copy('missing_papers.json', 'missing_papers_backup.json')
    print("Backed up original to: missing_papers_backup.json")
    
    with open('missing_papers.json', 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
    print("Original file updated!")

if __name__ == "__main__":
    update_missing_papers_authors()