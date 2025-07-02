---
cite_key: dunbar_2022
title: Driving Digital Engineering Integration and Interoperability Through Semantic
  Integration of Models with Ontologies
authors: Daniel Dunbar, Semantic Web, Digital Engineering
year: 2022
doi: 10.1002/sys.21592
date_processed: '2025-07-02'
phase2_processed: true
original_folder: arxiv_2206.10454_Microsoft_Word_-_INCOSE_SWTMethodology_v20.docx
images_total: 13
images_kept: 13
images_removed: 0
tags:
- Data Integration
- Machine Learning
- Semantic Web
keywords:
- a novel model
- agnostic authoritative source
- agnostic model representation
- analysis tasks that
- and analysis tasks
- and interoperability across
- and interoperability benefits
- are becoming
- as well as
- becoming more
- becoming more complex
- by external users
- data integration
- defii
- digital engineering
- digital engineering framework
- engineered
- integration
- interoperability
- misd
---

# Driving Digital Engineering Integration and Interoperability Through Semantic Integration of Models with Ontologies

Daniel Dunbar1 | Thomas Hagedorn1 | Mark Blackburn1 | John Dzielski1 | Steven Hespelt1 | Benjamin Kruse2 | Dinesh Verma1 | Zhongyuan Yu1

1 Systems Engineering Research Center (SERC), Stevens Institute of Technology, Hoboken, NJ 07030, USA 2 Virginia Polytechnic Institute and State University, Blacksburg, VA 24061, USA

# Abstract

Engineered solutions are becoming more complex and multi-disciplinary in nature. This evolution requires new techniques to enhance design and analysis tasks that incorporate data integration and interoperability across various engineering tool suites spanning multiple domains at different abstraction levels. Semantic Web Technologies (SWT) offer data integration and interoperability benefits as well as other opportunities to enhance reasoning across knowledge represented in multiple disparate models. This paper introduces the Digital Engineering Framework for Integration and Interoperability (DEFII) for incorporating SWT into engineering design and analysis tasks. The framework includes three notional interfaces for interacting with ontology-aligned data. It also introduces a novel Model Interface Specification Diagram (MISD) that provides a tool-agnostic model representation enabled by SWT that exposes data stored for use by external users through standards-based interfaces. Use of the framework results in a tool-agnostic authoritative source of truth spanning the entire project, system, or mission.

# KEYWORDS

Semantic Web and Ontologies, Digital Engineering, SEE24 Model-Based Systems Engineering (MBSE), SEE26 Modeling and Simulation, SEE29 Other Systems Engineering Enablers

## Significance and Practitioner Points

This paper develops the use of ontologies and semantic web technologies for Digital Engineering by introducing the Digital Engineering Framework for Integration and Interoperability (DEFII). The DEFII framework establishes three notional interfaces for populating, interacting with, and enhancing ontology-aligned data. It provides the ability to establish tool-agnostic interfaces for data contained in a system design with the novel Model Interface Specification Diagram (MISD). The MISD uses the SysML language as a descriptive model of the analysis system and co-mingles this with the system model, giving modelers the ability to specify interfaces used for analysis in a context dependent manner. This allows for models to be defined to include data from disparate sources within the system and exposed in a way that gives external tools, from industry established design and analysis software to in-house visualization tools, access to an established, authoritative source of truth. This approach to interoperability allows practitioners to continue using tools that suit their needs and preferences while taking advantage of enhanced interoperability between disciplines and creating a knowledge base that can be expanded on in the future to allow for further integration of artificial and augmented intelligence applications.

# 1 | INTRODUCTION

Increasing complexity in engineered projects requires a high level of collaboration across disciplines. To maintain high standards of quality and reasonable time frames, computer assisted collaboration is increasingly necessary. Data integration that enables cross-domain reasoning and collaboration at the model level is key to enabling and enhancing computer assisted engineering and design across multiple abstraction levels, domains, and disciplines.

Digital Engineering (DE) is an umbrella domain that seeks to integrate the Model Based Systems Engineering (MBSE) and domain specific Model Based Engineering (MBE) domains. Defense Acquisition University defines DE as "an integrated digital approach that uses authoritative sources of systems' data and models as a continuum across disciplines to support lifecycle activities from concept

through disposal."1 In order to do this, it relies heavily on the concepts of Authoritative Source of Truth (AST) and Digital Thread (DT). The AST serves as a central data registry where all tools associated with the project must go to access system data. Thus, multiple tools can access the same datapoint and have certainty that they are working from the same value. Researchers have used various structures to form the AST, including system models2 , databases3 , and various graph data structures4–7 . The DT digitally connects different models used in system design and analysis across domain and software boundaries.8 This requires a robust data integration plan to enable the model level connection that is needed.

Integration of various models is traditionally done through tool-to-tool integration. Custom interfaces designed to connect tool A to tool B have been used for years to accommodate data integration needs in cross domain analysis. However, tool-to-tool integration is brittle in nature4 , and the number of tool-to-tool integrations needed to fully connect the design and analysis system grows exponentially as tools are added9 . In other words, tool-to-tool integration is prone to error, difficult to maintain, and hard to scale.

A database approach, which allows for a central hub of data that is accessed by multiple tools, is a better fit as a DE AST. Particularly, a graph data structure that captures system specific data and connects it to domain knowledge presents an interesting foundation for a potential solution. Graph data structures capture relationships between nodes and can take advantage of both relational and graph based algorithms.10

Computer based ontologies and associated technologies collectively known as Semantic Web Technologies (SWT) provide a technological base to build out a graph data structure as an AST in the DE context. SWT comprises a suite of technologies to tag graph data with semantically meaningful labels, to store and retrieve that data, and to automatically reason upon it based upon the logical framework underpinning the tags. Ontologies provide the markup schema used to tag the graph and a logical formalization in the form of a taxonomy of terms, relations, and machine-readable logical expressions using them. Data repositories called triple stores provide storage and endpoints for semantic queries, which are used to retrieve and interact with graph data. Automated reasoners afford the ability to deduce new relations within tagged data based upon logical inferencing, and to enhance query results with that inferred information.

While graph data structures have been used in DE and systems engineering domains with positive results4–7 , to date there is not a robust framework for guiding engineers to integrate SWT into a DE environment.

