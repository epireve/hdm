---
cite_key: garg_2021
title: Knowledge Graph Completion: A Bird's Eye View on Knowledge Graph Embeddings, Software Libraries, Applications and Challenges
authors: Satvik Garg, Dwaipayan Roy
year: 2022
date_processed: 2025-07-02
phase2_processed: true
original_folder: arxiv_2205.09088_A_Birds_Eye_View_on_Knowledge_Graph_Embeddings,_So
images_total: 22
images_kept: 22
images_removed: 0
tags: 
keywords: 
---

# Knowledge Graph Completion: A Bird's Eye View on Knowledge Graph Embeddings, Software Libraries, Applications and Challenges

Satvik Garg^a^, Dwaipayan Roy^b,^*

*^a^Department of Computer Science, Jaypee University of Information Technology, Solan, India ^b^Department of Computational and Data Sciences, Indian Institute of Science, Education and Research, Kolkata, India*

## Abstract

In recent years, Knowledge Graph (KG) development has attracted significant researches considering the applications in web search, relation prediction, natural language processing, information retrieval, question answering to name a few. However, often KGs are incomplete due to which Knowledge Graph Completion (KGC) has emerged as a sub-domain of research to automatically track down the missing connections in a KG. Numerous strategies have been suggested to work out the KGC dependent on different representation procedures intended to embed triples into a low-dimensional vector space. Given the difficulties related to KGC, researchers around the world are attempting to comprehend the attributes of the problem statement. This study intends to provide an overview of knowledge bases combined with different challenges and their impacts. We discuss existing KGC approaches, including the state-of-the-art Knowledge Graph Embeddings (KGE), not only on static graphs but also for the latest trends such as multimodal, temporal, and uncertain knowledge graphs. In addition, reinforcement learning techniques are reviewed to model complex queries as a link prediction problem. Subsequently, we explored popular software packages for model training and examine open research challenges that can guide future research.

*Keywords:* Knowledge Graphs, Knowledge Graph Embeddings, Representation Learning, Knowledge Graph Completion, Link Prediction, Reinforcement Learning, Neural Networks

## Introduction

