---
cite_key: valle_2023
title: Digital twin for healthcare systems
authors: Alexandre Vallée
year: 2023
doi: 10.3389/fdgth.2023.1253050
date_processed: '2025-07-02'
phase2_processed: true
original_folder: frontiers_dt_healthcare_systems
images_total: 0
images_kept: 0
images_removed: 0
tags:
- Biomedical
- Data Integration
- Digital Health
- Electronic Health Records
- Healthcare
- IoT
- Machine Learning
- Personal Health
keywords:
- MacFeely
- PubMed
- accuracy
- alexandre vallée
- artificial intelligence
- author contributions
- biller-andorno
- closed-loop
- cloud-based
- cloud-based framework
- community-based
- community-based interventions
- conflict of interest
- context-aware
- convergence
- copyright
- corral-acero
- data privacy
- data-driven
- decision-making
- diagnosis
- digital health
- digital twin
- efficiency
- entity
- evidence-based
- evidence-based medicine
- evidence-based practices
- genomics
- iot
---

EDITED BY Camelia Quek, The University of Sydney, Australia

REVIEWED BY Pantelis Natsiavas, Centre for Research and Technology Hellas (INAB|CERTH), Greece Yu Leng Phua, Mount Sinai Genomics, Inc., United States

\*CORRESPONDENCE Alexandre Vallée al.vallee@hopital-foch.com

RECEIVED 04 July 2023 ACCEPTED 28 August 2023 PUBLISHED 07 September 2023