This paper presents the Digital Engineering Framework for Integration and Interoperability (DEFII), an ontologybased framework for solving integration and interoperability concerns inherent to the DE domain space. It uses a graph data structure as the DE AST and establishes three notional interfaces to allow interaction with the ontology aligned data: the Direct Interface, the Mapping Interface, and the Specified Model Interface. Additionally, the paper introduces a novel Model Interface Specification Diagram (MISD) to specify ontologically relevant interfaces without deep understanding of the ontologies being used.

A successful framework for integrating SWT into DE must move beyond theory and enable practice that realizes these benefits. For a framework to reach that threshold, this paper holds that it must:

- 1. Provide clear avenues for mapping data from engineering design and analysis models to an ontology-aligned data store
- 2. Allow access to contained data in a flexible, toolagnostic manner
- 3. Allow for the transformation and enhancement of data using various semantic technologies

These three success criteria address current data integration needs in DE and prepare for future capability by taking advantage of an ontology-based AST that provides a holistic view of the systems under design. This paper shows the DEFII framework satisfies all three criteria.

Section 2 looks at related work and identifies a gap the DEFII framework fills in existing literature. Section 3 details the DEFII framework and notional interfaces related to it. It also introduces a case study from the Information Technology (IT) cyber security domain that uses DEFII to produce results that can be analyzed. Section 4 instantiates the notional interfaces to address a specific use case and describes the results of usage of the DEFII framework. Section 5 analyzes the results to validate DEFII against the success criteria defined above, discusses limitations of the research and opportunities to extend the research, and interprets the results for the larger DE context. Section 6 provides a conclusion to the paper.

# 2 | RELATED WORK

Ontologies have long been proposed as a medium for knowledge representation in engineering. Theoretical benefits include the potential for reuse, automated inferencing, and knowledge sharing11–13. . These theoretical benefits have led to research on how to build solutions that make use of the SWT to enhance engineering efforts. A first step in this research is the use of SWT directly.

A significant body of past research has focused on demonstrating engineering capabilities that are enabled by SWT. Most prior work focuses narrowly on either pure ontology definition for the engineering domain or the capabilities afforded by ontology aligned data. Coelho et al. use direct invocation of the SWT stack in their proposal of the "Data-Ontology-Rule footing" as a mechanism for building ontology integration into the design and analysis workflow. Mechanisms for pulling system data into ontologies beyond direct manipulation of the ontological data using semantic tools are not discussed14. Eddy et al. describe a framework for design alternative development based on the use of modular ontologies of the engineering design domain and various reasoning capabilities15. Similarly, Hagedorn et al. use SWT to enable design and ideation in the Additive Manufacturing domain16 based upon semantic querying and rule-based inferences. Daun et al. use ontologies to describe contexts in concurrent engineering17. While these works demonstrate possible benefits of SWT in engineering context, they lack defined techniques for populating ontology aligned-data instances and interacting with engineering models or tools. Thus the benefits demonstrated in these and similar works remain largely hypothetical <sup>6</sup> .

Several works have attempted to bridge this gap between tools and SWT using a process of data mapping. Termed "data ingestion" by commercial tools18, mapping is a process by which data from outside the SWT stack is parsed into SWT formats and aligned to ontology-tagged graph patterns. El Kadiri and Kiritsis discuss mapping for ontology use in the Product Lifecycle Management (PLM) domain19. Several other publications discuss mapping both specifically and generically in reference to systems engineering domain10,18,20–23. Mapping tool and model information to ontology-aligned data allows the use of the SWT in more realistic engineering workflows using real or realistic data. Examples of this include JPL's use in CEASAR to establish logical consistency and build reports through the use of custom queries24, Lu et al.'s use of custom querying21, DL reasoning by Petnga et al.23, and data exploration by Hagedorn et al.18.

Multiple frameworks have been introduced that make use of direct mappings from tools to enable SWT applications in engineering contexts. NASA's Jet Propulsion Lab (JPL) has introduced the Computer Aided Engineering for Spacecraft Architectures Tool Suite (CAESAR) as a type of framework to aid in MBSE. CAESAR uses the Ontological Modeling Language (OML) to capture models in a controlled vocabulary and a number of tool adapters to incorporate different external design and analysis tools into the ontologybased approach24. Moser has proposed the Engineering Knowledge Base (EKB) as a framework for integrating SWT in multidisciplinary engineering environments9 . This framework focuses on the use of custom tool mappings to interface with the underlying graph data structure9,25. Moser contrasts this approach with a common repository approach. In a common repository approach, schema must be predetermined and are tool specific, which makes them more fragile and harder to maintain. In the EKB approach, tool data is mapped to common engineering concepts, which enables a more robust representation of the data and semiautomatic transformation of data from one tool to another9 . Both the CAESAR and EKB frameworks use an ontologybased AST and enable aspects of the DT. Mapping is often used alongside descriptive models such as those defined using the Systems Modeling Language (SysML). NASA's Jet Propulsion Lab (JPL)5,26, Bone et al.7 , and Blackburn et al.27 all populate SWT tools with ontologically aligned information using SysML that use stereotypes to inject ontological tags. In all these cases, stereotypes serve to guide a tool-specific mapping process.

Across all of these efforts, mapping provides a mechanism for connecting engineering tools with ontologyaligned data and the broader SWT stack. However, it does so through a rigid, often tool-specific, connection point. As a result, it may be difficult or labor intensive to add new tools to a workflow. It also limits accessibility the data to those with knowledge of how to use SWT tools. Broader access, through a more flexible input and output mechanism would enable more design and analysis functionality. SysML v2 begins to provide more flexible access to system data through the use of a standards based Application Programming Interface (API)28,29. However, SysML v2 uses this flexible input/output mechanism to access the system model, not an ontology-aligned representation of the information stored in the system model.

DTs require the interaction of multiple tools external to an AST. Flexibility in how tools can interact with data in the AST enables more opportunity for this interaction and increases the usability of a DE solution. While the SWT stack and mapping provide capability for a DT and are being used in current engineering research, there is space for additional types of interfaces to enable more diverse access to the AST.

# 3 | METHODS

The DEFII framework structures usage of SWT in the DE context. This section will define the framework and introduce a case study from the Information Technology (IT) domain to validate the usability of the framework in a domain setting.

# 3.1 | Framework Description

The DEFII framework (Figure 1) assigns the role of the AST to ontologies and data aligned to those ontologies. This forms the foundation of the framework. It then uses automated reasoning capabilities of SWT to enrich the ontology-aligned data through the use of rules and relationships defined in the ontologies. Finally, it provides clear categories of interfaces that users can use to access, modify, and populate the AST.

