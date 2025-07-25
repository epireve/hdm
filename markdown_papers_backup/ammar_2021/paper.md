---
cite_key: ammar_2021
title: Using a Personal Health Library–Enabled mHealth Recommender System for Self-Management of Diabetes Among Underserved Populations: Use Case for Knowledge Graphs and Linked Data
authors: Nariman Ammar, James E Bailey, Robert L Davis, Arash Shaban-Nejad
year: 2021
doi: 10.2196/24738
url: https://doi.org/10.2196/24738
relevancy: High
relevancy_justification: Directly addresses HDM/PKG concepts with focus on personal data management
tags:
  - ai
  - children
  - federated
  - healthcare
  - heterogeneous
  - integration
  - knowledge_graph
  - machine_learning
  - ontology
  - pediatric
  - personal
  - privacy
  - semantic
date_processed: 2025-07-02
phase2_processed: true
original_folder: formative-2021-3-e24738
images_total: 18
images_kept: 18
images_removed: 0
keywords: 
---

# Original Paper

## Using a Personal Health Library–Enabled mHealth Recommender System for Self-Management of Diabetes Among Underserved Populations: Use Case for Knowledge Graphs and Linked Data

Nariman Ammar<sup>1</sup> , MSc, PhD; James E Bailey 2 , MD, MPH; Robert L Davis<sup>1</sup> , MD, MPH; Arash Shaban-Nejad<sup>1</sup> , MSc, MPH, PhD

<sup>1</sup>Oak Ridge National Laboratory Center for Biomedical Informatics, Department of Pediatrics, College of Medicine, The University of Tennessee Health Science Center, Memphis, TN, United States

<sup>2</sup>Center for Health System Improvement, College of Medicine, The University of Tennessee Health Science Center, Memphis, TN, United States

## Corresponding Author:

Arash Shaban-Nejad, MSc, MPH, PhD Oak Ridge National Laboratory Center for Biomedical Informatics, Department of Pediatrics College of Medicine The University of Tennessee Health Science Center 50 N Dunlap Street Memphis, TN, 38103 United States Phone: 1 901 287 5863 Email: [ashabann@uthsc.edu](mailto:ashabann@uthsc.edu)

## *Abstract*

