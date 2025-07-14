---
cite_key: yue_2023
title: MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI
authors: Xiang Yue, Yuansheng Ni, Kai Zhang, Tianyu Zheng, Ruoqi Liu, Ge Zhang, Samuel Stevens, Dongfu Jiang, Weiming Ren, Yuxuan Sun, Cong Wei, Botao Yu, Ruibin Yuan, Renliang Sun, Ming Yin, Boyuan Zheng, Zhenzhu Yang, Yibo Liu, Wenhao Huang, Huan Sun, Yu Su, Wenhu Chen
year: 2023
date_processed: 2025-07-02
phase2_processed: true
original_folder: arxiv_2311.16502_MMMU_A_Massive_Multi-discipline_Multimodal_Understanding_and_Reasoning_Benchmark_for_Expert_AGI
images_total: 123
images_kept: 84
images_removed: 39
tags: 
keywords: 
---

# MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI

Xiang Yue\*† , Yuansheng Ni\*, Kai Zhang\*, Tianyu Zheng\*, Ruoqi Liu, ^2^Ge Zhang, ^3^Samuel Stevens, ^2^Dongfu Jiang, ^2^Weiming Ren, ^4^Yuxuan Sun, Cong Wei, ^3^Botao Yu, ^5^Ruibin Yuan, ^2^Renliang Sun, ^7^Ming Yin, Boyuan Zheng, ^4^Zhenzhu Yang, ^6^Yibo Liu, ^4^Wenhao Huang, Huan Sun\*, ^3^Yu Su\*† , Wenhu Chen\*†

1 IN.AI Research, ^2^University of Waterloo, ^3^The Ohio State University, ^4^ Independent, ^5^Carnegie Mellon University, ^6^University of Victoria, ^7^Princeton University

![](_page_0_Figure_4.jpeg)

Figure 1. Overview of the MMMU dataset. MMMU presents four challenges: 1) comprehensiveness: 11.5K college-level problems across six broad disciplines and 30 college subjects; 2) highly heterogeneous image types; 3) interleaved text and images; 4) expert-level perception and reasoning rooted in deep subject knowledge.

## Abstract

**We introduce:** MMMU*: a new benchmark designed to evaluate multimodal models on massive multi-discipline tasks demanding college-level subject knowledge and deliberate reasoning.*MMMU*includes 11.5K meticulously collected multimodal questions from college exams, quizzes, and textbooks, covering six core disciplines: Art & Design, Business, Science, Health & Medicine, Humanities & Social Science, and Tech & Engineering. These questions span 30 subjects and 183 subfields, comprising 30 highly heterogeneous image types, such as charts, diagrams, maps, tables, music sheets, and chemical structures. Unlike existing benchmarks,*MMMU*focuses on advanced perception and reasoning with domain-specific knowledge, challenging models to perform tasks akin to those faced by experts. The evaluation of 28 open-source LMMs as well as the proprietary GPT-4V(ision) and Gemini highlights the substantial* *challenges posed by* MMMU*. Even the advanced GPT-4V and Gemini Ultra only achieve accuracies of 56% and 59% respectively, indicating significant room for improvement. We believe*MMMU*will stimulate the community to build nextgeneration multimodal foundation models towards expert artificial general intelligence.*

### Introduction

