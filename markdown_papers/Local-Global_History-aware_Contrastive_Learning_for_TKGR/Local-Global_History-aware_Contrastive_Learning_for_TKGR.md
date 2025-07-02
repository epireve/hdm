---
cite_key: "chen2023"
title: "Local-Global History-aware Contrastive Learning for Temporal Knowledge Graph Reasoning"
authors: "Wei Chen, Huaiyu Wan, Yuting Wu, Shuyuan Zhao, Jiayaqi Cheng, Yuxin Li, Youfang Lin"
year: 2023
doi: "https://doi.org/10.48550/arXiv.2312.01601"
url: "https://arxiv.org/abs/2312.01601"
relevancy: "High"
downloaded: "Yes"
tags:
  - "temporal knowledge graph"
  - "contrastive learning"
  - "historical encoding"
  - "noise resistance"
  - "TKG reasoning"
tldr: "Improves temporal knowledge graph reasoning through local-global history-aware contrastive learning with enhanced noise resistance"
date_processed: "2025-07-02"
phase2_processed: true
original_folder: "Local-Global_History-aware_Contrastive_Learning_for_TKGR"
images_total: 11
images_kept: 11
images_removed: 0
---

# Local-Global History-aware Contrastive Learning for Temporal Knowledge Graph Reasoning

Wei Chen†‡, Huaiyu Wan†‡, Yuting Wu §∗, Shuyuan Zhao†‡, Jiayaqi Cheng† , Yuxin Li† , Youfang Lin†‡ ,

†*School of Computer and Information Technology, Beijing Jiaotong University, Beijing, China*

§*School of Software Engineering, Beijing Jiaotong University, Beijing, China*

‡*Beijing Key Laboratory of Traffic Data Analysis and Mining, Beijing, China*{w chen, hywan, ytwu1, sy zhao, jyq cheng, yuxinli, yflin}@bjtu.edu.cn
*Abstract*—Temporal knowledge graphs (TKGs) have been identified as a promising approach to represent the dynamics of facts along the timeline. The extrapolation of TKG is to predict unknowable facts happening in the future, holding significant practical value across diverse fields. Most extrapolation studies in TKGs focus on modeling global historical fact repeating and cyclic patterns, as well as local historical adjacent fact evolution patterns, showing promising performance in predicting future unknown facts. Yet, existing methods still face two major challenges: (1) They usually neglect the importance of historical information in KG snapshots related to the queries when encoding the local and global historical information; (2) They exhibit weak antinoise capabilities, which hinders their performance when the inputs are contaminated with noise. To this end, we propose a novel Local-global history-aware Contrastive Learning model (LogCL) for TKG reasoning, which adopts contrastive learning to better guide the fusion of local and global historical information and enhance the ability to resist interference. Specifically, for the first challenge, LogCL proposes an entity-aware attention mechanism applied to the local and global historical facts encoder, which captures the key historical information related to queries. For the latter issue, LogCL designs a local-global query contrast module, effectively improving the robustness of the model. The experimental results on four benchmark datasets demonstrate that LogCL delivers better and more robust performance than the state-of-the-art baselines. **背 景 研究动机 选题思路及研究 内容 实验结果 主要方法**

*Index Terms*—Temporal knowledge graph, Graph convolutional network, Contrastive learning

## I. INTRODUCTION

