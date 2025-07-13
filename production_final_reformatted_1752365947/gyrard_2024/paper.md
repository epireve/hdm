---
cite_key: gyrard_2024
title: IoT-Based Preventive Mental Health Using Knowledge Graphs and Standards for Better Well-Being
authors: Amelie Gyrarda, Seyedali Mohammadi, Manas Gaur, Antonio Kung, Mental Health
year: 2024
date_processed: 2025-07-02
phase2_processed: true
original_folder: arxiv_2406.13791_IoT-Based_Preventive_Mental_Health_Using_Knowledge
images_total: 2
images_kept: 2
images_removed: 0
tags: 
keywords: 
---

# IoT-Based Preventive Mental Health Using Knowledge Graphs and Standards for Better Well-Being

Amelie Gyrarda,c,*, Seyedali Mohammadi^b^, Manas Gaur^b^ and Antonio Kung^a^

^a^Trialog, Paris, France; ^b^University of Maryland, Baltimore County (UMBC), USA; ^c^Machine-to-Machine Measurement (M3), Paris, France

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

More than one-fifth of adults in the United States have dealt with mental health issues, according to the National Institute of Mental Health^1^. This situation has led to the government setting aside $280 billion to improve the availability and quality of mental health services^2^. Mental health can increase productivity and efficiency, improve staff morale, and reduce absenteeism (Albraikan, 2019). There are numerous reviews on mental health using Wearable sensors and Artificial Intelligence Techniques (Gedam & Paul, 2021). Sustainable Development Goals (SDGs)^3^ give the UN a road map for development with Agenda 2030 as a target. SDG3 "Good Health and Well-Being" ensures healthy lives and promotes well-being for all ages. Digital technologies can support SDG3. We review hereafter definitions relevant to mental health, the need for Digital Twin for Mental Health, and the benefit of a Knowledge Graph (KG). Mental health^4^ is a state of mental well-being that enables people to cope with the stresses of life, realize their abilities, learn well, and work well, and contribute to their community. It has intrinsic and instrumental value and is integral to our well-being. IEEE 7010 defines well-being as "the continuous and sustainable physical, mental, and social flourishing of individuals, communities, and populations where their economic needs are cared for within a thriving ecological environment." Stress vs. Anxiety: People under stress^5^ experience mental and physical symptoms, such as irritability, anger, fatigue, muscle pain, digestive troubles, and difficulty sleeping. Anxiety, on the other hand, is defined by persistent, excessive worries that don't go away even in the absence of a stressor^6^. Burnout and even depression^7^ could be reduced by encouraging better preventive health. Lack of patient knowledge and focus to take care of their health before it is too late. New trends such as positive psychology (Seligman, 2008) and mindfulness (MBSR) (Kabat-Zinn, 2003) are highly encouraged in the USA. Depression is considered the main mental health crisis by the World Health Organization (WHO) (Mullick, Singh, Shaw, et al., 2022). Mental health includes emotional, psychological, and social well-being changes. DSM-V (Diagnostic and Statistical Manual of Mental Disorders)^8^ references more than 70 mental disorders that complement the International Classification of Diseases (ICD). DSM-V helps clinicians and researchers define and classify mental disorders, which can improve diagnoses, treatment, and research. DSM-V provides a form with checklists of symptoms for better diagnosis. Burnout does NOT appear in DSM and ICD. Mental illness is a type of health condition that changes a person's mind, emotions, or behavior and has been shown to impact an individual's physical health (Su, 2020). Depressive disorders, or unipolar depression's symptoms are low mood, loss of interest in day-to-day activities, significant weight changes, reduction of mobility, constant fatigue, difficulty concentrating, and feelings of worthlessness that can be diagnosed, and severity, using the Patient Health Questionnaire-9 (PHQ-9) (Gutierrez, Rabbani, et al., 2021).

<a id="ref-1"></a>^1^https://www.nimh.nih.gov/health/statistics/mental-illness

<a id="ref-2"></a>^2^https://www.whitehouse.gov/cea/written-materials/2022/05/31/reducing-the-economic-burden-of-unmet-mental-health-needs/

<a id="ref-3"></a>^3^https://sdgs.un.org/goals

<a id="ref-4"></a>^4^https://www.who.int/health-topics/mental-health#tab=tab_1

<a id="ref-5"></a>^5^https://www.apa.org/topics/stress/anxiety-difference

<a id="ref-6"></a>^6^https://www.apa.org/topics/stress/anxiety-difference

<a id="ref-7"></a>^7^https://www.who.int/news-room/fact-sheets/detail/depression

<a id="ref-8"></a>^8^https://www.psychiatry.org/psychiatrists/practice/dsm

The necessity of AI-enabled IoT Digital Twin using knowledge graph for achieving SDG-3: An IoT Digital Twin designed for proactive mental health care corresponds with four of the United Nations' Sustainable Development Goals. First is good health and well-being (SDG-3), which aims to ensure healthy lives and promote well-being for all age groups. We provide a pragmatic approach to developing IoT Digital Twin using domain-specific standards and knowledge graphs, which would advance mental health care and well-being. Disparities in mental health care access are prevalent, varying among regions, socioeconomic statuses, and genders. By prioritizing preventive strategies using domain-specific standards (e.g., questionnaires, guidelines) and leveraging AI-enabled IoT technology, this endeavor can potentially mitigate these access gaps, aligning with initiatives like the NIH's AIM-AHEAD Initiative.

Why do we need a Digital Twin for Mental Health? The StandICT landscape of Digital Twins (DT)^9^ reminds that "Digital Twin" was first introduced by Professor Michael Grieves from the University of Michigan in 2002. According to ISO/IEC 30173 Digital twin – concepts and terminology^10^, DTs are defined as a "digital representation of a target entity with data connections that enable convergence between the physical and digital states at an appropriate rate of synchronization." Notable implementation of DTs include Siemens Healthineers (Erol, Mendi, & Dogan, 2020), IBM Maximo Application Suite^11^ and Philips HeartModel^12^. DT can help with emotion monitoring using physiological signals (e.g., collected via wearables). Healthcare DTs facilitate monitoring, understanding, and optimization of human functioning and monitor health to improve quality of life and well-being (Laamarti et al., 2020), (Ferdousi, Laamarti, & El Saddik, 2022), (Albraikan, 2019), (Anand & Dhanalakshmi, 2024) with better personalization (Bagaria et al., 2020) by using digital technologies such as IoT, AI, etc. Healthcare DT challenges highlight the need for standardizing data format, communication protocols, and data-exchange mechanisms (Turab, 2023).

<a id="ref-9"></a>^9^https://www.standict.eu/landscape-analysis-report/landscape-digital-twin

<a id="ref-10"></a>^10^https://www.iso.org/standard/81442.html

<a id="ref-11"></a>^11^https://www.ibm.com/products/maximo

<a id="ref-12"></a>^12^https://www.philips.com/a-w/about/news/archive/blogs/innovation-matters/20181112-how-a-virtual-heart-could-save-your-real-one.html

Why do we need Knowledge Graphs for Mental Health? The European Human Brain Project (150 000 000 Euros, 161 partners), more precisely, the EBRAINS KG^13^, is a synergy project between neuroscience, computing, informatics, and brain-inspired technologies, encourages open-science through a web-based system to share tools, etc. However, when looking for keywords such as cortisol (the stress hormone), nothing can be found. KGs (Sheth, Padhee, & Gyrard, 2019) can use ontologies to structure data. An ontology provides a shared common understanding of a domain (Gruber, 1995). The use of ontologies is already recognized in the biomedical domain with BioPortal ontology catalog^14^. Ontology Development 101 methodology (designed by the creators of the Standford Protégé Ontology Editor tool) encourages reusing domain knowledge by reusing ontologies in Step 2 "Consider reusing ontologies."

In this paper, we describe about semantic interoperability applied to mental health, which is a follow-up of our health IoT semantic interoperability past work (Gyrard & Sheth, 2020) (Gyrard et al., 2022). Toward Converging Standards and Semantic Web Technologies applied to Mental Health: We illustrate the vision of our aligning technologies on Semantic Web and Data spaces and Standards such as ISO, IEC, and W3C as depicted in Figure 1. W3C Standards are more adapted to Semantic Web technologies such as W3C RDF, W3C RDFS, W3C OWL, W3C SPARQL, etc. Semantic Web technologies include knowledge Graphs with ontologies and Linked Data. There are also ISO standards about ontologies such as ISO/IEC 21838-1:2021 Information technology — Top-level ontologies (TLO) — Part 1: Requirements, ISO/IEC 21838-2:2021 Information technology — Top-level ontologies (TLO) — Part 2: Basic Formal Ontology (BFO), etc. Data Space initiatives such as BDVA, Gaia-X, etc. are considered. Some energy data spaces are designed by projects such as EDHS2, and TEHDAS. The list is not exhaustive. "Charting past, present, and future research in the semantic web and interoperability" highlights the importance of semantic interoperability (Rejeb et al., 2022) and on our past work: Table 5 "Top 20 most productive authors" and Figure 4 "Co-authorship network." The recommendation is that interoperability should remain a primary research focus and closer collaborations with industry, governments, and standards organizations to develop more effective models.

