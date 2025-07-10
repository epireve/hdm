---
cite_key: gyrarda_2024
title: IoT-Based Preventive Mental Health Using Knowledge Graphs and Standards for Better Well-Being
authors: Amelie Gyrarda, Seyedali Mohammadi, Manas Gaur, Antonio Kung, Mental Health
year: 2024
date_processed: '2025-07-02'
phase2_processed: true
original_folder: arxiv_2406.13791_IoT-Based_Preventive_Mental_Health_Using_Knowledge
images_total: 2
images_kept: 2
images_removed: 0
tags:
- Data Integration
- Healthcare
- IoT
- Knowledge Graph
- Machine Learning
- Mental Health
- Semantic Web
keywords:
- 1 introduction
- 6 conclusion and future work
- BetterHelp
- BioMedInformatics
- BioPortal
- BlenderBot
- ChatCounselo
- ChatDiet
- EHR
- FoodOn
- GPT
- HealthyOffice
- a-rank
- accra-project
- acknowledgements and funding
- ageing-well
- ai magazine
- ai-based
- ai-based assessment
- ai-based mental
- ai-enabled
- ai-enabled health informatics
- aim-ahead
- anxiety-difference
- apadisor-ders
- applied psychology
- article history
- artificial intelligence
- authorea preprints
- based learning
---

# IoT-Based Preventive Mental Health Using Knowledge Graphs and Standards for Better Well-Being

Amelie Gyrarda,c,\*, Seyedali Mohammadi<sup>b</sup> , Manas Gaur<sup>b</sup> and Antonio Kung<sup>a</sup>

<sup>a</sup>Trialog, Paris, France; <sup>b</sup>University of Maryland, Baltimore County (UMBC), USA; <sup>c</sup>Machine-to-Machine Measurement (M3), Paris, France

## ARTICLE HISTORY

Compiled October 22, 2024

### ABSTRACT

Sustainable Development Goals (SDGs) give the UN a road map for development with Agenda 2030 as a target. SDG3 "Good Health and Well-Being" ensures healthy lives and promotes well-being for all ages. Digital technologies can support SDG3. Burnout and even depression could be reduced by encouraging better preventive health. Due to the lack of patient knowledge and focus to take care of their health, it is necessary to help patients before it is too late. New trends such as positive psychology and mindfulness are highly encouraged in the USA. Digital Twins (DTs) can help with the continuous monitoring of emotion using physiological signals (e.g., collected via wearables). DTs facilitate monitoring and provide constant health insight to improve quality of life and well-being with better personalization. Healthcare DTs challenges are standardizing data formats, communication protocols, and data exchange mechanisms. As an example, ISO has the ISO/IEC JTC 1/SC 41 Internet of Things (IoT) and DTs Working Group, with standards such as "ISO/IEC 21823-3:2021 IoT - Interoperability for IoT Systems - Part 3 Semantic interoperability", "ISO/IEC CD 30178 - IoT - Data format, value and coding". To achieve those data integration and knowledge challenges, we designed the Mental Health Knowledge Graph (ontology and dataset) to boost mental health. As an example, explicit knowledge is described such as chocolate contains magnesium which is recommended for depression. The Knowledge Graph (KG) acquires knowledge from ontology-based mental health projects classified within the LOV4IoT ontology catalog (Emotion, Depression, and Mental Health). Furthermore, the KG is mapped to standards (e.g., W3C Semantic Web languages such as RDF, RDFS, OWL, SPARQL to develop and query ontologies and datasets) when possible. Standards from ETSI SmartM2M can be used such as SAREF4EHAW (SAREF for eHealth Ageing Well domain) to represent medical devices and sensors, but also ITU/WHO, ISO, W3C, NIST, and IEEE standards relevant to mental health can be considered.

### KEYWORDS

Well-Being; Mental Health; Standard; Semantic Web Technologies; Health Ontology; Knowledge Graph; IoT Ontology Catalog; Large Language Model.

CONTACT A. N. Author. Email: amelie.gyrard@trialog.com

"An ounce of prevention is worth a pound of cure."

Benjamin Franklin

"How to gain, how to keep, how to recover happiness is in fact for most men at all times the secret motive of all they do, and of all they are willing to endure."

William James

### 1 Introduction

More than one-fifth of adults in the United States have dealt with mental health issues, according to the National Institute of Mental Health<sup>1</sup> . This situation has led to the government setting aside \$280 billion to improve the availability and quality of mental health services<sup>2</sup> . Mental health can increase productivity and efficiency, improve staff morale, and reduce absenteeism (Albraikan, 2019). There are numerous reviews on mental health using Wearable sensors and Artificial Intelligence Techniques (Gedam & Paul, 2021). Sustainable Development Goals (SDGs)<sup>3</sup> give the UN a road map for development with Agenda 2030 as a target. SDG3 "Good Health and Well-Being" ensures healthy lives and promotes well-being for all ages. Digital technologies can support SDG3. We review hereafter definitions relevant to mental health, the need for Digital Twin for Mental Health, and the benefit of a Knowledge Graph (KG). Mental health<sup>4</sup> is a state of mental well-being that enables people to cope with the stresses of life, realize their abilities, learn well, and work well, and contribute to their community. It has intrinsic and instrumental value and is integral to our well-being. IEEE 7010 defines well-being as "the continuous and sustainable physical, mental, and social flourishing of individuals, communities, and populations where their economic needs are cared for within a thriving ecological environment." Stress vs. Anxiety: People under stress<sup>5</sup> experience mental and physical symptoms, such as irritability, anger, fatigue, muscle pain, digestive troubles, and difficulty sleeping. Anxiety, on the other hand, is defined by persistent, excessive worries that don't go away even in the absence of a stressor<sup>6</sup> . Burnout and even depression<sup>7</sup> could be reduced by encouraging better preventive health. Lack of patient knowledge and focus to take care of their health before it is too late. New trends such as positive psychology (Seligman, 2008) and mindfulness (MBSR) (Kabat-Zinn, 2003) are highly encouraged in the USA. Depression is considered the main mental health crisis by the World Health Organization (WHO) (Mullick, Singh, Shaw, et al., 2022). Men-

<sup>1</sup>https://www.nimh.nih.gov/health/statistics/mental-illness

<sup>2</sup>https://www.whitehouse.gov/cea/written-materials/2022/05/31/reducing-the-economic -burden-of-unmet-mental-health-needs/

<sup>3</sup>https://sdgs.un.org/goals

<sup>4</sup>https://www.who.int/health-topics/mental-health#tab=tab\_1

<sup>5</sup>https://www.apa.org/topics/stress/anxiety-difference

<sup>6</sup>https://www.apa.org/topics/stress/anxiety-difference

<sup>7</sup>https://www.who.int/news-room/fact-sheets/detail/depression

tal health includes emotional, psychological, and social well-being changes. DSM-V (Diagnostic and Statistical Manual of Mental Disorders)<sup>8</sup> references more than 70 mental disorders that complement the International Classification of Diseases (ICD). DSM-V helps clinicians and researchers define and classify mental disorders, which can improve diagnoses, treatment, and research. DSM-V provides a form with checklists of symptoms for better diagnosis. Burnout does NOT appear in DSM and ICD. Mental illness is a type of health condition that changes a person's mind, emotions, or behavior and has been shown to impact an individual's physical health (Su, 2020). Depressive disorders, or unipolar depression's symptoms are low mood, loss of interest in day-to-day activities, significant weight changes, reduction of mobility, constant fatigue, difficulty concentrating, and feelings of worthlessness that can be diagnosed, and severity, using the Patient Health Questionnaire-9 (PHQ-9) (Gutierrez, Rabbani, et al., 2021).

The necessity of AI-enabled IoT Digital Twin using knowledge graph for achieving SDG-3: An IoT Digital Twin designed for proactive mental health care corresponds with four of the United Nations' Sustainable Development Goals. First is good health and well-being (SDG-3), which aims to ensure healthy lives and promote well-being for all age groups. We provide a pragmatic approach to developing IoT Digital Twin using domain-specific standards and knowledge graphs, which would advance mental health care and well-being. Disparities in mental health care access are prevalent, varying among regions, socioeconomic statuses, and genders. By prioritizing preventive strategies using domain-specific standards (e.g., questionnaires, guidelines) and leveraging AI-enabled IoT technology, this endeavor can potentially mitigate these access gaps, aligning with initiatives like the NIH's AIM-AHEAD Initiative.

Why do we need a Digital Twin for Mental Health? The StandICT landscape of Digital Twins (DT)<sup>9</sup> reminds that "Digital Twin" was first introduced by Professor Michael Grieves from the University of Michigan in 2002. According to ISO/IEC 30173 Digital twin – concepts and terminology<sup>10</sup>, DTs are defined as a "digital representation of a target entity with data connections that enable convergence between the physical and digital states at an appropriate rate of synchronization." Notable implementation of DTs include Siemens Healthineers (Erol, Mendi, & Dogan, 2020), ˘ IBM Maximo Application Suite<sup>11</sup> and Philips HeartModel<sup>12</sup>. DT can help with emotion monitoring using physiological signals (e.g., collected via wearables). Healthcare DTs facilitate monitoring, understanding, and optimization of human functioning and monitor health to improve quality of life and well-being (Laamarti et al., 2020), (Ferdousi, Laamarti, & El Saddik, 2022), (Albraikan, 2019), (Anand & Dhanalakshmi, 2024) with better personalization (Bagaria et al., 2020) by using digital technologies such as IoT, AI, etc. Healthcare DT challenges highlight the need for standardizing data format, communication protocols, and data-exchange mechanisms (Turab, 2023).

