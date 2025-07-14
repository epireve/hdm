---
cite_key: yao_2024
---

# FEDRKG: A Privacy-preserving Federated Recommendation Framework via Knowledge Graph Enhancement

Dezhong Yao^1^ Tongtong Liu^1^ Qi Cao^2^ Hai Jin^1^ ^1^Huazhong University of Science and Technology ^2^University of Glasgow {dyao,tliu,hjin}@hust.edu.cn qi.cao@glasgow.ac.uk

## Abstract

**Federated Learning:** (FL) has emerged as a promising approach for preserving data privacy in recommendation systems by training models locally. Recently, *Graph Neural Networks* (GNN) have gained popularity in recommendation tasks due to their ability to capture high-order interactions between users and items. However, privacy concerns prevent the global sharing of the entire user-item graph. To address this limitation, some methods create pseudo-interacted items or users in the graph to compensate for missing information for each client. Unfortunately, these methods introduce random noise and raise privacy concerns. In this paper, we propose FEDRKG, a novel federated recommendation system, where a global *knowledge graph* (KG) is constructed and maintained on the server using publicly available item information, enabling higher-order user-item interactions. On the client side, a relation-aware GNN model leverages diverse KG relationships. To protect local interaction items and obscure gradients, we employ pseudo-labeling and *Local Differential Privacy* (LDP). Extensive experiments conducted on three real-world datasets demonstrate the competitive performance of our approach compared to centralized algorithms while ensuring privacy preservation. Moreover, FEDRKG achieves an average accuracy improvement of 4% compared to existing federated learning baselines.

## TL;DR
Privacy-preserving federated recommendation framework that leverages knowledge

## Key Insights
Uses Local Differential Privacy (LDP) and pseudo-labeling to enable federated learning with knowledge graph enhancement while preventing global sharing of user-item interactions, achieving 4% accuracy improvement over baselines.

## 1 Introduction

