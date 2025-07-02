#!/usr/bin/env python3
"""
Check the current status of image descriptions across all papers
"""
import re
from pathlib import Path
from datetime import datetime

def has_image_description(content, image_file):
    """Check if an image already has a description comment"""
    pattern = rf'!\[\]\({re.escape(image_file)}\)\s*\n\s*<!-- Image Description:.*?-->'
    return bool(re.search(pattern, content, re.DOTALL))

def check_paper(paper_path):
    """Check a single paper for image description status"""
    try:
        with open(paper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all images with empty alt text
        image_pattern = r'!\[\]\(([^)]+)\)'
        empty_images = re.findall(image_pattern, content)
        
        if not empty_images:
            return 0, 0, 0  # no images, described, not described
        
        # Check which images have descriptions
        described = 0
        not_described = 0
        
        for image_file in empty_images:
            if has_image_description(content, image_file):
                described += 1
            else:
                not_described += 1
        
        return len(empty_images), described, not_described
        
    except Exception as e:
        return 0, 0, 0

def main():
    """Main function"""
    markdown_papers = Path('markdown_papers')
    
    stats = {
        'total_papers': 0,
        'papers_with_images': 0,
        'papers_fully_described': 0,
        'papers_partially_described': 0,
        'papers_no_descriptions': 0,
        'total_images': 0,
        'total_described': 0,
        'total_not_described': 0
    }
    
    papers_needing_work = []
    
    print("Checking image description status...")
    print("=" * 60)
    
    # Check all papers
    for folder in sorted(markdown_papers.iterdir()):
        if folder.is_dir():
            paper_path = folder / 'paper.md'
            if paper_path.exists():
                stats['total_papers'] += 1
                
                total, described, not_described = check_paper(paper_path)
                
                if total > 0:
                    stats['papers_with_images'] += 1
                    stats['total_images'] += total
                    stats['total_described'] += described
                    stats['total_not_described'] += not_described
                    
                    if not_described == 0:
                        stats['papers_fully_described'] += 1
                    elif described > 0:
                        stats['papers_partially_described'] += 1
                        papers_needing_work.append((folder.name, total, described, not_described))
                    else:
                        stats['papers_no_descriptions'] += 1
                        papers_needing_work.append((folder.name, total, described, not_described))
    
    # Generate report
    print(f"\nOVERALL STATISTICS")
    print("-" * 40)
    print(f"Total papers: {stats['total_papers']}")
    print(f"Papers with images: {stats['papers_with_images']}")
    print(f"  - Fully described: {stats['papers_fully_described']}")
    print(f"  - Partially described: {stats['papers_partially_described']}")
    print(f"  - No descriptions: {stats['papers_no_descriptions']}")
    print(f"\nTotal images: {stats['total_images']}")
    print(f"  - Described: {stats['total_described']} ({stats['total_described']/stats['total_images']*100:.1f}%)")
    print(f"  - Not described: {stats['total_not_described']} ({stats['total_not_described']/stats['total_images']*100:.1f}%)")
    
    if papers_needing_work:
        print(f"\n\nPAPERS NEEDING IMAGE DESCRIPTIONS ({len(papers_needing_work)} papers)")
        print("-" * 60)
        print(f"{'Paper':<40} {'Total':>8} {'Done':>8} {'Todo':>8}")
        print("-" * 60)
        
        # Sort by number of images needing description
        papers_needing_work.sort(key=lambda x: x[3], reverse=True)
        
        for paper_name, total, described, not_described in papers_needing_work[:20]:
            print(f"{paper_name:<40} {total:>8} {described:>8} {not_described:>8}")
        
        if len(papers_needing_work) > 20:
            print(f"... and {len(papers_needing_work) - 20} more papers")
    
    # Save detailed report
    report_file = Path(f'image_description_status_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
    with open(report_file, 'w') as f:
        f.write(f"Image Description Status Report\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write("=" * 60 + "\n")
        f.write(f"\nTotal papers: {stats['total_papers']}\n")
        f.write(f"Papers with images: {stats['papers_with_images']}\n")
        f.write(f"Total images: {stats['total_images']}\n")
        f.write(f"Images described: {stats['total_described']} ({stats['total_described']/stats['total_images']*100:.1f}%)\n")
        f.write(f"Images not described: {stats['total_not_described']} ({stats['total_not_described']/stats['total_images']*100:.1f}%)\n")
        
        if papers_needing_work:
            f.write(f"\nPapers needing descriptions:\n")
            for paper_name, total, described, not_described in papers_needing_work:
                f.write(f"  {paper_name}: {not_described} images need descriptions (out of {total})\n")
    
    print(f"\nDetailed report saved to: {report_file}")

if __name__ == '__main__':
    main()