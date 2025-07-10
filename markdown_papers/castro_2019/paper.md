cite_key: castro_2019
title: Research Knowledge Graphs: the Shifting Paradigm of Scholarly Information Representation
authors: Leyla Jael Castro, Benjamin Zapilko, Saurav Karmakar, Brigitte Mathiak, Markus Stocker, Wolfgang Otto
year: 2019
doi: 10.15488/13072
url: https://doi.org/10.15488/13072
relevancy: Medium
relevancy_justification: Contains relevant concepts applicable to HDM systems
tags:
  - ai
  - healthcare
  - heterogeneous
  - integration
  - knowledge_graph
  - llm
  - machine_learning
  - ontology
  - personal
  - semantic
  - survey
date_processed: 2025-07-02
phase2_processed: true
original_folder: arxiv_2506.07285_Research_Knowledge_Graphs_the_Shifting_Paradigm_o
images_total: 1
images_kept: 1
images_removed: 0
keywords: 
---

# Research Knowledge Graphs: the Shifting Paradigm of Scholarly Information Representation

Matthäus Zloch1,<sup>2</sup> , Danilo Dessì<sup>3</sup> , Jennifer D'Souza<sup>4</sup> , Leyla Jael Castro<sup>5</sup> , Benjamin Zapilko<sup>1</sup> , Saurav Karmakar<sup>1</sup> , Brigitte Mathiak<sup>1</sup> , Markus Stocker<sup>4</sup> , Wolfgang Otto<sup>1</sup> , Sören Auer<sup>4</sup> , and Stefan Dietze1,<sup>2</sup>

<sup>1</sup> GESIS – Leibniz Institute for the Social Sciences, Köln, Germany firstname.lastname@gesis.org

<sup>2</sup> Heinrich-Heine-University, Düsseldorf, Germany

firstname.lastname@hhu.de

<sup>3</sup> Department of Computer Science, College of Computing and Informatics,

University of Sharjah, UAE

ddessi@sharjah.ac.ae

<sup>4</sup> TIB – Leibniz Information Centre for Science and Technology, Hannover, Germany firstname.lastname@tib.eu <sup>5</sup> ZB MED – Information Centre for Life Sciences, Köln, Germany

ljgarcia@zbmed.de

Abstract. Sharing and reusing research artifacts, such as datasets, publications, or methods is a fundamental part of scientific activity, where heterogeneity of resources and metadata and the common practice of capturing information in unstructured publications pose crucial challenges. Reproducibility of research and finding state-of-the-art methods or data have become increasingly challenging. In this context, the concept of Research Knowledge Graphs (RKGs) has emerged, aiming at providing an easy to use and machine-actionable representation of research artifacts and their relations. That is facilitated through the use of established principles for data representation, the consistent adoption of globally unique persistent identifiers and the reuse and linking of vocabularies and data. This paper provides the first conceptualisation of the RKG vision, a categorisation of in-use RKGs together with a description of RKG building blocks and principles. We also survey real-world RKG implementations differing with respect to scale, schema, data, used vocabulary, and reliability of the contained data. We also characterise different RKG construction methodologies and provide a forward-looking perspective on the diverse applications, opportunities, and challenges associated with the RKG vision.

## TL;DR
Research on research knowledge graphs: the shifting paradigm of scholarly information representation providing insights for knowledge graph development and data integration.

## Key Insights  
Contributes to the broader understanding of knowledge graph technologies and data management practices relevant to PKG system development.

Keywords: knowledge graphs · information representation · scholarly knowledge · open science · linked data

2 M. Zloch, D. Dessì, J. D'Souza, L. Castro, B. Zapilko, S. Karmakar et al.

## 1 Introduction - Open Science Challenges

The scientific process constantly produces and consumes scientific resources, such as publications, datasets, research methods, software, machine learning models, and discipline-specific research instruments. That has led to an ever-growing amount of research artifacts, where finding, understanding, and reusing them is crucial to scientists' daily activities. The widespread availability of diverse datasets and significant advancements in computational capabilities have led to the adoption of data science and artificial intelligence techniques across various research fields and disciplines. Deep learning methods, in particular, have become the dominant approach in research areas such as natural language processing and image analysis. These methods typically involve a combination of code, machine learning models, and training data. The lack of transparency about dependencies and relations between such resources has led to a reproducibility crisis, where reproducing research and determining the state of the art has become increasingly challenging [12].

To help researchers find, share, and reuse such resources, there is a need for infrastructures incorporating appropriate techniques to structure such information. In recent years, a number of platforms and services have emerged, aiming at organizing different types of information. These include bibliographic databases such as DBLP<sup>6</sup> , SCOPUS<sup>7</sup> , and Web of Science<sup>8</sup> , dataset portals such as DataCite<sup>9</sup> , Zenodo<sup>10</sup> or da|ra<sup>11</sup>, code sharing portals such as GitHub<sup>12</sup>, or bibliographic search engines such as Google Scholar<sup>13</sup>. While such services usually focus on artifacts of particular types (e.g., either publications or research datasets), dependencies between artifacts of different types are crucial to better understand the provenance, the context of individual resources, and how they relate to each other, e.g., how a specific dataset was produced or what methods contributed to a specific finding. Such relations are usually not reflected as part of the aforementioned infrastructures.

Despite recent efforts by the research community to get datasets and software recognized as first-class citizens (e.g., cited on their own), unstructured scholarly publications remain the primary source of scientific insight. As a result, knowledge about scientific advancements and resource dependencies is often buried within these unstructured documents, with Portable Document Format (PDF) being the standard format for sharing such information. Extracting and utilizing this knowledge as part of the scientific process is a laborious and time-consuming task [25].

