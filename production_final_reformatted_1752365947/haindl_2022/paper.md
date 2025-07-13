---
cite_key: haindl_2022
title: Towards a Reference Software Architecture for Human-AI Teaming in Smart Manufacturing
authors: Philipp Haindl, Maqbool Khan, Georg Buchgeher, Bernhard Moser
year: 2022
doi: 10.1145/3510455.3512788
date_processed: 2025-07-02
phase2_processed: true
original_folder: arxiv_arxiv_2201.04876_Towards_a_Reference_Software_Architecture_for_Human-AI_Teaming_in_Smart_Manufact
tags: 
keywords: 
standardization_date: 2025-07-10
standardization_version: 1.0
---

# Towards a Reference Software Architecture for Human-AI Teaming in Smart Manufacturing

Philipp Haindl philipp.haindl@scch.at Software Competence Center Hagenberg Hagenberg, Austria

Maqbool Khan maqbool.khan@fecid.paf-iast.edu.pk Pak-Austria Fachhochschule - Institute of Applied Sciences and Technology Mang, Haripur, Pakistan

## ABSTRACT

With the proliferation of AI-enabled software systems in smart manufacturing, the role of such systems moves away from a reactive to a proactive role that provides context-specific support to manufacturing operators. In the frame of the EU funded Teaming.AI project, we identified the monitoring of teaming aspects in human-AI collaboration, the runtime monitoring and validation of ethical policies, and the support for experimentation with data and machine learning algorithms as the most relevant challenges for human-AI teaming in smart manufacturing. Based on these challenges, we developed a reference software architecture based on knowledge graphs, tracking and scene analysis, and components for relational machine learning with a particular focus on its scalability. Our approach uses knowledge graphs to capture product and process specific knowledge in the manufacturing process and to utilize it for relational machine learning. This allows for context-specific recommendations for actions in the manufacturing process for the optimization of product quality and the prevention of physical harm. The empirical validation of this software architecture will be conducted in cooperation with three large-scale companies in the automotive, energy systems, and precision machining domain. In this paper we discuss the identified challenges for such a reference software architecture, present its preliminary status, and sketch our further research vision in this project.

## TL;DR

Reference software architecture for human-AI teaming in smart manufacturing using Lambda architecture pattern, knowledge graphs, and relational machine learning to enable context-specific recommendations and real-time collaboration.

## Key Insights

Lambda architecture pattern for manufacturing with knowledge graphs and relational machine learning that addresses different latency requirements for heterogeneous data processing; demonstrates practical implementation of temporal-first architecture principles with real-time IIoT data integration and context-specific decision support capabilities essential for bespoke PKG system development.

## CCS CONCEPTS

* Human-centered computing;
* Computing methodologies → Artificial intelligence;
* Software and its engineering;

ICSE-NIER'22, May 21–29, 2022, Pittsburgh, PA, USA

© 2022 Association for Computing Machinery.

ACM ISBN 978-1-4503-9224-2/22/05. . . $15.00

<https://doi.org/10.1145/3510455.3512788>

Georg Buchgeher georg.buchgeher@scch.at Software Competence Center Hagenberg Hagenberg, Austria

Bernhard Moser bernhard.moser@scch.at Software Competence Center Hagenberg Hagenberg, Austria

### KEYWORDS

human-AI teaming, IIoT, knowledge graphs, relational machine learning, software architecture, smart manufacturing

### ACM Reference Format:

