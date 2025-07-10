---
cite_key: "liyitong_2024"
title: "A Unified Temporal Knowledge Graph Reasoning Model Towards Interpolation and Extrapolation"
authors: "nudt.edu.cn liyitong"
year: 2024
doi: "10.48550/arXiv.2405.18106"
url: "https://arxiv.org/abs/2405.18106"
relevancy: "High"
tldr: "Novel unified approach to temporal knowledge graph reasoning that handles both interpolation (historical analysis) and extrapolation (future prediction) through neural-driven symbolic reasoning with enhanced robustness and interpretability."
insights: "Proposes Temporal PAth-based Reasoning (TPAR) model that performs neural-driven symbolic reasoning robust to ambiguous and noisy temporal data while providing fine interpretability, outperforming SOTA methods in link prediction for both interpolation and extrapolation settings."
summary: "This paper addresses limitations in existing temporal knowledge graph (TKG) reasoning methods that are designed specifically for either interpolation or extrapolation reasoning but not both. The proposed Temporal PAth-based Reasoning (TPAR) model provides a unified approach that performs neural-driven symbolic reasoning, designed to be robust to ambiguous and noisy temporal data while maintaining fine interpretability. The approach addresses temporal correlations and chronological knowledge that existing methods have de-emphasized or ignored."
research_question: "How can we develop a unified reasoning model that effectively handles both interpolation and extrapolation in temporal knowledge graphs while maintaining robustness to noisy data and providing interpretable results?"
methodology: "Developed Temporal PAth-based Reasoning (TPAR) model using neural-driven symbolic reasoning approach, designed for robustness to ambiguous and noisy temporal data, implemented pipeline experimental setting for unified evaluation, comprehensive experiments on link prediction tasks."
key_findings: "TPAR outperformed state-of-the-art methods in link prediction tasks for both interpolation and extrapolation settings, demonstrated effective integration of temporal reasoning capabilities, showed robustness to noisy temporal data with enhanced interpretability."
limitations: "Previous methods de-emphasized temporal correlations, existing approaches ignored inferring clues from missing past facts, limited handling of temporal data complexity in unified frameworks."
conclusion: "The TPAR model provides a unified approach to temporal knowledge graph reasoning that successfully addresses previous methodological constraints while maintaining robustness and interpretability for practical applications."
future_work: "Further refinement of TPAR model capabilities, exploration of more diverse temporal reasoning scenarios, integration with real-world temporal knowledge systems."
implementation_insights: "Provides architectural framework for implementing temporal reasoning capabilities in HDM systems with focus on unified interpolation/extrapolation and robust handling of noisy temporal data."
tags:
  - "Temporal Knowledge Graphs"
  - "Unified Reasoning"
  - "Interpolation Extrapolation"
  - "Neural-Symbolic Reasoning"
  - "Temporal Modeling"
---

# A Unified Temporal Knowledge Graph Reasoning Model Towards Interpolation and Extrapolation

Kai Chen<sup>1</sup><sup>∗</sup> , Ye Wang<sup>1</sup><sup>∗</sup> , Yitong Li<sup>2</sup>† , Aiping Li<sup>1</sup>† , Han Yu<sup>1</sup> , Xin Song<sup>1</sup>

<sup>1</sup>National University of Defense Technology, Changsha, China

<sup>2</sup>Huawei Technologies Co., Ltd.

{chenkai\_,ye.wang,liaiping,yuhan17,songxin}@nudt.edu.cn liyitong3@huawei.com

### Abstract

Temporal knowledge graph (TKG) reasoning has two settings: interpolation reasoning and extrapolation reasoning. Both of them draw plenty of research interest and have great significance. Methods of the former deemphasize the temporal correlations among facts sequences, while methods of the latter require strict chronological order of knowledge and ignore inferring clues provided by missing facts of the past. These limit the practicability of TKG applications as almost all of the existing TKG reasoning methods are designed specifically to address either one setting. To this end, this paper proposes an original Temporal PAth-based Reasoning (TPAR) model for both the interpolation and extrapolation reasoning. TPAR performs a neural-driven symbolic reasoning fashion that is robust to ambiguous and noisy temporal data and with fine interpretability as well. Comprehensive experiments show that TPAR outperforms SOTA methods on the link prediction task for both the interpolation and the extrapolation settings. A novel pipeline experimental setting is designed to evaluate the performances of SOTA combinations and the proposed TPAR towards interpolation and extrapolation reasoning. More diverse experiments are conducted to show the robustness and interpretability of TPAR.

### 1 Introduction

