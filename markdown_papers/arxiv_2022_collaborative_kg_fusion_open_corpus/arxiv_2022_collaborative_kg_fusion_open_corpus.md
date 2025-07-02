<!-- cite_key: wang2022 -->

# Collaborative Knowledge Graph Fusion by Exploiting the Open Corpus

Yue Wang<sup>1</sup> , Yao Wan<sup>2</sup> , Lu Bai<sup>3</sup> , Lixin Cui<sup>1</sup> , Zhuo Xu<sup>1</sup> , Ming Li<sup>4</sup> Philip S. Yu<sup>5</sup> , *Fellow, IEEE*and Edwin R Hancock<sup>6</sup> ,*Fellow, IEEE*

**Abstract**—To alleviate the challenges of building Knowledge Graphs (KG) from scratch, a more general task is to enrich a KG using triples from an open corpus, where the obtained triples contain noisy entities and relations. It is challenging to enrich a KG with newly harvested triples while maintaining the quality of the knowledge representation. This paper proposes a system to refine a KG using information harvested from an additional corpus. To this end, we formulate our task as two coupled sub-tasks, namely join event extraction (JEE) and knowledge graph fusion (KGF). We then propose a Collaborative Knowledge Graph Fusion Framework to allow our sub-tasks to mutually assist one another in an alternating manner. More concretely, the explorer carries out the JEE supervised by both the ground-truth annotation and an existing KG provided by the supervisor. The supervisor then evaluates the triples extracted by the explorer and enriches the KG with those that are highly ranked. To implement this evaluation, we further propose a Translated Relation Alignment Scoring Mechanism to align and translate the extracted triples to the prior KG. Experiments verify that this collaboration can both improve the performance of the JEE and the KGF.

**Index Terms**—Knowledge Graph Enrichment, Joint Event Extraction, Knowledge Graph Fusion, Collaborative Learning, Contrastive Learning

✦

## 1 INTRODUCTION

