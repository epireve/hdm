---
cite_key: "zhao2024"
title: "AGENTiGraph: An Interactive Knowledge Graph Platform for LLM-based Chatbots Utilizing Private Data"
authors: "Xinjie Zhao, Moritz Blum, Rui Yang, Boming Yang, Tony Wang, Xin Li, Huitao Li, Yanran Fu, Rongrong Wang, Juntao Zhang, Irene Li, Weill Cornell Medicine"
year: 2024
doi: "arXiv:2410.11531"
url: "https://arxiv.org/abs/2410.11531"
relevancy: "High"
downloaded: "No"
tags:
  - "Multi-Agent Systems"
  - "LLM-KG Integration"
  - "Private Data Processing"
  - "Knowledge Management"
  - "Interactive Platforms"
tldr: "Multi-agent knowledge management platform enabling dynamic knowledge extraction, integration, and visualization for LLM-based chatbots using private data"
date_processed: "2025-07-02"
phase2_processed: true
original_folder: "arxiv_2410.11531_AGENTiGraph_An_Interactive_Knowledge_Graph_Platform_for_LLM-based_Chatbots_Utilizing_Private_Data"
images_total: 5
images_kept: 5
images_removed: 0
---

# <span id="page-0-0"></span>AGENTiGraph: An Interactive Knowledge Graph Platform for LLM-based Chatbots Utilizing Private Data

Xinjie Zhao<sup>1</sup> , Moritz Blum<sup>2</sup> , Rui Yang<sup>3</sup> , Boming Yang<sup>1</sup> , Luis Márquez Carpintero<sup>4</sup> , Mónica Pina-Navarro<sup>4</sup> , Tony Wang<sup>5</sup> , Xin Li<sup>3</sup> , Huitao Li<sup>3</sup> , Yanran Fu<sup>6</sup> , Rongrong Wang<sup>7</sup> , Juntao Zhang<sup>8</sup> , Irene Li<sup>1</sup>

<sup>1</sup> The University of Tokyo, <sup>2</sup> Universität Bielefeld, <sup>3</sup> Duke-NUS Medical School, <sup>4</sup> Universidad de Alicante, <sup>5</sup> Yale University, <sup>6</sup> Xiamen University, <sup>7</sup> Weill Cornell Medicine, <sup>8</sup> Henan University

## Abstract

Large Language Models (LLMs) have demonstrated capabilities across various applications but face challenges such as hallucination, limited reasoning abilities, and factual inconsistencies, especially when tackling complex, domain-specific tasks like question answering (QA). While Knowledge Graphs (KGs) have been shown to help mitigate these issues, research on the integration of LLMs with background KGs remains limited. In particular, user accessibility and the flexibility of the underlying KG have not been thoroughly explored. We introduce AGENTiGraph (Adaptive Generative ENgine for Task-based Interaction and Graphical Representation), a platform for knowledge management through natural language interaction. It integrates knowledge extraction, integration, and real-time visualization. AGENTi-Graph employs a multi-agent architecture to dynamically interpret user intents, manage tasks, and integrate new knowledge, ensuring adaptability to evolving user requirements and data contexts. Our approach demonstrates superior performance in knowledge graph interactions, particularly for complex domain-specific tasks. Experimental results on a dataset of 3,500 test cases show AGENTiGraph significantly outperforms state-of-the-art zero-shot baselines, achieving 95.12% accuracy in task classification and 90.45% success rate in task execution. User studies corroborate its effectiveness in real-world scenarios. To showcase versatility, we extended AGENTiGraph to legislation and healthcare domains, constructing specialized KGs capable of answering complex queries in legal and medical contexts. <sup>1</sup>

## 1 Introduction