<sup>12</sup> https://github.com

<sup>6</sup> The dblp computer science bibliography, https://dblp.org

<sup>7</sup> Scopus - the abstract and citation database, https://www.scopus.com/

<sup>8</sup> https://clarivate.com/products/scientific-and-academic-research/researchdiscovery-and-workflow-solutions/webofscience-platform/

<sup>9</sup> https://datacite.org/

<sup>10</sup> https://zenodo.org/

<sup>11</sup> https://www.da-ra.de/

<sup>13</sup> https://scholar.google.com

![](_page_2_Figure_1.jpeg)
<!-- Image Description: The image presents a conceptual framework for Research Knowledge Graphs (RKGs). A central hexagon depicts RKG components: datasets, publications, organizations, annotations/expressions, software, events, authors, presentations, and ML models, categorized by scientific domain. A flowchart illustrates RKG creation methods (manual, rule-based, deep learning) and types (curated vs. automatically generated), showing data flow between community expressions and primary research data. Finally, logos represent example RKG services. The image visually summarizes RKG creation, types, and related resources. -->

Figure 1. The figure illustrates examples of scholarly artifacts, methodologies to build RKGs, the five categories described in this paper, and examples of well-known services built on top.

To address these challenges, the research community has begun to design and develop Knowledge Graphs (KGs), i.e., networks of machine-readable, semantically rich, interlinked descriptions of entities and their relationships, usually expressed as graph-based databases either as Resource Descriptor Framework (RDF) triples or property graphs. To enhance the interoperability and understanding of Knowledge Graphs, researchers employ standardized vocabularies and ontologies, defining a common set of terms within a specific domain. This semantic layer facilitates consistent interpretation and communication. Furthermore, they use Persistent Identifiers (PIDs) providing a unique and persistent way to reference and retrieve specific resources and ensuring their long-term stability and accessibility.

This paper investigates, describes, and categorizes KGs of research artifacts (e.g., methods, datasets, research papers) and entities (e.g., paper authors, organizations) [33, 9, 16] within the scholarly domain; we refer to them as Research Knowledge Graphs (RKGs). They stand as a transformative technology for the scholarly landscape, aiming in the long term at simplifying the way scientific outcomes are represented and utilized. Notable examples are OpenAlex [30], the Microsoft Academic Graph [11], the GESIS Knowledge Graph<sup>14</sup>, and Springer SciGraph<sup>15</sup>, holding scholarly metadata information about research publications, research data, and authors. Another more recent example is the Open Research Knowledge Graph (ORKG) [16] that includes aspects such as research objectives and research problems. SoftwareKG [34] is an RKG representing software usage and citations in scholarly works. Beyond these examples, RKGs like TweetsKB [10] and ClaimsKG [36] offer a different focus, containing interlinked and semantically annotated research data. These RKGs serve research purposes, such

<sup>14</sup> https://data.gesis.org/gesiskg

<sup>15</sup> https://communities.springernature.com/users/82895-sn-scigraph

as the long-term collection of tweets [10], and the presentation of factual information alongside ratings extracted from fact-checking websites [36, 13].

By representing relationships between research artifacts and scholarly domain entities through machine-actionable data structures [25], RKGs not only enhance data reusability but also empower machine-driven applications, encouraging new paths for scientific exploration and analysis. Well-structured RKGs enable researchers to trace data lineage, efficiently identify appropriate methods, and assess result validity. For publishers, RKGs offer structured representations of research contributions, facilitating indexing and discovery. Citizen scientists and open science initiatives similarly benefit from increased transparency and structured access to scholarly knowledge. One more key aspect is their compliance with the Findable, Accessible, Interoperable, Reproducible (FAIR) principles [39] which enhances the appeal of RKGs to diverse stakeholders interested in exploring, accessing, and making use of scholarly knowledge. However, the development and usage of RKGs vary widely, originating from diverse data sources and employing different methodologies. This paper delves into this world, exploring RKGs' significance, applications, and challenges, to provide a comprehensive understanding of their pivotal role in advancing scholarly knowledge. Figure 1 sketches the outlook our paper describes; on the left side the reader can observe scholarly entities and research artifacts RKGs target, on the right side, the existing types and nature, and in the middle the processes that can be used to generate them. The next sections further delve into these aspects. More precisely, to understand the variety of uses RKGs can offer Section 2 provides prominent examples of RKGs, analyzing their diverse nature. In Section 3, the focus shifts to the methodologies to build RKGs and highlights the related challenges. RKGs' role in reshaping the scholarly information representation paradigm is a topic delved further in Section 4, which emphasizes the need for standardized approaches and outlooks future perspectives. Finally, Section 5 concludes the paper and remarks on the role of RKGs in the Scholarly Domain future.

### 2 Conceptualization of Scholarly Knowledge

To provide an overview of the types of RKGs within the scholarly domain, the following categorization system will help us to characterize existing RKGs based on the dimensions of data quality, but also with regard to changes to the schema, data growth, vocabulary reuse, and graph inter-connectedness. The dimensions are grounded in observations of existing RKG implementations and their role in different scholarly infrastructural projects (institutions and products are mentioned in the corresponding sections). Table 1 shows an overview of the five categories and a comparison using RKGs' features over the five dimensions.