Rapid advances in large language models (LLMs) [[13]](#ref-13), [[59]](#ref-59), [[74]](#ref-74) have sparked broad discussions on the controversial concept of artificial general intelligence (AGI), often used to describe AI systems that perform on par or surpass humans at most tasks [[1]](#ref-1), [[7]](#ref-7), [[21]](#ref-21), [[32]](#ref-32), [[53]](#ref-53), [[57]](#ref-57). Candid and constructive discussions on AGI have been challenging due to a lack of shared operationalizable definitions. In an attempt to remedy this, Morris et al. [[57]](#ref-57) propose a leveled taxonomy for AGI that centers around both *generality* (or breadth) and *performance* (or depth). In the suggested taxonomy, Level 3, or *Expert AGI*, marks a critical milestone. It denotes an

\*Core Contributors. See the Author Contribution Statement for details. †B: {yue.149,su.809}@osu.edu; wenhuchen@uwaterloo.ca

![](_page_1_Figure_0.jpeg)

Figure 2. Sampled MMMU examples from each discipline. The questions and images need expert-level knowledge to understand and reason.

AI system that reaches "at least 90th percentile of skilled adults" in a broad range of tasks, thus starting to achieve "the substitution threshold for machine intelligence in lieu of human labor" for many industries, leading to significant risks of job displacement and economic disruption. Therefore, it is of both intellectual and societal importance to closely monitor the progress towards Expert AGI.

How to create benchmarks for measuring Expert AGI? Since the definition is based on comparison with *skilled adults*, a natural starting point is college-level exams for different disciplines, because those are designed to evaluate *skilled adults* specialized in each discipline. This strategy has been successfully adopted in benchmarks such as MMLU [[25]](#ref-25) and AGIEval [[92]](#ref-92), but only text-based questions are considered, while human experts are capable of solving multimodal problems. Meanwhile, large multimodal models (LMMs) that can understand both text and images have been making a major stride towards more general AI [[9]](#ref-9), [[16]](#ref-16), [[35]](#ref-35), [[44]](#ref-44), [[80]](#ref-80). These LMMs have consistently excelled in existing multimodal benchmarks [[3]](#ref-3), [[24]](#ref-24), [[33]](#ref-33), [[40]](#ref-40), [[47]](#ref-47), [[69]](#ref-69), [[83]](#ref-83), [[86]](#ref-86). For instance, CogVLM [[77]](#ref-77) achieves 85% on VQA-v2 [[24]](#ref-24), 92% on ScienceQA-IMG [[50]](#ref-50), and 93% on RefCOCO [[30]](#ref-30). However, most existing multimodal benchmarks focus on commonsense/daily knowledge rather than expert-level domain knowledge and advanced reasoning. The closest one to our goal is ScienceQA [[50]](#ref-50). While it covers diverse disciplines (breadth), the majority of the questions are at the elementary to the middle school level, thus falling short in depth for benchmarking Expert AGI.

To this end, we introduce MMMU: a comprehensive benchmark designed for college-level multi-discipline multimodal understanding and reasoning. It features problems sourced from college exams, quizzes, and textbooks spanning six common disciplines: Art & Design, Business, Science, Health & Medicine, Humanities & Social Science, and Tech & Engineering. MMMU consists of 11.5K carefully selected multimodal questions, which cover 30 diverse subjects and 183 subfields, thus meeting the breadth goal. Moreover, many problems within MMMU require expert-level reasoning, such as applying "Fourier Transform" or "Equilibrium Theory" to derive the solution, thus meeting the depth goal. MMMU also presents two unique challenges absent in current benchmarks ([Figure 1](#ref-1)). Firstly, it covers diverse image formats, from visual scenes like photographs and paintings to diagrams and tables, testing the perceptual capabilities of LMMs. Secondly, MMMU features interleaved text-image inputs. A model needs to jointly understand the images and text, which often requires recalling deep subject knowledge, and conducting complex reasoning based on the understanding and knowledge to reach a solution.

We evaluate 28 open-source LMMs as well as the advanced proprietary LMMs such as GPT-4V(ision) [[60]](#ref-60) on MMMU. Our key findings are summarized as follows:

- MMMU presents significant challenges; notably, GPT-4V only achieves an accuracy of 55.7%, indicating substantial room for improvement.
- There is a pronounced disparity in performance between open-source LMMs and GPT-4V. The highest-performing

open-source models, such as BLIP2-FLAN-T5-XXL and LLaVA-1.5, achieve approximately 34% in accuracy.

- LLMs augmented with optical character recognition (OCR) or generated captions do not see notable improvement, indicating that MMMU necessitates deeper joint interpretation of images and text.
- In disciplines such as Art & Design and Humanities & Social Science, where visual data is less complex, models exhibit higher performance. In contrast, Business, Science, Health & Medicine, and Tech & Engineering, which present more complex visual data and require intricate reasoning, see relatively lower model performance.
- Our error analysis on 150 error cases of GPT-4V reveals that 35% of errors are perceptual, 29% stem from a lack of knowledge, and 26% are due to flaws in the reasoning process. These findings underscore the challenges of the MMMU benchmark and point towards areas needing further research and model enhancement.

Our aim with MMMU is to push the boundaries of what LMMs can achieve. We believe it will prove instrumental in developing next-generation multimodal foundation models and monitoring the progress towards Expert AGI. We shall caution that MMMU is not a *sufficient* test for Expert AGI, as per the definition [[57]](#ref-57), because there lacks a direct mapping between performance on MMMU and "90th percentile of skilled adults," nor are college exams the only tasks an AGI shall tackle. However, we believe it should be *necessary* for an Expert AGI to achieve strong performance on MMMU to demonstrate their broad and deep subject knowledge as well as expert-level understanding and reasoning capabilities.

### Related Work

Multimodal Pre-Training. In recent years, rapid progress has been made in multimodal pre-training, which aims to jointly encode vision and language in a fusion model. LXMERT [[71]](#ref-71), UNITER [[10]](#ref-10), VinVL [[87]](#ref-87), Oscar [[37]](#ref-37), VilBert [[49]](#ref-49), and VLP [[93]](#ref-93) are among the earliest work to train universal vision-language models to tackle many multimodal tasks. This work relies on pre-trained visual representations like Faster RCNN features [[67]](#ref-67) to minimize the training sample complexity. Later on, CLIP [[66]](#ref-66), ALIGN [[29]](#ref-29), SimVLM [[78]](#ref-78), CoCa [[85]](#ref-85), Flamingo [[2]](#ref-2), BLIP-2 [[35]](#ref-35), and Fuyu [[6]](#ref-6) (inter alia) have been proposed to train visual representation using ViT [[18]](#ref-18) from scratch with massive amount of web data. These models have achieved great success on existing VQA and captioning tasks, which require less knowledge and reasoning.

Multimodal Instruction Tuning. Inspired by opensource instruction-tuned LLMs like FLAN-T5 [[14]](#ref-14) and Vicuna [[12]](#ref-12), models like LLaVA [[44]](#ref-44), [[45]](#ref-45) and MiniGPT-4 [[94]](#ref-94) utilized open-source resources, to improve the instructionfollowing capabilities of LMMs. The evolutionary trajectory of LMMs has also led to subsequent advancements aimed at improving the quantity and quality of visual instruction data. Models such as LLaMA-Adapter [[20]](#ref-20), [[88]](#ref-88), mPlug-OWL [[81]](#ref-81), [[82]](#ref-82), SVIT [[89]](#ref-89), LRV-Instruction [[43]](#ref-43), and InstructBLIP [[16]](#ref-16) exemplify these developments. Another pivotal aspect of LMM research revolves around multimodal in-context learning and the management of interleaved text and image examples. This area has been explored in depth by models such as Flamingo [[2]](#ref-2) and OpenFlamingo [[4]](#ref-4), Otter [[34]](#ref-34), M3IT [[36]](#ref-36), MetaVL [[56]](#ref-56), Sparkles [[26]](#ref-26), and MMICL [[90]](#ref-90). These models have significantly contributed to the ongoing advancements in multimodal training and instruction-following capabilities.

LMM Benchmarks. With the surge of multi-modal pretraining and instruction tuning, the prior single-task evaluation benchmarks like VQA [[3]](#ref-3), [[24]](#ref-24), OK-VQA [[52]](#ref-52), MSCOCO [[40]](#ref-40), GQA [[27]](#ref-27), etc., have become insufficient to holistically evaluate LMMs' general multimodal perception and reasoning abilities. Therefore, numerous all-round benchmarks have been established to assess different facets of LMMs. These benchmarks cover a wide spectrum of specific skills of LMMs, from Optical Character Recognition (OCR) as seen in the study by [[48]](#ref-48), to adversarial robustness [[91]](#ref-91) and hallucination [[15]](#ref-15), [[42]](#ref-42), e.g., POPE [[38]](#ref-38) and HaELM [[76]](#ref-76). More holistic evaluations have been conducted as well, such as LAMM [[83]](#ref-83), LVLM-eHub [[79]](#ref-79), SEED [[33]](#ref-33), MMBench [[47]](#ref-47), and MM-Vet [[86]](#ref-86). These benchmarks still largely focus on relatively basic perception abilities without requiring expert-level domain knowledge and deliberate reasoning. More recently, MathVista [[51]](#ref-51) presents a collection of visually challenging questions; however, its scope is limited exclusively to the mathematical domain. MMMU is highly different from these benchmarks by collecting more difficult expert-level problems that cover 30 different subjects and require nuanced perception, recalling domain-specific knowledge to perform stepby-step reasoning to derive the solution. In line with the motivation of our study, concurrently, GAIA [[53]](#ref-53) introduces 466 questions that test fundamental abilities of models such as reasoning, multimodality handling, or tool use.

### The MMMU Benchmark

### 1. Overview of MMMU

We introduce the Massive Multi-discipline Multimodal Understanding and Reasoning (MMMU) benchmark, a novel benchmark meticulously curated to assess the expert-level multimodal understanding capability of foundation models across a broad scope of tasks. Covering 30 subjects across 6 disciplines, including Art, Business, Health & Medicine, Science, Humanities & Social Science, and Tech & Engineering, and over 183 subfields. The detailed subject coverage and statistics are detailed in [Figure 7](#ref-7). The questions in our benchmark were manually collected by a team of

| Statistics | Number |
|---|---|
| Total Questions | 11550 |
| Total Disciplines/Subjects/Subfields | 6/30/183 |
| Image Types | 30 |
| Dev:Validation:Test | 150:900:10500 |
| Difficulties (Easy: Medium: Hard) | 28%:45%:27% |
| Multiple-choice Questions | 10861 (94.03%) |
| Open Questions | 689 (5.97%) |
| Questions with an Explanation | 2035 (17.62%) |
| Image in the Question | 11264 (97.52%) |
| * Images at the beginning | 2006 (17.81%) |
| *Images in the middle | 4159 (36.92%) |
| * Images at the end | 5679 (50.42%) |
| Image in Options | 389 (3.37%) |
| Example with Multiple Images | 854 (7.39%) |
| Average question length | 59.33 |
| Average option length | 9.17 |
| Average explanation length | 107.92 |

Table 1. Key statistics of the MMMU benchmark.

50 college students (including coauthors) from various disciplines and subjects, drawing from online sources, textbooks, and lecture materials.

MMMU, constituting 11.5K questions, is divided into a few-shot development set, a validation set, and a test set. The few-shot development set includes 5 questions per subject, and the validation set, useful for hyperparameter selection, contains approximately 900 questions, while the test set comprises 10.5K questions. MMMU is designed to measure three essential skills in LMMs: perception, knowledge, and reasoning. Our aim is to evaluate how well these models can not only perceive and understand information across different modalities but also apply reasoning with subjectspecific knowledge to derive the solution.

Our MMMU benchmark introduces four key challenges to multimodal foundation models, as detailed in [Figure 1](#ref-1). Among these, we particularly highlight the challenge stemming from the requirement for both expert-level visual perceptual abilities and deliberate reasoning with subjectspecific knowledge. This challenge is vividly illustrated through our tasks, which not only demand the processing of various heterogeneous image types but also necessitate a model's adeptness in using domain-specific knowledge to deeply understand both the text and images and to reason. This goes significantly beyond basic visual perception, calling for an advanced approach that integrates advanced multimodal analysis with domain-specific knowledge.

### 2. Data Curation Process

Data Collection. Our benchmark collection takes three stages. Firstly, we go through the common university majors to decide what subjects should be included in our benchmark. The selection is based on the principle that visual inputs should be commonly adopted in the subjects to provide valuable information. Through this principle, we rule out a few subjects like law and linguistics because it is difficult to find enough relevant multimodal problems in these subjects. Consequently, we select 30 subjects from six different disciplines. In the second stage, we recruit over 50 university students, including co-authors, specializing in these majors as annotators to assist in question collection. They collect multimodal questions from major textbooks and online resources, creating new questions based on their expertise where necessary. The annotators are instructed to adhere to copyright and license regulations, avoiding data from sites prohibiting copy and redistribution. Given the arising data contamination concerns of foundation models, the annotators are advised to select questions without immediately available answers, such as those with answers in separate documents or at the end of textbooks. This process results in a diverse collection of 13K questions from various sources. The detailed annotation protocol is in Appendix A. Data Quality Control. To further control the quality of our data, we perform two steps of data cleaning. In the first stage, lexical overlap and source URL similarity are employed to identify potential duplicate problems. These suspected duplicates were then reviewed by the authors to identify and eliminate any duplications. The second stage involves distributing the problems among different co-authors for format and typo checking. This step requires authors to ensure adherence to a standardized format, undertaking necessary corrections where deviations are found. In the third and final stage, the authors categorize the problems into four difficulty levels: very easy, easy, medium, and hard. Approximately 10% of the problems, classified as very easy and not aligning with our design criteria due to their simplistic nature, are excluded from the benchmark. This rigorous process plays a crucial role in maintaining the quality and difficulty of the problem set.

### 3. Comparisons with Existing Benchmarks

To further distinguish the difference between MMMU and other existing ones, we elaborate the benchmark details in [Figure 3](#ref-3). From the *breadth* perspective, the prior benchmarks are heavily focused on daily knowledge and common sense. The covered image format is also limited. Our benchmark aims to cover college-level knowledge with 30 image formats including diagrams, tables, charts, chemical structures, photos, paintings, geometric shapes, music sheets, medical images, etc. In the *depth* aspect, the previous benchmarks normally require commonsense knowledge or simple physical or temporal reasoning. In contrast, our benchmark requires deliberate reasoning with college-level subject knowledge.

| Depth (Reasoning) | Dataset | Size | Images | Format | Source | Answer |
|---|---|---|---|---|---|---|
| | VQA | > 1M | V | I+T | Annotated | Open |
| | GQA | > 1M | V | I+T | Synthesized | Open |
| MMMU | VisWiz | 32K | V | I+T | Annotated | Open |
| | TextVQA | 45K | OC | I+T | Annotated | MC |
| | OKVQA | 14K | V+OC | I+T | Annotated | Open |
| | SEED | 19K | V+OC | I+T | Annotated | MC |
| Breadth (Knowledge) | MMBench | 3K | V+OC | I+T | Repurposed | MC |
| | MM-Vet | 0.2K | V+OC | I+T | Annotated | Open |
| VQA<br>GQA<br>VisWiz | ScienceQA | 6K | 5 Types | I+T | Textbooks | MC |
| MMBench<br>TextVQA<br>SEED | | | | | Textbooks, | |
| OKVQA<br>MM-Vet<br>ScienceQA | MMMU | 11.5K | 30 Types | Interleaved | Internet, | MC |
| | | | | | Annotated | Open / |

Figure 3. The comparison between MMMU and other existing benchmarks. MMMU excels in both its breadth to cover a wide range of disciplines and its depth to test LMMs' reasoning abilities. In the image format, V means visual input, OC means optical characters, MC means multi-choice. Repurposed means the benchmark is a compilation of prior datasets.

### Experiments

We evaluate various models including LLMs and LMMs. In each type, we consider both closed- and open-source models. Our evaluation is conducted under a *zero-shot* setting to assess the capability of models to generate accurate answers without fine-tuning or few-shot demonstrations on our benchmark. For all models, we use the default prompt provided by each model for multi-choice or open QA, if available. If models do not provide prompts for task types in MMMU, we conduct prompt engineering on the validation set and use the most effective prompt for the zero-shot setup in the main experiments. We also report the few-shot results of some selected models in the Appendix. All experiments are conducted with NVIDIA A100 GPUs.

### 1. Baselines

LMMs. We consider various large multimodal models. By default, for each model family, we use the latest, largest, and best-performing available checkpoint to date. *(i)* Kosmos2 [[63]](#ref-63) is pre-trained to ground fine-grained visual objects with texts and to follow instructions. With only 1.6B model size, Kosmos2 is able to achieve comparable or better performance with Flamingo-9B [[2]](#ref-2) on VQA and captioning tasks. *(ii)* LLaMA-Adapter2 [[20]](#ref-20) fine-tunes Llama [[74]](#ref-74) in a parameter-efficient way and utilizes visual encoder CLIP [[66]](#ref-66) and modular experts such as Optical Character Recognition (OCR) to capture more image information for later better visual understanding. *(iii)* BLIP-2 [[35]](#ref-35) introduces light-weight learnable visual queries to bridge the frozen CLIP ViT [[66]](#ref-66) and FLAN-T5 [[14]](#ref-14). *(iv)* Starting from the parameters from BLIP-2, InstructBLIP [[16]](#ref-16) is further fine-tuned with visual instruction tuning data for better zero-shot generalization capabilities. *(v)* LLaVA-1.5 [[44]](#ref-44) linearly projects the visual embedding into word embedding space of Vicuna [[12]](#ref-12), thus equipping the LLM with visual abilities. *(vi)* As an open-source alternative to Flamingo [[2]](#ref-2), OpenFlamingo [[4]](#ref-4) has close performance on most vision-language tasks. *(vii)* CogVLM [[77]](#ref-77) concatenates image and text in the input embedding space and adds trainable visual layers in textual Transformer blocks to deeply align two modalities. It has been reported to achieve very promising performance on existing VQA benchmarks recently. *(viii)* Fuyu [[6]](#ref-6) projects the patches of the input image into text embedding space. *(ix)* Qwen-VL [[5]](#ref-5) introduces a set of trainable query embeddings and singlelayer cross-attention module to bridge the modalities, supporting interleaved image-text input. *(x)* Otter [[34]](#ref-34) is finetuned with diverse instruction-tuning data and able to perform in-context learning. *(xi)* MiniGPT-4 [[94]](#ref-94) is built upon Vicuna [[12]](#ref-12) and designs a linear modality projection layer for visual understanding abilities. *(xii)* mPLUG-Owl2 [[82]](#ref-82) designs a modality-adaptive module to unify vision and language while preserving their distinct properties of them.

Text-only LLMs. For text-only LLMs, we consider the most capable ones including GPT-4 and several open-source LLMs, Llama2-7B [[74]](#ref-74), FLAN-T5-XXL and Vicuna-13B, which are adopted as the text encoder or decoder in the selected LMMs. To determine if an external image-to-text tool can enhance these LLMs' performance on MMMU, we deploy OCR by MMOCR^1^ or captioning by LLaVA-1.5 to provide the recognized text information to text-only LLMs. Human Experts. We involve 90 college senior students, selected to represent a wide range of experts in the corresponding 30 subjects (3 student experts per subject). These students were tasked with completing the 30 questions in their corresponding subjects (900 validation questions in total). The students were allowed to consult their textbooks

^1^<https://github.com/open-mmlab/mmocr>

| | Validation<br>Overall | Test<br>Overall<br>(10,500) | Art &<br>Design<br>(1,163) | Business<br>(1,428) | Science<br>(2,426) | Health &<br>Medicine<br>(1,752) | Human. &<br>Social Sci.<br>(947) | Tech &<br>Eng.<br>(2,784) |
|---|---|---|---|---|---|---|---|---|
| | (900) | | | | | | | |
| Random Choice | 22.1 | 23.9 | 24.1 | 24.9 | 21.6 | 25.3 | 22.8 | 24.8 |
| Frequent Choice | 26.8 | 25.8 | 26.7 | 28.4 | 24.0 | 24.4 | 25.2 | 26.5 |
| Expert (Worst) | 76.2 | - | - | - | - | - | - | - |
| Expert (Medium) | 82.6 | - | - | - | - | - | - | - |
| Expert (Best) | 88.6 | - | - | - | - | - | - | - |
| | Large Multimodal Models (LMMs): Text + Image as Input | | | | | | | |
| OpenFlamingo2-9B [[4]](#ref-4) | 28.7 | 26.3 | 31.7 | 23.5 | 26.3 | 26.3 | 27.9 | 25.1 |
| Kosmos2 [[63]](#ref-63) | 24.4 | 26.6 | 28.8 | 23.7 | 26.6 | 27.2 | 26.3 | 26.8 |
| Adept Fuyu-8B [[6]](#ref-6) | 27.9 | 27.4 | 29.9 | 27.0 | 25.6 | 27.0 | 32.5 | 26.4 |
| MiniGPT4-Vicuna-13B [[94]](#ref-94) | 26.8 | 27.6 | 30.2 | 27.0 | 26.2 | 26.9 | 30.9 | 27.2 |
| LLaMA-Adapter2-7B [[88]](#ref-88) | 29.8 | 27.7 | 35.2 | 25.4 | 25.6 | 30.0 | 29.1 | 25.7 |
| CogVLM [[77]](#ref-77) | 32.1 | 30.1 | 38.0 | 25.6 | 25.1 | 31.2 | 41.5 | 28.9 |
| Qwen-VL-7B-Chat [[5]](#ref-5) | 35.9 | 32.9 | 47.7 | 29.8 | 25.6 | 33.6 | 45.3 | 30.2 |
| InstructBLIP-T5-XXL [[16]](#ref-16) | 35.7 | 33.8 | 48.5 | 30.6 | 27.6 | 33.6 | 49.8 | 29.4 |
| BLIP-2 FLAN-T5-XXL [[35]](#ref-35) | 35.4 | 34.0 | 49.2 | 28.6 | 27.3 | 33.7 | 51.5 | 30.4 |
| InternLM-XComposer2-VL* [[17]](#ref-17) | 43.0 | 38.2 | 56.8 | 32.8 | 30.1 | 39.8 | 60.7 | 31.8 |
| Yi-VL-34B* [[84]](#ref-84) | 45.9 | 41.6 | 56.1 | 33.3 | 32.9 | 45.9 | 66.5 | 36.0 |
| LLaVA-1.6-34B* [[46]](#ref-46) | 51.1 | 44.7 | 58.6 | 39.9 | 36.0 | 51.2 | 70.2 | 36.3 |
| InternVL-Chat-V1.2* [[11]](#ref-11) | 51.6 | 46.2 | 62.5 | 37.6 | 37.9 | 49.7 | 70.1 | 40.8 |
| VILA1.5* [[39]](#ref-39) | 51.9 | 46.9 | 62.1 | 40.6 | 37.7 | 51.7 | 74.0 | 39.5 |
| Qwen-VL-MAX* [[65]](#ref-65) | 51.4 | 46.8 | 64.2 | 39.8 | 36.3 | 52.5 | 70.4 | 40.7 |
| SenseChat-Vision-0423-Preview* [[68]](#ref-68) | 54.6 | 50.3 | 62.7 | 44.1 | 42.3 | 55.7 | 74.7 | 43.5 |
| GPT-4V(ision) (Playground) [[60]](#ref-60) | 56.8 | 55.7 | 65.3 | 64.3 | 48.4 | 63.5 | 76.3 | 41.7 |
| Claude 3 Opus* [[72]](#ref-72) | 59.4 | - | - | - | - | - | - | - |
| Gemini 1.5 Pro* [[23]](#ref-23) | 62.2 | - | - | - | - | - | - | - |
| GPT-4o* [[61]](#ref-61) | 69.1 | - | - | - | - | - | - | - |
| | Large Language Models (LLMs): Only Text as Input | | | | | | | |
| Llama2 7B [[75]](#ref-75) | 30.1 | 28.7 | 30.7 | 27.2 | 26.7 | 27.7 | 32.6 | 29.8 |
| FLAN-T5-XXL [[14]](#ref-14) | 32.1 | 31.2 | 36.8 | 28.9 | 26.7 | 32.8 | 44.8 | 28.3 |
| + OCR | 34.7 | 31.9 | 36.2 | 28.8 | 26.2 | 32.6 | 50.5 | 29.7 |
| + LLaVA Caption | 34.8 | 31.9 | 38.4 | 27.8 | 27.0 | 33.2 | 49.9 | 28.7 |
| Vicuna-13B [[12]](#ref-12) | 33.3 | 31.0 | 35.1 | 30.1 | 24.7 | 31.4 | 44.8 | 30.1 |
| + OCR | 35.4 | 31.9 | 37.1 | 28.6 | 26.5 | 32.0 | 49.3 | 30.0 |
| + LLaVA Caption | 33.9 | 32.7 | 42.0 | 26.8 | 26.2 | 33.4 | 49.4 | 31.4 |
| GPT-4 Text [[59]](#ref-59) | 34.9 | 33.8 | 32.9 | 28.5 | 30.6 | 41.3 | 53.0 | 28.4 |

Table 2. Selected results of different models on the MMMU validation and test set. Besides reporting the performance of LMMs, we additionally add text-only LLM baselines. The best-performing model in each category is in-bold, and the second best is underlined. \*: results provided by the authors. Due to the page limit, we show other models' results in Appendix [Table 4](#ref-4). The live-updating leaderboard is available at: <https://mmmu-benchmark.github.io/#leaderboard>

but were prohibited from searching the Internet for answers.

Evaluation. We adopt micro-averaged accuracy as the evaluation metric. For both open and multiple-choice questions, we design systematic, rule-based evaluation pipelines. Specifically, to mitigate the potential influence of any intermediate generations (e.g., reasoning steps, calculations) in the long response, we construct robust regular expressions and develop response-processing workflows. These are employed to extract key phrases, such as numbers and conclusion phrases, from the long responses for accurate answer matching. If there is no valid answer in the model's response, we perform random selection as a remedy for multiple-choice questions or consider the response incorrect for open questions. For reference, we add Random Choice and Frequent Choice baselines: the former randomly selects an option, while the latter selects the most frequent option within each specific subject of the validation set, based on its frequency of occurrence in that subject.

### 2. Main Results

In this section, we present a comprehensive comparison of different LLMs and LMMs using the MMMU benchmark, detailed in [Table 2](#ref-2). We summarize our key findings as follows: Challenging Nature of **MMMU**: The benchmark poses significant challenges to current models. The Best human expert achieves a validation accuracy of 88.6%, significantly outperforming all the models reported in the table. This demonstrates the still-existing gap between human expertise and the performance of current models on the MMMU benchmark. This reflects the benchmark's rigorous standards.

![](_page_6_Figure_0.jpeg)

Figure 4. Performance of models on different types of images.

Disparity between Open-source Models and Closedsource models: Leading open-source models (as the paper submission) such as BLIP2-FLAN-T5-XXL and LLaVA-1.5 reach an accuracy level of approximately 34%, which is significantly lower than GPT-4V. However, it is exciting to see that open-source models have made significant strides in performance. For example, LLaVA-1.6-34B and InternVL-Chat-V1.2 achieve test accuracies of 44.7% and 46.2%, respectively, narrowing the gap with proprietary models.

Effectiveness of OCR and Captioning Enhancements: The application of OCR and captioning technologies does not yield a significant improvement in the performance of text-only LMMs. This finding suggests that the MMMU benchmark requires models that can effectively interpret and integrate both textual and visual information, underscoring the complexity of the multimodal tasks it presents. Model Performance across Different Disciplines: In disciplines such as Art & Design and Humanities & Social Sciences, where the images tends to be more 'natural' and questions involve relatively less reasoning, models demonstrate relatively higher performance. Conversely, in fields like Science, Health & Medicine, and Technology & Engineering, where tasks often involve intricate perception and complex reasoning, models exhibit lower performance.

The MMMU benchmark underscores both the progress and the challenges in multimodal understanding and reasoning. While GPT-4V leads in performance, the overall results indicate substantial room for improvement, especially in domains with complex visual input and heavy reasoning with subject knowledge.

### 3. Analysis on Images Types and Difficulties

Different Image Types. We compare the performance of various models across top frequent image types in [Figure 4](#ref-4). Across all types, GPT-4V consistently outperforms the other models by a huge margin. Open-source models demonstrate relatively strong performance in categories like Photos and Paintings, which are more frequently seen during training. However, for less common image categories like Geometric shapes, Music sheets and Chemical struc-

| Models | Easy<br>(2946) | Medium<br>(4917) | Hard<br>(2637) | Overall<br>(10500) | |
|---|---|---|---|---|---|
| Fuyu-8B [[6]](#ref-6) | 28.9 | 27.0 | 26.4 | 27.4 | |
| Qwen-VL-7B [[5]](#ref-5) | 39.4 | 31.9 | 27.6 | 32.9 | |
| LLaVA-1.5-13B [[44]](#ref-44) | 41.3 | 32.7 | 26.7 | 33.6 | |
| InstructBLIP-T5-XXL [[16]](#ref-16) | 40.3 | 32.3 | 29.4 | 33.8 | |
| BLIP-2 FLAN-T5-XXL [[35]](#ref-35) | 41.0 | 32.7 | 28.5 | 34.0 | |
| GPT-4V [[60]](#ref-60) | 76.1 | 55.6 | 31.2 | 55.7 | |

Table 3. Result decomposition across question difficulty levels.

tures, all models obtain very low scores (some are close to random guesses). This indicates that the existing models are generalizing poorly towards these image types.

Different Difficulty Levels. [Table 3](#ref-3) compares the performance of selected models across three difficulty levels. GPT-4V demonstrates a significantly higher proficiency, with a success rate of 76.1%, compared to opensource models in the "Easy" category. When it comes to the "Medium" category, while the gap narrows, GPT-4V still leads at 55.6%. The further diminishing performance gap in the "Hard" category across models indicates that as the complexity of tasks increases, the advantage of more advanced models like GPT-4V almost disappears. This might reflect a current limitation in handling expert-level challenging queries even for the most advanced models.

### Error Analysis and Future Work

In this section, we delve into the analysis of errors by GPT-4V, a pivotal aspect for understanding its operational capabilities and limitations. This analysis serves not only to identify the model's current shortcomings but also to guide future enhancements in its design and training. We meticulously examine 150 randomly sampled error instances from GPT-4V's predictions. These instances are analyzed by expert annotators who identify the *root causes of mispredictions* based on their knowledge and the golden explanations if available. The distribution of these errors is illustrated in [Figure 5](#ref-5), and a selection of 100 notable cases, along with detailed analyses, is included in the Appendix.

Perceptual Errors (35%): Perceptual errors, forming the bulk of the inaccuracies in the GPT-4V model, are categorized into two types: basic perceptual errors and domainspecific perceptual errors. Basic perceptual errors, as depicted in [Figure 6](#ref-6), occur when the model accurately processes and understands the given information but fails in elementary visual interpretation, such as misjudging the sequence described as "from left to right, top to bottom." On the other hand, domain-specific perceptual errors occur due to the lack of knowledge. As we analyze the root cause, we classify such errors as lack of knowledge (see analysis below). Additionally, GPT-4V often exhibits a bias towards

![](_page_7_Figure_0.jpeg)

Figure 5. Error distribution over 150 annotated GPT-4V errors.

text, prioritizing textual information over visual inputs, a trend noted in recent studies [[15]](#ref-15). A prominent example is in [Figure 67](#ref-67), where the model incorrectly prioritizes its textbased interpretation of "imperialism" over the visual narrative in a cartoon depicting the United States as a "Savior." This underscores the need for a more balanced approach to multimodal interpretation.

Lack of Knowledge (29%): A fundamental root cause of 'domain-specific' perceptual errors in the GPT-4V model, as previously discussed, is the lack of specialized knowledge. This deficiency is exemplified in the Computer Science context illustrated in Appendix [Figure 83](#ref-83), where the model identifies visual elements such as double circles but fails to interpret them accurately within the domain-specific context, such as their representation of an 'accept state' in Deterministic Finite Automata. Similarly, a deficit in specialized knowledge can lead to flawed reasoning, as demonstrated in the medical example in Appendix [Figure 54](#ref-54). These instances underscore the necessity of enriching the training datasets of foundation models with a diverse range of domain-specific knowledge to improve their accuracy and general applicability in various specialized fields.

Reasoning Errors (26%): Flawed reasoning emerges as another significant cause of errors. In instances where the model correctly interprets text and images and recalls relevant knowledge, it still often fails to apply logical and mathematical reasoning skills effectively to derive accurate inferences. A notable instance of this can be observed in Appendix [Figure 45](#ref-45), where the model neglects an essential step in a mathematical reasoning process, leading to an incorrect conclusion. Enhancing the model's reasoning capability is critical to address these shortcomings.

Other Errors: The remaining errors include Textual Understanding Error (6%), Rejection to Answer (3%), Annotation Error (2%), and Answer Extraction Error (1%). These errors are attributed to various factors such as complex text interpretation challenges, limitations in response generation, inaccuracies in data annotation, and issues in extracting precise answers from longer outputs.

![](_page_7_Picture_6.jpeg)

Figure 6. A basic perceptual error, easy for humans but challenging for GPT-4V. More examples can be found in the Appendix.

In summary, our error analysis underlines the challenges posed by MMMU and highlights areas for further research in visual perception, knowledge representation, reasoning abilities, and multimodal joint understanding. 1) *Interplay of language and vision*: language can aid in making visual understanding more explainable, while also leading models to hallucinate. 2) *Challenges in grounding*: tasks involving grounding or referring to specific elements within a visual input remain challenging, even for sophisticated models like GPT-4V. 3) *Complex reasoning is still challenging*: models still fail in complex reasoning scenarios involving lengthy reasoning chains or extensive calculations.

### Conclusion

The introduction of MMMU marks a significant step towards evaluating the capabilities of LMMs in the context of Expert AGI. By assessing both basic perceptual skills and complex reasoning abilities across various professional domains, MMMU provides a comprehensive benchmark that aligns with the expectations of skilled adults in these fields.

MMMU, like any benchmark, has limitations despite its comprehensive nature. The manual curation process may carry biases, and the focus on college-level subjects might not be sufficient for testing Expert AGI [[57]](#ref-57). However, we argue that strong performance on this benchmark should be a necessary criterion for an Expert AGI system. The challenging nature of MMMU is evident from the performance of over 30 models and human experts. To strike a balance between complexity and practicality, MMMU combines multiple-choice questions with concise open-ended questions, enabling the assessment of diverse subjects while addressing the challenges associated with evaluating openended responses.

### References

- <a id="ref-1"></a>[1] Blaise Aguera y Arcas and Peter Norvig. Artificial general intelligence is already here. *Noema Magazine*, 2023. [[1]](#ref-1)
- <a id="ref-2"></a>[2] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katherine Millican, Malcolm Reynolds, et al. Flamingo: a visual language model for few-shot learning. In *Advances in Neural Information Processing Systems*, 2022. [[3]](#ref-3), [[5]](#ref-5)
- <a id="ref-3"></a>[3] Stanislaw Antol, Aishwarya Agrawal, Jiasen Lu, Margaret Mitchell, Dhruv Batra, C. Lawrence Zitnick, and Devi Parikh. VQA: Visual Question Answering. In *International Conference on Computer Vision (ICCV)*, 2015. [[2]](#ref-2), [[3]](#ref-3)
- <a id="ref-4"></a>[4] Anas Awadalla, Irena Gao, Josh Gardner, Jack Hessel, Yusuf Hanafy, Wanrong Zhu, Kalyani Marathe, Yonatan Bitton, Samir Gadre, Shiori Sagawa, et al. Openflamingo: An opensource framework for training large autoregressive visionlanguage models. *arXiv preprint arXiv:2308.01390*, 2023. [[3]](#ref-3), [[5]](#ref-5), [[6]](#ref-6), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-5"></a>[5] Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang Zhou, and Jingren Zhou. Qwen-vl: A versatile vision-language model for understanding, localization, text reading, and beyond. *arXiv preprint arXiv:2308.12966*, 2023. [[5]](#ref-5), [[6]](#ref-6), [[7]](#ref-7), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-6"></a>[6] Rohan Bavishi, Erich Elsen, Curtis Hawthorne, Maxwell Nye, Augustus Odena, Arushi Somani, and Sagnak Tas¸ırlar. ˘ Introducing our multimodal models, 2023. [[3]](#ref-3), [[5]](#ref-5), [[6]](#ref-6), [[7]](#ref-7), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-7"></a>[7] Sebastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Jo- ´ hannes Gehrke, Eric Horvitz, Ece Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg, et al. Sparks of artificial general intelligence: Early experiments with gpt-4. *arXiv preprint arXiv:2303.12712*, 2023. [[1]](#ref-1)
- <a id="ref-8"></a>[8] Bunny. Bunny-3b. <https://github.com/cappuch/Bunny-Qwen>, 2024. GitHub Repository. [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-9"></a>[9] Xi Chen, Josip Djolonga, Piotr Padlewski, Basil Mustafa, Soravit Changpinyo, Jialin Wu, Carlos Riquelme Ruiz, Sebastian Goodman, Xiao Wang, Yi Tay, et al. Pali-x: On scaling up a multilingual vision and language model. *arXiv preprint arXiv:2305.18565*, 2023. [[2]](#ref-2)
- <a id="ref-10"></a>[10] Yen-Chun Chen, Linjie Li, Licheng Yu, Ahmed El Kholy, Faisal Ahmed, Zhe Gan, Yu Cheng, and Jingjing Liu. Uniter: Universal image-text representation learning. In *European Conference on Computer Vision*, pages 104–120, 2020. [[3]](#ref-3)
- <a id="ref-11"></a>[11] Zhe Chen, Jiannan Wu, Wenhai Wang, Weijie Su, Guo Chen, Sen Xing, Zhong Muyan, Qinglong Zhang, Xizhou Zhu, Lewei Lu, et al. Internvl: Scaling up vision foundation models and aligning for generic visual-linguistic tasks. *arXiv preprint arXiv:2312.14238*, 2023. [[6]](#ref-6), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-12"></a>[12] Wei-Lin Chiang, Zhuohan Li, Zi Lin, Ying Sheng, Zhanghao Wu, Hao Zhang, Lianmin Zheng, Siyuan Zhuang, Yonghao Zhuang, Joseph E. Gonzalez, Ion Stoica, and Eric P. Xing. Vicuna: An open-source chatbot impressing gpt-4 with 90%*chatgpt quality, 2023. [[3]](#ref-3), [[5]](#ref-5), [[6]](#ref-6), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)

- <a id="ref-13"></a>[13] Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, et al. Palm: Scaling language modeling with pathways.*arXiv preprint arXiv:2204.02311*, 2022. [[1]](#ref-1)
- <a id="ref-14"></a>[14] Hyung Won Chung, Le Hou, Shayne Longpre, Barret Zoph, Yi Tay, William Fedus, Eric Li, Xuezhi Wang, Mostafa Dehghani, Siddhartha Brahma, et al. Scaling instruction-finetuned language models. *arXiv preprint arXiv:2210.11416*, 2022. [[3]](#ref-3), [[5]](#ref-5), [[6]](#ref-6), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-15"></a>[15] Chenhang Cui, Yiyang Zhou, Xinyu Yang, Shirley Wu, Linjun Zhang, James Zou, and Huaxiu Yao. Holistic analysis of hallucination in gpt-4v (ision): Bias and interference challenges. *arXiv preprint arXiv:2311.03287*, 2023. [[3]](#ref-3), [[8]](#ref-8)
- <a id="ref-16"></a>[16] Wenliang Dai, Junnan Li, Dongxu Li, Anthony Meng Huat Tiong, Junqi Zhao, Weisheng Wang, Boyang Li, Pascale Fung, and Steven Hoi. Instructblip: Towards generalpurpose vision-language models with instruction tuning. *arXiv preprint arXiv:2305.06500*, 2023. [[2]](#ref-2), [[3]](#ref-3), [[5]](#ref-5), [[6]](#ref-6), [[7]](#ref-7), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-17"></a>[17] Xiaoyi Dong, Pan Zhang, Yuhang Zang, Yuhang Cao, Bin Wang, Linke Ouyang, Xilin Wei, Songyang Zhang, Haodong Duan, Maosong Cao, et al. Internlm-xcomposer2: Mastering free-form text-image composition and comprehension in vision-language large model. *arXiv preprint arXiv:2401.16420*, 2024. [[6]](#ref-6), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-18"></a>[18] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, and Neil Houlsby. An image is worth 16x16 words: Transformers for image recognition at scale. In *International Conference on Learning Representations*, 2021. [[3]](#ref-3)
- <a id="ref-19"></a>[19] Adept Fuyu Team. Adept fuyu-heavy: A new multimodal model. <https://www.adept.ai/blog/adept-fuyu-heavy>, 2024. [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-20"></a>[20] Peng Gao, Jiaming Han, Renrui Zhang, Ziyi Lin, Shijie Geng, Aojun Zhou, Wei Zhang, Pan Lu, Conghui He, Xiangyu Yue, et al. Llama-adapter v2: Parameter-efficient visual instruction model. *arXiv preprint arXiv:2304.15010*, 2023. [[3]](#ref-3), [[5]](#ref-5)
- <a id="ref-21"></a>[21] Yingqiang Ge, Wenyue Hua, Jianchao Ji, Juntao Tan, Shuyuan Xu, and Yongfeng Zhang. Openagi: When llm meets domain experts. *arXiv preprint arXiv:2304.04370*, 2023. [[1]](#ref-1)
- <a id="ref-22"></a>[22] Google Gemini Team. Gemini: A family of highly capable multimodal models. <https://storage.googleapis.com/deepmind-media/gemini/gemini_1_report.pdf>, 2023. [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21), [[119]](#ref-119)
- <a id="ref-23"></a>[23] Google Gemini Team. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. <https://storage.googleapis.com/deepmind-media/gemini/gemini_v1_5_report.pdf>, 2024. [[6]](#ref-6), [[15]](#ref-15), [[119]](#ref-119)
- <a id="ref-24"></a>[24] Yash Goyal, Tejas Khot, Douglas Summers-Stay, Dhruv Batra, and Devi Parikh. Making the v in vqa matter: Elevating

the role of image understanding in visual question answering. In *Proceedings of the IEEE conference on computer vision and pattern recognition*, pages 6904–6913, 2017. [[2]](#ref-2), [[3]](#ref-3)

- <a id="ref-25"></a>[25] Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob Steinhardt. Measuring massive multitask language understanding. In *International Conference on Learning Representations*, 2020. [[2]](#ref-2)
- <a id="ref-26"></a>[26] Yupan Huang, Zaiqiao Meng, Fangyu Liu, Yixuan Su, Collier Nigel, and Yutong Lu. Sparkles: Unlocking chats across multiple images for multimodal instruction-following models. *arXiv preprint arXiv:2308.16463*, 2023. [[3]](#ref-3)
- <a id="ref-27"></a>[27] Drew A Hudson and Christopher D Manning. Gqa: A new dataset for real-world visual reasoning and compositional question answering. In *Proceedings of the IEEE/CVF conference on computer vision and pattern recognition*, pages 6700–6709, 2019. [[3]](#ref-3)
- <a id="ref-28"></a>[28] HyperGAI. Revolutionizing the future with hyper generative ai. 2024. [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-29"></a>[29] Chao Jia, Yinfei Yang, Ye Xia, Yi-Ting Chen, Zarana Parekh, Hieu Pham, Quoc Le, Yun-Hsuan Sung, Zhen Li, and Tom Duerig. Scaling up visual and vision-language representation learning with noisy text supervision. In *International conference on machine learning*, pages 4904–4916. PMLR, 2021. [[3]](#ref-3)
- <a id="ref-30"></a>[30] Sahar Kazemzadeh, Vicente Ordonez, Mark Matten, and Tamara Berg. Referitgame: Referring to objects in photographs of natural scenes. In *Proceedings of the 2014 conference on empirical methods in natural language processing (EMNLP)*, pages 787–798, 2014. [[2]](#ref-2)
- <a id="ref-31"></a>[31] Kunlun. Agi and aigc business skywork. 2024. [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-32"></a>[32] Ehsan Latif, Gengchen Mai, Matthew Nyaaba, Xuansheng Wu, Ninghao Liu, Guoyu Lu, Sheng Li, Tianming Liu, and Xiaoming Zhai. Artificial general intelligence (agi) for education. *arXiv preprint arXiv:2304.12479*, 2023. [[1]](#ref-1)
- <a id="ref-33"></a>[33] Bohao Li, Rui Wang, Guangzhi Wang, Yuying Ge, Yixiao Ge, and Ying Shan. Seed-bench: Benchmarking multimodal llms with generative comprehension. *arXiv preprint arXiv:2307.16125*, 2023. [[2]](#ref-2), [[3]](#ref-3)
- <a id="ref-34"></a>[34] Bo Li, Yuanhan Zhang, Liangyu Chen, Jinghao Wang, Jingkang Yang, and Ziwei Liu. Otter: A multi-modal model with in-context instruction tuning. *arXiv preprint arXiv:2305.03726*, 2023. [[3]](#ref-3), [[5]](#ref-5), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-35"></a>[35] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. *International Conference on Machine Learning*, 2023. [[2]](#ref-2), [[3]](#ref-3), [[5]](#ref-5), [[6]](#ref-6), [[7]](#ref-7), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-36"></a>[36] Lei Li, Yuwei Yin, Shicheng Li, Liang Chen, Peiyi Wang, Shuhuai Ren, Mukai Li, Yazheng Yang, Jingjing Xu, Xu Sun, et al. M3it: A large-scale dataset towards multimodal multilingual instruction tuning. *arXiv preprint arXiv:2306.04387*, 2023. [[3]](#ref-3)
- <a id="ref-37"></a>[37] Xiujun Li, Xi Yin, Chunyuan Li, Pengchuan Zhang, Xiaowei Hu, Lei Zhang, Lijuan Wang, Houdong Hu, Li Dong, Furu Wei, et al. Oscar: Object-semantics aligned pre-training for vision-language tasks. In *Computer Vision–ECCV 2020:*

*16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part XXX 16*, pages 121–137. Springer, 2020. [[3]](#ref-3)

- <a id="ref-38"></a>[38] Yifan Li, Yifan Du, Kun Zhou, Jinpeng Wang, Wayne Xin Zhao, and Ji-Rong Wen. Evaluating object hallucination in large vision-language models. *arXiv preprint arXiv:2305.10355*, 2023. [[3]](#ref-3)
- <a id="ref-39"></a>[39] Ji Lin, Hongxu Yin, Wei Ping, Yao Lu, Pavlo Molchanov, Andrew Tao, Huizi Mao, Jan Kautz, Mohammad Shoeybi, and Song Han. Vila: On pre-training for visual language models. *arXiv preprint arXiv:2312.07533*, 2023. [[6]](#ref-6), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-40"></a>[40] Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollar, and C Lawrence ´ Zitnick. Microsoft coco: Common objects in context. In *Computer Vision–ECCV 2014: 13th European Conference, Zurich, Switzerland, September 6-12, 2014, Proceedings, Part V 13*, pages 740–755. Springer, 2014. [[2]](#ref-2), [[3]](#ref-3)
- <a id="ref-41"></a>[41] Ziyi Lin, Chris Liu, Renrui Zhang, Peng Gao, Longtian Qiu, Han Xiao, Han Qiu, Chen Lin, Wenqi Shao, Keqin Chen, et al. Sphinx: The joint mixing of weights, tasks, and visual embeddings for multi-modal large language models. *arXiv preprint arXiv:2311.07575*, 2023. [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-42"></a>[42] Fuxiao Liu, Tianrui Guan, Zongxia Li, Lichang Chen, Yaser Yacoob, Dinesh Manocha, and Tianyi Zhou. Hallusionbench: You see what you think? or you think what you see? an image-context reasoning benchmark challenging for gpt-4v (ision), llava-1.5, and other multi-modality models. *arXiv preprint arXiv:2310.14566*, 2023. [[3]](#ref-3)
- <a id="ref-43"></a>[43] Fuxiao Liu, Kevin Lin, Linjie Li, Jianfeng Wang, Yaser Yacoob, and Lijuan Wang. Aligning large multi-modal model with robust instruction tuning. *arXiv preprint arXiv:2306.14565*, 2023. [[3]](#ref-3)
- <a id="ref-44"></a>[44] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual instruction tuning. *arXiv preprint arXiv:2310.03744*, 2023. [[2]](#ref-2), [[3]](#ref-3), [[5]](#ref-5), [[7]](#ref-7), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-45"></a>[45] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. *arXiv preprint arXiv:2304.08485*, 2023. [[3]](#ref-3)
- <a id="ref-46"></a>[46] Haotian Liu, Chunyuan Li, Yuheng Li, Bo Li, Yuanhan Zhang, Sheng Shen, and Yong Jae Lee. Llava-next: Improved reasoning, ocr, and world knowledge. 2024. [[6]](#ref-6), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-47"></a>[47] Yuan Liu, Haodong Duan, Yuanhan Zhang, Bo Li, Songyang Zhang, Wangbo Zhao, Yike Yuan, Jiaqi Wang, Conghui He, Ziwei Liu, et al. Mmbench: Is your multi-modal model an all-around player? *arXiv preprint arXiv:2307.06281*, 2023. [[2]](#ref-2), [[3]](#ref-3)
- <a id="ref-48"></a>[48] Yuliang Liu, Zhang Li, Hongliang Li, Wenwen Yu, Mingxin Huang, Dezhi Peng, Mingyu Liu, Mingrui Chen, Chunyuan Li, Lianwen Jin, et al. On the hidden mystery of ocr in large multimodal models. *arXiv preprint arXiv:2305.07895*, 2023. [[3]](#ref-3)
- <a id="ref-49"></a>[49] Jiasen Lu, Dhruv Batra, Devi Parikh, and Stefan Lee. Vilbert: Pretraining task-agnostic visiolinguistic representations for vision-and-language tasks. *Advances in neural information processing systems*, 32, 2019. [[3]](#ref-3)

- <a id="ref-50"></a>[50] Pan Lu, Swaroop Mishra, Tanglin Xia, Liang Qiu, Kai-Wei Chang, Song-Chun Zhu, Oyvind Tafjord, Peter Clark, and Ashwin Kalyan. Learn to explain: Multimodal reasoning via thought chains for science question answering. *Advances in Neural Information Processing Systems*, 35:2507–2521, 2022. [[2]](#ref-2)
- <a id="ref-51"></a>[51] Pan Lu, Hritik Bansal, Tony Xia, Jiacheng Liu, Chunyuan Li, Hannaneh Hajishirzi, Hao Cheng, Kai-Wei Chang, Michel Galley, and Jianfeng Gao. Mathvista: Evaluating mathematical reasoning of foundation models in visual contexts. *arXiv preprint arXiv:2310.02255*, 2023. [[3]](#ref-3)
- <a id="ref-52"></a>[52] Kenneth Marino, Mohammad Rastegari, Ali Farhadi, and Roozbeh Mottaghi. Ok-vqa: A visual question answering benchmark requiring external knowledge. In *Conference on Computer Vision and Pattern Recognition (CVPR)*, 2019. [[3]](#ref-3)
- <a id="ref-53"></a>[53] Gregoire Mialon, Clementine Fourrier, Craig Swift, Thomas Wolf, Yann LeCun, and Thomas Scialom. Gaia: a benchmark for general ai assistants. *arXiv preprint arXiv:2311.12983*, 2023. [[1]](#ref-1), [[3]](#ref-3)
- <a id="ref-54"></a>[54] MiniCPM. Minicpm-v. <https://github.com/OpenBMB/MiniCPM>, 2024. GitHub Repository. [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-55"></a>[55] MiniCPM. Minicpm-v-2, 2024. [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-56"></a>[56] Masoud Monajatipoor, Liunian Harold Li, Mozhdeh Rouhsedaghat, Lin F Yang, and Kai-Wei Chang. Metavl: Transferring in-context learning ability from language models to vision-language models. *arXiv preprint arXiv:2306.01311*, 2023. [[3]](#ref-3)
- <a id="ref-57"></a>[57] Meredith Ringel Morris, Jascha Sohl-dickstein, Noah Fiedel, Tris Warkentin, Allan Dafoe, Aleksandra Faust, Clement Farabet, and Shane Legg. Levels of agi: Operationalizing progress on the path to agi. *arXiv preprint arXiv:2311.02462*, 2023. [[1]](#ref-1), [[3]](#ref-3), [[8]](#ref-8)
- <a id="ref-58"></a>[58] OminiLMM. Ominilmm-12b. <https://github.com/OpenBMB/OmniLMM>, 2024. GitHub Repository. [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-59"></a>[59] OpenAI. Gpt-4 technical report. *arXiv preprint arXiv:2303.08774*, 2023. [[1]](#ref-1), [[6]](#ref-6), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-60"></a>[60] OpenAI. Gpt-4v(ision) system card, 2023. [[2]](#ref-2), [[6]](#ref-6), [[7]](#ref-7), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-61"></a>[61] OpenAI. Gpt-4o. 2024. [[6]](#ref-6), [[15]](#ref-15), [[119]](#ref-119)
- <a id="ref-62"></a>[62] Aitor Ormazabal, Che Zheng, Cyprien de Masson d'Autume, Dani Yogatama, Deyu Fu, Donovan Ong, et al. Reka core, flash, and edge: A series of powerful multimodal language models. <https://publications.reka.ai/reka-core-tech-report.pdf>, 2024. [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21), [[119]](#ref-119)
- <a id="ref-63"></a>[63] Zhiliang Peng, Wenhui Wang, Li Dong, Yaru Hao, Shaohan Huang, Shuming Ma, and Furu Wei. Kosmos-2: Grounding multimodal large language models to the world. *arXiv preprint arXiv:2306.14824*, 2023. [[5]](#ref-5), [[6]](#ref-6), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-64"></a>[64] Qwen. Qwen-vl-plus. <https://github.com/QwenLM/Qwen-VL?tab=readme-ov-file#qwen-vl-plus>, 2023. GitHub Repository. [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)

- <a id="ref-65"></a>[65] Qwen. Qwen-vl-max. <https://github.com/QwenLM/Qwen-VL?tab=readme-ov-file#qwen-vl-max>, 2024. GitHub Repository. [[6]](#ref-6), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-66"></a>[66] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In *International conference on machine learning*, pages 8748–8763. PMLR, 2021. [[3]](#ref-3), [[5]](#ref-5)
- <a id="ref-67"></a>[67] Shaoqing Ren, Kaiming He, Ross Girshick, and Jian Sun. Faster r-cnn: Towards real-time object detection with region proposal networks. *Advances in neural information processing systems*, 28, 2015. [[3]](#ref-3)
- <a id="ref-68"></a>[68] sensenova. Sensechat-vision, 2024. [[6]](#ref-6), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-69"></a>[69] Amanpreet Singh, Vivek Natarjan, Meet Shah, Yu Jiang, Xinlei Chen, Devi Parikh, and Marcus Rohrbach. Towards vqa models that can read. In *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, pages 8317–8326, 2019. [[2]](#ref-2)
- <a id="ref-70"></a>[70] Quan Sun, Yufeng Cui, Xiaosong Zhang, Fan Zhang, Qiying Yu, Zhengxiong Luo, Yueze Wang, Yongming Rao, Jingjing Liu, Tiejun Huang, et al. Generative multimodal models are in-context learners. *arXiv preprint arXiv:2312.13286*, 2023. [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-71"></a>[71] Hao Tan and Mohit Bansal. Lxmert: Learning crossmodality encoder representations from transformers. In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)*, pages 5100–5111, 2019. [[3]](#ref-3)
- <a id="ref-72"></a>[72] Claude Team. Introducing the next generation of claude. <https://www.anthropic.com/news/claude-3-family>, 2024. [[6]](#ref-6), [[15]](#ref-15), [[119]](#ref-119)
- <a id="ref-73"></a>[73] InfiMM Team. Infimm: Advancing multimodal understanding from flamingo's legacy through diverse llm integration, 2024. [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-74"></a>[74] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothee Lacroix, Baptiste ´ Roziere, Naman Goyal, Eric Hambro, Faisal Azhar, et al. ` Llama: Open and efficient foundation language models. *arXiv preprint arXiv:2302.13971*, 2023. [[1]](#ref-1), [[5]](#ref-5)
- <a id="ref-75"></a>[75] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. *arXiv preprint arXiv:2307.09288*, 2023. [[6]](#ref-6), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-76"></a>[76] Junyang Wang, Yiyang Zhou, Guohai Xu, Pengcheng Shi, Chenlin Zhao, Haiyang Xu, Qinghao Ye, Ming Yan, Ji Zhang, Jihua Zhu, et al. Evaluation and analysis of hallucination in large vision-language models. *arXiv preprint arXiv:2308.15126*, 2023. [[3]](#ref-3)
- <a id="ref-77"></a>[77] Weihan Wang, Qingsong Lv, Wenmeng Yu, Wenyi Hong, Ji Qi, Yan Wang, Junhui Ji, Zhuoyi Yang, Lei Zhao, Xixuan Song, et al. Cogvlm: Visual expert for pretrained language

models. *arXiv preprint arXiv:2311.03079*, 2023. [[2]](#ref-2), [[5]](#ref-5), [[6]](#ref-6), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)

- <a id="ref-78"></a>[78] Zirui Wang, Jiahui Yu, Adams Wei Yu, Zihang Dai, Yulia Tsvetkov, and Yuan Cao. Simvlm: Simple visual language model pretraining with weak supervision. In *International Conference on Learning Representations*, 2021. [[3]](#ref-3)
- <a id="ref-79"></a>[79] Peng Xu, Wenqi Shao, Kaipeng Zhang, Peng Gao, Shuo Liu, Meng Lei, Fanqing Meng, Siyuan Huang, Yu Qiao, and Ping Luo. Lvlm-ehub: A comprehensive evaluation benchmark for large vision-language models. *arXiv preprint arXiv:2306.09265*, 2023. [[3]](#ref-3)
- <a id="ref-80"></a>[80] Zhengyuan Yang, Linjie Li, Kevin Lin, Jianfeng Wang, Chung-Ching Lin, Zicheng Liu, and Lijuan Wang. The dawn of lmms: Preliminary explorations with gpt-4v (ision). *arXiv preprint arXiv:2309.17421*, 2023. [[2]](#ref-2)
- <a id="ref-81"></a>[81] Qinghao Ye, Haiyang Xu, Guohai Xu, Jiabo Ye, Ming Yan, Yiyang Zhou, Junyang Wang, Anwen Hu, Pengcheng Shi, Yaya Shi, et al. mplug-owl: Modularization empowers large language models with multimodality. *arXiv preprint arXiv:2304.14178*, 2023. [[3]](#ref-3)
- <a id="ref-82"></a>[82] Qinghao Ye, Haiyang Xu, Jiabo Ye, Ming Yan, Haowei Liu, Qi Qian, Ji Zhang, Fei Huang, and Jingren Zhou. mplug-owl2: Revolutionizing multi-modal large language model with modality collaboration. *arXiv preprint arXiv:2311.04257*, 2023. [[3]](#ref-3), [[5]](#ref-5), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-83"></a>[83] Zhenfei Yin, Jiong Wang, Jianjian Cao, Zhelun Shi, Dingning Liu, Mukai Li, Lu Sheng, Lei Bai, Xiaoshui Huang, Zhiyong Wang, et al. Lamm: Language-assisted multimodal instruction-tuning dataset, framework, and benchmark. *arXiv preprint arXiv:2306.06687*, 2023. [[2]](#ref-2), [[3]](#ref-3)
- <a id="ref-84"></a>[84] Alex Young, Bei Chen, Chao Li, Chengen Huang, Ge Zhang, Guanwei Zhang, Heng Li, Jiangcheng Zhu, Jianqun Chen, Jing Chang, et al. Yi: Open foundation models by 01. ai. *arXiv preprint arXiv:2403.04652*, 2024. [[6]](#ref-6), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-85"></a>[85] Jiahui Yu, Zirui Wang, Vijay Vasudevan, Legg Yeung, Mojtaba Seyedhosseini, and Yonghui Wu. Coca: Contrastive captioners are image-text foundation models. *TMLR*, 2022. [[3]](#ref-3)
- <a id="ref-86"></a>[86] Weihao Yu, Zhengyuan Yang, Linjie Li, Jianfeng Wang, Kevin Lin, Zicheng Liu, Xinchao Wang, and Lijuan Wang. Mm-vet: Evaluating large multimodal models for integrated capabilities. *arXiv preprint arXiv:2308.02490*, 2023. [[2]](#ref-2), [[3]](#ref-3)
- <a id="ref-87"></a>[87] Pengchuan Zhang, Xiujun Li, Xiaowei Hu, Jianwei Yang, Lei Zhang, Lijuan Wang, Yejin Choi, and Jianfeng Gao. Vinvl: Revisiting visual representations in vision-language models. In *Proceedings of the IEEE/CVF conference on computer vision and pattern recognition*, pages 5579–5588, 2021. [[3]](#ref-3)
- <a id="ref-88"></a>[88] Renrui Zhang, Jiaming Han, Aojun Zhou, Xiangfei Hu, Shilin Yan, Pan Lu, Hongsheng Li, Peng Gao, and Yu Qiao. Llama-adapter: Efficient fine-tuning of language models with zero-init attention. *arXiv preprint arXiv:2303.16199*, 2023. [[3]](#ref-3), [[6]](#ref-6), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)
- <a id="ref-89"></a>[89] Bo Zhao, Boya Wu, and Tiejun Huang. Svit: Scaling up visual instruction tuning. *arXiv preprint arXiv:2307.04087*, 2023. [[3]](#ref-3), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)

- <a id="ref-90"></a>[90] Haozhe Zhao, Zefan Cai, Shuzheng Si, Xiaojian Ma, Kaikai An, Liang Chen, Zixuan Liu, Sheng Wang, Wenjuan Han, and Baobao Chang. Mmicl: Empowering vision-language model with multi-modal in-context learning. *arXiv preprint arXiv:2309.07915*, 2023. [[3]](#ref-3)
- <a id="ref-91"></a>[91] Yunqing Zhao, Tianyu Pang, Chao Du, Xiao Yang, Chongxuan Li, Ngai-Man Cheung, and Min Lin. On evaluating adversarial robustness of large vision-language models. *arXiv preprint arXiv:2305.16934*, 2023. [[3]](#ref-3)
- <a id="ref-92"></a>[92] Wanjun Zhong, Ruixiang Cui, Yiduo Guo, Yaobo Liang, Shuai Lu, Yanlin Wang, Amin Saied, Weizhu Chen, and Nan Duan. Agieval: A human-centric benchmark for evaluating foundation models. *arXiv preprint arXiv:2304.06364*, 2023. [[2]](#ref-2)
- <a id="ref-93"></a>[93] Luowei Zhou, Hamid Palangi, Lei Zhang, Houdong Hu, Jason Corso, and Jianfeng Gao. Unified vision-language pretraining for image captioning and vqa. In *Proceedings of the AAAI conference on artificial intelligence*, pages 13041– 13049, 2020. [[3]](#ref-3)
- <a id="ref-94"></a>[94] Deyao Zhu, Jun Chen, Xiaoqian Shen, Xiang Li, and Mohamed Elhoseiny. Minigpt-4: Enhancing vision-language understanding with advanced large language models. *arXiv preprint arXiv:2304.10592*, 2023. [[3]](#ref-3), [[5]](#ref-5), [[6]](#ref-6), [[15]](#ref-15), [[16]](#ref-16), [[17]](#ref-17), [[18]](#ref-18), [[19]](#ref-19), [[20]](#ref-20), [[21]](#ref-21)

## MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI

Supplementary Material

## Table of Contents in Appendix

| | |
|---|---|
| A. Subject Distribution | 14 |
| B. Breakdown Results on Different Subjects | 15 |
| B.1. Main Results | 15 |
| B.2. Art & Design | 16 |
| B.3. Business | 17 |
| B.4. Science | 18 |
| B.5. Health & Medicine | 19 |
| B.6. Humanities & Social Science | 20 |
| B.7. Tech & Engineering | 21 |
| C. Case Study | 22 |
| D. Subfields of Different Subjects | 112 |
| E. Distributions of Image Types | 112 |
| F. Results on Different Image Types | 112 |
| G. Few-shot Results | 115 |
| H. Data Annotation Protocol | 116 |
| H.1. Data Collection | 116 |
| H.2. General Guidelines | 116 |
| H.3. Data Format and Structure | 116 |
| H.4. Quality Control and Validation | 116 |
| H.5. Handling Ambiguities | 116 |
| H.6. Ethical Considerations | 116 |
| H.7. Data Contamination Considerations | 117 |
| H.8. Example Questions | 117 |
| I. Author Contribution Statement | 117 |
| J. Version Change Log | 119 |

## A. Subject Distribution

Figure 7. MMMU contains 11.5K multimodal questions covering six broad disciplines, 30 subjects, and 183 subfields.

## B. Breakdown Results on Different Subjects

In this appendix, we show the main results and breakdown results of different models on each discipline and subject.

### B.1. Main Results

| | Validation<br>Overall<br>(900) | Test<br>Overall<br>(10,500) | Art &<br>(1,163) | Design Business<br>(1,428) | Science<br>(2,426) | Health &<br>Medicine<br>(1,752) | Human. &<br>Social Sci.<br>(947) | Tech &<br>Eng.<br>(2,784) |
|---|---|---|---|---|---|---|---|---|
| Random Choice | 22.1 | 23.9 | 24.1 | 24.9 | 21.6 | 25.3 | 22.8 | 24.8 |
| Frequent Choice | 26.8 | 25.8 | 26.7 | 28.4 | 24.0 | 24.4 | 25.2 | 26.5 |
| Expert (Worst) | 76.2 | - | - | - | - | - | - | - |
| Expert (Medium) | 82.6 | - | - | - | - | - | - | - |
| Expert (Best) | 88.6 | - | - | - | - | - | - | - |
| | Large Multimodal Models (LMMs): Text + Image as Input | | | | | | | |
| OpenFlamingo2-9B [[4]](#ref-4) | 28.7 | 26.3 | 31.7 | 23.5 | 26.3 | 26.3 | 27.9 | 25.1 |
| Kosmos2 [[63]](#ref-63) | 24.4 | 26.6 | 28.8 | 23.7 | 26.6 | 27.2 | 26.3 | 26.8 |
| Adept Fuyu-8B [[6]](#ref-6) | 27.9 | 27.4 | 29.9 | 27.0 | 25.6 | 27.0 | 32.5 | 26.4 |
| MiniGPT4-Vicuna-13B [[94]](#ref-94) | 26.8 | 27.6 | 30.2 | 27.0 | 26.2 | 26.9 | 30.9 | 27.2 |
| LLaMA-Adapter2-7B [[88]](#ref-88) | 29.8 | 27.7 | 35.2 | 25.4 | 25.6 | 30.0 | 29.1 | 25.7 |
| Otter [[34]](#ref-34) | 32.2 | 29.1 | 37.4 | 24.0 | 24.1 | 29.6 | 35.9 | 30.2 |
| CogVLM [[77]](#ref-77) | 32.1 | 30.1 | 38.0 | 25.6 | 25.1 | 31.2 | 41.5 | 28.9 |
| InstructBLIP-T5-XL [[16]](#ref-16) | 32.9 | 30.6 | 43.3 | 25.2 | 25.2 | 29.3 | 45.8 | 28.6 |
| BLIP-2 FLAN-T5-XL [[35]](#ref-35) | 34.4 | 31.0 | 43.0 | 25.6 | 25.1 | 31.8 | 48.0 | 27.8 |
| mPLUGw-OWL2* [[82]](#ref-82) | 32.7 | 32.1 | 48.5 | 25.6 | 24.9 | 32.8 | 46.7 | 29.6 |
| SPHINX* [[41]](#ref-41) | 32.9 | 32.9 | 50.9 | 27.2 | 25.3 | 34.1 | 51.2 | 27.8 |
| Qwen-VL-7B-Chat [[5]](#ref-5) | 35.9 | 32.9 | 47.7 | 29.8 | 25.6 | 33.6 | 45.3 | 30.2 |
| Bunny-3B* [[8]](#ref-8) | 38.2 | 33.0 | 44.3 | 29.5 | 26.8 | 34.5 | 50.5 | 28.7 |
| LLaVA-1.5-13B [[44]](#ref-44) | 36.4 | 33.6 | 49.8 | 28.2 | 25.9 | 34.9 | 54.7 | 28.3 |
| InstructBLIP-T5-XXL [[16]](#ref-16) | 35.7 | 33.8 | 48.5 | 30.6 | 27.6 | 33.6 | 49.8 | 29.4 |
| BLIP-2 FLAN-T5-XXL [[35]](#ref-35)<br>Emu2-Chat* [[70]](#ref-70) | 35.4<br>36.3 | 34.0<br>34.1 | 49.2<br>50.6 | 28.6<br>27.7 | 27.3<br>28.0 | 33.7<br>32.4 | 51.5<br>50.3 | 30.4<br>31.3 |
| MiniCPM-V-2* [[55]](#ref-55) | 37.1 | - | - | - | - | - | - | - |
| MiniCPM-V* [[54]](#ref-54) | 37.2 | - | - | - | - | - | - | - |
| SVIT* [[89]](#ref-89) | 38.0 | 34.1 | 48.9 | 28.0 | 26.8 | 35.5 | 50.9 | 30.7 |
| InternVL-Chat-V1.1* [[11]](#ref-11) | 39.1 | 35.3 | 53.7 | 31.7 | 28.2 | 36.5 | 56.4 | 28.0 |
| InfiMM-Zephyr-7B* [[73]](#ref-73) | 39.4 | 35.5 | 50.0 | 29.6 | 28.2 | 37.5 | 54.6 | 31.1 |
| Yi-VL-6B* [[84]](#ref-84) | 39.1 | 37.8 | 53.4 | 30.3 | 30.0 | 39.3 | 58.5 | 34.1 |
| OmniLMM-12B* [[58]](#ref-58) | 41.1 | - | - | - | - | - | - | - |
| InternLM-XComposer2-VL* [[17]](#ref-17) | 43.0 | 38.2 | 56.8 | 32.8 | 30.1 | 39.8 | 60.7 | 31.8 |
| HPT Air* [[28]](#ref-28) | 44.0 | - | - | - | - | - | - | - |
| Yi-VL-34B* [[84]](#ref-84) | 45.9 | 41.6 | 56.1 | 33.3 | 32.9 | 45.9 | 66.5 | 36.0 |
| LLaVA-1.6-34B* [[46]](#ref-46) | 51.1 | 44.7 | 58.6 | 39.9 | 36.0 | 51.2 | 70.2 | 36.3 |
| InternVL-Chat-V1.2* [[11]](#ref-11) | 51.6 | 46.2 | 62.5 | 37.6 | 37.9 | 49.7 | 70.1 | 40.8 |
| VILA1.5* [[39]](#ref-39) | 51.9 | 46.9 | 62.1 | 40.6 | 37.7 | 51.7 | 74.0 | 39.5 |
| Gemini Nano2* [[22]](#ref-22) | 32.6 | - | - | - | - | - | - | - |
| Marco-VL* | 41.2 | 40.4 | 56.5 | 31.0 | 31.0 | 46.9 | 66.5 | 33.8 |
| Reka Edge* [[62]](#ref-62) | 42.8 | - | - | - | - | - | - | - |
| Qwen-VL-PLUS* [[64]](#ref-64) | 45.2 | 40.8 | 59.9 | 34.5 | 32.8 | 43.7 | 65.5 | 32.9 |
| Marco-VL-Plus* | 46.2 | 44.3 | 57.4 | 34.7 | 38.5 | 48.7 | 72.2 | 36.7 |
| Gemini 1.0 Pro* [[22]](#ref-22) | 47.9 | - | - | - | - | - | - | - |
| Adept Fuyu-Heavy* [[19]](#ref-19) | 48.3 | - | - | - | - | - | - | - |
| Claude 3 Haiku* [[72]](#ref-72) | 50.2 | - | - | - | - | - | - | - |
| Reka Flash* [[62]](#ref-62) | 53.3 | - | - | - | - | - | - | - |
| Skywork-VL* [[31]](#ref-31) | 51.4 | 46.2 | 61.4 | 39.6 | 36.6 | 50.8 | 71.6 | 40.2 |
| Qwen-VL-MAX* [[65]](#ref-65) | 51.4 | 46.8 | 64.2 | 39.8 | 36.3 | 52.5 | 70.4 | 40.7 |
| HPT Pro* [[28]](#ref-28) | 52.0 | - | - | - | - | - | - | - |
| Claude 3 Sonnet* [[72]](#ref-72) | 53.1 | - | - | - | - | - | - | - |
| SenseChat-Vision-0423-Preview* [[68]](#ref-68) | 54.6 | 50.3 | 62.7 | 44.1 | 42.3 | 55.7 | 74.7 | 43.5 |
| Gemini 1.5 Flash* [[23]](#ref-23) | 56.1 | - | - | - | - | - | - | - |
| Reka Core* [[62]](#ref-62) | 56.3 | - | - | - | - | - | - | - |
| GPT-4V(ision) (Playground) [[60]](#ref-60) | 56.8 | 55.7 | 65.3 | 64.3 | 48.4 | 63.5 | 76.3 | 41.7 |
| Claude 3 Opus* [[72]](#ref-72) | 59.4 | - | - | - | - | - | - | - |
| Gemini 1.0 Ultra* [[22]](#ref-22) | 59.4 | - | - | - | - | - | - | - |
| Gemini 1.5 Pro* [[23]](#ref-23) | 62.2 | - | - | - | - | - | - | - |
| GPT-4o* [[61]](#ref-61) | 69.1 | - | - | - | - | - | - | - |
| | Large Language Models (LLMs): Only Text as Input | | | | | | | |
| Llama2 7B [[75]](#ref-75) | 30.1 | 28.7 | 30.7 | 27.2 | 26.7 | 27.7 | 32.6 | 29.8 |
| FLAN-T5-XXL [[14]](#ref-14) | 32.1 | 31.2 | 36.8 | 28.9 | 26.7 | 32.8 | 44.8 | 28.3 |
| + OCR | 34.7 | 31.9 | 36.2 | 28.8 | 26.2 | 32.6 | 50.5 | 29.7 |
| + LLaVA Caption | 34.8 | 31.9 | 38.4 | 27.8 | 27.0 | 33.2 | 49.9 | 28.7 |
| Vicuna-13B [[12]](#ref-12) | 33.3 | 31.0 | 35.1 | 30.1 | 24.7 | 31.4 | 44.8 | 30.1 |
| + OCR | 35.4 | 31.9 | 37.1 | 28.6 | 26.5 | 32.0 | 49.3 | 30.0 |
| + LLaVA Caption | 33.9 | 32.7 | 42.0 | 26.8 | 26.2 | 33.4 | 49.4 | 31.4 |
| GPT-4 Text [[59]](#ref-59) | 34.9 | 33.8 | 32.9 | 28.5 | 30.6 | 41.3 | 53.0 | 28.4 |

Table 4. Overall results of different models on the MMMU validation and test set. The best-performing model in each category is in-bold, and the second best is underlined. \*: results provided by the authors.

### B.2. Art & Design

| | Validation Overall | Test Overall | Art | Art Theory | Design | Music |
|---|---|---|---|---|---|---|
| | (120) | (1,163) | (231) | (429) | (169) | (334) |
| Random Choice | 29.2 | 24.1 | 23.4 | 20.3 | 19.5 | 31.7 |
| Frequent Choice | 23.3 | 26.7 | 24.2 | 23.5 | 33.7 | 29.0 |
| Expert (Worst) | 80.8 | - | - | - | - | - |
| Expert (Medium) | 84.2 | - | - | - | - | - |
| Expert (Best) | 89.2 | - | - | - | - | - |
| | Large Multimodal Models (LMMs): Text + Image as Input | | | | | |
| OpenFlamingo2-9B [[4]](#ref-4) | 40.0 | 31.7 | 36.8 | 28.4 | 27.8 | 34.4 |
| Kosmos2 [[63]](#ref-63) | 25.0 | 28.8 | 30.7 | 24.9 | 28.4 | 32.6 |
| Adept Fuyu-8B [[6]](#ref-6) | 36.7 | 29.9 | 28.6 | 26.8 | 29.0 | 35.3 |
| MiniGPT4-Vicuna-13B [[94]](#ref-94) | 29.2 | 30.2 | 28.6 | 28.7 | 40.2 | 28.1 |
| LLaMA-Adapter2-7B [[88]](#ref-88) | 29.2 | 35.2 | 38.5 | 35.4 | 41.4 | 29.3 |
| Otter [[34]](#ref-34) | 37.5 | 37.4 | 40.7 | 35.9 | 46.2 | 32.6 |
| CogVLM [[77]](#ref-77) | 40.8 | 38.0 | 43.3 | 39.2 | 44.4 | 29.6 |
| InstructBLIP-T5-XL [[16]](#ref-16) | 40.0 | 43.3 | 49.8 | 45.0 | 52.1 | 32.3 |
| BLIP-2 FLAN-T5-XL [[35]](#ref-35) | 44.2 | 43.0 | 50.2 | 45.0 | 47.3 | 33.2 |
| mPLUG-OWL2* [[82]](#ref-82) | 45.8 | 48.5 | 57.6 | 53.4 | 59.8 | 30.2 |
| SPHINX* [[41]](#ref-41) | 48.3 | 50.9 | 59.3 | 55.5 | 61.5 | 33.8 |
| Qwen-VL-7B-Chat [[5]](#ref-5) | 51.7 | 47.7 | 57.1 | 49.7 | 58.6 | 33.2 |
| Bunny-3B* [[8]](#ref-8) | 49.2 | 44.3 | 49.8 | 48.7 | 55.0 | 29.3 |
| LLaVA-1.5-13B [[44]](#ref-44) | 51.7 | 49.8 | 58.4 | 51.5 | 61.5 | 35.6 |
| InstructBLIP-T5-XXL [[16]](#ref-16) | 44.2 | 48.5 | 51.9 | 52.7 | 60.4 | 34.7 |
| BLIP-2 FLAN-T5-XXL [[35]](#ref-35)<br>Emu2-Chat* [[70]](#ref-70) | 41.7<br>55.0 | 49.2<br>50.6 | 54.5<br>59.3 | 51.5<br>54.1 | 64.5<br>63.3 | 34.7<br>33.8 |
| MiniCPM-V-2* [[55]](#ref-55) | 63.3 | - | - | - | - | - |
| MiniCPM-V* [[54]](#ref-54) | 55.8 | - | - | - | - | - |
| SVIT* [[89]](#ref-89) | 52.5 | 48.9 | 54.1 | 51.0 | 68.0 | 32.9 |
| InternVL-Chat-V1.1* [[11]](#ref-11) | 56.7 | 53.7 | 60.6 | 59.0 | 74.6 | 31.4 |
| InfiMM-Zephyr-7B* [[73]](#ref-73) | 55.8 | 50.0 | 57.1 | 57.3 | 62.1 | 29.3 |
| Yi-VL-6B* [[84]](#ref-84) | 52.5 | 53.4 | 57.6 | 61.8 | 74.0 | 29.3 |
| OmniLMM-12B* [[58]](#ref-58) | 58.3 | - | - | - | - | - |
| InternLM-XComposer2-VL* [[17]](#ref-17) | 60.0 | 56.8 | 68.0 | 63.6 | 69.2 | 34.1 |
| HPT Air* [[28]](#ref-28) | 56.7 | - | - | - | - | - |
| Yi-VL-34B* [[84]](#ref-84) | 59.2 | 56.1 | 60.6 | 61.8 | 72.8 | 37.1 |
| LLaVA-1.6-34B* [[46]](#ref-46) | 67.5 | 58.6 | 67.5 | 65.3 | 80.5 | 32.6 |
| InternVL-Chat-V1.2* [[11]](#ref-11) | 62.5 | 62.5 | 68.8 | 69.5 | 82.2 | 39.2 |
| VILA1.5* [[39]](#ref-39) | 60.8 | 62.1 | 69.3 | 69.5 | 82.2 | 37.4 |
| Marco-VL* | 57.5 | 56.5 | 64.5 | 61.8 | 75.1 | 34.7 |
| Reka-Edge* [[62]](#ref-62) | 52.5 | - | - | - | - | - |
| Qwen-VL-PLUS* [[64]](#ref-64) | 60.0 | 59.9 | 67.5 | 68.1 | 78.7 | 34.7 |
| Marco-VL-Plus* | 60.8 | 57.4 | 65.4 | 62.5 | 75.1 | 36.5 |
| Adept Fuyu-Heavy* [[19]](#ref-19) | 53.4 | - | - | - | - | - |
| Reka-Flash* [[62]](#ref-62) | 61.7 | - | - | - | - | - |
| Skywork-VL* [[31]](#ref-31) | 66.7 | 61.4 | 70.1 | 69.5 | 83.4 | 33.8 |
| Qwen-VL-MAX* [[65]](#ref-65) | 72.5 | 64.2 | 72.3 | 74.8 | 84.0 | 35.0 |
| HPT Pro* [[28]](#ref-28) | 70.0 | - | - | - | - | - |
| SenseChat-Vision-0423-Preview* [[68]](#ref-68) | 66.7 | 62.7 | 67.5 | 70.4 | 85.8 | 37.7 |
| Reka-Core* [[62]](#ref-62) | 75.9 | - | - | - | - | - |
| GPT-4V(ision) (Playground) [[60]](#ref-60) | 65.8 | 65.3 | 74.0 | 75.5 | 80.5 | 38.6 |
| Gemini 1.0 Ultra* [[22]](#ref-22) | 70.0 | - | - | - | - | - |
| | Large Language Models (LLMs): Text + Image as Input | | | | | |
| Llama2 7B [[75]](#ref-75) | 29.2 | 30.7 | 30.3 | 27.5 | 37.9 | 31.4 |
| FLAN-T5-XXL [[14]](#ref-14) | 38.3 | 36.8 | 32.0 | 36.8 | 52.1 | 32.3 |
| + OCR | 37.5 | 36.2 | 36.4 | 33.8 | 47.9 | 33.2 |
| + LLaVA Caption | 43.3 | 38.4 | 45.9 | 38.2 | 46.2 | 29.6 |
| Vicuna-13B [[12]](#ref-12) | 41.7 | 35.1 | 35.1 | 31.5 | 46.7 | 33.8 |
| + OCR | 39.2 | 37.1 | 35.5 | 32.9 | 50.3 | 36.8 |
| + LLaVA Caption | 38.3 | 42.0 | 51.1 | 42.7 | 46.2 | 32.6 |
| GPT-4 Text [[59]](#ref-59) | 35.0 | 32.9 | 35.1 | 28.7 | 47.3 | 29.6 |

Table 5. Art & Design results of different models on the MMMU validation and test set. The best-performing model in each category is in-bold, and the second best is underlined. \*: results provided by the authors.

### B.3. Business

| | Validation<br>Overall | Test<br>Overall | Accounting | Economics | Finance | Manage | Marketing |
|---|---|---|---|---|---|---|---|
| | (150) | (1,428) | (380) | (267) | (355) | (245) | (181) |
| Random Choice | 24.7 | 24.9 | 30.0 | 29.6 | 17.7 | 22.4 | 24.9 |
| Frequent Choice | 29.3 | 28.4 | 33.4 | 36.3 | 22.0 | 15.9 | 35.9 |
| Expert (Worst) | 78.0 | - | - | - | - | - | - |
| Expert (Medium) | 86.0 | - | - | - | - | - | - |
| Expert (Best) | 90.7 | - | - | - | - | - | - |
| | | | Large Multimodal Models (LMMs): Text + Image as Input | | | | |
| OpenFlamingo2-9B [[4]](#ref-4) | 28.0 | 23.5 | 24.7 | 25.8 | 19.4 | 25.3 | 22.7 |
| Kosmos2 [[63]](#ref-63) | 18.0 | 23.7 | 29.7 | 24.0 | 21.4 | 22.4 | 17.1 |
| Fuyu-8B [[6]](#ref-6) | 32.0 | 27.0 | 32.1 | 30.3 | 22.5 | 20.0 | 29.3 |
| MiniGPT4-Vicuna-13B [[94]](#ref-94) | 21.3 | 27.0 | 29.7 | 34.1 | 25.6 | 16.7 | 27.6 |
| LLaMA-Adapter2-7B [[88]](#ref-88)<br>Otter [[34]](#ref-34) | 25.3<br>24.0 | 25.4<br>24.0 | 30.8<br>30.8 | 24.7<br>29.6 | 20.6<br>17.5 | 24.9<br>16.3 | 25.4<br>24.9 |
| CogVLM [[77]](#ref-77) | 25.3 | 25.6 | 28.2 | 29.6 | 19.2 | 21.2 | 32.6 |
| InstructBLIP-T5-XL [[16]](#ref-16) | 28.0 | 25.2 | 27.6 | 31.8 | 18.0 | 22.0 | 28.7 |
| BLIP-2 FLAN-T5-XL [[35]](#ref-35) | 26.7 | 25.6 | 28.2 | 31.1 | 17.5 | 24.1 | 29.8 |
| mPLUG-OWL2* [[82]](#ref-82) | 24.7 | 25.6 | 28.7 | 29.2 | 20.3 | 22.4 | 28.7 |
| SPHINX* [[41]](#ref-41) | 24.7 | 27.2 | 25.8 | 31.8 | 22.5 | 25.7 | 34.8 |
| Qwen-VL-7B-Chat [[5]](#ref-5) | 29.3 | 29.8 | 34.2 | 29.6 | 18.9 | 32.2 | 38.7 |
| Bunny-3B* [[8]](#ref-8) | 30.7 | 29.5 | 30.5 | 33.3 | 24.2 | 25.3 | 37.6 |
| LLaVA-1.5-13B [[44]](#ref-44) | 22.7 | 28.2 | 29.2 | 33.3 | 23.7 | 23.3 | 34.3 |
| InstructBLIP-T5-XXL [[16]](#ref-16) | 24.0 | 30.6 | 34.2 | 35.6 | 23.4 | 30.2 | 30.4 |
| BLIP-2 FLAN-T5-XXL [[35]](#ref-35) | 30.0 | 28.6 | 32.4 | 33.3 | 22.5 | 26.1 | 28.7 |
| Emu2-Chat* [[70]](#ref-70) | 30.0 | 27.7 | 29.2 | 34.1 | 20.0 | 27.3 | 30.4 |
| MiniCPM-V-2* [[55]](#ref-55)<br>MiniCPM-V* [[54]](#ref-54) | 28.7<br>33.3 | -<br>- | -<br>- | -<br>- | -<br>- | -<br>- | -<br>- |
| SVIT* [[89]](#ref-89) | 27.3 | 28.0 | 28.7 | 35.6 | 22.3 | 22.9 | 33.7 |
| InternVL-Chat-V1.1* [[11]](#ref-11) | 34.7 | 31.7 | 34.5 | 34.5 | 24.5 | 29.0 | 39.2 |
| InfiMM-Zephyr-7B* [[73]](#ref-73) | 28.0 | 29.6 | 31.8 | 37.1 | 23.7 | 21.6 | 35.9 |
| Yi-VL-6B* [[84]](#ref-84) | 30.7 | 30.3 | 33.7 | 36.3 | 19.4 | 26.9 | 39.8 |
| OmniLMM-12B* [[58]](#ref-58) | 34.0 | - | - | - | - | - | - |
| InternLM-XComposer2-VL* [[17]](#ref-17) | 34.0 | 32.8 | 35.3 | 31.5 | 25.6 | 31.8 | 45.3 |
| HPT Air* [[28]](#ref-28) | 31.3 | - | - | - | - | - | - |
| Yi-VL-34B* [[84]](#ref-84) | 36.0 | 33.3 | 33.2 | 44.9 | 22.0 | 29.4 | 43.6 |
| LLaVA-1.6-34B* [[46]](#ref-46) | 46.0 | 39.9 | 41.3 | 45.3 | 32.4 | 35.9 | 49.2 |
| InternVL-Chat-V1.2* [[11]](#ref-11)<br>VILA1.5* [[39]](#ref-39) | 40.7 | 37.6 | 38.2 | 43.4<br>48.3 | 27.3<br>32.4 | 37.6 | 48.1 |
| | 43.3 | 40.6 | 41.8 | | | 35.9 | 49.2 |
| Marco-VL*<br>Reka-Edge* [[62]](#ref-62) | 30.0<br>36.0 | 31.0<br>- | 28.2<br>- | 37.1<br>- | 22.8<br>- | 31.4<br>- | 43.1<br>- |
| Qwen-VL-PLUS* [[64]](#ref-64) | 35.3 | 34.5 | 35.0 | 41.6 | 26.2 | 34.7 | 39.2 |
| Marco-VL-Plus* | 37.3 | 34.7 | 36.6 | 38.6 | 27.6 | 31.4 | 43.1 |
| Adept Fuyu-Heavy* [[19]](#ref-19) | 46.3 | - | - | - | - | - | - |
| Reka-Flash* [[62]](#ref-62) | 42.7 | - | - | - | - | - | - |
| Skywork-VL* [[31]](#ref-31) | 41.3 | 39.6 | 39.7 | 47.2 | 31.0 | 36.7 | 48.6 |
| Qwen-VL-MAX* [[65]](#ref-65) | 43.3 | 39.8 | 37.9 | 44.9 | 33.0 | 39.6 | 50.3 |
| HPT Pro* [[28]](#ref-28) | 43.3 | - | - | - | - | - | - |
| SenseChat-Vision-0423-Preview* [[68]](#ref-68) | 54.0 | 44.1 | 45.0 | 51.7 | 38.3 | 37.6 | 51.4 |
| Reka-Core* [[62]](#ref-62) | 47.3 | - | - | - | - | - | - |
| GPT-4V(ision) (Playground) [[60]](#ref-60) | 59.3 | 64.3 | 69.7 | 70.8 | 61.1 | 51.0 | 67.4 |
| Gemini 1.0 Ultra* [[22]](#ref-22) | 56.7 | - | - | - | - | - | - |
| | | | Large Language Models (LLMs): Text + Image as Input | | | | |
| Llama2 7B [[75]](#ref-75) | 22.7 | 27.2 | 28.9 | 34.1 | 23.7 | 21.6 | 27.6 |
| FLAN-T5-XXL [[14]](#ref-14) | 28.0 | 28.9 | 31.6 | 31.5 | 23.1 | 29.0 | 30.4 |
| + OCR | 29.3 | 28.8 | 32.4 | 30.0 | 24.8 | 26.9 | 29.8 |
| + LLaVA Caption | 31.3 | 27.8 | 28.2 | 30.7 | 24.2 | 27.8 | 29.8 |
| Vicuna-13B [[12]](#ref-12) | 26.7 | 30.1 | 29.5 | 34.8 | 25.6 | 30.6 | 32.6 |
| + OCR | 31.3 | 28.6 | 27.1 | 34.1 | 23.9 | 30.6 | 30.4 |
| + LLaVA Caption | 26.0 | 26.8 | 27.1 | 32.6 | 22.3 | 25.3 | 28.7 |
| GPT-4 Text [[59]](#ref-59) | 36.7 | 28.5 | 29.7 | 35.2 | 21.1 | 32.2 | 25.4 |

Table 6. Business results of different models on the MMMU validation and test set. The best-performing model in each category is in-bold, and the second best is underlined. \*: results provided by the authors.

### B.4. Science

| | Validation | Test | Biology | Chemistry | Geography | Math | Physics |
|---|---|---|---|---|---|---|---|
| | Overall<br>(150) | Overall<br>(2,426) | (345) | (603) | (565) | (505) | (408) |
| Random Choice | 18.0 | 21.6 | 18.3 | 18.6 | 26.0 | 22.2 | 22.1 |
| Frequent Choice | 27.3 | 24.0 | 25.8 | 19.9 | 26.9 | 26.1 | 22.1 |
| Expert (Worst) | 78.0 | - | - | - | - | - | - |
| Expert (Medium) | 84.7 | - | - | - | - | - | - |
| Expert (Best) | 90.0 | - | - | - | - | - | - |
| | | | | Large Multimodal Models (LMMs): Text + Image as Input | | | |
| OpenFlamingo2-9B [[4]](#ref-4) | 23.3 | 26.3 | 27.8 | 22.9 | 30.8 | 25.1 | 25.0 |
| Kosmos2 [[63]](#ref-63) | 19.3 | 26.6 | 28.4 | 21.7 | 29.2 | 26.7 | 28.4 |
| Fuyu-8B [[6]](#ref-6) | 22.0 | 25.6 | 27.8 | 20.9 | 30.1 | 24.8 | 25.7 |
| MiniGPT4-Vicuna-13B [[94]](#ref-94) | 28.7 | 26.2 | 23.2 | 22.1 | 29.4 | 30.1 | 25.5 |
| LLaMA-Adapter2-7B [[88]](#ref-88) | 30.7 | 25.6 | 27.5 | 24.9 | 30.4 | 23.0 | 21.3 |
| Otter [[34]](#ref-34) | 34.7 | 24.1 | 24.6 | 23.4 | 27.1 | 23.0 | 21.8 |
| CogVLM [[77]](#ref-77) | 28.0 | 25.1 | 29.3 | 24.2 | 28.0 | 23.4 | 21.1 |
| InstructBLIP-T5-XL [[16]](#ref-16) | 32.7 | 25.2 | 27.0 | 22.1 | 28.3 | 24.4 | 25.0 |
| BLIP-2 FLAN-T5-XL [[35]](#ref-35) | 30.7 | 25.1 | 26.7 | 24.4 | 25.7 | 24.0 | 25.2 |
| mPLUG-OWL2* [[82]](#ref-82) | 22.7 | 24.9 | 27.2 | 23.9 | 29.7 | 18.8 | 25.2 |
| SPHINX* [[41]](#ref-41) | 26.7 | 25.3 | 29.0 | 20.1 | 32.6 | 23.8 | 21.8 |
| Qwen-VL-7B-Chat [[5]](#ref-5) | 29.3 | 25.6 | 27.8 | 23.1 | 28.8 | 24.6 | 24.3 |
| Bunny-3B* [[8]](#ref-8) | 30.7 | 26.8 | 32.8 | 25.2 | 27.8 | 26.5 | 22.8 |
| LLaVA-1.5-13B [[44]](#ref-44)<br>InstructBLIP-T5-XXL [[16]](#ref-16) | 29.3<br>30.7 | 25.9<br>27.6 | 27.2<br>29.0 | 25.0<br>26.5 | 28.8<br>31.0 | 24.0<br>25.5 | 24.5<br>26.0 |
| BLIP-2 FLAN-T5-XXL [[35]](#ref-35) | 34.7 | 27.3 | 28.4 | 25.5 | 29.4 | 27.5 | 26.0 |
| Emu2-Chat* [[70]](#ref-70) | 28.7 | 28.0 | 28.7 | 23.5 | 35.4 | 25.3 | 27.0 |
| MiniCPM-V-2* [[55]](#ref-55) | 30.0 | - | - | - | - | - | - |
| MiniCPM-V* [[54]](#ref-54) | 28.0 | - | - | - | - | - | - |
| SVIT* [[89]](#ref-89) | 28.0 | 26.8 | 27.0 | 27.2 | 29.2 | 23.4 | 26.7 |
| InternVL-Chat-V1.1* [[11]](#ref-11) | 31.3 | 28.2 | 35.7 | 24.4 | 31.2 | 27.5 | 24.0 |
| InfiMM-Zephyr-7B* [[73]](#ref-73) | 33.3 | 28.2 | 33.0 | 24.2 | 31.7 | 27.3 | 26.0 |
| Yi-VL-6B* [[84]](#ref-84) | 31.3 | 30.0 | 32.2 | 25.0 | 34.9 | 29.9 | 28.7 |
| OmniLMM-12B* [[58]](#ref-58) | 27.3 | - | - | - | - | - | - |
| InternLM-XComposer2-VL* [[17]](#ref-17) | 34.7 | 30.1 | 34.8 | 26.0 | 34.7 | 29.7 | 26.2 |
| HPT Air* [[28]](#ref-28) | 34.7 | - | - | - | - | - | - |
| Yi-VL-34B* | 33.3 | 32.9 | 36.8 | 26.9 | 37.0 | 31.7 | 34.3 |
| LLaVA-1.6-34B* [[46]](#ref-46) | 39.3 | 36.0 | 41.4 | 29.5 | 42.7 | 33.1 | 35.3 |
| InternVL-Chat-V1.2* [[11]](#ref-11) | 39.3 | 37.9 | 40.3 | 32.0 | 44.6 | 36.6 | 36.8 |
| VILA1.5* [[39]](#ref-39) | 36.0 | 37.7 | 44.6 | 32.5 | 42.1 | 36.8 | 34.3 |
| Marco-VL* | 28.0 | 31.0 | 35.9 | 28.0 | 35.8 | 26.3 | 30.6 |
| Reka-Edge* [[62]](#ref-62) | 42.7 | - | - | - | - | - | - |
| Skywork-VL* [[31]](#ref-31) | 38.7 | 36.6 | 41.4 | 29.0 | 42.8 | 35.8 | 36.0 |
| Qwen-VL-PLUS* [[64]](#ref-64) | 37.3 | 32.8 | 40.3 | 27.9 | 34.7 | 31.3 | 33.1 |
| Marco-VL-Plus*<br>Adept Fuyu-Heavy* [[19]](#ref-19) | 35.3<br>33.7 | 38.5<br>- | 40.3<br>- | 32.5<br>- | 46.0<br>- | 36.8<br>- | 37.5<br>- |
| Reka-Flash* [[62]](#ref-62) | 47.3 | - | - | - | - | - | - |
| Qwen-VL-MAX* [[65]](#ref-65) | 40.0 | 36.3 | 38.0 | 33.3 | 39.6 | 33.7 | 38.0 |
| HPT Pro* [[28]](#ref-28) | 42.7 | - | - | - | - | - | - |
| SenseChat-Vision-0423-Preview* [[68]](#ref-68) | 45.3 | 42.3 | 44.3 | 37.0 | 47.4 | 41.8 | 41.7 |
| Reka-Core* [[62]](#ref-62) | 49.3 | - | - | - | - | - | - |
| GPT-4V(ision) (Playground) [[60]](#ref-60) | 54.7 | 48.4 | 52.2 | 46.9 | 44.8 | 45.0 | 56.4 |
| Gemini 1.0 Ultra* [[22]](#ref-22) | 48.0 | - | - | - | - | - | - |
| | Large Language Models (LLMs): Only Text as Input | | | | | | |
| Llama2 7B [[75]](#ref-75) | 34.0 | 26.7 | 28.4 | 21.4 | 29.7 | 28.5 | 26.7 |
| FLAN-T5-XXL [[14]](#ref-14) | 28.0 | 26.7 | 27.8 | 24.4 | 27.3 | 30.7 | 23.5 |
| + OCR | 30.0 | 26.2 | 24.6 | 24.5 | 27.4 | 27.9 | 26.0 |
| + LLaVA Caption | 32.7 | 27.0 | 25.8 | 23.9 | 30.3 | 29.1 | 25.5 |
| Vicuna-13B [[12]](#ref-12) | 23.3 | 24.7 | 24.6 | 22.7 | 25.0 | 26.1 | 25.7 |
| + OCR | 30.0 | 26.5 | 26.4 | 24.7 | 29.0 | 27.1 | 25.2 |
| + LLaVA Caption | 28.7 | 26.2 | 31.3 | 21.7 | 28.7 | 26.7 | 24.3 |
| GPT-4 Text [[59]](#ref-59) | 34.7 | 30.6 | 29.3 | 28.0 | 34.0 | 27.7 | 34.3 |
| | | | | | | | |

Table 7. Science results of different models on the MMMU validation and test set. The best-performing model in each category is in-bold, and the second best is underlined. \*: results provided by the authors.

### B.5. Health & Medicine

| | Validation<br>Overall<br>(150) | Test<br>Overall<br>(1,752) | Basic Medical<br>Science<br>(326) | Clinical<br>Meicine<br>(325) | Diagnostics &<br>Lab. Medicine<br>(162) | Pharmacy<br>(430) | Public<br>Health<br>(509) |
|---|---|---|---|---|---|---|---|
| Random Choice | 20.7 | 25.3 | 24.8 | 21.8 | 25.9 | 28.6 | 24.8 |
| Frequent Choice | 30.0 | 24.4 | 22.1 | 24.3 | 17.3 | 23.3 | 29.3 |
| Expert (Worst) | 73.3 | - | - | - | - | - | - |
| Expert (Medium) | 78.8 | - | - | - | - | - | - |
| Expert (Best) | 87.3 | - | - | - | - | - | - |
| | | | Large Multimodal Models (LMMs): Text + Image as Input | | | | |
| OpenFlamingo2-9B [[4]](#ref-4) | 27.3 | 26.3 | 29.1 | 21.8 | 22.2 | 32.1 | 23.8 |
| Kosmos2 [[63]](#ref-63) | 28.0 | 27.2 | 27.3 | 24.0 | 27.2 | 30.7 | 26.1 |
| Fuyu-8B [[6]](#ref-6) | 28.0 | 27.0 | 28.8 | 23.1 | 24.1 | 27.0 | 29.3 |
| MiniGPT4-Vicuna-13B [[94]](#ref-94) | 30.7 | 26.9 | 27.0 | 26.2 | 21.6 | 27.7 | 28.5 |
| LLaMA-Adapter2-7B [[88]](#ref-88) | 30.7 | 30.0 | 31.0 | 30.2 | 26.5 | 36.5 | 25.0 |
| Otter [[34]](#ref-34) | 30.7 | 29.6 | 34.4 | 28.3 | 28.4 | 28.6 | 28.5 |
| CogVLM [[77]](#ref-77) | 32.0 | 31.2 | 33.4 | 27.4 | 27.2 | 33.7 | 31.4 |
| InstructBLIP-T5-XL [[16]](#ref-16) | 28.7 | 29.3 | 31.3 | 28.9 | 22.8 | 34.2 | 26.1 |
| BLIP-2 FLAN-T5-XL [[35]](#ref-35) | 35.3 | 31.8 | 35.9 | 31.7 | 24.1 | 35.8 | 28.5 |
| mPLUG-OWL2* [[82]](#ref-82) | 32.0 | 32.8 | 29.9 | 32.3 | 34.0 | 31.2 | 29.7 |
| SPHINX* [[41]](#ref-41) | 30.7 | 34.1 | 39.9 | 36.0 | 33.3 | 31.4 | 31.8 |
| Qwen-VL-7B-Chat [[5]](#ref-5) | 33.3 | 33.6 | 38.0 | 34.8 | 32.1 | 29.5 | 33.8 |
| Bunny-3B* [[8]](#ref-8) | 40.7 | 34.5 | 39.6 | 38.5 | 33.3 | 31.4 | 31.6 |
| LLaVA-1.5-13B [[44]](#ref-44) | 38.7 | 34.9 | 42.6 | 36.6 | 34.6 | 32.1 | 31.4 |
| InstructBLIP-T5-XXL [[16]](#ref-16)<br>BLIP-2 FLAN-T5-XXL [[35]](#ref-35) | 35.3<br>32.0 | 33.6<br>33.7 | 35.6<br>38.7 | 32.3<br>34.5 | 29.6<br>27.2 | 34.2<br>33.7 | 33.8<br>32.2 |
| Emu2-Chat* [[70]](#ref-70) | 28.7 | 32.4 | 39.3 | 34.8 | 29.6 | 33.0 | 26.9 |
| MiniCPM-V-2* [[55]](#ref-55) | 30.0 | - | - | - | - | - | - |
| MiniCPM-V* [[54]](#ref-54) | 32.7 | - | - | - | - | - | - |
| SVIT* [[89]](#ref-89) | 42.0 | 35.5 | 43.3 | 36.0 | 36.4 | 34.4 | 30.8 |
| InternVL-Chat-V1.1* [[11]](#ref-11) | 39.3 | 36.5 | 43.6 | 39.7 | 36.4 | 30.9 | 34.6 |
| InfiMM-Zephyr-7B* [[73]](#ref-73) | 42.7 | 37.5 | 44.5 | 43.1 | 37.7 | 32.6 | 33.6 |
| Yi-VL-6B* [[84]](#ref-84) | 38.0 | 39.3 | 43.6 | 45.8 | 37.7 | 38.6 | 33.4 |
| OmniLMM-12B* [[58]](#ref-58) | 44.0 | - | - | - | - | - | - |
| InternLM-XComposer2-VL* [[17]](#ref-17) | 46.0 | 39.8 | 45.1 | 42.2 | 34.0 | 42.1 | 34.8 |
| HPT Air* [[28]](#ref-28) | 45.3 | - | - | - | - | - | - |
| Yi-VL-34B* [[84]](#ref-84) | 51.3 | 45.9 | 54.6 | 48.9 | 50.0 | 44.9 | 38.1 |
| LLaVA-1.6-34B* [[46]](#ref-46) | 52.0 | 51.2 | 56.4 | 58.8 | 45.1 | 50.7 | 45.4 |
| InternVL-Chat-V1.2* [[11]](#ref-11) | 58.7 | 49.7 | 58.9 | 54.5 | 43.8 | 50.0 | 42.2 |
| VILA1.5* [[39]](#ref-39) | 57.3 | 51.7 | 58.6 | 55.4 | 40.7 | 53.3 | 47.2 |
| Marco-VL* | 45.3 | 46.9 | 51.2 | 50.2 | 42.0 | 50.7 | 40.5 |
| Reka-Edge* [[62]](#ref-62) | 41.3 | - | - | - | - | - | - |
| Qwen-VL-PLUS* [[64]](#ref-64) | 46.7 | 43.7 | 49.7 | 42.2 | 34.0 | 46.5 | 41.5 |
| Marco-VL-Plus* | 48.7 | 48.7 | 57.4 | 53.5 | 40.7 | 46.5 | 44.6 |
| Adept Fuyu-Heavy* [[19]](#ref-19) | 51.3 | - | - | - | - | - | - |
| Reka-Flash* [[62]](#ref-62)<br>Skywork-VL* [[31]](#ref-31) | 59.3<br>55.3 | -<br>50.8 | -<br>58.9 | -<br>55.1 | - | -<br>50.9 | -<br>43.4 |
| Qwen-VL-MAX* [[65]](#ref-65) | 58.0 | 52.5 | 58.9 | 51.1 | 48.8<br>44.4 | 57.4 | 47.7 |
| HPT Pro* [[28]](#ref-28) | 50.7 | - | - | - | - | - | - |
| SenseChat-Vision-0423-Preview* [[68]](#ref-68) | 53.3 | 55.7 | 62.6 | 58.2 | 50.0 | 55.6 | 51.5 |
| Reka-Core* [[62]](#ref-62) | 58.0 | - | - | - | - | - | - |
| GPT-4V(ision) (Playground) [[60]](#ref-60) | 64.7 | 63.5 | 65.0 | 62.5 | 43.8 | 68.1 | 65.4 |
| Gemini 1.0 Ultra* [[22]](#ref-22) | 67.3 | - | - | - | - | - | - |
| | | | Large Language Models (LLMs): Only Text as Input | | | | |
| Llama2 7B [[75]](#ref-75) | 26.7 | 27.7 | 26.1 | 30.8 | 25.3 | 27.7 | 27.7 |
| FLAN-T5-XXL [[14]](#ref-14) | 32.0 | 32.8 | 33.7 | 34.8 | 30.2 | 34.4 | 30.5 |
| + OCR | 32.7 | 32.6 | 33.7 | 35.1 | 27.8 | 32.3 | 32.2 |
| + LLaVA Caption | 32.0 | 33.2 | 35.3 | 34.2 | 30.9 | 32.6 | 32.4 |
| Vicuna-13B [[12]](#ref-12) | 31.3 | 31.4 | 37.7 | 33.2 | 36.4 | 27.7 | 27.9 |
| + OCR | 31.3 | 32.0 | 38.3 | 33.5 | 37.0 | 28.4 | 28.5 |
| + LLaVA Caption | 34.0 | 33.4 | 37.1 | 35.4 | 32.7 | 32.6 | 30.6 |
| GPT-4 Text [[59]](#ref-59) | 40.7 | 41.3 | 52.5 | 52.9 | 27.8 | 39.1 | 33.0 |

Table 8. Health & Medicine results of different models on the MMMU validation and test set. The best-performing model in each category is in-bold, and the second best is underlined. \*: results provided by the authors.

### B.6. Humanities & Social Science

| | Validation | Test<br>History<br>Overall<br>Overall | | Literature | Sociology | Psychology | | | |
|---|---|---|---|---|---|---|---|---|---|
| | (120) | (947) | (278) | (112) | (252) | (305) | | | |
| Random Choice | 20.0 | 22.8 | 22.3 | 24.1 | 27.0 | 19.3 | | | |
| Frequent Choice | 25.8 | 25.2 | 27.0 | 27.7 | 25.4 | 22.6 | | | |
| Expert (Worst) | 74.2 | - | - | - | - | - | | | |
| Expert (Medium) | 85.0 | - | - | - | - | - | | | |
| Expert (Best) | 89.2 | - | - | - | - | - | | | |
| | Large Multimodal Models (LMMs): Text + Image as Input | | | | | | | | |
| OpenFlamingo2-9B [[4]](#ref-4) | 30.8 | 27.9 | 24.5 | 42.0 | 29.0 | 24.9 | | | |
| Kosmos2 [[63]](#ref-63) | 30.0 | 26.3 | 24.5 | 24.1 | 34.1 | 22.3 | | | |
| Fuyu-8B [[6]](#ref-6) | 32.5 | 32.5 | 32.7 | 44.6 | 32.9 | 27.5 | | | |
| MiniGPT4-Vicuna-13B [[94]](#ref-94) | 29.2 | 30.9 | 30.9 | 47.3 | 30.6 | 25.2 | | | |
| LLaMA-Adapter2-7B [[88]](#ref-88)<br>Otter [[34]](#ref-34) | 33.3<br>41.7 | 29.1<br>35.9 | 27.0<br>33.8 | 43.8<br>67.0 | 32.1<br>34.9 | 23.3<br>27.2 | | | |
| CogVLM [[77]](#ref-77) | 45.0 | 41.5 | 39.2 | 69.6 | 41.3 | 33.4 | | | |
| InstructBLIP-T5-XL [[16]](#ref-16) | 47.5 | 45.8 | 45.0 | 71.4 | 44.8 | 38.0 | | | |
| BLIP-2 FLAN-T5-XL [[35]](#ref-35) | 50.0 | 48.0 | 48.2 | 76.8 | 47.2 | 38.0 | | | |
| mPLUG-OWL2* [[82]](#ref-82) | 45.8 | 46.7 | 46.0 | 74.1 | 44.4 | 39.0 | | | |
| SPHINX* [[41]](#ref-41) | 50.0 | 51.2 | 56.5 | 81.2 | 48.0 | 38.0 | | | |
| Qwen-VL-7B-Chat [[5]](#ref-5) | 45.0 | 45.3 | 47.8 | 64.3 | 46.4 | 35.1 | | | |
| Bunny-3B* [[8]](#ref-8) | 45.0 | 50.5 | 52.2 | 78.6 | 50.0 | 39.0 | | | |
| LLaVA-1.5-13B [[44]](#ref-44) | 53.3 | 54.7 | 58.6 | 76.8 | 51.2 | 45.9 | | | |
| InstructBLIP-T5-XXL [[16]](#ref-16) | 49.2 | 49.8 | 48.6 | 72.3 | 51.2 | 41.6 | | | |
| BLIP-2 FLAN-T5-XXL [[35]](#ref-35) | 50.8 | 51.5 | 49.6 | 75.9 | 53.2 | 43.0 | | | |
| Emu2-Chat* [[70]](#ref-70) | 46.7 | 50.3 | 50.4 | 78.6 | 48.4 | 41.3 | | | |
| MiniCPM-V-2* [[55]](#ref-55)<br>MiniCPM-V* [[54]](#ref-54) | 56.7<br>58.3 | -<br>- | -<br>- | -<br>- | -<br>- | -<br>- | | | |
| SVIT* [[89]](#ref-89) | 51.7 | 50.9 | 51.8 | 75.9 | 48.8 | 42.6 | | | |
| InternVL-Chat-V1.1* [[11]](#ref-11) | 57.5 | 56.4 | 57.9 | 80.4 | 55.6 | 46.9 | | | |
| InfiMM-Zephyr-7B* [[73]](#ref-73) | 59.2 | 54.6 | 55.4 | 75.9 | 54.4 | 46.2 | | | |
| Yi-VL-6B* [[84]](#ref-84) | 53.3 | 58.5 | 59.0 | 80.4 | 55.6 | 52.5 | | | |
| OmniLMM-12B* [[58]](#ref-58) | 62.5 | - | - | - | - | - | | | |
| InternLM-XComposer2-VL* [[17]](#ref-17) | 62.5 | 60.7 | 66.5 | 87.5 | 56.3 | 49.2 | | | |
| HPT Air* [[28]](#ref-28) | 59.2 | - | - | - | - | - | | | |
| Yi-VL-34B* [[84]](#ref-84) | 62.5 | 66.5 | 69.4 | 81.2 | 65.9 | 59.0 | | | |
| LLaVA-1.6-34B* [[46]](#ref-46) | 67.5 | 70.2 | 74.8 | 91.1 | 65.9 | 62.0 | | | |
| InternVL-Chat-V1.2* [[11]](#ref-11) | 70.0 | 70.1 | 73.0 | 88.4 | 70.6 | 60.3 | | | |
| VILA1.5* [[39]](#ref-39) | 73.3 | 74.0 | 79.1 | 90.2 | 73.0 | 64.3 | | | |
| Marco-VL*<br>Reka-Edge* [[62]](#ref-62) | 65.8<br>59.2 | 66.5<br>- | 69.1<br>- | 85.7<br>- | 64.7<br>- | 58.7<br>- | | | |
| Qwen-VL-PLUS* [[64]](#ref-64) | 65.8 | 65.5 | 69.8 | 79.5 | 63.9 | 57.7 | | | |
| Marco-VL-Plus* | 69.2 | 72.2 | 78.1 | 87.5 | 68.7 | 64.3 | | | |
| Adept Fuyu-Heavy* [[19]](#ref-19) | 72.2 | - | - | - | - | - | | | |
| Reka-Flash* [[62]](#ref-62) | 74.2 | - | - | - | - | - | | | |
| Skywork-VL* [[31]](#ref-31) | 68.3 | 71.6 | 77.7 | 90.2 | 69.8 | 60.7 | | | |
| Qwen-VL-MAX* [[65]](#ref-65) | 69.2 | 70.4 | 75.9 | 89.3 | 62.7 | 64.9 | | | |
| HPT Pro* [[28]](#ref-28) | 72.5 | - | - | - | - | - | | | |
| SenseChat-Vision-0423-Preview* [[68]](#ref-68) | 75.0 | 74.7 | 78.8 | 90.2 | 72.6 | 66.9 | | | |
| Reka-Core* [[62]](#ref-62) | 75.0 | - | - | - | - | - | | | |
| GPT-4V(ision) (Playground) [[60]](#ref-60) | 72.5 | 76.3 | 79.1 | 89.3 | 71.4 | 73.1 | | | |
| Gemini 1.0 Ultra* [[22]](#ref-22) | 78.3 | - | - | - | - | - | | | |
| Large Language Models (LLMs): Only Text as Input | | | | | | | | | |
| Llama2 7B [[75]](#ref-75) | 37.5 | 32.6 | 32.4 | 46.4 | 32.9 | 27.5 | | | |
| FLAN-T5-XXL [[14]](#ref-14) | 42.5 | 44.8 | 46.8 | 56.2 | 39.7 | 43.0 | | | |
| + OCR | 55.0 | 50.5 | 53.6 | 75.0 | 46.4 | 42.0 | | | |
| + LLaVA Caption | 49.2 | 49.9 | 51.8 | 75.0 | 46.8 | 41.6 | | | |
| Vicuna-13B [[12]](#ref-12) | 45.8 | 44.8 | 51.1 | 59.8 | 39.3 | 38.0 | | | |
| + OCR | 50.0 | 49.3 | 58.3 | 66.1 | 48.0 | 36.1 | | | |
| + LLaVA Caption | 48.3 | 49.4 | 53.6 | 72.3 | 48.8 | 37.7 | | | |
| GPT-4 Text [[59]](#ref-59) | 51.7 | 53.0 | 52.9 | 82.1 | 34.5 | 57.7 | | | |

Table 9. Humanities & Social Science results of different models on the MMMU validation and test set. The best-performing model in each category is in-bold, and the second best is underlined. \*: results provided by the authors.

### B.7. Tech & Engineering

| | Val<br>Overall<br>(210) | Test<br>Overall<br>(2,784) | Agri.<br>(287) | Arch. &<br>Eng.<br>(551) | Comp.<br>Sci.<br>(371) | Electr.<br>(256) | Energy<br>&Power<br>(432) | Materials<br>(458) | Mech.<br>Eng.<br>(429) | | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Random Choice | 21.4 | 24.8 | 21.3 | 27.0 | 22.6 | 10.5 | 31.5 | 24.2 | 28.7 | | |
| Frequent Choice | 24.8 | 26.5 | 24.7 | 24.1 | 29.6 | 12.9 | 30.3 | 30.3 | 28.0 | | |
| Expert (Worst) | 74.3 | - | - | - | - | - | - | - | - | | |
| Expert (Medium) | 79.1 | - | - | - | - | - | - | - | - | | |
| Expert (Best) | 86.2 | - | - | - | - | - | - | - | - | | |
| Large Multimodal Models (LMMs): Text + Image as Input | | | | | | | | | | | |
| OpenFlamingo2-9B [[4]](#ref-4) | 26.2 | 25.1 | 20.6 | 29.6 | 26.1 | 13.7 | 24.1 | 26.0 | 28.4 | | |
| Kosmos2 [[63]](#ref-63) | 26.7 | 26.8 | 20.6 | 28.3 | 32.1 | 10.2 | 29.9 | 27.3 | 30.5 | | |
| Fuyu-8B [[6]](#ref-6) | 21.4 | 26.4 | 26.5 | 25.0 | 26.1 | 12.1 | 35.0 | 25.1 | 29.8 | | |
| MiniGPT4-Vicuna-13B [[94]](#ref-94) | 23.8 | 27.2 | 29.6 | 23.8 | 28.8 | 13.7 | 36.1 | 27.3 | 27.5 | | |
| LLaMA-Adapter2-7B [[88]](#ref-88) | 30.0 | 25.7 | 23.0 | 25.2 | 25.6 | 17.6 | 30.3 | 25.8 | 28.4 | | |
| Otter [[34]](#ref-34)<br>CogVLM [[77]](#ref-77) | 29.0<br>27.6 | 30.2<br>28.9 | 30.7<br>26.8 | 26.3<br>27.0 | 32.1<br>31.8 | 19.1<br>14.1 | 35.2<br>33.1 | 30.1<br>28.4 | 34.7<br>35.4 | | |
| InstructBLIP-T5-XL [[16]](#ref-16) | 27.1 | 28.6 | 26.1 | 33.6 | 28.3 | 23.8 | 29.9 | 22.9 | 31.5 | | |
| BLIP-2 FLAN-T5-XL [[35]](#ref-35) | 27.6 | 27.8 | 17.8 | 32.5 | 26.7 | 20.7 | 33.6 | 24.9 | 30.8 | | |
| mPLUG-OWL2* [[82]](#ref-82) | 31.0 | 29.6 | 32.4 | 29.4 | 31.8 | 14.5 | 39.4 | 26.6 | 28.2 | | |
| SPHINX* [[41]](#ref-41) | 26.2 | 27.8 | 31.0 | 26.1 | 33.7 | 16.4 | 35.2 | 23.1 | 26.8 | | |
| Qwen-VL-7B-Chat [[5]](#ref-5) | 32.9 | 30.2 | 33.1 | 25.0 | 33.4 | 19.1 | 37.0 | 28.8 | 33.1 | | |
| Bunny-3B* [[8]](#ref-8) | 37.1 | 28.7 | 32.1 | 26.0 | 34.0 | 18.8 | 33.6 | 27.5 | 27.7 | | |
| LLaVA-1.5-13B [[44]](#ref-44) | 31.4 | 28.3 | 34.5 | 26.1 | 29.6 | 22.7 | 30.1 | 26.9 | 28.9 | | |
| InstructBLIP-T5-XXL [[16]](#ref-16) | 35.2 | 29.4 | 24.7 | 30.3 | 29.6 | 20.7 | 37.3 | 26.6 | 31.5 | | |
| BLIP-2 FLAN-T5-XXL [[35]](#ref-35) | 30.0 | 30.4 | 28.2 | 27.2 | 29.6 | 25.0 | 35.6 | 26.9 | 38.0 | | |
| Emu2-Chat* [[70]](#ref-70) | 35.2 | 31.3 | 35.9 | 26.9 | 30.7 | 16.0 | 41.9 | 26.2 | 38.5 | | |
| MiniCPM-V-2* [[55]](#ref-55) | 27.1 | - | - | - | - | - | - | - | - | | |
| MiniCPM-V* [[54]](#ref-54) | 27.1 | - | - | - | - | - | - | - | - | | |
| SVIT* [[89]](#ref-89)<br>InternVL-Chat-V1.1* [[11]](#ref-11) | 33.8<br>27.1 | 30.7<br>28.0 | 29.6<br>36.9 | 27.2<br>27.2 | 34.5<br>31.5 | 21.9<br>15.2 | 37.7<br>30.6 | 27.9<br>26.0 | 34.0<br>27.0 | | |
| InfiMM-Zephyr-7B* [[73]](#ref-73) | 29.0 | 31.1 | 39.0 | 28.7 | 34.5 | 20.3 | 31.7 | 31.0 | 31.9 | | |
| Yi-VL-6B* [[84]](#ref-84) | 35.7 | 34.1 | 32.4 | 29.2 | 33.4 | 28.9 | 35.0 | 35.8 | 42.4 | | |
| OmniLMM-12B* [[58]](#ref-58) | 31.9 | - | - | - | - | - | - | - | - | | |
| InternLM-XComposer2-VL* [[17]](#ref-17) | 32.4 | 31.8 | 41.8 | 29.6 | 36.4 | 22.3 | 33.3 | 27.7 | 32.2 | | |
| HPT Air* [[28]](#ref-28) | 42.9 | - | - | - | - | - | - | - | - | | |
| Yi-VL-34B* [[84]](#ref-84) | 41.0 | 36.0 | 39.4 | 31.6 | 40.2 | 28.9 | 36.8 | 34.1 | 41.5 | | |
| LLaVA-1.6-34B* [[46]](#ref-46) | 43.8 | 36.3 | 40.1 | 31.9 | 43.7 | 27.0 | 34.0 | 34.5 | 42.7 | | |
| InternVL-Chat-V1.2* [[11]](#ref-11) | 46.2 | 40.8 | 42.9 | 32.8 | 42.6 | 32.4 | 45.8 | 40.8 | 48.0 | | |
| VILA1.5* [[39]](#ref-39) | 48.1 | 39.5 | 45.3 | 31.0 | 46.6 | 32.8 | 43.3 | 38.4 | 41.7 | | |
| Marco-VL*<br>Reka-Edge* [[62]](#ref-62) | 32.4<br>33.8 | 33.8<br>- | 35.5<br>- | 31.2<br>- | 36.7<br>- | 24.2<br>- | 34.7<br>- | 35.4<br>- | 36.4<br>- | | |
| Qwen-VL-PLUS* [[64]](#ref-64) | 36.7 | 32.9 | 40.4 | 25.6 | 36.1 | 24.6 | 33.6 | 34.7 | 36.8 | | |
| Marco-VL-Plus* | 37.1 | 36.7 | 43.9 | 27.6 | 40.2 | 34.8 | 37.7 | 34.3 | 43.1 | | |
| Adept Fuyu-Heavy* [[19]](#ref-19) | 44.0 | - | - | - | - | - | - | - | - | | |
| Reka-Flash* [[62]](#ref-62) | 44.3 | - | - | - | - | - | - | - | - | | |
| Skywork-VL* [[31]](#ref-31) | 46.7 | 40.2 | 45.3 | 31.6 | 44.5 | 32.4 | 42.4 | 38.9 | 48.3 | | |
| Qwen-VL-MAX* [[65]](#ref-65) | 38.6 | 40.7 | 45.6 | 27.6 | 42.6 | 35.2 | 48.1 | 37.8 | 51.5 | | |
| HPT Pro* [[28]](#ref-28) | 43.8 | - | - | - | - | - | - | - | - | | |
| SenseChat-Vision-0423-Preview [[68]](#ref-68) | 43.8 | 43.5 | 48.8 | 31.2 | 47.2 | 33.2 | 51.2 | 41.9 | 52.7 | | |
| Reka-Core* [[62]](#ref-62) | 44.2 | - | - | - | - | - | - | - | - | | |
| GPT-4V(ision) (Playground) [[60]](#ref-60) | 36.7 | 41.7 | 43.9 | 37.2 | 57.1 | 27.0 | 47.5 | 36.9 | 41.0 | | |
| Gemini 1.0 Ultra* [[22]](#ref-22) | 47.1 | - | - | - | - | - | - | - | - | | |
| Large Language Models (LLMs): Only Text as Input | | | | | | | | | | | |
| Llama2 7B [[75]](#ref-75) | 31.4 | 29.8 | 33.1 | 23.8 | 32.6 | 17.6 | 39.1 | 27.9 | 32.6 | | |
| FLAN-T5-XXL [[14]](#ref-14) | 28.6 | 28.3 | 21.3 | 30.3 | 28.8 | 25.4 | 26.6 | 27.9 | 33.8 | | |
| + OCR | 30.0 | 29.7 | 20.2 | 30.7 | 31.3 | 27.0 | 29.9 | 29.0 | 35.9 | | |
| + LLaVA Caption | 27.6 | 28.7 | 17.8 | 31.4 | 26.4 | 24.2 | 32.4 | 26.4 | 35.7 | | |
| Vicuna-13B [[12]](#ref-12) | 34.8 | 30.1 | 31.7 | 26.3 | 28.8 | 25.4 | 39.4 | 26.4 | 32.6 | | |
| + OCR | 34.8 | 30.0 | 31.7 | 25.6 | 29.9 | 18.8 | 40.3 | 27.5 | 33.6 | | |
| + LLaVA Caption | 32.4 | 31.4 | 32.4 | 26.9 | 31.8 | 20.3 | 39.8 | 28.8 | 37.3 | | |
| GPT-4 Text [[59]](#ref-59) | 20.0 | 28.4 | 28.9 | 25.6 | 33.4 | 17.2 | 38.4 | 23.6 | 28.9 | | |

Table 10. Tech & Engineering results of different models on the MMMU validation and test set. The best-performing model in each category is in-bold, and the second best is underlined. \*: results provided by the authors.

## C. Case Study

### List of Case Study Figures

| | | |
|---|---|---|
| 8 | Art 1: Correct Case | 25 |
| 9 | Art 2: Correct Case | 26 |
| 10 | Art 3: Perceptual Error | 27 |
| 11 | Art Theory 1: Correct Case | 28 |
| 12 | Art Theory 2: Correct Case | 29 |
| 13 | Art Theory 3: Lack of Knowledge | 30 |
| 14 | Design 1: Correct Case | 31 |
| 15 | Design 2: Perceptual Error | 32 |
| 16 | Design 3: Lack of Knowledge | 33 |
| 17 | Music 1: Correct Case | 34 |
| 18 | Music 2: Perceptual Error, Lack of Knowledge | 35 |
| 19 | Music 3: Perceptual Error | 36 |
| 20 | Accounting 1: Correct Case | 37 |
| 21 | Accounting 2: Perceptual Error | 38 |
| 22 | Economics 1: Correct Case | 39 |
| 23 | Economics 2: Perceptual Error | 40 |
| 24 | Economics 3: Perceptual Error | 41 |
| 25 | Finance 1: Correct Case | 42 |
| 26 | Finance 2: Reasoning Error | 43 |
| 27 | Manage 1: Correct Case | 44 |
| 28 | Manage 2: Perceptual Error | 45 |
| 29 | Marketing 1: Correct Case | 46 |
| 30 | Marketing 2: Perceptual Error | 47 |
| 31 | Biology 1: Correct Case | 48 |
| 32 | Biology 2: Reasoning Error | 49 |
| 33 | Biology 3: Reasoning Error | 50 |
| 34 | Biology 4: Reasoning Error | 51 |
| 35 | Chemistry 1: Correct Case | 52 |
| 36 | Chemistry 2: Correct Case | 53 |
| 37 | Chemistry 3: Perceptual Error, Reasoning Error | 54 |
| 38 | Chemistry 4: Lack of Knowledge | 55 |
| 39 | Geography 1: Correct Case | 56 |
| 40 | Geography 2: Reasoning Error | 57 |
| 41 | Geography 3: Perceptual Error, Reasoning Error | 58 |
| 42 | Math 1: Correct Case | 59 |
| 43 | Math 2: Perceptual Error | 60 |
| 44 | Math 3: Textual Understanding Error | 61 |
| 45 | Math 4: Reasoning Error | 62 |
| 46 | Physics 1: Correct Case | 63 |
| 47 | Physics 2: Perceptual Error | 64 |
| 48 | Basic Medical Science 1: Correct Case | 65 |
| 49 | Basic Medical Science 2: Perceptual Error | 66 |
| 50 | Clinical Medicine 1: Correct Case | 67 |
| 51 | Clinical Medicine 2: Correct Case | 68 |
| 52 | Clinical Medicine 3: Correct Case | 69 |
| 53 | Clinical Medicine 4: Perceptual Error | 70 |
| 54 | Clinical Medicine 5: Lack of Knowledge | 71 |
| 55 | Diagnostics and Lab Medicine 1: Correct Case | 72 |
| 56 | Diagnostics and Lab Medicine 2: Perceptual Error | 73 |

| | | |
|---|---|---|
| 57 | Diagnostics and Lab Medicine 3: Reject to Answer | 74 |
| 58 | Diagnostics and Lab Medicine 4: Perceptual Error, Lack of Knowledge | 75 |
| 59 | Pharmacy 1: Correct Case | 76 |
| 60 | Pharmacy 2: Lack of Knowledge | 77 |
| 61 | Pharmacy 3: Lack of Knowledge | 78 |
| 62 | Public Health 1: Correct Case | 79 |
| 63 | Public Health 2: Textual Understanding Error | 80 |
| 64 | Public Health 3: Lack of Knowledge | 81 |
| 65 | History 1: Correct Case | 82 |
| 66 | History 2: Correct Case | 83 |
| 67 | History 3: Perceptual Error | 84 |
| 68 | History 4: Lack of Knowledge | 85 |
| 69 | Literature 1: Correct Case | 86 |
| 70 | Literature 2: Perceptual Error | 87 |
| 71 | Sociology 1: Correct Case | 88 |
| 72 | Sociology 2: Reasoning Error | 89 |
| 73 | Psychology 1: Correct Case | 90 |
| 74 | Psychology 2: Perceptual Error | 91 |
| 75 | Agriculture 1: Correct Case | 92 |
| 76 | Agriculture 2: Perceptual Error | 93 |
| 77 | Agriculture 3: Perceptual Error | 94 |
| 78 | Agriculture 4: Perceptual Error | 95 |
| 79 | Architecture and Engineering 1: Correct Case | 96 |
| 80 | Architecture and Engineering 2: Correct Case | 97 |
| 81 | Architecture and Engineering 3: Reasoning Error | 98 |
| 82 | Computer Science 1: Correct Case | 99 |
| 83 | Computer Science 2: Perceptual Error, Lack of Knowledge | 100 |
| 84 | Computer Science 3: Perceptual Error | 101 |
| 85 | Computer Science 4: Perceptual Error | 102 |
| 86 | Electronics 1: Correct Case | 103 |
| 87 | Electronics 2: Reject to Answer | 104 |
| 88 | Energy and Power 1: Correct Case | 105 |
| 89 | Energy and Power 2: Reasoning Error | 106 |
| 90 | Materials 1: Correct Case | 107 |
| 91 | Materials 2: Lack of Knowledge | 108 |
| 92 | Mechanical Engineering 1: Correct Case | 109 |
| 93 | Mechanical Engineering 2: Reasoning Error | 110 |
| 94 | Mechanical Engineering 3: Reasoning Error | 111 |

| Subject | Correct Case | Perception | Lack of Knowledge | Reasoning | Other |
|---|---|---|---|---|---|
| Art | 8, 9 | 10 | | | |
| Art Theory | 11, 12 | | 13 | | |
| Design | 14 | 15 | 16 | | |
| Music | 17 | 18, 19 | 18 | | |
| Accounting | 20 | 21 | | | |
| Economics | 22 | 23, 24 | | | |
| Finance | 25 | | | 26 | |
| Manage | 27 | 28 | | | |
| Marketing | 29 | 30 | | | |
| Biology | 31 | | | 32, 33 | |
| Chemistry | 35, 36 | 37 | 38 | 37 | |
| Geography | 39 | 41 | | 40, 41 | |
| Math | 42 | 43 | | 45 | 44 |
| Physics | 46 | 47 | | | |
| Basic Medical Science | 48 | 49 | | | |
| Clinical Medicine | 50, 51, 52 | 53 | 54 | | |
| Diagnostics and Laboratory Medicine | 55 | 56, 58 | 58 | | 57 |
| Pharmacy | 59 | | 60, 61 | | |
| Public Health | 62 | | 64 | | 63 |
| History | 65, 66 | 67 | 68 | | |
| Literature | 69 | 70 | | | |
| Sociology | 71 | | | 72 | |
| Psychology | 73 | 74 | | | |
| Agriculture | 75 | 76, 77,78 | | | |
| Architecture and Engineering | 79 | | | 80 | |
| Computer Science | 82 | 83, 84, 85 | 83 | | |
| Electronics | 86 | | | | 87 |
| Energy and Power | 88 | | | 89 | |
| Materials | 90 | | 91 | | |
| Mechanical Engineering | 92 | | | 93, 94 | |

Table 11. Table index of case study figures by subjects with associated (error) categories.

## Art: Visual Arts

**Question:**The artist's use of color and neutral tones helps convey primarily which of the following themes? <image 1>
**Option:**(A) the inequities of societies

(B) the innocence of youth

(C) the conveniences of technology

(D) the threat of climate change

![](_page_24_Picture_8.jpeg)

<image 1>
**GPT-4V:**The artist's use of color and neutral tones in this picture, along with the chosen imagery, helps convey the theme of "the inequities of societies" (A). The contrast between the small child laboring to pull the rickshaw and the larger, relaxed adults taking a selfie is a stark commentary on social and economic disparities. The neutral background emphasizes the subjects, drawing the viewer's attention to the inequality presented within the scene.

## Ground Truth: (A) the inequities of societies

**Explanation:**The work depicts a small boy pulling a rickshaw in which two adults are seated. The boy, the rickshaw, and the background are all depicted with shades of gray and black. By contrast, the couple in the rickshaw is depicted in full color. Even without this use of color, the work would convey a theme of inequity because a little boy is pulling two adults, who seem to represent Western culture. The color contrast underscores the theme because one culture is depicted as bright, happy, and colorful, while the other is depicted as small and drab.

> Figure 8. A sample correct case of Art (subfield: Visual Arts). [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

**Ground Truth: (C) Photo 3**
Figure 9. A sample correct case of Art (subfield: Photography). [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Art: Fine Arts

**Question:**A main function of castles was to provide a defense against invaders. This was achieved by several devices, including water-filled moats and barbicans, high stone walls surrounding the castle. Another such device was battlements (or crenellations). These were alternating sections of wall, called merlons, and openings, called embrasures. The embrasures were used for firing arrows. They also permitted boulders to be dropped on attackers attempting to scale the castle walls. If you were going to write an alternate caption for <image 1>, you might note that this castle was equipped with

## Option:

- (A) a barbican and a moat.
- (B) merlons but not embrasures.
- (C) a moat and crenellations.
- (D) a barbican and battlements.

![](_page_26_Picture_8.jpeg)

<image 1>
**GPT-4V:**The correct alternate caption for the image based on the provided information would be: (C) a moat and crenellations.

### Error Category: Perceptual Error

**Error Reason:**GPT-4V fails to interpret the image. Based on the image and the explanation, the analysis should be 'we cannot actually see if there is a moat or not'. However, GPT-4V incorrectly thinks there's a moat and gives a wrong answer.

### Ground Truth: (D) a barbican and battlements.

**Explanation:**We can see that the castle has outer walls with battlements on top, but we cannot actually see if there is a moat or not.

Figure 10. A sample error case of Art (subfield: Fine Arts). Error category: Perceptual Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

![](_page_27_Figure_0.jpeg)

Figure 11. A sample correct case of Art Theory (subfield: Art History). [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Art Theory: Art Criticism

**Question:**What is NOT exhibited in the painting? <image 1>**Option:**(A) hierarchical scale

(B) graphic representation of horror and despair

(C) a sense of immediacy and drama

(D) use of sharply contrasting light and shade

![](_page_28_Picture_7.jpeg)

<image 1>
**GPT-4V:**Based on the painting provided:

- (A) hierarchical scale This technique, where figures or objects are represented in varying sizes to indicate their relative importance or position in the narrative, is evident in the painting. The central figures are larger and more pronounced, while secondary figures and elements are smaller or placed in the background.
- (B) graphic representation of horror and despair This is clearly exhibited in the painting. The expressions on the faces of the figures, their body language, and the overall chaotic scene depict horror and despair.
- (C) a sense of immediacy and drama The dynamic poses, facial expressions, and the chaotic nature of the scene give a strong sense of immediacy and drama.
- (D) use of sharply contrasting light and shade The painting employs a technique known as chiaroscuro, where light and shade are used to give depth, volume, and a three-dimensional effect to the subjects. This is evident in the way light falls on certain figures, highlighting them, while others are in shadow.
- Given these observations, the correct answer is:
- (A) hierarchical scale.
**Ground Truth: (A) hierarchical scale**

Figure 12. A sample correct case of Art Theory (subfield: Art Criticism). [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Art Theory: Art History

**Question:**The original placement of this painting was**Option:**- (A) in the Prado Museum in Madrid, showing a willingness to be compared to great Spanish painters of the past
- (B) in the cathedral in Madrid, indicating a desire to find acceptance with the Catholic Church
- (C) in the study of King Philip IV, challenging him to consider the multitude of interpretations the painting represents
- (D) in the reception room at the Royal Palace in Madrid, where the portraits of the royal family would be viewable by visiting dignitaries

![](_page_29_Picture_6.jpeg)

<image 1>
**GPT-4V:**This painting is "Las Meninas" by Diego Velázquez. The original placement of this painting was**(A) in the Prado Museum in Madrid**, showing a willingness to be compared to great Spanish painters of the past.

## Error Category: Lack of knowledge

**Error Reason:**GPT-4V successfully recognizes that the painting is Las Meninas (1656), painted by Velazquez, showcasing its perceptual ability. However, it does not know the fact that the work was placed in the study of King Philip IV. GPT-4V suggests that the painting was placed in Prado Museum in Madrid, and even provides a reason to support this answer, which is the willingness to be compared to great Spanish painters in the past. This shows some reasoning ability. However, the original placement is a piece of factual knowledge; the reasoning was based on incorrect knowledge and it led to a wrong answer. This behavior illustrates that GPT-4V lacks specific art knowledge.
**Ground Truth: (C) in the study of King Philip IV, challenging him to consider the multitude of interpretations the painting represents**
Figure 13. A sample error case of Art Theory (subfield: Art History). Error category: Lack of Knowledge [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Design : Industrial Design

**Question:**In the Robie House Dining room, what design elements were used to create a 'room within a room' vibe? <image 1>
**Option:**(A) Tall backs of chairs and lamps at the corners of dining tables

(B) Low-back chairs and pendant lights in the center

(C) Circular dining tables and wall-mounted shelves

(D) Folding chairs and floor-standing lamps

![](_page_30_Picture_8.jpeg)

<image 1>
**GPT-4V:**Based on the image you've provided of the Robie House Dining room, the design elements used to create a 'room within a room' vibe are:(A) Tall backs of chairs and lamps at the corners of dining tables.
**Ground Truth: (A) Tall backs of chairs and lamps at the corners of dining tables**

Figure 14. A sample correct case of Design (subfield: Industrial Design). [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Design: Design History

**Question:**The painting <image 1> reflects contemporary culture primarily through the mapping of**Option:**(A) consumerism and national identities

(B) flight paths and time intervals

(C) sports car and racing signage

(D) information systems on the Internet

![](_page_31_Picture_6.jpeg)

<image 1>
**GPT-4V:**The painting (<image 1>) appears to be a complex and abstract representation with various lines, patterns, and colors. Based on the visual elements in the painting:(D) information systems on the Internetseems to be the most fitting description. The interconnected lines and vibrant, diverse patterns might suggest the vastness and complexity of information systems on the Internet. However, art interpretation can be subjective, and different viewers may see different meanings in the same piece.

### Error Category: Perceptual Error

**Error Reason:**The model failed to recognize and interpret the symbolic elements of national flags present in the image, which are key indicators of 'consumerism and national identities', leading to an incorrect answer.

### Ground Truth: (D) information systems on the Internet

**Explanation:**The painting reflects contemporary culture's consumerism and national identities through its visual elements that evoke the commercial marketplace and specific country symbols. Bright colors and recognizable patterns may suggest mass-produced goods and advertising, a common commentary on consumer culture in contemporary art. Additionally, abstract representations of flags, national colors, or iconic images could signify different countries' identities, illustrating the global interconnectedness of consumerism where products and brands cross borders and adapt to local cultures. The painting's complexity and layering mirror the saturated, interconnected nature of our globalized world, where the flow of consumer goods and cultural symbols creates a vibrant, dynamic map of modern life.

Figure 15. A sample error case of Design (subfield: Design History). Error category: Perceptual Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Design: Design History

**Question:**The double-tiered columns allowed for all of the following EXCEPT (<image 1>)**Option:**(A) barrel-vaulted roofing

(B) decorative rhythm and repetition

- (C) a higher roof to make up for the short columns
- (D) the entrance of light and air into the hall

![](_page_32_Picture_7.jpeg)

<image 1>
**GPT-4V:**The double-tiered columns in the image provided would allow for: (A) barrel-vaulted roofing (B) decorative rhythm and repetition (C) a higher roof to make up for the short columns. However, the double-tiered columns would not directly affect: (D) the entrance of light and air into the hall. So the correct answer is (D) the entrance of light and air into the hall.

## Error Category: Lack of Knowledge

**Error Reason:**The error reason is a lack of specific subject knowledge: the incorrect response suggests that double-tiered columns would not affect the entrance of light and air, which is not necessarily true. Architecturally, double-tiered columns do not prevent light and air from entering; such features are more influenced by the building's windows and overall design rather than the column structure itself. The correct answer should be that double-tiered columns would not allow for barrel-vaulted roofing, as the Mezquita features flat ceilings above the arches.

### Ground Truth: (A) barrel-vaulted roofing

**Explanation**: The double-tiered columns depicted in the image, characteristic of Islamic architecture like that found in the Mosque-Cathedral of Córdoba, are not designed to support a barrel-vaulted roof; instead, they serve other purposes. These arches create a visually striking pattern of rhythm and repetition, elevate the roofline by stacking arches, which compensates for the shorter columns, and contribute to the structure's stability. However, they are not related to the entrance of light and air, which is typically managed by windows, nor are they structurally supportive of a barrelvaulted roof, as their design and construction cater to a flat roofing system. Hence, the correct answer is "barrel-vaulted roofing," as it is the element not facilitated by the double-tiered columns.

Figure 16. A sample error case of Design (subfield: Design History). Error category: Lack of Knowledge [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

![](_page_33_Figure_0.jpeg)

**Ground Truth: (A) <image 1>**
![](_page_33_Figure_2.jpeg)

| Music : Music | |
|---|---|
| Question: Choose the name for the following interval. <image 1=""/><br>Option:<br>(A) Perfect 6th<br>(B) Compound perfect 4th<br>(C) Major 6th<br>(D) Minor 6th<br><image 1=""/><br>GPT-4V:<br>The interval shown in the image is a "major 6th." It spans from the first note, F, to the<br>second note, D. In a standard diatonic scale, the interval from F to D is a sixth, and since the key<br>signature does not indicate any flats or sharps that would alter the D, it remains a major sixth. The<br>options "perfect 6th" and "compound perfect 4th" do not exist in music theory as "perfect" is used<br>for unison, 4th, 5th, and octave intervals. A "minor 6th" would require the D to be flattened, which | |
| is not the case here.<br>Error Category: Perceptual Error, Lack of knowledge<br>Error Reason: The model immediately recognized it as a 6th interval, but got confused whether it's<br>a major 6th or a minor 6th. A closer look at the response reveals that the model failed to recognize<br>the starting and ending notes of the interval. The first note is actually G, but the model mistook it<br>for the adjacent not F. The second note is Eb, and the model might have simply deduced that it was<br>D based on the assumption of major 6th + F. Additionally, the model's mistaken identification of a<br>compound perfect 4th indicates a lack of subject knowledge. | |
**Ground Truth: (D) Minor 6th**
Figure 18. A sample error case of Music (subfield: Music). Error category: Perceptual Error, Lack of Knowledge [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

![](_page_35_Figure_0.jpeg)

### <image 1>

**GPT-4V:**In response to your inquiry, I examined the provided image for the presence of a compound minor third interval in the right-hand part starting from bar 13. A compound minor third, or a tenth, combines an octave (twelve semitones) with a minor third (three semitones), totaling fifteen semitones. Upon inspection, I found that bar 17 doesn't have this interval in the right-hand part. Bars 14 and 15 do contain intervals, but I'm uncertain if any are a compound minor third. I can't confirm the presence of this interval in bars 28 and 29, as they're not visible in the image. Bar 18 also requires checking for this interval. Unfortunately, I can't process the image visually to provide the exact bar number of the specified interval.

### Error Category: Perceptual Error

**Error Reason:**Surprisingly, the model fails to find the corresponding bar number based on the relative location of labeled bars. This is a simple visual inference task for humans.
**Ground Truth: (A) 28 and 29**
Figure 19. A sample error case of Music (subfield: Music). Error category: Perceptual Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Accounting : Investment

**Question:**Consider the three stocks in the following table. Pt represents price at time t, and Qt represents shares outstanding at time t. Stock C splits two for one in the last period. Calculate the rate of return on a price-weighted index of the three stocks for the first period ( t 0 to t 1).**Option:**## (A) 4.17%

(B) 4.03%

(C) 3.89%

| | $P_0$ | $Q_0$ | | Q1 | | $Q_{2}$ |
|---|---|---|---|---|---|---|
| A | 90 | 100 | 95 | 100 | 95 | 100 |
| B | 50 | 200 | 45 | 200 | 45 | 200 |
| | 100 | 200 | 110 | 200 | 55 | 400 |

<image 1>
**GPT-4V:**To calculate the rate of return on a price-weighted index of the three stocks for the first period (t0 to t1), follow these steps: Calculate the initial index value at t0. Calculate the index value at t1. Compute the rate of return using the two index values.

Initial Index Value at t0: Price-weighted index value at 0 = (0() + 0() + 0()) / 3 = (90 + 50 + 100) / 3 = 80 Index Value at t1: Price-weighted index value at 1 = (1() + 1() + 1()) / 3 = (95 + 45 + 110) / 3 = 83.33 Rate of Return: Rate of Return = (Index Value at t1 - Index Value at t0) / Index Value at t0 = (83.33 − 80) / 80 = 0.041625 = 4.1625% Therefore, the rate of return on a price-weighted index of the three stocks for the first period is approximately 4.17%. The correct answer is:**(A) 4.17%**

**Ground Truth: (A)**. %**Explanation:** At t = 0, the value of the index is: (90 + 50 + 100)/3 = 80. At = 1, the value of the index is: (95 + 45 + 110)/3 = 83.333. The rate of return is: (83.333/80) − 1 = 4.17%

> Figure 20. A sample correct case of Accounting (subfield: Investment). [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Accounting: Financial Accounting

**Question:**From the following Company Y adjusted trial balance, what is the retained earnings to be reported?<image 1>
**Option:**(A) \$17,800 (B) \$16,800 (C) \$15,550 (D) \$12,280

| **Adjusted Trial Balance** | | | | |
|---|---|---|---|---|
| | **Debit** | Credit | | |
| Cash | \$32,000 | | | |
| Accounts receivable | 17,300 | | | |
| Prepaid insurance | 6.400 | | | |
| Land | 10,000 | | | |
| Accounts payable | | \$10,900 | | |
| Salaries payable | | 6,000 | | |
| Common stock | | 31,000 | | |
| Retained earnings | | 4.200 | | |
| **Dividends** | 8.000 | | | |
| Service revenue | | 74,000 | | |
| Insurance expense | 5,600 | | | |
| Salaries expense | 24,000 | | | |
| Miscellaneous expense | 22,800 | | | |
| | 126,100 | 126,100 | | |

<image 1>
**GPT-4V:**To calculate the retained earnings to be reported for Company Y from the adjusted trial balance, we need to consider the following components:

1. Beginning Retained Earnings: This would be the retained earnings balance at the start of the period. However, since it is not provided, we can assume it is included in the current retained earnings figure in the trial balance or that this is the first year of operation, and as such, it would be zero.

2. Add: Net Income (or Less: Net Loss): Net income is calculated as revenues minus expenses. If expenses exceed revenues, it results in a net loss.

3. Less: Dividends: These are distributions to shareholders, which reduce retained earnings.

From the adjusted trial balance provided, the calculation would be as follows:

Net Income: Service Revenue (\$74,000) - (Insurance Expense \$5,600 + Salaries Expense \$24,000 + Miscellaneous Expense \$22,800) = \$74,000 - \$52,400 = \$21,600.

Less Dividends: \$8,000. Retained Earnings to be Reported = Beginning Retained Earnings (if not given, assumed to be included in the trial balance) + Net Income - Dividends. The trial balance shows Retained Earnings as \$6,000. Assuming this is the beginning balance and adding the net income less dividends: Retained Earnings to be Reported = \$6,000 + \$21,600 - \$8,000 = \$19,600. There is no answer matching the option.

## Error Category: Perceptual Error

**Error Reason:**GPT-4V understands the question and can know how to calculate the Retained Earnings to be Reported. Most of the calculation process is correct. However, in the final steps, GPT-4V wrongly extracts the number of Retained Earnings from the table image (should be \$4,200 instead of \$6,000).
**Ground Truth: (A) \$17,800**
Figure 21. A sample error case of Accounting (subfield: Financial Accounting). Error category: Perceptual Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Economics : Econometrics

**Question:**Figure 1 displays the number of cases of Melanoma (Mt) in the male population of a US State, from 1936 to 1972. Figure 2 shows the Spanish Industrial Production Index (IPIt), from January 1975 to March 2001. <image 1> <image 2> According to figures 1 and 2, which of the following statements is FALSE:

## Option:

- (A) IPIt displays a strong seasonality
- (B) Both time series are mean stationary
- (C) Both time series display a trending behavior

![](_page_38_Figure_7.jpeg)
**GPT-4V:**Based on the provided figures:(A) IPIt displays a strong seasonality. - This statement appears to be TRUE. Figure 2 shows consistent and repeating peaks and valleys for the Spanish Industrial Production Index (IPIt), indicative of seasonality.(B) Both time series are mean stationary. - This statement appears to be FALSE. A mean stationary time series would have a constant mean (average) over time. Both figures show a changing mean over the given time frames, particularly Figure 1 where the mean value for Melanoma cases appears to be increasing over time.(C) Both time series display a trending behavior. - This statement appears to be TRUE. Figure 1 shows an upward trend in the number of Melanoma cases over time, and Figure 2 displays fluctuations but also an overall upward trend in the Industrial Production Index. Therefore, the FALSE statement is: (B) Both time series are mean stationary.

### Ground Truth: (B) Both time series are mean stationary.

Figure 22. A sample correct case of Economics (subfield: Econometrics). [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Economics: Macroeconomics

**Question:**Question below is based on the production possibilities of two nations that can produce both crepes and paper. <image 1> Which of the following statements is true of these production possibilities?

## Option:

(A) Nation X has comparative advantage in paper production and should trade paper to Nation Y in exchange for crepes.

(B) Nation X has comparative advantage in crepe production and should trade crepes to Nation Y in exchange for paper

(C) Nation X has absolute advantage in paper production, and Nation Y has absolute advantage in crepe production. No trade is possible.

(D) Nation Y has absolute advantage in paper production, and Nation X has absolute advantage in crepe production. No trade is possible.

(E) Nation Y has comparative advantage in crepe production and should trade paper to Nation X in exchange for crepes.

| Industry | **Economic Forecast** |
|---|---|
| a. Housing construction<br>b. Health care<br>c. Gold mining<br>d. Steel production | (i) Deep recession: falling inflation, interest rates, and GDP<br>(ii) Superheated economy: rapidly rising GDP, increasing inflation<br>and interest rates<br>(iii) Healthy expansion: rising GDP, mild inflation, low<br>unemployment<br>(iv) Stagflation: falling GDP, high inflation |

<image 1>
**GPT-4V:**To determine which nation has a comparative advantage in producing a particular good, we need to calculate the opportunity cost for each good in both nations. Opportunity cost is calculated as the amount of the other good that has to be given up to produce one unit of a particular good. Opportunity cost for Nation X: For 1 crepe, Nation X gives up producing 3 units of paper. So, opportunity cost of 1 crepe = 3 paper. For 1 paper, Nation X gives up producing 1/3 unit of crepe. So, opportunity cost of 1 paper = 1/3 crepe. Opportunity cost for Nation Y:For 1 crepe, Nation Y gives up producing 5 units of paper. So, opportunity cost of 1 crepe = 5 paper. For 1 paper, Nation Y gives up producing 1/5 unit of crepe. So, opportunity cost of 1 paper = 1/5 crepe. Comparing opportunity costs: Nation X has a lower opportunity cost (1/3 < 1/5) in producing paper than Nation Y. So, Nation X has a comparative advantage in producing paper. Nation Y has a lower opportunity cost (5 > 3) in producing crepes than Nation X. So, Nation Y has a comparative advantage in producing crepes. Given this, the statement:

(A) Nation X has comparative advantage in paper production and should trade paper to Nation Y in exchange for crepes.is the correct answer.

### Error Category: Perceptual Error

**Error Reason:**Although GPT-4V correctly identifies the numbers in the table, it fails to correctly attribute these numbers to the correct objects for production. For example, when calculating the opportunity cost of Nation X, GPT-4V makes the mistake that nation X can either produce 3 units of crepe or 9 units of piece. But in fact, according to the table, nation X can produce 3 units of paper or 9 units of crepe. This error leads to the incorrect calculation of opportunity cost and the incorrect answer.
**Ground Truth: (A) Nation X has comparative advantage in paper production and should trade paper to Nation Y in exchange for crepes.**
Figure 23. A sample error case of Economics (subfield: Macroeconomics). Error category: Perceptual Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

![](_page_40_Figure_0.jpeg)

Figure 24. A sample error case of Economics (subfield: Macroeconomics). Error category: Perceptual Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Finance: Corporate Finance

**Question:**Spike Equino is the CEO of a private medical equipment company that is proposing to sell 100,000 shares of its stock in an open auction. Suppose the company receives the bids in the following table. <image 1> What will be the company's total receipts (\$) from the sale if the auction is a uniform price auction?

| **Shares** | **Price** |
|---|---|
| 20,000 | !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! |
| 10,000 | 78 |
| 15,000 | 73 |
| 25,000 | 70 |
| 10,000 | 69 |
| 8,000 | 67 |
| 14,000 | 66 |
| 15,000 | 65 |
| 30,000 | 61 |

<image 1>
**GPT-4V:** In a uniform price auction, all successful bidders pay the same price per share, which is the lowest price at which the entire quantity can be sold. To determine this price, we need to accumulate the bids starting from the highest price until the total number of shares reaches or exceeds the quantity being sold (100,000 shares in this case). Using the given table: 20,000 shares at \$8010,000 shares at \$7815,000 shares at \$7325,000 shares at \$7010,000 shares at \$698,000 shares at \$6714,000 shares at \$6615,000 shares at \$6530,000 shares at \$61. Accumulating the shares: 20,000 shares (total: 20,000) 10,000 shares (total: 30,000) 15,000 shares (total: 45,000) 25,000 shares (total: 70,000) 10,000 shares (total: 80,000) 8,000 shares (total: 88,000) 14,000 shares (total: 102,000). We can see that after accumulating the first 7 bids, we exceed the 100,000 shares being sold. Therefore, the price that every successful bidder will pay is \$66 per share (which is the lowest bid price that allows the company to sell all 100,000 shares). To calculate the company's total receipts from the sale: 100,000 shares × \$66/share = \$6,600,000.

The company's total receipts from the sale will be \$6,600,000.

## Ground Truth: \$6600000

Figure 25. A sample correct case of Finance (subfield: Corporate Finance). [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Finance : Financial Marketing

**Question:**<image 1> Which point designates the optimal portfolio of risky assets?**Option:**(A) Point E

- (B) Point F
- (C) Point G
- (D) Point H

![](_page_42_Figure_5.jpeg)

<image 1>
**GPT-4V:**The optimal portfolio of risky assets is the one that provides the highest expected return for a given level of risk. On the Capital Market Line (CML) or Capital Allocation Line (CAL) depicted in the graph, this is represented by the tangent point where the CAL touches the efficient frontier (the curve of possible portfolios).From the graph provided, Point F is where the CAL is tangent to the efficient frontier, which means Point F designates the optimal portfolio of risky assets. The answer is: (B) Point F.

## Error Category: Reasoning Error

**Error Reason:**GPT-4V accurately identifies point F as the optimal portfolio of risky assets in the given problem and applies the correct theoretical framework in its reasoning. However, it overlooks an important aspect of point E, which also lies on the Capital Allocation Line (CAL) and is situated at the CAL's rightmost end. Given that point E offers a higher expected return while maintaining the same Sharpe ratio as point F, it should be considered more optimal than point F. This oversight in GPT-4V's analysis leads to an incorrect conclusion, as it fails to adequately assess the significance of point E in the context of portfolio optimization.
**Ground Truth: (A) Point E**

Figure 26. A sample error case of Finance (subfield: Financial Marketing). Error category: Reasoning Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

### Manage: Cost Management

**Question:**Eastern Chemical Company produces three products. The operating results of the current year are: <image 1> The firm sets the target price of each product at 150% of the product's total manufacturing cost. It appears that the firm was able to sell Product C at a much higher price than the target price of the product and lost money on Product B. Tom Watson, CEO, wants to promote Product C much more aggressively and phase out Product B. He believes that the information suggests that Product C has the greatest potential among the firm's three products because the actual selling price of Product C was almost 50% higher than the target price, while the firm was forced to sell Product B at a price below the target price. Both the budgeted and actual factory overhead for the current year are \$510,000. The actual units sold for each product also are the same as the budgeted units. The firm uses direct labor dollars to assign manufacturing overhead costs. The direct materials and direct labor costs per unit for each product are: <image 2> The controller noticed that not all products consumed factory overhead similarly. Upon further investigation, she identified the following usage of factory overhead during the year: <image 3> Determine the manufacturing cost per unit for Product A using the volume-based method

| <image 1=""/> | | | | | | <image 2=""/> | | |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |
| | | | | | | | | |
| | | <image 3=""/> | | | | | | |
**GPT-4V:**To determine the manufacturing cost per unit for Product A using the volume-based method, we'll follow these steps: Calculate the total overhead rate. Calculate the total manufacturing cost for Product A. Calculate the manufacturing cost per unit for Product A.1. Calculate the total overhead rate: Overhead rate = Total Factory Overhead / Total Direct Labor Dollars. Using the information given: Total Factory Overhead = \$510,000, Direct labor cost for: Product A = \$20.00, Product B = \$12.00, Product C = \$10.00. Sales Quantity: Product A = 1,000 units, Product B = 5,000 units, Product C = 500 units. Total Direct Labor Dollars = (Product A direct labor cost per unit × Product A Sales Quantity) + (Product B direct labor cost per unit × Product B Sales Quantity) + (Product C direct labor cost per unit × Product C Sales Quantity) = (\$20.00 × 1,000) + (\$12.00 × 5,000) + (\$10.00 × 500)= \$20,000 + \$60,000 + \$5,000= \$85,000

Overhead Rate:= Total Factory Overhead / Total Direct Labor Dollars= \$510,000 / \$85,000 = \$6 per direct labor dollar2. Calculate the total manufacturing cost for Product A:Manufacturing cost = Direct Materials + Direct Labor + Overhead. Using the information given for Product A:Direct Materials = \$50.00, Direct Labor = \$20.00, Overhead = Overhead Rate × \$20.00= \$120.00Total Manufacturing Cost for Product A:= Direct Materials + Direct Labor + Overhead= \$50.00 + \$20.00 + \$120.00= \$190.003. Calculate the manufacturing cost per unit for Product A:Since the actual units sold for each product are the same as the budgeted units, we can use the given sales quantity for Product A:Manufacturing Cost Per Unit for Product A:= Total Manufacturing Cost for Product A / Product A Sales Quantity= \$190,000 units= \$0.19 per unit (This seems too low, there might be an error in our calculations or in the given data.).

However, since we're asked for the manufacturing cost per unit, \$190.00 is the correct manufacturing cost per unit for Product A using the volume-based method.
**Ground Truth: \$190**

Figure 27. A sample correct case of Manage (subfield: Cost Management). [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

![](_page_44_Figure_0.jpeg)

**Question:**Look at the situation in the <image 1>. You are traveling on a plane with a small child. The cabin is depressurized and the oxygen mask falls from the ceiling. Which of these pictures shows the reconciliation of egoism and other-isms (the order is from left to right, top to bottom)?
**Option:**(A) 1

(B) 2 (C) 3

![](_page_44_Figure_5.jpeg)

<image 1>
**GPT-4V:**The image shows three situations on a plane when the oxygen mask falls: The adult puts on the mask first while the child watches (egoism).The adult puts the mask on the child first while struggling for breath. Both the adult and the child share the mask. The reconciliation of egoism and other-isms would be a situation where both the individual's needs and the needs of others are considered and addressed. Therefore, the correct answer is: (C) 3

### Error Category: Perceptual Error

**Error Reason:**GPT-4V recalled the right knowledge and made the right reasoning, but it failed to correctly map the IDs to the corresponding illustrations in the figure, which is not explicitly marked in the figure but is only described in text (the order is from left to right, top to bottom).
**Ground Truth: (B) 2**
Figure 28. A sample error case of Manage (subfield: Management Models). Error category: Perceptual Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Marketing: Market Research

**Question:**A golf instructor is interested in determining if her new technique for improving players' golf scores is effective. She takes four (4) new students. She records their 18-hole scores before learning the technique and then after having taken her class. She conducts a hypothesis test. The data are as Table 10.27. <image 1>

## Option:

(A) a test of two independent means

- (B) a test of two proportions
- (C) a test of a single mean
- (D) a test of a single proportion

| | Player 1 | Player 2 | Player 3 | Player 4 |
|---|---|---|---|---|
| Mean score before class | 83 | 78 | 93 | 87 |
| Mean score after class | !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! | !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! | !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! | !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! |
| **Table 10.27** | | | | |

<image 1>
**GPT-4V:**Based on the data provided in Table 10.27, the golf instructor is comparing the mean scores of her students before and after taking her class. She is interested in determining if there's a significant difference in the mean scores of the same students before and after learning her new technique. Given this, the most appropriate statistical test to use in this scenario would be:(A) a test of two independent means.
**Ground Truth: (A) a test of two independent means**

Figure 29. A sample correct case of Marketing (subfield: Market Research). [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Marketing: Market Research

**Question:**The graph in <image 1> displays the sample sizes and percentages of people in different age and gender groups who were polled concerning their approval of Mayor Ford's actions in office. The total number in the sample of all the age groups is 1,045. Out of the males and females, what percent are males?

## Option:

(A) 44.8%

(B) 44.5%

(C) 45.7%

(D) 46.8%

![](_page_46_Figure_8.jpeg)

![](_page_46_Figure_9.jpeg)
<image 1>
**GPT-4V:**To find the percentage of males in the sample: First, we'll identify the number of males and females from the graph:

Males = 52, Females = 63, Sum of males and females = 52 + 63 = 115

Now, to calculate the percentage of males:

Percentage of males = (Number of males / Total number of males and females) × 100

= () × 100

= 45.22% The closest answer to 45.22% from the given options is:(B) 45.5%

### Error Category: Perceptual Error

**Error Reason:**GPT-4V misunderstands the percentage of male and female as the number of samples.
**Ground Truth: (C) 45.7%**

Figure 30. A sample error case of Marketing (subfield: Market Research). Error category: Perceptual Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Biology: Physiology

**Question:**The patient is a post-mature newborn. What is the most likely diagnosis? <image 1>**Option:**- (A) Vision may be restored with concave lens and refractive surgery
- (B) Vision may be restored with convex lens and refractive surgery
- (C) This condition often occurs in elderly people
- (D) This phenomenon can not be fixed by LASIK (laser-assisted in situ keratomileusis) surgery

![](_page_47_Picture_7.jpeg)

<image 1>
**GPT-4V:**The image depicts a case of myopia, or nearsightedness. In myopia, light entering the eye is focused in front of the retina rather than directly on it, which results in distant objects appearing blurred. Given the choices:(A) Vision may be restored with concave lens and refractive surgery - This is correct. A concave lens can help to spread out the light rays so that they can focus on the retina correctly. Additionally, refractive surgeries like LASIK can help correct myopia.(B) Vision may be restored with convex lens and refractive surgery - This is incorrect. Convex lenses are used for hyperopia or farsightedness, not myopia.(C) This condition often occurs in elderly people - This is not necessarily true. Myopia can begin in childhood and progress into adulthood. It is not limited to elderly people.(D) This phenomenon can not be fixed by LASIK (laser-assisted in situ keratomileusis) surgery - This is incorrect. LASIK is one of the common surgeries used to correct myopia.So, the true statement is:

(A) Vision may be restored with concave lens and refractive surgery.
**Ground Truth: (A) Vision may be restored with concave lens and refractive surgery**
Figure 31. A sample correct case of Biology (subfield: Physiology). [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Biology: Genetics

**Question:**Consider the figure <image 1> for ABC hypothesis. If wild type Arabidopsis were transformed with a chimeric gene consisting of an A class promoter fused to a B class coding sequence, which of the following arrangements (inner to outer) would be predicted?
**Option:**(A) Ca, St, St, St.

- (B) Ca, St, Se, Se.
- (C) Ca, St, Se, Pe.
- (D) Ca, St, Pe, Se.
- (E) Ca, St, St, Ca.

![](_page_48_Picture_9.jpeg)

<image 1>
**GPT-4V:**The ABC model is a classic model for understanding flower development. This model stipulates that: A-class genes alone specify sepals. A-class and B-class genes together specify petals. B-class and C-class genes together specify stamens. C-class genes alone specify carpels. Given the information, if a wild type Arabidopsis were transformed with a chimeric gene consisting of an A class promoter fused to a B class coding sequence, then the B class gene would be expressed where normally only the A class gene would be active. Here's how the flower would develop according to the modified ABC model: Whorl 1 (outermost): Normally A class genes would specify sepals, but with the B class coding sequence under the A class promoter, it would be A+B which specifies petals.

Whorl 2: A + B class genes together specify petals, and this remains unchanged.

Whorl 3: Normally B + C class genes together would specify stamens. This remains unchanged.

Whorl 4 (innermost): C class genes alone specify carpels, and this remains unchanged. So the new arrangement from innermost to outermost would be:

Ca, St, Pe, Pe. So, the arrangement from outermost to innermost would be:

Pe, Pe, St, Ca The closest match to the given options would be:

(D) Ca, St, Pe, Se.

## Error Category: Reasoning Error

**Error Reason:**GPT-4V correctly interprets the image. However, it does not correctly reason about the relationship between a 'coding sequence' and a 'class promoter'. This prevents it from correctly predicting the answer for Whorl 1 and Whorl 2.
**Ground Truth: (B) Ca, St, Se, Se.**
Figure 32. A sample error case of Biology (subfield: Genetics). Error category: Reasoning Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Biology: Genetics

**Question:**Based on <image 1> if a Hox 13 gene in a mouse was replaced with a Hox 1 gene, which of the following will be the most likely outcome?

-**Option:**(A) The mouse may develop one head and one tail
- (B) The mouse may develop two heads and no tail
- (C) The mouse may develop no head and two tails

![](_page_49_Picture_6.jpeg)

<image 1>
**GPT-4V:**The Hox genes are a group of related genes that control the body plan of an embryo along the anterior-posterior (head-tail) axis. These genes determine where limbs and other body segments will grow in a developing fetus.

In the image provided, you appear to reference a mouse with a head and a tail, with what seems to be color-coding or sequencing perhaps representing the Hox genes.

To understand the likely outcome, it's essential to consider the function of Hox genes:

Hox 1 genes are typically expressed in anterior regions of the body, such as the head.

Hox 13 genes are typically expressed in posterior regions, like the tail.

Given this information, if a Hox 13 gene in a mouse was replaced with a Hox 1 gene, the posterior region where the tail would normally develop would now be getting instructions to develop anterior structures.

Therefore, the most likely outcome is:
**(C) The mouse may develop no head and two tails.**
## Error Category: Reasoning Error
**Error Reason:**GPT-4V accurately interpreted the image and correctly recalled that "Hox 1 genes are typically expressed in anterior regions of the body, such as the head. Hox 13 genes are typically expressed in posterior regions, like the tail." The model also correctly processed most of the intermediate reasoning steps. However, the concluding statement "The mouse may develop no head and two tails" does not logically follow from the prior step: "the posterior region where the tail would normally develop would now be getting instructions to develop anterior structures."
**Ground Truth: (B) The mouse may develop two heads and no tail**
Figure 33. A sample error case of Biology (subfield: Genetics). Error category: Reasoning Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Biology: Evolution

**Question:**The diagram in <image 1> represents a section of undisturbed layers of sedimentary rock in New York State and shows the location of fossils of several closely related species. According to currently accepted evolutionary theory, which is the most probable assumption about species A, B and C?
**Option:**- (A) Species B is more abundant than species C
- (B) Species A and B are genetically identical
- (C) Both species A and C are descended from species B
- (D) Species B descended from species A
- (E) Species C existed before species B

| Species A | -Surface<br>of ground |
|---|---|
| Species B and A | |
| Species B | |
| **Species** | |
**GPT-4V:**The diagram depicts layers of sedimentary rock with fossils of different species. In sedimentary rock layers, the oldest layers are at the bottom and the youngest layers are at the top. Based on this, the order of appearance of the species from oldest to youngest is: Species C → Species B → Species A (and then A continues to exist with B). Given this order and the choices provided, the most probable assumption according to currently accepted evolutionary theory is: (D) Species B descended from species A.

## Error Category: Reasoning Error

**Error Reason:**GPT-4V correctly understands the evolutionary order of A, B and C (C → B → A). But D is a contradiction of this timeline order.
**Ground Truth: (E) Species C existed before species B**

Figure 34. A sample error case of Biology (subfield: Evolution). Error category: Reasoning Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

^&^lt;image 1>

### Chemistry: Organic Chemistry

**Question:**The configuration at C-2 and C-3 of the compound given: <image 1>**Option:**- (A) 2R, 3S
- (B) 2S, 3R
- (C) 2S, 3S
- (D) 2R, 3R

![](_page_51_Figure_6.jpeg)

<image 1>
**GPT-4V:**To determine the configuration (R or S) of a chiral center, we follow the Cahn-Ingold-Prelog (CIP) priority rules: Assign priorities based on atomic number. The atom bonded to the chiral center with the highest atomic number gets the highest priority (1). If two atoms have the same atomic number, consider the atoms they are bonded to in order to determine priority. Orient the molecule so that the atom or group with the lowest priority (4) is pointing away (in the background). Observe the order of groups 1-2-3: If the order is clockwise, the configuration is R. If the order is counterclockwise, the configuration is S. Let's determine the configuration for the two chiral centers: For C-2: Attached groups and their atomic numbers: CH3 (Carbon = 6)Cl (Chlorine = 17)H (Hydrogen = 1)C2H5 (Carbon = 6, but this will have higher priority than CH3 because the subsequent carbons in the chain will be used for breaking the tie). Priority order: ClC2H5CH3H. With the H pointing to the background, the order is 1 (Cl) to 2 (C2H5) to 3 (CH3), which is clockwise. So, the configuration at C-2 is R. For C-3: Attached groups and their atomic numbers: H (Hydrogen = 1)Cl (Chlorine = 17)CH3 (Carbon = 6)C2H5 (Carbon = 6, but like before, C2H5 will have higher priority than CH3). Priority order: ClC2H5CH3H. With the H pointing to the background, the order is 1 (Cl) to 2 (C2H5) to 3 (CH3), which is counterclockwise. So, the configuration at C-3 is S. Therefore, the correct configuration for the compound is: 2R, 3S. So, the answer is (A) 2R, 3S.
**Ground Truth: (A) 2R, 3S**

Figure 35. A sample correct case of Chemistry (subfield: Organic Chemistry). [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

![](_page_52_Figure_0.jpeg)

Figure 36. A sample correct case of Chemistry (subfield: Organic Chemistry). [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Chemistry: Inorganic Chemistry

**Question:**Which of the following Lewis (electron-dot) structures is/are wrong? <image 1>**Option:**(A) (a) (B) (a) and (d) (C) (a) and (b) (D) (d) and (e)

| $\circ = \circ = \circ$<br>$\blacksquare$<br>$\blacksquare$ | <br>н | ี :∘—่่ง—่อ<br>$\cdots$<br>J | <br>:a:<br>$H_{\text{max}}$ | |
|---|---|---|---|---|
| (a) $SO2$ | $(b)$ NH ~3~ | (c) $NO2+$ | $(d)$ NH ~4~ Cl | (e) NH ~4~ Cl |
| | | | | |

| <image 1=""/> | | | |
|---|---|---|---|
|---|---|---|---|
**GPT-4V:**Let's analyze each of the Lewis structures:(a) SO₂: The structure shows sulfur with a double bond to each oxygen atom. Each oxygen atom has two lone pairs, and sulfur has no lone pairs. This is the correct Lewis structure for SO₂.(b) NH₃: The structure shows nitrogen with a single bond to each of the three hydrogen atoms and one lone pair on nitrogen. This is the correct Lewis structure for NH₃.(c) NO₂⁺: The structure shows nitrogen with a double bond to one oxygen and a single bond to the other oxygen. The single bonded oxygen has three lone pairs, while the double bonded oxygen has two lone pairs. This results in the nitrogen having a positive charge. This is the correct Lewis structure for NO₂⁺.(d) NH₄Cl: The structure shows the ammonium ion (NH₄⁺) with nitrogen having four single bonds to four hydrogen atoms, and there's no lone pair on nitrogen. However, chlorine is shown with a single bond to a hydrogen atom, which is incorrect. Chlorine should not be bonded to hydrogen in this structure. Instead, NH₄⁺ and Cl⁻ are present as ions, and they are attracted to each other through ionic bonding.(e) NH₄Cl: This structure shows the correct ionic representation with the ammonium ion (NH₄⁺) and the chloride ion (Cl⁻) as separate entities. Based on the analysis, the incorrect Lewis structure is: (d) NH₄Cl. The correct answer is: (D) (d) and (e)

## Error Category: Perceptual Error, Reasoning Error

**Error Reason:**For choice (a), GPT-4V incorrectly recognizes the carbon atom as a sulfur atom, and even if it was a sulfur atom, there would be two electrons near the sulfur atom. Therefore, the Lewis structure in choice (a) is completely wrong and should be one of the final answers. For choice (e), even though the model correctly decides that it is correct, it still chooses a wrong option that contains (e).
**Ground Truth: (B) (a) and (d)**

Figure 37. A sample error case of Chemistry (subfield: Inorganic Chemistry). Error category: Perceptual Error, Reasoning Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

![](_page_54_Figure_0.jpeg)

**Question:**<image> Which point corresponds to a sublimation/deposition equilibrium?**Option:**![](_page_54_Figure_2.jpeg)

(B) 3

(C) 5 (D) 6

(E) 8

![](_page_54_Figure_6.jpeg)
**GPT-4V:**The graph provided is a phase diagram, which illustrates the conditions (in terms of pressure and temperature) under which different phases of a substance coexist in equilibrium. In such a diagram: The line between the solid and gas regions represents the sublimation/deposition equilibrium, where a substance can transition directly between the solid and gaseous states. The line between the solid and liquid regions represents the melting/freezing equilibrium. The line between the liquid and gas regions represents the boiling/condensation equilibrium. From the image provided, point (B) 3 is on the line between the solid and gas regions, representing the sublimation/deposition equilibrium. So, the correct answer is: (B) 3.

## Error Category: Lack of Knowledge

**Error Reason:**The model correctly describes the knowledge, but due to the lack of knowledge about the phase diagram, it thinks point 3 is the one on the line between the solid and gas regions, while the correct one is point 8.
**Ground Truth: (B) 3**
Figure 38. A sample error case of Chemistry (subfield: Inorganic Chemistry). Error category: Lack of Knowledge [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Geography: Human Geography

**Question:**The circled areas on <image 1> are all areas which**Option:**- (A) are under the control of al-Qaeda from 2001 to present
- (B) were under the control of the U.S.-led military coalition as of 2003
- (C) are home to the Kurdish peoples
- (D) are production zones of proven oil reserves
- (E) have large-scale irrigated agriculture

![](_page_55_Figure_8.jpeg)

<image 1>
**GPT-4V:**Based on the provided map, the circled areas seem to align with regions that: (D) are production zones of proven oil reserves.Many of the circled areas are in regions known for their significant oil reserves, such as parts of Saudi Arabia, Iraq, and other parts of the Middle East.
**Ground Truth: (D) are production zones of proven oil reserves**

Figure 39. A sample correct case of Geography (subfield: Human Geography). [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Geography: Physical Geography

**Question:**Which weather does 11 represent in <image 1>?**Option**:

- (A) Boreal forest climate
- (B) Moist subtropical climate
- (C) Wet-dry tropical climate
- (D) Tundra climate

![](_page_56_Picture_6.jpeg)

<image 1>

**GPT-4V:**The image appears to be a climate zone map. The zone labeled "11" corresponds to regions such as northern Canada and parts of Russia. Based on the options provided, zone "11" would represent:

(D) Tundra climate.

## Error Category: Reasoning Error

**Error Reason:**GPT-4V correctly summarize that the zone labeled "11" corresponds to regions such as northern Canada and parts of Russia, which is a correct interpretation of the map. However, GPT-4V wrongly gets the conclusion that zone "11" would be Tundra climate based on the observation.
**Ground Truth: (A) Boreal forest climate**
Figure 40. A sample error case of Geography (subfield: Physical Geography). Error category: Reasoning Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Geography: Physical Geography

**Question:**What are satellite 1, 2, 3 in <image 1>?**Option:**- (A) Terra, Aqua, Landsat 7
- (B) Aqua, Terra, Landsat 7
- (C) Landsat 7, Aqua, Terra
- (D) Landsat 7, Terra, Aqua

![](_page_57_Picture_7.jpeg)

<image 1>
**GPT-4V:**The satellites labeled in the image as:Landsat 7, Aqua, Terra So, the correct option is: (C) Landsat 7, Aqua, Terra

## Error Category: Perceptual Error, Reasoning Error

**Error Reason:**GPT-4V fails to match the cartoon image with the real satellites. Additionally, Landsat 7 is in a different path while Terra and Aqua are both in the 705 path. So 3 definitely represents Landsat 7. GPT-4V ignores the hint provided in the diagram. Given the fact that GPT-4V doesn't provide a detailed explanation of its choice, it might be a perceptual error because of wrongly matching the cartoon image with the real satellites or a reasoning error due to ignorance of the path hint.
**Ground Truth: (A) Terra, Aqua, Landsat 7**

Figure 41. A sample error case of Geography (subfield: Physical Geography). Error category: Perceptual Error, Reasoning Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

### Math: Calculus

**Question:**<image 1>The region bounded by the graph as shown above. Choose an integral expression that can be used to find the area of R.
**Option:**(A) ^∫^ ~−~ !.# \$ (B) ^∫^ ~−~ !.# \$ (C) ^∫^ ~−~ % \$ (D) ^∫^ ~−~ % \$

![](_page_58_Figure_4.jpeg)
<image 1>
**GPT-4V:**To determine the integral expression to find the area of R, we need to observe which curve is above the other in the region R. From the given graph, for the region R, f(x) (the curve represented by = & − 6% + 8 ) is above g(x) (the curve represented by = ! % % + 2). The interval over which we're integrating is from x=0 to the point where the two curves intersect, which seems to be before x=2 (based on the graph). So, the upper limit of the integral is not 2. Given the options, the only possible upper limit is x=1.5. Thus, the integral expression to find the area of R is: ^∫^ ~−~ !.# \$ The correct choice is: (A) ^∫^ ~−~ !.# \$
**Ground Truth: (A)** ^∫^ ~−~ .

> Figure 42. A sample correct case of Math (subfield: Calculus). [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Math: Graph Theory

**Question:**Consider <image 1> on the torus, with its faces labeled A through H. Give a colouring of the faces of with four colours so that faces meeting along an edge have different colours. Is such colouring possible with only three colours?

## Option:

(A) Yes

(B) No

![](_page_59_Figure_5.jpeg)

<image 1>
**GPT-4V:**To solve the problem, we can start by attempting to color the diagram with three colors and see if it's possible to do so without having two adjacent faces of the same color. Let's label our three colors as Red, Green, and Blue (for the sake of this explanation).We can begin by coloring face A with Red. Adjacent to A are B and C, so let's color B with Green and C with Blue. D is adjacent to both B and C, so it must be Red. E is adjacent to A, D, and B. Since A and D are Red and B is Green, E should be Blue. F is adjacent to C, D, and E. D is Red, E is Blue, so F should be Green. G is adjacent to D, F, and A. D is Red, F is Green, so G should be Blue. Lastly, H is adjacent to B, E, and F. B is Green, E is Blue, and F is Green. So H can be colored Red. From this coloring, it seems that we can color the diagram with three colors such that no two adjacent faces have the same color. Hence, the answer is:(A) Yes.

### Error Category: Perceptual Error

**Error Reason:** GPT-4V encounters an issue in the third step of reasoning, when it concludes, "D is adjacent to both B and C, so it must be Red." The problem begins at this point because, according to the image, D is actually adjacent to A, B, and C. The error should be identified at this step, but the model recognizes incomplete information, believing that D is only adjacent to B and C, which leads to a series of subsequent incorrect deductions.

### Ground Truth: (B) No

Figure 43. A sample error case of Math (subfield: Graph Theory). Error category: Perceptual Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

![](_page_60_Figure_0.jpeg)

AB and CD are parallel, m∠AOB = m∠COD, but we've just shown that m∠AOB is 52°, which means that our diagram or understanding has an inconsistency because m∠COD is given as 84°.However, assuming the information provided is correct and using the fact that the sum of measures of arcs intercepted by two inscribed angles that sum up to 180° will be 360°, we get: m~AB~ + m~BD~ = 360°104 + m~BD~ = 360° m~BD~ = 256°The measure of inscribed angle BOD that intercepts arc BD is: m∠BOD = ½ m~BD~ = ½(256) = 128°But, m∠BOD = 180° - m∠COD = 180° - 84° = 96°, which contradicts our previous calculation.Assuming the latter to be correct (as it's based directly on the given information), m~BD~ = 2 *m∠BOD = 2(96°) = 192°.Thus, the correct answer should be: (D) 192 However, since 192 is not one of the options and our calculations seem to contradict the given data, it's likely there's an error or oversight in the information provided.

### Error Category: Textual Understanding Error

**Error Reason:**GPT-4V does not correctly understand the symbols and terminology in mathematics or geometry. In this question, it incorrectly interprets m ~AB~ = 104 as the measure of an inscribed angle, when the correct interpretation should be the measure of an arc or a central angle. Therefore, the angle represented in the question, ∠AOB, is 104 degrees, and ∠COD is 168 degrees. Since the concept is confused right from the start, GPT4-V does not derive the correct answer in the subsequent calculations. The key to the question is to determine the angle of BOD, which is equal to the angle AOC by using the condition of parallel lines. Then, by subtracting the two given angles from 360 degrees and dividing by two, we can obtain the correct answer.
**Ground Truth: (B) 44**
Figure 44. A sample error case of Math (subfield: Geometry). Error category: Textual Understanding Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

### Math: Calculus

**Question:**A thin-walled cone-shaped cup (Figure 16-4) is to hold 36 ! of water when full. What dimensions will minimize the amount of material needed for the cup?
**Option:**(A) = 3 ~2~ , ℎ = 6 (B) = 3 ~3~ , ℎ = 4 (C) = 3 ~2~ , ℎ = 4 (D) = 2 ~6~ , ℎ = 6

![](_page_61_Figure_4.jpeg)
**GPT-4V:**Given that the volume V of the cone-shaped cup is 36 ! when it's full, the formula for the volume of a cone is:

= " ! #ℎ. From the given volume, we can set up the equation: " ! #ℎ = 36. From which, #ℎ = ^108^. (1) ^ℎ^ ^=^ "\$% &! . Next, the surface area S of the cone (which does not include the base since it's a cup) is given by: S = . Where l is the slant height of the cone.

Using the Pythagoras theorem for the right triangle formed by the radius, height, and slant height in the cone, we get: # = #+ ℎ#. From which, = #+ ℎ#. Now, substituting the value of h from equation (1) into the equation for , we get: = #+108#/'. Substituting this l value in S, we get: S = #+108#/' . To minimize the surface area, we differentiate S with respect to r and set it equal to zero.

The differentiation and solving for r would be complex. Instead, we can substitute the given r and h values from options (A) to (D) into the volume equation to see which one satisfies = 36 . The option that satisfies this and also minimizes S would be our answer. #

(A) For
$$
r = 3\sqrt{2}
$$
and $h = 6$ : $V = \frac{1}{3}\pi (3\sqrt{2})^2$ (6) = 36 $\pi$

(B) For ~ =~ ~3~ ~3~ and ~ℎ~ =~ ~4~: ~=~ " ! 3 3 # 4 ≠ 36 #

(C) For ~ =~ ~3~ ~2~ and ~ℎ~ =~ ~4~: ~=~ " ! 3 2 4 ≠ 36

(D) For
$$
r = 2\sqrt{3}
$$
and $h = 6$ : $V = \frac{1}{3}\pi (2\sqrt{3})^2 (6) = 36\pi$

From options (A) and (D) which satisfy the volume, the surface area for each needs to be calculated: (A) = (3 ~2~) (3 ~2~)#+6#. (D) = 2 ~3~ 2 ~3~ # + 6#.

Comparing the two surface areas, we can determine which one is minimal.

However, without doing the calculations, it's hard to definitively say which one is the minimal surface area. For practical purposes, the answer could be either (A) or (D) based on the volume, and one would need to compute the surface areas to confirm.

### Error Category: Reasoning Error

**Error Reason:**The volume formula seems to be correct. The errors are made during the symbol computation.
**Ground Truth: (A)**=**,** =

Figure 45. A sample error case of Math (subfield: Calculus). Error category: Reasoning Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

Figure 46. A sample correct case of Physics (subfield: Classical Mechanics). [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Physics: Optics

**Question:**A narrow beam of monochromatic light enters a lens parallel to the optic axis, as shown in the accompanying diagram. Which arrow best represents the direction of the light after leaving the lens?
**Option:**(A) arrow A

(B) arrow B

(C) arrow C

(D) arrow D

(E) arrow E

![](_page_63_Figure_8.jpeg)

<image 1>
**GPT-4V**: The given diagram depicts a converging lens (a double convex lens) and a parallel beam of monochromatic light entering it. For a converging lens, parallel rays of light that are parallel to the optic axis will be refracted in such a way that they will converge or meet at the focal point on the other side of the lens. In the provided diagram, the ray is converging towards a point after passing through the lens. Among the given options:

(A) arrow A

(B) arrow B

(C) arrow C

(D) arrow D

(E) arrow E

The direction that best represents where the light will converge after leaving the lens is (C) arrow C.

## Error Category: Perceptual Error

**Error Reason:**GPT-4Vcorrectly identifies the theory behind the reflection of a converging lens. However, when choosing the correct arrows in the diagram, it chooses arrow C instead of arrow E that converging to the focal point. This is due the perceptual error of GPT-4V on the direction of arrows, demonstrating the lacking ability in the sense of direction in the image.

### Ground Truth: (E) arrow E

**Explanation:** A horizontal beam approaching a converging lens bends and converges through the focal point

Figure 47. A sample error case of Physics (subfield: Optics). Error category: Perceptual Error [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

## Basic Medical Science: Pathophysiology

**Question:**At which level, in the photograph, do the primary vestibular axons enter the brain stem? <image 1>

## Option:

(A) The caudal medulla.

(B) The pontomedullary junction.

(C) The mid-pons.

(D) Near the mammillary bodies in the interpeduncular fossa.

![](_page_64_Picture_7.jpeg)

<image 1>
**GPT-4V:**The image you provided appears to be of the brainstem and related structures. Based on your question, you are referring to the point where the primary vestibular axons enter the brainstem. The primary vestibular axons enter the brainstem at the level of the pontomedullary junction. Therefore, the correct answer is: (B) The pontomedullary junction.
**Ground Truth: (B) The pontomedullary junction.**
Figure 48. A sample correct case of Basic Medical Science (subfield: Pathophysiology). [[Back to List of Figures]](#ref-list-of-figures) | [[Back to Table Index]](#ref-table-index)

![](_page_65_Figure_0.jpeg)

## Basic Medical Science: Cardiovascular Physiology

**Question:**<image 1> The diagram shows the front view of a human heart. Letters P, Q, R and S indicate the different chambers of the heart. Which of the following shows the sequence in which a blood cell returning from other parts of the body passes through the four chambers of the heart?**Option:**(A) R-S-P-Q (B) Q-S-R-P (C) P-R-Q-S (D) S-R-P-Q

![](_page_65_Figure_4.jpeg)
<