Large Language Models (LLMs) have recently demonstrated remarkable capabilities in questionanswering (QA) tasks [\(Zhuang et al.,](#page-8-0) [2023;](#page-8-0) [Gao](#page-6-0)

[et al.,](#page-6-0) [2024;](#page-6-0) [Ke et al.,](#page-6-1) [2024;](#page-6-1) [Yang et al.,](#page-8-1) [2023\)](#page-8-1), showcasing their prowess in text comprehension, semantic understanding, and logical reasoning [\(Yang et al.,](#page-7-0) [2024a;](#page-7-0) [Srivastava et al.,](#page-7-1) [2024\)](#page-7-1). These models can process and respond to a wide range of queries with impressive accuracy and context awareness [\(Safavi and Koutra,](#page-7-2) [2021\)](#page-7-2). However, LLMs sometimes struggle with factual consistency and up-to-date information [\(Gao et al.,](#page-6-0) [2024;](#page-6-0) [Xu](#page-7-3) [et al.,](#page-7-3) [2024;](#page-7-3) [Augenstein et al.,](#page-6-2) [2024;](#page-6-2) [Yang et al.,](#page-7-4) [2024b\)](#page-7-4). This is where Knowledge Graphs (KGs) come into play [\(Edge et al.,](#page-6-3) [2024;](#page-6-3) [Nickel et al.,](#page-7-5) [2015\)](#page-7-5). By integrating KGs with LLMs, we can significantly enhance QA performance [\(Yang et al.,](#page-7-0) [2024a\)](#page-7-0). KGs provide structured, factual information that complements the broad knowledge of LLMs, improving answer accuracy, reducing hallucinations, and enabling more complex reasoning tasks [\(Li and Yang,](#page-6-4) [2023a,](#page-6-4)[b;](#page-6-5) [Pan et al.,](#page-7-6) [2024\)](#page-7-6). This synergy between LLMs and KGs opens up new possibilities for advanced, reliable, and context-aware QA systems [\(Yang et al.,](#page-8-2) [2024c\)](#page-8-2).

Despite the potential of KG-enhanced QA systems, current KG tools and query languages face significant challenges [\(Sabou et al.,](#page-7-7) [2017;](#page-7-7) [Li et al.,](#page-6-6) [2024\)](#page-6-6). Traditional systems like SPARQL and Cypher [\(Pérez et al.,](#page-7-8) [2009;](#page-7-8) [Francis et al.,](#page-6-7) [2018\)](#page-6-7), while powerful for data retrieval and analysis, often lack user-friendly interfaces and require specialized technical expertise [\(Castelltort and Martin,](#page-6-8) [2018\)](#page-6-8), which restricts their accessibility to a narrow audience of specialists. Moreover, these systems often struggle with contextual understanding and flexibility [\(Ji et al.,](#page-6-9) [2021\)](#page-6-9), making it difficult to handle nuanced or complex queries. The lack of seamless integration between KGs and natural language interfaces further complicates their use in conjunction with LLMs [\(Barbon Junior et al.,](#page-6-10) [2024\)](#page-6-10). Additionally, the absence of a unified system architecture among existing tools poses obstacles for developers aiming to innovate or build

<sup>1</sup>[The system demo video is available at:](#page-6-0) [https://](https://shorturl.at/qMSzM) [shorturl.at/qMSzM](#page-6-0).

upon these platforms [\(Wang et al.,](#page-7-9) [2023\)](#page-7-9). These challenges highlight the need for a more adaptive, user-friendly, and integrated approach to leveraging KGs in QA systems.

To address these challenges, we present AGENTiGraph (Adaptive General-purpose Entities Navigated Through Interaction), a novel platform that revolutionizes the interaction between LLMs and KGs using an agent-based approach. AGENTiGraph introduces innovative modules that enable seamless, intelligent interactions with knowledge graphs through natural language interfaces. Key features of our system include:

- Semantic Parsing. The interface optimizes user interaction by translating natural language queries (including free-form ones) into structured graph operations, enabling AGENTiGraph to process user requests with enhanced accuracy and speed. It reduces the complexity of interacting with knowledge graphs with an up-to-90% accuracy of automated recognition and realization of user intent tasks, ensuring efficient operation for users of all technical levels.
- Adaptive Multi-Agent System. AGENTi-Graph integrates multi-modal inputs such as user intent, query history, and graph structure for LLM agents to create coherent action plans that match user intent. Users can modify, pause, or reset tasks at any time, offering flexibility and ease of use. The modular design also allows easy model integration, module replacement and the design of custom agents for specific tasks by developers.
- Dynamic Knowledge Integration. The system supports continuous knowledge extraction and integration, ensuring the knowledge graph remains up-to-date. It also offers dynamic visualization capabilities, enabling users to explore and understand complex relationships within the data.

These innovations place AGENTiGraph at the forefront of knowledge graph technology. AGENTiGraph is not just a tool but a paradigm shift in how humans interact with and harness the power of knowledge graphs for complex data management and analysis tasks.

Contributions. (1) We implement a powerful natural language-driven interface that simplifies complex knowledge graph operations into user-friendly interactions; (2) We design an adap-

tive multi-agent system driven versatile knowledge graph management framework, enabling users to perform action on knowledge graphs freely while allowing developers to easily integrate LLMs or multimodal models for creating robust, taskoriented agents; (3) Experiments demonstrate the effectiveness of AGENTiGraph, achieving 95.12% accuracy in user intent identification and a 90.45% success rate in execution, outperforming state-ofthe-art zero-shot baselines. User studies further validate the system's efficiency, with participants highlighting its ability to deliver concise, focused answers and effectiveness in complex knowledge management tasks across diverse domains.

# 2 AGENTiGraph Framework Design

AGENTiGraph is designed to provide an intuitive and seamless interaction between users and knowledge graphs (G), the core of which is a humancentric approach that allows users to interact with the system using natural language inputs (q). We employ a multi-agent system to provide intuitive interaction between users and knowledge graphs, leveraging advanced LLM techniques. Each agent specializes in a specific task, collaboratively interpreting user input, decomposing it into actionable tasks, interacting with the knowledge graph, and generating responses (a).

User Intent Interpretation. The User Intent Agent is responsible for interpreting natural language input to determine the underlying intent (i). Utilizing Few-Shot Learning [\(Wang et al.,](#page-7-10) [2020a\)](#page-7-10) and Chain-of-Thought (CoT) [\(Wei et al.,](#page-7-11) [2024\)](#page-7-11) reasoning, it guides the LLM to accurately interpret diverse query types without extensive training data [\(Kwiatkowski et al.,](#page-6-11) [2019\)](#page-6-11), ensuring adaptability to evolving user needs.

Key Concept Extraction The Key Concept Extraction Agent performs Named Entity Recognition (NER) [\(Wang et al.,](#page-7-12) [2020b\)](#page-7-12) and Relation Extraction (RE) [\(Miwa and Bansal,](#page-7-13) [2016\)](#page-7-13) on the input (q). By presenting targeted examples to guide precise extraction, it then maps extracted entities (E) and relations (R) to the knowledge graph by semantic similarity with BERT-derived vector representations [\(Turton et al.,](#page-7-14) [2021\)](#page-7-14). This two-step process ensures accurate concept linking while maintaining computational efficiency.

Task Planning. The Task Planning Agent elevates the process by decomposing the identified

![](_page_2_Figure_0.jpeg)
<!-- Image Description: The image depicts a multi-agent framework for question answering. A flowchart shows a pipeline starting with user input, processed through task classification, key concept extraction, and knowledge graph fusion/construction agents. The framework uses a knowledge graph database for semantic data retrieval, visualized as interconnected nodes and databases. The output is an answer and visualization, displayed via an interactive query interface. Example prompt engineering for each agent is included. -->

Figure 1: AGENTiGraph Framework: A multi-agent system for intelligent KG interaction and management.

intent into a sequence of executable tasks (T = {t1, t2, ..., tn}). Leveraging CoT reasoning, this agent models task dependencies, optimizes execution order and then generates logically structured task sequences, which is particularly effective for complex queries requiring multi-step reasoning [\(Fu](#page-6-12) [et al.,](#page-6-12) [2023\)](#page-6-12).

Knowledge Graph Interaction. The Knowledge Graph Interaction Agent serves as a bridge, translating high-level tasks into executable graph queries. For each task (tk), it generates a formal query (ck), combining Few-Shot Learning with the Re-Act framework [\(Yao et al.,](#page-8-3) [2023\)](#page-8-3), which allows for dynamic query refinement based on intermediate results, adapting to various graph structures and query languages without extensive pre-training.

Reasoning. Enhancing raw query results (Rk), the Reasoning Agent applies logical inference, which capitalizes on the LLM's inherent contextual understanding and reasoning capabilities [\(Sun](#page-7-15) [et al.,](#page-7-15) [2024\)](#page-7-15). By framing reasoning as a series of logical steps, it enables flexible and adaptive inference across diverse reasoning tasks, bridging the gap between structured knowledge and natural language understanding.

Response Generation. The Response Generation Agent synthesizes processed information into coherent responses, which employs CoT, ReAct,

and Few-Shot Learning to orchestrate structured and contextually relevant responses, ensuring that responses are not only informative but also aligned with the user's original query context.

Dynamic Knowledge Integration. The Update Agent enables dynamic knowledge integration, incorporating new entities (Enew) and relationships (Rnew) into the existing graph: G ← G ∪ {Enew, Rnew}. This agent directly interfaces with the Neo4j database, using LLM-generated Cypher queries to seamlessly update the graph structure [\(Miller,](#page-7-16) [2013\)](#page-7-16).

Through this orchestrated multi-agent architecture, AGENTiGraph achieves a synergistic balance between structured knowledge representation and flexible interaction. Each agent, while utilizing similar underlying LLM technologies, is uniquely designed to address specific challenges in the knowledge graph interaction pipeline. The specific prompt design for each agent are provided in App. [A.](#page-9-0)

## 3 System Demonstration

### 1 User Interface

The AGENTiGraph interface is designed for intuitive use and efficient knowledge exploration, as illustrated in Figure [2.](#page-3-0) It features a dual-mode interaction paradigm that combines conversational AI capabilities with interactive knowledge exploration.

<span id="page-3-0"></span>![](_page_3_Figure_0.jpeg)
<!-- Image Description: The image depicts a system architecture with two modes: Chatbot and Exploration. The Chatbot mode shows knowledge graph reasoning for user queries, processing a query about the relationship between "penn treebank" and "first-order logic," visualized as a graph and culminating in a system response. The Exploration mode displays interactive knowledge exploration using knowledge graphs, enabling automated induction of related nodes and showcasing a local knowledge base with selectable topics like text generation and probability. Both modes feature knowledge graph visualizations. -->

Figure 2: AGENTiGraph's Dual-Mode Interface: Conversational AI with Interactive Knowledge Exploration

The interface consists of three main components:

- Chatbot Mode employs LLMs for intent interpretation and dynamic response construction via knowledge graph traversal. This mode facilitates nuanced query processing, bridging natural language input with complex knowledge structures.
- Exploration Mode provides an interactive knowledge graph visualization interface with entity recognition capabilities, supporting conceptual hierarchy navigation and semantic relationship exploration.
- Knowledge Graph Management Layer is the interface between the multi-agent system and the underlying Neo4j graph database, utilizing the Neo4j Bolt protocol for high-performance communication with the database and focusing on efficient graph operations and retrieval mechanisms for enhanced user interaction.

## <span id="page-3-1"></span>3.2 Task Design

To support user interaction with knowledge graphs and their diverse needs in knowledge exploration, AGENTiGraph provides a suite of pre-designed functionalities, inspired by the TutorQA, an expertverified TutorQA benchmark, designed for graph reasoning and question-answering in the NLP domain. [\(Yang et al.,](#page-8-2) [2024c\)](#page-8-2). Specifically, AGENTi-Graph supports the following tasks currently:

Relation Judgment: Users can explore and verify semantic relationships between concepts within a knowledge graph and the system would provide detailed explanations of these connections, enriching the graph with contextual information, which aids in developing a deeper understanding of complex knowledge structures and their interdependencies.

Prerequisite Prediction: When approaching complex topics, AGENTiGraph recommends prerequisite knowledge by analyzing the knowledge graph structure, helping users to identify and suggest foundational concepts and facilitating more effective learning paths and ensuring users build a solid foundation before advancing to more complex ideas.

Path Searching: This functionality enables users to discover personalized learning sequences between concepts. By generating optimal paths through the knowledge graph, AGENTiGraph helps users navigate from familiar concepts to new, related ideas, tailoring the learning journey to individual needs and interests.

Concept Clustering: Users can explore macrolevel knowledge structures, which group related concepts within a given domain. By revealing thematic areas and their interrelations, it provides a high-level overview of complex fields, aiding in comprehensive understanding and efficient knowledge navigation.

Subgraph Completion: This functionality assists users in expanding specific areas of the knowledge graph by identifying hidden associations between concepts in a subgraph, which supports the discovery of new connections and the enrichment of existing knowledge structures, promoting a more comprehensive understanding of the subject matter.

Idea Hamster: By synthesizing information from the knowledge graph, this feature helps users translate theoretical knowledge into practical applications, which supports the generation of project proposals and implementation strategies, fostering innovation and bridging the gap between abstract concepts and real-world problem-solving.

AGENTiGraph's flexibility extends beyond these predefined functionalities. Users can pose any question or request to the system, not limited to the six categories described above. The system automatically determines whether the user's input falls within these predefined categories. If not, it treats the input as a free-form query, employing a more flexible approach to address the user's specific needs. Moreover, users with specific requirements can design custom agents or reconfigure existing ones to create tailored functionalities, ensuring that AGENTiGraph can evolve to meet diverse and changing user needs, providing a versatile platform for both guided and open-ended knowledge discovery. In subsequent sections ([§5\)](#page-5-0), we also illustrate the system's scalability and expansion capabilities on other domains.

## 4 Evaluation

To assess AGENTiGraph's performance, we conducted a comprehensive evaluation focusing on two key aspects: (1) the system's ability to accurately identify user intents and execute corresponding tasks, and (2) the system's effectiveness and user satisfaction in real-world scenarios.

### 1 Dataset and Experimental Setup

To comprehensively evaluate AGENTiGraph's performance, we developed an expanded test set that addresses the limitations of the original TutorQA dataset, which comprises 3,500 cases, with 500 queries for each of the six predefined task types and an additional 500 free-form queries ([§3.2\)](#page-3-1). The dataset generation process involved using LLMs to mimic student questions [\(Liu et al.,](#page-7-17) [2024\)](#page-7-17), followed by human verification to ensure quality and relevance, allowing us to create a diverse set of

queries that closely resemble real-world scenarios [\(Extance,](#page-6-13) [2023\)](#page-6-13). Detailed prompts and example cases used in this process can be found in App. [B.](#page-16-0) Our evaluation of AGENTiGraph focuses on two key aspects: Query Classification: We assess the system's ability to correctly categorize user inputs into the seven task types (six predefined plus freeform), measured by accuracy and F1 score. Task Execution: We also evaluate its practical utility by testing whether it can generate valid outputs for each query, which is quantified through an execution success rate.

## 2 User Intent Identification and Task Execution

<span id="page-4-0"></span>

| Model          | Acc.   | F1     | Exec. Success |  |  |
|----------------|--------|--------|---------------|--|--|
| Zero-shot      |        |        |               |  |  |
| LLaMa 3.1-8b   | 0.6234 | 0.6112 | 0.5387        |  |  |
| LLaMa 3.1-70b  | 0.6789 | 0.6935 | 0.5912        |  |  |
| Gemini-1.5 pro | 0.8256 | 0.8078 | 0.7434        |  |  |
| GPT-4          | 0.7845 | 0.7463 | 0.7123        |  |  |
| GPT-4o         | 0.8334 | 0.8156 | 0.7712        |  |  |
| AGENTiGraph    |        |        |               |  |  |
| LLaMa 3.1-8b   | 0.8356 | 0.8178 | 0.7230        |  |  |
| LLaMa 3.1-70b  | 0.8789 | 0.8367 | 0.7967        |  |  |
| Gemini-1.5 pro | 0.9389 | 0.9323 | 0.8901        |  |  |
| GPT-4          | 0.9234 | 0.8912 | 0.8778        |  |  |
| GPT-4o         | 0.9512 | 0.9467 | 0.9045        |  |  |

| Table 1: Evaluation of task classification accuracy and |  |  |
|---------------------------------------------------------|--|--|
| execution success.                                      |  |  |

Table [1](#page-4-0) presents the results of our experiment. We evaluated AGENTiGraph's performance against zero-shot baselines using several stateof-the-art language models, which demonstrate AGENTiGraph's significant performance improvements across all evaluated models and metrics. GPT-4o, when integrated with AGENTiGraph framework, achieves the highest performance, with a 95.12% accuracy in task classification, 94.67% F1 score, and a 90.45% success rate in task execution, which represents a substantial improvement over its zero-shot counterpart. These improvements are consistent across all model sizes, with even smaller models like LLaMa 3.1-8b showing marked enhancements, suggesting that AGENTi-Graph's agent-based architecture effectively augments the capabilities of underlying language models, potentially offering more efficient solutions for complex knowledge graph interactions.

The performance gap between zero-shot and AGENTiGraph implementations narrows as model size increases, indicating that larger models benefit less dramatically from the AGENTiGraph framework. However, the consistent improvement across all models underscores the robustness of AGENTi-Graph's approach in enhancing knowledge graph interactions. Notably, there is a consistent gap between classification accuracy and execution success rates across all models, suggesting that while AGENTiGraph framework excels at identifying the correct task type, there's room for improvement in task execution. The gap is smallest for the most advanced models (GPT-4o and Gemini-1.5 pro), indicating that these models are better equipped to bridge the understanding-execution divide.

## 3 User Feedback and System Usability

To evaluate the real-world effectiveness and user satisfaction of AGENTiGraph, we conducted a comprehensive user study involving participants with varying levels of expertise in knowledge graph systems. Participants interacted with the system within the domain of natural language processing (NLP) and provided feedback on their experience. We collected qualitative feedback from 50 user interactions with AGENTiGraph, compared to ChatGPT-4o [2](#page-0-0) . Users generally found AGENTi-Graph's responses to be more concise. Specifically, 32 queries highlighted its ability to deliver shorter, more focused answers. However, in 5 queries, users noted that AGENTiGraph's responses were incomplete or missing key details, especially for more complex tasks, where ChatGPT's more detailed answers is preferred. Additionally, 4 queries indicated that AGENTiGraph misunderstood the question or provided incorrect answers. Despite the limitations, user satisfaction with AGENTiGraph remained high, particularly regarding the efficiency the freedon of knowledge graph interactions. For users familiar with core concepts, the concise responses helped avoid information overload, beneficial in learning or review scenarios.

We also analyzed 34 queries in computer vision domain, of which 14 were marked satisfactory, while 20 included suggestions for improvement, needing for more detailed explanations. Users often requested clearer descriptions of concepts like convolutional layers, optical flow, and feature extraction. For example, one suggestion emphasized the importance of explaining how convolutional filters slide across an image to generate feature maps. Detailed case studies in the App. [C.](#page-21-0)

## 5 Customized Knowledge Graph Extension

Our system is also extendable to private or personalized data. The code can be found at [https:](https://shorturl.at/axsPd) [//shorturl.at/axsPd](https://shorturl.at/axsPd). In this section, we showcase its ability to create knowledge graphs in a zero-shot manner within two complex domains: legal and medical.

UK Legislation Data. The first use case demonstrates the system's ability to generate a KG about the UK Legislation. As a knowledge source, we use the dataset *UK Legislation*published by [Chalkidis](#page-6-14) [et al.](#page-6-14) [\(2021\)](#page-6-14). We illustrate a sub-graph generated by our system in Fig. [4](#page-28-0) in App. [D.](#page-25-0) Potentially, it may be helpful to answer this question:*"What legislation provides the definition for the 'duty of excise' related to biodiesel, and which Act cites this duty?"*The system will allow users to identify relationships between legal provisions, definitions, and affected statutes.

Japanese Healthcare Data. The second use case is in the Japanese medical domain based on the*MMedC (Japanese)*[\(Qiu et al.,](#page-7-18) [2024\)](#page-7-18) corpus, comprising research and product information about medical treatments and healthcare technology written in Japanese. The small sub-graph shown in Fig. [5](#page-28-1) in App. [D](#page-25-0) reveals that chemotherapy, hematopoietic stem cell transplantation, and CAR-T cell therapy are treatments for blood tumors. Furthermore, CAR-T cell therapy is also used to treat non-Hodgkin's lymphoma and hematologic malignancies. For example, such a sub-graph is helpful to answer this question*"What treatments are used to address blood tumors and related hematologic conditions?"*Further details on the datasets, applications, and visualizations are available in App. [D.](#page-25-0)

## 6 Conclusion and Future Work

AGENTiGraph presents a novel approach to knowledge graph interaction, leveraging an adaptive multi-agent system to bridge the gap between LMMs and structured knowledge representations. Our platform significantly outperforms existing solutions in task classification and execution, demonstrating its potential to revolutionize complex knowledge management tasks across diverse domains. Future work will enhance multi-hop reasoning, optimize response conciseness and completeness, and develop continuous learning from user interactions.

<span id="page-5-0"></span><sup>2</sup> <https://chat.openai.com/>

## References

- <span id="page-6-2"></span>Isabelle Augenstein, Timothy Baldwin, Meeyoung Cha, Tanmoy Chakraborty, Giovanni Luca Ciampaglia, David Corney, Renee DiResta, Emilio Ferrara, Scott Hale, Alon Halevy, et al. 2024. Factuality challenges in the era of large language models and opportunities for fact-checking.*Nature Machine Intelligence*, pages 1–12.
- <span id="page-6-10"></span>Sylvio Barbon Junior, Paolo Ceravolo, Sven Groppe, Mustafa Jarrar, Samira Maghool, Florence Sèdes, Soror Sahri, and Maurice Van Keulen. 2024. [Are](https://doi.org/10.1145/3663741.3664785) [large language models the new interface for data](https://doi.org/10.1145/3663741.3664785) [pipelines?](https://doi.org/10.1145/3663741.3664785) In *Proceedings of the International Workshop on Big Data in Emergent Distributed Environments*, BiDEDE '24, New York, NY, USA. Association for Computing Machinery.
- <span id="page-6-16"></span>Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens Winter, Chris Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. 2020. Language models are few-shot learners. In *Advances in Neural Information Processing Systems*, volume 33, pages 1877–1901. Curran Associates, Inc.
- <span id="page-6-8"></span>Arnaud Castelltort and Trevor Martin. 2018. Handling scalable approximate queries over nosql graph databases: Cypherf and the fuzzy4s framework. *Fuzzy Sets and Systems*, 348:21–49.
- <span id="page-6-14"></span>Ilias Chalkidis, Manos Fergadiotis, Nikolaos Manginas, Eva Katakalou, and Prodromos Malakasiotis. 2021. [Regulatory compliance through Doc2Doc informa](https://doi.org/10.18653/v1/2021.eacl-main.305)[tion retrieval: A case study in EU/UK legislation](https://doi.org/10.18653/v1/2021.eacl-main.305) [where text similarity has limitations.](https://doi.org/10.18653/v1/2021.eacl-main.305) In *Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume*, pages 3498–3511, Online. Association for Computational Linguistics.
- <span id="page-6-3"></span>Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, and Jonathan Larson. 2024. [From local to global: A](https://arxiv.org/abs/2404.16130) [graph rag approach to query-focused summarization.](https://arxiv.org/abs/2404.16130) *Preprint*, arXiv:2404.16130.
- <span id="page-6-13"></span>Andy Extance. 2023. [Chatgpt has entered the class](https://www.nature.com/articles/d41586-023-03507-3)[room: how llms could transform education.](https://www.nature.com/articles/d41586-023-03507-3) *Nature*, 623:474–477.
- <span id="page-6-7"></span>Nadime Francis, Alastair Green, Paolo Guagliardo, Leonid Libkin, Tobias Lindaaker, Victor Marsault, Stefan Plantikow, Mats Rydberg, Petra Selmer, and Andrés Taylor. 2018. [Cypher: An evolving query](https://doi.org/10.1145/3183713.3190657) [language for property graphs.](https://doi.org/10.1145/3183713.3190657) In *Proceedings of the 2018 International Conference on Management of*

*Data*, SIGMOD '18, page 1433–1445, New York, NY, USA. Association for Computing Machinery.

- <span id="page-6-12"></span>Yao Fu, Hao Peng, Ashish Sabharwal, Peter Clark, and Tushar Khot. 2023. [Complexity-based prompting for](https://arxiv.org/abs/2210.00720) [multi-step reasoning.](https://arxiv.org/abs/2210.00720) *Preprint*, arXiv:2210.00720.
- <span id="page-6-0"></span>Fan Gao, Hang Jiang, Rui Yang, Qingcheng Zeng, Jinghui Lu, Moritz Blum, Tianwei She, Yuang Jiang, and Irene Li. 2024. [Evaluating large language mod](https://doi.org/10.18653/v1/2024.findings-acl.321)[els on Wikipedia-style survey generation.](https://doi.org/10.18653/v1/2024.findings-acl.321) In *Findings of the Association for Computational Linguistics ACL 2024*, pages 5405–5418, Bangkok, Thailand and virtual meeting. Association for Computational Linguistics.
- <span id="page-6-15"></span>Maarten Grootendorst. 2022. Bertopic: Neural topic modeling with a class-based tf-idf procedure. *arXiv preprint arXiv:2203.05794*.
- <span id="page-6-9"></span>Shaoxiong Ji, Shirui Pan, Erik Cambria, Pekka Marttinen, and S Yu Philip. 2021. A survey on knowledge graphs: Representation, acquisition, and applications. *IEEE transactions on neural networks and learning systems*, 33(2):494–514.
- <span id="page-6-1"></span>Yu He Ke, Rui Yang, Sui An Lie, Taylor Xin Yi Lim, Hairil Rizal Abdullah, Daniel Shu Wei Ting, and Nan Liu. 2024. Enhancing diagnostic accuracy through multi-agent conversations: Using large language models to mitigate cognitive bias. *arXiv preprint arXiv:2401.14589*.
- <span id="page-6-11"></span>Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, et al. 2019. Natural questions: a benchmark for question answering research. *Transactions of the Association for Computational Linguistics*, 7:453– 466.
- <span id="page-6-4"></span>Irene Li and Boming Yang. 2023a. [NNKGC: improving](https://ceur-ws.org/Vol-3559/paper-6.pdf) [knowledge graph completion with node neighbor](https://ceur-ws.org/Vol-3559/paper-6.pdf)[hoods.](https://ceur-ws.org/Vol-3559/paper-6.pdf) In *Proceedings of the Workshop on Deep Learning for Knowledge Graphs (DL4KG 2023) colocated with the 21th International Semantic Web Conference (ISWC 2023), Athens, November 6-10, 2023*, volume 3559 of *CEUR Workshop Proceedings*. CEUR-WS.org.
- <span id="page-6-5"></span>Irene Li and Boming Yang. 2023b. [Nnkgc: Improving](https://arxiv.org/abs/2302.06132) [knowledge graph completion with node neighbor](https://arxiv.org/abs/2302.06132)[hoods.](https://arxiv.org/abs/2302.06132) *Preprint*, arXiv:2302.06132.
- <span id="page-6-6"></span>Jinyang Li, Binyuan Hui, Ge Qu, Jiaxi Yang, Binhua Li, Bowen Li, Bailin Wang, Bowen Qin, Ruiying Geng, Nan Huo, Xuanhe Zhou, Chenhao Ma, Guoliang Li, Kevin C.C. Chang, Fei Huang, Reynold Cheng, and Yongbin Li. 2024. Can llm already serve as a database interface? a big bench for large-scale database grounded text-to-sqls. In *Proceedings of the 37th International Conference on Neural Information Processing Systems*, NIPS '23, Red Hook, NY, USA. Curran Associates Inc.

- <span id="page-7-17"></span>Lihui Liu, Blaine Hill, Boxin Du, Fei Wang, and Hanghang Tong. 2024. [Conversational question answer](https://doi.org/10.18653/v1/2024.findings-acl.48)[ing with language models generated reformulations](https://doi.org/10.18653/v1/2024.findings-acl.48) [over knowledge graph.](https://doi.org/10.18653/v1/2024.findings-acl.48) In *Findings of the Association for Computational Linguistics ACL 2024*, pages 839–850, Bangkok, Thailand and virtual meeting. Association for Computational Linguistics.
- <span id="page-7-16"></span>Justin J Miller. 2013. Graph database applications and concepts with neo4j. In *Proceedings of the southern association for information systems conference, Atlanta, GA, USA*, volume 2324, pages 141–147.
- <span id="page-7-13"></span>Makoto Miwa and Mohit Bansal. 2016. [End-to-end re](https://doi.org/10.18653/v1/P16-1105)[lation extraction using LSTMs on sequences and tree](https://doi.org/10.18653/v1/P16-1105) [structures.](https://doi.org/10.18653/v1/P16-1105) In *Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 1105–1116, Berlin, Germany. Association for Computational Linguistics.
- <span id="page-7-5"></span>Maximilian Nickel, Kevin Murphy, Volker Tresp, and Evgeniy Gabrilovich. 2015. A review of relational machine learning for knowledge graphs. *Proceedings of the IEEE*, 104(1):11–33.
- <span id="page-7-6"></span>Shirui Pan, Linhao Luo, Yufei Wang, Chen Chen, Jiapu Wang, and Xindong Wu. 2024. Unifying large language models and knowledge graphs: A roadmap. *IEEE Transactions on Knowledge and Data Engineering*.
- <span id="page-7-8"></span>Jorge Pérez, Marcelo Arenas, and Claudio Gutierrez. 2009. [Semantics and complexity of sparql.](https://doi.org/10.1145/1567274.1567278) *ACM Trans. Database Syst.*, 34(3).
- <span id="page-7-18"></span>Pengcheng Qiu, Chaoyi Wu, Xiaoman Zhang, Weixiong Lin, Haicheng Wang, Ya Zhang, Yanfeng Wang, and Weidi Xie. 2024. [Towards building multi](https://arxiv.org/abs/2402.13963)[lingual language model for medicine.](https://arxiv.org/abs/2402.13963) *Preprint*, arXiv:2402.13963.
- <span id="page-7-19"></span>Nils Reimers and Iryna Gurevych. 2019. Sentence-bert: Sentence embeddings using siamese bert-networks. In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing*. Association for Computational Linguistics.
- <span id="page-7-7"></span>Marta Sabou, Konrad Höffner, Sebastian Walter, Edgard Marx, Ricardo Usbeck, Jens Lehmann, and Axel-Cyrille Ngonga Ngomo. 2017. [Survey on challenges](https://doi.org/10.3233/SW-160247) [of question answering in the semantic web.](https://doi.org/10.3233/SW-160247) *Semant. Web*, 8(6):895–920.
- <span id="page-7-2"></span>Tara Safavi and Danai Koutra. 2021. [Relational world](https://arxiv.org/abs/2104.05837) [knowledge representation in contextual language](https://arxiv.org/abs/2104.05837) [models: A review.](https://arxiv.org/abs/2104.05837) *Preprint*, arXiv:2104.05837.
- <span id="page-7-1"></span>Pragya Srivastava, Manuj Malik, Vivek Gupta, Tanuja Ganu, and Dan Roth. 2024. [Evaluating llms' math](https://doi.org/10.18653/v1/2024.findings-acl.231)[ematical reasoning in financial document question](https://doi.org/10.18653/v1/2024.findings-acl.231) [answering.](https://doi.org/10.18653/v1/2024.findings-acl.231) In *Findings of the Association for Computational Linguistics ACL 2024*, pages 3853–3878, Bangkok, Thailand and virtual meeting. Association for Computational Linguistics.

- <span id="page-7-15"></span>Hongda Sun, Weikai Xu, Wei Liu, Jian Luan, Bin Wang, Shuo Shang, Ji-Rong Wen, and Rui Yan. 2024. [De](https://doi.org/10.18653/v1/2024.acl-long.531)[termLR: Augmenting LLM-based logical reasoning](https://doi.org/10.18653/v1/2024.acl-long.531) [from indeterminacy to determinacy.](https://doi.org/10.18653/v1/2024.acl-long.531) In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 9828–9862, Bangkok, Thailand. Association for Computational Linguistics.
- <span id="page-7-14"></span>Jacob Turton, Robert Elliott Smith, and David Vinson. 2021. [Deriving contextualised semantic fea](https://doi.org/10.18653/v1/2021.repl4nlp-1.26)[tures from BERT \(and other transformer model\) em](https://doi.org/10.18653/v1/2021.repl4nlp-1.26)[beddings.](https://doi.org/10.18653/v1/2021.repl4nlp-1.26) In *Proceedings of the 6th Workshop on Representation Learning for NLP (RepL4NLP-2021)*, pages 248–262, Online. Association for Computational Linguistics.
- <span id="page-7-9"></span>Lu Wang, Chenhan Sun, Chongyang Zhang, Weikun Nie, and Kaiyuan Huang. 2023. Application of knowledge graph in software engineering field: A systematic literature review. *Information and Software Technology*, page 107327.
- <span id="page-7-10"></span>Yaqing Wang, Quanming Yao, James T. Kwok, and Lionel M. Ni. 2020a. [Generalizing from a few exam](https://doi.org/10.1145/3386252)[ples: A survey on few-shot learning.](https://doi.org/10.1145/3386252) *ACM Comput. Surv.*, 53(3).
- <span id="page-7-12"></span>Yu Wang, Yining Sun, Zuchang Ma, Lisheng Gao, Yang Xu, and Ting Sun. 2020b. Application of pre-training models in named entity recognition. In *2020 12th International Conference on Intelligent Human-Machine Systems and Cybernetics (IHMSC)*, volume 1, pages 23–26. IEEE.
- <span id="page-7-11"></span>Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le, and Denny Zhou. 2024. Chain-of-thought prompting elicits reasoning in large language models. In *Proceedings of the 36th International Conference on Neural Information Processing Systems*, NIPS '22, Red Hook, NY, USA. Curran Associates Inc.
- <span id="page-7-3"></span>Rongwu Xu, Zehan Qi, Zhijiang Guo, Cunxiang Wang, Hongru Wang, Yue Zhang, and Wei Xu. 2024. [Knowledge conflicts for llms: A survey.](https://arxiv.org/abs/2403.08319) *Preprint*, arXiv:2403.08319.
- <span id="page-7-0"></span>Rui Yang, Haoran Liu, Edison Marrese-Taylor, Qingcheng Zeng, Yuhe Ke, Wanxin Li, Lechao Cheng, Qingyu Chen, James Caverlee, Yutaka Matsuo, and Irene Li. 2024a. [KG-rank: Enhancing large](https://doi.org/10.18653/v1/2024.bionlp-1.13) [language models for medical QA with knowledge](https://doi.org/10.18653/v1/2024.bionlp-1.13) [graphs and ranking techniques.](https://doi.org/10.18653/v1/2024.bionlp-1.13) In *Proceedings of the 23rd Workshop on Biomedical Natural Language Processing*, pages 155–166, Bangkok, Thailand. Association for Computational Linguistics.
- <span id="page-7-4"></span>Rui Yang, Yilin Ning, Emilia Keppo, Mingxuan Liu, Chuan Hong, Danielle S Bitterman, Jasmine Chiat Ling Ong, Daniel Shu Wei Ting, and Nan Liu. 2024b. Retrieval-augmented generation for generative artificial intelligence in medicine. *arXiv preprint arXiv:2406.12449*.

- <span id="page-8-2"></span>Rui Yang, Boming Yang, Sixun Ouyang, Tianwei She, Aosong Feng, Yuang Jiang, Freddy Lecue, Jinghui Lu, and Irene Li. 2024c. Graphusion: Leveraging large language models for scientific knowledge graph fusion and construction in nlp education. *arXiv preprint arXiv:2407.10794*.
- <span id="page-8-1"></span>Rui Yang, Qingcheng Zeng, Keen You, Yujie Qiao, Lucas Huang, Chia-Chun Hsieh, Benjamin Rosand, Jeremy Goldwasser, Amisha D Dave, Tiarnan DL Keenan, et al. 2023. Ascle: A python natural language processing toolkit for medical text generation. *arXiv e-prints*, pages arXiv–2311.
- <span id="page-8-3"></span>Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. 2023. [React: Synergizing reasoning and acting in language](https://arxiv.org/abs/2210.03629) [models.](https://arxiv.org/abs/2210.03629) *Preprint*, arXiv:2210.03629.
- <span id="page-8-4"></span>Takumi Yoshikoshi, Daisuke Kawahara, and Sadao Kurohashi. 2020. Multilingualization of a natural language inference dataset using machine translation (japanese). *The 244th Meeting of Natural Language Processing*.
- <span id="page-8-0"></span>Yuchen Zhuang, Yue Yu, Kuan Wang, Haotian Sun, and Chao Zhang. 2023. [Toolqa: A dataset for llm](https://arxiv.org/abs/2306.13304) [question answering with external tools.](https://arxiv.org/abs/2306.13304) *Preprint*, arXiv:2306.13304.

# <span id="page-9-0"></span>A Prompt Designs for AGENTiGraph Agents

## A.1 User Intent Interpretation Agent

## User Intent Interpretation Prompt

You are an expert NLP task classifier specializing in knowledge graph interactions. Your role is to interpret user intents from natural language queries using Few-Shot Learning and Chain-of-Thought reasoning. Analyze the given query and classify it into one of the following categories:

- 1. Relation Judgment
- 2. Prerequisite Prediction
- 3. Path Searching
- 4. Concept Clustering
- 5. Subgraph Completion
- 6. Idea Hamster
- 7. Freestyle NLP Question

Here are some examples to guide your classification:

## Example 1:

Query: "Is word embedding a prerequisite for understanding BERT?"

Classification: 1 (Relation Judgment)

Reasoning: This query asks about a specific relationship (prerequisite) between two NLP concepts. Example 2:

Query: "What should I learn before diving into transformer architectures?"

Classification: 2 (Prerequisite Prediction)

Reasoning: The query seeks prerequisites for a specific NLP concept.

## Example 3:

Query: "How do I progress from basic NLP to advanced natural language generation?" Classification: 3 (Path Searching)

Reasoning: This query asks for a learning path between two points in the NLP domain. Now, analyze the following query:

Query: {query}

{

}

Provide your analysis in the following JSON format:

```text
"key_concepts": ["list", "of", "identified", "concepts"],
"linguistic_analysis": "Brief description of query structure and intent indicators",
"task_classification": "number (1-7)",
"confidence": "percentage (0-100)",
"reasoning": "Explanation for your classification"
```text

Your final output should only be the valid JSON object.

## A.2 Key Concept Extraction Agent

## Key Concept Extraction Prompt

As an advanced NLP concept extractor, your task is to identify and extract key concepts, entities, and relationships from the given query using Named Entity Recognition (NER) and Relation Extraction (RE) techniques. You will then map these to the knowledge graph schema using BERT-derived vector representations for semantic similarity.

Here's an example of the extraction process:

Query: "How does BERT relate to transformer architecture in NLP?"

Extracted Information:

```text
{
  "entities": ["BERT", "transformer architecture"],
  "relations": [{"type": "relates_to", "source": "BERT", "target": "transformer architecture"}],
  "domain": "NLP"
}
```text

Now, perform the extraction for the following query:

Query: {query}

Task Type: {task\_type}

Provide the extracted information in the following JSON format based on the task type:

```text
For Relation Judgment (Task 1):
```text

```text
{
  "concept_1": "First concept",
  "concept_2": "Second concept",
  "relation": "Proposed relationship between concepts",
  "relation_description": "Description of the relationship, if provided"
}
For Prerequisite Prediction (Task 2):
{
  "target_concept": "Concept for which prerequisites are sought",
  "domain": "Specific NLP domain or subdomain, if mentioned"
}
Ensure that your extraction is precise and relevant to the given task type.
```text

## A.3 Task Planning Agent

## Task Planning Prompt

As the Task Planning Agent, your role is to decompose the identified user intent into a logical sequence of executable tasks for knowledge graph interaction. Create an optimal plan, considering task dependencies and execution order.

Here's an example of task planning for a complex query:

User Intent: Find the learning path from basic NLP to advanced machine translation

Extracted Concepts: ["basic NLP", "advanced machine translation"]

Task Type: 3 (Path Searching)

```text
Task Plan:
```text

- 1. Identify key concepts in basic NLP
- 2. Locate 'advanced machine translation' in the knowledge graph
- 3. Find intermediate concepts connecting basic NLP to advanced machine translation
- 4. Order concepts based on complexity and dependencies
- 5. Construct a step-by-step learning path

Now, create a task plan for the following: User Intent: {user\_intent} Extracted Concepts: {extracted\_concepts} Task Type: {task\_type} Provide your task plan in the following JSON format: { "goal\_analysis": "Brief description of the main query goal", "tasks": [ {"id": 1, "description": "Task 1 description", "dependencies": []}, {"id": 2, "description": "Task 2 description", "dependencies": [1]}, ... ], "execution\_strategy": "Description of optimal execution order", "potential\_challenges": ["Challenge 1", "Challenge 2", ...], "success\_criteria": "Definition of successful execution"

}

Ensure your plan is adaptable and can handle complex, multi-step reasoning if necessary.

## A.4 Knowledge Graph Interaction Agent

Knowledge Graph Interaction Prompt

As the Knowledge Graph Interaction Agent, your task is to translate high-level tasks into executable graph queries. Utilize Few-Shot Learning and the ReAct framework to generate and refine queries dynamically.

Here's an example of query generation:

Task: Find all papers that cite BERT and were published after 2018

Relevant Concepts: ["BERT", "citation", "publication date"]

Graph Schema:

```text
{
  "nodes": ["Paper", "Author", "Conference"],
  "relationships": ["CITES", "PUBLISHED_IN", "AUTHORED_BY"],
  "properties": {"Paper": ["title", "year"], "Author": ["name"], "Conference": ["name", "year"]}
}
```text

## Generated Query (Cypher):

MATCH (p1:Paper)-[:CITES]->(p2:Paper {title: 'BERT'}) WHERE p1.year > 2018 RETURN p1.title, p1.year ORDER BY p1.year DESC

Now, generate a query for the following task:

Task: {task}

Relevant Concepts: {concepts}

Graph Schema: {schema}

Provide your query plan in the following JSON format:

{

}

```text
"query_objective": "Brief statement of the query goal",
"cypher_query": "The full Cypher query string",
"query_explanation": "Explanation of the query components and logic",
"potential_optimizations": ["Optimization 1", "Optimization 2", ...],
"refinement_strategy": "Description of how the query might be refined based on results"
```text

Ensure that your query is efficient, adheres to the given graph schema, and can be dynamically adjusted based on intermediate results.

## A.5 Reasoning Agent

### Reasoning Agent Prompt

As the Reasoning Agent, your role is to apply logical inference to the raw query results, leveraging contextual understanding and reasoning capabilities. Bridge the gap between structured knowledge graph data and natural language understanding.

Here's an example of the reasoning process:

```text
Raw Query Results:
[
  {"paper": "Attention Is All You Need", "year": 2017, "citations": 50000},
  {"paper": "BERT", "year": 2018, "citations": 30000},
  {"paper": "GPT-3", "year": 2020, "citations": 10000}
```text

```text
]
```text

Original User Query: "How has the impact of transformer models evolved over time?" Reasoning:

- 1. The results show three significant papers in the transformer model timeline.
- 2. "Attention Is All You Need" introduced the transformer architecture in 2017.
- 3. BERT, which uses transformers, was published a year later and has substantial citations.
- 4. GPT-3, a more recent model, already has a high citation count despite being newer.
- 5. The increasing citation counts over time suggest growing impact and adoption of transformer models.

Now, apply reasoning to the following: Raw Query Results: {query\_results} Original User Query: {user\_query} Task Type: {task\_type} Provide your reasoning in the following JSON format:

```text
{
  "key_observations": ["Observation 1", "Observation 2", ...],
  "inferred_relationships": ["Relationship 1", "Relationship 2", ...],
  "logical_inferences": ["Inference 1", "Inference 2", ...],
  "contextual_interpretation": "Explanation of how insights relate to the original query",
  "confidence_assessment": "Percentage (0-100)",
  "conclusion": "Summary of key findings and their relevance to the user's intent"
}
```text

Ensure that your reasoning is clear, logically sound, and directly addresses the user's original query and intent.

### A.6 Response Generation Agent

## Response Generation Prompt

As the Response Generation Agent, your task is to synthesize all processed information into a coherent, contextually relevant response. Utilize Chain-of-Thought reasoning, ReAct framework, and Few-Shot Learning to craft an informative and user-friendly answer.

Here's an example of response generation:

User Query: "What are the key differences between BERT and GPT models?" Reasoning Results:

```text
{
  "key_points": [
    "BERT uses bidirectional context, GPT uses unidirectional",
    "BERT is primarily for understanding, GPT for generation",
    "Both use transformer architecture but with different objectives"
  ],
  "confidence": 95
}
```text

## Generated Response:

"BERT and GPT models, while both based on the transformer architecture, have key differences:

- 1. Context Processing: BERT uses bidirectional context, allowing it to understand words based on both left and right context. GPT, on the other hand, is unidirectional, processing text from left to right.
- 2. Primary Use: BERT is mainly used for understanding tasks like classification and question-answering. GPT excels in text generation tasks.
- 3. Training Objective: BERT is trained to predict masked words in a sentence, while GPT is trained to predict the next word in a sequence.

These differences make BERT more suited for tasks requiring deep language understanding, while GPT is better for tasks involving text generation or completion."

Now, generate a response for the following:

User Query: {user\_query} Identified Intent: {intent} Reasoning Results: {reasoning\_results} Task Type: {task\_type} Provide your response in the following JSON format: {

```text
"direct_answer": "A concise answer to the user's query",
  "detailed_explanation": "A more comprehensive explanation",
  "examples": ["Example 1", "Example 2", ...],
  "caveats": ["Caveat 1", "Caveat 2", ...],
  "further_exploration": ["Related topic 1", "Related topic 2", ...]
}
```text

Ensure that your response is informative, engaging, and aligned with the user's original intent. Balance technical accuracy with accessibility based on the inferred user expertise level.

## A.7 Dynamic Knowledge Integration Agent

Dynamic Knowledge Integration Prompt

As the Dynamic Knowledge Integration Agent, your role is to incorporate new entities and relationships into the existing knowledge graph. You'll interface directly with the Neo4j database using LLM-generated Cypher queries.

Here's an example of knowledge integration:

```text
New Information:
```text

```text
{
  "entity": "T5",
  "type": "LanguageModel",
  "properties": {"publication_year": 2020, "architecture": "transformer"},
  "relations": [
    {"type": "DEVELOPED_BY", "target": "Google"},
    {"type": "USED_FOR", "target": "TextToTextTasks"}
  ]
}
```text

## Existing Graph Schema:

```text
{
  "nodes": ["LanguageModel", "Organization", "Task"],
  "relationships": ["DEVELOPED_BY", "USED_FOR"],
  "properties": {"LanguageModel": ["name", "year", "architecture"]}
}
```text

## Integration Cypher Queries:

- 1. CREATE (t5:LanguageModel name: 'T5', year: 2020, architecture: 'transformer')
- 2. MATCH (t5:LanguageModel name: 'T5'), (org:Organization name: 'Google') CREATE (t5)- [:DEVELOPED\_BY]->(org)
- 3. MATCH (t5:LanguageModel name: 'T5'), (task:Task name: 'TextToTextTasks') CREATE (t5)-[:USED\_FOR]->(task)

Now, create an integration plan for the following:

## New Information: {new\_info}

Existing Graph Schema: {graph\_schema}

Provide your integration plan in the following JSON format:

```text
{
  "analysis": "Summary of the new information to be integrated",
  "integration_strategy": "Description of how the new information will be incorporated",
  "cypher_queries": [
    {"purpose": "Node creation", "query": "CREATE (...) ..."},
    {"purpose": "Relationship creation", "query": "MATCH (...) CREATE (...) ..."},
    ...
  ],
  "verification_queries": [
    {"purpose": "Verify node creation", "query": "MATCH (...) RETURN ..."},
    ...
  ],
  "conflict_resolution": "Strategy for resolving potential conflicts with existing data",
  "rollback_plan": "Steps to undo changes if integration fails"
}
```text

Ensure that your integration plan maintains the integrity and consistency of the knowledge graph while successfully incorporating the new information.

# <span id="page-16-0"></span>B Dataset Generation Process

## B.1 Overview

To comprehensively evaluate AGENTiGraph's performance, we generated an expanded test set consisting of 3,500 queries. This dataset includes 500 queries for each of the six predefined task types and an additional 500 free-form queries. The test queries were generated using Large Language Models (LLMs) to mimic student questions, followed by human verification to ensure quality and relevance.

In this appendix, we detail the process of generating these test queries, including the specific LLM prompts used for each task type and the human verification procedures employed to maintain the dataset's integrity.

# B.2 LLM Prompt Designs for Test Query Generation

For each task type, we carefully crafted specialized prompts to guide the LLMs in generating appropriate test queries. These prompts were designed to leverage prompt engineering strategies, incorporating clear instructions, relevant examples, and specifying the desired output format. The prompts were constructed to:

- Encourage the generation of queries covering a wide range of NLP topics, from foundational concepts to advanced techniques.
- Ensure that the language used in the queries is natural and reflects how a student might pose questions to an instructor or mentor.
- Include explicit instructions to avoid redundancy and promote diversity in the concepts and relationships addressed.
- Utilize examples to illustrate the desired style and format, enhancing the LLMs' understanding of the task.

By mdesigning these prompts, we sought to maximize the LLMs' ability to produce queries that are not only challenging and relevant but also varied in content and complexity, which contributes to a robust evaluation framework for AGENTiGraph, allowing us to assess its performance across different types of user interactions.

## B.2.1 Relation Judgment Queries

Enhanced Relation Judgment Query Generation Prompt

Task Description: Generate high-quality questions that ask about the existence or nature of relationships between two NLP concepts, suitable for testing the Relation Judgment capabilities of AGENTiGraph. Instructions for the LLM:

You are an expert in Natural Language Processing (NLP) education and assessment design. Your task is to generate diverse, challenging, and insightful questions where a student inquires about the relationship between two specific NLP concepts. Reasoning internally to ensure the relevance and correctness of the questions, but only output the final questions. The questions should:

- Cover a wide range of NLP topics, from foundational concepts to advanced techniques.
- Explicitly ask about the existence, importance, or nature of a relationship between two NLP concepts.
- Be phrased in natural, conversational language, reflecting how a student would ask.
- Avoid overlap with the provided examples and ensure diversity in concepts and relationships.

### Few-Shot Examples:

#### Example 1:

*Question:*"Is understanding word embeddings necessary for implementing neural machine translation models?" Example 2:
*Question:*"Does knowledge of morphological analysis contribute to better performance in lemmatization tasks?" Example 3:
*Question:*"Are recurrent neural networks related to sequence labeling in NLP applications?"

Now, generate 10 unique questions following these guidelines. Do not include any explanations or reasoning in your final output; only provide the questions.

## B.2.2 Prerequisite Prediction Queries

| Enhanced Prerequisite Prediction Query Generation Prompt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Task Description: Generate high-quality questions where a student seeks to know the prior knowledge or prerequi<br>sites needed before learning a particular NLP concept, suitable for testing the Prerequisite Prediction capabilities of<br>AGENTiGraph.<br>Instructions for the LLM:<br>You are an experienced NLP educator creating study guides for students. Generate diverse and thoughtful questions where<br>a student asks about the necessary background knowledge before tackling a specific NLP topic. Use Chain-of-Thought<br>reasoning to ensure the prerequisites are logical and appropriate, but only output the final questions.<br>The questions should: |
| • Focus on NLP concepts that typically require foundational knowledge.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| • Reflect a student's curiosity about what they need to learn first.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| • Be phrased naturally, as a student would ask their instructor or mentor.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| • Avoid repetition with the examples and cover a variety of NLP areas.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Few-Shot Examples:<br>Example 1:<br>Question: "What should I understand before learning about attention mechanisms in neural networks?"<br>Example 2:<br>Question: "Do I need a background in linguistics to study semantic role labeling?"<br>Example 3:<br>Question: "Is it important to know about convolutional neural networks before exploring text classification methods?"<br>Now, generate 10 unique questions following these guidelines. Only provide the questions in your final output.                                                                                                                                                                         |

## B.2.3 Path Searching Queries

### Enhanced Path Searching Query Generation Prompt

Task Description: Generate high-quality questions where a student asks for a learning path or sequence between two NLP concepts, suitable for testing the Path Searching capabilities of AGENTiGraph.

#### Instructions for the LLM:

As an NLP curriculum developer, craft questions where a student seeks guidance on progressing from one NLP concept to another more advanced concept. Use Chain-of-Thought reasoning to ensure the learning paths are feasible and pedagogically sound, but only output the final questions.

The questions should:

- Specify both a starting point and a target NLP concept.
- Reflect a desire to know the intermediate steps or topics needed to progress.
- Be phrased in a way that a student might ask for academic or career advice.
- Include a variety of starting and ending concepts across different NLP domains.

#### Few-Shot Examples:

#### Example 1:
*Question:*"How can I move from understanding basic sentiment analysis to developing conversational AI chatbots?" Example 2:
*Question:*"What steps should I follow to transition from learning POS tagging to mastering syntactic parsing?" Example 3:
*Question:*"Can you suggest a learning path from n-gram language models to transformer-based models like BERT?" Now, generate 10 unique questions following these guidelines. Only provide the questions in your final output.

## B.2.4 Concept Clustering Queries

| Enhanced Concept Clustering Query Generation Prompt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Task Description: Generate high-quality questions where a student asks about groups or clusters of related NLP concepts,<br>suitable for testing the Concept Clustering capabilities of AGENTiGraph.<br>Instructions for the LLM:<br>You are an NLP instructor helping students understand how different concepts are grouped within the field. Generate<br>questions where a student inquires about categories or clusters of related NLP topics. Use Chain-of-Thought reasoning to<br>ensure the clusters are coherent and meaningful, but only output the final questions.<br>The questions should: |
| • Seek information about groups of concepts, techniques, or methodologies.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| • Be phrased as a student trying to organize their knowledge or study plan.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| • Cover various NLP domains and encourage understanding of how concepts interrelate.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| • Be diverse and not overlap with the provided examples.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Few-Shot Examples:<br>Example 1:<br>Question: "What are the common techniques included in text normalization processes?"<br>Example 2:<br>Question: "Which algorithms are considered part of unsupervised learning in NLP?"<br>Example 3:<br>Question: "Can you tell me which NLP tasks are categorized under natural language understanding?"<br>Now, generate 10 unique questions following these guidelines. Only provide the questions in your final output.                                                                                                                                       |

## B.2.5 Subgraph Completion Queries

### Enhanced Subgraph Completion Query Generation Prompt

Task Description: Generate high-quality questions where a student wants to explore or complete parts of the knowledge graph related to specific NLP concepts, suitable for testing the Subgraph Completion capabilities of AGENTiGraph. Instructions for the LLM:

As an NLP mentor, create questions where a student is interested in discovering additional concepts or relationships connected to a particular NLP topic. Use Chain-of-Thought reasoning to ensure the suggestions are relevant and enhance the student's understanding, but only output the final questions.

The questions should:

- Focus on extending knowledge around a specific NLP concept or area.
- Encourage exploration of related topics or identification of missing links.
- Be phrased naturally, reflecting a student's desire to deepen their understanding.
- Include a range of concepts and avoid redundancy with the examples.

#### Few-Shot Examples:

#### Example 1:
*Question:*"After learning about named entity recognition, what other related topics should I study to enhance my skills?" Example 2:
*Question:*"Are there any lesser-known applications of dependency parsing that I should be aware of?" Example 3:
*Question:*"What concepts am I missing if I want to fully understand discourse analysis in NLP?"

Now, generate 10 unique questions following these guidelines. Only provide the questions in your final output.

## B.2.6 Idea Hamster Queries

### Enhanced Idea Hamster Query Generation Prompt

Task Description: Generate high-quality questions where a student seeks to apply theoretical knowledge to practical projects or is brainstorming ideas, suitable for testing the Idea Hamster capabilities of AGENTiGraph. Instructions for the LLM:

You are an NLP project advisor helping students connect theory to practice. Generate open-ended questions where a student is looking for innovative ways to apply NLP concepts in real-world scenarios. Use Chain-of-Thought reasoning to ensure the ideas are feasible and stimulating, but only output the final questions. The questions should:

- Encourage creative thinking and application of NLP concepts.
- Relate theoretical knowledge to practical use cases or projects.
- Be phrased as a student seeking inspiration or guidance on project ideas.
- Cover a variety of NLP applications and avoid repeating the examples.

#### Few-Shot Examples:

Example 1:
*Question:*"How can I utilize sentiment analysis to improve customer feedback systems?"

Example 2:
*Question:*"What are some innovative projects I can develop using question-answering models?"

Example 3:
*Question:*"Can I apply topic modeling to enhance recommendation systems, and if so, how?"

Now, generate 10 unique questions following these guidelines. Only provide the questions in your final output.

### B.2.7 Free-form Queries

### Enhanced Free-form Query Generation Prompt

Task Description: Generate diverse and high-quality questions on any NLP-related topic that do not necessarily fit into the predefined categories, suitable for testing the Freestyle NLP Question capabilities of AGENTiGraph. Instructions for the LLM:

As an NLP expert and educator, produce a variety of thoughtful and challenging questions that a student might ask about any aspect of NLP. Use Chain-of-Thought reasoning to ensure the questions are meaningful and cover a wide range of topics, but only output the final questions.

The questions should:

- Be varied in topic, complexity, and scope within the field of NLP.
- Reflect genuine curiosity or common challenges faced by learners.
- Be phrased naturally, as a student would ask.
- Avoid overlapping with previous examples and ensure diversity.

#### Few-Shot Examples:

Example 1:
*Question:*"What are the limitations of current NLP models when it comes to understanding context?"

Example 2:
*Question:*"How does transfer learning benefit NLP tasks, and can you provide some examples?"

#### Example 3:
*Question:*"What are the ethical considerations when deploying language models in social media platforms?" Now, generate 10 unique questions following these guidelines. Only provide the questions in your final output.

## B.3 Human Verification Process

Following the generation of queries using LLMs, we implemented a comprehensive human verification process to ensure the quality, relevance, and appropriateness of the test dataset. The verification process involved a team of NLP experts and educators who conducted a review of sampled queries. The process comprised several stages to uphold the highest standards of professionalism and academic rigor:

- 1. Relevance and Accuracy Assessment: Each query was evaluated to confirm that it directly pertains to NLP concepts and is appropriate for the intended task type. Reviewers checked for correct alignment with the task definitions and ensured that the queries were meaningful within the context of knowledge graph interactions.
- 2. Task Classification Validation: We verified that each query was correctly categorized according to the predefined task types.
- 3. Clarity and Linguistic Quality Check: Queries were examined for grammatical correctness, clarity, and naturalness. Reviewers ensured that the language used mirrored authentic student inquiries, enhancing the realism and practical applicability of the dataset.
- 4. Duplication and Redundancy Elimination: We identified and removed any duplicate or overly similar queries to maintain diversity and breadth in the dataset.
- 5. Content Appropriateness Review: The content of each query was scrutinized to avoid any sensitive, inappropriate, or disallowed topics. Reviewers ensured adherence to ethical standards and academic guidelines, guaranteeing that the dataset is suitable for scholarly use.
- 6. Inter-Rater Reliability Assessment: To ensure consistency and objectivity in the verification process, multiple reviewers independently evaluated a subset of the queries. The inter-rater agreement was measured, and any discrepancies were discussed and resolved through consensus.
- 7. Final Approval and Inclusion: Only queries that passed all the above checks were included in the final dataset. Queries that did not meet the criteria were either revised or discarded.

By implementing this human verification process, we ensured that the dataset not only reflects realistic and diverse interactions but also adheres to high standards of academic quality and integrity.

# <span id="page-21-0"></span>C User Feedback Analysis

We conducted a comprehensive user study involving participants with varying levels of expertise in knowledge graph systems, focusing on the domains of Natural Language Processing (NLP) and Computer Vision (CV). The feedback was collected from 50 user interactions with AGENTiGraph, compared against ChatGPT (GPT-4o), and provides valuable insights into the system's performance, user satisfaction, and areas for improvement.

# C.1 Methodology

Participants interacted with AGENTiGraph within the domains of NLP and CV, posing various questions and evaluating the system's responses. The feedback was collected and analyzed qualitatively, focusing on the conciseness, accuracy, and completeness of the responses. We also compared AGENTiGraph's performance with that of ChatGPT to benchmark its effectiveness.

# C.2 Representative Cases

Selected user feedback:

- NLP domain: Table [2,](#page-23-0)
- CV domian: Table [3.](#page-24-0)

# C.3 Analysis of User Feedback

Our user study revealed several key insights into the performance and user perception of AGENTiGraph compared to ChatGPT, particularly in the domains of Natural Language Processing (NLP) and Computer Vision (CV). The feedback highlights both strengths and areas for improvement in AGENTiGraph's responses.

# C.3.1 Natural Language Processing Domain

In the NLP domain, users consistently noted that AGENTiGraph provided more concise responses compared to ChatGPT. This brevity was generally appreciated, especially for users already familiar with core NLP concepts. The concise nature of responses helped avoid information overload, making AGENTiGraph particularly useful for quick reviews or refreshers on NLP topics.

## Strengths:

- Conciseness: AGENTiGraph excelled in providing succinct explanations for complex NLP concepts. For instance, in explaining the role of preprocessing steps or the differences between modern and traditional NLP models, AGENTiGraph delivered clear, to-the-point responses.
- Efficiency: Users appreciated the system's ability to quickly identify and articulate key points, making it efficient for reviewing or understanding core NLP concepts.

## Areas for Improvement:

- Completeness: In some cases, particularly for more complex or open-ended questions (e.g., "What are the most complicated fields in NLP?"), AGENTiGraph's responses were incomplete or missing entirely. This suggests a need for improving the system's ability to handle broader, more abstract queries.
- Depth of Explanation: While conciseness was appreciated, some users noted that for certain topics, AGENTiGraph's responses lacked the depth provided by ChatGPT. This was particularly evident in questions about future trends or comprehensive overviews of NLP applications.

# C.3.2 Computer Vision Domain

In the Computer Vision domain, user feedback was more mixed, with a higher proportion of responses requiring improvement or expansion.

## Strengths:

- Accuracy: For fundamental CV concepts, such as the role of GANs or the importance of data preprocessing, AGENTiGraph provided satisfactory explanations.
- Clarity: When AGENTiGraph did provide complete answers, users found them clear and easy to understand.

## Areas for Improvement:

- Completeness: Several responses were noted as incomplete, particularly for questions about challenges in object detection or differences between supervised and unsupervised methods.
- Technical Depth: Users often requested more detailed explanations of technical concepts, such as how convolutional filters work or the specifics of image augmentation techniques.
- Practical Examples: Feedback suggested that including practical examples or applications could enhance the explanations, especially for complex topics like feature extraction vs. feature selection.

## C.3.3 Overall Analysis

The user feedback reveals that AGENTiGraph has significant strengths in providing concise, efficient responses, particularly beneficial for users with some prior knowledge seeking quick information or review. This aligns well with the system's design goal of offering focused, knowledge graph-based interactions. However, the feedback also highlights areas where AGENTiGraph can improve:

- 1. Balancing Conciseness and Completeness: While brevity is appreciated, there's a need to ensure that responses, especially for complex topics, are comprehensive enough to provide valuable insights.
- 2. Handling Abstract Queries: Improving the system's ability to address broad, open-ended questions would enhance its versatility.
- 3. Domain-Specific Enhancements: Particularly in the Computer Vision domain, there's a need for more detailed technical explanations and practical examples.
- 4. Consistency: Ensuring consistent quality of responses across different types of questions and domains is crucial for user trust and satisfaction.

## C.4 Conclusion

The user feedback analysis provides valuable insights into the performance of AGENTiGraph across two important domains in AI: Natural Language Processing and Computer Vision. The system's strength in providing concise, efficient responses is evident, particularly in the NLP domain. This aligns well with its design goal of offering focused, knowledge graph-based interactions. However, the analysis also reveals areas for improvement, especially in handling more complex, open-ended queries and providing deeper technical explanations in specialized domains like Computer Vision. The feedback suggests that while AGENTiGraph's concise responses are appreciated, there's a need to balance this brevity with comprehensive coverage of topics, particularly for more advanced or abstract concepts.

Moving forward, these insights will be invaluable in guiding the development of AGENTiGraph. Future iterations should focus on enhancing the system's ability to provide more comprehensive responses when needed, improving its handling of abstract queries, and ensuring consistent performance across different domains. By addressing these areas, AGENTiGraph can further solidify its position as a powerful tool for knowledge graph interactions, catering to users with varying levels of expertise and information needs.

| Table 2: Representative User Feedback Cases in NLP Domain |  |  |  |
|-----------------------------------------------------------|--|--|--|
|-----------------------------------------------------------|--|--|--|

<span id="page-23-0"></span>

| Question                                                                                                                                                                                                                                                                                        | AGENTiGraph Response                                                                                                                                                                                                                                                                                                                                                                                                                                           | User Feedback                |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------|
| What is the role of prepro<br>cessing steps like stop-word re<br>moval, stemming, and lemmati<br>zation in improving the perfor<br>mance of NLP models?                                                                                                                                         | The role of preprocessing steps like stop-word removal,<br>stemming, and lemmatization is to clean and normalize<br>text data, reducing noise and dimensionality. This helps<br>NLP models focus on the most relevant information,<br>improving their performance and efficiency.                                                                                                                                                                              | Shorter compared to ChatGPT  |
| How do NLP models like BERT<br>and GPT differ from traditional<br>models such as Word2Vec?                                                                                                                                                                                                      | BERT and GPT use transformer architectures to under<br>stand context and generate text, while Word2Vec uses<br>shallow neural networks to create word embeddings<br>based on local context.                                                                                                                                                                                                                                                                    | Shorter compared to ChatGPT  |
| What are the most complicated<br>fields in NLP?                                                                                                                                                                                                                                                 | None                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Incomplete or missing answer |
| Can you explain what word em<br>beddings are and how they im<br>prove traditional text represen<br>tation methods?                                                                                                                                                                              | Word embeddings are dense vector representations of<br>words that capture their meanings, semantic relation<br>ships, and syntactic properties. They improve tradi<br>tional text representation methods, like bag-of-words<br>or tf-idf, by providing context-aware representations<br>that preserve the relationships between words, leading<br>to better performance in natural language processing<br>tasks.                                               | Shorter compared to ChatGPT  |
| How do transformers and atten<br>tion mechanisms improve the<br>accuracy of language models<br>compared to older models like<br>RNNs and LSTMs?                                                                                                                                                 | Transformers and attention mechanisms address the<br>limitations of RNNs and LSTMs, leading to improved<br>accuracy in language models.                                                                                                                                                                                                                                                                                                                        | Shorter compared to ChatGPT  |
| What is Natural Language Pro<br>cessing (NLP), and how is it<br>used in real-world applications?                                                                                                                                                                                                | None                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Incomplete or missing answer |
| How does tokenization work in<br>NLP, and why is it important for<br>text processing?                                                                                                                                                                                                           | Tokenization in NLP involves breaking down text into<br>smaller units called tokens, such as words or phrases.<br>This process is crucial for text processing because it<br>enables the analysis and understanding of the text by<br>converting it into manageable pieces. Tokenization is<br>directly connected to text processing as it is a foun<br>dational step that facilitates further tasks like parsing,<br>sentiment analysis, and machine learning. | Shorter compared to ChatGPT  |
| What are the differences be<br>tween rule-based NLP systems<br>and<br>machine<br>learning-based<br>NLP systems?                                                                                                                                                                                 | Rule-based NLP systems rely on predefined linguistic<br>rules and patterns, while machine learning-based NLP<br>systems use statistical models and algorithms to learn<br>from data.                                                                                                                                                                                                                                                                           | Shorter compared to ChatGPT  |
| How do computational con<br>straints and the efficiency of full<br>attention mechanisms in trans<br>formers affect the processing of<br>long sequences, and what alter<br>natives, such as local attention<br>or hierarchical attention, are be<br>ing explored to overcome this<br>limitation? | Computational constraints and the efficiency of full at<br>tention mechanisms in transformers limit the processing<br>of long sequences due to their quadratic time and mem<br>ory complexity. Alternatives like local attention, which<br>restricts attention to a fixed window, and hierarchical<br>attention, which processes sequences at multiple levels<br>of granularity, are being explored to mitigate these limi<br>tations.                         | Shorter compared to ChatGPT  |
| What is your opinion of the<br>NLP and its key points in the<br>coming years?                                                                                                                                                                                                                   | The relationship type in the given context is "opinion."<br>The question is asking for a personal viewpoint on the<br>future of natural language processing (NLP) and its key<br>points.                                                                                                                                                                                                                                                                       | Shorter compared to ChatGPT  |

<span id="page-24-0"></span>

| Question                                                                                                   | AGENTiGraph Response                                                                                                                                                                     | User Feedback                                                                                                                                                                                                                |
|------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| What is the role of convolutional layers<br>in image processing?                                           | (Not provided)                                                                                                                                                                           | Improvement suggestion: It<br>could mention that the filters<br>slide across the image to pro<br>duce feature maps and that<br>convolutional layers preserve<br>spatial relationships by learn<br>ing hierarchical features. |
| How do pooling layers help reduce the<br>computational complexity in CNNs?                                 | (Not provided)                                                                                                                                                                           | Improvement<br>suggestion:<br>Adding<br>that<br>pooling<br>helps<br>retain<br>the<br>most<br>relevant<br>information<br>while<br>discard<br>ing<br>redundant<br>data<br>could<br>strengthen the explanation.                 |
| What are the differences between su<br>pervised and unsupervised methods for<br>image classification?      | The chatbot identifies that the<br>question is about a compari<br>son between supervised and<br>unsupervised methods. How<br>ever, it doesn't provide an an<br>swer to the core question | Incomplete answer                                                                                                                                                                                                            |
| What are some of the challenges in ob<br>ject detection in computer vision?                                | (Not provided)                                                                                                                                                                           | Incomplete answer: Not di<br>rectly answer the question<br>about challenges in object de<br>tection                                                                                                                          |
| How<br>do<br>image<br>augmentation<br>tech<br>niques help in improving the robust<br>ness of models?       | (Not provided)                                                                                                                                                                           | Improvement suggestion: It<br>could mention that augmen<br>tation reduces overfitting                                                                                                                                        |
| How does feature extraction differ from<br>feature selection in image processing?                          | (Not provided)                                                                                                                                                                           | Satisfactory                                                                                                                                                                                                                 |
| What are the key differences between<br>classical computer vision methods and<br>deep learning approaches? | (Not provided)                                                                                                                                                                           | Satisfactory                                                                                                                                                                                                                 |
| What is the importance of data prepro<br>cessing in computer vision tasks?                                 | (Not provided)                                                                                                                                                                           | Satisfactory                                                                                                                                                                                                                 |
| What are the major challenges in face<br>recognition systems?                                              | (Not provided)                                                                                                                                                                           | Satisfactory                                                                                                                                                                                                                 |
| How do GANs work and what role do<br>they play in generating synthetic im<br>ages?                         | Explains the basic GAN pro<br>cess and the roles of the gen<br>erator and discriminator.                                                                                                 | Satisfactory                                                                                                                                                                                                                 |

Table 3: Representative User Feedback Cases in Computer Vision Domain

## <span id="page-25-0"></span>D Customized Knowledge Graph Extension

In this section, we include the experimental details about the demonstrations in both legal and medical domains.

### D.1 Data
*UK Legislation*The dataset published by [Chalkidis et al.](#page-6-14) [\(2021\)](#page-6-14) comprises legislative and regulatory texts sourced from <legislation.gov.uk>, the official UK government website for accessing legislation, all written in English. The UK government offers a searchable database of all UK laws and regulations, including current and historical statutes, statutory instruments, and amendments. The dataset includes detailed records about, e. g., the UK Public General Acts and UK Local Acts.
*MMedC (Japanese)*MMedC [\(Qiu et al.,](#page-7-18) [2024\)](#page-7-18) is a large-scale multilingual medical corpus developed to enrich LLMs with domain-specific medical knowledge. The dataset is based on multiple sources, and we use a subset derived from open-source medical websites in Japanese. The subset comprises research and product information about medical treatments and healthcare technology written in Japanese. For instance, it contains studies on chemotherapy regimens and information about medical devices.

|                          | UK Leg. | Jap. Med. |
|--------------------------|---------|-----------|
| # docs                   | 52,515  | 54,435    |
| avg. tokens/doc          | 1,582   | 973       |
| # extracted entities     | 88      | 86        |
| # entities w/o abstracts | 8       | 11        |
| # relations              | 10      | 13        |
| # triples w/o fusion     | 268     | 124       |
| # entities w/o fusion    | 328     | 143       |
| # triples w/ fusion      | 1,168   | 408       |
| # entities w/ fusion     | 318     | 124       |

<span id="page-25-1"></span>Tab. [4](#page-25-1) shows some general statistics about the two datasets.

Table 4: Dataset statistics on UK Legislation and Japanese Medicine domain.

### D.2 Knowledge Graph Construction

The semantic data retrieval component of AGENTiGraph relies on a KG. We build this KG from the textual documents with Graphusion [\(Yang et al.,](#page-8-2) [2024c\)](#page-8-2). Graphusion is an approach for Knowledge Graph Construction from text, which is based on three steps: i) seed entity extraction, ii) candidate triple extraction, and iii) KG fusion.

We provide an easy-to-use command line interface for Graphusion that enables the evaluation of different LLMs on different datasets. The input to Graphusion is a set of domain-specific documents D and a set of relations R with textual descriptions. The relationships should be defined based on the anticipated queries for the knowledge graph. The output of the pipeline is a set of (s, r, o) triples, where r ∈ R, forming the Knowledge Graph.

In the following, we explain how we modified and used Graphusion for our two example use-cases.

Relation Definition. For each use case, we provide a set of relations together with their associated relation definitions to the knowledge graph construction pipeline. These relations are chosen to capture connections between entities within the domain, aligning with the types of information that domain-expert users are likely to query. In order to obtain these relations, we queried a LLM (latest ChatGPT-4o model) with the following prompt:

Relation Definition Prompt

We want to build a Knowledge Graph from text. Therefore, we need to define the relations (relation types) of the Knowledge Graph beforehand. Provide me 10 suitable relations (label, definition, example) for the following dataset description and described application.

This is the description of the dataset: [dataset description]

This would be a desired application: [example application]

This is an example document: [example document]

We run this prompt five times per dataset, each with a random example document. Then, we selected 10-15 relations from all five runs manually. The resulting relations for our two use-cases are shown in Fig. [3.](#page-27-0)

Candidate Entity Extraction. We use BERTopic [\(Grootendorst,](#page-6-15) [2022\)](#page-6-15) for the seed entity extraction. As document features, we use semantic sentence embeddings. These sentence embeddings are generated using a Sentence-BERT model [\(Reimers and Gurevych,](#page-7-19) [2019\)](#page-7-19). Specifically, we use the original Sentence-BERT model pre-trained on English web datasets for the UK Legislation data and a model pre-trained on the Japanese SNLI dataset [\(Yoshikoshi et al.,](#page-8-4) [2020\)](#page-8-4) for the MMedC (Japanese) data.

Candidate Triple Extraction. The next pipeline steps are mostly language independent, as they rely on prompting LLMs, which can usually handle multiple languages. However, LLMs handle different languages differently well, depending e. g. on the training data [\(Brown et al.,](#page-6-16) [2020\)](#page-6-16). Therefore, the data and application language should be taken into account when selecting the LLM for the knowledge graph construction. For this demonstration, we use*Gemini 1.5 Pro*.

For our two use cases, we set the number of candidate entities to 50 and limited the LLM input to 2,000 tokens and the output to 400 tokens to keep the computational costs low. As a result, we anticipate that the generated knowledge graph will be a smaller subgraph compared to what could be created without these constraints. However, the created graphs serve as a sufficient basis for this demonstration.

### D.3 Applications

*KG retrieval of UK Legislation Data.*We demonstrate the capabilities of the constructed KG with the following multistep query:*"What legislation provides the definition for the 'duty of excise' related to biodiesel, and which Act cites this duty?"*We extracted the sub-graph relevant to this question that serves as the basis for the answer. The sub-graph is visualized in Fig. [4.](#page-28-0)

So, the answer would reveal that the*"Biodiesel and Bioblend Regulations 2002"*defines*"biodiesel duty"*which is related to*"duty of excise"*as defined by the*"Hydrocarbon Oil Duties Act 1979"*and the*"Oil Act"*cites this duty.
*KG retrieval of Japanese Healthcare Data.* We demonstrate the capabilities of the constructed KG with the following multistep query: "What treatments are used to address blood tumors and related hematologic conditions?"

We extracted the sub-graph relevant to this question that serves as the basis for the answer. The sub-graph is visualized in Fig. [5.](#page-28-1)

The answer reveals that chemotherapy, hematopoietic stem cell transplantation, and CAR-T cell therapy are treatments for blood tumors. Furthermore, CAR-T cell therapy is also used to treat non-Hodgkin's lymphoma and hematologic malignancies.

### <span id="page-27-0"></span>English UK Legislation Data

Defines: Connects a legal term (like 'account' or 'property') to its definition as provided in the document.

Has Provision: Links the document to specific provisions or sections that it contains.

Appoints: Used to connect an entity to the entity or position being appointed under the act. Transfers: Represents the transfer of rights, liabilities, or properties from one entity to another. Cites Act: Links the current document to other legal acts it references.

Has Entity: Describes ownership or inclusion of a subsidiary or entity within a larger group. Regulates: Establishes the relationship where the document regulates certain actions, such as business activities.

Obliges: Represents obligations placed on entities, individuals, or organizations by the act. Includes Clause: Connects sections to specific legal clauses or detailed subsections.

Excludes: Captures exceptions or exclusions where certain entities or assets are not subject to the provisions.

### Japanese Medical Data

効果を示す (Show effect): This relation indicates the effects that a drug exhibits.

作用機序 (Mechanism of action): This relation indicates the mechanism by which a drug acts. 抑制される (Be suppressed): This relation indicates how conditions like allergies or inflammation are inhibited.

原因となる (Cause): This relation indicates the factors that cause specific diseases or symptoms. 放出を抑える (Suppress release): This relation indicates how substances that cause allergic reactions are suppressed.

副作用を引き起こす (Cause side effect): This relation indicates the side effects that specific drugs cause.

配合される (Be formulated): This relation indicates how a drug is formulated with other components.

使用される (Be used): This relation indicates the diseases or symptoms a drug is used for.

治療する (Treat): This relation indicates the diseases or treatments that are treated with specific drugs or therapies.

引き起こす (Cause): This relation indicates the diseases or symptoms caused by specific factors. 治癒される (Be cured): This relation indicates how specific diseases are healed by treatments or drugs.

予防する (Prevent): This relation indicates how specific diseases or symptoms are prevented. 関連する症状 (Related symptoms): This relation indicates the symptoms related to a specific disease or condition.

Figure 3: Descriptions of pre-defined relations used to build the KGs.

<span id="page-28-0"></span>![](_page_28_Figure_0.jpeg)
<!-- Image Description: The image is a directed acyclic graph illustrating the relationships between several acts and regulations concerning biodiesel duty. "Biodiesel and Bioblend Regulations 2002" defines "biodiesel duty," which in turn defines "duty of excise." Separately, the "Oil Act" cites another act and defines the "Hydrocarbon Oil Duties Act 1979." The graph visually represents the legal framework surrounding biodiesel taxation. -->

Figure 4: This graph outlines the relationships between regulations and acts concerning biodiesel and excise duties.

<span id="page-28-1"></span>![](_page_28_Figure_2.jpeg)
<!-- Image Description: The image is a directed graph illustrating treatments for blood cancers. Nodes represent treatments (chemotherapy, hematopoietic stem cell transplantation, CAR-T cell therapy) and blood cancer types (blood tumor, non-Hodgkin's lymphoma, hematologic malignancies). Directed edges, labeled "To_treat," show the relationships between treatments and the cancers they address. The graph visually depicts the therapeutic options for various hematological malignancies. -->

Figure 5: This graph shows treatments for blood-related tumors and hematologic malignancies, including chemotherapy, hematopoietic stem cell transplantation, and CAR-T cell therapy (machine translated from Japanese to English).

![](_page_29_Figure_0.jpeg)
<!-- Image Description: The image displays a graph visualization generated by a Cypher query (`MATCH (n) RETURN n`) within a graph database interface. The query retrieves all nodes (n) in the database. The visualization shows numerous nodes, interconnected to form clusters and smaller groups, representing the relationships between data points within the database. The purpose is to illustrate the structure and connectivity of the data. The interface also provides options for viewing data in table, text and code formats. -->

Figure 6: Visualization of the created UK Legislation Knowledge Graph in Neo4j.

|                                                                                                                         |                                                           | $\mathrel{\mathcal{R}}$ | $\epsilon^{\pi}$<br>$\wedge$ | $\mathsf{X}% _{0}$             |
|-------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|-------------------------|------------------------------|--------------------------------|
|                                                                                                                         | uklegislation\$ MATCH (n) RETURN n                        |                         | ☆                            | 上                              |
| ္ဆာင္က<br>Graph                                                                                                         |                                                           |                         |                              | $\lt$                          |
| $\equiv$<br>Table                                                                                                       |                                                           |                         |                              |                                |
| $\bigwedge_{\text{Text}}$                                                                                               |                                                           |                         |                              |                                |
| $\fbox{ \begin{tabular}{ c c } \hline \textbf{$\lambda$} \\ \hline \textbf{$\lambda$} \\ \textbf{Code} \end{tabular} }$ |                                                           |                         |                              |                                |
|                                                                                                                         |                                                           |                         |                              |                                |
|                                                                                                                         |                                                           |                         |                              |                                |
|                                                                                                                         | è<br>$\bullet-\frac{1}{2}$<br>$\mathcal{L}^{\mathcal{A}}$ |                         |                              | $\mathord{\textcircled{\lhd}}$ |
|                                                                                                                         |                                                           |                         |                              | $\mathbin{\ominus}$            |
|                                                                                                                         |                                                           |                         |                              | $\mathbb{C}^n_2$               |

Figure 7: Visualization of the created Japanese Med. Knowledge Graph in Neo4j.