Why do we need Knowledge Graphs for Mental Health? The European Human Brain Project (150 000 000 Euros, 161 partners), more precisely, the

<sup>8</sup>https://www.psychiatry.org/psychiatrists/practice/dsm

<sup>9</sup>https://www.standict.eu/landscape-analysis-report/landscape-digital-twin

<sup>10</sup>https://www.iso.org/standard/81442.html

<sup>11</sup>https://www.ibm.com/products/maximo

<sup>12</sup>https://www.philips.com/a-w/about/news/archive/blogs/innovation-matters/20181112

<sup>-</sup>how-a-virtual-heart-could-save-your-real-one.html

EBRAINS KG<sup>13</sup>, is a synergy project between neuroscience, computing, informatics, and brain-inspired technologies, encourages open-science through a web-based system to share tools, etc. However, when looking for keywords such as cortisol (the stress hormone), nothing can be found. KGs (Sheth, Padhee, & Gyrard, 2019) can use ontologies to structure data. An ontology provides a shared common understanding of a domain (Gruber, 1995). The use of ontologies is already recognized in the biomedical domain with BioPortal ontology catalog<sup>14</sup> . Ontology Development 101 methodology (designed by the creators of the Standford Protégé Ontology Editor tool) encourages reusing domain knowledge by reusing ontologies in Step 2 "Consider reusing ontologies."

In this paper, we describe about semantic interoperability applied to mental health, which is a follow-up of our health IoT semantic interoperability past work (Gyrard & Sheth, 2020) (Gyrard et al., 2022). Toward Converging Standards and Semantic Web Technologies applied to Mental Health: We illustrate the vision of our aligning technologies on Semantic Web and Data spaces and Standards such as ISO, IEC, and W3C as depicted in Figure 1. W3C Standards are more adapted to Semantic Web technologies such as W3C RDF, W3C RDFS, W3C OWL, W3C SPARQL, etc. Semantic Web technologies include knowledge Graphs with ontologies and Linked Data. There are also ISO standards about ontologies such as ISO/IEC 21838-1:2021 Information technology — Top-level ontologies (TLO) — Part 1: Requirements, ISO/IEC 21838-2:2021 Information technology — Top-level ontologies (TLO) — Part 2: Basic Formal Ontology (BFO), etc. Data Space initiatives such as BDVA, Gaia-X, etc. are considered. Some energy data spaces are designed by projects such as EDHS2, and TEHDAS. The list is not exhaustive. "Charting past, present, and future research in the semantic web and interoperability" highlights the importance of semantic interoperability (Rejeb et al., 2022) and on our past work: Table 5 "Top 20 most productive authors" and Figure 4 "Co-authorship network." The recommendation is that interoperability should remain a primary research focus and closer collaborations with industry, governments, and standards organizations to develop more effective models.

Our vision has been shared with the EUCloudEdgeIoT Concentration and Consultation Meeting on Computing Continuum: Uniting the European ICT community for a digital future in May 2023<sup>15</sup> .

The remainder of this chapter is organized as follows: related work limitations in Section 2, standards for mental health in Section 3, the mental health ontology catalog in Section 4 (which includes mapping to standards ontologies), the project use cases in

![](_page_3_Figure_4.jpeg)
<!-- Image Description: This diagram illustrates the landscape of Internet of Things (IoT), edge, and cloud technologies. It uses overlapping circles to represent various standards organizations (e.g., ISO, IEEE), EU projects, alliances (e.g., Gaia-X), data spaces, and related technologies (e.g., AI, linked data). The relationships and overlaps between these elements are visually depicted, highlighting their interconnectedness within the broader IoT ecosystem. The legend clarifies the meaning of different colored shapes. -->

Figure 1.: Standards, Semantic Web and Data Spaces applied to Health

<sup>13</sup>https://search.kg.ebrains.eu/?facet\_type[0]=Dataset&q=cortisol

<sup>14</sup>https://bioportal.bioontology.org/

<sup>15</sup>https://eucloudedgeiot.eu/concentration-and-consultation-meeting-on-computing -continuum-uniting-the-european-ict-community-for-a-digital-future/

Section 5, and conclusion in Section 6.

## 2 Related Work: IoT, Digital Twin, and AI for Mental Health, Stress and Well-Being

This section reviews IoT-based Mental Health Monitoring Applications, IoT-based Stress Detection, Digital Twin for Mental Health, and AI-based Mental Health.

| Authors | Year Research Problem | Sensor or | Reasoning |
|--------------------|------------------------------------------|-------------------------------------------------|-----------------------------|
| | Addressed & Project | Measurement Type | |
| Garcia-Ceja et al. | 2018 Mental Health Monitoring | ✓Heart rate, GSR, | Survey paper |
| | Systems (NHMS) Survey | body or skin temperature | ✓ML algorithm |
| Kim | 2017 Depression Severity | ✓Infrared motion sensor | ✓Bayesian Network |
| | Elderly People, AAL | | Decision Tree, SVM, ANN |
| Zhou et al. | 2015 Monitoring mental health | ✓Heart rate, pupil variation, | ✓ML (Logistic |
| | states | head movement, eye blink, facial expression | regression, SVM) |
| Garcia-Ceja et al. | 2016 Stress | ✓Accelerometer data (from smartphone) | ✓Naive Bayes, Decision Tree |
| Yoon, Sim, and Cho | 2016 New stress monitoring patch | ✓Skin conductance, pulse wave, skin temperature | ×- |
| Lu et al. | 2012 StressSense | ✓Voice data (smartphone) | ✓GMMs |
| K.-h. Chang et al. | 2011 AMMON: Stress detector | ✓Voice data | ✓SVM |
| Erol et al. | 2020 DT for patients and medical devices | ×No | ×No |
| Liu et al. | 2019 CloudDTH -<br>DT healthcare | ✓Yes Wearable medical devices | ×No |
| Albraikan | 2019 inHarmony - Emotional Well-being | DT ✓Yes Empatica E4 | ×No |

Table 1.: Digital Twin for Mental Health, Depression, Stress, and Well-Being: sensors, reasoning, and applications.

IoT-based Mental health and depression monitoring applications are summarized in Table 1. 23 Mental Health Monitoring Systems (NHMS) Garcia-Ceja et al. (2018) using sensor data provided by IoT devices and analyzed with Machine Learning are classified according to the study type (e.g., bipolar disorder detection, migraine forecasting, depression detection, anxiety detection, stress detection, social phobia association, bipolar disorder association, anxiety association, depression association, and epilepsy). Various devices are employed (e.g., eye sensor, heart rate variability, electrodermal activity, wrist accelerometer, galvanic skin response, skin conductance, spo2, photoplethysmogram, accelerometer, gyroscope, pressure sensitive, video cameras, VR headset, pupil-corneal reflection and head tracker, SMS, calls, screen, GPS, location, touchscreens, audio, contacts, videos, sound, head-mounted display, questionnaires). Conclusion: We focus on IoT devices relevant to mental health disorders such as stress, anxiety, and depression, and do not consider others such as bipolar, migraine, or phobia. The authors do not mention at all the term "ontology" or knowledge graph."

24 IoT-based mental health care applications Gutierrez et al. (2021) (bipolar disorders, depression, schizophrenia, and stress-related disorders); from 2010 to 2020 are designed for: 1) data acquisition, 2) self-organization, 3) service level agreement, and 4) identity management during mental health interventions. IoT devices considered are proximity sensors, ambient light, accelerometers, gyroscopes, magnetometers, ambient sound, barometers, temperature, and humidity. Diagnostic and Statistical Manual of Mental Disorders 5 (DSM 5) categorizes the mental health disorder literature. HealthyOffice smartphone app Zenonos et al. (2016) focuses on eight mood state recognition (Excited, Happy, Calm, Tired, Bored, Sad, Stressed, Angr) in work environments.

Conclusion: We focus on mental health disorders such as stress, and depression, and do not consider other disorders such as bipolar, or schizophrenia. Gutierrez et al. Gutierrez et al. (2021) only cite the mental health ontology from Hazdic et al. Hadzic, Chen, and Dillon (2008), and do not mention at all the KG term, so key research on depression ontologies and KGs are missing. For this reason, we built the ontology catalog as introduced in Section 4.1 and Table 2.

IoT-based Stress Detection is summarized in Table 1. Stress is a reaction from the human body in response to a challenging event or a demanding condition Gedam and Paul (2021); which can be detected using wearable sensors (e.g., Electrocardiogram, Electroencephalography, and Photoplethysmography) and applied machine learning. Activities such as driving, studying, and working are taken into consideration. Wearable healthcare-monitoring systems for pain and stress detection J. Chen, Abbod, and Shieh (2021)) are using wearable sensors to measure physiological signals such as heart, brain, muscle, electrodermal, respiratory, blood volume pulse, and skin temperature. A system to detect, diagnose and manage mental health emergencies Mullick et al. (2022); is based on four physiological parameters: heart rate, Spo2, body temperature (LM35 sensor), pressure (BMP180 sensor).

