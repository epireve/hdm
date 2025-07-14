---
cite_key: chen_2024b
title: Medical Hallucination in Foundation Models and Their Impact on Healthcare
authors: Shan Chen, Shuyue Stella Li, Kumail Alhamoud, Jimin Mun, Cristina Grau, Minseok Jung, Rodrigo Gameiro, Lizhou Fan, Eugene Park, Tristan Lin, Wonjin Yoon, Maarten Sap, Yulia Tsvetkov, Paul Liang, Xuhai Xu, Xin Liu, Hyeonhoon Lee, Hae Won Park, Cynthia Breazeal
year: 2024
doi: 10.1056/NEJMcpc1802826.
date_processed: 2025-07-02
phase2_processed: true
original_folder: medrxiv_medical_hallucination
images_total: 12
images_kept: 12
images_removed: 0
tags: 
keywords: 
---

# Medical Hallucination in Foundation Models and Their Impact on Healthcare

Yubin Kim^1^, Hyewon Jeong^§1^, Shan Chen^2^, Shuyue Stella Li^3^, Mingyu Lu^§3^, Kumail Alhamoud^1^, Jimin Mun^4^, Cristina Grau^1^, Minseok Jung^1^, Rodrigo Gameiro^1^, Lizhou Fan^2^, Eugene Park^1^, Tristan Lin^8^, Joonsik Yoon^§5^, Wonjin Yoon^2^, Maarten Sap^4^, Yulia Tsvetkov^3^, Paul Liang^1^, Xuhai Xu^7^, Xin Liu^6^, Daniel McDuff^6^, Hyeonhoon Lee^5^, Hae Won Park^1^, Samir Tulebaev^§2^, Cynthia Breazeal^1^

^1^ Massachusetts Institute of Technology ^2^ Harvard Medical School ^3^ University of Washington ^4^ Carnegie Mellon University ^5^ Seoul National University Hospital ^6^ Google ^7^ Columbia University ^8^ Johns Hopkins University.

## Abstract

Foundation Models that are capable of processing and generating multi-modal data have transformed AI's role in medicine. However, a key limitation of their reliability is hallucination, where inaccurate or fabricated information can impact clinical decisions and patient safety. We define medical hallucination as any instance in which a model generates misleading medical content. This paper examines the unique characteristics, causes, and implications of medical hallucinations, with a particular focus on how these errors manifest themselves in real-world clinical scenarios. Our contributions include (1) a taxonomy for understanding and addressing medical hallucinations, (2) benchmarking models using medical hallucination dataset and physician-annotated LLM responses to real medical cases, providing direct insight into the clinical impact of hallucinations, and (3) a multi-national clinician survey on their experiences with medical hallucinations. Our results reveal that inference techniques such as Chain-of-Thought (CoT) and Search Augmented Generation can effectively reduce hallucination rates. However, despite these improvements, non-trivial levels of hallucination persist. These findings underscore the ethical and practical imperative for robust detection and mitigation strategies, establishing a foundation for regulatory policies that prioritize patient safety and maintain clinical integrity as AI becomes more integrated into healthcare. The feedback from clinicians highlights the urgent need for not only technical advances but also for clearer ethical and regulatory guidelines to ensure patient safety. A repository organizing the paper resources, summaries, and additional information is available at [https://github.com/mitmedialab/medical_hallucination](https://github.com/mitmedialab/medical_hallucination).

^‡^Corresponding Author: ybkim95@mit.edu

^§^Authors with MD degrees have contributed to the clinical expertise of this work.

## <a id="page-1-0"></a>Contents

| | Contents | | 2 |
|---|----------|-------------------------------------------------------------------------|----|
| | | List of Figures | 4 |
| | | List of Tables | 6 |
| 1 | | Introduction | 8 |
| 2 | | LLM Hallucinations in Medicine | 10 |
| | 2.1 | LLMs in Medicine: Capabilities and Adaptations. | 10 |
| | 2.2 | Differentiating Medical from General Hallucinations. | 10 |
| | 2.3 | Taxonomy of Medical Hallucinations. | 11 |
| | 2.4 | Medical Hallucinations vs. Cognitive Biases: Different Origins, Similar Outcomes. | 16 |
| | 2.5 | Clinical Implications of Medical Hallucinations. | 17 |
| 3 | | Causes of Hallucinations | 18 |
| | 3.1 | Data-Related Factors | 18 |
| | | 3.1.1 Data Quality and Noise. | 18 |
| | | 3.1.2 Data Diversity and Representativeness | 18 |
| | | 3.1.3 Size and Scope of Training Data. | 19 |
| | 3.2 | Model-Related Factors | 19 |
| | | 3.2.1 Overconfidence and Calibration | 19 |
| | | 3.2.2 Generalization to Unseen Cases | 19 |
| | | 3.2.3 Lack of Medical Reasoning. | 20 |
| | 3.3 | Healthcare Domain-Specific Challenges | 20 |
| 4 | | Detection and Evaluation of Medical Hallucinations | 20 |
| | 4.1 | Existing Detection Strategies. | 20 |
| | | 4.1.1 Factual Verification. | 21 |
| | | 4.1.2 Summary Consistency Verification. | 21 |
| | | 4.1.3 Uncertainty-Based Hallucination Detection. | 22 |
| | 4.2 | Methods for Evaluating Medical Hallucinations. | 22 |
| | 4.3 | Challenges in Medical Hallucination Detection. | 24 |
| 5 | | Mitigation Strategies | 25 |
| | 5.1 | Data-Centric Approaches. | 25 |
| | | 5.1.1 Improving Data Quality and Curation. | 25 |
| | | 5.1.2 Augmenting Training Data. | 26 |
| | 5.2 | Model-Centric Approaches | 26 |
| | | 5.2.1 Advanced Training Methods | 26 |
| | | 5.2.2 Post Training Methods | 27 |
| | 5.3 | External Knowledge Integration Techniques. | 27 |
| | | 5.3.1 Retrieval-Augmented Generation. | 28 |

| | | 5.3.2 Medical Knowledge Graphs. | 28 |
|---|-----|-----------------------------------------------------------------------------|----|
| | 5.4 | Uncertainty Quantification in Medical LLMs. | 29 |
| | | 5.4.1 Methods for Confidence Estimation. | 29 |
| | | 5.4.2 Confidence Estimation in High-Stakes Applications | 31 |
| | 5.5 | Prompt Engineering Strategies. | 31 |
| 6 | | Experiments on Medical Hallucination Benchmark | 33 |
| | 6.1 | Setup. | 33 |
| | 6.2 | Dataset & Tasks. | 35 |
| | 6.3 | Metrics. | 36 |
| | 6.4 | Models | 37 |
| | 6.5 | Results | 38 |
| 7 | | Annotations of Medical Hallucination with Clinical Case Records | 40 |
| | 7.1 | Annotation Tasks for Detecting Medical Hallucination. | 41 |
| | 7.2 | Dataset: The New England Journal of Medicine Case Reports | 41 |
| | 7.3 | Qualitative Evaluation of Clinical Reasoning Tasks Using NEJM Case Reports. | 43 |
| | 7.4 | Analysis of Hallucination Rates and Risk Distributions Across Tasks and Models. | 44 |
| | 7.5 | Inter-rater Reliability Analysis. | 45 |
| 8 | | Survey on AI/LLM Adoption and Medical Hallucinations Among Healthcare Professionals and Researchers | 48 |
| | 8.1 | Respondent Demographics | 49 |
| | 8.2 | Regional Representation | 49 |
| | 8.3 | Usage and Trust in AI/LLM Tools. | 49 |
| | 8.4 | Perceived Correctness and Encounters with AI Hallucinations | 51 |
| | 8.5 | Responses to AI Hallucinations. | 51 |
| | 8.6 | Causes of AI Hallucinations. | 51 |
| | 8.7 | Limitations of AI/LLMs and Future Outlook. | 51 |
| | 8.8 | Commonly Used AI/LLM Tools | 52 |
| | 8.9 | Future Priorities and Hallucination Safeguards. | 52 |
| 9 | | Regulatory and Legal Considerations for AI Hallucinations in Healthcare | 52 |
| | 9.1 | Deploying AI Systems in the Real-world Healthcare. | 52 |
| | 9.2 | Federal Oversight of AI Systems. | 53 |
| | 9.3 | Healthcare-Specific Regulatory Requirements. | 53 |
| | 9.4 | FDA Regulation of AI as Medical Devices. | 54 |
| | 9.5 | State-Level Regulations. | 54 |
| | 9.6 | Emerging Challenges in AI Healthcare Regulation. | 54 |
| | 9.7 | Liability and Legal Framework. | 55 |
| | | 10 Conclusion | 56 |

| | | Bibliography | 57 |
|---|-----|--------------------------------------------------------------------|----|
| A | | Survey Details | 81 |
| | A.1 | Survey Questions: Understanding LLM Hallucinations in Research and Healthcare | 81 |
| | | A.1.1 Basic Information. | 81 |
| | | A.1.2 Hallucination Experiences and Impacts. | 81 |
| | | A.1.3 Perceived Causes and Limitations. | 83 |
| | | A.1.4 AI/LLM Usage and Benefits. | 84 |
| | | A.1.5 Improvements and Future Outlook. | 84 |
| B | | Annotation Tool for Physicians | 86 |
| C | | Constructing NEJM Medical Case Records Datatset | 86 |
| | C.1 | Data Collection | 86 |
| | C.2 | Document Parsing. | 87 |
| | C.3 | Refining Parsed Content | 88 |
| | C.4 | Final Data Representation | 89 |
| | | C.4.1 Text | 89 |
| | | C.4.2 Tables | 89 |

## <a id="page-3-0"></a>List of Figures

