---
cite_key: azevedo_2024
title: A Polystore Architecture Using Knowledge Graphs to Support Queries on Heterogeneous Data Stores
authors: Leonardo Guerreiro Azevedo, Renan Francisco Santos Souza, Elton F. de S. Soares, Raphael M. Thiago, Julio Cesar Cardoso Tesolin, Anna C. Oliveira, Marcio Ferreira Moreno
year: 2023
doi: 10.1007/s00778-017-0474-5
url: https://doi.org/10.1007/s00778-017-0474-5
relevancy: Low
relevancy_justification: Tangentially related to knowledge management or data systems
tags: 
date_processed: 2025-07-02
phase2_processed: true
original_folder: arxiv_2308.03584_A_Polystore_Architecture_Using_Knowledge_Graphs_to
images_total: 13
images_kept: 13
images_removed: 0
keywords: 
---

# A POLYSTORE ARCHITECTURE USING KNOWLEDGE GRAPHS TO SUPPORT QUERIES ON HETEROGENEOUS DATA STORES ^*^

Leonardo Guerreiro Azevedo IBM Research Rio de Janeiro, RJ, Brazil lga@br.ibm.com

Renan Francisco Santos Souza^*^ National Center for Computational Sciences Oak Ridge National Laboratory Oak Ridge, TN, USA souzar@ornl.gov

Elton F. de S. Soares, Raphael M. Thiago IBM Research Rio de Janeiro, RJ, Brazil eltons@ibm.com, raphaelt@br.ibm.com Julio Cesar Cardoso Tesolin^*^ PGED/IME jcctesolin@ime.eb.br

Anna C. Oliveira^*^ PESC/COPPE acoliveira@cos.ufrj.br

Marcio Ferreira Moreno^*^ MOBR Systems Sao Paulo, Brazil marcio@mobr.ai

## ABSTRACT

Modern applications commonly need to manage dataset types composed of heterogeneous data and schemas, making it difficult to access them in an integrated way. A single data store to manage heterogeneous data using a common data model is not effective in such a scenario, which results in the domain data being fragmented in the data stores that best fit their storage and access requirements (*e.g.,* NoSQL, relational DBMS, or HDFS). Besides, organization workflows independently consume these fragments, and usually, there is no explicit link among the fragments that would be useful to support an integrated view. The research challenge tackled by this work is to provide the means to query heterogeneous data residing on distinct data repositories that are not explicitly connected. We propose a federated database architecture by providing a single abstract global conceptual schema to users, allowing them to write their queries, encapsulating data heterogeneity, location, and linkage by employing: (i) meta-models to represent the global conceptual schema, the remote data local conceptual schemas, and mappings among them; (ii) provenance to create explicit links among the consumed and generated data residing in separate datasets. We evaluated the architecture through its implementation as a polystore service, following a microservice architecture approach, in a scenario that simulates a real case in Oil & Gas industry. Also, we compared the proposed architecture to a relational multidatabase system based on foreign data wrappers, measuring the user's cognitive load to write a query (or query complexity) and the query processing time. The results demonstrated that the proposed architecture allows query writing two times less complex than the one written for the relational multidatabase system, adding an excess of no more than 30% in query processing time.
*Keywords* Knowledge and Data Engineering Tools and Techniques · Database integration · Distributed databases · Query processing

^*^ *For authors marked with * : Work done while at IBM Research*
![This flowchart illustrates a data processing workflow. Four workflows (Wf1-Wf4) are depicted: data quality assessment, geospatial index generation, expert knowledge ingestion, and data preparation. These workflows process geological raw data files through R-DBMS, Doc DBMS, and T-DBMS, culminating in training datasets stored in a parallel file system. Rectangles represent workflow steps, cylinders represent databases, and the legend clarifies data usage (used vs. generated). The image shows the stages involved in preparing data for a machine learning model.](_page_1_Figure_1.jpeg)