1. Scholarly resource metadata Scholarly metadata resources and services serve as the primary access point for researchers to search for publications and associated artifacts. They facilitate bibliometric studies, perform research assessments, and effective research management. Managed by organizations focused on (i) providing access to preserved research artifacts, (ii) collecting, aligning, and aggregating metadata from various publishers, and (iii) investigating specific research aspects or use cases, these resources are characterized by high-quality, curated content contributed by (a) researchers describing their work and (b) publishers ensuring proper quality control, indexing, and discoverability/findability of research artifacts. The schema used by these resources is stable, facilitating the development of research engines and services. However, the metadata vocabulary may vary depending on the organization and its focus. These resources expand over time and receive periodical updates. Validation is typically conducted by cross-referencing metadata with authoritative sources (e.g., CrossRef, ORCID) and leveraging expert curation. Examples of single-organization metadata resources include SciGraph<sup>16</sup>, primarily encompassing SpringNature publications, and CultureGraph<sup>17</sup>, provided by the Deutsche Nationalbibliothek, linking library network metadata from Germany and Austria, along with the German National Library. Examples of aggregated resources are ResearchGraph<sup>18</sup> , a nonprofit metadata organization initiative closely aligned with the Research Data Alliance; OpenAIRE Research Graph<sup>19</sup> and OpenAlex<sup>20</sup>, which provide integrated metadata about funders, organizations, researchers, research communities, and publishers; and PID Graph<sup>21</sup>, which is a DataCite service that uses a GraphQL interface to enable integrated metadata searches on entities like datasets, publications, and people. Examples of metadata resources designed for more specific use cases are WikiCite/Scholia<sup>22</sup>, a Wikimedia project for organizing bibliographic information and researcher profiles for Wikipedia/Wikidata; and OpenCitations<sup>23</sup>, which is an infrastructure dedicated to the publication of open bibliographic and citation data. An example of a domain-specific RKG is the GESIS KG<sup>24</sup> which comprises metadata of over 450,000 scientific resources (datasets, publications, variables, and survey instruments) from the social sciences and its semantic relationships in an integrated and consistent form and makes them accessible for reuse. This RKG serves also as a backbone for the GESIS Search<sup>25</sup> .

2. Quality-controlled ground truth data For many scholarly information extraction (IE) tasks, the availability of ground truth datasets is limited. Typically, publications related to scholarly IE tasks provide a ground truth dataset, a trained model on that dataset, and an automatically generated RKG. Alternatively, they might introduce a novel, fine-tuned model based on another

<sup>16</sup> https://communities.springernature.com/users/82895-sn-scigraph <sup>17</sup> CultureGraph:

https://www.dnb.de/DE/Professionell/Standardisierung/AGV/\_content/culturegraph\_akk.html

<sup>18</sup> ResearchGraph: https://researchgraph.org

<sup>19</sup> OpenAIRE: https://graph.openaire.eu

<sup>20</sup> OpenAlex: https://docs.openalex.org/

<sup>21</sup> PID Graph: https://api.datacite.org/graphql

<sup>22</sup> WikiCite/Scholia: http://wikicite.org and https://scholia.toolforge.org/

<sup>23</sup> OpenCitations: https://opencitations.net/

<sup>24</sup> https://data.gesis.org/gesiskg/

<sup>25</sup> https://search.gesis.org/

| Category | Scale | Schema | Data | Vocabulary | Connectedness |
|----------------------|--------------|--------------|-------------|------------------------|---------------|
| 1. Scholarly<br>re | medium | fixed<br>and | evolving | well-defined, | high |
| source metadata | | stable | | focused subset | |
| 2. Quality | small | fixed<br>and | stable | well-defined, | high |
| controlled | | stable | | focused subset | |
| ground<br>truths | | | | | |
| data | | | | | |
| 3. RKGs<br>of<br>pri | varies, po | potentially | stable | focused subset varies, | poten |
| mary<br>research | tentially | fixed<br>and | | | tially high |
| data | large | stable | | | |
| 4. Community | medium | evolving | evolving | recommended/ | local, varies |
| expressions<br>of | | openly, | | used,<br>not<br>en | |
| scholarly<br>arti | | template | | forced | |
| facts | | design | | | |
| 5. Automatically | large (e.g., | fixed<br>and | potentially | focused subset high | |
| generated | 300M) | stable | evolving | | |
| RKGs<br>focusing | | | | | |
| on scholarly ar | | | | | |
| tifact relations | | | | | |

Table 1. Overview of the introduced qualitative categories for research knowledge graphs.

pre-trained model, demonstrating superior performance through transfer learning. Datasets in this category are crucial for quality assurance checks during machine learning model training for downstream tasks. High-quality datasets in this category are usually annotated, curated , and validated by humans (trained crowd-workers, students, postdocs, domain experts) and employ controlled metrics, such as Fleiss' κ or Cohen's κ, to measure inter-annotator agreements. However, manual annotation is resource-intensive and time-consuming. Therefore, datasets in this category tend to be smaller and fewer compared to other categories. Their schemas remain fixed and stable, and the data remains static unless a new version is published under a (new) persistent identifier (PID) for reference purposes. Whenever ground truth data is stored in an RKG (either natively or via programmatic generation), the data becomes more connected and meaningful thanks to the use of existing (controlled) vocabularies and PIDs that can later connect other RKGs. Notable examples of such ground truth data in the form of RKGs include Software Mentions in Science (SoMeSci) [32] and a specialized corpus for scientific literature entity tagging of tasks, datasets, and metrics, namely TDMSci [15].