Digital Twin (DT) for Mental Health and Well-Being is summarized in Table 1. Digital Twin Coaching for Physical Activities's survey (Gámez Díaz, Yu, Ding, Laamarti, & El Saddik, 2020) explore papers from Scopus, Web of Science, IEEE Xplore and ACM Digital Library the last ten years (2010–2020). The papers have been classified into: 1) sports, 2) wellbeing, and 3) rehabilitation. The following information is extracted: 1) ML algorithms being used 2) Type of application being researched, 3) Sensors and actuators devices used, 4) Performance of the ML algorithm, 5) Usability feedback of users about the system. Digital Twin in healthcare (Turab, 2023) highlights the need for standardizing data format, communication protocols, and data-exchange mechanisms. Turab et al. highlight that ISO has an interest in Digital Twin. Indeed, we are involved in ISO SC 41 IoT and Digital Twin. Wellbeing digital twin (WDT) (Ferdousi et al., 2022) challenges for predictive wellbeing applications are technical issues of handling heterogeneous data and standards, data bias, level of autonomy, trust in intelligence, data visualization issues, and consent of humans. Drawbacks of WDT are: 1) Inadequate or missing data, 2) Ethical overheads, 3) Trust in AI, and 4) Necessity of domain knowledge. Well-being digital twin (WDT) areas are: 1) Collecting and managing vast healthcare data, 2) Meaningful data visualization, 3) Facilitating predictive healthcare, 4) Improving healthcare quality of experience (QoE), 5) Personalized healthcare system (e.g., digital coaching, elderly healthcare (e.g. device in Ponmalar and Anand (2024)), immune system care), and 6) Understanding clinical pathways. An ISO/IEEE 11073 standardized digital twin framework architecture for health and well-being to analyze data from personal health devices is compliant or not with X73 standards (Laamarti et al., 2020). inHarmony (Albraikan, 2019) is an Emotional Well-being DT for workplace which includes emotion detection, emotional biofeedback, and emotion-aware recommender systems. A usability study was carried out with 35 practitioners wearing the Empatica E4 sensor to acquire physiological signals. CloudDTH (Liu et al., 2019) is a DT Healthcare (DHT) framework for real-time monitoring, diagnosing, and predicting of elderly's health, based on cloud, and wearable medical devices technologies. A Big Data-based Precision Medicine Cloud Platform is designed to display human physiological health data for data management, data analysis, etc. DTs of patients and DTs of medical devices are considered (Erol et al., 2020). DT Siemens Healthineers (Erol et al., 2020) for radiology department in Mater Private Hospitals from Ireland to reduce patient's waiting time. Siemens Healthineers is also applied to cardiologists in a research project at Heidelberg University for patients with chronic congestive heart failure. Philips HeartModel<sup>16</sup> is a personalized Digital Twin of the heart to help surgeons with real-time 3D. Its HeartNavigator tool combines the Computed Tomography (CT) heart anatomy obtained before the surgical procedure and live during the surgery. Sooma is a startup that simulates the electrical signals of the brain to treat depression, other neurological and psychiatric disorders.

Conclusion: We did not find a digital twin for mental health. inHarmony is addressing well-being.

AI-based Mental Health: "Positive AI" (van der Maden, Lomas, & Hekkert, 2023), means that AI systems actively and intentionally support human well-being based on fields such as positive psychology, human-centered design, and computing. The authors categorized twelve well-being AI challenges into 1) knowledge (how to conceptualize, operationalize, optimize for, and design), and 2) motivation (misaligned incentives, PR & monetary risks, and lack of access, preventing). To identify mental health states, machine learning algorithms such as support vector machines, decision trees, naïve Bayes classifier, K-nearest neighbor classifier, and logistic regression are used (Srividya, Mohanavalli, & Bhalaji, 2018).

Related work shortcomings: Those works do not use health standards that we are addressing in Section 3. Furthermore, in this chapter, we will focus on KGs (e.g., ontologies) as AI solutions as explained in Section 4.

## 3 Standards for Mental Health and Well-Being: Artificial Intelligence (Semantic Web, Ontologies)

We investigate Standards Development Organizations (SDOs) for (mental) health covering AI (Semantic Web, Ontologies) such as: ETSI SmartM2M EHealth/Ageing-Well Ontology in Section 3.1, ITU/WHO Focus Group on Artificial Intelligence for Health in Section 3.2, ISO Health Standards in Section 3.3, W3C Health Standards in Section 3.4, NIST Health Standards in Section 3.5, and IEEE Health Standards in Section 3.6. Standards De-

![](_page_6_Figure_6.jpeg)
<!-- Image Description: This diagram illustrates standardized ontologies categorized by their standardization body. Several ontologies are shown, including ETSI SmarM2M SAREF, IEEE Std 1872.2-2021 Autonomous Robotics, W3C SSN/SOSA, OneM2M, W3C Thing Description, HL7 FHIR, and ISO/IEC 21838-2:2021 (BFO). The diagram's purpose is to visually represent the landscape of standardized ontologies used in a specific domain (likely within the paper's focus area). -->

Figure 2.: Standardized Ontologies

velopment Organizations SDOs define health ontologies or IoT ontologies describing sensors to measure the physiological signals of patients as depicted in Figure 2.

<sup>16</sup>https://www.philips.com/a-w/about/news/archive/blogs/innovation-matters/20181112 -how-a-virtual-heart-could-save-your-real-one.html

## *3.1 ETSI SmartM2M SAREF for EHealth/Ageing-Well Ontology*

ETSI Smart M2M SAREF4EHAW ontology (*ETSI TS 103 410-8 V1.1.1 (2020- 07) SmartM2M; Extension to SAREF; Part 8: eHealth/Ageing-well Domain*, 2020) reviews standards such as IEEE, ETSI, SNOMED, OneM2M), Alliances (AIOTI), IoT Platforms, and European projects and initiatives, etc.

The use cases are classified into some of those categories: 1) Daily Activity Monitoring, 2) Cognitive simulation for mental decline prevention, 3) Prevention of social isolation, 4) Comfort and safety at home. SAREF4EHAW investigated the following ontologies: 1) WSNs/measurement ontologies: OGC (Open Geospatial Consortium) Observations & Measurements (O&M), Sensor Model Language (SensorML), Semantic Sensor Web (SWE): W3C & OGC SOSA (Sensing, Observation, Sampling, and Actuation) and W3C SSN (Semantic Sensor Network). NASA QUDT (Quantities, Units, Dimensions, and Types). 2) eHealth/Ageing-well domain main ontologies: ISO/IEEE 11073 Personal Health Device (PHD) standards, ETSI SmartBAN Reference Data Model and associated modular ontologies, FHIR RDF (Resource Description Framework), FIESTA-IoT Ontology to support the federation of testbeds, Bluetooth® LE (Low Energy) profiles for medical devices proposed by Zontinua, MIMU-Wear (Magnetic and Inertial Measurement Units) ontology, and Active and Healthy Ageing (AHA) platform wearables' device ontology. The document explains that SAREF has been mapped with oneM2M base ontology in 2017. SAREF4EHAW (*ETSI TS 103 410-8 V1.1.1 (2020-07) SmartM2M; Extension to SAREF; Part 8: eHealth/Ageing-well Domain*, 2020) selected 43 ontological requirements, and 59 service-level assumptions of the eHealth/Ageing-well domain (use cases included). For instance, as a requirement, the ontology describes ECG ((Muthalagu, Ramachandran, Anupama, et al., 2023)) device concepts. There is also SAREF4WEAR <sup>17</sup> an extension for wearables.

Conclusion: SAREF4EHAW demonstrates the need for ontologies. We did not find standards more specific to mental health in ETSI.

### *3.2 ITU/WHO Focus Group on Artificial Intelligence for Health*ITU/WHO Focus Group on Artificial Intelligence for Health (FG-AI4H)<sup>18</sup>, established in 2018, free and open, partners with the World Health Organization (WHO) to standardize AI-based assessment framework and evaluation for health, diagnosis, triage or treatment decisions. It provides an AI for health online platform and complementary tools for benchmarking of data. FG-AI4H comprises experts: machine learning/AI researchers, healthcare practitioners and researchers, regulators, representatives of health ministries and ministries of telecommunication, international organizations, and individuals from complementary fields. The FG highlights the need for explainability and interpretability of AI tools. ITU-T/WHO FG-AI4H use cases: 24 AI4H use cases are introduced, including traditional medicine, psychiatry, neurological disorders, falls among the elderly, etc. DEL.10.23 TG-AI for Traditional Medicine reviews the existing AI solutions for Traditional Medicine. AI in traditional medicine will be relevant to support healthcare practitioners in recommending integrative medical practices. Traditional Medicine treatments: 1) Ontological and Natural language processing (NLP) are encouraged to extract useful information, 2) Analyz-

<sup>17</sup>https://saref.etsi.org/saref4wear/

<sup>18</sup>https://www.itu.int/go/fgai4h

ing and integrating data, and 3) Decision support, 4) Predictive analytics, 5) Patient monitoring and feedback, 6) virtual health assistants, and 7) Research and knowledge discovery.

Conclusion: We find a standard on AI Traditional Medicine, but we did not find standards for mental health in this SDO.

