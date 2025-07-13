#!/usr/bin/env python3
"""
Export SQLite database to static JSON files for GitHub Pages
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

class StaticExporter:
    def __init__(self, db_path, output_dir):
        self.db_path = db_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def export_all(self):
        """Export all data to static JSON files"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 1. Export all papers
        print("📄 Exporting papers...")
        cursor.execute("SELECT * FROM papers ORDER BY year DESC, cite_key")
        papers = []
        for row in cursor.fetchall():
            paper = dict(row)
            # Add computed fields
            if paper['cite_key']:
                paper['markdown_link'] = f"markdown_papers/{paper['cite_key']}/paper.md"
                paper['viewer_link'] = f"paper_viewer.html?id={paper['cite_key']}"
                paper['folder_path'] = f"production_final_reformatted_1752365947/{paper['cite_key']}"
            papers.append(paper)
        
        with open(self.output_dir / 'papers.json', 'w', encoding='utf-8') as f:
            json.dump({
                'papers': papers,
                'count': len(papers),
                'generated': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        print(f"  ✅ Exported {len(papers)} papers")
        
        # 2. Export statistics
        print("📊 Exporting statistics...")
        cursor.execute("SELECT * FROM papers_statistics")
        stats_row = cursor.fetchone()
        stats = dict(stats_row) if stats_row else {}
        
        # Year distribution
        cursor.execute("""
            SELECT year, COUNT(*) as count 
            FROM papers 
            WHERE year IS NOT NULL 
            GROUP BY year 
            ORDER BY year
        """)
        year_dist = [dict(row) for row in cursor.fetchall()]
        
        # Tag cloud data
        cursor.execute("""
            SELECT tags FROM papers WHERE tags IS NOT NULL AND tags != ''
        """)
        tag_counts = {}
        for row in cursor.fetchall():
            tags = row['tags'].split(',')
            for tag in tags:
                tag = tag.strip()
                if tag:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        
        with open(self.output_dir / 'statistics.json', 'w', encoding='utf-8') as f:
            json.dump({
                'statistics': stats,
                'year_distribution': year_dist,
                'top_tags': top_tags,
                'tag_counts': tag_counts,
                'generated': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        print(f"  ✅ Exported statistics")
        
        # 3. Export years list
        print("📅 Exporting years...")
        cursor.execute("""
            SELECT DISTINCT year 
            FROM papers 
            WHERE year IS NOT NULL 
            ORDER BY year DESC
        """)
        years = [row['year'] for row in cursor.fetchall()]
        
        with open(self.output_dir / 'years.json', 'w', encoding='utf-8') as f:
            json.dump(years, f)
        print(f"  ✅ Exported {len(years)} years")
        
        # 4. Export relevancy levels
        print("🎯 Exporting relevancy levels...")
        cursor.execute("""
            SELECT DISTINCT relevancy, COUNT(*) as count
            FROM papers 
            WHERE relevancy IS NOT NULL 
            GROUP BY relevancy
            ORDER BY count DESC
        """)
        relevancy_levels = [dict(row) for row in cursor.fetchall()]
        
        with open(self.output_dir / 'relevancy.json', 'w', encoding='utf-8') as f:
            json.dump(relevancy_levels, f)
        print(f"  ✅ Exported relevancy levels")
        
        # 5. Create index file for easy access
        print("📑 Creating index file...")
        index = {
            'papers_count': len(papers),
            'years': years,
            'relevancy_levels': relevancy_levels,
            'top_tags': top_tags[:10],
            'files': {
                'papers': 'papers.json',
                'statistics': 'statistics.json',
                'years': 'years.json',
                'relevancy': 'relevancy.json'
            },
            'generated': datetime.now().isoformat()
        }
        
        with open(self.output_dir / 'index.json', 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        print(f"  ✅ Created index file")
        
        conn.close()
        
        print(f"\n✅ Export complete! Files saved to: {self.output_dir}")
        print(f"   Total size: {sum(f.stat().st_size for f in self.output_dir.glob('*.json')) / 1024 / 1024:.2f} MB")

def main():
    """Main entry point"""
    base_dir = Path("/Users/invoture/dev.local/hdm")
    db_path = base_dir / "hdm_papers.db"
    output_dir = base_dir / "data"
    
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return
    
    exporter = StaticExporter(db_path, output_dir)
    exporter.export_all()

if __name__ == "__main__":
    main()