The concept of Knowledge Graphs (KG) was proposed by Google in 2012 to utilize semantic information in web search to enhance the performance of web crawlers and upgrade the experience of clients [[1]](#ref-1). The Knowledge Graphs are based on numerous information retrieval frameworks that obtain admittance to organized information and are utilized to distinguish and disambiguate elements in text, advance query response with semantically organized outlines, and give links to related entities in experimental search. Leveraging real world information in data

^*Corresponding author
*Email addresses:* satvikgarg27@gmail.com (Satvik Garg), dwaipayan.roy@iiserkol.ac.in (Dwaipayan Roy)

frameworks is one of the significant advancements in automation [[2]](#ref-2). Representation of data and logic inspired by human critical thinking expected to present data or information to secure, improve the ability to deal with complex questions and have drawn in incredible scholarly thought and professions [[1]](#ref-1) [[3]](#ref-3) [[4]](#ref-4) [[5]](#ref-5).

Knowledge graph is a graph-based data representation modality consisting of binary relationships and labeled edges. It comprises real-world triplets, where each triplet or fact (*e*1,*r*, *e*2) addresses a connection *r*between head entity*e*1 and tail entity *e*2. They are often called as multi relational graphs where each node and edge represents an element (or entity) and a relation, respectively. The relations helps to connect nodes to encode different links separately. The entities can be addressed as things of real world knowledge such as film, person, city, country to name a few. An example is shown in figure 1, a relation *'Friends with'*connects person entity type, and the connection type*'works in'*represents the relationship between entity type of person and organization.

The knowledge graphs are important for many applicative use cases like social networks, web-based collaborative knowledge bases like DBpedia [[6]](#ref-6), and in healthcare when trying to model protein-protein interaction networks or genetic information [[7]](#ref-7). They are also useful for Natural Language Processing (NLP) applications like entity recognition [[8]](#ref-8), entity linking [[9]](#ref-9), dialogue systems [[10]](#ref-10), semantic parsing [[11]](#ref-11), information retrieval [[12]](#ref-12) and question answering systems [[13]](#ref-13). Most KG's are available online and open sourced ranging from domain specific KG's such as GeneOntology [[14]](#ref-14) and for general purposes such as YAGO [[15]](#ref-15), FreeBase [[16]](#ref-16), DBpedia [[6]](#ref-6), WordNet [[17]](#ref-17), NELL [[18]](#ref-18). Knowledge Graphs are the result of automatic generation, in some cases from mining web pages like GDELT [[19]](#ref-19) and craft source operations like WIKIDATA [[20]](#ref-20). Commercial KG's are pretty common in applications like search engines. Examples of commercial KG include Facebook Open Graph, Microsoft Satori, Yahoo Spark and Google Knowledge Graph [[21]](#ref-21).

![Image Description: The image is a knowledge graph illustrating relationships between entities. Nodes represent entities (e.g., John, Company, Delhi), while edges represent relationships (e.g., "works in," "likes," "is a"). The graph visually depicts a knowledge base's structure, showing how different entities are connected and the types of relationships between them. It likely serves to illustrate the data structure used in a knowledge representation or reasoning system described in the paper.](_page_1_Figure_3.jpeg)

**Figure 1:** An example of hypothetical knowledge graph.

Knowledge graphs are often generated automatically, have missing edges, and may not be completely comprehensive. An emerging issue arise when huge KG's, for example, DBpedia and Freebase contain many facts or triples on real world knowledge and are long way from complete [[22]](#ref-22) [[23]](#ref-23). In Freebase, it has been shown that about 70% of people have missing birth status, while 75% miss identification and 95% have no information on their parents [[22]](#ref-22). In DBpedia, like Freebase, around 65% of people do not have any birthplace knowledge, and 60% of scientists miss information on their study area [[23]](#ref-23). Some reasons are introduced as to why KG's have flaws of its own and are mainly fragmentary. First, recognizing billions of reals on human knowledge is not scalable. In addition, accurate information and data are dynamically advancing, making it challenging to build complete and suitable KGs. A link prediction problem is presented as an examination area named Knowledge Graph Completion (KGC) [[5]](#ref-5) to combat all the previously mentioned issues and helps to anticipate the missing connection and knowledge between entities or facts. An example is shown in figure 2 to comprehend the topic of link prediction easier to understand. Strong lines address total or existing relationships, while red dotted lines represent potential relationships that may extend the knowledge graph completeness.

Leveraging automation techniques in graphs can be helpful as graphs are enormous and carries a lot of knowledge. Problems such as link prediction and triple classification are used for graph completion, content recommendation, and question-answer systems. Triple classification determines whether a link missing is true or false [[24]](#ref-24) and is a binary classification task. There are other valuable areas of study like collective node classification [[25]](#ref-25) and link-based clustering [[26]](#ref-26) used to assign a label to two nodes according to its topology and structure of graph, which is useful for customer segmentation. The mapping of copied items can easily be dissected utilizing the concept of Entity Matching (EM) [[27]](#ref-27), which is principal to link information of similar real world entities and helps in knowledge refining. It is an active research area and considered a significant advance to perform downstream tasks like entity linking, triple classification, and many more.

This work focused merely on knowledge graph completion (KGC) to generate the ranking of missing relationships. It involves two subtasks: entity ranking and relationship prediction. The entity ranking problem is responsible for discovering missing elements, given ? as a missing connection or entity, anticipate*e*1 given (?,*r*, *e*2) or *e*2 given (*e*1,*r*, ?) in contrast to relation prediction problem to rank the missing connection, foreseeing *r* given (*e*1, ?, *e*2). The main objective consists in using the facts and relations given in KG as an aid to increase the probability of finding the missing elements. For example, the relationship between a person element and a country element can be easily dissected by knowing a person's neighborhood and the country that city is located in.

Several approaches exist to tackle the challenging problem of link prediction. The decomposition based method maps the given entities, links them to tensors, and provides expected semantic data [[28]](#ref-28). The path based approaches, including earliest random walks and path ranking algorithm (PRA) [[29]](#ref-29), potentially include a path between destinations through a sequence of edges. In particular, these models experience low proficiency, versatility and may consist of numerous parameters making models computationally costly to prepare. Knowledge Graph Embeddings (KGE) have been proposed to handle the aforementioned challenges and acquired huge consideration recently [[30]](#ref-30). The aim is to extract meaningful knowledge, i.e., entities and relations from a given knowledge graph, and install them into a continuous low dimensional vector space to perform downstream tasks like KGC, triple classification, entity resolution, collective node classification, and so forth. More importantly, it works on the intricacy and improves scalability while safeguarding the intrinsic construction of graphs.

The KGE models are mostly categorized into three different types of models namely, translation, semantic, and neural network based. Models such as TransE [[31]](#ref-31), TransH [[32]](#ref-32), TransR [[33]](#ref-33), TransD [[34]](#ref-34), TranSparse [[35]](#ref-35) are common examples of translation based approaches. DistMult [[36]](#ref-36), RESCAL [[37]](#ref-37), CompleX [[38]](#ref-38) belong to the semantic-based methods. These models are good yet fail to provide deeper semantics, ignoring hierarchical associations. Contrary to previ-

![Image Description: This diagram is a knowledge graph illustrating relationships between entities. Nodes represent entities (e.g., John, Company, Person, City) and edges depict relationships (e.g., "works in," "is a," "nationality is"). The graph shows how various entities connect, demonstrating a semantic network within a specific domain, likely used in the paper to explain a knowledge representation or reasoning system. Solid and dashed lines likely indicate different types of relationships.](_page_3_Figure_0.jpeg)

**Figure 2:** An example of hypothetical knowledge graph for knowledge graph completion. Red dotted line represents potential links.

ous techniques, neural based methods such as ConvKB [[39]](#ref-39), ConvE [[40]](#ref-40), HypER [[41]](#ref-41) generate state of the art (SOTA) performance by employing deep learning structures assessing temporal features, path, and structural information that helps produce better embeddings for downstream tasks.

## 1.1. Related Works and Contributions

There exists several surveys available for Knowledge Graph Completion. Wang et al. [[42]](#ref-42) provide a review of KGE techniques for link prediction and compared the analysis between the performance of different models. Similar work was done by Dai et al. [[43]](#ref-43) to conduct a thorough analysis by manually training the KGE models. They likewise surveyed the works that leverage extra semantic data dependent on text-based features and relation paths. Both surveys focused more on overseeing a comparative analysis by conducting experiments on standard datasets. When looking at research papers on KGE for link prediction, a mere disconnection between the state-of-the-art techniques reported in articles and the techniques actually employed in some related applications has been noticed. So, we focused more on delivering practical postprocessing techniques for comparative analysis such as hyper parameter tuning, calibration techniques [[44]](#ref-44) and Neighborhood Inconsistency Matrix [[45]](#ref-45) that helps connect fellow researchers to identify the recent works with more dimensions. Taking one step forward, a brief overview of graph representation learning methods based on traditional statistical learning methods, graphbased features methods, graph neural networks [[46]](#ref-46) are also discussed in this work.

Papers by Chen et al. [[5]](#ref-5) and Ji et al. [[4]](#ref-4) are most up-to-date survey papers on Knowledge Graph Completion and Representation. Chen et al. [[5]](#ref-5) briefly discussed the advantages and disadvantages of KGE models and provides an overview of KGC based on Network Representation Learning. Ji et al. [[4]](#ref-4) reviewed the knowledge graphs for representation, acquisition, and their applications. They covered the broad spectrum of knowledge graphs in terms of KGC, relation extraction, and entity classification. However, both these papers lack the studies to leverage multimodal Knowledge Graphs. We, therefore, attempt to give a survey of methods on KGE strategies, including not only on the single facts alone but also on KGs that further leverage multimodal information such as images, text, and timestamps [[47]](#ref-47). More importantly, we present how learned embeddings can be applied to an advantage over a wide assortment of applications. Rossi et al. [[48]](#ref-48) ordered models into three classifications: mathematical models, tensor decomposition models, and neural network models. They chose standard models for point-by-point depiction, experimental result comparison, and analysis for these three classes. Nonetheless, there is no general grouping and outline of the KGE models proposed lately in this paper, and the chosen models are not many, which cannot cover a wide range of KGE models. In addition, reinforcement learning techniques to model complex QA systems are reviewed in Section 4.

Real-world knowledge comprises multimodality such as images, text and timestamps. Leveraging literals in KG is a challenging task [[47]](#ref-47). Gesese et al. [[49]](#ref-49) conducted a survey on KGE for multimodal knowledge graphs, in which they covered models such as KBLRN [[50]](#ref-50), LiteralE [[51]](#ref-51), and many more. An overview of existing techniques related to multimodality, including temporal and uncertain knowledge graphs, is also conducted in our survey providing readers a comprehensive view on KGC. Most of the works focus on providing applications related to Knowledge Graphs. Abu-Salih et al. [[52]](#ref-52) surveyed domain-specific KG to give readers a thorough review of the state-of-the-art approaches drawn from academic works relevant to different knowledge domains. Zou et al. [[53]](#ref-53) conducted a bird's eye view on applications stemming from different domains like Question answering and recommendation systems. Taking their work forward, we also included the applications of knowledge graphs in the context of COVID-19, healthcare informatics, drug discovery, human resource and knowledge protection.

To the best of our knowledge, no past examination gives an orderly survey of the software libraries that revolves around Knowledge graph embeddings. As a result, unlike other related works that focus on KG development, this work aims to provide the first survey on these software ecosystems available for KGE training to perform downstream tasks. This paper likewise points to significant progress in applying knowledge graphs to available open research challenges, such as robustness, interpretability, scalability, and few-shot learning, and many more.

We provide readers with a bird's eye view on understanding the concepts required for the KGE model, and include a survey of SOTA KGE methods with the most recent patterns. This survey additionally goes deeper into the flow of KGE and provides a full-scale view of the KGE pipeline, including loss functions, scoring functions, negative generation, evaluation metrics, and auxiliary information for downstream tasks such as Link prediction.

The following are the notable contributions:

*   Apparently, this is one of few endeavors to provide a beginner-friendly comprehensive review that covers all aspects related to knowledge graph completion. The scoring models are separated into three general classifications: translation-based, semantic matching based, and neural-based to make this review readers friendly.
*   A high perspective is given on traditional relational learning and graph representation learning techniques that help new researchers to effectively understand research work from both traditional and non-traditional perspectives.
*   Each of the steps identified with the construction of the KGE model are explored to perform downstream tasks, including the scoring function, loss function, negative generation, and optimization.
*   We examined the recent developments made in reinforcement learning techniques for KGC to infer complex queries.
*   The KGE based on utilizing real world knowledge including numeric values, text, images, uncertain and temporal information, for link prediction is reviewed.
*   A Comparative analysis of open software libraries is analyzed for training knowledge graphs to perform downstream tasks.
*   We explored the open research challenges such as robustness, scalability, few shot learning, knowledge transfer, multi-path predictions that help direct future examination.
*   Different use cases identified with KG are mentioned in the context of question answering, recommendation, information retrieval, COVID-19, etc., to help readers understand the real-world applications.

This study has nine segments and is organized as follows: Section 2 outlines traditional relational learning and graph representation learning techniques. Section 3 examines existing knowledge graph embedding models for link prediction. Section 4 contains a comparative analysis of various methodologies for KGC. Section 5 review the reinforcement learning techniques for KGC. Section 6 incorporates techniques to leverage multimodality in knowledge graphs for KGC. Section 7 aims to give concise information on open-source software libraries for executing KGE models for link prediction. Section 7 examines a few applications identified with the Knowledge Graph. Section 8 contains open research challenges. Lastly, we conclude this study in Section 9.

## On Relational Learning and Representational Learning

This section discusses an overview of traditional statistical relational learning and graph representation learning methods for the task of link prediction. This will help fellow researchers to develop a good understanding of problem statement from traditional and non-traditional perspectives.

## 2.1. Traditional Relational Learning

The realm of statistical relational learning is quite an established field [[54]](#ref-54). There are several techniques proposed over the years that are widely used to predict new links from facts. However, the design logic and techniques used are quite different compared to the current state of art models. It is important to know that these methods exist, for example, similarity-based methods [[55]](#ref-55), inductive logical programming [[56]](#ref-56), rule mining [[57]](#ref-57), graphical models such as bayesian and markov logic networks [[58]](#ref-58).

## 2.1.1. Similarity Based Methods

Techniques that incorporate similarity based features originally centered around the topological construction of graphs are the most straightforward and traditional link prediction practice [[55]](#ref-55). Similarity based methods are broadly utilized for predicting the missing links in graphs that consist of only one connection, for example; in science (associations between protein), social networks (friend recommendation), web mining (hyperlinks between web destinations). It works by assigning a comparability score between node pairs using the underlying topology of the graph. The tendency behind this approach is that entities are probably being connected if they are similar and can be measured by the locality of nodes or by the presence of walk between nodes. It can be researched under three principal classifications: local [[59]](#ref-59), global [[60]](#ref-60), and quasi local methodologies [[61]](#ref-61). Local similarity based techniques, for example, Academic Adar index [[62]](#ref-62), Jaccard Index [[63]](#ref-63), Salton Index [[64]](#ref-64), Common Neighbors [[65]](#ref-65) infer the closeness or similarity of entities from their outright number of neighbors. They are quick to implement for single connections and scale well to enormous information graphs as their calculation relies just upon the neighborhood of the participating entities. They can however be too restricted to even consider catching significant patterns and may not show long range dependencies. As opposed to local, the global similarity methods [[60]](#ref-60) utilize the entire structure of the graph to rank the similitude between nodes even if the nodes are slightly further. In spite of the fact that the entire topology of the graph gives greater adaptability in prediction, it likewise expands the computational time since a fusion of all paths between nodes is incorporated. Some common examples include Katz Index [[66]](#ref-66), SimRank [[67]](#ref-67), Rooted PageRank [[68]](#ref-68), Random Walk with Restart [[69]](#ref-69). The compromise between the proficiency of the data with respect to the entire graph topological design (global methodologies) and reduced time based methods (local similarity) approaches have brought about the rise of quasi local similarity based methods [[61]](#ref-61). Semi neighborhood similarity examples include Local Path Index [[70]](#ref-70), FriendLink Index [[71]](#ref-71), Superposed and Local Random Walks [[72]](#ref-72). It attempts to adjust computational logic and precision by determining the likeness of entities from random walks and paths of limited length. A portion of these methods may leverage the entire topology of the graph still the complexity is lesser than global similarity based methods.

## 2.1.2. Rule Induction and Reasoning

Taking in rules from KGs is a significant errand for link prediction, cleaning and classification. "Rules over graphs are of the structure head ← body, where head is a binary atom and body is a combination of possibly negated binary and unary atoms" [[73]](#ref-73). It can be utilized to recognize noticeable examples from KGs and cast them as Horn rules. The objective of Inductive Logic Programming (ILP) [[56]](#ref-56) is to sum up individual examples within the sight of background information by building speculations about unseen occurrences. Background information is considered as a cluster of triples or facts over different relations and rules that can be utilized to actuate the meaning of a logic program. The most general task in ILP is the task of learning sensible meanings of relationships. In particular, the conventional ILP assignment of gaining from both positive and negative instances is called learning from entailment. ALEPH is an ILP method that takes in rules using inverse entailment [[74]](#ref-74). A portion of the common models for Horn and non monotonic principle enlistment are CIGOL [[75]](#ref-75), CLINT [[76]](#ref-76), LINUS [[77]](#ref-77), GOLEM [[78]](#ref-78), ILASP [[79]](#ref-79), ILED [[80]](#ref-80). Most of the traditional existing style standard rule induction strategies referenced above accept that the given information to which the rules are actuated is absolute, representative and precise. Accordingly, they depend on notions of closed world assumptions and are intended to mine rule hypotheses that fulfill inductive learning from instances. However, KG are exceptionally deficient, biased and error prone implying that the assignment of initiating an ideal rule set from a KG is ordinarily unworkable. Therefore, with respect to KG, one regularly aims to remove some generalities from the information, which is generally not true, when viewed as rules that a substantial portion of the confirmed facts are inferred.

The most conspicuous instances of such frameworks (rule mining) that are explicitly custom fitted towards prompting Horn rules from KGs are AMIE [[81]](#ref-81) and RDF2Rules [[82]](#ref-82). AMIE receives the PCA proportion of certainty and assembles rules in a hierarchical design beginning with rule heads like →?*x nation* ?*y*. For each rule on top of this structure (one for each edge name), three kinds of refinements are thought of adding dangling atom, instantiated atom and closing atom. It intends to augment another edge to the body of the rule. The execution of AMIE utilizes an assortment of procedures from the database region, which permit it to accomplish high scalability. While AMIE mines one rule at an instant, RDF2Rules parallelize this interaction by mining frequent predicate cycles (FPC). To separate FPCs, the RDF2Rules initially extract the frequent predicate paths (FPP). As soon as FPC are extracted, rules are then mined from them by picking a predicate to be in the rule head, and gathering the rest into its body. RDF2Rules is fit for representing unary predicates which are disregarded in AMIE for scalability issues. RDF2Rules plays out the standard extraction quicker than AMIE because of a viable pruning procedure utilized during mining FPC however the supported rule rationale is more prohibitive. An advantage of rule based mining approaches is that they are viably interpretable as some logical rules are given to the model.

## 2.1.3. Probabilistic Graphical Models

A probabilistic or graphical model [[58]](#ref-58) signifies the conditional independent structure for a graph between nodes. These models leverage the benefits of adaptable topological design, clear semantics and viable multi-data combination in managing complex issues. Graphical models infer a basic method to envision the construction of a probabilistic model and can be utilized to plan and propel new models. In a probabilistic graphical model, every node addresses a random variable, and the connections between them express probabilistic relations. The graph then, at that point, catches the paths by which the joint appropriation over the entirety of the nodes can be broken down into a product of elements relying just upon a subset of the random variables. The link prediction methods dependent on the graphical models generally utilizes Bayesian [[83]](#ref-83) and Markov logic networks [[84]](#ref-84).

Bayes' rule incorporates four different types of models namely, network evolution [[85]](#ref-85), stochastic models [[86]](#ref-86), structural models based on hierarchy [[87]](#ref-87) and local probabilistic based methods [[88]](#ref-88). The main downside of a portion of these models is in effect sluggish and computationally expensive for enormous graphs [[89]](#ref-89). In contrast to a bayesian network, which incorporates Directed Acyclic Graph (DAG), the Relational Markov Network (RMN) is likewise proposed [[90]](#ref-90) based on an undirected graph. RMN addresses two drawbacks of Bayesian networks that is they do not compel the graph to be non cyclic, which takes into account different conceivable representations of graphs. Moreover, they are more appropriate for discriminative modeling [[91]](#ref-91). There also exists other methods for solving the KGC. "The DAPER model is a DAG sort of probabilistic entity relationship model [[92]](#ref-92)". The benefit of the DAPER model is to provide more expressivity than the previously mentioned approaches [[93]](#ref-93).

The manual feature extraction techniques that are explored in this study furnish a beginning stage to the efficient prediction of absent and future links accessible through learning the powerful characteristics in graphs. Among these powerful highlights for KGC, utilizing the structural features that can be mined from the graph is the stepping stone of all learning-based KGC techniques. The issue with manual feature extraction is generally that they are restricted in adaptability and for KG we need techniques that scale better given the size of the graph. Another drawback is that they have restricted model power unlike KG Embeddings and are not differentiable and cannot utilize current GPU designs with SGD learning. Other than the topological qualities, some machine learning based models may utilize the nodes with the domain explicit characteristics, alluded to as the proximity and accumulated features [[94]](#ref-94) [[95]](#ref-95).

## 2.2. Graph Representation Learning

While traditional machine learning models for KGC rely on hand-crafted feature engineering (as shown in figure 3), advances in graph representation learning (GRL) models have led to the introduction of automatically generated feature encoders, which prevent hand-designed features that forestall hand-designed attributes [[96]](#ref-96). In simple words, GRL represents an area of study to apply machine learning on graphs, but avoid extracting features manually as they are difficult and time consuming on graphs.

![Image Description: The image is a flowchart comparing two approaches to graph prediction. The top row depicts manual feature engineering: an input graph is processed via handcrafted features and a feature mapping to generate predictions. The bottom row illustrates graph representation learning: an input graph undergoes automated feature generation and feature mapping for prediction. The flowchart highlights the shift from manual to automated feature extraction in graph-based prediction tasks.](_page_8_Figure_0.jpeg)

**Figure 3:** Manual Feature Engineering versus Graph Representation Learning

The graph representation or graph embedding based learning models learn and encode graph features with nodes into low dimensional space. It can be trained incorporating dimensionality reduction [[97]](#ref-97) and neural networks. The utilization of GRL prompted the improvement of cutting edge language models like dialogue systems, relation prediction and natural language understanding. Existing well-known and standard models such as CNN [[98]](#ref-98), RNN [[99]](#ref-99) and Word2Vec [[100]](#ref-100) can be employed. However, these models are generally used for grids (in case of CNN) and sequences (in case of RNN). In addition, graphs are more complex due to no spatial locality, no fixed ordering and an isomorphism problem [[101]](#ref-101) which is one of the most critical aspects when designing an architecture. Graphs therefore tend to be more connected and complex. It may also contain multimodal knowledge like nodes representing concepts, text, numbers and timestamps that further adds to the complexity. We need specific models tailored to graphs only. Due to this researchers came up with graph representation that is learning representation of nodes and edges to turn facts into vector representations. Feeding the graph to a vector space is called encoding. The reproduction of the graph neighborhood from the embeddings represents decoding. The vital advantage of the encoder-decoder structure is that it permits to concisely characterize and analyze diverse modeling strategies dependent on the similarity values, loss and decoder function [[102]](#ref-102).

## 2.2.1. Graph Feature Based Methods

One method of reviewing the encoder decoder approach is according to the viewpoint of matrix factorization. Of course, the test of interpreting local neighborhood structure from vector space of nodes is firmly identified with rebuilding items in graph adjacency matrix. We can see this approach as utilizing factorization of matrix to gain proficiency with a low-dimensional estimation for a node to node similarity matrix M, where S sums up the adjacency matrix and gains concepts of similarity between nodes. The fundamental reason for employing matrix factorization based techniques is to diminish the dimensionality while likewise preserving the locality and nonlinearity of the graph. Nonetheless, the global structural information may be lost. SVD (Singular Value Decomposition) is commonly used because of its realization in the low-position approximation [[103]](#ref-103).

Later works frequently employ decoders based on the inner product (e.g. graph factorization (GF) [[104]](#ref-104) and HOPE [[105]](#ref-105)) on the assumption that the closeness between two nodes (the cover between their nearby areas) is relative to the dot product of their embeddings for link prediction. The Graph factorization model works by limiting the quantity of adjoining nodes for cutting the graph, as opposed to applying edge cuts. HOPE is centered around modeling and representing directed graphs on the premise that directed relations can address any type of graph. For directed graph embeddings, HOPE also features the asymmetric and transitive properties. It additionally upholds traditional similarity based methods such as common neighbors (CN), academic adar index (AAI), katz index (KI) and rooted pagerank (RPR).

The objective of GF techniques is to learn embeddings for every node to such an extent that the inner product between the vectors of the learned embeddings approximates some deterministic proportion of the overlap between their local neighborhood areas. Late years have seen a flood in productive techniques that adjust the inner product technique to deal with utilization of stochastic proportions of node similarity. A vital advance in these methodologies is that the node embeddings are upgraded so that two nodes have comparable embeddings if they can coexist on a short random walk. DeepWalk [[106]](#ref-106) and node2vec [[107]](#ref-107) employ a shallow embedding technique and an inner product decoder. The key difference in these techniques is how they portray the concepts of similarity between nodes and neighborhood remaking. Instead of directly remaking the adjacency matrix, they forward embeddings to encode the measure of the random walk. To generate random walk embeddings, the overall methodology is to use decoders and limit the cross entropy loss. However, easily estimating the cross entropy loss can be computationally expensive.

There are various systems to conquer this computational test and this is one of the fundamental contrasts between the DeepWalk and node2vec methods. DeepWalk utilizes a progressive softmax to inexact cross entropy loss which includes incorporating a binary tree design to speed up the calculations whereas node2vec employs a noise contrastive technique with the approximation of normalizing factor utilizing negative facts. The node2vec approach likewise separates itself from the prior DeepWalk calculation by considering a more adaptable meaning of random walks. To be specific, DeepWalk utilizes random walks consistently to characterize the operation of decoder whereas the node2vec algorithm presents hyper parameters that permit the random walk probabilities to easily add between walks that are more likened towards the BFS or DFS on the graph. A change to the node2vec variation, graph2vec basically focuses on how to properly embed a subgraph from a graph [[96]](#ref-96).

Dissimilar to the aforementioned strategies, SDNE (Structural deep network embedding) [[94]](#ref-94) does not utilize random walks. It attempts to gain information from two particular measurements namely first order proximity and second order proximity. In the former approach, two nodes are considered comparable in the event that they share an edge whereas in the latter one, they are considered related if they share many adjoining or nearby nodes. The objective is to catch deep non linear patterns. The first order proximity is preserved using a graph dimensionality reduction algorithm namely laplacian eigen maps [[97]](#ref-97) whereas second order proximity is preserved by utilizing an unsupervised autoencoder that contains reconstruction loss function to minimize. Both loss functions are then jointly minimized to obtain graph embedding.

LINE [[95]](#ref-95) also adopts the similar methodology by defining first and second order proximity. Its main functionality is to decrease the range of the distinction between the input and embedding distributions and is accomplished by utilizing KL divergence [[108]](#ref-108). It generates two probability distributions (adjacency matrix and dot product) for each pair of nodes and decreases the KL divergence. The main drawback of this approach is that it does not perform well overall if the application requires insights relating to node neighborhood structure. This is because it needs to mark new functions for each extended sequence of proximity.

One method worth mentioning is HARP [[109]](#ref-109) which improves the performance of the walking and embedding based techniques mentioned above. Due to the non-convex based objective functions in the previous models, they can be trapped in local optima (as shown in figure 4) and therefore reduce performance. HARP on the other hand preprocess the graph using coarsening techniques to accumulate associated nodes into super nodes. In any case, it is important to

![Image Description: The image contains two 2D graphs illustrating different optimization scenarios. (a) shows a single, global minimum represented by a parabola with a yellow sphere at its vertex. (b) depicts a more complex function with multiple local minima and maxima, indicated by yellow spheres at the lowest points of each curve section. The graphs likely illustrate the difference between simple and complex optimization problems.](_page_10_Figure_0.jpeg)

**Figure 4:** (a) Convex (b) Non Convex

understand that shallow embedding approaches experience the negative effects of some significant disadvantages. The first issue is that they do not share the parameters among nodes in the encoder, since it straightforwardly processes a unique embedding vector for every node. This absence of parameter sharing is computationally and statistically expensive. A subsequent major drawback that questions the shallow embedding approaches is that they don't have the ability to utilize node features in the encoder. The shallow embedding based techniques can create embeddings for nodes that were available during the preparation stage only. Creating embeddings for new nodes (after training stage) is not possible except if extra processing steps are performed to gain proficiency with the embeddings for these nodes. These limitations forestalls shallow embeddings from being utilized on inductive applications [[102]](#ref-102), which include summing up to hidden nodes subsequent to training. To mitigate these restrictions, shallow encoders can be substituted with more refined encoders like graph neural networks [[46]](#ref-46) that depend for the most part on the structure and properties present in the graph.

## 2.2.2. Graph Neural Networks

The overall idea of graph neural networks was introduced in [[46]](#ref-46), however various neural network based models have been introduced for inferring multi relational representation. Learning from subgraph, entities and attributes (SEAL) [[110]](#ref-110), exploit graph neural networks to learn structural and latent information in graphs for link prediction. It works by preparing the features from local enclosing subgraphs for each target link and feeding it into GNN to predict the missing links. HetGNN [[111]](#ref-111) on the other hand takes into account heterogeneous networks and begins random walk with restart methodology and tests a fixed size of associated heterogeneous neighbors to cluster them dependent on type of nodes. In this way, the neural network design with two modules is used to aggregate the feature data of the adjacent vertices examined. The first module is responsible to inherit the content vector space for every vertex; on the other hand, the aggregate of content embeddings generated is completed by the second module. HetGNN then ensembles the generated outputs to acquire the ultimate embedding.

The GNN's are further classified into types such as GAE (Graph AutoEncoder) [[112]](#ref-112) and VGAE (Variational GAE) [[113]](#ref-113) (for example GCMC [[114]](#ref-114) and ARGA [[115]](#ref-115)) aim to leverage unsupervised learning to become familiar with node representations in a graph. GAE can train with the structural features in graphs while exploiting neural networks, and lessen the graph dimensionality as per the quantity of channels of the autoencoder covered up layers [[116]](#ref-116). Moreover, GAE based models can install the entities to two dimensional vectors with assorted range. This advantages the auto-encoders exclusively to accomplish superior performance for evaluating over the obscured node embeddings, in addition to combining the characteristics of node to further enhance the predictive power [[102]](#ref-102).

The representation procedures that depend on GNN consider both structural information and

![Image Description: The image is a flowchart depicting a graph neural network architecture. An input graph is processed through sequential layers: a lookup layer, a scoring layer, and a loss layer. A negative generation module feeds into the lookup layer. The final output feeds into downstream tasks. The diagram illustrates the data flow and processing steps within the model.](_page_11_Figure_0.jpeg)

**Figure 5:** A bird's eye view on knowledge graph embedding pipeline

node attributes; however, they experience the effects of high complexity and shortcoming in recursive refreshing of the hidden states. Besides, GNN exploits identical boundaries for all layers, which restricts their adaptability. Taking advantage of convolutional neural networks (CNNs), GCNs lead to flexibly deriving features from complex graphs. The iterative combination of a node locality is leveraged by GCN to acquire graph embeddings. Here the accumulation technique prompts higher versatility other than learning global neighborhoods in graphs. Moreover, GCNs can also be used for subgraph embeddings [[117]](#ref-117).

GraphSAGE [[118]](#ref-118) is one of the earliest models that aggregates the data from nearby neighborhoods iteratively. This recursive feature may generalize the model to hidden nodes. The nodes ascribed for this model may incorporate basic node measurements, like node degrees, literary information for profile data or for online social graphs. RGCN (Relational Graph Convolutional Networks) is introduced in [[119]](#ref-119) with the aim to predict the missing links for relational data types utilizing GCN. This model is not quite the same as would be expected GCNs as the aggregation of features vectors of adjoining nodes are specific to relations. The errand of link expectation by this model can be seen as processing representation of nodes with a RGCN encoder and employing DistMult factorization [[36]](#ref-36) as the scoring capacity. We talk about different GCN based strategies for KGC in Section 3.3.3.

## Knowledge Graph Embeddings

KGE are models that attempt to learn the embeddings, i.e., vector representation of nodes and edges, by taking advantage of supervised learning. They do that by projecting entities and relationships into a continuous low dimensional space. These vectors have a few hundred dimensions which suggests memory efficiency. A vector space in which each point represents a concept and the position in the space of each point is semantically meaningful, similar to word embeddings. Examples of KGE models include RESCAL [[37]](#ref-37), TransE [[31]](#ref-31), DisMult [[36]](#ref-36), ComplexE [[38]](#ref-38), HolE [[120]](#ref-120), ConvE [[40]](#ref-40), RotatE [[121]](#ref-121) and many more. All these competing models try to achieve a goal by learning a meaningful set of embeddings by maximizing the chance of predicting a test set of missing links. An ideal KGE model should be expressive enough to catch KG properties, for example, symmetric, asymmetric, inversion, and composition, that address the ability to represent distinctive logical patterns for relations [[121]](#ref-121).

Definition 1. *Symmetric Relation: A relation R is symmetric if* ∀*e1, e2: (e1, R, e2)* → *(e2, R, e1).*

*For Example: e1* = *John and e2* = *Peter and R* = *"is brother of"; (e1, R, e2)* = *John is brother of Peter* → *(e2, R, e1)* = *Peter is brother of John.*

Definition 2. *Asymmetric Relation: A relation R is antisymmetric if* ∀*e1, e2: (e1, R, e2)* → ¬*(e2, R, e1)*

*For Example: e1* = *John and e2* = *Peter and R* = *"is a supervisor of"; (e1, R, e2)* = *John is a supervisor of Peter* → *(e2,* ¬*R, e1)* = *Peter is not a supervisor of John.*

Definition 3. *Inverse Relation: A relation Ri inverse to relation Rj if* ∀*e1, e2: Rj(e1, e2)* → *Ri(e2, e1).*

*For Example: e1* = *John, e2* = *Peter, Ri* = *"is a supervisor of" and Rj* = *"is a student of"; (e1, Ri, e2)* = *John is a supervisor of Peter* → *(e2, Rj, e1)* = *Peter is a student of John.*

Definition 4. *Composite Relation: A relation Ri is composed of relation Rj and relation Rk if* ∀*e1, e2, e3 : (e1, Rj, e2)* ∧ *(e2, Rk, e3)* → *(e1, Ri, e3).*

*For Example: e1* = *John, e2* = *London, e3* = *United Kingdom, Rj* = *"is born in", Rk* = *"is capital of", Ri* = *"is from"; (e1, Rj, e2)* = *John is born in London* ∧ *(e2, ,Rk, e3)* = *London is capital of United Kingdom* → *(e1, Ri, e3)* = *John is from United Kingdom.*

Considering KG properties helps differentiate the representation limits of KGE decoders. Although we cannot infer that these patterns should hold precisely in practice, there might be numerous relations that show these examples to a certain extent. For instance, symmetric relations hold more than 90% of the time. Table 1 reproduced from [[121]](#ref-121) sums up the capacity of the different decoders to encode the aforementioned KG properties. KGE models ought to likewise show hierarchies, type constraints, transitivity, homophily, and long range dependencies. A good embedding should model these properties as best as possible while keeping a good tradeoff upon expressivity, scalability, and time to train a model.

A bird's eye view on learning the multi relation embeddings comprises various stages, as given in figure 5. To start with, the embeddings of both the entities and relations are first introduced utilizing random noise. These generated embeddings are then used to assign a score for correct and incorrect facts by employing a scoring function that learns their interaction. The embeddings are then updated using the optimizer function to limit the loss on the triples scored. During KGE training, we are basically learning how to place vectors in an embedding space. The main task is to provide a maximum score for correct facts and less score for negative facts.

**Table 1:** A Comparison of KGE models in terms of capturing relation types [[121]](#ref-121)

| Model | Symmetry | AntiSymmetry | Inversion | Composition |
|---|---|---|---|---|
| SE | False | False | False | False |
| TransE | False | True | True | True |
| TransX | True | True | False | False |
| DistMult | True | False | False | False |
| CompleX | True | True | True | False |
| RotatE | True | True | True | True |

## 3.1. Embedding Lookup Layer

This layer is responsible for mapping the one hot encoding vector to embedding vectors. The one hot vector represents a discrete sparse vector addressing an input. For a triple (e1, R, e2), three one-hot encoding vectors are required to map e1, R, e2, respectively. The embedding vector, on the other hand, is a low dimensional space containing semantically meaningful associations. It reduces the sparsity and leads to productive distributed representations.

## 3.2. Negatives Generation

An important step in training the KGE model is negative generation, which researchers have not fully emphasized in recent years. However, attempts have been made to fully exploit and generate corruption to help rectify scalability issues. There are two general assumptions, i.e., closed world assumption (CWA) and open world assumption (OWA). In CWA, the absence of a fact means that it is necessarily false, whereas, in the case of OWA, the absence of fact does not indicate that the fact is false. Knowledge graphs operate under the open-world assumptions that means that if we process knowledge bases such as DBpedia [[6]](#ref-6) does not have false facts in it. The task of link prediction requires training models with false facts that can separate the true facts from them. Therefore, the CWA [[122]](#ref-122) is used to assume that the KG is only locally complete. To avoid insignificant predictions from the embedding, a complete set that includes all the corrupted facts should be handcrafted. Then, while reflecting on calculation cost and memory space, stochastic preparation is required at each step. In particular, to train KGE whenever we get a positive fact, we need to test some corrupted triples from its related negative sampling set. When generating corruptions under the CWA assumptions, we always try to corrupt either the subject or the object, as given in the equation below:

Corrutions = {
$$
(s', p, o)|s' \in E
$$
} $\cup$ {( $(s, p, o')|o' \in E$ } (1)

Here s' and o' represents corrupted subject and object. It is worth noting to mention some negative sampling techniques [[123]](#ref-123) such as uniform sampling [[31]](#ref-31), Bernoulli sampling [[32]](#ref-32), KBGAN [[124]](#ref-124), IGAN [[125]](#ref-125), NSCaching [[126]](#ref-126).

Uniform sampling [[31]](#ref-31) refers developing negative triples by substituting the tail or the head entity of a positive triplet with the element arbitrarily tested from the entity set by the uniform distribution. Nonetheless, this sampling technique develops directly classified triplets that do not contribute to providing meaningful and important knowledge [[121]](#ref-121) [[126]](#ref-126). Thereafter, as the preparation progresses, a large proportion of the tested negative triples obtain very low scores and almost zero gradients, hindering the preparation of the embedding model after just a few cycles of recurrence. One more extreme downside of uniform sampling is generating facts that appear negative when they should not. Subsequent to supplanting the head in (KamalaHarris, Gender, Female) with NikkiHaley, (NikkiHaley, Gender, Female) is verified truth. To lighten this issue, Bernoulli sampling [[32]](#ref-32) was proposed substituting head or tail elements with various probabilities as per the mapping property of relationships. Nonetheless, for relations with less information, it neglects to foresee the missing facts among semantically potential choices even after many epochs of training. Probabilistic negative examining [[127]](#ref-127) speeds up the most common way of producing negative triples by acquiring a train bias tuning boundary that decides the likelihood by which the created negative facts are supplemented with early-recorded potential examples. To resolve the issue of simple negatives, self adversarial sampling was proposed [[121]](#ref-121), which gauges each inspected negative as per its likelihood beneath the embedding models. On the other hand, the literature [[128]](#ref-128) [[125]](#ref-125) proposed sampling techniques leveraging Generative Adversarial Networks (GANs) [[129]](#ref-129) that are powerful and effective but expensive to formulate and require black-box evaluation methods, and are not interpretable. In contrast to the aforementioned GAN-based strategies, one rich methodology that uses fewer boundaries and is simple to prepare is NSCaching [[126]](#ref-126), which includes employing a cache or reserve of strong negative triples with high scores.

## 3.3. Scoring layer

The scoring layer interacts with the loss function. A scoring function (*fr*(*h*, *t*)) assigns a score to a triple (s, p, o). The higher score represents a higher probability of the triplets being true facts. There are several ways to design a scoring function. Some functions determine a model that scales better than others, and some are designed to capture properties in KG such as symmetry, asymmetry, homophily, etc. The three main categories of scoring functions for the KGE model, i.e., translation, factorization, and neural networks, are discussed in the following subsections.

## 3.3.1. Translation Models

Since the advent of the word embedding model, word2vec [[100]](#ref-100), a lot of progress has been made to embed the representation learning in a distributed manner. Researchers are attempting to explore the interesting translation invariance phenomenon generated by the word2vec model. In simple words, the vector space generated by word2vec contains intrinsic semantically meaningful examples that can help capture the properties of facts for a better representation space. For example, Man is semantically related to a Male, whereas Woman is semantically related to a Female. Inspired by the word2vec model, TransE [[31]](#ref-31), a translation-based knowledge graph embedding model is proposed to capture the translation invariance phenomenon in multi-relational graphs. The principle thought behind adopting this approach is to acknowledge the most general and interpretable way of discovering legitimate triples as the translation activity of elements, characterizing the scoring function, and afterward limit the loss function to become familiar with the embedding of triples. TransE is responsible for modeling the entities (e) and relations (r) in uniform low dimensional continuous space Rd. As shown in figure 6, assuming the triple (h, r, t) is valid, the t generated is near the vector representation of h and r. As seen, TransE follows a mathematical principle given below:

$$
h + r \approx t \tag{2}
$$

![Image Description: The image is a vector diagram showing three vectors: **r**, **h**, and **t**, forming a triangle in two-dimensional space. The vectors originate from a common point at the origin of a Cartesian coordinate system. The diagram likely illustrates vector addition or decomposition within a physical or mathematical model presented in the paper. Vector **r** appears to be the resultant vector of **h** and **t**.](_page_14_Figure_6.jpeg)

**Figure 6:** TransE [[31]](#ref-31)

Here the triplet (h, r, t) consists of a head unit (h), tail unit (t), and the relation (r) between them, which are embedded in the vectors h, r, t. The scoring function of TransE is given in the equation below:

$$
f_r(h,t) = ||h + r - t||_{1/2}
$$
(3)

where *l*1/*l*2 are the norm constraints. The TransE has repeatedly shown good performance for large scale knowledge graphs. Nonetheless, it fails to effectively model the complex relations such as one to many, many to many [[33]](#ref-33). More specifically, assuming a one to many relation (i.e., for each head element, there are multiple tails elements associated with it) in which the ResearchArea depicts one to many relation between triplets (Ram, ResearchArea, Computer-Vision) and (Ram, ResearchArea, LanguageProcessing). The embedding vectors generated by TransE for ComputerVision and LanguageProcessing will be somewhat similar in the feature vector space. But this outcome is completely unreasonable on the grounds that ComputerVision and LanguageProcessing are entirely different fields.

Curbing the limitation of the TransE model, Ma et al. proposed TransH [[32]](#ref-32) to give different representation vectors to each entity depending on the relation. In other words, TransH works by issuing an entirely separate relation-specific hyperplane for each relationship so that the entities associated with it have different semantics only in the context of that relationship. As shown in Figure 7, for the entity embedding vectors h and t, TransH projects it to the hyperplane (relation specific) in the direction of mapping vector *W*r that gives the projection vector*h*^⊥^ and *t*^⊥^.

![Image Description: The image is a 2D vector diagram illustrating vector decomposition. Two vectors, **r** and **h**, are shown. **h** is decomposed into components parallel (**h~||~**) and perpendicular (**h~⊥~**) to **r**. A third vector **t** is also shown, likely representing a transformation or relation between **h** and **r**. Dashed lines form a parallelogram, visually representing vector addition and subtraction. The diagram likely serves to explain a geometrical or physical relationship between vectors within the paper's mathematical framework.](_page_15_Figure_2.jpeg)

**Figure 7:** TransH [[32]](#ref-32)

The score function of TransH is formulated as follows:

$$
f_r(h, t) = || h_\perp + D_r - t_\perp || \tag{4}
$$

Here *D*r represents relation specific translation vector,*h*^⊥^ and *t*^⊥^ follows the calculation approach given below:

$$
X_{\perp} = X - W_r^T X W_r \tag{5}
$$

where *W*r represents the normal vector of hyperplane that mentions*D*r. TransH to some extent solves the problem related to complex relations by modeling each entity to different representation vectors dependent on the relation. However, it still employs the same vector feature space,*Rd*, for representing the facts. In general, an entity may have multiple semantics, and the relations are centralized towards numerous aspects of the entity.

TransR [[33]](#ref-33) attempts to model the entities utilizing relation specific vector space. The relations are modeled as a vector r particular to relation space *R*s . As shown in figure 8, it operates by projecting the h and t from entity space (*Rd*) to relation specific space (*Rs*) generated by projected vectors *h*^⊥^ and *t*^⊥^. The scoring function is similar to that given in equation 4 but with *h*^⊥^ and *t*^⊥^ as follows:

$$
X_{\perp} = M_r X \tag{6}
$$

where *M*r is a projection matrix or mapping matrix generated by projecting entity vectors into relation specific space. Compared to TransE and TransR, TransR shows some competitive performance. However, it is also associated with limitations that need to be addressed. Without much trouble, one can understand that the semantics shared by the tail and head unit may be completely different. For example, triplet(John, research\_area\_is, computervision) in which the

![Image Description: The image is a diagram illustrating a transformation between "Entity Space" and "Relation Space." Two 2D Cartesian coordinate systems are shown. Gold arrows represent vectors 'h' and 't' in Entity Space, and 'h⊥' and 't⊥' in Relation Space, connected by a dotted line representing a transformation matrix 'Mr'. A gold arrow 'r' shows the result of the transformation in Relation Space. The diagram visually explains a linear transformation mapping entities to relations.](_page_16_Figure_0.jpeg)

**Figure 8:** TransR [[33]](#ref-33)

head entity John (person) is completely different from computervision (field of computer science). Nonetheless, in TransR, the projection matrix is the same for the head and tail unit for a particular relationship that directly impacts the predictive accuracy. It also suffers from high memory complexity because it creates a separate representation space for a relation that is not memory efficient.

TransD [[34]](#ref-34), an improvement of TransR, adopts a dynamic mapping matrix that effectively generates two separate mapping matrices for head and tail entities. It exploits two embedding vectors for the representation of each entity and relation. The first embedding vector is used to represent the semantics of entity and relations (r belongs to*R*s and h, t belongs to*Rd*). The second embedding vector (*R*m belongs to*R*s and*Hm*, *T*m belongs to*Rd*) is employed to generate two dynamic projection matrices (*M*h*, *M*t) as shown in figure 9. The scoring function is given in

![Image Description: The image displays a two-part diagram illustrating a transformation between "Entity Space" and "Relation Space". The left panel shows points (h1, h2, h3, t1, t2, t3) in the Entity Space. The right panel shows transformed points (h1r, h2r, h3r, t1r, t2r, t3r) in Relation Space. Two parallel arrows labeled "Mrhi" and "Mrti" represent the transformation matrices mapping entities to relations. The diagram visually depicts a linear transformation, likely used in a knowledge representation or relational learning context.](_page_16_Figure_4.jpeg)

**Figure 9:** TransD [[34]](#ref-34)

equation 4 with *h*^⊥^ and *t*^⊥^ follows:

$$
X_{\perp} = M_x X \tag{7}
$$

$$
M_x = R_m X_m^T + I_m \tag{8}
$$

where, *I*m represents the Identity matrix. TransD replaces the vector product and matrix operations with the vector product operation in the previous model. This improves the computation effectiveness marginally and addresses the excessive number of hyperparameters in the TransR model, making TransD reasonable for huge scope KGs.

Most of the aforementioned approaches failed to represent specific types of properties such as imbalance and heterogeneity. Heterogeneity indicates that some relations may have many connections to simple relations, which cause overfitting or underfitting (when the relationship is complex). On the other hand, the imbalance suggests treating the head and tail differently since there may be a high contrast present between them. To handle these issues, a TranSparse [[35]](#ref-35) embedding method is proposed which is divided into two parts namely share and separate version.

In TranSparse (share) method, the projection metrics are substituted by an adaptive sparse matrix*Mr*(*degr*). The idea is to replace the dense features with sparse features to tackle the nonuniform assortment of relations and entities and decrease the number of hyperparameters in the model simultaneously [[35]](#ref-35). The *deg*r represents the sparse degree dependent on the number of entities that are associated with relation r. Given scoring function in equation 4, the*h*^⊥^ and *t*^⊥^ follow:

$$
X_{\perp} = M_r (deg_r) X \tag{9}
$$

$$
deg_r = 1 - (1 - deg_{min})n_r/n_{r'}
$$
(10)

Here, *degmin*is a hyper parameter that lies between 0 and 1. And,*n*r represent the number of entities that are associated with relation with*n*r^0^ constitute the maximum of them. In TranSparse (separate) method, two sparse mappings are employed for projecting the head (*MrH*(*degrH*)) and tail (*MrT* (*degrT*)) separately for each relation. Given scoring function in equation 4, the*h*^⊥^ and *t*^⊥^ follow:

$$
X_{\perp} = M_{rX}(deg_{rX})X\tag{11}
$$

$$
deg_{rX} = 1 - (1 - deg_{min})n_{rX}/n_{rX'}
$$
(12)

To simplify the execution of the TranSparse embedding, the literature propose sTransE [[130]](#ref-130) that works by simply replacing the projection sparse matrix by mapping matrix. The projected vectors are extended as follows:

$$
X_{\perp} = M_{rX}X \tag{13}
$$

The aforementioned approaches merely focus on modifying projection vectors, mapping matrices, and embedding spaces. However, none of the techniques were taken advantage of in employing better optimization techniques to increase the predictive power of the standard TransE model. The TransA [[131]](#ref-131) model optimizes the TransE model by replacing the distance measure from the standard Euclidean distance to adaptive Mahalanobis distance as it provides more flexibility and adaptability managing complex relations. Given a nonnegative symmetric weighted matrix *M*r (with relation r), the scoring function of TransA is defined as follows:

$$
f_r(h, t) = (|h + r - t|)^T M_r(|h + r - t|)
$$
(14)

Other than permitting entities to possess different embedding when engaged with various relations, a different line of exploration augments TransE by weakening the overstrict prerequisite given in equation (2). The equation (15) represents the scoring function of TransM [[132]](#ref-132). It maps each triplet with weight particular to a relation Θ*r*. By allocating low weight to complex relations (i.e., one to many, many to many) it permits the tail entity to place afar from*h*+*r*.

$$
f_r(h,t) = -\Theta_r ||h + r - t||_{1/2}
$$
(15)

ManifoldE [[133]](#ref-133) employs the concept of hypersphere by relaxing equation(2) with Θ^2^ *r* for each triplet belonging to the set of all facts. With this, the tail entity can lie roughly on a hypersphere with a diameter of 2Θ*r*focused at h + r, instead of near the specific place of h + r. The score capacity is henceforth outlined as:

$$
f_r(h,t) = -(||h + r - t||_2^2 - \Theta_r^2)^2
$$
(16)

TransF [[134]](#ref-134) adopts a similar approach. Rather than upholding the precise interpretation given in equation(2), it expects the tail entity to place in the same direction of*h*+*r*, like *h*with*t*−*r*. The scoring function has to coordinate *h*+*r*with*t*as well as*t*−*r*with*h*,

$$
f_r(h, t) = (h + r)^T t + (t - r)^T h
$$
(17)

Recently, Xie et al. [[135]](#ref-135) proposed ITransF to reduce the data sparsity problem shown by TransE and STransE. They used the concept of sparse attention mechanism responsible for locating hidden concepts with statistical strength transfer through concept sharing. Besides, the learned relationship among concepts and relations, addressed by sparse attention vectors, is interpretable. The scoring function is given by:

$$
f_r(h, t) = ||\alpha_r^H \cdot D \cdot h + r - \alpha_r^T \cdot D \cdot t||_l \tag{18}
$$

Here, *D*represents a concept projection matrix composed by normalized attention vectors α*H r*, α*T r* belongs to [0, 1]*m*adopting convex combinations. Qian et al. [[136]](#ref-136) recommend that previous models fail to attract attention by disregarding the hierarchical structure of characteristics of the entities of human cognition and proposed TransAt [[136]](#ref-136). It coordinates translation embedding utilizing an attention mechanism. To deal with more complex relations, literature proposed TransMS [[137]](#ref-137) which uses the concept of multidimensional semantics. It captures the semantics for the relation to the head or tail entity and from the head or tail entity to relations and between the entities employing nonlinear*tanh* function.

A large part of current techniques is centered around the structured knowledge of triplets and augments the chance of their foundation [[30]](#ref-30). However, they overlook the semantic data and the earlier information shown by semantic data incorporated in most KG. Taking advantage of the semantic encoding of data, TransT [[138]](#ref-138) was proposed for structured data representing the range of an entity and coordinate entity type. The entity type is responsible for creating the relationship type. Semantic analogy based on related elements and types of relationships is used to capture the prior arrangement of relations and entities. The models presented so far translate triples as deterministic focuses in vector space. New works consider Gaussian embeddings to counter the uncertainty and translate it as random variable [[139]](#ref-139) [[140]](#ref-140). KG2E [[139]](#ref-139) sees relations and entities as vectors drawn randomly from multivariate Gaussian distribution (*Gd*) and scores a triple utilizing the distance between the two arbitrary vectors. The TransG [[140]](#ref-140) model additionally translates entities with G, utilizing a combination of *G*d to acquire various semantics. These models consider the uncertainty of the facts; however, this outcome is a complex model.

Techniques, for example, QuatE [[141]](#ref-141), RotatE [[121]](#ref-121) and TorusE [[142]](#ref-142) exploits quaternions, rotations, lie groups respectively and are like TransE. They do not supersede distance-based models fundamentally. However, their thought is equivalent to that of translation-based embeddings. Given a fact or triplet (*h*,*r*, *t*), they all guide the head element to the tail element through the relationship *r*; however, the particular mapping function on *r*is unique. Therefore this work places them in this subsection. RotatE [[121]](#ref-121) develops a rotational hadmard product or element-wise multiplication (◦) based on Euler's identity*e*^iφ^ = cos φ + *i*sin φ. The relation is categorized as a rotation between the head and tail entity in a complex-valued space. The score function is formulated below:

$$
f_r(h, t) = ||h \circ r - t|| \tag{19}
$$

RotatE also introduces a novel self-adversarial sampling technique that helps to effectively interpret the relationship types shown in Table 1. QuatE [[141]](#ref-141) diversifies the complex space into 4-Dimensional hypercomplex space and uses a Hamilton product (^N^) and acquires more meaningful rotational ability than RotatE. The scoring function of QuatE is represented below:

$$
f_r(h,t) = ||h \otimes \frac{r}{|r|} \cdot t|| \tag{20}
$$

Even though the TransE can viably catch the properties in a KG by keeping a basic principle of *h*+*r*≈*t*. It presents an issue of regularization by compelling embeddings of elements on a sphere in the vector space, which unfavorably influences the exhibition of the downstream tasks. TorusE [[142]](#ref-142) tackles the above mentioned issue by adopting a Lie Group representing a n-dimensional torus space defined as π : *R*n − > *T*n, *x*− > [*x*] where [*h*], [*r*], [*t*] belongs to *T*n. Like TransE, it additionally learns embeddings following the translation in torus space:

$$
[h] + [r] \approx [t] \tag{21}
$$

To sum up, KGC techniques dependent on the translation embeddings emphasized the utilization of the relations between entities, semantics between the relations and elements, and the structural data of the KG, which compensates for the complicated preparation and perturbing augmentation of conventional strategies. These techniques are fundamental and clear with solid interpretability [[143]](#ref-143).

## 3.3.2. Tensor Factorization Models

This class of models classifies the function of the KGC task as a tensor decomposition belonging to the family of factorization models. It addresses the graph as a three-sided tensor that is disintegrated into a composition of low-dimensional element vectors. The principle thought is to ensure that the model does not overfit by employing a small number of common hyperparameters, making them easier and simpler to train.

As shown in figure 10, it works by first creating a 3D binary tensor X (that is, X belongs to*R*^i^.*i*.*j*where*i*and*j* denotes the number entity and relation, respectively) utilizing the triplets present in multi-relational graphs. Each slice X*s*where*s*belongs to 0, 1, 2, to n present in tensor X directly represents a relation type*R*s . The value of X*pqr*= 1 tells that*p th*,*q th*entity and*r th*relation is present in the graph is true; otherwise, it indicates an undefined fact if the value equals zero.

![Image Description: The image is a diagram illustrating a tensor. It depicts a multi-dimensional array represented as a stack of matrices. Each matrix represents a two-dimensional slice, indexed by `e¹`, `e²`, ... `eⁱ` along one axis and `r¹`, `r²`, ... `rʲ` along the other. The diagram visually explains the structure of a tensor used within the paper, likely to represent data or parameters in a machine learning or deep learning context.](_page_19_Figure_8.jpeg)

**Figure 10:** Knowledge graph representation as Tensors.

Rescal [[37]](#ref-37) is one of the earliest model to exploit this approach for capturing semantics. As presented in figure 11, it uses the rank-r factorization technique to capture the latent meaningful representation of the required structure present in the knowledge graph as a result of applying the tensor. For*s th*relation from the set of*m*relations, equation (22) reflects tensor factorization in*s th*slice of X:

$$
\mathbb{X}_s = AR_s A^T \tag{22}
$$

Here,*A*represents an adjacency matrix responsible for capturing the latent semantic representation of entities. The pairwise interaction in*s th*relation is represented by matrix*R*s. Given,*M*r is relationship matrix, the scoring function is defined as follows:

$$
f_r(h,t) = h^T M_r t \tag{23}
$$

![Image Description: The image displays a three-layer neural network architecture. The bottom layer represents "Head Entity" and "Tail Entity" nodes, feeding into a middle layer of nodes. All middle layer nodes connect to a single top layer node, labeled *fr(h,t)*, representing the relationship score. Arrows indicate information flow. The network likely models relationships between entities ("Head Entity" and "Tail Entity") for a task such as knowledge graph embedding or relation extraction. *Mr* likely denotes a matrix of embeddings.](_page_20_Figure_4.jpeg)

**Figure 11:** RESCAL [[37]](#ref-37).

Fan et al. proposed TATEC [[144]](#ref-144), which is a more complex version of RESCAL by combining the two-way interactions between the entities and relations. To reduce the computationally complex nature of RESCAL, the DistMult [[36]](#ref-36) suggests to incorporate only the diagonal matrix*dig*(*r*) in place of *M*r. The scoring function is then reduced to:

$$
f_r(h,t) = h^T \operatorname{dig}(r)t \tag{24}
$$

It infers the fundamental relations between sets of elements that are present in the same dimension. Contrasted with RESCAL model, it decreases the parameter count and remarkably augments the performance for extracting the target knowledge in graphs.

![Image Description: The image is a diagram illustrating a knowledge graph embedding model. It depicts a three-layer architecture. The bottom layer represents "Head Entity" and "Tail Entity" nodes. The middle layer shows intermediate nodes, labeled *r*, representing relations. The top layer contains a single node, *fr(h,t)*, representing the final embedding based on head (h) and tail (t) entities and relation (r). The arrows indicate the flow of information, illustrating how entity and relation embeddings are combined to produce a final representation. The diagram visually explains the model's structure and information processing.](_page_20_Figure_9.jpeg)

**Figure 12:** DistMult [[36]](#ref-36).

To capture the pairwise compositional properties between entities, HolE [[120]](#ref-120) introduces circular correlation operation [[145]](#ref-145) denoted by ? :*R*^d^ ×*R*^d^ →*R d*. The scoring function of HolE is represented as:

$$
f_r(h,t) = r^T(h \star t) \tag{25}
$$

Here, ? is expessed as:

$$
[a \star b]_k = \sum_{i=0}^{d-1} a_i b_{(k+i) \text{mod}(d)} \tag{26}
$$

The main intention behind adopting ? is to leverage the reduced complexity of composite representation in the form of compressed tensor product. Furthermore, HolE makes use of the fast Fourier transform*f*(.) [[146]](#ref-146) which can further accelerate the computational process via:

$$
a \star b = f^{-1}(\overline{f(a)} \circ f(b)) \tag{27}
$$

A significant disadvantage of modeling with a circular correlation coefficient is that it is not composite. In simple terms, HolE cannot model asymmetric relations. Recently, Xu et al. [[147]](#ref-147) proposed HolEX, which is Extended Holographic Embedding that interpolates both the full tensor product and HolE. Given *c*, a fixed vector belongs to *R d*, for*a*, *b*belongs to*R*d, they introduced a perturbed holographic compositional operation which is defined as follows:

$$
h(a, b; c) = (c \circ a) \star b \tag{28}
$$

Most of the previous models exploit 3-way bivariate tensor decomposition for KGC. However, this methodology is not recommended for effectively capturing asymmetric relationships. Trouillon et al. [[38]](#ref-38) introduced the concept of leveraging the complex space*C d*to embed the entities and relations present in KG and proposed CompleX, which is a continuation of DistMult. The CompleX can effectively infer asymmetric relationships. Instead of using a real-valued space, CompleX leverages complex space*C d*to embed the entities and relations. The scoring function is defined below:

$$
f_r(h,t) = Real(h^T \operatorname{dig}(r)\overline{t}) = Real\left\{ \sum_{k=0}^{d-1} (h)_k(r)_k(\overline{t})_k \right\} \tag{29}
$$

where,*t*represents the complex conjugate of the tail entity and*Real*(.) denotes the real part of a complex relation. Hayashi et al. [[148]](#ref-148) analyzed and studied the equivalence of Complex and HolE. It has been shown that the HolE is understood by CompleX as an exceptional example where conjugate symmetry is inflicted on the embedding, and alternatively, each complex has a corresponding HolE.

Another interesting area of research is to integrate other reasoning regimes into knowledge graph embedding architectures. For example, if the *sun*is surrounded by*planets*and attracts*mass*by analogical reasoning, then scale*sun*to the*nucleus*and*planets*to the*electrons*. It can easily be concluded that the *nucleus*attracts a*charge*by analogy with the*sun*attracting a*mass*. To infer the analogical reasoning in knowledge graphs, ANALOGY [[149]](#ref-149) an extended version of RESCAL was proposed to model the characteristics of relations and entities as analogical properties by employing a bilinear scoring function as given in equation (23). This equation however is followed by two major constraints that depend on the analogical properties given in equation (30, 31). First, it should be a normal matrix. Secondly, for each pair of relations, their structure of the linear map (that is, *Mr*) must be mutually commutative.

$$
M_r M_r^T = M_r^T M_r \tag{30}
$$

$$
M_r M_{r'} = M_{r'} M_r
$$
(31)

To address the issue of independence in taking advantage of the earliest tensor decomposition, a.k.a Canonical Polyadic (CP), Kazemi et al. [[150]](#ref-150) introduced SimplE, an extension of CP, to dependently learn two embeddings of each entity to simplify link prediction tasks. It introduces the inverse of relationships (*r*0 ) and calculates the mean score with scoring function via:

$$
f_r(h,t) = \frac{1}{2}(t \circ r't + h \circ rt)
$$
(32)

It has been shown that the earlier works have not focused on the utilization of crossover interactions, a.k.a bidirectional interactions between relations and entities that help to segment the related knowledge for KGC tasks [[151]](#ref-151). The concept of related knowledge or information is explained in figure 13. The CrossE [[151]](#ref-151) model was proposed to exploit crossover interactions with

![Image Description: This diagram illustrates a knowledge graph, depicting relationships between individuals (A-E, P-Q). Nodes represent individuals, and edges represent relationships (e.g., "isMotherOf," "worksFor," "bestEmployee"). Edge styles (solid, dashed, colored) might indicate relationship types or data provenance. The graph likely exemplifies a knowledge representation used in the paper, potentially for reasoning or data integration. The central node "A" appears to be a key connection point.](_page_22_Figure_3.jpeg)

**Figure 13:** An example of made up Knowledge Graph [[151]](#ref-151). The black-colored relationships represents the potential related knowledge and interaction to infer the dotted relation i.e. father-child relationship. The red-colored links depicting the professional relations of A do not give important knowledge to this undertaking.

an interaction matrix*C*to obtain relationship specific embeddings*C*r =*x T r C*. It uses hadmard product operation to incorporate head entity and relation with *C*r via:

$$
h_I = C_r \circ h \tag{33}
$$

and,

$$
r_I = h_I \circ r \tag{34}
$$

Here,*h*I and*r*I represents head interaction and relation interaction respectively. The score energy function of CrossE is then formulated as follows:

$$
f_r(h, t) = \sigma(\tanh(h_l + r_l + b)t^T)
$$
(35)

where, σ(*x*) is nonlinear function and *b*represents bias vector.

## 3.3.3. Deeper scoring function

Over the years, deep learning has proven its implication in all specializations like computer vision, natural language processing, and graph-based learning. Researchers are attempting to take advantage of this cutting-edge technology in knowledge graph embedding to model complex nonlinear projections in continuous low dimensional space [[152]](#ref-152).

SME [[153]](#ref-153) or semantic matching energy characterizes energy functions employing neural networks, which can be utilized to quantify the certainty of each noticed reality ^h^(*s*, *p*, *o*)i. As displayed in figure 14, initially each triplet is inserted to the vector space. Then, at that point, two projection matrices are applied to catch the semantic associations among elements and relations. The fully connected layer is then applied to finally calculate the semantic matching energy for each fact. The main advantage of SME is that the relation type is not represented by a matrix, but is addressed by a vector. Therefore, in a situation where there are a large number of relation types, information related to the position of parameters and elements can be easily shared. The SME has two variants namely, bilinear form and linear form. In the two versions, the linear requires more computation time than the bilinear as it takes extra *n*parameters for training. Given,*Mx*1, *Mx*2, *My*^1^ and *My*^2^ are projection matrices, the bilinear and linear form are represented in equation (36) and (37) respectively.

$$
g_x(h, r) = M_{x1}h + M_{x2}r + b_x
$$

$$
g_y(t, r) = M_{y1}t + M_{y2}r + b_y
$$
(36)

$$
g_x(h, r) = (M_{x1}h) \circ (M_{x2}r) + b_x
$$
(37)

$$
g_{y}(t,r) = (M_{y1}t) \circ (M_{y2}r) + b_{y}
$$

Here, *b*represents a global bias vector. The final energy score is achieved by combining the*g*\_*x*(*h*,*r*) and *g*\_*y*(*t*,*r*) as follows:

$$
f_r(h, t) = g_x(h, r)^T g_y(t, r)
$$
(38)

![Image Description: The diagram illustrates a computational model, likely for knowledge graph embedding. It shows a function, *fr(h,t)*, taking "Head" and "Tail" entity embeddings as input (*Mx1, Mx2, My1, My2*) via intermediate representations. The model integrates "Relation" embeddings to generate a final output. The diagram's purpose is to visually represent the architecture of this specific knowledge graph embedding model.](_page_23_Figure_6.jpeg)

**Figure 14:** SME [[153]](#ref-153).

The NTN or neural tensor network model [[154]](#ref-154) aims to substitute the standard linear layer in conventional neural networks with the bilinear tensor, and associate the head and tail element vectors in various arrangements as given in figure 15. Firstly, the elements in the triplet (that is, head and tail entity) are fed to the first layer which is responsible for mapping the given entities to the projection matrices *M*r^1^ and *M*r^2^ with the relation specific tensor ^χ^*r*in the second layer. Secondly, these three elements are then pushed to the third layer i.e. non-linear layer accountable for merging the features to obtain the semantic knowledge. The semantic information is then finally fed to the relation specific output layer to obtain the final score. Given,*g*(*x*) = tanh(*x*) and *b*r=*bias*, the energy score of NTN is defined as follows:

$$
f_r(h,t) = r^T g(h^T \chi_r t + M_{r1} h + M_{r2} t + b_r)
$$
(39)

The NTN can accomplish good accuracy for predicting obscure relations between entities. The presentation of tensors can precisely depict the complex semantic connection among elements. Although, there are problems with high computation cost due to the additional parameters introduced by relation-specific tensors that cannot be adjusted to represent KG on a large scale. In the same literature [[154]](#ref-154), a less complex single layer model (SLM) model was proposed in which the value of relation specific tensor is null. The scoring function is obtained putting the value of ^χ^*r* = 0 in equation (39):

$$
f_r(h,t) = r^T g(M_{r1}h + M_{r2}t + b_r)
$$
(40)

![Image Description: The image is a diagram illustrating a neural network architecture. It depicts the processing of "Head" and "Tail" inputs through matrices ($M_{r1}$, $M_{r2}$, and a central 3D matrix $X_r$) to generate a relation ($fr(h,t)$). The process involves a hyperbolic tangent (tanh) activation function and shows the flow of information through the network layers. The diagram's purpose is to visually explain the model's structure and how input data is transformed to produce the relation output.](_page_24_Figure_2.jpeg)

**Figure 15:** NTN [[154]](#ref-154).

Curbing the limitations of NTN, Dong et al. introduced MLP [[122]](#ref-122) that gives a lightweight design for modeling the knowledge. It keeps all the elements i.e head entity, tail entity and relation at the same level that are simultaneously combined and projected into the vector space in the input layer. The generated matrices (*M*i*,*Mj*,*M*k*) are then fed into the nonlinear hidden layer (tanh) to generate the output score. The scoring function is defined as follows:

$$
f_r(h,t) = m^T g(M_i h + M_j r + M_k t)
$$
(41)

![Image Description: Figure 16 is a diagram illustrating a Multilayer Perceptron (MLP) architecture. Three input vectors ("Head," "Relation," "Tail") are processed through individual layers (Mᵢ, Mⱼ, Mₖ) before converging into a tanh activation function. The output, *fr(h,t)*, represents the final result of the MLP. The diagram visually depicts the information flow and layer interactions within this specific MLP model.](_page_24_Figure_6.jpeg)

NAM or Neural Association Model [[155]](#ref-155) sets up a deep neural architecture. The NAM embeds a given triplet into a feature vector space. At that point, the vector embeddings of the relation as well as the head entity are combined to get a vector *z*^0^ = [*h*;*r*] which act as an input

to architecture consisting of *N* rectified units (*RELU*) as follows:

$$
a^{n} = M^{n} Z^{n-1} + b^{n}, \quad where, n = 1, 2, ..., N,
$$

$$
z^{n} = RELU(a^{n}), \quad where, n = 1, 2, ..., N
$$
(42)

The final score is generated by matching the output of the last hidden layer with the tail entity vector via:

$$
f_r(h,t) = t^T z^N \tag{43}
$$

ConvE [[40]](#ref-40) is one of the first models to use Convolutional Neural Networks (CNN) to predict missing links in knowledge graphs. Unlike fully connected dense layers, CNNs can help capture complex nonlinear relationships by learning with very few parameters. ConvE adopts embedded 2-dimensional convolution, which outperforms 1-dimensional convolution to capture the interactions between features for two embeddings. ConvE achieves local linkages between different entities in multiple dimensions; however, it ignores global relations of triple embeddings. First, it works by combining the head entities matrix and the relations it feeds into a 2-dimensional convolution to generate a feature map tensor. This tensor then goes through a linear transformation parameterized by matrix *M*for projecting it into a low dimensional feature space. Finally, an inner product is used to match the tail unit. The scoring function for ConvE is defined as follows:

$$
f_r(h,t) = g(\text{vec}(g(\text{concat}(\overline{e_s}, \overline{e_r})* w))M)e_o \tag{44}
$$

where, *concat*is concatenation operator, ∗ represents convolution, and*e*s and*e*r are responsible for the 2D reshaping of the subject unit and relation unit, respectively.

Removing the reshaping activity from ConvE, ConvKB [[39]](#ref-39) uses 1D convolution to retain the interpretation properties of TransE, sufficient to capture global relationships and temporal attributes between entities. It addresses the embedding of each triple as a three-segment network and feeds it into the convolutional layer with the aim of achieving global connections between dimensional classes of a fact. The scoring potential of ConvKB is designed as follows:

$$
concat(g([es, er, eo]* \Omega))w
$$
(45)

where, Ω (filter set) and *w* (weight vector) represents shared parameters. In HypER [[41]](#ref-41), the vector embeddings of each relationship are completely reshaped after projecting them through the dense layer, and subsequently, a bunch of convolutional channel weight vector relationships in each layer are adjusted. In contrast to linear combinations in ConvE, the non-linear and quadratic mix of element and connection embeddings gives HypER a much higher expressive range and the benefit of fewer hyperparameters. HypER can likewise be viewed as a factorization model.

Capsule networks (CapsNets) [[156]](#ref-156) is a new type of architecture introduced recently to limit the constraints of CNNs. The main problem with CNNs is that they are unable to predict translation-invariant events. For example, consider the task of guessing whether a cat is present in the given image. CNN can easily predict that the given image is of a cat. But, being unable to predict any additional information such as a change in the position of a cat. Nonetheless, CapsNets consists of many capsules and can capture the translation-invariant properties. A capsule is a small group of neurons where each neuron in the capsule represents different properties of a particular part of the given input followed by a dynamic routing process.

Nguyen et al. [[157]](#ref-157) adopted this approach and proposed CapsE to explore the state-of-theart application of CapsNets in triple-based data. CapsE embeds a triplet ^h^*h*,*r*, *t*^i^ as unique ddimensional vectors *V*h*, *V*r* and*V*t* respectively. The vectorized triplet ^h^*V*h*, *V*r*,*V*t*^i^ of ^h^*h*,*r*, *t*^i^ put into the convolution layer where different channels of a similar 1×3 shape are iteratively executed to generate d-dimensional feature maps which are then fed into neurons called capsules. As a result, each capsule can encode multiple features in setting up the triplet to address sections on the equivalent dimension, which are then sent to another layer containing a capsule to output the triplet score.

More recently, graph neural networks (GNNs) [[46]](#ref-46) have attracted much attention due to their incredible ability to represent graph structure. R-GCN [[119]](#ref-119) was perhaps the initial attempt to exploit GNNs for KGC. RGCN produces region-linked embeddings, feeds them to a decoder that predicts missing relationships in KG. Ordinary GCN cannot embed multi-relational graphs because it ignores edge knowledge present in the graph. Therefore, R-GCN somewhat replaces the scoring ability of basic GCN to capture the relationship between edges. However, R-GCN learns additional weight networks for every connection, consequently making the proposed work non-adaptable for enormous graphs. The authors attempted to quantify this issue with decomposition techniques, namely block diagonalization and basis [[110]](#ref-110). These methods help to manage to overfit as well as make the connection weight matrices interdependent. In any case, the differential weight of the nodes locality is still undocumented, and a decoder is needed because they do not learn to embed relationships via graph neural nets.

SACN [[158]](#ref-158) attempts to augment the RGCN by adopting WGCN (Weighted Graph Convolution Network). It accumulates data from the locality of nodes by being sensitive to edge relationship types. In WGCN, the entire graph is broken into subgraphs to such an extent that each subgraph contains edges of just a solitary connection type. Like the methodology in R-GCN, SACN uses WGCN as an encoder to comprehend entity embeddings, which is then fed to a decoder (Conv-TransE). The aforementioned models indicate the shortcoming of treating all adjoining nodes for every relationship with equivalent significance. To beat this restriction, KB-GAT [[159]](#ref-159) uses the concept of attention to recognize significant data in the locality of nodes. Like RGCN and SACN, the encoder-decoder approach is followed. It uses graph neural nets as encoders and ConvKB as decoders. In contrast to the prior approaches, it exploits GNNs to learn both relation and entity embeddings.

## 3.4. Loss function layer

Neural networks are specifically used to embed information in KGs. The inaccuracy of a predicate is determined using the explicit scoring potential for the embedding. The loss function is used in conjunction with the scoring function. Extensive research is underway to develop new scoring functions, yet until recently, there has been almost no emphasis put on researching novel loss functions [[160]](#ref-160). The scoring elements of HolE and ComplEx are displayed similarly, although their effectiveness is opposite [[160]](#ref-160). One possible explanation for this difference is the miscellaneous loss function used for the scoring energy function. Five distinct loss functions are mentioned in this study. Here λ represents hyperparameter and [*t*]^+^ mentions *max*(*t*, 0). For Pointwise functions, given triplet *t*, if *t*is true,*g*(*t*) equals 1; otherwise, 0. For pairwise losses, *f*(*t*0 ) represents false fact and*f*(*t*) equals true fact.

Pointwise square error loss is used by RESCAL [[37]](#ref-37) where the objective is to limit the squared difference between the model scores and the labels. The ideal score for valid and false triples is 1 and 0, respectively. This loss profits by not having the hyperparameter contracting the space of hyper boundaries that differentiate with other loss functions.

Pointwise square loss =
$$
\frac{1}{2} \sum_{t \in T} (f(t) - g(t))^2
$$
(46)

Pointwise hinge loss is used by HolE [[120]](#ref-120). The objective is to limit the scores of negative realities and expand the scores of positive realities to a particular configurable value. In particular, this loss function reduces negative scores to - λ and amplifies positive scores to ^+^ λ.

$$
Pointwise hinge loss = \sum_{t \in T} (\lambda - g(t)f(t))^+
$$
(47)

Pointwise Logistic Loss is utilized by CompleX [[38]](#ref-38) with the benefit of ignoring the parameter λ results in a smoother loss slope. It likewise uses a logistic function to limit the negative triples score and advance the positive triples score.

$$
Pointwise logistic loss = \sum_{t \in T} log(1 + exp(-g(t)f(t)))
$$
(48)

TransE [[31]](#ref-31) and DistMult [[36]](#ref-36) adopts the Pairwise Hinge Loss. Hinge loss can be executed in both pairwise or pointwise strategies. Linear learning is to rank to loss in order to maximize the difference or margin between true and false triplets.

$$
Pairwise hinge loss = \sum_{t \in T^+} \sum_{t' \in T^-} (\lambda + f(t') - f(t))^+
$$
(49)

Lately, KGE methods have been developed to resolve the ranking issue as a form of multiclass characterization. A binary cross-entropy loss is employed by ConvE [[40]](#ref-40) to model the multi-class losses. It works by preparing the entire lexicon of entities for training each positive fact to such an extent that for a triple (s, p, o), all triples (s, p, o') with *o*^0^ belong to the entire set of entities with*o*^0^ =*o*considered false. Notwithstanding the extra computational expense of this methodology, it permitted ConvE to sum up over a bigger example of negative occurrences and outflank different methodologies. There are new loss functions proposed, for example, self adversarial [[121]](#ref-121), soft margin loss [[159]](#ref-159), multiclass negative log-likelihood [[161]](#ref-161) ordinarily utilized for training KGE and have shown good performances in downstream tasks. It is important to focus on training different loss functions, just like scoring functions, when researching KGE for KGC.

## 3.5. Evaluation Metrics

Typically, KGC task assessment metrics include Mean Reciprocal Rank, Mean Rank, and Hits@k [[162]](#ref-162). They comprehensively assess the efficiency of KGC algorithms from various angles and are not complicated to use.

Here, N refers to all the expectations.

Mean Rank works by calculating the average of rank associated with predictions between all competitors. The low value of the Mean Rank suggests the predictive power of the model is higher. The Mean Rank values can mirror the positioning of the right triples in the likelihood of setting up the test triples. In simple terms, it is a proportion of the exactness of the KGC algorithm.

$$
Mean Rank = \frac{1}{|N|} \sum_{i=1}^{|N|} rank_{triple(i)}
$$
(50)

Mean Reciprocal Rank (MRR) works by predicting the scores of triples based on whether they are correct or not. It is an ordinarily utilized metric to quantify the impact of search algorithms. The larger the value of MRR, the better the performance of the model. On the off chance that the first anticipated triple is valid, its score is 1, and the subsequent true scores are 1/2, —,1/n, where 'n' is the nth triple. The final score is the addition of all the scores.

Mean Reciprocal Rank =
$$
\frac{1}{|N|} \sum_{i=1}^{|N|} \frac{1}{rank_{triple(i)}}
$$
(51)

Hits@K demonstrates the likelihood of the right prediction in the top K possible triples determined by the model. Hits@K addresses the capacity of the model to anticipate the connection between facts effectively. In simple terms, it counts how many positive triples are ranked in the top k positions against a bunch of synthetic negatives. The value of K is generally chosen as 10. The value of Hits@k lies in the range of 0 and 1. The larger the value of the Hits score, the better the performance of the model.

$$
Hits@K = \frac{1}{|N|} 1 if rank_{triple(i)} = < K \tag{52}
$$

## Reinforcement Learning for Knowledge Graph Completion

When employing KG to advance a question answering (QA) framework, only one of the triple is inferred to respond to the inquiry. For complex QA frameworks and when the given KG is mainly fragmented, it is essential to have the option to deduce obscure answers with existing triples. State-of-the-art embedding-based techniques limit their applications to model complex queries due to their inability to model the symbolic composition of facts present in KGs. An elective answer is to deduce missing links by orchestrating data from multi-hop paths, for example, BornIn(JoeBiden, Pennsylvania) ∧ LocatedIn(Pennsylvania, USA) ⇒ bornIn(JoeBiden, USA), given in figure 17. Reinforcement learning can help to understand questions and answers by modeling them as a sequential decision problem. As of late, the Path-Ranking Algorithm (PRA) [[163]](#ref-163) arises as a promising technique for learning complex paths in huge KGs. PRA uses random walk with restart-based deduction component to run a depth first search to extract required features called relational paths. Although it works in a completely discrete space, making it hard to assess and look at comparable entities and relations in a KG.

![Image Description: This image is a knowledge graph depicting relationships between individuals and entities. Nodes represent individuals (Joe Biden, Kamala Harris, Chuck Schumer) and entities (U.S. Government, USA, Pennsylvania). Edges, labeled with relationship types (e.g., "BelongTo," "BornIn," "CollaboratedWith," "LiveIn," "LocatedIn"), show connections between them. The graph illustrates the relationships among these individuals within the context of the U.S. government and their geographical locations. The purpose is likely to demonstrate the use of a knowledge graph for representing complex relationships in the paper's domain.](_page_28_Figure_6.jpeg)

**Figure 17:** An example of knowledge graph completion to infer complex queries.

DeepPath [[164]](#ref-164) is one of the earliest attempts to use reinforcement learning techniques to estimate multi-hop logic over a KG. The RL environment in DeepPath is defined by Markov Decision Process (MDP). The translation-based embeddings, namely TransE [[31]](#ref-31), and TransH [[32]](#ref-32) is utilized for encoding the state of the RL agent in low dimensional space, which is responsible for sampling the relations to extend the number of paths. The reward function for policy gradient-based training is defined to control the path search for better precision, accuracy, and productivity to better guide the agent. However, it needs to know the objective target entity ahead of time to direct the agent. DeepPath outperformed standard PRA and KGE methods, yet one principle issue is that its action space is moderately huge. Moreover, it must not be exploitative of complex tasks where the subsequent element is obscure and should be procured by inferring. Exploring the limitations of DeepPath, Das et al. [[165]](#ref-165) proposed MINERVA, which takes into account that the objective element found from the source element through the path. It does that without knowing the objective element and pre-figuring the path that worked on the past technique. It presents the Long Short Term Memory (LSTM) network to oversee previous paths and helps to guide the agent over a specific entity and relations that help better perform the policy-guided walk to the right element.

In contrast to MINERVA, M-WALK [[166]](#ref-166) utilizes RNN to map historical paths to the agent and Q values which then at that point employs the Monte Carlo sampling technique to unravel the direction. It lastly utilizes the Q-Learning algorithm to learn the values present in action. However, it exhibits two major drawbacks. RNN, as we know, suffers from a gradient explosion problem when the size of input data is significant. The Monte Carlo sampling typically requires a finalized direction to assess the technique and update the model, so the productivity is likewise low.

The walk-based QA frameworks may experience significant downsides. First, because most of the KGs have missing links, the agent may show up at a right answer whose connection to the source substance is absent from the KG without getting any reward. Second, since no ground truth is accessible for training, the agent might unintentionally navigate misleading paths that lead to the right answer. To counter this, Lin et al. [[167]](#ref-167) suggests two techniques for RLbased KG reasoning, namely, reward shaping and action dropout. The former one joins ability in demonstrating the semantics of triples with the representative thinking capacity of the path-based methodology. Whereas the latter one is more powerful in empowering the policy to test different paths. In most of the works at the decision level, only the absolute entity is named, by which the agent, in turn, brings about sparse and deferred rewards. To take care of this issue, Qiu et al. [[168]](#ref-168) proposed a potential-based reward forming technique to supply extra compensations to the agent to direct its reasoning cycle, which can speed up the convergence and cause the model to perform better.

Several works have been done to abolish the pre-training cycle needed to diminish the complexity. Specifically, the attention mechanism focuses harder on the neighbors to avoid choosing an invalid path. Wang et al. [[169]](#ref-169) develop a system that joins LSTM and graph attention mechanism as memory parts to dispose of the fine-tuning process. Augmenting the work of [[167]](#ref-167) they further develop the deep reinforcement learning framework by introducing three techniques, namely, reward shaping, action dropout, and force forward. Recently, a methodology called DA-Path [[170]](#ref-170) is proposed dependent on distance-based reward in the RL system to map variable awards for various positions. To allow the model to recall the path that considers overseeing the memory of relations in the path, it considers GSA (graph self-attention) with gated recurrent unit (GRU). However, it experiences slow convergence and low learning proficiency. Most of the earlier methodologies are based on a popular REINFORCE [[171]](#ref-171) (policy gradient) algorithm, which as a rule has a huge variation and vigorously relies upon starting policy.

Wang et al. [[172]](#ref-172) propose ADRL, which introduces the Actor Critic Algorithm that exploits policy gradient and sequence-based differential learning. Contrasted with REINFORCE, it works by updating the parameters in a single step fashion by utilizing the value function responsible for decreasing the variance of policy gradient without remaining idle so that the value function and policy gradient are trained concurrently. Less thought has been given to examining the hierarchical construction for KG reasoning, which exhibits performance improvement for modeling multiple semantics. Wan et al. [[173]](#ref-173) introduce a framework called HRL (hierarchical reinforcement learning) that functions by augmenting the whole action into sub-actions. The component is carried out by a progression of the high to low-level policy. The former helps manage to learn historical data. The latter is answerable for learning sub-actions just as augmenting every action space into a light action space. Thus, the numerous semantics of each relationship can likewise be learned.

## Comparative Analysis

Looking at the execution of best-in-class models is precarious because of various training techniques adopted by researchers. For example, different loss functions (self adversarial or absolute margin), 1vsAll scoring or negative sampling, new types of regularization (for example, weighted and unweighted L1, L2, L3), initialization techniques, utilization of reciprocal relations [[150]](#ref-150), and ablation studies are also not carried out. Exploiting different techniques for KGE preparation makes it hard to analyze execution performance for different model designs, particularly when predictions are repeated in earlier examinations that utilized alternate training methods. For example, the parameters of a model are normally tuned utilizing grid search on a small search space by involving custom-built boundary parameters. A search space reasonable for one model might be imperfect for another. Of course, the more up-to-date training procedures can extensively execute better in performance [[174]](#ref-174) [[175]](#ref-175).

In [[176]](#ref-176), summed up the effect of various model designs and distinctive training systems on model execution experimentally. They played out on a broad arrangement of trials utilizing mainstream model structures and methodology in a typical exploratory arrangement. As opposed to most earlier work, they considered training the models on enormous search space and performed model tuning utilizing quasi random search rather than grid search followed by bayesian parameter optimization. They tracked down the relative execution contrasts between different model structures and suggested that the results frequently dropped and sometimes improved compared with earlier outcomes. For instance, RESCAL [[37]](#ref-37), which establishes the principal embedding model however is hardly explored to be in current works, showed solid performance and outflanked state of the art models, for example, TuckER [[177]](#ref-177), and ConvE [[40]](#ref-40). It recommends that appropriate training systems and hyperparameter settings shift essentially across data and models, demonstrating that a little change in search space can influence predictions on model execution.

Pouya Pezeshkpour et al. [[178]](#ref-178) reconsidered and researched the current issues with evaluation metrics and clarified that the currently adopted techniques do not assess KGC, are hard to use for calibration, and cannot reliably differentiate between various models. Calibration is additionally a vital part of KGC that has as of late got consideration [[179]](#ref-179). Safavi et al. [[180]](#ref-180) show that calibration procedures can altogether diminish the alignment error of KGE models in the downstream tasks. Instinctively, calibration is a post-preparing step that changes KGE expectation scores to illustrate real and correct probabilities. "Treating the likelihood of truth of a triple (σ(ψ(*s*,*r*, *o*)) *for triple s, r, o) as the certainty of the model for the triple, the model is considered to be calibrated if the certainty lines up with the pace of confirmed realities"* [[178]](#ref-178). If certainty is equivalent to 0.5, then around half of triples with this certainty to be valid. Assuming this extent is a long way from 50%, the model isn't calibrated, i.e., the model is underconfident if the extent is greater and overconfident if it is lower. Under an optimal circumstance, if the model predicts that a triple is valid with a 0.9 certainty score, it ought to be right 90% of the time. Model calibration needs dependable certainty estimation and successful alignment strategies to fix the calibration mistakes. As far as KGE is concerned, two certainty or confidence estimation techniques, SigmoidMax (SIG) and TopKSoftmax (TOP), are exploited in [[179]](#ref-179) [[180]](#ref-180).

There are two calibration techniques. Isotonic regression [[181]](#ref-181) is a non-parametric technique and does take into account sigmoid assumption. It fits an increasing constant function to the model yield and is generally suitable for many examples. However, it is prone to overfit. Platt scaling [[182]](#ref-182) on the other takes into account the sigmoid function that learns scalar weights to yield a confidence score for each example. It might work better for smaller datasets. Model Calibration has a few advantages. According to the framework's point of view, language processing pipelines that incorporate KG can depend on calibrated scores to determine which KGE forecasts to trust. According to a research point of view, incorporating calibration helps determine the output predictions for acknowledging KGE models. As given in figure 18, we can easily analyze how a very much calibrated model resembles. A straight spotted line addresses an ideal calibrated model though the red shaded line addresses an uncalibrated model.

![Image Description: The image contains two diagrams (a) and (b), each showing a square with a dashed diagonal line and a solid black line representing a path. Diagram (a) depicts a simple L-shaped path, while diagram (b) shows a more complex, stepwise path. Both paths begin at the lower left corner and approach, but do not cross, the diagonal. The diagrams likely illustrate different strategies or solutions within an algorithm or model described in the paper, possibly related to pathfinding, optimization, or constraint satisfaction problems.](_page_31_Figure_2.jpeg)

**Figure 18:** (a) Uncalibrated Model (b) Calibrated Model

Models after calibration procedures work impressively better compared to uncalibrated strategies [[44]](#ref-44). Nonetheless, two primary issues are confining the viability of the probabilistic calibration techniques for link prediction tasks [[183]](#ref-183). Firstly, the lack of suitable confidence estimation. The evaluation techniques revolve around the ideal score and contrast it with different scores in the score sequence. High ideal scores lead to high certainty yet do not accomplish a similar level of precision since the score of each triple shows its relative ordering among other triples in a single prediction. Secondly, the inconsistent and unreliable calibration metrics. Expected Calibration Error (ECE) [[184]](#ref-184) is ordinarily used to assess the impact of calibration, yet is not appropriate for downstream tasks such as link prediction. Benefitted from a causal inference analysis, Kai Wang et al. [[45]](#ref-45) proposed a novel neighborhood intervention consistency (NIC) method that can effectively intercede the scoring cycle of KGE models. In particular, it creates a progression of neighborhood vectors for an input element by changing the entity vector in various dimensions and inspecting whether the model's output changes or matches the initial one. On this premise, the authors also designed neighborhood intervention values and a dimension selection system for high-dimensional KGE models to focus on efficiency. However, there is a tradeoff between the number of dimensions incorporated and the accuracy achieved. Selecting a proper neighborhood is very much needed to focus on both efficiency and predictive power.

## Towards Embedding Real World Knowledge Graphs

Existing methodologies fundamentally revolve around static link structure between a finite arrangement of entities overlooking the assortment of information types that are regularly utilized in information bases like content, arithmetic values, images, uncertain and temporal information. In this section, a higher outline on utilizing this real-world knowledge on link prediction tasks is discussed. As shown in figure 19, this segment is split into three subsections, multimodal knowledge graph, temporal knowledge graph, and uncertain knowledge graph embeddings.

![Image Description: This flowchart categorizes knowledge graph embedding methods. The root node is "Real World Knowledge Graph," branching into "Uncertain," "Temporal," and "Multi-modal" categories. Each branch further subdivides into data modalities (Text, Numeric, Multiple) which then list specific embedding models applicable to that data type and characteristic. The diagram thus provides a structured overview of different knowledge graph embedding techniques based on their input data characteristics.](_page_32_Figure_1.jpeg)

**Figure 19:** Hierarchical Distribution for emneddings real world knowledge graphs.

## 6.1. Multimodal Knowledge Graph Embeddings

Aside from relations to a fixed arrangement of triples, multimodal knowledge bases not solely incorporate mathematical attributes like age, monetary, and geo-data, but inherit literary features like names, biodata, and designation, and images such as profile photographs, banners, etc. These knowledge types act as a critical part providing additional information that can play as a catalyst for improving the accuracy in knowledge graph completion tasks. For instance, the literary descriptions and images may give proof of an individual's age and occupation. If we consider a multimodal KG containing an image of a person with a description as text, a 'Person' designation can easily be attributed utilizing a literal image, while the description contains his identity. Incorporating multimedia into existing methodologies as triples are difficult as they relegate every element to a particular vector and anticipate missing connections or characteristics by specifying the potential values, the two of which are only conceivable if the elements come from a smallscale enumerable set. In this study, the KGE models with multimodality are separated into the accompanying classes dependent on the multimedia used: Numeric, Text and Multiple literals. A KGE model which leverages no less than two categories of multimedia is considered multimodal.

## 6.1.1. Text Literal

Extended RESCAL, DKRL, Jointly, KDCoE and KGlove with literals leverage the text literals. Extended RESCAL [[185]](#ref-185) augments the initial RESCAL approach by handling textual attributes more effectively and managing the sparsity of the tensors. The idea was to utilize multiplicative update rules to extend the nonnegative factorization such that the triplets that contain textual knowledge are encoded in a matrix by tokenizing and stemming operations. This model, however, converges slowly compared to RESCAL and does not take into account the grouping and sequencing of the text.

DKRL (Description Embodied Knowledge Representation Learning) [[186]](#ref-186) is an extension of TransE that constructs embeddings of triplets by joining structure and description features. Deep CNN and a continuous bag of words (CBOW) are utilized to produce the descriptionbased representation of entities. The structural highlights are then incorporated by translationbased scoring function TransE. However, it isolates the objective functions into energy elements of description and structural representation, which is inefficient. Instead of utilizing CNN, the literature suggests Jointly [[187]](#ref-187) as it exploits attentive LSTM and incorporates the textual as well as structural knowledge of entities into a joint representation. However, the scoring function in both DKRL and jointly is based on TransE only.

KDCoE [[188]](#ref-188) centers around the formation of an arrangement for elements of multi-lingual knowledge bases by making novel inter-lingual links with high confidence. It employs a multilingual KG for semisupervised cross-lingual training and performs cotraining of a multi-lingual KGE model with a multi-lingual description embedding model that repetitively associates with each model for entity descriptions and structured based knowledge. Michael Cochez et al. [[189]](#ref-189) proposed KGlove with literals intending to incorporate descriptions on their original KGlove [[190]](#ref-190) model. The two co-occurrence matrices are generated autonomously and are finally merged to perform a joint embedding. The first co-occurrence matrix is based on the KGlove approach, which performs the individualized page rank on the original weighted graph and is normalized using the optimization used in Glove. The latter is an inverted edged graph, and the named entity recognition is performed before the former matrix is constructed and subsequently normalized.

The fundamental difference between these models lies in the procedures used to get as much benefit from the information in the text as possible. The advantage of KDCoE over other models is that it considers the descriptions present in multi-lingual graphs. However, the different types of text literals are not widely used in the aforementioned literature because the works are more aligned towards longer text literals and less overview on shorter text like labels and names.

## 6.1.2. Numeric Literal

The works that leverage numerical knowledge are MTKGNN, KBLRN, LiteralE, and TransEA. MTKGNN [[191]](#ref-191) adopts both relational networks and attribute networks to train triple classification and regression tasks, respectively, to obtain the knowledge contained in entities and learned embeddings. A linked fact is fed into a non-linear transformation in a relational network and thereafter implements a sigmoid function to obtain linear transformation. Two regressions are performed for the head and tail properties separately to predict continuous attribute values in attribute networks. Finally, both networks are modeled in a multifunctional design using a common embedding space. Mathias Niepert et al. [[50]](#ref-50) propose a novel KBLRN approach to merge relational, latent, and numerical highlights to represent large numerical values. The Probability of Experts (PoE) method is utilized to merge these features and train them together from start to finish.

LiteralE [[51]](#ref-51) feeds data into the current latent feature model by adjusting the scoring function in base model DistMult. It does by supplanting the vector representation of the elements in the scoring function with the literally enriched entities. To produce new entities vectors that are lexically rich, it exploits a learnable transformation method that inputs the original entities and its initially aligned literal vectors as data sources and maps them to new vectors. TransEA [[192]](#ref-192) on the other hand, is comprised of two embedding models, namely TransE and Attribute Embedding Model (AEM). AEM undergoes linear regression with attributive numeric features as input. The TransE is then characterized using the individual loss measure of the part model with thresholds for the weights to be distributed.

Despite their commitment to leverage numerical literals, each method discussed neglect to understand the meaningful relationship between the information and a variety of multimodality. For example, 'Year 2010' and '2010e' can be seen as something similar because the type semantics are discarded. Also, the standardization is not implemented properly. Henceforth the semantic equivalence between two values, for example, '500nm' and '5m', is not highlighted. Similarly, most models do not have the appropriate components to deal with multi-valued literals.

## 6.1.3. Multiple Literals

To the best of our knowledge, MKBE [[47]](#ref-47) is the current state of the art model that incorporates numeric, text and image multimedia for modeling KGE. It works on the principle of DistMult which adds neural encoders to different types of information to form embeddings for triplets. A fixed-length vector is encoded utilizing CNN for image knowledge type. For text features, LSTM is employed to learn and extract the sequences present in text data. The scoring used in MKBE is the same as the scoring function employed in DistMult and is utilized to decide the accuracy of likelihood of triples. IKRL [[193]](#ref-193) incorporates TransE for structural learning and mutual training with an image encoder to create embeddings in each instance for the image relation. It additionally configures the attention of each instance of the image using multi-valued attention based training. Other approaches like EAKGAE [[194]](#ref-194) and [[186]](#ref-186) are also worth mentioning. However, they only include text and numeric literals.

## 6.2. Temporal Knowledge Graph Embeddings

A few KGs include temporal realities, for example, the triple*(DonaldTrump, PresidentOf, USA)*only substantial in a particular time span (2017, 2021). Temporal Knowledge graphs like YAGO3 [[15]](#ref-15), ICEWS2014, ICEWS2005-15, ICEWS [[195]](#ref-195), GDELT [[196]](#ref-196) feed time data into facts. Triples appended with time data are addressed as quadruples, formed like*(s, r, o, T)*, where T signifies the timestamp. Conventional KGE models dismiss time data, prompting an insufficiency of performing link prediction on Temporal KGs, including relations, for example, *(?, PresidentOf, USA, 2018)*.

![Image Description: This diagram depicts a graph showing Donald Trump's presidency (20-01-2017 to 20-01-2021). Nodes represent key entities (Trump, USA, China, India), and edges represent events with dates: Trump's presidency start and end dates and his visits to China (08-11-2017) and India (24-02-2020). The image likely illustrates a data model or knowledge representation within the paper, possibly related to temporal events or political datasets.](_page_34_Figure_5.jpeg)

**Figure 20:** An example of Temporal Knowledge Graph.

In general, KGE models neglect to undertake time-based modality while learning embeddings for static Knowledge bases. Temporal-KGs is a significant yet infrequently examined research area. The past few years have witnessed a good number of TKGs models [[197]](#ref-197) [[198]](#ref-198) [[199]](#ref-199) [[200]](#ref-200) [[201]](#ref-201). The purpose of the temporal KGE is to dynamically change the (time-based) associated relationships between adjacent triples. t-TransE [[197]](#ref-197) is a combined model of TransE and temporal boundaries. It suggests placing these bounds in temporal order on the vector space to maintain temporally stable and precise embeddings. Influenced by TransH, HyTE [[198]](#ref-198) associates entities with temporal knowledge and relation by projecting them into a hyperplane trained by temporal data and achieving embeddings by limiting translation distances. To exploit sequences present in temporal knowledge, TA-DistMult [[199]](#ref-199) adopts RNN to gain efficiency with the time-based features of the relation, which is used in TransE and DistMult for link prediction tasks.

To leverage the cognitive capacity, ConT [[202]](#ref-202) generalizes static knowledge graph embedding methods, including RESCAL and Tucker, to episodic tensors (Et) in order to reduce complexity. Tree and ConT are two novel speculations of RESCAL to Et. ConT acquires exceptional execution for modeling temporal Knowledge graphs due to its latent representational flexibility of sparse tensor for time index. Even though the complexity of Tree and ConT is decreased when contrasted with episodic Tucker, it may, however, cause fast overfitting during training. DE-SimplE [[203]](#ref-203) incorporates diachronic word embeddings responsible for deriving entities' characteristics by uncovering the implications of advanced information over time. It simply works by combining it with a static KG such as SimplE for the function of temporal KGC.

Inspired by the CP (canonical product) decomposition of the order 4 tensor, TNTComplEx [[200]](#ref-200) presents an extension of ComplEx for Temporal KGC. Although TNTComplEx achieves significant functioning, it is difficult to accurately determine the position and rank of tensors using CP decomposition. Propelled by the TuckeR decomposition of order 4 tensor, the literature proposed TuckERT [[204]](#ref-204), a variation of TNTComplEx. However, this model does not manually select the position of the tensor, and it considers only temporal facts. TuckERTNT [[204]](#ref-204), an extension of TuckERT [[204]](#ref-204), is additionally proposed in literature to include both static and temporal facts.

Temporal KGs often exhibit various concurrent non-Euclidean features, such as hierarchical and cyclic designs. The current KGE approach to the representation of temporal knowledge of entities and their dynamic progression in Euclidean space cannot fully capture such specific structures. To curb this, DyERNIE [[201]](#ref-201), a non-Euclidean embedding approach has been proposed that masters developing entities as a result of Riemannian manifolds, where structures are assessed from the geometrical bends of hidden information. But this approach is highly dependent on a distance function, which may hamper the performance. More recently, a new temporal KG completion method TeLM [[205]](#ref-205) is proposed. It performs order 4 tensor factorization of temporal knowledge using a linear temporal regularization for modeling time-based embeddings. It also uses multi-vector embeddings to represent knowledge as it provides better generality and greater expressivity for temporal KGEs as opposed to single and complex-valued embeddings.

## 6.3. Uncertain Knowledge Graph Embeddings

Knowledge Graphs, for example, ConceptNet [[206]](#ref-206), carry uncertain data with a certainty score allocated to each triplet. In a numeric-enhanced KG, each triple is associated with a numeric feature. It is significant to add a triplet with a particular numeric feature semantics, as these numbers may encode significance, vulnerability, strength, and so forth. For instance, figure 21 suggests that numeric highlights demonstrate the significance of a relationship. The triple (ANDREW, Skill, MLOps, 0.90) is accordingly more significant than (ANDREW, Skill, Physics, 0.15) as far choosing a career path is concerned.

Many works are mentioned in the literature of knowledge graph representation learning that supports multimodal data and leverage numeric features related to node entities to produce better embeddings for upgraded link prediction tasks [[51]](#ref-51) [[192]](#ref-192) [[47]](#ref-47). However, these models are not

![Image Description: The image is a directed graph representing Andrew's skills. Nodes represent skills (Python, Java, MLOps, Physics) and Andrew's central node. Directed edges show skill levels (0.15–0.90), indicating the strength of each skill. The graph likely illustrates a skill profile or competency model within the context of the paper.](_page_36_Figure_0.jpeg)

**Figure 21:** An example of Uncertain Knowledge Graph

intended to gain from numeric qualities related to edges in a KG. With the prominent exemption of [[207]](#ref-207), supporting numeric features is up to date still an under-achieved exploration. UKGE [[207]](#ref-207) produces certainty scores for seen triples by flattening the numeric values from range 0 to 1. It then utilizes probabilistic logic [[208]](#ref-208) to anticipate the likelihood estimates for triples that are unseen by mutually preparing a model to regress over the certainty scores. A constraint of this methodology is that out-of-band logic principles are needed as extra information. It is additionally significant to note that UKGE targets at supporting uncertain KG, in particular graphs whose edge numeric features address uncertainty. Sumit Pai et al. [[209]](#ref-209) proposed FocusE, an extra layer that fits between the loss and scoring layers of an ordinary KGE technique, and it is intended to be utilized during training. In contrast to conventional techniques, prior to inputting the scoring layer to a loss function, they balance the output dependent on numeric attributes to acquire focused scores. They influence numeric values so that while preparing the model, it focuses more on the triples whose associated numeric values are large. However, this extra layer does not exploit unseen triples into consideration, and incorporating multi-valued numeric features is still a challenge.

## Software Libraries

In this section, we will briefly discuss the software ecosystem that revolves around embedding knowledge graphs. Over the past three years, several libraries have been distributed recently with plans to upgrade further the development process related to KGE (as shown in figure 22). The research and development community has additionally distributed code to work with open source contributions. A correlation between open-source software libraries based on features, accessibility, scalability, state of the art produced, and programming environment practices is reviewed in this paper.

The center of the KGE's are models, and we have mentioned (in section 5) that there are many models available for training the KGE. The accessibility of models for each library is recorded in Table 2. Some of the most common models are TransE [[31]](#ref-31), CompleX [[38]](#ref-38) and DistMult [[36]](#ref-36) accessible practically in almost all the libraries and there are a few varieties present across the rest of the models for which library gives what models. Libraries like Pykg2vec [[210]](#ref-210) and PyKEEN [[211]](#ref-211) offer a wide scope of models, for example, RGCN [[119]](#ref-119), TuckER [[177]](#ref-177), NTN [[33]](#ref-33), KG2E

![Image Description: The image is a timeline illustrating the evolution of eight knowledge graph embedding (KGE) libraries: OpenKE, PyTorch-BigGraph, LibKGE, PyKeen, TORCH-KGE, AmpliGraph, Pykg2vec, and Graphvite, and DGL-KE. Each library is represented by a box, connected to a subsequent library via a horizontal timeline arrow indicating their development order. The timeline depicts a progression of KGE tool development.](_page_37_Figure_0.jpeg)

**Figure 22:** Open source libraries for training KGE.

[[139]](#ref-139) which are absent in libraries such as AmpliGraph, Pytorch BigGraph and GraphVite etc. It all depends on what the use case is, if it is a research task where different models or approaches need to be analyzed then the libraries with the largest number of models are ideal. However, assuming that the requirement is good performance only for applicable use cases, it may not be fundamentally relevant to have too many models where we only need high performance and accuracy.

| **Table 2:** A comparative analysis of open source libraries for training KGE. S1*: TransE, DistMult, ComplEx, TransH, | | |
|---|---|---|
| TransD, TransR, RESCAL, HolE, SimplE. S2*: KG2E, NTN, ProjE, TuckER. S3*: TransE, DistMult, ComplEx | | |

| Library | Model | Pre Training | Performance | Framework |
|---|---|---|---|---|
| | | support | | |
| OpenKE[[212]](#ref-212) | S1*, Analogy | WikiData, FreeBase | Support GPU | Pytorch, Tensorflow |
| AmpliGraph [[213]](#ref-213) | S3*, HolE, ConvKB, ConvE | - | Support GPU | Tensorflow |
| Pytorch BigGraph | S3*, RESCAL | WikiData | Support GPU, CPU | Pytorch |
| [[214]](#ref-214) | | | (Distributed | |
| | | | Execution) | |
| Pykg2vec[[210]](#ref-210) | S1*, S2*, Analogy, CP, ConvE, | - | Support GPU | Pytorch, Tensorflow |
| | RotatE, TransM, SLM, SME, | | | |
| | ComplexN3 | | | |
| LibKGE [[215]](#ref-215) | S3*, RESCAL, SimplE, ConvE, | WikiData, FreeBase | Support GPU | Pytorch |
| | RotatE, TuckER, CP | | | |
| GraphVite [[216]](#ref-216) | S3*, SimplE, RotatE, QuatE | WikiData | Support GPU, CPU | Pytorch |
| | | | (Distributed | |
| | | | Execution) | |
| PyKeen [[211]](#ref-211) | S1*, S2*, ConvKB, ConvE, | - | Support GPU | Pytorch |
| | RotatE, RGCN, SME | | | |
| DGL-KE [[217]](#ref-217) | S3*, TransR, RESCAL, RotatE | - | Support GPU, CPU | Pytorch |
| | | | (Distributed | |
| | | | Execution) | |

Access to pre-trained embeddings for large-scale knowledge graphs to perform downstream tasks is an important perspective. This is probably the most useful parameter when the client does not have enough resources and technology to train KGE's from scratch. Thus, utilizing Pre-Trained models that are accessible in certain libraries for instance, WikiData in (OpenKE [[212]](#ref-212), pytorch BigGraph [[214]](#ref-214), GraphVite [[216]](#ref-216), Lib-KGE [[215]](#ref-215)) and a few parts of FreeBase is likewise accessible in OpenKE. Libraries, for example, AmpliGraph [[213]](#ref-213) and Lib-KGE [[215]](#ref-215) additionally offer benchmark datasets.

Sometimes, the user may need to train embeddings themselves, so it is important to consider scalability when we cannot leverage pre-trained embeddings. If the graph is enormous, we may need to scale it through distributed execution offered by Pytorch BigGraph, GraphVite, and DGL-KE. Another important viewpoint is the core framework; that is, different libraries support different frameworks like TensorFlow and PyTorch. A large subset of them support PyTorch; However, if the user only knows TensorFlow, it may be more appropriate to use libraries that maintain TensorFlow, such as AmpliGraph and Pykg2vec.

There are likewise other extra features of libraries that should be looked at. The most significant are detailed hereafter in the following subsections.

## 7.1. OpenKE

OpenKE [[212]](#ref-212) assembles a cohesive and coordinated framework for organizing information and memory. It likewise implements GPU and parallel learning to accelerate model training. It binds together numerical structures for certain models and encapsulates them to be maintained with modular programming. Some highlights are carried out in C++ to maintain extensibility. More KGE models are required to keep up with the stable embeddings of some huge scope KG. It is additionally tough to use as it has no versioning and is not appropriately contained for any package manager.

## 7.2. AmpliGraph

AmpliGraph [[213]](#ref-213) gives instinctive APIs that are intended to decrease the code sum needed to learn models that foresee triples in KG. It depends on TensorFlow and is intended to run flawlessly on CPU and GPU units to accelerate model training. It contains modules that help load KG and provides knowledge discovery API to find new triples, group elements, and explore duplicates. It is also well documented and provides slack support with google colab instructional exercises.

## 7.3. PyTorch BigGraph

PyTorch BigGraph [[214]](#ref-214) was created to circumvent the issue of scalability in huge KG. It provides distributed training on a set of machines and accomplishes this through the segmentation of graphs. Therefore, the models do not need to be stacked entirely in memory. Multithread computation on each machine is working on different subsets of the graph simultaneously with distributed execution across different machines. This enables learning on huge graphs whose embeddings will not fit in a single GPU unit, yet it cannot provide top-notch embeddings for small graphs without careful tuning.

## 7.4. Pykg2vec

Pykg2vec [[210]](#ref-210) provides functions for hyperparameter optimization such as Bayesian optimization with negative sampling techniques in batches, as well as information charts to visualize embeddings and model performance metrics. The mini-batches generated for negative sampling result from employing multiple concurrent cycles that smoothens the batch generation process. These mini-batches are then transferred to a queue to be handled by the model carried out in TensorFlow. The batch generator function runs autonomously so that there is low idleness for faster execution. It likewise pictures the latent portrayals of triples on the 2D plane utilizing t-SNE [[218]](#ref-218), which helps to investigate the model for training KGE's.

## 7.5. LibKGE

The decision of training methodology and hyperparameters are more powerful for model execution regularly more than the class of model itself. LibKGE [[215]](#ref-215) intends to give clean executions for parameter search, assessment techniques, and training that can be utilized with any model. For tuning of parameters, it upholds Bayesian Optimization, grid search, and quasirandom search. Each preparation work or parameter search can be hindered and continued at any time. LibKGE benefits further from its configuration because everything can be treated as a hyperparameter, even the decision of the model and the score function. It performs broad logging in both human and machine-readable formats during analyses and screens execution metrics, such as runtime, memory use, loss, and evaluation metrics.

## 7.6. GraphVite

GraphVite [[216]](#ref-216) extends existing embedding techniques for GPUs and essentially speeds up training to generate embeddings on a single unit. It is centered around multi-GPU and does not support distributed training. It creates a subgraph, moves all the information in the subgraph to GPU memory and performs several mini-batch steps on the subgraph. This strategy minimizes information development between the CPU and GPU at the cost of reducing the liveliness of the embedding, which generally results in much slower convergence.

## 7.7. PyKEEN

PyKEEN [[211]](#ref-211), one of the early programming bundles for KGE modeling, had some issues such as the model should only be modeled under the stochastic neighborhood closed world method. The evaluation technique for large KGs was excessively delayed, and was intended to be used only via the command line interface line. PyKEEN (Python KnowlEdge EmbeddiNgs) 1.0 is a refreshed form that controls the previously mentioned issues and empowers clients to create KGE models dependent on a wide scope of association models, loss functions, distinctive training approaches, and grants the modeling of converse relations. A programmed memory streamlining step is executed that registers the configuration of models and hardware availability to assess batch sizes for the current model arrangement prior to executing the real experimentation. If the user input batch size is too large, then the programmed memory optimization decides the largest sub batch size for execution. Through the integration of Optuna, extensive HPO functionalities are also included.

## 7.8. DGL-KE

DGL-KE [[217]](#ref-217) introduces distinct new advancements that accelerate execution on KGs with large numbers of nodes and billions of edges using distributed parallelism, multiprocessing, and GPUs. These improvements are intended to build information around, reduce overhead, cover calculations with memory ingress, and achieve high efficiency. This bundle is implemented with Python on top of the Deep Graph Library (DGL) [[219]](#ref-219) with a C++ based operable keyvalue store explicitly intended for DGL-KE. Various negative inspection procedures have also been incorporated to create smaller than expected clusters with some embeddings engaged in the batch, which minimizes information movement from memory to processing units.

## 7.9. TORCH-KGE

TORCH-KGE is the most recent software package that has been acknowledged at KDD, which is worth mentioning. It [[220]](#ref-220) is a Python module for KG that completely depends on PyTorch. Its major strength is a rapid evaluation module for link prediction. Extensive consideration is given to improved code proficiency and simplicity, documentation, and API stability.

## Open Research Challenges

| Challenge | Model | Ref. | Description |
|---|---|---|---|
| Interpretability | CRIAGE | [[221]](#ref-221) | Defense mechanism for the automatic identification of a triplet from a graph that |
| | | | may alter the prediction for a target fact by adversarial modifications. |
| | - | [[222]](#ref-222) | Scalable attack mechanism to effectively generate poisoning attacks for KGE |
| | | | models. |
| | IDOpt, IDRank | [[223]](#ref-223) | Defense mechanism for similarity-based link prediction by effectively modeling |
| | | | target links as a Bayesian Stackelberg game. |
| Few Shot Learning | CogKR | [[224]](#ref-224) | Cognitive graph that incorporates dual theory in cognitive science into a |
| | | | reasoning module for one-shot learning. |
| | FSRL | [[225]](#ref-225) | Adopt heterogenous graphs for KGC by utilizing recurrent auto-encoder |
| | | | aggregation. |
| | FTAL | [[226]](#ref-226) | Incorporate the self-attention method to encode temporal dependence and a |
| | | | network to capture similarity scores for temporal graphs |
| | GMatching | [[227]](#ref-227) | One shot learning technique to learn entity embeddings utilizing local neighbor |
| | | | encoder. |
| Hyper Parameter | pykg2vec | [[210]](#ref-210) | Provides built-in automatic Bayesian hyperparameter optimization module to |
| Search | | | detect optimized hyperparameters for model training. |
| | LibKGE | [[215]](#ref-215) | Support quasi random search, grid search, manual search and bayesian |
| | | | optimization, including checkpoint support for model training. |
| Scalability | KGTK | [[228]](#ref-228) | A knowledge graph toolkit aimed at manipulating, deriving and enhancing KGs |
| | | | on a large scale. It provides the KGTK file format using the concept of hyper |
| | | | graphs for effective representation of information. |
| | Marius | [[229]](#ref-229) | A framework built to optimize the data movement using partition caching and |
| | | | BETA data ordering for scalable training. |
| | RDF2Vec Light | [[230]](#ref-230) | An embedding approach built on RDF2VEC to selectively select a subset of |
| | | | triples to generate vectors using a walk generation algorithm. |
| | Cleora | [[231]](#ref-231) | An unsupervised learning approach based on optimizing the embeddings |
| | | | generated by the weighted ensemble of each node locality. |
| Dynamic | NODE | [[232]](#ref-232) | Exploits Neural ordinary differential equations and GNN to capture temporal and |
| Knowledge | | | structure knowledge respectively. |
| | CTDNE | [[233]](#ref-233) | Augmentation of random walk based models to capture the order of edges that |
| | | | moves ahead in time. |
| | SDG | [[234]](#ref-234) | Replace message passing mechanism in GNN by page rank mechanism to |
| | | | capture the dynamic nature in graphs. |
| Knowledge Quality | DSKRL | [[235]](#ref-235) | Proposed dissimilarity and support method for measuring the degree of similarity |
| | | | with its reliability using structural and supporting information. |
| | KGRefiner | [[236]](#ref-236) | Augmenting current nodes by using their hierarchical information for a |
| | | | translation based embedding model to produce more informative graphs. |
| Knowledge | Pretrain-KGE | [[237]](#ref-237) | A universal training framework with three steps namely, fine tuning, feature |
| Transfer | | | extraction and training phase using BERT |

**Table 3:** Towards Open Research Challenges for Knowledge Graph Completion

The knowledge graphs address information in graph components and their associations. The prerequisites for KG emerge in view of the web improvements associated with the advancement of data on the Internet. Despite the various advantages of state-of-the-art KGs, they manage several issues. As shown in Table 3, many open search challenges may choose future assessment titles on knowledge development, refinement, reproducibility, etc. The given subsections have their share of challenges and issues.

## 8.1. Interpretability and Robustness

One of the primary functions of the KGE model is to embed the entities and relations of the KG into a low-dimensional vector space that is semantically meaningful. The embedding learning strategy works primarily by transforming the given vectors into auxiliary embeddings, which use gradient descent at a particular target objective loss. These systems, in any case, fill in as a black box, which is difficult to understand, unlike other approaches based on association rule mining and graph features, which can be deciphered dependent on the highlights they use. Preliminary efforts have been made to make the models more robust for link prediction tasks [[221]](#ref-221) [[222]](#ref-222) [[223]](#ref-223) [[238]](#ref-238). In this way, further work must go into interpretability and work on the reliance of the anticipated information and make the models more robust towards adversarial modifications.

## 8.2. Few Shot Learning

The relationships between the elements in the KG are far from complete, especially for unusual relationships, making it incredibly difficult to capture hidden examples of these relationships. Few shot learning is a technique proposed for learning in case the training data is low, which has previously been shown to have significant performance in image vision tasks [[239]](#ref-239). Few attempts have been made to incorporate few-shot learning strategies into the knowledge graph, aimed at finding hidden examples of a relation with which only certain triples are related [[227]](#ref-227) [[225]](#ref-225) [[224]](#ref-224) [[226]](#ref-226) [[240]](#ref-240). Although these are acceptable efforts, their low performance suggests that few-shot learning in graphs is an open research area.

## 8.3. Hyper Parameter Search

The resultant predictive exactness of KGE embeddings is highly dependent on their hyperparameters [[175]](#ref-175) [[176]](#ref-176). Hence, minor changes in these boundaries can negatively affect the predictive power of KGE models. The way towards tracking down the ideal boundaries of KGE models is customarily accomplished through a brute force parameter search which is time-consuming and inefficient. Thus, their preparation may require a rather novel framework that can optimize the training parameters to segment the optimal search space for each new dataset.

## 8.4. Scalability

Scalability is imperative in a large-scope knowledge graph. With a predetermined number of functions applied to over 1 million elements, there is a compromise between computational effectiveness and model expression. Some embedding strategies use rearrangement to reduce computing costs, for example, HolE[[120]](#ref-120). ExpressGNN [[241]](#ref-241) tries to use NeuralLP [[242]](#ref-242) for efficient rule induction. Nonetheless, there is a need for a more thorough and tailored incorporation of Big Data development frameworks and modern factual models, and this remains an open research area.

## 8.5. Dynamic Knowledge

It targets learning new rationale and interpreting new knowledge developing with time. Existing representation techniques are totally given to reasoning in the static KGs; however, they overlook the dynamic data contained in graphs. Of course, the triples contained in KGs, for example, (Steve Ballmer, CEO of, Microsoft) are not in every case valid over time. Plus, new information is created constantly, which might be infused into KGs progressively. In this manner, dynamic reasoning upon the huge KGs is requested to self-right KGs and mining new rationale techniques consistently. A dynamic information graph, along with methods catching dynamics, may address the restriction of conventional information reasoning and representation by mining the temporal facts.

## 8.6. Knowledge Quality

KGE models form vector embeddings of elements according to their prior information. Therefore, the nature of this information affects the nature of the embeddings created. In fact, it is important to refine the information in KG to maintain its uniformity and accuracy. Refinement is an interaction between the inclusion of missing information and the identification of errors. KG refinement strategies [[243]](#ref-243) distinguish misinformation and allow congruent knowledge.

## 8.7. Knowledge Transfer

Neural reasoning techniques, for example, TransE and ConvE, construct the semantically meaningful embeddings of the facts. The generated embeddings can be transferred to the neurosymbolic reasoning cycle to work on the limit of adaptation to fault tolerance. This reasoning cycle only aims to learn the features as boundaries present in the KG. In simple terms, it cannot be further transferred to some different KG. Lately, the graph neural networks (GNN) have successfully proven to capture the structure knowledge in graphs and transfer this knowledge to other graphs [[244]](#ref-244) [[245]](#ref-245). Roused by the accomplishment of the GNN pre-trained models, the KGE pre-trained model that can catch the adaptable semantics of the entities and relations across various datasets is an open research challenge.

## Applications

Multi-relational graphs, also known as knowledge graphs, have substantially impacted several applications. Their property of delivering semantically organized data has brought important potential answers to some problems and provides excellent solutions. Many works devoted to leveraging KG have set their leanings on dialogue frameworks, recommendation frameworks, and information retrieval systems. Nevertheless, there are certain areas where KG's has wide applications in clinical, monetary, online security, news, and human resources.

## 9.1. Information Retrieval Systems

Recently, more and more web-based search frameworks use KG's fusing rich semantic entity information to help improve query results. It extends web indexing by using complex multirelational information on real records, enriching queries and improving their ability to understand records. For the most part, search frameworks are well organized units to build with improvements over the vast range of knowledge graphs. Experts are investigating the potential of KG for information retrieval in several possible approaches that take advantage of KG's semantics in various segments, for example, query retrieval, document retrieval, and ranking models [[246]](#ref-246) [[247]](#ref-247). Queries can be advanced and expanded by introducing new possibilities from related entities and their attributes, which then improve the function of query retrieval. The authors of [[248]](#ref-248) used this idea by separating features from the elements themselves, and the relationships between entities to information bases, such as organized facts and text, used to advance the query. In document retrieval tasks, an approach to improve and address documents is to create a vector space model of the given elements [[249]](#ref-249). As presented in [[249]](#ref-249), a bag of entity vector space models is introduced in which documents and queries can be addressed using entity information. The authors of [[250]](#ref-250) proposed an entity linking framework to represent documents and questions as a set of semantic ideas, which can then be acted upon downstream tasks. The positioning vector model can also be improved by building various associations from queries to documents through related elements.

## 9.2. Recommender Systems

It has been observed that the amount of online information like pictures, news and items is expanding, which brings confusion and issues for the users. Recommendation frameworks reduce the data overload faced by people emerging in this decade. These frameworks typically rely on collaborative filtering strategies, which dissect customers' prehistoric data and preferences. In any case, the primary impediment of exploiting this approach is that it experiences the sparsity of users' information and is computationally costly to prepare. The idea of side data can be used by recommendation systems by adopting knowledge graphs that deal with the issues mentioned earlier. KG can help improve accuracy, interpretability, and increase the variety of things recommended.

KGE models are utilized to preprocess the KG by displaying the learned entity embeddings to a recommendation framework [[251]](#ref-251) [[252]](#ref-252) [[253]](#ref-253). Hongwei Wang et al. [[251]](#ref-251) proposed a content-based deep knowledge aware network (DKN) for news recommendation. The work [[252]](#ref-252) developed a collaborative knowledge-based embedding (CKE) model by extracting semantic representation of items from past knowledge leveraging TransR. It considers the heterogeneity of both nodes and relationships, textual content, and visual content by utilizing stacked denoising and convolutional auto-encoders. A multi-task feature learning approach (MKR) is introduced in [[253]](#ref-253) for augmenting the recommendation leveraging knowledge graph embeddings. KGE based strategies have high adaptability in recommendation systems; however, the significant disadvantage is that they have no side data other than text. To provide additional information for recommendation, graph algorithms and path-based methods have also been employed to track significant associations between nodes in a knowledge graph [[254]](#ref-254) [[255]](#ref-255). The above strategies are acceptable in making KG more general and intuitive to use. However, manual meta path feature extraction is generally troublesome and difficult to optimize practically. These techniques are also impossible where entities are relationships are not inside one realm like news suggestions.

## 9.3. Questions Answering Systems

Multi-relational graphs can be employ to upgrade indexed results to what is referred to as a question-and-answer (QA) system. For example, a QA framework, 'Watson', is built by IBM using YAGO [[15]](#ref-15) and DBpedia [[6]](#ref-6). The QA systems are divided into types namely, semantic-based, information retrieval-based, embedding-based, and deep learning-based [[53]](#ref-53). In a semantic-based QA framework, the semantics of the query can be communicated by turning standard language-based questions into logic structures. Then organized questions are prepared to elicit answers through the knowledge graph [[256]](#ref-256) [[13]](#ref-13). Semantic parsing strategy shows excellent performance when managing complex queries. But, it relies on vast highlights or features being hand-made for semantic parsers, which restricts the application areas and versatility of their technology.

QA noting frameworks that are information retrieval based aim to automatically interpret given inquiries into organized questions to retrieve the arrangement of candidate answers from multi-relational graphs. Then, the attributes are extracted from the questions, and candidates can identify the correct answers and rank them. Information retrieval-based techniques rely more on natural language semantics and help manage basic queries. When compared with semantic and data retrieval strategy, the embedding-based model yields good results without hand-generated features or additional frameworks for grammatically labeling, dependencies, and syntactic parsing during preparation. Nonetheless, it overlooks word order data and cannot handle convoluted inquiries [[257]](#ref-257).

Since the advent of deep learning models for natural language processing tasks, researchers have been attempting to take advantage of neural nets to perform QA tasks. It aims to reduce the over-reliance on hand-crafted features, which are time-consuming. A multi-channel CNN method for retrieving information is proposed [[258]](#ref-258). The concept of embedding and information retrieval techniques was adopted to reduce semantic parsing for query graph generation [[259]](#ref-259). Bidirectional LSTM is applied by Zhang et al. [[260]](#ref-260) to get familiar with the representations of queries leveraging embedding-based methods.

Regular QA framework can be seen as a single round response framework by formulating correct answers in the form of feedback. However, dialogue frameworks are in advance because of their potential to quickly create multi-round responses through semantic enhancements and KG walks. An encoder–decoder structure-based graph attention component has been proposed by Liu et al. [[261]](#ref-261) to encode the data to enhance the semantic representation. The literature proposed [[262]](#ref-262) to learn logical progressions in turn via representative knowledge graphs navigating to the anticipated response with the attention graph path-based decoder. Semantic parsing through formal logical representation is another heading for dialogue frameworks [[263]](#ref-263); in any case, they are difficult to parse and interpret.

## 9.4. Other Applications

## 9.4.1. Health Informatics

Clinical data is evolving rapidly, and natural language information is quite common and occupies an important place in the health informatics framework. Endeavors have been made to use the accessible data into knowledge graphs to furnish frameworks with extricating and compiling clinical information accurately and speedily. A strategy for creating a huge-scope biomedical KG was proposed by Ernst et al. [[264]](#ref-264). The health information was effectively coordinated into a heterogeneous literary information graph in [[265]](#ref-265). A method has been proposed by Rotmensch et al. [[266]](#ref-266) to effectively exploit the knowledge in electronic medical records to map diseases with symptoms automatically. The previously mentioned approaches help build largescale knowledge graphs taking into account the standard clinical terminology. But, especially for dialects like Chinese, the standards are not necessarily met. This brings about the relatively low accuracy of clinical KG in such dialects.

## 9.4.2. Drug Discovery

Drug development is a difficult and costly cycle, from gene distinguishing evidence to quality checks and identifying a compound for experimentation on subjects. Inherent progress of a gene or drug requires many years and can result in loss of time and resources if not identified effectively. Drug developers identify genes and drugs by reading the most recent literature before continuing with the experiment. In any case, it is profoundly reliant upon the experience of the specialists. Knowledge graph embeddings can be used to deal with these issues [[7]](#ref-7) [[267]](#ref-267). A knowledge graph can be created based on a genetic approach by combining different genes and their associations for a particular disease. The KGE's can then be employed to learn complex interactions from graphs and make link predictions to predict associations present in the dataset. It will follow some priority-based ranking protocols and list the priority genes in hierarchical order of calibration. The drug designer may then discover the confirmation behind the expected results and continue working accordingly.

## 9.4.3. Covid-19

The current worldwide emergency brought about by COVID-19 nearly stopped normal life in many places of the world. As of September 1, over 220 million individuals were infected, and the quantity of COVID-19 patients is drastically expanding. The shortage of medical supplies is at its peak and has likewise turned into a significant challenge [[268]](#ref-268). Knowledge Graphs (KG) have been demonstrated to effectively look through the overwhelming volume of COVID-19 literature and gain actionable understanding, which would either be very monotonous or difficult to accomplish without leveraging AI. The applications are comprehensively sorted into primary parts, i.e., in Drug Repurposing and Knowledge Graph Construction [[269]](#ref-269). In Drug repurposing, the task is to locate potential medications to repurpose for COVID-19 utilizing literature determined information and KGC methods [[270]](#ref-270). The latter task involves building a knowledge graph to facilitate literature search [[271]](#ref-271).

## 9.4.4. Human Rescource

Technology is advancing at an astonishingly high speed, and job seekers need to acquire new capabilities to be relevant in the marketplace. But due to automation, many jobs are becoming obsolete, and organizations are forced to lay off people. The KGE's can be used to propose new technologies or tasks to professionals and suggest comparable roles and skills within the organization [[272]](#ref-272). It can also estimate the relationship between entities in monetary business areas and deduce recognized patterns in knowledge.

## 9.4.5. Knowledge Protection

Advances in information technology are at their peak, resulting in the need to prevent cyber attacks from securing the system fully. Increasingly more examination work is done leveraging KG's associated with cyber security to identify and anticipate dynamic attacks and protect individuals' data. A five-level model introduced by Jian et al. [[273]](#ref-273) is built on a network security knowledge graph that aims to obtain updated knowledge using path ranking algorithms. The study [[274]](#ref-274) shows patterns associated with digital attacks and breaks down links between attacks, incidents, and precautions by elevating the nature of the incident. The given approaches are more focused on the development of data security KG. Nevertheless, how to isolate digital security incidents using KG's indistinguishable information thought capability and rapidly update KG with new improvements by researchers requires further exploration in the future.

## Conclusion

Knowledge Graph Completion (KGC) is an intriguing issue in KG development and related applications, which expects to construct KG by foreseeing the missing relationships and entities. The thought behind introducing a paper like this was to conduct an examination that assembles all cutting-edge approaches on the knowledge graphs for link prediction. To the best of our knowledge, this paper is one of only a handful of works that systemically give an outline on knowledge graph completion from various methodologies such as conventional statistical relational learning, probabilistic graphical models, rule mining, and graph representation learning techniques.

Knowledge graph embeddings (KGE), as the innovation of feeding triples into a low-dimensional consistent vector space, has gained astounding headway in offering exact, viable, and underlying portrayal of data in numerous fields. We explored primary advances of KGE, sorted the current scoring capacities into three kinds, namely, translation, factorization, and deeper scoring functions, and afterward outlined the benefits and weaknesses of embedding models in every class. Techniques based on reinforcement learning like DeepPath, Minerva, M-Walk, DAPath, and many more are also reviewed and discussed to estimate complex queries in the link prediction task.

When seeing examination papers and conversing with specialists in link prediction, we discovered a slight disconnect between what analysts accept best in class and what really is cutting edge. Along these lines, a comparative analysis is given to help fellow researchers to comprehend the less explored areas like calibration, reciprocal relations, and different training strategies. Our work is efficient, simple to study, and contains detailed figures and tables. A bird's eye view of the current state-of-the-art models on KGC for temporal, uncertain, and multimodal knowledge graphs is also discussed. Next, we compared recently published software packages for model training and open research challenges, also discussed to guide future research.

We firmly accept that this literature will help researchers influence our findings and act as stepping stones to push the cutting edge. Even though, there are a few impediments in this work because of space and time constraints. This study centered around the KGE for link prediction; we will investigate more research areas of Knowledge graph completion in later versions, like triple classification, entity classification, etc. Additionally, we emphasize static KG; we will explore new model designs, like dynamic, heterogeneous, and bipartite graphs.

## References

*   <a id="ref-1"></a>[1] A. Hogan, E. Blomqvist, M. Cochez, C. d'Amato, G. D. Melo, C. Gutierrez, S. Kirrane, J. E. L. Gayo, R. Navigli, S. Neumaier, et al., Knowledge graphs, ACM Computing Surveys (CSUR) 54 (2021) 1–37.
*   <a id="ref-2"></a>[2] E. S. MYCIN, Computer-based medical consultations, 1976.
*   <a id="ref-3"></a>[3] M. Nickel, K. Murphy, V. Tresp, E. Gabrilovich, A review of relational machine learning for knowledge graphs, Proceedings of the IEEE 104 (2015) 11–33.
*   <a id="ref-4"></a>[4] S. Ji, S. Pan, E. Cambria, P. Marttinen, S. Y. Philip, A survey on knowledge graphs: Representation, acquisition, and applications, IEEE Transactions on Neural Networks and Learning Systems (2021).
*   <a id="ref-5"></a>[5] Z. Chen, Y. Wang, B. Zhao, J. Cheng, X. Zhao, Z. Duan, Knowledge graph completion: A review, IEEE Access 8 (2020) 192435–192456.
*   <a id="ref-6"></a>[6] C. Bizer, J. Lehmann, G. Kobilarov, S. Auer, C. Becker, R. Cyganiak, S. Hellmann, Dbpedia-a crystallization point for the web of data, Journal of web semantics 7 (2009) 154–165.
*   <a id="ref-7"></a>[7] S. K. Mohamed, V. Novácek, A. Nounu, Discovering protein drug targets using knowledge graph embeddings, ˇ Bioinformatics 36 (2020) 603–610.
*   <a id="ref-8"></a>[8] G. Luo, X. Huang, C.-Y. Lin, Z. Nie, Joint entity recognition and disambiguation, in: Proceedings of the 2015 Conference on Empirical Methods in Natural Language Processing, pp. 879–888.
*   <a id="ref-9"></a>[9] W. Shen, J. Wang, J. Han, Entity linking with a knowledge base: Issues, techniques, and solutions, IEEE Transactions on Knowledge and Data Engineering 27 (2014) 443–460.
*   <a id="ref-10"></a>[10] H. He, A. Balakrishnan, M. Eric, P. Liang, Learning symmetric collaborative dialogue agents with dynamic knowledge graph embeddings, arXiv preprint arXiv:1704.07130 (2017).
*   <a id="ref-11"></a>[11] J. Krishnamurthy, T. Mitchell, Weakly supervised training of semantic parsers, in: Proceedings of the 2012 Joint Conference on Empirical Methods in Natural Language Processing and Computational Natural Language Learning, pp. 754–765.
*   <a id="ref-12"></a>[12] R. Reinanda, E. Meij, M. de Rijke, et al., Knowledge graphs: An information retrieval perspective, Now Publishers, 2020.
*   <a id="ref-13"></a>[13] A. Fader, L. Zettlemoyer, O. Etzioni, Open question answering over curated and extracted knowledge bases, in: Proceedings of the 20th ACM SIGKDD international conference on Knowledge discovery and data mining, pp. 1156–1165.
*   <a id="ref-14"></a>[14] G. O. Consortium, Expansion of the gene ontology knowledgebase and resources, Nucleic acids research 45 (2017) D331–D338.
*   <a id="ref-15"></a>[15] F. M. Suchanek, G. Kasneci, G. Weikum, Yago: A large ontology from wikipedia and wordnet, Journal of Web Semantics 6 (2008) 203–217.
*   <a id="ref-16"></a>[16] K. Bollacker, R. Cook, P. Tufts, Freebase: A shared database of structured general human knowledge, in: AAAI, volume 7, pp. 1962–1963.
*   <a id="ref-17"></a>[17] G. A. Miller, WordNet: An electronic lexical database, MIT press, 1998.
*   <a id="ref-18"></a>[18] A. Carlson, J. Betteridge, B. Kisiel, B. Settles, E. R. Hruschka, T. M. Mitchell, Toward an architecture for never-ending language learning, in: Twenty-Fourth AAAI conference on artificial intelligence.
*   <a id="ref-19"></a>[19] M. D. Ward, A. Beger, J. Cutler, M. Dickenson, C. Dorff, B. Radford, Comparing gdelt and icews event data, Analysis 21 (2013) 267–297.
*   <a id="ref-20"></a>[20] D. Vrandeciˇ c, M. Krötzsch, Wikidata: a free collaborative knowledgebase, Communications of the ACM 57 ´ (2014) 78–85.
*   <a id="ref-21"></a>[21] H. Overland, What is facebook open graph, Online: http://www. searchenginepeople. com/blog/what-is-facebookopen-graph. html# ixzz1fHZXna2C [09 December 2011] (2011).
*   <a id="ref-22"></a>[22] R. West, E. Gabrilovich, K. Murphy, S. Sun, R. Gupta, D. Lin, Knowledge base completion via search-based question answering, in: Proceedings of the 23rd international conference on World wide web, pp. 515–526.
*   <a id="ref-23"></a>[23] D. Krompaß, S. Baier, V. Tresp, Type-constrained representation learning in knowledge graphs, in: International semantic web conference, Springer, pp. 640–655.
*   <a id="ref-24"></a>[24] E. Shijia, S. Jia, Y. Xiang, Z. Ji, Knowledge graph embedding for link prediction and triplet classification, in: China Conference on Knowledge Graph and Semantic Computing, Springer, pp. 228–232.
*   <a id="ref-25"></a>[25] M. Bilgic, G. M. Namata, L. Getoor, Combining collective classification and link prediction, in: Seventh IEEE International Conference on Data Mining Workshops (ICDMW 2007), IEEE, pp. 381–386.
*   <a id="ref-26"></a>[26] A. Saeedi, E. Peukert, E. Rahm, Using link features for entity clustering in knowledge graphs, in: European Semantic Web Conference, Springer, pp. 576–592.
*   <a id="ref-27"></a>[27] M. Pershina, M. Yakout, K. Chakrabarti, Holistic entity matching across knowledge graphs, in: 2015 IEEE International Conference on Big Data (Big Data), IEEE, pp. 1585–1590.
*   <a id="ref-28"></a>[28] K.-W. Chang, W.-t. Yih, B. Yang, C. Meek, Typed tensor decomposition of knowledge bases for relation extraction, in: Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing (EMNLP), pp. 1568–1579.
*   <a id="ref-29"></a>[29] N. Lao, T. Mitchell, W. Cohen, Random walk inference and learning in a large scale knowledge base, in: Proceedings of the 2011 conference on empirical methods in natural language processing, pp. 529–539.
*   <a id="ref-30"></a>[30] Q. Wang, Z. Mao, B. Wang, L. Guo, Knowledge graph embedding: A survey of approaches and applications, IEEE Transactions on Knowledge and Data Engineering 29 (2017) 2724–2743.
*   <a id="ref-31"></a>[31] A. Bordes, N. Usunier, A. Garcia-Duran, J. Weston, O. Yakhnenko, Translating embeddings for modeling multirelational data, Advances in neural information processing systems 26 (2013).
*   <a id="ref-32"></a>[32] Z. Wang, J. Zhang, J. Feng, Z. Chen, Knowledge graph embedding by translating on hyperplanes, in: Proceedings of the AAAI Conference on Artificial Intelligence, volume 28.
*   <a id="ref-33"></a>[33] Y. Lin, Z. Liu, M. Sun, Y. Liu, X. Zhu, Learning entity and relation embeddings for knowledge graph completion, in: Twenty-ninth AAAI conference on artificial intelligence.
*   <a id="ref-34"></a>[34] G. Ji, S. He, L. Xu, K. Liu, J. Zhao, Knowledge graph embedding via dynamic mapping matrix, in: Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), pp. 687–696.
*   <a id="ref-35"></a>[35] G. Ji, K. Liu, S. He, J. Zhao, Knowledge graph completion with adaptive sparse transfer matrix, in: Thirtieth AAAI conference on artificial intelligence.
*   <a id="ref-36"></a>[36] B. Yang, W.-t. Yih, X. He, J. Gao, L. Deng, Embedding entities and relations for learning and inference in knowledge bases, arXiv preprint arXiv:1412.6575 (2014).
*   <a id="ref-37"></a>[37] M. Nickel, V. Tresp, H.-P. Kriegel, A three-way model for collective learning on multi-relational data, in: Icml.
*   <a id="ref-38"></a>[38] T. Trouillon, J. Welbl, S. Riedel, É. Gaussier, G. Bouchard, Complex embeddings for simple link prediction, in: International conference on machine learning, PMLR, pp. 2071–2080.
*   <a id="ref-39"></a>[39] D. Q. Nguyen, T. D. Nguyen, D. Q. Nguyen, D. Phung, A novel embedding model for knowledge base completion based on convolutional neural network, arXiv preprint arXiv:1712.02121 (2017).
*   <a id="ref-40"></a>[40] T. Dettmers, P. Minervini, P. Stenetorp, S. Riedel, Convolutional 2d knowledge graph embeddings, in: Thirtysecond AAAI conference on artificial intelligence.
*   <a id="ref-41"></a>[41] I. Balaževic, C. Allen, T. M. Hospedales, Hypernetwork knowledge graph embeddings, in: International Confer- ´ ence on Artificial Neural Networks, Springer, pp. 553–565.
*   <a id="ref-42"></a>[42] M. Wang, L. Qiu, X. Wang, A survey on knowledge graph embeddings for link prediction, Symmetry 13 (2021) 485.
*   <a id="ref-43"></a>[43] Y. Dai, S. Wang, N. N. Xiong, W. Guo, A survey on knowledge graph embedding: Approaches, applications and benchmarks, Electronics 9 (2020) 750.
*   <a id="ref-44"></a>[44] T. Safavi, D. Koutra, E. Meij, Evaluating the calibration of knowledge graph embeddings for trustworthy link prediction, arXiv preprint arXiv:2004.01168 (2020).
*   <a id="ref-45"></a>[45] K. Wang, Y. Liu, Q. Z. Sheng, Neighborhood intervention consistency: Measuring confidence for knowledge graph link prediction (????).
*   <a id="ref-46"></a>[46] F. Scarselli, M. Gori, A. C. Tsoi, M. Hagenbuchner, G. Monfardini, The graph neural network model, IEEE transactions on neural networks 20 (2008) 61–80.
*   <a id="ref-47"></a>[47] P. Pezeshkpour, L. Chen, S. Singh, Embedding multimodal relational data for knowledge base completion, arXiv preprint arXiv:1809.01341 (2018).
*   <a id="ref-48"></a>[48] A. Rossi, D. Barbosa, D. Firmani, A. Matinata, P. Merialdo, Knowledge graph embedding for link prediction: A comparative analysis, ACM Transactions on Knowledge Discovery from Data (TKDD) 15 (2021) 1–49.
*   <a id="ref-49"></a>[49] G. A. Gesese, R. Biswas, M. Alam, H. Sack, A survey on knowledge graph embeddings with literals: Which model links better literal-ly?, Semantic Web (2019) 1–31.
*   <a id="ref-50"></a>[50] A. García-Durán, M. Niepert, Kblrn: End-to-end learning of knowledge base representations with latent, relational, and numerical features, arXiv preprint arXiv:1709.04676 (2017).
*   <a id="ref-51"></a>[51] A. Kristiadi, M. A. Khan, D. Lukovnikov, J. Lehmann, A. Fischer, Incorporating literals into knowledge graph embeddings, in: International Semantic Web Conference, Springer, pp. 347–363.
*   <a id="ref-52"></a>[52] B. Abu-Salih, Domain-specific knowledge graphs: A survey, Journal of Network and Computer Applications 185 (2021) 103076.
*   <a id="ref-53"></a>[53] X. Zou, A survey on application of knowledge graph, in: Journal of Physics: Conference Series, volume 1487, IOP Publishing, p. 012016.
*   <a id="ref-54"></a>[54] A. Popescul, L. H. Ungar, Statistical relational learning for link prediction, in: IJCAI workshop on learning statistical models from relational data, volume 2003, Citeseer.
*   <a id="ref-55"></a>[55] C. Yu, X. Zhao, L. An, X. Lin, Similarity-based link prediction in social networks: A path and node combined approach, Journal of Information Science 43 (2017) 683–695.
*   <a id="ref-56"></a>[56] N. Lavrac, S. Dzeroski, Inductive logic programming., in: WLP, Springer, pp. 146–160.
*   <a id="ref-57"></a>[57] L. A. Galárraga, N. Preda, F. M. Suchanek, Mining rules to align knowledge bases, in: Proceedings of the 2013 workshop on Automated knowledge base construction, pp. 43–48.
*   <a id="ref-58"></a>[58] L. E. Sucar, Probabilistic graphical models, Advances in Computer Vision and Pattern Recognition. London: Springer London. doi 10 (2015) 1.
*   <a id="ref-59"></a>[59] R. Kaushik, P. Shenoy, P. Bohannon, E. Gudes, Exploiting local similarity for indexing paths in graph-structured data, in: Proceedings 18th International Conference on Data Engineering, IEEE, pp. 129–140.
*   <a id="ref-60"></a>[60] D. Anand, K. K. Bharadwaj, Exploring graph-based global similarity estimates for quality recommendations, International journal of computational science and engineering 9 (2014) 188–197.
*   <a id="ref-61"></a>[61] X. Liu, N. Kertkeidkachorn, T. Murata, K.-S. Kim, J. Leblay, S. Lynden, Network embedding based on a quasilocal similarity measure, in: Pacific Rim International Conference on Artificial Intelligence, Springer, pp. 429– 440.
*   <a id="ref-62"></a>[62] L. A. Adamic, E. Adar, Friends and neighbors on the web, Social networks 25 (2003) 211–230.
*   <a id="ref-63"></a>[63] P. Jaccard, Étude comparative de la distribution florale dans une portion des alpes et des jura, Bull Soc Vaudoise Sci Nat 37 (1901) 547–579.
*   <a id="ref-64"></a>[64] G. G. Chowdhury, Introduction to modern information retrieval, Facet publishing, 2010.
*   <a id="ref-65"></a>[65] M. E. Newman, Clustering and preferential attachment in growing networks, Physical review E 64 (2001) 025102.
*   <a id="ref-66"></a>[66] L. Katz, A new status index derived from sociometric analysis, Psychometrika 18 (1953) 39–43.
*   <a id="ref-67"></a>[67] G. Jeh, J. Widom, Simrank: a measure of structural-context similarity, in: Proceedings of the eighth ACM SIGKDD international conference on Knowledge discovery and data mining, pp. 538–543.
*   <a id="ref-68"></a>[68] P. Wang, B. Xu, Y. Wu, X. Zhou, Link prediction in social networks: the state-of-the-art, Science China Information Sciences 58 (2015) 1–38.
*   <a id="ref-69"></a>[69] L. Lü, T. Zhou, Link prediction in weighted networks: The role of weak ties, EPL (Europhysics Letters) 89 (2010) 18001.
*   <a id="ref-70"></a>[70] T. Zhou, L. Lü, Y.-C. Zhang, Predicting missing links via local information, The European Physical Journal B 71 (2009) 623–630.
*   <a id="ref-71"></a>[71] A. Papadimitriou, P. Symeonidis, Y. Manolopoulos, Fast and accurate link prediction in social networking systems, Journal of Systems and Software 85 (2012) 2119–2132.
*   <a id="ref-72"></a>[72] W. Liu, L. Lü, Link prediction based on local random walk, EPL (Europhysics Letters) 89 (2010) 58007.
*   <a id="ref-73"></a>[73] D. Stepanova, M. H. Gad-Elrab, V. T. Ho, Rule induction and reasoning over knowledge graphs, in: Reasoning Web International Summer School, Springer, pp. 142–172.
*   <a id="ref-74"></a>[74] A. Srinivasan, The aleph manual, 2001.
*   <a id="ref-75"></a>[75] S. Muggleton, W. Buntine, Machine invention of first-order predicates by inverting resolution, in: Machine Learning Proceedings 1988, Elsevier, 1988, pp. 339–352.
*   <a id="ref-76"></a>[76] L. De Raedt, M. Bruynooghe, Clint: a multi-strategy interactive concept-learner and theory revision system, in: Proceedings of the Multi-Strategy Learning Workshop, Virginia, pp. 175–191.
*   <a id="ref-77"></a>[77] S. Džeroski, N. Lavrac, Learning relations from noisy examples: An empirical comparison of linus and foil, in: ˇ Machine Learning Proceedings 1991, Elsevier, 1991, pp. 399–402.
*   <a id="ref-78"></a>[78] A. Cropper, S. H. Muggleton, Learning efficient logic programs, Machine Learning 108 (2019) 1063–1083.
*   <a id="ref-79"></a>[79] M. Law, A. Russo, K. Broda, The ilasp system for learning answer set programs, 2015.
*   <a id="ref-80"></a>[80] N. Katzouris, A. Artikis, G. Paliouras, Incremental learning of event definitions with inductive logic programming, Machine Learning 100 (2015) 555–585.
*   <a id="ref-81"></a>[81] L. Galárraga, C. Teflioudi, K. Hose, F. M. Suchanek, Fast rule mining in ontological knowledge bases with amie + +, The VLDB Journal 24 (2015) 707–730.
*   <a id="ref-82"></a>[82] Z. Wang, J. Li, Rdf2rules: Learning rules from rdf knowledge bases by mining frequent predicate cycles, arXiv preprint arXiv:1512.07734 (2015).
*   <a id="ref-83"></a>[83] H. Lu, Y. Zhidu, W. Yujie, et al., Link prediction of knowledge graph based on bayesian network, Journal of Frontiers of Computer Science and Technology 11 (2017) 742–751.
*   <a id="ref-84"></a>[84] N. Lao, W. W. Cohen, Relational retrieval using a combination of path-constrained random walks, Machine learning 81 (2010) 53–67.
*   <a id="ref-85"></a>[85] H. Kashima, N. Abe, A parameterized probabilistic model of network evolution for supervised link prediction, in: Sixth International Conference on Data Mining (ICDM'06), IEEE, pp. 340–349.
*   <a id="ref-86"></a>[86] A. Goldenberg, A. X. Zheng, S. E. Fienberg, E. M. Airoldi, A survey of statistical network models (2010).
*   <a id="ref-87"></a>[87] E. Ravasz, A.-L. Barabási, Hierarchical organization in complex networks, Physical review E 67 (2003) 026112.
*   <a id="ref-88"></a>[88] C. Wang, V. Satuluri, S. Parthasarathy, Local probabilistic models for link prediction, in: Seventh IEEE international conference on data mining (ICDM 2007), IEEE, pp. 322–331.
*   <a id="ref-89"></a>[89] M. Al Hasan, M. J. Zaki, A survey of link prediction in social networks, in: Social network data analytics, Springer, 2011, pp. 243–275.
*   <a id="ref-90"></a>[90] B. Taskar, P. Abbeel, D. Koller, Discriminative probabilistic models for relational data, arXiv preprint arXiv:1301.0604 (2012).
*   <a id="ref-91"></a>[91] D. Koller, N. Friedman, S. Džeroski, C. Sutton, A. McCallum, A. Pfeffer, P. Abbeel, M.-F. Wong, C. Meek, J. Neville, et al., Introduction to statistical relational learning, MIT press, 2007.
*   <a id="ref-92"></a>[92] D. Heckerman, C. Meek, D. Koller, Probabilistic entity-relationship models, prms, and plate models, Introduction to statistical relational learning 2007 (2007) 201–238.
*   <a id="ref-93"></a>[93] D. Heckerman, C. Meek, D. Koller, Probabilistic models for relational data, Technical Report, Citeseer, 2004.
*   <a id="ref-94"></a>[94] D. Wang, P. Cui, W. Zhu, Structural deep network embedding, in: Proceedings of the 22nd ACM SIGKDD international conference on Knowledge discovery and data mining, pp. 1225–1234.
*   <a id="ref-95"></a>[95] J. Tang, M. Qu, M. Wang, M. Zhang, J. Yan, Q. Mei, Line: Large-scale information network embedding, in: Proceedings of the 24th international conference on world wide web, pp. 1067–1077.
*   <a id="ref-96"></a>[96] W. L. Hamilton, Graph representation learning, Synthesis Lectures on Artifical Intelligence and Machine Learning 14 (2020) 1–159.
*   <a id="ref-97"></a>[97] M. Belkin, P. Niyogi, Laplacian eigenmaps and spectral techniques for embedding and clustering., in: Nips, volume 14, pp. 585–591.
*   <a id="ref-98"></a>[98] S. Albawi, T. A. Mohammed, S. Al-Zawi, Understanding of a convolutional neural network, in: 2017 International Conference on Engineering and Technology (ICET), Ieee, pp. 1–6.
*   <a id="ref-99"></a>[99] T. Mikolov, M. Karafiát, L. Burget, J. Cernock ˇ y, S. Khudanpur, Recurrent neural network based language model, ` in: Eleventh annual conference of the international speech communication association.
*   <a id="ref-100"></a>[100] Y. Goldberg, O. Levy, word2vec explained: deriving mikolov et al.'s negative-sampling word-embedding method, arXiv preprint arXiv:1402.3722 (2014).
*   <a id="ref-101"></a>[101] S. Fortin, The graph isomorphism problem (1996).
*   <a id="ref-102"></a>[102] W. L. Hamilton, R. Ying, J. Leskovec, Representation learning on graphs: Methods and applications, arXiv preprint arXiv:1709.05584 (2017).
*   <a id="ref-103"></a>[103] H. Abdi, Singular value decomposition (svd) and generalized singular value decomposition, Encyclopedia of measurement and statistics (2007) 907–912.
*   <a id="ref-104"></a>[104] A. Ahmed, N. Shervashidze, S. Narayanamurthy, V. Josifovski, A. J. Smola, Distributed large-scale natural graph factorization, in: Proceedings of the 22nd international conference on World Wide Web, pp. 37–48.
*   <a id="ref-105"></a>[105] M. Ou, P. Cui, J. Pei, Z. Zhang, W. Zhu, Asymmetric transitivity preserving graph embedding, in: Proceedings of the 22nd ACM SIGKDD international conference on Knowledge discovery and data mining, pp. 1105–1114.
*   <a id="ref-106"></a>[106] B. Perozzi, R. Al-Rfou, S. Skiena, Deepwalk: Online learning of social representations, in: Proceedings of the 20th ACM SIGKDD international conference on Knowledge discovery and data mining, pp. 701–710.
*   <a id="ref-107"></a>[107] A. Grover, J. Leskovec, node2vec: Scalable feature learning for networks, in: Proceedings of the 22nd ACM SIGKDD international conference on Knowledge discovery and data mining, pp. 855–864.
*   <a id="ref-108"></a>[108] M. Ponti, J. Kittler, M. Riva, T. de Campos, C. Zor, A decision cognizant kullback–leibler divergence, Pattern Recognition 61 (2017) 470–478.
*   <a id="ref-109"></a>[109] H. Chen, B. Perozzi, Y. Hu, S. Skiena, Harp: Hierarchical representation learning for networks, in: Proceedings of the AAAI Conference on Artificial Intelligence, volume 32.
*   <a id="ref-110"></a>[110] M. Zhang, Y. Chen, Link prediction based on graph neural networks, Advances in Neural Information Processing Systems 31 (2018) 5165–5175.
*   <a id="ref-111"></a>[111] C. Zhang, D. Song, C. Huang, A. Swami, N. V. Chawla, Heterogeneous graph neural network, in: Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, pp. 793–803.
*   <a id="ref-112"></a>[112] Y. Han, Q. Fang, J. Hu, S. Qian, C. Xu, Gaeat: Graph auto-encoder attention networks for knowledge graph completion, in: Proceedings of the 29th ACM International Conference on Information & Knowledge Management, pp. 2053–2056.
*   <a id="ref-113"></a>[113] T. N. Kipf, M. Welling, Variational graph auto-encoders, arXiv preprint arXiv:1611.07308 (2016).
*   <a id="ref-114"></a>[114] R. v. d. Berg, T. N. Kipf, M. Welling, Graph convolutional matrix completion, arXiv preprint arXiv:1706.02263 (2017).
*   <a id="ref-115"></a>[115] S. Pan, R. Hu, G. Long, J. Jiang, L. Yao, C. Zhang, Adversarially regularized graph autoencoder for graph embedding, arXiv preprint arXiv:1802.04407 (2018).
*   <a id="ref-116"></a>[116] S. Cao, W. Lu, Q. Xu, Deep neural networks for learning graph representations, in: Proceedings of the AAAI Conference on Artificial Intelligence, volume 30.
*   <a id="ref-117"></a>[117] W.-L. Chiang, X. Liu, S. Si, Y. Li, S. Bengio, C.-J. Hsieh, Cluster-gcn: An efficient algorithm for training deep and large graph convolutional networks, in: Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, pp. 257–266.
*   <a id="ref-118"></a>[118] W. L. Hamilton, R. Ying, J. Leskovec, Inductive representation learning on large graphs, in: Proceedings of the 31st International Conference on Neural Information Processing Systems, pp. 1025–1035.
*   <a id="ref-119"></a>[119] M. Schlichtkrull, T. N. Kipf, P. Bloem, R. Van Den Berg, I. Titov, M. Welling, Modeling relational data with graph convolutional networks, in: European semantic web conference, Springer, pp. 593–607.
*   <a id="ref-120"></a>[120] M. Nickel, L. Rosasco, T. Poggio, Holographic embeddings of knowledge graphs, in: Proceedings of the AAAI Conference on Artificial Intelligence, volume 30.
*   <a id="ref-121"></a>[121] Z. Sun, Z.-H. Deng, J.-Y. Nie, J. Tang, Rotate: Knowledge graph embedding by relational rotation in complex space, arXiv preprint arXiv:1902.10197 (2019).
*   <a id="ref-122"></a>[122] X. Dong, E. Gabrilovich, G. Heitz, W. Horn, N. Lao, K. Murphy, T. Strohmann, S. Sun, W. Zhang, Knowledge vault: A web-scale approach to probabilistic knowledge fusion, in: Proceedings of the 20th ACM SIGKDD international conference on Knowledge discovery and data mining, pp. 601–610.
*   <a id="ref-123"></a>[123] J. Qian, G. Li, K. Atkinson, Y. Yue, Negative sampling in knowledge representation learning: Amini-review (????).
*   <a id="ref-124"></a>[124] L. Cai, W. Y. Wang, Kbgan: Adversarial learning for knowledge graph embeddings, arXiv preprint arXiv:1711.04071 (2017).
*   <a id="ref-125"></a>[125] P. Wang, S. Li, R. Pan, Incorporating gan for negative sampling in knowledge representation learning, in: Proceedings of the AAAI Conference on Artificial Intelligence, volume 32.
*   <a id="ref-126"></a>[126] Y. Zhang, Q. Yao, Y. Shao, L. Chen, Nscaching: simple and efficient negative sampling for knowledge graph embedding, in: 2019 IEEE 35th International Conference on Data Engineering (ICDE), IEEE, pp. 614–625.
*   <a id="ref-127"></a>[127] V. Kanojia, H. Maeda, R. Togashi, S. Fujita, Enhancing knowledge graph embedding with probabilistic negative sampling, in: Proceedings of the 26th International Conference on World Wide Web Companion, pp. 801–802.
*   <a id="ref-128"></a>[128] L. Cai, W. Y. Wang, Kbgan: Adversarial learning for knowledge graph embeddings, in: Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers), pp. 1470–1480.
*   <a id="ref-129"></a>[129] I. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley, S. Ozair, A. Courville, Y. Bengio, Generative adversarial nets, Advances in neural information processing systems 27 (2014).
*   <a id="ref-130"></a>[130] D. Q. Nguyen, K. Sirts, L. Qu, M. Johnson, Stranse: a novel embedding model of entities and relationships in knowledge bases, arXiv preprint arXiv:1606.08140 (2016).
*   <a id="ref-131"></a>[131] H. Xiao, M. Huang, Y. Hao, X. Zhu, Transa: An adaptive approach for knowledge graph embedding, arXiv preprint arXiv:1509.05490 (2015).
*   <a id="ref-132"></a>[132] M. Fan, Q. Zhou, E. Chang, F. Zheng, Transition-based knowledge graph embedding with relational mapping properties, in: Proceedings of the 28th Pacific Asia conference on language, information and computing, pp. 328–337.
*   <a id="ref-133"></a>[133] H. Xiao, M. Huang, Y. Hao, X. Zhu, From one point to a manifold: Orbit models for knowledge graph embedding (2015).
*   <a id="ref-134"></a>[134] J. Feng, M. Huang, M. Wang, M. Zhou, Y. Hao, X. Zhu, Knowledge graph embedding by flexible translation, in:
Fifteenth International Conference on the Principles of Knowledge Representation and Reasoning.
*   <a id="ref-135"></a>[135] Q. Xie, X. Ma, Z. Dai, E. Hovy, An interpretable knowledge transfer model for knowledge base completion, arXiv preprint arXiv:1704.05908 (2017).
*   <a id="ref-136"></a>[136] W. Qian, C. Fu, Y. Zhu, D. Cai, X. He, Translating embeddings for knowledge graph completion with relation attention mechanism., in: IJCAI, pp. 4286–4292.
*   <a id="ref-137"></a>[137] S. Yang, J. Tian, H. Zhang, J. Yan, H. He, Y. Jin, Transms: Knowledge graph embedding for complex relations by multidirectional semantics., in: IJCAI, pp. 1935–1942.
*   <a id="ref-138"></a>[138] S. Ma, J. Ding, W. Jia, K. Wang, M. Guo, Transt: Type-based multiple embedding representations for knowledge graph completion, in: Joint European Conference on Machine Learning and Knowledge Discovery in Databases, Springer, pp. 717–733.
*   <a id="ref-139"></a>[139] S. He, K. Liu, G. Ji, J. Zhao, Learning to represent knowledge graphs with gaussian embedding, in: Proceedings of the 24th ACM international on conference on information and knowledge management, pp. 623–632.
*   <a id="ref-140"></a>[140] H. Xiao, M. Huang, Y. Hao, X. Zhu, Transg: A generative mixture model for knowledge graph embedding, arXiv preprint arXiv:1509.05488 (2015).
*   <a id="ref-141"></a>[141] S. Zhang, Y. Tay, L. Yao, Q. Liu, Quaternion knowledge graph embeddings, arXiv preprint arXiv:1904.10281 (2019).
*   <a id="ref-142"></a>[142] T. Ebisu, R. Ichise, Toruse: Knowledge graph embedding on a lie group, in: Thirty-Second AAAI Conference on Artificial Intelligence.
*   <a id="ref-143"></a>[143] G. A. Miller, Wordnet: a lexical database for english, Communications of the ACM 38 (1995) 39–41.
*   <a id="ref-144"></a>[144] A. García-Durán, A. Bordes, N. Usunier, Effective blending of two and three-way interactions for modeling multirelational data, in: Joint European Conference on Machine Learning and Knowledge Discovery in Databases, Springer, pp. 434–449.
*   <a id="ref-145"></a>[145] T. A. Plate, Holographic reduced representations, IEEE Transactions on Neural networks 6 (1995) 623–641.
*   <a id="ref-146"></a>[146] K. L. Stratos, The fast fourier transform and its applications, 2010.
*   <a id="ref-147"></a>[147] Y. Xue, Y. Yuan, Z. Xu, A. Sabharwal, Expanding holographic embeddings for knowledge completion., in: NeurIPS, pp. 4496–4506.
*   <a id="ref-148"></a>[148] K. Hayashi, M. Shimbo, On the equivalence of holographic and complex embeddings for link prediction, in: Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers), pp. 554–559.
*   <a id="ref-149"></a>[149] H. Liu, Y. Wu, Y. Yang, Analogical inference for multi-relational embeddings, in: International conference on machine learning, PMLR, pp. 2168–2178.
*   <a id="ref-150"></a>[150] S. M. Kazemi, D. Poole, Simple embedding for link prediction in knowledge graphs, arXiv preprint arXiv:1802.04868 (2018).
*   <a id="ref-151"></a>[151] W. Zhang, B. Paudel, W. Zhang, A. Bernstein, H. Chen, Interaction embeddings for prediction and explanation in knowledge graphs, in: Proceedings of the Twelfth ACM International Conference on Web Search and Data Mining, pp. 96–104.
*   <a id="ref-152"></a>[152] X. Chen, S. Jia, Y. Xiang, A review: Knowledge reasoning over knowledge graph, Expert Systems with Applications 141 (2020) 112948.
*   <a id="ref-153"></a>[153] A. Bordes, X. Glorot, J. Weston, Y. Bengio, A semantic matching energy function for learning with multirelational data, Machine Learning 94 (2014) 233–259.
*   <a id="ref-154"></a>[154] R. Socher, D. Chen, C. D. Manning, A. Ng, Reasoning with neural tensor networks for knowledge base completion, in: Advances in neural information processing systems, pp. 926–934.
*   <a id="ref-155"></a>[155] Q. Liu, H. Jiang, A. Evdokimov, Z.-H. Ling, X. Zhu, S. Wei, Y. Hu, Probabilistic reasoning via deep learning: Neural association models, arXiv preprint arXiv:1603.07704 (2016).
*   <a id="ref-156"></a>[156] S. Sabour, N. Frosst, G. E. Hinton, Dynamic routing between capsules, arXiv preprint arXiv:1710.09829 (2017).
*   <a id="ref-157"></a>[157] T. Vu, T. D. Nguyen, D. Q. Nguyen, D. Phung, et al., A capsule network-based embedding model for knowledge graph completion and search personalization, in: Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers), pp. 2180–2189.
*   <a id="ref-158"></a>[158] C. Shang, Y. Tang, J. Huang, J. Bi, X. He, B. Zhou, End-to-end structure-aware convolutional networks for knowledge base completion, in: Proceedings of the AAAI Conference on Artificial Intelligence, volume 33, pp. 3060–3067.
*   <a id="ref-159"></a>[159] D. Nathani, J. Chauhan, C. Sharma, M. Kaul, Learning attention-based embeddings for relation prediction in knowledge graphs, arXiv preprint arXiv:1906.01195 (2019).
*   <a id="ref-160"></a>[160] S. K. Mohamed, V. Novácek, P.-Y. Vandenbussche, E. Muñoz, Loss functions in knowledge graph embedding models., DL4KG@ ESWC 2377 (2019) 1–10.
*   <a id="ref-161"></a>[161] T. Lacroix, N. Usunier, G. Obozinski, Canonical tensor decomposition for knowledge base completion, in: International Conference on Machine Learning, PMLR, pp. 2863–2872.
*   <a id="ref-162"></a>[162] F. Akrami, M. S. Saeef, Q. Zhang, W. Hu, C. Li, Realistic re-evaluation of knowledge graph completion methods:
An experimental study, in: Proceedings of the 2020 ACM SIGMOD International Conference on Management of Data, pp. 1995–2010.
*   <a id="ref-163"></a>[163] N. Lao, J. Zhu, L. Liu, Y. Liu, W. W. Cohen, Efficient relational learning with hidden variable detection, Advances in Neural Information Processing Systems 23 (2010) 1234–1242.
*   <a id="ref-164"></a>[164] W. Xiong, T. Hoang, W. Y. Wang, Deeppath: A reinforcement learning method for knowledge graph reasoning, in: Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing, pp. 564–573.
*   <a id="ref-165"></a>[165] R. Das, S. Dhuliawala, M. Zaheer, L. Vilnis, I. Durugkar, A. Krishnamurthy, A. Smola, A. McCallum, Go for a walk and arrive at the answer: Reasoning over paths in knowledge bases using reinforcement learning, arXiv preprint arXiv:1711.05851 (2017).
*   <a id="ref-166"></a>[166] Y. Shen, J. Chen, P.-S. Huang, Y. Guo, J. Gao, M-walk: learning to walk over graphs using monte carlo tree search, in: Proceedings of the 32nd International Conference on Neural Information Processing Systems, pp. 6787–6798.
*   <a id="ref-167"></a>[167] X. V. Lin, C. Xiong, R. Socher, Multi-hop knowledge graph reasoning with reward shaping, 2019. US Patent App. 16/051,309.
*   <a id="ref-168"></a>[168] Y. Qiu, Y. Wang, X. Jin, K. Zhang, Stepwise reasoning for multi-relation question answering over knowledge graph with weak supervision, in: Proceedings of the 13th International Conference on Web Search and Data Mining, pp. 474–482.
*   <a id="ref-169"></a>[169] S. Li, H. Wang, R. Pan, M. Mao, Memorypath: A deep reinforcement learning framework for incorporating memory component into knowledge graph reasoning, Neurocomputing 419 (2021) 273–286.
*   <a id="ref-170"></a>[170] P. Tiwari, H. Zhu, H. M. Pandey, Dapath: Distance-aware knowledge graph reasoning based on deep reinforcement learning, Neural Networks 135 (2021) 1–12.
*   <a id="ref-171"></a>[171] R. J. Williams, Simple statistical gradient-following algorithms for connectionist reinforcement learning, Machine learning 8 (1992) 229–256.
*   <a id="ref-172"></a>[172] G. Wan, S. Pan, C. Gong, C. Zhou, G. Haffari, Reasoning like human: Hierarchical reinforcement learning for knowledge graph reasoning., in: IJCAI, pp. 1926–1932.
*   <a id="ref-173"></a>[173] Q. Wang, Y. Hao, J. Cao, Adrl: An attention-based deep reinforcement learning framework for knowledge graph reasoning, Knowledge-Based Systems 197 (2020) 105910.
*   <a id="ref-174"></a>[174] F. Salehi, R. Bamler, S. Mandt, Probabilistic knowledge graph embeddings (2018).
*   <a id="ref-175"></a>[175] R. Kadlec, O. Bajgar, J. Kleindienst, Knowledge base completion: Baselines strike back, arXiv preprint arXiv:1705.10744 (2017).
*   <a id="ref-176"></a>[176] D. Ruffinelli, S. Broscheit, R. Gemulla, You can teach an old dog new tricks! on training knowledge graph embeddings, in: International Conference on Learning Representations.
*   <a id="ref-177"></a>[177] I. Balaževic, C. Allen, T. M. Hospedales, Tucker: Tensor factorization for knowledge graph completion, arXiv ´ preprint arXiv:1901.09590 (2019).
*   <a id="ref-178"></a>[178] P. Pezeshkpour, Y. Tian, S. Singh, Revisiting evaluation of knowledge base completion models, in: Automated Knowledge Base Construction.
*   <a id="ref-179"></a>[179] P. Tabacof, L. Costabello, Probability calibration for knowledge graph embedding models, arXiv preprint arXiv:1912.10000 (2019).
*   <a id="ref-180"></a>[180] T. Safavi, D. Koutra, E. Meij, Improving the utility of knowledge graph embeddings with calibration, arXiv e-prints (2020) arXiv–2004.
*   <a id="ref-181"></a>[181] B. Zadrozny, C. Elkan, Transforming classifier scores into accurate multiclass probability estimates, in: Proceedings of the eighth ACM SIGKDD international conference on Knowledge discovery and data mining, pp. 694–699.
*   <a id="ref-182"></a>[182] J. Platt, et al., Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods, Advances in large margin classifiers 10 (1999) 61–74.
*   <a id="ref-183"></a>[183] I. Chami, A. Wolf, D.-C. Juan, F. Sala, S. Ravi, C. Ré, Low-dimensional hyperbolic knowledge graph embeddings, arXiv preprint arXiv:2005.00545 (2020).
*   <a id="ref-184"></a>[184] A. Niculescu-Mizil, R. Caruana, Predicting good probabilities with supervised learning, in: Proceedings of the 22nd international conference on Machine learning, pp. 625–632.
*   <a id="ref-185"></a>[185] M. Nickel, V. Tresp, H.-P. Kriegel, Factorizing yago: scalable machine learning for linked data, in: Proceedings of the 21st international conference on World Wide Web, pp. 271–280.
*   <a id="ref-186"></a>[186] R. Xie, Z. Liu, J. Jia, H. Luan, M. Sun, Representation learning of knowledge graphs with entity descriptions, in: Proceedings of the AAAI Conference on Artificial Intelligence, volume 30.
*   <a id="ref-187"></a>[187] J. Xu, X. Qiu, K. Chen, X. Huang, Knowledge graph representation with jointly structural and textual encoding, in: Proceedings of the 26th International Joint Conference on Artificial Intelligence, pp. 1318–1324.
*   <a id="ref-188"></a>[188] M. Chen, Y. Tian, K.-W. Chang, S. Skiena, C. Zaniolo, Co-training embeddings of knowledge graphs and entity descriptions for cross-lingual entity alignment, arXiv preprint arXiv:1806.06478 (2018).
*   <a id="ref-189"></a>[189] M. Cochez, M. Garofalo, J. Lenßen, M. A. Pellegrino, A first experiment on including text literals in kglove, arXiv preprint arXiv:1807.11761 (2018).
*   <a id="ref-190"></a>[190] M. Cochez, P. Ristoski, S. P. Ponzetto, H. Paulheim, Global rdf vector space embeddings, in: International Semantic Web Conference, Springer, pp. 190–207.
*   <a id="ref-191"></a>[191] Y. Tay, L. A. Tuan, M. C. Phan, S. C. Hui, Multi-task neural network for non-discrete attribute prediction in knowledge graphs, in: Proceedings of the 2017 ACM on Conference on Information and Knowledge Management, pp. 1029–1038.
*   <a id="ref-192"></a>[192] Y. Wu, Z. Wang, Knowledge graph embedding with numeric attributes of entities, in: Proceedings of The Third Workshop on Representation Learning for NLP, pp. 132–136.
*   <a id="ref-193"></a>[193] R. Xie, Z. Liu, H. Luan, M. Sun, Image-embodied knowledge representation learning, arXiv preprint arXiv:1609.07028 (2016).
*   <a id="ref-194"></a>[194] B. D. Trisedya, J. Qi, R. Zhang, Entity alignment between knowledge graphs using attribute embeddings, in: Proceedings of the AAAI Conference on Artificial Intelligence, volume 33, pp. 297–304.
*   <a id="ref-195"></a>[195] E. Boschee, J. Lautenschlager, S. O'Brien, S. Shellman, J. Starz, M. Ward, Icews coded event data, Harvard Dataverse 12 (2015).
*   <a id="ref-196"></a>[196] K. Leetaru, P. A. Schrodt, Gdelt: Global data on events, location, and tone, 1979–2012, in: ISA annual convention, volume 2, Citeseer, pp. 1–49.
*   <a id="ref-197"></a>[197] T. Jiang, T. Liu, T. Ge, L. Sha, S. Li, B. Chang, Z. Sui, Encoding temporal information for time-aware link prediction, in: Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing, pp. 2350–2354.
*   <a id="ref-198"></a>[198] S. S. Dasgupta, S. N. Ray, P. Talukdar, Hyte: Hyperplane-based temporally aware knowledge graph embedding, in: Proceedings of the 2018 conference on empirical methods in natural language processing, pp. 2001–2011.
*   <a id="ref-199"></a>[199] A. García-Durán, S. Dumanciˇ c, M. Niepert, Learning sequence encoders for temporal knowledge graph comple- ´ tion, arXiv preprint arXiv:1809.03202 (2018).
*   <a id="ref-200"></a>[200] T. Lacroix, G. Obozinski, N. Usunier, Tensor decompositions for temporal knowledge base completion, arXiv preprint arXiv:2004.04926 (2020).
*   <a id="ref-201"></a>[201] Z. Han, Y. Ma, P. Chen, V. Tresp, Dyernie: Dynamic evolution of riemannian manifold embeddings for temporal knowledge graph completion, arXiv preprint arXiv:2011.03984 (2020).
*   <a id="ref-202"></a>[202] Y. Ma, V. Tresp, E. A. Daxberger, Embedding models for episodic knowledge graphs, Journal of Web Semantics 59 (2019) 100490.
*   <a id="ref-203"></a>[203] R. Goel, S. M. Kazemi, M. Brubaker, P. Poupart, Diachronic embedding for temporal knowledge graph completion, in: Proceedings of the AAAI Conference on Artificial Intelligence, volume 34, pp. 3988–3995.
*   <a id="ref-204"></a>[204] P. Shao, G. Yang, D. Zhang, J. Tao, F. Che, T. Liu, Tucker decomposition-based temporal knowledge graph completion, arXiv preprint arXiv:2011.07751 (2020).
*   <a id="ref-205"></a>[205] C. Xu, Y.-Y. Chen, M. Nayyeri, J. Lehmann, Temporal knowledge graph completion using a linear temporal regularizer and multivector embeddings, in: Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pp. 2569–2578.
*   <a id="ref-206"></a>[206] R. Speer, J. Chin, C. Havasi, Conceptnet 5.5: An open multilingual graph of general knowledge, in: Thirty-first AAAI conference on artificial intelligence.
*   <a id="ref-207"></a>[207] X. Chen, M. Chen, W. Shi, Y. Sun, C. Zaniolo, Embedding uncertain knowledge graphs, in: Proceedings of the AAAI Conference on Artificial Intelligence, volume 33, pp. 3363–3370.
*   <a id="ref-208"></a>[208] A. Kimmig, S. Bach, M. Broecheler, B. Huang, L. Getoor, A short introduction to probabilistic soft logic, in: Proceedings of the NIPS Workshop on Probabilistic Programming: Foundations and Applications, pp. 1–4.
*   <a id="ref-209"></a>[209] S. Pai, L. Costabello, Learning embeddings from knowledge graphs with numeric edge attributes, arXiv preprint arXiv:2105.08683 (2021).
*   <a id="ref-210"></a>[210] S.-Y. Yu, S. R. Chhetri, A. Canedo, P. Goyal, M. A. Al Faruque, Pykg2vec: A python library for knowledge graph embedding., J. Mach. Learn. Res. 22 (2021) 16–1.
*   <a id="ref-211"></a>[211] M. Ali, M. Berrendorf, C. T. Hoyt, L. Vermue, S. Sharifzadeh, V. Tresp, J. Lehmann, Pykeen 1.0: A python library for training and evaluating knowledge graph embeddings, Journal of Machine Learning Research 22 (2021) 1–6.
*   <a id="ref-212"></a>[212] X. Han, S. Cao, X. Lv, Y. Lin, Z. Liu, M. Sun, J. Li, Openke: An open toolkit for knowledge embedding, in: Proceedings of the 2018 conference on empirical methods in natural language processing: system demonstrations, pp. 139–144.
*   <a id="ref-213"></a>[213] L. Costabello, S. Pai, C. Van, R. McGrath, N. McCarthy, P. Tabacof, Ampligraph: a library for representation learning on knowledge graphs, Retrieved October 10 (2019) 2019.
*   <a id="ref-214"></a>[214] A. Lerer, L. Wu, J. Shen, T. Lacroix, L. Wehrstedt, A. Bose, A. Peysakhovich, Pytorch-biggraph: A large-scale graph embedding system, arXiv preprint arXiv:1903.12287 (2019).
*   <a id="ref-215"></a>[215] S. Broscheit, D. Ruffinelli, A. Kochsiek, P. Betz, R. Gemulla, Libkge-a knowledge graph embedding library for reproducible research, in: Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations, pp. 165–174.
*   <a id="ref-216"></a>[216] Z. Zhu, S. Xu, J. Tang, M. Qu, Graphvite: A high-performance cpu-gpu hybrid system for node embedding, in: The World Wide Web Conference, pp. 2494–2504.
*   <a id="ref-217"></a>[217] D. Zheng, X. Song, C. Ma, Z. Tan, Z. Ye, J. Dong, H. Xiong, Z. Zhang, G. Karypis, Dgl-ke: Training knowledge graph embeddings at scale, in: Proceedings of the 43rd International ACM SIGIR Conference on Research and Development in Information Retrieval, pp. 739–748.
*   <a id="ref-218"></a>[218] L. Van der Maaten, G. Hinton, Visualizing data using t-sne., Journal of machine learning research 9 (2008).
*   <a id="ref-219"></a>[219] M. Wang, L. Yu, D. Zheng, Q. Gan, Y. Gai, Z. Ye, M. Li, J. Zhou, Q. Huang, C. Ma, et al., Deep graph library: Towards efficient and scalable deep learning on graphs. (2019).
*   <a id="ref-220"></a>[220] A. Boschin, Torchkge: Knowledge graph embedding in python and pytorch, arXiv preprint arXiv:2009.02963 (2020).
*   <a id="ref-221"></a>[221] P. Pezeshkpour, Y. Tian, S. Singh, Investigating robustness and interpretability of link prediction via adversarial modifications, arXiv preprint arXiv:1905.00563 (2019).
*   <a id="ref-222"></a>[222] P. Bhardwaj, J. Kelleher, L. Costabello, D. O'Sullivan, Poisoning knowledge graph embeddings via relation inference patterns (????).
*   <a id="ref-223"></a>[223] K. Zhou, T. P. Michalak, Y. Vorobeychik, Adversarial robustness of similarity-based link prediction, in: 2019 IEEE International Conference on Data Mining (ICDM), IEEE, pp. 926–935.
*   <a id="ref-224"></a>[224] Z. Du, C. Zhou, M. Ding, H. Yang, J. Tang, Cognitive knowledge graph reasoning for one-shot relational learning, arXiv preprint arXiv:1906.05489 (2019).
*   <a id="ref-225"></a>[225] C. Zhang, H. Yao, C. Huang, M. Jiang, Z. Li, N. V. Chawla, Few-shot knowledge graph completion, in: Proceedings of the AAAI Conference on Artificial Intelligence, volume 34, pp. 3041–3048.
*   <a id="ref-226"></a>[226] M. Mirtaheri, M. Rostami, X. Ren, F. Morstatter, A. Galstyan, One-shot learning for temporal knowledge graphs, arXiv preprint arXiv:2010.12144 (2020).
*   <a id="ref-227"></a>[227] W. Xiong, M. Yu, S. Chang, X. Guo, W. Y. Wang, One-shot relational learning for knowledge graphs, arXiv preprint arXiv:1808.09040 (2018).
*   <a id="ref-228"></a>[228] F. Ilievski, D. Garijo, H. Chalupsky, N. T. Divvala, Y. Yao, C. Rogers, R. Li, J. Liu, A. Singh, D. Schwabe, et al., Kgtk: a toolkit for large knowledge graph manipulation and analysis, in: International Semantic Web Conference, Springer, pp. 278–293.
*   <a id="ref-229"></a>[229] J. Mohoney, R. Waleffe, H. Xu, T. Rekatsinas, S. Venkataraman, Marius: Learning massive graph embeddings on a single machine, in: 15th {USENIX} Symposium on Operating Systems Design and Implementation ({OSDI} 21), pp. 533–549.
*   <a id="ref-230"></a>[230] J. Portisch, M. Hladik, H. Paulheim, Rdf2vec light–a lightweight approach for knowledge graph embeddings, arXiv preprint arXiv:2009.07659 (2020).
*   <a id="ref-231"></a>[231] B. Rychalska, P. B ˛abel, K. Gołuchowski, A. Michałowski, J. D ˛abrowski, Cleora: A simple, strong and scalable graph embedding scheme, arXiv preprint arXiv:2102.02302 (2021).
*   <a id="ref-232"></a>[232] Z. Ding, Z. Han, Y. Ma, V. Tresp, Temporal knowledge graph forecasting with neural ode, arXiv preprint arXiv:2101.05151 (2021).
*   <a id="ref-233"></a>[233] G. H. Nguyen, J. B. Lee, R. A. Rossi, N. K. Ahmed, E. Koh, S. Kim, Dynamic network embeddings: From random walks to temporal random walks, in: 2018 IEEE International Conference on Big Data (Big Data), IEEE, pp. 1085–1092.
*   <a id="ref-234"></a>[234] D. Fu, J. He, Sdg: A simplified and dynamic graph neural network, in: Proceedings of the 44th International ACM SIGIR Conference on Research and Development in Information Retrieval, pp. 2273–2277.
*   <a id="ref-235"></a>[235] T. Shao, X. Li, X. Zhao, H. Xu, W. Xiao, Dskrl: A dissimilarity-support-aware knowledge representation learning framework on noisy knowledge graph, Neurocomputing (2021).
*   <a id="ref-236"></a>[236] M. J. Saeedizade, N. Torabian, B. Minaei-Bidgoli, Kgrefiner: Knowledge graph refinement for improving accuracy of translational link prediction methods, arXiv preprint arXiv:2106.14233 (2021).
*   <a id="ref-237"></a>[237] Z. Zhang, X. Liu, Y. Zhang, Q. Su, X. Sun, B. He, Pretrain-kge: Learning knowledge representation from pretrained language models, in: Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: Findings, pp. 259–266.
*   <a id="ref-238"></a>[238] J. Xu, J. Chen, S. You, Z. Xiao, Y. Yang, J. Lu, Robustness of deep learning models on graphs: A survey, AI Open 2 (2021) 69–78.
*   <a id="ref-239"></a>[239] L. Fei-Fei, R. Fergus, P. Perona, One-shot learning of object categories, IEEE transactions on pattern analysis and machine intelligence 28 (2006) 594–611.
*   <a id="ref-240"></a>[240] Y. Hu, A. Chapman, G. Wen, D. W. Hall, What can knowledge bring to machine learning?–a survey of low-shot learning for structured data, arXiv preprint arXiv:2106.06410 (2021).
*   <a id="ref-241"></a>[241] Y. Zhang, X. Chen, Y. Yang, A. Ramamurthy, B. Li, Y. Qi, L. Song, Efficient probabilistic logic reasoning with graph neural networks, arXiv preprint arXiv:2001.11850 (2020).
*   <a id="ref-242"></a>[242] F. Yang, Z. Yang, W. W. Cohen, Differentiable learning of logical rules for knowledge base reasoning, arXiv preprint arXiv:1702.08367 (2017).
*   <a id="ref-243"></a>[243] H. Paulheim, Knowledge graph refinement: A survey of approaches and evaluation methods, Semantic web 8 (2017) 489–508.
*   <a id="ref-244"></a>[244] J. Qiu, Q. Chen, Y. Dong, J. Zhang, H. Yang, M. Ding, K. Wang, J. Tang, Gcc: Graph contrastive coding for graph
neural network pre-training, in: Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, pp. 1150–1160.
*   <a id="ref-245"></a>[245] Z. Hu, Y. Dong, K. Wang, K.-W. Chang, Y. Sun, Gpt-gnn: Generative pre-training of graph neural networks, in: Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, pp. 1857–1867.
*   <a id="ref-246"></a>[246] C. Xiong, J. Callan, T.-Y. Liu, Word-entity duet representations for document ranking, in: Proceedings of the 40th International ACM SIGIR conference on research and development in information retrieval, pp. 763–772.
*   <a id="ref-247"></a>[247] X. Liu, H. Fang, Latent entity space: a novel retrieval approach for entity-bearing queries, Information Retrieval Journal 18 (2015) 473–503.
*   <a id="ref-248"></a>[248] J. Dalton, L. Dietz, J. Allan, Entity query feature expansion using knowledge base links, in: Proceedings of the 37th international ACM SIGIR conference on Research & development in information retrieval, pp. 365–374.
*   <a id="ref-249"></a>[249] H. Raviv, O. Kurland, D. Carmel, Document retrieval using entity-based language models, in: Proceedings of the 39th International ACM SIGIR conference on Research and Development in Information Retrieval, pp. 65–74.
*   <a id="ref-250"></a>[250] F. Ensan, E. Bagheri, Document retrieval model through semantic linking, in: Proceedings of the tenth ACM international conference on web search and data mining, pp. 181–190.
*   <a id="ref-251"></a>[251] H. Wang, F. Zhang, X. Xie, M. Guo, Dkn: Deep knowledge-aware network for news recommendation, in: Proceedings of the 2018 world wide web conference, pp. 1835–1844.
*   <a id="ref-252"></a>[252] F. Zhang, N. J. Yuan, D. Lian, X. Xie, W.-Y. Ma, Collaborative knowledge base embedding for recommender systems, in: Proceedings of the 22nd ACM SIGKDD international conference on knowledge discovery and data mining, pp. 353–362.
*   <a id="ref-253"></a>[253] H. Wang, F. Zhang, M. Zhao, W. Li, X. Xie, M. Guo, Multi-task feature learning for knowledge graph enhanced recommendation, in: The World Wide Web Conference, pp. 2000–2010.
*   <a id="ref-254"></a>[254] H. Zhao, Q. Yao, J. Li, Y. Song, D. L. Lee, Meta-graph based recommendation fusion over heterogeneous information networks, in: Proceedings of the 23rd ACM SIGKDD international conference on knowledge discovery and data mining, pp. 635–644.
*   <a id="ref-255"></a>[255] X. Wang, D. Wang, C. Xu, X. He, Y. Cao, T.-S. Chua, Explainable reasoning over knowledge graphs for recommendation, in: Proceedings of the AAAI Conference on Artificial Intelligence, volume 33, pp. 5329–5336.
*   <a id="ref-256"></a>[256] J. Berant, A. Chou, R. Frostig, P. Liang, Semantic parsing on freebase from question-answer pairs, in: Proceedings of the 2013 conference on empirical methods in natural language processing, pp. 1533–1544.
*   <a id="ref-257"></a>[257] X. Yao, B. Van Durme, Information extraction over structured data: Question answering with freebase, in: Proceedings of the 52nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 956–966.
*   <a id="ref-258"></a>[258] L. Dong, F. Wei, M. Zhou, K. Xu, Question answering over freebase with multi-column convolutional neural networks, in: Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), pp. 260–269.
*   <a id="ref-259"></a>[259] S. W.-t. Yih, M.-W. Chang, X. He, J. Gao, Semantic parsing via staged query graph generation: Question answering with knowledge base (2015).
*   <a id="ref-260"></a>[260] Y. Zhang, K. Liu, S. He, G. Ji, Z. Liu, H. Wu, J. Zhao, Question answering over knowledge base with neural attention combining global knowledge information, arXiv preprint arXiv:1606.00979 (2016).
*   <a id="ref-261"></a>[261] Z. Liu, Z.-Y. Niu, H. Wu, H. Wang, Knowledge aware conversation generation with explainable reasoning over augmented graphs, arXiv preprint arXiv:1903.10245 (2019).
*   <a id="ref-262"></a>[262] S. Moon, P. Shah, A. Kumar, R. Subba, Opendialkg: Explainable conversational reasoning with attention-based walks over knowledge graphs, in: Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics, pp. 845–854.
*   <a id="ref-263"></a>[263] D. Guo, D. Tang, N. Duan, M. Zhou, J. Yin, Dialog-to-action: Conversational question answering over a largescale knowledge base, in: Advances in Neural Information Processing Systems, pp. 2942–2951.
*   <a id="ref-264"></a>[264] P. Ernst, C. Meng, A. Siu, G. Weikum, Knowlife: a knowledge graph for health and life sciences, in: 2014 IEEE 30th International Conference on Data Engineering, IEEE, pp. 1254–1257.
*   <a id="ref-265"></a>[265] L. Shi, S. Li, X. Yang, J. Qi, G. Pan, B. Zhou, Semantic health knowledge graph: semantic integration of heterogeneous medical knowledge and services, BioMed research international 2017 (2017).
*   <a id="ref-266"></a>[266] M. Rotmensch, Y. Halpern, A. Tlimat, S. Horng, D. Sontag, Learning a health knowledge graph from electronic medical records, Scientific reports 7 (2017) 1–11.
*   <a id="ref-267"></a>[267] S. K. Mohamed, A. Nounu, V. Novácek, Drug target discovery using knowledge graph embeddings, in: Proceed- ˇ ings of the 34th ACM/SIGAPP Symposium on Applied Computing, pp. 11–18.
*   <a id="ref-268"></a>[268] M. Okereke, N. A. Ukor, Y. A. Adebisi, I. O. Ogunkola, E. Favour Iyagbaye, G. Adiela Owhor, D. E. Lucero-Prisno III, Impact of covid-19 on access to healthcare in low-and middle-income countries: current evidence and future recommendations, The International journal of health planning and management 36 (2021) 13–17.
*   <a id="ref-269"></a>[269] A. Chatterjee, C. Nardi, C. Oberije, P. Lambin, Knowledge graphs for covid-19: An exploratory review of the current landscape, Journal of personalized medicine 11 (2021) 300.
*   <a id="ref-270"></a>[270] J. Al-Saleem, R. Granet, S. Ramakrishnan, N. A. Ciancetta, C. Saveson, C. Gessner, Q. Zhou, Knowledge graphbased approaches to drug repurposing for covid-19, Journal of chemical information and modeling 61 (2021) 4058–4067.
*   <a id="ref-271"></a>[271] T. Kim, Y. Yun, N. Kim, Deep learning-based knowledge graph generation for covid-19, Sustainability 13 (2021) 2276.
*   <a id="ref-272"></a>[272] D. Zhang, J. Liu, H. Zhu, Y. Liu, L. Wang, P. Wang, H. Xiong, Job2vec: Job title benchmarking with collective multi-view representation learning, in: Proceedings of the 28th ACM International Conference on Information and Knowledge Management, pp. 2763–2771.
*   <a id="ref-273"></a>[273] Y. Jia, Y. Qi, H. Shang, R. Jiang, A. Li, A practical approach to constructing a knowledge graph for cybersecurity, Engineering 4 (2018) 53–60.
*   <a id="ref-274"></a>[274] Y. Qi, R. Jiang, Y. Jia, R. Li, A. Li, Association analysis algorithm based on knowledge graph for space-ground integrated network, in: 2018 IEEE 18th International Conference on Communication Technology (ICCT), IEEE, pp. 222–226.