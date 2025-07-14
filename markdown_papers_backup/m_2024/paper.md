---
cite_key: "m_2024"
title: Privacy-preserving in Blockchain-based Federated Learning Systems
authors: Sameera K. M., Marco Arazzi, Serena Nicolazzo, Antonino Nocera, Rafidha Rehiman K. A., Vinod P., Mauro Conti
year: 2024
date_processed: '2025-07-02'
phase2_processed: true
original_folder: arxiv_2401.03552_Privacy-preserving_in_Blockchain-based_Federated_Learning_Systems
images_total: 11
images_kept: 11
images_removed: 0
tags:
- Biomedical
- Blockchain
- Federated Learning
- Healthcare
- IoT
- Knowledge Graph
- Machine Learning
- Privacy
keywords:
- blockchain
- blockchain-based
- blockchain-enabled
- federated learning
- internet of things
- machine learning
- privacy-preserving
- under-explored
---

# PRIVACY-PRESERVING IN BLOCKCHAIN-BASED FEDERATED LEARNING SYSTEMS

Sameera K. M. Department of Computer Applications, Cochin University of Science and Technology, India sameerakm@cusat.ac.in

Marco Arazzi

Department of Electrical, Computer and Biomedical Engineering, University of Pavia, Italy marco.arazzi01@universitadipavia.it

Serena Nicolazzo<sup>∗</sup> Department of Computer Science, University of Milan, Italy serena.nicolazzo@unimi.it <sup>∗</sup>Corresponding author

Antonino Nocera Department of Electrical, Computer and Biomedical Engineering, University of Pavia, Italy antonino.nocera@unipv.it

Rafidha Rehiman K. A. Department of Computer Applications, Cochin University of Science and Technology, India rafidharehimanka@cusat.ac.in

Vinod P. Department of Mathematics, University of Padua, Italy vinod.p@cusat.ac.in vinod.puthuvath@unipd.it

Mauro Conti Department of Mathematics, University of Padua, Italy mauro.conti@unipd.it

## ABSTRACT

Federated Learning (FL) has recently arisen as a revolutionary approach to collaborative training Machine Learning models. According to this novel framework, multiple participants train a global model collaboratively, coordinating with a central aggregator without sharing their local data. As FL gains popularity in diverse domains, security, and privacy concerns arise due to the distributed nature of this solution. Therefore, integrating this strategy with Blockchain technology has been consolidated as a preferred choice to ensure the privacy and security of participants.

This paper explores the research efforts carried out by the scientific community to define privacy solutions in scenarios adopting Blockchain-Enabled FL. It comprehensively summarizes the background related to FL and Blockchain, evaluates existing architectures for their integration, and the primary attacks and possible countermeasures to guarantee privacy in this setting. Finally, it reviews the main application scenarios where Blockchain-Enabled FL approaches have been proficiently applied. This survey can help academia and industry practitioners understand which theories and techniques exist to improve the performance of FL through Blockchain to preserve privacy and which are the main challenges and future directions in this novel and still under-explored context. We believe this work provides a novel contribution respect to the previous surveys and is a valuable tool to explore the current landscape, understand perspectives, and pave the way for advancements or improvements in this amalgamation of Blockchain and Federated Learning.

*K*eywords Federated Learning · Blockchain · Privacy · Blockchain-enabled FL · Internet of Things · Industry 5.0.

## 1 Introduction

Federated Learning (FL, hereafter) has undergone a significant surge in popularity in recent years. This novel strategy enables training Machine Learning models directly on user devices or at the edge without centralizing raw data. Because sensitive data stays on the user's device, the risk of exposing information to possible data breaches is lowered, and user privacy is preserved. Moreover, collaboration among workers provides access to a large amount of data, which enhances performance, making models more efficient and scalable. While FL offers several advantages, it also has limitations and challenges. The main FL characteristics that expose it to new threats are *(i)*system heterogeneity,*(ii)*the need for a trustworthy central authority for the coordination of the processing of locally trained models,*(iii)*vulnerability to data falsification and inference attack,*(iv)*the lack of incentive mechanism for the participating nodes,*(v)*communication security, and*(vi)*regulatory complaints[\[1,](#page-34-0) [2\]](#page-34-1).

