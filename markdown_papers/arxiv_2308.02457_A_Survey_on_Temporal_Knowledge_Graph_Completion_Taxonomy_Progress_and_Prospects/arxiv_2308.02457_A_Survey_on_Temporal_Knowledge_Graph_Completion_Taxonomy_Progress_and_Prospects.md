---
cite_key: "typically2009"
title: "A Survey on Temporal Knowledge Graph Completion: Taxonomy, Progress, and Prospects"
authors: "Typically, the facts in KGs are time-specific and are valid"
year: 2009
date_processed: "2025-07-02"
phase2_processed: true
original_folder: "arxiv_2308.02457_A_Survey_on_Temporal_Knowledge_Graph_Completion_Taxonomy_Progress_and_Prospects"
images_total: 12
images_kept: 12
images_removed: 0
---

# A Survey on Temporal Knowledge Graph Completion: Taxonomy, Progress, and Prospects

Jiapu Wang, Boyue Wang, Meikang Qiu, *Senior Member, IEEE*, Shirui Pan, *Senior Member, IEEE*, Bo Xiong, Heng Liu, Linhao Luo, Tengfei Liu, Yongli Hu, Baocai Yin, Wen Gao, *Fellow, IEEE*

**Abstract**—Temporal characteristics are prominently evident in a substantial volume of knowledge, which underscores the pivotal role of *Temporal Knowledge Graphs (TKGs)*in both academia and industry. However, TKGs often suffer from incompleteness for three main reasons: the continuous emergence of new knowledge, the weakness of the algorithm for extracting structured information from unstructured data, and the lack of information in the source dataset. Thus, the task of*Temporal Knowledge Graph Completion (TKGC)*has attracted increasing attention, aiming to predict missing items based on the available information. In this paper, we provide a comprehensive review of TKGC methods and their details. Specifically, this paper mainly consists of three components, namely,*1) Background,*which covers the preliminaries of TKGC methods, loss functions required for training, as well as the dataset and evaluation protocol;*2) Interpolation,*that estimates and predicts the missing elements or set of elements through the relevant available information. It further categorizes related TKGC methods based on how to process temporal information;*3) Extrapolation,*which typically focuses on continuous TKGs and predicts future events, and then classifies all extrapolation methods based on the algorithms they utilize. We further pinpoint the challenges and discuss future research directions of TKGC.

✦
**Index Terms**—Knowledge Graphs, Temporal Knowledge Graphs, Knowledge Graph Completion, Interpolation, Extrapolation.

# 1 INTRODUCTION

