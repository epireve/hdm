---
cite_key: wang_2008
title: 'A Survey on Accuracy-oriented Neural Recommendation: From Collaborative Filtering
  to Information-rich Recommendation'
authors: Meng Wang, Fellow, IEEE
year: 2008
date_processed: '2025-07-02'
phase2_processed: true
original_folder: arxiv_2021_survey_accuracy_neural_recommendation
images_total: 8
images_kept: 8
images_removed: 0
tags:
- Knowledge Graph
- Machine Learning
- Natural Language Processing
- Recommendation System
- Semantic Web
- Temporal
---

# A Survey on Accuracy-oriented Neural Recommendation: From Collaborative Filtering to Information-rich Recommendation

Le Wu *Member, IEEE*, Xiangnan He *Member, IEEE*, Xiang Wang *Member, IEEE*, Kun Zhang *Member, IEEE*, and Meng Wang, *Fellow, IEEE*

**Abstract**—Influenced by the great success of deep learning in computer vision and language understanding, research in recommendation has shifted to inventing new recommender models based on neural networks. In recent years, we have witnessed significant progress in developing neural recommender models, which generalize and surpass traditional recommender models owing to the strong representation power of neural networks. In this survey paper, we conduct a systematic review on neural recommender models from the perspective of recommendation modeling with the accuracy goal, aiming to summarize this field to facilitate researchers and practitioners working on recommender systems. Specifically, based on the data usage during recommendation modeling, we divide the work into collaborative filtering and information-rich recommendation: 1) *collaborative filtering*, which leverages the key source of user-item interaction data; 2) *content enriched recommendation*, which additionally utilizes the side information associated with users and items, like user profile and item knowledge graph; and 3) *temporal/sequential recommendation*, which accounts for the contextual information associated with an interaction, such as time, location, and the past interactions. After reviewing representative work for each type, we finally discuss some promising directions in this field.

✦

**Index Terms**—Recommendation Survey, Deep Learning, Neural Networks, Neural Recommendation Models

# 1 INTRODUCTION

I NFORMATION overload is an increasing problem in people's every life due to the proliferation of the Internet. Recommender system serves as an effective solution to alleviate the information overload issue, to facilitate users seeking desired information, and to increase the traffic and revenue of service providers. It has been used in a wide range of applications, such as e-commerce, social media sites, news portals, app stores, digital libraries, and so on. It is one of the most ubiquitous user-centered artificial intelligence applications in modern information systems.

