---

cite_key: ghani_2020b
title: Issues and challenges in Cloud Storage Architecture: A Survey
authors: Anwar Ghani, Afzal Badshah, Saeed Ullah Jan, Abdulrahman A. Alshdadi, Ali Daud
year: 2020
doi: 10.1109/RpJC.2020.DOI
date_processed: '2025-07-02'
phase2_processed: true
original_folder: arxiv_2004.06809_Issues_and_challenges_in_Cloud_Storage_Architecture_A_Survey
images_total: 6
images_kept: 5
images_removed: 1
tags: 
- Cloud Computing
- Data Integration
- IoT
- Machine Learning
- Privacy
keywords: 
- block-chain
- cloud computing
- fog computing
- heterogeneous data
- internet of things
- real-time
- self-driving
- state-of-the-art
---

**Received**: 1 April 2020; **Revised**: 7 Jun 2020; **Accepted**: 8 Jun 2020; **Published Online**: 10 June 2020 *Researchpedia Journal of Computing, Volume 1, Issue 1, Article 6, Pages 50–65, Jun 2020*

*Digital Object Identifier 10.1109/RpJC.2020.DOI Number*# Issues and challenges in Cloud Storage Architecture: A Survey
**Anwar Ghani<sup>1</sup> , Afzal Badshah<sup>1</sup> , Saeed Ullah Jan<sup>2</sup> , Abdulrahman A. Alshdadi<sup>3</sup> and Ali Daud<sup>3</sup>**<sup>1</sup>Department of Computer Science & Software Engineering, International Islamic University Islamabad, 44000, Pakistan (e-mail: anwar.ghani@iiu.edu.pk, afzal.phdcs120@iiu.edu.pk)

<sup>2</sup>Department of Computer Science & IT, University of Malakand, Chakdara, 18800, Pakistan (e-mail:saeedullah@uom.edu.pk)

<sup>3</sup>Department of Information Systems and Technology, College of Computer Science and Engineering, University of Jeddah, Saudi Arabia (e-mail:

alshdadi@uj.edu.sa, ali\_msdb@hotmail.com)

Corresponding author: Anwar Ghani(e-mail: anwar.ghani@iiu.edu.pk).

# ABSTRACT

[ From home appliances to industrial enterprises, the Information and Communication Technology (ICT) industry is revolutionizing the world. We are witnessing the emergence of new technologies (e.g, Cloud computing, Fog computing, Internet of Things (IoT), Artificial Intelligence (AI) and Block-chain) which proves the growing use of ICT (e,g. business, education, health and home appliances), resulting in massive data generation. It is expected that more than 175 ZB data will be processed annually by 75 billion devices by 2025. The 5G technology (i.e. mobile communication technology) dramatically increases network speed, enabling users to upload ultra high definition videos in real-time, will generate a massive stream of big data. Furthermore, smart devices, having artificial intelligence, will act like a human being (e.g, a self-driving vehicle etc) on the network, will also generate big data. This sudden shift and massive data generation created serious challenges in storing and managing heterogeneous data at such a large scale. This article presents a state-of-the-art review of the issues and challenges involved in storing heterogeneous big data, their countermeasures (i.e, from security and management perspectives), and future opportunities of cloud storage. These challenges are reviewed in detail and new dynamics for researchers in the field of cloud storage are discovered.
**Keywords**Internet of Things, Cloud Computing, Storage Architecture, Cloud Security, Cloud Data Management

### I. INTRODUCTION

]

The recent advances and development in smart technology is getting more attention and attraction, resulting in a massive data generation. The 75 billion devices forecast is a big number; even ten times greater than the whole world population [\[1\]](#page-13-0). These devices will increase the annual size of the global data-sphere up to 175 ZB [\[2\]](#page-13-1), [\[3\]](#page-13-2). Another report states, as shown in Fig. [1,](#page-1-0) that more than 331 billion dollars will be invested in cloud up to 2023 [\[2\]](#page-13-1). This development not only requires special infrastructural improvements but also special techniques to process and store the incoming data [\[4\]](#page-13-3). Furthermore, integrating Artificial Intelligence (AI) in smart devices makes the data storage process more complicated. This big data expectation increases the need for cloud storage and related challenges to be explored. Fig. [1](#page-1-0) shows the devices and revenue forecast of cloud computing [\[2\]](#page-13-1).

Today more embedded devices joined the Internet to monitor and connect everything (e.g, traffic facilities, buildings, environment, and lakes), enlarging the size of the data generation [\[5\]](#page-13-4)–[\[9\]](#page-13-5). As the data on the Internet is increasing day by day, therefore, analyzing and storing it through traditional data management method is a great challenge [\[10\]](#page-13-6), [\[11\]](#page-13-7) . However, researchers are struggling to design new kinds of databases based on NoSQL for handling unstructured data at such a large

![](_page_1_Figure_1.jpeg)
<!-- Image Description: The image displays a line graph showing the growth of "Devices" and "Investment" from 2017 to 2023. The Investment line exhibits exponential growth, significantly surpassing the slower, linear growth of Devices over the same period. The graph's purpose is to illustrate a disparity in growth rates between investment in, and the number of, devices within a specific sector (not specified in image). -->
**FIGURE 1.** The cloud devices and revenue forecost.

<span id="page-1-0"></span>![](_page_1_Figure_3.jpeg)
<!-- Image Description: This diagram illustrates cloud storage architecture. Multiple virtual machines (VMs) sit atop servers, which in turn rely on underlying physical storage units. The image uses icons to represent VMs, servers, and physical storage, visually depicting the layered abstraction of cloud storage. A caption explains that cloud storage offers virtual resources with remote accessibility, citing examples like iCloud, OneDrive, and Google Drive. -->

<span id="page-1-1"></span>**FIGURE 2.** Structure of cloud storage.

scale [\[12\]](#page-13-8)–[\[14\]](#page-13-9). There are many proposals in the literature for a universal storage architecture which supports multiple data models at the same time and can store big heterogeneous data in the cloud environment [\[15\]](#page-13-10)–[\[18\]](#page-13-11). Fig. [2](#page-1-1) shows the structure of cloud storage.

With the advent of technology, computing requirements of organizations grew exponentially prompting the organization to incorporate more computing and storage resources [\[19\]](#page-13-12) [\[20\]](#page-13-13). Setting up systems at such large scale require more efforts and heavy investments prompting the enterprise customers to outsource their computing and storage resources [\[21\]](#page-13-14)–[\[24\]](#page-13-15). The users have no full control over the computing resources available through cloud over the Internet [\[25\]](#page-13-16), [\[26\]](#page-13-17). Storage in the cloud is becoming a hot research venue today because new applications are data intensive which doubles storage capacity requirement as well as data usage every year. It prompted some commercial organizations to work for another cloud service called as "on

![](_page_2_Figure_1.jpeg)
<!-- Image Description: The image is a diagram illustrating a distributed data storage system architecture. Multiple consumers access data via the internet, connecting to a master node within a storage service provider's cloud. The master node manages access to numerous data nodes, each storing a portion of the data. The diagram visually represents the data flow and system components, clarifying the system's distributed nature and data redundancy. -->

<span id="page-2-0"></span>**FIGURE 3.**Master and data node in cloud storage architecture.

demand storage". Currently, the storage providers are fixated towards other aspects related to cloud storage like cost issues, performance issues and incorporating multiple storage [\[27\]](#page-13-18) [\[28\]](#page-13-19) [\[29\]](#page-13-20) [\[30\]](#page-13-21). Fig. [3](#page-2-0) shows the structure of master and data node in cloud storage architecture.

The models of data centers in cloud computing are based on "design-for-failure" principle. Provisioning of global storage services require, cloud storage must use scalable, cheaper and purposed built solutions. Such solutions may include different hardware like, servers, networking equipment, and storage systems. It should use standard delivery models on massive economies of scale. "off-the-shelf" products designed for the traditional IT market may not be suitable to use in cloud data centers since they are not only expensive but also they do not meet the specific requirements of cloud data center environment.

This study explores the cloud storage architecture its challenges and possible solutions. Additionally the cloud storage future and opportunities. Cloud storage issues include but not limited to Security, Confidentiality, Data Dynamics, Integrity, Data Access, Data Segregation, Authentication and Authorization, Data Breaches, Backup Problem and vulnerabilities in Virtualization.

Rest of this article is structured as follows: Section [II](#page-2-1) provides an insight into the issues related to cloud storage and their countermeasures. Section [II](#page-2-1) discusses the future opportunities of cloud storage. Finally, section [IV](#page-12-0) concludes the article with the key findings and future directions.

## <span id="page-2-1"></span>II. CLOUD STORAGE CHALLENGES AND POSSIBLE SOLUTIONS

Storage in a cloud is a crucial part of the Infrastructure as a Service (IaaS). The lack of proper storage management in cloud environment, may lead to severe consequences [\[31\]](#page-13-22). Cloud storage related issues have been categorized as data security and data management issues [\[32\]](#page-13-23), [\[33\]](#page-13-24). This paper focuses on issues related to these two categories and a review of possible solutions to such issues. Some of the points may overlap both categories, however, this distinction may help in understanding the challenges faced by cloud storage providers and tenants. Fig [4](#page-3-0) shows the challenges in cloud storage architecture. The following subsections elaborate these issues and their counter measures.

## *A. DATA SECURITY ISSUES*

Data security is an important requirement from tenant as a right. Secure services attract users to store their data in a cloud. Companies providing the cloud storage services are searching for techniques that can control access to cloud data and improve security. With increase in size of the data, there is also an increase in data attacks and interceptions. The cloud computing provides storage services as a vitalized environment where a user has no control over the data [\[34\]](#page-13-25). In such situation, a user may ask questions like "where exactly is my data located?", "what happen if I delete my data?" and "is the deleted data really deleted?".

![](_page_3_Figure_1.jpeg)
<!-- Image Description: The image is a hierarchical tree diagram categorizing cloud storage issues. "Cloud Storage Issues" branches into "Data Security Issues" and "Data Management Issues." "Data Security Issues" further subdivides into data integrity, confidentiality, access, authentication/authorization, and breaches. "Data Management Issues" branches into data dynamics, segregation, virtualization vulnerabilities, backup issues, availability, and data locality. The diagram visually organizes and clarifies various aspects of cloud storage challenges for the paper's discussion. -->

<span id="page-3-0"></span>**FIGURE 4.**Cloud storage challenges.

Many solutions to data security in cloud can be found in literature. Authors in [\[34\]](#page-13-25) divided the security solutions into four layers (i.e. availability, authentication, confidentiality and integrity). They argued that if confidentiality is achieved, it automatically ensures integrity. However, this sub section is dedicated to a more elaborate study of the issues related to data security. A recent study exploring data security and privacy in cloud storage [\[31\]](#page-13-22) pointed out the three main reasons based on the features of cloud computing independent of the technology being used on the server. It includes outsourcing and multitenancy.

A Time Stamp Authority (TSA) and Public Key Infrastructure (PKI) technologies are introduced into the cloud storage system for authentication and security with minimum cost and less system overhead. Trusted time stamp helps in audit and recording [\[19\]](#page-13-12), [\[35\]](#page-13-26)–[\[37\]](#page-13-27). The three points considered are User Identification, Time Stamping and User Verification through cloud storage system. The use of PKI improves security whereas authentication is done through directory services. The use of a time stamp provides security services like audit and evidences with a very minimum overhead. TSA also performs data management and optimization in cloud storage system. The workload is increased by TSA and client communication and the verification of users' operations. As during the communication process no certificate is used so extra overhead is not involved. The operation commands are converted into time stamp and sent to TSA server, which communicates with directory server and verify certificate. On validating the certificate, a time stamp is issued. The corresponding time stamp is then sent to the cloud and further operations may be performed. The cloud system stores the time stamps and operations record. The operations may

## <span id="page-4-0"></span>TABLE 1. Basic approaches used in designing data security techniques

| | Public Key Inscription | Low cost/system overhead | | |
|---------------|------------------------|--------------------------------------|--|--|
| Data Security | Trusted Timestamps | Auditing, recording, data management | | |
| | Directory Services | Authentication, verification | | |

be queries, downloads and uploads etc. The basic approaches used in designing data security techniques are shown in Table [1.](#page-4-0) Furthermore, AI, 5G, IoT and block chain are improving the privacy and security [\[38\]](#page-13-28).

### 1) Confidentiality Issues

Cloud storage is a collection of storage servers on which multiple customers' data is stored, which makes privacy a major concern. The fundamental requirement for confidentiality of the information stored or processed in the cloud is the guaranteed protection of confidential or sensitive information. Based on the requirements of a specific scenario, this may relate to all or part of the externally stored data, the identity of the users who have access to the data or the actions that the users take on the data cite t05. Encryption techniques are used to achieve confidentiality in such systems. Cloud computing is a technology that uses the internet and servers to maintain and manage data and applications. Cloud computing has improved computing capabilities without large investments.

In the existing situation in order to avoid confidentiality issues, the system may want to implement encryption and decryption techniques [\[39\]](#page-13-29) which lead to limited system operations and the user must know encryption decryption Keys. Some systems may implement both encryption and obfuscation depending on the type of data to be stored [\[34\]](#page-13-25).

A system based on proxy encryption, which supports various functions during the distributed storage system, is proposed in cite p38, p55, which consists of four stages: 1) system configuration, 2) data storage, 3) data transfer and 4) data recovery. An RSA-based algorithm is used to generate keys. The solution is when a sender " A " wants to send a message to recipient " B ", " A " signs the message with his secret key and then encrypts it with the public key of " B " and downloads the encoded text. After retrieving the message, " B " decrypts it with its public key and then checks the public key sign " A ". The whole process involves two communication stages; a download from the sender " A " and download by the recipient " B ". This is why the proxy recording scheme is used to reduce the overhead of the data transfer function in the secure storage system. Here are some crucial points regarding data privacy in a cloud storage environment.

- 1) In a cloud computing paradigm confidentiality of governmental and business information as well as privacy of personal information has the highest insinuations.
- 2) The level of confidentiality and privacy of a user depends upon the privacy policies and terms of service provided by a cloud provider.
- 3) Disclosure of information to a cloud provider by a user may change information of some specific types as well as certain user categories, rights and obligations of privacy and confidentiality.
- 4) Personal and business information may be adversely affected in terms of legal status protection.
- 5) Protecting confidentiality and privacy and the privacy rights of those processing and storing this information in a cloud environment may be highly affected by the location of information.
- 6) A cloud may store information at different venues with different legal implications leading to different legal consequences at the same time.
- 7) Different laws against criminal activities and other matters can oblige/force a provider to disclose or examine user records for the sack of evidence.
- 8) In addition to the legal protection for protecting a user's privacy and confidentiality, various legal qualms resist against gauging an information in a cloud for its status.

### 2) Integrity Issues

Data integrity is one of the most crucial elements of any system. Integrity requires that the authenticity of the parties (i.e. users and vendors) communicating in the cloud guarantee the data stored with third-party vendors and the responses resulting from the calculation of requests cite t05. In a standalone system, data integrity may be achieved with a single database using constraints and transactions. To insure integrity of the data transactions must adhere the mostly used property in databases known as the ACID (atomicity, consistency, isolation and durability) property. But distributed systems are entirely different in complexity where multiple databases and multiple applications execution is a normal trait. In a distributed environment, data may be maintained at different sites. Therefore, any transaction involving data shared by multiple sites must be handled carefully in a way to avoid transaction failure and allow various distributed applications through a resource manager to be a part of the global transaction.

With the entrance to the world of Service Oriented Architecture (SOA) and Cloud computing, issues of data integrity grow exponentially because a mixture of local and SaaS (Software as a Service) applications are displayed as a service. SaaS model supports multi tenancy in applications which usually hosted by third party and their functionality is exposed through XML based APIs (Application Programming Interface). Similarly in other environments like SOA various applications uses web services for example SOAP and REST to expose their functionality. However, managing transactions using web services is a serious challenge. Since guaranteed delivery or transactions are not supported by HTTP protocol level giving the only way out of implementing these SOA at the API level.

## 3) Data Access Issues

Issues in access to data in a cloud storage are mostly due to security policies. For example, a small level business organization may use services of a cloud provider for executing its business processes [\[40\]](#page-14-0), [\[41\]](#page-14-1). Such organizations allow their employees to access a specific organizational data according to its own organizational security policies. These policies may prevent some employees from accessing a specific set of data and allow them to access certain data. To stop intruders from gaining unauthorized access to cloud resources, a cloud must adhere these security policies [\[42\]](#page-14-2). The SaaS model must have the ability to allow organizations to integrate their security policies as well as keep organizational data within its boundary in case when multiple organizations use the same cloud environment. The requirement of availability is; there must be a mechanism for verification of Service Level Agreements (SLA) between a user and providers which verifies that the user's requirements are fulfilled [\[43\]](#page-14-3).

Many counter measures proposed in the literature can be found to mitigate the problems related to data access in cloud storage. In literature three categories of secure access control can be found (i.e. Role Based Access Control (RBAC), User Based Access Control (UBAC) and Attribute Based Access Control (ABAC)) [\[44\]](#page-14-4), [\[45\]](#page-14-5). Due to the attachment of access control list (ACL) to user data, UBAC is usually not considered as a suitable candidate for cloud storage. Additionally, the involvement of Big Data the computational and communication overhead required for handling ACL is high [\[46\]](#page-14-6). Then there is role based classification of users to control access to data. A user matching a specific role is granted access to data. Such approaches are considered suitable for business organizations at enterprise level for example hospitals [\[47\]](#page-14-7). The third and often used category in cloud storage is Attribute Based Access Control (ABAC) where a data owner assigns attributes and policies to users and data respectively [\[48\]](#page-14-8). In this case access to the data is granted to users having attributes that satisfy a specific access policy. For a confidential fine-grained access to data in cloud, this category is further divided into two approaches i.e. KP-ABE [\[35\]](#page-13-26), [\[49\]](#page-14-9) and CP-ABE [\[50\]](#page-14-10)[13]. In case of KP-ABE the key of a user is linked with an access policy whereas attributes are linked with ciphertext. In contrast to KP-ABE, in CP-ABE the key of a user is linked with an attribute whereas the ciphertext is linked with an access policy.

However, the complexity of attribute based access control techniques grows linearly, as the number of attributes used in decryption raises, incorporating tremendous overhead in computation specially for devices with limited resources like mobile devices [\[41\]](#page-14-1).

## 4) Authentication and Authorization Issues

Authentication, in any system that needs a foolproof security, plays a crucial role like an entrance door that allows only trusted individuals, to the premises of a cloud. Access to important information depends on authentication, therefore, due to it's sensitive nature, authentication process must be robust to ensure availability to authentic users. In combination with cryptography, not only data confidentiality, but also its integrity can be ensured by granting access only to authenticated individuals. Most of the security concerns can be mitigated through a sophisticated authentication mechanism [\[39\]](#page-13-29), [\[51\]](#page-14-11), [\[52\]](#page-14-12).

A Lightweight Directory Access Protocol (LDAP) server is used by various companies to store information about their employees [\[53\]](#page-14-13). Managing users in small and medium size businesses is mostly achieved through Active Directory in the portion of business where the adoption of SaaS model is high (Microsoft White Paper, 2000). This model allows software to be hosted outside the organizational firewall. Many organizations separate user credential database from their IT infrastructure therefore, a customer must keep track of all the employees joining or leaving the organization and must enable or remove their accounts accordingly from the system. This may result in extra management overhead on the customer organization if it uses multiple SaaS products. In such cases different powers can be delegated to the customer by the provider, authentication for example enabling customer organizations internal LDAP/AD server to control their user management.

## 5) Data Breaches

A cloud environment is usually shared among many customers to store their data. Therefore, a compromise of the cloud environment means a potential threat to the data of all users making cloud an attractive target for attackers [\[40\]](#page-14-0). R. Cooper in his report [\[54\]](#page-14-14) rated external criminals as the highest threat contributing 73% but with least impact compromising 30,000 records producing 67,500 Pseudo Risk Score (PRS). Similarly, insider threats received the minimum rating of (18%) but with greatest impact compromising 375,000 records with a PRS of 67,500. The middle rating has been received by partners with 73.39% compromising 187,500 with a PRS of 73,125. The security provided by SaaS is argued to be better in comparison to conventional means, however insiders may not have direct database access but it still raises a risk with huge impact on data security. Employees of SaaS providers can cause exposure of customers private information since they have access to a lot of information. In order to avoid such complications, standards like PCI-DSS (Payment Card Industry-Data Security Standards) must be followed by SaaS providers.

## *B. DATA MANAGEMENT ISSUES*The management issues related to data has been explored in this sub sections. The data management issues has been categorized and briefly explained as follows.

## 1) Data Dynamics Issues

Data management in cloud is considered to be untrustworthy due to the fact that it shifts databases as well as application software to large centralized data centers. This new paradigm introduces various security issues yet to be understood. Data dynamics support through operations in cloud for example insertion, block modification, and deletion is a huge step in the direction of practicality as cloud services are not restricted only to backup and archiving. The following different methods are used for the assurance of data dynamics in cloud storage [\[55\]](#page-14-15), [\[56\]](#page-14-16).

- On a large scale the data centers are being transformed into computing pools by "Software as a Service" (SaaS) computing architecture. In addition the fast growth in network resources like bandwidth and reliability enables customers to subscribe services with high quality from the remote data and software applications in data centers.
- A cloud service provider for his own benefits may conceal errors in data or software used by the clients. For example a provider may deliberately delete data of an ordinary client which is accessed less often without the client's knowledge in order to increase his savings in money and storage space [\[55\]](#page-14-15).
- For data dynamics various schemes have been designed with the efforts to combine efficiency, unlimited use of queries and information retrievablity in these schemes.

One possible solution in this case could be to motivate public auditing system of data storage security in Cloud computing [\[37\]](#page-13-27). In addition, fully dynamic protocols for data operations specially for block insertion, must be designed which is a lacking feature in most of the existing approaches. To support public auditing which is efficient and scalable, the existing schemes must be extended. Such extension should achieve batch auditing enabling a third party auditor (TPA) to perform auditing tasks delegated from multiple users simultaneously.

## 2) Data Segregation Issues

Cloud computing architecture became popular because of it multi-tenancy nature [\[53\]](#page-14-13), [\[57\]](#page-14-17). Multi-tenancy in cloud through SaaS applications allow storage of data from multiple users simultaneously. This may create an opportunity for a user's data to intrude into another user's data since data of different users reside at single location. This intrusion may exploit application's

| | | | | | TABLE 2. Security solution for cloud storage architecture (Part-I) | |
|--|--|--|--|--|--------------------------------------------------------------------|--|
|--|--|--|--|--|--------------------------------------------------------------------|--|

| Security Properties | Approaches | Description | | |
|---------------------|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|--|
| Confidentiality | Cryptography | Cryptography secure and protect data during communication. It<br>is useful to block an unauthorized users from accessing private | | |
| | Digital signatures | data.<br>Digital signature is a symbolic description that can verify the<br>authenticity of messages or digital documents. A true digital<br>signature provides access to the data. | | |
| | Proxy Re-encryption | Proxy encryption is commonly used when a party wants to<br>reveal to a third party the content of messages sent to it that are<br>encrypted with their public key. | | |
| | Obfuscation | Obfuscation is the intentional creation of source code or machine<br>code that is difficult for a human to understand. Like natural<br>language eclipse, it can use unnecessarily redirected expressions<br>to make statements. | | |
| | Blockchain | Blockchain is a smart design that offers digital information for<br>sharing, but not for copying. Blockchain technology has created<br>the backbone of a new type of internet. | | |
| Atomicity | MC | Data MC is a world leader in the delivery of highly com<br>plex data migrations, specializing in end-to-end delivery of<br>industry-specific, custom and enterprise transformation ERP,<br>CRM projects. | | |
| | Consistency | The consistency of the database system refers to the fact that<br>the database transaction can only be modified in an authorized<br>manner. | | |
| | Isolation | Isolation in database systems determines, how the integrity of<br>activities are visible to other users and systems. | | |
| | Durability | In database systems, sustainability is the ACID property that<br>ensures that closed transactions persist. | | |
| Data Access | Role Based Access Control | RBAC is an entrance approach to regulate access to the system<br>to authorized users. It is used by most companies with more than<br>500 employees and can implement mandatory access control<br>(MAC) or discretionary access control (DAC). | | |
| | User Based Access Control | Role-based access (or role-based permissions) adds another cat<br>egorization layer in addition to what is provided by user-based<br>access. | | |
| | Attribute<br>Based<br>Access<br>Control | Attribute-based access control (ABAC) is also called as policy<br>based access control, defines an access control that give access<br>rights to users through the use of policies that combine attributes. | | |
| Data Breaches | Directory Services | A Lightweight Directory Access Protocol (LDAP) server is used<br>to provide authentication and authorization services | | |

loopholes or by injecting SaaS system with malicious client code. If an application injected with a masked code executes it without verification shows that there are high possibilities of intrusion into others data. Therefore, a SaaS model must ensure that the data of each user is bounded both at physical and application levels. Data from different users must be ghettoise intelligently by the SaaS service [\[58\]](#page-14-18).

Security checks may be bypassed using vulnerabilities in application by attackers through handcraft parameters. This may lead to the exposure of other tenants sensitive data. Therefore different assessments test must be performed to ensure that data from different users in multi-tenant environment is fully segregated from each other. These tests include; i) Data validation, ii) SQL injection flaws and iii) Storage insecurity. Any possible flaws detected by these tests could be used to illegally access sensitive data of the enterprise or other tenants.

| | | | | | TABLE 3. Security solution for cloud storage architecture (Part-II) | |
|--|--|--|--|--|---------------------------------------------------------------------|--|
|--|--|--|--|--|---------------------------------------------------------------------|--|

| Security Issue | Solution | Description |
|-----------------|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Data Dynamics | Public Auditing | Efficient and scalable public auditing system should be intro<br>duced to extend the existing schemes |
| Data validity | Data Segregation | Security<br>layers<br>give<br>you<br>the<br>flexibility<br>to<br>consolidate<br>vast<br>amounts of data while controlling who can see what, through a<br>sophisticated system of work groups, organizational rollups, and<br>access levels, combined with field and function level security. |
| Virtualization | Root Security | Root protection enables users (e.g. smartphones, tablets) with |
| Vulnerabilities | | the android mobile operating system to get privileged control<br>(known as root access) over different Android subsystems |
| Backup Issues | Encryption schemes | Different encryption schemes coded the data before storing. This<br>secure the backup data from unauthorized users. |
| Availability | Multitier architecture | Multitier architecture (often referred to as multi-level architec<br>ture) or multi-layer architecture is a client-server structure in<br>which the functions of presentation, application processing and<br>data management are separated. |
| | Load Balancing | Running on different servers, resilient to software and hardware<br>failure, and be protected against DOS and DDOS attacks |
| Data Locality | Regional backup servers | Due to the different, region cyber rules, data should be kept in<br>the same region servers to avoid data locality, cultural and cyber<br>rules issues. |

### 3) Virtualization Issues and Vulnerability

One of the major component of cloud environment which ensures that various instances running over a single machine be ghettoise from each other is known as virtualization. It is the source of major security challenges in a cloud environment which are not fully investigated today [\[59\]](#page-14-19), [\[60\]](#page-14-20). Second issue is the administrative control of the operating systems, operating as guest and host systems and their imperfect provisioning of isolation [\[61\]](#page-14-21) and scalability issues [\[62\]](#page-14-22). Many of the current Virtual Machine Monitors (VMM's) suffer from bugs allowing escape from VM therefore, "root security" is mandatory in such cases to prevent host operating system from being interfere with by any virtualized guest systems. Some virtualization software has been reported to have vulnerabilities which could allow a local user or an attacker to skip certain security checks and gain illegitimate access [\[61\]](#page-14-21), [\[63\]](#page-14-23). One such example is that of Microsoft Virtual Server and Virtual PC vulnerability where a user of guest operating system could be allowed to execute code on other guest operating system or even the host operating system itself. This could allow a raise in privileges which can lead to unauthorized access of sensitive information. Similarly a validation error in "tools/pygrub/src/GrubConf.py" of Xen which could allow a user with "root" access in a guest operating system through specific crafted contents in grub conf to use domain 0 for running various commands at booting time of guest operating system. Fully functional interposition, inspection and complete isolation are not achieved in VMMM yet and need further investigation.

### 4) Backup Issues

The sensitive data belonging to various business enterprises must be backed up by the SaaS providers to be used for fast recovery in disasters cases. Also, to protect against security threats like accidental leakage of data various encryption schemes be used to protect the back up data. These encryption schemes must be strong enough to resist modern attacks.

Amazon as cloud vendor does not encrypt the data by default at rest in S3. This control is given to the user to secure their back up data separately in order to protect against unauthorized access or tempering. Various tests can be performed to validate that a back up data is secure provided by SaaS model. These tests include; i) Storage insecurity and ii) Configuration insecurity. Any flaws identified by these tests may be potential threats which can lead unauthorized users to access information which is sensitive and stored in cloud backups belonging to different enterprises.

### 5) Availability

The SaaS applications guarantee around the clock services to a client. This involves architectural level changes in SaaS infrastructure and applications to attain availability and scalability. Multitier cloud architecture needs to be adopted, cloud architecture must also support load balancing of application instances, running on different servers. Cloud storage must be resilient to software and hardware failures further, it must be protected from both distributed denial of service attacks (DDOS) as well as denial of service DOS attacks [\[64\]](#page-14-24)–[\[67\]](#page-14-25).

For any unforeseen disaster, appropriate disaster recovery and operational sustainability action plan should be considered. This is important for certifying organizational data security and organizational nominal downtime. For example, at Amazon, the AWS API endpoints are hosted by the same world-class Internet infrastructure that Amazon supports and use connection throttling. To further reduce the potential impact of a DDOS attack, Amazon internally maintains the bandwidth that surfs on its vendor's internet bandwidth to validate the SaaS vendor's availability and evaluation tests.

Many applications automatically provide security locks for user accounts after successive incorrect credentials. Also, improper implementation and configuration of these functions can be vulnerable to malicious users as a result of DDOS attacks.

### 6) Data Locality

In SaaS cloud model, a client uses the application provided by the SaaS and their own business data, but the client is unaware of storage location of the data in the cloud [\[42\]](#page-14-2), [\[68\]](#page-14-26). This may lead to several issues and many cases. For example, due to data privacy laws in different counties, data locality is of utmost importance in enterprise business architecture. For instance in many Southern American States and several countries in European Union, certain types of data may not be allowed to leave the country premises because of the sensitivity of the information. Similarly local GovernmentâA˘ Zs laws and jurisdiction issues ´ may arise in case of any type of investigation [\[69\]](#page-14-27). A secure SaaS model may be capable to provide reliability to its clients at the consumer data locality.

### III. CLOUD STORAGE FUTURE AND OPPORTUNITIES

The future of the cloud is not less than a dream. AI-enabled objects (e.g, self-driving vehicle), the web of IoT devices, and 5G connectivity (i.e, mobile communication technology) is changing the way of living [\[3\]](#page-13-2). The IT industry is rapidly changing everything. Its simple and easy user interface; no cost and capacity constraints; and other numbers of features are attracting the individual and market [\[70\]](#page-14-28). The opportunities of cloud storage is listed in Fig [5.](#page-10-0)

The recent advances in smart technology generate a massive data traffic. The 51 billion devices forecast is a big number; even seven times greater than the whole world population [\[1\]](#page-13-0). These devices will increase the annual size of the global data-sphere up to 175 ZB [\[2\]](#page-13-1), [\[3\]](#page-13-2). Another report states, as shown in Figure [1,](#page-1-0) that more than 331 billion dollars will be invested in cloud up to 2023 [\[2\]](#page-13-1). It needs special techniques and infrastructure to process the incoming data [\[4\]](#page-13-3). Furthermore, integration of Artificial Intelligence (AI) in smart devices increases the data production value dramatically. With this rapid development in smart technology, cloud storage is getting more and more attention. Along with the AI, block-chain is adding safety and security to the cloud storage. This technology in storage is getting mature and will increase the customer trust on cloud. Furthermore, data compression is playing a good role in data archives by reducing the size of data storage on storage devices.

This section presents a quick review of the cloud storage future and its opportunities [\[42\]](#page-14-2), [\[71\]](#page-14-29)–[\[79\]](#page-14-30).

### *A. REMOTE ACCESSIBILITY*

Remote accessibility (i.e, access from everywhere and anytime) is the core of cloud storage. The fast network speed and AI is making it more smarter and faster. Leading cloud provider (i.e, Apple iCloud [\[80\]](#page-14-31), Microsoft OneDrive [\[81\]](#page-14-32), and Google Drive [\[82\]](#page-14-33) etc) are providing fast and reliable remote services to their users. Remote access allows to store and retrieve items from a cloud storage without needing to create a physical connection. Accessibility of storage devices is getting interested after introducing high storage devices and high bandwidth network. Remote access increases the usage of cloud storage and business. In the presence of internet services, cloud storage can provide seamless access to data files [\[72\]](#page-14-34). The coming 5G internet service will make the accessibility very easy and smart as real-time access [\[83\]](#page-14-35).

![](_page_10_Figure_1.jpeg)
<!-- Image Description: This diagram illustrates the opportunities presented by cloud storage. A central cloud, labeled "Cloud Storage Opportunities," connects to seven surrounding clouds, each representing a benefit: remote accessibility, usability, disaster recovery, cost savings, sharing and collaboration, automation and synchronization, and privacy and security. Invisibility is also listed as a benefit. The diagram visually summarizes the advantages of utilizing cloud storage technology. -->

<span id="page-10-0"></span>**FIGURE 5.**Opportunities of cloud storage

## *B. 5G CONNECTIVITY*With this high-speed technology, humans will be able to virtually operate any machine at a distance of thousands of KMs [\[84\]](#page-14-36). This will reduce the latency of up to 0 ms. Such a big speed will minimize the need for the local hard drive. This technology will able to store and process data on the cloud without facing any jitters or delay. It is making real-time use possible. 5G is a new era of cloud storage [\[85\]](#page-15-0), [\[86\]](#page-15-1).

## *C. INTERNET OF THINGS (IOT)*With the introduction of the Internet of Things (IoT), the number of devices connected to the internet has increased enormously. By 2025, 75 billion devices are expected to be connected to the Internet processing 75 ZB data annually. This is a great number and will need a high technology to process and store this data. These figures clearly shows that the cloud storage has great worth in coming years. Furthermore, the use smart devices are also dramatically increasing. These devices are small in size and have not enough space to store or process big data therefore, they depend on cloud [\[87\]](#page-15-2).

## *D. ARTIFICIAL INTELLIGENCE (AI)*From facial expressions to self-driving vehicles, AI is progressing very rapidly. AI is making smart decisions in complex situations. The today AI is called the weak AI which performs limited tasks such as recognizing facial expression and driving a car, however, the future will have general AI which will perform a task just like human beings. The AI is making the cloud storage further smarter and attractive [\[88\]](#page-15-3). Furthermore, the use of block-chain in storage is making it more secure [\[89\]](#page-15-4).

## *E. USABILITY*The provider business directly depends on resources utilization. Today technologies massively increase the cloud usage because it provides a very easy and reliable user interface. Usually, cloud storage has a local desktop folder for PCs and mobile devices which allows users to move files back and forth between the cloud and the local system using drag and drop facilities [\[42\]](#page-14-2), [\[72\]](#page-14-34), [\[76\]](#page-14-37). The integration of smarts technologies (i.e, IoT, AI, fog and 5G), making the cloud storage usability very easy. The 5G will provide a high bandwidth like real-time access. Its cost is very low compared to buy the devices; which is very appealing [\[83\]](#page-14-35).

## *F. DISASTER RECOVERY*In today modern world, data is the most valuable asset. Losing it, cause irreversible damage to the business (including loss of productivity, income, reputation and even customers). Business enterprises use cloud storage as a backup for their important files. In cloud storage, data is stored in three different locations and in case of any disaster, data may easily be recovered. Furthermore, cloud storage provides remote access to files therefore, these files can be used for recovery of their system in case any emergency or disaster [\[42\]](#page-14-2). 5G technology made the recovery process very easy and fast. Comparatively to the traditional disaster recovery, cloud storage recovery is very easy, cheaper and fast. High investment, staff and maintenance are required for local disaster recovery site .

## *G. COST SAVINGS*When we talk about cloud, it means that we are getting the resources of a supercomputer at our home without buying it. We actually, hire these resources on very cheaper rates which save the capital investment of the consumer. Cloud storage is used by various types of business enterprises to reduce their annual database operation expenses. Especially, the medium corporations, which are not able to invest too much on storage infrastructure, hire the cloud storage. This saves their major investment. Storing one gigabyte of data using cloud storage services cost about three whereas a user can achieve further saving in terms of power consumption as remote cloud storage does not need internal power [\[77\]](#page-14-38), [\[78\]](#page-14-39). Cloud storage saves operational and maintenance cost and just as per their usage.

## *H. INVISIBILITY*The word storage create the imagination of a big physical device to store big data. Big data and storage mean a big physical device, which will need operation and maintenance. However, cloud storage does not need physical space and user access it remotely [\[90\]](#page-15-5). Cloud storage services, use virtualization techniques to provide resources to the customers. Customers do not know the complexities and working of the back end. Cloud storage is invisible and provides storage transparency, with no physical presence on the user side. It does not take up valuable space in the office or at home. It does not need to spare a huge space for rocks and storage. Customers only hire the services and use them on the go.

## *I. PRIVACY AND SECURITY*Security of cloud storage for sensitive and confidential information is usually higher than that for the locally stored data, especially for enterprises. It uses advance security (i.e, advanced firewalls, event logging, internal firewalls, intrusion detection, data replication, encryption, and physical security) to protect the data from outside attacks. Different type of security layers is used to protect the data houses. Concerning individual storage, enterprises invest more in security. Storage services in the cloud used encrypted data both in transmission as well as at rest ensuring no unauthorized access to data files. AI, 5G, IoT and block chain are improving the privacy and security [\[38\]](#page-13-28).

### *J. AUTOMATION AND SYNCHRONIZATION*Cloud automation is a term for the processes and tools that are used to reduce the manual effort involved in provisioning and managing cloud workloads. The cloud storage is self managed and does not need any human efforts [\[91\]](#page-15-6). The main issue most businesses and customers have, the proper follow up of data backup. Cloud storage provides an automated data backup service to ease this tedious process. A user simply needs to tell the system what and when to back up, and the cloud service takes care of it by itself.

Another attraction with the cloud storage is automatic synchronization. Synchronization process ensures that user data files are automatically updated across all of the user devices. In this way the latest versions of the user's data files are saved on his/her local device and available on all of other user devices like user Smartphone etc. 5G made the syncing more easy and now the devices works on real time [\[91\]](#page-15-6).

## *K. SHARING AND COLLABORATION*Cloud storage makes the sharing easy. Either it is a photo or a file or even a folder containing hundreds of information files, storage service in cloud make it convenient for a user to share it with a few clicks. Furthermore, it makes the files availability everywhere and every time [\[92\]](#page-15-7). Online cloud storage services are also ideal for collaboration purposes. It allows multiple users to collaborate and edit on a single document or data file. User do not have to concern about tracking the up-to-date version or who has made what changes [\[72\]](#page-14-34).

## *L. MASSIVE DEVICES AND DATA*

As mentioned earlier, up to 2025, approximately 75 billion devices will connect to the internet and this will process more than 175 ZB of data per year. This is a very large figure and requires a lot of cloud storage. These predictions will drastically change the need for cloud storage. This shows that cloud storage has a very bright future ahead.

## <span id="page-12-0"></span>IV. CONCLUSION AND FUTURE DIRECTIONS

The recent advances in IT industry (e.g, Cloud computing, Internet of Things (IoT), Fog computing, Artificial Intelligence (AI) and Block-chain) is rapidly revolutionizing the cloud storage. Especially, the 5G facilitation (i.e, minimum access delay and ultra high speed) boost the use of cloud storage dramatically. This article presented different challenges, their counter measures, opportunities and future of cloud storage. it seems that cloud storage is designed to be highly scalable and conveniently manageable storage system rather than an efficient file system.

Further, it is revealed that despite the ease of use and economic benefits, cloud storage technology still suffers from numerous problems. The cloud storage architecture is mostly clouded by security (e.g, confidentiality, integrity, access, authentication, authorization and data breaches) and data management issues (e.g, dynamics, data segregation, backup, and virtualization). To counter these threats, various measures are proposed in the literature. For example, for the security of data, digital certificates are used along with a trusted timestamp approach. Similarly, confidentiality is ensured through cryptography solutions while for data access issues, attribute-based encryption is mostly used. Access control is achieved through authentication and authorization. To maintain the integrity of the data, a global transaction manager is used to ensure fail-safe management of transaction across multiple databases.

Finally, it can be concluded that cloud computing (along with the integrated technologies) is a fast-growing technology which rapidly changing traditional computing. However, still, a lot of research efforts are needed to attract customers, especially business and enterprise customers to store their sensitive data, using cloud storage.

### REFERENCES

- <span id="page-13-0"></span>[1] G. Davis, "2020: Life with 50 billion connected devices," in IEEE International Conference on Consumer Electronics (ICCE). Las Vegas, NV, USA: IEEE, Jan 2018, pp. 1–1.
- <span id="page-13-1"></span>[2] "Forbes: Cloud computing forecast," [https://www.forbes.com/sites/louiscolumbus/2017/04/29/roundup-of-cloud-computing-forecasts2017/#5c42322c31e8/,](https://www.forbes.com/sites/louiscolumbus/2017/04/29/roundup-of-cloud-computing-forecasts2017/#5c42322c31e8/) 2020.
- <span id="page-13-2"></span>[3] S. Kinza, K. Bilal, S. Farah, Q. Sameer, and M. Muhammad, "Internet of things (iot) for next-generation smart systems: A review of current challenges, future trends and prospects for emerging 5g-iot scenarios," Antenna and Propagation for 5G and Beyond, vol. 8, no. 1, pp. 2169–3536, 2020.
- <span id="page-13-3"></span>[4] X. Wang, B. Wang, and J. Huang, "Cloud computing and its key techniques computer science and automation engineering (csae)," in International Conference on Cloud Computing. Shanghai, China: IEEE, 2011, pp. 404–410.
- <span id="page-13-4"></span>[5] W. Songyun, Y. Jiabin, L. Xin, Q. Zhuzhong, A. Fabio, and Y. Ilsun, "Active data replica recovery for quality-assurance big data analysis in ic-iot," IEEE Access, vol. 7, pp. 106 997 – 107 005, 2019.
- [6] S. Karen, "Iot big data security and privacy versus innovation," IEEE Internet of Things Journal, vol. 6, no. 2, pp. 1628 1635, 2019.
- [7] S. Syed Attique, Z. S. Dursun, H. Sufian, and D. Dirk, "The rising role of big data analytics and iot in disaster management: Recent advances, taxonomy and prospects," IEEE Access, vol. 7, pp. 54 595 – 54 614, 2019.
- [8] Q. Basheer, A.-F. Ala, A. Gupta, B. Driss, A. Safaa, and Q. Junaid, "Leveraging machine learning and big data for smart buildings: A comprehensive survey," IEEE Access, vol. 7, pp. 90 316 – 90 356, 2019.
- <span id="page-13-5"></span>[9] S. Rui, L. Shanyun, W. Shuo, X. Ke, and F. Pingyi, "Importance of small probability events in big data: Information measures, applications, and challenges," IEEE Access, vol. 7, pp. 100 363 – 100 382, 2019.
- <span id="page-13-6"></span>[10] B. Afzal, G. Anwar, S. Shahaboddin, A. Giuseppe, and P. Antonio, "Performance based service level agreement (psla) in cloud computing to optimize penalties and revenue," IET Communications, 2020.
- <span id="page-13-7"></span>[11] B. Afzal, S. Shahaboddin, G. Anwar, and C. Anthony, "Optimizing iaas provider revenue through customer satisfaction and efficient resource provisioning in cloud computing," IET Communications, vol. 13, no. 9, pp. 2913–2922, 2019.
- <span id="page-13-8"></span>[12] A. Ankita, V. Gregory, H. Seghbroecka, F. Morab, T. De, and V. Bruno, "Spech: A scalable framework for data placement of data-intensive services in geodistributed clouds," Journal of Network and Computer Applications, vol. 142, pp. 1–14, 2019.
- [13] Z. Lei, F. Anmin, Y. Shui, S. Mang, , and K. Boyu, "Data integrity verification of the outsourced big data in the cloud environment: A survey," Journal of Network and Computer Applications, vol. 112, pp. 1–15, 2019.
- <span id="page-13-9"></span>[14] A. Sidra, U. Saif, K. Abid, A. Mansoor, A. Adnan, and K. K. Muhammad, "Information collection centric techniques for cloud resource management: Taxonomy, analysis and challenges," Journal of Network and Computer Applications, vol. 100, pp. 80–94, 2019.
- <span id="page-13-10"></span>[15] W.-T. Tsai, Z. Jin, and X. Bai, "Internetware computing: issues and perspective," in Proceedings of the First Asia-Pacific Symposium on Internetware. ACM, 2009, p. 1.
- [16] H. Raj, R. Nathuji, A. Singh, and P. England, "Resource management for isolation enhanced cloud services," in Proceedings of the ACM workshop on Cloud computing security. ACM, 2009, pp. 77–84.
- [17] V. Chang and G. Wills, "A model to compare cloud and non-cloud storage of big data," Future Generation Computer Systems, vol. 57, pp. 56–76, 2016.
- <span id="page-13-11"></span>[18] R. Kumar and A. K. Bose, "Internet of things and opc ua," ICNS 2015, p. 52, 2015.
- <span id="page-13-12"></span>[19] S. Kamara and K. Lauter, Cryptographic Cloud Storage. Canary Islands, Spain: Springer Berlin Heidelberg, January 25-28 2010, pp. 136–149. [Online]. Available: [http://dx.doi.org/10.1007/978-3-642-14992-4\\$\\_\\$13](http://dx.doi.org/10.1007/978-3-642-14992-4$_$13)
- <span id="page-13-13"></span>[20] J. Ateeqa, B. Afzal, and R. Tauseef, "Sla based infrastructure resources allocation in cloud computing to increase iaas provider revenue," Research Journal of Science and IT Management, vol. 4, no. 3, pp. 37–44, 2015.
- <span id="page-13-14"></span>[21] P. Paola, C. Roberto, B. Alberto, and P. Lorenzo, "Amazon, google and microsoft solutions for iot: Architectures and a performance comparison," IEEE Access, vol. 8, pp. 5455 – 5470, 2020.
- [22] T. Ye, X. Peng, and J. Hai, "Secure data sharing and search for cloud-edge-collaborative storage," IEEE Access, vol. 7, pp. 15 963 15 972, 2019.
- [23] Q. Shuaiqing, Z. Qisheng, Z. Qimao, G. Feng, and L. Wenhao, "Hybrid seismic-electrical data acquisition station based on cloud technology and green iot," IEEE Access, vol. 8, pp. 31 026 – 31 033, 2020.
- <span id="page-13-15"></span>[24] K. P. Chan and J. B. Seung, "Blockchain of finite-lifetime blocks with applications to edge-based iot," IEEE Internet of Things Journal, vol. 7, no. 9, pp. 120–133, 2020.
- <span id="page-13-16"></span>[25] A. P. Rajan et al., "Evolution of cloud storage as cloud computing infrastructure service," arXiv preprint arXiv:1308.1303, no. 1, 2013.
- <span id="page-13-17"></span>[26] R. Ghani-Ur, G. Anwar, Z. Muhammad, A. N. Syed Husnain, and S. Dhananjay, "Ips: Incentive and punishment scheme for omitting selfishness in the internet of vehicles (iov)," IEEE Access, vol. 7, pp. 109 026 – 109 037, 2019.
- <span id="page-13-18"></span>[27] V. Chang, Y.-H. Kuo, and M. Ramachandran, "Cloud computing adoption framework: A security framework for business clouds," Future Generation Computer Systems, vol. 57, pp. 24–41, 2016.
- <span id="page-13-19"></span>[28] B. Afzal, G. Anwar, Q. Ahsan, and S. Shahaboddin, "Smart security framework for educational institutions using the internet of things (iot) computers," Materials and Continua (CMC), vol. 6, no. 1, pp. 81–101, 2019.
- <span id="page-13-20"></span>[29] B. Afzal, J. Ateeqa, and R. Tauseef, "Performance based service level agreement in cloud computing," Research Journal of Science and IT Management, vol. 4, no. 4, pp. 20–31, 2015.
- <span id="page-13-21"></span>[30] G.-U. Rehman, A. Ghani, S. Muhammad, M. Singh, and D. Singh, "elfishness in vehicular delay-tolerant networks," Sensors, vol. 20, no. 10, 2020.
- <span id="page-13-22"></span>[31] N. Kaaniche and M. Laurent, "Data security and privacy preservation in cloud storage environments based on cryptographic mechanisms," Computer Communications, vol. 111, pp. 120–141, 2017.
- <span id="page-13-23"></span>[32] X. Sun, S. Qu, X. Zhu, M. Zhang, Z. Ren, and C. Yang, "Cloud storage architecture achieving privacy protection and sharing," Appl. Math, vol. 9, no. 3, pp. 1639–1644, 2015.
- <span id="page-13-24"></span>[33] L. Geng, "The research of digital library mass information storage system architecture," in International Symposium on Computers & Informatics. Atlantis Press, 2015.
- <span id="page-13-25"></span>[34] L. Arockiam and S. Monikandan, "Efficient cloud storage confidentiality to ensure data security," in International Conference on Computer Communication and Informatics. IEEE, Jan 2014, pp. 1–5.
- <span id="page-13-26"></span>[35] J. Han, W. Susilo, Y. Mu, and J. Yan, "Privacy-preserving decentralized key-policy attribute-based encryption," IEEE Transactions on Parallel and Distributed Systems, vol. 23, no. 11, pp. 2150–2162, 2012.
- [36] N. H. Hussein, A. Khalid, and K. Khanfar, "A survey of cryptography cloud storage techniques," International Journal of Computer Science and Mobile Computing, no. 5, 2016.
- <span id="page-13-27"></span>[37] C. Wang, K. Ren, W. Lou, and J. Li, "Toward publicly auditable secure cloud data storage services." IEEE network, vol. 24, no. 4, pp. 19–24, 2010.
- <span id="page-13-28"></span>[38] G. Hittu and D. Mayank, "Securing iot devices and securelyconnecting the dots using rest api and middleware," in 4th International Conference on Internet of Things: Smart Innovation and Usages (IoT-SIU). IEEE, 2019, pp. 1 – 6.
- <span id="page-13-29"></span>[39] Z. Kartit, A. Azougaghe, H. K. Idrissi, M. El Marraki, M. Hedabou, M. Belkasmi, and A. Kartit, "Applying encryption algorithm for data security in cloud storage," in Advances in Ubiquitous Networking. Springer, 2016, pp. 141–154.

- <span id="page-14-0"></span>[40] V. Chang and M. Ramachandran, "Towards achieving data security with the cloud computing adoption framework," IEEE Transactions on Services Computing, vol. 9, no. 1, pp. 138–151, Jan 2016.
- <span id="page-14-1"></span>[41] Q. Li, J. Ma, R. Li, X. Liu, J. Xiong, and D. Chen, "Secure, efficient and revocable multi-authority access control system in cloud storage," Computers & Security, vol. 59, pp. 45–59, 2016.
- <span id="page-14-2"></span>[42] S. Subashini and V. Kavitha, "A survey on security issues in service delivery models of cloud computing," Journal of network and computer applications, vol. 34, no. 1, pp. 1–11, 2011.
- <span id="page-14-3"></span>[43] P. Samarati and S. De Capitani di Vimercati, "Cloud security: Issues and concerns," Encyclopedia on Cloud Computing. Wiley, New York, 2016.
- <span id="page-14-4"></span>[44] A. Sahai and B. Waters, Fuzzy Identity-Based Encryption. Aarhus, Denmark: Springer Berlin Heidelberg, May 2005, pp. 457–473.
- <span id="page-14-5"></span>[45] E.-J. Goh, H. Shacham, N. Modadugu, and D. Boneh, "Sirius: Securing remote untrusted storage." in NDSS, vol. 3, 2003, pp. 131–145.
- <span id="page-14-6"></span>[46] J. Shen, D. Liu, Q. Liu, B. Wang, and Z. Fu, "An authorized identity authentication-based data access control scheme in cloud," in 18th International Conference on Advanced Communication Technology (ICACT). IEEE, 2016, pp. 56–60.
- <span id="page-14-7"></span>[47] L. Zhou, V. Varadharajan, and M. Hitchens, "Achieving secure role-based access control on encrypted data in cloud storage," IEEE Transactions on Information Forensics and Security, vol. 8, no. 12, pp. 1947–1960, 2013.
- <span id="page-14-8"></span>[48] S. Yu, C. Wang, K. Ren, and W. Lou, "Achieving secure, scalable, and fine-grained data access control in cloud computing," in proceedings of IEEE Infocom. IEEE, 2010, pp. 1–9.
- <span id="page-14-9"></span>[49] N. Attrapadung, J. Herranz, F. Laguillaumie, B. Libert, E. De Panafieu, and C. Ràfols, "Attribute-based encryption schemes with constant-size ciphertexts," Theoretical Computer Science, vol. 422, pp. 15–38, 2012.
- <span id="page-14-10"></span>[50] C. Hong, Z. lv, M. Zhang, and D. Feng, A Secure and Efficient Role-Based Access Policy towards Cryptographic Cloud Storage. Wuhan, China: Springer Berlin Heidelberg, September 2011, pp. 264–276.
- <span id="page-14-11"></span>[51] D. Pritam and M. Chatterjee, "Enforcing role-based access control for secure data storage in cloud using authentication and encryption techniques," Journal of Network Communications and Emerging Technologies (JNCET), vol. 6, no. 4, 2016.
- <span id="page-14-12"></span>[52] L. Zhou, V. Varadharajan, and M. Hitchens, "Enforcing role-based access control for secure data storage in the cloud," The Computer Journal, p. bxr080, 2011.
- <span id="page-14-13"></span>[53] A. Gholami and E. Laure, "Security and privacy of sensitive data in cloud computing: A survey of recent developments," arXiv preprint arXiv:1601.01498, 2016.
- <span id="page-14-14"></span>[54] R. Cooper, "Verizon business data breach security blog," 2008.
- <span id="page-14-15"></span>[55] Q. Wang, C. Wang, K. Ren, W. Lou, and J. Li, "Enabling public auditability and data dynamics for storage security in cloud computing," IEEE transactions on parallel and distributed systems, vol. 22, no. 5, pp. 847–859, 2011.
- <span id="page-14-16"></span>[56] Q. Wang, C. Wang, J. Li, K. Ren, and W. Lou, "Enabling public verifiability and data dynamics for storage security in cloud computing," in European Symposium on Research in Computer Security. Springer, 2009, pp. 355–370.
- <span id="page-14-17"></span>[57] N. Ahmed, V. K. Ojha, and A. Abraham, "An ensemble of neuro-fuzzy model for assessing risk in cloud computing environment," in Advances in Nature and Biologically Inspired Computing. Springer, 2016, pp. 27–36.
- <span id="page-14-18"></span>[58] N. Khan and A. Al-Yasiri, "Framework for cloud computing adoption: A road map for smes to cloud migration," arXiv preprint arXiv:1601.01608, 2016.
- <span id="page-14-19"></span>[59] A. V. Nimkar and S. K. Ghosh, "Router framework for secured network virtualization in data center of iaas cloud," in Proceedings of 3rd International Conference on Advanced Computing, Networking and Informatics. Springer, 2016, pp. 475–483.
- <span id="page-14-20"></span>[60] S. Mercyshalinie, G. Madhupriya, S. Vairamani, and S. Velayutham, "Defense against dos attack: Pso approach in virtualization," in 6th International Conference on Advanced Computing (ICoAC), Dec 2014, pp. 199–204.
- <span id="page-14-21"></span>[61] K. Benzidane, S. Khoudali, and A. Sekkaki, "Secured architecture for inter-vm traffic in a cloud environment," in 2nd IEEE Latin American Conference on Cloud Computing and Communications (LatinCloud), Dec 2013, pp. 23–28.
- <span id="page-14-22"></span>[62] Y. Dong, X. Zhang, J. Dai, and H. Guan, "Hyvi: A hybrid virtualization solution balancing performance and manageability," IEEE Transactions on Parallel and Distributed Systems, vol. 25, no. 9, pp. 2332–2341, Sept 2014.
- <span id="page-14-23"></span>[63] C. Li, A. Raghunathan, and N. K. Jha, "A trusted virtual machine in an untrusted management environment," IEEE Transactions on Services Computing, vol. 5, no. 4, pp. 472–483, April 2012.
- <span id="page-14-24"></span>[64] R. K. Banyal, V. K. Jain, and P. Jain, "Data management system to improve security and availability in cloud storage," in International Conference on Computational Intelligence and Networks (CINE), Jan 2015, pp. 124–129.
- [65] C. W. Chang, P. Liu, and J. J. Wu, "Probability-based cloud storage providers selection algorithms with maximum availability," in 41st International Conference on Parallel Processing, Sept 2012, pp. 199–208.
- [66] B. Mao, S. Wu, and H. Jiang, "Exploiting workload characteristics and service diversity to improve the availability of cloud storage systems," IEEE Transactions on Parallel and Distributed Systems, vol. 27, no. 7, pp. 2010–2021, July 2016.
- <span id="page-14-25"></span>[67] M. H. Chen, Y. C. Tung, S. H. Hung, K. C. J. Lin, and C. F. Chou, "Availability is not enough: Minimizing joint response time in peer-assisted cloud storage systems," IEEE Systems Journal, vol. PP, no. 99, pp. 1–11, 2016.
- <span id="page-14-26"></span>[68] Y. Hua, B. Xiao, X. Liu, and D. Feng, "The design and implementations of locality-aware approximate queries in hybrid storage systems," IEEE Transactions on Parallel and Distributed Systems, vol. 26, no. 11, pp. 3194–3207, Nov 2015.
- <span id="page-14-27"></span>[69] D. Espley, "Legal sector will embrace cloud, big data and mobility in 2016," [http://www.itproportal.com/2015/12/14/](http://www.itproportal.com/2015/12/14/legal-sector-will-embrace-cloud-big-data-and-mobility-in-2016/) [legal-sector-will-embrace-cloud-big-data-and-mobility-in-2016/,](http://www.itproportal.com/2015/12/14/legal-sector-will-embrace-cloud-big-data-and-mobility-in-2016/) 2020.
- <span id="page-14-28"></span>[70] P. Matthias, "5g is coming around the corner [mobile radio]," IEEE Vehicular Technology Magazine, vol. 4, no. 1, pp. 4 – 10, 2019.
- <span id="page-14-29"></span>[71] R. L. Grossman, "The case for cloud computing," IT professional, vol. 11, no. 2, pp. 23–27, 2009.
- <span id="page-14-34"></span>[72] L. Coles-Kemp, J. Reddington, and P. A. Williams, "Looking at clouds from both sides: The advantages and disadvantages of placing personal narratives in the cloud," Information Security Technical Report, vol. 16, no. 3, pp. 115–122, 2011.
- [73] S. Marston, Z. Li, S. Bandyopadhyay, J. Zhang, and A. Ghalsasi, "Cloud computing–the business perspective," Decision Support Systems, vol. 51, no. 1, pp. 176–189, 2011.
- [74] R. Buyya, C. S. Yeo, S. Venugopal, J. Broberg, and I. Brandic, "Cloud computing and emerging it platforms: Vision, hype, and reality for delivering computing as the 5th utility," Future Generation Computer Systems, vol. 25, no. 6, pp. 599–616, 2009.
- [75] S. Mansfield-Devine, "Danger in the clouds," Network Security, vol. 2008, no. 12, pp. 9–11, 2008.
- <span id="page-14-37"></span>[76] D. Zissis and D. Lekkas, "Addressing cloud computing security issues," Future Generation Computer Systems, vol. 28, no. 3, pp. 583–592, 2012.
- <span id="page-14-38"></span>[77] N. Sultan, "Cloud computing for education: A new dawn?" International Journal of Information Management, vol. 30, no. 2, pp. 109–116, 2010.
- <span id="page-14-39"></span>[78] P. Hofmann and D. Woods, "Cloud computing: the limits of public clouds for business applications," IEEE Internet Computing, vol. 14, no. 6, pp. 90–93, 2010.
- <span id="page-14-30"></span>[79] W. Kim, "Cloud computing: Today and tomorrow." Journal of Object Technology, vol. 8, no. 1, pp. 65–72, 2009.
- <span id="page-14-31"></span>[80] "Icloud," [https://www.icloud.com/,](https://www.icloud.com/) 2020.
- <span id="page-14-32"></span>[81] "Microsoft onedrive," [https://products.office.com/en-us/onedrive/online-cloud-storage,](https://products.office.com/en-us/onedrive/online-cloud-storage) 2020.
- <span id="page-14-33"></span>[82] "Google drive," [https://gsuite.google.com/,](https://gsuite.google.com/) 2020.
- <span id="page-14-35"></span>[83] C. Lalit and B. Rabindranath, "A comprehensive survey on internet of things (iot) toward 5g wireless systems," IEEE Internet of Things Journal, vol. 7, no. 1, pp. 16 – 32, 2020.
- <span id="page-14-36"></span>[84] S. Richa, W. Isaac, C. Glaucio, and A. Alagan, "Mobile cloud storage over 5g: A mechanism design approach," IEEE Systems Journal, vol. 13, no. 4, pp. 4060 – 4071, 2019.

- <span id="page-15-0"></span>[85] C. Lalit, I. Majitar, and B. Rabindranath, "A comprehensive survey on internet of things (iot) toward 5g wireless systems," IEEE Internet of Things Journal, vol. 7, no. 1, pp. 16 – 32, 2020.
- <span id="page-15-1"></span>[86] P. Samuela, C. Claudia, B. Marina, T. Marco, P. Valeria, G. Andrea, and F. Manuel, "Iot enabling technologies for extreme connectivity smart grid applications," in CTTE–FITCE: Smart Cities & Information and Communication Technology (CTTE–FITCE). IEEE, 2020, pp. 16–32.
- <span id="page-15-2"></span>[87] X. Shuming, N. Qiang, W. Liangmin, and W. Qian, "Sem-acsit: Secure and efficient multi-authority access control for iot cloud storage," IEEE Internet of Things Journal, pp. 1 – 1, 2020.
- <span id="page-15-3"></span>[88] G. Tudor, C.-C. Andrei, A.-C. Madalina, and Z. Alexandru, "Cloud storage. a comparison between centralized solutions versus decentralized cloud storage solutions using blockchain technology," in 54th International Universities Power Engineering Conference (UPEC). IEEE, 2019, pp. 16 – 32.
- <span id="page-15-4"></span>[89] W. Shangping, W. Yuying, and Z. Yaling, "Blockchain-based fair payment protocol for deduplication cloud storage system," IEEE Access, vol. 7, pp. 127 652 – 127 668, 2019.
- <span id="page-15-5"></span>[90] L. Mingyu, P. Li, and L. Shijun, "To transfer or not: An online cost optimization algorithm for using two-tier storage-as-a-service clouds," IEEE Access, vol. 7, pp. 94 263 – 94 275, 2019.
- <span id="page-15-6"></span>[91] R. N. Ridwan, M. Rohit, and L. Palden, "Towards self-managing cloud storage with reinforcement learning," in IEEE International Conference on Cloud Engineering (IC2E). IEEE, 2019, pp. 1 – 6.
- <span id="page-15-7"></span>[92] F. Majid, B. Hamideh, and M. Reza, "An efficient secret sharing-based storage system for cloud-based iots," in 16th International ISC (Iranian Society of Cryptology) Conference on Information Security and Cryptology (ISCISC), vol. 7, 2019, pp. 1–6.


## TL;DR
Comprehensive survey examining cloud storage architecture challenges and solutions for managing heterogeneous big data at massive scale.

## Key Insights
State-of-the-art review identifying security (confidentiality, integrity, access control, breaches) and management (dynamics, segregation, virtualization, backup) challenges in cloud storage; proposes systematic taxonomy of countermeasures including cryptographic solutions, attribute-based access control, and multi-tier architectures for heterogeneous big data environments

## Metadata Summary
### Research Context
- **Research Question**: What are the issues and challenges involved in storing heterogeneous big data in cloud storage architectures, and what are their countermeasures and future opportunities?
- **Methodology**: Comprehensive literature review and state-of-the-art analysis methodology examining 92 references; systematic taxonomy development for categorizing security and management challenges; comparative analysis of proposed solutions and countermeasures
- **Key Findings**: Two main challenge categories identified: data security issues (confidentiality, integrity, access, authentication, breaches) and data management issues (dynamics, segregation, virtualization, backup, availability, locality); 175 ZB data processing expected by 2025; multi-tenancy creates data segregation challenges; attribute-based access control (ABAC) preferred for fine-grained access; cryptographic solutions essential for confidentiality; blockchain technology improving security and trust

### Analysis
- **Limitations**: Focus on general cloud storage rather than specialized knowledge graph architectures; limited discussion of temporal data management strategies; theoretical analysis without extensive empirical validation; concentration on infrastructure challenges rather than schema-level integration approaches
- **Future Work**: Research on integrated privacy-security frameworks for heterogeneous data; development of temporal-aware cloud storage architectures; investigation of standardized multi-source data integration protocols; advancement of AI-driven automated security and management systems for diverse data types