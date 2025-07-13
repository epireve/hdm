---
cite_key: abdallah_2023
title: Towards a GML-Enabled Knowledge Graph Platform
authors: Hussein Abdallah, Essam Mansour
year: 2021
doi: 10.1145/3447772
url: https://doi.org/10.1145/3447772
relevancy: Medium
relevancy_justification: Contains relevant concepts applicable to HDM systems
tags: 
date_processed: 2025-07-02
phase2_processed: true
original_folder: arxiv_2303.02166_Towards_a_GML-Enabled_Knowledge_Graph_Platform
images_total: 9
images_kept: 9
images_removed: 0
keywords: 
---

# Towards a GML-Enabled Knowledge Graph Platform

Hussein Abdallah *Concordia University,* hussein.abdallah@concordia.ca
**Abstract:** This vision paper proposes KGNet, an on-demand graph machine learning (GML) as a service on top of RDF engines to support GML-enabled SPARQL queries. KGNet automates the training of GML models on a KG by identifying a task-specific subgraph. This helps reduce the task-irrelevant KG structure and properties for better scalability and accuracy. While training a GML model on KG, KGNet collects metadata of trained models in the form of an RDF graph called KGMeta, which is interlinked with the relevant subgraphs in KG. Finally, all trained models are accessible via a SPARQL-like query. We call it a GML-enabled query and refer to it as SPARQLML. KGNet supports SPARQLML on top of existing RDF engines as an interface for querying and inferencing over KGs using GML models. The development of KGNet poses research opportunities in several areas, including meta-sampling for identifying task^specific^ subgraphs, GML pipeline automation with computational constraints, such as limited time and memory budget, and SPARQLML query optimization. KGNet supports different GML tasks, such as node classification, link prediction, and semantic entity matching. We evaluated KGNet using two real KGs of different application domains. Compared to training on the entire KG, KGNet significantly reduced training time and memory usage while maintaining comparable or improved accuracy. The KGNet source-code [[1]](#ref-1) is available for further study.

## I. INTRODUCTION

Knowledge graphs (KGs) are constructed based on semantics captured from heterogeneous datasets using various Artificial Intelligence (AI) techniques, such as representation learning and classification models [[1]](#ref-1). Graph machine learning (GML) techniques, such as graph representation learning and graph neural networks (GNNs), are powerful tools widely used to solve real-world problems by defining them as prediction tasks on KGs. For instance, node classification tasks for problems, such as recommendations [[2]](#ref-2) and entity alignment [[3]](#ref-3), can be solved using GML techniques. Similarly, drug discovery [[4]](#ref-4) and fraud detection [[5]](#ref-5), [[6]](#ref-6) problems are tackled as link prediction tasks using GML techniques.

Data scientists often work with KGs, which are typically stored in RDF engines. They are responsible for developing GML pipelines using frameworks, such as PyG [[7]](#ref-7) and DGL [[8]](#ref-8), to train models on these KGs. However, there is often a gap between the GML frameworks and RDF engines. This necessitates an initial step of transforming the entire KG from RDF triple format into adjacency matrices in a traditional GML pipeline. Afterward, the data scientist needs to select a suitable GML method from a wide range of KG embedding (KGE) or GNN methods [[9]](#ref-9), [[10]](#ref-10) to train the model. For the average user, this responsibility is time-consuming.

Essam Mansour *Concordia University,* essam.mansour@concordia.ca

![A KG with nodes/edges in red, which could be predicted by classification and link prediction models on the fly.](_page_0_Figure_9.jpeg)

**Figure 1:** A KG with nodes/edges in red, which could be predicted by classification and link prediction models on the fly.

**prefix dblp**: <https://www.**dblp**.org/> **prefix kgnet**: <https://www.**kgnet**.com/> **select**?title ?venue 4**where**{ ?paper**a dblp**:Publication. ?paper **dblp**:title ?title. ?paper **?NodeClassifier**?venue. ?NodeClassifier**a kgnet:NodeClassifier**. ?NodeClassifier **kgnet**:TargetNode **dblp**:Publication. ?NodeClassifier **kgnet**:NodeLabel **dblp**:venue.}

**Figure 2:** SPARQLML pv : a SPARQLML query uses a node classification model to predict a paper's venue by querying and inferencing over the KG shown in Figure [[1]](#ref-1).

Furthermore, the trained models are isolated from the RDF engine, where the KG is stored. Therefore, automating the training of GML models on KGs and providing accessibility to the trained models via a SPARQL-like query is essential. We refer to this query as a SPARQLML query.

The KG shown in Figure [[1]](#ref-1) contains information about published papers in DBLP [[11]](#ref-11). However, the traditional SPARQL query language cannot be used to apply GML models on top of a KG, such as predicting a node's class or a missing affiliation link for an author. For instance, the venue node in Figure [[1]](#ref-1) is a virtual node that could be predicted using a node classification (NC) model. It would be fascinating to query this KG using a GML model for NC through a SPARQL-like query to obtain the paper-venue node, as shown in the SPARQLML pv in Figure [[2]](#ref-2). This query uses a model of type *kgnet:NodeClassifier*to predict a venue for each paper. The SPARQLML triple patterns in lines 8-10 will retrieve all models of type*kgnet:NodeClassifier*that predict a class of type*dblp:venue*. In the triple pattern h?paper, ?NodeClassifier, ?venuei, we refer to *?NodeClassifier* as a user-defined predicate.

Enabling queries like SPARQLML pv , shown in Figure [[2]](#ref-2), presents several challenges. These include: (*i*) automatically training GML models for various tasks, (*ii*) optimizing SPARQLML for GML model selection based on accuracy and inference time, and (*iii*) efficiently interacting with the selected model during query execution. Additionally, seamless integration of GML models into RDF engines is necessary. As a result, users should be able to express their SPARQLML queries easily by following the SPARQL logic of pattern matching, avoiding the explicit use of user-defined functions (UDFs).

There is a growing adoption of integrating GML with existing graph databases, such as Neo4j [[12]](#ref-12) or Stardog [[13]](#ref-13). However, while these databases offer some machine learning primitive methods, such as PageRank and shortest-path using the *Cypher*language, they do not address the challenges of integrating GML models with RDF engines. For example, Neo4j Graph Data Science [[14]](#ref-14) supports limited graph embedding methods in a beta version, such as FastRP [[15]](#ref-15), Node2Vec [[16]](#ref-16), and Graph-SAGE [[17]](#ref-17). However, a user must train the models separately as an initial step. To address these challenges, there is a need to bring GML to data stored in RDF engines instead of getting data to machine learning pipelines. This would encourage the development of KG data science libraries powered by the expressiveness of SPARQL, enabling better analysis and insight discovery based on KG structure and semantics. These libraries would empower data scientists with a full breadth of KG machine learning services on top of KGs stored in RDF engines.

This vision paper proposes KGNet, an on-demand GMLas-a-service on top of RDF engines to support SPARQLML queries, as illustrated in Figure [[3]](#ref-3). KGNet extends existing RDF engines with two main components GML-as-aservice (GMLaaS) and SPARQLML as a Service. KGNet automatically trains a GML model on a KG for tasks, such as node classification or like prediction, and maintains metadata of the trained model as an RDF graph called*KGMeta*. To reduce training time and memory usage while improving accuracy on a specific task A, KGNet performs meta-sampling to identify a task-specific subgraph KG^0^ of the larger KG that preserves essential characteristics relevant to A. This enables KGNet to scale on large KGs. GMLaaS is in charge of: (*i*) selecting the near-optimal GML method for training A using KG^0^ based on a given time or memory budget, and (*ii*) communicating with RDF engines via HTTP calls requesting inferencing of a specific trained model, (*iii*) storing the trained models and embeddings related to KGs. The SPARQLML service transparently: (*i*) maintains and interlinks the KGMeta with associated KGs, (*ii*) optimizes the GML model selection for a user-defined predicate, and (*iii*) finally rewrites the SPARQLML query as a SPARQL query.

In summary, the contributions of this paper are:

- a fully-fledged GML-enabled KG platform^2^ <https://github.com/CoDS-GCS/KGNET> on top of existing RDF engines.
- GML-as-a-service to provide automatic training of GML models based on a given memory or time budget.

![The KGNet architecture, which provides an interface language (SPARQLML) and enables AI applications and data scientists to automatically train GML models on top of KGs for querying and inferencing KGs based on the trained models.](_page_1_Figure_7.jpeg)

**Figure 3:** The KGNet architecture, which provides an interface language (SPARQLML) and enables AI applications and data scientists to automatically train GML models on top of KGs for querying and inferencing KGs based on the trained models.

This automatic training utilizes task-specific subgraphs extracted using our meta-sampling approach.

- SPARQLML as a Service to perform meta-sampling, maintain training meta-data in KGMeta, and optimize the GML model selection, i.e., opt for the near-optimal model based on constraints on accuracy and inference time.
- A comprehensive evaluation with different GML methods using three GML tasks on real KGs. Our experiments show that KGNet achieved comparable or improved accuracy compared to training on the entire KG, while significantly reducing training time and memory usage.

The remainder of this paper is organized as follows. Section [[II]](#ref-II) provides a background about existing graph machine learning pipelines. Section [[III]](#ref-III) outlines the main research challenges of developing a GML-enabled KG engine. Section [[IV]](#ref-IV) presents the KGNet platform. Section [[V]](#ref-V) discusses the results of evaluating our automated pipeline for training GML models. Sections [[VI]](#ref-VI) and [[VII]](#ref-VII) are related work and conclusion.

### II. BACKGROUND: ML PIPELINES FOR KGS

ML pipelines developed to train models on a KG can be grouped into three main categories: (*i*) traditional ML on KG data in tabular format, (*ii*) traditional ML on KG embeddings, and (*iii*) graph neural networks (GNNs) trained directly on the KG. In the traditional ML approach using KG data in tabular format, data from the KG is transformed into inmemory data frames, and classical ML classifiers are trained using feature engineering techniques and libraries, such as Scikit-Learn or SparkMLib. In contrast, traditional ML on KG embeddings avoids the feature engineering process and generates embeddings for nodes and edges. Apple Saga [[18]](#ref-18) is an example of this approach, which uses graph ML libraries like DGL-KE [[8]](#ref-8) to generate KG embeddings. Data scientists have the flexibility to choose the ML method for training.

GNNs have gained significant popularity in recent years. Hence, data scientists frequently utilize them to perform GML tasks. The Open Graph Benchmark (OGB) [[19]](#ref-19) standardized the GNN training pipeline, emphasizing the best practices for tackling GML tasks and building a GNN training pipeline. Figure [[4]](#ref-4) summarizes this pipeline, which involves encoding

![A traditional GML pipeline [[19]](#ref-19) using a GML framework. The pipeline starts with extracting the graph data, followed by data transformation into sparse matrices to train models for a GML task. Finally, the inference step is ready to predict results in isolation from the graph databases.](_page_2_Figure_0.jpeg)

**Figure 4:** A traditional GML pipeline [[19]](#ref-19) using a GML framework. The pipeline starts with extracting the graph data, followed by data transformation into sparse matrices to train models for a GML task. Finally, the inference step is ready to predict results in isolation from the graph databases.

KG nodes and edges, generating adjacency matrices, loading them into memory, and training GNNs using specific methods. Various GML frameworks, such as DGL [[8]](#ref-8) and PyG [[7]](#ref-7), offer multiple implementations of GNN methods. These frameworks support data transformation by loading graphs into memory as graph data structures and applying transformations. However, existing GML frameworks require significant memory and processing time for large KGs and a deep understanding of various GNN methods. In comparison, the OGB pipeline is simple, but it is a semi-automated process that necessitates human intervention and ML expertise to construct an effective pipeline and select an appropriate GNN method. Data scientists may choose the most appropriate GNN method based on various constraints, such as time or memory limitations. Furthermore, as depicted in Figure [[4]](#ref-4), the separation of the trained models from the KG engines adds an extra layer of complexity for data scientists to apply their models when inferring the KG.

### III. CHALLENGES OF GML-ENABLED KG ENGINE

This section highlights the open research challenges and opportunities raised by developing GML-enabled KG Engine.

## *A. Automatic Training: Method Selection and Meta-sampling*
There are numerous methods for training models for GML tasks, as summarized in Figure [[5]](#ref-5). These methods could be classified mainly into two categories KG embeddings (KGE) or graph neural network (GNN) methods. Examples of KGE methods are TransE, RotatE, ComplEx, and DistMult [[10]](#ref-10). Some GNN methods support sampling on full graph, such as Graph-SAINT [[20]](#ref-20), Shadow-SAINT [[21]](#ref-21), and MorsE [[22]](#ref-22). Examples of GNN full-batch training (without sampling) methods are RGCN [[23]](#ref-23) and GAT [[24]](#ref-24). Our taxonomy has more categories, as shown in Figure [[5]](#ref-5).

GML methods vary significantly in terms of their accuracy, training time, and memory requirements. Furthermore, the complexity of each GML task may differ depending on various factors, such as the size of KGs and the number of node/edge types related to the task. For example, link prediction can be more resource-intensive than node classification. Different

![A taxonomy of methods for training GML models.](_page_2_Figure_8.jpeg)

**Figure 5:** A taxonomy of methods for training GML models.

GML methods may perform differently under the same budget constraints, and selecting the best method can depend on several factors. Hence, automating a training pipeline for a specific GML task based on a user's budget for time and memory is challenging. For instance, some GML methods perform fullbatch training, which requires more memory budget. These methods require huge memory to train models on large KGs. Some other GNN methods may suffer from over-smoothing, which can cause accuracy degradation. Sampling-based GNN (mini-batch training) methods use different types of sampling, which vary in avoiding these limitations. Therefore, automating the selection of GML methods for a specific task based on a given time or memory budget is challenging.

Real KGs can contain millions to billions of triples, such as DBLP [[11]](#ref-11) and MAG [[25]](#ref-25). However, training GML models on these large KGs requires colossal computing resources that exceed the capabilities of a single machine. As a result, there is a need for identifying a smaller training dataset of the KG, which is specific to the task at hand. This process is known as meta-sampling. It has been proposed in various application domains, including computer vision [[26]](#ref-26), [[27]](#ref-27) and speech recognition [[28]](#ref-28), to extract a training dataset that is tailored to the given task. In the context of GML, meta-sampling presents an opportunity to optimize training models on large KGs by selecting a representative sub-graph that is relevant to the task. This approach can help reduce time and memory requirements without sacrificing accuracy. Therefore, exploring the potential benefits of using meta-sampling in training GML models to extract task-specific subgraphs is crucial. By doing so, we can improve the efficiency and effectiveness of GML methods on large-scale KGs. This raises a research opportunity to explore different meta-sampling approaches for GML methods on large knowledge graphs (KGs).

### *B. Seamless Integration Between GML Models and KGs*
Enabling GML on top of RDF engines poses significant challenges, mainly interfacing between the trained models and the underlying data management engine. One common approach is to use user-defined functions (UDFs) to implement this interface [[29]](#ref-29)–[[31]](#ref-31). However, this comes with a cost for query optimizations in data systems [[32]](#ref-32). The existence of an extensive catalog of UDFs can limit the expressiveness of MLbased queries. For instance, a large catalog of UDFs makes it difficult for users to choose between UDFs and find the

![This flowchart illustrates a system for automated graph machine learning (GML). It shows the stages: input (GML task, subgraph, budget, specifications); dataset transformation (preprocessing, adjacency matrix generation, train-test split); optimal GML method selection (considering GNN methods, budget, resources); GML model training (using libraries like DGL and PyG); and GML inference via a REST API, outputting results in JSON format. A key component is the GML optimizer which selects the best GNN (GCN, RGCN, etc.) based on resource constraints.](_page_3_Figure_0.jpeg)

**Figure 6:** The automation of training pipeline and inference in our GML-as-a-service (GMLaaS). GMLaaS interacts with the KGMeta Manager to train a model for a specific task with limited budget. The automated pipeline opt to the near-optimal GML method for training a model within a limited budget. GMLaaS supports task inference through RestAPI that is called by a UDF.

right one for their needs. Most existing query optimizers do not have models estimating the cost of these UDFs. Hence, automating the query optimization of SPARQLML queries is challenging. There is a research opportunity for seamless integration between trained GML models and RDF. To address these challenges, we proposed KGMeta as a graph representation of metadata of trained models interlinked with the KGs.

## *C. Optimizing SPARQL*ML *Queries and Benchmarks*
User-defined predicates were first proposed for SQL [[33]](#ref-33). In SPARQLML, a user-defined predicate is used to get a prediction from one of the trained models associated with a specific node in the graph. Estimating the cost of evaluating a user-defined predicate is more complex than estimating the cost of a traditional RDF predicate. While cardinality estimation is used to optimize only the execution time for the latter, a user-defined predicate in a SPARQLML query can be inferred by multiple models, each with varying accuracy and inference time. RDF engines are unaware of this information, leading to the problem of selecting the best model for inference.

For a SPARQLML query, the inference step in an RDF engine using a chosen model is a challenging task that requires optimization, specifically for rank-ordering the inference process. The challenge lies in deciding whether to perform the inference in a single call to a UDF or per instance, which may result in an extensive number of UDF calls. Additionally, each model has a unique cardinality, i.e., the total number of predictions it can make. This makes predicting rank-ordering complex as RDF engines lack accurate estimation of UDF costs.

To address these challenges, there are research opportunities for developing benchmarks to evaluate optimization approaches for SPARQLML queries. These benchmarks should consider various models for different user-defined predicates and be designed to work with large datasets. Furthermore, each SPARQLML query should vary in the number of user-defined predicates and be associated with variables of different cardinalities. This will enable a comprehensive evaluation of the performance and scalability of varying optimization approaches for SPARQLML queries.

## IV. THE KGNET PLATFORM

KGNet provides two main services, namely GML as a Service (GMLaaS) and SPARQLML as a Service on top of existing RDF engines, as shown in Figure [[3]](#ref-3).

### *A. GML as a Service (GMLaaS)*
Random Comunity KGNet is a platform that offers end-to-end automation of GML training on KGs, as depicted in Figure [[6]](#ref-6). The platform provides*GMLaaS*, a Restful service that manages GML models in terms of automatic training and interactive inferencing. Additionally, it utilizes an embedding store to facilitate entity similarity search tasks by computing the similarity between embedding vectors. The *GML training manager*automates the training pipeline per task. However, the automation of GML training on KGs is challenging due to the complexity and size of KGs. Therefore, KGNet leverages our meta-sampling approach to optimize the training process by selecting a taskspecific subgraph (KG^0^ ) that is specific to the given task. This step helps reduce the time and memory required without trading accuracy. The pipeline takes as input a task-specific subgraph (KG^0^ ), the GML task, the task budget, and the available resources within the ML environment.

The*Data Transformer*step converts the subgraph into a sparse-matrix format optimized for in-memory and matrix operations. This format is compatible with popular graph ML data loaders, such as Py-Geometric and DGL, and is ideal for sparse KGs. Our pipeline ensures data consistency by validating node/edge types counts, removing literal data and target class edges, and generating graph statistics. We also perform a train-validation-test split using different strategies like random and community-based. KGNet automates this transformation, making ad-hoc GML training queries possible.

The*Optimal GML Method Selection*step selects the best GML method for a given task. KGNet supports various GNN methods, including GCN, RGCN, Graph-SAINT, Shadow-SAINT, Morse, and KGE methods such as ComplEx. We estimate the required memory for each method based on the size and the number of generated sparse-matrices, as well as the training time based on the matrix dimensions and feature aggregation approach. Moreover, we estimate the training time

![This image presents two diagrams (A and B) illustrating the architecture of link prediction and node classification tasks. Each diagram uses a graph structure showing the relationships between tasks (e.g., Link Predictor Task, Node Classifier Task), data sources (dblp:Person, dblp:Publication), models (GML Model), and evaluation metrics (MRR Score, F1 Score). The diagrams highlight the flow of information and dependencies between different components within each task. Dashed lines represent relationships, and solid lines show direct dependencies.](_page_4_Figure_0.jpeg)

**Figure 7:** A KGMeta graph of two trained models for node classification and link prediction tasks. The white nodes are nodes from the original data KG. The dashed nodes/edges are metadata collected per trained model.

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
```

**Figure 8:** A SPARQLML insert query that trains a paper-venue classifier on DBLP. The TrainGML function is a UDF that is implemented inside the RDF engine.

based on the dimension of the sparse-matrices and GNN neighbour nodes features aggregation approach adopted by each method. For GNN sampling-based methods, the sampling cost basically depends on the sampling heuristic used [[34]](#ref-34). Thus, we are working on a more advanced estimation method based on sampling the sparse-matrices and running a few epochs on them.

KGNet's GML-optimizer determines the necessary resources for each method and optimizes the training settings, ensuring scalability in distributed environments. The automated pipeline trains a model and collects evaluation metrics and inference time statistics. A URI is generated for the trained model to distinguish it from other models used for inference tasks. The model meta-data is returned to the KGMeta Manager to update the KGMeta graph. Figure [[7]](#ref-7).a and b show the generated meta-data for link prediction and node classification models, respectively. The *Embedding Store*sub-component, shown in Figure [[3]](#ref-3), is used for fast similarity search by storing, indexing, and searching embeddings. The*GML Inferencing*receives HTTP calls for inference, serializes the result into a JSON Restful-API response, and sends it back to the RDF engine, as shown in Figure [[3]](#ref-3). The current version uses FAISS embedding store [[35]](#ref-35) to enable ad-hoc queries for node similarity search.

- 1**prefix dblp**:<https://www.**dblp**.org/>
- 2 **prefix kgnet**:<https://www.**kgnet**.com/>

```text
3 delete {?NodeClassifier ?p ?o}
```

4 **where**{

```text
5 ?NodeClassifier a kgnet:NodeClassifier.
```

- 6 ?NodeClassifier**kgnet**:TargetNode **dblp**:Publication.
- 7 ?NodeClassifier **kgnet**:NodeLabel **dblp**:venue.}

**Figure 9:** A SPARQLML delete query that deletes a trained model and its meta-data.

```text
1 prefix dblp: <https://www.dblp.com/>
```

2 **prefix kgnet**: <https://www.**kgnet**.com/>

- 3 **select**?author ?affiliation
- 4**where**{ ?author**a dblp**:person.
- 5 ?author ?**LinkPredictor** ?affiliation.
- 6 ?**LinkPredictor a kgnet:LinkPredictor**.
- 7 ?**LinkPredictor kgnet**:SourceNode **dblp**:person.
- 8 ?**LinkPredictor kgnet**:DestinationNode **dblp**:affiliation.
- 9 ?**LinkPredictor kgnet**:TopK-Links 10.}

**Figure 10:** A SPARQLML query predicting author affiliation link (edge) on DBLP KG.

## *B. The SPARQL*ML *as a Service*

We offer a SPARQLML as a Service, which comprises three main components: Query Manager, KGMeta Governor, and Meta-sampler. In addition, we provide an interfacing language called SPARQLML that enables users to express SPARQLlike queries for INSERT, DELETE, or SELECT operations, such that: (*i*) a SPARQLML *INSERT* query is used to train a GML model and maintain its metadata in KGMeta (as shown in Figure [[8]](#ref-8)), (*ii*) a SPARQLML *DELETE* query is used to delete trained model files and associated embeddings from the GML-aaS component and then deletes its metadata from the KGMeta (as in Figure [[9]](#ref-9)), (*iii*) a SPARQLML *SELECT*query is for querying and inferencing the KG, e.g., the query in Figure [[10]](#ref-10). When a SPARQLML query is received, the Query Manager parses it. An INSERT or DELETE query is sent to the KGMeta Governor. If it is a SELECT query, it is optimized and rewritten as a SPARQL query.
*1) KGMeta Governor:*The KGMeta Governor maintains a KGMeta graph for each KG, using statistics and metadata collected from trained GML models specific to that KG. The INSERT query is a request to train a task on a certain KG. The parsed information includes the task type (such as node classification or link prediction), the task inputs (such as the target nodes and classification labels (Y classes) for a classification task), and a budget (such as memory and time budget). Experienced ML users can provide additional information, such as hyperparameters or a specific GML method. This information is encapsulated as a JSON object, as shown in Figure [[8]](#ref-8). At line 4, the*TrainGML*is a UDF that takes as input a JSON object that encapsulates all required information to train a GML model. The KGMeta Governor sends the task to the meta-sampler to obtain a task-specific subgraph (KG^0^ ) for the given task. Then governor interacts with the GML Training Manager to automate the training

```text
1 prefix dblp: <https://www.dblp.org/>
2 prefix kgnet: <https://www.kgnet.com/>
3 select ?title
4 sql:UDFS.getNodeClass($m,?paper) as ?venue
5 where {
6 ?paper a dblp:Publication.
7 ?paper dblp:title ?title.
8 }
```

**Figure 11:** A candidate SPARQL for SPARQLML pv

pipeline for this task. Once training is complete, the KGMeta Governor receives the trained model's metadata, including accuracy and inference time, to maintain the KGMeta, as illustrated in Figure [[7]](#ref-7).
*2) Meta-sampler:* Our meta-sampler aims to identify a task-specific subgraph (KG^0^ ) for training a GML task. Each GML task targets nodes of a specific type, such as dblp:Publication in SPARQLML pv . Our meta-sampler extracts a task-specific subgraph (KG^0^ ), which comprises a set of triples with representative triples associated with the target nodes. Based on the KG schema structure the size of KG^0^ is much smaller than the size of KG. This smaller size will optimize training time and require less memory for training the GML task A. However, the KG may contain triples that are not reachable from a target node v ^T^ or connected via more than three hops from v ^T^ . These triples do not assist the model in generalizing and may lead to over-smoothing problems [[36]](#ref-36), [[37]](#ref-37).

Our SPARQL-based meta-sampling method determines the scope of the extracted subgraph based on two parameters: (*i*) the direction d, where d = 1 for outgoing and d = 2 for bidirectional (i.e., both outgoing and incoming), and (*ii*) the number of hops h. We evaluated the performance of our method using four combinations of d ∈ {1, 2} and h ∈ {1, 2}. Our metasampling approach achieved better results with d = 1 and h = 1 for node classification, whereas for link prediction, our metasampling method performed better with d = 2 and h = 1.

*3) The Query Manager:*The Query Manager is responsible for optimizing SPARQLML queries for model selection and rank-ordering to evaluate user-defined predicates. In the case of SPARQLML pv shown in Figure [[2]](#ref-2), the query optimizer fetches all URIs of the models satisfying the conditions associated with the user-defined predicate*?NodeClassifier*. The KGMeta is an RDF graph containing optimizer statistics, such as model accuracy, inference time, and model cardinality. Therefore, we use a SPARQL query to obtain the models' URIs, accuracy, inference time, and cardinality. The query optimizer selects the near-optimal GML model that achieves high accuracy and low inference time. We define this problem as an integer programming optimization problem to minimize total execution time or maximize inference accuracy.

The *SPARQL*ML *Query Re-writer*uses the near-optimal GML model with URI m to generate a candidate SPARQL query. KGNet currently supports two possible execution plans, whose query templates are shown in Figures [[11]](#ref-11) and [[12]](#ref-12). The core idea is to map a user-defined predicate into a user-defined function (UDF), such as*sql:UDFS.getNodeClass*, to send HTTP calls during the execution time to the GML Inference

```text
1 prefix dblp: <https://www.dblp.com/>
2 prefix kgnet: <https://www.kgnet.com/>
3 select ?title
4 sql:UDFS.getKeyValue(?venues_dic,?paper) as ?venue
5 where {
6 ?paper a dblp:Publication.
7 ?paper dblp:title ?title.
8 {select sql:UDFS.getNodeClass($m,dblp:Publication)
9 as ?venues_dic where { } }}
```

**Figure 12:** A candidate SPARQL for SPARQLML pv

Manager in our GMLaaS to get inference based on the pretrained model m. The number of HTTP calls may dominates the query execution cost. For example, SPARQLML pv predicts the venue of all papers, whose size is |?papers|.

The query template shown in Figure [[11]](#ref-11) will generate |?papers| HTTP calls. However, the query template shown in Figure [[12]](#ref-12) reduces the number of HTTP calls to one by enforcing an inner select query constructing a dictionary of all papers and their predicted venues. Then, *sql:UDFS.getKeyValue*is used to look up the venue of each paper. Our query optimizer decomposes the triple patterns related quering the KG triples in the SPARQLML query into sets per variable associated with a user-defined predicate. For example, in the SPARQLML pv query shown in Figure [[2]](#ref-2), our optimizer identifies two triple patterns that match the variable*?paper*and one triple pattern that matches the variable*?venue*. We use a SPARQL query to get the cardinality of each set, which is the number of distinct values of the variable in the dataset. We formulate this problem as another integer programming optimization problem [[38]](#ref-38) that minimizes the total number of HTTP calls or minimizes the constructed dictionary size, which is based on the model cardinality. For instance, in the query shown in Figure [[12]](#ref-12), our optimizer generates a dictionary of all papers and their predicted venues, which is then used to retrieve the venue of each paper using the UDF *sql:UDFS.getKeyValue*.

## V. EXPERIMENTAL EVALUATION

This section analyzes the ability of KGNet in automating pipelines to train a model for a specific task with less time and memory w.r.t traditional pipelines on full graphs.

### *A. Evaluation Setup*
Compared Methods: We used RGCN [[23]](#ref-23) as a full-batch training method and GraphSAINT [[20]](#ref-20), ShadowSAINT [[21]](#ref-21) as mini-batch sampling-based methods for node classification and MorsE [[22]](#ref-22) as edge sampling-based method for link prediction. The OGB [[19]](#ref-19) default configurations are used in both sampling and training. Node features are initialized randomly using Xavier weight initialization in all experiments.

Computing Infrastructure: All experiments are conducted on Ubuntu server virtual machine that is equipped with dual 64-core Intel Xeon 2.4 GHZ (Skylake, IBRS) CPUs, 256 GB of main memory and 1TB of disk storage.

Real KGs: We mainly focus on two benchmark KGs distinguishing in graph size, graph data domain, task type, and connection density including (DBLP [[11]](#ref-11) and Yago-4

TABLE I: Statistics of the used KGs and GNN tasks. We used four times larger KGs (DBLP and Yago) than the ones reported in OGB [[19]](#ref-19).

![This image presents a technical comparison of two knowledge graph embedding methods, DBLP(KG) and KGNET(KG'), on three metrics: accuracy, training time, and memory usage. Three bar charts illustrate the performance of each method across three different models (G-SAINT, RGCN, SH-SAINT). A table summarizes the size and characteristics of the DBLP and YAGO4 knowledge graphs used in the evaluation. The image aims to demonstrate the relative efficiency and accuracy of the KGNET method compared to DBLP across different tasks and models.](_page_6_Figure_1.jpeg)

**Figure 13:** (a) Accuracy, (B) Training Time, and (C) Training Memory for DBLP KG Paper-Venue node classification task. The KGNet task-oriented sampled subgraph (KG') significantly improves accuracy, training time, and memory.

[[39]](#ref-39)). We conducted two node classification tasks and one link prediction. We followed the tasks used in OGB [[19]](#ref-19). Statistics about used KG and tasks are provided in Table [[I]](#ref-I).

Endpoints: We use Virtuoso 07.20.3229 as a SPARQL endpoint, as it is widely adopted as an endpoint for large KGs, such as DBLP. The standard, unmodified installation of the Virtuoso engine was run at the endpoints and used in all experiments.

### *B. GML Experiments With Real KGs*
Three GML tasks are conducted to evaluate the KGNet automated GML pipeline. For Node classification task, GNN methods are used to train node classifiers to predict a venue for each DBLP paper. The KG is loaded into the Virtuoso RDF engine. KGNet performs meta-sampling using d1h1 to extract the task-specific subgraph (KG^0^ ) to train RGCN, Graph-SAINT, and Shadow-SAINT methods. The task results in Figures [[13]](#ref-13) and [[14]](#ref-14) show that our KGNet training pipeline using (KG^0^ ) outperforms the traditional pipeline on the full KG in all methods with up to 11% accuracy score. The automated training pipeline of KGNet has successfully enabled GNN methods to achieve significant reductions in memory consumption and training time. Specifically, KGNet has demonstrated a reduction of at least 22% in memory consumption and 27% in training time. These results demonstrate that KGNet can effectively discover task-specific subgraphs for each task.

Our Link prediction task aims to predict an author's affiliation link based on their publications and affiliations history

![This figure presents a comparative analysis of YAGO and KGNET knowledge graph embedding models across three metrics: accuracy (A), training time (B), and memory usage (C). Each bar chart displays the performance of both models on three datasets (G-SAINT, RGCN, SH-SAINT). The numerical values on the bars represent the specific performance in each category for each model-dataset combination. The purpose is to demonstrate the relative strengths and weaknesses of YAGO and KGNET regarding accuracy, efficiency, and resource consumption.](_page_6_Figure_8.jpeg)

**Figure 14:** (a) Accuracy, (B) Training Time, and (C) Training Memory for YAGO-4 KG Place-Country node classification task. The KGNet task-oriented sampled subgraph (KG') significantly improves accuracy, training time, and memory.

![This figure presents a comparative analysis of DBLP(KG) and KGNET(KG') methods using bar charts. (A) shows Hits@10, (B) shows training time in hours, and (C) shows memory usage in GB for the MorsE dataset. KGNET(KG') generally demonstrates superior performance in terms of Hits@10, while DBLP(KG) requires significantly more time and memory. The figure illustrates the trade-off between performance and resource consumption.](_page_6_Figure_10.jpeg)

**Figure 15:** (a) Accuracy, (B) Training Time, and (C) Training Memory for the DBLP Author Affiliation link prediction task. The KGNet task-oriented edge sampled subgraph (KG') significantly improves the Hits@10 MRR score, training time, and training memory.

on the DBLP knowledge graph. MorsE [[22]](#ref-22) is the state-of-theart link-prediction sampling-based method. We use the MorsE in the traditional pipeline with the full KG. In the KGNet pipeline, our meta-sampling first extracts the task-specific subgraph (KG^0^ ) using d2h1 to train MorsE. The results, shown in Figure [[15]](#ref-15), demonstrate that the KGNet automated pipeline outperforms the pipeline trained on the full KG in terms of Hits@10 MRR score. KGNet achieves a significant reduction in memory usage and training time, with a reduction of 94% compared to the pipeline trained on the full KG.

### VI. RELATED WORK

The adoption of combining AI and database systems has been growing rapidly, with two main approaches emerging: AI models incorporated in DB systems (AI4DB) and database techniques optimized for AI systems for better scalability (DB4AI) [[40]](#ref-40). In KGNet, we classify SPARQLML as part of the AI4DB approach since we have extended the KG engine to query and perform inference on KGs using GML models. However, we classify GMLaaS as part of the DB4AI approach since we have optimized the training pipeline using our meta-sampling approach, which queries a KG to extract a task-specific subgraph. Works RDFFrames [[41]](#ref-41), DistRDF2ML [[42]](#ref-42), and Apple Saga [[18]](#ref-18) aim to bridge the gap between ML and RDF systems by enabling the user to extract data from heterogeneous graph engines in a standard tabular format to apply traditional ML tasks such as classification, regression, and clustering or use KGE methods to generate node/edge embeddings for similarity search applications.

Yuo Lu et.al. addressed the problem of AI-enabled query optimization for SQL in [[29]](#ref-29) and introduced the probabilistic predicates (PPs) method that can be trained without any knowledge of the inference models. In Learned B+tree [[43]](#ref-43), the B+tree index is optimized based on AI models that map each query key to its page. Hasan et al [[44]](#ref-44) allow fast join queries by utilizing auto-regressive densities model to represent the joint data distribution among columns. ITLCS [[45]](#ref-45) introduced an index selection ML-based method that uses a classifier model as well as a genetic algorithm that selects the accurate index. Stardog [[13]](#ref-13) supports supervised learning to build predictive analytics models. Stardog enables users to write SPARQL queries that collect the ML training features set in a tabular format and apply classical ML, i.e., classification, clustering, and regression that can be used for inference queries.

Google's BigQuery ML [[46]](#ref-46) provides user-friendly tools to support AI models in SQL statements by introducing a hybrid language model that contains both AI and DB operations, which executes AI operations on AI platforms such as TensorFlow and Keras. SQL4ML [[47]](#ref-47) translates ML operators implemented in SQL into a TensorFlow pipeline for efficient training. To enable ad-hoc GML pipelines using SPARQL, RDF engines require this level of support.

Bordawekar et al. [[48]](#ref-48) built a cognitive relation database engine that queries database records utilizing word similarity using word2vec embeddings and extends results with external data sources. The cognitive DB represents a step towards linking representation learning with DB using text embedding techniques. EmbDI [[49]](#ref-49) automatically learns local relation embeddings with high quality from relational datasets using a word embedding to support datasets schema matching. Unlike all the above-mentioned systems, KGNet proposed a platform combining DB4AI and AI4DB approaches to bridge the gap between GML frameworks and RDF engines.

### VII. CONCLUSION

The lack of integration between GML frameworks and RDF engines necessitates that data scientists manually optimize GML pipelines to retrieve KGs stored in RDF engines and select appropriate GML methods that align with their computing resources. Furthermore, the trained models cannot be directly used for querying and inference over KGs, which impedes systems' scalability, particularly as KGs grow in size and require excessive computing resources. Additionally, these limitations impact the system's flexibility, as descriptive query languages are incapable of incorporating GML models. To overcome these limitations, this vision paper proposed KGNet, an on-demand GML-as-a-service (GMLaaS) platform on top of RDF engines to support GML-enabled SPARQL queries (SPARQLML). KGNet uses meta-sampling to extract a task-specific subgraph (KG^0^ ) as a search query against a KG for a specific task. Our GMLaaS automates a costeffective pipeline using KG^0^ to train a model within a given time or memory budget. KGNet maintains the metadata and statistics of trained models as an RDF graph called KGMeta, which is stored alongside associated KGs. KGMeta leads to a seamless integration between GML models and RDF engines, allowing users to easily express their SPARQLML queries based on the SPARQL logic of pattern matching. Moreover, KGMeta enables KGNet to optimize SPARQLML queries for model selection and rank-ordering for the inferencing process. KGNet raises research opportunities spanning across data management and AI.

### REFERENCES

- <a id="ref-1"></a>[1] H. Aidan, B. Eva, and et.al., "Knowledge graphs,"*ACM Comput. Surv.*, vol. 54, no. 4, 2021. [Online]. Available: [https://doi.org/10.1145/3447772](https://doi.org/10.1145/3447772)
- <a id="ref-2"></a>[2] S. Wu, F. Sun, W. Zhang, X. Xie, and B. Cui, "Graph neural networks in recommender systems: A survey," *ACM Comput. Surv.*, vol. 55, no. 5, pp. 97:1–97:37, 2023. [Online]. Available: <https://doi.org/10.1145/3535101>
- <a id="ref-3"></a>[3] Z. Wang, Q. Lv, X. Lan, and Y. Zhang, "Cross-lingual knowledge graph alignment via graph convolutional networks," in *Proceedings of the Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 2018, pp. 349–357. [Online]. Available: <https://aclanthology.org/D18-1032>
- <a id="ref-4"></a>[4] X. Lin, Z. Quan, Z. Wang, T. Ma, and X. Zeng, in *Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI)*, 2020, pp. 2739–2745. [Online]. Available: [https://doi.org/10.24963/ijcai.2020/380](https://doi.org/10.24963/ijcai.2020/380)
- <a id="ref-5"></a>[5] Y. Dou, Z. Liu, L. Sun, Y. Deng, H. Peng, and P. S. Yu, "Enhancing graph neural network-based fraud detectors against camouflaged fraudsters," in *The ACM International Conference on Information and Knowledge Management (CIKM)*, 2020, pp. 315–324. [Online]. Available:<https://doi.org/10.1145/3340531.3411903>
- <a id="ref-6"></a>[6] Y. Dou, Z. Liu, and et.al., "Enhancing graph neural network-based fraud detectors against camouflaged fraudsters." ACM, 2020. [Online]. Available:<https://doi.org/10.1145/3340531.3411903>
- <a id="ref-7"></a>[7] PyG. (2022) Torch geometric documentation. [Online]. Available: <https://pytorch-geometric.readthedocs.io/en/latest/index.html>
- <a id="ref-8"></a>[8] D. Zheng, C. Ma, M. Wang, and et.al., "Distdgl: Distributed graph neural network training for billion-scale graphs," in *IEEE/ACM,10th*. IEEE, 2020.
- <a id="ref-9"></a>[9] Z. Wu, S. Pan, F. Chen, and et.al., "A comprehensive survey on graph neural networks," *IEEE Trans. Neural Networks Learn. Syst.*, vol. 32, no. 1, pp. 4–24, 2021. [Online]. Available: [https://doi.org/10.1109/TNNLS.2020.2978386](https://doi.org/10.1109/TNNLS.2020.2978386)
- <a id="ref-10"></a>[10] Q. Wang, Z. Mao, B. Wang, and L. Guo, "Knowledge graph embedding: A survey of approaches and applications," *IEEE Transactions on Knowledge and Data Engineering*, vol. 29, no. 12, pp. 2724–2743, 2017.
- <a id="ref-11"></a>[11] M. R. Ackermann. (2022) dblp in rdf. [Online]. Available: [https://blog.dblp.org/2022/03/02/dblp-in-rdf/](https://blog.dblp.org/2022/03/02/dblp-in-rdf/)
- <a id="ref-12"></a>[12] D. Gordon. (2021) Fulltext search in neo4j. [Online]. Available: <https://neo4j.com/developer/kb/fulltext-search-in-neo4j/>
- <a id="ref-13"></a>[13] docs@stardog.com. Stardog documentation-machine learning. [Online]. Available:<https://docs.stardog.com/machine-learning#machine-learning>
- <a id="ref-14"></a>[14] Neo4j.Inc. (2022) Neo4j graph data science for machine learning. [Online]. Available: [https://neo4j.com/docs/graph-data-science/current/machine-learning/machine-learning/](https://neo4j.com/docs/graph-data-science/current/machine-learning/machine-learning/)
- <a id="ref-15"></a>[15] H. Chen, S. F. Sultan, and et.al., "Fast and accurate network embeddings via very sparse random projection," in *Proceedings of the 28th ACM International Conference on Information and Knowledge Management*, ser. CIKM '19, 2019, p. 399–408. [Online]. Available: <https://doi.org/10.1145/3357384.3357879>
- <a id="ref-16"></a>[16] A. Grover and J. Leskovec, "node2vec: Scalable feature learning for networks," in *Proceedings of the 22nd ACM SIGKDD*, 2016, pp. 855–864. [Online]. Available:<https://doi.org/10.1145/2939672.2939754>
- <a id="ref-17"></a>[17] W. L. Hamilton, Z. Ying, and J. Leskovec, "Inductive representation learning on large graphs," in *NeurIPS*, 2017, pp. 1024– 1034. [Online]. Available: [https://proceedings.neurips.cc/paper/2017/hash/5dd9db5e033da9c6fb5ba83c7a7ebea9-Abstract.html](https://proceedings.neurips.cc/paper/2017/hash/5dd9db5e033da9c6fb5ba83c7a7ebea9-Abstract.html)
- <a id="ref-18"></a>[18] I. F. Ilyas, T. Rekatsinas, V. Konda, J. Pound, X. Qi, and M. A. Soliman, "Saga: A platform for continuous construction and serving of knowledge at scale," in *SIGMOD*, 2022, pp. 2259–2272. [Online]. Available:<https://doi.org/10.1145/3514221.3526049>
- <a id="ref-19"></a>[19] W. Hu, M. Fey, M. Zitnik, Y. Dong, H. Ren, B. Liu, M. Catasta, and J. Leskovec, "Open graph benchmark: Datasets for machine learning on graphs," in *NeurIPS*, 2020.
- <a id="ref-20"></a>[20] H. Zeng, H. Zhou, and et.al., "Graphsaint: Graph sampling based inductive learning method," in *ICLR(8)*, 2020. [Online]. Available: <https://openreview.net/forum?id=BJe8pkHFwS>
- <a id="ref-21"></a>[21] H. Zeng, M. Zhang, Y. Xia, and et.al., "Decoupling the depth and scope of graph neural networks," *CoRR*, vol. abs/2201.07858, 2022. [Online]. Available:<https://arxiv.org/abs/2201.07858>
- <a id="ref-22"></a>[22] M. Chen, W. Zhang, and et.al., "Meta-knowledge transfer for inductive knowledge graph embedding," in *ACM SIGIR*, 2022, p. 927–937. [Online]. Available:<https://doi.org/10.1145/3477495.3531757>
- <a id="ref-23"></a>[23] M. S. Schlichtkrull, T. N. Kipf, and e. a. Peter Bloem, "Modeling relational data with graph convolutional networks," in *ESWC*, vol. 10843. Springer, 2018, pp. 593–607. [Online]. Available: [https://doi.org/10.1007/978-3-319-93417-4_38](https://doi.org/10.1007/978-3-319-93417-4_38)
- <a id="ref-24"></a>[24] M. Chen, Y. Zhang, X. Kou, and et.al., "r-gat: Relational graph attention network for multi-relational graphs," *CoRR*, vol. abs/2109.05922, 2021. [Online]. Available:<https://arxiv.org/abs/2109.05922>
- <a id="ref-25"></a>[25] M. Färber, "The microsoft academic knowledge graph: A linked data source with 8 billion triples of scholarly data," in *ISWC*, vol. 11779, 2019, pp. 113–129. [Online]. Available: [https://doi.org/10.1007/978-3-030-30796-7_8](https://doi.org/10.1007/978-3-030-30796-7_8)
- <a id="ref-26"></a>[26] T. Y. Cheng, Q. Hu, Q. Xie, N. Trigoni, and A. Markham, "Metasampler: Almost-universal yet task-oriented sampling for point clouds," *ECCV*, 2022. [Online]. Available: [https://doi.org/10.48550/arXiv.2203.16001](https://doi.org/10.48550/arXiv.2203.16001)
- <a id="ref-27"></a>[27] O. Dovrat, I. Lang, and S. Avidan, "Learning to sample," in *IEEE CVPR*, 2019, pp. 2760–2769. [Online]. Available: [http://openaccess.thecvf.com/content_CVPR_2019/html/Dovrat_Learning_to_Sample_CVPR_2019_paper.html](http://openaccess.thecvf.com/content_CVPR_2019/html/Dovrat_Learning_to_Sample_CVPR_2019_paper.html)
- <a id="ref-28"></a>[28] Y. Xiao, K. Gong, P. Zhou, G. Zheng, X. Liang, and L. Lin, "Adversarial meta sampling for multilingual low-resource speech recognition," in *AAAI*, 2021, pp. 14 112–14 120. [Online]. Available: <https://ojs.aaai.org/index.php/AAAI/article/view/17661>
- <a id="ref-29"></a>[29] Y. Lu, A. Chowdhery, S. Kandula, and S. Chaudhuri, "Accelerating machine learning inference with probabilistic predicates," in *SIGMOD*, ser. SIGMOD '18, 2018, p. 1493–1508. [Online]. Available: [https://doi.org/10.1145/3183713.3183751](https://doi.org/10.1145/3183713.3183751)
- <a id="ref-30"></a>[30] R. Bordawekar and O. Shmueli, "Enabling cognitive intelligence queries in relational databases using low-dimensional word embeddings," *CoRR*, vol. abs/1603.07185, 2016. [Online]. Available: [http://arxiv.org/abs/1603.07185](http://arxiv.org/abs/1603.07185)
- <a id="ref-31"></a>[31] M. Schule, H. Lang, M. Springer, A. Kemper, T. Neumann, and S. Gunnemann, "In-database machine learning with sql on gpus," in *SSDBM*, 2021. [Online]. Available: [https://doi.org/10.1145/3468791.3468840](https://doi.org/10.1145/3468791.3468840)
- <a id="ref-32"></a>[32] K. Awada, M. Y. Eltabakh, C. Tang, M. Al-Kateb, S. Nair, and G. Au,

"Cost estimation across heterogeneous sql-based big data infrastructures in teradata intellisphere," in *EDBT*, 2020.

- <a id="ref-33"></a>[33] S. Chaudhuri and K. Shim, "Optimization of queries with user-defined predicates," *ACM Trans. Database Syst.*, vol. 24, no. 2, pp. 177–228, 1999. [Online]. Available:<https://doi.org/10.1145/320248.320249>
- <a id="ref-34"></a>[34] M. Serafini, "Scalable graph neural network training: The case for sampling," *ACM SIGOPS Oper. Syst. Rev.*, vol. 55, no. 1, pp. 68–76, 2021. [Online]. Available:<https://doi.org/10.1145/3469379.3469387>
- <a id="ref-35"></a>[35] J. Johnson, M. Douze, and H. Jégou, "Billion-scale similarity search with gpus," *IEEE Trans. Big Data*, vol. 7, no. 3, pp. 535–547, 2021. [Online]. Available:<https://doi.org/10.1109/TBDATA.2019.2921572>
- <a id="ref-36"></a>[36] D. Chen, Y. Lin, W. Li, P. Li, J. Zhou, and X. Sun, "Measuring and relieving the over-smoothing problem for graph neural networks from the topological view," in *IAAI*, 2020, pp. 3438–3445.
- <a id="ref-37"></a>[37] J. Liu, K. Kawaguchi, B. Hooi, Y. Wang, and X. Xiao, "Eignn: Efficient infinite-depth graph neural networks," in *NIPS*, vol. 34, 2021, pp. 18 762–18 773. [Online]. Available: [https://proceedings.neurips.cc/paper/2021/file/9bd5ee6fe55aaeb673025dbcb8f939c1-Paper.pdf](https://proceedings.neurips.cc/paper/2021/file/9bd5ee6fe55aaeb673025dbcb8f939c1-Paper.pdf)
- <a id="ref-38"></a>[38] S. Bradley, A. Hax, A. Hax, and T. Magnanti, *Chapter 9: Integer Programming*. Addison-Wesley, 1977.
- <a id="ref-39"></a>[39] T. P. Tanon, G. Weikum, and F. M. Suchanek, "YAGO 4: A reasonable knowledge base," in *ESWC*, vol. 12123, 2020, pp. 583–596. [Online]. Available: [https://doi.org/10.1007/978-3-030-49461-2_34](https://doi.org/10.1007/978-3-030-49461-2_34)
- <a id="ref-40"></a>[40] X. Zhou, C. Chai, G. Li, and J. Sun, "Database meets artificial intelligence: A survey," *IEEE TKDE*, vol. 34, no. 3, pp. 1096–1116, 2022.
- <a id="ref-41"></a>[41] A. Mohamed, G. Abuoda, and et.al., "Rdfframes: Knowledge graph access for machine learning tools," *PVLDB*, vol. 13, no. 12, 2020. [Online]. Available: [http://www.vldb.org/pvldb/vol13/p2889-mohamed.pdf](http://www.vldb.org/pvldb/vol13/p2889-mohamed.pdf)
- <a id="ref-42"></a>[42] C. F. Draschner, C. Stadler, F. Bakhshandegan Moghaddam, J. Lehmann, and H. Jabeen, "Distrdf2ml-scalable distributed in-memory machine learning pipelines for rdf knowledge graphs," in *Proceedings of the 30th ACM*, 2021, p. 4465–4474. [Online]. Available: [https://doi.org/10.1145/3459637.3481999](https://doi.org/10.1145/3459637.3481999)
- <a id="ref-43"></a>[43] T. Kraska, A. Beutel, E. H. Chi, J. Dean, and N. Polyzotis, "The case for learned index structures," in *SIGMOD*. ACM, 2018, pp. 489–504. [Online]. Available:<https://doi.org/10.1145/3183713.3196909>
- <a id="ref-44"></a>[44] S. Hasan, S. Thirumuruganathan, J. Augustine, N. Koudas, and G. Das, "Multi-attribute selectivity estimation using deep learning," *CoRR*, vol. abs/1903.09999, 2019. [Online]. Available: [http://arxiv.org/abs/1903.09999](http://arxiv.org/abs/1903.09999)
- <a id="ref-45"></a>[45] W. G. Pedrozo, J. C. Nievola, and D. C. Ribeiro, "An adaptive approach for index tuning with learning classifier systems on hybrid storage environments," in *HAIS*, vol. 10870, 2018, pp. 716–729. [Online]. Available: [https://doi.org/10.1007/978-3-319-92639-1_60](https://doi.org/10.1007/978-3-319-92639-1_60)
- <a id="ref-46"></a>[46] S. Fernandes and J. Bernardino, "What is bigquery?" *Proceedings of the 19th International Database Engineering & Applications Symposium*, 2015.
- <a id="ref-47"></a>[47] N. Makrynioti, R. Ley-Wild, and V. Vassalos, "sql4ml A declarative end-to-end workflow for machine learning," *CoRR*, vol. abs/1907.12415, 2019. [Online]. Available:<http://arxiv.org/abs/1907.12415>
- <a id="ref-48"></a>[48] R. Bordawekar, B. Bandyopadhyay, and O. Shmueli, "Cognitive database: A step towards endowing relational databases with artificial intelligence capabilities," vol. abs/1712.07199, 2017. [Online]. Available:<http://arxiv.org/abs/1712.07199>
- <a id="ref-49"></a>[49] C. Riccardo, P. Paolo, and T. Saravanan, "Creating embeddings of heterogeneous relational datasets for data integration tasks," in *ACM SIGMOD*, USA, 2020, p. 1335–1349. [Online]. Available: <https://doi.org/10.1145/3318464.3389742>

## TL;DR
This vision paper proposes KGNet, a platform that provides on-demand graph machine learning (GML) as a service on top of RDF engines. It aims to bridge the gap between GML frameworks and RDF data stores by automating the training of GML models on task-specific subgraphs of a knowledge graph. The platform introduces SPARQLML, a GML-enabled query language, to allow for querying and inferencing over KGs using the trained models, thereby improving scalability, accuracy, and accessibility of GML on knowledge graphs.

## Key Insights
The paper introduces KGNet, a platform that automates the training of GML models on knowledge graphs by using task-specific subgraphs. This approach improves scalability and accuracy for tasks like node classification and link prediction. It also proposes SPARQLML, a SPARQL-like query language that allows users to query and perform inference over KGs using the trained GML models.

## Metadata Summary
### Research Context
- **Research Question**: The paper proposes the KGNet platform, which consists of two main components: GML-as-a-service (GMLaaS) and SPARQLML as a Service. GMLaaS automates the GML training pipeline by using a meta-sampling approach to extract task-specific subgraphs, selecting the optimal GML method based on budget constraints, and managing the trained models. SPARQLML as a Service provides a query interface that allows users to train, delete, and query GML models using a SPARQL-like syntax.
- **Methodology**: The experimental evaluation shows that training GML models on task-specific subgraphs identified by KGNet's meta-sampling approach significantly reduces training time and memory usage while maintaining comparable or even improved accuracy compared to training on the entire knowledge graph. For instance, on the DBLP dataset, KGNet achieved up to an 11% improvement in accuracy with at least a 22% reduction in memory and 27% reduction in training time.
- **Key Findings**: The primary outcome is the proposal of the KGNet platform, a vision for a fully-fledged GML-enabled knowledge graph platform. The paper outlines the architecture, key components, and research challenges, and provides a proof-of-concept evaluation that demonstrates the feasibility and benefits of the proposed approach.

### Analysis
- **Limitations**: The integration of GML frameworks with RDF engines is a critical step towards building scalable and intelligent knowledge graph applications. By automating the GML pipeline and providing a high-level query language, platforms like KGNet can significantly lower the barrier for data scientists and developers to apply advanced machine learning techniques to knowledge graphs.
- **Future Work**: The paper provides valuable insights into the architecture of a GML-enabled KG platform. The use of a meta-sampler to extract task-specific subgraphs is a key technique for improving scalability. The KGMeta graph, which stores metadata about trained models, is a clever way to enable seamless integration and query optimization. The proposed SPARQLML language provides a user-friendly interface for interacting with the system.