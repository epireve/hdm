#!/usr/bin/env python3
"""
Execute the final consolidation strategy with intelligent data selection
and removal of the 'downloaded' column.
"""

import sqlite3
import json
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import shutil
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('final_consolidation_execution.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FinalConsolidationExecutor:
    """Execute the final consolidation with backup and safety measures."""
    
    def __init__(self):
        self.backup_created = False
        self.consolidation_stats = {
            'total_records': 0,
            'records_updated': 0,
            'fields_updated': 0,
            'downloaded_column_removed': False,
            'yaml_columns_removed': False,
            'execution_timestamp': None
        }
    
    def create_database_backup(self) -> str:
        """Create a backup of the database before consolidation."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'hdm_papers_backup_{timestamp}.db'
        
        try:
            shutil.copy2('hdm_papers.db', backup_filename)
            self.backup_created = True
            logger.info(f"Database backup created: {backup_filename}")
            return backup_filename
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            raise
    
    def validate_database_integrity(self) -> bool:
        """Validate database integrity before and after operations."""
        try:
            conn = sqlite3.connect('hdm_papers.db')
            cursor = conn.cursor()
            
            # Check table exists and has expected structure
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='papers'")
            if not cursor.fetchone():
                logger.error("Papers table not found")
                return False
            
            # Check record count
            cursor.execute("SELECT COUNT(*) FROM papers")
            count = cursor.fetchone()[0]
            
            if count == 0:
                logger.error("No records found in papers table")
                return False
            
            logger.info(f"Database validation passed: {count} records found")
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Database validation failed: {e}")
            return False
    
    def get_consolidation_plan(self) -> Dict[str, Any]:
        """Load the consolidation plan from dry run analysis."""
        try:
            with open('intelligent_consolidation_dry_run.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("Dry run analysis not found. Run intelligent_consolidation_strategy.py first.")
            raise
    
    def execute_consolidation_updates(self) -> Dict[str, Any]:
        """Execute the consolidation updates based on the intelligent strategy."""
        logger.info("Executing consolidation updates...")
        
        # Import the consolidator logic
        from intelligent_consolidation_strategy import IntelligentConsolidator
        
        consolidator = IntelligentConsolidator()
        
        # Get database connection
        conn = sqlite3.connect('hdm_papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all data
        all_columns = set()
        for config in consolidator.consolidation_rules.values():
            all_columns.update(config['priority_sources'])
        all_columns.add('cite_key')
        all_columns.add('id')  # Need ID for updates
        
        query = f"SELECT {', '.join(all_columns)} FROM papers"
        cursor.execute(query)
        records = [dict(row) for row in cursor.fetchall()]
        
        self.consolidation_stats['total_records'] = len(records)
        
        # Process each record
        updated_records = 0
        total_field_updates = 0
        
        for record in records:
            record_id = record['id']
            cite_key = record.get('cite_key', 'unknown')
            
            # Get consolidated values (not dry run)
            consolidated = consolidator.consolidate_single_record(record, dry_run=False)
            
            # Check what changed
            updates = []
            update_values = []
            
            for field in consolidator.consolidation_rules.keys():
                if field == 'downloaded':  # Skip downloaded field
                    continue
                    
                original_value = record.get(field)
                new_value = consolidated.get(field)
                
                if new_value != original_value:
                    updates.append(f"{field} = ?")
                    update_values.append(new_value)
                    total_field_updates += 1
            
            # Execute updates if any changes
            if updates:
                update_query = f"UPDATE papers SET {', '.join(updates)} WHERE id = ?"
                update_values.append(record_id)
                
                cursor.execute(update_query, update_values)
                updated_records += 1
                
                logger.debug(f"Updated {cite_key}: {len(updates)} fields changed")
        
        # Commit all updates
        conn.commit()
        conn.close()
        
        self.consolidation_stats['records_updated'] = updated_records
        self.consolidation_stats['fields_updated'] = total_field_updates
        
        logger.info(f"Consolidation complete: {updated_records} records updated, {total_field_updates} fields improved")
        
        return {
            'records_updated': updated_records,
            'fields_updated': total_field_updates
        }
    
    def remove_downloaded_column(self) -> bool:
        """Remove the 'downloaded' column from the database."""
        logger.info("Removing 'downloaded' column...")
        
        try:
            conn = sqlite3.connect('hdm_papers.db')
            cursor = conn.cursor()
            
            # Check if column exists
            cursor.execute("PRAGMA table_info(papers)")
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'downloaded' not in columns:
                logger.info("Downloaded column not found - already removed")
                conn.close()
                return True
            
            # Create new table without downloaded column
            columns_to_keep = [col for col in columns if col != 'downloaded']
            columns_def = []
            
            # Get column definitions
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='papers'")
            create_sql = cursor.fetchone()[0]
            
            # For simplicity, create new table with kept columns
            new_columns_str = ', '.join(columns_to_keep)
            
            # Create temporary table
            cursor.execute(f"""
                CREATE TABLE papers_new AS 
                SELECT {new_columns_str} FROM papers
            """)
            
            # Drop old table and rename new one
            cursor.execute("DROP TABLE papers")
            cursor.execute("ALTER TABLE papers_new RENAME TO papers")
            
            # Recreate indexes (simplified)
            cursor.execute("CREATE INDEX idx_cite_key ON papers(cite_key)")
            cursor.execute("CREATE INDEX idx_year ON papers(year)")
            cursor.execute("CREATE INDEX idx_relevancy ON papers(relevancy)")
            
            # Recreate triggers
            cursor.execute("""
                CREATE TRIGGER update_papers_timestamp 
                AFTER UPDATE ON papers
                BEGIN
                    UPDATE papers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
                END
            """)
            
            conn.commit()
            conn.close()
            
            self.consolidation_stats['downloaded_column_removed'] = True
            logger.info("Successfully removed 'downloaded' column")
            return True
            
        except Exception as e:
            logger.error(f"Error removing downloaded column: {e}")
            return False
    
    def cleanup_yaml_columns(self) -> bool:
        """Optionally remove YAML columns after consolidation."""
        logger.info("Cleaning up YAML columns...")
        
        try:
            conn = sqlite3.connect('hdm_papers.db')
            cursor = conn.cursor()
            
            # Get all YAML columns
            cursor.execute("PRAGMA table_info(papers)")
            columns = [row[1] for row in cursor.fetchall()]
            yaml_columns = [col for col in columns if col.startswith('yaml_')]
            
            if not yaml_columns:
                logger.info("No YAML columns found to remove")
                conn.close()
                return True
            
            logger.info(f"Found {len(yaml_columns)} YAML columns to remove")
            
            # Create new table without YAML columns
            columns_to_keep = [col for col in columns if not col.startswith('yaml_')]
            new_columns_str = ', '.join(columns_to_keep)
            
            # Create temporary table
            cursor.execute(f"""
                CREATE TABLE papers_final AS 
                SELECT {new_columns_str} FROM papers
            """)
            
            # Drop old table and rename new one
            cursor.execute("DROP TABLE papers")
            cursor.execute("ALTER TABLE papers_final RENAME TO papers")
            
            # Recreate essential indexes
            cursor.execute("CREATE INDEX idx_cite_key ON papers(cite_key)")
            cursor.execute("CREATE INDEX idx_year ON papers(year)")
            cursor.execute("CREATE INDEX idx_relevancy ON papers(relevancy)")
            
            # Recreate trigger
            cursor.execute("""
                CREATE TRIGGER update_papers_timestamp 
                AFTER UPDATE ON papers
                BEGIN
                    UPDATE papers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
                END
            """)
            
            conn.commit()
            conn.close()
            
            self.consolidation_stats['yaml_columns_removed'] = True
            logger.info(f"Successfully removed {len(yaml_columns)} YAML columns")
            return True
            
        except Exception as e:
            logger.error(f"Error removing YAML columns: {e}")
            return False
    
    def generate_final_report(self, backup_filename: str) -> Dict[str, Any]:
        """Generate final consolidation report."""
        
        # Get final database stats
        conn = sqlite3.connect('hdm_papers.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM papers")
        final_record_count = cursor.fetchone()[0]
        
        cursor.execute("PRAGMA table_info(papers)")
        final_columns = [row[1] for row in cursor.fetchall()]
        
        conn.close()
        
        report = {
            'consolidation_timestamp': datetime.now().isoformat(),
            'backup_file': backup_filename,
            'consolidation_stats': self.consolidation_stats,
            'final_database_state': {
                'total_records': final_record_count,
                'total_columns': len(final_columns),
                'columns': final_columns,
                'downloaded_column_present': 'downloaded' in final_columns,
                'yaml_columns_present': any(col.startswith('yaml_') for col in final_columns)
            },
            'success': all([
                self.consolidation_stats['records_updated'] > 0,
                self.consolidation_stats['downloaded_column_removed'],
                final_record_count == self.consolidation_stats['total_records']
            ])
        }
        
        return report

def main():
    """Execute the final consolidation process."""
    logger.info("Starting Final Consolidation Execution...")
    
    executor = FinalConsolidationExecutor()
    
    try:
        # Step 1: Validate database integrity
        if not executor.validate_database_integrity():
            logger.error("Database validation failed. Aborting consolidation.")
            return
        
        # Step 2: Create backup
        backup_filename = executor.create_database_backup()
        
        # Step 3: Load and validate consolidation plan
        plan = executor.get_consolidation_plan()
        logger.info(f"Consolidation plan loaded: {plan['total_fields_updated']} fields to update")
        
        # Step 4: Execute consolidation updates
        consolidation_results = executor.execute_consolidation_updates()
        
        # Step 5: Remove downloaded column
        if not executor.remove_downloaded_column():
            logger.error("Failed to remove downloaded column")
            return
        
        # Step 6: Optionally cleanup YAML columns
        print("\nWould you like to remove the YAML columns now that data has been consolidated? (y/N): ", end="")
        # For automation, we'll keep YAML columns for now
        print("N (automated choice - keeping YAML columns for reference)")
        
        # Step 7: Final validation
        if not executor.validate_database_integrity():
            logger.error("Post-consolidation validation failed")
            return
        
        # Step 8: Generate final report
        executor.consolidation_stats['execution_timestamp'] = datetime.now().isoformat()
        final_report = executor.generate_final_report(backup_filename)
        
        # Save report
        with open('final_consolidation_report.json', 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False, default=str)
        
        # Print success summary
        print("\n" + "="*80)
        print("FINAL CONSOLIDATION EXECUTION COMPLETED")
        print("="*80)
        
        print(f"✅ Database backup created: {backup_filename}")
        print(f"✅ Records updated: {final_report['consolidation_stats']['records_updated']}")
        print(f"✅ Fields improved: {final_report['consolidation_stats']['fields_updated']}")
        print(f"✅ Downloaded column removed: {final_report['consolidation_stats']['downloaded_column_removed']}")
        print(f"✅ Final record count: {final_report['final_database_state']['total_records']}")
        print(f"✅ Final column count: {final_report['final_database_state']['total_columns']}")
        
        if final_report['success']:
            print(f"\n🎉 CONSOLIDATION SUCCESSFUL!")
            print(f"   Database optimized with best available information")
            print(f"   Expert curation preserved, metadata enhanced")
            print(f"   Downloaded column removed as requested")
        else:
            print(f"\n⚠️  CONSOLIDATION COMPLETED WITH ISSUES")
            print(f"   Please review final_consolidation_report.json for details")
        
        print(f"\n📄 Full report saved to: final_consolidation_report.json")
        print("="*80)
        
        return final_report
        
    except Exception as e:
        logger.error(f"Consolidation failed: {e}")
        if executor.backup_created:
            print(f"\n🔄 To restore from backup:")
            print(f"   cp {backup_filename} hdm_papers.db")
        raise

if __name__ == "__main__":
    main()