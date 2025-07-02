#!/usr/bin/env python3
"""
Main runner for Phase 2 processing with CSV support
Usage: python scripts/phase2/run_phase2_csv.py [--test] [--full] [--step STEP]
"""
import sys
import argparse
from pathlib import Path
import subprocess
import os

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import TEST_MODE, RESEARCH_TABLE_CSV, UPDATED_RESEARCH_TABLE_CSV
from utils import setup_logging


def main():
    """Run Phase 2 processing with CSV support"""
    # Parse arguments
    parser = argparse.ArgumentParser(description='Run Phase 2 processing with CSV support')
    parser.add_argument('--test', action='store_true', help='Run in test mode (process only 5 papers)')
    parser.add_argument('--full', action='store_true', help='Run in full mode (override TEST_MODE, process all papers)')
    parser.add_argument('--step', default='all', 
                       choices=['convert', 'update-table', 'analyze', 'standardize', 
                                'integrate-metadata', 'describe-images', 'reorganize', 'all'],
                       help='Which step to run')
    args = parser.parse_args()
    
    test = args.test
    full = args.full
    step = args.step
    
    logger = setup_logging("run_phase2_csv")
    
    # Determine mode
    if full:
        logger.info("Running in FULL MODE - will process ALL papers")
        mode_flag = "--full"
    elif test:
        logger.info("Running in TEST MODE - will process only 5 papers")
        mode_flag = "--test"
    else:
        logger.info(f"Running with default TEST_MODE={TEST_MODE}")
        mode_flag = "--test" if TEST_MODE else "--full"
    
    logger.info(f"Starting Phase 2 CSV processing - Step: {step}")
    
    steps_to_run = []
    if step == 'all':
        steps_to_run = ['convert', 'update-table', 'analyze', 'standardize', 
                       'integrate-metadata', 'describe-images', 'reorganize']
    else:
        steps_to_run = [step]
    
    # Execute steps
    for current_step in steps_to_run:
        logger.info(f"\n{'='*50}")
        logger.info(f"Running step: {current_step}")
        logger.info(f"{'='*50}\n")
        
        if current_step == 'convert':
            # Check if CSV already exists
            if RESEARCH_TABLE_CSV.exists():
                logger.info("research_table.csv already exists, skipping conversion")
                continue
            
            logger.info("Converting markdown table to CSV...")
            result = subprocess.run([
                sys.executable, 
                "scripts/phase2/convert_to_csv.py"
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Conversion failed: {result.stderr}")
                sys.exit(1)
            else:
                logger.info("Conversion completed successfully")
        
        elif current_step == 'update-table':
            logger.info("Updating research table CSV with cite_key column...")
            
            # Modify the script call based on mode
            cmd = [sys.executable, "scripts/phase2/research_table_updater_csv.py"]
            
            # For full mode, we need to temporarily modify TEST_MODE
            if full:
                # Create a temporary environment with TEST_MODE=False
                import os
                env = os.environ.copy()
                env['PHASE2_TEST_MODE'] = 'false'
                result = subprocess.run(cmd, capture_output=True, text=True, env=env)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Research table update failed: {result.stderr}")
                sys.exit(1)
            else:
                logger.info("Research table update completed successfully")
                
                # Check if output file was created
                output_file = UPDATED_RESEARCH_TABLE_CSV if test or TEST_MODE else RESEARCH_TABLE_CSV
                if output_file.exists():
                    logger.info(f"Updated CSV saved to: {output_file}")
        
        elif current_step == 'analyze':
            logger.info("Analyzing papers and generating cite keys...")
            
            cmd = [sys.executable, "scripts/phase2/paper_analyzer_csv.py"]
            if full:
                env = os.environ.copy()
                env['PHASE2_TEST_MODE'] = 'false'
                result = subprocess.run(cmd, capture_output=True, text=True, env=env)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Paper analysis failed: {result.stderr}")
                sys.exit(1)
            else:
                logger.info("Paper analysis completed successfully")
        
        elif current_step == 'standardize':
            logger.info("Standardizing markdown files...")
            
            cmd = [sys.executable, "scripts/phase2/markdown_standardizer_csv.py"]
            if full:
                env = os.environ.copy()
                env['PHASE2_TEST_MODE'] = 'false'
                result = subprocess.run(cmd, capture_output=True, text=True, env=env)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Markdown standardization failed: {result.stderr}")
                sys.exit(1)
            else:
                logger.info("Markdown standardization completed successfully")
        
        elif current_step == 'integrate-metadata':
            logger.info("Integrating metadata into markdown files...")
            
            cmd = [sys.executable, "scripts/phase2/metadata_integrator_csv.py"]
            if full:
                env = os.environ.copy()
                env['PHASE2_TEST_MODE'] = 'false'
                result = subprocess.run(cmd, capture_output=True, text=True, env=env)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Metadata integration failed: {result.stderr}")
                sys.exit(1)
            else:
                logger.info("Metadata integration completed successfully")
        
        elif current_step == 'describe-images':
            logger.info("Generating image descriptions...")
            
            cmd = [sys.executable, "scripts/phase2/image_descriptor_csv.py"]
            if full:
                import os as os_module  # Import with different name to avoid shadowing
                env = os_module.environ.copy()
                env['PHASE2_TEST_MODE'] = 'false'
                result = subprocess.run(cmd, capture_output=True, text=True, env=env)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Image description failed: {result.stderr}")
                sys.exit(1)
            else:
                logger.info("Image description completed successfully")
        
        elif current_step == 'reorganize':
            logger.info("Reorganizing folders with cite keys...")
            
            cmd = [sys.executable, "scripts/phase2/cite_key_reorganizer_csv.py"]
            if full:
                env = os.environ.copy()
                env['PHASE2_TEST_MODE'] = 'false'
                result = subprocess.run(cmd, capture_output=True, text=True, env=env)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Folder reorganization failed: {result.stderr}")
                sys.exit(1)
            else:
                logger.info("Folder reorganization completed successfully")
    
    logger.info("\n" + "="*50)
    logger.info("Phase 2 CSV processing completed!")
    logger.info("="*50)
    
    if test or (TEST_MODE and not full):
        logger.info("\nTest mode completed. Review the results before running full processing.")
        logger.info("To run full processing, use: --full flag")
        logger.info(f"\nOutput saved to: {UPDATED_RESEARCH_TABLE_CSV}")
    else:
        logger.info(f"\nFull processing completed. Output saved to: {RESEARCH_TABLE_CSV}")


if __name__ == "__main__":
    main()