**Figure 1**The DEFII Framework for use of SWT in DE contexts

![](_page_2_Figure_10.jpeg)
<!-- Image Description: The image is a layered architecture diagram illustrating a system's data access and interaction methods. It shows multiple layers: a bottom layer of "Ontology Aligned Data," a middleware layer using DL reasoners and SWRL rules, and a top layer with various interfaces (direct, REST API, SPARQL queries). The diagram showcases how different system models (MISD) and expansion capabilities are integrated into the architecture through a SysML authoring tool and defined interfaces. The purpose is to visually represent the system's modular design and data access pathways. -->

# 3.1.1 | Ontology Aligned Data

Ontology-aligned data is the foundation of the framework. It enables the use of a graph data structure to act as the AST. Using a triple store as a graph repository, the ontological knowledge base uses controlled vocabulary defined by ontology class data to characterize system data as instances of assigned classes. Representation of system data as ontology-aligned data in a graph data structure has four primary benefits:

1. Interoperability

Gruber argues for the use of ontologies for both reusability and interoperability between domains11,12. The framework specifies the use of a top-level ontology and shared development principles to drive co-development terminology across disparate knowledge domains. A toplevel ontology provides a high-level philosophical basis and development guidance that is shared by all ontologies within an ecosystem aligned to it. Subsequent, domain specific ontologies simply extend this high-level understanding to ever more specific knowledge domains.

2. Tool Agnostic

Because ontologies model domains of knowledge, rather than specific tools or datasets, data aligned to ontologies is tool agnostic. The use of a standards-based open formats, such as the Resource Description Framework (RDF) syntax and the Web Ontology Language (OWL) enhances this tool agnostic representation of system data. This makes the data portable and offers greater flexibility and freedom with tool access to the data.

3. Domain Agnostic

Not only does the graph data structure promote tool agnostic access to data, it also promotes a domain agnostic approach. As noted by Mordecai et al.10, the use of graph data structures extracts the system representation from the MBSE toolset and presents it in more general terms. As DE serves as an umbrella domain to connect many different domains30, representation of data in a way that separates it from any specific domain, including the systems engineering domain, offers more equitable access to it.

4. Access to SWT stack

The SWT stack offers many functions based on the formal nature of ontology-aligned data and the triple format in which data is stored. Access to powerful querying, reasoning, and validation is enabled by the foundational decision of the framework to use ontology-aligned data and will be detailed in subsequent sections of the paper.

# 3.1.2 | Reasoning Layer

The reasoning layer uses some of the automated reasoning capabilities included in the SWT stack. Since ontologies make use of axioms and relationships to characterize classes within them, these axioms can be used to further enrich the data beyond what has been explicitly defined. For example, if a child's mother and the mother's mother are defined explicitly in a graph repository and definitions and relations are encoded in the ontology (i.e., a grandmother is a role filled by a parent's mother for that parent's child), then the relationship between the child and the grandmother can be made through automated reasoning, bypassing the need to explicitly declare all knowledge in the graph repository. In characterizing engineering knowledge applied to a system, the ability to infer knowledge based on a heterogenous data store opens the possibility of discovering insights to how design elements originating in separate tools relate to each other. This capability uses mathematical logic, specifically

Description Logics (DL), to enable DL reasoners as part of the SWT stack to automatically enrich the data without any extra involvement by external users.

# 3.1.3 | Notional Interfaces

The characterization of the system data in the AST is established, updated, viewed, and analyzed through interfaces to external sources. DEFII specifies three types of notional interfaces: the Direct Interface, the Mapping Interface, and the Specified Model Interface. The Specified Model Interface is further refined by the introduction of the Model Interface Specification Diagram (MISD). With these three types of interfaces and the MISD, the framework provides a structured approach to access and manipulation of ontology-aligned data.

The Direct Interface enables the use of the SWT stack directly on stored data. Data stored as ontology-aligned data enables the use of SWT tools to extract specific knowledge, apply constraint checking, and more using a growing set of tools in the SWT suite. This interface acknowledges this reality and codifies it within the framework's view of interfaces. While implementation of subsequent interface types will inevitably use SWT tools to enable them, this interface type is distinguished by its direct invocation of those tools.

The Mapping Interface transforms model data into ontology-aligned data by accessing data stored in a model or tool and mapping it to ontological classes in the controlled vocabulary. Beginning with external model data and establishing a connection to an ontology limits this interface type to a tool or model specific implementation per instance of the interface connected. Primarily, this interface addresses MBSE models and maps system models to ontology-aligned data. System models are broad in scope and capture design criteria for multiple domains. Thus, tagging data with relevant ontological terms and mapping that data to an ontology-aligned graph provides flexibility for the system model to be built to describe the relevant domains instead of fitting it into predetermined structure. It also means that the interface is domain agnostic: the ontological tags are simply changed or expanded to handle new domains.

This interface is the most restrictive interface as it is responsible for accessing data stored in other tools, making most instances tool-specific implementations. However, this form of interface still provides reductions in development efforts and maintains the benefits of ontologies over the use of direct tool-to-tool data integrations (Figure 2). The use of a mapping to an AST provides a limiting principle on the development efforts related to interfaces. Instead of a growing stable of tool-to-tool integrations, which will multiply with each tool added, an AST limits development to a single new interface per tool added to the workflow9 . In addition, if the AST uses a triple store and ontology-aligned data, these add functionality to the AST by giving access to the reasoning capacities of the SWT and the other two types of notional interfaces.
**Figure 2**Mapping to an AST reduces interface development work

![](_page_4_Figure_2.jpeg)
<!-- Image Description: This image compares two software integration approaches. The left side shows a "new tool" integrating with multiple "existing tools" via a central "Authoritative Source of Truth (AST)," a tool-agnostic triple store. The right side illustrates direct tool-to-tool integration. The diagrams illustrate that using a mapping interface (AST) reduces the number of interfaces needed compared to direct integration, thus reducing development effort. -->

The Specified Model interface characterizes models of interest within the broader system model. A model of interest is defined here as an aggregation of parameters present in the system model that is beneficial for external tools and application purposes. In contrast with the Mapping Interface, the Specified Model Interface begins with ontology-aligned data and exposes this data towards tools. This reverse of direction enables the interface to be tool agnostic. Even if an instantiation of the Specified Model Interface is designed with a particular tool in mind, the direction of the interface creation enables other tools to access the same information via the same interface. This interface primarily addresses MBE models and exposes data in a structured way to be analyzed, visualized, etc.