K NOWLEDGE Graph (KGs) are structured multirelational knowledge bases that typically contain a set of facts. Each fact in a KG is stored in the form of triplet (s, r, o), where s and o represent the head and tail entities, respectively, and r denotes the relation connecting the head entity and the tail entity. For example, given one triplet *(Barack Hussein Obama, President of, USA)*, "*Barack Hussein Obama*" and "*USA*" are the head entity s and the tail entity o, respectively, while "*president of*" represents the relation r. Currently, large-scale KGs are widely exploited in artificial intelligence and data mining applications, including trafficflow forecasting [\[1\]](#page-16-0), information retrieval [\[2\]](#page-16-1), and dialogue systems [\[3\]](#page-16-2).

Typically, the facts in KGs are time-specific and are valid

-*Jiapu Wang, Boyue Wang, Heng Liu, Tengfei Liu, Yongli Hu and Baocai Yin are with Beijing Municipal Key Lab of Multimedia and Intelligent Software Technology, Beijing Artificial Intelligence Institute, Faculty of Information Technology, Beijing University of Technology, Beijing 100124, China. Email:* {*jpwang, liuheng, tfliu*}*@emails.bjut.edu.cn,* {*wby, huyongli, ybc*}*@bjut.edu.cn.*-*Meikang Qiu is with the Beacom College of Computer and Cyber Sciences, Dakota State University, Madison, South Dakota, USA. Email: qiumeikang@ieee.org*-*Shirui Pan is with the School of Information and Communication Technology and Institute for Integrated and Intelligent Systems (IIIS), Griffith University, Queensland, Australia. Email: s.pan@griffith.edu.au.*-*Bo Xiong is with the Department of Computer Science, University of Stuttgart, 70569 Stuttgart, Germany. E-mail: bo.xiong@ipvs.unistuttgart.de.*-*Linhao Luo is with the Department of Data Science and AI, Monash University, Melbourne, Australia. E-mail: linhao.luo@monash.edu.*-*Wen Gao is with the Institute of Digital Media, Peking University, Beijing 100871, China and also with the School of Electronic and Computer Engineering, Peking University Shenzhen Graduate School, Shenzhen 518055, China. E-mail: wgao@pku.edu.cn.*-*Jiapu Wang and Boyue Wang contributed equally to this work.*-*Corresponding author: Shirui Pan.*only within a particular period, rendering knowledge timelimited. For example, the triplet*(Barack Hussein Obama, President of, USA)*is only valid during the period*[2009, 2017]*. Consequently, KGs that contain temporal labels form *Temporal Knowledge Graphs (TKG)*and have gained significant attention in recent years. The fundamental unit of a TKG is a quadruplet (s, r, o, t) formed by introducing the temporal information alongside the triplet. For example, the quadruplet can be represented as*(Barack Hussein Obama, President of, USA, [2009, 2017])*. As events continually evolve, TKGs can be regularly updated to capture the dynamic changes in the real world.

TKGs (*e.g.,*ICEWS [\[4\]](#page-16-3) and GDELT [\[5\]](#page-16-4)) can contain millions or even billions of quadruplets. However, despite their vastness, these TKGs remain incomplete for three primary reasons. Firstly, the source datasets often lack comprehensive information. Secondly, the algorithms used to extract entities and relations face challenges when dealing with diverse forms of unstructured data, rendering them less effective. Lastly, knowledge continuously evolves due to the ongoing events in nature. The incompleteness of the knowledge graph significantly hampers the effectiveness of knowledge-driven systems, thereby emphasizing the significance of*Temporal Knowledge Graph Completion (TKGC)*as a crucial task.

The TKGC task aims to predict the missing items according to the available information, e.g.,*(Donald Trump, succeeded, Barack Hussein Obama, 2017)*can be inferred from existing quadruplets*(Barack Hussein Obama, President of, USA, [2009, 2017])*and*(Donald Trump, President of, USA, [2017, 2021])*. Specifically, following the strategy whether forecasting future facts, we categorize existing TKGC literature into the *interpolation methods*and the*extrapolation methods*. More specifically, interpolation methods typically

<span id="page-1-3"></span>![](_page_1_Figure_1.jpeg)

<span id="page-1-0"></span>Fig. 1. Two categorizations of the *Temporal Knowledge Graph Completion (TKGC)*, e.g., (a) Interpolation, in which the red bolded "**?**" represents the missing knowledge*(Donald Trump, succeeded, Barack Hussein Obama, 2017)*; (b) Extrapolation, in which Gt denotes the static KG at time t.

estimate unknown knowledge through the relevant known facts, and extrapolation methods aim to estimate unknown knowledge in the future. Fig [1](#page-1-0) illustrates an example of these two different scenarios.

Each type of TKGC method faces specific important challenges that need to be addressed. When it comes to interpolation methods, two significant challenges arise: how to effectively incorporate temporal information into the evolution process of KGs and how to handle the timestamps to make full exploitation of its semantic information. Although some TKGC methods are designed to explore the semantics of temporal information, they often treat temporal information independently and fail to capture the hidden semantic information associated with the facts. Moreover, existing TKGC methods simply associate temporal information with the facts, which is challenging to reflect on the evolution process. On the other hand, extrapolation methods face the challenge of effectively mitigating the impact of anomalous historical information on TKG embedding. These methods explore the structural and temporal information among historical snapshots to further help predict future events. However, the presence of anomalous historical information severely hampers the accurate prediction of future events.

In response to these challenges, there have been increasing studies emerging recently. For instance, Ma *et al.*[\[6\]](#page-16-5) employed bag-of-words and Bi-LSTM algorithms to fully explore the latent semantics of temporal information. Goel*et al.*[\[7\]](#page-16-6) presented an approach called DE-SimplE, which incorporates a diachronic embedding function to integrate temporal information into facts. This approach effectively captures the evolution process of KGs, allowing for more accurate predictions. However, it is crucial to recognize that there are still unresolved issues that require attention and should be prioritized. To facilitate further progress in the field, it becomes imperative to provide a comprehensive summary and comparison of existing TKGC methods.

In this paper, we provide an overview of TKGC methods with a fine-grained categorization. We also summarize the benchmark datasets commonly used for the evaluation of TKGC methods and present the evaluation protocol. Furthermore, we analyze the challenges in the filed and discuss the future directions for this rapidly emerging topic. By conducting this comprehensive analysis, we aim to contribute to the advancement of TKGC research and provide insights <span id="page-1-4"></span>for researchers and practitioners. Our main contributions are summarized as follows:

- 1)**Comprehensive survey.**We conduct a systematic summary of all TKGC literature, with a particular focus on the most recent studies. Furthermore, we detail each TKGC method, make essential comparisons, and summarize the techniques and codes[1](#page-1-1) used.
- 2)**Categorization and new taxonomies.**We provide a comprehensive summary and a fine-grained categorization of TKGCs. At the high level, we classify the current TKGC literature into two categories according to whether they forecast future events: the interpolation and the extrapolation methods. For interpolation methods, we divide them according to how to process temporal information. For the extrapolation methods, we classify them based on the algorithms they utilize.
- 3)**Future directions.**We pinpoint future research directions of this fast-growing field, providing guidelines and suggestions on TKGC.

The rest of this paper is organized as follows. Section [2](#page-1-2) briefly reviews the background of TKGC. Section [3](#page-3-0) details an overview and the categorization of TKGCs. In Section [4,](#page-4-0) we introduce the interpolation methods and classify in detail the interpolation methods. Likewise, Section [5](#page-8-0) presents the extrapolation methods. Afterwards, we discuss the applications of TKG in recommendation and Q&A systems in Section [6.](#page-13-0) Section [7](#page-15-0) discusses the challenges and future research directions. Finally, we conclude this paper in Section [8.](#page-16-7)

# <span id="page-1-2"></span>2 BACKGROUND

In this section, we describe the background of the*Temporal Knowledge Graph Completion (TKGC)*, including *Preliminaries*, *Loss functions*, *Benchmark datasets*, and *Evaluation protocol*.

## 2.1 Preliminaries

*Temporal Knowledge Graphs (TKGs)*are structured knowledge bases consisting of time-specific knowledge. Specifically, the TKG can be denoted as G = {Q | E, R, T }, and

<span id="page-1-1"></span>1. https://github.com/jiapuwang/Awesome-TKGC

TABLE 1 Statistic information of whole datasets.

<span id="page-2-0"></span>

| Datasets        | #Entities | #Relations | #Timestamps | #Time Span              | #Training | #Validation | #Test   | #Granularity | #Category     |
|-----------------|-----------|------------|-------------|-------------------------|-----------|-------------|---------|--------------|---------------|
| ICEWS14 [8]     | 6,869     | 230        | 365         | 01/01/2014 – 12/31/2014 | 72,826    | 8,941       | 8,963   | 24 hours     | Interpolation |
| ICEWS05-15 [8]  | 10,094    | 251        | 4,017       | 01/01/2005 – 12/31/2015 | 368,962   | 46,275      | 46,092  | 24 hours     | Interpolation |
| GDELT [5]       | 500       | 20         | 366         | 04/01/2015 – 03/31/2016 | 2,735,685 | 341,961     | 341,961 | 24 hours     | Interpolation |
| YAGO11k [9]     | 10,623    | 10         | 70          | -431 – 2844             | 16,406    | 2,050       | 2,051   | –            | Interpolation |
| YAGO15k [8]     | 15,403    | 34         | 198         | 1553 – 2017             | 29,381    | 3,635       | 3,685   | –            | Interpolation |
| Wikidata12k [9] | 12,554    | 24         | 81          | 1709 – 2018             | 32,497    | 4,062       | 4,062   | –            | Interpolation |
| ICEWS14 [8]     | 6,869     | 230        | 365         | 01/01/2014 – 12/31/2014 | 72,826    | 8,941       | 8,963   | 24 hours     | Extrapolation |
| ICEWS18 [10]    | 23,033    | 256        | 304         | 01/01/2018 – 10/31/2018 | 373,018   | 45,995      | 49,545  | 24 hours     | Extrapolation |
| GDELT [5]       | 7,691     | 240        | 2,751       | 01/01/2018 – 01/31/2018 | 1,734,399 | 238,765     | 305,241 | 15 mins      | Extrapolation |
| WIKI [11]       | 12,554    | 24         | 232         | 1786 – 2018             | 539,286   | 67,538      | 63,110  | 1 year       | Extrapolation |
| YAGO [12]       | 10,623    | 10         | 189         | 1830 – 2019             | 161,540   | 19,523      | 20,026  | 1 year       | Extrapolation |

these symbols E, R, T , Q respectively represent the entity, relation, timestamp and quadruplet sets. More specifically, each knowledge in TKGs is stored in the form of quadruplet (s, r, o, t) ∈ Q, where s, o ∈ E are the head and tail entities, r ∈ R denotes the relation and t ∈ T means the timestamp. Furthermore, s and o represent the nodes of the TKG, r denotes the edge from the head entity to the tail entity and t is the temporal label, which mainly contains two forms, such as the time point or the time interval.

### 2.2 Loss Functions

Due to the incompleteness of TKGs, TKGC has become increasingly urgent. Specifically, in the TKGC task, the score function, denoted as g(x), is introduced to evaluate or predict the credibility or probability of the quadruplet. Furthermore, the loss function L is designed to minimize the score function. Additionally, in order to enhance the efficiency of model training, negative sampling [\[13\]](#page-16-13) is incorporated into the TKGC task, whereby quadruplets are uniformly sampled from the entire set of possible quadruplets. In specific, we summarize two commonly-used loss functions and three temporal regularizations in the TKGC task.
**Margin-based ranking loss**L<sup>m</sup> [\[11\]](#page-16-11), [\[14\]](#page-16-14), [\[15\]](#page-16-15) introduces the margin to ensure that the score of the true quadruplet is lower than that of the corrupted quadruplet,

$$
\mathcal{L}_m = \sum_{(\mathbf{s}, \mathbf{r}, \mathbf{o}, \mathbf{t}) \in \mathcal{Q}} [\lambda + g(\mathbf{s}, \mathbf{r}, \mathbf{o}, \mathbf{t}) - \sum_{\mathbf{o'} \in \mathcal{E}} g(\mathbf{s}, \mathbf{r}, \mathbf{o'}, \mathbf{t})]_+, (1)
$$

where [x]<sup>+</sup> = max(x, 0) and λ > 0 is a margin hyperparameter. However, the margin-based ranking loss is sensitive to outliers.
**Cross-entropy loss**L<sup>c</sup> [\[16\]](#page-16-16) calculates the difference between two probability distributions, accurately reflecting the prediction accuracy of the model while being less sensitive to outliers. In TKGC task, we follow the standard data augmentation protocol [\[17\]](#page-16-17) and add inverse relations to the datasets, i.e., creating one quadruplet (o, r −1 , s, t) for each quadruplet (s, r, o, t). Afterwards, the cross-entropy loss can be defined as follows,

$$
\mathcal{L}_c = -\log\left(\frac{\exp(f(\mathbf{s}, \mathbf{r}, \mathbf{o}, \mathbf{t}))}{\sum_{\mathbf{s}' \in \mathcal{E}} \exp(f(\mathbf{s}', \mathbf{r}, \mathbf{o}, \mathbf{t}))}\right) \n- \log\left(\frac{\exp(f(\mathbf{o}, \mathbf{r}^{-1}, \mathbf{s}, \mathbf{t}))}{\sum_{\mathbf{o'} \in \mathcal{E}} \exp(f(\mathbf{o'}, \mathbf{r}^{-1}, \mathbf{s}, \mathbf{t}))}\right).
$$
\n(2)

Finally, we summarize three classical temporal regularizations L<sup>τ</sup> widely used for ensuring facts behave smoothly over time in TKG. TComplEx [\[18\]](#page-16-18) first proposes the nuclear 3-norm [\[19\]](#page-16-19) temporal regularization in the TKGC task, which expects corresponding elements of neighboring temporal embeddings to be close. The temporal regularization can be denoted as follows,

$$
\mathcal{L}_{\tau} = \frac{1}{|\mathcal{T}| - 1} \sum_{i=1}^{|\mathcal{T}| - 1} \|\mathbf{t}_{i+1} - \mathbf{t}_{i}\|_{3}^{3},
$$
(3)

where |T | is the number of timestamps and t<sup>i</sup> denotes the i-th timestamp. Based on TComplEx, TeLM [\[19\]](#page-16-19) imposes a bias component into the temporal regularization, enhancing flexibility and expressiveness. Mathematically, this can be represented as follows,

$$
\mathcal{L}_{\tau} = \frac{1}{|\mathcal{T}| - 1} \sum_{i=1}^{|\mathcal{T}| - 1} \|\mathbf{t}_{i+1} - \mathbf{t}_i + \mathbf{t}_b\|_3^3, \tag{4}
$$

where t<sup>b</sup> denotes the bias term and is randomly initialized.

However, the aforementioned temporal regularizations primarily emphasize the absolute distance between corresponding elements, thereby restricting the flexibility of neighboring temporal embeddings to a significant extent. QDN [\[20\]](#page-16-20) proposes a cosine similarity-based temporal regularization, which measures the global similarity between neighboring temporal embeddings,

$$
\mathcal{L}_{\tau} = -\frac{1}{|\mathcal{T}| - 1} \sum_{i=1}^{|\mathcal{T}| - 1} (\mathbf{t}_{i+1}^T \cdot \mathbf{t}_i).
$$
 (5)

#### 2.3 Benchmark Datasets

We list eleven common datasets widely used in the TKGC task and the major statistics of these datasets are

![](_page_3_Figure_1.jpeg)

<span id="page-3-1"></span>Fig. 2. Fine-grained categorization of*Temporal Knowledge Graph Completion (TKGC)*methods.

summarized in TABLE [1](#page-2-0) [\[21\]](#page-16-21).**ICEWS14**, **ICEWS05-15**[\[8\]](#page-16-8) and**ICEWS18**[\[10\]](#page-16-10) are three subsets of*Integrated Crisis Early Warning System (ICEWS)*[\[4\]](#page-16-3), which involves some political events with time points.**GDELT**[\[5\]](#page-16-4) is a subset of the larger*Global Database of Events, Language, and Tone (GDELT)*[\[5\]](#page-16-4) that contains human social relationships, and timestamps are mainly in the form of time points. It should be emphasized that GDELT exhibits a complex geometry characterized by a small number of nodes and a substantial volume of training data.
**YAGO11k**[\[9\]](#page-16-9),**YAGO15k**[\[8\]](#page-16-8) and**YAGO**[\[12\]](#page-16-12) are three subsets of YAGO3 [\[12\]](#page-16-12).**Wikidata12k**[\[9\]](#page-16-9) and**WIKI**[\[11\]](#page-16-11) are two subsets of WIKIDATA [\[22\]](#page-16-22). Different from ICEWS and GDELT, time annotations in YAGO11k and Wikidata12k are represented in various forms, i.e., time points like 2015−12−12, time intervals like "Since 2015 ([2015, ##])" and [2015, 2016]. Unlike ICEWS and GDELT, YAGO3 and WIKIDATA have a more sparse graph structure.

## 2.4 Evaluation Protocol

The evaluation protocol serves as a crucial metric for assessing the performance of TKGC methods. Typically, it involves replacing either the head or tail entity in each test quadruplet (s, r, o, t) with all possible entities in the TKG, and subsequently ranking the scores produced by the scoring function. Some widely used evaluation metrics include Mean Rank (MR), Mean Reciprocal Rank (MRR) and Hit@N.

-**Mean Rank (MR)**: the average rank assigned to the true quadruplet overall test quadruplets;
- **Mean Reciprocal Rank (MRR)**: the average of the reciprocal rank assigned to the true quadruplet overall test quadruplets;

• **Hit@**N: the percentage of cases in which the true quadruplet appears in the top N ranked quadruplets. Here, we specifically report the N = 1, 3, 10 scores to verify the performance of TKGC methods.

Higher values of MRR and Hits@N, as well as lower MR, indicate better performance. In addition, the final experimental results consist of two flavors: *Raw*and*Filter*. Specifically, the *Filter*metric is calculated by excluding all reconstituted quadruplets that existed in the training, validation, or test set from the rank, whereas the*Raw*metric does not consider such exclusions. A more extensive description of these metrics can be found in [\[23\]](#page-16-23), [\[24\]](#page-16-24).

# <span id="page-3-0"></span>3 TEMPORAL KNOWLEDGE GRAPH COMPLETION

In this section, we categorize them into two flavors based on whether they forecast future events, including*Interpolation-based TKGCs*(Fig. [1a\)](#page-1-3) and*Extrapolation-based TKGCs*(Fig. [1b\)](#page-1-4). The further fine-grained sub-categories are illustrated in Fig. [2.](#page-3-1)

## 3.1 Interpolation-based TKGCs

Interpolation [\[25\]](#page-16-25), [\[26\]](#page-16-26) is a statistical method that use the relevant known values to estimate an unknown value or set. By identifying the consistent trend within a dataset, it becomes possible to reasonably estimate values that have not been explicitly calculated.

Interpolation-based TKGC methods generally complete the missing item by analyzing the known knowledge in TKGs. We categorize them based on how they process temporal information as follows,

1)*Timestamps dependent-based TKGC methods*do not impose operations on timestamps.

- 2)*Timestamps-specific functions-based TKGC methods*apply the timestamps-specific functions to obtain embeddings of timestamps or the evolution of entities and relations.
- 3)*Deep learning-based TKGC methods*utilize deep learning algorithms to encode temporal information and investigate the dynamic evolution of entities and relations.

### 3.2 Extrapolation-based TKGCs

Extrapolation [\[27\]](#page-16-27), [\[28\]](#page-16-28) focuses on forecasting the 'future' unknown values beyond the data that is currently accessible.

Extrapolation-based TKGC methods focus on continuous TKGs, enabling predictions of future events by learning embeddings of entities and relations from historical snapshots. We categorize them according to the algorithms they utilize as follows,

- 1)*Rule-based TKGC methods*apply the logical rules to reason future events.
- 2)*Graph neural network-based TKGC methods*generally utilize GNN and RNN to explore the structural and temporal information in TKG.
- 3)*Meta learning-based TKGC methods*design the metalearner to instruct the learning process of the model.
- 4)*Reinforcement learning-based TKGC methods*introduce the reinforcement learning strategy to ensure that the model achieves its training goals better.

In the following sections (Section [4](#page-4-0) and Section [5\)](#page-8-0), we will introduce these TKGC categorizations in detail.

# <span id="page-4-0"></span>4 INTERPOLATION-BASED TKGCS

In this section, we provide an overview of the interpolation methods from three aspects:*Timestamps dependent-based TKGC methods*, *Timestamps-specific functions-based TKGC methods*and*Deep learning-based TKGC methods*.

## 4.1 Timestamps Dependent-based TKGCs

Timestamps dependent-based TKGC methods typically do not perform operations on timestamps. Instead, they simply associate the timestamp with the corresponding entity or relation to accomplish the evolution of entities or relations. As shown in Fig. [3,](#page-4-1) given a query *(Barack Hussein Obama, President of, ?, [2009 - 2017])*, timestamps dependent-based TKGC methods generally associate the timestamp *[2009 - 2017]*with the entity*Barack Hussein Obama*and relation*President of*to achieve the evolution process. Finally, they complete the missing item*USA*using*Static Knowledge Graph Completion (SKGC)*methods.
**TuckERTNT**[\[29\]](#page-16-29) is a classic timestamps dependentbased TKGC method that expands upon TuckER [\[30\]](#page-16-30). TuckER is modeled based on the triplet (s, r, o) and incorporates a 3rd-order tensor to facilitate the link prediction task. Here, TuckER explores the Tucker decomposition algorithm to overcome the over-parameterization problem. The score function of TuckER is defined as,

$$
g(\mathbf{s}, \mathbf{r}, \mathbf{o}) = \mathcal{W} \times_1 \mathbf{s} \times_2 \mathbf{r} \times_3 \mathbf{o},
$$

$$
\mathcal{W} = \mathcal{Z} \times_1 \mathbf{A} \times_2 \mathbf{B} \times_3 \mathbf{C},
$$
 (6)

![](_page_4_Figure_17.jpeg)

<span id="page-4-1"></span>Fig. 3. The framework of the timestamps dependent-based TKGCs.

where W denotes the 3rd-order tensor, which can be decomposed as a core tensor Z and three factor matrices A, B and C; ×<sup>i</sup> represents the tensor multiplication between the core tensor and factor matrix in i-th dimension; g(s, r, o) is the score function. TuckERTNT is an extension of TuckER by introducing timestamps. Moreover, TuckERTNT takes into account the notion that certain facts may vary with respect to time, while others remain independent of time. It defines its score function as,

$$
g(\mathbf{s}, \mathbf{r}, \mathbf{o}, \mathbf{t}) = \mathcal{W} \times_1 \mathbf{s} \times_2 (\mathbf{r} \circ \mathbf{t} + \mathbf{r}) \times_3 \mathbf{o}, \quad (7)
$$

where ◦ denotes the Hadamard (or element-wise) product.
**TTransE**[\[11\]](#page-16-11) extends the classic TransE by introducing the joint encoding of relations and timestamps within the same space.Based on TTransE,**ST-TransE**[\[31\]](#page-16-31) further proposes a specific time embedding method to constrain the representation learning of entities and relations. Both TTransE and ST-TransE struggle to effectively handle facts that undergo temporal evolution.**T-SimplE**[\[32\]](#page-16-32) introduces the 4th-order tensor to capture the associativity among the elements of the quadruplet. Likewise,**He** *et al.*[\[33\]](#page-16-33) introduce*Canonical Polyadic (CP)*decomposition into the TKGC task, and incorporate both temporal and non-temporal relations to model temporal facts (change over time) and non-temporal facts (not change over time). In particular, T-SimplE ignores the evolving strength of representations of pairwise relations in the same relational chain over time, as well as the revision of candidate prediction. Thus,**TKGFrame**[\[34\]](#page-16-34) proposes a relation evolving enhanced model, which obtains more accurate TKG embeddings by learning a new temporal evolving matrix. Meanwhile, TKGFrame introduces a refinement model to revise the candidate predictions. To further capture the semantic property between relation and its involved entities at various time steps,**Li** *et al.*[\[35\]](#page-16-35) design several regularizations to constrain the expression of TKG. Recently,**TBDRI**[\[36\]](#page-16-36) takes inverse relations as one of the most important types of relations. It independently learns inverse relations through block decomposition based on relational interaction.

## 4.2 Timestamps-specific Functions-based TKGCs

Timestamps-specific functions-based TKGC methods exploit the specific functions to learn the embeddings of timestamps or the evolution of entities and relations, such as diachronic embedding functions [\[7\]](#page-16-6), Gaussian functions [\[37\]](#page-16-37) and transformation functions [\[38\]](#page-16-38).

###*4.2.1 Transformation Functions*Transformation functions-based TKGC methods encode timestamps via the transformation functions. Some classic methods are proposed, such as**BoxTE**[\[39\]](#page-16-39),**SPLIME**[\[40\]](#page-16-40) and**TARGCN**[\[41\]](#page-16-41).
**Jiang** *et al.*[\[15\]](#page-16-15) first propose a time-aware TKGC method to comprehensively capture the temporal nature of facts. Specifically, they respectively utilize the time-aware embedding model and*Integer Linear Programming (ILP)*to encode temporal order information and temporal consistency information. However, this method has room for improvement in terms of effectively leveraging temporal information.**HTTR**[\[38\]](#page-16-38) introduces the Householder transformation [\[42\]](#page-17-0) to explore the temporal evolution of relations. Specifically, HTTR defines the orthogonal matrix that represents the rotation from the head entity to the tail entity. This orthogonal matrix is obtained through the Householder transformation, and it directly links to the fused information of the relation and the temporal aspects.
**BoxTE**[\[39\]](#page-16-39) extends from the SKGC model BoxE [\[43\]](#page-17-1). BoxE encodes entities as points and represents relations as a set of boxes to enable the flexible representation of fundamental logical properties. Additionally, BoxTE embeds temporal information via the relation-specific transfer matrix to explore rich inference patterns.**Dai** *et al.*[\[44\]](#page-17-2) propose a model-agnostic method on the basis of BoxTE, in which they initially introduce the generative adversarial learning technique into the TKGC task. Specifically, the generator constructs high-quality plausible quadruplets and the discriminator obtains the embeddings of entities and relations based on the generator. To overcome the problem of vanishing gradients on discrete data, Dai*et al.*simultaneously introduce the Wasserstein distance and Gumbel-Softmax relaxation.
**SPLIME**[\[40\]](#page-16-40) is essentially a transformation function, which applies*splitting*and*merging*operations to model TKGs through SKGC methods (e.g., McRL [\[45\]](#page-17-3) and BoxE [\[43\]](#page-17-1)). However, a substantial number of parameters introduced in SPLIME lead to large memory consumption and limit the running efficiency.**Ding** *et al.*[\[41\]](#page-16-41) put forward**TARGCN** *(Time-Aware Relational Graph Convolutional Network)*, a time-aware relational graph encoder designed for the TKGC task. It can achieve greater expressiveness with a smaller number of parameters. TARGCN explores the temporal context of each entity to learn entity embeddings and models temporal differences to encode temporal information through a functional temporal encoder. **TASTER**[\[46\]](#page-17-4) explores the evolution process of entities via a sparse transformation matrix and simultaneously models the local information in a specific timestamp and global information. Subsequently, TASTER respectively models entity association and evolution to overcome scalability limitations.**Time-LowFER**[\[47\]](#page-17-5) proposes a cycle-aware time-encoding function to decompose the timestamp into four important components including*year*, *month*, *week*and*day*, so as to better encode the timestamp. Afterwards, Time-LowFER models the association of TKG through LowFER [\[48\]](#page-17-6), which

![](_page_5_Figure_7.jpeg)

<span id="page-5-0"></span>Fig. 4. The framework of the complex embedding functions-based TKGCs.

introduces a low-rank tensor decomposition mechanism to facilitate the interaction between entities and relations.

Moreover, special transformation functions, i.e., diachronic embedding functions, can encode timestamps or associate timestamps with entities and relations more efficiently [\[7\]](#page-16-6), [\[49\]](#page-17-7). **Goel** *et al.*[\[7\]](#page-16-6) first propose a general diachronic embedding function (such as DE-SimplE and DE-DistMult), which is model-independent and can be combined with any SKGC method. The diachronic embedding function can obtain the entity representation at any timestamp. Although DE-SimplE is capable of capturing temporal information of TKGs, it is insufficient to exploit the complex structure of the graph and its entity modeling is not comprehensive enough.**DEGAT**[\[49\]](#page-17-7) exploits the*Graph ATtention network (GAT)*to capture the complex graph structure and introduces the diachronic embedding function to model the association of the entity and timestamp.

##*4.2.2 Complex Embedding Functions*Complex embedding functions-based TKGC methods typically embed TKGs into complex spaces or special coordinate systems to capture various relational patterns, such as symmetry (e.g., spouse), antisymmetry (e.g., predecessor), inversion (e.g., hypernym and hyponym) and composition (e.g., my son's mother is my wife) [\[50\]](#page-17-8), [\[51\]](#page-17-9), [\[52\]](#page-17-10), and semantic information. As shown in Fig. [4,](#page-5-0) the quadruplet*(Barack Hussein Obama, President of, USA, [2009 - 2017])*is converted into the triplet by associating timestamps with entities or relations in complex space or polar/spherical coordinate system, and then the missing item can be predicted through SKGC methods.
**ChronoR**[\[16\]](#page-16-16) is an extension of RotatE [\[52\]](#page-17-10) that embeds the triplet (s, r, o) into the complex space and interprets the relation as a rotation from the head entity to the tail entity. Similarly, ChronoR associates the timestamp with the relation and treats the combination of relation and timestamp as a rotation from the head entity to the tail entity. The score function is defined as follows,

$$
g(\mathbf{s}, \mathbf{r}, \mathbf{o}, \mathbf{t}) = \langle \mathbf{s} \circ [\mathbf{r} | \mathbf{t}] \circ \mathbf{r}_2, \mathbf{o} \rangle, \tag{8}
$$

where s, r, o, t ∈ C d ; ◦ denotes Hadamard (or elementwise) product; ⟨·⟩ denotes the inner product operation.
**TComplEx**and**TNTComplEx**[\[18\]](#page-16-18) initially expand the 3rd-order tensor to the 4th-order in complex space to perform TKGC. Especially, TNTComplEx considers that some facts may not change over time, thus dividing the TKG into temporal and non-temporal components. Equally important,**TeRo**[\[53\]](#page-17-11) incorporates timestamps into the head and tail entities in complex space to define the temporal evolution of entities, and the relation is served as the rotation from the head to the tail entity. To further improve the modeling and reasoning ability of the temporal relation pattern,**TGeomE**[\[54\]](#page-17-12) embeds the TKG into the hypercomplex (quaternion) space, and incorporates the timestamp into relation to define a time-specific relation embedding. Meanwhile, TGeomE performs geometric product and Clifford conjugation operations among the head entity, the time-specific relation and the tail entity to denote the score function in quaternion space. Based on TGeomE,**TeLM**[\[19\]](#page-16-19) further proposes a novel temporal regularization for temporal embeddings to improve smoothness between the neighboring timestamps.**RotateQVS**[\[55\]](#page-17-13) regards temporal information as the rotation axis and employs a rotation on the entity to represent the evolution of the entity in the quaternion space. In order to comprehensively capture the spatio-temporal and relational dependencies in TKG,**ST-NewDE**[\[56\]](#page-17-14) encodes the TKG into a rich geometric space and uses Dihedron algebra to learn such spatial and temporal aspects. Recently,**BiQCap**[\[57\]](#page-17-15) explores the evolution of the entity and represents each temporal entity as a translation, while each relation is represented as a combination of Euclidean rotation and hyperbolic rotation in biquaternion space.

The aforementioned methods embed TKGs into complex or quaternion spaces, which achieve the capturing of complex relation patterns. However, they face challenges in capturing the semantic information within TKGs. Currently, some researchers attempt to embed TKGs into special coordinate systems to uncover their semantic information.**HA-TKGE**[\[58\]](#page-17-16) divides temporal information into three hierarchies: year*(Y)*, month *(Y-M)*, and day *(Y-M-D)*(semantic hierarchy in descending order: year, month, day). It hierarchically encodes temporal information into a polar coordinate system to fully exploit the semantic information in TKG. Specifically, HA-TKGE uses radial coordinates to represent temporal information at different levels, where entities with smaller radii indicate a higher semantic hierarchy. Angular coordinates model temporal information at the same semantic hierarchy. Similarly,**STKE**[\[59\]](#page-17-17) embeds TKG into a spherical coordinate system, and regards each fact as a rotation from the head entity to the tail entity. Specifically, STKE divides each fact into the radial part, the azimuth part, and the polar part to learn the accurate embeddings of each quadruplet. However, STKE cannot model and infer complex relation patterns.**HTKE**[\[60\]](#page-17-18) simultaneously embeds the knowledge that happen at the same timestamp into both a polar coordinate system and a temporal hyperplane to model complex relation patterns.

![](_page_6_Figure_5.jpeg)

<span id="page-6-0"></span>Fig. 5. The framework of the non-linear embedding functions-based TKGC methods, which embeds the TKG through*Non-Euclidean Function*and*Gaussian Function*to capture the temporal uncertainty, the semantic and structural information hidden in the TKG.

##*4.2.3 Non-linear Embedding Functions*Non-linear embedding functions-based TKGC methods typically utilize non-linear functions, such as Gaussian and non-Euclidean functions, to embed TKGs, so as to deeply capture the temporal uncertainty, the semantic and structural information. The framework of the non-linear embedding functions-based TKGC methods is shown in Fig. [5.](#page-6-0) Here, we summarize some classic non-linear embedding functions-based TKGC methods, such as**DyERNIE**[\[61\]](#page-17-19),**ATiSE**[\[37\]](#page-16-37) and**HTKE**[\[60\]](#page-17-18).
**DyERNIE**[\[61\]](#page-17-19) proposes a non-Euclidean embedding function that explores evolving entity representations through a velocity vector defined in the tangent space at each timestamp. Specifically, DyERNIE embeds the TKG into the Riemannian manifold and introduces an entityspecific velocity vector to capture dynamic facts that change over time. The evolution process can be denoted as,

$$
\mathbf{s}(t) = \exp_{\mathbf{0}}^{c}(\log_{\mathbf{0}}^{c}(\overline{\mathbf{s}}) + \mathbf{v}_{\mathbf{s}}t) \tag{9}
$$

where ¯s ∈ M<sup>D</sup> c represents the entity embedding that does not change over time in manifold space with the curvature c and the dimension D; v<sup>s</sup> ∈ T0M<sup>D</sup> c represents an entity-specific velocity vector that is defined in the tangent space at origin 0 and captures evolution of the entity s over time. Moreover, DyERNIE measures the distance [\[62\]](#page-17-20) between the head entity s(t) and the tail entity o(t) to define the score function. Likewise,**HERCULES**[\[63\]](#page-17-21) is a timeaware extension of ATTH [\[64\]](#page-17-22), which embeds TKG into the hyperbolic space to fully model different relation patterns and hierarchical structure of TKG. Equally important, HER-CULES defines the curvature of a Riemannian manifold as the product of the relation and temporal information, which captures the evolution process of relation.
**ATiSE**[\[37\]](#page-16-37) initially embeds TKG into the space of multidimensional Gaussian distributions and regards the evolution of the entity/relation representation as an additive time series, comprising the trend component, seasonal component, and random component. ATiSE considers the temporal uncertainty during the evolution of entity/relation repre-

![](_page_7_Figure_1.jpeg)

<span id="page-7-0"></span>Fig. 6. The framework of the deep learning-based TKGC methods.

sentations over time. Similarly,**TKGC-AGP**[\[65\]](#page-17-23) embeds entities and relations of TKG into a specific*Multivariate Gaussian Process (MGP)* to improve the flexibility and expressiveness of TKG, and models the temporal uncertainty through the kernel function and entity/relation-specific covariance matrix of MGP. Furthermore, a 1st-order Markov assumption-based algorithm is designed to effectively optimize the training process of TKGC-AGP.

### 4.3 Deep Learning-based TKGCs

Thanks to the powerful information mining ability, various deep learning algorithms are used to process temporal information in TKGs. As depicted in Fig. [6,](#page-7-0) deep learningbased TKGC methods employ CNN or LSTM to encode the timestamp "*2008-11-4*". Then, the encoded timestamp supports the entity and relation evolution by capturing their intrinsic correlations.

#### *4.3.1 Timestamps-Specific Space*Temporal-specific space-based TKGC methods [\[9\]](#page-16-9), [\[20\]](#page-16-20), [\[60\]](#page-17-18) generally encode timestamps as specific hyperplanes or semantic spaces to enhance the expression of temporal information.
**HyTE**[\[9\]](#page-16-9) associates each timestamp with a corresponding hyperplane, and then maps entities and relations into this hyperplane to perform the translation operation. However, it is worth noting that HyTE is limited in its ability to model and infer complex relation patterns.**HTKE**[\[60\]](#page-17-18) embeds knowledge that happened at the same timestamp into a polar coordinate system, effectively capturing complex relation patterns. It introduces time-specific hyperplanes to explicitly incorporate temporal information with entities and relations.

However, both HyTE and HTKE ignore the diversity of potential temporal properties and relations, as well as the temporal dependency between neighboring hyperplanes. Consequently,**TRHyTE**[\[66\]](#page-17-24) defines three typical temporal properties, such as time interval, open interval, and time point, to distinguish different situations. Specifically, TRHyTE sequentially maps entities to the relational space and subsequently to the temporal hyperplane, enabling the learning of time-relation-aware embeddings. Additionally, TRHyTE applies*Gate Recurrent Unit (GRU)*to simulate the evolution process, so as to capture the temporal dependency between neighboring hyperplanes. Nevertheless, TRHyTE ignores the balance of timestamp distribution, which will severely limit the expressiveness of the TKGC method.**BTHyTE**[\[67\]](#page-17-25) proposes the HyTE [\[9\]](#page-16-9)-based direct encoding temporal information model to embed the timestamp and sets the finest granularity to ensure a balanced distribution of the number of facts in each finest granularity cell.

TABLE 2 Representation of the timestamp.

<span id="page-7-1"></span>

| Section                   | Quarters |  |  | Months |  |  | Weeks |  |  | Days |  |  |                         |  |  |  |  |  |  |
|---------------------------|----------|--|--|--------|--|--|-------|--|--|------|--|--|-------------------------|--|--|--|--|--|--|
| 12 June, 2023 0 1 0 0 0 0 |          |  |  |        |  |  | 1     |  |  |      |  |  | 0 1 0 0 0 0 0 0 0 1 0 0 |  |  |  |  |  |  |
**ToKEi**[\[68\]](#page-17-26) is also based on the HyTE, representing the timestamp within a vector of four sections of sizes 4, 3, 5, and 7, respectively. Specifically, the first section represents*Quarters*, the second section denotes *Months*, the next section is *Weeks*, and *Days*is the final section. More precisely, a year consists of four quarters, a quarter contains three months, a month encompasses five weeks, and a week comprises seven days. As shown in TABLE [2,](#page-7-1) ToKEi sets the second position of the*Quarters*to 1 (Due to June is in the second quarter) and the rest to 0. Similarly, the third position of the*Months*(corresponding to June being the third month of the second quarter), the second position of the*Weeks*(as the 12th of June falls in the second week) and the fifth position of the*Days*, are set to 1. According to the above operations, ToKEi can obtain the embedding of timestamps. Finally, ToKEi associates timestamps with entities and relations to explore the temporal evolution and accomplish the missing items through HyTE. **SANe**[\[69\]](#page-17-27) employs an adaptive approach to learn different latent spaces for temporal snapshots at different timestamps and introduces*Convolutional Neural Networks (CNN)*to embed KGs of different timestamps into their respective latent spaces. Moreover, SANe assigns different CNN-specific parameters for different timestamps to address the problem of overlapping latent spaces.

However, the above methods are all modeled based on triplets, i.e., they associate timestamps with entities and relations to translate quadruplets into triplets. Undoubtedly, this severely limits the ability to express temporal information. In contrast,**QDN**[\[20\]](#page-16-20) is proposed as an extension of TDN [\[70\]](#page-17-28), independently handling timestamps, entities, and relations in their respective spaces to comprehensively capture their semantics. Afterwards, QDN creatively designs the*Quadruplet Distributor (QD)*to facilitate the representation learning of TKG through the information aggregation and distribution among timestamps, relations and entities. In addition, QDN extends the 3rd-order tensor into 4thorder to build the intrinsic correlation of entities, relations, and timestamps.

####*4.3.2 Long Short-Term Memory*

*Long Short-Term Memory (LSTM)*-based TKGC methods [\[71\]](#page-17-29), [\[72\]](#page-17-30) encode timestamps and the evolution of events by *Recurrent Neural Network (RNN)*[\[73\]](#page-17-31), LSTM [\[74\]](#page-17-32) or its variants [\[75\]](#page-17-33).
**TA-TransE**and**TA-DistMult**[\[8\]](#page-16-8) first decompose the timestamp into a series of temporal tokens, such as*year*, *month*and*day*. For example, given a fact *(Barack Hussein Obama, born in, USA, 1961-8-4)*, the timestamp "*1961-8-4*" can be represented as *[1y, 9y, 6y, 1y, 8m, 4d]*. Afterward, TA-TransE and TA-DistMult apply RNNs to learn the relation representation incorporated with the timestamp. Finally, they predict the missing item of the quadruplet through TransE [\[14\]](#page-16-14) and DistMult [\[76\]](#page-17-34), respectively. **TDG2E**[\[71\]](#page-17-29) applies the*Gated Recurrent Unit (GRU)*to capture the structural information of each semantic KG, while preserving the evolution process of the TKG. In addition, TDG2E designs a timespan gate within GRU to solve the problem of unbalanced timestamp distribution in TKG. Specifically, the timespan gate can effectively associate the timestamp between the neighboring static KGs. Likewise,**TRHyTE**[\[66\]](#page-17-24) sequentially maps entities to the relational space and subsequently to the temporal hyperplane, and employs GRU to simulate the evolution process, so as to capture the temporal dependency between neighboring hyperplanes.
**Ma** *et al.*[\[6\]](#page-16-5) decompose the timestamp into sequences through the bag of words model and introduce*Bi-directional Long Short-Term Memory (Bi-LSTM)*to capture the semantic properties of the timestamp together with relations and entities. To further enhance the utilization of uncertain information in TKG,**CTRIEJ**[\[72\]](#page-17-30) employs the GRU-based sequence model to integrate the uncertainty, structural and temporal information. Equally important, CTRIEJ introduces the self-adversarial negative sampling technique to generate negative samples, so as to improve the model expression ability. Similarly,**TeCre**[\[77\]](#page-17-35) vectorizes the timestamp by representing it as a sequence of*year*, *month*and*day*. Moreover, in order to ensure that the model is valid enough for large and complex datasets, TeCre trains the *Long Short-Term Memory (LSTM)*network to learn the joint representation of timestamps and relations. Finally, it creatively designs a novel loss function to guarantee the consistency between entities and relations.

##*4.3.3 Temporal Constraint*Temporal constraint-based TKGC methods [\[78\]](#page-17-36), [\[79\]](#page-17-37) usually regard temporal information as the constraint to ensure the reasoning path along the right direction.
**Chekol** *et al.*[\[78\]](#page-17-36) simultaneously capture the uncertainty and temporality of TKG and explore*Markov Logic Networks (MLNs)*and*Probabilistic Soft Logics (PSLs)*to achieve reasoning tasks on TKG. However, this method has high computational complexity and limited running efficiency. In contrast,**Kgedl**[\[79\]](#page-17-37) captures the evolution process of TKG by embedding entities, relations and path structures. In particular, Kgedl further applies temporal information to constrain path reasoning and representation learning of entities. Likewise,**T-GAP**[\[80\]](#page-17-38) introduces the novel temporal*Graph Neural Network (GNN)*to adaptively aggregate the query-specific sub-TKG, and further encodes the temporal displacement between the timestamp of query and each edge. Furthermore, T-GAP performs a path-based inference operation over the sub-TKG to reason out the missing item.**TempCaps**[\[81\]](#page-17-39) is a light-weighted capsule network [\[82\]](#page-17-40) based embedding method, which dynamically routes retrieved relations and entities in TKG. Specifically, TempCaps

<span id="page-8-1"></span>Fig. 7. The translation of multi-edges mesh form of TKG to the relational multi-chains forms of TKG.

mainly consists of two important components, including the neighbor selector and the dynamic routing aggregator. More specifically, the neighbor selector is imposed with temporal constraints to facilitate the selection process. Based on the results of the neighbor selector, the dynamic routing aggregator further reasons and aggregates the neighbors, so as to dynamically learn the contextualized embedding of the query.

Existing attention-based methods primarily emphasize entity learning and may even update entities through the original embeddings of relations. Consequently, the importance of relations is significantly diminished in these methods.**RoAN**[\[83\]](#page-17-41) proposes a relation-oriented attention mechanism that enhances the impact of relations. Specifically, RoAN reconstructs the multi-edge mesh form of TKG as the relational multi-chain form of TKG (shown in Fig. [7\)](#page-8-1). Afterwards, RoAN adaptively assigns different weights to different relations to achieve the optimization process of relations. Furthermore, while RoAN focuses on the importance of relations, it ignores the importance of temporal information as well as structural information in TKG.**TAL-TKGC**[\[84\]](#page-18-0) designs a temporal attention module that captures the intrinsic correlation between timestamps and entities, and introduces the weighted GCN module to explore the structure information of the entire TKG.

# <span id="page-8-0"></span>5 EXTRAPOLATION-BASED TKGCS

In this section, we group the extrapolation-based TKGC methods into the following several categories:*Rule-based TKGC methods*, *Graph neural network-based TKGC methods*, *Reinforcement learning-based TKGC methods*and*Meta learningbased TKGC methods*.

## 5.1 Rule-based TKGCs

Rule-based TKGC methods are often praised due to their interpretability and reliability, which obtains great success in static knowledge graph applications [\[86\]](#page-18-1), [\[87\]](#page-18-2). Recently, researchers explore the potential that applies the rule-based methods for TKGC. As shown in Fig. [8,](#page-9-0) rule-based TKGC methods extract a series of temporal logical rules from the given TKG before the reasoning operation. Temporal logical rules define the relationship between two entities x and y at timestamp t<sup>l</sup> ,

<span id="page-8-2"></span>
$$
\mathbf{r}(\mathbf{x},\mathbf{y},\mathbf{t}_l) \leftarrow \mathbf{r}_1(\mathbf{x},\mathbf{z}_1,\mathbf{t}_1) \wedge \ldots \wedge \mathbf{r}_{l-1}(\mathbf{z}_{l-1},\mathbf{y},\mathbf{t}_{l-1}), \quad (10)
$$

where the left-hand side denotes the rule head with relation r that can be induced by (←) the right-hand rule body. The

Methods Category Technique SKGC Methods Category Technique SKGC TTransE(2018) [\[11\]](#page-16-11) Timestamps Dep Translation ✓ ChronoR(2021) [\[16\]](#page-16-16) Complex Emb Complex Space ✓ TuckERTNT(2022) [\[29\]](#page-16-29) Timestamps Dep Tensor Decomp ✓ TeLM(2021) [\[19\]](#page-16-19) Complex Emb Quaternion Space ✓ ST-TransE(2020) [\[31\]](#page-16-31) Timestamps Dep Translation ✓ RotateQVS(2022) [\[55\]](#page-17-13) Complex Emb Quaternion Space ✓ T-SimplE(2020) [\[32\]](#page-16-32) Timestamps Dep Tensor Decomp ✓ ST-NewDE(2022) [\[56\]](#page-17-14) Complex Emb Dihedron Algebra ✓ TKGFrame(2020) [\[34\]](#page-16-34) Timestamps Dep ILP – TGeomE(2023) [\[54\]](#page-17-12) Complex Emb Quaternion Space ✓ HERCULES(2021) [\[63\]](#page-17-21) Timestamps Dep Manifold ✓ BiQCap(2023) [\[57\]](#page-17-15) Complex Emb Biquaternions/Manifold ✓ TBDRI(2023) [\[36\]](#page-16-36) Timestamps Dep Block Decomp ✓ TA-DistMult(2018) [\[8\]](#page-16-8) Decomp-Time Time-Encoding ✓ TransR-ILP(2016) [\[15\]](#page-16-15) Transform Func Translation ✓ TeCre(2018) [\[77\]](#page-17-35) Decomp-Time Time-Encoding/LSTM ✓ DE-SimplE(2020) [\[7\]](#page-16-6) Transform Func Tensor Decomp ✓ ToKEi(2020) [\[68\]](#page-17-26) Decomp-Time Time-Encoding ✓ TARGCN(2021) [\[41\]](#page-16-41) Transform Func GCN ✓ LBiE(2021) [\[6\]](#page-16-5) Decomp-Time Bag of Words/BiLSTM ✓ DEGAT(2022) [\[49\]](#page-17-7) Transform Func GAT – Time-LowFER(2022) [\[47\]](#page-17-5) Decomp-Time Tensor Decomp ✓ TNTSimplE(2022) [\[33\]](#page-16-33) Transform Func CP Decomp ✓ HyTE(2018) [\[9\]](#page-16-9) Temporal-Specific Temporal-Hyperp ✓ BoxTE(2022) [\[39\]](#page-16-39) Transform Func Translation ✓ TRHyTE(2021) [\[66\]](#page-17-24) Temporal-Specific Temporal-Hyperp/GRU ✓ F-BoxTE(2022) [\[44\]](#page-17-2) Transform Func Adversarial Learn ✓ BTHyTE(2021) [\[67\]](#page-17-25) Temporal-Specific Temporal-Hyperp ✓ SPLIME(2023) [\[40\]](#page-16-40) Transform Func Transformation ✓ SANe(2022) [\[69\]](#page-17-27) Temporal-Specific Multi-semantic Space – TASTER(2023) [\[46\]](#page-17-4) Transform Func Sparse Matrix ✓ QDN(2023) [\[20\]](#page-16-20) Temporal-Specific Tensor Decomposition – HTTR(2023) [\[38\]](#page-16-38) Transform Func Householder ✓ TDG2E(2020) [\[71\]](#page-17-29) LSTM GRU – DyERNIE(2020) [\[61\]](#page-17-19) Special Space Manifold ✓ CTRIEJ(2023) [\[72\]](#page-17-30) LSTM GRU/Negative Sampling ✓ ATiSE(2020) [\[37\]](#page-16-37) Special Space Gaussian – MUT(2017) [\[78\]](#page-17-36) Constraint Markov – TKGC-AGP(2022) [\[65\]](#page-17-23) Special Space Gaussian/Markov – Kgedl(2019) [\[79\]](#page-17-37) Constraint Path Reasoning – HA-TKGE(2022) [\[58\]](#page-17-16) Special Space Polar CS ✓ T-GAP(2021) [\[80\]](#page-17-38) Constraint GNN – HTKE(2022) [\[60\]](#page-17-18) Special Space Polar CS ✓ TempCaps(2022) [\[81\]](#page-17-39) Constraint Capsule Network – STKE(2023) [\[59\]](#page-17-17) Special Space Spherical CS ✓ IMR(2023) [\[85\]](#page-18-3) Constraint Path Reasoning – TNTComplEx(2020) [\[18\]](#page-16-18) Complex Emb Complex Space ✓ RoAN(2023) [\[83\]](#page-17-41) Constraint Attention ✓ TeRo(2020) [\[53\]](#page-17-11) Complex Emb Complex Space ✓ TAL-TKGC(2023) [\[84\]](#page-18-0) Constraint Attention ✓

TABLE 3 Summary of the interpolation TKGC methods.

<sup>1</sup> **SKGC**represents whether TKGC methods are modeled based on SKGC methods, and draws ✓if it is;

<sup>2</sup>**Constraint**is*Temporal constraint-based TKGC methods*. **Temporal-Hyperp**is*Temporal Hyperplane*; **ILP**represents*Integer Linear Programming*; **CS**denote*Coordinate System*.

![](_page_9_Figure_5.jpeg)

<span id="page-9-0"></span>Fig. 8. The framework of the rule-based TKGC methods.

rule body is represented by the conjunction (∧) of a series of body relations r∗.

Each rule is written in the form of a logical implication. If the conditions on the right-hand side (rule body) are satisfied, the statement on the left-hand (rule head) holds true. The extracted rules are fed into a logical rule reasoning module to infer new events on TKG, applying either forward-chain or backward-chain reasoning module [\[88\]](#page-18-4).

# *5.1.1 Manual Rule Mining*Recently, many researchers analyze the characteristic of TKG and manually design some logical rules for TKGC.**TPRG**[\[89\]](#page-18-5) proposes a multi-hop TKGC method based on temporal logical rules. TPRG analyzes the logical connections of multi-hop paths in the TKG. It manually defines fourteen temporal logical rules. These rules capture different kinds of logical relations between entities and can be used to infer new facts.**KGFFP**[\[90\]](#page-18-6) asks human experts to define several temporal logical rules for forest fire prediction.**TLmod**[\[91\]](#page-18-7) analyzes the principles of the temporal logical rule definition. It proposes a pruning strategy to obtain rules and calculate confidence scores. The rules with high confidence are selected for TKGC.

##*5.1.2 Automatic Rule Mining*With the increasing relations and entities in TKG, it is burdensome to manually define the logical rules. Thus, automatic rule mining has attached increasing attention from researchers.
**ALRE-IR**[\[92\]](#page-18-8) proposes an adaptive logical rule embedding model that automatically extracts logical rules from historical data. ALRE-IR extracts all possible rule paths between entities. Then, it adopts GRU to encode the representation of each rule. The learned rule embeddings are

used to predict missing facts.**TLogic**[\[93\]](#page-18-9) introduces a novel symbolic framework based on temporal random walks in TKGs. TLogic directly learns temporal logical rules from TKG and feeds these rules into a symbolic reasoning module for prediction. TLogic offers explicit and human-readable explanations in the form of temporal logical rules that can be easily scaled to accommodate large datasets.**TILP**[\[94\]](#page-18-10) presents a differentiable framework for temporal logical rule learning. TILP proposes the constrained random walk mechanism on TKG. By introducing the temporal operators, TILP enables to learn temporal logical rules from TKG without restrictions. Instead of learning simple chain-like rules as shown in Eq. [10,](#page-8-2)**TFLEX**[\[95\]](#page-18-11) proposes a temporal feature-logic embedding framework that supports complex multi-hop logical rules on TKG.

### 5.2 Graph Neural Network-based TKGCs
*Graph Neural Network (GNN)*-based TKGC methods generally apply GNN to explore the intrinsic topology relevance between entities or between entities and relations in TKG, so as to obtain high-quality embeddings. In specific, GNNbased TKGC methods mainly consist of *Graph convolutional network-based TKGC methods*, *Graph attention network-based TKGC methods*and*Transformer-based TKGC methods*####*5.2.1 Graph Convolutional Network*

*Graph Convolutional Network (GCN)*-based TKGC methods typically integrate the graph structural encoder and the temporal encoder to derive entity representations. As depicted in Fig. [9,](#page-10-0) each snapshot of the TKG is encoded by *Graph Convolutional Network (GCN)*, while the temporal dependencies among multiple snapshots are captured by *Recurrent Neural Networks (RNNs)*.

**Structural encoder**generates entity embeddings based on the graph G(t) within each time step. This is typically built upon existing encoders of message passing networks on static KGs. For example, RE-NET [\[10\]](#page-16-10) uses a multirelational graph aggregator [\[96\]](#page-18-12) to capture the graph structural information. Specifically, the multi-relational graph aggregator can incorporate information from multi-relational and multi-hop neighbors. Formally, the aggregator is defined as follows,

$$
g\left(\mathbf{N}_t^{(s)}\right) = \mathbf{h}_s^{(l+1)} = \sigma \left(\sum_{r \in \mathcal{R}} \sum_{s,o \in \mathcal{E}} \frac{1}{c_s} \mathbf{W}_r^{(l)} \mathbf{h}_o^{(l)} + \mathbf{W}_0^{(l)} \mathbf{h}_s^{(l)}\right),\tag{11}
$$

where initial hidden representation for each node h (0) o is set to trainable embedding vector; σ denotes the non-linear activation function and c<sup>s</sup> is a normalizing factor.
**Temporal Encoder**integrates temporal information into entity representations. Specifically, RE-NET [\[10\]](#page-16-10) employs an RNN-based temporal encoder to capture temporal dependencies as follows,

$$
\mathbf{H}_{t} = \text{RNN}^{1} (g(G_{t}), \mathbf{H}_{t-1})
$$

\n
$$
\mathbf{h}_{t}(\mathbf{s}, \mathbf{r}) = \text{RNN}^{2} (g(\mathbf{N}_{t}^{(\mathbf{s})}), \mathbf{H}_{t}, \mathbf{h}_{t-1}(\mathbf{s}, \mathbf{r}))
$$
\n
$$
\mathbf{h}_{t}(\mathbf{s}) = \text{RNN}^{3} (g(\mathbf{N}_{t}^{(\mathbf{s})}), \mathbf{H}_{t}, \mathbf{h}_{t-1}(\mathbf{s})),
$$
\n(12)

where g denotes an aggregate function and N (s) t stands for all the events related to entity s at the current time step t.

![](_page_10_Figure_13.jpeg)

<span id="page-10-0"></span>Fig. 9. The framework of the graph convolutional network-based TKGC methods

Based on the above framework, subsequent studies have made improvements to the structural encoder and/or the temporal encoder by incorporating more complex message passing or recurrent neural architectures. For instance,**Deng** *et al.*[\[97\]](#page-18-13) utilize CompGCN to capture the influence of neighboring entities and event types, while incorporating GRUs to model the temporal dependency among representations.**TeMP**–*Temporally Enhanced Message Passing*[\[98\]](#page-18-14) leverages RGCN to account for the impact of neighboring entities and introduces a frequency-based gating GRU to capture the temporal dependency among inactive events.**DACHA**[\[99\]](#page-18-15) proposes dual GCN to obtain entity representations, which considers information interaction on both the primal graph (i.e., entity interaction graph) and the edge graph (i.e., relation interaction graph). Moreover, a self-attentive encoder is employed to model the temporal dependency among event types. Similarly,**RE-GCN**[\[100\]](#page-18-16) employs RGCN to aggregate messages from neighboring entities and utilizes an auto-regressive GRU to model the temporal dependency among events.**CyGNet**[\[101\]](#page-18-17) leverages a copy-generation mechanism to capture the global repetition frequency of facts.

However, these methods are difficult to simultaneously consider the sequential, repetitive, and cyclical historical facts.**TiRGN**[\[102\]](#page-18-18) combines local and global historical information to capture sequential, repetitive, and cyclical patterns of historical facts. It achieves this purpose through a GNN-based encoder with double recurrent mechanism.**HiSMatch**[\[103\]](#page-18-19) integrates the background knowledge into the TKGC model via a background knowledge encoder that is also formulated by**CompGCN**[\[97\]](#page-18-13). HiSMatch complementally captures high-order associations among entities.**SPA**[\[104\]](#page-18-20) automatically designs data-specific message passing architectures for TKGC.**TANGO**[\[105\]](#page-18-21) extends neural ODE [\[106\]](#page-18-22) to model dynamic TKGs. TANGO preserves the continuous nature of TKGs and encodes both temporal and structural information into continuous-time dynamic embeddings.**HGLS**[\[107\]](#page-18-23) transforms the TKG sequence into a global graph to explicitly associate historical entities in different time steps. A hierarchical RGCN module is designed to capture long-term dependencies among entities by hierarchically encoding the global graph. Besides,

![](_page_11_Figure_1.jpeg)

<span id="page-11-0"></span>Fig. 10. The framework of the graph attention network-based TKGC methods.

a gating integration module is developed to adaptively integrate long- and short-term information for each entity and relation.

##*5.2.2 Graph Attention Network*

*Graph ATtention network (GAT)*-based TKGC methods aggregate neighboring nodes to enhance the expression capability of current node. As illustrated in Fig. [10,](#page-11-0) GATbased TKGC methods assign different weights to neighboring nodes to aggregate them and update the embedding of the current node to enable the link prediction task.

**TPmod**[\[108\]](#page-18-24) defines the Goodness values for relations and the Closeness values for entity pairs, which proposes a tendency strategy to fuse the values of Goodness and Closeness and utilizes the attention mechanism to aggregate historical events related to entities.**EvoKG**[\[109\]](#page-18-25) simultaneously captures the structural and temporal dynamics in TKGs by jointly modeling the event time and the evolving network structure. However, it is crucial to note that the influence of historical events on future events is not constant and will change over time.**DA-Net**[\[110\]](#page-18-26) learns historical information from different timestamps through an attention mechanism and allocates attention to future events. Similarly,**TAE**[\[111\]](#page-18-27) proposes an effective time-aware encoder that captures the impact of temporal information from entities and relations to obtain accurate time-specific representations. In order to explore the nature of graph evolution over time,**EvoExplore**[\[112\]](#page-18-28) describes the formation process of graph structure and the dynamic topology transformation of graphs from local and global structures, respectively. Among them, the local structure adopts the hierarchical attention mechanism to describe the establishment process of the relations. The global structure employs soft modularity parameterized by the entity representations to capture the dynamic community partition of TKGs.

Future events may occur simultaneously, and there may be mutual influences among them.**CRNet**[\[113\]](#page-18-29) leverages concurrent events from both history and future for TKG reasoning. Additionally, CRNet selects the top-N candidate events and constructs a candidate graph for all missing events in the future. Subsequently, the GAT network handles the interaction among candidate events. However, predicting future events not only relies on repetitive and

![](_page_11_Figure_9.jpeg)

<span id="page-11-1"></span>Fig. 11. The framework of the Transformer-based TKGC methods.

periodic historical events but also requires the integration of potential non-historical events.**CENET**[\[114\]](#page-18-30) considers both types of information, learning a convincing distribution of entities from historical and non-historical events and identifying important entities through a comparative learning algorithm. Currently, the incompleteness issue of lowresource language TKGs is particularly prominent because of the challenge in collecting sufficient corpus and annotations. As a consequence, this leads to suboptimal reasoning performance.**MP-KD**[\[115\]](#page-18-31) aims to enhance reasoning in low-resource TKGs by leveraging high-resource language TKGs through cross-lingual alignment and knowledge distillation.
**Know-Evolve**[\[116\]](#page-18-32) learns non-linearly evolving entity representations by considering their interactions with other entities in multi-relational space. It mainly models the occurrence of a fact as a multi-dimensional temporal point process, where the conditional intensity function of the process is adjusted based on the relationship score of the event. To consider the continuity of states in the evolution of the TKG,**RTFE**[\[117\]](#page-18-33) treats the sequence of the graph as a Markov chain so that the state of the next timestamp is only related to the previous timestamp. When new timestamps appear, there is no need to retrain previous all timestamps, and the expansion to new timestamps occurs naturally through the state transition process. However, RTFE does not take into account recurring events.**CyGNet**[\[101\]](#page-18-17) addresses this problem by learning knowledge from known events. It involves predicting future events not only from the entire entity vocabulary but also by repeatedly identifying transactions and referencing known facts.**xERTE**[\[118\]](#page-18-34) also designs the temporal relational graph attention mechanism to reason the subgraph and poses temporal constraints to ensure the inference along the right direction. Likewise,**T-GAP**[\[80\]](#page-17-38) explores query-relevant substructure in the TKG for path-based inference. Additionally, T-GAP aggregates useful information by considering the temporal displacement between each edge and the timestamps of input query.

##*5.2.3 Transformer*Transformer-based TKGC methods leverage the powerful modeling ability of Transformer to capture both structural and temporal association within TKGs. As illustrated in Fig. [11,](#page-11-1) Transformer not only enables the exploration of structural associations within each historical snapshot but also captures the temporal relationships among different historical snapshots to accomplish link prediction tasks.

Existing TKGC methods often only focus on entities or relations, while ignoring the structural information of the entire TKG.**HSAE**[\[119\]](#page-18-35) employs a self-attention mechanism to capture the structural information of entities and relations and utilizes diachronic embedding functions to explore the evolution of entities and relations. Events often come with certain precursors, meaning that future events often evolve from historical events.**rGalT**[\[120\]](#page-18-36) proposes a novel auto-encoder architecture that introduces a relation-aware graph attention layer into Transformer to accommodate extrapolation inference over the TKG.**GHT**[\[121\]](#page-18-37) captures both structural and temporal information by introducing the Transformer framework. It not only predicts the occurrence time of events but also processes unseen timestamps through a continuous-time encoding function and provides personalized query responses.

### 5.3 Meta Learning-based TKGCs

TKGs undergo a dynamic evolutionary process with new entities and relations continuously being added. These entities and relations are often unseen during the training process and are associated with only a limited number of facts, which makes it difficult for existing models to handle the future data [\[122\]](#page-18-38), [\[123\]](#page-18-39).

To address this challenge, the promising meta-learning method learns a meta-learner to quickly adapt to new tasks with a few training examples [\[124\]](#page-18-40), [\[125\]](#page-18-41). In the context of TKG, the meta-learner is generalized to handle the future data with a limited number of historical facts. The meta learning-based TKGC can be roughly grouped into two categories:*matching network-based methods*and*meta-optimizationbased methods*.

## *5.3.1 Matching Network*Matching network-based TKGC methods aim to learn a metric space where the distance between the few-shot historical facts and the future data can be used to predict new facts.**FTAG**[\[126\]](#page-19-0) proposes a one-shot meta-learning TKGC framework, which designs a novel temporal neighborhood encoder empowered by a self-attention mechanism to capture the temporal interactions between entities and represent historical facts. Subsequently, it builds a matching network to compute the similarity score between new facts and historical examples. In this way, FTAG predicts new facts with only one-shot historical data. To handle fewshot data,**FTMF**[\[127\]](#page-19-1) employs a cyclic recursive aggregation network to aggregate few-shot data and utilizes a fault-tolerant mechanism to consider the noise information. Finally, a RNN-based matching network is employed to measure the similarity between the few-shot data and future data.**TFSC**[\[128\]](#page-19-2) designs a time-aware matching processor that incorporates the temporal information to calculate the similarity score.

###*5.3.2 Meta-optimization*Meta-optimization-based TKGC methods update the parameters with the meta-learning objective on the fewshot samples and better generalize to future data.**MOST**[\[129\]](#page-19-3) proposes a meta-learning framework to learn metarepresentation for the few-shot relations and predict new facts.**MetaTKG**[\[130\]](#page-19-4) designs a temporal meta-learner to learn evolutionary meta-knowledge, which guides the prediction model in adapting to future data. Specifically, a gating integration module adaptively establishes temporal correlations between historical data.**MetaTKGR**[\[131\]](#page-19-5) proposes a novel meta-learning temporal knowledge graph reasoning framework. To consider the dynamic distribution shift, it dynamically adjusts the strategies of sampling and aggregating neighbors from recent facts for new entities. In this way, MetaTKGR enables to handle temporal adaptation with large variance.

### 5.4 Reinforcement Learning-based TKGCs
*Reinforcement Learning (RL)*[\[138\]](#page-19-6) adjusts the strategy based on feedback to maximize cumulative rewards in the process of interaction and finally obtain the optimal learning strategy. RL-based methods treat TKGC as a*Markov Decision Process (MDP)* [\[139\]](#page-19-7), which is superior to producing explainable predictions.

For instance, by establishing connections among the temporal events (*COVID-19*, *Infect*, *Tom*, *2022-12-3*), (*Tom*, *Talk to*, *Fack*, *2022-12-4*) and (*Jack*, *Visit*, *City Hall*, *2022-12- 5*), RL-based TKGC methods can infer a new quadruplet (*COVID-19*, *Occur*, *City Hall*, *2022-12-6*) [\[136\]](#page-19-8). These methodes leverage historical TKG snapshots to infer answers for future-related queries. The components of the MDP are described as follows:

- **States.**Let S denote the state space, where a state is represented by a quintuple s<sup>l</sup> = (e<sup>l</sup> , t<sup>l</sup> , eq, tq, rq) ∈ S. Here, (e<sup>l</sup> , tl) represents the node visited at step l, and (eq, tq, rq) represents the elements in the query. The former represents local information, while the latter can be seen as global information. The agent starts from the source node of the query, so the initial state is s<sup>0</sup> = (eq, tq, eq, tq, rq).
-**Observations.**An agent cannot observe the overall state of the environment. Intuitively, the answer remains hidden while the query and current location are visible to the agent. Formally, the observation function over the state is defined as O ((e<sup>l</sup> , t<sup>l</sup> , eq, tq, rq)) = (e<sup>l</sup> , t<sup>l</sup> , eq, rq).
-**Actions.**Let A denote the action space, and A<sup>l</sup> denote the set of available actions at step l. A<sup>l</sup> ⊂ A consists of the outgoing edges from node e tl l . More specifically, A<sup>l</sup> should be {(r ′ , e ′ , t ′ ) | (e<sup>l</sup> , r ′ , e ′ , t ′ ) ∈ F, t ′ ≤ t<sup>l</sup> , t ′ < tq}, but since an entity often has multiple related historical events, this leads to a large number of possible actions. Therefore, the final set of available actions A<sup>l</sup> are sampled from the aforementioned outgoing edges.
-**Transition.**The environment state transitions to a new node through the edge selected by the agent. The transition function δ : S × A → S is defined as δ (s<sup>l</sup> , Al) = sl+1 = (el+1, tl+1, eq, tq, rq), where A<sup>l</sup> represents the sampled outgoing edges of e tl l .

TABLE 4 Summary of the extrapolation TKGC methods.

| Methods                                 | Category        | Technique                              | ED | Methods                            | Category      | Technique                                 | ED |
|-----------------------------------------|-----------------|----------------------------------------|----|------------------------------------|---------------|-------------------------------------------|----|
| TPmod(2021) [108]                       | Graph attention | GRU                                    | –  | FTAG(2022) [126]                   | Meta learning | Attention                                 | –  |
| EvoKG(2022) [109]                       | Graph attention | R-GCN                                  | –  | FTMF(2022) [127]                   | Meta learning | RNN Matching Network                      | –  |
| DA-Net(2022) [110]                      | Graph attention | Attention                              | –  | MOST(2022) [129]                   | Meta learning | Meta-representation Learner               | –  |
| TAE(2022) [111]                         | Graph attention | CNN                                    | ✓  | MetaTKGR(2022) [131] Meta learning |               | Temporal Domain Gen                       | –  |
| EvoExplore(2022) [112]                  | Graph attention | Attention                              | –  | MetaTKG(2023) [130] Meta learning  |               | Gating Integration Module                 | –  |
| CRNet(2022) [113]                       | Graph attention | Translation                            | –  | TFSC(2023) [128]                   |               | Meta learning Time-aware Matching Network | –  |
| CENET(2022) [114]                       | Graph attention | Contrastive Learning                   | –  | RE-NET(2019) [10]                  | GNN           | GCN/RNN                                   | ✓  |
| Know-Evolve(2022) [116] Graph attention |                 | RNN                                    | –  | Glean(2020) [97]                   | GNN           | GCN/GRU                                   | ✓  |
| RTFE(2022) [117]                        | Graph attention | Contrastive Learning                   | –  | TeMP(2020) [98]                    | GNN           | GCN/gating GRU                            | ✓  |
| MPKD(2023) [115]                        |                 | Graph attention Knowledge Distillation | –  | DACHA(2021) [99]                   | GNN           | GCN/Self-attention                        | ✓  |
| CyGNet(2023) [101]                      |                 | Graph attention Knowledge Distillation | –  | RE-GCN(2021) [100]                 | GNN           | GCN/Self-attention                        | ✓  |
| rGalT(2022) [120]                       | Transformer     | self-attention                         | ✓  | TANGO(2021) [105]                  | GNN           | GCN/Neural ODE                            | ✓  |
| GHT(2022) [121]                         | Transformer     | self-attention                         | ✓  | TiRGN(2022) [102]                  | GNN           | GCN/Double RNN                            | ✓  |
| HSAE(2023) [119]                        | Transformer     | self-attention                         | ✓  | HiSMatch(2022) [103]               | GNN           | GCN/RNN                                   | ✓  |
| KGFFP(2022) [90]                        | Rule Mining     | Manual Rule Mining                     | –  | HGLS(2023) [107]                   | GNN           | GCN/Gating mechanism                      | ✓  |
| TLogic(2022) [93]                       | Rule Mining     | Temporal Random Walk                   | –  | CluSTeR(2020) [132]                | RL            | Beam-level rewards                        | –  |
| TILP(2022) [94]                         | Rule Mining     | Differentiable Learning                | –  | TAgent(2021) [133]                 | RL            | Binary terminal rewards                   | –  |
| TFLEX(2022) [95]                        | Rule Mining     | Logical Embedding                      | –  | TPath(2021) [134]                  | RL            | Path diversity rewards                    | –  |
| TPRG(2023) [89]                         | Rule Mining     | Manual Rule Mining                     | –  | TITer(2021) [135]                  | RL            | Time-shaped rewards                       | –  |
| TLmod(2023) [91]                        | Rule Mining     | Manual Rule Mining                     | –  | DREAM(2023) [136]                  | RL            | Attention/dynamic rewards                 | –  |
| ALRE-IR(2023) [92]                      | Rule Mining     | GRU                                    | ✓  | RLAT(2023) [137]                   | RL            | LSTM/attention/RL                         | –  |

<sup>1</sup>**ED**represents whether TKGC methods are Encoder-Decoder structure, and draw ✓if it is;

<sup>2</sup>**Temporal Domain Gen**denotes*Temporal Domain Generalization*.

When applying RL to the TKG reasoning task, a key challenge lies in constructing an appropriate reward function. Many existing methods rely on manually designed rewards.

**TAgent**[\[133\]](#page-19-10) adopts binary terminal rewards for TKGC, which limits its ability to obtain sufficient rewards. In order to improve the quality of the reward function, subsequent methods have made novel attempts.**TPath**[\[134\]](#page-19-11) introduces path diversity rewards, while**TITer**[\[135\]](#page-19-12) incorporates timeshaped rewards based on Dirichlet distribution to guide the model learning.**CluSTeR**[\[132\]](#page-19-9) utilizes the RNN to acquire temporal information and incorporates it into the beamlevel reward function. However, these models heavily rely on manually designed rewards, which introduces limitations due to the sparse reward dilemma, laborious design process, and performance fluctuations.**DREAM**[\[136\]](#page-19-8) introduces an attention-based adaptive RL model to predict future missing items. The model consists of two main components: (1) a multi-faceted attention representation learning method that captures simultaneously semantic dependence and temporal evolution; (2) an adaptive RL framework that performs multi-hop reasoning by dynamically learning the reward function.

For temporal multi-hop reasoning,**TPath**[\[134\]](#page-19-11) takes temporal information into consideration and selects specific multi-hop reasoning paths in TKGs. TPath proposes a policy network that can train the agent to learn temporal multihop reasoning paths. In addition, it also proposes a reward function that considers the diversity of temporal reasoning paths.**RLAT**[\[137\]](#page-19-13) combine RL with the attention mechanism for temporal multi-hop reasoning. RLAT uses LSTM

and attention mechanism as memory components, which are helpful to train multi-hop reasoning paths. Second, an attention mechanism with an influence factor is proposed. This mechanism measures the influence of neighbor information and provides different feature vectors. The strategy function makes the agent focus on occurring relations with high frequency, allowing for multi-hop reasoning paths with higher correlation.

# <span id="page-13-0"></span>6 APPLICATIONS

In this section, we mainly summarize the applications of TKGC to some downstream tasks, including*Question answering systems*, *Medical and risk analysis systems*and*Recommendation systems*.

## 6.1 Question Answering Systems

Question answering systems are crucial applications of TKGCs. They typically perform queries and reasoning on TKGs, leveraging keywords from the question to predict missing entities or relations, and subsequently provide accurate answers to the questions. The specific process is shown in Fig. [12.](#page-14-0)

**Event-QA**[\[140\]](#page-19-14) proposes a TKG designed for answering event-centric questions, including 1000 semantic queries and more than 970 thousand multilingual events. This method involves inferring missing entities or relations in the TKG using the keywords provided in the question, thereby guiding the QA model to provide an accurate answer. In

![](_page_14_Figure_1.jpeg)

<span id="page-14-0"></span>Fig. 12. The framework of question answering with TKG reasoning.

order to better address complex temporal reasoning questions based on the TKG.**TwiRGCN**[\[141\]](#page-19-15) designs a novel weighted GCN to answer questions that require complex temporal reasoning in TKGs. Furthermore,**FORECAST-TKGQA**[\[142\]](#page-19-16) proposes a large-scale TKGQA dataset that aims to predict future facts. For each question in this dataset, the QA models can only have access to the TKG information before the timestamp annotated in the given question for answer inference.**Ong** *et al.*[\[143\]](#page-19-17) propose a new TKGQA dataset based on the TKGC task,which associates over 5000 financial news documents with question-answer pairs.

Previous studies have identified various issues, notably the omission of specific time references within the TKG and the neglect of the temporal order of timestamps. To address these issues,**TSQA**[\[144\]](#page-19-18) uses the timestamp estimation module to infer the timestamp of the question, and uses a time-sensitive KG encoder to fuse ordering information into TKG embedding. The existing question-answer scheme on the TKG mainly focuses on a simple temporal question, which can rely on a single TKG fact.**TempoQR**[\[145\]](#page-19-19) proposes a framework to solve complex questions by retrieving relevant information from the underlying TKG based on the keywords in question. Afterwards, this method infers temporal information through the TKGC task, eliminating the necessity of directly accessing the TKG. Likewise,**CTRN**[\[146\]](#page-19-20) captures implicit temporal and relation representations of each question via the TKG reasoning process, and then generates accurate answers through the QA model.

## 6.2 Medical and Risk Analysis Systems

Medical and risk analysis systems are important applications of TKGC, e.g., medical diagnosis systems [\[147\]](#page-19-21) and risk analysis systems [\[148\]](#page-19-22).

For the medical domain, traditional systems are designed based on static data, which is difficult to reflect the dynamical variation characteristics of data.**Song** *et al.*[\[147\]](#page-19-21) first explore GRU to integrate the temporal information into the KG, and then apply TransR [\[149\]](#page-19-23) to ensure the structural completeness of the TKG. Finally, they improve the accuracy of medical diagnosis systems by leveraging the complete TKG.**Yang** *et al.*[\[150\]](#page-19-24) propose a novel Chinese medical search system that applies the TKG to represent the dynamic changing of traditional Chinese medicine. Afterwards, they propose a TKGC model to complete the temporal intentions of search sentences for medical diagnosis.

![](_page_14_Figure_8.jpeg)

<span id="page-14-1"></span>Fig. 13. The framework of recommendation with TKG Reasoning.

Since most data, in reality, is multi-source spatiotemporal data, it is difficult for traditional static data to reflect the temporal dependency among the data. Especially for analysis systems, most of the data involved are timedependent, such as weather data and traffic data.**Lin** *et al.*[\[151\]](#page-19-25) first present a TKGC model and utilize the complete TKG for analyzing the multi-source data in smart cities. Likewise,**KG4MR**[\[148\]](#page-19-22) designs a TKGC model to predict relations between risky weather and models the relationship among risky weather events, human activity events and element attributes in knowledge graphs. Afterwards, KG4MR proposes a query method to solve the spatio-temporal intersection reasoning and successfully applied it to the Olympic Winter Games Beijing 2022.

### 6.3 Recommendation Systems

Recommendation systems based on TKGC mainly analyze the historical behaviors and preferences of users, and subsequently leverage entity-related TKGs to identify the relevant products or services that users may purchase. The framework is shown in Fig. [13.](#page-14-1)
**TSTKG4Rec**[\[152\]](#page-19-26) constructs a rich travel spatialtemporal KG derived from diverse sources including Baidupedia, Interactive Encyclopedia and Wikipedia. It addresses the problem of fusion of multi-source heterogeneous data and lacking of spatial-temporal information. In order to update the representation of related entities,**Xiao** *et al.*[\[153\]](#page-19-27) propose an incremental construction model for TKGs, which emphasizes the importance of semantic path information between involved entities and the interaction in refining their representations. Specifically, this model extracts semantic paths of varying lengths between user and item, and captures the semantic information of the path and interaction itself information through RNN to update entity representations. In addition, most recommendation systems provide unchanged services without making corresponding improvements over time. To address this issue,**TASR**[\[154\]](#page-19-28) provides service recommendations by leveraging the knowledge graph of practice. It incorporates multiple and complex interactions between heterogeneous entities, including modeling the user-service interactions over time through the construction of a*Temporal Service Knowledge Graph (TSKG)*. TASR explores the TSKG and extracts top-rated services to enhance the quality of service recommendations. With regard to the challenges of representing users' dynamic mobility behaviors and modeling users' long- and shortterm preferences using TKGs, **STKGRec**[\[155\]](#page-19-29) constructs

a spatial-temporal KG based on users' historical check-in sequence. It enables the promotion of the next*Point-of-Interest (POI)*recommendations without introducing external attribute information of users and POIs.

#### 6.4 Others

TKGC also has been widely applied in many other applications, e.g., citiation prediction [\[156\]](#page-19-30), and mobility prediction [\[157\]](#page-19-31).**STKG**[\[157\]](#page-19-31) models the urban mobility trajectories as a temporal knowledge graph, where mobility trajectories, category information of venues, and temporal information are jointly modeled by the facts with different relation types. Then, the mobility prediction is converted to the TKGC problem through an embedding model that captures spatio-temporal patterns.**CTPIR**[\[156\]](#page-19-30) proposes a citation trajectory prediction framework that captures the dynamic influence of citation to predict the future citation trajectory of a paper. It first adopts the R-GCN model to capture the connections between two snapshots. Then, it learns a fine-grained influence representation for trajectory prediction.

# <span id="page-15-0"></span>7 FUTURE DIRECTIONS

In the previous sections, we comprehensively reviewed the TKGC literature and provided an in-depth dissection of them. Meanwhile, we also identified many challenges and open problems that need to be addressed. In this section, we discuss the future directions of this research area.

## 7.1 Multi-Modal Temporal Knowledge Graphs

The rapid development of Internet technology has given rise to the emergence of various forms of data. However, a single modality is often insufficient to fully represent an object, and leveraging multiple modalities for joint representation can enrich the semantics from diverse perspectives. Similarly, this holds true for KGs. Most of the existing KGs consist solely of textual information, which often fails to provide a comprehensive and detailed description of entities, resulting in limited expression of accurate and rich semantics. Consequently, the development of multi-modal KGs becomes increasingly crucial as they allow for diverse representations of entities, enabling a more nuanced and enriched understanding of their semantics. Of course, several research teams have initiated the exploration and construction of multi-modal static KGs. However, the static KGs cannot reflect the temporal correlation and the evolution process. In contrast, multi-modal TKGs can describe the rich semantics of entities, the temporal evolution of events, and the semantic, temporal, and spatial relationships between entities. This enriched representation can be leveraged more effectively in downstream tasks, such as visual question answering and recommendation systems.

### 7.2 Inductive and Few-Shot Learning Settings

The majority of TKGC methods typically rely on the assumption that a large number of training examples are available to learn entity representations, i.e., transductive settings. These methods typically aim to complete the missing facts in TKGs by leveraging the known information in the graph. However, in real-world settings, TKGs often exhibit long-tail distributions, meaning that there are many rare entities and relations (i.e., few-shot settings) or even unseen entities and relations (i.e., inductive settings). These unseen entities and relations pose a challenge for traditional TKGC methods, as they lack sufficient training data to learn accurate representations. In such scenarios, traditional methods may struggle to provide optimal representations for these rare entities and relations. The sparsity of data makes it difficult to generalize and make accurate predictions for these entities. As a result, these methods may fail to effectively complete the missing facts associated with unseen or rare entities.

## 7.3 Logical Query Answering via Temporal Conditions

Answering complex queries with temporal information, e.g.,*what was the first film Julie Andrews starred in after her divorce with Tony Walton*, is an interesting direction for question answerings. Complex query answering has been extensively studied in static KGs, static KGC methods map queries into the vector space and model logical connectives (conjunction, disjunction, and negation) as neural geometric operations. However, these methods do not apply to queries with temporal conditions. Future work can focus on developing more sophisticated complex query embedding models that can handle complex temporal conditions, such as temporal intervals, durations, and granularities. This can enable more accurate and precise query answering, especially when dealing with temporal constraints and evolving information in TKGs.

## 7.4 Unification with Large Language Models

*Large Language Models (LLMs)*have shown great performance in various applications. Pre-trained on the largescale corpus, LLMs enable to contain enormous general knowledge and reasoning ability. Recently, the possibility of unifying LLMs with KGs has attracted increasing attention from researchers and practitioners [\[158\]](#page-19-32). Much research has utilized LLMs to tackle tasks in the field of KGs. However, the unification of LLMs with TKGC methods is less explored by existing research. LLMs are pre-trained on the static corpus which are inadequate in capturing the temporal information. Moreover, TKGs are evolving over time with new knowledge added. How to enable LLMs effectively model the dynamic dependence of TKG and represent new knowledge is still an open question.

## 7.5 Interpretability Analysis

Knowledge graphs are credited for their good interpretability. However, most existing TKGC methods are based on deep learning algorithms which are black-box models. The reasoning process of TKGC methods used to arrive at their results is not explainable to humans. This largely limits their applications in high-stake scenarios, such as medical diagnosis and legal judgment. Although some works [\[80\]](#page-17-38), [\[85\]](#page-18-3), [\[118\]](#page-18-34) attempt to provide humanunderstandable evidence explaining the forecast, they focus on simple models with plain explanations e.g., logical rules and paths. Explaining the complex captured temporal patterns utilized for reasoning and interpreting the more intricate TKGC models still remains an unresolved matter.

# <span id="page-16-7"></span>8 CONCLUSION
*Temporal Knowledge Graph Completion (TKGC)*is an emerging and active research direction that has attracted increasing attention from both academia and industry. In this paper, we presented a comprehensive overview of the recent research in this field. Firstly, we detailed the interpolation methods and further categorized them based on how they handle temporal information. The extrapolation methods were then further described and classified based on how they predict future events. Finally, we discussed the challenges and future directions in this field.

# REFERENCES

- <span id="page-16-0"></span>[1] B. Pu, J. Liu, Y. Kang, J. Chen, and P. S. Yu, "MVSTT: A multiview spatial-temporal transformer network for traffic-flow forecasting,"*IEEE Transactions on Cybernetics*, pp. 1–14, 2022.
- <span id="page-16-1"></span>[2] J. Dalton, L. Dietz, and J. Allan, "Entity query feature expansion using knowledge base links," in *Proceedings of the International ACM SIGIR Conference on Research & Development in Information Retrieval*, 2014, pp. 365–374.
- <span id="page-16-2"></span>[3] Y. Ma, P. A. Crook, R. Sarikaya, and E. Fosler-Lussier, "Knowledge graph inference for spoken dialog systems," in *International Conference on Acoustics, Speech and Signal Processing*, 2015, pp. 5346–5350.
- <span id="page-16-3"></span>[4] E. Boschee, J. Lautenschlager, S. O'Brien, S. Shellman, J. Starz, and M. Ward, "Icews coded event data," in *Harvard Dataverse*, 2015.
- <span id="page-16-4"></span>[5] K. Leetaru and P. A. Schrodt, "Gdelt: Global data on events, location, and tone, 1979–2012," in *the International Studies Association Annual Convention*, vol. 2, no. 4, 2013, pp. 1–49.
- <span id="page-16-5"></span>[6] S. Ma, A. Li, X. Zhao, and Y. Song, "Learning bilstm-based embeddings for relation prediction in temporal knowledge graph," in *Journal of Physics: Conference Series*, vol. 1871, no. 1, 2021, p. 012050.
- <span id="page-16-6"></span>[7] R. Goel, S. M. Kazemi, M. Brubaker, and P. Poupart, "Diachronic embedding for temporal knowledge graph completion," in *Proceedings of the AAAI Conference on Artificial Intelligence*, 2020, pp. 3988–3995.
- <span id="page-16-8"></span>[8] A. Garc´ıa-Duran, S. Duman ´ ciˇ c, and M. Niepert, "Learning se- ´ quence encoders for temporal knowledge graph completion," in *Proceedings of the Conference on Empirical Methods in Natural Language Processing*, 2018, pp. 4816–4821.
- <span id="page-16-9"></span>[9] S. S. Dasgupta, S. N. Ray, and P. P. Talukdar, "HyTE: Hyperplanebased temporally aware knowledge graph embedding." in *Proceedings of the Conference on Empirical Methods in Natural Language Processing*, 2018, pp. 2001–2011.
- <span id="page-16-10"></span>[10] W. Jin, M. Qu, X. Jin, and X. Ren, "Recurrent event network: Autoregressive structure inference over temporal knowledge graphs," *arXiv preprint arXiv:1904.05530*, 2019.
- <span id="page-16-11"></span>[11] J. Leblay and M. W. Chekol, "Deriving validity time in knowledge graph," in *International World Wide Web Conference*, 2018, pp. 1771–1776.
- <span id="page-16-12"></span>[12] F. Mahdisoltani, J. Biega, and F. Suchanek, "YAGO3: A knowledge base from multilingual wikipedias," in *Conference on Innovative Data Systems Research*, 2015.
- <span id="page-16-13"></span>[13] Z. Yang, M. Ding, C. Zhou, H. Yang, J. Zhou, and J. Tang, "Understanding negative sampling in graph representation learning," in *Proceedings of the International Conference on Knowledge Discovery & Data Mining*, 2020, pp. 1666–1676.
- <span id="page-16-14"></span>[14] A. Bordes, N. Usunier, A. Garcia-Duran, J. Weston, and O. Yakhnenko, "Translating embeddings for modeling multirelational data," in *Advances in Neural Information Processing Systems*, 2013, pp. 2787–2795.
- <span id="page-16-15"></span>[15] T. Jiang, T. Liu, T. Ge, L. Sha, B. Chang, S. Li, and Z. Sui, "Towards time-aware knowledge graph completion," in *International Conference on Computational Linguistics: Technical Papers*, 2016, pp. 1715–1724.
- <span id="page-16-16"></span>[16] A. Sadeghian, M. Armandpour, A. Colas, and D. Z. Wang, "ChronoR: rotation based temporal knowledge graph embedding," in *Proceedings of the AAAI Conference on Artificial Intelligence*, 2021, pp. 6471–6479.
- <span id="page-16-17"></span>[17] T. Lacroix, N. Usunier, and G. Obozinski, "Canonical tensor decomposition for knowledge base completion," in *International Conference on Machine Learning*, 2018, pp. 2863–2872.

- <span id="page-16-18"></span>[18] T. Lacroix, G. Obozinski, and N. Usunier, "Tensor decompositions for temporal knowledge base completion," in *International Conference on Learning Representations*, 2020, pp. 1–12.
- <span id="page-16-19"></span>[19] C. Xu, Y.-Y. Chen, M. Nayyeri, and J. Lehmann, "Temporal knowledge graph completion using a linear temporal regularizer and multivector embeddings," in *Annual Meeting of the Association for Computational Linguistics*, 2021, pp. 2569–2578.
- <span id="page-16-20"></span>[20] J. Wang, B. Wang, J. Gao, X. Li, Y. Hu, and B. Yin, "QDN: A quadruplet distributor network for temporal knowledge graph completion," *IEEE Transactions on Neural Networks and Learning Systems*, 2023.
- <span id="page-16-21"></span>[21] B. Cai, Y. Xiang, L. Gao, H. Zhang, Y. Li, and J. Li, "Temporal knowledge graph completion: a survey," *arXiv preprint arXiv:2201.08236*, 2022.
- <span id="page-16-22"></span>[22] F. Erxleben, M. Gunther, M. Kr ¨ otzsch, J. Mendez, and ¨ D. Vrandeciˇ c, "Introducing wikidata to the linked data web," in ´ *Proceedings of the International Semantic Web Conference*, 2014, pp. 50–65.
- <span id="page-16-23"></span>[23] T. Trouillon, J. Welbl, S. Riedel, E. Gaussier, and G. Bouchard, ´ "Complex embeddings for simple link prediction," in *International Conference on Machine Learning*, 2016, pp. 2071–2080.
- <span id="page-16-24"></span>[24] T. Dettmers, P. Minervini, P. Stenetorp, and S. Riedel, "Convolutional 2D knowledge graph embeddings," in *Proceedings of the AAAI Conference on Artificial Intelligence*, 2018, pp. 1811–1818.
- <span id="page-16-25"></span>[25] A. Lunardi, *Interpolation theory*. Springer, 2009, vol. 9.
- <span id="page-16-26"></span>[26] F. M. Gardner, "Interpolation in digital modems. i. fundamentals," *IEEE Transactions on communications*, vol. 41, no. 3, pp. 501– 507, 1993.
- <span id="page-16-27"></span>[27] C. Brezinski and M. R. Zaglia, *Extrapolation methods: theory and practice*. Elsevier, 2013.
- <span id="page-16-28"></span>[28] C. Brezinski, "A general extrapolation algorithm," *Numerische Mathematik*, vol. 35, pp. 175–187, 1980.
- <span id="page-16-29"></span>[29] P. Shao, D. Zhang, G. Yang, J. Tao, F. Che, and T. Liu, "Tucker decomposition-based temporal knowledge graph completion," *Knowledge-Based Systems*, vol. 238, p. 107841, 2022.
- <span id="page-16-30"></span>[30] I. Balazevi ˇ c, C. Allen, and T. M. Hospedales, "Tucker: Tensor ´ factorization for knowledge graph completion," in *Proceedings of the Conference on Empirical Methods in Natural Language Processing*, 2019, pp. 5185–5194.
- <span id="page-16-31"></span>[31] R. Ni, Z. Ma, K. Yu, and X. Xu, "Specific time embedding for temporal knowledge graph completion," in *International Conference on Cognitive Informatics & Cognitive Computing*, 2020, pp. 105–110.
- <span id="page-16-32"></span>[32] L. Lin and K. She, "Tensor decomposition-based temporal knowledge graph embedding," in *International Conference on Tools with Artificial Intelligence*, 2020, pp. 969–975.
- <span id="page-16-33"></span>[33] P. He, G. Zhou, M. Zhang, J. Wei, and J. Chen, "Improving temporal knowledge graph embedding using tensor factorization," *Applied Intelligence*, pp. 1–15, 2022.
- <span id="page-16-34"></span>[34] J. Zhang, Y. Sheng, Z. Wang, and J. Shao, "TKGFrame: a twophase framework for temporal-aware knowledge graph completion," in *Web and Big Data: International Joint Conference, APWeb-WAIM*, 2020, pp. 196–211.
- <span id="page-16-35"></span>[35] M. Li, Z. Sun, W. Zhang, and W. Liu, "Leveraging semantic property for temporal knowledge graph completion," *Applied Intelligence*, pp. 1–14, 2022.
- <span id="page-16-36"></span>[36] M. Yu, J. Guo, J. Yu, T. Xu, M. Zhao, H. Liu, X. Li, and R. Yu, "Tbdri: block decomposition based on relational interaction for temporal knowledge graph completion," *Applied Intelligence*, vol. 53, no. 5, pp. 5072–5084, 2023.
- <span id="page-16-37"></span>[37] C. Xu, M. Nayyeri, F. Alkhoury, H. Yazdi, and J. Lehmann, "Temporal knowledge graph completion based on time series Gaussian embedding," in *Proceedings of the International Semantic Web Conference*, 2020, pp. 654–671.
- <span id="page-16-38"></span>[38] X. Zhao, A. Li, R. Jiang, K. Chen, and Z. Peng, "Householder transformation-based temporal knowledge graph reasoning," *Electronics*, vol. 12, no. 9, p. 2001, 2023.
- <span id="page-16-39"></span>[39] J. Messner, R. Abboud, and I. I. Ceylan, "Temporal knowledge graph completion using box embeddings," in *Proceedings of the AAAI Conference on Artificial Intelligence*, 2022, pp. 7779–7787.
- <span id="page-16-40"></span>[40] W. Radstok, M. Chekol, and Y. Velegrakis, "Leveraging static models for link prediction in temporal knowledge graphs," in *the International Conference on Tools with Artificial Intelligence*, 2021, pp. 1034–1041.
- <span id="page-16-41"></span>[41] Z. Ding, Y. Ma, B. He, and V. Tresp, "A simple but powerful graph encoder for temporal knowledge graph completion," *arXiv preprint arXiv:2112.07791*, 2021.

- <span id="page-17-0"></span>[42] M. L. De Campos, S. Werner, and J. A. Apolinario, "Constrained ´ adaptation algorithms employing householder transformation," *IEEE Transactions on Signal Processing*, vol. 50, no. 9, pp. 2187– 2195, 2002.
- <span id="page-17-1"></span>[43] R. Abboud, I. Ceylan, T. Lukasiewicz, and T. Salvatori, "BoxE: A box embedding model for knowledge base completion," *Advances in Neural Information Processing Systems*, vol. 33, pp. 9649– 9661, 2020.
- <span id="page-17-2"></span>[44] Y. Dai, W. Guo, and C. Eickhoff, "Wasserstein adversarial learning based temporal knowledge graph embedding," *arXiv preprint arXiv:2205.01873*, 2022.
- <span id="page-17-3"></span>[45] J. Wang, B. Wang, J. Gao, Y. Hu, and B. Yin, "Multi-concept representation learning for knowledge graph completion," *ACM Transactions on Knowledge Discovery from Data*, vol. 17, no. 1, pp. 1–19, 2023.
- <span id="page-17-4"></span>[46] X. Wang, S. Lyu, X. Wang, X. Wu, and H. Chen, "Temporal knowledge graph embedding via sparse transfer matrix," *Information Sciences*, vol. 623, pp. 56–69, 2023.
- <span id="page-17-5"></span>[47] I. Dikeoulias, S. Amin, and G. Neumann, "Temporal knowledge graph reasoning with low-rank and model-agnostic representations," *arXiv preprint arXiv:2204.04783*, 2022.
- <span id="page-17-6"></span>[48] S. Amin, S. Varanasi, K. A. Dunfield, and G. Neumann, "Lowfer: Low-rank bilinear pooling for link prediction," in *International Conference on Machine Learning*, 2020, pp. 257–268.
- <span id="page-17-7"></span>[49] J. Wang, C. Zhu, and W. Zhu, "Dynamic embedding graph attention networks for temporal knowledge graph completion," in *Knowledge Science, Engineering and Management*, 2022, pp. 722– 734.
- <span id="page-17-8"></span>[50] B. Xiong, S. Zhu, M. Nayyeri, C. Xu, S. Pan, C. Zhou, and S. Staab, "Ultrahyperbolic knowledge graph embeddings," in *Proceedings of the ACM SIGKDD Conference on Knowledge Discovery and Data Mining*, 2022, pp. 2130–2139.
- <span id="page-17-9"></span>[51] B. Xiong, M. Nayyeri, S. Pan, and S. Staab, "Shrinking embeddings for hyper-relational knowledge graphs," in *Annual Meeting of the Association for Computational Linguistics*, 2023, pp. 1–13.
- <span id="page-17-10"></span>[52] Z. Sun, Z.-H. Deng, J.-Y. Nie, and J. Tang, "RotatE: Knowledge graph embedding by relational rotation in complex space," in *International Conference on Learning Representations*, 2019, pp. 1– 18.
- <span id="page-17-11"></span>[53] C. Xu, M. Nayyeri, F. Alkhoury, H. S. Yazdi, and J. Lehmann, "TeRo: A time-aware knowledge graph embedding via temporal rotation," in *International Conference on Computational Linguistics*, 2020, pp. 1583–1593.
- <span id="page-17-12"></span>[54] C. Xu, M. Nayyeri, Y.-Y. Chen, and J. Lehmann, "Geometric algebra based embeddings for static and temporal knowledge graph completion," *IEEE Transactions on Knowledge and Data Engineering*, vol. 35, no. 5, pp. 4838–4851, 2023.
- <span id="page-17-13"></span>[55] K. Chen, Y. Wang, Y. Li, and A. Li, "RotateQVS: Representing temporal information as rotations in quaternion vector space for temporal knowledge graph completion," *arXiv preprint arXiv:2203.07993*, 2022.
- <span id="page-17-14"></span>[56] M. Nayyeri, S. Vahdati, M. T. Khan, M. M. Alam, L. Wenige, A. Behrend, and J. Lehmann, "Dihedron algebraic embeddings for spatio-temporal knowledge graph completion," in *Proceedings of the International Semantic Web Conference*, 2022, pp. 253–269.
- <span id="page-17-15"></span>[57] S. Zhang, X. Liang, Z. Li, J. Feng, X. Zheng, and B. Wu, "Biqcap: A biquaternion and capsule network-based embedding model for temporal knowledge graph completion," in *Database Systems for Advanced Applications*, 2023, pp. 673–688.
- <span id="page-17-16"></span>[58] J. Zhang and H. Yu, "Hierarchy-aware temporal knowledge graph embedding," in *International Conference on Knowledge Graph*, 2022, pp. 373–380.
- <span id="page-17-17"></span>[59] S. Wang, R. Liu, L. Shen, and A. M. Khattak, "Stke: Temporal knowledge graph embedding in the spherical coordinate system," in *International Conference on Artificial Intelligence and Security*, 2022, pp. 292–305.
- <span id="page-17-18"></span>[60] P. He, G. Zhou, H. Liu, Y. Xia, and L. Wang, "Hyperplane-based time-aware knowledge graph embedding for temporal knowledge graph completion," *Journal of Intelligent & Fuzzy Systems*, vol. 42, no. 6, pp. 5457–5469, 2022.
- <span id="page-17-19"></span>[61] Z. Han, Y. Ma, P. Chen, and V. Tresp, "Dyernie: Dynamic evolution of riemannian manifold embeddings for temporal knowledge graph completion," in *Proceedings of the Conference on Empirical Methods in Natural Language Processing*, 2020, pp. 7301–7316.
- <span id="page-17-20"></span>[62] O. Skopek, O.-E. Ganea, and G. Becigneul, "Mixed-curvature ´ variational autoencoders," in *International Conference on Learning Representations*, 2020.

- <span id="page-17-21"></span>[63] S. Montella, L. Rojas-Barahona, and J. Heinecke, "Hyperbolic temporal knowledge graph embeddings with relational and time curvatures," *arXiv preprint arXiv:2106.04311*, 2021.
- <span id="page-17-22"></span>[64] I. Chami, A. Wolf, D. C. Juan, F. Sala, S. Ravi, and C. Re,´ "Low-dimensional hyperbolic knowledge graph embeddings," in *Annual Meeting of the Association for Computational Linguistics*, 2020, p. 6901–6914.
- <span id="page-17-23"></span>[65] L. Zhang and D. Zhou, "Temporal knowledge graph completion with approximated gaussian process embedding," in *Proceedings of the International Conference on Computational Linguistics*, 2022, pp. 4697–4706.
- <span id="page-17-24"></span>[66] L. Yuan, Z. Li, J. Qu, T. Zhang, A. Liu, L. Zhao, and Z. Chen, "Trhyte: Temporal knowledge graph embedding based on temporal-relational hyperplanes," in *Database Systems for Advanced Applications*, 2022, pp. 137–152.
- <span id="page-17-25"></span>[67] K. Liu and Y. Zhang, "A temporal knowledge graph completion method based on balanced timestamp distribution," *arXiv preprint arXiv:2108.13024*, 2021.
- <span id="page-17-26"></span>[68] J. Leblay, M. W. Chekol, and X. Liu, "Towards temporal knowledge graph embeddings with arbitrary time precision," in *Proceedings of the ACM International Conference on Information & Knowledge Management*, 2020, pp. 685–694.
- <span id="page-17-27"></span>[69] Y. Li, X. Zhang, B. Zhang, and H. Ren, "Each snapshot to each space: Space adaptation for temporal knowledge graph completion," in *Proceedings of the International Semantic Web Conference*, 2022, pp. 248–266.
- <span id="page-17-28"></span>[70] J. Wang, B. Wang, J. Gao, X. Li, Y. Hu, and B. Yin, "Tdn: Triplet distributor network for knowledge graph completion," *IEEE Transactions on Knowledge and Data Engineering*, 2023.
- <span id="page-17-29"></span>[71] X. Tang, R. Yuan, Q. Li, T. Wang, H. Yang, Y. Cai, and H. Song, "Timespan-aware dynamic knowledge graph embedding by incorporating temporal evolution," *IEEE Access*, vol. 8, pp. 6849– 6860, 2020.
- <span id="page-17-30"></span>[72] T. Li, W. Wang, X. Li, T. Wang, X. Zhou, and M. Huang, "Embedding uncertain temporal knowledge graphs," *Mathematics*, vol. 11, no. 3, p. 775, 2023.
- <span id="page-17-31"></span>[73] L. R. Medsker and L. Jain, "Recurrent neural networks," *Design and Applications*, vol. 5, no. 64-67, p. 2, 2001.
- <span id="page-17-32"></span>[74] S. Hochreiter and J. Schmidhuber, "Long short-term memory," *Neural Computation*, vol. 9, no. 8, pp. 1735–1780, 1997.
- <span id="page-17-33"></span>[75] K. Cho, B. V. Merrienboer, D. Bahdanau, and Y. Bengio, "On the properties of neural machine translation: Encoder-decoder approaches," *ArXiv*, vol. abs/1409.1259, 2014.
- <span id="page-17-34"></span>[76] B. Yang, W. T. Yih, X. He, J. Gao, and L. Deng, "Embedding entities and relations for learning and inference in knowledge bases," in *International Conference on Learning Representations*, 2015, pp. 1– 13.
- <span id="page-17-35"></span>[77] J. Ma, C. Zhou, Y. Chen, Y. Wang, G. Hu, and Y. Qiao, "Tecre: A novel temporal conflict resolution method based on temporal knowledge graph embedding," *Information*, vol. 14, no. 3, p. 155, 2023.
- <span id="page-17-36"></span>[78] M. Chekol, G. Pirro, J. Schoenfisch, and H. Stuckenschmidt, ` "Marrying uncertainty and time in knowledge graphs," in *Proceedings of the AAAI Conference on Artificial Intelligence*, vol. 31, no. 1, 2017.
- <span id="page-17-37"></span>[79] Y. Wang, Y. Qiao, J. Ma, G. Hu, C. Zhang, A. K. Sangaiah, H. Zhang, and K. Ren, "A novel time constraint-based approach for knowledge graph conflict resolution," *Applied Sciences*, vol. 9, no. 20, p. 4399, 2019.
- <span id="page-17-38"></span>[80] J. Jung, J. Jung, and U. Kang, "Learning to walk across time for interpretable temporal knowledge graph completion," in *Proceedings of the ACM SIGKDD Conference on Knowledge Discovery & Data Mining*, 2021, pp. 786–795.
- <span id="page-17-39"></span>[81] G. Fu, Z. Meng, Z. Han, Z. Ding, Y. Ma, M. Schubert, V. Tresp, and R. Wattenhofer, "Tempcaps: A capsule network-based embedding model for temporal knowledge graph completion," in *Proceedings of the Workshop on Structured Prediction for Natural Language Processing*, 2022, pp. 22–31.
- <span id="page-17-40"></span>[82] T. Vu, T. D. Nguyen, D. Q. Nguyen, D. Phung *et al.*, "A capsule network-based embedding model for knowledge graph completion and search personalization," in *Proceedings of the Conference of the North American Chapter of the Association for Computational Linguistics*, 2019, pp. 2180–2189.
- <span id="page-17-41"></span>[83] L. Bai, X. Ma, X. Meng, X. Ren, and Y. Ke, "RoAN: A relationoriented attention network for temporal knowledge graph completion," *Engineering Applications of Artificial Intelligence*, vol. 123, p. 106308, 2023.

- <span id="page-18-0"></span>[84] H. Nie, X. Zhao, X. Yao, Q. Jiang, X. Bi, Y. Ma, and Y. Sun, "Temporal-structural importance weighted graph convolutional network for temporal knowledge graph completion," *Future Generation Computer Systems*, vol. 143, pp. 30–39, 2023.
- <span id="page-18-3"></span>[85] Z. Du, L. Qu, Z. Liang, K. Huang, L. Cui, and Z. Gao, "IMF: Interpretable multi-hop forecasting on temporal knowledge graphs," *Entropy*, vol. 25, no. 4, p. 666, 2023.
- <span id="page-18-1"></span>[86] F. Yang, Z. Yang, and W. W. Cohen, "Differentiable learning of logical rules for knowledge base reasoning," *Advances in Neural Information Processing Systems*, vol. 30, 2017.
- <span id="page-18-2"></span>[87] A. Sadeghian, M. Armandpour, P. Ding, and D. Z. Wang, "Drum: End-to-end differentiable rule mining on knowledge graphs," *Advances in Neural Information Processing Systems*, vol. 32, 2019.
- <span id="page-18-4"></span>[88] E. Salvat and M.-L. Mugnier, "Sound and complete forward and backward chainings of graph rules," in *International Conference on Conceptual Structures*. Springer, 1996, pp. 248–262.
- <span id="page-18-5"></span>[89] L. Bai, M. Chen, L. Zhu, and X. Meng, "Multi-hop temporal knowledge graph reasoning with temporal path rules guidance," *Expert Systems with Applications*, vol. 223, p. 119804, 2023.
- <span id="page-18-6"></span>[90] X. Ge, Y. Yang, L. Peng, L. Chen, W. Li, W. Zhang, and J. Chen, "Spatio-temporal knowledge graph based forest fire prediction with multi source heterogeneous data," *Remote Sensing*, vol. 14, no. 14, p. 3496, 2022.
- <span id="page-18-7"></span>[91] L. Bai, W. Yu, D. Chai, W. Zhao, and M. Chen, "Temporal knowledge graphs reasoning with iterative guidance by temporal logical rules," *Information Sciences*, vol. 621, pp. 22–35, 2023.
- <span id="page-18-8"></span>[92] X. Mei, L. Yang, X. Cai, and Z. Jiang, "An adaptive logical rule embedding model for inductive reasoning over temporal knowledge graphs," in *Proceedings of the Conference on Empirical Methods in Natural Language Processing*, 2022, pp. 7304–7316.
- <span id="page-18-9"></span>[93] Y. Liu, Y. Ma, M. Hildebrandt, M. Joblin, and V. Tresp, "Tlogic: Temporal logical rules for explainable link forecasting on temporal knowledge graphs," in *Proceedings of the AAAI Conference on Artificial Intelligence*, 2022, pp. 4120–4127.
- <span id="page-18-10"></span>[94] S. Xiong, Y. Yang, F. Fekri, and J. C. Kerce, "TILP: Differentiable learning of temporal logical rules on knowledge graphs," in *the International Conference on Learning Representations*, 2023.
- <span id="page-18-11"></span>[95] X. Lin, C. Xu, F. Su, G. Zhou, T. Hu, N. Li, M. Sun, H. Luo *et al.*, "TFLEX: Temporal feature-logic embedding framework for complex reasoning over temporal knowledge graph," *arXiv preprint arXiv:2205.14307*, 2022.
- <span id="page-18-12"></span>[96] M. Schlichtkrull, T. N. Kipf, P. Bloem, R. Van Den Berg, I. Titov, and M. Welling, "Modeling relational data with graph convolutional networks," in *Proceedings of the International Semantic Web Conference*, 2018, pp. 593–607.
- <span id="page-18-13"></span>[97] S. Deng, H. Rangwala, and Y. Ning, "Dynamic knowledge graph based multi-event forecasting," in *Proceedings of the ACM SIGKDD Conference on Knowledge Discovery and Data Mining*, 2020, pp. 1585–1595.
- <span id="page-18-14"></span>[98] J. Wu, M. Cao, J. C. K. Cheung, and W. L. Hamilton, "Temp: Temporal message passing for temporal knowledge graph completion," in *Proceedings of the Conference on Empirical Methods in Natural Language Processing*, 2020, pp. 5730–5746.
- <span id="page-18-15"></span>[99] L. Chen, X. Tang, W. Chen, Y. Qian, Y. Li, and Y. Zhang, "Dacha: A dual graph convolution based temporal knowledge graph representation learning method using historical relation," *ACM Transactions on Knowledge Discovery from Data*, vol. 16, no. 3, pp. 1–18, 2021.
- <span id="page-18-16"></span>[100] Z. Li, X. Jin, W. Li, S. Guan, J. Guo, H. Shen, Y. Wang, and X. Cheng, "Temporal knowledge graph reasoning based on evolutional representation learning," in *Proceedings of the International ACM SIGIR Conference on Research and Development in Information Retrieval*, 2021, pp. 408–417.
- <span id="page-18-17"></span>[101] C. Zhu, M. Chen, C. Fan, G. Cheng, and Y. Zhang, "Learning from history: Modeling temporal knowledge graphs with sequential copy-generation networks," in *Proceedings of the AAAI Conference on Artificial Intelligence*, 2021, pp. 4732–4740.
- <span id="page-18-18"></span>[102] Y. Li, S. Sun, and J. Zhao, "TiRGN: Time-guided recurrent graph network with local-global historical patterns for temporal knowledge graph reasoning," in *Proceedings of the International Joint Conference on Artificial Intelligence*, 2022, pp. 2152–2158.
- <span id="page-18-19"></span>[103] Z. Li, Z. Hou, S. Guan, X. Jin, W. Peng, L. Bai, Y. Lyu, W. Li, J. Guo, and X. Cheng, "HiSMatch: Historical structure matching based temporal knowledge graph reasoning," in *Proceedings of the Conference on Empirical Methods in Natural Language Processing*, 2022, pp. 7328–7338.
- <span id="page-18-20"></span>[104] Z. Wang, H. Du, Q. Yao, and X. Li, "Search to pass messages for temporal knowledge graph completion," in *Proceedings of the*

*Conference on Empirical Methods in Natural Language Processing*, 2022, pp. 6160–6172.

- <span id="page-18-21"></span>[105] Z. Han, Z. Ding, Y. Ma, Y. Gu, and V. Tresp, "Learning neural ordinary equations for forecasting future links on temporal knowledge graphs," in *Proceedings of the Conference on Empirical Methods in Natural Language Processing*, 2021, pp. 8352–8364.
- <span id="page-18-22"></span>[106] R. T. Chen, Y. Rubanova, J. Bettencourt, and D. K. Duvenaud, "Neural ordinary differential equations," *Advances in Neural Information Processing Systems*, vol. 31, 2018.
- <span id="page-18-23"></span>[107] M. Zhang, Y. Xia, Q. Liu, S. Wu, and L. Wang, "Learning longand short-term representations for temporal knowledge graph reasoning," in *International World Wide Web Conference*, 2023, pp. 2412–2422.
- <span id="page-18-24"></span>[108] L. Bai, X. Ma, M. Zhang, and W. Yu, "Tpmod: A tendency-guided prediction model for temporal knowledge graph completion," *ACM Transactions on Knowledge Discovery from Data*, vol. 15, no. 3, pp. 1–17, 2021.
- <span id="page-18-25"></span>[109] N. Park, F. Liu, P. Mehta, D. Cristofor, C. Faloutsos, and Y. Dong, "EvoKG: Jointly modeling event time and network structure for reasoning over temporal knowledge graphs," in *Proceedings of the ACM International Conference on Web Search and Data Mining*, 2022, pp. 794–803.
- <span id="page-18-26"></span>[110] K. Liu, F. Zhao, H. Chen, Y. Li, G. Xu, and H. Jin, "DA-Net: Distributed attention network for temporal knowledge graph reasoning," in *Proceedings of the ACM International Conference on Information & Knowledge Management*, 2022, pp. 1289–1298.
- <span id="page-18-27"></span>[111] H. Duan, H. Jin, K. Chen, S. Du, T. Fang, and H. Huo, "An effective time-aware encoder for temporal knowledge graph reasoning," in *Proceedings of the International Conference on Machine Learning and Natural Language Processing*, 2022, pp. 81–87.
- <span id="page-18-28"></span>[112] J. Zhang, S. Liang, Y. Sheng, and J. Shao, "Temporal knowledge graph representation learning with local and global evolutions," *Knowledge-Based Systems*, vol. 251, p. 109234, 2022.
- <span id="page-18-29"></span>[113] S. Wang, X. Cai, Y. Zhang, and X. Yuan, "CRNet: Modeling concurrent events over temporal knowledge graph," in *Proceedings of the International Semantic Web Conference*, 2022, pp. 516–533.
- <span id="page-18-30"></span>[114] Y. Xu, J. Ou, H. Xu, and L. Fu, "Temporal knowledge graph reasoning with historical contrastive learning," in *Proceedings of the AAAI Conference on Artificial Intelligence*, vol. 37, no. 4, 2023, pp. 4765–4773.
- <span id="page-18-31"></span>[115] R. Wang, Z. Li, J. Yang, T. Cao, C. Zhang, B. Yin, and T. Abdelzaher, "Mutually-paced knowledge distillation for cross-lingual temporal knowledge graph reasoning," in *Proceedings of the ACM Web Conference*, 2023, pp. 2621–2632.
- <span id="page-18-32"></span>[116] R. Trivedi, H. Dai, Y. Wang, and L. Song, "Know-evolve: Deep temporal reasoning for dynamic knowledge graphs," in *the International Conference on Machine Learning*, 2017, pp. 3462–3471.
- <span id="page-18-33"></span>[117] Y. Xu, E. Haihong, M. Song, W. Song, X. Lv, W. Haotian, and Y. Jinrui, "RTFE: a recursive temporal fact embedding framework for temporal knowledge graph completion," *arXiv preprint arXiv:2009.14653*, 2020.
- <span id="page-18-34"></span>[118] Z. Han, P. Chen, Y. Ma, and V. Tresp, "Explainable subgraph reasoning for forecasting on temporal knowledge graphs," in *International Conference on Learning Representations*, 2021.
- <span id="page-18-35"></span>[119] X. Ren, L. Bai, Q. Xiao, and X. Meng, "Hierarchical self-attention embedding for temporal knowledge graph completion," in *International World Wide Web Conference*, 2023, pp. 2539–2547.
- <span id="page-18-36"></span>[120] Y. Gao, L. Feng, Z. Kan, Y. Han, L. Qiao, and D. Li, "Modeling precursors for temporal knowledge graph reasoning via autoencoder structure," in *Proceedings of the International Joint Conference on Artificial Intelligence*, 2022, pp. 23–29.
- <span id="page-18-37"></span>[121] H. Sun, S. Geng, J. Zhong, H. Hu, and K. He, "Graph hawkes transformer for extrapolated reasoning on temporal knowledge graphs," in *Proceedings of the Conference on Empirical Methods in Natural Language Processing*, 2022, pp. 7481–7493.
- <span id="page-18-38"></span>[122] L. Luo, Y.-F. Li, G. Haffari, and S. Pan, "Normalizing flow-based neural process for few-shot knowledge graph completion," in *Proceedings of the International ACM SIGIR Conference on Research and Development in Information Retrieval*, 2023.
- <span id="page-18-39"></span>[123] L. Luo, G. Haffari, and S. Pan, "Graph sequential neural ode process for link prediction on dynamic and sparse graphs," in *Proceedings of the ACM International Conference on Web Search and Data Mining*, 2023, pp. 778–786.
- <span id="page-18-40"></span>[124] C. Finn, P. Abbeel, and S. Levine, "Model-agnostic meta-learning for fast adaptation of deep networks," in *the International Conference on Machine Learning*. PMLR, 2017, pp. 1126–1135.
- <span id="page-18-41"></span>[125] A. Nichol, J. Achiam, and J. Schulman, "On first-order metalearning algorithms," *arXiv preprint arXiv:1803.02999*, 2018.

- <span id="page-19-0"></span>[126] M. Mirtaheri, M. Rostami, X. Ren, F. Morstatter, and A. Galstyan, "One-shot learning for temporal knowledge graphs," *arXiv preprint arXiv:2010.12144*, 2020.
- <span id="page-19-1"></span>[127] L. Bai, M. Zhang, H. Zhang, and H. Zhang, "Ftmf: Few-shot temporal knowledge graph completion based on meta-optimization and fault-tolerant mechanism," *International World Wide Web Conference*, pp. 1–28, 2022.
- <span id="page-19-2"></span>[128] H. Zhang and L. Bai, "Few-shot link prediction for temporal knowledge graphs based on time-aware translation and attention mechanism," *Neural Networks*, vol. 161, pp. 371–381, 2023.
- <span id="page-19-3"></span>[129] Z. Ding, B. He, Y. Ma, Z. Han, and V. Tresp, "Learning meta representations of one-shot relations for temporal knowledge graph link prediction," *arXiv preprint arXiv:2205.10621*, 2022.
- <span id="page-19-4"></span>[130] Y. Xia, M. Zhang, Q. Liu, S. Wu, and X.-Y. Zhang, "Metatkg: Learning evolutionary meta-knowledge for temporal knowledge graph reasoning," *arXiv preprint arXiv:2302.00893*, 2023.
- <span id="page-19-5"></span>[131] R. Wang, Z. Li, D. Sun, S. Liu, J. Li, B. Yin, and T. Abdelzaher, "Learning to sample and aggregate: Few-shot reasoning over temporal knowledge graphs," *Advances in Neural Information Processing Systems*, vol. 35, pp. 16 863–16 876, 2022.
- <span id="page-19-9"></span>[132] Z. Li, X. Jin, S. Guan, W. Li, J. Guo, Y. Wang, and X. Cheng, "Search from history and reason for future: Two-stage reasoning on temporal knowledge graphs," in *The Joint Conference of the Annual Meeting of the Association for Computational Linguistics and the International Joint Conference on Natural Language Processing*, 2021, pp. 4732–4743.
- <span id="page-19-10"></span>[133] Y. Tao, Y. Li, and Z. Wu, "Temporal link prediction via reinforcement learning," in *IEEE International Conference on Acoustics, Speech and Signal Processing*, 2021, pp. 3470–3474.
- <span id="page-19-11"></span>[134] L. Bai, W. Yu, M. Chen, and X. Ma, "Multi-hop reasoning over paths in temporal knowledge graphs using reinforcement learning," *Applied Soft Computing*, vol. 103, p. 107144, 2021.
- <span id="page-19-12"></span>[135] H. Sun, J. Zhong, Y. Ma, Z. Han, and K. He, "Timetraveler: Reinforcement learning for temporal knowledge graph forecasting," in *Proceedings of the Conference on Empirical Methods in Natural Language Processing*, 2021, pp. 8306–8319.
- <span id="page-19-8"></span>[136] S. Zheng, H. Yin, T. Chen, Q. V. H. Nguyen, W. Chen, and L. Zhao, "DREAM: adaptive reinforcement learning based on attention mechanism for temporal knowledge graph reasoning," *Computing Research Repository*, vol. abs/2304.03984, 2023.
- <span id="page-19-13"></span>[137] L. Bai, D. Chai, and L. Zhu, "RLAT: multi-hop temporal knowledge graph reasoning based on reinforcement learning and attention mechanism," *Knowledge-Based Systems*, vol. 269, p. 110514, 2023.
- <span id="page-19-6"></span>[138] C. Li and M. Qiu, *Reinforcement learning for cyber-physical systems: with cybersecurity case studies*. Chapman and Hall/CRC, 2019.
- <span id="page-19-7"></span>[139] G. Wan, S. Pan, C. Gong, C. Zhou, and G. Haffari, "Reasoning like human: Hierarchical reinforcement learning for knowledge graph reasoning," in *Proceedings of the International Joint Conference on Artificial Intelligence*, 2020, pp. 1926–1932.
- <span id="page-19-14"></span>[140] T. Souza Costa, S. Gottschalk, and E. Demidova, "Event-QA: A dataset for event-centric question answering over knowledge graphs," in *Proceedings of the ACM International Conference on Information & Knowledge Management*, 2020, pp. 3157–3164.
- <span id="page-19-15"></span>[141] A. Sharma, A. Saxena, C. Gupta, S. M. Kazemi, P. Talukdar, and S. Chakrabarti, "Twirgcn: Temporally weighted graph convolution for question answering over temporal knowledge graphs," *arXiv preprint arXiv:2210.06281*, 2022.
- <span id="page-19-16"></span>[142] Z. Ding, R. Qi, Z. Li, B. He, J. Wu, Y. Ma, Z. Meng, Z. Han, and V. Tresp, "Forecasting question answering over temporal knowledge graphs," *arXiv preprint arXiv:2208.06501*, 2022.

- <span id="page-19-17"></span>[143] R. Ong, J. Sun, O. S, erban, and Y.-K. Guo, "TKGQA Dataset: Using question answering to guide and validate the evolution of temporal knowledge graph," *Data*, vol. 8, no. 3, p. 61, 2023.
- <span id="page-19-18"></span>[144] C. Shang, G. Wang, P. Qi, and J. Huang, "Improving time sensitivity for question answering over temporal knowledge graphs," *arXiv preprint arXiv:2203.00255*, 2022.
- <span id="page-19-19"></span>[145] C. Mavromatis, P. L. Subramanyam, V. N. Ioannidis, A. Adeshina, P. R. Howard, T. Grinberg, N. Hakim, and G. Karypis, "Tempoqr: temporal question reasoning over knowledge graphs," in *Proceedings of the AAAI Conference on Artificial Intelligence*, vol. 36, no. 5, 2022, pp. 5825–5833.
- <span id="page-19-20"></span>[146] S. Jiao, Z. Zhu, W. Wu, Z. Zuo, J. Qi, W. Wang, G. Zhang, and P. Liu, "An improving reasoning network for complex question answering over temporal knowledge graphs," *Applied Intelligence*, vol. 53, no. 7, pp. 8195–8208, 2023.
- <span id="page-19-21"></span>[147] F. Song, B. Wang, Y. Tang, and J. Sun, "Research of medical aided diagnosis system based on temporal knowledge graph," in *the International Conference on Advanced Data Mining and Applications*, 2020, pp. 236–250.
- <span id="page-19-22"></span>[148] J. Chen, S. Zhong, X. Ge, W. Li, H. Zhu, and L. Peng, "Spatiotemporal knowledge graph for meteorological risk analysis," in *IEEE International Conference on Software Quality, Reliability and Security Companion*, 2021, pp. 440–447.
- <span id="page-19-23"></span>[149] Y. Lin, Z. Liu, M. Sun, Y. Liu, and X. Zhu, "Learning entity and relation embeddings for knowledge graph completion," in *Proceedings of the AAAI Conference on Artificial Intelligence*, 2015, pp. 2181–2187.
- <span id="page-19-24"></span>[150] C. Yang, W. Li, X. Zhang, R. Zhang, and G. Qi, "A temporal semantic search system for traditional chinese medicine based on temporal knowledge graphs," in *the Joint International Conference on Semantic Technology*. Springer, 2020, pp. 13–20.
- <span id="page-19-25"></span>[151] L. Zhao, H. Deng, L. Qiu, S. Li, Z. Hou, H. Sun, and Y. Chen, "Urban multi-source spatio-temporal data analysis aware knowledge graph embedding," *Symmetry*, vol. 12, no. 2, p. 199, 2020.
- <span id="page-19-26"></span>[152] W. Zhang, T. Gu, W. Sun, Y. Phatpicha, L. Chang, and C. Bin, "Travel attractions recommendation with travel spatial-temporal knowledge graphs," in *the International Conference of Pioneering Computer Scientists, Engineers and Educators*, 2018, pp. 213–226.
- <span id="page-19-27"></span>[153] C. Xiao, L. Sun, and W. Ji, "Temporal knowledge graph incremental construction model for recommendation," in *International Joint Conference on Web and Big Data*, 2020, pp. 352–359.
- <span id="page-19-28"></span>[154] H. Mezni, "Temporal knowledge graph embedding for effective service recommendation," *IEEE Transactions on Services Computing*, vol. 15, no. 5, pp. 3077–3088, 2021.
- <span id="page-19-29"></span>[155] W. Chen, H. Wan, S. Guo, H. Huang, S. Zheng, J. Li, S. Lin, and Y. Lin, "Building and exploiting spatial–temporal knowledge graph for next poi recommendation," *Knowledge-Based Systems*, vol. 258, p. 109951, 2022.
- <span id="page-19-30"></span>[156] C. Zong, Y. Zhuang, W. Lu, J. Shao, and S. Tang, "Citation trajectory prediction via publication influence representation using temporal knowledge graph," *arXiv preprint arXiv:2210.00450*, 2022.
- <span id="page-19-31"></span>[157] H. Wang, Q. Yu, Y. Liu, D. Jin, and Y. Li, "Spatio-temporal urban knowledge graph enabled mobility prediction," *Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies*, vol. 5, no. 4, pp. 1–24, 2021.
- <span id="page-19-32"></span>[158] S. Pan, L. Luo, Y. Wang, C. Chen, J. Wang, and X. Wu, "Unifying large language models and knowledge graphs: A roadmap," *arXiv preprint arXiv:2306.08302*, 2023.