3. RKGs representing and enriching primary research data Contrary to scholarly resource metadata, this category of research knowledge graphs contains primary research data (first-party data) collected directly by researchers, representing actual scientific domain knowledge. These RKGs primarily serve researchers seeking specific research data pertinent to their discipline, such as sensor data from physical experiments or Twitter data for studying evolving opinions on topics in the Social Sciences domain. Similar to automatically (NLP- )generated RKGs (last category), these RKGs undergo quality control to ensure transparency regarding the accuracy of specific information or features. Examples of validation methods include analysis of experimental results to ensure alignment with current research, expert review, and reproducibility checks. The size of RKGs representing primary research data can be quite large, depending upon the domain and the scope of the data. Typically, the schema remains fixed and stable, with vocabulary reused whenever possible (e.g., NIF<sup>26</sup>, DCAT<sup>27</sup> , schema.org<sup>28</sup>). Access to these graphs is often provided via assigned and public DOIs. The connectedness of such graphs (graph density) is influenced by the applied collection method and the utilization of the underlying vocabulary. Examples of research knowledge graphs containing primary research data can be found in [10, 20].

4. Community-expressions of scholarly artifacts This category includes RKGs built with significant manual support from the scientific community, rather than primarily through automatic extraction from scholarly publications. However, those solutions offer automatic, NLP-powered services to aid users in uploading or entering semi-structured scientific content. Their primary objective is to enhance the visibility and discoverability of scholarly knowledge, making them particularly valuable for researchers seeking (semi-automatically) access to scholarly information. The nature of such graphs is cross-domain, facilitating the creation of tabular summaries (leaderboards) featuring state-of-the-art works across diverse disciplines. Unlike automated extraction methods requiring manual triggers for updates, community-driven RKGs tend to remain more up-to-date. Nevertheless, such solutions may suffer from low quality in some sections due to community-driven vocabulary usage without quality assurance mechanisms. Continuous community involvement contributes to improving data quality over time. In fact, validation is obtained through consensus and crowdsourced mechanisms such as post-publication peer review. Vocabulary (re-)use depends on additional services provided by the systems, resulting in a flexible and continually evolving schema, especially when new data is introduced. The level of entity inter-connectedness in such graphs can vary from low to high and may exhibit clustering. An example of such a system is the previously mentioned ORKG [3], which aims to describe research papers in a structured way.

5. Automatically generated RKGs focusing on scholarly artifact relations This group comprises automatically generated RKGs, often produced through an NLP end-to-end pipeline, employing various deep learning technologies for tasks such as data cleaning, disambiguation, integration, named entity recognition and linking, and quality assessment. RKGs in this category focus on scholarly artifacts and their relationships. Typical use cases include employment

<sup>26</sup> https://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core/nif-core.html

<sup>27</sup> https://www.w3.org/TR/vocab-dcat-2/

<sup>28</sup> https://schema.org/

in productive systems, such as scholarly search systems, for analyzing aspects like citation habits and patterns or competing solutions to NLP tasks. Users of these RKGs typically include researchers interested in scholarly information, or specific scholarly artifacts, like datasets, ML models, and software code repositories. Because of potential errors in automatic generation pipelines, the generated RKGs are in need of quality controls, in order to ensure transparency regarding the accuracy of specific information. As RKGs in this category can be created using pre-trained models fine-tuned on a variety of sources, they can scale to include hundreds of millions of triples. Validation is often performed using precision-recall analysis on top of smaller manually curated datasets and domain-expert verification of a portion of extracted relationships. The schema for these RKGs is typically fixed and stable, as schema elements are not necessarily dynamic in the pipeline processes. Consequently, the vocabulary tends to concentrate on a particular subset of entity types like publications, software, models, and other research artifacts. While they may not be initially expressed in RDF, their structure and metadata can be easily annotated using vocabularies from schema.org, as well as formulated in accordance with schemas such as NIF and DCAT. Notable examples of such research knowledge graphs include SoftwareKG [34, 33] and CS-KG [9].

### 3 Methods for Constructing RKGs

Construction of RKGs relies on both manual effort and machine-based extraction and data lifting, where methods are applied and combined depending on the nature and characteristics of the RKG to be generated. While some entities, like articles and datasets, have readily available metadata that can be transformed to fit RKG requirements, extracting content from sources like Twitter or scientific literature is more complex. A particular focus of RKGs is on identifying and explicitly representing relations between different artifacts. Typical examples include dataset citations or method citations, that capture relations between datasets (methods) and publications or even between datasets and methods if citations are found in the same scholarly work [34, 32, 25].

Manual RKG generation For the case of scientific information originally expressed in scientific literature, manual production can occur pre- or postpublication of the original work while automated extraction occurs only postpublication. Post-publication manual production is "crowdsource" content, whereby contributors in the roles of authors or readers of original work manually produce structured expressions of the scientific information published originally in articles. By contrast, pre-publication manual production occurs by integrating the production of machine-actionable knowledge into the research data lifecycle, specifically data analysis, and can be heavily supported by infrastructure in order to automate most aspects of the task [7].

Rule-based RKG extraction Generally, automated RKG construction involves turning unstructured scientific article text into structured entities and

