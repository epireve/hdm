---
cite_key: presutti_2019
title: Pattern-based Visualization of Knowledge Graphs
authors: Valentina Presutti, Luigi Asprino, Christian Colonna, Misael Mongiovì, Margherita Porena
year: 2019
date_processed: '2025-07-02'
phase2_processed: true
original_folder: arxiv_2106.12857_
images_total: 6
images_kept: 6
images_removed: 0
tags:
- Knowledge Graph
- Machine Learning
- Semantic Web
keywords:
- 1 introduction
- 2 pattern-based visualization of knowledge graphs
- 6 conclusions and future work
- BlueSky
- GitHub
- HTTP
- LodView
- MacroVu
- McBrien
- PatternInstance
- SemDev
- bottom-right
- client-side
- double-clicks
- e-ld-r
- e-mauroux
- extended-ld-reactor
- first-class
- gomez-perez
- graph-aware
- graph-based
- graph-based visualization
- high-level
- human-readability
- hypertext transfer protocol
- knowledge graph
- ld-reactor
- multi-filter
- ontology
- performance
---

# Pattern-based Visualization of Knowledge Graphs

Luigi Asprino 1 , Christian Colonna 1 , Misael Mongiov`ı 2 , Margherita Porena 2 , and Valentina Presutti 1 , 2

<sup>1</sup> University of Bologna, Bologna, Italy <sup>2</sup> STLab, ISTC-CNR, Rome, Italy {luigi.asprino,christian.colonna2,valentina.presutti }@unibo.it {misael.mongiovi,margherita.porena }@istc.cnr.it

Abstract. We present a novel approach to knowledge graph visualization based on ontology design patterns. This approach relies on OPLa (Ontology Pattern Language) annotations and on a catalogue of visual frames, which are associated with foundational ontology design patterns. We demonstrate that this approach significantly reduces the cognitive load required to users for visualizing and interpreting a knowledge graph and guides the user in exploring it through meaningful thematic paths provided by ontology patterns.

Keywords: Knowledge Graphs · Information Visualization · Ontology Design Patterns · Exploratory Search.

# 1 Introduction

Exploring and understanding large knowledge graphs is a recurrent and tricky task in most knowledge graph and ontology projects. Its difficulty is amplified by the magnitude and the heterogeneity of the analyzed KG [\[8\]](#page-14-0). Visualization methods are the main means to support KG understanding, but existing visualization tools mainly reflect the syntactic structure of KGs rather than their conceptual semantics, thus limiting usability and clarity [\[10\]](#page-14-1). An ideal KG visualization tool should facilitate the answering of questions such as: what are the conceptual components of a KG? What are the key elements of such components? How these components are instantiated? Which altogether help answering the more general question of what a KG talks about. We think that to address this problem there is a need for a change of perspective on how to visualize the content of a KG, and that this perspective can be supported by ontology design patterns. Ideally, an intuitive (displayed) overview of a large knowledge graph should fit the dimension of a page, which can be achieved if KG data are grouped according to conceptual components, identified by ODPs.

In this paper, we propose a novel approach to KG visualization which relies on the notion of Ontology Design Pattern. Ontology Design Patterns (ODPs) [\[11\]](#page-15-0) are modeling solutions that address recurrent ontology design problems. ODPs are the basic building blocks of ontologies, and, consequently, they shape the

<span id="page-1-2"></span><span id="page-1-1"></span><span id="page-1-0"></span>(ontology-based) KGs. In this vision, ODPs embody the key conceptual components that a KG instantiates. Following this intuition, we devised an approach that promotes ontology design patterns as first-class citizens for accessing and navigating KGs. The approach relies on the following hypotheses. (H1) The collection of ODPs provides a very concise summary of the overall content of a KG. (H2) Each ODP provides a meaningful view of the content of a KG. (H3) ODPs define thematic paths that guide the exploration and interaction with the KG. (H4) Each ODP can be associated with a visual frame that is meant to define an intuitive standard visualization for the instances of a pattern thus easing the interpretation of the information.

<span id="page-1-3"></span>To assess the feasibility and benefits of our approach we conducted a pilot study. In this study, we developed a tool, called ODPReactor, which provides us with a proof-of-concept of the pattern-based approach to KG visualization. ODPReactor leverages the Ontology Pattern Language annotations (OPLa) for recognizing instances of patterns within a KG. Once pattern instances are recognized, ODPReactor summarizes the content of the KG in a single concise visualization showing what are the patterns composing the KG, how they are instantiated and what are the key concepts of each pattern (cf. [\(H1\)](#page-1-0)). ODPReactor allows the users to select a pattern for accessing and navigating the KG (cf. [\(H2\)](#page-1-1) and [\(H3\)](#page-1-2)). ODPReactor also defines a set of visual frames that are used to display intuitively the data in a pattern occurrence (cf. [\(H4\)](#page-1-3)).

As a case study, we deployed ODPReactor for accessing (a portion of) ArCo, the Italian Cultural Heritage KG [\[5\]](#page-14-2). ArCo consists of a network of seven ontologies and 169 million triples about 820 thousand cultural entities. ArCo's ontologies reuse ODPs from online repositories (e.g. ODP portal) whose occurrences are annotated using OPLa. We selected the ODPs to ensure a balance between patterns involving "physical" and "abstract" concepts (for example, the visualization of the geo-localization of a cultural property involves physical objects only, while a collection of measurements of an object involves both physical and abstract concepts) and then, we associated each pattern with a cognitivegrounded visualization. Finally, to validate our hypotheses, we conducted a user study that involved 11 participants. The results show the validity of the ODPbased visualization approach in terms of usability and rapidity in accessing the information.

The remainder of this paper is structured as follows. After a discussion of related work (Sect. [2\)](#page-1-4), we present the proposed ODP-based visualization approach (Sect. [3\)](#page-2-0) and discuss its implementation (Sect. [4\)](#page-7-0). Eventually we report the results of our user study (Sect. [5\)](#page-10-0) and conclude the paper.

# <span id="page-1-4"></span>2 Related Work

We place our research in the area of Knowledge Graph visualization. To the best of our knowledge, the only tool that adopts patterns as guidance for the exploratory search is Aemoo [\[21\]](#page-15-1). Aemoo is a Linked Data exploration tool that uses Encyclopedic Knowledge Patterns as relevance criteria for selecting, organizing, and visualizing knowledge. Although our work draws inspiration from Aemoo, our approach aims at broadening Aemoo's scope (which is limited to encyclopedic patterns) by developing a general method for interacting with Knowledge Graphs shaped according to any Ontology Design Pattern.

Plenty of approaches have been proposed for visualizing KGs [\[9\]](#page-14-3). Most of them fall into two categories: graph-based visualization and template-based visualization [\[9\]](#page-14-3). Tools in the former category use network layouts to visualize RDF data as they mirror the underlying RDF structure. Tools belonging to the latter category rely on the design of predefined HTML templates which are populated with resources resulting from the execution of predefined SPARQL queries.

Graph-based visualization tools. H-BOLD [\[24\]](#page-15-2) is a graph-based visualization tool whose architecture is divided in three different levels: the Cluster View, the Schema View, and the Instance View. This approach is similar to ours, especially in the summarization provided in the Cluster View. However, the summarization is guided by statistical correlations instead of conceptual analysis of the KG. KC-Viz [\[20\]](#page-15-3) was among the firsts ontology visualization tools using the notion of key concepts [\[23\]](#page-15-4) (which are the statistically relevant classes for the KG at hand). Other tools (e.g. RDFDIGEST+ [\[28\]](#page-15-5)) followed the KC-Viz approach. We adopt a similar strategy for selecting the key concepts of a KG and relating them to ODPs.

Template-based visualization tools. Exhibit [\[15\]](#page-15-6) is one of the first example of usage of templates (called Lens Templates) for presenting KGs. On the same line of research we can find other works based on template based visualization, such as LodView[3](#page-2-1) (the tool adopted for accessing the ArCo KG) or others [\[1,](#page-14-4)[29,](#page-15-7)[18,](#page-15-8)[26,](#page-15-9)[2\]](#page-14-5). A special case is the tool proposed by McBrien et al. [\[19\]](#page-15-10) which includes a mechanism for recommending the most appropriate visualization for a given SPARQL query. Our approach leverages these experiences, meaning that, the visualization strategies implemented by ODPReactor could be seen as templates for visualizing a KG. A limit of the existing template-based approaches is that they consider as meaningful boundary for describing an entity its neighborhood only (which is typically the set of triples involving a resource), and all the entities are described with the same boundary. However, while this is an effective strategy for "simple" KGs, it fails short with sophisticated KGs in which the meaningful boundary of each entity depends on the type of the entity and the pattern the entity is involved in. ODPReactor goes beyond these approaches since it associates each entity of the KG with a meaningful boundary that depends on the ODPs the entity is involved in (implying that each entity might have a different boundary).

# <span id="page-2-0"></span>3 Approach

In this section we briefly review the main concepts we build upon (ODP, OPLa and key-concept classes), then we describe our framework and an example of visualization based on the ODP Part Of.

<span id="page-2-1"></span><sup>3</sup> <https://lodview.it/>

## <span id="page-3-1"></span>3.1 Background

Design patterns: Ontology Design Patterns (ODPs)[4](#page-3-0) [\[11\]](#page-15-0) are modeling solutions to recurrent ontology design problems. ODPs can be divided into multiple categories: logical, architectural, content, presentation [\[25\]](#page-15-11). In our case study, we used three ontology design patterns (implemented in the context of ArCo project [\[6\]](#page-14-6)). The first, Time-Indexed Typed Location, represents the locations of an object (e.g. a cultural property) in specific time intervals and with specific purposes (e.g. storage, exposition). It specializes Time-Indexed Situation, a pattern to represent situations that have an explicit time parameter. The second, Measurement Collection, represents a collection of measures. It is a specialization of pattern Collection, to represents collections and their members. Last, Cultural Property Component Of represents a cultural property and its components and specializes Part Of, a pattern to represent entities and their parts.

OPLa: OPLa ontology is an ontology design pattern representation language [\[13\]](#page-15-12), which enables annotating ontologies to (1) indicate that an axiom or class belongs to a certain module or pattern, (2) specify how an axiom or class is related to the pattern, and (3) represent relationships between two patterns or between a pattern and a module. We extended OPLa to represent instances of patterns. We added the property opla:isPatternInstanceOf with domain an individual of type opla:PatternInstance and range an individual of type opla:Pattern. To indicate that an entity belongs to a pattern instance. We defined the property opla:belongsToPatternInstance (and its inverse opla:hasPatternInstanceMember), whose domain and range are respectively owl:Thing and opla:PatternInstance. Our methodology relies on the use of this annotations to identify and distinguish specific instances of patterns in data.

Key Concepts: Knowledge graph summarization is crucial in graph visualization and other applications where large graphs need to be handled [\[7\]](#page-14-7). In [\[23\]](#page-15-4) the authors introduced key concepts as elements which best summarize an ontology. Following this approach, we adopted the Degree centrality measure [\[7\]](#page-14-7) (a measure often used for knowledge graph summarization [\[27\]](#page-15-13)) for estimating the relevance of each class of a given ontology.

### 2 Pattern-based visualization of Knowledge Graphs

We propose a general framework based on three levels of visualizations. The top level, namely the ODP level, is a view of the knowledge graph that shows a graph whose nodes represent either an ODP instantiated in the KG or a key concept of an ODP. Edges of this graph are modeled according to the OPLa vocabulary and its extension discussed in Sect. [3.1.](#page-3-1) The second level, called exploration level, presents the occurrences of a specific ODP and allows users to filter the occurrences according to her information needs. The third one, the visualization level, is dedicated to the visualization of a single occurrence of an ODP or an

<span id="page-3-0"></span><sup>4</sup> <http://ontologydesignpatterns.org>

<span id="page-4-0"></span>![](_page_4_Figure_1.jpeg)
<!-- Image Description: This image from an academic paper presents three visualizations related to a data model. (a) shows a graph illustrating relationships (specializes, part of, has view) between different types of cultural properties. (b) depicts a table for exploration, showing "view," "object," "parts," and "filter controls." (c) displays a visualization level illustrating a part-whole relationship using geometric shapes. The image likely describes different levels of data representation and user interaction within the system. -->

Fig. 1: Overview of the system on three levels

entity of the KG. First, we intuitively describe the aim and the characteristic of these levels, and, then we formally define our visualization method.

We remark that the design of all the layers followed Gestalt psychology principles [\[17\]](#page-15-14) and studies on visual language [\[14\]](#page-15-15). This principles were particularly relevant for the visualization level. For example, Common Region Gestalt principle states that when objects are enclosed in the same region we perceive them as being grouped together. Following this idea, we enclosed all members of a collection within a line in designing the visual frame for pattern Collection.

ODP level. This is the highest level of abstraction and summarization of a knowledge graph. This visualization provides (in the dimension of a page) a concise overview (cf. H1) of the most relevant concepts instantiated in a KG. Specifically, the system shows a graph representation of the most relevant key concepts (i.e. classes) of a KG and a number of views related to such concept. Each view corresponds to an ODP and identifies a perspective for exploring a KG. Views and key concepts are represented by nodes, while edges explain the relations among them. Figure [1a](#page-4-0) depicts an example of the graph visualized at this level. The graph contains two views (Part Of and its specialization Cultural Property Component Of) and a key concept (Cultural Property). Edges are of two types: those describing the relation between ODPs (e.g. specializes, has component) and those relating a key concept to the ODP it appears in (has View). It is worth noticing that both relations are retrieved from OPLa annotations, the edge has view symbolizes opla:isNativeTo property, whereas specializes edges stand for opla:specializationOfPattern. ODPReactor also provides filters (not shown in Figure) to reduce the number of nodes in the graph visualization, including an importance threshold for classes to be visualized as key concepts. the size of the nodes is proportional to the logarithm of the number of occurrences of the pattern. This provides the user with an insight of how the various components of the KG are instantiated. Interestingly, this view gives a concise overview of the overall knowledge graph From this view the user can rapidly perceive a summary of the information in the KG: what its main conceptual components are, what the key elements of such components are and how these components are instantiated.

Exploration level. The Exploration level is the second level of visualization. This level shows the instances of ODPs and key concepts. The user can access to this level by clicking either on an ODP or a key concept showed at the ODP level. In both cases instances are presented in a tabular form. A schematic representation of this level is shown in Figure [1b.](#page-4-0) As for the instances of the key concepts, the table shows the list of individuals that can be filtered by the user. The user can access to the detailed view of a single individual by clicking on a row in the table.

As for ODP instances, each column of the table is associated with an ODP dimension (e.g. for Time Indexed Typed Location dimensions are start time, end time, location type, and coordinates), while each row represents an instance. For every dimension of an ODP, we designed a set of semantic filters that allow users to define the criteria for filtering instances. In agreement with the open-world assumption, by default, the filters include instances that do not have a value for the filtering criteria. However, we give the possibility to switch to the close-world assumption and exclude resources for which missing data do not consent filters to be applied. Clearly, filters can be combined in order to restrict the set of instances according to multiple criteria defined on multiple dimensions. Then, the user can access to the detailed view of a single pattern instance by clicking a row of the table.

It is noteworthy that the exploration and the filtering strategy implemented in the visualization depends on the ODPs which the KG is composed of. Therefore, both the summary presented at ODP level and the interaction designed at visualization level rely on the ODPs instantiated in the KG thus complying with the hypotheses H2 and H3.

Visualization level. The visualization level provides the users with a detailed view of an instance of a pattern or a class of the KG. Specifically, this visualization presents the pattern instances through the lens of a visual frame. A visual frame is a standard visualization designed for a pattern (e.g. Geo-Localization of entities are depicted as markers of a map) which presents the pattern instance by means of a set of intuitive graphical elements. Figure [1c](#page-4-0) depicts a schematic example of visual frame for pattern Part Of. It is worth noticing that, even if the visual frame is specifically designed for an ODP, it can be reused on different KGs implementing the ODP. Consequently, this strategy implicitly promotes visual frames as standard visualization for a pattern (cf. H4). The visual frames are also displayed in the visualization of the individuals of the KG. In fact, the visualization level for an individual is designed for displaying all the visual frames which the individual is involved in and all the property-value pairs associated to the individual. Interestingly, in doing so, the boundary of information presented together an individual of the KG is delimited by the boundary of the ODPs.

Formalization of the approach. We now formally describe our approach. We define a RDF knowledge graph G as G ⊆ (U ∪ B) × U × (U ∪ B ∪ L) where U, B and L are the set of URIs, the set of blank nodes and the set of literals, respectively. We assume that ODPs are annotated with OPLa ontology [\[13\]](#page-15-12). Briefly, classes that belong to an ODP are annotated with a relation opla:isNativeTo connecting to the URI of the corresponding ODP pattern. We define P as the set of ODP patterns implemented in G. We also define implementationG(P) ⊆ G as the subgraph (set of tuples) corresponding to the TBox implementation of the pattern in the knowledge graph, induced by the set of source nodes of relations opla:isNativeTo targeted in P. We also considers a special set of (key concept) nodes K, which are special classes that help the user identify and distinguish specific instances of patterns.

Given an ODP pattern P ∈ P, we can identify a number of occurrences of such a pattern in the knowledge graph, where an occurrence is an ABox implementation of P, composed by individuals and relations that respect the pattern structure. The identification of such occurrences is dependent on the specific pattern and can be performed by suitable SPARQL queries. While a general way to identify ODP occurrences is worth of further investigation, in this work we assume such occurrences have been previously identified and annotated with the extension of OPLa discussed in Sect. [3.1](#page-3-1)[5](#page-6-0) . We denote the set of occurrences of a pattern P as Q<sup>P</sup> , where an element Q ∈ Q<sup>P</sup> is a subgraph of G that concretely materializes P. Their nodes are denoted as nodes(Q).

At the ODP level our tool shows a graph whose nodes represent patterns and key concepts (P ∪K) and edges show their relations. A Key-concept node K ∈ K, which corresponds to a class in G, is connected to a pattern node P through a relation hasView if K is a class in implementationG(P). Patterns are also interconnected by OPLa [\[13\]](#page-15-12) relations (e.g. opla:specializationOfPattern – in the tool URIs are substituted with user-friendly descriptions).

The exploration level requires a pattern-specific mapping function from data elements to visual elements and a pattern-specific set of filter controls. Since at this level data are visualized in a table, the mapping needs to associate nodes of the pattern (typically literals) to columns. Specifically, each pattern P is associated to a set of c columns and a function (implemented by specific code) emap<sup>P</sup> : Q<sup>P</sup> → L<sup>c</sup> ∪ {φ} which associates a pattern instance Q ∈ Q<sup>P</sup> to a list of c literals to be shown in a row. The special symbol φ accounts for filters. Specifically emap<sup>P</sup> (Q) = φ if Q does not satisfy the filter constraints set by the user. The GUI for filters is pattern dependent and can be built by combining a set of filter controls, each one associated to a specific property. We implemented a set of filter control templates to account for different data types (dates, locations, numerical values, discrete values), which can be combined to construct the filter GUI of each pattern.

The visualization level consists of the visualization of a pattern instance in a specific page. Our approach requires a pattern-specific function vmap<sup>P</sup> : Q<sup>P</sup> → VF that associates each pattern instance Q to its correspondent visualization frame. The correspondence between data values and visual elements is established by suitable knowledge-graph-independent SPARQL queries.

Note that our approach is completely independent of the specific implementation of patterns in the knowledge graph and therefore enable reusing the visu-

<span id="page-6-0"></span><sup>5</sup> We implemented the code to generate such annotations for the patterns we employed in our prototype

<span id="page-7-1"></span>![](_page_7_Figure_1.jpeg)
<!-- Image Description: This image from an academic paper illustrates a data model and query processing for visual pattern matching. It shows an Entity-Relationship Diagram (ERD) representing objects and their parts, linked to visual depictions. SQL-like queries (`emapp`, `vmapp`) are presented, demonstrating how to extract object labels and counts, and their corresponding visual frames (depictions). A mapping table links the symbolic object-part relationships to their visual representations. The diagrams clarify the relationships between data in different layers. -->

(a) Pattern Part Of and associated mapping functions (b) Example of pattern instances mapping

Fig. 2: An example of application of our approach on pattern Part Of

alization code of a pattern on a different knowledge graph that implements the same pattern and is annotated with the extended OPLa. To make a pattern P visualizable, the developer needs to compose the set of filter controls, design the visual frame and define the functions emap<sup>P</sup> (Q) and vmap<sup>P</sup> (Q). Figure [2](#page-7-1) shows an example of a pattern and how data of specific instances is mapped into the GUI. The left part (Figure [2a\)](#page-7-1) depicts the Part Of ODP, defined by property hasPart, which connects an object to its parts. We include the properties label and depiction, although not part of the pattern, since they are present (at least label) in all KGs for crucially increase their human-readability. The pattern is associated to the emap<sup>P</sup> and vmap<sup>P</sup> functions, whose implementation is reported in the right side of Figure [2a](#page-7-1) in pseudo-SPARQL. Given a pattern instance Q, identified by uri(Q), emap<sup>P</sup> (Q) retrieves the object label (?l) and the number of parts (?p). It also applies the filter (user defined filter in the WHERE clause) and return φ (an empty set of tuples) if filter constraints are not satisfied. vmap<sup>P</sup> (Q) extracts figures of the object and every part (?d and ?dp, identified by property depiction) and maps them into the visual frame (the visual mapping is summarized by the visual frame() function). The right part (Figure [2b](#page-7-1) shows a concrete example of two instances Q<sup>1</sup> and Q<sup>2</sup> of pattern Part Of and their mapping into the table for the exploration (bottom-right side) and the visual frame (top-right side). For space reasons we only show the visual frame for Q1. For each label and depiction we report the corresponding SPARQL variable of the emap<sup>P</sup> and vmap<sup>P</sup> implementations (taken from Figure [2a\)](#page-7-1).

# <span id="page-7-0"></span>4 Implementation

Design Methodology. We put emphasys on the importance of user cognition in the visualization design process [\[22\]](#page-15-16) and, taking inspiration by other successful experiences (e.g. [\[12\]](#page-15-17)) we applied User-Centered Design (UCD) principles. Specifically, we followed agile design methodology with brief iteration cycles (1

<span id="page-8-3"></span>![](_page_8_Figure_1.jpeg)
<!-- Image Description: This diagram illustrates the architecture of a system for exploring and visualizing linked data (LD). It shows a frontend with two microservices (ODPBrowser and Extended-Ld-Reactor), built using Node.js and React.js, communicating via HTTP. The frontend interacts with a data layer comprising SPARQL endpoints and a MongoDB database. The ODP-UI, a ReactJS component package, facilitates LD visualization. The user interacts with the system through exploratory search and ontology/LD visualization functionalities. -->

Fig. 3: ODPReactor architecture.

week sprints). This process involved 2 developers, and 3 users collaborated in the process by continuously providing feedback on the tool. Once the tool reached a stable version, we conducted an experiment with an 11-participants focus group and evaluated the usability according to the System Usability Scale (SUS) [\[4\]](#page-14-8). The results are discussed in Section [5.](#page-10-0)

ODPReactor Architecture. ODPReactor is divided into three main components:

- ODPBrowser, a service to explore and filter the ODP/key concepts graph and their instances (it encapsulates ODP level and exploration level described in Sect. [3\)](#page-2-0);
- Extended-Ld-Reactor (E-LD-R), a service to visualize resource pages with their data (it encapsulates the visualization level);
- ODP-UI, the visual frames library, embedded in the E-LD-R microservice.

The two services are exposed in a client-side React.js[6](#page-8-0) application hosted and served by a Node.js[7](#page-8-1) environment. The services can be configured to retrieve data from one or more SPARQL endpoints and store configuration data (e.g. the list of KGs and their respective SPARQL endpoints) in a MongoDB[8](#page-8-2) The architecture is detailed in Figure [3.](#page-8-3) We discuss here the three components.

ODPBrowser is a service implementing the ODP level (ODPs and concepts graph visualization) and the exploration level (table with filters) discussed in Sect. [3.](#page-2-0) The ODP/key concepts graph is implemented by using Graphin[9](#page-8-4) , a

<span id="page-8-0"></span><sup>6</sup> <https://reactjs.org/>

<span id="page-8-1"></span><sup>7</sup> <https://nodejs.org/>

<span id="page-8-2"></span><sup>8</sup> <https://www.mongodb.com/>

<span id="page-8-4"></span><sup>9</sup> <https://graphin.antv.vision/>

graph visualization library. Every concept has an associated importance score (computed by degree centrality), which enables filtering concepts whose importance is below a user-defined threshold. By double clicking on a node, the user can navigate to the exploration level where all instances of the selected key concept or data associated to the selected ODP are displayed in a table. This view contains filters semantically related to the specific ODP (e.g. the ODP Time Indexed Situation enable filtering by time interval).

ODP-based Semantic Filtering. To filter geographic locations, we implemented a map with LeafletJS[10](#page-9-0) where users can draw a closed perimeter. Perimeter coordinates are then calculated and resources localized inside the area are selected while others discarded. Numeric filtering (such as measures, time intervals, number of components) can be performed by means of sliders where the user can select with a cursor interval of interest. We used React Compound Slider[11](#page-9-1) to develop the facets. Among other facets, we used checkboxes to select or deselect categorical data such as location types. By double clicking on a table row, the user is redirected to Extended-Ld-Reactor, which visualizes the selected instance.

Extended-Ld-Reactor is an extension of Linked Data Reactor (LD-R) [\[16\]](#page-15-18), a full stack application (based on Fluxible[12](#page-9-2), React.js and Semantic UI[13](#page-9-3)), which facilitates mapping URIs into visual components. We embedded specific user interface for ODP-based visualization in LD-Reactor and configured it to visualize resources related to ODPs. The user interface makes use of a library of visual frames (namely ODP-UI, discussed below), which can be visualized singularly or through a mosaic grid with all visual frames associated to a specific resource.

ODP-UI is a library of visual frames where each frame displays data related to a specific ODP, as discussed in Sect. [3.](#page-2-0) Each visual frame is implemented as a React.js component. We implemented visual frames for the patterns Time-Indexed Typed Location, Measurement Collection, and Cultural Property Component Of, discussed in Sect. [3.1.](#page-3-1)

Deployment. We deployed ODPReactor for the ArCo knowledge graph [\[5\]](#page-14-2). ArCo is the Italian Cultural Heritage knowledge graph, consisting of a network of seven vocabularies and 169 million triples representing 820 thousand cultural entities. The ArCo ontology has been developed following the eXtreme Design methodology, an ontolology design methodology which uses ODPs as building blocks for constructing ontologies. This makes ArCo a good candidate for evaluating our approach.

Code. The implementation of the framework is available as open source project on GitHub[14](#page-9-4) .

Use case scenario. We describe a use-case scenario as an example to show how the ODPReactor components interact. A user (say Claire) is interested in getting

<span id="page-9-0"></span><sup>10</sup> <https://leafletjs.com/>

<span id="page-9-1"></span><sup>11</sup> <https://react-compound-slider.netlify.app/>

<span id="page-9-2"></span><sup>12</sup> <https://fluxible.io/>

<span id="page-9-3"></span><sup>13</sup> <https://semantic-ui.com/>

<span id="page-9-4"></span><sup>14</sup> <https://github.com/ODPReactor>

information about all cultural properties that in 1856 were located in a specific area in Paris. Claire accesses to the ODPBroswer, retrieves the ODPs composing ArCo and double-clicks the node representing the Time-Indexed Typed Location. A data table with cultural property instances and associated data (according to dimensions of the pattern) is shown and a series of filter facilities are made available to her. Claire then filters data by: (i) drawing an area around Paris on the location filter control geographical map; and (ii) selecting a time interval with the interval filter control slider. She locates the specific cultural property she is interested in, and selects it. ODPBrowser pass the control to Extended-Ld-Reactor to load the instance data from the SPARQL endpoint and display it in a mosaic grid of visual frames.

# <span id="page-10-0"></span>5 User Study

In this section, we report on the results of the user evaluation of the proposed approach. As proof-of-concept of our approach, we deployed ODPReactor for a portion of the ArCo KG. The portion included 200 cultural properties randomly selected among those participating to (at least) an instance of the three ODPs chosen for the case study. In terms of pattern instances this selection included: 49 instances for Cultural Property Component Of, 270 for Time Indexed Typed Location and 158 for Measurement Collection. The test was conducted by 11 users, composed by 3 researchers, 5 Phd students and 3 working professionals. All participants were familiar with Semantic Web and Linked Data technologies and were not involved in the development process.

The purpose of the test was to evaluate the ability of the tool to perform the following tasks:

- present the KG in a clear, concise and intuitive way (cf. H1, H2, H4);
- give the users a usable interface for searching specific instances (cf. H3).

Each tester was asked to perform a series of searching tasks (e.g. finding the length of an object) and to answer questions about the selected items. We dedicated a section of the questionnaire for each task. Each section presents the task and asks the user to rate: (i) the difficulty and rapidity in performing the task; (ii) the usability of the tool. The scores range was on a scale of 1 (very easy/rapid/usable) to 5 (very difficult/slow/unusable). To evaluate the general level of user satisfaction, we added to the survey a section containing the SUS-System Usability Scale questionnaire [\[3\]](#page-14-9). Before starting the test, the users were asked to perform a brief tutorial defined for the tool. The tutorial presents the user the three visualization levels (ODP level, exploration level, visualization level) and, in each of them, it shows the position of the filters. We measured the actual time occurred for performing each task and asked the participants to record their screen and send us the recording. The latter was useful for understanding the reason of possible failures or slowdowns. 10 of the 11 participants agreed to record their screen and share the recording.

<span id="page-11-0"></span>![](_page_11_Figure_1.jpeg)
<!-- Image Description: The image is a pie chart illustrating the distribution of subjective ratings. Six respondents rated something as "Excellent," four as "Good," one as "Poor," and one as "Awful." The chart visually represents the frequency of each rating category, likely to summarize participant feedback or survey results within the paper's overall analysis. No equations or other illustrations are present. -->

Fig. 4: SUS results.

The results of the evaluation according to the SUS scale are presented in Figure [4.](#page-11-0) They show that the tool is considered excellent by more than half of the users and good by the remaining ones except one, whose judgment was poor. The average score was 81.4, with a standard deviation of 12.6.

Assessment of the visualization level. A first group of tasks, reported in Table [1,](#page-12-0) was designed to evaluate the clarity of the visualization level (therefore assessing the hypothesis H4). In order to compare ODPReactor with existing tools we asked each user to perform the same task also using LodView (a widely known KGs viewer adopted for ArCo). We considered one task per ODP View. Each task was executed twice per tool in order to measure also the improvement with the experience. For each execution the user was asked questions about the dimensions of the ODP.

We considered as evaluation metric the number of correct answers, the time of execution and the users judgment of usability. An answer has been evaluated as correct if the user correctly identified the entry containing the data, although the answer is only partial. For example in tasks TITL1 and TITL2, for littleknown cities the users had difficulties in distinguishing the city from the village or from the county (all reported in the same entry). Therefore we considered all such answers as correct. The results are reported in Figure [5.](#page-13-0) Figure [5a](#page-13-0) shows the number of correct task executions. ODPReactor always performs similarly or better than LodView. Figure [5b](#page-13-0) shows the average task execution time. ODPReactor always performs better than LodView, with the exception of TITL 1, which regards retrieving the location of a cultural property. By analyzing the recordings it emerges that the users have quickly identified the data, but have delayed the transcription, because of difficulties in distinguishing the town (specifically Caravino and Vittorio Veneto) from the village or from the province. The same behaviour is not reflected in the LodView tasks, since the answers consist in widely-known cities (specifically Rome and Turin). Figure [5c](#page-13-0) shows the user judgment of the tool, where ODPReactor was considered significantly more adequate than LodView. This result is emphasized for the Measurement Collection tasks, where ODPReactor was evaluated unanimuosly very adequate while the

<span id="page-12-0"></span>

| ID     | ODP involved       | Question                                                          |
|--------|--------------------|-------------------------------------------------------------------|
| Comp 1 | Cultural Property  | How many components is the object                                 |
| Comp 2 | Component of       | made of?                                                          |
| TITL 1 | Time indexed typed | In which city is the cultural property                            |
| TITL 2 | location           | located?                                                          |
| MC 1   |                    | Measurement collection What is the length/height of this cultural |
| MC 2   |                    | property?                                                         |

Table 1: Data visualization tasks

<span id="page-12-1"></span>

| ID        | ODP involved                      | Question                                                                |
|-----------|-----------------------------------|-------------------------------------------------------------------------|
|           | ES Task 1 Measurement collection  | How many cultural properties are higher<br>than 2 m?                    |
| ES Task 2 | Cultural Property<br>Component of | How many cultural properties have at least<br>eight components?         |
| ES Task 3 | Time indexed typed<br>location    | How many cultural properties have Firenze as<br>their current location? |
| ES Task 4 |                                   | How many cultural properties were there in<br>Firenze before the 1945?  |
| ES Task 5 |                                   | How many works by Prampolini Enrico are<br>there in Bologna?            |

Table 2: Exploratory search tasks

judgment for LodView was almost equally distributed from Very adequate to Inadequate.

Assessment of the ODP and exploration level. In order to assess H1-3 hypotheses we designed a group of tasks involving the ODP level and exploration level. These tasks, reported in Table [2,](#page-12-1) are designed for evaluating the benefits of the approach in streamline the navigation and search of information in the KG. All the tasks required to identify the number of occurrences in the KG satisfying a given searching criterion. The first two tasks (referred to Measurement collection ODP and Cultural property component of ODP) can be performed by applying just one filter, while the last three ones (referred to Time indexed typed location ODP) require the activation of more than one filter. We chose the ODP Time Indexed Typed Location for the multi-filter tasks since this pattern is more complex then the others and hence it has more filter controls. To evaluate the general level of user satisfaction, we asked the users to answer a survey defined according to the SUS-System Usability Scale questionnaire [\[3\]](#page-14-9).

Finally, we report on the results of the exploratory research tasks on ODPReactor. We did not compare this task with LodView since it does not provide exploratory search functionalities. In counting the number of occurrences that satisfy the given constraints, we did not make any assumption about open or close world, and considered correct both the answers that include or exclude objects that do not contain some of the properties necessary for applying the filter.

<span id="page-13-0"></span>![](_page_13_Figure_1.jpeg)
<!-- Image Description: The figure presents three bar charts comparing "ODP-Reactor" and "Lodview" performance across six test cases (Comp 1, Comp 2, TITL1, TITL2, MC1, MC2). (a) shows correctness, with values seemingly representing a correctness score. (b) displays timing results, likely execution times. (c) provides a more granular assessment of adequacy, categorized as very adequate, adequate, medium, inadequate, and very inadequate. The charts aim to quantitatively evaluate and compare the two systems' performance in terms of correctness, speed, and adequacy. -->

(c) Usability.

Fig. 5: Data visualization tasks

Results are summed up in Figure [6.](#page-14-10) We collected 55 (11 × 5) responses by aggregating correctness, usability and difficulty, from all tasks and all users. Most of the users performed the task correctly (Fig. [6a\)](#page-14-10). We analyzed the recordings for understanding the reasons of failure or difficulties in executing the task. It emerged that among 10 wrong answers, 9 ones are due to failures to apply all filters necessary for the complex multi-filter tasks, while for the other one the data was correctly identified but wrongly reported. Specifically, the testers wrongly set the filter of the Time-indexed Typed Location instances for selecting only those having a certain type (e.g. Current Location). This indicates that the usage of such filter was not intuitive for the testers and it has to redesigned. Finally, Figure [6b](#page-14-10) shows the result of the questions about usability of the tool. Most of the users judged the tool very adequate or adequate. 51 answers out of 55 were positive or intermediate. Figure [6c](#page-14-10) shows similar positive results about difficulty.

# 6 Conclusions and Future Work

This work proposed a novel approach to Knowledge Graph visualization that uses Ontology Design Patterns as first-class citizens for accessing and navigating KGs. We described a general framework that enables reusing an ODP-related visual

<span id="page-14-10"></span>![](_page_14_Figure_1.jpeg)
<!-- Image Description: The image contains three pie charts presenting survey results. (a) shows the correctness of answers (45 correct, 10 incorrect). (b) displays usability ratings (24 very adequate, 16 adequate, 11 medium, 2 very inadequate). (c) illustrates task difficulty (19 very easy, 19 easy, 13 medium, 2 difficult, 2 very difficult). The charts likely assess system performance based on user feedback in an academic study. -->

Fig. 6: Exploratory search tasks

frame to different KGs and implemented a tool for validating the concept. The results of the execution of a set of tasks on the tool demonstrated the validity of the proposed approach, confirmed by considering both objective parameters and user perspective. In future we plan to enrich our library of visual frames with new ODP-based views and to explore general methods for automatizing the annotation of pattern instances. We also plan to study an automatic system for building filter facets and to make an extensive evaluation on a larger number of users.

# References

- <span id="page-14-4"></span>1. Arndt, N., Z¨anker, S., Sejdiu, G., Tramp, S.: Jekyll rdf: Template-based linked data publication with minimized effort and maximum scalability. In: Proc of ICWE. pp. 331–346 (2019)
- <span id="page-14-5"></span>2. Auer, S., Doehring, R., Dietzold, S.: Less - template-based syndication and presentation of linked data. In: Proc of ESWC. pp. 211–224 (2010)
- <span id="page-14-9"></span>3. Brooke, J.: Sus - a quick and dirty usability scale. In: Usability Evaluation in Industry, pp. pp.189–194. Taylor & Francis (1996)
- <span id="page-14-8"></span>4. Brooke, J.: Sus: a retrospective. Journal of usability studies 8(2), 29–40 (2013)
- <span id="page-14-2"></span>5. Carriero, V.A., Gangemi, A., Mancinelli, M.L., Marinucci, L., Nuzzolese, A.G., Presutti, V., Veninata, C.: Arco: The italian cultural heritage knowledge graph. In: Proc of ISWC. pp. 36–52 (2019)
- <span id="page-14-6"></span>6. Carriero, V.A., Gangemi, A., Mancinelli, M.L., Nuzzolese, A.G., Presutti, V., Veninata, C.: Pattern-based design applied to cultural heritage knowledge graphs. Semantic Web (Preprint), 1–45 (2019)
- <span id="page-14-7"></span>7. Cebiri´c, ˇ S., Goasdou´e, F., Kondylakis, H., Kotzinos, D., Manolescu, I., Troullinou, ˇ G., Zneika, M.: Summarizing semantic graphs: a survey. The VLDB Journal 28(3), 295–327 (2019)
- <span id="page-14-0"></span>8. Desimoni, F., Po, L.: Empirical evaluation of linked data visualization tools. Future Gener. Comput. Syst. 112, 258–282 (2020)
- <span id="page-14-3"></span>9. Desimoni, F., Po, L.: Empirical evaluation of linked data visualization tools. Future Generation Computer Systems 112, 258–282 (2020)
- <span id="page-14-1"></span>10. Dud´as, M., Lohmann, S., Sv´atek, V., Pavlov, D.: Ontology visualization methods and tools: a survey of the state of the art. Knowl. Eng. Rev. 33, e10 (2018)

- 16 L. Asprino et al.
- <span id="page-15-0"></span>11. Gangemi, A., Presutti, V.: Ontology design patterns. In: Handbook on ontologies, pp. 221–243 (2009)
- <span id="page-15-17"></span>12. He, X., Zhang, R., Rizvi, R., Vasilakes, J., Yang, X., Guo, Y., He, Z., Prosperi, M., Huo, J., Alpert, J., et al.: Aloha: developing an interactive graph-based visualization for dietary supplement knowledge graph through user-centered design. BMC medical informatics and decision making 19(4), 1–18 (2019)
- <span id="page-15-12"></span>13. Hitzler, P., Gangemi, A., Janowicz, K., Krisnadhi, A.A., Presutti, V.: Towards a simple but useful ontology design pattern representation language. In: Proc of WOP@ISWC (2017)
- <span id="page-15-15"></span>14. Horn, R.E.: Visual language. MacroVu Inc. Washington (1998)
- <span id="page-15-6"></span>15. Huynh, D.F., Karger, D.R., Miller, R.C.: Exhibit: lightweight structured data publishing. In: Proc of WWW. pp. 737–746 (2007)
- <span id="page-15-18"></span>16. Khalili, A.: Linked data reactor: a framework for building reactive linked data applications. In: Proc of SemDev@ESWC (2016)
- <span id="page-15-14"></span>17. K¨ohler, W.: Gestalt psychology. Psychologische Forschung 31(1), XVIII–XXX (1967)
- <span id="page-15-8"></span>18. Luggen, M., Gschwend, A., Anrig, B., Cudr´e-Mauroux, P.: Uduvudu: a graph-aware and adaptive ui engine for linked data. In: Proc of LDOW@WWW (2015)
- <span id="page-15-10"></span>19. McBrien, P., Poulovassilis, A.: A conceptual modelling approach to visualising linked data. In: Proc of OTM. pp. 227–245 (2019)
- <span id="page-15-3"></span>20. Motta, E., Mulholland, P., Peroni, S., d'Aquin, M., Gomez-Perez, J.M., Mendez, V., Zablith, F.: A novel approach to visualizing and navigating ontologies. In: Proc of ISWC. pp. 470–486 (2011)
- <span id="page-15-1"></span>21. Nuzzolese, A.G., Presutti, V., Gangemi, A., Peroni, S., Ciancarini, P.: Aemoo: Linked data exploration based on knowledge patterns. Semantic Web 8(1), 87–112 (2017)
- <span id="page-15-16"></span>22. Patterson, R.E., Blaha, L.M., Grinstein, G.G., Liggett, K.K., Kaveney, D.E., Sheldon, K.C., Havig, P.R., Moore, J.A.: A human cognition framework for information visualization. Computers & Graphics 42, 42–58 (2014)
- <span id="page-15-4"></span>23. Peroni, S., Motta, E., d'Aquin, M.: Identifying key concepts in an ontology, through the integration of cognitive principles with statistical and topological measures. In: Proc of ASWC. pp. 242–256 (2008)
- <span id="page-15-2"></span>24. Po, L., Malvezzi, D.: High-level visualization over big linked data. In: Prof of ISWC (P&D/Industry/BlueSky) (2018)
- <span id="page-15-11"></span>25. Presutti, V., Gangemi, A.: Content ontology design patterns as practical building blocks for web ontologies. In: Proc of ER. pp. 128–141 (2008)
- <span id="page-15-9"></span>26. Thellmann, K., Galkin, M., Orlandi, F., Auer, S.: Linkdaviz–automatic binding of linked data to visualizations. In: Proc of ISWC. pp. 147–162 (2015)
- <span id="page-15-13"></span>27. Troullinou, G., Kondylakis, H., Stefanidis, K., Plexousakis, D.: Exploring rdfs kbs using summaries. In: Proc of ISWC. pp. 268–284 (2018)
- <span id="page-15-5"></span>28. Troullinou, G., Kondylakis, H., Stefanidis, K., Plexousakis, D.: Rdfdigest+: A summary-driven system for kbs exploration. In: Proc of ISWC (P&D/Industry/BlueSky) (2018)
- <span id="page-15-7"></span>29. Wang, X., Xin, Y., Xu, Q.: Template-based sparql query and visualization on knowledge graphs. In: Proc of DASFAA. pp. 184–200 (2018)
