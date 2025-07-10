```
---
cite_key: saad_2025
title: SENAI: Towards Software Engineering Native Generative Artificial Intelligence
authors: Mootez Saad
year: 2025
doi: 10.1145/nnnnnnn.nnnnnnn
date_processed: '2025-07-02'
phase2_processed: true
original_folder: arxiv_arxiv_2503.15282_SENAI_Towards_Software_Engineering_Native_Generative_Artificial_Intelligence
standardization_date: 2025-07-10
standardization_version: 1.0
tags:
- Machine Learning
- Semantic Web
keywords:
- 1 evaluation strategy
- 1 pre-training of llms of code
- 2 benchmarks and evaluation
- 2 enriching llms with se knowledge
- 2 the status quo
- 4 conclusions
- BigCode
- BigCodeBench
- CodeLlama
- CodeUltraFeedback
- DeepSeek
- FineWeb
- GitHub
- GraphCodebert
- HumanEval
- JavaBench
- artificial intelligence
- ast-probe
- boqi chenhttpsorcidorg0000-0002-1451-3603
- by learning
- ccs concepts
- chin-yew
- code-related
- code-to-text
- crowd-sourced
- data generation
- deepseek-ai
- deepseek-coder
- dual-generation
- dániel varróhttpsorcidorg0000-0002-8790-252x
---

<!-- cite_key: saadhttpsorcidorg---2017 -->

# SENAI: Towards Software Engineering Native Generative Artificial Intelligence

[Mootez Saad](https://orcid.org/0009-0008-8159-3632)

Dalhouise University Halifax, Canada mootez@dal.ca

## [Neil Ernst](https://orcid.org/0000-0001-5992-2366)

University of Victoria Victoria, Canada nernst@uvic.ca

## [José Antonio Hernández López](https://orcid.org/0000-0003-2439-2136)

University of Murcia Murcia, Spain joseantonio.hernandez6@um.es

### [Dániel Varró](https://orcid.org/0000-0002-8790-252X)

Linköping University Linköping, Sweden daniel.varro@liu.se

### [Boqi Chen](https://orcid.org/0000-0002-1451-3603)

McGill University Montréal, Canada boqi.chen@mail.mcgill.ca

### [Tushar Sharma](https://orcid.org/0000-0002-0538-052X)

Dalhouise University Halifax, Canada tushar@dal.ca

## Abstract

Large Language Models have significantly advanced the field of code generation, demonstrating the ability to produce functionally correct code snippets. However, advancements in generative ai for code overlook foundational Software Engineering (se) principles such as modularity, and single responsibility, and concepts such as cohesion and coupling which are critical for creating maintainable, scalable, and robust software systems. These concepts are missing in pipelines that start with pre-training and end with the evaluation using benchmarks.

This vision paper argues for the integration of se knowledge into llms to enhance their capability to understand, analyze, and generate code and other se artifacts following established se knowledge. The aim is to propose a new direction where llms can move beyond mere functional accuracy to perform generative tasks that require adherence to se principles and best practices. In addition, given the interactive nature of these conversational models, we propose using Bloom's Taxonomy as a framework to assess the extent to which they internalize se knowledge. The proposed evaluation framework offers a sound and more comprehensive evaluation technique compared to existing approaches such as linear probing. Software engineering native generative models will not only overcome the shortcomings present in current models but also pave the way for the next generation of generative models capable of handling real-world software engineering.

## TL;DR
Research on senai: towards software engineering native generative artificial intelligence providing insights for knowledge graph development and data integration.

## Key Insights
Contributes to the broader understanding of knowledge graph technologies and data management practices relevant to PKG system development.

## CCS Concepts

• Software and its engineering → Software notations and tools; • Computing methodologies → Machine learning algorithms;

## Keywords

Generative Artificial Intelligence for se, Code Intelligence

Conference'17, July 2017, Washington, DC, USA

© 2025 Copyright held by the owner/author(s). Publication rights licensed to ACM. ACM ISBN 978-1-4503-XXXX-X/18/06 <https://doi.org/10.1145/nnnnnnn.nnnnnnn>

ACM Reference Format:

Mootez Saad, José Antonio Hernández López, Boqi Chen, Neil Ernst, Dániel Varró, and Tushar Sharma. 2025. SENAI: Towards Software Engineering Native Generative Artificial Intelligence. In . ACM, New York, NY, USA, [5](#page-4-0) pages. <https://doi.org/10.1145/nnnnnnn.nnnnnnn>

## <span id="page-0-0"></span>1 Introduction

Large language models (llms) have significantly transformed software development by enabling on-demand code generation and assistance capabilities. These models have demonstrated remarkable capabilities in automating programming tasks, providing code completions, and generating functions or classes based on textual prompts [\[9,](#page-4-1) [15\]](#page-4-2). By learning from vast code repositories, llms have become valuable tools for developers, enhancing productivity and reducing the time required to write boilerplate or routine code.

However, while these models are used within a software engineering context, they are not entirely trained on abstract knowledge embodied in the field such as design principles. Indeed, most contemporary models are directly pre-trained on source code, sometimes including other sources such as Jupyter notebooks and GitHub pull requests [\[20\]](#page-4-3). Furthermore, functional correctness is the main criterion used to evaluate their output.

In se, programming is a crucial step in creating concrete, operational systems that address specific problems, use cases, or functionalities from requirements. The evaluation and fitness of written code, however, go beyond mere functional correctness [\[16\]](#page-4-4). This is because code is rarely written in isolation; it must conform to many constraints, standards, and best practices that ensure its suitability within a larger context.

These constraints stem from the necessity for code to integrate seamlessly with existing systems, be understandable and maintainable by other developers, and remain adaptable to future requirements. Software systems evolve as requirements change or emerge, bugs are fixed, and new features are added; hence, ensuring conformance to these constraints, standards, and best practices is a constant endeavor.

More broadly, se is a multifaceted domain, encompassing many development process steps (such as requirement elicitation, design, and testing), attempting to ensure various quality attributes (such as reliability, maintainability, and performance [\[16\]](#page-4-4)), while ensuring relevance of the software being developed by appropriate communication and collaboration mechanisms. Current llm development

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

is mostly confined to models that autocomplete functionally correct code. This creates a rift between se expectations and what these models deliver. This deficit in expectation was initially investigated by Pudari and Ernst [\[25\]](#page-4-5). They created a hierarchy of software abstractions inspired by Koopman's Autonomous Vehicle Safety Hierarchy of Needs [\[18\]](#page-4-6). Using such a hierarchy, they showed that Copilot [\[7\]](#page-4-7) could clear out low levels of abstractions, e.g., autocompleting syntactically correct code, but often struggled with deducing and suggesting the correct design patterns and architectural tactics for a given project. Similarly, Cao et al. [\[6\]](#page-4-8) demonstrated recent models such as WizardCoder [\[21\]](#page-4-9) and DeepSeek-coder 33B [\[1\]](#page-4-10) struggled in programming scenarios involving object-oriented programming concepts, notably inheritance and encapsulation. Given these evidences, it is reasonable to assume that they may produce poorly structured software designs, leading to inflexible, hard-tomain systems. This could result in increased technical debt and higher maintenance costs.

In this paper, we first start by providing a brief overview of the steps involved in pre-training and evaluating large language models of code. Then, we lay a vision for how these models can be further aligned with se practices. We propose the integration of higherlevel design and architectural insights into the training process, with the aim to equip language models with a deeper understanding of software systems and with better reasoning capabilities. In addition, we propose the incorporation of other evaluation strategies to validate these models that extend beyond software correctness and other techniques for model understanding.

## 2 The Status Quo

This section provides background knowledge by presenting current practices used to pre-train and evaluate llms for code generation.

### 1 Pre-training of LLMs (of Code)

2.1.1 Pre-training objectives: llms are typically trained on extensive text-based datasets such as The Pile [\[11\]](#page-4-11) and FineWeb [\[24\]](#page-4-12) that include source code and question-answer discussions involving code snippets. Language models of code are trained specifically using source code [\[8\]](#page-4-13). Pre-training objectives enable them to learn patterns, structures, and semantics of code to predict code-related properties and to generate code effectively. Common pre-training objectives include next-token prediction, used by models such as gpt [\[26\]](#page-4-14), where the model predicts the next word based on previous words, modeling language in a left-to-right manner.

Models such as CodeT5 [\[29\]](#page-4-15), specialized for source code, extend these objectives. It consolidates pre-training tasks tailored for code understanding and generation into a single framework. Specifically, it combines masking strategies by masking code spans and identifiers and trains the model to predict them, enhancing its understanding of code syntax and semantics. It also includes dual-generation tasks between code and natural language, training on code-to-text (e.g., generating documentation from code) and textto-code (e.g., generating code from natural language descriptions), to bridge the gap between code and human language.

Recently, models such as CodeLlama [\[28\]](#page-4-16) and StarCoder 2 [\[20\]](#page-4-3), are pre-trained using the fill-in-the-middle (fim) objective. In this objective, the model is trained to generate a missing code segment

between a given prefix and suffix. With this, the model becomes adept at understanding bidirectional context and generates code that integrates with surrounding code. This enhances its capability in tasks like code completion, refactoring, and debugging.

2.1.2 Data representation: Another important aspect during pretraining is the input representation fed to the language model. Cubert [\[17\]](#page-4-17), one of the earliest code language models, was trained directly on Python code snippets, treating the code as a plain sequence of tokens. Codebert [\[10\]](#page-4-18) improved upon this by introducing a bimodal representation where the input consists of a natural language sequence that describes the code snippet, followed by the code snippet. This approach aims to capture the semantic relationship between natural language and programming languages, particularly relevant for tasks such as code search and documentation generation.

However, treating code as a stream of tokens ignores its inherent syntactic and semantic structure, failing to model the relations and dependencies within it properly. To address this limitation, Graph-Codebert [\[12\]](#page-4-19) enriches the input representation by incorporating data flow graphs of the code alongside the token sequences. This enhanced input representation allows the model to comprehend the semantic nuances of the code more effectively, which enhances its performance on tasks that require advanced code understanding.

While the aforementioned models show good results in various code intelligence tasks, they still operate primarily at the function or file level. However, real-world scenarios involve complex dependencies with interactions between different parts of the codebase. By confining the pre-training phase to isolated code snippets, models may perform suboptimally when code generation necessitates repository-level knowledge. Recognizing this limitation, recent approaches, such as StarCoder 2 [\[20\]](#page-4-3) and DeepSeek-Coder [\[13\]](#page-4-20), have begun to include repository-level contextual information during the pre-training stage.

## 2 Benchmarks and Evaluation

In this section, we cover some of the metrics used to quantify performance of llms of code. Second, we list a non-comprehensive list of benchmarks used to evaluate these models systematically.

2.2.1 Performance metrics: The evaluation metrics used can be broadly categorized into two types: token-based metrics and executionbased metrics. Token-based metrics, such as bleu [\[23\]](#page-4-21), rouge [\[19\]](#page-4-22) and Codebleu [\[27\]](#page-4-23), evaluate the generated code by comparing it to reference code at the token or syntactic level. This provides a quantitative assessment of similarity in terms of syntax and structure. However, these metrics may not fully capture functional correctness or the ability of the code to execute successfully. Execution-based metrics, such as pass@k and execution accuracy, assess the functional correctness by executing the generated code and verifying the outputs against expected results, usually against test suites

2.2.2 Benchmarks: Several widely used benchmarks have been developed to evaluate language models of code, inter alia, HumanEval [\[7\]](#page-4-7), mbpp [\[2\]](#page-4-24), and recently, BigCodeBench [\[31\]](#page-4-25). HumanEval consists of 164 handcrafted Python programming problems, each providing a natural language description, a function signature, and hidden unit tests. Models are evaluated based on their ability to

generate code that fulfills the problem descriptions and passes all the hidden tests, using metrics like pass@k to measure functional correctness. mbpp contains 974 crowd-sourced programming tasks designed to reflect challenges encountered by beginner programmers. It assesses models on both syntactic correctness and functional performance across a diverse set of basic programming tasks. BigCodeBench developed as part of the BigCode project, is designed for HumanEval-like function-level code generation tasks but with more complex instructions and diverse function calls to simulate solving practical problems faced in real-world scenarios.

## 3 Vision: Software Engineering Grounded Language Models

So far, llms are conceived as "(natural) language" models, and hence natural language is the first-class citizen. Given the textual form, these models perform code-related tasks satisfactorily. Most of the llm development, during architecture conceptualization, pretraining, or evaluation, focuses on generating syntactically and functionally correct code. However, as discussed in Section [1,](#page-0-0) these quality attributes are necessary, but not sufficient. In the following subsections, we lay out a vision, illustrated in Figure [1,](#page-3-0) of how to make these models grounded in se. We discuss some of the works conducted towards this goal, their limitations, and potential new directions to address these limitations.

Native software models are grounded in se and can adhere to se principles and software systems. We need se native large language models because the existing AI models overlook the essential se knowledge encapsulated in the form of principles and best practices to make software maintainable, scalable, robust, and reliable.

## 1 Evaluation Strategy

The evaluation process needs to be adapted to gauge the extent to which the models, old and new, grasp se knowledge.

3.1.1 Benchmarks and metrics. se principles such as modularity, cohesion, coupling, and abstraction are crucial for creating maintainable, scalable, and efficient software systems [\[3\]](#page-4-26). Assessing language models' performance concerning such principles requires a shift in both our evaluation methods and the datasets we use for assessment. Current evaluation benchmarks and metrics primarily measure the correctness of generated code against a set of test cases or reference implementations. They do not assess whether the code adheres to good software design practices. As a result, models might receive high scores even if the generated code is poorly structured or violates fundamental engineering concepts.

These new benchmarks would present tasks that require the model to demonstrate good design practices. For instance, tasks could involve, refactoring exercises, where models are provided with low-quality code snippets (e.g., from a maintenance perspective), and tasked to refactor them to improve quality metrics such as lcom and cbo, while maintaining functional correctness. A step further would require the model to first identify the suboptimal parts of code in a software system, and then suggest refactoring strategies that cover different levels of granularity (i.e., from methods to packages).

3.1.2 Model understanding. Investigating the se knowledge these models internalize is an important step towards native se models. Currently, probing methods such as linear classifier probes [\[14,](#page-4-27) [22\]](#page-4-28) are employed to investigate the information language models have internalized during pre-training. These probes analyze the model's hidden representations to determine whether specific properties or concepts are encoded in a way that can be extracted via simple classifiers. While valuable, this approach has limitations in capturing the full extent of a model's understanding, especially regarding complex and abstract se concepts.

## <span id="page-2-0"></span>Table 1: Bloom's Taxonomy Levels and Corresponding Potential Assessment Questions

| Level | Assessment strategy |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Recall | This level relates to recall from learned material. We have<br>decided to ignore this level as it would not gauge useful<br>information. Prompting the model on whether it recollects<br>cohesion or coupling has limited practical implications. |
| Understand | To assess LLMs' capabilities concerning this level, the model<br>can be prompted with code snippets, or pairs of code snippets,<br>that exhibit different degrees (low and high) of cohesion. |
| Apply | In this stage, Code snippets with low cohesion and high<br>coupling can be provided to the models for refactoring to<br>improve these attributes. The software's behavior should<br>remain the same. The evaluation will be based on test suite<br>execution and relevant software metrics (e.g., lcom, cbo). |
| Analyze | At the analysis level, the model is given a tuple of code frag<br>ments with varying degrees (low to high) of cohesion (or<br>coupling) in random order. The model then ranks the snip<br>pets from lowest to highest cohesion (or coupling). Also, this<br>level can investigate the model's understanding concerning<br>different types of cohesion (e.g., functional, sequential, com<br>municational) and coupling (e.g., temporal, data). |
| Evaluate | At this taxonomy level, the model will be given a set or pairs<br>of classes, ranked by cohesion or a coupling measure, and<br>asked to evaluate whether such ranking is valid. |
| Synthesis | In this stage, the model will be presented with requirements<br>of a feature that must be implemented as a part of a software<br>system. Then, the generated implementation will be evalu<br>ated based on correctness and its ability to produce loosely<br>coupled and highly cohesive code. |

The emergence of instruction-based language models, which allow for more flexible and interactive engagement, presents an opportunity to complement existing probing techniques with mature frameworks from psychology. A possible framework would be Bloom's Taxonomy [\[4\]](#page-4-29) which categorizes cognitive skills into hierarchical levels. This framework has been previously used by Buckley and Exton [\[5\]](#page-4-30) to assess developers' comprehension of a software system. A comprehensive assessment strategy can be designed to probe the model's knowledge across various cognitive dimensions. This framework would allow us to move beyond the surface-level analysis provided by linear probes. This includes assessing higher-order cognitive skills such as applying principles in new situations, analyzing code for adherence to best practices, evaluating design decisions, and even creating original code that embodies se principles. In addition, a taxonomy-based assessment

<span id="page-3-0"></span>![](_page_3_Figure_1.jpeg)
<!-- Image Description: This flowchart depicts a software engineering pipeline. It shows data flowing from repositories (containing synthetic data) through three stages: 1) artifact processing (using architectural decision records, UML diagrams, and source code); 2) model pre-training/finetuning (involving relationship masking and next entity prediction); and 3) evaluation (assessing testability, extensibility, maintainability, and multidimensional understanding). Each stage is illustrated with icons and short descriptions. -->

### Figure 1: Overview of the vision of seNAI, incorporating software engineering knowledge into the training and evaluation process of large language models.

can highlight specific areas where the model excels or underperforms. For instance, a model might effectively recall definitions but struggle with applying principles in code refactoring tasks. Identifying such gaps is crucial for guiding further pre-training and improvement. In Table [1,](#page-2-0) we present an example of a survey that can be used to examine to what extent a model internalizes foundational concepts, notably, cohesion and coupling.

### 2 Enriching LLMs with se knowledge

To transform language models into truly se-grounded tools, it is important to extend their training beyond the generation of syntactically correct and functionally accurate code. While these attributes are foundational, they do not encompass the full spectrum of se practices that ensure code is maintainable, scalable, and aligned with sound design principles. To achieve this deeper integration, we propose several strategies on which we elaborate on blow.

3.2.1 SE Guided Training: Software development processes produce many artifacts. Including these artifacts in the training may significantly enhance the models' capabilities. For example, Unified Modeling Language (uml) diagrams provide abstract high-level representations of software systems, capturing essential aspects such as class hierarchies, object interactions, and system behaviors. Training models on both the code and its corresponding abstractions would enable them to understand the relationships between high-level design and concrete implementations. This multimodal learning strategy can potentially allow models to grasp architectural patterns and design principles that are not readily apparent from code alone. It can bridge the gap between conceptual understanding and practical application.

Another avenue to reinforce se knowledge in the models is modifying pre-training objectives to include the prediction of entity relationships within code. By training models to recognize and predict relationships such as composition and association among classes and objects, we enhance their understanding of design and architectural structures. Similar to how models such as CodeT5 predict identifiers and their types, and GraphCodebert predicts data flow edges, incorporating entity relation prediction tasks helps models internalize the structural and semantic aspects of code. This enhancement can lead to code generation that not only functions correctly but also adheres to sound architectural practices such as

promoting better cohesion and reducing coupling within the codebase. Reinforcement Learning (rl)-based techniques can further align code generation models. Incorporating rl guides the models to learn from feedback grounded in se knowledge. A work towards this direction by Weyssow et al. [\[30\]](#page-4-31) integrates RL into code generation models to better align them with respect to code preferences, such as code readability and style.

3.2.2 Beyond Code and Its Abstractions: Incorporating other types of software artifacts, such as Architectural Decision Records (adrs), can also equip language models with reasoning abilities regarding design choices. adrs document the rationale behind architectural decisions, capturing the context, alternatives considered, and implications of each choice. When adding adrs to the training data, models might learn to associate code implementations with the underlying design intentions. This insight enables models to generate code that aligns with specific architectural tactics and to provide explanations for their design decisions, mirroring the reasoning process of experienced software engineers.

3.2.3 Potential Challenges: We acknowledge that these approaches present challenges, particularly concerning data procurement. Artifacts like uml diagrams and adrs are not as widely available as raw code, which could limit the volume and diversity of training data. However, there are viable strategies to mitigate this issue. Existing works in architectural recovery provide methodologies for extracting architectural information from codebases, effectively generating the necessary abstractions. Additionally, synthetic data generation techniques, such as those employed in models like WizardCoder [\[21\]](#page-4-9), can augment the training dataset.

It is important to emphasize that we are not advocating for the abandonment of current data and pre-training methodologies. Instead, we propose enriching existing models with se-grounded data and training objectives where the signal of software engineering knowledge is more amplified. These additional signals that emphasize design principles and architectural considerations, can enhance the models' capabilities without compromising their existing strengths in code generation. This approach ensures that models retain their proficiency in generating syntactically correct and functional code, while also evolving to produce code that embodies best practices in software design.

<span id="page-4-0"></span>SENAI: Towards Software Engineering Native Generative Artificial Intelligence Conference'17, July 2017, Washington, DC, USA

## 4 Conclusions

Grounding llms in SE principles is essential for advancing code generation beyond mere functional correctness. In this work, we called for integrating high-level design insights into language models which would steer towards the generation of code that is maintainable, scalable, and aligned with best practices. This proposal bridges the gap between code autocompletion and the demands of SE, leading to AI systems that can more effectively assist developers. Ultimately, this integration holds the promise of enhancing software quality and reducing potential technical debt in real-world applications. In parallel, we have also illustrated potential improvements to the current benchmarks and evaluation practices of language models of code.

## References

- <span id="page-4-10"></span>[1] DeepSeek AI. 2023. DeepSeek Coder 33B Instruct. [https://huggingface.co/](https://huggingface.co/deepseek-ai/deepseek-coder-33b-instruct) [deepseek-ai/deepseek-coder-33b-instruct.](https://huggingface.co/deepseek-ai/deepseek-coder-33b-instruct) Accessed: 2025-Jan-16.
- <span id="page-4-24"></span>[2] Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le, et al. 2021. Program synthesis with large language models. arXiv preprint arXiv:2108.07732 (2021).
- <span id="page-4-26"></span>[3] Len Bass, Paul Clements, and Rick Kazman. 2012. Software Architecture in Practice, 3rd Edition. [https://insights.sei.cmu.edu/library/software-architecture-in](https://insights.sei.cmu.edu/library/software-architecture-in-practice-third-edition/)[practice-third-edition/](https://insights.sei.cmu.edu/library/software-architecture-in-practice-third-edition/) Accessed: 2025-Jan-16.
- <span id="page-4-29"></span>[4] Benjamin Samuel Bloom, Max D Engelhart, Edward J Furst, Walker H Hill, and David R Krathwohl. 1964. Taxonomy of educational objectives. Vol. 2. Longmans, Green New York.
- <span id="page-4-30"></span>[5] J. Buckley and C. Exton. 2003. Bloom's taxonomy: a framework for assessing programmers' knowledge of software systems. In 11th IEEE International Workshop on Program Comprehension, 2003. 165–174. [https://doi.org/10.1109/WPC.](https://doi.org/10.1109/WPC.2003.1199200) [2003.1199200](https://doi.org/10.1109/WPC.2003.1199200)
- <span id="page-4-8"></span>[6] Jialun Cao, Zhiyong Chen, Jiarong Wu, Shing-Chi Cheung, and Chang Xu. 2024. JavaBench: A Benchmark of Object-Oriented Code Generation for Evaluating Large Language Models. In Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering.
- <span id="page-4-7"></span>[7] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. 2021. Evaluating large language models trained on code. arXiv preprint arXiv:2107.03374 (2021).
- <span id="page-4-13"></span>[8] Jacob Devlin. 2018. Bert: Pre-training of deep bidirectional transformers for language understanding. arXiv preprint arXiv:1810.04805 (2018).
- <span id="page-4-1"></span>[9] Angela Fan, Beliz Gokkaya, Mark Harman, Mitya Lyubarskiy, Shubho Sengupta, Shin Yoo, and Jie M. Zhang. 2023. Large Language Models for Software Engineering: Survey and Open Problems . In 2023 IEEE/ACM International Conference on Software Engineering: Future of Software Engineering (ICSE-FoSE). <https://doi.org/10.1109/ICSE-FoSE59343.2023.00008>
- <span id="page-4-18"></span>[10] Zhangyin Feng, Daya Guo, Duyu Tang, Nan Duan, Xiaocheng Feng, Ming Gong, Linjun Shou, Bing Qin, Ting Liu, Daxin Jiang, et al. 2020. Codebert: A pre-trained model for programming and natural languages. arXiv preprint arXiv:2002.08155 (2020).
- <span id="page-4-11"></span>[11] Leo Gao, Stella Biderman, Sid Black, Laurence Golding, Travis Hoppe, Charles Foster, Jason Phang, Horace He, Anish Thite, Noa Nabeshima, et al. 2020. The pile: An 800gb dataset of diverse text for language modeling. arXiv preprint arXiv:2101.00027 (2020).
- <span id="page-4-19"></span>[12] Daya Guo, Shuo Ren, Shuai Lu, Zhangyin Feng, Duyu Tang, Shujie Liu, Long Zhou, Nan Duan, Alexey Svyatkovskiy, Shengyu Fu, et al. 2020. Graphcodebert: Pre-training code representations with data flow. arXiv preprint arXiv:2009.08366 (2020).
- <span id="page-4-20"></span>[13] Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang, Guanting Chen, Xiao Bi, Yu Wu, YK Li, et al. 2024. DeepSeek-Coder: When the

Large Language Model Meets Programming–The Rise of Code Intelligence. arXiv preprint arXiv:2401.14196 (2024).

- <span id="page-4-27"></span>[14] José Antonio Hernández López, Martin Weyssow, Jesús Sánchez Cuadrado, and Houari Sahraoui. 2023. AST-Probe: Recovering abstract syntax trees from hidden representations of pre-trained language models. In Proceedings of the 37th IEEE/ACM International Conference on Automated Software Engineering. <https://doi.org/10.1145/3551349.3556900>
- <span id="page-4-2"></span>[15] Xinyi Hou, Yanjie Zhao, Yue Liu, Zhou Yang, Kailong Wang, Li Li, Xiapu Luo, David Lo, John Grundy, and Haoyu Wang. 2024. Large Language Models for Software Engineering: A Systematic Literature Review. ACM Trans. Softw. Eng. Methodol. (2024). <https://doi.org/10.1145/3695988>
- <span id="page-4-4"></span>[16] ISO/IEC 25010:2011 2011. Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models. Standard ISO/IEC 25010:2011. International Organization for Standardization, Geneva, Switzerland.
- <span id="page-4-17"></span>[17] Aditya Kanade, Petros Maniatis, Gogul Balakrishnan, and Kensen Shi. 2020. Learning and evaluating contextual embedding of source code. In International conference on machine learning. PMLR, 5110–5121.
- <span id="page-4-6"></span>[18] Phil Koopman. 2022. Maturity Levels for Autonomous Vehicle Safety. [https://safeautonomy.blogspot.com/2022/04/maturity-levels-for-autonomous](https://safeautonomy.blogspot.com/2022/04/maturity-levels-for-autonomous-vehicle.html)[vehicle.html](https://safeautonomy.blogspot.com/2022/04/maturity-levels-for-autonomous-vehicle.html) Safe Autonomy Blog.
- <span id="page-4-22"></span>[19] Chin-Yew Lin. 2004. ROUGE: A Package for Automatic Evaluation of Summaries. In Text Summarization Branches Out. Association for Computational Linguistics, Barcelona, Spain.
- <span id="page-4-3"></span>[20] Anton Lozhkov, Raymond Li, Loubna Ben Allal, Federico Cassano, Joel Lamy-Poirier, Nouamane Tazi, Ao Tang, Dmytro Pykhtar, Jiawei Liu, Yuxiang Wei, et al. 2024. Starcoder 2 and the stack v2: The next generation. arXiv preprint arXiv:2402.19173 (2024).
- <span id="page-4-9"></span>[21] Ziyang Luo, Can Xu, Pu Zhao, Qingfeng Sun, Xiubo Geng, Wenxiang Hu, Chongyang Tao, Jing Ma, Qingwei Lin, and Daxin Jiang. 2023. Wizardcoder: Empowering code large language models with evol-instruct. arXiv preprint arXiv:2306.08568 (2023).
- <span id="page-4-28"></span>[22] Wei Ma, Shangqing Liu, Mengjie Zhao, Xiaofei Xie, Wenhang Wang, Qiang Hu, Jie Zhang, and Yang Liu. 2024. Unveiling Code Pre-Trained Models: Investigating Syntax and Semantics Capacities. ACM Trans. Softw. Eng. Methodol. (2024). <https://doi.org/10.1145/3664606>
- <span id="page-4-21"></span>[23] Kishore Papineni, Salim Roukos, Todd Ward, and Wei-Jing Zhu. 2002. BLEU: a method for automatic evaluation of machine translation. In Proceedings of the 40th Annual Meeting on Association for Computational Linguistics (Philadelphia, Pennsylvania) (ACL '02). <https://doi.org/10.3115/1073083.1073135>
- <span id="page-4-12"></span>[24] Guilherme Penedo, Hynek Kydlíček, Anton Lozhkov, Margaret Mitchell, Colin Raffel, Leandro Von Werra, Thomas Wolf, et al. 2024. The fineweb datasets: Decanting the web for the finest text data at scale. arXiv preprint arXiv:2406.17557 (2024).
- <span id="page-4-5"></span>[25] Rohith Pudari and Neil A Ernst. 2023. From copilot to pilot: Towards AI supported software development. arXiv preprint arXiv:2303.04142 (2023).
- <span id="page-4-14"></span>[26] Alec Radford. 2018. Improving language understanding by generative pretraining. (2018).
- <span id="page-4-23"></span>[27] Shuo Ren, Daya Guo, Shuai Lu, Long Zhou, Shujie Liu, Duyu Tang, Neel Sundaresan, Ming Zhou, Ambrosio Blanco, and Shuai Ma. 2020. Codebleu: a method for automatic evaluation of code synthesis. (2020).
- <span id="page-4-16"></span>[28] Baptiste Roziere, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi, Jingyu Liu, Romain Sauvestre, Tal Remez, et al. 2023. Code llama: Open foundation models for code. arXiv preprint arXiv:2308.12950 (2023).
- <span id="page-4-15"></span>[29] Yue Wang, Weishi Wang, Shafiq Joty, and Steven CH Hoi. 2021. Codet5: Identifieraware unified pre-trained encoder-decoder models for code understanding and generation. arXiv preprint arXiv:2109.00859 (2021).
- <span id="page-4-31"></span>[30] Martin Weyssow, Aton Kamanda, and Houari Sahraoui. 2024. CodeUltraFeedback: An LLM-as-a-Judge Dataset for Aligning Large Language Models to Coding Preferences. arXiv preprint arXiv:2403.09032 (2024).
- <span id="page-4-25"></span>[31] Terry Yue Zhuo, Minh Chien Vu, Jenny Chim, Han Hu, Wenhao Yu, Ratnadira Widyasari, Imam Nur Bani Yusuf, Haolan Zhan, Junda He, Indraneil Paul, et al. 2024. Bigcodebench: Benchmarking code generation with diverse function calls and complex instructions. arXiv preprint arXiv:2406.15877 (2024).

## Metadata Summary
### Research Context
- **Research Question**: 
- **Methodology**: 
- **Key Findings**: 
- **Primary Outcomes**: 

### Analysis
- **Limitations**: 
- **Research Gaps**: 
- **Future Work**: 
- **Conclusion**: 

### Implementation Notes