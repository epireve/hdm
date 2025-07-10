#!/usr/bin/env python3
"""
Fix the authors field for zha_2024 paper
"""
from pathlib import Path

def main():
    paper_path = Path('markdown_papers/zha_2024/paper.md')
    
    # Read content
    with open(paper_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the empty authors line
    content = content.replace(
        "authors: '",
        "authors: Daochen Zha, Zaid Pervaiz Bhat, Kwei-Herng Lai, Fan Yang, Zhimeng Jiang, Shaochen Zhong, Xia Hu"
    )
    
    # Write back
    with open(paper_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed authors field for zha_2024")

if __name__ == '__main__':
    main()