relations, and then republishing it in the form of graphs. The structuring can be based on an ontology or driven by NLP corpora. For instance, as an interdisciplinary RKG construction system, Research Spotlight [29] leverages the Scholarly Ontology (SO) [28] which models research practices representing the information for "who does what, when, and how" in an RKG, for ontology-driven structured information extraction. The methodology is rule-based and applied on a database of scholarly articles. First, article metadata is mapped as SO instances via rules. The raw text undergoes sentence segmentation and entity extraction via an NER module. Relations are then generated using rules based on dependency trees, POS tags, SO semantic rules, and proximity constraints. Finally, URIs are created for the SO namespace and linked to relevant DBpedia entities for publication as linked data.

Deep Learning-based RKG extraction Early systems followed a similar rule-based pipeline as discussed above, however with the advent of the "deep learning tsunami" [21] the KG construction pipelines incorporated neural learning methods. A generalized architecture is neural and symbolic involving a pipeline of complementary deep learning and rule-based solutions at various levels in the knowledge composition workflow. The CS-KG system [8] is a relevant exemplar of neural-symbolic RKG construction. It integrates the DyGIEpp deep learning module [38], which works within the transformers architecture [17] for predefined entity and relation extraction. Additionally, it uses the Computer Science Ontology classifier (CSO-C) [31] for further entity extraction. The Stanford Core NLP suite's OpenIE [2] determines open domain relations, and the Stanford POS Tagger [22] identifies verbs between entity pairs as relation candidates. As alternative or complementary components, the NER and relation extraction tasks for RKG construction can be addressed by finetuning transformer models based on the Bidirectional Encoder Representations from Transformers (BERT) architecture [17] on downstream task application corpora such as the NER or RE datasets discussed in Section 3. BERT offers pretrained parameters from large-scale general domain corpora such as Wikipedia or books trained with the masked language model objective producing language models capable of natural language understanding. The finetuning procedure then simply involves initializing the desired language model with the pretrained NLU models parameters and further in the context of task-specific architectures tuning the probabilistic parameters for a downstream extraction task given task-specific datasets. As such for the scientific domain, the widely used transformer language models are SciBERT [5], PubMedBERT [14], SemMedDB [18], BioBERT [19], BioClinical-BERT [1], and BlueBERT [27]. In the realm of works around RKG construction, it is not uncommon to also leverage external knowledge bases as entity and relation extraction and linking candidates. This is the approach commonly witnessed in biomedicine. For instance, the iASiS knowledge graph [37] from biomedical data including scholarly publications on Lung Cancer and Dementia is generated utilizing NLP techniques coupled with the standardized biomedical ontologies such as UMLS [6] to annotate their extracted entities and relations. This latter system practically demonstrates the discovery of interactions between drugs in the treatments prescribed to lung cancer patients. As a final exemplar, in the domain of Biodiversity Science, OpenBioDiv [26] is a knowledge graph from scholarly articles published by Pensoft<sup>29</sup> and Plazi<sup>30</sup> that is structured by the OpenBiodiv-O ontology [35] for knowledge management. Thus, the themes of knowledge graphs vary between domain-specific subjects such as diseases in biomedicine or plant treatments in biodiversity, or domain-independent subjects such as research activity. While scientific articles are stored in silos isolated from each other, RKGs demonstrate how this is overcome by semantically combining different units of information.

### 4 Outlook

Representing data in the form of graphs can open new doors for better managing and making sense of produced research artifacts. This section looks at the RKGs' benefits and incentives and outlines their perspectives.

Research Management, FAIRness, and Consensus RKGs offer researchers and practitioners the possibility to describe research artifacts using established vocabularies and ontologies. These can enable several benefits, especially when well-established vocabularies are reused. For example, some RKGs model artifacts using schema.org, making them more visible, searchable, and findable to widely used search engines such as Google Search but also specific-purpose aggregators (e.g., the dataset search provided by the Australian Research Data Commons). In addition, well-established vocabularies also allow describing entities with rich metadata ensuring that this can be provided to the search engines for richer and better results. Standardized vocabularies simplify artifact update and maintenance while enabling clear and consistent research management (e.g., data and software management) and reducing the chances of introducing errors and inconsistencies. Finally, describing research artifacts with these technologies makes them more valuable due to a shared understanding and better integration and interoperability. Using well-established vocabularies with a broad scope, such as schema.org, already encouraged by recent RKGs e.g., SoMeSci and SoftwareKG, can promote effective governance by creating a common framework for data management, guaranteeing data quality, enabling findability and search on the web, and promoting community decision-making.

State-of-the-art Exploration and Enhanced Reproducibility Today, we are witnessing a reproducibility crisis and insufficient transparency is a growing concern: (i) many proposed solutions lack reproducibility due to unshared or unreported implementation details alongside traditional PDF publications, (ii) some machine learning models produce different outputs for the same input (e.g., generative large language models such as ChatGPT [24]) and cannot be explained due to their black-box nature, and (iii) keeping pace with the stateof-the-art is challenging; a large number of papers (and more and more also

<sup>29</sup> https://pensoft.net/

<sup>30</sup> http://plazi.org/

datasets and software) is published daily with no specific structure for searching specific relationships (e.g., find the performance of a given method on a specific dataset) leading several authors to adopt wrong baselines and claim themselves to be at the forefront of the field [12]. RKGs will be crucial to address these issues providing direct practical impact. First, RKGs can describe models along with their design parameters and results on certain tasks and datasets, facilitating their reproducibility (and to some extent transparency). Second, RKGs can provide explanations of black-box models, a direction already showing promising outcomes [4]. Finally, RKGs can bridge models with the tasks they are designed for, the datasets they are applied to, and the corresponding performance results, offering a comprehensive and connected global view of methods, tasks, data, and performance and easy access to the state of the art. For example, CS-KG can be used to i) discover uncommon scientific facts e.g., <home automation, usesMaterial, telegram>, ii) better understanding of computer science concepts e.g., <ontology, supportsTask, reasoning>, <ontology, supportsTask, semantic interoperability>, and iii) finding literature associated to a specific method and material such as <graph neural network, solvesTask, molecular property prediction>. This will enable researchers to better compare their solutions as well as reviewers to provide a more solid basis for evaluations during the review process. By adopting RKGs, the research community can take significant strides toward research reliability, mitigating the reproducibility and state-of-the-art crisis.