# 3.1.4 | Model Interface Specification Diagram

The Model Interface Specification Diagram (MISD) is a reusable, graphical specification for the Specified Model Interface. The MISD makes use of SysML parametric diagrams to describe a model of interest and define connections to parameters established elsewhere in the system model (Figure 3). The MISD acts as a graphical specification of data that will be provided to a given tool when requested. This extends Cilli's concept of the Assessment Flow Diagram31.

Once mapped into the ontological layer, this specification can be concretized in a variety of formats, such as the Comma Separated Value (CSV) format. The MISD allows users unfamiliar with semantic technologies or the underlying ontologies used by the framework to nevertheless request and update ontology-aligned data captured by the system model. It provides the means for tool-agnostic Specified Model Interfaces to be created and accessed by broader user group and toolset.
**Figure 3**Abstract Model Interface Specification Diagram (MISD)

![](_page_4_Figure_8.jpeg)
<!-- Image Description: The image is a diagram depicting an "Abstract MISD" (Multiple Instruction Single Data) model. It shows a central "Model of Interest" component receiving "parameter 1" and "parameter n" inputs from external sources. The diagram illustrates the flow of parameters into the model, clarifying the system's architecture and data handling within the context of the paper's discussion on MISD models. The use of boxes and lines represents the components and data paths, respectively. -->

## 3.2 | Framework Case Study

An Information Technology (IT) example is provided as a case study18,27. While the DEFII framework is domain agnostic, the IT case study provides a simple use case that is intuitive to understand as a test of the framework and a demonstration of its functionality. The case study examines a simple cyber system that has various cyber elements such as a laptop and software. The system is represented by a SysML Block Definition Diagram (Figure 4).

![](_page_4_Figure_11.jpeg)
<!-- Image Description: Figure 4 is a Binary Decision Diagram (BDD) illustrating a cyber system's hierarchical architecture. The BDD visually represents the system's structure, likely showing its various components and their relationships in a layered or nested format. Its purpose is to provide a clear, concise, and structured visualization of the cyber system's organization for the reader. -->

![](_page_4_Figure_12.jpeg)
<!-- Image Description: The image displays a hierarchical model of a cyber system's vulnerability analysis. A top-level box, "Cyber Vulnerability Analysis," branches down to "Cyber System," which further subdivides into components: Laptop, Software (including Internet Explorer with version and patch details), Magnetometer, and Ethernet Cord. Relationships are denoted using "subsets sub." The model likely illustrates a system's structure for vulnerability assessment using the CVSS (Common Vulnerability Scoring System) model. -->

The use case involving this case study is the identification of a seeded cyber vulnerability in the Internet Explorer web browser (contrived for demonstration) and the generation of a system wide Common Vulnerability Scoring System (CVSS)32 score. This requires the use of both an MBSE model (system model in SysML) and an MBE model (MATLAB analysis model). In addition, a visualization of the results is included to demonstrate that a single toolagnostic interface can service multiple tools. The DEFII Framework is displayed in the context of the case study (Figure 5). The gray portions of the figure will be realized as results are generated in Section 4.
**Figure 5**DEFII Framework applied to cyber case study

![](_page_5_Figure_1.jpeg)
<!-- Image Description: The image is a system architecture diagram showing the components and data flow of a vulnerability analysis system. It depicts data moving from a CATIA Teamwork Cloud via a mapping interface into an Ontotext GraphDB triple store using SPARQL queries and RDFS reasoning. A REST API provides access for MATLAB analysis and dashboard visualization, incorporating CVSS MISD parameters. The system utilizes a cyber ontology aligned with CCO's BFO. -->

To account for the cyber vulnerability portion of the use case, each cyber element also includes the value properties listed in Table I related to a CVSS score. These attributes are used to apply a CVSS score to a specific cyber vulnerability. For example, the scope value can be "Unchanged" or "Changed," and the CVSS scoring process would take that value into account when calculating the overall CVSS score. They are left off Figure 4 for readability.
**Table I**List of CVSS related value properties assigned to each block

| ac (Attack Complexity)     | av (Attack Vector)    |
|----------------------------|-----------------------|
| a (Availability)           | vs (CVSS Vector)      |
| score (CVSS Overall Score) | i (Integrity)         |
| s (Scope)                  | c (Confidentiality)   |
| pr (Privileges Required)   | ui (User Interaction) |

Reflecting the collaborative and reusable nature of ontologies, the case study is based on existing, publicly available ontologies. The Basic Formal Ontology (BFO)33 was used as a top-level ontology. BFO provides a small core of rigorously vetted terms, philosophical principles, and strict development guidelines which may be used to develop domain ontologies. This work also used the Common Core ontologies (CCO)34, which extend BFO to cover common things found in many domains such as information. A Cybersecurity Ontology extending the CCO lexicon was used to describe the Cyber domain. This ecosystem was then extended to describe the CVSS scoring system, as well as to introduce configuration management type notions such as version and patch numbers that are used to identify the vulnerability seeded into the case study.

Elements in the BDD (Figure 4) are stereotyped with ontological classes according to the ontologies being used in the DEFII framework. For example, the Laptop block has the <<LaptopComputer>> stereotype. These custom stereotypes

will be used to map the system model to ontology-aligned data.

The cyber system is instantiated within the system model. This allows the stakeholder to observe a specific instance of a system definition and for observation of both structure (an instantiation captures structure inherited from the definition) and specific values (e.g., Internet Explorer Version 1 and Version 2). A partial instantiation table is shown in Table II.

|                   | ac : Attack | a :          | av : Attack |
|-------------------|-------------|--------------|-------------|
| Name              | Complexity  | Availability | Vector      |
| centOS            | High        | Low          | Physical    |
| cyber System      | High        | Low          | Physical    |
| ethernet Cord     | High        | Low          | Physical    |
| Internet Explorer | Low         | Low          | Network     |
**Table II**Partial Instance Table of Instantiated Model

Several tools are used to instantiate the DEFII framework for the case study. Ontotext's GraphDB triple store35 is used as the graph repository. Dassault Systemes' SysML Authoring tool suite, including CATIA Teamwork Cloud36 is used to create SysML models and provides remote, APIbased access to the SysML elements. Protégé37 is used for editing ontologies. Python is used for interacting with the various tools and instantiating the interfaces. The OWLREADY238 Python library is used for programmatic manipulation of graph data aligned to ontologies.