Because current implementations of the FL system do not provide proper mechanisms to address these challenges, researchers have recently begun to study approaches that leverage Blockchain [\[3\]](#page-34-2). This new technology, derived from the decentralized cryptocurrency system, has attracted the interest of industry and academia for its countless potential. It relies on the possibility of performing authentic and traceable transactions without a trusted third party and ensuring secure data storage and tracking. Hence, integrating Blockchain and FL can empower this last paradigm, ensuring data privacy, trust, and model security in decentralized collaborative Learning environments.

This study comprehensively reviews Blockchain-enabled FL, focusing mainly on data privacy. Although several papers analyze different aspects of the Blockchain-enabled FL paradigm, a systematic review of existing works on privacy still needs to be included. Moreover, we provide a novel perspective examining the possible attacks menacing privacy in this scenario and all the current adopted countermeasures present in literature to guarantee privacy through a Blockchain-enabled FL system. Specifically, our main aim is to examine the existing literature on privacy attacks in Blockchain-enabled Federated Learning (BCFL) systems. Moreover, we organize related papers according to the type of solution they implemented for privacy preservation, such as differential privacy, homomorphic encryption, secure multiparty computation, reward-driven approaches, hybrid privacy approaches, and cross-chained Federated Learning. Lastly, we delve into the practical applications of BCFL in cutting-edge scenarios, including healthcare, Industry 5.0, and the Internet of Vehicles. This survey provides several contributions, namely:

- it introduces a conceptual introduction to both FL and Blockchain technologies. Moreover, it deep dives into the description of existing architectures for Blockchain-enabled FL, describing how Blockchain can tackle the current challenges for FL, especially those related to privacy.
- it identifies the primary attacks menacing data privacy in Blockchain-enabled FL systems and the recently investigated countermeasures involving privacy methods, such as homomorphic encryption, differential privacy, secure multiparty computation methods, reputation approaches, and solutions relying on cross-chain FL.
- It describes how several practical application scenarios in various industries can benefit from integrating Blockchain and FL.
- It discusses and examines Blockchain-enabled FL systems' future directions and open research problems.

This survey offers fresh perspectives on the new paradigm of Blockchain-enabled FL focused on privacy-preserving. We expect the conducted analysis to be helpful to practitioners and researchers in categorizing the high number of studies dealing with privacy-preserving Blockchain-enabled FL approaches and in highlighting potentially promising directions to motivate future research work.

The structure of this paper is outlined as follows. Section [2](#page-1-0) introduces related survey studies, while Section [3](#page-3-0) delves into the methodology employed for conducting this survey. In section [4,](#page-4-0) we overview both FL and Blockchain main concepts. In Section [5,](#page-12-0) we analyze the state-of-the-art regarding the integration of FL and Blockchain technology, describing the main architectures. Section [6](#page-15-0) addresses the primary privacy threats within Blockchain-enabled FL. Sections [7](#page-16-0) and [8](#page-27-0) focus on the possible solutions to preserve privacy in such a domain. Section [9](#page-28-0) is devoted to the analysis of several application scenarios that benefit from Blockchain-enabled FL (such as Healthcare, Industrial IoT (IIoT), and the Internet of Vehicles). In Section [10,](#page-32-0) we explore various unresolved challenges and provide insights for potential areas of future research. Ultimately, Section [11](#page-33-0) encapsulates our concluding remarks on the survey.

## <span id="page-1-0"></span>2 Comparison with other survey articles

Although several related surveys have been conducted to explore the integration of Blockchain and FL from different perspectives, most of them focus on different aspects, issues, or application domains related to this combination [\[1,](#page-34-0) [4,](#page-34-3) [5,](#page-35-0) [6,](#page-35-1) [7\]](#page-35-2).

For instance, Qu et al. [\[1\]](#page-34-0) consider three problems of Blockchain-enabled FL, namely decentralization, incentive mechanism, and membership selection. They focus on attack categorization and evaluate the performance of existing countermeasures. The paper presented in [\[4\]](#page-34-3) describes the structural designs of Blockchain-enabled FL, the deployed platforms, and possible industrial applications. Moreover, it analyses the aspects of Blockchain that allow an improvement of the FL system, such as the node incentive mechanisms.

| Survey paper | Literature<br>Timeline | Blockchain<br>FL<br>and<br>Background | Proposed<br>General<br>Architecture | Privacy<br>Attack in<br>BCFL | | Privacy Preserving Approaches in BCFL | | | | | Applications | |
|---------------------|------------------------|---------------------------------------|-------------------------------------|------------------------------|----|---------------------------------------|----|----|----|----|--------------|--|
| | | | | | C1 | C2 | C3 | C4 | C5 | C6 | C7 | |
| Ali et al.[5] | 2019-2020 | | | | | | | | | | | |
| Nguyen et al.[6] | 2019-2020 | | | | | | | | | | | |
| Huang et al.[9] | 2019-2020 | | | | | | | | | | | |
| Li et al.[4] | 2020-2021 | | | | | | | | | | | |
| Qu et al.[1] | 2019-2021 | | | | | | | | | | | |
| Issa et al.[7] | 2019-2021 | | | | | | | | | | | |
| Zhu et al.[2] | 2019-2021 | | | | | | | | | | | |
| Chhetri et al. [11] | 2019-2022 | | | | | | | | | | | |
| Qammar et al. [8] | 2019-2022 | | | | | | | | | | | |
| Our Work | 2018-2023 | | | | | | | | | | | |

<span id="page-2-0"></span>**Table 1:** Summary of related surveys and their significant contributions to Our Work, specifically focused on Privacy attacks and privacy preservation approaches in BCFL.

C<sup>1</sup> : BCFL architectures for security and privacy protection, C<sup>2</sup> :BCFL with differential privacy based approach, C<sup>3</sup> :BCFL with homomorphic encryption based approach, C<sup>4</sup> :BCFL with secure multiparty computation based approach, C<sup>5</sup> :BCFL with reward-driven based approach, C<sup>6</sup> :BCFL with hybrid privacy approach, C<sup>7</sup> :Using cross-chain based approach.

denotes that the corresponding aspect has not been discussed, indicates a partial discussion, and signifies a comprehensive exploration.

The authors of [\[8\]](#page-35-5) conduct a literature review on the integration of Blockchain in FL, analyzing 41 research studies published between the years 2016 to June 2022. They focus on several aspects of the BCFL system: security and privacy, record and reward, verification, and accountability.

In [\[5,](#page-35-0) [7\]](#page-35-2), the authors focus on Blockchain-based FL approaches for IoT applications. Specifically, [\[5\]](#page-35-0) presents the notion of Blockchain, its application to IoT, and the privacy issues and possible countermeasures. Then, they introduce the FL application in IoT systems, devise a taxonomy, and present privacy threats in FL. The combination of these two paradigms is only briefly presented through an IoT-based use case. The work proposed by Nguyen et al. [\[6\]](#page-35-1) instead focuses on the applications of BCFL in mobile-edge computing domains, analyzing some critical aspects of system design, including communication cost, resource allocation, incentive mechanism, as well as aspects related to security and the safeguarding of privacy.

Several works rely on custom taxonomies to categorize related literature on Blockchain-based FL [\[9,](#page-35-3) [10,](#page-35-6) [2\]](#page-34-1). In particular, in [\[9\]](#page-35-3), the authors propose a taxonomy to categorize Blockchain-based FL systems referring to three distinct layers: the Blockchain, the training, and the aggregation layers. They briefly review and summarize representative work according to this taxonomy.

Similarly, the study presented in [\[10\]](#page-35-6) analyses 41 research papers between 2018 and 2021 deal with Blockchain-based FL methodologies in smart environments, categorizing work in a custom taxonomy. In particular, FL methodologies are divided into public FL and private FL environments. In public Blockchain mechanisms, they investigate only vertical FL approaches, whereas, for private Blockchain mechanisms, they evaluate both horizontal FL and Federated Transfer Learning approaches.

Zhu et al. [\[2\]](#page-34-1) rely on a categorization of BCFL models in three classes: decoupled, coupled, and overlapped, according to how the FL and Blockchain functions are integrated. Then, they use these classes to compare the advantages and disadvantages of the e state-of-the-art solution they considered.

The authors of [\[11\]](#page-35-4) conduct a brief review of existing literature on Blockchain-based FL that addresses privacy challenges. They describe only 18 papers published mainly from 2019 to 2022 but do not consider all the possible approaches to guarantee privacy in BCFL.

Table [1](#page-2-0) summarizes the main topics addressed by related surveys and makes a comparison with our contribution. As visible from the table, none of the existing contributions cover the topics presented in the survey or consider papers in the temporal span we analyzed. Table [2](#page-5-0) outlines the distribution of articles, specifying the number of articles considered in each category related to existing surveys and our work, along with the corresponding publication years.

![](_page_3_Figure_1.jpeg)
<!-- Image Description: This flowchart details a systematic review's literature selection process. Starting with 471 records identified from four databases (IEEE Xplore, ACM Library, Springer Link, Science Direct), it shows the reduction in number of studies through duplicate removal, title/abstract/full-text screening, and application of inclusion/exclusion criteria, ultimately yielding 102 final papers. Each stage displays the number of studies remaining. -->

<span id="page-3-1"></span>**Figure 1:** The PRISMA flow diagram visually outlines the various phases of the systematic review process.

## <span id="page-3-0"></span>3 Methodology

## 1 Research Approach

Blockchain-enabled Federated Learning has surfaced as a groundbreaking paradigm in the rapidly evolving technology landscape, presenting the prospect of decentralized and collaborative machine Learning while safeguarding data privacy. This study intricately explores the critical aspect of privacy within this innovative framework, meticulously examining potential threats and presenting effective mitigating strategies. It systematically explores Blockchain fundamentals and Federated Learning along with its categorization. It delves into relevant literature on privacy attacks and protection methods in BCFL. Moreover, it highlights the essential need for privacy preservation in BCFL-focused applications across domains. The study aims to identify areas of concern, and the paper thoroughly examines the open issues and limitations faced by Blockchain-enabled Federated Learning. Finally, it discusses the future direction in these areas, primarily focusing on enhancing BCFL's privacy.

## 2 Search Strategy

To acquire pertinent information concerning Federated Learning based on Blockchain, we devised a search plan in line with our research objectives. We started by thoroughly exploring Google Scholar and Web of Science. Then, we expanded our investigation to reputable academic repositories such as IEEE Xplore, ACM Digital Library, ScienceDirect, and SpringerLink. Our search spanned publications from 2018 to 2023 to ensure a thorough review of recent research. Additionally, we formulated search terms using specific phrases and keywords to cover different aspects of Blockchainenabled Federated Learning.

We consolidated the search terms using the conjunction operator ( AND) to pinpoint relevant studies accurately. Key search terms included "Blockchain AND Federated Learning AND privacy"and "privacy-preserving in Blockchain-based Federated Learning ". In addition to these primary terms, we incorporated supplementary search terms such as "privacy

attack ", "inference attack", "homomorphic encryption", "differential privacy", "secure multiparty computation", "privacy-preserving in healthcare", and "internet of things"to enhance the comprehensiveness and scope of the search.

The PRISMA flow diagram in Figure [1](#page-3-1) visually illustrates the iterative screening process, depicting the counts of identified, excluded, and included research works.

### 3 Selection Criteria

This section outlines the criteria employed to assess the relevance and quality of scientific works selected for inclusion in this survey based on our search criteria. A paper is considered eligible for inclusion if it meets at least one of the following inclusion criteria and does not meet any exclusion criteria.

### 3.1 Inclusion Criteria

In assessing the relevance of a paper for inclusion in this survey, we consider the following criteria:

- the importance of the corresponding author or supervisor in the domain under analysis;
- the citation count (primarily relying on Google Scholar [\[12\]](#page-35-7) and Scopus [\[13\]](#page-35-8) platforms);
- the age of the paper, we privileged more recent works;
- the paper's publication venue significance is assessed using Scimago [\[14\]](#page-35-9) and Core.edu [\[15\]](#page-35-10) rankings for journals and conferences, respectively.

### 3.2 Exclusion Criteria

Following the inclusion process, we apply the exclusion process, excluding a paper if it meets any of the following criteria:

- the paper is not peer-reviewed;
- the paper is written in a language other than English;
- the date of publication exceeds six years w.r.t. our work (i.e., the paper publication year should be 2018 or later);
- the paper is not focused on solutions for Federated Learning-based Blockchain technology nor dealing with privacy;
- the paper lacks significance, as it represents an incremental improvement on a previously proposed approach, a duplicate publication, or an extended version of an already published key contribution.

## <span id="page-4-0"></span>4 Background Knowledge

This section provides the essential background information to contextualize our survey. In particular, we describe the main concepts related to FL, its workflow, and the principal categorizations and challenges of such an approach. Moreover, we illustrate the fundamental notions about Blockchain. Table [3](#page-5-1) summarizes the acronyms used in the paper.

## 1 Centralized Learning, Distributed Learning, vs. Federated Learning

This part explains how ML architectures have evolved, progressing from centralized models to distributed on-site solutions and, most recently, up to Federated Learning (FL) [\[16\]](#page-35-11).

The classical architecture, illustrated in Figure [2,](#page-6-0) is called Centralized Learning. In this strategy, generated data is continuously streamed into the Cloud, where high-performance servers can process them and train models efficiently. Examples of the use of such an approach are provided by popular ML-As-A-Service providers, such as Amazon Web Services[1](#page-4-1) , Google Cloud[2](#page-4-2) , and Microsoft Azure[3](#page-4-3) .

In Centralized Learning, data is sent to the Cloud, where the ML model is built. A user uses the model through an API by requesting access to one of the available services. Within this architecture, abundant interactions generate a

<span id="page-4-1"></span><sup>1</sup> https://aws.amazon.com/

<span id="page-4-2"></span><sup>2</sup> https://cloud.google.com/

<span id="page-4-3"></span><sup>3</sup> https://azure.microsoft.com/

| Survey paper | Privacy Attack in BCFL | Privacy Preserving Approaches in BCFL | | | | | | | |
|---------------------|------------------------|---------------------------------------|-------------|-------------|-------------|-------------|-------------|-------------|--------------|
| | | C1 | C2 | C3 | C4 | C5 | C6 | C7 | Applications |
| Ali et al.[5] | | | | | | | | | 3 |
| | | | | | | | | | (2018-2020) |
| Nguyen et al.[6] | | 6 | | | | 4 | | | 5 |
| | | (2020-2021) | | | | (2019-2020) | | | (2018-2021) |
| Huang et al.[9] | | 4 | | | | 4 | | | |
| | | (2021) | | | | (2020-2021) | | | |
| Li et al.[4] | | | | | | 1 | | | 8 |
| | | | | | | (2019-2021) | | | (2018-2021) |
| Qu et al.[1] | | 16 | | | | 7 | | | |
| | | (2019-2021) | | | | (2019-2021) | | | |
| Issa et al.[7] | | 8 | | | | | | | |
| | | (2019-2021) | | | | | | | |
| Zhu et al.[2] | | 5 | | | | | | | 2 |
| | | (2019-2020) | | | | | | | (2019-2021) |
| Chhetri et al. [11] | | | 5 | 5 | 7 | | | | |
| | | | (2020-2022) | (2019-2021) | (2019-2021) | | | | |
| Qammar et al. [8] | | 4 | | | | 1 | | | 2 |
| | | (2020-2022) | | | | (2022) | | | (2019-2022) |
| Our Work | 2 | 14 | 19 | 14 | 5 | 17 | 9 | 4 | 31 |
| | (2020-2023) | (2018-2023) | (2019-2023) | (2021-2023) | (2019-2023) | (2018-2023) | (2020-2022) | (2021-2023) | (2018-2023) |

<span id="page-5-0"></span>**Table 2:** Number of articles compared with existing surveys and Our Work, specifically focused on privacy attacks and privacy preservation in BCFL.

C<sup>1</sup> : BCFL architectures for security and privacy protection, C<sup>2</sup> :BCFL with differential privacy based approach, C<sup>3</sup> :BCFL with homomorphic encryption based approach, C<sup>4</sup> :BCFL with secure multiparty computation based approach, C<sup>5</sup> :BCFL with reward-driven based approach, C<sup>6</sup> :BCFL with hybrid privacy approach, C<sup>7</sup> :Using cross-chain based approach.

| Acronyms | Description |
|----------|-----------------------------------------|
| BCFL | Blockchain-enabled FL |
| DP | Differential Privacy |
| FL | Federated Learning |
| HE | Homomorphic Encryption |
| IID | Independent and Identically Distributed |
| IPFS | Interplanetary File System |
| ML | Machine Learning |
| SMPC | Secure Multiparty Computation |
| IoT | Internet of Things |

<span id="page-5-1"></span>**Table 3:** List of the acronyms used in the paper.

substantial volume of data. This can lead to privacy issues, latency, as data could be transmitted far away from the central server, and, consequently, high transfer costs.

Some ML tasks are moved to clients with powerful resources to overcome such drawbacks. This more recent strategy, visible in Figure [3,](#page-6-1) is called Distributed On-Site Machine Learning architecture. Here, each device owns a local dataset through which it can build its model. After the first interaction with the Cloud to distribute a pre-trained or generic model to the devices, no more communication with the Cloud is needed. Hence, privacy is obtained as data does not leave its hosts. Although popular applications benefit from this architecture, such as medical solutions [\[17\]](#page-35-12) and smart classrooms [\[18\]](#page-35-13), models are local, and, therefore, they cannot take advantage of the results of their peers.

In Federated Learning, shown in Figure [4,](#page-7-0) each device trains a local model leveraging local data and sends its parameters to the central curator for aggregation. Data is kept on-device, and knowledge is shared with peers through an aggregated model. In this way, FL combines all the advantages of the previous architectures. Indeed, it maintains data privacy while minimizing communication overhead by keeping raw data on devices and aggregating local model updates.

![](_page_6_Figure_1.jpeg)
<!-- Image Description: The image is a diagram illustrating a cloud-based machine learning system. A smartphone, smartwatch, and webcam send data to a cloud server. The cloud stores machine learning training data and machine learning models. A desktop computer requests ("get_service") and receives models from the cloud. The diagram showcases the data flow and interaction between IoT devices, cloud infrastructure, and a machine learning application. -->

<span id="page-6-0"></span>**Figure 2:** Centralized ML Architecture

![](_page_6_Figure_3.jpeg)
<!-- Image Description: The image is a diagram illustrating a federated learning architecture. Multiple devices (smartphone, smartwatch, webcam, computer) each possess local data and a local machine learning (ML) model. These models send updates to a cloud-based central machine learning model, which aggregates the updates to improve the overall model without sharing raw data. The diagram visually represents the distributed nature of the learning process and the data privacy advantages of federated learning. -->

<span id="page-6-1"></span>**Figure 3:** Distributed On-Site ML Architecture

### 2 Overview of Federated Learning

In the next sections, we deal with the key notions related to FL and its workflow. Finally, we discuss the primary categorizations and the main challenges inherent to such an approach.

### 2.1 Main Concepts and Workflow

As stated, FL is a Machine Learning strategy that allows a model to be trained across decentralized devices or servers holding local data samples while maintaining the localized data. This technique is beneficial if data cannot be efficiently centralized due to privacy regulations, network constraints, or large data volumes.

The participants in the protocol are mainly divided into two types: devices known as "clients" or "workers" devices (e.g., IoT devices or remote servers) and a central server called "aggregator". Workers are individual devices, such as smartphones, IoT devices, or remote servers, that announce to the server that they are ready to run local training and participate in an FL task. Every client possesses its local dataset and utilizes it to train a dedicated local model. On the contrary, the central server or aggregator acts as the coordinating entity overseeing the Federated Learning process. The basic FL workflow consists of the following steps [\[19\]](#page-35-14):

- Model initialization: A global ML model is initialized on a central server or node, commonly with random parameters. During this phase, workers (e.g., IoT devices or remote servers) are selected to participate in the FL process.
- Local model training and upload: Clients download the current global model to their local devices. Then, they perform local training using their data, which is kept private and not shared with the central server or other clients. The local training typically involves multiple iterations of gradient descent, back-propagation, or other optimization methods to improve the local model's performance. Following the local training, every client

![](_page_7_Figure_1.jpeg)
<!-- Image Description: The diagram illustrates a federated learning system. Multiple edge devices (smartphone, smartwatch, computer) process local data and send trained machine learning models to a central cloud server. The server aggregates these models, creating an improved global model. Arrows depict model transmission; text labels clarify data flow. The image visually explains the core process of federated learning—distributed model training and aggregation. -->

<span id="page-7-0"></span>**Figure 4:** Federated Learning Architecture

computes the model parameter updates and transmits them to the central server either in an aggregated form or encrypted.

• Global model aggregation and update: The central server collects and aggregates the model parameter updates from all the clients. The central server can employ various aggregation methods like averaging, weighted averaging, or secure multi-party computation to incorporate the received updates from each client. This process enhances the performance of the global model by integrating diverse insights from the individual client models.

Figure [5](#page-7-1) illustrates a schematic diagram of FL workflow with the three phases described above. Observe that the last two steps of*(i)*iterative process of local model training and upload and*(ii)*global model aggregation and update are iterated across multiple epochs, continuously enhancing and refining the global model.

![](_page_7_Figure_6.jpeg)
<!-- Image Description: This flowchart illustrates a federated learning system. Multiple workers (phone, watch, webcam, computer) train local models on their respective data. These models are then uploaded to a central server, which aggregates them into a global model. The updated global model is then distributed back to the workers, iterating the process. The initial step depicts model initialization. The diagram visually represents the distributed training process and model updates. -->

<span id="page-7-1"></span>**Figure 5:** A schematic diagram of the Federated Learning workflow

### 2.2 Categorization of FL

This section deals with the different architectures for Federated Learning based on the feature and sample spaces shared by the workers and the aggregating server.

Vertical FL, Horizontal FL, and Federated Transfer Learning. A different perspective to classify FL relates to how data is distributed among the participating parties in the feature and sample spaces [\[20,](#page-35-15) [19\]](#page-35-14). According to this criterion, Privacy-preserving in Blockchain-based Federated Learning Systems

![](_page_8_Figure_1.jpeg)
<!-- Image Description: The image displays three diagrams illustrating different federated learning approaches. (a) shows horizontal federated learning, with datasets A and B sharing the same feature space but different sample spaces. (b) depicts vertical federated learning where datasets A and B have different feature spaces but a shared sample space. (c) presents federated transfer learning where datasets A and B have overlapping feature and sample spaces. The diagrams use rectangular regions to represent data from sources A and B, axes labeled "sample space" and "feature space," and shaded regions to highlight the overlap in the federated transfer learning approach. -->

<span id="page-8-0"></span>**Figure 6:** The three categories of FL divided for feature and sample spaces

FL can be divided into Horizontal FL (HFL), Vertical FL (VFL), and Federated Transfer Learning (FTL). Figure [6](#page-8-0) shows a graphic representation of the three FL categories.

- Horizontal FL refers to scenarios where the parties share the same feature space but have different data samples. This schema can be also referred to HFL as sample-partitioned FL.
- Differently from HFL, Vertical FL applies to the case where the actors share overlapping data samples but differ in the feature space. We also refer to VFL as feature-partitioned FL.
- FTL is applicable for scenarios in which there is little overlapping in data samples and features. For instance, the case in which multiple subjects with heterogeneous distributions build models in a collaboratively way.

Types of data heterogeneity FL. In this part, we consider a possible FL classification according to the types of data heterogeneity. In FL, data can be Independent and Identically Distributed (IID) or Non-Independent and Non-Identically Distributed (Non-IID). These characteristics refer to how data is distributed among the different clients [\[21\]](#page-35-16). In the ideal scenario of an IID data distribution, the data on each client is assumed to be drawn from the same underlying probability distribution. In real-world scenarios, instead, data on different clients may have different statistical properties, feature distributions, label distributions, and data sizes. In FL, data heterogeneity refers to variations in data distributions among participants. During each federated iteration, participants are selected randomly to undertake the supervised task, incorporating features x and labels y. Subsequently, the local data distribution of the chosen client, denoted as Pi(x, y), is utilized to extract feature-label pairs from (x, y). In particular, the authors of [\[22\]](#page-35-17) consider the following categories:

-*Feature distribution skew*. It consists of an imbalance or non-uniformity in the distribution of features (input variables) across different devices, clients, or participants. Specifically, this happens when the distribution Pi(x) of the features varies from participant to participant, but the distribution of the probability Pi(y|x) is the same.
- *Label distribution skew*. It means that the distribution of labels Pi(y) is different for different participants, but given Pi(x|y) is the same. Label distribution may vary across participants even when they share the same label annotations. For example, consider two participants, denoted as i and j, containing data from the Fashion-MNIST dataset. In the participant i's dataset, 80% images, while the remaining 20% display other image types. Conversely, participant j's data illustrates that 85% of the images are shirts, and the remaining 15% depict the other types. Consequently, the distribution of labels ((Pi(y))) differs among participants. However, focusing explicitly on images featuring shirts (y = 6), the probability of the associated features x portraying a shirt remains roughly equal for both participants. Hence, the Pi(x|y) distributions are similar.
- *Quantity skew*. It is a common situation that causes data to deviate from a homogeneous distribution, and it refers to the significant difference in the quantity in different participant data Pi(x, y). For instance, participant i has 500 samples, and participant j has 30,0000 samples for training. Therefore, the distribution of Pi(x, y) differs significantly.

Cross-device and cross-silo FL. A further strategy to classify FL approaches is based on the participating clients and the training scale. According to this principle, FL can be divided into cross-device FL and cross-silo FL [\[23\]](#page-35-18).

The first group consists of clients that are small distributed entities (e.g., smartphones, wearables, and IoT devices) holding few local data. Hence, to obtain good performance, many clients usually need to participate in the training process. Unlike the previous group, cross-silo FL clients are typically big companies or organizations (e.g., hospitals, transportation companies, and banks). In these environments, the number of participants is small (typically 2 to 100 clients), but each client usually participates in the entire training process.

## 2.3 Primary Challenges to FL

Most of the scientific papers focusing on FL [\[24,](#page-35-19) [25,](#page-35-20) [26\]](#page-35-21) investigate several core open challenges that still need to be addressed, such as:

- *Privacy protection*. One of the primary aims of FL is to guarantee the privacy and protection of data in ML solutions. It is essential that FL model training does not reveal users' private information. Most recent approaches often provide privacy at the cost of reduced model performance or system efficiency.
- *Security*. FL systems must be robust against adversarial attacks or clients with malicious intent. FL has been analyzed through an adversarial lens to study the vulnerability of the learning process to model-poisoning adversaries [\[27\]](#page-35-22). Since FL, in its classical form, is susceptible to adversarial attacks, poisoning resilience defense mechanisms should be investigated.
- *Data shortage*. ML algorithms usually demand extensive data for optimal performance, but in a distributed context (such as IoT), involved devices have limited data. Hence, FL needs local data utilization for training on each device, after which the resulting local models are sent to the server and consolidated into a global model.
- *Statistical heterogeneity*. Clients may have different data distributions, and data held by these devices may be non-IID. This makes it difficult to create a globally useful model that performs well on all clients.
- *Expensive communication*. Transmitting model updates between clients and the central server can be resourceintensive, especially in scenarios with high latency or limited bandwidth. Reducing both the total amount of communication rounds and the size of transmitted messages at each round are two main aspects to be considered.
- *Systems heterogeneity*. The presence of heterogeneous devices in terms of storage, computational, and communication capabilities leads to several challenges related to dropped devices in the network, a low amount of participation in the FL framework, and the design of scalable and flexible solutions.
- *Algorithm convergence*. The work presented in [\[28\]](#page-36-0) describes a theoretical analysis of the convergence bounds of the gradient descent-based FL for convex loss functions. Anyhow, further studies on the optimum number of local workers and on the frequency of local updates and global aggregation to improve model performance and resource preservation should be deeply investigated [\[26\]](#page-35-21).
- *Lack of incentive mechanisms*. Limited research acknowledges that participants in Federated Learning lack incentives to share their data and train models. As a result, task requesters face challenges in identifying and choosing trustworthy participants with high-quality data [\[29,](#page-36-1) [30\]](#page-36-2).

## 3 Overview of Blockchain

![](_page_9_Figure_12.jpeg)
<!-- Image Description: The image illustrates a blockchain's structure. Three blocks are depicted: a genesis block, block *i*, and block *i+1*. Each block contains a hash of the previous block, a timestamp, a nonce, and a set of transactions (TX1...TXn). Arrows show the chain's sequential linking, where each block's hash becomes the previous block's reference in the next block. This diagram visually explains the chained structure fundamental to blockchain technology. -->

<span id="page-9-0"></span>**Figure 7:** Example of a Blockchain

This section is devoted to providing a background description of the Blockchain technology. In the next subsections, we will describe the main concept and workflow, the strategies to build the consensus mechanism, the smart contract technology, and the main Blockchain categories.

### 3.1 Concepts and Workflow

In 2008, Nakamoto introduced the revolutionary Bitcoin cryptocurrency [\[3\]](#page-34-2), which operates as a decentralized and transparent peer-to-peer system. Blockchain, the underlying technology supporting Bitcoin, finds extensive utility across many financial and industrial applications due to its remarkable characteristics. A Blockchain network's most prominent feature is its utilization of a publicly digitally distributed and immutable ledger of blocks, which is shared across all participants in the peer-to-peer network without relying on any centralized trusted third party [\[31\]](#page-36-3). Each participant in the Blockchain network retains an individual copy of the distributed ledger to ensure data integrity, and every block contains the previous block's hash and comprises multiple transactions, as illustrated in Figure [7.](#page-9-0)

In addition to the transactions and the hash value of the previous block, each block includes a timestamp and a nonce, which is a random number for verifying the hash. Since hash values are unique, changes on any block in the chain would immediately change the respective hash values. Indeed, once generated, the information within each block cannot be altered, ensuring the network's immutability. Whenever a new transaction is generated, it undergoes validation and verification through a consensus protocol carried out by *miners*. If the majority of nodes in the network agree by a consensus mechanism on the validity of transactions included in a new block and on the validity of the block itself, this block is created and seamlessly integrated into the distributed ledger. In summary, as shown in the scheme illustrated in Figure [8,](#page-10-0) once created by a client, a transaction goes through several steps [\[32\]](#page-36-4), namely:

- *Propagation*. The transaction is propagated in a block towards the validating peers.
- *Validation*. The transactions collected in blocks must address the different phases of the consensus mechanism. Thereafter, the block of transactions can be attached to the Blockchain.
- *Update Propagation*. The valid transactions block is propagated throughout the network to let all nodes update their own replica.
- *Confirmation*. The consensus procedure comes to an end, and the nodes have to agree on a single chain of blocks. Blocks of transactions are published on the Blockchain and are confirmed in the final version of the ledger, from which they may no longer be discarded.

![](_page_10_Figure_7.jpeg)
<!-- Image Description: The image illustrates a blockchain transaction process. Two rows depict the stages: transaction creation, propagation, validation (top), and confirmation, update propagation, and addition to the blockchain (bottom). Simple diagrams show a transaction originating on a computer, propagating to multiple nodes for validation, and finally being added as a block to the blockchain, represented by a cube. The gray and black cubes illustrate the process of block creation and addition. -->

<span id="page-10-0"></span>**Figure 8:** Transactions workflow in Blockchain

The key features of this strategy can be summarized as follows:

- *Security*. Blockchain employs advanced cryptographic procedures to keep data secure. Once a transaction is written in a block, altering or deleting it is impractical. This makes Blockchain robust against attacks, such as fraud or tampering.
- *Decentralization*. Blockchain distributes data across a network of nodes. These nodes work together to validate and record transactions. In this way, all the drawbacks of centralized solutions can be avoided, i.e., bottleneck servers or high latency due to excessive resource contention.
- *Transparency*. All transactions on a Blockchain are publicly available to all the participants in the network. This transparency can help build trust among users.
- *Immutability*. Due to cryptographic hashing and chaining of blocks, once a block is added to the Blockchain, it cannot be changed, and the user cannot revoke it.

## 3.2 Consensus mechanism

As already stated in the previous section, Blockchain uses consensus mechanisms, such as Proof of Work (PoW) or Proof of Stake (PoS), to agree on the validity of transactions and ensure that all nodes in the network have a consistent view of the shared ledger [\[32\]](#page-36-4).

PoW is the older and more widely adopted consensus mechanism, it has been adopted in Bitcoin and many other cryptocurrencies [\[33\]](#page-36-5). To validate a block in the PoW approach, miners should find a hash value of the block that meets a certain difficulty requirement as a mathematical puzzle. The winner of this competition can validate the block of transactions and is rewarded with cryptocurrency. PoW does not guarantee consensus finality; transactions can be considered as confirmed only when included in the longest chain. PoW is designed to consume a high amount of energy because of the miners' energy-intensive computations needed to solve puzzles.

On the contrary, PoS has recently gained popularity because it is a less energy-consuming alternative to PoW, and it is used in cryptocurrencies like Ethereum 2.0[4](#page-11-0) [\[34\]](#page-36-6). PoS is adopted by a category of Blockchain algorithm where the consensus is achieved by stakes (e.g. digital assets) in the network. Validator nodes, which are participants who hold and "stake" a certain amount of cryptocurrency, are chosen in a deterministic and pseudo-random manner to create new blocks and validate transactions based on the amount of cryptocurrency they hold and are willing to "stake" as collateral. Validators are incentivized by earning transaction fees.

## 3.3 Smart Contract

Smart contracts, serving as executable codes, embody a mutual agreement between two or more parties. They operate atop Blockchain to enforce and execute agreements among parties that might lack trustworthiness. These contracts define the rules, conditions, and actions to be taken when certain conditions are satisfied [\[35\]](#page-36-7). Moreover, it stores information, processes inputs, and writes outputs thanks to its pre-defined functions. Smart contracts are replicated on each node of the Blockchain network to prevent contract tampering. Platforms like NXT[5](#page-11-1) , Ethereum, and Hyperledger Fabric [\[36\]](#page-36-8) are Blockchain-based development frameworks able to provide smart contracts to execute automatically events and actions.

Once deployed on a Blockchain, a smart contract operates autonomously. Usually, it is initiated by activating its constructor function via a transaction submitted to the Blockchain network. Each contract will be assigned to a unique address of 20 bytes. This constructor function is, then, executed, and the resulting smart contract code is permanently stored on the Blockchain. Once deployed, the creator of the smart contract receives essential parameters (e.g., the contract address). Subsequently, users can trigger any accessible functions within the smart contract by initiating transactions [\[37\]](#page-36-9).

There are two main groups of smart contracts, namely, deterministic and non-deterministic. The smart contracts that belong to the first type do not require any information from an external party outside the Blockchain. Instead, a non-deterministic smart contract depends on information (called oracles or data feeds) from an external party.

## 3.4 Blockchain Categorization

Depending on the characteristics of the Blockchain, researchers and industries have defined several categories.

Private and Public Blockchain. Both public Blockchain and private Blockchain networks are decentralized and shared among their clients to register all peer-to-peer transactions without the presence of a third-party authority. However, private Blockchains are restricted to authorized participants, and a centralized entity controls access. This leads to a very high transaction processing rate with few authorized participants. Moreover, a shorter time is required to get the consensus for the network, and more transactions can be processed within a time unit. Public Blockchain, on the other hand, is an open and permissionless network accessible to anyone, posing a risk to information privacy. However, since each transaction is open for the public to verify, they are very transparent, and the risk of hacking and data manipulation is lower when compared to private Blockchains. For this reason, it can be stated that public Blockchains are generally more secure [\[38\]](#page-36-10). A further type of Blockchain is represented by Hybrid Blockchain that combines elements of both public and private ones. Some parts of the network are public, while others are private. Finally, Consortium Blockchains, like hybrid Blockchains, have private and public features, but they involve various organizational members working together on a decentralized network.

Permissioned and Permissionless Blockchain. Permissioned Blockchains usually involve a consortium of organizations where transactions are grouped, accessed, and verified by authorized gatekeepers instead of anonymous miners.

<span id="page-11-0"></span>4 https://ethereum.org/

<span id="page-11-1"></span><sup>5</sup> https://nxtdocs.jelurida.com/Nxt\_Whitepaper

Their implementation is arising within the finance sector [\[39\]](#page-36-11). On the contrary, permissionless Blockchains, typically associated with public Blockchains, are open for anyone to join and participate without demanding prior authorization. They represent the first and oldest Blockchain development, in which the hashing of blocks of transactions relies on the work of many anonymous miners competing to solve a complex mathematical algorithm for that block of transactions via trial and error [\[40\]](#page-36-12).

## <span id="page-12-0"></span>5 State-of-the-art: Integration of FL and Blockchain

Blockchain is a promising technology, providing robust and secure solutions for various applications, even when dealing with untrusted entities. In FL, it primarily safeguards user privacy. Consequently, the amalgamation of FL and Blockchain, known as Blockchain-enabled Federated Learning (BCFL), enhances privacy and security in various distributed applications. These applications span sectors such as healthcare, cyber-physical systems, secure vehicular networks, pharmaceuticals, Industrial Internet of Things, and telemedicine[\[41,](#page-36-13) [42,](#page-36-14) [43\]](#page-36-15). BCFL effectively tackles the challenges associated with the FL paradigm by providing a range of valuable features. These include robust authentication and traceability, enhanced privacy, reliable availability, scalability, resilience against byzantine faults, resilience against inference attacks, long-term persistence, and anonymity[\[1\]](#page-34-0).

## 1 Benefits and characteristics of Blockchain-enabled FL

In this section, we explore the advantages of incorporating Blockchain in the FL process. The primary limitation of current FL systems is their dependence on centralized processing, which introduces vulnerabilities such as single-point failure and susceptibility to attacks [\[44,](#page-36-16) [45,](#page-36-17) [46\]](#page-36-18). Additionally, the extensive participation of edge devices contributes to network strain, leading to concerns about bandwidth availability and scalability [\[42\]](#page-36-14). Also, Blockchain technology offers a solution by providing decentralization, replacing the central server in FL applications with smart contract execution, enhancing security, and reducing the risk of malicious activities [\[47,](#page-36-19) [48\]](#page-37-0). The decentralized nature of Blockchain, preventing any single entity from having control over the entire network, aligns seamlessly with the principles of FL. In FL, data remains on individual devices and only updated models are exchanged, thereby significantly enhancing security and privacy. Nguyen *et al.*[\[6\]](#page-35-1) explored combining FL and Blockchain to create a decentralized, secure, privacy-enhanced intelligent edge network.

Furthermore, smart contracts automate and enforce governance rules in FL, ensuring participants adhere to predefined agreements and offering automated and transparent incentives for participants, miners, or validators based on their contributions. These agreements authenticate node contributions, perform global model computations, and facilitate node incentives based on their performance, enhancing the collaborative learning process's efficiency, audibility, and reliability [\[49,](#page-37-1) [46\]](#page-36-18). Incentives provided through smart contracts enhance the security and functionality of the Blockchain infrastructure while maintaining transparency and accountability [\[50,](#page-37-2) [51\]](#page-37-3).

Transactions in BCFL enable participants to trace and verify the complete history of model updates, fostering a culture of accountability within the system [\[52\]](#page-37-4). Also, Blockchain's standardized protocols enhance interoperability in BCFL, allowing for seamless integration across various platforms and devices.

## 2 The general architecture of Blockchain-enabled FL

The general abstracted architecture for Blockchain-enabled Federated Learning (BCFL) is illustrated in Figure [9.](#page-13-0) This architectural framework comprises three distinct layers: the Federated node layer, integration middleware, and the Blockchain layer. In decentralized applications on a blockchain, the task publisher, as an entity or user, initiates and creates tasks, actively defining and structuring them within the blockchain. This role is pivotal in task creation and execution, starting by formally requesting a specific Federated Learning task and publishing the details into the blockchain. Subsequently, participants expressing interest in the FL tasks retrieve the models from the Blockchain and contribute their trained models back to the Blockchain. The Blockchain then operates as a central server, employing smart contracts that aggregate the models from participants. A designated miner executes this operation and creates the new global FL model to fulfill the specific FL task. In the subsequent sections, we will briefly introduce each component in detail.
**Task Publisher:**  The task publisher initiates the process by formally submitting a request for a specific Federated Learning task, meticulously outlining the parameters, requirements, and objectives. This encompasses the task publisher's identity, initialization details (such as the Machine Learning model type), targeted performance metrics for optimization, expected processing time, and other relevant information. Furthermore, it encompasses additional crucial parameters, such as the task's initiation time, the number of federation rounds, the total reward amount, and other relevant details. The task publisher submits details of the Federated Learning task into the Blockchain for securely

![](_page_13_Figure_1.jpeg)
<!-- Image Description: This figure depicts a system architecture for federated learning on a blockchain. The top layer shows a blockchain with miners and a task publisher interacting via consensus algorithms and a smart contract. The middle layer is an integration middleware. The bottom layer illustrates the federated learning process, where multiple participants (Participant 1, 2, ..., N) locally preprocess data, train models, and upload model parameters to a global model, which is then downloaded for further training iterations. The diagram uses boxes, arrows, and database icons to represent the various components and data flows. -->

<span id="page-13-0"></span>**Figure 9:** General architecture for the Blockchain-enabled Federated Learning.

and transparently storing information for participants interested in contributing to or downloading models related to the specified task. In [\[24\]](#page-35-19), the manufacturer is a task publisher to develop a smart home system. In [\[53\]](#page-37-5), the task publisher refers to enterprises, research institutes, or healthcare research units aiming to acquire a medical disease detection model.

**Federated Node Layer:**  For the collaborative training of an ML model, the Federated node layer encompasses a varied group of participants, including diverse devices such as smartphones, wearables, servers, and other computing entities. Participants in the FL task download the model from the Blockchain. Each participant has their private local dataset and performs data preprocessing and feature extraction on its local dataset. Preprocessing may involve cleaning the data, normalizing, handling missing values, and extracting relevant features contributing to the model's learning process. Following this, participants individually train their models using their local datasets. After the training process, participants in FL produce personalized model updates specific to their datasets. Subsequently, participants submit these local model updates for verification and aggregation in the subsequent phase into the Blockchain.

**Integration Middleware:**  The integration middleware bridges FL participants and the Blockchain. Lamken *et al.*[\[54\]](#page-37-6) employed the Representational state transfer application Programming Interface (REST-API) to engage with Blockchain (Hyperledger Fabric) to enable a systematic allocation of network resources for recording and incentivizing gradient uploads. Additionally, the gRPC API, a remote procedure call (RPC) protocol developed by Google, facilitates model transfer between FL participants and the Blockchain network (Ethereum) [\[8\]](#page-35-5).
*Blockchain Layer:*In the Blockchain layer, pivotal elements encompass smart contracts, miners, consensus protocols, and the underlying Blockchain networks. The smart contract, another key component in Blockchain networks, operates between parties to facilitate interactions within the decentralized system. The participants utilize smart contracts (Registration Contract) to register for FL model training, ensuring transparency and immutability of conditions. After a successful registration, the revised local model is transmitted to the miners. The miners, encompassing personal computers, cloud-based nodes, or standby servers, willingly adopt the mining software. Their primary responsibilities involve receiving local model updates (local weights or local gradients) transmitted by FL participants. Furthermore, miners verify and authenticate the trained local model using the consensus algorithm, which may involve Proof of

![](_page_14_Figure_1.jpeg)
<!-- Image Description: The image is a flowchart depicting the process of federated learning on a blockchain. It shows a task publisher initiating a training task, participants registering and responding, local model training, smart contract execution for model aggregation, miners downloading and updating global models, and consensus algorithm execution to add a new global model to the blockchain. The flow is represented by numbered steps and colored arrows illustrating data flow between the task publisher, participants, miners, and the blockchain. -->

<span id="page-14-0"></span>**Figure 10:** The high-level workflow for a single epoch Blockchain-enabled Federated Learning

Work (PoW), Practical Byzantine Fault Tolerance (PBFT), Proof of Stake (PoS), and more. Once verified, the connected miners receive updated local models from FL participants, aggregate these models, add the new updated model into the block, and subsequently upload the block onto the Blockchain network.

## 3 High-level Workflow of Blockchain-enabled Federated Learning

The high-level workflow for a single epoch in Blockchain-enabled Federated Learning is depicted in Figure [10.](#page-14-0) The system iterates these procedures until the model converges or attains the designated federation round.

- 1. The task publisher initiates a service request by publishing a training task defining the parameters and details of the Federated Learning task. Following this, the task publisher deploys a smart contract to represent and regulate the Federated Learning task. This smart contract encapsulates the requisite rules, conditions, and parameters that govern the execution of the task.
- 2. Then, the task publisher publishes a training task on the Blockchain.
- 3. Participants willing to contribute to the Federated Learning task enroll through the smart contract. This registration process guarantees participants' adherence to the terms and conditions outlined in the smart contract.
- 4. The smart contract processes the registration request, validating participant information against predefined rules. If successful, it generates a response message to acknowledge the registration, given that it fulfills the required criteria.
- 5. The FL Participants download the global model from the Blockchain.
- 6. The FL Participants train the model utilizing their individually preprocessed local datasets.
- 7. During smart contract execution, the contract facilitates interactions among the Blockchain network, FL participants, and miners. FL participants transfer their local model updates to the miners, and the smart contract verifies the registration and validity of participants.

- 8. Subsequently, participants upload their local model updates to the miners on the Blockchain. Once sufficient participants are reached, the miners, in turn, validate and authenticate these local model updates.
- 9. The miners receive updates to the local models from registered Federated Learning participants and subsequently verify the received local models.
- 10. Each miner actively engages in the consensus algorithm by competitively solving complex puzzles to earn the role of a temporary leader. These temporary leaders then execute a smart contract for local model aggregation, collectively generating a new block that encapsulates information about the updated global model. Subsequently, the newly created block is disseminated to all miners within the network.
- 11. Finally, a fresh block is appended to the Blockchain network, encapsulating details of the updated global model.
- 12. FL participants request and download the latest global model for further training.

The Blockchain functions as a secure and decentralized ledger, originating from the Bitcoin network, that permanently records transactions through a chain of blocks containing relevant information. There are two primary classifications for Blockchain storage: on-chain storage, which consolidates all records within a single ledger, and off-chain storage, where the trusted third party stores the data externally, notably through the InterPlanetary File System (IPFS), employs a decentralized and private storage system. IPFS, a peer-to-peer distributed file system, prioritizes content-based addresses, storing hashes on the Blockchain for efficient retrieval. It offers permanent data storage, version traceability, speed enhancements, reduced bandwidth waste, and serves as a decentralized cloud storage solution, mitigating the risks associated with centralized servers. Several researchers have successfully incorporated IPFS to store actual models (Local and Global models), ensuring immutability by sending the corresponding hash values to the Blockchain [\[24,](#page-35-19) [55,](#page-37-7) [56\]](#page-37-8).

## <span id="page-15-0"></span>6 Attacks to privacy in Blockchain-enabled FL

Existing works have shown that approaches based on FL are vulnerable to attacks against data privacy. In particular, malicious actors can be identified both in:

- the server that aims to infer sensitive information from local updates of the participants over time.
- the workers that can infer other participants' sensitive information.

As a matter of fact, recent works have demonstrated that only by gradient observation a malicious attacker can successfully steal the training data, causing a deep leakage and revealing sensitive information both to a third party or the central server [\[57,](#page-37-9) [58\]](#page-37-10).

The known attacks against data privacy that may lead to information leakage and data breaches are*(i)*background knowledge attack,*(ii)*collusion attack, and*(iii)*inference attacks [\[1\]](#page-34-0).

Background knowledge attack is a privacy-oriented attack in which an adversary leverages external information or prior knowledge to gain insights into the data used in the FL process [\[59\]](#page-37-11). In particular, a worker regularly obtaining updates to the global model from a central authority might initiate background knowledge attacks by exploiting the differences. This results in a certain degree of privacy compromise.

Collusion attack is a particular class of background knowledge attack, where malicious participants (that may be both devices or servers) collaborate to compromise the privacy of the model, leveraging background knowledge for aggregation [\[58\]](#page-37-10). If the main aim is to reveal sensitive information to reconstruct individual data samples or learn specific patterns present in the data, this attack realizes a model inversion. Instead, if participants aim to determine whether a specific data sample is part of the training set, this attack is a membership inference attack.

Inference attack aims at extracting sensitive information about the data used in the training process by examining its outputs [\[60\]](#page-37-12). It can be divided into reconstruction attacks and tracing attacks. In the former group, adversaries try to deduce sensitive information, specific attributes, or characteristics of the training data. For instance, in [\[61\]](#page-37-13), a gradient inversion attack is presented. Instead, in tracing attacks, the attacker wants to determine the existence of an individual in a specific dataset. To this last group belongs the attack proposed by Shen et al., [\[62\]](#page-37-14) that exploits unintended property leakage to enable a server to infer a set of participants with target properties. Unlike collusion attacks, where participants work together to compromise the system, inference attacks typically focus on using only information that can be deduced from the FL model's predictions or other outputs.

In the following sections, we describe recent works providing effective defenses to these attacks in scenarios involving Blockchain technology and adopting several privacy-preserving techniques while maintaining the collaborative nature of the FL paradigm.

## <span id="page-16-0"></span>7 Solutions for privacy preservation in Blockchain-enabled FL

Ensuring the security and privacy of user data within the framework of Blockchain-enabled Federated Learning is a vital objective, as it necessitates a delicate equilibrium between collaborative machine learning and data protection. This section delves into various strategies and techniques to tackle the issues of safeguarding privacy in the FL empowered by Blockchain. However, these studies have collectively addressed the imperative challenge of safeguarding privacy through diverse means. Some suggested solutions involve employing homomorphic encryption, differential privacy, secure multiparty computations, incorporating reputation-aware BCFL, and, in some instances, combining these methods to fortify privacy measures. These approaches are designed to uphold the global model's accuracy, safeguard participants' privacy, and minimize the influence of malicious local updates.

## 1 Blockchain-enabled FL Architectures for Security and Privacy Protection

Numerous studies have introduced various approaches to incorporating Blockchain technology into Federated Learning, primarily focusing on enhancing privacy and security protection. This section explores strategies and techniques to address the challenges of ensuring privacy and security in FL empowered by Blockchain. These architectures guarantee user data protection while enabling collaborative machine learning within the Blockchain ecosystem.

Furthermore, the integration offers the benefit of reducing the risk of a single point of failure attributed to the centralized aggregation curator. For example, in [\[63\]](#page-37-15), the authors introduced a BCFL system to bolster privacy and security and mitigate the risk of a single point of failure within fog computing. The study examines an attack model where adversaries attempt to manipulate training output by replacing the global model before update transmission. Achieves these goals by modifying fog servers to store global updates on the Blockchain, allowing end devices to maintain global learning models through distributed consensus, and saving only pointers on the Blockchain. In contrast, data is stored in an off-chain distributed hash table. Singh*et al.*[\[64\]](#page-37-16) presented an alternative framework for safeguarding the privacy of IoT healthcare data through BCFL, aiming to minimize resource requirements while maintaining model accuracy and enabling fair compensation. The study also discusses the potential enhancement of this approach by not solely relying on the protocol but by incorporating a trust model and a novel consensus method within the Blockchain to support nodes. Xu et al. [\[65\]](#page-37-17) presented a privacy-focused personalized reliability prediction model for IoT using Federated Learning Neural Collaborative Filtering (FNCF), offering user privacy protection and personalized predictions, along with context awareness and improved convergence speed via local model training.

The authors in [\[43\]](#page-36-15) ensure privacy and network security within vehicular networks by enabling local model training on end devices, eliminating the need to share data with the edge server. They used practical Byzantine Fault Tolerance (pBFT) for reliable model training. The proposed framework has demonstrated remarkable performance, minimal energy consumption, low latency, high throughput, long lifetime rate, and high accuracy, approximately 97%. Lu*et al.*[\[66\]](#page-37-18) introduced a system to reduce communication latency and enhance reliability in BCFL within edge computing. This system integrates Blockchain technology using a consensus mechanism called Delegated Proof of Stake (DPoS) to create a decentralized training network. The system assesses latency by considering local training costs, model aggregation, parameter transmission, and block verification. It employs a deep reinforcement learning algorithm with multi-agent to optimize latency while meeting learning accuracy and bandwidth constraints. The study in [\[67\]](#page-38-0) presents a comprehensive framework for enhancing CT image recognition, focusing on COVID-19 detection while preserving privacy. It includes data normalization for diverse hospital data, uses Capsule Network-based segmentation and classification for precise patient identification, employs collaborative model training with BCFL, and achieves 98.68% accuracy. The authors in [\[68\]](#page-38-1) present a lightweight encryption strategy based on Blockchain combined with Federated Learning. This integration aims to bolster the security and privacy of electronic health records (EHR) kept within a decentralized cloud system. The approach ensures protected access for authorized users, minimizing potential attacks on EHR data. They utilize active smart contracts to facilitate secure data transfer and validate the system's efficacy on an Ethereum-based testbed, showcasing its effectiveness. Moreover, they utilize Google Firebase to store the models.

Presently, solutions focus on favoring the selection of portable, honest local models rather than promptly and efficiently detecting Byzantine models and identifying attackers. This is mainly due to verification delays, exposing significant security risks, especially concerning untrustworthy edge and potential Byzantine attacks. To solve these issues, the authors in [\[69\]](#page-38-2) proposed that BytoChain enhances model verification efficiency by employing verifiers to perform parallel verification workflows and employs a consensus mechanism called Proof-of-Accuracy (PoA) to detect byzantine attacks. It offloads the verification burden from miners by using verifiers for parallel verification workflows and introduces PoA to detect inferior models while preserving accuracy. The framework proposed in [\[70\]](#page-38-3) addresses both byzantine-robustness and inference-resistance. Utilizes permissioned Blockchain to replace the central curator, ensuring decentralized trust and fairness while protecting participant privacy. It employs private data collections in Fabric, supports multiple learning and prediction channels, and includes vertically partitioned secure aggregation to evaluate local model updates. This process calculates updated coordinate weights through Euclidean and cosine measures and determines new global model parameters via weighted averaging. Additionally, a secure prediction mechanism enables third-party applications to query the global model by securely processing raw data across peers before aggregating results for predictions.

Furthermore, Blockchain-based asynchronous FL aims to enhance reliability and security by introducing decentralized and transparent training processes [\[5\]](#page-35-0). However, traditional Blockchain consensus algorithms are either computationally intensive or communication-intensive, hindering efficiency, and committee-based algorithms like DPoS [\[71\]](#page-38-4) may not be ideal for smart public transportation. The work of [\[72\]](#page-38-5) presents a novel asynchronous BCFL system tailored for intelligent public transportation, integrating a dynamic scaling factor and a unique committee-based consensus algorithm to enhance reliability while minimizing communication overhead. Specifically, the committee leader, acting as the aggregation server, identifies low-accuracy local models from its local dataset to guard against poisoning attacks. Without requiring communication and voting, a new committee leader is periodically elected from roadside units based on the latest block's hash to reduce the vulnerability to DDoS attacks. Additionally, during the aggregation process, a dynamic scaling factor is employed to allocate suitable weights to local models based on their accuracy, subsequently improving the Learning performance of FL. Feng*et al.*[\[73\]](#page-38-6) introduced BAFL as a novel asynchronous strategy designed to expedite Federated Learning. BAFL incorporates two policies to enhance its workflow: one regulates the block generation rate to minimize Federated Learning delays, and the other dynamically adapts training duration to avoid transaction overloads. In contrast to the conventional FedAvg, BAFL employs an entropy weight method to evaluate device participation and records it in the Blockchain for trust. It also employs Pareto optimization to reduce model energy consumption and local device delays, striking a balance between model update speed and transaction delays. Sarhan*et al.*[\[74\]](#page-38-7) presents a hierarchical BCFL framework for secure and privacy-preserving collaborative IoT intrusion detection. With a smart contract, transactions (model updates) and processes are executed on a secure Blockchain, enhancing system security and reliability through task compliance verification.

The BCFL architecture removes the necessity for a trusted server in edge environments by utilizing Blockchain to enhance trust among participants and enable all users to verify the training process and maintain transparency. The authors in [\[75\]](#page-38-8) proposed an innovative approach to facilitate collaborative learning in trustless edge computing environments. This strategy introduces a novel paradigm that includes a sandbox and a state channel for creating a secure FL environment, effectively tackling concerns regarding data privacy and quality. In addition, this approach employs smart contracts to incentivize local device and edge node participation to enhance node selection performance further. At the same time, they are utilizing a Deep Reinforcement Learning (DRL) node selection mechanism to enhance accuracy and efficiency. In [\[76\]](#page-38-9), they proposed a decentralized BCFL architecture that enhances security and privacy by utilizing secure global aggregation and also employed a byzantine fault tolerance consensus protocol, which effectively safeguards against attacks from malicious servers and devices. However, the authors formulate a network optimization problem to mitigate potential long training latency that jointly considers bandwidth and power allocation. They propose transforming this problem into a Markov decision process and employing a DRL-based algorithm for adaptive and efficient resource allocation. It employs a twin delayed deep deterministic policy gradient algorithm that handles continuous optimization variables for long-term resource allocation.

### 2 Privacy preservation using BCFL with Differential Privacy Approach

Differential privacy incorporates randomly generated noises into data to enhance privacy and prevent precise inference of sensitive information. In this approach, noise is introduced into the client's local parameters, ensuring the perturbation or encoding of responses independently before submission to the central curator and effectively thwarting adversaries from inferring sensitive data. However, this approach minimizes communication and computational overhead compared to cryptographic approaches. A random function K provides (ϵ, δ)- differentially private for δ ≥ 0 if, for any pair of datasets D and D′ differing in at most one element, and all C ⊂ Range(K) [\[77\]](#page-38-10).

$$
P[(K(\mathcal{D}) \in \mathcal{C})] \le e^{\epsilon} \times P[(\mathcal{K}(\mathcal{D}') \in C)] + \delta \tag{1}
$$

The equation shows a probabilistic inequality where the likelihood of random function K producing a result in set C with dataset D is limited by e ϵ times the probability of obtaining a result in set C with a different dataset D′ , emphasizing that using D′ increases the chance of results in C compared to D by a factor of e ϵ . Where ϵ denotes the privacy loss and δ denotes the error probability for the differential privacy algorithm. DP is categorized into Central Differential Privacy (CDP) and Local Differential Privacy (LDP). CDP relies on user trust in the data curator, incorporating random noise into the original aggregated model for privacy protection. Conversely, LDP ensures privacy without relying on trust by having individuals perturb or encode their local models. However, precise implementation of LDP is crucial to avoid inaccuracies in estimated frequencies, given that each individual independently perturbs their response [\[78\]](#page-38-11).

To ensure privacy in BCFL, Lu*et al.*[\[41\]](#page-36-13) suggests a novel framework for applications beyond 5G, emphasizing improved security and privacy through Blockchain integration. It also introduces a DRL optimization strategy to reduce resource costs, learning time, communication expenses, and parameter quality validation. Additionally, they added random noise in local updates for each participant to ensure privacy and tackle resource allocation challenges by optimizing resource consumption and learning quality. The system employs a DPoS protocol to validate transactions and, in the event that no consensus is achieved within a specified timeframe, diverts the computation to alternative edge servers for faster processing. Utilizes a DPoS protocol for verification, rerouting computation to alternative edge servers if consensus is not reached on time. This is followed by aggregating and verifying updates before uploading to the Blockchain, with added security through encryption using the aggregator's private key. In another work, Qi et al. [\[79\]](#page-38-12) introduced an enhanced GRU neural network tailored for traffic flow prediction. They integrate a consortium Blockchain to decentralize the FL process, ensuring that local model updates are validated by trusted consensus nodes instead of relying on a vulnerable central server. This approach effectively mitigates security risks for the central server and participating individuals. Furthermore, they implement local differential privacy by introducing Gaussian noise to local model updates, significantly bolstering location privacy protection and thwarting malicious attempts at inferring participant information through membership inference attacks.

Wang et al. [\[80\]](#page-38-13) proposed a secure and decentralized learning network for a mobile crowdsensing system utilizing unmanned aerial vehicles (UAVs), allowing UAVs to securely share model updates and verify contributions without needing a central server. Furthermore, it incorporates local differential privacy to safeguard the privacy of UAVs' updated local models and maintain privacy. Additionally, it incorporates a two-tier reinforcement learning-based incentive system to encourage the sharing of high-quality models among UAVs, even when network parameters are not explicitly disclosed. Xu et al. [\[42\]](#page-36-14) proposed a novel BCFL model for the Industrial Internet of Things, incorporating adaptive differential privacy to safeguard local model privacy without compromising accuracy. They used the Laplace mechanism, which relies on local DP, to introduce noise into the intermediate parameters during the model update phase. The cropping threshold can adapt automatically based on the training progress, effectively minimizing the influence of additional noise on model accuracy. The model further implements model parameter validation and proof of contribution consensus to effectively detect and prevent malicious node poisoning attacks, ensuring fairness through reputation and incentive mechanisms. A node reputation system is designed to assess participant reliability, calculated using a multi-subjective logic model. It serves as the basis for consensus committee election and incentives, enhancing overall fairness among participating nodes.

The authors in [\[24\]](#page-35-19) designed a privacy-preserving BCFL for home appliances. They employed DP on locally trained customer models specifically to the gradient of the local model using the regularization method, and selected customers acted as miners to aggregate the model. They suggested using the IPFS for off-chain model storage to address limited storage, recording their hashes in the Blockchain. It also introduced a novel normalization technique for improved accuracy and proposed an incentive mechanism for rewarding honest customers. Attained a minimum accuracy of 90% but highlighted the existence of a trade-off between accuracy and the level of induced noise. In [\[81\]](#page-38-14), it introduces a novel approach to tackle crucial challenges within edge computing environments by BCFL with DP facilitated by Wasserstein Generative Adversarial Networks (WGAN) in B5G networks. Minimize communication overhead between edge devices and the cloud, address data falsification concerns, and promote a collaborative data-sharing approach. WGAN generates controllable random noise that complies with DP requirements and is injected into model parameters, bolstering the privacy and security of local model data. Applying game theory to attain Nash Equilibrium among the generator, discriminator, and DP-identifier enhances the overall efficacy. In [\[82\]](#page-38-15), they introduced a novel BCFL approach, integrating generative adversarial networks and differential privacy (GAN-DP) for privacy and decentralization in Delay-Tolerant (DT) networks. They used a modified Isolation Forest to detect and remove falsified local models. They employed an improved Markov decision process to select optimal DTs for flexible asynchronous aggregation. GAN-DP addressed privacy concerns and encouraged end devices to contribute sensitive data, enhancing system performance. It also supported local data augmentation, mitigating size and class balance issues, improving learning efficiency, and reducing operational costs. Cui et al. [\[83\]](#page-38-16) designed an innovative GAN-driven differentially private algorithm to protect the privacy of local model parameters by adding controlled noise, ensuring compliance with differential privacy requirements while improving the utility of the anomaly detection model in IoT Infrastructures.

Safeguarding medical records data represents a crucial challenge in the modern digital age, demanding advanced protective measures as cyber threats evolve. In [\[84\]](#page-38-17) and [\[85\]](#page-38-18), proposed BCFL to enhance patient data privacy in healthcare applications along with DP noise added into the local models. The system addressed storage efficiency by storing only the hash value on IPFS within the Blockchain while the original data was kept locally. Liu et al. [\[86\]](#page-38-19) introduced a cross-layer architecture, employing differential data sharing for origin data and model providers. Their targeted incentive mechanism, designed as a two-stage Stackelberg game, optimizes utility, enhancing privacy and speeding up performance, surpassing the simple shared model and data schemes by 1.72 and 2.59 seconds, respectively. Furthermore, Laplace differential privacy protects intermediate privacy parameters during aggregation. Li et al. [\[87\]](#page-39-0)

proposed an architecture to enhance FL privacy and security while dealing with lazy clients and SPoF issues. It introduces a bounded loss function to analyze the relationship between block creation and the impact of lazy clients on training efficiency. Optimizing the loss function improves performance despite the presence of lazy clients. Also, it provides learning incentives by optimizing computational resource allocation and ensuring data privacy through differential privacy. In [\[88\]](#page-39-1), the authors have presented a lightweight authentication framework tailored for BCFL. This framework incorporates a flexible Blockchain consensus algorithm and zero-knowledge proof to validate the identity of participants. Furthermore, an adaptive model aggregation algorithm, considering both the model's quality and the contribution of each node, is employed to boost overall performance, thereby attaining a high level of training accuracy. The Laplacian mechanism for differential privacy protection is applied in intermediate gradients to protect local data privacy from inference assaults while reducing the possibility of data leaking.

Numerous researchers are developing custom Blockchains for various applications, including exchanging and verifying local model parameters in IoT-based Federated Learning. For instance, Salim et al. [\[89\]](#page-39-2) developed a Python-based custom Blockchain for Blockchain-based Explainable Federated Learning (DP-BFL) to enhance security in IoT-based Social Media 3.0 networks. DP-BFL employs differential privacy to safeguard the exchanged local model updates and the aggregated global model from potential inference or membership attacks. Furthermore, this allows Internet-enabled devices to actively contribute to a globally preserved privacy model by uploading local updates to Blockchain miners. These miners evaluate and reward these contributions, with the added feature of introducing adaptable Gaussian noise to enhance privacy. Miao et al. [\[90\]](#page-39-3) developed a secure data-sharing model using peer-to-peer FL with Blockchaindistributed ledgers to ensure data transparency and differential privacy for enhanced data privacy in IoT. They employed team-based data sharing with reward and punishment mechanisms to guarantee high-quality and reliable data sharing, where team sponsors initiate tasks and assess members' contributions, rewarding active participants and excluding poorly engaged members. They suggested a proof of model contribution consensus algorithm that relies on the contribution of the training model to enhance computational efficiency. Experimental results confirmed the effectiveness of their approach, highlighting high accuracy and improved privacy in IoT. Zhang*et al.*[\[91\]](#page-39-4) present a privacy-protecting FL framework for IoT that employs Blockchain and committee consensus. Local updates are verified through Blockchain, ensuring data privacy with local differential privacy where Laplace noise is used. Committee nodes validate model parameters, and when sufficient validation responses are received, updates are aggregated through a smart contract for the next training round.

In [\[45\]](#page-36-17) explores a permissioned Blockchain system with the Proof of Training Quality (PoQ) consensus process, optimizing node computing resources during data model training. The Laplace mechanism enhances local data model privacy and improves computing resource utilization and efficiency of the data-sharing scheme. Chen*et al.*[\[92\]](#page-39-5) introduced an efficient Privacy-Preserving and Traceable FL framework with minimal overhead and high performance. Their innovative approach incorporates hierarchical aggregate Federated Learning, involving sub-aggregators and aggregators and adding noise to local model parameters using random seeds. The sub-aggregator can reconstruct pseudorandom weights with user IDs or decrypt subtracted parameters. After aggregating and encrypting the parameters, the sub-aggregator forwards them to the aggregator, which decrypts and combines parameters, subtracts user-added noise, and obtains global parameters sent to the server. In [\[93\]](#page-39-6), PriModChain, a specialized FL architecture for Industrial Internet of Things networks, incorporates a differential privacy approach to add artificial noise to locally generated models, which reduces the risk of the identification of individual records. The secure transfer of the global ML model is facilitated through smart contracts, ensuring consensus on update verification and transparency in FL updates. Simulations in Python evaluate PriModChain's feasibility in terms of security, privacy, safety, reliability, and resilience, highlighting its innovative features in promoting unbiased and error-free data manipulations for enhanced FL safety and reliability against external data threats. The frameworks [\[92,](#page-39-5) [93\]](#page-39-6) integrate FL with Blockchain and IPFS, guaranteeing the traceability and immutability of model parameters, particularly suitable for Industrial Internet of Things scenarios. Table [4](#page-20-0) comprehensively outlines the strategies employed for privacy preservation in BCFL by applying the differential privacy approach. The table details the diverse methods and techniques this privacy framework utilizes to ensure robust privacy measures in FL on the Blockchain.

### 3 Privacy Preservation in BCFL using Homomorphic Encryption-based Approaches

Homomorphic Encryption (HE) is a technique that enables computations on encrypted data, yielding encrypted results without requiring data decryption [\[94\]](#page-39-7). In FL, users can employ HE to secure their parameters while sharing them with the server, which protects data privacy and facilitates accurate model aggregation [\[95,](#page-39-8) [96\]](#page-39-9). Typically, in FL, the server involves the processing function f, which aggregates parameters from local models across all participating nodes. The encryption computation utilizing HE is detailed in equation [2](#page-19-0) as follows:

$$
E(m_1)* E(m_2) *\cdots* E(m_n) = E(m_1 *m_2* \cdots *m_n)
$$
\n(2)

Where, (m1, m2, m3, . . . , mn) denotes the parameters and E represents the encryption algorithm.

Privacy-preserving in Blockchain-based Federated Learning Systems

| Reference paper | CDP/ | Exponential | Gaussian | Laplace Dis | Random Dis | Parameter |
|-----------------|------|--------------|--------------|-------------|------------|-----------------|
| | LDP | Distribution | Distribution | tribution | tribution | |
| [41] | LDP | ✓ | | | | Local Gradient |
| [79, 82, 87] | LDP | | ✓ | | | Local Weight |
| [80, 85, 86] | LDP | | | ✓ | | Local model |
| [24, 42, 91] | LDP | | | ✓ | | Local Gradient |
| [81] | LDP | | | ✓ | | Local Weight |
| [45, 83, 88] | LDP | | | ✓ | | Local Weight |
| [89, 93] | LDP | | ✓ | | | Local Gradient |
| [90] | CDP | | | ✓ | | Global Gradient |
| [92] | LDP | | | | ✓ | Global Gradient |

<span id="page-20-0"></span>**Table 4:** Privacy Preservation in BCFL using using differential privacy approaches

CDP: Central Differential Privacy, LDP: Local Differential Privacy,

Chen*et al.*[\[97\]](#page-39-10) developed a data-sharing private model that utilizes BCFL. The study addresses data privacy by proposing a scheme based on FL and employs HE to safeguard user parameters during parameter updates. To alleviate storage issues and manage diverse data formats, the work combines Blockchain storage with off-blockchain key-value storage, using Blockchain only for data pointers. An innovative on-chain data retrieval mechanism selects data providers for FL. Additionally, the research introduces a consensus mechanism called contribution authorizing Byzantine faulttolerant algorithm (Con-dBFT), based on contribution, to improve fairness and efficiency in the system. Wang*et al.*[\[98\]](#page-39-11) proposed a BCFL to address the security threats faced by the privacy-preserving FL, which enhances Multi-Krum technology by integrating it with HE, resulting in ciphertext-level model aggregation and filtering. This method ensures the verifiability of local models and preserves user privacy. In [\[99\]](#page-39-12), it also protects the local model's gradients through encryption using the Threshold Paillier encryption algorithm. Furthermore, it introduces a reputation-based incentive mechanism within the Internet of Vehicles to incentivize honest participation in FL, and the authors used a semidecentralized consortium Blockchain structure with an Elliptic Curve signature and Merkle tree to ensure data security. Sun*et al.*[\[100\]](#page-39-13) proposed BCFL, which encrypts the local gradients using the Bresson-Catalano-Pointcheva (BCP) mechanism and then adds homomorphic noise to each encrypted gradient. The modified gradients are then gathered and assessed for quality using a joint audit algorithm. The system identifies any gradients that lead to the global model's degradation, effectively removing them from the model. It then aggregates the remaining gradients, generating a new global model with reduced processing time. However, the behavior and audit chains may become overwhelming as data owners increase, leading to delays and processing times, potentially limiting its practical use in large-scale Federated Learning scenarios. In another work, Miao*et al.*[\[101\]](#page-39-14) created a BCFL-based byzantine robust model to ensure privacy and mitigate the system to infer the client's local data. They create a reliable global model by identifying malicious gradients and honest gradient vectors through cosine similarity. Additionally, they used the Cheon-Kim-Kim-Song (CKKS) scheme based on fully homomorphic encryption to safeguard privacy and encrypt local gradients. Furthermore, it significantly decreased the computation and communication overheads. In [\[51\]](#page-37-3), researchers utilized a similar approach to safeguard the local model from inference attacks. Chen*et al.*[\[53\]](#page-37-5) also an effective non-interactive designated decryptor function encryption method as a novel lightweight cryptography tool. The method effectively maintains the accuracy of the global model with comparatively low and efficient transmission costs. Sezer et al. [\[102\]](#page-39-15) introduced the BCFL framework to guarantee the security and privacy of IoT sensor-based structures utilizing sampled data from electrochemical sensors. Within this architecture, they employed Federated models and cryptographic primitives to ensure user and data privacy in off-chain fog nodes with high accuracy, efficiency, and security.

However, existing HE-based systems face significant challenges, such as the reliance on trusted third parties for key management, increased complexity and vulnerability, and scalability issues with Deep Learning (DL) models due to computational constraints in encrypting and decrypting the trainable parameters [\[103\]](#page-39-16). The authors in [\[104\]](#page-39-17) introduced a BCFL system empowered by edge computing for resource management in the Internet of Medical Things (IoMT). It employs an improved linear regressor model and Paillier encryption for gradient parameter security. Mobile devices act as initiators for model bootstrapping and local task initialization, while validators, selected based on computing capabilities, engage in Blockchain consensus processes, block verification, and validation. The computing threshold for validator miners is determined using maximum likelihood estimation, ensuring a data-driven approach to resource allocation. The resulting blocks are digitally signed, hashed, and encapsulated into the Blockchain, enhancing security features for IoMT and edge computing.

The approach presented by Qi*et al.*[\[50\]](#page-37-2) guarantees gradient privacy using HE while tackling trust issues and Single Point of Failure (SPoF) through a reputation system based on smart contracts. Additionally, the model addresses Blockchain storage challenges by implementing an on/off-chain storage strategy. Li*et al.*[\[61\]](#page-37-13) proposed a privacypreserving FL system, employing distributed ElGamal encryption to safeguard gradient inversion attacks. The system recovers original data from local sign-based quantized gradients and utilizes smart contracts for secure self-aggregation among participants without reliance on a centralized server. Some works have focused on privacy in vertical FL, proposing a novel technique that utilizes DL and Blockchain to preserve the privacy of electronic health records by developing a secure logistic regression architecture [\[105\]](#page-39-18).

In [\[106\]](#page-40-0) uses a combination of FL, Blockchain, and HE to compute a global behavioral fingerprinting model for a target object in an IoT context. This fingerprint is derived from the interactions of an object with different peers and allows anomaly detection in the network to be performed. The underlying model, thanks to HE, guarantees the privacy of both the target object and the different workers, as well as the robustness of the strategy in the presence of attacks.

Li*et al.*enforced privacy safeguards in [\[107\]](#page-40-1) by combining BCFL and HE within a traceable identity-based scheme, ensuring the records' integrity and traceability. They aimed to establish an anonymous identity-based scheme for safeguarding driver identity privacy by adopting FL and utilizing the classic Feige-Fiat-Shamir zero-knowledge-proof authentication.

Table [5](#page-22-0) offers a comprehensive summary of privacy preservation within BCFL, utilizing homomorphic encryption with diverse approaches. Awan et al. [\[46\]](#page-36-18) enhanced the Paillier cryptosystem, incorporating features like additive Homomorphic Encryption and proxy re-encryption to safeguard individual local model updates in FL. Their approach addresses issues such as random client dropouts through asynchronous recording on the Blockchain. Integrating BCFL mitigates multiparty dropout and enhances transparency, verifiability, and data privacy protection.

## 4 Privacy preservation using BCFL with Secure Multiparty Computation approach

Secure Multiparty Computation (SMPC), introduced by Andrew Yao in 1982, forms the foundational protocol for secure computations [\[109\]](#page-40-2). It facilitates different parties (P1, P<sup>2</sup> . . . Pn), with private data (d1, d<sup>2</sup> . . . dn), in jointly computing an objective function (f) on their private data f(P1, P<sup>2</sup> . . . Pn), thus preserving the confidentiality of the input data [\[94\]](#page-39-7). The authors in [\[48\]](#page-37-0) present BCFL with novel committee consensus, utilizing Blockchain for global model storage and local updates. The innovative committee consensus minimizes computation and enhances security. A committee validates updates in each round, reinforcing the global model while rejecting incorrect ones. It allows flexible participation, enabling nodes to join or leave without disruption, and uses Smart Contracts driven by Blockchain transactions to execute the central server functions.

However, some studies emphasize persistent security concerns in key management, particularly regarding secret key ownership in adopted cryptographic systems. To tackle this issue, multiple studies, exemplified by [\[110\]](#page-40-3) and [\[111\]](#page-40-4), advocate for the adoption of the SecAgg protocol [\[112\]](#page-40-5). Within this protocol, secret keys are collaboratively shared and securely stored using Blockchain. Fang et al. [\[111\]](#page-40-4) also address these concerns by employing Blockchain to verify global model gradients, effectively mitigating the potential risk of tampering attacks. Moreover, gradient compression methods are employed to alleviate communication overhead. In [\[110\]](#page-40-3), a variant of ElGamal encryption was employed to validate the accuracy of aggregated results.

In the architecture proposed by [\[113\]](#page-40-6), multiple smart hospitals in different regions are assumed, each equipped with a cluster of IoT medical devices and an edge server executing FL tasks. This verification involves encrypted inference through a SMPC protocol. Upon verification, the Blockchain node obtains the authenticated portion of the local model. Utilizing SMPC-based secure aggregation, the Blockchain and the hospital collaborate to reach a consensus on the global model, which is securely stored in the Blockchain. The tamper-proof storage system then disseminates the revised global model to all involved hospitals in the Federated Learning round.

In a Blockchain-based decentralized, secure multiparty Learning system outlined in [\[114\]](#page-40-7), every client calculates and disseminates its local model via the Blockchain. Following a calibration process specifically designed for edge computing-based IoT applications, clients execute models received from other participants. The system employs a cooperative mining strategy, incorporating on-chain and off-chain mining, to address potential attacks during model broadcasting and calibration.

## 5 Privacy preservation using BCFL with reward-driven approaches

Integrating BCFL with incentive mechanisms not only addresses the challenge of preserving user privacy and encouraging active participation but also ensures the confidentiality and security of the BCFL system. By leveraging smart contracts, BCFL establishes a transparent and tamper-proof framework for fair and verifiable incentives, mitigating concerns about opaque reward structures in traditional BCFL platforms. This innovative integration promotes collaboration and significantly enhances the effectiveness and trustworthiness of the BCFL system [\[115,](#page-40-8) [107\]](#page-40-1). BCFL's selection

| Reference<br>paper | Encryption<br>Type | Privacy scheme | Parameter | Attack against | Adversary |
|--------------------|--------------------|------------------------------------------|----------------------------------------------|---------------------------------------------------------------------|---------------------|
| [97] | PHE | Additive | Local<br>Gradi<br>ent | I | Server |
| [98] | PHE | Paillier additive | Local Weights | I&P | HbCS & MalC |
| [100] | FHE | BCP | Local<br>Gradi<br>ent | I&P | HbCS |
| [51, 101] | FHE | CKKS | Local<br>Gradi<br>ent | I | Server & MalC |
| [53] | FE | NDD-FE | Local Weights | I | - |
| [104] | PFE | Paillier additive | Local<br>Gradi<br>ent,<br>Global<br>Gradient | Transaction Hack<br>ing, I, Imperson<br>ation&<br>51%<br>at<br>tack | Insider or Outsider |
| [61] | PHE | Distributed ElGamal | Local<br>Gradi<br>ent | Gradient<br>Inver<br>sion | HbC clients |
| [108] | Encryption | Proxy<br>re-encryption,<br>ECC, SS,CH | Local Weights | I | HbC clients |
| [105] | Encryption | Proxy re-encryption | Global<br>Weights | I | - |
| [46] | PFE | Paillier additive&Proxy<br>re-encryption | Local<br>Gradi<br>ent | I | SHbCS |
| [50, 99] | PHE | Paillier additive | Local<br>Gradi<br>ent | I&P | Insider/Outsider |
| [107] | FHE | Dijk-Gentry-Halevi<br>Vaikutanathan | Local Model&<br>Global Model | I&P | MalC,HbCS & SHbCS |


| | **Table 5:** Privacy Preservation in BCFL using HE | | |
|--|------------------------------------------------|--|--|
| | | | |

FHE: Fully Homomorphic Encryption, PHE: Partially Homormophic Encryption, HbCS: Honest-but-Curious Server,MalC:

Malicious Client,

I: Inference attack, P: Poisoning attack, SS:Secret Sharing, ECC:Elliptic Curve Cryptography, CH: Chameleon hash, SHbCS: Semi Honest-but-Curious Server

process is guided by a strong emphasis on client reputation. Higher-reputation clients are more likely to contribute reliable and high-quality training. After each training task, client reputations are updated based on their behavior, influencing client selection in subsequent training by considering their reputation records.

Assessing the contributions of diverse data providers is fundamental for fair profit allocation. Implementing reasonable contribution evaluation criteria enhances the incentive mechanism, attracting more participants to join. Clients' contributions can be distilled into two main categories: data quality and data quantity. For example, Salim*et al.*[\[89\]](#page-39-2) introduced an incentive mechanism designed to combat free-riding attacks by proportionally rewarding participants based on the quality of their contributions. They implemented the Quality-Based Consensus (QBC) algorithm in DP-based BCFL, ensuring that only legitimate local updates contribute to the global model. QBC rewards participants for added updates, promoting high-quality contributions, and selects the consensus leader based on the miner with the highest accuracy for inclusion of the most qualified models in the global update.

Furthermore, Qi*et al.*[\[116\]](#page-40-10) proposed a mechanism to motivate data owners to provide high-quality data by establishing a distinct equilibrium by analyzing noncooperative games. A reputation layer utilizing Blockchain for collaborative assessment strengthens the equilibrium, which signifies that contributing the highest quality data leads to the highest reward. In the reward layer, incentives, determined by both the quantity and quality of contributions, are granted using a reputation-weighted algorithm to ensure fair distribution. The unique Nash equilibrium in the non-cooperative data-sharing game shows that data owners act selfishly to maximize their profits.


| Approach | Reference Paper |
|--------------------------------|-----------------------|
| Client Data Contribution | [24, 89, 98, 99, 119, |
| | 120, 116, 117] |
| Auction theory-based schemes | [121, 122, 123] |
| Mechanism design-based schemes | [118] |
| Contract-theoretic approach | [29] |
| Game theory-based schemes | [86] |
| Smart contract-based schemes | [50, 51, 124] |

**Table 6:** Privacy Preservation in BCFL using Reward Driven approaches

Additionally, in [\[99\]](#page-39-12) proposed Deepchain, which also provides reward based on the data quantity. The system involves data owners collaborating to train a model and miners processing transactions for model updates on DeepChain. Data owners pay transaction fees based on their data quantity, with miners competing to process transactions and receive rewards. Value-based incentives promote correct participant behavior. Smart contracts regulate behavior and track attackers. The system assesses global model accuracy using local updates, penalizing invalid transactions and considering updates with decreased accuracy as potentially malicious. In [\[24,](#page-35-19) [98\]](#page-39-11), a customer-centric incentive system assesses contributions and calculates reputations using Multi-KRUM to eliminate unsatisfactory and malicious updates. In conjunction with this study, Abdel*et al.*[\[117\]](#page-40-13) enforced a hybrid incentive strategy, incorporating Multi-KRUM for providing incentives. The authors in [\[118\]](#page-40-17) introduce a fair and incentive-aware mechanism. Workers actively choose their top k previous models during each round, assigning precisely one vote to each model. The smart contract then calculates aggregated votes, determines worker counts from the preceding round, and allocates rewards in descending order based on these counts.

Rewards for edge nodes, tied to their contributions to the global model, may lack fairness and reasonability. This imbalance arises because edge nodes with substantial datasets and robust computational resources enjoy an unfair advantage, resulting in uneven reward distribution. However, [\[51\]](#page-37-3) introduced the forward bidding mechanism, which selects the top k edge nodes within the FL task publisher/server budget and compensates them accordingly. To prevent edge nodes from withdrawing during model training, they must submit a fixed security amount, refunded upon successful convergence of the global model along with the reward.

In certain studies, a consensus mechanism has been introduced to fairly reward legitimate users across cross-silos using the model quality. Participants earn a reputation by staking cryptocurrency deposits or their existing reputation in the Proof-of-Federated Deep-Learning (PoFDL) consensus mechanism proposed in [\[119\]](#page-40-11). This approach enhances trust among participants and reinforces the immutability of the Blockchain. Participants who take on the role of validator nodes gain reputation through their active involvement in the PoFDL process, establishing a mechanism where contributions to the Federated Learning system increase reputation within the network. Furthermore, Kashyap*et al.*[\[120\]](#page-40-12) introduced Proof of Interpretation and Selection (PoIS), a consensus mechanism for participant incentives. PoIS assesses individual contributions using label-wise model interpretation through Shapley value, detecting adversaries through feature attribution aggregation.

The authors in [\[124\]](#page-40-18) proposed the "Balanced Sign SGD ", a 1-bit gradient compression method that emphasizes privacy by exchanging only the signs of gradients, excluding the gradients themselves. Additionally, it introduces a novel committee-based consensus algorithm featuring a personalized incentive mechanism. It also ensures that every contributing participant is rewarded based on their distinct contributions to enhancing the model. Committee members engage in global aggregation and achieve consensus through cross-validation, with the first finisher receiving additional rewards. Other committee members are rewarded based on their response times, working as evidence of effectiveness. Participants contributing to local models receive rewards based on the cosine distance of their contributions to the global model, with rewards increasing proportionally as the cosine distance approaches predetermined thresholds. In Qi*et al.*[\[50\]](#page-37-2), a smart contract-based reputation scheme uses the Reputation Contract (RC) and Hunter Contract (HC) to establish trust. The RC assigns reputation scores, rewarding positive actions and penalizing negatives. Simultaneously, the HC guards against malicious nodes by verifying weights' accuracy and reporting dishonest behavior to the RC, contributing to a trustworthy system.

Some studies incorporate an auction-based mechanism to reward participants efficiently, ensuring a fair and transparent compensation system for their contributions. For example, Batool*et al.*[\[121\]](#page-40-14) proposed a multidimensional auctionbased reward mechanism that utilizes a smart contract to compensate participating clients with cryptocurrencies. This auction considers factors like computational and network resources and local data quality. The reward distribution is based on the Shapley value, ensuring fairness by measuring the relative contribution of each client. Kang*et al.*introduced a Subjective Logic approach, as outlined in [\[122\]](#page-40-15), to assess individual reputations in the context of

| Reference<br>paper | Privacy Scheme Used | Parameter | Attack against | Adversary |
|--------------------|--------------------------------------------------|----------------|-------------------------------------------------------------------------------------|------------------------------------|
| [127] | HE & SMPC | Local Gradient | I | MalC, Malicious<br>Miners |
| [108] | HE & SMPC | Local models | I | HbC, Clients |
| [125] | HE & SMPC | Local Models | I&P | HbCS |
| [126] | HE & SMPC | Local Model | I | MalC |
| [119] | DP & SMPC | Local Gradient | Byzantine<br>and<br>Sybil<br>attacks,<br>Model inversion, I, Model theft<br>attacks | HbCS,<br>HbCC,<br>MalC |
| [128] | DP & SMPC | Local Gradient | I | HbC, MalC |
| [129] | DP & HE | Local weights | Model extraction attack, Model<br>reverse attack | |
| [130] | DP& HE & SMPC | Local Gradient | Collusion attack, Sybil attack, I,<br>& P | HbCC, MalC |
| [131] | SS, Combine Paillier and<br>ElGamal based scheme | Local Gradient | I | Internal or Exter<br>nal Adversary |

<span id="page-24-0"></span>**Table 7:** Privacy Preservation in BCFL using hybrid privacy approaches

HbCS: Honest-but-Curious Server, MalC: Malicious Client, I: Inference attack, P: Poisoning attack, HbCC: Honest-but-Curious Client, SS: Secret Sharing

vehicular networks. This framework for probabilistic information fusion relies on subjective beliefs and operates by evaluating interactions as the basis for reputation assessment. In [\[29\]](#page-36-1), the study extends [\[122\]](#page-40-15) by introducing a multi-subjective logic function to enhance the reward approach. The authors also propose a worker selection scheme for dependable Federated Learning, incorporating a multiweight subjective logic model for reputation assessment. Blockchain integration ensures secure decentralized reputation management with nonrepudiation and tamper-resistant properties. Additionally, the incentive mechanism, blending reputation and contract theory, encourages high-reputation mobile devices with quality data to engage in model learning actively. Kang*et al.*[\[123\]](#page-40-16) proposed Multi-weight subjective logic to enhance reputation calculation in BCFL, considering interaction attributes like frequency, timelines, and effects.

In [\[86\]](#page-38-19), the study proposes an incentive mechanism for a privacy-preserved data-sharing system, formulating it as a two-stage Stackelberg game. The mechanism is designed to maximize the utility of data requesters and two types of data providers, considering their distinct roles and contributions. The non-cooperative nature of the interactions justifies the choice of a Stackelberg game model, the hierarchical relationship between requesters and providers, and the one-to-many data-sharing structure. Table [6](#page-23-0) presents an overview of privacy preservation in BCFL by enforcing a reward-driven approach using various methodologies.

## 6 Privacy protection using BCFL with Hybrid Privacy Approaches

Several studies indicate that integrating diverse privacy approaches helps mitigate security and privacy attacks in BCFL. This section explores hybrid approaches that provide privacy by combining various privacy-preserving techniques. For instance, integrating differential privacy for initial data aggregation and applying homomorphic encryption could yield a more resilient solution. The amalgamation of HE and SMPC in BCFL markedly enhances the confidentiality and privacy of the FL process within a transparent and decentralized Blockchain framework. This integration fosters trust and security in data sharing and model training, as exemplified by [\[125\]](#page-40-19) and [\[126\]](#page-40-20). HE enables computations on encrypted data, preserving the privacy of individual contributions, while SMPC ensures secure collaboration among participants without exposing their raw data. Table [7](#page-24-0) summarizes privacy preservation in BCFL by employing various privacy approaches. In the privacy-focused collaborative training proposed by Zhu*et al.*[\[127\]](#page-41-0), participants protect their local gradients using the Paillier cryptosystem with threshold decryption and a secure multi-party aggregation algorithm. This method ensures data privacy during collaborative training by transforming gradients into a secure form.

Furthermore, in [\[108\]](#page-40-9) introduced a flexible and trustworthy framework for industrial intelligence, integrating autonomous FL and secure data-sharing on the Blockchain. The proposed approach preserves privacy through a combination of

HE and SMPC approaches, which can enhance the security of sensitive data. Their approach involves an autonomous Federated extreme gradient boosting Learning algorithm for privacy protection, verifiability of aggregated results, and model reliability. They also introduced a secure and trusted trading mechanism for controlled on-demand data sharing, a threshold aggregation signature for model ownership assurance, and proxy re-encryption and retrieval to facilitate controllable and reliable data sharing with high accuracy and performance. Feng*et al.*[\[125\]](#page-40-19) presents a framework for decentralized cross-domain FL in 5G-enabled UAVs, leveraging Blockchain technology. It utilizes multi-signature smart contracts for dynamic cross-domain authentication, enhancing collaborative Learning. The framework employs decentralized smart contracts for model aggregation, addressing security concerns related to centralized servers. Additional security measures, such as homomorphic encryption and multiparty computation, are applied to protect against local update attacks.

FL presents a promising avenue for developing energy-efficient consensus algorithms, addressing the resource-intensive nature of traditional methods like PoW. Integrating the consensus process with FL eliminates the need for extra computational resources dedicated to separate consensus algorithms, potentially leading to substantial energy savings. From a communication standpoint, public Blockchains often require miners to broadcast their local model parameters, resulting in considerable communication overhead, especially as the number of miners grows. The authors in [\[126\]](#page-40-20) proposed a method to mitigate these challenges using a novel consensus protocol like Proof-of-Federated-Learning (PoFL), leveraging the computational overhead of local training in Federated Learning as proof for consensus. PoFL significantly reduces mining power wastage and trims computational overhead while ensuring efficient consensus processes without reference to external sources. Moreover, it proposed a novel method utilizing a reverse game-based data trading mechanism to enhance data privacy by determining optimal data trading probabilities and pricing strategies. This approach encourages data pools with high privacy risks to trade less data at a higher cost, incentivizing them to train models without data leakage. Additionally, a privacy-preserving model verification mechanism consists of HE-based label prediction and SMPC with two-party-based label comparison, ensuring model accuracy while preserving privacy for both the task requester's test data and the pool's submitted model.

In [\[119\]](#page-40-11), they explored the integration of secure multi-party computation and differential privacy to enhance system privacy. Also, a permissioned Blockchain and private peer-to-peer channels are utilized in their approach. Encourage cross-silo FL using the lightweight and energy-efficient consensus Proof-of-Federated Deep-Learning protocol, effectively detecting and classifying IIoT attacks in Non-IID and IID scenarios. Bai et al. [\[131\]](#page-41-4) proposed a Blockchain-based privacy-preserving approach using no trusted third-party Federated Learning. They employ a conference key agreement to negotiate keys between the initiator and partners, eliminating the need for a trusted third party. A double-layer encryption mechanism ensures privacy encrypts local and global models, preventing partners from accessing each other's private information. The decentralized nature of Blockchain enhances transparency, traceability, and resilience against SPoF. Additionally, they used an efficient secret-sharing scheme to encrypt model parameters, reducing communication costs and computation time compared to Paillier and ElGamal-based schemes and secure aggregation protocols.

Bolstering security against Sybil attacks, poisoning attacks, and inference attacks, Shayan et al. [\[128\]](#page-41-1) incorporate differential privacy and encryption approach within BCFL with secure and private multi-party ML. In each iteration, peers compute local model updates, keeping them private by masking with differentially private noise obtained from a set of peers identified through a verifiable random function. Verification committees validate these masked updates to prevent poisoning. If the majority of the committee approves, the updates are divided into Shamir's secret shares and passed to an aggregation committee. This committee securely aggregates the unmasked updates, with contributing peers and committee members receiving additional stake in the system. The aggregated updates are then added to the global model within a newly created Blockchain block and shared with all peers, and the process repeats with the updated global model and stake.

The studies outlined in [\[129\]](#page-41-2) focus on establishing a secure data-sharing mechanism to uphold privacy among numerous distributed users. It also suggests a data protection aggregation approach that utilizes distributed K-means clustering with DP and HE, random forest with DP, and AdaBoost with HE to enhance data protection in Industrial IoT scenarios. Sun*et al.*[\[130\]](#page-41-3) address the challenge of enhancing security and privacy in their work. They use a Blockchain to record each global model update, ensuring the verifiability and traceability of local updates through permanent records. It also enables an incentive mechanism tailored to user contributions. Additionally, HE secures users' local model updates. A validation process precedes local update aggregation to thwart poisoning attacks, and privacy is maintained with differential privacy noise. Ultimately, they establish a secure aggregation scheme for local updates using the Shamir secret sharing technique, balancing utility and privacy compared to differential privacy.

Table [8](#page-26-0) elucidates the overview of studies specifically in BCFL, highlighting their privacy approach, Blockchain types, the Blockchain frameworks utilized within Federated Learning systems, consensus algorithms, and block storage techniques.

**Table 8:** Summary of studies on integration of Blockchain enabled Federated Learning, elucidating their privacy preservation methods, types of Blockchain used, the Blockchain frameworks integrated within Federated Learning systems, consensus algorithms employed, block storage, and data distribution used.


| | Techniques | Reference Paper |
|---------------------|----------------------------|----------------------------------------------------------------------------------------|
| | Differential privacy | [24, 41, 42, 45, 63, 69, 79, 80, 81, 82, |
| | | 83, 84, 85, 86, 87, 88, 89, 91, 92, 93] |
| | Homomorphic encryption | [50, 61, 68, 97, 98, 99, 100, 102, 104, |
| | | 107, 126, 53] |
| | Secure multi-party computa | [46, 48, 110, 111, 114] |
| Privacy Approach | tion | |
| | Reward driven approaches | [29, 42, 64, 66, 73, 75, 80, 86, 87, 89, |
| | | 90, 98, 99, 116, 117, 121, 122, 119, |
| | | 123] |
| | Hybrid privacy approaches | [125, 126, 119, 127, 129, 108, 131, 128, |
| | | 130] |
| | PoW | [63, 64, 67, 73, 80, 81, 83, 87, 89, 104, |
| | | 107, 114] |
| | PoS | [53] |
| | DPoS | [41, 66] |
| | pBFT | [29, 43, 50, 75, 76, 79, 86, 98, 125, 130, |
| | | 123] |
| Consensus Protocol | PoA | [69, 85] |
| | PoQ | [45] |
| | PoF | [69, 82, 126, 128] |
| | PoC | [102] |
| | PoFL | [126] |
| | RAFT | [125, 129] |
| | Con-dBFT | [97] |
| | Algorand | [24, 99, 117] |
| | Public | [41, 43, 67, 68, 69, 81, 82, 83, 85, 93, |
| | | 117, 121, 129] |
| | Private | [101, 113] |
| Blockchain Type | Permissioned | [61, 66, 70, 74, 108, 119] |
| | Consortium | [24, 29, 50, 63, 72, 75, 79, 80, 82, 86, |
| | | 97, 98, 100, 104, 116, 122, 123, 125, |
| | | 131] |
| | Ethereum | [46, 51, 61, 68, 85, 90, 93, 101, 104, |
| | | 108, 110, 117, 121, 127] |
| Blockchain Platform | Hyperledger Fabric | [63, 70, 72, 75, 98, 100, 116, 125, 130] |
| | Custom Blockchain | [89] |
| | off-chain | [24, 43, 46, 50, 51, 63, 68, 69, 84, 85, |
| | | 86, 88, 92, 93, 97, 102, 121, 125, 128] |
| Blockchain Storage | on-chain | [61, 72, 73, 75, 81, 83, 86, 91, 100, 102, |
| | | 104] |
| | IID | [24, 41, 42, 43, 53, 63, 66, 68, 69, 72, |
| | | 73, 76, 81, 83, 86, 88, 89, 92, 93, 99, 97,<br>100, 101, 113, 116, 117, 119, 126, 128] |
| Data Distribution | Non-IID | [70, 75, 76, 82, 87, 90, 98, 116, 117, |
| | | 119, 120, 127] |
| | | |

## <span id="page-27-0"></span>8 Privacy Preservation using Cross-chained FL Approaches

In this section, we have delved into the intricacies of cross-chain-enabled Federated Learning as a mechanism for preserving privacy. The discussion thoroughly explores how leveraging cross-chain capabilities enhances Federated Learning methodologies to uphold and safeguard privacy.

## 1 Overview of Cross-chained FL

Recent studies indicate that BCFL systems preserve the system's privacy. Still, the limited scalability of a single Blockchain becomes evident as the number of FL training tasks increases, resulting in the simultaneous generation of numerous blocks and subsequent queuing for block verification. This scalability challenge emerges due to the difficulty of managing massive block data with a limited number of miners, leading to constrained throughput, reduced efficiency, and slower FL training processes [\[132\]](#page-41-5). Additionally, BCFL incurs a substantial communication cost for model update transmission, requiring multiple rounds of communication to achieve the desired accuracy level. This arises from frequent gradient exchanges among peers over limited bandwidth channels, and as the block data size increases, so does the flow of model updates across the Blockchain network, posing significant communication challenges. Moreover, Blockchain-enabled Federated Learning encounters numerous challenges, including selecting efficient miners, consensus algorithm implementation, and chain validation [\[133,](#page-41-6) [134,](#page-41-7) [48\]](#page-37-0). Cross-chain technology enables data exchange among multiple Blockchains. Which also facilitates secure data transfers while maintaining the same machine-learning models throughout various Blockchain networks [\[135,](#page-41-8) [1\]](#page-34-0). The following highlights the major benefits and key advantages of cross-chained enabled FL [\[136\]](#page-41-9).

- Higher Scalability: Cross-chained FL outperforms single Blockchain in efficiency and scalability. Unlike single Blockchain limitations in managing FL training tasks, cross-chained systems efficiently distribute workloads, mitigating bottlenecks. The parallel processing capability ensures optimal scalability, seamlessly accommodating growing FL task demands. Multiple interconnected Blockchains enhance resource management, improving system efficiency and security compared to a singular Blockchain system. The cross-chain integration in FL enables global collaboration, fostering diverse participation and data federation across regions and industries.
- Low Communication Cost: Blockchain-based FL requires frequent gradient exchanges to synchronize model updates among peers, utilizing limited bandwidth channels. Cross-chained FL networks employ a compressed gradient strategy, ensuring cost-effectiveness and high accuracy. Due to the compression of gradients, this scheme fortifies the safeguarding of training data privacy by reducing the efficacy of gradient leakage attacks when there is an inadequate amount of gradient information [\[57\]](#page-37-9).
- Reduced Single-Point-of-Failure Risks: Cross-chain Federated Learning mitigates the risks associated with a single-point-of-failure. Distributing the learning process across multiple Blockchain's makes the system more resilient to potential disruptions or attacks on a single chain.

## 2 Solutions for privacy preservation using cross-chain approaches

In this section, we explored the intricacies of the cross-chained network, which has diverse privacy solutions meticulously crafted to safeguard the system's privacy by integrating cross-chain-enabled Federated Learning. Kang*et al.*[\[136\]](#page-41-9) introduced an innovative cross-chain powered FL framework with parallel Blockchains designed to handle model updates securely, with scalability and flexibility, eliminating the constraints of conventional single BCFL systems. Their approach incorporated a two-phase commit protocol to validate and authenticate block data across multiple Blockchains for Artificial Intelligence of Things in 6G. Furthermore, they utilized a mixed-precision local training strategy combined with flexible model update compression to improve communication efficiency without compromising accuracy. In the "Prepare"phase, the system establishes the groundwork by deploying model training and payment smart contracts on the source and destination parachains. The task publisher calls the training smart contract, sends a cross-chain request, and collaborates with validators and collators across parachains for legitimacy. Simultaneously, the payment smart contract activates to secure assets for worker rewards upon model training completion. Transitioning to the "Commit"phase, the trained model undergoes quality evaluation, triggering the training smart contract to generate a Simplified Payment Verification (SPV) proof and block header. Verified by the relay chain's validator group, they reach a consensus on the model training's legitimacy. Successful validation leads to worker compensation, with payment records logged in the payment chain. Discrepancies prompt a rollback, releasing locked assets. This two-phase process ensures the secure execution of cross-chain-enabled Federated Learning, managing complexities across interconnected Blockchains.

The prevailing BCFL system encounters data sparsity issues despite its commendable system efficiency. To tackle these concerns, Jin*et al.*[\[137\]](#page-41-10) introduced a cross-cluster Blockchain-enabled FL framework employing a cross-chain approach for the Internet of Medical Things. Their proposal includes the integration of two Blockchain consensus algorithms to facilitate secure model exchange across clusters using PBFT and a two-phase cross-chain consensus mechanism. Additionally, they advocate for model aggregation within each BCFL cluster and subsequent transmission to the other cluster, resulting in a remarkable enhancement of system efficiency and accuracy, with performance increased from 39.3% to 75.8%. This places a significant burden on computational and communication resources, so researchers suggested using it with edge computing instead of end devices. Kang*et al.*[\[138\]](#page-41-11) introduced a privacy framework that employed a hierarchical cross-chain structure for healthcare metaverses. The proposed system empowers users to safeguard sensitive data in the physical space and contribute non-sensitive data for metaverse tasks. Also, a data freshness-based incentive mechanism inspired by prospect theory [\[139\]](#page-41-12) is used for user-centric data sharing, and a pallier homomorphic encryption algorithm is used to provide security and privacy. Their approach achieved 93.71% accuracy in breast cancer prediction via vertical FL training.

Xu*et al.*[\[140\]](#page-41-13) present a hierarchical micro chained fabric, denoted as µDFL, designed for decentralized, Federated Learning across devices in edge networks. The microchain consensus protocol, built upon a partially decentralized Blockchain utilizing Proof-of-Credit (PoC), ensures the transparency and privacy of data sharing during local model training. The proposed µDFL introduces a hierarchical Internet of Things network fabric, incorporating lightweight microchains. Each microchain adopts a hybrid approach involving PoC block generation and a Voting-based Chain Finality consensus to enhance efficiency and privacy. The Federated structure of µDFL is achieved through an inter-chain network employing Byzantine Fault Tolerance. Validation through a proof-of-concept prototype demonstrates the effectiveness of µDFL in cross-device Federated Learning environments, emphasizing efficiency, security, and privacy.

## <span id="page-28-0"></span>9 Application of Blockchain-enabled FL for Privacy Preservation

In the following sections, we describe how several approaches leveraging FL and Blockchain for privacy preservation are used in different application scenarios, such as Healthcare, Industrial IoT (IIoT), and the Internet of Vehicles.

## 1 Healthcare

The analysis of health data using ML techniques can result in therapies and procedures with lower risks and better outcomes for patients, thus increasing the quality of care [\[141\]](#page-41-14). Healthcare data are usually spread across various sources such as hospitals, clinics, and wearable devices, which are characterized by highly sensitive information demanding to keep patients' data as private as possible. The decentralized nature of Blockchain technology and the ability of FL solutions to train models locally, while sharing only model parameters, has made the combination of the two approaches well-suited for healthcare. Moreover, Blockchain-based FL not only overcomes challenges associated with the outflow of confidential medical data efficiently but can*(i)*reward FL members for their contribution to the network*(ii)*monitor that the centralized FL server accurately aggregates the global model.

In this context, multiple IoT devices, including weight meters, blood pressure, glucose meters, insulin pumps, and others are connected to patients and aim at acquiring specific data they are meant to be gathered from the human body, such as temperature, heartbeat, electrocardiograph, and many others. These devices communicate data to smart systems such as smart monitors, laptops, and mobiles to be analyzed and visualized. The main goals of the different Blockchain-based FL approaches for healthcare can be summarized as follows [\[142\]](#page-41-15):

- management of medical records, also thanks to the cooperation between multiple hospitals/systems;
- tracking disease outbreak;
- enhanced monitoring of patients thanks to a wider amount of data to be analyzed;
- improving sensors' performance;
- pharmaceutical clinical trials.

In the system presented in [\[64\]](#page-37-16), IoT devices, before communicating with third-party components, send data to a Blockchain network for validation and, after this step, data is forwarded to other systems. Moreover, Blockchain provides large independent storage for healthcare data, recording usage behavior and ensuring authenticity. Multiple actors collaborate to provide a privacy-preserving solution, namely:*(i)*the sub-feature manager, which vertically partitions the aggregated data into different datasets;*(ii)*the different clients, which provide data to the federation manager and receives a sub-model for the training;*(iii)*the privacy broker, in charge of solving privacy issues;*(iv)*the integrity manager, which maintains the result integrity by avoiding errors inside sub-models.

The authors in [\[113\]](#page-40-6) proposed Blockchain architecture assumes the presence of numerous smart hospitals situated in diverse regions, each equipped with a cluster of IoT medical devices. These devices use edge servers for FL tasks with privacy-preserving verification via SMPC before aggregation. After verification, the local model is sent to the Blockchain for SMPC-based secure aggregation. Once a consensus is reached, the global model is stored in the Blockchain, and tamper-proof storage shares it with all FL round hospitals.

Also, the works presented in [\[143,](#page-41-16) [144\]](#page-41-17) are related to the Internet of Medical Things (IoMT) devices. In particular, [\[143\]](#page-41-16) proposes a Blockchain-enabled Federated Learning in the context of IoMT, with privacy-preservation and fraud detection characteristics. The solution is intended for healthcare applications in a fog-cloud-assisted network. The authors of [\[144\]](#page-41-17) introduce a real-time medical data processing multi-agent system that utilizes Blockchain for sharing and safeguarding private data.

Similarly to the previous approach, the architecture presented in [\[67\]](#page-38-0) considers multiple hospitals leveraging FL to keep their data private, thus sharing only weights and gradients. In this case, the aim is to recognize the presence of COVID-19 infection from lung Computed Tomography (CT, hereafter) scans. Each hospitals use Blockchain technology to distribute data, with each hospital storing an actual CT scan, and Blockchain facilitating the retrieval of the trained model. Privacy is ensured through encryption and the storage of unique identifiers for each hospital.

In the realm of COVID-19 diagnosis, [\[145\]](#page-41-18) introduces a Federated Blockchain-powered medical system, termed FedMedChain. The primary objective of this system is to distribute COVID-19 information and establish a collaborative diagnosis model while safeguarding the privacy of data owners.

In the paper presented in [\[146\]](#page-42-0), the authors propose a framework called Blockchain Vertical Federated Learning E-Medical Recommendation (BVFLEMR). It adopts a decentralized digital ledger system for Electronic Health Records (EHR) storage, LightGBM, and N-Gram models to recommend tailored treatments for the patients based on their EHR. In this way, it achieves private storage and management of patients' sensitive data in EHRs, such as diagnosis, treatment, medication, surgery, and diet specifications.

Privacy of EHRs is taken into account also by the authors of [\[105\]](#page-39-18), who propose a framework called CNN\_BC\_Cryp\_FL. It consists of*(i)*, a CNN-based secure classification component able to classify normal and abnormal users using the available dataset; *(ii)*a Blockchain-integrated cryptography-based FL used to restrict the accessibility of the database to abnormal users.

Several studies leverage Blockchain to incentivize participants to contribute their local data in training FL tasks [\[53,](#page-37-5) [147,](#page-42-1) [52\]](#page-37-4). In particular, the work presented in [\[53\]](#page-37-5) describes the system called ESB-FL that can train a model while protecting the privacy of local training data using a function encryption scheme called non-interactive designated decryptor function encryption (NDD-FE). It also integrates Blockchain to support the fair payment between the task publisher and all participants, thus guaranteeing that each participant gets a reward if the trained model satisfies the task requirements. Instead, the authors of [\[52\]](#page-37-4) aim to improve the fairness of the federated learned model and the trustworthiness of medical diagnostic image analyses to detect COVID-19.

Table [9](#page-30-0) shows the main differences among the papers analyzed in this section in terms of goal, type of involved devices, and type of healthcare data.

## 2 Industry 5.0

Industry 5.0 is a new concept that focuses on the cooperation between humans and machines to create sustainable industrial products and services. The main principles inspiring this innovative scenario, (namely, sustainability, humancenteredness, and resilience) are obtained thanks to the integration of digital technologies, the Industrial Internet of Things (IIoT, hereafter), artificial intelligence, and other advanced technologies into the manufacturing and industrial processes [\[148\]](#page-42-2). In this context, the combination of FL and Blockchain could provide powerful solutions for industries seeking to leverage data for innovation, while ensuring privacy, security, and efficiency.

In [\[119\]](#page-40-11), the authors present a framework called PPSS to protect privacy and defend against cyber attacks in the context of industry 4.0/5.0. PPSS includes two modules:*(i)*a Blockchain-enabled FL scheme, leveraging a differentially private training strategy, with an energy-efficient consensus protocol, named Proof-of-Federated Deep-Learning (PoFDL), and*(ii)*a privacy-preserving intrusion detection scheme using Convolutional Neural Networks for attack identification.

Similarly, [\[149\]](#page-42-3) proposes a Federated threat-hunting model in IIoT networks to identify anomalous behavior, while preserving the privacy of IIoT devices related to Blockchain-based smart factories.

The goal of the works proposed in [\[45,](#page-36-17) [92,](#page-39-5) [129\]](#page-41-2) is to design a secure data-sharing mechanism, that can share data among multiple distributed users while maintaining data privacy. In particular, the paper presented in [\[45\]](#page-36-17) integrates FL in the consensus process of a permissioned Blockchain, so that the computing work for consensus can also be used for Federated training tasks. Whereas, [\[92\]](#page-39-5) uses FL to obtain privacy-preserving model training, the InterPlanetary File

| Reference paper | Aim | Type of devices generat<br>ing data | Type of Data | |
|------------------------------------------------------|----------------------------------------------------------------|----------------------------------------------------------------------------------|----------------------------------------------------------------------|--|
| Singh et al.[64] | Private storage, Health alert | IoT sensors (weight me<br>ters, blood pressure, glu<br>cose meter, insulin pump) | Temperature,<br>heart<br>beat, blood pressure,<br>electrocardiograph | |
| Kalapaaking<br>et<br>al.[113], Polap et<br>al. [144] | Privacy-preserving<br>analysis<br>from<br>multiple hospitals | Internet<br>of<br>Medical<br>Things devices | Medical datasets | |
| Lakhan<br>et<br>al.[143] | Fraud analysis, and Data validation | Internet<br>of<br>Medical<br>Things (IoMT) devices | Medical datasets | |
| Kumar et al.[67] | Diagnosis of COVID-19 | CT device | Lung Computed To<br>mography scans | |
| Samuel<br>et<br>al.[145] | Privacy-preserving Diagnosis and<br>Dissemination of COVID-19 | Internet<br>of<br>Medical<br>Things (IoMT) devices | Medical datasets | |
| Hai et al.[146] | EHR Private storage, Recommenda<br>tion for tailored treatment | Manual data insertion | Electronic<br>Health<br>Records (EHR) | |
| Alzubi<br>er<br>al.<br>[105] | Abnormal users identification and<br>Database access | Manual data insertion | Electronic<br>Health<br>Records (EHR) | |
| Chen et al. [53] | Privacy-preserving image detection,<br>and incentive mechanism | Manual data insertion | Chest X-ray images | |
| Liu et al. [147] | Privacy-preserving image detection,<br>and incentive mechanism | Manual data insertion | Skin Cancer images | |
| Lo et al. [52] | Diagnosis of COVID-19, and incen<br>tive mechanism | Manual data insertion<br>X-rays images | | |

<span id="page-30-0"></span>**Table 9:** Healthcare Applications

System (IPFS) distributed storage system for storing model parameters and generating corresponding addresses based on the content, and Blockchain to provide the provenance and immutability of the parameters. Instead, the work of [\[129\]](#page-41-2) proposes a data protection aggregation scheme based on three ML methods (i.e., distributed K-means clustering based on differential privacy and homomorphic encryption, distributed random forest with differential privacy, and distributed AdaBoost with homomorphic encryption) to enable multiple data protection in IIoT scenarios.

Always in the context of secure data sharing, the paper described in [\[150\]](#page-42-4) tackles the problem of privacy-preserved credit data sharing. The combined credit data storage mechanism with a Deletable Bloom filter (DLBF) guarantees the traceability of the entire credit data sharing process in industrial applications. Moreover, they leverage homomorphic encryption, FL, and Blockchain to avoid data leakage. The paper presented in [\[151\]](#page-42-5) has a different goal. It focuses on preserving the privacy of the client data (e.g., usage frequency and time) adopting FL to train the models locally on the client to detect possible device failures in the network. Moreover, to resolve disputes between the central organization and client organizations about failure causes, the architecture leverages a combination of Blockchain and Merkle-tree to enable verifiable integrity of client data.

The authors of [\[152\]](#page-42-6) develop a framework for FL tasks to preserve privacy among various industrial departments. Decentralized secure storage is provided by the Distributed Hash Table (DHT) at the cloud layer of the proposed scheme, while the Blockchain network provides data authentication and validation.

Industry 5.0 is also expected to reshape the agriculture industry, as already done in the past, and promote the fourth agricultural revolution [\[153\]](#page-42-7). In this context, the authors of [\[154\]](#page-42-8) propose an intrusion detection system, called FELIDS, for securing agricultural-IoT infrastructures. It aims to protect data privacy through FL, employing three deep Learning classifiers, namely, Deep Neural Networks, Convolutional Neural Networks, and Recurrent Neural Networks against Agricultural IoT attacks. Moreover, Blockchain helps network members to track relevant information for supply chain management.

Table [10](#page-31-0) summarizes the main aim of the papers analyzed in this section.

| Reference paper | Main Aim |
|----------------------------------------------------------------|------------------------------------------------|
| Hamouda et al.[119] | Privacy-preserving FL, and Intrusion Detection |
| Yazdinejad et al.[149], Friha<br>et al. [154] | Privacy-preserving Anomalies Detection |
| Lu<br>et<br>al.[45],<br>Chen<br>et<br>al.[92], Jia et al.[129] | Privacy-preserving Data Sharing |
| Yang et al. [150] | Privacy-preserving Credit Data Sharing |
| Zang et al.[151] | Privacy-preserving Device Failure Detection |
| Singh et al.[152] | Privacy-preserving FL |


| **Table 10:** Industry 5.0 applications | | | | |
|-------------------------------------|--|--|--|--|
|-------------------------------------|--|--|--|--|

## 3 Internet of Vehicles

Internet of Vehicles (IoV, hereafter) defines the evolution of the conventional Vehicle Ad-hoc Networks and enables real-time information exchange among all the actors traveling through streets (e.g., vehicles, drivers, pedestrians) and road infrastructure through vehicle-to-everything (V2X) communication. The objective of IoV is to realize the convergence of mobile communication technology, intelligent transportation, and information systems [\[155,](#page-42-9) [156\]](#page-42-10). Because this scenario allows for quick and efficient exchange of large amounts of data containing private information (i.e. location and user preferences), approaches that rely on the combination of FL and Blockchain have been investigated. The arisen challenges are the following:

- strengthening privacy protection mechanisms;
- preventing hostile intelligent connected vehicles (ICVs) and edge servers from faking FL aggregate results with verification mechanisms;
- reducing the high communication overhead of FL.

The papers proposed in [\[157,](#page-42-11) [41,](#page-36-13) [98\]](#page-39-11) provide approaches for data sharing among vehicles for collaborative analysis to enhance service quality and driving experience. In particular, in [\[157\]](#page-42-11), a Blockchain-enabled and privacy-preserving FL framework called BV-ICVs is presented. In this system, smart contracts are used to prevent malicious ICVs from uploading unreliable, erroneous, or low-quality FL model updates. The authors of [\[41\]](#page-36-13) use FL to relieve transmission load and address privacy concerns of providers, and a hybrid Blockchain architecture, which consists of a permissioned Blockchain and a local Directed Acyclic Graph (DAG), executing a two-stage verification to obtain the reliability of shared data. The scheme illustrated in [\[98\]](#page-39-11), in addition to a Blockchain-based Privacy-preserving Federated Learning approach, also proposes a reputation-based model as an incentive mechanism to encourage users of IoV to participate in FL tasks actively.

The work presented in [\[79\]](#page-38-12) describes a framework for traffic flow prediction. To avoid using a centralized model coordinator, a consortium Blockchain-based FL framework is proposed to enable decentralized and secure FL. The model updates from distributed vehicles are verified by miners and stored on the Blockchain. Moreover, to preserve model privacy on the Blockchain, a differential privacy method with a noise-adding mechanism is used. Likewise, the system proposed in [\[158\]](#page-42-12) aims at removing the FL centralized global server and using a Blockchain to exchange local model updates from vehicles while providing and verifying their corresponding rewards.

The authors of [\[159\]](#page-42-13) focus on an approach to provide a hierarchical Blockchain-enabled FL algorithm for knowledge sharing in IoV. Moreover, they formulate a lightweight Proof-of-Knowledge (PoK) consensus mechanism to reduce the computation consumption. The works presented in [\[160,](#page-42-14) [161\]](#page-42-15) have the different goal of designing a cooperative intrusion detection mechanism that offloads the training model to IoV devices. [\[160\]](#page-42-14) distributes the FL computation to reduce the resource utilization of a central server while assuring security and privacy, and it relies on Blockchain to ensure the security of the aggregation model, store, and share the training models. Instead, [\[161\]](#page-42-15) uses Blockchain to store and share models from the previous steps in a smart contract and return the updated models to the vehicles.

An IoV-related application scenario is that of Drone Edge Intelligence, which refers to the ability of unmanned aerial vehicles (UAVs), or drones, to process and analyze data directly at the source or edge rather than relying on a centralized computing system. Drones' characteristics, such as line of sight, ease of deployment, and capture of high-resolution images, make them the efficient solution for disaster mitigation, security surveillance, environmental monitoring, and recovery [\[162\]](#page-42-16). FL allows drones to execute decentralized collaborative learning by computing local models. Only

| Reference paper | Main Aim |
|-----------------------------------------------------------|--------------------------------------------------------|
| Smahi et al.[157],<br>Lu et<br>al. [41], Wang et al. [98] | Privacy-preserving and verifiable FL |
| Qi et al.[79] | Privacy-preserving traffic flow prediction |
| Pokhrel et al.[158] | Privacy-preserving distributed FL |
| Chai et al.[159] | Privacy-preserving knowledge sharing |
| Liu et al.[160], Moulahi et<br>al.[161] | Privacy-preserving and cooperative intrusion detection |
| Akram et al.[164] | Privacy-preserving malicious drone detection |

## <span id="page-32-1"></span>Table 11: Internet of Vehicles applications

model parameters are shared with neighbors and the centralized unit to improve global model accuracy, while still keeping local data private. On the other hand, Blockchain can enable privacy-preserving data sharing in a distributed manner. However, combining the two solutions raises several challenges, such as scalability, energy efficiency, and transaction capacity [\[163\]](#page-42-18). The paper presented in [\[164\]](#page-42-17) relies on Blockchain technology and FL for privacy-preserving malicious node detection in the Internet of Drone Things (IoDTs).

Table [11](#page-32-1) summarizes the main aim of the paper analyzed in this section.

## <span id="page-32-0"></span>10 Open Issues and Future Directions

Integrating Blockchain technology into Federated Learning is a noteworthy research area, offering substantial improvements in protecting privacy models. As highlighted earlier, BCFL is crucial in supporting various domain applications. In this section, we address issues in BCFL and propose potential solutions to shed light on future research directions for readers and researchers in this evolving domain.

## 1 Open Issues

• Privacy Issues in BCFL: Preserving data privacy in BCFL involves a delicate balance between cryptographic tools and lightweight techniques. While private aggregation using cryptographic tools provides robust parameter privacy, it is computationally intensive and limited in arithmetic operations. On the other hand, noise perturbation methods, such as adding noise and gradient compression, offer a more lightweight approach but come with a trade-off between model performance and data privacy.

Current research predominantly emphasizes using HE to safeguard against inference attacks. However, a noteworthy drawback of HE is its limited computational efficiency and inability to handle large and complex operations efficiently. This limitation presents challenges in ensuring privacy for extensive and intricate datasets. Additionally, it is essential to note that HE does not inherently guard against collusion attacks, and this vulnerability remains a concern even when utilizing HE for privacy protection in data-intensive scenarios [\[165\]](#page-43-0).

Integrating SMPC in BCFL presents notable issues. Firstly, SMPC's interactive nature clashes with the noninteractive protocol required for secure aggregation in BCFL. Additionally, the susceptibility to collusion attacks poses a significant threat even when employing SMPC to protect the model, undermining the overall security and integrity of the FL process within the Blockchain environment. Addressing these issues is crucial for fortifying BCFL against collaboration threats and maintaining trust in the collaborative model training process. In BCFL, employing HE or SMC-based methods may prove impractical for large-scale scenarios due to the considerable increase in communication and computation expenses.

- Computation Overheads in BCFL: Researchers' incorporation of encryption methods aims to bolster privacy but comes with computational overhead as encrypted gradients are transmitted on the Blockchain. The size of local model gradients plays a role in determining the communication overhead. In addressing this, some studies employ gradient compression methods to reduce overhead, though this introduces potential issues such as removing pertinent information during compression. These compression-related challenges may have repercussions on the performance of the global model [\[166\]](#page-43-1).
- Gas consumption in HE based system: In [\[50\]](#page-37-2), an incentive mechanism has been introduced to the BCFL system, leveraging HE applied to local gradients to simultaneously provide rewards and preserve participant

privacy. However, the system faces a substantial hurdle, such as unexpectedly high gas consumption during PHE-related smart contract execution. The varying gas costs associated with encryption, additive, and decryption functions, with the additive operation incurring the highest cost, have emerged as a bottleneck, impacting both the economic feasibility and scalability of the BCFL system. These challenges underscore the pressing need to optimize gas consumption for PHE-related functions to ensure the continued effectiveness of the incentivization mechanism while maintaining privacy through HE.

### 2 Future Directions

The Federated Learning utilizing Blockchain technology offers numerous promising avenues for prospective research. We merely highlight specific directions for future investigations.

- Privacy Preserving Techniques: As a future research direction, explore the seamless integration of zeroknowledge proofs to bolster privacy within the Blockchain-enabled FL framework. This forward-looking methodology empowers participants to validate the accuracy of their updates without revealing the raw data, ensuring an elevated standard of confidentiality and privacy throughout the learning process. Moreover, it has the potential to substantially alleviate the verification burden on clients, thereby paving the way for more efficient and secure systems with enhanced privacy measures. Future research should focus on integrating zero-knowledge proofs in BCFL to enhance privacy, allowing participants to validate updates without revealing raw data. This approach not only ensures elevated confidentiality throughout the learning process but also has the potential to significantly reduce the verification burden on clients, paving the way for more efficient and secure systems with enhanced privacy measures.
- Gas Consumption Optimization: In the pursuit of advancing the BCFL system, a crucial area for exploration involves optimizing gas consumption for encryption-related smart contract functions. Currently, there is a notable absence of research addressing the reduction of gas consumption in the BCFL system, emphasizing privacy provision at a low cost. Investigating and implementing strategies to achieve low-cost and low gas consumption in the context of privacy-preserving BCFL operations represents a valuable and unexplored avenue for future research and system improvement.
- Addressing Vulnerabilities in Smart Contracts: For future directions in this area, it is crucial to prioritize research that delves explicitly into the vulnerabilities of smart contracts within BCFL. Given the inherent risks posed by faulty implementations, leading to persistent vulnerabilities and potential compromise of security and privacy in the model, a focused investigation is needed. Future efforts should aim to comprehensively identify and address these vulnerabilities, offering solutions to enhance the robustness of smart contracts in BCFL. This research would contribute to establishing a more secure foundation for the execution of logic and storage of final states in smart contracts, thereby mitigating risks associated with false data and bolstering overall security in BCFL models. Also, conduct a comprehensive security audit of the smart contract to identify and rectify system performance vulnerabilities.

## <span id="page-33-0"></span>11 Summary and Conclusions

Blockchain-enabled FL (BCFL) systems are emerging approaches that combine the principles of FL with Blockchain technology to address various challenges. The main objective of these solutions is to guarantee privacy, security, and trust in decentralized collaborative Learning environments while providing a trustworthy and transparent framework for participants. By adopting a privacy perspective, this survey paper presents a systematic overview of the fundamental concepts of BCFL architectures and explores the opportunities and challenges that arise from their development. This survey gives a novel contribution to the present literature because it analyzes in detail the existing attacks on privacy in BCFL, along with state-of-the-art solutions relying on differential privacy, homomorphic encryption, secure multiparty computation, reward-driven approaches, multiple methods, and cross-chained FL. Finally, we investigate the BCFL application in real-case scenarios, such as healthcare, Industry 5.0, and the Internet of Vehicles.

In summary, we analyzed 102 articles published in renowned international conferences, journals, symposiums, and workshops from 2018 to 2023 and focused on privacy aspects of Blockchain-enabled FL. Table [12](#page-34-4) represents a quantitative overview of the reviewed research papers divided into topics, whereas Figure [11](#page-34-5) pictures the analyzed number of articles published per year in the reference period.

The research direction explored in this paper can be regarded as a foundation, as we plan to continue our investigation by deep-diving into certain aspects only mentioned in the present work. For instance, a fascinating path can be the review of the paper exploiting existing security threats and countermeasures for BCFL systems to give the reader a

| Topic | Amount of papers |
|--------------------------------------------------------|------------------|
| BCFL Architecture | 16 |
| Attacks to privacy in BCFL | 2 |
| BCFL Architectures for Security and Privacy Protection | 14 |
| BCFL with Differential Privacy Approaches | 19 |
| BCFL with HE Approaches | 14 |
| BCFL with SMPC Approaches | 5 |
| BCFL with Reward-driven Approaches | 17 |
| BCFL with Hybrid Privacy Approaches | 9 |
| Cross-chained FL Approaches for privacy | 4 |
| Application of BCFL for privacy | 31 |

<span id="page-34-4"></span>**Table 12:** Amount of papers analyzed per topic

![](_page_34_Figure_3.jpeg)
<!-- Image Description: The image is a line graph showing the number of articles published each year from 2018 to 2023. The x-axis represents the year, and the y-axis represents the number of articles. The graph illustrates a growth in publications, peaking in 2022 (28 articles) before declining slightly in 2023 (20 articles). The purpose is to visually represent the publication trend over time within the paper's subject area. -->

<span id="page-34-5"></span>**Figure 11:** Literature timeline

larger spectrum of diverse problems in this domain. Moreover, an extensive and exhaustive technical description of all the implemented BCFL systems currently available is also a demanding task.

We sincerely aspire for this work to assist researchers and practitioners in comprehending the essential aspects of this field, capturing notable advancements, and highlighting future research progress.

## Acknowledgments

This work was supported in part by the project SERICS (PE00000014) under the NRRP MUR program funded by the EU-NGEU, and by the Italian Ministry of University and Research through the PRIN Project "HOMEY: a Humancentric IoE-based Framework for Supporting the Transition Towards Industry 5.0" (code 2022NX7WKE), and by the HORIZON Europe Framework Programme through the project "OPTIMA - Organization sPecific Threat Intelligence Mining and sharing" (101063107).

## References

- <span id="page-34-0"></span>[1] Youyang Qu, Md Palash Uddin, Chenquan Gan, Yong Xiang, Longxiang Gao, and John Yearwood. Blockchainenabled federated learning: A survey.*ACM Computing Surveys*, 55(4):1–35, 2022.
- <span id="page-34-1"></span>[2] Juncen Zhu, Jiannong Cao, Divya Saxena, Shan Jiang, and Houda Ferradi. Blockchain-empowered federated learning: Challenges, solutions, and future directions. *ACM Computing Surveys*, 55(11):1–31, 2023.
- <span id="page-34-2"></span>[3] Nakamoto S Bitcoin. Bitcoin: A peer-to-peer electronic cash system, 2008.
- <span id="page-34-3"></span>[4] Dun Li, Dezhi Han, Tien-Hsiung Weng, Zibin Zheng, Hongzhi Li, Han Liu, Arcangelo Castiglione, and Kuan-Ching Li. Blockchain for federated learning toward secure distributed machine learning systems: a systemic survey. *Soft Computing*, 26(9):4423–4440, 2022.

- <span id="page-35-0"></span>[5] Mansoor Ali, Hadis Karimipour, and Muhammad Tariq. Integration of blockchain and federated learning for internet of things: Recent advances and future challenges. *Computers & Security*, 108:102355, 2021.
- <span id="page-35-1"></span>[6] Dinh C Nguyen, Ming Ding, Quoc-Viet Pham, Pubudu N Pathirana, Long Bao Le, Aruna Seneviratne, Jun Li, Dusit Niyato, and H Vincent Poor. Federated learning meets blockchain in edge computing: Opportunities and challenges. *IEEE Internet of Things Journal*, 8(16):12806–12825, 2021.
- <span id="page-35-2"></span>[7] Wael Issa, Nour Moustafa, Benjamin Turnbull, Nasrin Sohrabi, and Zahir Tari. Blockchain-based federated learning for securing internet of things: A comprehensive survey. *ACM Computing Surveys*, 55(9):1–43, 2023.
- <span id="page-35-5"></span>[8] Attia Qammar, Ahmad Karim, Huansheng Ning, and Jianguo Ding. Securing federated learning with blockchain: a systematic literature review. *Artificial Intelligence Review*, 56(5):3951–3985, 2023.
- <span id="page-35-3"></span>[9] Junqin Huang, Linghe Kong, Guihai Chen, Qiao Xiang, Xi Chen, and Xue Liu. Blockchain-based federated learning: A systematic survey. *IEEE Network*, 2022.
- <span id="page-35-6"></span>[10] Dong Li, Zai Luo, and Bo Cao. Blockchain-based federated learning methodologies in smart environments. *Cluster Computing*, 25(4):2585–2599, 2022.
- <span id="page-35-4"></span>[11] Bipin Chhetri, Saroj Gopali, Rukayat Olapojoye, Samin Dehbashi, and Akbar Siami Namin. A survey on blockchain-based federated learning and data privacy. In *2023 IEEE 47th Annual Computers, Software, and Applications Conference (COMPSAC)*, pages 1311–1318. IEEE, 2023.
- <span id="page-35-7"></span>[12] Google. Google scholar. <https://scholar.google.com>, 2023.
- <span id="page-35-8"></span>[13] Elsevier. Scopus. <https://www.scopus.com>, 2023.
- <span id="page-35-9"></span>[14] Scimago Lab. Scimago. <https://www.scimagojr.com/>, 2023.
- <span id="page-35-10"></span>[15] Computing Research & Education. CORE Conference Portal. <https://portal.core.edu.au/conf-ranks>, 2023.
- <span id="page-35-11"></span>[16] Sawsan AbdulRahman, Hanine Tout, Hakima Ould-Slimane, Azzam Mourad, Chamseddine Talhi, and Mohsen Guizani. A survey on federated learning: The journey from centralized to distributed on-site learning and beyond. *IEEE Internet of Things Journal*, 8(7):5476–5497, 2020.
- <span id="page-35-12"></span>[17] Kyong Ho Lee and Naveen Verma. A low-power processor with configurable embedded machine-learning accelerators for high-order and adaptive analysis of medical-sensor signals. *IEEE Journal of Solid-State Circuits*, 48(7):1625–1637, 2013.
- <span id="page-35-13"></span>[18] Alberto Pacheco, Ever Flores, Raúl Sánchez, and Salvador Almanza-García. Smart classrooms aided by deep neural networks inference on mobile devices. In *2018 IEEE International Conference on Electro/Information Technology (EIT)*, pages 0605–0609. IEEE, 2018.
- <span id="page-35-14"></span>[19] Chen Zhang, Yu Xie, Hang Bai, Bin Yu, Weihong Li, and Yuan Gao. A survey on federated learning. *Knowledge-Based Systems*, 216:106775, 2021.
- <span id="page-35-15"></span>[20] Yong Cheng, Yang Liu, Tianjian Chen, and Qiang Yang. Federated learning for privacy-preserving ai. *Communications of the ACM*, 63(12):33–36, 2020.
- <span id="page-35-16"></span>[21] Hangyu Zhu, Jinjin Xu, Shiqing Liu, and Yaochu Jin. Federated learning on non-iid data: A survey. *Neurocomputing*, 465:371–390, 2021.
- <span id="page-35-17"></span>[22] Xiaodong Ma, Jia Zhu, Zhihao Lin, Shanxuan Chen, and Yangjie Qin. A state-of-the-art survey on solving non-iid data in federated learning. *Future Generation Computer Systems*, 135:244–258, 2022.
- <span id="page-35-18"></span>[23] Peter Kairouz, H Brendan McMahan, Brendan Avent, Aurélien Bellet, Mehdi Bennis, Arjun Nitin Bhagoji, Kallista Bonawitz, Zachary Charles, Graham Cormode, Rachel Cummings, et al. Advances and open problems in federated learning. *Foundations and Trends® in Machine Learning*, 14(1–2):1–210, 2021.
- <span id="page-35-19"></span>[24] Yang Zhao, Jun Zhao, Linshan Jiang, Rui Tan, Dusit Niyato, Zengxiang Li, Lingjuan Lyu, and Yingbo Liu. Privacy-preserving blockchain-based federated learning for iot devices. *IEEE Internet of Things Journal*, 8(3):1817–1829, 2020.
- <span id="page-35-20"></span>[25] Tian Li, Anit Kumar Sahu, Ameet Talwalkar, and Virginia Smith. Federated learning: Challenges, methods, and future directions. *IEEE signal processing magazine*, 37(3):50–60, 2020.
- <span id="page-35-21"></span>[26] Solmaz Niknam, Harpreet S Dhillon, and Jeffrey H Reed. Federated learning for wireless communications: Motivation, opportunities, and challenges. *IEEE Communications Magazine*, 58(6):46–51, 2020.
- <span id="page-35-22"></span>[27] Arjun Nitin Bhagoji, Supriyo Chakraborty, Prateek Mittal, and Seraphin Calo. Analyzing federated learning through an adversarial lens. In *International Conference on Machine Learning*, pages 634–643. PMLR, 2019.

- <span id="page-36-0"></span>[28] Shiqiang Wang, Tiffany Tuor, Theodoros Salonidis, Kin K Leung, Christian Makaya, Ting He, and Kevin Chan. Adaptive federated learning in resource constrained edge computing systems. *IEEE journal on selected areas in communications*, 37(6):1205–1221, 2019.
- <span id="page-36-1"></span>[29] Jiawen Kang, Zehui Xiong, Dusit Niyato, Shengli Xie, and Junshan Zhang. Incentive mechanism for reliable federated learning: A joint optimization approach to combining reputation and contract theory. *IEEE Internet of Things Journal*, 6(6):10700–10714, 2019.
- <span id="page-36-2"></span>[30] Jingwen Zhang, Yuezhou Wu, and Rong Pan. Incentive mechanism for horizontal federated learning based on reputation and reverse auction. In *Proceedings of the Web Conference 2021*, pages 947–956, 2021.
- <span id="page-36-3"></span>[31] Michael Nofer, Peter Gomber, Oliver Hinz, and Dirk Schiereck. Blockchain. *Business & Information Systems Engineering*, 59:183–187, 2017.
- <span id="page-36-4"></span>[32] Marianna Belotti, Nikola Božic, Guy Pujolle, and Stefano Secci. A vademecum on blockchain technologies: ´ When, which, and how. *IEEE Communications Surveys & Tutorials*, 21(4):3796–3838, 2019.
- <span id="page-36-5"></span>[33] Markus Jakobsson and Ari Juels. Proofs of work and bread pudding protocols. In *Secure Information Networks: Communications and Multimedia Security IFIP TC6/TC11 Joint Working Conference on Communications and Multimedia Security (CMS'99) September 20–21, 1999, Leuven, Belgium*, pages 258–272. Springer, 1999.
- <span id="page-36-6"></span>[34] Kristián Košt'ál, Tomáš Krupa, Martin Gembec, Igor Vereš, Michal Ries, and Ivan Kotuliak. On transition between pow and pos. In *2018 International Symposium ELMAR*, pages 207–210. IEEE, 2018.
- <span id="page-36-7"></span>[35] Vitalik Buterin et al. A next-generation smart contract and decentralized application platform. *white paper*, 3(37):2–1, 2014.
- <span id="page-36-8"></span>[36] Elli Androulaki, Artem Barger, Vita Bortnikov, Christian Cachin, Konstantinos Christidis, Angelo De Caro, David Enyeart, Christopher Ferris, Gennady Laventman, Yacov Manevich, et al. Hyperledger fabric: a distributed operating system for permissioned blockchains. In *Proceedings of the thirteenth EuroSys conference*, pages 1–15, 2018.
- <span id="page-36-9"></span>[37] Shafaq Naheed Khan, Faiza Loukil, Chirine Ghedira-Guegan, Elhadj Benkhelifa, and Anoud Bani-Hani. Blockchain smart contracts: Applications, challenges, and future trends. *Peer-to-peer Networking and Applications*, 14:2901–2925, 2021.
- <span id="page-36-10"></span>[38] Rebecca Yang, Ron Wakefield, Sainan Lyu, Sajani Jayasuriya, Fengling Han, Xun Yi, Xuechao Yang, Gayashan Amarasinghe, and Shiping Chen. Public and private blockchain in construction business process and information integration. *Automation in construction*, 118:103276, 2020.
- <span id="page-36-11"></span>[39] Purva Grover, Arpan Kumar Kar, and Marijn Janssen. Diffusion of blockchain technology: Insights from academic literature and social media analytics. *Journal of Enterprise Information Management*, 32(5):735–757, 2019.
- <span id="page-36-12"></span>[40] Christine V Helliar, Louise Crawford, Laura Rocca, Claudio Teodori, and Monica Veneziani. Permissionless and permissioned blockchain diffusion. *International Journal of Information Management*, 54:102136, 2020.
- <span id="page-36-13"></span>[41] Yunlong Lu, Xiaohong Huang, Ke Zhang, Sabita Maharjan, and Yan Zhang. Blockchain and federated learning for 5g beyond. *Ieee Network*, 35(1):219–225, 2020.
- <span id="page-36-14"></span>[42] Guangxia Xu, Zhaojian Zhou, Jingnan Dong, Lejun Zhang, and Xiaoling Song. A blockchain-based federated learning scheme for data sharing in industrial internet of things. *IEEE Internet of Things Journal*, 2023.
- <span id="page-36-15"></span>[43] Safa Otoum, Ismaeel Al Ridhawi, and Hussein T Mouftah. Blockchain-supported federated learning for trustworthy vehicular networks. In *GLOBECOM 2020-2020 IEEE Global Communications Conference*, pages 1–6. IEEE, 2020.
- <span id="page-36-16"></span>[44] Youyang Qu, Shiva Raj Pokhrel, Sahil Garg, Longxiang Gao, and Yong Xiang. A blockchained federated learning framework for cognitive computing in industry 4.0 networks. *IEEE Transactions on Industrial Informatics*, 17(4):2964–2973, 2020.
- <span id="page-36-17"></span>[45] Yunlong Lu, Xiaohong Huang, Yueyue Dai, Sabita Maharjan, and Yan Zhang. Blockchain and federated learning for privacy-preserved data sharing in industrial iot. *IEEE Transactions on Industrial Informatics*, 16(6):4177–4186, 2019.
- <span id="page-36-18"></span>[46] Sana Awan, Fengjun Li, Bo Luo, and Mei Liu. Poster: A reliable and accountable privacy-preserving federated learning framework using the blockchain. In *Proceedings of the 2019 ACM SIGSAC conference on computer and communications security*, pages 2561–2563, 2019.
- <span id="page-36-19"></span>[47] You Jun Kim and Choong Seon Hong. Blockchain-based node-aware dynamic weighting methods for improving federated learning performance. In *2019 20th Asia-pacific network operations and management symposium (APNOMS)*, pages 1–4. IEEE, 2019.

- <span id="page-37-0"></span>[48] Yuzheng Li, Chuan Chen, Nan Liu, Huawei Huang, Zibin Zheng, and Qiang Yan. A blockchain-based decentralized federated learning framework with committee consensus. *IEEE Network*, 35(1):234–241, 2020.
- <span id="page-37-1"></span>[49] Timon Rückel, Johannes Sedlmeir, and Peter Hofmann. Fairness, integrity, and privacy in a scalable blockchainbased federated learning system. *Computer Networks*, 202:108621, 2022.
- <span id="page-37-2"></span>[50] Minfeng Qi, Ziyuan Wang, Fan Wu, Rob Hanson, Shiping Chen, Yang Xiang, and Liming Zhu. A blockchainenabled federated learning model for privacy preservation: System design. In *Information Security and Privacy: 26th Australasian Conference, ACISP 2021, Virtual Event, December 1–3, 2021, Proceedings 26*, pages 473–489. Springer, 2021.
- <span id="page-37-3"></span>[51] Attia Qammar, Abdenacer Naouri, Jianguo Ding, and Huansheng Ning. Blockchain-based optimized edge node selection and privacy preserved framework for federated learning. *Cluster Computing*, pages 1–16, 2023.
- <span id="page-37-4"></span>[52] Sin Kit Lo, Yue Liu, Qinghua Lu, Chen Wang, Xiwei Xu, Hye-Young Paik, and Liming Zhu. Toward trustworthy ai: Blockchain-based architecture design for accountability and fairness of federated learning systems. *IEEE Internet of Things Journal*, 10(4):3276–3284, 2022.
- <span id="page-37-5"></span>[53] Biwen Chen, Honghong Zeng, Tao Xiang, Shangwei Guo, Tianwei Zhang, and Yang Liu. Esb-fl: Efficient and secure blockchain-based federated learning with fair payment. *IEEE Transactions on Big Data*, 2022.
- <span id="page-37-6"></span>[54] Dennis Lamken, Tobias Wagner, Tim Hoiss, Karl Seidenfad, Andreas Hermann, Mehmet Kus, and Ulrike Lechner. Design patterns and framework for blockchain integration in supply chains. In *2021 IEEE International Conference on Blockchain and Cryptocurrency (ICBC)*, pages 1–3. IEEE, 2021.
- <span id="page-37-7"></span>[55] Shuo Yuan, Bin Cao, Mugen Peng, and Yaohua Sun. Chainsfl: Blockchain-driven federated learning from design to realization. In *2021 IEEE Wireless Communications and Networking Conference (WCNC)*, pages 1–6. IEEE, 2021.
- <span id="page-37-8"></span>[56] Ying He, Ke Huang, Guangzheng Zhang, F Richard Yu, Jianyong Chen, and Jianqiang Li. Bift: A blockchainbased federated learning system for connected and autonomous vehicles. *IEEE Internet of Things Journal*, 9(14):12311–12322, 2021.
- <span id="page-37-9"></span>[57] Ligeng Zhu, Zhijian Liu, and Song Han. Deep leakage from gradients. *Advances in neural information processing systems*, 32, 2019.
- <span id="page-37-10"></span>[58] Luca Melis, Congzheng Song, Emiliano De Cristofaro, and Vitaly Shmatikov. Exploiting unintended feature leakage in collaborative learning. In *2019 IEEE symposium on security and privacy (SP)*, pages 691–706. IEEE, 2019.
- <span id="page-37-11"></span>[59] Zhibo Wang, Mengkai Song, Zhifei Zhang, Yang Song, Qian Wang, and Hairong Qi. Beyond inferring class representatives: User-level privacy leakage from federated learning. In *IEEE INFOCOM 2019-IEEE conference on computer communications*, pages 2512–2520. IEEE, 2019.
- <span id="page-37-12"></span>[60] Milad Nasr, Reza Shokri, and Amir Houmansadr. Comprehensive privacy analysis of deep learning: Passive and active white-box inference attacks against centralized and federated learning. In *2019 IEEE symposium on security and privacy (SP)*, pages 739–753. IEEE, 2019.
- <span id="page-37-13"></span>[61] Huilin Li, Yu Sun, Yong Yu, Dawei Li, Zhenyu Guan, and Jianwei Liu. Privacy-preserving cross-silo federated learning atop blockchain for iot. *IEEE Internet of Things Journal*, 2023.
- <span id="page-37-14"></span>[62] Meng Shen, Huan Wang, Bin Zhang, Liehuang Zhu, Ke Xu, Qi Li, and Xiaojiang Du. Exploiting unintended property leakage in blockchain-assisted federated learning for intelligent edge computing. *IEEE Internet of Things Journal*, 8(4):2265–2275, 2020.
- <span id="page-37-15"></span>[63] Youyang Qu, Longxiang Gao, Tom H Luan, Yong Xiang, Shui Yu, Bai Li, and Gavin Zheng. Decentralized privacy using blockchain-enabled federated learning in fog computing. *IEEE Internet of Things Journal*, 7(6):5171–5183, 2020.
- <span id="page-37-16"></span>[64] Saurabh Singh, Shailendra Rathore, Osama Alfarraj, Amr Tolba, and Byungun Yoon. A framework for privacypreservation of iot healthcare data using federated learning and blockchain technology. *Future Generation Computer Systems*, 129:380–388, 2022.
- <span id="page-37-17"></span>[65] Jianlong Xu, Jian Lin, Wei Liang, and Kuan-Ching Li. Privacy preserving personalized blockchain reliability prediction via federated learning in iot environments. *Cluster Computing*, 25(4):2515–2526, 2022.
- <span id="page-37-18"></span>[66] Yunlong Lu, Xiaohong Huang, Ke Zhang, Sabita Maharjan, and Yan Zhang. Low-latency federated learning and blockchain for edge association in digital twin empowered 6g networks. *IEEE Transactions on Industrial Informatics*, 17(7):5098–5107, 2020.

- <span id="page-38-0"></span>[67] Rajesh Kumar, Abdullah Aman Khan, Jay Kumar, Noorbakhsh Amiri Golilarz, Simin Zhang, Yang Ting, Chengyu Zheng, Wenyong Wang, et al. Blockchain-federated-learning and deep learning models for covid-19 detection using ct imaging. *IEEE Sensors Journal*, 21(14):16301–16314, 2021.
- <span id="page-38-1"></span>[68] Manisha Guduri, Chinmay Chakraborty, Martin Margala, et al. Blockchain-based federated learning technique for privacy preservation and security of smart electronic health records. *IEEE Transactions on Consumer Electronics*, 2023.
- <span id="page-38-2"></span>[69] Zonghang Li, Hongfang Yu, Tianyao Zhou, Long Luo, Mochan Fan, Zenglin Xu, and Gang Sun. Byzantine resistant secure blockchained federated learning at the edge. *Ieee Network*, 35(4):295–301, 2021.
- <span id="page-38-3"></span>[70] Harsh Kasyap and Somanath Tripathy. Privacy-preserving and byzantine-robust federated learning framework using permissioned blockchain. *Expert Systems with Applications*, page 122210, 2023.
- <span id="page-38-4"></span>[71] Seyed Mojtaba Hosseini Bamakan, Amirhossein Motavali, and Alireza Babaei Bondarti. A survey of blockchain consensus algorithms performance evaluation criteria. *Expert Systems with Applications*, 154:113385, 2020.
- <span id="page-38-5"></span>[72] Chenhao Xu, Youyang Qu, Tom H Luan, Peter W Eklund, Yong Xiang, and Longxiang Gao. An efficient and reliable asynchronous federated learning scheme for smart public transportation. *IEEE Transactions on Vehicular Technology*, 2022.
- <span id="page-38-6"></span>[73] Lei Feng, Yiqi Zhao, Shaoyong Guo, Xuesong Qiu, Wenjing Li, and Peng Yu. Bafl: A blockchain-based asynchronous federated learning framework. *IEEE Transactions on Computers*, 71(5):1092–1103, 2021.
- <span id="page-38-7"></span>[74] Mohanad Sarhan, Wai Weng Lo, Siamak Layeghy, and Marius Portmann. Hbfl: A hierarchical blockchain-based federated learning framework for collaborative iot intrusion detection. *Computers and Electrical Engineering*, 103:108379, 2022.
- <span id="page-38-8"></span>[75] Shaoyong Guo, Keqin Zhang, Bei Gong, Liandong Chen, Yinlin Ren, Feng Qi, and Xuesong Qiu. Sandbox computing: A data privacy trusted sharing paradigm via blockchain and federated learning. *IEEE Transactions on Computers*, 72(3):800–810, 2022.
- <span id="page-38-9"></span>[76] Zhanpeng Yang, Yuanming Shi, Yong Zhou, Zixin Wang, and Kai Yang. Trustworthy federated learning via blockchain. *IEEE Internet of Things Journal*, 10(1):92–109, 2022.
- <span id="page-38-10"></span>[77] Pathum Chamikara Mahawaga Arachchige, Peter Bertok, Ibrahim Khalil, Dongxi Liu, Seyit Camtepe, and Mohammed Atiquzzaman. Local differential privacy for deep learning. *IEEE Internet of Things Journal*, 7(7):5827–5842, 2019.
- <span id="page-38-11"></span>[78] Kang Wei, Jun Li, Ming Ding, Chuan Ma, Howard H Yang, Farhad Farokhi, Shi Jin, Tony QS Quek, and H Vincent Poor. Federated learning with differential privacy: Algorithms and performance analysis. *IEEE Transactions on Information Forensics and Security*, 15:3454–3469, 2020.
- <span id="page-38-12"></span>[79] Yuanhang Qi, M Shamim Hossain, Jiangtian Nie, and Xuandi Li. Privacy-preserving blockchain-based federated learning for traffic flow prediction. *Future Generation Computer Systems*, 117:328–337, 2021.
- <span id="page-38-13"></span>[80] Yuntao Wang, Zhou Su, Ning Zhang, and Abderrahim Benslimane. Learning in the air: Secure federated learning for uav-assisted crowdsensing. *IEEE Transactions on network science and engineering*, 8(2):1055–1069, 2020.
- <span id="page-38-14"></span>[81] Yichen Wan, Youyang Qu, Longxiang Gao, and Yong Xiang. Privacy-preserving blockchain-enabled federated learning for b5g-driven edge computing. *Computer Networks*, 204:108671, 2022.
- <span id="page-38-15"></span>[82] Youyang Qu, Longxiang Gao, Yong Xiang, Shigen Shen, and Shui Yu. Fedtwin: Blockchain-enabled adaptive asynchronous federated learning for digital twin networks. *IEEE Network*, 36(6):183–190, 2022.
- <span id="page-38-16"></span>[83] Lei Cui, Youyang Qu, Gang Xie, Deze Zeng, Ruidong Li, Shigen Shen, and Shui Yu. Security and privacyenhanced federated learning for anomaly detection in iot infrastructures. *IEEE Transactions on Industrial Informatics*, 18(5):3492–3500, 2021.
- <span id="page-38-17"></span>[84] Huiru Zhang, Guangshun Li, Yue Zhang, Keke Gai, and Meikang Qiu. Blockchain-based privacy-preserving medical data sharing scheme using federated learning. In *Knowledge Science, Engineering and Management: 14th International Conference, KSEM 2021, Tokyo, Japan, August 14–16, 2021, Proceedings, Part III 14*, pages 634–646. Springer, 2021.
- <span id="page-38-18"></span>[85] Laraib Javed, Adeel Anjum, Bello Musa Yakubu, Majid Iqbal, Syed Atif Moqurrab, and Gautam Srivastava. Sharechain: Blockchain-enabled model for sharing patient data using federated learning and differential privacy. *Expert Systems*, 40(5):e13131, 2023.
- <span id="page-38-19"></span>[86] Yuan Liu, Peng Liu, Weipeng Jing, and Houbing Herbert Song. Pd2s: A privacy-preserving differentiated data sharing scheme based on blockchain and federated learning. *IEEE Internet of Things Journal*, 2023.

- <span id="page-39-0"></span>[87] Jun Li, Yumeng Shao, Kang Wei, Ming Ding, Chuan Ma, Long Shi, Zhu Han, and H Vincent Poor. Blockchain assisted decentralized federated learning (blade-fl): Performance analysis and resource allocation. *IEEE Transactions on Parallel and Distributed Systems*, 33(10):2401–2415, 2021.
- <span id="page-39-1"></span>[88] Shan Ji, Jiale Zhang, Yongjing Zhang, Zhaoyang Han, and Chuan Ma. Lafed: A lightweight authentication mechanism for blockchain-enabled federated learning system. *Future Generation Computer Systems*, 145:56–67, 2023.
- <span id="page-39-2"></span>[89] Sara Salim, Benjamin Turnbull, and Nour Moustafa. A blockchain-enabled explainable federated learning for securing internet-of-things-based social media 3.0 networks. *IEEE Transactions on Computational Social Systems*, 2021.
- <span id="page-39-3"></span>[90] Qinyang Miao, Hui Lin, Jia Hu, and Xiaoding Wang. An intelligent and privacy-enhanced data sharing strategy for blockchain-empowered internet of things. *Digital Communications and Networks*, 8(5):636–643, 2022.
- <span id="page-39-4"></span>[91] Shuxin Zhang and Jinghua Zhu. Privacy protection federated learning framework based on blockchain and committee consensus in iot devices. In *2023 IEEE 47th Annual Computers, Software, and Applications Conference (COMPSAC)*, pages 627–636. IEEE, 2023.
- <span id="page-39-5"></span>[92] Junbao Chen, Jingfeng Xue, Yong Wang, Lu Huang, Thar Baker, and Zhixiong Zhou. Privacy-preserving and traceable federated learning for data sharing in industrial iot applications. *Expert Systems with Applications*, 213:119036, 2023.
- <span id="page-39-6"></span>[93] Pathum Chamikara Mahawaga Arachchige, Peter Bertok, Ibrahim Khalil, Dongxi Liu, Seyit Camtepe, and Mohammed Atiquzzaman. A trustworthy privacy preserving framework for machine learning in industrial iot systems. *IEEE Transactions on Industrial Informatics*, 16(9):6092–6102, 2020.
- <span id="page-39-7"></span>[94] Emmanuel Antwi-Boasiako, Shijie Zhou, Yongjian Liao, Qihe Liu, Yuyu Wang, and Kwabena Owusu-Agyemang. Privacy preservation in distributed deep learning: A survey on distributed deep learning, privacy preservation techniques used and interesting research directions. *Journal of Information Security and Applications*, 61:102949, 2021.
- <span id="page-39-8"></span>[95] Chengliang Zhang, Suyi Li, Junzhe Xia, Wei Wang, Feng Yan, and Yang Liu. {BatchCrypt}: Efficient homomorphic encryption for {Cross-Silo} federated learning. In *2020 USENIX annual technical conference (USENIX ATC 20)*, pages 493–506, 2020.
- <span id="page-39-9"></span>[96] Li Zhang, Jianbo Xu, Pandi Vijayakumar, Pradip Kumar Sharma, and Uttam Ghosh. Homomorphic encryptionbased privacy-preserving federated learning in iot-enabled healthcare system. *IEEE Transactions on Network Science and Engineering*, 2022.
- <span id="page-39-10"></span>[97] Yanru Chen, Jingpeng Li, Fan Wang, Kaifeng Yue, Yang Li, Bin Xing, Lei Zhang, and Liangyin Chen. Ds2pm: A data sharing privacy protection model based on blockchain and federated learning. *IEEE Internet of Things Journal*, 2021.
- <span id="page-39-11"></span>[98] Naiyu Wang, Wenti Yang, Xiaodong Wang, Longfei Wu, Zhitao Guan, Xiaojiang Du, and Mohsen Guizani. A blockchain based privacy-preserving federated learning scheme for internet of vehicles. *Digital Communications and Networks*, 2022.
- <span id="page-39-12"></span>[99] Jiasi Weng, Jian Weng, Jilian Zhang, Ming Li, Yue Zhang, and Weiqi Luo. Deepchain: Auditable and privacypreserving deep learning with blockchain-based incentive. *IEEE Transactions on Dependable and Secure Computing*, 18(5):2438–2455, 2019.
- <span id="page-39-13"></span>[100] Zhe Sun, Junping Wan, Lihua Yin, Zhiqiang Cao, Tianjie Luo, and Bin Wang. A blockchain-based audit approach for encrypted data in federated learning. *Digital Communications and Networks*, 8(5):614–624, 2022.
- <span id="page-39-14"></span>[101] Yinbin Miao, Ziteng Liu, Hongwei Li, Kim-Kwang Raymond Choo, and Robert H Deng. Privacy-preserving byzantine-robust federated learning via blockchain systems. *IEEE Transactions on Information Forensics and Security*, 17:2848–2861, 2022.
- <span id="page-39-15"></span>[102] Bora Bugra Sezer, Hasret Turkmen, and Urfat Nuriyev. Ppfchain: A novel framework privacy-preserving blockchain-based federated learning method for sensor networks. *Internet of Things*, 22:100781, 2023.
- <span id="page-39-16"></span>[103] Hangyu Zhu, Rui Wang, Yaochu Jin, Kaitai Liang, and Jianting Ning. Distributed additive encryption and quantization for privacy preserving federated deep learning. *Neurocomputing*, 463:309–327, 2021.
- <span id="page-39-17"></span>[104] Tasiu Muazu, Mao Yingchi, Abdullahi Uwaisu Muhammad, Muhammad Ibrahim, Omaji Samuel, and Prayag Tiwari. Iomt: A medical resource management system using edge empowered blockchain federated learning. *IEEE Transactions on Network and Service Management*, 2023.
- <span id="page-39-18"></span>[105] Jafar A Alzubi, Omar A Alzubi, Ashish Singh, and Manikandan Ramachandran. Cloud-iiot-based electronic health record privacy-preserving by cnn and blockchain-enabled federated learning. *IEEE Transactions on Industrial Informatics*, 19(1):1080–1087, 2022.

- <span id="page-40-0"></span>[106] Marco Arazzi, Serena Nicolazzo, and Antonino Nocera. A fully privacy-preserving solution for anomaly detection in iot using federated learning and homomorphic encryption. *Information Systems Frontiers*, pages 1–24, 2023.
- <span id="page-40-1"></span>[107] Yijing Li, Xiaofeng Tao, Xuefei Zhang, Junjie Liu, and Jin Xu. Privacy-preserved federated learning for autonomous driving. *IEEE Transactions on Intelligent Transportation Systems*, 23(7):8423–8434, 2021.
- <span id="page-40-9"></span>[108] Zhou Zhou, Youliang Tian, Jinbo Xiong, Jianfeng Ma, and Changgen Peng. Blockchain-enabled secure and trusted federated data sharing in iiot. *IEEE Transactions on Industrial Informatics*, 2022.
- <span id="page-40-2"></span>[109] Chuan Zhao, Shengnan Zhao, Minghao Zhao, Zhenxiang Chen, Chong-Zhi Gao, Hongwei Li, and Yu-an Tan. Secure multi-party computation: theory, practice and applications. *Information Sciences*, 476:357–372, 2019.
- <span id="page-40-3"></span>[110] Changsong Jiang, Chunxiang Xu, and Yuan Zhang. Pflm: Privacy-preserving federated learning with membership proof. *Information Sciences*, 576:288–311, 2021.
- <span id="page-40-4"></span>[111] Chen Fang, Yuanbo Guo, Jiali Ma, Haodong Xie, and Yifeng Wang. A privacy-preserving and verifiable federated learning method based on blockchain. *Computer Communications*, 186:1–11, 2022.
- <span id="page-40-5"></span>[112] Keith Bonawitz, Vladimir Ivanov, Ben Kreuter, Antonio Marcedone, H Brendan McMahan, Sarvar Patel, Daniel Ramage, Aaron Segal, and Karn Seth. Practical secure aggregation for privacy-preserving machine learning. In *proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security*, pages 1175–1191, 2017.
- <span id="page-40-6"></span>[113] Aditya Pribadi Kalapaaking, Ibrahim Khalil, and Xun Yi. Blockchain-based federated learning with smpc model verification against poisoning attack for healthcare systems. *IEEE Transactions on Emerging Topics in Computing*, 2023.
- <span id="page-40-7"></span>[114] Qianlong Wang, Yifan Guo, Xufei Wang, Tianxi Ji, Lixing Yu, and Pan Li. Ai at the edge: Blockchain-empowered secure multiparty learning with heterogeneous models. *IEEE Internet of Things Journal*, 7(10):9600–9610, 2020.
- <span id="page-40-8"></span>[115] Yufeng Zhan, Jie Zhang, Zicong Hong, Leijie Wu, Peng Li, and Song Guo. A survey of incentive mechanism design for federated learning. *IEEE Transactions on Emerging Topics in Computing*, 10(2):1035–1044, 2021.
- <span id="page-40-10"></span>[116] Jiahao Qi, Feilong Lin, Zhongyu Chen, Changbing Tang, Riheng Jia, and Minglu Li. High-quality model aggregation for blockchain-based federated learning via reputation-motivated task participation. *IEEE Internet of Things Journal*, 9(19):18378–18391, 2022.
- <span id="page-40-13"></span>[117] Mohamed Abdel-Basset, Nour Moustafa, and Hossam Hawash. Privacy-preserved cyberattack detection in industrial edge of things (ieot): a blockchain-orchestrated federated learning approach. *IEEE Transactions on Industrial Informatics*, 18(11):7920–7934, 2022.
- <span id="page-40-17"></span>[118] Kentaroh Toyoda and Allan N Zhang. Mechanism design for an incentive-aware blockchain-enabled federated learning platform. In *2019 IEEE international conference on big data (Big Data)*, pages 395–403. IEEE, 2019.
- <span id="page-40-11"></span>[119] Djallel Hamouda, Mohamed Amine Ferrag, Nadjette Benhamida, and Hamid Seridi. Ppss: A privacy-preserving secure framework using blockchain-enabled federated deep learning for industrial iots. *Pervasive and Mobile Computing*, 88:101738, 2022.
- <span id="page-40-12"></span>[120] Harsh Kasyap, Arpan Manna, and Somanath Tripathy. An efficient blockchain assisted reputation aware decentralized federated learning framework. *IEEE Transactions on Network and Service Management*, 2022.
- <span id="page-40-14"></span>[121] Zahra Batool, Kaiwen Zhang, and Matthew Toews. Fl-mab: client selection and monetization for blockchainbased federated learning. In *Proceedings of the 37th ACM/SIGAPP symposium on applied computing*, pages 299–307, 2022.
- <span id="page-40-15"></span>[122] Jiawen Kang, Rong Yu, Xumin Huang, Maoqiang Wu, Sabita Maharjan, Shengli Xie, and Yan Zhang. Blockchain for secure and efficient data sharing in vehicular edge computing and networks. *IEEE internet of things journal*, 6(3):4660–4670, 2018.
- <span id="page-40-16"></span>[123] Jiawen Kang, Zehui Xiong, Dusit Niyato, Yuze Zou, Yang Zhang, and Mohsen Guizani. Reliable federated learning for mobile networks. *IEEE Wireless Communications*, 27(2):72–80, 2020.
- <span id="page-40-18"></span>[124] Youyang Qu, Chenhao Xu, Longxiang Gao, Yong Xiang, and Shui Yu. Fl-sec: Privacy-preserving decentralized federated learning using signsgd for the internet of artificially intelligent things. *IEEE Internet of Things Magazine*, 5(1):85–90, 2022.
- <span id="page-40-19"></span>[125] Chaosheng Feng, Bin Liu, Keping Yu, Sotirios K Goudos, and Shaohua Wan. Blockchain-empowered decentralized horizontal federated learning for 5g-enabled uavs. *IEEE Transactions on Industrial Informatics*, 18(5):3582–3592, 2021.
- <span id="page-40-20"></span>[126] Xidi Qu, Shengling Wang, Qin Hu, and Xiuzhen Cheng. Proof of federated learning: A novel energy-recycling consensus algorithm. *IEEE Transactions on Parallel and Distributed Systems*, 32(8):2074–2085, 2021.

- <span id="page-41-0"></span>[127] Xudong Zhu and Hui Li. Privacy-preserving decentralized federated deep learning. In *Proceedings of the ACM Turing Award Celebration Conference-China*, pages 33–38, 2021.
- <span id="page-41-1"></span>[128] Muhammad Shayan, Clement Fung, Chris JM Yoon, and Ivan Beschastnikh. Biscotti: A blockchain system for private and secure federated learning. *IEEE Transactions on Parallel and Distributed Systems*, 32(7):1513–1525, 2020.
- <span id="page-41-2"></span>[129] Bin Jia, Xiaosong Zhang, Jiewen Liu, Yang Zhang, Ke Huang, and Yongquan Liang. Blockchain-enabled federated learning data protection aggregation scheme with differential privacy and homomorphic encryption in iiot. *IEEE Transactions on Industrial Informatics*, 18(6):4049–4058, 2021.
- <span id="page-41-3"></span>[130] Jin Sun, Ying Wu, Shangping Wang, Yixue Fu, and Xiao Chang. Permissioned blockchain frame for secure federated learning. *IEEE Communications Letters*, 26(1):13–17, 2021.
- <span id="page-41-4"></span>[131] Shuangjie Bai, Geng Yang, Guoxiu Liu, Hua Dai, and Chunming Rong. Nttpfl: Privacy-preserving oriented no trusted third party federated learning system based on blockchain. *IEEE Transactions on Network and Service Management*, 19(4):3750–3763, 2022.
- <span id="page-41-5"></span>[132] Enrique Tomás Martínez Beltrán, Mario Quiles Pérez, Pedro Miguel Sánchez Sánchez, Sergio López Bernal, Gérôme Bovet, Manuel Gil Pérez, Gregorio Martínez Pérez, and Alberto Huertas Celdrán. Decentralized federated learning: Fundamentals, state of the art, frameworks, trends, and challenges. *IEEE Communications Surveys & Tutorials*, 2023.
- <span id="page-41-6"></span>[133] Ahmed Imteaj, Urmish Thakker, Shiqiang Wang, Jian Li, and M Hadi Amini. A survey on federated learning for resource-constrained iot devices. *IEEE Internet of Things Journal*, 9(1):1–24, 2021.
- <span id="page-41-7"></span>[134] Umer Majeed and Choong Seon Hong. Flchain: Federated learning via mec-enabled blockchain network. In *2019 20th Asia-Pacific Network Operations and Management Symposium (APNOMS)*, pages 1–4. IEEE, 2019.
- <span id="page-41-8"></span>[135] Xiantao Jiang, F Richard Yu, Tian Song, Zhaowei Ma, Yanxing Song, and Daqi Zhu. Blockchain-enabled cross-domain object detection for autonomous driving: A model sharing approach. *IEEE Internet of Things Journal*, 7(5):3681–3692, 2020.
- <span id="page-41-9"></span>[136] Jiawen Kang, Xuandi Li, Jiangtian Nie, Yi Liu, Minrui Xu, Zehui Xiong, Dusit Niyato, and Qiang Yan. Communication-efficient and cross-chain empowered federated learning for artificial intelligence of things. *IEEE Transactions on Network Science and Engineering*, 9(5):2966–2977, 2022.
- <span id="page-41-10"></span>[137] Hai Jin, Xiaohai Dai, Jiang Xiao, Baochun Li, Huichuwu Li, and Yan Zhang. Cross-cluster federated learning and blockchain for internet of medical things. *IEEE Internet of Things Journal*, 8(21):15776–15784, 2021.
- <span id="page-41-11"></span>[138] Jiawen Kang, Jinbo Wen, Dongdong Ye, Bingkun Lai, Tianhao Wu, Zehui Xiong, Jiangtian Nie, Dusit Niyato, Yang Zhang, and Shengli Xie. Blockchain-empowered federated learning for healthcare metaverses: Usercentric incentive mechanism with optimal data freshness. *IEEE Transactions on Cognitive Communications and Networking*, 2023.
- <span id="page-41-12"></span>[139] Daniel Kahneman and Amos Tversky. Prospect theory: An analysis of decision under risk. In *Handbook of the fundamentals of financial decision making: Part I*, pages 99–127. World Scientific, 2013.
- <span id="page-41-13"></span>[140] Ronghua Xu and Yu Chen. µdfl: A secure microchained decentralized federated learning fabric atop iot networks. *IEEE Transactions on Network and Service Management*, 19(3):2677–2688, 2022.
- <span id="page-41-14"></span>[141] Rodolfo Stoffel Antunes, Cristiano André da Costa, Arne Küderle, Imrana Abdullahi Yari, and Björn Eskofier. Federated learning for healthcare: Systematic review and architecture proposal. *ACM Transactions on Intelligent Systems and Technology (TIST)*, 13(4):1–23, 2022.
- <span id="page-41-15"></span>[142] Raushan Myrzashova, Saeed Hamood Alsamhi, Alexey V Shvetsov, Ammar Hawbani, and Xi Wei. Blockchain meets federated learning in healthcare: A systematic review with challenges and opportunities. *IEEE Internet of Things Journal*, 2023.
- <span id="page-41-16"></span>[143] Abdullah Lakhan, Mazin Abed Mohammed, Jan Nedoma, Radek Martinek, Prayag Tiwari, Ankit Vidyarthi, Ahmed Alkhayyat, and Weiyu Wang. Federated-learning based privacy preservation and fraud-enabled blockchain iomt system for healthcare. *IEEE journal of biomedical and health informatics*, 27(2):664–672, 2022.
- <span id="page-41-17"></span>[144] Dawid Połap, Gautam Srivastava, and Keping Yu. Agent architecture of an intelligent medical system based on federated learning and blockchain technology. *Journal of Information Security and Applications*, 58:102748, 2021.
- <span id="page-41-18"></span>[145] Omaji Samuel, Akogwu Blessing Omojo, Abdulkarim Musa Onuja, Yunisa Sunday, Prayag Tiwari, Deepak Gupta, Ghulam Hafeez, Adamu Sani Yahaya, Oluwaseun Jumoke Fatoba, and Shahab Shamshirband. Iomt: A covid-19 healthcare system driven by federated learning and blockchain. *IEEE Journal of Biomedical and Health Informatics*, 27(2):823–834, 2022.

- <span id="page-42-0"></span>[146] Tao Hai, Jincheng Zhou, SR Srividhya, Sanjiv Kumar Jain, Praise Young, and Shweta Agrawal. Bvflemr: an integrated federated learning and blockchain technology for cloud-based medical records recommendation system. *Journal of Cloud Computing*, 11(1):22, 2022.
- <span id="page-42-1"></span>[147] Yuan Liu, Wangyuan Yu, Zhengpeng Ai, Guangxia Xu, Liang Zhao, and Zhihong Tian. A blockchain-empowered federated learning in healthcare-based cyber physical systems. *IEEE Transactions on Network Science and Engineering*, 2022.
- <span id="page-42-2"></span>[148] Jiewu Leng, Weinan Sha, Baicun Wang, Pai Zheng, Cunbo Zhuang, Qiang Liu, Thorsten Wuest, Dimitris Mourtzis, and Lihui Wang. Industry 5.0: Prospect and retrospect. *Journal of Manufacturing Systems*, 65:279– 295, 2022.
- <span id="page-42-3"></span>[149] Abbas Yazdinejad, Ali Dehghantanha, Reza M Parizi, Mohammad Hammoudeh, Hadis Karimipour, and Gautam Srivastava. Block hunter: Federated learning for cyber threat hunting in blockchain-based iiot networks. *IEEE Transactions on Industrial Informatics*, 18(11):8356–8366, 2022.
- <span id="page-42-4"></span>[150] Fan Yang, Yanan Qiao, Mohammad Zoynul Abedin, and Cheng Huang. Privacy-preserved credit data sharing integrating blockchain and federated learning for industrial 4.0. *IEEE Transactions on Industrial Informatics*, 18(12):8755–8764, 2022.
- <span id="page-42-5"></span>[151] Weishan Zhang, Qinghua Lu, Qiuyu Yu, Zhaotong Li, Yue Liu, Sin Kit Lo, Shiping Chen, Xiwei Xu, and Liming Zhu. Blockchain-based federated learning for device failure detection in industrial iot. *IEEE Internet of Things Journal*, 8(7):5926–5937, 2020.
- <span id="page-42-6"></span>[152] Sushil Kumar Singh, Laurence T Yang, and Jong Hyuk Park. Fusionfedblock: Fusion of blockchain and federated learning to preserve privacy in industry 5.0. *Information Fusion*, 90:233–240, 2023.
- <span id="page-42-7"></span>[153] Ye Liu, Xiaoyuan Ma, Lei Shu, Gerhard Petrus Hancke, and Adnan M Abu-Mahfouz. From industry 4.0 to agriculture 4.0: Current status, enabling technologies, and research challenges. *IEEE Transactions on Industrial Informatics*, 17(6):4322–4334, 2020.
- <span id="page-42-8"></span>[154] Othmane Friha, Mohamed Amine Ferrag, Lei Shu, Leandros Maglaras, Kim-Kwang Raymond Choo, and Mehdi Nafaa. Felids: Federated learning-based intrusion detection system for agricultural internet of things. *Journal of Parallel and Distributed Computing*, 165:17–31, 2022.
- <span id="page-42-9"></span>[155] Fangchun Yang, Shangguang Wang, Jinglin Li, Zhihan Liu, and Qibo Sun. An overview of internet of vehicles. *China communications*, 11(10):1–15, 2014.
- <span id="page-42-10"></span>[156] Omprakash Kaiwartya, Abdul Hanan Abdullah, Yue Cao, Ayman Altameem, Mukesh Prasad, Chin-Teng Lin, and Xiulei Liu. Internet of vehicles: Motivation, layered architecture, network model, challenges, and future aspects. *IEEE access*, 4:5356–5373, 2016.
- <span id="page-42-11"></span>[157] Abla Smahi, Hui Li, Yong Yang, Xin Yang, Ping Lu, Yong Zhong, and Caifu Liu. Bv-icvs: A privacy-preserving and verifiable federated learning framework for v2x environments using blockchain and zksnarks. *Journal of King Saud University-Computer and Information Sciences*, page 101542, 2023.
- <span id="page-42-12"></span>[158] Shiva Raj Pokhrel and Jinho Choi. Federated learning with blockchain for autonomous vehicles: Analysis and design challenges. *IEEE Transactions on Communications*, 68(8):4734–4746, 2020.
- <span id="page-42-13"></span>[159] Haoye Chai, Supeng Leng, Yijin Chen, and Ke Zhang. A hierarchical blockchain-enabled federated learning algorithm for knowledge sharing in internet of vehicles. *IEEE Transactions on Intelligent Transportation Systems*, 22(7):3975–3986, 2020.
- <span id="page-42-14"></span>[160] Hong Liu, Shuaipeng Zhang, Pengfei Zhang, Xinqiang Zhou, Xuebin Shao, Geguang Pu, and Yan Zhang. Blockchain and federated learning for collaborative intrusion detection in vehicular edge computing. *IEEE Transactions on Vehicular Technology*, 70(6):6073–6084, 2021.
- <span id="page-42-15"></span>[161] Tarek Moulahi, Rateb Jabbar, Abdulatif Alabdulatif, Sidra Abbas, Salim El Khediri, Salah Zidi, and Muhammad Rizwan. Privacy-preserving federated learning cyber-threat detection for intelligent transport systems with blockchain-based security. *Expert Systems*, 40(5):e13103, 2023.
- <span id="page-42-16"></span>[162] Saeed Hamood Alsamhi, Faris A Almalki, Hatem Al-Dois, Alexey V Shvetsov, Mohammad Samar Ansari, Ammar Hawbani, Sachin Kumar Gupta, and Brian Lee. Multi-drone edge intelligence and sar smart wearable devices for emergency communication. *Wireless Communications and Mobile Computing*, 2021:1–12, 2021.
- <span id="page-42-18"></span>[163] Saeed Hamood Alsamhi, Faris A Almalki, Fatemeh Afghah, Ammar Hawbani, Alexey V Shvetsov, Brian Lee, and Houbing Song. Drones' edge intelligence over smart environments in b5g: Blockchain and federated learning synergy. *IEEE Transactions on Green Communications and Networking*, 6(1):295–312, 2021.
- <span id="page-42-17"></span>[164] Junaid Akram, Muhammad Umair, Rutvij H Jhaveri, Muhammad Naveed Riaz, Haoran Chi, and Sharaf Malebary. Chained-drones: Blockchain-based privacy-preserving framework for secure and intelligent service provisioning in internet of drone things. *Computers and Electrical Engineering*, 110:108772, 2023.

- <span id="page-43-0"></span>[165] Meng Hao, Hongwei Li, Xizhao Luo, Guowen Xu, Haomiao Yang, and Sen Liu. Efficient and privacy-enhanced federated learning for industrial artificial intelligence. *IEEE Transactions on Industrial Informatics*, 16(10):6532– 6542, 2019.
- <span id="page-43-1"></span>[166] Laizhong Cui, Xiaoxin Su, Zhongxing Ming, Ziteng Chen, Shu Yang, Yipeng Zhou, and Wei Xiao. Creat: Blockchain-assisted compression algorithm of federated learning for content caching in edge computing. *IEEE Internet of Things Journal*, 9(16):14151–14161, 2020.