**Background:**Traditionally, digital health data management has been based on electronic health record (EHR) systems and has been handled primarily by centralized health providers. New mechanisms are needed to give patients more control over their digital health data. Personal health libraries (PHLs) provide a single point of secure access to patients' digital health data and enable the integration of knowledge stored in their digital health profiles with other sources of global knowledge. PHLs can help empower caregivers and health care providers to make informed decisions about patients' health by understanding medical events in the context of their lives.
**Objective:**This paper reports the implementation of a mobile health digital intervention that incorporates both digital health data stored in patients' PHLs and other sources of contextual knowledge to deliver tailored recommendations for improving self-care behaviors in diabetic adults.
**Methods:**We conducted a thematic assessment of patient functional and nonfunctional requirements that are missing from current EHRs based on evidence from the literature. We used the results to identify the technologies needed to address those requirements. We describe the technological infrastructures used to construct, manage, and integrate the types of knowledge stored in the PHL. We leverage the Social Linked Data (Solid) platform to design a fully decentralized and privacy-aware platform that supports interoperability and care integration. We provided an initial prototype design of a PHL and drafted a use case scenario that involves four actors to demonstrate how the proposed prototype can be used to address user requirements, including the construction and management of the PHL and its utilization for developing a mobile app that queries the knowledge stored and integrated into the PHL in a private and fully decentralized manner to provide better recommendations.
**Results:**To showcase the main features of the mobile health app and the PHL, we mapped those features onto a framework comprising the user requirements identified in a use case scenario that features a preventive intervention from the diabetes self-management domain. Ongoing development of the app requires a formative evaluation study and a clinical trial to assess the impact of the digital intervention on patient-users. We provide synopses of both study protocols.
**Conclusions:**The proposed PHL helps patients and their caregivers take a central role in making decisions regarding their health and equips their health care providers with informatics tools that support the collection and interpretation of the collected knowledge. By exposing the PHL functionality as an open service, we foster the development of third-party applications or services and provide motivational technological support in several projects crossing different domains of interest.
*(JMIR Form Res 2021;5(3):e24738)*doi: [10.2196/24738](http://dx.doi.org/10.2196/24738)

## KEYWORDS

personal health library; mobile health; personal health knowledge graph; patient-centered design; personalized health; recommender system; observations of daily living; Semantic Web; privacy

## *Introduction*## Overview

Historically, medicine has been largely health care provider–centered rather than patient-centered [\[1](#page-17-0)[-3\]](#page-17-1). However, the new trend is moving toward incorporating patients' social and behavioral characteristics into electronic health records (EHRs) [[4\]](#page-17-2). This combination of medical, social, behavioral, and lifestyle information about the patient is essential to facilitate understanding of medical events in the context of one's life and, conversely, to allow lifestyle choices to be considered jointly with that patient's medical context [\[5](#page-17-3)]. This data is generated over time by patients, their caregivers, and their providers and is potentially useful to all parties for decision making [[6\]](#page-17-4). Patients are increasingly frustrated by the lack of EHR interoperability among fragmented systems and platforms dictated by providers or insurers, and they have expressed their needs to have an active role in managing their own health care data [[7-](#page-17-5)[12\]](#page-17-6). Improved interoperability and support for patient-provider communication have the potential to improve patient satisfaction and, evidence suggests, could even help detect and prevent medical errors [\[12](#page-17-6)].

In the field of personal digital health management, we often distinguish between a health*state*and a health*process*[[12\]](#page-17-6). Health*state*is a digital representation of the patients' health at a given point in time, including their prescribed and over-the-counter medications, test results, exercise regimens, diets, appointments with providers, and clinical outcomes. Patients also receive other digital health information through other communication modalities and from diverse sources. These data can often come in different formats depending on their source, including EHRs, family histories, data streams from activity trackers, published research documents and data sets, websites, social media platforms, and videos. A health state changes over time as data is acquired through ongoing processes and events embedded within those processes. A health-related intervention is a*process*, which could either be therapeutic or preventive. For instance, an intervention for self-management of diabetes mellitus (commonly referred to simply as diabetes) focused on promoting change or changes in health behavior to improve clinical outcomes is an example of a preventive intervention. Early interventions are the best way to prevent the progression of a negative health outcome to its end stage. Digital interventions through mobile Health (mHealth) apps can serve as an effective tool in chronic disease self-management [\[13](#page-17-7)]. An integrated *personal health library* (PHL) can facilitate the building of mHealth apps by maintaining a historical digital representation of a patient's health state from diagnosis to monitoring and integrating local knowledge about patients with global web-based knowledge while providing patients with full ownership of their digital health states. Applications can process the knowledge stored in the library to generate intelligent personalized interventions that can help improve patients' health state.

## Objective

We recently proposed both the conceptualization and initial implementation plan of a PHL [\[14](#page-17-8),[15\]](#page-17-9). The proposed PHL architecture [\(Figure 1](#page-2-0)) is the first of its kind to incorporate privacy, data ownership, integration, interoperability, portability, dynamic knowledge discovery, social determinants of health (SDoH) [\[16](#page-17-10)], and observations of daily living (ODLs) [\[5](#page-17-3)] into an end-to-end framework. In this paper, we provide a thematic assessment of patient requirements in a PHL, demonstrate how our proposed PHL meets these requirements, and describe an mHealth app that queries the PHL to deliver intelligent recommendations for improving self-care behaviors in diabetic adults.

![](_page_1_Picture_11.jpeg)
<!-- Image Description: The image is a simple text graphic showing "XSL-FO" in grey and "RenderX" in light purple below it. It likely serves as a visual identifier or logo within the paper, indicating the use of RenderX software, a XSL-FO processor, in the described methods or results. No diagrams, charts, graphs, or equations are present. The purpose is purely to denote a specific technology used in the research. -->

<span id="page-2-0"></span>**Figure 1.** A PHL that leverages the semantic technologies and decentralized privacy and security mechanisms of Social Linked Data (Solid) to enable true ownership, data integration, interoperability, portability, and dynamic knowledge discovery. The PHL enables building Hybrid mHealth Recommenders and Digital Librarians (HRDLs). ACL: access control list; API: application programming interface; Bp: blood pressure; DWPC: Diabetes Wellness and Prevention Coalition; ED: emergency department; LDN: Linked Data Notifications; LDP: Linked Data Platform; LOD: Linked Open Data; mHealth: mobile health; OWL: Web Ontology Language; PKG: personal knowledge graph; RDF: Resource Description Framework; REST: representational state transfer; SPARQL: SPARQL Protocol and RDF Query Language; WAC: Web Access Control.

![](_page_2_Figure_3.jpeg)
<!-- Image Description: This image depicts an architecture for a Personal Health Library (PHL). It shows PHL data distributed across Solid-enabled Personal Online Data Stores (PODs), integrating data from various sources including electronic health records (EHRs), regional health systems, and social media. The architecture utilizes REST APIs and knowledge graphs (KGs) in RDF format for data exchange and integration. Different data formats (CSV, RDF, HTML, PDF) and database systems are also illustrated, along with a "web of trust" encompassing devices, organizations, and individuals. The diagram's purpose is to visually represent the system's design and data flow. -->

## Review of Relevant Literature

To the best of our knowledge, little data exist on the implementation of PHLs. Barr et al [\[17](#page-17-11),[18\]](#page-18-0) proposed the Audio-PaHL project that utilizes text, audio, and image mining, natural language processing (NLP), and social network analysis to integrate audio-recordings of clinic visits into a library. They link medical terms that appear in the recordings to trustworthy patient resources, which can be retrieved, organized, edited, and shared by patients. Their project enables self-management in caregivers and older adults with multimorbidity. Several other researchers have utilized Semantic Web technologies and techniques to enhance EHRs or build research prototypes that can be integrated within clinical workflows. [Table 1](#page-3-0) describes some of the efforts in this area, including the rationale, the methods used, the health outcomes on which they focused, and whether they incorporate PHLs, SDoH, ODLs, and privacy. These works utilized a mix of Semantic Web and Machine Learning techniques. Most of these prior studies have predominantly focused on diabetes as the health outcome of interest. However, none of them incorporated privacy, SDoH, and ODLs in an integrated end-to-end framework.

![](_page_2_Picture_7.jpeg)
<!-- Image Description: The image simply displays the text "XSL-FO" stacked above "RenderX" in different colors and font styles. It likely serves to identify the specific XSL-FO processor (RenderX) used in the paper's experiments or implementation, providing crucial context for the reproducibility and understanding of the results. No charts, graphs, or equations are present. -->

<span id="page-3-0"></span>**Table 1.**Comparison with existing methods.

| Reference | Rationale | Method | Health outcome | Utilizes a<br>PHLa | Privacy<br>aware | Incorpo<br>rates<br>ODLsb | Incorpo<br>rates<br>SDoHc |
|------------------------|--------------------------------|----------------------------------------------------|----------------|--------------------|------------------|---------------------------|---------------------------|
| Audio-PaHL | Self-management | Audio text retrieval | Multiple | Yes | No | No | No |
| Barr et al [17,18] | | Natural Language Process<br>ing (NLP) | | | | | |
| | | Social Network Analysis | | | | | |
| d<br>PHD | EHRe<br>Enhancements | Collection of structured | Multiple | No | Yes | Yes | No |
| Backonja et al [19,20] | | data using standards and<br>protocols | | | | | |
| Ralston et al [21] | Self-management | Web-based Interactive<br>EHR | Diabetes | No | No | Yes | No |
| PerKApp [22] | Health promotion | Semantic inference and<br>knowledge representation | Diabetes | No | No | No | No |
| PHKGf<br>[23,24] | Health promotion | Semantic inference and<br>knowledge representation | Diabetes | No | No | No | No |
| kHealth | Early warning decision | Declarative knowledge- | Asthma | No | No | No | No |
| Sheth et al [25] | support system | based reasoning and ma<br>chine learning | | | | | |
| Seneviratne et al [26] | Disease characterization | Semantic inference and<br>knowledge representation | Breast cancer | No | No | No | No |
| Chari et al [27] | Treatment recommenda-<br>tions | Knowledge integration | Diabetes | No | No | No | No |

a PHL: personal health library.

<sup>b</sup>ODLs: observations of daily living.

c SDoH: social determinants of health.

d PHD: Project HealthDesign.

<sup>e</sup>EHR: electronic health record.

f PHKG: personal health knowledge graph.

## *Efforts to Enhance EHRs*There have been efforts to move EHRs from being mere data stores to being platforms that provide actionable information to patients, their caregivers, and health care providers. The Project HealthDesign program introduced ODLs as a major component of such enhanced EHR platforms [[5,](#page-17-3)[19](#page-18-1),[20\]](#page-18-2). Ralston et al describe a web-based disease self-management platform based on an interactive EHR that incorporates a diabetes module [[21\]](#page-18-3).

### *Applications for Promoting Healthy Behavior*Some standalone applications utilize semantic inference and knowledge representation capabilities for promoting healthy behavior. For example, the PerKApp [[22\]](#page-18-4) leverages augmented domain knowledge in ontologies as well as reasoning rules to implement a persuasive platform targeted toward health promotion in the workplace that monitors employees' dietary and physical activity habits and sends interactive messages to persuade them to change their behaviors. A few studies leverage the notion of a personal health knowledge graph (PHKG) for patients that enables them to monitor and self-manage their chronic diseases while incorporating their ODLs [[23,](#page-18-5)[24](#page-18-6)]. They utilize knowledge representation to define ontologies and perform intelligence tasks on top of Resource Description Framework (RDF) graphs.

## models [\[25](#page-18-7)]. They developed the kHealth project and deployed

it as an mHealth app for decision support in patients with asthma. Seneviratne et al developed a semantic end-to-end prototype for cancer characterization [[26\]](#page-18-8). Their tool utilizes a cancer staging ontology to aid physicians to quickly stage a new patient and identify risks, treatment options, and monitoring plans. Physicians can also restage existing patients or patient populations, allowing them to find patients whose stage has changed within a given patient cohort. They applied knowledge integration by converting a patient's EHR to an RDF knowledge graph and perform deductive reasoning to infer the stage of a tumor.
**Knowledge Integration for Disease Characterization:** Some researchers have combined statistical and machine learning approaches with knowledge representation approaches. For example, Sheth et al proposed a knowledge-enabled approach to health data analytics that combines declarative knowledge-based models with probabilistic machine learning

## *Applications for Treatment Recommendations Based on Cohort Characteristics*Chari et al utilized semantic technologies and knowledge graphs to implement a tool that allows users to quickly derive clinically relevant inferences about study populations [\[27\]](#page-18-9). They developed a prototype workflow that utilizes an ontology to

![](_page_3_Picture_18.jpeg)
<!-- Image Description: The image is a URL: https://formative.jmir.org/2021/3/e24738. This likely represents a link to a specific article or resource within the Journal of Medical Internet Research (JMIR) Formative platform, published in 2021, identified by the code "e24738". It serves as a reference to external material within the academic paper. -->

expose population descriptions in research studies through visual aids. Their goal is to enable physicians to better understand the applicability and generalizability of treatment recommendations within clinical practice guidelines.

## Innovative Technologies Used in The PHL Implementation

The PHL leverages several innovative technologies that were inspired by the requirements that we identified in the literature. We highlight some of the relevant efforts undertaken over time, including protocol specifications, vocabularies, standards, and technologies to support those requirements. We also introduce the terminology used throughout the paper, and in the results section we include several code snippets to illustrate these technologies.

## *Linked Open Data*An abundance of scientific evidence and open data sets are available on the Web in different formats. To enhance*discoverability*and*linkability*by enabling both humans and machines to access such data, Berners-Lee proposed the*Linked Open Data*(LOD) project, which aimed to make open data available on the Web as linked data (eg, Bio2RDF) [[28\]](#page-18-10). LOD is a way of connecting resources located throughout the Web by establishing a URI for each piece of data and explicitly stating how they are related to one another. LOD has led the research community to transform life sciences data sets into semantic format and make them available on the Web. LinkedCT, for example, is a ClinicalTrials.gov LOD data set that defines concepts related to diseases and interventions. The*Linked Open Research*(LOR) project leverages the LOD principles by providing an infrastructure to semantically represent research artifacts and to connect resources and the activity around them using notifications and visualizations to facilitate scientometric studies and decision making. By leveraging LOD, the proposed PHL simplifies the process of systematically and dynamically adding typed data relating to unique health and nonhealth concepts (eg, ODLs and SDoH) to the patients'digital health profiles, thereby*reducing the effort*needed for both patients and health care professionals to collect data and understand it, respectively. In addition, by leveraging the LOR initiative, the PHL enables physicians and patients to conduct scientific activities by combining global scientific knowledge discovered on the Web with local knowledge stored in their own library.

## *Web Annotation Specification*Annotations are typically used to convey information about a resource or associations between resources. The*Web Annotation*specification [[29\]](#page-18-11) describes a structured data model to enable annotations to be shared and reused across different platforms. It provides a specific format for creating annotations and consuming them based on a conceptual model and a set vocabulary of terms that accommodate a certain use case. One research challenge is to explore the potentially large number of annotations to discover patterns that capture semantic knowledge not only about individual nodes and their connections but also about groups of related nodes. For example, annotating clinical trials to look for patterns is an active research area [[30\]](#page-18-12), and there are open data sets that can be used for that purpose. Therefore, there is a need for more automatic tools to support scientists in pattern discovery, including link predictions or discovering complex patterns of annotation (eg across multiple disease conditions and drug interventions). By leveraging LOD, the PHL enables the mining of data sets that are semantically annotated with controlled vocabulary terms and concepts (eg, risk factors) and properties (eg, risk factors associated with a disease) encoded in ontologies. Through annotations, the PHL enables a user (eg, a physician) to convey information about a resource or associations between resources (eg, a tag on a lab test or image or a comment on a blog post about a research article). Annotations also help them capture scientific knowledge and use it as a basis for conducting focused literature reviews or planning new clinical trials.

## *Representational State Transfer*Representational state transfer (REST) is an architectural design pattern [\[31](#page-18-13)] for client-server communication that is centered around the following principles. First, each piece of content on the Web (both data and functionality) is considered a resource with a unique URI that provides a global addressing space for resource and service discovery. Second, resources are considered documents acted upon by Web application programming interface (API) operations (GET, POST, UPDATE, and DELETE) to manipulate those resources using HTTP as a communication protocol. Third, resources are decoupled from their representations, so their content can be accessed in a variety of formats (HTML, XML, JSON, plaintext, JPEG, PDF, etc). Finally, Web content should be designed as a network of resources that link to each other following the Hypermedia as the Engine of Application State principle. This principle enables discoverability using hypermedia controls that indicate to the resource requester a set of actions that are available to them on that resource as well as the URLs on which those actions can be performed. APIs using RESTful architecture have been widely adopted for software-to-software communication across heterogeneous distributed environments. RDF, the model driving the Linked Data Platform (LDP), follows the REST principles of identifying resources by URIs, which facilitates managing resources via HTTP operations on their URIs. It also enables hypermedia-based discovery [[32\]](#page-18-14). We follow this approach for adding, deleting, and updating resources in the PHL. However, our approach solves the lack of substitutability with non-native RESTful APIs in current EHR implementations, which often hinders systems programmed for a specific API task (eg, adding a resource to Cerner at Hospital 1) from performing that same task with another incompatible API (eg, adding that same resource to Cerner at Hospital 2). Solid adopts a pattern-based approach to API design that enables applications to be compatible with APIs beyond those for which they were explicitly programmed [[33\]](#page-18-15).

## *Web-Scale Semantic Querying*The LOD stack (RDF, URIs, and SPARQL [SPARQL Protocol and RDF Query Language]) makes any piece of data accessible and queryable on the Web. SPARQL can be used to execute federated queries across many endpoints on the Web. The most straightforward technique for accessing LOD data is following

a URL of an RDF document through a process called*dereferencing*, which involves using the HTTP protocol to retrieve a representation of a resource identified by a URL. SPARQL endpoints offer interfaces that permit selection of data in a granular way with the ability to perform complex data retrieval from multiple *personal online data stores*(PODs) via link-following SPARQL. Solid exposes data in a document-oriented way (RDF) and provides a uniform interface to query this data.

## *Federated Linked Data Querying*Federated queries are used to achieve web-scale integration and interoperability. Executing federated Linked Data queries on the Web requires accessing multiple data sources, which involves the discovery of data sources and determining relevant ones. Researchers have proposed discovery approaches for Linked Data interfaces based on hypermedia links and controls and applied them to federated query execution with Triple Pattern Fragments [[34\]](#page-18-16). SPARQL endpoints are expensive for the server and not always available for all data sets. Downloadable dumps are expensive for clients and do not allow live querying on the web. The Linked Data Fragments framework enables client-side SPARQL querying of live Linked Data on the Web and federated querying through a triple-pattern interface, providing a much faster, less expensive solution [[34\]](#page-18-16).

## *Methods*We conducted a thematic assessment of patients' requirements and used the identified requirements to develop a use case scenario that motivates the need for a PHL. We explain the technological infrastructures used to build the PHL platform, including the Solid platform and knowledge graphs.

## Thematic Assessment of Patient Requirements

The patient requirements for a PHL that we identified in the literature [\[7](#page-17-5)[-12](#page-17-6)] fall into three broad themes: (1) construction and management of the library, (2) dynamic discovery and integration of new knowledge related to data and types stored in the library, and (3) the ability to leverage the knowledge stored in the library through digital interventions [\(Table 2\)](#page-6-0). We assessed the technological innovations required to meet those requirements. To address R1.2 and R3.2, we need an infrastructure that supports privacy by design. To enable patients to effectively share data and knowledge, we need a platform that supports sharing not only with individuals (R5, R11) but also with organizations (R6) and devices (R10, R13.2). To enable patients to selectively define and store*types* of knowledge or data (R1.3, R3.1), we need to leverage Semantic Web technologies. Finally, to incorporate dynamic discovery and knowledge enrichment, we need to store patient's data using a KG (R4.1, R4.2) in a machine-readable format. Besides these functional requirements, the platform should support nonfunctional requirements, including security, integration, and interoperability. Our innovative technologies meet all of these requirements.

![](_page_5_Picture_10.jpeg)
<!-- Image Description: The image is a simple text-based logo. It displays "XSL-FO" in grey, stacked above "RenderX" in purple. This likely represents the RenderX implementation of the XSL-FO (Extensible Stylesheet Language Formatting Objects) standard, a markup language for formatting XML documents. The image's purpose in the paper is likely to identify the specific software or technology used in the described work. -->

<span id="page-6-0"></span>**Table 2.** Some requirements for a PHL (from a patient perspective, per the literature).

| Requirement | Description | | | | |
|-----------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|--|--|--|
| I. Construction and management of digital health state | | | | | |
| R1.1 Integration<br>R1.2 Security and privacy<br>R1.3 Semantic technologies: ontologies | Construct a PHLa<br>by bringing a patient's data together in a trustworthy, usable, and<br>useful library by gathering different types of knowledge into a single resource | | | | |
| R2 Management: | Manage the PHL by creating, reading, updating, or deleting resources | | | | |
| a. RESTfulb<br>resources | | | | | |
| b. CRUDc<br>operations | | | | | |
| R3.1 Semantic technologies: ontologies<br>R3.2 Privacy: | Decide what types of data should be kept and who has access to that data | | | | |
| a. What: resource<br>b. Who: agent | | | | | |
| II. Dynamic knowledge discovery and integration | | | | | |
| R4.1 Dynamic knowledge discovery<br>R4.2 Knowledge enrichment | Seek health data from constantly changing public sources, enriched with new streams<br>and types of data | | | | |
| R5 Knowledge sharing with individuals | Decide what types of data are important to collect, manage, and share | | | | |
| R6 Knowledge sharing with organizations | Share data with citizen science and research initiatives | | | | |
| III. Processing digital health state (digital interventions/mHealthd | apps) | | | | |
| Interaction-based usage | | | | | |
| R7.1 Searching<br>R7.2 Semantic technologies: | Search through the PHL using intelligent mapping for vocabulary used to describe re<br>sources in the patients' profiles | | | | |
| a. Unique resource representation<br>b. Vocabulary mapping | | | | | |
| R8.1 Semantic technologies: annotations | Annotate results from patient's participation in clinical trials to look for patterns | | | | |
| R8.2 AIe<br>: pattern detection | | | | | |
| Notification-based usage | | | | | |
| R9 Dynamic knowledge discovery | Receive alerts about new data related to topics covered in their PHL | | | | |
| earable device agents (ODLf<br>R10 W<br>data) | Play an active role in staying healthy by monitoring their progress | | | | |
| R11 Knowledge sharing with individuals | Stay current with treatment options and clinical trials for a family member with a debili<br>tating condition | | | | |
| R12 Semantic technologies: | Find and use information including text summarization, knowledge mapping, etc | | | | |
| a. Text summarization<br>b. Knowledge mapping | | | | | |
| R13.1 Intelligent mHealth apps: | Access digital assistance via personalized alerts and suggestions, text summarization,<br>literacy aids, translations, etc | | | | |
| a. Digital assistants | | | | | |
| b. Recommender systems | | | | | |
| R13.2 Software agents | | | | | |

a PHL: personal health library.

<sup>b</sup>REST: representational state transfer.

<sup>c</sup>CRUD: creating, reading, updating, or deleting.

<sup>d</sup>mHealth: mobile health.

<sup>e</sup>AI: artificial intelligence.

<sup>f</sup>ODL: observations of daily living.

![](_page_6_Picture_10.jpeg)
<!-- Image Description: The image shows a simple text-based comparison of two technologies: "XSL-FO" (in gray) and "RenderX" (in purple). It's likely a figure used to briefly introduce or distinguish between these two systems within the paper, possibly related to XML processing, document formatting, or similar topics. The lack of visual complexity suggests a purely comparative, rather than detailed explanatory, purpose. -->

## Scenario

We present a scenario that involves Bob as the main actor and

Alice and Mary as supporting actors to demonstrate how a diabetic patient can benefit from the PHL and use the mHealth app for diabetes self-management ([Textbox 1\)](#page-7-0).

<span id="page-7-0"></span>**Textbox 1.**Use case scenario of self-management for a diabetic patient.
**Bob:** is an African American adult with diabetes equipped with a smartwatch and smartphone that collect physiological data (eg, step counts) in real time. The social app on his smartphone queries his decentralized personal health library (PHL) to deliver tailored push notifications to support behavior change related to chronic disease self-care. Depending on sensor readings and other information in his PHL, the app provides personalized and tailored recommendations for healthy eating, physical activity, medication taking, and/or visiting health care providers. The health recommendations also take into account different characteristics of the nearby points-of-interest. For example, as Bob has another comorbidity (asthma), running activities must be avoided.
**Alice:** is a patient who is under treatment for cancer and is also part of Bob's social network. She would like to report acute health conditions and side effects of using medications by sharing a notepad with her physician.
**Mary:** is a physician who follows up with both Bob and Alice. Through the PHL, she would like to interact with her patients and to be able to access their test results easily. She would also like to conduct research about their health conditions using the content generated through their PHLs and her own by tracking publications and scientific observations from trusted public knowledge sources.
**A clinic or lab:** would like to access the PHLs of Alice and Bob to share the results of their lab tests and to follow up on the test and visit history. It also wants to share those tests with their physician, Mary.

In the following, we describe two of the main technological infrastructures used to construct, manage, and integrate the types of knowledge stored in the PHL. Namely, we describe the Solid platform and the role of personal knowledge graphs in designing the PHL and the mHealth app.

## *Social Linked Data (Solid)*To extend the current functionality of the Web (World Wide Web Consortium [W3C] standards and protocols) by applying LOD principles, Berners-Lee proposed the Solid project [\[35,](#page-18-17)[36\]](#page-18-18). Solid is shaping the future vision of the decentralized Web (Web 3.0) by enhancing the technologies used to build Web 2.0 while bringing back the privacy and freedom-oriented values of Web 1.0. Solid uses the*WebID specification*[\[37](#page-18-19)] to implement a global identity management architecture based on the notion of decentralized identity providers. Coupled with the WebID-TLS decentralized authentication protocol, a WebID enables a global web-scale single sign-on. Moreover, Solid follows a unique architecture for building applications by separating users' data from the applications that use that data, which guarantees not only privacy and true ownership but also flexibility. Users can store their data among several Solid-compatible PODs hosted on Solid-enabled Web servers ([Figure 1\)](#page-2-0) that users can either install on their own machines or obtain from a listed provider and selectively authenticate applications to access and process specific resources within those servers. When users register for an identity, their WebID profile document and associated cryptographic key is stored on their main POD server ([Figure](#page-2-0) [1\)](#page-2-0). By leveraging Solid, the underlying storage for patients' digital data in the proposed PHL can be implemented in several ways, for example, file systems, key-value stores, and relational or graph database systems ([Figure 1\)](#page-2-0). In addition, accessing physical data and the metadata will be performed through an allocated semantic layer so that changing or reorganizing the data sources does not cause interruption in the application. Solid is a stack of protocols and standards, so any mHealth app that utilizes the PHL will enable users to maintain control of their data so long as the app is built in a Solid-compatible way.

## *Personal Knowledge Graphs*A personal knowledge graph (PKG) [\[38](#page-18-20)] provides a new research frontier toward building intelligent applications. Assembling data from distributed sources is often challenging, but by leveraging the LOD stack (RDF, URIs, and SPARQL), our PHL platform can achieve such assembly by building an RDF representation of a PKG for each patient that maintains a historical representation of that patient's digital health state. Applications can query those graphs to render different aspects through visual aids and aggregate data by accessing the PODs of the target patient, PODs belonging to other users, and external Web resources ([Figure 1](#page-2-0)).

## *Results*

## Summary

We present the results of assessing the requirements in the previous scenario, the prototype of the PHL and mHealth app, and our evaluation plan. We follow the three main themes identified in [Table 2](#page-6-0) to demonstrate how the different innovative technologies incorporated into the PHL meet these requirements through actions performed by the actors in our scenario (summarized in [Textbox 1](#page-7-0)). In [Textbox 2,](#page-8-0) we distill the most important requirements that the three actors and the involved organization or organizations will need in the proposed PHL and show how we leverage Solid and PKGs, among other technologies, to achieve those requirements.

![](_page_7_Picture_19.jpeg)
<!-- Image Description: The image is a simple text-based graphic showing "XSL-FO" in grey and "RenderX" in purple below. It likely identifies RenderX as a specific software or tool used for processing or rendering Extensible Stylesheet Language Formatting Objects (XSL-FO) within the academic paper. The purpose is to clearly and concisely label a technology used in the research. -->

<span id="page-8-0"></span>**Textbox 2.** Requirements identified in the use case scenario from Textbox 1.

| Functional requirements: | | | | |
|-------------------------------------|-----------------------------------------------------------------------------------------------|--|--|--|
| Agents | | | | |
| • | Device agents (smartwatch, smartphone) | | | |
| • | Person agents (Mary/physician, Alice/another patient) | | | |
| • | Organization agents (clinic) | | | |
| • | Software agents (blogging app, calendar app) | | | |
| | Integrate different types of knowledge from different sources | | | |
| • | Registries: comorbidity (asthma) | | | |
| • | Global knowledge: blogs (HTML), articles (PDF) | | | |
| • | SDoH: neighborhood with low walkability score | | | |
| • | ODL: healthy eating, physical activity, medication taking, and visiting health care providers | | | |
| Usage patterns | | | | |
| • | Annotation of research articles and clinical trials | | | |
| • | Sharing knowledge and resources | | | |
| Nonfunctional requirements: | | | | |
| Security, privacy, interoperability | | | | |
| • | Clinic and PHL software integration (posting test results) | | | |
| • | PHL and EHR software integration (patient's self-reported outcome) | | | |

## Construction and Management of the PHL

We describe how the three actors in our scenario [\(Textboxes 1](#page-7-0) and [2](#page-8-0)) can use our platform to construct their PHLs [\(Figure 2\)](#page-9-0). This includes decentralized identity through WebIDs, main and extended profile documents ([Figure 2](#page-9-0), F1-F3), trusted agents ([Figure 2,](#page-9-0) F4), and resource management ([Figure 2](#page-9-0), F5).

<span id="page-9-0"></span>**Figure 2.**Main PHL features that meet some of the patients' requirements [\(Table 2](#page-6-0)) demonstrated through the PODs of Alice, Bob, and Mary. Bob's POD contains his main profile document in RDF-based KG representation. Social interactions within the PHL ecosystem include: (1) Alice and Mary can subscribe to Bob's channel using their WebIDs. (2) Alice can share her lab tests by pushing them to Mary's inbox. (3.1) Alice can share a notepad with Mary to discuss her lab results. (3.2) Alice can add annotations or comments to message content in Bob's diabetes channel. (4) Software from a clinic or other provider can share test results with Alice by performing a POST Web API operation on the unique URI of her inbox. POD: personal online data store.

![](_page_9_Figure_3.jpeg)
<!-- Image Description: This image displays a data model illustrating data flow and relationships among multiple entities (Alice, Bob, Mary) and their respective Personal Online Datastores (PODs). It uses a UML-like diagram showing data containers (Inbox, public/private containers), resources (bloodtests, deviceReadings), and relationships (Idp:contains, foaf:knows, isParticipant). The diagram highlights data sharing via POST requests, focusing on access control and data exchange between individuals and organizations. Numbered circles indicate process steps. -->

## *Decentralized Identity Through WebIDs*<span id="page-9-1"></span>First, the three actors generate unique WebIDs ([Figure 2](#page-9-0), F1) to securely log in to their main RDF-based PHL*profile document*([Figure 2,](#page-9-0) F2). Once they set up their main PHL profiles, they can build a*Web of Trust*using the FOAF (Friend of a Friend) vocabulary (eg, foaf:knows) by linking their main profiles to one or more extended profiles [\(Figure 2](#page-9-0), F3). In their extended profiles, our actors can keep lists of vCard URIs of trusted agents and selectively grant them access to content in their PHL. For example, Bob can create an extended document in which he stores his friends list ([Figures 3](#page-9-1) and [4\)](#page-10-0). Once they set up their profiles, users can manage content within those documents. In the following section, we explain how Bob manages content under his PHL and how he adds trusted agents.

**Figure 3.** Bob's main PHL profile document with a reference to his friends' extended profiles.

![](_page_9_Picture_9.jpeg)
<!-- Image Description: The image is a simple text graphic showing "XSL-FO" in gray and "RenderX" in light purple. It likely serves as a logo or identifier within the academic paper, indicating the use of RenderX software, a XSL-FO processor, in the research described. No diagrams, charts, graphs, or equations are present. The purpose is to clearly identify a specific technology used in the paper's methodology or implementation. -->

<span id="page-10-0"></span>**Figure 4.**Bob's extended profile document (friends) that identifies Alice and Mary as trusted agents by establishing foaf:knows relations with their WebIDs.

## *Hierarchical Resource Representation*Whether it is a person, an inbox, a file, an image, a notification, or a relationship, content within the PHL is represented as a collection of Web resources. Patients can organize resources in their PHL as a hierarchy of nested*containers*. For example, an event is nested inside a calendar and a message is nested within a chat channel. Both containers and resources conform to the LDP BasicContainer specification. The different actors in our scenario can start with default containers provided by the PHL. For example, the inbox container gets created in the PHL as a default container preconfigured with live notifications. The patient's inbox is also discoverable through the ldp:inbox property specified in the Linked Data Notification (LDN) specification [\[39](#page-18-21)]. Beyond default containers, patients can define their own resources or containers. For example, Bob can add the calendar and diabetes folders under his public or private folders ([Figure 5\)](#page-10-1). He can also set up a chat channel about diabetes as a resource of type LongChat and nest that within the Diabetes folder ([Figure 2](#page-9-0), F5).

<span id="page-10-1"></span>**Figure 5.**Hierarchy of containers under Bob's PHL.

![](_page_10_Picture_8.jpeg)
<!-- Image Description: The image displays a snippet of RDF (Resource Description Framework) code. It defines a `BasicContainer` with three contained resources: `calendar`, `diabetes`, and `inbox`. Each contained resource is further defined using URIs to specify their respective types. The code illustrates a simple knowledge representation using RDF triples, showcasing how relationships between resources are expressed. The purpose is likely to exemplify the data model or syntax used in the paper. -->

## *Flexible Data Representations*The PHL supports reading and writing resources in different formats: (1) structured Linked Data resources (eg, RDF, HTML+RDFa (RDF in Attributes), etc), (2) binary data (eg, images, videos, webpages), and (3) non–linked data structured text. While the PHL enables building applications with nonlinked resources, using RDF-based linked data provides extra benefits in terms of interoperability with the rest of the ecosystem.

## *Trusted Agents*

Agents can be persons, organizations, devices, or software. For example, Bob can add the clinic as an organization agent, Alice and Mary as person agents, his mobile phone as a device agent, and the diabetes self-management mobile app as a software agent ([Figure 2](#page-9-0), F4). Access can be granted either to individual agents or agent groups. For example, Bob can define two work-groups (Physicians and Caregivers) in an extended document (work-groups) ([Figure 6\)](#page-11-0). In that document, he can list Mary and Alice as members using their WebIDs. He can then grant each of these agent groups fine-grained access permissions to his shared-notepad resource. Bob can reference a group as a resource under the work-groups document ([Figure](#page-11-1) [7\)](#page-11-1).

In addition, since he is interested in tracking and gathering data about diabetes from a blogging app, he can add the app under the trusted apps section of his extended profile document [\(Figure](#page-11-2) [8\)](#page-11-2).

![](_page_10_Picture_15.jpeg)
<!-- Image Description: The image shows a simple text comparison of "XSL-FO" (in grey) and "RenderX" (in purple). It likely serves to visually distinguish between two different XML formatting object languages or rendering engines within the paper. The contrast in color and font style highlights a key difference or comparison point between the two systems. The image's purpose is likely to provide a clear visual identifier for readers familiar with these technologies. -->

<span id="page-11-0"></span>**Figure 6.** Bob's work-groups document that defines Physicians and Caregivers as groups.

<span id="page-11-1"></span>**Figure 7.** Individual and Group authorizations to Bob's notepad.

<span id="page-11-2"></span>**Figure 8.**Bob's trusted apps.

## *Access Control Lists*

The PHL uses the W3C Web Access Control (WAC) ontology to describe Read, Write, Control, and Append access control modes (eg, acl:mode acl:Read, [Figure 9](#page-12-0)) at the level of a container or resource. Each resource can have an associated access control list (ACL) resource. If a container or resource does not have an ACL, it inherits the authorization of its parent container. For example, the default ACL on the inbox container is append-only by the public. Bob can associate the lab\_test resource within his inbox with a corresponding ACL resource (lab\_test.acl). Then, within that ACL resource, he can specify trusted agents and their corresponding access modes. For example, he can limit access to his friends'list extended profile document [\(Figure 4](#page-10-0)) by defining an ACL rule using the WAC ontology [\(Figure 9\)](#page-12-0).

<span id="page-12-0"></span>**Figure 9.**An ACL rule granting Read permission to Alice and Mary on Bob's "Friends" document.

## Dynamic Knowledge Discovery and Integration

In this section, we describe how dynamic discovery and integration can be achieved through linkability, the ability to interact with the PHL content through annotations, rich embedding, and social interactions between the different actors in our scenario.

## *Linkability*

Resources generated by each of the three actors get stored in their PHLs, with the possibility of linking resources in their PHLs to resources in other users' PHLs [\(Figure 2](#page-9-0), F7). For example, if Alice comments on a message stored under the diabetes channel resource in Bob's PHL, her message will be stored under her PHL but links to Bob's message using the hasTarget Link type defined in the Web Annotation Ontology (WAO) [\(Figure 10\)](#page-12-1).

<span id="page-12-1"></span>**Figure 10.**Alice's comment is linked to Bob's message using the hasTarget link type of the Web Annotation Ontology.

![](_page_12_Figure_9.jpeg)
<!-- Image Description: The image displays a snippet of RDF (Resource Description Framework) code. It shows a prefix declaration for "wao" and two triples. The first triple links a comment resource (a URL) to the "wao:hasTarget" predicate. The second triple is the object of the first triple, linking to a diabetes-related message resource (a URL). The code illustrates a data model representing relationships between online resources using RDF syntax. -->

## *Annotations, Rich Embedding, and Social Interaction*The PHL can be used as a decentralized authoring, annotation, and social interaction framework that can be accessed from several platforms (eg, Web browsers and mobile apps). By implementing the Web Annotation specification [[29\]](#page-18-11), the PHL enables physicians to annotate content within resources stored under their PHLs. As a physician-researcher, Mary can benefit from the content generated through her PHL about diabetes. To this end, she can announce her inbox so she can receive LDN notifications of scholarly activities related to diabetes (eg, published articles, annotations in peer reviews [\[29](#page-18-11)], scientific observations). She can add identifiers to important concepts within her received content (eg, article) and add descriptive markup to those identified concepts. Her PHL uses the identifiers to automatically generate URIs for every article section to make it easy for others to refer to them or link them to external knowledge resources. Using Mary's descriptions, the PHL automatically generates RDFa markup documents, and by implementing the protocol, it enables her to expose those generated documents as Linked Data for other researchers to consume.

The PHL also supports rich embedding, whereby a researcher or a physician can embed raw data within a document in several formats and add provenance links (eg, nanopublications). For example, having Mary as a physician in the chat channel can add credibility to the discussion and enrich the knowledge exchanged. She can highlight certain statements exchanged in a message and correct a misconception. She can also comment on shared knowledge in a particular message and probably refer patients to more trusted sources of knowledge (eg, Centers for Disease Control and Prevention, World Health Organization). Similarly, when Bob receives information about treatment options from Mary as his physician, he can integrate it with information obtained from the blogging app. For example, he can highlight concepts in a blog post relating to diabetes and related interventions and link them to the same concepts in Mary's shared notepad or concepts shared by other users in his diabetes channel.

Mary, Bob, and Alice can perform social interactions within the PHL ecosystem in different ways ([Figure 2\)](#page-9-0). For example, (1) Alice and Mary can subscribe to Bob's channel using their WebIDs; (2) Alice can share the results of her lab tests by pushing them to Mary's inbox; (3.1) Alice can share a notepad with Mary to discuss digital health knowledge that she obtained from other sources, and Mary can interact with the content by adding annotations, refining provenance links, or linking words to scientific concepts; (3.2) Alice can also add annotations or comments to message content in Bob's diabetes channel; and (4) software from a clinic or other provider can share test results with Alice. Users get notifications for every activity performed on content under their PHLs, including annotations, replies, shares, reviews, citations, links, bookmarks, and even likes.

## *Data Access Through RESTful HTTP Operations*

Data stored in the PHL is managed in a RESTful way; new resources are created under a container by sending them to the container's unique URI via an HTTP POST operation. The PHL

supports two-way server-to-server and client-to-server communication. Either way, the requesting agent performs an HTTP operation on a given resource URI under a given POD server. Sending lab results from the clinic to Alice's inbox is an example of a server-to-server communication. The software agent (eg, Cerner) hosted on the clinic's server performs a POST operation on the /inbox/lab-tests resource on the POD server hosting Alice's PHL ([Figure 2,](#page-9-0) step 4). A self-reported outcome is an example of a client-to-server communication that originates from a patient's PHL to external software. For example, Bob can report an allergy, which generates a POST request on a URI under the server hosting his EHR.

Agents do not need to know the internal structure of a patient's PHL. Each resource in PHL is its own SPARQL endpoint, which can be advertised through Link headers that can be discovered by sending HTTP GET/HEAD operations on the main PHL URI. Performing a GET operation on any URI that ends with a \* returns an aggregate of all the resources that match the indicated pattern. For example, to fetch all diabetes self-management recommendations under Bob's diabetes container, an agent can send a single GET request to the /data/diabetes/\* resource on the server hosting his PHL profile ([Figure 11\)](#page-13-0).

<span id="page-13-0"></span>**Figure 11.**A GET request on Bob's diabetes messages folder under his POD.

Application-to-server communication happens when an application pushes content to a user's PHL. Users can interact with their PHLs through different apps installed on their phones after signing in using their WebIDs. For instance, when Bob installs the diabetes mHealth app on his phone, recommendations are pushed to the corresponding container within his messaging POD [\(Figure 1](#page-2-0)). By signing up, his PHL sends periodic GET requests to the app to get the latest recommendations. Similarly, Mary can add follow-up events using the calendar app of her choice, and that app can share those events by pushing them as resources under Bob's calendar container by sending POST requests on that container's URI.

## *Prototype Design of the PHL and mHealth App*[Figure 12](#page-14-0) shows the main interface design of the mobile app and [Figure 13](#page-15-0) shows the PHL. Through the PHL, patients can set their preferences to tailor the*content* in the desired recommendations in terms of focus (eg, diet, exercise, and medication adherence), frame (eg, educational, motivational, goal-based), and frequency (daily, weekly, etc).

![](_page_13_Picture_10.jpeg)
<!-- Image Description: The image is a simple text-based illustration showing "XSL-FO" in gray and "RenderX" in light purple below it. It likely serves to identify the XSL-FO formatting language and the RenderX processor used in the paper, probably within the context of a discussion of document processing, publishing, or XML technologies. No charts, graphs, or equations are present. -->

<span id="page-14-0"></span>**Figure 12.** Mobile app for chronic disease self-management.

![](_page_14_Figure_3.jpeg)
<!-- Image Description: The image displays a screenshot of a mobile application interface for diabetes self-management. The app's main screen is organized into colored blocks providing medication adherence, physical activity, healthy eating recommendations, nearby resource listings (farmers market, clinic, gym), a health monitor for blood pressure and glucose, a calendar, reminders, and an outcome reporting feature. A user can select a difficulty level (basic, intermediate, advanced). The screenshot illustrates the app's user interface and functionality. -->

![](_page_14_Picture_4.jpeg)
<!-- Image Description: The image shows text-based labels: "XSL-FO" in gray and "RenderX" in purple. It's likely a simple illustration identifying a specific XSL-FO processor (RenderX) used in the paper's methodology. The purpose is to clearly state the software implementation details for a reproducible experiment or result regarding XSL-FO document processing. -->

<span id="page-15-0"></span>**Figure 13.**The PHL that enables the app in Figure 12. Through the PHL patients can perform (a) Chronic disease self-management, obtain (b) External knowledge and resource suggestions, and (c) manage trusted agents. The PHL can personalize recommendations by utilizing knowledge about monitored ODL readings, location-based detection of SDoH, external knowledge suggestions, and EHRs. Other features include reminders of medications and shared notepads with physicians.

![](_page_15_Figure_3.jpeg)
<!-- Image Description: The image displays a user interface (UI) mockup for a personal health management mobile application. The UI is organized into tiled sections, showcasing features such as chronic disease self-management (with customizable preferences), daily living observation tracking, external knowledge suggestions (linking to CDC articles and PubMed), a calendar, shared notes, and access to electronic medical records. A "Manage Trusted Agents" section allows users to specify trusted contacts and applications. The UI also includes a user level selection (Basic, Intermediate, Advanced). The purpose is to illustrate the app's design and functionality. -->

The app, on the other hand, sends enriched message recommendations based on patients' preferences. By accessing dynamic knowledge in the PHL, the app can provide real-time hybrid recommendations that are both*content-*and*context*-based. To capture context, the PHL collects both ODL and SDoH data from activity trackers and population-level neighborhood characteristics. It utilizes both the data and the semantic conceptual hierarchies of knowledge types stored in the library to infer new knowledge and collect more evidence. For example, if a patient lives in a zip code that has a low walkability score, the app avoids sending recommendations that encourage walking in the neighborhood. In addition, if their device reading shows a high heart rate or if their EHR shows they have asthma, the app avoids recommendations of physical activities that would severely affect their health conditions. In addition to textual message recommendations, the app provides resource suggestions within the patients' zip code area or provides language-speaking services that respect their race or ethnicity.

## *Sources of Data and Knowledge*The PHL utilizes and integrates data and knowledge from several sources:

1. Historical data collected systematically through regional registries—in the case of the mobile app proposed in this paper, we utilize the Diabetes Wellness and Prevention Coalition (DWPC) regional registry, which aims to improve care for people with obesity, diabetes, and other obesity-associated chronic conditions. It provides clinical information, including hospital and clinic visits, as well as labs, diagnoses, and medications.

2. ODL data collected through mobile devices and activity trackers, such as physical exercises, heart rate, etc

3. Population-level SDoH data, such as walkability scores in a neighborhood and access to public transport, among others

4. Public knowledge obtained from research and news articles, blogs, and social networks

## *Enabling Technologies for Building the mHealth App*To implement PHL-enabled mobile apps, we will utilize a RESTful API that will expose the RDF-based PKG data model stored in a patient's PHL. We will leverage the Solid technology stack from within JavaScript-based environments, which will enable us to integrate data by invoking APIs exposed by different POD servers. For Linked Data manipulation and

querying, we will utilize RDFlib and LDflex. We will use the Solid-authenticated RDFlib API and query engine for advanced parsing and querying of the patient's RDF-based PKG data model stored in a patient's PHL.

In addition to querying the patient's local PKG data model, we will utilize the LDflex domain-specific language to query any Linked Data resource on the Web, which enables dynamic external knowledge discovery and integration. LDflex provides concise expressions that allow us to perform complex federated query execution without having to craft all HTTP requests required in a query and without hardcoding resource URLs. We provided the query engine with the root node (eg, Bob's WebID), an entry point (eg, Bob's inbox/lab\_tests/test1), and a property (eg, testResult) to query Bob's health knowledge graph data model. The engine uses the entry point to recognize the context in which the query is executed and resolves the expression into an actual path on Bob's graph. Expression execution involves several steps: obtaining Bob's WebID URL, resolving the terms included in the expressions (eg, lab\_test) to their URLs, creating the SPARQL query that represents the expression, fetching the document of the root user (Bob) through an HTTP request, and executing the SPARQL query on the document and returning the result.

## Evaluation Plan

Before fully implementing the PHL and the mHealth app, we will conduct two evaluation studies. In this section, we provide a protocol synopsis for each study.

## *Study 1: User-Centered Design and Formative Evaluation of the Prototype*The so-called "digital divide" may hinder the adoption of digital interventions, but the use of human factors engineering can overcome some of the challenges in that regard [\[40](#page-18-22)[,41](#page-19-0)]. We will conduct a descriptive, iterative, user-centered design and formative evaluation study by seeking feedback from pre-development focus groups, specifically participants from regional hospitals, including patients, caregivers, health care professionals (clinicians, residents, physicians), and health education professionals. The goal is to reveal issues related to the (1) usability, (2) clinical content, and (3) educational content of both the (a) PHL platform and (b) recommendations produced by the app. We will organize a workshop to both verify initial requirements, scenarios, and storyboards and identify new ones. We will use our findings to refine the initial requirements and develop new scenarios and generate new storyboard simulations. We will assign participants to focus groups and run different scenarios and dashboard simulations by them. We will use the System Usability Scale and the EHR Usability Scale to gather feedback [\[42](#page-19-1),[43\]](#page-19-2). Finally, we will apply thematic assessment to the resulting transcripts and use the results to design the final PHL and mHealth app following the refined storyboard simulations.

## *Study 2: Pragmatic Clinical Trial for Evaluation of the Digital Intervention*To evaluate the effectiveness of this intelligent digital intervention compared to existing interventions on the population of patients with diabetes, we will replicate the

[XSL](http://www.w3.org/Style/XSL)•FO**[RenderX](http://www.renderx.com/)**pragmatic randomized controlled trial design described by Bailey et al [[44\]](#page-19-3), with variations. The three primary*outcomes*that we will test are the number of days in the previous week that participants (1) ate healthy meals, (2) participated in at least 30 minutes of physical activity, and (3) took medications as prescribed. Participants will be adults age ≥18 years who have uncontrolled diabetes (A1c≥8), exhibit one or more additional chronic conditions seen in clinics in medically underserved areas of the mid-South, and possess a phone with texting and voicemail capability. Intervention arms will be standard motivational SMS text messaging (TM) and intelligent recommendation–enhanced TM (IR-TM), and the control arm will be usual care. We will capture the patients' perceptions of diabetes self-care activities using subscales of the revised Summary of Diabetes Self-Care Activities questionnaire administered over the study follow-up period. We will also use the DWPC registry to obtain clinical data, including A1c, body mass index, and blood pressure. We will test multiple hypotheses to determine the comparative effectiveness of the control and intervention arms for each primary outcome. Sample size and power estimates for these types of digital interventions will follow the approach described by Bailey et al [[44\]](#page-19-3), with the assumption that effect sizes will range from small (standardized difference=0.375) to medium (=0.50). To obtain power estimates, projected mean changes over 12-month follow-up from baseline (mean for 12-month follow-up minus mean for baseline) of the control and intervention arms for each primary outcome will be obtained using results reported in the literature. We expect the TM and IR-TM arms to have adequate power to detect meaningful changes from baseline with respect to all three primary outcome variables compared to the usual care arm will.

## *Discussion*Our previous research has identified that minorities and low-income, underserved communities are disproportionately affected by chronic diseases [\[45](#page-19-4)] such as obesity [[46\]](#page-19-5), a risk factor for diabetes, heart disease, and cancer. In this paper, we describe a personal health library–enabled mHealth app that provides hybrid recommendations by incorporating SDoH and ODLs in addition to digital health information to provide insights for informing preventive digital interventions in chronic disease management.

The PHL gathers different types of knowledge into a single searchable resource. While there has been some effort to build similar systems, the novelty of the proposed approach lies in (1) providing a decentralized yet linked architecture; (2) supporting interoperability, portability, knowledge mapping, and reasoning by following protocol, format, and vocabulary standards; (3) building trust with patients by facilitating true ownership over their data and appropriate reporting; and (4) giving those patients fine-grained access control mechanisms.

The PHL will not only help patients and their caregivers to assume a central role in making decisions regarding their health but also equip health care providers with informatics tools that will support the collection, interpretation, and dissemination of the collected knowledge. By moving health care beyond clinical

settings, clinicians can benefit from the PHL in leading new treatment regimens and keeping in touch with their patients between office visits.

Future work will focus on further implementation of an end-to-end framework of an intelligent recommender and digital librarian, including text summarization, knowledge mapping, and personalized resource suggestions. In achieving this goal, we will incorporate artificial intelligence techniques and knowledge representation methods that have been successfully used in our previous works [[47,](#page-19-6)[48](#page-19-7)]. Other ongoing tasks will include establishing a clinical trial of the app and recruiting participants to fully evaluate the app. Future work will also focus on the enrichment of patients' health knowledge graphs to improve the reasoning capabilities of the knowledge layer.

Finally, we plan to expose parts of the PHL functionality as an open service for fostering the development of third-party applications that may provide motivational technological support in several national and international projects crossing different domains of interest. To achieve this, the library will serve as an API for querying, managing, and using a patient's health RDF-based knowledge graph. This will give the community access to the infrastructure of the library to enable building applications that benefit from the library for other phenotypes.

## Conflicts of Interest

None declared.

## <span id="page-17-0"></span>References

- 1. Baird A, North F, Raghu TS. Personal Health Records (PHR) and the future of the physician-patient relationship. 2011 Presented at: 2011 iConference; February 2011; Seattle, WA p. 281-288. [doi: [10.1145/1940761.1940800\]](http://dx.doi.org/10.1145/1940761.1940800)
- <span id="page-17-2"></span><span id="page-17-1"></span>2. Laine C, Davidoff F. Patient-centered medicine. A professional evolution. JAMA 1996 Jan 10;275(2):152-156. [Medline: [8531314\]](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=8531314&dopt=Abstract)
- 3. People-Centred Health Care: A policy framework. Geneva: World Health Organization; 2007.
- <span id="page-17-3"></span>4. Diez Roux AV, Katz M, Crews DC, Ross D, Adler N. Social and Behavioral Information in Electronic Health Records: New Opportunities for Medicine and Public Health. Am J Prev Med 2015 Dec;49(6):980-983. [doi: [10.1016/j.amepre.2015.08.027](http://dx.doi.org/10.1016/j.amepre.2015.08.027)] [Medline: [26590943\]](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=26590943&dopt=Abstract)
- <span id="page-17-5"></span><span id="page-17-4"></span>5. Backonja U, Kim K, Casper GR, Patton T, Ramly E, Brennan PF. Observations of daily living: putting the "personal" in personal health records. NI 2012 (2012) 2012;2012:6 [\[FREE Full text\]](http://europepmc.org/abstract/MED/24199037) [Medline: [24199037\]](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=24199037&dopt=Abstract)
- 6. McWilliam CL. Patients, persons or partners? Involving those with chronic disease in their care. Chronic Illn 2009 Dec;5(4):277-292. [doi: [10.1177/1742395309349315\]](http://dx.doi.org/10.1177/1742395309349315) [Medline: [19933246\]](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=19933246&dopt=Abstract)
- 7. Auerbach SM. Should patients have control over their own health care?: empirical evidence and research issues. Ann Behav Med 2000;22(3):246-259. [doi: [10.1007/BF02895120\]](http://dx.doi.org/10.1007/BF02895120) [Medline: [11126470\]](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=11126470&dopt=Abstract)
- 8. Ross SE, Todd J, Moore LA, Beaty BL, Wittevrongel L, Lin C. Expectations of patients and physicians regarding patient-accessible medical records. J Med Internet Res 2005 May 24;7(2):e13 [[FREE Full text\]](https://www.jmir.org/2005/2/e13/) [doi: [10.2196/jmir.7.2.e13](http://dx.doi.org/10.2196/jmir.7.2.e13)] [Medline: [15914460](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=15914460&dopt=Abstract)]
- 9. Wildemuth B, Blake CL, Spurgin K, Oh S, Zhang Y. Patient's perspectives on personal health records: An assessments of needs and concerns. In: Proceedings of Critical Issues in eHealth Research 2006. 2006 Presented at: Critical Issues in eHealth Research 2006; 2006; National Institutes of Health.
- <span id="page-17-6"></span>10. Hassol A, Walker JM, Kidder D, Rokita K, Young D, Pierdon S, et al. Patient experiences and attitudes about access to a patient electronic health care record and linked web messaging. J Am Med Inform Assoc 2004;11(6):505-513 [[FREE Full](http://europepmc.org/abstract/MED/15299001) [text](http://europepmc.org/abstract/MED/15299001)] [doi: [10.1197/jamia.M1593\]](http://dx.doi.org/10.1197/jamia.M1593) [Medline: [15299001](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=15299001&dopt=Abstract)]
- <span id="page-17-7"></span>11. Arora NK, Johnson P, Gustafson DH, McTavish F, Hawkins RP, Pingree S. Barriers to information access, perceived health competence, and psychosocial health outcomes: test of a mediation model in a breast cancer sample. Patient Educ Couns 2002 May;47(1):37-46. [doi: [10.1016/s0738-3991\(01\)00170-7\]](http://dx.doi.org/10.1016/s0738-3991(01)00170-7) [Medline: [12023099](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=12023099&dopt=Abstract)]
- <span id="page-17-8"></span>12. Pratt W, Unruh K, Civan A, Skeels MM. Personal health information management. Commun ACM 2006 Jan;49(1):51-55. [doi: [10.1145/1107458.1107490\]](http://dx.doi.org/10.1145/1107458.1107490)
- <span id="page-17-9"></span>13. Kay M, Santos J, Takane M. mhealth: New horizons for health through mobile technologies.: World Health Organization; 2011. URL: [https://www.who.int/goe/publications/goe\\_mhealth\\_web.pdf](https://www.who.int/goe/publications/goe_mhealth_web.pdf) [accessed 2021-02-12]
- <span id="page-17-10"></span>14. Ammar N, Bailey JE, Davis RL, Shaban-Nejad A. The Personal Health Library: A Single Point of Secure Access to Patient Digital Health Information. Stud Health Technol Inform 2020 Jun 16;270:448-452. [doi: [10.3233/SHTI200200\]](http://dx.doi.org/10.3233/SHTI200200) [Medline: [32570424](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=32570424&dopt=Abstract)]
- <span id="page-17-11"></span>15. Ammar N, Bailey J, Davis RL, Shaban-Nejad A. Implementation of a Personal Health Library (PHL) To Support Self-Management of Chronic Diseases. In: Shaban-Nejad A, Michalowski M, Buckeridge DL, editors. Explainable AI in Healthcare and Medicine: Building a Culture of Transparency and Accountability. New York City: Springer; 2020.
- 16. World Health Organization. Social determinants of health. 2019. URL: [https://www.who.int/social\\_determinants/](https://www.who.int/social_determinants/sdh_definition/en/) [sdh\\_definition/en/](https://www.who.int/social_determinants/sdh_definition/en/) [accessed 2020-03-02]
- 17. Barr PJ, Hassanpour S, Haslett W, Dannenberg MD, Ganoe CH, Faill R, et al. The Development of a Personal Audio Health Library (Audio Pahl) - Preliminary Usability Testing & Annotation Guide Development. 2019 Presented at: American Medical Informatics Association (AMIA) Summit on Informatics; 2019; San Francisco, CA.

- <span id="page-18-0"></span>18. Barr PJ, Hassanpour S, Haslett W, Dannenberg MD, Ganoe CH, Faill R, et al. Improving Patient and Caregiver Engagement through the Application of Data Science Methods to Audio Recorded Clinic Visits Stored in Personal Health Libraries Using ORALS. 2018 Presented at: American Medical Informatics Association Summit on Informatics; 2018; San Francisco, CA.
- <span id="page-18-2"></span><span id="page-18-1"></span>19. Brennan PF, Downs S, Casper G. Project HealthDesign: rethinking the power and potential of personal health records. J Biomed Inform 2010 Oct;43(5 Suppl):S3-S5 [\[FREE Full text\]](http://linkinghub.elsevier.com/retrieve/pii/S1532-0464(10)00133-4) [doi: [10.1016/j.jbi.2010.09.001](http://dx.doi.org/10.1016/j.jbi.2010.09.001)] [Medline: [20937482](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=20937482&dopt=Abstract)]
- 20. Cohen DJ, Keller SR, Hayes GR, Dorr DA, Ash JS, Sittig DF. Developing a model for understanding patient collection of observations of daily living: A qualitative meta-synthesis of the Project HealthDesign Program. Pers Ubiquitous Comput 2015 Jan 01;19(1):91-102 [\[FREE Full text\]](http://europepmc.org/abstract/MED/26949381) [doi: [10.1007/s00779-014-0804-1](http://dx.doi.org/10.1007/s00779-014-0804-1)] [Medline: [26949381\]](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=26949381&dopt=Abstract)
- <span id="page-18-4"></span><span id="page-18-3"></span>21. Ralston JD, Revere D, Robins LS, Goldberg HI. Patients' experience with a diabetes support programme based on an interactive electronic medical record: qualitative study. BMJ 2004 May 15;328(7449):1159 [\[FREE Full text\]](http://europepmc.org/abstract/MED/15142919) [doi: [10.1136/bmj.328.7449.1159\]](http://dx.doi.org/10.1136/bmj.328.7449.1159) [Medline: [15142919\]](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=15142919&dopt=Abstract)
- <span id="page-18-5"></span>22. Maimone R, Guerini M, Dragoni M, Bailoni T, Eccher C. PerKApp: A general purpose persuasion architecture for healthy lifestyles. J Biomed Inform 2018 Jun;82:70-87 [[FREE Full text\]](https://linkinghub.elsevier.com/retrieve/pii/S1532-0464(18)30074-1) [doi: [10.1016/j.jbi.2018.04.010\]](http://dx.doi.org/10.1016/j.jbi.2018.04.010) [Medline: [29729482\]](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=29729482&dopt=Abstract)
- <span id="page-18-6"></span>23. Amelie G, Manas G, Saeedeh S, Krishnaprasad T, Amit S. Personalized health knowledge graph. In: Proceedings of ISWC 2018 Contextualized Knowledge Graph Workshop. 2018 Presented at: ISWC 2018 Contextualized Knowledge Graph Workshop; 2018; Monterey, CA p. 29.
- <span id="page-18-7"></span>24. Rotmensch M, Halpern Y, Tlimat A, Horng S, Sontag D. Learning a Health Knowledge Graph from Electronic Medical Records. Sci Rep 2017 Jul 20;7(1):5994 [[FREE Full text](https://doi.org/10.1038/s41598-017-05778-z)] [doi: [10.1038/s41598-017-05778-z](http://dx.doi.org/10.1038/s41598-017-05778-z)] [Medline: [28729710\]](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=28729710&dopt=Abstract)
- <span id="page-18-8"></span>25. Sheth, Amit, Pramod A, Krishnaprasad T. khealth: Proactive personalized actionable information for better healthcare. 2014 Presented at: First International Workshop on Personal Data Analytics in the Internet of Things; 2014; France URL: <https://pdfs.semanticscholar.org/9722/6061407b61d9eb631698f315a3d704b55503.pdf>
- <span id="page-18-9"></span>26. Seneviratne O, Rashid SM, Chari S, McCusker JP, Bennett KP, Hendler JA, et al. Knowledge integration for disease characterization: A breast cancer example. 2018 Presented at: International Semantic Web Conference; October 2018; Monterey, CA p. 223-238. [doi: [10.1007/978-3-030-00668-6\\_14](http://dx.doi.org/10.1007/978-3-030-00668-6_14)]
- <span id="page-18-12"></span><span id="page-18-11"></span><span id="page-18-10"></span>27. Chari S, Qi M, Agu NN, Seneviratne O, McCusker JP, Bennett KP, et al. Making study populations visible through knowledge graphs. 2019 Presented at: International Semantic Web Conference; October 2019; Auckland, New Zealand p. 53-68. [doi: [10.1007/978-3-030-30796-7\\_4\]](http://dx.doi.org/10.1007/978-3-030-30796-7_4)
- <span id="page-18-13"></span>28. Linked Data. W3C. 2006. URL: <https://www.w3.org/DesignIssues/LinkedData> [accessed 2021-03-02]
- 29. The Web Annotation specification. W3C. URL: <https://www.w3.org/TR/annotation-model/> [accessed 2021-03-02]
- <span id="page-18-14"></span>30. Zeng J, Shufean MA, Khotskaya Y, Yang D, Kahle M, Johnson A, et al. OCTANE: Oncology Clinical Trial Annotation Engine. JCO Clin Cancer Inform 2019 Jul;3:1-11 [[FREE Full text](https://ascopubs.org/doi/10.1200/CCI.18.00145?url_ver=Z39.88-2003&rfr_id=ori:rid:crossref.org&rfr_dat=cr_pub%3dpubmed)] [doi: [10.1200/CCI.18.00145](http://dx.doi.org/10.1200/CCI.18.00145)] [Medline: [31265323](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=31265323&dopt=Abstract)]
- <span id="page-18-15"></span>31. Fielding RT, Taylor RN. Architectural Styles and the Design of Network-Based Software Architectures (Vol. 7). Irvine: University of California, Irvine; 2000.
- <span id="page-18-16"></span>32. Vander Sande M, Verborgh R, Dimou A, Colpaert P, Mannens E. Hypermedia-Based Discovery for Source Selection Using Low-Cost Linked Data Interfaces. International Journal on Semantic Web and Information Systems 2016;12(3):79-110. [doi: [10.4018/ijswis.2016070103](http://dx.doi.org/10.4018/ijswis.2016070103)]
- <span id="page-18-17"></span>33. Verborgh R, Dumontier M. A Web API Ecosystem through Feature-Based Reuse. IEEE Internet Comput 2018 May;22(3):29-37. [doi: [10.1109/mic.2018.032501515](http://dx.doi.org/10.1109/mic.2018.032501515)]
- <span id="page-18-18"></span>34. Verborgh R, Vander Sande M, Hartig O, Van Herwegen J, De Vocht L, De Meester B, et al. Triple Pattern Fragments: A Low-Cost Knowledge Graph Interface for the Web. Journal of Web Semantics 2016;37-38:184-206. [doi: [10.2139/ssrn.3199223](http://dx.doi.org/10.2139/ssrn.3199223)]
- <span id="page-18-19"></span>35. Yeung CMA, Liccardi I, Lu K, Seneviratne O, Berners-Lee T. The future of online social networking. In: W3C Workshop on the Future of Social Networking Position Papers (Vol. 2). 2009 Presented at: W3C Workshop on the Future of Social Networking Position Papers; January 2009; Barcelona, Spain p. 2-7.
- <span id="page-18-21"></span><span id="page-18-20"></span>36. Sambra AV, Mansour E, Hawke S, Zareba M, Greco N, Ghanem A, et al. Solid: A Platform for Decentralized Social Applications Based on Linked Data. Technical Report. 2017. URL: [http://www.emansour.com/publications/paper/](http://www.emansour.com/publications/paper/solid_protocols.pdf) [solid\\_protocols.pdf](http://www.emansour.com/publications/paper/solid_protocols.pdf) [accessed 2021-02-19]
- <span id="page-18-22"></span>37. Sambra AV, Story H, Berners-Lee T. WebID Specification. 2014. URL: [http://www.w3.org/2005/Incubator/webid/spec/](http://www.w3.org/2005/Incubator/webid/spec/identity/) [identity/](http://www.w3.org/2005/Incubator/webid/spec/identity/) [accessed 2021-02-19]
- 38. Krisztian BK, Kenter T. Personal Knowledge Graphs: A Research Agenda. : ACM; 2019 Presented at: ACM SIGIR International Conference on Theory of Information Retrieval; 2019; Paris, France p. 217-220. [doi: [10.1145/3341981.3344241\]](http://dx.doi.org/10.1145/3341981.3344241)
- 39. Capadisli S, Guy A, Lange C, Auer S, Sambra A, Berners-Lee T. Linked data notifications: a resource-centric communication protocol. 2017 Presented at: European Semantic Web Conference; May 2017; Slovenia p. 537-553. [doi: [10.1007/978-3-319-58068-5\\_33](http://dx.doi.org/10.1007/978-3-319-58068-5_33)]
- 40. Yamin CK, Emani S, Williams DH, Lipsitz SR, Karson AS, Wald JS, et al. The digital divide in adoption and use of a personal health record. Arch Intern Med 2011 Mar 28;171(6):568-574. [doi: [10.1001/archinternmed.2011.34\]](http://dx.doi.org/10.1001/archinternmed.2011.34) [Medline: [21444847](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=21444847&dopt=Abstract)]

- <span id="page-19-0"></span>41. Sittig DF, Wright A, Osheroff JA, Middleton B, Teich JM, Ash JS, et al. Grand challenges in clinical decision support. J Biomed Inform 2008 Apr;41(2):387-392 [\[FREE Full text\]](http://linkinghub.elsevier.com/retrieve/pii/S1532-0464(07)00104-9) [doi: [10.1016/j.jbi.2007.09.003\]](http://dx.doi.org/10.1016/j.jbi.2007.09.003) [Medline: [18029232](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=18029232&dopt=Abstract)]
- <span id="page-19-2"></span><span id="page-19-1"></span>42. System usability scale (SUS). Usability.gov. 2018. URL: [https://www.usability.gov/how-to-and-tools/methods/](https://www.usability.gov/how-to-and-tools/methods/system-usability-scale.html) [system-usability-scale.html](https://www.usability.gov/how-to-and-tools/methods/system-usability-scale.html) [accessed 2021-03-02]
- <span id="page-19-3"></span>43. Wiklund M, Kendler J, Hochberg L, Weinger M. Technical basis for user interface design of health IT (NIST GCR 15-996). Washington: National Institute of Standards and Technology, US Department of Commerce; 2015.
- 44. Bailey JE, Surbhi S, Gatwood J, Butterworth S, Coday M, Shuvo SA, et al. The management of diabetes in everyday life study: Design and methods for a pragmatic randomized controlled trial comparing the effectiveness of text messaging versus health coaching. Contemp Clin Trials 2020 Sep;96:106080. [doi: [10.1016/j.cct.2020.106080\]](http://dx.doi.org/10.1016/j.cct.2020.106080) [Medline: [32653539](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=32653539&dopt=Abstract)]
- <span id="page-19-5"></span><span id="page-19-4"></span>45. Shin EK, Kwon Y, Shaban-Nejad A. Geo-clustered chronic affinity: pathways from socio-economic disadvantages to health disparities. JAMIA Open 2019 Oct;2(3):317-322 [\[FREE Full text](http://europepmc.org/abstract/MED/31984364)] [doi: [10.1093/jamiaopen/ooz029](http://dx.doi.org/10.1093/jamiaopen/ooz029)] [Medline: [31984364](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=31984364&dopt=Abstract)]
- <span id="page-19-6"></span>46. Addy NA, Shaban-Nejad A, Buckeridge DL, Dubé L. An innovative approach to addressing childhood obesity: a knowledge-based infrastructure for supporting multi-stakeholder partnership decision-making in Quebec, Canada. Int J Environ Res Public Health 2015 Jan 23;12(2):1314-1333 [\[FREE Full text\]](https://www.mdpi.com/resolver?pii=ijerph120201314) [doi: [10.3390/ijerph120201314\]](http://dx.doi.org/10.3390/ijerph120201314) [Medline: [25625409](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=25625409&dopt=Abstract)]
- <span id="page-19-7"></span>47. Ammar N, Shaban-Nejad A. Explainable Artificial Intelligence Recommendation System by Leveraging the Semantics of Adverse Childhood Experiences: Proof-of-Concept Prototype Development. JMIR Med Inform 2020 Nov 4;8(11):e18752. [doi: [10.2196/18752](http://dx.doi.org/10.2196/18752)] [Medline: [33146623\]](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=33146623&dopt=Abstract)
- 48. Brenas JH, Shin EK, Shaban-Nejad A. A Hybrid Recommender System to Guide Assessment and Surveillance of Adverse Childhood Experiences. Stud Health Technol Inform 2019 Jul 04;262:332-335. [doi: [10.3233/SHTI190086](http://dx.doi.org/10.3233/SHTI190086)] [Medline: [31349335](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=31349335&dopt=Abstract)]

## Abbreviations

**ACL:**access control list**API:**application programming interface**DWPC:**Diabetes Wellness and Prevention Coalition**EHR:**electronic health record**IR-TM:**intelligent recommendation–enhanced TM**LDP:**Linked Data Platform**LDN:**Linked Data Notifications**LOD:**Linked Open Data**LOR:**Linked Open Research**ODLs:**observations of daily living**PHKG:**personal health knowledge graph**PHL:**personal health library**POD:**personal online data store**REST:**representational state transfer**RDF:**Resource Description Framework**RDFa:**RDF in Attributes**SDoH:**social determinants of health**Solid:**Social Linked Data**SPARQL:**SPARQL Protocol and RDF Query Language**TM:**text messaging**W3C:**World Wide Web Consortium**WAC:**Web Access Control**WAO:**Web Annotation Ontology
*Edited by G Eysenbach; submitted 02.10.20; peer-reviewed by Y Chu; comments to author 26.10.20; revised version received 08.12.20; accepted 12.02.21; published 16.03.21*###*Please cite as:*

*Ammar N, Bailey JE, Davis RL, Shaban-Nejad A Using a Personal Health Library–Enabled mHealth Recommender System for Self-Management of Diabetes Among Underserved Populations: Use Case for Knowledge Graphs and Linked Data JMIR Form Res 2021;5(3):e24738 URL: <https://formative.jmir.org/2021/3/e24738> doi: [10.2196/24738](http://dx.doi.org/10.2196/24738) PMID: [33724197](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=33724197&dopt=Abstract)*

![](_page_19_Picture_15.jpeg)
<!-- Image Description: The image displays text indicating two software components: "XSL-FO" in gray and "RenderX" in purple. This likely serves as a simple visual identification of the specific XSL-FO processor (RenderX) used in the paper's methodology. The purpose is to clearly communicate the tools employed for generating output from Extensible Stylesheet Language - Formatting Objects (XSL-FO) files, which are crucial to the paper's technical approach. -->

©Nariman Ammar, James E Bailey, Robert L Davis, Arash Shaban-Nejad. Originally published in JMIR Formative Research (http://formative.jmir.org), 16.03.2021. This is an open-access article distributed under the terms of the Creative Commons Attribution License (https://creativecommons.org/licenses/by/4.0/), which permits unrestricted use, distribution, and reproduction in any medium, provided the original work, first published in JMIR Formative Research, is properly cited. The complete bibliographic information, a link to the original publication on http://formative.jmir.org, as well as this copyright and license information must be included.

![](_page_20_Picture_3.jpeg)
<!-- Image Description: The image displays text-based labels: "XSL-FO" in grey and "RenderX" in light purple. It's likely a figure identifying the XSL-FO formatting language and RenderX, a specific XSL-FO processor, used in the paper. The image's purpose is to clearly indicate the technologies employed for document processing or rendering within the research. No diagrams, charts, graphs, or equations are present. -->


## TL;DR
The paper proposes a Personal Health Library (PHL) built on the decentralized Solid platform, using knowledge graphs to integrate diverse health data and deliver personalized recommendations for diabetes self-management.

## Key Insights
The key insight is the necessity of a patient-centric data model (the PHL/PKG) that gives users true ownership and control over their health data. The paper emphasizes that integrating data from various sources (EHRs, Observations of Daily Living, Social Determinants of Health) into a unified, semantically rich KG is essential for enabling personalized and effective mHealth interventions. The use of Solid for decentralization is a critical architectural choice.

## Metadata Summary
### Research Context
- **Research Question**: How can a Personal Health Library (PHL), incorporating both digital health data and contextual knowledge, be implemented to deliver tailored recommendations for improving self-care behaviors in diabetic adults?
- **Methodology**: The methodology involves: (1) A thematic assessment of patient requirements from literature. (2) The design of a PHL architecture using the Solid platform for decentralization and privacy. (3) The use of Semantic Web technologies (RDF, ontologies) to create a Personal Knowledge Graph (PKG) for each user. (4) The development of a prototype mHealth recommender system that queries the PKG to provide personalized interventions. (5) The paper also outlines plans for a formative evaluation and a pragmatic clinical trial.
- **Key Findings**: The paper primarily presents a framework and a prototype design. The key "finding" is the successful conceptualization and architectural design of a PHL-enabled mHealth system that meets identified patient requirements for data ownership, integration, and privacy. It demonstrates the feasibility of using Solid and KGs to build such a system.

### Analysis
- **Limitations**: The paper itself is a proposal and initial design. The system has not yet undergone the planned formative evaluation or clinical trial. The practical challenges of large-scale deployment, user adoption, and the clinical effectiveness of the recommendations are not yet evaluated.
- **Future Work**: The authors state that future work will focus on the full implementation of the end-to-end framework, including text summarization and knowledge mapping features. Crucially, they plan to conduct the formative evaluation and the pragmatic clinical trial to assess the usability and effectiveness of the intervention.