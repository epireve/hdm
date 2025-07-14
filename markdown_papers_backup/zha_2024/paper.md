---
cite_key: zha_2024
title: Data-centric Artificial Intelligence: A Survey
authors: Daochen Zha, Zaid Pervaiz Bhat, Kwei-Herng Lai, Fan Yang, Zhimeng Jiang, Shaochen Zhong, Xia Hu
year: 2024
doi: 10.48550/arXiv.2303.10158
url: https://arxiv.org/abs/2303.10158
relevancy: High
tldr: First comprehensive survey providing global view of data lifecycle tasks and systematic data engineering for AI systems
insights: Shift from model design to data quality enhancement represents fundamental paradigm change; systematic data engineering crucial for AI success; data-centric approach addresses three key goals: training data development, inference data development, and data maintenance
summary: This survey addresses the emerging concept of data-centric AI, where attention has shifted from advancing model design to enhancing data quality and quantity. The paper discusses the necessity of data-centric AI, followed by a holistic view of three general data-centric goals and representative methods. The authors provide the first comprehensive survey offering a global view of tasks across various stages of the data lifecycle, aiming to help readers grasp the broad picture of systematic data engineering for building AI systems.
research_question: "How can we systematically engineer data for building AI systems across the entire data lifecycle to improve AI performance and reliability?"
methodology: Holistic review of data-centric AI across three goals: training data development, inference data development, and data maintenance; systematic analysis of data lifecycle tasks; comprehensive methodology review for data quality enhancement
key_findings: Shift from model design to data quality enhancement represents fundamental paradigm change; systematic data engineering crucial for AI success; first comprehensive framework for understanding data-centric AI approaches
limitations: Emerging field with evolving methodologies; standardization of data-centric approaches still developing; evaluation metrics for data quality improvements need refinement
conclusion: Systematic data engineering is crucial for AI success, with data quality being more important than model architecture refinements in many applications
future_work: Develop standardized data-centric methodologies; create comprehensive evaluation frameworks; explore domain-specific data engineering approaches
implementation_insights: Emphasizes systematic data engineering over model development; provides framework for data lifecycle management; offers practical guidance for data quality improvement
tags:
  - Data-centric AI
  - Machine Learning
  - Data Quality
  - Data Engineering
  - AI Systems
---

# Data-centric Artificial Intelligence: A Survey

DAOCHEN ZHA, Rice University, United States ZAID PERVAIZ BHAT, Texas A&M University, United States KWEI-HERNG LAI, Rice University, United States FAN YANG, Rice University, United States ZHIMENG JIANG, Texas A&M University, United States SHAOCHEN ZHONG, Rice University, United States XIA HU, Rice University, United States

Artificial Intelligence (AI) is making a profound impact in almost every domain. A vital enabler of its great success is the availability of abundant and high-quality data for building machine learning models. Recently, the role of data in AI has been significantly magnified, giving rise to the emerging concept of data-centric AI. The attention of researchers and practitioners has gradually shifted from advancing model design to enhancing the quality and quantity of the data. In this survey, we discuss the necessity of data-centric AI, followed by a holistic view of three general data-centric goals (training data development, inference data development, and data maintenance) and the representative methods. We also organize the existing literature from automation and collaboration perspectives, discuss the challenges, and tabulate the benchmarks for various tasks. We believe this is the first comprehensive survey that provides a global view of a spectrum of tasks across various stages of the data lifecycle. We hope it can help the readers efficiently grasp a broad picture of this field, and equip them with the techniques and further research ideas to systematically engineer data for building AI systems. A companion list of data-centric AI resources will be regularly updated on <https://github.com/daochenzha/data-centric-AI>

## CCS Concepts: - Computing methodologies -> Artificial intelligence.

Additional Key Words and Phrases: Artificial intelligence, machine learning, data-centric AI

### ACM Reference Format:

Daochen Zha, Zaid Pervaiz Bhat, Kwei-Herng Lai, Fan Yang, Zhimeng Jiang, Shaochen Zhong, and Xia Hu. 2023. Data-centric Artificial Intelligence: A Survey. 1, 1 (June 2023), [39](#page-38-0) pages. [https://doi.org/10.1145/nnnnnnn.](https://doi.org/10.1145/nnnnnnn.nnnnnnn) [nnnnnnn](https://doi.org/10.1145/nnnnnnn.nnnnnnn)

## 1 INTRODUCTION

The past decade has witnessed dramatic progress in Artificial Intelligence (AI), which has made a profound impact in almost every domain, such as natural language processing [\[47\]](#page-29-0), computer vision [\[236\]](#page-36-0), recommender system [\[285\]](#page-37-0), healthcare [\[161\]](#page-33-0), biology [\[249\]](#page-36-1), finance [\[175\]](#page-34-0), and so forth. A vital enabler of these great successes is the availability of abundant and high-quality data. Many major AI breakthroughs occur only after we have the access to the right training data. For example, AlexNet [\[127\]](#page-32-0), one of the first successful convolutional neural networks, was designed based on

XXXX-XXXX/2023/6-ART \$15.00

<https://doi.org/10.1145/nnnnnnn.nnnnnnn>

Figure 1. Motivating examples that highlight the central role of data in AI. On the left, large and high-quality training data are the driving force of recent successes of GPT models, while model architectures remain similar, except for more model weights. The detailed data collection strategies of GPT models are provided in [\[34,](#page-29-1) [172,](#page-34-1) [174,](#page-34-2) [187,](#page-34-3) [188,](#page-34-4) [296\]](#page-37-1). On the right, when the model becomes sufficiently powerful, we only need to engineer prompts (inference data) to accomplish our objectives, with the model being fixed.

the ImageNet dataset [\[59\]](#page-30-0). AlphaFold [\[117\]](#page-32-1), a breakthrough of AI in scientific discovery, will not be possible without annotated protein sequences [\[163\]](#page-33-1). The recent advances in large language models rely on large text data for training [\[34,](#page-29-1) [121,](#page-32-2) [187,](#page-34-3) [188\]](#page-34-4) (left of Figure [1\)](#page-1-0). Besides training data, well-designed inference data has facilitated the initial recognition of numerous critical issues in AI and unlocked new model capabilities. A famous example is adversarial samples [\[129\]](#page-32-3) that confuse neural networks through specialized modifications of input data, which causes a surge of interest in studying AI security. Another example is prompt engineering [\[146\]](#page-33-2), which accomplishes various tasks by solely tuning the input data to probe knowledge from the model while keeping the model fixed (right of Figure [1\)](#page-1-0). In parallel, the value of data has been well-recognized in industries. Many big tech companies have built infrastructures to organize, understand, and debug data for building AI systems [\[7,](#page-28-0) [15,](#page-28-1) [231,](#page-35-0) [234\]](#page-36-2). All these efforts in constructing training data, inference data, and the infrastructure to maintain data have paved the path for the achievements in AI today.

Recently, the role of data in AI has been significantly magnified, giving rise to the emerging concept of data-centric AI [\[108,](#page-31-0) [109,](#page-31-1) [183,](#page-34-5) [251,](#page-36-3) [269\]](#page-37-2). In the conventional model-centric AI lifecycle, researchers and developers primarily focus on identifying more effective models to improve AI performance while keeping the data largely unchanged. However, this model-centric paradigm overlooks the potential quality issues and undesirable flaws of data, such as missing values, incorrect labels, and anomalies. Complementing the existing efforts in model advancement, data-centric AI emphasizes the systematic engineering of data to build AI systems, shifting our focus from model to data. It is important to note that "data-centric" differs fundamentally from "data-driven", as the latter only emphasizes the use of data to guide AI development, which typically still centers on developing models rather than engineering data.

Several initiatives have already been dedicated to the data-centric AI movement. A notable one is a competition launched by Ng et al. [\[170\]](#page-33-3), which asks the participants to iterate on the dataset only to improve the performance. Snorkel [\[190\]](#page-34-6) builds a system that enables automatic data annotation with heuristic functions without hand labeling. A few rising AI companies have placed data in the central role because of many benefits, such as improved accuracy, faster deployment, and standardized workflow [\[169,](#page-33-4) [189,](#page-34-7) [241\]](#page-36-4). These collective initiatives across academia and industry demonstrate the necessity of building AI systems using data-centric approaches.

With the growing need for data-centric AI, various methods have been proposed. Some relevant research subjects are not new. For instance, data augmentation [\[74\]](#page-30-1) has been extensively investigated to improve data diversity. Feature selection [\[138\]](#page-32-4) has been studied since decades ago for preparing more concise data. Meanwhile, some new research directions have emerged recently, such as data programming for labeling data quickly [\[191\]](#page-34-8), algorithmic recourse for understanding model decisions [\[120\]](#page-32-5), and prompt engineering that modifies the input of large language models to obtain the desirable predictions [\[146\]](#page-33-2). From another dimension, some works are dedicated to making data processing more automated, such as automated data augmentation [\[56\]](#page-30-2), and automated pipeline discovery [\[68,](#page-30-3) [132\]](#page-32-6). Some other methods emphasize human-machine collaboration in creating data so that the model can align with human intentions. For example, the remarkable success of ChatGPT and GPT-4 [\[172\]](#page-34-1) is largely attributed to the reinforcement learning from human feedback procedure [\[48\]](#page-30-4), which asks humans to provide appropriate responses to prompts and rank the outputs to serve as the rewards [\[174\]](#page-34-2). Although the above methods are independently developed for different purposes, their common objective is to ensure data quality, quantity, and reliability so that the models behave as intended.

Motivated by the need for data-centric AI and the numerous proposed methods, this survey provides a holistic view of the technological advances in data-centric AI and summarizes the existing research directions. In particular, this survey centers on the following research questions:

- RQ1: What are the necessary tasks to make AI data-centric?
- RQ2: Why is automation significant for developing and maintaining data?
- RQ3: In which cases and why is human participation essential in data-centric AI?
- RQ4: What is the current progress of data-centric AI?

By answering these questions, we make three contributions. Firstly, we provide a comprehensive overview to help readers efficiently grasp a broad picture of data-centric AI from different perspectives, including definitions, tasks, algorithms, challenges, and benchmarks. Secondly, we organize the existing literature under a goal-driven taxonomy. We further identify whether human involvement is needed in each method and label the method with a level of automation or a degree of human participation. Lastly, we analyze the existing research and discuss potential future opportunities.

This survey is structured as follows. Section [2](#page-2-0) presents an overview of the concepts and tasks related to data-centric AI. Then, we elaborate on the needs, representative methods, and challenges of three general data-centric AI goals, including training data development (Section [3\)](#page-7-0), inference data development (Section [4\)](#page-16-0), and data maintenance (Section [5\)](#page-19-0). Section [6](#page-24-0) summarizes benchmarks for various tasks. Section [7](#page-26-0) discusses data-centric AI from a global view and highlights the potential future directions. Finally, we conclude this survey in Section [8.](#page-28-2)

## 2 BACKGROUND OF DATA-CENTRIC AI

This section provides a background of data-centric AI. Section [2.1](#page-2-1) defines the relevant concepts. Section [2.2](#page-3-0) discusses why data-centric AI is needed. Section [2.3](#page-4-0) draws a big picture of the related tasks and presents a goal-driven taxonomy to organize the existing literature. Section [2.4](#page-5-0) focuses on automation and human participation in data-centric AI.

## 2.1 Definitions

Researchers have described data-centric AI in different ways. Ng et al. defined it as "the discipline of systematically engineering the data used to build an AI system" [\[168\]](#page-33-5). Polyzotis and Zaharia described it as "an exciting new research field that studies the problem of constructing high-quality datasets for machine learning" [\[183\]](#page-34-5). Jarrahi et al. mentioned that data-centric AI "advocates for a systematic and iterative approach to dealing with data issues" [\[109\]](#page-31-1). Miranda noted that data-centric AI focuses on the problems that "do not only involve the type of model to use, but also the quality of data at hand" [\[162\]](#page-33-6). While all these descriptions have emphasized the importance of data, the scope of data-centric AI remains ambiguous, i.e., what tasks and techniques belong to data-centric AI. Such ambiguity could prevent us from grasping a concrete picture of this field. Before starting the survey, it is essential to define some relevant concepts:

- Artificial Intelligence (AI): AI is a broad and interdisciplinary field that tries to enable computers to have human intelligence to solve complex tasks [\[253\]](#page-36-5). A dominant technique for AI is machine learning, which leverages data to train predictive models to accomplish some tasks.
- Data: Data is a very general concept to describe a collection of values that convey information. In the context of AI, data is used to train machine learning models or serve as the model input to make predictions. Data can appear in various formats, such as tabular data, images, texts, audio, and video.
- Training Data: Training data is the data used in the training phase of machine learning models. The model leverages training data to adjust its parameters and make predictions.
- Inference Data: Inference data is the data used in the inference phase of machine learning models. On the one hand, it can evaluate the performance of the model after it has been trained. On the other hand, tuning the inference data can help obtain the desirable outputs, such as tuning prompts for language models [\[146\]](#page-33-2).
- Data Maintenance: Data maintenance refers to the process of maintaining the quality and reliability of data, which often involves efficient algorithms, tools, and infrastructures to understand and debug data. Data maintenance plays a crucial role in AI since it ensures training and inference data are accurate and consistent [\[107\]](#page-31-2).
- Data-centric AI: Data-centric AI refers to a framework to develop, iterate, and maintain data for AI systems [\[269\]](#page-37-2). Data-centric AI involves the tasks and methods for building effective training data, designing proper inference data, and maintaining the data.

### 2.2 Need for Data-centric AI

In the past, AI was often viewed as a model-centric field, where the focus was on advancing model designs given fixed datasets. However, the overwhelming reliance on fixed datasets does not necessarily lead to better model behavior in real-world applications, as it overlooks the breadth, difficulty, and fidelity of data to the underlying problem [\[155\]](#page-33-7). Moreover, the models are often difficult to transfer from one problem to another since they are highly specialized and tailored to specific problems. Furthermore, undervaluing data quality could trigger data cascades [\[200\]](#page-34-9), causing negative effects such as decreased accuracy and persistent biases [\[36\]](#page-29-2). This can severely hinder the applicability of AI systems, particularly in high-stakes domains.

Consequently, the attention of researchers and practitioners has gradually shifted toward datacentric AI to pursue data excellence [\[9\]](#page-28-3). Data-centric AI places a greater emphasis on enhancing the quality and quantity of the data with the model relatively more fixed. While this transition is still ongoing, we have already witnessed several accomplishments that shed light on its benefits. For example, the advancement of large language models is greatly dependent on the use of huge datasets [\[34,](#page-29-1) [121,](#page-32-2) [187,](#page-34-3) [188\]](#page-34-4). Compared to GPT-2 [\[188\]](#page-34-4), GPT-3 [\[34\]](#page-29-1) only made minor modifications in the neural architecture while spending efforts collecting a significantly larger high-quality dataset for training. ChatGPT [\[174\]](#page-34-2), a remarkably successful application of GPT-3, adopts a similar neural architecture as GPT-3 and uses a reinforcement learning from human feedback procedure [\[48\]](#page-30-4) to generate high-quality labeled data for fine-tuning. A new approach, known as prompt engineering [\[146\]](#page-33-2), has seen significant success by focusing solely on tuning data inputs. The benefits of data-centric approaches can also be validated by practitioners [\[169,](#page-33-4) [189,](#page-34-7) [241\]](#page-36-4). For instance, Landing AI, a computer vision company, observes improved accuracy, reduced development time, and more

![](_page_4_Figure_1.jpeg)
<!-- Image Description: The image is a hierarchical diagram outlining the key components of data-centric AI. It branches from "Data-centric AI" into three main areas: "Training data development" (including data collection, labeling, preparation, reduction, and augmentation); "Inference data development" (including in-distribution and out-of-distribution evaluation, and prompt engineering); and "Data maintenance" (including data understanding, quality assurance, and storage/retrieval). The diagram visually organizes the multifaceted aspects of data-centric AI development and management. -->

Figure 2. Data-centric AI framework.

consistent and scalable methods from the adoption of data-centric approaches [\[169\]](#page-33-4). All these achievements demonstrate the promise of data-centric AI.

It is noteworthy that data-centric AI does not diminish the value of model-centric AI. Instead, these two paradigms are complementarily interwoven in building AI systems. On the one hand, model-centric methods can be used to achieve data-centric AI goals. For example, we can utilize a generation model, such as GAN [\[86,](#page-31-3) [283\]](#page-37-3) and diffusion model [\[101,](#page-31-4) [124,](#page-32-7) [194\]](#page-34-10), to perform data augmentation and generate more high-quality data. On the other hand, data-centric AI could facilitate the improvement of model-centric AI objectives. For instance, the increased availability of augmented data could inspire further advancements in model design. Therefore, in production scenarios, data and models tend to evolve alternatively in a constantly changing environment [\[183\]](#page-34-5).

### 2.3 Tasks in Data-centric AI

The ambitious movement to data-centric AI can not be achieved without making progress on concrete and specific tasks. Unfortunately, most of the existing literature has been focused on discussing the foundations and perspectives of data-centric AI without clearly specifying the associated tasks [\[108,](#page-31-0) [109,](#page-31-1) [183,](#page-34-5) [209\]](#page-35-1). As an effort to resolve this ambiguity, the recently proposed DataPerf benchmark [\[155\]](#page-33-7) has defined six data-centric AI tasks: training set creation, test set creation, selection algorithm, debugging algorithm, slicing algorithm, and valuation algorithm. However, this flat taxonomy can only partially cover the existing data-centric AI literature. For example, some crucial tasks such as data labeling [\[284\]](#page-37-4) are not included. The selection algorithm only addresses instance selection but not feature selection [\[138\]](#page-32-4). The test set creation is restricted to selecting items from a supplemental set rather than generating a new set [\[203\]](#page-35-2). Thus, a more nuanced taxonomy is necessary to fully encompass data-centric AI literature.

To gain a more comprehensive understanding of data-centric AI, we draw a big picture of the related tasks and present a goal-driven taxonomy to organize the existing literature in Figure [2.](#page-4-1) We divide data-centric AI into three goals: training data development, inference data development, and data maintenance, where each goal is associated with several sub-goals, and each task belongs to a sug-goal. We give a high-level overview of these goals below.

- Training data development: The goal of training data development is to collect and produce rich and high-quality training data to support the training of machine learning models. It consists of five sub-goals, including 1) data collection for gathering raw training data, 2) data labeling for adding informative labels, 3) data preparation for cleaning and transforming data, 4) data reduction for decreasing data size with potentially improved performance, and 5) data augmentation for enhancing data diversity without collecting more data.

| Goal | Sub-goal | Tasks | | | |
|------------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------|--|--|--|
| Training data<br>development | Collection | Dataset discovery [28], data integration [222], raw data synthesis [133] | | | |
| | Labeling | Crowdsourced labeling [130], semi-supervised labeling [298], active learning [192],<br>data programming [191], distant supervision [160] | | | |
| | Preparation | Data cleaning [289], feature extraction [199], feature transformation [5] | | | |
| | Reduction | Feature selection [138], dimensinality reduction [2], instance selection [193] | | | |
| | Augmentation | Basic manipulation [282], augmentation data synthesis [79], upsampling [273] | | | |
| Inference data | In-distribution | Data slicing [53], algorithmic recourse [120] | | | |
| development | Out-of-distribution | Generating adversarial samples [165], generating samples with distribution shift [125] | | | |
| | | Prompt engineeringManual prompt engineering [206], automated prompt engineering [239] | | | |
| Data<br>maintenance | Understanding | Visual summarization [37], clustering for visualization [72],<br>visualization recommendation [254], valuation [83] | | | |
| | Quality assurance | Quality assessment [195], quality improvement [19] | | | |
| | Storage & retrieval | Resource allocation [100], query index selection [224], query rewriting [12] | | | |

| | | | | | | | | | Table 1. Representative tasks under the data-centric AI framework. | |
|--|--|--|--|--|--|--|--|--|--------------------------------------------------------------------|--|
|--|--|--|--|--|--|--|--|--|--------------------------------------------------------------------|--|

- Inference data development: The objective is to create novel evaluation sets that can provide more granular insights into the model or trigger a specific capability of the model with engineered data inputs. There are three sub-goals in this effort: 1) in-distribution evaluation and 2) out-of-distribution evaluation aim to generate samples that adhere to or differ from the training data distribution, respectively, while 3) prompt engineering tunes the prompt in language models to get the desired predictions. The tasks in inference data development are relatively open-ended since they are often designed to assess or unlock various capabilities of the model.
- Data maintenance: In real-world applications, data is not created once but rather necessitates continuous maintenance. The purpose of data maintenance is to ensure the quality and reliability of data in a dynamic environment. It involves three essential sub-goals: 1) data understanding, which targets providing visualization and valuation of the complex data, enabling humans to gain valuable insights, 2) data quality assurance, which develops quantitative measurements and quality improvement strategies to monitor and repair data, and 3) data storage & retrieval, which aims to devise efficient algorithms to supply the data in need via properly allocating resources and efficiently processing queries. Data maintenance plays a fundamental and supportive role in the data-centric AI framework, ensuring that the data in training and inference is accurate and reliable.

Following the three general goals, we survey various data-centric AI tasks, summarized in Table [1.](#page-5-1)

### 2.4 Automation and Human Participation in Data-centric AI

Data-centric AI consists of a spectrum of tasks related to different data lifecycle stages. To keep pace with the ever-growing size of the available data, in some data-centric AI tasks, it is imperative to develop automated algorithms to streamline the process. For example, there is an increasing interest in automation in data augmentation [\[56,](#page-30-2) [273\]](#page-37-7), and feature transformation [\[122\]](#page-32-11). Automation in these tasks will improve not only efficiency but also accuracy [\[155\]](#page-33-7). Moreover, automation can facilitate the consistency of the results, reducing the chance of human errors. Whereas for some other tasks, human involvement is essential to ensure the data is consistent with our intentions. For example, humans often play an indispensable role in labeling data [\[284\]](#page-37-4), which helps machine learning algorithms learn to make the desired predictions. Whether human participation is needed depends on whether our objective is to align data with human expectations. In this survey, we

![](_page_6_Figure_1.jpeg)
<!-- Image Description: The image is a flowchart illustrating the automation levels in data-centric AI papers. It branches from a "Data-centric AI Paper" source into "Automation" and "Collaboration" paths. Each path shows further branching into levels of automation (programmatic, learning-based, pipeline) and participation (full, partial, minimum). The diagram categorizes approaches to AI paper creation based on the degree of automation and human involvement. -->

Figure 3. Data-centric AI papers are categorized into automation and collaboration depending on whether human participation is needed. Each method has a different level of automation or requires a different degree of human participation.

categorize each paper into automation and collaboration, where the former focuses on automating the process, and the latter concerns human participation. Automation-oriented methods usually have different automation objectives. We can identify several levels of automation from the existing methods:

- Programmatic automation: Using programs to deal with the data automatically. The programs are often designed based on some heuristics and statistical information.
- Learning-based automation: Learning automation strategies with optimization, e.g., minimizing an objective function. The methods at this level are often more flexible and adaptive but require additional costs for learning.
- Pipeline automation: Integrating and tuning a series of strategies across multiple tasks, which could help identify globally optimal strategies. However, tuning may incur significantly more costs.

Note that this categorization does not intend to differentiate good and bad methods. For example, a pipeline automation method may not necessarily be better than programmatic automation solutions since it could be over-complicated in many scenarios. Instead, we aim to show insight into how automation has been applied to different data-centric goals and understand the literature from a global view. From another perspective, collaboration-oriented methods often require human participation in different forms. We can identify several degrees of human participation:

- Full participation: Humans fully control the process. The method assists humans in making decisions. The methods that require full participation can often align well with human intentions but can be costly.
- Partial participation: The method is in control of the process. However, humans need to intensively or continuously supply information, e.g., by providing a large amount of feedback or frequent interactions.
- Minimum participation: The method is in full control of the whole process and only consults humans when needed. Humans only participate when prompted or asked to do so. The methods that belong to this degree are often more desirable when encountering a massive amount of data and a limited budget for human efforts.

Similarly, the degree of human participation, to a certain extent, only reflects the tradeoff between efficiency (less human labor) and effectiveness (better aligned with humans). The selection of methods depends on the application domain and stakeholders' needs. To summarize, we design Figure [3](#page-6-0) to organize the existing data-centric AI papers. We assign each paper to either a level of automation or a degree of human participation.

![](_page_7_Figure_1.jpeg)
<!-- Image Description: This flowchart illustrates a data preparation pipeline for machine learning. It depicts the stages from data collection (using existing datasets, crowdsourcing, and other sources) through labeling, cleaning, feature transformation and reduction, data augmentation, and finally, model training. Each stage is represented by a labeled box with icons symbolizing the process, showing the flow of data from raw to augmented, ready-for-training format. -->

Figure 4. An overview of training data development. Note that the figure illustrates only a general pipeline, and not all steps are mandatory. For instance, unsupervised learning does not require data labeling. These steps can be executed in a different order as well. For example, data augmentation can occur before data reduction.

Some previous surveys only focus on specific scopes of data-centric AI, such as data augmentation [\[74,](#page-30-1) [215,](#page-35-6) [250\]](#page-36-8), data labeling [\[284\]](#page-37-4), and feature selection [\[138\]](#page-32-4). The novelty of our paper is that it provides a holistic view of the tasks, methods, and benchmarks by providing a goal-driven taxonomy to organize the tasks followed by an automation- and collaboration-oriented design to categorize methods. Moreover, we discuss the needs, challenges, and future directions from the broad data-centric AI view, aiming to motivate collective initiatives to push forward this field.

### 3 TRAINING DATA DEVELOPMENT

Training data provides the foundation for machine learning models, as the model performance is heavily influenced by its quality and quantity. In this section, we summarize the essential steps to create and process training data, visualized in Figure [4.](#page-7-1) Data creation focuses on effectively and efficiently encoding human intentions into datasets, including data collection (Section [3.1\)](#page-7-2) and data labeling (Section [3.2\)](#page-9-0). Data processing aims to make data suitable for learning, including data preparation (Section [3.3\)](#page-11-0), data reduction (Section [3.4\)](#page-12-0), and data augmentation (Section [3.5\)](#page-14-0). After introducing these steps, we discuss pipeline search (Section [3.6\)](#page-15-0), an emerging trend that aims to connect them and search for the most effective end-to-end solution. Table [2](#page-9-1) summarizes the representative tasks and methods for training data development.

### 3.1 Data Collection

Data collection is the process of gathering and acquiring data from various sources, which fundamentally determines data quality and quantity. This process heavily relies on domain knowledge. With the increasing availability of data, there has been a surge in the development of efficient strategies to leverage existing datasets. In the following, we discuss the role of domain knowledge, an overview of more efficient data collection strategies, and challenges.

3.1.1 Role of Domain Knowledge. A deep understanding of the application domain or industry is critical for collecting relevant and representative data. For example, when building a recommendation system, it is crucial to decide what user/item features to collect based on the application domain [\[285\]](#page-37-0). The domain-specific knowledge can also help in synthesizing data. For instance, knowledge about financial markets and trading strategies can facilitate the generation of more realistic synthetic anomalies [\[133\]](#page-32-8). Domain knowledge is essential for effective data collection since it helps align data with the intentions of stakeholders and ensure the data is relevant and representative.

3.1.2 Efficient Data Collection Strategies. Traditionally, datasets are constructed from scratch by manually collecting the relevant information. However, this process is time-consuming. More efficient methods have been developed by leveraging the existing data. Here, we describe the methods for dataset discovery, data integration, and data synthesis.

Dataset discovery. As the number of available datasets continuously grows, it becomes possible to amass the existing datasets of interest to construct a new dataset that meets our needs. Given a human-specified query (e.g., the expected attribute names), dataset discovery aims to identify the most related and useful datasets from a data lake, a repository of datasets stored in its raw formats, such as public data-sharing platforms [\[22\]](#page-29-5) and data marketplaces. The existing research for dataset discovery mainly differs in calculating relatedness. A representative strategy is to abstract the datasets as a graph, where the nodes are columns of the data sources, and edges represent relationships between two nodes [\[75\]](#page-30-7). Then a tailored query language is designed to allow users to express complex query logic to retrieve the relevant datasets. Another approach is table union search [\[167\]](#page-33-10), which measures the unionability of datasets based on the overlapping of the attribute values. Recent work measures the relatedness in a more comprehensive way by considering attribute names, value overlapping, word embedding, formats, and domain distributions [\[28\]](#page-29-3). All these methods can significantly reduce human labor in dataset discovery, as humans only need to provide queries.

Data integration. Given a few datasets from different sources, data integration aims to combine them into a unified dataset. The difficulty lies in matching the columns across datasets and transforming the values of data records from the source dataset to the target dataset. Traditional solutions rely on rule-based systems [\[128,](#page-32-12) [137\]](#page-32-13), which can not scale. Recently, machine learning has been utilized to automate the data integration process in a more scalable way [\[221,](#page-35-7) [222\]](#page-35-3). For example, the transformation of data values can be formulated as a classification problem, where the input is the data value from the source dataset, and the output is the transformed value from the target dataset [\[222\]](#page-35-3). Then we can train a classifier with the training data generated by rules and generalize it to unseen data records. The automated data integration techniques make it possible to merge a larger number of existing datasets efficiently.

Raw data synthesis. In some scenarios, it is more efficient to synthesize a dataset that contains the desirable patterns than to collect these patterns from the real world. A typical scenario is anomaly detection, where it is often hard to collect sufficient real anomalies since they can be extremely rare. Thus, researchers often insert anomaly patterns into anomaly-free datasets. For example, a general anomaly synthesis criterion has been proposed for time series data [\[133\]](#page-32-8), where a time series is modeled as a parameterized combination of trend, seasonality, and shapelets. Then different pointand pattern-wise anomalies can be generated by altering these parameters. However, such synthesis strategies may not be suitable for all domains. For example, the anomaly patterns in financial time series can be quite different from those from electricity time series. Thus, properly designing data synthesis strategies still requires domain knowledge.

3.1.3 Challenges. Data collection is a very challenging process that requires careful planning. From the technical perspective, datasets are often diverse and not well-aligned with each other, so it is non-trivial to measure their relatedness or integrate them appropriately. Effectively synthesizing data from the existing dataset is also tricky, as it heavily relies on domain knowledge. Moreover, some critical issues during data collection can not be resolved solely from a technical perspective. For example, in many real-world situations, we may be unable to locate a readily available dataset that aligns with our requirements so we still have to collect data from the ground up. However, some data sources can be difficult to obtain due to legal, ethical, or logistical reasons. Collecting new data also involves ethical considerations, particularly with regard to informed consent, data

### 10 Daochen Zha, Zaid Pervaiz Bhat, Kwei-Herng Lai, Fan Yang, Zhimeng Jiang, Shaochen Zhong, and Xia Hu

| Sub-goal | Task | Method type | Automation level/<br>participation degree | Reference |
|--------------|-----------------------------|---------------|-------------------------------------------|----------------------------------|
| | Dataset discovery | Collaboration | Minimum | [28, 75, 167] |
| Collection | Data integration | Automation | Programmatic | [128, 137] |
| | Data integration | Automation | Learning-based | [221, 222] |
| | Raw data synthesis | Automation | Programmatic | [133] |
| | Crowdsourced labeling | Collaboration | Full | [58, 130, 227] |
| | Semi-supervised labeling | Collaboration | Partial | [46, 174, 295, 298] |
| Labeling | Active learning | Collaboration | Partial | [55, 66, 192, 274] |
| | Data programming | Collaboration | Partial | [27, 80] |
| | Data programming | Collaboration | Minimum | [103, 190, 191, 278] |
| | Distant supervision | Automation | Learning-based | [160] |
| | Data cleaning | Automation | Programmatic | [289] |
| | Data cleaning | Automation | Learning-based | [98, 116, 126, 135] |
| | Data cleaning | Collaboration | Partial | [244] |
| Preparation | Feature extraction | Automation | Programmatic | [14, 199] |
| | Feature extraction | Automation | Learning-based | [127, 248] |
| | Feature transformation | Automation | Programmatic | [5, 24] |
| | Feature transformation | Automation | Learning-based | [122] |
| | Feature selection | Automation | Programmatic | [10, 229] |
| | Feature selection | Automation | Learning-based | [245, 258] |
| Reduction | Feature selection | Collaboration | Partial | [208, 287] |
| | Dimensionality reduction | Automation | Learning-based | [2, 13, 255] |
| | Instance selection | Automation | Programmatic | [186, 193][148] |
| | Instance selection | Automation | Learning-based | [148, 225] |
| | Basic manipulation | Automation | Programmatic | [42, 93, 250, 282, 282, 288]. |
| | Basic manipulation | Automation | Learning-based | [56] |
| Augmentation | Augmentation data synthesis | Automation | Learning-based | [79, 102, 104, 216] |
| | Upsampling | Automation | Programmatic | [41, 95] |
| | Upsampling | Automation | Learning-based | [273] |
| - | Pipeline search | Automation | Pipeline | [68, 76, 97, 132, 154, 159, 280] |

Table 2. Papers for achieving different sub-goals of training data development.

privacy, and data security. Researchers and practitioners must be aware of these challenges in studying and executing data collection.

## 3.2 Data Labeling

Data labeling is the process of assigning one or more descriptive tags or labels to a dataset, enabling algorithms to learn from and make predictions on the labeled data. Traditionally, this is a timeconsuming and resource-intensive manual process, particularly for large datasets. Recently, more efficient labeling methods have been proposed to reduce human efforts. In what follows, we discuss the need for data labeling, efficient labeling strategies, and challenges.

3.2.1 Need for Data Labeling. Labeling plays a crucial role in ensuring that the model trained on the data accurately reflects human intentions. Without proper labeling, a model may not be able to make the desired predictions since the model can, at most, be as good as the data fed into it. Although unsupervised learning techniques are successful in domains such as large language models [\[34,](#page-29-1) [121,](#page-32-2) [187,](#page-34-3) [188\]](#page-34-4) and anomaly detection [\[176\]](#page-34-16), the trained models may not well align with human expectations. Thus, to achieve a better performance, we often still need to fine-tune the large language models with human labels, such as ChatGPT [\[174\]](#page-34-2), and tune anomaly detectors

with a small amount of labeled data [\[111,](#page-32-17) [142](#page-33-14)[-144\]](#page-33-15). Thus, labeling data is essential for teaching models to align with and behave like humans.

3.2.2 Efficient Labeling Strategies. Researchers have long recognized the importance of data labeling. Various strategies have been proposed to enhance labeling efficiency. We will discuss crowdsourced labeling, semi-supervised labeling, active learning, data programming, and distant supervision. Note that it is possible to combine them as hybrid strategies.

Crowdsourced labeling. Crowdsourcing is a classic approach that breaks down a labeling task into smaller and more manageable parts so that they can be outsourced and distributed to a large number of non-expert annotators. Traditional methods often only provide initial guidelines to annotators [\[265\]](#page-36-14). However, the guidelines can be unclear and ambiguous, so each annotator could judge the same situation subjectively and differently. One way to mitigate this inconsistency is to start with small pilot studies and iteratively refine the design of the labeling task [\[130\]](#page-32-9). Another is to ask multiple workers to annotate the same sample and infer a consensus label [\[227\]](#page-35-8). Other studies focus on algorithmically improving label quality, e.g., pruning low-quality teachers [\[58\]](#page-30-8). All these crowdsourcing methods require full human participation but assist humans or enhance label quality in different ways.

Semi-supervised labeling. The key idea is to leverage a small amount of labeled data to infer the labels of the unlabeled data. A popular approach is self-training [\[298\]](#page-38-1), which trains a classifier based on labeled data and uses it to generate pseudo labels. To improve the quality of pseudo labels, a common strategy is to train multiple classifiers and find a consensus label, such as using different machine learning algorithms to train models on the same data [\[295\]](#page-37-8). In parallel, researchers have studied graph-based semi-supervised labeling techniques [\[46\]](#page-29-6). The idea is to construct a graph, where each node is a sample, and each edge represents the distance between the two nodes it connects. Then they infer labels through label propagation in the graph. Recently, a reinforcement learning from human feedback procedure is proposed [\[48\]](#page-30-4) and used in ChatGPT [\[174\]](#page-34-2). They train a reward model based on human-labeled data and infer the reward for unlabeled data to fine-tune the language model. These semi-supervised labeling methods only require partial human participation to provide the initial labels.

Active learning. Active learning is an iterative labeling procedure that involves humans in the loop. In each iteration, the algorithm selects an unlabeled sample or batch of samples as a query for human annotation. The newly labeled samples help the algorithm choose the next query. The existing work mainly differs in query selection strategies. Early methods use statistical methods to estimate sample uncertainty and select the unlabeled sample the model is most uncertain about [\[55\]](#page-30-9). Recent studies have investigated deep active learning, which leverages model output or designs specialized architectures to measure uncertainty [\[192\]](#page-34-11). More recent research aligns the querying process with a Markov decision process and learns to select the long-term best query with contextual bandit [\[66\]](#page-30-10) or reinforcement learning [\[274\]](#page-37-9). Unlike semi-supervised labeling, which requires one-time human participation in the initial stage, active learning needs a continuous supply of information from humans to adaptively select queries.

Data programming. Data programming [\[190,](#page-34-6) [191\]](#page-34-8) is a weakly-supervised approach that infers labels based on human-designed labeling functions. The labeling functions are often some heuristic rules and vary for different data types, e.g., seed words for text classification [\[278\]](#page-37-10), masks for image segmentation [\[103\]](#page-31-9), etc. However, sometimes the labeling functions may not align with human intentions. To address this limitation, researchers have proposed interactive data programming [\[27,](#page-29-7) [80\]](#page-31-8), where humans participate more by interactively providing feedback to refine labeling functions. Data programming methods often require minimum human participation or, at most, partial

participation. Thus, the methods in this research line are often more desirable when we need to quickly generate a large number of labels.

Distant supervision. Another weakly-supervised approach is distant supervision, which assigns labels by leveraging external sources. A famous application of distant supervision is on relation extraction [\[160\]](#page-33-8), where the semantic relationships between entities in the text are labeled based on external data, such as Freebase [\[30\]](#page-29-11). Distant supervision is often an automated approach that does not require human participation. However, the automatically generated labels can be noisy if there is a discrepancy between the dataset and the external source.

3.2.3 Challenges. The main challenge for data labeling stems from striking a balance between label quality, label quantity, and financial cost. If given adequate financial support, it is possible to hire a sufficient number of expert annotators to obtain a satisfactory quantity of high-quality labels. However, when we have a relatively tight budget, we often have to resort to more efficient labeling strategies. Identifying the proper labeling strategy often requires domain knowledge to balance different tradeoffs, particularly human labor and label quality/quantity. Another difficulty lies in the subjectivity of labeling. While the instructions may be clear to the designer, they may be misinterpreted by annotators, which leads to labeling noise. Last but not least, ethical considerations, such as data privacy and bias, remain a pressing issue, especially when the labeling task is distributed to a large and undefined group of people.

### 3.3 Data Preparation

Data preparation involves cleaning and transforming raw data into a format that is appropriate for model training. Conventionally, this process often necessitates a considerable amount of engineering work with laborious trial and error. To automate this process, state-of-the-art approaches often adopt search algorithms to discover the most effective strategies. In this subsection, we introduce the need, representative methods, and challenges for data preparation.

3.3.1 Need for Data Preparation. Raw data is often not ready for model training due to potential issues such as noise, inconsistencies, and unnecessary information, leading to inaccurate and biased results. For instance, the model could overfit on noises, outliers, and irrelevant extracted features, resulting in reduced generalizability [\[260\]](#page-36-15). If sensitive information (e.g., race and gender) is not removed, the model may unintentionally learn to make biased predictions [\[240\]](#page-36-16). In addition, the raw feature values may negatively affect model performance if they are in different scales or follow skewed distributions [\[4\]](#page-28-11). Thus, it is imperative to clean and transform data. The need can also be verified by a Forbes survey [\[185\]](#page-34-17), which suggests that data preparation accounts for roughly 80% of the work of data scientists.

3.3.2 Methods. We will review and discuss the techniques for achieving three key data preparation objectives, namely data cleaning, feature extraction, and feature transformation.

Data cleaning. Data cleaning is the process of identifying and correcting errors, inconsistencies, and inaccuracies in datasets. Traditional methods repair data with programmatic automation, e.g., imputing missing values with mean or median [\[289\]](#page-37-5) and scanning all data to find duplicates. However, such heuristics can be inaccurate or inefficient. Thus, learning-based methods have been developed, such as training a regression model to predict missing values [\[135\]](#page-32-16), efficiently estimating the duplicates with sampling [\[98\]](#page-31-10), and correcting labeling errors [\[116\]](#page-32-14). Contemporary data cleaning methods often do not solely focus on the cleaning itself, but rather on learning to improve final model performance. For instance, a recent study has adopted search algorithms to automatically identify the best cleaning strategy to optimize validation performance [\[126\]](#page-32-15). Beyond automation, researchers have studied collaboration-oriented cleaning methods. For example, a

hybrid human-machine workflow is proposed to identify duplicates by presenting similar pairs to humans for annotation [\[244\]](#page-36-9).

Feature extraction. Feature extraction is an important step in extracting relevant features from raw data. For training traditional machine learning models, we often need to extract features based on domain knowledge of the data type being targeted. Common features used for images include color features, texture features, intensity features, etc. [\[199\]](#page-34-12). For time series data, temporal, statistical, and spectral features are often considered [\[14\]](#page-28-8). Deep learning, in contrast, automatically extracts features by learning the weights of neural networks, which requires less domain knowledge. For instance, convolutional neural networks can be used in both images [\[127\]](#page-32-0) and time series [\[248\]](#page-36-10). The boundary between data and model becomes blurred with deep learning feature extractors, which operate on the data while also being an integral part of the model. Although deep extractors could learn high-quality feature representations, the extraction process is uninterpretable and may amplify the bias in the learned representation [\[240\]](#page-36-16). Therefore, traditional feature extraction methods are often preferred in high-stakes domains for interpretability and removing sensitive information.

Feature transformation. Feature transformation refers to the process of converting the original features into a new set of features, which can often lead to improved model performance. Some typical transformations include normalization, which scales the feature into a bounding range, and standardization, which transforms features so that they have a mean of zero and a standard deviation of one [\[5\]](#page-28-4). Other strategies include log transformation and polynomial transformation to smooth the long-tail distribution and create new features through multiplication [\[24\]](#page-29-8). These transformation methods can be combined in different ways to improve model performance. For example, a representative work builds a transformation graph for a given dataset, where each node is a type of transformation, and adopts reinforcement learning to search for the best transformation strategy [\[122\]](#page-32-11). Learning-based methods often yield superior performance by optimizing transformation strategies based on the feedback obtained from the model.

3.3.3 Challenges. Properly cleaning and transforming data is challenging due to the unique characteristics of different datasets. For example, the errors and inconsistencies in text data are quite different from those in time-series data. Even if two datasets have the same data type, their feature values and potential issues can be very diverse. Thus, researchers and data scientists often need to devote a significant amount of time and effort to clean the data. Although learning-based methods can search for the optimal preparation strategy automatically [\[122,](#page-32-11) [126\]](#page-32-15), it remains a challenge to design the appropriate search space, and the search often requires a non-trivial amount of time.

### 3.4 Data Reduction

The goal of data reduction is to reduce the complexity of a given dataset while retaining its essential information. This is often achieved by either reducing the feature size or the sample size. Our discussion will focus on the need for data reduction, representative methods for feature and sample size reduction, and challenges.

3.4.1 Need for Data Reduction. With more data being collected at an unprecedented pace, data reduction plays a critical role in boosting training efficiency. From the sample size perspective, reducing the number of samples leads to a simpler yet representative dataset, which can alleviate memory and computation constraints. It also helps to alleviate data imbalance issues by downsampling the samples from the majority class [\[186\]](#page-34-15). Similarly, reducing feature size brings many benefits. For example, eliminating irrelevant or redundant features mitigates the risk of overfitting [\[138\]](#page-32-4). Smaller feature sizes will also enable faster training and inference in model deployment [\[242\]](#page-36-17). In addition, only keeping a subset of features will make the model more interpretable [\[51,](#page-30-12) [52,](#page-30-13) [243\]](#page-36-18). Data reduction techniques can enable the model to focus only on the essential information, thereby enhancing accuracy, efficiency, and interpretability.

## 3.4.2 Methods for Reducing Feature Size. From the feature perspective, we discuss two common reduction strategies.

Feature selection. Feature selection is the process of selecting a subset of features most relevant to the intended tasks [\[138\]](#page-32-4). It can be broadly classified into filter, wrapper, and embedded methods. Filter methods [\[229\]](#page-35-9) evaluate and select features independently using a scoring function based on statistical properties such as information gain [\[10\]](#page-28-9). Although filter methods are very efficient, they ignore feature dependencies and interactions with the model. Wrapper methods alleviate these issues by leveraging the model performance to assess the quality of selected features and refining the selection iteratively [\[258\]](#page-36-12). While these methods often achieve better performances, they are computationally more expensive. Embedded methods, from another angle, integrate feature selection into the model training process [\[245\]](#page-36-11) so that the selection process is optimized in an endto-end manner. Beyond automation, active feature selection takes into account human knowledge and incrementally selects the most appropriate features [\[208,](#page-35-10) [287\]](#page-37-11). Feature selection reduces the complexity, producing cleaner and more understandable data while retaining feature semantics.

Dimensionality reduction. Dimensionality reduction aims to transform high-dimensional features into a lower-dimensional space while preserving the most representative information. The existing methods can be mainly categorized into linear and non-linear techniques. The former generates new features via linear combinations of features from the original data. One of the most popular algorithms is Principal Component Analysis (PCA) [\[2\]](#page-28-5), which performs orthogonal linear combinations of the original features based on the variance in an unsupervised manner. Another representative method targeted for supervised scenarios is Linear Discriminant Analysis (LDA) [\[255\]](#page-36-13), which statistically learns linear feature combinations that can separate classes well. Linear techniques, however, may not always perform well, especially when features have complex and non-linear relationships. Non-linear techniques address this issue by utilizing nonlinear mapping functions. A popular technique is autoencoders [\[13\]](#page-28-10), which use neural networks to encode the original features into a low-dimensional space and reconstruct the features using a neural decoder.

3.4.3 Methods for Reducing Sample Size. The reduction of samples is typically achieved with instance selection, which selects a representative subset of data samples that retain the original properties of the dataset. The existing studies can be divided into wrapper and filter methods. The former selects instances based on scoring functions. For example, a common strategy is to select border instances since they can often shape the decision boundary [\[193\]](#page-34-13). Wrapper methods, in contrast, select instances based on model performance [\[225\]](#page-35-11), which considers the interaction effect with the model. Instance selection techniques can also alleviate data imbalance issues by undersampling the majority class, e.g., with random undersampling [\[186\]](#page-34-15). More recent work adopts reinforcement learning to learn the best undersampling strategies [\[148\]](#page-33-11). Overall, instance selection is a simple yet effective way to reduce data sizes or balance data distributions.

3.4.4 Challenges. The challenges of data reduction are two-folded. On the one hand, selecting the most representative data or projecting data in a low-dimensional space with minimal information loss is non-trivial. While learning-based methods can partially address these challenges, they may necessitate substantial computational resources, especially when dealing with extremely large datasets, e.g., the wrapper and reinforcement learning methods [\[148,](#page-33-11) [225,](#page-35-11) [258\]](#page-36-12). Therefore, achieving both high accuracy and efficiency is challenging. On the other hand, data reduction can potentially amply data bias, raising fairness concerns. For example, the selected features could

be over associating with protected attributes [\[256\]](#page-36-19). Fairness-aware data reduction is a critical yet under-explored research direction.

### 3.5 Data Augmentation

Data augmentation is a technique to increase the size and diversity of data by artificially creating variations of the existing data, which can often improve the model performance. It is worth noting that even though data augmentation and data reduction seem to have contradictory objectives, they can be used in conjunction with each other. While data reduction focuses on eliminating redundant information, data augmentation aims to enhance data diversity. We will delve into the need for data augmentation, various representative methods, and the associated challenges.

3.5.1 Need for Data Augmentation. Modern machine learning algorithms, particularly deep learning, often require large amounts of data to learn effectively. However, collecting large datasets, especially annotated data, is labor-intensive. By generating similar data points with variance, data augmentation helps to expose the model to more training examples, hereby improving accuracy, generalization capabilities, and robustness. Data augmentation is particularly important in applications where there is limited data available. For example, it is often expensive and time-consuming to acquire well-annotated medical data [\[45\]](#page-29-12). Data augmentation can also alleviate class imbalance issues, where there is a disproportionate ratio of training samples in each class, by augmenting the data from the under-represented class.

3.5.2 Common Augmentation Methods. In general, data augmentation methods often manipulate the existing data to generate variances or synthesize new data. We discuss some representative methods in each category below.

Basic manipulation. This research line involves making minor modifications to the original data samples to produce augmented samples directly. Various strategies have been proposed in the computer vision domain, such as scaling, rotation, flipping, and blurring [\[288\]](#page-37-12). One notable approach is Mixup [\[282\]](#page-37-6), which interpolates the existing data samples to create new samples. It is shown that Mixup serves as a regularizer, encouraging the model to prioritize simpler linear patterns, which in turn enhances the generation performance [\[282\]](#page-37-6). More recent studies use learning-based algorithms to automatically search for augmentation strategies. A representative work is AutoAugment, which uses reinforcement learning to iteratively improve the augmentation policies [\[56\]](#page-30-2). Beyond image data, basic manipulation often needs to be tailored for the other data types, such as permutation and jittering in time-series data [\[250\]](#page-36-8), mixing data in the hidden space for text data to retain semantic meanings [\[42\]](#page-29-9), and mixing graphon for graph data [\[93\]](#page-31-11).

Augmentation data synthesis. Another category focuses on synthesizing new training samples by learning the distribution of the existing data, which is typically achieved by generative modeling. GAN [\[86,](#page-31-3) [283\]](#page-37-3) has been widely used for data augmentation [\[79\]](#page-31-5). The key idea is to train a discriminator in conjunction with a generator, making the latter generate synthetic data that closely resembles the existing data. GAN-based data augmentation has also been used to augment other data types, such as time-series data [\[140\]](#page-32-18) and text data [\[216\]](#page-35-12). Other studies have used Variational Autoencoder [\[104\]](#page-31-13) and diffusion models [\[102\]](#page-31-12) to achieve augmentation. Compared to basic manipulation that augments data locally, data synthesis learns data patterns from the global view and generates new samples with a learned model.

3.5.3 Methods Tailored for Class Imbalance. Class imbalance is a fundamental challenge in machine learning, where the number of majority samples is much larger than that of minority samples. Data augmentation can be used to perform upsampling on the minority class to balance the data distribution. One popular approach is SMOTE [\[41\]](#page-29-10), which involves generating synthetic samples

![](_page_15_Figure_1.jpeg)
<!-- Image Description: The image presents a flowchart illustrating a model evaluation framework. It shows "in-distribution" evaluation using data slicing and algorithmic recourse, and "out-of-distribution" evaluation using adversarial samples and distribution shift analysis. All evaluations feed into a central "Model" which is refined via "Prompt engineering" to understand the decision boundary and improve robustness and sensitivity. Simple icons represent data analysis techniques. -->

Figure 5. An overview of inference data development.

by linearly interpolating between minority instances and their neighbors. ADASYN [\[95\]](#page-31-14) is an extension of SMOTE that generates additional synthetic samples for data points that are more difficult to learn, as determined by the ratio of majority class samples in their nearest neighbors. A recent study proposes AutoSMOTE, a learning-based algorithm that searches for best oversampling strategies with reinforcement learning [\[273\]](#page-37-7).

3.5.4 Challenges. One critical challenge in data augmentation is that there is no single augmentation strategy that is suitable for all scenarios. Different data types may require diverse strategies. For example, compared to image data, graph data is irregular and not well-aligned, and thus the vanilla Mixup strategy can not be directly applied [\[93\]](#page-31-11). Even though two datasets have the same data type, the optimal strategy differs. For instance, we often need to upsample the minority samples differently to achieve the best results [\[273\]](#page-37-7). Although search-based algorithms can identify the best strategies with trial and error, it also increases the computation and storage costs, which can be a limiting factor in some applications. More effective and efficient data augmentation techniques are required to overcome these challenges.

### 3.6 Pipeline Search

In real-world applications, we often encounter complex data pipelines, where each pipeline step corresponds to a task associated with one of the aforementioned sub-goals. Despite the progress made in each individual task, a pipeline typically functions as a whole, and the various pipeline steps may have an interactive effect. For instance, the best data augmentation strategy may depend on the selected features. Pipeline search is a recent trend that tries to automatically search for the best combinations. This subsection introduces some representative pipeline search algorithms.

One of the first pipeline search frameworks is AutoSklearn [\[76\]](#page-30-11). It performs a combined search of preprocessing modules, models, and the associated hyperparameters to optimize the validation performance. However, they use a very small search space for preprocessing modules. DARPA's Data-Driven Discovery of Models (D3M) program pushes the progress further by building an infrastructure for pipeline search [\[159\]](#page-33-13). Although D3M originally focused on automated model discovery, it has developed numerous data-centric modules for processing data. Building upon D3M, AlphaD3M uses Monte-Carlo Tree Search to identify the best pipeline [\[68\]](#page-30-3). D3M is then tailored for time-series anomaly detection [\[132\]](#page-32-6) and video analysis [\[280\]](#page-37-13). Deepline enables the search within a large number of data-centric modules using multi-step reinforcement learning [\[97\]](#page-31-15). ClusterP3S allows for personalized pipelines to be created for various features, utilizing clustering techniques to enhance search efficiency [\[154\]](#page-33-12).

Despite these progresses, pipeline search still faces a significant challenge due to the high computational overhead since the search algorithm often needs to try different module combinations repeatedly. This overhead becomes more pronounced as the number of modules increases, leading to an exponential growth of the search space. Thus, more efficient search strategies [\[97,](#page-31-15) [154\]](#page-33-12) are required to enable a broader application of pipeline search in real-world scenarios.

### 4 INFERENCE DATA DEVELOPMENT

Another crucial component in building AI systems is to design inference data to evaluate a trained model or unlock a specific capability of the model. In the conventional model-centric paradigm, we often adopt a hold-out evaluation set that is not included in the training data to measure model performance using specific metrics such as accuracy. However, relying solely on performance metrics may not fully capture many important properties of a model, such as its robustness, generalizability, and rationale in decision-making. Moreover, as models become increasingly large, it becomes possible to obtain the desired predictions by solely engineering the data input. This section introduces some representative methods that evaluate models from a more granular view, or engineering data inputs for inference, shown in Figure [5.](#page-15-1) Our discussion involves in-distribution set evaluation (Section [4.1\)](#page-16-1), out-of-distribution evaluation (Section [4.2\)](#page-17-0), and prompt engineering (Section [4.3\)](#page-19-1). We summarize the relevant tasks and methods in Table [3.](#page-17-1)

### 4.1 In-distribution Evaluation

In-distribution evaluation data construction aims to generate samples that conform to training data. We will begin by addressing the need for constructing in-distribution evaluation sets. Next, we will review representative methods for two scenarios: evaluating important sub-populations on which the model underperforms through data slicing, and assessing decision boundaries through algorithmic recourse. Lastly, we will discuss the challenges.

4.1.1 Need for In-distribution Evaluation. In-distribution evaluation is the most direct way to assess the quality of trained models, as it reflects their capabilities within the training distribution. The need for a more fine-grained in-distribution evaluation is two-fold. Firstly, models that perform well on average may fail to perform adequately on specific sub-populations, requiring identification and calibration of underrepresented groups to avoid biases and errors, particularly in high-stakes applications [\[158,](#page-33-16) [173\]](#page-34-18). Secondly, it is crucial to understand the decision boundary and inspect the model ethics before deployment, especially in risky applications like policy making [\[218\]](#page-35-13).

4.1.2 Data Slicing. Data slicing involves partitioning a dataset into relevant sub-populations and evaluating a model's performance on each sub-population separately. A common approach to data slicing is to use pre-defined criteria, such as age, gender, or race [\[16\]](#page-28-12). However, data in many real-world applications can be complex, and properly designing the partitioning criteria heavily relies on domain knowledge, such as slicing 3-D seismic data in geophysics [\[267\]](#page-37-14) and program slicing [\[202\]](#page-34-19).

To reduce human effort, automated slicing methods have been developed to discover important data slices by sifting through all potential slices in the data space. One representative work is SliceFinder [\[53\]](#page-30-5), which identifies slices that are both interpretable (i.e., slicing based on a small set of features) and problematic (the model performs poorly on the slice). To solve this search problem, SliceFinder offers two distinct methods, namely the tree-based search and the lattice-based search. The former is more efficient, while the latter has better efficacy. SliceLine [\[198\]](#page-34-20) is another notable work that addresses the scalability limitations of slice finding by focusing on both algorithmic and system perspectives. This approach is motivated by frequent itemset mining and leverages relevant monotonicity properties and upper bounds for effective pruning. Moreover, to address hidden stratification, which occurs when each labeled class contains multiple semantically distinct subclasses, GEORGE [\[217\]](#page-35-14) employs clustering algorithms to slide data across different subclasses. Another tool for automated slicing is Multiaccuracy [\[123\]](#page-32-19), where a simple "auditor" is trained to predict the residual of the full model using input features. Multiaccuracy, in general, is an efficient approach since it only requires a small amount of audit data. Data slicing allows researchers and

| Sub-goal | Task | | Method type Automation level/<br>participation degree References | |
|--------------|-----------------------|---------------|------------------------------------------------------------------|----------------------------------------------------|
| | Data slicing | Collaboration | Minimum | [16] |
| In | Data slicing | Collaboration | Partial | [202, 267] |
| distribution | Data slicing | Automation | Learning-based | [53, 123, 198, 217] |
| | Algorithmic recourse | Collaboration | Minimum | [20, 26, 38, 57, 62, 118, 136, 149, 184, 212, 237] |
| | Adversarial samples | Collaboration | Minimum | [99] |
| | Adversarial samples | Automation | Learning-based | [23, 43, 71, 151, 165, 177, 210] |
| Out-of | Distribution shift | Collaboration | Full | [63, 125, 197] |
| distribution | Distribution shift | Collaboration | Partial | [90, 211] |
| | Distribution shift | Automation | Programmatic | [11, 87, 145, 223] |
| | Distribution shift | Automation | Learning-based | [73, 91] |
| Prompt | Manual engineering | Collaboration | Partial | [205-207] |
| engineering | Automated engineering | Automation | Programmatic | [94, 115, 264] |
| | Automated engineering | Automation | Learning-based | [82, 239] |

Table 3. Papers for achieving different sub-goals of inference data development.

practitioners to identify biases and errors in a model's predictions and calibrate the model to improve its overall capabilities.

4.1.3 Algorithmic Recourse. Algorithmic recourse (also known as "counterfactuals" [\[237\]](#page-36-20) in the explainable AI domain) aims to generate a hypothetical set of samples that can flip model decisions toward preferred outcomes. For example, if an individual is denied a loan, algorithmic recourse seeks the closest sample (e.g., with a higher account balance) that would have been approved. Hypothetical samples derived through algorithmic recourse are valuable in understanding decision boundaries. For the previously mentioned example, the hypothetical sample addresses the question of how the individual could have been approved and also aids in the detection of potential biases across individuals.

The existing methods primarily vary in their strategies for identifying hypothetical samples, and can generally be classified into white-box and black-box methods. White-box methods necessitate access to the evaluated models, which can be achieved through complete internals [\[38,](#page-29-15) [118,](#page-32-20) [149\]](#page-33-17), gradients [\[237\]](#page-36-20), or solely the prediction function [\[57,](#page-30-14) [62,](#page-30-15) [136,](#page-32-21) [212\]](#page-35-15). Conversely, black-box methods do not require access to the model at all. For example, Dijkstra's algorithm is employed to obtain the shortest path between existing training data points to find recourse under certain distributions [\[184\]](#page-34-21). An alternative approach involves dividing the feature space into pure regions, where all data points belong to a single class, and utilizing graph traversing techniques [\[20,](#page-29-13) [26\]](#page-29-14) to identify the nearest recourse. Given that the target label for reasoning is usually inputted by humans, these recourse methods all require minimal human participation.

4.1.4 Challenges. The main challenge of constructing in-distribution evaluation sets lies in identifying the targeted samples effectively and efficiently. In the case of data slicing, determining the optimal subset of data is particularly challenging due to the exponential increase in the number of possible subsets with additional data points. Similarly, identifying the closest recourse when limited information is available also requires significant effort.

## 4.2 Out-of-distribution Evaluation

Out-of-distribution evaluation data refers to a set of samples that follow a distribution that differs from the one observed in the training data. We begin by discussing the need for out-of-distribution evaluation, followed by a review of two representative tasks: generating adversarial samples and generating samples with distribution shifts. Then we delve into the challenges associated with out-of-distribution data generation.

4.2.1 Need for Out-of-distribution Evaluation. Although modern machine learning techniques generally perform well on in-distribution datasets, the distribution of data in the deployment environment may not align with the training data [\[214\]](#page-35-21). Out-of-distribution evaluation primarily assesses a model's ability to generalize to unexpected scenarios by utilizing data samples that differ significantly from the ones used during training. This evaluation can uncover the transferability of a model and instill confidence in its performance in unexpected scenarios. Out-of-distribution evaluation can also provide essential insights into a model's robustness, exposing potential flaws that must be addressed before deployment. This is crucial in determining whether the model is secure in real-world deployments.

4.2.2 Generating Adversarial Samples. Adversarial samples are the ones with intentionally manipulated or modified input data in a way that causes a model to make incorrect predictions. Adversarial samples can aid in comprehending a model's robustness and are typically generated by applying perturbations to the input data. Manual perturbation involves adding synthetic and controllable perturbations, such as noise and blur, to the original data [\[99\]](#page-31-16).

Automated methods design learning-based strategies to generate perturbations automatically and are commonly classified into four categories: white-box attacks, physical world attacks, blackbox attacks, and poisoning attacks. White-box attacks involve the attacker being provided with the model and victim sample. Examples of white-box attacks include Biggio's attack [\[23\]](#page-29-16), Deep-Fool [\[165\]](#page-33-9), and projected gradient descent attack [\[151\]](#page-33-18). Physical world attacks involve introducing real perturbations to real-world objects. For instance, in the work by [\[71\]](#page-30-16), stickers were attached to road signs to significantly impact the sign identifiers of autonomous cars. Black-box attacks are often applied when an attacker lacks access to a classifier's parameters or training set but possesses information regarding the data domain and model architecture. In [\[177\]](#page-34-22), the authors exploit the transferability property to generate adversarial examples. A zero-th order optimizationbased black-box attack is proposed in [\[43\]](#page-29-17) that leverages the prediction confidence for the victim sample. Poisoning attacks involve the creation of adversarial examples prior to training, utilizing knowledge about model architectures. For instance, the poison frogs technique [\[210\]](#page-35-16) inserts an adversarial image into the training set with a true label. By evaluating a trained model on various adversarial samples, we can gain a better understanding of the potential weaknesses of the model in deployment. This can help us take steps to prevent undesirable outcomes.

4.2.3 Generating Samples with Distribution Shift. Generating samples with distribution shifts enables the evaluation of a model on a different distribution. One straightforward way is to collect data with varying patterns, such as shifts across different times or locations [\[63\]](#page-30-17), camera traps for wildlife monitoring [\[125\]](#page-32-10), and diverse domains [\[197\]](#page-34-23). A more efficient approach would involve constructing the evaluation set from pre-collected data. To illustrate, some studies [\[90,](#page-31-17) [211\]](#page-35-17) generate various sets of contiguous video frames that appear visually similar to humans but lead to inconsistent predictions due to the small perturbations.

Apart from natural distribution shifts in real-world data, synthetic distribution shifts are widely adopted, including three types: 1) covariate shift, which assumes that the input distribution is shifted [\[87,](#page-31-18) [223\]](#page-35-18), 2) label shift, which assumes that the label distribution is shifted [\[11,](#page-28-13) [145\]](#page-33-19), and 3) general distribution shift, which assumes that both the input and label distributions are shifted [\[73,](#page-30-18) [91\]](#page-31-19). Biased data sampling can be used to synthesize covariate shifts or label shifts, whereas learningbased methods are typically required to synthesize general distribution shifts [\[73,](#page-30-18) [91\]](#page-31-19). Generating

samples with distribution shift is essential in evaluating a model's transferability, especially when there is a distribution gap between the training and deployment environments.

4.2.4 Challenges. The challenges for out-of-distribution generation set construction are two-fold. Firstly, generating high-quality out-of-distribution data is challenging. If the training data is not representative, it may be difficult to generate appropriate data. Furthermore, the generation models may encounter mode collapse issues, meaning that they only generate a limited number of similar samples and disregard the diversity of the target distribution. Secondly, evaluating the quality of out-of-distribution generation is difficult since no single metric can capture the diversity and quality of the generated samples. Commonly used metrics, such as likelihood or accuracy, may not be suitable as they may exhibit bias toward generating samples similar to the training data. Therefore, various evaluation metrics have been proposed to assess the distance between in-distribution and out-of-distribution samples [\[21,](#page-29-18) [32,](#page-29-19) [114,](#page-32-23) [171,](#page-34-24) [201\]](#page-34-25). Overall, creating high-quality out-of-distribution data is a complex and demanding task that requires meticulous design.

## 4.3 Prompt Engineering

With the advent of large language models, it becomes feasible to accomplish a task by solely fine-tuning the input to probe knowledge from the model, while keeping the model fixed. Prompt engineering is an emerging task that aims to design and construct high-quality prompts to achieve the most effective performance on downstream tasks [\[146\]](#page-33-2). For example, when performing text summarization, we can provide the texts we want to summarize followed by specific instructions such as "summarize it" or "TL;DR" to guide the inference. Prompt engineering revolutionizes the traditional workflow by fine-tuning the input data rather than the model itself to achieve a given task.

A natural way is to perform manual prompt engineering by creating templates. For example, in [\[205](#page-35-19)[-207\]](#page-35-20), the authors have pre-defined templates for few-shot learning in text classification and conditional text generation tasks. However, manually crafting templates may not be sufficient to discover the optimal prompts for complex tasks. Thus, automated prompt engineering has been studied. Common programmatic approaches include mining the templates from an external corpus [\[115\]](#page-32-22) and paraphrasing with a seed prompt [\[94,](#page-31-20) [264\]](#page-36-21). Learning-based methods automatically generate the prompt tokens by gradient-based search [\[239\]](#page-36-6) or generative models [\[82\]](#page-31-21). The primary obstacle in prompt engineering arises from the absence of a universal prompt template that consistently performs well. Various templates may result in different model behaviors, and obtaining the desired answers is not guaranteed. Therefore, further research is necessary to gain insight into the response of the model to prompts and guide the prompt engineering process.

## 5 DATA MAINTENANCE

In production scenarios, data is not created once but is rather continuously updated, making data maintenance a significant challenge that must be considered to ensure reliable and instant data supply in building AI systems. This section provides an overview of the need, representative methods (as depicted in Figure [6\)](#page-20-0), and challenges of data maintenance. Our discussion spans across three aspects: data understanding (Section [5.1\)](#page-19-2), data quality assurance (Section [5.2\)](#page-22-0), and data storage & retrieval (Section [5.3\)](#page-23-0). Additionally, Table [4](#page-21-0) summarizes the relevant tasks and methods.

## 5.1 Data Understanding

To ensure proper maintenance, it is essential to first understand the data. The following discussion covers the need for data understanding techniques, ways to gain insights through visualization and valuation, and the challenges involved.

![](_page_20_Figure_1.jpeg)
<!-- Image Description: This diagram illustrates a data maintenance process. Three interconnected blocks represent "Data Understanding" (data visualization and valuation), "Data Quality Assurance" (quality assessment and improvement), and "Data Storage & Retrieval" (resource allocation and query acceleration). Arrows show how each component contributes to the central "Data Maintenance" process, which supplies high-quality data. Simple icons further clarify the functions of each block. -->

Figure 6. An overview of data maintenance.

5.1.1 Need for Data Understanding Techniques. Real-world data often comes in large volumes and complexity, which can make it difficult to understand and analyze. There are three main reasons why data understanding techniques are crucial. Firstly, comprehending a large number of raw data samples can be challenging for humans. To make it more manageable, we need to summarize the data and present it in a more concise and accessible way. Secondly, real-world data is often high-dimensional, while human perception is limited to two-or-three-dimensional space. Therefore, visualizing data in a lower-dimensional space is essential for understanding the data. Finally, it is crucial for organizations and stakeholders to understand the value of their data assets and the contribution of each data sample to the performance.

5.1.2 Data Visualization. Human beings are visual animals, and as such, we have a natural tendency to process and retain information presented in a pictorial and graphical format. Data visualization aims to leverage this innate human trait to help us better understand complex data. In what follows, we will discuss three relevant research topics: visual summarization, clustering for visualization, and visualization recommendation.

Visual summarization. Summarizing the raw data as a set of graphical diagrams can assist humans in gaining insights through a condensed interface. Despite its wide application, generating a faithful yet user-friendly summarization diagram is a non-trivial task. For example, it is hard to select the right visualization format. Radial charts (e.g., star glyphs and rose charts) and linear charts (e.g., line charts and bar charts) are two common formats for visualization. However, it is controversial which format is better. Although empirical evidence suggests that linear charts are superior to radial charts for many analytical tasks [\[37\]](#page-29-4), radial charts are often more natural and memorable [\[33\]](#page-29-20). In some cases, it is acceptable to compromise on the faithfulness of data representation in favor of enhanced memorability or space efficiency [\[37,](#page-29-4) [238\]](#page-36-22). For readers who are interested, [\[61\]](#page-30-19) and [\[78\]](#page-31-22) provide a comprehensive taxonomy of visualization formats. Although automated scripts can generate plots, the process of visual summarization often demands minimal human participation to select the most appropriate visualization formats.

Clustering for visualization. Real-world data can be high-dimensional and with complex manifold structures. As such, dimensionality reduction techniques (mentioned in Section [3.4\)](#page-12-0) are often applied to visualize data in a two-or-three-dimensional space. Furthermore, automated clustering methods [\[72\]](#page-30-6) are frequently combined with dimensionality reduction techniques to organize data points in a grouped, categorized, and often color-coded fashion, facilitating human comprehension and insightful analysis of the data.

Visualization recommendation. Building upon various visualization formats, there has been a surge of interest in visualization recommendation, which involves suggesting the most suitable visualization formats for a particular user. Programmatic automation approaches rank visualization candidates based on predefined rules composed of human perceptual metrics such as data type,

| Sub-goal | Task | Method type | Automation level/<br>participation degree | Reference |
|---------------------|------------------------------|---------------|-------------------------------------------|-----------------------|
| | Visual summarization | Collaboration | Minimum | [33, 37, 61, 78, 238] |
| | Clustering for visualization | Automation | Learning-based | [72] |
| Understanding | Visualization recommendation | Automation | Programmatic | [254] |
| | Visualization recommendation | Automation | Learning-based | [150] |
| | Visualization recommendation | Collaboration | Partial | [213, 219] |
| | Valuation | Automation | Learning-based | [3, 83, 84] |
| | Quality assessment | Collaboration | Minimum/partial | [18, 181, 195, 257] |
| | Quality improvement | Automation | Programmatic | [17, 29, 49] |
| Quality assurance | Quality improvement | Automation | Learning-based | [19] |
| | Quality improvement | Automation | Pipeline | [204, 230] |
| | Quality improvement | Collaboration | Partial | [44, 60, 81, 247] |
| | Resource allocation | Automation | Programmatic | [6, 152, 252] |
| | Resource allocation | Automation | Learning-based | [100, 233] |
| Storage & retrieval | Query index selection | Automation | Programmatic | [39, 224, 232] |
| | Query index selection | Automation | Learning-based | [179, 196] |
| | Query rewriting | Automation | Programmatic | [12, 40] |
| | Query rewriting | Automation | Learning-based | [96, 294] |

Table 4. Papers for achieving different sub-goals of data maintenance.

statistical information, and human visual preference [\[254\]](#page-36-7). Learning-based approaches exploit various machine learning techniques to rank the visualization candidates. An example of such a method is DeepEye [\[150\]](#page-33-20), which utilizes the statistical information of the data as input and optimizes the normalized discounted cumulative gain (NDCG) based on the quality of the match between the data and the chart. Collaborative visualization techniques allow for a more adaptable user experience by enabling users to continuously provide feedback and requirements for the visualization [\[213\]](#page-35-22). A recent study, Snowy [\[219\]](#page-35-23) accepts human language as input and generates recommendations for utterances during conversational visual analysis. As visualizations are intended for human users, allowing for human-in-the-loop feedback is crucial in developing visualization recommender systems.

5.1.3 Data Valuation. The objective of data valuation is to understand how each data point contributes to the final performance. Such information not only provides valuable insights to stakeholders but is also useful in buying or selling data points in the data market and credit attribution [\[83\]](#page-31-6). To accomplish this, researchers estimate the Shapley value of the data points, which assigns weights to each data point based on its contribution [\[3,](#page-28-14) [84\]](#page-31-23). A subsequent study has enhanced the robustness of this estimation across multiple datasets and models [\[83\]](#page-31-6). Since calculating the exact Shapley value can be computationally expensive, especially when dealing with a large number of data points, the above methods all adopt learning-based algorithms for efficient estimation.

5.1.4 Challenges. There are two major challenges. Firstly, the most effective data visualization formats and algorithms (e.g., clustering algorithms) are often specific to the domain and influenced by human behavior, making it difficult to select the best option. This selection process often requires human input. Determining how to best interact with humans adds an additional complexity. Secondly, developing efficient data valuation algorithms is challenging, since estimating the Shapley value can be computationally expensive, especially as data sizes continue to grow. Additionally, the Shapley value may only offer a limited perspective on data value, as there are many other important factors beyond model performance, such as the problems that can be addressed through training a model on the data.

## 5.2 Data Quality Assurance

To ensure a reliable data supply, it is essential to maintain data quality. We will discuss why quality assurance is necessary, the key tasks involved in maintaining data quality (quality assessment and improvement), and the challenges.

5.2.1 Need for Data Quality Assurance. In real-world scenarios, data and the corresponding infrastructure for data processing are subject to frequent and continuous updates. As a result, it is important not only to create high-quality training or inference data once but also to maintain their excellence in a dynamic environment. Ensuring data quality in such a dynamic environment involves two aspects. Firstly, continuous monitoring of data quality is necessary. Real-world data in practical applications can be complex, and it may contain various anomalous data points that do not align with our intended outcomes. As a result, it is crucial to establish quantitative measurements that can evaluate data quality. Secondly, if a model is affected by low-quality data, it is important to implement quality improvement strategies to enhance data quality, which will also lead to improved model performance.

5.2.2 Quality Assessment. Quality assessment develops evaluation metrics to measure the quality of data and detect potential flaws and risks. These metrics can be broadly categorized as either objective or subjective assessments [\[18,](#page-28-15) [181,](#page-34-26) [195,](#page-34-14) [257\]](#page-36-23). Although objective and subjective assessments may require different degrees of human participation, both of them are used in each paper we surveyed. Thus, we tag each paper with more than one degree of human participation in Table [4.](#page-21-0) We will discuss these two types of assessments in general and provide some representative examples of each.

Objective assessments directly measure data quality using inherent data attributes that are independent of specific applications. Examples of such metrics include accuracy, timeliness, consistency, and completeness. Accuracy refers to the correctness of obtained data, i.e., whether the obtained data values align with those stored in the database. Timeliness assesses whether the data is up-to-date. Consistency refers to the violation of semantic rules defined over a set of data items. Completeness measures the percentage of values that are not null. All of these metrics can be collected directly from the data, requiring only minimal human participation to specify the calculation formula.

Subjective assessments evaluate data quality from a human perspective, often specific to the application and requiring external analysis from experts. Metrics like trustworthiness, understandability, and accessibility are often assessed through user studies and questionnaires. Trustworthiness measures the accuracy of information provided by the data source. Understandability measures the ease with which users can comprehend collected data, while accessibility measures users' ability to access the data. Although subjective assessments may not directly benefit model training, they can facilitate easier collaboration within an organization and provide long-term benefits. Collecting these metrics typically requires full human participation since they are often based on questionnaires.

5.2.3 Quality Improvement. Quality improvement involves developing strategies to enhance the quality of data at various stages of a data pipeline. Initially, programmatic automation methods are used to enforce quality constraints, including integrity constraints [\[17\]](#page-28-16), denial constraints [\[49\]](#page-30-20), and conditional functional dependencies [\[29\]](#page-29-21) between columns. More recently, machine learning-based automation approaches have been developed to improve data quality. For instance, in [\[19\]](#page-28-6), a data validation module trains a machine learning model on a training set with expected data schema and generalizes it to identify potential problems in unseen scenarios. Furthermore, pipeline automation approaches have been developed to systematically curate data in multiple stages of the data pipeline, such as data integration and data cleaning [\[204,](#page-35-24) [230\]](#page-35-25).

Apart from automation, collaborative approaches have been developed to encourage expert participation in data improvement. For example, in autonomous driving [\[81\]](#page-31-24) and video content reviewing [\[60\]](#page-30-21), human annotations are continuously used to enhance the quality of training data with the assistance of machine learning models. Moreover, UniProt [\[247\]](#page-36-24), a public database for protein sequence and function literature, has created a systematic submission system to harness collective intelligence [\[44\]](#page-29-22) for data improvement. This system automatically verifies meta-information, updated versions, and research interests of the submitted literature. All of these methods necessitate partial human participation, as humans must continuously provide information through annotations or submissions.

5.2.4 Challenges. Ensuring data quality poses two main challenges. Firstly, selecting the most suitable assessment metric is not a straightforward task and heavily relies on domain knowledge. A single metric may not always be adequate in a constantly evolving environment. Secondly, quality improvement is a vital yet laborious process that necessitates careful consideration. Although automation is crucial in ensuring sustainable data quality, human involvement may also be necessary to ensure that the data quality meets human expectations. Therefore, data assessment metrics and data improvement strategies must be thoughtfully designed.

### 5.3 Data Storage & Retrieval

Data storage and retrieval systems play an indispensable role in providing the necessary data to build AI systems. To expedite the process of data acquisition, various efficient strategies have been proposed. In the following discussion, we elaborate on the importance of efficient data storage and retrieval, review some representative acceleration methods for resource allocation and query acceleration, and discuss the challenges associated with them.

5.3.1 Need for Efficient Data Storage & Retrieval. As the amount of data being generated continues to grow exponentially, having a robust and scalable data administration system that can efficiently handle the large data volume and velocity is becoming increasingly critical to support the training of AI models. This need encompasses two aspects. Firstly, data administration systems, such as Hadoop [\[77\]](#page-30-22) and Spark [\[266\]](#page-36-27), often need to store and merge data from various sources, requiring careful management of memory and computational resources. Secondly, it is crucial to design querying strategies that enable fast data acquisition to ensure timely and accurate processing of the data.

5.3.2 Resource Allocation. Resource allocation aims to estimate and balance the cost of operations within a data administration system. Two key efficiency metrics in data administration systems are throughput, which refers to how quickly new data can be collected, and latency, which measures how quickly the system can respond to a request. To optimize these metrics, various parametertuning techniques have been proposed, including controlling database configuration settings (e.g., buffer pool size) and runtime operations (e.g., percentage of CPU usage and multi-programming level) [\[69\]](#page-30-23). Early tuning methods rely on rules that are based on intuition, experience, data domain knowledge, and industry best practices from sources such as Apache [\[6\]](#page-28-17) and Cloudera [\[152\]](#page-33-21). For instance, Hadoop guidelines [\[252\]](#page-36-25) suggest that the number of reduced tasks should be set to approximately 0.95 or 1.75 times the number of reduced slots available in the cluster to ensure system tolerance for re-executing failed or slow tasks.

Various learning-based strategies have been developed for resource allocation in data processing systems. For instance, Starfish [\[100\]](#page-31-7) proposes a profile-predict-optimize approach that generates job profiles with dataflow and cost statistics, which are then used to predict virtual job profiles for task scheduling. More recently, machine learning approaches such as OtterTune [\[233\]](#page-36-26) have been developed to automatically select the most important parameters, map workloads, and recommend parameters to improve latency and throughput. These learning-based automation strategies can adaptively balance system resources without assuming any internal system information.

5.3.3 Query Acceleration. Another research direction is efficient data retrieval, which can be achieved through efficient index selection and query rewriting strategies.

Query index selection. The objective of index selection is to minimize the number of disk accesses needed during query processing. To achieve this, programmatic automation strategies create an indexing scheme with indexable columns and record query execution costs [\[224\]](#page-35-5). Then, they apply either a greedy algorithm [\[39\]](#page-29-23) or dynamic programming [\[232\]](#page-35-26) to select the indexing strategy. To enable a more adaptive and flexible querying strategy, learning-based automation strategies collect indexing data from human experts and train machine learning models to predict the proper indexing strategies [\[179\]](#page-34-27), or search for the optimal strategies using reinforcement learning [\[196\]](#page-34-28).

Query rewriting. In parallel, query rewriting aims to reduce the workload by identifying repeated sub-queries from input queries. Rule-based strategies [\[12,](#page-28-7) [40\]](#page-29-24) rewrite queries with pre-defined rules, such as DBridge [\[40\]](#page-29-24), which constructs a dependency graph to model the data flow and iteratively applies transformation rules. Learning-based approaches use supervised learning [\[96\]](#page-31-25) or reinforcement learning [\[294\]](#page-37-15) to predict rewriting rules given an input query.

5.3.4 Challenges. Existing data storage and retrieval methods typically focus on optimizing specific parts of the system, such as resource allocation and query acceleration we mentioned. However, the real data administration system as a whole can be complex since it needs to process a vast amount of data in various formats and structures, making end-to-end optimization a challenging task. Additionally, apart from efficiency, data storage and retrieval require consideration of several other crucial and challenging aspects, such as data access control and system maintenance.

### 6 DATA BENCHMARK

In the previous sections, we explored a diverse range of data-centric AI tasks throughout various stages of the data lifecycle. Examining benchmarks is a promising approach for gaining insight into the progress of research and development in these tasks, as benchmarks comprehensively evaluate various methods based on standard and agreed-upon metrics. It is important to note that, within the context of data-centric AI, we are specifically interested in data benchmarks rather than model benchmarks, which should assess various techniques aimed at achieving data excellence. In this section, we survey the existing benchmarks for different goals of data-centric AI. Firstly, we will introduce the benchmark collection strategy, and subsequently, we will summarize and analyze the collected benchmarks.

Collection strategy. We primarily utilize Google Scholar to search for benchmark papers. Specifically, we generate a series of queries for each task using relevant keywords for the sub-goal and task, and supplement them with terms such as "benchmark", "quantitative analysis", and "quantitative survey". For example, the queries for the task "data cleaning" include "benchmark data cleaning", "benchmark data cleansing", "quantitative analysis for data cleaning", "quantitative survey for data cleaning", etc. It is worth noting that many of the queried benchmarks evaluate models rather than data. Thus, we have carefully read each paper and manually filtered the papers to ensure that they focus on the evaluation of data. We have also screened them based on the number of citations and the reputation of the publication venues.

Summary of the collected benchmarks. Table [5](#page-25-0) comprises the 36 benchmarks that we collected using the above process, out of which 23 incorporate open-source codes. Notably, we did not

| Reference | Sub-goal | Task | Domain | Data modality | Open-source | | | |
|---------------------------|---------------------|---------------------------------------------------------|-----------------------------|------------------------------------|-------------|--|--|--|
| Training data development | | | | | | | | |
| Cohen et al. [54] | Collection | Dataset discovery | Biomedical | Tabular, text | ✗ | | | |
| Poess et al. [182] | Collection | Data integration | Database | Tabular, time-series | ✗ | | | |
| Pinkel et al. [180] | Collection | Data integration | Database | Tabular, graph | ✗ | | | |
| Wang et al. [246] | Labeling | Semi-supervised learning | AI | Image, text, audio | ✓ | | | |
| Yang et al. [259] | Labeling | Active learning | AI | Tabular, image, text | ✗ | | | |
| Meduri et al. [156] | Labeling | Active learning | Database | Tabular, text | ✗ | | | |
| Abdelaal et al. [1] | Preparation | Data cleaning | Database | Tabular, text, time-series | ✓ | | | |
| Li et al. [139] | Preparation | Data cleaning | Database | Tabular, time-series | ✓ | | | |
| Jäger et al. [106] | Preparation | Data cleaning | AI | Tabular, image | ✗ | | | |
| Buckley et al. [35] | Preparation | Feature extraction | Healthcare | Tabular, image, time-series | ✓ | | | |
| Vijayan et al. [235] | Preparation | Feature extraction | Biomedical | Tabular, sequential | ✓ | | | |
| Bommert et al. [31] | Reduction | Feature selection | Biomedical | Tabular, sequential | ✓ | | | |
| Espadoto et al. [70] | Reduction | Dimensionality reduction | Computer graphics | Tabular, image, audio | ✓ | | | |
| Grochowski et al. [89] | Reduction | Instance selection | Computer graphics | Tabular, image, audio | ✓ | | | |
| Blachnik et al. [25] | Reduction | Instance selection | Computer graphics | Tabular, image, audio | ✓ | | | |
| Iwana et al. [105] | Augmentation | All sub-goals | AI | Time-series | ✓ | | | |
| Nanni et al. [166] | Augmentation | Basic manipulation | AI | Image | ✓ | | | |
| Yoo et al. [261] | Augmentation | Basic manipulation | AI | Image | ✓ | | | |
| Ding et al. [64] | Augmentation | Augmentation data synthesis | AI | Graph | ✗ | | | |
| Tao et al. [228] | Augmentation | Augmentation data synthesis | Computer security | Tabular | ✗ | | | |
| Zoller et al. [297] | - | Pipeline search | AI | Tabular, image, audio, time-series | ✓ | | | |
| Gijsbers et al. [85] | - | Pipeline search | AI | Tabular, image, audio, time-series | ✓ | | | |
| | | | Evaluation data development | | | | | |
| Srivastava et al. [220] | In-distribution | Evaluation data synthesis | AI | Text | ✓ | | | |
| Pawelczyk et al. [178] | In-distribution | Algorithmic recourse | AI | Tabular | ✓ | | | |
| Dong et al. [67] | Out-of-distribution | Adversarial samples | AI | Image | ✓ | | | |
| Hendrycks et al. [99] | Out-of-distribution | Adversarial samples | AI | Image | ✓ | | | |
| Yoo et al. [262] | Out-of-distribution | Adversarial samples | AI | Text | ✓ | | | |
| | | | Data maintenance | | | | | |
| Kanthara et al. [119] | Understanding | Visual summarization | AI | Tabular, text | ✓ | | | |
| Grinstein et al. [88] | Understanding | Visual summarization | Human-computer interaction | Tabular, image | ✓ | | | |
| Zeng et al. [268] | Understanding | Visualization recommendation Human-computer Interaction | | Tabular | ✗ | | | |
| Jia et al. [110] | Understanding | Data valuation | AI | Image | ✓ | | | |
| Batini et al. [18] | Quality assurance | Quality assessment | Database | Tabular | ✗ | | | |
| Arocena et al. [8] | Quality assurance | Quality improvement | Database | Tabular | ✗ | | | |
| Zhang et al. [286] | Storage & retrieval | Resource allocation | Database | Tabular | ✓ | | | |
| Marcus et al. [153] | Storage & retrieval | Query index selection | Database | Tabular | ✗ | | | |
| | | | Unified benchmark | | | | | |
| Mazumder et al. [155] | Multiple | 6 distinct tasks | AI | Multiple | ✗ | | | |

Table 5. Data benchmarks. Note that they evaluate data rather than model.

encounter a benchmark for the task of "generating distribution shift samples", although there are benchmarks available for detecting distribution-shifted samples [\[125\]](#page-32-10). We omitted it from the table since it mainly assesses model performance on distribution shift rather than discussing how to create distribution-shifted data that can expose model weaknesses.

Meta-analysis. We give a bird-eye view of existing data-centric AI research across various dimensions by analyzing these collected benchmarks. ❶ Although the AI community has made the most significant contributions to these benchmarks (17), numerous other domains have also made substantial contributions, including databases (9), computer graphics (3), human-computer interaction (2), biomedical (3), computer security (1), and healthcare (1). Notably, healthcare and biomedical are outside the realm of computer science. An established benchmark in a domain often implies that there is a collection of published works. Therefore, data-centric AI is an interdisciplinary effort that spans various domains within and outside of computer science. ❷ The most frequently benchmarked data modality is tabular data (25), followed by image (15), time-series (7), text (6), audio (6), and graph (2). We conjecture that this is because tabular and image data have been extensively studied, while research on graph data is still emerging. ❸ Training data development has received more attention, if we measure it based on the number of benchmarks (22), compared to evaluation data development (5) and data maintenance (8). We hypothesize that this is due to the fact that many of the tasks involved in training data development were considered as preprocessing steps in the model-centric paradigm.

## 7 DISCUSSION AND FUTURE DIRECTION

What is the current stage of data-centric AI research, and what are the potential future directions? This section provides a top-level discussion of data-centric AI and presents some of the open problems that we have identified, aiming to motivate future exploration in this field. We start by trying to answer the research questions posed at the beginning:

- RQ1: What are the necessary tasks to make AI data-centric? Data-centric AI encompasses a range of tasks that involve developing training data, inference data, and maintaining data. These tasks include but are not limited to 1) cleaning, labeling, preparing, reducing, and augmenting the training data, 2) generating in-distribution and out-of-distribution data for evaluation, or tuning prompts to achieve desired outcomes, and 3) constructing efficient infrastructures for understanding, organizing, and debugging data.
- RQ2: Why is automation significant for developing and maintaining data? Given the availability of an increasing amount of data at an unprecedented rate, it is imperative to develop automated algorithms to streamline the process of data development and maintenance. Based on the papers surveyed in Tables [2,](#page-9-1) [3,](#page-17-1) and [4,](#page-21-0) automated algorithms have been developed for all sub-goals. These automation algorithms span different automation levels, from programmatic automation to learning-based automation, to pipeline automation.
- RQ3: In which cases and why is human participation essential in data-centric AI? Human participation is necessary for many data-centric AI tasks, such as the majority of data labeling tasks (Table [2\)](#page-9-1) and several tasks in inference data development (Table [3\)](#page-17-1). Notably, different methods may require varying degrees of human participation, ranging from full involvement to providing minimal inputs. Human participation is crucial in many scenarios because it is often the only way to ensure that the behavior of AI systems aligns with human intentions.
- RQ4: What is the current progress of data-centric AI? Although data-centric AI is a relatively new concept, considerable progress has already been made in many relevant tasks, the majority of which were viewed as preprocessing steps in the model-centric paradigm. Meanwhile, many new tasks have recently emerged, and research on them is still ongoing. In Section [6,](#page-24-0) our meta-analysis on benchmark papers reveals that progress has been made across different domains, with the majority of the benchmarks coming from the AI domain. Among the three general data-centric AI goals, training data development has received relatively more research attention. For data modality, tabular and image data have been the primary focus. As research papers on data-centric AI are growing exponentially [\[269\]](#page-37-2), we could witness even more progress in this field in the future.

By attempting to address these questions, our survey delves into a variety of tasks and their needs and challenges, yielding a more concrete picture of the scope and progress of data-centric AI. However, although we have endeavored to broadly and comprehensively cover various tasks and techniques, it is impossible to include every aspect of data-centric AI. In the following, we connect data-centric AI with two other popular research topics in AI:

- Foundation models. A foundation model is a large model that is trained on massive amounts of unlabeled data and can be adapted to various tasks, such as large language models [\[34,](#page-29-1) [172\]](#page-34-1), and Stable Diffusion [\[194\]](#page-34-10). As models become sufficiently powerful, it becomes feasible to perform many data-centric AI tasks with models, such as data labeling [\[172\]](#page-34-1), and data augmentation [\[263\]](#page-36-33). Consequently, the recent trend of foundation models has the potential to fundamentally alter our understanding of data. Unlike the conventional approach of storing raw data values in datasets, the model itself can be a form of data (or a "container" of raw data) since the model can convey information (see the definition of data in Section [2.1\)](#page-2-1). Foundation

models blur the boundary between data and model, but their training still heavily relies on large and high-quality datasets.

- Reinforcement learning. Reinforcement learning is a research field that trains intelligent agents to optimize rewards without any initial data [\[131,](#page-32-26) [164,](#page-33-25) [270-](#page-37-19)[272,](#page-37-20) [275,](#page-37-21) [276,](#page-37-22) [279,](#page-37-23) [281\]](#page-37-24). It is a unique learning paradigm that alternates between generating data with the model and training the model with self-generated data. Like foundation models, the advancement of reinforcement learning could also possibly blur the boundary between data and model. Furthermore, reinforcement learning has already been widely adopted in several data-centric AI sub-goals, such as data labeling [\[48,](#page-30-4) [66,](#page-30-10) [274\]](#page-37-9), data preparation [\[122\]](#page-32-11), data reduction [\[148\]](#page-33-11), and data augmentation [\[56,](#page-30-2) [273\]](#page-37-7). The reason could be attributed to its goal-oriented nature, which is well-suited for automation.

Upon examining the connections to these two rapidly evolving research fields, we hypothesize that data-centric AI and model-centric AI could become even more intertwined in the development of AI systems. Looking forward, we present some potential future directions we have identified in data-centric AI:

- Cross-task automation. While there has been significant progress in automating various individual data-centric AI tasks, joint automation across multiple tasks remains largely unexplored. Although pipeline search methods [\[76,](#page-30-11) [97,](#page-31-15) [132,](#page-32-6) [280\]](#page-37-13) have emerged, they are limited only to training data development. From a broad data-centric AI perspective, it would be desirable to have a unified framework for jointly automating tasks aimed at different goals, ranging from training data development to inference data development and data maintenance.
- Data-model co-design. Although data-centric AI advocates for shifting the focus to data, it does not necessarily imply that the model has to remain unchanged. The optimal data strategies may differ when using different models, and vice versa. Furthermore, as discussed above, the boundary between data and model could potentially become increasingly blurred with the advancement of foundation models and reinforcement learning. Consequently, future progress in AI could arise from co-designing data and models, and the co-evolution of data and models could pave the way toward more powerful AI systems.
- Debiasing data. In many high-stakes applications, AI systems have recently been found to exhibit discriminatory behavior towards certain groups of people, sparking significant concerns about fairness [\[50,](#page-30-28) [65,](#page-30-29) [112,](#page-32-27) [113,](#page-32-28) [157,](#page-33-26) [240\]](#page-36-16). These biases often originate from imbalanced distributions of sensitive variables in the data. From a data-centric perspective, more research efforts are needed to debias data, including but limited to mitigating biases in training data, systematic methodologies to construct evaluation data to expose unfairness issues of unfairness, and continuously maintaining fair data in a dynamic environment.
- Tackling data in various modalities. Based on the benchmark analysis presented in Section [6,](#page-24-0) most research efforts have been directed toward tabular and image data. However, other data modalities that are comparably important but less studied in data-centric AI pose significant challenges. For instance, time-series data [\[92,](#page-31-32) [141,](#page-33-27) [277\]](#page-37-25) exhibit complex temporal correlations, while graph data [\[134,](#page-32-29) [147,](#page-33-28) [226,](#page-35-29) [290](#page-37-26)[-293\]](#page-37-27) has intricate data dependencies. Therefore, more research on how to engineer data for these modalities is required. Furthermore, developing data-centric AI solutions that can simultaneously address multiple data modalities is an intriguing avenue for future exploration.
- Data benchmarks development. The advancement of model-centric AI has been facilitated by benchmarks in advancing model designs. Whereas data-centric AI requires more attention to benchmarking. As discussed in Section [6,](#page-24-0) existing benchmarks for data-centric AI typically only focus on specific tasks. Constructing a unified benchmark to evaluate overall data quality

and various data-centric AI techniques comprehensively presents a significant challenge. Although DataPerf [\[155\]](#page-33-7) has made notable progress towards this objective, it currently supports only a limited number of tasks. The development of more unified data benchmarks would greatly accelerate research progress in this area.

### 8 CONCLUSION

This survey focuses on data-centric AI, an emerging and important research field in AI. We motivated the need for data-centric AI by showing how carefully designing and maintaining data can make AI solutions more desirable across academia and industry. Next, we provided a background of data-centric AI, which includes its definition and a goal-driven taxonomy. Then, guided by the research questions posed, we reviewed various data-centric AI techniques for different purposes from the perspectives of automation and collaboration. Furthermore, we collected data benchmarks from different domains and analyzed them at a meta-level. Lastly, we discussed data-centric AI from a global view and shared our perspectives on the blurred boundaries between data and model. We also presented potential future directions for this field. To conclude in one line, we believe that data will play an increasingly important role in building AI systems. At the same time, there are still numerous challenges that need to be addressed. We hope our survey could inspire collaborative initiatives in our community to push forward this field.

### REFERENCES

- [1] Abdelaal, M., Hammacher, C., and Schoening, H. Rein: A comprehensive benchmark framework for data cleaning methods in ml pipelines. arXiv preprint arXiv:2302.04702 (2023).
- [2] Abdi, H., and Williams, L. J. Principal component analysis. Wiley interdisciplinary reviews: computational statistics 2, 4 (2010), 433-459.
- [3] Agarwal, A., Dahleh, M., and Sarkar, T. A marketplace for data: An algorithmic solution. In EC (2019).
- [4] Ahsan, M. M., Mahmud, M. P., Saha, P. K., Gupta, K. D., and Siddiqe, Z. Effect of data scaling methods on machine learning algorithms and model performance. Technologies 9, 3 (2021), 52.
- [5] Ali, P. J. M., Faraj, R. H., Koya, E., Ali, P. J. M., and Faraj, R. H. Data normalization and standardization: a technical report. Mach Learn Tech Rep 1, 1 (2014), 1-6.
- [6] Apache. Apache. https://storm.apache.org/releases/current/Performance.html (2023).
- [7] Armbrust, M., Ghodsi, A., Xin, R., and Zaharia, M. Lakehouse: a new generation of open platforms that unify data warehousing and advanced analytics. In CIDR (2021).
- [8] Arocena, P. C., Glavic, B., Mecca, G., Miller, R. J., Papotti, P., and Santoro, D. Benchmarking data curation systems. IEEE Data Eng. Bull. 39, 2 (2016), 47-62.
- [9] Aroyo, L., Lease, M., Paritosh, P., and Schaekermann, M. Data excellence for ai: why should you care? Interactions 29, 2 (2022), 66-69.
- [10] Azhagusundari, B., Thanamani, A. S., et al. Feature selection based on information gain. International Journal of Innovative Technology and Exploring Engineering (IJITEE) 2, 2 (2013), 18-21.
- [11] Azizzadenesheli, K., Liu, A., Yang, F., and Anandkumar, A. Regularized learning for domain adaptation under label shifts. arXiv preprint arXiv:1903.09734 (2019).
- [12] Baik, C., Jagadish, H. V., and Li, Y. Bridging the semantic gap with sql query logs in natural language interfaces to databases. In ICDE (2019).
- [13] Bank, D., Koenigstein, N., and Giryes, R. Autoencoders. arXiv preprint arXiv:2003.05991 (2020).
- [14] Barandas, M., Folgado, D., Fernandes, L., Santos, S., Abreu, M., Bota, P., Liu, H., Schultz, T., and Gamboa, H. Tsfel: Time series feature extraction library. SoftwareX 11 (2020), 100456.
- [15] Barclay, T., Gray, J., and Slutz, D. Microsoft terraserver: a spatial data warehouse. In SIGMOD (2000).
- [16] Barenstein, M. Propublica's compas data revisited. arXiv preprint arXiv:1906.04711 (2019).
- [17] Basu, A., and Blanning, R. W. Discovering implicit integrity constraints in rule bases using metagraphs. In HICSS (1995).
- [18] Batini, C., Cappiello, C., Francalanci, C., and Maurino, A. Methodologies for data quality assessment and improvement. ACM computing surveys (CSUR) 41, 3 (2009), 1-52.
- [19] Baylor, D., Breck, E., Cheng, H.-T., Fiedel, N., Foo, C. Y., Haqe, Z., Haykal, S., Ispir, M., Jain, V., Koc, L., et al. Tfx: A tensorflow-based production-scale machine learning platform. In KDD (2017).

- [20] Becker, M., Burkart, N., Birnstill, P., and Beyerer, J. A step towards global counterfactual explanations: Approximating the feature space through hierarchical division and graph search. Adv. Artif. Intell. Mach. Learn. 1, 2 (2021), 90-110.
- [21] Betzalel, E., Penso, C., Navon, A., and Fetaya, E. A study on the evaluation of generative models. arXiv preprint arXiv:2206.10935 (2022).
- [22] Bhardwaj, A., Bhattacherjee, S., Chavan, A., Deshpande, A., Elmore, A. J., Madden, S., and Parameswaran, A. G. Datahub: Collaborative data science & dataset version management at scale. In CIDR (2015).
- [23] Biggio, B., Corona, I., Maiorca, D., Nelson, B., Šrndić, N., Laskov, P., Giacinto, G., and Roli, F. Evasion attacks against machine learning at test time. In ECMLPKDD (2013).
- [24] Bisong, E., and Bisong, E. Introduction to scikit-learn. Building Machine Learning and Deep Learning Models on Google Cloud Platform: A Comprehensive Guide for Beginners (2019), 215-229.
- [25] Blachnik, M., and Kordos, M. Comparison of instance selection and construction methods with various classifiers. Applied Sciences 10, 11 (2020), 3933.
- [26] Blanchart, P. An exact counterfactual-example-based approach to tree-ensemble models interpretability. arXiv preprint arXiv:2105.14820 (2021).
- [27] Boecking, B., Neiswanger, W., Xing, E., and Dubrawski, A. Interactive weak supervision: Learning useful heuristics for data labeling. In ICLR (2021).
- [28] Bogatu, A., Fernandes, A. A., Paton, N. W., and Konstantinou, N. Dataset discovery in data lakes. In ICDE (2020).
- [29] Bohannon, P., Fan, W., Geerts, F., Jia, X., and Kementsietsidis, A. Conditional functional dependencies for data cleaning. In 2007 IEEE 23rd international conference on data engineering (2006), IEEE, pp. 746-755.
- [30] Bollacker, K., Evans, C., Paritosh, P., Sturge, T., and Taylor, J. Freebase: a collaboratively created graph database for structuring human knowledge. In SIGMOD (2008).
- [31] Bommert, A., Welchowski, T., Schmid, M., and Rahnenführer, J. Benchmark of filter methods for feature selection in high-dimensional gene expression survival data. Briefings in Bioinformatics 23, 1 (2022), bbab354.
- [32] Borgwardt, K. M., Gretton, A., Rasch, M. J., Kriegel, H.-P., Schölkopf, B., and Smola, A. J. Integrating structured biological data by kernel maximum mean discrepancy. Bioinformatics 22, 14 (2006), e49-e57.
- [33] Borkin, M. A., Vo, A. A., Bylinskii, Z., Isola, P., Sunkavalli, S., Oliva, A., and Pfister, H. What makes a visualization memorable? IEEE transactions on visualization and computer graphics 19, 12 (2013), 2306-2315.
- [34] Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., et al. Language models are few-shot learners. NeurIPS (2020).
- [35] Buckley, T., Ghosh, B., and Pakrashi, V. A feature extraction & selection benchmark for structural health monitoring. Structural Health Monitoring (2022), 14759217221111141.
- [36] Buolamwini, J., and Gebru, T. Gender shades: Intersectional accuracy disparities in commercial gender classification. In FAccT (2018).
- [37] Burch, M., and Weiskopf, D. On the benefits and drawbacks of radial diagrams. Handbook of human centric visualization (2014), 429-451.
- [38] Carreira-Perpinán, M. A., and Hada, S. S. Counterfactual explanations for oblique decision trees: Exact, efficient algorithms. In AAAI (2021).
- [39] Chaudhuri, S., and Narasayya, V. R. An efficient, cost-driven index selection tool for microsoft sql server. In VLDB (1997).
- [40] Chavan, M., Guravannavar, R., Ramachandra, K., and Sudarshan, S. Dbridge: A program rewrite tool for set-oriented query execution. In ICDE (2011).
- [41] Chawla, N. V., Bowyer, K. W., Hall, L. O., and Kegelmeyer, W. P. Smote: synthetic minority over-sampling technique. Journal of artificial intelligence research 16 (2002), 321-357.
- [42] Chen, J., Yang, Z., and Yang, D. Mixtext: Linguistically-informed interpolation of hidden space for semi-supervised text classification. In ACL (2020).
- [43] Chen, P.-Y., Zhang, H., Sharma, Y., Yi, J., and Hsieh, C.-J. Zoo: Zeroth order optimization based black-box attacks to deep neural networks without training substitute models. In AISec Workshop (2017).
- [44] Chen, T., Han, L., Demartini, G., Indulska, M., and Sadiq, S. Building data curation processes with crowd intelligence. In CAiSE (2020).
- [45] Chlap, P., Min, H., Vandenberg, N., Dowling, J., Holloway, L., and Haworth, A. A review of medical image data augmentation techniques for deep learning applications. Journal of Medical Imaging and Radiation Oncology 65, 5 (2021), 545-563.
- [46] Chong, Y., Ding, Y., Yan, Q., and Pan, S. Graph-based semi-supervised learning: A review. Neurocomputing 408 (2020), 216-230.
- [47] Chowdhary, K., and Chowdhary, K. Natural language processing. Fundamentals of artificial intelligence (2020), 603-649.

- [48] Christiano, P. F., Leike, J., Brown, T., Martic, M., Legg, S., and Amodei, D. Deep reinforcement learning from human preferences. In NeurIPS (2017).
- [49] Chu, X., Ilyas, I. F., and Papotti, P. Discovering denial constraints. In VLDB (2013).
- [50] Chuang, Y.-N., Lai, K.-H., Tang, R., Du, M., Chang, C.-Y., Zou, N., and Hu, X. Mitigating relational bias on knowledge graphs. arXiv preprint arXiv:2211.14489 (2022).
- [51] Chuang, Y.-N., Wang, G., Yang, F., Liu, Z., Cai, X., Du, M., and Hu, X. Efficient xai techniques: A taxonomic survey. arXiv preprint arXiv:2302.03225 (2023).
- [52] Chuang, Y.-N., Wang, G., Yang, F., Zhou, Q., Tripathi, P., Cai, X., and Hu, X. Cortx: Contrastive framework for real-time explanation. In ICLR (2023).
- [53] Chung, Y., Kraska, T., Polyzotis, N., Tae, K. H., and Whang, S. E. Slice finder: Automated data slicing for model validation. In ICDE (2019).
- [54] Cohen, T., Roberts, K., Gururaj, A. E., Chen, X., Pournejati, S., Alter, G., Hersh, W. R., Demner-Fushman, D., Ohno-Machado, L., and Xu, H. A publicly available benchmark for biomedical dataset retrieval: the reference standard for the 2016 biocaddie dataset retrieval challenge. Database 2017 (2017).
- [55] Cohn, D. A., Ghahramani, Z., and Jordan, M. I. Active learning with statistical models. Journal of artificial intelligence research 4 (1996), 129-145.
- [56] Cubuk, E. D., Zoph, B., Mane, D., Vasudevan, V., and Le, Q. V. Autoaugment: Learning augmentation policies from data. In CVPR (2019).
- [57] Dandl, S., Molnar, C., Binder, M., and Bischl, B. Multi-objective counterfactual explanations. In PPSN (2020).
- [58] Dekel, O., and Shamir, O. Vox populi: Collecting high-quality labels from a crowd. In COLT (2009).
- [59] Deng, J., Dong, W., Socher, R., Li, L.-J., Li, K., and Fei-Fei, L. Imagenet: A large-scale hierarchical image database. In CVPR (2009).
- [60] Deodhar, M., Ma, X., Cai, Y., Koes, A., Beutel, A., and Chen, J. A human-ml collaboration framework for improving video content reviews. arXiv preprint arXiv:2210.09500 (2022).
- [61] Desnoyers, L. Toward a taxonomy of visuals in science communication. Technical Communication 58, 2 (2011), 119-134.
- [62] Dhurandhar, A., Pedapati, T., Balakrishnan, A., Chen, P.-Y., Shanmugam, K., and Puri, R. Model agnostic contrastive explanations for structured data. arXiv preprint arXiv:1906.00117 (2019).
- [63] Ding, F., Hardt, M., Miller, J., and Schmidt, L. Retiring adult: New datasets for fair machine learning. In NeurIPS (2021).
- [64] Ding, K., Xu, Z., Tong, H., and Liu, H. Data augmentation for deep graph learning: A survey. ACM SIGKDD Explorations Newsletter 24, 2 (2022), 61-77.
- [65] Ding, S., Tang, R., Zha, D., Zou, N., Zhang, K., Jiang, X., and Hu, X. Fairly predicting graft failure in liver transplant for organ assigning. arXiv preprint arXiv:2302.09400 (2023).
- [66] Dong, J., Zhang, Q., Huang, X., Tan, Q., Zha, D., and Zhao, Z. Active ensemble learning for knowledge graph error detection. In WSDM (2023).
- [67] Dong, Y., Fu, Q.-A., Yang, X., Pang, T., Su, H., Xiao, Z., and Zhu, J. Benchmarking adversarial robustness on image classification. In CVPR (2020).
- [68] Drori, I., Krishnamurthy, Y., Rampin, R., Lourenco, R. d. P., Ono, J. P., Cho, K., Silva, C., and Freire, J. Alphad3m: Machine learning pipeline synthesis. arXiv preprint arXiv:2111.02508 (2021).
- [69] Duan, S., Thummala, V., and Babu, S. Tuning database configuration parameters with ituned. In VLDB (2009).
- [70] Espadoto, M., Martins, R. M., Kerren, A., Hirata, N. S., and Telea, A. C. Toward a quantitative survey of dimension reduction techniques. IEEE transactions on visualization and computer graphics 27, 3 (2019), 2153-2173.
- [71] Eykholt, K., Evtimov, I., Fernandes, E., Li, B., Rahmati, A., Xiao, C., Prakash, A., Kohno, T., and Song, D. Robust physical-world attacks on deep learning visual classification. In CVPR (2018).
- [72] Fahad, A., Alshatri, N., Tari, Z., Alamri, A., Khalil, I., Zomaya, A. Y., Foufou, S., and Bouras, A. A survey of clustering algorithms for big data: Taxonomy and empirical analysis. IEEE transactions on emerging topics in computing 2, 3 (2014), 267-279.
- [73] Farahani, A., Voghoei, S., Rasheed, K., and Arabnia, H. R. A brief review of domain adaptation. Advances in Data Science and Information Engineering: Proceedings from ICDATA 2020 and IKE 2020 (2021), 877-894.
- [74] Feng, S. Y., Gangal, V., Wei, J., Chandar, S., Vosoughi, S., Mitamura, T., and Hovy, E. A survey of data augmentation approaches for nlp. In ACL (2021).
- [75] Fernandez, R. C., Abedjan, Z., Koko, F., Yuan, G., Madden, S., and Stonebraker, M. Aurum: A data discovery system. In ICDE (2018).
- [76] Feurer, M., Klein, A., Eggensperger, K., Springenberg, J., Blum, M., and Hutter, F. Efficient and robust automated machine learning. In NeurIPS (2015).
- [77] Foundation, A. S. Hadoop. https://hadoop.apache.org (2023).

- [78] Franconeri, S. L., Padilla, L. M., Shah, P., Zacks, J. M., and Hullman, J. The science of visual data communication: What works. Psychological Science in the public interest 22, 3 (2021), 110-161.
- [79] Frid-Adar, M., Klang, E., Amitai, M., Goldberger, J., and Greenspan, H. Synthetic data augmentation using gan for improved liver lesion classification. In ISBI (2018).
- [80] Galhotra, S., Golshan, B., and Tan, W.-C. Adaptive rule discovery for labeling text data. In SIGMOD (2021).
- [81] Gamboa, E., Libreros, A., Hirth, M., and Dubiner, D. Human-ai collaboration for improving the identification of cars for autonomous driving. In CIKM Workshop (2022).
- [82] Gao, T., Fisch, A., and Chen, D. Making pre-trained language models better few-shot learners. In ACL (2021).
- [83] Ghorbani, A., Kim, M., and Zou, J. A distributional framework for data valuation. In ICML (2020).
- [84] Ghorbani, A., and Zou, J. Data shapley: Equitable valuation of data for machine learning. In ICML (2019).
- [85] Gijsbers, P., Bueno, M. L., Coors, S., LeDell, E., Poirier, S., Thomas, J., Bischl, B., and Vanschoren, J. Amlb: an automl benchmark. arXiv preprint arXiv:2207.12560 (2022).
- [86] Goodfellow, I., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D., Ozair, S., Courville, A., and Bengio, Y. Generative adversarial networks. Communications of the ACM 63, 11 (2020), 139-144.
- [87] Gretton, A., Smola, A., Huang, J., Schmittfull, M., Borgwardt, K., and Schölkopf, B. Covariate shift by kernel mean matching. Dataset shift in machine learning 3, 4 (2009), 5.
- [88] Grinstein, G. G., Hoffman, P., Pickett, R. M., and Laskowski, S. J. Benchmark development for the evaluation of visualization for data mining. Information visualization in data mining and knowledge discovery (2002), 129-176.
- [89] Grochowski, M., and Jankowski, N. Comparison of instance selection algorithms ii. results and comments. In ICAISC (2004).
- [90] Gu, K., Yang, B., Ngiam, J., Le, Q., and Shlens, J. Using videos to evaluate image model robustness. arXiv preprint arXiv:1904.10076 (2019).
- [91] Guan, H., and Liu, M. Domain adaptation for medical image analysis: a survey. IEEE Transactions on Biomedical Engineering 69, 3 (2021), 1173-1185.
- [92] Hamilton, J. D. Time series analysis. Princeton university press, 2020.
- [93] Han, X., Jiang, Z., Liu, N., and Hu, X. G-mixup: Graph data augmentation for graph classification. In ICML (2022).
- [94] Haviv, A., Berant, J., and Globerson, A. Bertese: Learning to speak to bert. In EACL (2021).
- [95] He, H., Bai, Y., Garcia, E. A., and Li, S. Adasyn: Adaptive synthetic sampling approach for imbalanced learning. In WCCI (2008).
- [96] He, Y., Tang, J., Ouyang, H., Kang, C., Yin, D., and Chang, Y. Learning to rewrite queries. In CIKM (2016).
- [97] Heffetz, Y., Vainshtein, R., Katz, G., and Rokach, L. Deepline: Automl tool for pipelines generation using deep reinforcement learning and hierarchical actions filtering. In KDD (2020).
- [98] Heise, A., Kasneci, G., and Naumann, F. Estimating the number and sizes of fuzzy-duplicate clusters. In CIKM (2014).
- [99] Hendrycks, D., and Dietterich, T. Benchmarking neural network robustness to common corruptions and perturbations. arXiv preprint arXiv:1903.12261 (2019).
- [100] Herodotou, H., Lim, H., Luo, G., Borisov, N., Dong, L., Cetin, F. B., and Babu, S. Starfish: A self-tuning system for big data analytics. In CIDR (2011).
- [101] Ho, J., Jain, A., and Abbeel, P. Denoising diffusion probabilistic models. In NeurIPS (2020).
- [102] Ho, J., Saharia, C., Chan, W., Fleet, D. J., Norouzi, M., and Salimans, T. Cascaded diffusion models for high fidelity image generation. J. Mach. Learn. Res. 23, 47 (2022), 1-33.
- [103] Hooper, S., Wornow, M., Seah, Y. H., Kellman, P., Xue, H., Sala, F., Langlotz, C., and Re, C. Cut out the annotator, keep the cutout: better segmentation with weak supervision. In ICLR (2021).
- [104] Hsu, W.-N., Zhang, Y., and Glass, J. Unsupervised domain adaptation for robust speech recognition via variational autoencoder-based data augmentation. In ASRU (2017).
- [105] Iwana, B. K., and Uchida, S. An empirical survey of data augmentation for time series classification with neural networks. Plos one 16, 7 (2021), e0254841.
- [106] Jäger, S., Allhorn, A., and Biessmann, F. A benchmark for data imputation methods. Frontiers in big Data 4 (2021), 693674.
- [107] Jain, A., Patel, H., Nagalapatti, L., Gupta, N., Mehta, S., Guttula, S., Mujumdar, S., Afzal, S., Sharma Mittal, R., and Munigala, V. Overview and importance of data quality for machine learning tasks. In KDD (2020).
- [108] Jakubik, J., Vössing, M., Kühl, N., Walk, J., and Satzger, G. Data-centric artificial intelligence. arXiv preprint arXiv:2212.11854 (2022).
- [109] Jarrahi, M. H., Memariani, A., and Guha, S. The principles of data-centric ai (dcai). arXiv preprint arXiv:2211.14611 (2022).
- [110] Jia, R., Wu, F., Sun, X., Xu, J., Dao, D., Kailkhura, B., Zhang, C., Li, B., and Song, D. Scalability vs. utility: Do we have to sacrifice one for the other in data importance quantification? In CVPR (2021).

- [111] Jiang, M., Hou, C., Zheng, A., Hu, X., Han, S., Huang, H., He, X., Yu, P. S., and Zhao, Y. Weakly supervised anomaly detection: A survey. arXiv preprint arXiv:2302.04549 (2023).
- [112] Jiang, Z., Han, X., Fan, C., Liu, Z., Zou, N., Mostafavi, A., and Hu, X. Fmp: Toward fair graph message passing against topology bias. arXiv preprint arXiv:2202.04187 (2022).
- [113] Jiang, Z., Han, X., Fan, C., Yang, F., Mostafavi, A., and Hu, X. Generalized demographic parity for group fairness. In ICLR (2022).
- [114] Jiang, Z., Han, X., Jin, H., Wang, G., Zou, N., and Hu, X. Weight perturbation can help fairness under distribution shift. arXiv preprint arXiv:2303.03300 (2023).
- [115] Jiang, Z., Xu, F. F., Araki, J., and Neubig, G. How can we know what language models know? Transactions of the Association for Computational Linguistics 8 (2020), 423-438.
- [116] Jiang, Z., Zhou, K., Liu, Z., Li, L., Chen, R., Choi, S.-H., and Hu, X. An information fusion approach to learning with instance-dependent label noise. In ICLR (2022).
- [117] Jumper, J., Evans, R., Pritzel, A., Green, T., Figurnov, M., Ronneberger, O., Tunyasuvunakool, K., Bates, R., Žídek, A., Potapenko, A., et al. Highly accurate protein structure prediction with alphafold. Nature 596, 7873 (2021), 583-589.
- [118] Kanamori, K., Takagi, T., Kobayashi, K., and Arimura, H. Dace: Distribution-aware counterfactual explanation by mixed-integer linear optimization. In IJCAI (2020).
- [119] Kanthara, S., Leong, R. T. K., Lin, X., Masry, A., Thakkar, M., Hoqe, E., and Joty, S. Chart-to-text: A large-scale benchmark for chart summarization. arXiv preprint arXiv:2203.06486 (2022).
- [120] Karimi, A.-H., Schölkopf, B., and Valera, I. Algorithmic recourse: from counterfactual explanations to interventions. In FAccT (2021).
- [121] Kenton, J. D. M.-W. C., and Toutanova, L. K. Bert: Pre-training of deep bidirectional transformers for language understanding. In NAACL (2019).
- [122] Khurana, U., Samulowitz, H., and Turaga, D. Feature engineering for predictive modeling using reinforcement learning. In AAAI (2018).
- [123] Kim, M. P., Ghorbani, A., and Zou, J. Multiaccuracy: Black-box post-processing for fairness in classification. In AIES (2019).
- [124] Kingma, D., Salimans, T., Poole, B., and Ho, J. Variational diffusion models. In NeurIPS (2021).
- [125] Koh, P. W., Sagawa, S., Marklund, H., Xie, S. M., Zhang, M., Balsubramani, A., Hu, W., Yasunaga, M., Phillips, R. L., Gao, I., et al. Wilds: A benchmark of in-the-wild distribution shifts. In ICML (2021).
- [126] Krishnan, S., and Wu, E. Alphaclean: Automatic generation of data cleaning pipelines. arXiv preprint arXiv:1904.11827 (2019).
- [127] Krizhevsky, A., Sutskever, I., and Hinton, G. E. Imagenet classification with deep convolutional neural networks. Communications of the ACM 60, 6 (2017), 84-90.
- [128] Kumar, A., Naughton, J., Patel, J. M., and Zhu, X. To join or not to join? thinking twice about joins before feature selection. In SIGMOD (2016).
- [129] Kurakin, A., Goodfellow, I. J., and Bengio, S. Adversarial examples in the physical world. In Artificial intelligence safety and security. Chapman and Hall/CRC, 2018, pp. 99-112.
- [130] Kutlu, M., McDonnell, T., Elsayed, T., and Lease, M. Annotator rationales for labeling tasks in crowdsourcing. Journal of Artificial Intelligence Research 69 (2020), 143-189.
- [131] Lai, K.-H., Zha, D., Li, Y., and Hu, X. Dual policy distillation. In IJCAI (2020).
- [132] Lai, K.-H., Zha, D., Wang, G., Xu, J., Zhao, Y., Kumar, D., Chen, Y., Zumkhawaka, P., Wan, M., Martinez, D., et al. Tods: An automated time series outlier detection system. In AAAI (2021).
- [133] Lai, K.-H., Zha, D., Xu, J., Zhao, Y., Wang, G., and Hu, X. Revisiting time series outlier detection: Definitions and benchmarks. In NeurIPS (2021).
- [134] Lai, K.-H., Zha, D., Zhou, K., and Hu, X. Policy-gnn: Aggregation optimization for graph neural networks. In KDD (2020).
- [135] Lakshminarayan, K., Harp, S. A., Goldman, R. P., Samad, T., et al. Imputation of missing data using machine learning techniques. In KDD (1996).
- [136] Laugel, T., Lesot, M.-J., Marsala, C., Renard, X., and Detyniecki, M. Comparison-based inverse classification for interpretability in machine learning. In IPMU (2018).
- [137] Lenzerini, M. Data integration: A theoretical perspective. In PODS (2002).
- [138] Li, J., Cheng, K., Wang, S., Morstatter, F., Trevino, R. P., Tang, J., and Liu, H. Feature selection: A data perspective. ACM computing surveys (CSUR) 50, 6 (2017), 1-45.
- [139] Li, P., Rao, X., Blase, J., Zhang, Y., Chu, X., and Zhang, C. Cleanml: A benchmark for joint data cleaning and machine learning [experiments and analysis]. arXiv preprint arXiv:1904.09483 (2019), 75.
- [140] Li, X., Metsis, V., Wang, H., and Ngu, A. H. H. Tts-gan: A transformer-based time-series generative adversarial

network. In AIME (2022).

- [141] Li, Y., Chen, Z., Zha, D., Du, M., Ni, J., Zhang, D., Chen, H., and Hu, X. Towards learning disentangled representations for time series. In KDD (2022).
- [142] Li, Y., Chen, Z., Zha, D., Zhou, K., Jin, H., Chen, H., and Hu, X. Automated anomaly detection via curiosity-guided search and self-imitation learning. IEEE Transactions on Neural Networks and Learning Systems 33, 6 (2021), 2365-2377.
- [143] Li, Y., Chen, Z., Zha, D., Zhou, K., Jin, H., Chen, H., and Hu, X. Autood: Neural architecture search for outlier detection. In ICDE (2021).
- [144] Li, Y., Zha, D., Venugopal, P., Zou, N., and Hu, X. Pyodds: An end-to-end outlier detection system with automated machine learning. In WWW (2020).
- [145] Lipton, Z., Wang, Y.-X., and Smola, A. Detecting and correcting for label shift with black box predictors. In ICML (2018).
- [146] Liu, P., Yuan, W., Fu, J., Jiang, Z., Hayashi, H., and Neubig, G. Pre-train, prompt, and predict: A systematic survey of prompting methods in natural language processing. ACM Computing Surveys 55, 9 (2023), 1-35.
- [147] Liu, Z., Chen, S., Zhou, K., Zha, D., Huang, X., and Hu, X. Rsc: Accelerating graph neural networks training via randomized sparse computations. arXiv preprint arXiv:2210.10737 (2022).
- [148] Liu, Z., Wei, P., Jiang, J., Cao, W., Bian, J., and Chang, Y. Mesa: boost ensemble imbalanced learning with meta-sampler. In NeurIPS (2020).
- [149] Lucic, A., Oosterhuis, H., Haned, H., and de Rijke, M. Focus: Flexible optimizable counterfactual explanations for tree ensembles. In AAAI (2022).
- [150] Luo, Y., Qin, X., Tang, N., and Li, G. Deepeye: Towards automatic data visualization. In 2018 IEEE 34th international conference on data engineering (ICDE) (2018), IEEE, pp. 101-112.
- [151] Madry, A., Makelov, A., Schmidt, L., Tsipras, D., and Vladu, A. Towards deep learning models resistant to adversarial attacks. arXiv preprint arXiv:1706.06083 (2017).
- [152] Management, C. P. Clouderayarntuning. https://docs.cloudera.com/documentation/enterprise/latest/topics/cdh\_ig\_yarn\_tuning.html (2023).
- [153] Marcus, R., Kipf, A., van Renen, A., Stoian, M., Misra, S., Kemper, A., Neumann, T., and Kraska, T. Benchmarking learned indexes. In VLDB (2020).
- [154] Martinex, D., Zha, D., Tan, Q., and Hu, X. Towards personalized preprocessing pipeline search. arXiv preprint arXiv:2302.14329 (2023).
- [155] Mazumder, M., Banbury, C., Yao, X., Karlaš, B., Rojas, W. G., Diamos, S., Diamos, G., He, L., Kiela, D., Jurado, D., et al. Dataperf: Benchmarks for data-centric ai development. arXiv preprint arXiv:2207.10062 (2022).
- [156] Meduri, V. V., Popa, L., Sen, P., and Sarwat, M. A comprehensive benchmark framework for active learning methods in entity matching. In SIGMOD (2020).
- [157] Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K., and Galstyan, A. A survey on bias and fairness in machine learning. ACM Computing Surveys (CSUR) 54, 6 (2021), 1-35.
- [158] Meng, C., Trinh, L., Xu, N., Enouen, J., and Liu, Y. Interpretability and fairness evaluation of deep learning models on mimic-iv dataset. Scientific Reports 12, 1 (2022), 7166.
- [159] Milutinovic, M., Schoenfeld, B., Martinez-Garcia, D., Ray, S., Shah, S., and Yan, D. On evaluation of automl systems. In ICML Workshop (2020).
- [160] Mintz, M., Bills, S., Snow, R., and Jurafsky, D. Distant supervision for relation extraction without labeled data. In ACL (2009).
- [161] Miotto, R., Wang, F., Wang, S., Jiang, X., and Dudley, J. T. Deep learning for healthcare: review, opportunities and challenges. Briefings in bioinformatics 19, 6 (2018), 1236-1246.
- [162] Miranda, L. J. Towards data-centric machine learning: a short review. ljvmiranda921.github.io (2021).
- [163] Mirdita, M., Von Den Driesch, L., Galiez, C., Martin, M. J., Söding, J., and Steinegger, M. Uniclust databases of clustered and deeply annotated protein sequences and alignments. Nucleic acids research 45, D1 (2017), D170-D176.
- [164] Mnih, V., Kavukcuoglu, K., Silver, D., Graves, A., Antonoglou, I., Wierstra, D., and Riedmiller, M. Playing atari with deep reinforcement learning. arXiv preprint arXiv:1312.5602 (2013).
- [165] Moosavi-Dezfooli, S.-M., Fawzi, A., and Frossard, P. Deepfool: a simple and accurate method to fool deep neural networks. In CVPR (2016).
- [166] Nanni, L., Paci, M., Brahnam, S., and Lumini, A. Comparison of different image data augmentation approaches. Journal of imaging 7, 12 (2021), 254.
- [167] Nargesian, F., Zhu, E., Pu, K. Q., and Miller, R. J. Table union search on open data. In VLDB (2018).
- [168] Ng, A. Data-centric ai resource hub. Snorkel AI. Available online: https://snorkel.ai/(accessed on 8 February 2023) (2021).
- [169] Ng, A. Landing ai. Landing AI. Available online: https://landing.ai/(accessed on 8 February 2023) (2023).
- [170] Ng, A., Laird, D., and He, L. Data-centric ai competition. DeepLearning AI. Available online: https://https-deeplearningai. github. io/data-centric-comp/(accessed on 8 December 2021) (2021).

Data-centric Artificial Intelligence: A Survey 35

- [171] Obukhov, A., and Krasnyanskiy, M. Quality assessment method for gan based on modified metrics inception score and fréchet inception distance. In CoMeSySo (2020).
- [172] OpenAI. Gpt-4 technical report, 2023.
- [173] Otles, E., Oh, J., Li, B., Bochinski, M., Joo, H., Ortwine, J., Shenoy, E., Washer, L., Young, V. B., Rao, K., et al. Mind the performance gap: examining dataset shift during prospective validation. In MLHC (2021).
- [174] Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C. L., Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A., et al. Training language models to follow instructions with human feedback. In NeurIPS (2022).
- [175] Ozbayoglu, A. M., Gudelek, M. U., and Sezer, O. B. Deep learning for financial applications: A survey. Applied Soft Computing 93 (2020), 106384.
- [176] Pang, G., Shen, C., Cao, L., and Hengel, A. V. D. Deep learning for anomaly detection: A review. ACM computing surveys (CSUR) 54, 2 (2021), 1-38.
- [177] Papernot, N., McDaniel, P., Goodfellow, I., Jha, S., Celik, Z. B., and Swami, A. Practical black-box attacks against machine learning. In ASIACCS (2017).
- [178] Pawelczyk, M., Bielawski, S., Heuvel, J. v. d., Richter, T., and Kasneci, G. Carla: a python library to benchmark algorithmic recourse and counterfactual explanation algorithms. arXiv preprint arXiv:2108.00783 (2021).
- [179] Pedrozo, W. G., Nievola, J. C., and Ribeiro, D. C. An adaptive approach for index tuning with learning classifier systems on hybrid storage environments. In HAIS (2018).
- [180] Pinkel, C., Binnig, C., Jiménez-Ruiz, E., May, W., Ritze, D., Skjæveland, M. G., Solimando, A., and Kharlamov, E. Rodi: A benchmark for automatic mapping generation in relational-to-ontology data integration. In ESWC (2015).
- [181] Pipino, L. L., Lee, Y. W., and Wang, R. Y. Data quality assessment. Communications of the ACM 45, 4 (2002), 211-218.
- [182] Poess, M., Rabl, T., Jacobsen, H.-A., and Caufield, B. Tpc-di: the first industry benchmark for data integration. In VLDB (2014).
- [183] Polyzotis, N., and Zaharia, M. What can data-centric ai learn from data and ml engineering? arXiv preprint arXiv:2112.06439 (2021).
- [184] Poyiadzi, R., Sokol, K., Santos-Rodriguez, R., De Bie, T., and Flach, P. Face: feasible and actionable counterfactual explanations. In AAAI (2020).
- [185] Press, G. Cleaning big data: Most time-consuming, least enjoyable data science task, survey says, Oct 2022.
- [186] Prusa, J., Khoshgoftaar, T. M., Dittman, D. J., and Napolitano, A. Using random undersampling to alleviate class imbalance on tweet sentiment data. In IRI (2015).
- [187] Radford, A., Narasimhan, K., Salimans, T., Sutskever, I., et al. Improving language understanding by generative pre-training. OpenAI (2018).
- [188] Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., Sutskever, I., et al. Language models are unsupervised multitask learners. OpenAI (2019).
- [189] Ratner, A. Scale ai. Snorkel AI. Available online: https://snorkel.ai/(accessed on 8 February 2023) (2023).
- [190] Ratner, A., Bach, S. H., Ehrenberg, H., Fries, J., Wu, S., and Ré, C. Snorkel: Rapid training data creation with weak supervision. In VLDB (2017).
- [191] Ratner, A. J., De Sa, C. M., Wu, S., Selsam, D., and Ré, C. Data programming: Creating large training sets, quickly. NeurIPS (2016).
- [192] Ren, P., Xiao, Y., Chang, X., Huang, P.-Y., Li, Z., Gupta, B. B., Chen, X., and Wang, X. A survey of deep active learning. ACM computing surveys (CSUR) 54, 9 (2021), 1-40.
- [193] Riqelme, J. C., Aguilar-Ruiz, J. S., and Toro, M. Finding representative patterns with ordered projections. pattern recognition 36, 4 (2003), 1009-1018.
- [194] Rombach, R., Blattmann, A., Lorenz, D., Esser, P., and Ommer, B. High-resolution image synthesis with latent diffusion models. In CVPR (2022).
- [195] Sadiq, S., Dasu, T., Dong, X. L., Freire, J., Ilyas, I. F., Link, S., Miller, M. J., Naumann, F., Zhou, X., and Srivastava, D. Data quality: The role of empiricism. ACM SIGMOD Record 46, 4 (2018), 35-43.
- [196] Sadri, Z., Gruenwald, L., and Leal, E. Online index selection using deep reinforcement learning for a cluster database. In ICDE Workshop (2020).
- [197] Saenko, K., Kulis, B., Fritz, M., and Darrell, T. Adapting visual category models to new domains. In ECCV (2010).
- [198] Sagadeeva, S., and Boehm, M. Sliceline: Fast, linear-algebra-based slice finding for ml model debugging. In SIGMOD (2021).
- [199] Salau, A. O., and Jain, S. Feature extraction: a survey of the types, techniques, applications. In ICSC (2019).
- [200] Sambasivan, N., Kapania, S., Highfill, H., Akrong, D., Paritosh, P., and Aroyo, L. M. "everyone wants to do the model work, not the data work": Data cascades in high-stakes ai. In CHI (2021).
- [201] Sangkloy, P., Lu, J., Fang, C., Yu, F., and Hays, J. Scribbler: Controlling deep image synthesis with sketch and color. In CVPR (2017).
- [202] Santelices, R., Zhang, Y., Jiang, S., Cai, H., and Zhang, Y.-j. Quantitative program slicing: Separating statements

36 Daochen Zha, Zaid Pervaiz Bhat, Kwei-Herng Lai, Fan Yang, Zhimeng Jiang, Shaochen Zhong, and Xia Hu

by relevance. In ICSE (2013).

- [203] Saporta, G. Data fusion and data grafting. Computational statistics & data analysis 38, 4 (2002), 465-473.
- [204] Schelter, S., Lange, D., Schmidt, P., Celikel, M., Biessmann, F., and Grafberger, A. Automating large-scale data quality verification. In VLDB (2018).
- [205] Schick, T., and Schütze, H. Exploiting cloze questions for few shot text classification and natural language inference. arXiv preprint arXiv:2001.07676 (2020).
- [206] Schick, T., and Schütze, H. Few-shot text generation with pattern-exploiting training. arXiv preprint arXiv:2012.11926 (2020).
- [207] Schick, T., and Schütze, H. It's not just size that matters: Small language models are also few-shot learners. arXiv preprint arXiv:2009.07118 (2020).
- [208] Schnapp, S., and Sabato, S. Active feature selection for the mutual information criterion. In AAAI (2021).
- [209] Seedat, N., Imrie, F., and van der Schaar, M. Dc-check: A data-centric ai checklist to guide the development of reliable machine learning systems. arXiv preprint arXiv:2211.05764 (2022).
- [210] Shafahi, A., Huang, W. R., Najibi, M., Suciu, O., Studer, C., Dumitras, T., and Goldstein, T. Poison frogs! targeted clean-label poisoning attacks on neural networks. In NeurIPS (2018).
- [211] Shankar, V., Dave, A., Roelofs, R., Ramanan, D., Recht, B., and Schmidt, L. Do image classifiers generalize across time? In ICCV (2021).
- [212] Sharma, S., Henderson, J., and Ghosh, J. Certifai: Counterfactual explanations for robustness, transparency, interpretability, and fairness of artificial intelligence models. arXiv preprint arXiv:1905.07857 (2019).
- [213] Shen, L., Shen, E., Luo, Y., Yang, X., Hu, X., Zhang, X., Tai, Z., and Wang, J. Towards natural language interfaces for data visualization: A survey. arXiv preprint arXiv:2109.03506 (2021).
- [214] Shen, Z., Liu, J., He, Y., Zhang, X., Xu, R., Yu, H., and Cui, P. Towards out-of-distribution generalization: A survey. arXiv preprint arXiv:2108.13624 (2021).
- [215] Shorten, C., and Khoshgoftaar, T. M. A survey on image data augmentation for deep learning. Journal of big data 6, 1 (2019), 1-48.
- [216] Shorten, C., Khoshgoftaar, T. M., and Furht, B. Text data augmentation for deep learning. Journal of big Data 8 (2021), 1-34.
- [217] Sohoni, N., Dunnmon, J., Angus, G., Gu, A., and Ré, C. No subclass left behind: Fine-grained robustness in coarse-grained classification problems. In NeurIPS (2020).
- [218] Souza, J. T. d., Francisco, A. C. d., Piekarski, C. M., and Prado, G. F. d. Data mining and machine learning to promote smart cities: A systematic review from 2000 to 2018. Sustainability 11, 4 (2019), 1077.
- [219] Srinivasan, A., and Setlur, V. Snowy: Recommending utterances for conversational visual analysis. In SIGCHI (2021).
- [220] Srivastava, A., Rastogi, A., Rao, A., Shoeb, A. A. M., Abid, A., Fisch, A., Brown, A. R., Santoro, A., Gupta, A., Garriga-Alonso, A., et al. Beyond the imitation game: Quantifying and extrapolating the capabilities of language models. arXiv preprint arXiv:2206.04615 (2022).
- [221] Stonebraker, M., Bruckner, D., Ilyas, I. F., Beskales, G., Cherniack, M., Zdonik, S. B., Pagan, A., and Xu, S. Data curation at scale: the data tamer system. In CIDR (2013).
- [222] Stonebraker, M., Ilyas, I. F., et al. Data integration: The current status and the way forward. IEEE Data Eng. Bull. 41, 2 (2018), 3-9.
- [223] Sugiyama, M., Krauledat, M., and Müller, K.-R. Covariate shift adaptation by importance weighted cross validation. Journal of Machine Learning Research 8, 5 (2007).
- [224] Sun, J., and Li, G. An end-to-end learning-based cost estimator. In VLDB (2019).
- [225] Sutton, O. Introduction to k nearest neighbour classification and condensed nearest neighbour data reduction. University lectures, University of Leicester 1 (2012).
- [226] Tan, Q., Zhang, X., Liu, N., Zha, D., Li, L., Chen, R., Choi, S.-H., and Hu, X. Bring your own view: Graph neural networks for link prediction with personalized subgraph selection. In WSDM (2023).
- [227] Tang, W., and Lease, M. Semi-supervised consensus labeling for crowdsourcing. In SIGIR Workshop (2011).
- [228] Tao, Y., McKenna, R., Hay, M., Machanavajjhala, A., and Miklau, G. Benchmarking differentially private synthetic data generation algorithms. arXiv preprint arXiv:2112.09238 (2021).
- [229] Thaseen, I. S., and Kumar, C. A. Intrusion detection model using fusion of chi-square feature selection and multi class svm. Journal of King Saud University-Computer and Information Sciences 29, 4 (2017), 462-472.
- [230] Thirumuruganathan, S., Tang, N., Ouzzani, M., and Doan, A. Data curation with deep learning. In EDBT (2020).
- [231] Thusoo, A., Shao, Z., Anthony, S., Borthakur, D., Jain, N., Sen Sarma, J., Murthy, R., and Liu, H. Data warehousing and analytics infrastructure at facebook. In SIGMOD (2010).
- [232] Valentin, G., Zuliani, M., Zilio, D. C., Lohman, G., and Skelley, A. Db2 advisor: An optimizer smart enough to recommend its own indexes. In ICDE (2000).

- [233] Van Aken, D., Pavlo, A., Gordon, G. J., and Zhang, B. Automatic database management system tuning through large-scale machine learning. In SIGMOD (2017).
- [234] Varia, J., Mathew, S., et al. Overview of amazon web services. Amazon Web Services (2014).
- [235] Vijayan, A., Fatima, S., Sowmya, A., and Vafaee, F. Blood-based transcriptomic signature panel identification for cancer diagnosis: benchmarking of feature extraction methods. Briefings in Bioinformatics 23, 5 (2022), bbac315.
- [236] Voulodimos, A., Doulamis, N., Doulamis, A., Protopapadakis, E., et al. Deep learning for computer vision: A brief review. Computational intelligence and neuroscience 2018 (2018).
- [237] Wachter, S., Mittelstadt, B., and Russell, C. Counterfactual explanations without opening the black box: Automated decisions and the gdpr. Harv. JL & Tech. 31 (2017), 841.
- [238] Waldner, M., Diehl, A., Gračanin, D., Splechtna, R., Delrieux, C., and Matković, K. A comparison of radial and linear charts for visualizing daily patterns. IEEE transactions on visualization and computer graphics 26, 1 (2019).
- [239] Wallace, E., Feng, S., Kandpal, N., Gardner, M., and Singh, S. Universal adversarial triggers for attacking and analyzing nlp. In IJCNLP (2019).
- [240] Wan, M., Zha, D., Liu, N., and Zou, N. In-processing modeling techniques for machine learning fairness: A survey. ACM Transactions on Knowledge Discovery from Data (TKDD) (2022).
- [241] Wang, A. Scale ai. Scale AI. Available online: https://scale.com/(accessed on 8 February 2023) (2023).
- [242] Wang, G., Bhat, Z. P., Jiang, Z., Chen, Y.-W., Zha, D., Reyes, A. C., Niktash, A., Ulkar, G., Okman, E., Cai, X., et al. Bed: A real-time object detection system for edge devices. In CIKM (2022), pp. 4994-4998.
- [243] Wang, G., Chuang, Y.-N., Du, M., Yang, F., Zhou, Q., Tripathi, P., Cai, X., and Hu, X. Accelerating shapley explanation via contributive cooperator selection. In ICML (2022).
- [244] Wang, J., Kraska, T., Franklin, M. J., and Feng, J. Crowder: crowdsourcing entity resolution. In VLDB (2012).
- [245] Wang, S., Tang, J., and Liu, H. Embedded unsupervised feature selection. In AAAI (2015).
- [246] Wang, Y., Chen, H., Fan, Y., Wang, S., Tao, R., Hou, W., Wang, R., Yang, L., Zhou, Z., Guo, L.-Z., et al. Usb: A unified semi-supervised learning benchmark for classification. In NeurIPS (2022).
- [247] Wang, Y., Wang, Q., Huang, H., Huang, W., Chen, Y., McGarvey, P. B., Wu, C. H., Arighi, C. N., and Consortium, U. A crowdsourcing open platform for literature curation in uniprot. PLoS biology 19, 12 (2021), e3001464.
- [248] Wang, Z., Yan, W., and Oates, T. Time series classification from scratch with deep neural networks: A strong baseline. In IJCNN (2017).
- [249] Webb, S., et al. Deep learning for biology. Nature 554, 7693 (2018), 555-557.
- [250] Wen, Q., Sun, L., Yang, F., Song, X., Gao, J., Wang, X., and Xu, H. Time series data augmentation for deep learning: A survey. In IJCAI (2021).
- [251] Whang, S. E., Roh, Y., Song, H., and Lee, J.-G. Data collection and quality challenges in deep learning: A data-centric ai perspective. In VLDB (2023).
- [252] White, T. Hadoop: The definitive guide. " O'Reilly Media, Inc.", 2012.
- [253] Winston, P. H. Artificial intelligence. Addison-Wesley Longman Publishing Co., Inc., 1984.
- [254] Wongsuphasawat, K., Moritz, D., Anand, A., Mackinlay, J., Howe, B., and Heer, J. Voyager: Exploratory analysis via faceted browsing of visualization recommendations. IEEE transactions on visualization and computer graphics 22, 1 (2015), 649-658.
- [255] Xanthopoulos, P., Pardalos, P. M., Trafalis, T. B., Xanthopoulos, P., Pardalos, P. M., and Trafalis, T. B. Linear discriminant analysis. Robust data mining (2013), 27-33.
- [256] Xing, X., Liu, H., Chen, C., and Li, J. Fairness-aware unsupervised feature selection. In CIKM (2021).
- [257] Xue, B., and Zou, L. Knowledge graph quality management: a comprehensive survey. IEEE Transactions on Knowledge and Data Engineering (2022).
- [258] Yan, K., and Zhang, D. Feature selection and analysis on correlated gas sensor data with recursive feature elimination. Sensors and Actuators B: Chemical 212 (2015), 353-363.
- [259] Yang, Y., and Loog, M. A benchmark and comparison of active learning for logistic regression. Pattern Recognition 83 (2018), 401-415.
- [260] Ying, X. An overview of overfitting and its solutions. Journal of physics: Conference series 1168 (2019), 022022.
- [261] Yoo, J., Ahn, N., and Sohn, K.-A. Rethinking data augmentation for image super-resolution: A comprehensive analysis and a new strategy. In CVPR (2020).
- [262] Yoo, J. Y., Morris, J. X., Lifland, E., and Qi, Y. Searching for a search method: Benchmarking search algorithms for generating nlp adversarial examples. arXiv preprint arXiv:2009.06368 (2020).
- [263] Yoo, K. M., Park, D., Kang, J., Lee, S.-W., and Park, W. Gpt3mix: Leveraging large-scale language models for text augmentation. In EMNLP (2021).
- [264] Yuan, W., Neubig, G., and Liu, P. Bartscore: Evaluating generated text as text generation. In NeurIPS (2021).
- [265] Yuen, M.-C., King, I., and Leung, K.-S. A survey of crowdsourcing systems. In PASSAT (2011).
- [266] Zaharia, M., Xin, R. S., Wendell, P., Das, T., Armbrust, M., Dave, A., Meng, X., Rosen, J., Venkataraman, S.,

Franklin, M. J., Ghodsi, A., Gonzalez, J., Shenker, S., and Stoica, I. Apache Spark: A unified engine for big data processing. Communications of the ACM 59 (2016).

- [267] Zeng, H., Henry, S. C., and Riola, J. P. Stratal slicing, part ii: Real 3-d seismic data. Geophysics 63, 2 (1998), 514-522.
- [268] Zeng, Z., Moh, P., Du, F., Hoffswell, J., Lee, T. Y., Malik, S., Koh, E., and Battle, L. An evaluation-focused framework for visualization recommendation algorithms. IEEE Transactions on Visualization and Computer Graphics 28, 1 (2021), 346-356.
- [269] Zha, D., Bhat, Z. P., Lai, K.-H., Yang, F., and Hu, X. Data-centric ai: Perspectives and challenges. arXiv preprint arXiv:2301.04819 (2023).
- [270] Zha, D., Feng, L., Bhushanam, B., Choudhary, D., Nie, J., Tian, Y., Chae, J., Ma, Y., Kejariwal, A., and Hu, X. Autoshard: Automated embedding table sharding for recommender systems. In KDD (2022).
- [271] Zha, D., Feng, L., Tan, Q., Liu, Z., Lai, K.-H., Bhushanam, B., Tian, Y., Kejariwal, A., and Hu, X. Dreamshard: Generalizable embedding table placement for recommender systems. In NeurIPS (2022).
- [272] Zha, D., Lai, K.-H., Huang, S., Cao, Y., Reddy, K., Vargas, J., Nguyen, A., Wei, R., Guo, J., and Hu, X. Rlcard: a platform for reinforcement learning in card games. In IJCAI (2021).
- [273] Zha, D., Lai, K.-H., Tan, Q., Ding, S., Zou, N., and Hu, X. B. Towards automated imbalanced learning with deep hierarchical reinforcement learning. In CIKM (2022).
- [274] Zha, D., Lai, K.-H., Wan, M., and Hu, X. Meta-aad: Active anomaly detection with deep reinforcement learning. In ICDM (2020).
- [275] Zha, D., Lai, K.-H., Zhou, K., and Hu, X. Experience replay optimization. In IJCAI (2019).
- [276] Zha, D., Lai, K.-H., Zhou, K., and Hu, X. Simplifying deep reinforcement learning via self-supervision. arXiv preprint arXiv:2106.05526 (2021).
- [277] Zha, D., Lai, K.-H., Zhou, K., and Hu, X. Towards similarity-aware time-series classification. In SDM (2022).
- [278] Zha, D., and Li, C. Multi-label dataless text classification with topic modeling. Knowledge and Information Systems 61 (2019), 137-160.
- [279] Zha, D., Ma, W., Yuan, L., Hu, X., and Liu, J. Rank the episodes: A simple approach for exploration in procedurallygenerated environments. In ICLR (2021).
- [280] Zha, D., Pervaiz Bhat, Z., Chen, Y.-W., Wang, Y., Ding, S., Jain, A. K., Qazim Bhat, M., Lai, K.-H., Chen, J., et al. Autovideo: An automated video action recognition system. In IJCAI (2022).
- [281] Zha, D., Xie, J., Ma, W., Zhang, S., Lian, X., Hu, X., and Liu, J. Douzero: Mastering doudizhu with self-play deep reinforcement learning. In ICML (2021).
- [282] Zhang, H., Cisse, M., Dauphin, Y. N., and Lopez-Paz, D. mixup: Beyond empirical risk minimization. In ICLR (2018).
- [283] Zhang, H., Goodfellow, I., Metaxas, D., and Odena, A. Self-attention generative adversarial networks. In IICML (2019).
- [284] Zhang, J., Hsieh, C.-Y., Yu, Y., Zhang, C., and Ratner, A. A survey on programmatic weak supervision. arXiv preprint arXiv:2202.05433 (2022).
- [285] Zhang, S., Yao, L., Sun, A., and Tay, Y. Deep learning based recommender system: A survey and new perspectives. ACM computing surveys (CSUR) 52, 1 (2019), 1-38.
- [286] Zhang, X., Chang, Z., Li, Y., Wu, H., Tan, J., Li, F., and Cui, B. Facilitating database tuning with hyper-parameter optimization: a comprehensive experimental evaluation. In VLDB (2022).
- [287] Zhang, X., Mei, C., Chen, D., Yang, Y., and Li, J. Active incremental feature selection using a fuzzy-rough-set-based information entropy. IEEE Transactions on Fuzzy Systems 28, 5 (2019), 901-915.
- [288] Zhang, X., Zhao, J., and LeCun, Y. Character-level convolutional networks for text classification. In NeurIPS (2015).
- [289] Zhang, Z. Missing data imputation: focusing on single imputation. Annals of translational medicine 4, 1 (2016).
- [290] Zhou, J., Cui, G., Hu, S., Zhang, Z., Yang, C., Liu, Z., Wang, L., Li, C., and Sun, M. Graph neural networks: A review of methods and applications. AI open 1 (2020), 57-81.
- [291] Zhou, K., Huang, X., Li, Y., Zha, D., Chen, R., and Hu, X. Towards deeper graph neural networks with differentiable group normalization. In NeurIPS (2020).
- [292] Zhou, K., Huang, X., Zha, D., Chen, R., Li, L., Choi, S.-H., and Hu, X. Dirichlet energy constrained learning for deep graph neural networks. In NeurIPS (2021).
- [293] Zhou, K., Song, Q., Huang, X., Zha, D., Zou, N., and Hu, X. Multi-channel graph neural networks. In IJCAI (2021).
- [294] Zhou, X., Jin, L., Sun, J., Zhao, X., Yu, X., Feng, J., Li, S., Wang, T., Li, K., and Liu, L. Dbmind: A self-driving platform in opengauss. In VLDB (2021).
- [295] Zhou, Y., and Goldman, S. Democratic co-learning. In ICTAI (2004).
- [296] Zhu, Y., Kiros, R., Zemel, R., Salakhutdinov, R., Urtasun, R., Torralba, A., and Fidler, S. Aligning books and movies: Towards story-like visual explanations by watching movies and reading books. In CVPR (2015).
- [297] Zöller, M.-A., and Huber, M. F. Benchmark and survey of automated machine learning frameworks. Journal of artificial intelligence research 70 (2021), 409-472.

[298] Zoph, B., Ghiasi, G., Lin, T.-Y., Cui, Y., Liu, H., Cubuk, E. D., and Le, Q. Rethinking pre-training and self-training. In NeurIPS (2020).