**Figure 1:** Workflows and data stores of the oil reserves discovery scenario (adapted from [[Souza *et al*., 2019]](#ref-Souza_et_al_2019)).

## 1 Introduction

Several modern applications manipulate diverse datasets with different models and usages, employing specific tools and techniques, *e.g.,* applications in medical informatics, oceanography, metagenomics, and exploration and production phases in Oil & Gas [[Souza *et al*., 2019]](#ref-Souza_et_al_2019).

For example, in an oil reserves discovery scenario, independent workflows process sizeable raw data files to generate training and validation datasets used by Deep Learning (DL) models, as illustrated in Figure [[1]](#ref-Figure_1). Although the workflows do not have direct relationships, they comprise several activities that consume and generate data from/to heterogeneous data stores in which data are not directly linked.

The first workflow processes geological raw data files to extract necessary metadata. It also assesses missing and displaced information as a measurement of metadata quality. While data files reside on a Parallel File System, the data quality score and extracted metadata are stored in a relational DBMS (R-DBMS). The second workflow considers the high-quality data files and generates geospatial indexes. This generated data is used to accelerate geospatial queries over the geological data and is stored in a document-oriented DBMS (Doc DBMS). The third workflow also considers the high-quality data files and augments the raw geodata files with extra knowledge informed by geoscience experts. This meta-information is stored in a Triplestore System (T-DBMS). Finally, the last workflow prepares the learning datasets used by DL algorithms. It queries the data from Doc DBMS and the related knowledge from the T-DBMS to generate datasets, which are stored as HDF5 files in the Parallel File System, ready to be used by DL algorithms.

In this scenario, the user is a Machine Learning (ML) expert with deep knowledge in the domain. When reporting the ML model, the user must query the data residing in the heterogeneous data stores. For instance, he/she should run a query to discover *what are the geographic coordinates extracted from the SEG-Y file that is being used to produce training and validation files and the spatial resolution between slices in the seismic data*. To answer this query, he/she has to inspect data residing on the file and the document database. Besides using specific tools to access both systems, the user should also know how the data is inter-related, *i.e.,* which lines of the file relate to objects of the document database. These issues illustrate the challenges of handling such scenarios: (i) the access to heterogeneous data stores; (ii) the linkage of heterogeneous data residing in remote distinct data stores.

The research question addressed in our work can be shortly enunciated as *How to query data that are not explicitly connected residing on heterogeneous data stores?*

Several data management solutions have emerged to handle heterogeneous data access, such as distributed file systems (*e.g.,* GFS [[Ghemawat *et al*., 2003]](#ref-Ghemawat_et_al_2003) and HDFS[[2]](#ref-2)), NoSQL databases (*e.g.,* MongoDB[[3]](#ref-3), AllegroGraph[[4]](#ref-4)), new data processing frameworks (*e.g.,* Spark[[5]](#ref-5)), and hybrid multimodal (*e.g.,* OrientDB[[6]](#ref-6)) or hybrid NewSQL (*e.g.,* LeanXcale[[7]](#ref-7)).

<a id="ref-2"></a>^2^ [https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html](https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html)

<a id="ref-3"></a>^3^ <https://www.mongodb.com/>

<a id="ref-4"></a>^4^ <https://allegrograph.com/>

<a id="ref-5"></a>^5^ <https://spark.apache.org/>

<a id="ref-6"></a>^6^ <https://orientdb.org/>

<a id="ref-7"></a>^7^ <https://www.leanxcale.com/>

In general, each solution handles a few kinds of data models or formats and does not addresses the diverse datasets required by modern applications [[Azevedo *et al*., 2020]](#ref-Azevedo_et_al_2020). On the other hand, migrating the heterogeneous data to a single database and schema does not work. Data conversion and loading is a very costly and time-consuming task, which is difficult to justify, and it may involve the integration of disparate data (*e.g.,* integration of structured data with text, web pages, semi-structured data, time series). Besides, no DBMS offers high performance in all kinds of data, *i.e.,* one size does not fit all [[Stonebraker, 2015]](#ref-Stonebraker_2015).

Therefore, a middleware that provides a seamless interface with an independent data model and (perhaps) data schemes is required to access heterogeneous data stores [[Stonebraker, 2015]](#ref-Stonebraker_2015). A Multidatabase System (MDBS) (or federated data system) provides a software layer that runs on top of individual autonomous data systems (or data stores) that share portions of their data. The MDBS allows users to access the various databases in an integrated way. A polystore system, a kind of MDBS, provides integrated access to several data stores, such as NoSQL, RDBMS, or HDFS, sometimes through a data processing framework [[Özsu and Valduriez, 2020]](#ref-Ozsu_and_Valduriez_2020). Nevertheless, there is still a lack of abstraction and query language to access heterogeneous data stores in an integrated way [[Stonebraker, 2015]](#ref-Stonebraker_2015).

To answer our research question, we propose a federated data system architecture that not only encapsulates heterogeneous data sources but also uses provenance for data linkage, *i.e.,* we create the explicit links by collecting the provenance of the workflow activities execution. Provenance contains information about the process and data used to derive the data product. We use causality as the kind of provenance information, which is the dependency relationships among data products and the processes that generate them, such as data-process dependencies and data dependencies [[Davidson and Freire, 2008]](#ref-Davidson_and_Freire_2008). So, the architecture provides an abstract layer to users to formulate queries based on a global conceptual schema, and, to be able to process the user query, it supports the creation of data mappings and record linkage transparent to service consumers. Its features are for: (i) Creation of global conceptual schema (the domain schema); (ii) Creation of local conceptual schemas for each external heterogeneous data store; (iii) Creation of mappings between global and local conceptual schemas; (iv) Creation of workflows' provenance schema; (v) Instrumentation of the applications that run the workflows; (vi) Capture of provenance during workflows execution; (vii) Processing of user queries.

We demonstrate the proposed architecture through its implementation as a RESTful web service in a microservice architecture [[Richardson and Ruby, 2008]](#ref-Richardson_and_Ruby_2008). We devise models to represent the global conceptual schema, local conceptual schemas, and mappings among them besides provenance schema and execution. This information is stored in a Knowledge Graph created using Hyperknowledge (HK), a hybrid conceptual model able to handle the multitude of media content and the meaning behind this data [[Moreno *et al*., 2017]](#ref-Moreno_et_al_2017). In particular, we are using the *context* element of HK to encapsulate and modularize the models and ingested data.

We evaluate the architecture implementation in a scenario that simulates a real case in Oil & Gas industry depicted previously in this section. The evaluation considered query complexity from the user and system perspectives. For the former, we analyzed the query components (like keywords, involved entities), and for the latter, we analyzed query execution time. We analyzed the architecture through comparing it against PostgreSQL FDW (Foreign Data Wrapper)[[8]](#ref-8). PostgreSQL is a widely used commercial open-source database management system and FDW is a module that allows access to external data stores using SQL language and wrappers. Our evaluation results demonstrated that while the query is more than two times less complex than the same written in SQL, the overhead created in query processing time is not greater than 30%. It indicates the applicability and utility of the architecture; although further investigations and improvements are required in query processing time.

The remainder of this work is divided as follows. Section [[2]](#ref-2_Background) presents the background and justify our choices. Section [[3]](#ref-3_Hyperknowledge_Polystore) presents the proposed architecture. Section [[4]](#ref-4_HKPoly_implementation_in_a_real_scenario) presents the proposal implementation and its evaluation. Section [[5]](#ref-5_Related_Work) presents the related work. Section [[6]](#ref-6_Conclusion) presents the conclusion and proposals of future work.

## 2 Background

This section presents the main concepts related to this work and the reasoning for their use in our proposal.

## 2.1 Multidatabase and Polystore system

A Multidatabase System (MDBS) provides a layer of software that runs on top of individual Database Management Systems (DBMSs) and facilitates users' access to various databases. The MDBS presents a Global Conceptual Schema (GCS) to the user, representing an integrated view of a database in which parts are allocated to different sites. In the MDBS environment, each site runs an individual DBMS, sharing some of its parts with the MDBS. Each local database

<a id="ref-8"></a>^8^ <https://www.postgresql.org/docs/current/postgres-fdw.html>

![This diagram illustrates a multi-mediator architecture for data integration. A client interacts with a chain of mediators (Mediator1...Mediator<sub>n</sub>), each communicating with wrappers accessing different data sources: an RDBMS (RDB), parallel file system (Files), document DBMS (JSON), and triple store (Triples). The architecture facilitates data access from diverse sources through a unified client interface.](_page_3_Figure_1.jpeg)

**Figure 2:** Layered Mediator/Wrapper Multidatabase System architecture (adapted from [[Özsu and Valduriez, 2020]](#ref-Ozsu_and_Valduriez_2020)).

is represented by a Local Conceptual Schema (LCS) [[Özsu and Valduriez, 2020]](#ref-Ozsu_and_Valduriez_2020). The database consumer formulates queries based on the GCS, and the MDBS translates them into a group of local queries and sends them to be executed by the individual DBMSs. The MDBS receives the responses, consolidates the queries' results, and returns an integrated result to the user [[Özsu and Valduriez, 2020]](#ref-Ozsu_and_Valduriez_2020).

The Mediator/Wrapper[[9]](#ref-9) is a kind of MDBS implementation. It uses a common GCS and interface language(s). The wrappers handle the heterogeneity performing mappings between LCS and GCS. Figure [[2]](#ref-Figure_2) illustrates this architecture with a mediator layered implementation. The wrappers encapsulate parts of the global database provisioned by heterogeneous data sources (*e.g.,* Relational-DBMS, Parallel File System, Document DBMS, and Triplestore).

The MDBS definition can be specialized when the encapsulated systems include other data store systems besides DBMS. Ozsu and Valduriez define this system as a polystore system, and it provides integrated access to several data stores, such as NoSQL, RDBMS, or HDFS, sometimes through a data processing framework (Figure [[2]](#ref-Figure_2)). Typically, they support only read-only queries, as processing distributed transactions across data stores is a hard problem [[Özsu and Valduriez, 2020]](#ref-Ozsu_and_Valduriez_2020). We are proposing a polystore architecture in this work.

## 2.2 Postgres FDW and SQL/MED

The International Organization for Standardization (ISO) developed and published the SQL/MED (Management of External Data)[[10]](#ref-10), an extension of SQL that allows applications to use standard SQL to access SQL and non-SQL data concurrently. SQL/MED defines an API that standardizes the communication between a SQL-based Server and wrappers (aka, Foreign-Data Wrappers or FDW) to access external servers (aka Foreign Servers) data. In other words, SQL/MED defines structures and routines the SQL-based Server and Foreign-Data Wrappers must provide [[Melton *et al*., 2001]](#ref-Melton_et_al_2001)[[Melton *et al*., 2002]](#ref-Melton_et_al_2002). Therefore, SQL/MED allows Relational-DBMS to work as an MDBS in a standard way, providing a homogeneous query language (SQL) and heterogeneous data structured (relational tables) to users. PostgreSQL supports SQL/MED since version 9.1[[11]](#ref-11). MySQL and MariaDB also implement the standard. Other DBMSs do not implement the standard, although they provide similar implementations to access heterogeneous data. Db2 provides distributed database feature, Microsoft SQL-Server offers Linked Server and Oracle provides database link [[Otuonye, 2021]](#ref-Otuonye_2021).

There are several foreign data wrappers already implemented for PostgreSQL[[12]](#ref-12), encapsulating systems like SQL DBMS, NoSQL Databases, File Systems, Scientific tools, Operating Systems, etc. Besides, many works published in the literature use PostgreSQL FDW in their proposals. For example, more than 25 papers are returned using the

<a id="ref-10"></a>^10^ <https://www.iso.org/standard/63476.html>

<a id="ref-9"></a>^9^ A mediator "is a software module that exploits encoded knowledge about certain sets or subsets of data to create information for a higher layer of applications" ([[Wiederhold, 1992]](#ref-Wiederhold_1992) *apud*[[Özsu and Valduriez, 2020]](#ref-Ozsu_and_Valduriez_2020)).

<a id="ref-11"></a>^11^ <https://wiki.postgresql.org/wiki/SQL/MED>

<a id="ref-12"></a>^12^ [https://wiki.postgresql.org/wiki/Foreign_data_wrappers](https://wiki.postgresql.org/wiki/Foreign_data_wrappers)

search string ("foreign data wrapper" OR fdw) AND (Postgres or PostgreSQL) in IEEE and ACM digital libraries. The robustness of PostgreSQL DBMS, its open-source license, the wrappers already implemented, and its wide use in literature motivated us to employ PostgreSQL FDW in validating our proposal.

## 2.3 Provenance

Provenance is also known as the audit trail, lineage, and pedigree of a data product. It contains information about the process and data used to derive the data product [[Davidson and Freire, 2008]](#ref-Davidson_and_Freire_2008).

In this work, we are employing ProvLake[[13]](#ref-13), a lineage data management system capable of capturing, integrating, and querying data across multiple workflows by leveraging provenance data. ProvLake's data model is a provenance data representation for workflows on data lakes [[Souza *et al*., 2019]](#ref-Souza_et_al_2019) which is built on W3C PROV [[Groth and Moreau, 2020]](#ref-Groth_and_Moreau_2020) and PROV-Wf [[Costa *et al*., 2013]](#ref-Costa_et_al_2013). ProvLake tracks data in distributed and heterogeneous environments.

ProvLake provides a lightweight *data tracking API* to be added to workflow codes (ProvLakeLib[[14]](#ref-14)), such as scripts. Also, it provides a *query API* for runtime analytical queries that integrate multistore data. When combined with a polystore, it can query data directly in multiple stores jointly with their provenance data. Conversely, our solution enables access to remote data not ingested during the capture process using remote data links loaded during provenance capture.

## 2.4 Knowledge Graph and Hyperknowledge (HK)

Knowledge Graphs have gained a broad use in research and business [[Ji *et al*., 2021]](#ref-Ji_et_al_2021) since the term was coined by a Google blog post [[Singhal, 2012]](#ref-Singhal_2012) in 2016 [[Ehrlinger and Wöß, 2016]](#ref-Ehrlinger_and_Woss_2016). There are several definitions of the term in the literature, and after a terminological analysis and based on the typical architecture of a knowledge-based system - which has information sources and is composed of a knowledge base (*e.g.,* ontology[[15]](#ref-15)) and a reasoning engine components, Ehrlinger and Wöß's proposed the following definition [[Ehrlinger and Wöß, 2016]](#ref-Ehrlinger_and_Woss_2016):

A knowledge graph acquires and integrates information into an ontology and applies a reasoner to derive new knowledge.

We follow this definition in our work since we create a knowledge base acquiring information of schemas and instances corresponding to the GCS, LCS, mappings, and provenance, and we use inference mechanisms for, *e.g.,* to navigate in the KG and compute queries to be executed on the remote data stores. To accomplish it, we use the IBM Hyperlinked Knowledge Graph[[16]](#ref-16) (or Hyperknowledge (HK) for short).

HK is a hybrid conceptual model able to handle the multitude of media content and the meaning behind this data [[Moreno *et al*., 2017]](#ref-Moreno_et_al_2017). More specifically, it supports the description of associations among symbolic semantics and non-symbolic data fragments within the same knowledge base. This representational approach takes advantage of combining in a single rationale user interaction, data segments (*e.g.,* sentences of a text document, fragments of images, segments of seismic data, frames of a video file, fragments of executable code), and semantic representations (*e.g.,* knowledge entities in an ontology that can be reasoned upon) [[Moreno *et al*., 2017]](#ref-Moreno_et_al_2017).

The foundation of HK is a pair of typical hypermedia concepts: (i) Nodes: represent information units; (ii) Links: define relationships among fragments of information (anchors) and properties of nodes.

Nodes can be of two classes: (i) Terminal nodes are composed of a collection of information units[[17]](#ref-17); (ii) Composite nodes, whose content is a set of nodes of the two classes. Composite nodes may also be specialized to better define the semantics of node collections. For example, a Context node is a composite node that contains a set of links and other attributes. They are handy for grouping knowledge and content specifications in logical containers [[Moreno *et al*., 2017]](#ref-Moreno_et_al_2017).

## 2.5 Hyperknowledge Platform — HK-Platform

HK-Platform is a set of tools developed for handling HK. From this set, we use two of them: HKBase and KES.

<a id="ref-16"></a>^16^ <https://github.com/ibm-hyperknowledge>

<a id="ref-17"></a>^17^ The exact notion of what constitutes an information unit is part of the node definition and depends on its specialization. For instance, a terminal node may represent a class (concept node) in an ontology or a media content (content node), such as a video [[Moreno *et al*., 2017]](#ref-Moreno_et_al_2017).

<a id="ref-13"></a>^13^ <http://ibm.biz/provlake>

<a id="ref-14"></a>^14^ <https://github.com/IBM/multi-data-lineage-capture-py>

<a id="ref-15"></a>^15^ Gruber defined ontology as "a set of representational primitives with which to model a domain of knowledge or discourse" [[Gruber, 2008]](#ref-Gruber_2008).

HKBase provides a RESTful API to manipulate structured data represented in HK and unstructured data (*e.g.,* images, videos). Structured data may be stored and retrieved from single data stores of different types (*e.g.,* Triplestores - Jena or AllegroGraph, Graph Databases - JanusGraph, Document Databases - MongoDB) while unstructured data is stored in Object Stores or File Stores (*e.g.,* MinIO, FileSystem).

In HKBase, data may be retrieved by using either HyQL (the Hyperknowledge Query Language) or SPARQL. HyQL is the language created to query data represented using HK constructs [[Moreno *et al*., 2021]](#ref-Moreno_et_al_2021). On the other hand, SPARQL is the query language for RDF (Resource Description Framework) defined by W3C [[Prud and Seaborne, 2008]](#ref-Prud_and_Seaborne_2008). RDF is a directed, labeled graph data format where datasets are represented as triples (subject, predicate, object) [[Zulkefli *et al*., 2013]](#ref-Zulkefli_et_al_2013), like the triple (LeonardoDaVinci, hasCreated, TheMonalisa). *Triplestores*, or RDF stores, are the matter of choice for storing and querying RDF data, like Jena and AllegroGraph. So, when HKBase is storing HK in a Triplestore database, HKBase provides a solution to query the underlying HK data using SPARQL, *i.e.,* one can query the database as if only RDF data was stored, filtering specific HK constructs.

KES (Knowledge Explorer System) [[Moreno *et al*., 2018]](#ref-Moreno_et_al_2018) is a web application that provides a user interface (UI) for collaborative management of HK bases (*i.e.,* knowledge bases with HK specifications). KES enables creating, validating, and curating HK descriptions in an interactive visual approach.

Our polystore solution is provisioned as an HKBase service and KES is used to inspect the ingested data and as an alternative to manually manage models and mappings.

## 2.6 Query complexity

The query complexity can be measured using the database and the user perspective. While the former considers the required time and the number of resources to run a query, the latter examines the user's cognitive load to read and write a query. Although query complexity measurement methods are well established for the database perspective, a few works address the user perspective [[Vashistha and Jain, 2016]](#ref-Vashistha_and_Jain_2016).

Ozsu and Valduriez [[Özsu and Valduriez, 2020]](#ref-Ozsu_and_Valduriez_2020) state that the number of relations and operators characterizes complex SQL queries. The complexity increases with the increasing number of equivalent operators.

Vashistha and Jain [[Vashistha and Jain, 2016]](#ref-Vashistha_and_Jain_2016) measure query complexity by: number of tables and columns in a query; query length (*i.e.,* number of characters); number of operators (*e.g.,* join, filter); query expressions (*e.g.,* like, greater than, or, and); and query runtime.

Yu *et al.* [[Yu *et al*., 2019]](#ref-Yu_et_al_2019) evaluate SQL query complexity considering the number of query components, like keywords (*e.g.,* group by, order by, intersect), nested subqueries, column selections, and aggregators. They define weights for each component, considering that the use of some of them makes the query harder to understand than others. In the same direction, Subali *et al.* [[Subali and Rochimah, 2018]](#ref-Subali_and_Rochimah_2018) propose a method to evaluate SQL query complexity based on the number of occurrences of SQL components classified in Variable Output, Variable Input, Nested Query, Join Table, and Number of Tables. The query complexity score is calculated using the number of occurrences of each SQL component multiplied by the assigned weight of its category.

For the SPARQL query language, Yuanbo *et al.* [[Guo *et al*., 2005]](#ref-Guo_et_al_2005) measure query complexity by the number of classes and properties. They used this approach to evaluate the LUBM benchmark queries. Souza *et al.* [[Souza *et al*., 2021a]](#ref-Souza_et_al_2021a) use a similar approach while evaluating workflow provenance techniques to build a holistic view to support the lifecycle of scientific ML. They measure query complexity based on the number of filter clauses, the patterns to match in the graph traversal, aggregations, and sorting, and the number of triples satisfying the patterns to match.

In this work, both perspectives of query complexity concern us. Our goal is to provide a model to the user that encapsulates heterogeneity, reducing his/her cognitive load when writing queries. At the same time, we also aim to build a solution that does not excessively increase the query processing time. We are considering the query components, like literature works, to measure user query complexity and query execution time to measure the database perspective.

## 3 Hyperknowledge Polystore

This section presents our proposal of a polystore architecture that provides users with a single layer for data access encapsulating data and data store heterogeneity, location, and data linkage using schemas metadata, mappings, and provenance. We named Hyperknowledge Polystore or HKPoly because we use HK (Section [[2.4]](#ref-2_4_Knowledge_Graph_and_Hyperknowledge_HK)) in its implementation. Although we could use other ontology representations, HKPoly supports our requirements, like the *Context* composite node we use for knowledge modularization.

![This diagram illustrates two pathways for interacting with a knowledge graph (KG) system. Path (a) shows a client service consumer interacting with the HKPoly service, which then uses a KG DBMS to access the HKPoly KG database. Path (b) depicts a client user employing a KG UI modeling tool to interact with the HKPoly service and, indirectly, the KG database. The diagram showcases the architecture's components and their interactions.](_page_6_Figure_1.jpeg)

**Figure 3:** HKPoly-client interaction: (a) Client application calls directly HKPoly service; (b) A user uses a UI which calls the HKPoly service.

## 3.1 Requirements and Stakeholders

To meet its goal, the Hyperknowledge Polystore supports the following requirements:

- (R1) Create a global conceptual schema (GCS) of the domain;
- (R2) Create a schema representation of the GCS;
- (R3) Create local conceptual schemas (LCS) to represent each remote heterogeneous data stores' schemas;
- (R4) Create mappings between the GCS and the LCSs;
- (R5) Create data links among the data residing in the data stores that are not explicitly linked;
- (R6) Process client queries, *i.e.,* receive the client query formulated using GCS, create queries considering the LCSs, run the queries on heterogeneous data stores, receive the result, and return to the user.

HKPoly stakeholders and their responsibilities are:

- (S1) *Domain Knowledge Engineer*: understands the domain and creates the GCS [[(R1)](#ref-R1)];
- (S2) *Database Administrators*: create the LCS of each heterogeneous data stores' shared schemas [[(R3)](#ref-R3)];
- (S3) HKPoly *Knowledge Engineer*: creates a schema for the GCS [[(R2)](#ref-R2)], and creates the mappings among GCS and LCSs [[(R4)](#ref-R4)];
- (S4) *Provenance Specialist*: understands the domain processes that manipulate the data residing on the heterogeneous data stores, creates the provenance schema of these processes, and supports developers to instrument the applications that support those processes [[(R5)](#ref-R5)];
- (S5) *Developers*: instrument the applications that support the domain processes [[(R5)](#ref-R5)];
- (S6) *Client User*: understands the GCS, formulates queries, and calls HKPoly to process the queries [[(R6)](#ref-R6)].

### 3.2 Architecture overview

This section presents how HKPoly architecture supports the requirements, depicting the HKPoly metamodel elements.

**HKPoly Knowledge Graph:** (HKPoly KG) metamodel was created based on W3C-Prov standard and ProvLake (Section [[2.3]](#ref-2_3_Provenance)). We proposed elements inheriting from W3C-Prov (like Collection and Entity), and we use ProvLake elements to represent workflow provenance schema and execution (*e.g.,* Workflow, Workflow Execution, Data Transformation, Data Transformation Execution, Attribute, Attribute Value).

HKPoly architecture supports requirements [[R1]](#ref-R1), [[R2]](#ref-R2), [[R3]](#ref-R3) and [[R4]](#ref-R4) through a service interface for client consumers manage domain and remote data stores metadata (Figure [[3]](#ref-Figure_3)). The service is accessed using a client application (Figure [[3]](#ref-Figure_3).a) or by a Web-based UI (Figure [[3]](#ref-Figure_3).b). The received metadata is stored in a database (HKPoly KG), which is managed by Database Management System (KG DBMS).

[[R1]](#ref-R1) Support: The HKPoly client user employs a simple language for the GCS creation, *i.e.,* a language without many constructs. We propose the use of a Knowledge Graph language (like RDF or Hyperknowledge), using vertices (nodes) to represent concepts and edges to represent relationships among them, respectively (Section [[2.4]](#ref-2_4_Knowledge_Graph_and_Hyperknowledge_HK)). As an example, the user represents the concepts *Seismic*, *Horizon* and *Well* as nodes, and the relationships *Seismic has Horizon*, *Seismic has Well* edges among these nodes. The user may create this model using the HKPoly UI or call HKPoly service. The GCS is stored in HKPoly KG.

![This image is a class diagram illustrating a data model. It shows the relationships between a `DatasetSchema` (a collection), `Attribute` (an entity), and a `referred` element. Relationships are defined using cardinality notations (e.g., 0..1, 1..*). The diagram clarifies how attributes relate to a dataset schema (as identifiers or general attributes), and how entities can be referenced. The purpose is to formally specify the structure of datasets within the paper.](_page_7_Figure_1.jpeg)

**Figure 4:** HKPoly model used to represent the GCS schema.

[[R2]](#ref-R2) Support: The Knowledge Engineer (KE) formulates a data schema to represent GCS domain elements as instances of the metamodel presented in Figure [[4]](#ref-Figure_4). The KE generates DatasetSchema for GCS's nodes, *e.g., Seismic*, *Horizon* and *Well* are created as dataset schemas. Attribute represent GCS's edges, *e.g., hasHorizon* and *hasWell* represent *has Horizon* and *has Well* edges which are related to *Seismic* dataset schema using isAttributeOf relationship. If the attribute identifies the class, the KE also creates the isIdentifierOf relationship, *e.g.,* the attribute *horizonURI* is identifier of *Seismic* dataset schema. The KE represents the relationship between two concepts using the referred relationship, *e.g.,* the attribute *Seismic.hasHorizon* referred the attribute *Horizon.horizonURI*.

[[R3]](#ref-R3) Support: The Database Administrator (DBA) creates LCS schemas for each shared portion of the remote data stores' databases using HKPoly template. This task may be automated by the DBA implementing a script that connects to the data store (*e.g.,* a MongoDB instance), reads the data store schema, creates the JSON content, and call HKPoly service. HKPoly service receives the request and creates the LCS schemas as instances of the metamodel presented in Figure [[5]](#ref-Figure_5), detailed as follows.

A DataStore may be a File System, Document Database, Relational Database Management System, Graph Database Management System among others. A DataStore runs on a Machine (wasRunOn relationship).

A Database resides in a DataStore (isInStore relationship), and it may have DatabaseSchemas that may have DatasetSchemas (isSchemaOf and isDataSchemaOf relationships, respectively).

DatasetSchema and Attributes are the same as presented in Figure [[4]](#ref-Figure_4). This excerpt is used to represent the GCS schema, and also to represent the LCS schema, *e.g.,* a table and columns of a remote PostgreSQL database.

An Attribute may be simple or complex (ComplexAttribute) (like a list or a dictionary). Simple Attributes cannot be subdivided. Complex attribute's elements may be composed by other attributes, which composition is represented by isMemberOfComplexAttribute relationship whith Attribute. An Attribute in a Schema can be equivalent to another Attribute in another Schema, even in different DataStores. We use alias to represent equivalent semantics and mappings between attributes, *e.g.,* an identifier column of a table in a RDBMS may be equivalent to a key of dictionary in a DocumentDBMS.

[[R4]](#ref-R4) Support: The mappings between GCS and LCS elements are performed by the HKPoly KE while creating alias relationships between GCS and LCS attributes. For instance, create an alias linking *Seismic.uri* of GCS with *Seismic.id* of a relational table of a PostgreSQL LCS. To accomplish this task, the KE should deeply understand GCS and LCS models. In our implementation (presented in Section [[4.2]](#ref-4_2_HKPoly_Implementation)), we have used the Context construct of HK to modularize the metadata to support the KE navigating in the models and creating the links.

[[R5]](#ref-R5) Support: The linkage between the remote heterogeneous data manipulated by independent workflows is achieved by capturing the provenance of their executions. Initially, a Provenance Specialist (PS) understands the workflows and creates their provenance schema. The PS works with Domain Experts and developers of the applications that support the workflows to create the schema[[18]](#ref-18) as instances of the classes presented in gray in Figure [[6]](#ref-Figure_6), such as: Workflow, its DataTransformations and manipulated Attributes.

Afterwards, the developers include calls to the ProvLakeLib (Section [[2.3]](#ref-2_3_Provenance)). in the code to capture the provenance execution and send it to the Provenance Manager (Figure [[7]](#ref-Figure_7)) to store data corresponding to the workflow execution as instances of the classes presented in white in Figure [[6]](#ref-Figure_6), such as: WorkflowExecution,

<a id="ref-18"></a>^18^ This model was created inheriting from W3C-Prov as presented by Souza *et al.* [[Souza *et al*., 2019]](#ref-Souza_et_al_2019). We omitted the stereotypes to simplify the model design.

![This image is a class diagram illustrating a data model. Rectangles represent classes (e.g., DataStore, Database, Attribute), with labels indicating class types and multiplicity. Arrows depict relationships (e.g., "isSchemaOf," "isMemberOfComplex") between classes, including cardinality constraints (e.g., "0..1," "1..*"). The diagram details the relationships between data stores (FileSystem, RDBMS, etc.), databases, schemas, and attributes, showing how they are interconnected within a system.](_page_8_Figure_1.jpeg)

**Figure 5:** HKPoly model used to represent the LCS schemas.

![This image is an Entity-Relationship Diagram (ERD) illustrating a data model. It depicts entities such as `Workflow`, `Data Transformation`, `Attribute`, `AttributeValue`, `DataStore`, and their relationships, indicated by labeled arrows and cardinality constraints (e.g., 1, *, 0..1). The diagram details the connections between workflow executions, data transformations, attribute values, and data storage, showing how data is generated, used, and derived throughout a workflow's lifecycle. The purpose is to formally represent the structure and relationships within a workflow data management system.](_page_8_Figure_3.jpeg)

**Figure 6:** Provenance model based on ProvLake [[Souza *et al*., 2019]](#ref-Souza_et_al_2019).

DataTransformationExecution and the used and generated AttributeValues. The DataReferences are the AttributeValues that identify the data records residing in the DataStores, *e.g., id* and *URI*.

The schemas metadata, mappings, workflow schema, and workflow execution data stored in HKPoly KG allow the data linkage. Hence, the mappings among global and local conceptual schemas allow identifying the linkage of instances of different data stores (*i.e.,* distinct LCSs) representing the same global concept when distinct workflows consume them. As an example, if one Workflow has a DataTransformation that consumes a *Seismic* file and generates data stored in a PostgreSQL table using *Seismic.id* as identifier, and it has another DataTransformation that reads the same file and generates data that is stored in a MongoDB collection using *Seismic.uri* as identifier, we can infer that these instances represent the same object.

[[R6]](#ref-R6) Support: An HKPoly architecture overview is depicted in Figure [[8]](#ref-Figure_8). It is based on the Multidatabase Mediator/Wrapper architecture [[Özsu and Valduriez, 2020]](#ref-Ozsu_and_Valduriez_2020) (Section [[2.1]](#ref-2_1_Multidatabase_and_Polystore_system)). To process client-user queries, HKPoly receives a user query formulated considering the GCS concepts and written using an HKPoly supported query language. Then, HKPoly

![The image is a data flow diagram illustrating a provenance tracking system. An instrumented client application sends data to a provenance manager, which then forwards it to a KG DBMS (Knowledge Graph Database Management System). Finally, the processed data is stored in an HKPoly KG (presumably a knowledge graph database specific to HKPoly). The diagram visually represents the stages of data processing and storage within the system.](_page_9_Figure_1.jpeg)

**Figure 7:** Provenance manager architecture overview.

![The image is a system architecture diagram. It illustrates the data flow in the HKPoly system. A client interacts with the HKPoly service, which in turn accesses data from various sources: a file system, document DBMS, relational DBMS, and a triplestore. These data sources are then integrated into a knowledge graph (HKPoly KG) via a KG DBMS. The diagram shows the system's layered architecture and data integration process.](_page_9_Figure_3.jpeg)

**Figure 8:** HKPoly architecture overview.

processes the query as follows: (i) It interprets and validates the input query concerning GCS elements, querying the KG, and supported operators; (ii) It creates local queries for each LCS that maps to the GCS elements used in the input query - HKPoly queries the KG to get the GCS and LCS mappings and provenance data required for query building; (iii) It creates an optimized query execution plan for the local queries; (iv) It coordinates the query execution on local DBMSs - *e.g.,* File System, Doc DBMS, RDBMS, and Triplestore in Figure [[8]](#ref-Figure_8); (v) It consolidates the results and sends the response to the client-user.

## 4 HKPoly implementation in a real scenario

This section presents the architecture implementation as well as its evaluation in a simulation of a real scenario. We present the scenario in Section [[4.1]](#ref-4_1_Scenario), then HKPoly implementation in Section [[4.2]](#ref-4_2_HKPoly_Implementation), and its evaluation in Section [[4.3]](#ref-4_3_Evaluation).

## 4.1 Scenario

We evaluate the architecture implementation in the oil reserves discovery, a critical scenario for the Oil & Gas (O&G) industry. We are concerned with seismic image interpretation. Typically, these images cover large extensions of the earth, and, by inspecting the images, geoscientists try to identify geological features, *e.g.,* salt bodies. Academia and O&G industry aim at automating this activity [[Randen *et al*., 2000]](#ref-Randen_et_al_2000), and deep learning (DL) is a promising ML technique for this [[Chevitarese *et al*., 2018]](#ref-Chevitarese_et_al_2018).

Managing the data generated during the training of production DL models is hard [[Souza *et al*., 2021b]](#ref-Souza_et_al_2021b). This is particularly true in geoscience problems [[Gil *et al*., 2018]](#ref-Gil_et_al_2018). It requires preprocessing, cleaning, and performing complex integrated data analysis. This lifecycle is decomposed into parts addressed by collaborating teams of geoscientists, computational scientists, engineers, and statisticians, among others. Each team has a preferred way to automate tasks and store data, while also having to consume data from other teams, whose preferences might differ.

In particular, the present case study focuses on activities that range from preprocessing large raw geological data files to the generation of training and validation datasets for DL models. More details are presented by [[Souza *et al*., 2019]](#ref-Souza_et_al_2019), [[Souza *et al*., 2021b]](#ref-Souza_et_al_2021b)). In this work, we focus on the heterogeneous data aspect of the use case. A description of the involved processes is presented in Section [[1]](#ref-1_Introduction). Figure [[1]](#ref-Figure_1) illustrates the processes simplified as four chained data processing workflows [[Souza *et al*., 2019]](#ref-Souza_et_al_2019), where each workflow uses one or more data store with heterogeneous data models.

In this case study, the user is an ML expert with deep knowledge in the domain. When reporting the results of the ML model, the user must provide domain data about the processed data by the workflows. An exemplary data to be queried is shown in Table [[1]](#ref-Table_1), which illustrates the various data stores that need to be integrated to resolve the query.

![This diagram depicts a system architecture. It shows a client user interacting with a Knowledge Exchange System (KES) which connects to an IHKBase. This communicates with an HKBase, which uses HKPolyService and HKBaseService to access data from DBMS and IDBMS. The queried data includes seismic information and geodetic systems, stored in PostgreSQL, AllegroGraph, and Mongo. The diagram illustrates data flow and component interactions within the system.](_page_10_Figure_1.jpeg)

**Table 1:** Seismic data and the data stores where they reside.

**Figure 9:** HKPoly service component diagram considering components to support requirements [[R1]](#ref-R1), [[R2]](#ref-R2), [[R3]](#ref-R3) and [[R4]](#ref-R4).

### 4.2 HKPoly Implementation

This section presents an architecture implementation to support the requirements (Section [[3.1]](#ref-3_1_Requirements_and_Stakeholders)). HKPoly data is stored as HK (Section [[2.4]](#ref-2_4_Knowledge_Graph_and_Hyperknowledge_HK)). The reason for this choice is to modularize the several kinds of data using the Context node of HK and reuse the same element in different contexts. The following tools are used in HKPoly implementation: HKBase and KES (Section [[2.5]](#ref-2_5_Hyperknowledge_Platform_HK-Platform)), ProvLake (Section [[2.3]](#ref-2_3_Provenance)), and PostgreSQL Foreign Data Wrapper (FDW) (Section [[2.2]](#ref-2_2_Postgres_FDW_and_SQL_MED)).

HKPoly service is implemented as a RESTful web service[[19]](#ref-19) [[Richardson and Ruby, 2008]](#ref-Richardson_and_Ruby_2008)[[Richardson *et al*., 2013]](#ref-Richardson_et_al_2013) provisioned by HKBase. This implementation is a realization of the architecture depicted in Figure [[8]](#ref-Figure_8).

Figure [[9]](#ref-Figure_9) presents a UML component diagram of HKPoly architecture to support [[R1]](#ref-R1), [[R2]](#ref-R2), [[R3]](#ref-R3), and [[R4]](#ref-R4) through two mechanisms: Service Interface, and UI tool. HKPoly Service Interface is provisioned as part of HKBase API, *i.e.,* HKPoly endpoints are provisioned as part of HKBase contract - IHKPoly interface in the diagram. Client applications call HKPoly service to create domain model, GCS, LCS, and mappings among them. HKPoly service uses HKBase's HKDataSource to store *HKPoly Knowledge Graph* data in its main DBMS. The main DBMS being the one supported by the HKBase instance being used, *e.g.,* Apache Jena[[20]](#ref-20) RDF store. In the UI mechanism, a client may use the KES tool to visualize and manipulate the ingested data.

The domain model may be created using basic elements of HK (like Concept node and Connectors for relationships), and the GCS, LCS, and mappings are created using the models presented in Section [[3.2]](#ref-3_2_Architecture_overview) in Figure [[4]](#ref-Figure_4) and Figure [[5]](#ref-Figure_5).

As an example, consider the domain model illustrated in Table [[1]](#ref-Table_1), *i.e., Seismic* node and edges connecting it with *name*, *inline*, *crossline*, *well*, *horizon*, and *epsg* properties. HKPoly creates a GCS for the domain using the proposed schemas, which data is illustrated in Table [[2]](#ref-Table_2) first line (after the header).

Consider also we have *Seismic* data stored in the following remote heterogeneous data stores, as follows:

- PostgreSQL: *SeismicHeader* table with columns *id*, *inline*, *crossline*, *header_info*, *filepath*;
- AllegroGraph: *SeismicCls* class with properties *URI*, *name*, *hasWell*, and *hasHorizon*;
- MongoDB: *Seismc_data* collection with fields *identifier*, *name*, *num_ilines*, *num_xlines*, *epsg*.

Table [[2]](#ref-Table_2) (lines 3, 4, and 5) presents the LCS remote data store schemas, and Table [[3]](#ref-Table_3) presents the mappings between GCS and LCS. These mappings are done using alias relationship of HKPoly model (Figure [[5]](#ref-Figure_5)).

<a id="ref-20"></a>^20^ <https://jena.apache.org/>

<a id="ref-19"></a>^19^ RESTful web services follow REST [[Fielding and Taylor, 2002]](#ref-Fielding_and_Taylor_2002) principles to expose cohesive and low coupled web services.

| Line | DataStore | Database | Schema | DatasetSchema | Attribute<br>(isAttributeOf) | Identifier<br>(isIdentifierOf) |
|------|--------------|-----------------|--------------|---------------|---------------------------------------------------------|--------------------------------|
| 1 | | | | Seismic | URI, inline, crossline,<br>well, horizon, epsg | URI |
| 2 | PostgreSQL | SeismicDB | SeismicSQ | SeismicHeader | id, inline, crossline,<br>header_info, filepath | id |
| 3 | AllegroGraph | Seismic catalog | Seismic repo | SeismicCls | URI, name, hasWell,<br>hasHorizon | URI |
| 4 | MongoDB | Seismicdb | Seismic | Seismic_data | identifier,<br>name,<br>num_ilines,<br>num_xlines, epsg | identifier |

**Table 2:** GCS of Seismic (line 1) and LCS of the Seismic data residing in the remote stores (lines 2, 3, and 4).

**Table 3:** Seismic GCS and LCS mappings attribute mappings.

| GCS | LCS |
|-------------------|-------------------------|
| Seismic.URI | SeismicHeader.id |
| Seismic.URI | SeismicCls.id |
| Seismic.URI | Seismic_data.identifier |
| Seismic.inline | SeismicHeader.inline |
| Seismic.crossline | SeismicHeader.crossline |
| Seismic.well | SeismicCls.hasWell |
| Seismic.horizon | SeismicCls.hasHorizon |
| Seismic.epsg | Seismic_data.epsg |

[[R5]](#ref-R5) is supported by provenance manager component, named as *HKProvManager*, provisioned also as a RESTful web service. The implementation is a realization of the overview architecture presented in Figure [[7]](#ref-Figure_7).

Figure [[10]](#ref-Figure_10) presents a component diagram of *HKProvManager*. So, the developers of client applications create hooks in their code (illustrated by the Instrumented client application component of Figure [[10]](#ref-Figure_10)) which make calls to *HKProvManager* service. *HKProvManager* uses HKBase services to store the provenance data, using the HKDataSource to access the DBMS that stores *HKPoly Knowledge Graph*. The service calls aim to store provenance execution data, like:

- 1. Workflow start information;
- 2. Workflow DataTransformation executions and their input parameters (used Attributes and AttributeValues) and returned data (generated Attributes and AttributeValues)
- 3. Workflow end information.

The Workflow schema and its counterparts are created when execution data is loaded, or a *Provenance Expert* may use the KES to create this schema. So, the only requirement of the instrumented code is that the Attributes' names are the same as those defined in the LCS. It allows the identification of which domain data were consumed by each workflow and, consequently, the linkage among the object fragments residing in each data store. These data are retrieved when HKPoly handles client queries, and it is combined with remote data stores' data to answer the user request. Details are presented when explaining how HKPoly supports Requirement [[R6]](#ref-R6).

Figure [[11]](#ref-Figure_11) presents a UML Activity diagram to exemplify the execution of the workflows of Figure [[1]](#ref-Figure_1) to process the Seismic *Netherlands*. Workflows are presented as actions for simplification. The first workflow *Data quality assessment* reads the *netherlands segy* file from the *FileSystem* and inserts *Netherlands assessments* in a *PostgreSQL* database table. The second workflow *Geospatial index generation* reads the same file and stores *Netherlands indexes* in a *MongoDB* collection. The third workflow *Expert knowledge ingestion* stores *Netherlands knowledge information* in AllegroGraph. An Expert provides this information when analyzing the *netherlands segy* seismic file. Finally, the fourth workflow Data preparation creates the training data by reading all the stored data and generating the *netherlands.train* file which is stored in the *FileSystem*. During this workflow execution, while storing data in the data stores, the instrumented client application also sends provenance data calling *HKProvManager*, which stores the DataReferences for the record, document, and triples (id, identifier, and respectively) in *HKPoly Knowledge Graph*. Table [[4]](#ref-Table_4) presents the DataReferences captured during the execution of Netherlands workflow. The provenance data, GCS, LCSs, and mappings are used to compute the polystore query detailed in [[R6]](#ref-R6) support implementation.

![The image is a system diagram illustrating the architecture of an application using HBase. It shows an instrumented client application interacting with an HKProvManager, which in turn connects to an HBase system comprised of an HKBaseService and an HKDataSource. The HKDataSource uses a DBMS via an IDBMS interface. The diagram clarifies the data flow and component relationships within the described system.](_page_12_Figure_1.jpeg)

**Figure 10:** Provenance Manager component architecture.

![This flowchart depicts a data processing workflow. Netherlands assessment and knowledge information are input, processed through PostgreSQL, MongoDB, and AllegroGraph databases. Geospatial index generation and expert knowledge ingestion are intermediate steps. Data quality assessment precedes the main process. The final outputs are stored in the filesystem. The diagram illustrates the data flow and storage mechanisms used in the research.](_page_12_Figure_3.jpeg)

**Figure 11:** Example of execution of the workflows of Figure [[1]](#ref-Figure_1) to investigate the Seismic Netherlands. Workflows are illustrated as actions in the diagram.

| **Table 4:** Remote data store data captured during Seismic interpretation DL workflow execution. | | |
|-----------------------------------------------------------------------------------------------|--|--|
| | | |

| DataTransformation | DatasetSchema | Attribute | AttributeValue |
|-----------------------------|---------------|---------------------------------------------|-------------------------|
| Data quality assessment | SeismicHeader | id | 12345 |
| Geospatial index generation | Seismic_data | identifier | 1111 |
| Expert Knowledge Ingestion | SeismicCls | URI<br>http://oilandgas/Seismic#Netherlands | |
| Data preparation | Training File | path | /data/netherlands.train |

Figure [[12]](#ref-Figure_12) presents HKPoly component diagram concerning the support for [[R6]](#ref-R6). It is a realization of the architecture depicted in Figure [[8]](#ref-Figure_8). The client application creates a query based on the GCS model using the Hyperknowledge query language (HyQL[[21]](#ref-21)) [[Moreno *et al*., 2021]](#ref-Moreno_et_al_2021) (Section [[2.4]](#ref-2_4_Knowledge_Graph_and_Hyperknowledge_HK)). An example is Query [[1]](#ref-Query_1) which retrieves *Seismic* attributes (lines 1 and 2) considering workflow *geological_data_ingestion_workflow* (Line 3) and *Seismic*'s *name* is *Netherlands* (Line 4). The workflow is referenced using the from clause, which indicates that queried data is contained in a Context object.

<a id="ref-Figure_12"></a>![This diagram illustrates a system architecture. A "Client service consumer" interacts with "IHKPoly," which in turn uses "HKPolyService" within "HKBase." "HKPolyService" uses "HKDataSource," which connects to an "IDBMS" and "DBMS." "HKDataSource" is further connected to a "PostgreSQL FDW," which acts as an interface to "FileSystem," "MongoDB," "PostgreSQL," and "Triplestore" databases. The diagram shows data flow and dependencies between different components.](_page_13_Figure_1.jpeg)

**Figure 12:** HKPoly component diagram considering the [[R6]](#ref-R6) support.

<a id="ref-Query_1"></a>**Query 1:** HyQL query to retrieve Netherlands seismic data.

```text
1 select Seismic . inline , Seismic . crossline ,
2 Seismic . hasWell , Seismic . hasHorizon , Seismic . epsg
3 where Seismic from geological_data_ingestion_workflow
4 and Seismic . name = " Netherlands "
```

HKPoly interprets and validates the query using the data stored in the *HKPoly Knowledge Graph*. Query [[2]](#ref-Query_2) is a example of HKPoly service query used to retrieve KG's data. It retrieves workflow execution and related GCS data (lines 1, 2, and 3), besides Foreign Data Wrapper data (lines 4 and 5), which is used by HKPoly to create a polystore query which will be explained afterward. The SPARQL language is used to navigate in KG executing, *e.g.,* query path and inverse property navigation (lines 10 and 11) and traversing the workflow elements (lines 8 to 15) and GCS (lines 16 to 19). The att variable is used to connect workflow and GCS data (Line 10 for workflow and Line 16 for the GCS).

<a id="ref-21"></a>^21^ The HyQL grammar is presented in <https://ibm.ent.box.com/v/iswc2021-hyql-grammar>

<a id="ref-Query_2"></a>**Query 2:** SPARQL query to retrieve workflow execution and LCS data.

```text
1 select distinct ? wfe ? atv ? atvValue ? att ? attName
2 ? datasetSchema ? datasetSchemaName
3 ? dataStore ? dataStoreName
4 ? attFDW ? attFDWName
5 ? datasetSchemaFDW ? datasetSchemaFDWName
6 where
7 {
8 ? atv <hk :// id / wasDerivedFromAttribute > ? att .
9 ? att <hk :// id / name > ? attName .
10 ? atv <hk :// id / wasGeneratedBy >
11 |^ < hk :// id / used > ? dte .
12 ? atv <hk :// id / value > ? atvValue .
13 ? dte <hk :// id / wasMemberOfWorkflowExecution > ? wfe .
14 ? wfe <hk :// id / wasDerivedFromWorkflow >
15 <hk :// id / ${ workflow } >.
16 ? att <hk :// id / isAttributeOf > ? datasetSchema .
17 ? datasetSchema <hk :// id / name > ? datasetSchemaName .
18 ? att <hk :// id / isStoredInStore > ? dataStore .
19 ? dataStore <hk :// id / name > ? dataStoreName .
20 ? attFDW <hk :// id / alias > ? att .
21 ? attFDW <hk :// id / name > ? attFDWName .
22 ? attFDW <hk :// id / isAttributeOf > ? datasetSchemaFDW .
23 ? datasetSchemaFDW < hk :// id / name >
24 ? datasetSchemaFDWName .
25 }
26 order by ? wfe ? dte ? atv
```

To access the remote heterogeneous data stores, HKPoly uses PostgreSQL Foreign Data Wrapper (FDW) (Section [[2.2]](#ref-2_2_Postgres_FDW_and_SQL_MED)). HKPoly does not implement a new polystore connector interface since there are some available, and the work focus on validating the use of the GCS and provenance to enable a seamless access interface to users regarding abstraction and data linkage. So, we use PostgreSQL FDW as our polystore connector since it has a broad use and several foreign data wrappers. Hence, the PostgreSQL FDW schemas are ingested as LCS, *i.e.,* the remote data stores' shared data are represented as LCS of PostgreSQL FDW data, and GCS is liked to these LCSs. The links are created using alias relationship which is used in Query [[2]](#ref-Query_2) (Line 20) to reach FDW data in lines 21 to 24. After getting this information, HKPoly computes the SQL presented in Query [[3]](#ref-Query_3). This query is sent to PostgreSQL FDW which process the results and returns to HKPoly the response to the Client service consumer.

<a id="ref-Query_3"></a>**Query 3:** SQL to get data of Netherlands seismic.

```text
1 SELECT distinct fdw_kb_seismic ." hasWell ",
2 fdw_mongo_seismic ." epsg ",
3 fdw_seismic_header ." crossline ",
4 fdw_kb_seismic ." hasHorizon " ,
5 fdw_seismic_header ." inline "
6 FROM segy fdw_segy , kb_seismic fdw_kb_seismic ,
7 mongo_seismic fdw_mongo_seismic ,
8 seismic_header fdw_seismic_header ,
9 ( VALUES ( ' netherlands . sgy ',
10 ' http :// br . ibm . com / hkpoly / seismicData_ABox # Netherland_3D ',
11 ' http :// br . ibm . com / hkpoly / seismicData_ABox # Netherland_3D ', 1 ))
12 as p( LocalFileSystem1_prov_id , Allegro1_prov_id ,
13 Mongo1_prov_id , Postgres1_prov_id )
14 WHERE fdw_kb_seismic . uri =p. Allegro1_prov_id
15 AND fdw_mongo_seismic . uri =p. Mongo1_prov_id
16 AND fdw_seismic_header . seismic_header_id =
17 p. Postgres1_prov_id
18 AND fdw_kb_seismic . name = ' Netherlands '
19 AND fdw_seismic_header . name = ' Netherlands '
```

In Query [[3]](#ref-Query_3), the from clause (lines 6 to 8) lists the PostgreSQL Foreign Tables[[22]](#ref-22) that maps to the remote data stored in a *segy file*, *AllegroGraph knowledge base triples*, *Mongo Seismic collection*, and *Seismic_Header table*. Lines 9 to 13 compute a "*constant table*" using the VALUES[[23]](#ref-23) SQL clause with the workflow executions data values retrieved using Query [[2]](#ref-Query_2). In the where clause, the *Foreign Tables* and *constant table* are joined (lines 14 to 17), and, as *Seismic.name* is linked to *kb_seismic* and *seismic_header Foreign Tables*, lines 18 and 19 are included in the SQL during its generation. The returned data is present in lines 1 to 5, which references the columns of the *Foreign Tables* mapping to *Seismic* domain object.

### 4.3 Evaluation

Our evaluation measures query complexity considering the two perspectives described in Section [[2.6]](#ref-2_6_Query_complexity): the user perspective and the database perspective.

### 4.3.1 Query Complexity - User's Perspective

We choose counting the query components to estimate the user's cognitive load measurement. It is an approach presented in some works as showed in Section [[2.6]](#ref-2_6_Query_complexity). We do not choose a weighted sum because there is no convergence that a weighting technique would improve the evaluation. We infer that counting the query components, regardless of the summing technique, is a fair estimate to evaluate the user's cognitive load.

<a id="ref-22"></a>^22^ Foreign tables behave like regular tables, and they are used to create mappings in a PostgreSQL database to external objects [[Melton *et al*., 2001]](#ref-Melton_et_al_2001).

<a id="ref-23"></a>^23^ <https://www.postgresql.org/docs/current/sql-values.html>

| Query Components | Query 1 | Query 3 |
|------------------|---------|---------|
| Projection | 5 | 5 |
| Filter | 1 | 1 |
| Join Clause | 0 | 3 |
| From Clause | 1 | 5 |
| Total | 7 | 14 |

**Table 5:** Accounting query components as an estimate of user's cognitive load.
In this case, we count query components as an estimate to measure the user's cognitive load while writing a query. As described in Table [[5]](#ref-Table_5), the user query (Query [[1]](#ref-Query_1)), written in HyQL language, has 5 elements in the projection, 1 element in from clause, and 1 query filter. It results in 7 query components. On the other hand, the equivalent polystore SQL query (Query [[3]](#ref-Query_3)) has 5 elements in the projection, 5 elements in from clause, 3 joins and 1 query filter, resulting on 14 query components [[24]](#ref-24). Hence, in this example, we can infer that the query written in HyQL is less complex than the SQL query generated by HKPoly to access the external data.

### 4.3.2 Query Complexity - Database's Perspective

In this case, we evaluate query complexity by measuring its processing time. Therefore, we evaluate the processing time HKPoly takes to process the user query, *i.e.,* the implementation depicted in Figure [[12]](#ref-Figure_12) to support [[R6]](#ref-R6). We compared this time against the time required to process solely the *PostgreSQL FDW* query. The HKPoly processing time includes: (i) receive the query (through *IHKPoly* interface), *e.g.,* Query [[1]](#ref-Query_1); (ii) parser the received query; (iii) run queries over *HKPoly Knowledge Graph* (using *HKDataSource*) to get required metadata and mappings, running Query [[2]](#ref-Query_2) and others; (iv) compute the *PostgreSQL FDW* query, *e.g.,* Query [[3]](#ref-Query_3); and, (v) run the computed query using *PostgreSQL FDW*. The compared *PostgreSQL FDW* time corresponds only to the time elapsed in Step [[4.3.2]](#ref-4_3_2_Query_Complexity_Databases_Perspective). We vary the data volume of

<a id="ref-24"></a>^24^ We are considering the constant table of Listing [[1]](#ref-Query_1), created using Values clause, counting as 1 since its data can be encapsulated, *e.g.,* in a temporary table, making the query easier to formulate.

*HKPoly Knowledge Graph:* and the data volume of remote data stores to analyze HKPoly overhead when remote data stores' data volume increases.

The first step to verify our hypothesis is to build an experimental deployment of our envisioned HKPoly architecture implementation. For that, we use Docker[[25]](#ref-25) container solution, allocating 5 CPUs, 10GB RAM, and a swap area of 2GB in a machine with i5 Intel Quad Core 2GHz CPU and 16 GB RAM. HKBase, and its services (including HKPoly and *HKDataSource*) are deployed in a container. Our test bed mirrored the proposed architecture presented in Figure [[12]](#ref-Figure_12), considering that all servers were part of the same network. In this setup, we use *Apache Jena* as HKBase's main DBMS, and it is deployed in a single container. Each remote data store is also deployed in a separate container using a proper schema to match the seismic domain model, corresponding to the scenario presented in Section [[4.1]](#ref-4_1_Scenario) and used to describe HKPoly implementation (Section [[4.2]](#ref-4_2_HKPoly_Implementation)). In this setup, we have the seismic data residing on *AllegroGraph*, *MongoDB*, and *PostgreSQL*. Table [[2]](#ref-Table_2) exemplifies Seismic attributes of data on each data store. The *PostgreSQL FDW* is deployed in a single container and loaded with data wrappers plugins to provide communication and data transformation between the remote databases. All these containers are started altogether with a composing script.

After the test environment is set up, we load domain data into the remote stores and provenance data into *HKPoly Knowledge Graph*. To control the volume of data, we generate domain data in what we call a batch. A batch has 16KB and represents three different files generated by a synthetic data generator whose schemas match the remote databases' schemas. They correspond to the data used by the three data transformations presented in Figure [[11]](#ref-Figure_11). After being generated, we simulate the data transformations' execution and load the results in *PostgreSQL*, *MongoDB*, and *AllegroGraph*, respectively. The generated provenance is loaded into *HKPoly Knowledge Graph*. Afterward, we start our performance tests.

We choose to run the test of query processing time performance using different numbers of batches varying the data volume to understand its influence on the processing. We start with one batch (B001) and then increase to 50, 100, 400, and 700. For each query performance test, we purge the provenance execution data from the *HKPoly Knowledge Graph* repository, keeping the schemas (GCS, LCS, provenance, and mappings schemas), and erase the remote databases' contents. Also, for each batch quantity, the query presented in Query [[1]](#ref-Query_1) is executed fifty times, so we can calculate the aggregated statistics for each one, waiting for one second between queries requests. According to Hoefler and Belli [[Hoefler and Belli, 2015]](#ref-Hoefler_and_Belli_2015), the academic literature suggests that sample sizes between thirty and forty are sufficient for normal distributions. Although we have not verified that the query processing time is normally distributed, we use the sample size of fifty based on this assumption.

Finally, we instrument HKPoly service to capture query execution times to understand the impact of building the query to be executed on the *PostgreSQL FDW* component (which we name as BuildingQuery step), *i.e.,* transform the input query (*e.g.,* Query [[1]](#ref-Query_1) to Query [[3]](#ref-Query_3) in the case of one batch). We collect the BuildingQuery step time and the time to run the query in *PostgreSQL FDW*, whose sum corresponds to the whole query execution time. We assume that the time of the *Client Application* to send the query to HKPoly and the time of HKPoly to send the response back is negligible. The result of the query response time experiments for each batch's quantities is shown in Figure [[13]](#ref-Figure_13). It presents the medians of the overall query response time extracted from the fifty rounds executed on each batch experiment. It shows this response time split into two parts: one for the query building (BuildingQuery) and another one for the *PostgreSQL FDW* query execution (FDW Query Execution).

Although it is straightforward to assume that the overall query response time would increase due to the increasing loaded data, the time consumed to build the *PostgreSQL FDW* SQL query is not the ruling part of the process. In the worst case, our experiments show that the transformation process takes less than 30% of the overall query processing time. We expect that this behavior remains the same whenever more data is loaded into the HKPoly environment.

<a id="ref-25"></a>^25^ <https://www.docker.com/>

<a id="ref-Figure_13"></a>![The image displays a bar chart comparing the time (in milliseconds) taken for HyQL-to-SQL query building and FDW SQL query execution at varying batch quantities (B001, B050, B100, B400, B700). Each bar is divided, showing the time spent in each process. The chart demonstrates how execution time increases with batch size for both processes, with FDW SQL query execution dominating the total time at larger batch quantities.](_page_16_Figure_1.jpeg)

**Figure 13:** HyQL to SQL Query Building and FDW SQL Query Execution Response Time Analysis Over Batch Quantities (ms).

## 5 Related Work

Several works have tackled the database federation problem [[Azevedo *et al*., 2020]](#ref-Azevedo_et_al_2020) [[Tan *et al*., 2017]](#ref-Tan_et_al_2017). The Garlic system [[Carey *et al*., 1995]](#ref-Carey_et_al_1995) is capable of integrating data from a broad range of data repositories. Garlic's architecture is based on repository wrappers, an object-oriented data model and query language to provide a uniform view of heterogeneous data types and data sources. The DiscoveryLink system [[Haas *et al*., 2001]](#ref-Haas_et_al_2001) allows users to query data stored in heterogeneous and physically distributed data stores by using a virtual database. DiscoveryLink system is based on the fusion of several DB2 [[Haas *et al*., 2002]](#ref-Haas_et_al_2002) and Garlic [[Carey *et al*., 1995]](#ref-Carey_et_al_1995) components.

While Garlic and DiscoveryLink use SQL, [[Langegger *et al*., 2008]](#ref-Langegger_et_al_2008) propose a middleware that employs SPARQL, shares architectural principles with Garlic's architecture, and enables integration of CSV files and Relational Databases with RDF data sources. This integration is achieved by the implementation of RDF wrappers that are very similar to the repository wrappers of Garlic and DiscoveryLink. [[Le-Phuoc *et al*., 2012]](#ref-Le-Phuoc_et_al_2012) proposal uses SPARQL and integrates time-dependent data with other RDF data sources by enriching both sensor sources and sensor data streams with semantic descriptions.

The Information Integrator tool [[Angele and Gesmann, 2006]](#ref-Angele_and_Gesmann_2006) uses ontologies and F-Logic to create an integrated view of data and mapping between data objects in distributed heterogeneous data sources, *e.g.,* databases, web services, and applications. The solution is divided in four layers: (i) Data sources; (ii) Ontologies that represent each data source; (iii) Business ontology that provide a conceptualization of business entities. (iv) views (*i.e.,* queries) of the business ontology. Elements of the layers are connected by mappings. F-Logic rules are used to specify mappings that assemble higher-value business ontologies from others.

HKPoly has similarities with these proposals, but it aims for simplification, expressiveness gain, and connecting heterogeneous data that do not have explicit links using provenance. The use of provenance to link data manipulated by independent workflows is not considered in any previous works. Using our proposal, the user specifies a query considering a single model and indicates from which workflow (or workflow execution) to get the data. Then, HKPoly discovers the paths to navigate and the data sources to reach.

Several years after those initial attempts to address the problem of heterogeneous data federation, the BigDAWG polystore system [[Gadepally *et al*., 2016]](#ref-Gadepally_et_al_2016) handles the competing notions of location transparency and semantic completeness when supporting diverse database systems working with different data models. For this purpose, the authors leveraged the concepts of islands and shims to create a middleware that provides a uniform query interface while allowing users to exploit the full capabilities of each database connected to the system. One can argue that BigDAWG still requires the implementation of so-called degenerate islands to support the full semantic power of a connected database, which is somewhat similar to the repository wrapper-based architecture of previous solutions. As novelty, this

system does not require the user to commit to one specific data model, such as Relational or RDF, as its base query language mainly comprises two general operators (CAST and SCOPE) that can be used to combine queries following multiple data models.

Although BigDAWG represents a breakthrough and has been evaluated with success in multiple medical applications, many large-scale applications continued to use federated database systems that extended the concept of repository wrappers used in Garlic and DiscoveryLink and used SQL as their primary query language. One of the most popular examples is PostgreSQL, which supports the implementation of Foreign Data Wrappers (FDWs) for external data sources access. These FDWs are mainly responsible for converting the data stored in the heterogeneous data sources into a relational representation, while the PostgreSQL engine is responsible for processing the multiple joins required to answer a query that integrates their corresponding tables. Nonetheless, this system allows the implementation of condition pushdowns in which conditions clauses of SQL queries, described after the WHERE clause, are directly translated to operations in the native query language of each data source, enabling significant gains in query performance [[Wang *et al*., 2017]](#ref-Wang_et_al_2017).

BigDAWG and PostgreSQL represent state-of-the-art solutions to the problem of database federation - BigDAWG mainly as a research prototype and PostgreSQL FDW as an industry solution. However, we consider that they can still not address the main requirements posed by modern applications since BigDAWG requires the user to understand the query languages of the multiple federated databases integrated through the system. Also, it requires how to combine them using its basic operators, while PostgreSQL requires the user to know the schema of the FDW Foreign tables to specify a SQL query to get remote data. In our view, these facts limit the level of usability these solutions can achieve that. Hence, we propose an architecture (and present its implementations) based on a hybrid conceptual model that enables users to write federated queries that are much richer and more comprehensive than the ones enabled by previous solutions.

Our solution encapsulates the remote data and the complexity of the underlying model. When accessing the data consumed and generated by the workflow execution, the user does not have to specify the paths to navigate to that data or to the remote data, since HKPoly handles this task. The user formulates a query considering a single repository (the *HKPoly Knowledge Graph*), and HKPoly uses the (provenance) data references also stored in its catalog to get the remote data.

Giacomo et al. [[De Giacomo *et al*., 2018]](#ref-De_Giacomo_et_al_2018) present an overview of the concept "Ontology-Based Data Access" (OBDA), propose a general OBDA framework, and exemplify its instantiation theoretically. An OBDA system implements three components: (i) Ontology: provides a formal high-level representation of a domain, *e.g.,* used by clients to formulate queries; (ii) Data source layer: the remote data stores; (iii) Mappings: explicitly representations that map data sources and ontologies used to translate the client operations (*e.g.,* query answering) in terms of actions on the data sources. The general approach of the framework is reasonably related to our proposal. However, it focuses on relational remote data stores. The authors point out that the encapsulation of NoSQL databases is still a challenge. Besides, they do not present the framework implementation and experimental evaluation nor handle data linkage of data stores data. Our approach is broader, encompassing heterogeneous data models and tackling the data linkage problem.

Maccioni and Torlone [[Maccioni and Torlone, 2018]](#ref-Maccioni_and_Torlone_2018) propose a data manipulation approach in polystores aka (query) augmentation which considers that objects in different data stores have a probabilistic relationship discovered by applying ML techniques. It allows query answering enrichment over a local database, using data from other databases inside a polystore system. Although we share the data linkage concept to bind related data objects in a polystore system, our approach is quite different. While [[Maccioni and Torlone, 2018]](#ref-Maccioni_and_Torlone_2018) relies on learning through user's data exploration and crawling to understand how data objects are related, we provide data linkage using provenance besides a high-level view (the GCS) for users through integrating multiple databases.

## 6 Conclusion

Provide an integrated view of heterogeneous data residing in different types of data stores is a big challenge [[Stonebraker, 2015]](#ref-Stonebraker_2015), [[Özsu and Valduriez, 2020]](#ref-Ozsu_and_Valduriez_2020). The main problem considered in this work is how to build data connections between such data and execute queries in an efficiently way.

The main contribution of this work is HKPoly, a novel polystore architecture that uses domain ontology, remote data stores' schema metadata, data mappings, and knowledge graphs to support users with a single abstract global conceptual schema to write their queries, encapsulating data heterogeneity, location, and linkage. As secondary contributions: (i) We analyzed the related components of federated database systems, including Multidatabase systems, SQL/MED specification, PostgreSQL FDW, Hyperknowledge, Polystore etc.; (ii) We presented an implementation of the architecture and we analyzed it in a real case within the O&G industry; (iii) We demonstrated how a knowledge

graph-centric approach could improve polystore queries by augmenting their semantics and facilitating the construction of queries that processes data in heterogeneous remote data stores linked by using provenance.

In our solution, a user application interacts with HKPoly through its provisioned services. HKPoly supports the requirements presented in Section [[3.1]](#ref-3_1_Requirements_and_Stakeholders), such as creating domain models, loading remote data stores' schema metadata, and processing user queries. We presented the architecture and its implementation to meet such requirements with examples to visualize and illustrate the proposal.

We evaluated the query processing feature in which the input query is at the domain abstraction level. The user does not have to know the complexities underlying the heterogeneous remote data systems. Using HKPoly, the user writes less complex queries. The evaluation in the O&G scenario shows that the proposed architecture allows query writing that is two times less complex than the query one should write to use the multidatabase system (*e.g., PostgreSQL FDW*) directly. Considering the processing time, HKPoly adds an excess of no more than 30% for transforming the high-level query (Query [[1]](#ref-Query_1)) in the *PostgreSQL FDW* query (Query [[3]](#ref-Query_3)). Although the current experimentation deals with only one use case, we got promising results on a real scenario that demonstrate applicability and utility of the proposal, It points out the use of schemas, provenance, and mappings among these data is a path to encapsulating the complexities of accessing and linking data from heterogeneous data stores.

In future work, we aim at evolving HKPoly implementation to process other query operators and workflows of other scenarios with distinct structures besides improving the query execution processing time. We also aim at handling multimedia data (*e.g.,* video, audio, and text) [[Pouyanfar *et al*., 2018]](#ref-Pouyanfar_et_al_2018) using the constructs of HK that represent this kind of data. In another direction, we can enhance the architecture by using ML techniques to augment polystore integration metadata like [[Maccioni and Torlone, 2018]](#ref-Maccioni_and_Torlone_2018).

## A Appendix with more details about the paper published at SBSI 2024

The following sections present details about the paper that was not included in the paper submission to SBSI due to lack of space.

## A.1 Use of the scientific research method

We followed the scientific research method in this work executing the following steps:

- 1. We defined the problem we are working on: querying heterogeneous data generated by business processes that are not explicitly connected.
- 2. We searched and read works to identify solutions in the literature that tackle that problem. We found such a solution was an open issue.
- 3. We defined the research question and used the Representation Theory to create our solution.
- 4. We identified the requirements and designed the data structures and components of the architecture (i.e., the deep structure).
- 5. We identified the requirements considering the literature on multi-database systems, and we identified how clients ("users") would interact with our architecture (i.e., the surface structure).
- 6. We defined the metrics we would measure considering the user and database perspective to evaluate the proposal.
- 7. We found a scenario where the problem we were tackling held.
- 8. We ran experiments considering varying data volumes to analyze the database perspective, measure the processing time, and compare the processing time against PostgreSQL FDW.
- 9. We analyzed the query complexity from the user's perspective by counting the query components to estimate the user's cognitive load. We compared the query written using the query language employed by HKPoly against the corresponding query in SQL.

## A.2 Use of Representation Theory

The Representation Theory was used to design the architecture, detail its components, and how they interact. Following the theory concepts, we presented the requirements and developed the data structures and components of the architecture (i.e., the deep structure). Afterward, we detailed how clients ("users") interact with an architecture implementation (i.e., the surface structure). We also presented an exemplary architecture implementation, which we named HKPoly. We give

details about its implementation, illustrating how it implements the proposed components and accesses the knowledge graph (i.e., physical structure).

Other IS theory could also strengthen the proposal construction, like Organizational Information Processing Theory and General Systems Theory.

## A.3 How the work was structured

In the Introduction, we present the motivation, problem, gaps in the current solution, the research question, the goal of our work, and our proposal. We explain the background required to understand our work in Section 2, i.e., before presenting the solution details. In Section 3, we present the requirements a solution should support to tackle the research problem and our proposal of architecture to support them. The architecture is presented without implementation details so that different technologies can be used for one who wants to develop a solution following our architecture proposal. Afterward, in Section 4, we present an implementation of our architecture proposal considering the state-of-the-art technologies and a scenario to illustrate its use. We also present an evaluation of the implementation to demonstrate its feasibility, considering query complexity from the user and database perspective. After presenting the details of our solution and its implementation, we believe the reader has the knowledge about it and can understand the comparison we do to existing works – presented in Section 5. Finally, we present our conclusions, highlight the contributions, and present proposals for future work in Section 6.

## A.4 Comparison against big data processing systems concerning the provenance aspect

To the best of our knowledge, most big data processing systems do not support provenance data management natively, relying on "plugins" to add such functionality. For example, work [1] adds provenance to the Apache Pig tool [2], and work [3] adds provenance to Spark [4]. However, none of these provenance plugins, alongside big data tools, deal with provenance in the form of knowledge graphs. Furthermore, as several of these plugins do not follow the W3C PROV standard, interoperability with other provenance databases is complex, which is also one of the essential aspects of our approach. As for data audit tools, they are typically considered complementary, not competitors, to provenance data management tools.

[1] Amsterdamer, Yael et al. "Putting Lipstick on Pig: Enabling Database-style Workflow Provenance." Proc. VLDB Endow. 5 (2011): 346-357.

[2] <https://pig.apache.org/>

[3] Interlandi, Matteo et al. "Adding data provenance support to Apache Spark." The VLDB journal: very large databases: a publication of the VLDB Endowment vol. 27,5 (2018): 595-615. doi:10.1007/s00778-017-0474-5

[4] <https://spark.apache.org/>

### A.5 Other papers of SBSI related to this work

Due to lack of space we could not include in the paper other references that are related to our work, such as:

- [[Villaça *et al*., 2023]](#ref-Villaca_et_al_2023) L. H. N. Villaça, S. W. M. Siqueira, and L. G. Azevedo, "EPAComp: An Architectural Model for EPA Composition," in Proceedings of the XIX Brazilian Symposium on Information Systems, in SBSI '23. New York, NY, USA: Association for Computing Machinery, Jun. 2023, pp. 61–69. doi: 10.1145/3592813.3592889.
- [[Campos *et al*., 2023]](#ref-Campos_et_al_2023) J. G. Campos, V. P. De Almeida, E. M. De Armas, G. M. H. Da Silva, E. T. Corseuil, and F. R. Gonzalez, "INSIDE: an Ontology-based Data Integration System Applied to the Oil and Gas Sector," in Proceedings of the XIX Brazilian Symposium on Information Systems, in SBSI '23. New York, NY, USA: Association for Computing Machinery, Jun. 2023, pp. 94–101. doi: 10.1145/3592813.3592893.
- [[Villaça *et al*., 2020]](#ref-Villaca_et_al_2020) L. H. N. Villaça, L. G. Azevedo, and S. W. M. Siqueira, "Microservice Architecture for Multistore Database Using Canonical Data Model," in Proceedings of the XVI Brazilian Symposium on Information Systems, in SBSI '20. New York, NY, USA: Association for Computing Machinery, Nov. 2020, pp. 1–8. doi: 10.1145/3411564.3411629.
- [[Mendes *et al*., 2019]](#ref-Mendes_et_al_2019) Y. Mendes, R. Braga, V. Ströele, and D. de Oliveira, "Polyflow: A SOA for Analyzing Workflow Heterogeneous Provenance Data in Distributed Environments," in Proceedings of the XV Brazilian Symposium on Information Systems, in SBSI '19. New York, NY, USA: Association for Computing Machinery, May 2019, pp. 1–8. doi: 10.1145/3330204.3330259.

## References

- <a id="ref-Angele_and_Gesmann_2006"></a>[Angele and Gesmann, 2006] Angele, J. and Gesmann, M. (2006). Data integration using semantic technology: a use case. In *2006 Second International Conference on Rules and Rule Markup Languages for the Semantic Web (RuleML'06)*, pages 58–66. IEEE. DOI: 10.1109/RULEML.2006.9.
- <a id="ref-Azevedo_et_al_2020"></a>[Azevedo *et al*., 2020] Azevedo, L. G., Soares, E. F. d. S., Souza, R., and Moreno, M. F. (2020). Modern federated database systems: An overview. In *22nd International Conference in Enterprise Information Systems (ICEIS)*, pages 276–283. European Association of Geoscientists & Engineers. DOI: 10.5220/0009795402760283.
- <a id="ref-Campos_et_al_2023"></a>[Campos *et al*., 2023] Campos, J. G., De Almeida, V. P., De Armas, E. M., Da Silva, G. M. H., Corseuil, E. T., and Gonzalez, F. R. (2023). INSIDE: An Ontology-based Data Integration System Applied to the Oil and Gas Sector. In *Proceedings of the XIX Brazilian Symposium on Information Systems*, SBSI '23, pages 94–101, New York, NY, USA. Association for Computing Machinery. DOI: 10.1145/3592813.3592893.
- <a id="ref-Carey_et_al_1995"></a>[Carey *et al*., 1995] Carey, M. J., Haas, L. M., Schwarz, P. M., Arya, M., Cody, W. F., Fagin, R., Flickner, M., Luniewski, A. W., Niblack, W., Petkovic, D., *et al*. (1995). Towards heterogeneous multimedia information systems: The garlic approach. In *Proceedings RIDE-DOM'95. Fifth International Workshop on Research Issues in Data Engineering-Distributed Object Management*, pages 124–131. IEEE. DOI: 10.1109/RIDE.1995.378736.
- <a id="ref-Chevitarese_et_al_2018"></a>[Chevitarese *et al*., 2018] Chevitarese, D. S., Szwarcman, D., Brazil, E. V., and Zadrozny, B. (2018). Efficient classification of seismic textures. In *2018 International Joint Conference on Neural Networks (IJCNN)*, pages 1–8. IEEE. DOI: 10.1109/IJCNN.2018.8489654.
- <a id="ref-Costa_et_al_2013"></a>[Costa *et al*., 2013] Costa, F., Silva, V., Oliveira, D., Ocaña, K., Ogasawara, E., Dias, J., and Mattoso, M. (2013). Capturing and querying workflow runtime provenance with prov: a practical approach. In *EDBT/ICDT workshops*. DOI: 10.1145/2457317.2457365.
- <a id="ref-Davidson_and_Freire_2008"></a>[Davidson and Freire, 2008] Davidson, S. B. and Freire, J. (2008). Provenance and scientific workflows: challenges and opportunities. In *Proceedings of the 2008 ACM SIGMOD international conference on Management of data*, pages 1345–1350. DOI: 10.1145/1376616.1376772.
- <a id="ref-De_Giacomo_et_al_2018"></a>[De Giacomo *et al*., 2018] De Giacomo, G., Lembo, D., Lenzerini, M., Poggi, A., and Rosati, R. (2018). Using ontologies for semantic data integration. In Flesca, S., Greco, S., Masciari, E., and Saccà, D., editors, *A Comprehensive Guide Through the Italian Database Research Over the Last 25 Years*, Studies in Big Data, pages 187–202. Springer International Publishing. DOI: 10.1007/978-3-319-61893-7\_11.
- <a id="ref-Ehrlinger_and_Woss_2016"></a>[Ehrlinger and Wöß, 2016] Ehrlinger, L. and Wöß, W. (2016). Towards a definition of knowledge graph. *SEMANTICS 2016: Posters adn Demos Track*, 48(1-4):2.
- <a id="ref-Fielding_and_Taylor_2002"></a>[Fielding and Taylor, 2002] Fielding, R. T. and Taylor, R. N. (2002). Principled design of the modern web architecture. *ACM Transactions on Internet Technology (TOIT)*, 2(2):115–150. DOI: 10.1145/514183.514185.
- <a id="ref-Gadepally_et_al_2016"></a>[Gadepally *et al*., 2016] Gadepally, V., Chen, P., Duggan, J., Elmore, A., Haynes, B., Kepner, J., Madden, S., Mattson, T., and Stonebraker, M. (2016). The bigdawg polystore system and architecture. In *2016 IEEE High Performance Extreme Computing Conference (HPEC)*, pages 1–6. IEEE. DOI: 10.1109/HPEC.2016.7761636.
- <a id="ref-Ghemawat_et_al_2003"></a>[Ghemawat *et al*., 2003] Ghemawat, S., Gobioff, H., and Leung, S.-T. (2003). The google file system. In *Proceedings of the nineteenth ACM symposium on Operating systems principles*, pages 29–43. DOI: 10.1145/945445.945450.
- <a id="ref-Gil_et_al_2018"></a>[Gil *et al*., 2018] Gil, Y., Pierce, S. A., Babaie, H., Banerjee, A., Borne, K., Bust, G., Cheatham, M., Ebert-Uphoff, I., Gomes, C., Hill, M., *et al*. (2018). Intelligent systems for geosciences: an essential research agenda. *Communications of the ACM*, 62(1):76–84. DOI: 10.1145/3192335.
- <a id="ref-Groth_and_Moreau_2020"></a>[Groth and Moreau, 2020] Groth, P. and Moreau, L. (2020). W3C PROV: an overview of the prov family of documents.
- <a id="ref-Gruber_2008"></a>[Gruber, 2008] Gruber, T. R. (2008). Ontology. In *Encyclopedia of Database Systems*. Springer-Verlag.
- <a id="ref-Guo_et_al_2005"></a>[Guo *et al*., 2005] Guo, Y., Pan, Z., and Heflin, J. (2005). LUBM: A benchmark for owl knowledge base systems. *Journal of Web Semantics*, 3(2-3):158–182. DOI: 10.1016/j.websem.2005.06.005.
- <a id="ref-Haas_et_al_2002"></a>[Haas *et al*., 2002] Haas, L. M., Lin, E. T., and Roth, M. A. (2002). Data integration through database federation. *IBM Systems Journal*, 41(4):578–596. DOI: 10.1147/sj.414.0578.
- <a id="ref-Haas_et_al_2001"></a>[Haas *et al*., 2001] Haas, L. M., Schwarz, P. M., Kodali, P., Kotlar, E., Rice, J. E., and Swope, W. C. (2001). Discoverylink: A system for integrated access to life sciences data sources. *IBM systems Journal*, 40(2):489–511. DOI: 10.1147/sj.402.0489.
- <a id="ref-Hoefler_and_Belli_2015"></a>[Hoefler and Belli, 2015] Hoefler, T. and Belli, R. (2015). Scientific benchmarking of parallel computing systems: twelve ways to tell the masses when reporting performance results. In *SC '15: Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis*, pages 1–12. DOI: 10.1145/2807591.2807644.

- <a id="ref-Ji_et_al_2021"></a>[Ji *et al*., 2021] Ji, S., Pan, S., Cambria, E., Marttinen, P., and Philip, S. Y. (2021). A survey on knowledge graphs: representation, acquisition, and applications. *IEEE Transactions on Neural Networks and Learning Systems*, 33(2):494–514. DOI: 10.1109/TNNLS.2021.3070843.
- <a id="ref-Langegger_et_al_2008"></a>[Langegger *et al*., 2008] Langegger, A., Wöß, W., and Blöchl, M. (2008). A semantic web middleware for virtual data integration on the web. In *European Semantic Web Conference*, pages 493–507. Springer. DOI: 10.1007/978-3-540- 68234-9\_37.
- <a id="ref-Le-Phuoc_et_al_2012"></a>[Le-Phuoc *et al*., 2012] Le-Phuoc, D., Nguyen-Mau, H. Q., Parreira, J. X., and Hauswirth, M. (2012). A middleware framework for scalable management of linked streams. *Journal of Web Semantics*, 16:42–51. DOI: 10.1016/j.websem.2012.06.003.
- <a id="ref-Maccioni_and_Torlone_2018"></a>[Maccioni and Torlone, 2018] Maccioni, A. and Torlone, R. (2018). Augmented access for querying and exploring a polystore. In *2018 IEEE 34th International Conference on Data Engineering (ICDE)*, pages 77–88. IEEE. DOI: 10.1109/ICDE.2018.00017.
- <a id="ref-Melton_et_al_2002"></a>[Melton *et al*., 2002] Melton, J., Michels, J. E., Josifovski, V., Kulkarni, K., and Schwarz, P. (2002). SQL/MED: a status report. *ACM SIGMOD Record*, 31(3):81–89. DOI: 10.1145/601858.601877.
- <a id="ref-Melton_et_al_2001"></a>[Melton *et al*., 2001] Melton, J., Michels, J.-E., Josifovski, V., Kulkarni, K., Schwarz, P., and Zeidenstein, K. (2001). SQL and management of external data. *ACM SIGMOD Record*, 30(1):70–77. DOI: 10.1145/373626.373709.
- <a id="ref-Mendes_et_al_2019"></a>[Mendes *et al*., 2019] Mendes, Y., Braga, R., Ströele, V., and de Oliveira, D. (2019). Polyflow: A SOA for Analyzing Workflow Heterogeneous Provenance Data in Distributed Environments. In *Proceedings of the XV Brazilian Symposium on Information Systems*, SBSI '19, pages 1–8, New York, NY, USA. Association for Computing Machinery. DOI: 10.1145/3330204.3330259.
- <a id="ref-Moreno_et_al_2017"></a>[Moreno *et al*., 2017] Moreno, M. F., Brandao, R., and Cerqueira, R. (2017). Extending hypermedia conceptual models to support hyperknowledge specifications. *International Journal of Semantic Computing*, 11(01):43–64. DOI: 10.1142/S1793351X17400037.
- <a id="ref-Moreno_et_al_2021"></a>[Moreno *et al*., 2021] Moreno, M. F., Costa, P., Costa, R., Nascimento, V., Soares, E. F., and Machado, M. (2021). A hyperknowledge approach to support dataset engineering. In *ISWC (Posters/Demos/Industry)*.
- <a id="ref-Moreno_et_al_2018"></a>[Moreno *et al*., 2018] Moreno, M. F., Santos, R., Santos, W., Brandão, R., Carrion, P., and Cerqueira, R. (2018). Handling hyperknowledge representations through an interactive visual approach. In *2018 IEEE International Conference on Information Reuse and Integration (IRI)*, pages 139–146. IEEE. DOI: 10.1109/IRI.2018.00029.
- <a id="ref-Otuonye_2021"></a>[Otuonye, 2021] Otuonye, A. I. (2021). Cloud-based enterprise resource planning for sustainable growth of smes in third world countries. *International Journal of Computer Science and Information Security (IJCSIS)*, 19(5). DOI: 10.5281/zenodo.4900658.
- <a id="ref-Ozsu_and_Valduriez_2020"></a>[Özsu and Valduriez, 2020] Özsu, M. T. and Valduriez, P. (2020). *Principles of distributed database systems*. Springer, 4th edition. DOI: 10.1007/978-3-030-26253-2.
- <a id="ref-Pouyanfar_et_al_2018"></a>[Pouyanfar *et al*., 2018] Pouyanfar, S., Yang, Y., Chen, S.-C., Shyu, M.-L., and Iyengar, S. (2018). Multimedia big data analytics: A survey. *ACM computing surveys (CSUR)*, 51(1):1–34. DOI: 10.1145/3150226.
- <a id="ref-Prud_and_Seaborne_2008"></a>[Prud and Seaborne, 2008] Prud, E. and Seaborne, A. (2008). Sparql query language for rdf. Accessed in April 12st, 2021.
- <a id="ref-Randen_et_al_2000"></a>[Randen *et al*., 2000] Randen, T., Monsen, E., Signer, C., Abrahamsen, A., Hansen, J. O., Sæter, T., and Schlaf, J. (2000). Three-dimensional texture attributes for seismic data analysis. In *SEG Technical Program Expanded Abstracts 2000*, pages 668–671. Society of Exploration Geophysicists.
- <a id="ref-Richardson_et_al_2013"></a>[Richardson *et al*., 2013] Richardson, L., Amundsen, M., and Ruby, S. (2013). *RESTful web APIs: services for a changing world*. O'Reilly Media Inc.

<a id="ref-Richardson_and_Ruby_2008"></a>[Richardson and Ruby, 2008] Richardson, L. and Ruby, S. (2008). *RESTful web services*. O'Reilly Media, Inc.

- <a id="ref-Singhal_2012"></a>[Singhal, 2012] Singhal, A. (2012). Introducing the knowledge graph: thing, not strings. https://blog.google/products/search/introducing-knowledge-graph-things-not. Accessed in June 25st, 2022.
- <a id="ref-Souza_et_al_2021a"></a>[Souza *et al*., 2021a] Souza, R., Azevedo, L. G., Lourenço, V., Soares, E., Thiago, R., Brandão, R., Civitarese, D., Vital Brazil, E., Moreno, M., Valduriez, P., Mattoso, M., Cerqueira, R., and Netto, M. A. S. (2021a). Workflow provenance in the lifecycle of scientific machine learning. *Concurrency and Computation: Practice and Experience*. DOI: 10.1002/cpe.6544.
- <a id="ref-Souza_et_al_2021b"></a>[Souza *et al*., 2021b] Souza, R., Azevedo, L. G., Lourenço, V., Soares, E., Thiago, R., Brandão, R., Civitarese, D., Vital Brazil, E., Moreno, M., Valduriez, P., Mattoso, M., Cerqueira, R., and A. S. Netto, M. (2021b). Workflow provenance in the lifecycle of scientific machine learning. *Concurrency and Computation: Practice and Experience*, e6544:1–21. DOI: 10.1109/eScience.2019.00047.

<a id="ref-Souza_et_al_2019"></a>[Souza *et al*., 2019] Souza, R., Azevedo, L. G., Thiago, R., Soares, E., Nery, M., Netto, M. A., Vital, E., Cerqueira, R., Valduriez, P., and Mattoso, M. (2019). Efficient runtime capture of multiworkflow data using provenance. In *2019 15th International Conference on eScience (eScience)*, pages 359–368. IEEE. DOI: 10.1109/eScience.2019.00047.

<a id="ref-Stonebraker_2015"></a>[Stonebraker, 2015] Stonebraker, M. (2015). The case for polystore. <https://wp.sigmod.org/?p=1629>.

- <a id="ref-Subali_and_Rochimah_2018"></a>[Subali and Rochimah, 2018] Subali, M. A. P. and Rochimah, S. (2018). A new model for measuring the complexity of sql commands. In *10th International Conference on Information Technology and Electrical Engineering (ICITEE)*, pages 1–5. DOI: 10.1109/ICITEED.2018.8534782.
- <a id="ref-Tan_et_al_2017"></a>[Tan *et al*., 2017] Tan, R., Chirkova, R., Gadepally, V., and Mattson, T. G. (2017). Enabling query processing across heterogeneous data models: A survey. In *IEEE Intl. Conf. on Big Data (Big Data)*, pages 3211–3220. IEEE. DOI: 10.1109/BigData.2017.8258302.
- <a id="ref-Vashistha_and_Jain_2016"></a>[Vashistha and Jain, 2016] Vashistha, A. and Jain, S. (2016). Measuring query complexity in sqlshare workload. <https://uwescience.github.io/sqlshare/pdfs/Jain-Vashistha.pdf>. Accessed in January 23rd, 2022.
- <a id="ref-Villaca_et_al_2020"></a>[Villaça *et al*., 2020] Villaça, L. H. N., Azevedo, L. G., and Siqueira, S. W. M. (2020). Microservice Architecture for Multistore Database Using Canonical Data Model. In *Proceedings of the XVI Brazilian Symposium on Information Systems*, SBSI '20, pages 1–8, New York, NY, USA. Association for Computing Machinery. DOI: 10.1145/3411564.3411629.
- <a id="ref-Villaca_et_al_2023"></a>[Villaça *et al*., 2023] Villaça, L. H. N., Siqueira, S. W. M., and Azevedo, L. G. (2023). EPAComp: An Architectural Model for EPA Composition. In *Proceedings of the XIX Brazilian Symposium on Information Systems*, SBSI '23, pages 61–69, New York, NY, USA. Association for Computing Machinery. DOI: 10.1145/3592813.3592889.
- <a id="ref-Wang_et_al_2017"></a>[Wang *et al*., 2017] Wang, X., Feng, R., Dong, W., Zhu, X., and Wang, W. (2017). Unified access layer with postgresql fdw for heterogeneous databases. In *IFIP International Conference on Network and Parallel Computing*, pages 131–135. Springer. DOI: 10.1007/978-3-319-68210-5\_14.
- <a id="ref-Wiederhold_1992"></a>[Wiederhold, 1992] Wiederhold, G. (1992). Mediators in the architecture of future information systems. *Computer*, 25(3):38–49. DOI: 10.1109/2.121508.
- <a id="ref-Yu_et_al_2019"></a>[Yu *et al*., 2019] Yu, T., Zhang, R., Yang, K., Yasunaga, M., Wang, D., Li, Z., Ma, J., Li, I., Yao, Q., Roman, S., Zhang, Z., and Radev, D. (2019). Spider: a large-scale human-labeled dataset for complex and cross-domain semantic parsing and text-to-sql task.
- <a id="ref-Zulkefli_et_al_2013"></a>[Zulkefli *et al*., 2013] Zulkefli, N. S. S., Rahman, N. A., Bakar, Z. A., Nordin, S., Sembok, T. M. T., and Teo, N. H. I. (2013). Evaluation of triple indices in retrieving web documents. In *International Conference on Advanced Computer Science Applications and Technologies (ACSAT)*, pages 525–529. IEEE. DOI: 10.1109/ACSAT.2013.109.