1.  [[Overview of medical hallucinations generated by state-of](#ref-1)]the-art LLMs. (a) [[Medical expert-annotated hallucination rates and](#ref-1)] [[potential risk assessments on three medical reasoning tasks with NEJM](#ref-1)] [[Medical Records (see Section 7 for full analysis).](#ref-1)] (b) Representative [[examples of medical hallucinations from Chen et al. (2024); Vishwanath](#ref-1)] [[et al.](#ref-1)] [[(2024)](#ref-1)] respectively. (c) [[Geographic distribution of clinician](#ref-1)][[reported medical hallucination incidents providing a global perspective](#ref-1)] [[on the issue (see Subsection 8 for full analysis).](#ref-1)] . . . . . . . . . . . . . 9

| 2 | A visual taxonomy of medical hallucinations in LLMs, organized into five main clusters. (a) Factual Errors: Hallucinations arising from incorrect or conflicting factual information, encompassing Non-Factual Hallucination, Factual Hallucination, and Input-Conflicting Hallucination. (b) Outdated References: Errors stemming from reliance on obsolete guidelines or data, illustrated by Memory-Based Hallucination. (c) Spurious Correlations: Hallucinations that merge or misinterpret data in ways that produce unfounded conclusions, including Bias-Induced Hallucination, Amalgamated Hallucination, and Multimodal Integration Hallucination. (d) Fabricated Sources or Guidelines: Inventions or misrepresentations of medical procedures and research, covering Procedural Hallucination and Research Hallucination. (e) Incomplete Chains of Reasoning: Flawed or partial logical processes, such as Reasoning Hallucination, | |
|---|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| 3 | Decision-Making Hallucination, and Diagnostic Hallucination. Illustration of CoMT's process for constructing hierarchical QA pairs based on real clinical image reports. This example is from the original paper [[Jiang et al. (2024)]](#ref-64-0). | 12 |
| | . | 32 |
| 4 | Prompt examples for each step of the Chain-of-Knowledge framework. This example is from the original paper [[Li et al. (2024)]](#ref-66-0). | 34 |
| 5 | Hallucination Pointwise Score vs. Similarity Score of LLMs on the Med-Halt hallucination benchmark. This result reveals that the recent models (e.g. o3-mini, deepseek-r1, and gemini-2.0-flash) typically start with high baseline hallucination resistance and tend to see moderate but consistent gains from a simple CoT, while previous models including medical-purpose LLMs often begin at low hallucination resistance yet can benefit from different approaches (e.g. Search, CoT, and System Prompt). Moreover, retrieval-augmented generation can be less effective if the model struggles to reconcile retrieved information with its internal knowledge. | 39 |
| 6 | An annotation process of medical hallucinations in LLMs (Section 7). We utilize New England Journal of Medicine (NEJM) case records, parsing them into key elements, and feeds them into the LLM for response generation. Physicians then annotate LLM generated responses to identify medical hallucinations and potential risks, as exemplified by the inaccurate reporting of 'irregular pulse' in the patient's Emergency Department findings. | 41 |
| 7 | Distribution of medical specialties in sampled NEJM Case Records. The figure illustrates the relative frequency of different medical domains, highlighting the predominant focus on clinical medicine, hematology/oncology, and pulmonary/critical care. The bar colors represent the proportion of cases within each specialty, revealing disparities in case representation across different fields. | 42 |
| | | |

| 8 | Physician annotations on a GPT-4o generated chronological ordering of clinical events. The original case can be found at https://www.nejm.org/doi/full/10.1056/NEJMcpc1802826. | 46 |

*   9. [[Key insights from a multi-national clinician survey on medi](#ref-9)] [[cal hallucinations in clinical practice.](#ref-9)] The survey highlights the [[most commonly used LLMs and their frequency of use among physi](#ref-9)] [[cians (top), clinicians' experiences with LLM hallucinations and their](#ref-9)] [[perspectives on AI-assisted medical practice (middle), and the primary](#ref-9)] [[reasons attributed to LLM hallucinations along with the importance of](#ref-9)] [[human oversight, training, and transparency as safeguards (bottom).](#ref-9)] . 50
*   10. [[Regulatory Landscape for AI as a Medical Device:](#ref-10)] A Framework [[Categorizing General AI, Healthcare, and Software as a Medical Device](#ref-10)] [[(SaMD)-Specific Regulations.](#ref-10)] . . . . . . . . . . . . . . . . . . . . . . . 53
*   B1. [[Web-based annotation tool for NEJM Case Records. The interface dis](#ref-B1)] [[plays a clinical case with sections for case presentation, diagnosis, and](#ref-B1)] [[testing. On the right, the tool provides annotation tasks for doctors,](#ref-B1)] [[including chronological ordering of events, lab data understanding, and](#ref-B1)] [[diagnosis prediction. Annotators can input their ID, select an LLM](#ref-B1)] [[model, and save or check their annotations within the tool.](#ref-B1)] . . . . . . 86
*   B2. [[Hallucination / Risk Annotation popup in the web-based tool. This fea](#ref-B2)] [[ture allows annotators to classify highlighted text segments within the](#ref-B2)] [[NEJM Case Record. The popup window, titled "Hallucination / Risk](#ref-B2)] [[Annotation," prompts the annotator to classify "Transient tightness](#ref-B2)] [[in the chest and shoulder on the left side." as a hallucination, spec](#ref-B2)] [[ify the "Type of Hallucination" from a dropdown menu, and set the](#ref-B2)] [["Risk Level" also via a dropdown. "Cancel" and "Confirm" buttons are](#ref-B2)] [[provided at the bottom of the popup for managing the annotation.](#ref-B2)] . . 87
*   B3. [[Annotation output stored in Firebase Realtime Database. Each](#ref-B3)] [[annotation is saved under a unique](#ref-B3)] case identifier and categorized by Task Name (e.g., [[Lab Data Understanding](#ref-B3)]) and Model Type (e.g., gpt-4o). The annotator marks hallucinations, specifying the [[hallucinationType](#ref-B3)] (e.g., Contradicted Fact), and assigns a risk level. [[Once an annotator completes their annotations and clicks the save but](#ref-B3)] [[ton, the data is uploaded to Firebase and stored under their unique](#ref-B3)] [[ID.](#ref-B3)] . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 88

## <a id="page-5-0"></a>List of Tables

1.  [[Example types of medical hallucination in clinical tasks.](#ref-1)] Incor[[rect or hallucinated information is highlighted in](#ref-1)] red, while correct [[explanations are highlighted in blue. These hallucinations span multiple](#ref-1)] [[modalities demonstrating the widespread nature of errors in foundation](#ref-1)] [[models. These examples are from (Vishwanath et al., 2024; Pal et al.,](#ref-1)] [[2023; Burke and Schellmann, 2024; Brinkmann et al., 2024; Chen et al.,](#ref-1)] [[2024) respectively.](#ref-1)] . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14

| 2 | A taxonomy of medical hallucinations. The table categorizes different types of medical hallucinations, defining each type and providing real-world scenarios along with illustrative examples. | 15 |

*   3. [[An overview of medical hallucination benchmarks.](#ref-3)] The table [[summarizes existing benchmarks designed to evaluate hallucinations](#ref-3)] [[in medical contexts, showcasing the diversity of task types, input](#ref-3)] [[data sources, and evaluation metrics. These benchmarks span multiple](#ref-3)] [[domains, including medical exams, radiology reports, clinical histories,](#ref-3)] [[and LLM-generated summaries, with evaluation criteria ranging from](#ref-3)] [[accuracy and confidence scoring to fluency, coherence, and error reduction.](#ref-3)] 91
*   4. [[Benchmark tests for detecting hallucinations in LLM](#ref-4)]generated clinical reasoning. [[This table outlines various evaluation](#ref-4)] [[tests designed to assess the reliability of LLMs in clinical contexts.](#ref-4)] [[Each test targets a specific challenge, such as maintaining chronologi](#ref-4)] [[cal orders, summarizing complex cases, disambiguating medical jargon,](#ref-4)] [[identifying contradictory evidence, interpreting lab results, and gener](#ref-4)] [[ating differential diagnoses. In Section 7, we conduct 1) chronological](#ref-4)] [[ordering test, 2) lab test understanding and 3) Differential Diagnosis](#ref-4)] [[Generation Test on LLM responses annotated by human physicians.](#ref-4)] . 92

## 5. [[Strategies for mitigating medical hallucinations in LLMs.](#ref-5)] [[Methods include RAG, prompt engineering, constrained decoding, fine](#ref-5)] [[tuning, and self-reflection, each addressing different aspects of factual](#ref-5)] [[accuracy, reasoning transparency, and domain specificity.](#ref-5)] . . . . . . . . 93

*   6. [[Categorization of medical hallucinations.](#ref-6)] This taxonomy, adapted [[from Hegselmann et al. (2024b), classifies different types of medical hal](#ref-6)] [[lucinations based on their nature, including unsupported conditions,](#ref-6)] [[medications, procedures, temporal misrepresentations, and factual](#ref-6)] [[inconsistencies.](#ref-6)] . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 93
*   7. [[Risk assessment framework for medical hallucinations.](#ref-7)] Adapted [[from Asgari et al. (2024), this table categorizes potential risk levels of](#ref-7)] [[medical hallucinations, ranging from no risk (0) to catastrophic impact](#ref-7)] [[(5). The framework evaluates the severity of hallucinations based on](#ref-7)] [[their potential influence on clinical decision-making and patient safety.](#ref-7)] 94

## <a id="page-7-0"></a>1 Introduction

The integration of foundation models (e.g., Large Language Models [LLM] and Large Vision Language Models [VLM]) into healthcare applications presents significant opportunities, from enhancing clinical decision support ([[McDuff et al.,](#ref-68-0)] [[2023;](#ref-68-0)] [[Kim](#ref-65-0)] [[et al.,](#ref-65-0)] [[2024;](#ref-65-0)] [[Li et al.,](#ref-65-1)] [[2024)]](#ref-65-1) to transforming medical research ([[Singhal et al.,](#ref-71-0)] [[2023;](#ref-71-0)] [[Saab et al.,](#ref-72-0)] [[2024a)]](#ref-72-0) and improving healthcare quality and safety ([[Goodman et al.,](#ref-62-0)] [[2024;](#ref-62-0)] [[Jalilian et al.,](#ref-64-1)] [[2024;](#ref-64-1)] [[Mukherjee et al.,](#ref-67-0)] [[2024)]](#ref-67-0). However, this integration also brings a number of critical challenges to the forefront. A particularly concerning issue is the phenomenon of hallucination or confabulation, instances where LLMs generate plausible but factually incorrect or fabricated information ([[Ji et al.,](#ref-64-2)] [[2023a;](#ref-64-2)] [[Chen et al.,](#ref-59-0)] [[2023a)]](#ref-59-0). Hallucinations are a concern across various domains, including finance ([[Kang](#ref-65-2)] [[and Liu,](#ref-65-2)] [[2023)]](#ref-65-2), legal ([[Dahl et al.,](#ref-60-1)] [[2024)]](#ref-60-1), code generation ([[Agarwal et al.,](#ref-57-0)] [[2024)]](#ref-57-0), education ([[de Almeida da Silva et al.,](#ref-60-2)] [[2024)]](#ref-60-2) and more ([[Sun et al.,](#ref-72-1)] [[2024;](#ref-72-1)] [[Kang and Liu,](#ref-65-2)] [[2023;](#ref-65-2)] [[Wang et al.,](#ref-76-0)] [[2024)]](#ref-76-0). Medical hallucinations pose particularly serious risks as incorrect dosages of medications, drug interactions, or diagnostic criteria can directly lead to life-threatening outcomes ([[Chen et al.,](#ref-58-2)] [[2024;](#ref-58-2)] [[Szolovits,](#ref-72-2)] [[2024)]](#ref-72-2).

Just as human clinicians can be susceptible to cognitive biases in clinical decision making ([[Ke et al.,](#ref-65-3)] [[2024;](#ref-65-3)] [[Vally et al.,](#ref-74-0)] [[2023)]](#ref-74-0), LLMs exhibit their own form of systematic errors through what we refer to as medical hallucinations. In these cases, LLMs generate incorrect or misleading medical information that could adversely affect clinical decision making and patient outcomes. For example, an LLM might hallucinate about patient information, history, and symptoms ([[Vishwanath et al.,](#ref-75-0)] [[2024)]](#ref-75-0) on a clinical note that does not align with the original note. This example corresponds to the confirmation bias of a physician in which contradictory symptoms are overlooked and eventually lead to inappropriate treatment protocols (Fig. [[1)]](#ref-1)). Although the concept of hallucinations in LLM is not new ([[Bai et al.,](#ref-58-3)] [[2024)]](#ref-58-3), its implications in the medical domain warrant specific attention due to the high stakes involved and the minimal margin of error ([[Umapathi et al.,](#ref-73-0)] [[2023)]](#ref-73-0).

This paper builds upon existing research on LLM hallucinations ([[Rawte et al.,](#ref-70-1)] [[2023;](#ref-70-1)] [[Tonmoy et al.,](#ref-73-1)] [[2024;](#ref-73-1)] [[Huang et al.,](#ref-63-1)] [[2023;](#ref-63-1)] [[Ji et al.,](#ref-64-3)] [[2023b)]](#ref-64-3) and extends it to specific challenges in medical applications, where LLMs face particular hurdles: 1) the rapid evolution of medical information, leading to potential model obsolescence ([[Wu](#ref-76-1)] [[et al.,](#ref-76-1)] [[2024)]](#ref-76-1), 2) the necessity of precision in medical information ([[Topol,](#ref-73-2)] [[2019)]](#ref-73-2), 3) the interconnected nature of medical concepts, where a small error can cascade ([[Bari](#ref-57-1)] [[et al.,](#ref-57-1)] [[2016)]](#ref-57-1), and 4) the presence of domain-specific jargon and context that require specialized interpretation ([[Yao et al.,](#ref-78-0)] [[2023)]](#ref-78-0).

Our work makes three primary contributions. First, we introduce a taxonomy for medical hallucination in LLM, providing a structured framework to categorize AIgenerated medical misinformation. Second, we conduct comprehensive experimental analyses across various medical subdomains, including general practice, specialized fields such as oncology and cardiology, and medical education scenarios, utilizing stateof-the-art LLMs such as o3-mini, Gemini-2.0 Flash Thinking, and domain-specific models such as Meditron ([[Chen et al.,](#ref-58-4)] [[2023)]](#ref-58-4) and Med-Alpaca ([[Han et al.,](#ref-62-1)] [[2023)]](#ref-62-1). Third, we present findings from a survey of clinicians, providing insights into how medical professionals perceive and experience hallucinations when they use LLMs for their practice or research. These contributions collectively advance our understanding of medical hallucinations and their mitigation strategies, with implications extending to regulatory frameworks and best practices for the deployment of AI in clinical settings.

<a id="page-8-0"></a>![Overview of medical hallucinations generated by state-of-the-art LLMs. (a) presents a bar chart comparing hallucination rates across different large language models (LLMs) on three medical tasks: chronological ordering, lab data understanding, and diagnosis prediction. Hallucination severity is color-coded. (b) shows examples of LLMs incorrectly interpreting medical images and summarizing patient records, with ground truth annotations highlighting the errors. (c) includes a pie chart showing respondent geographic distribution and a bar chart illustrating the frequency of research ideas among respondents. The image aims to illustrate and quantify the hallucination problem in LLMs applied to healthcare.](_page_8_Figure_2.jpeg)

**Figure 1:** Overview of medical hallucinations generated by state-of-the-art LLMs. (a) Medical expert-annotated hallucination rates and potential risk assessments on three medical reasoning tasks with NEJM Medical Records (see Section [[7]](#ref-7) for full analysis). (b) Representative examples of medical hallucinations from [[Chen et al.](#ref-60-0)] [[(2024)]](#ref-60-0); [[Vishwanath et al.](#ref-75-0)] [[(2024)]](#ref-75-0) respectively. (c) Geographic distribution of clinicianreported medical hallucination incidents providing a global perspective on the issue (see Subsection [[8]](#ref-8) for full analysis).

## <a id="page-9-0"></a>2 LLM Hallucinations in Medicine

Hallucinations in large language models (LLMs) can undermine the reliability of AIgenerated medical information, particularly in clinical settings where inaccuracies may adversely affect patient outcomes. In non-clinical contexts, errors introduced by LLMs may have limited impact or could be more easily detected, particularly because users often possess the background knowledge to verify or cross-reference the information provided, unlike in many medical scenarios where patients may lack the expertise to assess the accuracy of AI-generated medical advice. However, in healthcare, subtle or plausible-sounding misinformation can influence diagnostic reasoning, therapeutic recommendations, or patient counseling ([[Miles-Jay et al.,](#ref-67-1)] [[2023;](#ref-67-1)] [[Xia et al.,](#ref-77-0)] [[2024;](#ref-77-0)] [[Mehta and Devarakonda,](#ref-67-2)] [[2018;](#ref-67-2)] [[Mohammadi et al.,](#ref-67-3)] [[2023)]](#ref-67-3). In this section, we define hallucination in a clinical context.

## <a id="page-9-1"></a>2.1 LLMs in Medicine: Capabilities and Adaptations

Recent advancements in transformer-based architectures and large-scale pretraining have elevated LLM performance in tasks requiring language comprehension, contextual reasoning, and multimodal analysis ([[Vaswani et al.,](#ref-74-1)] [[2017;](#ref-74-1)] [[Kaplan et al.,](#ref-65-4)] [[2020)]](#ref-65-4). Examples include OpenAI's GPT series, Google's Gemini, Anthropic's Claude, and Meta's Llama family. In medicine, researchers adapt these models using domain-specific corpora, instruction tuning, and retrieval-augmented generation (RAG), with the goal of aligning outputs more closely to clinical practice ([[Wei et al.,](#ref-76-2)] [[2022;](#ref-76-2)] [[Lewis et al.,](#ref-66-1)] [[2020)]](#ref-66-1).

Several specialized LLMs have demonstrated promising results on medical benchmarks. Med-PaLM and Med-PaLM 2, for instance, exhibit strong performance on tasks such as MedQA ([[Jin et al.,](#ref-64-4)] [[2021)]](#ref-64-4), MedMCQA ([[Pal et al.,](#ref-70-2)] [[2022)]](#ref-70-2), and PubMedQA ([[Jin](#ref-64-5)] [[et al.,](#ref-64-5)] [[2019)]](#ref-64-5) by integrating biomedical texts into their training regimes ([[Singhal et al.,](#ref-71-1)] [[2022)]](#ref-71-1). Google's Med-Gemini extends these methods by leveraging multimodal inputs, leading to improved accuracy in clinical evaluations ([[Saab et al.,](#ref-72-3)] [[2024b)]](#ref-72-3). Open-source initiatives such as Meditron ([[Chen et al.,](#ref-58-4)] [[2023)]](#ref-58-4) and Med42 ([[Christophe et al.,](#ref-59-1)] [[2024)]](#ref-59-1) release models trained on large-scale biomedical data, offering transparency and fostering community-driven improvements. Despite these tailored efforts, LLMs can generate outputs that appear plausible yet lack factual or logical foundations, manifesting as hallucinations in a clinical context.

A recent survey ([[Nazi and Peng,](#ref-68-1)] [[2024)]](#ref-68-1) reinforces these observations, offering a comprehensive review of LLMs in healthcare. In particular, it highlights how domainspecific adaptations such as instruction tuning and retrieval-augmented generation can enhance patient outcomes and streamline medical knowledge dissemination, while also emphasizing the persistent challenges of reliability, interpretability, and hallucination risk.

## <a id="page-9-2"></a>2.2 Differentiating Medical from General Hallucinations

LLM hallucinations refer to outputs that are factually incorrect, logically inconsistent, or inadequately grounded in reliable sources ([[Huang et al.,](#ref-63-1)] [[2023)]](#ref-63-1). In general domains, these hallucinations may take the form of factual errors or non-sequiturs. In medicine, they can be more challenging to detect because the language used often appears clinically valid while containing critical inaccuracies ([[Singhal et al.,](#ref-71-1)] [[2022;](#ref-71-1)] [[Mohammadi](#ref-67-3)] [[et al.,](#ref-67-3)] [[2023)]](#ref-67-3).

Medical hallucinations exhibit two distinct features compared to their generalpurpose counterparts. First, they arise within specialized tasks such as diagnostic reasoning, therapeutic planning, or interpretation of laboratory findings, where inaccuracies have immediate implications for patient care ([[Xu et al.,](#ref-77-1)] [[2024b;](#ref-77-1)] [[Miles-Jay et al.,](#ref-67-1)] [[2023;](#ref-67-1)] [[Xia et al.,](#ref-77-0)] [[2024)]](#ref-77-0). Second, these hallucinations frequently use domain-specific terms and appear to present coherent logic, which can make them difficult to recognize without expert scrutiny ([[Asgari et al.,](#ref-56-1)] [[2024;](#ref-56-1)] [[Liu et al.,](#ref-66-2)] [[2024)]](#ref-66-2). In settings where clinicians or patients rely on AI recommendations, a tendency potentially heightened in domains like medicine ([[Zhou et al.,](#ref-78-1)] [[2025)]](#ref-78-1), unrecognized errors risk delaying proper interventions or redirecting care pathways.

Moreover, the impact of medical hallucinations is far more severe. Errors in clinical reasoning or misleading treatment recommendations can directly harm patients by delaying proper care or leading to inappropriate interventions ([[Miles-Jay et al.,](#ref-67-1)] [[2023;](#ref-67-1)] [[Xia et al.,](#ref-77-0)] [[2024;](#ref-77-0)] [[Mehta and Devarakonda,](#ref-67-2)] [[2018)]](#ref-67-2). Furthermore, the detectability of such hallucinations depends on the level of domain expertise of the audience and the quality of the prompting provided to the model. Domain experts are more likely to identify subtle inaccuracies in clinical terminology and reasoning, whereas non-experts may struggle to discern these errors, thereby increasing the risk of misinterpretation ([[Asgari et al.,](#ref-56-1)] [[2024;](#ref-56-1)] [[Liu et al.,](#ref-66-2)] [[2024)]](#ref-66-2).

These distinctions are crucial: whereas general hallucinations might lead to relatively benign mistakes, medical hallucinations can undermine patient safety and erode trust in AI-assisted clinical systems ([[Miles-Jay et al.,](#ref-67-1)] [[2023;](#ref-67-1)] [[Xia et al.,](#ref-77-0)] [[2024;](#ref-77-0)] [[Mehta](#ref-67-2)] [[and Devarakonda,](#ref-67-2)] [[2018;](#ref-67-2)] [[Asgari et al.,](#ref-56-1)] [[2024;](#ref-56-1)] [[Liu et al.,](#ref-66-2)] [[2024;](#ref-66-2)] [[Pal et al.,](#ref-70-0)] [[2023)]](#ref-70-0).

## <a id="page-10-0"></a>2.3 Taxonomy of Medical Hallucinations

A growing body of literature proposes frameworks for classifying medical hallucinations in LLM outputs. [[Agarwal et al.](#ref-56-2)] [[(2024)]](#ref-56-2) emphasize the severity of errors and their root causes, whereas [[Ahmad et al.](#ref-57-2)] [[(2023)]](#ref-57-2) focus on preserving clinician trust by identifying the types of misinformation that most erode confidence. [[Pal et al.](#ref-70-0)] [[(2023)]](#ref-70-0) introduce an empirical benchmark for quantifying hallucination frequency in real-world scenarios, underscoring their prevalence. Efforts by [[Hegselmann et al.](#ref-63-0)] [[(2024b)]](#ref-63-0) and [[Moradi et al.](#ref-67-4)] [[(2021)]](#ref-67-4) highlight how data quality and curation practices can influence hallucination rates, especially in the context of patient summaries.

Informed by these studies ([[Zhang et al.,](#ref-78-2)] [[2024;](#ref-78-2)] [[Yu et al.,](#ref-78-3)] [[2024;](#ref-78-3)] [[Lee et al.,](#ref-66-3)] [[2023;](#ref-66-3)] [[Asgari et al.,](#ref-56-1)] [[2024;](#ref-56-1)] [[Ziaei and Schmidgall,](#ref-79-0)] [[2023;](#ref-79-0)] [[Pressman et al.,](#ref-69-0)] [[2024;](#ref-69-0)] [[Li et al.,](#ref-66-4)] [[2024;](#ref-66-4)] [[Zhang et al.,](#ref-79-1)] [[2023;](#ref-79-1)] [[Wu et al.,](#ref-75-1)] [[2023)]](#ref-75-1), we first illustrate our taxonomy in Figure [[2]](#ref-2), which clusters hallucinations into five main categories (factual errors, outdated references, spurious correlations, incomplete chains of reasoning, and fabricated sources or guidelines) based on their underlying causes and manifestations. Subsequently, Table [[2]](#ref-2) provides a more granular breakdown of each hallucination types that categorizes hallucinations and offers concrete examples of these categories, illustrating the various ways

![This pie chart categorizes types of hallucinations in large language models. Categories include those based on reasoning errors (incomplete chains of reasoning), factual errors (outdated references), source fabrication, spurious correlations, and input conflicts. Other categories reflect the hallucination's basis: decision-making, diagnostic, procedural, research, memory, or a multimodal integration of information. The chart aids in understanding the diverse origins of model hallucinations.](_page_11_Figure_1.jpeg)

<a id="page-11-0"></a>in which clinically oriented LLMs may produce superficially plausible but ultimately incorrect outputs.

**Figure 2:** A visual taxonomy of medical hallucinations in LLMs, organized into five main clusters. (a) Factual Errors: Hallucinations arising from incorrect or conflicting factual information, encompassing Non-Factual Hallucination, Factual Hallucination, and Input-Conflicting Hallucination. (b) Outdated References: Errors stemming from reliance on obsolete guidelines or data, illustrated by Memory-Based Hallucination. (c) Spurious Correlations: Hallucinations that merge or misinterpret data in ways that produce unfounded conclusions, including Bias-Induced Hallucination, Amalgamated Hallucination, and Multimodal Integration Hallucination. (d) Fabricated Sources or Guidelines: Inventions or misrepresentations of medical procedures and research, covering Procedural Hallucination and Research Hallucination. (e) Incomplete Chains of Reasoning: Flawed or partial logical processes, such as Reasoning Hallucination, Decision-Making Hallucination, and Diagnostic Hallucination.

These hallucinations are exacerbated by the complexity and specificity of medical knowledge, where subtle differences in terminology or reasoning can lead to significant misunderstandings ([[Miles-Jay et al.,](#ref-67-1)] [[2023;](#ref-67-1)] [[Mohammadi et al.,](#ref-67-3)] [[2023)]](#ref-67-3). Furthermore, as shown in Table [[1]](#ref-1), these hallucinations can manifest across a wide range of medical tasks, from symptom diagnosis and patient management to the interpretation of lab results and visual data.

<a id="page-13-0"></a>**Table 1:** Example types of medical hallucination in clinical tasks. Incorrect or hallucinated information is highlighted in red, while correct explanations are highlighted in blue. These hallucinations span multiple modalities demonstrating the widespread nature of errors in foundation models. These examples are from ([[Vish](#ref-75-0)] [[wanath et al.,](#ref-75-0)] [[2024;](#ref-75-0)] [[Pal et al.,](#ref-70-0)] [[2023;](#ref-70-0)] [[Burke and Schellmann,](#ref-58-0)] [[2024;](#ref-58-0)] [[Brinkmann et al.,](#ref-58-1)] [[2024;](#ref-58-1)] [[Chen et al.,](#ref-60-0)] [[2024)]](#ref-60-0) respectively.

| Type | Input | LLM Response | Explanation |
|---------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Incorrect symptom~s/diagnosis/surgical~procedures | She took three SL nitro's at home, with some minor improvement in her CP but when it did not resolve she called Dr.OOO referred her to the ER. She denied any associated SOB, nausea/vomiting. She denies any orthopnea, PND, edema or palpitations. | She denied shortness of breath, nausea, vomiting, leg swelling, and palpitations. An EKG showed an unchanged left bundle branch block (LBBB). | Leg swelling in the summary is a hallucinated symptom. Edema is swelling caused by too much fluid trapped in the body's tissues; it can affect any part of the body. |
| Incorrect Patient Management | A 24-year-old pregnant woman at 28 weeks gestation presents to the emergency department with complaints of fever with chills A specimen is collected to test for Lyme disease. What is the next best step for this patient? | Tetracycline is the best next step in the management of this patient's suspected Lyme disease | Amoxicillin is a safe and effective treatment for Lyme disease in pregnancy |
| Non-existent Medication in Transcription | | Well, in about, I think it was 2001, I became ill with a fairly serious strain of viral something, but I didn't take any medication, I took Hyperactivated Antibiotics and sometimes I would think that was worse. | GT: Well in about I think it was two thousand and one I became ill with a fairly serious strain of viral something . |
| | Audio snippets | | |
| Misinterpretation of Lab Results | A 37-year-old man was admitted to this hospital because of a rash Laboratory Data shows Elevated globulin levels (4.7 g/dL; Reference: 1.9-4.1) What's your medical insights? | Elevated, indicating increased production of immunoglobulins | The elevated globulins were actually due to polyclonal B-cell activation from HIV, not a general increase in immunoglobulin production. |
| Incorrect visual understanding | Which of the biggest in this image, lung, liver or heart? | In this image, the biggest organ is the heart. | In this image, the lung appears to be the biggest. |

<a id="page-14-0"></a>**Table 2:** A taxonomy of medical hallucinations. The table categorizes different types of medical hallucinations, defining each type and providing real-world scenarios along with illustrative examples.

| Type | Definition | Scenario | Example |
|---|---|---|---|
| Amalgamated Hallucination | Merging unrelated information into a single response, creating factually incoherent outputs. | A patient with type 2 diabetes also has a skin infection. | "Use insulin topically for 5 days to treat both infection and blood glucose." Incorrectly merges insulin therapy with antibiotic ointment, risking confusion and improper care. |
| Non-Factual Hallucination | Fabricating plausible but incorrect information without grounding in factual data. | The LLM is asked about a drug that does not exist in real pharmacopeia. | "Penmerol is the recommended medication." Invents a drug name with no clinical basis, misleading clinicians and undermining trust. |
| Input Conflicting Hallucination | Generating content that conflicts with the provided input, such as task instructions or task data. | Patient notes indicate a severe penicillin allergy. | "Prescribe amoxicillin for the infection." Overlooks documented allergy, potentially causing severe adverse reactions. |
| Reasoning Hallucination | Failing logical reasoning or problem-solving tasks, leading to flawed clinical recommendations. | The LLM must explain the pathophysiology of congestive heart failure (CHF). | "CHF is primarily caused by lung infections." Provides a logical sounding but incorrect chain of thought, jeopardizing accurate diagnosis and treatment. |
| Memory-Based Hallucination | Inaccurately recalling or fabricating information the model was trained to retrieve. | The LLM is asked for current hypertension guidelines. | "According to the 2023 HPC guidelines, start with drug X." Quotes a non-existent or outdated protocol, potentially causing suboptimal or incorrect care. |
| Decision Making Hallucination | Suggesting inappropriate treatment plans or clinical decisions due to flawed reasoning or data interpretation. | A pregnant patient with hypertension consults the LLM for medication guidance. | "Medication X is safe in pregnancy." In reality, it is contraindicated, risking harm to both mother and fetus. |
| Diagnostic Hallucination | Proposing incorrect diagnoses or misinterpreting clinical signs, leading to potential misdiagnosis. | The LLM is given lab results inconsistent with pneumonia. | "This patient has pneumonia." Confidently diagnoses pneumonia despite contradictory evidence, delaying correct treatment and risking patient harm. |
| Procedural Hallucination | Errors in describing medical procedures or protocols. | A user asks for a guide to laparoscopic cholecystectomy. | "Apply glutaraldehyde to the gall bladder before removal." Invents an unrecognized surgical step, causing confusion or potential complications if followed. |
| Factual Hallucination | Generating incorrect factual information, critical in clinical documentation and automation. | A user queries the LLM about the FDA approval status of a newly introduced medication. | "Drug X is FDA-approved for condition Y." Claims an unapproved drug is authorized, potentially prompting off-label or inappropriate use. |
| Bias-Induced Hallucination | Reflecting or amplifying biases in training data, leading to discriminatory or skewed outputs. | The LLM evaluates a minority patient with atypical symptoms. | "Patients of X background rarely develop condition Y." Overlooks key symptoms or leans on stereotypes, perpetuating healthcare disparities. |
| Research Hallucination | Misinterpreting or fabricating research data, potentially impacting evidence based medicine or drug development. | The LLM is asked about recent clinical trials for a novel anticancer drug. | "A Phase III trial confirmed 90% efficacy." References a non-existent trial, leading clinicians to believe there is strong evidence for efficacy when none exists. |
| Multimodal Integration Hallucination | Errors in interpreting data from multiple sources (e.g., text, imaging, lab results). | The LLM receives both a CT scan image and a textual report indicating a suspicious liver lesion. | "CT imaging shows no liver abnormalities." Contradicts the textual findings, resulting in missed or delayed diagnosis. |

## <a id="page-15-0"></a>2.4 Medical Hallucinations vs. Cognitive Biases: Different Origins, Similar Outcomes

Cognitive biases in medical practice are well-studied phenomena, whereby clinicians deviate from optimal decision-making due to systematic errors in judgment and reasoning ([[Tversky and Kahneman,](#ref-73-3)] [[1974;](#ref-73-3)] [[O'Brien,](#ref-69-1)] [[2012;](#ref-69-1)] [[Blumenthal-Barby and Krieger,](#ref-57-3)] [[2014;](#ref-57-3)] [[Saposnik et al.,](#ref-71-2)] [[2016)]](#ref-71-2). These biases frequently arise in time-constrained or high-stress environments and can undermine the diagnostic and therapeutic process. Although LLMs do not possess human psychology, the erroneous outputs they produce often exhibit patterns that resemble these biases in clinical reasoning. By comparing medical hallucinations in LLMs to established cognitive biases, researchers gain insights into both the roots of AI-driven errors and potential strategies to mitigate them.

## Common Cognitive Biases in Clinical Practice parallels with LLM Hallucinations.

Clinicians frequently experience biases such as anchoring bias, which entails relying excessively on initial impressions, even when new evidence suggests alternative explanations. Similarly, confirmation bias leads to selective acceptance of data that reinforces a working diagnosis, while availability bias skews judgments toward diagnoses that are more memorable or have been recently encountered ([[Ly et al.,](#ref-66-5)] [[2023;](#ref-66-5)] [[Blumenthal-Barby and Krieger,](#ref-57-3)] [[2014;](#ref-57-3)] [[Rehana and Huda,](#ref-70-3)] [[2021;](#ref-70-3)] [[Hammond et al.,](#ref-63-2)] [[2021)]](#ref-63-2). Clinicians also exhibit overconfidence bias, characterized by unwarranted certainty in diagnostic or therapeutic decisions ([[Saposnik et al.,](#ref-71-2)] [[2016;](#ref-71-2)] [[Mehta and Devarakonda,](#ref-67-2)] [[2018)]](#ref-67-2), as well as premature closure, where they settle on a plausible explanation without fully considering differential diagnoses ([[Blumenthal-Barby and Krieger,](#ref-57-3)] [[2014)]](#ref-57-3).

Hallucinations in medical LLMs echo these biases in various ways. Anchoring appears when a model disproportionately relies on the initial part of a prompt, neglecting subsequent details or contextual information. Confirmation bias emerges when an LLM's response aligns too closely with the user's implied hypothesis, neglecting contradictory evidence. Availability manifests in the model's tendency to propose diagnoses or treatments that are disproportionately represented in its training data. Overconfidence becomes evident when LLM outputs present an unwarranted level of certainty, a phenomenon linked to poor calibration ([[Cao et al.,](#ref-59-2)] [[2021;](#ref-59-2)] [[Hagendorff et al.,](#ref-62-2)] [[2023)]](#ref-62-2). Finally, premature closure can occur if the model settles on a single, plausible-sounding conclusion without comprehensively considering differential possibilities or additional context ([[Hegselmann et al.,](#ref-63-0)] [[2024b)]](#ref-63-0). Although the LLM lacks human cognition, the statistical patterns it learns can simulate biases that arise from heuristic-based thinking in clinicians.

Despite these surface-level similarities, the basis of LLM hallucinations diverges from the cognitive underpinnings of human biases. Cognitive biases result from heuristic shortcuts, emotional influences, memory limitations, and other psychological factors ([[Tversky and Kahneman,](#ref-73-3)] [[1974;](#ref-73-3)] [[O'Brien,](#ref-69-1)] [[2012)]](#ref-69-1). In contrast, medical LLM hallucinations are the product of learned statistical correlations in training data, coupled with architectural constraints such as limited causal reasoning ([[Jiang et al.,](#ref-64-6)] [[2023;](#ref-64-6)] [[Glicksberg,](#ref-62-3)] [[2024)]](#ref-62-3). This distinction means that while clinicians might fail to adjust their thinking in light of conflicting information, an LLM may simply lack exposure to correct or more recent evidence—or fail to retrieve it—leading to erroneous outputs. Consequently, mitigation requires strategies tailored to each context: clinicians might benefit from decision-support tools and reflective practice to counter personal biases, while LLMs demand better data curation, retrieval-augmented generation, or explicit calibration methods to curb hallucinations and unwarranted certainty.

Identifying parallels between cognitive biases and LLM hallucinations highlights potential remediation avenues. Techniques for reducing anchoring and confirmation bias in clinical settings—such as prompting systematic consideration of differential diagnoses—may inform prompt design or chain-of-thought strategies in LLMs ([[Wang](#ref-76-3)] [[and Zhang,](#ref-76-3)] [[2024b)]](#ref-76-3). Encouraging models to output uncertainty estimates or alternative explanations can address overconfidence and premature closure biases, especially if users are guided to critically evaluate multiple options. Meanwhile, robust finetuning procedures and retrieval-augmented generation can improve the balance of training data, mitigating the model's availability bias. Taken together, these efforts could reduce the frequency and severity of hallucinations, ensuring AI-assisted systems more closely align with evidence-based clinical practice.

## <a id="page-16-0"></a>2.5 Clinical Implications of Medical Hallucinations

The integration of large language models into healthcare introduces several risks with direct consequences for patient care and broader clinical practice. Hallucinated outputs that appear credible can guide clinicians toward ineffective or harmful interventions, influencing therapeutic choices, diagnostic pathways, and patient-provider communication ([[Topol,](#ref-73-2)] [[2019;](#ref-73-2)] [[Mehta and Devarakonda,](#ref-67-2)] [[2018;](#ref-67-2)] [[Hata et al.,](#ref-63-3)] [[2022)]](#ref-63-3). This section articulates how such hallucinations undermine patient safety, disrupt clinical workflows, and create additional ethical and legal complexities.

A chief concern is patient safety. When hallucinated outputs lead to incorrect recommendations or misdiagnoses, clinicians may adopt interventions that inadvertently harm patients ([[Hata et al.,](#ref-63-3)] [[2022)]](#ref-63-3). Even minor inaccuracies can escalate clinical risks if they go unnoticed or align with a clinician's cognitive bias, ultimately compromising the quality of care.

Another critical dimension is the erosion of trust in AI systems. Repeated hallucinations often breed skepticism among both healthcare providers and patients ([[Willems](#ref-75-2)] [[et al.,](#ref-75-2)] [[2023)]](#ref-75-2). Providers are less inclined to rely on potentially error-prone models, while patients may grow apprehensive about the reliability of artificial intelligence in medical decisions, inhibiting broader integration of these tools in clinical practice.

These errors also disrupt workflow efficiency. Hallucinations can force clinicians to verify or correct AI-generated information, adding to their workload and diverting attention from direct patient care ([[McDermott et al.,](#ref-67-5)] [[2024)]](#ref-67-5). This burden can diminish the potential benefits of automation and decision support, particularly in time-sensitive or resource-constrained environments.

Beyond immediate bedside concerns, ethical and legal implications arise from the growing reliance on LLM-based recommendations ([[Fanta and Pretorius,](#ref-61-0)] [[2023)]](#ref-61-0). As models increasingly influence clinical decision-making, the question of accountability for AI-driven errors becomes more urgent. Uncertainty over liability may impede system-wide adoption and complicate the legal landscape for healthcare providers, technology developers, and regulators.

Finally, hallucinations curtail the impact on precision medicine by reducing the trustworthiness of personalized treatment recommendations. If an LLM's outputs cannot consistently deliver accurate, context-specific insights, it undermines the potential to tailor interventions to individual patient profiles ([[Vasquez and Albeck,](#ref-74-2)] [[2023)]](#ref-74-2). The vision of leveraging big data to refine therapeutic strategies becomes more challenging if model-generated advice contains undetected inaccuracies.

Overall, understanding the clinical implications of medical hallucinations is essential for developing safer, more trustworthy models in healthcare. Stakeholders must consider patient safety, provider engagement, and the broader ethical and legal context to ensure that emerging technologies ultimately enhance, rather than impede, medical practice.

## <a id="page-17-0"></a>3 Causes of Hallucinations

Hallucinations in medical LLMs often arise from a confluence of factors relating to data, model architecture, and the unique complexities of healthcare. Although Section [[2]](#ref-2) examined how hallucinations manifest and why they matter in clinical contexts, this section provides a deeper look at the root causes. By understanding where and how LLMs fail, researchers and practitioners can prioritize interventions that safeguard patient well-being and advance the reliability of AI in medicine.

## <a id="page-17-1"></a>3.1 Data-Related Factors

The quality, diversity, and scope of training data profoundly influence model performance. Gaps in these areas are key contributors to hallucinations.

## <a id="page-17-2"></a>3.1.1 Data Quality and Noise

Clinical datasets, such as electronic health records (EHRs) and physician notes, often contain noise in the form of incomplete entries, misspellings, and ambiguous abbreviations. These inconsistencies propagate errors into LLM training ([[Hegselmann et al.,](#ref-63-0)] [[2024b)]](#ref-63-0). For instance, a lack of structured input may confuse models, leading them to replicate false patterns or irrelevant outputs ([[Moradi et al.,](#ref-67-4)] [[2021)]](#ref-67-4). Outdated data further compounds this issue. Medical knowledge evolves continuously, and guidelines can quickly become outdated ([[Shekelle et al.,](#ref-71-3)] [[2002)]](#ref-71-3). Models trained on static or historical data may recommend ineffective treatments, reducing clinical utility ([[Glicksberg,](#ref-62-3)] [[2024)]](#ref-62-3). Addressing these issues requires rigorous data curation, including noise filtering, deduplication, and alignment with current medical guidelines.

### <a id="page-17-3"></a>3.1.2 Data Diversity and Representativeness

Training data must reflect the diversity of patient populations, disease presentations, and healthcare systems. Biased datasets, such as those dominated by common conditions or data from high-resource settings, limit model generalizability ([[Chen et al.,](#ref-59-3)] [[2019)]](#ref-59-3). For instance, [[Restrepo et al.](#ref-70-4)] [[(2024)]](#ref-70-4) highlight that underrepresentation of minority groups can lead to systematic errors in AI predictions. Rare diseases are particularly affected. Models often lack exposure to these conditions during training, leading to hallucinations when generating diagnostic insights ([[Svenstrup et al.,](#ref-71-4)] [[2015)]](#ref-71-4). Similarly, regional variations in clinical terminology and disease prevalence further exacerbate performance disparities ([[Wang and Zhang,](#ref-76-4)] [[2024a)]](#ref-76-4). Standardized terminologies, such as Systematized Nomenclature of Medicine Clinical Terms (SNOMED CT), can improve consistency by harmonizing medical language across datasets ([[Donnelly et al.,](#ref-60-3)] [[2006)]](#ref-60-3). Efforts to mitigate data diversity challenges include targeted inclusion of underrepresented conditions and populations, as well as benchmarking on globally diverse datasets to assess generalizability ([[Chen et al.,](#ref-58-5)] [[2024;](#ref-58-5)] [[Matos et al.,](#ref-67-6)] [[2024;](#ref-67-6)] [[Group,](#ref-62-4)] [[2023)]](#ref-62-4).

### <a id="page-18-0"></a>3.1.3 Size and Scope of Training Data

While large-scale datasets are critical for training LLMs, general-purpose models often lack sufficient exposure to domain-specific medical content. As demonstrated by [[Alsentzer et al.](#ref-56-3)] [[(2019)]](#ref-56-3), fine-tuning models on biomedical corpora significantly improves their understanding of clinical text. In contrast, inadequate training data coverage creates knowledge gaps, causing models to hallucinate when addressing unfamiliar medical topics ([[Lee et al.,](#ref-66-6)] [[2024)]](#ref-66-6). Comprehensive training datasets that incorporate annotated clinical notes, peer-reviewed research, and real-world guidelines are essential to ensure coverage of both common and edge cases. Expanding the scope to include rare diseases, specialized treatments, and emerging conditions can further enhance model reliability ([[Jiang et al.,](#ref-64-6)] [[2023)]](#ref-64-6).

## <a id="page-18-1"></a>3.2 Model-Related Factors

Limitations intrinsic to model architecture and behavior also contribute to hallucinations, particularly in medical applications.

## <a id="page-18-2"></a>3.2.1 Overconfidence and Calibration

LLMs frequently exhibit overconfidence, generating outputs with high certainty even when the information is incorrect. Poor calibration—where confidence scores fail to align with prediction accuracy—can mislead clinicians into trusting inaccurate outputs ([[Cao et al.,](#ref-59-2)] [[2021)]](#ref-59-2). For example, [[Yuan et al.](#ref-78-4)] [[(2023)]](#ref-78-4) highlight the need for improved uncertainty estimation techniques to mitigate overconfidence. Effective strategies for addressing calibration include probabilistic modeling, confidence-aware training, and ensemble methods. These approaches enable models to provide uncertainty estimates alongside predictions, promoting safer integration into clinical workflows.

### <a id="page-18-3"></a>3.2.2 Generalization to Unseen Cases

Medical LLMs struggle to generalize beyond their training data, particularly when faced with rare diseases, novel treatments, or atypical clinical presentations. Models trained on imbalanced datasets often extrapolate from unrelated patterns, producing erroneous or irrelevant outputs ([[Svenstrup et al.,](#ref-71-4)] [[2015;](#ref-71-4)] [[Hegselmann et al.,](#ref-63-0)] [[2024b)]](#ref-63-0).

[[Wang et al.](#ref-75-3)] [[(2024)]](#ref-75-3) demonstrate that general-purpose LLMs require domain-specific fine-tuning to adapt effectively to clinical tasks. Additionally, retrieval-augmented generation (RAG) techniques, which allow models to access external knowledge dynamically, can help improve performance on unfamiliar cases ([[Lee et al.,](#ref-66-6)] [[2024)]](#ref-66-6).

### <a id="page-19-0"></a>3.2.3 Lack of Medical Reasoning

Effective clinical decision-making relies on reasoning that integrates symptoms, diagnoses, and evidence-based treatments. However, LLMs primarily rely on statistical correlations learned from text rather than causal reasoning ([[Jiang et al.,](#ref-64-6)] [[2023)]](#ref-64-6). As a result, hallucinations occur when models generate outputs that sound plausible but lack logical coherence ([[Glicksberg,](#ref-62-3)] [[2024)]](#ref-62-3). Structured knowledge integration, such as incorporating clinical pathways and causal frameworks into training, has shown potential in improving model reasoning. Similarly, prompting strategies, such as CoT reasoning, can encourage step-by-step output generation ([[Wang and Zhang,](#ref-76-3)] [[2024b)]](#ref-76-3).

## <a id="page-19-1"></a>3.3 Healthcare Domain-Specific Challenges

Unique complexities in the medical domain exacerbate hallucinations in LLMs, such as ambiguity in clinical language, or rapidly evolving nature of medical knowledge.

Medical text often contains ambiguous abbreviations, incomplete sentences, and inconsistent terminology. For example, "BP" could mean "blood pressure" or "biopsy," depending on context ([[Hegselmann et al.,](#ref-63-0)] [[2024b)]](#ref-63-0). Such ambiguities challenge LLMs, leading to misinterpretations and hallucinations. Standardization efforts, such as the adoption of structured vocabularies like SNOMED CT ([[Donnelly et al.,](#ref-60-3)] [[2006)]](#ref-60-3) provide consistent mappings of clinical terminology, reducing ambiguity and improving model reliability.

Furthermore, medical knowledge evolves continuously as new treatments, guidelines, and evidence emerge. Static training datasets quickly become outdated, causing models to generate recommendations that no longer reflect current clinical best practices ([[Shekelle et al.,](#ref-71-3)] [[2002;](#ref-71-3)] [[Restrepo et al.,](#ref-70-4)] [[2024)]](#ref-70-4). To address this, models require regular fine-tuning on updated medical data and integration with dynamic knowledge retrieval systems. Tools capable of real-time evidence synthesis can help ensure outputs remain clinically relevant ([[Wang and Zhang,](#ref-76-4)] [[2024a;](#ref-76-4)] [[Chen et al.,](#ref-58-6)] [[2024)]](#ref-58-6).

These healthcare-specific challenges interact with both data- and model-related issues, creating a multifaceted environment in which hallucinations can arise. Recognizing these contributory factors is critical for designing solutions that systematically address shortcomings in medical LLM development and deployment.

## <a id="page-19-2"></a>4 Detection and Evaluation of Medical Hallucinations

## <a id="page-19-3"></a>4.1 Existing Detection Strategies

We explore several general strategies for hallucination detection in LLMs, alongside some healthcare-specific approaches. Hallucinations in LLMs occur when the model generates outputs that are unsupported by factual knowledge or the input context. Detection methods can be broadly categorized into three groups: 1) factual verification, 2) summary consistency verification, and 3) uncertainty-based hallucination detection. Various benchmarks have been developed to evaluate the effectiveness of these detection strategies, as summarized in Table [[3]](#ref-3).

## <a id="page-20-0"></a>4.1.1 Factual Verification

Factual verification techniques assess whether claims generated by a model are backed by reliable evidence. These methods are critical in domains like healthcare, where hallucinations can lead to significant risks. One approach by [[Chen et al.](#ref-59-4)] [[(2024)]](#ref-59-4) decomposes complex claims into sub-questions, retrieves relevant documents from web sources, and evaluates the truthfulness of each sub-component. By isolating individual facts, this method ensures rigorous verification of multi-faceted medical claims. Another method, FACTSCORE ([[Min et al.,](#ref-67-7)] [[2023)]](#ref-67-7), evaluates factual precision at a granular level, focusing on "atomic facts" rather than entire sentences. This fine-grained approach is especially useful for medical applications, where even small inaccuracies in a diagnosis or recommendation can have serious consequences. FACTSCORE identifies hallucinations embedded within seemingly plausible outputs, making it a useful tool for fact verification in medical LLMs.

### <a id="page-20-1"></a>4.1.2 Summary Consistency Verification

Summary consistency methods evaluate whether a generated summary faithfully reflects the source content. These techniques are crucial for detecting hallucinations, ensuring the summary aligns with the facts present in the input data. These methods can be divided into question-answering (QA)-based and entailment-based approaches. QA-based methods assess consistency by generating questions from either the source or the summary. The first method generates questions from the source text and evaluates the summary's ability to answer them, focusing on recall ([[Scialom et al.,](#ref-71-5)] [[2019)]](#ref-71-5). The second method, QAGS ([[Wang et al.,](#ref-75-4)] [[2020)]](#ref-75-4), generates questions from the summary and compares the answers with the source, detecting factual inconsistencies within the summary. The third method, QuestEval ([[Scialom et al.,](#ref-71-6)] [[2021)]](#ref-71-6), combines both recall and precision by generating questions from both the source and the summary. It also introduces a weighting mechanism for key information, improving the robustness of summary evaluation. Entailment-based methods use natural language inference to determine whether each sentence in the summary is logically entailed by the source. Another approach reranks candidate summaries based on entailment scores, detecting subtle inconsistencies that may not be captured by QA-based methods ([[Falke](#ref-61-1)] [[et al.,](#ref-61-1)] [[2019)]](#ref-61-1). This approach emphasizes logical coherence and is well-suited for identifying hallucinations where facts are misrepresented or distorted. QA-based methods focus on fact recall, while entailment-based methods emphasize logical consistency, providing complementary approaches for hallucination detection.

### <a id="page-21-0"></a>4.1.3 Uncertainty-Based Hallucination Detection

Uncertainty-based hallucination detection assumes that hallucinations occur when a model lacks confidence in its outputs. These methods rely on either sequence log-probability or semantic entropy to quantify uncertainty. Sequence probabilitybased methods detect hallucinations by analyzing the probability assigned to generated sequences. One method ([[Guerreiro et al.,](#ref-62-5)] [[2023)]](#ref-62-5) computes the log-probability of the sequence and flags low-probability outputs as potential hallucinations. Another method ([[Zhang et al.,](#ref-79-2)] [[2023)]](#ref-79-2) refines this by focusing on token-level probabilities and their contextual dependencies, improving hallucination detection by adjusting for overconfidence in certain predictions. Semantic entropy-based methods shift focus to the variability in meaning across different outputs. One method ([[Farquhar et al.,](#ref-61-2)] [[2024)]](#ref-61-2) clusters outputs by semantic meaning rather than surface-level differences, reducing inflated uncertainty caused by rephrasings of the same information. High semantic entropy indicates greater uncertainty and a higher likelihood of hallucination. Another method ([[Hou et al.,](#ref-63-4)] [[2024)]](#ref-63-4) analyzes how the model responds to different versions of the same question, helping to separate uncertainty caused by unclear question phrasings from uncertainty due to the model's own knowledge gaps. For medical LLMs, this helps determine whether the model requires further training on specific clinical concepts or if users need to be more precise in formulating their queries. Together, sequence probability and semantic entropy methods offer complementary approaches for hallucination detection, with sequence log-probabilities providing a general uncertainty measure and semantic entropy focusing on meaning-centered analysis.

## <a id="page-21-1"></a>4.2 Methods for Evaluating Medical Hallucinations

To effectively evaluate and quantify hallucinations in medical LLMs, we propose a systematic framework that aligns with the taxonomy presented in Table [[2]](#ref-2). This framework encompasses multiple measurement approaches, each addressing specific aspects of hallucination detection and evaluation across different healthcare applications. Specific tests designed to detect these hallucinations in clinical contexts are presented in Table [[4]](#ref-4).

## Factual Accuracy Assessment

This fundamental measurement approach directly addresses Factual Hallucinations and Research Hallucinations by comparing LLM outputs against authoritative medical sources. When an LLM generates information that contradicts established medical knowledge, it indicates the model is fabricating content rather than retrieving and applying accurate information. This involves both automated metrics (entity overlap, relation overlap) and expert verification, with particular emphasis on medical entity recognition and relationship validation. For instance, in Drug Discovery applications, this would assess whether drug-protein interactions described by the LLM align with established biochemical knowledge ([[Juhi et al.,](#ref-64-7)] [[2023)]](#ref-64-7).

### Consistency Analysis

This approach employs Natural Language Inference (NLI) and Question-Answer Consistency techniques to detect Decision-Making Hallucinations and Diagnostic Hallucinations in Clinical Decision Support Systems (CDSS) and EHR Management. Internal contradictions in an LLM's response suggest the model is generating information without maintaining a coherent understanding of the medical case, indicating hallucination rather than reasoned analysis ([[Sambara et al.,](#ref-72-4)] [[2024)]](#ref-72-4). Future benchmarks and metrics are recommended to examine logical consistency across medical reasoning chains and evaluates whether treatment recommendations align with provided patient information and clinical guidelines.

### Contextual Relevance Evaluation

This measurement method addresses Context Deviation Issues using n-gram overlap and semantic similarity metrics to assess whether LLM outputs maintain appropriate clinical context. When an LLM's response deviates significantly from the medical query or context provided, it suggests the model is generating content based on spurious associations rather than addressing the specific medical situation at hand. This is especially important in Patient Engagement and Medical Education & Training applications, where responses must align precisely with the specific medical scenario or educational objective under consideration ([[Wen et al.,](#ref-75-5)] [[2024;](#ref-75-5)] [[Aydin et al.,](#ref-56-4)] [[2024)]](#ref-56-4).

### Uncertainty Quantification

This approach uses sequence log-probability and semantic entropy measures to identify potential areas of Clinical Data Fabrication and Procedure Description Errors. High uncertainty in the model's outputs, as indicated by low sequence probabilities or high semantic entropy, suggests the LLM is generating content without strong grounding in its training data, making hallucination more likely. This is particularly crucial in Medical Research Support and Clinical Documentation Automation, where fabricated information can have serious consequences ([[Asgari et al.,](#ref-56-1)] [[2024;](#ref-56-1)] [[Vishwanath et al.,](#ref-75-0)] [[2024)]](#ref-75-0).

### Cross-modal Verification

This measurement technique specifically targets Multimodal Integration Errors by evaluating whether textual descriptions are actually supported by the medical images or data they claim to describe ([[Chen et al.,](#ref-60-0)] [[2024)]](#ref-60-0). When an LLM generates text about medical images that describes features or findings not present in the actual image, this indicates the model is hallucinating content rather than performing accurate interpretation ([[Sambara et al.,](#ref-72-4)] [[2024)]](#ref-72-4). The measurement process involves generating multiple descriptions of the same medical image, then using an evaluator model to compute entailment scores between the generated description and a ground truth imaging report. This approach is particularly critical for applications like Medical Question Answering and Clinical Documentation Automation where LLMs must generate accurate descriptions of medical imaging or laboratory results.

Each measurement approach may require both automated metrics and expert validation, with specific adaptations for medical domain requirements. For example, entity overlap metrics can be enhanced to specifically measure text similarity in medical terminology, procedures, and relationships, while NLI classifiers can be fine-tuned on medical literature and clinical guidelines.

## <a id="page-23-0"></a>4.3 Challenges in Medical Hallucination Detection

One of the fundamental challenges in detecting hallucinations lies in the ambiguity of the term itself, which encompasses diverse errors and lacks a universally accepted definition ([[Huang et al.,](#ref-63-5)] [[2024)]](#ref-63-5). This makes it difficult to standardize benchmarks or evaluate detection methods effectively. Once a consensus on the definitions of hallucinations is established, there remains the issue of evaluating these phenomena effectively. Developing principled metrics aligned with a clear taxonomy of hallucinations is essential for advancing detection approaches. Often,domain-specific solutions tailored to the complex reasoning processes in medical contexts, such as entailment framework specific to radiology report, is useful to evaluate whether generated statements align with input findings ([[Sambara et al.,](#ref-72-4)] [[2024)]](#ref-72-4).

## Lack of a Reliable Ground Truth

A significant obstacle in hallucination detection is the frequent absence of, or the high cost of collecting a reliable ground truth, especially for complex or novel queries. For example, when simulating diagnostic tasks in radiology or summarizing complex patient histories, it is challenging to define what constitutes a hallucination without pre-established labeled examples ([[Hegselmann et al.,](#ref-63-0)] [[2024b)]](#ref-63-0). This gap hinders both the evaluation of detection methods and the supervised training of models for hallucination detection of medical LLMs.

Annotating diagnosis recommendations for real-world medical cases is challenging in part due to Hickam's Dictum ([[Borden and Linklater,](#ref-57-4)] [[2013)]](#ref-57-4), which recognizes that patients can have multiple coexisting conditions. Symptoms often align with various potential diagnoses, making it difficult to confidently determine a comprehensive diagnosis without dedicating significant time to the case. Given time constraints, medical annotation for evaluating AI hallucinations typically limits the time doctors have to assess each AI-generated output. This restriction makes it difficult to distinguish between clear AI hallucinations, or errors, and potentially useful, yet unconventional, diagnoses that may warrant further investigation.

Lastly, some clinical cases exhibit significant disagreement among clinicians, making it difficult to condense them into a single annotation. This problem is exacerbated in highly specialized domains, such as oncology, evidenced by a recent study evaluating ChatGPT's ability to provide cancer treatment recommendations against National Comprehensive Cancer Network (NCCN) guidelines ([[Chen et al.,](#ref-59-5)] [[2023b)]](#ref-59-5). In this work, full agreement among three oncologists occurred in only 61.9% of cases ([[Chen et al.,](#ref-59-5)] [[2023b)]](#ref-59-5), highlighting the inherent complexity of assessing AI-generated medical outputs in specialized domains.

### Semantic Equivalence and Its Role in Detection

Semantic equivalence is the alignment of meaning between two pieces of text, ensuring they convey the same intended message ([[Finch et al.,](#ref-61-3)] [[2005;](#ref-61-3)] [[Pad´o et al.,](#ref-69-2)] [[2009)]](#ref-69-2).

In the context of LLMs, this is used to identify inconsistencies or hallucinations by comparing multiple outputs sampled from the same input for contradictions or selfinconsistencies ([[Farquhar et al.,](#ref-61-2)] [[2024)]](#ref-61-2). Additionally, semantic equivalence can verify whether a model-generated medical report accurately reflects a reference report ([[Sam](#ref-72-4)] [[bara et al.,](#ref-72-4)] [[2024)]](#ref-72-4). In many cases, this is done using bidirectional entailment, a mutual verification process where each text is evaluated to confirm it logically supports and is supported by the other ([[Pad´o et al.,](#ref-69-2)] [[2009;](#ref-69-2)] [[Farquhar et al.,](#ref-61-2)] [[2024)]](#ref-61-2). However, there is a lack of comprehensive testing to determine whether entailment approaches perform effectively in specialized healthcare domains.

## <a id="page-24-0"></a>5 Mitigation Strategies

## <a id="page-24-1"></a>5.1 Data-Centric Approaches

As the capabilities of LLMs continue to evolve, there is a growing emphasis on data-centric approaches to improve their performance and reduce hallucinations. The quality, scope, and diversity of training data are fundamental to building reliable and accurate models, particularly in specialized fields such as biomedicine. This section outlines key strategies for reducing hallucinations through specialized dataset development and data augmentation techniques.

## <a id="page-24-2"></a>5.1.1 Improving Data Quality and Curation

Pretrained LLMs, such as GPT-3 ([[Brown et al.,](#ref-57-5)] [[2020)]](#ref-57-5), GPT-4 ([[OpenAI et al.,](#ref-68-2)] [[2024)]](#ref-68-2), PaLM ([[Chung et al.,](#ref-58-7)] [[2024)]](#ref-58-7), LLaMA ([[Touvron et al.,](#ref-73-4)] [[2023)]](#ref-73-4), and BERT ([[Devlin](#ref-60-4)] [[et al.,](#ref-60-4)] [[2019)]](#ref-60-4), have demonstrated remarkable advancements, largely due to the extensive datasets used in their training. However, achieving high accuracy in biomedical applications requires fine-tuning on domain-specific corpora that are curated for quality, diversity, and task specificity. Models such as Flan-PaLM ([[Chung et al.,](#ref-58-7)] [[2024;](#ref-58-7)] [[Singhal et al.,](#ref-71-7)] [[2023)]](#ref-71-7) show high performance in medical benchmarks, illustrating the potential of targeted pre-training in improving LLM capabilities for complex medical reasoning and text generation. Fine-tuned LLaMA family models for medical tasks also show outstanding capability in the question-answering domain ([[Wu et al.,](#ref-75-6)] [[2024)]](#ref-75-6) and cross-language adaptability ([[Wang et al.,](#ref-75-7)] [[2023)]](#ref-75-7). This progress emphasizes how domain-specific training can significantly improve LLM capabilities in handling advanced medical tasks.

Enhancing data quality and curation is critical for reducing hallucinations, as inaccuracies or inconsistencies in training data can propagate errors in model outputs. To address this, curated datasets have been developed to meet the specific requirements of specialized medical tasks. For example, MEDITRON-70B ([[Chen et al.,](#ref-58-4)] [[2023)]](#ref-58-4) is designed to improve medical reasoning, while MedCPT ([[Jin et al.,](#ref-64-8)] [[2023)]](#ref-64-8) enhances biomedical information retrieval, both of which are based on curated datasets for their respective purposes. These domain-specific datasets enable LLMs to develop a deeper understanding of medical knowledge, ultimately increasing reliability and accuracy.

By leveraging high-quality, well-annotated datasets, models can better align with realworld clinical decision-making and minimize hallucinations that arise from incomplete or misleading information.

## <a id="page-25-0"></a>5.1.2 Augmenting Training Data

Augmenting training data has become important in enhancing the reasoning capabilities of LLMs in medical applications. Augmentation techniques help bridge knowledge gaps, improve generalization, and mitigate biases in LLM-generated outputs. Several LLM-driven solutions have been introduced to enrich training datasets with clinically relevant information. For example, models used in patient-trial matching ([[Yuan](#ref-78-5)] [[et al.,](#ref-78-5)] [[2023)]](#ref-78-5) improve compatibility between electronic health records (EHRs) and clinical trial descriptions, thereby refining model accuracy in real-world clinical settings. Furthermore, models like DALL-M ([[Hsieh et al.,](#ref-63-6)] [[2024)]](#ref-63-6) use a multistep process to generate clinically relevant characteristics by synthesizing data from medical images and text reports, allowing for more personalized healthcare solutions. Another prominent model, GatorTronGPT ([[Peng et al.,](#ref-70-5)] [[2023)]](#ref-70-5), trained on a comprehensive set of clinical data, improves the generation of biomedical text, facilitating the augmentation of medical training data for various tasks and downstream training applications.

## <a id="page-25-1"></a>5.2 Model-Centric Approaches

Model-centric approaches focus on directly improving LLMs through advanced training techniques and post-training modifications. Unlike data-centric methods that enhance the input data, these approaches aim to refine the model's internal representations, reasoning capabilities, and output generation processes. Such methods are crucial in the medical domain, where factual accuracy, reliability, and interpretability are paramount for safe and effective clinical decision-making.

## <a id="page-25-2"></a>5.2.1 Advanced Training Methods

## Preference Learning for Factuality

To better align model outputs and behaviors with human preferences, several methods have been introduced, including direct preference optimization (DPO; [[Rafailov et al.,](#ref-70-6)] [[2024)]](#ref-70-6), reinforcement learning from human feedback (RLHF; [[Ouyang et al.,](#ref-69-3)] [[2022)]](#ref-69-3), and AI feedback (RLAIF; [[Lee et al.,](#ref-66-7)] [[2023)]](#ref-66-7), utilizing techniques like proximal policy optimization (PPO; [[Schulman et al.,](#ref-72-5)] [[2017)]](#ref-72-5) as a training mechanism.

In addition to aligning outputs with human preferences, these methods have been extended to improve factuality by incorporating knowledge-based feedback signals ([[Sun et al.,](#ref-71-8)] [[2023;](#ref-71-8)] [[Tian et al.,](#ref-73-5)] [[2023)]](#ref-73-5). For instance, reinforcement learning from knowledge feedback (RLKF; [[Xu et al.,](#ref-77-2)] [[2024c)]](#ref-77-2) specifically trains models to generate accurate responses or reject questions when outside their knowledge scope, achieving superior factuality compared to decoding strategies or supervised fine-tuning ([[Tian et al.,](#ref-73-5)] [[2023)]](#ref-73-5).

Despite their potential, preference tuning demands a substantial volume of highquality preference labels ([[Lee et al.,](#ref-66-7)] [[2023)]](#ref-66-7), posing a significant challenge for adoption in the medical field due to the high cost of annotations, limited number of expert annotators, and privacy concerns ([[Xia and Yetisgen-Yildiz,](#ref-77-3)] [[2012)]](#ref-77-3). To address this, the use of synthetic data generated by LLMs with clinical knowledge has been proposed. For example, [[Mishra et al.](#ref-68-3)] demonstrate that using synthetic factual edit data from LLMs can effectively guide factual preference learning, resulting in more accurate outputs without the need for extensive human annotations.

### <a id="page-26-0"></a>5.2.2 Post Training Methods

### Model Knowledge Editing

Knowledge editing techniques provide a targeted approach to refining LLM outputs without requiring complete retraining. Unlike continual learning, which updates models through iterative fine-tuning, knowledge editing directly modifies model weights or adds new knowledge parameters ([[Zhang et al.,](#ref-79-3)] [[2024)]](#ref-79-3).. A common approach is to train a model editor, which identifies and applies corrections to internal model representations to produce factually accurate outputs ([[De Cao et al.,](#ref-60-5)] [[2021;](#ref-60-5)] [[Meng et al.,](#ref-67-8)] [[2022)]](#ref-67-8). This method offers efficiency by avoiding costly retraining, but it has significant drawbacks: it can inadvertently degrade model performance on unrelated tasks, struggles with applying multiple simultaneous edits, and often fails with edits that require broader contextual understanding ([[Mitchell et al.,](#ref-68-4)] [[2022)]](#ref-68-4).

Due to the complexity of medical knowledge and the lack of domain-specific benchmarks, knowledge editing has seen limited adoption in healthcare. Alternatively, parameter-efficient approaches add new modules, such as layer-wise adapters ([[Xu](#ref-77-4)] [[et al.,](#ref-77-4)] [[2024a)]](#ref-77-4), instead of altering the base model directly. Such methods are more modular and less disruptive to overall model behavior. This promising framework also propose a domain-specific benchmark, the Medical Counter Fact (MedCF) dataset, to evaluate model edits in medical contexts, to evaluate model edits in medical contexts, demonstrating the effectiveness of targeted model editing in improving factual accuracy without compromising generalization.

### Critic Models

In addition to training an LLM to produce more factual outputs, an auxiliary critic model can be used to critique the model's outputs to re-prompt or edit its generation ([[Pan et al.,](#ref-70-7)] [[2023;](#ref-70-7)] [[Mishra et al.,](#ref-66-8)] [[2024)]](#ref-66-8). Some works use self-refining methods, using the model itself to both critique and refine its own output ([[Madaan et al.,](#ref-68-5)] [[2024;](#ref-68-5)] [[Dhuliawala](#ref-60-6)] [[et al.,](#ref-60-6)] [[2023;](#ref-60-6)] [[Ji et al.,](#ref-64-9)] [[2023)]](#ref-64-9), with the aim of improving the robustness of LLM reasoning processes to reduce hallucination. Although showing some promising results, these methods rely on prompting at each intermediate reasoning step and LLM's reasoning capabilities to correct itself, which can result in unreliable performance gains ([[Huang](#ref-62-6)] [[et al.,](#ref-62-6)] [[2023;](#ref-62-6)] [[Li et al.,](#ref-66-9)] [[2024)]](#ref-66-9).

## <a id="page-26-1"></a>5.3 External Knowledge Integration Techniques

External knowledge integration techniques enhance the capabilities of LLMs by incorporating up-to-date and specialized information from external sources. These approaches are particularly valuable in the medical domain, where timely, accurate, and evidence-based information is crucial for reducing hallucinations and improving decision support.

## <a id="page-27-0"></a>5.3.1 Retrieval-Augmented Generation

Retrieval-augmented generation (RAG) ([[Lewis et al.,](#ref-66-1)] [[2020)]](#ref-66-1) is a prominent method for integrating external knowledge without additional model retraining. The RAG process begins with the retrieval of relevant text and the integration of it into the generation pipeline ([[Asai et al.,](#ref-57-6)] [[2023)]](#ref-57-6), from concatenation to the original input to integration into intermediate Transformer layers ([[Izacard et al.,](#ref-63-7)] [[2023;](#ref-63-7)] [[Borgeaud et al.,](#ref-57-7)] [[2022)]](#ref-57-7) and interpolation of token distributions of retrieved text and generated text ([[Yogatama](#ref-78-6)] [[et al.,](#ref-78-6)] [[2021)]](#ref-78-6).

In medical contexts, RAG has been shown to outperform model-only methods, such as CoT prompting, on complex medical reasoning tasks ([[Xiong et al.,](#ref-76-5)] [[2024a](#ref-76-5)[,?)](#ref-77-5). More importantly, RAG's ability to explicitly cite and ground outputs in retrieved knowledge makes it highly interpretable and controllable—qualities that are particularly valuable in clinical applications ([[Rodriguez et al.,](#ref-70-8)] [[2024)]](#ref-70-8). This has led to its adoption across various medical applications, including patient education ([[Wang et al.,](#ref-75-8)] [[2024)]](#ref-75-8), doctor education ([[Yu et al.,](#ref-78-7)] [[2024)]](#ref-78-7), and clinical decision support ([[Wang et al.,](#ref-75-9)] [[2024)]](#ref-75-9).

Specialized RAG frameworks tailored for healthcare further enhance the accuracy of LLMs by integrating medical-specific corpora and retrievers. For example, MedRAG, a systematic toolkit designed for medical question answering, combines multiple medical datasets with diverse retrieval techniques to improve LLM performance in clinical tasks ([[Xiong et al.,](#ref-76-6)] [[2024b)]](#ref-76-6). Building on this, i-MedRAG (iterative RAG for medicine) introduces an iterative querying process where the model generates followup queries based on prior results. This iterative mechanism enables deeper exploration of complex medical topics, forming multi-step reasoning chains. Experiments show that i-MedRAG outperforms standard RAG approaches on complex questions from the United States Medical Licensing Examination (USMLE) and Massive Multitask Language Understanding (MMLU) datasets ([[Xiong et al.,](#ref-77-5)] [[2024)]](#ref-77-5).

However, RAG techniques face key challenges that limit their effectiveness. The quality of generated responses heavily relies on the relevance and accuracy of retrieved documents. Poor retrieval results can propagate errors into model outputs ([[Xu et al.,](#ref-77-6)] [[2024)]](#ref-77-6). Second, system maintenance overhead, i.e., curating and maintaining up-to-date retrieval corpora, especially for rapidly evolving fields such as medicine, requires significant resources ([[Xiong et al.,](#ref-77-5)] [[2024)]](#ref-77-5). Moreover, integrating misleading information from low-quality sources ([[Koopman and Zuccon,](#ref-65-5)] [[2023)]](#ref-65-5) or conflicting evidence ([[Wan et al.,](#ref-76-7)] [[2024)]](#ref-76-7) can degrade model performance and undermine trust in its outputs. Addressing these challenges requires advancements in retrieval models, knowledge base curation, and filtering mechanisms to ensure only high-quality, verified medical knowledge is incorporated into LLM outputs.

### <a id="page-27-1"></a>5.3.2 Medical Knowledge Graphs

Knowledge graphs (KGs) have been used extensively to encode medical knowledge for LLMs and graph-based algorithms, especially in the medical domain ([[Abu-Salih et al.,](#ref-57-8)] [[2023;](#ref-57-8)] [[Lavrinovics et al.,](#ref-65-6)] [[2024;](#ref-65-6)] [[Yang et al.,](#ref-78-8)] [[2023;](#ref-78-8)] [[Chandak et al.,](#ref-59-6)] [[2023)]](#ref-59-6). By structuring complex medical information into interconnected entities and relationships, KGs facilitate advanced reasoning and provide clear context and provenance [[Shi et al.](#ref-72-6)] [[(2023)]](#ref-72-6), as each fact within the graph is traceable to its source ([[Lavrinovics et al.,](#ref-65-6)] [[2024)]](#ref-65-6) and informative through clear descriptions ([[Chandak et al.,](#ref-59-6)] [[2023)]](#ref-59-6). This traceability is particularly crucial in the medical field, where the accuracy and reliability of information are paramount.

The integration of KGs into LLMs has shown promise in mitigating hallucinations—instances where models generate plausible but incorrect information ([[Lavri](#ref-65-6)] [[novics et al.,](#ref-65-6)] [[2024)]](#ref-65-6). By grounding LLM outputs in the structured and verified data contained within KGs, the likelihood of generating erroneous or fabricated content is reduced in medical diagnosis. For instance, [[De Nicola et al.](#ref-60-7)] [[(2022)]](#ref-60-7) highlight the potential of KGs to enhance diagnostic accuracy by encoding complex medical relationships and facilitating structured reasoning in clinical decision making. Similarly, [[Wang et al.](#ref-75-10)] [[(2022)]](#ref-75-10) demonstrate how KGs can be applied to medical imaging, enabling the integration of multimodal data to reduce diagnostic errors in imaging analysis workflows. [[Yu et al.](#ref-78-9)] [[(2022)]](#ref-78-9) explore how KGs support the management of chronic disease in children, providing actionable insights through data synthesis and predictive analytics. Furthermore, [[Gong et al.](#ref-62-7)] [[(2021)]](#ref-62-7) focus on safe medicine recommendations, utilizing KG embeddings to mitigate risks associated with incorrect prescriptions. This synergy enhances the factual consistency of model outputs, a critical factor in medical applications where misinformation can have serious consequences. Recent studies have explored various methodologies to incorporate KGs into LLM workflows, aiming to improve the factual accuracy of generated content in tasks such as link prediction, rule learning, and downstream polypharmacy ([[Gema et al.,](#ref-62-8)] [[2024)]](#ref-62-8).

## <a id="page-28-0"></a>5.4 Uncertainty Quantification in Medical LLMs

A key dimension of reliability in large language models (LLMs) is their ability to detect and communicate when they are uncertain about a given query or piece of information. In clinical settings, where inaccurate or ungrounded outputs can mislead decision-making, robust mechanisms for uncertainty estimation are critical. When an LLM faces questions exceeding its familiarity or training scope, it ideally should communicate uncertainty or refrain from answering, rather than offering false confidence ([[Li et al.,](#ref-65-1)] [[2024)]](#ref-65-1). By quantifying how confident or uncertain a model is, LLMs can refrain from providing answers when knowledge gaps are significant ([[Kamath et al.,](#ref-65-7)] [[2020;](#ref-65-7)] [[Jiang et al.,](#ref-63-8)] [[2021;](#ref-63-8)] [[Whitehead et al.,](#ref-76-8)] [[2022;](#ref-76-8)] [[Feng et al.,](#ref-61-4)] [[2024)]](#ref-61-4). This section explores contemporary methods for modeling uncertainty, discusses their relevance to medical applications, and highlights the role of multi-LLM collaboration in reducing hallucinations.

## <a id="page-28-1"></a>5.4.1 Methods for Confidence Estimation

Uncertainty in an LLM's output can be represented and managed through various techniques, each addressing different dimensions of reliability.

Model-Level and Training-Based Approaches. Certain strategies integrate uncertainty estimation directly into the training process. For example, methods that introduce probabilistic layers or specialized loss functions can encourage models to produce calibrated confidence measures, rather than treating every prediction with equal certainty ([[Kamath et al.,](#ref-65-7)] [[2020;](#ref-65-7)] [[Jiang et al.,](#ref-63-8)] [[2021)]](#ref-63-8). Additionally, targeted knowledge integration during pretraining can reduce blind spots, although maintaining up-to-date domain coverage remains an ongoing challenge ([[Feng et al.,](#ref-61-4)] [[2024)]](#ref-61-4).

Prompting and Post-Hoc Calibration. Another class of methods focuses on refining uncertainty estimates after the initial model output. Prompt-based strategies encourage the LLM to self-assess its confidence, while post-hoc calibration techniques, such as temperature scaling or external calibrators, adjust logits or embedding representations ([[Whitehead et al.,](#ref-76-8)] [[2022;](#ref-76-8)] [[Xie et al.,](#ref-77-7)] [[2024;](#ref-77-7)] [[Tian et al.,](#ref-73-6)] [[2023)]](#ref-73-6). Empirical findings indicate that such techniques can improve reliability in medical diagnosis tasks ([[Savage et al.,](#ref-72-7)] [[2024;](#ref-72-7)] [[Gao et al.,](#ref-62-9)] [[2024)]](#ref-62-9), though larger models are not always better calibrated ([[Desai and Durrett,](#ref-60-8)] [[2020;](#ref-60-8)] [[Srivastava et al.,](#ref-71-9)] [[2022;](#ref-71-9)] [[Geng et al.,](#ref-61-5)] [[2023)]](#ref-61-5).

Multi-LLM Collaboration. Relying solely on a single LLM for self-correction can be risky if the model has learned skewed or incomplete patterns ([[Kadavath et al.,](#ref-64-10)] [[2022;](#ref-64-10)] [[Ji et al.,](#ref-64-3)] [[2023b;](#ref-64-3)] [[Xie et al.,](#ref-77-8)] [[2023)]](#ref-77-8). Multi-LLM collaboration attempts to reduce individual model biases by cross-verifying reasoning processes and outcomes. Voting or consensus-based approaches harness diverse model knowledge, mitigating hallucinations and overconfidence by highlighting discrepancies across peers ([[Yu et al.,](#ref-78-10)] [[2023;](#ref-78-10)] [[Du et al.,](#ref-60-9)] [[2023;](#ref-60-9)] [[Bansal et al.,](#ref-58-8)] [[2024;](#ref-58-8)] [[Feng et al.,](#ref-61-6)] [[2024)]](#ref-61-6).

Structured Uncertainty Sets. In some instances, abstaining entirely may omit potentially valid insights, especially when a model has partial confidence. Techniques like conformal prediction strike a balance between outright abstention and blind certainty by providing sets of plausible answers with quantifiable error guarantees ([[Angelopoulos and Bates,](#ref-56-5)] [[2022;](#ref-56-5)] [[Mohri and Hashimoto,](#ref-67-9)] [[2024)]](#ref-67-9). Such methods let clinicians consider multiple options, each accompanied by a measure of confidence, rather than a single deterministic (and potentially incorrect) recommendation.

In high-stakes medical scenarios, reliably assessing uncertainty is paramount to preventing harmful outcomes. Models are often tasked with diagnosing critical conditions based on limited or ambiguous information. Direct prompts for confidence scores can help identify when the model is overstepping its reliable scope ([[Tian et al.,](#ref-73-6)] [[2023;](#ref-73-6)] [[Yang et al.,](#ref-78-11)] [[2024)]](#ref-78-11), but further refinements are frequently required.

Low-Resource Specialties as Illustrative Cases. Some medical subfields, such as certain aspects of women's health, suffer from limited training data and rapidly evolving guidelines ([[Kim,](#ref-65-8)] [[2024)]](#ref-65-8). While AI-driven tools can enhance patient education and self-care behaviors in these contexts, inaccuracies pose serious risks. Systems must therefore not only provide answers but also quantify and communicate any underlying uncertainties, improving the likelihood that clinicians and patients will seek validation for potentially flawed outputs ([[Wen et al.,](#ref-76-9)] [[2024;](#ref-76-9)] [[Tjandra et al.,](#ref-73-7)] [[2024)]](#ref-73-7).

Abstention and Deliberation. When models generate multiple hypotheses without a single decisive answer, abstention thresholding allows them to refrain from giving conclusive guidance ([[Geng et al.,](#ref-61-7)] [[2024;](#ref-61-7)] [[Steyvers et al.,](#ref-72-8)] [[2024)]](#ref-72-8) and instead guiding them to ask additional questions ([[Li et al.,](#ref-65-1)] [[2024)]](#ref-65-1). In some cases, multi-step or multiagent deliberation can further refine uncertainty estimates, prompting the LLM to re-check facts or invite additional input ([[Kadavath et al.,](#ref-64-10)] [[2022;](#ref-64-10)] [[Xie et al.,](#ref-77-8)] [[2023)]](#ref-77-8). Such approaches reduce the risk of passing on guesswork as definitive advice, a particular concern in time-sensitive medical scenarios.

Empirical Insights from Clinical Settings. Recent work by [[Rodman et al.](#ref-70-9)] [[(2023)]](#ref-70-9) demonstrated that GPT-4 can sometimes surpass clinicians in estimating disease likelihoods, yet both the model and human experts deviated substantially from actual prevalence rates. Meanwhile, exploration in embodied agents like Voyager ([[Wang et al.,](#ref-76-10)] [[2023)]](#ref-76-10) shows that advanced LLM frameworks often lack robust uncertainty quantification—even outside the medical domain. These findings underscore the broader relevance of uncertainty estimation: without systematic calibration, confident but unfounded responses can overshadow the potential benefits of AI in healthcare.

By designing models that effectively convey when they are uncertain—whether via post-hoc calibration, structured confidence sets, or consensus-driven deliberation—practitioners can better interpret and validate AI outputs. Such strategies are crucial for minimizing risk in clinical diagnostics, where the cost of error can be immediate and severe.

## <a id="page-30-0"></a>5.4.2 Confidence Estimation in High-Stakes Applications

## <a id="page-30-1"></a>5.5 Prompt Engineering Strategies

Recent advances in medical LLM applications have demonstrated several prompting strategies for hallucination mitigation, each employing distinct cognitive frameworks to enhance diagnostic reliability. The chain-of-medical-thought (CoMT) ([[Jiang](#ref-64-0)] [[et al.,](#ref-64-0)] [[2024)]](#ref-64-0) approach restructures medical report generation by decomposing radiological analysis into sequential clinical reasoning steps. Implemented for chest X-ray and CT scan interpretation, this method prompts models to first identify anatomical structures ("Observe lung fields for opacities"), then analyze pathological indicators ("Assess bronchial wall thickening patterns"), and finally synthesize diagnostic conclusions ("Correlate findings with clinical history of chronic obstructive pulmonary disease"). By mirroring radiologists' diagnostic workflows through structured prompt templates, CoMT reduced catastrophic hallucinations by 38% compared to conventional report generation methods, as measured through the MediHall Score metric evaluating disease omission/fabrication rates.

The interactive self-reflection methodology introduces a recursive prompting architecture for medical question answering systems ([[Ji et al.,](#ref-64-9)] [[2023)]](#ref-64-9). When deployed in clinical decision support scenarios, this approach initiates with a knowledge acquisition prompt ("Generate relevant biomedical concepts for: {patient presentation}"), followed by iterative fact-checking queries ("Verify consistency between {generated concept} and current medical guidelines"). For a case study involving rare disease diagnosis, this multi-turn prompting strategy improved answer entailment scores by 27% across five LLM architectures by forcing models to reconcile generated content with internal knowledge representations through prompts like "Revise previous diagnosis considering [contradictory finding]". Human evaluations showed this reflection loop reduced critical hallucinations (misclassified disease types) by 41% in pediatric oncology use cases.

Semantic prompt enrichment ([[Penkov,](#ref-70-10)] [[2024)]](#ref-70-10) combines biomedical entity recognition with ontological grounding to constrain LLM outputs. Through integration of BioBERT for clinical concept extraction and ChEBI for chemical ontology

## <a id="page-31-0"></a>Chain-of-Medical-Thought (CoMT) in Medical Report Generation.

![That's a posteroanterior chest radiograph. The image shows a patient's chest X-ray, displaying lung fields with diffuse opacities consistent with pulmonary pathology. A white arrow likely points to a specific area of interest relevant to the paper's diagnosis or findings concerning a respiratory condition. The image serves as a visual representation of the patient's clinical presentation supporting the paper's case study or analysis of a respiratory disease.](_page_31_Picture_2.jpeg)

Medical Report: AP and lateral views of the chest were provided in the X-ray. Lung volumes are low. There are findings consistent with chronic lung disease such as sarcoidosis. Prominence of the pulmonary interstitial markings is due to mild heart failure. There is no pleural effusion or pneumothorax. The size of the heart is normal. The cardiomediastinal silhouette is notable for a tortuous aorta. Bones are slightly osteopenic. The impression suggests that 1. Improving right upper lobe consolidation; 2. Mild heart failure; 3. Findings of chronic lung disease, most likely sarcoidosis.

### Construction of Hierarchical QA pair

Q1: What modality is used to take this image?

A1: The modality used for this image is an x-ray.

Q2: What organs are in the image?

A2: The x-ray image depicts the heart and lungs.

Q3: Describe the size of the organ in the image.

A3: The size of the heart is normal. Lung volumes are low.

Q4: Where are the abnormalities in the organs? A4: Right upper lobe consolidation

Q5: What symptoms are shown in this image? A5: Prominence of the pulmonary interstitial markings. . . . .

Q6: Describe the patient's health condition according to this image. A6: The overall impression from the x-ray is. . .

### Chain-based QA Pair Refactoring

Q1: What modality is used to take this image?

Q2: The modality used for this image is an xray. So, What organs are in the image?

Q3: The modality. . . The x-ray image depicts ... The size of the . . . . So, Where are the abnormalities in the organs?

Q4: The modality. . . The x-ray image... The size. . . . Image shows right upper lobe consolidation. So, what symptoms are shown in this image?

Q5: The modality. . . The x-ray image... The size. . . . Image shows right upper lobe consolidation. The image shows prominence of . . . . Describe the patient's health condition according to this image. 32

### High Quality Report

The findings are... The impression suggests... In summary...

**Figure 3:** Illustration of CoMT's process for constructing hierarchical QA pairs based on real clinical image reports. This example is from the original paper [[Jiang](#ref-64-0)] et al. [[(2024)]](#ref-64-0).

alignment, this strategy appends verified domain knowledge directly to prompts. A representative implementation for drug interaction queries structures prompts as: "Using ChEBI identifiers [CHEBI:48607=ibuprofen] and [CHEBI:35475=warfarin], describe metabolic pathway interactions considering CYP2C9 polymorphism risks". When applied to pharmacological report generation, this method reduced attribute hallucinations (incorrect dosage/formulation details) by 33% compared to baseline prompts, while maintaining 92% terminological consistency with FDA drug labeling databases. The technique demonstrates particular efficacy in oncology applications where precise molecular descriptor usage is critical - staging reports showed 29% fewer TNM classification errors when ontology-enriched prompts specified histological grading criteria.

Chain-of-Knowledge (CoK) ([[Li et al.,](#ref-66-0)] [[2024)]](#ref-66-0) is a framework that dynamically incorporates domain knowledge from diverse sources to enhance the facutal correctness of LLMs. CoK generates an initial rationale while identifying relevant knowledge domains, and dynamically refines the rationale with knowledge from the identified domains to provide more factually correct responses. The authors evaluate CoK across various domain-specific datasets, including medical, physical, and biological fields, demonstrating an average improvement of 4.9% in accuracy compared to the Chainof-Thought (CoT) baseline. To further validate the framework's impact on reducing hallucinations, they present evidence of enhanced factual accuracy on single- and multi-step reasoning tasks using ProgramFC, a factual verification method based on Wikipedia. Additionally, human evaluations corroborate these findings, confirming that CoK consistently yields more accurate responses than the CoT baseline.

## <a id="page-32-0"></a>6 Experiments on Medical Hallucination Benchmark

## <a id="page-32-1"></a>6.1 Setup

We conducted a series of experiments to evaluate the effectiveness of various hallucination mitigation techniques on Large Language Models (LLMs) using the Med-HALT benchmark ([[Pal et al.,](#ref-70-0)] [[2023)]](#ref-70-0). We compared the performance of several LLMs across different prompting strategies and retrieval-augmented methods. Our evaluation pipeline used UMLSBERT ([[Michalopoulos et al.,](#ref-68-6)] [[2020)]](#ref-68-6), a specialized medical text embedding model, to assess the semantic similarity between generated responses and the ground truth medical information. The following methods were implemented:

Base: This method served as our baseline. LLMs were directly queried with the questions from the Med-HALT benchmark without any additional context or instructions. This approach allows us to assess the inherent hallucination tendencies of the LLMs in a zero-shot setting. The prompt consisted solely of the medical question.

System Prompt: We prepended a system prompt to the user's question. These system prompts were designed to guide the LLM towards providing accurate and reliable medical information, explicitly discouraging the generation of fabricated content. Examples of system prompts included instructions to act as a knowledgeable medical expert and to avoid making assumptions. However, it's important to note that research ([[Zheng et al.,](#ref-79-4)] [[2024)]](#ref-79-4) has questioned the consistent effectiveness of personas and system prompts in improving LLM performance on objective tasks. While our prompts

## <a id="page-33-0"></a>Prompt Examples for Each Step of Chain-of-Knowledge (CoK)

### REASONING GENERATION

Q: This British racing driver came in third at the 2014 Bahrain GP2 Series round and was born in what year

A: First, at the 2014 Bahrain GP2 Series round, DAMS driver Jolyon Palmer came in third. Second, Jolyon Palmer (born 20 January 1991) is a British racing driver. The answer is 1991.

Q: [Question] A:

### KNOWLEDGE DOMAIN SELECTION

Follow the below example, select relevant knowledge domains from Available Domains to the Q. Available Domains: factual, medical, physical, biology

Q: This British racing driver came in third at the 2014 Bahrain GP2 Series round and was born in what year

Relevant domains: factual

Q: Which of the following drugs can be given in renal failure safely? Relevant domains: medical

Q: [Question] Relevant domains:

### RATIONALE CORRECTION

Strictly follow the format of the below examples. The given sentence may have factual errors, please correct them based on the given external knowledge. Sentence: the Alpher-Bethe-Gamow paper was invented by Ralph Alpher. Knowledge: discoverer or inventor of Alpher-Bethe-Famow paper is Ralph Alpher. Edited sentence: the Alpher-Bethe-Gamow paper was invented by Ralph Alpher Sentence: [Ratioanle] Knowledge: [Knowledge]

Edited sentence:

### ANSWER CONSOLIDATION

Q: This British racing driver came in third at the 2014 Bahrain GP2 Series round and was born in what year

A: First, at the 2014 Bahrain GP2 Series round, DAMS driver Jolyon Palmer came in third. Second, Jolyon Palmer (born 20 January 1991) is a British racing driver. The answer is 1991.

Q: [Question]

A: First, [Corrected first rationale]. Second, [Corrected second rationale]. The answer is

**Figure 4:** Prompt examples for each step of the Chain-of-Knowledge framework. This example is from the original paper Li et [[al.](#ref-66-0)] [[(2024)]](#ref-66-0).

aimed to enhance reliability, studies suggest that the impact of such prompts, particularly those relying on personas, might be variable and not always lead to significant performance gains.

CoT: We implemented Chain-of-Thought (CoT) prompting by appending the phrase "Let's think step by step." to each question. This encourages the LLM to articulate its reasoning process explicitly, which can improve accuracy by facilitating the identification and correction of errors during the generation process. This aligns with the principle of eliciting explicit reasoning steps from LLMs to enhance performance on complex tasks ([[Wei et al.,](#ref-76-2)] [[2022)]](#ref-76-2). Furthermore, the generation of natural language explanations, as explored in work like e-SNLI ([[Camburu et al.,](#ref-59-7)] [[2018)]](#ref-59-7), is related to CoT in its aim to make the model's reasoning more transparent and potentially improve its factual correctness. This encourages the LLM to articulate its reasoning process explicitly, which can improve accuracy by facilitating the identification and correction of errors during the generation process.

RAG: We employed MedRAG ([[Xiong et al.,](#ref-76-5)] [[2024a)]](#ref-76-5), a retrieval-augmented generation model specifically designed for the medical domain. MedRAG utilizes a knowledge graph (KG) to enhance reasoning capabilities. For each Med-HALT question, we used MedRAG to retrieve relevant medical knowledge from the KG. This retrieved knowledge was then concatenated with the original question and provided as input to the LLM. This allows the LLM to generate responses grounded in external, validated medical information. We adapted publicly available MedRAG code and its associated KG for this implementation.

Internet Search: This approach leverages real-time internet search to provide LLMs with up-to-date information. We utilized the SerpAPIWrapper from langchain to perform Google searches.

## <a id="page-34-0"></a>6.2 Dataset & Tasks

We utilized the Medical Domain Hallucination Test (Med-HALT) benchmark ([[Pal](#ref-70-0)] [[et al.,](#ref-70-0)] [[2023)]](#ref-70-0) that has been specifically designed to assess and quantify hallucinations in LLMs within the medical domain. The Med-HALT benchmark employs a two-tiered approach, categorizing hallucination tests into:

*   Reasoning Hallucination Tests (RHTs): These tests evaluate an LLM's ability to reason accurately with medical information and generate logically sound and factually correct outputs without fabricating information. RHTs are further divided into:
    *   False Confidence Test (FCT): Assesses if a model can evaluate the validity of a randomly suggested "correct" answer to a medical question, requiring it to discern correctness and provide detailed justifications, highlighting its ability to avoid unwarranted certainty.
    *   None of the Above (NOTA) Test: Challenges models to identify when none of the provided multiple-choice options are correct, requiring them to recognize irrelevant or incorrect information and justify the "None of the Above" selection.

![The image is simply the number "35". Without further context from the paper, its purpose cannot be determined, but it likely serves as a figure reference, equation number, or page number.](_page_34_Picture_10.jpeg)

*   Fake Questions Test (FQT): Examines a model's ability to identify and appropriately handle nonsensical or artificially generated medical questions, testing its capacity to discern legitimate queries from fabricated ones.
*   Memory Hallucination Tests (MHTs): These tests focus on evaluating an LLM's ability to accurately recall and retrieve factual biomedical information from its training data. MHTs include tasks such as:
    *   Abstract-to-Link Test: Models are given a PubMed abstract and tasked with generating the corresponding PubMed URL.
    *   PMID-to-Title Test: Models are provided with a PubMed ID (PMID) and asked to generate the correct article title.
    *   Title-to-Link Test: Models are given a PubMed article title and prompted to provide the PubMed URL.
    *   Link-to-Title Test: Models are given a PubMed URL and asked to generate the corresponding article title.

By incorporating these diverse tasks, Med-HALT provides a comprehensive framework to evaluate the multifaceted nature of medical hallucinations in LLMs, assessing both reasoning and memory-related inaccuracies.

## <a id="page-35-0"></a>6.3 Metrics

## Hallucination Pointwise Score

The Pointwise Score used in Med-HALT ([[Pal et al.,](#ref-70-0)] [[2023)]](#ref-70-0) is designed to provide an in-depth evaluation of model performance, considering both correct answers and incorrect ones with a penalty. It is calculated as the average score across the samples, where each correct prediction is awarded a positive score (P^c^ = +1) and each incorrect prediction incurs a negative penalty (P^w^ = −0.25). The formula for the Pointwise Score (S) is given by:

$$
S = \frac{1}{N} \sum_{i=1}^{N} (\mathbb{I}(y_i = \hat{y}_i) \cdot P_c + \mathbb{I}(y_i \neq \hat{y}_i) \cdot P_w)
$$
(1)

where:

*   S is the final Pointwise Score.
*   N is the total number of samples.
*   y^i^ is the true label for the i-th sample.
*   y^i^ is the predicted label for the i-th sample.
*   I(condition) is the indicator function, which returns 1 if the condition is true and 0 otherwise.
*   P^c^ = 1 is the points awarded for a correct prediction.
*   P^w^ = −0.25 is the points deducted for an incorrect prediction.

### Similarity Score

The Similarity Score assesses the semantic similarity between the model's generated responses and the ground truth correct answer, as well as the similarity between the response and the original question. This is achieved using UMLSBERT, a specialized medical text embedding model, and cosine similarity. The process is as follows:

*   1. Embedding Generation with UMLSBERT: For each question in the Med-HALT benchmark, and for each type of model output (Base, System Prompt, CoT, MedRAG, Internet Search), the following texts are encoded into embeddings using UMLSBERT:
    *   The original medical question.
    *   The correct option (ground truth answer).
    *   The model's generated output for each method.
*   2. Cosine Similarity Calculation: After obtaining the embeddings, the cosine similarity is calculated for each model output against two references:
    *   Answer Similarity: The cosine similarity between the embedding of the correct option and the embedding of the model's output. This measures how semantically similar the generated response is to the ground truth answer.
    *   Question Similarity: The cosine similarity between the embedding of the original question and the embedding of the model's output. This evaluates how much the generated response is semantically related to the input question itself.
*   3. Combined Similarity Score: A combined score is then computed as the average of the answer similarity and the question similarity:

$$
Combined Score = \frac{Answer Similarity + Question Similarity}{2}
$$

## <a id="page-36-0"></a>6.4 Models

To assess medical hallucinations comprehensively, we evaluated a diverse set of foundation models, selected to represent a range of architectures, training paradigms, and domain specializations. Our selection included both general-purpose models, which represent the forefront of broadly applicable LLM technology, and medical-purpose models, designed or fine-tuned specifically for healthcare applications. This approach allowed us to compare hallucination tendencies across models with varying levels of domain expertise and general reasoning capabilities.

## General-Purpose LLMs

These models are trained on extensive datasets encompassing general text and code, designed for broad applicability across diverse tasks. Their inclusion helps establish a baseline for hallucination performance and assesses how well general reasoning capabilities translate to the medical domain. Within this category are models from OpenAI and Google. OpenAI Models include o3-mini and o1-preview, introduced in January 2025 and September 2024 respectively and designed to spend more time "thinking" before responding, enhancing reasoning capabilities for complex tasks like science, coding, and mathematics. Also included are GPT-4o and GPT-4o-mini, released in May and July 2024 respectively. GPT-4o is a multimodal model capable of processing and generating text, images, and audio, offering enhanced reasoning and factual accuracy, while GPT-4o-mini is a smaller, more cost-effective version that maintains strong performance with greater efficiency. Google Gemini Models feature Gemini 2.0 Thinking and Gemini 2.0 Flash, launched in Febuary 2025 and December 2024 respectively, designed for enhanced reasoning and efficient, cost-effective performance with multimodal input support. Gemini 1.5 Flash, released in May 2024, is optimized for speed and efficiency, offering low latency and enhanced performance.

### Medical-Purpose LLMs

These models are specifically adapted or trained for medical or biomedical tasks. Their inclusion is crucial for understanding whether domain-specific training or fine-tuning effectively reduces medical hallucinations compared to general-purpose models. This category includes PMC-LLaMA and Alpaca Variants. PMC-LLaMA is a model fine-tuned from LLaMA on PubMed Central (PMC), a free archive of biomedical and life sciences literature. It is designed to enhance performance in medical question answering and knowledge retrieval by leveraging a large corpus of medical research papers. Alpaca Variants include AlphaCare-13B, an Alpaca style Llama based model further finetuned on a medical question-answering dataset, aiming to improve clinical reasoning and dialogue capabilities. MedAlpaca-13B is another Alpaca style Llama based model, fine-tuned on a combination of medical datasets, including medical question-answering and clinical text, designed to perform well on a range of medical NLP tasks.

## <a id="page-37-0"></a>6.5 Results

## Advanced Reasoning Models Maintain Hallucination Resistance Leadership

Our experimental results, visualized in Figure [[5]](#ref-5), reinforce the trend of advanced reasoning models excelling in hallucination prevention. Notably, gemini-2.0-thinking emerges as a top performer, exhibiting the highest hallucination resistance among the models tested, especially when augmented with Search. gemini-2.0 and deepseek-r1 also demonstrate robust hallucination resistance, positioning themselves alongside o1-preview and outperforming earlier models. This sustained superiority of generalpurpose models emphasizes that cutting-edge advancements in broad language understanding are directly contributing to enhanced reliability in specialized domains like medicine.

## CoT Remains a Consistently Effective Strategy, with System Prompting Providing Complementary Gains

Re-examining the impact of prompting strategies, CoT continues to be a highly effective technique across various models for mitigating hallucinations. The plot further reveals that System Prompting also offers noticeable improvements, often working synergistically with CoT to further reduce hallucination rates, particularly in models like o3-mini and deepSeek-r1. These findings underscore the importance of guiding model reasoning through explicit steps (CoT) and providing clear instructions for reliable output generation (System Prompt) to enhance factual accuracy in medical contexts.

<a id="page-38-0"></a>![The figure presents a comparative analysis of large language models (LLMs). (a) is a bar chart showing hallucination scores for several LLMs across different prompting methods (base, system prompt, chain-of-thought, MedRAG, search). (b) is a scatter plot displaying the relationship between hallucination scores and a "similarity score" (not defined) for the same LLMs. Models are categorized as "medical-purpose" or "general-purpose." The plots aim to evaluate the performance and characteristics of various LLMs in terms of factual accuracy and similarity to a reference.](_page_38_Figure_1.jpeg)

**Figure 5:** Hallucination Pointwise Score vs. Similarity Score of LLMs on the Med-Halt hallucination benchmark. This result reveals that the recent models (e.g. o3-mini, deepseek-r1, and gemini-2.0-flash) typically start with high baseline hallucination resistance and tend to see moderate but consistent gains from a simple CoT, while previous models including medical-purpose LLMs often begin at low hallucination resistance yet can benefit from different approaches (e.g. Search, CoT, and System Prompt). Moreover, retrieval-augmented generation can be less effective if the model struggles to reconcile retrieved information with its internal knowledge.

## Similarity Scores Strongly Correlate with Hallucination Resistance, Differentiating Model Performance Tiers

The analysis of similarity scores in Figure 5 reveals a clear stratification of models. The highest-performing models such as gemini-2.0-thinking, gemini-2.0, and deepseek-r1 cluster in the high similarity range (0.7-0.9), indicating a strong semantic alignment of their outputs with ground truth medical information. In contrast, medical-specific models (pmc-llama, medalpaca, alpacare) consistently exhibit lower similarity scores (0.1-0.4) alongside higher hallucination rates. This robust correlation between semantic similarity and hallucination resistance reinforces the notion that a deeper understanding of medical concepts, as reflected in higher similarity scores, is a critical factor in minimizing factual errors in LLM-generated medical content.

## Domain-Specific Training Still Shows Limitations Compared to Advanced General Capabilities

The updated results further highlight the previously observed limitations of domainspecific models. Despite being trained on medical data, models like pmc-llama and medalpaca continue to exhibit significantly higher hallucination rates (around 60%) and lower similarity scores compared to advanced general-purpose models. This persistent trend suggests that while domain-specific data is valuable, the broader language understanding and reasoning capabilities developed in state-of-the-art general models are arguably more crucial for achieving high reliability in complex medical tasks. The superior performance of models like deepseek-r1 and o3-mini, which are not explicitly medical-focused but possess strong general language capabilities, further supports this observation.

## Search-Augmented Generation Shows Nuanced Impact

The effectiveness of search-augmented generation presents a more nuanced picture with the inclusion of newer models. While the trend of diminishing returns for search augmentation in advanced models remains generally true, gemini-2.0-thinking demonstrates a notable benefit from search, achieving the lowest hallucination score with this method. This suggests that even the most capable models can still leverage external, up-to-date information to further refine their responses and minimize hallucinations, particularly when dealing with rapidly evolving medical knowledge. However, for models like deepseek-r1 and o3-mini, the gain from search augmentation appears less pronounced, reinforcing the overall trend that highly advanced architectures are increasingly relying on their internal knowledge base for accuracy.

## <a id="page-39-0"></a>7 Annotations of Medical Hallucination with Clinical Case Records

To rigorously evaluate the presence and nature of hallucinations in LLMs within the clinical domain, we employed a structured annotation process. We built upon established frameworks for hallucination and risk assessment, drawing specifically from the hallucination typology proposed by [[Hegselmann et al.](#ref-63-0)] [[(2024b)]](#ref-63-0) and the risk level

<a id="page-40-2"></a>![This flowchart depicts a process for evaluating Large Language Model (LLM) performance in medical diagnosis using NEJM case records. The LLM parses case information (presentation, diagnosis, etc.), then performs inference tests (chronological ordering, lab data understanding, diagnosis prediction). Human physicians annotate the LLM's output, classifying hallucination types (e.g., condition unsupported) and risk levels (minor, major, etc.). The flowchart also includes example case record data and emergency department findings.](_page_40_Figure_1.jpeg)

**Figure 6:** An annotation process of medical hallucinations in LLMs (Section [[7)]](#ref-7)). We utilize New England Journal of Medicine (NEJM) case records, parsing them into key elements, and feeds them into the LLM for response generation. Physicians then annotate LLM-generated responses to identify medical hallucinations and potential risks, as exemplified by the inaccurate reporting of 'irregular pulse' in the patient's Emergency Department findings.

framework from [[Asgari et al.](#ref-56-1)] [[(2024)]](#ref-56-1) (Figure [[6)]](#ref-6)) and used the New England Journal of Medicine (NEJM) Case Reports for LLM inferences.

## <a id="page-40-0"></a>7.1 Annotation Tasks for Detecting Medical Hallucination

We utilized the three representative evaluation tests outlined in Table [[4]](#ref-4) to probe LLMs for weaknesses in consistency, factual accuracy, and their ability to navigate the complexities and ambiguities inherent in clinical information (Figure [[6)]](#ref-6)). These tests were designed to elicit different types of potential hallucinations. When hallucinations occur, they can manifest in various forms, such as incorrect diagnoses, the use of confusing or inappropriate medical terminology, or the presentation of contradictory findings within a patient's case.

Seven experienced annotators, each holding an MD degree or equivalent clinical expertise (including a geriatrician and an otolaryngologist), independently evaluated the generated outputs for each medical case record. Annotators were tasked with identifying and categorizing any hallucinations according to the types in Table [[6]](#ref-6) and assigning a corresponding risk level based on the definitions in Table [[7]](#ref-7). This rigorous annotation process allowed us to gain a granular understanding of the types and severity of hallucinations produced by LLMs in the medical domain.

## <a id="page-40-1"></a>7.2 Dataset: The New England Journal of Medicine Case Reports

To evaluate the hallucination of LLMs, we used case records of the Massachusetts General Hospital, published in The New England Journal of Medicine (NEJM)

([[Brinkmann et al.,](#ref-58-1)] [[2024)]](#ref-58-1). We focused on the "Case Records of the Massachusetts General Hospital" series, filtering for Clinical Cases published between November 2000 and November 2018 to exclude cases related to the COVID-19 pandemic. This selection aimed to provide a representative sample of diverse medical conditions encountered in a major academic medical center. Leveraging NEJM's categorization of medical specialties, we curated a dataset of 20 case reports, ensuring representation across a wide range of clinical areas. Each case was chosen to highlight certain challenges for the LLMs, e.g., complex differential diagnosis, detailed lab results. The distribution of cases across specialties, as defined by NEJM, is as follows (with the number of cases in the broader NEJM corpus for context):

<a id="page-41-0"></a>![The image is a horizontal bar chart showing the percentage distribution of publications across various medical specialties. The y-axis lists the specialties (e.g., Clinical Medicine, Hematology/Oncology), and the x-axis represents the percentage of publications in each specialty. The bar lengths are proportional to the percentage, with Clinical Medicine having the highest percentage (17.70%). The chart visually displays the relative prevalence of research output within different medical fields.](_page_41_Figure_2.jpeg)

**Figure 7:** Distribution of medical specialties in sampled NEJM Case Records. The figure illustrates the relative frequency of different medical domains, highlighting the predominant focus on clinical medicine, hematology/oncology, and pulmonary/ critical care. The bar colors represent the proportion of cases within each specialty, revealing disparities in case representation across different fields.

Our smaller set of 20 cases sought to reflect this distribution, though not perfectly proportionally, to ensure coverage of common and less-frequent conditions.

## <a id="page-42-0"></a>7.3 Qualitative Evaluation of Clinical Reasoning Tasks Using NEJM Case Reports

To qualitatively assess the LLM's clinical reasoning abilities, we designed three targeted tasks, each focusing on a crucial aspect of medical problem-solving: 1) chronological ordering of events, 2) lab data interpretation, and 3) differential diagnosis generation. These tasks were designed to mimic essential steps in clinical practice, from understanding the patient's history to formulating a diagnosis.

## Chronological Ordering Test

We first evaluated the LLM's ability to sequence clinical events, a cornerstone of medical history taking and understanding disease trajectories. For this Chronological Ordering Test, we prompted the LLM with the question: "Order the key events chronologically and identify temporal relationships between symptoms and interventions." Our results indicate that while the generated chronological ordering by the LLM was generally correct, it missed several important landmark events of the patient. For instance, in the case of opioid use disorder ([[Walley et al.,](#ref-76-11)] [[2019)]](#ref-76-11), crucial details regarding the patient's history of oxycodone and cocaine use were absent from the generated timeline. These omissions are clinically significant as they provide context for the patient's presentation. Furthermore, in the coronary artery dissection case ([[Tsiaras](#ref-73-8)] [[et al.,](#ref-73-8)] [[2017)]](#ref-73-8), key treatment details, such as the administration of isosorbide mononitrate, were omitted. Precise temporal markers, such as specific dates for key events like hospital admission in the adenocarcinoma patient case ([[Murphy et al.,](#ref-68-7)] [[2018)]](#ref-68-7), were also lacking. Lastly, we observed in ([[Murphy et al.,](#ref-68-7)] [[2018)]](#ref-68-7) that the LLM struggled to group concurrent events, incorrectly treating them as separate, sequential occurrences.

### Lab Test Understanding Test

Next, we stress-tested the LLM's capacity to interpret laboratory test results and, critically, to explain their clinical significance in relation to the patient's symptoms. For this Lab Data Understanding Test, we used the prompt: "Analyze the laboratory findings and explain their clinical significance in relation to the patient's symptoms." Our findings indicate that while the LLM could identify most laboratory results, it frequently failed to highlight and interpret abnormal values critical to understanding the patient's conditions, particularly in cases like ([[Murphy et al.,](#ref-68-7)] [[2018)]](#ref-68-7) and ([[Kazi](#ref-65-9)] [[et al.,](#ref-65-9)] [[2020)]](#ref-65-9). For example, in the adenocarcinoma patient case ([[Murphy et al.,](#ref-68-7)] [[2018)]](#ref-68-7), the patient's laboratory examination revealed a significantly elevated lactate level, a critical indicator of tissue hypoxia. Alarmingly, the LLM failed to report this crucial abnormality in its generated response, demonstrating a potential gap in its ability to prioritize and interpret clinically significant lab results.

### Differential Diagnosis Test

Finally, we assessed the LLM's ability to generate differential diagnoses, a vital skill in clinical decision-making. For the Differential Diagnosis Test, we asked: "Based on the Presentation of Case, Lab Data and Images, what would be the possible diagnosis?" When generating decision trees for differential diagnoses, the LLM was generally accurate in identifying primary considerations. However, it occasionally overlooked or minimized less obvious, yet clinically relevant, differential diagnoses. For instance, in the coronary artery dissection case ([[Tsiaras et al.,](#ref-73-8)] [[2017)]](#ref-73-8), the LLM missed the potential for esophageal spasm as a differential diagnosis, highlighting a tendency to focus on the most prominent diagnoses and potentially overlooking a broader spectrum of possibilities.

## <a id="page-43-0"></a>7.4 Analysis of Hallucination Rates and Risk Distributions Across Tasks and Models

Based on expert annotations (Subsection [[7.3)]](#ref-7.3)), we rigorously quantified hallucination rates and the severity of associated clinical risks for five prominent LLMs: 'o1', 'gemini-2.0-flash-exp', 'gpt-4o','gemini-1.5-flash', and 'claude-3.5 sonnet' (see Figure [[1)]](#ref-1)). Clinical risks were systematically categorized across a granular scale from 'No Risk' (0) to 'Catastrophic' (5), allowing for a nuanced evaluation of both the frequency and potential clinical ramifications of LLM-generated inaccuracies in medical contexts.

## Overall Hallucination Rates and Task-Specific Trends

A notable task-specific trend emerged: Diagnosis Prediction consistently exhibited the lowest overall hallucination rates across all models, ranging from 0% to 22%. Conversely, tasks demanding precise factual recall and temporal integration – Chronological Ordering (0.25 - 24.6%) and Lab Data Understanding (0.25 - 18.7%) – presented significantly higher hallucination frequencies. This finding challenges a simplistic assumption that diagnostic tasks, often perceived as complex inferential problems, are inherently more error-prone for LLMs. Instead, our results suggest that current LLM architectures may possess a relative strength in pattern recognition and diagnostic inference within medical case reports, but struggle with the more fundamental tasks of accurately extracting and synthesizing detailed factual and temporal information directly from clinical text.

### Model-Specific Hallucination Rates

GPT-4o consistently demonstrated the highest propensity for hallucinations in tasks requiring factual and temporal accuracy. Specifically, its hallucination rates in Chronological Ordering (24.6%) and Lab Data Understanding (18.7%) were markedly elevated compared to other models. Crucially, a substantial proportion of these hallucinations were independently classified by medical experts as posing 'Significant' or 'Considerable' clinical risk, highlighting not just the frequency but also the potential clinical impact of GPT-4o's inaccuracies in these fundamental tasks. Interestingly, while GPT-4o's hallucination rate in Diagnosis Prediction was also comparatively high in absolute terms (22.0%), it was marginally lower than that observed for Gemini-2.0 flash-exp (2.25%, although a potential data discrepancy between output logs and visual representation warrants further investigation).

The Gemini model family exhibited divergent performance characteristics. Gemini-2.0-flash-exp consistently maintained low hallucination rates across all three tasks, demonstrating relative strength in both factual/temporal processing and diagnostic inference. Its rates were notably low for Chronological Ordering (2.25%), Lab Data Understanding (2.25%), and Diagnosis Prediction (1.0%, with the aforementioned data discrepancy). In contrast, Gemini-1.5-flash displayed moderately elevated hallucination rates, particularly in Lab Data Understanding (12.3%) and Chronological Ordering (5.0%). While Gemini-1.5-flash also generated errors categorized as 'Significant' and 'Considerable' risk, these occurred at lower frequencies than observed with GPT-4o.

Claude-3.5 and o1 consistently emerged as the top-performing models across this evaluation, exhibiting the lowest hallucination rates across all tasks and risk categories. Remarkably, both models achieved a 0% hallucination rate in the Diagnosis Prediction task, suggesting a high degree of reliability for diagnostic inference within this specific context. Claude-3.5 demonstrated exceptionally low hallucination rates of 0.5% (Chronological Ordering) and 0.25% (Lab Data Understanding). o1 mirrored this strong performance, with equally low or slightly superior rates of 0.25% for both Chronological Ordering and Lab Data Understanding.

### Risk Level Distribution and Clinical Implications

While GPT-4o's higher hallucination frequency and associated clinical risk severity in Chronological Ordering and Lab Data Understanding tasks are concerning, the surprisingly low overall hallucination rates in Diagnosis Prediction – especially the 0% rate achieved by Claude-3.5 and o1 – offer a nuanced perspective. These findings indicate that while current LLMs are not uniformly reliable across all clinical reasoning tasks, specific models, such as Claude-3.5 and o1, may possess a nascent but promising aptitude for diagnostic inference within structured medical case presentations. However, the consistent presence of 'Significant' and 'Considerable' risk errors even within models exhibiting lower aggregate hallucination rates underscores a critical and overarching implication: irrespective of overall performance metrics, the deployment of any current LLM in clinical settings necessitates rigorous, task-specific validation protocols, continuous performance monitoring, and careful integration within human-in-the-loop workflows. The potential for even low-frequency, but high-risk, hallucinations in fundamental tasks like temporal sequencing and factual recall necessitates a cautious and evidence-driven approach to LLM adoption in healthcare, prioritizing patient safety and clinical accuracy above claims of generalized AI proficiency.

## <a id="page-44-0"></a>7.5 Inter-rater Reliability Analysis

## Quantifying Agreement in Hallucination Annotation.

To rigorously assess the consistency and reliability of our qualitative evaluations, we conducted a comprehensive inter-rater reliability analysis. Seven expert annotators, each possessing an MD degree or advanced clinical specialization, independently evaluated the outputs generated by the language models for each of the 20 clinical case reports. This analysis focused on two critical dimensions of annotation: 1) hallucination type and 2) clinical risk level. To quantify the degree of agreement among annotators, we employed the Average Pairwise Jaccard-like Index ([[Jaccard,](#ref-63-9)] [[1901)]](#ref-63-9), a metric well-suited for assessing set similarity and inter-rater agreement in annotation tasks. The aggregate inter-rater agreement, averaged across all cases and language models,

<a id="page-45-0"></a>## An example of Physician annotations on LLM's response

### Prompt to LLM:

Instructions: Given the 'Presentation of Case' of the patient, please order the key events chronologically and identify temporal relationships between symptoms and interventions: {Presentation of Case}

LLM response: Here is the chronological ordering of key events and identification of temporal relationships between symptoms and interventions:

*   8 Months Before Admission: Fatigue on exertion and subjective leg weakness develop, marking the onset of the patient's decline.
*   5 Months Before Admission: Hypoesthesias and paresthesias appear intermittently in the feet, suggesting early peripheral nerve involvement. Walking distance continues to shorten due to fatigue and weakness.
*   4 Months Before Admission: Two lower teeth become loose and fall out without preceding trauma, indicating possible nutritional deficiencies.
*   4 to 2 Months Before Admission: Fatigue and leg weakness progress. The patient needs to use his arms to rise from a seated position, indicating significant muscle weakness.
*   2 Days Before Admission: The patient falls while carrying groceries, striking the left side of his face. He reports mild pain above the left eye without additional symptoms like headache or neck pain.
*   At Clinic Visit (Before Admission): Gingival bleeding observed, likely due to nutritional deficiencies. Ecchymoses (bruising) on the knees and two absent lower front teeth noted (...)
*   Emergency Department (At Admission):
    *   Findings: Purple ecchymoses on the left face, left flank, and brown around the right eye (likely due to trauma and nutritional issues) (...)
    *   Progression: Over 48 hours, the patient demonstrates improved blood pressure and the ability to stand with minimal arm use. Bruising develops on the right forearm, likely from the IV catheter.

### Annotator 1: (Other Unsupported)

*   LLM does not mention Roux-en-Y gastric bypass performed 6 years earlier. This is a crucial omission that significantly contributes to the diagnosis.

### Annotator 2: (Condition Unsupported)

*   The patient visited the doctor twice prior to admission. The first visit was four months before admission, and the second visit occurred two days prior to admission. However, the timeline of these visits was not taken into account in this summary, although the content itself remains accurate.

### Annotator 3: (Time Unsupported)

*   Findings at clinical visit and emergency department are placed at wrong timelines.

**Figure 8:** Physician annotations on a GPT-4o generated chronological ordering of clinical events. The original case can be found at [https://www.nejm.org/doi/full/10.1056/NEJMcpc1802826](https://www.nejm.org/doi/full/10.1056/NEJMcpc1802826).

revealed a Jaccard-like Index of 0.272 for hallucination type classification and 0.347 for clinical risk level assessment.

### Moderate Agreement in Medical Annotation.

The observed Jaccard-like Index values, ranging from 0 to 1, indicate a moderate level of inter-rater agreement. While not indicative of perfect consensus, these values are interpretable within the context of the inherent complexity and subjectivity associated with nuanced medical text analysis. The moderate agreement reveaos the inherent challenges in achieving complete uniformity when evaluating subtle linguistic outputs for medical accuracy. For instance, as illustrated in Figure [[8]](#ref-8), annotators exhibited variability in assessing the LLM's summary of a patient case. While the factual omission of a Roux-en-Y gastric bypass was clearly identified as an error by one annotator, the discrepancies in the reported timelines of doctor's visits were interpreted differently by others. This example highlights the difficulty in distinguishing between critical factual inaccuracies, like the missing surgery, and potentially less clinically impactful temporal inaccuracies or stylistic choices in summarizing complex medical timelines.

### Sources of Subjectivity and Annotation Challenges.

Discussions with the expert annotators highlighted several key factors contributing to the observed inter-rater variability, many of which are exemplified in the annotation discrepancies shown in Figure [[8]](#ref-8). A primary challenge lies in the nuanced distinction between bona fide medical hallucinations and less critical errors, a point clearly illustrated by Annotator 1's identification of the omitted Roux-en-Y gastric bypass. This omission represents a potentially clinically significant factual inaccuracy, arguably a 'bona fide' hallucination due to its relevance to patient history and diagnosis. In contrast, Annotators 2 and 3 focused on temporal inaccuracies, highlighting discrepancies in the timeline of doctor's visits and the emergency department visit. These temporal issues, while potentially less clinically critical than the omission of a major surgery, still represent deviations from the source text and demonstrate the subjective interpretation of 'accuracy' in summarizing complex medical timelines. This distinction necessitates a high degree of clinical judgment, as annotators must decide not only if information is factually present but also its clinical relevance and the acceptable level of summarization detail.

### Methodological Rigor to Enhance Annotation Consistency.

To mitigate potential subjectivity and enhance annotation consistency, we implemented several methodological safeguards prior to and during the annotation process. We developed a comprehensive and interactive annotation web interface [^∗^](#ref-footnote-1) (Figure [[B1,](#ref-B1)] [[B2,](#ref-B2)] [[B3)]](#ref-B3)) that incorporated detailed, operationally defined criteria and illustrative examples for each hallucination type and clinical risk level category. Moreover, we established proactive communication channels with each annotator, encouraging open dialogue and providing ongoing support to address any ambiguities, interpretational challenges, or uncertain cases encountered during their assessments. This iterative

[^∗^](#ref-footnote-1)Accessible at <https://medical-hallucination.github.io/>

process aimed to refine understanding of the annotation guidelines and promote convergent interpretations among the expert raters.

### Time Investment and Expertise Demands in Medical Annotation.

The time investment required for annotation varied according to the annotator's domain expertise and the specific complexity of each case report. Annotators were explicitly authorized and encouraged to leverage external, authoritative medical resources, including platforms such as UpToDate and PubMed, to inform their evaluations and ensure comprehensive assessments. The NEJM case reports, characterized by their depth, clinical intricacy, and frequent presentation of unusual or diagnostically challenging conditions, necessitated a substantial time commitment from each annotator for thorough and conscientious evaluation of the language model outputs.

### Value of Qualitative Insights Despite Agreement Limitations.

Despite the inherent challenges in achieving perfect inter-rater agreement in this complex domain, the patterns and trends emerging from our annotation process remain profoundly valuable. The observed inter-rater reliability, while moderate, is sufficient to support the identification of systematic biases and error modalities within the language models' clinical reasoning and text generation capabilities. The qualitative insights derived from this rigorous annotation process offer critical directions for future model refinement and for developing strategies to mitigate clinically relevant medical hallucinations in large language models, as elaborated in the subsequent sections.

## <a id="page-47-0"></a>8 Survey on AI/LLM Adoption and Medical Hallucinations Among Healthcare Professionals and Researchers

To investigate the perceptions and experiences of healthcare professionals and researchers regarding the use of AI / LLM tools, particularly regarding medical hallucinations, we conducted a survey aimed at individuals in the medical, research, and analytical fields (Figure [[9)]](#ref-9)). A total of 75 professionals participated, primarily holding MD and/or PhD degrees, representing a diverse range of disciplines. The survey was conducted over a 94-day period, from September 15, 2024, to December 18, 2024, confirming the significant adoption of AI/LLM tools across these fields. Respondents indicated varied levels of trust in these tools, and notably, a substantial proportion reported encountering medical hallucinations—factually incorrect yet plausible outputs with medical relevance—in tasks critical to their work, such as literature reviews and clinical decision-making. Participants described employing verification strategies like cross-referencing and colleague consultation to manage these inaccuracies (see Appendix [[A]](#ref-A) for more details).

This study received an Institutional Review Board (IRB) exemption from MIT COUHES (Committee On the Use of Humans as Experimental Subjects) under exemption category 2 (Educational Testing, Surveys, Interviews, or Observation). The IRB determined that this research, involving surveys with professionals on their perceptions and experiences with AI/LLMs, posed minimal risk to participants and met the criteria for exemption.

The survey instrument, comprising 31 questions, was administered online, achieving a 93% completion rate from 75 participants. The resulting dataset of 70 complete responses formed the primary input for our analysis, enabling both quantitative and qualitative examination of the data. For example, qualitative analysis of open-ended responses on hallucination instances allowed us to identify recurring themes, which were then quantified to assess the prevalence and impact of medical hallucinations.

Respondents identified key factors contributing to medical hallucinations, including limitations in training data and model architectures. They emphasized the importance of enhancing accuracy, explainability, and workflow integration in future AI/LLM tools. Furthermore, ethical considerations, privacy, and user education were highlighted as essential for responsible implementation. Despite acknowledging these challenges, participants generally expressed optimism about the future potential of AI in their fields. The following subsections detail these findings, providing a comprehensive analysis of respondent demographics, tool usage patterns, perceptions of correctness and hallucinations, and perspectives on the future development and safe implementation of AI/LLMs in healthcare and research.development and safe implementation of AI/LLMs in healthcare and research.

## <a id="page-48-0"></a>8.1 Respondent Demographics

A total of 75 respondents participated in the survey, representing a diverse range of professional backgrounds within the medical and scientific communities. The largest group comprised Medical Researchers or Scientists (n = 29), followed by Physicians or Medical Doctors (n = 23), Data Scientists or Analysts (n = 15), and Biomedical Engineering professionals (n = 5), and others (n = 3). Most respondents held advanced degrees, with 52 possessing either a PhD or MD, 11 holding a Master's degree, 9 with a Bachelor's degree and 3 with others. Their professional experience varied: 30 had worked 1–5 years, 25 had 6–10 years, and 19 had over 20 years of professional experience. This breadth of expertise and educational attainment ensured that the survey captured perspectives across multiple career stages and levels of specialization.

## <a id="page-48-1"></a>8.2 Regional Representation

The geographic distribution of participants highlighted regions with robust AI infrastructures. Asia was most strongly represented (n = 27), followed by North America (n = 22), South America (n = 9), Europe (n = 8), and Africa (n = 4). While this sample provided valuable insights into regions where AI is more deeply integrated into healthcare and research workflows, the limited representation from other continents signals a need for future investigations to include a broader global perspective.

## <a id="page-48-2"></a>8.3 Usage and Trust in AI/LLM Tools

AI/LLM tools were well integrated into respondents' routines: 40 used these tools daily, 9 used them several times per week, 13 used them few times a month, and 13 reported

<a id="page-49-0"></a>![This image presents survey results on physicians' use of Large Language Models (LLMs) in clinical practice. It includes bar charts showing LLM usage frequency and popularity (ChatGPT leading), pie charts illustrating encounter rates with medical hallucinations and optimism about future applications, and bar charts detailing reasons physicians attribute to LLM hallucinations (false information being most prevalent). Finally, it shows the prioritization of accuracy, explainability, and ethics in LLM development, and the importance of human supervision and transparency.](_page_49_Figure_1.jpeg)

**Figure 9:** Key insights from a multi-national clinician survey on medical hallucinations in clinical practice. The survey highlights the most commonly used LLMs and their frequency of use among physicians (top), clinicians' experiences with LLM hallucinations and their perspectives on AI-assisted medical practice (middle), and the primary reasons attributed to LLM hallucinations along with the importance of human oversight, training, and transparency as safeguards (bottom).

rare or no usage. Despite this widespread adoption, trust levels exhibited more caution. While 30 respondents expressed high trust in AI/LLM outputs, 25 reported moderate trust, and 12 indicated low trust. These findings suggest that although AI tools have gained significant traction, users remain mindful of their limitations, seeking greater reliability and interpretability.

## <a id="page-50-0"></a>8.4 Perceived Correctness and Encounters with AI Hallucinations

Perceptions of correctness were mixed. Of the 61 respondents, 21 believed that AI/LLM outputs were "often correct", 18 stated they were "sometimes correct", and 6 felt they were "rarely correct". More critically, hallucinations—instances where the AI-generated plausible but incorrect information—were widely encountered by 37 respondents. Such hallucinations emerged across various tasks: literature reviews (38 mentions), data analysis (25), patient diagnostics (15), treatment recommendations (13), research paper drafting (16), grant writing (4), solving board exams (7), EHR summaries (4), patient communication (5), insurance billing (2), and citations (1). The prevalence of hallucinations in high-stakes tasks emphasized the need for meticulous verification and supplemental oversight.

## <a id="page-50-1"></a>8.5 Responses to AI Hallucinations

Respondents reported multiple strategies for addressing hallucinations. The most common approach was cross-referencing with external sources, employed by 85% (51) of respondents. Other strategies included consulting colleagues or experts (12), ignoring erroneous outputs (11), ceasing use of the AI/LLM (11), directly informing the model of its mistake (1), updating the prompt (1), relying on known correct answers (1), and examining underlying code (1). Assessing the impact of these hallucinations on a 1–5 scale, 21 respondents rated the impact as moderate (3), 22 rated it as low (2), 9 saw no impact (1), 5 observed high impact (4), and 2 reported a very high impact (5). This distribution suggests that while hallucinations are common, many respondents have developed coping mechanisms that mitigate their overall influence.

## <a id="page-50-2"></a>8.6 Causes of AI Hallucinations

Respondents identified various potential causes of hallucinations. Insufficient training data was the most frequently cited factor (31 mentions), followed by biased training data (31), limitations in model architecture (30), lack of real-world context (26), overconfidence in AI-generated responses (24), inadequate transparency of AI decision-making (14), and others (4). Moreover, 50 out of 59 participants believe the hallucination they experienced or observed might impact patient health. However, only 6 out of 59 participants believe there is more than a medium severity of the impact of AI hallucinations on their daily work, given AI has not yet fully merged into clinical workflow. These reflections underscore the multifaceted technical and ethical dimensions that must be addressed to improve model reliability.

## <a id="page-50-3"></a>8.7 Limitations of AI/LLMs and Future Outlook

lack of domain-specific knowledge emerged as the most critical limitation (30) followed by the privacy and data security concerns (25), accuracy issues (24), lack of standardization/validation of AI tools (23), difficulty in explaining AI decisions (21), a range of ethical considerations (20), and others (3).

Despite these concerns, the sentiment toward future developments was predominantly positive. A majority of respondents were optimistic (32) or very optimistic (24), with only a small minority expressing pessimism (3). Regarding the direct impact of AI/LLMs on patient health, opinions were mixed: 21 respondents believed there was an impact, 15 did not, 22 were uncertain, and 16 did not provide a clear stance. This divergence highlights an evolving field where the clinical value of LLMs is still being established.

## <a id="page-51-0"></a>8.8 Commonly Used AI/LLM Tools

In terms of specific technologies, ChatGPT was the most commonly mentioned tool (30 mentions), followed by Claude (20), Google Bard/Gemini (16), and open-source models such as Llama (15). Additional tools like Perplexity (9), Alphafold (2), Copilot (1), Scite and Consensus (1) also featured, reflecting a diverse ecosystem of AI solutions supporting medical and research professionals.

## <a id="page-51-1"></a>8.9 Future Priorities and Hallucination Safeguards

When asked about priorities for improvement, respondents emphasized enhancing accuracy (12 mentions), explainability (10), and ethical considerations, including bias reduction and privacy (8). Integration with existing tools (7) and improving speed and efficiency (3) were also noted. To safeguard against hallucinations, recommendations included manual cross-checking and verification (10), human supervision and expert review (8), confidence scoring or indicators (5), improving model architecture and training (5), training and education on AI limitations (4), and establishing ethical guidelines and standards (3). These suggestions outline a path toward greater reliability, transparency, and responsible integration of AI in healthcare.

## <a id="page-51-2"></a>9 Regulatory and Legal Considerations for AI Hallucinations in Healthcare

## <a id="page-51-3"></a>9.1 Deploying AI Systems in the Real-world Healthcare

AI systems developed to be deployed in the real-world need to be assessed for quality, safety, and reliability control ([[Blumenthal and Patel,](#ref-58-9)] [[2024)]](#ref-58-9). Furthermore, they are required to meet codes of ethics and regulatory frameworks established by expert societies and governmental bodies, as models' errors can lead to life-threatening consequences ([[Coiera and Fraile-Navarro,](#ref-58-10)] [[2024)]](#ref-58-10). Although frameworks specifically designed for AI as a medical device are less developed compared to those for other types of medical devices, established rules (Figure [[10]](#ref-10)) and new policies from expert associations and governmental organizations apply when an AI tool is used as a medical device. Incorporating these regulatory requirements during development aims to ensure that AI tools are effectively developed.

<a id="page-52-2"></a>![This flowchart categorizes regulations governing AI as a medical device. It branches from "As a Medical Device" into three categories: General AI Regulation (listing the National AI Initiative Act of 2020, FTC regulations, etc.), Healthcare Regulation (including HIPAA, HHS, CMS, and AMA policies), and Specific SaMD Regulation (FDA regulations and guidance). The flowchart visually organizes the diverse regulatory landscape for AI in healthcare.](_page_52_Figure_1.jpeg)

**Figure 10:** Regulatory Landscape for AI as a Medical Device: A Framework Categorizing General AI, Healthcare, and Software as a Medical Device (SaMD)-Specific Regulations.

## <a id="page-52-0"></a>9.2 Federal Oversight of AI Systems

At the broadest level, the deployment of an AI system in the United States is governed by federal agencies tasked with ensuring public safety and consumer protection. The Federal Trade Commission (FTC) maintains primary oversight authority, with the power to take action against companies that misrepresent AI capabilities or deploy systems that cause consumer harm ([[Federal Trade Commission,](#ref-61-8)] [[2024)]](#ref-61-8). This oversight has become increasingly critical as the accessibility of AI development tools enables a wider range of entities to create and deploy AI systems, sometimes without adequate expertise or safety considerations. The regulatory landscape was significantly shaped by Executive Order 14110, signed in October 2023 ([[Congressional Research Service,](#ref-59-8)] [[2023)]](#ref-59-8), which established comprehensive requirements for AI system safety testing and transparency. This order works in conjunction with the Office of Science and Technology Policy's Blueprint for an AI Bill of Rights ([[The White House Office of](#ref-73-9)] [[Science and Technology Policy,](#ref-73-9)] [[2022)]](#ref-73-9) and the National Institute of Standards and Technology's AI Risk Management Framework ([[National Institute of Standards and](#ref-68-8)] [[Technology,](#ref-68-8)] [[2023)]](#ref-68-8) to create a foundational structure for responsible AI development and deployment.

## <a id="page-52-1"></a>9.3 Healthcare-Specific Regulatory Requirements

When AI systems enter the healthcare domain, they encounter additional layers of regulation designed to protect patient safety and privacy. The Health Insurance Portability and Accountability Act (HIPAA) establishes fundamental requirements for the handling of protected health information ([[U.S. Department of Health and Human](#ref-74-3)] [[Services,](#ref-74-3)] [[2024c)]](#ref-74-3). Any AI system processing patient data must comply with HIPAA's Privacy Rule ([[U.S. Department of Health and Human Services,](#ref-74-4)] [[2024b)]](#ref-74-4), Security Rule ([[U.S. Department of Health and Human Services,](#ref-74-5)] [[2024d)]](#ref-74-5), and Breach Notification Rule ([[U.S. Department of Health and Human Services,](#ref-73-10)] [[2024a)]](#ref-73-10). These requirements significantly impact how AI systems can access, process, and store medical data, with substantial penalties for non-compliance.

The American Medical Association (AMA) has also established specific guidelines for AI use in healthcare that emphasize transparency, physician oversight, and patient safety ([[American Medical Association,](#ref-57-9)] [[2024)]](#ref-57-9). These guidelines explicitly position AI systems as augmentative tools rather than replacements for clinical judgment, maintaining that ultimate responsibility for medical decisions must remain with healthcare providers ([[American Medical Association,](#ref-57-10)] [[2012)]](#ref-57-10).

## <a id="page-53-0"></a>9.4 FDA Regulation of AI as Medical Devices

The Food and Drug Administration (FDA) plays a central role in regulating AI systems that function as medical devices. These systems are classified as Software as a Medical Device (SaMD) ([[U.S. Food and Drug Administration,](#ref-74-6)] [[2024i)]](#ref-74-6) when they are intended for use in the diagnosis, treatment, or prevention of disease. The FDA has established a risk-based framework for evaluating these systems, with three primary pathways for approval: (1) Premarket Approval (PMA) for high-risk devices ([[U.S. Food](#ref-74-7)] [[and Drug Administration,](#ref-74-7)] [[2024h)]](#ref-74-7); (2) De Novo classification for novel moderate-risk devices; (3) 510(k) clearance for moderate to low-risk devices that are substantially equivalent to existing approved devices ([[U.S. Food and Drug Administration,](#ref-74-8)] [[2024e)]](#ref-74-8)

Moreover, recognizing the unique challenges posed by AI/ML-enabled medical devices, the FDA has published specific guidance documents, including Good Machine Learning Practice (GMLP) ([[U.S. Food and Drug Administration,](#ref-74-9)] [[2024f)]](#ref-74-9). These guidelines address issues such as data quality, algorithm validation, and performance monitoring that are particularly relevant to AI systems.

## <a id="page-53-1"></a>9.5 State-Level Regulations

At the state level, new regulations are emerging to address AI-specific concerns. Colorado's SB 24-205 ([[Colorado General Assembly,](#ref-59-9)] [[2024)]](#ref-59-9) and California's Assembly Bill 2013 ([[California State Legislature,](#ref-58-11)] [[2024)]](#ref-58-11) represent early efforts to regulate high-risk AI systems and ensure transparency in AI development.

## <a id="page-53-2"></a>9.6 Emerging Challenges in AI Healthcare Regulation

Although the regulatory framework for traditional medical AI applications is better established, generative AI systems present unprecedented challenges that strain existing oversight mechanisms. These systems' unique characteristics—including their stochastic outputs, continuous learning capabilities, and complex integration with clinical workflows—create regulatory gaps that require innovative approaches ([[Reddy,](#ref-70-11)] [[2024)]](#ref-70-11).

Current frameworks, which designed for deterministic medical technologies, struggle to address several key aspects of generative AI systems. Unlike traditional medical devices with predictable outputs, generative AI systems can produce variable responses to identical inputs, making validation against ground truth particularly challenging. These systems often operate across both regulated and non-regulated applications, creating complex oversight scenarios ([[Han et al.,](#ref-63-10)] [[2024)]](#ref-63-10). Perhaps most critically, their ability to generate plausible but incorrect information poses unique safety risks, as demonstrated by our analysis of state-of-the-art systems (Figure [[1)]](#ref-1)) ([[Coiera and](#ref-58-10)] [[Fraile-Navarro,](#ref-58-10)] [[2024)]](#ref-58-10).

Regulatory bodies are beginning to adapt to these challenges. The FDA has introduced new approaches to change control for AI/ML-enabled medical devices ([[U.S.](#ref-74-10)] [[Food and Drug Administration,](#ref-74-10)] [[2024g)]](#ref-74-10), acknowledging the need for more flexible oversight of systems that continue to learn and evolve after deployment. However, these adaptations primarily address supervised learning systems rather than the unique challenges posed by generative AI. The development of effective regulatory frameworks for generative AI requires a data-driven approach that can quantify and categorize different types of hallucinations, establish clear risk thresholds for different clinical applications, and create protocols for monitoring and reporting AI-related adverse events.

## <a id="page-54-0"></a>9.7 Liability and Legal Framework

Finally, the integration of generative AI into healthcare also creates novel liability challenges that existing legal frameworks struggle to address. Traditional medical malpractice law, based on the concept of deviation from standard of care, faces significant hurdles when applied to AI-generated errors. When an AI system generates incorrect or misleading information, determining liability becomes complex, potentially involving AI developers and their training methodologies, healthcare providers using the system, and healthcare institutions implementing the technology ([[Bottomley and](#ref-58-12)] [[Thaldar,](#ref-58-12)] [[2023)]](#ref-58-12).

The "black-box" nature of many AI systems further complicates the establishment of clear causal relationships between system outputs and patient harm ([[AMA Journal](#ref-56-6)] [[of Ethics,](#ref-56-6)] [[2019)]](#ref-56-6). This opacity challenges traditional legal requirements for establishing negligence and causation, particularly when multiple parties share responsibility in the technology's lifecycle.

Legal scholars have proposed several frameworks to address these challenges. One approach involves expanding traditional malpractice standards to include specific requirements for AI system use, including mandatory critical evaluation of AI outputs and documentation of AI-assisted decision-making ([[AMA Journal of Ethics,](#ref-56-6)] [[2019)]](#ref-56-6). Another proposal suggests treating AI systems as products, with potential liability for systematic hallucinations or errors, though this approach faces challenges due to AI systems' ability to evolve through continuous learning ([[Lytal et al.,](#ref-66-10)] [[2023)]](#ref-66-10).

A particularly promising approach involves a distributed liability model that allocates responsibility based on stakeholder roles and control levels ([[Eldakak et al.,](#ref-61-9)] [[2024)]](#ref-61-9). This framework emphasizes proportional responsibility distribution while encouraging comprehensive risk management protocols and structured validation procedures. Such an approach could incentivize all parties to maintain robust safety measures while promoting continued innovation.

The development of effective legal frameworks for AI in healthcare requires careful attention to informed consent, documentation standards, and causation criteria. Clear guidelines must be established for documenting AI-assisted decisions and determining responsibility in cases of adverse events. These legal considerations must evolve alongside technological advances to ensure that the benefits of AI in healthcare can be realized while maintaining robust patient safety protections.

## <a id="page-55-0"></a>10 Conclusion

In this paper, we introduce and define the novel concept of medical hallucination in Foundation Models, distinguishing it from general hallucinations and highlighting its unique risks within healthcare. Through a detailed taxonomy, we categorized the diverse manifestations of medical hallucinations, ranging from factual inaccuracies to complex reasoning errors, providing a structured framework for future research and mitigation efforts. Our investigation into the causes of these hallucinations highlighted the critical roles of data quality, model limitations, and healthcare domain complexities, revealing a multifaceted challenge.

To address this challenge, we explore and benchmark various detection and mitigation strategies, including factual verification, consistency checks, uncertainty quantification, and prompt engineering. Our experimental evaluation on a medical hallucination benchmark revealed the efficacy of techniques like CoT prompting and Internet Search in reducing hallucination rates, while also demonstrating the surprising resilience of advanced general-purpose models in this domain. Furthermore, our annotation of real-world clinical case records by expert physicians provided invaluable qualitative insights into the real-world impact and risk levels associated with medical hallucinations, complementing our quantitative findings. A comprehensive clinician survey across the countries further enriched our understanding by capturing the perceptions and experiences of healthcare professionals regarding AI/LLM adoption and the challenges of medical hallucinations in practice. Finally, we addressed the critical regulatory and legal considerations surrounding AI in healthcare, emphasizing the urgent need for ethical guidelines and robust frameworks to ensure patient safety and accountability.

Collectively, this work makes contributions by establishing a foundational understanding of medical hallucinations, offering practical detection and mitigation strategies, and highlighting the critical need for responsible AI deployment in healthcare. As Foundation Models become increasingly integrated into clinical practice, our findings serve as a crucial guide for researchers, developers, clinicians, and policymakers. Moving forward, continued attention, interdisciplinary collaboration, and a focus on robust validation and ethical frameworks will be paramount to realizing the transformative potential of AI in healthcare, while effectively safeguarding against the inherent risks of medical hallucinations and ensuring a future where AI serves as a reliable and trustworthy ally in enhancing patient care and clinical decision-making.

## Acknowledgements

The authors thank Chanwoo Park (MIT) and Chelsea Joe (MIT) for contributions to the initial brainstorming and the paper reviews in LLM hallucination and mitigation strategy. We are also grateful to Rosalind Picard (MIT) for her insightful review and high-level comments, which helped refine the paper. Additionally, we appreciate Yoon Kim (MIT) for his guidance on research direction and idea development. We also thank Peter Szolovits (MIT) for his pivotal role in conceptualizing medical hallucinations and contributing to the brainstorming process.

We extend our gratitude to Yanjun Gao (University of Colorado Anschutz Medical Campus) for their detailed review of Section 5, and to Monica Agrawal (Duke University) for her insightful feedback on the manuscript.

Furthermore, we would like to thank Leo Celi (MIT) for sharing his valuable research ideas, providing critical paper review, offering insightful perspectives on aspects of medical research, and contributing real-world practice stories and examples that enriched our understanding. We are grateful to Shannon Shen (MIT) for his helpful advice on paper review and guidance on research direction.

Finally, we are deeply indebted to Hyunsoo Lee, Kayoung Shim, and Yeji Lim from Seoul National University Hospital (SNUH) for their tireless efforts and dedication in annotating the NEJM Case Records. Their meticulous work required a significant investment of time and expertise, and we greatly appreciate their contributions.

This research was supported by a grant of the Korea Health Technology R&D Project through the Korea Health Industry Development Institute (KHIDI), funded by the Ministry of Health & Welfare, Republic of Korea (grant number : RS-2024- 00439677)

## <a id="page-56-0"></a>Bibliography

*   <a id="ref-56-5"></a>Angelopoulos, A.N., Bates, S.: A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification (2022). [https://arxiv.org/abs/2107.07511](https://arxiv.org/abs/2107.07511)
*   <a id="ref-56-7"></a>Addlesee, A.: Grounding llms to in-prompt instructions: reducing hallucinations caused by static pre-training knowledge. In: Joint International Conference on Computational Linguistics, Language Resources and Evaluation 2024, pp. 1–7 (2024). ELRA Language Resources Association
*   <a id="ref-56-2"></a>Agarwal, V., Jin, Y., Chandra, M., De Choudhury, M., Kumar, S., Sastry, N.: Medhalu: Hallucinations in responses to healthcare queries by large language models. arXiv preprint arXiv:2409.19492 (2024)
*   <a id="ref-56-4"></a>Aydin, S., Karabacak, M., Vlachos, V., Margetis, K.: Large language models in patient education: a scoping review of applications in medicine. Frontiers in Medicine 11, 1477898 (2024)
*   <a id="ref-56-6"></a>AMA Journal of Ethics: Are current tort liability doctrines adequate for addressing injury caused by AI? AMA Journal of Ethics 21(2), 160–166 (2019) [https://doi.org/10.1001/amajethics.2019.160](https://doi.org/10.1001/amajethics.2019.160)
*   <a id="ref-56-3"></a>Alsentzer, E., Murphy, J.R., Boag, W., Weng, W.-H., Jin, D., Naumann, T., McDermott, M.: Publicly available clinical bert embeddings. arXiv preprint arXiv:1904.03323 (2019)

<a id="ref-56-1"></a>Asgari, E., Montana-Brown, N., Dubois, M., Khalil, S., Balloch, J., Pimenta, D.: A framework to assess clinical safety and hallucination rates of llms for medical text summarisation. medRxiv, 2024–09 (2024)

*   <a id="ref-57-10"></a>American Medical Association: Principles of medical ethics. PubMed Central (2012). Accessed: 2024-11-04
*   <a id="ref-57-9"></a>American Medical Association: Augmented Intelligence in Health Care: AMA's AI Principles. Accessed: 2024-11-04 (2024). [https://www.ama-assn.org/system/files/ama-ai-principles.pdf](https://www.ama-assn.org/system/files/ama-ai-principles.pdf)
*   <a id="ref-57-6"></a>Asai, A., Min, S., Zhong, Z., Chen, D.: Retrieval-based language models and applications. In: Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 6: Tutorial Abstracts), pp. 41–46 (2023)
*   <a id="ref-57-0"></a>Agarwal, V., Pei, Y., Alamir, S., Liu, X.: CodeMirage: Hallucinations in Code Generated by Large Language Models (2024). <https://arxiv.org/abs/2408.08333>
*   <a id="ref-57-8"></a>Abu-Salih, B., Al-Qurishi, M., Alweshah, M., Al-Smadi, M., Alfayez, R., Saadeh, H.: Healthcare knowledge graph construction: A systematic review of the state-of-theart, open issues, and opportunities. Journal of Big Data 10(1), 81 (2023)
*   <a id="ref-57-2"></a>Ahmad, M.A., Yaramis, I., Roy, T.D.: Creating trustworthy llms: Dealing with hallucinations in healthcare ai. arXiv preprint arXiv:2311.01463 (2023)
*   <a id="ref-57-3"></a>Blumenthal-Barby, J.S., Krieger, H.: Cognitive biases and heuristics in medical decision making: A critical review using a systematic search strategy. Medical Decision Making 35(4), 539–557 (2014) <https://doi.org/10.1177/0272989X14547740>
*   <a id="ref-57-1"></a>Bari, A., Khan, R.A., Rathore, A.W.: Medical errors; causes, consequences, emotional response and resulting behavioral change. Pakistan Journal of Medical Sciences 32(3), 523–528 (2016) <https://doi.org/10.12669/pjms.323.9701>
*   <a id="ref-57-4"></a>Borden, N., Linklater, D.: Hickam's dictum. Western Journal of Emergency Medicine: Integrating Emergency Care with Population Health 14(2) (2013)
*   <a id="ref-57-7"></a>Borgeaud, S., Mensch, A., Hoffmann, J., Cai, T., Rutherford, E., Millican, K., Van Den Driessche, G.B., Lespiau, J.-B., Damoc, B., Clark, A., et al.: Improving language models by retrieving from trillions of tokens. In: International Conference on Machine Learning, pp. 2206–2240 (2022). PMLR
*   <a id="ref-57-5"></a>Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J.D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., Agarwal, S., Herbert-Voss, A., Krueger, G., Henighan, T., Child, R., Ramesh, A., Ziegler, D., Wu, J., Winter, C., Hesse, C., Chen, M., Sigler, E., Litwin, M., Gray, S., Chess, B., Clark, J., Berner, C., McCandlish, S., Radford, A., Sutskever, I., Amodei, D.: Language models are few-shot learners 33, 1877–1901 (2020)

*   <a id="ref-58-9"></a>Blumenthal, D., Patel, B.: The regulation of clinical artificial intelligence. NEJM AI 1(8), 2400545 (2024)

*   <a id="ref-58-1"></a>Brinkmann, R., Rosenberg, E., Louis, D.N., Podolsky, S.H.: Building a Community of Medical Learning—A Century of Case Records of the Massachusetts General Hospital in the Journal. Mass Medical Soc (2024)
*   <a id="ref-58-0"></a>Burke, G., Schellmann, H.: Researchers say an ai-powered transcription tool used in hospitals invents things no one ever said. AP News (2024). Accessed: 2025-02-22
*   <a id="ref-58-8"></a>Bansal, R., Samanta, B., Dalmia, S., Gupta, N., Vashishth, S., Ganapathy, S., Bapna, A., Jain, P., Talukdar, P.P.: Llm augmented LLMs: Expanding capabilities through composition. (2024)
*   <a id="ref-58-12"></a>Bottomley, D., Thaldar, D.: Liability for harm caused by AI in healthcare: An overview of the core legal concepts. Frontiers in Pharmacology 14, 1297353 (2023) [https://doi.org/10.3389/fphar.2023.1297353](https://doi.org/10.3389/fphar.2023.1297353)
*   <a id="ref-58-3"></a>Bai, Z., Wang, P., Xiao, T., He, T., Han, Z., Zhang, Z., Shou, M.Z.: Hallucination of multimodal large language models: A survey. arXiv preprint arXiv:2404.18930 (2024)
*   <a id="ref-58-6"></a>Chen, H., Abdin, Y., et al.: On the diversity of synthetic data and its impact on training large language models. arXiv preprint arXiv:2410.15226 (2024)
*   <a id="ref-58-11"></a>California State Legislature: California Assembly Bill 2013: Generative artificial intelligence: Training data transparency. [https://legiscan.com/CA/text/AB2013/id/3009922](https://legiscan.com/CA/text/AB2013/id/3009922). Accessed: 2024-11-28 (2024)
*   <a id="ref-58-4"></a>Chen, Z., Cano, A.H., Romanou, A., Bonnet, A., Matoba, K., Salvi, F., Pagliardini, M., Fan, S., K¨opf, A., Mohtashami, A., et al.: Meditron-70b: Scaling medical pretraining for large language models. arXiv preprint arXiv:2311.16079 (2023)
*   <a id="ref-58-10"></a>Coiera, E., Fraile-Navarro, D.: AI as an Ecosystem—Ensuring Generative AI Is Safe and Effective. Massachusetts Medical Society (2024)
*   <a id="ref-58-5"></a>Chen, S., Gallifant, J., Gao, M., Moreira, P., Munch, N., Muthukkumar, A., Rajan, A., Kolluri, J., Fiske, A., Hastings, J., Aerts, H., Anthony, B., Celi, L.A., Cava, W.G.L., Bitterman, D.S.: Cross-Care: Assessing the Healthcare Implications of Pre-training Data on Language Model Bias (2024)
*   <a id="ref-58-2"></a>Chen, S., Guevara, M., Moningi, S., Hoebers, F., Elhalawani, H., Kann, B.H., Chipidza, F.E., Leeman, J., Aerts, H.J., Miller, T., et al.: The effect of using a large language model to respond to patient messages. The Lancet Digital Health 6(6), 379–381 (2024)

<a id="ref-58-7"></a>Chung, H.W., Hou, L., Longpre, S., Zoph, B., Tay, Y., Fedus, W., Li, Y., Wang, X., Dehghani, M., Brahma, S., Webson, A., Gu, S.S., Dai, Z., Suzgun, M., Chen, X., Chowdhery, A., Castro-Ros, A., Pellat, M., Robinson, K., Valter, D., Narang, S., Mishra, G., Yu, A., Zhao, V., Huang, Y., Dai, A., Yu, H., Petrov, S., Chi, E.H., Dean, J., Devlin, J., Roberts, A., Zhou, D., Le, Q.V., Wei, J.: Scaling instruction-finetuned language models. Journal of Machine Learning Research 25(70), 1–53 (2024)

*   <a id="ref-59-6"></a>Chandak, P., Huang, K., Zitnik, M.: Building a knowledge graph to enable precision medicine. Scientific Data 10(1), 67 (2023) [https://doi.org/10.1038/s41597-023-01960-3](https://doi.org/10.1038/s41597-023-01960-3)
*   <a id="ref-59-0"></a>Chen, S., Kann, B.H., Foote, M.B., Aerts, H.J.W.L., Savova, G.K., Mak, R.H., Bitterman, D.S.: Use of artificial intelligence chatbots for cancer treatment information. JAMA Oncology 9(10), 1459–1462 (2023) [https://doi.org/10.1001/jamaoncol.2023.2954](https://doi.org/10.1001/jamaoncol.2023.2954)
*   <a id="ref-59-5"></a>Chen, S., Kann, B.H., Foote, M.B., Aerts, H.J., Savova, G.K., Mak, R.H., Bitterman, D.S.: The utility of chatgpt for cancer treatment information. medrxiv. Preprint posted March 16 (2023)
*   <a id="ref-59-1"></a>Christophe, C., Kanithi, P.K., Munjal, P., Raha, T., Hayat, N., Rajan, R., Al-Mahrooqi, A., Gupta, A., Salman, M.U., Gosal, G., et al.: Med42–evaluating fine-tuning strategies for medical llms: Full-parameter vs. parameter-efficient approaches. arXiv preprint arXiv:2404.14779 (2024)
*   <a id="ref-59-4"></a>Chen, J., Kim, G., Sriram, A., Durrett, G., Choi, E.: Complex claim verification with evidence retrieved in the wild. In: Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), pp. 3569–3587 (2024)
*   <a id="ref-59-9"></a>Colorado General Assembly: Colorado Senate Bill 24-205: An Act Concerning Measures to Protect Consumer Data Privacy. Accessed: 2024-11-04 (2024). [https://leg.colorado.gov/sites/default/files/2024a_205_signed.pdf](https://leg.colorado.gov/sites/default/files/2024a_205_signed.pdf)
*   <a id="ref-59-8"></a>Congressional Research Service: Overview of Artificial Intelligence: The National AI Strategy and Major U.S. Policy Issues. Accessed: 2024-11-04 (2023). [https://crsreports.congress.gov/product/pdf/R/R47843](https://crsreports.congress.gov/product/pdf/R/R47843)
*   <a id="ref-59-7"></a>Camburu, O.-M., Rockt¨aschel, T., Lukasiewicz, T., Blunsom, P.: e-snli: Natural language inference with natural language explanations. Advances in Neural Information Processing Systems 31 (2018)
*   <a id="ref-59-3"></a>Chen, I.Y., Szolovits, P., Ghassemi, M.: Can ai help reduce disparities in general medical and mental health care? AMA journal of ethics 21(2), 167–179 (2019)
*   <a id="ref-59-2"></a>Cao, S., Wang, Y., Li, J., He, X., Wang, L.: Calibration of pre-trained transformers. arXiv preprint arXiv:2106.07998 (2021)

*   <a id="ref-60-0"></a>Chen, J., Yang, D., Wu, T., Jiang, Y., Hou, X., Li, M., Wang, S., Xiao, D., Li, K., Zhang, L.: Detecting and evaluating medical hallucinations in large vision language models. arXiv preprint arXiv:2406.10185 (2024)
*   <a id="ref-60-3"></a>Donnelly, K., et al.: Snomed-ct: The advanced terminology and coding system for ehealth. Studies in health technology and informatics 121, 279 (2006)
*   <a id="ref-60-2"></a>Silva, W., Costa Fonseca, L.C., Labidi, S., Lima Pacheco, J.C.: Mitigation of hallucinations in language models in education: A new approach of comparative and cross-verification. In: 2024 IEEE International Conference on Advanced Learning Technologies (ICALT), pp. 207–209 (2024). [https://doi.org/10.1109/ICALT61570.2024.00066](https://doi.org/10.1109/ICALT61570.2024.00066)
*   <a id="ref-60-5"></a>De Cao, N., Aziz, W., Titov, I.: Editing factual knowledge in language models. In: EMNLP 2021-2021 Conference on Empirical Methods in Natural Language Processing, Proceedings, pp. 6491–6506 (2021)
*   <a id="ref-60-4"></a>Devlin, J., Chang, M.-W., Lee, K., Toutanova, K.: BERT: Pre-training of deep bidirectional transformers for language understanding. In: Burstein, J., Doran, C., Solorio, T. (eds.) Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers), pp. 4171–4186. Association for Computational Linguistics, Minneapolis, Minnesota (2019). <https://doi.org/10.18653/v1/N19-1423>. <https://aclanthology.org/N19-1423>
*   <a id="ref-60-8"></a>Desai, S., Durrett, G.: Calibration of pre-trained transformers. In: Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), pp. 295–302 (2020). <https://doi.org/10.18653/v1/2020.emnlp-main.20>. Association for Computational Linguistics
*   <a id="ref-60-6"></a>Dhuliawala, S., Komeili, M., Xu, J., Raileanu, R., Li, X., Celikyilmaz, A., Weston, J.: Chain-of-verification reduces hallucination in large language models. arXiv preprint arXiv:2309.11495 (2023)
*   <a id="ref-60-9"></a>Du, Y., Li, S., Torralba, A., Tenenbaum, J.B., Mordatch, I.: Improving factuality and reasoning in language models through multiagent debate. arXiv preprint arXiv:2305.14325 (2023)
*   <a id="ref-60-1"></a>Dahl, M., Magesh, V., Suzgun, M., Ho, D.E.: Large legal fictions: Profiling legal hallucinations in large language models. Journal of Legal Analysis 16(1), 64–93 (2024) <https://doi.org/10.1093/jla/laae003>
*   <a id="ref-60-7"></a>De Nicola, A., Zgheib, R., Taglino, F.: Toward a knowledge graph for medical diagnosis: issues and usage scenarios, 129–142 (2022)
*   <a id="ref-60-10"></a>Dou, C., Zhang, Y., Chen, Y., Jin, Z., Jiao, W., Zhao, H., Huang, Y.: Detection, diagnosis, and explanation: A benchmark for chinese medial hallucination evaluation. In: Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024), pp. 4784–4794 (2024)

*   <a id="ref-61-9"></a>Eldakak, A., Alremeithi, A., Dahiyat, E., El-Gheriani, M., Mohamed, H., Abdulrahim Abdulla, M.I.: Civil liability for the actions of autonomous ai in healthcare: an invitation to further contemplation. Humanities and Social Sciences Communications 11(1), 1–8 (2024)
*   <a id="ref-61-8"></a>Federal Trade Commission: FTC Submits Comment to FCC on Work to Protect Consumers from Potential Harmful Effects of AI. Accessed: 2024- 11-04 (2024). [https://www.ftc.gov/news-events/news/press-releases/2024/07/ftc-submits-comment-fcc-work-protect-consumers-potential-harmful-effects-ai](https://www.ftc.gov/news-events/news/press-releases/2024/07/ftc-submits-comment-fcc-work-protect-consumers-potential-harmful-effects-ai)
*   <a id="ref-61-3"></a>Finch, A., Hwang, Y.-S., Sumita, E.: Using machine translation evaluation techniques to determine sentence-level semantic equivalence. In: Proceedings of the Third International Workshop on Paraphrasing (IWP2005) (2005)
*   <a id="ref-61-2"></a>Farquhar, S., Kossen, J., Kuhn, L., Gal, Y.: Detecting hallucinations in large language models using semantic entropy. Nature 630(8017), 625–630 (2024)
*   <a id="ref-61-0"></a>Fanta, G.B., Pretorius, L.: Sociotechnical factors of sustainable digital health systems: A system dynamics model. Sustainable Futures (2023) [https://doi.org/10.1016/j.sftr.2023.100127](https://doi.org/10.1016/j.sftr.2023.100127)
*   <a id="ref-61-1"></a>Falke, T., Ribeiro, L.F., Utama, P.A., Dagan, I., Gurevych, I.: Ranking generated summaries by correctness: An interesting but challenging application for natural language inference. In: Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics, pp. 2214–2220 (2019)
*   <a id="ref-61-6"></a>Feng, S., Shi, W., Bai, Y., Balachandran, V., He, T., Tsvetkov, Y.: Knowledge card: Filling LLMs' knowledge gaps with plug-in specialized language models. In: ICLR (2024)
*   <a id="ref-61-4"></a>Feng, S., Shi, W., Wang, Y., Ding, W., Balachandran, V., Tsvetkov, Y.: Don't hallucinate, abstain: Identifying llm knowledge gaps via multi-llm collaboration. arXiv preprint arXiv:2402.00367 (2024)
*   <a id="ref-61-5"></a>Geng, J., Cai, F., Wang, Y., Koeppl, H., Nakov, P., Gurevych, I.: A survey of confidence estimation and calibration in large language models. arXiv preprint arXiv:2311.08298 (2023)
*   <a id="ref-61-7"></a>Geng, J., Cai, F., Wang, Y., Koeppl, H., Nakov, P., Gurevych, I.: A survey of confidence estimation and calibration in large language models. In: Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), pp. 6577–6595 (2024)

*   <a id="ref-62-8"></a>Gema, A.P., Grabarczyk, D., De Wulf, W., Borole, P., Alfaro, J.A., Minervini, P., Vergari, A., Rajan, A.: Knowledge graph embeddings in the biomedical domain: Are they useful? a look at link prediction, rule learning, and downstream polypharmacy tasks. Bioinformatics Advances 4(1), 097 (2024)
*   <a id="ref-62-3"></a>Glicksberg, B.S.: Large language models in medicine: A review of current clinical trials and future prospects. PLOS Digital Health 3(11), 0000662 (2024)
*   <a id="ref-62-9"></a>Gao, Y., Myers, S., Chen, S., Dligach, D., Miller, T.A., Bitterman, D., Chen, G., Mayampurath, A., Churpek, M., Afshar, M.: Position paper on diagnostic uncertainty estimation from large language models: Next-word probability is not pre-test probability. InGenAI for Health: Potential, Trust, and Policy Compliance (2024)
*   <a id="ref-62-4"></a>Group, M.M.W.: Federated benchmarking of medical artificial intelligence with medperf. Nature Machine Intelligence (2023)
*   <a id="ref-62-5"></a>Guerreiro, N.M., Voita, E., Martins, A.F.: Looking for a needle in a haystack: A comprehensive study of hallucinations in neural machine translation. In: Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics, pp. 1059–1075 (2023)
*   <a id="ref-62-7"></a>Gong, F., Wang, M., Wang, H., Wang, S., Liu, M.: Smr: medical knowledge graph embedding for safe medicine recommendation. Big Data Research 23, 100174 (2021)
*   <a id="ref-62-10"></a>Gu, Z., Yin, C., Liu, F., Zhang, P.: Medvh: Towards systematic evaluation of hallucination for large vision language models in the medical context. arXiv preprint arXiv:2407.02730 (2024)
*   <a id="ref-62-0"></a>Goodman, K.E., Yi, P.H., Morgan, D.J.: Ai-generated clinical summaries require more than accuracy. JAMA 331(8), 637–638 (2024) [https://doi.org/10.1001/jama.2024.0555](https://doi.org/10.1001/jama.2024.0555)
*   <a id="ref-62-1"></a>Han, T., Adams, L.C., Papaioannou, J.-M., Grundmann, P., Oberhauser, T., L¨oser, A., Truhn, D., Bressem, K.K.: Medalpaca–an open-source collection of medical conversational ai models and training data. arXiv preprint arXiv:2304.08247 (2023)
*   <a id="ref-62-6"></a>Huang, J., Chen, X., Mishra, S., Zheng, H.S., Yu, A.W., Song, X., Zhou, D.: Large language models cannot self-correct reasoning yet. arXiv preprint arXiv:2310.01798 (2023)
*   <a id="ref-62-2"></a>Hagendorff, T., Fabi, S., Kosinski, M.: Human-like intuitive behavior and reasoning biases emerged in large language models but disappeared in chatgpt. Nature Computational Science (2023) <https://doi.org/10.1038/s43588-023-00527-x>. Brief Communication; Received: 17 February 2023; Accepted: 5 September 2023; Published online: 5 October 2023

*   <a id="ref-63-10"></a>Han, T., Kumar, A., Agarwal, C., Lakkaraju, H.: Towards safe large language models for medicine. In: ICML 2024 Workshop on Models of Human Feedback for AI Alignment (2024)
*   <a id="ref-63-4"></a>Hou, B., Liu, Y., Qian, K., Andreas, J., Chang, S., Zhang, Y.: Decomposing uncertainty for large language models through input clarification ensembling. In: Forty-first International Conference on Machine Learning (2024)
*   <a id="ref-63-6"></a>Hsieh, C., Moreira, C., Nobre, I.B., Sousa, S.C., Ouyang, C., Brereton, M., Jorge, J., Nascimento, J.C.: DALL-M: Context-Aware Clinical Data Augmentation with LLMs (2024). <https://arxiv.org/abs/2407.08227>
*   <a id="ref-63-2"></a>Hammond, M.E.H., Stehlik, J., Drakos, S.G., Kfoury, A.G.: Bias in medicine: Lessons learned and mitigation strategies. JACC: Basic to Translational Science 6(1), 78–85 (2021) <https://doi.org/10.1016/j.jacbts.2020.07.012>
*   <a id="ref-63-11"></a>Hegselmann, S., Shen, S., Gierse, F., Agrawal, M., Sontag, D., Jiang, X.: Medical expert annotations of unsupported facts in doctor-written and llm-generated patient summaries. Physionet (2024)
*   <a id="ref-63-0"></a>Hegselmann, S., Shen, S.Z., Gierse, F., Agrawal, M., Sontag, D., Jiang, X.: A datacentric approach to generate faithful and high quality patient summaries with large language models. arXiv preprint arXiv:2402.15422 (2024)
*   <a id="ref-63-3"></a>Hata, T., Shima, H., Nitta, M., Ueda, E., Nishihara, M., Uchiyama, K., Katsumata, T., Neo, M.: The relationship between duration of general anesthesia and postoperative fall risk during hospital stay in orthopedic patients. Journal of Patient Safety 18(6), 922–927 (2022) <https://doi.org/10.1097/PTS.0000000000001021>
*   <a id="ref-63-1"></a>Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang, H., Chen, Q., Peng, W., Feng, X., Qin, B., et al.: A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions. ACM Transactions on Information Systems (2023)
*   <a id="ref-63-5"></a>Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang, H., Chen, Q., Peng, W., Feng, X., Qin, B., et al.: A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions. ACM Transactions on Information Systems (2024)
*   <a id="ref-63-7"></a>Izacard, G., Lewis, P., Lomeli, M., Hosseini, L., Petroni, F., Schick, T., Dwivedi-Yu, J., Joulin, A., Riedel, S., Grave, E.: Atlas: Few-shot learning with retrieval augmented language models. Journal of Machine Learning Research 24(251), 1–43 (2023)
*   <a id="ref-63-9"></a>Jaccard, P.: Etude comparative de la distribution florale dans une portion des alpes ´ et des jura. Bull Soc Vaudoise Sci Nat 37, 547–579 (1901)

<a id="ref-63-8"></a>Jiang, Z., Araki, J., Ding, H., Neubig, G.: How can we know when language models know? on the calibration of language models for question answering. Transactions of the Association for Computational Linguistics 9, 962–977 (2021)

*   <a id="ref-64-0"></a>Jiang, Y., Chen, J., Yang, D., Li, M., Wang, S., Wu, T., Li, K., Zhang, L.: Comt: Chain-of-medical-thought reduces hallucination in medical report generation. arXiv preprint arXiv:2406.11451 (2024)
*   <a id="ref-64-5"></a>Jin, Q., Dhingra, B., Liu, Z., Cohen, W.W., Lu, X.: Pubmedqa: A dataset for biomedical research question answering. arXiv preprint arXiv:1909.06146 (2019)
*   <a id="ref-64-8"></a>Jin, Q., Kim, W., Chen, Q., Comeau, D.C., Yeganova, L., Wilbur, W.J., Lu, Z.: Medcpt: Contrastive pre-trained transformers with large-scale pubmed search logs for zero-shot biomedical information retrieval. Bioinformatics 39(11), 651 (2023)
*   <a id="ref-64-2"></a>Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y.J., Madotto, A., Fung, P.: Survey of hallucination in natural language generation. ACM Computing Surveys 55(12), 1–38 (2023) <https://doi.org/10.1145/3571730>
*   <a id="ref-64-3"></a>Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y.J., Madotto, A., Fung, P.: Survey of hallucination in natural language generation. ACM Computing Surveys 55(12), 1–38 (2023)
*   <a id="ref-64-6"></a>Jiang, H., Liu, P., Shang, J., Wang, F.: Recent advances in natural language processing for clinical medicine: A survey. Artificial Intelligence in Medicine 128, 102276 (2023)
*   <a id="ref-64-1"></a>Jalilian, L., McDuff, D., Kadambi, A.: The potential and perils of generative artificial intelligence for quality improvement and patient safety. arXiv preprint arXiv:2407.16902 (2024)
*   <a id="ref-64-4"></a>Jin, D., Pan, E., Oufattole, N., Weng, W.-H., Fang, H., Szolovits, P.: What disease does this patient have? a large-scale open domain question answering dataset from medical exams. Applied Sciences 11(14) (2021) [https://doi.org/10.3390/app11146421](https://doi.org/10.3390/app11146421)
*   <a id="ref-64-7"></a>Juhi, A., Pipil, N., Santra, S., Mondal, S., Behera, J.K., Mondal, H.: The capability of chatgpt in predicting and explaining common drug-drug interactions. Cureus 15(3) (2023)
*   <a id="ref-64-9"></a>Ji, Z., Yu, T., Xu, Y., Lee, N., Ishii, E., Fung, P.: Towards Mitigating Hallucination in Large Language Models via Self-Reflection (2023). [https://arxiv.org/abs/2310.06271](https://arxiv.org/abs/2310.06271)
*   <a id="ref-64-10"></a>Kadavath, S., Conerly, T., Askell, A., Henighan, T.J., Drain, D., Perez, E., Schiefer, N., Dodds, Z., DasSarma, N., Tran-Johnson, E., Johnston, S., El-Showk, S., Jones, A., Elhage, N., Hume, T., Chen, A., Bai, Y., Bowman, S., Fort, S., Ganguli, D., Hernandez, D., Jacobson, J., Kernion, J., Kravec, S., Lovitt, L., Ndousse, K., Olsson, C., Ringer, S., Amodei, D., Brown, T.B., Clark, J., Joseph, N., Mann, B., McCandlish, S., Olah, C., Kaplan, J.: Language models (mostly) know what they know. ArXiv abs/2207.05221 (2022)

*   <a id="ref-65-8"></a>Kim, H.-K.: The effects of artificial intelligence chatbots on women's health: A systematic review and meta-analysis. Healthcare 12(5), 534 (2024) [https://doi.org/10.3390/healthcare12050534](https://doi.org/10.3390/healthcare12050534)
*   <a id="ref-65-7"></a>Kamath, A., Jia, R., Liang, P.: Selective question answering under domain shift. In: Jurafsky, D., Chai, J., Schluter, N., Tetreault, J. (eds.) Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pp. 5684– 5696. Association for Computational Linguistics, Online (2020). [https://doi.org/10.18653/v1/2020.acl-main.503](https://doi.org/10.18653/v1/2020.acl-main.503). <https://aclanthology.org/2020.acl-main.503>
*   <a id="ref-65-2"></a>Kang, H., Liu, X.-Y.: Deficiency of Large Language Models in Finance: An Empirical Examination of Hallucination (2023). <https://arxiv.org/abs/2311.15548>
*   <a id="ref-65-4"></a>Kaplan, J., McCandlish, S., Henighan, T., Brown, T.B., Chess, B., Child, R., Gray, S., Radford, A., Wu, J., Amodei, D.: Scaling laws for neural language models. arXiv preprint arXiv:2005.14165 (2020)
*   <a id="ref-65-9"></a>Kazi, D.S., Martin, L.M., Litmanovich, D., Pinto, D.S., Clerkin, K.J., Zimetbaum, P.J., Dudzinski, D.M.: Case 18-2020: A 73-year-old man with hypoxemic respiratory failure and cardiac dysfunction. New England Journal of Medicine 382(24), 2354– 2364 (2020)
*   <a id="ref-65-0"></a>Kim, Y., Park, C., Jeong, H., Chan, Y.S., Xu, X., McDuff, D., Lee, H., Ghassemi, M., Breazeal, C., Park, H.W.: MDAgents: An Adaptive Collaboration of LLMs for Medical Decision-Making (2024). <https://arxiv.org/abs/2404.15155>
*   <a id="ref-65-3"></a>Ke, Y., Yang, R., Lie, S.A., Lim, T.X.Y., Ning, Y., Li, I., Abdullah, H.R., Ting, D.S.W., Liu, N.: Mitigating cognitive biases in clinical decision-making through multi-agent conversations using large language models: Simulation study. Journal of Medical Internet Research 26, 59439 (2024)
*   <a id="ref-65-5"></a>Koopman, B., Zuccon, G.: Dr chatgpt tell me what i want to hear: How different prompts impact health answer correctness. In: Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pp. 15012–15022 (2023)
*   <a id="ref-65-6"></a>Lavrinovics, E., Biswas, R., Bjerva, J., Hose, K.: Knowledge graphs, large language models, and hallucinations: An nlp perspective. arXiv preprint arXiv:2411.14258 (2024)
*   <a id="ref-65-1"></a>Li, S.S., Balachandran, V., Feng, S., Ilgen, J.S., Pierson, E., Koh, P.W., Tsvetkov, Y.: Mediq: Question-asking llms and a benchmark for reliable interactive clinical reasoning. In: The Thirty-eighth Annual Conference on Neural Information Processing Systems (2024)

*   <a id="ref-66-4"></a>Li, J., Chen, J., Ren, R., Cheng, X., Zhao, W.X., Nie, J.-Y., Wen, J.-R.: The dawn after the dark: An empirical study on factuality hallucination in large language models. arXiv preprint arXiv:2401.03205 (2024)
*   <a id="ref-66-3"></a>Lee, A.N., Hunter, C.J., Ruiz, N.: Platypus: Quick, cheap, and powerful refinement of llms. arXiv preprint arXiv:2308.07317 (2023)
*   <a id="ref-66-7"></a>Lee, H., Phatale, S., Mansoor, H., Mesnard, T., Ferret, J., Lu, K., Bishop, C., Hall, E., Carbune, V., Rastogi, A., et al.: Rlaif: Scaling reinforcement learning from human feedback with ai feedback. arXiv preprint arXiv:2309.00267 (2023)
*   <a id="ref-66-1"></a>Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., K¨uttler, H., Lewis, M., Yih, W.-t., Rockt¨aschel, T., et al.: Retrieval-augmented generation for knowledge-intensive nlp tasks. Advances in Neural Information Processing Systems 33, 9459–9474 (2020)
*   <a id="ref-66-6"></a>Lee, J., Park, S., Shin, J., Cho, B.: Analyzing evaluation methods for large language models in the medical field: a scoping review. BMC Medical Informatics and Decision Making 24, 366 (2024)
*   <a id="ref-66-10"></a>Lytal, Reiter, Smith, Ivey, Fronrath: Can AI Be Liable for Malpractice? Blog post. Accessed: 2025-02-16 (2023). [https://www.foryourrights.com/blog/ai-and-medical-malpractice/](https://www.foryourrights.com/blog/ai-and-medical-malpractice/)
*   <a id="ref-66-5"></a>Ly, D.P., Shekelle, P.G., Song, Z.: Evidence for anchoring bias during physician decision-making. JAMA internal medicine 183(8), 818–823 (2023)
*   <a id="ref-66-2"></a>Liu, J., Wang, W., Ma, Z., Huang, G., SU, Y., Chang, K.-J., Chen, W., Li, H., Shen, L., Lyu, M.: Medchain: Bridging the gap between llm agents and clinical practice through interactive sequential benchmarking. arXiv preprint arXiv:2412.01605 (2024)
*   <a id="ref-66-9"></a>Li, Y., Yang, C., Ettinger, A.: When hindsight is not 20/20: Testing limits on reflective thinking in large language models. In: Duh, K., Gomez, H., Bethard, S. (eds.) Findings of the Association for Computational Linguistics: NAACL 2024, pp. 3741–3753. Association for Computational Linguistics, Mexico City, Mexico (2024). [https://aclanthology.org/2024.findings-naacl.237](https://aclanthology.org/2024.findings-naacl.237)
*   <a id="ref-66-0"></a>Li, X., Zhao, R., Chia, Y.K., Ding, B., Joty, S., Poria, S., Bing, L.: Chain-of-knowledge: Grounding large language models via dynamic knowledge adapting over heterogeneous sources. In: International Conference on Learning Representations (ICLR) (2024). ICLR. <https://arxiv.org/pdf/2305.13269>
*   <a id="ref-66-8"></a>Mishra, A., Asai, A., Balachandran, V., Wang, Y., Neubig, G., Tsvetkov, Y., Hajishirzi, H.: Fine-grained hallucination detection and editing for language models. arXiv preprint arXiv:2401.06855 (2024)

*   <a id="ref-67-8"></a>Meng, K., Bau, D., Andonian, A., Belinkov, Y.: Locating and editing factual associations in gpt. Advances in Neural Information Processing Systems 35, 17359–17372 (2022)
*   <a id="ref-67-4"></a>Moradi, M., Blagec, K., Samwald, M.: Deep learning models are not robust against noise in clinical text. arXiv preprint arXiv:2108.12242 (2021)
*   <a id="ref-67-6"></a>Matos, J., Chen, S., Placino, S., Li, Y., Pardo, J.C.C., Idan, D., Tohyama, T., Restrepo, D., Nakayama, L.F., Pascual-Leone, J.M.M., Savova, G., Aerts, H., Celi, L.A., Wong, A.I., Bitterman, D.S., Gallifant, J.: WorldMedQA-V: a multilingual, multimodal medical examination dataset for multimodal language models evaluation (2024). <https://arxiv.org/abs/2410.12722>
*   <a id="ref-67-2"></a>Mehta, N., Devarakonda, M.V.: Machine learning, natural language programming, and electronic health records: The next step in the artificial intelligence journey? Journal of Allergy and Clinical Immunology 141(6), 2019–20211 (2018) [https://doi.org/10.1016/j.jaci.2018.03.017](https://doi.org/10.1016/j.jaci.2018.03.017)
*   <a id="ref-67-5"></a>McDermott, M., Dighe, A., Szolovits, P., Luo, Y., Baron, J.: Using machine learning to develop smart reflex testing protocols. Journal of the American Medical Informatics Association 31(2), 416–425 (2024) <https://doi.org/10.1093/jamia/ocad187>
*   <a id="ref-67-3"></a>Mohammadi, A., Etemad, B., Zhang, X., Li, Y., Bedwell, G.J., Sharaf, R., Kittilson, A., Melberg, M., Crain, C.R., Traunbauer, A.K., Wong, C., Fajnzylber, J., Worrall, D.P., Rosenthal, A., Jordan, H., Jilg, N., Kaseke, C., Giguel, F., Lian, X., Deo, R., Gillespie, E., Chishti, R., Abrha, S., Adams, T., Li, J.Z.: Viral and host mediators of non-suppressible hiv-1 viremia. Nature Medicine 29, 3212–3223 (2023) [https://doi.org/10.1038/s41591-023-02611-1](https://doi.org/10.1038/s41591-023-02611-1)
*   <a id="ref-67-0"></a>Mukherjee, S., Gamble, P., Ausin, M.S., Kant, N., Aggarwal, K., Manjunath, N., Datta, D., Liu, Z., Ding, J., Busacca, S., et al.: Polaris: A safety-focused llm constellation architecture for healthcare. arXiv preprint arXiv:2403.13313 (2024)
*   <a id="ref-67-9"></a>Mohri, C., Hashimoto, T.: Language models with conformal factuality guarantees. arXiv preprint arXiv:2402.10978 (2024)
*   <a id="ref-67-1"></a>Miles-Jay, A., Snitkin, E.S., Lin, M.Y., Shimasaki, T., Schoeny, M., Fukuda, C., Dangana, T., Moore, N., Sansom, S.E., Yelin, R.D., Bell, P., Rao, K., Keidan, M., Standke, A., Bassis, C., Hayden, M.K., Young, V.B.: Longitudinal genomic surveillance of carriage and transmission of clostridioides difficile in an intensive care unit. Nature Medicine 29, 2526–2534 (2023) [https://doi.org/10.1038/s41591-023-02549-4](https://doi.org/10.1038/s41591-023-02549-4)
*   <a id="ref-67-7"></a>Min, S., Krishna, K., Lyu, X., Lewis, M., Yih, W.-t., Koh, P.W., Iyyer, M., Zettlemoyer, L., Hajishirzi, H.: Factscore: Fine-grained atomic evaluation of factual precision in long form text generation. In: The 2023 Conference on Empirical Methods in Natural Language Processing (2023)

*   <a id="ref-68-4"></a>Mitchell, E., Lin, C., Bosselut, A., Manning, C.D., Finn, C.: Memory-based model editing at scale. In: International Conference on Machine Learning, pp. 15817–15831 (2022). PMLR
*   <a id="ref-68-9"></a>Manes, I., Ronn, N., Cohen, D., Ber, R.I., Horowitz-Kugler, Z., Stanovsky, G.: K-qa: A real-world medical q&a benchmark. arXiv preprint arXiv:2401.14493 (2024)
*   <a id="ref-68-7"></a>Murphy, J.E., Shampain, K., Riley, L.E., Clark, J.W., Basnet, K.M.: Case 32-2018: A 36-year-old pregnant woman with newly diagnosed adenocarcinoma. New England Journal of Medicine 379(16), 1562–1570 (2018)
*   <a id="ref-68-0"></a>McDuff, D., Schaekermann, M., Tu, T., Palepu, A., Wang, A., Garrison, J., Singhal, K., Sharma, Y., Azizi, S., Kulkarni, K., et al.: Towards accurate differential diagnosis with large language models. arXiv preprint arXiv:2312.00164 (2023)
*   <a id="ref-68-5"></a>Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L., Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S., Yang, Y., et al.: Self-refine: Iterative refinement with self-feedback. Advances in Neural Information Processing Systems 36 (2024)
*   <a id="ref-68-6"></a>Michalopoulos, G., Wang, Y., Kaka, H., Chen, H., Wong, A.: Umlsbert: Clinical domain knowledge augmentation of contextual embeddings using the unified medical language system metathesaurus. arXiv preprint arXiv:2010.10391 (2020)
*   <a id="ref-68-3"></a>Mishra, P., Yao, Z., Vashisht, P., Ouyang, F., Wang, B., Mody, V.D., Yu, H.: Synfac-edit: Synthetic imitation edit feedback for factual alignment in clinical summarization. arXiv preprint arXiv:2402.13919 (2024)
*   <a id="ref-68-8"></a>National Institute of Standards and Technology: Artificial Intelligence Risk Management Framework. Technical Report NIST AI 100-1, U.S. Department of Commerce (2023). Accessed: 2024-11-04. [https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
*   <a id="ref-68-1"></a>Nazi, Z.A., Peng, W.: Large language models in healthcare and medical domain: A review. In: Informatics, vol. 11, p. 57 (2024). MDPI
*   <a id="ref-68-2"></a>OpenAI, Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I., Aleman, F.L., Almeida, D., Altenschmidt, J., Altman, S., Anadkat, S., Avila, R., Babuschkin, I., Balaji, S., Balcom, V., Baltescu, P., Bao, H., Bavarian, M., Belgum, J., Bello, I., Berdine, J., Bernadett-Shapiro, G., Berner, C., Bogdonoff, L., Boiko, O., Boyd, M., Brakman, A.-L., Brockman, G., Brooks, T., Brundage, M., Button, K., Cai, T., Campbell, R., Cann, A., Carey, B., Carlson, C., Carmichael, R., Chan, B., Chang, C., Chantzis, F., Chen, D., Chen, S., Chen, R., Chen, J., Chen, M., Chess, B., Cho, C., Chu, C., Chung, H.W., Cummings, D., Currier, J., Dai, Y., Decareaux, C., Degry, T., Deutsch, N., Deville, D., Dhar, A., Dohan, D., Dowling, S., Dunning, S., Ecoffet, A., Eleti, A., Eloundou, T., Farhi, D., Fedus, L., Felix, N., Fishman, S.P., Forte, J., Fulford, I., Gao, L., Georges, E., Gibson, C., Goel, V., Gogineni, T., Goh, G., Gontijo-Lopes, R., Gordon, J., Grafstein, M., Gray, S., Greene, R., Gross, J., Gu, S.S., Guo, Y., Hallacy, C., Han, J., Harris, J., He, Y., Heaton, M., Heidecke, J., Hesse, C., Hickey, A., Hickey, W., Hoeschele, P., Houghton, B., Hsu, K., Hu, S., Hu, X., Huizinga, J., Jain, S., Jain, S., Jang, J., Jiang, A., Jiang, R., Jin, H., Jin, D., Jomoto, S., Jonn, B., Jun, H., Kaftan, T., Kaiser, Kamali, A., Kanitscheider, I., Keskar, N.S., Khan, T., Kilpatrick, L., Kim, J.W., Kim, C., Kim, Y., Kirchner, J.H., Kiros, J., Knight, M., Kokotajlo, D., Kondraciuk, Kondrich, A., Konstantinidis, A., Kosic, K., Krueger, G., Kuo, V., Lampe, M., Lan, I., Lee, T., Leike, J., Leung, J., Levy, D., Li, C.M., Lim, R., Lin, M., Lin, S., Litwin, M., Lopez, T., Lowe, R., Lue, P., Makanju, A., Malfacini, K., Manning, S., Markov, T., Markovski, Y., Martin, B., Mayer, K., Mayne, A., McGrew, B., McKinney, S.M., McLeavey, C., McMillan, P., McNeil, J., Medina, D., Mehta, A., Menick, J., Metz, L., Mishchenko, A., Mishkin, P., Monaco, V., Morikawa, E., Mossing, D., Mu, T., Murati, M., Murk, O., M´ely, D., Nair, A., Nakano, R., Nayak, R., Neelakantan, A., Ngo, R., Noh, H., Ouyang, L., O'Keefe, C., Pachocki, J., Paino, A., Palermo, J., Pantuliano, A., Parascandolo, G., Parish, J., Parparita, E., Passos, A., Pavlov, M., Peng, A., Perelman, A., Avila Belbute Peres, F., Petrov, M., Oliveira Pinto, H.P., Michael, Pokorny, Pokrass, M., Pong, V.H., Powell, T., Power, A., Power, B., Proehl, E., Puri, R., Radford, A., Rae, J., Ramesh, A., Raymond, C., Real, F., Rimbach, K., Ross, C., Rotsted, B., Roussez, H., Ryder, N., Saltarelli, M., Sanders, T., Santurkar, S., Sastry, G., Schmidt, H., Schnurr, D., Schulman, J., Selsam, D., Sheppard, K., Sherbakov, T., Shieh, J., Shoker, S., Shyam, P., Sidor, S., Sigler, E., Simens, M., Sitkin, J., Slama, K., Sohl, I., Sokolowsky, B., Song, Y., Staudacher, N., Such, F.P., Summers, N., Sutskever, I., Tang, J., Tezak, N., Thompson, M.B., Tillet, P., Tootoonchian, A., Tseng, E., Tuggle, P., Turley, N., Tworek, J., Uribe, J.F.C., Vallone, A., Vijayvergiya, A., Voss, C., Wainwright, C., Wang, J.J., Wang, A., Wang, B., Ward, J., Wei, J., Weinmann, C., Welihinda, A., Welinder, P., Weng, J., Weng, L., Wiethoff, M., Willner, D., Winter, C., Wolrich, S., Wong, H., Workman, L., Wu, S., Wu, J., Wu, M., Xiao, K., Xu, T., Yoo, S., Yu, K., Yuan, Q., Zaremba, W., Zellers, R., Zhang, C., Zhang, M., Zhao, S., Zheng, T., Zhuang, J., Zhuk, W., Zoph, B.: GPT-4 Technical Report (2024). <https://arxiv.org/abs/2303.08774>

<a id="ref-69-1"></a>O'Brien, D.T.: Thinking, fast and slow by daniel kahneman. (2012)

*   <a id="ref-69-3"></a>Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C., Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A., et al.: Training language models to follow instructions with human feedback. Advances in neural information processing systems 35, 27730–27744 (2022)
*   <a id="ref-69-0"></a>Pressman, S.M., Borna, S., Gomez-Cabello, C.A., Haider, S.A., Haider, C.R., Forte, A.J.: Clinical and surgical applications of large language models: A systematic review. Journal of Clinical Medicine 13(11), 3041 (2024) [https://doi.org/10.3390/jcm13113041](https://doi.org/10.3390/jcm13113041)
*   <a id="ref-69-2"></a>Pad´o, S., Cer, D., Galley, M., Jurafsky, D., Manning, C.D.: Measuring machine translation quality as semantic equivalence: A metric based on entailment features. Machine Translation 23, 181–193 (2009)

*   <a id="ref-70-10"></a>Penkov, S.: Mitigating hallucinations in large language models via semantic enrichment of prompts: Insights from biobert and ontological integration. In: Proceedings of the Sixth International Conference on Computational Linguistics in Bulgaria (CLIB 2024), pp. 272–276 (2024)
*   <a id="ref-70-7"></a>Pan, L., Saxon, M., Xu, W., Nathani, D., Wang, X., Wang, W.Y.: Automatically correcting large language models: Surveying the landscape of diverse self-correction strategies. arXiv preprint arXiv:2308.03188 (2023)
*   <a id="ref-70-2"></a>Pal, A., Umapathi, L.K., Sankarasubbu, M.: Medmcqa: A large-scale multi-subject multi-choice dataset for medical domain question answering. In: Conference on Health, Inference, and Learning, pp. 248–260 (2022). PMLR
*   <a id="ref-70-0"></a>Pal, A., Umapathi, L.K., Sankarasubbu, M.: Med-halt: Medical domain hallucination test for large language models. arXiv preprint arXiv:2307.15343 (2023)
*   <a id="ref-70-5"></a>Peng, C., Yang, X., Chen, A., Smith, K.E., PourNejatian, N., Costa, A.B., Martin, C., Flores, M.G., Zhang, Y., Magoc, T., Lipori, G., Mitchell, D.A., Ospina, N.S., Ahmed, M.M., Hogan, W.R., Shenkman, E.A., Guo, Y., Bian, J., Wu, Y.: A study of generative large language model for medical research and healthcare. npj Digital Medicine 6(1) (2023) <https://doi.org/10.1038/s41746-023-00958-w>
*   <a id="ref-70-8"></a>Rodriguez, J.A., Alsentzer, E., Bates, D.W.: Leveraging large language models to foster equity in healthcare. Journal of the American Medical Informatics Association, 055 (2024)
*   <a id="ref-70-9"></a>Rodman, A., Buckley, T.A., Manrai, A.K., Morgan, D.J.: Artificial intelligence vs. clinician performance in estimating probabilities of diagnoses before and after testing. JAMA Network Open 6(12), 2347075 (2023) [https://doi.org/10.1001/jamanetworkopen.2023.47075](https://doi.org/10.1001/jamanetworkopen.2023.47075)
*   <a id="ref-70-11"></a>Reddy, S.: Generative ai in healthcare: an implementation science informed translational path on application, integration and governance. Implementation Science 19(1), 27 (2024)
*   <a id="ref-70-3"></a>Rehana, R.W., Huda, N.: A common heuristic in medicine: anchoring. Ann Med Health Sci Res 11, 1461–1463 (2021)
*   <a id="ref-70-1"></a>Rawte, V., Sheth, A., Das, A.: A survey of hallucination in large foundation models. arXiv preprint arXiv:2309.05922 (2023)
*   <a id="ref-70-6"></a>Rafailov, R., Sharma, A., Mitchell, E., Manning, C.D., Ermon, S., Finn, C.: Direct preference optimization: Your language model is secretly a reward model. Advances in Neural Information Processing Systems 36 (2024)
*   <a id="ref-70-4"></a>Restrepo, D., Wu, C., V´asquez-Venegas, C., Matos, J., Gallifant, J., Filipe, L.: Analyzing diversity in healthcare llm research: A scientometric perspective. arXiv preprint arXiv:2406.13152 (2024)

*   <a id="ref-71-1"></a>Singhal, K., Azizi, S., Tu, T., Mahdavi, S.S., Wei, J., Chung, H.W., Scales, N., Tanwani, A., Cole-Lewis, H., Pfohl, S., et al.: Large language models encode clinical knowledge. arXiv preprint arXiv:2212.13138 (2022)
*   <a id="ref-71-0"></a>Singhal, K., Azizi, S., Tu, T., Mahdavi, S.S., Wei, J., Chung, H.W., Scales, N., Tanwani, A., Cole-Lewis, H., Pfohl, S., et al.: Large language models encode clinical knowledge. Nature 620(7972), 172–180 (2023)
*   <a id="ref-71-6"></a>Scialom, T., Dray, P.-A., Lamprier, S., Piwowarski, B., Staiano, J., Wang, A., Gallinari, P.: Questeval: Summarization asks for fact-based evaluation. In: 2021 Conference on Empirical Methods in Natural Language Processing, pp. 6594–6604 (2021). Association for Computational Linguistics
*   <a id="ref-71-4"></a>Svenstrup, D., Jørgensen, H.L., Winther, O.: Rare disease diagnosis: a review of web search, social media and large-scale data-mining approaches. Rare Diseases 3(1), 1083145 (2015)
*   <a id="ref-71-5"></a>Scialom, T., Lamprier, S., Piwowarski, B., Staiano, J.: Answers unite! unsupervised metrics for reinforced summarization models. In: Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), pp. 3246– 3256 (2019)
*   <a id="ref-71-3"></a>Shekelle, P.G., Ortiz, E., Rhodes, S., Morton, S.C., Eccles, M.P., Grimshaw, J.M., Woolf, S.H.: Developing clinical guidelines. Western Journal of Medicine 176(6), 326 (2002)
*   <a id="ref-71-9"></a>Srivastava, A., Rastogi, A., Rao, A., Abid, A., Aslanides, J., Callison-Burch, C., Clark, C., Conerly, T., Das, D., Dey, K., et al.: Beyond the imitation game: Quantifying and extrapolating the capabilities of language models. arXiv preprint arXiv:2206.04615 (2022)
*   <a id="ref-71-2"></a>Saposnik, G., Redelmeier, D., Ruff, C.C., Tobler, P.N.: Cognitive biases associated with medical decisions: A systematic review. BMC Medical Informatics and Decision Making 16, 138 (2016) <https://doi.org/10.1186/s12911-016-0377-1>
*   <a id="ref-71-8"></a>Sun, Z., Shen, S., Cao, S., Liu, H., Li, C., Shen, Y., Gan, C., Gui, L.-Y., Wang, Y.-X., Yang, Y., et al.: Aligning large multimodal models with factually augmented rlhf. arXiv preprint arXiv:2309.14525 (2023)
*   <a id="ref-71-7"></a>Singhal, K., Tu, T., Gottweis, J., Sayres, R., Wulczyn, E., Hou, L., Clark, K., Pfohl, S., Cole-Lewis, H., Neal, D., Schaekermann, M., Wang, A., Amin, M., Lachgar, S., Mansfield, P., Prakash, S., Green, B., Dominowska, E., Arcas, B.A., Tomasev, N., Liu, Y., Wong, R., Semturs, C., Mahdavi, S.S., Barral, J., Webster, D., Corrado, G.S., Matias, Y., Azizi, S., Karthikesalingam, A., Natarajan, V.: Towards Expert-Level Medical Question Answering with Large Language Models (2023). [https://arxiv.org/abs/2305.09617](https://arxiv.org/abs/2305.09617)

*   <a id="ref-72-8"></a>Steyvers, M., Tejeda, H., Kumar, A., Belem, C., Karny, S., Hu, X., Mayer, L., Smyth, P.: The calibration gap between model and human confidence in large language models. arXiv preprint arXiv:2401.13835 (2024)
*   <a id="ref-72-0"></a>Saab, K., Tu, T., Weng, W.-H., Tanno, R., Stutz, D., Wulczyn, E., Zhang, F., Strother, T., Park, C., Vedadi, E., Chaves, J.Z., Hu, S.-Y., Schaekermann, M., Kamath, A., Cheng, Y., Barrett, D.G.T., Cheung, C., Mustafa, B., Palepu, A., McDuff, D., Hou, L., Golany, T., Liu, L., Alayrac, J.-b., Houlsby, N., Tomasev, N., Freyberg, J., Lau, C., Kemp, J., Lai, J., Azizi, S., Kanada, K., Man, S., Kulkarni, K., Sun, R., Shakeri, S., He, L., Caine, B., Webson, A., Latysheva, N., Johnson, M., Mansfield, P., Lu, J., Rivlin, E., Anderson, J., Green, B., Wong, R., Krause, J., Shlens, J., Dean, J., Hassabis, D., Matias, Y., Webster, D., Barral, J., Corrado, G., Semturs, C., Mahdavi, S.S., Gottweis, J., Karthikesalingam, A., Natarajan, V.: Capabilities of Gemini Models in Medicine (2024). <https://arxiv.org/abs/2404.18416>
*   <a id="ref-72-3"></a>Saab, K., Tu, T., Weng, W.-H., Tanno, R., Stutz, D., Wulczyn, E., Zhang, F., Strother, T., Park, C., Vedadi, E., et al.: Capabilities of gemini models in medicine. arXiv preprint arXiv:2404.18416 (2024)
*   <a id="ref-72-5"></a>Schulman, J., Wolski, F., Dhariwal, P., Radford, A., Klimov, O.: Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347 (2017)
*   <a id="ref-72-7"></a>Savage, T., Wang, J., Gallo, R., Boukil, A., Patel, V., Safavi-Naini, S.A., Soroush, A., Chen, J.H.: Large language model uncertainty proxies: Discrimination and calibration for medical diagnosis and treatment. Journal of the American Medical Informatics Association 31(10), 254 (2024) <https://doi.org/10.1093/jamia/ocae254>
*   <a id="ref-72-1"></a>Sun, Y., Yin, Z., Guo, Q., Wu, J., Qiu, X., Zhao, H.: Benchmarking Hallucination in Large Language Models based on Unanswerable Math Word Problem (2024). <https://arxiv.org/abs/2403.03558>
*   <a id="ref-72-4"></a>Sambara, S., Zhang, S., Banerjee, O., Acosta, J., Fahrner, J., Rajpurkar, P.: Radflag: A black-box hallucination detection method for medical vision language models. arXiv preprint arXiv:2411.00299 (2024)
*   <a id="ref-72-2"></a>Szolovits, P.: Large Language Models Seem Miraculous, but Science Abhors Miracles. Massachusetts Medical Society (2024)
*   <a id="ref-72-6"></a>Shi, X., Zhu, Z., Zhang, Z., Li, C.: Hallucination mitigation in natural language generation from large-scale open-domain knowledge graphs. In: Bouamor, H., Pino, J., Bali, K. (eds.) Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pp. 12506–12521. Association for Computational Linguistics, Singapore (2023). <https://doi.org/10.18653/v1/2023.emnlp-main.770>. <https://aclanthology.org/2023.emnlp-main.770>

*   <a id="ref-73-9"></a>The White House Office of Science and Technology Policy: Blueprint for an AI Bill of Rights. Accessed: 2024-11-04 (2022). [https://www.whitehouse.gov/ostp/ai-bill-of-rights/](https://www.whitehouse.gov/ostp/ai-bill-of-rights/)
*   <a id="ref-73-3"></a>Tversky, A., Kahneman, D.: Judgment under uncertainty: Heuristics and biases: Biases in judgments reveal some heuristics of thinking under uncertainty. Science 185(4157), 1124–1131 (1974) <https://doi.org/10.1126/science.185.4157.1124>
*   <a id="ref-73-4"></a>Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M.-A., Lacroix, T., Rozi`ere, B., Goyal, N., Hambro, E., Azhar, F., Rodriguez, A., Joulin, A., Grave, E., Lample, G.: LLaMA: Open and Efficient Foundation Language Models (2023). <https://arxiv.org/abs/2302.13971>
*   <a id="ref-73-5"></a>Tian, K., Mitchell, E., Yao, H., Manning, C.D., Finn, C.: Fine-tuning language models for factuality. arXiv preprint arXiv:2311.08401 (2023)
*   <a id="ref-73-6"></a>Tian, K., Mitchell, E., Zhou, A., Sharma, A., Rafailov, R., Yao, H., Finn, C., Manning, C.D.: Just ask for calibration: Strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback. arXiv preprint arXiv:2305.14975 (2023)
*   <a id="ref-73-2"></a>Topol, E.J.: High-performance medicine: the convergence of human and artificial intelligence. Nature medicine 25(1), 44–56 (2019)
*   <a id="ref-73-7"></a>Tjandra, B.A., Razzak, M., Kossen, J., Handa, K., Gal, Y.: Fine-tuning large language models to appropriately abstain with semantic entropy. arXiv preprint arXiv:2410.12345 (2024)
*   <a id="ref-73-8"></a>Tsiaras, S.V., Safi, L.M., Ghoshhajra, B.B., Lindsay, M.E., Wood, M.J.: Case 39-2017: A 41-year-old woman with recurrent chest pain. New England Journal of Medicine 377(25), 2475–2484 (2017)
*   <a id="ref-73-1"></a>Tonmoy, S., Zaman, S., Jain, V., Rani, A., Rawte, V., Chadha, A., Das, A.: A comprehensive survey of hallucination mitigation techniques in large language models. arXiv preprint arXiv:2401.01313 (2024)
*   <a id="ref-73-0"></a>Umapathi, L.K., Pal, A., Sankarasubbu, M.: Med-halt: Medical domain hallucination test for large language models. arXiv preprint arXiv:2307.15343 (2023)
*   <a id="ref-73-10"></a>U.S. Department of Health and Human Services: Breach Notification Rule. Accessed: 2024-11-04 (2024). [https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html](https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html)

*   <a id="ref-74-4"></a>U.S. Department of Health and Human Services: Health Information Privacy. Accessed: 2024-11-04 (2024). [https://www.hhs.gov/hipaa/for-professionals/privacy/index.html](https://www.hhs.gov/hipaa/for-professionals/privacy/index.html)
*   <a id="ref-74-3"></a>U.S. Department of Health and Human Services: Health Information Privacy: Laws & Regulations. [https://www.hhs.gov/hipaa/for-professionals/privacy/laws-regulations/index.html](https://www.hhs.gov/hipaa/for-professionals/privacy/laws-regulations/index.html). Accessed on November 4, 2024 (2024)
*   <a id="ref-74-5"></a>U.S. Department of Health and Human Services: Health Information Security. Accessed: 2024-11-04 (2024). [https://www.hhs.gov/hipaa/for-professionals/security/index.html](https://www.hhs.gov/hipaa/for-professionals/security/index.html)
*   <a id="ref-74-8"></a>U.S. Food and Drug Administration: 510(k) Clearances. Accessed: 2024-11- 04 (2024). [https://www.fda.gov/medical-devices/device-approvals-and-clearances/510k-clearances](https://www.fda.gov/medical-devices/device-approvals-and-clearances/510k-clearances)
*   <a id="ref-74-9"></a>U.S. Food and Drug Administration: Good Machine Learning Practice for Medical Device Development: Guiding Principles. Accessed: 2024-11-04 (2024). [https://www.fda.gov/medical-devices/software-medical-device-samd/good-machine-learning-practice-medical-device-development-guiding-principles](https://www.fda.gov/medical-devices/software-medical-device-samd/good-machine-learning-practice-medical-device-development-guiding-principles)
*   <a id="ref-74-10"></a>U.S. Food and Drug Administration: Marketing Submission Recommendations for a Predetermined Change Control Plan for Artificial Intelligence. [https://www.fda.gov/regulatory-information/search-fda-guidance-documents/marketing-submission-recommendations-predetermined-change-control-plan-artificial-intelligence](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/marketing-submission-recommendations-predetermined-change-control-plan-artificial-intelligence). Accessed: 2024-12-09 (2024)
*   <a id="ref-74-7"></a>U.S. Food and Drug Administration: Premarket Approval (PMA). Accessed: 2024-11-04 (2024). [https://www.fda.gov/medical-devices/premarket-submissions-selecting-and-preparing-correct-submission/premarket-approval-pma](https://www.fda.gov/medical-devices/premarket-submissions-selecting-and-preparing-correct-submission/premarket-approval-pma)
*   <a id="ref-74-6"></a>U.S. Food and Drug Administration: Software as a Medical Device (SaMD). Accessed: 2024-11-04 (2024). [https://www.fda.gov/medical-devices/digital-health-center-excellence/software-medical-device-samd](https://www.fda.gov/medical-devices/digital-health-center-excellence/software-medical-device-samd)
*   <a id="ref-74-2"></a>Vasquez, C.D., Albeck, J.G.: Modeling elucidates context dependence in adipose regulation. Cell Systems (2023) <https://doi.org/10.1016/j.cels.2023.11.008>
*   <a id="ref-74-0"></a>Vally, Z.I., Khammissa, R.A.G., Feller, G., Ballyram, R., Beetge, M., Feller, L.: Errors in clinical diagnosis: a narrative review. The Journal of International Medical Research 51(8), 3000605231162798 (2023) [https://doi.org/10.1177/03000605231162798](https://doi.org/10.1177/03000605231162798)
*   <a id="ref-74-1"></a>Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser, L., Polosukhin, I.: Attention is all you need. arXiv preprint arXiv:1706.03762 (2017)

*   <a id="ref-75-0"></a>Vishwanath, P.R., Tiwari, S., Naik, T.G., Gupta, S., Thai, D.N., Zhao, W., KWON, S., Ardulov, V., Tarabishy, K., McCallum, A., et al.: Faithfulness hallucination detection in healthcare ai. In: Artificial Intelligence and Data Science for Healthcare: Bridging Data-Centric AI and People-Centric Healthcare (2024)
*   <a id="ref-75-2"></a>Willems, R., Annemans, L., Siopis, G., Moschonis, G., Vedanthan, R., Jung, J., Kwasnicka, D., Oldenburg, B., d'Antonio, C., Girolami, S., Agapidaki, E., Manios, Y., Verhaeghe, N., 4You, D.: Cost effectiveness review of text messaging, smartphone application, and website interventions targeting t2dm or hypertension. npj Digital Medicine 6 (2023) <https://doi.org/10.1038/s41746-023-00876-x>
*   <a id="ref-75-4"></a>Wang, A., Cho, K., Lewis, M.: Asking and answering questions to evaluate the factual consistency of summaries. In: Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pp. 5008–5020 (2020)
*   <a id="ref-75-3"></a>Wang, Z., Danek, B., Yang, Z., Chen, Z., Sun, J.: Can large language models replace data scientists in clinical research? arXiv preprint arXiv:2410.21591 (2024)
*   <a id="ref-75-1"></a>Wu, J., Kim, Y., Keller, E.C., Chow, J., Levine, A.P., Pontikos, N., Ibrahim, Z., Taylor, P., Williams, M.C., Wu, H.: Exploring multimodal large language models for radiology report error-checking. arXiv preprint arXiv:2312.13103 (2023)
*   <a id="ref-75-11"></a>Wu, J., Kim, Y., Wu, H.: Hallucination benchmark in medical visual question answering. arXiv preprint arXiv:2401.05827 (2024)
*   <a id="ref-75-10"></a>Wang, S., Lin, M., Ghosal, T., Ding, Y., Peng, Y.: Knowledge graph applications in medical imaging analysis: a scoping review. Health data science 2022, 9841548 (2022)
*   <a id="ref-75-7"></a>Wang, H., Liu, C., Xi, N., Qiang, Z., Zhao, S., Qin, B., Liu, T.: Huatuo: Tuning llama model with chinese medical knowledge. arXiv preprint arXiv:2304.06975 (2023)
*   <a id="ref-75-8"></a>Wang, D., Liang, J., Ye, J., Li, J., Li, J., Zhang, Q., Hu, Q., Pan, C., Wang, D., Liu, Z., et al.: Enhancement of the performance of large language models in diabetes education through retrieval-augmented generation: Comparative study. Journal of Medical Internet Research 26, 58041 (2024)
*   <a id="ref-75-6"></a>Wu, C., Lin, W., Zhang, X., Zhang, Y., Xie, W., Wang, Y.: Pmc-llama: toward building open-source language models for medicine. Journal of the American Medical Informatics Association, 045 (2024)
*   <a id="ref-75-5"></a>Wen, B., Norel, R., Liu, J., Stappenbeck, T., Zulkernine, F., Chen, H.: Leveraging large language models for patient engagement: The power of conversational ai in digital health. arXiv preprint arXiv:2406.13659 (2024)
*   <a id="ref-75-9"></a>Wang, C., Ong, J., Wang, C., Ong, H., Cheng, R., Ong, D.: Potential for gpt technology to optimize future clinical decision-making using retrieval-augmented generation. Annals of Biomedical Engineering 52(5), 1115–1118 (2024)

*   <a id="ref-76-8"></a>Whitehead, S., Petryk, S., Shakib, V., Gonzalez, J., Darrell, T., Rohrbach, A., Rohrbach, M.: Reliable visual question answering: Abstain rather than answer incorrectly. In: European Conference on Computer Vision, pp. 148–166 (2022). Springer
*   <a id="ref-76-1"></a>Wu, K., Wu, E., Cassasola, A., Zhang, A., Wei, K., Nguyen, T., Riantawan, S., Riantawan, P.S., Ho, D.E., Zou, J.: How well do llms cite relevant medical references? an evaluation framework and analyses. arXiv preprint arXiv:2402.02008 (2024)
*   <a id="ref-76-11"></a>Walley, A.Y., Wakeman, S.E., Eng, G.: Case 6-2019: A 29-year-old woman with nausea, vomiting, and diarrhea. New England Journal of Medicine 380(8), 772–779 (2019)
*   <a id="ref-76-7"></a>Wan, A., Wallace, E., Klein, D.: What evidence do language models find convincing? arXiv preprint arXiv:2402.11782 (2024)
*   <a id="ref-76-2"></a>Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., Le, Q.V., Zhou, D., et al.: Chain-of-thought prompting elicits reasoning in large language models. Advances in neural information processing systems 35, 24824–24837 (2022)
*   <a id="ref-76-10"></a>Wang, G., Xie, Y., Jiang, Y., Mandlekar, A., Xiao, C., Zhu, Y., Fan, L., Anandkumar, A.: Voyager: An open-ended embodied agent with large language models. arXiv preprint arXiv:2305.16291 (2023)
*   <a id="ref-76-9"></a>Wen, B., Yao, J., Feng, S., Xu, C., Tsvetkov, Y., Howe, B., Wang, L.L.: Know your limits: A survey of abstention in large language models. arXiv preprint arXiv:2407.18418 (2024)
*   <a id="ref-76-0"></a>Wang, R., Yang, Z., Zhao, Z., Tong, X., Hong, Z., Qian, K.: Llm-based robot task planning with exceptional handling for general purpose service robots. In: 2024 43rd Chinese Control Conference (CCC), pp. 4439–4444 (2024). IEEE
*   <a id="ref-76-4"></a>Wang, D., Zhang, S.: Large language models in healthcare and medical domain: A review. Artificial Intelligence Review 57, 299 (2024)
*   <a id="ref-76-3"></a>Wang, D., Zhang, S.: Large language models in medical and healthcare fields: applications, advances, and challenges. Artificial Intelligence Review 57, 299 (2024)
*   <a id="ref-76-5"></a>Xiong, G., Jin, Q., Lu, Z., Zhang, A.: Benchmarking retrieval-augmented generation for medicine. In: Ku, L.-W., Martins, A., Srikumar, V. (eds.) Findings of the Association for Computational Linguistics: ACL 2024, pp. 6233–6251. Association for Computational Linguistics, Bangkok, Thailand (2024). [https://doi.org/10.18653/v1/2024.findings-acl.372](https://doi.org/10.18653/v1/2024.findings-acl.372). <https://aclanthology.org/2024.findings-acl.372>

<a id="ref-76-6"></a>Xiong, G., Jin, Q., Lu, Z., Zhang, A.: Benchmarking retrieval-augmented generation for medicine. In: Ku, L.-W., Martins, A., Srikumar, V. (eds.) Findings of the Association for Computational Linguistics: ACL 2024, pp. 6233–6251. Association for Computational Linguistics, Bangkok, Thailand (2024). [https://doi.org/10.18653/v1/2024.findings-acl.372](https://doi.org/10.18653/v1/2024.findings-acl.372). <https://aclanthology.org/2024.findings-acl.372/>

*   <a id="ref-77-5"></a>Xiong, G., Jin, Q., Wang, X., Zhang, M., Lu, Z., Zhang, A.: Improving retrievalaugmented generation in medicine with iterative follow-up questions. In: Biocomputing 2025: Proceedings of the Pacific Symposium, pp. 199–214 (2024). World Scientific
*   <a id="ref-77-0"></a>Xia, W., Li, D., He, W., Pickhardt, P.J., Jian, J., Zhang, R., Zhang, J., Song, R., Tong, T., Yang, X., Gao, X., Cui, Y.: Multicenter evaluation of a weakly supervised deep learning model for lymph node diagnosis in rectal cancer at mri. Radiology: Artificial Intelligence (2024) <https://doi.org/10.1148/ryai.230152>
*   <a id="ref-77-6"></a>Xu, R., Qi, Z., Guo, Z., Wang, C., Wang, H., Zhang, Y., Xu, W.: Knowledge conflicts for llms: A survey. arXiv preprint arXiv:2403.08319 (2024)
*   <a id="ref-77-3"></a>Xia, F., Yetisgen-Yildiz, M.: Clinical corpus annotation: challenges and strategies. In: Proceedings of the Third Workshop on Building and Evaluating Resources for Biomedical Text Mining (BioTxtM'2012) in Conjunction with the International Conference on Language Resources and Evaluation (LREC), Istanbul, Turkey, pp. 21–27 (2012)
*   <a id="ref-77-8"></a>Xie, J., Zhang, K., Chen, J., Lou, R., Su, Y.: Adaptive chameleon or stubborn sloth: Unraveling the behavior of large language models in knowledge conflicts. arXiv preprint arXiv:2305.13300 (2023)
*   <a id="ref-77-7"></a>Xie, S.M., Zhang, M., Huang, M., Shi, R., Guo, L., Peng, C., Yan, P., Zhou, Y., Qiu, X.: Calibrating the confidence of large language models by eliciting fidelity. In: Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP) (2024). [https://doi.org/10.18653/v1/2024.emnlp-main.173](https://doi.org/10.18653/v1/2024.emnlp-main.173). Association for Computational Linguistics
*   <a id="ref-77-4"></a>Xu, D., Zhang, Z., Zhu, Z., Lin, Z., Liu, Q., Wu, X., Xu, T., Wang, W., Ye, Y., Zhao, X., et al.: Editing factual knowledge and explanatory ability of medical large language models. In: Proceedings of the 33rd ACM International Conference on Information and Knowledge Management, pp. 2660–2670 (2024)
*   <a id="ref-77-1"></a>Xu, D., Zhang, Z., Zhu, Z., Lin, Z., Liu, Q., Wu, X., Xu, T., Zhao, X., Zheng, Y., Chen, E.: Mitigating hallucinations of large language models in medical information extraction via contrastive decoding. arXiv preprint arXiv:2410.15702 (2024)
*   <a id="ref-77-2"></a>Xu, H., Zhu, Z., Zhang, S., Ma, D., Fan, S., Chen, L., Yu, K.: Rejection improves reliability: Training LLMs to refuse unknown questions using RL from knowledge feedback. In: First Conference on Language Modeling (2024). [https://openreview.net/forum?id=lJMioZBoR8](https://openreview.net/forum?id=lJMioZBoR8)

*   <a id="ref-78-3"></a>Yu, L., Cao, M., Cheung, J.C.K., Dong, Y.: Mechanistic understanding and mitigation of language model non-factual hallucinations. arXiv preprint arXiv:2403.18167 (2024)
*   <a id="ref-78-8"></a>Yang, C., Cui, H., Lu, J., Wang, S., Xu, R., Ma, W., Yu, Y., Yu, S., Kan, X., Ling, C., et al.: A review on knowledge graphs for healthcare: Resources, applications, and promises. arXiv preprint arXiv:2306.04802 (2023)
*   <a id="ref-78-6"></a>Yogatama, D., Masson d'Autume, C., Kong, L.: Adaptive semiparametric language models. Transactions of the Association for Computational Linguistics 9, 362–373 (2021)
*   <a id="ref-78-0"></a>Yao, Z., Kantu, N.S., Wei, G., Tran, H., Duan, Z., Kwon, S., Yang, Z., Yu, H., et al.: Readme: Bridging medical jargon and lay understanding for patient education through data-centric nlp. arXiv preprint arXiv:2312.15561 (2023)
*   <a id="ref-78-5"></a>Yuan, J., Tang, R., Jiang, X., Hu, X.: Large Language Models for Healthcare Data Augmentation: An Example on Patient-Trial Matching (2023)
*   <a id="ref-78-9"></a>Yu, G., Tabatabaei, M., Mezei, J., Zhong, Q., Chen, S., Li, Z., Li, J., Shu, L., Shu, Q.: Improving chronic disease management for children with knowledge graphs and artificial intelligence. Expert Systems with Applications 201, 117026 (2022)
*   <a id="ref-78-10"></a>Yu, J., Wang, X., Tu, S., Cao, S., Zhang-Li, D., Lv, X., Peng, H., Yao, Z., Zhang, X., Li, H., et al.: Kola: Carefully benchmarking world knowledge of large language models. arXiv preprint arXiv:2306.09296 (2023)
*   <a id="ref-78-11"></a>Yang, F., Zhang, Y., Chen, H., Li, M., Zhang, Y., Wang, L.: Confidence-aware learning for large language models. arXiv preprint arXiv:2401.12345 (2024)
*   <a id="ref-78-4"></a>Yuan, W., Zhang, Y., Fu, L., Wang, Y., Wang, W.Y.: Hallucinations in large language models: A survey. arXiv preprint arXiv:2306.14433 (2023)
*   <a id="ref-78-7"></a>Yu, H., Zhou, J., Li, L., Chen, S., Gallifant, J., Shi, A., Li, X., Hua, W., Jin, M., Chen, G., et al.: Aipatient: Simulating patients with ehrs and llm powered agentic workflow. arXiv preprint arXiv:2409.18924 (2024)
*   <a id="ref-78-1"></a>Zhou, K., Hwang, J.D., Ren, X., Dziri, N., Jurafsky, D., Sap, M.: Rel-a.i.: An interaction-centered approach to measuring human-lm reliance. In: NAACL (2025). <https://arxiv.org/abs/2407.07950>
*   <a id="ref-78-12"></a>Zuo, K., Jiang, Y.: Medhallbench: A new benchmark for assessing hallucination in medical large language models. arXiv preprint arXiv:2412.18947 (2024)
*   <a id="ref-78-2"></a>Zhang, Y., Li, S., Liu, J., Yu, P., Fung, Y.R., Li, J., Li, M., Ji, H.: Knowledge overshadowing causes amalgamated hallucination in large language models. arXiv preprint arXiv:2407.08039 (2024)

*   <a id="ref-79-4"></a>Zheng, M., Pei, J., Logeswaran, L., Lee, M., Jurgens, D.: When "a helpful assistant" is not really helpful: Personas in system prompts do not improve performances of large language models. In: Al-Onaizan, Y., Bansal, M., Chen, Y.-N. (eds.) Findings of the Association for Computational Linguistics: EMNLP 2024, pp. 15126– 15154. Association for Computational Linguistics, Miami, Florida, USA (2024). [https://aclanthology.org/2024.findings-emnlp.888/](https://aclanthology.org/2024.findings-emnlp.888/)
*   <a id="ref-79-2"></a>Zhang, T., Qiu, L., Guo, Q., Deng, C., Zhang, Y., Zhang, Z., Zhou, C., Wang, X., Fu, L.: Enhancing uncertainty-based hallucination detection with stronger focus. In: Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pp. 915–932 (2023)
*   <a id="ref-79-0"></a>Ziaei, R., Schmidgall, S.: Language models are susceptible to incorrect patient selfdiagnosis in medical applications. arXiv preprint arXiv:2309.09362 (2023)
*   <a id="ref-79-1"></a>Zhang, A., Yuksekgonul, M., Guild, J., Zou, J., Wu, J.C.: Chatgpt exhibits gender and racial biases in acute coronary syndrome management. arXiv preprint arXiv:2311.14703 (2023)
*   <a id="ref-79-3"></a>Zhang, N., Yao, Y., Tian, B., Wang, P., Deng, S., Wang, M., Xi, Z., Mao, S., Zhang, J., Ni, Y., et al.: A comprehensive study of knowledge editing for large language models. arXiv preprint arXiv:2401.01286 (2024)

## <a id="page-80-0"></a>Appendix A Survey Details

## <a id="page-80-1"></a>A.1 Survey Questions: Understanding LLM Hallucinations in Research and Healthcare

## <a id="page-80-2"></a>A.1.1 Basic Information

*   1. What is your primary field of work