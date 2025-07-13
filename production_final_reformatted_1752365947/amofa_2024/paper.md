---
cite_key: amofa_2024
title: Blockchain-secure patient Digital Twin in healthcare using smart contracts
authors: Sandro Amofa, Qi Xia, Hu Xia, Isaac Amankona Obiri, Bonsu Adjei-Arthur, Jingcong Yang, Jianbin Gao
year: 2024
doi: 10.1371/journal.pone.0286120
url: https://doi.org/10.1371/journal.pone.0286120
relevancy: High
relevancy_justification: Directly addresses HDM/PKG concepts with focus on personal data management
tags: 
date_processed: 2025-07-02
phase2_processed: true
original_folder: plos_blockchain_dt
images_total: 15
images_kept: 14
images_removed: 1
keywords: 
---

# OPEN ACCESS

**Citation:** Amofa S, Xia Q, Xia H, Obiri IA, Adjei-Arthur B, Yang J, et al. (2024) Blockchain-secure patient Digital Twin in healthcare using smart contracts. PLoS ONE 19(2): e0286120. [https://doi.org/10.1371/journal.pone.0286120](https://doi.org/10.1371/journal.pone.0286120)
**Editor:** Omar A. Alzubi, Al-Balqa Applied University Prince Abdullah bin Ghazi Faculty of Information Technology, JORDAN
**Received:** January 4, 2023
**Accepted:** April 25, 2023
**Published:** February 29, 2024
**Copyright:** © 2024 Amofa et al. This is an open access article distributed under the terms of the Creative Commons [Attribution](http://creativecommons.org/licenses/by/4.0/) License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original author and source are credited.
**Data Availability Statement:** We do not know of specific legal reasons to completely bar us from sharing data with other researchers for the purposes of scientific inquiry. However, in all our research we are guided by healthcare privacy regulations HIPAA, HITECH, and others as they apply so as to avoid legal challenges altogether. The dataset can be made available on request. To place a request, please send an email to that effect to [202124080119@std.uestc.edu.cn](mailto:202124080119@std.uestc.edu.cn), Graduate Student Researcher: He is the Curator for this research.

RESEARCH ARTICLE

## Blockchain-secure patient Digital Twin in healthcare using smart contracts

## Sandro Amofa, Qi Xia, Hu Xia, Isaac Amankona Obiri, Bonsu Adjei-Arthur, Jingcong Yang, Jianbin Gao

School of Computer Science and Engineering, University of Electronic Science and Technology of China, Chengdu, China

* gaojb@uestc.edu.cn

## Abstract

Modern healthcare has a sharp focus on data aggregation and processing technologies. Consequently, from a data perspective, a patient may be regarded as a timestamped list of medical conditions and their corresponding corrective interventions. Technologies to securely aggregate and access data for individual patients in the quest for precision medicine have led to the adoption of Digital Twins in healthcare. Digital Twins are used in manufacturing and engineering to produce digital models of physical objects that capture the essence of device operation to enable and drive optimization. Thus, a patient's Digital Twin can significantly improve health data sharing. However, creating the Digital Twin from multiple data sources, such as the patient's electronic medical records (EMR) and personal health records (PHR) from wearable devices, presents some risks to the security of the model and the patient. The constituent data for the Digital Twin should be accessible only with permission from relevant entities and thus requires authentication, privacy, and provable provenance. This paper proposes a blockchain-secure patient Digital Twin that relies on smart contracts to automate the updating and communication processes that maintain the Digital Twin. The smart contracts govern the response the Digital Twin provides when queried, based on policies created for each patient. We highlight four research points: access control, interaction, privacy, and security of the Digital Twin and we evaluate the Digital Twin in terms of latency in the network, smart contract execution times, and data storage costs.

## 1 Introduction

A Digital Twin is a data-driven model of a physical asset, process, or system [[1]](#ref-1) with a persistent data connection between the physical object and model. This enables sensory data from the physical object to create increasingly detailed virtual models that reveal detective, preventative, or corrective insights for optimized operations [[2]](#ref-2). There are several benefits to Digital Twins and the barrier to their creation is getting lower by the day due to the availability of digital tools for data collection and analytics, increasing computing power, and diminishing costs of cloud data storage.

Digital Twins are used in manufacturing for quality control and optimization purposes [[3]](#ref-3) where they permit virtual objects to be created and tested by subjecting them to exploitative,

**Funding:** This research was funded by the Basic Strengthening Program (2021- JCJQ-JJ-0463), the scientific and technological innovation talents of Sichuan Province (2023JDRC0001), the National Natural Science Foundation of China (No. U22B2029), Shenzhen Research Program (No. JSGG20210802153537009).
**Competing interests:** The authors of the article declare that there are no competing interests.

destructive experiments which may not be permitted in the physical world due to prohibitive financial costs, ethical or legal implications, etc. [[4]](#ref-4). Thus, the application of Digital Twin technology to healthcare can bring many benefits, as experiments can be performed on data models to determine optimal treatments before prescribing them to the patient. Using available patient electronic medical records, data from smart devices, computing power, and analytics algorithms, a Digital Twin can be created for the patient, as shown in Fig 1. With more data, better approximations of the patient Digital Twin can be produced and queried to provide better access to healthcare at reduced costs and enable a higher quality of life for patients.

However, Digital Twins raise difficult questions regarding security and privacy [[5]](#ref-5). The data connection between the patient and the Digital Twin creates the computational model of the patient's condition(s). Inevitably, without adequate security, inaccurate data input to the Digital Twin can have serious consequences for the patient since his/her treatment may be based on the output the Digital Twin demonstrates. Additionally, unauthorized access to the Digital Twin can reveal compromising details about the patient that may cause long-term damage to their reputation with adverse financial consequences. Hence, it is critical to demand guarantees on the security of the Digital Twin and also to restrict the information it provides when queried. This research proposes a mechanism to handle four key research points: access control, interaction, privacy, and security of the Digital Twin. The need for secure data, reliable storage, trusted computing and other cooperative mechanisms with mutually beneficial interactions can be addressed using the blockchain [[6]](#ref-6)–[[9]](#ref-9) where a network of institutions and users collaborate to share data, collectively confer consensus-based validity on transactions, and

![Image Description: The figure depicts a blockchain-like structure illustrating Digital Twin instances from multiple data sources. Document icons represent data sources sequentially feeding into blocks. Each block contains a "PrevHash," "Nonce," and multiple transactions. Blocks are linked, showing the chaining of data through "PrevHash," illustrating a sequential data flow and potentially indicating a distributed ledger system.](_page_1_Figure_7.jpeg)

<https://doi.org/10.1371/journal.pone.0286120.g001>

maintain a single coherent transactions history. Provenance of data and transactions can also be guaranteed since the blockchain provides rigorous mechanisms for data integrity using digital signatures and cryptographic hashes with timestamps [[10]](#ref-10). Periodic updates are critical for Digital Twins, thus it is important to set limits on the data the Digital Twin can receive or provide when queried. Hence, we propose a blockchain-based Digital Twin that can model the individual patient's condition(s) and facilitate care by accessing specific services. We employ a suite of smart contracts to mediate access to the data stores from which the Digital Twin is updated.

### 1.1 Contribution

We outline our main contribution to the use of Digital Twins in healthcare below:

- 1. We present an automated, blockchain-based patient Digital Twin that uses smart contracts to mediate access to the Digital Twin and control its interactions.
- 2. We present a mathematical model of the patient Digital Twin defining it with a focus on timestamped instances.
- 3. We present a novel Multi-receiver Identity-Based Signcryption (mIBSC) scheme to secure the patient Digital Twin which has a constant ciphertext size and an element that can be stored on the blockchain to prove the authorship of digital twin.

The remainder of the paper is organized as follows: Section 2 presents Related Works while Section 3 provides Preliminaries dealing with the Blockchain, Digital Twins and cryptographic assumptions. Section 4 deals with the System Overview and component interactions. Section 5 discusses System Design and Section 6 presents Security proofs for our research. Section 7 provides the Efficiency Evaluation of the computations implemented and some metrics. Section 8 concludes the research and offers directions for future works.

### 2 Related works

In this section we review Digital Twins usage in healthcare with a focus on secure patient data sharing using smart contracts. In [[11]](#ref-11), the authors continuously monitor patients' conditions and improve patient outcomes, quality of life and reduce financial costs by using Digital Twin technology for healthcare. According to this research, health monitoring can be achieved using wearable sensors for early detection of worsening health or manage chronic conditions. Furthermore, assistive technologies and increasing usage of real-time data can enable new and dynamic health services with minimal risk for the patient. The research also proposes fast simulations of conditions using machine learning for accurate crisis prediction. Thus, doctors can use the patient's Digital Twin as a planning tool for intelligent control and emergency response. In [[12]](#ref-12), the authors define questions surrounding the materialisation, expectation and the implementation of Digital Twins in healthcare. They conclude Digital Twins can provide a useful test platform for enabling preventive healthcare for patients through simulations that employ trial-and-error so that consequences of given treatments can be evaluated empirically before the actual treatment is administered to patients. This provides a cost-effective implementation of precision medicine that offers patients the possibility of personalized treatments. For [[13]](#ref-13), the researchers tackle the integration of Digital Twins with agents and multi-agent systems. They focused on the design of agent-based Digital Twins and their utility in the context of healthcare management. They highlight the importance of Digital Twins using a case study where contextual Digital Twins of a trauma victim alert emergency medical staff in a hospital with vital details about the incoming

patient. The authors of A Blockchain-based Secure Digital Twin Framework for Smart Healthy City propose a Digital Twin framework that consists of three layers: a Device Layer, a Blockchain Layer and an Application Layer. They discuss the application of their framework to the COVID-19 pandemic and highlight its suitability for use with other future public health emergencies. It provided a sequence diagram that shows how two Digital Twins and a hospital could collaborate to exchange public keys necessary for notification in case of confirmed infection. However, they do not provide proof for encryption and other security-related algorithms necessary to protect a Digital Twin [[14]](#ref-14). This article [[15]](#ref-15) is concerned with the lack of a data collection mechanism that adequately addresses the challenge of fusing data from multiple disparate sources. The research then describes a concrete computational model of a Digital Twin for healthcare, proposes a Healthcare Digital Twin (HDT) system, and defines the protocol progression for the framework that corresponds to the mathematical model. Being a conceptual model, it provides no experimental results for any of the interactions of the Digital Twins.

We considered [[16]](#ref-16)–[[19]](#ref-19) for their insights on coupling Digital Twins with blockchain technology. While we appreciate their views, they do not apply to healthcare or patients. The literature agrees that the security of the Digital Twin is essential. Still, there are few proposals on guaranteeing the patient Digital Twin's privacy and security. Thus, our research uses smart contracts to mediate access to and control of the patient's Digital Twin.

### 2.1 Broadcast encryption

Fiat and Naor first introduced the concept of broadcast encryption (BE) or multi-receivers encryption in [[20]](#ref-20). They proposed a method for securely encrypting a message for a group of users so that only those in the group could decrypt it. On the other hand, a coalition of non-set users cannot obtain any information about the broadcast message. Many BE methods have been developed in the contexts of identity-based encryption [[21]](#ref-21)–[[23]](#ref-23) and standard public-key encryption [[24]](#ref-24). Delerable´e [[21]](#ref-21) introduced the first identity-based broadcast encryption (IBBE) system with constant-size ciphertexts and private keys in the identity-based encryption context. The approach, however, does not provide ciphertext authentication. The properties of authentication and secrecy are both necessary for sharing sensitive data, such as electronic medical data. BE with source authentication is also called authenticated BE or broadcast signcryption. Selvi et al. [[25]](#ref-25) proposed an efficient identity-based signcryption scheme in this area. Similar to broadcast signcryption, there have been several multi-receiver signcryption schemes [[26]](#ref-26), [[27]](#ref-27), where the ciphertexts are of a size linear in the number of the set of receivers. Broadcast authentication schemes have also been proposed without supporting the confidentiality of the broadcast message in the public key setting [[23]](#ref-23). Recently, Yang et al. [[28]](#ref-28) proposed a multi-message and multi-receiver signcryption scheme based on blockchain. The scheme enables medical data providers to send messages to multiple data requesters by executing one signcryption operation, which satisfies the multi-message sending requirements of the data providers in the communication environment. However, the ciphertexts are linear in the number of sets of receivers. Note that our case requires that the data owner use the blockchain to track the sequence of the patient's Digital Twin data so that each care provider can ascertain the progress of the patient's health. The proposed solution requires a constant ciphertext size and an element that can be stored on the blockchain to prove the authorship of data encryption. The existing multi-receiver signcryption does not appear relevant to our scenario. Therefore, the proposed multi-receiver signcryption has a constant ciphertext size with a small size of elements that can be stored on the blockchain to determine the sequence and authorship of the ciphertext.

| | Reference Limitations | Our work |
|---|---|---|
| [[15]](#ref-15) | Does not specify model for data sharing | Provides one-to-one/many model for data sharing |
| | Does not provide any experimental results | Provides experimental results on operations/costs |
| | Unclear explanation of blockchain implementation. | Provides clear implementation of blockchain and operations |
| | Stores raw data off-chain | Stores only encrypted health records |
| | Seeks to virtualize healthcare as a service | Provides the digital twin to access services and data. |
| [[29]](#ref-29) | Work is not applicable to healthcare | Presents a digital twin that is healthcare-inclined |
| | No data confidentiality, a key point of health data sharing | Preserves confidentiality & integrity required in health data sharing |
| | No description of security parameters for storage of files. | Adequately describes the security for stored files |
| [[30]](#ref-30) | Uses symmetric encryption with no support for one-to-many sharing | Uses mIBSC encryption which supports one-to-many sharing |
| | Does not provide integrity controls for off-chain data storage | Uses inherent blockchain integrity controls |
| [[31]](#ref-31) | Focused on securing health data sharing between individual patients | Provides a digital twin that supports multiple user access |
| | Uses anonymity as a key security metric. | Requires identity for digital twin creation and usage |
| [[24]](#ref-24) | Does not protect data integrity, essential for secure data transactions | Guarantees data integrity, scheme thrives on signcryption & blockchain. |
| | Not applicable to health data sharing as there is no system model | Provides a system model, digital twin can access data/services. |
| | Protocol also lack verification. | Verification of protocol |
| [[26]](#ref-26) | Ciphertext sizes grow linearly with increasing number of receivers | Maintains static ciphertext size irrespective of no. of receivers |
| | | Reduces communication and computation costs. |
| | Not applicable to data sharing as there is no system model | Provides system model, digital twin can securely access data |
| [[28]](#ref-28) | Ciphertext sizes grow linearly with increasing number of receivers | Maintains static ciphertext size irrespective of size of no. of receivers |
| | | Reduces communication and computation costs. |
| | Not applicable to digital twin operations such as data contracts and service contracts. | Is based on digital twin operations. |
| | No sequential ordering for tracking digital twin authorship | Provides digital twin authorship tracking to check patient progress and completeness of patient data. |

### <a id="ref-T1"></a>Table 1. Comparison of reviewed literature with proposed solution.

<https://doi.org/10.1371/journal.pone.0286120.t001>

### <a id="ref-T2"></a>Table 2. A comparison of some state-of-the-art Digital Twin research papers in healthcare.

| | [[11]](#ref-11) | [[12]](#ref-12) [[13]](#ref-13) | [[14]](#ref-14) | [[15]](#ref-15) |
|---|---|---|---|---|
| Focus | Mo Imp Integration | | Public health management | Structured data aggregation |
| Utility SI SI | | Strategic care planning | Pandemic control (Covid-19) | Secure health data storage |
| Paradigm PM PC | | Multi-agent systems | Smart City health | Multi-agent systems |
| Security | NP | NP | NP | NP | AP |
| Privacy | NP | NP | NP | NP | AP |
| Framework | NP | NP | Agent-based | Blockchain-based | Blockchain-based |

AP = Applicable, NP = Non-applicable, Mo = Monitoring, PM = Precision medicine, Imp = Implementation, SI = Simulation, PC = Preventive care

<https://doi.org/10.1371/journal.pone.0286120.t002>

Table 1 presents a summary of related work and identified research gaps, while Table 2 compares state-of-the-art research papers in digital twin technology applied to healthcare, categorized by focus, utility, paradigm, security, privacy, and framework. This comprehensive and well-organized overview of research papers serves as a valuable reference for understanding the various areas of focus and approaches in the digital twin field applied to healthcare.

### 3 Preliminaries

This section presents Digital Twins in healthcare, noting their properties. It also emphasizes the Blockchain, Smart Contracts and cryptographic notions.

### 3.1 Multi-receiver Identity-Based Signcryption

A multi-receiver identity-based encryption scheme (mIBSC) comprises four algorithms: Setup, Extract, Signcrypt, and Designcrypt, which are described as follows:

- 1. Setup(λ, *N*) → (*params*, *MSK*): The Setup algorithm takes a security parameter λ and *N* maximal size of the set of receivers for one encryption as input and provides a master secret key *MSK* and a set of public parameters *params* as the outputs.
- 2. Extract( *MSK*; *IDi*) → *SKIDi*: The Extract algorithm takes a master secret key, *MSK* and an identity, *IDi* as input and provides the secret key *SKIDi* as an output.
- 3. Signcrypt( *m*; *S*; *IDSender*; *SKIDSender*) → s. The signcrypt algorithm takes in message *m*, the sender's identity *IDSender* and the sender's secret key *SKIDSender* and a set of identities of recipients *S* = {*ID*1, . . ., *IDt*}, with *s* ≤ *N*, and returns signcryption *σ* of *m* from *SKIDSender*. The broadcast message to users in *S* is made up of (*S*, *IDSender*, *CT*).
- 4. Designcrypt(s*; S*; *IDSender*; *IDi* ; *SKIDi*) → *m*: The Designcrypt algorithm takes in a signcryption *σ*, a subset *S* = {*ID*1, . . ., *IDt*}, with *s* ≤ *N*, the sender's identity *IDSender*, a receiver's identity *IDi* and the associated private key *SKIDi*. If *IDi* ∈ *S*, the algorithm returns the message *m*. Otherwise it returns an error symbol ?.

Note that the public parameters *params* have been omitted for a concise description of the algorithms in mIBSC scheme. Due to page limitations the confidentiality and unforgeability security models of mIBSC have been omitted. Readers can refer to [[25]](#ref-25) for the security models.

### 3.2 Digital Twins

A patient Digital Twin is an evolving data-driven model that presents increasingly detailed approximations of a patient's condition(s). Data from patients' Electronic Medical Records (EMRs) and other relevant data sources can be combined and analyzed to produce a computational model to represent the patient digitally. Thus, analyses of the Digital Twin can facilitate predictions in sensitive areas such as experimental drug interactions [[32]](#ref-32), performance of tasks, create working models of organs, and study the behavior of physiological systems. The patient's Digital Twin needs properties that facilitate analytics and other services. We describe these properties briefly below:

- **Adaptability**: For a patient Digital Twin, we define adaptability as the capacity to accept and incorporate changes to the Digital Twin so that it can adjust to suit predicted, anticipated, or stochastic changes. The virtual model must accommodate the changes that occur over its lifetime. Critically, the adaptability property provides the basis for other properties as well.
- **Extensibility**: The Digital Twin must be extensible to account for new parameters to be tracked for optimal operation and performance. For a patient's Digital Twin, this is important for the several cycles of health conditions a patient may have over time. Extensibility allows the addition of new modules to enable functionality and capabilities so the Digital Twin can grow.
- **Modularity**: Aspects of the person that require monitoring can be virtualized and updated to provide insights for improved care. The patient Digital Twin can therefore be composed of several distinct but interconnected modules grouped into logical categories. These modules may represent physiological systems, conditions, etc. The modules can include all data relevant to patient care.

- **Connectivity**: Connectivity distinguishes the Digital Twin from other analytic models. Hence, we define connectivity as the capacity to connect to systems, platforms, and services to provide data for operating the physical asset. It may be updated periodically from data sources with changes in predefined categories of data, contexts, and conditions. The availability of new data, bandwidth, etc., can determine the frequency of connectivity.
- **Programmability**: The patient Digital Twin can support experiments by taking data inputs that can be processed to determine desirable outcomes within constrained boundaries and under specific conditions to support optimal health. Thus, a Digital Twin instance can test and adaptively refine treatment until the desired outcome is optimal. Conversely, failure of such experiments has no disadvantage for the patient since the Digital Twin can have multiple instances.
- **Flags**: The Digital Twin can represent a set of distinct conditions and system states that a physical system manifests under specified constraints. The Digital Twin can provide data to adaptively and preemptively manage the patient's condition(s) through simulations. Thus, the twin can receive configurations that respond to each medical condition's thresholds.

### 3.3 Blockchain

The blockchain is a linked-list data structure and a consensus protocol initially designed to prevent double-spending in Bitcoin. Each block *b* in the blockchain *β* is a container that holds transaction data. The blockchain maintains an extending list of transactions such that each node contains copies of transactions accepted by the network. Transactions in the blockchain are immutable and pseudonymous, and users may generate a new address for each transaction to achieve credible anonymity on the network. Nodes collaborate to confer transaction validity through a consensus mechanism, so that a single coherent version of history is maintained as the basis for further action. This blockchain property provides behavioral data for developing the patient's Digital Twin. Fig 2 depicts a visual representation of the blockchain showing how transactions are linked. We base our system on the blockchain to account for the following:

- **Preemptive Assumptions on User Behavior**: The patient Digital Twin is a data-sharing agent that provides insights on specific aspects of the patient's health. A requester may exhibit behavior that deviates from care requirements, so capturing all requests/responses is crucial to account for connections between healthcare goals and outcomes. Thus, we capture instances of the patient Digital Twin for offline storage while proof of their existence is stored on the blockchain. The timestamps of Digital Twin instances and blockchain data are essential in preemptively constructing a timeline for the sequence of actions that definitively establish cause and effect.
- **Consistent View of Transactions**: For specialized care, patients' mobility among several hospitals makes healthcare a collaborative venture. However, hospitals do not update one another on patients' progress for obvious regulatory, competitive, and economic reasons. Thus, while a complete, consistent view of a patient's medical history is beneficial, it may be unavailable. Using a patient Digital Twin instance for each hospital, the patient can maintain a master Digital Twin that synchronizes with the other instances after validation.
- **Immutability of Records**: Since a complete medical history is critical to the treatment, the blockchain can be used to create and sustain a distributed, immutable ledger of Digital Twin instances for the patient. This guarantees access to health records for caregivers in multiple institutions while ensuring that appending data to patient Digital Twin instances cannot be

![Image Description: This diagram illustrates a system architecture for managing patient data across multiple hospitals using blockchain technology. It shows data flowing from patients to hospitals, then to a data management module for collection and analytics. The processed data is stored on a blockchain, with a query system providing access control via smart contracts and authentication. Finally, a separate offline storage layer maintains patient digital twin instances, mirroring data across hospitals. The diagram visually depicts data flow and interaction between various components, clarifying the system’s layered design.](_page_7_Figure_2.jpeg)
**Fig 2. A visual representation of transactions on the blockchain.**<https://doi.org/10.1371/journal.pone.0286120.g002>

performed without the proper permissions. Thus, timestamped updates to Digital Twin instances and their hashes combine to provide greater security.

### 3.4 Smart contracts

We include the blockchain in our research to fully take advantage of the Smart Contract functionality. A *smart contract* is a script stored and executed on the blockchain by a connected node after meeting specific contract conditions. By encoding desirable actions as respondent scripts without specifying which node can perform them, we can ensure required interactions are censorship-resistant. It is critical to automate the predictable aspects of Digital Twin operations like updates and limit manual interactions by users other than the patient and approved caregivers. Smart contracts securely decentralize the Digital Twin update process by conceptualizing the patient as a set of interacting scripts, as shown in Fig 3. While smart contracts are not the only way to secure updates to the Digital Twin, they rely on other blockchain properties to offer extra layers of security through data provenance [[33]](#ref-33). In this research, we used the Ethereum blockchain because of its global user base and support for smart contracts.

### 4 System overview

This section presents an overview of the proposed blockchain-secure patient Digital Twin system using smart contracts. Fig 4 shows the overall system architecture. The proposed system has several entities, including the data owner (patient), data users (hospitals), and the system itself, which includes data management, query system, and blockchain network. These entities

![Image Description: The bar chart displays ciphertext size (in bytes) against the number of identities for different cryptographic schemes. It compares the ciphertext size of "our" method against several existing methods ([36], [37], [38], [28], [39]). The chart shows that the "our" method generally produces smaller ciphertexts, particularly as the number of identities increases. The comparison highlights the efficiency improvement achieved by the proposed scheme.](_page_8_Figure_7.jpeg)
**Fig 3. A conceptual overview of the Digital Twin as a construct of smart contracts.**<https://doi.org/10.1371/journal.pone.0286120.g003>

![Image Description: Figure 4 illustrates a system architecture for a patient Digital Twin. A diagram shows a patient (black figure) providing data and receiving insights. This information feeds into a "Medical Profile" block containing Electronic Medical Records, Electronic Health Records, and Data Analytics. A model generates a light-blue figure representing the Digital Twin, updated over time ("Twin Instanceᵢ", "Twin Instanceₙ"). The diagram depicts data flow and the creation of multiple twin instances across time.](_page_9_Figure_2.jpeg)

![Image Description: The image contains a Digital Object Identifier (DOI). Specifically, it shows "https://doi.org/10.1371/journal.pone.0286120.g004", which serves as a persistent link to access a specific figure (g004) within a research article published in PLOS ONE. The DOI facilitates easy retrieval of the referenced figure from online databases.](_page_9_Figure_3.jpeg)

work together to ensure seamless interactions and secure data sharing among the components of the system. Below is a brief description of the system entities and their functions:

- 1. **Data owner**: The patient is the owner of the data obtained from sensors, hospital records, and other health records required to create their digital twin. However, the franchise of the data is given to the hospital to maintain accurate health records to secure the wellness of the patient without any security breaches. Therefore, the hospital is the custodian of the data.
- 2. **Hospitals**: Hospitals play a crucial role in creating complete medical information for the patient to generate master records, which are accurate, fresh, computed, and sound to create a digital twin for the patient. Nurses and doctors who deal directly with the patient's digital twin for good health provision are considered trustworthy to execute their roles without being an adversary for data breaches. The system ensures that encrypted data used in creating the patient digital twin is accessible only to those authorized in the hospital to avoid sensitive information falling into the wrong hands.
- 3. **Patient**: In the context of this research, a patient is defined as a human entity who seeks healthcare services from a hospital and is a primary data contributor in the healthcare system. The healthcare services that the patient receives require data sharing transactions with other entities within the hospital or outside of it. Hence, the patient's medical record is essential for proper care and can also be shared with other healthcare providers as necessary upon authorised request.
- 4. **Query System**: The Query System has three components and processes users' requests for access to the patient Digital Twin. The first is the Authentication module which verifies the source and destination of requests before they can be processed. It connects to an Access Policies module which is the second component to check for specific permissions patients define when they first register in the system as users. The third is the Smart Contracts module which executes the transaction of data access after the first two modules have successfully processed a user's request.
- 5. **Data Management**: This component presents an interface for participating hospitals to provide data on patients. It receives patient data from the hospitals and assigns it to the respective Digital Twin after performing preliminary analytics to check for new content for updating the patient Digital Twin. It has three modules: Data Collection, Analytics, and

![Image Description: Figure 5 is a flowchart illustrating a system architecture for managing patient digital twins on a blockchain. A patient's data undergoes authentication and access control via smart contracts. Multiple digital twin instances (Hᵢ, Hₙ) are shown, with a master twin, all stored on the blockchain represented as interconnected blocks. The diagram depicts data flow from patient to digital twin instances and interactions between doctors and the system via requests and replies.](_page_10_Figure_2.jpeg)

<https://doi.org/10.1371/journal.pone.0286120.g005>

Storage modules. The Storage is partitioned into two distinct areas of administration: online Storage for operational data and offline Storage for data at rest, such as inactive Digital Twin instances.

6. **Blockchain**: The blockchain network receives and stores completed transactions from network nodes. The data from complete transactions is first prepared into discrete blocks containing transaction details of import to patient care. In this study, we define the blockchain as a decentralized and distributed network of participating hospitals that collectively maintain a tamper-proof and transparent record of longitudinal patient data using consensus mechanisms, cryptographic algorithms, and smart contracts. The patient's latest transaction hash is included in the current block, along with records of queries, access requests, and hashes of patient Digital Twin instances as shown in Fig 5. The blockchain network's version of transactions takes precedence over any single institution's records, ensuring transparency and accountability.

## 5 System design

In this section, we will present a thorough description of the proposed scheme's design and provide an illustrative scenario of its application.

### 5.1 Multi-receiver Identity-Based Signcryption(mIBSC)

**5.1.1** *Setup***(λ,** *N***)**→**(***params***,** *MSK***).**The scheme's security parameter is λ, and the maximum size of the collection of receivers is *N*. G1*;*G^2^ are two prime groups of order *p* such that |*p*| = λ. *g* ∈ G^1^ and *h* ∈ G^2^ such that a bilinear map *e* : G^1^ × G^2^ → G*T*. Let's call the number of bits required to indicate an identity and a message *n*^0^ and *n*^1^, respectively. Three hash functions are used: H^1^ : {0*;*1}^n^0^ → Z^*^p^*; H^2^ : {0*;*1}^n^1^ × G^2^ → Z^*^p^*, and H^3^ : G^2^ → {0*;* 1}^(n^1^)+|G2| .

The PKG selects g $ Z^*^p^* and calculates *w*=*g^γ^* and *u*=*e*(*g*, *h*). The public parameters are as follows:

$$
params \leftarrow (w, u, h, h^{\gamma}, \ldots, h^{\gamma^N})
$$

The Master Secret Key is

$$
MSK = (g, \gamma).
$$

**5.1.2 Extract**(*IDi*; *MSK*) → *SKIDi* **.**The PKG runs the Extract algorithm with the input of the user identity *IDi* and master secret key *MSK* = (*g*, *γ*). Upon successful validation of the *IDi*, the PKG computes the secret key as *SKIDi*^=^ *g*^(1/H1(*IDi*)+γ)^. As a patient medical data is tailored into a Digital Twin to predict how a patient would respond to a given medication, the health models and data must be stored chronologically. Hence, a doctor may be confident that the patient digital twin holds accurate data and that all computational results on the patient digital twin are correct. This permits the doctor to see how a patient digital twin responds to a set of data input over time. Before outsourcing medical data to a cloud server, the hospital employs a smart contract to establish blockchain proof to achieve immutable sequential order.

**5.1.3 Signcryption.**Suppose a hospital with an identity *IDSender*, and a private key

**SKsender:** ^ = ^ *g*^(1/H^1^(*IDSender*)+γ)^ wants to signcrypt a patient's health data and a Digital Twin which are denoted here as *m* such that *t* healthcare providers of the identities *ID*1, . . ., *IDt* can access the data, it performs the following:

• Select *k* $ Z^*^p^*; {0*;*1}^n^*.

- Compute the following:
- *C*^1^ = *w*^-k^
- *C*^2^ = *h*^k^ *∏*^S^^i=1^ (*g*+H^1^(*IDi*))
- *C*^3^ = *m* *u*^k^.
- *f* = H^2^(*m*; *C*^1^*; C*^2^*; C*^3^)
- *v* = *SK*^k*^sender^
- Output Signcryption(*m*; *S*; *IDSender*; *SKIDSender*) of *m* as s = (*C*^1^*; C*^2^*; C*^3^*; v*;*L), where L is the list of the recipients who can be authorized to designcrypt *σ*.

Here, we provide the details on how a patient digital twin is created. First, in Algorithm 1, a smart contract is deployed by the private key generator. It has to authorize a hospital before it uses Algorithm 2 to create an instance of the patient digital twin. Patients provide data to hospital data management platforms, as shown in the overall system architecture in Fig 4. To create the digital twin, one first provides a list of data sources that can later be updated. Ideally, these are hospital databases that host detailed patient data and online storage platforms for Personal Health Records from wearable sensors and other devices. A patient may have a digital twin for each unique condition such as disease progression, an organ, the whole body, etc.

![Image Description: The image is a flowchart illustrating a contractual framework for digital twins. "Digital Twin Contracts" are central, branching into "Data Contracts" and "Services Contracts". Data contracts further subdivide into contracts for contribution, storage, and requests. Service contracts encompass registration and access contracts. The diagram depicts the relationships between different types of contracts needed to manage a digital twin system.](_page_12_Figure_2.jpeg)

![Image Description: Figure 6 is a caption describing a missing visual representation of a patient Digital Twin. The caption states that the missing figure is a visual depiction of the data request and response process within the Digital Twin framework. No diagram, chart, graph, or equation is present in the provided image; only the caption.](_page_12_Figure_4.jpeg)

<https://doi.org/10.1371/journal.pone.0286120.g006>

Thus, for each patient, doctors can access multiple digital twin instances, as shown in Fig 6. Formally, a digital twin instance *Ti*, as proposed in this research, is a tuple of data sources, *σ* = [*σ*1, *σ*2, . . ., *σn*], and identity of hospital *IDH*, patient *IDP* and ciphertext auxiliary *v* which are encoded into smart contract as *v* = [*v*1, *v*2, . . ., *vn*] in Algorithm 2. The smart contract execution generates a cryptographic hash of the twin instance, *hi*, Merkel root, *mki*, block number, *bi*, and a timestamp, *ts*, to facilitate proper sequencing of the digital twin instances. The digital twin instance *Ti* is represented as shown below.

$$
T_i = \{\sigma_i, h_i, mk_i, b_i, t_s\}.
$$
^(1)^

After being generated, the patient digital twin can be updated continuously to provide the details required for effective care. Hence, for this research, the primary smart contracts included, such as Algorithms 1 and 2, facilitate patient digital twin updates, access to health services, and provenance of the patient digital twin data. Finally, the hospital sends the digital twin instance *Ti* to the cloud server for sequential tracking of the various healthcare centers the patient visits. The EmitNotification alerts the hospitals about the new record update and alerts the hospital about the current digital twin instance.

```text
Algorithm 1: AH: Authorized Hospitals
Data: Identity of hospital (IDH), Address (Addr)
Result: True/False
1 struct {
2 _IDH,A ddr;
3 } T;
4 mapping(IDH ) T) AuthorizedHospitalList;
5 AuthorizedHospitalList[IDH] ←_IDH True;
6 AuthorizedHospitalList[IDH]←_Addr True;
7 EmitNotification(IDH,Addr, msg.sender) /*The EmitNotification trig-
ger event on the blockchain which hospital IDp can listen to get
informed*/
```

**5.1.4 Unsigncryption**(*S*; s*;IDSender*; *SKIDi* ;*IDi* ; *params*)**.**To recover the message *m* from the ciphertext *σ*, a data user with the private key *SKIDi*^=^ *g*^(1/H1(*IDi*)+γ)^ and identity *IDi* (*IDi* ∈ *S*) performs the following:

1. Compute

$$
\begin{array}{l} R=\big(e(C_1, h^{p_{i,S}(\gamma)}\big) \cdot e(SK_{I\!D_i}, C_2)\big)^\frac{1}{\prod_{j=1,j\neq i}^s \pi_1 \cdot n_{j}} \text{ with } \\ p_{i,S}(\gamma)=\frac{1}{\gamma} \cdot (\prod_{j=1,j\neq i}^s (\gamma+\mathcal{H}_1(\text{ID}_j)) - \prod_{j=1,j\neq i}^s \mathcal{H}_1(\text{ID}_j)). \end{array}
$$

- 2. Recover the message as *m*=*C*^3^/*R* and compute *f* = H^2^(*m*; *C*^1^*; C*^2^*; C*^3^)
- 3. Accept the message *m* if *e*(*v*; *h*^γ^ *h*^H^1^(*IDSender*)^) *R*^f^ = 1; otherwise output the error symbol ?.

### 5.2 Correctness

Considering *σ* is well formed ciphertext for *S*:

$$
R' = e(C_1, h^{p_{i,S}(\gamma)}) \cdot e(SK_{ID_i}, C_2)
$$

$$
= e(g^{-k\gamma}, h^{p_{i,S}(\gamma)}) \cdot e\left(g^{\overline{\mathcal{H}}_1(ID_i) + \gamma}, h^k \prod_{j=1}^S (\gamma + \mathcal{H}(ID_j))\right)
$$

$$
= e(g, h)^{-k(\prod_{j=1,j\neq i}^S (\gamma + \mathcal{H}_1(ID_j)) - \prod_{j=1,j\neq i}^S \mathcal{H}_1(ID_j))}.
$$

$$
e(g, h)^k \prod_{j=1,j\neq i}^S (\gamma + \mathcal{H}(ID_j))
$$

$$
= e(g, h)^k \prod_{j=1,j\neq i}^S \mathcal{H}_1(ID_j)
$$

$$
= R \prod_{j=1,j\neq i}^S \mathcal{H}_1(ID_j)
$$

$$
\frac{1}{\gamma \text{prod}_{j=1,j\neq i}^S \mathcal{H}_1(ID_j)} = R = e(g, h)^k
$$

Then, the correctness of signature is performed as:

$$
\begin{aligned} &e(\nu,h^{\gamma}h^{\mathcal{H}_1(D_{sender})})\cdot R^f==1\\ &e\bigg(g^{\big(\frac{1}{\mathcal{H}_1(sender)+\gamma}\big)-kf},h^{\gamma+\mathcal{H}_1(D_{sender})}\bigg)\cdot e(g,h)^{kf}==1\\ &(g,h)^{\big(\frac{\mathcal{H}_1(D_{sender})+\gamma}{\mathcal{H}_1(D_{sender})}\big)-kf}\cdot e(g,h)^{kf}==1\\ &e(g,h)^{-kf+kf}==1\end{aligned}
$$

After successful unsigncryption of the ciphertext which is part of the digital twin data *Ti* recovered from the cloud server, the hospital, decryptor uses the block number *bi* to confirm that the twin instance *hi* the Merkel root *mki* and all other details of the digital twin are true on the blockchain. Note that the Merkel root guarantees the sequence of the digital twin.
**Algorithm 2**: PDTC: Patient Digital Twin Creation

**Data**: ciphertext auxiliary *v*, identity of hospital *IDH*, patient *IDP* **1 struct**{**2** _*IDH*, _*IDP*, _*v*; **3**}*T*;

```text
4 mapping(address ) T) DataTwin;
5 AH ah = AH();
/*Algorithm 1 is called here*/
6 if ah→ AuthorizedHospitalList[IDH] and ah→ AuthorizedAddressList[msg.
sender] then
7 DataTwin[msg.sender]←_IDH IDH;
8 DataTwin[msg.sender]←_IDP IDP;
9 DataTwin[msg.sender]←_v v;
10 EmitNotification(IDH,IDs,P, msg.sender)
11 end
/*The EmitNotification alerts the hospitals about the new record
update*/
```

### 5.3 Application scenarios

The proposed scheme for Blockchain-secure Patient Digital Twin in Healthcare using Smart Contracts can be applied in various domains of healthcare, such as chronic disease management, mental health disorders, patient monitoring, and personalized healthcare. The scheme can help improve the management of these health conditions by securely storing and accessing patient data on the blockchain, while also ensuring data confidentiality, integrity, and privacy through smart contract-based access control and cryptographic techniques.

One of the potential application of the proposed scheme is in managing mental health disorders. A patient with a mental health disorder can use wearable devices to collect data on their mood, sleep patterns, medication adherence, and other health metrics. The data can be securely stored on the cloud repository using Multi-receiver Identity-Based Signcryption (mIBSC) cryptographic technique for data confidentiality and integrity. The data is hashed on the blockchain for secure offline storage and protection of sensitive health information from unauthorized access.

The patient's digital twin (virtual model that captures the essence of a patient's medical conditions and interventions, based on the data collected from various sources, such as electronic medical records (EMR) and personal health records (PHR) from wearable devices) would contain a timestamped list of their medical conditions and corrective interventions, including information on medications, treatments, and therapy sessions. The patient digital twin could be used to monitor the patient's progress over time, identify trends and patterns in their health data, and provide personalized recommendations for managing their mental health disorder.

For example, if the patient's mood is consistently low at certain times of day, the digital twin could suggest adjustments to their medication regimen or therapy sessions. If the patient's sleep patterns change, the digital twin could track the impact on their mood and adjust recommendations accordingly. Smart contracts can provide access control to the patient digital twin, enabling the patient to choose who can view and update their health information. The system could also monitor medication adherence and identify potential adverse drug interactions.

In summary, the proposed scheme can be a powerful tool for improving the management of healthcare and delivering personalized, data-driven care to patients. The use of mIBSC and smart contract-based access control would help ensure the privacy, security, and integrity of the patient's health data, while also enabling secure offline data storage.

### 6 Security proof

Using the Gap Diffie-Hellman Exponent (GDDHE) assumption of [[34]](#ref-34), we demonstrate the IND-sID-CPA security of our system. We begin by defining the intermediate decisional problem as follows.

**Definition 1** *((f,g,F)-GDDHE). Let* B = (*p*; G1*;* G2*;* G*T; e*(*;*)) *denotes a bilinear map group system and let f and g represent two coprime polynomials with distinct pairwise roots with respective orders t and n. Let g*^0^ *denotes a generator of* G^1^ *and h*^0^ *be a generator of* G2.*Solving the (f,g, F)-GDDHE problem consists*:

$$
g_0, g_0^{\gamma}, \ldots, g_0^{\gamma^{t-1}}, g_0^{\gamma f(\gamma)}, g_0^{k, \gamma f(\gamma)},
$$

$$
h_0, h_0^{\gamma}, \ldots, h_0^{\gamma^{2n}}, h_0^{k, g(\gamma)},
$$

**The adversary:** A *decides whether T* ∈ *e*(*g*0, *h*0) *k*^f^(*γ*) *or T is a random element in* G*T*. **Definition 2** *(l-SDHP Problem) The l-Strong Diffie– Hellman problem (l—SDHP) in the* group G consists of, given g^0^; g^0^γ^;*. . .*; g^γ^l^0^ ,*finding a pair c; g^c+γ^0^ *with c* ∈ Z^*^p^* [[18]](#ref-18)]

We denote by *Advl SDHP*^A^ the advantage of A in solving the (l—SDHP) in G and set *Advl SDHP*^A^ = *Pr* A(*g*^0^; g^0^γ^;*. . .*; g^γ^l^0^) = *c; g*^1^c+γ^0^ , where *l*;*c* ∈ Z^*^p^*. The l—SDHP assumption is that, for any probabilistic polynomial time algorithm A, the advantage *Advl SDHP*^A^ is negligible.

### 6.1 Confidentiality

Let *Advgddhe* (*f*; *g*; *F*; A) denotes the advantage of A in distinguishing the distributions (i.e., *T* ∈ *R*G or *T* ∈ (*g*0, *h*0) *k*^f^(*γ*) , where *R* denotes random selection of an element in G).
**Corollary 0.1** *For any probabilistic algorithm* A *that sends at most q queries to the oracle, the adversary* A *has*:

$$
Advgddhe(f, g, F) \le \frac{(q + 2(n + t + 4) + 2)^2 \cdot d}{2p}
$$

*where, d*= 2 *max*(*n*, *t*+ 1), *t* ∈ *R* Zq*, *and n is the total number of identities*.

**Theorem 1** *For any n, t we have Adv*IND sID CPA *mIBSC* ≤ 2 *Advgddhe* (*f*; *g*; *F*)

Algorithm C is provided with the input B = (*p*; G1*;* G2*;* G*T; e*(*;*)), and a (f,g,F)-GDDHE instance in B (as described in Definition 1). Hence, we have f and g two coprime polynomials with pairwise distinct roots, of respective orders t and n, and C is given

$$
g_0, g_0^{\gamma}, \ldots, g_0^{\gamma^{t-1}}, g_0^{\gamma f(\gamma)}, g_0^{k \gamma f(\gamma)}, h_0, h_0^{\gamma}, \ldots, h_0^{\gamma^{2n}}, h_0^{k g(\gamma)},
$$

and *T* ∈ G*T*, decides whether *T* ∈ *e*(*g*0, *h*0) *k*^f^(*γ*) or *T* is a random element in G*T*. We indicate that *f* and *g* are unitary polynomials for clarity, but this is not a requirement.

### 6.2 Notations

- *f*(*X*) = *∏*^t^^i=1^(*X*+*xi*); *g*(*X*) = *∏*^t+n^^i=t+1^(*X*+*xi*)
- *fi* (*x*) = *f*(*x*)/(*x*+*xi*) for *i* ∈ [1,*t*], which is a polynomial of degree *t*− 1
- *gi* (*x*) = *g*(*x*)/(*x*+*xi*) for *i* ∈ [*t*+ 1,*t*+*n*], which is a polynomial of degree *n*− 1
- 1.**Init**: The adversary A commits a set *S*^*^ = *ID*^*^1^;*. . .*; ID*^*^t*^*^ of identities that it wants to attack (with *t*^*^ ≤ *n*).

2. **Setup**: To produce the system parameters, C sets *g* = *g*^f^(*y*)^0^ (i.e. without computing it) and sets

$$
h = h_0^{\prod_{i=t+S^*+i}^{t+n}(\gamma + x_i)}, w = g_0^{\gamma f(\gamma) - g^{\gamma}},
$$

$$
v = e(g_0, h_0)^{f(\gamma)} \prod_{t+s^*+1}^{t+n}(\gamma + x_i)} = e(g, h).
$$

Eventually, C defines the public parameters as *params* = (*w*; *u*; *h*; *h*^γ^;*. . .*; h^γ^N^). Note that the challenger C is restricted from accessing the element *g*. C runs A on the system parameters B*;* H1*;* H^2^ and params. Here, the hash oracles H1*;*H^2^ are controlled by C.

- 3.**Query Phase 1**: At any point in time, the adversary A can query the following random oracles. To answer the queries, C maintains two lists LH^1^ and LH^2^ .
- H^1^ queries: The list LH^1^ contains at the beginning:

$$
\big\{ \big(*, x_i, *\big)\big\}_{i=1}^t, \big\{ \big( ID_i, x_i, *\big)\big\}_{i=t+1}^{t+s^*}
$$

(We select * to represent an empty element in LH^1^ . When A decides to query on identity *IDi*,

(a) If *IDi* already exists in the list LH^1^ , C answers with *xi*.

(b) Else, C sets H1(*IDi*) = *xi* and completes the list with (*IDi*, *xi*, *).

- H^2^ queries: To respond to this query, C keeps a list of tuples known as LH^2^ list. Each entry in this tuple is of the form (*m*, *C*^1^*, C*^2^*, C*^3^*). At the beginning of the list, it is empty. To respond to queries, algorithm C performs the following:
- If the queries on (*m*, *C*^1^*, C*^2^*, C*^3^*) is in the list (*m*, *C*^1^*, C*^2^*, C*^3^*, *f*), then respond with *f* = H^2^(*m*; *C*^1^*; C*^2^*; C*^3^*).
- Else, C selects a random *f* ∈ Z^*^p^* and updates *L*^H^2^ list with (*m*, *C*^1^*, C*^2^*, C*^3^*, *f*). C outputs *f* to A.
- 4.**Extraction queries**: The challenger C runs O*Extract* on *IDi* ∈ *S*^*^ and sends the associated private key *SKIDi* to the adversary A. To generate the keys,
- If A has already issued an extraction query on *IDi*, C responds with the associated *SKIDi* in the list LH^1^ .
- Otherwise, if A already issued a hash query on *IDi*, then C uses the associated *xi* to generate *SKIDi* = *g*^(fi(γ))^0^ = *g*^(1/(γ+H1(*IDi*)))^ and then updates the list LH^1^ with *SKIDi* for *IDi*.
- Otherwise, C sets H1(*IDi*) = *xi*, generates the associated *SKIDi* exactly as stated earlier and completes the list LH^1^ with *SKIDi* for *IDi*.
- 5. **Challenge** At some point in time, C decides that phase 1 is over, challenger C computes Signcrypt(*m*; *S*^*^;*IDSender*; *SKIDSender* ; *params*) → s^*^ , where

$$
\begin{array}{lll} C_1=&g_0^{-k\gamma f(\gamma)}, C_2=h_0^{k g(\gamma)}, C_3=m_b\cdot T^{\prod_{i=t+s^*+1}^{t+n}x_i}\\[2mm] &e(g_0^{k\gamma f(\gamma)},h_0^{q'})\\[2mm] f=&\mathcal{H}_2(m_b,C_1,C_2,C_3), v^*=SK_{\textit{sender}}^{-kf}\\ \end{array}
$$

Here the challenger C randomly selects *b* ∈ {0, 1} and sets *m*=*mb*. C returns

$$
\sigma^* = (C_1, C_2, C_3^*, v^*).
$$
with $q(\gamma) = \frac{1}{\gamma} \left( \prod_{i=t+s^*+1}^{t+n} (\gamma + x_i) - \prod_{i=t+s^*+1}^{t+n} (x_i) \right)$ . One can verify that

$$
C_1 = w^{-k},
$$

$$
C_2 = h_0^{k} \prod_{i=t+s^*=1}^{t+1} (\gamma + x_i) \prod_{i=t+1}^{t+s^*} (\gamma + x_i)
$$

$$
= h^k \prod_{i=t+1}^{t+s^*} (\gamma + \mathcal{H}_1(D_i^*))
$$

Note that if *T*=*e*(*g*0, *h*0) *k*^f^(*y*) , then *C*^3^ = *mb* *u*^k^.

- 6.**Query Phase 2**: This phase is same as phase 1. The adversary A continues to issue queries with the restriction that no extraction query is committed on *IDi* ∈ *S*^*^.
- 7. **Guess**: Finally, A returns a guess *b*^0^ ∈ {0, 1} and wins the game if *b*=*b*^0^ . One has

$$
Advsdthe(f, g, F, C)
$$

= Pr[ $b' = b$ |real] - Pr[ $b' = b$ |rand]
= $\frac{1}{2}$ × (Pr[ $b' = 1$ | $b = 1$ ∧ real] -
Pr[ $b' = 1$ | $b = 0$ ∧ real])
= $\frac{1}{2}$ × (Pr[ $b' = 1$ | $b = 1$ ∧ rand] -
Pr[ $b' = 1$ | $b = 0$ ∧ rand])

In the random situation, the distribution of *b* is independent of the adversary's point of view. *Pr*[*b*^0^ = 1|*b*= 1 ^*rand*] − *Pr*[*b*^0^ = 1|*b*= 0 ^*rand*]. All simulations are perfect, the distributions of all variables defined by C absolutely conform with the semantic security game. Therefore *Adv*IND sID CPA *mIBSC* (*t*; *n*A) = *Pr*[ *b*^0^ = 1|*b*= 1 ^*real*] − *Pr*[ *b*^0^ = 1|*b*= 0 ^*real*]. Putting it together, yield *Advgddhe*(*f*; *g*; *F*; C) = ^(1/2)^ *Adv*IND sID CPA *mIBSC* (*t*; *n*A).

### 6.3 Unforgeability

Assume that EUF-CMA adversary A making *l* extraction queries, *q*H*i* queries to random oracles *Hi* (*i*= 1, 2) and *qsc* signcryption queries, has an advantage *e* ≥ 10(*qsc* + 1)(*qsc*+*qH*^2^) = 2^k^ against the proposed scheme. Then, there is an algorithm *R* to solve the (*l*+*N*)–*SDHP* with advantage

$$
e'\geq \frac{1}{9}.
$$
*R* provides the input (*h*; *h*^γ^;*. . .*; h^γ^l+N^) and aims to find a pair *c*; *h*^(1/(c+γ))^. In a setup phase, it constructs a generator *G* ∈ G^1^ such that it knows *l*− 1 pairs *xi*;*G*^(1/(xi+γ))^ for *x*1*;*. . .*; xl^1^ $ Z^*^p^*. The challenger C performs the following:

- Select Z $ Z^*^p^* and set *P* = *h*^η^.
- Select *x*1*;*. . .*; xl^1^ $ Z^*^p^* such that *f*(*z*) = *∏*^l^1^^i=1^(*z*+*xi*) to get *c*0*;c*1*;*. . .*;cl^1^ $ Z^*^p^* with *f*(*z*) = *∑*^l^1^^i=0^ *c*1*zi*.

- Set elements *H* = *h* *∑*^l^1^^i=0^ *ci*g^i^ = *hf*(*γ*)^ and *G*=*H*^η^=*pf*(*γ*).
- Compute *h* *∏*^l^^i=1^ *cl*^1^g^i^ = *H*^γ^; *H*^γ^2^;*. . .*; H^γ^N^ and make h*G*^γ^; *H*^γ^; *H*^γ^2^;*. . .*; H^γ^N^; *e*(*G*; *H*) public.
- Let 1 ≤ *i* ≤ *l*− 1 and expand *fi* (*z*) = *f*(*z*)/(*z*+*xi*) = *∑*^l^2^^i=0^ *di zi* and *pfi*(*γ*) = *G*^(1/(xi+γ))^.

A gives C the target user identity *ID*^*^'* on which A wants to forge a signature. C then prepares to respond to A's queries throughout the game. It starts by setting the counter *i* to 1. We will assume that H^1^ queries are distinct for the sake of simplicity, and that any query involving an identity *IDi* is preceded by the random oracle query H1(*IDi*).

- H^1^**queries**: On the input of the identity *IDi* by A, C returns a random *x'* $ Z^*^p^* if *IDi* = *ID*^*^'*. Else, C responds *xi* and increases *i*. C stores (*IDi*, *xi*) in a list LH^1^ . Note H^2^ query is same as in the confidentiality proof, so it is omitted here.
- **Key generation queries on** *IDi* ≠ *ID*^*^'* : C retrieves the matching pair (*IDi*, *xi*) from LH^1^ and outputs the previously computed *G*^(1/(γ+xi))^. Note: No extraction query on *ID*^*^'* can be executed.
- **Forgery**: Signcryption query on (*m*; *ID*A*;*ID*1*; *ID*2*;*. . .*;IDn*): If *ID*^A^ ≠ *ID*^*^'*, proceeds normally as in the Signcrypt algorithm. Otherwise, C performs the following:
- Select *k* $ Z^*^p^*.
- Compute the following:
- *C*^*^1^ = *w*^((γ+xA)k)^
- *C*^*^2^ = *H*^((γ+xA)k) *∏*^n^^i=1^ (*xi*+γ)^
- *C*^*^3^ = *m* *u*^k^.
- *f*^*^ = H^2^(*m*; *C*^1^*; C*^2^*; C*^3^)
- *v*^*^ = *G*^(1/(γ+xA)) *kf*
- Add the elements (*m*; *C*^*^1^*; C*^*^2^*; C*^*^3^*; f*^*^) to LH^2^ list.
- Output signcryption of *m* as h*C*^*^1^*; C*^*^2^*; C*^*^3^*; v*^*^;*Li, where L is the list of recipients who are authorized to designcrypt *σ*^*^.
- **Unsigncryption** (*S*;s^*^;*ID*^*^'*; *SKIDi* ;*IDi* ; *params*): C looks up L*^H^2^ for an entry of the form (*m*; *C*^*^1^*; C*^*^2^*; C*^*^3^*; f*^*^) and checks whether it satisfies the following condition:

$$
\begin{aligned} &e(G^{\frac{1}{(\gamma+\kappa_{\mathcal{A}})-k_{\mathcal{I}}}},H^{\gamma}H^{\mathcal{H}_{1}(ID^*_{\ell})})\cdot\left(G,H\right)^{k_{\mathcal{I}}}\overset{?}{=}1\\ &e(G,H)^{\left(\frac{\kappa_{\mathcal{A}}+\gamma}{H_{1}(ID^*_{\ell})+\gamma}\right)-k_{\mathcal{I}}^{\mathcal{I}}}\cdot e(G,H)^{k_{\mathcal{I}}}\overset{?}{=}1\end{aligned}
$$

The case in which A can generate a valid ciphertext is by correctly guessing the hash value *x*^A^ = H1(*ID*^*^'*) without querying on (*ID*^*^'*). However, this event occurs only with a negligible probability of ^(1/2)^l.

Note that, with the forking lemma, A does not perform key generation queries on *IDi* ≠ *ID*^*^'*. Based on the theory of irreflexivity, *R* can generate the message-signature from *σ*^*^ with the private key *skID'*. Since identity-less chosen message attack is possible with a forking

lemma [[35]](#ref-35), we unify the sender's message *m* and identity A*'* as a fake message (A*'; m*). Supposing A is an effective forger, then there exists a very powerful algorithm A^0^ which can produce a pair of signed messages ((A*'; f*^*^; k*^*^); v*^*^) and ((A*'; f ; k*); v), where *f* ≠ *f*^*^ under the same commitment. *C*^ interacts with A^0^ and A to solve the ECDL problem as follows:

1. Based on the forking lemma in [[35]](#ref-35), by executing A', *C*^ can derive two distinct equations from the signatures ((*IDℓ*, *m*, *f*, *k*), *v*) and ((ID*^*^'*; *m*; *f*^*^; k*^*^); v*^*^) as:

$$
e\bigg(G^{\frac{1}{(\gamma + x_{\mathcal{A}_{\ell}}) - k_{j}^{i}}}, H^{\gamma} H^{\mathcal{H}_{1}(ID_{\ell}^{*})}\bigg) \cdot (G, H)^{k_{j}^{i}} = 1
$$
(2)

$$
e\left(G^{\overline{(y+x_{\mathcal{A}_{\ell}})^{-k^{*}f^{*}}}},H^{\gamma}H^{\mathcal{H}_{1}(D_{\ell}^{*})}\right)\cdot(G,H)^{k^{*}f^{*}}=1
$$
(3)

2. Since both Eqs 2 and 3 satisfy the relations:

$$
e\bigg(G^{\frac{1}{(\gamma+x_{\mathcal{A}_{\ell}})-kj}},H^{\gamma}H^{\mathcal{H}_{1}(ID^{*}_{\ell})}\bigg)\cdot\left(G,H\right)^{kf}\tag{4}
$$

$$
=e\bigg(G^{\frac{1}{(\gamma+\kappa_{\mathcal{A}_{\ell}})-k^{*}f^{*}}},H^{\gamma}H^{\mathcal{H}_{1}(ID_{\ell}^{*})}\bigg)\cdot\left(G,H\right)^{k^{*}f^{*}}\tag{5}
$$

Then, Set *T*^*^ = *v*/*v*^*^ = *G*^(1/(γ+xA')) *kf* / *G*^(1/(γ+xA')) *k*^*^f*^*^ = *G*^(1/(ID*^*^'+γ))^ (Here, *x*^A*'^ = *H*1(*ID*^*^'*)). From *T*^*^, R first obtains *a*−1, . . . *al*−^2^ for which *f*(*z*)/(*z*+*x*A*'^) = *a*^(1/(z+xA'))^ + *∑*^l^2^^i=0^ *ai zi* and computes

$$
\nu^*=[T^*\cdot P^{\prod_{i=0}^{l-2}a_i\gamma_i}]^{\frac{1}{a_1}}=P^{\frac{1}{X_\ell+\gamma}}
$$

and Z^(1)^ *v*^*^ = *h*^(1/(x'+γ))^ = *h*^(1/H1(ID'))^ since *P*=*h*^η^. Eventually, *R* outputs the *x'*; *h*^(1/(x'+γ))^ as the solution to (l + N)—SDHP.

As in [[22]](#ref-22), if *Adv*mIBBSC^A^ ≥ 10(*qsc* + 1)(*qsc*+*qH*^2^) = 2^k^, where *l* extraction queries, *qHi* queries to random oracles *Hi* (*i*= 1, 2) and *qsc* signcryption queries are made, then *Adv*^((l+N))^R SDHP^R^ ≥ 1/9.

### 7 Efficiency evaluation

This section evaluates the efficiency of our scheme as it relates to computational and storage overheads, and the deployment of smart contracts.

### 7.1 Computational overhead

To demonstrate the efficiency of the proposed scheme relative to other schemes, we perform computation analysis with recent broadcast signcryption schemes: [[28]](#ref-28), [[36]](#ref-36)–[[39]](#ref-39). The experiment was conducted on a Windows desktop computer with a 2.0GHz Intel Core i7 processor and 8GB 1600 MHz DDR3 RAM. We used Multi-Precision Integer and Rational Arithmetic C Library (MIRACL), a C++ cryptographic library. The execution times are based on the average of 300 trials. The results of the execution are shown in Table 3. In Table 3, we define the related

| Operation | Timing (ms) |
|---|---|
| Elliptic curve group exponentiation (E^) | 1.26 |
| Bilinear pairing( P^) | 14.32 |
| Pairing-based scalar point multiplication (M1) | 4.34 |
| Elliptic curve point multiplication (M2) | 0.98 |

<a id="ref-T3"></a>Table 3. Running times of time-consuming operations.

<https://doi.org/10.1371/journal.pone.0286120.t003>

symbols to indicate the computational complexity of the operations. However, only the operations in the table are considered in this paper. Other operations, such as addition, subtraction, and hashing, with little or insignificant computational time, are ignored. The theoretical comparison of our proposed scheme and other related works is shown in Table 4. The computation cost benchmarks are shown in Figs 7 and 8. Although the proposed scheme has a high computation cost compared to other related schemes, when we consider pre-computation of the element, the cost of signcryption becomes 3*E*^ while unsigncryption becomes 3*P*^. Hence, the proposed scheme is efficient in communication and computational aspects. The pre-computation becomes applicable when the set of receivers remains the same as in the previous session. Both broadcasters and receivers can reuse the previous information. The difference is significant because the computation operations are reduced to 3*P*^ for unsigncryption on the client side.

### 7.2 Communication overhead

Additionally, we examine the communication overhead of the proposed scheme and other related schemes. As in [[40]](#ref-40), we undertake the size of elements jG1j = 1024 bits, jG2j = 1024 bits and |*m*| = 160 bits. The five schemes are compared in Table 4. The benchmark result in Fig 9 demonstrates unequivocally that the proposed scheme achieves the objectives. The prime objective of the proposed scheme is to have the smallest ciphertext size so that the element which is stored on the blockchain will not increase when the attribute size increases.

### 7.3 Discussion of smart contract deployment and evaluations

We assume the presence of a sensor that can transmit continuous physiological data from the patient to the aggregation platform represented in our research by the Data Management module. Patients' increasing use of wearable sensors validates our assumption in this respect. The Data Management module collects and processes data using the analytics component to sort through received signals to distinguish status data (such as positioning) from care data, such as

| Scheme | Signcryption | Unsigncryption | Ciphertext size |
|---|---|---|---|
| [[36]](#ref-36) | (3n + 1)E^ | M1 + 3P^ + E^ | 3|G1| + n|Z^*^p^*| + |ID| |
| [[37]](#ref-37) | (2n + 1)M2 | 4M2 | 2|G1| + (S + 2)|Z^*^p^*| |
| [[38]](#ref-38) | (4n + 2)E^ | E^ + 4P^ | (2n + 3)|G1| |
| [[28]](#ref-28) | (n + 1)M2 | 3M2 | 2|G1| + (n + 2)|Z^*^p^*| |
| [[39]](#ref-39)* | nM1 + (n + 5)E^ | nM1 + (n + 2)E^ + 3P^ | 3|G1| + (n + 1)|ID| |
| Ours | M1 + (3 + n)E^ | 3P^ + nM1 + nE^ | 4|G1| + |Z^*^p^*| |
<a id="ref-T4"></a>Table 4. Comparison of computational cost and communication cost.

[[39]](#ref-39)*= Proposal I

<https://doi.org/10.1371/journal.pone.0286120.t004>

![Image Description: The bar chart displays ciphertext size (in bytes) versus the number of identities for different encryption schemes ([36], [37], [38], [28], [39]) and a new ("our") method. It compares the ciphertext size performance of various methods as the number of identities increases, showing that the proposed method generally produces smaller ciphertexts.](_page_21_Figure_2.jpeg)
**Fig 7. Signcryption.**<https://doi.org/10.1371/journal.pone.0286120.g007>

![Image Description: The bar chart displays ciphertext size (in bytes) against the number of identities for different encryption schemes ([36], [37], [38], [28], [39]) and a new ("our") scheme. It compares the ciphertext size performance of various schemes as the number of identities increases, showing a generally linear increase in ciphertext size with the number of identities for all schemes. The purpose is to demonstrate the efficiency and scalability of the authors' proposed encryption scheme compared to existing methods.](_page_21_Figure_5.jpeg)
**Fig 8. Unsigncryption cost.**<https://doi.org/10.1371/journal.pone.0286120.g008>

![Image Description: This bar chart displays the gas cost (in Wei) for different components of digital twin smart contracts on a blockchain. The components are contribution, storage, request, registration, and access. Contribution has the highest cost, while request has the lowest. The chart illustrates the varying computational costs associated with each smart contract function.](_page_22_Figure_2.jpeg)

<https://doi.org/10.1371/journal.pone.0286120.g009>

inputs made by doctors and other caregivers. The output from the analytics module is stored by the connected offline storage till the Query System receives requests for data, or smart contracts are executed to create a patient digital twin instance and to update the master digital twin. The metadata for the transaction, such as hashes, timestamps and commitments, are then prepared into a block and transmitted to the blockchain.

For the experiment, we used the Ropsten Test Environment to test several smart contracts grouped into two categories: Data Contracts and Service Contracts. The Data Contracts handle events relating to data contribution, storage and requests. The Service Contracts deal with services to patients. Each smart contract is invoked using its address on the test Blockchain. Each individual contract was developed using the solidity programming language with the Remix IDE. The appropriate amount of ether was provided by Infura at 4 ETH for all tests needed to run on an Ethereum Decentralized Node with more than 2000 test nodes providing an acceptable degree of consensus. The resources for this experiment were a minimum transaction fee of 0.0002 ETH and a gas rate of 0.27 US dollars per transfer. The computer on which the experiments were performed was an Ubuntu Linux desktop configured with a 1.5 TB Solid State Drive hard drive, 16 GB RAM, and an Intel Core i7 CPU running at 2.67 GHz.

Smart contracts-based patient digital twins can effectively and economically automate patient activities in healthcare considering the current high costs. For example, with the Data Contracts that manage data acquisition and sharing tasks, we measured a total deployment cost of 1308303 Wei on Ethereum, which amounts to about $2.6153, a competitive amount for accessing healthcare. Figs 10 and 11 present the costs of deploying smart contracts in dollars and in Wei while Fig 12 shows the cumulative latency for increasing numbers of user requests. Thus, the aggregate latency for 200 requests in the scheme is 1600 seconds, i.e., 8 seconds per request. The average block confirmation time was approximately 11.7 seconds. The low costs of transactions in both time and monetary terms coupled with our system's provable security make it an effective tool for health data sharing. Even in the unlikely event of a dispute, the immutable records and timestamped transactions provide sufficient input for fault tracing and effective resolution.

![Image Description: The bar chart displays the cost of four component smart contracts within a digital twin system: contribution, storage, request, and access. Contribution and access have the highest costs (around $1.2 and $1.1 respectively), while request shows the lowest (approximately $0.4). The chart illustrates the relative expense of each contract type in the context of the paper's discussion on digital twin architecture.](_page_23_Figure_2.jpeg)
**Fig 10. Smart contracts costs in wei.**<https://doi.org/10.1371/journal.pone.0286120.g010>

Researchers have conducted studies on the use of blockchain in healthcare, focusing on secure data sharing. Most research emphasize the blockchain properties of immutable transactions and distributed storage. None have considered hosting a collection of smart contracts to act as a data-sharing agent on behalf of the patient, as proposed in this research. Hospitals' data sharing requirement for patient care makes our proposed smart contracts-based patient digital twin a necessary addition to healthcare innovation. Thus, we compare our proposed system to blockchain-based health data-sharing papers, each of which has been cited more than 200 times. The comparison is made in Table 5.

![Image Description: The bar graph displays the relationship between user requests and latency. The x-axis represents the number of user requests (200, 400, 600, 800, 1000), and the y-axis shows latency in seconds. The graph demonstrates a positive correlation: as the number of user requests increases, latency increases significantly, showing a nearly exponential growth pattern. The purpose is to illustrate the performance impact of increasing user load.](_page_23_Figure_6.jpeg)
**Fig 11. Smart contracts costs in US dollars.**<https://doi.org/10.1371/journal.pone.0286120.g011>

![Image Description: Figure 12 depicts a system architecture diagram. A patient icon inputs data and receives insights from a "Medical Profile" block containing Electronic Medical Records, Electronic Health Records, and Data Analytics. This profile generates a model which produces multiple "Twin Instance" outputs (data, time). The figure illustrates the system's data flow and likely aims to explain system latency in relation to the number of requests processed.](_page_24_Figure_2.jpeg)
<a id="ref-T5"></a>Table 5. Comparison of our work with other frameworks for blockchain health data sharing.

| Metrics | [[36]](#ref-36) | [[37]](#ref-37) | [[38]](#ref-38) | [[28]](#ref-28) | [[39]](#ref-39) | Ours |
|---|---|---|---|---|---|---|
| Blockchain-based | N | N | N | Y | N | Y |
| Digital Twin-based | N | N | N | N | N | Y |
| Access Control | Y | Y | Y | Y | Y | Y |
| Senders and Receivers Known | N | N | N | N | Y | Y |
| Data Privacy-Preserving | Y | Y | Y | Y | Y | Y |

<https://doi.org/10.1371/journal.pone.0286120.t005>

## 8 Conclusion

Modern healthcare places unprecedented focus on patient-centered care, which requires secure communication among multiple parties. The process depends on the secure sharing of patient data and can be tedious for those involved. Thus, automation of a data-sharing mechanism with agency such as the patient digital twin can promote efficient interaction between the entities required to administer patient care. This paper proposes a blockchain-secure patient digital twin as a secure construct for personal health data sharing. We use smart contracts on the Ethereum network to ensure that patients have control over their medical records with guaranteed privacy and security. We protect the data and instances of the digital twins generated using proven cryptographic techniques that are also computationally light. We evaluate our research with some experimental results and comparison with other works. Our proposed system can be integrated into existing healthcare platforms using a permissioned blockchain for maximum privacy and security. We hope to extend the research to provide the patient digital twin with greater autonomy.

## Supporting information

S1 [File.](http://www.plosone.org/article/fetchSingleRepresentation.action?uri=info:doi/10.1371/journal.pone.0286120.s001)(ZIP)
S2 [File.](http://www.plosone.org/article/fetchSingleRepresentation.action?uri=info:doi/10.1371/journal.pone.0286120.s002)(ZIP)

### Author Contributions

**Conceptualization:** Sandro Amofa, Isaac Amankona Obiri.
**Data curation:** Sandro Amofa, Isaac Amankona Obiri.
**Formal analysis:** Sandro Amofa, Isaac Amankona Obiri.
**Project administration:** Qi Xia, Jianbin Gao.
**Resources:** Jingcong Yang.
**Software:** Isaac Amankona Obiri, Bonsu Adjei-Arthur.
**Supervision:** Qi Xia.
**Visualization:** Hu Xia.
**Writing – original draft:** Sandro Amofa, Isaac Amankona Obiri.
**Writing – review & editing:** Sandro Amofa, Isaac Amankona Obiri.

### References

- <a id="ref-1"></a>**[1].** El Saddik A. Digital twins: The convergence of multimedia technologies. IEEE multimedia. 2018; 25 (2):87–92 <https://doi.org/10.1109/MMUL.2018.023121167>
- <a id="ref-2"></a>**[2].** Moser A, Appl C, Bruning S, Hass VC. Mechanistic mathematical models as a basis for digital twins. In: Digital Twins. Springer; 2020. p. 133–180.
- <a id="ref-3"></a>**[3].** Schluse M, Priggemeyer M, Atorf L, Rossmann J. Experimentable digital twins—Streamlining simulation-based systems engineering for industry 4.0. IEEE 627 Transactions on industrial informatics. 2018; 14(4):1722–1731. <https://doi.org/10.1109/TII.2018.2804917>
- <a id="ref-4"></a>**[4].** Popa EO, van Hilten M, Oosterkamp E, Bogaardt MJ. The use of digital twins in healthcare: socio-ethical benefits and socio-ethical risks. Life sciences, society and policy. 2021; 17(1):1–25. [https://doi.org/10.1186/s40504-021-00113-x](https://doi.org/10.1186/s40504-021-00113-x) PMID: [34218818](http://www.ncbi.nlm.nih.gov/pubmed/34218818)
- <a id="ref-5"></a>**[5].** Eckhart M, Ekelhart A. Towards security-aware virtual environments for digital twins. In: Proceedings of the 4th ACM workshop on cyber-physical system security; 2018. p. 61–72.
- <a id="ref-6"></a>**[6].** Amofa S, Sifah EB, Kwame OB, Abla S, Xia Q, Gee JC, et al. A blockchain-based architecture framework for secure sharing of personal health data. In: 2018 IEEE 20th International Conference on e-Health Networking, Applications and Services (Healthcom). IEEE; 2018. p. 1–6.
- <a id="ref-7"></a>**[7].** Xia Q, Gao J, Amofa S. Blockchain Medical Data Sharing. Wireless Blockchain: Principles, Technologies and Applications. 2021; p. 245–268. <https://doi.org/10.1002/9781119790839.ch11>
- <a id="ref-8"></a>**[8].** Xia Q, Sifah EB, Smahi A, Amofa S, Zhang X. BBDS: Blockchain-based data sharing for electronic medical records in cloud environments. Information. 2017; 8(2):44. [https://doi.org/10.3390/info8020044](https://doi.org/10.3390/info8020044)
- <a id="ref-9"></a>**[9].** Sifah EB, Xia Q, Agyekum KOBO, Amofa S, Gao J, Chen R, et al. Chain-based big data access control infrastructure. The Journal of Supercomputing. 2018; 74(10):4945–4964. [https://doi.org/10.1007/s11227-018-2308-7](https://doi.org/10.1007/s11227-018-2308-7)
- <a id="ref-10"></a>**[10].** Zyskind G, Nathan O, et al. Decentralizing privacy: Using blockchain to protect 647 personal data. In: 2015 IEEE Security and Privacy Workshops. IEEE; 2015. p. 180–184.
- <a id="ref-11"></a>**[11].** Ahmadi-Assalemi G, Al-Khateeb H, Maple C, Epiphaniou G, Alhaboby ZA, Alkaabi S, et al. Digital twins for precision healthcare. Cyber Defence in the Age of AI, Smart Societies and Augmented Humanity; Springer Nature Switzerland AG: Cham, Switzerland. 2020; p. 133–158.
- <a id="ref-12"></a>**[12].** De Maeyer C, Markopoulos P. Future outlook on the materialisation, expectations and implementation of Digital Twins in healthcare. In: 34th British HCI Conference 34; 2021. p. 180–191.
- <a id="ref-13"></a>**[13].** Croatti A, Gabellini M, Montagna S, Ricci A. On the integration of agents and digital twins in healthcare. Journal of Medical Systems. 2020; 44(9): 1–8. <https://doi.org/10.1007/s10916-020-01623-5> PMID: [32748066](http://www.ncbi.nlm.nih.gov/pubmed/32748066)
- <a id="ref-14"></a>**[14].** EL Azzaoui A, Kim TW, Loia V, Park JH. Blockchain-based secure digital twin framework for smart healthy city. In: Advanced Multimedia and Ubiquitous Engineering. Springer; 2021. p. 107–113.
- <a id="ref-15"></a>**[15].** Akash SS, Ferdous MS. A Blockchain Based System for Healthcare Digital Twin. IEEE Access. 2022;.

- <a id="ref-16"></a>**[16].** Nielsen CP, da Silva ER, Yu F. Digital Twins and Blockchain–Proof of Concept. Procedia CIRP. 2020; 93:251–255. <https://doi.org/10.1016/j.procir.2020.04.104>
- <a id="ref-17"></a>**[17].** Altun C, Tavli B. Social internet of digital twins via Distributed Ledger 666 technologies: application of predictive maintenance. In: 2019 27th Telecommunications Forum (TELFOR). IEEE; 2019. p. 1–4.
- <a id="ref-18"></a>**[18].** Teng SY, Tous M, Leong WD, How BS, Lam HL, Masa V. Recent advances on industrial data-driven energy savings: Digital twins and infrastructures. Renewable and Sustainable Energy Reviews. 2021; 135:110208. <https://doi.org/10.1016/j.rser.2020.110208>
- <a id="ref-19"></a>**[19].** Yaqoob I, Salah K, Uddin M, Jayaraman R, Omar M, Imran M. Blockchain for digital twins: Recent advances and future research challenges. IEEE Network. 2020; 34(5):290–298. [https://doi.org/10.1109/MNET.001.1900661](https://doi.org/10.1109/MNET.001.1900661)
- <a id="ref-20"></a>**[20].** Fiat A, Naor M. Broadcast Encryption; Crypto'93, LNCS 773; 1994.
- <a id="ref-21"></a>**[21].** Delerablee C. Identity-based broadcast encryption with constant size ciphertexts and private keys. In: International Conference on the Theory and Application of Cryptology and Information Security. Springer; 2007. p. 200–215.
- <a id="ref-22"></a>**[22].** Delerablee C, Paillier P, Pointcheval D. Fully collusion secure dynamic broadcast encryption with constant-size ciphertexts or decryption keys. In: International Conference on Pairing-Based Cryptography. Springer; 2007. p. 39–59.
- <a id="ref-23"></a>**[23].** Ren Y, Gu D. Fully CCA2 secure identity based broadcast encryption without random oracles. Information Processing Letters. 2009; 109(11):527–533. <https://doi.org/10.1016/j.ipl.2009.01.017>
- <a id="ref-24"></a>**[24].** Boneh D, Gentry C, Waters B. Collusion resistant broadcast encryption with short ciphertexts and private keys. In: Annual international cryptology conference. Springer; 2005. p. 258–275.
- <a id="ref-25"></a>**[25].** Sharmila Deva Selvi S, Sree Vivek S, Srinivasan R, Pandu Rangan C. An efficient identity-based signcryption scheme for multiple receivers. In: International workshop on security. Springer; 2009. p. 71–88.
- <a id="ref-26"></a>**[26].** Zia Ullah Bashir M, Ali R. Correction to: A Multi Recipient Aggregate Signcryption Scheme Based on Elliptic Curve. Wireless Personal Communications. 2021; 120(2):1921–1921. [https://doi.org/10.1007/s11277-021-08750-3](https://doi.org/10.1007/s11277-021-08750-3)
- <a id="ref-27"></a>**[27].** Fajari MF, Ogi D. Implementation of Efficient Anonymous Certificate-Based Multi-Message and Multi-Receiver Signcryption On Raspberry Pi-Based Internet of Things Monitoring System. In: 2021 International Conference on ICT for Smart Society (ICISS). IEEE; 2021. p. 1–5.
- <a id="ref-28"></a>**[28].** Yang X, Li X, Li T, Wang X, Wang C, Li B. Efficient and anonymous multi-message and multi-receiver electronic health records sharing scheme without secure channel based on blockchain. Transactions on Emerging Telecommunications Technologies. 2021; 32(12):e4371. [https://doi.org/10.1002/ett.4371](https://doi.org/10.1002/ett.4371)
- <a id="ref-29"></a>**[29].** Hasan HR, Salah K, Jayaraman R, Omar M, Yaqoob I, Pesic S, et al. A blockchain-based approach for the creation of digital twins. IEEE Access. 2020; 8:34113–34126. [https://doi.org/10.1109/ACCESS.2020.2974810](https://doi.org/10.1109/ACCESS.2020.2974810)
- <a id="ref-30"></a>**[30].** Putz B, Dietz M, Empl P, Pernul G. Ethertwin: Blockchain-based secure digital twin information management. Information Processing & Management. 2021; 58(1):102425. [https://doi.org/10.1016/j.ipm.2020.102425](https://doi.org/10.1016/j.ipm.2020.102425)
- <a id="ref-31"></a>**[31].** Amofa S, Gao J, Asante-Mensah MG, Haruna CR, Qi X. Blockchain-Based Patient-to-Patient Health Data Sharing. In: Frontiers in Cyber Security: 5th International Conference, FCS 2022, Kumasi, Ghana, December 13–15, 2022, Proceedings. Springer; 2022. p. 198–210.
- <a id="ref-32"></a>**[32].** Agyemang B, Wu WP, Kpiebaareh MY, Lei Z, Nanor E, Chen L. Multi-view self-attention for interpretable drug–target interaction prediction. Journal of Biomedical Informatics. 2020; 110:103547. [https://doi.org/10.1016/j.jbi.2020.103547](https://doi.org/10.1016/j.jbi.2020.103547) PMID: [32860883](http://www.ncbi.nlm.nih.gov/pubmed/32860883)
- <a id="ref-33"></a>**[33].** Kusi GA, Xia Q, Cobblah CNA, Gao J, Xia H. Training Machine Learning Models Through Preserved Decentralization; 2020. p. 465–472.
- <a id="ref-34"></a>**[34].** Boneh D, Boyen X, Goh EJ. Hierarchical identity based encryption with constant size ciphertext. In: Annual international conference on the theory and applications of cryptographic techniques. Springer; 2005. p. 440–456.
- <a id="ref-35"></a>**[35].** Pointcheval D., Stern J. Security Arguments for Digital Signatures and Blind Signatures. J. Cryptology 13, 361–396 (2000). <https://doi.org/10.1007/s001450010003>
- <a id="ref-36"></a>**[36].** Fan CI, Tseng YF. Anonymous multi-receiver identity-based authenticated encryption with CCA security. Symmetry. 2015; 7(4):1856–1881. <https://doi.org/10.3390/sym7041856>
- <a id="ref-37"></a>**[37].** Pang L, Kou M, Wei M, Li H. Anonymous certificateless multi-receiver signcryption scheme without secure channel. IEEE Access. 2019; 7:84091–84106. [https://doi.org/10.1109/ACCESS.2019.2900072](https://doi.org/10.1109/ACCESS.2019.2900072)

- <a id="ref-38"></a>**[38].** Niu S, Niu L, Yang X, Wang C, Jia X. Heterogeneous hybrid signcryption for multi-message and multireceiver. PloS one. 2017; 12(9):e0184407. <https://doi.org/10.1371/journal.pone.0184407> PMID: [28886125](http://www.ncbi.nlm.nih.gov/pubmed/28886125)
- <a id="ref-39"></a>**[39].** Kim I, Hwang SO. Efficient identity-based broadcast signcryption schemes. Security and Communication Networks. 2014; 7(5):914–925. <https://doi.org/10.1002/sec.802>
- <a id="ref-40"></a>**[40].** Obiri IA, Xia Q, Xia H, Affum E, Abla S, Gao J. Personal health records sharing scheme based on attribute based signcryption with data integrity verifiable. Journal of Computer Security. 2021;(Preprint):1– 34.

## TL;DR
The paper proposes a blockchain-secured patient Digital Twin that uses smart contracts to automate and control access to the twin, ensuring data privacy and integrity through a novel cryptographic scheme.

## Key Insights
The key insight is that smart contracts can be used to automate and enforce access control policies for a patient's Digital Twin, creating a secure and programmable layer for managing sensitive health data. This approach, combined with a novel signcryption scheme (mIBSC) optimized for blockchain, provides a practical solution for ensuring data provenance, privacy, and integrity in a distributed healthcare ecosystem.

## Metadata Summary
### Research Context
- **Research Question**: How can a patient's Digital Twin be secured using blockchain and smart contracts to guarantee access control, privacy, and data provenance, while automating its updates and interactions?
- **Methodology**: The methodology involves designing a three-layer architecture (Device, Blockchain, Application) and using the Ethereum blockchain with smart contracts to manage the Digital Twin. A novel Multi-receiver Identity-Based Signcryption (mIBSC) scheme is proposed to secure the data. The system's performance is evaluated based on latency, smart contract execution times, and storage costs.
- **Key Findings**: The research demonstrates the feasibility of a blockchain-secured Digital Twin framework. The use of smart contracts provides a robust mechanism for automated, policy-based access control. The proposed mIBSC scheme is shown to be efficient for blockchain applications due to its constant-size ciphertext.

### Analysis
- **Limitations**: The evaluation is based on a prototype and does not involve a large-scale, real-world deployment with actual patient data. The paper focuses on the technical framework and does not deeply explore the ethical or legal implications of such a system.
- **Future Work**: Future work could involve applying the framework to a wider range of healthcare use cases, further optimizing the performance and scalability of the system, and conducting real-world clinical trials to validate its effectiveness.