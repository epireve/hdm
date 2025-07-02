#!/usr/bin/env python3
"""
Main runner for Phase 2 processing
Usage: python scripts/phase2/run_phase2.py [--test] [--step STEP]
"""
import sys
import click
from pathlib import Path
import subprocess

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import TEST_MODE
from utils import setup_logging


@click.command()
@click.option('--test', is_flag=True, help='Run in test mode (process only 5 papers)')
@click.option('--step', default='all', 
              type=click.Choice(['analyze', 'update-table', 'standardize', 'integrate-metadata', 
                                'describe-images', 'reorganize', 'all']),
              help='Which step to run')
def main(test, step):
    """Run Phase 2 processing"""
    logger = setup_logging("run_phase2")
    
    # Update config for test mode
    if test:
        logger.info("Running in TEST MODE - will process only 5 papers")
        # Note: This would need to be handled differently in production
        # For now, the TEST_MODE is set in config.py
    
    logger.info(f"Starting Phase 2 processing - Step: {step}")
    
    steps_to_run = []
    if step == 'all':
        steps_to_run = ['update-table', 'analyze', 'standardize', 
                       'integrate-metadata', 'describe-images', 'reorganize']
    else:
        steps_to_run = [step]
    
    # Execute steps
    for current_step in steps_to_run:
        logger.info(f"\n{'='*50}")
        logger.info(f"Running step: {current_step}")
        logger.info(f"{'='*50}\n")
        
        if current_step == 'update-table':
            logger.info("Updating research table with cite_key column...")
            result = subprocess.run([
                sys.executable, 
                "scripts/phase2/research_table_updater.py"
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Research table update failed: {result.stderr}")
                sys.exit(1)
            else:
                logger.info("Research table update completed successfully")
        
        elif current_step == 'analyze':
            logger.info("Analyzing papers and generating cite keys...")
            result = subprocess.run([
                sys.executable,
                "scripts/phase2/paper_analyzer.py"
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Paper analysis failed: {result.stderr}")
                sys.exit(1)
            else:
                logger.info("Paper analysis completed successfully")
        
        elif current_step == 'standardize':
            logger.info("Standardizing markdown files...")
            result = subprocess.run([
                sys.executable,
                "scripts/phase2/markdown_standardizer.py"
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Markdown standardization failed: {result.stderr}")
                sys.exit(1)
            else:
                logger.info("Markdown standardization completed successfully")
        
        elif current_step == 'integrate-metadata':
            logger.info("Integrating metadata into markdown files...")
            result = subprocess.run([
                sys.executable,
                "scripts/phase2/metadata_integrator.py"
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Metadata integration failed: {result.stderr}")
                sys.exit(1)
            else:
                logger.info("Metadata integration completed successfully")
        
        elif current_step == 'describe-images':
            logger.info("Generating image descriptions...")
            result = subprocess.run([
                sys.executable,
                "scripts/phase2/image_descriptor.py"
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Image description failed: {result.stderr}")
                if "GOOGLE_API_KEY" in result.stderr:
                    logger.error("Please set GOOGLE_API_KEY environment variable")
                sys.exit(1)
            else:
                logger.info("Image description completed successfully")
        
        elif current_step == 'reorganize':
            logger.info("Reorganizing folders with cite keys...")
            result = subprocess.run([
                sys.executable,
                "scripts/phase2/cite_key_reorganizer.py"
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Folder reorganization failed: {result.stderr}")
                sys.exit(1)
            else:
                logger.info("Folder reorganization completed successfully")
    
    logger.info("\n" + "="*50)
    logger.info("Phase 2 processing completed successfully!")
    logger.info("="*50)
    
    if test:
        logger.info("\nTest mode completed. Review the results before running full processing.")
        logger.info("To run full processing, run without --test flag")


if __name__ == "__main__":
    main()