### *3.3 ISO Health Standards*The CEN/ISO EN13606 is a European norm approved as an ISO standard to achieve EHR semantic interoperability. ISO 13606-5:2010 Health Informatics - Electronic Health Record communication standards<sup>19</sup> defines an architecture for exchanging Electronic Health Record (EHR) describing patient's health status and ease communication between EHR systems (e.g., clinicians applications, decision support systems). ISO 13606 seems an open standard. Within the ISO SC41 IoT and Digital Twin, there is an ongoing standard entitled "IoT/IEC 30197 IoT for Stress Management, Good health & Well-being". ISO SC42 AI - "AI-enabled Health Informatics" is a joint working group that will provide a landscape survey and a set of recommendations for future work on the impact of ISO/TC 215 standards. The group comprises experts from ISO/IEC/JTC 1/SC 42, IEEE, and the ITU/WHO AI4Health focus group. ISO/IEEE 11073 medical device communication standard - Used by Personal Connected Health Alliance (PCHAlliance) - X73 standards facilitates health data exchange while providing plug-and-play real-time interoperability by being compliant with the X73 communication model. However, the X73 standards do not address security or users' privacy. This ISO/IEEE 11073 standard is used by Laamarti et al. (2020) for a digital twin framework architecture for health and well-being in smart cities. NIST researchers are collaborating with medical device experts to develop standards for medical device communications to enhance semantic interoperability. XML schema and tool based on the ISO/IEEE 11073 medical device communication standard is developed by Garguilo et al. (Garguilo, Martinez, et al., 2007). Personal Connected Health Alliance (PCHAlliance) products use the ISO/IEEE 11073 Personal Health Data (PHD) Standards.

Conclusion: ISO 215 Health Informatics must be explored further to dig any documents related to mental health. CEN/ISO EN13606 focuses on EHR semantic interoperability. ISO SC42 AI joint working group "AI-enabled Health Informatics" comprises experts from ISO/IEC/JTC 1/SC 42, IEEE, and the ITU/WHO AI4Health focus group.

## *3.4 W3C Semantic Web Health Care and Life Sciences Community Group (HCLS CG)*W3C Semantic Web (SW) Health Care and Life Sciences Community Group (HCLS CG)<sup>20</sup> encourages the use of SW technologies across health care, life sciences, clinical research and translational medicine as they need interoperability of information from many disciplines. HCLS CG use SW technologies to design use cases which have a clinical, research of business values. The CG develops liaisons with organizations in healthcare, life sciences, and clinical research, including organizations that are working on standards.

<sup>19</sup>http://www.en13606.org/information.html

<sup>20</sup>https://www.w3.org/community/hclscg/

Conclusion: W3C HCLS CG highlights the need of using Semantic Web. The final report is more focused on drug-drug interaction. We did not find standards specific to mental health.

## *3.5 NIST Health Standards*NIST researchers are collaborating with medical device experts to develop standards for medical device communications to enhance semantic interoperability. XML schema and tool based on the ISO/IEEE 11073 medical device communication standard (Garguilo et al., 2007).

Conclusion: NIST has an interest in semantic interoperability.

## *3.6 IEEE Health Standards*IEEE digital health standards can help save lives and improve people's quality of life. Standards aim to share information across end-to-end infrastructure, particularly: 1) interoperability: information exchange among organizations, 2) cost savings/efficiency (e.g., for hospitals), etc. We selected four standards: 1) IEEE 7010's definition of well-being (mentioned earlier), 2) IEEE 1752.1-2021 Standard for Open Mobile Health Data–Representation of Metadata, Sleep, and Physical Activity Measures, 3) ISO/IEEE 11073 medical device communication standard, and 4) IEEE P1157 Medical Data Interchange (MEDIX). IEEE 1752.1-2021 Standard for Open Mobile Health Data–Representation of Metadata, Sleep, and Physical Activity Measures<sup>21</sup> eases semantic interoperability across mobile health sources and provides meaningful description, exchange, sharing, and use of such mHealth data for consumer health, biomedical research, and clinical care stakeholders. NIST researchers are collaborating with medical device experts to develop standards for medical device communications to enhance semantic interoperability. XML schema and tool based on the ISO/IEEE 11073 Medical Device Communication standard (Garguilo et al., 2007). IEEE P1157 Medical Data Interchange (MEDIX) is a standard for communication of medical information between heterogeneous healthcare information systems such as between a patient care system and selected ancillaries in the medical center setting. IEEE 1157 Standard for Health Data Interchange is designed with health care professionals.

Conclusion: Within IEEE 7010, we found a standard explaining the definition of well-being. Understanding well-being will help as a preventive solution to reduce mental health problems.

### *3.7 Standards: Conclusion*We did not find standards for mental health in those SDOs: ETSI SmartM2M, ITU/WHO FG-AI4H, and W3C HCLS CG. ISO 215 Health Informatics must be explored further to dig any documents related to mental health. CEN/ISO EN13606 focuses on EHR semantic interoperability. We are involved in "IoT for Stress Management, Good health & Well-being, a standard under development within ISO SC41 IoT. ISO SC42 AI joint working group "AI-enabled Health Informatics" comprises experts from ISO/IEC/JTC 1/SC 42, IEEE, and the ITU/WHO AI4Health focus group.

<sup>21</sup>https://standards.ieee.org/ieee/1752.1/6982/

| Authors | Year | Project | Ontology-based Reasoning | |
|-------------------------------------------------------------------|------|------------------------------------------------------------------------|--------------------------|-------------------------------------------|
| | | | project | |
| Hastings et al. Hastings et al. (2012) | 2012 | Mental Disease (MD) | ✓(online code) | No |
| Ceusters et al. Smith et al. | | Ontology | | |
| Amoretti et al. Amoretti, Frixione, Lieto, and Adamo (2019) | 2019 | Mental Disorder<br>Schizophrenia ontology | ✓(online code) | OWL-DL |
| | | | | |
| Chang et al. Y.-S. Chang et al. (2013) | 2015 | Depression ontology | ✓(but not shared) | Bayesian networks |
| Chang et al. Y.-S. Chang, Fan, Lo, Hung, and Yuan (2015), Taiwan | 2013 | | | Jena rule (Dysthymia), 46 inference rules |
| Huang et al. Huang, Yang, van Harmelen, and Hu (2017) | 2017 | DepressionKG | ✓(datasets) | No |
| Hadzic et al Hadzic et al. (2008) | 2008 | Mental Health<br>Ontology | ✓(but not shared) | No |
| Perth, Australia | | disorder, factors, and treatments | | |
| Jung et al. Jung, Park, and Song (2017) Jung et al. (2015), Korea | | 2017-2015 Depression Ontology, adolescent population, Twitter analysis | ✓(but not shared) | No |

Table 2.: Ontology-based depression and mental health projects

NIST has an interest in semantic interoperability. IEEE 7010 focused on well-being which encourages us to investigate well-being as a preventive solution to reduce mental health problems.

## 4 LOV4IoT Ontology Catalog for IoT-Based Depression and Mental Health KGs

Ontology catalogs such as BioPortal (Noy et al., 2009), Linked Open Vocabularies (LOV) (Vandenbussche, Atemezing, Poveda-Villalón, & Vatant, 2016) do not cover sensors (Internet of Things). For this reason, we built the LOV4IoT ontology catalog (introduced in Section 4.1), with a subset specific to mental health and depression (demonstrated in Table 2), and emotion ontologies explained in (Gyrard, Tabeau, Fiorini, Kung, et al., 2021) (Gyrard & Boudaoud, 2022) or LOV4IoT-Health to collect sensor used, etc. Mapping to Standards such as ETSI SmartM2M SAREF4EHAW is mentioned in Section 4.2. Mapping to Standardized Health KGs/Ontologies/Terminologies such as SNOMED-CT, FMA, RXNORM, MedDRA, LOINC, ChEBI, or well-known knowledge graphs such as DBpedia is described in Section 4.3.

## *4.1 LOV4IoTMental Health Ontology Catalog and Knowledge Graph*We have designed an ontology catalog for depression and mental health, called LOV4IoT Mental Health <sup>22</sup> (Table 2).

GENA (Graph of mEntal-health and Nutrition Association) (Dang, Phan, & Nguyen, 2023)<sup>23</sup> encodes relationships between nutrition and mental health. GENA describes food, biochemicals, and mental illnesses extracting knowledge from PubMed. GENA consists of 43,367 relationships with concepts such as nutrition, biochemical, mental health, chemical, and disease. GENA used ontologies such as Human Disease Ontology (DOID), Chemical Entities of Biological Interest Ontology (CHEBI), Foundational Model of Anatomy (FMA), Disorders cluster (APADISOR-DERS), Autism Spectrum Disorder Phenotype Ontology (ASDTTO), The FoodOn Food Ontology (FOODON), MFO Mental Disease Ontology (MFOMD), Protein Ontology (PR), and Symptom Ontology (SYMP). As an example, CHEBI, FMA, is used as explained in Section 4.3.

DSM-V (Diagnostic and Statistical Manual of Mental Disorders)<sup>24</sup> references more than 70 mental disorders that complement the International Classification of Diseases (ICD). DSM-V helps clinicians and researchers define and classify mental disorders, which can improve diagnoses, treatment, and research. DSM-V provides a

<sup>22</sup>http://lov4iot.appspot.com/?p=lov4iot-depression

<sup>23</sup>https://github.com/ddlinh/gena-db

<sup>24</sup>https://www.psychiatry.org/psychiatrists/practice/dsm

checklist form of symptoms for better diagnosis. As an example, DSM-V is used as explained in Section 5.3.

Mental Health Ontology (Hadzic et al., 2008) comprises three sub-ontologies: 1) disorder/illness types, (2) factors, and (3) treatments. Disorders types are anxiety disorder, eating disorder, childhood disorder, cognitive disorder, mood disorder. Factors can be: 1) Physical (e.g. vitamin B deficiency, health injury, liver disease), 2) Environmental (E physical, social, financial), 3) Personal (belief, emotion, response). The need to understand emotions like stress, anger, bitterness, guilt, joy, happiness, peace, and fear, since they directly affect mental health is highlighted by Hadzic et al. (2008).

