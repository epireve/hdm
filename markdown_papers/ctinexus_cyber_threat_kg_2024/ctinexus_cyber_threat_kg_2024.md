---
cite_key: "ctinexus_cyber_threat_kg_2024"
title: "<span id=\"page-0-0\"></span>Knowledge-enhanced Multi-perspective Video Representation Learning for Scene Recognition"
year: 2016
date_processed: "2025-07-02"
phase2_processed: true
original_folder: "ctinexus_cyber_threat_kg_2024"
images_total: 2
images_kept: 2
images_removed: 0
---

# <span id="page-0-0"></span>Knowledge-enhanced Multi-perspective Video Representation Learning for Scene Recognition

*Xuzheng Yu*<sup>1</sup>,<sup>2</sup> , *Chen Jiang*<sup>2</sup> , *Wei Zhang*<sup>2</sup> , *Tian Gan*<sup>1</sup> *Linlin Chao*<sup>2</sup> , *Jianan Zhao*<sup>2</sup> , *Yuan Cheng*<sup>2</sup> , *Qingpei Guo*<sup>2</sup> , *Wei Chu*<sup>2</sup> <sup>1</sup>Shandong University <sup>2</sup>Ant Group

# Abstract

*With the explosive growth of video data in real-world applications, a comprehensive representation of videos becomes increasingly important. In this paper, we address the problem of video scene recognition, whose goal is to learn a high-level video representation to classify scenes in videos. Due to the diversity and complexity of video contents in realistic scenarios, this task remains a challenge. Most existing works identify scenes for videos only from visual or textual information in a temporal perspective, ignoring the valuable information hidden in single frames, while several earlier studies only recognize scenes for separate images in a non-temporal perspective. We argue that these two perspectives are both meaningful for this task and complementary to each other, meanwhile, external introduced knowledge can also promote the comprehension of videos. We propose a novel two-stream framework to model video representations from multiple perspectives, i.e. temporal and non-temporal perspectives, and integrate the two perspectives in an end-to-end manner by self-distillation. Besides, we design a knowledge-enhanced feature fusion and label prediction method that contributes to naturally introducing knowledge into the task of video scene recognition. Experiments conducted on a real-world dataset demonstrate the effectiveness of our proposed method.*# INTRODUCTION

With the explosive growth of video data in real-world applications, analysis and reasoning on video content become increasingly important. One important branch is scene recognition from videos, which is to identify scene labels based on the content of videos.

Video understanding itself is complex, including the diversity and redundancy of video contents, and the inherent gap among video multi-modal information. Therefore, the first intuitive challenge is how to effectively and

![](_page_0_Picture_7.jpeg)

Figure 1. An illustration of the task of scene recognition.

comprehensively understand the contents of videos for this task. Based on a deep insight of the characteristics of video scene recognition, it is notable that there exists multiperspective information, including global vs local, temporal vs non-temporal, visual vs textural, etc. However, the diversity and discreteness of multiple information make it difficult to distinguish between useful and useless information. Meanwhile, we note that knowledge enhancement has been proven effective in many tasks, largely due to its modeling distinctiveness that contributes to constructing and reweighing a relation among multi-perspective information. Inspired by this, we hope to introduce the knowledge enhancement into the task of video scene recognition to achieve an improvement. However, due to the conflict between the domain specificity and generality of knowledge enhancement, and the lack of general and excellent ways of fusing multi-perspective information with knowledge in the field of video understanding, how to leverage the external knowledge in our model is the second challenge. Moreover, knowledge-enhanced models are usually large-scale with low computational efficiency, and we expect to balance the efficiency and the additional time-consuming of introducing knowledge. Hence, it brings the third challenge that how to make the model as efficient as possible.