Philipp Haindl, Georg Buchgeher, Maqbool Khan, and Bernhard Moser. 2022. Towards a Reference Software Architecture for Human-AI Teaming in Smart Manufacturing. In New Ideas and Emerging Results (ICSE-NIER'22), May 21–29, 2022, Pittsburgh, PA, USA. ACM, New York, NY, USA, [[5]](#ref-5) pages. <https://doi.org/10.1145/3510455.3512788>

### 1 INTRODUCTION

Applications of AI in smart manufacturing are manifold, ranging from improving maintenance times of machinery, the detection of failures in the product or the machinery to the prevention of harm to manufacturing operators. In general, complex processes that are worked on collaboratively are characterized by a sequence of reactive and proactive elements, which each actor alternatingly supporting the other. AI-enabled systems in smart manufacturing are capable of self-sensing, self-adaptation, self-organization, and self-decision [[17]](#ref-17), [[20]](#ref-20), allowing them to respond to physical changes in the production environment in various ways - by stopping machines, adapting production tasks, or suggesting the change of production parameters. However, effective teaming between manufacturing operators and AI-enabled manufacturing systems requires mutual trust into the other's capabilities, primarily resulting from self-sensing and self-adaption. With regards to collaborative AI systems, this demands a high degree of situational awareness for each other actor's needs, knowledge of the production process, and its adjustable parameters.

From a higher perspective, two main challenges related to teaming AI and manufacturing operators in smart manufacturing can be identified: The first challenge relates to the required scalability of the architecture when processing data in near-realtime, particulary in combination with relational machine learning, i.e., the statistical analysis of relational, or graph-structured, data [[16]](#ref-16). The second challenge relates to examining a suitable framework to explicate the knowledge for effective teaming in the manufacturing process. Shared mental models capture the common ground knowledge in the collaboration between humans with robots [[5]](#ref-5), [[11]](#ref-11), [[26]](#ref-26). We use knowledge graphs and ontologies to formalize these shared mental

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

models of the manufacturing process and the semantics of trust factors for human-AI teaming in an operational manner.

In this paper we first present the initial reference software architecture as one important contribution of the Teaming.AI [[1]](#ref-1) project. The remainder of the paper is structured as follows: First we sketch the envisioned approach based on a use case from one of the industrial partners in Section [[2]](#ref-2), before we elaborate the identified challenges for such a reference architecture in Section [[3]](#ref-3). Afterwards, we present the current status of this software architecture in Section [[4]](#ref-4). Finally, we sketch our next research activities and conclude the paper in Section [[5]](#ref-5).

### 2 ENVISIONED APPROACH

One of our industrial partners specializes in high-precision machining of large-sized parts by milling or grinding based on cast materials or machine-welded structures. Manufacturing operators must manually clamp large and heavy parts into high-precision manufacturing machines to perform grinding or milling operations. This process takes up a large portion of the total cycle time of a work order and workers are exposed to occupational hazards. A reliable full automation by an AI-assisted robotic system is beyond the capabilities of current AI-based technologies, due to large part variety and the complexity of the associated handling processes.

By compensating for the limited visual perception of both actors in the manufacturing process - the manufacturing operator and the AI system - we seek to maximize awareness of hazardous situations and conditions that negatively impact physical or mental ergonomics. Based on human feedback, the AI system learns to predict which action sequences are ergonomically favorable. However, since the AI-augmented manufacturing system cannot be sure that it has the complete information about the situation due to occlusions and unseen areas, it expresses its confidence to the manufacturing operator by, for example, displaying safety warnings. The system fuses observational data from a visual tracking system with prior knowledge about the scene and process with in-process feedback from the manufacturing operator. Obviously, for such a system to gain the trust from the manufacturing operator, not only the correctness, and context-dependent suitability are critical success factors, but also the timely provision of recommended actions or the display of safety warnings. Of course, such a system must also comply with ethical policies and standards, which the manufacturing operator also tacitly assumes.

The general approach envisioned in our research project uses these data for machine learning and the development of a context-aware AI-augmented manufacturing system. Thereby, prior knowledge about the scene, geometry of the parts, and compositional workflow patterns for the handling and processing steps are encoded in a knowledge graph, along with safety guidelines. The knowledge graph is updated at runtime with current contextual information. An integrated self-diagnostic component simultaneously assesses the system's level of consistency and completeness and expresses its epistemic confidence. In case of ambiguity, the manufacturing operator is asked for feedback.

From a functional perspective, the teaming of manufacturing operators and AI in an industrial manufacturing process raises specific challenges related to relational machine learning, processing IIoT streaming data, the modeling and monitoring of trust (factors), and the continuous evaluation of human feedback and compliance with ethical policies. From a non-functional perspective, scalability and timing requirements of the components play a special role for meeting the functional requirements in such a system.

### 3 RESEARCH CHALLENGES

In multiple workshops over the course of six months our research consortium identified five core challenges relevant for a reference architecture for human-AI teaming in smart manufacturing. These workshops involved researchers from software engineering (3), knowledge engineering (3), machine learning (4), computer vision (2), vision systems (2), and human factors (1) and domain experts from the companies, such as production and quality managers.

1 Monitoring of Teaming Aspects in Human-AI Interaction. Salsas et al. in [[24]](#ref-24) identified five core components that are necessary for effective teamwork. In addition, shared mental models [[11]](#ref-11), mutual trust, and closed-loop communication serve as coordination mechanism between the actors. We use these concepts as foundation for modeling the manufacturing process as alternating activities between the manufacturing operator and the AI-augmented manufacturing system. Further, we rely on the 4S Interdependence Framework to define the neccessary state, structural organization, skills, and strategy for each actor and activitiy in the smart manufacturing process. The monitoring of these aspects, e.g., through mining event logs or scene detection through a tracking and scene analysis system, is the main challenge in this context.

2 Scalability for Near-Realtime IIoT Data Processing. In smart manufacturing, streaming data acquired from IIoT sensors continuously need to be processed so that they can be used for machine learning. Thus, the scalability of a reference architecture [[12]](#ref-12), [[25]](#ref-25) remains a key challenge in this context as delayed or incorrect recommendations of the AI systems to manufacturing operators may delay the workflow or, even worse, can also endanger their safety. In this context we research on appropriate consistency requirements in the face of data sharding between different replicas to better cope with typical data volumes in this context.

3 Runtime Monitoring and Validation of Ethical Policies Formalizing ethical and standards in an operational manner and validating their fulfillment by an AI system at runtime remains a key challenge [[6]](#ref-6), [[9]](#ref-9), [[29]](#ref-29), [[30]](#ref-30) in this context. The continuous validation of fulfillment of these policies and standards is exacerbated by the fact that they can only be evaluated at runtime. In our research we aim on developing a formalism based on ontology-reasoning to express these policies and standards in an operational manner.

4 Relational Machine Learning for Knowledge Graphs. The first research challenge relates to examining different approaches for calculating graph embeddings and their respective computational costs [[16]](#ref-16), [[28]](#ref-28). Second, for the development of the framework abstraction layer, the required functionalities for orchestrated machine learning need to be identified, which is the main challenge in this context. Subsequently, generic interfaces covering these common functionalities can be derived thereof.

^1^https://www.teamingai-project.eu

5 Experimentation of Data and Algorithms. The automatization of experiments requires an operational definition of the experiments' evaluation criteria, the parameterization of required data pipelines and machine learning algorithms, and the configuration of their deployment and execution. Thus, the research challenge comprises the development of domain-specific languages to describe and evaluate these experiments based on quality factors of AI-based systems [[27]](#ref-27) in an operational manner. Further it comprises the development of respective tooling for automatizing the evaluation of the experiments [[3]](#ref-3), [[15]](#ref-15) that also integrates qualitative expert feedback from the human-in-the-loop (HITL).

## 4 PRELIMINARY STATUS OF THE REFERENCE SOFTWARE ARCHITECTURE

Based on the aforementioned challenges our research consortium developed a reference software architecture that serves as a blueprint for our subsequent research activities and validations. Though this architecture merges different viewpoints from researchers with software engineering and machine learning backgrounds, we expect subtle changes with progress of the research project. Thus, this description captures its preliminary status.

Figure [[1]](#ref-fig-1) shows the different components of this reference architecture. To account for the different latency requirements of the components to process the data in a streaming-like manner, we followed the Lambda architecture pattern as described by Warren and Marz [[31]](#ref-31). This architectural pattern groups the components based on their latency requirements into three layers. The batch layer (model authoring) ingests and stores large amounts of data, the speed layer (knowledge graph, graph-based ML and teaming engine, production line systems) processes updates to the data in low-latency, and the serving layer (operation support, ML experimentation, introspection & policy monitoring) provides precalculated results also in a low-latency fashion [[19]](#ref-19). To separate read and write operations and therewith be able to balance the processing of large data volumes, all data stores used in the architecture (i.e., dynamic knowledge graph, time series, and media data) are replicated as read and write shards. The synchronization between these replicas is performed autonomously by the synchronization management component.

### 1 Model Authoring & Import

Product- and process specific models for the manufacturing process are imported into the knowledge graph by means of batches. In this regard, importing might also comprise to convert these domain-specific models into a graph representation such as RDF (Resource Description Framework). This component also embodies the functionality needed for authoring and versioning the models.

### 2 ML Experimentation

During the continuous improvement and testing of AI-based systems, huge amounts of data are generated that can be used for targeted experiments with these systems [[1]](#ref-1), [[2]](#ref-2). Particularly, the indeterministic nature of data-driven algorithms and their entanglement with the used training data underpins the need for continuous experimentation and validation of AI components.

### 3 Introspection & Policy Monitoring

Explainability of AI (XAI) [[23]](#ref-23), ethics-based auditability [[14]](#ref-14), and the alignment with human rights and autonomy [[8]](#ref-8) are common examples for ethical requirements towards AI systems. In recent years, several policies and guidelines have been presented by companies, e.g., Google [[18]](#ref-18), governmental bodies, e.g., the EU [[7]](#ref-7), and standardization organizations, e.g., from IEEE [[8]](#ref-8). The compliance with these standards and policies needs to be assured throughout the operation of any AI-enabled software system. To this end, this component encapsulates introspection capabilities, i.e., the self-directed evaluation of the AI system by itself, and additional monitoring and validation facilities related to ethical standards and policies. While introspection is triggered ad-hoc, e.g., upon the detection of suspicious interaction patterns, monitoring and validation is performed continuously at runtime. To also take into account historical data when evaluating the compliance with ethical policies, all processed events are stored in the event store.

### 4 Knowledge Graph

Due to the emerging use of knowledge graphs to represent ontologies and semantic data, they also become increasingly important to formalize expert knowledge, process, and simulation data in manufacturing [[13]](#ref-13). Based on the frequency of updates to the data, the reference architecture differentiates between a dynamic and a static knowledge subgraph. Models related to the product, the manufacturing process, and to experimentation are static in the sense that they do not need to be continuously updated at runtime. These data are embodied in the static subgraph. The dynamic subgraph on the other hand covers operational data accruing in the manufacturing process itself [[21]](#ref-21), [[22]](#ref-22), augmented by added facts from relational machine learning to optimize the interplay between human and AI. This interplay can, e.g., be optimized by proactively giving the operator recommendations for the next manufacturing step or suggesting parameter changes for the machinery to respond to observed product quality deviations, detected by the AI systems.

### 5 Graph-based ML Engine

This component provides relational machine learning capabilities that focus on the application of machine learning methods onto relational or graph-structured data such as knowledge graphs. An essential prerequisite for this is the calculation of graph embeddings, i.e., the transfer of a graph representation into a vector space. to orchestrate complex machine learning tasks (e.g., via frameworks such as Kubeflow, TensorFlow Extended, or MLFlow) it provides a framework abstraction layer to make these frameworks accessible through a generic software interface.

### 6 Teaming Engine

The orchestration engine controls the reliable execution of the teaming process, which is defined in the teaming model. This model structures the concrete sequence of activities in the interaction between the AI system and the manufacturing operator. Also, it gives a framework to define which policies are relevant in a specific time period of the manufacturing process and to formalize the ground rules for team interaction, as described by the 4S Interdependence Framework of Johnson and Vera [[10]](#ref-10). For the orchestration of the

### ICSE-NIER'22, May 21–29, 2022, Pittsburgh, PA, USA

![Reference Software Architecture For Human-AI Teaming in Smart Manufacturing.](_page_3_Figure_1.jpeg)
**Figure 1:** Reference Software Architecture For Human-AI Teaming in Smart Manufacturing.

teaming process, two types of events are processed by the teaming engine: Raw events are extracted from the production line system through IIoT sensors, whereby teaming events are exchanged by the different components after processing. As a result, only teaming events contain contextual data. The orchestration engine can only work with teaming events, since the contextual data must also be evaluated to decide on the next manufacturing activity. The event translation merges several atomic events so that they can be used for decision-making by the orchestration engine.

### 7 Operation Support

The current situation on the shopfloor, i.e., the position of parts and movements of the manufacturing operator, machine settings, and their observed effects on production quality must be taken into account when giving recommendations to the manufacturing operator. Thereby, tracking and scene analysis (TSA) is provided by the situation awareness component, based on media data such as video, imagery or audio recordings. The system's self diagnosis evaluates the reliability of its recommendations and prematurely alerts upon violations of policies. The interplay of these components, the knowledge graph, and machine learning components for the calculation and selection of recommended actions to the manufacturing operator is controlled by the decision support component.

For the storage of near-realtime data acquired from the production line systems, a time series database is provided. Media data from the TSA system are persisted in the context media database.

### 8 Production Line Systems

Operational data from production and contextual systems, e.g., auxillary systems or manufacturing process control, are acquired from IIoT sensors or from machine-specific implementations, e.g., based on the OPC Unified Architecture [[4]](#ref-4). An HMI (Human Machine Interface) is provided to interact with the manufacturing operator, to gather context-dependent feedback about the relevance of given recommendations by the AI. Also, it allows to acquire information about unexpectedly taken actions by the manufacturing operator.

### 5 FUTURE WORK AND CONCLUSION

The presented reference software architecture is framework- and technology agnostic. It shall serve as a blueprint for deriving the software architecture for a particular manufacturing context in a producing company. We use this reference architecture to derive the concrete architecture for the AI-enabled smart manufacturing systems of our three industrial partners in the automotive, energy systems, and precision machining domain. Thus, all three companies have different manufacturing processes in place that result in diverging scalability and interoperability requirements of the software architecture. The validation of the reference architecture will investigate its applicability to different manufacturing contexts, its scalability, and its suitability for validating the compliance of ethical standards during operation. To examine its applicability we will conduct expert interviews with software architects of our industrial partners after having applied the reference software architecture. Likewise, we will conduct interviews with manufacturing operators to assess the suitability of the overall approach and how well it supports the teaming between human and AI in smart manufacturing. Complementary, the quantitative validation will use data acquired from runtime probes to examine the scalability and the consistency among the data shards under heavy load.

## 6 ACKNOWLEDGEMENTS

This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No 957402.

Towards a Reference Software Architecture for Human-AI Teaming in Smart Manufacturing ICSE-NIER'22, May 21–29, 2022, Pittsburgh, PA, USA

### REFERENCES

* <a id="ref-1"></a>[1] Saleema Amershi, Andrew Begel, Christian Bird, Robert DeLine, Harald Gall, Ece Kamar, Nachiappan Nagappan, Besmira Nushi, and Thomas Zimmermann. 2019. Software Engineering for Machine Learning: A Case Study. In 2019 IEEE/ACM 41st International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP). 291–300. <https://doi.org/10.1109/ICSE-SEIP.2019.00042>
* <a id="ref-2"></a>[2] Anders Arpteg, Björn Brinne, Luka Crnkovic-Friis, and Jan Bosch. 2018. Software Engineering Challenges of Deep Learning. In 2018 44th Euromicro Conference on Software Engineering and Advanced Applications (SEAA). 50–59. <https://doi.org/10.1109/SEAA.2018.00018>
* <a id="ref-3"></a>[3] Jan Bosch, Ivica Crnkovic, and Helena Holmström Olsson. 2020. Engineering AI Systems: A Research Agenda. arXiv:2001.07522 [cs] (2020). <http://arxiv.org/abs/2001.07522> arXiv: 2001.07522.
* <a id="ref-4"></a>[4] OPC Foundation. 2008. What is OPC? <https://opcfoundation.org/about/what-is-opc/> Accessed 2022-01-13.
* <a id="ref-5"></a>[5] Felix Gervits, Terry W. Fong, and Matthias Scheutz. 2018. Shared Mental Models to Support Distributed Human-Robot Teaming in Space. In 2018 AIAA SPACE and Astronautics Forum and Exposition. American Institute of Aeronautics and Astronautics. <https://doi.org/10.2514/6.2018-5340>
* <a id="ref-6"></a>[6] Thilo Hagendorff. 2020. The Ethics of AI Ethics: An Evaluation of Guidelines. Minds and Machines 30, 1 (2020), 99–120. <https://doi.org/10.1007/s11023-020-09517-8>
* <a id="ref-7"></a>[7] HLEG. 2019. Ethics guidelines for trustworthy AI | Shaping Europe's digital future. <https://digital-strategy.ec.europa.eu/en/library/ethics-guidelines-trustworthy-ai> Accessed 2022-01-13.
* <a id="ref-8"></a>[8] IEEE. 2019. IEEE Global A/IS Ethics Initiative. <https://standards.ieee.org/industry-connections/ec/autonomous-systems.html> Accessed 2022-01-13.
* <a id="ref-9"></a>[9] Brittany Johnson and Justin Smith. 2021. Towards Ethical Data-Driven Software: Filling the Gaps in Ethics Research & Practice. In 2021 IEEE/ACM 2nd International Workshop on Ethics in Software Engineering Research and Practice (SEthics). 18–25. <https://doi.org/10.1109/SEthics52569.2021.00011>
* <a id="ref-10"></a>[10] Matthew Johnson and Alonso Vera. 2019. No AI Is an Island: The Case for Teaming Intelligence. AI Magazine 40, 1 (2019), 16–28. <https://doi.org/10.1609/aimag.v40i1.2842>
* <a id="ref-11"></a>[11] Catholijn M. Jonker, M. Birna van Riemsdijk, and Bas Vermeulen. 2011. Shared Mental Models. In Coordination, Organizations, Institutions, and Norms in Agent Systems VI (Lecture Notes in Computer Science), Marina De Vos, Nicoletta Fornara, Jeremy V. Pitt, and George Vouros (Eds.). Springer, Berlin, Heidelberg, 132–151. <https://doi.org/10.1007/978-3-642-21268-0_8>
* <a id="ref-12"></a>[12] Ruhul Amin Khalil, Nasir Saeed, Mudassir Masood, Yasaman Moradi Fard, Mohamed-Slim Alouini, and Tareq Y. Al-Naffouri. 2021. Deep Learning in the Industrial Internet of Things: Potentials, Challenges, and Emerging Applications. IEEE Internet of Things Journal 8, 14 (2021), 11016–11040. <https://doi.org/10.1109/JIOT.2021.3051414>
* <a id="ref-13"></a>[13] Franz Georg Listl, Jan Fischer, Dagmar Beyer, and Michael Weyrich. 2020. Knowledge Representation in Modeling and Simulation: A survey for the production and logistic domain. In 2020 25th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA), Vol. 1. 1051–1056. <https://doi.org/10.1109/ETFA46521.2020.9211994>
* <a id="ref-14"></a>[14] Jakob Mökander, Jessica Morley, Mariarosaria Taddeo, and Luciano Floridi. 2021. Ethics-Based Auditing of Automated Decision-Making Systems: Nature, Scope, and Limitations. Science and Engineering Ethics 27, 4 (2021), 44. <https://doi.org/10.1007/s11948-021-00319-4>
* <a id="ref-15"></a>[15] Anh Nguyen-Duc and Pekka Abrahamsson. 2020. Continuous experimentation on artificial intelligence software: a research agenda. In Proceedings of the 28th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE 2020). Association for Computing Machinery, New York, NY, USA, 1513–1516. <https://doi.org/10.1145/3368089.3417039>
* <a id="ref-16"></a>[16] Maximilian Nickel, Kevin Murphy, Volker Tresp, and Evgeniy Gabrilovich. 2016. A Review of Relational Machine Learning for Knowledge Graphs. Proc. IEEE 104, 1 (2016), 11–33. <https://doi.org/10.1109/JPROC.2015.2483592>
* <a id="ref-17"></a>[17] Sudip Phuyal, Diwakar Bista, and Rabindra Bista. 2020. Challenges, Opportunities and Future Directions of Smart Manufacturing: A State of Art Review. Sustainable Futures 2 (2020), 100023. <https://doi.org/10.1016/j.sftr.2020.100023>
* <a id="ref-18"></a>[18] S Pichai. 2018. AI at Google: our principles. <https://blog.google/technology/ai/ai-principles/> Accessed 2022-01-13.
* <a id="ref-19"></a>[19] Davy Preuveneers, Yolande Berbers, and Wouter Joosen. 2016. SAMURAI: A batch and streaming context architecture for large-scale intelligent applications and environments. Journal of Ambient Intelligence and Smart Environments 8, 1 (2016), 63–78. <https://doi.org/10.3233/AIS-150357>
* <a id="ref-20"></a>[20] Y. J. Qu, X. G. Ming, Z. W. Liu, X. Y. Zhang, and Z. T. Hou. 2019. Smart manufacturing systems: state of the art and future trends. The International Journal of Advanced Manufacturing Technology 103, 9 (2019), 3751–3768. <https://doi.org/10.1007/s00170-019-03754-7>
* <a id="ref-21"></a>[21] Martin Ringsquandl, E. Kharlamov, Daria Stepanova, Marcel Hildebrandt, S. Lamparter, R. Lepratti, I. Horrocks, and Peer Kröger. 2018. Filling Gaps in Industrial Knowledge Graphs via Event-Enhanced Embedding. In Proceedings of ISWC 2018 Posters & Demonstrations, Industry and Blue Sky Ideas Tracks co-located with 17th International Semantic Web Conference (ISWC 2018). CEUR Workshop Proceedings (CEUR-WS.org). <http://ceur-ws.org/Vol-2180/paper-52.pdf> Accessed 2022-01-13.
* <a id="ref-22"></a>[22] Martin Ringsquandl, Evgeny Kharlamov, Daria Stepanova, Steffen Lamparter, Raffaello Lepratti, Ian Horrocks, and Peer Kröger. 2017. On event-driven knowledge graph completion in digital factories. In 2017 IEEE International Conference on Big Data (Big Data). 1676–1681. <https://doi.org/10.1109/BigData.2017.8258105>
* <a id="ref-23"></a>[23] Cynthia Rudin. 2019. Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead. Nature Machine Intelligence 1, 5 (2019), 206–215. <https://doi.org/10.1038/s42256-019-0048-x>
* <a id="ref-24"></a>[24] Eduardo Salas, Dana E. Sims, and C. Shawn Burke. 2005. Is there a "Big Five" in Teamwork? Small Group Research 36, 5 (2005), 555–599. <https://doi.org/10.1177/1046496405277134>
* <a id="ref-25"></a>[25] Nuno Santos, Francisco Morais, Helena Rodrigues, and Ricardo J. Machado. 2019. Systems Development for the Industrial IoT: Challenges from Industry R&D Projects. In The Internet of Things in the Industrial Sector: Security and Device Connectivity, Smart Environments, and Industry 4.0, Zaigham Mahmood (Ed.). Springer International Publishing, Cham, 55–78. <https://doi.org/10.1007/978-3-030-24892-5_3>
* <a id="ref-26"></a>[26] Matthias Scheutz, Scott A. DeLoach, and Julie A. Adams. 2017. A Framework for Developing and Using Shared Mental Models in Human-Agent Teams. Journal of Cognitive Engineering and Decision Making 11, 3 (2017), 203–224. <https://doi.org/10.1177/1555343416682891>
* <a id="ref-27"></a>[27] Julien Siebert, Lisa Jöckel, Jens Heidrich, Koji Nakamichi, Kyoko Ohashi, Isao Namba, Rieko Yamamoto, and Mikio Aoyama. 2020. Towards Guidelines for Assessing Qualities of Machine Learning Systems. In Quality of Information and Communications Technology - 13th International Conference, QUATIC 2020, Faro, Portugal, September 9-11, 2020, Proceedings (Communications in Computer and Information Science, Vol. 1266), Martin J. Shepperd, Fernando Brito e Abreu, Alberto Rodrigues da Silva, and Ricardo Pérez-Castillo (Eds.). Springer, 17–31. <https://doi.org/10.1007/978-3-030-58793-2_2>
* <a id="ref-28"></a>[28] Théo Trouillon, Christopher R. Dance, Éric Gaussier, Johannes Welbl, Sebastian Riedel, and Guillaume Bouchard. 2017. Knowledge graph completion via complex tensor factorization. The Journal of Machine Learning Research 18, 1 (2017), 4735– 4772.
* <a id="ref-29"></a>[29] Ville Vakkuri, Kai-Kristian Kemell, and Pekka Abrahamsson. 2019. Ethically Aligned Design: An Empirical Evaluation of the RESOLVEDD-Strategy in Software and Systems Development Context. In 2019 45th Euromicro Conference on Software Engineering and Advanced Applications (SEAA). 46–50. <https://doi.org/10.1109/SEAA.2019.00015>
* <a id="ref-30"></a>[30] Ville Vakkuri, Kai-Kristian Kemell, Marianna Jantunen, Erika Halme, and Pekka Abrahamsson. 2021. ECCOLA — A method for implementing ethically aligned AI systems. Journal of Systems and Software 182 (2021), 111067. <https://doi.org/10.1016/j.jss.2021.111067>
* <a id="ref-31"></a>[31] James Warren and Nathan Marz. 2015. Big Data: Principles and best practices of scalable realtime data systems (1st edition). Manning.

## Metadata Summary
### Research Context
- **Research Question**: How can software architecture effectively support human-AI teaming in smart manufacturing environments while addressing scalability, ethics, and real-time processing requirements?
- **Methodology**: Reference architecture design methodology; Lambda architecture pattern implementation; Knowledge graph engineering with static/dynamic separation; Relational machine learning integration; Multi-domain validation planning across automotive, energy systems, and precision machining; Expert workshop analysis with researchers from software engineering, knowledge engineering, machine learning, computer vision, and human factors
- **Key Findings**: Lambda architecture successfully addresses different latency requirements through three-layer organization; Knowledge graphs effectively capture manufacturing knowledge with separation of static models and dynamic operational data; Relational machine learning enables context-specific recommendations and safety warnings; Architecture demonstrates scalability potential for near-realtime IIoT data processing; Framework provides systematic approach to runtime ethical policy monitoring; Teaming engine successfully orchestrates human-AI interaction workflows
- **Primary Outcomes**: Reference software architecture for human-AI teaming in smart manufacturing; Lambda architecture pattern implementation with batch/speed/serving layers; Knowledge graph framework with static/dynamic subgraph separation; Relational machine learning integration system; Teaming engine for orchestrating human-AI collaboration; Runtime ethical policy monitoring framework; Multi-domain validation methodology across three industrial sectors
   
### Analysis
- **Limitations**: Preliminary status without comprehensive empirical validation; Implementation complexity may challenge practical deployment; Scalability claims require quantitative validation under heavy load; Limited exploration of cross-domain knowledge transfer; Ethical policy formalization methodology needs further development; Architecture framework remains technology-agnostic requiring domain-specific instantiation
- **Research Gaps**: Need for comprehensive empirical validation across diverse manufacturing contexts; Limited quantitative analysis of scalability and consistency under heavy load; Insufficient exploration of cross-domain applicability and knowledge transfer; Missing detailed ethical policy formalization methodologies; Gap between reference architecture and concrete technology implementations
- **Future Work**: Validate reference architecture with three industrial partners in automotive, energy systems, and precision machining; Conduct expert interviews with software architects and manufacturing operators; Perform quantitative validation using runtime probes for scalability assessment; Develop concrete technology implementations; Enhance ethical policy monitoring frameworks
- **Conclusion**: Reference architecture provides viable framework for human-AI teaming in smart manufacturing; Lambda architecture pattern effectively addresses heterogeneous data processing requirements; Knowledge graph integration successfully captures manufacturing domain knowledge; Relational machine learning enables intelligent context-aware recommendations; Framework demonstrates potential for scalable real-time collaboration systems
   
### Implementation Notes
Lambda architecture provides proven pattern for managing different latency requirements in heterogeneous data environments; Static/dynamic knowledge graph separation offers effective schema organization for temporal-first architectures; Relational machine learning integration demonstrates practical approach for context-aware PKG systems; Teaming engine concept applicable to human-AI collaboration in HDM interfaces; Runtime policy monitoring framework relevant for ethical AI governance in personal data systems; Multi-domain validation approach provides template for bespoke PKG system evaluation