The research in recommendation can be dated back to 1990s [\[1\]](#page-14-0), in the age the early work has developed many heuristics for content-based and Collaborative Filtering (CF) [\[2\]](#page-14-1). Popularized by the Netflix challenge, Matrix Factorization (MF) [\[3\]](#page-14-2) later becomes the mainstream recommender model for a long time (from 2008 until 2016) [\[4\]](#page-14-3), [\[5\]](#page-14-4). However, the linear nature of factorization models makes them less effective when dealing with large and complex data, e.g., the complex user-item interactions, and the items may contain complex semantics (e.g., texts and images) that require a thorough understanding. Around the same time in the mid-2010s, the rise of deep neural networks in machine learning (a.k.a., Deep Learning) has revolutionized several areas including speech recognition, computer vision, and natural language processing [\[6\]](#page-14-5). The great success of deep learning stems from the considerable expressiveness of neural networks, which are particularly advantageous for learning from large data with complicated patterns. This naturally brings new opportunities to advance the recommendation technologies. And not surprisingly, there emerges a lot of work on developing neural network approaches to recommender systems in the past several years. In this work, we aim to provide a systematic review on the recommender models that use neural networks — referred to as "*neural recommender models*". This is the most thriving topic in current recommendation research, not only has many exciting progresses in recent years, but also shows the potential to be the technical foundations of the nextgeneration recommender systems.

## 1.1 Differences with Existing Surveys.

Given the significance and popularity of recommendation research, there are some recently published surveys also reviewed this area [\[2\]](#page-14-1), [\[7\]](#page-14-6), [\[8\]](#page-14-7), [\[9\]](#page-14-8), [\[10\]](#page-14-9). Here we shortly discuss the main differences with these work to highlight the necessity and significance of this survey.

Existing surveys consist of two main parts. The first part focuses on the specific topics or directions, such as side information utilization in collaborative filtering [\[7\]](#page-14-6), crossdomain recommendation [\[8\]](#page-14-7), explainable recommendation [\[11\]](#page-14-10), knowledge graph-enhanced recommendation [\[12\]](#page-14-11), sequential recommendation [\[13\]](#page-14-12), [\[14\]](#page-14-13), and session-based

<sup>•</sup> *L. Wu, and M Wang are with Key Laboratory of Knowledge Engineering with Big Data, Hefei University of Technology, Hefei, Anhui 230029, China, and Institute of Artificial Intelligence, Hefei Comprehensive National Science Center, Hefei, Anhui 230088 (email: lewu.ustc, eric.mengwang@gmail.com).*<sup>•</sup>*K. Zhang is with Key Laboratory of Knowledge Engineering with Big Data, Hefei University of Technology, Hefei, Anhui 230029, China.(email:zhang1028kun@gmail.com).*<sup>•</sup>*X. He is with University of Science and Technology of China, Hefei 230026, China. (email: xiangnanhe@gmail.com).*<sup>•</sup>*X. Wang is with National University of Singapore, Singapore. (email: xiangwang@u.nus.edu).*<span id="page-1-1"></span>![](_page_1_Figure_1.jpeg)
<!-- Image Description: The image is a 3D diagram illustrating different data types used in recommendation systems. Three data categories are shown as stacked boxes: User Data (blue), Interaction Data (grey), and Item Data (yellow). A larger, encompassing box represents Context Data. The diagram's right side lists three recommendation model types: Collaborative Filtering (using Interaction Data), Content-enriched Models (using Interaction, User, and Item Data), and Context-aware Models (using Interaction and Context Data). Dashed lines show how data is combined in the models. -->

Fig. 1: An illustration of the data used for recommendation modeling and the three model types.

recommendation [\[15\]](#page-14-14). The other part follows the taxonomy of Deep Learning (DL) to summarize the recommendation methods. For example, Zhang et al. [\[16\]](#page-14-15) organized the discussions on recommendation methods into MLP based, autoencoder based, RNN based, attention based, etc. Similar surveys can also be found [\[17\]](#page-14-16), [\[18\]](#page-14-17). These surveys mainly compare the technical difference of using various deep learning methods for recommendation.

Different from existing surveys, our survey is organized from the perspective of recommendation modeling with the accuracy goal, and covers the most typical recommendation scenarios, such as CF, content-enriched methods, and temporal/sequential methods. This will not only help researchers understanding why and when a deep learning technique would work but also facilitate practitioners designing better solutions for a specific recommendation scenario.

## 1.2 How Do We Collect the Papers?

Since our survey focuses on reviewing recommender system from the perspective of recommendation modeling with the accuracy goal, we retrieved most of the related top conferences such as WWW, SIGIR, KDD, ICLR, AAAI, IJCAI, WSDM, and RecSys, as well as the top journals such as TKDE, TKDD, and so on. Meanwhile, we also leveraged Google Scholar to search the recent related work. According to the categories that we made in this survey, we used key words such as*collaborative filtering*, *content+RS*, *recommender systems*, *context+RS*, *side information*, *graph neural network*, *neural recommendation*, etc, to search the relevant work. Then, based on the retrieved papers, we carefully design the topical structure to cover all papers as completely as possible. Besides, in order to avoid missing some important work, we also double-checked those classic and influential papers in recommendation.

## 1.3 Scope and Organization of This Survey

This survey is organized into two major parts: Sections [2](#page-1-0) to [4](#page-10-0) review existing methods, and Section [5](#page-12-0) discusses future directions and open issues. Before elaborating each section, we first give the problem formulation.

Regardless of the recommendation domain and scenario, we can abstract the "learning to recommend" problem as:

$$
\hat{y}_{u,i,c} = f(D_u, D_i, D_c),\tag{1}
$$

that is, learning the prediction function f to estimate the likelihood that a user u will favor an item i under the context c, given the data D<sup>u</sup> , D<sup>i</sup> , and D<sup>c</sup> to describe the user u, item i, and context c, respectively. In doing so, we allow a unified framework to summarize neural recommendation models:

- Section [2](#page-1-0) reviews *collaborative filtering models*, which forms the basis of personalized recommendation and is the most researched topic in recommendation. They can be seen as ignoring the context data D<sup>c</sup> and using only the ID or interaction history in D<sup>u</sup> and D<sup>i</sup> .
- Section [3](#page-4-0) reviews the models that integrate the side information of users and items into recommendation, such as user profiles and social network, item attributes and knowledge graph. We term them as *content-enriched models*, which naturally extend collaborative filtering (CF) by integrating the side information into D<sup>u</sup> and D<sup>i</sup> , whereas the context data D<sup>c</sup> is also ignored.
- Section [4](#page-10-0) reviews the models that use contextual information. The contextual data are associated with each user-item interaction, but do not belong to either user content or item content, like time, location, and the past interaction sequence [\[2\]](#page-14-1). The *context-aware models*make predictions based on the context data Dc, in addition to the user-related data D<sup>u</sup> and item-related data D<sup>i</sup> . Due to page limit, we focus on temporal context, which is one of the most common contextual data.

Fig. [1](#page-1-1) illustrates the typical data used for recommendation modeling and three model types. It is worth noting that different models are designed for different recommendation scenarios. Nevertheless, in many cases we can make simple adjustments on a model's component to make it suitable (at least technically viable) for another scenario. For example, many CF models are designed to first obtain user and item representations, and then the prediction function is learned given the user and item representations. To make them be content-enriched, we simply need to enhance the representation learning component with content modeling. Another example is that we can treat the contextual information as part of user data, i.e., constructing Du,c to replace Du, to tweak content-enriched models to also be contextaware. Although these adjusted models may not be officially proposed or published, they can be obtained without much effort and worth exploring in real applications. Such design flexibility can be attributed to the layer-wise architecture of neural recommendation models, where different layers are designed for different aims. For convenience, we also summarize related neural recommendation models into the taxonomy of recommendation modeling [1](#page-1-2) . We hope this survey would provide a clear road-map to facilitate practitioners understanding and better designing models for their purpose.

# <span id="page-1-0"></span>2 COLLABORATIVE FILTERING MODELS

The concept of CF stems from the idea that leveraging collaborative behaviors of all users for predicting the behavior of a target user. Early approaches directly calculate the behavior similarity of users (user-based CF) or items (itembased CF) with memory based models. Later on, matrix factorization based models become prevalent by collectively finding the latent spaces that encode user-item interaction

<span id="page-1-2"></span><sup>1.</sup> <https://github.com/lmcRS/AWS-recommendation-papers>

matrix [\[3\]](#page-14-2), [\[19\]](#page-14-18). Given the expressive complex modeling power of neural networks, the current solutions for neural CF can be summarized into two categories: representation modeling of users and items, and user-item interaction modeling given the representations.

## 2.1 Representation Learning

Let U and V denote users and items in CF, with R ∈ RM×<sup>N</sup> is a user-item interaction behavior matrix. The general objective is to learn a user embedding matrix P and an item embedding matrix Q, with p<sup>u</sup> and q<sup>i</sup> denote the representation parameters for user u and item i, respectively.

In fact, as each user has limited behavior compared to the large item set, a key challenge that lies in CF is the sparsity of the user-item interaction behavior for accurate user and item embedding learning. Different kinds of representation learning models vary in input data, as well as the representation modeling techniques given the input data. We divide this section into three categories:*history behavior aggregation enhanced models*, *autoencoder based models*, and *graph learning approaches*. For ease of explanation, we list the typical representation learning models in Table [1.](#page-3-0)

## *2.1.1 History Behavior Attention Aggregation Models*By taking the one-hot User ID (UID), and one-hot Item ID (IID) as input, classical latent factor models associate each UID u and IID i with a free embedding vector of**p**<sup>u</sup> and **q**i [\[3\]](#page-14-2), [\[19\]](#page-14-18). Instead of modeling users with free embeddings, researchers further proposed borrowing users' historical behavior for better user representation modeling. E.g., Factored Item Similarity Model (FISM) pools the interacted item embeddings as a user representation vector [\[20\]](#page-14-19), and SVD++ [\[24\]](#page-14-20) adds UID embedding **p**<sup>u</sup> with the interaction history embedding (i.e., the FISM user representation) as the final user representation. These models relied on simple linear matrix factorization, and used heuristics or equal weights for the interaction history aggregation.

However, different historical items should contribute differently to model a user's preference. Thus, some researchers integrate neural attention mechanism into history representation learning [\[25\]](#page-14-21), [\[26\]](#page-14-22), [\[42\]](#page-14-23). One representative work is Attentive Collaborative Filtering (ACF) [\[26\]](#page-14-22), which assigns each interacted item with a user-aware attentive weight to indicate its importance to user representation:

$$
\hat{r}_{ui} = (\mathbf{p}_u + \sum_{j \in \mathcal{R}_u} \alpha(u, j) \mathbf{q}_j)^T \mathbf{q}_i, \tag{2}
$$

where **p**<sup>u</sup> is the ID embedding of user u, R<sup>u</sup> denotes the items that u has interacted with. α(u, j) is the attentive weight defined as:

$$
\alpha(u,j) = \frac{\exp\left(\mathcal{F}(\mathbf{p}_u, \mathbf{q}_j)\right)}{\sum_{j' \in \mathcal{R}_u} \exp\left(\mathcal{F}(\mathbf{p}_u, \mathbf{q}_{j'})\right)},\tag{3}
$$

where F(·, ·) is a function that can be implemented as a MLP or simply inner product.

In practice, the influence of a historical item can be dependent on the target item, e.g., the purchase of a phone case is more related to the previous purchase of phone, while the purchase of a pant could be more related to the previous purchase of a shirt. As such, it may be beneficial to have dynamic user representation when considering the prediction on different target items. To this end, the Neural Attentive Item Similarity model (NAIS) model [\[25\]](#page-14-21) revises the attention mechanism to be target item-aware:

$$
\hat{r}_{ui} = \left(\sum_{j \in \mathcal{R}_u} \alpha(i,j) \mathbf{q}_j\right)^T \mathbf{q}_i
$$
\n
$$
\alpha(i,j) = \frac{\exp\left(\mathcal{F}(\mathbf{q}_i, \mathbf{q}_j)\right)}{\left[\sum_{k \in \mathcal{R}_u} \exp\left(\mathcal{F}(\mathbf{q}_i, \mathbf{q}_k)\right)\right]^{\beta}},\tag{4}
$$

where α(i, j) denotes the contribution of historical item j to user representation when predicting a user's preference on target item i. β is a hyper-parameter between 0 and 1 (e.g., 0.5), for smoothing the interaction histories of different lengths. Similar attention mechanisms have been adopted for representation learning from interaction history, e.g., the Deep Item-based CF model (DeepICF) [\[42\]](#page-14-23) and Deep Interest Network (DIN) [\[43\]](#page-14-24). As such, interaction history contains more information than single user ID and is a suitable choice for representation learning.

### *2.1.2 Autoencoder based Representation Learning*By utilizing the idea of reconstructing input for a better representation learning, autoencoder based models take the incomplete user-item matrix as input, and learn a hidden representation of each instance with an encoder, and further with a decoder part that reconstructs the input based on the hidden representation. By treating each user's historical records as input, the autoencoder based models learn each user's latent representation with a complex encoder neural network, and feed the learned user representation into a decoder network to output the predicted preference of each user. An alternative approach is to take each item's rating records from all users as input, and learn the item's latent representation to reconstruct the predicted preference of each item from all users [\[27\]](#page-14-25), [\[28\]](#page-14-26). Similar to the development of autoencoder, the extensions of autoencoder based models can also be classified into two categories. The first category leveraged autoencoder variants, and injected denoising autoencoders [\[28\]](#page-14-26), variational autoencoders [\[29\]](#page-14-27) into CF. These models can be seen as using complex deep learning techniques for learning either user or item encoders. The second category exploited the duality of users and items in autoencoders, and designed two parallel encoders to learn the user and item representations, and then also use inner product to model users' preferences to items [\[30\]](#page-14-28). It is worth pointing out the autoencoder based CF approaches can also be classified as extensions of the historical behavior attention based models, as these approaches adopt deep neural networks for aggregating historical behavior. Therefore, for the sake of simplicity, we have only briefly introduced autoencoder based models and have not repeated the specific technical details.

##*2.1.3 Graph based Representation Learning*The CF effects are reflected in interaction histories of multiple users. As such, using collective interaction histories has the potential to improve the representation quality. From the perspective of user-item interaction graph, the individual interaction history is equivalent to the first-order connectivity of the user. Thus, a natural extension is to mine the

| TABLE 1: Summarization of representation learning approaches for CF |                        |        |
|---------------------------------------------------------------------|------------------------|--------|
| Category                                                            | Modeling Summarization | Models |
|                                                                     |                        |        |

<span id="page-3-0"></span>

| Category                             | Modeling Summarization                                                                   | Models                                                                               |
|--------------------------------------|------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Classical<br>Matrix<br>Factorization | User UID (Free Embed)<br>Item IID (Free Embed)                                           | BPR [19], MF [3] et al.                                                              |
|                                      | User Interacted items (Free Embed+Heuristic Agg)<br>Item IID (Free Embed)                | FISM [20], PMLAM [21], pQCF [22], FAWMF [23]                                         |
|                                      | User Interacted items+UID (Free Embed+Heuristic Agg)<br>Item IID (Free Embed)            | SVD++ [24]                                                                           |
| History<br>Attention                 | User Interacted items (Free Embed+Heuristic Agg)<br>Item IID (Free Embed)                | NAIS [25]                                                                            |
|                                      | User Interacted items+UID (Free Embed+Heuristic Agg)<br>Item IID (Free Embed)            | ACF [26]                                                                             |
| Autoencoder                          | Item Interacted Items (Non-linear Encoder)                                               | AutoRec [27], CDAE [28], Mult-VAE [29] et al.                                        |
| Models                               | User Interacted Items (Non-linear encoder)<br>Item Interacted users (Non-linear Encoder) | REAP [30], CE-VNCF [31], SW-DAE [32]                                                 |
| Graph<br>Learning                    | User UID+Graph (GNN)<br>Item IID+Graph (GNN)                                             | GC-MC [33], NGCF [34], SpectralCF [35],<br>NIA-GCN [36], BGCF [37], DGCF [38] et al. |
|                                      | User UID+Graph (Simplified GNN)<br>Item IID+Graph (Simplified GNN)                       | LR-GCCF [39], LightGCN [40], DHCF [41] et al.                                        |

higher-order connectivity from the user-item graph structure. For example, the second-order connectivity of a user consists of similar users who have co-interacted with the same items. Fortunately, with the success of Graph Neural Networks (GNNs) for modeling graph structure data in the community [\[44\]](#page-14-43), many prior studies have been proposed to model the user-item bipartite graph structure for neural graph based representation learning. Given the user-item bipartite graph, let P<sup>0</sup> and Q<sup>0</sup> denote the free user latent matrix and item latent matrix as many classical latent factor based models, i.e., the 0 th-order user and item embedding. These neural graph based models iteratively update the (l + 1)th-order user (item) embedding as an aggregation of the l th-order item (user) embedding. For instance, each user u's updated embedding p (l+1) u is calculated as:

$$
\mathbf{a}_u^{(l+1)} = Agg(\mathbf{q}_j^l | j \in \mathcal{R}_u),\tag{5}
$$

$$
\mathbf{p}_u^{(l+1)} = \rho(\mathbf{W}^l[\mathbf{p}_u^l, \mathbf{a}_u^{(l+1)}]),\tag{6}
$$

where q l j is item j's representation at l th layer, R<sup>u</sup> denotes items that connect to user u in the user-item bipartite graph. a (l+1) u is the aggregation of connected items' representations in the l th layer, W<sup>l</sup> is an embedding transformation matrix that needs to be learned, and ρ() is an activation function. After that, each user's (item's) final embedding can be seen as combining each entity's embedding at each layer.

The above steps can be seen as embedding propagation in the user-item bipartite graph. With a predefined layer L, the up to L th order sub graph structure is directly encoded in the user and item embedding representation step. For example, SpectralCF utilized the spectral graph convolutions for CF [\[35\]](#page-14-36). GC-MC [\[33\]](#page-14-34) and NGCF [\[34\]](#page-14-35) modeled the graph convolutions of user-item interactions in the original space, and are more effective and efficient in practice. Very recently, researchers argued that these neural graph based CF models differ from the classical GNNs as CF models do not contain any user or item features. Directly borrowing complex steps such as embedding transformation, and non-linear activations in GNNs may not be a good choice. Simplified neural graph CF models, including LR-GCCF [\[39\]](#page-14-40), and LightGCN [\[40\]](#page-14-41) have been proposed, which eliminate unnecessary deep learning operations. These simplified neural

graph based models show superior performance in practice without the need of carefully chosen activation functions.

# 2.2 Interaction Modeling

Let p<sup>u</sup> and q<sup>i</sup> denote the learned embeddings of user u and item i from representation models, this component aims at interaction function modeling that estimates the user's preference towards the target item based on their representations. In the following, we describe how to model users' predicted preference, denoted as rˆui based on the learned embeddings. For ease of explanation, as shown in Table [2,](#page-4-1) we summarize three main categories for interaction modeling: classical inner product based approaches, distance based modeling and neural network based approaches.

Most previous recommendation models relied on the inner product between user embedding and item embedding to estimate the user-item pair score as: rˆui = p > <sup>u</sup> q<sup>i</sup> = P<sup>d</sup> <sup>f</sup>=1 puf qif . Despite its great success and simplicity, prior efforts suggest that simply conducting inner product would have two major limitations. First, the triangle inequality is violated [\[45\]](#page-14-44). That is, inner product only encourages the representations of users and historical items to be similar, but lacks guarantees for the similarity propagation between user-user and item-item relationships. Second, it models the linear interaction, and may fail to capture the complex relationships between users and items [\[49\]](#page-14-45).

##*2.2.1 Distance based Metrics*To solve the first issue, a line of research [\[45\]](#page-14-44), [\[46\]](#page-14-46), [\[47\]](#page-14-47) borrows ideas from translation principles and uses distance metric as the interaction function. The inherent triangle inequality assumption plays an important role in helping capture underlying relationships among users and items. For instance, if user u tends to purchase items i and j, the representations of i and j should be close in the latent space.

Towards this end, CML [\[45\]](#page-14-44) minimizes the distance dui between each user-item interaction < u, i > in Euclidean space as: dui = kp<sup>u</sup> − qik 2 2 . Instead of minimizing the distance between each observed user-item pair, TransRec exploits the translation principle to model the sequential behaviors of users [\[46\]](#page-14-46). In particular, the representation of user u is treated as the translation vector between the

<span id="page-4-1"></span>

| Category             | Modeling Summarization                                         | Models                         |
|----------------------|----------------------------------------------------------------|--------------------------------|
| Inner Product        | rˆui = p><br>u qi                                              | Most models                    |
| Distance<br>Modeling | 2<br>Euclidean distance dui = kpu − qik<br>2                   | CML [45]                       |
|                      | Nearby translation dˆ<br>ui = βj − d(qj + pu, qi)              | TransRec [46]                  |
|                      | Memory enhanced Translation dˆ<br>2<br>ui = kpu + E − qik<br>2 | LRML [47]                      |
|                      | Distance in Hpyerbolic Space                                   | HyperML [48]                   |
| Neural<br>Networks   | rˆui = MLP(pu  qi)                                             | NCF [49] et al.                |
|                      | rˆui = CNN(pu ⊗ qi)                                            | ONCF [50] et al.               |
|                      | 2<br>Autoencoder based reconstruction kri − dec(enc(ri))k<br>2 | AutoRec [27], CDAE [28] et al. |

representations of the items i and the item j to visit next, namely, q<sup>j</sup> + p<sup>u</sup> ≈ q<sup>i</sup> .

Distinct from CML that uses simple metric learning that assumes each user's embedding is equally close to every item embedding she likes, LRML introduces the relation vectors r to capture the relationships between user and item pairs [\[47\]](#page-14-47) . More formally, the score function is defined as:

$$
s_{ui} = \|\mathbf{p}_u + \mathbf{e} - \mathbf{q}_i\|_F^2, \tag{7}
$$

where the relation vector e ∈ R d is constructed using a neural attention mechanism over a memory matrix M. M ∈ R m×d is the trainable memory module, hence E is the attentive sum of m memory slots. As a result, the relation vectors not only ensure the triangle inequality, but also achieve better representation ability.

###*2.2.2 Neural Network based Metrics*Distinct from the foregoing that employs linear metrics, recent studies adopt a diverse array of neural architectures, spanning from MLP, Convolutional Neural Network (CNN), and AE as the main building block to mine complex and nonlinear patterns of user-item interactions.

Researchers made attempts to replace similarity modeling between users and items with MLPs, as MLPs are general function approximators to model any complex continuous function. NCF is proposed to model the interaction function between each user-item pair with MLPs as: rˆui = fMLP(pu||qi). Besides, NCF also incorporates a generic MF component into the interaction modeling, thereby making use of both linearity of MF and non-linearity of MLP to enhance recommendation quality.

Researchers also proposed to leverage CNN based architecture for interaction modeling. This kind of models first generate interaction maps via outer product of user and item embeddings, explicitly capturing the pairwise correlations between embedding dimensions [\[50\]](#page-14-49), [\[51\]](#page-14-50). These CNN based CF model focuses on higher-order correlations among representation dimensions. However, such improvements on performance come at the cost of increasing model complexity and time cost.

Besides, a line of research exploits AEs to fulfill the blanks of user-item interaction matrix directly in the decoder part [\[27\]](#page-14-25), [\[28\]](#page-14-26), [\[29\]](#page-14-27), [\[30\]](#page-14-28), [\[52\]](#page-14-51), [\[53\]](#page-15-0), [\[54\]](#page-15-1). As the encoder and decoder can be implemented via neural networks, such stacks of nonlinear transformations give the recommenders more capacity to model the user representation from complex combinations of all historically interacted items.
**Summary**: Many recent studies have shown the superiority of GNNs in the representation learning of users and items. We ascribe the success to (1) the essential data structure, where the user-item interactions can be naturally represented as a bipartite graph between user and item nodes; and (2) GNNs can explicitly encode the crucial collaborative filtering signal of user-item interactions through information propagation process. As for interaction modeling, compared with the complex functions and metrics, simple inner product is much more efficient especially in the online and large-scale recommendation.

# <span id="page-4-0"></span>3 CONTENT-ENRICHED RECOMMENDATION

In collaborative filtering, item representations encode the collaborative signal — behavioral patterns of users — solely, but ignore the semantic relatedness. To enhance the representation learning, many researchers go beyond the useritem interactions and exploit auxiliary data. The auxiliary data could be classified into two categories: content based information and context-aware data. Specifically, the first category of content information is associated with users and items, including general user and item features, textual content (a.k.a, item tags, item textual descriptions and users' reviews for items), multimedia descriptions (a.k.a, images, videos, and audio information), user social networks, and knowledge graphs. In contrast, contextual information shows the environment when users make item decisions, which usually denotes descriptions that beyond users and items [\[2\]](#page-14-1). Contextual information includes time, location, and specific data that are collected from sensors (such as speed, and weather), and so on. Due to page limits, we discuss the most typical contextual data: temporal data. In the following of the two sections, we would give a detailed summary of the content-enriched recommendation and context-aware recommendation. For the contentenriched recommendation, we classify the related work into five categories based on the available content information: the general features of users and items, the textual content information, the multimedia information, social networks and knowledge graphs.

## 3.1 Modeling General Feature Interactions

Factorization Machine (FM) provides an intuitive idea of feature interaction modeling [\[55\]](#page-15-2). As features are usually sparse, FM first embeds each feature i into a latent embedding v<sup>i</sup> , and models second-order interaction of any two feature instances with x<sup>i</sup> and x<sup>j</sup> as: v T <sup>i</sup> × vjxix<sup>j</sup> . Naturally, FM models the second-order interactions, and reduces the parameter size of computing similarity of any two features with embedding based models. FM has been extended to field-aware FM by expanding each feature with several

<span id="page-5-0"></span>

| Category                 | Modeling Summarization                                                | Models                                                   |
|--------------------------|-----------------------------------------------------------------------|----------------------------------------------------------|
| Second order             | Model second order correlations<br>with embedding based similarity    | FM [55], FFM [56]                                        |
| MLP based                | Design better initialization techniques<br>to facilitate MLP modeling | NFM [57], FNN [58], PNN [59],<br>DeepCrossing [60], [61] |
| higher order             | Combine deep and shallow features                                     | Wide&Deep [62], DeepFM [63]                              |
| Up to Kth order modeling | Deep cross network structure for defined order depth                  | DCN [64], xDeepFM [65]                                   |
| Tree structure           | Tree enhanced embedding for attentive cross feature aggregation       | TEM [11]                                                 |

latent embeddings based on the field aware property [\[56\]](#page-15-3), or higher-order FMs by directly expanding 2-order interactions with all feature interactions [\[66\]](#page-15-13). Despite the ability to model higher-order interactions, these models suffer from noisy feature interactions in the modeling process.

Researchers have explored the possibility of adopting neural models to automatically discover complex higherorder feature interactions for CTR prediction and recommendation. As shown in Table [3,](#page-5-0) besides FM based approaches, current related work on this topic can be classified into three categories: implicit MLP structures and explicit up to K-th order modeling, and tree enhanced models.

**MLP based High Order Modeling.**As the feature interactions are hidden, researchers proposed to first embed each feature with an embedding layer, and then exploit MLPs to discover high order correlations. This category can be seen as modeling feature interactions in an implicit way as MLPs are black-box approaches, and we do not know what kind of feature interactions from the output of the MLP structure models. Since MLPs suffer from training difficulties, some researchers proposed pretraining techniques [\[58\]](#page-15-5). Others injected specific structures in MLPs for better capturing feature interactions. DeepCrossing designed residual structures to add back the original input after every two layers of MLPs [\[60\]](#page-15-7). The NFM architecture has a proposed biinteraction operation before MLP layers [\[57\]](#page-15-4). PNN modeled both the bit-wise interactions of feature embedding interactions and vector-wise feature interactions [\[59\]](#page-15-6). Besides the complex high order interactions, another effective approach is to combine the MLP based high order modeling with the classical linear models [\[62\]](#page-15-9), [\[63\]](#page-15-10).
**Cross Network for K-th Order Modeling.**The cross network differs from the MLP based approaches with a carefully designed cross network operation, such that a Kth layer cross network models the up to Kth order feature interactions. The k th hidden layer output x<sup>k</sup> is calculated by the cross operation as: x<sup>k</sup> = x0xk−1w<sup>k</sup> +b<sup>k</sup> +xk−<sup>1</sup> [\[64\]](#page-15-11). Instead of operating cross operations at a bitwise level, xDeepFM applies cross interactions at the vector-wise level explicitly [\[65\]](#page-15-12). These kinds of models are able to learn bounded-degree feature interactions.
**Tree Enhanced Modeling.**As trees can naturally show cross feature interactions, researchers incorporated trees as a proxy for recommendation with cross feature explanation. Specifically, TEM [\[11\]](#page-14-10) first utilizes decision trees to extract high order interaction of features in the form of cross features, and then input embeddings of cross features into an attentive model to perform prediction. As a result, the depth of the decision tree determines the maximum degree of feature interactions. Furthermore, by combining embedding and tree based models seamlessly, TEM is able to unify their

strengths — strong representation ability and explainability.

### 3.2 Modeling Textual Content

Neural network technique has revolutionized Natural Language Processing (NLP) [\[67\]](#page-15-14), [\[68\]](#page-15-15). These neural NLP models enable multi-level automatic representation learning of textual content, and can be combined in the recommendation framework for better user and item semantic embedding learning. Given the above neural based NLP models, we discuss some typical textual enhanced recommendation models based on the above techniques. Textual content input for recommendation could be classified into two categories: the first category is the content descriptions associated with either items or users, such as the abstract of an article, or the content descriptions of a user. The second category links a user-item pair, such as users annotating tags to items, or writing reviews for products. For the second category, most models summarize the associated content with each user, and each item [\[69\]](#page-15-16), [\[70\]](#page-15-17). Under such a situation, the second category of content information degenerates to the first category. In the following, we do not distinguish the input content data types, and summarize the related work for modeling contextual content into the following categories: autoencoder based models, word embeddings, attention models, and text explanations for recommendation.
**Autoencoder based Models.**By treating item content as raw features, such as bag-of-words and item tag representations, these models use autoencoders and their variants to learn the bottleneck hidden content representations of items [\[30\]](#page-14-28), [\[54\]](#page-15-1), [\[71\]](#page-15-18), [\[72\]](#page-15-19), [\[73\]](#page-15-20), [\[74\]](#page-15-21), [\[75\]](#page-15-22), [\[76\]](#page-15-23), [\[77\]](#page-15-24), [\[78\]](#page-15-25). For example, Collaborative Deep Learning (CDL) [\[71\]](#page-15-18) is proposed to simultaneously learn each item i's embedding q<sup>i</sup> as a combination of two parts: a hidden representation from the item content x<sup>i</sup> with a stacked denoising autoencoder and an auxiliary embedding θ that is not encoded in the item content as:

$$
\mathbf{q}_i = f_e(\mathbf{x}_i) + \theta_i, \quad \theta_i \sim \mathcal{N}(0, \sigma^2)
$$
 (8)

where fe(x) transforms raw content input into a bottleneck hidden vector with an autoencoder. θ<sup>i</sup> is a free item latent vector that is not captured in the item content, which is similar to many classical latent factor based CF models. In the model optimization process, the objective function is to simultaneously optimize the rating based loss from users' historical behavior and the content-reconstruction loss from the autoencoder:

$$
\mathcal{L} = \mathcal{L}_R(\mathbf{R}, \hat{\mathbf{R}}) + \lambda \mathcal{L}_X(\mathbf{X}, f_d(f_e(\mathbf{X}))),
$$
 (9)

where λ is a parameter that measures the relative weight between the two loss terms. In the above optimization

function, R is the user-item rating matrix and Rˆ denotes the predicted rating. Similarly, X is the item content input and fd(fe(X)) is an reconstructed content from an autoencoder that encodes the item content into a bottleneck representation fe, and then reconstructs it with a decoder fd.

Following this basic autoencoder based recommendation model, some studies proposed improvements to consider the uniqueness of the content information. For example, instead of learning a deterministic vector representation of the item content, a Collaborative Variational AutoEncoder (CVAE) is proposed to simultaneously recover the rating matrix and the side content information with a variational autoencoder [\[74\]](#page-15-21). Researchers also proposed to leverage the item neighbor information from item content to better represent the bottleneck representation of the item [\[79\]](#page-15-26). For some recommendation scenarios, items are also associated with category information. A denoising autoencoder with weak supervision is proposed to learn the distributed representation vector of each item [\[80\]](#page-15-27). Besides, as both users and items could be associated with content information, dual autoencoder based recommendation models have been proposed [\[30\]](#page-14-28), [\[54\]](#page-15-1), [\[73\]](#page-15-20), [\[81\]](#page-15-28).
**Leveraging Word Embeddings for Recommendation.**Autoencoders provide general neural solutions for unsupervised feature learning, which do not take the uniqueness of text input into consideration. Recently, researchers proposed to leverage word embedding techniques for better content recommendation [\[69\]](#page-15-16), [\[82\]](#page-15-29), [\[83\]](#page-15-30), [\[84\]](#page-15-31), [\[85\]](#page-15-32), [\[86\]](#page-15-33), [\[87\]](#page-15-34), [\[88\]](#page-15-35). With the success of TextCNN [\[89\]](#page-15-36), a Convolutional Matrix Factorization (ConvMF) is proposed to integrate CNN into probabilistic matrix factorization [\[82\]](#page-15-29). Let x<sup>i</sup> denote the text input of item i. The item latent embedding matrix Q is then represented as a Gaussian distribution that centers around its embedding representation as:

$$
p(\mathbf{Q}|\mathbf{W}, \mathbf{X}, \sigma^2) = \prod_{i=1}^{|V|} \mathcal{N}(\mathbf{q}_i | TextCNN(\mathbf{W}, \mathbf{x}_i), \sigma^2), \qquad (10)
$$

where W is the parameters in TextCNN. Besides CNN based models, researchers also employed various state-ofthe-art content embedding techniques, such as RNNs for item content representation [\[90\]](#page-15-37).

Reviews widely appear in recommendation applications and are natural forms for users to express feelings about items. Given user's rating records and associated reviews, most review based recommendation algorithms aggregate historical review text of users (items) as user content input D(u) (item content input D(i)). DeepCoNN [\[69\]](#page-15-16) is a deep model for review based recommendation. As shown in Fig. [2,](#page-7-0) DeepCoNN consists of two parallel TextCNNs for content modeling: one focuses on learning user behaviors by exploiting review content D(u) written by user u, and the other one learns item embedding from reviews D(u) written for item i. After that, a factorization machine is proposed to learn the interaction between user and item latent vectors. Specifically, DeepCoNN can be formulated as:

$$
\hat{r}_{ui} = FM(TextCNN(D_u), TextCNN(D_i)).
$$
 (11)

Many studies have empirically found that the most predictive power of review text comes from the particular review of the target user to the target item. As the associated reviews of a user-item pair are not available in the test stage, TransNet is proposed to tackle the situation when the target review information is not available [\[83\]](#page-15-30). TransNet has a source network of DeppCoNN that does not include the joint review revui, and a target network that models the joint review of the current user-item pair (u, i). Therefore, the target network could approximate the predicted review revˆ ui for the test user-item pair even when users do not give reviews to items.
**Attention Models.**Attention mechanism has also been widely used in content enriched recommender systems. Given textual descriptions of an item, attention based models have been proposed to assign attentive weights to different pieces of content, such that informative elements are automatically selected for item content representation [\[91\]](#page-15-38), [\[92\]](#page-15-39), [\[93\]](#page-15-40), [\[94\]](#page-15-41), [\[95\]](#page-15-42), [\[96\]](#page-15-43), [\[97\]](#page-15-44), [\[98\]](#page-15-45). For example, given a tweet, the attention based CNN learns the trigger words in the tweet for better hashtag recommendation [\[91\]](#page-15-38). With the historical rated items of a user, an attention model is proposed to selectively aggregate content representations of each historical item for user content preference embedding modeling [\[99\]](#page-15-46), [\[100\]](#page-15-47), [\[101\]](#page-15-48). Given user (item) collaborative embeddings, and content based embeddings, attention networks have also been designed to capture the correlation and alignment between these two kinds of data sources [\[98\]](#page-15-45), [\[102\]](#page-15-49). Researchers have also proposed a co-evolutionary topical attention regularized matrix factorization model, with the user attentive features learned from an attention network that combines the user reviews, and the item attentive features learned from an attention network that combines the item reviews [\[102\]](#page-15-49). For review based recommendation, researchers argued that most content based user and item representation models neglected the interaction behavior between user-item pairs, and a dual attention model named DAML is proposed to learn the mutual enhanced user and item representations [\[103\]](#page-15-50). As item content sometimes is presented in multi-view forms (e.g., title, body, keywords and so on), multi-view attention networks are applied to learn unified item representations by aggregating multiple representations from different views [\[104\]](#page-15-51), [\[105\]](#page-15-52), [\[106\]](#page-15-53). With both the textual descriptions and the image visual information, co-attention is utilized to learn the correlation between the two modalities for better item representation learning [\[107\]](#page-16-0), [\[108\]](#page-16-1).
**Text Explanations for Recommendation.**Instead of improving recommendation accuracy with content input, there is a growing interest of providing text explanations for recommendation. Current solutions for explainable recommendations with text input can be classified into two categories:*extraction based models*and*generation based models*.

*Extraction based models*focus on selecting important text pieces for recommendation explanation. Attention techniques are widely used for extraction based explainable recommendation, with the learned attentive weights empirically showing the importance of different elements for model output [\[104\]](#page-15-51), [\[109\]](#page-16-2). After that, the text pieces with larger attentive weights are extracted as recommendation explanations. Despite extracting text pieces from reviews, there exist other methods to extract useful text information for explanation, such as review-level explanations [\[109\]](#page-16-2), [\[110\]](#page-16-3).

With the huge success of language generation tech-

<span id="page-7-0"></span>![](_page_7_Figure_1.jpeg)
<!-- Image Description: The image presents three diagrams (A, B, C) illustrating the architectures of DeepCoNN, VBPR, and DiffNet, respectively. (A) shows a multi-layered neural network processing user and item review text. (B) depicts a model using a pretrained deep CNN to extract visual features from an item image, followed by factorisation. (C) illustrates DiffNet, showing user and item feature embedding and processing through multiple layers, culminating in a prediction. Each diagram visually represents a different recommendation system architecture. -->

Fig. 2: The classical methods for content-enriched models

niques [\[111\]](#page-16-4),*generation based models*draw more and more attention [\[70\]](#page-15-17), [\[112\]](#page-16-5), [\[113\]](#page-16-6), [\[114\]](#page-16-7), [\[115\]](#page-16-8), [\[115\]](#page-16-8), [\[116\]](#page-16-9). Given both users' rating records and reviews, the key idea of these models is to design an encoder-decoder structure, with the encoder part encodes related embeddings of users and items, and the decoder generates reviews that are similar to the ground truth of the corresponding user-item review text. NRT is a state-of-the-art model that simultaneously predicts ratings and generates reviews [\[112\]](#page-16-5). By taking the one-hot user representation and item representation, the encoder part outputs the user latent embedding and item latent embedding, the review is generated with an RNN based decoder structure, and the rating is predicted with an MLP structure. Since we have both the ground truth rating records and the corresponding records of users, the two tasks of rating prediction and review generation can be trained in a multi-task framework. Meanwhile, additional information and more advanced encoder-decoder structures are also applied to explanation generation. For example, user and item attributes [\[113\]](#page-16-6), [\[117\]](#page-16-10) are multimodal item data [\[118\]](#page-16-11), which are considered in the encoder. Then, an advanced attention selector [\[114\]](#page-16-7) is designed in the decoder.

#### 3.3 Modeling Multimedia Content

With the popularity of multimedia based platforms, visual content based multimedia contents, e.g., images and videos, are the most eye-catching for users. In the following, we introduce related work on modeling multimedia content in recommender systems. For ease of explanation, we summarize the related work on multimedia based recommendation with different kinds of input data in Table [4.](#page-8-0)

#*3.3.1 Modeling Image Information*The current solutions for image recommendation can be categorized into two categories: content based models and hybrid recommendation models. Content based models exploit visual signals for constructing item visual representations, and the user preference is represented in the visual space [\[108\]](#page-16-1), [\[122\]](#page-16-12), [\[123\]](#page-16-13), [\[124\]](#page-16-14), [\[131\]](#page-16-15), [\[144\]](#page-16-16), [\[145\]](#page-16-17), [\[146\]](#page-16-18), [\[147\]](#page-16-19). In contrast, the hybrid recommendation models alleviate the data sparsity issue in CF with item visual modeling [\[26\]](#page-14-22), [\[119\]](#page-16-20), [\[121\]](#page-16-21), [\[130\]](#page-16-22), [\[134\]](#page-16-23), [\[148\]](#page-16-24), [\[149\]](#page-16-25).
**Image Content based Models.**Image content based models are suitable for recommendation scenarios that rely heavily on visual influence (e.g., fashion recommendation) or new items with little user feedback. As visual images are often associated with text descriptions (e.g., tags, titles), researchers designed some unpersonalized recommender systems that suggest tags to images [\[108\]](#page-16-1), [\[145\]](#page-16-17). These models apply CNNs to extract image visual information, and content embedding models to get textual embedding. Then, in order to model the correlation between visual and textual information, these models either project text and images into a same space [\[122\]](#page-16-12), concatenate representations from different modalities [\[133\]](#page-16-26) or design co-attention mechanism to better describe items [\[107\]](#page-16-0), [\[108\]](#page-16-1).

For personalized image recommendation, a typical solution is to project both users and items in the same visual space, with the item visual space derived from CNNs, and the user's visual preference either modeled by the items they like [\[144\]](#page-16-16) or a deep neural network that takes the user related profiles as input [\[131\]](#page-16-15), [\[146\]](#page-16-18). Researchers have also argued that CNNs focus on the global item visual representation without fine-grained modeling. Therefore, some sophisticated image semantic understanding models have been proposed to enhance image recommendation performance [\[122\]](#page-16-12), [\[123\]](#page-16-13), [\[124\]](#page-16-14), [\[125\]](#page-16-27). For instance, in order to suggest makeups for people, makeup related facial traits are first classified into structured coding. The facial attributes are then fed into a deep learning based recommendation system for personalized makeup synthesis [\[124\]](#page-16-14). In some visual based recommendation domains, such as the fashion domain, each product is associated with multiple semantic attributes [\[123\]](#page-16-13), [\[125\]](#page-16-27). To exploit users' semantic preferences for detailed fashion attributes, a semantic attributed explainable recommender system is proposed by projecting both users and items in a fine-grained interpretable semantic attribute space [\[123\]](#page-16-13).
**Hybrid Recommendation Models.**Hybrid models utilize both the collaborative signals and the visual content for recommendation, which could alleviate the data sparsity issue in CF and improve recommendation performance. Some researchers proposed to first extract item visual information as features, and the item visual features are fed into factorization machines for recommendation. Instead of the inferior performance induced by the two step learning process, recent studies proposed end-to-end learning frameworks for hybrid visual recommendation [\[26\]](#page-14-22), [\[119\]](#page-16-20), [\[130\]](#page-16-22), [\[134\]](#page-16-23), [\[140\]](#page-16-28), [\[148\]](#page-16-24). Visual Bayesian Personalized Ranking (VBPR) is one of the first few attempts that leverage the visual content for unified hybrid recommendation [\[119\]](#page-16-20). In VBPR, each user (item) is projected into two latent spaces: a visual space that is projected from the CNN based visual features, and a collaborative latent space to capture users' latent preferences. Then, given a user-item pair (u, i) with

<span id="page-8-0"></span>

| Category             | Model Summarization                                                  | Models                                    |  |
|----------------------|----------------------------------------------------------------------|-------------------------------------------|--|
|                      | CNN content based features                                           | ACF [26],VBPR [119],OutfitNet [120]       |  |
|                      | Aesthetic based features pretrained from                             | BDN [121]                                 |  |
| Image                | a deep aesthetic network                                             |                                           |  |
|                      | CNN content based features and the style features                    | DMF [122]                                 |  |
|                      | from feature maps of CNNS                                            |                                           |  |
|                      | Fine grained image attributes                                        | SAERS [123], SNMO [124], AIC [125]        |  |
|                      | Co-attention networks for learning enhanced                          | UVCAN [126]                               |  |
|                      | user and image representation                                        |                                           |  |
|                      | GNNs to model visual relationships                                   | PinSage [127], HFGN [128], TransGec [129] |  |
| Image+ Behavior Time | CNN based temporal content evolution                                 | BDN [121], [130]                          |  |
|                      |                                                                      | DMF [122], GraphCAR [131],                |  |
|                      | Deep fusion networks to learn unified item representation            | CKE [132], Transnfcm [133]                |  |
| Image+Text           | Co-attention networks for learning unified item representation       | CoA-CAMN [107], Co-Attention [108]        |  |
|                      | Multi-task learning model with detailed image attributes             | [134]                                     |  |
|                      | Text generation models by encoding user, item text and image content | VECF [117], KFRCI [135], MRG [118], [136] |  |
| Audio                | Learning deep audio features                                         | HLDBN [137], [138], [139]                 |  |
|                      | Attention networks to learn video representations from               |                                           |  |
| Video                | multiple image representations                                       | ACF [26], JIFR [140], AGCN [141]          |  |
|                      | GNNs to learn video representation                                   | AGCN [141]                                |  |
| Video+Audio          | Deep fusion networks to learn unified item representation            | CDML [142], [143]                         |  |

the associated image x<sup>i</sup> , the predicted preference rˆui is learned by combining users' preferences from two spaces:

$$
\hat{r}_{ui} = \mathbf{p}_u^T \mathbf{q}_i + \mathbf{w}_u^T f(CNN(x_i)),\tag{12}
$$

where f(CNN(xi)) denotes the item content representation by transforming items from the original visual space CNN(xi). In this equation, the first term models the collaborative effect with free user latent vector p<sup>u</sup> and item latent vector q<sup>i</sup> . The second term models the visual content preference with the item visual embeddings as f(CNN(xi), and the user visual embedding w<sup>u</sup> in the visual space.

Given the basic idea of VBPR, researchers have further introduced the temporal evolution of visual trends in the visual space [\[130\]](#page-16-22), or the associated location representation of the image [\[148\]](#page-16-24). Instead of representing users' preferences into two spaces, the visual content of the item has been leveraged as a regularization term in matrix factorization based models, ensuring that the learned item latent vector of each item is similar to the visual image representation learned from CNNs [\[130\]](#page-16-22). Besides learning the CNN content representations for item visual representation, many models have been proposed to consider additional information from the imagery for item visual representation, such as the pretrained aesthetics learned from a deep aesthetic network [\[121\]](#page-16-21). As users show time-synchronized comments on video frames, researchers proposed a multi-modal framework to simultaneously predict users' preferences to key frames and generate personalized comments [\[135\]](#page-16-35). Compared to review generation models [\[112\]](#page-16-5), the visual embedding is injected into both the user preference prediction part, as well as each hidden state of the LSTM architecture for better text generation.

Recently, GNNs have shown powerful performance in modeling graph data with heuristic graph convolution [\[150\]](#page-16-43), [\[151\]](#page-16-44). PinSage is one of the first few attempts to apply GNNS for web-scale recommender systems [\[127\]](#page-16-31). Given an item-item correlation graph, PinSage takes node attributes as input, and iteratively generates node embeddings to learn the graph structure with iterative graph convolutions. Researchers also proposed to formulate a heterogeneous graph of users, outfits and items, and performed hierarchical GNNs for personalized outfit recommendation [\[128\]](#page-16-32).

#*3.3.2 Video Recommendation*Researchers proposed content-based video recommender systems with rich visual and audio information [\[142\]](#page-16-41), [\[143\]](#page-16-42). Specifically, these proposed models first extracted video features and audio features, and then adopted a neural network to fuse these two kinds of features with early fusion or late fusion techniques. As these content based video recommendation models do not rely on user-video interaction behavior, they can be applied to new video recommendation without any historical behavior data [\[142\]](#page-16-41), [\[143\]](#page-16-42). In contrast to the content-based recommendation models, with user-video interaction records, researchers proposed an Attentive Collaborative Filtering (ACF) model for multimedia recommendation [\[26\]](#page-14-22). ACF leverages the attention mechanism with visual inputs to learn the attentive weights to summarize users' preferences for historical items and the components of the item.

The key idea of ACF is to leverage users' multimedia behavior and explicitly project users into two spaces: a collaborative space and a visual space, such that users' key frame preference could be approximated in visual space. The authors designed a model to discern both the collaborative and visual dimensions of users, and model how users make decisive item preferences from these two aspects [\[140\]](#page-16-28).

## 3.4 Modeling Social Network

With the emergence of social networks, users like to perform item preferences on these social platforms and share their interests with social connections. Social recommendation has emerged in these platforms, with the goal to model the social influence and social correlation among users to boost recommendation performance. The underlying reason for social recommendation is the existence of social influence among social neighbors, leading to the correlation of users' interests in a social network [\[152\]](#page-16-45), [\[153\]](#page-16-46), [\[154\]](#page-16-47), [\[155\]](#page-16-48), [\[156\]](#page-16-49), [\[157\]](#page-16-50), [\[158\]](#page-16-51). We summarize social recommendation models into following two categories: the social correlation enhancement and regularization models, and GNN based models.
**Social Correlation Enhancement and Regularization.**By treating users' social behavior as the social domain and item preference behavior as the item domain, the social correlation enhancement and regularization models tried to fuse users' two kinds of behaviors from two domains in a unified representation. For each user, her latent embedding p<sup>u</sup> is composed of two parts: a free embedding e<sup>u</sup> from the item domain, and a social embedding h<sup>u</sup> that is similar with social connections in the social domain [\[152\]](#page-16-45), [\[155\]](#page-16-48), [\[157\]](#page-16-50), [\[159\]](#page-16-52), [\[160\]](#page-16-53). In other words, we have:

$$
\mathbf{h}_u = g(u, \mathbf{S})\tag{13}
$$

$$
\mathbf{p}_u = f(\mathbf{e}_u, \mathbf{h}_u),\tag{14}
$$

where g models the social embedding part with the social network structure as input, and f fuses the two kinds of embeddings, such as concatenation, addition or neural networks. Different models vary in the detailed implementation of the social domain representation hu. For example, it can be directly learned from the social network embedding models [\[152\]](#page-16-45), aggregated from the social neighbors' embedding [\[155\]](#page-16-48), [\[159\]](#page-16-52), or transferred from the social domain to item domain with attention based transfer learning models [\[157\]](#page-16-50). Besides, the social network is also utilized as a regularization term in the model optimization process, with the assumption that connected users are more similar in the learned embedding space [\[152\]](#page-16-45).

In the real-world, users' interests are dynamic over time due to users' personal interests change and the varying social influence strengths. Researchers extended the social correlation based model with RNN to model the evolution of users' preferences under dynamic social influences [\[153\]](#page-16-46), [\[154\]](#page-16-47). Specifically, for each user u, her latent preferences h t a at time t could be modeled as the transition from her previous latent preference h t−1 u , as well as the social influence from social neighbors at t − 1 as:

$$
\mathbf{h}_u^t = f_{RNN}(R_u^t, \mathbf{h}_u^{t-1}, \sum_{a \in S_u} t_{au} \mathbf{h}_a^{t-1})
$$
(15)

where R<sup>t</sup> <sup>u</sup> <sup>P</sup> is the temporal behaviors of user u at this time, a∈S<sup>u</sup> tauh t−1 <sup>a</sup> denotes the influences from her social neighbors. In particular, the social influence strength tau could be simply set as equally for each social neighbor, or with attention modeling for influence strength inference.
**GNN Based Approaches.** Most of the above social recommendation models utilized the local first-order social neighbors for social recommendation. In the real world, the social diffusion process presents a dynamic recursive effect to influence a user's decision. In other words, each user is influenced recursively by the global social network graph structure. To this end, researchers argued that it is better to leverage the GNN based models to better model the global social diffusion process for recommendation. DiffNet is designed to simulate how users are influenced by the recursive social diffusion process for social recommendation with the social GNN modeling. Specifically, DiffNet recursively diffuses the social influence from step 0 to the stable diffusion depth K. Let h k <sup>u</sup> denote the user embedding at the k th diffusion process, which is modeled as:

<span id="page-9-1"></span><span id="page-9-0"></span>
$$
\mathbf{h}_u^0 = f_{NN}(\mathbf{x}_u, \mathbf{e}_u) \tag{16}
$$

$$
\mathbf{h}_{Su}^{(k-1)} = Pool(\mathbf{h}_{a}^{(k-1)} | a \in S_u)
$$
\n(17)

<span id="page-9-2"></span>
$$
\mathbf{h}_u^k = s(W^k[\mathbf{h}_{Su}^{k-1}, \mathbf{h}_u^{(k-1)}])
$$
 (18)

where Eq.[\(16\)](#page-9-0) fuses the user feature x<sup>u</sup> and user free latent vector e<sup>u</sup> with a neural network fNN for initial influence diffusion. At each diffusion step k, Eq.[\(17\)](#page-9-1) models the influence diffusion from u's social neighbors, and Eq.[\(18\)](#page-9-2) depicts the user embedding at the recursive step k by fusing her previous embedding h k−1 u and influences from her social neighbors as h k−1 Su . As k diffuses from step 1 to depth K, the recursive social diffusion process is captured.

Instead of performing GNNs on the user-user social graph, researchers have also considered jointly modeling the social diffusion process in the social network and the interest diffusion process in the user-item graph with heterogeneous GNN based models [\[158\]](#page-16-51), [\[161\]](#page-17-0), [\[162\]](#page-17-1), [\[163\]](#page-17-2), [\[164\]](#page-17-3), [\[165\]](#page-17-4), [\[166\]](#page-17-5). For instance, DiffNet++ is proposed to jointly model the interest diffusion from user-item bipartite graph and the influence diffusion from the user-user social graph for user modeling in social recommendation, and have achieved state-of-the-art performance [\[164\]](#page-17-3).

# 3.5 Modeling Knowledge Graph

Researchers have also considered leveraging Knowledge Graphs (KG) for recommendation, which provide rich side information for items (*i.e.,*item attributes and external knowledge). Typically, KG organizes such subject-propertyobject facts in the form of directed graph G = {(h, r, t|h, t ∈ E, r ∈ R)}, where each triplet presents that there is a relationship r from head entity h to tail entity t. Exploring such interlinks, as well as user-item interactions, being a promising solution to enrich item profile and enhance the relationships between users and items. Furthermore, such graph structure endows recommender systems the ability of reasoning and explainability [\[167\]](#page-17-6), [\[168\]](#page-17-7), [\[169\]](#page-17-8), [\[170\]](#page-17-9), [\[171\]](#page-17-10), [\[172\]](#page-17-11), [\[173\]](#page-17-12). Recent efforts for KG enhanced recommendation can be roughly categorized into three categories: pathbased models [\[168\]](#page-17-7), [\[174\]](#page-17-13), [\[175\]](#page-17-14), [\[176\]](#page-17-15), [\[177\]](#page-17-16), regularizationbased models [\[132\]](#page-16-34), [\[169\]](#page-17-8), [\[178\]](#page-17-17), [\[179\]](#page-17-18), and GNN-based approaches [\[97\]](#page-15-44), [\[128\]](#page-16-32), [\[141\]](#page-16-40), [\[170\]](#page-17-9), [\[180\]](#page-17-19), [\[181\]](#page-17-20), [\[182\]](#page-17-21), [\[183\]](#page-17-22), [\[184\]](#page-17-23), [\[185\]](#page-17-24), [\[186\]](#page-17-25), [\[187\]](#page-17-26).
**Path Based Methods.** Many efforts introduce metapaths [\[174\]](#page-17-13), [\[176\]](#page-17-15), [\[177\]](#page-17-16), [\[188\]](#page-17-27), [\[189\]](#page-17-28), [\[190\]](#page-17-29), [\[191\]](#page-17-30), [\[192\]](#page-17-31) and paths [\[168\]](#page-17-7), [\[175\]](#page-17-14), [\[193\]](#page-17-32), [\[194\]](#page-17-33), [\[195\]](#page-17-34) that present high-order connectivity between users and items, and then feed them into predictive models to directly infer user preferences. In particular, a path from user u to item i can be defined as a sequence of entities and relations: p = [e<sup>1</sup> <sup>r</sup><sup>1</sup> −→ e<sup>2</sup> <sup>r</sup><sup>2</sup> −→ · · · <sup>r</sup>L−<sup>1</sup> −−−→ <sup>e</sup>L], where <sup>e</sup><sup>1</sup> <sup>=</sup> <sup>u</sup> and <sup>e</sup><sup>L</sup> <sup>=</sup> <sup>i</sup>, and (e<sup>l</sup> , r<sup>l</sup> , el+1) is the l-th triplet in p, and L−1 denotes the number of triplets in the path. As such, the set of paths connecting u and i can be defined as P(u, i) = {p}.

FMG [\[176\]](#page-17-15), MCRec [\[177\]](#page-17-16), and KPRN [\[168\]](#page-17-7) convert the path set into an embedding vector to represent the user-item connectivity. Such paradigm can be summarized as follows:

$$
\mathbf{c} = f_{\text{Pooling}}(\{f_{\text{Embed}}(p)|p \in \mathcal{P}(u,i)\}),\tag{19}
$$

where fEmbed(·) embeds path p as a trainable vector. fPooling(·) is the pooling operation to synthesize all path information into the connectivity representation, such as the attention networks adopted in MCRec and KPRN. RippleNet [\[196\]](#page-17-35) constructs ripple set (*i.e.,*high-order neighboring items derived from P) for each user to enrich her representations.

While explicitly modeling high-order connectivity, it is highly challenging in real-world recommendation scenarios because most of these methods require extensive domain knowledge to define meta-paths or labor-intensive feature engineering to obtain qualified paths [\[167\]](#page-17-6), [\[170\]](#page-17-9). Moreover, the scale of paths can easily reach millions or even larger when a large number of KG entities are involved, making it prohibitive to efficiently transfer knowledge.
**Regularization Based Methods.**This research line devises a joint learning framework, where direct user-item interactions are used to optimize the recommender loss, and KG triples are utilized as additional loss terms to regularize the recommender model learning. In particular, the anchors between two modeling components are the embeddings of the overlapped items. CKE [\[132\]](#page-16-34) makes use of Knowledge Graph Embedding (KGE) techniques, especially TransR [\[197\]](#page-17-36), to generate additional representations of items, and then integrates them with item embeddings of the recommender MF, which is defined as:

$$
\mathbf{q}_i = f_{\text{Embed}}(i) + f_{\text{KGE}}(i|\mathcal{G}),\tag{20}
$$

where fEmbed(·) is the embedding function which takes the item ID as the input, while fKGE is the output of KGE method which considers the KG structure. Similarly, DKN [\[198\]](#page-17-37) generates item embeddings from NCF and TransE. These approaches focus on enriching item representations by the joint learning framework.
**GNN Based Methods.**The regularization-based methods only take direct connectivity between entities into consideration, while encoding the high-order connectivity in a rather implicit manner. Due to the lack of explicit modeling, neither the long-range connectivities are guaranteed to be captured, nor the results of high-order modeling are interpretable [\[170\]](#page-17-9). More recent studies, such as KGAT [\[170\]](#page-17-9), CKAN [\[199\]](#page-17-38), MKM-SR [\[200\]](#page-17-39), and KGCN [\[180\]](#page-17-19), get inspired by the advances of GNNs and explore the message-passing mechanism over graphs to exploit high-order connectivity in an end-to-end fashion.

KGAT [\[170\]](#page-17-9) encodes user-item interactions and KG as a unified relational graph by representing each user behavior as a triplet, (u, Interact, i). Based on the item-entity alignment set, the user-item bipartite graph can be seamlessly integrated with KG as a so-called collaborative knowledge graph G = {(h, r, t)|h, t ∈ E<sup>0</sup> , r ∈ R}, where E <sup>0</sup> = E ∪ U and R<sup>0</sup> = R ∪ {Interact}. Over such graph, KGAT recursively propagates the embeddings from a node's neighbors (which can be users, items, or other entities) to refine the node's embedding, and employs an attention mechanism to discriminate the importance of the neighbors as:

$$
\mathbf{p}_u = f_{\text{GNN}}(u, \mathcal{G}),\tag{21}
$$

where fGNN(·) is the GNN component.
**Summary:**Auxiliary data, such as text, multimedia, and social network, is capable of enhancing the user and item

representation learning and boosting the recommendation performance. The keys are the selection of auxiliary data and the integration methods. For example, text information can help models to generate corresponding recommendation explanation. Social network information is very useful to provide social influence and social correlation among users for better recommendation. Meanwhile, attention mechanism is a general method to select the most relevant information from auxiliary data to enhance the representation learning. GNN-based methods are good at obtaining structure information and high-order correlation for the utilization of auxiliary data. As a conclusion, based on the recommendation target (recommendation accuracy, explanation, cold-start problem, etc), selecting proper auxiliary data and integration method can help recommendation models to achieve a good performance.

# <span id="page-10-0"></span>4 TEMPORAL/SEQUENTIAL MODELS

Users' preferences are not static but evolve over time. Instead of modeling users' static preferences with the aforementioned models, temporal/sequential based recommendation focuses on modeling users' dynamic preferences or sequential patterns over time. Given a userset U = [u1, u2, ..., uM] and an itemset V = [i1, i2, ..., i<sup>N</sup> ], current temporal/sequential recommendation could be generally classified into three categories:

-*Temporal based recommendation*: For a user u ∈ U and an item i∈V, the associated user-item interaction behavior is denoted as a quadri-tuple as [u, i, rui, tui]. In this representation, rui denotes the detailed rating and tui is the timestamp of this behavior. Temporal recommendation focuses on modeling the temporal dynamics of users' behavior over time.
- *Session based recommendation*: In a certain session ∫ = [i1, i2, ..., i<sup>|</sup>S<sup>|</sup> ] (s ⊆ V), a user interacts with a collection of items (e.g., consumption with a shopping basket, browsing the internet in a limited time period). In many session based applications, users do not log in and user IDs are not available [\[201\]](#page-17-40), [\[202\]](#page-17-41), [\[203\]](#page-17-42). Therefore, the popular direction of session based recommendation is to mine the sequential item-item interaction patterns from the session data for better recommendation.
- *Temporal and session based recommendation*: This approach combines the definition of temporal recommendation and session recommendation, in which each transaction is described as [u, s, t], with s ⊆ V is a collection of items that are consumed at a particular time t. Under this scenario, both the temporal evolution and the sequential patterns of items need to be captured.

We summarize the main techniques for modeling temporal and sequential effects in recommender systems in Table [5](#page-11-0) and illustrate some representative work in Fig. [3.](#page-12-1)

## 4.1 Temporal based recommendation

Temporal recommendation models focus on capturing the temporal evolution of users' preferences over time. Due to the superior of RNNs in modeling temporal patterns, many temporal based approaches take RNNs into consideration. Recurrent Recommender Networks (RRN) is one of the

<span id="page-11-0"></span>

| Model Type        | Model Summarization                                 | Models                                       |  |
|-------------------|-----------------------------------------------------|----------------------------------------------|--|
|                   | Recurrent neural networks                           | ARSE [153],RRN [204]                         |  |
| Temporal Models   | to capture temporal evolution                       | [205], [206], [207], [208], [209]            |  |
|                   | Memory network based models                         | NMRN [210], MANN [211], STAMP [212]          |  |
|                   | RNN based models that rely on sessions              | p-RNN [202],KERL [193],CRNNs [213],          |  |
|                   | to construct input and output                       | NARM [214], [215], [216], [217], [201],      |  |
|                   | Translation based models for modeling               | TransRec [46],PeterRec [218], [219]          |  |
| Sequential Models | the correlations of consecutive items               |                                              |  |
|                   | Convolutional sequence embedding models             | 3D CNNs [220]                                |  |
|                   | Self attention for learning item correlations       | SASRec [221], MFGAN [222]                    |  |
|                   | Memory network to learn the session representation  | DMN [223]                                    |  |
|                   | GNN based models for learning                       | SR-GNN [203],GC-SAN [224],Gag [225],         |  |
|                   | item correlations                                   | GCE-GNN [226],SGNN-HN [227], [228]           |  |
|                   | Hierarchical attention networks with                | SHAN [229],HRM [230],HGN [231],              |  |
|                   | long and short term interest                        | MARank [232],Fissa [233],SSE-PT [234]        |  |
|                   | RNN based models                                    | RRN [235],BINN [204],HIERNN [236]            |  |
| Temporal and      | Attention based models for                          | CTRec [237],M3 [238],S3-rec [239],CTA [240], |  |
| Sequential Models | user interest modeling                              | MTAM [241],TASER [242],ReChorus [243]        |  |
|                   | Memory Networks for long distance item correlations | KA-MemNN [244],CSRM [245],MTAM [241]         |  |
|                   | CNN based models                                    | Caser [51],CTRec [237], [246]                |  |
|                   | GNN based models                                    | HyperRec [247],MA-GNN [248],IMfOU [249]      |  |

representative studies for temporal recommendation by endowing both users and items with an LSTM autoregressive architecture [\[204\]](#page-17-43). In RRN, the predicted rating rˆ t ui of user u to item i at time t is modeled as:

$$
\hat{r}_{ui}^t = f(\mathbf{p}_u^t, \mathbf{q}_i^t) \quad \text{where} \tag{22}
$$

$$
\mathbf{p}_u^t = RNN(\mathbf{p}_u^{(t-1)}, \mathbf{W}\mathbf{x}_u^t), \quad \mathbf{q}_i^t = RNN(\mathbf{q}_i^{(t-1)}, \mathbf{W}\mathbf{x}_i^t) \tag{23}
$$

where p t u and q t i are the dynamic embeddings of user u and item i at time t, respectively. Specifically, f in Eq.[\(22\)](#page-11-1) is a temporal rating prediction function. Eq.[\(23\)](#page-11-2) models the evolution of users and items' dynamic embeddings with RNN architecture. As the user side and item side share similar LSTM structure, we take the user side as an example. x t <sup>u</sup> ∈ R |V | is a rating vector for u between t − 1 and current time t, with each element x t ul denotes the rating of user u to each item l at that time. W is a transformation matrix that needs to be learned. Therefore, RRN learns the evolution of user and item latent vectors over time with two RNNs. Based on RRNs, rich context factors were considered, such as the social influence [\[153\]](#page-16-46), [\[207\]](#page-17-46), item metadata [\[208\]](#page-17-47), [\[250\]](#page-18-40) and multimedia data fusion [\[251\]](#page-18-41). Take the RNN in the user side as an example, and we can generalize the user latent embedding evolution as:

$$
\mathbf{p}_u^t = RNN(\mathbf{p}_u^{(t-1)}, \mathbf{W}\mathbf{x}_u^t, ContextualEmbedding), \tag{24}
$$

where additional contextual embeddings are also injected to model temporal evolution of users' temporal embedding.

Recently, an emerging trend is to model the temporal evolution with Neural Turning Machines [\[252\]](#page-18-42) and Memory Networks [\[253\]](#page-18-43). Compared to RNNs, memory networks introduce a memory matrix to store the states in memory slots, and update memories over time with read and write operations. As the memory storage is limited, the key component in applying memory networks in recommendation is how to update memories over time with users' temporal behavior. Researchers proposed a general memory augmented neural network with user memory networks to store and update users' historical records, and the user memory network is implemented from the item and feature level [\[211\]](#page-18-1). Researchers further proposed to use attention mechanism in the memory reading and writing process with soft-addressing, in order to better capture users' long-term stable and short-term temporal interests [\[210\]](#page-18-0).

## <span id="page-11-2"></span><span id="page-11-1"></span>4.2 Session based recommendation

Many real-world recommender systems often encounter the short session data from anonymous users, i.e., the user ID information is not available. Session based recommendation is popular under this situation, which models the sequential item transition patterns given many session records. Hidasi et al. [\[201\]](#page-17-40) made one of the first few attempts to design GRU4REC for session based recommendation under the RNN based framework. Specifically, GRU4REC resembles an RNN structure, which recursively takes the current item in the session as input, updates the hidden states, and outputs the predicted next item based on the hidden state. Given anonymous sessions, the key component of GRU4REC is how to construct mini-batches to suit the data forms of RNNs. Since the goal is to capture how a session evolves over time with item dependencies, the authors designed a session parallel min-batches. The first events of the first several sessions are extracted to form the first mini-batch, with the desired output is the second event of the corresponding session. Under such a formulation, the complex correlations of items in a session are captured for session based recommendation.

GRU4REC has been further investigated with item feature consideration [\[202\]](#page-17-41), local intent [\[214\]](#page-18-4), user information consideration [\[254\]](#page-18-44), data augmentation techniques [\[215\]](#page-18-5). By treating item ID, name, and category with an embedding matrix, a sequence of clicks could be represented as frames. Therefore, the architecture of 3D CNNs could be transferred to session-based recommendation [\[220\]](#page-18-10). Furthermore, a self attention based sequential model of SASRec is proposed. SASRec models the entire user sequence without any recurrent and convolutional operations, and adaptively considers consumed items for recommendation [\[221\]](#page-18-11).

Researchers also proposed a translation based model to capture the personalized sequential third order interactions

<span id="page-12-1"></span>![](_page_12_Figure_1.jpeg)
<!-- Image Description: The image displays architectural diagrams of three recommendation systems: GRU4Rec, SASRec, and SR-GNN. (A) shows GRU4Rec as a sequence of GRU layers processing embedded input items. (B) illustrates SASRec with self-attention and feed-forward networks for sequence prediction. (C) depicts SR-GNN using a graph neural network and attention mechanism to model user-item relationships, culminating in a softmax layer to predict item probabilities. Each diagram visually represents the model's components and data flow. -->

Fig. 3: The classical methods for temporal/sequential Models

between a user u, the previous item j, and the current item i. Given the item embedding matrix Q, each user's embedding p<sup>u</sup> can be approximated as: q<sup>i</sup> + p<sup>u</sup> ≈ q<sup>j</sup> [\[46\]](#page-14-46). Therefore, the translation based models capture the correlation of two constructive items.

While above models built relationships between consecutive items in a session, how to globally model the transitions in a session among distant items remain under explored. Researchers adopted GNNs for session based recommendation [\[203\]](#page-17-42), [\[224\]](#page-18-14), [\[225\]](#page-18-15), [\[226\]](#page-18-16), [\[227\]](#page-18-17), [\[228\]](#page-18-18), [\[255\]](#page-18-45), [\[256\]](#page-18-46). SR-GNN is one of the first few attempts. As shown in Fig. [3,](#page-12-1) the graph is constructed by taking all items as the graph node set, and there is an edge between two nodes if these two nodes appear in consecutive orders in a session. Then, the GNN is adopted to learn item embeddings, such that the higher-order relationships of items from session behavior data can be modeled [\[203\]](#page-17-42). Different GNN based models vary in graph construction, and graph aggregation process [\[224\]](#page-18-14), [\[225\]](#page-18-15), [\[226\]](#page-18-16).

### 4.3 Temporal and session based recommendation

Given the session data of each user over time, models in this category leverage both the temporal evolution modeling of users, as well as the sequential item patterns hidden in the sessions for recommendation. Currently, the solutions could be classified into two categories: the first category learns both users' long term preference and the short term dynamic preferences, and the second category adopts advanced neural models for learning a unified user representation.

In the first category, each user's long term preference is modeled from her historical behaviors, and the short term dynamics is modeled from the previous session or the current session [\[229\]](#page-18-19), [\[230\]](#page-18-20), [\[232\]](#page-18-22) . For example, researchers proposed hierarchical attention networks for temporal and session based recommendation, with the first attention layer learns the user long term preference based on historical records, and the second one attentively aggregates user representation from the current session as:

$$
\mathbf{p}_u^t = Att_2(\mathbf{p}_u, Att_1(\mathbf{q}_l, l \in T_u^{(t-1)})),\tag{25}
$$

where Att<sup>1</sup> denotes the bottom layer attention network that depicts the user's short term preference from recent user behavior T (t−1) <sup>u</sup> , and Att<sup>2</sup> is a top layer attention network that balances the short term user preference and long term preference embedding vector pu. Instead of using hierarchical attentions, researchers proposed to adopt attention techniques to learn item correlations, and designed recurrent states at top layers for sequential recommendation [\[240\]](#page-18-30).

Hierarchical RNNs are also proposed for personalized session-based recommendation over time, with a session level GRU unit to model the user activity within sessions, and a user level GRU models the evolution of the user preference over time [\[200\]](#page-17-39), [\[236\]](#page-18-26). Besides, researchers exploited hierarchical attention networks to learn better short term user preference with feature-level attention and item level attention [\[231\]](#page-18-21). For the long term user interest modeling, researchers proposed to leverage nearby sessions [\[235\]](#page-18-25), designed attention modeling or memory addressing techniques to find related sessions [\[237\]](#page-18-27), [\[244\]](#page-18-34), [\[245\]](#page-18-35), [\[257\]](#page-18-47).

Another kind of models utilize the 3D convolutional networks for recommendation, which defines the recommendation problem as [\[51\]](#page-14-50), [\[246\]](#page-18-36): (S u t−L, ...., S<sup>u</sup> t−2 , S<sup>u</sup> t−1 ) → S u t , where S u <sup>t</sup> ⊆ V is the t-th time sequential behavior of user u at time t, and L denotes the maximum sequence length. Convolutional Sequence Embedding Recommendation (Caser) is a representative work that incorporates CNNs to learn the sequential patterns. It captures both user's general preferences and sequential patterns, at both the union level and point level with convolution operations, and captures the skip behavior [\[51\]](#page-14-50), [\[246\]](#page-18-36).

Besides, researchers proposed to leverage the advances of GNN based models for recommendation [\[247\]](#page-18-37), [\[248\]](#page-18-38), [\[249\]](#page-18-39). The graph structure is constructed from all sessions to form a global item correlation graph or graphs at each time period. For example, researchers constructed timeaware hypergraphs to model item correlations over time. After that, the self attention modules are used to model users' dynamic interests based on the learned dynamic item embeddings over time [\[247\]](#page-18-37).

**Summary:**Temporal/sequential based models focus on the dynamic preferences of users over times. Therefore, most existing work concentrates on the sequential information of users and items, and leverages sequential models (e.g., RNN, Memory Network) to capture the trends of user preference evolution. The main challenges lie in the recognition of long-term and short-term temporal interests, as well as the identification of global and local interests in the absence of user ID information. Since GNNs are skilled at processing user-item interactions at different granularities, we can observe that it receives more and more attention in temporal/sequential based models.

# <span id="page-12-0"></span>5 DISCUSSION AND FUTURE DIRECTIONS

The foregoing various neural network based recommendation models have demonstrated the superior recommendation quality. However, we realize that current solutions for recommendation are far from satisfactory, and there are still many opportunities in this area. Therefore, we outline some possible directions that deserve more research efforts from the basis, modeling, and evaluation perspectives. Last but not least, we present a discussion about the reproducibility of recommendation models.
*Basis: Recommendation Benchmarking.*While the field of neural recommender systems has seen a great surge of interests in recent years, it has also been difficult for researchers to keep track of what represents the state-of-the-art models. It is urgent to identify the architectures and key mechanisms that generalize to most recommender models. However, this is a non-trivial task as recommendation scenarios are diverse, e.g., static recommendation models or dynamic recommendation models, content enriched or knowledge enhanced models. Different recommendation models rely on different data sets with varying inputs. Besides, the same model would have varying performance on different recommendation scenarios due to the assumption in the modeling process. In fact, the Netflix competition for CF based recommendation has passed more than 10 years, how to design a large benchmarking recommendation dataset that keeps track of the state-of-the-art recommendation problems and update the leading performance for comparisons is a challenging yet urgent future direction.
*Models: Graph Reasoning*&*Self-supervised Learning.*Graphs are ubiquitous structures in representing various recommendation scenarios. For instance, CF could be seen as a user-item bipartite graph, content based recommendation is represented as an attributed user-item bipartite graph or a heterogeneous information network [\[151\]](#page-16-44), [\[258\]](#page-18-48), and knowledge enhanced recommendation is defined as a combination of knowledge graph and user-item bipartite graph. With the great success of deep learning on graphs [\[151\]](#page-16-44), it is promising to design graph based models for recommendation. Some recent studies have empirically demonstrated the superiority of graph embedding based recommendation models, how to explore the natural graph reasoning techniques for better recommendation is a promising direction. Besides, self-supervised learning [\[259\]](#page-18-49), [\[260\]](#page-18-50) is becoming emerged and showing promises in recommendation tasks [\[261\]](#page-18-51), [\[262\]](#page-19-0), [\[263\]](#page-19-1), [\[264\]](#page-19-2), [\[265\]](#page-19-3). Its core is to distill extra supervision signals from the limited available user interaction data via some auxiliary tasks and facilitate the downstream recommendation tasks. As such supervisions are complementary to the user-item interactions, they enhance the representation learning of users and items. Incorporating self-supervised learning into recommendation could offer promising solutions to the long-standing issues of data sparsity and long-tail distribution.
*Evaluation: Multi-Objective Goals for Social Good Recommendation.*Recommender systems have penetrated every aspect in our daily life, and have greatly shaped the decision process of providers and users. Most previous recommender systems concentrated on the single goal of recommendation accuracy based user experience. These systems limit the ability to incorporate user satisfaction from multiple goals, e.g., recommendation diversity and explanations to persuade users [\[9\]](#page-14-8). Besides, the user-centric approach neglects system objectives from multistakeholders and the society. The data-driven approaches with accuracy as goals may lead to biases in the algorithmic process decision process [\[266\]](#page-19-4), [\[267\]](#page-19-5), [\[268\]](#page-19-6), [\[269\]](#page-19-7). For recommender systems, researchers have realized that long tailed items have fewer chances to be recommended, and benefiting users may obscure concerns that might come from other stakeholders in this system. How to provide multi-objective goals for social good recommendation, such as explainability, balance of multistakeholders, and fairness for the society is an important research topic that needs to be paid attention to.
*Discussion: Reproducibility.*While the neural recommendation models have dominated in the recommendation field and claimed substantial improvements over previous models, recent efforts raise questions about their reproducibility and published claims [\[270\]](#page-19-8), [\[271\]](#page-19-9), [\[272\]](#page-19-10), [\[273\]](#page-19-11), [\[274\]](#page-19-12). This can be attributed to two aspects. First, neural recommendation models are based on neural networks, which are hard to tune in practice. Thus, we should carefully choose the initialization, tune hyperparameters, avoid model collapse, and so on. Besides, due to the various application scenarios of recommendation, different models vary in the selection of datasets and setting of experiments. Specifically, it is well known that recommender models are sensitive to the dataset size, the dataset sparsity, the data preprocessing and splitting techniques, the strategy of negative sampling, the choice of loss function and optimization manner, and the evaluation metrics of performance. Thus, it is very challenging to conduct a fair performance comparison. In order to advance the recommendation community, some researchers make efforts on the data level, such as industryrelevant recommendation benchmark [\[275\]](#page-19-13), MIcrosoft News Dataset (MIND) [\[276\]](#page-19-14), and Yelp dataset[2](#page-13-0) . Others concentrate on the unified evaluation framework [\[277\]](#page-19-15), [\[278\]](#page-19-16). For example, researchers argue that previously default choice of evaluating recommender models with sampled metrics (e.g., rather than using the full set, only sampling a small set of negative items during testing) would be inconsistent to the true trend [\[279\]](#page-19-17). Towards fair and reproducible comparisons, it is of crucial importance to make the experimental settings transparent (e.g., release the codes, datasets, and experimental settings, and set up a leaderboard if possible). Furthermore, beyond network architecture engineering and hunting for the "best" performance, research studies on theoretical considerations and reproducibility analysis should be encouraged.

# 6 CONCLUSION

In this survey, we provide a systematic review on neural recommender models from the perspective of recommendation modeling with accuracy goal. Based on the data usage, we organize existing work into three categories:*collaborative filtering model*, *content enriched model*, and *temporal/sequential model*. In each part, we summarize a bunch of influential research work and conclude corresponding main contributions as well as our opinions. Moreover, we also elaborate possible promising directions from the basics, modeling, and evaluation perspectives, and reproducibility problem in recommender systems. Still, a large number of novel methods and techniques are proposed each year. We hope

<span id="page-13-0"></span>2. <https://www.yelp.com/dataset>

this survey is able to help reader to quickly understand the development and key aspects of recommendation modeling, and inspires some future studies.

# REFERENCES

- <span id="page-14-0"></span>[1] D. Goldberg, D. Nichols, B. M. Oki, and D. Terry, "Using collaborative filtering to weave an information tapestry," *Commun. ACM*, vol. 35, no. 12, pp. 61–70, 1992.
- <span id="page-14-1"></span>[2] G. Adomavicius and A. Tuzhilin, "Toward the next generation of recommender systems: A survey of the state-of-the-art and possible extensions," *IEEE TKDE*, vol. 17, no. 6, pp. 734–749, 2005.
- <span id="page-14-2"></span>[3] Y. Koren, R. Bell, and C. Volinsky, "Matrix factorization techniques for recommender systems," *Computer*, no. 8, pp. 30–37, 2009.
- <span id="page-14-3"></span>[4] A. Karatzoglou, X. Amatriain, L. Baltrunas, and N. Oliver, "Multiverse recommendation: n-dimensional tensor factorization for context-aware collaborative filtering," in *RecSys*, 2010, pp. 79–86.
- <span id="page-14-4"></span>[5] S. Rendle, C. Freudenthaler, and L. Schmidt-Thieme, "Factorizing personalized markov chains for next-basket recommendation," in *WWW*, 2010, pp. 811–820.
- <span id="page-14-5"></span>[6] I. Goodfellow, Y. Bengio, A. Courville, and Y. Bengio, *Deep learning*. MIT press Cambridge, 2016, vol. 1, no. 2.
- <span id="page-14-6"></span>[7] Y. Shi, M. Larson, and A. Hanjalic, "Collaborative filtering beyond the user-item matrix: A survey of the state of the art and future challenges," *ACM CSUR*, vol. 47, no. 1, pp. 1–45, 2014.
- <span id="page-14-7"></span>[8] M. M. Khan, R. Ibrahim, and I. Ghani, "Cross domain recommender systems: A systematic literature review," *ACM CSUR*, vol. 50, no. 3, pp. 1–34, 2017.
- <span id="page-14-8"></span>[9] Y. Zhang and X. Chen, "Explainable recommendation: A survey and new perspectives," *TRIR*, vol. 14, no. 1, pp. 1–101, 2020.
- <span id="page-14-9"></span>[10] S. Wang, L. Hu, Y. Wang, X. He, Q. Z. Sheng, M. A. Orgun, L. Cao, F. Ricci, and P. S. Yu, "Graph learning based recommender systems: A review," in *IJCAI*, 2021, pp. 4644–4652.
- <span id="page-14-10"></span>[11] X. Wang, X. He, F. Feng, L. Nie, and T.-S. Chua, "Tem: Treeenhanced embedding model for explainable recommendation," in *WWW*, 2018, pp. 1543–1552.
- <span id="page-14-11"></span>[12] Q. Guo, F. Zhuang, C. Qin, H. Zhu, X. Xie, H. Xiong, and Q. He, "A survey on knowledge graph-based recommender systems," *IEEE TKDE*, 2020, preprint.
- <span id="page-14-12"></span>[13] H. Fang, D. Zhang, Y. Shu, and G. Guo, "Deep learning for sequential recommendation: Algorithms, influential factors, and evaluations," *ACM Trans. Inf. Syst.*, vol. 39, no. 1, pp. 10:1–10:42, 2020.
- <span id="page-14-13"></span>[14] M. Quadrana, P. Cremonesi, and D. Jannach, "Sequence-aware recommender systems," *ACM CSUR*, vol. 51, no. 4, pp. 66:1– 66:36, 2018.
- <span id="page-14-14"></span>[15] S. Wang, L. Cao, Y. Wang, Q. Z. Sheng, M. A. Orgun, and D. Lian, "A survey on session-based recommender systems," *ACM CSUR*, vol. 54, no. 7, pp. 1–38, 2021.
- <span id="page-14-15"></span>[16] S. Zhang, L. Yao, A. Sun, and Y. Tay, "Deep learning based recommender system: A survey and new perspectives," *ACM CSUR*, vol. 52, no. 1, pp. 5:1–5:38, 2019.
- <span id="page-14-16"></span>[17] Z. Batmaz, A. Yurekli, A. Bilge, and C. Kaleli, "A review on deep learning for recommender systems: challenges and remedies," *Artif. Intell. Rev.*, vol. 52, no. 1, pp. 1–37, 2019.
- <span id="page-14-17"></span>[18] A. Da'u and N. Salim, "Recommendation system based on deep learning methods: a systematic review and new directions," *Artif. Intell. Rev.*, vol. 53, no. 4, pp. 2709–2748, 2020.
- <span id="page-14-18"></span>[19] S. Rendle, C. Freudenthaler, Z. Gantner, and L. Schmidt-Thieme, "Bpr: Bayesian personalized ranking from implicit feedback," in *UAI*, 2009, pp. 452–461.
- <span id="page-14-19"></span>[20] S. Kabbur, X. Ning, and G. Karypis, "FISM: factored item similarity models for top-n recommender systems," in *SIGKDD*, 2013, pp. 659–667.
- <span id="page-14-29"></span>[21] C. Ma, L. Ma, Y. Zhang, R. Tang, X. Liu, and M. Coates, "Probabilistic metric learning with adaptive margin for top-k recommendation," in *SIGKDD*, 2020, pp. 1036–1044.
- <span id="page-14-30"></span>[22] D. Lian, X. Xie, E. Chen, and H. Xiong, "Product quantized collaborative filtering," *IEEE TKDE*, 2020, preprint.
- <span id="page-14-31"></span>[23] J. Chen, C. Wang, S. Zhou, Q. Shi, J. Chen, Y. Feng, and C. Chen, "Fast adaptively weighted matrix factorization for recommendation with implicit feedback," in *AAAI*, 2020, pp. 3470–3477.
- <span id="page-14-20"></span>[24] Y. Koren, "Factorization meets the neighborhood: a multifaceted collaborative filtering model," in *SIGKDD*, 2008, pp. 426–434.

- <span id="page-14-21"></span>[25] X. He, Z. He, J. Song, Z. Liu, Y.-G. Jiang, and T.-S. Chua, "Nais: Neural attentive item similarity model for recommendation," *IEEE TKDE*, vol. 30, no. 12, pp. 2354–2366, 2018.
- <span id="page-14-22"></span>[26] J. Chen, H. Zhang, X. He, L. Nie, W. Liu, and T.-S. Chua, "Attentive collaborative filtering: Multimedia recommendation with item- and component-level attention," in *SIGIR*, 2017, pp. 335–344.
- <span id="page-14-25"></span>[27] S. Sedhain, A. K. Menon, S. Sanner, and L. Xie, "Autorec: Autoencoders meet collaborative filtering," in *WWW*, 2015, pp. 111–112.
- <span id="page-14-26"></span>[28] Y. Wu, C. DuBois, A. X. Zheng, and M. Ester, "Collaborative denoising auto-encoders for top-n recommender systems," in *WSDM*, 2016, pp. 153–162.
- <span id="page-14-27"></span>[29] D. Liang, R. G. Krishnan, M. D. Hoffman, and T. Jebara, "Variational autoencoders for collaborative filtering," in *WWW*, 2018, pp. 689–698.
- <span id="page-14-28"></span>[30] F. Zhuang, D. Luo, N. J. Yuan, X. Xie, and Q. He, "Representation learning with pair-wise constraints for collaborative ranking," in *WSDM*, 2017, pp. 567–575.
- <span id="page-14-32"></span>[31] K. Luo, H. Yang, G. Wu, and S. Sanner, "Deep critiquing for vaebased recommender systems," in *SIGIR*, 2020, pp. 1269–1278.
- <span id="page-14-33"></span>[32] F. Khawar, L. Poon, and N. L. Zhang, "Learning the structure of auto-encoding recommenders," in *WWW*, 2020, pp. 519–529.
- <span id="page-14-34"></span>[33] R. van den Berg, T. Kipf, and M. Welling, "Graph convolutional matrix completion," in *KDD DL Workshop*, 2018.
- <span id="page-14-35"></span>[34] X. Wang, X. He, M. Wang, F. Feng, and T.-S. Chua, "Neural graph collaborative filtering," in *SIGIR*, 2019, pp. 165–174.
- <span id="page-14-36"></span>[35] L. Zheng, C. Lu, F. Jiang, J. Zhang, and P. S. Yu, "Spectral collaborative filtering," in *RecSys*, 2018, pp. 311–319.
- <span id="page-14-37"></span>[36] J. Sun, Y. Zhang, W. Guo, H. Guo, R. Tang, X. He, C. Ma, and M. Coates, "Neighbor interaction aware graph convolution networks for recommendation," in *SIGIR*, 2020, pp. 1289–1298.
- <span id="page-14-38"></span>[37] J. Sun, W. Guo, D. Zhang, Y. Zhang, F. Regol, Y. Hu, H. Guo, R. Tang, H. Yuan, X. He *et al.*, "A framework for recommending accurate and diverse items using bayesian graph convolutional neural networks," in *SIGKDD*, 2020, pp. 2030–2039.
- <span id="page-14-39"></span>[38] X. Wang, H. Jin, A. Zhang, X. He, T. Xu, and T.-S. Chua, "Disentangled graph collaborative filtering," in *SIGIR*, 2020, pp. 1001– 1010.
- <span id="page-14-40"></span>[39] L. Chen, L. Wu, R. Hong, K. Zhang, and M. Wang, "Revisiting graph based collaborative filtering: A linear residual graph convolutional network approach," in *AAAI*, 2020, pp. 27–34.
- <span id="page-14-41"></span>[40] X. He, K. Deng, X. Wang, Y. Li, Y. Zhang, and M. Wang, "Lightgcn: Simplifying and powering graph convolution network for recommendation," in *SIGIR*, 2020, pp. 639–648.
- <span id="page-14-42"></span>[41] S. Ji, Y. Feng, R. Ji, X. Zhao, W. Tang, and Y. Gao, "Dual channel hypergraph collaborative filtering," in *SIGKDD*, 2020, pp. 2020– 2029.
- <span id="page-14-23"></span>[42] F. Xue, X. He, X. Wang, J. Xu, K. Liu, and R. Hong, "Deep itembased collaborative filtering for top-n recommendation," *ACM TOIS*, vol. 37, no. 3, pp. 1–25, 2019.
- <span id="page-14-24"></span>[43] G. Zhou, X. Zhu, C. Song, Y. Fan, H. Zhu, X. Ma, Y. Yan, J. Jin, H. Li, and K. Gai, "Deep interest network for click-through rate prediction," in *SIGKDD*, 2018, pp. 1059–1068.
- <span id="page-14-43"></span>[44] T. N. Kipf and M. Welling, "Semi-supervised classification with graph convolutional networks," in *ICLR*, 2017.
- <span id="page-14-44"></span>[45] C.-K. Hsieh, L. Yang, Y. Cui, T.-Y. Lin, S. Belongie, and D. Estrin, "Collaborative metric learning," in *WWW*, 2017, pp. 193–201.
- <span id="page-14-46"></span>[46] R. He, W.-C. Kang, and J. McAuley, "Translation-based recommendation," in *RecSys*, 2017, pp. 161–169.
- <span id="page-14-47"></span>[47] Y. Tay, L. Anh Tuan, and S. C. Hui, "Latent relational metric learning via memory-based attention for collaborative ranking," in *WWW*, 2018, pp. 729–739.
- <span id="page-14-48"></span>[48] L. V. Tran, Y. Tay, S. Zhang, G. Cong, and X. Li, "Hyperml: A boosting metric learning approach in hyperbolic space for recommender systems," in *WSDM*, 2020, pp. 609–617.
- <span id="page-14-45"></span>[49] X. He, L. Liao, H. Zhang, L. Nie, X. Hu, and T.-S. Chua, "Neural collaborative filtering," in *WWW*, 2017, pp. 173–182.
- <span id="page-14-49"></span>[50] X. He, X. Du, X. Wang, F. Tian, J. Tang, and T. Chua, "Outer product-based neural collaborative filtering," in *IJCAI*, 2018, pp. 2227–2233.
- <span id="page-14-50"></span>[51] J. Tang and K. Wang, "Personalized top-n sequential recommendation via convolutional sequence embedding," in *WSDM*, 2018, pp. 565–573.
- <span id="page-14-51"></span>[52] F. Strub and J. Mary, "Collaborative filtering with stacked denoising autoencoders and sparse inputs," in *NeurIPS workshop*, 2015.

- <span id="page-15-0"></span>[53] S. Zhang, L. Yao, and X. Xu, "Autosvd++: An efficient hybrid collaborative filtering model via contractive auto-encoders," in *SIGIR*, 2017, pp. 957–960.
- <span id="page-15-1"></span>[54] F. Zhuang, Z. Zhang, M. Qian, C. Shi, X. Xie, and Q. He, "Representation learning via dual-autoencoder for recommendation," *NN*, vol. 90, pp. 83–89, 2017.
- <span id="page-15-2"></span>[55] S. Rendle, "Factorization machines," in *ICDM*, 2010, pp. 995– 1000.
- <span id="page-15-3"></span>[56] Y. Juan, Y. Zhuang, W.-S. Chin, and C.-J. Lin, "Field-aware factorization machines for ctr prediction," in *RecSys*, 2016, pp. 43–50.
- <span id="page-15-4"></span>[57] X. He and T.-S. Chua, "Neural factorization machines for sparse predictive analytics," in *SIGIR*, 2017, pp. 355–364.
- <span id="page-15-5"></span>[58] W. Zhang, T. Du, and J. Wang, "Deep learning over multi-field categorical data," in *ECIR*, 2016, pp. 45–57.
- <span id="page-15-6"></span>[59] Y. Qu, H. Cai, K. Ren, W. Zhang, Y. Yu, Y. Wen, and J. Wang, "Product-based neural networks for user response prediction," in *ICDM*, 2016, pp. 1149–1154.
- <span id="page-15-7"></span>[60] Y. Shan, T. R. Hoens, J. Jiao, H. Wang, D. Yu, and J. Mao, "Deep crossing: Web-scale modeling without manually crafted combinatorial features," in *SIGKDD*, 2016, pp. 255–262.
- <span id="page-15-8"></span>[61] P. Covington, J. Adams, and E. Sargin, "Deep neural networks for youtube recommendations," in *RecSys*, 2016, pp. 191–198.
- <span id="page-15-9"></span>[62] H.-T. Cheng, L. Koc, J. Harmsen, T. Shaked, T. Chandra, H. Aradhye, G. Anderson, G. Corrado, W. Chai, M. Ispir *et al.*, "Wide & deep learning for recommender systems," in *DLRS*, 2016, pp. 7–10.
- <span id="page-15-10"></span>[63] H. Guo, R. Tang, Y. Ye, Z. Li, and X. He, "Deepfm: A factorizationmachine based neural network for CTR prediction," in *IJCAI*, 2017, pp. 1725–1731.
- <span id="page-15-11"></span>[64] R. Wang, B. Fu, G. Fu, and M. Wang, "Deep & cross network for ad click predictions," in *ADKDD*, 2017, pp. 1–7.
- <span id="page-15-12"></span>[65] J. Lian, X. Zhou, F. Zhang, Z. Chen, X. Xie, and G. Sun, "xdeepfm: Combining explicit and implicit feature interactions for recommender systems," in *SIGKDD*, 2018, pp. 1754–1763.
- <span id="page-15-13"></span>[66] M. Blondel, A. Fujino, N. Ueda, and M. Ishihata, "Higher-order factorization machines," in *NeurIPS*, 2016, pp. 3351–3359.
- <span id="page-15-14"></span>[67] D. W. Otter, J. R. Medina, and J. K. Kalita, "A survey of the usages of deep learning for natural language processing," *IEEE TNNLS*, 2020, preprint.
- <span id="page-15-15"></span>[68] S. Lappin, *Deep Learning and Linguistic Representation*. CRC Press, 2021.
- <span id="page-15-16"></span>[69] L. Zheng, V. Noroozi, and P. S. Yu, "Joint deep modeling of users and items using reviews for recommendation," in *WSDM*, 2017, pp. 425–434.
- <span id="page-15-17"></span>[70] P. Sun, L. Wu, K. Zhang, Y. Fu, R. Hong, and M. Wang, "Dual learning for explainable recommendation: Towards unifying user preference prediction and review generation," in *WWW*, 2020, pp. 837–847.
- <span id="page-15-18"></span>[71] H. Wang, N. Wang, and D.-Y. Yeung, "Collaborative deep learning for recommender systems," in *SIGKDD*, 2015, pp. 1235–1244.
- <span id="page-15-19"></span>[72] H. Wang, S. Xingjian, and D.-Y. Yeung, "Collaborative recurrent autoencoder: Recommend while learning to fill in the blanks," in *NeurIPS*, 2016, pp. 415–423.
- <span id="page-15-20"></span>[73] X. Dong, L. Yu, Z. Wu, Y. Sun, L. Yuan, and F. Zhang, "A hybrid collaborative filtering model with deep structure for recommender systems." in *AAAI*, 2017, pp. 1309–1315.
- <span id="page-15-21"></span>[74] X. Li and J. She, "Collaborative variational autoencoder for recommender systems," in *SIGKDD*, 2017, pp. 305–314.
- <span id="page-15-22"></span>[75] H. Ying, L. Chen, Y. Xiong, and J. Wu, "Collaborative deep ranking: A hybrid pair-wise recommendation algorithm with implicit feedback," in *PAKDD*, 2016, pp. 555–567.
- <span id="page-15-23"></span>[76] J. Wei, J. He, K. Chen, Y. Zhou, and Z. Tang, "Collaborative filtering and deep learning based recommendation system for cold start items," *ESWA*, vol. 69, pp. 29–39, 2017.
- <span id="page-15-24"></span>[77] Z. Xu, T. Lukasiewicz, C. Chen, Y. Miao, and X. Meng, "Tag-aware personalized recommendation using a hybrid deep model," in *IJCAI*, 2017, pp. 3196–3202.
- <span id="page-15-25"></span>[78] F. Strub, R. Gaudel, and J. Mary, "Hybrid recommender system based on autoencoders," in *DLRS*, 2016, pp. 11–16.
- <span id="page-15-26"></span>[79] C. Ma, P. Kang, B. Wu, Q. Wang, and X. Liu, "Gated attentiveautoencoder for content-aware recommendation," in *WSDM*, 2019, pp. 519–527.
- <span id="page-15-27"></span>[80] S. Okura, Y. Tagami, S. Ono, and A. Tajima, "Embedding-based news recommendation for millions of users," in *SIGKDD*, 2017, pp. 1933–1942.

- <span id="page-15-28"></span>[81] W. Fu, Z. Peng, S. Wang, Y. Xu, and J. Li, "Deeply fusing reviews and contents for cold start users in cross-domain recommendation systems," in *AAAI*, 2019, pp. 94–101.
- <span id="page-15-29"></span>[82] D. Kim, C. Park, J. Oh, S. Lee, and H. Yu, "Convolutional matrix factorization for document context-aware recommendation," in *RecSys*, 2016, pp. 233–240.
- <span id="page-15-30"></span>[83] R. Catherine and W. Cohen, "Transnets: Learning to transform for recommendation," in *RecSys*, 2017, pp. 288–296.
- <span id="page-15-31"></span>[84] T. Ebesu and Y. Fang, "Neural citation network for context-aware citation recommendation," in *SIGIR*, 2017, pp. 1093–1096.
- <span id="page-15-32"></span>[85] H. Lee, Y. Ahn, H. Lee, S. Ha, and S.-g. Lee, "Quote recommendation in dialogue using deep neural network," in *SIGIR*, 2016, pp. 957–960.
- <span id="page-15-33"></span>[86] C.-Y. Wu, A. Ahmed, A. Beutel, and A. J. Smola, "Joint training of ratings and reviews with recurrent recommender networks," in *ICLR Workshop*, 2017.
- <span id="page-15-34"></span>[87] S. Fan, J. Zhu, X. Han, C. Shi, L. Hu, B. Ma, and Y. Li, "Metapathguided heterogeneous graph neural network for intent recommendation," in *SIGKDD*, 2019, pp. 2478–2486.
- <span id="page-15-35"></span>[88] D. Liu, J. Lian, S. Wang, Y. Qiao, J.-H. Chen, G. Sun, and X. Xie, "Kred: Knowledge-aware document representation for news recommendations," in *RecSys*, 2020, pp. 200–209.
- <span id="page-15-36"></span>[89] Y. Kim, "Convolutional neural networks for sentence classification," in *EMNLP*, 2014, pp. 1746–1751.
- <span id="page-15-37"></span>[90] T. Bansal, D. Belanger, and A. McCallum, "Ask the gru: Multitask learning for deep text recommendations," in *RecSys*, 2016, pp. 107–114.
- <span id="page-15-38"></span>[91] Y. Gong and Q. Zhang, "Hashtag recommendation using attention-based convolutional neural network," in *IJCAI*, 2016, pp. 2782–2788.
- <span id="page-15-39"></span>[92] S. Seo, J. Huang, H. Yang, and Y. Liu, "Interpretable convolutional neural networks with dual local and global attention for review rating prediction," in *RecSys*, 2017, pp. 297–305.
- <span id="page-15-40"></span>[93] Y. Li, T. Liu, J. Jiang, and L. Zhang, "Hashtag recommendation with topical attention-based LSTM," in *COLING*, 2016, pp. 3019– 3029.
- <span id="page-15-41"></span>[94] C. Qin, H. Zhu, C. Zhu, T. Xu, F. Zhuang, C. Ma, J. Zhang, and H. Xiong, "Duerquiz: A personalized question recommender system for intelligent job interview," in *SIGKDD*, 2019, pp. 2165– 2173.
- <span id="page-15-42"></span>[95] H. Wang, F. Wu, Z. Liu, and X. Xie, "Fine-grained interest matching for neural news recommendation," in *ACL*, 2020, pp. 836–845.
- <span id="page-15-43"></span>[96] T. Qi, F. Wu, C. Wu, Y. Huang, and X. Xie, "Privacy-preserving news recommendation model learning," in *EMNLP*, 2020, pp. 1423–1432.
- <span id="page-15-44"></span>[97] D. Lee, B. Oh, S. Seo, and K.-H. Lee, "News recommendation with topic-enriched knowledge graphs," in *CIKM*, 2020, pp. 695– 704.
- <span id="page-15-45"></span>[98] Z. Cheng, Y. Ding, X. He, L. Zhu, X. Song, and M. S. Kankanhalli, "Aˆ3ncf: An adaptive aspect attention model for rating prediction," in *IJCAI*, 2018, pp. 3748–3754.
- <span id="page-15-46"></span>[99] Q. Zhu, X. Zhou, Z. Song, J. Tan, and L. Guo, "Dan: Deep attention neural network for news recommendation," in *AAAI*, 2019, pp. 5973–5980.
- <span id="page-15-47"></span>[100] X. Chen, Y. Zhang, and Z. Qin, "Dynamic explainable recommendation based on neural attentive models," in *AAAI*, 2019, pp. 53–60.
- <span id="page-15-48"></span>[101] C. Wu, F. Wu, M. An, J. Huang, Y. Huang, and X. Xie, "Npa: Neural news recommendation with personalized attention," in *SIGKDD*, 2019, pp. 2576–2584.
- <span id="page-15-49"></span>[102] Y. Lu, R. Dong, and B. Smyth, "Coevolutionary recommendation model: Mutual learning between ratings and reviews," in *WWW*, 2018, pp. 773–782.
- <span id="page-15-50"></span>[103] D. Liu, J. Li, B. Du, J. Chang, and R. Gao, "Daml: Dual attention mutual learning between ratings and reviews for item recommendation," in *SIGKDD*, 2019, pp. 344–352.
- <span id="page-15-51"></span>[104] L. Hu, S. Jian, L. Cao, and Q. Chen, "Interpretable recommendation via attraction modeling: Learning multilevel attractiveness over multimodal movie contents." in *IJCAI*, 2018, pp. 3400–3406.
- <span id="page-15-52"></span>[105] C. Wu, F. Wu, M. An, J. Huang, Y. Huang, and X. Xie, "Neural news recommendation with attentive multi-view learning," in *IJCAI*, 2019, pp. 3863–3869.
- <span id="page-15-53"></span>[106] J. Gao, Y. Lin, Y. Wang, X. Wang, Z. Yang, Y. He, and X. Chu, "Set-sequence-graph: A multi-view approach towards exploiting reviews for recommendation," in *CIKM*, 2020, pp. 395–404.

- <span id="page-16-0"></span>[107] R. Ma, Q. Zhang, J. Wang, L. Cui, and X. Huang, "Mention recommendation for multimodal microblog with cross-attention memory network," in *SIGIR*, 2018, pp. 195–204.
- <span id="page-16-1"></span>[108] Q. Zhang, J. Wang, H. Huang, X. Huang, and Y. Gong, "Hashtag recommendation for multimodal microblog using co-attention network," in *IJCAI*, 2017, pp. 3420–3426.
- <span id="page-16-2"></span>[109] C. Chen, M. Zhang, Y. Liu, and S. Ma, "Neural attentional rating regression with review-level explanations," in *WWW*, 2018, pp. 1583–1592.
- <span id="page-16-3"></span>[110] X. Wang, Y. Chen, J. Yang, L. Wu, Z. Wu, and X. Xie, "A reinforcement learning framework for explainable recommendation," in *ICDM*, 2018, pp. 587–596.
- <span id="page-16-4"></span>[111] D. Bahdanau, K. Cho, and Y. Bengio, "Neural machine translation by jointly learning to align and translate," in *ICLR*, 2015.
- <span id="page-16-5"></span>[112] P. Li, Z. Wang, Z. Ren, L. Bing, and W. Lam, "Neural rating regression with abstractive tips generation for recommendation," in *SIGIR*, 2017, pp. 345–354.
- <span id="page-16-6"></span>[113] P. Li, Z. Wang, L. Bing, and W. Lam, "Persona-aware tips generation," in *WWW*, 2019, pp. 1006–1016.
- <span id="page-16-7"></span>[114] Z. Chen, X. Wang, X. Xie, T. Wu, G. Bu, Y. Wang, and E. Chen, "Co-attentive multi-task learning for explainable recommendation," in *IJCAI*, 2019, pp. 2137–2143.
- <span id="page-16-8"></span>[115] L. Li, Y. Zhang, and L. Chen, "Generate neural template explanations for recommendation," in *CIKM*, 2020, pp. 755–764.
- <span id="page-16-9"></span>[116] Z. Chen, X. Wang, X. Xie, M. Parsana, A. Soni, X. Ao, and E. Chen, "Towards explainable conversational recommendation," in *IJCAI*, 2020, pp. 2994–3000.
- <span id="page-16-10"></span>[117] X. Chen, H. Chen, H. Xu, Y. Zhang, Y. Cao, Z. Qin, and H. Zha, "Personalized fashion recommendation with visual explanations based on multimodal attention network: Towards visually explainable recommendation," in *SIGIR*, 2019, pp. 765–774.
- <span id="page-16-11"></span>[118] Q.-T. Truong and H. Lauw, "Multimodal review generation for recommender systems," in *WWW*, 2019, pp. 1864–1874.
- <span id="page-16-20"></span>[119] R. He and J. McAuley, "VBPR: visual bayesian personalized ranking from implicit feedback," in *AAAI*, 2016, pp. 144–150.
- <span id="page-16-29"></span>[120] Y. Lin, M. Moosaei, and H. Yang, "Outfitnet: Fashion outfit recommendation with attention-based multiple instance learning," in *WWW*, 2020, pp. 77–87.
- <span id="page-16-21"></span>[121] W. Yu, H. Zhang, X. He, X. Chen, L. Xiong, and Z. Qin, "Aesthetic-based clothing recommendation," in *WWW*, 2018, pp. 649–658.
- <span id="page-16-12"></span>[122] J. Wen, X. Li, J. She, S. Park, and M. Cheung, "Visual background recommendation for dance performances using dancer-shared images," in *iThings*, 2016, pp. 521–527.
- <span id="page-16-13"></span>[123] M. Hou, L. Wu, E. Chen, Z. Li, Z. Vincent W., and Q. Liu, "Explainable fashion recommendation: A semantic attribute region guided approach," in *IJCAI*, 2019, pp. 4681–4688.
- <span id="page-16-14"></span>[124] T. Alashkar, S. Jiang, S. Wang, and Y. Fu, "Examples-rules guided deep neural network for makeup recommendation." in *AAAI*, 2017, pp. 941–947.
- <span id="page-16-27"></span>[125] X. Yang, X. He, X. Wang, Y. Ma, F. Feng, M. Wang, and T.-S. Chua, "Interpretable fashion matching with rich attributes," in *SIGIR*, 2019, pp. 775–784.
- <span id="page-16-30"></span>[126] S. Liu, Z. Chen, H. Liu, and X. Hu, "User-video co-attention network for personalized micro-video recommendation," in *WWW*, 2019, pp. 3020–3026.
- <span id="page-16-31"></span>[127] R. Ying, R. He, K. Chen, P. Eksombatchai, W. L. Hamilton, and J. Leskovec, "Graph convolutional neural networks for web-scale recommender systems," in *SIGKDD*, 2018, pp. 974–983.
- <span id="page-16-32"></span>[128] X. Li, X. Wang, X. He, L. Chen, J. Xiao, and T.-S. Chua, "Hierarchical fashion graph network for personalized outfit recommendation," in *SIGIR*, 2020, pp. 159–168.
- <span id="page-16-33"></span>[129] L. Wu, Y. Yang, L. Chen, D. Lian, R. Hong, and M. Wang, "Learning to transfer graph embeddings for inductive graph based recommendation," in *SIGIR*, 2020, pp. 1211–1220.
- <span id="page-16-22"></span>[130] R. He and J. McAuley, "Ups and downs: Modeling the visual evolution of fashion trends with one-class collaborative filtering," in *WWW*, 2016, pp. 507–517.
- <span id="page-16-15"></span>[131] Q. Xu, F. Shen, L. Liu, and H. T. Shen, "Graphcar: Content-aware multimedia recommendation with graph autoencoder," in *SIGIR*, 2018, pp. 981–984.
- <span id="page-16-34"></span>[132] F. Zhang, N. J. Yuan, D. Lian, X. Xie, and W.-Y. Ma, "Collaborative knowledge base embedding for recommender systems," in *SIGKDD*, 2016, pp. 353–362.
- <span id="page-16-26"></span>[133] X. Yang, Y. Ma, L. Liao, M. Wang, and T.-S. Chua, "Transnfcm: Translation-based neural fashion compatibility modeling," in *AAAI*, 2019, pp. 403–410.

- <span id="page-16-23"></span>[134] Â. Cardoso, F. Daolio, and S. Vargas, "Product characterisation towards personalisation: Learning attributes from unstructured data to recommend fashion products," in *SIGKDD*, 2018, pp. 80– 89.
- <span id="page-16-35"></span>[135] X. Chen, Y. Zhang, Q. Ai, H. Xu, J. Yan, and Z. Qin, "Personalized key frame recommendation," in *SIGIR*, 2017, pp. 315–324.
- <span id="page-16-36"></span>[136] T. Yu, Y. Shen, and H. Jin, "Towards hands-free visual dialog interactive recommendation," in *AAAI*, 2020, pp. 1137–1144.
- <span id="page-16-37"></span>[137] X. Wang and Y. Wang, "Improving content-based and hybrid music recommendation using deep learning," in *MM*, 2014, pp. 627–636.
- <span id="page-16-38"></span>[138] A. v. d. Oord, S. Dieleman, and B. Schrauwen, "Deep contentbased music recommendation," in *NeurIPS*, 2013, pp. 2643–2651.
- <span id="page-16-39"></span>[139] Z. Nazari, C. Charbuillet, J. Pages, M. Laurent, D. Charrier, B. Vecchione, and B. Carterette, "Recommending podcasts for cold-start users based on music listening and taste," in *SIGIR*, 2020, pp. 1041–1050.
- <span id="page-16-28"></span>[140] L. Wu, L. Chen, Y. Yang, R. Hong, Y. Ge, X. Xie, and M. Wang, "Personalized multimedia item and key frame recommendation," in *IJCAI*, 2019, pp. 1431–1437.
- <span id="page-16-40"></span>[141] L. Wu, Y. Yang, K. Zhang, R. Hong, Y. Fu, and M. Wang, "Joint item recommendation and attribute inference: An adaptive graph convolutional network approach," in *SIGIR*, 2020, pp. 679–688.
- <span id="page-16-41"></span>[142] J. Lee, S. Abu-El-Haija, B. Varadarajan, and A. Natsev, "Collaborative deep metric learning for video understanding," in *SIGKDD*, 2018, pp. 481–490.
- <span id="page-16-42"></span>[143] J. Lee and S. Abu-El-Haija, "Large-scale content-only video recommendation," in *ICCVW*, 2017, pp. 987–995.
- <span id="page-16-16"></span>[144] J. McAuley, C. Targett, Q. Shi, and A. Van Den Hengel, "Imagebased recommendations on styles and substitutes," in *SIGIR*, 2015, pp. 43–52.
- <span id="page-16-17"></span>[145] Y. S. Rawat and M. S. Kankanhalli, "Contagnet: Exploiting user context for image tag recommendation," in *MM*, 2016, pp. 1102– 1106.
- <span id="page-16-18"></span>[146] C. Lei, D. Liu, W. Li, Z.-J. Zha, and H. Li, "Comparative deep learning of hybrid representations for image recommendations," in *CVPR*, 2016, pp. 2545–2553.
- <span id="page-16-19"></span>[147] Q. Liu, S. Wu, and L. Wang, "Deepstyle: Learning user preferences for visual recommendation," in *SIGIR*, 2017, pp. 841–844.
- <span id="page-16-24"></span>[148] W. Niu, J. Caverlee, and H. Lu, "Neural personalized ranking for image recommendation," in *WSDM*, 2018, pp. 423–431.
- <span id="page-16-25"></span>[149] S. Wang, Y. Wang, J. Tang, K. Shu, S. Ranganath, and H. Liu, "What your images reveal: Exploiting visual contents for pointof-interest recommendation," in *WWW*, 2017, pp. 391–400.
- <span id="page-16-43"></span>[150] T. N. Kipf and M. Welling, "Semi-supervised classification with graph convolutional networks," in *ICLR*, 2017.
- <span id="page-16-44"></span>[151] Z. Zhang, P. Cui, and W. Zhu, "Deep learning on graphs: A survey," *IEEE TKDE*, 2020, preprint.
- <span id="page-16-45"></span>[152] L. Wu, P. Sun, R. Hong, Y. Ge, and M. Wang, "Collaborative neural social recommendation," *IEEE TSMC-S*, vol. 51, no. 1, pp. 464–476, 2021.
- <span id="page-16-46"></span>[153] P. Sun, L. Wu, and M. Wang, "Attentive recurrent social recommendation," in *SIGIR*, 2018, pp. 185–194.
- <span id="page-16-47"></span>[154] P. Wu, Y. Tu, X. Yuan, A. Jatowt, and Z. Yang, "Neural framework for joint evolution modeling of user feedback and social links in dynamic social networks." in *IJCAI*, 2018, pp. 1632–1638.
- <span id="page-16-48"></span>[155] L. Wu, L. Chen, R. Hong, Y. Fu, X. Xie, and M. Wang, "A hierarchical attention model for social contextual image recommendation," *IEEE TKDE*, vol. 32, no. 10, pp. 1854–1867, 2019.
- <span id="page-16-49"></span>[156] L. Wu, P. Sun, Y. Fu, R. Hong, X. Wang, and M. Wang, "A neural influence diffusion model for social recommendation," in *SIGIR*, 2019, pp. 235–244.
- <span id="page-16-50"></span>[157] C. Chen, M. Zhang, C. Wang, W. Ma, M. Li, Y. Liu, and S. Ma, "An efficient adaptive transfer neural network for social-aware recommendation," in *SIGIR*, 2019, pp. 225–234.
- <span id="page-16-51"></span>[158] Y. Liu, C. Liang, X. He, J. Peng, Z. Zheng, and J. Tang, "Modelling high-order social relations for item recommendation," *IEEE TKDE*, 2020, preprint.
- <span id="page-16-52"></span>[159] L. Hu, S. Jian, L. Cao, Z. Gu, Q. Chen, and A. Amirbekyan, "Hers: Modeling influential contexts with heterogeneous relations for sparse and cold-start recommendation," in *AAAI*, 2019, pp. 3830– 3837.
- <span id="page-16-53"></span>[160] W. Xiao, H. Zhao, H. Pan, Y. Song, V. W. Zheng, and Q. Yang, "Beyond personalization: Social content recommendation for creator equality and consumer satisfaction," in *SIGKDD*, 2019, pp. 235– 245.

- <span id="page-17-0"></span>[161] W. Fan, Y. Ma, Q. Li, Y. He, E. Zhao, J. Tang, and D. Yin, "Graph neural networks for social recommendation," in *WWW*, 2019, pp. 417–426.
- <span id="page-17-1"></span>[162] W. Song, Z. Xiao, Y. Wang, L. Charlin, M. Zhang, and J. Tang, "Session-based social recommendation via dynamic graph attention networks," in *WSDM*, 2019, pp. 555–563.
- <span id="page-17-2"></span>[163] Q. Wu, H. Zhang, X. Gao, P. He, P. Weng, H. Gao, and G. Chen, "Dual graph attention networks for deep latent representation of multifaceted social effects in recommender systems," in *WWW*, 2019, pp. 2091–2102.
- <span id="page-17-3"></span>[164] L. Wu, J. Li, P. Sun, R. Hong, Y. Ge, and M. Wang, "Diffnet++: A neural influence and interest diffusion network for social recommendation," *IEEE TKDE*, 2020, preprint.
- <span id="page-17-4"></span>[165] V. Satuluri, Y. Wu, X. Zheng, Y. Qian, B. Wichers, Q. Dai, G. M. Tang, J. Jiang, and J. Lin, "Simclusters: Community-based representations for heterogeneous recommendations at twitter," in *SIGKDD*, 2020, pp. 3183–3193.
- <span id="page-17-5"></span>[166] B. Jin, K. Cheng, L. Zhang, Y. Fu, M. Yin, and L. Jiang, "Partial relationship aware influence diffusion via a multi-channel encoding scheme for social recommendation," in *CIKM*, 2020, pp. 585–594.
- <span id="page-17-6"></span>[167] Y. Xian, Z. Fu, S. Muthukrishnan, G. de Melo, and Y. Zhang, "Reinforcement knowledge graph reasoning for explainable recommendation," in *SIGIR*, 2019, pp. 285–294.
- <span id="page-17-7"></span>[168] X. Wang, D. Wang, C. Xu, X. He, Y. Cao, and T.-S. Chua, "Explainable reasoning over knowledge graphs for recommendation," in *AAAI*, 2019, pp. 5329–5336.
- <span id="page-17-8"></span>[169] Y. Cao, X. Wang, X. He, Z. Hu, and T. Chua, "Unifying knowledge graph learning and recommendation: Towards a better understanding of user preferences," in *WWW*, 2019, pp. 151–161.
- <span id="page-17-9"></span>[170] X. Wang, X. He, Y. Cao, M. Liu, and T. Chua, "KGAT: knowledge graph attention network for recommendation," in *SIGKDD*, 2019, pp. 950–958.
- <span id="page-17-10"></span>[171] K. Zhao, X. Wang, Y. Zhang, L. Zhao, Z. Liu, C. Xing, and X. Xie, "Leveraging demonstrations for reinforcement recommendation reasoning over knowledge graphs," in *SIGIR*, 2020, pp. 239–248.
- <span id="page-17-11"></span>[172] X. Wang, X. He, and T.-S. Chua, "Learning and reasoning on graph for recommendation," in *WSDM*, 2020, pp. 890–893.
- <span id="page-17-12"></span>[173] Q. Zhu, X. Zhou, J. Wu, J. Tan, and L. Guo, "A knowledge-aware attentional reasoning network for recommendation," in *AAAI*, 2020, pp. 6999–7006.
- <span id="page-17-13"></span>[174] X. Yu, X. Ren, Y. Sun, Q. Gu, B. Sturt, U. Khandelwal, B. Norick, and J. Han, "Personalized entity recommendation: a heterogeneous information network approach," in *WSDM*, 2014, pp. 283– 292.
- <span id="page-17-14"></span>[175] Z. Sun, J. Yang, J. Zhang, A. Bozzon, L. Huang, and C. Xu, "Recurrent knowledge graph embedding for effective recommendation," in *RecSys*, 2018, pp. 297–305.
- <span id="page-17-15"></span>[176] H. Zhao, Q. Yao, J. Li, Y. Song, and D. L. Lee, "Meta-graph based recommendation fusion over heterogeneous information networks," in *SIGKDD*, 2017, pp. 635–644.
- <span id="page-17-16"></span>[177] B. Hu, C. Shi, W. X. Zhao, and P. S. Yu, "Leveraging meta-path based context for top- N recommendation with A neural coattention model," in *SIGKDD*, 2018, pp. 1531–1540.
- <span id="page-17-17"></span>[178] J. Huang, W. X. Zhao, H. Dou, J.-R. Wen, and E. Y. Chang, "Improving sequential recommendation with knowledge-enhanced memory networks," in *SIGIR*, 2018, pp. 505–514.
- <span id="page-17-18"></span>[179] H. Wang, F. Zhang, M. Zhao, W. Li, X. Xie, and M. Guo, "Multitask feature learning for knowledge graph enhanced recommendation," in *WWW*, 2019, pp. 2000–2010.
- <span id="page-17-19"></span>[180] H. Wang, F. Zhang, M. Zhang, J. Leskovec, M. Zhao, W. Li, and Z. Wang, "Knowledge-aware graph neural networks with label smoothness regularization for recommender systems," in *SIGKDD*, 2019, pp. 968–977.
- <span id="page-17-20"></span>[181] C.-Y. Tai, M.-R. Wu, Y.-W. Chu, S.-Y. Chu, and L.-W. Ku, "Mvin: Learning multiview items for recommendation," in *SIGIR*, 2020, pp. 99–108.
- <span id="page-17-21"></span>[182] C. Chen, M. Zhang, W. Ma, Y. Liu, and S. Ma, "Jointly nonsampling learning for knowledge graph enhanced recommendation," in *SIGIR*, 2020, pp. 189–198.
- <span id="page-17-22"></span>[183] R. Sun, X. Cao, Y. Zhao, J. Wan, K. Zhou, F. Zhang, Z. Wang, and K. Zheng, "Multi-modal knowledge graphs for recommender systems," in *CIKM*, 2020, pp. 1405–1414.
- <span id="page-17-23"></span>[184] K. Zhou, W. X. Zhao, S. Bian, Y. Zhou, J.-R. Wen, and J. Yu, "Improving conversational recommender systems via knowledge graph based semantic fusion," in *SIGKDD*, 2020, pp. 1006–1014.

- <span id="page-17-24"></span>[185] B. Jin, C. Gao, X. He, D. Jin, and Y. Li, "Multi-behavior recommendation with graph convolutional networks," in *SIGIR*, 2020, pp. 659–668.
- <span id="page-17-25"></span>[186] L. Hu, S. Xu, C. Li, C. Yang, C. Shi, N. Duan, X. Xie, and M. Zhou, "Graph neural news recommendation with unsupervised preference disentanglement," in *ACL*, 2020, pp. 4255–4264.
- <span id="page-17-26"></span>[187] X. Wang, T. Huang, D. Wang, Y. Yuan, Z. Liu, X. He, and T. Chua, "Learning intents behind interactions with knowledge graph for recommendation," in *WWW*, 2021, pp. 878–887.
- <span id="page-17-27"></span>[188] L. Gao, H. Yang, J. Wu, C. Zhou, W. Lu, and Y. Hu, "Recommendation with multi-source heterogeneous information," in *IJCAI*, 2018, pp. 3378–3384.
- <span id="page-17-28"></span>[189] J. Gong, S. Wang, J. Wang, W. Feng, H. Peng, J. Tang, and P. S. Yu, "Attentional graph convolutional networks for knowledge concept recommendation in moocs in a heterogeneous view," in *SIGIR*, 2020, pp. 79–88.
- <span id="page-17-29"></span>[190] Y. Wang, S. Tang, Y. Lei, W. Song, S. Wang, and M. Zhang, "Disenhan: Disentangled heterogeneous graph attention network for recommendation," in *CIKM*, 2020, pp. 1605–1614.
- <span id="page-17-30"></span>[191] Z. Han, F. Xu, J. Shi, Y. Shang, H. Ma, P. Hui, and Y. Li, "Genetic meta-structure search for recommendation on heterogeneous information network," in *CIKM*, 2020, pp. 455–464.
- <span id="page-17-31"></span>[192] X. Wang, Y. Xu, X. He, Y. Cao, M. Wang, and T.-S. Chua, "Reinforced negative sampling over knowledge graph for recommendation," in *WWW*, 2020, pp. 99–109.
- <span id="page-17-32"></span>[193] P. Wang, Y. Fan, L. Xia, W. X. Zhao, S. Niu, and J. Huang, "Kerl: A knowledge-guided reinforcement learning model for sequential recommendation," in *SIGIR*, 2020, pp. 209–218.
- <span id="page-17-33"></span>[194] P. Symeonidis, A. Janes, D. Chaltsev, P. Giuliani, D. Morandini, A. Unterhuber, L. Coba, and M. Zanker, "Recommending the video to watch next: an offline and online evaluation at youtv. de," in *RecSys*, 2020, pp. 299–308.
- <span id="page-17-34"></span>[195] W. Lei, G. Zhang, X. He, Y. Miao, X. Wang, L. Chen, and T.-S. Chua, "Interactive path reasoning on graph for conversational recommendation," in *SIGKDD*, 2020, pp. 2073–2083.
- <span id="page-17-35"></span>[196] H. Wang, F. Zhang, J. Wang, M. Zhao, W. Li, X. Xie, and M. Guo, "Ripplenet: Propagating user preferences on the knowledge graph for recommender systems," in *CIKM*, 2018, pp. 417–426.
- <span id="page-17-36"></span>[197] Y. Lin, Z. Liu, M. Sun, Y. Liu, and X. Zhu, "Learning entity and relation embeddings for knowledge graph completion," in *AAAI*, 2015, pp. 2181–2187.
- <span id="page-17-37"></span>[198] H. Wang, F. Zhang, X. Xie, and M. Guo, "Dkn: Deep knowledgeaware network for news recommendation," in *WWW*, 2018, pp. 1835–1844.
- <span id="page-17-38"></span>[199] Z. Wang, G. Lin, H. Tan, Q. Chen, and X. Liu, "Ckan: Collaborative knowledge-aware attentive network for recommender systems," in *SIGIR*, 2020, pp. 219–228.
- <span id="page-17-39"></span>[200] W. Meng, D. Yang, and Y. Xiao, "Incorporating user microbehaviors and item knowledge into multi-task learning for session-based recommendation," in *SIGIR*, 2020, pp. 1091–1100.
- <span id="page-17-40"></span>[201] B. Hidasi, A. Karatzoglou, L. Baltrunas, and D. Tikk, "Sessionbased recommendations with recurrent neural networks," in *ICLR*, 2016.
- <span id="page-17-41"></span>[202] B. Hidasi, M. Quadrana, A. Karatzoglou, and D. Tikk, "Parallel recurrent neural network architectures for feature-rich sessionbased recommendations," in *RecSys*, 2016, pp. 241–248.
- <span id="page-17-42"></span>[203] S. Wu, Y. Tang, Y. Zhu, L. Wang, X. Xie, and T. Tan, "Sessionbased recommendation with graph neural networks," in *AAAI*, 2019, pp. 346–353.
- <span id="page-17-43"></span>[204] C.-Y. Wu, A. Ahmed, A. Beutel, A. J. Smola, and H. Jing, "Recurrent recommender networks," in *WSDM*, 2017, pp. 495–503.
- <span id="page-17-44"></span>[205] H. Jing and A. J. Smola, "Neural survival recommender," in *WSDM*, 2017, pp. 515–524.
- <span id="page-17-45"></span>[206] H. Dai, Y. Wang, R. Trivedi, and L. Song, "Recurrent coevolutionary latent feature processes for continuous-time recommendation," in *DLRS*, 2016, pp. 29–34.
- <span id="page-17-46"></span>[207] P. Wu, Y. Tu, Z. Yang, A. Jatowt, and M. Odagaki, "Deep modeling of the evolution of user preferences and item attributes in dynamic social networks," in *WWW*, 2018, pp. 115–116.
- <span id="page-17-47"></span>[208] A. Beutel, P. Covington, S. Jain, C. Xu, J. Li, V. Gatto, and E. H. Chi, "Latent cross: Making use of context in recurrent recommender systems," in *WSDM*, 2018, pp. 46–54.
- <span id="page-17-48"></span>[209] T. Donkers, B. Loepp, and J. Ziegler, "Sequential user-based recurrent neural network recommendations," in *RecSys*, 2017, pp. 152–160.

- <span id="page-18-0"></span>[210] Q. Wang, H. Yin, Z. Hu, D. Lian, H. Wang, and Z. Huang, "Neural memory streaming recommender networks with adversarial training," in *SIGKDD*, 2018, pp. 2467–2475.
- <span id="page-18-1"></span>[211] X. Chen, H. Xu, Y. Zhang, J. Tang, Y. Cao, Z. Qin, and H. Zha, "Sequential recommendation with user memory networks," in *WSDM*, 2018, pp. 108–116.
- <span id="page-18-2"></span>[212] Q. Liu, Y. Zeng, R. Mokhosi, and H. Zhang, "STAMP: short-term attention/memory priority model for session-based recommendation," in *SIGKDD*, 2018, pp. 1831–1839.
- <span id="page-18-3"></span>[213] E. Smirnova and F. Vasile, "Contextual sequence modeling for recommendation with recurrent neural networks," in *DLRS*, 2017, pp. 2–9.
- <span id="page-18-4"></span>[214] J. Li, P. Ren, Z. Chen, Z. Ren, T. Lian, and J. Ma, "Neural attentive session-based recommendation," in *CIKM*, 2017, pp. 1419–1428.
- <span id="page-18-5"></span>[215] Y. K. Tan, X. Xu, and Y. Liu, "Improved recurrent neural networks for session-based recommendations," in *DLRS*, 2016, pp. 17–22.
- <span id="page-18-6"></span>[216] D. Jannach and M. Ludewig, "When recurrent neural networks meet the neighborhood for session-based recommendation," in *RecSys*, 2017, pp. 306–310.
- <span id="page-18-7"></span>[217] P. Loyola, C. Liu, and Y. Hirate, "Modeling user session and intent with an attention-based encoder-decoder architecture," in *RecSys*, 2017, pp. 147–151.
- <span id="page-18-8"></span>[218] F. Yuan, X. He, A. Karatzoglou, and L. Zhang, "Parameterefficient transfer from sequential behaviors for user modeling and recommendation," in *SIGIR*, 2020, pp. 1469–1478.
- <span id="page-18-9"></span>[219] J. Yin, C. Liu, W. Wang, J. Sun, and S. C. Hoi, "Learning transferrable parameters for long-tailed sequential user behavior modeling," in *SIGKDD*, 2020, pp. 359–367.
- <span id="page-18-10"></span>[220] T. X. Tuan and T. M. Phuong, "3d convolutional networks for session-based recommendation with content features," in *RecSys*, 2017, pp. 138–146.
- <span id="page-18-11"></span>[221] W.-C. Kang and J. McAuley, "Self-attentive sequential recommendation," in *ICDM*, 2018, pp. 197–206.
- <span id="page-18-12"></span>[222] R. Ren, Z. Liu, Y. Li, W. X. Zhao, H. Wang, B. Ding, and J.- R. Wen, "Sequential recommendation with self-attentive multiadversarial network," in *SIGIR*, 2020, pp. 89–98.
- <span id="page-18-13"></span>[223] D. Gligorijevic, J. Gligorijevic, A. Raghuveer, M. Grbovic, and Z. Obradovic, "Modeling mobile user actions for purchase recommendation using deep memory networks," in *SIGIR*, 2018, pp. 1021–1024.
- <span id="page-18-14"></span>[224] C. Xu, P. Zhao, Y. Liu, V. S. Sheng, J. Xu, F. Zhuang, J. Fang, and X. Zhou, "Graph contextualized self-attention network for session-based recommendation," in *IJCAI*, 2019, pp. 3940–3946.
- <span id="page-18-15"></span>[225] R. Qiu, H. Yin, Z. Huang, and T. Chen, "Gag: Global attributed graph neural network for streaming session-based recommendation," in *SIGIR*, 2020, pp. 669–678.
- <span id="page-18-16"></span>[226] Z. Wang, W. Wei, G. Cong, X.-L. Li, X.-L. Mao, and M. Qiu, "Global context enhanced graph neural networks for sessionbased recommendation," in *SIGIR*, 2020, pp. 169–178.
- <span id="page-18-17"></span>[227] Z. Pan, F. Cai, W. Chen, H. Chen, and M. de Rijke, "Star graph neural networks for session-based recommendation," in *CIKM*, 2020, pp. 1195–1204.
- <span id="page-18-18"></span>[228] T. Chen and R. C.-W. Wong, "Handling information loss of graph neural networks for session-based recommendation," in *SIGKDD*, 2020, pp. 1172–1180.
- <span id="page-18-19"></span>[229] H. Ying, F. Zhuang, F. Zhang, Y. Liu, G. Xu, X. Xie, H. Xiong, and J. Wu, "Sequential recommender system based on hierarchical attention networks," in *IJCAI*, 2018, pp. 3926–3932.
- <span id="page-18-20"></span>[230] P. Wang, J. Guo, Y. Lan, J. Xu, S. Wan, and X. Cheng, "Learning hierarchical representation model for nextbasket recommendation," in *SIGIR*, 2015, pp. 403–412.
- <span id="page-18-21"></span>[231] C. Ma, P. Kang, and X. Liu, "Hierarchical gating networks for sequential recommendation," in *SIGKDD*, 2019, pp. 825–833.
- <span id="page-18-22"></span>[232] L. Yu, C. Zhang, S. Liang, and X. Zhang, "Multi-order attentive ranking model for sequential recommendation," in *AAAI*, 2019, pp. 5709–5716.
- <span id="page-18-23"></span>[233] J. Lin, W. Pan, and Z. Ming, "Fissa: fusing item similarity models with self-attention networks for sequential recommendation," in *RecSys*, 2020, pp. 130–139.
- <span id="page-18-24"></span>[234] L. Wu, S. Li, C.-J. Hsieh, and J. Sharpnack, "Sse-pt: Sequential recommendation via personalized transformer," in *RecSys*, 2020, pp. 328–337.
- <span id="page-18-25"></span>[235] Z. Li, H. Zhao, Q. Liu, Z. Huang, T. Mei, and E. Chen, "Learning from history and present: Next-item recommendation via discriminatively exploiting user behaviors," in *SIGKDD*, 2018, pp. 1734–1743.

- <span id="page-18-26"></span>[236] M. Quadrana, A. Karatzoglou, B. Hidasi, and P. Cremonesi, "Personalizing session-based recommendations with hierarchical recurrent neural networks," in *RecSys*, 2017, pp. 130–137.
- <span id="page-18-27"></span>[237] T. Bai, L. Zou, W. X. Zhao, P. Du, W. Liu, J.-Y. Nie, and J.-R. Wen, "Ctrec: A long-short demands evolution model for continuoustime recommendation," in *SIGIR*, 2019, pp. 675–684.
- <span id="page-18-28"></span>[238] J. Tang, F. Belletti, S. Jain, M. Chen, A. Beutel, C. Xu, and E. H. Chi, "Towards neural mixture recommender for long range dependent user sequences," in *WWW*, 2019, pp. 1782–1793.
- <span id="page-18-29"></span>[239] K. Zhou, H. Wang, W. X. Zhao, Y. Zhu, S. Wang, F. Zhang, Z. Wang, and J.-R. Wen, "S3-rec: Self-supervised learning for sequential recommendation with mutual information maximization," in *CIKM*, 2020, pp. 1893–1902.
- <span id="page-18-30"></span>[240] J. Wu, R. Cai, and H. Wang, "Déjà vu: A contextualized temporal attention mechanism for sequential recommendation," in *WWW*, 2020, pp. 2199–2209.
- <span id="page-18-31"></span>[241] W. Ji, K. Wang, X. Wang, T. Chen, and A. Cristea, "Sequential recommender via time-aware attentive memory network," in *CIKM*, 2020, pp. 565–574.
- <span id="page-18-32"></span>[242] W. Ye, S. Wang, X. Chen, X. Wang, Z. Qin, and D. Yin, "Time matters: Sequential recommendation with complex temporal information," in *SIGIR*, 2020, pp. 1459–1468.
- <span id="page-18-33"></span>[243] C. Wang, M. Zhang, W. Ma, Y. Liu, and S. Ma, "Make it a chorus: knowledge-and time-aware item modeling for sequential recommendation," in *SIGIR*, 2020, pp. 109–118.
- <span id="page-18-34"></span>[244] N. Zhu, J. Cao, Y. Liu, Y. Yang, H. Ying, and H. Xiong, "Sequential modeling of hierarchical user intention and preference for nextitem recommendation," in *WSDM*, 2020, pp. 807–815.
- <span id="page-18-35"></span>[245] M. Wang, P. Ren, L. Mei, Z. Chen, J. Ma, and M. de Rijke, "A collaborative session-based recommendation approach with parallel memory modules," in *SIGIR*, 2019, pp. 345–354.
- <span id="page-18-36"></span>[246] F. Yuan, A. Karatzoglou, I. Arapakis, J. M. Jose, and X. He, "A simple convolutional generative network for next item recommendation," in *WSDM*, 2019, pp. 582–590.
- <span id="page-18-37"></span>[247] J. Wang, K. Ding, L. Hong, H. Liu, and J. Caverlee, "Next-item recommendation with sequential hypergraphs," in *SIGIR*, 2020, pp. 1101–1110.
- <span id="page-18-38"></span>[248] C. Ma, L. Ma, Y. Zhang, J. Sun, X. Liu, and M. Coates, "Memory augmented graph neural networks for sequential recommendation," in *AAAI*, 2020, pp. 5045–5052.
- <span id="page-18-39"></span>[249] X. Guo, C. Shi, and C. Liu, "Intention modeling from ordered and unordered facets for sequential recommendation," in *WWW*, 2020, pp. 1127–1137.
- <span id="page-18-40"></span>[250] Q. Liu, Z. Huang, Y. Yin, E. Chen, H. Xiong, Y. Su, and G. Hu, "Ekt: Exercise-aware knowledge tracing for student performance prediction," *IEEE TKDE*, vol. 33, no. 1, pp. 100–115, 2021.
- <span id="page-18-41"></span>[251] Q. Cui, S. Wu, Q. Liu, W. Zhong, and L. Wang, "Mv-rnn: a multiview recurrent neural network for sequential recommendation," *IEEE TKDE*, pp. 317–331, 2020.
- <span id="page-18-42"></span>[252] A. Graves, G. Wayne, and I. Danihelka, "Neural turing machines," *ArXiv*, vol. abs/1410.5401, 2014.
- <span id="page-18-43"></span>[253] S. Sukhbaatar, J. Weston, R. Fergus *et al.*, "End-to-end memory networks," in *NeurIPS*, 2015, pp. 2440–2448.
- <span id="page-18-44"></span>[254] M. Quadrana, A. Karatzoglou, B. Hidasi, and P. Cremonesi, "Personalizing session-based recommendations with hierarchical recurrent neural networks," in *RecSys*, 2017, pp. 130–137.
- <span id="page-18-45"></span>[255] S. Wu, Y. Tang, Y. Zhu, L. Wang, X. Xie, and T. Tan, "Sessionbased recommendation with graph neural networks," in *AAAI*, 2019, pp. 346–353.
- <span id="page-18-46"></span>[256] C. Xu, P. Zhao, Y. Liu, V. S. Sheng, J. Xu, F. Zhuang, J. Fang, and X. Zhou, "Graph contextualized self-attention network for session-based recommendation," in *IJCAI*, 2019, pp. 3940–3946.
- <span id="page-18-47"></span>[257] Q. Wu, Y. Gao, X. Gao, P. Weng, and G. Chen, "Dual sequential prediction models linking sequential recommendation and information dissemination," in *SIGKDD*, 2019, pp. 447–457.
- <span id="page-18-48"></span>[258] C. Shi, Y. Li, J. Zhang, Y. Sun, and S. Y. Philip, "A survey of heterogeneous information network analysis," *IEEE TKDE*, vol. 29, no. 1, pp. 17–37, 2016.
- <span id="page-18-49"></span>[259] S. Gidaris, P. Singh, and N. Komodakis, "Unsupervised representation learning by predicting image rotations," in *ICLR (Poster)*, 2018.
- <span id="page-18-50"></span>[260] A. v. d. Oord, Y. Li, and O. Vinyals, "Representation learning with contrastive predictive coding," *ArXiv*, 2018.
- <span id="page-18-51"></span>[261] J. Wu, X. Wang, F. Feng, X. He, L. Chen, J. Lian, and X. Xie, "Selfsupervised graph learning for recommendation," in *SIGIR*, 2021, pp. 726–735.

- <span id="page-19-0"></span>[262] Y. Yang, L. Wu, R. Hong, K. Zhang, and M. Wang, "Enhanced graph learning for collaborative filtering via mutual information maximization," in *SIGIR*, 2021, pp. 71–80.
- <span id="page-19-1"></span>[263] Y. Wei, X. Wang, Q. Li, L. Nie, Y. Li, X. Li, and T.-S. Chua, "Contrastive learning for cold-start recommendation," *ArXiv*, vol. abs/2107.05315, 2021.
- <span id="page-19-2"></span>[264] X. Xia, H. Yin, J. Yu, Q. Wang, L. Cui, and X. Zhang, "Selfsupervised hypergraph convolutional networks for sessionbased recommendation," in *AAAI*, 2021, pp. 4503–4511.
- <span id="page-19-3"></span>[265] L. Chen, L. Wu, K. Zhang, R. Hong, and M. Wang, "Set2setrank: Collaborative set to set ranking for implicit feedback based recommendation," in *SIGIR*, 2021, pp. 585–594.
- <span id="page-19-4"></span>[266] N. Mehrabi, F. Morstatter, N. Saxena, K. Lerman, and A. Galstyan, "A survey on bias and fairness in machine learning," *ArXiv*, vol. abs/1908.09635, 2019.
- <span id="page-19-5"></span>[267] J. Chen, H. Dong, X. lei Wang, F. Feng, M.-C. Wang, and X. He, "Bias and debias in recommender system: A survey and future directions," *ArXiv*, vol. abs/2010.03240, 2020.
- <span id="page-19-6"></span>[268] L. Wu, L. Chen, P. Shao, R. Hong, X. Wang, and M. Wang, "Learning fair representations for recommendation: A graph based perspective," in *WWW*, 2021, pp. 2198s–2208.
- <span id="page-19-7"></span>[269] P. Shao, L. Wu, L. Chen, K. Zhang, and M. Wang, "Faircf: Fairness-aware collaborative filtering."
- <span id="page-19-8"></span>[270] Y. Ji, A. Sun, J. Zhang, and C. Li, "A re-visit of the popularity baseline in recommender systems," in *SIGIR*, 2020, pp. 1749– 1752.
- <span id="page-19-9"></span>[271] M. F. Dacrema, P. Cremonesi, and D. Jannach, "Are we really making much progress? a worrying analysis of recent neural recommendation approaches," in *Recsys*, 2019, pp. 101–109.
- <span id="page-19-10"></span>[272] M. F. Dacrema, S. Boglio, P. Cremonesi, and D. Jannach, "A troubling analysis of reproducibility and progress in recommender systems research," *TOIS*, vol. 39, no. 2, pp. 20:1–20:49, 2021.
- <span id="page-19-11"></span>[273] S. Rendle, W. Krichene, L. Zhang, and J. R. Anderson, "Neural collaborative filtering vs. matrix factorization revisited," in *Rec-Sys*, 2020, pp. 240–248.
- <span id="page-19-12"></span>[274] S. Rendle, L. Zhang, and Y. Koren, "On the difficulty of evaluating baselines: A study on recommender systems," *ArXiv*, vol. abs/1905.01395, 2019.
- <span id="page-19-13"></span>[275] C.-J. Wu, R. Burke, E. H. Chi, J. Konstan, J. McAuley, Y. Raimond, and H. Zhang, "Developing a recommendation benchmark for mlperf training and inference," *ArXiv*, vol. abs/2003.07336, 2020.
- <span id="page-19-14"></span>[276] F. Wu, Y. Qiao, J.-H. Chen, C. Wu, T. Qi, J. Lian, D. Liu, X. Xie, J. Gao, W. Wu *et al.*, "Mind: A large-scale dataset for news recommendation," in *ACL*, 2020, pp. 3597–3606.
- <span id="page-19-15"></span>[277] B. Paudel, D. Kocev, and T. Eftimov, "Mix and rank: A framework for benchmarking recommender systems," in *Big Data*, 2019, pp. 3717–3726.
- <span id="page-19-16"></span>[278] A. Said and A. Bellogín, "Rival: a toolkit to foster reproducibility in recommender system evaluation," in *RecSys*, 2014, pp. 371–372.
- <span id="page-19-17"></span>[279] W. Krichene and S. Rendle, "On sampled metrics for item recommendation," in *SIGKDD*, 2020, pp. 1748–1757.

![](_page_19_Picture_19.jpeg)
<!-- Image Description: The image is a text block providing biographical information on Le Wu. It states her current position as associate professor and Ph.D. supervisor at Hefei University of Technology, her Ph.D. from University of Science and Technology of China, her research interests (data mining, recommender systems, social network analysis), and her publication record (over 50 papers). It also mentions awards she received. The image contains no diagrams, charts, graphs, or equations. -->

sociation for Artificial Intelligence (CAAI) 2017, and the Youth Talent Promotion Project from China Association for Science and Technology.

![](_page_19_Picture_21.jpeg)
<!-- Image Description: That's not a technical image; it's a photograph of a person. There are no diagrams, charts, graphs, equations, or technical illustrations present. The image is likely an author photograph for the academic paper, providing a visual representation of the author. It serves no technical purpose within the paper's content. -->

**Xiangnan He**is a professor at the University of Science and Technology of China (USTC). He received his Ph.D. in Computer Science from the National University of Singapore (NUS). His research interests span information retrieval, data mining, and multi-media analytics. He has over 80 publications that appeared in several top conferences such as SIGIR, WWW, and MM, and journals including TKDE, TOIS, and TMM. His work has received the Best Paper Award Honorable Mention in WWW 2018 and ACM SIGIR

2016. He is in the editorial board of journals including Frontiers in Big Data, AI Open etc. Moreover, he has served as the PC chair of CCIS 2019 and SPC/PC member for several top conferences including SIGIR, WWW, KDD, MM, WSDM, ICML etc., and the regular reviewer for journals including TKDE, TOIS, TMM, etc.

![](_page_19_Picture_24.jpeg)
<!-- Image Description: That's not a technical image; it's a headshot photograph of a person. It contains no diagrams, charts, graphs, equations, or technical illustrations. Within the context of an academic paper, it would likely be an author photograph, serving only an identification purpose and not conveying any technical information. -->
**Xiang Wang**is now a research fellow at National University of Singapore. He received his Ph.D. degree from National University of Singapore in 2019. His research interests include recommender systems, graph learning, and explainable deep learning techniques. He has published some academic papers on international conferences such as KDD, WWW, SIGIR, and AAAI. He serves as a program committee member for several top conferences such as KDD, SIGIR, WWW, and IJCAI, and invited reviewer for pres-

tigious journals such as TKDE, TOIS, TNNLS, and TMM.

![](_page_19_Picture_27.jpeg)
<!-- Image Description: That's not a technical image; it's a headshot photograph of a person. There are no diagrams, charts, graphs, equations, or technical illustrations. The image is likely an author photograph included in the paper for identification purposes and not related to the technical content of the research. -->
**Kun Zhang**received the PhD degree in computer science and technology from University of Science and Technology of China, Hefei, China, in 2019. He is is currently a faculty member with the Hefei University of Technology (HFUT), China. His research interests include Natural Language Understanding, Recommendation System. He has published several papers in refereed journals and conferences, such as the IEEE Transactions on Systems, Man, and Cybernetics: Systems, the ACM Transactions on

Knowledge Discovery from Data, AAAI, KDD, ACL, SIGIR, WWW, ICDM. He received the KDD 2018 Best Student Paper Award.

![](_page_19_Picture_30.jpeg)
<!-- Image Description: That's not a technical image; it's a photograph of a person. It contains no diagrams, charts, graphs, equations, or technical illustrations. In the context of an academic paper, it's likely an author portrait or a contributor photograph and has no technical content. -->
**Meng Wang** received the BE and PhD degrees from USTC, in 2003 and 2008, respectively. He is a professor with HFUT. His current research interests include multimedia content analysis, computer vision, and pattern recognition. He has authored more than 200 book chapters, journal, and conference papers in these areas. He is the recipient of the ACM SIGMM Rising Star Award 2014. He is an associate editor of the IEEE Transactions on Knowledge and Data Engineering, the IEEE Transactions on Circuits and

Systems for Video Technology, and the IEEE Transactions on Neural Networks and Learning Systems. He is an IEEE Fellow and IAPR Fellow.
