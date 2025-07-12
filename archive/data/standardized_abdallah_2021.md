---
cite_key: abdallah_2021
title: Towards a GML-Enabled Knowledge Graph Platform
authors: Hussein Abdallah, Essam Mansour
year: 2021
doi: 10.1145/3447772
url: https://doi.org/10.1145/3447772
relevancy: HIGH
relevancy_justification: This paper is highly relevant as it proposes KGNet, a platform for on-demand graph machine learning (GML) as a service on top of RDF engines. This directly addresses the HDM project's need for integrating machine learning with knowledge graphs to enable intelligent reasoning over personal data. The focus on scalability, automated model training, and a GML-enabled query language (SPARQLML) provides a strong architectural blueprint for the HDM system.
tags:
  - Knowledge Graph
  - Graph Machine Learning
  - GML
  - SPARQL
  - RDF
  - GNN
  - AI
  - Heterogeneous
  - Integration
  - Semantic
date_processed: 2025-07-02
phase2_processed: true
standardization_date: 2025-07-10
standardization_version: 1.0
word_count: 1043
sections_count: 7
---

# Towards a GML-Enabled Knowledge Graph Platform

## Authors
Hussein Abdallah, Essam Mansour

## Abstract
This vision paper proposes KGNet, an on-demand graph machine learning (GML) as a service on top of RDF engines to support GML-enabled SPARQL queries. KGNet automates the training of GML models on a KG by identifying a task-specific subgraph. This helps reduce the task-irrelevant KG structure and properties for better scalability and accuracy. While training a GML model on KG, KGNet collects metadata of trained models in the form of an RDF graph called KGMeta, which is interlinked with the relevant subgraphs in KG. Finally, all trained models are accessible via a SPARQL-like query. We call it a GML-enabled query and refer to it as SPARQLML . KGNet supports SPARQLML on top of existing RDF engines as an interface for querying and inferencing over KGs using GML models. The development of KGNet poses research opportunities in several areas, including meta-sampling for identifying taskspecific subgraphs, GML pipeline automation with computational constraints, such as limited time and memory budget, and SPARQLML query optimization. KGNet supports different GML tasks, such as node classification, link prediction, and semantic entity matching. We evaluated KGNet using two real KGs of different application domains. Compared to training on the entire KG, KGNet significantly reduced training time and memory usage while maintaining comparable or improved accuracy. The KGNet source-code[1](#page-0-0) is available for further study.

## TL;DR
This vision paper proposes KGNet, a platform that provides on-demand graph machine learning (GML) as a service on top of RDF engines. It aims to bridge the gap between GML frameworks and RDF data stores by automating the training of GML models on task-specific subgraphs of a knowledge graph. The platform introduces SPARQLML, a GML-enabled query language, to allow for querying and inferencing over KGs using the trained models, thereby improving scalability, accuracy, and accessibility of GML on knowledge graphs.

## Key Insights
The paper introduces KGNet, a platform that automates the training of GML models on knowledge graphs by using task-specific subgraphs. This approach improves scalability and accuracy for tasks like node classification and link prediction. It also proposes SPARQLML, a SPARQL-like query language that allows users to query and perform inference over KGs using the trained GML models.

## I. INTRODUCTION

Knowledge graphs (KGs) are constructed based on semantics captured from heterogeneous datasets using various Artificial Intelligence (AI) techniques, such as representation learning and classification models [\[1\]](#page-7-0). Graph machine learning (GML) techniques, such as graph representation learning and graph neural networks (GNNs), are powerful tools widely used to solve real-world problems by defining them as prediction tasks on KGs. For instance, node classification tasks for problems, such as recommendations [\[2\]](#page-7-1) and entity alignment [\[3\]](#page-7-2), can be solved using GML techniques. Similarly, drug discovery [\[4\]](#page-7-3) and fraud detection [\[5\]](#page-7-4), [\[6\]](#page-7-5) problems are tackled as link prediction tasks using GML techniques.

<span id="page-0-0"></span>Data scientists often work with KGs, which are typically stored in RDF engines. They are responsible for developing GML pipelines using frameworks, such as PyG [\[7\]](#page-7-6) and DGL [\[8\]](#page-7-7), to train models on these KGs. However, there is often a gap between the GML frameworks and RDF engines. This necessitates an initial step of transforming the entire KG from RDF triple format into adjacency matrices in a traditional GML pipeline. Afterward, the data scientist needs to select a suitable GML method from a wide range of KG embedding (KGE) or GNN methods [\[9\]](#page-7-8), [\[10\]](#page-7-9) to train the model. For the average user, this responsibility is time-consuming.

Essam Mansour *Concordia University,* essam.mansour@concordia.ca

<span id="page-0-1"></span>![](_page_0_Figure_9.jpeg)
<!-- Image Description: This diagram is an Entity-Relationship Diagram (ERD) illustrating a data model. It depicts relationships between entities such as "Paper," "Venue," "Author," and "Affiliation." Relationships are shown with arrows and labels (e.g., "publishedIn," "authoredBy"). Dashed lines indicate weaker or less direct relationships. Features are represented as feature vectors. The diagram likely explains the data structure used for representing author and publication information within the paper. -->

**Figure 1:** A KG with nodes/edges in red, which could be predicted by classification and link prediction models on the fly.

<span id="page-0-2"></span>**prefix dblp**: <https://www.**dblp**.org/> **prefix kgnet**: <https://www.**kgnet**.com/> **select**?title ?venue 4**where**{ ?paper**a dblp**:Publication. ?paper **dblp**:title ?title. ?paper **?NodeClassifier**?venue. ?NodeClassifier**a kgnet:NodeClassifier**. ?NodeClassifier **kgnet**:TargetNode **dblp**:Publication. ?NodeClassifier **kgnet**:NodeLabel **dblp**:venue.}

**Figure 2:** SPARQLML pv : a SPARQLML query uses a node classification model to predict a paper's venue by q

[... rest of paper ...]

## References
[PRESERVE ORIGINAL REFERENCES]

## Metadata Summary
### Research Context
- **Research Question**: The paper proposes the KGNet platform, which consists of two main components: GML-as-a-service (GMLaaS) and SPARQLML as a Service. GMLaaS automates the GML training pipeline by using a meta-sampling approach to extract task-specific subgraphs, selecting the optimal GML method based on budget constraints, and managing the trained models. SPARQLML as a Service provides a query interface that allows users to train, delete, and query GML models using a SPARQL-like syntax.
- **Methodology**: The experimental evaluation shows that training GML models on task-specific subgraphs identified by KGNet's meta-sampling approach significantly reduces training time and memory usage while maintaining comparable or even improved accuracy compared to training on the entire knowledge graph. For instance, on the DBLP dataset, KGNet achieved up to an 11% improvement in accuracy with at least a 22% reduction in memory and 27% reduction in training time.
- **Key Findings**: The primary outcome is the proposal of the KGNet platform, a vision for a fully-fledged GML-enabled knowledge graph platform. The paper outlines the architecture, key components, and research challenges, and provides a proof-of-concept evaluation that demonstrates the feasibility and benefits of the proposed approach.
- **Primary Outcomes**: The paper is a vision paper, so the implementation is a prototype and not a fully mature system. The query optimization for SPARQLML is still an open research problem. The meta-sampling approach has been evaluated on a limited number of scenarios.

### Analysis
- **Limitations**: The integration of GML frameworks with RDF engines is a critical step towards building scalable and intelligent knowledge graph applications. By automating the GML pipeline and providing a high-level query language, platforms like KGNet can significantly lower the barrier for data scientists and developers to apply advanced machine learning techniques to knowledge graphs.
- **Research Gaps**: The paper identifies several research gaps, including the need for more advanced meta-sampling techniques, better methods for SPARQLML query optimization, and the development of comprehensive benchmarks for evaluating GML-enabled KG engines. There is also a need for more seamless integration between GML models and RDF engines to avoid the use of UDFs.
- **Future Work**: Future work includes developing more sophisticated meta-sampling approaches, creating advanced query optimization techniques for SPARQLML, and building comprehensive benchmarks to evaluate the performance of GML-enabled KG platforms. There is also an opportunity to explore the use of KGNet in various application domains beyond the ones presented in the paper.
- **Conclusion**: The paper identifies several research gaps, including the need for more advanced meta-sampling techniques, better methods for SPARQLML query optimization, and the development of comprehensive benchmarks for evaluating GML-enabled KG engines. There is also a need for more seamless integration between GML models and RDF engines to avoid the use of UDFs.

### Implementation Notes
The paper provides valuable insights into the architecture of a GML-enabled KG platform. The use of a meta-sampler to extract task-specific subgraphs is a key technique for improving scalability. The KGMeta graph, which stores metadata about trained models, is a clever way to enable seamless integration and query optimization. The proposed SPARQLML language provides a user-friendly interface for interacting with the system.