Mental Functioning (MF) Ontology and Mental Disease (MD) Ontology<sup>25</sup> (Hastings et al., 2012) describe human mental functioning and disease, including mental processes such as cognitive processes and qualities such as intelligence. MF Ontology is based on Basic Formal Ontology (BFO). MD ontology covers concepts such as disease, diagnosis, disorder, and addiction. Mental Functioning Ontology and Mental Disease Ontology could be used to map answers from clinical interview questionnaires about mood, psychotic disorders, and related spectrum conditions. Hastings et al. also designed emotion ontology. Mapping to https:// obofoundry.org/ontology/mfomd.html (Hastings et al., 2012) is not simple since there are no labels or comments within the ontology code but concepts IRI such as MFOMD\_0000040. Fortunately, the URI are deferenceable which means that if we copy and paste https://ontobee.org/ontology/MFOMD?iri= http://purl.obolibrary.org/obo/MFOMD\_0000040 we can get additional information such as the definition: "A diagnosis asserting the presence of an instance of a mental disease in a given organism."

Depression KG (Huang et al., 2017) is a disease-centric KG applied to Major Depressive Disorder, which addresses several challenges: (1) Heterogeneity of datasets, (2) text processing, (3) incompleteness, inconsistency, and incorrectness of datasets, and (4) expressive, representation of medical knowledge. Depression KG utilizes rulebased reasoning over the KG, which helps psychiatric doctors without KG expertise. MDepressionKG (Fu, Jiang, He, & Jiang, 2021) integrates the human microbial metabolism network, human diseases, microbes and other ontologies. Ontology for College Student Mental Health Service (CSMH) (X. Zhang & Chen, 2020) describes appointments, mental disorders, self-help resources, information for parents, local referral sources, and substance abuse prevention. Some of the information is extracted from two CSMH websites. Ontology for mental disorders - Schizophrenia Spectrum Ontology (Amoretti et al., 2019), is compliant with DSM-5 descriptions of mental disorders, with a specific focus on Schizophrenia. It comprises 58 classes (Mental\_Disorder, Patient, and Symptom), 5 properties, and 191 axioms. Classes of the Schizophrenia Spectrum category and the associated symptoms are defined. Future work is planned to address borderline personality disorder or major depression. Ontology for managing mental healthcare network in Brazil (Yamada et al., 2018), based on BFO, used for integration and interoperability between databases and to design a Semantic Web-based Decision Support System (DSS) for a regional mental healthcare network in Brazil for clinical and administrative processes. The challenges of dealing with standardization and low-quality data are highlighted. The competency question is whether a manager wants to know how many people had schizophrenia in the city of São Paulo in 2017 without looking at various systems of hospitals in the city.

<sup>25</sup>https://obofoundry.org/ontology/mfomd.html

### *4.2 Mapping to Standards: ETSI SmartM2M SAREF4EHAW*The mapping to the ETSI SmartM2M SAREF4EHAW ontology is already explained within the book chapter "SAREF4EHAW-Compliant Knowledge Discovery and Reasoning for IoT-based Preventive Healthcare and Well-Being" (Gyrard & Kung, 2022). The mapping focuses on the sensor type used.

## *4.3 Mapping to Standardized Health KGs/Ontologies/Terminologies: SNOMED-CT, FMA, RXNORM, MedDRA, LOINC, ChEBI, MESH, GALEN and DBpedia*The mapping to health knowledge bases is explained within "Interdisciplinary IoT and Emotion Knowledge Graph-Based Recommendation System to Boost Mental Health" (Gyrard & Boudaoud, 2022). We mapped hormones and neurotransmitters concepts. We searched key ontologies on the Bioportal ontology catalog, to be mapped with the Emotion KG. We found ontologies such as SNOMED-CT, Mapping Foundational Model of Anatomy (FMA), RXNORM, MedDRA, Logical Observation Identifier Names and Code (LOINC), Medical Subject Headings (MESH), GALEN, and Chemical Entities of Biological Interest Ontology (ChEBI). The mappings of hormones and neurotransmitters are summarized in two Tables "Subset of mapping hormones and neurotransmitters to existing knowledge bases to demonstrate the difficulty of reusing only one knowledge base." DBpedia is also used due to its popularity, and links emotion-related concepts to existing emotion ontologies when available online. Most of the emotion ontologies cannot be found on BioPortal; only Hastings's ontology (Hastings, Ceusters, Smith, & Mulligan, 2011) is referenced on BioPortal.

## 5 Ontology-Based Mental Health Recommender System and Project Use Cases: ACCRA, etc.

Project use cases are explained in this Section 5. Social robots to support active and healthy aging (ACCRA European-Japan Project) in Section 5.1, Large Language Models (LLMs) for Mental Health in Section 5.2, and other projects on Mental Health such as Depression and Suicide in Section 5.3.

## *5.1 ACCRA European-Japan Project: Social robots to support active and healthy aging*To design emotional-based robotic applications, how can Internet of Robotic Things (IoRT) technology and co-creation methodologies be used? The ACCRA (Agile Co-Creation of Robots for Ageing) EU project<sup>26</sup> (Gyrard et al., 2021), coordinated by Trialog, develops advanced social robots to support active and healthy aging, co-created by various stakeholders such as aging people and physicians. Three robots, Buddy, ASTRO, and RoboHon, are used for daily life, mobility, and conversation. The three robots understand and convey emotions in real-time using the Internet of Things and Artificial Intelligence technologies (e.g., knowledge-based reasoning). The ACCRA project explains that social companion robots assist elderly people in staying independent at home and decrease their social isolation. A challenge was to design appli-

<sup>26</sup>https://www.accra-project.org/en/sample-page/

cations usable by elderly people using co-creation methodologies involving multiple stakeholders and a multidisciplinary research team (e.g., elderly people, medical professionals, and computer scientists such as roboticists or IoT engineers).

## *5.2 Large Language Models (LLMs) for Mental Health*Large Language Models (LLMs) have become increasingly popular due to their vast statistical knowledge, allowing them to produce fluent English sentences and exhibit human-like performance across tasks such as question-answering, summarization, and recommendations. The debut of ChatGPT on November 30, 2022, garnered considerable attention alongside similar autoregressive LLMs like Google BARD, Google GEMINI, and Anthropic Claude (Minaee et al., 2024). Despite their impressive performance, these LLMs have been criticized for providing confidently asserted yet factually inaccurate information, referred to as "hallucination" (Rawte, Sheth, & Das, 2023). This poses a significant challenge to their reliability and trustworthiness. Moreover, LLMs sometimes yield inconsistent answers, eroding trust in their outputs. Attention explanations (generated by models) do not closely align with the ground truth explanations provided by human experts (Mohammadi et al., 2024). When LLMs offer irrelevant explanations, it exacerbates trust issues, casting doubt on their reliability as tools (Y. Zhang, Li, Cui, Cai, et al., 2023). Consequently, their application in healthcare, particularly mental health, has been hindered. Although there are mental health-specific LLMs, their performance lacks consistency, reliability, explainability, and trust assessment (Gaur & Sheth, 2024).

Efforts to enhance these LLMs for better utility in healthcare have led to recent research focusing on instruction-tuned and retrieval-augmented (e.g. Tilwani et al. (2024)) LLMs (Lewis et al., 2020). Instruction tuning involves incorporating an additional feature called "instruction" into the dataset, which can be a guideline, protocol, or rule for the LLM to follow (Sheth, Gaur, Roy, Venkataraman, & Khandelwal, 2022; S. Zhang et al., 2023). However, such training methods have not proven very effective in sensitive domains. Recent work has shown that rules learned by LLMs after instruction tuning do not match the model's performance level, raising concerns about this training approach, particularly in areas akin to moral question answering, such as mental health. An empirical study by Gupta et al. (2022) demonstrates that LLMs struggle to complete clinical questionnaires for depression and anxiety . Subsequently, Roy, Zi, et al. (2023) proposed architecture changes, particularly in autoregressive language models, suggesting that a tree-based learning prediction layer could yield safer outcomes in mental health contexts . Further exploration at the intersection of instruction-tuned LLMs and mental health is warranted. Examples of publicly available mental health LLMs include ChatCBPTSD, Diagnosis of Thought Prompting (Z. Chen, Lu, & Wang, 2023), Mental-LLM (Alpaca/FLAN-T5 based), MentaLLaMA (LLaMA-2 based; (K. Yang, Zhang, Kuang, et al., 2023)), ChatCounselo, ExTES-LLaMA (both LLaMA based), and BBMHR (BlenderBot-BST based), while some, like MindShift, Psy-LLM, and LLM-Counselors (all GPT-3.5 based), remain unavailable to the public (Hua et al., 2024).

Retrieval-augmented LLMs represent another category, where a generator model is paired with a knowledge retriever capable of accessing documents from a vectorized database. These LLMs draw context from the retriever, offering reliability and domain-specific explainability crucial in domains like mental health. Gaur, Gunaratna, et al. (2022) demonstrated the extension of these LLMs to knowledge graphs . However, experimentation has primarily been limited to open-domain knowledgeintensive language understanding tasks, leaving its utility in mental health as an ongoing research question (Sarkar, Gaur, Srivastava, et al., 2023). An example of retrievalaugmented LLM is shown in openCHA (Z. Yang, Khatibi, Nagesh, et al., 2024). Abbasian, Azimi, Rahmani, and Jain (2023) developed openCHA, a framework that empowers health agents to enhance the processing of healthcare inquiries by efficiently analyzing input queries, integrating essential information, and offering personalized, context-aware responses.The framework's effectiveness in managing complex healthcare tasks through various expert-provided demonstrations. For example, Z. Yang et al. (2024) leveraged openCHA to create a personalized nutrition-oriented food recommendation chatbot, enabled by user's longitudinal data on diabetes, American Diabetes Association dietary guidelines, the Nutritionix information, personal causal models, and population models. On an evaluation includes 100 diabetes-related questions on daily meal choices and the potential risks associated with the diet, openCHA demonstrated superior performance compared to state-of-the-art GPT 4.

