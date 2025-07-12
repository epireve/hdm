#!/usr/bin/env python3
"""
YAML Frontmatter Restoration Script
Restores rich YAML frontmatter for papers using research table data
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
try:
    import yaml
except ImportError:
    # Simple YAML alternative if PyYAML not available
    yaml = None
import re
from datetime import datetime
import shutil

class FrontmatterRestorer:
    def __init__(self, research_table_path: str = None):
        self.base_dir = Path("/Users/invoture/dev.local/hdm")
        self.markdown_papers_dir = self.base_dir / "markdown_papers"
        self.research_table_path = research_table_path or str(self.base_dir / "research_table_with_citekeys.md")
        
        # Backup directory
        self.backup_dir = self.base_dir / "backups" / f"frontmatter_restore_{datetime.now():%Y%m%d_%H%M%S}"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Load research table data
        self.research_data = {}
        self.load_research_table()
        
        # Papers categorized by frontmatter status
        self.minimal_papers = [
            "das_2024", "bui_2024", "e065929_full", "fafrowicz_2022", 
            "li_2022", "mohbat_2025", "pascual_2022", "plailly_2019", "bui_2023"
        ]
        
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "restored": [],
            "fixed": [],
            "created": [],
            "errors": [],
            "skipped": []
        }
    
    def load_research_table(self):
        """Load research table data into memory for metadata population"""
        print(f"📖 Loading research table from {self.research_table_path}")
        
        if not Path(self.research_table_path).exists():
            print(f"❌ Research table not found: {self.research_table_path}")
            return
            
        try:
            with open(self.research_table_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse markdown table
            lines = content.strip().split('\n')
            headers = None
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                if '|' in line and not line.startswith('|---'):
                    cols = [col.strip() for col in line.split('|')[1:-1]]  # Remove empty first/last
                    
                    if headers is None:
                        headers = cols
                        continue
                    
                    if len(cols) >= len(headers):
                        cite_key = cols[0].strip()
                        if cite_key and cite_key != 'cite_key':
                            # Map to research table structure
                            paper_data = {
                                'title': cols[1] if len(cols) > 1 else '',
                                'authors': cols[2] if len(cols) > 2 else '',
                                'year': cols[3] if len(cols) > 3 else '',
                                'downloaded': cols[4] if len(cols) > 4 else '',
                                'relevancy': cols[5] if len(cols) > 5 else '',
                                'relevancy_justification': cols[6] if len(cols) > 6 else '',
                                'insights': cols[7] if len(cols) > 7 else '',
                                'tldr': cols[8] if len(cols) > 8 else '',
                                'summary': cols[9] if len(cols) > 9 else '',
                                'research_question': cols[10] if len(cols) > 10 else '',
                                'methodology': cols[11] if len(cols) > 11 else '',
                                'key_findings': cols[12] if len(cols) > 12 else '',
                                'primary_outcomes': cols[13] if len(cols) > 13 else '',
                                'limitations': cols[14] if len(cols) > 14 else '',
                                'conclusion': cols[15] if len(cols) > 15 else '',
                                'research_gaps': cols[16] if len(cols) > 16 else '',
                                'future_work': cols[17] if len(cols) > 17 else '',
                                'implementation_insights': cols[18] if len(cols) > 18 else '',
                                'url': cols[19] if len(cols) > 19 else '',
                                'doi': cols[20] if len(cols) > 20 else '',
                                'tags': cols[21] if len(cols) > 21 else ''
                            }
                            self.research_data[cite_key] = paper_data
            
            print(f"✅ Loaded {len(self.research_data)} papers from research table")
            
        except Exception as e:
            print(f"❌ Error loading research table: {e}")
    
    def parse_frontmatter(self, content: str) -> Tuple[Optional[Dict], str]:
        """Parse YAML frontmatter from markdown content"""
        lines = content.split('\n')
        if not lines or lines[0].strip() != '---':
            return None, content
        
        yaml_lines = []
        content_start = 0
        
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == '---':
                content_start = i + 1
                break
            yaml_lines.append(line)
        
        if content_start == 0:
            return None, content
        
        try:
            if yaml:
                frontmatter = yaml.safe_load('\n'.join(yaml_lines)) if yaml_lines else {}
            else:
                # Simple YAML parsing fallback
                frontmatter = {}
                for line in yaml_lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        frontmatter[key.strip()] = value.strip().strip('"\'')
            return frontmatter, '\n'.join(lines[content_start:])
        except Exception as e:
            print(f"⚠️  YAML parsing error: {e}")
            return {}, '\n'.join(lines[content_start:])
    
    def create_rich_frontmatter(self, cite_key: str, existing_frontmatter: Dict = None) -> Dict:
        """Create rich frontmatter using research table data"""
        existing_frontmatter = existing_frontmatter or {}
        
        # Start with existing data
        frontmatter = existing_frontmatter.copy()
        
        # Get research table data
        research_data = self.research_data.get(cite_key, {})
        
        # Core fields (always update from research table if available)
        if research_data.get('title'):
            frontmatter['title'] = research_data['title']
        if research_data.get('authors'):
            frontmatter['authors'] = research_data['authors']
        if research_data.get('year'):
            try:
                frontmatter['year'] = int(research_data['year'])
            except (ValueError, TypeError):
                pass
        if research_data.get('doi'):
            frontmatter['doi'] = research_data['doi']
        if research_data.get('url'):
            frontmatter['url'] = research_data['url']
        
        # Research analysis fields (only if missing)
        analysis_fields = {
            'relevancy': research_data.get('relevancy', '').upper() if research_data.get('relevancy') else 'Medium',
            'relevancy_justification': research_data.get('relevancy_justification', ''),
            'tldr': research_data.get('tldr', ''),
            'insights': research_data.get('insights', ''),
            'summary': research_data.get('summary', ''),
            'research_question': research_data.get('research_question', ''),
            'methodology': research_data.get('methodology', ''),
            'key_findings': research_data.get('key_findings', ''),
            'primary_outcomes': research_data.get('primary_outcomes', ''),
            'limitations': research_data.get('limitations', ''),
            'conclusion': research_data.get('conclusion', ''),
            'research_gaps': research_data.get('research_gaps', ''),
            'future_work': research_data.get('future_work', ''),
            'implementation_insights': research_data.get('implementation_insights', '')
        }
        
        for field, value in analysis_fields.items():
            if field not in frontmatter and value:
                frontmatter[field] = value
        
        # Process tags
        if research_data.get('tags') and 'tags' not in frontmatter:
            tags = research_data['tags']
            if isinstance(tags, str):
                # Split by comma and clean up
                tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
                frontmatter['tags'] = tag_list
        
        # Ensure cite_key is correct
        frontmatter['cite_key'] = cite_key
        
        # Add processing metadata if missing
        if 'date_processed' not in frontmatter:
            frontmatter['date_processed'] = datetime.now().strftime('%Y-%m-%d')
        
        return frontmatter
    
    def save_with_frontmatter(self, file_path: Path, frontmatter: Dict, content: str):
        """Save markdown file with YAML frontmatter"""
        # Create backup
        backup_path = self.backup_dir / file_path.name
        if file_path.exists():
            shutil.copy2(file_path, backup_path)
        
        # Order frontmatter fields logically
        ordered_fields = [
            'cite_key', 'title', 'authors', 'year', 'doi', 'url', 
            'relevancy', 'relevancy_justification', 'downloaded',
            'tldr', 'insights', 'summary', 'research_question', 
            'methodology', 'key_findings', 'primary_outcomes',
            'limitations', 'conclusion', 'research_gaps', 'future_work',
            'implementation_insights', 'tags', 'date_processed', 'phase2_processed'
        ]
        
        ordered_frontmatter = {}
        
        # Add fields in order
        for field in ordered_fields:
            if field in frontmatter:
                ordered_frontmatter[field] = frontmatter[field]
        
        # Add any remaining fields
        for field, value in frontmatter.items():
            if field not in ordered_frontmatter:
                ordered_frontmatter[field] = value
        
        # Write file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('---\n')
            if yaml:
                yaml.dump(ordered_frontmatter, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            else:
                # Simple YAML writing fallback
                for key, value in ordered_frontmatter.items():
                    if isinstance(value, list):
                        f.write(f'{key}:\n')
                        for item in value:
                            f.write(f'  - {item}\n')
                    elif isinstance(value, str) and '\n' in value:
                        f.write(f'{key}: |\n')
                        for line in value.split('\n'):
                            f.write(f'  {line}\n')
                    else:
                        f.write(f'{key}: {value}\n')
            f.write('---\n\n')
            f.write(content)
    
    def restore_minimal_papers(self):
        """Restore the 9 papers with minimal frontmatter"""
        print("🔄 Restoring minimal frontmatter papers...")
        
        for cite_key in self.minimal_papers:
            paper_path = self.markdown_papers_dir / cite_key / "paper.md"
            
            if not paper_path.exists():
                self.report["errors"].append(f"{cite_key}: Paper file not found")
                continue
            
            print(f"   📝 Restoring {cite_key}...")
            
            try:
                with open(paper_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                existing_frontmatter, body = self.parse_frontmatter(content)
                rich_frontmatter = self.create_rich_frontmatter(cite_key, existing_frontmatter)
                
                self.save_with_frontmatter(paper_path, rich_frontmatter, body)
                self.report["restored"].append(cite_key)
                print(f"   ✅ Restored {cite_key}")
                
            except Exception as e:
                error_msg = f"{cite_key}: {str(e)}"
                self.report["errors"].append(error_msg)
                print(f"   ❌ Error restoring {cite_key}: {e}")
    
    def fix_incomplete_yaml(self):
        """Fix papers with incomplete/malformed YAML"""
        print("🔧 Fixing incomplete YAML papers...")
        
        # Get list from analysis report  
        incomplete_papers = [
            "aburasheed_2023b", "barton_2024", "benevides_2021", "bhowmik_2024",
            "burton_2023", "cao_2024", "ferreira_2023", "fitrianie_2021",
            "guevara_2023", "guo_2024", "ijjina_2023", "jakaria_2021",
            "jinyi_2024", "komal_2021", "kumar_2023", "lei_2024",
            "liang_2024", "liu_2024a", "majumder_2024", "malik_2024",
            "naveed_2024", "neha_2021", "rezig_2020", "rodrigues_2024",
            "saeedi_2023", "shen_2024", "su_2024", "tran_2021",
            "wang_2023", "wu_2021", "xu_2023", "yang_2024a",
            "zhang_2020", "zhang_2024"
        ]
        
        for cite_key in incomplete_papers:
            paper_path = self.markdown_papers_dir / cite_key / "paper.md"
            
            if not paper_path.exists():
                continue
            
            print(f"   🔧 Fixing {cite_key}...")
            
            try:
                with open(paper_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                existing_frontmatter, body = self.parse_frontmatter(content)
                
                if existing_frontmatter is None:
                    # No frontmatter, create new
                    rich_frontmatter = self.create_rich_frontmatter(cite_key)
                else:
                    # Fix/enhance existing frontmatter
                    rich_frontmatter = self.create_rich_frontmatter(cite_key, existing_frontmatter)
                
                self.save_with_frontmatter(paper_path, rich_frontmatter, body)
                self.report["fixed"].append(cite_key)
                print(f"   ✅ Fixed {cite_key}")
                
            except Exception as e:
                error_msg = f"{cite_key}: {str(e)}"
                self.report["errors"].append(error_msg)
                print(f"   ❌ Error fixing {cite_key}: {e}")
    
    def create_missing_yaml(self):
        """Create YAML frontmatter for papers with no frontmatter"""
        print("📝 Creating missing YAML frontmatter...")
        
        no_yaml_papers = [
            "ai_2025", "bernard_2024", "bontempelli_2017", "castilloescamilla_2024",
            "chen_2024", "cheng_2024", "cotelo_2017", "dai_2023", 
            "deng_2020", "ding_2024", "dong_2021", "duan_2024",
            "firdaus_2023", "ghashghaei_2021", "golshan_2024", "guo_2021",
            "han_2023", "he_2024", "hou_2024", "hu_2021",
            "huang_2024", "islam_2023", "jiang_2024", "khan_2024",
            "konstantinidis_2022", "lee_2023", "li_2024a", "lin_2024",
            "liu_2024b", "ma_2024", "mehta_2024", "memariani_2024",
            "nan_2024", "nasiri_2023", "nguyen_2024", "ojha_2023",
            "pan_2021", "patterson_2024", "peng_2023", "qin_2024",
            "rahman_2023", "rehman_2024", "salehnia_2024", "seraj_2024",
            "sharma_2024", "shen_2023", "singh_2024", "sun_2024",
            "tan_2023", "teh_2024", "tran_2024", "wang_2024a",
            "wong_2024", "wu_2024", "xing_2024", "yan_2023",
            "yang_2024b", "ye_2024", "yilmaz_2023", "yu_2024",
            "yuan_2024", "zenuni_2024", "zhang_2023", "zhang_2024a",
            "zhang_2024b", "zhao_2024", "zhou_2024", "zhu_2024",
            "das_2025"  # Also has no frontmatter issue
        ]
        
        for cite_key in no_yaml_papers:
            paper_path = self.markdown_papers_dir / cite_key / "paper.md"
            
            if not paper_path.exists():
                continue
            
            print(f"   📝 Creating YAML for {cite_key}...")
            
            try:
                with open(paper_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if it already has frontmatter
                existing_frontmatter, body = self.parse_frontmatter(content)
                
                if existing_frontmatter is not None:
                    # Skip - already has frontmatter
                    self.report["skipped"].append(f"{cite_key}: Already has frontmatter")
                    continue
                
                # Create new frontmatter
                rich_frontmatter = self.create_rich_frontmatter(cite_key)
                self.save_with_frontmatter(paper_path, rich_frontmatter, content)
                self.report["created"].append(cite_key)
                print(f"   ✅ Created YAML for {cite_key}")
                
            except Exception as e:
                error_msg = f"{cite_key}: {str(e)}"
                self.report["errors"].append(error_msg)
                print(f"   ❌ Error creating YAML for {cite_key}: {e}")
    
    def run_restoration(self):
        """Run complete frontmatter restoration process"""
        print("🚀 Starting YAML Frontmatter Restoration")
        print(f"📁 Backup directory: {self.backup_dir}")
        print()
        
        # Phase 1: Restore minimal papers
        self.restore_minimal_papers()
        print()
        
        # Phase 2: Fix incomplete YAML
        self.fix_incomplete_yaml()
        print()
        
        # Phase 3: Create missing YAML
        self.create_missing_yaml()
        print()
        
        # Save report
        report_path = self.base_dir / f"frontmatter_restoration_report_{datetime.now():%Y%m%d_%H%M%S}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2)
        
        print("📊 Restoration Complete!")
        print(f"   ✅ Restored: {len(self.report['restored'])} papers")
        print(f"   🔧 Fixed: {len(self.report['fixed'])} papers")
        print(f"   📝 Created: {len(self.report['created'])} papers")
        print(f"   ⚠️  Errors: {len(self.report['errors'])} papers")
        print(f"   ⏭️  Skipped: {len(self.report['skipped'])} papers")
        print(f"📄 Report: {report_path}")

if __name__ == "__main__":
    restorer = FrontmatterRestorer()
    restorer.run_restoration()