Our vision has been shared with the EUCloudEdgeIoT Concentration and Consultation Meeting on Computing Continuum: Uniting the European ICT community for a digital future in May 2023^15^.

The remainder of this chapter is organized as follows: related work limitations in Section 2, standards for mental health in Section 3, the mental health ontology catalog in Section 4 (which includes mapping to standards ontologies), the project use cases in Section 5, and conclusion in Section 6.

<a id="ref-13"></a>^13^https://search.kg.ebrains.eu/?facet_type[0]=Dataset&q=cortisol

<a id="ref-14"></a>^14^https://bioportal.bioontology.org/

<a id="ref-15"></a>^15^https://eucloudedgeiot.eu/concentration-and-consultation-meeting-on-computing-continuum-uniting-the-european-ict-community-for-a-digital-future/

![Standards, Semantic Web and Data Spaces applied to Health](_page_3_Figure_4.jpeg)

Figure 1.: Standards, Semantic Web and Data Spaces applied to Health

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

Conclusion: We focus on mental health disorders such as stress, and depression, and do not consider other disorders such as bipolar, or schizophrenia. Gutierrez et al. [[1]](#ref-1) only cite the mental health ontology from Hazdic et al. Hadzic, Chen, and Dillon (2008), and do not mention at all the KG term, so key research on depression ontologies and KGs are missing. For this reason, we built the ontology catalog as introduced in Section 4.1 and Table 2.

IoT-based Stress Detection is summarized in Table 1. Stress is a reaction from the human body in response to a challenging event or a demanding condition Gedam and Paul (2021); which can be detected using wearable sensors (e.g., Electrocardiogram, Electroencephalography, and Photoplethysmography) and applied machine learning. Activities such as driving, studying, and working are taken into consideration. Wearable healthcare-monitoring systems for pain and stress detection J. Chen, Abbod, and Shieh (2021)) are using wearable sensors to measure physiological signals such as heart, brain, muscle, electrodermal, respiratory, blood volume pulse, and skin temperature. A system to detect, diagnose and manage mental health emergencies Mullick et al. (2022); is based on four physiological parameters: heart rate, Spo2, body temperature (LM35 sensor), pressure (BMP180 sensor).

Digital Twin (DT) for Mental Health and Well-Being is summarized in Table 1. Digital Twin Coaching for Physical Activities's survey (Gámez Díaz, Yu, Ding, Laamarti, & El Saddik, 2020) explore papers from Scopus, Web of Science, IEEE Xplore and ACM Digital Library the last ten years (2010–2020). The papers have been classified into: 1) sports, 2) wellbeing, and 3) rehabilitation. The following information is extracted: 1) ML algorithms being used 2) Type of application being researched, 3) Sensors and actuators devices used, 4) Performance of the ML algorithm, 5) Usability feedback of users about the system. Digital Twin in healthcare (Turab, 2023) highlights the need for standardizing data format, communication protocols, and data-exchange mechanisms. Turab et al. highlight that ISO has an interest in Digital Twin. Indeed, we are involved in ISO SC 41 IoT and Digital Twin. Wellbeing digital twin (WDT) (Ferdousi et al., 2022) challenges for predictive wellbeing applications are technical issues of handling heterogeneous data and standards, data bias, level of autonomy, trust in intelligence, data visualization issues, and consent of humans. Drawbacks of WDT are: 1) Inadequate or missing data, 2) Ethical overheads, 3) Trust in AI, and 4) Necessity of domain knowledge. Well-being digital twin (WDT) areas are: 1) Collecting and managing vast healthcare data, 2) Meaningful data visualization, 3) Facilitating predictive healthcare, 4) Improving healthcare quality of experience (QoE), 5) Personalized healthcare system (e.g., digital coaching, elderly healthcare (e.g. device in Ponmalar and Anand (2024)), immune system care), and 6) Understanding clinical pathways. An ISO/IEEE 11073 standardized digital twin framework architecture for health and well-being to analyze data from personal health devices is compliant or not with X73 standards (Laamarti et al., 2020). inHarmony (Albraikan, 2019) is an Emotional Well-being DT for workplace which includes emotion detection, emotional biofeedback, and emotion-aware recommender systems. A usability study was carried out with 35 practitioners wearing the Empatica E4 sensor to acquire physiological signals. CloudDTH (Liu et al., 2019) is a DT Healthcare (DHT) framework for real-time monitoring, diagnosing, and predicting of elderly's health, based on cloud, and wearable medical devices technologies. A Big Data-based Precision Medicine Cloud Platform is designed to display human physiological health data for data management, data analysis, etc. DTs of patients and DTs of medical devices are considered (Erol et al., 2020). DT Siemens Healthineers (Erol et al., 2020) for radiology department in Mater Private Hospitals from Ireland to reduce patient's waiting time. Siemens Healthineers is also applied to cardiologists in a research project at Heidelberg University for patients with chronic congestive heart failure. Philips HeartModel^16^ is a personalized Digital Twin of the heart to help surgeons with real-time 3D. Its HeartNavigator tool combines the Computed Tomography (CT) heart anatomy obtained before the surgical procedure and live during the surgery. Sooma is a startup that simulates the electrical signals of the brain to treat depression, other neurological and psychiatric disorders.

Conclusion: We did not find a digital twin for mental health. inHarmony is addressing well-being.

AI-based Mental Health: "Positive AI" (van der Maden, Lomas, & Hekkert, 2023), means that AI systems actively and intentionally support human well-being based on fields such as positive psychology, human-centered design, and computing. The authors categorized twelve well-being AI challenges into 1) knowledge (how to conceptualize, operationalize, optimize for, and design), and 2) motivation (misaligned incentives, PR & monetary risks, and lack of access, preventing). To identify mental health states, machine learning algorithms such as support vector machines, decision trees, naïve Bayes classifier, K-nearest neighbor classifier, and logistic regression are used (Srividya, Mohanavalli, & Bhalaji, 2018).

Related work shortcomings: Those works do not use health standards that we are addressing in Section 3. Furthermore, in this chapter, we will focus on KGs (e.g., ontologies) as AI solutions as explained in Section 4.

<a id="ref-16"></a>^16^https://www.philips.com/a-w/about/news/archive/blogs/innovation-matters/20181112-how-a-virtual-heart-could-save-your-real-one.html

## 3 Standards for Mental Health and Well-Being: Artificial Intelligence (Semantic Web, Ontologies)

We investigate Standards Development Organizations (SDOs) for (mental) health covering AI (Semantic Web, Ontologies) such as: ETSI SmartM2M EHealth/Ageing-Well Ontology in Section 3.1, ITU/WHO Focus Group on Artificial Intelligence for Health in Section 3.2, ISO Health Standards in Section 3.3, W3C Health Standards in Section 3.4, NIST Health Standards in Section 3.5, and IEEE Health Standards in Section 3.6. Standards Development Organizations SDOs define health ontologies or IoT ontologies describing sensors to measure the physiological signals of patients as depicted in Figure 2.

![Standardized Ontologies](_page_6_Figure_6.jpeg)

Figure 2.: Standardized Ontologies

## *3.1 ETSI SmartM2M SAREF for EHealth/Ageing-Well Ontology*

ETSI Smart M2M SAREF4EHAW ontology (*ETSI TS 103 410-8 V1.1.1 (2020-07) SmartM2M; Extension to SAREF; Part 8: eHealth/Ageing-well Domain*, 2020) reviews standards such as IEEE, ETSI, SNOMED, OneM2M), Alliances (AIOTI), IoT Platforms, and European projects and initiatives, etc.