### *5.3 Other Projects on Mental Health*Mental health professionals (MHPs) are overwhelmed by the rising prevalence of declining mental health (MH), depression, and suicide risk. Traditionally, they rely on time-consuming clinical questionnaires (e.g., DSM-5 assessment measures, strengths and difficulties questionnaires) and long patient interviews<sup>27</sup>. However, the growing demand for MH services and the shortage of MHPs motivate automated methods for early screening. However, it's important to note that receiving high-quality assistance is not guaranteed<sup>28</sup>. We require online screening assistance as an improvement over online consultations (e.g., BetterHelp), aiming for higher-quality support. AI has emerged as a promising tool for analyzing text data from various sources, including Electronic Health Records (EHR) and social media posts (Joyce, Kormilitzin, Smith, & Cipriani, 2023; Thiruvalluru, Gaur, Thirunarayan, Sheth, et al., 2021; T. Zhang, Schoene, Ji, & Ananiadou, 2022).

Research in AI and Mental health can be broadly categorized into two categories: (a) Statistical data-driven machine learning in the realm of mental health, as exemplified by the contributions of De Choudhury, Gamon, Counts, and Horvitz (2013), De Choudhury et al. (2016), Saha, Chandrasekharan, and De Choudhury (2019), Chancellor and De Choudhury (2020), Shing et al. (2018) and Gkotsis et al. (2017), represents a significant advancement. However, while these studies showcase the effectiveness of AI in this domain, they are limited in their ability to instill trustworthiness, primarily due to a deficiency in explainability and interoperability, which could be greatly enhanced by incorporating domain-specific expertise. (b) Knowledgedriven Machine Learning for Mental Health: This comprises work involving clinical questionnaires for question answering, summarization, longitudinal assessment (Alambo et al., 2019; Gaur, Aribandi, et al., 2021; Gupta et al., 2022; Manas et al., 2021), a diagnostic statistical manual for mental health disorders for identifying mental health disorders (Gaur et al., 2018), and detecting and assessing the severity of substance use disorder using domain-specific drug abuse ontology (Kursuncu et al., 2018; Lokala, Lamy, et al., 2022; Lokala, Srivastava, et al., 2022). Machine-readable mental

<sup>27</sup>https://wiki.aiisc.ai/index.php?title=Mental\_Health\_Projects

<sup>28</sup>https://wiki.aiisc.ai/index.php?title=Modeling\_Social\_Behavior\_for\_Healthcare \_Utilization\_in\_Depression

health knowledge has resulted in explainable classification and interpretable design of black-box language models and conversational agents (Dalal et al., 2024; Gaur, Faldu, & Sheth, 2021; Roy, Sheth, & Gaur, 2023). Further, datasets designed using such a knowledge are capable of examining grounding, instructability, and alignment of domain-specific language models (e.g., ClinicalBERT (Alsentzer et al., 2019), PsychBERT (Vajre et al., 2021), MentalBERT (Ji et al., 2021)) to the intent, needs, and requirements of MHPs (Gaur et al., 2019; Sheth, Gaur, Roy, & Faldu, 2021).

### 6 Conclusion and Future Work

A Mental Health KG (ontology and dataset) acquires knowledge from ontologybased projects classified within the LOV4IoT ontology catalog (Depression, Mental Health, and Emotion). LOV4IoT supports researchers with 1) the Systematic Literature Survey, which is a time-consuming task and requires an eagerness to learn and investigate existing projects, 2) FAIR principles to encourage researchers to share their reproducible experiments by publishing online ontologies, datasets, rules, etc.

Short-term challenges: LOV4IoT is relevant for the IoT community. The results are encouraging to update the dataset with additional domains and ontologies. LOV4IoT leads to the AIOTI (The Alliance for the Internet of Things Innovation) IoT ontology landscape survey form<sup>29</sup> and analysis result<sup>30</sup>, executed by the Standard WG - Semantic Interoperability Expert Group. It aims to help industrial practitioners and non-experts answer those questions: Which ontologies are relevant in a certain domain? Where to find them? How to choose the most suitable? Who is maintaining and taking care of their evolution? There is also the AIOTI Health WG white paper publications on health data space "IoT/Edge Computing and Health Data and Data Spaces"<sup>31</sup>, "AI for better health"<sup>32</sup>, and "IoT Improving Healthy Urban Living"<sup>33</sup> .

Mid-term challenges: Automatic knowledge extraction from ontologies and scientific publications describing the ontology purpose is challenging, as highlighted in our AI4EU Knowledge Extraction for the Web of Things (KE4WoT) Challenge. The challenge encourages the reuse of the expertise designed by domain experts and makes the domain knowledge usable, interoperable, and integrated by machines. We released the set of ontologies, as dumps, web services, and tutorials, and made them available.

Long-term challenges: To improve the veracity and the evaluation of the KG integrated with a reasoning engine, involving domain experts such as psychologists, neuroscientists, etc. would enhance the KG, by proving more of the facts. The knowledgebased reasoning engine can be extended by considering additional research fields such as psychophysiology, psychobiology, etc. An emphasis on the emotional aspect can be done (e.g., fear, pessimism, sadness) since it impacts mental health.

<sup>29</sup>https://ec.europa.eu/eusurvey/runner/OntologyLandscapeTemplate

<sup>30</sup>https://bit.ly/3fRpQUU

<sup>31</sup>https://aioti.eu/aioti-white-paper-iot-edge-computing-and-health-data-and-data -spaces/

<sup>32</sup>https://aioti.eu/aioti-wg-health-white-paper-on-ai-for-better-health/

<sup>33</sup>https://aioti.eu/wp-content/uploads/2022/09/IoT-and-Healthy-Urban-Living-Final.pdf

### Acknowledgements and Funding

We want to acknowledge the Kno.e.sis research team (lead by Professor Amit Sheth) from Wright State University, Ohio, USA for fruitful discussions about related topics such as "Mental Health/Depression/Suicide", and "Semantic, Cognitive, and Perceptual Computing" and with cognitive psychologists such as Professor Valerie Shalin during Dr. Gyrard's post-doc in 2018-2019.

This work has partially received funding from the European Union's Horizon 2020 research and innovation program under project grant agreement StandICT.eu 2026 No. 101091933 (open call). We would like to thank the project partners for their valuable comments. The opinions expressed are those of the authors and do not reflect those of the sponsors.

### References