Research Knowledge Graph Integration RKGs are built with a focus on specific aspects or variables of interest and are suitable for specific use cases. As mentioned in the previous section, one advantage is their potential for interlinking, which widens RKG use cases and unlocks new knowledge generation. This feature sets RKGs apart from other data storage and usage technologies (e.g., databases or CSV files). RKGs, built using Semantic Web best practices, are web-accessible, utilize vocabularies and ontologies, employ non-proprietary formats, use permanent identifiers (PIDs) for entity identification, and enable links to internal and external research artifacts. Therefore, different RKGs can be explored using the same queries, simplifying information search across multiple RKGs and providing a common ground for interpreting results. Furthermore, several RKGs can represent the same entities but have different information about them. Linking RKGs allows users to collect various knowledge pieces about the same entity. For example, a user can first discover an author's papers from an RKG describing paper metadata, find links to NLP or community-expression RKGs describing the paper content, and discover the methods or dataset the author used. Interlinking RKGs opens the door to discovering a vast amount of new knowledge that is currently difficult to achieve due to the article-centric publishing paradigm.

Citability and Creditability of Research Artifacts Today, scholarly papers remain the most common form of referenced research artifacts ensuring their permanence in literature. There is an increasing demand to reference and cite other essential research artifacts. For example, ORCIDs are identifiers associated with researchers, DOIs (and PIDs) are used to identify datasets and software, and Research Organization Registry<sup>31</sup> (ROR) are used to identify organizations. However, many other research artifacts and entities require proper reference to enable their citability and credit to their owners. These encompass a wide range, such as machine learning models, methodologies, achieved results, and more. In this context, RKGs and their best practices in PIDs, i.e., longlasting stable URIs associated with entities, can serve for example as a tool for reliably and efficiently attributing researchers, such as identifying them as owners, developers, or maintainers of a particular machine learning model. Furthermore, researchers can be acknowledged for their role in methodologies, and the methodologies themselves can be cited. Moreover, PIDs enable the linking of methodologies to tasks they solve, thus allowing the generation of valuable connections among different research artifacts. RKGs can make research interconnected and traceable, thus paving the way for a more liable and integrated scholarly research paradigm.

Research Knowledge Graphs to Support Large Language Models With the recent advent of large language models (LLMs), researchers and professionals in various industries are increasingly incorporating this technology into their daily work routines. However, despite their impressive performance at first glance, LLMs come with several well-known limitations. These limitations include their high training and operational costs, challenges associated with maintenance and updates, tendencies to generate hallucinatory and inconsistent responses (depending on the language employed), and difficulties in tracing and attributing the sources of their answers. This is also problematic for the scholarly domain where LLMs can suggest fictional articles as well as misleading statistics (e.g., an erroneous citation count) [23]. Furthermore, LLMs are static in nature, as they are trained only once at a specific point in time, which hinders their ability to continuously evolve and adapt to the changing knowledge, particularly in scholarly domains where research is in constant flux, with researchers continuously adding, modifying, or removing findings.

In this context, RKGs take a pivotal role and serve as a verifiable source of truth to obtain up-to-date information. RKGs significantly enhance the capabilities of LLMs by facilitating the integration of language-independent knowledge, enabling fact verification, enhancing contextual understanding, providing domain-specific expertise, enabling personalization, and adeptly addressing complex queries.

### 5 Conclusion

This paper introduced RKGs as a transformative paradigm for storing, managing, and sharing research artifacts. By exploring types and construction methodologies underlying RKGs, we have outlined the transformative potential RKGs

<sup>31</sup> https://ror.org/

hold for scholarly information representation. Their adoption implies a profound shift in how scientists can conceptualize, organize, and interact with scholarly knowledge. By integrating disparate data sources and forming meaningful relationships, RKGs foster interdisciplinary collaboration and knowledge discovery. Scholars, researchers, and practitioners can benefit from linked data to explore complex research questions, identify emerging trends, and gain deeper insights into academic knowledge. Embracing this novel paradigm helps navigate the expanding knowledge landscape. Continued research and development of RKGs will refine our understanding and utilization of research artifacts unlocking new opportunities to address scientific challenges.

Acknowledgements. This work is partially supported by the DFG-funded project NFDI for Data Science & Artificial Intelligence (NFDI4DS, project number 460234259).

## References

