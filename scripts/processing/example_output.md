# Example Output from Relevancy Analysis

## Sample Paper Before Processing

```csv
cite_key: smith_2023
title: "A Novel Approach to Heterogeneous Data Integration in Healthcare Knowledge Graphs"
Relevancy: [empty]
Relevancy Justification: [empty]
Summary: "This paper presents a comprehensive framework for integrating heterogeneous healthcare data sources..."
```

## Sample Paper After Processing

```csv
cite_key: smith_2023
title: "A Novel Approach to Heterogeneous Data Integration in Healthcare Knowledge Graphs"
Relevancy: SUPER
Relevancy Justification: "This paper directly addresses heterogeneous data integration in healthcare knowledge graphs, presenting a comprehensive framework that aligns perfectly with our research focus. The paper specifically tackles multi-modal data fusion from structured (EHR databases), semi-structured (HL7 messages), and unstructured (clinical notes) sources, demonstrating upstream data orchestration techniques and achieving significant improvements in entity resolution accuracy."
Summary: "This paper presents a comprehensive framework for integrating heterogeneous healthcare data sources..."
```

## Relevancy Distribution Example

After processing 100 papers, typical distribution might be:
- SUPER: 15 papers (15%)
- HIGH: 35 papers (35%)
- MEDIUM: 40 papers (40%)
- LOW: 10 papers (10%)

## Log File Example

```
2025-07-10 10:15:23 - INFO - Starting processing from index 0
2025-07-10 10:15:23 - INFO - Total papers to process: 358
2025-07-10 10:15:24 - INFO - Processing paper 1/358: smith_2023
2025-07-10 10:15:24 - INFO -   - Assessing relevancy for smith_2023
2025-07-10 10:15:25 - INFO -   - Relevancy: SUPER
2025-07-10 10:15:25 - INFO -   - Generating justification for smith_2023
2025-07-10 10:15:27 - INFO -   - Generated justification
2025-07-10 10:15:28 - INFO - Processing paper 2/358: jones_2024
...
```