- Abbasian, M., Azimi, I., Rahmani, A. M., & Jain, R. (2023). Conversational health agents: A personalized llm-powered agent framework.*arXiv preprint arXiv:2310.02374*.
- Alambo, A., Gaur, M., Lokala, U., Kursuncu, U., Thirunarayan, K., Gyrard, A., . . . Pathak, J. (2019). Question answering for suicide risk assessment using reddit. In *2019 ieee 13th international conference on semantic computing (icsc)*(pp. 468–473).
- Albraikan, A. (2019).*inharmony: A digital twin for emotional well-being*(Unpublished doctoral dissertation). Université d'Ottawa/University of Ottawa.
- Alsentzer, E., Murphy, J. R., Boag, W., Weng, W.-H., Jin, D., Naumann, T., . . . McDermott, M. B. (2019). Publicly available clinical bert embeddings.*NAACL HLT 2019*.
- Amoretti, M. C., Frixione, M., Lieto, A., & Adamo, G. (2019). Ontologies, mental disorders and prototypes. In *On the cognitive, ethical, and scientific dimensions of artificial intelligence.*Springer.
- Anand, J., & Dhanalakshmi, R. (2024). Hygieia: Multipurpose healthcare assistance using the internet of things. In*Internet of medical things in smart healthcare*(pp. 77–96). Apple Academic Press.
- Bagaria, N., Laamarti, F., Badawi, H. F., Albraikan, A., Martinez Velazquez, R. A., & El Saddik, A. (2020). Health 4.0: Digital twins for health and well-being.*Connected health in smart cities*.
- Chancellor, S., & De Choudhury, M. (2020). Methods in predictive techniques for mental health status on social media: a critical review. *NPJ digital medicine*.
- Chang, K.-h., et al. (2011). How's my Mood and Stress?: an Efficient Speech Analysis Library for Unobtrusive Monitoring on Mobile Phones. In *Body area networks conference.*- Chang, Y.-S., Fan, C.-T., Lo, W.-T., Hung, W.-C., & Yuan, S.-M. (2015). Mobile cloud-based depression diagnosis using an ontology and a bayesian network.*Future Generation Computer Systems*, *43*, 87–98.
- Chang, Y.-S., et al. (2013). Depression Diagnosis Based on Ontologies and Bayesian Networks. In *Systems, man, and cybernetics (smc), 2013 ieee international conference on.*- Chen, J., Abbod, M., & Shieh, J.-S. (2021). Pain and stress detection using wearable sensors and devices—a review.*Sensors*.
- Chen, Z., Lu, Y., & Wang, W. (2023). Empowering psychotherapy with large language models: Cognitive distortion detection through diagnosis of thought prompting. In *Findings of the association for computational linguistics: Emnlp 2023.*- Dalal, S., Tilwani, D., Gaur, M., Jain, S., Shalin, V., & Sheth, A. (2024). A cross attention approach to diagnostic explainability using clinical practice guidelines for depression.*Authorea Preprints*.
- Dang, L. D., Phan, U. T., & Nguyen, N. T. (2023). Gena: A knowledge graph for nutrition and mental health. *Journal of Biomedical Informatics*, *145*, 104460.
- De Choudhury, M., Gamon, M., Counts, S., & Horvitz, E. (2013). Predicting depression via social media. In *Proceedings of the international aaai conference on web and social media.*- De Choudhury, M., et al. (2016). Discovering shifts to suicidal ideation from mental health content in social media. In*CHI conference on human factors in computing systems.*- Erol, T., Mendi, A. F., & Dogan, D. (2020). The digital twin revolution in healthcare. In ˘*2020 4th international symposium on multidisciplinary studies and innovative technologies (ismsit).*-*ETSI TS 103 410-8 V1.1.1 (2020-07) SmartM2M; Extension to SAREF; Part 8: eHealth/Ageing-well Domain.*(2020).
- Ferdousi, R., Laamarti, F., & El Saddik, A. (2022). Digital twins for well-being: an overview.*Digital Twin*.
- Fu, C., Jiang, X., He, T., & Jiang, X. (2021). Mdepressionkg: a knowledge graph for metabolismdepression associations. In *Proceedings of the 2nd international symposium on artificial intelligence for medicine sciences*(pp. 63–68).
- Gámez Díaz, R., Yu, Q., Ding, Y., Laamarti, F., & El Saddik, A. (2020). Digital twin coaching for physical activities: A survey.*Sensors*.
- Garcia-Ceja, E., et al. (2016). Automatic Stress Detection in Working Environments from Smartphones' Accelerometer Data: a First Step. *Journal of Biomedical and Health Informatics*.
- Garcia-Ceja, E., et al. (2018). Mental Health Monitoring with Multimodal Sensing and Machine Learning: A survey. *Elsevier Pervasive and Mobile Computing Journal (IF: 2.974 in 2017)*.
- Garguilo, J. J., Martinez, S., et al. (2007). Moving toward semantic interoperability of medical devices. In *Workshop on high confidence medical devices, software, and systems and medical device plugand-play interoperability.*- Gaur, M., Alambo, A., Sain, J. P., Kursuncu, U., Thirunarayan, K., Kavuluru, R., . . . Pathak, J. (2019). Knowledge-aware assessment of severity of suicide risk for early intervention. In*The world wide web conference.*- Gaur, M., Aribandi, V., Alambo, A., Kursuncu, U., Thirunarayan, K., Beich, J., . . . Sheth, A. (2021). Characterization of time-variant and time-invariant assessment of suicidality on reddit using c-ssrs.*PloS one*.
- Gaur, M., Faldu, K., & Sheth, A. (2021). Semantics of the black-box: Can knowledge graphs help make deep learning systems more interpretable and explainable? *IEEE Internet Computing*.
- Gaur, M., Gunaratna, K., et al. (2022). Iseeq: Information seeking question generation using dynamic meta-information retrieval and knowledge graphs. In *Aaai conference on artificial intelligence.*- Gaur, M., Kursuncu, U., Alambo, A., Sheth, A., Daniulaityte, R., Thirunarayan, K., & Pathak, J. (2018). "Let me tell you about your mental health!" Contextualized classification of reddit posts to DSM-5 for web-based intervention. In*ACM Conference on Information and Knowledge Management.*- Gaur, M., & Sheth, A. (2024). Building trustworthy neurosymbolic ai systems: Consistency, reliability, explainability, and safety.*AI Magazine*.
- Gedam, S., & Paul, S. (2021). A review on mental stress detection using wearable sensors and machine learning techniques. *IEEE Access*.
- Gkotsis, G., Oellrich, A., Velupillai, S., Liakata, M., Hubbard, T. J., et al. (2017). Characterisation of mental health conditions in social media using informed deep learning. *Scientific reports*.
- Gruber, T. R. (1995). Toward principles for the design of ontologies used for knowledge sharing? *Elsevier International journal of human-computer studies*.
- Gupta, S., Agarwal, A., Gaur, M., Roy, K., Narayanan, V., Kumaraguru, P., & Sheth, A. (2022). Learning to automate follow-up question generation using process knowledge for depression triage on reddit posts. In *Workshop on computational linguistics and clinical psychology.*- Gutierrez, L. J., Rabbani, K., et al. (2021). Internet of things for mental health: Open issues in data acquisition, self-organization, service level agreement, and identity management.*International Journal of Environmental Research and Public Health*.
- Gyrard, A., & Boudaoud, K. (2022). Interdisciplinary IoT and Emotion Knowledge Graph-Based Recommendation System to Boost Mental Health.
- Gyrard, A., Jaimini, U., Gaur, M., Shekarpour, S., Thirunarayan, K., & Sheth, A. (2022). Reasoning Over Personalized Healthcare Knowledge Graph: A Case Study of Patients with Allergies and Symptoms. In *Semantic Models in IoT and e-Health Applications.*Elsevier.
- Gyrard, A., & Kung, A. (2022). SAREF4EHAW-Compliant Knowledge Discovery and Reasoning for IoT-based Preventive Healthcare and Well-Being. In*Semantic Models in IoT and e-Health Applications.*Elsevier.
- Gyrard, A., & Sheth, A. (2020). IAMHAPPY: Towards An IoT Knowledge-Based Cross-Domain Well-

Being Recommendation System for Everyday Happiness.*IEEE/ACM Conference on Connected Health: Applications, Systems and Engineering Technologies (CHASE) Conference*.

- Gyrard, A., Tabeau, K., Fiorini, L., Kung, A., et al. (2021). Knowledge Engineering Framework for IoT Robotics Applied to Smart Healthcare and Emotional Well-Being. *International Journal of Social Robotics 2021. Springer.*.
- Hadzic, M., Chen, M., & Dillon, T. S. (2008). Towards the mental health ontology. In*2008 ieee international conference on bioinformatics and biomedicine*(pp. 284–288).
- Hastings, J., Ceusters, W., Smith, B., & Mulligan, K. (2011). The emotion ontology: enabling interdisciplinary research in the affective sciences.*Modeling and Using Context*.
- Hastings, J., et al. (2012). Representing Mental Functioning: Ontologies for Mental Health and Disease. In *International conference on biomedical ontology (icbo).*- Hua, Y., Liu, F., Yang, K., Li, Z., Sheu, Y.-h., Zhou, P., . . . Beam, A. (2024). Large language models in mental health care: a scoping review.*arXiv preprint arXiv:2401.02984*.
- Huang, Z., Yang, J., van Harmelen, F., & Hu, Q. (2017). Constructing knowledge graphs of depression. In *Health information science: 6th international conference, his 2017, moscow, russia, october 7-9, 2017, proceedings 6*(pp. 149–161).
- Ji, S., Zhang, T., Ansari, L., Fu, J., Tiwari, P., & Cambria, E. (2021). Mentalbert: Publicly available pretrained language models for mental healthcare.*arXiv preprint arXiv:2110.15621*.
- Joyce, D. W., Kormilitzin, A., Smith, K. A., & Cipriani, A. (2023). Explainable artificial intelligence for mental health through transparency and interpretability for understandability. *npj Digital Medicine*.
- Jung, H., Park, H.-A., & Song, T.-M. (2017). Ontology-based approach to social data sentiment analysis: detection of adolescent depression signals. *Journal of Medical Internet Research (IF: 4.671 in 2017)*.
- Jung, H., Park, H.-A., Song, T.-M., Jeon, E., Kim, A. R., & Lee, J. Y. (2015). Development of an Adolescent Depression Ontology for Analyzing Social Data. *Studies in Health Technology and Informatics*.
- Kabat-Zinn, J. (2003). Mindfulness-based stress reduction (MBSR). *Constructivism in the Human Sciences*.
- Kim, J.-Y. e. a. (2017). Unobtrusive Monitoring to Detect Depression for Elderly with Chronic Illnesses. *IEEE Sensors Journal (IF: 3.076 in 2020)*.
- Kursuncu, U., Gaur, M., Lokala, U., Illendula, A., Thirunarayan, K., Daniulaityte, R., . . . Arpinar, I. B. (2018). What's ur type? contextualized classification of user types in marijuana-related communications using compositional multiview embedding. In *2018 ieee/wic/acm international conference on web intelligence (wi)*(pp. 474–479).
- Laamarti, F., Badawi, H. F., Ding, Y., Arafsha, F., Hafidh, B., & El Saddik, A. (2020). An iso/ieee 11073 standardized digital twin framework for health and well-being in smart cities.*IEEE Access*.
- Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., . . . others (2020). Retrievalaugmented generation for knowledge-intensive nlp tasks. *Advances in Neural Information Processing Systems*, *33*, 9459–9474.
- Liu, Y., Zhang, L., Yang, Y., Zhou, L., Ren, L., Wang, F., . . . Deen, M. J. (2019). A novel cloud-based framework for the elderly healthcare services using digital twin. *IEEE Access*, *7*, 49088–49101.
- Lokala, U., Lamy, F., Daniulaityte, R., Gaur, M., Gyrard, A., Thirunarayan, K., . . . Sheth, A. (2022). Drug abuse ontology to harness web-based data for substance use epidemiology research: ontology development study. *JMIR public health and surveillance*.
- Lokala, U., Srivastava, A., Dastidar, T. G., Chakraborty, T., Akhtar, M. S., Panahiazar, M., & Sheth, A. (2022). A computational approach to understand mental health from reddit: knowledge-aware multitask learning framework. In *Proceedings of the international aaai conference on web and social media*(Vol. 16, pp. 640–650).
- Lu, H., et al. (2012). StressSense: Detecting Stress in Unconstrained Acoustic Environments Using Smartphones. In*Ubiquitous computing (ubicomp, a-rank conference).*- Manas, G., Aribandi, V., Kursuncu, U., Alambo, A., Shalin, V. L., Thirunarayan, K., . . . others (2021). Knowledge-infused abstractive summarization of clinical diagnostic interviews: Framework development study.*JMIR Mental Health*.

