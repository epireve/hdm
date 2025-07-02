---
cite_key: "arxiv_230302166_towards_a_gml_"
title: "Towards a GML-Enabled Knowledge Graph Platform"
authors: "Hussein Abdallah, Essam Mansour"
year: 2021
doi: "10.1145/3447772)"
date_processed: "2025-07-02"
phase2_processed: true
original_folder: "arxiv_2303.02166_Towards_a_GML-Enabled_Knowledge_Graph_Platform"
images_total: 9
images_kept: 9
images_removed: 0
---

# Towards a GML-Enabled Knowledge Graph Platform

Hussein Abdallah *Concordia University,*hussein.abdallah@concordia.ca
*Abstract*—This vision paper proposes KGNet, an on-demand graph machine learning (GML) as a service on top of RDF engines to support GML-enabled SPARQL queries. KGNet automates the training of GML models on a KG by identifying a task-specific subgraph. This helps reduce the task-irrelevant KG structure and properties for better scalability and accuracy. While training a GML model on KG, KGNet collects metadata of trained models in the form of an RDF graph called KGMeta, which is interlinked with the relevant subgraphs in KG. Finally, all trained models are accessible via a SPARQL-like query. We call it a GML-enabled query and refer to it as SPARQLML . KGNet supports SPARQLML on top of existing RDF engines as an interface for querying and inferencing over KGs using GML models. The development of KGNet poses research opportunities in several areas, including meta-sampling for identifying taskspecific subgraphs, GML pipeline automation with computational constraints, such as limited time and memory budget, and SPARQLML query optimization. KGNet supports different GML tasks, such as node classification, link prediction, and semantic entity matching. We evaluated KGNet using two real KGs of different application domains. Compared to training on the entire KG, KGNet significantly reduced training time and memory usage while maintaining comparable or improved accuracy. The KGNet source-code[1](#page-0-0) is available for further study.

## I. INTRODUCTION

Knowledge graphs (KGs) are constructed based on semantics captured from heterogeneous datasets using various Artificial Intelligence (AI) techniques, such as representation learning and classification models [\[1\]](#page-7-0). Graph machine learning (GML) techniques, such as graph representation learning and graph neural networks (GNNs), are powerful tools widely used to solve real-world problems by defining them as prediction tasks on KGs. For instance, node classification tasks for problems, such as recommendations [\[2\]](#page-7-1) and entity alignment [\[3\]](#page-7-2), can be solved using GML techniques. Similarly, drug discovery [\[4\]](#page-7-3) and fraud detection [\[5\]](#page-7-4), [\[6\]](#page-7-5) problems are tackled as link prediction tasks using GML techniques.

<span id="page-0-0"></span>Data scientists often work with KGs, which are typically stored in RDF engines. They are responsible for developing GML pipelines using frameworks, such as PyG [\[7\]](#page-7-6) and DGL [\[8\]](#page-7-7), to train models on these KGs. However, there is often a gap between the GML frameworks and RDF engines. This necessitates an initial step of transforming the entire KG from RDF triple format into adjacency matrices in a traditional GML pipeline. Afterward, the data scientist needs to select a suitable GML method from a wide range of KG embedding (KGE) or GNN methods [\[9\]](#page-7-8), [\[10\]](#page-7-9) to train the model. For the average user, this responsibility is time-consuming.

Essam Mansour *Concordia University,*essam.mansour@concordia.ca

<span id="page-0-1"></span>![](_page_0_Figure_9.jpeg)
<!-- Image Description: This diagram is an Entity-Relationship Diagram (ERD) illustrating a data model. It depicts relationships between entities such as "Paper," "Venue," "Author," and "Affiliation." Relationships are shown with arrows and labels (e.g., "publishedIn," "authoredBy"). Dashed lines indicate weaker or less direct relationships. Features are represented as feature vectors. The diagram likely explains the data structure used for representing author and publication information within the paper. -->

Fig. 1: A KG with nodes/edges in red, which could be predicted by classification and link prediction models on the fly.

<span id="page-0-2"></span>**prefix dblp**: <https://www.**dblp**.org/> **prefix kgnet**: <https://www.**kgnet**.com/> **select**?title ?venue 4**where**{ ?paper**a dblp**:Publication. ?paper **dblp**:title ?title. ?paper **?NodeClassifier**?venue. ?NodeClassifier**a kgnet:NodeClassifier**. ?NodeClassifier **kgnet**:TargetNode **dblp**:Publication. ?NodeClassifier **kgnet**:NodeLabel **dblp**:venue.}

Fig. 2: SPARQLML pv : a SPARQLML query uses a node classification model to predict a paper's venue by querying and inferencing over the KG shown in Figure [1.](#page-0-1)

Furthermore, the trained models are isolated from the RDF engine, where the KG is stored. Therefore, automating the training of GML models on KGs and providing accessibility to the trained models via a SPARQL-like query is essential. We refer to this query as a SPARQLML query.

The KG shown in Figure [1](#page-0-1) contains information about published papers in DBLP [\[11\]](#page-7-10). However, the traditional SPARQL query language cannot be used to apply GML models on top of a KG, such as predicting a node's class or a missing affiliation link for an author. For instance, the venue node in Figure [1](#page-0-1) is a virtual node that could be predicted using a node classification (NC) model. It would be fascinating to query this KG using a GML model for NC through a SPARQL-like query to obtain the paper-venue node, as shown in the SPARQLML pv in Figure [2.](#page-0-2) This query uses a model of type *kgnet:NodeClassifier*to predict a venue for each paper. The SPARQLML triple patterns in lines 8-10 will retrieve all models of type*kgnet:NodeClassifier*that predict a class of type*dblp:venue*. In the triple pattern h?paper, ?NodeClassifier, ?venuei, we refer to *?NodeClassifier* as a user-defined predicate.

Enabling queries like SPARQLML pv , shown in Figure [2,](#page-0-2) presents several challenges. These include: (*i*) automatically training GML models for various tasks, (*ii*) optimizing SPARQLML for GML model selection based on accuracy and inference time, and (*iii*) efficiently interacting with the selected model during query execution. Additionally, seamless integration of GML models into RDF engines is necessary. As a result, users should be able to express their SPARQLML queries easily by following the SPARQL logic of pattern matching, avoiding the explicit use of user-defined functions (UDFs).

There is a growing adoption of integrating GML with existing graph databases, such as Neo4j [\[12\]](#page-7-11) or Stardog [\[13\]](#page-7-12). However, while these databases offer some machine learning primitive methods, such as PageRank and shortest-path using the *Cypher*language, they do not address the challenges of integrating GML models with RDF engines. For example, Neo4j Graph Data Science [\[14\]](#page-7-13) supports limited graph embedding methods in a beta version, such as FastRP [\[15\]](#page-7-14), Node2Vec [\[16\]](#page-8-0), and Graph-SAGE [\[17\]](#page-8-1). However, a user must train the models separately as an initial step. To address these challenges, there is a need to bring GML to data stored in RDF engines instead of getting data to machine learning pipelines. This would encourage the development of KG data science libraries powered by the expressiveness of SPARQL, enabling better analysis and insight discovery based on KG structure and semantics. These libraries would empower data scientists with a full breadth of KG machine learning services on top of KGs stored in RDF engines.

This vision paper proposes KGNet, an on-demand GMLas-a-service on top of RDF engines to support SPARQLML queries, as illustrated in Figure [3.](#page-1-0) KGNet extends existing RDF engines with two main components GML-as-aservice (GMLaaS) and SPARQLML as a Service. KGNet automatically trains a GML model on a KG for tasks, such as node classification or like prediction, and maintains metadata of the trained model as an RDF graph called*KGMeta*. To reduce training time and memory usage while improving accuracy on a specific task A, KGNet performs meta-sampling to identify a task-specific subgraph KG<sup>0</sup> of the larger KG that preserves essential characteristics relevant to A. This enables KGNet to scale on large KGs. GMLaaS is in charge of: (*i*) selecting the near-optimal GML method for training A using KG<sup>0</sup> based on a given time or memory budget, and (*ii*) communicating with RDF engines via HTTP calls requesting inferencing of a specific trained model, (*iii*) storing the trained models and embeddings related to KGs. The SPARQLML service transparently: (*i*) maintains and interlinks the KGMeta with associated KGs, (*ii*) optimizes the GML model selection for a user-defined predicate, and (*iii*) finally rewrites the SPARQLML query as a SPARQL query.

In summary, the contributions of this paper are:

- a fully-fledged GML-enabled KG platform[2](#page-1-1) on top of existing RDF engines.
- GML-as-a-service to provide automatic training of GML models based on a given memory or time budget.

<span id="page-1-1"></span><sup>2</sup><https://github.com/CoDS-GCS/KGNET>

<span id="page-1-0"></span>![](_page_1_Figure_7.jpeg)
<!-- Image Description: This diagram depicts an architecture for a SPARQL-ML service. It shows two main components: a "GML as a Service" section with inference and training managers using embeddings and models via HTTP calls, and a "SPARQLML as a Service" section with a query manager (parser, re-writer, optimizer) interacting with a KGMeta governor and meta sampler. The system uses an RDF engine (Apache Jena, Star-dog, Openlink-Virtuoso) and exchanges metadata (A, KG') between the components. The purpose is to illustrate the system's workflow and the interaction between GML and SPARQL-ML components. -->

Fig. 3: The KGNet architecture, which provides an interface language (SPARQLML) and enables AI applications and data scientists to automatically train GML models on top of KGs for querying and inferencing KGs based on the trained models.

This automatic training utilizes task-specific subgraphs extracted using our meta-sampling approach.

- SPARQLML as a Service to perform meta-sampling, maintain training meta-data in KGMeta, and optimize the GML model selection, i.e., opt for the near-optimal model based on constraints on accuracy and inference time.
- A comprehensive evaluation with different GML methods using three GML tasks on real KGs. Our experiments show that KGNet achieved comparable or improved accuracy compared to training on the entire KG, while significantly reducing training time and memory usage.

The remainder of this paper is organized as follows. Section [II](#page-1-2) provides a background about existing graph machine learning pipelines. Section [III](#page-2-0) outlines the main research challenges of developing a GML-enabled KG engine. Section [IV](#page-3-0) presents the KGNet platform. Section [V](#page-5-0) discusses the results of evaluating our automated pipeline for training GML models. Sections [VI](#page-6-0) and [VII](#page-7-15) are related work and conclusion.

### II. BACKGROUND: ML PIPELINES FOR KGS

<span id="page-1-2"></span>ML pipelines developed to train models on a KG can be grouped into three main categories: (*i*) traditional ML on KG data in tabular format, (*ii*) traditional ML on KG embeddings, and (*iii*) graph neural networks (GNNs) trained directly on the KG. In the traditional ML approach using KG data in tabular format, data from the KG is transformed into inmemory data frames, and classical ML classifiers are trained using feature engineering techniques and libraries, such as Scikit-Learn or SparkMLib. In contrast, traditional ML on KG embeddings avoids the feature engineering process and generates embeddings for nodes and edges. Apple Saga [\[18\]](#page-8-2) is an example of this approach, which uses graph ML libraries like DGL-KE [\[8\]](#page-7-7) to generate KG embeddings. Data scientists have the flexibility to choose the ML method for training.

GNNs have gained significant popularity in recent years. Hence, data scientists frequently utilize them to perform GML tasks. The Open Graph Benchmark (OGB) [\[19\]](#page-8-3) standardized the GNN training pipeline, emphasizing the best practices for tackling GML tasks and building a GNN training pipeline. Figure [4](#page-2-1) summarizes this pipeline, which involves encoding

<span id="page-2-1"></span>![](_page_2_Figure_0.jpeg)
<!-- Image Description: The image displays a flowchart illustrating the GML (Graph Machine Learning) framework. It shows data flowing from a Graph Database (CSV input) through a Dataset Transformer (encoding and adjacency matrix creation), resulting in sparse matrices fed into the GML method (training and inferencing). The flowchart details the stages of data processing and model application within the framework. -->

Fig. 4: A traditional GML pipeline [\[19\]](#page-8-3) using a GML framework. The pipeline starts with extracting the graph data, followed by data transformation into sparse matrices to train models for a GML task. Finally, the inference step is ready to predict results in isolation from the graph databases.

KG nodes and edges, generating adjacency matrices, loading them into memory, and training GNNs using specific methods. Various GML frameworks, such as DGL [\[8\]](#page-7-7) and PyG [\[7\]](#page-7-6), offer multiple implementations of GNN methods. These frameworks support data transformation by loading graphs into memory as graph data structures and applying transformations. However, existing GML frameworks require significant memory and processing time for large KGs and a deep understanding of various GNN methods. In comparison, the OGB pipeline is simple, but it is a semi-automated process that necessitates human intervention and ML expertise to construct an effective pipeline and select an appropriate GNN method. Data scientists may choose the most appropriate GNN method based on various constraints, such as time or memory limitations. Furthermore, as depicted in Figure [4,](#page-2-1) the separation of the trained models from the KG engines adds an extra layer of complexity for data scientists to apply their models when inferring the KG.

#### <span id="page-2-0"></span>III. CHALLENGES OF GML-ENABLED KG ENGINE

This section highlights the open research challenges and opportunities raised by developing GML-enabled KG Engine.

## *A. Automatic Training: Method Selection and Meta-sampling*There are numerous methods for training models for GML tasks, as summarized in Figure [5.](#page-2-2) These methods could be classified mainly into two categories KG embeddings (KGE) or graph neural network (GNN) methods. Examples of KGE methods are TransE, RotatE, ComplEx, and DistMult [\[10\]](#page-7-9). Some GNN methods support sampling on full graph, such as Graph-SAINT [\[20\]](#page-8-4), Shadow-SAINT [\[21\]](#page-8-5), and MorsE [\[22\]](#page-8-6). Examples of GNN full-batch training (without sampling) methods are RGCN [\[23\]](#page-8-7) and GAT [\[24\]](#page-8-8). Our taxonomy has more categories, as shown in Figure [5.](#page-2-2)

GML methods vary significantly in terms of their accuracy, training time, and memory requirements. Furthermore, the complexity of each GML task may differ depending on various factors, such as the size of KGs and the number of node/edge types related to the task. For example, link prediction can be more resource-intensive than node classification. Different

<span id="page-2-2"></span>![](_page_2_Figure_8.jpeg)
<!-- Image Description: The image is a hierarchical flowchart categorizing graph embedding methods. It branches from "Graph Embedding" into "KGE" (Knowledge Graph Embedding) methods (Semantic, DistMult, ComplEx, Translational) and "GNN" (Graph Neural Network) methods. GNNs are further divided into homogeneous and heterogeneous networks, with subcategories including sampling (node/layer, subgraph) and propagation (spectral, attentional) techniques. Specific algorithms under each category are listed. The purpose is to provide a comprehensive overview of the different approaches to graph embedding. -->

Fig. 5: A taxonomy of methods for training GML models.

GML methods may perform differently under the same budget constraints, and selecting the best method can depend on several factors. Hence, automating a training pipeline for a specific GML task based on a user's budget for time and memory is challenging. For instance, some GML methods perform fullbatch training, which requires more memory budget. These methods require huge memory to train models on large KGs. Some other GNN methods may suffer from over-smoothing, which can cause accuracy degradation. Sampling-based GNN (mini-batch training) methods use different types of sampling, which vary in avoiding these limitations. Therefore, automating the selection of GML methods for a specific task based on a given time or memory budget is challenging.

Real KGs can contain millions to billions of triples, such as DBLP [\[11\]](#page-7-10) and MAG [\[25\]](#page-8-9). However, training GML models on these large KGs requires colossal computing resources that exceed the capabilities of a single machine. As a result, there is a need for identifying a smaller training dataset of the KG, which is specific to the task at hand. This process is known as meta-sampling. It has been proposed in various application domains, including computer vision [\[26\]](#page-8-10), [\[27\]](#page-8-11) and speech recognition [\[28\]](#page-8-12), to extract a training dataset that is tailored to the given task. In the context of GML, meta-sampling presents an opportunity to optimize training models on large KGs by selecting a representative sub-graph that is relevant to the task. This approach can help reduce time and memory requirements without sacrificing accuracy. Therefore, exploring the potential benefits of using meta-sampling in training GML models to extract task-specific subgraphs is crucial. By doing so, we can improve the efficiency and effectiveness of GML methods on large-scale KGs. This raises a research opportunity to explore different meta-sampling approaches for GML methods on large knowledge graphs (KGs).

###*B. Seamless Integration Between GML Models and KGs*Enabling GML on top of RDF engines poses significant challenges, mainly interfacing between the trained models and the underlying data management engine. One common approach is to use user-defined functions (UDFs) to implement this interface [\[29\]](#page-8-13)–[\[31\]](#page-8-14). However, this comes with a cost for query optimizations in data systems [\[32\]](#page-8-15). The existence of an extensive catalog of UDFs can limit the expressiveness of MLbased queries. For instance, a large catalog of UDFs makes it difficult for users to choose between UDFs and find the

<span id="page-3-1"></span>![](_page_3_Figure_0.jpeg)
<!-- Image Description: This flowchart illustrates a system for automated graph machine learning (GML). It shows the stages: input (GML task, subgraph, budget, specifications); dataset transformation (preprocessing, adjacency matrix generation, train-test split); optimal GML method selection (considering GNN methods, budget, resources); GML model training (using libraries like DGL and PyG); and GML inference via a REST API, outputting results in JSON format. A key component is the GML optimizer which selects the best GNN (GCN, RGCN, etc.) based on resource constraints. -->

Fig. 6: The automation of training pipeline and inference in our GML-as-a-service (GMLaaS). GMLaaS interacts with the KGMeta Manager to train a model for a specific task with limited budget. The automated pipeline opt to the near-optimal GML method for training a model within a limited budget. GMLaaS supports task inference through RestAPI that is called by a UDF.

right one for their needs. Most existing query optimizers do not have models estimating the cost of these UDFs. Hence, automating the query optimization of SPARQLML queries is challenging. There is a research opportunity for seamless integration between trained GML models and RDF. To address these challenges, we proposed KGMeta as a graph representation of metadata of trained models interlinked with the KGs.

#*C. Optimizing SPARQL*ML *Queries and Benchmarks*User-defined predicates were first proposed for SQL [\[33\]](#page-8-16). In SPARQLML, a user-defined predicate is used to get a prediction from one of the trained models associated with a specific node in the graph. Estimating the cost of evaluating a user-defined predicate is more complex than estimating the cost of a traditional RDF predicate. While cardinality estimation is used to optimize only the execution time for the latter, a user-defined predicate in a SPARQLML query can be inferred by multiple models, each with varying accuracy and inference time. RDF engines are unaware of this information, leading to the problem of selecting the best model for inference.

For a SPARQLML query, the inference step in an RDF engine using a chosen model is a challenging task that requires optimization, specifically for rank-ordering the inference process. The challenge lies in deciding whether to perform the inference in a single call to a UDF or per instance, which may result in an extensive number of UDF calls. Additionally, each model has a unique cardinality, i.e., the total number of predictions it can make. This makes predicting rank-ordering complex as RDF engines lack accurate estimation of UDF costs.

To address these challenges, there are research opportunities for developing benchmarks to evaluate optimization approaches for SPARQLML queries. These benchmarks should consider various models for different user-defined predicates and be designed to work with large datasets. Furthermore, each SPARQLML query should vary in the number of user-defined predicates and be associated with variables of different cardinalities. This will enable a comprehensive evaluation of the performance and scalability of varying optimization approaches for SPARQLML queries.

## IV. THE KGNET PLATFORM

<span id="page-3-0"></span>KGNet provides two main services, namely GML as a Service (GMLaaS) and SPARQLML as a Service on top of existing RDF engines, as shown in Figure [3.](#page-1-0)

###*A. GML as a Service (GMLaaS)*Random Comunity KGNet is a platform that offers end-to-end automation of GML training on KGs, as depicted in Figure [6.](#page-3-1) The platform provides*GMLaaS*, a Restful service that manages GML models in terms of automatic training and interactive inferencing. Additionally, it utilizes an embedding store to facilitate entity similarity search tasks by computing the similarity between embedding vectors. The *GML training manager*automates the training pipeline per task. However, the automation of GML training on KGs is challenging due to the complexity and size of KGs. Therefore, KGNet leverages our meta-sampling approach to optimize the training process by selecting a taskspecific subgraph (KG<sup>0</sup> ) that is specific to the given task. This step helps reduce the time and memory required without trading accuracy. The pipeline takes as input a task-specific subgraph (KG<sup>0</sup> ), the GML task, the task budget, and the available resources within the ML environment.

The*Data Transformer*step converts the subgraph into a sparse-matrix format optimized for in-memory and matrix operations. This format is compatible with popular graph ML data loaders, such as Py-Geometric and DGL, and is ideal for sparse KGs. Our pipeline ensures data consistency by validating node/edge types counts, removing literal data and target class edges, and generating graph statistics. We also perform a train-validation-test split using different strategies like random and community-based. KGNet automates this transformation, making ad-hoc GML training queries possible.

The*Optimal GML Method Selection*step selects the best GML method for a given task. KGNet supports various GNN methods, including GCN, RGCN, Graph-SAINT, Shadow-SAINT, Morse, and KGE methods such as ComplEx. We estimate the required memory for each method based on the size and the number of generated sparse-matrices, as well as the training time based on the matrix dimensions and feature aggregation approach. Moreover, we estimate the training time

<span id="page-4-0"></span>![](_page_4_Figure_0.jpeg)
<!-- Image Description: This image presents two diagrams (A and B) illustrating the architecture of link prediction and node classification tasks. Each diagram uses a graph structure showing the relationships between tasks (e.g., Link Predictor Task, Node Classifier Task), data sources (dblp:Person, dblp:Publication), models (GML Model), and evaluation metrics (MRR Score, F1 Score). The diagrams highlight the flow of information and dependencies between different components within each task. Dashed lines represent relationships, and solid lines show direct dependencies. -->

Fig. 7: A KGMeta graph of two trained models for node classification and link prediction tasks. The white nodes are nodes from the original data KG. The dashed nodes/edges are metadata collected per trained model.

```text
1 prefix dblp:<https://www.dblp.org/>
2 prefix kgnet:<https://www.kgnet.com/>
3 Insert into <kgnet> { ?s ?p ?o }
4 where {select* from kgnet.TrainGML(
5 {Name: 'MAG_Paper-Venue_Classifer',
6 GML-Task:{ TaskType:kgnet:NodeClassifier,
7 TargetNode: dblp:publication,
8 NodeLable: dblp:venue},
9 Task Budget:{ MaxMemory:50GB, MaxTime:1h,
10 Priority:ModelScore} } )};
```text

Fig. 8: A SPARQLML insert query that trains a paper-venue classifier on DBLP. The TrainGML function is a UDF that is implemented inside the RDF engine.

based on the dimension of the sparse-matrices and GNN neighbour nodes features aggregation approach adopted by each method. For GNN sampling-based methods, the sampling cost basically depends on the sampling heuristic used [\[34\]](#page-8-17). Thus, we are working on a more advanced estimation method based on sampling the sparse-matrices and running a few epochs on them.

KGNet's GML-optimizer determines the necessary resources for each method and optimizes the training settings, ensuring scalability in distributed environments. The automated pipeline trains a model and collects evaluation metrics and inference time statistics. A URI is generated for the trained model to distinguish it from other models used for inference tasks. The model meta-data is returned to the KGMeta Manager to update the KGMeta graph. Figure [7.](#page-4-0)a and b show the generated meta-data for link prediction and node classification models, respectively. The *Embedding Store*sub-component, shown in Figure [3,](#page-1-0) is used for fast similarity search by storing, indexing, and searching embeddings. The*GML Inferencing*receives HTTP calls for inference, serializes the result into a JSON Restful-API response, and sends it back to the RDF engine, as shown in Figure [3.](#page-1-0) The current version uses FAISS embedding store [\[35\]](#page-8-18) to enable ad-hoc queries for node similarity search.

- <span id="page-4-2"></span>1**prefix dblp**:<https://www.**dblp**.org/>
- 2 **prefix kgnet**:<https://www.**kgnet**.com/>

```text
3 delete {?NodeClassifier ?p ?o}
```text

4 **where**{

```text
5 ?NodeClassifier a kgnet:NodeClassifier.
```text

- 6 ?NodeClassifier**kgnet**:TargetNode **dblp**:Publication.
- 7 ?NodeClassifier **kgnet**:NodeLabel **dblp**:venue.}

Fig. 9: A SPARQLML delete query that deletes a trained model and its meta-data.

```text
1 prefix dblp: <https://www.dblp.com/>
```text

2 **prefix kgnet**: <https://www.**kgnet**.com/>

- 3 **select**?author ?affiliation
- 4**where**{ ?author**a dblp**:person.
- 5 ?author ?**LinkPredictor** ?affiliation.
- 6 ?**LinkPredictor a kgnet:LinkPredictor**.
- 7 ?**LinkPredictor kgnet**:SourceNode **dblp**:person.
- 8 ?**LinkPredictor kgnet**:DestinationNode **dblp**:affiliation.
- 9 ?**LinkPredictor kgnet**:TopK-Links 10.}

Fig. 10: A SPARQLML query predicting author affiliation link (edge) on DBLP KG.

# *B. The SPARQL*ML *as a Service*

We offer a SPARQLML as a Service, which comprises three main components: Query Manager, KGMeta Governor, and Meta-sampler. In addition, we provide an interfacing language called SPARQLML that enables users to express SPARQLlike queries for INSERT, DELETE, or SELECT operations, such that: (*i*) a SPARQLML *INSERT* query is used to train a GML model and maintain its metadata in KGMeta (as shown in Figure [8\)](#page-4-1), (*ii*) a SPARQLML *DELETE* query is used to delete trained model files and associated embeddings from the GML-aaS component and then deletes its metadata from the KGMeta (as in Figure [9\)](#page-4-2), (*iii*) a SPARQLML *SELECT*query is for querying and inferencing the KG, e.g., the query in Figure [10.](#page-4-3) When a SPARQLML query is received, the Query Manager parses it. An INSERT or DELETE query is sent to the KGMeta Governor. If it is a SELECT query, it is optimized and rewritten as a SPARQL query.
*1) KGMeta Governor:*The KGMeta Governor maintains a KGMeta graph for each KG, using statistics and metadata collected from trained GML models specific to that KG. The INSERT query is a request to train a task on a certain KG. The parsed information includes the task type (such as node classification or link prediction), the task inputs (such as the target nodes and classification labels (Y classes) for a classification task), and a budget (such as memory and time budget). Experienced ML users can provide additional information, such as hyperparameters or a specific GML method. This information is encapsulated as a JSON object, as shown in Figure [8.](#page-4-1) At line 4, the*TrainGML*is a UDF that takes as input a JSON object that encapsulates all required information to train a GML model. The KGMeta Governor sends the task to the meta-sampler to obtain a task-specific subgraph (KG<sup>0</sup> ) for the given task. Then governor interacts with the GML Training Manager to automate the training

```text
1 prefix dblp: <https://www.dblp.org/>
2 prefix kgnet: <https://www.kgnet.com/>
3 select ?title
4 sql:UDFS.getNodeClass($m,?paper) as ?venue
5 where {
6 ?paper a dblp:Publication.
7 ?paper dblp:title ?title.
8 }
```text

Fig. 11: A candidate SPARQL for SPARQLML pv

pipeline for this task. Once training is complete, the KGMeta Governor receives the trained model's metadata, including accuracy and inference time, to maintain the KGMeta, as illustrated in Figure [7.](#page-4-0)
*2) Meta-sampler:* Our meta-sampler aims to identify a task-specific subgraph (KG<sup>0</sup> ) for training a GML task. Each GML task targets nodes of a specific type, such as dblp:Publication in SPARQLML pv . Our meta-sampler extracts a task-specific subgraph (KG<sup>0</sup> ), which comprises a set of triples with representative triples associated with the target nodes. Based on the KG schema structure the size of KG<sup>0</sup> is much smaller than the size of KG. This smaller size will optimize training time and require less memory for training the GML task A. However, the KG may contain triples that are not reachable from a target node v <sup>T</sup> or connected via more than three hops from v T . These triples do not assist the model in generalizing and may lead to over-smoothing problems [\[36\]](#page-8-19), [\[37\]](#page-8-20).

Our SPARQL-based meta-sampling method determines the scope of the extracted subgraph based on two parameters: (*i*) the direction d, where d = 1 for outgoing and d = 2 for bidirectional (i.e., both outgoing and incoming), and (*ii*) the number of hops h. We evaluated the performance of our method using four combinations of d ∈ {1, 2} and h ∈ {1, 2}. Our metasampling approach achieved better results with d = 1 and h = 1 for node classification, whereas for link prediction, our metasampling method performed better with d = 2 and h = 1.

*3) The Query Manager:*The Query Manager is responsible for optimizing SPARQLML queries for model selection and rank-ordering to evaluate user-defined predicates. In the case of SPARQLML pv shown in Figure [2,](#page-0-2) the query optimizer fetches all URIs of the models satisfying the conditions associated with the user-defined predicate*?NodeClassifier*. The KGMeta is an RDF graph containing optimizer statistics, such as model accuracy, inference time, and model cardinality. Therefore, we use a SPARQL query to obtain the models' URIs, accuracy, inference time, and cardinality. The query optimizer selects the near-optimal GML model that achieves high accuracy and low inference time. We define this problem as an integer programming optimization problem to minimize total execution time or maximize inference accuracy.

The *SPARQL*ML *Query Re-writer*uses the near-optimal GML model with URI m to generate a candidate SPARQL query. KGNet currently supports two possible execution plans, whose query templates are shown in Figures [11](#page-5-1) and [12.](#page-5-2) The core idea is to map a user-defined predicate into a user-defined function (UDF), such as*sql:UDFS.getNodeClass*, to send HTTP calls during the execution time to the GML Inference

```text
1 prefix dblp: <https://www.dblp.org/>
2 prefix kgnet: <https://www.kgnet.com/>
3 select ?title
4 sql:UDFS.getKeyValue(?venues_dic,?paper) as ?venue
5 where {
6 ?paper a dblp:Publication.
7 ?paper dblp:title ?title.
8 {select sql:UDFS.getNodeClass($m,dblp:Publication)
9 as ?venues_dic where { } }}
```text

Fig. 12: A candidate SPARQL for SPARQLML pv

Manager in our GMLaaS to get inference based on the pretrained model m. The number of HTTP calls may dominates the query execution cost. For example, SPARQLML pv predicts the venue of all papers, whose size is |?papers|.

The query template shown in Figure [11](#page-5-1) will generate |?papers| HTTP calls. However, the query template shown in Figure [12](#page-5-2) reduces the number of HTTP calls to one by enforcing an inner select query constructing a dictionary of all papers and their predicted venues. Then, *sql:UDFS.getKeyValue*is used to look up the venue of each paper. Our query optimizer decomposes the triple patterns related quering the KG triples in the SPARQLML query into sets per variable associated with a user-defined predicate. For example, in the SPARQLML pv query shown in Figure [2,](#page-0-2) our optimizer identifies two triple patterns that match the variable*?paper*and one triple pattern that matches the variable*?venue*. We use a SPARQL query to get the cardinality of each set, which is the number of distinct values of the variable in the dataset. We formulate this problem as another integer programming optimization problem [\[38\]](#page-8-21) that minimizes the total number of HTTP calls or minimizes the constructed dictionary size, which is based on the model cardinality. For instance, in the query shown in Figure [12,](#page-5-2) our optimizer generates a dictionary of all papers and their predicted venues, which is then used to retrieve the venue of each paper using the UDF *sql:UDFS.getKeyValue*.

## V. EXPERIMENTAL EVALUATION

<span id="page-5-0"></span>This section analyzes the ability of KGNet in automating pipelines to train a model for a specific task with less time and memory w.r.t traditional pipelines on full graphs.

### *A. Evaluation Setup*Compared Methods: We used RGCN [\[23\]](#page-8-7) as a full-batch training method and GraphSAINT [\[20\]](#page-8-4), ShadowSAINT [\[21\]](#page-8-5) as mini-batch sampling-based methods for node classification and MorsE [\[22\]](#page-8-6) as edge sampling-based method for link prediction. The OGB [\[19\]](#page-8-3) default configurations are used in both sampling and training. Node features are initialized randomly using Xavier weight initialization in all experiments.

Computing Infrastructure: All experiments are conducted on Ubuntu server virtual machine that is equipped with dual 64-core Intel Xeon 2.4 GHZ (Skylake, IBRS) CPUs, 256 GB of main memory and 1TB of disk storage.

Real KGs: We mainly focus on two benchmark KGs distinguishing in graph size, graph data domain, task type, and connection density including (DBLP [\[11\]](#page-7-10) and Yago-4

<span id="page-6-1"></span>TABLE I: Statistics of the used KGs and GNN tasks. We used four times larger KGs (DBLP and Yago) than the ones reported in OGB [\[19\]](#page-8-3).

<span id="page-6-2"></span>![](_page_6_Figure_1.jpeg)
<!-- Image Description: This image presents a technical comparison of two knowledge graph embedding methods, DBLP(KG) and KGNET(KG'), on three metrics: accuracy, training time, and memory usage. Three bar charts illustrate the performance of each method across three different models (G-SAINT, RGCN, SH-SAINT). A table summarizes the size and characteristics of the DBLP and YAGO4 knowledge graphs used in the evaluation. The image aims to demonstrate the relative efficiency and accuracy of the KGNET method compared to DBLP across different tasks and models. -->

Fig. 13: (a) Accuracy, (B) Training Time, and (C) Training Memory for DBLP KG Paper-Venue node classification task. The KGNet task-oriented sampled subgraph (KG') significantly improves accuracy, training time, and memory.

[\[39\]](#page-8-22)). We conducted two node classification tasks and one link prediction. We followed the tasks used in OGB [\[19\]](#page-8-3). Statistics about used KG and tasks are provided in Table [I.](#page-6-1)

Endpoints: We use Virtuoso 07.20.3229 as a SPARQL endpoint, as it is widely adopted as an endpoint for large KGs, such as DBLP. The standard, unmodified installation of the Virtuoso engine was run at the endpoints and used in all experiments.

####*B. GML Experiments With Real KGs*Three GML tasks are conducted to evaluate the KGNet automated GML pipeline. For Node classification task, GNN methods are used to train node classifiers to predict a venue for each DBLP paper. The KG is loaded into the Virtuoso RDF engine. KGNet performs meta-sampling using d1h1 to extract the task-specific subgraph (KG<sup>0</sup> ) to train RGCN, Graph-SAINT, and Shadow-SAINT methods. The task results in Figures [13](#page-6-2) and [14](#page-6-3) show that our KGNet training pipeline using (KG<sup>0</sup> ) outperforms the traditional pipeline on the full KG in all methods with up to 11% accuracy score. The automated training pipeline of KGNet has successfully enabled GNN methods to achieve significant reductions in memory consumption and training time. Specifically, KGNet has demonstrated a reduction of at least 22% in memory consumption and 27% in training time. These results demonstrate that KGNet can effectively discover task-specific subgraphs for each task.

Our Link prediction task aims to predict an author's affiliation link based on their publications and affiliations history

<span id="page-6-3"></span>![](_page_6_Figure_8.jpeg)
<!-- Image Description: This figure presents a comparative analysis of YAGO and KGNET knowledge graph embedding models across three metrics: accuracy (A), training time (B), and memory usage (C). Each bar chart displays the performance of both models on three datasets (G-SAINT, RGCN, SH-SAINT). The numerical values on the bars represent the specific performance in each category for each model-dataset combination. The purpose is to demonstrate the relative strengths and weaknesses of YAGO and KGNET regarding accuracy, efficiency, and resource consumption. -->

Fig. 14: (a) Accuracy, (B) Training Time, and (C) Training Memory for YAGO-4 KG Place-Country node classification task. The KGNet task-oriented sampled subgraph (KG') significantly improves accuracy, training time, and memory.

<span id="page-6-4"></span>![](_page_6_Figure_10.jpeg)
<!-- Image Description: This figure presents a comparative analysis of DBLP(KG) and KGNET(KG') methods using bar charts. (A) shows Hits@10, (B) shows training time in hours, and (C) shows memory usage in GB for the MorsE dataset. KGNET(KG') generally demonstrates superior performance in terms of Hits@10, while DBLP(KG) requires significantly more time and memory. The figure illustrates the trade-off between performance and resource consumption. -->

Fig. 15: (a) Accuracy, (B) Training Time, and (C) Training Memory for the DBLP Author Affiliation link prediction task. The KGNet task-oriented edge sampled subgraph (KG') significantly improves the Hits@10 MRR score, training time, and training memory.

on the DBLP knowledge graph. MorsE [\[22\]](#page-8-6) is the state-of-theart link-prediction sampling-based method. We use the MorsE in the traditional pipeline with the full KG. In the KGNet pipeline, our meta-sampling first extracts the task-specific subgraph (KG<sup>0</sup> ) using d2h1 to train MorsE. The results, shown in Figure [15,](#page-6-4) demonstrate that the KGNet automated pipeline outperforms the pipeline trained on the full KG in terms of Hits@10 MRR score. KGNet achieves a significant reduction in memory usage and training time, with a reduction of 94% compared to the pipeline trained on the full KG.

#### VI. RELATED WORK

<span id="page-6-0"></span>The adoption of combining AI and database systems has been growing rapidly, with two main approaches emerging: AI models incorporated in DB systems (AI4DB) and database techniques optimized for AI systems for better scalability (DB4AI) [\[40\]](#page-8-23). In KGNet, we classify SPARQLML as part of the AI4DB approach since we have extended the KG engine to query and perform inference on KGs using GML models. However, we classify GMLaaS as part of the DB4AI approach since we have optimized the training pipeline using our meta-sampling approach, which queries a KG to extract a task-specific subgraph. Works RDFFrames [\[41\]](#page-8-24), DistRDF2ML [\[42\]](#page-8-25), and Apple Saga [\[18\]](#page-8-2) aim to bridge the gap between ML and RDF systems by enabling the user to extract data from heterogeneous graph engines in a standard tabular format to apply traditional ML tasks such as classification, regression, and clustering or use KGE methods to generate node/edge embeddings for similarity search applications.

Yuo Lu et.al. addressed the problem of AI-enabled query optimization for SQL in [\[29\]](#page-8-13) and introduced the probabilistic predicates (PPs) method that can be trained without any knowledge of the inference models. In Learned B+tree [\[43\]](#page-8-26), the B+tree index is optimized based on AI models that map each query key to its page. Hasan et al [\[44\]](#page-8-27) allow fast join queries by utilizing auto-regressive densities model to represent the joint data distribution among columns. ITLCS [\[45\]](#page-8-28) introduced an index selection ML-based method that uses a classifier model as well as a genetic algorithm that selects the accurate index. Stardog [\[13\]](#page-7-12) supports supervised learning to build predictive analytics models. Stardog enables users to write SPARQL queries that collect the ML training features set in a tabular format and apply classical ML, i.e., classification, clustering, and regression that can be used for inference queries.

Google's BigQuery ML [\[46\]](#page-8-29) provides user-friendly tools to support AI models in SQL statements by introducing a hybrid language model that contains both AI and DB operations, which executes AI operations on AI platforms such as TensorFlow and Keras. SQL4ML [\[47\]](#page-8-30) translates ML operators implemented in SQL into a TensorFlow pipeline for efficient training. To enable ad-hoc GML pipelines using SPARQL, RDF engines require this level of support.

Bordawekar et al. [\[48\]](#page-8-31) built a cognitive relation database engine that queries database records utilizing word similarity using word2vec embeddings and extends results with external data sources. The cognitive DB represents a step towards linking representation learning with DB using text embedding techniques. EmbDI [\[49\]](#page-8-32) automatically learns local relation embeddings with high quality from relational datasets using a word embedding to support datasets schema matching. Unlike all the above-mentioned systems, KGNet proposed a platform combining DB4AI and AI4DB approaches to bridge the gap between GML frameworks and RDF engines.

#### VII. CONCLUSION

<span id="page-7-15"></span>The lack of integration between GML frameworks and RDF engines necessitates that data scientists manually optimize GML pipelines to retrieve KGs stored in RDF engines and select appropriate GML methods that align with their computing resources. Furthermore, the trained models cannot be directly used for querying and inference over KGs, which impedes systems' scalability, particularly as KGs grow in size and require excessive computing resources. Additionally, these limitations impact the system's flexibility, as descriptive query languages are incapable of incorporating GML models. To overcome these limitations, this vision paper proposed KGNet, an on-demand GML-as-a-service (GMLaaS) platform on top of RDF engines to support GML-enabled SPARQL queries (SPARQLML). KGNet uses meta-sampling to extract a task-specific subgraph (KG<sup>0</sup> ) as a search query against a KG for a specific task. Our GMLaaS automates a costeffective pipeline using KG<sup>0</sup> to train a model within a given time or memory budget. KGNet maintains the metadata and statistics of trained models as an RDF graph called KGMeta, which is stored alongside associated KGs. KGMeta leads to a seamless integration between GML models and RDF engines, allowing users to easily express their SPARQLML queries based on the SPARQL logic of pattern matching. Moreover, KGMeta enables KGNet to optimize SPARQLML queries for model selection and rank-ordering for the inferencing process. KGNet raises research opportunities spanning across data management and AI.

#### REFERENCES

- <span id="page-7-0"></span>[1] H. Aidan, B. Eva, and et.al., "Knowledge graphs,"*ACM Comput. Surv.*, vol. 54, no. 4, 2021. [Online]. Available: [https://doi.org/10.1145/](https://doi.org/10.1145/3447772) [3447772](https://doi.org/10.1145/3447772)
- <span id="page-7-1"></span>[2] S. Wu, F. Sun, W. Zhang, X. Xie, and B. Cui, "Graph neural networks in recommender systems: A survey," *ACM Comput. Surv.*, vol. 55, no. 5, pp. 97:1–97:37, 2023. [Online]. Available: <https://doi.org/10.1145/3535101>
- <span id="page-7-2"></span>[3] Z. Wang, Q. Lv, X. Lan, and Y. Zhang, "Cross-lingual knowledge graph alignment via graph convolutional networks," in *Proceedings of the Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 2018, pp. 349–357. [Online]. Available: <https://aclanthology.org/D18-1032>
- <span id="page-7-3"></span>[4] X. Lin, Z. Quan, Z. Wang, T. Ma, and X. Zeng, in *Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI)*, 2020, pp. 2739–2745. [Online]. Available: [https://doi.org/10.24963/ijcai.2020/](https://doi.org/10.24963/ijcai.2020/380) [380](https://doi.org/10.24963/ijcai.2020/380)
- <span id="page-7-4"></span>[5] Y. Dou, Z. Liu, L. Sun, Y. Deng, H. Peng, and P. S. Yu, "Enhancing graph neural network-based fraud detectors against camouflaged fraudsters," in *The ACM International Conference on Information and Knowledge Management (CIKM)*, 2020, pp. 315–324. [Online]. Available:<https://doi.org/10.1145/3340531.3411903>
- <span id="page-7-5"></span>[6] Y. Dou, Z. Liu, and et.al., "Enhancing graph neural network-based fraud detectors against camouflaged fraudsters." ACM, 2020. [Online]. Available:<https://doi.org/10.1145/3340531.3411903>
- <span id="page-7-6"></span>[7] PyG. (2022) Torch geometric documentation. [Online]. Available: <https://pytorch-geometric.readthedocs.io/en/latest/index.html>
- <span id="page-7-7"></span>[8] D. Zheng, C. Ma, M. Wang, and et.al., "Distdgl: Distributed graph neural network training for billion-scale graphs," in *IEEE/ACM,10th*. IEEE, 2020.
- <span id="page-7-8"></span>[9] Z. Wu, S. Pan, F. Chen, and et.al., "A comprehensive survey on graph neural networks," *IEEE Trans. Neural Networks Learn. Syst.*, vol. 32, no. 1, pp. 4–24, 2021. [Online]. Available: [https:](https://doi.org/10.1109/TNNLS.2020.2978386) [//doi.org/10.1109/TNNLS.2020.2978386](https://doi.org/10.1109/TNNLS.2020.2978386)
- <span id="page-7-9"></span>[10] Q. Wang, Z. Mao, B. Wang, and L. Guo, "Knowledge graph embedding: A survey of approaches and applications," *IEEE Transactions on Knowledge and Data Engineering*, vol. 29, no. 12, pp. 2724–2743, 2017.
- <span id="page-7-10"></span>[11] M. R. Ackermann. (2022) dblp in rdf. [Online]. Available: [https:](https://blog.dblp.org/2022/03/02/dblp-in-rdf/) [//blog.dblp.org/2022/03/02/dblp-in-rdf/](https://blog.dblp.org/2022/03/02/dblp-in-rdf/)
- <span id="page-7-11"></span>[12] D. Gordon. (2021) Fulltext search in neo4j. [Online]. Available: <https://neo4j.com/developer/kb/fulltext-search-in-neo4j/>
- <span id="page-7-12"></span>[13] docs@stardog.com. Stardog documentation-machine learning. [Online]. Available:<https://docs.stardog.com/machine-learning#machine-learning>
- <span id="page-7-13"></span>[14] Neo4j.Inc. (2022) Neo4j graph data science for machine learning. [Online]. Available: [https://neo4j.com/docs/graph-data-science/current/](https://neo4j.com/docs/graph-data-science/current/machine-learning/machine-learning/) [machine-learning/machine-learning/](https://neo4j.com/docs/graph-data-science/current/machine-learning/machine-learning/)
- <span id="page-7-14"></span>[15] H. Chen, S. F. Sultan, and et.al., "Fast and accurate network embeddings via very sparse random projection," in *Proceedings of the 28th ACM International Conference on Information and Knowledge Management*, ser. CIKM '19, 2019, p. 399–408. [Online]. Available: <https://doi.org/10.1145/3357384.3357879>

- <span id="page-8-0"></span>[16] A. Grover and J. Leskovec, "node2vec: Scalable feature learning for networks," in *Proceedings of the 22nd ACM SIGKDD*, 2016, pp. 855–864. [Online]. Available:<https://doi.org/10.1145/2939672.2939754>
- <span id="page-8-1"></span>[17] W. L. Hamilton, Z. Ying, and J. Leskovec, "Inductive representation learning on large graphs," in *NeurIPS*, 2017, pp. 1024– 1034. [Online]. Available: [https://proceedings.neurips.cc/paper/2017/](https://proceedings.neurips.cc/paper/2017/hash/5dd9db5e033da9c6fb5ba83c7a7ebea9-Abstract.html) [hash/5dd9db5e033da9c6fb5ba83c7a7ebea9-Abstract.html](https://proceedings.neurips.cc/paper/2017/hash/5dd9db5e033da9c6fb5ba83c7a7ebea9-Abstract.html)
- <span id="page-8-2"></span>[18] I. F. Ilyas, T. Rekatsinas, V. Konda, J. Pound, X. Qi, and M. A. Soliman, "Saga: A platform for continuous construction and serving of knowledge at scale," in *SIGMOD*, 2022, pp. 2259–2272. [Online]. Available:<https://doi.org/10.1145/3514221.3526049>
- <span id="page-8-3"></span>[19] W. Hu, M. Fey, M. Zitnik, Y. Dong, H. Ren, B. Liu, M. Catasta, and J. Leskovec, "Open graph benchmark: Datasets for machine learning on graphs," in *NeurIPS*, 2020.
- <span id="page-8-4"></span>[20] H. Zeng, H. Zhou, and et.al., "Graphsaint: Graph sampling based inductive learning method," in *ICLR(8)*, 2020. [Online]. Available: <https://openreview.net/forum?id=BJe8pkHFwS>
- <span id="page-8-5"></span>[21] H. Zeng, M. Zhang, Y. Xia, and et.al., "Decoupling the depth and scope of graph neural networks," *CoRR*, vol. abs/2201.07858, 2022. [Online]. Available:<https://arxiv.org/abs/2201.07858>
- <span id="page-8-6"></span>[22] M. Chen, W. Zhang, and et.al., "Meta-knowledge transfer for inductive knowledge graph embedding," in *ACM SIGIR*, 2022, p. 927–937. [Online]. Available:<https://doi.org/10.1145/3477495.3531757>
- <span id="page-8-7"></span>[23] M. S. Schlichtkrull, T. N. Kipf, and e. a. Peter Bloem, "Modeling relational data with graph convolutional networks," in *ESWC*, vol. 10843. Springer, 2018, pp. 593–607. [Online]. Available: [https://doi.org/10.1007/978-3-319-93417-4\\_38](https://doi.org/10.1007/978-3-319-93417-4_38)
- <span id="page-8-8"></span>[24] M. Chen, Y. Zhang, X. Kou, and et.al., "r-gat: Relational graph attention network for multi-relational graphs," *CoRR*, vol. abs/2109.05922, 2021. [Online]. Available:<https://arxiv.org/abs/2109.05922>
- <span id="page-8-9"></span>[25] M. Färber, "The microsoft academic knowledge graph: A linked data source with 8 billion triples of scholarly data," in *ISWC*, vol. 11779, 2019, pp. 113–129. [Online]. Available: [https://doi.org/10.1007/](https://doi.org/10.1007/978-3-030-30796-7_8) [978-3-030-30796-7\\_8](https://doi.org/10.1007/978-3-030-30796-7_8)
- <span id="page-8-10"></span>[26] T. Y. Cheng, Q. Hu, Q. Xie, N. Trigoni, and A. Markham, "Metasampler: Almost-universal yet task-oriented sampling for point clouds," *ECCV*, 2022. [Online]. Available: [https://doi.org/10.48550/arXiv.2203.](https://doi.org/10.48550/arXiv.2203.16001) [16001](https://doi.org/10.48550/arXiv.2203.16001)
- <span id="page-8-11"></span>[27] O. Dovrat, I. Lang, and S. Avidan, "Learning to sample," in *IEEE CVPR*, 2019, pp. 2760–2769. [Online]. Available: [http://openaccess.thecvf.com/content\\_CVPR\\_2019/html/Dovrat\\_](http://openaccess.thecvf.com/content_CVPR_2019/html/Dovrat_Learning_to_Sample_CVPR_2019_paper.html) [Learning\\_to\\_Sample\\_CVPR\\_2019\\_paper.html](http://openaccess.thecvf.com/content_CVPR_2019/html/Dovrat_Learning_to_Sample_CVPR_2019_paper.html)
- <span id="page-8-12"></span>[28] Y. Xiao, K. Gong, P. Zhou, G. Zheng, X. Liang, and L. Lin, "Adversarial meta sampling for multilingual low-resource speech recognition," in *AAAI*, 2021, pp. 14 112–14 120. [Online]. Available: <https://ojs.aaai.org/index.php/AAAI/article/view/17661>
- <span id="page-8-13"></span>[29] Y. Lu, A. Chowdhery, S. Kandula, and S. Chaudhuri, "Accelerating machine learning inference with probabilistic predicates," in *SIGMOD*, ser. SIGMOD '18, 2018, p. 1493–1508. [Online]. Available: [https:](https://doi.org/10.1145/3183713.3183751) [//doi.org/10.1145/3183713.3183751](https://doi.org/10.1145/3183713.3183751)
- [30] R. Bordawekar and O. Shmueli, "Enabling cognitive intelligence queries in relational databases using low-dimensional word embeddings," *CoRR*, vol. abs/1603.07185, 2016. [Online]. Available: [http://arxiv.org/](http://arxiv.org/abs/1603.07185) [abs/1603.07185](http://arxiv.org/abs/1603.07185)
- <span id="page-8-14"></span>[31] M. Schule, H. Lang, M. Springer, A. Kemper, T. Neumann, and S. Gunnemann, "In-database machine learning with sql on gpus," in *SSDBM*, 2021. [Online]. Available: [https://doi.org/10.1145/3468791.](https://doi.org/10.1145/3468791.3468840) [3468840](https://doi.org/10.1145/3468791.3468840)
- <span id="page-8-15"></span>[32] K. Awada, M. Y. Eltabakh, C. Tang, M. Al-Kateb, S. Nair, and G. Au,

"Cost estimation across heterogeneous sql-based big data infrastructures in teradata intellisphere," in *EDBT*, 2020.

- <span id="page-8-16"></span>[33] S. Chaudhuri and K. Shim, "Optimization of queries with user-defined predicates," *ACM Trans. Database Syst.*, vol. 24, no. 2, pp. 177–228, 1999. [Online]. Available:<https://doi.org/10.1145/320248.320249>
- <span id="page-8-17"></span>[34] M. Serafini, "Scalable graph neural network training: The case for sampling," *ACM SIGOPS Oper. Syst. Rev.*, vol. 55, no. 1, pp. 68–76, 2021. [Online]. Available:<https://doi.org/10.1145/3469379.3469387>
- <span id="page-8-18"></span>[35] J. Johnson, M. Douze, and H. Jégou, "Billion-scale similarity search with gpus," *IEEE Trans. Big Data*, vol. 7, no. 3, pp. 535–547, 2021. [Online]. Available:<https://doi.org/10.1109/TBDATA.2019.2921572>
- <span id="page-8-19"></span>[36] D. Chen, Y. Lin, W. Li, P. Li, J. Zhou, and X. Sun, "Measuring and relieving the over-smoothing problem for graph neural networks from the topological view," in *IAAI*, 2020, pp. 3438–3445.
- <span id="page-8-20"></span>[37] J. Liu, K. Kawaguchi, B. Hooi, Y. Wang, and X. Xiao, "Eignn: Efficient infinite-depth graph neural networks," in *NIPS*, vol. 34, 2021, pp. 18 762–18 773. [Online]. Available: [https://proceedings.neurips.cc/](https://proceedings.neurips.cc/paper/2021/file/9bd5ee6fe55aaeb673025dbcb8f939c1-Paper.pdf) [paper/2021/file/9bd5ee6fe55aaeb673025dbcb8f939c1-Paper.pdf](https://proceedings.neurips.cc/paper/2021/file/9bd5ee6fe55aaeb673025dbcb8f939c1-Paper.pdf)
- <span id="page-8-21"></span>[38] S. Bradley, A. Hax, A. Hax, and T. Magnanti, *Chapter 9: Integer Programming*. Addison-Wesley, 1977.
- <span id="page-8-22"></span>[39] T. P. Tanon, G. Weikum, and F. M. Suchanek, "YAGO 4: A reasonable knowledge base," in *ESWC*, vol. 12123, 2020, pp. 583–596. [Online]. Available: [https://doi.org/10.1007/978-3-030-49461-2\\_34](https://doi.org/10.1007/978-3-030-49461-2_34)
- <span id="page-8-23"></span>[40] X. Zhou, C. Chai, G. Li, and J. Sun, "Database meets artificial intelligence: A survey," *IEEE TKDE*, vol. 34, no. 3, pp. 1096–1116, 2022.
- <span id="page-8-24"></span>[41] A. Mohamed, G. Abuoda, and et.al., "Rdfframes: Knowledge graph access for machine learning tools," *PVLDB*, vol. 13, no. 12, 2020. [Online]. Available: [http://www.vldb.org/pvldb/vol13/p2889-mohamed.](http://www.vldb.org/pvldb/vol13/p2889-mohamed.pdf) [pdf](http://www.vldb.org/pvldb/vol13/p2889-mohamed.pdf)
- <span id="page-8-25"></span>[42] C. F. Draschner, C. Stadler, F. Bakhshandegan Moghaddam, J. Lehmann, and H. Jabeen, "Distrdf2ml-scalable distributed in-memory machine learning pipelines for rdf knowledge graphs," in *Proceedings of the 30th ACM*, 2021, p. 4465–4474. [Online]. Available: [https:](https://doi.org/10.1145/3459637.3481999) [//doi.org/10.1145/3459637.3481999](https://doi.org/10.1145/3459637.3481999)
- <span id="page-8-26"></span>[43] T. Kraska, A. Beutel, E. H. Chi, J. Dean, and N. Polyzotis, "The case for learned index structures," in *SIGMOD*. ACM, 2018, pp. 489–504. [Online]. Available:<https://doi.org/10.1145/3183713.3196909>
- <span id="page-8-27"></span>[44] S. Hasan, S. Thirumuruganathan, J. Augustine, N. Koudas, and G. Das, "Multi-attribute selectivity estimation using deep learning," *CoRR*, vol. abs/1903.09999, 2019. [Online]. Available: [http://arxiv.org/abs/1903.](http://arxiv.org/abs/1903.09999) [09999](http://arxiv.org/abs/1903.09999)
- <span id="page-8-28"></span>[45] W. G. Pedrozo, J. C. Nievola, and D. C. Ribeiro, "An adaptive approach for index tuning with learning classifier systems on hybrid storage environments," in *HAIS*, vol. 10870, 2018, pp. 716–729. [Online]. Available: [https://doi.org/10.1007/978-3-319-92639-1\\_60](https://doi.org/10.1007/978-3-319-92639-1_60)
- <span id="page-8-29"></span>[46] S. Fernandes and J. Bernardino, "What is bigquery?" *Proceedings of the 19th International Database Engineering & Applications Symposium*, 2015.
- <span id="page-8-30"></span>[47] N. Makrynioti, R. Ley-Wild, and V. Vassalos, "sql4ml A declarative end-to-end workflow for machine learning," *CoRR*, vol. abs/1907.12415, 2019. [Online]. Available:<http://arxiv.org/abs/1907.12415>
- <span id="page-8-31"></span>[48] R. Bordawekar, B. Bandyopadhyay, and O. Shmueli, "Cognitive database: A step towards endowing relational databases with artificial intelligence capabilities," vol. abs/1712.07199, 2017. [Online]. Available:<http://arxiv.org/abs/1712.07199>
- <span id="page-8-32"></span>[49] C. Riccardo, P. Paolo, and T. Saravanan, "Creating embeddings of heterogeneous relational datasets for data integration tasks," in *ACM SIGMOD*, USA, 2020, p. 1335–1349. [Online]. Available: <https://doi.org/10.1145/3318464.3389742>