CITATION Vallée A (2023) Digital twin for healthcare systems. Front. Digit. Health 5:1253050. doi: [10.3389/fdgth.2023.1253050](https://doi.org/10.3389/fdgth.2023.1253050)

# COPYRIGHT

© 2023 Vallée. This is an open-access article distributed under the terms of the [Creative](http://creativecommons.org/licenses/by/4.0/) [Commons Attribution License \(CC BY\).](http://creativecommons.org/licenses/by/4.0/) The use, distribution or reproduction in other forums is permitted, provided the original author(s) and the copyright owner(s) are credited and that the original publication in this journal is cited, in accordance with accepted academic practice. No use, distribution or reproduction is permitted which does not comply with these terms.

## [Digital twin for healthcare systems](https://www.frontiersin.org/articles/10.3389/fdgth.2023.1253050/full)

## Alexandre Vallée\*

Department of Epidemiology and Public Health, Foch Hospital, Suresnes, France

Digital twin technology is revolutionizing healthcare systems by leveraging real-time data integration, advanced analytics, and virtual simulations to enhance patient care, enable predictive analytics, optimize clinical operations, and facilitate training and simulation. With the ability to gather and analyze a wealth of patient data from various sources, digital twins can offer personalized treatment plans based on individual characteristics, medical history, and real-time physiological data. Predictive analytics and preventive interventions are made possible by machine learning algorithms, allowing for early detection of health risks and proactive interventions. Digital twins can optimize clinical operations by analyzing workflows and resource allocation, leading to streamlined processes and improved patient care. Moreover, digital twins can provide a safe and realistic environment for healthcare professionals to enhance their skills and practice complex procedures. The implementation of digital twin technology in healthcare has the potential to significantly improve patient outcomes, enhance patient safety, and drive innovation in the healthcare industry.

### KEYWORDS

healthcare, patient, digital health, digital twin, patient safety, innovation, prediction

### Introduction

Digital twin technology is emerging as a transformative force in healthcare systems, revolutionizing the way patient care is delivered. By leveraging real-time data integration, advanced analytics, and virtual simulations, digital twins offer enhanced patient care, predictive analytics, optimization of clinical operations, and training and simulation opportunities [\(1\)](#page-4-0).

In terms of enhanced patient care, digital twins enable healthcare providers to gather and analyze a wealth of patient data from various sources, including electronic health records (EHRs), wearables, and medical devices ([2](#page-4-0)). This holistic view of the patient allows for personalized treatment plans, considering individual characteristics, medical history, and real-time physiological data. With digital twins, healthcare professionals can make accurate diagnoses, monitor patients in real-time, and empower patients to actively participate in their own care [\(3](#page-4-0), [4\)](#page-4-0).

Predictive analytics and preventive interventions are facilitated through digital twin technology by analyzing patient data and employing machine learning algorithms. Digital twins can predict disease progression, identify high-risk individuals, and recommend preventive measures. This proactive approach improves patient safety, long-term outcomes, and resource allocation within healthcare systems [\(5](#page-4-0)). Thus, digital twin technology may have the potential to transform healthcare systems by leveraging real-time data integration, advanced analytics, and virtual simulations. It can enhance patient care, enables predictive analytics, optimizes clinical operations, and supports training and simulation. This review focused on the potential of digital twins in healthcare systems to improve patient outcomes, operational efficiency, and overall healthcare excellence.

### Search strategy

PubMed Medline Web of Science, Google Scholar, Scopus databases were used for the research, with only articles in English language, using the following terms: "Digital twin", "Digital health" and "Healthcare". Articles included in this review were both, original research, reviews, viewpoints, and opinions articles. Literature was searched from inception to 2023.

### Digital twin

In recent times, the notion of digital twin has garnered escalating attention from both researchers and engineers. As research in the field of digital twin advances, conducted by both industry and academia, the distinctions between digital twin and other related concepts have begun to fade. Initially, the scope of digital twin encompassed physical and virtual products along with their interconnections [\(6\)](#page-4-0). This concept has evolved due to the rapid advancements in communication technology, sensor technology, big data analysis, the Internet of Things (IoT), and simulation technology ([7](#page-4-0)). This growth has fueled substantial research into digital twins.

Subsequently, digital twin was redefined as a digital replication of living or non-living physical entities, ushering in applications in areas like health and well-being ([8](#page-4-0)). Functioning as a dynamic concept, digital twin embodies a virtual replica of human organs, tissues, cells, or micro-environments that continually adapts to real-time data variations and predicts corresponding future scenarios [\(9](#page-4-0)). However, digital twin transcends being a mere digital model linked to its real-life counterpart through emerging technologies. It emerges as a sentient, intelligent, and evolving model, capable of optimizing processes and continuously forecasting future states, such as defects, damages, and failures, through a closed-loop interaction between the digital twin and its surrounding environment.

Broadly, the technologies essential for digital twin can be categorized into two groups: one involves a data-driven statistical model, while the other integrates multi-scale knowledge and data into a mechanical model ([10,](#page-4-0) [11\)](#page-4-0). The numerical model computes structural performance, while the analytical model facilitates structural analysis. An artificial intelligence (AI) model, trained with samples and numerical data, derives real-time structural insights from sensor data.

The impact of digital twin is profoundly reshaping industries and has been embraced by major corporations to heighten efficiency and identify issues. This transformative technology is also finding its way into the healthcare sector. Within this context, digital twin can treat patients as virtualized standalone assets applicable to diverse healthcare scenarios ([12](#page-4-0)). This potential holds substantial promise for improving treatment and diagnostics within hospitals and for individual patients.

Within the realm of healthcare, a digital twin embodies a virtual replica of a tangible entity or process, such as a patient, their anatomical structure, or the setting of a hospital. At present, digital twins in healthcare are designed to dynamically mirror various data sources, including EHRs, disease registries, "-omics" data (such as genomics, biomics, proteomics, or metabolomics data), as well as physical indicators, demographic information, and lifestyle data pertaining to an individual's progression over time ([6,](#page-4-0) [13](#page-4-0)). The evolution of foundational technologies like the IoT and AI, coupled with the availability of a growing array of accurate and accessible data types (ranging from biometric and behavioral data to emotional, cognitive, and psychological insights), has sparked heightened interest and exploration in the research and potential applications of digital twins within the healthcare domain ([13](#page-4-0)).

### Enhanced patient care through digital twin technology

Digital twin technology has the potential to significantly enhance patient care by leveraging real-time data integration, advanced analytics, and personalized insights [\(1\)](#page-4-0). These tools can enable healthcare providers to gather and analyze a wealth of patient data from various sources, such as electronic health records (EHRs), medical devices, wearables, and genetic information [\(2](#page-4-0), [14](#page-4-0)). By integrating and analyzing this data, digital twins create a holistic view of the patient, allowing healthcare professionals to develop personalized treatment plans ([6](#page-4-0), [9,](#page-4-0) [15](#page-4-0)). This approach considers individual patient characteristics, medical history, genetic factors, and real-time physiological data to tailor interventions and medications specifically to the patient's needs, resulting in improved treatment outcomes and patient satisfaction ([16](#page-4-0)–[18](#page-5-0)).

Healthcare professionals could receive support from digital twins in achieving precise and timely diagnoses [\(19\)](#page-5-0). By analyzing patient data and symptoms, digital twins can simulate various diagnostic scenarios, assisting in differential diagnoses and identifying patterns that may be missed through traditional diagnostic methods alone [\(14,](#page-4-0) [20](#page-5-0)). This improves diagnostic accuracy, reduces errors, and enables earlier intervention, leading to more effective and targeted treatments.

The integration of digital twins with real-time data from wearable devices, remote monitoring systems, and IoT devices enables the ongoing monitoring of patients [\(21\)](#page-5-0). By monitoring vital signs, physiological parameters, and other health-related data in real-time, digital twins can detect early signs of deterioration or anomalies. This enables healthcare providers to intervene proactively, prevent complications, and optimize treatment plans. Real-time monitoring through digital twins is particularly beneficial for patients with chronic conditions, enabling remote patient management and reducing the need for frequent hospital visits ([15](#page-4-0), [22,](#page-5-0) [23](#page-5-0)).

Digital twins empower patients to actively participate in their own care [\(24\)](#page-5-0). By providing patients with access to their digital twin data, including personalized health insights, treatment plans, and progress tracking, patients can become more engaged in managing their health [\(25\)](#page-5-0). This increased engagement leads to better adherence to treatment regimens, lifestyle modifications, and self-management practices. Moreover, digital twins can facilitate communication and collaboration between patients and healthcare providers, promoting shared decision-making and patient-centered care ([26](#page-5-0)).

These tools can leverage predictive analytics and machine learning algorithms to forecast disease progression and treatment outcomes ([27](#page-5-0)). By analyzing patient data and historical trends, digital twins can identify high-risk individuals, predict potential complications, and recommend preventive measures. This proactive approach to care allows healthcare providers to intervene early, prevent adverse events, and optimize treatment plans based on predicted patient responses, ultimately improving patient safety and long-term outcomes ([28](#page-5-0)).

Through secure sharing of patient data across diverse healthcare providers and settings, digital twins can streamline the continuity of care seamlessly [\(23\)](#page-5-0). This ensures that all involved healthcare professionals have access to the most up-to-date and comprehensive patient information, enabling coordinated care, minimizing duplication of tests, and reducing medical errors. Digital twins could promote efficient and effective communication and collaboration between healthcare teams, enhancing the overall patient care experience ([26](#page-5-0), [29\)](#page-5-0).

### Predictive analytics and preventive interventions through digital twin technology

Digital twin technology, with its ability to integrate real-time data and advanced analytics, holds great potential for predictive analytics and preventive interventions in healthcare. By leveraging patient data, machine learning algorithms, and predictive modeling, digital twins can identify potential health risks, predict disease progression, and enable proactive interventions ([6](#page-4-0)).

Integrating and analyzing an extensive range of patient data, including medical history, lifestyle factors, genetic information, and real-time physiological data, fosters a comprehensive view of individual health ([22](#page-5-0)). By applying advanced analytics and machine learning algorithms, digital twins can identify patterns, correlations, and anomalies within the data. This could allow healthcare professionals to detect early signs of health risks, such as the development of chronic conditions, adverse reactions to medications, or potential complications. Early detection enables timely interventions and preventive measures to mitigate or manage these risks effectively [\(30\)](#page-5-0).

Digital twins can simulate disease progression based on patient data and historical trends [\(9\)](#page-4-0). By analyzing patterns, treatment outcomes, and patient characteristics, digital twins can generate predictive models to forecast disease progression. This information enables healthcare providers to anticipate potential complications, adjust treatment plans, and optimize interventions to slow down or prevent disease progression. Digital twins allow for personalized disease modeling, considering individual patient factors, genetics, lifestyle, and response patterns, leading to more accurate predictions and tailored interventions [\(31](#page-5-0)).

Risk stratification can be supported by digital twins, as they categorize patients into varying risk groups according to their health data and predictive models [\(32](#page-5-0)). By identifying high-risk individuals, healthcare providers can allocate resources more efficiently, focus on preventive interventions, and implement targeted strategies. Digital twins provide insights into which patients are most likely to benefit from preventive measures, early screenings, lifestyle modifications, or specific interventions. This targeted approach improves the allocation of healthcare resources, reduces costs, and enhances patient outcomes [\(33](#page-5-0)).

Digital twins can enable proactive interventions and preventive care by alerting healthcare providers to potential health risks in real-time ([34](#page-5-0)). Through continuous monitoring of patient data, digital twins can detect deviations from normal health parameters, identify early warning signs, and trigger timely interventions. This proactive approach allows healthcare providers to intervene before a condition worsens, preventing hospital admissions, reducing healthcare costs, and improving patient outcomes. Preventive care through digital twins includes personalized health recommendations, reminders for screenings, medication adherence support, and lifestyle modifications [\(32](#page-5-0)).

Population health management can be enhanced by digital twins, which analyze collective data from large populations. Employing predictive analytics on this data enables healthcare systems to recognize health trends, risk factors, and disease prevalence patterns at the population level. Digital twins enable healthcare providers to design targeted interventions and preventive strategies at a population level, such as public health campaigns, vaccination programs, or community-based interventions. This population health approach aims to prevent the onset of diseases, improve health outcomes, and reduce the overall burden on the healthcare system [\(35,](#page-5-0) [36\)](#page-5-0).

### Optimization of clinical operations through digital twin technology

Digital twin technology offers significant potential for optimizing clinical operations within healthcare systems. By creating virtual replicas of physical systems and integrating realtime data, digital twins enable healthcare providers to analyze and streamline workflows, enhance resource allocation, and improve operational efficiency ([19](#page-5-0)).

Offering a holistic perspective of the clinical workflow, digital twins enable healthcare providers to assess and enhance processes. Through the integration of data from diverse sources like electronic health records (EHRs), medical devices, and administrative systems, digital twins pinpoint bottlenecks, inefficiencies, and areas with potential for improvement ([2](#page-4-0), [15\)](#page-4-0). This analysis enables healthcare professionals to streamline workflows, reduce redundant tasks, and enhance the overall efficiency of clinical operations.

Contributing to resource allocation optimization within healthcare systems, digital twins offer insights into patient volumes, demand patterns, and resource utilization by analyzing patient data, historical trends, and real-time information [\(37\)](#page-5-0). This enables healthcare providers to allocate staff, equipment, and facilities effectively, ensuring optimal utilization and minimizing wait times. Digital twins also facilitate capacity planning, allowing healthcare organizations to anticipate future demands and make informed decisions regarding resource investments and expansions.

By predictive analytics and machine learning algorithms, digital twins could aid in operational decision-making. They analyze data from various sources, encompassing patient flow, staffing levels, and equipment usage, enabling them to anticipate future operational scenarios ([5](#page-4-0)). This enables healthcare providers to make proactive decisions, such as adjusting staffing schedules, optimizing bed allocation, or rescheduling procedures, to optimize resource utilization and improve patient care [\(5\)](#page-4-0).

Integrating seamlessly with real-time data from IoT devices, wearables, and medical sensors, digital twins enable continuous monitoring of clinical operations. Through the monitoring of key performance indicators, patient flow, and operational metrics, digital twins can swiftly identify deviations from anticipated norms and initiate alerts [\(38](#page-5-0), [39\)](#page-5-0). This allows healthcare providers to address issues promptly, such as equipment malfunctions, staffing shortages, or patient bottlenecks, minimizing disruptions and ensuring smooth operations.

Digital twins can support quality improvement initiatives and enhance patient safety within clinical operations ([40](#page-5-0)). By analyzing data on adverse events, near misses, and process variations, digital twins help identify areas where improvements can be made. Healthcare providers can implement evidencebased practices, standardize workflows, and monitor adherence to protocols through digital twins. This fosters a culture of continuous improvement, reduces errors, and enhances patient safety across clinical operations.

Enabling collaboration and communication among various departments and healthcare professionals, digital twins establish a shared virtual platform. This platform permits real-time data sharing, facilitates collaboration on patient care plans, and streamlines communication processes [\(37,](#page-5-0) [41\)](#page-5-0). By providing a shared virtual platform, digital twins enable real-time data sharing, collaboration on patient care plans, and streamlined communication. This improves care coordination, reduces delays, and enhances interdisciplinary teamwork, ultimately leading to more efficient clinical operations and improved patient outcomes.

Digital twins can support continuous monitoring and iterative improvement of clinical operations ([2\)](#page-4-0). By continuously collecting and analyzing data, digital twins provide insights into operational performance over time. Healthcare providers can identify trends, assess the impact of process changes, and iteratively refine operations based on real-time feedback. This iterative improvement process enables healthcare organizations to adapt to evolving needs, address inefficiencies, and continuously optimize clinical operations.

### Training and simulation through digital twin technology

Digital twin technology can offer valuable opportunities for training and simulation in the healthcare sector [\(28\)](#page-5-0). By creating virtual replicas of physical systems, integrated with real-time data and advanced simulations, digital twins provide a safe and realistic environment for healthcare professionals to enhance their skills, practice complex procedures, and improve decisionmaking. This section explores how digital twins contribute to training and simulation in healthcare ([42](#page-5-0)).

Healthcare professionals, notably surgeons, can use digital twins to rehearse and enhance their surgical skills in a simulated environment ([43](#page-5-0)). By replicating surgical procedures and simulating different scenarios, digital twins allow surgeons to gain hands-on experience, test different techniques, and improve their proficiency without risk to real patients. This immersive training enhances surgical skills, hand-eye coordination, and decision-making abilities, ultimately leading to improved patient outcomes and safety.

A platform for healthcare professionals to simulate various medical procedures can be provided by digital twins [\(6\)](#page-4-0). From invasive interventions to non-invasive techniques, digital twins can replicate procedures and allow healthcare professionals to practice and refine their techniques. This includes simulations of catheter insertions, intubations, ultrasound-guided procedures, and more. By providing a realistic virtual environment, digital twins help healthcare professionals gain confidence, enhance their procedural skills, and ensure patient safety during actual procedures.

Thus, these tools could be particularly valuable for training healthcare professionals in emergency response situations ([44\)](#page-5-0). By simulating critical scenarios, such as cardiac arrests, trauma situations, or mass casualty incidents, digital twins allow healthcare providers to practice their response skills, teamwork, and decision-making under high-stress conditions. This training prepares them to handle emergencies effectively, improve coordination, and optimize patient outcomes in real-life emergency situations.

The simulation of intricate clinical cases, providing healthcare professionals with the opportunity to refine and augment their clinical decision-making abilities can be supported by digital twins ([45](#page-5-0)). By incorporating patient data, medical history, and real-time monitoring information, digital twins present healthcare professionals with realistic cases to analyze, diagnose, and develop treatment plans. This interactive simulation provides a valuable learning experience, enabling healthcare professionals to refine their diagnostic reasoning, consider different treatment options, and make informed decisions in a risk-free environment.

By furnishing a shared virtual platform, digital twins facilitate interprofessional collaboration and communication among healthcare professionals from diverse disciplines, enabling them to collaborate effectively ([46](#page-5-0)). Through digital twins, healthcare professionals can practice interdisciplinary teamwork, communicate effectively, and coordinate patient care. This enhances the understanding of each professional's role, fosters collaboration, and improves patient outcomes by ensuring comprehensive and coordinated care.

A platform for continuous professional development for healthcare professionals can be offered by digital twins' use. By providing access to virtual training modules, case studies, and <span id="page-4-0"></span>Vallée [10.3389/fdgth.2023.1253050](https://doi.org/10.3389/fdgth.2023.1253050)

simulation scenarios, digital twins enable healthcare professionals to stay updated with the latest advancements, learn new techniques, and acquire specialized skills. This self-paced learning and continuous training enhance professional development, promote lifelong learning, and ensure healthcare professionals are well-prepared to deliver high-quality care.

Digital twins can also serve as a valuable tool for research and innovation in healthcare [\(47\)](#page-5-0). Researchers can use digital twins to conduct experiments, analyze data, and test hypotheses. Thus, these tools enable researchers to simulate different patient populations, treatment interventions, and disease scenarios, providing insights that can drive evidence-based practices and innovation in healthcare.

### Conclusion

In conclusion, digital twin technology holds immense promise for revolutionizing healthcare systems and enhancing patient care. By integrating real-time data, advanced analytics, and virtual simulations, digital twins offer personalized treatment plans, predictive analytics, optimized clinical operations, and immersive training opportunities. The use of digital twins empowers healthcare professionals to make accurate diagnoses, monitor patients in real-time, and intervene proactively to prevent adverse events. It also enables patients to actively participate in their own care and promotes collaborative decision-making between patients and healthcare providers. Moreover, digital twins optimize resource allocation, streamline workflows, and improve operational efficiency within healthcare systems. The potential of digital twin technology in healthcare is vast, and its implementation has the potential to significantly improve patient outcomes, enhance patient safety, and drive innovation in the

### References

1. Attaran M, Celik BG. Digital twin: benefits, use cases, challenges, and opportunities. Decis Anal J. (2023) 6:100165. [doi: 10.1016/j.dajour.2023.100165](https://doi.org/10.1016/j.dajour.2023.100165)

2. Armeni P, Polat I, De Rossi LM, Diaferia L, Meregalli S, Gatti A. Digital twins in healthcare: is it the beginning of a new era of evidence-based medicine? A critical review. J Pers Med. (2022) 12:1255. [doi: 10.3390/jpm12081255](https://doi.org/10.3390/jpm12081255)

3. Cornetta K, Brown CG. Perspective: balancing personalized medicine and personalized care. Acad Med J Assoc Am Med Coll. (2013) 88:309–13. [doi: 10.1097/](https://doi.org/10.1097/ACM.0b013e3182806345) [ACM.0b013e3182806345](https://doi.org/10.1097/ACM.0b013e3182806345)

4. Jasemi M, Valizadeh L, Zamanzadeh V, Keogh B. A concept analysis of holistic care by hybrid model. Indian J Palliat Care. (2017) 23:71–80. [doi: 10.4103/0973-](https://doi.org/10.4103/0973-1075.197960) [1075.197960](https://doi.org/10.4103/0973-1075.197960)

5. van Dinter R, Tekinerdogan B, Catal C. Predictive maintenance using digital twins: a systematic literature review. Inf Softw Technol. (2022) 151:107008. [doi: 10.](https://doi.org/10.1016/j.infsof.2022.107008) [1016/j.infsof.2022.107008](https://doi.org/10.1016/j.infsof.2022.107008)

6. Sun T, He X, Li Z. Digital twin in healthcare: recent updates and challenges. Digit Health. (2023) 9:20552076221149652. [doi: 10.1177/20552076221149651](https://doi.org/10.1177/20552076221149651)

7. Li L, Lei B, Mao C. Digital twin in smart manufacturing. J Ind Inf Integr. (2022) 26:100289. [doi: 10.1016/j.jii.2021.100289](https://doi.org/10.1016/j.jii.2021.100289)

8. El Saddik A. Digital twins: the convergence of multimedia technologies. IEEE Multimed. (2018) 25:87–92. [doi: 10.1109/MMUL.2018.023121167](https://doi.org/10.1109/MMUL.2018.023121167)

9. Sun T, He X, Song X, Shu L, Li Z. The digital twin in medicine: a key to the future of healthcare? Front Med. (2022) 9:907066. [doi: 10.3389/fmed.2022.907066](https://doi.org/10.3389/fmed.2022.907066)

healthcare industry. However, its successful implementation requires addressing challenges related to data privacy, interoperability, data quality, ethics, resource intensity, integration with workflows, validation, education, scalability, and cultural shifts. As these challenges are navigated, digital twin technology could revolutionize healthcare systems, leading to improved patient outcomes, more efficient operations, and a higher quality of care.

### Author contributions

Conceptualization, formal analysis, writing – original draft preparation: AV. The author has read and agreed to the published version of the manuscript.

## Conflict of interest

The author declares that the research was conducted in the absence of any commercial or financial relationships that could be construed as a potential conflict of interest.

### Publisher's note

All claims expressed in this article are solely those of the authors and do not necessarily represent those of their affiliated organizations, or those of the publisher, the editors and the reviewers. Any product that may be evaluated in this article, or claim that may be made by its manufacturer, is not guaranteed or endorsed by the publisher.

10. Corral-Acero J, Margara F, Marciniak M, Rodero C, Loncaric F, Feng Y, et al. The "digital twin" to enable the vision of precision cardiology. Eur Heart J. (2020) 41:4556–64. [doi: 10.1093/eurheartj/ehaa159](https://doi.org/10.1093/eurheartj/ehaa159)

11. Peirlinck M, Costabal FS, Yao J, Guccione JM, Tripathy S, Wang Y, et al. Precision medicine in human heart modeling : perspectives, challenges, and opportunities. Biomech Model Mechanobiol. (2021) 20:803–31. [doi: 10.1007/s10237-021-01421-z](https://doi.org/10.1007/s10237-021-01421-z)

12. Tao F, Qi Q. Make more digital twins. Nature. (2019) 573:490–1. [doi: 10.1038/](https://doi.org/10.1038/d41586-019-02849-1) [d41586-019-02849-1](https://doi.org/10.1038/d41586-019-02849-1)

13. Schwartz SM, Wildenhaus K, Bucher A, Byrd B. Digital twins and the emerging science of self: implications for digital health experience design and "small" data. Front Comput Sci. (2020) 2,<https://www.frontiersin.org/articles/10.3389/fcomp.2020.00031> (accessed 31 May2023). [doi: 10.3389/fcomp.2020.00031](https://doi.org/10.3389/fcomp.2020.00031)

14. Voigt I, Inojosa H, Dillenseger A, Haase R, Akgün K, Ziemssen T. Digital twins for multiple sclerosis. Front Immunol. (2021) 12:669811. [doi: 10.3389/](https://doi.org/10.3389/fimmu.2021.669811)fimmu.2021. [669811](https://doi.org/10.3389/fimmu.2021.669811)

15. Haleem A, Javaid M, Pratap Singh R, Suman R. Exploring the revolution in healthcare systems through the applications of digital twin technology. Biomed Technol. (2023) 4:28–38. [doi: 10.1016/j.bmt.2023.02.001](https://doi.org/10.1016/j.bmt.2023.02.001)

16. Johnson KB, Wei W, Weeraratne D, Frisse ME, Misulis K, Rhee K, et al. Precision medicine, AI, and the future of personalized health care. Clin Transl Sci. (2021) 14:86–93. [doi: 10.1111/cts.12884](https://doi.org/10.1111/cts.12884)

17. Goetz LH, Schork NJ. Personalized medicine: motivation, challenges and progress. Fertil Steril. (2018) 109:952–63. [doi: 10.1016/j.fertnstert.2018.05.006](https://doi.org/10.1016/j.fertnstert.2018.05.006)

<span id="page-5-0"></span>18. Subbiah V. The next generation of evidence-based medicine. Nat Med. (2023) 29:49–58. [doi: 10.1038/s41591-022-02160-z](https://doi.org/10.1038/s41591-022-02160-z)

19. Venkatesh KP, Raza MM, Kvedar JC. Health digital twins as tools for precision medicine: considerations for computation, implementation, and regulation. Npj Digit Med. (2022) 5:1–2.

20. Zhong D, Xia Z, Zhu Y, Duan J. Overview of predictive maintenance based on digital twin technology. Heliyon. (2023) 9:e14534. [doi: 10.1016/j.heliyon.2023.e14534](https://doi.org/10.1016/j.heliyon.2023.e14534)

21. Volkov I, Radchenko G, Tchernykh A. Digital twins, internet of things and Mobile medicine: a review of current platforms to support smart healthcare. Program Comput Softw. (2021) 47:578–90.

22. Kamel Boulos MN, Zhang P. Digital twins: from personalised medicine to precision public health. J Pers Med. (2021) 11:745. [doi: 10.3390/jpm11080745](https://doi.org/10.3390/jpm11080745)

23. Elkefi S, Asan O. Digital twins for managing health care systems: rapid literature review. J Med Internet Res. (2022) 24:e37641. [doi: 10.2196/37641](https://doi.org/10.2196/37641)

24. Syed-Abdul S, Li Y-C. Empowering patients and transforming healthcare in the post-COVID-19 era: the role of digital and wearable technologies. J Pers Med. (2023) 13:722. [doi: 10.3390/jpm13050722](https://doi.org/10.3390/jpm13050722)

25. Abernethy A, Adams L, Barrett M, Bechtel C, Brennan P, Butte A, et al. The promise of digital health: then, now, and the future.. NAM Perspect. (2022) 2022. [doi: 10.31478/202206e](https://doi.org/10.31478/202206e)

26. Hassani H, Huang X, MacFeely S. Impactful digital twin in the healthcare revolution. Big Data Cogn Comput. (2022) 6:83. [doi: 10.3390/bdcc6030083](https://doi.org/10.3390/bdcc6030083)

27. Allen A, Siefkas A, Pellegrini E, Burdick H, Barnes G, Calvert J, et al. A digital twins machine learning model for forecasting disease progression in stroke patients. Appl Sci. (2021) 11:5576. [doi: 10.3390/app11125576](https://doi.org/10.3390/app11125576)

28. Erol T, Mendi AF, Doğan D. The digital twin revolution in healthcare. 2020 4th international symposium on multidisciplinary studies and innovative technologies (ISMSIT) (2020). p. 1–7.

29. Pang TY, Pelaez Restrepo JD, Cheng C-T, Yasin A, Lim H, Miletic M. Developing a digital twin and digital thread framework for an 'industry 4.0' shipyard. Appl Sci. (2021) 11:1097. [doi: 10.3390/app11031097](https://doi.org/10.3390/app11031097)

30. Ginsburg O, Yip C-H, Brooks A, Cabanes A, Caleffi M, Dunstan YJ, et al. Breast cancer early detection: a phased approach to implementation. Cancer. (2020) 126:2379–93. [doi: 10.1002/cncr.32887](https://doi.org/10.1002/cncr.32887)

31. Pascual H, Masip-Bruin X, Alonso A, Cerdá J. A Systematic Review on Human Modeling: Digging into Human Digital Twin Implementations.

32. Coorey G, Figtree GA, Fletcher DF, Snelson VJ, Vernon ST, Winlaw D, et al. The health digital twin to tackle cardiovascular disease—a review of an emerging interdisciplinary field. Npj Digit Med. (2022) 5:1–12. [doi: 10.1038/s41746-022-00640-7](https://doi.org/10.1038/s41746-022-00640-7)

33. Morande S. Enhancing psychosomatic health using artificial intelligence-based treatment protocol: a data science-driven approach. Int J Inf Manag Data Insights. (2022) 2:100124. [doi: 10.1038/s41746-022-00640-7](https://doi.org/10.1038/s41746-022-00640-7)

34. Sahal R, Alsamhi SH, Brown KN. Personal digital twin: a close Look into the present and a step towards the future of personalised healthcare industry. Sensors. (2022) 22:5918. [doi: 10.3390/s22155918](https://doi.org/10.3390/s22155918)

35. Popa EO, van Hilten M, Oosterkamp E, Bogaardt M-J. The use of digital twins in healthcare: socio-ethical benefits and socio-ethical risks. Life Sci Soc Policy. (2021) 17:6. [doi: 10.1186/s40504-021-00113-x](https://doi.org/10.1186/s40504-021-00113-x)

36. Calcaterra V, Pagani V, Zuccotti G. Digital twin: a future health challenge in prevention, early diagnosis and personalisation of medical care in paediatrics. Int J Environ Res Public Health. (2023) 20:2181. [doi: 10.3390/ijerph20032181](https://doi.org/10.3390/ijerph20032181)

37. Elayan H, Aloqaily M, Guizani M. Digital twin for intelligent context-aware IoT healthcare systems. IEEE Internet Things J. (2021) 8:16749–57. [doi: 10.1109/JIOT.](https://doi.org/10.1109/JIOT.2021.3051158) [2021.3051158](https://doi.org/10.1109/JIOT.2021.3051158)

38. Kaur MJ, Mishra VP, Maheshwari P. The convergence of digital twin, IoT, and machine learning: transforming data into action. In: Farsi M, Daneshkhah A, Hosseinian-Far A, Jahankhani H, editors. Digital twin technologies and smart cities. Cham: Springer International Publishing (2020). p. 3–17.

39. Canedo A. Industrial IoT lifecycle via digital twins. Proceedings of the eleventh IEEE/ACM/IFIP international conference on hardware/software codesign and system synthesis. New York, NY, USA: Association for Computing Machinery (2016). p. 1.

40. Bruynseels K, Santoni de Sio F, van den Hoven J. Digital twins in health care: ethical implications of an emerging engineering paradigm. Front Genet. (2018) 9:31. [doi: 10.3389/fgene.2018.00031](https://doi.org/10.3389/fgene.2018.00031)

41. Liu Y, Zhang L, Yang Y, Zhou L, Ren L, Wang F, et al. A novel cloud-based framework for the elderly healthcare services using digital twin. IEEE Access. (2019) 7:49088–101. [doi: 10.1109/ACCESS.2019.2909828](https://doi.org/10.1109/ACCESS.2019.2909828)

42. Alazab M, Khan LU, Koppu S, Ramu SP, Iyapparaja M, Boobalan P, et al. Digital twins for healthcare 4.0—recent advances. Architecture, and open challenges. IEEE Consum Electron Mag. (2022):1–8.

43. Moztarzadeh O, Jamshidi M, Sargolzaei S, Jamshidi A, Baghalipour N, Malekzadeh Moghani M, et al. Metaverse and healthcare: machine learning-enabled digital twins of cancer. Bioengineering. (2023) 10:455. [doi: 10.3390/bioengineering10040455](https://doi.org/10.3390/bioengineering10040455)

44. Fan C, Zhang C, Yahja A, Mostafavi A. Disaster city digital twin: a vision for integrating artificial and human intelligence for disaster management. Int J Inf Manag. (2021) 56:102049. [doi: 10.1016/j.ijinfomgt.2019.102049](https://doi.org/10.1016/j.ijinfomgt.2019.102049)

45. Kaul R, Ossai C, Forkan ARM, Jayaraman PP, Zelcer J, Vaughan S, et al. The role of AI for developing digital twins in healthcare: the case of cancer care. WIRES Data Min Knowl Discov. (2023) 13:e1480. [doi: 10.1002/widm.1480](https://doi.org/10.1002/widm.1480)

46. Iqbal JD, Krauthammer M, Biller-Andorno N. The use and ethics of digital twins in medicine. J Law Med Ethics J Am Soc Law Med Ethics. (2022) 50:583–96. [doi: 10.](https://doi.org/10.1017/jme.2022.97) [1017/jme.2022.97](https://doi.org/10.1017/jme.2022.97)

47. Semeraro C, Lezoche M, Panetto H, Dassisti M. Digital twin paradigm: a systematic literature review. Comput Ind. (2021) 130:103469. [doi: 10.1016/j.](https://doi.org/10.1016/j.compind.2021.103469) [compind.2021.103469](https://doi.org/10.1016/j.compind.2021.103469)