### 4 | RESULTS

To produce results, a DT is established (Figure 6) that uses all the interfaces to realize the defined use case. The first step is a mapping of the SysML system model from a tool specific implementation to an ontology aligned, tool-agnostic representation stored in a triple store. Second, the Direct Interface is used to directly query the graph repository, via a SPARQL query, to discover a specific vulnerability. After the vulnerability is discovered, the third step is a MATLAB analysis program pulling data specified by an MISD from the triple store via a REST API GET call. Fourth, after the analysis is complete, the triple store is updated with new values produced by the analysis. Fifth, the same REST API endpoint that was used by the MATLAB analysis program is reused by a web application dashboard to display the results of the analysis. In this dataflow, all major elements of the framework are instantiated, and the reusability of the notional Specified Model Interface is highlighted.

A functional analysis of the three success criteria identified in the introduction must be performed to determine in the DEFII framework fulfills its purpose.
**Figure 6**Digital Thread Across Different Interfaces

![](_page_6_Figure_1.jpeg)
<!-- Image Description: The image depicts a data integration architecture. A central GraphDB triple store (ontology-aligned data) connects various tools via a REST API. CATIA Teamwork Cloud (SysML model) and MATLAB (analysis model) use a mapping interface to interact with the store (1, 3, 4). A dashboard visualizes the data (5), while a SPARQL query performs vulnerability identification directly (2). The diagram illustrates the data flow and interfaces between different software components within a system. -->

#### 4.1 | Mapping Interface Instantiation

The use of a SysML System Model requires a mapping interface. Specifically, it requires a tools specific interface for the CATIA Cameo Teamwork Cloud (TWC) SysML authoring tool. The mapping makes use of a combination of SysML language elements, like the custom stereotype, and TWC specific features, like the Application Programming Interface (API) to TWC data that results in a JSON representation of the data that can be analyzed and mapped to ontology-aligned data. Mapping begins by transforming this API data to a representation in triples. SPARQL, a query language for semantic languages, can then be used to extract data relevant to the ontologies. Below is an example of a mapping rule executed in the mapping process. The example is presented in pseudocode (Figure 7) followed by a general explanation.

```text
Figure 7 Pseudocode describing the implementation of a mapping rule
```text

First a SPARQL query is run (Figure 8). This simple SPARQL query extracts classes from the graph repository that have been stereotyped by various names. The results are then checked against known classes in the ontologies loaded. If the variable '?name' is the name of an ontological class, then the variable '?class' is mapped to the ontology aligned data. An entity and spec are created and related to each other to adhere to the way that the CCO describes information. Finally, a link back to the original, unmapped graph representation of the tool data is created to enable pushing updates back to the mapped tool. If the variable '?name' does not correspond to an ontological class, the result is discarded, and the mapping program moves to the next result. More

details about this mapping process can be found in Bone et al.7

![](_page_6_Figure_8.jpeg)
<!-- Image Description: Figure 8 presents a SPARQL query designed to identify stereotyped classes within a dataset. It's a text-based query, not a visual representation like a chart or graph. The purpose is to illustrate the specific query used in the research methodology for discovering and analyzing these classes. -->

![](_page_6_Figure_9.jpeg)
<!-- Image Description: The image displays a data query (SELECT statement) and its corresponding graph representation. The query selects `?class` and `?name` variables where `?class` has a relationship with `?name` via `SysM:_appliedStereotypeIds` and `test:name`. The graph visually depicts this relationship, showing nodes for `?class`, an intermediate node, and `?name`, connected by labeled edges representing the query's conditions. The graph clarifies the data flow implied in the query. -->

This example mapping rule is implemented as part of a collection of mapping rules that address other aspects of the SysML model representation as presented by the Teamwork Cloud tool to include other facets of the language such as instances and enumerations. Together, these rules provide a process for transferring a SysML model representation to a tool-agnostic, ontology-aligned graph data structure. While this specific result relates to the cyber case study described in the Methods section, the mapping rules discussed are more general and can be applied to any SysML model stored in a TWC instance. Thus, the mapping interface is tool-specific, but it can be used across models and domains.

### 4.2 | Direct Interface

Accessing the triple store via the Direct Interface allows for use of the SWT stack. Step 2 in the DT (Figure 6) uses a SPARQL query to directly query the triple store in search of a specific vulnerability. Seen in Figure 9, SPARQL is selective enough to isolate a specific vulnerability tied to a particular version and patch number of the Internet Explorer web browser (a contrived vulnerability created for demonstration purposes).
**Figure 9**Top: SPARQL Query; Bottom: Graph View

![](_page_7_Figure_3.jpeg)
<!-- Image Description: The image displays a directed graph representing an RDF data model. Nodes depict concepts (e.g., "browser," "VersionNumber") and relationships (e.g., "rdf:type," "Comm:designated_by"). Arrows indicate relationships between nodes. The graph models information about Internet Explorer's version and patch numbers, with numbered nodes likely representing unique identifiers within the data model. A SPARQL filter query is shown above, suggesting the graph's use in querying this data. The graph visually explains the data structure and its use in a specific query within the paper. -->

# 4.3 | Specified Model Interface with MISD

Steps 3 through 5 of the DT (Figure 6) require the use of the Specified Model Interface. In order to instantiate the interface, an MISD is created to define the CVSS model for a system level vulnerability score (Figure 10). The MISD connects parameters from a variety of levels of the architecture to a single analysis model. It also shows multiple like parameters coming into the same port. The multiple levels of hierarchy show the flexibility of the interface specification – as long as the parameter is specified within the system model, it can be attached to a specified interface for exposure. Multiple parameters sharing a single port in the analysis model collects the parameters into an array that can be analyzed as a block of data.

This interface definition is mapped to ontology-aligned data via the same mapping process described above and delineated by the <<Model>> stereotype.

# Figure 10 CVSS Model Interface Specification Diagram (MISD)

![](_page_7_Figure_8.jpeg)
<!-- Image Description: This image displays a hierarchical model of a cyber system using a CVSS (Common Vulnerability Scoring System) model. The diagram shows nested boxes representing system components (Magnetometer, Laptop, CentOS, Internet Explorer, Ethernet Cord, Software) and their attributes (ac, c, pr, ui, av, a, s, i). Each attribute is defined as a string with a specified range. The top-level box represents the overall system with inherited attributes and scores (vs, score). The purpose is to visually represent the system's structure and vulnerability attributes for security analysis. -->