Recommendation systems are widely used in various domains, such as e-commerce and social recommendation, by alleviating users from the burden of sifting through vast amounts of data to discover suitable options [[1]](#ref-1). These systems utilize user preferences and relevant information to provide personalized recommendations, making the process of finding relevant items more efficient and convenient [[2]](#ref-2). However, the effectiveness of most recommendation methods heavily relies on centralized storage of user data [[3]](#ref-3). User data generated from software usage has the potential to enhance user experiences, deliver personalized services, and provide insights into user behavior [[4]](#ref-4). Nevertheless, user data inherently includes user preferences and involves personal privacy. With the increasing awareness of privacy and the implementation of relevant regulations such as the *General Data Protection Regulation* (GDPR) [[5]](#ref-5), service providers may face growing challenges in centrally storing and processing user data, as shown in Fig. [1](#ref-fig-1)a).

The exclusive client access to local data leads to two challenges. Firstly, limited access to firstorder interaction data hampers the effectiveness of the recommendation model. Secondly, privacypreserving mechanisms are required to ensure secure communication between the client and server. To address these challenges, FL is introduced into the recommendation system. Existing works focus on the case of Fig. [1](#ref-fig-1)b), where recommendations are achieved by directly finding correlations between

![The image compares three machine learning approaches: centralized learning, federated learning based on user relevance, and federated learning based on item relevance. It uses diagrams showing users (represented by icons) interacting with items (shopping bags). (a) shows a centralized server collecting all data. (b) and (c) illustrate federated learning, where data remains decentralized, with (b) focusing on user-based interactions and (c) on item-based interactions, ultimately contributing to a knowledge graph.](_page_1_Figure_0.jpeg)
<a id="ref-fig-1"></a>**Figure 1:** Comparison of centralized learning, federated learning with enhanced user connections, and federated learning with enhanced project connections.

users. For example, FedMF [[6]](#ref-6) and FedGNN [[7]](#ref-7) use only the local user-item interaction graph to find links between different users by *collaborative filtering* (CF). However, incorporating various types of information in the conventional graph recommendation task can significantly improve the recommendation accuracy while changing the graph structure [[4]](#ref-4). Additionally, FeSoG [[8]](#ref-8) utilizes social networks as side information, adding direct connections between different users. Nevertheless, this method requires the server to possess the complete social network, which is a type of private data that is difficult to obtain for most recommendation systems. Furthermore, methods like FedGNN employ homomorphic encryption, which incurs substantial computational overhead and is not suitable as the primary encryption algorithm on edge devices with performance constraints.

To maximize the utilization of diverse data types while ensuring privacy protection on edge devices, we propose FEDRKG^1^, a GNN-based federated learning recommendation framework. Unlike CF or direct construction of connections between users using privacy-sensitive information, FEDRKG leverages publicly available item information (e.g., appearance, attributes) to establish higher-order connections between different items, as shown in Fig. [1](#ref-fig-1)c).

The server firstly constructs and maintains *knowledge graphs* (KGs) by utilizing publicly available item information. Then, we employ on-demand sampling of KGs and distribute them to the client. Subsequently, we design a novel method to expand the local graph by merging KG subgraphs with the local user-item interaction graph, enabling the construction of high-order user-item interactions through KGs. Additionally, our framework introduces a request-based distribution mechanism. By obfuscating interaction items into request items, the server can efficiently distribute only the necessary request embeddings, significantly reducing communication overhead compared to previous methods while effectively protecting the privacy of raw interaction items. Simultaneously, we employ *local differential privacy* (LDP) to protect all uploaded gradients, further enhancing the privacy of the federated learning process. Our approach has been extensively evaluated on three real-world datasets, demonstrating its competitive performance compared to centralized algorithms while ensuring privacy preservation. Moreover, FEDRKG outperforms existing federated learning baselines, achieving an average accuracy improvement of approximately 4%. The major contributions of this work are summarized as follows:

- To the best of our knowledge, we are the first to introduce a knowledge graph to enhance the performance of the federated recommendation system while protecting privacy.
- We introduce an algorithm for user-item graph expansion using KG subgraphs to improve local training.
- We propose innovative privacy-preserving techniques for interaction items, while simultaneously reducing communication overhead through strategic distribution of embeddings.

^1^The source code is available at: <https://github.com/ttliu98/FedRKG>

## 2 Related Work

## 1 Knowledge Graph Based Recommendation

In recent years, significant research has focused on recommendation systems that utilize *Graph Neural Networks* (GNNs). GNNs have gained attention and popularity in recommendation systems due to their ability to learn representations of graph-structured data, which is well-suited for the inherent graph structures in recommendation systems. Knowledge graphs, as a typical graph structure, are often leveraged as side information in recommendation systems. By incorporating knowledge graphs, high-order connections can be established through the relationships between items and their attributes. This integration enhances the accuracy of item representations and provides interpretability to the recommendation results. One type of method is integrating user-item interactions into KG. Methods like KGAT [[1]](#ref-1), CKAN [[9]](#ref-9), and MKGAT [[10]](#ref-10) treat users as entities within KG, and relationships between users and items are incorporated as part of KG's relationships, too. This integration enables the merged graph to be processed using a generic GNN model designed for knowledge graphs. Another idea is employed by KGCN [[11]](#ref-11) and KGNN-LS [[12]](#ref-12), directly connecting KG to the useritem graph without any transformation. These methods utilize relation-aware aggregation and consider the user's preference for relationships when generating recommendations.

## 2 Federated Learning for Recommendation System

Federated learning is extensively utilized in privacy-preserving scenarios, as it ensures that the original data remains on local devices while allowing multiple clients to train a model together [[13]](#ref-13). Considering the information required for recommendations, which includes users' preferences for items, the introduction of federated learning can help us prevent privacy breaches. FedSage [[14]](#ref-14) and FKGE [[15]](#ref-15) focus on cross-silo federation learning, they are not suitable for protecting the privacy of individual users on client devices. FCF [[16]](#ref-16) and FedMF [[6]](#ref-6) decompose the scoring matrix, retain user embeddings locally, and aggregate item embeddings on the server. FedGNN [[7]](#ref-7) utilizes homomorphic encryption for CF and protects the original gradients using pseudo-labeling and LDP. However, the computational requirements for homomorphic encryption pose challenges, particularly on performance-constrained devices. In contrast to methods that do not leverage any side information, FeSoG [[8]](#ref-8) introduces social networks to establish connections between users. Unfortunately, in many recommendation scenarios such as e-commerce, service providers do not offer social services, and social network information is considered private. Therefore, the lack of user connection on the server in Fig. [1](#ref-fig-1)b), like a social network, restricts the method's ability to generalize [[17]](#ref-17). Currently, there is a scarcity of federated learning algorithms that effectively utilize side information for cross-device scenarios.

## 3 Federated Recommendation with Knowledge Graph Enhancement

## 1 Problem Definition

User-item interactions can be represented by a typical bipartite graph G = (U, T , E), where U = {u~1~, u~2~, . . . , u^N^ } and T = {t~1~, t~2~, . . . , t~M~} represent a set of users and items of size N and M, respectively. To describe the set of edges E, an interaction matrix Y ∈ R^M×N^ is employed. In particular, y~ut~ takes on the value 1 if an interaction exists in the user's history, and 0 otherwise.

For federated recommendation, each client c^i^ owned by corresponding user u^i^ can only access the interaction graph G^i^ stored locally, containing a set of items T^i^ that have been interacted with. Each G^i^ is a subgraph of the global interaction graph G.

In addition to the client-side data, the server maintains a knowledge graph K, which is represented as a series of triples {(h, r, t) | h, t ∈ E, r ∈ R}. The entities h and t each refer to the head and tail, respectively, within the specific combination denoted by each triple, both belonging to the set of entities E. The relationship r represents the connection between two distinct entities, belonging to a set of relations R.

Our goal is to train a generalized GNN model using the local bipartite graphs G^i^ and the knowledge graph K while preserving user privacy. The model predicts the probability y^ut^ that a user u will be interested in an unexplored item t.

![This flowchart illustrates a federated learning framework using graph neural networks (GNNs). Two clients (i and j) independently process their local data (uᵢ, uⱼ) through local differential privacy (LDP) mechanisms and GNNs, generating model and embedding gradients. These gradients are uploaded to an aggregator, which updates the global GNN model based on a knowledge graph. The updated model is then distributed back to the clients. The diagram depicts the data flow and processing steps for distributed GNN training with privacy preservation.](_page_3_Figure_0.jpeg)
<a id="ref-fig-2"></a>**Figure 2:** The framework of FEDRKG.

## 2 Framework Overview

To enable privacy-preserving recommendation tasks across diverse private devices, we introduce a federated learning framework, in Fig. [2](#ref-fig-2), based on the knowledge graph named FEDRKG. In the proposed framework, the client-server architecture is adopted. The client, which is the user's private device, is responsible for training a local graph neural network model. The server, on the other hand, is responsible for aggregating the models and embeddings, maintaining the knowledge graph, and constructing higher-order connections between clients.

The entire workflow is summarized in Algorithm [1](#ref-alg-1), which concisely represents the complete workflow.

### 3 Client Design

In our framework, the client plays a crucial role in two tasks. First, it is responsible for ensuring the confidentiality of the user's private information during the communication process with the server, which is achieved through privacy-preserving algorithms. Second, the client utilizes the embeddings and models provided by the server to expand the local user-item graph and train the local model.

Based on the knowledge graph shared by the server, we design a novel method to expand the local subgraph. During the request phase, the client applies a privacy protection mechanism to the interaction items T~n~, generating obfuscated request items T'~n~. These request items are then transmitted to the server. The client receives a GNN model and a knowledge subgraph that includes the request items and some of their neighboring entities in the complete KG. By merging this knowledge subgraph with local user-item interaction, the client generates a graph for local training. This approach guarantees the privacy of the user's interaction records by never disclosing them to the server, while also allowing the client to obtain more item-related information for training, thus indirectly enabling the construction of higher-order connections through knowledge subgraph.

Once the aggregated global model is received, the client proceeds to update its local model and initiates a training process. We use a relation-aware GNN as a recommendation model [[18]](#ref-18) that conforms to the message-passing paradigm [[13]](#ref-13), as shown in Fig. [3](#ref-fig-3). For a given user u, entity e^i^, e^j^, and r~i,j~ as the relation between two entities, we follow node-wise computation at step t+1:

$$
x_i^{(t+1)} = \phi\left(x_i^{(t)}, \rho\left(\left\{m_{r_{i,j}}^{(t+1)} : (u, e_j, r_{u,v}) \in \mathcal{E}\right\}\right)\right)
$$
(1)

where x~t~^i^ ∈ R^d^ is embedding of entity e^i^ in step t. We utilize a simple summation operation as the reduce function ρ and directly replace the original embeddings with the aggregated results as the

### Algorithm 1: FEDRKG
<a id="ref-alg-1"></a>
Input: Neighbor sampling size K; embedding size d; depth of receptive field H; learning rate η; client number N; item number M; pseudo items p; (0, 1) flipping q;LDP parameter δ, λ; knowledge graph K; clients local graph n G~n~| N n=1^o^

Output: GNN parameters and KG embeddings θ,user embeddings n e~*~u~ | N n=1^o^

1 Initialize θ, K, n e~*~u~ N n=1^o^ ;
2 while FEDRKG *not converged* do
3 Randomly select a subset N from N randomly;
4 // client
5 for *each client* n ∈ N do
6 T'~n~ ← GenerateRequestItems(G~n~, p, q);
7 θ, G^n^ ← Request(T'~n~)
8 g^n^ ← LocalTrain(θ, G~n~)
9 g~n~ ←LDP(g~n~)
10 Upload(g~n~)
11 end
12 // server
13 for *each client* n ∈ N do
14 T'~n~ ←ReceiveRequest()
15 G^n^ ← GetSubKG(T'~n~)
16 Distribute(θ, G~n~)
17 g~n~ ←ReceiveGrad()
18 end
19 g ←Eq. [5](#eq-5)
20 θ ←Eq. [6](#eq-6)
21 end

reduce function, denoted as ϕ. e^j^ sends a relationship-aware message m~ri,j~ to its neighbor:

$$
m_{r_{i,j}} = \alpha_{r_{i,j}}^u x_j \tag{2}
$$

where the attention score α^u^~ri,j~ between user u and relation r~i,j~ is derived from the following formula:

s~u~^r^t,i = score(e~u~, e~rt,i~ ) (3)

$$
Att(e_u, e_i) = \alpha_{r_{t,i}}^u = \frac{\exp\left(s_{r_{t,i}}^u\right)}{\sum_{i' \in \mathcal{N}(t)} \exp\left(s_{r_{t,i'}}^u\right)}
$$
(4)

We calculate an attention score using a score function (e.g. inner product) and then normalize it. After obtaining the final embedding x^t^ of item t, we calculate the prediction y^ by a readout function and then train this GNN model using BCE as the loss function. Finally, client uploads encrypted gradient to server.

### 4 Server Design

Similar to clients, the server performs distinct tasks that are mainly distributed across two phases. Firstly, the server's primary responsibility is to respond to the client's requests. Based on the requested items, the server utilizes the knowledge graph to sample a subgraph that corresponds to a specific client. The subgraph comprises two key components, namely the structural information in the form of triples, and the feature information, represented by the embedding of entities and relations. Subsequently, the server shares the subgraph, together with the global model, with the client. Secondly, the server needs to receive all gradients of local models and embeddings uploaded by clients. These gradients are then aggregated and used to update the global model and knowledge graph.

![The image is a diagram illustrating a knowledge graph-based recommendation system. It shows user-item interactions represented as embeddings (e<sub>u</sub>, e<sub>t</sub>, e<sub>k</sub>) which are processed through attention mechanisms (Att) and combined via dot products and summation. Different colored blocks represent user, item, relation, and entity embeddings. The diagram visually explains the model's architecture and the flow of information from user-item interactions to the final recommendation.](_page_5_Figure_0.jpeg)
<a id="ref-fig-3"></a>**Figure 3:** Relation-aware aggregation in client.

In each communication round, the server activates N clients. After receiving request items from those clients, server randomly samples a set of neighbors, denoted as S(t) ≜ {e|e ∼ N(t)}, for the request item t. Here, |S(v)| = K represents the fixed size when sampling, and N(t) represents immediate neighbors for item t. In our framework, S(v) is also referred to as the (single-layer) receptive field of item t. Repeat the above sampling several times to obtain G^i^ containing n iterations and then distribute it to the client along with the parameters θ, consisting of the model parameters θ^m^ and all embeddings of entities and relations in G^i^ denoted by θ~e~. Finally, it receives the local gradients g~i~ of these clients and aggregates them as follow:

$$
\overline{\mathbf{g}} = \frac{\sum_{n \in \mathcal{N}} |\mathcal{T}'_n| \cdot \tilde{\mathbf{g}}^n}{\sum_{n \in \mathcal{N}} |\mathcal{T}'_n|} \tag{5}
$$
<a id="eq-5"></a>

After aggregation, the server updates all parameters θ with gradient descent as:

$$
\theta^*= \theta - \eta \cdot \bar{g} \tag{6}
$$
<a id="eq-6"></a>

where η is the learning rate.

### 5 Privacy-Preserving Communication

### 5.1 User privacy

Within our proposed framework, user-related privacy pertains primarily to user embedding. Traditional embedding-based recommendation algorithms can derive both user and item embeddings and generate user-specific recommendations through a straightforward readout operation. However, user embeddings comprise the user's preference characteristics, which can lead to a compromise of their privacy. In the federated learning scenario where the server does not have access to the raw data, to avoid exposing user preferences directly to the server, it is obvious that we need to keep the user embeddings on the client side and isolate them from the server. Clients can simply protect user-related privacy by refraining from uploading user embeddings after the training phase.

### 5.2 Interaction privacy

The interaction between users and items is considered highly sensitive information, susceptible to potential leaks during two stages. Firstly, due to the large size of the knowledge graph for items and limited transmission bandwidth, it is not practical to distribute all embeddings to client similar to FedGNN and FedSoG. Instead, we aim to complete the entire training process through the limited distribution of embeddings. However, this presents a challenge in determining which embeddings should be distributed by the server. Server can not explicitly obtain the required embeddings, as this would mean that it has access to the client's real interaction item. Therefore, we need to obfuscate

the original interaction items to obtain encrypted request items, which can then be sent to the server to sample the corresponding subgraph required for training.

We have designed a *local differential privacy* (LDP) mechanism to generate request items from the interaction items. Specifically, user-item interaction for user u can be represented as a set {(t^i^ , y~ui~) | y~ui~ ∈ {0, 1}, i = 1, 2, . . . , n}. This collection contains |T | elements, each of which is a binary, the first of which is an item and the second is either 0 or 1, indicating whether the user interacted with the item. Let the query for the t^i^ be y~ui~, then the interaction can be privacy-preserving using an ϵ-LDP algorithm. The privacy budget ϵ indicates the maximum acceptable loss of privacy. Let the interaction for each item satisfy ϵ-LDP, and we have: for any item, keep the original interaction value with probability e^ϵ^ / (e^ϵ^+1) and invert it to another value with 1 / (e^ϵ^+1) (0,1 flipping).

A potential privacy concern with the widely used pseudo-labeling method in previous work is that the interacted item will always generate gradients, even if pseudo-labeling is used. Additionally, the pseudo-labeling method applied during the training phase does not effectively reduce the communication overhead associated with distributing embeddings. To address this issue, we first sample several non-interactive samples, mix them with real interaction items, and further obfuscate them by the above LDP method to achieve privacy protection.

### 5.3 Gradients privacy

Ensuring the privacy of users' sensitive information is a critical concern when maintaining a knowledge graph and updating the global model in a federated recommendation system. In each communication round, the server needs to aggregate gradients of entity embeddings, relational embeddings, and GNN models from different clients. However, it has been demonstrated, as exemplified by FedMF, that uploading users' gradients in consecutive steps can lead to the inadvertent exposure of sensitive data, such as users' ratings. Therefore, we need to obfuscate gradients to protect user privacy. However clients of recommendation systems, such as mobile devices, often have limited computational capabilities [[19]](#ref-19), and computationally intensive methods like homomorphic encryption may not be practical to implement on such devices. To tackle this, we employ LDP by injecting random noise into the local gradients before uploading them to the server. This approach effectively protects row gradients without compromising the accuracy of the model. Moreover, it helps ensure that the computational overhead remains manageable and within acceptable limits.

To be more specific, gives all gradients as g^n^ = {g~e~^n^ , g^m~^n^ } = ∂L^n^ / ∂θ , where L^n^ denotes loss of client n, the LDP is formulated as:

$$
\tilde{\mathbf{g}}_n = \text{clip}\left(\mathbf{g}_n, \delta\right) + \text{Laplacian}\left(0, \lambda\right) \tag{7}
$$

where g~n~ is the encrypted gradient, clip(x, δ) denotes the gradient clipping operation with a threshold δ to limit x and prevent the gradient from being too large, after which we add to the gradient a mean value of 0 and an intensity of λ of Laplacian noise, denoted by Laplacian (0, λ). This results in a ϵ-LDP, where the privacy budget ϵ is 2δ / λ.

## 4 Experiment

## 1 Datasets

In order to ensure the robustness of the algorithm, we aim to test the overall performance of the framework on a variety of datasets with different sizes, sparsity, and domains. Therefore, we have selected the following real-world datasets:

- MovieLens-20M [[20]](#ref-20) contains five-star ratings from MovieLens, a movie recommendation service, as of 2019. Each user in the dataset has provided a minimum of 20 ratings (ranging from 1 to 5) on the MovieLens website.
- Book-Crossing [[21]](#ref-21) contains user ratings (ranging from 0 to 10) of books extracted from the Book-Crossing community in 2004. In this dataset, a rating of 0 indicates an implicit interaction between the user and the book.

| | MovieLens-20M | Book-Crossing | Last.FM | |
|---|---|---|---|---|
| users | 138,159 | 19,676 | 1,872 | |
| items | 16,954 | 20,003 | 3,846 | |
| interactions | 13,501,622 | 172,576 | 42,346 | |
| entities | 102,569 | 25,787 | 9,366 | |
| relations | 32 | 18 | 60 | |
| KG triples | 499,474 | 60,787 | 15,518 | |
| K | 4 | 8 | 8 | |
| d | 32 | 64 | 16 | |
| H | 2 | 1 | 1 | |
| λ | 10^-7^ | 2 × 10^-5^ | 10^-4^ | |
| η | 2 × 10^-2^ | 2 × 10^-4^ | 5 × 10^-4^ | |
| N | 32768 | 64 | 32 | |

<a id="ref-tab-1"></a>**Table 1:** Dataset basic information and hyperparameters, notation is consistent with Algorithm [1](#ref-alg-1).

• Last.FM [[22]](#ref-22) contains musician listening recodes from the Last.FM music streaming service. We consider artists as items and the number of listens as ratings. In particular, we utilize the HetRec 2011 version in our study.

To adapt the dataset for the recommendation task in a federated learning environment, several steps are taken. Firstly, only the user-item interactions are retained from the original dataset, while other data are discarded. Then, the publicly available Microsoft Satori is utilized to create a knowledge graph by selecting triples with a confidence level greater than 0.9, where the tail corresponds to items in the dataset. Interactions, where the item is not present in the knowledge graph, are subsequently removed. Next, these three datasets are transformed into implicit feedback. We consider all artists listened to in Last.FM, all books with ratings present in book-cross, and all movies with ratings greater than or equal to 4 stars in MovieLens, as positive feedback. Conversely, items not meeting these criteria are treated as negative feedback. Lastly, since the original recommendation dataset already contains user information, each user's data is assigned to the corresponding client to generate a federated learning dataset. Details of the dataset are shown in Table [1](#ref-tab-1)

## 2 Baselines

We compare the proposed FEDRKG with the following baselines, in which the first two baselines are KG-free while the rest are all KG-aware methods. Hyper-parameter settings for baselines are introduced in the next subsection.

- SVD [[23]](#ref-23) is a classical CF recommendation algorithm based on matrix decomposition. Here we use an unbiased version.
- LibFM [[24]](#ref-24) is a method based on Factorization Machines that captures the similarity between features
- PER [[25]](#ref-25) is an algorithm based on a personalized attention mechanism and constructs a Meta-path between users and items through a heterogeneous graph (KG).
- CKE [[26]](#ref-26) is a knowledge graph-based collaborative embedding recommendation algorithm that combines data from CF and other modalities.
- RippleNet [[27]](#ref-27) is a memory-network-like approach that simulates and exploits the ripple effect between users and items to propagate information on the knowledge graph
- KGCN [[11]](#ref-11) is a KG-based method, that achieves efficient recommendations by merging KG and CF data.
- FedMF [[6]](#ref-6) is a recommendation algorithm based on matrix decomposition while protecting privacy through an encryption mechanism.
- FedGNN [[7]](#ref-7) is a GNN-based recommendation algorithm that uses homomorphic encryption for aggregation and protects the original gradient by differential privacy and pseudo-labeling.

<a id="ref-tab-2"></a>**Table 2:** Results for CRT prediction. KGCN achieves the best AUC among the first five centralized learning methods. Our method performs best in the next three federal learning methods, while the gap with KGCN is acceptable.

| Model | MovieLens-20M | | Book-Crossing | | Last.FM | |
|---|---|---|---|---|---|---|
| | AUC | F1 | AUC | F1 | AUC | F1 |
| SVD | 0.952(±0.013) | 0.909(±0.014) | 0.665(±0.058) | 0.628(±0.051) | 0.760(±0.026) | 0.688(±0.022) |
| LibFM | 0.960(±0.018) | 0.907(±0.024) | 0.692(±0.046) | 0.619(±0.063) | 0.779(±0.019) | 0.711(±0.011) |
| PER | 0.824(±0.119) | 0.780(±0.121) | 0.611(±0.101) | 0.557(±0.100) | 0.627(±0.125) | 0.593(±0.107) |
| CKE | 0.918(±0.050) | 0.866(±0.056) | 0.673(±0.057) | 0.607(±0.055) | 0.739(±0.044) | 0.669(±0.046) |
| RippleNet | 0.964(±0.010) | 0.909(±0.020) | 0.712(±0.023) | 0.648(±0.032) | 0.777(±0.016) | 0.699(±0.015) |
| KGCN | 0.978(±0.002) | 0.932(±0.001) | 0.738(±0.003) | 0.688(±0.006) | 0.794(±0.002) | 0.719(±0.003) |
| FedMF | 0.865(±0.012) | 0.852(±0.015) | 0.657(±0.039) | 0.605(±0.060) | 0.720(±0.018) | 0.660(±0.013) |
| FedGNN | 0.939(±0.011) | 0.891(±0.021) | 0.671(±0.024) | 0.620(±0.037) | 0.753(±0.014) | 0.681(±0.028) |
| FEDRKG | 0.970(±0.002) | 0.919(±0.002) | 0.724(±0.004) | 0.667(±0.006) | 0.785(±0.004) | 0.708(±0.002) |

### 3 Experimental Settings

Table [2](#ref-tab-2) shows the hyperparameter for the experiments. We split the datasets into training, validation, and testing sets in a 6:2:2 ratio. AUC and F1 scores are used as evaluation metrics for *click-through rate* (CTR) prediction.

For the Last.FM, Book-Crossing, and MovieLens-20M datasets, the SVD method is applied with imensions (8, 8, 8) and learning rates (0.1, 0.5, 0.5). For LibFM, the dimensions are (8, 1, 1). PER utilizes the user-item-attribute-item meta-path, with dimensions (64, 128, 64) and learning rates (0.1, 0.5, 0.5). The learning rates for KG in CKE are (0.1, 0.1, 0.1), while the dimensions are (16, 4, 8) and the H values are (3, 3, 2). RippleNet's dimensions are (16, 4, 8), H values are (3, 3, 2), learning rates are (0.005, 0.001, 0.01), regularization parameters λ^1^ are (10^-5^ , 10^-5^ , 10^-6^ ), and λ^2^ are (0.02, 0.01, 0.01). Other hyperparameters remain the same as in the original papers, and the federated learning settings are consistent with this paper.

## 4 Overall Comparison

We conduct a comprehensive comparison of multiple models under various settings. Given the dataset's specific characteristics, only including knowledge graphs and user-item graphs, many federated learning algorithms simplify to FedGNN in this dataset. Therefore, we select FedGNN and FedMF as the baseline methods, representing GNN and matrix decomposition approaches in federated learning. The experimental results for CTR prediction are presented in Table [2](#ref-tab-2), while Fig. [4](#ref-fig-4) illustrates the outcomes of top-k recommendation. Based on those results, we draw the following conclusions:

- On the one hand, GNN-based algorithms, such as KGCN and FEDRKG, outperform matrix decomposition-based algorithms like SVD and FedMF. This is due to the superior performance of GNNs in automatically capturing user preferences and enabling the spreading of user or item embeddings to neighboring nodes. On the other hand, algorithms that require manual design such as meta-paths for PER and *knowledge graph embedding* (KGE) method for CKE, often underperform due to the complexity of graph data.
- The experimental results consistently demonstrate that the appropriate utilization of additional side information can significantly improve the accuracy of recommendation systems. For example, KGCN and RippleNet outperform other centralized algorithms regarding both AUC and F1 metrics, while FEDRKG, as a knowledge graph-based algorithm, performs best in federated learning. However, it should be noted that not all methods that leverage side information deliver satisfactory outcomes. This holds true for methods like PER and CKE, which encounter difficulties in effectively harnessing side information.
- Knowledge graphs are well-suited for integration into recommendation systems as side information, especially using GNNs, given their inherent graph structure and the ability to combine multi-domain knowledge. Algorithms incorporating relation-aware aggregation, such as KGCN and FEDRKG, achieve the best performance in their respective settings, confirming the effectiveness of introducing relational attention mechanisms.

Overall, our framework outperforms existing federated learning algorithms and achieves competitive performance compared to centralized algorithms.

![The image contains three line graphs comparing the Recall@K performance of several recommendation algorithms (PER, CKE, LibFM, RippleNet, KGCN, FedMF, FedGNN, FedRKG) across different datasets: MovieLens 20M, Book Crossing, and LastFM. Each graph shows Recall@K plotted against varying values of K, illustrating how recall changes with the number of recommendations. The purpose is to compare the effectiveness of these algorithms in terms of recommendation accuracy.](_page_9_Figure_1.jpeg)
<a id="ref-fig-4"></a>(a) MovieLens-20M (b) Book-Crossing (c) Last.FM **Figure 4:** Results for top-K recommendation. The dashed line represents centralized learning, while the solid line represents federated learning. Our method surpasses all federated baselines and, furthermore, achieves competitive results compared to centralized learning.

### 5 Sensitivity Analysis

### 5.1 Activated client number

In general, a smaller number of activated clients in each training round will speed up the model convergence and conversely better capture the global user data distribution. We test the algorithm on three datasets with three different numbers of activation clients, and the results are shown in the figure above. Probably due to the sparse data and a large number of clients, a small adjustment has a limited impact on the final results and the Last.FM and Book-Crossing datasets both show a small decrease in AUC when 64 clients are activated.

### 5.2 Receptive field depth

By testing different receptive field depths, we note that an excessive receptive field reduces model prediction accuracy. As data sparsity decreases, better performance needs a larger receptive field, while a one-layer perceptual region is sufficient to achieve better performance on those sparse data sets.

![The image presents two bar charts comparing the Area Under the Curve (AUC) performance metric across three datasets (Movielens-20M, Book-Crossing, Last.FM) for a machine learning model. The left chart shows AUC variation with the number of activated clients (1x, 2x, 4x), while the right chart displays AUC changes based on receptive field depth (1-4). The charts illustrate the model's performance sensitivity to these hyperparameters across different datasets.](_page_9_Figure_8.jpeg)
<a id="ref-fig-5"></a>**Figure 5:** Sensitivity analysis of activated clients and receptive field depth.

### 5.3 Interaction item protection

We introduce new interaction record protection and assess diverse flipping rates, with corresponding results depicted in Fig. [6](#ref-fig-6). Generally, integrating privacy-preserving mechanisms often diminishes recommendation accuracy. However given limited client-side graph data, our scenario tends to induce model overfitting. Hence, proper regularization effectively enhances recommendation accuracy

![The image contains three line graphs displaying Area Under the Curve (AUC) values against "flipping rate" for three different datasets: MovieLens-20M, Book-Crossing, and Last.FM. Each graph shows how AUC, a measure of model performance, varies with the flipping rate, likely representing a parameter influencing data augmentation or model training. The purpose is to illustrate the effect of this parameter on model performance across different datasets.](_page_10_Figure_0.jpeg)
<a id="ref-fig-6"></a>**Figure 6:** Effect of flipping rate on AUC.

and privacy protection. Notably, excessive flip rates can compromise system performance despite heightened privacy. Our experiments indicate a balance between accuracy and privacy at a flipping rate of 0.1.

## 5 Conclusion

This paper introduces a novel federated learning framework, FEDRKG, which employs GNN for recommendation tasks. Our approach integrates KG information while upholding user privacy. The limitation here is the absence of user connections, and our forthcoming focus is on improving the efficiency and interpretability of utilizing existing user connections without introducing new private data. Specifically, a server-side KG is created from public item data, maintaining relevant embeddings. The client conceals local interaction items and requests server training data. The server samples a KG subgraph and distributes it with the GNN model to the client. The client then expands its user-item graph with the KG subgraph for training, uploading the gradient for server aggregation. Our framework creates higher-order interactions without extra privacy data, relying solely on public information for KG. Sampled KG subgraphs enhance local training by capturing interactions between users and items without direct links. We employ LDP and pseudo-labeling to protect privacy and reduce overhead by requesting partial data. Gradients are encrypted using LDP for user preference protection and local user embedding storage. Experimental results on three datasets demonstrate our framework's superiority over SOTA federated learning recommendation methods. It also performs competitively against centralized algorithms while preserving privacy.

## 0.1 Acknowledgements

This work is supported by the National Key Research and Development Program of China under Grant No.2021YFB1714600 and the National Natural Science Foundation of China under Grant No.62072204 and No.62032008. The computation is completed in the HPC Platform of Huazhong University of Science and Technology and supported by the National Supercomputing Center in Zhengzhou.

## References

- <a id="ref-1"></a>[1] Xiang Wang, Xiangnan He, Yixin Cao, Meng Liu, and Tat-Seng Chua. Kgat: Knowledge graph attention network for recommendation. In *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, KDD*, pages 950–958, 2019.
- <a id="ref-2"></a>[2] Qingyu Guo, Fuzhen Zhuang, Chuan Qin, Hengshu Zhu, Xing Xie, Hui Xiong, and Qing He. A survey on knowledge graph-based recommender systems. *IEEE Transactions on Knowledge and Data Engineering*, 34(8):3549–3568, 2020.
- <a id="ref-3"></a>[3] Jie Zhou, Ganqu Cui, Shengding Hu, Zhengyan Zhang, Cheng Yang, Zhiyuan Liu, Lifeng Wang, Changcheng Li, and Maosong Sun. Graph neural networks: A review of methods and applications. *AI Open*, 1:57–81, 2020.
- <a id="ref-4"></a>[4] Shiwen Wu, Fei Sun, Wentao Zhang, Xu Xie, and Bin Cui. Graph neural networks in recommender systems: a survey. *ACM Computing Surveys*, 55(5):1–37, 2022.
- <a id="ref-5"></a>[5] Paul Voigt and Axel Von dem Bussche. The EU general data protection regulation (GDPR). *A Practical Guide, 1st Ed., Cham: Springer International Publishing*, 10(3152676):10–5555, 2017.
- <a id="ref-6"></a>[6] Di Chai, Leye Wang, Kai Chen, and Qiang Yang. Secure federated matrix factorization. *IEEE Intelligent Systems*, 36(5):11–20, 2020.
- <a id="ref-7"></a>[7] Chuhan Wu, Fangzhao Wu, Yang Cao, Yongfeng Huang, and Xing Xie. FedGNN: Federated graph neural network for privacy-preserving recommendation. *arXiv preprint arXiv:2102.04925*, 2021.
- <a id="ref-8"></a>[8] Zhiwei Liu, Liangwei Yang, Ziwei Fan, Hao Peng, and Philip S Yu. Federated social recommendation with graph neural network. *ACM Transactions on Intelligent Systems and Technology*, 13(4):1–24, 2022.
- <a id="ref-9"></a>[9] Ze Wang, Guangyan Lin, Huobin Tan, Qinghong Chen, and Xiyang Liu. Ckan: collaborative knowledge-aware attentive network for recommender systems. In *Proceedings of the 43rd International ACM SIGIR Conference on Research and Development in Information Retrieval, SIGIR*, pages 219–228, 2020.
- <a id="ref-10"></a>[10] Rui Sun, Xuezhi Cao, Yan Zhao, Junchen Wan, Kun Zhou, Fuzheng Zhang, Zhongyuan Wang, and Kai Zheng. Multi-modal knowledge graphs for recommender systems. In *Proceedings of the 29th ACM International Conference on Information & Knowledge Managemen, CIKM*, pages 1405–1414, 2020.
- <a id="ref-11"></a>[11] Hongwei Wang, Miao Zhao, Xing Xie, Wenjie Li, and Minyi Guo. Knowledge graph convolutional networks for recommender systems. In *Proceedings of the World Wide Web Conference, WWW*, pages 3307–3313, 2019.
- <a id="ref-12"></a>[12] Hongwei Wang, Fuzheng Zhang, Mengdi Zhang, Jure Leskovec, Miao Zhao, Wenjie Li, and Zhongyuan Wang. Knowledge-aware graph neural networks with label smoothness regularization for recommender systems. In *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, KDD*, pages 968–977, 2019.
- <a id="ref-13"></a>[13] Hai Jin, Dongshan Bai, Dezhong Yao, Yutong Dai, Lin Gu, Chen Yu, and Lichao Sun. Personalized edge intelligence via federated self-knowledge distillation. *IEEE Transactions on Parallel and Distributed Systems*, 34(2):567–580, 2023.
- <a id="ref-14"></a>[14] Ke Zhang, Carl Yang, Xiaoxiao Li, Lichao Sun, and Siu Ming Yiu. Subgraph federated learning with missing neighbor generation. In *Proceedings of the Annual Conference on Neural Information Processing Systems, NeurIPS*, volume 34, pages 6671–6682, 2021.
- <a id="ref-15"></a>[15] Hao Peng, Haoran Li, Yangqiu Song, Vincent Zheng, and Jianxin Li. Differentially private federated knowledge graphs embedding. In *Proceedings of the 30th ACM International Conference on Information & Knowledge Management, CIKM*, pages 1416–1425, 2021.
- <a id="ref-16"></a>[16] Muhammad Ammad-Ud-Din, Elena Ivannikova, Suleiman A Khan, Were Oyomno, Qiang Fu, Kuan Eeik Tan, and Adrian Flanagan. Federated collaborative filtering for privacy-preserving personalized recommendation system. *arXiv preprint arXiv:1901.09888*, 2019.
- <a id="ref-17"></a>[17] Guoren Wang, Yue Zeng, Rong-Hua Li, Hongchao Qin, Xuanhua Shi, Yubin Xia, Xuequn Shang, and Liang Hong. Temporal graph cube. *IEEE Transactions on Knowledge and Data Engineering*, pages 1–15, 2023.
- <a id="ref-18"></a>[18] Wenming Cao, Canta Zheng, Zhiyue Yan, and Weixin Xie. Geometric deep learning: progress, applications and challenges. *Science China Information Sciences*, 65(2):126101, 2022.
- <a id="ref-19"></a>[19] Yuanyishu Tian, Yao Wan, Lingjuan Lyu, Dezhong Yao, Hai Jin, and Lichao Sun. FedBERT: When federated learning meets pre-training. *ACM Transactions on Intelligent Systems and Technology*, 13(4):1–26, 2022.
- <a id="ref-20"></a>[20] F Maxwell Harper and Joseph A Konstan. The movielens datasets: History and context. *ACM Transactions on Interactive Intelligent Systems*, 5(4):19:1–19:19, 2016.
- <a id="ref-21"></a>[21] Cai-Nicolas Ziegler, Sean M McNee, Joseph A Konstan, and Georg Lausen. Improving recommendation lists through topic diversification. In *Proceedings of the World Wide Web Conference, WWW*, pages 22–32, 2005.
- <a id="ref-22"></a>[22] Iván Cantador, Peter Brusilovsky, and Tsvi Kuflik. Second workshop on information heterogeneity and fusion in recommender systems (HetRec2011). In *Proceedings of the 2011 ACM Conference on Recommender Systems, RecSys*, pages 387–388, 2011.
- <a id="ref-23"></a>[23] Yehuda Koren. Factorization meets the neighborhood: a multifaceted collaborative filtering model. In *Proceedings of the 14th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, KDD*, pages 426–434, 2008.
- <a id="ref-24"></a>[24] Steffen Rendle. Factorization machines with libfm. *ACM Transactions on Intelligent Systems and Technology*, 3(3):1–22, 2012.
- <a id="ref-25"></a>[25] Xiao Yu, Xiang Ren, Yizhou Sun, Quanquan Gu, Bradley Sturt, Urvashi Khandelwal, Brandon Norick, and Jiawei Han. Personalized entity recommendation: A heterogeneous information network approach. In *Proceedings of the 7th ACM International Conference on Web Search and Data Mining, WSDM*, pages 283–292, 2014.
- <a id="ref-26"></a>[26] Fuzheng Zhang, Nicholas Jing Yuan, Defu Lian, Xing Xie, and Wei-Ying Ma. Collaborative knowledge base embedding for recommender systems. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, KDD*, pages 353–362, 2016.
- <a id="ref-27"></a>[27] Hongwei Wang, Fuzheng Zhang, Jialin Wang, Miao Zhao, Wenjie Li, Xing Xie, and Minyi Guo. Ripplenet: Propagating user preferences on the knowledge graph for recommender systems. In *Proceedings of the 27th ACM International Conference on Information and Knowledge Management, CIKM*, pages 417–426, 2018.

## Metadata Summary
### Research Context
- **Research Question**: How can federated learning and knowledge graphs be combined to create privacy-preserving recommendation systems that maintain high accuracy while protecting user data?
- **Methodology**: Federated learning framework with local differential privacy, relation-aware GNN model, experiments on three real-world datasets, comparison with centralized and federated baselines.
- **Key Findings**: Achieved 4% average accuracy improvement over federated learning baselines while maintaining competitive performance with centralized algorithms, demonstrated effective privacy preservation through LDP and pseudo-labeling techniques.

### Analysis
- **Limitations**: Relies on publicly available item information for knowledge graph construction, potential computational overhead from privacy mechanisms, limited evaluation to specific recommendation datasets.
- **Future Work**: Explore advanced privacy preservation methods, expand knowledge graph relationship types, evaluate scalability with larger user bases, investigate integration with additional data modalities.