The use cases are classified into some of those categories: 1) Daily Activity Monitoring, 2) Cognitive simulation for mental decline prevention, 3) Prevention of social isolation, 4) Comfort and safety at home. SAREF4EHAW investigated the following ontologies: 1) WSNs/measurement ontologies: OGC (Open Geospatial Consortium) Observations & Measurements (O&M), Sensor Model Language (SensorML), Semantic Sensor Web (SWE): W3C & OGC SOSA (Sensing, Observation, Sampling, and Actuation) and W3C SSN (Semantic Sensor Network). NASA QUDT (Quantities, Units, Dimensions, and Types). 2) eHealth/Ageing-well domain main ontologies: ISO/IEEE 11073 Personal Health Device (PHD) standards, ETSI SmartBAN Reference Data Model and associated modular ontologies, FHIR RDF (Resource Description Framework), FIESTA-IoT Ontology to support the federation of testbeds, Bluetooth® LE (Low Energy) profiles for medical devices proposed by Zontinua, MIMU-Wear (Magnetic and Inertial Measurement Units) ontology, and Active and Healthy Ageing (AHA) platform wearables' device ontology. The document explains that SAREF has been mapped with oneM2M base ontology in 2017. SAREF4EHAW (*ETSI TS 103 410-8 V1.1.1 (2020-07) SmartM2M; Extension to SAREF; Part 8: eHealth/Ageing-well Domain*, 2020) selected 43 ontological requirements, and 59 service-level assumptions of the eHealth/Ageing-well domain (use cases included). For instance, as a requirement, the ontology describes ECG ((Muthalagu, Ramachandran, Anupama, et al., 2023)) device concepts. There is also SAREF4WEAR^17^ an extension for wearables.

Conclusion: SAREF4EHAW demonstrates the need for ontologies. We did not find standards more specific to mental health in ETSI.

<a id="ref-17"></a>^17^https://saref.etsi.org/saref4wear/

### *3.2 ITU/WHO Focus Group on Artificial Intelligence for Health*

ITU/WHO Focus Group on Artificial Intelligence for Health (FG-AI4H)^18^, established in 2018, free and open, partners with the World Health Organization (WHO) to standardize AI-based assessment framework and evaluation for health, diagnosis, triage or treatment decisions. It provides an AI for health online platform and complementary tools for benchmarking of data. FG-AI4H comprises experts: machine learning/AI researchers, healthcare practitioners and researchers, regulators, representatives of health ministries and ministries of telecommunication, international organizations, and individuals from complementary fields. The FG highlights the need for explainability and interpretability of AI tools. ITU-T/WHO FG-AI4H use cases: 24 AI4H use cases are introduced, including traditional medicine, psychiatry, neurological disorders, falls among the elderly, etc. DEL.10.23 TG-AI for Traditional Medicine reviews the existing AI solutions for Traditional Medicine. AI in traditional medicine will be relevant to support healthcare practitioners in recommending integrative medical practices. Traditional Medicine treatments: 1) Ontological and Natural language processing (NLP) are encouraged to extract useful information, 2) Analyzing and integrating data, and 3) Decision support, 4) Predictive analytics, 5) Patient monitoring and feedback, 6) virtual health assistants, and 7) Research and knowledge discovery.

Conclusion: We find a standard on AI Traditional Medicine, but we did not find standards for mental health in this SDO.

<a id="ref-18"></a>^18^https://www.itu.int/go/fgai4h

### *3.3 ISO Health Standards*

The CEN/ISO EN13606 is a European norm approved as an ISO standard to achieve EHR semantic interoperability. ISO 13606-5:2010 Health Informatics - Electronic Health Record communication standards^19^ defines an architecture for exchanging Electronic Health Record (EHR) describing patient's health status and ease communication between EHR systems (e.g., clinicians applications, decision support systems). ISO 13606 seems an open standard. Within the ISO SC41 IoT and Digital Twin, there is an ongoing standard entitled "IoT/IEC 30197 IoT for Stress Management, Good health & Well-being". ISO SC42 AI - "AI-enabled Health Informatics" is a joint working group that will provide a landscape survey and a set of recommendations for future work on the impact of ISO/TC 215 standards. The group comprises experts from ISO/IEC/JTC 1/SC 42, IEEE, and the ITU/WHO AI4Health focus group. ISO/IEEE 11073 medical device communication standard - Used by Personal Connected Health Alliance (PCHAlliance) - X73 standards facilitates health data exchange while providing plug-and-play real-time interoperability by being compliant with the X73 communication model. However, the X73 standards do not address security or users' privacy. This ISO/IEEE 11073 standard is used by Laamarti et al. (2020) for a digital twin framework architecture for health and well-being in smart cities. NIST researchers are collaborating with medical device experts to develop standards for medical device communications to enhance semantic interoperability. XML schema and tool based on the ISO/IEEE 11073 medical device communication standard is developed by Garguilo et al. (Garguilo, Martinez, et al., 2007). Personal Connected Health Alliance (PCHAlliance) products use the ISO/IEEE 11073 Personal Health Data (PHD) Standards.

Conclusion: ISO 215 Health Informatics must be explored further to dig any documents related to mental health. CEN/ISO EN13606 focuses on EHR semantic interoperability. ISO SC42 AI joint working group "AI-enabled Health Informatics" comprises experts from ISO/IEC/JTC 1/SC 42, IEEE, and the ITU/WHO AI4Health focus group.

<a id="ref-19"></a>^19^http://www.en13606.org/information.html

## *3.4 W3C Semantic Web Health Care and Life Sciences Community Group (HCLS CG)*

W3C Semantic Web (SW) Health Care and Life Sciences Community Group (HCLS CG)^20^ encourages the use of SW technologies across health care, life sciences, clinical research and translational medicine as they need interoperability of information from many disciplines. HCLS CG use SW technologies to design use cases which have a clinical, research of business values. The CG develops liaisons with organizations in healthcare, life sciences, and clinical research, including organizations that are working on standards.

Conclusion: W3C HCLS CG highlights the need of using Semantic Web. The final report is more focused on drug-drug interaction. We did not find standards specific to mental health.

<a id="ref-20"></a>^20^https://www.w3.org/community/hclscg/

## *3.5 NIST Health Standards*

NIST researchers are collaborating with medical device experts to develop standards for medical device communications to enhance semantic interoperability. XML schema and tool based on the ISO/IEEE 11073 medical device communication standard (Garguilo et al., 2007).

Conclusion: NIST has an interest in semantic interoperability.

## *3.6 IEEE Health Standards*

IEEE digital health standards can help save lives and improve people's quality of life. Standards aim to share information across end-to-end infrastructure, particularly: 1) interoperability: information exchange among organizations, 2) cost savings/efficiency (e.g., for hospitals), etc. We selected four standards: 1) IEEE 7010's definition of well-being (mentioned earlier), 2) IEEE 1752.1-2021 Standard for Open Mobile Health Data–Representation of Metadata, Sleep, and Physical Activity Measures, 3) ISO/IEEE 11073 medical device communication standard, and 4) IEEE P1157 Medical Data Interchange (MEDIX). IEEE 1752.1-2021 Standard for Open Mobile Health Data–Representation of Metadata, Sleep, and Physical Activity Measures^21^ eases semantic interoperability across mobile health sources and provides meaningful description, exchange, sharing, and use of such mHealth data for consumer health, biomedical research, and clinical care stakeholders. NIST researchers are collaborating with medical device experts to develop standards for medical device communications to enhance semantic interoperability. XML schema and tool based on the ISO/IEEE 11073 Medical Device Communication standard (Garguilo et al., 2007). IEEE P1157 Medical Data Interchange (MEDIX) is a standard for communication of medical information between heterogeneous healthcare information systems such as between a patient care system and selected ancillaries in the medical center setting. IEEE 1157 Standard for Health Data Interchange is designed with health care professionals.

Conclusion: Within IEEE 7010, we found a standard explaining the definition of well-being. Understanding well-being will help as a preventive solution to reduce mental health problems.

<a id="ref-21"></a>^21^https://standards.ieee.org/ieee/1752.1/6982/

### *3.7 Standards: Conclusion*

We did not find standards for mental health in those SDOs: ETSI SmartM2M, ITU/WHO FG-AI4H, and W3C HCLS CG. ISO 215 Health Informatics must be explored further to dig any documents related to mental health. CEN/ISO EN13606 focuses on EHR semantic interoperability. We are involved in "IoT for Stress Management, Good health & Well-being, a standard under development within ISO SC41 IoT. ISO SC42 AI joint working group "AI-enabled Health Informatics" comprises experts from ISO/IEC/JTC 1/SC 42, IEEE, and the ITU/WHO AI4Health focus group.

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

## *4.1 LOV4IoTMental Health Ontology Catalog and Knowledge Graph*

We have designed an ontology catalog for depression and mental health, called LOV4IoT Mental Health^22^ (Table 2).

GENA (Graph of mEntal-health and Nutrition Association) (Dang, Phan, & Nguyen, 2023)^23^ encodes relationships between nutrition and mental health. GENA describes food, biochemicals, and mental illnesses extracting knowledge from PubMed. GENA consists of 43,367 relationships with concepts such as nutrition, biochemical, mental health, chemical, and disease. GENA used ontologies such as Human Disease Ontology (DOID), Chemical Entities of Biological Interest Ontology (CHEBI), Foundational Model of Anatomy (FMA), Disorders cluster (APADISOR-DERS), Autism Spectrum Disorder Phenotype Ontology (ASDTTO), The FoodOn Food Ontology (FOODON), MFO Mental Disease Ontology (MFOMD), Protein Ontology (PR), and Symptom Ontology (SYMP). As an example, CHEBI, FMA, is used as explained in Section 4.3.