- 1. Alsentzer, E., Murphy, J.R., Boag, W., Weng, W.H., Jin, D., Naumann, T., Redmond, W., McDermott, M.B.: Publicly available clinical bert embeddings. NAACL HLT 2019 p. 72 (2019)
- 2. Angeli, G., Premkumar, M.J.J., Manning, C.D.: Leveraging linguistic structure for open domain information extraction. In: Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing (Volume 1: Long Papers). pp. 344–354 (2015)
- 3. Auer, S., Oelen, A., Haris, M., Stocker, M., D'Souza, J., Farfar, K.E., Vogt, L., Prinz, M., Wiens, V., Jaradeh, M.Y.: Improving access to scientific literature with knowledge graphs. Bibliothek Forschung und Praxis 44(3), 516–529 (2020)
- 4. Balloccu, G., Boratto, L., Fenu, G., Marras, M.: Reinforcement recommendation reasoning through knowledge graphs for explanation path quality. Knowledge-Based Systems 260, 110098 (2023)
- 5. Beltagy, I., Lo, K., Cohan, A.: Scibert: Pretrained language model for scientific text. In: EMNLP (2019)
- 6. Bodenreider, O.: The unified medical language system (umls): integrating biomedical terminology. Nucleic acids research 32(suppl\_1), D267–D270 (2004)
- 7. Boubakri, Z.: The orkg r package and its use in data science (Nov 2022). https://doi.org/10.15488/13072, https://www.repo.unihannover.de/handle/123456789/13177
- 8. Dessì, D., Osborne, F., Recupero, D.R., Buscaldi, D., Motta, E.: Scicero: A deep learning and nlp approach for generating scientific knowledge graphs in the computer science domain. Knowledge-Based Systems 258, 109945 (2022)
- 9. Dessì, D., Osborne, F., Reforgiato Recupero, D., Buscaldi, D., Motta, E.: Cs-kg: A large-scale knowledge graph of research entities and claims in computer science. In: International Semantic Web Conference. pp. 678–696. Springer (2022)
- 10. Fafalios, P., Iosifidis, V., Ntoutsi, E., Dietze, S.: TweetsKB: A Public and Large-Scale RDF Corpus of Annotated Tweets. In: Gangemi, A., Navigli, R., Vidal, M.E., Hitzler, P., Troncy, R., Hollink, L., Tordai, A., Alam, M. (eds.) The Semantic Web. pp. 177–190. Springer International Publishing, Cham (2018)

- 14 M. Zloch, D. Dessì, J. D'Souza, L. Castro, B. Zapilko, S. Karmakar et al.
- 11. Färber, M.: The microsoft academic knowledge graph: A linked data source with 8 billion triples of scholarly data. In: The Semantic Web–ISWC 2019: 18th International Semantic Web Conference, Auckland, New Zealand, October 26–30, 2019, Proceedings, Part II 18. pp. 113–129. Springer (2019)
- 12. Ferrari Dacrema, M., Cremonesi, P., Jannach, D.: Are we really making much progress? a worrying analysis of recent neural recommendation approaches. In: Proceedings of the 13th ACM Conference on Recommender Systems. p. 101–109. RecSys '19, Association for Computing Machinery, New York, NY, USA (2019). https://doi.org/10.1145/3298689.3347058, https://doi.org/10.1145/3298689.3347058
- 13. Gangopadhyay, S., Schellhammer, S., Hafid, S., Dessi, D., Koß, C., Todorov, K., Dietze, S., Jabeen, H.: Investigating characteristics, biases and evolution of factchecked claims on the web. In: Proceedings of the 35th ACM Conference on Hypertext and Social Media. pp. 246–258 (2024)
- 14. Gu, Y., Tinn, R., Cheng, H., Lucas, M., Usuyama, N., Liu, X., Naumann, T., Gao, J., Poon, H.: Domain-specific language model pretraining for biomedical natural language processing. ACM Transactions on Computing for Healthcare (HEALTH) 3(1), 1–23 (2021)
- 15. Hou, Y., Jochim, C., Gleize, M., Bonin, F., Ganguly, D.: TDMSci: A specialized corpus for scientific literature entity tagging of tasks datasets and metrics. In: Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume. pp. 707–714. Association for Computational Linguistics, Online (Apr 2021). https://doi.org/10.18653/v1/2021.eaclmain.59, https://aclanthology.org/2021.eacl-main.59
- 16. Jaradeh, M.Y., Oelen, A., Farfar, K.E., Prinz, M., D'Souza, J., Kismihók, G., Stocker, M., Auer, S.: Open research knowledge graph: Next generation infrastructure for semantic scholarly knowledge. In: Proceedings of the 10th International Conference on Knowledge Capture. p. 243–246. K-CAP '19, Association for Computing Machinery, New York, NY, USA (2019). https://doi.org/10.1145/3360901.3364435, https://doi.org/10.1145/3360901.3364435
- 17. Kenton, J.D.M.W.C., Toutanova, L.K.: Bert: Pre-training of deep bidirectional transformers for language understanding. In: Proceedings of NAACL-HLT. pp. 4171–4186 (2019)
- 18. Kilicoglu, H., Shin, D., Fiszman, M., Rosemblat, G., Rindflesch, T.C.: Semmeddb: a pubmed-scale repository of biomedical semantic predications. Bioinformatics 28(23), 3158–3160 (2012)
- 19. Lee, J., Yoon, W., Kim, S., Kim, D., Kim, S., So, C.H., Kang, J.: Biobert: a pre-trained biomedical language representation model for biomedical text mining. Bioinformatics 36(4), 1234–1240 (2020)
- 20. Liu, C., Zhang, X., Xu, Y., Xiang, B., Gan, L., Shu, Y.: Knowledge graph for maritime pollution regulations based on deep learning methods. Ocean & Coastal Management 242, 106679 (2023). https://doi.org/https://doi.org/10.1016/j.ocecoaman.2023.106679,
- https://www.sciencedirect.com/science/article/pii/S0964569123002041 21. Manning, C.D.: Computational linguistics and deep learning. Computational Lin-
- guistics 41(4), 701–707 (2015) 22. Manning, C.D., Surdeanu, M., Bauer, J., Finkel, J.R., Bethard, S., McClosky, D.: The stanford corenlp natural language processing toolkit. In: Proceedings of 52nd annual meeting of the association for computational linguistics: system demonstrations. pp. 55–60 (2014)

