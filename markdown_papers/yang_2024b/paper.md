---
cite_key: yang_2024b
title: SSTKG: Simple Spatio-Temporal Knowledge Graph for Intepretable and Versatile Dynamic Information Embedding
authors: Ruiyi Yang
year: 2024
doi: arXiv:2402.12132
url: https://arxiv.org/abs/2402.12132
relevancy: High
downloaded: 'Yes'
tags:
- Spatio-Temporal Knowledge Graphs
- Dynamic Information Embedding
- Location-Aware Modeling
- Temporal-Spatial Patterns
tldr: Simple spatio-temporal knowledge graph framework that enables interpretable
  and versatile dynamic information embedding by integrating spatial and temporal
  dimensions for enhanced prediction and recommendation systems.
date_processed: '2025-07-02'
phase2_processed: true
original_folder: sstkg_spatio_temporal_kg_2024
images_total: 4
images_kept: 4
images_removed: 0
keywords:
- knowledge graph
- knowledge graphs
- link prediction
- real-world
- spatio-temporal
- temporal knowledge graph
---


# SSTKG: Simple Spatio-Temporal Knowledge Graph for Intepretable and Versatile Dynamic Information Embedding

Ruiyi Yang ruiyi.yang@student.unsw.edu.au

University of New South Wales Sydney, NSW, Australia

Flora D. Salim flora.salim@unsw.edu.au University of New South Wales Sydney, NSW, Australia

Hao Xue hao.xue1@unsw.edu.au University of New South Wales Sydney, NSW, Australia

## ABSTRACT

Knowledge graphs (KGs) have been increasingly employed for link prediction and recommendation using real-world datasets. However, the majority of current methods rely on static data, neglecting the dynamic nature and the hidden spatio-temporal attributes of real-world scenarios. This often results in suboptimal predictions and recommendations. Although there are effective spatio-temporal inference methods, they face challenges such as scalability with large datasets and inadequate semantic understanding, which impede their performance. To address these limitations, this paper introduces a novel framework - Simple Spatio-Temporal Knowledge Graph (SSTKG), for constructing and exploring spatio-temporal KGs. To integrate spatial and temporal data into KGs, our framework exploited through a new 3-step embedding method. Output embeddings can be used for future temporal sequence prediction and spatial information recommendation, providing valuable insights for various applications such as retail sales forecasting and traffic volume prediction. Our framework offers a simple but comprehensive way to understand the underlying patterns and trends in dynamic KG, thereby enhancing the accuracy of predictions and the relevance of recommendations. This work paves the way for more effective utilization of spatio-temporal data in KGs, with potential impacts across a wide range of sectors.

### KEYWORDS

Knowledge graph, Spatio-temporal data, Time series forecasting

#### ACM Reference Format:

Ruiyi Yang, Flora D. Salim, and Hao Xue. 2023. SSTKG: Simple Spatio-Temporal Knowledge Graph for Intepretable and Versatile Dynamic Information Embedding. In Proceedings of The 2024 ACM Web Conference (WWW '24). ACM, New York, NY, USA, [9](#page-8-0) pages.<https://doi.org/XXXXXXX.XXXXXXX>

#### <span id="page-0-1"></span>1 INTRODUCTION

Knowledge graphs (KGs) are directed graphs comprising entities (nodes), their attributes, and the relationships between them. They represent information as facts using a node-edge-node structure. For instance, the triplet (Macdonald-compete-Burger King) represents a competitive relationship between Macdonald and Burger

WWW '24, MAY 13 - 17, 2024, Singapore

© 2023 Association for Computing Machinery.

ACM ISBN 978-x-xxxx-xxxx-x/YY/MM. . . \$15.00 <https://doi.org/XXXXXXX.XXXXXXX>

<span id="page-0-0"></span>

Figure 1: An example of spatio-temporal KG

King. KGs adeptly capture intricate relationships between entities, enabling more contextually rich and accurate predictions. By encoding millions of real-world events or facts into graphs, KGs facilitate various downstream tasks such as recommendation system [\[30\]](#page-8-1), information retrieval [\[12\]](#page-8-2), and question answering [\[20\]](#page-8-3). Knowledge graph completion (KGC) methods assist KG construction by inferring missing facts based on existing ones in KGs. They learn the embedding of entities and relations on known facts and apply score functions on all possible facts to compute the possibility the fact exists, like transE [\[3\]](#page-8-4), to help enhance the comprehensiveness and utility of the KG.

In practical scenarios, historical facts influence potential future relations, such as retail sales and traffic. spatio-temporal data, inherently dynamic and complex, exhibits dependencies and relationships that evolve across time and space. The dynamic features of the data complicate the construction and maintenance of KGs that represent data comprehensively and factor in geographical relationships between entities. Static KGC methods treat facts as time-independent, leading to relation and entity embeddings stagnant, which is unrealistic [\[6\]](#page-8-5). Many methods are raised towards temporal KG construction and completion [\[24,](#page-8-6) [1,](#page-8-7) [16,](#page-8-8) [25\]](#page-8-9). Without using KGs, a myriad of spatio-temporal prediction and recommendation methods have been proposed, yielding promising outcomes across various tasks [\[32\]](#page-8-10). Traditional statistical and machine learning methods like ARIMA [\[36\]](#page-8-11), have been complemented by more recent deep learning methods, notably graph convolutional networks [\[42\]](#page-8-12).

Although the above methods show effectiveness when dealing with dynamic data, they still harbor notable limitations. Deep learning methods also struggle when capturing the intricate, non-linear relationships endemic to spatio-temporal data, and may fall short of incorporating broader contextual information. Data sparsity posed another challenge, constraining the improvement of their recommendation performance [\[5\]](#page-8-13). KGs can alleviate the issues occurred using DL methods, courtesy of their rich semantics information.

For clarity, Fig [1](#page-0-0) showcases an STKG tailored for the physical store sales within a city. While various retail outlets like Walmarts,

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

IKEA, are depicted alongside entities from different sectors, such as McDonald. Their sales records, inherently temporal, are typically tabulated over a time interval Δ , including records in several time intervals Δ1,2,.... In a static KG, entities might be linked through relations like competing,collaborating, etc. However, in a temporal KG, these relations might evolve over time based on sales data or other practical considerations. Beyond temporal aspects, entities also exhibit geographical relations, heavily influenced by locations and distances separating them. Entities within STKGs can be expressed using triplets, (ℎ, ,), signifying an entity's state at a specific time. Meanwhile, relations are represented as ( , , ) under a given ,(, ) highlighting the spatio-temporal connection between two entities. By integrating these triplets, a semantic path is constructed, elucidating the evolution of relationships grounded in spatio-temporal data.

STKGs are versatile tools suitable for variety of predictive and recommendation tasks. However, training a spatio-temporal KG on benchmark datasets like Wikidata [\[23,](#page-8-14) [22\]](#page-8-15) or YAGO15K [\[13\]](#page-8-16) proves time-consuming [\[4\]](#page-8-17). The time cost is magnified when applied to extensive real-world datasets. The dynamic nature of data and intricate relationships within the graph present challenges in harnessing an STKG effectively for downstream applications, which leads to research questions: Is there a simple and effective way to construct and exploit an STKG versatile enough to accommodate diverse data types? How to enable this framework for KG completions while ensuring its interpretability?

In this paper, a novel framework - Simple Spatio-Temporal Knowledge Graph (SSTKG) is raised for constructing and exploring spatiotemporal knowledge graphs for prediction and recommendation. By integrating spatio-temporal data into KGs and exploiting these KGs through entity and relation embeddings, the framework aims to leverage the strengths of KGs to enhance the accuracy and relevance of spatio-temporal predictions, while ensuring efficiency as well as interpretability. To validate its efficacy, the framework was applied to two datasets: Safegraph's Spend-Ohio dataset and the Traffic Volume of New South Wales (TFNSW) dataset to do experiments on temporal sequence prediction.

#### 2 RELATED WORK

#### 1 Spatio-Temporal Data Prediction

In the early stages, methods are based on statistical knowledge, or using machine learning, such as Autoregressive Integrated Moving Average (ARIMA) [\[36\]](#page-8-11), Support Vector Regression (SVR) [\[19\]](#page-8-18), Critical Support Vector Machine (CSVM) [\[27\]](#page-8-19) These methods focus more on numerical data. Although they consider number series to be related to time, they are unable to capture enough spatio-temporal dependencies. More recently, researchers have begun to consider more complex methods, thanks to the emergence of deep learning. Long Short-Term Memory (LSTM) networks [\[15\]](#page-8-20): It's a type of Recurrent Neural Networks(RNNs) outperforming other RNNs particularly in learning long-term dependencies. Gated Recurrent Unit (GRU) RNNs [\[7\]](#page-8-21) can capture dependencies of different time scales, controling the information flow from the previous activation when computing the new. [\[8\]](#page-8-22). Temporal Convolutional Networks(TCNs) [\[2\]](#page-8-23) can effectively capture temporal features with an architecture of sequence modeling, causal convolutions, dilated convolutions, and residual connections. Based on TCN, Multivariable Temporal Convolutional Networks (M-TCN) [\[29\]](#page-8-24) allows a model for multivariable time series prediction.

The above models are efficient in handling temporal patterns inside sequences, however, sensors collecting data may also be spatially related, which is omitted by the above models. Graph Neural Networks(GNNs) [\[41\]](#page-8-25) are neural models that capture the dependence of graphs via message passing between nodes of graphs. Based on that, Temporal Graph Convolutional Network (T-GCN) [\[40\]](#page-8-26) is combined with the GCN and the GRU. By using GCN to learn topological structures to learn spatial dependence and using GRU to learn temporal patterns. Moreover, Spatio-Temporal Graph Convolutional Networks (ST-GCN) [\[38\]](#page-8-27) utilizes graph CNNs for extracting spatial features, and gated CNNs for extracting temporal features. A spatio-temporal convolutional block is used to fuse the above two patterns. The fusion of deep learning models leads to a great fit for spatio-temporal data. spatio-temporal GNNs can simultaneously model spatial and temporal information [\[10\]](#page-8-28), and dealing with real-world related works like Traffic flow prediction [\[11,](#page-8-29) [37,](#page-8-30) [35\]](#page-8-31), Next POI recommendation [\[17\]](#page-8-32), Crime prediction [\[18\]](#page-8-33), Weather forecasting [\[21\]](#page-8-34) and Human action recognition [\[33\]](#page-8-35).

#### 2 Knowledge Graph for prediction

2.2.1 Static KGs for Prediction. Since KGs have a unified structure, based on their embeddings or paths, they can be used to predict potential links hidden in established datasets. For static data, KGs can assist and accelerate drug discovery [\[39\]](#page-8-36) in the medical field, and they also perform well on fake news detection [\[9\]](#page-8-37) by finding the shortest path between facts.

2.2.2 Temporal KGs/STKGs for Prediction. Dynamic data, typically sourced from sensors, can also be transferred into structured entities and shaped into temporal KGs(TKGs) or STKGs. Embeddings encompassing distinct spatial or temporal information are compared to determine the entities that would appear in certain time points under certain locations. Since dynamic KGs capture time relationships between entities in events, temporal predictions like the time of natural disasters [\[14\]](#page-8-38) could be achieved. STKGs also help in spatial predictions, by modeling trajectories data, users' mobility patterns or activities can be predicted [\[31,](#page-8-39) [5\]](#page-8-13).

#### 3 Knowledge Graph for recommendation

Apart from prediction, knowledge graphs are also widely used for recommendation. While prediction works (sequence prediction, event prediction, POI prediction, etc.) are highly related to the dynamic nature of entities evolution over time, large proportions of recommendation systems on KG are related to the structure of KG (like entity properties or relation properties), which are related to graph algorithms (path searching) or embedding techniques.

2.3.1 Path-based recommendation. Paths in KGs contain relationships between entities, enabling the extraction of features such as users' preferences or item characteristics by analyzing paths. KPRN [\[34\]](#page-8-40) used the LSTM network to represent path information, like users and movie interactions, thus can calculate user preferences towards target movies.

<span id="page-2-0"></span>SSTKG: Simple Spatio-Temporal Knowledge Graph for Intepretable and Versatile Dynamic Information Embedding WWW '24, MAY 13 - 17, 2024, Singapore

| Notation             | Description                                     |  |  |  |  |  |
|----------------------|-------------------------------------------------|--|--|--|--|--|
| e, r                 | An entity and a relation                        |  |  |  |  |  |
| e, r                 | Vector representation of e and r                |  |  |  |  |  |
| 𝑟𝑖,𝑗                 | directional relation from i to j                |  |  |  |  |  |
| E, R                 | Entity set and relation set                     |  |  |  |  |  |
| 𝑑<br>(𝑒𝑖<br>, 𝑒𝑗)    | Distance between two entities                   |  |  |  |  |  |
| G                    | A STKG                                          |  |  |  |  |  |
| T                    | The set of time                                 |  |  |  |  |  |
| 𝑒𝑎𝑡𝑡𝑟𝑖𝑏𝑢𝑡𝑒           | The embeddings of certain attribute of entities |  |  |  |  |  |
| 𝐼<br>(𝑒𝑖<br>,𝑒0<br>) | Influence that 𝑒𝑖<br>applied on 𝑒0              |  |  |  |  |  |
| 𝑊(𝑒𝑖<br>,𝑒0<br>)     | Weight variable used during training influence  |  |  |  |  |  |

Table 1: Notations and descriptions

<span id="page-2-1"></span>![](_page_2_Figure_4.jpeg)
<!-- Image Description: This flowchart illustrates a data processing pipeline for spatial-temporal data. It begins with raw spatial-temporal data (time, location, dynamic attributes), which is structured through input transfer, relation/influence calculation, and fact construction. This structured data is then represented as spatial-temporal relations (shown as a graph with nodes and edges) using STKG (likely a graph-based model). Finally, an embedding model processes these relations for downstream tasks such as prediction or recommendation. -->

Figure 2: The workflow of proposed framework

2.3.2 Embedding-based recommendation. Entities and relations can normally be transferred into embeddings under certain rules, these embeddings can be applied to recommendation algorithms. Entity2rec [\[26\]](#page-8-41) uses property-specific embeddings on KGs to do recommendation, while HAKG [\[28\]](#page-8-42) uses subgraph embeddings for enhanced user preference prediction.

While the aforementioned methodologies have registered good performances in designated tasks, they are encumbered by certain limitations: 1) Their inherent complexity or the extensive versatility of entities often renders them time-intensive or restricts adaptability to diverse domains. 2) They are not explainable enough to describe features extracted from spatio-temporal data. The proposed model aspires to bridge these gaps, presenting streamlined a solution, adaptable to diverse data types while ensuring interpretability.

#### 3 METHODOLOGY

#### 1 Preliminaries and method overview

The STKG problem is defined as: An optimal STKG should accommodate the dynamic nature of data, adapting to changes in entities' attributes influenced by time and location, facilitating the completion and enhancement of KG after construction, and predicting forthcoming attributes and relationships for entities. Table [1](#page-2-0) summarizes notations used in the paper as well as their meanings.

Input representation The objective of the proposed STKG is to attain universality. To this end, a uniform representation for diverse types of spatio-temporal data is integrated to generalize raw entities and relations types.

STKG embedding model The embedding model is designed to encode entity attributes into vector representations and subsequently decode embeddings into numerical representations mirroring the raw data. The embedding model facilitates KG completion on existing STKG and enables the prediction of underlying or between entities.

Figure [2](#page-2-1) illustrates the general workflow of the framework. Upon acquiring spatio-temporal data, pre-established rules are utilized to extract and compute entities, relationships, and facts, thereby constructing STKG while ensuring limited entity types and relationship types. Subsequently, a new embedding model is raised to vectorize the features of entities, enabling the utilization of the STKG in downstream tasks. This streamlined process facilitates a more efficient and effective application of knowledge graphs in real-world scenarios, able to be used for inference with enhanced speed. Finally, the underlying patterns and insights captured by the STKG are interpreted based on its structure, making the whole model explainable.

### <span id="page-2-3"></span>3.2 Knowledge Graph Construction

3.2.1 Definition of STKG. The spatio-temporal knowledge graph is defined as graphs G = (E, R, T, F), where E, as table [1](#page-2-0) shows, is entities that contains spatio-temporal attributes. R represent the set of relation between entities. T describes how the temporal records get divided. F is the set of facts mentioned in section [1.](#page-0-1) Specifically, R and T in the knowledge graph define certain relation between entities under certain time, which denotes facts. Facts under STKG are seen as a quadruple ( , , , ).

<span id="page-2-2"></span>3.2.2 Simple STKG (SSTKG). Considering when entities like stores are rigidly classified according to their business establishments, as exemplified by the 6-digit North American Industry Classification System (NAICS) code. The strict categorization can lead to an excessive fragmentation of entity types. Also, the dynamics of relationships between entities can vary significantly based on spatial and temporal factors. Two entities, even if their spatial distances are fixed, might have totally inverted relations at different times. Moreover, detailed numerical time and location are hard to be transferred as distinct entities.

In light of these complexities, the simple STKG (SSTKG) aims to provide a more flexible and realistic representation of entities and their relationships, establishing rules for the SSTKG as follows:

- Rule 1: Time and location are not treated as independent entities. Instead, they are integrated as attributes inherent and between entities, represented as part of entity and relation embeddings.
- Rule 2. The model prioritizes a reduction in the number of entity types, embedding classification data directly within the entity. This not only simplifies the graph structure but also facilitates more efficient and direct retrievals of classification information from the entity embeddings.
- Rule 3. Numerical representations are adopted to directly articulate the relationship between two entities. Under this paradigm, the association between entities is conceptualized as a continuous variable termed "influence". Within this

framework, any pair of entities can exhibit a relationship that is fluid across both temporal and spatial dimensions

• Rule 4: Relationships between entities that are quantitatively negligible are omitted, ensuring focus on significant interactions and reducing noise within the graph.

Leveraging this SSTKG framework, entities are directly extracted from structured data. The process of relation extraction is thus transformed into "relation computation", or "influence computation", while fact still be seen as the quadruple ( , , , ).

3.2.3 Algorithm for constructing SSTKG. The detailed process of constructing the SSTKG is elucidated according to [3.2.2.](#page-2-2) The temporal records for an entity are viewed as The result of related entities applying influence plus itself's basic record, which is:

<span id="page-3-0"></span>
$$
p_{e_0} *Record_{e_0}(t) = \sum_{i=1}^{n} I_{(e_i, e_0)} Record_{e_i}(t)
$$
 (1)

Fitting Equation [\(1\)](#page-3-0) is seen as a regression process, where 1-p is seen as a parameter quantifying the self-influence of an entity, providing a measure of how much an entity's characteristics contribute to its own behavior or status within the knowledge graph. While temporal variable t represents a time slot, the integration of temporal data and spatial relationships facilitates the computation of a relation "weight" [\(2\)](#page-3-1), using overall record and distance between two entities, is seen as a ratio of properties of to 0. The p in [\(1\)](#page-3-0) is counted in Equation [\(3\)](#page-3-2). Then the influence that entity may apply on during time slot t is calculated in Equation [\(4\)](#page-3-3):

<span id="page-3-1"></span>
$$
W_{(e_i,e_0)} = \frac{OverallRecord(e_i)}{OverallRecord(e_0)}* log(1 + \frac{\sum_{j=i}^{n} Distance(e_j,e_0)}{n *Distance(e_i,e_0)})
$$
 (2)

<span id="page-3-2"></span>
$$
p_{e_0} = \frac{\Sigma_i W_{(e_i, e_0)}}{\Sigma_{k,j} W_{(e_k, e_j)}}
$$
(3)

<span id="page-3-3"></span>
$$
I_{(e_i,e_0)} = regressionFactor* W_{(e_i,e_0)}
$$
\n(4)

Algorithm [1](#page-3-4) shows the pseudocode for constructing SSTKG, yt needs to be emphasized that, the "influence" is unidirectional. In determining the "influence", only the spatio-temporal information of entities is considered. Attributes of entities, such as categories, remain unaddressed. Such an omission in SSTKG construction arises from potential complexities in the data; for instance, the prevalence of numerous categories as seen with the NAICS code shown in Section [3.2.](#page-2-3) On the other hand, some data is hard to fit entities in specific categories, like traffic volume data. Hence, these data are integrated into KG embedding, as elaborated in Section [3.3.](#page-3-5)

#### <span id="page-3-5"></span>3.3 Embedding Model

One entity's temporal data record as well as its spatial location is assumed to influence other entities' temporal records. While the numerical "influence" is seen as a relation, the embedding model aims to map attributes of entities and relations into low-dimensional vectors. Embeddings generated by the model are further implemented into downstream work. Specifically, the embeddings are categorized into 3 boxes: static, dynamic in and dynamic out.

| Ruivi et al. |  |  |
|--------------|--|--|
|--------------|--|--|

<span id="page-3-4"></span>

|  | Algorithm 1 Constructing a SSTKG using time-series records data |  |  |  |  |
|--|-----------------------------------------------------------------|--|--|--|--|
|--|-----------------------------------------------------------------|--|--|--|--|

| Require: Entity 𝐸, Location |  |  | 𝐿, time-series records |  | 𝑇𝑆, distance |
|-----------------------------|--|--|------------------------|--|--------------|
| threshold 𝐷                 |  |  |                        |  |              |

Ensure: Quadratic relation set

- 1: for ∈ do 2: filtering <sup>0</sup> ⊆ where 3: for all ∈ <sup>0</sup> do
- 4: if Distance(, ) ≤ then
- 5: end if
- 6: end for
- 7: for ∈ <sup>0</sup> do
- 8: ( , ) ← Compute weight using ([\(2\)](#page-3-1))
- 9: end for
- 10: ← Compute using ([\(3\)](#page-3-2))
- 11: (0, ) <sup>←</sup> Compute influence using ([\(4\)](#page-3-3))

12: end for

3.3.1 Static Embedding. This component encapsulates the static attributes of an entity, yielding a representation that remains invariant over time. Static attributes are left when calculating "influence". However, in the computation of the static embedding, these attributes that were previously set aside are reintegrated. Apart from categorical attributes, a summary of the entity's comprehensive spatio-temporal data is integrated into the static embedding. Metrics such as average sales volume or average traffic flow are included to represent the "magnitude" or "scale" of the entity. Equation [\(5\)](#page-3-6) shows the formation of static embedding, where manages to regularize overall records into a smaller range.

<span id="page-3-6"></span>
$$
e_{i\_static} = e_{i\_category} *\phi(overall\_records)
$$
 (5)

3.3.2 Dynamic Embedding. Dynamic embedding contains directions of entity relationships. With the use of spatial-temporal records, it is formed by two subsets: out embedding and in embedding, reflecting "pointing to" and "pointing from" links between entities on a knowledge graph.

Out embedding signifies the potential influence an entity may impart upon its linked entities. It is configured as the dynamic embedding representing the "influence level" of the entity itself, disregarding spatial relationships with other entities. The computation of the out embedding is shown in Equation [\(6\)](#page-3-7), encompassing concatenation of the static embedding with its temporal records. The out embedding is a combination of the entity's overall status and temporal status.

<span id="page-3-7"></span>
$$
e_{i\_out}^t = \psi(e_{i\_static}, e_{i\_records}^t)
$$
 (6)

In Embedding quantifies the influence that an entity receives from its associated entities, reflecting the cumulative impact of these relationships on the entity. Analogously, in the formation of the SSTKG, the embedding is viewed as an aggregate of the entity's inherent influence and the influences exerted by its associated entities. Shown in Equation [\(8\)](#page-4-0), p is the weight shown in Equation [\(3\)](#page-3-2). On vector space it is represented in Equation [\(9\)](#page-4-1).

$$
p_i* e_{i\_out}^t = e_{i\_in}^t \tag{7}
$$

<span id="page-4-0"></span>
$$
\mathbf{e}_{\mathbf{i\_in}}^{\mathbf{t}} = \Sigma_j F(Influence_{(i,j)} *\mathbf{e}_{\mathbf{j\_out}}^{\mathbf{t}})
$$
 (8)

<span id="page-4-1"></span>
$$
\mathbf{e}_{\mathbf{i\_in}}^{\mathbf{t}} = \Sigma_j (Influence_{(i,j)}* \mathbf{e}_{\mathbf{j\_record}}^{\mathbf{t}} + \mathbf{e}_{\mathbf{j\_static}})
$$
(9)

3.3.3 Embedding Training Algorithm. The output of Equation [\(8\)](#page-4-0) in the embedding model is not directly ascertainable, since after adding the influence, out-embedding needs to be trained to fit the equation, which leads to modification in static embedding. The static embedding and out-embeddings are used as input, optimized embeddings are obtained after training.

Let <sup>0</sup> represent a set of out embeddings of entities that have potential relations, with entity 0, while set denotes the initial influence of entities in <sup>0</sup> as (1\*n) vector to 0. Given a training tuple x = (0, R, 0, t) Equation [\(10\)](#page-4-2) defined a score as how precise one entity is influenced by related entities. Meanwhile, valid relations and embedding sets are used to obtain a lower score of , then the first loss function is defined in Equation [\(11\)](#page-4-3).

<span id="page-4-2"></span>
$$
f_{p1}(x) = f_1(e_0, R, E_0, t) = ||p_{e_0} *e_{0\_out}^t - e_{0\_in}^t||_2^2
$$
 (10)

<span id="page-4-3"></span>
$$
l_{emb}(x) = l_{emb}(e_0, R, E_0, t) = -\Sigma_i log \sigma(f_{p1}(e_0, R^i, E_0, t) - f_{p1}(x))
$$
\n(11)

Embedding is replaced in <sup>2</sup> (0, , 0, ) with another random entity that has similar overall selling records in the whole dataset and without relations with , using the same Influence value. An alternate score function is defined for the loss of entity influence values. For an entity 0, its influence on the SSTKG, which is related to entities <sup>0</sup> that connect with 0, now denotes after optimizing out-embeddings, the influence of <sup>0</sup> to entities in 0. Given a training tuple x = (0, R, 0, t), the score function is articulated as:

<span id="page-4-5"></span>
$$
f_{p2}(x) = f_{p2}(e_0, R, E_0, t) = ||p_{e_0}* e_{0\_out}^t - \Sigma_i R_i *e_{i\_out}^t||_2^2 \quad (12)
$$

<span id="page-4-6"></span>
$$
l_{inf}(x) = l_{inf}(e_0, R, E_0, t) = -\Sigma_i log \sigma(f_{p2}(e_0, R, E_0^i, t) - f_{p2}(x))
$$
\n(13)

In (0, , 0, ) one related entity's influence is replaced to average. The second loss function denotes the loss of specific "influence" value, which is the relations. Algorithm [2](#page-4-4) shows the process of learning improved embeddings and influences.

#### 4 MODEL PROPERTIES

#### 1 Efficiency and Speed

The proposed model is designed with computational efficiency in mind. It requires less computational resources compared to traditional models, thereby enabling faster construction of the STKG. This feature is particularly beneficial in scenarios where rapid knowledge graph construction is crucial. Here is the test result of constructing and optimizing an SSTKG using the Spend-Ohio dataset mentioned in Section [5.1,](#page-5-0) with 100 training epochs.

<span id="page-4-4"></span>Algorithm 2 Training entity embeddings and relations for SSTKG

| Require: 𝑁𝑒𝑝𝑜𝑐ℎ𝐼𝑛 𝑓<br>, 𝑁𝑒𝑝𝑜𝑐ℎ𝐸𝑚𝑏, SSTKG<br>𝐺<br>with initialized 𝑒𝑠𝑡𝑎𝑡𝑖𝑐 | , |
|----------------------------------------------------------------------------|---|
| 𝑒𝑜𝑢𝑡, influence                                                            |   |
| Ensure: SSTKG with trained 𝑒𝑜𝑢𝑡, influence                                 |   |
| 1: for 𝑖<br>= 1 to 𝑁𝑒𝑝𝑜𝑐ℎ𝐼𝑛 𝑓<br>do                                        |   |
| 𝑆1<br>← 𝐺<br>2:                                                            |   |
| while 𝑆1<br>≠ ∅ do<br>3:                                                   |   |
| Sample batch 𝑆𝑏𝑎𝑡𝑐ℎ<br>⊂ 𝑆1<br>4:                                          |   |
| 𝑆1<br>← 𝑆1<br>\ 𝑆𝑏𝑎𝑡𝑐ℎ<br>5:                                               |   |
| 𝐿1<br>← 0<br>6:                                                            |   |
| for 𝑠<br>∈ 𝑆𝑏𝑎𝑡𝑐ℎ<br>do<br>7:                                              |   |
| 𝑓𝑝1<br>(𝑠) ←<br>compute score using (10)<br>8:                             |   |
| 𝑙<br>𝑖𝑛 𝑓 (𝑠) ←<br>compute loss using (11)<br>9:                           |   |
| 𝐿1<br>← 𝐿1<br>+ 𝑙<br>𝑖𝑛 𝑓 (𝑠)<br>10:                                       |   |
| end for<br>11:                                                             |   |
| Update out embeddings using ∇𝐿1<br>12:                                     |   |
| end while<br>13:                                                           |   |
| 14: end for                                                                |   |
| 15: for 𝑖<br>= 1 to 𝑁𝑒𝑝𝑜𝑐ℎ𝐸𝑚𝑏<br>do                                        |   |
| 𝑆2<br>← 𝐺<br>16:                                                           |   |
| while 𝑆2<br>≠ ∅ do<br>17:                                                  |   |
| Sample batch 𝑆𝑏𝑎𝑡𝑐ℎ<br>⊂ 𝑆2<br>18:                                         |   |
| 𝑆2<br>← 𝑆2<br>\ 𝑆𝑏𝑎𝑡𝑐ℎ<br>19:                                              |   |
| 𝐿2<br>← 0<br>20:                                                           |   |
| for 𝑠<br>∈ 𝑆𝑏𝑎𝑡𝑐ℎ<br>do<br>21:                                             |   |
| 𝑓𝑝2<br>(𝑠) ←<br>compute score using (12)<br>22:                            |   |
| 𝑙𝑒𝑚𝑏<br>(𝑠) ←<br>compute loss using (13)<br>23:                            |   |
| 𝐿2<br>← 𝐿2<br>+ 𝑙𝑒𝑚𝑏<br>(𝑠)<br>24:                                         |   |
| end for<br>25:                                                             |   |
| Update influence in relations using ∇𝐿2<br>26:                             |   |
| end while<br>27:                                                           |   |
| 28: end for                                                                |   |

#### 2 Inference Patterns

By using the embedding model in Section [3.3,](#page-3-5) a certain entity's temporal record is predicted using its related entities' records. Based on Equation [\(8\)](#page-4-0), trained static embedding of related entities and their current temporal records are used to compute the target entity's out-embedding. Therefore, final temporal records are decoded from out embedding as well as the static embedding, since for the trained embeddings, influence∈ are obtained, while having related entities' records on time slot 1, the out/in embeddings for <sup>0</sup> is inferred based on Equation [\(8\)](#page-4-0) and [\(9\)](#page-4-1). Subsequently, the referred \_ is decoded in accordance with Equation [\(6\)](#page-3-7).

#### 3 Interpretability

Another significant advantage of SSTKG is its interpretability. The simple structure and the numerical representation of relationships make it easier to understand the underlying patterns and insights captured by the STKG. This interpretability enhances the model's usability, especially in applications where understanding the reasoning behind predictions is important.

Embedding directly reflects the spatio-temporal properties of each entity based on backward induction. The whole fitting and training process, to simply explain, is a process of finding proper

Table 2: Time cost for training SSTKG on Spend-Ohio dataset

| entity number | time records (day) | average time(s) |
|---------------|--------------------|-----------------|
| 1000          | 30                 | 347.7           |
| 39188         | 30                 | 15942.8         |
| 41200         | 30                 | 16506.1         |

embeddings that incorporate an entity's spatio-temporal data, such that the embedding (out-embedding), is viewed as the result of the combined effects of related entities' embeddings(out-embedding), during which the unidirectional relation between two entities serves as the parameter of fitting the whole equation. First, an expansion of the Equation [\(8\)](#page-4-0) is resented in Equation [\(14\)](#page-5-1) and then transferred as Equation [\(15\)](#page-5-2).

<span id="page-5-1"></span>
$$
p_i* e_{i\_in}^t = \sum_j \psi(e_{i\_static}, e_{i\_records}^t) *Influence_{j,i} \qquad (14)
$$

<span id="page-5-2"></span>
$$
p_i* e_{i\_in}^t = \Sigma_j e_{j\_static} * \Omega(e_{i\_records}^t, Influence_{j,i})
$$
 (15)

Clearly, Ω after this transformation, served as connecting parameters of out-embeddings (the temporal record) to the influence variables: it's a temporal relation of entity to , which is further explained as entity 's influence to under time , also it can serve as generating an embedding of temporal relation, simplified as Equation [\(16\)](#page-5-3).

<span id="page-5-3"></span>
$$
p_i \cdot e_i^t = \sum_j e_j^t \cdot influence_{j,i} = \sum_j e_{j\_static} \cdot r_{j,i}^t \tag{16}
$$

Thus, from the final result, training the embedding serves to refine the processes undertaken during SSTKG construction. it optimizes the whole SSTKG, forming the exact relationship using both entities' categorical, spatial, and temporal attributes.

#### 5 EXPERIMENTS

#### <span id="page-5-0"></span>5.1 Datasets

Two datasets are used to evaluate the performance of SSTKG. The first one is Spend-Ohio data from January 2022 to April 2023, collected by Safegraph, containing many Ohio stores' geographical and categorical information, as well as the selling records counted by day. Figure [3](#page-5-4) represent entities' distribution in forms of heatmap. The second one is Traffic Volume of Transport for New South Wales (TFNSW) data, which encompasses the traffic volume from a collection of permanent traffic counters and classifiers in Sydney, with data collated since 2008 on an hourly basis. Locations of these counters have been further categorized based on their respective suburbs. Table [3](#page-5-5) presents the size of the two datasets. Notably, the 'distance' attribute represents the distance threshold employed during SSTKG construction as per Algorithm [1.](#page-3-4) The attributes used in processed Spend-Ohio and TFNSW data are shown in Table [4.](#page-5-6)

#### 2 Evaluation

The accuracy rate for a prediction in the study is quantified using ACCn metric, which is defined as, if the predicted value falls within a specific range of the real value, it is deemed accurate. The range

<span id="page-5-5"></span>Table 3: Quantities of data used in datasets

| Spend-Ohio dataset |          |          |           |         |
|--------------------|----------|----------|-----------|---------|
| data               | entities | distance | relations | records |
| 2022-3             | 39188    | 2km      | 2941374   | 1014976 |
| 2022-4             | 39461    | 2km      | 2970417   | 1055901 |
| 2022-5             | 39654    | 2km      | 3028519   | 1083649 |
| 2022-6             | 39931    | 2km      | 3062957   | 1098972 |
| 2023-1             | 41200    | 2km      | 3200018   | 1277200 |
| 2023-2             | 41138    | 2km      | 3194903   | 1151864 |
| 2023-3             | 42932    | 2km      | 3314523   | 1300893 |
| TFNSW dataset      |          |          |           |         |
| data               | entities | distance | relations | records |
| 2015               | 67       | 4km      | 496       | 1045200 |
| 2016               | 69       | 4km      | 511       | 1212192 |
|                    |          |          |           |         |

<span id="page-5-6"></span>Table 4: Attributes for constructing SSTKG in datasets

| Spend-Ohio dataset                                            |                                                                                                                                                                |  |  |
|---------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|--|--|
| attribute                                                     | detail explanation                                                                                                                                             |  |  |
| Placekey<br>NAICE code<br>Temporal records<br>Overall records | a tuple representing entity location<br>6-digit code reflecting category<br>selling records collected day by day<br>overall records calculated by past results |  |  |
| TFNSW dataset                                                 |                                                                                                                                                                |  |  |
| attribute                                                     | detail explanation                                                                                                                                             |  |  |
| Location<br>Suburb<br>Temporal records<br>Overall records     | counters' locations<br>the suburb where counters are located<br>traffic volume collected by hour<br>aggregated traffic volume                                  |  |  |

<span id="page-5-4"></span>![](_page_5_Figure_19.jpeg)
<!-- Image Description: The image is a heatmap overlaid on a map of Ohio. It displays a spatial distribution, likely of population density or a related metric. Brighter colors (yellow-green) indicate higher concentrations, while lighter colors (purple-blue) show lower concentrations. The heatmap's purpose is to visually represent the geographic clustering or spatial patterns of the phenomenon being studied within the state of Ohio. -->

Figure 3: Heatmap of stores in Spend-Ohio dataset

is determined by equation [17,](#page-6-0) allowing for a flexible yet rigorous assessment of prediction accuracy. Root Mean Square (RMS) and Relative Standard Deviation (RSD) are also used as supplementary evaluation metrics, defined in equation [18](#page-6-1) and [19.](#page-6-2)

<span id="page-6-3"></span>SSTKG: Simple Spatio-Temporal Knowledge Graph for Intepretable and Versatile Dynamic Information Embedding WWW '24, MAY 13 - 17, 2024, Singapore

Table 5: Test results for Spend-Ohio datasets

|        | Spend-Ohio dataset: 2022.3 - 2022.6 |                                     |         |       |
|--------|-------------------------------------|-------------------------------------|---------|-------|
| method | acc@10                              | acc@15                              | RMS     | RSD   |
| SVR    | 0.5621                              | 0.6528                              | 0.09872 | 158.9 |
| LSTM   | 0.5984                              | 0.7025                              | 0.09031 | 135.7 |
| GRU    | 0.7057                              | 0.8544                              | 0.0607  | 97.3  |
| T-GCN  | 0.7489                              | 0.8386                              | 0.0651  | 103.5 |
| ST-GCN | 0.7902                              | 0.8945                              | 0.0463  | 87.9  |
| SSTKG  | 0.8016                              | 0.8922                              | 0.0452  | 86.1  |
|        |                                     |                                     |         |       |
|        |                                     | Spend-Ohio dataset: 2023.1 - 2023.3 |         |       |
| method | acc@10                              | acc@15                              | RMS     | RSD   |
| SVR    | 0.6015                              | 0.7325                              | 0.09751 | 144.3 |
| LSTM   | 0.6394                              | 0.7672                              | 0.08865 | 127.2 |
| GRU    | 0.7359                              | 0.8897                              | 0.0528  | 88.3  |
| T-GCN  | 0.7826                              | 0.8597                              | 0.0562  | 91.3  |
| ST-GCN | 0.8435                              | 0.09291                             | 0.0399  | 76.8  |

<span id="page-6-0"></span>
$$
r_{predict} \in (r_{real}(1 - n\%), r_{real}(1 + n\%))
$$
 (17)

<span id="page-6-1"></span>
$$
RMS = \sqrt{\frac{\Sigma_{i=1}^{n} (o_i - p_i)^2}{\Sigma_{i=1}^{n} (o_i)^2}}
$$
(18)

<span id="page-6-2"></span>
$$
RSD = \sqrt{\frac{\sum_{i=1}^{n} (o_i - p_i)^2}{N}}
$$
(19)

To benchmark the performance of our model (SSTKG), several established models are used for comparison: (1) Support Vector Regression Machine(SVR). (2)Long Short-Term Memory (LSTM) network. (3) Gated Recurrent Unit(GRU) [\[7\]](#page-8-21). (4) TGCN [\[40\]](#page-8-26), the fusion of GCN and GRU. (5) STGCN [\[38\]](#page-8-27) which combines two TCNs and one GCN.

#### 3 Case study

In order to validate the interpretability of the proposed model, a case study was conducted using the Spend-Ohio data in 2023- 1. Specific stores served as exemplars. Following the knowledge graph construction and training of the influences and embeddings, the distance thresholds were adjusted to modify the quantity of entities deemed related in the knowledge graph. Three groups of entities near the center store are chosen, and prediction records after removing each of them are prepared and analyzed. By repeating the construction process with these variations, differences in outcomes aim to elucidate the model's explainability.

#### 6 RESULT

#### 1 Experiment Results

6.1.1 Safegraph: Spend-Ohio dataset. In Spend-Ohio dataset, the first 25 days are used to construct and train the SSTKG for monthly data, while the rest data is used for testing(which is 6 days, 3 days, and 6 days in the three subsets). To help compare and reduce the effect of null values, when calculating the RMS and RSD, the score's

Table 6: Test results for TFNSW datasets

|        | TFNSW dataset: hourly prediction |        |         |       |
|--------|----------------------------------|--------|---------|-------|
| method | acc@10                           | acc@15 | RMS     | RSD   |
| SVR    | 0.701                            | 0.7583 | 0.06737 | 129.8 |
| LSTM   | 0.7639                           | 0.8072 | 0.05615 | 113.4 |
| GRU    | 0.7825                           | 0.8404 | 0.0475  | 107.8 |
| T-GCN  | 0.7973                           | 0.8345 | 0.0497  | 105.2 |
| ST-GCN | 0.8137                           | 0.8641 | 0.0429  | 96.9  |
| SSTKG  | 0.8095                           | 0.8692 | 0.04245 | 95.7  |
|        | TFNSW dataset: daily prediction  |        |         |       |
| method | acc@10                           | acc@15 | RMS     | RSD   |
| SVR    | 0.7914                           | 0.8215 | 0.05047 | 90.1  |
| LSTM   | 0.8145                           | 0.8374 | 0.4059  | 87.2  |
| GRU    | 0.8609                           | 0.9285 | 0.03867 | 63.7  |
| T-GCN  | 0.8745                           | 0.948  | 0.03641 | 67.5  |
| ST-GCN | 0.8991                           | 0.9625 | 0.03583 | 52.8  |
| SSTKG  | 0.9051                           | 0.9571 | 0.03488 | 54.3  |
|        |                                  |        |         |       |

selling records is normalized to a range of (0,20). The results are shown in Table [5.](#page-6-3)

6.1.2 TFNSW dataset. In TFNSW data, two separate experiments were done. The first one used the hourly data collected 24/7. 40 weeks' data were used to train, and then a 24-hour prediction in the following days was generated. In the second experiment, hourly records were added to daily ones, then the daily records were used to train. It is similar to the scale in the Spend-Ohio dataset. Similarly, the traffic volume was also normalized to (0,20). The accuracy result (acc10 and acc15) and the RMS and RSD for normalized data are shown in Table [6.](#page-6-3)

#### 2 Result analysis

Notably, from the results, the prediction of T-GCN, ST-GCN, and SSTKG are consistently outperformed the SVR, GRU and LSTM models. This is because these three models only focus on temporal record correlations while failing to consider spatial relations. SSTKG, as well as T-GCN and ST-GCN, model both spatial and temporal characteristics to ensure the data effectiveness, which are more suitable for datasets. SSTKG, in particular, demonstrates the ability to balance and integrate spatial-tempoal dimensions. Is outperformed T-GCN. Its performance is noteworthy, especially in acc@15 and RSD metrics on the Spend-Ohio dataset. It outshines others in acc@15, RMS, and RSD for the hourly predictions in the TFNSW dataset, and acc@10 and RMS metrics in daily predictions.

#### 3 Interpretability: case study

To demonstrate the interpretability of the SSTKG model, this section presents a detailed case study involving a specific entity in the Spend-Ohio dataset. A full type service restaurant is selected carefully and set as the center entity (placekey: 225-222@63j-xxx-xxx; NAICS:722511). The sample is selected due to following reasons: 1. Completeness of records: The selected stores as well as linked entities have complete records in all parts of Spend-Ohio dataset. 2. General category: The selected sample belongs to full type

service restaurant, which is a general type in the data. 3. Proper related entities: The store located in a relatively popular area. Distances of nearby entities are shown in Figure [4.](#page-7-0) There are 36 entities in SSTKG that have influence with this shop. Figure [5](#page-7-1) shows the influence values that are calculated and extracted from SSTKG.

<span id="page-7-2"></span>Table 7: Real values vs Predicted and Adjusted Data

| Day | Real values | 𝑅0     | 𝑅𝑎     | 𝑅𝑏     | 𝑅𝑐     |
|-----|-------------|--------|--------|--------|--------|
| 1   | 263.95      | 277.47 | 257.44 | 289.69 | 281.82 |
| 2   | 495.81      | 530.09 | 517.74 | 539.26 | 528.27 |
| 3   | 257.85      | 239.37 | 228.33 | 245.70 | 242.62 |
| 4   | 352.82      | 372.83 | 352.14 | 381.54 | 373.38 |
| 5   | 196.54      | 188.06 | 172.63 | 191.41 | 190.35 |
| 6   | 409.67      | 435.99 | 413.76 | 443.57 | 434.63 |
| 7   | 200.7       | 189.11 | 180.15 | 198.97 | 185.34 |

From the above results, generally, entities close to the sample entity tend to have larger absolute influence values, whereas those entities located further away exhibit minimal or no influence on the sample. Three groups of entities are chosen for further analysis, marked as A, B and C. Entity A and Entity B are close to the center store, having high 'influence' values. Group C, although their temporal records are significant, their spatial and categorical attributes play a crucial role in the model's calculations, resulting in them having a minimal influence value. By integrating the above influences with trained embeddings, the sample's selling is predicted based on Equation [\(6\)](#page-3-7), [\(8\)](#page-4-0) and [\(9\)](#page-4-1) (first calculate embeddings then decode records). However, if some related entities, like A, B and group C were masked, the predicted result would change. Table [7](#page-7-2) shows the change of prediction after masking entities. While the former predicted data is 0, predicted data after removing A, B and C are , and .

<span id="page-7-0"></span>![](_page_7_Figure_5.jpeg)
<!-- Image Description: The histogram displays the distribution of distances from various shops to a central shop. The x-axis represents the distance, and the y-axis shows the number of shops at that distance. The data shows a multimodal distribution, with several peaks indicating clusters of shops at specific distances from the central location. The histogram likely illustrates spatial patterns or characteristics of shop locations relative to a central point in the study area. -->

Figure 4: Related entities' distances with sample shop

A hypothesis test is set to show the difference between predicted data. The null hypothesis are: 0 : <sup>0</sup> < ; 0 : <sup>0</sup> > ; 0 : 0! = , while alternative hypothesis are 1 : <sup>0</sup> > ; 1 : <sup>0</sup> < ; 1 : <sup>0</sup> = . Table [8](#page-7-3) shows the p-value after t-test under 95% confidence level. For all three null hypotheses, the p-value of t-test is greater than 0.05, thus are all rejected, drawing the conclusion that, by masking entity A, the predicted value for sample's selling decreased(<sup>0</sup> > ), while by masking B the predicted value increased (<sup>0</sup> > ) – those who have positive

<span id="page-7-1"></span>![](_page_7_Figure_8.jpeg)
<!-- Image Description: The scatter plot displays the relationship between influence and distance. Red 'x' markers represent individual data points. Three box plots (A, B, C) show the distribution of influence at different distance ranges. A dashed horizontal line indicates zero influence. The figure illustrates how influence changes with distance, with A showing high positive, B negative, and C near-zero influence. -->

Figure 5: Related entities' influence to sample shop

influence on SSTKG would increase prediction, which means "prosperity in one shop leads to prosperity to another", and vice versa. On the other hand, in group C, where entities have small influence values, the prediction value changed a little after masking them (more than 95% confidence to confirm that <sup>0</sup> = ).

Table 8: Result for t-test

<span id="page-7-3"></span>

| hypothesis                                                               | p-value                            | result                                                                                |
|--------------------------------------------------------------------------|------------------------------------|---------------------------------------------------------------------------------------|
| 𝐻0𝑎<br>: 𝑅0<br><<br>𝑅𝑎<br>𝐻0𝑏<br>: 𝑅0<br>><br>𝑅𝑏<br>𝐻0𝑐<br>: 𝑅0!<br>= 𝑅𝑐 | 0.9998975<br>0.999873<br>0.6717662 | reject 𝐻0𝑎, accept<br>𝐻1𝑎<br>reject 𝐻0𝑏<br>, accept 𝐻1𝑏<br>reject 𝐻0𝑐<br>, accept 𝐻1𝑐 |

#### 7 CONCLUSIONS AND FUTURE WORK

In this paper, a new knowledge graph framework is proposed, i.e., Simple Spatio-Temporal Knowledge Graph (SSTKG), which leverages 3 kinds of embeddings (static, temporal in and out embeddings) to model entities, as well as using "influence" to model the spatiotemporal relations between entities. A comprehensive evaluation using real-world data has underscored the efficacy of the proposed SSTKG in prediction tasks and highlighted its interpretability. Future endeavors will focus on (1)Refining the SSTKG construction algorithm. (2) Enhancing dynamism in SSTKG to reflect entities' exhibit temporal mobility such as user POI trajectories in which locations are shifting. (3)Balance between model size and efficiency.

#### 8 ETHICAL USE OF DATA

The Spend-Ohio dataset from SafeGraph was utilized for this study. While it provides granular transaction data, all transactions and associated credit or debit card details have undergone rigorous anonymization to safeguard consumer privacy. Specific details about the merchants (like location and brand) within the Spend-Ohio dataset were masked from the study. All information regarding merchants and consumers was handled with strict confidentiality, ensuring that no privacy boundaries were breached. No credit information of merchants and consumers is involved in this paper.

Additionally, the TFNSW dataset used in the experiment is a publicly available dataset that contains neither personal nor private details. The dataset only incorporates generic traffic flow without identifiable details, without specific identifiable details such as license plate numbers or exact timestamps of certain car passes.

<span id="page-8-0"></span>SSTKG: Simple Spatio-Temporal Knowledge Graph for Intepretable and Versatile Dynamic Information Embedding WWW '24, MAY 13 - 17, 2024, Singapore

#### ACKNOWLEDGMENTS

We acknowledge the support of Cisco Research Gift (CG# 75677887), the Australian Research Council (ARC) Centre of Excellence for Automated Decision-Making and Society (ADM+S) (CE200100005), and the resources and services from the National Computational Infrastructure (NCI), which is supported by the Australian Government.

#### REFERENCES

- <span id="page-8-7"></span>[1] Luyi Bai, Xiangnan Ma, Mingcheng Zhang, and Wenting Yu. 2021. Tpmod: a tendency-guided prediction model for temporal knowledge graph completion. ACM Transactions on Knowledge Discovery from Data, 15, 3, 1–17.
- <span id="page-8-23"></span>[2] Shaojie Bai, J Zico Kolter, and Vladlen Koltun. 2018. An empirical evaluation of generic convolutional and recurrent networks for sequence modeling. arXiv preprint arXiv:1803.01271.
- <span id="page-8-4"></span>[3] Antoine Bordes, Nicolas Usunier, Alberto Garcia-Duran, Jason Weston, and Oksana Yakhnenko. 2013. Translating embeddings for modeling multi-relational data. Advances in neural information processing systems, 26.
- <span id="page-8-17"></span>[4] Borui Cai, Yong Xiang, Longxiang Gao, He Zhang, Yunfeng Li, and Jianxin Li. 2022. Temporal knowledge graph completion: a survey. arXiv preprint arXiv:2201.08236.
- <span id="page-8-13"></span>[5] Wei Chen, Huaiyu Wan, Shengnan Guo, Haoyu Huang, Shaojie Zheng, Jiamu Li, Shuohao Lin, and Youfang Lin. 2022. Building and exploiting spatial–temporal knowledge graph for next poi recommendation. Knowledge-Based Systems, 258, 109951.
- <span id="page-8-5"></span>[6] Zhe Chen, Yuehan Wang, Bin Zhao, Jing Cheng, Xin Zhao, and Zongtao Duan. 2020. Knowledge graph completion: a review. Ieee Access, 8, 192435–192456.
- <span id="page-8-21"></span>[7] Kyunghyun Cho, Bart Van Merriënboer, Dzmitry Bahdanau, and Yoshua Bengio. 2014. On the properties of neural machine translation: encoder-decoder approaches. arXiv preprint arXiv:1409.1259.
- <span id="page-8-22"></span>[8] Junyoung Chung, Caglar Gulcehre, KyungHyun Cho, and Yoshua Bengio. 2014. Empirical evaluation of gated recurrent neural networks on sequence modeling. arXiv preprint arXiv:1412.3555.
- <span id="page-8-37"></span>[9] Giovanni Luca Ciampaglia, Prashant Shiralkar, Luis M Rocha, Johan Bollen, Filippo Menczer, and Alessandro Flammini. 2015. Computational fact checking from knowledge networks. PloS one, 10, 6, e0128193.
- <span id="page-8-28"></span>[10] Michaël Defferrard, Xavier Bresson, and Pierre Vandergheynst. 2016. Convolutional neural networks on graphs with fast localized spectral filtering. Advances in neural information processing systems, 29.
- <span id="page-8-29"></span>[11] Frederik Diehl, Thomas Brunner, Michael Truong Le, and Alois Knoll. 2019. Graph neural networks for modelling traffic participant interaction. In 2019 IEEE Intelligent Vehicles Symposium (IV). IEEE, 695–701.
- <span id="page-8-2"></span>[12] Laura Dietz, Alexander Kotov, and Edgar Meij. 2018. Utilizing knowledge graphs for text-centric information retrieval. In The 41st international ACM SIGIR conference on research & development in information retrieval, 1387–1390.
- <span id="page-8-16"></span>[13] Alberto Garcıéa-Durán, Sebastijan Dumančić, and Mathias Niepert. 2018. Learning sequence encoders for temporal knowledge graph completion. arXiv preprint arXiv:1809.03202.
- <span id="page-8-38"></span>[14] Xingtong Ge, Yi Yang, Jiahui Chen, Weichao Li, Zhisheng Huang, Wenyue Zhang, and Ling Peng. 2022. Disaster prediction knowledge graph based on multi-source spatio-temporal information. Remote Sensing, 14, 5, 1214.
- <span id="page-8-20"></span>[15] Felix A Gers, Nicol N Schraudolph, and Jürgen Schmidhuber. 2002. Learning precise timing with lstm recurrent networks. Journal of machine learning research, 3, Aug, 115–143.
- <span id="page-8-8"></span>[16] Rishab Goel, Seyed Mehran Kazemi, Marcus Brubaker, and Pascal Poupart. 2020. Diachronic embedding for temporal knowledge graph completion. In Proceedings of the AAAI conference on artificial intelligence number 04. Vol. 34, 3988–3995.
- <span id="page-8-32"></span>[17] Haoyu Han, Mengdi Zhang, Min Hou, Fuzheng Zhang, Zhongyuan Wang, Enhong Chen, Hongwei Wang, Jianhui Ma, and Qi Liu. 2020. Stgcn: a spatialtemporal aware graph learning method for poi recommendation. In 2020 IEEE International Conference on Data Mining (ICDM). IEEE, 1052–1057.
- <span id="page-8-33"></span>[18] Xinge Han, Xiaofeng Hu, Huanggang Wu, Bing Shen, and Jiansong Wu. 2020. Risk prediction of theft crimes in urban communities: an integrated model of lstm and st-gcn. IEEE Access, 8, 217222–217230.
- <span id="page-8-18"></span>[19] Marti A. Hearst, Susan T Dumais, Edgar Osuna, John Platt, and Bernhard Scholkopf. 1998. Support vector machines. IEEE Intelligent Systems and their applications, 13, 4, 18–28.
- <span id="page-8-3"></span>[20] Xiao Huang, Jingyuan Zhang, Dingcheng Li, and Ping Li. 2019. Knowledge graph embedding based question answering. In Proceedings of the twelfth ACM international conference on web search and data mining, 105–113.
- <span id="page-8-34"></span>[21] Ryan Keisler. 2022. Forecasting global weather with graph neural networks. arXiv preprint arXiv:2202.07575.

- <span id="page-8-15"></span>[22] Timothée Lacroix, Guillaume Obozinski, and Nicolas Usunier. 2020. Tensor decompositions for temporal knowledge base completion. arXiv preprint arXiv:2004.04926.
- <span id="page-8-14"></span>[23] Julien Leblay and Melisachew Wudage Chekol. 2018. Deriving validity time in knowledge graph. In Companion Proceedings of the The Web Conference 2018, 1771–1776.
- <span id="page-8-6"></span>[24] Lifan Lin and Kun She. 2020. Tensor decomposition-based temporal knowledge graph embedding. In 2020 IEEE 32nd International Conference on Tools with Artificial Intelligence (ICTAI). IEEE, 969–975.
- <span id="page-8-9"></span>[25] Johannes Messner, Ralph Abboud, and Ismail Ilkan Ceylan. 2022. Temporal knowledge graph completion using box embeddings. In Proceedings of the AAAI Conference on Artificial Intelligence number 7. Vol. 36, 7779–7787.
- <span id="page-8-41"></span>[26] Enrico Palumbo, Diego Monti, Giuseppe Rizzo, Raphaël Troncy, and Elena Baralis. 2020. Entity2rec: property-specific knowledge graph embeddings for item recommendation. Expert Systems with Applications, 151, 113235.
- <span id="page-8-19"></span>[27] Thanapant Raicharoen, Chidchanok Lursinsap, and Paron Sanguanbhokai. 2003. Application of critical support vector machine to time series prediction. In Proceedings of the 2003 International Symposium on Circuits and Systems, 2003. ISCAS'03. Vol. 5. IEEE, V–V.
- <span id="page-8-42"></span>[28] Xiao Sha, Zhu Sun, and Jie Zhang. 2021. Hierarchical attentive knowledge graph embedding for personalized recommendation. Electronic Commerce Research and Applications, 48, 101071.
- <span id="page-8-24"></span>[29] Renzhuo Wan, Shuping Mei, Jun Wang, Min Liu, and Fan Yang. 2019. Multivariate temporal convolutional network: a deep neural networks approach for multivariate time series forecasting. Electronics, 8, 8, 876.
- <span id="page-8-1"></span>[30] Hongwei Wang, Miao Zhao, Xing Xie, Wenjie Li, and Minyi Guo. 2019. Knowledge graph convolutional networks for recommender systems. In The world wide web conference, 3307–3313.
- <span id="page-8-39"></span>[31] Huandong Wang, Qiaohong Yu, Yu Liu, Depeng Jin, and Yong Li. 2021. Spatiotemporal urban knowledge graph enabled mobility prediction. Proceedings of the ACM on interactive, mobile, wearable and ubiquitous technologies, 5, 4, 1–24.
- <span id="page-8-10"></span>[32] Jingyuan Wang, Jiawei Jiang, Wenjun Jiang, Chengkai Han, and Wayne Xin Zhao. 2023. Towards efficient and comprehensive urban spatial-temporal prediction: a unified library and performance benchmark. arXiv preprint arXiv:2304.14343.
- <span id="page-8-35"></span>[33] Quanyu Wang, Kaixiang Zhang, and Manjotho Ali Asghar. 2022. Skeletonbased st-gcn for human action recognition with extended skeleton graph and partitioning strategy. IEEE Access, 10, 41403–41410.
- <span id="page-8-40"></span>[34] Xiang Wang, Dingxian Wang, Canran Xu, Xiangnan He, Yixin Cao, and Tat-Seng Chua. 2019. Explainable reasoning over knowledge graphs for recommendation. In Proceedings of the AAAI conference on artificial intelligence number 01. Vol. 33, 5329–5336.
- <span id="page-8-31"></span>[35] Xiaoyang Wang, Yao Ma, Yiqi Wang, Wei Jin, Xin Wang, Jiliang Tang, Caiyan Jia, and Jian Yu. 2020. Traffic flow prediction via spatial temporal graph neural network. In Proceedings of the web conference 2020, 1082–1092.
- <span id="page-8-11"></span>[36] Billy M Williams and Lester A Hoel. 2003. Modeling and forecasting vehicular traffic flow as a seasonal arima process: theoretical basis and empirical results. Journal of transportation engineering, 129, 6, 664–672.
- <span id="page-8-30"></span>[37] Yi Xie, Yun Xiong, and Yangyong Zhu. 2020. Sast-gnn: a self-attention based spatio-temporal graph neural network for traffic prediction. In Database Systems for Advanced Applications: 25th International Conference, DASFAA 2020, Jeju, South Korea, September 24–27, 2020, Proceedings, Part I 25. Springer, 707– 714.
- <span id="page-8-27"></span>[38] Bing Yu, Haoteng Yin, and Zhanxing Zhu. 2017. Spatio-temporal graph convolutional networks: a deep learning framework for traffic forecasting. arXiv preprint arXiv:1709.04875.
- <span id="page-8-36"></span>[39] Xiangxiang Zeng, Xinqi Tu, Yuansheng Liu, Xiangzheng Fu, and Yansen Su. 2022. Toward better drug discovery with knowledge graph. Current opinion in structural biology, 72, 114–126.
- <span id="page-8-26"></span>[40] Ling Zhao, Yujiao Song, Chao Zhang, Yu Liu, Pu Wang, Tao Lin, Min Deng, and Haifeng Li. 2019. T-gcn: a temporal graph convolutional network for traffic prediction. IEEE transactions on intelligent transportation systems, 21, 9, 3848– 3858.
- <span id="page-8-25"></span>[41] Jie Zhou, Ganqu Cui, Shengding Hu, Zhengyan Zhang, Cheng Yang, Zhiyuan Liu, Lifeng Wang, Changcheng Li, and Maosong Sun. 2020. Graph neural networks: a review of methods and applications. AI open, 1, 57–81.
- <span id="page-8-12"></span>[42] Jiawei Zhu, Xing Han, Hanhan Deng, Chao Tao, Ling Zhao, Pu Wang, Tao Lin, and Haifeng Li. 2022. Kst-gcn: a knowledge-driven spatial-temporal graph convolutional network for traffic forecasting. IEEE Transactions on Intelligent Transportation Systems, 23, 9, 15055–15065.