- Minaee, S., Mikolov, T., Nikzad, N., Chenaghlu, M., Socher, R., Amatriain, X., & Gao, J. (2024). Large language models: A survey. *arXiv preprint arXiv:2402.06196*.
- Mohammadi, S., Raff, E., Malekar, J., Palit, V., Ferraro, F., & Gaur, M. (2024). Welldunn: On the robustness and explainability of language models and large language models in identifying wellness dimensions. *arXiv preprint arXiv:2406.12058*.
- Mullick, S., Singh, A. K., Shaw, A. K., et al. (2022). Iot based smart system to detect mental health emergencies: A proposed model. *American Journal of Science & Engineering*.
- Muthalagu, R., Ramachandran, R., Anupama, P., et al. (2023). Pattern recognition and modelling in electrocardiogram signals: Early detection of myocardial ischemia and infraction. In *2023 2nd international conference on edge computing and applications (icecaa)*(pp. 1035–1041).
- Noy, N. F., Shah, N. H., Whetzel, P. L., Dai, B., Dorf, M., Griffith, N., . . . others (2009). Bioportal: ontologies and integrated data resources at the click of a mouse.*Nucleic acids research*.
- Ponmalar, A., & Anand, J. (2024). Iomt-based caring system for aged people in a post-covid scenario. In *Internet of medical things in smart healthcare*(pp. 207–224). Apple Academic Press.
- Rawte, V., Sheth, A., & Das, A. (2023). A survey of hallucination in large foundation models.*arXiv preprint arXiv:2309.05922*.
- Rejeb, A., Keogh, J. G., Martindale, W., Dooley, D., Smart, E., Simske, S., . . . others (2022). Charting past, present, and future research in the semantic web and interoperability. *Future internet*.
- Roy, K., Sheth, A., & Gaur, M. (2023). Alleviate chatbot. *UMBC Faculty Collection*.
- Roy, K., Zi, Y., Gaur, M., Malekar, J., Zhang, Q., Narayanan, V., & Sheth, A. (2023). Process knowledge-infused learning for clinician-friendly explanations. In *Aaai symposium series.*- Saha, K., Chandrasekharan, E., & De Choudhury, M. (2019). Prevalence and psychological effects of hateful speech in online college communities. In*Acm conference on web science.*- Sarkar, S., Gaur, M., Srivastava, B., et al. (2023). A review of the explainability and safety of conversational agents for mental health to identify avenues for improvement.*Frontiers in AI*.
- Seligman, M. E. (2008). Positive health. *Applied psychology*.
- Sheth, A., Gaur, M., Roy, K., & Faldu, K. (2021). Knowledge-intensive language understanding for explainable ai. *IEEE Internet Computing*.
- Sheth, A., Gaur, M., Roy, K., Venkataraman, R., & Khandelwal, V. (2022). Process knowledge-infused ai: Toward user-level explainability, interpretability, and safety. *IEEE Internet Computing*.
- Sheth, A., Padhee, S., & Gyrard, A. (2019). Knowledge Graphs and Knowledge Networks The Story in Brief.
- Shing, H.-C., et al. (2018). Expert, crowdsourced, and machine assessment of suicide risk via online postings. In *Computational linguistics and clinical psychology: from keyboard to clinic workshop.*- Srividya, M., Mohanavalli, S., & Bhalaji, N. (2018). Behavioral modeling for mental health using machine learning algorithms.*Journal of medical systems*.
- Su, C. e. a. (2020). Deep learning in mental health outcome research: a scoping review. *Translational Psychiatry*.
- Thiruvalluru, R. K., Gaur, M., Thirunarayan, K., Sheth, A., et al. (2021). Comparing suicide risk insights derived from clinical and social media data. *AMIA Summits on Translational Science Proceedings*.
- Tilwani, D., Saxena, Y., Mohammadi, A., Raff, E., Sheth, A., Parthasarathy, S., & Gaur, M. (2024). Reasons: A benchmark for retrieval and automated citations of scientific sentences using public and proprietary llms. *arXiv preprint arXiv:2405.02228*.
- Turab, M. e. a. (2023). A comprehensive survey of digital twins in healthcare in the era of metaverse. *BioMedInformatics*.
- Vajre, V., et al. (2021). PsychBERT: a mental health language model for social media mental health behavioral analysis. In *International conference on bioinformatics and biomedicine.*- Vandenbussche, P.-Y., Atemezing, G. A., Poveda-Villalón, M., & Vatant, B. (2016). Linked Open Vocabularies (LOV): a Gateway to Reusable Semantic Vocabularies on the Web.*Semantic Web J*.
- van der Maden, W., Lomas, D., & Hekkert, P. (2023). Positive ai: Key challenges for designing wellbeing-aligned artificial intelligence. *arXiv preprint arXiv:2304.12241*.
- Yamada, D. B., Yoshiura, V. T., Miyoshi, N. S. B., de Lima, I. B., Shinoda, G. Y. U., et al. (2018). Proposal of an ontology for mental health management in brazil. *Procedia computer science*.

- Yang, K., Zhang, T., Kuang, Z., et al. (2023). Mentalllama: Interpretable mental health analysis on social media with large language models. *arXiv preprint 2309.13567*.
- Yang, Z., Khatibi, E., Nagesh, N., et al. (2024). ChatDiet: Empowering personalized nutrition-oriented food recommender chatbots through an LLM-augmented framework. *Smart Health*.
- Yoon, S., Sim, J. K., & Cho, Y.-H. (2016). A Flexible and Wearable Human Stress Monitoring Patch. *Nature Scientific Reports Journal (IF: 4.122 in 2017)*.
- Zenonos, A., et al. (2016). Healthyoffice: Mood recognition at work using smartphones and wearable sensors. In *International conference on pervasive computing and communication workshops.*- Zhang, S., Dong, L., Li, X., Zhang, S., Sun, X., Wang, S., . . . others (2023). Instruction tuning for large language models: A survey.*arXiv preprint arXiv:2308.10792*.
- Zhang, T., Schoene, A. M., Ji, S., & Ananiadou, S. (2022). Natural language processing applied to mental illness detection: a narrative review. *NPJ digital medicine*, *5*(1), 1–13.
- Zhang, X., & Chen, J. (2020). Understanding information resources for college student mental health: A knowledge graph approach. *iConference 2020 Proceedings*.
- Zhang, Y., Li, Y., Cui, L., Cai, D., et al. (2023). Siren's song in the ai ocean: a survey on hallucination in large language models. *arXiv preprint arXiv:2309.01219*.
- Zhou, D., Luo, J., Silenzio, V. M., Zhou, Y., Hu, J., Currier, G., & Kautz, H. (2015). Tackling Mental Health by Integrating Unobtrusive Multimodal Sensing. In *Conference on artificial intelligence.*


## TL;DR
Proposes IoT-based preventive mental health framework using knowledge graphs and standards for semantic data integration and personalized well-being monitoring.

## Key Insights
Presents Mental Health Knowledge Graph (ontology and dataset) integrated with IoT Digital Twins using domain-specific standards and semantic web technologies for preventive mental health care with heterogeneous data integration capabilities

## Metadata Summary
### Research Context
- **Research Question**: How can IoT-based digital twin technologies and knowledge graphs be integrated with semantic web standards to enable preventive mental health care through heterogeneous data fusion and real-time personalized monitoring?
- **Methodology**: Systematic literature review; Standards analysis; Ontology engineering; Knowledge graph construction; Multi-source data integration methodology; Semantic mapping between ontologies and standards; Framework design for IoT-healthcare integration
- **Key Findings**: Mental Health Knowledge Graph successfully integrates multiple ontology-based projects; LOV4IoT catalog provides comprehensive mental health ontology classification; Semantic mappings established between health standards and knowledge bases; Framework demonstrates successful integration of IoT data with clinical knowledge; Digital twin approach enables real-time monitoring and personalized interventions; Standards analysis reveals comprehensive coverage across multiple organizations

### Analysis
- **Limitations**: Limited empirical validation of integrated framework in real-world healthcare settings; Complexity of maintaining semantic mappings across evolving standards; Privacy and ethical considerations for personal health data integration not fully addressed; Scalability challenges for large-scale deployment across diverse healthcare environments
- **Future Work**: Conduct clinical trials to validate framework effectiveness in real healthcare environments; Develop privacy-preserving semantic integration techniques for sensitive mental health data; Create user-centered design methodologies for diverse patient populations; Establish regulatory compliance frameworks for IoT-healthcare integration; Implement comprehensive evaluation of prevention outcomes and cost-effectiveness; Develop automated ontology evolution and maintenance systems