In recent years, there has been an increasing amount of literature on video understanding [\[6,](#page-8-0) [15,](#page-8-1) [27\]](#page-9-0). These works are usually based on spatio-temporal relationship modeling, and build models for video from multiple perspectives. <span id="page-1-0"></span>However, due to paying too much attention to the temporal information of videos, these works may ignore or lose the non-temporal information to varying degrees. In addition, several studies have revealed that external knowledge is beneficial for obtaining better performance [\[9,](#page-8-2) [10,](#page-8-3) [25\]](#page-9-1). Specifically, these studies focus on linking linguistic tokens to entities in knowledge graphs, and enhancing reasoning based on the neighborhood of entities, while lacking attention to vision due to scarce general visual entity linking. Meanwhile, numerous studies have also focused on the reasoning efficiency [\[5,](#page-8-4) [11,](#page-8-5) [15\]](#page-8-1). These studies employ various methods to distill models, which give us great inspiration.

In this paper, we propose a novel two-stream framework to learn video representations from multiple perspectives. Additionally, we design a knowledge-enhanced feature fusion method to integrate the multi-perspective information, which makes it natural to introduce knowledge into label recognition tasks. Finally, the application of knowledge distillation is employed to fuse the multiple representations, hoping to achieve high performance with low computational costs.

Our main contributions are as follows:

- We propose a novel two-stream framework to model videos from temporal and non-temporal perspectives, and integrate the two perspectives through knowledge distillation in order to better comprehend videos while maintaining efficiency.
- We design a knowledge-enhanced feature fusion method to leverage external knowledge to better integrate features non-temporally, and introduce knowledge into the scene label prediction task naturally while additionally gaining label scalability as a byproduct.
- We quantitatively evaluated our model on a real-world dataset. Experimental results demonstrate the effectiveness of our model.

The rest of this paper is structured as follows. In Section 2, we briefly review the related literature. In Section 3, we detail our proposed model, followed by experimental results and analyses in Section 4. We finally conclude the work in Section 5.

# RELATED WORK

In this section, we mainly review the studies that are most related to our work, including video representation, scene recognition, and knowledge-enhanced learning.

## 1. Video Representation

Obtaining video representation is essential and indispensable for video analytics, while for obtaining video representation, spatio-temporal modeling of videos is an important step [\[16,](#page-8-6) [17,](#page-8-7) [26\]](#page-9-2). There are many attempts have been made to model videos from spatial and temporal perspectives [\[6,](#page-8-0) [15,](#page-8-1) [19,](#page-8-8) [29\]](#page-9-3). Hu*et al.*[\[6\]](#page-8-0) proposed a hierarchical temporal method to construct the temporal structure at frame-level and object-level successively, and extract pivotal information effectively from global to local, which improves the model capacity of recognizing fine-grained objects and actions. Pan*et al.*[\[15\]](#page-8-1) proposed a novel spatiotemporal graph network to explicitly exploit the spatiotemporal object interaction, which is crucial for video understanding and description. Besides, Shi*et al.*[\[19\]](#page-8-8) proposed to learn the semantic concepts explicitly and design a temporal alignment mechanism to better align the video and transcript. These studies give us a lot of inspiration, however, they are too focused on the impact of temporal information on video comprehension due to task constraints, while ignoring non-temporal information to some extent.

## 2. Scene Recognition

Scene recognition is a task to develop robust and reliable models for the automatic recognition of what scenes are described by visual information [\[13\]](#page-8-9). Early research on scene recognition mainly focus on separate images [\[30\]](#page-9-4), while scholars' attention naturally turn towards scene recognition from videos [\[7,](#page-8-10) [28\]](#page-9-5). Zhou*et al.*[\[30\]](#page-9-4) described the Places Database, and provided scene recognition convolutional neural networks as baselines. Jiang*et al.*[\[7\]](#page-8-10) proposed a novel framework, which jointly utilized multi-platform data, object-scene deep features and the hierarchical venue structure prior for scene category prediction from videos. Zhang*et al.*[\[28\]](#page-9-5) proposed a Hybrid-Attention Enhanced Two-Stream Fusion Network for the task of video scene label prediction, and develops a novel Global-Local Attention Module, which can be inserted into neural networks to generate enhanced visual features from video content. Most recent studies identify scenes only from visual or textual information in a temporal perspective, ignoring the valuable information hidden in single frames, while several earlier studies only recognize scenes for separate images in nontemporal perspective. In this paper, we argue these two perspectives are both meaningful for this task and complementary to each other.

## 3. Knowledge-enhanced Learning

Knowledge-enhanced learning is increasingly attracting more attention from researchers in recent years. To make models better mine the hidden information in data, many scholars tried to introduce different types of additional information into their methods [\[5,](#page-8-4)[9,](#page-8-2)[11,](#page-8-5)[15](#page-8-1)[,25](#page-9-1)[,27,](#page-9-0)[31\]](#page-9-6). This additional information is considered as knowledge, and is usually related to knowledge graphs [\[9,](#page-8-2) [25\]](#page-9-1), transferred knowledge [\[5,](#page-8-4)[11,](#page-8-5)[15\]](#page-8-1), and specifically defined knowledge [\[27,](#page-9-0)[31\]](#page-9-6).

<span id="page-2-0"></span>When it comes to knowledge, scholars often refer to knowledge graphs and the embedding representations of the nodes and edges in knowledge graphs. Several studies [\[9,](#page-8-2)[10,](#page-8-3)[20,](#page-8-11)[24,](#page-8-12)[25\]](#page-9-1) have been carried out on knowledge graphs and verified that the pretrained embeddings from knowledge graphs are helpful to reasoning. Liu*et al.*[\[9\]](#page-8-2) proposed a knowledge-enabled language representation model with knowledge graphs, in which triples are injected into the sentences as domain knowledge. Xiong*et al.* [\[25\]](#page-9-1) introduced a novel method to represent queries and documents in the entity space, and rank documents based on their semantic relatedness to queries. These studies fully explore the node embeddings and edges in knowledge graphs, while they mainly focus on text modality. And in our work, we leverage the pretrained knowledge embeddings to guide cross-modality fusion instead of single-modal reasoning.

Compared with knowledge graphs focusing on mining the valuable information hidden in nodes and edges in themselves, transferred knowledge focus on the transmission and sharing of known valuable information (*e.g.,*distributions). The transferred knowledge is usually related to the pretrained models [\[3,](#page-8-13)[4\]](#page-8-14), especially pretrained language models [\[3\]](#page-8-13), and the transferred distributions are common in the task of knowledge distillation [\[5,](#page-8-4) [11,](#page-8-5) [15,](#page-8-1) [29\]](#page-9-3). Pan*et al.*[\[15\]](#page-8-1) proposed a novel spatio-temporal graph network and designed a two-branch framework with an object-aware knowledge distillation mechanism. Zhang*et al.*[\[29\]](#page-9-3) proposed a novel teacher-recommended learning method that introduces external language model to guide the main model to learn abundant linguistic knowledge. In these methods, for better reasoning, knowledge is transferred between multiple modules that perform the same task in different ways, and this idea is adopted in our work.

The specifically defined knowledge in certain scenarios also appears in numerous recent studies [\[27,](#page-9-0) [31\]](#page-9-6). Zhang*et al.*[\[27\]](#page-9-0) proposed to narrate the user-preferred product characteristics depicted in user-generated product videos, and proposed a novel framework to perform knowledgeenhanced spatio-temporal inference on product-oriented video graphs. Zhu*et al.* [\[31\]](#page-9-6) introduced knowledge modality in multi-modal pretraining to correct the noise and supplement the missing image and text modalities. The aforementioned methods introduce several types of additional associated information, and leverage the specifically defined knowledge to guide the learning of models. However, the introduced knowledge also brings barriers to these methods, because the knowledge and methods usually target specific datasets, and are not easy to be extended to other tasks. In our work, though we similarly introduce additional specifically defined information (*i.e.,* keywords) as knowledge, yet the introduced keywords are easily obtained from text descriptions, making our method extendable and adjustable.

# OUR PROPOSED METHOD

## 1. Overview

### 1.1 Problem setting.

Before describing our method, we briefly introduce the problem setting first. Formally, let V, L, and G denote the set of videos, the set of scene labels, and the external knowledge graph respectively. Each video v ∈ V contains textual descriptions t and a sequence of RGB frames. Scene labels L belong to a two-level scene hierarchy, and each video is associated with a set of paths P<sup>v</sup> = {p1, p2, ..., p|Pv<sup>|</sup>} on this hierarchy, where p<sup>l</sup> = {p 1 l , p<sup>2</sup> l | p 1 l , p<sup>2</sup> <sup>l</sup> ∈ L} for p<sup>l</sup> ∈ Pv, and p 1 l is the parent scene label of p 2 l . Our goal is to learn a video scene recognition model, which could recognize suitable scene labels p based on the video frame sequences and the associated text descriptions.

#### 1.2 Model overview.

Temporal information can well describe what happens in videos, while non-temporal information can well reflect several moments in videos. We argue that these two perspectives are both meaningful for this task and complementary to each other. Meanwhile, external introduced knowledge can also promote the comprehension of videos. In order to make full use of these kinds of information, we propose a novel two-stream framework to model video representations from the two perspectives, i.e. temporal and nontemporal perspectives, and integrate these two perspectives in an end-to-end manner by self-distillation. Besides, in the non-temporal module, we design a knowledge-enhanced feature fusion and label prediction method that contributes to naturally introducing knowledge into the task of video scene recognition.

## 2. Temporal Feature Learning

The temporal feature learning module is used to model videos from a temporal perspective, including temporal modeling and hierarchical multi-label prediction.

### 2.1 Temporal modeling.

In this module, we employ Multimodal Bitransformers [\[8\]](#page-8-15) as the backbone, and utilize Transformer [\[23\]](#page-8-16) that is effective in various tasks in recent years as the feature encoder. Specifically, for each video v, we uniformly sample N<sup>f</sup> frames as keyframes, and utilized the pretrained ResNet [\[4\]](#page-8-14) to extract the frame-level 2D feature f 2D <sup>j</sup> of each keyframe, where j ∈ [1, N<sup>f</sup> ]. We then collect N<sup>c</sup> consecutive frames with each sampled keyframe as center, and utilized the pretrained I3D [\[2\]](#page-8-17) to extract the frame-level 3D features f 3D j . For the associated textual descriptions, we utilize the pre-

<span id="page-3-0"></span>![](_page_3_Figure_0.jpeg)

Figure 2. An overview of our proposed framework for scene recognition using knowledge-enhanced multi-perspective video representation learning.

e

<sup>t</sup> video as follows:

trained BERT [\[3\]](#page-8-13) to extract the video-level textual features f text .

j

f

j

After extracting the aforementioned features, we concatenate them to obatin the frame-level global features gframe and local features f lframe as follows:

$$
\boldsymbol{e}_{j}^{\text{con},\tau}=(\boldsymbol{f}_{j}^{\text{2D}}\oplus\boldsymbol{f}_{j}^{\text{3D}}\oplus\boldsymbol{f}^{\text{text}}),\qquad(1)
$$

$$
\boldsymbol{e}_{j}^{\text{ref}.\tau} = \boldsymbol{W}_{2}^{\tau} \,\delta(\boldsymbol{W}_{1}^{\tau} \boldsymbol{e}_{j}^{\text{con}.\tau} + \boldsymbol{b}_{1}^{\tau}) + \boldsymbol{b}_{2}^{\tau},\tag{2}
$$

$$
\boldsymbol{f}_{j}^{\tau} = Norm(Dropout(\boldsymbol{e}_{j}^{\text{ref}.\tau}) + \boldsymbol{W}_{3}^{\tau}\boldsymbol{e}_{j}^{\text{con}.\tau}), \quad (3)
$$

$$
\tau \in \{\text{gframe}, \text{Iframe}\},\
$$

where ⊕ indicates concatenation, e con j and e ref j indicate the concatenated and the refined features respectively, δ(·) indicates the activation function, W1, W2, b<sup>1</sup> and b<sup>2</sup> denote the weight matrices and bias vectors in fully connected layers, W<sup>3</sup> denotes the residual transformation matrices, and Norm refers to the operation of layer normalization.

In order to better model the temporal aspects of video, we send the special tag [CLS] and the frame-level global features f gframe j into the self-attention layers of the Transformer encoder with position embeddings. After the encoding, the Transformer encoder generates a sequence of outputs, and we denote the generated output corresponding to the special tag [CLS] as the video-level temporal features

$$
O = [o0, o1, ..., oNf]
$$

= Transformer([[*CLS*] + *pos*<sub>0</sub>, (4)
$$
f_1^{\text{frame}} + pos_1, ..., f_{N_f}^{\text{frame}} + pos_{N_f}
$$
]),
$$
e^{\text{t video}} = o_0,
$$
 (5)

where O indicates the output sequence, pos<sup>j</sup> ( j ∈ [0, N<sup>f</sup> ] ) indicates the position embedding, and N<sup>f</sup> denotes the number of sampled keyframes.

#### 2.2 Hierarchical multi-label prediction.

After obtaining the video-level temporal features e t video , we employ multi-layer perceptrons to obtain the basic scores of labels score′<sup>t</sup> i for the i th-level scene hierarchical layer. Besides, for each label q<sup>1</sup> in the 1 st-level scene hierarchical layer, we make the refined scores score<sup>t</sup> q1 of it the same as its basic score. And for each label q<sup>2</sup> in the 2 rd-level layer, we obtain the refined scores score<sup>t</sup> q2 of it by summing the basic scores of itself and its parent label µ<sup>q</sup><sup>2</sup>

<span id="page-4-0"></span>as follows:

$$
score'_{i}^{\dagger} = W_{5}^{i} \delta(W_{4}^{i} e^{t \text{-video}} + b_{4}^{i}) + b_{5}^{i}, \qquad (6)
$$

$$
score_{q_1}^{\mathbf{t}} = score_{1,q_1}^{\prime \mathbf{t}},\qquad(7)
$$

$$
score_{q_2}^t = score'_{1,\mu_{q_2}}^t + score'_{2,q_2},
$$
 (8)

where score<sup>t</sup> <sup>i</sup> ∈ R |Li| and |L<sup>i</sup> | denote the scores and the number of the labels in the i th-level scene hierarchical layer respectively, µ<sup>θ</sup> denotes the parent label of θ in scene hierarchy, δ(·) indicates the activation function, W<sup>i</sup> <sup>4</sup> ∈ R <sup>d</sup>emb×demb and W<sup>i</sup> <sup>5</sup> ∈ R |Li|×demb denote weight matrices in fully connected layers, b i <sup>4</sup> ∈ R <sup>d</sup>emb and b i <sup>5</sup> ∈ R |Li| denote bias vectors, and demb denotes the dimensions of the video-level temporal features.

And then we employ the Multi-label Cross Entropy Loss [\[21,](#page-8-18) [22\]](#page-8-19) to calculate the loss for the i th-level scene hierarchical layer as follows:

$$
\mathcal{J}_i^{\text{t}} = \frac{1}{|\mathcal{V}|} \sum_{v \in \mathcal{V}} \{ \log[1 + \sum_{q_i^- \notin \mathcal{P}_v^i} \exp(\text{score}_{q_i^-}^{\text{t}})] \newline + \log[1 + \sum_{q_i^+ \in \mathcal{P}_v^i} \exp(-\text{score}_{q_i^+}^{\text{t}})] \}, \tag{9}
$$

where |V| denotes the number of videos, q + i and q − i denotes the positive and the negative scene labels in the i th-level scene hierarchy respectively, and P i <sup>v</sup> denotes the annotated scene labels of video v in the i th-level scene hierarchy.

Finally, the final temporal objective function can be formulated as follows:

$$
\mathcal{J}^{\mathrm{t}} = \beta_1^{\mathrm{level}} \mathcal{J}_1^{\mathrm{t}} + \beta_2^{\mathrm{level}} \mathcal{J}_2^{\mathrm{t}},\tag{10}
$$

where β level 1 and β rmlevel 2 are hyper-parameters as coefficients of J t 1 and J t 2 .

## 3. Knowledge-enhanced Non-temporal Feature Learning

The knowledge-enhanced non-temporal feature learning module is used to model videos from a knowledgeenhanced non-temporal perspective. We first obtain framelevel local features by fusing candidate local regions, and then introduce external knowledge to perform and enhance the video feature fusion and scene prediction.

### 3.1 Frame-level local feature fusion.

In this module, we employ the pretrained Faster-RCNN [\[18\]](#page-8-20) to detect the candidate local regions, extract their 2D features with the pretrained ResNet, and denote the 2D feature of the m-th candidate regions of the j-th keyframe as f R2D j,m .

Then we send all the candidate region features detected in each keyframe directly into the self-attention layers of the Transformer encoder. We employ this way to complete inner-frame reasoning among the candidate regions detected in the same keyframe, and obtain the enhanced feature f ′R2D j,m ∈ f ′R2D <sup>j</sup> of each candidate region as follows:

$$
\boldsymbol{f'}_{j}^{\text{R2D}} = \text{Transformer}([\boldsymbol{f}_{j,1}^{\text{R2D}}, \boldsymbol{f}_{j,2}^{\text{R2D}}, ..., \boldsymbol{f}_{j,N_{r}}^{\text{R2D}}]), \quad (11)
$$

where N<sup>r</sup> indicates the number of candidate regions extracted in the same keyframe.

After that, we leverage the frame-level local features f lframe <sup>j</sup> obtained in the previous section as queries, perform self-attention operations on the enhanced candidate region feature e R2D j,m ∈ e R2D j , and denote the obtained fused framelevel local features f ′ lframe j as follows:

$$
Query_j = f_j^{\text{Ifname}} W_Q^{\text{local}},\tag{12}
$$

$$
Key_{j,m} = f'_{j,m}^{\text{R2D}} W_{\text{K}}^{\text{local}},\tag{13}
$$

$$
Value_{j,m} = f'_{j,m}^{\text{R2D}} W_{\text{V}}^{\text{local}},\tag{14}
$$

$$
\alpha_{j,m}^{\text{frame}} = \text{softmax}(\frac{\mathbf{Query}_{j,m} \mathbf{Key}_{j,m}}{\sqrt{d_{\text{Key}}}}),\qquad(15)
$$

$$
\boldsymbol{f'}_{j}^{\text{lframe}} = \sum_{m \in [1,M]} \alpha_{j,m}^{\text{frame}} \boldsymbol{Value}_{j,m}, \qquad (16)
$$

where Wlocal <sup>Q</sup> , Wlocal <sup>K</sup> , Wlocal <sup>V</sup> indicate the weight matrices corresponding to the queries, keys and values of the selfattention module, and dKey represents the dimensions of the key vectors.

#### 3.2 Knowledge-enhanced video feature fusion.

In this module, we leverage the entity embeddings pretrained from knowledge graphs G as external knowledge, and denote G<sup>θ</sup> as the pretrained embeddings corresponding to the token θ. In addition, we also employ the embeddingbased [\[3,](#page-8-13) [14\]](#page-8-21) unsupervised keyword extraction algorithm to extract N<sup>k</sup> keywords kw<sup>k</sup> ∈ K<sup>v</sup> ⊆ G from the associated text descriptions of video v.

In terms of feature fusion, inspired by NetVLAD [\[1\]](#page-8-22), we design a knowledge-enhanced feature fusion method. Unlike NetVLAD, which directly learn a set of parameters for each cluster center and clusters features based on the measured distances, we employ shared parameter modules to generate the required parameters based on the features of the clustering target (*i.e.,* the pretrained word embeddings of keywords) as follows:

$$
\varphi_{\mathbf{w}}(\theta) = \mathbf{W}_{2}^{\mathbf{w}} \delta(\mathbf{W}_{1}^{\mathbf{w}} \theta + \mathbf{b}_{1}^{\mathbf{w}}) + \mathbf{b}_{2}^{\mathbf{w}}, \quad (17)
$$

$$
\varphi_{\rm c}(\theta) = \mathbf{W}_{2}^{\rm c} \,\delta(\mathbf{W}_{1}^{\rm c}\theta + \mathbf{b}_{1}^{\rm c}) + \mathbf{b}_{2}^{\rm c},\tag{18}
$$

$$
\varphi_{\mathbf{z}}(\theta) = \mathbf{W}_{2}^{\mathbf{z}} \delta(\mathbf{W}_{1}^{\mathbf{z}} \theta + \mathbf{b}_{1}^{\mathbf{z}}) + \mathbf{b}_{2}^{\mathbf{z}},\tag{19}
$$

where W<sup>τ</sup> 1 , W<sup>τ</sup> 2 , b τ 1 and b τ 2 ( τ ∈ {w, c, z} ) denote weight matrices and bias vectors in fully connected layers, φw(θ) and φ<sup>c</sup> (θ) denote the functions which can generate parameters to measure distances, φ<sup>z</sup> (θ) denotes the function which is usd to generate the representations of the cluster centers, and δ(·) indicates the activation function.

Then we measure the similarity between different framelevel local features and keyword semantics based on the learned parameters, and weighted summing the difference between the frame-level local features and the obtained representations of the keyword cluster centers. Through this design, we can fuse the features of the sampled frames to varying degrees based on the semantics of specific keywords, and obtain the knowledge-enhanced keyword-level non-temporal feature f kw k as follows:

$$
\alpha_{j,k}^{\text{kw}} = \text{softmax}(\varphi_{\text{w}}(\boldsymbol{G}_{kw_k}) \boldsymbol{f}')_j^{\text{frame}} + \varphi_{\text{c}}(\boldsymbol{G}_{kw_k})), \tag{20}
$$

$$
\boldsymbol{f}_{k}^{\text{kw}} = \sum_{j \in [1, N_{\text{f}}]} \alpha_{j,k}^{\text{video}} (\boldsymbol{f}_{j}^{\prime \text{frame}} - \varphi_{\text{z}}(\boldsymbol{G}_{kw_k})), \qquad (21)
$$

where kw<sup>k</sup> represents the k-th extracted keyword of video v, N<sup>f</sup> denotes the number of the sampled keyframes of each video, and G<sup>θ</sup> denotes the operation of obtaining the pretrained word embedding corresponding to the specific linguistic token θ.

After that, we utilize mean pooling to fuse multiple knowledge-enhanced keyword-level non-temporal features of the same video, and leverage the mean feature of the fused frame-level local features, to receive the knowledgeenhanced video-level non-temporal feature e nt video for each video as follows:

$$
e^{\prime^{\text{nt}, \text{video}}} = \frac{1}{|\mathcal{K}|} \sum_{k \in [1, |\mathcal{K}|]} f_k^{\text{kw}} + \frac{1}{N_f} \sum_{j \in [1, N_f]} f^{\prime \text{frame}}_{j}, \tag{22}
$$
$$
e^{\text{nt}, \text{video}} = \mathbf{W}^{\text{nt}} e^{\prime^{\text{nt}, \text{video}}} + \mathbf{b}^{\text{nt}}, \tag{23}
$$

where Wnt and b nt denote weight matrices and bias vectors in the fully connected layer, |K| denotes the number of the extracted keywords of videos, and N<sup>f</sup> denotes the number of the sampled keyframes for each video.

## 3.3 Knowledge-enhanced multi-label scene prediction

In order to make better use of knowledge for scene prediction, we design shared matching networks to calculate the basic matching scores score′nt v,q between videos v and the i th-level scene label q<sup>i</sup> , based on the knoweledge-enhanced video-level non-temporal featrue e nt video v and the scene label representations e label qi . After that, we obtain the refined scores scorent video qi using approaches similar to those in the hierarchical multi-label prediction in the temporal module as follows:

$$
e^{\prime n t_v \text{video}}_{v,i} = \mathbf{W}_7^i \, \delta(\mathbf{W}_6^i e_v^{\text{nt}, \text{video}} + \mathbf{b}_6^i) + \mathbf{b}_7^i, \qquad (24)
$$

$$
e'_{q_i}^{\text{label}} = W_9^i \, \delta(W_8^i e_{q_i}^{\text{label}} + b_8^i) + b_9^i, \tag{25}
$$

$$
score'_{v,q_i}^{nt} = e'_{v,i}^{nt\_video} \circ e'_{q_i}^{label}, \qquad (26)
$$

$$
score_{v,q_1}^{\text{nt}} = score'_{v,q_1}^{\text{nt}},\tag{27}
$$

$$
score_{v,q_2}^{\text{nt}} = score_{v,\mu_{q_2}}^{\text{nt}} + score_{v,q_2}^{\text{nt}},\qquad(28)
$$

where W<sup>i</sup> τ and b i τ (i ∈ {1, 2}, τ ∈ {6, 7, 8, 9} ) denote weight matrices and bias vectors in fully connected layers, δ(·) indicates the activation function, ◦ represents the inner product operation, and µ<sup>θ</sup> denotes the parent label of θ in scene hierarchy.

For those scene labels whose corresponding entity can be found in the knowledge graph G, we directly utilize their corresponding pretrained entity embeddings G<sup>q</sup> as the scene representations e label q . And for the remaining unmatched scene labels, we initialize their embeddings randomly and update them when training the network. In this way, we also receive an additional benefit, which is the scalability of labels. Specifically, the scalability of labels means that, when we need to predict an unseen label that is not in the original label list but is an entity in knowledge graphs, we do not need to retrain the model, and can perform inferences directly.

Similar to the temporal module, we also employ the Multi-label Cross Entropy Loss to calculate the loss J nt i for each scene hierarchical layer, and the final non-temporal objective function can be formulated as follows:

$$
\mathcal{J}^{\rm nt} = \beta_1^{\rm level} \mathcal{J}_1^{\rm nt} + \beta_2^{\rm level} \mathcal{J}_2^{\rm nt},\tag{29}
$$

where β level 1 and β level 2 are hyper-parameters as coefficients of J nt 1 and J nt 2 .

## 4. Self-distillation and Scene Recognition

In the aforementioned sections, we model videos from two perspectives (*i.e.,* the temporal perspective and the knowledge-enhanced non-temporal perspective), and obtain scene label scores from both perspectives.

To enable the two modules (*i.e.,* temporal module and the knowledge-enhanced non-temporal module) to learn information separately, and integrate the learned information with each other, we employ Euclideandistance to measure the difference between the two groups (*i.e.,*the temporal perspective and the knowledge-enhanced non-temporal perspective) of scene label scores in each scene hierarchical layer. We obtain the distillation loss J distill according to the obtained Euclidean distances J distill i for the i th-level <span id="page-6-1"></span>scene hierarchy as follows:

$$
\mathcal{J}_i^{\text{distill}} = \frac{1}{|\mathcal{V}|}sqrt[5]{\sum_{q_i \in \mathcal{L}_i} (score_{q_i}^{\text{t}} - score_{q_i}^{\text{nt}})^2}, \quad (30)
$$

$$
\mathcal{J}^{\text{distill}} = \beta_1^{\text{level}} \mathcal{J}_1^{\text{distill}} + \beta_2^{\text{level}} \mathcal{J}_2^{\text{distill}},\qquad(31)
$$

where β level 1 and β level 2 are hyper-parameters as coefficients of J distill 1 and J distill 2 , and L<sup>i</sup> denotes the set of the scene labels in the i th-level hierarchical layer.

In the end, the final objective function is defined as:

$$
\mathcal{J} = \beta^{\text{t}} \mathcal{J}^{\text{t}} + \beta^{\text{nt}} \mathcal{J}^{\text{nt}} + \beta^{\text{distill}} \mathcal{J}^{\text{distill}},\qquad(32)
$$

where β t , β nt and β distill are hyper-parameters as coefficients of J t , J nt and J distill .

Moreover, to balance the performance and efficiency of the model, inspired by previous work [\[5,](#page-8-4) [11,](#page-8-5) [15\]](#page-8-1), the two modules are both utilized to participate in the training, but only the temporal module is employed for reasoning. When reasoning, given videos and the associated textual descriptions as queries, the model will first calculate the scene label scores through the temporal module, then take out the scene labels with the Top-K scores or the scores that exceed a specific threshold, and return them to users.

# EXPERIMENTS

In this section, we conduct experiments on a realworld dataset to evaluate the performance of our proposed method.

## 1. Dataset

We evaluate our model on one of the largest available video scene datasets, which is called the Koubei dataset. The Koubei Dataset contains metadata from Koubei Platform[1](#page-6-0) , including 63,977 videos with associated textual descriptions, and manually annotated hierarchical scene labels, where each video can correspond to multiple scene labels. Besides, the scene label hierarchy has 6 1 st-level labels and 320 2 rd-level labels.

We randomly split the Koubei dataset into training, validation, and testing sets. Specifically, we randomly sample 1,000 videos into the validation and 1,000 videos into the testing sets, respectively, and the remaining 61,977 videos are utilized as the training set.

## 2. Evaluation Protocol and Parameters Settings

We evaluate the performance of different models using F1 score and RP@90% as the evaluation metrics. RP@90% denotes the proportion of labelled videos when we add threshold constraints to make Accuracy reaches 90%, and this metric is widely employed in commercial products.

In our experiments, we set the number of the sampled keyframes N<sup>f</sup> as 12, the number of consecutive frames for 3D features N<sup>c</sup> as 16, and the maximum number of extracted keywords N<sup>r</sup> as 10. For simplicity, We set all the hyper-parameters β t , β nt , β distill , β distill 1 , β distill 2 , β level 1 , β level 2 to the same value 1. We introduce*ConceptNet*as the external knowledge graph, and the pretrained entity embeddings are provided by*ConceptNet Numberbatch*[\[20\]](#page-8-11). We utilize GeLU as the activation function, and employ*dropout*with 50% keep probability, weight decay, and early stopping to alleviate overfitting. To train our proposed model, we randomly initialize model parameters with a Gaussian distribution, and utilize AdamW [\[12\]](#page-8-23) algorithm for optimization. We further restrict the dimensions of the final representation vector of each video to be the same for fair comparisons. We have tried different parameter settings, including the batch size of {8, 16, 32}, the latent feature dimension of {192, 384, 768}, the learning rate of {1e-1, 3e-4, 1e-4, 3e-5, 1e-5}. As the findings are consistent across the dimensions of latent vectors, if not specified, we only report the results based on the dimension of 768, which gives relatively good performance.

## 3. Baselines

To evaluate the effectiveness of our model, we compare our proposed method with several state-of-the-art baselines. Specifically, the original task of the first four models is not video scene recognition, we adjust these models and perform the task of scene prediction based on the obtained video representations using them. The latter two models which are originally designed for scene recognition are directly utilized in experiments.

- MMBT [\[8\]](#page-8-15): introduces a supervised multi-modal bi-Transformer that jointly finetunes uni-modally pretrained text and image encoders. Besides, this model is the backbone of the temporal module of our model.
- LSCTA [\[19\]](#page-8-8): employs a Transformer model as the backbone, and develops a framework to align sequences in different modalities to capture information.
- HGLTM [\[6\]](#page-8-0): proposes a hierarchical model which can construct the temporal structure at frame-level and object-level successively, and extract pivotal information effectively from global to local, which improves the model capacity.
- STGK [\[15\]](#page-8-1): proposes a novel spatio-temporal graph network to explicitly exploit the spatio-temporal object interaction, which is crucial for video understanding.
- HCMFL [\[7\]](#page-8-10): develops a Hierarchy-dependent Crossplatform Multi-view Feature Learning framework, which jointly utilizes multi-platform data, object-scene

<span id="page-6-0"></span><sup>1</sup>www.koubei.com

| Model                  | RP@90% | F1 score |
|------------------------|--------|----------|
| MMBT                   | 0.521  | 0.720    |
| LSCTA                  | 0.324  | 0.706    |
| HGLTM                  | 0.434  | 0.719    |
| STGK                   | 0.452  | 0.707    |
| HCMFL                  | 0.445  | 0.735    |
| HETFN                  | 0.483  | 0.710    |
| Ours-S2                | 0.536  | 0.726    |
| Ours-S2w/o-hier        | 0.511  | 0.731    |
| Ours-S2w/o-know&w-temp | 0.511  | 0.709    |
| Ours-S2w/o-know        | 0.504  | 0.707    |
| Ours-S2w/o-kw          | 0.531  | 0.706    |
| OurModel               | 0.561  | 0.735    |

<span id="page-7-1"></span><span id="page-7-0"></span>Table 1. Performance comparison among our model and all fullytrained baselines using the metrics RP@90% and F1 score.

deep features, and the hierarchical structure prior for category prediction from videos.

- HETFN [\[28\]](#page-9-5): proposes a Hybrid-Attention Enhanced Two-Stream Fusion Network for the video recognition task, and develops a novel Global-Local Attention Module, which can be inserted into neural networks to generate enhanced visual features from video content.
- Ours-S2: This variant removes the Temporal Feature Learning module (S1) from the origin proposed model, and keeps the Knowledge-enhanced Non-temporal Feature Learning module (S2) to learn the representation of videos.
- Ours-S2w/o-hier: This variant additionally removes the loss functions for the 1 st-level scene hierarchical layer on the basis of Ours-S2.
- Ours-S2w/o-know&w-temp: This variant replaces the frame-level local feature fusion and the knowledgeenhanced video feature fusion in the non-temporal module by*Transformer* on the basis of Ours-S2.
- Ours-S2w/o-know: This variant drops the proposed knowledge-enhanced video feature fusion module, and utilizes the mean feature of the fused frame-level local features as the video-level non-temporal feature on the basis of Ours-S2.
- Ours-S2w/o-kw: This variant replaces the employed pretrained keyword entity embeddings by an equal number of randomly initialized embeddings shared by all videos on the basis of Ours-S2.

## 4. Performances, Quantitative Analysis and Ablation Study

We evaluate all fully-trained models using the metrics F1 score and RP@90%, and report the results in Table [1.](#page-7-0) We have the following observations with respect to our experimental results.

First, our proposed method achieves the best performance on Koubei Dataset using the metric RP@90% and F1 score, demonstrating the effectiveness of our model.

Second, compared with MMBT which is the backbone of the temporal module of OurModel, and models videos only from the temporal perspective, the whole OurModel achieves a 7.7% performance gain on RP@90% and 2.1% performance gain on F1 score, demonstrating the effectiveness of our proposed knowledge-enhanced non-temporal module. Besides, OurModel achieves better performance than separate stream modules MMBT and Ours-S2, verifying that the two perspectives (*i.e.,*the temporal and the knowledge-enhanced non-temporal perspectives) are both valuable for the task of scene recognition and complementary to each other.

Third, compared with Ours-S2w/o-hier, Ours-S2 receives better performance, verifying that calculating loss function simultaneously for multi-level scene hierarchy can improve the performance of our model.

Moreover, Ours-S2 obtain better performance than Ours-S2w/o-know&w-temp and Ours-S2w/o-know, demonstrating the effectiveness of the proposed frame-level local feature fusion and knowledge-enhanced video feature fusion.

Finally, compared with Ours-S2w/o-kw, Ours-S2 achieves better performance, verifying that the introduced external knowledge is valuable to our proposed model.

# Conclusions and Future Work

With the explosive growth of video data in real-world applications, a comprehensive representation of videos becomes increasingly important. In this paper, we address the problem of video scene recognition, whose goal is to learn a high-level video representation to classify scenes in videos. In this paper, we propose a novel two-stream framework to model video representations from the temporal and knowledge-enhanced non-temporal perspectives, and integrate these two perspectives in an end-to-end manner by self-distillation. Besides, we design a knowledge-enhanced feature fusion and label prediction method that contributes to naturally introducing knowledge into the task of video scene recognition. We evaluated our model for scene recognition on a real-world dataset, and the experimental results demonstrate the effectiveness of our proposed model. In addition, we also conducted ablation studies, which demonstrated the effectiveness of our proposed temporal and nontemporal two-stream framework and knowledge-enhanced feature fusion method, respectively. In future work, we may pay more attention to the utilization of knowledge graphs, and try to leverage edge information in knowledge graphs to assist reasoning to enhance video understanding.

# References

- <span id="page-8-22"></span>[1] Relja Arandjelovic, Petr Gronat, Akihiko Torii, Tom ´ as Pa- ´ jdla, and Josef Sivic. Netvlad: CNN architecture for weakly supervised place recognition. In*IEEE Conference on Computer Vision and Pattern Recognition, CVPR*, pages 5297– 5307. IEEE Computer Society, 2016. [5](#page-4-0)
- <span id="page-8-17"></span>[2] Joao Carreira and Andrew Zisserman. Quo vadis, action ˜ recognition? A new model and the kinetics dataset. In *IEEE Conference on Computer Vision and Pattern Recognition, CVPR*, pages 4724–4733. IEEE Computer Society, 2017. [3](#page-2-0)
- <span id="page-8-13"></span>[3] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. BERT: pre-training of deep bidirectional transformers for language understanding. In *Proceedings of the Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, NAACL-HLT*, pages 4171–4186. Association for Computational Linguistics, 2019. [3,](#page-2-0) [4,](#page-3-0) [5](#page-4-0)
- <span id="page-8-14"></span>[4] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In *IEEE Conference on Computer Vision and Pattern Recognition, CVPR*, pages 770–778. IEEE Computer Society, 2016. [3](#page-2-0)
- <span id="page-8-4"></span>[5] Geoffrey E. Hinton, Oriol Vinyals, and Jeffrey Dean. Distilling the knowledge in a neural network. *CoRR*, abs/1503.02531, 2015. [2,](#page-1-0) [3,](#page-2-0) [7](#page-6-1)
- <span id="page-8-0"></span>[6] Yaosi Hu, Zhenzhong Chen, Zheng-Jun Zha, and Feng Wu. Hierarchical global-local temporal modeling for video captioning. In *Proceedings of the ACM International Conference on Multimedia, MM*, pages 774–783. ACM, 2019. [1,](#page-0-0) [2,](#page-1-0) [7](#page-6-1)
- <span id="page-8-10"></span>[7] Shuqiang Jiang, Weiqing Min, and Shuhuan Mei. Hierarchydependent cross-platform multi-view feature learning for venue category prediction. *IEEE Trans. Multim.*, 21(6):1609–1619, 2019. [2,](#page-1-0) [7](#page-6-1)
- <span id="page-8-15"></span>[8] Douwe Kiela, Suvrat Bhooshan, Hamed Firooz, and Davide Testuggine. Supervised multimodal bitransformers for classifying images and text. In *Visually Grounded Interaction and Language (ViGIL), NeurIPS Workshop*, 2019. [3,](#page-2-0) [7](#page-6-1)
- <span id="page-8-2"></span>[9] Weijie Liu, Peng Zhou, Zhe Zhao, Zhiruo Wang, Qi Ju, Haotang Deng, and Ping Wang. K-BERT: enabling language representation with knowledge graph. In *The AAAI Conference on Artificial Intelligence, AAAI , The Innovative Applications of Artificial Intelligence Conference, IAAI, The AAAI Symposium on Educational Advances in Artificial Intelligence, EAAI*, pages 2901–2908. AAAI Press, 2020. [2,](#page-1-0) [3](#page-2-0)
- <span id="page-8-3"></span>[10] Zhenghao Liu, Chenyan Xiong, Maosong Sun, and Zhiyuan Liu. Entity-duet neural ranking: Understanding the role of knowledge graph semantics in neural information retrieval. In *Proceedings of the Annual Meeting of the Association for Computational Linguistics, ACL*, pages 2395–2405. Association for Computational Linguistics, 2018. [2,](#page-1-0) [3](#page-2-0)
- <span id="page-8-5"></span>[11] David Lopez-Paz, Leon Bottou, Bernhard Sch ´ olkopf, and ¨ Vladimir Vapnik. Unifying distillation and privileged information. In *International Conference on Learning Representations, ICLR, Conference Track Proceedings*, 2016. [2,](#page-1-0) [3,](#page-2-0) [7](#page-6-1)

- <span id="page-8-23"></span>[12] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. In *International Conference on Learning Representations, ICLR*. OpenReview.net, 2019. [7](#page-6-1)
- <span id="page-8-9"></span>[13] Alina Matei, Andreea Glavan, and Estefan´ıa Talavera. Deep learning for scene recognition from visual data: A survey. In *Hybrid Artificial Intelligent Systems, HAIS*, volume 12344 of *Lecture Notes in Computer Science*, pages 763– 773. Springer, 2020. [2](#page-1-0)
- <span id="page-8-21"></span>[14] Tomas Mikolov, Kai Chen, Greg Corrado, and Jeffrey Dean. ´ Efficient estimation of word representations in vector space. In *International Conference on Learning Representations, ICLR Workshop Track Proceedings*, 2013. [5](#page-4-0)
- <span id="page-8-1"></span>[15] Boxiao Pan, Haoye Cai, De-An Huang, Kuan-Hui Lee, Adrien Gaidon, Ehsan Adeli, and Juan Carlos Niebles. Spatio-temporal graph for video captioning with knowledge distillation. In *IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR*, pages 10867–10876. Computer Vision Foundation / IEEE, 2020. [1,](#page-0-0) [2,](#page-1-0) [3,](#page-2-0) [7](#page-6-1)
- <span id="page-8-6"></span>[16] Zhaofan Qiu, Ting Yao, and Tao Mei. Learning spatiotemporal representation with pseudo-3d residual networks. In *IEEE International Conference on Computer Vision, ICCV*, pages 5534–5542. IEEE Computer Society, 2017. [2](#page-1-0)
- <span id="page-8-7"></span>[17] Zhaofan Qiu, Ting Yao, Chong-Wah Ngo, Xinmei Tian, and Tao Mei. Learning spatio-temporal representation with local and global diffusion. In *IEEE Conference on Computer Vision and Pattern Recognition, CVPR*, pages 12056–12065. Computer Vision Foundation / IEEE, 2019. [2](#page-1-0)
- <span id="page-8-20"></span>[18] Shaoqing Ren, Kaiming He, Ross B. Girshick, and Jian Sun. Faster R-CNN: towards real-time object detection with region proposal networks. In *Advances in Neural Information Processing Systems: Annual Conference on Neural Information Processing Systems*, pages 91–99, 2015. [5](#page-4-0)
- <span id="page-8-8"></span>[19] Botian Shi, Lei Ji, Zhendong Niu, Nan Duan, Ming Zhou, and Xilin Chen. Learning semantic concepts and temporal alignment for narrated video procedural captioning. In *Proceedings of the ACM International Conference on Multimedia, MM*, pages 4355–4363. ACM, 2020. [2,](#page-1-0) [7](#page-6-1)
- <span id="page-8-11"></span>[20] Robyn Speer, Joshua Chin, and Catherine Havasi. Conceptnet 5.5: An open multilingual graph of general knowledge. In *Proceedings of the Thirty-First AAAI Conference on Artificial Intelligence*, pages 4444–4451. AAAI Press, 2017. [3,](#page-2-0) [7](#page-6-1)
- <span id="page-8-18"></span>[21] Jianlin Su. *Extend 'Softmax+Cross Entropy' to Multi-label Classification Problem*, 2020. [5](#page-4-0)
- <span id="page-8-19"></span>[22] Yifan Sun, Changmao Cheng, Yuhan Zhang, Chi Zhang, Liang Zheng, Zhongdao Wang, and Yichen Wei. Circle loss: A unified perspective of pair similarity optimization. In *IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR*, pages 6397–6406. Computer Vision Foundation / IEEE, 2020. [5](#page-4-0)
- <span id="page-8-16"></span>[23] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia Polosukhin. Attention is all you need. In *Advances in Neural Information Processing Systems: Annual Conference on Neural Information Processing Systems*, pages 5998–6008, 2017. [3](#page-2-0)
- <span id="page-8-12"></span>[24] Chenyan Xiong, Jamie Callan, and Tie-Yan Liu. Word-entity duet representations for document ranking. In *Proceedings*

*of the International ACM SIGIR Conference on Research and Development in Information Retrieval*, pages 763–772. ACM, 2017. [3](#page-2-0)

- <span id="page-9-1"></span>[25] Chenyan Xiong, Russell Power, and Jamie Callan. Explicit semantic ranking for academic search via knowledge graph embedding. In *Proceedings of the International Conference on World Wide Web, WWW*, pages 1271–1279. ACM, 2017. [2,](#page-1-0) [3](#page-2-0)
- <span id="page-9-2"></span>[26] Yuan Yuan, Haopeng Li, and Qi Wang. Spatiotemporal modeling for video summarization using convolutional recurrent neural network. *IEEE Access*, 7:64676–64685, 2019. [2](#page-1-0)
- <span id="page-9-0"></span>[27] Shengyu Zhang, Ziqi Tan, Jin Yu, Zhou Zhao, Kun Kuang, Jie Liu, Jingren Zhou, Hongxia Yang, and Fei Wu. Poet: Product-oriented video captioner for e-commerce. In *Proceedings of the ACM International Conference on Multimedia, MM*, pages 1292–1301. ACM, 2020. [1,](#page-0-0) [2,](#page-1-0) [3](#page-2-0)
- <span id="page-9-5"></span>[28] Yanchao Zhang, Weiqing Min, Liqiang Nie, and Shuqiang Jiang. Hybrid-attention enhanced two-stream fusion network for video venue prediction. *IEEE Trans. Multim.*, 23:2917– 2929, 2021. [2,](#page-1-0) [8](#page-7-1)
- <span id="page-9-3"></span>[29] Ziqi Zhang, Yaya Shi, Chunfeng Yuan, Bing Li, Peijin Wang, Weiming Hu, and Zheng-Jun Zha. Object relational graph with teacher-recommended learning for video captioning. In *IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR*, pages 13275–13285. Computer Vision Foundation / IEEE, 2020. [2,](#page-1-0) [3](#page-2-0)
- <span id="page-9-4"></span>[30] Bolei Zhou, Agata Lapedriza, Aditya Khosla, Aude Oliva, ` and Antonio Torralba. Places: A 10 million image database for scene recognition. *IEEE Trans. Pattern Anal. Mach. Intell.*, 40(6):1452–1464, 2018. [2](#page-1-0)
- <span id="page-9-6"></span>[31] Yushan Zhu, Huaixiao Zhao, Wen Zhang, Ganqiang Ye, Hui Chen, Ningyu Zhang, and Huajun Chen. Knowledge perceived multi-modal pretraining in e-commerce. In *Proceedings of the ACM International Conference on Multimedia, MM*, pages 2744–2752. ACM, 2021. [2,](#page-1-0) [3](#page-2-0)