Once it has be mapped to ontology-aligned data, the instantiated data associated with the definition can be transformed to a REpresentational State Transfer (REST) API. REST APIs allow stateless interaction with web services via HTTP requests. The DEFII REST API allows the Python implementation of the specified model interface to be exercised remotely via POST, GET, and PUT requests to instantiate, retrieve, and modify data in the triple store (Figure 11).
**Figure 11**Partial Results of GET Request of MISD

| "individual": "http://testontology.org/cyber_mapped/48165ac. |
|--------------------------------------------------------------|
| a205bac33c1d_entity",                                        |
| "CVSS Model": {                                              |
| "score": $1.6$ .                                             |
| "s_inherited": [                                             |
| "Changed",                                                   |
| "Unchanged",                                                 |
| "Unchanged",                                                 |
| "Unchanged",                                                 |
| "Unchanged",                                                 |
| "Unchanged"                                                  |
| ŀ,                                                           |
| "pr_inherited": [                                            |
| $H \sqcup \exists \neg \neg \neg H$                          |

For the CVSS model defined, a simple MATLAB analysis model was deployed to determine a system wide CVSS score along with a text-based vector for characterizing the CVSS score. Using MATLAB's*webread*and*webwrite* functions to access the REST API endpoint, data specified by the MISD is read into the analysis program, transformed by the analysis, and written back to the triple store. In this process, the data is kept in a semantically aware position – all data using the Specified Model Interface is specified and modified in terms of its place in the ontology-aligned data.

The results can be visualized using the same REST API endpoint accessed by the MATLAB analysis program. Since the interface is tool-agnostic and specified for a defined model, a simple dashboard can be created to pull the results data from the same interface. Figure 12 shows a resulting CVSS score and vector after the MATLAB analysis model has been run.

![](_page_8_Figure_2.jpeg)
<!-- Image Description: Figure 12 displays a screenshot of a "Cyber Demo Dashboard" showing CVSS analysis results. The dashboard presents an "Overall Cyber System Vulnerability Score (CVSS)" and a section labeled "Retrieve Information," which details how to run a GET request and output JSON data. The image illustrates the interface used to access and present the vulnerability scoring system's results. -->

# 4.4 | Additional SWT Transformation

Additional SWT Transformation is seen in the use of automated reasoning supported by the triple store used. In the case study, Ontotext's GraphDB triple store was used. The chosen reasoning profile for this paper was RDFS-Plus, which includes sub-classes and property inferences plus transitivity. This profile was chosen because it allows for relatively fast query answering, and this application does not require more sophisticated OWL semantics. Figure 13 shows that 36,674 of the total statements in the mapped repository were inferred compared to the 19,720 statements that were explicitly provided (an expansion ratio of 2.86). This result demonstrates that additional information was inferable through automated reasoning on the ontology definitions and provided instance data.

## Figure 13 GraphDB display of explicit and inferred statements

![](_page_8_Figure_6.jpeg)
<!-- Image Description: The image displays a table summarizing data from a local database labeled "cyber_mapped." It shows a total of 56,394 statements, categorized into 19,720 explicit and 36,674 inferred statements. An expansion ratio of 2.86 is also provided, likely indicating the relationship between explicit and inferred statements. The icon suggests the data is stored in a database. The purpose is to present key statistics about the dataset used in the study. -->

### 5 | DISCUSSION AND FUTURE WORK

#### 5.1 | Analysis of Results

The introduction identifies three functional attributes of a framework to be used as success criteria for its operation in the DE context:

- 1. Provide clear avenues for mapping data from engineering design and analysis models to an ontology-aligned data store
- 2. Allow access to contained data in a flexible, toolagnostic manner
- 3. Allow for the transformation and enhancement of data using various semantic technologies.

All three criteria are met by the DEFII framework presented in the paper.

Success Criteria 1 is fulfilled by the mapping interface. It provides clear guidance for what function the interface performs for the framework, and an example of its usage mapping a SysML model from an authoring tool to ontologyaligned data provides results that demonstrate the interface and give details to aid in reproduction of the interface.

Success Criteria 2 is fulfilled by the Specified Model Interface and the associated MISD. Use of the MISD allowed creation of a REST API endpoint that exposed ontologyaligned data to external tools. The results show the toolagnostic nature of the data by accessing the same interface with two different tools, MATLAB and a web application dashboard. The MISD can also be created by system modelers that are unfamiliar with the underlying ontologies used by the DEFII framework. This enhances the functionality of the framework by expanding its usability beyond those adept in semantic technologies.

Success Criteria 3 is fulfilled by both the Direct Interface and the reasoning layer of the DEFII framework. The results show a SPARQL query accessing the ontology-aligned data to identify a vulnerability embedded in the data. The reasoning layer is demonstrated through the additional inferred statements based on the reasoning profile setup in the triple store.

The DEFII framework's use of the MISD and Specified Model Interface also promote tool interoperability. Tool interoperability denotes the ability to use multiple tools to perform similar functionality on a single model. In the cyber case study, the CVSS analysis was performed by a MATLAB program. However, a program written in Java, Python, or a myriad of other tools and programming languages that can call REST services could perform the same analysis using the same interface. Further, another Specified Model Interface could be instantiated to provide the model specified by the MISD in a format other than the REST API endpoint. For example, it may be more beneficial to create and ingest CSV files for a particular model. As many different tools can read csv files, the potential for creating tool-interoperable data increases. The more complicated the analysis, the harder tool interoperability may become on the tool side, but the DEFII framework establishes a standard way of specifying and exposing data in a tool agnostic format that promotes tool interoperability.

# 5.2 | Limitations and Future Research Opportunities

The MISD presented in the cyber case study includes many like elements manually connected to a cyber analysis model. While the diversity of elements and parameters (multiple levels of hierarchy, single and multiple inputs to various ports) demonstrates key features of the MISD and thus is useful for presenting the overall notional interface, the actual analysis being performed could be characterized as a pattern to greatly simplify the specific instantiation of the interface. A roll-up pattern like the one presented (also consider weight18 and cost) is recursive in nature, where like elements at one level of architecture are "rolled up" to their parent element, which then serves as an element of analysis for the next level of architecture. Future research needs to determine how to account for these types of analysis in the interface specification.

The Specified Model Interface is the preferred interface in the presented framework for most uses in a DE environment. It enables tool-agnostic implementation of a DT across multiple toolsets and consolidates interface development in a way that preserves the semantic underpinnings of the approach. It may be extended to provide tool specific data through the use of middleware that transforms the tool-agnostic representation of an interface (i.e., JSON from a REST API endpoint) to a tool specific format of an external tool that does not have web services capability. This implementation could have two benefits: developers don't need to understand SWT to create the middleware whereas they would need that background information to create a custom mapping interface, and (2) the interface could still be used by other tools. For example, an analysis program may make use of middleware to transform standard JSON to a tool specific representation, but a dashboard could access that same interface to do reporting and visualization of the data the analysis program is using/producing. If this is consistently used in practice, the Mapping Interface may be limited to the unique semantic mapping needs of a system model.

The Direct Interface enables a wide range of applications and further exploration of the SWT stack. Results in this paper show a simple SPARQL query to demonstrate access

to the SWT, but more complex applications of the SWT could provide deeper functionality to the notional interface. For example, the use of the W3C recommended Shapes Constraint Language (SHACL)39 could allow for certain verification and validation tasks to occur on the semantic representation of the system model, such as checks for wellformedness and consistency.

While this paper only integrates a single analysis model and visualization tool, most cyber physical systems would need multiple simulation-based analyses. Therefore, multiple MISDs would be linked together into a broader Assessment Flow Diagram31 where various discipline specific simulation models (Computational Fluid Dynamics, Finite Element Analysis, Computer Aided Design, etc.) have one or more shared, interrelated parameters. Co-mingling the model of analysis with the system or mission model allows designers to relate the metadata and results from various analysis models to the system or mission level performance measures.

# 5.3 | Framework Impact on Digital Engineering Domain

Ultimately, the DEFII framework guides engineering organizations in transforming domain specific models into a knowledge representation that both provides needs for existing workflows (integrating with domain models) and establishes the foundation for additional applications depending on an integrated view of the system as a whole (Digital Assistants, reasoning, constraint checking, etc.). This forward-looking component of the DEFII framework adds value to its use in the present day as it solves an existing problem (robust data integration across multiple models) with a solution that presents opportunity beyond the current need.

Augmented Intelligence applications such as Digital Assistants can be a force multiplier in a context where solutions are becoming increasingly complex and quicker turnaround times are expected. A robust, machine readable knowledge representation of the system under design, along with the relevant domains, is needed to inform an augmented intelligence agent, and semantic technologies are a viable candidate for this representation18,40. Existing research into the use of Machine Learning algorithms applied to ontological data could also be leveraged to provide added value41. The DEFII framework gives structure for using SWT in the DE context and opens these opportunities in the future.

# 6 | CONCLUSION

The DEFII framework addresses integration and interoperability challenges in the Digital Engineering context through the use of ontology-aligned data that is exposed through to external toolsets through three types of interfaces: the Mapping Interface, the Specified Model Interface, and the Direct Interface. It introduces the Model Interface Specification Diagram as a mechanism for defining interfaces that align with ontologically relevant data without the need for the interface designer to be an expert in ontologies or semantic technologies. By taking advantage of the formal nature of ontologies and the various technologies that have been developed to enhance and use ontologies, the framework both provides for the integration and interoperability needs of model-based design and analysis today and sets a foundation for further innovation in the future.

# ACKNOWLEDGEMENTS

This research was sponsored by the Systems Engineering Research Center (SERC), a University Affiliated Research Center (UARC) housed at Stevens Institute of Technology.

## REFERENCES

- 1. Defense Acquisition University Glossary. Accessed May 15, 2022. https://www.dau.edu/glossary/Pages/Glossary.aspx#!both|D|27345
- 2. Rogers EB, Mitchell SW. MBSE delivers significant return on investment in evolutionary development of complex SoS. Syst Eng. 2021;24(6):385-408. doi:10.1002/sys.21592
- 3. Kruse B, Blackburn M. Collaborating with OpenMBEE as an Authoritative Source of Truth Environment. Procedia Comput Sci. 2019;153:277-284. doi:10.1016/j.procs.2019.05.080
- 4. Bone MA, Blackburn MR, Rhodes DH, Cohen DN, Guerrero JA. Transforming systems engineering through digital engineering. J Def Model Simul Appl Methodol Technol. 2019;16(4):339-355. doi:10.1177/1548512917751873
- 5. Wagner DA, Bennett MB, Karban R, Rouquette N, Jenkins S, Ingham M. An ontology for State Analysis: Formalizing the mapping to SysML. In: 2012 IEEE Aerospace Conference. IEEE; 2012:1-16. doi:10.1109/AERO.2012.6187335
- 6. Hagedorn TJ, Smith B, Krishnamurty S, Grosse I. Interoperability of disparate engineering domain ontologies using basic formal ontology. J Eng Des. 2019;30(10-12):625-654. doi:10.1080/09544828.2019.1630805
- 7. Bone M, Blackburn M, Kruse B, Dzielski J, Hagedorn T, Grosse I. Toward an Interoperability and Integration Framework to Enable Digital Thread. Systems. 2018;6(4):46. doi:10.3390/systems6040046
- 8. Roper W. There Is No Spoon: The New Digital Acquisition Reality. United States Air Force; 2020. https://software.af.mil/wp-content/ uploads/2020/10/There-Is-No-Spoon-Digital-Acquisition-7-Oct-2020-digital- version.pdf
- 9. Moser T. The Engineering Knowledge Base Approach. In: Biffl S, Sabou M, eds. Semantic Web Technologies for Intelligent Engineering Applications. Springer International Publishing; 2016:85-103. doi:10.1007/978-3-319-41490-4\_4
- 10. Mordecai Y, Fairbanks JP, Crawley EF. Category-Theoretic Formulation of the Model-Based Systems Architecting Cognitive-Computational Cycle. Appl Sci. 2021;11(4):1945. doi:10.3390/app11041945
- 11. Gruber TR. The Role of Common Ontology in Achieving Sharable, Reusable Knowledge Bases. Kr. 1991;91:601-602.
- 12. Gruber TR. A translation approach to portable ontology specifications. Knowl Acquis. 1993;5(2):199-220. doi:10.1006/knac.1993.1008
- 13. Gruber TR. Toward principles for the design of ontologies used for knowledge sharing? Int J Hum-Comput Stud. 1995;43(5-6):907-928.
- 14. Coelho M, Austin MA, Blackburn MR. The Data-Ontology-Rule Footing: A Building Block for Knowledge-Based Development and Event-Driven Execution of Multi-domain Systems. In: Adams S, Beling PA, Lambert JH, Scherer WT, Fleming CH, eds. Systems Engineering in Context. Springer International Publishing; 2019:255- 266. doi:10.1007/978-3-030-00114-8\_21
- 15. Eddy D, Krishnamurty S, Grosse I, Wileden J. Support of Product Innovation With a Modular Framework for Knowledge Management: A Case Study. In: Volume 2: 31st Computers and Information in

Engineering Conference, Parts A and B. ASMEDC; 2011:1223-1235. doi:10.1115/DETC2011-48346

- 16. Hagedorn TJ, Krishnamurty S, Grosse IR. A Knowledge-Based Method for Innovative Design for Additive Manufacturing Supported by Modular Ontologies. J Comput Inf Sci Eng. 2018;18(021009). doi:10.1115/1.4039455
- 17. Daun M, Brings J, Weyer T, Tenbergen B. Fostering concurrent engineering of cyber-physical systems a proposal for an ontological context framework. In: 2016 3rd International Workshop on Emerging Ideas and Trends in Engineering of Cyber-Physical Systems (EITEC). IEEE; 2016:5-10. doi:10.1109/EITEC.2016.7503689
- 18. Hagedorn T, Bone M, Kruse B, Grosse I, Blackburn M. Knowledge Representation with Ontologies and Semantic Web Technologies to Promote Augmented and Artificial Intelligence in Systems Engineering. INSIGHT. 2020;23(1):15-20. doi:https://doi.org/10.1002/inst.12279
- 19. El Kadiri S, Kiritsis D. Ontologies in the context of product lifecycle management: state of the art literature review. Int J Prod Res. 2015;53(18):5657-5668. doi:10.1080/00207543.2015.1052155
- 20. Hoppe T, Eisenmann H, Viehl A, Bringmann O. Digital Space Systems Engineering through Semantic Data Models. In: 2017 IEEE International Conference on Software Architecture (ICSA). IEEE; 2017:93-96. doi:10.1109/ICSA.2017.35
- 21. Lu J, Ma J, Zheng X, Wang G, Li H, Kiritsis D. Design Ontology Supporting Model-Based Systems Engineering Formalisms. IEEE Syst J. Published online 2021:1-12. doi:10.1109/JSYST.2021.3106195
- 22. Madni AM, Sievers M. Model-based systems engineering: Motivation, current status, and research opportunities. Syst Eng. 2018;21(3):172-190. doi:10.1002/sys.21438
- 23. Petnga L, Austin M, Blackburn M. Semantically-Enabled Model-Based Systems. INSIGHT. 2017;20(3):29-38. doi:https://doi.org/10.1002/inst.12161
- 24. Wagner D, Kim-Castet SY, Jimenez A, Elaasar M, Rouquette N, Jenkins S. CAESAR Model-Based Approach to Harness Design. In: 2020 IEEE Aerospace Conference. IEEE; 2020:1-13. doi:10.1109/AERO47225.2020.9172630
- 25. Kovalenko O, Euzenat J. Semantic Matching of Engineering Data Structures. In: Biffl S, Sabou M, eds. Semantic Web Technologies for Intelligent Engineering Applications. Springer International Publishing; 2016:137-157. doi:10.1007/978-3-319-41490-4\_6
- 26. Jenkins JS, Rouquette NF. Semantically-Rigorous Systems Engineering Modeling Using SysML and OWL. Published online 2012:8.
- 27. Blackburn MR, Bone MA, Dzielski J, et al. Transforming Systems Engineering through Model-Centric Engineering, Final Technical Report SERC-2020-TR-009, WRT-1008 (NAVAIR.; 2020.
- 28. Bajaj M, Friedenthal S, Seidewitz E. Systems Modeling Language (SysML v2) Support for Digital Engineering. INSIGHT. 2022;25(1):19-24. doi:10.1002/inst.12367
- 29. Friedenthal S, Seidewitz E. A Preview of the Next Generation System Modeling Language (SysML v2). Syst Eng Newsl Proj Perform Int PPI. 2020;SyEN 95:18.
- 30. Zimmerman P, Gilbert T, Salvatore F. Digital engineering transformation across the Department of Defense. J Def Model Simul Appl Methodol Technol. 2019;16(4):325-338. doi:10.1177/1548512917747050
- 31. Cilli M, Parnell GS, Cloutier R, Zigh T. A Systems Engineering Perspective on the Revised Defense Acquisition System. Syst Eng. 2015;18(6):584-603. doi:10.1002/sys.21329
- 32. NVD Vulnerability Metrics. Accessed May 28, 2021. https://nvd.nist.gov/vuln-metrics/cvss
- 33. Arp R, Smith B, Spear AD. Building Ontologies with Basic Formal Ontology. Mit Press; 2015.
- 34. CUBRC, Inc. An Overview of the Common Core Ontologies. Published online September 23, 2020. Accessed March 20, 2021. https://github.com/CommonCoreOntology/CommonCoreOntologies/ blob/master/documentation/An%20Overview%20of%20the%20Com mon%20Core%20Ontologies%201.3.docx
- 35. GraphDBTM. Ontotext. Accessed March 20, 2021. https://www.ontotext.com/products/graphdb/

- 36. Teamwork Cloud CATIA Dassault Systèmes®. Accessed May 15, 2022. https://www.3ds.com/products-services/catia/products/nomagic/teamwork-cloud/
- 37. Musen MA. The protégé project: a look back and a look forward. AI Matters. 2015;1(4):4-12. doi:10.1145/2757001.2757003
- 38. Lamy JB. Owlready: Ontology-oriented programming in Python with automatic classification and high level constructs for biomedical ontologies. Artif Intell Med. 2017;80:11-28. doi:10.1016/j.artmed.2017.07.002
- 39. Shapes Constraint Language (SHACL). Accessed May 15, 2022. https://www.w3.org/TR/shacl/
- 40. Rouse WB. AI as Systems Engineering Augmented Intelligence for Systems Engineers. INSIGHT. 2020;23(1):52-54. doi:https://doi.org/10.1002/inst.12286
- 41. Austin M, Delgoshaei P, Coelho M, Heidarinejad M. Architecting Smart City Digital Twins: Combined Semantic Model and Machine Learning Approach. J Manag Eng. 2020;36(4):04020026. doi:10.1061/(ASCE)ME.1943-5479.0000774