Research Knowledge Graphs for Scholarly Information Representation 15

- 23. Meloni, A., Angioni, S., Salatino, A., Osborne, F., Recupero, D.R., Motta, E.: Integrating conversational agents and knowledge graphs within the scholarly domain. IEEE Access 11, 22468–22489 (2023)
- 24. OpenAI: Chatgpt (mar 14 version) (2024), https://chat.openai.com/, large language model developed by OpenAI
- 25. Otto, W., Zloch, M., Gan, L., Karmakar, S., Dietze, S.: GSAP-NER: A novel task, corpus, and baseline for scholarly entity extraction focused on machine learning models and datasets. In: Bouamor, H., Pino, J., Bali, K. (eds.) Findings of the Association for Computational Linguistics: EMNLP 2023. pp. 8166–8176. Association for Computational Linguistics, Singapore (Dec 2023), https://aclanthology.org/2023.findings-emnlp.548
- 26. Penev, L., Dimitrova, M., Senderov, V., Zhelezov, G., Georgiev, T., Stoev, P., Simov, K.: Openbiodiv: A knowledge graph for literature-extracted linked open data in biodiversity science. Publications 7(2), 38 (2019)
- 27. Peng, Y., Yan, S., Lu, Z.: Transfer learning in biomedical natural language processing: An evaluation of bert and elmo on ten benchmarking datasets. In: Proceedings of the 18th BioNLP Workshop and Shared Task. pp. 58–65 (2019)
- 28. Pertsas, V., Constantopoulos, P.: Scholarly ontology: modelling scholarly practices. International Journal on Digital Libraries 18(3), 173–190 (2017)
- 29. Pertsas, V., Constantopoulos, P.: Ontology-driven information extraction from research publications. In: International Conference on Theory and Practice of Digital Libraries. pp. 241–253. Springer (2018)
- 30. Priem, J., Piwowar, H., Orr, R.: Openalex: A fully-open index of scholarly works, authors, venues, institutions, and concepts. arXiv preprint arXiv:2205.01833 (2022)
- 31. Salatino, A., Osborne, F., Motta, E.: Cso classifier 3.0: a scalable unsupervised method for classifying documents in terms of research topics. International Journal on Digital Libraries 23(1), 91–110 (2022)
- 32. Schindler, D., Bensmann, F., Dietze, S., Krüger, F.: Somesci- a 5 star open data gold standard knowledge graph of software mentions in scientific articles. In: Proceedings of the 30th ACM International Conference on Information and Knowledge Management. p. 4574–4583. CIKM '21, Association for Computing Machinery, New York, NY, USA (2021). https://doi.org/10.1145/3459637.3482017, https://doi.org/10.1145/3459637.3482017
- 33. Schindler, D., Bensmann, F., Dietze, S., Krüger, F.: The role of software in science: a knowledge graph-based analysis of software mentions in pubmed central. PeerJ Computer Science 8 (2022)
- 34. Schindler, D., Zapilko, B., Krüger, F.: Investigating Software Usage in the Social Sciences: A Knowledge Graph Approach. In: Harth, A., Kirrane, S., Ngonga Ngomo, A.C., Paulheim, H., Rula, A., Gentile, A.L., Haase, P., Cochez, M. (eds.) The Semantic Web. pp. 271–286. Lecture Notes in Computer Science, Springer International Publishing, Cham (2020). https://doi.org/10.1007/978-3- 030-49461-2\_16
- 35. Senderov, V., Simov, K., Franz, N., Stoev, P., Catapano, T., Agosti, D., Sautter, G., Morris, R.A., Penev, L.: Openbiodiv-o: ontology of the openbiodiv knowledge management system. Journal of biomedical semantics 9(1), 5 (2018)
- 36. Tchechmedjiev, A., Fafalios, P., Boland, K., Gasquet, M., Zloch, M., Zapilko, B., Dietze, S., Todorov, K.: Claimskg: A knowledge graph of fact-checked claims. In: The Semantic Web–ISWC 2019: 18th International Semantic Web Conference, Auckland, New Zealand, October 26–30, 2019, Proceedings, Part II 18. pp. 309– 324. Springer (2019)

- 16 M. Zloch, D. Dessì, J. D'Souza, L. Castro, B. Zapilko, S. Karmakar et al.
- 37. Vidal, M.E., Endris, K.M., Jazashoori, S., Sakor, A., Rivas, A.: Transforming heterogeneous data into knowledge for personalized treatments—a use case. Datenbank-Spektrum 19, 95–106 (2019)
- 38. Wadden, D., Wennberg, U., Luan, Y., Hajishirzi, H.: Entity, relation, and event extraction with contextualized span representations. In: Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP). pp. 5784–5789 (2019)
- 39. Wilkinson, M.D., Dumontier, M., Aalbersberg, I.J., Appleton, G., Axton, M., Baak, A., Blomberg, N., Boiten, J.W., da Silva Santos, L.B., Bourne, P.E., et al.: The fair guiding principles for scientific data management and stewardship. Scientific data 3(1), 1–9 (2016)

## Metadata Summary
### Research Context
- **Research Question**: 
- **Methodology**: 
- **Key Findings**: 

### Analysis
- **Limitations**: 
- **Future Work**: