cite_key: olusanya_2023
title: Digital Personal Health Coaching Platform for Promoting Human Papillomavirus Infection Vaccinations and Cancer Prevention: Knowledge Graph-Based Recommendation System
authors: Olufunto A Olusanya, Lokesh Chinthala, Xiaolei Huang, Brianna M White
year: 2023
doi: 10.2196/50210
url: https://formative.jmir.org/2023/1/e50210
relevancy: High
downloaded: 'No'
tags:
- Personal Health Coaching
- Knowledge Graph Recommendations
- HPV Prevention
- Digital Health
- Personalized Medicine
tldr: Knowledge graph-powered digital health coaching for personalized preventive
  care
date_processed: '2025-07-02'
phase2_processed: true
original_folder: jmir_e50210
images_total: 7
images_kept: 6
images_removed: 1
keywords:
- API
- ClinicalTrials
- EHR
- NLP
- PubMed
- abbreviations
- abstract
- ace-associated
- application programming interface
- artificial intelligence
- authors contributions
- berners-lee
- cancer-causing
- case-by-case
- city-level
- conflicts of interest
- corresponding author
- cost-beneficial
- data availability
- data-driven
- decision-making
- deep learning
- diagnosis
- discussion
- dossow-hanfstingl
- ehr
- electronic health record
- ethical considerations
- evidence-based
- evidence-based and
---

Original Paper

# Digital Personal Health Coaching Platform for Promoting Human Papillomavirus Infection Vaccinations and Cancer Prevention: Knowledge Graph-Based Recommendation System

Nariman Ammar1,2,3 , PhD; Olufunto A Olusanya<sup>1</sup> , MBBS, PhD, MPH; Chad Melton1,4 , PhD; Lokesh Chinthala<sup>1</sup> , MSc; Xiaolei Huang<sup>5</sup> , PhD; Brianna M White<sup>1</sup> , MPH; Arash Shaban-Nejad<sup>1</sup> , MPH, MSc, PhD

<sup>1</sup>Center for Biomedical Informatics, Department of Pediatrics, College of Medicine, University of Tennessee Health Science Center, Memphis, TN, United States

2 School of Information Technology, Illinois State University, Normal, IL, United States

<sup>3</sup>Ochsner Xavier Institute for Health Equity and Research, Ochsner Clinic Foundation, New Orleans, LA, United States

<sup>4</sup>Bredesen Center for Interdisciplinary Research and Graduate Education, University of Tennessee, Knoxville, TN, United States

<sup>5</sup>Department of Computer Science, University of Memphis, Memphis, TN, United States

## Corresponding Author:

Arash Shaban-Nejad, MPH, MSc, PhD Center for Biomedical Informatics, Department of Pediatrics College of Medicine University of Tennessee Health Science Center 50 North Dunlap Street - R492 Memphis, TN United States Phone: 1 9012875863 Email: [ashabann@uthsc.edu](mailto:ashabann@uthsc.edu)

## *Abstract*

**Background:**Health promotion can empower populations to gain more control over their well-being by using digital interventions that focus on preventing the root causes of diseases. Digital platforms for personalized health coaching can improve health literacy and information-seeking behavior, leading to better health outcomes. Personal health records have been designed to enhance patients' self-management of a disease or condition. Existing personal health records have been mostly designed and deployed as a supplementary service that acts as views into electronic health records.
**Objective:**We aim to overcome some of the limitations of electronic health records. This study aims to design and develop a personal health library (PHL) that generates personalized recommendations for human papillomavirus (HPV) vaccine promotion and cancer prevention.
**Methods:**We have designed a proof-of-concept prototype of the Digital Personal Health Librarian, which leverages machine learning; natural language processing; and several innovative technological infrastructures, including the Semantic Web, social linked data, web application programming interfaces, and hypermedia-based discovery, to generate a personal health knowledge graph.
**Results:**We have designed and implemented a proof-of-the-concept prototype to showcase and demonstrate how the PHL can be used to store an individual's health data, for example, a personal health knowledge graph. This is integrated with web-scale knowledge to support HPV vaccine promotion and prevent HPV-associated cancers among adolescents and their caregivers. We also demonstrated how the Digital Personal Health Librarian uses the PHL to provide evidence-based insights and knowledge-driven explanations that are personalized and inform health decision-making.
**Conclusions:**Digital platforms such as the PHL can be instrumental in improving precision health promotion and education strategies that address population-specific needs (ie, health literacy, digital competency, and language barriers) and empower individuals by facilitating knowledge acquisition to make healthy choices.
*(JMIR Form Res 2023;7:e50210)*doi: [10.2196/50210](http://dx.doi.org/10.2196/50210)

## TL;DR
Knowledge graph-powered digital health coaching for personalized preventive

## Key Insights  
Platform uses knowledge graphs to provide personalized HPV vaccination recommendations and cancer prevention guidance

## KEYWORDS

health information exchanges; knowledge graphs; recommender systems; personal health libraries; vaccine promotion; cancer prevention; personal health informatics

## *Introduction*## Background

Precision health promotion empowers populations and communities to choose health-related behaviors that allow them to gain more control over their health and well-being through a variety of socio-behavioral, environmental, and economic interventions [\[1](#page-7-0)]. The World Health Organization conceptualizes health promotion as "the process of enabling people to increase control over and to improve their health" [\[2](#page-7-1)]. Rather than emphasizing treatments and palliation, health promotion ultimately reduces the risks of chronic diseases by targeting and preventing the root causes of these diseases [[1](#page-7-0)]. Some of the main elements of health promotion [[1\]](#page-7-0) are to (1) improve population health literacy and knowledge acquisition to ensure healthy behavioral choices; (2) create healthy cities through healthy urban planning to mitigate; and (3) prioritize good policies and better health decision-making that facilitates, for example, vaccine uptake [[3\]](#page-7-2). Vaccinations have deterred countless incidences of vaccine-preventable illnesses and some infectious diseases across the globe.

Consequently, vaccines are proven to be the most effective and cost-beneficial public health intervention for improving health outcomes and saving lives [\[4](#page-7-3)]. While lifestyle factors, including alcohol consumption, cigarette smoking, and prolonged sun exposure, are recognized for increasing the risk of cancer, vaccination against infectious agents such as viruses and bacteria does not receive the same level of attention. For instance, approximately 90% of human papillomavirus (HPV)–associated cancers found in the cervix, vagina, vulva, penis, anus, rectum, and oropharynx are preventable through the uptake of the HPV vaccine [[5\]](#page-7-4).

Despite the HPV vaccine's effectiveness at preventing cancer-causing infections and precancers, more than 45,000 incident cases of HPV-associated cancer diagnoses are reported in the United States annually [\[6](#page-7-5),[7\]](#page-7-6). Although secondary cancer prevention methods (ie, Papanicolaou tests) can detect some types of HPV-related cancers, other types associated with infection are left undetected due to the absence of screening measures (ie, head and neck cancers) [\[8](#page-7-7)]. As a result, the Centers for Disease Control and Prevention (CDC) Advisory Committee on Immunization Practice recommends a 2-dose vaccine series for male and female adolescents aged 9 to 12 years in the United States [\[9](#page-7-8)]. Since vaccinations are only a prophylactic measure and cannot treat HPV infections, early vaccination before infection exposure is key to cancer prevention [[9\]](#page-7-8). Though most effective if administered in early childhood, all individuals through the age of 26 years who have not been fully vaccinated should obtain the HPV vaccine [\[10](#page-7-9)].

More recently, vaccination uptake behavior has been adversely impacted by growing parental vaccine hesitancy due to religious and philosophical beliefs that oppose vaccinations, infodemic, spikes in vaccine misinformation, vitriolic and politicized

[XSL](http://www.w3.org/Style/XSL)•FO**[RenderX](http://www.renderx.com/)**debates about COVID-19 vaccines, COVID-19 pandemic-related disruptions to routine childhood vaccination services, socio-contextual and environmental barriers, public mistrust in vaccine safety and efficacy, perceptions about vaccine side effects, as well as the lack of or inadequate health insurance and health provider recommendations [[11,](#page-7-10)[12](#page-7-11)].

Accordingly, it is pertinent that novel techniques that support precision health promotion are implemented to increase vaccination uptake behaviors. The application of digital educational interventions for personalized health coaching can generate customized recommendations in a case-by-case manner, improve health literacy and knowledge acquisition, optimize information-seeking behavior, promote healthy behavior (eg, HPV vaccine uptake; sexually transmitted infection [STI], HPV, or genital warts testing; and cervical cancer screening), and lead to better population health outcomes (eg, HPV-associated cancer prevention) [\[13](#page-7-12),[14\]](#page-8-0). Advances in artificial intelligence (AI) and digital technologies have revolutionized several applications in health care [\[15](#page-8-1)], promoting and enhancing personalized patient care. For instance, formal semantic data and knowledge representation techniques have enabled the implementation of explainable AI systems by providing extra insights for learning and explanations based on hybrid approaches to AI that combine probabilistic machine learning with symbolic, rule-based reasoning. Those approaches use content and contextual knowledge encoded in ontologies to build and enrich personal health knowledge graphs (PHKGs).

## Role of Digital Technologies in Improving Health and the Delivery of Care

Digital health technologies such as mobile health (mHealth) and mobile medical applications, health information technology, smart devices, wearable sensors, wireless medical devices, and telemedicine or telehealth have revolutionized health care systems [\[15](#page-8-1)]. With the use and application of AI and machine learning, these technologies provide scientists, health care providers, and public health officials with the infrastructure to gather, manage, and interpret heterogeneous complex data sets to provide real-time recommendations for health decision-making and response [\[16\]](#page-8-2). In addition to rapid analysis, digital health solutions could enable personalized and patient-centered approaches to health care management, giving providers better insight into interpreting biological and social markers that could accurately predict actual health status [[17\]](#page-8-3). The application of these innovative tools could optimize decision-making with the ability to tailor treatment and therapies to patient-specific characteristics such as disease history, genetic profile, psychosocial attributes, diagnostic imaging information, or prior treatment responses [\[18](#page-8-4)].

## Design of Digital Health Solutions to Promote Patient Engagement

The continual expansion of digital health solutions provides the opportunity for patient empowerment and the ability to participate fully in their health care decision-making processes.

Patient engagement has historically been limited to patient-provider interactions, with little room for self-management of both chronic and acute conditions [[18\]](#page-8-4). Notably, findings from numerous studies demonstrate that patient empowerment and engagement are key factors in achieving positive health outcomes [\[19](#page-8-5)-[22\]](#page-8-6). With the development of digital technologies such as wearable smart devices and sensors, individuals can track essential vitals such as heart rate and blood pressure and even identify cardiac arrhythmias by generating single-lead electrocardiograms at the touch of a finger [\[23](#page-8-7)]. However, despite a well-documented public desire for technological advancements in health management [[24](#page-8-8)[,25](#page-8-9)], digital health solutions are often not effectively used [\[19](#page-8-5)]. This underuse is attributed to numerous challenges of current digital health solutions, such as digital health disparities (ie, the lack of access to digital health services), unsustainable costs, insufficient digital skills, low level of end user satisfaction, poor user experience, digital navigation difficulties, privacy concerns, varying levels of digital and health literacy, and unreliable provider recommendations for use [\[26](#page-8-10)]. To successfully empower patients to take a stake in their health, effective digital health solutions should be designed with end users in mind to fully engage and educate patients on disease management and monitoring, digital health literacy, health information-seeking behaviors, and vaccine safety or efficacy.

## *Methods*## <span id="page-2-0"></span>Study Design

We have recently proposed a paradigm-shifting design for building a personal health library (PHL) [\[27](#page-8-11),[28\]](#page-8-12) and demonstrated how the PHL can serve as a knowledge infrastructure for building mHealth apps for the self-management of diabetes [[29\]](#page-8-13). We have also implemented a hybrid evidence-based and knowledge-driven explainable AI recommender and digital assistant for mental health surveillance [[30\]](#page-8-14). The PHL integrates health data with multidimensional and multimodal nonhealth data, including observations of daily living (ODL) and population-level social determinants of health (SDoH). Therefore, it enables both patients and health care professionals to make evidence-based decisions by integrating 3 components: clinical expertise, research literature, and patient preferences [[31\]](#page-8-15). The approach used to build the PHL leverages several innovative technological infrastructures, including Semantic Web, the web application programming interface (API), hypermedia-based discovery, and the social linked data [[32\]](#page-8-16) platform to build a privacy-aware, decentralized, yet linked architecture that enables seamless communication among health professionals across different organizations and platforms.

In this paper, we demonstrate how the Digital Personal Health Librarian (DPHL; [Figure 1](#page-2-0)) can use the PHL to generate personalized recommendations, enhance health literacy and knowledge acquisition, optimize information-seeking behavior, promote healthy behavior (eg, HPV vaccine uptake; STI, HPV, or genital warts testing; safe sexual practices; and cervical cancer screening) and overcome false perceptions and misinformation regarding HPV infection and vaccine hesitancy among adolescents and their caregivers. The PHL is currently in its prototype stage and is actively being developed to optimize its implementation and functionalities.
**Figure 1.** A DPHL that uses the types of knowledge stored in the PHL to provide hybrid recommendations and explanations. DPHL: Digital Personal Health Librarian; HPV: human papillomavirus; ML: machine learning; ODL: observations of daily living; PHL: personal health library; SDoH: social determinants of health.

![](_page_2_Figure_9.jpeg)
<!-- Image Description: This diagram depicts the architecture of a Digital Personal Health Librarian (DPHL) system. It shows the interaction between several components: a Digital Personal Health Librarian, a Hybrid Recommendation Service using ML and symbolic reasoning, a Personal Health Library, and an Explanation Service. The system utilizes domain ontologies (e.g., chronic disease, opinion mining) and linked data from urban health observatories and public opinion to build a Personalized Health Knowledge Graph. Data flows are indicated by arrows, illustrating the system's information processing and knowledge generation. -->

## Health Coaching Scenario

In [Figure 2,](#page-3-0) we showcase a scenario from the vaccine promotion, education, and cancer prevention domain. Our goal is to identify issues and needs that can be resolved with the help of a digital intervention. This intervention could improve knowledge acquisition, promote safe sexual practices, increase HPV vaccine uptake, and facilitate the adoption of routine HPV-based screening and testing protocols.

<span id="page-3-0"></span>**Figure 2.** A health coaching scenario. HPV: human papillomavirus.

The scenario shows that in a real-world setting, several types of knowledge can be captured through a conversation with a health coach or a clinician. For example, engaging in unprotected sex is considered risky behavior that increases the likelihood of unintended pregnancies, HPV infections, HIV, and other STIs. In addition, other types of knowledge are brought up during the conversation. For example, the fact that Hailey's mom cannot speak English fluently and Hailey's unvaccinated status serve as upstream social determinants of risk factors. We wish to simulate this conversation in a digital health intervention platform, which we will explain next.

## Hybrid DPHL

[Figure 1](#page-2-0) shows the main components of our DPHL, which simulates a digital health coach. The app passes detected entity types and contextual parameter values to backend services, including the recommendation service, the explanation service, and the PHKG generation component. Based on our scenario, the PHL needs to capture knowledge from relevant domains of interest by reusing several domain ontologies and controlled vocabularies focusing on patients' education (eg, Chronic Disease Patient Education Ontology [\[33](#page-8-17)]), behavior change (eg, Behavior Change Ontology [\[34](#page-8-18)]), and supporting healthy lifestyles (eg, HELiS Ontology [[35\]](#page-8-19)). It also uses other ontologies for knowledge misconceptions. Further, if Hailey wants to receive warnings about misconceptions discussed over social media platforms, the PHL can collect such knowledge by using concepts from opinion-mining ontologies (eg, Marl standardized data schema or ontology [\[36](#page-9-0)]). By accessing dynamic knowledge discovered through the PHL, the DPHL can provide real-time hybrid recommendations that are both content and context based. For example, based on our scenario, the DPHLP can provide recommendations on HPV-associated cancer preventive measures, including safe sexual practices, HPV vaccine uptake, and routine HPV testing.

## Setting Up the PHL

We explain the steps by which the PHL processes Hailey's digital health state, including the following: (1) setting up her digital health profile and specifying her web of trusted agents, (2) specifying types of knowledge (concepts) she would like to maintain in the library, (3) populating concepts with content based on evidence, and (4) using context to personalize the collected knowledge-seeking for resources considering SDoH and ODL.

## Setting Up the Web of Trust

It is apparent from the scenario that Hailey may need to rely on (and trust) several individuals, including her mom, the health coach, and the clinician. A personal health coach is qualified to discuss adolescent preventive health care measures, for example, (1) increase Hailey's sexual or reproductive health knowledge; (2) promote HPV vaccine uptake and HPV or STI testing as cancer preventive measures; (3) counsel on safe sexual practices; (4) counsel on contraception, for example, condom use; and (5) screen substance use or depression. The coach can also counsel on the adverse outcomes of HPV or STI and unprotected sex. On the other hand, only the clinician can administer the vaccines and obtain samples for STI tests. Next, we explain how the above scenario reflects needs related to the 4 HPV-associated cancer preventive measures: safe sexual practices, HPV vaccine uptake, routine HPV testing, and cancer screenings.

## Generating the PHKG

The PHL then uses those types of knowledge to construct and enrich a PHKG for Hailey ([Figure 3](#page-4-0)). The knowledge graph (KG) refinement is performed in three main iterations: (1) first, the PHL uses the information provided by Hailey as contextual entry points to the KG and links them to entity types already stored in the library; (2) it then infers extra knowledge based on concept hierarchies and object properties stored in different domain ontologies; and (3) then, it populates the inferred concepts with evidence from local (city-level urban observatories) or public knowledge (opinions and research).

![](_page_3_Picture_14.jpeg)
<!-- Image Description: The image is a simple text graphic showing "XSL-FO" in gray and "RenderX" in purple. It likely identifies the XSL-FO formatting language and the RenderX processor used in the paper. The image serves as a concise notation of the technologies employed for document generation or processing within the study. No charts, graphs, or equations are present. -->

<span id="page-4-0"></span>**Figure 3.**A PHKG that represents contextual parameters detected in conversations, their corresponding types of knowledge stored in the PHL, as well as new types and causal relations inferred using concept hierarchies and axioms encoded in ontologies. ACE: adverse childhood experience; ACEO/PopHR: ACEs Ontology/population health record; HPV: human papillomavirus infection; mHealth: mobile health; ODL: observations of daily living; PHKG: personal health knowledge graph; PHL: personal health library; SDoH: social determinants of health; STI: sexually transmitted infection; UPHO: Urban Population Health Observatory.

![](_page_4_Figure_3.jpeg)
<!-- Image Description: The image displays two interconnected knowledge graphs representing personal and contextual health knowledge. Nodes represent concepts (e.g., "sexual intercourse," "alcoholism," "internet access"), linked by edges indicating relationships. The upper graph focuses on personal health data, while the lower depicts contextual factors. Different node colors signify data sources (inferred, given, external knowledge). The graphs illustrate how personal information is integrated with broader contextual data to infer rules and personalized insights about an individual (Hailey) regarding STI risk. -->

## Populating PHKG With Evidence

The PHL captures context and collects evidence from several sources of data and knowledge [\(Figure 4](#page-5-0)).

- Individual-level patient preferences and ODL: data from physical activity trackers and electronic subscription behaviors are collected.
- Individual-level data from electronic health records: a huge amount of data in electronic health record (EHR)–specific standards are made available for multiple purposes. In addition to using EHR data for clinical practice, EHR data warehousing can provide longitudinal data on the patient care received over time and benefit hypothesis testing, population screening, clinical trial feasibility evaluation, and analyzing treatment pathways. Furthermore, the vaccination and immunization history data can also be leveraged from structured and unstructured EHR data. The EHR data can also be combined with immunization

[XSL](http://www.w3.org/Style/XSL)•FO**[RenderX](http://www.renderx.com/)**

information systems to track the immunizations received in multiple health care facilities. We plan to deploy text-mining techniques to extract physiological and immunization-related information from these unstructured data.

- Multidimensional population-level SDoH: the PHL aligns the individual-level data with population-level SDoH data regarding neighborhood characteristics from public sources (eg, from the US Census Bureau and local partners).
- Trusted sources of evidence: to collect evidence and enrich the knowledge base, the PHL connects the data and concepts with available literature (eg, PubMed KG [\[37](#page-9-1)] and LinkedCT [\[38](#page-9-2)]). It also collects data from the CDC, which maintains a data repository of concepts related to pregnancy and vaccination, sexually transmitted diseases, smoking and tobacco use, teen vaccinations, vaccinations, and web metrics and makes them accessible through the Socrata

Open Data API. Using this API, we aim to use the data sets on teen vaccinations.

• Public opinions: online social media has been proven to be a valuable resource for vaccine attitude surveillance [[39\]](#page-9-3). We intend to collect vaccine-related data from the Reddit information-sharing social media platform, which is composed of user-created communities (subreddits) in which members adhere to a set of regulations. Subreddit members have the option to post links, images, videos, and text. Anonymous community members then typically upvote or downvote a post based on their opinion of the quality of that post. Depending on the distribution of votes, posts are classified as hot, new, rising, and controversial. The most popular posts within each category are then promoted. Users can also post comments, which undergo the same vote ranking mechanism. The upvote or downvote system within Reddit is intended to increase the quality of the posts to minimize nonrelevant material. We will collect and harvest textual data through the Reddit API in conjunction with the Python Reddit API Wrapper. We will then conduct sentiment analysis and content analysis and apply semantic techniques to develop an optimal system to identify misinformation within these communities.

<span id="page-5-0"></span>**Figure 4.**(1) Multimodal multidimensional data integration from multiple sources, including text detected in conversations, text, or tabular data from literature or reports, individual-level and population-level data, as well as data stored in graphs (focusing on adverse childhood experiences screening scenarios as an example). (2) NLP is applied to text to detect domain concepts based on domain ontologies to generate RDF graphs. ACE: adverse childhood experience; EHR: electronic health record; NLP: natural language processing; RDF: resource description framework.

![](_page_5_Figure_6.jpeg)
<!-- Image Description: The image displays multiple visualizations related to a study on Adverse Childhood Experiences (ACE) scores and health outcomes. It includes: (1) a flowchart illustrating the study's theoretical framework connecting ACE scores to various health issues; (2) tables showing individual patient data (EHR), population-level data (food access, etc.), and ACE-associated health conditions in pediatrics; and (3) ontological graphs representing relationships between ACEs, social determinants, and health outcomes, alongside a table extracted from text analysis of client stories. The purpose is to demonstrate the data sources and analysis methods used in the study linking ACEs to various health outcomes. -->

The PHL integrates global knowledge from the above sources with local knowledge in Hailey's library. Some of the collected knowledge is already in semantic representation (eg, LinkedCT [[38\]](#page-9-2), a ClinicalTrials.gov linked data set that defines concepts related to diseases and interventions). For unstructured data, the PHL transforms the collected evidence into a machine-readable format using Semantic Web technologies and links them to semantic conceptual hierarchies of knowledge types stored in the library.

## Ethical Considerations

This study does not include any real patient data, identifiable personal information, or any human material, and therefore, it is not human subjects research and did not require ethics committee approval. All information presented in case scenarios are solely generated for the sake of clarity in describing and demonstrating functionalities provided by the PHL.

## *Results*

The preliminary prototype design and capabilities provided by the DPHL mHealth app are shown in [Figure 5](#page-6-0). Some of the features include preferences to set up their profile, indicating the types of knowledge they are interested in, their level of experience, and their trusted agents, as well as privacy controls. The app will generate recommendations based on their preferences and they can choose different goals. They also obtain reminders of cancer screening and routine testing as well as vaccines.

<span id="page-6-0"></span>**Figure 5.**Capabilities provided by the DPHL mHealth app include preferences to set up their profile, indicate types of knowledge they are interested in, their level of experience, and their trusted agents as well as privacy controls. The app will generate recommendations based on their preferences and they can choose different goals. They also obtain reminders of cancer screening and routine testing as well as vaccines. CDC: Centers for Disease Control and Prevention; DPHL: Digital Personal Health Librarian; HPV: human papillomavirus; mHealth: mobile health; PHL: personal health library; STI: sexually transmitted infection.

![](_page_6_Figure_6.jpeg)
<!-- Image Description: This image displays the interface design of a mobile health (mHealth) application for self-managing HPV-associated cancers. The app's features are presented in a grid, including sections for managing personal profiles, trusted agents, privacy controls, knowledge sources, and various recommendations (safe sex, cancer screening, vaccine uptake, substance abuse). Each section lists functionalities and data types, illustrating the app's structure and scope. A level of generated knowledge indicator is also visible. -->

## *Discussion*Health promotion empowers individuals by facilitating the acquisition of knowledge and information to make healthy choices and decisions. In this work, we have proposed a paradigm-shifting design of the PHL that improves the maturity of EHR implementations. The proposed PHL could integrate and leverage complex individual- and population-level data from several multidimensional sources such as EHR systems (health histories, prescriptions, laboratory results, and demographic information); consumer health applications, wearable sensors, and devices; US Census Bureau (eg, SDoH indicators and neighborhood characteristics); PubMed KG and LinkedCT; CDC data repository; and social media platforms, for example, Reddit, to offer patients a personalized health assessment and wellness plan.

While the primary focus of this paper is on promoting HPV vaccinations and cancer screening with the PHL, this app could also address barriers to the receipt of other vaccinations, including tetanus, diphtheria, and acellular pertussis; viral hepatitis (hepatitis A, hepatitis B, and hepatitis C); meningococcal; influenza; and COVID-19. Additionally, the proposed PHL could address obstacles to health care delivery services, including limited access to care, poor knowledge and the lack of information, and the lack of provider's recommendation, to improve vaccination outcomes.

[XSL](http://www.w3.org/Style/XSL)•FO**[RenderX](http://www.renderx.com/)**The digital PHL could provide personalized recommendations in the form of either follow-up interventions with associated geo-mapped resource suggestions (eg, clinics near patient or consumer zip code) or follow-up questions to gather further knowledge. It could also provide digital content in the PHL in the form of summarized textual educational material, visual aids, and explanations of recommendations (by providing source links to evidence). Further, similar to grammar checkers, semantic fact-checking can enable patients or consumers to identify and correct misconceptions using fact-checking links. The PHL can also adjust personalized recommendations to the end user's level of literacy.

The PHL uses advances in Semantic Web and AI technologies to augment EHR implementation capabilities and fill existing gaps in EHR knowledge acquisition and explanation. We have demonstrated how the DPHL can use the PHL for personalized self-management, including education and precision health promotion. Our proposed PHL could empower patients and caregivers by giving them a central role in their own decision-making process. Moreover, it could equip health providers with informatics tools to proactively collect and effectively interpret patient data in a contextualized and personalized manner. By offering the PHL functionality as an open service, our proposed platform can encourage the development of third-party applications and services.

The PHL has the potential to offer motivational technological support for projects that span different domains of interest beyond the HPV case study discussed in this paper. We expect that this technology will complement conventional clinical care and management for patients with a variety of other comorbidities and chronic conditions by providing tailored, personalized messaging to improve health-related behaviors and enhance treatment plans. The PHL is currently at the prototype stage and is under active development to implement and optimize its full functionalities. A formal user experience assessment using qualitative focus group interviews and quantitative surveys has been planned to be conducted after the system's full implementation and performance. The assessment of end user experience could be used to gain insights into application effectiveness, functionality, usability, and popularity.

## Acknowledgments

The project described was supported (in part) by grant 1R37CA234119-01A1 from the National Cancer Institute at the National Institutes of Health.

## Data Availability

Data sharing does not apply to this paper as no data sets were generated or analyzed during this study.

## Authors' Contributions

NA and OAO conceptualized the study, wrote the original draft, reviewed and edited the writing, and supervised this study. CM, LC, XH, and AS-N wrote the original draft and reviewed and edited it. BMW reviewed and edited the writing. AS-N supervised this study and acquired the funding.

## Conflicts of Interest

<span id="page-7-0"></span>None declared.

## <span id="page-7-1"></span>References

- <span id="page-7-2"></span>1. Shaban-Nejad A, Michalowski M, Peek N, Brownstein JS, Buckeridge DL. Seven pillars of precision digital health and medicine. Artif Intell Med 2020;103:101793 [doi: [10.1016/j.artmed.2020.101793](http://dx.doi.org/10.1016/j.artmed.2020.101793)] [Medline: [32143798](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=32143798&dopt=Abstract)]
- <span id="page-7-3"></span>2. World Health Organization; Canadian Public Health Association. Ottawa charter for health promotion. Bull Pan Am Health Organ 1987;21(2):200-204 [doi: [10.1016/0168-8510\(87\)90136-9\]](http://dx.doi.org/10.1016/0168-8510(87)90136-9)
- <span id="page-7-4"></span>3. Health promotion. World Health Organization. 2016. URL: [https://www.who.int/news-room/questions-and-answers/item/](https://www.who.int/news-room/questions-and-answers/item/health-promotion) [health-promotion](https://www.who.int/news-room/questions-and-answers/item/health-promotion) [accessed 2022-09-13]
- <span id="page-7-5"></span>4. Kazi AM. The role of mobile phone-based interventions to improve routine childhood immunisation coverage. Lancet Glob Health 2017;5(4):e377-e378 [[FREE Full text](https://linkinghub.elsevier.com/retrieve/pii/S2214-109X(17)30088-8)] [doi: [10.1016/S2214-109X\(17\)30088-8\]](http://dx.doi.org/10.1016/S2214-109X(17)30088-8) [Medline: [28288737\]](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=28288737&dopt=Abstract)
- <span id="page-7-6"></span>5. Printz C. FDA approves Gardasil 9 for more types of HPV. Cancer 2015;121(8):1156-1157 [\[FREE Full text\]](https://onlinelibrary.wiley.com/doi/10.1002/cncr.29374) [doi: [10.1002/cncr.29374\]](http://dx.doi.org/10.1002/cncr.29374) [Medline: [25855331\]](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=25855331&dopt=Abstract)
- <span id="page-7-7"></span>6. How many cancers are linked with HPV each year? Centers for Disease Control and Prevention. 2021. URL: [https://www.](https://www.cdc.gov/cancer/hpv/statistics/cases.htm) [cdc.gov/cancer/hpv/statistics/cases.htm](https://www.cdc.gov/cancer/hpv/statistics/cases.htm) [accessed 2022-09-13]
- <span id="page-7-8"></span>7. Liao CI, Francoeur AA, Kapp DS, Caesar MAP, Huh WK, Chan JK. Trends in human papillomavirus-associated cancers, demographic characteristics, and vaccinations in the US, 2001-2017. JAMA Netw Open 2022;5(3):e222530 [[FREE Full](https://europepmc.org/abstract/MED/35294540) [text](https://europepmc.org/abstract/MED/35294540)] [doi: [10.1001/jamanetworkopen.2022.2530](http://dx.doi.org/10.1001/jamanetworkopen.2022.2530)] [Medline: [35294540](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=35294540&dopt=Abstract)]
- <span id="page-7-10"></span><span id="page-7-9"></span>8. Shapiro GK. HPV vaccination: an underused strategy for the prevention of cancer. Curr Oncol 2022;29(5):3780-3792 [[FREE Full text](https://www.mdpi.com/resolver?pii=curroncol29050303)] [doi: [10.3390/curroncol29050303](http://dx.doi.org/10.3390/curroncol29050303)] [Medline: [35621693\]](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=35621693&dopt=Abstract)
- 9. Glatman-Freedman A, Nichols K. The effect of social determinants on immunization programs. Hum Vaccin Immunother 2012;8(3):293-301 [[FREE Full text](https://www.tandfonline.com/doi/full/10.4161/hv.19003)] [doi: [10.4161/hv.19003\]](http://dx.doi.org/10.4161/hv.19003) [Medline: [22327490](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=22327490&dopt=Abstract)]
- <span id="page-7-11"></span>10. HPV vaccine. Centers for Disease Control and Prevention. 2021. URL: [https://www.cdc.gov/hpv/parents/vaccine-for-hpv.](https://www.cdc.gov/hpv/parents/vaccine-for-hpv.html) [html](https://www.cdc.gov/hpv/parents/vaccine-for-hpv.html) [accessed 2022-09-13]
- <span id="page-7-12"></span>11. Meites E, Szilagyi PG, Chesson HW, Unger ER, Romero JR, Markowitz LE. Human papillomavirus vaccination for adults: updated recommendations of the advisory committee on immunization practices. Centers for Disease Control and Prevention. 2019. URL: <https://www.cdc.gov/mmwr/volumes/68/wr/mm6832a3.htm> [accessed 2022-09-13]
- 12. Olusanya OA, Bednarczyk RA, Davis RL, Shaban-Nejad A. Addressing parental vaccine hesitancy and other barriers to childhood/adolescent vaccination uptake during the coronavirus (COVID-19) pandemic. Front Immunol 2021;12:663074 [[FREE Full text](https://europepmc.org/abstract/MED/33815424)] [doi: [10.3389/fimmu.2021.663074](http://dx.doi.org/10.3389/fimmu.2021.663074)] [Medline: [33815424](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=33815424&dopt=Abstract)]
- 13. Michalowski M, Austin RR, Mathiason MA, Maganti S, Schorr E, Monsen KA. Relationships among interventions and health literacy outcomes for sub-populations: a data-driven approach. Kontakt 2018;20(4):e319-e325 [[FREE Full text\]](https://kont.zsf.jcu.cz/artkey/knt-201804-0002_relationships-among-interventions-and-health-literacy-outcomes-for-sub-populations-a-data-driven-approach.php) [doi: [10.1016/j.kontakt.2018.10.009\]](http://dx.doi.org/10.1016/j.kontakt.2018.10.009)

- <span id="page-8-0"></span>14. Olusanya OA, Ammar N, Davis RL, Bednarczyk RA, Shaban-Nejad A. A digital personal health library for enabling precision health promotion to prevent human papilloma virus-associated cancers. Front Digit Health 2021;3:683161 [\[FREE](https://europepmc.org/abstract/MED/34713154) [Full text\]](https://europepmc.org/abstract/MED/34713154) [doi: [10.3389/fdgth.2021.683161\]](http://dx.doi.org/10.3389/fdgth.2021.683161) [Medline: [34713154](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=34713154&dopt=Abstract)]
- <span id="page-8-2"></span><span id="page-8-1"></span>15. Shaban-Nejad A, Michalowski M, Buckeridge DL. Health intelligence: how artificial intelligence transforms population and personalized health. NPJ Digit Med 2018;1:53 [\[FREE Full text](https://doi.org/10.1038/s41746-018-0058-9)] [doi: [10.1038/s41746-018-0058-9](http://dx.doi.org/10.1038/s41746-018-0058-9)] [Medline: [31304332](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=31304332&dopt=Abstract)]
- 16. Ahmed Z, Mohamed K, Zeeshan S, Dong X. Artificial intelligence with multi-functional machine learning platform development for better healthcare and precision medicine. Database (Oxford) 2020;2020:baaa010 [[FREE Full text](https://europepmc.org/abstract/MED/32185396)] [doi: [10.1093/database/baaa010](http://dx.doi.org/10.1093/database/baaa010)] [Medline: [32185396](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=32185396&dopt=Abstract)]
- <span id="page-8-4"></span><span id="page-8-3"></span>17. Bohr A, Memarzadeh K. The rise of artificial intelligence in healthcare applications. In: Artificial Intelligence in Healthcare. San Diego, CA: Academic Press; 2020:25-60
- <span id="page-8-5"></span>18. Di Minno G, Tremoli E. Tailoring of medical treatment: hemostasis and thrombosis towards precision medicine. Haematologica 2017;102(3):411-418 [[FREE Full text](https://europepmc.org/abstract/MED/28250003)] [doi: [10.3324/haematol.2016.156000\]](http://dx.doi.org/10.3324/haematol.2016.156000) [Medline: [28250003](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=28250003&dopt=Abstract)]
- 19. Birnbaum F, Lewis D, Rosen RK, Ranney ML. Patient engagement and the design of digital health. Acad Emerg Med 2015;22(6):754-756 [[FREE Full text](https://europepmc.org/abstract/MED/25997375)] [doi: [10.1111/acem.12692](http://dx.doi.org/10.1111/acem.12692)] [Medline: [25997375](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=25997375&dopt=Abstract)]
- 20. Schmidt M, Eckardt R, Scholtz K, Neuner B, von Dossow-Hanfstingl V, Sehouli J, et al. Patient empowerment improved perioperative quality of care in cancer patients aged ≥ 65 years—a randomized controlled trial. PLoS One 2015;10(9):e0137824 [\[FREE Full text](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0137824)] [doi: [10.1371/journal.pone.0137824\]](http://dx.doi.org/10.1371/journal.pone.0137824) [Medline: [26378939\]](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=26378939&dopt=Abstract)
- <span id="page-8-6"></span>21. Hibbard JH, Greene J. What the evidence shows about patient activation: better health outcomes and care experiences; fewer data on costs. Health Aff (Millwood) 2013;32(2):207-214 [doi: [10.1377/hlthaff.2012.1061](http://dx.doi.org/10.1377/hlthaff.2012.1061)] [Medline: [23381511\]](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=23381511&dopt=Abstract)
- <span id="page-8-7"></span>22. Chatzimarkakis J. Why patients should be more empowered: a European perspective on lessons learned in the management of diabetes. J Diabetes Sci Technol 2010;4(6):1570-1573 [[FREE Full text](https://europepmc.org/abstract/MED/21129355)] [doi: [10.1177/193229681000400634\]](http://dx.doi.org/10.1177/193229681000400634) [Medline: [21129355](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=21129355&dopt=Abstract)]
- <span id="page-8-8"></span>23. Spaccarotella CAM, Polimeni A, Migliarino S, Principe E, Curcio A, Mongiardo A, et al. Multichannel electrocardiograms obtained by a smartwatch for the diagnosis of ST-segment changes. JAMA Cardiol 2020;5(10):1176-1180 [\[FREE Full](https://europepmc.org/abstract/MED/32865545) [text](https://europepmc.org/abstract/MED/32865545)] [doi: [10.1001/jamacardio.2020.3994](http://dx.doi.org/10.1001/jamacardio.2020.3994)] [Medline: [32865545](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=32865545&dopt=Abstract)]
- <span id="page-8-9"></span>24. Ranney ML, Choo EK, Wang Y, Baum A, Clark MA, Mello MJ. Emergency department patients' preferences for technology-based behavioral interventions. Ann Emerg Med 2012;60(2):218-227.e48 [doi: [10.1016/j.annemergmed.2012.02.026](http://dx.doi.org/10.1016/j.annemergmed.2012.02.026)] [Medline: [22542311\]](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=22542311&dopt=Abstract)
- <span id="page-8-11"></span><span id="page-8-10"></span>25. Brittne KN. Older adults keep pace on tech usage: 2020 tech trends of the 50+. AARP Research. Washington, DC; 2020. URL:<https://www.aarp.org/research/topics/technology/info-2019/2020-technology-trends-older-americans.html> [accessed 2023-10-31]
- <span id="page-8-12"></span>26. Affinito L, Fontanella A, Montano N, Brucato A. How physicians can empower patients with digital tools. J Public Health (Berl.) 2022;30(4):897-909 [[FREE Full text](https://doi.org/10.1007/s10389-020-01370-4)] [doi: [10.1007/s10389-020-01370-4\]](http://dx.doi.org/10.1007/s10389-020-01370-4)
- <span id="page-8-13"></span>27. Ammar N, Bailey JE, Davis RL, Shaban-Nejad A. Implementation of a personal health library (PHL) to support chronic diseases self-management. In: Shaban-Nejad A, Buckeridge DL, Michalowski M, editors. Explainable AI in Healthcare and Medicine: Building a Culture of Transparency and Accountability. New York, NY: Springer; 2020:221-226
- <span id="page-8-14"></span>28. Ammar N, Bailey JE, Davis RL, Shaban-Nejad A. The personal health library: a single point of secure access to patient digital health information. Stud Health Technol Inform 2020;270:448-452 [doi: [10.3233/SHTI200200\]](http://dx.doi.org/10.3233/SHTI200200) [Medline: [32570424\]](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=32570424&dopt=Abstract)
- <span id="page-8-15"></span>29. Ammar N, Bailey JE, Davis RL, Shaban-Nejad A. Using a personal health library-enabled mHealth recommender system for self-management of diabetes among underserved populations: use case for knowledge graphs and linked data. JMIR Form Res 2021;5(3):e24738 [[FREE Full text\]](https://formative.jmir.org/2021/3/e24738/) [doi: [10.2196/24738\]](http://dx.doi.org/10.2196/24738) [Medline: [33724197](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=33724197&dopt=Abstract)]
- <span id="page-8-16"></span>30. Ammar N, Shaban-Nejad A. Explainable artificial intelligence recommendation system by leveraging the semantics of adverse childhood experiences: proof-of-concept prototype development. JMIR Med Inform 2020;8(11):e18752 [\[FREE](https://medinform.jmir.org/2020/11/e18752/) [Full text\]](https://medinform.jmir.org/2020/11/e18752/) [doi: [10.2196/18752\]](http://dx.doi.org/10.2196/18752) [Medline: [33146623](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=33146623&dopt=Abstract)]
- <span id="page-8-17"></span>31. Haynes RB, Sackett DL, Richardson WS, Rosenberg W, Langley RG. Evidence-based Medicine: How to Practice and Teach EBM. New York, NY: Churchill Livingstone; 1997.
- <span id="page-8-18"></span>32. Yeung CMA, Liccardi I, Lu K, Seneviratne O, Berners-Lee T. Decentralization: the future of online social networking. W3C Workshop on Future of Social Networking Position Papers. 2009. URL: [https://www.w3.org/2008/09/msnws/papers/](https://www.w3.org/2008/09/msnws/papers/decentralization.pdf) [decentralization.pdf](https://www.w3.org/2008/09/msnws/papers/decentralization.pdf) [accessed 2023-10-31]
- <span id="page-8-19"></span>33. Wang Z, Huang H, Cui L, Chen J, An J, Duan H, et al. Using natural language processing techniques to provide personalized educational materials for chronic disease patients in China: development and assessment of a knowledge-based health recommender system. JMIR Med Inform 2020;8(4):e17642 [[FREE Full text](https://medinform.jmir.org/2020/4/e17642/)] [doi: [10.2196/17642\]](http://dx.doi.org/10.2196/17642) [Medline: [32324148](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=32324148&dopt=Abstract)]
- 34. Norris E, Finnerty AN, Hastings J, Stokes G, Michie S. A scoping review of ontologies related to human behaviour change. Nat Hum Behav 2019;3(2):164-172 [doi: [10.1038/s41562-018-0511-4](http://dx.doi.org/10.1038/s41562-018-0511-4)] [Medline: [30944444](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=30944444&dopt=Abstract)]
- 35. Dragoni M, Bailoni T, Maimone R, Ecche C. HeLiS: an ontology for supporting healthy lifestyles. Cham, Switzerland: Springer; 2018 Presented at: The Semantic Web—ISWC 2018: 17th International Semantic Web Conference; October 8–12, 2018; Monterey, CA p. 53-69 [doi: [10.1007/978-3-030-00668-6\\_4](http://dx.doi.org/10.1007/978-3-030-00668-6_4)]

- <span id="page-9-0"></span>36. Westerski A, Iglesias CA, Rico FT. Linked opinions: describing sentiments on the structured web of data. 2011 Presented at: 4th International Workshop Social Data on the Web; October 23, 2011; Bonn, Germany p. 10-21 URL: [https://oa.upm.es/](https://oa.upm.es/13139/) [13139/](https://oa.upm.es/13139/)
- <span id="page-9-2"></span><span id="page-9-1"></span>37. Xu J, Kim S, Song M, Jeong M, Kim D, Kang J, et al. Building a PubMed knowledge graph. Sci Data 2020;7(1):205 [\[FREE](https://doi.org/10.1038/s41597-020-0543-2) [Full text\]](https://doi.org/10.1038/s41597-020-0543-2) [doi: [10.1038/s41597-020-0543-2](http://dx.doi.org/10.1038/s41597-020-0543-2)] [Medline: [32591513](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=32591513&dopt=Abstract)]
- 38. Hassanzadeh O, Miller RJ. Automatic curation of clinical trials data in LinkedCT. Cham: Springer; 2015 Presented at: The Semantic Web—ISWC 2015: 14th International Semantic Web Conference; October 11-15, 2015; Bethlehem, PA p. 270-278 [doi: [10.1007/978-3-319-25010-6\\_16](http://dx.doi.org/10.1007/978-3-319-25010-6_16)]
- <span id="page-9-3"></span>39. White BM, Melton C, Zareie P, Davis RL, Bednarczyk RA, Shaban-Nejad A. Exploring celebrity influence on public attitude towards the COVID-19 pandemic: social media shared sentiment analysis. BMJ Health Care Inform 2023;30(1):e100665 [\[FREE Full text](https://informatics.bmj.com/lookup/pmidlookup?view=long&pmid=36810135)] [doi: [10.1136/bmjhci-2022-100665](http://dx.doi.org/10.1136/bmjhci-2022-100665)] [Medline: [36810135](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=36810135&dopt=Abstract)]

## Abbreviations

**AI:**artificial intelligence**API:**application programming interface**CDC:**Centers for Disease Control and Prevention**DPHL:**Digital Personal Health Librarian**EHR:**electronic health record**HPV:**human papillomavirus**KG:**knowledge graph**mHealth:**mobile health**ODL:**observations of daily living**PHKG:**personal health knowledge graph**PHL:**personal health library**SDoH:**social determinants of health**STI:**sexually transmitted infection
*Edited by A Mavragani; submitted 22.06.23; peer-reviewed by W Wei, A Chaturvedi; comments to author 02.09.23; revised version received 09.10.23; accepted 24.10.23; published 15.11.23*

*Please cite as:*

*Ammar N, Olusanya OA, Melton C, Chinthala L, Huang X, White BM, Shaban-Nejad A Digital Personal Health Coaching Platform for Promoting Human Papillomavirus Infection Vaccinations and Cancer Prevention: Knowledge Graph-Based Recommendation System JMIR Form Res 2023;7:e50210 URL: <https://formative.jmir.org/2023/1/e50210> doi: [10.2196/50210](http://dx.doi.org/10.2196/50210) PMID: [37966885](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=37966885&dopt=Abstract)*

©Nariman Ammar, Olufunto A Olusanya, Chad Melton, Lokesh Chinthala, Xiaolei Huang, Brianna M White, Arash Shaban-Nejad. Originally published in JMIR Formative Research (https://formative.jmir.org), 15.11.2023. This is an open-access article distributed under the terms of the Creative Commons Attribution License (https://creativecommons.org/licenses/by/4.0/), which permits unrestricted use, distribution, and reproduction in any medium, provided the original work, first published in JMIR Formative Research, is properly cited. The complete bibliographic information, a link to the original publication on https://formative.jmir.org, as well as this copyright and license information must be included.

![](_page_9_Picture_12.jpeg)
<!-- Image Description: The image is a simple text-based graphic showing "XSL-FO" in gray and "RenderX" in light purple. It likely identifies the XSL-FO (Extensible Stylesheet Language Formatting Objects) processing software, RenderX, used in the paper. The purpose is to specify the technology employed for document formatting and generation, likely within a section describing the research methodology or tools. -->

## Metadata Summary
### Research Context
- **Research Question**: How can knowledge graphs enable personalized digital health coaching for preventive care and vaccination promotion?
- **Methodology**: Knowledge graph-based recommendation engine, personalized health coaching algorithms, HPV and cancer prevention knowledge integration
- **Key Findings**: Developed functional platform for personalized health recommendations using KG technology for preventive care guidance

### Analysis
- **Limitations**: Limited details available from title/URL, specific evaluation metrics not accessible
- **Future Work**: Adapt recommendation approach for HDM health monitoring, implement privacy-preserving personalization