Knowledge graph (KG) is a semantic network that represents real-world facts in a structured way using entities and relations [\(Bollacker et al.,](#page-8-0) [2008;](#page-8-0) [Song et al.,](#page-10-0) [2021;](#page-10-0) [Zhao et al.,](#page-11-0) [2021\)](#page-11-0). Typically, a fact is represented by a triple (s, r, o) in KG, consisting of a subject entity s, an object entity o, and a relation r between s and o.

In the real world, many facts are closely associated with a particular time interval. For example, the fact *"Barack Obama is the president of USA"*

is valid for the time period of *2009 January 20th - 2017 January 20th* and the fact *"Donald Trump is the president of USA"* is only valid for the following four years. To represent such time-sensitive facts, Temporal Knowledge Graphs (TKGs) have recently gained significant attention from both academic and industrial communities. Specifically, TKGs extend static KGs by incorporating the temporal information t into fact triples, represented as a quadruple (s, r, o, t), which allows for modelling the temporal dependencies and evolution of knowledge over time, being crucial for reasoning time-evolving facts in applications such as financial forecasting, social networks, and healthcare.

TKG reasoning infers new knowledge with timesensitive facts in existing TKGs, which generally has two settings: the interpolation reasoning [\(Xu](#page-11-1) [et al.,](#page-11-1) [2020;](#page-11-1) [Lacroix et al.,](#page-9-0) [2020;](#page-9-0) [Xu et al.,](#page-10-1) [2021;](#page-10-1) [Chen et al.,](#page-8-1) [2022\)](#page-8-1) and the extrapolation reasoning [\(Jin et al.,](#page-9-1) [2020;](#page-9-1) [Sun et al.,](#page-10-2) [2021;](#page-10-2) [Liu et al.,](#page-10-3) [2022\)](#page-10-3). Given a temporal knowledge graph with facts from time t<sup>0</sup> to time t<sup>T</sup> , the interpolation reasoning infers missing facts at any time in history (t<sup>0</sup> ≤ t ≤ t<sup>T</sup> ) and the extrapolation reasoning attempt to predict unknown facts that may occur in the future (t > t<sup>T</sup> ).

Many approaches have been proposed to tackle the TKG reasoning problem, however, these two reasoning tasks are tackled in totally different and incompatible manners. On the one hand, interpolation methods de-emphasize the temporal correlations among fact sequences while training, thus it's difficult to cope with the challenges of invisible timestamps and invisible entities in extrapolation due to their poor inductive reasoning ability [\(Sun et al.,](#page-10-2) [2021\)](#page-10-2). On the other hand, most stateof-the-art (SOTA) extrapolation solutions require a strict chronological order of data during training. As a result, they can only predict unknown future facts, but they could hardly infer missing historical facts which are crucial for completing the

<sup>∗</sup> Equal contributions.

<sup>†</sup> Corresponding authors.

overall knowledge landscape and providing more clues for predicting accurate future events. These limit the practicability of TKG applications as almost all of the existing TKG reasoning methods are designed specifically to address either one setting. Experiments with a novel pipeline setting intuitively reveal that even with the SOTA methods from both settings, the composed methods show a frustrating decrease in reasoning performance. More in-depth analysis can be found in Section [5.3](#page-6-0) and Appendix [F.](#page-14-0) Therefore, the motivation of this work is to propose a unified method that can accommodate two types of reasoning settings, enabling temporal knowledge graph reasoning to be conducted simultaneously for both the interpolation and the extrapolation.

To this end, we take inspiration from recent neural [\(Xu et al.,](#page-10-1) [2021;](#page-10-1) [Li et al.,](#page-9-2) [2021\)](#page-9-2) and symbolic [\(Sun et al.,](#page-10-2) [2021;](#page-10-2) [Liu et al.,](#page-10-3) [2022\)](#page-10-3) TKG reasoning approaches. Neural network approaches can perform effective reasoning but lack interpretation as they cannot provide explicit rules to explain the reasoning results, while symbolic reasoning approaches use logical symbols and rules to perform reasoning tasks but are not suitable for handling ambiguous and noisy data due to their strict matching and discrete logic operations used during rule searching [\(Zhang et al.,](#page-11-2) [2021\)](#page-11-2). In this paper, we propose a Temporal PAth based Reasoning (TPAR) model with a neural-symbolic fashion applicable to both the interpolation and the extrapolation TKG Reasoning. Specifically, we utilize the Bellman-Ford Shortest Path Algorithm [\(Ford,](#page-8-2) [1956;](#page-8-2) [Bell](#page-8-3)[man,](#page-8-3) [1958;](#page-8-3) [Baras and Theodorakopoulos,](#page-8-4) [2010\)](#page-8-4) and introduce a recursive encoding method to score the destination entities of various temporal paths, and then our TPAR performs symbolic reasoning with the help of the obtained scores. It is noticeable that the neural-driven symbolic reasoning fashion we adopted is more robust to the uncertainty data compared to traditional pure symbolic reasoning methods, and comprehensible temporal paths with fine interpretability as well. We summarize our main contributions as follows:

- 1. We propose an original unified Temporal PAthbased Reasoning (TPAR) model for both the interpolation and extrapolation reasoning settings. To the best of our knowledge, this is the first work to achieve the best of both worlds.
- 2. We develop a novel neural-driven symbolic reasoning fashion on various temporal paths to

enhance both the robustness and interpretability of temporal knowledge reasoning.

3. Comprehensive experiments show that TPAR outperforms SOTA methods on the link prediction task for both the interpolation and the extrapolation settings with decent interpretability and robustness. An intriguing pipeline experiment is meticulously designed to demonstrate the strengths of TPAR in addressing the unified prediction through both settings.

### 2 Related Work

### 2.1 Static KG Reasoning

Static KG reasoning methods can be summarized into three classes: the translation models [\(Bordes](#page-8-5) [et al.,](#page-8-5) [2013;](#page-8-5) [Wang et al.,](#page-10-4) [2014;](#page-10-4) [Lin et al.,](#page-10-5) [2015\)](#page-10-5), the semantic matching models [\(Yang et al.,](#page-11-3) [2015;](#page-11-3) [Trouillon et al.,](#page-10-6) [2016\)](#page-10-6), and the embedding-based models [\(Dettmers et al.,](#page-8-6) [2018;](#page-8-6) [Shang et al.,](#page-10-7) [2019\)](#page-10-7). Recently, R-GCN [\(Schlichtkrull et al.,](#page-10-8) [2018\)](#page-10-8) and CompGCN [\(Vashishth et al.,](#page-10-9) [2020\)](#page-10-9) extended GCN to relation-aware GCN for KGs.

### 2.2 TKG Reasoning

Interpolation TKG Reasoning Many interpolation TKG reasoning methods [\(Leblay and Chekol,](#page-9-3) [2018;](#page-9-3) [Dasgupta et al.,](#page-8-7) [2018;](#page-8-7) [García-Durán et al.,](#page-8-8) [2018;](#page-8-8) [Xu et al.,](#page-10-10) [2019;](#page-10-10) [Lacroix et al.,](#page-9-0) [2020;](#page-9-0) [Jain](#page-9-4) [et al.,](#page-9-4) [2020;](#page-9-4) [Xu et al.,](#page-10-1) [2021\)](#page-10-1) are extended from static KGs to TKGs. Besides, TeRo [\(Xu et al.,](#page-11-1) [2020\)](#page-11-1) represents each relation as dual complex embeddings and can handle the time intervals between relations. RotateQVS [\(Chen et al.,](#page-8-1) [2022\)](#page-8-1) represents temporal evolutions as rotations in quaternion vector space and can model various complex relational patterns. T-GAP [\(Jung et al.,](#page-9-5) [2021\)](#page-9-5) performs pathbased inference by propagating attention through the graph.

Extrapolation TKG Reasoning To predict future facts, many extrapolation TKG reasoning methods [\(Jin et al.,](#page-9-1) [2020;](#page-9-1) [Li et al.,](#page-9-2) [2021;](#page-9-2) [Han et al.,](#page-9-6) [2021b;](#page-9-6) [Zhu et al.,](#page-11-4) [2021a;](#page-11-4) [Sun et al.,](#page-10-2) [2021;](#page-10-2) [Li et al.,](#page-9-7) [2022b,](#page-9-7)[a\)](#page-9-8) have been studied. For better interpretability, TLogic [\(Liu et al.,](#page-10-3) [2022\)](#page-10-3) adopts temporary logical rules extracted via temporary random walks, while xERTE [\(Han et al.,](#page-9-9) [2021a\)](#page-9-9) utilizes an explainable subgraph and attention mechanism for predictions. Besides, RPC [\(Liang et al.,](#page-9-10) [2023\)](#page-9-10) employs relational graph convolutional networks and

gated recurrent units to mine relational correlations and periodic patterns from temporal facts.

### 2.3 Neural-Symbolic Reasoning

Neural-symbolic reasoning aims to combine the strengths of both approaches, namely the ability of symbolic reasoning to perform logical inference and the ability of neural networks to perform learning from data [\(Zhang et al.,](#page-11-2) [2021\)](#page-11-2). Generally, it can be divided into three categories: (1) Symbolicdriven neural fashion [\(Guo et al.,](#page-8-9) [2016,](#page-8-9) [2018;](#page-8-10) [Wang](#page-10-11) [et al.,](#page-10-11) [2019\)](#page-10-11), which targets neural reasoning but leverages the logic rules to improve the embeddings. (2) Symbolic-driven probabilistic fashion [\(Richardson and Domingos,](#page-10-12) [2006;](#page-10-12) [Qu and Tang,](#page-10-13) [2019;](#page-10-13) [Raedt et al.,](#page-10-14) [2007\)](#page-10-14), which replaces the neural reasoning with a probabilistic framework, i.e., builds a probabilistic model to infer the answers. (3) Neural-driven symbolic fashion [\(Lao and Co](#page-9-11)[hen,](#page-9-11) [2010;](#page-9-11) [Lao et al.,](#page-9-12) [2012;](#page-9-12) [Neelakantan et al.,](#page-10-15) [2015\)](#page-10-15), which aims to infer rules by symbolic reasoning, and incorporates neural networks to deal with the uncertainty and ambiguity of data. For this work, we adopt the neural-driven symbolic fashion for our TKG reasoning.

### 3 Preliminaries

### 3.1 Problem Definition of TKG Reasoning

A Temporal knowledge graph is a collection of millions of temporal facts, expressed as G ⊂ E × R × E × T . Here we use E to denote the set of entities, R to denote the set of relations, and T to denote the set of time stamps. Each temporal fact in G is formed as a quadruple (es, r, eo, t), where a relation r ∈ R holds between a subject entity e<sup>s</sup> ∈ E and an object entity e<sup>o</sup> ∈ E at the time t. And for each quadruple (es, r, eo, t)), an inverse quadruple (eo, r−<sup>1</sup> , es, t)) is also added to the dataset.

Let O = {(es, r, eo, t)|t ∈ [t0, T]} represent the set of known facts that we can observe, and let [t0, T] denote the time interval we can access. For a query q = (eq, rq, ?, tq), TKG Reasoning aims to infer the missing object entity given the other three elements. As we have two distinctive TKG Reasoning settings: the interpolation (inferring a query where t<sup>0</sup> ≤ t<sup>q</sup> ≤ T) and the extrapolation (predicting facts for t<sup>q</sup> > T), we use a unified concept of "temporal background" to represent all known temporal facts of existing TKG.

### <span id="page-2-2"></span>3.2 Bellman-Fold Based Recursive Encoding

The Bellman-Ford Algorithm [\(Ford,](#page-8-2) [1956;](#page-8-2) [Bell](#page-8-3)[man,](#page-8-3) [1958;](#page-8-3) [Baras and Theodorakopoulos,](#page-8-4) [2010\)](#page-8-4) provides a recursive approach to search for the shortest path in a graph.[1](#page-2-0) Since TKGs are far from complete, we do not directly copy it for TKG Reasoning, but utilize a recursive encoding method for representations.

<span id="page-2-1"></span>![](_page_2_Figure_9.jpeg)
<!-- Image Description: The image is a graph illustrating a network structure. Node `u` connects to nodes `x₁, x₂, x₃, x₄` which are at distance `l-1` and `l` respectively. Nodes `x₁, x₂, x₃` have a directed edge pointing to node `v`, implying a relationship or flow. Dashed concentric ovals represent layers or distance from `u`. The illustration likely depicts a multi-layer network model or a specific graph structure used in the paper's algorithm or analysis. -->

**Figure 1:** An illustration of Bellman-Ford-based recursive encoding.

As illustrated in Fig[.1,](#page-2-1) the basic idea of our Bellman-Ford-based recursive encoding is: once the representations of the ℓ − 1 iterations (the node x) starting from node u are ready, we can obtain the representations of the ℓ iterations (the node v) by combining them with the edge (x, v):

$$
h^{0}(u, v) \leftarrow \mathbb{1}(u = v)
$$
$$
h^{\ell}(u, v) \leftarrow \left(\bigoplus_{(x, v) \in \mathcal{E}(v)} h^{\ell-1}(u, x) \otimes w(x, v)\right) \oplus h^{(0)}(u, v),
$$

where 1(u = v) is the indicator function that outputs 1 if u = v and 0 otherwise, ⊗ is the multiplication operator, ⊕ is the summation operator, E(v) is the set of all edges connected to the node v, and w(x, v) is the weight of the edge (x, v).

### 4 Methodology

In this section, we introduce a novel temporal pathbased reasoning model with a neural-driven symbolic fashion for both the interpolation and the extrapolation TKG Reasoning settings.

### <span id="page-2-3"></span>4.1 Temporal Path in TKGs

Definition 1. *(Temporal link). In a TKG, each entity is viewed as a node in the graph, and a temporal link is viewed as an edge connecting two nodes which represent the subject* e<sup>s</sup> *and the object entity* e<sup>o</sup> *in a certain quadruple* (es, r, eo, t)*. Due to the heterogeneity and time constraints, each link is bonded with a relation* r *and a particular time* t*. Thus, we can denote a temporal link as* <sup>t</sup> r (es, eo)*.*

<span id="page-2-0"></span><sup>1</sup> See Appendix [A](#page-12-0) for more details.

Definition 2. *(Temporal path). A temporal path* P *is a combination of several temporal links that are sequentially connected from subject entity to object entity. We denote a temporal path* P *as*

$$
t_1
$$
<sub>t<sub>1</sub></sub>(e<sub>1</sub>, e<sub>2</sub>) $\wedge \frac{t_2}{r_2}$ (e<sub>2</sub>, e<sub>3</sub>) $\wedge \cdots \frac{t_\ell}{r_\ell}$ (e<sub>\ell</sub>, e<sub>\ell+1</sub>), (1)

*or* V<sup>ℓ</sup> i=1 ti ri (e<sup>i</sup> , ei+1) *for short, where* e1*,* e2*,* ···el+1 *are sequentially connected to form a chain, and* ℓ *is the path length. We take* e<sup>1</sup> *and* el+1 *as the origin and the destination of the path respectively, and use* P(i) *to denote the temporal link* <sup>t</sup><sup>i</sup> ri (e<sup>i</sup> , ei+1) *of the* i*-th step in* P*.* [2](#page-3-0)

For the extrapolation setting, a non-increasing temporal path fashion has been applied in recent works [\(Han et al.,](#page-9-9) [2021a;](#page-9-9) [Liu et al.,](#page-10-3) [2022\)](#page-10-3), and requires t<sup>1</sup> ≥ t<sup>2</sup> ≥ · · ·t<sup>ℓ</sup> ≥ tℓ+1. In this paper, we are not going to follow the non-increasing setup. For a query q = (eq, rq, ?, tq), we require each t<sup>i</sup> in a temporal path P to satisfy t<sup>i</sup> < t<sup>q</sup> such that we only use information from the past to predict the future, but have no restrictions to the chronological orders among t1, t2, · · · t<sup>l</sup> , i.e. we can have t<sup>i</sup> < ti+1, t<sup>i</sup> = ti+1 or t<sup>i</sup> > ti+1. This relaxation provides more temporal paths deriving from the temporal background, enabling us to utilize more information for reasoning. Further discussions for this can be found in Appendix [H.](#page-15-0)

For the interpolation setting, we mainly focus on how to find the missing object entity from the given subject entity e<sup>q</sup> and indeed we ignore any time constraints. For a temporal link <sup>t</sup><sup>i</sup> ri (e<sup>i</sup> , ei+1) in the temporal background, whether it is before or after tq, we can include it in a temporal path as long as it has been known to us.

### <span id="page-3-1"></span>4.2 Relative Time Encoding on Temporal Links

We adopt relative time encoding and focus on the impact of a certain temporal link in the temporal path on a query. For each temporal link ti ri (e<sup>i</sup> , ei+1), we first obtain the relative time ∆t<sup>i</sup> = t<sup>i</sup> − tq. Notice that a temporal link itself is query-independent, but the obtained relative time ∆t<sup>i</sup> is query-dependent. For the extrapolation setting, there is always an inequality ∆t<sup>i</sup> < 0 since t<sup>i</sup> < tq. But for the interpolation setting, ∆t<sup>i</sup> < 0, ∆t<sup>i</sup> = 0 and ∆t<sup>i</sup> > 0 are all possible since there is no restriction on the order of t<sup>i</sup> and tq.

As mentioned by [Zhu et al.](#page-11-4) [\(2021a\)](#page-11-4), many facts have occurred repeatedly throughout history, such as economic crises that occur every seven to ten years [\(Korotayev and Tsirel,](#page-9-13) [2010\)](#page-9-13). We pay close attention to the periodic property as well as the non-periodic property of time. We then extend the idea of periodic and non-periodic time vectors [\(Li](#page-9-8) [et al.,](#page-9-8) [2022a\)](#page-9-8) to a relative time encoding fashion:

$$
h_{t_i}^p = \sin(\omega_p \Delta t_i + \varphi_p)
$$

\n
$$
h_{t_i}^{np} = \omega_{np} \Delta t_i + \varphi_{np},
$$
\n(2)

where ωp, φp, ωnp, φnp are learnable parameters, sin() denotes the sine function, and the obtained h p ti and h np ti are the periodic and the non-periodic relative time vectors, respectively. For the periodic vector h p ti , the frequency ω<sup>p</sup> and the phase shift φ<sup>p</sup> reflect the periodic property. For the non-periodic vector h np ti , ωnp acts as a velocity vector [\(Han et al.,](#page-8-11) [2020\)](#page-8-11) indicating the temporal evolving dynamics.

Finally, we combine both periodic and nonperiodic properties to design our relative time embedding as:

$$
\boldsymbol{h}_{t_i} = \boldsymbol{h}_{t_i}^p + \boldsymbol{h}_{t_i}^{np} \,, \tag{3}
$$

where we use the same embedding dimension d for h p ti , h np ti and ht<sup>i</sup> .

### 4.3 Recursive Encoding on Temporal Paths

In Section [3.2,](#page-2-2) we have mentioned the idea of Bellman-Ford-based recursive encoding. Now, we start from the query and introduce our recursive encoding on temporal paths for TKG reasoning.

Basic Design Our recursive encoding on temporal paths aims to encode the destination entities of various temporal paths. And the basic idea is: Once the representations of the destination entities of all the (ℓ − 1)-length paths are ready, we can combine them with the link P(l) to encode the destination entities of the ℓ-length paths.

For a query q = (eq, rq, ?, tq), our recursive encoding is query-specific, and we start with the query entity eq. Initially, we can only reach the original entity eq, so we initialize h 0 <sup>e</sup><sup>q</sup> = 0 and the entity set E 0 <sup>e</sup><sup>q</sup> = {eq}. In the ℓ-th step, we collect all the ℓ-length temporal paths from temporal background based on eq, and update E ℓ <sup>e</sup><sup>q</sup> with the destination entities. We utilize D(Pe<sup>q</sup> ) to denote the destination entity set of the temporal paths Pe<sup>q</sup> , and Peq,(ℓ) to denote the set of links of the ℓ-th step in

<span id="page-3-0"></span><sup>2</sup>An illustration of temporal paths and temporal links is shared in Appendix [B.](#page-12-1)

Pe<sup>q</sup> . Thus, we actually have E ℓ <sup>e</sup><sup>q</sup> = E ℓ−1 eq ∪ D(Pe<sup>q</sup> ) for ℓ > 1.

Then, the message is passed along temporal paths Pe<sup>q</sup> from <sup>e</sup><sup>s</sup> to <sup>e</sup>o, where <sup>t</sup> r (es, eo) ∈ Peq,(l) . And we can get the representations for all e<sup>o</sup> ∈ D(Pe<sup>q</sup> ) for ℓ = 1, 2, · · ·L by:

$$
\boldsymbol{h}_{e_o}^{\ell} = \delta \Big(\boldsymbol{W}^{\ell} \sum\nolimits_{\mathcal{P}_{e_q,(\ell)}} \phi \big(\boldsymbol{h}_{e_s}^{\ell-1}, \boldsymbol{h}_r^{\ell}, \boldsymbol{h}_t\big) \Big),\qquad(4)
$$

where δ denotes an activation function, W<sup>ℓ</sup> ∈ R d×d is a learnable parameter, ϕ() denotes a function to compute and process the messages, h ℓ r is the embedding for relation r in the ℓ-th step, and h<sup>t</sup> is a result of the relative time encoding that we have introduced in Section [4.2.](#page-3-1) The proposed recursive encoding algorithm is shown in Algorithm [1.](#page-4-0) [3](#page-4-1)

<span id="page-4-0"></span>Algorithm 1 The Proposed Recursive Encoding Algorithm

- Input: A temporal knowledge graph G, a query q = (eq, rq, ?, tq), the maximum length L Output: The query-specific entity representations
- 1: initialize h 0 <sup>e</sup><sup>q</sup> = 0 and the entity set E 0 <sup>e</sup><sup>q</sup> = {eq};
- 2: for ℓ = 1, 2, · · ·L do
- 3: collect all the ℓ-length temporal paths and update E ℓ <sup>e</sup><sup>q</sup> with the destination entity set D(P<sup>e</sup><sup>q</sup> ); 4: message passing along temporal paths P<sup>e</sup><sup>q</sup> from
- e<sup>s</sup> ∈ D(P<sup>e</sup>q,(ℓ−1)) to e<sup>o</sup> ∈ D(P<sup>e</sup>q,(ℓ)): h ℓ <sup>e</sup><sup>o</sup> = δ W<sup>ℓ</sup> P Peq,(l) ϕ h ℓ−1 es ,h ℓ <sup>r</sup>, h<sup>t</sup> , 5: end for L ;

6: assign
$$
\mathbf{h}_{e_a}^L = \mathbf{0}
$$
for all $e_a \notin \mathcal{E}_{e_q}^L$

7: return h L ea for all e<sup>a</sup> ∈ E.

Message Passing We then give a detailed description of the message passing along temporal paths from e<sup>s</sup> to eo.

Given a quadruple (es, r, eo, t) in temporal ground, we can transform it to a temporal link t r (es, eo). We take the message as a combination of the query-specific representation of e<sup>s</sup> learned in the (ℓ − 1)-th recursive encoding step, the representation of r, and the representation of t:

$$
M_{(e_s,r,e_o,t)|q} = h_{e_s}^{\ell-1} + h_r^{\ell} + h_t, \qquad (5)
$$

Note that we use the same embedding dimension d for h ℓ−1 es , h ℓ r , h ℓ rq and h<sup>t</sup> .

Then, we utilize an attention-based mechanism to weigh the message. Inspired by graph attention networks [\(Velickovic et al.,](#page-10-16) [2018\)](#page-10-16), we first take a concatenation operation on h ℓ−1 es , h ℓ r , h ℓ rq and h<sup>t</sup> to get

$$
\boldsymbol{U}_{(e_s,r,e_o,t)|q} = concat[\boldsymbol{h}_{e_s}^{\ell-1}(e_q,r_q,t_q)||\boldsymbol{h}_r^{\ell}||\boldsymbol{h}_{r_q}^{\ell}||\boldsymbol{h}_t],
$$
\n(6)

where U(es,r,eo,t)|<sup>q</sup> ∈ R 4d is the concatenated result. Then, the attention weight for the message can be defined as

$$
\alpha_{(e_s,r,e_o,t)|\mathbf{q}}^{\ell} = \sigma \Big( (\mathbf{w}_{\alpha}^{\ell})^T ReLU(\mathbf{W}_{\alpha}^{\ell} \cdot \mathbf{U}_{(e_s,r,e_o,t)|\mathbf{q}}) \Big), \tag{7}
$$

where w<sup>ℓ</sup> <sup>α</sup> ∈ R <sup>d</sup>a, W<sup>ℓ</sup> <sup>α</sup> ∈ R da×4d are learnable parameters for attention (d<sup>a</sup> is the dimension for attention). Just like [\(Zhang and Yao,](#page-11-5) [2022\)](#page-11-5), we use the Sigmoid function σ rather than the Softmax function to ensure multiple temporal links can be selected in the same recursive step.

Aggregation With messages and the weights obtained, we take an aggregation operation on messages along different temporal links in various temporal paths, by means of a weighted sum of messages. For the ℓ-th recursive step, our encoded representation is specified as

$$
h_{e_o}^{\ell} = \delta \Big(W^{\ell} \sum\nolimits_{\mathcal{P}_{e_q,(\ell)}} \alpha^{\ell}_{(e_s,r,e_o,t)|q} \cdot M_{(e_s,r,e_o,t)|q} \Big) . \tag{8}
$$

So far, we have provided a detailed version of our recursive encoding function (also see a general version in Equation [4\)](#page-4-2) for each recursive step ℓ = 1, 2, · · ·L. After L recursive steps, the representation of each entity inside various L-length temporal paths (starting from eq) can be learned step by step. We assign h L ea (eq, rq, tq) = 0 for all e<sup>a</sup> ∈ E / L eq . For each entity e<sup>a</sup> ∈ E, we finally get its representation h L ea after L-length recursive encoding process.

### 4.4 Reasoning on Temporal Paths

Then, we can leverage the learned representations to measure the quality of temporal paths to reason.

Neural based Scoring To accomplish neuralsymbolic reasoning, we take a neural-based scoring first and use a simple scoring function to compute the likelihood for each candidate answer entity ea:

$$
f(\boldsymbol{q}, e_a) = \boldsymbol{w}^T \boldsymbol{h}_{e_a}^L(e_q, r_q, t_q), \qquad (9)
$$

where w ∈ R d is a parameter for scoring.

And for training loss, we use a multi-class logloss function to train the neural networks for our TKG Reasoning, which has been proven effective [\(Lacroix et al.,](#page-9-14) [2018;](#page-9-14) [Zhang and Yao,](#page-11-5) [2022\)](#page-11-5):

$$
\mathcal{L} = \sum_{(\mathbf{q}, e_a) \in \mathcal{T}_{\text{train}}} \left( -f(\mathbf{q}, e_a) + \log \left( \sum_{\forall e \in \mathcal{E}} e^{f(\mathbf{q}, e)} \right) \right), \tag{10}
$$

where Ttrain is set of training queries, and P ∀e∈E is for all the quadruples w.r.t. the same query q.

<span id="page-4-1"></span><sup>3</sup>The time complexity is O(|E|d + |V|d 2 ), where |E| and |V| denote the number of entities and relations respectively.

Symbolic Reasoning As for our symbolic reasoning, we target both the suitable temporal path and its destination entity. Using m<sup>i</sup> to denote the i-th intermediary entity, our reasoning can be expressed as

$$
t_{1}(e_{q}, m_{1}) \wedge \frac{t_{2}}{r_{2}}(m_{1}, m_{2}) \wedge \cdots \frac{t_{L}}{r_{L}}(m_{L-1}, e_{a})
$$

$$
\rightarrow \frac{t_{q}}{r_{q}}(e_{q}, e_{a}), \qquad (11)
$$

where the left part of → denotes a temporal path composed of L sequentially connected temporal links, and the right part is the link we aim to infer.

We use A<sup>ℓ</sup> eq ∈ {0, 1} Nℓ×N<sup>ℓ</sup> to denote the adjacent matrix of the ℓ-th step in the set of L-length paths Pe<sup>q</sup> starting from eq, i.e. Peq,(ℓ) , where N<sup>ℓ</sup> is the number of entities involved for ℓ = 1, 2, · · ·L. If <sup>t</sup><sup>1</sup> r1 (eq, m1) ∧ t2 r2 (m1, m2) ∧ · · ·t<sup>L</sup> rL (mL−1, ea) → tq rq (eq, ea) holds, ideally there exists a suitable path P ⋆ :

$$
\mathcal{P}^{\star} = \beta^1 A_{e_q}^1 \otimes \beta^2 A_{e_q}^2 \cdots \otimes \beta^L A_{e_q}^L.
$$
(12)

where β <sup>ℓ</sup> ∈ {0, 1} Nℓ×N<sup>ℓ</sup> is the choice of links for step ℓ.

From Equation [6](#page-4-3) and [7,](#page-4-4) we can know the learned α ℓ (es,r,eo,t)|<sup>q</sup> <sup>=</sup> MLP<sup>ℓ</sup> (es, r, eq, rq, ∆t), and abbreviate it as α ℓ . Our recursive encoding provides

$$
\arg\max_{\Theta} Score(\mathcal{P}) = \alpha^1 \mathbf{A}_{e_q}^1 \otimes \alpha^2 \mathbf{A}_{e_q}^2 \cdots \otimes \alpha^L \mathbf{A}_{e_q}^L,
$$
\n(13)

where Score(P) is the score of the path P obtained by Equation [9.](#page-4-5) Based on universal approximation theorem [\(Hornik,](#page-9-15) [1991\)](#page-9-15), there exists a set of parameters Θ that can learn α <sup>ℓ</sup> ≃ β ℓ , to make P ≃ P<sup>⋆</sup> . Note that multiple temporal paths may lead to the same destination. In such cases, the score can be regarded as a comprehensive measure of the various reasoning paths. Case-based analysis on this can be found in Section [5.4.](#page-7-0)

To summarize, our temporal path-based reasoning first collects temporal paths from the temporal background, then scores the destination entities of various temporal paths by attention-based recursive encoding, and lastly takes the entity with the highest score as the reasoning answer.

### 5 Experiments

### 5.1 Evaluation Protocol

Link prediction task that aims to infer incomplete time-wise fact with a missing entity ((s, r, ?, t) or (?, r, o, t)) is adopted to evaluate the proposed

model for both interpolation and extrapolation reasoning over TKGs. During inference, we follow the same procedure of [Xu et al.](#page-11-1) [\(2020\)](#page-11-1) to generate candidates. For a test sample (s, r, o, t), we first generate candidate quadruples set C = {(s, r, o, t) : o ∈ E} ∪ {(s, r, o, t) : s ∈ E} by replacing s or o with all possible entities, and then rank all the quadruples by their scores (Equation [9\)](#page-4-5). We use the time-wise filtered setting [\(Xu et al.,](#page-10-10) [2019;](#page-10-10) [Goel](#page-8-12) [et al.,](#page-8-12) [2020\)](#page-8-12) to report the experimental results.

We use ICEWS14, ICEWS05-15 [\(García-Durán](#page-8-8) [et al.,](#page-8-8) [2018\)](#page-8-8), YAGO11k [\(Dasgupta et al.,](#page-8-7) [2018\)](#page-8-7) and WIKIDATA12k [\(Dasgupta et al.,](#page-8-7) [2018\)](#page-8-7) datasets for interpolation reasoning evaluation, and use ICEWS14 [\(García-Durán et al.,](#page-8-8) [2018\)](#page-8-8), ICEWS18 [\(Jin et al.,](#page-9-1) [2020\)](#page-9-1), YAGO [\(Mahdisoltani et al.,](#page-10-17) [2015\)](#page-10-17) and WIKI [\(Leblay and Chekol,](#page-9-3) [2018\)](#page-9-3) for extrapolation.[4](#page-5-0) The performance is reported on the standard evaluation metrics: the proportion of correct triples ranked in the top 1, 3 and 10 (Hits@1, Hits@3, and Hits@10), and Mean Reciprocal Rank (MRR). All of them are the higher the better. For all experiments, we report averaged results across 5 runs, and we omit the variance as it is generally low.

### 5.2 Main Results

### 5.2.1 Interpolation Reasoning

Due to space limitations, we share the experimental details in Appendix [D.](#page-13-0) Table [1](#page-6-1) shows the results of the interpolation TKG Reasoning on link prediction over four experimented datasets where the proposed TPAR continuously outperforms all baselines across all metrics. We specifically compare our proposed TPAR with another GNN-based method, T-GAP [\(Jung et al.,](#page-9-5) [2021\)](#page-9-5), which samples a subgraph from the whole TKG for each node. In contrast, our TPAR recursively traverses the entire graph based on previously visited nodes to collect temporal paths. Our experimental results show that TPAR outperforms T-GAP across all evaluation metrics on the ICEWS14 and ICEWS05-15 datasets. This can be attributed to TPAR's ability to capture the temporal information of the entire graph and generate longer paths, which leads to more accurate and comprehensive TKG reasoning.

### 5.2.2 Extrapolation Reasoning

Experimental details for Extrapolation reasoning are shown in Appendix [E.](#page-13-1) Table [2](#page-6-2) presents the results of the extrapolation TKG reasoning on

<span id="page-5-0"></span><sup>4</sup>More details for datasets can be found in Appdendix [C.](#page-12-2)


| Interpolation | ICEWS14 | | | | | YAGO11k | | | ICEWS05-15<br>WIKIDATA12k | | | | | | | |
|---------------|---------|--------|---------|-------|------------|---------|---------|-------|---------------------------|--------|---------|-------|------------|--------|---------|-------|
| | Hits@1 | Hits@3 | Hits@10 | | MRR Hits@1 | Hits@3 | Hits@10 | | MRR Hits@1 | Hits@3 | Hits@10 | | MRR Hits@1 | Hits@3 | Hits@10 | MRR |
| TTransE | 7.4 | - | 60.1 | 25.5 | 2.0 | 15.0 | 25.1 | 10.8 | 8.4 | - | 61.6 | 27.1 | 9.6 | 18.4 | 32.9 | 17.2 |
| HyTE | 10.8 | 41.6 | 65.5 | 29.7 | 1.5 | 14.3 | 27.2 | 10.5 | 11.6 | 44.5 | 68.1 | 31.6 | 9.8 | 19.7 | 33.3 | 18.0 |
| TA-DistMult | 36.3 | - | 68.6 | 47.7 | 10.3 | 17.1 | 29.2 | 16.1 | 34.6 | - | 72.8 | 47.4 | 12.2 | 23.2 | 44.7 | 21.8 |
| ATiSE | 43.6 | 62.9 | 75.0 | 55.0 | 11.0 | 17.1 | 28.8 | 17.0 | 37.8 | 60.6 | 79.4 | 51.9 | 17.5 | 31.7 | 48.1 | 28.0 |
| TeRo | 46.8 | 62.1 | 73.2 | 56.2 | 12.1 | 19.7 | 31.9 | 18.7 | 46.9 | 66.8 | 79.5 | 58.6 | 19.8 | 32.9 | 50.7 | 29.9 |
| TComplEx | 53 | 66 | 77 | 61 | 12.7 | 18.3 | 30.7 | 18.5 | 59 | 71 | 80 | 66 | 23.3 | 35.7 | 53.9 | 33.1 |
| T-GAP | 50.9 | 67.7 | 79.0 | 61.0 | - | - | - | - | 56.8 | 74.3 | 84.5 | 67.0 | - | - | - | - |
| TELM | 54.5 | 67.3 | 77.4 | 62.5 | 12.9 | 19.4 | 32.1 | 19.1 | 59.9 | 72.8 | 82.3 | 67.8 | 23.1 | 36.0 | 54.2 | 33.2 |
| RotateQVS | 50.7 | 64.2 | 75.4 | 59.1 | 12.4 | 19.9 | 32.3 | 18.9 | 52.9 | 70.9 | 81.3 | 63.3 | 20.1 | 32.7 | 51.5 | 30.2 |
| TGoemE++ | 54.6 | 68.0 | 78.0 | 62.9 | 13.0 | 19.6 | 32.6 | 19.5 | 60.5 | 73.6 | 83.3 | 68.6 | 23.2 | 36.2 | 54.6 | 33.3 |
| TPAR (Ours) | 57.03 | 69.74 | 80.41 | 65.07 | 17.35 | 25.14 | 37.42 | 24.12 | 62.17 | 75.29 | 85.86 | 69.33 | 25.05 | 38.68 | 54.79 | 34.89 |

**Table 1:** Interpolation TKG Reasoning results (in percentage) on link prediction over four experimented datasets.


| Extrapolation | ICEWS14 | | | | | YAGO | | | ICEWS18<br>WIKI | | | | | | | |
|---------------|---------|--------|---------|-------|------------|--------|---------|-------|-----------------|--------|---------|-------|------------|--------|---------|-------|
| | Hits@1 | Hits@3 | Hits@10 | | MRR Hits@1 | Hits@3 | Hits@10 | | MRR Hits@1 | Hits@3 | Hits@10 | | MRR Hits@1 | Hits@3 | Hits@10 | MRR |
| RE-NET | 30.11 | 44.02 | 58.21 | 39.86 | 58.59 | 71.48 | 86.84 | 66.93 | 19.73 | 32.55 | 48.46 | 29.78 | 50.01 | 61.23 | 73.57 | 58.32 |
| CyGNeT | 27.43 | 42.63 | 57.90 | 37.65 | 58.97 | 76.80 | 86.98 | 68.98 | 17.21 | 30.97 | 46.85 | 27.12 | 47.89 | 66.44 | 78.70 | 58.78 |
| TANGO | - | - | - | - | 60.04 | 65.19 | 68.79 | 63.34 | 18.68 | 30.86 | 44.94 | 27.56 | 51.52 | 53.84 | 55.46 | 53.04 |
| xERTE | 32.70 | 45.67 | 57.30 | 40.79 | 80.09 | 88.02 | 89.78 | 84.19 | 21.03 | 33.51 | 46.48 | 29.31 | 69.05 | 78.03 | 79.73 | 73.60 |
| RE-GCN | 31.63 | 47.20 | 61.65 | 42.00 | 78.83 | 84.27 | 88.58 | 82.30 | 22.39 | 36.79 | 52.68 | 32.62 | 74.50 | 81.59 | 84.70 | 78.53 |
| TITer | 32.76 | 46.46 | 58.44 | 41.73 | 80.09 | 89.96 | 90.27 | 87.47 | 22.05 | 33.46 | 44.83 | 29.98 | 71.70 | 75.41 | 76.96 | 73.91 |
| CEN | 32.08 | 47.46 | 61.31 | 42.20 | - | - | - | - | 21.70 | 35.44 | 50.59 | 31.50 | 75.05 | 81.90 | 84.90 | 78.93 |
| TLogic | 33.56 | 48.27 | 61.23 | 43.04 | - | - | - | - | 20.54 | 33.95 | 48.53 | 29.82 | - | - | - | - |
| TIRGN | 33.83 | 48.95 | 63.84 | 44.04 | 84.34 | 91.37 | 92.92 | 87.95 | 23.19 | 37.99 | 54.22 | 33.66 | 77.77 | 85.12 | 87.08 | 81.65 |
| RPC | 34.87 | 49.80 | 65.08 | 44.55 | 85.10 | 92.57 | 94.04 | 88.87 | 24.34 | 38.74 | 55.89 | 34.91 | 76.28 | 85.43 | 88.71 | 81.18 |
| TPAR (Ours) | 36.88 | 52.28 | 65.89 | 46.89 | 89.67 | 92.93 | 94.60 | 91.53 | 26.58 | 39.27 | 56.94 | 35.76 | 79.85 | 87.04 | 88.96 | 83.20 |

**Table 2:** Extrapolation TKG Reasoning results (in percentage) on link prediction over four experimented datasets.

link prediction across four different datasets. Notably, we compare TPAR with two SOTA methods, namely, the neural network-based RPC [\(Liang](#page-9-10) [et al.,](#page-9-10) [2023\)](#page-9-10) and the symbolic-based TLogic [\(Liu](#page-10-3) [et al.,](#page-10-3) [2022\)](#page-10-3). Our results show that TPAR outperforms all baselines, underscoring the benefits of combining neural and symbolic-based approaches for TKG reasoning.

### <span id="page-6-0"></span>5.3 Analysis on Pipeline Setting

To test the hypothesis that completing missing knowledge about the past can enhance the accuracy of predicting future knowledge, we design a novel experimental pipeline. Building upon the facts within the known time range, we sample a ratio of facts to train interpolation, while the other unsampled facts have either the subject entity or the object entity masked, forming incomplete quadruples. Specifically, we have three settings: set the ratio to 60% for Setting A, 70% for Setting B, and 80% for Setting C.[5](#page-6-3) The lower the ratio, the more incomplete facts need to be interpolated first.

The pipeline involves first completing these incomplete quadruples through interpolation, and subsequently predicting future events. Baselines: Since there are currently no existing methods capable of both interpolation and extrapolation, we assemble SOTA interpolation and extrapolation meth-


| | Interpolation Extrapolation | Setting | | | | | | | | |
|-----------|-----------------------------|---------|----------------------------------------------|-------|--|--|--|--|--|--|
| | | | A (Ratio: 60%) B (Ratio: 70%) C (Ratio: 80%) | | | | | | | |
| TELM | TLogic | 40.88 | 41.55 | 42.09 | | | | | | |
| \$ | TLogic | 41.85 | 41.88 | 42.18 | | | | | | |
| RotateQVS | TIRGN | 40.86 | 42.35 | 42.78 | | | | | | |
| \$ | TIRGN | 42.53 | 43.68 | 43.69 | | | | | | |
| TPAR | TPAR | 44.56 | 46.07 | 46.66 | | | | | | |
| \$ | TPAR | 43.86 | 45.49 | 36.36 | | | | | | |

**Table 3:** MRR performance of the pipeline setting on ICEWS 14.

ods[6](#page-6-4) , and get two combinations: a) TELM and TLogic, b) RotateQVS and TIRGN.

The experimental results in Table [3](#page-6-5) [7](#page-6-6) show two key observations: a) For both of the SOTA combination baselines, employing the pipeline (interpolation followed by extrapolation) leads to a reduction in extrapolation performance compared to straightforward extrapolation. And this reduction in the effect is gradually alleviated as the ratio increases from 60% to 80%. We believe that this could be attributed to the fact that the newly acquired knowledge from interpolation may contain errors, which have the potential to propagate and amplify in subsequent extrapolation. As the amount of newly acquired knowledge decreases, the likelihood of introducing errors into the system also diminishes.

<span id="page-6-3"></span><sup>5</sup> See Appendix [F](#page-14-0) for full pipeline setting details.

<span id="page-6-4"></span><sup>6</sup> For fairness, we do not use TGoemE++ and RPC as they have not made their code publicly available.

<span id="page-6-6"></span><sup>7</sup> See Table [5](#page-14-1) for the more detailed results.

<span id="page-7-3"></span><span id="page-7-2"></span><span id="page-7-1"></span>

| (a) Interpolation for the maximum length L = 2. |
|-------------------------------------------------|
| |
| |
| |
| |
| |
| |
| |
| |
| |
| |
| |
| |
| |
| |
| |
| |
| |
| |
| |
| |
| |
| |
| |
| |

(b) Extrapolation for the maximum length L = 3.

**Figure 2:** Path interpretations of TKG reasoning on ICEWS14 test set. Dashed lines mean inverse relations.

b) In all three settings, our TPAR with pipeline outperforms the straightforward extrapolation results, which demonstrates the superiority of our TPAR model to effectively integrate interpolation and extrapolation as a unified task for TKG reasoning.

### <span id="page-7-0"></span>5.4 Case Study: Path Interpretations

Benefiting from the neural-symbolic fashion, we can interpret the reasoning results through temporal paths. Following local interpretation methods [\(Zeiler and Fergus,](#page-11-6) [2014;](#page-11-6) [Zhu et al.,](#page-11-7) [2021b\)](#page-11-7), we approximate the local landscape of our TPAR with a linear model over the set of all paths, i.e., 1st-order Taylor polynomial. Thus, the importance of a path can be defined as its weight in the linear model and can be computed by the partial derivative of the prediction w.r.t. the path. Formally, top-k temporal path interpretations for f(q, ea) are defined as

$$
P_1, P_2, ..., P_k = \underset{P \in \mathcal{P}_{e_q e_a}}{\text{top-k}} \frac{\partial f(q, e_a)}{\partial P}, \quad (14)
$$

where Peqe<sup>a</sup> denotes the set of all temporal paths starting from e<sup>q</sup> to ea.

Fig. [2](#page-7-1) illustrates the path interpretations of TKG reasoning for both two settings on the ICEWS14 test set. While users may have different insights

<span id="page-7-4"></span>![](_page_7_Figure_9.jpeg)
<!-- Image Description: This image presents two bar charts comparing the Mean Reciprocal Rank (MRR) of different knowledge graph completion methods (RotateQVS, TELM, TPAR, TLogic, TIRGN) at varying sparsity ratios. Chart (a) shows interpolation results, while (b) shows extrapolation. Both charts illustrate how MRR performance changes across different methods as data sparsity increases. The purpose is to compare the robustness of these methods under varying data conditions. -->

**Figure 3:** Performance w.r.t. sparsity ratio on ICEWS14.

towards the visualization, here are our understandings: 1) In Fig. [2\(a\),](#page-7-2) for the interpolation setting, when we need to reason about the fact that happened on t<sup>q</sup> =2014-02-14, we can use the path formed by the links before or after tq. 2) For the extrapolation of Fig. [2\(b\),](#page-7-3) we do not strictly impose a chronological order constraint on the links in the path, ensuring that the paths used in our reasoning can be as rich as possible. 3) Multiple different temporal paths may lead to the same reasoning destination, and the explanation is that a reasoning result can have multiple evidence chains.

In addition, we conduct analyses on path lengths, and the contents can be found in Appendix [G.](#page-14-2)

### 5.5 Robustness Analysis

Fig[.3](#page-7-4) illustrates a performance comparison under varying degrees of data sparsity on the ICEWS14 dataset. We compare our TPAR model with RotateQVS [\(Chen et al.,](#page-8-1) [2022\)](#page-8-1) and TELM [\(Xu et al.,](#page-10-1) [2021\)](#page-10-1) in the interpolation setting, while TLogic [\(Liu et al.,](#page-10-3) [2022\)](#page-10-3) and TIRGN [\(Li et al.,](#page-9-8) [2022a\)](#page-9-8) are taken as extrapolation baselines. Our TPAR demonstrates superior performance compared to the other models across a wide range of data sparsity levels for both interpolation and extrapolation settings. This highlights its exceptional robustness and ability to handle sparse data effectively.

Furthermore, we conduct an analysis on the chronological order in Appendix [H,](#page-15-0) which also demonstrates robustness to some extent.

### 6 Conclusion

We propose a temporal path-based reasoning (TPAR) model with a neural-symbolic fashion that can be applied to both interpolation and extrapolation TKG Reasoning settings in this paper. Introducing the Bellman-Ford Algorithm and a recursive encoding method to score the destination entities of various temporal paths, TPAR performs robustly on uncertain temporal knowledge with fine interpretability. Comprehensive experiments demonstrate the superiority of our proposed model for both settings. A well-designed pipeline experiment further verified that TPAR is capable of integrating two settings for a unified TKG reasoning.

### 7 Limitations

We identify that there may be some possible limitations in this study. First, our reasoning results are dependent on the embeddings learned by the proposed (Bellman-Ford-based) recursive encoding algorithm, where the selection of hyperparameters may have a significant impact on the reasoning results. Further, we can explore additional neuralsymbolic reasoning approaches, expanding beyond the current neural-driven symbolic fashion. Second, the reasoning process relies on attention mechanisms, but it has been pointed out [\(Sui et al.,](#page-10-18) [2022\)](#page-10-18) that existing attention-based methods are prone to visit the noncausal features as the shortcut to predictions. In future work, we will try to focus on researching causal attention mechanisms for a more solid comprehension of the complicated correlations between temporal knowledge.

### Acknowledgements

This work is particularly supported by the National Key Research and Development Program of China (No. 2022YFB31040103), and the National Natural Science Foundation of China (No. 62302507).

### References

- <span id="page-8-4"></span>John S. Baras and George Theodorakopoulos. 2010. *[Path Problems in Networks](https://doi.org/10.2200/S00245ED1V01Y201001CNT003)*. Synthesis Lectures on Communication Networks. Morgan & Claypool Publishers.
- <span id="page-8-3"></span>Richard Bellman. 1958. On a routing problem. *Quarterly of Applied Mathematics*, 16:87–90.
- <span id="page-8-0"></span>Kurt D. Bollacker, Colin Evans, Praveen Paritosh, Tim Sturge, and Jamie Taylor. 2008. Freebase: a collaboratively created graph database for structuring human knowledge. In *Proceedings of the ACM SIGMOD International Conference on Management of Data, SIGMOD 2008*, pages 1247–1250.
- <span id="page-8-5"></span>Antoine Bordes, Nicolas Usunier, Alberto Garcia-Duran, Jason Weston, and Oksana Yakhnenko. 2013. Translating embeddings for modeling multirelational data. In *Advances in neural information processing systems*, pages 2787–2795.
- <span id="page-8-1"></span>Kai Chen, Ye Wang, Yitong Li, and Aiping Li. 2022. [Rotateqvs: Representing temporal information as](https://doi.org/10.18653/v1/2022.acl-long.402)

[rotations in quaternion vector space for temporal](https://doi.org/10.18653/v1/2022.acl-long.402) [knowledge graph completion.](https://doi.org/10.18653/v1/2022.acl-long.402) In *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2022, Dublin, Ireland, May 22-27, 2022*, pages 5843– 5857. Association for Computational Linguistics.

- <span id="page-8-7"></span>Shib Sankar Dasgupta, Swayambhu Nath Ray, and Partha Talukdar. 2018. Hyte: Hyperplane-based temporally aware knowledge graph embedding. In *Proceedings of the 2018 conference on empirical methods in natural language processing*, pages 2001– 2011.
- <span id="page-8-6"></span>Tim Dettmers, Pasquale Minervini, Pontus Stenetorp, and Sebastian Riedel. 2018. Convolutional 2d knowledge graph embeddings. In *Proceedings of the Thirty-Second AAAI Conference on Artificial Intelligence*, pages 1811–1818.
- <span id="page-8-13"></span>Fredo Erxleben, Michael Günther, Markus Krötzsch, Julian Mendez, and Denny Vrandecic. 2014. [Introduc](https://doi.org/10.1007/978-3-319-11964-9_4)[ing wikidata to the linked data web.](https://doi.org/10.1007/978-3-319-11964-9_4) In *The Semantic Web - ISWC 2014 - 13th International Semantic Web Conference, Riva del Garda, Italy, October 19-23, 2014. Proceedings, Part I*, volume 8796 of *Lecture Notes in Computer Science*, pages 50–65. Springer.

<span id="page-8-2"></span>Lester Randolph Ford. 1956. Network flow theory.

- <span id="page-8-8"></span>Alberto García-Durán, Sebastijan Dumancic, and Mathias Niepert. 2018. Learning sequence encoders for temporal knowledge graph completion. In *Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing, Brussels, Belgium, October 31 - November 4, 2018*, pages 4816–4821. Association for Computational Linguistics.
- <span id="page-8-12"></span>Rishab Goel, Seyed Mehran Kazemi, Marcus Brubaker, and Pascal Poupart. 2020. Diachronic embedding for temporal knowledge graph completion. *Proceedings of the AAAI Conference on Artificial Intelligence*, 34(04):3988–3995.
- <span id="page-8-9"></span>Shu Guo, Quan Wang, Lihong Wang, Bin Wang, and Li Guo. 2016. [Jointly embedding knowledge graphs](https://doi.org/10.18653/v1/d16-1019) [and logical rules.](https://doi.org/10.18653/v1/d16-1019) In *Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing, EMNLP 2016, Austin, Texas, USA, November 1-4, 2016*, pages 192–202. The Association for Computational Linguistics.
- <span id="page-8-10"></span>Shu Guo, Quan Wang, Lihong Wang, Bin Wang, and Li Guo. 2018. [Knowledge graph embedding with](https://www.aaai.org/ocs/index.php/AAAI/AAAI18/paper/view/16369) [iterative guidance from soft rules.](https://www.aaai.org/ocs/index.php/AAAI/AAAI18/paper/view/16369) In *Proceedings of the Thirty-Second AAAI Conference on Artificial Intelligence, (AAAI-18), the 30th innovative Applications of Artificial Intelligence (IAAI-18), and the 8th AAAI Symposium on Educational Advances in Artificial Intelligence (EAAI-18), New Orleans, Louisiana, USA, February 2-7, 2018*, pages 4816–4823. AAAI Press.
- <span id="page-8-11"></span>Zhen Han, Peng Chen, Yunpu Ma, and Volker Tresp. 2020. [Dyernie: Dynamic evolution of riemannian](https://doi.org/10.18653/v1/2020.emnlp-main.593)

[manifold embeddings for temporal knowledge graph](https://doi.org/10.18653/v1/2020.emnlp-main.593) [completion.](https://doi.org/10.18653/v1/2020.emnlp-main.593) In *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing, EMNLP 2020, Online, November 16-20, 2020*, pages 7301–7316. Association for Computational Linguistics.

- <span id="page-9-9"></span>Zhen Han, Peng Chen, Yunpu Ma, and Volker Tresp. 2021a. [Explainable subgraph reasoning for forecast](https://openreview.net/forum?id=pGIHq1m7PU)[ing on temporal knowledge graphs.](https://openreview.net/forum?id=pGIHq1m7PU) In *9th International Conference on Learning Representations, ICLR 2021, Virtual Event, Austria, May 3-7, 2021*. OpenReview.net.
- <span id="page-9-6"></span>Zhen Han, Zifeng Ding, Yunpu Ma, Yujia Gu, and Volker Tresp. 2021b. [Learning neural ordinary equa](https://doi.org/10.18653/v1/2021.emnlp-main.658)[tions for forecasting future links on temporal knowl](https://doi.org/10.18653/v1/2021.emnlp-main.658)[edge graphs.](https://doi.org/10.18653/v1/2021.emnlp-main.658) In *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, EMNLP 2021, Virtual Event / Punta Cana, Dominican Republic, 7-11 November, 2021*, pages 8352– 8364. Association for Computational Linguistics.
- <span id="page-9-15"></span>Kurt Hornik. 1991. [Approximation capabilities of](https://doi.org/https://doi.org/10.1016/0893-6080(91)90009-T) [multilayer feedforward networks.](https://doi.org/https://doi.org/10.1016/0893-6080(91)90009-T) *Neural Networks*, 4(2):251–257.
- <span id="page-9-4"></span>Prachi Jain, Sushant Rathi, Mausam, and Soumen Chakrabarti. 2020. [Temporal knowledge base com](https://doi.org/10.18653/v1/2020.emnlp-main.305)[pletion: New algorithms and evaluation protocols.](https://doi.org/10.18653/v1/2020.emnlp-main.305) In *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing, EMNLP 2020, Online, November 16-20, 2020*, pages 3733– 3747. Association for Computational Linguistics.
- <span id="page-9-1"></span>Woojeong Jin, Meng Qu, Xisen Jin, and Xiang Ren. 2020. Recurrent event network: Autoregressive structure inference over temporal knowledge graphs. In *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, pages 6669–6683.
- <span id="page-9-5"></span>Jaehun Jung, Jinhong Jung, and U Kang. 2021. [Learn](https://doi.org/10.1145/3447548.3467292)[ing to walk across time for interpretable temporal](https://doi.org/10.1145/3447548.3467292) [knowledge graph completion.](https://doi.org/10.1145/3447548.3467292) In *KDD '21: The 27th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, Virtual Event, Singapore, August 14-18, 2021*, pages 786–795. ACM.
- <span id="page-9-13"></span>Andrey V. Korotayev and Sergey V. Tsirel. 2010. A spectral analysis of world gdp dynamics: Kondratieff waves, kuznets swings, juglar and kitchin cycles in global economic development, and the 2008c2009 economic crisis. *Structure and Dynamics: eJournal of Anthropological and Related Sciences*, pages 1– 57.
- <span id="page-9-0"></span>Timothée Lacroix, Guillaume Obozinski, and Nicolas Usunier. 2020. [Tensor decompositions for temporal](https://openreview.net/forum?id=rke2P1BFwS) [knowledge base completion.](https://openreview.net/forum?id=rke2P1BFwS) In *8th International Conference on Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April 26-30, 2020*. OpenReview.net.

- <span id="page-9-14"></span>Timothée Lacroix, Nicolas Usunier, and Guillaume Obozinski. 2018. [Canonical tensor decomposition](http://proceedings.mlr.press/v80/lacroix18a.html) [for knowledge base completion.](http://proceedings.mlr.press/v80/lacroix18a.html) In *Proceedings of the 35th International Conference on Machine Learning, ICML 2018, Stockholmsmässan, Stockholm, Sweden, July 10-15, 2018*, volume 80 of *Proceedings of Machine Learning Research*, pages 2869–2878. PMLR.
- <span id="page-9-11"></span>Ni Lao and William W. Cohen. 2010. [Relational re](https://doi.org/10.1007/s10994-010-5205-8)[trieval using a combination of path-constrained ran](https://doi.org/10.1007/s10994-010-5205-8)[dom walks.](https://doi.org/10.1007/s10994-010-5205-8) *Mach. Learn.*, 81(1):53–67.
- <span id="page-9-12"></span>Ni Lao, Amarnag Subramanya, Fernando C. N. Pereira, and William W. Cohen. 2012. [Reading the web with](https://aclanthology.org/D12-1093/) [learned syntactic-semantic inference rules.](https://aclanthology.org/D12-1093/) In *Proceedings of the 2012 Joint Conference on Empirical Methods in Natural Language Processing and Computational Natural Language Learning, EMNLP-CoNLL 2012, July 12-14, 2012, Jeju Island, Korea*, pages 1017–1026. ACL.
- <span id="page-9-16"></span>Jennifer Lautenschlager, Steve Shellman, and Michael Ward. 2015. Icews events and aggregations. *Harvard Dataverse*, 3.
- <span id="page-9-3"></span>Julien Leblay and Melisachew Wudage Chekol. 2018. Deriving validity time in knowledge graph. In *Companion Proceedings of the The Web Conference 2018*, pages 1771–1776.
- <span id="page-9-8"></span>Yujia Li, Shiliang Sun, and Jing Zhao. 2022a. [Tirgn:](https://doi.org/10.24963/ijcai.2022/299) [Time-guided recurrent graph network with local](https://doi.org/10.24963/ijcai.2022/299)[global historical patterns for temporal knowledge](https://doi.org/10.24963/ijcai.2022/299) [graph reasoning.](https://doi.org/10.24963/ijcai.2022/299) In *Proceedings of the Thirty-First International Joint Conference on Artificial Intelligence, IJCAI 2022, Vienna, Austria, 23-29 July 2022*, pages 2152–2158. ijcai.org.
- <span id="page-9-7"></span>Zixuan Li, Saiping Guan, Xiaolong Jin, Weihua Peng, Yajuan Lyu, Yong Zhu, Long Bai, Wei Li, Jiafeng Guo, and Xueqi Cheng. 2022b. [Complex evolutional](https://doi.org/10.18653/v1/2022.acl-short.32) [pattern learning for temporal knowledge graph rea](https://doi.org/10.18653/v1/2022.acl-short.32)[soning.](https://doi.org/10.18653/v1/2022.acl-short.32) In *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers), ACL 2022, Dublin, Ireland, May 22-27, 2022*, pages 290–296. Association for Computational Linguistics.
- <span id="page-9-2"></span>Zixuan Li, Xiaolong Jin, Wei Li, Saiping Guan, Jiafeng Guo, Huawei Shen, Yuanzhuo Wang, and Xueqi Cheng. 2021. [Temporal knowledge graph reason](https://doi.org/10.1145/3404835.3462963)[ing based on evolutional representation learning.](https://doi.org/10.1145/3404835.3462963) In *SIGIR '21: The 44th International ACM SIGIR Conference on Research and Development in Information Retrieval, Virtual Event, Canada, July 11-15, 2021*, pages 408–417. ACM.
- <span id="page-9-10"></span>Ke Liang, Lingyuan Meng, Meng Liu, Yue Liu, Wenxuan Tu, Siwei Wang, Sihang Zhou, and Xinwang Liu. 2023. [Learn from relational correlations and periodic](https://doi.org/10.1145/3539618.3591711) [events for temporal knowledge graph reasoning.](https://doi.org/10.1145/3539618.3591711) In *Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval, SIGIR 2023, Taipei, Taiwan, July 23-27, 2023*, pages 1559–1568. ACM.

- <span id="page-10-5"></span>Yankai Lin, Zhiyuan Liu, Maosong Sun, Yang Liu, and Xuan Zhu. 2015. Learning entity and relation embeddings for knowledge graph completion. In *Proceedings of the Twenty-Ninth AAAI Conference on Artificial Intelligence, January 25-30, 2015, Austin, Texas, USA*, pages 2181–2187. AAAI Press.
- <span id="page-10-3"></span>Yushan Liu, Yunpu Ma, Marcel Hildebrandt, Mitchell Joblin, and Volker Tresp. 2022. [Tlogic: Tempo](https://ojs.aaai.org/index.php/AAAI/article/view/20330)[ral logical rules for explainable link forecasting on](https://ojs.aaai.org/index.php/AAAI/article/view/20330) [temporal knowledge graphs.](https://ojs.aaai.org/index.php/AAAI/article/view/20330) In *Thirty-Sixth AAAI Conference on Artificial Intelligence, AAAI 2022, Thirty-Fourth Conference on Innovative Applications of Artificial Intelligence, IAAI 2022, The Twelveth Symposium on Educational Advances in Artificial Intelligence, EAAI 2022 Virtual Event, February 22 - March 1, 2022*, pages 4120–4127. AAAI Press.
- <span id="page-10-17"></span>Farzaneh Mahdisoltani, Joanna Biega, and Fabian M. Suchanek. 2015. YAGO3: A knowledge base from multilingual wikipedias. In *CIDR 2015, Seventh Biennial Conference on Innovative Data Systems Research*.
- <span id="page-10-15"></span>Arvind Neelakantan, Benjamin Roth, and Andrew Mc-Callum. 2015. [Compositional vector space models](http://www.aaai.org/ocs/index.php/SSS/SSS15/paper/view/10254) [for knowledge base inference.](http://www.aaai.org/ocs/index.php/SSS/SSS15/paper/view/10254) In *2015 AAAI Spring Symposia, Stanford University, Palo Alto, California, USA, March 22-25, 2015*. AAAI Press.
- <span id="page-10-13"></span>Meng Qu and Jian Tang. 2019. [Probabilistic logic neu](https://proceedings.neurips.cc/paper/2019/hash/13e5ebb0fa112fe1b31a1067962d74a7-Abstract.html)[ral networks for reasoning.](https://proceedings.neurips.cc/paper/2019/hash/13e5ebb0fa112fe1b31a1067962d74a7-Abstract.html) In *Advances in Neural Information Processing Systems 32: Annual Conference on Neural Information Processing Systems 2019, NeurIPS 2019, December 8-14, 2019, Vancouver, BC, Canada*, pages 7710–7720.
- <span id="page-10-14"></span>Luc De Raedt, Angelika Kimmig, and Hannu Toivonen. 2007. [Problog: A probabilistic prolog and its applica](http://ijcai.org/Proceedings/07/Papers/396.pdf)[tion in link discovery.](http://ijcai.org/Proceedings/07/Papers/396.pdf) In *IJCAI 2007, Proceedings of the 20th International Joint Conference on Artificial Intelligence, Hyderabad, India, January 6-12, 2007*, pages 2462–2467.
- <span id="page-10-12"></span>Matthew Richardson and Pedro M. Domingos. 2006. [Markov logic networks.](https://doi.org/10.1007/s10994-006-5833-1) *Mach. Learn.*, 62(1-2):107– 136.
- <span id="page-10-8"></span>Michael Sejr Schlichtkrull, Thomas N. Kipf, Peter Bloem, Rianne van den Berg, Ivan Titov, and Max Welling. 2018. Modeling relational data with graph convolutional networks. In *The Semantic Web - 15th International Conference, ESWC 2018*, volume 10843, pages 593–607.
- <span id="page-10-7"></span>Chao Shang, Yun Tang, Jing Huang, Jinbo Bi, Xiaodong He, and Bowen Zhou. 2019. End-to-end structureaware convolutional networks for knowledge base completion. In *The Thirty-Third AAAI Conference on Artificial Intelligence*, pages 3060–3067.
- <span id="page-10-0"></span>Yichen Song, Aiping Li, Hongkui Tu, Kai Chen, and Chenchen Li. 2021. [A novel encoder-decoder knowl](https://doi.org/10.3389/fnbot.2021.674428)[edge graph completion model for robot brain.](https://doi.org/10.3389/fnbot.2021.674428) *Frontiers Neurorobotics*, 15:674428.

- <span id="page-10-18"></span>Yongduo Sui, Xiang Wang, Jiancan Wu, Min Lin, Xiangnan He, and Tat-Seng Chua. 2022. [Causal attention](https://doi.org/10.1145/3534678.3539366) [for interpretable and generalizable graph classifica](https://doi.org/10.1145/3534678.3539366)[tion.](https://doi.org/10.1145/3534678.3539366) In *KDD '22: The 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, Washington, DC, USA, August 14 - 18, 2022*, pages 1696–1705. ACM.
- <span id="page-10-2"></span>Haohai Sun, Jialun Zhong, Yunpu Ma, Zhen Han, and Kun He. 2021. [Timetraveler: Reinforcement learning](https://doi.org/10.18653/v1/2021.emnlp-main.655) [for temporal knowledge graph forecasting.](https://doi.org/10.18653/v1/2021.emnlp-main.655) In *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, EMNLP 2021, Virtual Event / Punta Cana, Dominican Republic, 7- 11 November, 2021*, pages 8306–8319. Association for Computational Linguistics.
- <span id="page-10-6"></span>Théo Trouillon, Johannes Welbl, Sebastian Riedel, Éric Gaussier, and Guillaume Bouchard. 2016. Complex embeddings for simple link prediction. In *Proceedings of the 33nd International Conference on Machine Learning, ICML 2016*, volume 48 of *JMLR Workshop and Conference Proceedings*, pages 2071– 2080.
- <span id="page-10-9"></span>Shikhar Vashishth, Soumya Sanyal, Vikram Nitin, and Partha P. Talukdar. 2020. [Composition-based multi](https://openreview.net/forum?id=BylA_C4tPr)[relational graph convolutional networks.](https://openreview.net/forum?id=BylA_C4tPr) In *8th International Conference on Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April 26-30, 2020*. OpenReview.net.
- <span id="page-10-16"></span>Petar Velickovic, Guillem Cucurull, Arantxa Casanova, Adriana Romero, Pietro Liò, and Yoshua Bengio. 2018. [Graph attention networks.](https://openreview.net/forum?id=rJXMpikCZ) In *6th International Conference on Learning Representations, ICLR 2018, Vancouver, BC, Canada, April 30 - May 3, 2018, Conference Track Proceedings*. OpenReview.net.
- <span id="page-10-11"></span>Pengwei Wang, Dejing Dou, Fangzhao Wu, Nisansa de Silva, and Lianwen Jin. 2019. [Logic rules](http://arxiv.org/abs/1903.03772) [powered knowledge graph embedding.](http://arxiv.org/abs/1903.03772) *CoRR*, abs/1903.03772.
- <span id="page-10-4"></span>Zhen Wang, Jianwen Zhang, Jianlin Feng, and Zheng Chen. 2014. [Knowledge graph embedding by trans](http://www.aaai.org/ocs/index.php/AAAI/AAAI14/paper/view/8531)[lating on hyperplanes.](http://www.aaai.org/ocs/index.php/AAAI/AAAI14/paper/view/8531) In *Proceedings of the Twenty-Eighth AAAI Conference on Artificial Intelligence, July 27 -31, 2014, Québec City, Québec, Canada*, pages 1112–1119. AAAI Press.
- <span id="page-10-1"></span>Chengjin Xu, Yung-Yu Chen, Mojtaba Nayyeri, and Jens Lehmann. 2021. [Temporal knowledge graph](https://doi.org/10.18653/v1/2021.naacl-main.202) [completion using a linear temporal regularizer and](https://doi.org/10.18653/v1/2021.naacl-main.202) [multivector embeddings.](https://doi.org/10.18653/v1/2021.naacl-main.202) In *Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, NAACL-HLT 2021, Online, June 6-11, 2021*, pages 2569–2578. Association for Computational Linguistics.
- <span id="page-10-10"></span>Chengjin Xu, Mojtaba Nayyeri, Fouad Alkhoury, Jens Lehmann, and Hamed Shariat Yazdi. 2019. Temporal knowledge graph embedding model based on additive time series decomposition. *CoRR*, abs/1911.07893.

- <span id="page-11-1"></span>Chengjin Xu, Mojtaba Nayyeri, Fouad Alkhoury, Hamed Shariat Yazdi, and Jens Lehmann. 2020. TeRo: A time-aware knowledge graph embedding via temporal rotation. In *Proceedings of the 28th International Conference on Computational Linguistics*, pages 1583–1593, Barcelona, Spain (Online). International Committee on Computational Linguistics.
- <span id="page-11-8"></span>Chengjin Xu, Mojtaba Nayyeri, Yung-Yu Chen, and Jens Lehmann. 2023. [Geometric algebra based](https://doi.org/10.1109/TKDE.2022.3151435) [embeddings for static and temporal knowledge](https://doi.org/10.1109/TKDE.2022.3151435) [graph completion.](https://doi.org/10.1109/TKDE.2022.3151435) *IEEE Trans. Knowl. Data Eng.*, 35(5):4838–4851.
- <span id="page-11-3"></span>Bishan Yang, Wen-tau Yih, Xiaodong He, Jianfeng Gao, and Li Deng. 2015. Embedding entities and relations for learning and inference in knowledge bases. In *3rd International Conference on Learning Representations, ICLR 2015*.
- <span id="page-11-6"></span>Matthew D. Zeiler and Rob Fergus. 2014. [Visualiz](https://doi.org/10.1007/978-3-319-10590-1_53)[ing and understanding convolutional networks.](https://doi.org/10.1007/978-3-319-10590-1_53) In *Computer Vision - ECCV 2014 - 13th European Conference, Zurich, Switzerland, September 6-12, 2014, Proceedings, Part I*, volume 8689 of *Lecture Notes in Computer Science*, pages 818–833. Springer.
- <span id="page-11-2"></span>Jing Zhang, Bo Chen, Lingxi Zhang, Xirui Ke, and Haipeng Ding. 2021. [Neural, symbolic and neural](https://doi.org/10.1016/j.aiopen.2021.03.001)[symbolic reasoning on knowledge graphs.](https://doi.org/10.1016/j.aiopen.2021.03.001) *AI Open*, 2:14–35.
- <span id="page-11-5"></span>Yongqi Zhang and Quanming Yao. 2022. [Knowledge](https://doi.org/10.1145/3485447.3512008) [graph reasoning with relational digraph.](https://doi.org/10.1145/3485447.3512008) In *WWW '22: The ACM Web Conference 2022, Virtual Event, Lyon, France, April 25 - 29, 2022*, pages 912–924. ACM.
- <span id="page-11-0"></span>Xiaojuan Zhao, Yan Jia, Aiping Li, Rong Jiang, Kai Chen, and Ye Wang. 2021. [Target relational attention](https://doi.org/10.1016/j.neucom.2021.03.135)[oriented knowledge graph reasoning.](https://doi.org/10.1016/j.neucom.2021.03.135) *Neurocomputing*, 461:577–586.
- <span id="page-11-4"></span>Cunchao Zhu, Muhao Chen, Changjun Fan, Guangquan Cheng, and Yan Zhang. 2021a. Learning from history: Modeling temporal knowledge graphs with sequential copy-generation networks. In *Thirty-Fifth AAAI Conference on Artificial Intelligence, AAAI 2021, Thirty-Third Conference on Innovative Applications of Artificial Intelligence, IAAI 2021, The Eleventh Symposium on Educational Advances in Artificial Intelligence, EAAI 2021, Virtual Event, February 2-9, 2021*, pages 4732–4740. AAAI Press.
- <span id="page-11-7"></span>Zhaocheng Zhu, Zuobai Zhang, Louis-Pascal A. C. Xhonneux, and Jian Tang. 2021b. [Neural bellman](https://proceedings.neurips.cc/paper/2021/hash/f6a673f09493afcd8b129a0bcf1cd5bc-Abstract.html)[ford networks: A general graph neural network](https://proceedings.neurips.cc/paper/2021/hash/f6a673f09493afcd8b129a0bcf1cd5bc-Abstract.html) [framework for link prediction.](https://proceedings.neurips.cc/paper/2021/hash/f6a673f09493afcd8b129a0bcf1cd5bc-Abstract.html) In *Advances in Neural Information Processing Systems 34: Annual Conference on Neural Information Processing Systems 2021, NeurIPS 2021, December 6-14, 2021, virtual*, pages 29476–29490.

### <span id="page-12-0"></span>A Bellman-Ford Shortest Path Algorithm

<span id="page-12-3"></span>Algorithm 2 The Bellman-Ford Shortest Path Algorithm

Input: A graph G with n nodes, the edge set E, the source node s

Output: The distance from node s to any node in the graph

```
1: d
(0) ← [+∞, +∞, ..., +∞]
2: d
(0)[s] ← 0
3: for i = 1 to n − 1 do
4: d
(i) ← d
(i−1)
5: for each edge (u, v) ∈ E do
6: d
(i)
[v] ← min n
d
(i)
[v], d(i−1)[u] + w(u, v)
7: end for
8: end for
9: return d
(n−1)
```

o

The Bellman-Ford shortest path algorithm [\(Ford,](#page-8-2) [1956;](#page-8-2) [Bellman,](#page-8-3) [1958;](#page-8-3) [Baras and Theodorakopou](#page-8-4)[los,](#page-8-4) [2010\)](#page-8-4), founded by Richard Bellman and Lester Ford, is an efficient algorithm for searching the shortest path from the starting point to each node in a graph. The details are shown in Algorithm [2.](#page-12-3) And the basic idea is: For a graph with n nodes, the shortest path between two nodes in the graph can contain at most n−1 edges. Then, we can perform n − 1 times of relaxation operations recursively on the graph to obtain the shortest path from the source node to all nodes in the graph.

## <span id="page-12-1"></span>B An Illustration of Temporal Paths and Temporal Links

<span id="page-12-4"></span>![](_page_12_Figure_7.jpeg)
<!-- Image Description: The image is a directed graph showing a network of six nodes (e1-e6) representing events. Each directed edge connects two nodes, labeled with an ordered pair (rᵢ, tᵢ), likely representing reward (rᵢ) and time cost (tᵢ) associated with the transition. The graph illustrates a process or workflow where transitions between events have associated costs and rewards. Its purpose is to visually represent the structure of a system described by the paper, possibly to explain algorithms or models for optimizing paths or resource allocation within that system. -->

**Figure 4:** An illustration of temporal paths and temporal links.

Fig. [4](#page-12-4) illustrates some temporal paths and temporal links. For example, <sup>t</sup><sup>1</sup> r1 (e1, e2) is a temporal link pointing from e<sup>1</sup> to e2, while <sup>t</sup><sup>2</sup> r2 (e1, e3) ∧ t5 r5 (e3, e4) ∧ t7 r7 (e4, e6) and

t1 r1 (e1, e2) ∧ t3 r3 (e2, e5) ∧ t6 r6 (e5, e6) are two distinct temporal paths from e<sup>1</sup> to e6.

### <span id="page-12-2"></span>C Benchmark Datasets

### C.1 Interpolation datasets

To evaluate our proposed TKG Reasoning method, we perform link prediction task on four widely-used interpolation datasets, namely ICEWS14, ICEWS05-15 [\(García-Durán et al.,](#page-8-8) [2018\)](#page-8-8), YAGO11k [\(Dasgupta et al.,](#page-8-7) [2018\)](#page-8-7) and WIKIDATA12k [\(Dasgupta et al.,](#page-8-7) [2018\)](#page-8-7).[8](#page-12-5) The left half of Table [4](#page-13-2) summarizes the details of the four interpolation datasets that we use.

ICEWS [\(Lautenschlager et al.,](#page-9-16) [2015\)](#page-9-16) is a repository containing political events with a specific timestamp. ICEWS14 and ICEWS05-15 [\(García-](#page-8-8)[Durán et al.,](#page-8-8) [2018\)](#page-8-8) are two subsets of ICEWS corresponding to facts from 1/1/2014 to 12/31/2014 and from 1/1/2005 to 12/31/2015. YAGO11k and WIKIDATA12k [\(Dasgupta et al.,](#page-8-7) [2018\)](#page-8-7) are subsets of YAGO3 [\(Mahdisoltani et al.,](#page-10-17) [2015\)](#page-10-17) and WIKI [\(Erxleben et al.,](#page-8-13) [2014\)](#page-8-13), where time annotations are represented as time intervals. We derive the two datasets from HyTE [\(Dasgupta et al.,](#page-8-7) [2018\)](#page-8-7) to obtain the same year-level granularity by dropping the month and date information. And the characteristic of a dataset used for the interpolation is disorderly arrangement, which means that it is random and not sorted according to time.

### C.2 Extrapolation datasets

The right half of Table [4](#page-13-2) summarizes the details of the four extrapolation datasets that we use, namely ICEWS14 [\(García-Durán et al.,](#page-8-8) [2018\)](#page-8-8), ICEWS18 [\(Jin et al.,](#page-9-1) [2020\)](#page-9-1), YAGO [\(Mahdisoltani et al.,](#page-10-17) [2015\)](#page-10-17) and WIKI [\(Leblay and Chekol,](#page-9-3) [2018\)](#page-9-3).[9](#page-12-6) ICEWS14 [\(García-Durán et al.,](#page-8-8) [2018\)](#page-8-8) and ICEWS18 [\(Jin](#page-9-1) [et al.,](#page-9-1) [2020\)](#page-9-1) are two subsets of ICEWS [\(Laut](#page-9-16)[enschlager et al.,](#page-9-16) [2015\)](#page-9-16) corresponding to facts from 1/1/2014 to 12/31/2014 and from 1/1/2018 to 10/31/2018. We drop the month and date information of YAGO and WIKI here for ease of processing and to obtain the same year-level granularity as [\(Jin et al.,](#page-9-1) [2020\)](#page-9-1). Compared to the interpolation datasets (see the left half of Table [4\)](#page-13-2), the facts in the four datasets for extrapolation are arranged in ascending order according to time. For the purpose

<span id="page-12-5"></span><sup>8</sup>All of the four interpolation datasets can be downloaded from <https://github.com/soledad921/ATISE>.

<span id="page-12-6"></span><sup>9</sup>All of the four extrapolation datasets can be downloaded from [https://github.com/Lee-zix/RE-GCN]( https://github.com/Lee-zix/RE-GCN).


| | | | Interpolation | Extrapolation | | | | | |
|------------------|----------|---------|---------------|---------------|----------|----------|---------|---------|--|
| Dataset | ICEWS14 | YAGO11k | ICEWS05-15 | Wikidata12k | ICEWS14 | ICEWS18 | YAGO | WIKI | |
| Entities | 7,128 | 10,623 | 10488 | 12554 | 6,869 | 23,033 | 10,623 | 12,554 | |
| Relations | 230 | 10 | 251 | 24 | 230 | 256 | 10 | 24 | |
| Train | 72,826 | 16,408 | 386,962 | 32,497 | 74,845 | 373,018 | 161,540 | 539,286 | |
| Validation | 8,941 | 2,050 | 46,275 | 4,062 | 8,514 | 45,995 | 19,523 | 67,538 | |
| Test | 8,963 | 2,051 | 46,092 | 4,062 | 7,371 | 49,545 | 20,026 | 63,110 | |
| Time granularity | 24 hours | 1 year | 24 hours | 1 year | 24 hours | 24 hours | 1 year | 1 year | |

**Table 4:** Statistics of our experimented datasets for both interpolation setting and extrapolation setting.

of extrapolation, we follow [Han et al.](#page-9-9) [\(2021a\)](#page-9-9) and split each dataset into three subsets by time, ensuring (time of training set) < (time of validation set) < (time of test set). Thus, we can smoothly use past knowledge (facts in the training set) to predict the future.

Some recent works have shown that the timeunwise filtered setting [\(Bordes et al.,](#page-8-5) [2013\)](#page-8-5) may probably get incorrect higher ranking scores [\(Li](#page-9-2) [et al.,](#page-9-2) [2021\)](#page-9-2), and that the time-wise filtered setting [\(Xu et al.,](#page-10-10) [2019;](#page-10-10) [Goel et al.,](#page-8-12) [2020\)](#page-8-12) is more suitable for TKG Reasoning since it ensures the facts which do not appear at time t are still considered as candidates for evaluating the given test quadruple [\(Xu et al.,](#page-11-1) [2020\)](#page-11-1). Therefore, we use the time-wise filtered setting [\(Xu et al.,](#page-10-10) [2019;](#page-10-10) [Goel et al.,](#page-8-12) [2020\)](#page-8-12) to report the experimental results.

## <span id="page-13-0"></span>D Experimental Details for Interpolation Reasoning

### <span id="page-13-3"></span>D.1 Setup

In this setting, we split each dataset into three subsets: a training set Ttrain, a validation set Tvalid and a test set Ttest.

For training, we further split the training set Ttrain into two parts: the fact set Ftrain including 3/4 of the training quadruples used to extract temporal paths, and the query set Qtrain including the other 1/4 of the training quadruples used as queries. Thus, we can train our model by using temporal paths collected by Ftrain to answer queries in Qtrain.

For verification and testing, we accomplish reasoning by answering queries derived from the validation set and test set, where the whole training set Ttrain is prepared to extract and collect temporal paths. Since the entire training set is known to us and we do not use any data from validation or test set during the training process, we can ensure that there is no data leakage issue.

### D.2 Baselines

For interpolation TKG Reasoning baselines, we consider TTransE [\(Leblay and Chekol,](#page-9-3) [2018\)](#page-9-3), HyTE [\(Dasgupta et al.,](#page-8-7) [2018\)](#page-8-7), TA-DistMult [\(García-Durán et al.,](#page-8-8) [2018\)](#page-8-8), ATiSE [\(Xu et al.,](#page-10-10) [2019\)](#page-10-10), and TeRo [\(Xu et al.,](#page-11-1) [2020\)](#page-11-1), TComplEx [\(Lacroix et al.,](#page-9-0) [2020\)](#page-9-0), T-GAP [\(Jung et al.,](#page-9-5) [2021\)](#page-9-5), TELM [\(Xu et al.,](#page-10-1) [2021\)](#page-10-1), RotateQVS [\(Chen et al.,](#page-8-1) [2022\)](#page-8-1) and TGeomE++ [\(Xu et al.,](#page-11-8) [2023\)](#page-11-8).

### <span id="page-13-4"></span>D.3 Hyperparameter

To seek and find proper hyperparameters, we utilize a grid search empirically over the following ranges for all four datasets: embedding dimension d in {32, 64, 128}, learning rate in [10−<sup>5</sup> , 10−<sup>3</sup> ], dimension for attention d<sup>a</sup> in [3, 4, 5], dropout in [0.1, 0.2, 0.3], batch size in [5, 10, 20, 50], the maximum length of temporal paths L in [3, 4, 5], activation function δ in [identity, tanh, ReLU], and the optimizer we use is Adam.

And we have found out the best hyperparameters combination as follows: for ICEWS14, we set learning rate as 0.0003, batch size as 10, and δ as identity; for ICEWS05-15, we set learning rate as 0.00005, batch size as 5, and δ as identity; for YAGO11k, we set learning rate as 0.00005, batch size as 20, and δ as ReLU; for WIKIDATA12k, we set learning rate as 0.00002, batch size as 20, and δ as ReLU; and for all of four datasets, we choose L as 5, d<sup>a</sup> as 5, dropout as 0.2, and d as 128.

## <span id="page-13-1"></span>E Experimental Details for Extrapolation Reasoning

### E.1 Setup

In this setting, first of all, we need to arrange each dataset in ascending order according to time. In addition to the same splitting operation as in Section [D.1,](#page-13-3) we need to ensure: (time of training set) < (time of validation set) < (time of test set). Since some entities and relations in the validation or test set may not have appeared in the training set, our

extrapolation setting can actually be seen as an inductive inference [\(Sun et al.,](#page-10-2) [2021\)](#page-10-2).

We use the ground truths for our extrapolation TKG Reasoning, as is the case with many previous methods [\(Jin et al.,](#page-9-1) [2020;](#page-9-1) [Li et al.,](#page-9-2) [2021;](#page-9-2) [Sun et al.,](#page-10-2) [2021\)](#page-10-2). Specifically, for all of the training, validation and testing, we predict future events assuming ground truths of the preceding events are given at inference time [\(Han et al.,](#page-9-9) [2021a\)](#page-9-9).

### E.2 Baselines

For extrapolation TKG Reasoning baselines, we consider RE-NET [\(Jin et al.,](#page-9-1) [2020\)](#page-9-1), CyGNeT [\(Zhu](#page-11-4) [et al.,](#page-11-4) [2021a\)](#page-11-4), TANGO [\(Han et al.,](#page-9-6) [2021b\)](#page-9-6), xERTE [\(Han et al.,](#page-9-9) [2021a\)](#page-9-9), RE-GCN [\(Li et al.,](#page-9-2) [2021\)](#page-9-2), TITer [\(Sun et al.,](#page-10-2) [2021\)](#page-10-2), CEN [\(Li et al.,](#page-9-7) [2022b\)](#page-9-7), TLogic [\(Liu et al.,](#page-10-3) [2022\)](#page-10-3), TIRGN [\(Li et al.,](#page-9-8) [2022a\)](#page-9-8) and RPC [\(Liang et al.,](#page-9-10) [2023\)](#page-9-10).

### E.3 Hyperparameter

A grid search has been taken empirically for the extrapolation TKG Reasoning on the same hyperparameter ranges as in Section [D.3.](#page-13-4) And we have found out the best hyperparameters combination as follows: for ICEWS14, we set learning rate as 0.0003, batch size as 10, d as 128, and δ as identity; for ICEWS18, we set learning rate as 0.00005, batch size as 5, d as 64, and δ as ReLU; for YAGO, we set learning rate as 0.00003, batch size as 10, d as 64, and δ as identity; for WIKI, we set learning rate as 0.00003, batch size as 5, d as 64, and δ as identity; and for all of four datasets, we choose L as 5, d<sup>a</sup> as 5, and dropout as 0.2.

### <span id="page-14-0"></span>F Details of the Pipeline Setting

To conduct our experimental pipeline, we sample a certain ratio (60% for Setting A, 70% for Setting B, and 80% for Setting C) of facts to train interpolation, while the other unsampled facts serve to provide incomplete quadruples (with either the subject entity or object entity masked) to be completed. The completed quadruples are then treated as new knowledge. Finally, the newly acquired knowledge from interpolation could be combined with the interpolation training set, ordered chronologically, and used as the training set for downstream (extrapolation) tasks, with the test set of the standard extrapolation dataset used to evaluate experimental results.

The process of the proposed pipeline can be seen in Table [6.](#page-15-1)


| Ratio | Inter- | Extra- | | | | MRR Hits@1 Hits@3 Hits@10 |
|-------|---------------------------|-------------|-------|-------|-------|---------------------------|
| 60% | - | TLogic | 41.85 | 32.51 | 47.05 | 59.58 |
| 60% | TELM | TLogic | 40.88 | 31.66 | 45.86 | 58.69 |
| 60% | - | TIRGN 42.53 | | 32.04 | 48.10 | 62.16 |
| | 60% RotateQVS TIRGN 40.86 | | | 30.24 | 45.78 | 61.63 |
| 60% | - | TPAR | 43.86 | 33.81 | 49.04 | 62.83 |
| 60% | TPAR | TPAR | 44.56 | 34.68 | 49.68 | 63.32 |
| 70% | - | TLogic | 41.88 | 32.51 | 46.91 | 59.97 |
| 70% | TELM | TLogic | 44.55 | 32.29 | 46.55 | 59.53 |
| 70% | - | TIRGN 43.68 | | 33.23 | 48.99 | 63.59 |
| | 70% RotateQVS TIRGN 42.35 | | | 31.87 | 47.78 | 62.25 |
| 70% | - | TPAR | 45.49 | 35.69 | 50.33 | 64.30 |
| 70% | TPAR | TPAR | 46.07 | 35.92 | 51.06 | 65.02 |
| 80% | - | TLogic | 42.18 | 32.81 | 47.27 | 60.18 |
| 80% | TELM | TLogic | 42.09 | 32.69 | 47.31 | 59.78 |
| 80% | - | TIRGN 43.69 | | 32.97 | 49.10 | 64.28 |
| | 80% RotateQVS TIRGN 42.78 | | | 32.15 | 48.06 | 63.14 |
| 80% | - | TPAR | 46.36 | 36.42 | 51.34 | 65.45 |
| 80% | TPAR | TPAR | 46.66 | 36.68 | 51.82 | 65.54 |

**Table 5:** A detailed version of Table [3.](#page-6-5)

The detailed results of the pipeline setting can be found in Table [5,](#page-14-1) where a concise version has been shown in Table [3](#page-6-5) in Section [5.3.](#page-6-0)

### <span id="page-14-2"></span>G Analysis on Path Length

<span id="page-14-3"></span>![](_page_14_Figure_13.jpeg)
<!-- Image Description: This bar chart compares the Mean Reciprocal Rank (MRR) of three methods (xERTE, TLogic, TPAR) for different maximum lengths. The x-axis represents the maximum length, and the y-axis shows the MRR. The chart illustrates how the performance of each method varies with the maximum length parameter, allowing for a comparison of their relative effectiveness. -->

**Figure 5:** The MRR performance with different maximum path lengths for the extrapolation reasoning on the ICEWS14 test set.

Fig. [5](#page-14-3) displays the MRR performance with different maximum path lengths for the extrapolation reasoning on ICEWS14 test set. We compare our TPAR with the symbolic method TLogic [\(Liu et al.,](#page-10-3) [2022\)](#page-10-3), where the maximum length L means it contains all lengths not exceeding L (L = 1, 2, · · · 5).

As the maximum length L increases, a greater number of temporal links are covered and can provide more detailed information. However, this also makes it more challenging to learn and reason with this information. The results demonstrate that the performance of TLogic decreases for L values of 4 or higher. In contrast, when L is too small, such as L ≤ 2, our TPAR approach struggles to perform


| Step 1<br>(Interpolation) | Inputs: A ratio (denoted as r) of known facts sampled from G, denoted as rG.<br>Queries: The other unsampled facts (1 − r)G with either the subject or the<br>object entity masked.<br>Outputs: Newly acquired facts Gnew<br>by completing the queries. |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Step 2<br>(Extrapolation) | Inputs: The basic rG, and the newly acquired Gnew. |
| | Queries: The standard extrapolation test set. |
| | Outputs: Performance evaluation. |

**Table 6:** The process of the proposed pipeline.

well due to the limited amount of information encoded in these short temporal paths. An interesting discovery can be made: For symbolic TLogic, a balance needs to be struck between the richness of the information contained and the ability to effectively learn from it. However, our TPAR appears to alleviate this issue, as neural-symbolic reasoning is more tolerant of ambiguous and noisy data.


| Length | Hits@1 | Hits@3 | Hits@10 | MRR |
|--------|--------|--------|---------|-------|
| 1 | 10.03 | 10.45 | 10.58 | 10.32 |
| 2 | 10.39 | 11.06 | 11.45 | 10.84 |
| 3 | 15.13 | 22.03 | 32.16 | 21.03 |
| 4 | 15.59 | 22.56 | 33.15 | 21.62 |
| 5 | 17.35 | 25.14 | 37.42 | 24.12 |

**Table 7:** Performance of our proposed TPAR with different maximum path lengths for the interpolation reasoning on the YAGO11k test set.

We also take a similar study on the interpolation reasoning, and Table [7](#page-15-2) illustrates the performance of our proposed TPAR with different maximum path lengths for the interpolation reasoning on the YAGO11k test set. As the length increases, all metrics of our TPAR have significantly improved.

### <span id="page-15-0"></span>H Analysis on Chronological Order


| Model | | TLogic | | TPAR | | | | |
|---------------------|---------|--------|-------|-------|-------|--|--|--|
| Chronological Order | | # | ! | # | ! | | | |
| ICEWS14 | Hits@1 | 32.60 | 33.56 | 36.88 | 36.02 | | | |
| | Hits@3 | 47.06 | 48.27 | 52.28 | 51.49 | | | |
| | Hits@10 | 60.06 | 61.23 | 65.89 | 64.30 | | | |
| | MRR | 42.02 | 43.04 | 46.89 | 45.77 | | | |
| ICEWS18 | Hits@1 | 19.92 | 20.54 | 26.58 | 25.24 | | | |
| | Hits@3 | 33.04 | 33.95 | 39.27 | 38.55 | | | |
| | Hits@10 | 47.75 | 48.53 | 56.94 | 55.54 | | | |
| | MRR | 28.79 | 29.82 | 35.76 | 33.98 | | | |

**Table 8:** An analysis on chronological order for the extrapolation reasoning.

As discussed in Section [4.1,](#page-2-3) for extrapolation reasoning, our TPAR does not require strict chronological order between links in a path. Alternatively,

methods like TLogic [\(Liu et al.,](#page-10-3) [2022\)](#page-10-3) demand that all links in a path be ordered chronologically. For example, given a path P = t1 r1 (e1, e2)∧ t2 r2 (e2, e3)∧ t3 r3 (e3, e4), TLogic requires t<sup>q</sup> > t<sup>1</sup> ≥ t<sup>2</sup> ≥ t3, while we simply require t<sup>q</sup> > t<sup>i</sup> for i = 1, 2, 3. We conduct an analysis on the chronological order of links in a path, and the results are shown in Table [8.](#page-15-3) The results indicate that when chronological order is relaxed, the performance of TLogic decreases, while that of our TPAR increases. We believe that by relaxing chronological order in paths, we can gather more paths, thereby providing more information for inference. Nonetheless, this may introduce noise and uncertainty into the process, which ultimately reduces the effectiveness of symbolic methods such as TLogic. On the other hand, our TPAR employs a neural-symbolic approach, which not only mitigates the impact of these challenges but also ensures excellent inference performance, showcasing its strong robustness.

## TL;DR
Novel unified approach to temporal knowledge graph reasoning that handles both interpolation (historical analysis) and extrapolation (future prediction) through neural-driven symbolic reasoning with enhanced robustness and interpretability.

## Key Insights
Proposes Temporal PAth-based Reasoning (TPAR) model that performs neural-driven symbolic reasoning robust to ambiguous and noisy temporal data while providing fine interpretability, outperforming SOTA methods in link prediction for both interpolation and extrapolation settings.

## Metadata Summary
### Research Context
- **Research Question**: How can we develop a unified reasoning model that effectively handles both interpolation and extrapolation in temporal knowledge graphs while maintaining robustness to noisy data and providing interpretable results?
- **Methodology**: Developed Temporal PAth-based Reasoning (TPAR) model using neural-driven symbolic reasoning approach, designed for robustness to ambiguous and noisy temporal data, implemented pipeline experimental setting for unified evaluation, comprehensive experiments on link prediction tasks.
- **Key Findings**: TPAR outperformed state-of-the-art methods in link prediction tasks for both interpolation and extrapolation settings, demonstrated effective integration of temporal reasoning capabilities, showed robustness to noisy temporal data with enhanced interpretability.

### Analysis
- **Limitations**: Previous methods de-emphasized temporal correlations, existing approaches ignored inferring clues from missing past facts, limited handling of temporal data complexity in unified frameworks.
- **Future Work**: Further refinement of TPAR model capabilities, exploration of more diverse temporal reasoning scenarios, integration with real-world temporal knowledge systems.