Temporal knowledge graphs (TKGs), which represent dynamic facts as quadruples in the form of (subject, relation, object, time), are actually sequences of KG snapshots with respective timestamps. Reasoning on TKGs aims to predict the unknown facts by modeling the historical KGs snapshots, which involves two reasoning settings: interpolation and extrapolation. The interpolation setting focuses on completing the missing facts in history while the extrapolation setting aims to predict the facts happening in the future. For TKGs, the extrapolation task is much more challenging and has great practical significance for various downstream applications, such as medical aided diagnosis system [\[1\]](#page-11-0), [\[2\]](#page-11-1), traffic flow prediction [\[3\]](#page-12-0) and stock prediction [\[4\]](#page-12-1). Therefore, this paper

![](_page_0_Figure_12.jpeg)

Fig. 1. An illustrative example highlighting the importance of capturing the historical information related to the query. The red arrows represent the most important facts associated with the query.

focuses on extrapolation tasks that explore future unknown facts forecasting.

Accurate predictions of future facts require a comprehensive understanding of the patterns of development of historical facts. According to human cognition of the development of historical facts [\[5\]](#page-12-2)–[\[7\]](#page-12-3), predicting future facts involves the exploration of two historical patterns: the repetition or cycling of historical facts and the evolution of recent adjacent facts. Many efforts for TKG extrapolation have been made toward learning the facts repeating and cyclic patterns by global historical information and modeling the adjacent fact evolution patterns by local historical information.

The studies of the historical fact repeating or cyclic pattern such as CyGNet [\[8\]](#page-12-4), aims to extract global repetition historical information for different queries in a heuristic way. This method leads to the narrow results that the predictions often lean towards the most frequently occurring facts. The research on historical adjacent fact evolution pattern focuses on local historical facts temporal dependency modeling such as RE-GCN [\[9\]](#page-12-5) and TANGO-Tucker [\[10\]](#page-12-6), but lacks the capture of global historical information. Recently, some methods have tried to consider capturing both global and local historical

<sup>∗</sup>Corresponding author: Yuting Wu.

patterns, such as TiRGN [\[11\]](#page-12-7) and HIPNet [\[12\]](#page-12-8), which integrate global and local final prediction results to restrict the prediction range and achieve promising performance. Yet, the performance of these methods is limited due to the following two challenges:

![](_page_1_Figure_1.jpeg)

Fig. 2. The Comparison results of REGCN [\[9\]](#page-12-5), TiRGN [\[11\]](#page-12-7) and our LogCL change after adding gaussian noise on ICEWS14 and ICEWS18 datasets. Light green shading, light red shading, and light blue shading indicate the variation range of LogCL, TiRGN, and REGCN, respectively.

The importance of historical information related to the query is neglected during the process of encoding historical facts. Most extrapolation methods on TKGs model the evolution of entities and relations by the order of time and argue that the KG snapshot facts closer to the query time are more important to predict the query. However, the entities in the query may not appear in all historical KG snapshots, which results in each snapshot taking on a different role in predicting the query. As shown in Fig. 1, for the query (China, Cooperate, ?, tq), the entity China does not appear and is not directly related to other facts in t<sup>q</sup> − 2 KG snapshot, which provides little help for the prediction of the query. The facts containing the China entity in t<sup>q</sup> − 2 KG snapshot appear earlier but are more helpful for predicting the query than t<sup>q</sup> − 2 KG snapshot. With the example in Fig. 1, we find that the historical facts in each KG snapshot are not always crucial for prediction. Existing approaches lack essential patterns for capturing the important historical facts related to queries in the KG snapshot, impairing the ability to accurately predict future facts. So finding a way to filter the irrelevant KG snapshots based on the queries is much critical to improve the performance of TKG reasoning.

The weak anti-noise ability exists in existing methods that cannot effectively guarantee accurate predictions when the inputs adjoint noise. Mainstream TKG reasoning methods focus on how to model historical information and improve the accuracy of predictions. Nevertheless, the robustness of the model as a key important property to ensure the correct prediction results is rarely considered for TKG reasoning. In practice, during the process of training, the input data may encounter different noise interference, which leads to a significant degradation in prediction performance and even generates wrong prediction results. To further elaborate on the challenge mentioned above, we conduct experiments to simulate scenarios where the inputs are perturbed by adding Gaussian noise on both the classical RE-GCN model and TiRGN model. The results shown in Fig. 2, it is observed that both REGCN and TiRGN models suffer varying degrees of performance degradation when Gaussian noise is added, especially the MRR of REGCN model on ICEWS14 and ICEWS18 datasets are reduced by 63.8% and 66.4%, respectively. This indicates that the existing TKG method is weak in resisting the interference of noise. Therefore, how to effectively improve the robustness of the model to ensure correct prediction results is of great significance.

To address the above challenges, we propose a novel Localglobal history-aware Contrastive Learning (LogCL) based on encoder-decoder structure for TKG reasoning, which leverages contrastive learning to guide the fusion of local and global historical information and effectively enhance the robustness of the model. Specifically, during the model encoding phase, we propose an entity-aware attention to flexibly learn queryrelated local and global historical information, thus forming a local entity-aware attention recurrent encoder and a global entity-aware attention encoder (First challenge). Inspired by the unsupervised contrastive learning [\[13\]](#page-12-9), we design a localglobal query contrast module to alleviate the interference brought by external noise to the model, which greatly improves the anti-noise ability of the model (Second challenge). As shown in Fig. 2, LogCL performs better than REGCN and TiRGN in the face of noise interference. In the final decoding part, we achieve entity prediction by fusing local and global historical information.

In general, this work presents the following contributions:

- We propose a novel TKG extrapolation model that uses contrastive learning to better guide the fusion of global and local historical information, and enhance the robustness of LogCL. To the best of our knowledge, LogCL is the first model to leverage local-global history-aware contrastive learning to improve model robustness in TKG reasoning.
- We propose entity-aware attention applied to encode local and global historical information in an elegant way, which captures the importance of historical facts related to queries in KG snapshots.
- Extensive experiments on four public datasets demonstrate that our proposed method shows better and more robust performance than the state-of-the-art baselines.

The rest of this paper is organized as follows. We first review the related work in Section II. Then we describe the notation and problem statement, and introduce our proposed LogCL model in Section III. Next, we report and analyze the experimental results in Section IV. Finally, Section V concludes our paper.

### II. RELATED WORK

In this section, a review of the related work is presented, which includes KG reasoning methods and contrastive learning.

# *A. Reasoning on KGs*Reasoning on KGs has been a hot research topic that infers unknown facts based on known facts. Existing reasoning methods over KGs can be divided into two categories: static KG (SKG) reasoning and temporal KG reasoning.
*1) Static KG reasoning:*Reasoning on SKG focus on static knowledge modeling, which can be roughly divided into four categories [\[14\]](#page-12-10)–[\[16\]](#page-12-11): translation-based methods, matrix factorization methods, convolutional neural network (CNN)-based methods and graph neural network (GNN)-based methods. Translation-based methods such as TransE [\[17\]](#page-12-12) and TransH [\[18\]](#page-12-13), which learn embedded representations of entities and relations in a low-dimensional vector space. Matrix factorization methods including DistMult [\[19\]](#page-12-14) and CompIEx [\[20\]](#page-12-15), which adopt tensor/matrix factorization to obtain the latent representation of entities and relations. CNN-based methods such as ConvE [\[21\]](#page-12-16) and Conv-TransE [\[22\]](#page-12-17), which utilize CNNs to capture the interactions between entities and relations. GNNbased methods, such as R-GCN [\[23\]](#page-12-18), CompGCN [\[24\]](#page-12-19) and KBGAT [\[25\]](#page-12-20), which utilize GNNs to capture the structured semantic features of graphs. SKG reasoning methods have high efficiency in processing static knowledge. However, SKG reasoning methods do not take temporal information into consideration, which makes it difficult to model dynamic facts.
*2) Temporal KG reasoning:*Reasoning over TKGs involves two settings: interpolation and extrapolation. The interpolation of TKGs infers the missing facts at historical timestamps. Most research works are based on the extension of SKG reasoning methods. For example, TTransE [\[26\]](#page-12-21) extends the scoring function based on the idea of TransE [\[17\]](#page-12-12) and adds temporal constraints between facts that share entities. HyTE [\[27\]](#page-12-22) considers timestamps as time-related hyperplanes and generates time-aware representations by projecting the entities and relations into time-related hyperplanes. TNTComplEx [\[28\]](#page-12-23) extends the idea of tensor factorization and proposes a 4thorder tensor factorization to obtain the time-aware representations of entities. Since these methods do not involve the evolution of facts over time, they are not suitable for modeling the entity representations in future unseen timestamps.

TKG extrapolation aims to predict facts at future timestamps. According to the law of human development of history cognition mainly involves two historical patterns: the repetition or cycling of historical facts and the evolution of recent adjacent facts. The former [\[8\]](#page-12-4), [\[29\]](#page-12-24) explores the repetition of facts related to queries from a global perspective. For example, CyGNet [\[8\]](#page-12-4) and CENET [\[29\]](#page-12-24) adopt a copy-generation mechanism to obtain the global repetition of one-hop facts, facilitating future entity reasoning. The latter [\[9\]](#page-12-5), [\[10\]](#page-12-6), [\[30\]](#page-12-25)–[\[33\]](#page-12-26) aims to study the local historical facts temporal dependency. For example, RE-GCN [\[9\]](#page-12-5) models the evolution of entities and relations at each timestamp by using the local historical dependency. CEN [\[33\]](#page-12-26) utilizes online learning strategies to deal with time-variability issues. GHT [\[34\]](#page-12-27) designs two Transformer modules [\[35\]](#page-13-0) to capture instantaneous structural information and temporal evolution information, respectively, and presents a novel relational continuous-time encoding function to facilitate feature evolution with Hawkes processes. TECHS [\[36\]](#page-13-1) encodes the topology and temporal dynamics by using heterogeneous attention and leverages both propositional and first-order reasoning to make predictions. Recent methods such as TiGRN [\[11\]](#page-12-7) and HIPNet [\[12\]](#page-12-8), attempt to integrate local and global historical information to obtain more accurate results. Nevertheless, these approaches fail to model the importance of historical facts related to queries in KG snapshots. This makes it difficult to distinguish the significance of each KG snapshot for predicting the query. To address this dilemma, we propose an entity-aware attention mechanism to flexibly model the KG snapshots that are relevant and irrelevant to the queries.

##*B. Contrastive Learning*Contrastive Learning as a self-supervised learning paradigm, due to its impressive performance in distinguishing instances of different categories, has gained significant attention in recent years. The basic idea of contrastive learning [\[13\]](#page-12-9), [\[37\]](#page-13-2) is to learn the similarity between different views of the same instances through training, while maximizing the dissimilarity between different views of instances. In selfsupervised contrastive learning, the augmented instances are derived by randomly sampling a mini-batch of N instances. The origin instances and the augmented instances are used to optimize the following loss function given a pair of positive instances (i, j). The contrastive loss is expressed as:

$$
\mathcal{L}_{i,j} = -\log \frac{\exp (\mathbf{x}_i \cdot \mathbf{x}_j / \tau)}{\sum_{k=1, k \neq i}^{2N} \exp (\mathbf{x}_i \cdot \mathbf{x}_k / \tau)},
$$
(1)

where 2N is the sum of the number of the original and augmented instances, x<sup>i</sup> is the projection embedding of the instance i, τ is a temperature parameter helping the model learn from hard negatives, and · is dot product that is used to compute the similarity of instances between different views. Recently, contrastive learning has been applied to static KG reasoning to alleviate the long-tail data problem but is rarely explored in TKG reasoning. The recent CENET [\[29\]](#page-12-24) is a single-view historical contrastive learning method designed to enhance the representation of entities with less historical interactions. Different from CENET, we propose a localglobal query contrast module to mitigate noise interference and enhance model robustness.

### III. OUR APPROACH

In this section, we will first introduce basic notations and definitions used in this paper and present the problem statement for the extrapolation of TKG, and then describe the framework and training optimizations of LogCL in detail.

####*A. Notations and Definitions*A TKG G is formalized as a sequence of KG snapshots, i.e., G = {G1, G2, ..., G|T |}. Each KG snapshot G<sup>t</sup> = (E, R, Ft) actually is a directed multi-relational graph that is a set of valid facts at t. A fact (or an event) is denoted as a quadruple (es, r, eo, t) where the subject entity e<sup>s</sup> ∈ E and the object

![](_page_3_Figure_0.jpeg)

Fig. 3. The overall architecture of LogCL, consists of three components: local entity-aware attention recurrent encoder, global entity-aware attention historical encoder, and local-global query contrast module.

TABLE I SUMMARY OF PRIMARY NOTATIONS.

| Notations   | Descriptions                                                  |
|-------------|---------------------------------------------------------------|
| G           | A TKG                                                         |
| Gt          | A KG snapshot composed of facts at t                          |
| Gg          | Global historical query subgraph                              |
| Ft          | Set of valid facts at t                                       |
| E, R, T     | Set of entities, relations and times in G                     |
| E ,  R ,  T | The number of entities, relations and times                   |
| d           | Embedding dimensionality                                      |
| m           | Length of the local KG snapshot sequence                      |
| H0          | 背<br>景<br>Randomly initialized embedding matrices of entities |
| R0          | Randomly initialized embedding matrices of realtions          |
| Ht          | Embedding matrices of entities at t                           |
| Rt          | Embedding matrices of relations at t                          |
| Hg          | 研究动机<br>Global embedding matrices of entities                 |

entity e<sup>o</sup> ∈ E is connected by a relation r ∈ R at time t ∈ T . The primary notations and their meanings used in this paper are described in Table I.**选题思路及研究 内容 主要方法**TKG extrapolation task involves forecasting a missing object entity (or subject entity ) given a query (eq, rq, ?, tq) (or (?, rq, eq, tq)) according to previous historical KG snapshots {G0, G1, ..., G<sup>t</sup>q−1}. Without loss of generality, the inverse relation quadruples (eo, r<sup>−</sup><sup>1</sup> , es, t) are added to the TKG dataset. So the TKG extrapolation task can be reduced to object entities predictions.**实验结果**####*B. Architecture Overview*As shown in Fig. 3, the overall framework of LogCL is composed of three components: global entity-aware attention encoder, local entity-aware recurrent encoder and local-global query contrast module. Local entity-aware attention recurrent encoder adopts an entity-aware attention mechanism to capture the necessary information related to queries for prediction. If facts in KG snapshots at the latest timestamps contain semantic information relevant to the queries, these facts will help to improve the probability of entity prediction. Global entity-aware attention encoder takes into account the global historical facts related to queries and avoids overlooking important historical facts that do not appear in the recent local KG snapshots. Local-global query contrast module is introduced to guide a better integration of global and local historical information and to enhance the robustness of LogCL. Finally, LogCL combines local and global historical embedding representations for entity prediction.

![](_page_3_Figure_9.jpeg)

Fig. 4. The architecture of our proposed global entity-aware attention encoder and local entity-aware attention recurrent encoder.

####*C. Local Entity-Aware Attention Recurrent Encoder*As discussed in the introduction, each KG snapshot at the latest m timestamp (i.e. {G<sup>t</sup>q−m+1, ..., G<sup>t</sup>q−1}) doesn't provide equally contributions for predicting the query q = (e<sup>t</sup><sup>q</sup> , r<sup>t</sup><sup>q</sup> , ?, tq). The importance of KG snapshot historical information relevant to the query needs to be modeled to further optimize the evolution of entity and relation in adjacent time. To this end, we propose a local entity-aware attention recurrent encoder that efficiently captures historical information in KG snapshots relevant to the query. The local entityaware attention recurrent encoder involves a KG snapshot aggregation pipeline and a KG snapshot sequences evolution pipeline. Specifically, the aggregation of the KG snapshot is to learn the spatial semantic structure of concurrent facts by the Graph Convolution Network (GCN) from the spatial view, while the evolution of KG snapshot sequences is to capture sequential dependencies of entities and relations through the recurrent mechanism from the temporal view. Note that, the inputs to entities and relations on the first timestamp are randomly initialized.
*1) KG Snapshot Aggregation:*For KG snapshots on each timestamp, we update the representation of entities by capturing the spatial structural semantics information among concurrent facts. Considering that some facts in KG snapshots occur cyclically, such as periodic meetings, we first follow [\[38\]](#page-13-3) to encode the time numerical information to obtain the dynamic entities embedding. Formally, the dynamic entities embedding as follows:

$$
\varphi(d) = \cos\left(dw_t + b_t\right),\tag{2}
$$

$$
\vec{\mathbf{h}}_t = W_0[\mathbf{h}_t \| \varphi(d)],\tag{3}
$$

where d = t<sup>q</sup> − t<sup>i</sup> is the time interval that is modeled by rescaling a learnable time unit w<sup>t</sup> with a time bias bt. cos(·) is a periodic activation function, ∥ is the vector concatenation operation, W<sup>0</sup> is a linear transformation matrix, and ⃗h<sup>t</sup> ∈ H⃗ t is the dynamic embedding of entity at timestamp t. Then, we utilize an R-GCN [\[23\]](#page-12-18) to capture the structure dependencies among concurrent facts. Note that, the R-GCN can be replaced by other relation-aware GCNs, such as CompGCN [\[24\]](#page-12-19) and KBGAT [\[25\]](#page-12-20). The entity-aggregating R-GCN aggregator is defined as:

$$
\vec{\mathbf{h}}_{t,o}^{(l+1)} = \text{RGCN}_{Local}(\vec{\mathbf{h}}_{t,s}^{(l)}, \mathbf{r}^{(l)}, \vec{\mathbf{h}}_{t,o}^{(l)}) \n= \sigma_1 \left( \frac{1}{c_o} \sum_{(e_s,r), \exists (e_s,r,e_o) \in \mathcal{E}_t} \mathbf{W}_1^{(l)} \left( \vec{\mathbf{h}}_{t,s}^{(l)} + \mathbf{r}^{(l)} \right) + \mathbf{W}_2^{(l)} \vec{\mathbf{h}}_{t,o}^{(l)} \right),
$$
\n(4)

where ⃗h l <sup>t</sup> ∈ R |E|×d , r l <sup>t</sup> ∈ R |R|×<sup>d</sup> denote the embedding of entities and relations in the l-th layers of the R-GCN in each KG snapshot at t-th timestamp, separately. For simplicity, the final layer of the output of R-GCN is denoted as H Agg t . c<sup>o</sup> is a normalization constant that equals the in-degree of entity, W<sup>1</sup> and W<sup>2</sup> are the parameters for aggregating features and self-loop in the l-th layer, and σ1(·) is the RReLU activation function.
*2) KG Snapshot Sequence Evolution:*After obtaining the structural semantic embedding of entities in each KG snapshot, it needs to further model the sequential dependencies of entities and relations in KG snapshot sequences at the latest m timestamps. We progressively update the representations of entities by a gated recurrent unit (GRU) [\[39\]](#page-13-4) which is a flexible and efficient recurrent mechanism modeling short sequences. The entity-oriented GRU can be represented as:

$$
\mathbf{H}_{t+1} = \text{GRU}_{\text{Ent}}\left(\mathbf{H}_t, \mathbf{H}_t^{Agg}\right),\tag{5}
$$

where H Agg t is the entity embedding matrix after KG snapshot aggeration at t. As for relation, we follow [\[9\]](#page-12-5) that considers r-related entities and the corresponding relation embedding to obtain R′ t at t KG snapshot. Thus, a time gate unit is adopted to update the relation embedding at t. Formally,

$$
\mathbf{r}'_t = f_{ave}(\mathbf{H}_{t,r}) + \mathbf{r},\tag{6}
$$

$$
\mathbf{R}_{t+1} = \mathbf{U}_t \cdot \mathbf{R}'_t + (1 - \mathbf{U}_t) \cdot \mathbf{R}_t, \tag{7}
$$

$$
\mathbf{U}_{t} = \sigma_{2} \left( \mathbf{W}_{3} \mathbf{R}'_{t} + \mathbf{b} \right), \tag{8}
$$

where fave(·) is the mean pooling operation, Ht,r is the embedding of entities connected to r at t, R′ t consists of r ′ t at t, Rt+1 is the finally updated through a time gate U<sup>t</sup> ∈ R<sup>d</sup>×<sup>d</sup> , W<sup>3</sup> is the learnable weight matrice of the time gate, and σ2(·) is the sigmoid activate function.

After the above operations, we obtain the entity evolution representations {Htq−m+2, ..., Ht<sup>q</sup> } and the relation evolution representations {Rtq−m+2, ..., Rt<sup>q</sup> } at the latest m timestamps. However, these evolutionary representations do not take into account the contribution of historical facts related to queries in the KG snapshots for predicting the query. Thus, we propose an entity-aware attention mechanism to distinguish the importance of different KG snapshots for queries. We first exploit the mean pooling applied on all relation embedding associated with the entity in q at timestamps tq, and then compute the final local entity representation via the entityaware attention mechanism. The operation is as follows,

$$
\mathbf{h}_{t_q}^{e_q} = W_4[f_{ave}(\mathbf{r}_{t_q})||\mathbf{h}],\tag{9}
$$

$$
\alpha_i = \sigma_2(W_5 \left( \mathbf{h}_{t_q - m + i}^{Agg} + \mathbf{h}_{t_q}^{e_q} \right)) \quad i \in [1, m - 1], \tag{10}
$$

$$
\vec{\mathbf{h}}_{t_q}^{e_q} = \mathbf{h}_{t_q} + \sum_{i=2}^{m} \alpha_i \mathbf{h}_{t_q - m + i},\tag{11}
$$

where α<sup>i</sup> is the attention score of KG snapshots, W<sup>4</sup> and W<sup>5</sup> are the learnable weight matrices, σ<sup>2</sup> is the softmax acitvate function, and ⃗h eq tq is the final local presentation at timestamp t<sup>q</sup> after local entity-aware attention recurrent encoder. In this way, LogCL can effectively model KG snapshot information related to queries at the latest m timestamps, providing more accurate prediction results.

####*D. Global Entity-Aware Attention Encoder*The global entity-aware attention encoder aims to capture the longer historical facts that are not considered in the local KG snapshot sequence. For each query (eq, rq, ?, tq), unlike CyGNet [\[8\]](#page-12-4) and TiRGN [\[11\]](#page-12-7) that only use one-hop target object entities associated with queries to learn the repetition of facts in further history, we consider candidate multi-hop historical facts that provide more semantic information of historical facts to help entities prediction. For example, meetings that are held periodically are preceded by different hosting processes, and these different hosting processes can be of great help to future meetings. Therefore, we construct the historical query subgraph by sampling the historical facts relevant to queries to obtain rich semantic information.

For a TKG G<t<sup>q</sup> = {G1, G2, ..., G<sup>t</sup>q−1}, we first sample the one-hop historical facts G ′ g1 containing the query subject entity s in the given query. Next, we extract the one-hop target object entity associated with the query entity-relation pair, and then proceed to sample the one-hop facts G ′ g2 containing the one-hop target object entity. Finally, we integrate the two collected historical fact sets to obtain the most relevant historical subgraph to the query, G ′ <sup>g</sup> = G ′ g1 ∪ G′ g2 . It is worth noting that, the historical query subgraph is a static KG that does not involve temporal information and can change along the query time.

After obtaining the historical query subgraph, we update the global entity representation by modeling the structural semantic representation of the historical query subgraph. To encode the historical query subgraph that is formed by sampling twohop neighbors, we adopt another R-GCN to perform message aggregation. Since the historical query subgraph does not consider temporal information, we directly use the randomly initialized embedding of entities and relations as input to R-GCN. The specific formula is expressed as follows:

$$
\mathbf{h}_{g}^{l+1} = \text{RGCN}_{\text{Global}}\left(\mathbf{h}_{g,e_s}^{l}, \mathbf{r}^{l}, \mathbf{h}_{g,e_o}^{l}\right),\tag{12}
$$

where h l+1 <sup>g</sup> denotes the output embedding of entities in the l-th layers of the R-GCN in the historical query subgraph. For simplicity, the final layer of the output of R-GCN is denoted as HAgg g . For global historical information, we also use the entity-aware attention mechanism to learn the historical facts related to queries. The specific formula is expressed as follows:

$$
\beta = \sigma_2(W_6\left(\mathbf{h}_g^{Agg} + \mathbf{h}\right)),\tag{13}
$$

$$
\vec{\mathbf{h}}_g^{e_q} = \beta \mathbf{h}_g^{Agg},\tag{14}
$$

where the β is the attention score, W<sup>6</sup> is the learnable weight matrice, and ⃗h eq <sup>g</sup> denotes the final global representation of entities through global entity-aware attention encoder.

####*E. Local and Global Historical Contrastive Learning*Clearly, the local and global encoders defined above well capture the local and global dependency for queries. However, during the actual training process, the input data is disturbed by extraneous noise, leading to a sharp decline in reasoning performance. Existing methods cannot address this challenge well. Inspired by the unsupervised contrastive learning [\[13\]](#page-12-9), [\[29\]](#page-12-24), we propose a local-global query contrast module that identifies highly correlated local and global features of entities and relations at the query level, enabling noise filtering. Specifically, for each query at timestamp tq, The purpose of the local-global query contrast module is to learn the local and global contrastive representations of queries by minimizing the supervised contrastive loss, which makes the local and global representations of the same query to be as close as possible in the semantic space, while different queries are separated. Formally, Formally, the query embedding representations of local and global are obtained by using the concatenation operation:

$$
\mathbf{z}_t = MLP[\mathbf{h}_t^{Agg} || \mathbf{r}_t], \tag{15}
$$

$$
\mathbf{z}_g = MLP[\mathbf{h}_g^{Agg} || \mathbf{r}], \tag{16}
$$

where z<sup>t</sup> is the representation of the local query at timestamp t, z<sup>g</sup> is the representation of the global query, and MLP is used to normalize and project the embedding of queries onto the unit sphere for further contrastive training. It is worth noting that since the historical query subgraph does not consider temporal information, the origin relation embeddings are used to encode the global embedding representation of queries.

In our work, the global and local query representations can be considered as the two-view representations derived from encoding historical facts in TKGs. Thus, if taking the query representation generated by the local encoder as the anchor, the global encoder can be viewed as an augmented encoding process. The local and global representations of the same query are used as positive pairs at timestamp t, i.e.,(zt,i, zg,i), the local and global of representation of different queries are used as negative pairs i.e.,(zt,i, zg,k). Formally, the computation of the supervised contrastive loss Llg at timestamp t<sup>q</sup> is as follows:

$$
\mathcal{L}_{lg} = \frac{1}{|Q_{t_q}|} \log \frac{\exp (\mathbf{z}_{t,i} \cdot \mathbf{z}_{g,i}/\tau)}{\sum_{k \in N_{t_q}, k \neq i} (\mathbf{z}_{t,i} \cdot \mathbf{z}_{g,k}/\tau)},
$$
(17)

where Qt<sup>q</sup> and Nt<sup>q</sup> denote the minibatch that is the set of queries and the number of queries at timestamp tq, separately; τ is the temperature parameter. The objective of Llg is to make the representations of the same category closer, enhancing the common essential features of the local and global encoders required for predicting the query, thus alleviating the influence of noise and improving the robustness of the model. Similarly, the supervised loss Lgl can be obtained by using the representation generated by the global encoder as an anchor. To make the LogCL further distinguish different semantic representations of queries in the semantic space, we adopt Eq. 17 to constrain the local and global query representations and obtain two supervised losses Lll and Lgg. In this way, we can obtain the four supervised contrastive losses: Llg, Lgl, Lll and Lgg. Thus, the final supervised contrastive loss is computed as Lcl = (Llg + Lgl + Lll + Lgg)/4.

####*F. Prediction and Optimization*ConvTransE [\[22\]](#page-12-17) is a strong score function that is widely adopted for the recent TKG reasoning task. In this work, we also adopt ConvTransE to perform the entity prediction task at timestamp tq. Therefore, the entity prediction score of ConvTransE is as follows:

$$
\phi(e_q, r_q, e, q) = \sigma_2 \left( \mathbf{h}_{t_q}^{e_q} \operatorname{ConvTransE} \left( \hat{\mathbf{h}}_{t_q}^{e_q}, \mathbf{r}_{t_q} \right) \right), \quad (18)
$$
$$
\hat{\mathbf{h}}_{t_q}^{e_q} = \lambda \vec{\mathbf{h}}_{g}^{e_q} + (1 - \lambda) \vec{\mathbf{h}}_{t_q}^{e_q}, \quad (19)
$$

where λ is a variable factor that is set at [0,1], which is used to trade off global and local representations of entities. In this paper, the entity prediction task can be considered as a multilabel learning problem. Thus, the loss of entity prediction Ltkg is formalized as:

$$
\mathcal{L}_{tkg} = \sum_{t=0}^{\mathcal{T}} \sum_{(e_s, r, e, t) \in \mathcal{F}_t} \sum_{e \in \mathcal{E}} y_t^e \log \phi(e_s, r, e, t), \qquad (20)
$$

where ϕ (es, r, e, t) is the entity prediction probabilistic scores. y e <sup>t</sup> ∈ R |E| is the label of which the element is 1 if the fact occurs, otherwise 0. The final loss function is computed as:

$$
\mathcal{L} = \mathcal{L}_{tkg} + \mathcal{L}_{cl}.
$$
 (21)

In the work, the contrastive supervised loss Lcl and the entity prediction of loss Ltkg are trained simultaneously.

Note that, since reverse quadruples are added in the training or testing process, the inverse query sets are generated by the original query sets at timestamp tq. During each epoch, the KG snapshots in history are built using the combination of the original quadruples and the inverse quadruples. If the combination sets are directly used for training, the entityaware attention will perceive the target subject entity and target object entity, resulting in data leakage. To avoid such potential data leakage, we present a two-phase forward propagation strategy. In detail, the original query set is first considered in the forward propagation, and then the second forward propagation is performed on the query inverse sets during each epoch. In this way, the prediction scores and loss can be obtained for training or testing from the two-phase forward propagation. The detailed training procedure of LogCL is summarized in Algorithm 1.

####*G. Complexity Analysis*We analyze the computational complexity of our proposed LogCL model. For the local entity-aware attention recurrent encoder, the time complexities of entity and relation evolution are O(m(|E| + P)) and O(m|R|), respectively, where P is the complexity of entity attention mechanism at t timestamp. For the global entity-aware encoder, the time complexity of generating the historical query subgraph is O(2|T ||Ft|), the time complexity of historical query subgraph aggregation is O(|E| + P). The time complexity of the local-global query contrast module is O(4mC). Thus, the time complexity of LogCL is O(m(|E + R + P|) + |E| + P + 2|T ||Ft| + 4mC).

#### IV. EXPERIMENTS

In this section, we conduct many experiments to evaluate LogCL on four public datasets, and analyze the experimental results in detail.

####*A. Datasets and Baselines*

*1) Datasets:*To evaluate LogCL on entity prediction task, we adopt four benchmark datasets that are widely used for TKG extrapolation, including ICEWS14, ICEWS18, ICEWS05-15 [\[40\]](#page-13-5) and GDELT [\[41\]](#page-13-6). ICEWS14, ICEWS18 and ICEWS05-15 are subsets generated from Integrated Crisis

#### Algorithm 1: Training procedure of LogCL

Input: the historical KG snapshot sequence

{G1, G2, ..., G<sup>t</sup><sup>q</sup> }, query set Qquery with unknown object entities at time tq.

- Output: The reasoning results for each query are in descending order of scores.
- 1: Initialize the embeddings of entities, relations.
- 2: while t < |T | do
- 3: t ′ = t<sup>q</sup> − m
- 4: while t ′ < t<sup>q</sup> and t ′ <sup>q</sup> > 0 do
- 5: t ′ = t ′ + 1
- 6: Aggregate local KG snapshot by Eq.2-Eq.4.
- 7: Learn KG snapshot sequence evolution and obtain the presentation of entities and relations by Eq.5-Eq.11.

#### 8: end while

- 9: Aggregate global query subgraph and obtain the representation of entities by Eq.12-Eq.14.
- 10: t ′′ = t − m
- 11: while t ′′ < t and t ′′ > 0 do
- 12: t ′′ = t ′′ + 1
- 13: Compute the local-global query contrast loss by Eq.15-Eq.17.
- 14: end while
- 15: Replace the missing object entities for each query (s, r, ?, t) ∈ Qquery and calculate the scoring function by Eq.18-Eq.21.
- 16: t = t + 1
- 17: end while

TABLE II DETAILS OF THE TKG DATASETS.

| Dataset              |          |          | ICEWS14 ICEWS18 ICEWS05-15 GDELT |           |
|----------------------|----------|----------|----------------------------------|-----------|
| Entities             | 6,869    | 10,094   | 23,033                           | 7,691     |
| Relations            | 230      | 256      | 251                              | 240       |
| Training             | 74,845   | 373,018  | 368,868                          | 1,734,399 |
| Validation           | 8,514    | 45,995   | 46,302                           | 238,765   |
| Test                 | 7,371    | 49,545   | 46,159                           | 305,241   |
| Time granularity     | 24 hours | 24 hours | 24 hours                         | 15 mins   |
| Snapshot numbers 365 |          | 365      | 4017                             | 2975      |

Early Warning System (ICEWS) [1](#page-6-0) , which contains a large number of political events with specific timestamps. GDELT [2](#page-6-1) is a subset generated from the Global Database of Events, Language datasets, which contains 20 of types events (e.g. Make a public statement, Appeal and consult). We follow the preprocessing strategy [\[9\]](#page-12-5), [\[30\]](#page-12-25) to split all datasets into training, validation, and test sets with the proportions of 80%/10%/10%. The statistics of all datasets are provided in Table II.
*2) Baselines:*To demonstrate the effectiveness of LogCL for TKG reasoning, we compare LogCL with 20 up-to-date

<span id="page-6-0"></span><sup>1</sup>http://www.icews.com/

<span id="page-6-1"></span><sup>2</sup>https://www.gdeltproject.org/

| TABLE III                                                                                      |
|------------------------------------------------------------------------------------------------|
| THE PREDICTION PERFORMANCE OF MRR AND HITS@1/3/10 ARE ON ALL DATASETS WITH TIME-AWARE METRICS. |

| ICEWS14       |                           |       |       |       |       | ICEWS18 |       |       |                                                                                                         | ICEWS05-15 |       |       |       | GDELT |       |       |       |
|---------------|---------------------------|-------|-------|-------|-------|---------|-------|-------|---------------------------------------------------------------------------------------------------------|------------|-------|-------|-------|-------|-------|-------|-------|
|               | Model                     |       |       |       |       |         |       |       | MRR Hits@1 Hits@3 Hits@10 MRR Hits@1 Hits@3 Hits@10 MRR Hits@1 Hits@3 Hits@10 MRR Hits@1 Hits@3 Hits@10 |            |       |       |       |       |       |       |       |
| Static        | DisMult (2014)            | 15.44 | 10.91 | 17.24 | 23.92 | 11.51   | 7.03  | 12.87 | 20.86                                                                                                   | 17.95      | 13.12 | 20.71 | 29.32 | 8.68  | 5.58  | 9.96  | 17.13 |
|               | ComplEx (2016)            | 32.54 | 23.43 | 36.13 | 50.73 | 22.94   | 15.19 | 27.05 | 42.11                                                                                                   | 32.63      | 24.01 | 37.50 | 52.81 | 16.96 | 11.25 | 19.52 | 32.35 |
|               | ConvE (2018)              | 35.09 | 25.23 | 39.38 | 54.68 | 24.51   | 16.23 | 29.25 | 44.51                                                                                                   | 33.81      | 24.78 | 39.00 | 54.95 | 16.55 | 11.02 | 18.88 | 31.60 |
|               | Conv-TransE (2019)        | 33.80 | 25.40 | 38.54 | 53.99 | 22.11   | 13.94 | 26.44 | 42.28                                                                                                   | 33.03      | 24.15 | 38.07 | 54.32 | 16.20 | 10.85 | 18.38 | 30.86 |
|               | RotatE (2019)             | 21.31 | 10.26 | 24.35 | 44.75 | 12.78   | 4.01  | 14.89 | 31.91                                                                                                   | 24.71      | 13.22 | 29.04 | 48.16 | 13.45 | 6.95  | 14.09 | 25.99 |
|               | TTransE (2016)            | 13.72 | 2.98  | 17.70 | 35.74 | 8.31    | 1.92  | 8.56  | 21.89                                                                                                   | 15.57      | 4.80  | 19.24 | 38.29 | 5.50  | 0.47  | 4.94  | 15.25 |
|               | TA-DisMult (2018)         | 25.80 | 16.94 | 29.74 | 42.99 | 16.75   | 8.61  | 18.41 | 33.59                                                                                                   | 24.31      | 14.58 | 27.92 | 44.21 | 12.00 | 5.76  | 12.94 | 23.54 |
| Interpolation | DE-SimIE (2020)           | 33.36 | 24.85 | 37.15 | 49.82 | 19.30   | 11.53 | 21.86 | 34.80                                                                                                   | 35.02      | 25.91 | 38.99 | 52.75 | 19.70 | 12.22 | 21.39 | 33.70 |
|               | TNTCompIEx (2020)         | 34.05 | 25.08 | 38.50 | 50.92 | 21.23   | 13.28 | 24.02 | 36.91                                                                                                   | 27.54      | 9.52  | 30.80 | 42.86 | 19.53 | 12.41 | 20.75 | 33.42 |
|               | RE-NET (2020)             | 36.93 | 26.83 | 39.51 | 54.78 | 28.81   | 19.05 | 32.44 | 47.51                                                                                                   | 43.32      | 33.43 | 47.77 | 63.06 | 19.62 | 12.42 | 21.00 | 34.01 |
|               | CyGNet (2020)             | 35.05 | 25.73 | 39.01 | 53.55 | 24.93   | 15.90 | 28.28 | 42.61                                                                                                   | 36.81      | 26.61 | 41.63 | 56.22 | 18.48 | 11.52 | 19.57 | 31.98 |
|               | TANGO-Tucker (2021) 36.80 |       | 27.43 | 40.89 | 54.93 | 28.68   | 19.35 | 32.17 | 47.04                                                                                                   | 42.86      | 32.72 | 48.14 | 62.34 | 19.53 | 12.43 | 20.79 | 33.19 |
|               | xERTE (2021)              | 40.02 | 32.06 | 44.63 | 56.17 | 29.98   | 22.05 | 33.46 | 44.83                                                                                                   | 46.62      | 37.84 | 52.31 | 63.92 | 18.09 | 12.30 | 20.06 | 30.34 |
|               | TITer (2021)              | 40.87 | 32.28 | 45.45 | 57.10 | 29.98   | 22.05 | 33.46 | 44.83                                                                                                   | 47.69      | 37.95 | 52.92 | 65.81 | 15.46 | 10.98 | 15.61 | 24.31 |
| Extrapolation | RE-GCN (2021)             | 40.39 | 30.66 | 44.96 | 59.21 | 30.58   | 21.01 | 34.34 | 48.75                                                                                                   | 48.03      | 37.33 | 53.85 | 68.27 | 19.64 | 12.42 | 20.90 | 33.69 |
|               | CEN (2022)                | 42.20 | 32.08 | 47.46 | 61.31 | 31.50   | 21.70 | 35.44 | 50.59                                                                                                   | 46.84      | 36.38 | 52.45 | 67.01 | 20.39 | 12.96 | 21.77 | 34.97 |
|               | TiRGN (2022)              | 44.04 | 33.83 | 48.95 | 63.84 | 33.66   | 23.19 | 37.99 | 54.22                                                                                                   | 50.04      | 39.25 | 56.13 | 70.71 | 21.67 | 13.63 | 23.27 | 37.60 |
|               | HisMatch (2022)           | 46.42 | 35.91 | 51.63 | 66.84 | 33.99   | 23.91 | 37.90 | 53.94                                                                                                   | 52.85      | 42.01 | 59.05 | 73.28 | 22.01 | 14.45 | 23.80 | 36.61 |
|               | RETIA (2023)              | 42.76 | 32.28 | 47.77 | 62.75 | 32.43   | 22.23 | 36.48 | 52.94                                                                                                   | 47.26      | 36.64 | 52.90 | 67.76 | 20.12 | 12.76 | 21.45 | 34.49 |
|               | CENET (2023)              | 39.02 | 29.62 | 43.23 | 57.49 | 27.85   | 18.15 | 31.63 | 46.98                                                                                                   | 41.95      | 32.17 | 46.93 | 60.43 | 20.23 | 12.69 | 21.70 | 34.92 |
|               | LogCL                     | 48.87 | 37.76 | 54.71 | 70.26 | 35.67   | 24.53 | 40.32 | 57.74                                                                                                   | 57.04      | 46.07 | 63.72 | 77.87 | 23.75 | 14.64 | 25.60 | 42.33 |

KG reasoning methods that cover SKG and TKG reasoning methods (including interpolation and extrapolation). The SKG methods include DisMult [\[19\]](#page-12-14), ConvE [\[21\]](#page-12-16), ComplEx [\[20\]](#page-12-15), Conv-TransE [\[22\]](#page-12-17), RotatE [\[42\]](#page-13-7). The interpolation methods include TTransE [\[26\]](#page-12-21), TA-DisMult [\[43\]](#page-13-8), De-SimIE [\[44\]](#page-13-9), TNT-ComIEx [\[28\]](#page-12-23), TANGO-Tucker [\[10\]](#page-12-6). The extrapolation methods include xERTE [\[32\]](#page-12-28), TITer [\[31\]](#page-12-29), CyGNet [\[8\]](#page-12-4), RE-NET [\[30\]](#page-12-25), RE-GCN [\[9\]](#page-12-5), CEN [\[33\]](#page-12-26), TiRGN [\[11\]](#page-12-7), HisMatch [\[38\]](#page-13-3), RETIA [\[45\]](#page-13-10), and CENET [\[29\]](#page-12-24).

#*B. Experimental Settings*

*1) Evaluation Metrics:*We adopt two evaluation metrics: mean reciprocal rank (MRR) and Hits@k (k=1,3,10), which are widely used to evaluate the effectiveness of TKG reasoning methods. MRR is the average reciprocal value that is used to compute the ranks of the ground truth for all queries, and Hits@k represents the proportion of times that the true entity candidates appear in the top-k of the ranked candidates. Some recent works [\[10\]](#page-12-6), [\[38\]](#page-13-3) point out that the traditional static filtered setting is not suitable for extrapolation on TKG reasoning due to ignoring the time dimension of facts. Actually, only the facts occurring at the same time should be filtered. Therefore, we report the experimental results with the time-aware filtered setting that is widely used in recent works, which only filters out the quadruples occurring at the query time. In addition, all experimental results on MRR and Hits@1/3/10 in this paper are reported as percentages.
*2) Implementation Details:*For all datasets, the embedding size d is set to 200, the learning rate is set to 0.001 and the batch size is set as the number of quadruples in each timestamp. The parameters of LogCL are optimized by using adam [\[46\]](#page-13-11) during training. The layer number of R-GCN on both local entity-aware attention recurrent encoder and global entity-aware attention encoder is set to 2 and the dropout rate for each layer is set to 0.2. The optimal local historical KG snapshots sequences lengths of ICEWS14, ICEWS18, ICEWS05-15, GDELT are set to 7, 7, 9 and 7, respectively. We follow works [\[9\]](#page-12-5), [\[11\]](#page-12-7), [\[45\]](#page-13-10) that add static KG information on ICEWS14, ICEWS18 and ICEWS05-15 datasets. The prediction weight of all datasets is set to 0.9. The optimal temperature coefficient of ICEWS14, ICEWS18, ICEWS05- 15, GDELT are set to 0.03, 0.03, 0.07 and 0.07. For the decoder on all datasets, the number of kernels is set to 50, the kernel size is set to 2×3, and the dropout rate is set to 0.2.

For SKG reasoning methods, the time dimension is removed on all TKG datasets. Some of the extrapolation baselines, including xERTE [\[32\]](#page-12-28), TANGO-Trucker [\[10\]](#page-12-6), TITer [\[31\]](#page-12-29), REGCN [\[9\]](#page-12-5), CEN [\[33\]](#page-12-26), TiRGN [\[11\]](#page-12-7) and RETIA [\[45\]](#page-13-10), publish their open source code, and their results with the time-aware filter setting are reported under the default parameters. The others are taken from the Hismathch [\[38\]](#page-13-3). For fairness of comparison, results of CEN and RETIA are reported under the offline setting that is adopted to other baselines. We also compare our LogCL with CEN and RETIA models under the online setting and results are reported in the following section*H*.

TABLE IV THE ABLATION STUDY RESULTS OF MRR AND HITS@1/3/10 ON ICEWS14, ICEWS18 AND ICEWS05-15 DATASETS.

| Model            | ICEWS14 |        |        |         |       |        | ICEWS18 |         | ICEWS05-15 |        |        |         |  |
|------------------|---------|--------|--------|---------|-------|--------|---------|---------|------------|--------|--------|---------|--|
|                  | MRR     | Hits@1 | Hits@3 | Hits@10 | MRR   | Hits@1 | Hits@3  | Hits@10 | MRR        | Hits@1 | Hits@3 | Hits@10 |  |
| LogCL            | 48.87   | 37.76  | 54.71  | 70.26   | 35.67 | 24.53  | 40.32   | 57.74   | 57.04      | 46.07  | 63.72  | 77.87   |  |
| LogCL-G          | 44.74   | 33.53  | 50.29  | 66.72   | 30.21 | 18.96  | 34.45   | 52.69   | 51.92      | 40.31  | 58.37  | 74.66   |  |
| LogCL-L          | 46.81   | 35.52  | 52.54  | 68.91   | 35.31 | 24.14  | 39.92   | 57.40   | 56.78      | 45.73  | 63.50  | 77.59   |  |
| LogCL-w/o-eatt   | 40.34   | 30.29  | 44.82  | 60.05   | 31.01 | 20.99  | 34.88   | 50.71   | 46.25      | 35.76  | 51.71  | 66.50   |  |
| LogCL-G-w/o-eatt | 38.61   | 29.04  | 42.79  | 57.42   | 27.83 | 18.56  | 31.11   | 46.30   | 41.40      | 31.20  | 46.44  | 60.93   |  |
| LogCL-L-w/o-eatt | 39.86   | 29.90  | 44.40  | 59.48   | 30.95 | 21.01  | 34.85   | 50.55   | 46.16      | 35.56  | 51.58  | 66.70   |  |
| LogCL-w/o-cl     | 46.84   | 35.62  | 52.44  | 69.05   | 35.32 | 24.04  | 40.00   | 57.62   | 56.85      | 45.83  | 63.61  | 77.81   |  |

![](_page_8_Figure_2.jpeg)

(a) The results of different intensity of noise in ICEWS14 dataset (b) The results of different intensity of noise in ICEWS18 dataset (c) The results of different intensity of noise in ICEWS05-15 dataset

Fig. 5. Study on the different intensity of noise on ICEWS14,ICEWS18 and ICEWS05-15 datasets on Hits@1 and MRR.

![](_page_8_Figure_5.jpeg)

(a) The results of different layers on ICEWS14 dataset (b) The results of different layers on ICEWS18 dataset

Fig. 6. Study on the number of layers in R-GCN in the global entity-aware attention encoder on ICEWS14 and ICEWS18 datasets.

## *C. Results of TKG Extrapolation*The overall experimental results of LogCL and baselines on four benchmark datasets are reported in Table III. The best results are marked in bold, and the second-best results are reported using underlining. From the experimental results, we have the following observation:

• The performance of LogCL consistently is better than the state-of-the-art methods on four benchmark datasets. Specifically, when comparing the second-best results, LogCL achieves the most significant improvements of 5.2%, 4.9%, 7.9%, and 7.9% in MRR on ICEWS14, ICEWS18, ICEWS05-15 and GDELT datasets.

- For the state-of-the-art models Hismatch and TIRGN, although HisMatch also considers the local historical information related to the query, it fails to effectively consider the importance of the local historical fact information related to the query and does not consider the global historical information, resulting in weaker performance than LogCL. TiRGN takes into account both global and local historical information, but ignoring query-related historical information leads to lower performance than Hismath. Although CENET considers historical contrastive learning with our model LogCL, its performance is lower than LogCL due to the lack of evolutionary modeling of facts. In addition, CENET uses historical contrastive learning to enhance entities with less historical interactions by contrast, while we use contrastive learning from a local and global view to improve the robustness of the model.
- An interesting phenomenon on all models is that the results on ICEWS14 and ICEWS18 datasets perform better than GDELT and ICEWS05-15 datasets. The reason for such phenomenon may be that more complex dynamic interactions among entities and relations exist in ICEWS18 and GDELT datasets. Such complex dynamic facts association are difficult to be modeled and lead to the worse results on ICEWS18 and GDELT datasets. The

excellent performance exhibited by LogCL on ICEWS18 and GDELT datasets demonstrates the ability of LogCL to model complex temporal facts interactions.

• Extrapolation models on all datasets perform better than interpolation and static models, mainly because static models do not consider temporal information and are difficult to capture the dynamic changes of entities and relations. For interpolation models, they only focus on the completion of historical missing facts and lack the ability to model the evolution of entities and relationships over time and predict future unseen facts.

![](_page_9_Figure_2.jpeg)

(a) The MRR results under different query contrast strategies (b) The Hits@1 results under different query contrast strategies

Fig. 7. Study on different query contrast strategies on ICEWS14 and ICEWS18 datasets.

##*D. Ablation Study*To further better analyze each part of LogCL that contributes to the prediction results, we conduct ablation studies on all datasets in terms of MRR and Hits@1/5/10. The results of the LogCL variants are presented in Table IV.
*1) Impact of Global Entity-Aware Attention Encoder:*The results denoted as LogCL-L in Table IV demonstrate the performance of LogCL without considering the global entityaware attention encoder. It can be seen that the performances of LogCL-L consistently performs poorly compared to the LogCL on ICEWS14, ICEWS18 and GDELT datasets, indicating that modeling the longer facts related to the queries is beneficial for TKG reasoning. We also conduct experiments to investigate the impact of varying the number of layers in the R-GCN in the global entity-aware attention encoder, and the results are shown in Fig. 6. It can be observed that demonstrate that the two-hop results are indeed slightly better than the one-hop results on both datasets. However, increasing the number of hops beyond two does not significantly improve performance on the ICEWS14 dataset and leads to decreased performance on the ICEWS18 dataset. A similar phenomenon also can be found in the local entity-aware attention recurrent encoder.
*2) Impact of Local Entity-Aware Attention Recurrent Encoder:*LogCL-G in Table IV is a variant of LogCL without modeling the recent local history at the adjacent timestamps. More specifically, the local entity-aware attention recurrent encoder is removed in LogCL-G. The scores of all entities are obtained by using the representation of entities from the global entity-aware attention encoder and the static relation embedding as the representation of the query relation. The results of LogCL-G in Table IV can be observed that ignoring the local entity-aware attention recurrent encoder can generate a great impact on the performances. Mainly because the recent local history contains rich information describing the behavior trends related to the query, which helps in the selection of the correct answer. Another observation is that the variant LogCL-L is superior to the variant LogCL-G, indicating that modeling the recent local entities and relations evolution is more effective than long historical information.

![](_page_9_Figure_10.jpeg)

(a) The results of different λ on on ICEWS14 dataset (b) The results of different λ on ICEWS18 dataset

![](_page_9_Figure_12.jpeg)

![](_page_9_Figure_13.jpeg)

(a) The results of different temperature coefficient τ on ICEWS14 dataset (b) The results of different temperature coefficient τ on ICEWS18 dataset

Fig. 9. Study on the temperature coefficient τ in ICEWS14 and ICEWS18 datasets.
*3) Impact of Entity-Aware Attention:*To demonstrate how the entity-aware attention contributes to the prediction results, the entity-aware attention is removed in the local entity-aware attention recurrent encoder and global entity-aware attention encoder, which is denoted as "-w/o-eatt" in Table IV. It can be intuitively observed that the performance degradation is great after removing the entity-aware attention on ICEWS14, ICEWS18 and ICEWS05-15 datasets. The main reason is that the entity attention mechanism can effectively capture the facts that the local KG snapshot and global historical subgraph are related to the query.
*4) Impact of Contrastive Learning:*LogCL-w/o-cl denotes a variant of LogCL that removes the local-global contrastive learning. It can be observed that the performance of LogCLw/o-cl is worse than that of LogCL, especially on the ICEWS14 dataset. It is because contrastive learning plays a role in guiding LogCL to fuse different historical characteristics. We also conduct experiments to investigate the impact of four query contrast strategies. The results are presented in Fig. 7. LogCL-gl, LogCL-lg, LogCL-gg, and LogCL-ll denote variants using four different query losses, respectively. It can be observed that LogCL-gl and Log-lg demonstrate slightly superior performance compared to LogCL-gg and LogCL-ll. This suggests that contrastive training by emphasizing the distinction between local and global query representations yields greater benefits.

To further analyze the ability of the local-global query contrast module of LogCL to resist noise interference, we conduct experiments by adding Gaussian noise with different intensities to LogCL and LogCL-w/o-cl. Here, Gaussian noise generated by the Gaussian distribution is added to the entity representation as the initial input of the model. As our primary objective is to predict future Gaussian entities, we solely introduce noise to the entities and not the relations. We control the intensity of Gaussian noises by varying the variance in the Gaussian formula. The experimental results are shown in Fig. 5. When faced with the same intensity of noise, a larger span of Y-axis values on the same color indicates a larger performance degradation. We can intuitively observe that the LogCL model always performs better than the LogCL-w/o-cl model under the same intensity of noise on ICEWS14, ICEWS18 and ICEWS05-15 datasets. This shows that local-global contrastive learning can effectively improve the anti-noise ability of the model. In addition, we also observe another interesting phenomenon, although the performance of LogCL model and LogCL-w/o-cl model gradually decreases with the increase of noise intensity, it is worth noting that the performance of LogCL model decreases less than that of LogCL-w/o-cl model when facing stronger noise, especially on ICEWS05- 15 dataset. LogCL shows relatively strong performance even when subjected to strong noise interference.

TABLE V THE ABLATION EXPERIMENT RESULTS OF MRR AND HITS@1 ON ICEWS14, ICEWS18 AND ICEWS05-15 DATASETS.

| Model                            | ICEWS14                          | ICEWS18     | ICEWS05-15 |             |  |
|----------------------------------|----------------------------------|-------------|------------|-------------|--|
|                                  | MRR Hits@1 MRR Hits@1 MRR Hits@1 |             |            |             |  |
| LogCL (RGCN)                     | 48.87 37.76                      | 35.67 24.53 |            | 57.04 46.07 |  |
| LogCL (CompGCN-sub)              | 49.25 36.84                      | 35.33 24.26 |            | 56.93 45.92 |  |
| LogCL (CompGCN-mult) 47.92 36.85 |                                  | 35.32 24.05 |            | 56.40 45.46 |  |
| LogCL (KBAT)                     | 48.46 37.17                      | 35.70 24.41 |            | 56.01 45.14 |  |

##*E. Sensitivity Analysis*In this section, we conduct experiments on ICEWS14 and 18 datasets to further analyze the impact of parameters in LogCL, including the parameter λ in the prediction part, the temperature coefficient τ in the local-global query contrast module, and GNN aggregation encoder.
*1) Analysis of the Parameter*λ*:*To explore the parameter λ that is used to trade off global and local representations

![](_page_10_Figure_7.jpeg)

(a) The MRR results under online learning (b) The Hits@1 results under online learning

Fig. 10. Study on online training on ICEWS14, ICEWS18 and ICEWS05-15 datasets.

of entities, we conduct experiments with different values of λ from 0 to 1 with other optimal hyperparameters fixed. The results of MRR and Hist@3 are shown in Fig.8. A larger value of λ indicates a higher proportion of the local entity-aware attention recurrent encoder. It can be seen that the performance of LogCL shows a trend of first upward and then falling as λ increases on ICEWS14 and ICEWS18 datasets, which indicates that only considering local historical information or global historical information cannot effectively predict the results. This trend further illustrates that an appropriate parameter is important for combining local and global historical patterns.
*2) Analysis of Temperature Coefficient*τ*:*We perform a batch of experiments with different temperature coefficients with other optimal hyperparameters fixed. The results of MRR and Hits@3 are shown in Fig.9. Different datasets are affected by the temperature coefficient differently, and choosing the appropriate temperature coefficient is helpful for TKG reasoning.

###*F. Study On Different GNN Aggregation*To further study the impact of different kinds of GNNs in the local entity-aware attention recurrent encoder and the global entity-aware attention encoder, R-GCN is replaced in these two encoders with CompGCN [\[24\]](#page-12-19) and KBGAT [\[25\]](#page-12-20). The MRR and Hits@1 results of ICEWS14, ICEWS18, and ICEWS05- 15 are reported in Table V. It can be seen that LogCL (RGCN) gets the best results on ICEWS05-15 dataset and shows strong performance in ICEWS14 and ICEWS18 datasets.

####*G. Study On the Two-Phase Propagation*To investigate the role of the two-phase propagation in our LogCL, we manage experiments to evaluate the results of two forward propagations separately. Log-FP denotes a variant that predicts the object entities on the origin query set and only performs the first phase propagation. Log-SP that predicts the subjected entities on the reverse query set and only considers the second phase propagation. The results are shown in Table VII. It can be seen that the performance of Log-FP is superior to the Log-SP. The reason behind this phenomenon is that the dataset composed of inverse relations may introduce a certain bias, which subsequently impacts the performance of the model. In contrast, the original dataset provides a more

| TABLE VI                                                                   |  |  |  |  |  |  |  |  |
|----------------------------------------------------------------------------|--|--|--|--|--|--|--|--|
| TWO EXAMPLES OF TOP 5 PREDICTIONS FOR THE GIVEN QUERIES ON ICEWS14 DATASET |  |  |  |  |  |  |  |  |

| Query and Answer                                                                             | LogCL                                                                                                                        | LogCL-w/o-eatt                                                                                                                  | LogCL-w/o-cl                                                                                                                         |  |
|----------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|--|
| Query:<br>( China, Sign<br>formal agreement,<br>?, 2014-12-4 )<br>Answer:<br>South Africa    | South Africa<br>0.6136<br>Ashraf Ghani Ahmadzai<br>Malaysia<br>0.084<br>South Korea<br>0.045<br>European Parliament<br>0.043 | Kazakhstan<br>0.109<br>0.088 France<br>0.083<br>South Korea<br>0.076<br>Vietnama<br>0.069<br>Iraq<br>0.049                      | South Africa<br>0.501<br>Ashraf Ghani Ahmadzai<br>0.244<br>South Korea<br>0.058<br>Malaysia<br>0.050<br>European Parliament<br>0.029 |  |
| Query:<br>( Iran, Engage in<br>diplomatic cooperation,<br>?, 2014-11-30 )<br>Answer:<br>Oman | Oman<br>0.687<br>Portugal<br>0.122<br>Guinea<br>0.077<br>Qatqr<br>0.034<br>China<br>0.021                                    | Oman<br>0.1098<br>Iraq<br>0.1095<br>Food and Agriculture Organization<br>0.0813 Iraq<br>China<br>0.0562<br>Tajikistan<br>0.0434 | Oman<br>0.668<br>Portugal<br>0.129<br>0.045<br>Qatar<br>0.041<br>Guinea<br>0.012                                                     |  |

TABLE VII THE RESULTS OF THE TWO-PHASE PROPAGATION ON ICEWS14 , ICEWS18 AND ICEWS05-15 DATASETS.

| Model    | ICEWS14 |             | ICEWS18 |                                  | ICEWS05-15 |             |
|----------|---------|-------------|---------|----------------------------------|------------|-------------|
|          |         |             |         | MRR Hits@1 MRR Hits@1 MRR Hits@1 |            |             |
| LogCL    |         | 48.87 37.76 |         | 35.67 24.53                      |            | 57.04 46.07 |
| LogCL-FP |         | 50.69 39.66 |         | 37.38 25.96                      |            | 58.69 47.79 |
| LogCL-SP |         | 47.04 35.87 |         | 33.89 22.97                      |            | 55.38 44.34 |

comprehensive reflection of the real relations between entities, resulting in better performance in the experimental results.

##*H. Study On the Online Training*Since the evolutionary pattern changes with emerging facts, exploring how to adjust the model to emerging facts is crucial. Following the CEN [\[33\]](#page-12-26) and RETIA [\[45\]](#page-13-10), we perform a batch of experiments to learn emerging facts on ICEWS14, ICEWS18 and ICEWS05-15 datasets under the online setting. The results are shown in the Fig.10. The results of CEN, RETIA and LogCL under the online setting outperform the results in Table III under the offline setting. It is because that historical facts in the test set are updated under the online setting. In addition, LogCL achieves greater improvements than the CEN and RETIA under the online setting. This proves that LogCL can effectively solve domain obstacles such as time-varying problems.

#*I. Case Study*We provide the case study for LogCL, LogCL-w/o-eatt, and LogCL-w/o-cl on ICEWS14 dataset. Two queries with the top-5 prediction entities and scores are reported in Table VI.

For the query (China, Sign formal agreement, ?, 2014- 12-4), we can observe that LogCL and logCL-w/o-cl can predict the correct answer, while the top-5 results given by LogCL-w/o-eatt do not contain the correct answer. For the query (Iran, Engage in diplomatic cooperation, ?, 2014-11- 30), although LogCL, LogCL-w/o-eatt, and LogCL-w/o-eatt can give answers prepared and the answers are top-1, the prediction scores of LogCl and LogCL-w/o-eatt for correct answers are much higher than that of LogCL-w/o-eatt. The reason for the above phenomenon is that the reasoning of LogCL-w/o-eatt primarily relies on historical facts that are in close proximity in time and weakly associated with the query. As a result, LogCL-w/o-eatt fails to capture the historical facts that have a strong relevance to the query, leading to lower accurate prediction results. These two cases can further prove the effectiveness of the entity-aware attention mechanism and the strong reasoning ability of LogCL.

# V. CONCLUSION

In this paper, we propose a novel TKG reasoning model, namely LogCL, which uses contrastive learning to better guide the model to integrate local and global historical information, thereby improving the robustness of the model. We propose a local entity-aware attention recurrent encoder, which effectively captures the importance of query-related historical information in each KG snapshot at the most recent time. We propose a global entity-aware attention encoder, which learns the importance of the global historical information in the history subgraph that is built by sampling the global historical facts based on queries. We design a local-global query contrast module to focus on the important common features of the local encoder and global encoder, so as to enhance the anti-noise ability of LogCL. Extensive experiments on four public datasets demonstrate that our proposed LogCL performs significant improvements and has a more robust performance than the state-of-the-art baselines.

## REFERENCES

- <span id="page-11-0"></span>[1] P. Ernst, C. Meng, A. Siu, and G. Weikum, "Knowlife: A knowledge graph for health and life sciences," in*IEEE 30th International Conference on Data Engineering, Chicago, ICDE 2014, IL, USA, March 31 - April 4, 2014*, I. F. Cruz, E. Ferrari, Y. Tao, E. Bertino, and G. Trajcevski, Eds. IEEE Computer Society, 2014, pp. 1254–1257.
- <span id="page-11-1"></span>[2] L. Cui, H. Seo, M. Tabar, F. Ma, S. Wang, and D. Lee, "DETERRENT: knowledge guided graph attention network for detecting healthcare misinformation," in *KDD '20: The 26th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, Virtual Event, CA, USA, August 23-27, 2020*. ACM, 2020, pp. 492–502.

- <span id="page-12-0"></span>[3] C. Yang and G. Qi, "An urban traffic knowledge graph-driven spatialtemporal graph convolutional network for traffic flow prediction," in *Proceedings of the 11th International Joint Conference on Knowledge Graphs, IJCKG 2022, Hangzhou, China, October 27-28, 2022*. ACM, 2022, pp. 110–114.
- <span id="page-12-1"></span>[4] F. Feng, X. He, X. Wang, C. Luo, Y. Liu, and T. Chua, "Temporal relational ranking for stock prediction," *ACM Trans. Inf. Syst.*, vol. 37, no. 2, pp. 27:1–27:30, 2019.
- <span id="page-12-2"></span>[5] G. W. Trompf, *The idea of historical recurrence in Western thought: from antiquity to the Reformation*. Univ of California Press, 1979, vol. 1.
- [6] J. S. B. Evans, "Heuristic and analytic processes in reasoning," *British Journal of Psychology*, vol. 75, no. 4, pp. 451–468, 1984.
- <span id="page-12-3"></span>[7] S. A. Sloman, "The empirical case for two systems of reasoning." *Psychological bulletin*, vol. 119, no. 1, p. 3, 1996.
- <span id="page-12-4"></span>[8] C. Zhu, M. Chen, C. Fan, G. Cheng, and Y. Zhang, "Learning from history: Modeling temporal knowledge graphs with sequential copygeneration networks," vol. 35, no. 5, pp. 4732–4740, 2021, number: 5.
- <span id="page-12-5"></span>[9] Z. Li, X. Jin, W. Li, S. Guan, J. Guo, H. Shen, Y. Wang, and X. Cheng, "Temporal knowledge graph reasoning based on evolutional representation learning," in *Proceedings of the 44th International ACM SIGIR Conference on Research and Development in Information Retrieval*. Association for Computing Machinery, 2021, pp. 408–417.
- <span id="page-12-6"></span>[10] Z. Han, Z. Ding, Y. Ma, Y. Gu, and V. Tresp, "Learning neural ordinary equations for forecasting future links on temporal knowledge graphs," in *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, EMNLP 2021, Virtual Event / Punta Cana, Dominican Republic, 7-11 November, 2021*. Association for Computational Linguistics, 2021, pp. 8352–8364.
- <span id="page-12-7"></span>[11] Y. Li, S. Sun, and J. Zhao, "Tirgn: time-guided recurrent graph network with local-global historical patterns for temporal knowledge graph reasoning," in *Proceedings of the Thirty-First International Joint Conference on Artificial Intelligence, IJCAI 2022, Vienna, Austria, 23-29 July 2022*. ijcai. org, 2022, pp. 2152–2158.
- <span id="page-12-8"></span>[12] Y. He, P. Zhang, L. Liu, Q. Liang, W. Zhang, and C. Zhang, "HIP network: Historical information passing network for extrapolation reasoning on temporal knowledge graph," in *Proceedings of the Thirtieth International Joint Conference on Artificial Intelligence, IJCAI 2021, Virtual Event / Montreal, Canada, 19-27 August 2021*. ijcai.org, 2021, pp. 1915–1921.
- <span id="page-12-9"></span>[13] P. Khosla, P. Teterwak, C. Wang, A. Sarna, Y. Tian, P. Isola, A. Maschinot, C. Liu, and D. Krishnan, "Supervised contrastive learning," in *Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual*, 2020.
- <span id="page-12-10"></span>[14] Q. Wang, Z. Mao, B. Wang, and L. Guo, "Knowledge graph embedding: A survey of approaches and applications," *IEEE Transactions on Knowledge and Data Engineering*, vol. 29, no. 12, pp. 2724–2743, 2017.
- [15] S. Liang, J. Shao, D. Zhang, J. Zhang, and B. Cui, "DRGI: deep relational graph infomax for knowledge graph completion: (extended abstract)," in *38th IEEE International Conference on Data Engineering, ICDE 2022, Kuala Lumpur, Malaysia, May 9-12, 2022*. IEEE, 2022, pp. 1499–1500.
- <span id="page-12-11"></span>[16] B. Liu, X. Wang, P. Liu, S. Li, Q. Fu, and Y. Chai, "Unikg: A unified interoperable knowledge graph database system," in *37th IEEE International Conference on Data Engineering, ICDE 2021, Chania, Greece, April 19-22, 2021*. IEEE, 2021, pp. 2681–2684.
- <span id="page-12-12"></span>[17] A. Bordes, N. Usunier, A. Garc´ıa-Duran, J. Weston, and O. Yakhnenko, ´ "Translating embeddings for modeling multi-relational data," in *The 27th Annual Conference on Neural Information Processing Systems 2013, December 5-8, 2013, Lake Tahoe, Nevada, United States*, 2013, pp. 2787–2795.
- <span id="page-12-13"></span>[18] Z. Wang, J. Zhang, J. Feng, and Z. Chen, "Knowledge graph embedding by translating on hyperplanes," in *Proceedings of the Twenty-Eighth AAAI Conference on Artificial Intelligence, July 27 -31, 2014, Quebec ´ City, Quebec, Canada ´*. AAAI Press, 2014, pp. 1112–1119.
- <span id="page-12-14"></span>[19] B. Yang, W. Yih, X. He, J. Gao, and L. Deng, "Embedding entities and relations for learning and inference in knowledge bases," in*3rd International Conference on Learning Representations, ICLR 2015, San Diego, CA, USA, May 7-9, 2015, Conference Track Proceedings*, 2015.
- <span id="page-12-15"></span>[20] T. Trouillon, J. Welbl, S. Riedel, E. Gaussier, and G. Bouchard, ´ "Complex embeddings for simple link prediction," in *Proceedings of the 33nd International Conference on Machine Learning, ICML 2016,*

*New York City, NY, USA, June 19-24, 2016*, ser. JMLR Workshop and Conference Proceedings, vol. 48. JMLR.org, 2016, pp. 2071–2080.

- <span id="page-12-16"></span>[21] T. Dettmers, P. Minervini, P. Stenetorp, and S. Riedel, "Convolutional 2d knowledge graph embeddings," in *Proceedings of the Thirty-Second AAAI Conference on Artificial Intelligence, (AAAI-18), New Orleans, Louisiana, USA, February 2-7, 2018*. AAAI Press, 2018, pp. 1811– 1818.
- <span id="page-12-17"></span>[22] C. Shang, Y. Tang, J. Huang, J. Bi, X. He, and B. Zhou, "End-to-end structure-aware convolutional networks for knowledge base completion," in *The Thirty-Third AAAI Conference on Artificial Intelligence, AAAI 2019, Honolulu, Hawaii, USA, January 27 - February 1, 2019*. AAAI Press, 2019, pp. 3060–3067.
- <span id="page-12-18"></span>[23] M. S. Schlichtkrull, T. N. Kipf, P. Bloem, R. van den Berg, I. Titov, and M. Welling, "Modeling relational data with graph convolutional networks," in *The Semantic Web - 15th International Conference, ESWC 2018, Heraklion, Crete, Greece, June 3-7, 2018, Proceedings*, ser. Lecture Notes in Computer Science, vol. 10843. Springer, 2018, pp. 593–607.
- <span id="page-12-19"></span>[24] S. Vashishth, S. Sanyal, V. Nitin, and P. P. Talukdar, "Composition-based multi-relational graph convolutional networks," in *8th International Conference on Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April 26-30, 2020*. OpenReview.net, 2020.
- <span id="page-12-20"></span>[25] D. Nathani, J. Chauhan, C. Sharma, and M. Kaul, in *Proceedings of the 57th Conference of the Association for Computational Linguistics, ACL 2019, Florence, Italy, July 28- August 2, 2019, Volume 1: Long Papers*. Association for Computational Linguistics, 2019, pp. 4710–4723.
- <span id="page-12-21"></span>[26] J. Leblay and M. W. Chekol, "Deriving validity time in knowledge graph," in *Companion of the The Web Conference 2018 on The Web Conference 2018, WWW 2018, Lyon , France, April 23-27, 2018*, P. Champin, F. Gandon, M. Lalmas, and P. G. Ipeirotis, Eds. ACM, 2018, pp. 1771–1776.
- <span id="page-12-22"></span>[27] S. S. Dasgupta, S. N. Ray, and P. P. Talukdar, "Hyte: Hyperplanebased temporally aware knowledge graph embedding," in *Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing, Brussels, Belgium, October 31 - November 4, 2018*, 2018, pp. 2001–2011.
- <span id="page-12-23"></span>[28] T. Lacroix, G. Obozinski, and N. Usunier, "Tensor decompositions for temporal knowledge base completion," in *8th International Conference on Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April 26-30, 2020*. OpenReview.net, 2020.
- <span id="page-12-24"></span>[29] Y. Xu, J. Ou, H. Xu, and L. Fu, "Temporal knowledge graph reasoning with historical contrastive learning," in *Thirty-Seventh AAAI Conference on Artificial Intelligence, AAAI 2023, Thirty-Fifth Conference on Innovative Applications of Artificial Intelligence, IAAI 2023, Thirteenth Symposium on Educational Advances in Artificial Intelligence, EAAI 2023, Washington, DC, USA, February 7-14, 2023*. AAAI Press, 2023, pp. 4765–4773.
- <span id="page-12-25"></span>[30] W. Jin, M. Qu, X. Jin, and X. Ren, "Recurrent event network: Autoregressive structure inferenceover temporal knowledge graphs," in *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)*. Association for Computational Linguistics, 2022-11-24, pp. 6669–6683.
- <span id="page-12-29"></span>[31] H. Sun, J. Zhong, Y. Ma, Z. Han, and K. He, "TimeTraveler: Reinforcement learning for temporal knowledge graph forecasting," in *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing*. Association for Computational Linguistics, 2021, pp. 8306–8319.
- <span id="page-12-28"></span>[32] Z. Han, P. Chen, Y. Ma, and V. Tresp, "Explainable subgraph reasoning for forecasting on temporal knowledge graphs," in *9th International Conference on Learning Representations, ICLR 2021, Virtual Event, Austria, May 3-7, 2021*. OpenReview.net, 2021.
- <span id="page-12-26"></span>[33] Z. Li, S. Guan, X. Jin, W. Peng, Y. Lyu, Y. Zhu, L. Bai, W. Li, J. Guo, and X. Cheng, "Complex evolutional pattern learning for temporal knowledge graph reasoning," in *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)*. Association for Computational Linguistics, 2022, pp. 290– 296.
- <span id="page-12-27"></span>[34] H. Sun, S. Geng, J. Zhong, H. Hu, and K. He, "Graph hawkes transformer for extrapolated reasoning on temporal knowledge graphs," in *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing, EMNLP 2022, Abu Dhabi, United Arab Emirates, December 7-11, 2022*. Association for Computational Linguistics, 2022, pp. 7481–7493.

- <span id="page-13-0"></span>[35] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, "Attention is all you need," in *Advances in Neural Information Processing Systems 30: Annual Conference on Neural Information Processing Systems 2017, December 4-9, 2017, Long Beach, CA, USA*, 2017, pp. 5998–6008.
- <span id="page-13-1"></span>[36] Q. Lin, J. Liu, R. Mao, F. Xu, and E. Cambria, "TECHS: temporal logical graph networks for explainable extrapolation reasoning," in *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2023, Toronto, Canada, July 9-14, 2023*. Association for Computational Linguistics, 2023, pp. 1281–1293.
- <span id="page-13-2"></span>[37] T. Chen, S. Kornblith, M. Norouzi, and G. E. Hinton, "A simple framework for contrastive learning of visual representations," in *Proceedings of the 37th International Conference on Machine Learning, ICML 2020, 13-18 July 2020, Virtual Event*, ser. Proceedings of Machine Learning Research, vol. 119. PMLR, 2020, pp. 1597–1607.
- <span id="page-13-3"></span>[38] Z. Li, Z. Hou, S. Guan, X. Jin, W. Peng, L. Bai, Y. Lyu, W. Li, J. Guo, and X. Cheng, "Hismatch: Historical structure matching based temporal knowledge graph reasoning," in *Findings of the Association for Computational Linguistics: EMNLP 2022, Abu Dhabi, United Arab Emirates, December 7-11, 2022*. Association for Computational Linguistics, 2022, pp. 7328–7338.
- <span id="page-13-4"></span>[39] K. Cho, B. van Merrienboer, C¸ . Gulc¸ehre, D. Bahdanau, F. Bougares, ¨ H. Schwenk, and Y. Bengio, "Learning phrase representations using RNN encoder-decoder for statistical machine translation," in *Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing, EMNLP 2014, October 25-29, 2014, Doha, Qatar,*. ACL, 2014, pp. 1724–1734.
- <span id="page-13-5"></span>[40] E. Boschee, J. Lautenschlager, S. O'Brien, S. Shellman, J. Starz, and M. Ward, "Icews coded event data. harvard dataverse," *V4 (http://dx. doi. org/10.7910/DVN/28075)*, 2015.
- <span id="page-13-6"></span>[41] K. Leetaru and P. A. Schrodt., "Gdelt: Global data on events, location, and tone, 1979-2012," *ISA Annual Convention*, vol. 4, pp. 1–49, 2013.
- <span id="page-13-7"></span>[42] Z. Sun, Z. Deng, J. Nie, and J. Tang, "Rotate: Knowledge graph embedding by relational rotation in complex space," in *7th International Conference on Learning Representations, ICLR 2019, New Orleans, LA, USA, May 6-9, 2019*. OpenReview.net, 2019.
- <span id="page-13-8"></span>[43] A. Garc´ıa-Duran, S. Dumancic, and M. Niepert, "Learning sequence ´ encoders for temporal knowledge graph completion," in *Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing, Brussels, Belgium, October 31 - November 4, 2018*. Association for Computational Linguistics, 2018, pp. 4816–4821.
- <span id="page-13-9"></span>[44] R. Goel, S. M. Kazemi, M. A. Brubaker, and P. Poupart, "Diachronic embedding for temporal knowledge graph completion," in *The Thirty-Fourth AAAI Conference on Artificial Intelligence, AAAI 2020, The Thirty-Second Innovative Applications of Artificial Intelligence Conference, IAAI 2020, The Tenth AAAI Symposium on Educational Advances in Artificial Intelligence, EAAI 2020, New York, NY, USA, February 7-12, 2020*. AAAI Press, 2020, pp. 3988–3995.
- <span id="page-13-10"></span>[45] K. Liu, F. Zhao, G. Xu, X. Wang, and H. Jin, "Retia: relation-entity twin-interact aggregation for temporal knowledge graph extrapolation," in *IEEE International Conference on Data Engineering*. IEEE, 2023.
- <span id="page-13-11"></span>[46] D. P. Kingma and J. Ba, "Adam: A method for stochastic optimization," in *3rd International Conference on Learning Representations, ICLR 2015, San Diego, CA, USA, May 7-9, 2015, Conference Track Proceedings*, 2015.