DSM-V (Diagnostic and Statistical Manual of Mental Disorders)^24^ references more than 70 mental disorders that complement the International Classification of Diseases (ICD). DSM-V helps clinicians and researchers define and classify mental disorders, which can improve diagnoses, treatment, and research. DSM-V provides a checklist form of symptoms for better diagnosis. As an example, DSM-V is used as explained in Section 5.3.

<a id="ref-22"></a>^22^http://lov4iot.appspot.com/?p=lov4iot-depression

<a id="ref-23"></a>^23^https://github.com/ddlinh/gena-db

<a id="ref-24"></a>^24^https://www.psychiatry.org/psychiatrists/practice/dsm

Mental Health Ontology (Hadzic et al., 2008) comprises three sub-ontologies: 1) disorder/illness types, (2) factors, and (3) treatments. Disorders types are anxiety disorder, eating disorder, childhood disorder, cognitive disorder, mood disorder. Factors can be: 1) Physical (e.g. vitamin B deficiency, health injury, liver disease), 2) Environmental (E physical, social, financial), 3) Personal (belief, emotion, response). The need to understand emotions like stress, anger, bitterness, guilt, joy, happiness, peace, and fear, since they directly affect mental health is highlighted by Hadzic et al. (2008).

Mental Functioning (MF) Ontology and Mental Disease (MD) Ontology^25^ (Hastings et al., 2012) describe human mental functioning and disease, including mental processes such as cognitive processes and qualities such as intelligence. MF Ontology is based on Basic Formal Ontology (BFO). MD ontology covers concepts such as disease, diagnosis, disorder, and addiction. Mental Functioning Ontology and Mental Disease Ontology could be used to map answers from clinical interview questionnaires about mood, psychotic disorders, and related spectrum conditions. Hastings et al. also designed emotion ontology. Mapping to https://obofoundry.org/ontology/mfomd.html (Hastings et al., 2012) is not simple since there are no labels or comments within the ontology code but concepts IRI such as MFOMD_0000040. Fortunately, the URI are deferenceable which means that if we copy and paste https://ontobee.org/ontology/MFOMD?iri=http://purl.obolibrary.org/obo/MFOMD_0000040 we can get additional information such as the definition: "A diagnosis asserting the presence of an instance of a mental disease in a given organism."

Depression KG (Huang et al., 2017) is a disease-centric KG applied to Major Depressive Disorder, which addresses several challenges: (1) Heterogeneity of datasets, (2) text processing, (3) incompleteness, inconsistency, and incorrectness of datasets, and (4) expressive, representation of medical knowledge. Depression KG utilizes rulebased reasoning over the KG, which helps psychiatric doctors without KG expertise. MDepressionKG (Fu, Jiang, He, & Jiang, 2021) integrates the human microbial metabolism network, human diseases, microbes and other ontologies. Ontology for College Student Mental Health Service (CSMH) (X. Zhang & Chen, 2020) describes appointments, mental disorders, self-help resources, information for parents, local referral sources, and substance abuse prevention. Some of the information is extracted from two CSMH websites. Ontology for mental disorders - Schizophrenia Spectrum Ontology (Amoretti et al., 2019), is compliant with DSM-5 descriptions of mental disorders, with a specific focus on Schizophrenia. It comprises 58 classes (Mental_Disorder, Patient, and Symptom), 5 properties, and 191 axioms. Classes of the Schizophrenia Spectrum category and the associated symptoms are defined. Future work is planned to address borderline personality disorder or major depression. Ontology for managing mental healthcare network in Brazil (Yamada et al., 2018), based on BFO, used for integration and interoperability between databases and to design a Semantic Web-based Decision Support System (DSS) for a regional mental healthcare network in Brazil for clinical and administrative processes. The challenges of dealing with standardization and low-quality data are highlighted. The competency question is whether a manager wants to know how many people had schizophrenia in the city of São Paulo in 2017 without looking at various systems of hospitals in the city.

<a id="ref-25"></a>^25^https://obofoundry.org/ontology/mfomd.html

### *4.2 Mapping to Standards: ETSI SmartM2M SAREF4EHAW*

The mapping to the ETSI SmartM2M SAREF4EHAW ontology is already explained within the book chapter "SAREF4EHAW-Compliant Knowledge Discovery and Reasoning for IoT-based Preventive Healthcare and Well-Being" (Gyrard & Kung, 2022). The mapping focuses on the sensor type used.

## *4.3 Mapping to Standardized Health KGs/Ontologies/Terminologies: SNOMED-CT, FMA, RXNORM, MedDRA, LOINC, ChEBI, MESH, GALEN and DBpedia*

The mapping to health knowledge bases is explained within "Interdisciplinary IoT and Emotion Knowledge Graph-Based Recommendation System to Boost Mental Health" (Gyrard & Boudaoud, 2022). We mapped hormones and neurotransmitters concepts. We searched key ontologies on the Bioportal ontology catalog, to be mapped with the Emotion KG. We found ontologies such as SNOMED-CT, Mapping Foundational Model of Anatomy (FMA), RXNORM, MedDRA, Logical Observation Identifier Names and Code (LOINC), Medical Subject Headings (MESH), GALEN, and Chemical Entities of Biological Interest Ontology (ChEBI). The mappings of hormones and neurotransmitters are summarized in two Tables "Subset of mapping hormones and neurotransmitters to existing knowledge bases to demonstrate the difficulty of reusing only one knowledge base." DBpedia is also used due to its popularity, and links emotion-related concepts to existing emotion ontologies when available online. Most of the emotion ontologies cannot be found on BioPortal; only Hastings's ontology (Hastings, Ceusters, Smith, & Mulligan, 2011) is referenced on BioPortal.

## 5 Ontology-Based Mental Health Recommender System and Project Use Cases: ACCRA, etc.

Project use cases are explained in this Section 5. Social robots to support active and healthy aging (ACCRA European-Japan Project) in Section 5.1, Large Language Models (LLMs) for Mental Health in Section 5.2, and other projects on Mental Health such as Depression and Suicide in Section 5.3.

## *5.1 ACCRA European-Japan Project: Social robots to support active and healthy aging*

To design emotional-based robotic applications, how can Internet of Robotic Things (IoRT) technology and co-creation methodologies be used? The ACCRA (Agile Co-Creation of Robots for Ageing) EU project^26^ (Gyrard et al., 2021), coordinated by Trialog, develops advanced social robots to support active and healthy aging, co-created by various stakeholders such as aging people and physicians. Three robots, Buddy, ASTRO, and RoboHon, are used for daily life, mobility, and conversation. The three robots understand and convey emotions in real-time using the Internet of Things and Artificial Intelligence technologies (e.g., knowledge-based reasoning). The ACCRA project explains that social companion robots assist elderly people in staying independent at home and decrease their social isolation. A challenge was to design applications usable by elderly people using co-creation methodologies involving multiple stakeholders and a multidisciplinary research team (e.g., elderly people, medical professionals, and computer scientists such as roboticists or IoT engineers).

<a id="ref-26"></a>^26^https://www.accra-project.org/en/sample-page/

## *5.2 Large Language Models (LLMs) for Mental Health*

Large Language Models (LLMs) have become increasingly popular due to their vast statistical knowledge, allowing them to produce fluent English sentences and exhibit human-like performance across tasks such as question-answering, summarization, and recommendations. The debut of ChatGPT on November 30, 2022, garnered considerable attention alongside similar autoregressive LLMs like Google BARD, Google GEMINI, and Anthropic Claude (Minaee et al., 2024). Despite their impressive performance, these LLMs have been criticized for providing confidently asserted yet factually inaccurate information, referred to as "hallucination" (Rawte, Sheth, & Das, 2023). This poses a significant challenge to their reliability and trustworthiness. Moreover, LLMs sometimes yield inconsistent answers, eroding trust in their outputs. Attention explanations (generated by models) do not closely align with the ground truth explanations provided by human experts (Mohammadi et al., 2024). When LLMs offer irrelevant explanations, it exacerbates trust issues, casting doubt on their reliability as tools (Y. Zhang, Li, Cui, Cai, et al., 2023). Consequently, their application in healthcare, particularly mental health, has been hindered. Although there are mental health-specific LLMs, their performance lacks consistency, reliability, explainability, and trust assessment (Gaur & Sheth, 2024).

