---
cite_key: hildebrandt_2014
title: TLogic: Temporal Logical Rules for Explainable Link Forecasting on Temporal Knowledge Graphs
authors: Marcel Hildebrandt, Mitchell Joblin
year: 2014
date_processed: '2025-07-02'
phase2_processed: true
original_folder: arxiv_2112.08025_TLogic_Temporal_Logical_Rules_for_Explainable_Link_Forecasting_on_Temporal_Knowledge_Graphs
images_total: 7
images_kept: 7
images_removed: 0
tags:
- Decision Support
- Healthcare
- Knowledge Graph
- Machine Learning
- Recommendation System
- Semantic Web
- Temporal
keywords:
- ComplEx
- DistMult
- StreamLearner
- acknowledgement
- analysis
- angela merkel
- any-burl
- artificial intelligence
- barack obama
- best-performing
- black-box
- bottom-up
- candidate ranking
- clinical decision support
- collective learning
- composition-based
- composition-based multi
- consult
- continuous-time
- copy-generation
- cyclic temporal logical rule
- datasets
- de-simple
- deep learning
- discuss by telephone
- during learning
- efficiency
- embedding-based
- entity
- experiments
---

# TLogic: Temporal Logical Rules for Explainable Link Forecasting on Temporal Knowledge Graphs

Yushan Liu1,2, Yunpu Ma1,2, Marcel Hildebrandt<sup>1</sup> , Mitchell Joblin<sup>1</sup> , Volker Tresp1,2

> <sup>1</sup>Siemens AG, Otto-Hahn-Ring 6, 81739 Munich, Germany {firstname.lastname}@siemens.com

<sup>2</sup>Ludwig Maximilian University of Munich, Geschwister-Scholl-Platz 1, 80539 Munich, Germany

## Abstract

Conventional static knowledge graphs model entities in relational data as nodes, connected by edges of specific relation types. However, information and knowledge evolve continuously, and temporal dynamics emerge, which are expected to influence future situations. In temporal knowledge graphs, time information is integrated into the graph by equipping each edge with a timestamp or a time range. Embeddingbased methods have been introduced for link prediction on temporal knowledge graphs, but they mostly lack explainability and comprehensible reasoning chains. Particularly, they are usually not designed to deal with link forecasting – event prediction involving future timestamps. We address the task of link forecasting on temporal knowledge graphs and introduce TLogic, an explainable framework that is based on temporal logical rules extracted via temporal random walks. We compare TLogic with state-of-the-art baselines on three benchmark datasets and show better overall performance while our method also provides explanations that preserve time consistency. Furthermore, in contrast to most state-ofthe-art embedding-based methods, TLogic works well in the inductive setting where already learned rules are transferred to related datasets with a common vocabulary.

## Introduction

Knowledge graphs (KGs) structure factual information in the form of triples (es, r, eo), where e<sup>s</sup> and e<sup>o</sup> correspond to entities in the real world and r to a binary relation, e. g., *(Anna, born in, Paris)*. This knowledge representation leads to an interpretation as a directed multigraph, where entities are identified with nodes and relations with edge types. Each edge (es, r, eo) in the KG encodes an observed fact, where the source node e<sup>s</sup> corresponds to the subject entity, the target node e<sup>o</sup> to the object entity, and the edge type r to the predicate of the factual statement.

Some real-world information also includes a temporal dimension, e. g., the event *(Anna, born in, Paris)*happened on a specific date. To model the large amount of available event data that induce complex interactions between entities over time, temporal knowledge graphs (tKGs) have been introduced. Temporal KGs extend the triples to quadruples (es, r, eo, t) to integrate a timestamp or time range t, where t

<span id="page-0-0"></span>![](_page_0_Figure_10.jpeg)
<!-- Image Description: This image is a directed graph illustrating diplomatic interactions among France, Germany, the USA, and China. Nodes represent countries (represented by flags) and Angela Merkel/Barack Obama (represented by portraits). Edges show communication types (e.g., "consult," "visit," "negotiate") and dates. The graph's purpose is to visually represent the sequence and nature of diplomatic engagements during a specific period. The dotted blue arrow indicates a less formal communication channel. -->

**Figure 1:** A subgraph from the dataset ICEWS14 with the entities*Angela Merkel, Barack Obama, France*, and *China*. The timestamps are displayed in the format yy/mm/dd. The dotted blue line represents the correct answer to the query *(Angela Merkel, consult, ?, 2014/08/09)*. Previous interactions between *Angela Merkel*and*Barack Obama*can be interpreted as an explanation for the prediction.