K NOWLEDGE graphs, which are a structurally organized form of information, have supported a variety of downstream tasks, including recommender systems [\[1\]](#page-11-0), NLP tasks [\[2\]](#page-11-1), question answering [\[3\]](#page-11-2), [\[4\]](#page-11-3), and entitylinking [\[5\]](#page-11-4). Existing open source knowledge graphs such as Wikidata [\[6\]](#page-11-5), WordNet [\[7\]](#page-11-6) and Freebase [\[8\]](#page-11-7) contain billions of Resource Description Framework (RDF) triples [\[9\]](#page-11-8) in the form of *(subject, relation, object)*relations, where both the*subject*and*object*represent the named entities [\[10\]](#page-11-9), and the*relation*models the relationship between these two named entities. However, since open source knowledge graphs are designed for general purposes, they contain only limited factuaL knowledge for particular tasks [\[11\]](#page-11-10) in restricted domais such as finance or medicine. To adapt to multiple domains, it is crucial to construct high-quality domain specific knowledge graphs.

In order to construct new knowledge graphs from unstructured textual sources, existing work mainly consists of several pipelined sub-tasks, e.g., named entity recognition [\[12\]](#page-11-11), relation extraction [\[13\]](#page-11-12) or relation alignment [\[14\]](#page-11-13). These methods are designed as separate subtasks and not as a unified system [\[15\]](#page-11-14). Thus they do not fully address the issue of how to effectively leverage the information hidden in the connections between the subtasks [\[16\]](#page-11-15) to improve the quality of a knowledge graph built from a text corpus. To this end, recent work has combined named entity recognition with relation extraction as a single jointevent-extraction [\[17\]](#page-11-16) task that can jointly obtain the entities and relations from text sources. However, since the current work does not focus on the resulting process to build an integrated knowledge graph from the extracted results, there still exists much scope for constructing a high-quality domain-oriented knowledge graph from test documents.

Knowledge graph fusion [\[15\]](#page-11-14), [\[18\]](#page-11-17), [\[19\]](#page-11-18) is a possible route by which to construct a knowledge graph from the extracted event factors in an open corpus. Early work applied the traditional data fusion method [\[20\]](#page-11-19) while considering only fusing the data under a global or compatible data schema [\[21\]](#page-11-20). This work evaluates the quality of data by checking whether or not a triple is contained in the extended set of a ground-truth knowledge graph [\[22\]](#page-11-21). However, this type of method may ignore the implications of knowledge that is indirectly contained in the ground-truth knowledge graph. It may thus discard many meaningful triples from different and potentially valuable sources. In order to overcome this problem, recent knowledge graph embedding [\[23\]](#page-11-22) methods have leveraged network embedding technology [\[24\]](#page-11-23) to infer the possibilities of the existence of triples in a given knowledge graph. This is done by representing the triples as latent vectors [\[25\]](#page-11-24), [\[26\]](#page-11-25), [\[27\]](#page-12-0). Specifically, with the representation vectors of the triples to hand, these methods use statistical models [\[28\]](#page-12-1) or neural networks [\[29\]](#page-12-2), [\[30\]](#page-12-3) to predict plausible scores for the potential triples.

Although much existing work discusses the potential triple evaluation problem for the knowledge graph fusion task, little considers generating the candidate triples from
*Yue Wang, Lu Bai (*∗*Corresponding Author: bailucs@cufe.edu.cn), Lixin Cui, and Zhuo Xu are with* <sup>1</sup>*Central University of Finance and Economics, Beijing, China. Yao Wan is with* <sup>2</sup>*College of Computer Science and Technology at Huazhong University of Science and Technology (HUST), Wuhan, China. Lu Bai is with* <sup>3</sup>*School of Artificial Intelligence, Beijing Normal University, Beijing, China. Ming Li is with*<sup>4</sup>*the Key Laboratory of Intelligent Education Technology and Application of Zhejiang Province, Zhejiang Normal University, Jinhua, China. Philip S. Yu is with* <sup>5</sup>*Department of Computer Science, University of Illinois at Chicago, US. Edwin R. Hancock is with* <sup>6</sup>*Department of Computer Science, University of York, UK. This work is supported by the National Natural Science Foundation of China under Grants T2122020, 61976235, and 61602535. This work is also supported in part by NSF under grants III-1526499, III-1763325, III-1909323, and CNS-1930941.*![](_page_1_Figure_1.jpeg)

<span id="page-1-0"></span>Fig. 1. In a collaborative knowledge graph fusion process, an explorer and a supervisor collaborate to create an enriched knowledge graph by extending a prior knowledge graph with RDF triples extracted from open text sources. Since the extracted RDF triples contain entities or relations that are not aligned to the prior knowledge graph, this process requires interaction mechanisms (translate the extracted results to the knowledge graph RDF triples and guide the explorer with meaningful entity pairs) between the explorer and the supervisor. To simplify the problem, we suppose both the explorer and supervisor share the same entity types (Geographical/Social/Political Entities (GPE), Persons (PER), Weapons (WEA), Organizations (ORG), Vehicles (VEH), etc.) and the extracted trigger mentions (killed, rained down, etc.) by the explorer belong to the trigger types (Life, Conflict, etc.) by following the definitions in the ACE 2005 corpus [\[31\]](#page-12-4). Then the core problem becomes to align the trigger mentions obtained by the explorer to the relations in the knowledge graph of the supervisor.

open text sources and linking candidate generation with the evaluation process to automatically. fuse the obtained triples to a prior knowledge graph. The main challenges that hinder progress in this direction are routed in the following shortcomings in the knowledge extraction and a knowledge graph fusion tasks. (1)*Difficulties in aligning RDF triples*. Since open text sources may contain relations outside the scope of a prior knowledge graph, it is a challenge to align the relations from the open texts to those in the knowledge graph. Although current work discusses the entity alignment [\[32\]](#page-12-5) between sources, little focusses on relation alignment. This leads to the difficulty of aligning the extracted RDF triples from the text sources to a prior knowledge graph. (2) *Difficulties maintaining knowledge graph quality*. Merging the unaligned RDF triples from the open text sources to a knowledge graph can mislead the knowledge graph embedding model and may result in unreliable plausible scores for potential triples. Moreover, a misleading knowledge graph can result in the the extractor relying on low-quality triples. This may further lower the quality of the knowledge graph. (3) *Difficulties sharing knowledge between sub-tasks.*Without a reliable way of aligning the RDF triples, it becomes difficult to share knowledge between the subtasks (e.g. event extraction and knowledge fusion). This leads to error propagation [\[33\]](#page-12-6) between sub-tasks and thus degrade the performance for each sub-task.

To address the aforementioned limitations, in this paper, we formulate a new method that combines event extraction (extractor) with knowledge graph fusion as a Collaborative Knowledge Graph Fusion process. Specifically, we propose a unified framework to build a domain-oriented knowledge graph by enriching an open-source knowledge graph with knowledge extracted automatically from a text corpus. Since our new method provides a mechanism to share the knowledge between sub-tasks, our enriched knowledge graph grows larger by incorporating facts of knowledge from the texts. In addition, the new method also leverages the enriched knowledge graph to assist our event extraction sub-task to obtain more reliable entities and relations from documents.

As illustrated in Figure [1,](#page-1-0) the collaborative knowledge graph fusion method consists of two interacting processes, an explorer and a supervisor. That is, by referring to the principles (e.g. the possible entity pairs) from a supervisor, an extractor explores new RDF triples from the available open text sources. After the extractor submits the newly discovered triples to the supervisor, the supervisor evaluates their quality and extends the existing set of triples using the highest quality newly discovered triples.

Specifically, our framework guides the extractor with the entity pairs from a prior seed knowledge graph, and then iteratively increments the seed knowledge graph with the extracted triples from the extractor. In this process, both the performance of the extractor and the quality of the enriched knowledge graph are improved. To this end, in our extractor, we propose a benchmark-based supervision mechanism to supervise the extraction process with the entity pairs from the seed knowledge graph maintained by the supervisor. This is implemented by a contrastive learning method which considers both the positive and negative entity pairs. These entity pairs are sampled from the prior knowledge graph with a neural Knowledge Graph Embedding (KGE) scoring function trained by the supervisor process. On the other hand, to the supervisor, the KGE scoring function is trained by the triples in the seed or the enriched knowledge graph and it evaluates the matching degree of the extracted RDF triples from the extractor to the knowledge of the supervisor. Consequently, the supervisor merges the high-ranked triples from the extracted results into the prior knowledge graph.

We conduct exhaustive experiments on real-world corpora and knowledge graphs. Experimental results show that our system achieves higher performance than state-ofthe-art baselines, both on the joint-event-extraction and the knowledge-graph-embedding tasks. This verifies not only that the proposed benchmark-based supervision mechanism guides the extractor well in our system, and but that it also implies that the knowledge graph of the supervisor maintains a high quality by being enriched with the triples evaluated by the supervisor.

In summary, our main contributions are as follows:

- We formalize the knowledge graph fusion with open corpora as an alternating process consisting of extracting the RDF triples from documents and then fusing a prior knowledge graph with the obtained triples. As far as we know, our work is the first to discuss a unified architecture to conduct the knowledge fusion directly based on the text sources.
- We propose the "Collaborative Knowledge Graph Fusion" framework as a solution for the aforementioned problem. In this framework, we propose the Benchmark-based Supervision Mechanism to further supervise the performance of our JEE process (in the explorer process) with positive and negative entity pairs sampled from a prior KG provided by the supervisor.
- We propose an unsupervised metric, Translated Relation Alignment Scoring (TRAS), to assist align and translate the extracted triples from the JEE process to those in the proper form to the prior KG.
- With the proposed Benchmark-based Supervision Mechanism and TRAS to hand, we implement the "Collaborative Knowledge Graph Fusion" as a unified process. It automatically extracts the triples from an open corpus and enriches them to a given prior KG in an alternative process.
- Our experiments on several real-world datasets show that, with the proposed framework, our system achieves better performance both on the JEE and KGF tasks than the related alternatives. This verifies that our method not only improves the JEE process but also yields a high-quality enriched KG. Specifically, our case study shows that our system could translate the extracted triples from a text corpus to the facts consistent with a prior KG with the assistance of the proposed TRAS score. This improves the quality of the prior KG and also explains the reason for the performance improvement of the KGF task.

The remainder of this paper is organized as follows. In Section [2,](#page-2-0) we introduce the preliminaries concerning the joint event extraction and knowledge graph fusion processes and then also formalize the problem of knowledge graph fusion with an open corpus. Section [3](#page-3-0) presents in detail our proposed framework and fusion mechanism. Section [4](#page-6-0) verifies the effectiveness of our model and compares it with recent methods on real-world datasets. Section [5](#page-10-0) summarizes recent related work. Finally, we conclude this paper in Section [6](#page-11-26) where we offer suggestions for further work in this direction.

## <span id="page-2-0"></span>2 PRELIMINARIES

Our overall objective is knowledge graph fusion with an open corpus. This task consists of a joint event extraction (JEE) step to extract knowledge triples from unstructured texts and a knowledge graph fusion (KGF) step to evaluate and enrich the extracted triples from the JEE step for a prior or exsiting Knowledge Graph (KG). We elaborate the notation for the JEE and KG, and formalize our problem in the following subsections.

### 2.1 Knowledge Graphs

A Knowledge Graph (KG) [\[34\]](#page-12-7) is represented as a set of factual (RDF) triples referring to specific topics. Formally, we define a knowledge graph G in the structure G = hE, R, Ti, where E is a set of entities, R is a set of relations and T is the set of the RDF triples. For example, G<sup>1</sup> = hE1, R1, T1i is a knowledge graph of capital city relationships with the entity set E<sup>1</sup> = {T okyo, Beijing, Japan, China}, the relation set R<sup>1</sup> = {capital of} and the triple set T<sup>1</sup> = {hT okyo, capital of, Japani,hBeijing, capital of, Chinai}. Since a human-composed document does not contain such structural information such as the entities, relationships or triples, to build a KG from a corpus, we require to extract the triples from the texts.

### 2.2 Joint Event Extraction

Event extraction is a technique to extract the structural information such as entities or relations [\[12\]](#page-11-11) from a given corpus. This requires applying sub-tasks such as Named Entity Recognition (NER) and Relation Extraction (RE). Traditional methods train separate multi-label classifiers to distinguish the labels for the tokens (both for the entity and text relation mentions) in sentences. In order to improve the accuracy of the extraction process, recent work leverages the pipelined method to classify the relationship first and then identify the entities with roles centered around the determined relation. However, since these methods invoke their sub-processes separately, they feedback weakly from the entity identification task to the preceding tasks. As a result they may suffer from limitations caused by errorpropagation [\[35\]](#page-12-8).

To this end, we use a universal sequence-to-sequence (Seq2Seq) framework [\[16\]](#page-11-15) to simultaneously extract the entities and relations from a text corpus.
**Seq2Seq Joint-Event-Extraction (JEE).**Let the text corpus D be a set of sentences, where D = {s1, s2, s3, . . .} (∀s ∈ D, s = {w1, w2, w3, . . . , wm}, where wis are tokens). Let A = A<sup>E</sup> S A<sup>R</sup> be a combined tag set with predefined types for tokens, where A<sup>E</sup> and A<sup>R</sup> are the sets of the predefined entity and text relation mention types respectively. Then the aim of JEE is to find an optimal map Y<sup>Θ</sup><sup>1</sup> : s → Π<sup>M</sup> <sup>i</sup>=0A, (∀s ∈ D), where Π is the Cartesian product, M is the maximum length for the sentences in D, Θ<sup>1</sup> is the vector for the learned parameters.

In this form, our JEE process transforms a sentence into a tag sequence with the tags in the combined tag set A. The loss function for the Seq2Seq JEE is computed as a crossentropy function, as follows:

<span id="page-3-1"></span>
$$
\mathcal{L}_{jee} = \sum_{i=0}^{M} \sum_{y_i \in \mathcal{A}} -Pr(y_i|w_i) \log \hat{Pr}(y_i|w_i).
$$
 (1)

With the mapped tag sequence optimized by the loss function in Equation [1,](#page-3-1) we obtain the annotated tag sequences for the sentences in a corpus. In this manner, the entity and relation mentions for a sentence are extracted together. Consequently, we generate RDF triples based on their extracted mentions and use these triples as the candidate triples for KG enrichment. In order to simplify the discussion, we use the term Y<sup>Θ</sup><sup>1</sup> as a joint operation that combines both the mapping from sentences to label sequences and the RDF generation process. Therefore, YΘ<sup>1</sup> (D) refers to a set of RDF triples and we refer to it as the*extractor map*in the following sections.

#### <span id="page-3-3"></span>2.3 Knowledge Graph Fusion with an Open Corpus

Knowledge Graph Fusion [\[18\]](#page-11-17) is the task of constructing a unified knowledge graph from different data sources. Traditional knowledge graph fusion aims to integrate several knowledge graphs into one knowledge graph, and we formalize this task as follows:
**Knowledge Graph Fusion (KGF).** Given two prior knowledge graphs G<sup>1</sup> = hE1, R1, T1i and G<sup>2</sup> = hE2, R2, T2i, suppose both G<sup>1</sup> and G<sup>2</sup> are used under the same RDF schema to build a new knowledge graph G<sup>0</sup> = hE<sup>0</sup> , R<sup>0</sup> , T<sup>0</sup> i, where T <sup>0</sup> = T<sup>1</sup> S ∆T and ∆T is the set of triples of G<sup>2</sup> with the top-K plausible scores fG<sup>1</sup> (i, r, t) (∀(i, r, t) ∈ G2). This score is computed as

$$
f_{G_1}(i,r,t) = \sum_{(i^*,r^*,t^*) \in T_1} Sim((i,r,t),(i^*,r^*,t^*)), \quad (2)
$$

where the function Sim gives the similarity between two triples. The plausibility score of a triple evaluates the consistency of this triple with an existing or prior knowledge graph. Since it is inefficient to compute the plausibility score by traversing all the triples of a knowledge graph, mainstream work applies the Knowledge Graph Embedding (KGE) [\[23\]](#page-11-22) method for this evaluation. Specifically, these methods generate the vector representations for triples and compute the similarities between triples through their vector similarities. Recent methods represent the knowledge triple as latent vectors by following the ideas introduced in the translation based embedding model (TransE) [\[28\]](#page-12-1).

**Knowledge Graph Embedding (KGE).**Given a KB G = hE, R, Ti, suppose (i, r, j) is a triple from T, then the loss is

<span id="page-3-2"></span>
$$
\mathcal{L}_{kge} = -\sum_{\substack{(i,r,j) \in T, \\ (i',r,j') \in N}} ||\gamma + f_G(i,r,j)) - f_G(i',r,j')|| \quad (3)
$$

where N is the corresponding negative set for the triples in T, γ is a hyperparameter, fG(i, r, j) is a scoring function

to evaluate the consistency of any triple (i, r, j) to the knowledge graph G and the normalization in Equation [3](#page-3-2) can be based on either the L1 or L2-norm. According to the design of TransE, a plausibility score fG(i, r, j) can be computed as the following.

$$
f_G(i, r, j) = d(e_i + e_r, e_j),
$$
\n(4)

where e is an embedding that maps any entity or relation to an R <sup>h</sup> vector and d(∗, ∗) is the Euclidean distance function between two R <sup>h</sup> vectors.

Therefore, with a trained embedding e based on the given prior knowledge graph G1, the plausibility of a triple (i, r, j) from G<sup>2</sup> to G<sup>1</sup> can be evaluated by computing the Euclidean distance d(e<sup>i</sup> + er, e<sup>j</sup> ).

As discussed in the Introduction, our objective is to build a knowledge graph fusion system using open text sources. This task is different from the aforementioned knowledge graph fusion and it means we require to: (1) extract the RDF triples from a given corpus D and (2) fuse the extracted triples to a knowledge graph G. Specifically, we formalize this problem as the following.
**Open Knowledge Graph Fusion (OKGF).**Given a prior knowledge graph G = hE, R, Ti, a corpus D and an extractor map YΘ<sup>1</sup> , suppose YΘ<sup>1</sup> (D) is a set of extracted triples from a corpus D. Then with a trainable scoring function f(∗) and embedding map e, the objective of OKGF is to find the optimal subset ∆T from YΘ<sup>1</sup> (D) that minimizes the following loss function:

$$
\mathcal{L}_{OKGF} = -\sum_{\substack{(i,r,j) \in T \cup \Delta T, \\ (i',r,j') \in N}} ||\gamma + f_G(i,r,j)) - f_G(i',r,j')||, \tag{5}
$$

where N is the corresponding negative triple set for the positive triples t from T.

This task links the JEE and the KGF processes together. However, it is a combinatorial optimization problem that exhaustively checks all the possible subsets ∆T from YΘ<sup>1</sup> (D). The newly discovered noisy entities and relations from the open corpus exacerbate the problem. Therefore, it is difficult to obtain the global optimal solution. To this end, we propose a heuristic collaborative knowledge graph fusion framework to connect the JEE and KGF subtasks to fuse an open corpus to obtain a prior knowledge graph. Our framework approaches open knowledge graph fusion from two directions, namely 1) our model guides the JEE process with a prior knowledge graph and 2) it selectively enriches the prior knowledge graph with the extracted results from the JEE process. This requires a careful design of both the JEE supervision mechanism with a prior knowledge graph and an effective "translation-and-evaluation" method to fuse the extracted results into the prior knowledge graph. We elaborate the details in the next section.

## <span id="page-3-0"></span>3 OUR PROPOSED METHOD

In this section, we introduce the Collaborative Knowledge Graph Fusion framework to address knowledge graph fusion with an open corpus.

### 3.1 Overview

To emulate a human-like collaborative process for our task, we propose a system with two processes, namely 1) an explorer process and 2) a supervisor process. In the explorer process, the system uses the proposed Benchmark-based Supervision Mechanism to assist the JEE task to extract the triples while guided by a supervisor (the benchmarks discovered by the supervisor from a prior KG). In the supervisor process, the system applies the proposed Relation Alignment-based Knowledge Graph Fusion module to selectively accept the extracted triples to be added to the prior KG. These two processes alternate to simultaneously extract knowledge triples and enrich a prior KG with highquality. Figure [2](#page-5-0) illustrates the architecture of our system. The details for the proposed processes are given in the following subsections.

#### <span id="page-4-5"></span>3.2 The Explorer: Benchmark-based Supervision JEE

In Figure [2,](#page-5-0) our explorer process implements the JEE task. To ensure the explorer is guided by the supervisor we introduce a Benchmark-based Supervision Layer. In this work, we apply the Seq2Seq JEE as the basic extraction process and use BERT [\[36\]](#page-12-9) as the sequence-to-sequence encoder. This JEE module can be substituted by any alternative JEE model if necessary.

Intuitively, during the exploratory period, an explorer receives examples from a supervisor and attempts to leverage the knowledge in these examples to facilitate better exploration. In our work, the explorer process extracts the triples from an open corpus based on a prior KG maintained by a supervisor. Since the open corpus may contain unaligned relations and extra entities that are not contained in the prior KG, it requires a relatively flexible method rather than strict supervision to guide the explorer. To this end, we introduce the Benchmark-based Supervision Mechanism.
**Benchmark-based Supervision Mechanism.**Given a prior KG, G = hE, R, Ti, let the benchmarks be a positive set of entity pairs P <sup>+</sup> and a negative set of entity pairs P <sup>−</sup>, where P <sup>+</sup> = {(i, j)|(i, ∗, j) ∈ T, ∀i, j ∈ E}, and P <sup>−</sup> = {(i, j)|(i, ∗, j) ∈/ T, ∀i, j ∈ E}. Then the Benchmarkbased Supervision Mechanism can be described as the task to minimize a loss function extended from the BPR loss [\[37\]](#page-12-10)

<span id="page-4-0"></span>
$$
\mathcal{L}_b = -\log\left(\delta(f(P^+) - f(P^-)\right),\tag{6}
$$

where δ is the Sigmoid function, f(P) is a function to compute the likelihood for any entity pair (i,j) (∀(i, j) ∈ P), and is given by

$$
f(P) = \text{ffnn}\left(\sum_{\forall i,j \in P} (e_i - e_j)\right),\tag{7}
$$

where e<sup>i</sup> is an R d embedding vector for any entity i (∀i ∈ E); "ffnn" is a fully connected neural network to map an R d embedding vector to an R 1 score.

Optimizing L<sup>b</sup> results in the training of a scoring function f(P) to measure the likelihood of any entity pair while maximizing the difference between the likelihood scores of the positive and negative entity pairs. This fits with the intuition that an explorer understands the knowledge in the examples from the supervisor.

Further, since an entity is a sequence of tokens with arbitrary lengths, we apply the weighted average method [\[38\]](#page-12-11) to represent an entity by its corresponding embedding vector. Formally, the embedding vector for an entity is computed as follows

<span id="page-4-2"></span>
$$
e_i = \sum_{\forall w \in i} e_w,\tag{8}
$$

where i is an entity in E and w is any token in the entity i. The embedding vector e<sup>w</sup> can be obtained by referring to the embedding dictionary table.

With the proposed Benchmark-based Supervision Mechanism, the loss function of our explorer process is a weighted sum of Equations [1](#page-3-1) and [6,](#page-4-0) i.e.

<span id="page-4-4"></span>
$$
\mathcal{L}_e = (1 - \alpha)\mathcal{L}_{jee} + \alpha \mathcal{L}_b,\tag{9}
$$

where α is the weight for the benchmark-based supervision.
**Candidate Triple Set.**With the aforementioned explorer process, our system simultaneously extracts the entity and relation mentions (or triggers). Then, we generate all RDF triples exhaustively based on the extracted mentions. The results are treated as the candidate triple set T 0 for subsequent processing steps.

#### <span id="page-4-6"></span>3.3 The Supervisor: Relation Alignment-based OKGF

Our supervisor process enriches the prior KG with the optimal subset of the candidate triples from the explorer process. This requires a scoring function to measure the plausibilities for triples trained by the prior KG. The process for a supervisor to evaluate the quality of the discovery is similar to that adopted by the explorer. As is discussed in Section [2.3,](#page-3-3) one of the challenges to implementing this task is that the relation mentions from the candidate triples may not be unaligned to the relations in the prior KG. In order to address this issue, we propose the Translated Relation Alignment Score (TRAS). This score facilitates the alignment of the relations between the candidate triples and the existing relations in the prior KG. After aligning the relations, our system translates the candidate triples to the aligned candidate triples. It then ranks the aligned candidate triples by considering the semantic information residing in the prior KG. The highly-ranked triples are integrated into the prior KG to generate an enriched KG. We expand the details of this process in the remainder of this section.
**Translated Relation Alignment Score (TRAS).**Given two KGs G<sup>1</sup> = hE1, R1, T1i and G<sup>2</sup> = hE2, R2, T2i sets (T<sup>1</sup> T T2 = φ). Then the TRAS score s(r1, r2) between two relation r<sup>1</sup> and r<sup>2</sup> (∀r<sup>1</sup> ∈ R1, ∀r<sup>2</sup> ∈ R2) is computed as follows

<span id="page-4-3"></span>
$$
s(r_1, r_2) = \gamma s_m(r_1, r_2) + (1 - \gamma) s_e(r_1, r_2), \qquad (10)
$$

where sm(r1, r2) is the text mention similarity between r<sup>1</sup> and r2, γ is the weight of the text mention similarity. The quantity se(r1, r2) is the**translated relation similarity**between two relations (r<sup>1</sup> and r2) which can be computed as follows

<span id="page-4-1"></span>
$$
s_e(r_1, r_2) = Sim(\sum_{\forall (i, r_1, j) \in T_1} e_i - e_j, \sum_{\forall (i, r_2, j) \in T_2} e_i - e_j),
$$
\n(11)

![](_page_5_Figure_1.jpeg)

<span id="page-5-0"></span>Fig. 2. The "Collaborative Knowledge Graph Fusion" framework for the Knowledge Graph Fusion with Open Corpus task. Our framework consists of two alternative running processes: 1) an explorer process carries on the Joint-Event-Extraction (JEE) task and 2) a supervisor process aligns and merges the extracted triples to a prior knowledge graph. Our system first embeds the texts to the latent vectors of tokens and then optimizes the forward scores for the explorer process. After training the JEE model, our system extracts the triples T 0 from the open texts. Then, our system treats them as candidate triples and enriches them to the prior KG by referring the proposed Translate Relation Alignment Score (TRAS). The enriched KG and the trained KGE likelihood scoring function helps to sample the top positive and negative entity pairs for the explorer process in return.

where Sim(∗, ∗) can be any similarity function between two vectors. In this paper, we use the Cosine similarity for this task. Generally, the summed entity embedding difference in Equation [11](#page-4-1) represents the embedding vector for a given relation. As a result, Equation [11](#page-4-1) computes the proximity between two relations in different KGs by considering the entities adjacent to them.
**Aligned Triple Set.**Our system ranks the relation pairs between the candidate triples from T 0 and the triples in the prior KG using their TRAS scores. As a result, our system translates the candidate triples from the JEE process to an aligned triple set with the same relation set in the prior KG. The aligned triple set is denoted by ∆T.
**Knowledge Graph Embedding (KGE) Triple Likelihood.** After generating the aligned candidate triple set from the extracted triples, the supervisor ranks the candidate triples and merges the top-ranked triples to the current prior KG. To this end, we use a Knowledge Graph Embedding (KGE) Triple likelihood to perform the ranking task for triples. This function represents the action of the supervisor and it is implemented using a Convolutional Neural Network (CNN) [\[39\]](#page-12-12) based model to map the triples to an R 1 score. Formally, given a KG G = hE, R, Ti. The KGE triple likelihood fG(i, r, j) (∀(i, j) ∈ E, ∀r ∈ R) is computed as follows

<span id="page-5-2"></span>
$$
f_G(i, r, j) = \delta(F([C_1, C_2, C_3, \dots, C_m])),\tag{12}
$$

where δ is the Sigmoid function, F is a fully-connected layer to map the concatenated convolution results to a R 1 score that refers to the plausible probability for the triple (i, r, j) based on G. The quantity C<sup>n</sup> is the n-th convolutional result which can be computed as follows

$$
C_n = Maxpool(Relu(W_n \otimes [e_i^T, e_r^T, e_j^T] + B_n)), \quad (13)
$$

where W<sup>n</sup> is the n-th (n=1, 2, . . . , m) convolutional kernel and B<sup>n</sup> is the corresponding bias, ⊗ is the convolution operator, M axpool is the Maxpooling function, Relu is the ReLU active function and e<sup>r</sup> is the embedding vector for the relation r. To alleviate the problems of sparsity in the extracted relations, rather than the one-hot encoding with a fixed dictionary, we applied a similar method to Equation [8](#page-4-2) to sum all the tokens in a relation mention to obtain the embedding vector e<sup>r</sup> of a relation r.

The KGE triple likelihood is trained by optimizing a BPR loss function

<span id="page-5-3"></span>
$$
\mathcal{L}_s = -\sum_{\substack{\forall (i,r,j) \in \mathcal{T} \cup \Delta \mathcal{T}, \\ \forall (i',r,j') \in N}} \log \left( \delta(f_G(i,r,j) - f_G(i',r,j')) \right). \tag{14}
$$

Optimizing this loss function maximizes the difference between the positive and negative triples. Since this training uses all of the triples in the prior KG, the trained KGE triples likelihood represents the action of a supervisor based on the current KG.

<span id="page-5-1"></span>**Benchmark Entity Pairs Sampling**. With the KGE triple likelihood to hand, we propose an algorithm (cf. in Algorithm [1\)](#page-5-1) to obtain the top positive and negative set pairs based on the current KG and embedding.

| Algorithm 1: Benchmark Entity Pairs Sampling                      |  |  |  |  |  |
|-------------------------------------------------------------------|--|--|--|--|--|
| Data: a KG G = hE, R, Ti, the embedding mapper E                  |  |  |  |  |  |
| from the JEE process, a threshold k.                              |  |  |  |  |  |
| +, the negative<br>Result: the positive entity pair set P         |  |  |  |  |  |
| −.<br>entity pair set P                                           |  |  |  |  |  |
| 1 begin                                                           |  |  |  |  |  |
| Compute all fG(i, r, j)s (∀(i, r, j) ∈ T) with Eq. (12).<br>2     |  |  |  |  |  |
| Sort the triples in T in ascending order and select<br>3          |  |  |  |  |  |
| +.<br>the top-k ranked entity pairs P                             |  |  |  |  |  |
| Enumerate all the negative triples N<br>4                         |  |  |  |  |  |
| (∀(i, r, j) ∈/ T, ∀i, j ∈ E, ∀r ∈ R).                             |  |  |  |  |  |
| Compute all fG(i, r, j)s (∀(i, r, j) ∈ N) with Eq. (12).<br>5     |  |  |  |  |  |
| 0<br>Sort the triples in T<br>in descending order and select<br>6 |  |  |  |  |  |
| +.<br>the top-k ranked entity pairs P                             |  |  |  |  |  |
| + and<br>−.<br>Output P<br>P<br>7                                 |  |  |  |  |  |
| 8 end                                                             |  |  |  |  |  |

The sampled positive and negative entity pairs are used directly as the benchmarks to supervise the explorer process (cf. Equation [6\)](#page-4-0). This simulates the way in which the supervisor provides the key examples to the explorer for the exploration task.

#### 3.4 The Complete Process and Discussion

The complete Collaborative Knowledge Graph Fusion process is described in the Algorithm [2.](#page-6-1) We initialize the

**Algorithm 2:**Collaborative Knowledge Graph Fusion Algorithm

|    | Data: A prior KG G = hE, R, Ti, a corpus D and a     |
|----|------------------------------------------------------|
|    | threshold k for the polarity triple sampling and a   |
|    | threshold ε for the KG enrichment.                   |
|    | 0<br>Result: An enriched KG G                        |
|    | 1 begin                                              |
| 2  | Initialize the embedding mapper E for all the        |
|    | tokens using the pre-trained features.               |
| 3  | 0 ←<br>0 ←<br>let G<br>G, T<br>φ.                    |
| 4  | while Round in [0, K) do                             |
| 5  | Supervisor-step:                                     |
| 6  | 0<br>if T<br>6= φ then                               |
| 7  | 0<br>Align the relations in T<br>to R with Eq. (10). |
| 8  | ∆T ←Find the top-K triples in the aligned            |
|    | 0 with the trained<br>T<br>fG0 (∗).                  |
| 9  | 0 ←<br>0<br>S<br>T<br>∆T<br>T                        |
| 10 | end                                                  |
| 11 | 0<br>Sample the negative triple set N based on T     |
| 12 | Train the KGE triple likelihood fG0 (∗) by           |
|    | 0<br>minimizing Eq. (14). with T<br>and N.           |
| 13 | Sample the top-k positive and negative entity        |
|    | + and<br>− based on Algorithm 1 with<br>pairs P<br>P |
|    | 0<br>T<br>and the embedding map E.                   |
| 14 | Explorer-step:                                       |
| 15 | Train the benchmark-based supervision JEE by         |
|    | minimizing the function in Eq. (9) with JEE          |
|    | training data.                                       |
| 16 | 0<br>Exhaustive generate the candidate triples T     |
|    | based on the mention results from the JEE            |
|    | testing data with the trained JEE.                   |
| 17 | end                                                  |
| 18 | 0<br>Output G                                        |
|    | 19 end                                               |

embeddings for all tokens in the corpus with pre-trained features (BERT [\[36\]](#page-12-9) in this paper, but alternative methods could potentially be used if necessary). These embeddings are then used in the supervisor process to infer the positive or negative entity pair sets using a prior knowledge graph. Next, the obtained positive and negative entity pair sets are used to supervise the explorer process. Then the JEE model in the explorer process extracts improved entities and relations to enrich the prior knowledge graph. The supervisor adds the top-K ranked aligned candidate triples in using beam search.
**Discussion and Analysis.**Our model links event extraction and knowledge graph fusion together as a single process. This alternative process enhance the performance of both of the aforementioned tasks and also results a high quality enriched KG. The main reasons for these improvements are twofold. First, with more useful knowledge implications (evaluated extracted triples from the corpus) for a given knowledge graph, the semantic relationships between its entities are improved. As a result, the performance of the knowledge graph embedding with the enriched knowledge graph is also improved. Second, the accuracies for the entity and relation extraction tasks are also improved with

the help of the enriched knowledge graph.

## 3.5 Negative Triple Sampling and Training

<span id="page-6-1"></span>Many existing methods use the randomized head or tail entity replaced triples from the positive triple set as the negative samples [\[40\]](#page-12-13). To further improve the quality of the negative samples in Line 11 of Algorithm [2,](#page-6-1) we treat the output of random sampled negative triples as the candidate set and then further use the KGE triple likelihood to measure their likelihoods. The final negative samples set in Line 11 of Algorithm [2](#page-6-1) are the top-ranked samples from the candidate set based on the KGE triple likelihood scores.

## <span id="page-6-0"></span>4 EXPERIMENTS AND ANALYSIS

In this section, we aim to address the following research questions:

-**RQ1:**Can a system in the proposed Collaborative Knowledge Graph Fusion framework successfully improve both the performances for the JEE and KGE tasks?
-**RQ2:**Are the automatically extracted and translated triples valuable or suitable for the target KG?
-**RQ3:**What is the generalizability of a system with the proposed Collaborative Knowledge Graph Fusion framework representation across different realworld corpora and KGs?

We also perform ablation analysis to investigate the effect of each module of the model, as well as a qualitative analysis of detailed examples.

### 4.1 Datasets

Since our system consists of the optimization processes of a JEE task and a KGF task, our dataset contains several real-world corpora for the JEE task and also two public Knowledge Graphs (KG) for the KGF task.
**The corpora.**ACE 2005 [\[31\]](#page-12-4) is a widely used dataset to test the performances for the event extraction models. WebNLG is a corpus used for a challenge of natural language generation [\[41\]](#page-12-14). CoNLL is a Spanish news corpus from [\[42\]](#page-12-15). We create the NYT and CoNLL datasets[1](#page-7-0) by preprocessing the original NYT [\[43\]](#page-12-16) and CoNLL [\[42\]](#page-12-15) corpora with the CoreNLP[2](#page-7-1) . This preprocessing includes annotating the triggers and entities from the sentences.
**The Knowledge Graphs.**In order to implement the benchmark-based supervision mechanism at the explorer process, we preprocess the WN18 and FB15k-237 [\[28\]](#page-12-1) as the prior KGs in our tasks. Since the entities in each KG are encoded as the inner IDs, we map these IDs to the real entity mentions by the corresponding mapping files. Further, since freebase API depressed, we map the entity IDs in FB15k-237 to the URLs on the Wikidata[3](#page-7-2) ) and then crawl the Wikidata titles to create the real entity mentions.
**Preprocessing Details.**To implement a complete "Collaborative Knowledge Graph Fusion" framework, we preprocess the datasets to obtain the training sets and the testing sets for the supervisor and explorer respectively. The details of these preprocessed datasets are list in the following Tables.

TABLE 1 Summary of the Corpora for the Explorer (JEE) Process

|                | ACE2005 | NYT   | CoNLL | WebNLG |
|----------------|---------|-------|-------|--------|
| Sentences      | 17,606  | 6,355 | 3,903 | 3,973  |
| Training sent. | 16,765  | 5,500 | 3,000 | 2,649  |
| Testing sent.  | 841     | 855   | 903   | 1,324  |

TABLE 2 Summary of the KGs for the Supervisor (KGF) Process

|       |                 | ACE2005 | CoNLL | NYT   | WebNLG |
|-------|-----------------|---------|-------|-------|--------|
| FB15K | Seed triples    | 20,00   | 3,440 | 3,000 | 3,973  |
|       | Testing triples | 969     | 698   | 1,129 | 1,786  |
| WN18  | Seed triples    | 526     | 68    | 2,042 | 311    |
|       | Testing triples | 129     | 68    | 730   | 113    |

#### 4.2 Comparison Baselines

We provide the baselines on both the JEE and the KGF tasks. The performance of KGF is evaluated by the link prediction performance of the trained knowledge graph embedding.
**JEE baselines.**- StagedMaxEnt [\[35\]](#page-12-8) and TwoStageBeam [\[44\]](#page-12-17) are classic pipe-lined framework methods to extract the event factors jointly.
- Reranking [\[35\]](#page-12-8) is the statistical state-of-the-art joint event extraction method.
- Seq2Seq [\[45\]](#page-12-18) is a Joint Event Extraction (JEE) model with the Sequence-to-Sequence framework. Our experiments use the universal Sequence-to-Sequence framework implementation from [\[16\]](#page-11-15).
- Seq2Seq<sup>∗</sup> [\[45\]](#page-12-18) is the extended Seq2Seq model with the Glove [\[46\]](#page-12-19) pre-trained features.
- CRF<sup>∗</sup> [\[45\]](#page-12-18) is a method extended from Seq2Seq with the conditional random field layer with the Glove [\[46\]](#page-12-19) pre-trained features.

<span id="page-7-1"></span>2. https://stanfordnlp.github.io/CoreNLP/

- BERT [\[36\]](#page-12-9) is the original BERT with Seq2Seq downstream layers.
- Joint3EE [\[47\]](#page-12-20) is an embedding-based method to extract the entities, event triggers and arguments together.
- Benchmark-based Supervision JEE (BJEE) is the joint model proposed in our paper. Our model supervised by the benchmark entity pairs sampled from a given knowledge graph. It is the explorer process in Sec [3.2.](#page-4-5) The subscripts in the experimental results are the names of the given knowledge graphs.

#### KGF baselines.

- TransE [\[28\]](#page-12-1) is a classic statistical KGF model. It assumes that a relation of a triple can be represented as the difference between the head and tail entity vectors of that triples. It trains the latent vectors for all the triples based on the aforementioned assumption.
- ConvE [\[29\]](#page-12-2) is a KGF method to concatenate the vectors for entities to create a matrix to represent the triples. It applies the convolutional neural network to capture the proximity between entities in a triple.
- Supervisor is the method proposed in our paper. It is the supervisor process in Sec [3.3](#page-4-6) that iteratively enriches its training knowledge triples with the extracted result from the explorer process.

#### 4.3 Evaluation Metrics

To compare the JEE and KGF tasks, we provide two families of metrics for them respectively.
**Supervisor process (KGF task).**In the KGF task, we apply the MRR, Hit@10, Hit@20 and Hit@30 as the metrics to measure the performance of a model to predict or judge the possibility of a triple.

The MRR (Mean Reciprocal Rank, MRR) is computed by Equation in our work.

$$
MRR = \sum_{t \in \hat{T}} \frac{1}{rank_t},\tag{15}
$$

where Tˆ is the testing triple set for the testing process.

Hit@n is the ratio of the positive triples that contains in the top-n ranked triples (n = 10, 20, 30 in our experiment) by our models towards the testing triple set Tˆ.

Since our system requires to run on the JEE and KGF tasks alternatively, in order to improve the efficiency we presampled the positive and negative triples from the testing triples and wrote them to files. Our evaluation on the performances of the KGF tasks are based on these pre-sampled triples.
**Explorer process (JEE task).**The performance of JEE is measured by the Precision, Recall, and the F1-scores for the triggers, the entities, and the arguments. The Precision is measured by the ratio of the correct tags output by a model from all the tokens in a corpus and the Recall is the ratio of the predefined tags contains in the output tags of a model.

#### 4.4 Prototype System and Implementation Details

We implement a prototype system with the proposed Collaborative Knowledge Graph Fusion framework with Pytorch. This system consists of an explorer process that

<span id="page-7-0"></span><sup>1.</sup> https://github.com/hkharryking/labeled NYT CoNLL

<span id="page-7-2"></span><sup>3.</sup> https://www.wikidata.org

TABLE 3 Detailed comparison on ACE 2005 testing set.

<span id="page-8-0"></span>

|              | Event Trigger Identification |        |      | Event Trigger Classification |        | Event Argument Identification |           | Event Argument Classification |      |           |        |      |
|--------------|------------------------------|--------|------|------------------------------|--------|-------------------------------|-----------|-------------------------------|------|-----------|--------|------|
| Model        | Precision                    | Recall | F1   | Precision                    | Recall | F1                            | Precision | Recall                        | F1   | Precision | Recall | F1   |
| StagedMaxEnt | 73.9                         | 66.5   | 70.0 | 70.4                         | 63.3   | 66.7                          | 75.7      | 20.2                          | 31.9 | 71.2      | 19.0   | 30.0 |
| TwoStageBeam | 76.6                         | 58.7   | 66.5 | 74.0                         | 56.7   | 64.2                          | 74.6      | 25.5                          | 38.0 | 68.8      | 23.5   | 35.0 |
| Reranking    | 77.6                         | 65.4   | 71.0 | 75.1                         | 63.3   | 68.7                          | 73.7      | 38.5                          | 50.6 | 70.6      | 36.9   | 48.4 |
| Joint3EE     | 70.5                         | 74.5   | 72.5 | 68.0                         | 71.8   | 69.8                          | 59.9      | 59.8                          | 59.9 | 52.1      | 52.1   | 52.1 |
| Seq2Seq      | 66.7                         | 62.4   | 64.5 | 57.3                         | 53.7   | 55.5                          | 62.8      | 72.8                          | 67.5 | 46.3      | 56.6   | 50.9 |
| Seq2Seq∗     | 72.4                         | 67.5   | 69.9 | 69.7                         | 65.0   | 67.2                          | 72.7      | 75.0                          | 73.8 | 58.7      | 67.0   | 62.6 |
| CRF∗         | 71.9                         | 73.6   | 72.7 | 68.2                         | 68.2   | 68.2                          | 70.7      | 79.6                          | 74.9 | 58.7      | 66.0   | 62.1 |
| BERT         | 75.0                         | 75.0   | 75.0 | 75.0                         | 75.0   | 75.0                          | 82.8      | 72.6                          | 77.4 | 71.4      | 69.0   | 70.2 |
| BJEEwn18     | 88.9                         | 66.7   | 76.2 | 85.7                         | 60.0   | 70.6                          | 88.2      | 77.8                          | 82.7 | 80.4      | 72.6   | 76.3 |
| BJEEf b15k   | 88.9                         | 72.7   | 80.0 | 88.9                         | 72.7   | 80.0                          | 89.0      | 77.7                          | 83.0 | 86.5      | 69.8   | 77.2 |

<span id="page-8-1"></span>TABLE 4 Comparison on the entity extraction on the ACE2005 testing set.

| Model       | Precision | Recall | F1   |
|-------------|-----------|--------|------|
| Seq2Seq     | 67.5      | 83.2   | 74.6 |
| Seq2Seq∗    | 74.4      | 85.1   | 79.4 |
| CRF∗        | 75.2      | 84.6   | 79.6 |
| Reranking   | 82.4      | 79.2   | 80.7 |
| PipelineGRU | 80.6      | 80.3   | 80.4 |
| Joint3EE    | 82.0      | 80.4   | 81.2 |
| BERT        | 89.2      | 78.3   | 83.4 |
| BJEEwn18    | 92.4      | 81.5   | 86.6 |
| BJEEf b15k  | 95.1      | 83.0   | 88.6 |

performs the Joint-Event-Extraction (JEE) task to extract the triples from a corpus and a supervisor process that conduct the Knowledge Graph Fusion (KGF) process to train the KGE triple likelihood based on the prior Knowledge Graph (KG). As is introduced in Section [3,](#page-3-0) our system enriches a prior KG as follows. In the beginning, the explorer process extracts the triples from a given corpus under the guidance (the Benchmark-based Supervision Mechanism) of the supervisor. After the explorer submits the triples to the supervisor, the supervisor translates the triples to suit the form of its prior KG. With the translated triples the supervisor assesses the quality of the triples based on the KGE triple likelihood (represents its own understanding of the prior KG). In the end, the supervisor merges highquality triples found in the last step to its prior KG and it also updates the benchmarks to the explorer.

In order to create a fair comparison platform, all the sequence-to-sequence encoders were implemented based on a BERT [\[36\]](#page-12-9) of 768 hidden dimensions. Since our framework requires two alternative processes, we use an Adam optimizer [\[48\]](#page-12-21) with 1e-3 learning rate and 30 epochs to train the explorer process for non-BERT models and all the BERT-based models (include our own) are trained with 2e-5 learning rate and 30 epochs. We apply an Adadelta [\[49\]](#page-12-22) optimizer with 1e-1 learning rate and 20 epochs to train the supervisor process. The rounds of the Collaborative Knowledge Graph Fusion framework are set to 8 for all our models. Both the weights for the benchmark-based supervision and the mention similarity ( α and γ) set to 0.5 in the prototype system. Besides, this prototype system runs on a Linux machine with 4 NVIDIA 2080TI GPUs.

### 4.5 Comparison on the JEE task

We compare our model with the others on the standard event extraction dataset ACE 2005. The results of the event trigger and argument extractions are shown in the Table [3.](#page-8-0) We observe that, the performances on all related subtasks of our model are superior to the other alternatives. We further compare the performance of the entity mention detection of our model with other methods, where our result also excels the other methods (in Table [4\)](#page-8-1). All these results verify that effectiveness of the proposed supervisorexplorer mechanism boosts the performance of the JEE process. Besides, we find that, due to the sequence-tosequence (seq2seq) uniform framework, the performances on the argument identification and classification tasks of the seq2seq-framework models are significant improved.

To validate the universality of our method, we compare the overall extraction performances for the proposed JEE models guided by FB15K and WN18 knowledge graphs on all mentioned real-world datasets in the Table [5.](#page-9-0) Since many methods do not consider these datasets, we only report the results of our implemented methods in this experiment. We can observe that the proposed method extracts better mentiones (both the event argument and trigger mentions) than the other non-knowledge-base-guided methods. Further, an interesting thing is that, although the CONLL is a Spanish corpus, the performances of the event extraction tasks on it can still be boosted by the proposed framework with the English-written knowledge graphs (FB15K and WN18). The reason is that many proper nouns are shared by both Spanish and English, and the semantic structure of them might also help the event extraction in Spanish. All the results in this experiment verify that the proposed Collaborative Knowledge Graph Fusion framework effectively boosts the performance of the JEE processes.

#### 4.6 Comparison on the KGF task

We compare the performance of our method with the other KGF models on the triple prediction task in this experiment. This experiment conducts in the following way. The classic models TransE and ConvE are directly trained on the training set of the knowledge graph FB15K. The supervisor of our model is trained with an enriched training set that is obtained through the proposed Supervisorexplorer Collaborative Learning process. All models are tested with the same testing set of FB15K. The results of the supervisor model are obtained by alternatively run the

| TABLE 5                                                              |  |  |  |  |  |  |
|----------------------------------------------------------------------|--|--|--|--|--|--|
| Comparison on all the real-world datasets with overall performances. |  |  |  |  |  |  |

<span id="page-9-0"></span>

| Model      | ACE 2005  |        |      | NYT       |        | CoNLL |           |        | WebNLG |           |        |      |
|------------|-----------|--------|------|-----------|--------|-------|-----------|--------|--------|-----------|--------|------|
|            | Precision | Recall | F1   | Precision | Recall | F1    | Precision | Recall | F1     | Precision | Recall | F1   |
| Seq2Seq∗   | 71.2      | 73.9   | 72.5 | 91.0      | 88.2   | 89.5  | 86.6      | 88.7   | 87.6   | 91.2      | 90.9   | 91.1 |
| CRF∗       | 71.3      | 76.5   | 73.8 | 89.9      | 89.8   | 89.9  | 87.3      | 88.6   | 88.0   | 92.2      | 89.6   | 90.9 |
| BERT       | 87.1      | 86.9   | 87.0 | 97.8      | 97.8   | 97.8  | 94.2      | 94.2   | 94.2   | 90.1      | 90.0   | 90.1 |
| BJEEf b15k | 92.1      | 92.1   | 92.1 | 99.2      | 99.2   | 99.2  | 96.3      | 96.3   | 96.3   | 96.3      | 96.3   | 96.3 |
| BJEEwn18   | 96.0      | 94.9   | 95.5 | 99.0      | 99.0   | 99.0  | 95.8      | 95.6   | 95.7   | 98.2      | 98.2   | 98.2 |

TABLE 6

Top extracted and aligned results from ACE 2005 corpus to knowledge graph FB15k by our system.

<span id="page-9-4"></span>

| Rank |                            | FB15K           |                             |                                                            |                                        |
|------|----------------------------|-----------------|-----------------------------|------------------------------------------------------------|----------------------------------------|
|      | Head Entity                | Trigger mention | Trigger type                | Tail Entity<br>1<br>93.9                                   | Relation<br>wn18_webnlg                |
| 1    | the Persian Gulf           | killed          | Life                        | 2<br>95.3<br>all six British crew members                  | /people/deceased person/place of death |
| 2    | two Royal Navy helicopters | killed          | Life                        | all six British crew members and one American<br>3<br>93.7 | /people/cause of death/people          |
| 3    | the capital                | rained down     | Conflict                    | aerial more than 300 Tomahawk cruise missiles<br>4<br>92.6 | /people/deceased person/place of death |
| 4    | the United States          | summit          | Contact                     | the president Putin<br>5<br>96.9                           | /business/business operation/industry  |
| 5    | the capital                | took control    | Baghdad the police stations | Movement<br>6<br>95.1                                      | /location/country/form of government   |

supervisor and explorer processes to 8 rounds. Furthermore, since to enumerate all the negative triples requires weeks from our hardware platform, we only used 200 sampled negative triples with their corresponding positive triples as the testing set to compute the metrics. The result of this experiment is shown in Table [7.](#page-9-1) From Table [7,](#page-9-1) we

TABLE 7 Comparison on the KGF task on the FB15K.

<span id="page-9-1"></span>

| Model      | Hit@10 | Hit@20 | Hit@30 | MRR    |
|------------|--------|--------|--------|--------|
| TransE     | 100.0  | 70.0   | 60.0   | 0.0219 |
| ConvE      | 100.0  | 100.0  | 93.3   | 0.0281 |
| Supervisor | 100.0  | 100.0  | 100.0  | 0.0294 |

observe that with the enriched triples, the performance of our KGF model is improved. This verifies that the obtained triples from our Collaborative Knowledge Graph Fusion framework bring useful information to predict the potential knowledge triples in a knowledge graph and the quality of the seed knowledge graph is enhanced.

#### 4.7 Ablation Analysis

Since we use BERT [\[36\]](#page-12-9) as the sequence-to-sequence encoder for our model, we compare the experimental results of our models (BJEEwn18 and BJEEf b15k) with the pure BERT [\[36\]](#page-12-9) model (with the same hidden dimensions) in Table [3,](#page-8-0) Table [4](#page-8-1) and Table [5.](#page-9-0) We observe that, with the proposed benchmarkbased supervision mechanism, our results significantly outperform the pure BERT after the iterative learning process between the supervisor and explorer. To further discuss the influence of the iterative process, we also provide an experiment to compare the overall JEE performances with different iterative rounds in Figure [3.](#page-9-2) From this figure, the overall JEE performance is improving with the iterative round increasing. This shows that the iterative process between the explorer and supervisor of our model indeed helps the overall performance of the JEE tasks.

![](_page_9_Figure_12.jpeg)

<span id="page-9-2"></span>![](_page_9_Figure_13.jpeg)

#### 4.8 Sensitivity Analysis

In order to further analyze the details of the proposed Collaborative Knowledge Graph Fusion framework, we provide several experiments to study the performance of our system with different forms of the teacher or explorer processes.

Figure [4](#page-9-3) shows the performances of our system with a fixed teacher (with 4 CNN kernels) under explorers in differenct sizes of hidden dimensions. From Figure [4,](#page-9-3) we observe that with the same teacher, the diligent (with more hidden dimensions) of an explorer is, the better performance of the teacher process. performs better.

![](_page_9_Figure_17.jpeg)

<span id="page-9-3"></span>Fig. 4. The performances of our system under different explorers.

Figure [5](#page-10-1) gives the performances of our system with a fixed explorer (with 150 hidden dimensions) under supervisors in different numbers of CNN kernels. From this figure, we observe that, with the same explorer, the performance of our system peaks with the supervisor having a certain number (32 in this expeiment) of CNN kernels.

![](_page_10_Figure_2.jpeg)

<span id="page-10-1"></span>Fig. 5. The performances of our system under different supervisors.

The two aforementioned experiments indicates that, the overall performance of a system with the SSL framework might be boosted by improving the explorer process, and the improvement of this overall performance is limit with the same explorer under different supervisors.

#### 4.9 Case study: Translate and Align the Triples

As is introduced in Algorithm [2,](#page-6-1) the explorer process of our system extracts new triples from the given corpus (ACE 2005) and generates a mapper to align the relations of these extracted triples to the relations in the knowledge graph (FB15K). Then, with the aligned relation mapper, our prototype system translates all the extracted triples in the forms of the target knowledge graph. In the last step, the explorer process ranks these translated triples with the trained KGE likelihood function from the supervisor and submits the top triples to the supervisor.

To further analyze the detail performance of the proposed TRAS (Translated Relation Alignment Score) method, we explore the automatically aligned relations by our Collaborative Knowledge Graph Fusion framework in the task to explore (extract) the ACE 2005 corpus guided by the FB15K knowledge graph.

We pick some top-ranked aligned and translated triples from the ACE 2005 corpus by our system and list them in Table [6.](#page-9-4) We can observe that most of these triples are aligned to the suitable relations in FB15K based on the given corpus. For example, our system aligns and the trigger mention "killed" of the type "Life" to the FB15K relation "/people/deceased person/place of death" for the 1-st triple extracted from the ACE 2005 corpus. In this result, our system infers that the trigger mention "killed" of the ACE 2005 corpus is highly similar to the relation "/people/deceased person/place of death" of the knowledge graph FB15K. In this result, our system infers that the trigger mention "killed" of the ACE 2005 corpus is aligned to the relation "/people/deceased person/place of death" of the knowledge graph FB15K. Our system makes this inference by considering both the semantic similarity between the mentions 'killed" and "deceased" and the affinities of the "PER" entities around the corresponding relations in the two sources. This shows that the proposed TRAS

score provides a possible way for the fully-automatically knowledge graph fusion of the future works.

## <span id="page-10-0"></span>5 RELATED WORKS

In this section, we survey the related works to ours from the perspectives of joint event extraction, knowledge graph fusion and open information extraction.

### 5.1 Joint Event Extraction

Joint event extraction (JEE) aims to obtain the named entities, trigger mentions and relations simultaneously from a given corpus. Many recent works apply the pipe-lined method to achieve this task. That is to train a series of classifiers for the aforementioned sub-tasks and classify the mentions in sentences as different triggers at first. Then, with the classified triggers to identify the entity mentions or relations. StagedMaxEnt [\[35\]](#page-12-8) and TwoStageBeam [\[44\]](#page-12-17) are such kind pipe-lined systems. Reranking [\[35\]](#page-12-8) is the state-ofthe-art statistical pipe-lined method for the JEE task.

Most neural network models apply the embedding method to capture the latent semantic relationships between sentence tokens and try to train different classifiers for different sub-tasks. Joint3EE [\[47\]](#page-12-20) is a such model with the multitask learning framework. However, since the separate training for different classifiers increases the sparsity of the efficient samples to each single classifier, the performance improvement of these methods are limited. The sequenceto-sequence methods [\[16\]](#page-11-15) train a neural network model to match a sentence in forms of a token sequence to a tag sequence. This kind of method focuses all sub-tasks to a single classifier and thus further improves the performance with the limited training data.

#### 5.2 Knowledge Graph Fusion

Knowledge graph fusion [\[18\]](#page-11-17) is a task to fuse a knowledge graph with other data sources. Many KGF systems apply an "enumerate-and-rank" framework [\[26\]](#page-11-25) to complete a knowledge graph. That is, to train a classifier based on a given knowledge graph and identify the possible triples from a series of candidate triples. Usually, such classifer is based on the knowledge graph embedding (KGE) [\[50\]](#page-12-23) method. The TransE [\[28\]](#page-12-1) is a classic KGE method to learn the embedding vectors to represent the triples in a knowledge graph. Recently, many works apply the neural network method to improve the performance of the KGE task. ConvE [\[29\]](#page-12-2) is a neural network KGE model with the convolutional neural network modules. As far as we know, none of the existing methods considers to link the JEE task to the KGE to create an automatically Knowledge Graph Fusion with Open Corpus.

#### 5.3 Open Information Extraction (Open IE)

Open Information Extraction (Open IE) [\[51\]](#page-12-24) is another way to generate structural information from text sources. The traditional methods [\[52\]](#page-12-25), [\[53\]](#page-12-26) get the new relation facts to form a KG based on the hand-crafted patterns. Recent works [\[54\]](#page-12-27), [\[55\]](#page-12-28) apply the neural relation extraction methods to directly generate relational facts from a given corpus and integrate them to an existing KG. During the integration process, these works trained a classifier to judge the correctness of the obtained relations according to the given KG. However, although the current Open IE works extract relational facts (triples) directly from text sources, few of them discuss that how to automatically merge the obtained facts to create a uniform and high-quality KG.

## <span id="page-11-26"></span>6 CONCLUSION AND FUTURE WORK

This paper has proposed a novel Collaborative Knowledge Graph Fusion framework to integrate the joint event extraction and the knowledge graph fusion tasks together. The implemented prototype system with the proposed framework could both extract the entity and trigger mentions and enrich the extracted mentions to a knowledge graph in the form of the knowledge graph triple (entity-relation-entity). To this end, we propose the benchmark-based supervision mechanism to guide the event extraction process of our system with a given knowledge graph and our system also merges the extracted triples to the target knowledge graph by referring the proposed Translated Relation Alignment Score. We test our prototype system on several real-world corpora and knowledge graphs. The experimental results show that our method improves the performances of both the event extraction and knowledge graph fusion processes after the alternatively training. Moreover, the aligned and translated relations from our system also show good interpretability about the improvements of the performances. Our future work is to align the triples directly with their semantic meanings to further improve the performance of our model.

## REFERENCES

- <span id="page-11-0"></span>[1] X. Wang, X. He, Y. Cao, M. Liu, and T. Chua, "KGAT: knowledge graph attention network for recommendation," in*Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, KDD 2019, Anchorage, AK, USA, August 4-8, 2019*, A. Teredesai, V. Kumar, Y. Li, R. Rosales, E. Terzi, and G. Karypis, Eds. ACM, 2019, pp. 950–958.
- <span id="page-11-1"></span>[2] K. Annervaz, S. B. R. Chowdhury, and A. Dukkipati, "Learning beyond datasets: Knowledge graph augmented neural networks for natural language processing," in *Proceedings of NAACL-HLT*, 2018, pp. 313–322.
- <span id="page-11-2"></span>[3] A. Talmor and J. Berant, "The web as a knowledge-base for answering complex questions," in *Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, NAACL-HLT 2018, New Orleans, Louisiana, USA, June 1-6, 2018, Volume 1 (Long Papers)*, M. A. Walker, H. Ji, and A. Stent, Eds. Association for Computational Linguistics, 2018, pp. 641–651.
- <span id="page-11-3"></span>[4] S. Hu, L. Zou, J. X. Yu, H. Wang, and D. Zhao, "Answering natural language questions by subgraph matching over knowledge graphs," *IEEE Transactions on Knowledge and Data Engineering*, vol. 30, no. 5, pp. 824–837, 2018.
- <span id="page-11-4"></span>[5] W. Shen, Y. Yin, Y. Yang, J. Han, J. Wang, and X. Yuan, "Toward tweet entity linking with heterogeneous information networks," *IEEE Transactions on Knowledge and Data Engineering*, pp. 1–1, 2021.
- <span id="page-11-5"></span>[6] D. Vrandecic and M. Krotzsch, "Wikidata: a free collaborative ¨ knowledgebase," *Commun. ACM*, vol. 57, no. 10, pp. 78–85, 2014.
- <span id="page-11-6"></span>[7] G. A. Miller, "Wordnet: A lexical database for english," *Commun. ACM*, vol. 38, no. 11, pp. 39–41, 1995.
- <span id="page-11-7"></span>[8] K. D. Bollacker, C. Evans, P. Paritosh, T. Sturge, and J. Taylor, "Freebase: a collaboratively created graph database for structuring human knowledge," in *Proceedings of the ACM SIGMOD International Conference on Management of Data, SIGMOD 2008, Vancouver, BC, Canada, June 10-12, 2008*, J. T. Wang, Ed. ACM, 2008, pp. 1247–1250.

- <span id="page-11-8"></span>[9] M. Farber, F. Bartscherer, C. Menne, and A. Rettinger, "Linked ¨ data quality of dbpedia, freebase, opencyc, wikidata, and YAGO," *Semantic Web*, vol. 9, no. 1, pp. 77–129, 2018.
- <span id="page-11-9"></span>[10] J. Li, A. Sun, J. Han, and C. Li, "A survey on deep learning for named entity recognition," *IEEE Transactions on Knowledge and Data Engineering*, pp. 1–1, 2020.
- <span id="page-11-10"></span>[11] D. Liu, T. Bai, J. Lian, X. Zhao, G. Sun, J. Wen, and X. Xie, "News graph: An enhanced knowledge graph for news recommendation," in *KaRS@CIKM 2019, Beijing, China, November 7, 2019*, ser. CEUR Workshop Proceedings, vol. 2601. CEUR-WS.org, 2019, pp. 1–7.
- <span id="page-11-11"></span>[12] G. Lample, M. Ballesteros, S. Subramanian, K. Kawakami, and C. Dyer, "Neural architectures for named entity recognition," in *NAACL HLT 2016, The 2016 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, San Diego California, USA, June 12-17, 2016*, K. Knight, A. Nenkova, and O. Rambow, Eds. The Association for Computational Linguistics, 2016, pp. 260–270.
- <span id="page-11-12"></span>[13] Y. Lin, S. Shen, Z. Liu, H. Luan, and M. Sun, "Neural relation extraction with selective attention over instances," in *Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics, ACL 2016, August 7-12, 2016, Berlin, Germany, Volume 1: Long Papers*. The Association for Computer Linguistics, 2016.
- <span id="page-11-13"></span>[14] M. Koutraki, N. Preda, and D. Vodislav, "Online relation alignment for linked datasets," in *The Semantic Web - 14th International Conference, ESWC 2017, Portoroˇz, Slovenia, May 28 - June 1, 2017, Proceedings, Part I*, ser. Lecture Notes in Computer Science, E. Blomqvist, D. Maynard, A. Gangemi, R. Hoekstra, P. Hitzler, and O. Hartig, Eds., vol. 10249, 2017, pp. 152–168.
- <span id="page-11-14"></span>[15] X. Zhao, Y. Jia, A. Li, R. Jiang, and Y. Song, "Multi-source knowledge fusion: a survey," *World Wide Web*, vol. 23, no. 4, pp. 2567– 2592, 2020.
- <span id="page-11-15"></span>[16] Y. Wang, Z. Xu, L. Bai, Y. Wan, L. Cui, Q. Zhao, E. R. Hancock, and P. S. Yu, "Cross-supervised joint-event-extraction with heterogeneous information networks," 2020.
- <span id="page-11-16"></span>[17] P. Huang, X. Zhao, R. Takanobu, Z. Tan, and W. Xiao, "Joint event extraction with hierarchical policy network," in *Proceedings of the 28th International Conference on Computational Linguistics*. Barcelona, Spain (Online): International Committee on Computational Linguistics, Dec. 2020, pp. 2653–2664.
- <span id="page-11-17"></span>[18] H. L. Nguyen, D. Vu, and J. J. Jung, "Knowledge graph fusion for smart systems: A survey," *Inf. Fusion*, vol. 61, pp. 56–70, 2020.
- <span id="page-11-18"></span>[19] X. Dong, E. Gabrilovich, G. Heitz, W. Horn, N. Lao, K. Murphy, T. Strohmann, S. Sun, and W. Zhang, "Knowledge vault: a webscale approach to probabilistic knowledge fusion," in *The 20th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, KDD '14, New York, NY, USA - August 24 - 27, 2014*, S. A. Macskassy, C. Perlich, J. Leskovec, W. Wang, and R. Ghani, Eds., 2014, pp. 601–610.
- <span id="page-11-19"></span>[20] X. L. Dong and D. Srivastava, "Knowledge curation and knowledge fusion: Challenges, models and applications," ser. SIGMOD '15. New York, NY, USA: Association for Computing Machinery, 2015, p. 2063–2066.
- <span id="page-11-20"></span>[21] J. Bleiholder and F. Naumann, "Data fusion," *ACM Comput. Surv.*, vol. 41, no. 1, jan 2009.
- <span id="page-11-21"></span>[22] X. L. Dong, E. Gabrilovich, G. Heitz, W. Horn, K. Murphy, S. Sun, and W. Zhang, "From data fusion to knowledge fusion," *Proc. VLDB Endow.*, vol. 7, no. 10, p. 881–892, jun 2014.
- <span id="page-11-22"></span>[23] R. Sourty, J. G. Moreno, F.-P. Servant, and L. Tamine-Lechani, "Knowledge base embedding by cooperative knowledge distillation," in *Proceedings of the 28th International Conference on Computational Linguistics*. Barcelona, Spain (Online): International Committee on Computational Linguistics, Dec. 2020, pp. 5579– 5590.
- <span id="page-11-23"></span>[24] P. Cui, X. Wang, J. Pei, and W. Zhu, "A survey on network embedding," *IEEE Trans. Knowl. Data Eng.*, vol. 31, no. 5, pp. 833– 852, 2019.
- <span id="page-11-24"></span>[25] R. Socher, D. Chen, C. D. Manning, and A. Y. Ng, "Reasoning with neural tensor networks for knowledge base completion," in *Advances in Neural Information Processing Systems 26: 27th Annual Conference on Neural Information Processing Systems 2013. Proceedings of a meeting held December 5-8, 2013, Lake Tahoe, Nevada, United States*, C. J. C. Burges, L. Bottou, Z. Ghahramani, and K. Q. Weinberger, Eds., 2013, pp. 926–934.
- <span id="page-11-25"></span>[26] Q. Wang, B. Wang, and L. Guo, "Knowledge base completion using embeddings and rules," in *Proceedings of the Twenty-Fourth International Joint Conference on Artificial Intelligence, IJCAI 2015,*

*Buenos Aires, Argentina, July 25-31, 2015*, Q. Yang and M. J. Wooldridge, Eds. AAAI Press, 2015, pp. 1859–1866.

- <span id="page-12-0"></span>[27] S. Guan, X. Jin, Y. Wang, and X. Cheng, "Shared embedding based neural networks for knowledge graph completion," in *Proceedings of the 27th ACM International Conference on Information and Knowledge Management, CIKM 2018, Torino, Italy, October 22-26, 2018*, A. Cuzzocrea, J. Allan, N. W. Paton, D. Srivastava, R. Agrawal, A. Z. Broder, M. J. Zaki, K. S. Candan, A. Labrinidis, A. Schuster, and H. Wang, Eds. ACM, 2018, pp. 247–256.
- <span id="page-12-1"></span>[28] A. Bordes, N. Usunier, A. Garc´ıa-Duran, J. Weston, and ´ O. Yakhnenko, "Translating embeddings for modeling multirelational data," in *Advances in Neural Information Processing Systems 26: 27th Annual Conference on Neural Information Processing Systems 2013. Proceedings of a meeting held December 5-8, 2013, Lake Tahoe, Nevada, United States*, C. J. C. Burges, L. Bottou, Z. Ghahramani, and K. Q. Weinberger, Eds., 2013, pp. 2787–2795.
- <span id="page-12-2"></span>[29] T. Dettmers, M. Pasquale, S. Pontus, and S. Riedel, "Convolutional 2d knowledge graph embeddings," in *Proceedings of the 32th AAAI Conference on Artificial Intelligence*, February 2018, pp. 1811–1818.
- <span id="page-12-3"></span>[30] D. Q. Nguyen, T. D. Nguyen, D. Q. Nguyen, and D. Phung, "A novel embedding model for knowledge base completion based on convolutional neural network," in *Proceedings of the 16th Annual Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT)*, 2018, pp. 327–333.
- <span id="page-12-4"></span>[31] "Ace 2005, linguistic data consortium," [http://projects.ldc.upenn.](http://projects.ldc.upenn.edu/ace) [edu/ace.](http://projects.ldc.upenn.edu/ace)
- <span id="page-12-5"></span>[32] B. D. Trisedya, J. Qi, and R. Zhang, "Entity alignment between knowledge graphs using attribute embeddings," in *The Thirty-Third AAAI Conference on Artificial Intelligence, AAAI 2019, The Thirty-First Innovative Applications of Artificial Intelligence Conference, IAAI 2019, The Ninth AAAI Symposium on Educational Advances in Artificial Intelligence, EAAI 2019, Honolulu, Hawaii, USA, January 27 - February 1, 2019*. AAAI Press, 2019, pp. 297–304.
- <span id="page-12-6"></span>[33] D. Zeng, K. Liu, Y. Chen, and J. Zhao, "Distant supervision for relation extraction via piecewise convolutional neural networks," in *Proceedings of the 2015 Conference on Empirical Methods in Natural Language Processing, EMNLP 2015, Lisbon, Portugal, September 17- 21, 2015*, L. Marquez, C. Callison-Burch, J. Su, D. Pighin, and ` Y. Marton, Eds. The Association for Computational Linguistics, 2015, pp. 1753–1762.
- <span id="page-12-7"></span>[34] S. Ji, S. Pan, E. Cambria, P. Marttinen, and P. S. Yu, "A survey on knowledge graphs: Representation, acquisition and applications," *CoRR*, vol. abs/2002.00388, 2020. [Online]. Available:<https://arxiv.org/abs/2002.00388>
- <span id="page-12-8"></span>[35] B. Yang and T. M. Mitchell, "Joint extraction of events and entities within a document context," in *NAACL HLT 2016, The 2016 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, San Diego California, USA, June 12-17, 2016*, K. Knight, A. Nenkova, and O. Rambow, Eds. The Association for Computational Linguistics, 2016, pp. 289–299.
- <span id="page-12-9"></span>[36] J. Devlin, M. Chang, K. Lee, and K. Toutanova, "BERT: pre-training of deep bidirectional transformers for language understanding," in *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, NAACL-HLT 2019, Minneapolis, MN, USA, June 2-7, 2019, Volume 1 (Long and Short Papers)*, J. Burstein, C. Doran, and T. Solorio, Eds. Association for Computational Linguistics, 2019, pp. 4171–4186.
- <span id="page-12-10"></span>[37] S. Rendle, C. Freudenthaler, Z. Gantner, and L. Schmidt-Thieme, "Bpr: Bayesian personalized ranking from implicit feedback," 2012. [Online]. Available:<https://arxiv.org/abs/1205.2618>
- <span id="page-12-11"></span>[38] S. Arora, Y. Liang, and T. Ma, "A simple but tough-to-beat baseline for sentence embeddings," in *5th International Conference on Learning Representations, ICLR 2017, Toulon, France, April 24-26, 2017, Conference Track Proceedings*, 2017.
- <span id="page-12-12"></span>[39] B. Hu, Z. Lu, H. Li, and Q. Chen, "Convolutional neural network architectures for matching natural language sentences," in *Advances in Neural Information Processing Systems 27: Annual Conference on Neural Information Processing Systems 2014, December 8-13 2014, Montreal, Quebec, Canada*, Z. Ghahramani, M. Welling, C. Cortes, N. D. Lawrence, and K. Q. Weinberger, Eds., 2014, pp. 2042–2050.
- <span id="page-12-13"></span>[40] T. N. Kipf, E. van der Pol, and M. Welling, "Contrastive learning of structured world models," in *8th International Conference on Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April 26- 30, 2020*. OpenReview.net, 2020.

- <span id="page-12-14"></span>[41] C. Gardent, A. Shimorina, S. Narayan, and L. Perez-Beltrachini, "Creating training corpora for NLG micro-planners," in *Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics, ACL 2017, Vancouver, Canada, July 30 - August 4, Volume 1: Long Papers*, R. Barzilay and M. Kan, Eds. Association for Computational Linguistics, 2017, pp. 179–188.
- <span id="page-12-15"></span>[42] "Conll 2002, spanish efe news agency," [https://www.clips.](https://www.clips.uantwerpen.be/conll2002/ner/) [uantwerpen.be/conll2002/ner/.](https://www.clips.uantwerpen.be/conll2002/ner/)
- <span id="page-12-16"></span>[43] E. Sandhaus, "The new york times annotated corpus, publish linguistic data consortium, philadelphia 2008," in *publish Linguistic Data Consortium*, 2008.
- <span id="page-12-17"></span>[44] Q. Li, H. Ji, and L. Huang, "Joint event extraction via structured prediction with global features," in *Proceedings of the 51st Annual Meeting of the Association for Computational Linguistics, ACL 2013, 4-9 August 2013, Sofia, Bulgaria, Volume 1: Long Papers*. The Association for Computer Linguistics, 2013, pp. 73–82.
- <span id="page-12-18"></span>[45] N. Limsopatham and N. Collier, "Bidirectional LSTM for named entity recognition in twitter messages," in *Proceedings of the 2nd Workshop on Noisy User-generated Text, NUT@COLING 2016, Osaka, Japan, December 11, 2016*, B. Han, A. Ritter, L. Derczynski, W. Xu, and T. Baldwin, Eds. The COLING 2016 Organizing Committee, 2016, pp. 145–152.
- <span id="page-12-19"></span>[46] J. Pennington, R. Socher, and C. D. Manning, "Glove: Global vectors for word representation," in *Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing, EMNLP 2014, October 25-29, 2014, Doha, Qatar, A meeting of SIGDAT, a Special Interest Group of the ACL*, A. Moschitti, B. Pang, and W. Daelemans, Eds. ACL, 2014, pp. 1532–1543.
- <span id="page-12-20"></span>[47] T. M. Nguyen and T. H. Nguyen, "One for all: Neural joint modeling of entities and events," in *The Thirty-Third AAAI Conference on Artificial Intelligence, AAAI 2019, The Thirty-First Innovative Applications of Artificial Intelligence Conference, IAAI 2019, The Ninth AAAI Symposium on Educational Advances in Artificial Intelligence, EAAI 2019, Honolulu, Hawaii, USA, January 27 - February 1, 2019*. AAAI Press, 2019, pp. 6851–6858.
- <span id="page-12-21"></span>[48] D. P. Kingma and J. Ba, "Adam: A method for stochastic optimization," in *3rd International Conference on Learning Representations, ICLR 2015, San Diego, CA, USA, May 7-9, 2015, Conference Track Proceedings*, Y. Bengio and Y. LeCun, Eds., 2015.
- <span id="page-12-22"></span>[49] M. D. Zeiler, "ADADELTA: an adaptive learning rate method," *CoRR*, vol. abs/1212.5701, 2012.
- <span id="page-12-23"></span>[50] Q. Wang, Z. Mao, B. Wang, and L. Guo, "Knowledge graph embedding: A survey of approaches and applications," *IEEE Trans. Knowl. Data Eng.*, vol. 29, no. 12, pp. 2724–2743, 2017.
- <span id="page-12-24"></span>[51] G. Angeli, M. J. J. Premkumar, and C. D. Manning, "Leveraging linguistic structure for open domain information extraction," in *Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing of the Asian Federation of Natural Language Processing, ACL 2015, July 26-31, 2015, Beijing, China, Volume 1: Long Papers*. The Association for Computer Linguistics, 2015, pp. 344– 354.
- <span id="page-12-25"></span>[52] G. Stanovsky, J. Ficler, I. Dagan, and Y. Goldberg, "Getting more out of syntax with props," *CoRR*, vol. abs/1603.01648, 2016. [Online]. Available:<http://arxiv.org/abs/1603.01648>
- <span id="page-12-26"></span>[53] Mausam, "Open information extraction systems and downstream applications," in *Proceedings of the Twenty-Fifth International Joint Conference on Artificial Intelligence, IJCAI 2016, New York, NY, USA, 9-15 July 2016*, S. Kambhampati, Ed. IJCAI/AAAI Press, 2016, pp. 4074–4077.
- <span id="page-12-27"></span>[54] L. Cui, F. Wei, and M. Zhou, "Neural open information extraction," in *Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics, ACL 2018, Melbourne, Australia, July 15- 20, 2018, Volume 2: Short Papers*, I. Gurevych and Y. Miyao, Eds. Association for Computational Linguistics, 2018, pp. 407–413.
- <span id="page-12-28"></span>[55] B. D. Trisedya, G. Weikum, J. Qi, and R. Zhang, "Neural relation extraction for knowledge base enrichment," in *Proceedings of the 57th Conference of the Association for Computational Linguistics, ACL 2019, Florence, Italy, July 28- August 2, 2019, Volume 1: Long Papers*, A. Korhonen, D. R. Traum, and L. Marquez, Eds. Association for ` Computational Linguistics, 2019, pp. 229–240.

### IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING, VOL. 14, NO. 8, AUGUST 2020 14

**Yue Wang**received the Ph.D. degree from Sichuan University, Sichuan, China. He was a postdoctor of Peking University, Beijing, China. He is now an Associate Professor at Central University of Finance and Economics, Beijing, China. He has published more than 30 journal and conference papers, including TKDE, WWWJ, Science China: Information Science, IJ-CAI, ICDM, IEEE BigData etc. His current research interests include data mining and machine learning.

![](_page_13_Picture_3.jpeg)
**Ming Li** is currently a "Shuang Long Scholar" Distinguished Professor at the Key Laboratory of Intelligent Education Technology and Application of Zhejiang Province, Zhejiang Normal University, China. He received his PhD degree from the Department of Computer Science and IT at La Trobe University, Australia. He completed two Postdoctoral Fellowship positions with the Department of Mathematics and Statistics, La Trobe University, Australia, and the Department of Information Technology in Education, South

China Normal University, China, respectively. He has published in toptier journals and conferences, including Artificial Intelligence, IEEE TCYB, IEEE TII, ACM TMOS, NeurIPS, ICML. He, as a leading guest editor, organized a special issue "*Deep Neural Networks for Graphs: Theory, Models, Algorithms and Applications*" in IEEE TNNLS. He is a PC member at ICML, AAAI, NeurIPS, ICLR, AJCAI, KDD, and an Associated Editor of Neural Networks.

![](_page_13_Picture_6.jpeg)

**Philip S. Yu**received received the B.S. degree in electrical engineering from National Taiwan University, the M.S. and Ph.D. degrees in EE from Stanford University, and the MBA degree from New York University. He is currently a Distinguished Professor of computer science with the University of Illinois at Chicago (UIC), and holds the Wexler Chair in information technology. He has published more than 970 papers in refereed journals and conferences. He holds or has applied for over 300 US patents. He was a

member of the Steering Committee of the IEEE Data Engineering and the IEEE Conference on Data Mining. He is a Fellow of the ACM and the IEEE. He is on the Steering Committee of the ACM Conference on Information and Knowledge Management. He received the ACM SIGKDD 2016 Innovation Award for his influential research and scientific contributions on mining, fusion, and anonymization of big data, the IEEE Computer Society's 2013 Technical Achievement Award for "pioneering and fundamentally innovative contributions to the scalable indexing, querying, searching, mining, and anonymization of big data", and the Research Contributions Award from ICDM 2003, for his pioneering contributions to the field of data mining. He also received the ICDM 2013 10-year Highest-Impact Paper Award, and the EDBT Test of Time Award (2014). He has received several IBM honors, including two IBM Outstanding Innovation Awards, an Outstanding Technical Achievement Award, two Research Division Awards, and the 94th plateau of Invention Achievement Awards. He was the Editor-in-Chief of the IEEE Transactions on Knowledge and Data Engineering (2001-2004).

![](_page_13_Picture_9.jpeg)
**Edwin R. Hancock**received the B.Sc., Ph.D., and D.Sc. degrees from the University of Durham, Durham, UK. He is currently an Emeritus Professor with the Department of Computer Science, University of York, York, UK. He has published over 200 journal articles and 650 conference papers. Prof. Hancock was a recipient of the Royal Author Biography Society Wolfson Research Merit Award in 2009, the Pattern Recognition Society Medal in 1991, the BMVA Distinguished Fellowship in 2016 and the IAPR

Piere Devijver Award in 2018. He is a fellow of the IAPR, IEEE, the Royal Astronomical Society, the Institute of Physics, the Institute of Engineering and Technology, and the British Computer Society. He was named Distinguished Fellow by the British Machine Vision Association. He has also received best paper prizes at CAIP 2001, ACCV 2002, ICPR in 2006 and 2018, BMVC 20 07, ICIAP in 2009 and 2015. He is currently Editor-in-Chief of the journal Pattern Recognition, and was founding Editor-in-Chief of IET Computer Vision from 2006 until 2012. He has also been a member of the editorial boards of the journals IEEE Transactions on Pattern Analysis and Machine Intelligence, Pattern Recognition, Computer Vision and Image Understanding, Image and Vision Computing, and the International Journal of Complex Networks. He has been Conference Chair for BMVC in 1994 and Program Chair in 2016, Track Chair for ICPR in 2004 and 2016 and Area Chair at ECCV 2006 and CVPR in 2008 and 2014, and in 1997 established the EMMCVPR workshop series. He was Second Vice President of the International Association of Pattern Recognition (2016-2018). He is currently an IEEE Computer Society Distinguished Visitor (2021-2023).

![](_page_13_Picture_12.jpeg)
**Yao Wan**received his Ph.D degree from the College of Computer Science, Zhejiang University, Hangzhou, China, in 2019. He is currently a lecturer of the College of Computer Science and Technology, Huazhong University of Science and Technology. He has been a visiting student of University of Technology Sydney and University of Illinois at Chicago in 2016 and 2018, respectively. His research interests lie in the synergy between artificial intelligence and software engineering, especially natural lan-

guage processing, programming languages, software engineering, and machine learning.

![](_page_13_Picture_15.jpeg)
**Lu Bai**received the Ph.D. degree from the University of York, UK, and both the B.Sc. and M.Sc degrees from Macau University of Science and Technology, Macau SAR, China. He was a recipient of the National Award for Outstanding Self-Financed Chinese Students Study Aboard by China Scholarship Council in 2015, and the Best Paper Awards of the International Conferences ICIAP 2015 (Eduardo Caianello Best Student Paper Award) and ICPR 2018. He is now a Professor in School of Artificial Intelligence, Beijing

Normal University, Beijing, China, Beijing, China. He has published more than 80 journal and conference papers, including TPAMI, TNNLS, TCYB, PR, ICML, IJCAI, ECML-PKDD, ICDM, etc. His current research interests include pattern recognition, machine learning, and financial data analysis. He is currently a member of the editorial board of the journal Pattern Recognition

![](_page_13_Picture_18.jpeg)
**Lixin Cui**received the Ph.D. degree from the University of Hong Kong, HKSAR, China, and both the B.Sc. and M.Sc. degrees from Tianjin University, Tianjin, China. She is now an Associate Professor at Central University of Finance and Economics, Beijing, China. She was the recipient of the Outstanding Paper Awards of the International Conference IEEE IEEM 2019, the Best Student Paper Awards of the International Conferences APIEMS 2011 and WCE 2011. She is currently an Associate Editor of Pat-

tern Recognition Journal. She has published more than 40 journal and conference papers, including TPAMI, TFS, TCYB, TNNLS, PR, WWWJ, IJCAI, ECML-PKDD, etc. Her current research interests include machine learning, deep learning, and their applications in Fintech problems. She is currently a member of the editorial board of the journal Pattern Recognition.

![](_page_13_Picture_21.jpeg)
**Zhuo Xu** received the B.Sc. degrees from Central University of Finance and Economics. He is now an graduate explorer in Central University of Finance and Economics, Beijing, China.