Efforts to enhance these LLMs for better utility in healthcare have led to recent research focusing on instruction-tuned and retrieval-augmented (e.g. Tilwani et al. (2024)) LLMs (Lewis et al., 2020). Instruction tuning involves incorporating an additional feature called "instruction" into the dataset, which can be a guideline, protocol, or rule for the LLM to follow (Sheth, Gaur, Roy, Venkataraman, & Khandelwal, 2022; S. Zhang et al., 2023). However, such training methods have not proven very effective in sensitive domains. Recent work has shown that rules learned by LLMs after instruction tuning do not match the model's performance level, raising concerns about this training approach, particularly in areas akin to moral question answering, such as mental health. An empirical study by Gupta et al. (2022) demonstrates that LLMs struggle to complete clinical questionnaires for depression and anxiety. Subsequently, Roy, Zi, et al. (2023) proposed architecture changes, particularly in autoregressive language models, suggesting that a tree-based learning prediction layer could yield safer outcomes in mental health contexts. Further exploration at the intersection of instruction-tuned LLMs and mental health is warranted. Examples of publicly available mental health LLMs include ChatCBPTSD, Diagnosis of Thought Prompting (Z. Chen, Lu, & Wang, 2023), Mental-LLM (Alpaca/FLAN-T5 based), MentaLLaMA (LLaMA-2 based; (K. Yang, Zhang, Kuang, et al., 2023)), ChatCounselo, ExTES-LLaMA (both LLaMA based), and BBMHR (BlenderBot-BST based), while some, like MindShift, Psy-LLM, and LLM-Counselors (all GPT-3.5 based), remain unavailable to the public (Hua et al., 2024).

Retrieval-augmented LLMs represent another category, where a generator model is paired with a knowledge retriever capable of accessing documents from a vectorized database. These LLMs draw context from the retriever, offering reliability and domain-specific explainability crucial in domains like mental health. Gaur, Gunaratna, et al. (2022) demonstrated the extension of these LLMs to knowledge graphs. However, experimentation has primarily been limited to open-domain knowledgeintensive language understanding tasks, leaving its utility in mental health as an ongoing research question (Sarkar, Gaur, Srivastava, et al., 2023). An example of retrievalaugmented LLM is shown in openCHA (Z. Yang, Khatibi, Nagesh, et al., 2024). Abbasian, Azimi, Rahmani, and Jain (2023) developed openCHA, a framework that empowers health agents to enhance the processing of healthcare inquiries by efficiently analyzing input queries, integrating essential information, and offering personalized, context-aware responses.The framework's effectiveness in managing complex healthcare tasks through various expert-provided demonstrations. For example, Z. Yang et al. (2024) leveraged openCHA to create a personalized nutrition-oriented food recommendation chatbot, enabled by user's longitudinal data on diabetes, American Diabetes Association dietary guidelines, the Nutritionix information, personal causal models, and population models. On an evaluation includes 100 diabetes-related questions on daily meal choices and the potential risks associated with the diet, openCHA demonstrated superior performance compared to state-of-the-art GPT 4.

### *5.3 Other Projects on Mental Health*

Mental health professionals (MHPs) are overwhelmed by the rising prevalence of declining mental health (MH), depression, and suicide risk. Traditionally, they rely on time-consuming clinical questionnaires (e.g., DSM-5 assessment measures, strengths and difficulties questionnaires) and long patient interviews^27^. However, the growing demand for MH services and the shortage of MHPs motivate automated methods for early screening. However, it's important to note that receiving high-quality assistance is not guaranteed^28^. We require online screening assistance as an improvement over online consultations (e.g., BetterHelp), aiming for higher-quality support. AI has emerged as a promising tool for analyzing text data from various sources, including Electronic Health Records (EHR) and social media posts (Joyce, Kormilitzin, Smith, & Cipriani, 2023; Thiruvalluru, Gaur, Thirunarayan, Sheth, et al., 2021; T. Zhang, Schoene, Ji, & Ananiadou, 2022).

<a id="ref-27"></a>^27^https://wiki.aiisc.ai/index.php?title=Mental_Health_Projects

<a id="ref-28"></a>^28^https://wiki.aiisc.ai/index.php?title=Modeling_Social_Behavior_for_Healthcare_Utilization_in_Depression

Research in AI and Mental health can be broadly categorized into two categories: (a) Statistical data-driven machine learning in the realm of mental health, as exemplified by the contributions of De Choudhury, Gamon, Counts, and Horvitz (2013), De Choudhury et al. (2016), Saha, Chandrasekharan, and De Choudhury (2019), Chancellor and De Choudhury (2020), Shing et al. (2018) and Gkotsis et al. (2017), represents a significant advancement. However, while these studies showcase the effectiveness of AI in this domain, they are limited in their ability to instill trustworthiness, primarily due to a deficiency in explainability and interoperability, which could be greatly enhanced by incorporating domain-specific expertise. (b) Knowledge-driven Machine Learning for Mental Health: This comprises work involving clinical questionnaires for question answering, summarization, longitudinal assessment (Alambo et al., 2019; Gaur, Aribandi, et al., 2021; Gupta et al., 2022; Manas et al., 2021), a diagnostic statistical manual for mental health disorders for identifying mental health disorders (Gaur et al., 2018), and detecting and assessing the severity of substance use disorder using domain-specific drug abuse ontology (Kursuncu et al., 2018; Lokala, Lamy, et al., 2022; Lokala, Srivastava, et al., 2022). Machine-readable mental health knowledge has resulted in explainable classification and interpretable design of black-box language models and conversational agents (Dalal et al., 2024; Gaur, Faldu, & Sheth, 2021; Roy, Sheth, & Gaur, 2023). Further, datasets designed using such a knowledge are capable of examining grounding, instructability, and alignment of domain-specific language models (e.g., ClinicalBERT (Alsentzer et al., 2019), PsychBERT (Vajre et al., 2021), MentalBERT (Ji et al., 2021)) to the intent, needs, and requirements of MHPs (Gaur et al., 2019; Sheth, Gaur, Roy, & Faldu, 2021).

### 6 Conclusion and Future Work

A Mental Health KG (ontology and dataset) acquires knowledge from ontology-based projects classified within the LOV4IoT ontology catalog (Depression, Mental Health, and Emotion). LOV4IoT supports researchers with 1) the Systematic Literature Survey, which is a time-consuming task and requires an eagerness to learn and investigate existing projects, 2) FAIR principles to encourage researchers to share their reproducible experiments by publishing online ontologies, datasets, rules, etc.

Short-term challenges: LOV4IoT is relevant for the IoT community. The results are encouraging to update the dataset with additional domains and ontologies. LOV4IoT leads to the AIOTI (The Alliance for the Internet of Things Innovation) IoT ontology landscape survey form^29^ and analysis result^30^, executed by the Standard WG - Semantic Interoperability Expert Group. It aims to help industrial practitioners and non-experts answer those questions: Which ontologies are relevant in a certain domain? Where to find them? How to choose the most suitable? Who is maintaining and taking care of their evolution? There is also the AIOTI Health WG white paper publications on health data space "IoT/Edge Computing and Health Data and Data Spaces"^31^, "AI for better health"^32^, and "IoT Improving Healthy Urban Living"^33^.

Mid-term challenges: Automatic knowledge extraction from ontologies and scientific publications describing the ontology purpose is challenging, as highlighted in our AI4EU Knowledge Extraction for the Web of Things (KE4WoT) Challenge. The challenge encourages the reuse of the expertise designed by domain experts and makes the domain knowledge usable, interoperable, and integrated by machines. We released the set of ontologies, as dumps, web services, and tutorials, and made them available.

Long-term challenges: To improve the veracity and the evaluation of the KG integrated with a reasoning engine, involving domain experts such as psychologists, neuroscientists, etc. would enhance the KG, by proving more of the facts. The knowledge-based reasoning engine can be extended by considering additional research fields such as psychophysiology, psychobiology, etc. An emphasis on the emotional aspect can be done (e.g., fear, pessimism, sadness) since it impacts mental health.

<a id="ref-29"></a>^29^https://ec.europa.eu/eusurvey/runner/OntologyLandscapeTemplate

<a id="ref-30"></a>^30^https://bit.ly/3fRpQUU

<a id="ref-31"></a>^31^https://aioti.eu/aioti-white-paper-iot-edge-computing-and-health-data-and-data-spaces/

<a id="ref-32"></a>^32^https://aioti.eu/aioti-wg-health-white-paper-on-ai-for-better-health/

<a id="ref-33"></a>^33^https://aioti.eu/wp-content/uploads/2022/09/IoT-and-Healthy-Urban-Living-Final.pdf

### Acknowledgements and Funding

We want to acknowledge the Kno.e.sis research team (lead by Professor Amit Sheth) from Wright State University, Ohio, USA for fruitful discussions about related topics such as "Mental Health/Depression/Suicide", and "Semantic, Cognitive, and Perceptual Computing" and with cognitive psychologists such as Professor Valerie Shalin during Dr. Gyrard's post-doc in 2018-2019.