indicates the time validity of the static event (es, r, eo), e. g.,*(Angela Merkel, visit, China, 2014/07/04)*. Figure [1](#page-0-0) visualizes a subgraph from the dataset ICEWS14 as an example of a tKG. In this work, we focus on tKGs where each edge is equipped with a single timestamp.

One of the common tasks on KGs is link prediction, which finds application in areas such as recommender systems [\(Hildebrandt et al. 2019\)](#page-7-0), knowledge base completion [\(Nguyen et al. 2018a\)](#page-7-1), and drug repurposing [\(Liu et al.](#page-7-2) [2021\)](#page-7-2). Taking the additional temporal dimension into account, it is of special interest to forecast events for future timestamps based on past information. Notable real-world applications that rely on accurate event forecasting are, e. g., clinical decision support, supply chain management, and extreme events modeling. In this work, we address link forecasting on tKGs, where we consider queries (es, r, ?, t) for a timestamp t that has not been seen during training.

Copyright © 2022, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

Several embedding-based methods have been introduced for tKGs to solve link prediction and forecasting (link prediction with future timestamps), e.g., TTransE [\(Leblay](#page-7-3) [and Chekol 2018\)](#page-7-3), TNTComplEx [\(Lacroix, Obozinski, and](#page-7-4) [Usunier 2020\)](#page-7-4), and RE-Net [\(Jin et al. 2019\)](#page-7-5). The underlying principle is to project the entities and relations into a lowdimensional vector space while preserving the topology and temporal dynamics of the tKG. These methods can learn the complex patterns that lead to an event but often lack transparency and interpretability.

To increase the transparency and trustworthiness of the solutions, human-understandable explanations are necessary, which can be provided by logical rules. However, the manual creation of rules is often difficult due to the complex nature of events. Domain experts cannot articulate the conditions for the occurrence of an event sufficiently formally to express this knowledge as rules, which leads to a problem termed as the knowledge acquisition bottleneck. Generally, symbolic methods that make use of logical rules tend to suffer from scalability issues, which make them impractical for the application on large real-world datasets.

We propose TLogic that automatically mines cyclic temporal logical rules by extracting temporal random walks from the graph. We achieve both high predictive performance and time-consistent explanations in the form of temporal rules, which conform to the observation that the occurrence of an event is usually triggered by previous events. The main contributions of this work are summarized as follows:

- We introduce TLogic, a novel symbolic framework based on temporal random walks in temporal knowledge graphs. It is the first approach that directly learns temporal logical rules from tKGs and applies these rules to the link forecasting task.
- Our approach provides explicit and human-readable explanations in the form of temporal logical rules and is scalable to large datasets.
- We conduct experiments on three benchmark datasets (ICEWS14, ICEWS18, and ICEWS0515) and show better overall performance compared with state-of-the-art baselines.
- We demonstrate the effectiveness of our method in the inductive setting where our learned rules are transferred to a related dataset with a common vocabulary.

## Related Work

Subsymbolic machine learning methods, e. g., embeddingbased algorithms, have achieved success for the link prediction task on static KGs. Well-known methods include RESCAL [\(Nickel, Tresp, and Kriegel 2011\)](#page-7-6), TransE [\(Bor](#page-7-7)[des et al. 2013\)](#page-7-7), DistMult [\(Yang et al. 2015\)](#page-7-8), and ComplEx [\(Trouillon et al. 2016\)](#page-7-9) as well as the graph convolutional approaches R-GCN [\(Schlichtkrull et al. 2018\)](#page-7-10) and CompGCN [\(Vashishth et al. 2020\)](#page-7-11). Several approaches have been recently proposed to handle tKGs, such as TTransE [\(Leblay and Chekol 2018\)](#page-7-3), TA-DistMult [\(Garc´ıa-](#page-7-12)[Duran, Duman](#page-7-12) ´ ci˘ c, and Niepert [2018\)](#page-7-12), DE-SimplE [\(Goel](#page-7-13) ´ [et al. 2020\)](#page-7-13), TNTComplEx [\(Lacroix, Obozinski, and](#page-7-4) [Usunier 2020\)](#page-7-4), CyGNet [\(Zhu et al. 2021\)](#page-7-14), RE-Net [\(Jin et al.](#page-7-5) [2019\)](#page-7-5), and xERTE [\(Han et al. 2021\)](#page-7-15). The main idea of these methods is to explicitly learn embeddings for timestamps or to integrate temporal information into the entity or relation embeddings. However, the black-box property of embeddings makes it difficult for humans to understand the predictions. Moreover, approaches with shallow embeddings are not suitable for an inductive setting with previously unseen entities, relations, or timestamps. From the above methods, only CyGNet, RE-Net, and xERTE are designed for the forecasting task. xERTE is also able to provide explanations by extracting relevant subgraphs around the query subject.

Symbolic approaches for link prediction on KGs like AMIE+ [\(Galarraga et al. 2015\)](#page-7-16) and AnyBURL [\(Meilicke](#page-7-17) ´ [et al. 2019\)](#page-7-17) mine logical rules from the dataset, which are then applied to predict new links. StreamLearner [\(Omran,](#page-7-18) [Wang, and Wang 2019\)](#page-7-18) is one of the first methods for learning temporal rules. It employs a static rule learner to generate rules, which are then generalized to the temporal domain. However, they only consider a rather restricted set of temporal rules, where all body atoms have the same timestamp.

Another class of approaches is based on random walks in the graph, where the walks can support an interpretable explanation for the predictions. For example, AnyBURL samples random walks for generating rules. The methods dynnode2vec [\(Mahdavi, Khoshraftar, and An 2018\)](#page-7-19) and change2vec [\(Bian et al. 2019\)](#page-7-20) alternately extract random walks on tKG snapshots and learn parameters for node embeddings, but they do not capture temporal patterns within the random walks. [Nguyen et al.](#page-7-21) [\(2018b\)](#page-7-21) extend the concept of random walks to temporal random walks on continuous-time dynamic networks for learning node embeddings, where the sequence of edges in the walk only moves forward in time.

## Preliminaries

Let [n] := {1, 2, . . . , n}.

Temporal knowledge graph Let E denote the set of entities, R the set of relations, and T the set of timestamps.

A *temporal knowledge graph*(tKG) is a collection of facts G ⊂ E × R × E × T , where each fact is represented by a quadruple (es, r, eo, t). The quadruple (es, r, eo, t) is also called link or edge, and it indicates a connection between the subject entity e<sup>s</sup> ∈ E and the object entity e<sup>o</sup> ∈ E via the relation r ∈ R. The timestamp t ∈ T implies the occurrence of the event (es, r, eo) at time t, where t can be measured in units such as hour, day, and year.

For two timestamps t and tˆ, we denote the fact that t occurs earlier than tˆby t < tˆ. If additionally, t could represent the same time as tˆ, we write t ≤ tˆ.

We define for each edge (es, r, eo, t) an inverse edge (eo, r<sup>−</sup><sup>1</sup> , es, t) that interchanges the positions of the subject and object entity to allow the random walker to move along the edge in both directions. The relation r <sup>−</sup><sup>1</sup> ∈ R is called the inverse relation of r.

Link forecasting The goal of the*link forecasting*task is to predict new links for future timestamps. Given a query with a previously unseen timestamp (es, r, ?, t), we want to

identify a ranked list of object candidates that are most likely to complete the query. For subject prediction, we formulate the query as (eo, r−<sup>1</sup> , ?, t).

Temporal random walk A*non-increasing temporal random walk*W of length l ∈ N from entity el+1 ∈ E to entity e<sup>1</sup> ∈ E in the tKG G is defined as a sequence of edges

$$
((e_{l+1}, r_l, e_l, t_l), (e_l, r_{l-1}, e_{l-1}, t_{l-1}), \ldots, (e_2, r_1, e_1, t_1))
$$

with $t_l \ge t_{l-1} \ge \cdots \ge t_1$ , (1)

where (ei+1, r<sup>i</sup> , e<sup>i</sup> , ti) ∈ G for i ∈ [l].

A non-increasing temporal random walk complies with time constraints so that the edges are traversed only backward in time, where it is also possible to walk along edges with the same timestamp.

Temporal logical rule Let E<sup>i</sup> and T<sup>i</sup> for i ∈ [l+1] be variables that represent entities and timestamps, respectively. Further, let r1, r2, . . . , r<sup>l</sup> , r<sup>h</sup> ∈ R be fixed.

A*cyclic temporal logical rule*R of length l ∈ N is defined as

$$
((E_1,r_h,E_{l+1},T_{l+1}) \leftarrow \wedge_{i=1}^l (E_i,r_i,E_{i+1},T_i))
$$

with the temporal constraints

$$
T_1 \leq T_2 \leq \cdots \leq T_l < T_{l+1}.\tag{2}
$$

The left-hand side of R is called the rule head, with r<sup>h</sup> being the head relation, while the right-hand side is called the rule body, which is represented by a conjunction of body atoms (E<sup>i</sup> , r<sup>i</sup> , Ei+1, Ti). The rule is called cyclic because the rule head and the rule body constitute two different walks connecting the same two variables E<sup>1</sup> and El+1. A temporal rule implies that if the rule body holds with the temporal constraints given by [\(2\)](#page-2-0), then the rule head is true as well for a future timestamp Tl+1.

The replacement of the variables E<sup>i</sup> and T<sup>i</sup> by constant terms is called grounding or instantiation. For example, a grounding of the temporal rule

((E1,*consult*, E2, T2) ← (E1, *discuss by telephone*, E2, T1))

is given by the edges *(Angela Merkel, discuss by telephone, Barack Obama, 2014/07/22)*and*(Angela Merkel, consult, Barack Obama, 2014/08/09)*in Figure [1.](#page-0-0) Let rule grounding refer to the replacement of the variables in the entire rule and body grounding refer to the replacement of the variables only in the body, where all groundings must comply with the temporal constraints in [\(2\)](#page-2-0).

In many domains, logical rules are frequently violated so that confidence values are determined to estimate the probability of a rule's correctness. We adapt the standard confidence to take timestamp values into account. Let (r1, r2, . . . , r<sup>l</sup> , rh) be the relations in a rule R. The body support is defined as the number of body groundings, i. e., the number of tuples (e1, . . . , el+1, t1, . . . , tl) such that (e<sup>i</sup> , r<sup>i</sup> , ei+1, ti) ∈ G for i ∈ [l] and t<sup>i</sup> ≤ ti+1 for i ∈ [l − 1]. The rule support is defined as the number of body groundings such that there exists a timestamp tl+1 > t<sup>l</sup> with (e1, rh, el+1, tl+1) ∈ G. The confidence of the rule R, denoted by conf(R), can then be obtained by dividing the rule support by the body support.

<span id="page-2-1"></span>Algorithm 1: Rule learning

Input: Temporal knowledge graph G.

Parameters: Rule lengths L ⊂ N, number of temporal random walks n ∈ N, transition distribution d ∈ {unif, exp}. Output: Temporal logical rules T R.

- 1: for relation r ∈ R do
- <span id="page-2-2"></span>2: for l ∈ L do
- 3: for i ∈ [n] do
- 4: T R<sup>l</sup> <sup>r</sup> ← ∅
- 5: According to transition distribution d, sample a temporal random walk W of length l + 1 with tl+1 > t<sup>l</sup> . . See [\(4\)](#page-3-0).
- 6: Transform walk W to the corresponding temporal logical rule R. . See [\(5\)](#page-3-1).

7: Estimate the confidence of rule
$$
R
$$
.

8: T R<sup>l</sup> <sup>r</sup> ← T R<sup>l</sup> <sup>r</sup> ∪ {(R, conf(R))}

r

9: T R<sup>r</sup> ← ∪l∈LT R<sup>l</sup>

10: T R ← ∪r∈RT R<sup>r</sup>

11: return T R

## Our Framework

We introduce TLogic, a rule-based link forecasting framework for tKGs. TLogic first extracts temporal walks from the graph and then lifts these walks to a more abstract, semantic level to obtain temporal rules that generalize to new data. The application of these rules generates answer candidates, for which the body groundings in the graph serve as explicit and human-readable explanations. Our framework consists of the components rule learning and rule application. The pseudocode for rule learning is shown in Algorithm [1](#page-2-1) and for rule application in Algorithm [2.](#page-3-2)

## Rule Learning

As the first step of rule learning, temporal walks are extracted from the tKG G. For a rule of length l, a walk of length l + 1 is sampled, where the additional step corresponds to the rule head.

Let r<sup>h</sup> be a fixed relation, for which we want to learn rules. For the first sampling step m = 1, we sample an edge (e1, rh, el+1, tl+1), which will serve as the rule head, uniformly from all edges with relation type rh. A temporal random walker then samples iteratively edges adjacent to the current object until a walk of length l + 1 is obtained.

For sampling step m ∈ {2, . . . , l+ 1}, let (es, r, e ˜ <sup>o</sup>, t) denote the previously sampled edge and A(m, eo, t) the set of feasible edges for the next transition. To fulfill the temporal constraints in [\(1\)](#page-2-2) and [\(2\)](#page-2-0), we define

$$
\mathcal{A}(m, e_o, t) :=
$$
\n
$$
\begin{cases}\n\{(e_o, r, e, \hat{t}) \mid (e_o, r, e, \hat{t}) \in \mathcal{G}, \ \hat{t} < t\} & \text{if } m = 2, \\
\{(e_o, r, e, \hat{t}) \mid (e_o, r, e, \hat{t}) \in \tilde{\mathcal{G}}, \ \hat{t} \le t\} & \text{if } m \in \{3, \ldots, l\}, \\
\{(e_o, r, e_1, \hat{t}) \mid (e_o, r, e_1, \hat{t}) \in \tilde{\mathcal{G}}, \ \hat{t} \le t\} & \text{if } m = l + 1,\n\end{cases}
$$

where G˜ := G \ {(eo, r˜ −1 , es, t)} excludes the inverse edge to avoid redundant rules. For obtaining cyclic walks, we sample in the last step m = l + 1 an edge that connects the walk to the first entity e<sup>1</sup> if such edges exist. Otherwise, we sample the next walk.

The transition distribution for sampling the next edge can either be uniform or exponentially weighted. We define an index mapping mˆ := (l + 1) − (m − 2) to be consistent with the indices in [\(1\)](#page-2-2). Then, the exponentially weighted probability for choosing edge u ∈ A (m, em<sup>ˆ</sup> , tm<sup>ˆ</sup> ) for m ∈ {2, . . . , l + 1} is given by

$$
\mathbb{P}(u; m, e_{\hat{m}}, t_{\hat{m}}) = \frac{\exp(t_u - t_{\hat{m}})}{\sum_{\hat{u} \in \mathcal{A}(m, e_{\hat{m}}, t_{\hat{m}})} \exp(t_{\hat{u}} - t_{\hat{m}})}
$$
(3)

where t<sup>u</sup> denotes the timestamp of edge u. The exponential weighting favors edges with timestamps that are closer to the timestamp of the previous edge and probably more relevant for prediction.

The resulting temporal walk W is given by

$$
((e_1, r_h, e_{l+1}, t_{l+1}), (e_{l+1}, r_l, e_l, t_l), \ldots, (e_2, r_1, e_1, t_1)).
$$
(4)

W can then be transformed to a temporal rule R by replacing the entities and timestamps with variables. While the first edge in W becomes the rule head (E1, rh, El+1, Tl+1), the other edges are mapped to body atoms, where each edge (ei+1, r<sup>i</sup> , e<sup>i</sup> , ti) is converted to the body atom (E<sup>i</sup> , r<sup>−</sup><sup>1</sup> i , Ei+1, Ti). The final rule R is denoted by

$$
((E_1, r_h, E_{l+1}, T_{l+1}) \leftarrow \wedge_{i=1}^l (E_i, r_i^{-1}, E_{i+1}, T_i)).
$$
(5)

In addition, we impose the temporal consistency constraints T<sup>1</sup> ≤ T<sup>2</sup> ≤ · · · ≤ T<sup>l</sup> < Tl+1.

The entities (e1, . . . , el+1) in W do not need to be distinct since a pair of entities can have many interactions at different points in time. For example, Angela Merkel made several visits to China in 2014, which could constitute important information for the prediction. Repetitive occurrences of the same entity in W are replaced with the same random variable in R to maintain this knowledge.

For the confidence estimation of R, we sample from the graph a fixed number of body groundings, which have to match the body relations and the variable constraints mentioned in the last paragraph while satisfying the condition from [\(2\)](#page-2-0). The number of unique bodies serves as the body support. The rule support is determined by counting the number of bodies for which an edge with relation type r<sup>h</sup> exists that connects e<sup>1</sup> and el+1 from the body. Moreover, the timestamp of this edge has to be greater than all body timestamps to fulfill [\(2\)](#page-2-0).

For every relation r ∈ R, we sample n ∈ N temporal walks for a set of prespecified lengths L ⊂ N. The set T R<sup>l</sup> r stands for all rules of length l with head relation r with their corresponding confidences. All rules for relation r are included in T R<sup>r</sup> := ∪l∈LT R<sup>l</sup> r , and the complete set of learned temporal rules is given by T R := ∪r∈RT Rr.

It is possible to learn rules only for a single relation or a set of specific relations of interest. Explicitly learning rules for all relations is especially effective for rare relations that would otherwise only be sampled with a small probability. The learned rules are not specific to the graph from which

### <span id="page-3-2"></span>Algorithm 2: Rule application

Input: Test query q = (e q , r<sup>q</sup> , ?, t<sup>q</sup> ), temporal logical rules T R, temporal knowledge graph G.

Parameters: Time window w ∈ N ∪ {∞}, minimum number of candidates k, score function f.

Output: Answer candidates C.

$$
1: \ \mathcal{C} \leftarrow \emptyset
$$

- . Apply the rules in T R by decreasing confidence.
- 2: if T R<sup>r</sup> <sup>q</sup> 6= ∅ then
- 3: for rule R ∈ T R<sup>r</sup> <sup>q</sup> do
- 4: Find all body groundings of R in SG ⊂ G, where SG consists of the edges within the time window [t <sup>q</sup> − w, t<sup>q</sup> ).
- 5: Retrieve candidates C(R) from the target entities of the body groundings.
- 6: for c ∈ C(R) do
- 7: Calculate score f(R, c). . See [\(6\)](#page-3-3).

8:
$$
\mathcal{C} \leftarrow \mathcal{C} \cup \{(c, f(R, c))\}
$$

9: if |{c | ∃R : (c, f(R, c)) ∈ C}| ≥ k then

10: break

11: return C

they have been extracted, but they could be employed in an inductive setting where the rules are transferred to related datasets that share a common vocabulary for straightforward application.

### Rule Application

The learned temporal rules T R are applied to answer queries of the form q = (e q , r<sup>q</sup> , ?, t<sup>q</sup> ). The answer candidates are retrieved from the target entities of body groundings in the tKG G. If there exist no rules T R<sup>r</sup> <sup>q</sup> for the query relation r q , or if there are no matching body groundings in the graph, then no answers are predicted for the given query.

To apply the rules on relevant data, a subgraph SG ⊂ G dependent on a time window w ∈ N ∪ {∞} is retrieved. For w ∈ N, the subgraph SG contains all edges from G that have timestamps t ∈ [t <sup>q</sup> − w, t<sup>q</sup> ). If w = ∞, then all edges with timestamps prior to the query timestamp t q are used for rule application, i. e., SG consists of all facts with t ∈ [tmin, t<sup>q</sup> ), where tmin is the minimum timestamp in the graph G.

We apply the rules T R<sup>r</sup> <sup>q</sup> by decreasing confidence, where each rule R generates a set of answer candidates C(R). Each candidate c ∈ C(R) is then scored by a function f : T R<sup>r</sup> <sup>q</sup> × E → [0, 1] that reflects the probability of the candidate being the correct answer to the query.

Let B(R, c) be the set of body groundings of rule R that start at entity e q and end at entity c. We choose as score function f a convex combination of the rule's confidence and a function that takes the time difference t <sup>q</sup>−t1(B(R, c)) as input, where t1(B(R, c)) denotes the earliest timestamp t<sup>1</sup> in the body. If several body groundings exist, we take from all possible t<sup>1</sup> values the one that is closest to t q . For candidate c ∈ C(R), the score function is defined as

$$
f(R, c) = a \cdot \text{conf}(R) + (1 - a) \cdot \exp(-\lambda(t^q - t_1(\mathcal{B}(R, c)))) \tag{6}
$$

with $\lambda > 0$ and $a \in [0, 1]$ .

The intuition for this choice of f is that candidates generated by high-confidence rules should receive a higher score. Adding a dependency on the timeframe of the rule grounding is based on the observation that the existence of edges in a rule become increasingly probable with decreasing time difference between the edges. We choose the exponential distribution since it is commonly used to model interarrival times of events. The time difference t <sup>q</sup> − t1(B(R, c)) is always non-negative for a future timestamp value t q , and with the assumption that there exists a fixed mean, the exponential distribution is also the maximum entropy distribution for such a time difference variable. The exponential distribution is rescaled so that both summands are in the range [0, 1].

All candidates are saved with their scores as (c, f(R, c)) in C. We stop the rule application when the number of different answer candidates |{c | ∃R : (c, f(R, c)) ∈ C}| is at least k so that there is no need to go through all rules.

### Candidate Ranking

For the ranking of the answer candidates, all scores of each candidate c are aggregated through a noisy-OR calculation, which produces the final score

$$
1 - \Pi_{\{s \mid (c,s) \in \mathcal{C}\}}(1 - s). \tag{7}
$$

The idea is to aggregate the scores to produce a probability, where candidates implied by more rules should have a higher score.

In case there are no rules for the query relation r q , or if there are no matching body groundings in the graph, it might still be interesting to retrieve possible answer candidates. In the experiments, we apply a simple baseline where the scores for the candidates are obtained from the overall object distribution in the training data if r q is a new relation. If r q already exists in the training set, we take the object distribution of the edges with relation type r q .

## Experiments

## Datasets

We conduct experiments on the dataset Integrated Crisis Early Warning System[1](#page-4-0) (ICEWS), which contains information about international events and is a commonly used benchmark dataset for link prediction on tKGs. We choose the subsets ICEWS14, ICEWS18, and ICEWS0515, which include data from the years 2014, 2018, and 2005 to 2015, respectively. Since we consider link forecasting, each dataset is split into training, validation, and test set so that the timestamps in the training set occur earlier than the timestamps in the validation set, which again occur earlier than the timestamps in the test set. To ensure a fair comparison, we use the split provided by [Han et al.](#page-7-15) [\(2021\)](#page-7-15)[2](#page-4-1) . The statistics of the datasets are summarized in the supplementary material.

### Experimental Setup

For each test instance (e q s , r<sup>q</sup> , e<sup>q</sup> o , t<sup>q</sup> ), we generate a list of candidates for both object prediction (e q s , r<sup>q</sup> , ?, t<sup>q</sup> ) and subject prediction (e q o ,(r q ) −1 , ?, t<sup>q</sup> ). The candidates are ranked by decreasing scores, which are calculated according to [\(7\)](#page-4-2).

The confidence for each rule is estimated by sampling 500 body groundings and counting the number of times the rule head holds. We learn rules of the lengths 1, 2, and 3, and for application, we only consider the rules with a minimum confidence of 0.01 and minimum body support of 2.

We compute the mean reciprocal rank (MRR) and hits@k for k ∈ {1, 3, 10}, which are standard metrics for link prediction on KGs. For a rank x ∈ N, the reciprocal rank is defined as <sup>1</sup> x , and the MRR is the average of all reciprocal ranks of the correct query answers across all queries. The metric hits@k (h@k) indicates the proportion of queries for which the correct entity appears under the top k candidates.

Similar to [Han et al.](#page-7-15) [\(2021\)](#page-7-15), we perform time-aware filtering where all correct entities at the query timestamp except for the true query object are filtered out from the answers. In comparison to the alternative setting that filters out all other objects that appear together with the query subject and relation at any timestamp, time-aware filtering yields a more realistic performance estimate.

Baseline methods We compare TLogic[3](#page-4-3) with the state-ofthe-art baselines for static link prediction DistMult [\(Yang](#page-7-8) [et al. 2015\)](#page-7-8), ComplEx [\(Trouillon et al. 2016\)](#page-7-9), and Any-BURL [\(Meilicke et al. 2019,](#page-7-17) [2020\)](#page-7-22) as well as for temporal link prediction TTransE [\(Leblay and Chekol 2018\)](#page-7-3), TA-DistMult [\(Garc´ıa-Duran, Duman](#page-7-12) ´ ci˘ c, and Niepert [2018\)](#page-7-12), DE- ´ SimplE [\(Goel et al. 2020\)](#page-7-13), TNTComplEx [\(Lacroix, Obozin](#page-7-4)[ski, and Usunier 2020\)](#page-7-4), CyGNet [\(Zhu et al. 2021\)](#page-7-14), RE-Net [\(Jin et al. 2019\)](#page-7-5), and xERTE [\(Han et al. 2021\)](#page-7-15). All baseline results except for the results on AnyBURL are from [Han et al.](#page-7-15) [\(2021\)](#page-7-15). AnyBURL samples paths based on reinforcement learning and generalizes them to rules, where the rule space also includes, e. g., acyclic rules and rules with constants. A non-temporal variant of TLogic would sample paths randomly and only learn cyclic rules, which would presumably yield worse performance than AnyBURL. Therefore, we choose AnyBURL as a baseline to assess the effectiveness of adding temporal constraints.

### Results

The results of the experiments are displayed in Table [1.](#page-5-0) TLogic outperforms all baseline methods with respect to the metrics MRR, hits@3, and hits@10. Only xERTE performs better than Tlogic for hits@1 on the datasets ICEWS18 and ICEWS0515.

Besides a list of possible answer candidates with corresponding scores, TLogic can also provide temporal rules and body groundings in form of walks from the graph that support the predictions. Table [2](#page-6-0) presents three exemplary rules with high confidences that were learned from ICEWS14. For the query*(Angela Merkel, consult, ?, 2014/08/09)*, two

<span id="page-4-0"></span><sup>1</sup> <https://dataverse.harvard.edu/dataverse/icews>

<span id="page-4-1"></span><sup>2</sup> <https://github.com/TemporalKGTeam/xERTE>

<span id="page-4-3"></span><sup>3</sup>Code available at<https://github.com/liu-yushan/TLogic.>


| Dataset | ICEWS14 | | | ICEWS18 | | | ICEWS0515 | | | | | |
|--------------------------------------------------------------------------------|--------------------------------------------------------------------|--------------------------------------------------------------------|--------------------------------------------------------------------|--------------------------------------------------------------------|--------------------------------------------------------------------|--------------------------------------------------------------------|--------------------------------------------------------------------|--------------------------------------------------------------------|--------------------------------------------------------------------|--------------------------------------------------------------------|--------------------------------------------------------------------|--------------------------------------------------------------------|
| Model | MRR | h@1 | h@3 | h@10 | MRR | h@1 | h@3 | h@10 | MRR | h@1 | h@3 | h@10 |
| DistMult<br>ComplEx<br>AnyBURL | 0.2767<br>0.3084<br>0.2967 | 0.1816<br>0.2151<br>0.2126 | 0.3115<br>0.3448<br>0.3333 | 0.4696<br>0.4958<br>0.4673 | 0.1017<br>0.2101<br>0.2277 | 0.0452<br>0.1187<br>0.1510 | 0.1033<br>0.2347<br>0.2544 | 0.2125<br>0.3987<br>0.3891 | 0.2873<br>0.3169<br>0.3205 | 0.1933<br>0.2144<br>0.2372 | 0.3219<br>0.3574<br>0.3545 | 0.4754<br>0.5204<br>0.5046 |
| TTransE<br>TA-DistMult<br>DE-SimplE<br>TNTComplEx<br>CyGNet<br>RE-Net<br>xERTE | 0.1343<br>0.2647<br>0.3267<br>0.3212<br>0.3273<br>0.3828<br>0.4079 | 0.0311<br>0.1709<br>0.2443<br>0.2335<br>0.2369<br>0.2868<br>0.3270 | 0.1732<br>0.3022<br>0.3569<br>0.3603<br>0.3631<br>0.4134<br>0.4567 | 0.3455<br>0.4541<br>0.4911<br>0.4913<br>0.5067<br>0.5452<br>0.5730 | 0.0831<br>0.1675<br>0.1930<br>0.2123<br>0.2493<br>0.2881<br>0.2931 | 0.0192<br>0.0861<br>0.1153<br>0.1328<br>0.1590<br>0.1905<br>0.2103 | 0.0856<br>0.1841<br>0.2186<br>0.2402<br>0.2828<br>0.3244<br>0.3351 | 0.2189<br>0.3359<br>0.3480<br>0.3691<br>0.4261<br>0.4751<br>0.4648 | 0.1571<br>0.2431<br>0.3502<br>0.2754<br>0.3497<br>0.4297<br>0.4662 | 0.0500<br>0.1458<br>0.2591<br>0.1952<br>0.2567<br>0.3126<br>0.3784 | 0.1972<br>0.2792<br>0.3899<br>0.3080<br>0.3909<br>0.4685<br>0.5231 | 0.3802<br>0.4421<br>0.5275<br>0.4286<br>0.5294<br>0.6347<br>0.6392 |
| TLogic | 0.4304 | 0.3356 | 0.4827 | 0.6123 | 0.2982 | 0.2054 | 0.3395 | 0.4853 | 0.4697 | 0.3621 | 0.5313 | 0.6743 |

**Table 1:** Results of link forecasting on the datasets ICEWS14, ICEWS18, and ICEWS0515. All metrics are time-aware filtered. The best results among all models are displayed in bold.

<span id="page-5-1"></span>![](_page_5_Figure_2.jpeg)
<!-- Image Description: The image displays a line graph comparing two methods ("unif" and "exp") for generating random walks in a network. The x-axis represents the number of walks, and the y-axis shows the Mean Reciprocal Rank (MRR). The graph illustrates how MRR improves as the number of walks increases for both methods, with "exp" showing slightly higher MRR values. The purpose is to demonstrate the impact of walk generation strategies on the performance of a ranking task, likely within a recommendation or knowledge graph context. -->

**Figure 2:** MRR performance on the validation set of ICEWS14. The transition distribution is either uniform or exponentially weighted.

walks are shown in Table [2,](#page-6-0) which serve as time-consistent explanations for the correct answer *Barack Obama*.

Inductive setting One advantage of our learned logical rules is that they are applicable to any new dataset as long as the new dataset covers common relations. This might be relevant for cases where new entities appear. For example, Donald Trump, who served as president of the United States from 2017 to 2021, is included in the dataset ICEWS18 but not in ICEWS14. The logical rules are not tied to particular entities and would still be applicable, while embeddingbased methods have difficulties operating in this challenging setting. The models would need to be retrained to obtain embeddings for the new entities, where existing embeddings might also need to be adapted to the different time range.

For the two rule-based methods AnyBURL and TLogic, we apply the rules learned on the training set of ICEWS0515 (with timestamps from 2005/01/01 to 2012/08/06) to the test set of ICEWS14 as well as the rules learned on the training set of ICEWS14 to the test set of ICEWS18 (see Table [3\)](#page-6-1). The performance of TLogic in the inductive setting is for all metrics close to the results in Table [1,](#page-5-0) while for AnyBURL, especially the results on ICEWS18 drop significantly. It seems that the encoded temporal information in TLogic is essential for achieving correct predictions in the inductive setting. ICEWS14 has only 7,128 entities, while ICEWS18 contains 23,033 entities. The results confirm that temporal rules from TLogic can even be transferred to a dataset with a large number of new entities and timestamps and lead to a strong performance.

### Analysis

The results in this section are obtained on the dataset ICEWS14, but the findings are similar for the other two datasets. More detailed results can be found in the supplementary material.

Number of walks Figure [2](#page-5-1) shows the MRR performance on the validation set of ICEWS14 for different numbers of walks that were extracted during rule learning. We observe a performance increase with a growing number of walks. However, the performance gains saturate between 100 and 200 walks where rather small improvements are attainable.

Transition distribution We test two transition distributions for the extraction of temporal walks: uniform and exponentially weighted according to [\(3\)](#page-3-4). The rationale behind using an exponentially weighted distribution is the observation that related events tend to happen within a short timeframe. The distribution of the first edge is always uniform to not restrict the variety of obtained walks. Overall, the performance of the exponential distribution consistently exceeds the uniform setting with respect to the MRR (see Figure [2\)](#page-5-1).

We observe that the exponential distribution leads to more rules of length 3 than the uniform setting (11,718 compared to 8,550 rules for 200 walks), while it is the opposite for rules of length 1 (7,858 compared to 11,019 rules). The exponential setting leads to more successful longer walks because the timestamp differences between subsequent edges tend to be smaller. It is less likely that there are no feasible transitions anymore because of temporal constraints. The uniform setting, however, leads to a better exploration of the neighborhood around the start node for shorter walks.


| Confidence | Head | Body |
|------------|------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| 0.963 | (E1, demonstrate or rally, E2, T4) | (E1,riot, E2, T1) ∧ (E2, make statement, E1, T2) ∧ (E1,riot, E2, T3) |
| 0.818 | (E1,share information, E2, T2) | (E1, express intent to ease sanctions−1<br>, E2, T1) |
| 0.750 | (E1, provide military aid, E3, T3) | (E1, provide military aid, E2, T1) ∧ (E2, intend to protect−1<br>, E3, T2) |
| 0.570 | (Merkel, consult, Obama, 14/08/09) | (Merkel, discuss by telephone, Obama, 14/07/22) |
| 0.500 | (Merkel, consult, Obama, 14/08/09) | (Merkel, express intent to meet, Obama, 14/05/02)<br>∧ (Obama, consult−1<br>, Merkel, 14/07/18) ∧ (Merkel, consult−1<br>, Obama, 14/07/29) |

<span id="page-6-1"></span>**Table 2:** Three exemplary rules from the dataset ICEWS14 and two walks for the query *(Angela Merkel, consult, ?, 2014/08/09)*that lead to the correct answer*Barack Obama*. The timestamps are displayed in the format yy/mm/dd.

| Gtrain | Gtest | Model | MRR | h@1 | h@3 | h@10 |
|-----------|---------|-------------------|------------------|------------------|------------------|------------------|
| ICEWS0515 | ICEWS14 | AnyBURL<br>TLogic | 0.2664<br>0.4253 | 0.1800<br>0.3291 | 0.3024<br>0.4780 | 0.4477<br>0.6122 |
| ICEWS14 | ICEWS18 | AnyBURL<br>TLogic | 0.1546<br>0.2915 | 0.0907<br>0.1987 | 0.1685<br>0.3330 | 0.2958<br>0.4795 |

**Table 3:** Inductive setting where rules learned on Gtrain are transferred and applied to Gtest.

Rule length We learn rules of lengths 1, 2, and 3. Using all rules for application results in the best performance (MRR on the validation set: 0.4373), followed by rules of only length 1 (0.4116), 3 (0.4097), and 2 (0.1563). The reason why rules of length 3 perform better than length 2 is that the temporal walks are allowed to transition back and forth between the same entities. Since we only learn cyclic rules, a rule body of length 2 must constitute a path with no recurring entities, resulting in fewer rules and rule groundings in the graph. Interestingly, simple rules of length 1 already yield very good performance.

Time window For rule application, we define a time window for retrieving the relevant data. The performance increases with the size of the time window, even though relevant events tend to be close to the query timestamp. The second summand of the score function f in [\(6\)](#page-3-3) takes the time difference between the query timestamp t q and the earliest body timestamp t1(B(R, c)) into account. In this case, earlier events with a large timestamp difference receive a lesser weight, while generally, as much information as possible is beneficial for prediction.

Score function We define the score function f in [\(6\)](#page-3-3) as a convex combination of the rule's confidence and a function that depends on the time difference t <sup>q</sup> − t1(B(R, c)). The performance of only using the confidence (MRR: 0.3869) or only using the exponential function (0.4077) is worse than the combination (0.4373), which means that both the information from the rules' confidences and the time differences are important for prediction.

Variance The variance in the performance due to different rules obtained from the rule learning component is quite small. Running the same model with the best hyperparameter settings for five different seeds results in a standard deviation of 0.0012 for the MRR. The rule application component is deterministic and always leads to the same candidates with corresponding scores for the same hyperparameter setting.

Training and inference time The worst-case time complexity for learning rules of length l is O(|R|nlDb), where n is the number of walks, D the maximum node degree in the training set, and b the number of body samples for estimating the confidence. The worst-case time complexity for inference is given by O(|G| + |T R<sup>r</sup> <sup>q</sup> |DL|E| log(k)), where L is the maximum rule length in T R<sup>r</sup> <sup>q</sup> and k the minimum number of candidates. For large graphs with high node degrees, it is possible to reduce the complexity to O (|G| + |T R<sup>r</sup> <sup>q</sup> |KLD|E| log(k)) by only keeping a maximum of K candidate walks during rule application.

Both training and application can be parallelized since the rule learning for each relation and the rule application for each test query are independent. Rule learning with 200 walks and exponentially weighted transition distribution for rule lengths {1, 2, 3} on a machine with 8 CPUs takes 180 sec for ICEWS14, while the application on the validation set takes 2000 sec, with w = ∞ and k = 20. For comparison, the best-performing baseline xERTE needs for training one epoch on the same machine already 5000 sec, where an MRR of 0.3953 can be obtained, while testing on the validation set takes 700 sec.

## Conclusion

We have proposed TLogic, the first symbolic framework that directly learns temporal logical rules from temporal knowledge graphs and applies these rules for link forecasting. The framework generates answers by applying rules to observed events prior to the query timestamp and scores the answer candidates depending on the rules' confidences and time differences. Experiments on three datasets indicate that TLogic achieves better overall performance compared to state-ofthe-art baselines. In addition, our approach also provides time-consistent, explicit, and human-readable explanations for the predictions in the form of temporal logical rules.

As future work, it would be interesting to integrate acyclic rules, which could also contain relevant information and might boost the performance for rules of length 2. Furthermore, the simple sampling mechanism for temporal walks could be replaced by a more sophisticated approach, which is able to effectively identify the most promising walks.

## Acknowledgement

This work has been supported by the German Federal Ministry for Economic Affairs and Climate Action (BMWK) as part of the project RAKI under grant number 01MD19012C and by the German Federal Ministry of Education and Research (BMBF) under grant number 01IS18036A. The authors of this work take full responsibility for its content.

## References

<span id="page-7-20"></span>Bian, R.; Koh, Y. S.; Dobbie, G.; and Divoli, A. 2019. Network embedding and change modeling in dynamic heterogeneous networks. In *Proceedings of the Forty-Second International ACM SIGIR Conference on Research and Development in Information Retrieval*.

<span id="page-7-7"></span>Bordes, A.; Usunier, N.; Garc´ıa-Duran, A.; Weston, J.; and ´ Yakhnenko, O. 2013. Translating embeddings for modeling multi-relational data. In *Proceedings of the Twenty-Sixth International Conference on Neural Information Processing Systems*.

<span id="page-7-16"></span>Galarraga, L.; Teflioudi, C.; Hose, K.; and Suchanek, F. M. ´ 2015. Fast rule mining in ontological knowledge bases with AMIE+. *The VLDB Journal*, 24: 707–730.

<span id="page-7-12"></span>Garc´ıa-Duran, A.; Duman ´ ci˘ c, S.; and Niepert, M. 2018. ´ Learning sequence encoders for temporal knowledge graph completion. In *Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing*.

<span id="page-7-13"></span>Goel, R.; Kazemi, S. M.; Brubaker, M.; and Poupart, P. 2020. Diachronic embedding for temporal knowledge graph completion. In *Proceedings of the Thirty-Fourth AAAI Conference on Artificial Intelligence*.

<span id="page-7-15"></span>Han, Z.; Chen, P.; Ma, Y.; and Tresp, V. 2021. Explainable subgraph reasoning for forecasting on temporal knowledge graphs. In *Proceedings of the Ninth International Conference on Learning Representations*.

<span id="page-7-0"></span>Hildebrandt, M.; Sunder, S. S.; Mogoreanu, S.; Joblin, M.; Mehta, A.; Thon, I.; and Tresp, V. 2019. A recommender system for complex real-world applications with nonlinear dependencies and knowledge graph context. In *Proceedings of the Sixteenth Extended Semantic Web Conference*.

<span id="page-7-5"></span>Jin, W.; Zhang, C.; Szekely, P.; and Ren, X. 2019. Recurrent event network for reasoning over temporal knowledge graphs. Workshop paper at the Seventh International Conference on Learning Representations.

<span id="page-7-4"></span>Lacroix, T.; Obozinski, G.; and Usunier, N. 2020. Tensor decompositions for temporal knowledge base completion. In *Proceedings of the Eighth International Conference on Learning Representations*.

<span id="page-7-3"></span>Leblay, J.; and Chekol, M. W. 2018. Deriving validity time in knowledge graph. In *Companion Proceedings of the Web Conference 2018*.

<span id="page-7-2"></span>Liu, Y.; Hildebrandt, M.; Joblin, M.; Ringsquandl, M.; Raissouni, R.; and Tresp, V. 2021. Neural multi-hop reasoning with logical rules on biomedical knowledge graphs. In *Proceedings of the Eighteenth Extended Semantic Web Conference*.

<span id="page-7-19"></span>Mahdavi, S.; Khoshraftar, S.; and An, A. 2018. dynnode2vec: scalable dynamic network embedding. In *Proceedings of the 2018 IEEE International Conference on Big Data*.

<span id="page-7-22"></span>Meilicke, C.; Chekol, M. W.; Fink, M.; and Stuckenschmidt, H. 2020. Reinforced anytime bottom-up rule learning for knowledge graph completion. arXiv:2004.04412.

<span id="page-7-17"></span>Meilicke, C.; Chekol, M. W.; Ruffinelli, D.; and Stuckenschmidt, H. 2019. Anytime bottom-up rule learning for knowledge graph completion. In *Proceedings of the Twenty-Eighth International Joint Conference on Artificial Intelligence*.

<span id="page-7-1"></span>Nguyen, D. Q.; Nguyen, T. D.; Nguyen, D. Q.; and Phung, D. 2018a. A novel embedding model for knowledge base completion based on convolutional neural network. In *Proceedings of the Sixteenth Annual Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies*.

<span id="page-7-21"></span>Nguyen, G. H.; Lee, J. B.; Rossi, R. A.; Ahmed, N. K.; Koh, E.; and Kim, S. 2018b. Dynamic network embeddings: from random walks to temporal random Walks. In *Proceedings of the 2018 IEEE International Conference on Big Data*.

<span id="page-7-6"></span>Nickel, M.; Tresp, V.; and Kriegel, H.-P. 2011. A three-way model for collective learning on multi-relational data. In *Proceedings of the Twenty-Eighth International Conference on Machine Learning*.

<span id="page-7-18"></span>Omran, P. G.; Wang, K.; and Wang, Z. 2019. Learning temporal rules from knowledge graph streams. In *Proceedings of the AAAI 2019 Spring Symposium on Combining Machine Learning with Knowledge Engineering*.

<span id="page-7-10"></span>Schlichtkrull, M.; Kipf, T. N.; Bloem, P.; Berg, R. v. d.; Titov, I.; and Welling, M. 2018. Modeling relational data with graph convolutional networks. In *Proceedings of the Fifteenth Extended Semantic Web Conference*.

<span id="page-7-9"></span>Trouillon, T.; Welbl, J.; Riedel, S.; Gaussier, E.; and ´ Bouchard, G. 2016. Complex embeddings for simple link prediction. In *Proceedings of the Thirty-Third International Conference on Machine Learning*.

<span id="page-7-11"></span>Vashishth, S.; Sanyal, S.; Nitin, V.; and Talukdar, P. 2020. Composition-based multi-relational graph convolutional networks. In *Proceedings of the Eighth International Conference on Learning Representations*.

<span id="page-7-8"></span>Yang, B.; Yih, W.-T.; He, X.; Gao, J.; and Deng, L. 2015. Embedding entities and relations for learning and inference in knowledge bases. In *Proceedings of the Third International Conference on Learning Representations*.

<span id="page-7-14"></span>Zhu, C.; Chen, M.; Fan, C.; Cheng, G.; and Zhang, Y. 2021. Learning from history: modeling temporal knowledge graphs with sequential copy-generation networks. In *Proceedings of the Thirty-Fifth AAAI Conference on Artificial Intelligence*.

## Supplementary Material

Dataset statistics Table [4](#page-8-0) shows the statistics of the three datasets ICEWS14, ICEWS18, and ICEWS0515. |X | denotes the cardinality of a set X .


| Dataset | Gtrain | Gvalid | Gtest | E | R | T |
|---------|---------|--------|--------|--------|-----|-------|
| 14 | 63,685 | 13,823 | 13,222 | 7,128 | 230 | 365 |
| 18 | 373,018 | 45,995 | 49,545 | 23,033 | 256 | 304 |
| 0515 | 322,958 | 69,224 | 69,147 | 10,488 | 251 | 4,017 |

**Table 4:** Dataset statistics with daily time resolution for all three ICEWS datasets.

Experimental details All experiments were conducted on a Linux machine with 16 CPU cores and 32 GB RAM. The set of tested hyperparameter ranges and best parameter values for TLogic are displayed in Table [5.](#page-8-1) Due to memory constraints, the time window w for ICEWS18 is set to 200 and for ICEWS0515 to 1000. The best hyperparameter values are chosen based on the MRR on the validation set. Due to the small variance of our approach, the shown results are based on one algorithm run. A random seed of 12 is fixed for the rule learning component to obtain reproducible results.


| Hyperparameter | Range | Best |
|---------------------------|----------------------------|-----------|
| Number of walks n | {10, 25, 50, 100, 200} | 200 |
| Transition distribution d | {unif, exp} | exp |
| Rule lengths L | {{1}, {2}, {3}, {1, 2, 3}} | {1, 2, 3} |
| Time window w | {30, 90, 150, 210, 270, ∞} | ∞ |
| Minimum candidates k | {10, 20} | 20 |
| α (score function f) | {0, 0.25, 0.5, 0.75, 1} | 0.5 |
| λ (score function f) | {0.01, 0.1, 0.5, 1} | 0.1 |

**Table 5:** Hyperparameter ranges and best parameter values.

All results in the appendix refer to the validation set of ICEWS14. However, the observations are similar for the test set and the other two datasets. All experiments use the best set of hyperparameters, where only the analyzed parameters are modified.

Object distribution baseline We apply a simple object distribution baseline when there are no rules for the query relation or no matching body groundings in the graph. This baseline is only added for completeness and does not improve the results in a significant way.

The proportion of cases where there are no rules for the test query relation is 15/26,444 = 0.00056 for ICEWS14, 21/99,090 = 0.00021 for ICEWS18, and 9/138,294 = 0.00007 for ICEWS0515. The proportion of cases where there are no matching body groundings is 880/26,444 = 0.0333 for ICEWS14, 2,535/99,090 = 0.0256 for ICEWS18, and 2,375/138,294 = 0.0172 for ICEWS0515.

Number of walks and transition distribution Table [6](#page-9-0) shows the results for different choices of numbers of walks and transition distributions. The performance for all metrics increases with the number of walks. Exponentially weighted transition always outperforms uniform sampling.


| Walks | Transition | MRR | h@1 | h@3 | h@10 |
|-------|------------|--------|--------|--------|--------|
| 10 | Unif | 0.3818 | 0.2983 | 0.4307 | 0.5404 |
| 10 | Exp | 0.3906 | 0.3054 | 0.4408 | 0.5530 |
| 25 | Unif | 0.4098 | 0.3196 | 0.4614 | 0.5803 |
| 25 | Exp | 0.4175 | 0.3270 | 0.4710 | 0.5875 |
| 50 | Unif | 0.4219 | 0.3307 | 0.4754 | 0.5947 |
| 50 | Exp | 0.4294 | 0.3375 | 0.4837 | 0.6024 |
| 100 | Unif | 0.4266 | 0.3315 | 0.4817 | 0.6057 |
| 100 | Exp | 0.4324 | 0.3397 | 0.4861 | 0.6092 |
| 200 | Unif | 0.4312 | 0.3366 | 0.4851 | 0.6114 |
| 200 | Exp | 0.4373 | 0.3434 | 0.4916 | 0.6161 |

**Table 6:** Results for different choices of numbers of walks and transition distributions.

Rule length Table [7](#page-9-1) indicates that using rules of all lengths for application results in the best performance. Learning only cyclic rules probably makes it more difficult to find rules of length 2, where the rule body must constitute a path with no recurring entities, leading to fewer rules and body groundings in the graph.


| Rule length | MRR | h@1 | h@3 | h@10 |
|-------------|--------|--------|--------|--------|
| 1 | 0.4116 | 0.3168 | 0.4708 | 0.5909 |
| 2 | 0.1563 | 0.0648 | 0.1776 | 0.3597 |
| 3 | 0.4097 | 0.3213 | 0.4594 | 0.5778 |
| 1,2,3 | 0.4373 | 0.3434 | 0.4916 | 0.6161 |

**Table 7:** Results for different choices of rule lengths.

Time window Generally, the larger the time window, the better the performance (see Table [8\)](#page-9-2). If taking all previous timestamps leads to a too high memory usage, the time window should be decreased.


| Time window | MRR | h@1 | h@3 | h@10 |
|-------------|--------|--------|--------|--------|
| 30 | 0.3842 | 0.3080 | 0.4294 | 0.5281 |
| 90 | 0.4137 | 0.3287 | 0.4627 | 0.5750 |
| 150 | 0.4254 | 0.3368 | 0.4766 | 0.5950 |
| 210 | 0.4311 | 0.3403 | 0.4835 | 0.6035 |
| 270 | 0.4356 | 0.3426 | 0.4892 | 0.6131 |
| ∞ | 0.4373 | 0.3434 | 0.4916 | 0.6161 |

**Table 8:** Results for different choices of time windows.

Score function Using the best hyperparameters values for α and λ, Table [9](#page-9-3) shows in the first row the results if only the rules' confidences are used for scoring, in the second row if only the exponential component is used, and in the last row the results for the combined score function. The combination yields the best overall performance. The optimal balance between the two terms, however, depends on the application and metric prioritization.


| α | λ | MRR | h@1 | h@3 | h@10 |
|-----|-----------|--------|--------|--------|--------|
| 1 | arbitrary | 0.3869 | 0.2806 | 0.4444 | 0.5918 |
| 0 | 0.1 | 0.4077 | 0.3515 | 0.4820 | 0.6051 |
| 0.5 | 0.1 | 0.4373 | 0.3434 | 0.4916 | 0.6161 |

**Table 9:** Results for different parameter values in the score function f.

Rule learning The figures [3](#page-9-4) and [4](#page-9-5) show the number of rules learned under the two transition distributions. The total number of learned rules is similar for the uniform and exponential distribution, but there is a large difference for rules of lengths 1 and 3. The exponential distribution leads to more successful longer walks and thus more longer rules, while the uniform distribution leads to a better exploration of the neighborhood around the start node for shorter walks.

<span id="page-9-4"></span>![](_page_9_Figure_13.jpeg)
<!-- Image Description: The image displays a line graph comparing the number of rules generated under two different distributions ("unif" and "exp") and considering both total rules and rules of length one. The x-axis represents the number of walks, while the y-axis shows the number of rules. The graph illustrates how the number of generated rules increases with the number of walks, differing based on the distribution and rule length. It likely demonstrates the scalability or efficiency of a rule generation algorithm within the paper. -->

**Figure 3:** Total number of learned rules and number of rules for length 1.

<span id="page-9-5"></span>![](_page_9_Figure_15.jpeg)
<!-- Image Description: The image displays a line graph showing the relationship between the number of walks and the number of rules generated, categorized by two rule length (2 and 3) and two distributions (uniform and exponential). The x-axis represents the number of walks, and the y-axis shows the number of rules. Four lines represent different combinations of rule length and distribution, illustrating how these factors affect rule generation scaling. The graph likely demonstrates the computational complexity or efficiency of a rule generation algorithm within the paper. -->

**Figure 4:** Number of rules for lengths 2 and 3.

Training and inference time The rule learning and rule application times are shown in the figures [5](#page-10-0) and [6,](#page-10-1) dependent on the number of extracted temporal walks during learning.

<span id="page-10-0"></span>![](_page_10_Figure_1.jpeg)
<!-- Image Description: The image displays a line graph comparing the computation time (in seconds) of two methods, "unif" and "exp," as a function of the number of walks. The x-axis represents the number of walks, and the y-axis shows the execution time. The graph shows that execution time increases linearly with the number of walks for both methods, but "exp" consistently takes longer than "unif." The purpose is to demonstrate a performance comparison between the two algorithms. -->

**Figure 5:** Rule learning time.

<span id="page-10-1"></span>![](_page_10_Figure_3.jpeg)
<!-- Image Description: The image displays a line graph comparing computation time (in seconds) against the number of walks for two methods: "unif" and "exp". The x-axis represents the number of walks, while the y-axis shows the time taken. The graph illustrates that computation time increases with the number of walks, with "exp" consistently exhibiting higher execution times than "unif". The graph likely serves to demonstrate the relative efficiency of the two methods within the paper's algorithm. -->

**Figure 6:** Rule application time.

The worst-case time complexity for learning rules of length l is O(|R|nlDb), where n is the number of walks, D the maximum node degree in the training set, and b the number of body samples for estimating the confidence. The worst-case time complexity for inference is given by O(|G| + |T R<sup>r</sup> <sup>q</sup> |DL|E| log(k)), where L is the maximum rule length in T R<sup>r</sup> <sup>q</sup> and k the minimum number of candidates. More detailed steps of the algorithms for understanding these complexity estimations are given by Algorithm [3](#page-11-0) and Algorithm [4.](#page-12-0)

![](_page_11_Figure_0.jpeg)
<!-- Image Description: This flowchart illustrates a temporal knowledge graph reasoning system. A temporal knowledge graph (showing nodes and edges with timestamps) undergoes temporal random walks, feeding into rule learning. Learned rules are applied to input (subject, predicate, ?, timestamp), generating ranked candidate answers (e.g., France, Germany with associated scores) based on temporal logical rules with confidence scores. The diagram depicts the workflow and data flow of the system. -->

**Figure 7:** Overall framework.


| | Algorithm 3: Rule learning (detailed) |
|-----|-----------------------------------------------------------------------------------------------------------------------|
| | Input: Temporal knowledge graph G. |
| | Parameters: Rule lengths L ⊂ N, number of temporal random walks<br>n ∈ N, transition distribution<br>d ∈ {unif, exp}. |
| | Output: Temporal logical rules T R. |
| | 1: for relation r ∈ R do |
| 2: | for l ∈ L do |
| 3: | for i ∈ [n] do |
| 4: | T Rl<br>r ← ∅ |
| 5: | According to transition distribution d, sample a temporal random walk W of length l + 1 with tl+1<br>> tl |
| | . See (4). |
| | Sample uniformly a start edge (es, r, eo, t) with edge type r. |
| 6: | for step m ∈ {2, , l + 1} do |
| 7: | Retrieve adjacent edges of current object node. |
| 8: | if m = 2 then |
| 9: | Filter out all edges with timestamps greater than or equal to the current timestamp. |
| 10: | else |
| 11: | Filter out all edges with timestamps greater than the current timestamp. |
| | Filter out the inverse edge of the previously sampled edge. |
| 12: | if m = l + 1 then |
| 13: | Retrieve all filtered edges that connect the current object to the source of the walk. |
| 14: | Sample the next edge from the filtered edges according to distribution d. |
| | break if there are no feasible edges because of temporal or cyclic constraints. |
| 15: | Transform walk W to the corresponding temporal logical rule R.<br>. See (5). |
| | Save information about the head relation and body relations.<br>Define variable constraints for recurring entities. |
| 16: | Estimate the confidence of rule R. |
| | Sample b body groundings. For each step m ∈ {1, , l}, filter the edges for the correct body relation besides for |
| | the timestamps required to fulfill the temporal constraints. |
| | For successful body groundings, check the variable constraints. |
| | For each unique body, check if the rule head exists in the graph. |
| | Calculate rule support / body support. |
| 17: | T Rl<br>r ← T Rl<br>r ∪ {(R, conf(R))} |
| 18: | ← ∪l∈LT Rl<br>T Rr |
| | r<br>19: T R ← ∪r∈RT Rr |
| | 20: return T R |
| | |

<span id="page-12-0"></span>Algorithm 4: Rule application (detailed)

Input: Test query q = (e q , r<sup>q</sup> , ?, t<sup>q</sup> ), temporal logical rules T R, temporal knowledge graph G. Parameters: Time window w ∈ N ∪ {∞}, minimum number of candidates k, score function f. Output: Answer candidates C. 1: C ← ∅ . Apply the rules in T R by decreasing confidence. 2: Retrieve subgraph SG ⊂ G with timestamps t ∈ [t <sup>q</sup> − w, t<sup>q</sup> ). . Only done if the timestamp changes. The queries in the test set are sorted by timestamp. Retrieve edges with timestamps t ∈ [t <sup>q</sup> − w, t<sup>q</sup> ). Store edges for each relation in a dictionary. 3: if T R<sup>r</sup> <sup>q</sup> 6= ∅ then 4: for rule R ∈ T R<sup>r</sup> <sup>q</sup> do 5: Find all body groundings of R in SG. Retrieve edges that could constitute walks that match the rule's body. First, retrieve edges whose subject matches e and the relation the first relation in the rule body. Then, retrieve edges whose subject match one of the current targets and the relation the next relation in the rule body. Generate complete walks by merging the edges on the same target-source entity. Delete all walks that do not comply with the time constraints. Check variable constraints, and delete the walks that do not comply with the variable constraints. 6: Retrieve candidates C(R) from the target entities of the walks. 7: for c ∈ C(R) do 8: Calculate score f(R, c). . See [\(6\)](#page-3-3). 9: C ← C ∪ {(c, f(R, c))} 10: if |{c | ∃R : (c, f(R, c)) ∈ C}| ≥ k then 11: break 12: return C

q
