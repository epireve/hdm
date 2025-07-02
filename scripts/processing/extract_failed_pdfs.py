#!/usr/bin/env python3
"""
Extract failed PDFs from conversion logs and create a CSV report
"""

import csv
import json
import re
from pathlib import Path

def extract_failed_pdfs():
    """Extract failed PDFs from checkpoint and logs"""
    
    # Read checkpoint file
    checkpoint_file = Path("checkpoint_markdown_papers.json")
    failed_pdfs = {}
    
    if checkpoint_file.exists():
        with open(checkpoint_file, 'r') as f:
            checkpoint = json.load(f)
            failed_pdfs = checkpoint.get('failed', {})
    
    # Also parse the terminal output that was captured
    # These are the errors from the timeout output
    terminal_errors = {
        "hitzler-et-al-2020-leveraging-knowledge-graphs-for-big-data-integration-the-xi-pipeline.pdf": "Timeout after 120s",
        "zep_temporal_kg_agent_memory_2025.pdf": "Timeout after 120s",
        "LLM+KG-1.pdf": "Timeout after 120s",
        "xu2015.pdf": "Timeout after 120s",
        "20746-13-24759-1-2-20220628.pdf": "Timeout after 120s",
        "cvf_open_access_d096d1c4_Quality_and_Relevance_Metrics_for_Selection_of_Multimodal_Pretraining_Data.pdf": "No such file or directory",
        "arxiv_arxiv_2102.02922_.pdf": "Timeout after 120s",
        "frontiers_dt_healthcare_systems.pdf": "Timeout after 120s",
        "arxiv_2307.04772_Digital_Twins_for_Patient_Care_via_Knowledge_Graph.pdf": "Timeout after 120s",
        "arxiv_2205.10123_Lifelong_Personal_Context_Recognition.pdf": "Timeout after 120s",
        "constructing_pkg_conversation_rl_2024.pdf": "Timeout after 120s",
        "978-3-030-59833-4_8.pdf": "Timeout after 120s",
        "arxiv_arxiv_2405.19877_KNOW_A_Real-World_Ontology_for_Knowledge_Capture_with_Large_Language_Models.pdf": "Timeout after 120s",
        "arxiv_2305.02077_An_Ontology_Design_Pattern_for_Role-Dependent_Name.pdf": "Timeout after 120s",
        "openaccess_thecvf_com_Quality_and_Relevance_Metrics_for_Selection_of_Multimodal_Pretraining_Data.pdf": "Timeout after 120s",
        "arxiv_2305.02077_An_Ontology_Design_Pattern_for_Role-Dependent_Names.pdf": "Timeout after 120s",
        "Lim-2010-Key-management-for-large-scale-dist.pdf": "Timeout after 120s",
        "arxiv_arxiv_2112.08025_TLogic_Temporal_Logical_Rules_for_Explainable_Link_Forecasting_on_Temporal_Knowledge_Graphs.pdf": "No output file created",
        "precision_nutrition_pkg_2024.pdf": "No output file created",
        "Cai-2023-Temporal-knowledge-graph-completion.pdf": "Timeout after 120s",
        "peerj-10-13861.pdf": "Timeout after 120s",
        "arxiv_2406.13791_IoT-Based_Preventive_Mental_Health_Using_Knowledge.pdf": "Timeout after 120s",
        "arxiv_arxiv_2208.07779_Steps_to_Knowledge_Graphs_Quality_Assessment.pdf": "Timeout after 120s",
        "arxiv_2208.07779_Steps_to_Knowledge_Graphs_Quality_Assessment.pdf": "Timeout after 120s",
        "0734.pdf": "Timeout after 120s",
        "Kuhlenkamp-2014-Benchmarking-scalability-and-elasti.pdf": "No such file or directory",
        "jmir_2023_digital_health_coaching_hpv.pdf": "Marker command failed",
        "pkg_ecosystem_survey_roadmap_2024.pdf": "Timeout after 120s",
        "arxiv_2304.09572_An_Ecosystem_for_Personal_Knowledge_Graphs_A_Surv.pdf": "Timeout after 120s",
        "arxiv_2308.06653_Smart_Knowledge_Transfer_using_Google-like_Search.pdf": "Marker command failed",
        "arxiv_2206.10212_A_Context_Model_for_Personal_Data_Streams.pdf": "Timeout after 120s",
        "connected_digital_twins_pkg_healthcare_2024.pdf": "Timeout after 120s",
        "arxiv_2304.09572_An_Ecosystem_for_Personal_Knowledge_Graphs_A_Survey_and_Research_Roadmap.pdf": "Timeout after 120s",
        "Platform_Development_for_Proof-of-Concept_of_Smartphone-based_Continuous_Complex_Positioning.pdf": "Timeout after 120s",
        "temporal_cognitive_arxiv_2502.00020_Temporal_Reasoning_in_AI_systems.pdf": "Timeout after 120s",
        "arxiv_2211.10011_Structural_Quality_Metrics_": "Timeout after 120s"
    }
    
    # Merge all failed PDFs
    papers_dir = Path("papers")
    for pdf_name, error in terminal_errors.items():
        pdf_path = papers_dir / pdf_name
        if pdf_path.exists():
            failed_pdfs[str(pdf_path)] = error
    
    # Create CSV report
    csv_file = Path("failed_pdf_conversions.csv")
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['PDF File', 'Error', 'File Size (MB)', 'Full Path'])
        
        for pdf_path, error in sorted(failed_pdfs.items()):
            pdf = Path(pdf_path)
            if pdf.exists():
                size_mb = pdf.stat().st_size / (1024 * 1024)
                writer.writerow([pdf.name, error, f"{size_mb:.2f}", str(pdf)])
            else:
                writer.writerow([pdf.name, error, "N/A", str(pdf)])
    
    print(f"Created failed_pdf_conversions.csv with {len(failed_pdfs)} failed PDFs")
    
    # Also check for successfully converted files
    markdown_dir = Path("markdown_papers")
    successful_count = len(list(markdown_dir.rglob("*.md"))) if markdown_dir.exists() else 0
    print(f"Successfully converted: {successful_count} PDFs")
    
    # Calculate statistics
    total_pdfs = len(list(papers_dir.glob("*.pdf")))
    print(f"\nConversion Statistics:")
    print(f"Total PDFs: {total_pdfs}")
    print(f"Failed: {len(failed_pdfs)} ({len(failed_pdfs)/total_pdfs*100:.1f}%)")
    print(f"Successful: {successful_count} ({successful_count/total_pdfs*100:.1f}%)")
    
    # Group errors by type
    error_types = {}
    for error in failed_pdfs.values():
        error_type = error.split(':')[0] if ':' in error else error
        error_types[error_type] = error_types.get(error_type, 0) + 1
    
    print(f"\nError Types:")
    for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  {error_type}: {count}")

if __name__ == "__main__":
    extract_failed_pdfs()