This work has partially received funding from the European Union's Horizon 2020 research and innovation program under project grant agreement StandICT.eu 2026 No. 101091933 (open call). We would like to thank the project partners for their valuable comments. The opinions expressed are those of the authors and do not reflect those of the sponsors.

### References

*   <a id="ref-Abbasian2023"></a>Abbasian, M., Azimi, I., Rahmani, A. M., & Jain, R. (2023). Conversational health agents: A personalized llm-powered agent framework.*arXiv preprint arXiv:2310.02374*.
*   <a id="ref-Alambo2019"></a>Alambo, A., Gaur, M., Lokala, U., Kursuncu, U., Thirunarayan, K., Gyrard, A., . . . Pathak, J. (2019). Question answering for suicide risk assessment using reddit. In *2019 ieee 13th international conference on semantic computing (icsc)*(pp. 468–473).
*   <a id="ref-Albraikan2019"></a>Albraikan, A. (2019).*inharmony: A digital twin for emotional well-being*(Unpublished doctoral dissertation). Université d'Ottawa/University of Ottawa.
*   <a id="ref-Alsentzer2019"></a>Alsentzer, E., Murphy, J. R., Boag, W., Weng, W.-H., Jin, D., Naumann, T., . . . McDermott, M. B. (2019). Publicly available clinical bert embeddings.*NAACL HLT 2019*.
*   <a id="ref-Amoretti2019"></a>Amoretti, M. C., Frixione, M., Lieto, A., & Adamo, G. (2019). Ontologies, mental disorders and prototypes. In *On the cognitive, ethical, and scientific dimensions of artificial intelligence.*Springer.
*   <a id="ref-Anand2024"></a>Anand, J., & Dhanalakshmi, R. (2024). Hygieia: Multipurpose healthcare assistance using the internet of things. In*Internet of medical things in smart healthcare*(pp. 77–96). Apple Academic Press.
*   <a id="ref-Bagaria2020"></a>Bagaria, N., Laamarti, F., Badawi, H. F., Albraikan, A., Martinez Velazquez, R. A., & El Saddik, A. (2020). Health 4.0: Digital twins for health and well-being.*Connected health in smart cities*.
*   <a id="ref-Chancellor2020"></a>Chancellor, S., & De Choudhury, M. (2020). Methods in predictive techniques for mental health status on social media: a critical review. *NPJ digital medicine*.
*   <a id="ref-Chang2011"></a>Chang, K.-h., et al. (2011). How's my Mood and Stress?: an Efficient Speech Analysis Library for Unobtrusive Monitoring on Mobile Phones. In *Body area networks conference.*
*   <a id="ref-Chang2015"></a>Chang, Y.-S., Fan, C.-T., Lo, W.-T., Hung, W.-C., & Yuan, S.-M. (2015). Mobile cloud-based depression diagnosis using an ontology and a bayesian network.*Future Generation Computer Systems*, *43*, 87–98.
*   <a id="ref-Chang2013"></a>Chang, Y.-S., et al. (2013). Depression Diagnosis Based on Ontologies and Bayesian Networks. In *Systems, man, and cybernetics (smc), 2013 ieee international conference on.*
*   <a id="ref-Chen2021"></a>Chen, J., Abbod, M., & Shieh, J.-S. (2021). Pain and stress detection using wearable sensors and devices—a review.*Sensors*.
*   <a id="ref-Chen2023"></a>Chen, Z., Lu, Y., & Wang, W. (2023). Empowering psychotherapy with large language models: Cognitive distortion detection through diagnosis of thought prompting. In *Findings of the association for computational linguistics: Emnlp 2023.*
*   <a id="ref-Dalal2024"></a>Dalal, S., Tilwani, D., Gaur, M., Jain, S., Shalin, V., & Sheth, A. (2024). A cross attention approach to diagnostic explainability using clinical practice guidelines for depression.*Authorea Preprints*.
*   <a id="ref-Dang2023"></a>Dang, L. D., Phan, U. T., & Nguyen, N. T. (2023). Gena: A knowledge graph for nutrition and mental health. *Journal of Biomedical Informatics*, *145*, 104460.
*   <a id="ref-DeChoudhury2013"></a>De Choudhury, M., Gamon, M., Counts, S., & Horvitz, E. (2013). Predicting depression via social media. In *Proceedings of the international aaai conference on web and social media.*
*   <a id="ref-DeChoudhury2016"></a>De Choudhury, M., et al. (2016). Discovering shifts to suicidal ideation from mental health content in social media. In*CHI conference on human factors in computing systems.*
*   <a id="ref-Erol2020"></a>Erol, T., Mendi, A. F., & Dogan, D. (2020). The digital twin revolution in healthcare. In *2020 4th international symposium on multidisciplinary studies and innovative technologies (ismsit).*
*   <a id="ref-ETSI2020"></a>*ETSI TS 103 410-8 V1.1.1 (2020-07) SmartM2M; Extension to SAREF; Part 8: eHealth/Ageing-well Domain.*(2020).
*   <a id="ref-Ferdousi2022"></a>Ferdousi, R., Laamarti, F., & El Saddik, A. (2022). Digital twins for well-being: an overview.*Digital Twin*.
*   <a id="ref-Fu2021"></a>Fu, C., Jiang, X., He, T., & Jiang, X. (2021). Mdepressionkg: a knowledge graph for metabolismdepression associations. In *Proceedings of the 2nd international symposium on artificial intelligence for medicine sciences*(pp. 63–68).
*   <a id="ref-GamezDiaz2020"></a>Gámez Díaz, R., Yu, Q., Ding, Y., Laamarti, F., & El Saddik, A. (2020). Digital twin coaching for physical activities: A survey.*Sensors*.
*   <a id="ref-GarciaCeja2016"></a>Garcia-Ceja, E., et al. (2016). Automatic Stress Detection in Working Environments from Smartphones' Accelerometer Data: a First Step. *Journal of Biomedical and Health Informatics*.
*   <a id="ref-GarciaCeja2018"></a>Garcia-Ceja, E., et al. (2018). Mental Health Monitoring with Multimodal Sensing and Machine Learning: A survey. *Elsevier Pervasive and Mobile Computing Journal (IF: 2.974 in 2017)*.
*   <a id="ref-Garguilo2007"></a>Garguilo, J. J., Martinez, S., et al. (2007). Moving toward semantic interoperability of medical devices. In *Workshop on high confidence medical devices, software, and systems and medical device plugand-play interoperability.*
*   <a id="ref-Gaur2019"></a>Gaur, M., Alambo, A., Sain, J. P., Kursuncu, U., Thirunarayan, K., Kavuluru, R., . . . Pathak, J. (2019). Knowledge-aware assessment of severity of suicide risk for early intervention. In*The world wide web conference.*
*   <a id="ref-Gaur2021a"></a>Gaur, M., Aribandi, V., Alambo, A., Kursuncu, U., Thirunarayan, K., Beich, J., . . . Sheth, A. (2021). Characterization of time-variant and time-invariant assessment of suicidality on reddit using c-ssrs.*PloS one*.
*   <a id="ref-Gaur2021b"></a>Gaur, M., Faldu, K., & Sheth, A. (2021). Semantics of the black-box: Can knowledge graphs help make deep learning systems more interpretable and explainable? *IEEE Internet Computing*.
*   <a id="ref-Gaur2022"></a>Gaur, M., Gunaratna, K., et al. (2022). Iseeq: Information seeking question generation using dynamic meta-information retrieval and knowledge graphs. In *Aaai conference on artificial intelligence.*
*   <a id="ref-Gaur2018"></a>Gaur, M., Kursuncu, U., Alambo, A., Sheth, A., Daniulaityte, R., Thirunarayan, K., & Pathak, J. (2018). "Let me tell you about your mental health!" Contextualized classification of reddit posts to DSM-5 for web-based intervention. In*ACM Conference on Information and Knowledge Management.*
*   <a id="ref-Gaur2024"></a>Gaur, M., & Sheth, A. (2024). Building trustworthy neurosymbolic ai systems: Consistency, reliability, explainability, and safety.*AI Magazine*.
*   <a id="ref-Gedam2021"></a>Gedam, S., & Paul, S. (2021). A review on mental stress detection using wearable sensors and machine learning techniques. *IEEE Access*.
*   <a id="ref-Gkotsis2017"></a>Gkotsis, G., Oellrich, A., Velupillai, S., Liakata, M., Hubbard, T. J., et al. (2017). Characterisation of mental health conditions in social media using informed deep learning. *Scientific reports*.
*   <a id="ref-Gruber1995"></a>Gruber, T. R. (1995). Toward principles for the design of ontologies used for knowledge sharing? *Elsevier International journal of human-computer studies*.
*   <a id="ref-Gupta2022"></a>Gupta, S., Agarwal, A., Gaur, M., Roy, K., Narayanan, V., Kumaraguru, P., & Sheth, A. (2022). Learning to automate follow-up question generation using process knowledge for depression triage on reddit posts. In *Workshop on computational linguistics and clinical psychology.*
*   <a id="ref-Gutierrez2021"></a>Gutierrez, L. J., Rabbani, K., et al. (2021). Internet of things for mental health: Open issues in data acquisition, self-organization, service level agreement, and identity management.*International Journal of Environmental Research and Public Health*.
*   <a id="ref-Gyrard2022a"></a>Gyrard, A., & Boudaoud, K. (2022). Interdisciplinary IoT and Emotion Knowledge Graph-Based Recommendation System to Boost Mental Health.
*   <a id="ref-Gyrard2022b"></a>Gyrard, A., Jaimini, U., Gaur, M., Shekarpour, S., Thirunarayan, K., & Sheth, A. (2022). Reasoning Over Personalized Healthcare Knowledge Graph: A Case Study of Patients with Allergies and Symptoms. In *Semantic Models in IoT and e-Health Applications.*Elsevier.
*   <a id="ref-Gyrard2022c"></a>Gyrard, A., & Kung, A. (2022). SAREF4EHAW-Compliant Knowledge Discovery and Reasoning for IoT-based Preventive Healthcare and Well-Being. In*Semantic Models in IoT and e-Health Applications.*Elsevier.
*   <a id="ref-Gyrard2020"></a>Gyrard, A., & Sheth, A. (2020). IAMHAPPY: Towards An IoT Knowledge-Based Cross-Domain Well-Being Recommendation System for Everyday Happiness.*IEEE/ACM Conference on Connected Health: Applications, Systems and Engineering Technologies (CHASE) Conference*.
*   <a id="ref-Gyrard2021"></a>Gyrard, A., Tabeau, K., Fiorini, L., Kung, A., et al. (2021). Knowledge Engineering Framework for IoT Robotics Applied to Smart Healthcare and Emotional Well-Being. *International Journal of Social Robotics 2021. Springer.*.
*   <a id="ref-Hadzic2008"></a>Hadzic, M., Chen, M., & Dillon, T. S. (2008). Towards the mental health ontology. In*2008 ieee international conference on bioinformatics and biomedicine*(pp. 284–288).
*   <a id="ref-Hastings2011"></a>Hastings, J., Ceusters, W., Smith, B., & Mulligan, K. (2011). The emotion ontology: enabling interdisciplinary research in the affective sciences.*Modeling and Using Context*.
*   <a id="ref-Hastings2012"></a>Hastings, J., et al. (2012). Representing Mental Functioning: Ontologies for Mental Health and Disease. In *International conference on biomedical ontology (icbo).*
*   <a id="ref-Hua2024"></a>Hua, Y., Liu, F., Yang, K., Li, Z., Sheu, Y.-h., Zhou, P., . . . Beam, A. (2024). Large language models in mental health care: a scoping review.*arXiv preprint arXiv:2401.02984*.
*   <a id="ref-Huang2017"></a>Huang, Z., Yang, J., van Harmelen, F., & Hu, Q. (2017). Constructing knowledge graphs of depression. In *Health information science: 6th international conference, his 2017, moscow, russia, october 7-9, 2017, proceedings 6*(pp. 149–161).
*   <a id="ref-Ji2021"></a>Ji, S., Zhang, T., Ansari, L., Fu, J., Tiwari, P., & Cambria, E. (2021). Mentalbert: Publicly available pretrained language models for mental healthcare.*arXiv preprint arXiv:2110.15621*.
*   <a id="ref-Joyce2023"></a>Joyce, D. W., Kormilitzin, A., Smith, K. A., & Cipriani, A. (2023). Explainable artificial intelligence for mental health through transparency and interpretability for understandability. *npj Digital Medicine*.
*   <a id="ref-Jung2017"></a>Jung, H., Park, H.-A., & Song, T.-M. (2017). Ontology-based approach to social data sentiment analysis: detection of adolescent depression signals. *Journal of Medical Internet Research (IF: 4.671 in 2017)*.
*   <a id="ref-Jung2015"></a>Jung, H., Park, H.-A., Song, T.-M., Jeon, E., Kim, A. R., & Lee, J. Y. (2015). Development of an Adolescent Depression Ontology for Analyzing Social Data. *Studies in Health Technology and Informatics*.
*   <a id="ref-KabatZinn2003"></a>Kabat-Zinn, J. (2003). Mindfulness-based stress reduction (MBSR). *Constructivism in the Human Sciences*.
*   <a id="ref-Kim2017"></a>Kim, J.-Y. e. a. (2017). Unobtrusive Monitoring to Detect Depression for Elderly with Chronic Illnesses. *IEEE Sensors Journal (IF: 3.076 in 2020)*.
*   <a id="ref-Kursuncu2018"></a>Kursuncu, U., Gaur, M., Lokala, U., Illendula, A., Thirunarayan, K., Daniulaityte, R., . . . Arpinar, I. B. (2018). What's ur type? contextualized classification of user types in marijuana-related communications using compositional multiview embedding. In *2018 ieee/wic/acm international conference on web intelligence (wi)*(pp. 474–479).
*   <a id="ref-Laamarti2020"></a>Laamarti, F., Badawi, H. F., Ding, Y., Arafsha, F., Hafidh, B., & El Saddik, A. (2020). An iso/ieee 11073 standardized digital twin framework for health and well-being in smart cities.*IEEE Access*.
*   <a id="ref-Lewis2020"></a>Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., . . . others (2020). Retrieval-augmented generation for knowledge-intensive nlp tasks. *Advances in Neural Information Processing Systems*, *33*, 9459–9474.
*   <a id="ref-Liu2019"></a>Liu, Y., Zhang, L., Yang, Y., Zhou, L., Ren, L., Wang, F., . . . Deen, M. J. (2019). A novel cloud-based framework for the elderly healthcare services using digital twin. *IEEE Access*, *7*, 49088–49101.
*   <a id="ref-Lokala2022a"></a>Lokala, U., Lamy, F., Daniulaityte, R., Gaur, M., Gyrard, A., Thirunarayan, K., . . . Sheth, A. (2022). Drug abuse ontology to harness web-based data for substance use epidemiology research: ontology development study. *JMIR public health and surveillance*.
*   <a id="ref-Lokala2022b"></a>Lokala, U., Srivastava, A., Dastidar, T. G., Chakraborty, T., Akhtar, M. S., Panahiazar, M., & Sheth, A. (2022). A computational approach to understand mental health from reddit: knowledge-aware multitask learning framework. In *Proceedings of the international aaai conference on web and social media*(Vol. 16, pp. 640–650).
*   <a id="ref-Lu2012"></a>Lu, H., et al. (2012). StressSense: Detecting Stress in Unconstrained Acoustic Environments Using Smartphones. In*Ubiquitous computing (ubicomp, a-rank conference).*
*   <a id="ref-Manas2021"></a>Manas, G., Aribandi, V., Kursuncu, U., Alambo, A., Shalin, V. L., Thirunarayan, K., . . . others (2021). Knowledge-infused abstractive summarization of clinical diagnostic interviews: Framework development study.*JMIR Mental Health*.
*   <a id="ref-Minaee2024"></a>Minaee, S., Mikolov, T., Nikzad, N., Chenaghlu, M., Socher, R., Amatriain, X., & Gao, J. (2024). Large language models: A survey. *arXiv preprint arXiv:2402.06196*.
*   <a id="ref-Mohammadi2024"></a>Mohammadi, S., Raff, E., Malekar, J., Palit, V., Ferraro, F., & Gaur, M. (2024). Welldunn: On the robustness and explainability of language models and large language models in identifying wellness dimensions. *arXiv preprint arXiv:2406.12058*.
*   <a id="ref-Mullick2022"></a>Mullick, S., Singh, A. K., Shaw, A. K., et al. (2022). Iot based smart system to detect mental health emergencies: A proposed model. *American Journal of Science & Engineering*.
*   <a id="ref-Muthalagu2023"></a>Muthalagu, R., Ramachandran, R., Anupama, P., et al. (2023). Pattern recognition and modelling in electrocardiogram signals: Early detection of myocardial ischemia and infraction. In *2023 2nd international conference on edge computing and applications (icecaa)*(pp. 1035–1041).
*   <a id="ref-Noy2009"></a>Noy, N. F., Shah, N. H., Whetzel, P. L., Dai, B., Dorf, M., Griffith, N., . . . others (2009). Bioportal: ontologies and integrated data resources at the click of a mouse.*Nucleic acids research*.
*   <a id="ref-Ponmalar2024"></a>Ponmalar, A., & Anand, J. (2024). Iomt-based caring system for aged people in a post-covid scenario. In *Internet of medical things in smart healthcare*(pp. 207–224). Apple Academic Press.
*   <a id="ref-Rawte2023"></a>Rawte, V., Sheth, A., & Das, A. (2023). A survey of hallucination in large foundation models.*arXiv preprint arXiv:2309.05922*.
*   <a id="ref-Rejeb2022"></a>Rejeb, A., Keogh, J. G., Martindale, W., Dooley, D., Smart, E., Simske, S., . . . others (2022). Charting past, present, and future research in the semantic web and interoperability. *Future internet*.
*   <a id="ref-Roy2023a"></a>Roy, K., Sheth, A., & Gaur, M. (2023). Alleviate chatbot. *UMBC Faculty Collection*.
*   <a id="ref-Roy2023b"></a>Roy, K., Zi, Y., Gaur, M., Malekar, J., Zhang, Q., Narayanan, V., & Sheth, A. (2023). Process knowledge-infused learning for clinician-friendly explanations. In *Aaai symposium series.*
*   <a id="ref-Saha2019"></a>Saha, K., Chandrasekharan, E., & De Choudhury, M. (2019). Prevalence and psychological effects of hateful speech in online college communities. In*Acm conference on web science.*
*   <a id="ref-Sarkar2023"></a>Sarkar, S., Gaur, M., Srivastava, B., et al. (2023). A review of the explainability and safety of conversational agents for mental health to identify avenues for improvement.*Frontiers in AI*.
*   <a id="ref-Seligman2008"></a>Seligman, M. E. (2008). Positive health. *Applied psychology*.
*   <a id="ref-Sheth2021a"></a>Sheth, A., Gaur, M., Roy, K., & Faldu, K. (2021). Knowledge-intensive language understanding for explainable ai. *IEEE Internet Computing*.
*   <a id="ref-Sheth2022"></a>Sheth, A., Gaur, M., Roy, K., Venkataraman, R., & Khandelwal, V. (2022). Process knowledge-infused ai: Toward user-level explainability, interpretability, and safety. *IEEE Internet Computing*.
*   <a id="ref-Sheth2019"></a>Sheth, A., Padhee, S., & Gyrard, A. (2019). Knowledge Graphs and Knowledge Networks The Story in Brief.
*   <a id="ref-Shing2018"></a>Shing, H.-C., et al. (2018). Expert, crowdsourced, and machine assessment of suicide risk via online postings. In *Computational linguistics and clinical psychology: from keyboard to clinic workshop.*
*   <a id="ref-Srividya2018"></a>Srividya, M., Mohanavalli, S., & Bhalaji, N. (2018). Behavioral modeling for mental health using machine learning algorithms.*Journal of medical systems*.
*   <a id="ref-Su2020"></a>Su, C. e. a. (2020). Deep learning in mental health outcome research: a scoping review. *Translational Psychiatry*.
*   <a id="ref-Thiruvalluru2021"></a>Thiruvalluru, R. K., Gaur, M., Thirunarayan, K., Sheth, A., et al. (2021). Comparing suicide risk insights derived from clinical and social media data. *AMIA Summits on Translational Science Proceedings*.
*   <a id="ref-Tilwani2024"></a>Tilwani, D., Saxena, Y., Mohammadi, A., Raff, E., Sheth, A., Parthasarathy, S., & Gaur, M. (2024). Reasons: A benchmark for retrieval and automated citations of scientific sentences using public and proprietary llms. *arXiv preprint arXiv:2405.02228*.
*   <a id="ref-Turab2023"></a>Turab, M. e. a. (2023). A comprehensive survey of digital twins in healthcare in the era of metaverse. *BioMedInformatics*.
*   <a id="ref-Vajre2021"></a>Vajre, V., et al. (2021). PsychBERT: a mental health language model for social media mental health behavioral analysis. In *International conference on bioinformatics and biomedicine.*
*   <a id="ref-Vandenbussche2016"></a>Vandenbussche, P.-Y., Atemezing, G. A., Poveda-Villalón, M., & Vatant, B. (2016). Linked Open Vocabularies (LOV): a Gateway to Reusable Semantic Vocabularies on the Web.*Semantic Web J*.
*   <a id="ref-vanderMaden2023"></a>van der Maden, W., Lomas, D., & Hekkert, P. (2023). Positive ai: Key challenges for designing wellbeing-aligned artificial intelligence. *arXiv preprint arXiv:2304.12241*.
*   <a id="ref-Yamada2018"></a>Yamada, D. B., Yoshiura, V. T., Miyoshi, N. S. B., de Lima, I. B., Shinoda, G. Y. U., et al. (2018). Proposal of an ontology for mental health management in brazil. *Procedia computer science*.
*   <a id="ref-Yang2023"></a>Yang, K., Zhang, T., Kuang, Z., et al. (2023). Mentalllama: Interpretable mental health analysis on social media with large language models. *arXiv preprint 2309.13567*.
*   <a id="ref-Yang2024"></a>Yang, Z., Khatibi, E., Nagesh, N., et al. (2024). ChatDiet: Empowering personalized nutrition-oriented food recommender chatbots through an LLM-augmented framework. *Smart Health*.
*   <a id="ref-Yoon2016"></a>Yoon, S., Sim, J. K., & Cho, Y.-H. (2016). A Flexible and Wearable Human Stress Monitoring Patch. *Nature Scientific Reports Journal (IF: 4.122 in 2017)*.
*   <a id="ref-Zenonos2016"></a>Zenonos, A., et al. (2016). Healthyoffice: Mood recognition at work using smartphones and wearable sensors. In *International conference on pervasive computing and communication workshops.*
*   <a id="ref-Zhang2023a"></a>Zhang, S., Dong, L., Li, X., Zhang, S., Sun, X., Wang, S., . . . others (2023). Instruction tuning for large language models: A survey.*arXiv preprint arXiv:2308.10792*.
*   <a id="ref-Zhang2022"></a>Zhang, T., Schoene, A. M., Ji, S., & Ananiadou, S. (2022). Natural language processing applied to mental illness detection: a narrative review. *NPJ digital medicine*, *5*(1), 1–13.
*   <a id="ref-Zhang2020"></a>Zhang, X., & Chen, J. (2020). Understanding information resources for college student mental health: A knowledge graph approach. *iConference 2020 Proceedings*.
*   <a id="ref-Zhang2023b"></a>Zhang, Y., Li, Y., Cui, L., Cai, D., et al. (2023). Siren's song in the ai ocean: a survey on hallucination in large language models. *arXiv preprint arXiv:2309.01219*.
*   <a id="ref-Zhou2015"></a>Zhou, D., Luo, J., Silenzio, V. M., Zhou, Y., Hu, J., Currier, G., & Kautz, H. (2015). Tackling Mental Health by Integrating Unobtrusive Multimodal Sensing. In *Conference on artificial intelligence.*

## TL;DR

Proposes IoT-based preventive mental health framework using knowledge graphs and standards for semantic data integration and personalized well-being monitoring.

## Key Insights

Presents Mental Health Knowledge Graph (ontology and dataset) integrated with IoT Digital Twins using domain-specific standards and semantic web technologies for preventive mental health care with heterogeneous data integration capabilities

## Metadata Summary

### Research Context

*   **Research Question**: How can IoT-based digital twin technologies and knowledge graphs be integrated with semantic web standards to enable preventive mental health care through heterogeneous data fusion and real-time personalized monitoring?
*   **Methodology**: Systematic literature review; Standards analysis; Ontology engineering; Knowledge graph construction; Multi-source data integration methodology; Semantic mapping between ontologies and standards; Framework design for IoT-healthcare integration
*   **Key Findings**: Mental Health Knowledge Graph successfully integrates multiple ontology-based projects; LOV4IoT catalog provides comprehensive mental health ontology classification; Semantic mappings established between health standards and knowledge bases; Framework demonstrates successful integration of IoT data with clinical knowledge; Digital twin approach enables real-time monitoring and personalized interventions; Standards analysis reveals comprehensive coverage across multiple organizations

### Analysis

*   **Limitations**: Limited empirical validation of integrated framework in real-world healthcare settings; Complexity of maintaining semantic mappings across evolving standards; Privacy and ethical considerations for personal health data integration not fully addressed; Scalability challenges for large-scale deployment across diverse healthcare environments
*   **Future Work**: Conduct clinical trials to validate framework effectiveness in real healthcare environments; Develop privacy-preserving semantic integration techniques for sensitive mental health data; Create user-centered design methodologies for diverse patient populations; Establish regulatory compliance frameworks for IoT-healthcare integration; Implement comprehensive evaluation of prevention outcomes and cost-effectiveness; Develop automated ontology evolution and maintenance systems