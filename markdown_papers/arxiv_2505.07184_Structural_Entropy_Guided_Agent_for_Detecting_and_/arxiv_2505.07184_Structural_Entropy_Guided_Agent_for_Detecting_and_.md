---
cite_key: "wei2015"
title: "Structural Entropy Guided Agent for Detecting and Repairing Knowledge Deficiencies in LLMs"
authors: "Tengfei Pan, Artificial Intelligence"
year: 2015
doi: "10.18653/v1/2023.findings-acl.551)"
date_processed: "2025-07-02"
phase2_processed: true
original_folder: "arxiv_2505.07184_Structural_Entropy_Guided_Agent_for_Detecting_and_"
images_total: 5
images_kept: 5
images_removed: 0
---

# Structural Entropy Guided Agent for Detecting and Repairing Knowledge Deficiencies in LLMs

Yifan Wei1,2, Xiaoyan Yu1,3, Tengfei Pan<sup>2</sup> , Angsheng Li1† , Li Du2†

<sup>1</sup>State Key Laboratory of CCSE,School of Computer Science and Engineering,Beihang University <sup>2</sup>Beijing Academy of Artificial Intelligence, <sup>3</sup>Beijing Institute of Technology weiyifan@buaa.edu.cn, {tfpan,duli}@baai.ac.cn

# Abstract

Large language models (LLMs) have achieved unprecedented performance by leveraging vast pretraining corpora, yet their performance remains suboptimal in knowledge-intensive domains such as medicine and scientific research, where high factual precision is required. While synthetic data provides a promising avenue for augmenting domain knowledge, existing methods frequently generate redundant samples that do not align with the model's true knowledge gaps. To overcome this limitation, we propose a novel Structural Entropy-guided Knowledge Navigator (SENATOR) framework that addresses the intrinsic knowledge deficiencies of LLMs. Our approach employs the Structure Entropy (SE) metric to quantify uncertainty along knowledge graph paths and leverages Monte Carlo Tree Search (MCTS) to selectively explore regions where the model lacks domain-specific knowledge. Guided by these insights, the framework generates targeted synthetic data for supervised fine-tuning, enabling continuous self-improvement. Experimental results on LLaMA-3 and Qwen2 across multiple domain-specific benchmarks show that SENATOR effectively detects and repairs knowledge deficiencies, achieving notable performance improvements. The code and data for our methods and experiments are available at [https://github.com/weiyifan1023/senator.](https://github.com/weiyifan1023/senator)

# 1 Introduction

With the pretraining process on massive-scale corpora, Large Language Models (LLMs) capture abundant knowledge and demonstrate impressive performance on various downstream tasks [\(Chen](#page-9-0) [et al., 2015;](#page-9-0) [Liu et al., 2021\)](#page-10-0). However, their performance may still be unsatisfactory in certain knowledge-intensive domains such as medicine and scientific research. This is primarily due to the difficulty in acquiring and scaling up high-quality domain-specific corpora [\(Lu et al., 2024;](#page-10-1) [Wang](#page-11-0) [et al., 2024\)](#page-11-0), which hinders the ability of the models to handle tasks that require high factual precision.

The development of data synthesis technology [\(Wang et al., 2023;](#page-11-1) [Zhao et al., 2024\)](#page-12-0) offers an alternative way to address these limitations in remedying the knowledge deficiency of LLMs. While promising, the efficiency of data synthesis remains a significant challenge. This is because current data synthesis methods may not consider the model's knowledge boundaries [\(Jiang et al., 2021;](#page-9-1) [Mallen et al., 2023;](#page-10-2) [Yue et al., 2025\)](#page-12-1), resulting in substantial efforts spent in generating data that the model may already be familiar with. In fact, even with advanced prompt engineering [\(Wei et al.,](#page-11-2) [2022\)](#page-11-2), generated outputs tend to skew toward high-frequency distributions seen in pretraining data, leading to severe redundancy. Therefore, efficient data synthesis should be tightly coupled with mechanisms for effectively detecting knowledge deficiencies [\(Xiong et al., 2024;](#page-11-3) [Song et al., 2025\)](#page-11-4) within LLMs, so that the synthesized data can repair the knowledge deficiencies.

<sup>†</sup>Corresponding Authors.

However, the knowledge boundaries of large models can be quite complex. Although these models are trained on massive amounts of data, their knowledge is implicitly encoded in model parameters [\(Geva et al., 2021;](#page-9-2) [Wei et al., 2025\)](#page-11-5) rather than being explicitly stored, leading to unclear distinctions between known and unknown information. In specialized domains, this challenge is compounded by the generation of unreliable or contradictory content [\(Yang et al., 2024c\)](#page-12-2), which produces flawed synthetic samples that hinder the effective expansion of high-quality, domain-specific corpora.

To overcome the aforementioned challenges, we propose SENATOR, a Structural Entropy-guided Knowledge Navigator framework, which achieves knowledge deficiency remediation through a closed loop of structured knowledge probing and targeted synthetic data generation. The framework comprises two key components: 1) Knowledge Deficiency Detection: Human-annotated knowledge graph (KG) systematically describes the underlying complexities and intricacies of the domain. However, the combinatorial explosion of possible paths makes enumeration computationally infeasible. To efficiently detect the knowledge paths, we drive the LLM as an agent to explore upon the KG in a Monte Carlo Tree Search (MCTS) manner [\(Metropolis and Ulam, 1949\)](#page-10-3), with the structure entropy as reward. The Structure Entropy (SE) [\(Li and Pan, 2016;](#page-10-4) [Li, 2024\)](#page-10-5) metric quantifies the structural information contained within a graph by capturing its topological organization and the interactions among nodes. This provides insight into the model's uncertainty along knowledge paths in the KG. By employing MCTS within the knowledge space, our framework uses SE values as intrinsic rewards to decide whether to expand specific entity nodes, effectively prioritizing the exploration of paths with high uncertainty and detecting critical knowledge deficiencies. 2) Knowledge Synthesis and Repair: Leveraging the critical knowledge paths identified via MCTS, our framework generates synthetic data by employing prompt templates to structure the content. The KG serves as a trusted source to ensure both the data inputs and the synthesized outputs are credible and contextually relevant. This synthetic data is then used to fine-tune the model through supervised learning, enabling continuous self-improvement and effective remediation of knowledge deficiencies.

Our experiments demonstrate that the SENATOR framework effectively detects knowledge deficiencies in large language models and efficiently repairs them, leading to significant performance improvements across multiple domain-specific benchmarks. Data distribution analyses confirm that our synthetic data incorporates knowledge deficiencies from the pretraining corpus. Moreover, supervised fine-tuning (SFT) of LLMs like Llama-3 [\(Grattafiori et al., 2024\)](#page-9-3) and Qwen2 [\(Yang et al.,](#page-12-3) [2024b\)](#page-12-3) using this data led to significant performance improvements, demonstrating that targeted injection of missing knowledge can substantially enhance overall model performance.

# 2 Related Work

Knowledge Deficiency Detection of LLMs Though LLMs possess extensive knowledge, they often struggle to accurately delineate what they know from what they do not [\(Yin et al., 2023;](#page-12-4) [Ren](#page-10-6) [et al., 2023\)](#page-10-6). Several approaches [\(Jiang et al., 2020;](#page-9-4) [Mallen et al., 2023;](#page-10-2) [Wei et al., 2024\)](#page-11-6)construct knowledge probability distributions based on existing annotated data, using metrics such as answer correctness or confidence scores to assess a model's knowledge proficiency. One line of work [\(Wei](#page-11-2) [et al., 2022;](#page-11-2) [Li et al., 2023a;](#page-10-7) [Tian et al., 2024a\)](#page-11-7) directly toward enhancing a model's ability to fully leverage its existing knowledge, thereby reducing the proportion of "Unknown Knows". Another line of work pay attention to enabling models to explicitly acknowledge their knowledge gaps, thus minimizing the occurrence of "Unknown Unknowns". Approaches such as R-tuning [\(Zhang](#page-12-5) [et al., 2023\)](#page-12-5) utilize labeled data with supervised fine-tuning to judge response correctness, while reinforcement learning based strategies have also been explored [\(Yang et al., 2023b;](#page-12-6) [Kang et al.,](#page-9-5) [2024\)](#page-9-5). In contrast, our approach for deficiency detection is designed not to rely on pre-existing labeled data, but instead to actively explore the KG to detect intrinsic model uncertainty.

Model Self-Improvement Self-improvement methods of LLM focus on leveraging internal knowledge and feedback to iteratively enhance the performance of LLMs [\(Zelikman et al., 2022,](#page-12-7) [2024\)](#page-12-8). A pivotal challenge is generating a reliable critique signal to discern high-quality responses from suboptimal ones. Previous methods [\(Bai et al., 2022;](#page-9-6) [Wang et al., 2023\)](#page-11-1) involve prompting the LLM to generate diverse task-specific queries and corresponding outputs, followed by the application of manually crafted heuristic rules, such as filtering based on query length to remove redundant or low-quality data pairs. Given the complexity of devising effective heuristics, subsequent research [\(Sun et al., 2023;](#page-11-8) [Li et al., 2023b;](#page-10-8) [Guo et al., 2024\)](#page-9-7) proposes a few general principles or judging

<span id="page-2-0"></span>![](_page_2_Figure_0.jpeg)
<!-- Image Description: The image details a process for Maximum Subgraph Extraction (Max SE) using Monte Carlo Tree Search (MCTS). A flowchart depicts MCTS stages: Selection, Expansion, Simulation, and Backup, iterated X times. Nodes represent states in a tree, with colors indicating node type (root, current, expanded, terminal). A separate diagram shows Max SE trajectory, a sequence of states (S₀, S₁, S₂, ..., Sₙ) connected by edges indicating transitions. The overall process leverages Large Language Models (LLM) and Knowledge Graphs (KG) for synthetic data generation and knowledge repair. -->

Figure 1: The SENATOR framework operates as follows: An entity state in the knowledge graph is (a) selected, (b) expanded, and (c) simulated using the LLM agent until a terminal node is reached. Specifically, we employ a random policy π during the expansion phase. (d) Subsequently, signals from the value function V (·) are backpropagated. This process is iterated multiple times, with the MCTS algorithm searching for (f) better trajectories guided by (e) signals from structural entropy to (g) generate data addressing knowledge deficiencies, (h) and repair model knowledge.

criteria and ask the LLM itself to assess the quality its responses according to these guidelines. However, this approach demands that LLMs possess a robust capability to apply these principles to each specific instance and render accurate judgments. Recently, reinforcement learning-based model show impressive reasoning ability by learning the experiences obtained from explorations in the solution space [\(Tian et al., 2024b;](#page-11-9) [Goldie et al., 2025\)](#page-9-8). While the probability of obtained plausible solution space of knowledge intensive tasks would be rather limited as the LLM may not possess the necessary knowledge, which would severely restrict the efficiency of exploration and data generation. In this paper, we choose to guide the exploration process in knowledge space using KGs, in a MCTS manner, so as to enable targeted synthetic data generation for high efficiency LLM self-improvement.

# 3 Methodology

Given a knowledge graph, the number of possible knowledge paths P (i.e., Figure [1f\)](#page-2-0) increases in a combinatorial speed along with the size of KG, making enumerating all possible paths and detecting the uncertainty of LLM on these paths computationally infeasible. To tackle this challenge, as shown in Figure [1,](#page-2-0) SENATOR employs MCTS to navigate the LLM-based agent to search on the KG for seeking out the most informative paths. To steer the agent to search toward regions with high uncertainty, we introduce a structural entropy based reward function. Based on the identified high-uncertainty paths, data are synthesized to remediate the identified knowledge deficiencies.

## 1 Structural Entropy Guided Knowledge Deficiency Detection

The structural entropy based reward function combines the uncertainty of LLM on individual KG triplets with the topological structure information of the KG, guiding the LLM-based agent to perform MCTS over the KG and discover knowledge paths with critical deficiencies.

Self-Information for Measuring Triplet-Level Uncertainty Self-Information [\(Shannon, 1948\)](#page-11-10) quantifies the amount of information conveyed by a "fact" given its probability distribution. In KGs, a "fact" is represented as a triplet τ =< subject u, relation ρ, object v >. To measure the LLM's uncertainty of such "facts", we transform τ into a cloze statement form. The cloze context is formed by combining the subject u and the relation ρ, creating a prompt to predict the missing object v. The

self-information of a fact τ is defined as:

<span id="page-3-0"></span>
$$
I(u, \rho, v) = -\log_2 P(v \mid u, \rho),\tag{1}
$$

where P(v | u, ρ) is the probability of the output v conditioned on the cloze context. Since the relation ρ in KGs is directional, the self-information calculated in this manner serves as a measure of the factual knowledge confidence for the entire triplet.

Structural Entropy of Modeling Knowledge Path-Level Uncertainty To integrate the uncertainty of all triplets along a knowledge path while considering their structural importance, we adopt structural entropy (SE) as a more comprehensive measure of an LLM's knowledge confidence, as shown in Figure [1e.](#page-2-0) Structural importance reflects the topological significance of a triplet τ within the knowledge graph. Triplets involving highly connected entities are considered more central, as these entities participate in more relational paths and exert broader influence across the graph. Unlike self-information or Shannon entropy, structural entropy accounts for the knowledge graph's topological structure and the interdependencies among its elements. This is crucial because each triplet is not an isolated piece of information but part of a structured network. The relationships among entities contribute to the overall representation of knowledge. Given a knowledge graph G = (V, E), each edge ρ ∈ E is assigned a weight derived from the self-confidence in Equation [1.](#page-3-0) The weighted degree of an entity node u ∈ V is defined as:

$$
d_u = \sum_{v \in \mathcal{N}(u)} I(u, \rho, v), \tag{2}
$$

where N (u) denotes the set of neighbors of entity u and d<sup>u</sup> represents the overall uncertainty contained within the node. To quantify the average information content of the graph G, we define the one-dimensional structural entropy of the weighted, connected graph G as:

H<sup>1</sup> (G) = − X u∈V du vol(G) log<sup>2</sup> du vol(G) , (3)

where vol(G) represents the total weighted degree of G. A higher H<sup>1</sup> (G) indicates a more complex and less confidently represented region within the knowledge graph. By formulating SE as the exploration reward in MCTS, we enable the search algorithm to prioritize paths traversing maximally uncertain knowledge structures, thereby efficiently exposing the model's systemic weaknesses.

### 2 MCTS for Knowledge Deficiency Detection

Given the SE-based reward function, we employ MCTS to explore the KG and identify potential knowledge deficiency paths in the model. We define the initial state s<sup>0</sup> as the starting node for traversing the KG, where a set of seed entities from [\(Soman et al., 2024\)](#page-11-11) is selected. KG triplets are incrementally incorporated into the knowledge paths until the maximum search depth T is reached. This process enhances the LLM's awareness of its knowledge deficiencies by maximizing the expected reward, which emphasizes the uncertainty associated with these deficiencies.

Node Selection. The objective of this stage is to identify and prioritize KG entities that are likely to expose the LLM's knowledge deficiencies, as shown in Figure [1a.](#page-2-0) Formally, at state st, the LLM agent reaches entity node u<sup>t</sup> of the KG, and the MCTS process choose from A = {a1, a2, . . . , am}, representing the relation edges ρt+1 that connect the current entity u<sup>t</sup> to its neighbors N (ut). It is guided by two key variables: Q(st, a), the cumulative value of taking action a in state st, and N(st), the visitation frequency of state st. Heuristically, Q(st, a) guides exploitation by favoring actions with historically high rewards, while N(st) encourages exploration of under-visited states. We integrate these complementary objectives using the PUCT algorithm [\(Rosin, 2011\)](#page-11-12), which selects the next state as:

$$
s_{t+1}^{*} = \arg \max_{s_t} \left[ Q(s_t, a) + c_{\text{puct}} \cdot P(a \mid s_t) \frac{\sqrt{N(s_t)}}{1 + N(s_t, a)} \right],
$$
 (4)

where P(a|st) denotes the prior probability of selecting action a given state st. In this way, an additional triplet τ is incorporated into the knowledge path P.

Path Expansion. Expansion occurs when a leaf node is reached during the selection phase, enabling the integration of new states and the assessment of immediate rewards. Upon reaching a leaf node, it is expanded by selecting all possible relation action from leaf node, where each action a represents a transition from the current entity state s<sup>t</sup> to a new entity state st+1 in N (st), as shown in Figure [1b.](#page-2-0) These unexplored entities N (st) are then added as leaf nodes to the search tree. The immediate reward function r(st, a) quantifies the advantage of each action a ∈ A available at state st.

$$
r_{t+1} = r(s_t, a) = I(s_t, a, s_{t+1}) = -\log_2 \frac{d_{s_{t+1}}}{\text{vol}(G)},
$$

$$
V(s_t) = r_{t+1} + \gamma V(s_{t+1}) = \sum_{k=0}^{T-k-1} \gamma^k r_{t+k+1},
$$
 (5)

where γ is the discount factor for future state values V (·) and T is the depth of the MCTS search space. To accommodate scenarios with limited decision steps and stable reward distributions, we eliminate the discount factor and instead compute the average of future immediate reward values, as formalized in Equation [6.](#page-4-0)

Reward Estimation. A simulation shown in Figure [1c](#page-2-0) is run from the new expanded node s<sup>t</sup> by making random relation actions until a terminal state is reached. The newly expanded nodes are evaluated using an evaluation function integrating future rewards, state relevance, and actual outcomes. In this paper, we propose a novel intrinsic reward mechanism to address the limitation of Shannon entropy in handling structured data. To overcome this challenge, we define one-dimensional structural entropy as an intrinsic reward for effective exploration:

<span id="page-4-0"></span>
$$
V(s_t) = H(\mathcal{P}) = \mathbb{E}\left[\sum_{k=0}^{T-k-1} r_{t+k+1} \middle| s_t\right]
$$

$$
\approx \mathcal{H}^1(\mathcal{G}) = -\sum_{s_t \in \mathcal{P}} \frac{d_{s_t}}{\text{vol}(\mathcal{G})} \log_2 \frac{d_{s_t}}{\text{vol}(\mathcal{G})},
$$
 (6)

where P = {st, st+1, · · · , s<sup>T</sup> } denote the selection trajectory of t-th iteration, which ends at the terminal state s<sup>T</sup> after one complete simulation. For simplicity, the notation omits the relationships A between states. Specifically, G is a subgraph of the knowledge graph G, representing a given search space, and we utilize the structural entropy on this subgraph to approximate the state value.

Backpropagation. We update the statistics of each state in the tree that was traversed during the selection stage. Specifically, the back propagation process updates the value estimates and visit counts of all ancestor nodes along the trajectory P as shown in Figure [1d,](#page-2-0) ensuring leaf node evaluation informs higher-level decision-making. The updated rules are as follows:

$$
N(s_t) \leftarrow N(s_t) + 1,
$$

\n
$$
Q(s_t, a) \leftarrow \frac{1}{N(s_t, a)} \sum_{i=1}^{N(s_t)} \mathbb{I}_i(s_t, a) V_i(s_t),
$$
\n(7)

where N(st, a) is the number of times relation action a has been selected from state st, N(st) is the number of times a simulation has been run from state st, and Ii(st, a) is 1 if relation action a was selected from state s<sup>t</sup> on the i-th simulation run from state st, or 0 otherwise.

#### 3 Deficiency Knowledge Synthesis and Repair

As shown in Figure [1f](#page-2-0) to [1h,](#page-2-0) our framework leverages the trajectories with the highest SE values obtained via MCTS to guide synthetic data generation. Specifically, we prompt the LLM agent to synthesize a set of QA pairs based on the identified knowledge path on which the LLM shows high uncertainty, so that the knowledge deficiency of the LLM can be remedied by training on these QA pairs. Formally, as shown in Figures [5](#page-13-0) and [6,](#page-13-1) given a trajectory P = {s1, s2, . . . , s<sup>T</sup> }, the prompt instructs the LLM to generate a question that focuses on P and an answer that logically explains on the relationship ρt+1 between s<sup>t</sup> and its neighboring entities N (st) in P. So that the synthesized QA pair can adhere to the underlying knowledge about the knowledge path and remedy the knowledge deficiency of the LLM. Furthermore, to maintain high data quality, we implement a multi-tiered evaluation mechanism that includes both heuristic rules and LLM-based judgments. Our quality standards encompass: *Format Consistency:*The generated QA pairs must strictly adhere to the predefined prompt template, ensuring that the structure, punctuation, and length conform to our specifications. This guarantees that the synthesized data maintains a uniform format that facilitates downstream processing.*Logical Coherence:*The QA pairs must exhibit clear and rational reasoning. The answer should provide a logically consistent explanation that reflects the relationships and context derived from the knowledge trajectory, ensuring that the data effectively captures and addresses the identified knowledge deficiencies.*Hallucination Avoidance:*The generated content must be grounded in the input trajectory. Specifically, all entities and facts mentioned in the QA pair must originate exclusively from the given trajectory, preventing the introduction of extraneous or unsupported information that could undermine the model's reliability. Data samples that do not meet these criteria are filtered out through our evaluation mechanism [A.1,](#page-13-2) thereby ensuring that only high-quality synthetic data is used to remediate the LLM's knowledge gaps.

The training process can be divided into two stages: First, a knowledge injection stage, that aims to enrich the LLMs with deficiency medical knowledge DK. Second, a medical instruction tuning stage, that tailors the model to align with the medical QA domain. (see Appendix [A.3](#page-14-0) for details).

# 4 Experiments

We conduct experiments on the knowledge-intensive*medical domain*to investigate the following research questions (RQs): RQ1: Can the proposed SENATOR framework effectively repair the knowledge deficiencies of existing LLMs? RQ2: How do different components of our proposed framework impact the performance of LLMs? RQ3: Does the synthetic data successfully incorporate knowledge that lies beyond the distribution of the pretraining corpus? RQ4: What is the scaling regularity of synthetic data on model performance?

## 1 Experimental Settings

Language Models We evaluate our methodology on two categories of LLMs: 1) General LLMs: We employ Llama-3-8B and Qwen2-7B as base models to examine the effectiveness of our approach and include Baichuan2 and Llama-2 for comparison. 2) Medical LLMs: Med-Alpaca [\(Han et al.,](#page-9-9) [2023\)](#page-9-9): Fine-tuned on LLaMA-13B with medical instruction data from Alpaca [\(Han et al., 2023\)](#page-9-9), specifically designed for medical dialogues and question-answering tasks. PMC-LLaMA [\(Wu et al.,](#page-11-13) [2024\)](#page-11-13): Enhanced with biomedical knowledge from 4.8 million academic papers and 30,000 medical books, followed by medical-specific instruction tuning on LLaMA-13B. HuatuoGPT-II [\(Chen et al.,](#page-9-10) [2023\)](#page-9-10): Built on Baichuan [\(Yang et al., 2023a\)](#page-11-14), fine-tuned with distilled ChatGPT data and real-world medical data from doctors.

Datasets Our instruction tuning data D<sup>I</sup> , which contains 514k samples, is derived from [Wu et al.](#page-11-13) [\(2024\)](#page-11-13) to align with the medical domain. It's widely used in the medical field for its large scale and comprehensive coverage of medical knowledge. We evaluate our approach on five standard medical benchmarks: 1) MedQA [\(Jin et al., 2021\)](#page-9-11): Multiple-choice questions from the USMLE assessing medical understanding and reasoning. 2) MedMCQA [\(Pal et al., 2022\)](#page-10-9): Over 194K questions from AIIMS exams covering 2,400 topics across 21 subjects. 3) PubMedQA [\(Jin et al., 2019\)](#page-9-12): A biomedical QA dataset from PubMed abstracts with 1K expert-annotated and 211K generated QA instances, designed to test comprehension and reasoning in biomedical research. 4) GPQA [\(Rein](#page-10-10) [et al., 2023\)](#page-10-10): A high-difficulty multiple-choice dataset validated by experts in biology, physics, and chemistry, focusing on interdisciplinary knowledge and reasoning. 5) MMLU [\(Hendrycks et al.,](#page-9-13) [2020\)](#page-9-13): A comprehensive benchmark covering 57 tasks for evaluating large language models.

Knowledge Graph We conduct experiments based on the SPOKE knowledge graph [\(Morris et al.,](#page-10-11) [2023\)](#page-10-11) due to its comprehensiveness on biological and medical knowledge, which contains over 42 million nodes of 28 different types and 160 million edges of 91 types, constructed by integrating information from 41 different biomedical databases. In this paper, the initial seed entities for MCTS are common disease entities in SPOKE, sourced from [Soman et al.](#page-11-11) [\(2024\)](#page-11-11).

| Model                  | MedQA  | MedMCQA | PubMedQA     | GPQA          |                      | Avg.    |
|------------------------|--------|---------|--------------|---------------|----------------------|---------|
|                        |        |         |              | Genetics      | Molecular<br>Biology |         |
| Human (pass)           | 50.0   | –       | 60.0         | 43.2          |                      | –       |
| Human (expert)         | 87.0   | 90.0    | 78.0         | 66.7          |                      | 80.43   |
| Medical LLMs           |        |         |              |               |                      |         |
| Chat-Doctor (7B)       | 33.93  | 31.10   | 54.3         | –             | –                    | –       |
| Med-Alpaca (13B)       | 30.85  | 31.13   | 53.2         | 10.0<br>15.43 |                      | 28.12   |
| HuatuoGPT-II (7B)      | 41.13  | 41.87   | 54.2         | 22.5<br>21.60 |                      | 36.26   |
| HuatuoGPT-II (13B)     | 45.72  | 38.75   | 51.6         | 20.0<br>27.78 |                      | 36.77   |
| PMC-LLaMA (13B)        | 50.67  | 50.18   | 59.8         | 15.0          | 27.16                | 40.56   |
|                        |        |         | General LLMs |               |                      |         |
| Baichuan2-7B           | 34.56  | 35.12   | 60.2         | 20.0          | 20.99                | 34.17   |
| Baichuan2-13B          | 43.60  | 39.25   | 50.7         | 27.5          | 30.86                | 38.38   |
| Llama-2-7B             | 30.95  | 28.85   | 60.8         | 25.0          | 17.28                | 32.58   |
| Llama-2-13B            | 31.26  | 29.00   | 62.2         | 35.0          | 20.99                | 35.69   |
| Llama-3-8B             | 55.54  | 52.21   | 54.8         | 20.0          | 29.01                | 42.31   |
| w/ instruction tuning  | 54.36  | 50.08   | 56.6         | 25.0          | 25.93                | 42.39   |
| w/ synthetic data + IT | 58.29  | 53.60   | 64.8         | 27.5          | 32.72                | 47.38   |
| ∆ promotion            | +4.95% | +2.66%  | +18.25%      | +37.50%       | +12.79%              | +11.98% |
| Qwen2-7B               | 54.67  | 53.41   | 64.6         | 32.5          | 36.42                | 48.32   |
| w/ instruction tuning  | 59.07  | 59.77   | 61.2         | 22.5          | 35.80                | 47.67   |
| w/ synthetic data + IT | 59.70  | 60.70   | 63.2         | 40.0          | 40.12                | 52.74   |
| ∆ promotion            | +9.20% | +13.65% | -2.17%       | +26.08%       | +10.16%              | +9.15%  |

<span id="page-6-0"></span>Table 1: Main Results on Medical Benchmarks in the Zero-shot Setting. ∆ represents the relative change in performance when using our synthetic data generated by SENATOR compared to the corresponding backbone model. "w/" denote "with" and IT represents instruciton tuning data.

### 2 Main Results (RQ1)

Table [1](#page-6-0) presents the performance of our approach and baseline models across four medical benchmarks. From this, we observe that (1) Through continuous pretraining on medical corpora, previous medical domain LLMs such as PMC-LLaMA could achieve ordinary-human-level performance on certain benchmarks. For example, PMC-LLaMA employs approximately 514k samples, 79 billion tokens of medical data to achieve performances close to such as MedQA and PubMedQA. However, its performance on genetics-related subset of GPQA still shows a substantial gap with human-level, indicating significant knowledge deficiency. (2) In contrast, our proposed SENATOR framework demonstrates its effectiveness in finding knowledge deficiencies to efficiently adapt LLMs to the medical domain. When applied to Llama-3-8B and Qwen2-7B, the SENATOR framework uses a much smaller amount of synthetic data (26k samples, 0.8 million tokens and 128k samples, 3.6 million tokens, respectively) to remedy the targeted knowledge areas, and improve the performance on corresponding benchmarks. For instance, the SENATOR optimizes the Qwen2 model attains an accuracy of 40% on the Genetics component of GPQA, demonstrating that supplementing missing domain-specific data can substantially enhance performance. Overall, on the four medical domainrelated benchmarks, on average, the SENATOR framework improves the performance of Llama-3-8B and Qwen2-7B for 11.98% and 9.15%, respectively. This shows the effectiveness and generality of our approach in comprehensively detecting and remedying the domain-related knowledge for different LLMs. In the following paragraphs (RQ2 and RQ3), we demonstrate that the improvement stems from SENATOR's ability to effectively detect the knowledge deficiencies by synthesizing data beyond the original pretraining corpus, expanding its coverage, and optimizing its distribution.

#### 3 Ablation Study (RQ2)

To validate the efficacy of SENATOR, we conduct ablation studies comparing three configurations: (1) base models, (2) models fine-tuned solely with general domain instruction data D<sup>I</sup> , and (3) models

<span id="page-7-0"></span>![](_page_7_Figure_0.jpeg)
<!-- Image Description: The image presents eight 2D density plots visualizing the distribution of data points across two principal components (PAC Component 1 and PAC Component 2). Each plot represents a different dataset (PubMedQA, MedQA, MedMCQA, and Hybrid) before and after a process (indicated by (a)-(d) and (e)-(h)). Redder colors indicate higher density in one region, while bluer colors indicate higher density in another, showing distinct cluster formations within each dataset. The purpose is to compare the data distribution and clustering characteristics across different datasets and after a specific processing step. -->

Figure 2: Distribution of Pretraining Corpus vs. Synthetic Data. In (a)-(d), blue regions represent the medical pretraining corpus (PubMedQA, MedQA, MedMCQA, and their hybrid), red regions show synthetic data generated by Llama-3. In (e)-(h), red regions indicate synthetic data produced by Qwen2. Darker areas reflect higher concentrations of data points, lighter areas vice versa.

trained with both instructions and synthesized data. As shown in Table [1,](#page-6-0) SFT on general domain instructions alone yields marginal improvements or even performance degradation (Llama-3-8B: 42.31 → 42.39; Qwen2-7B: 48.32 → 47.67). This suggests that the general domain instructions struggle to alleviate the intrinsic knowledge gaps in general-domain LLMs for the specialized medical domain, and constructing more general domain instructions would inevitably be inefficient. In contrast, incorporating synthetic data leads to a significant improvement. For Llama-3-8B, additional synthesized data make average performance improvements of 5.07, with particularly significant gains in underrepresented domains: +7.5 points in GPQA Genetics and +3.71 points in Molecular Biology. Similarly, Qwen2-7B attains 40.0% accuracy in GPQA Genetics (7.5-point increase) and 40.12% in Molecular Biology (3.7-point gain). These results indicate that performance improvement is brought by synthesizing data from detecting the deficiency of LLMs instead of simply enlarging the size of existing instruction data, and a deficiency-oriented synthetic data generation strategy would be a more efficient method for expanding knowledge of LLMs, suggesting a way towards "new fuel" [\(PwC Australia, 2023\)](#page-10-12) for enriching the existing corpus and empowering future LLMs.

#### 4 Analysis for Distribution of Synthesized Data (RQ3)

To examine if our approach can generate synthetic data beyond the original pretraining distribution and address the knowledge deficiency of LLMs, we visualize the distribution of both the original pretraining data, which is sourced from the training sets of PubMedQA, MedQA, and MedMCQA, and the synthetic data. This visualization is achieved by first projecting data into a unified semantic space using 2D UMAP [\(McInnes et al., 2018\)](#page-10-13) and obtaining their distribution using kernel density estimation (KDE) [\(Rosenblat, 1956;](#page-11-15) [Parzen, 1962\)](#page-10-14). From Figure [2](#page-7-0) we can observe: 1) Expanded Coverage by synthetic data: Figures [2a](#page-7-0) to [2h](#page-7-0) reveal that the red area (representing synthetic data) encircles the blue area (pretraining data), indicating that the synthetic data effectively broadens the coverage of the pretraining data. Additionally, Figure [2b](#page-7-0) and [2f](#page-7-0) display smaller blue regions, indicating that the distribution of synthesized data is much broader than the

<span id="page-7-1"></span>![](_page_7_Figure_5.jpeg)
<!-- Image Description: The image displays a 2D kernel density estimation plot showing the distribution of data points across two principal components (PAC Component 1 and PAC Component 2) resulting from a principal component analysis (PCA). The plot reveals several clusters or modes in the data, suggesting distinct subgroups within the dataset. Darker shades of red indicate higher data density. The purpose is likely to visualize data structure and identify potential clusters for further analysis within the paper. -->

Figure 3: Distribution of Data Generated by Llama-3 (red) and Qwen2 (blue).

pretraining data available for MedQA. 2) Distribution Overlap: In Figure [2d,](#page-7-0) the synthetic data

<span id="page-8-0"></span>![](_page_8_Figure_0.jpeg)
<!-- Image Description: The image contains three bar charts and one line chart illustrating the performance of different question answering models. The line chart (a) shows accuracy varying with scaling, while bar charts (b) and (c) compare model accuracy across different data exchange scenarios and subdomains, respectively. Each chart displays accuracy metrics for various models (MedQA, MedMCQA, PubMedQA, Llama, Qwen), with 'Avg' representing average performance across datasets or subdomains. The charts collectively demonstrate the impact of scaling, data exchange, and subdomain variations on model accuracy. -->

Figure 4: Performance differences for various data compositions.

shows a high degree of overlap with the overall pretraining data. We hypothesize that this may be due to Llama-3's relatively weaker grasp of pretraining knowledge compared to Qwen2, causing SENATOR to collect information that Llama-3 did not consolidate well during pretraining. 3) Topic-Specific Differences: Compared to Figure [2a,](#page-7-0) Figure [2e](#page-7-0) exhibits an opposite trend. Accordingly, as indicated in Table [1,](#page-6-0) Qwen2 demonstrates a higher performance on PubMedQA. This is likely because Qwen2 demonstrated a stronger mastery of PubMedQA during pretraining [\(Yang et al.,](#page-12-9) [2024a\)](#page-12-9), leading SENATOR to explore that topic distribution to a lesser extent during the defect detection phase. 4) Global Trends and Localized Discrepancies: The analysis of synthetic data distributions generated by Llama-3 and Qwen2 (Figure [3\)](#page-7-1) shows substantial overlap in high-density areas, indicating that both models have a roughly similar pattern (may also share with more LLMs) in knowledge deficiency about the medical domain. This is because of the similarity in the distribution of the pretraining corpus [\(Lee et al., 2022;](#page-10-15) [Yauney et al., 2023\)](#page-12-10). Such similarity indicates the necessity of systematically reviewing the deficiencies of present LLMs to find common knowledge blind spots in the pretraining corpus, and synthesizing data to complement them. However, there still exist differences in certain locations, suggesting model-specific knowledge deficiencies. This suggests the effectiveness of our approach in targeting model-specific knowledge deficiencies.

#### 5 Analysis of Synthetic Data Scaling (RQ4)

To explore how the amount of synthetic data affects model repair, we integrate different proportions of synthetic data into the SFT stage, as depicted in Figure [4a.](#page-8-0) We observe an upward trend in overall performance, calculated as a weighted average based on dataset sizes, with increasing synthetic data proportions. This indicates that, when the instruction-aligned data D<sup>I</sup> is fixed, expanding the synthetic data enhances model performance. As more synthetic data is used, more LLM knowledge deficiencies can be identified and addressed, thereby improving the model's performance. This highlights the potential of our method to effectively boost model performance by targeting and synthesizing data to fill specific knowledge gaps. Due to the limitation in computation resources, in this paper, for the two base LLMs, Llama and Qwen, we synthesize 26k and 128k data entries, respectively. In future work, we will explore integrating diverse knowledge across more domains to further enhance model performance. Additionally, we compare two settings: the default setting (SENATOR), where each model is fine-tuned using data synthesized using its own detected deficiencies, and the swap setting, where a model is trained with data synthesized using deficiencies of another model, for example, synthetic data produced by Llama-3 is used for SFT of Qwen2, and vice versa. As shown in Figure [4b](#page-8-0) and [4c,](#page-8-0) SENATOR demonstrates effective deficiency correction even under the swap setting. This could be brought by the similarities between the pretraining corpus of different LLMs, which can lead to similar knowledge deficiencies. This finding not only reinforces the potential of our synthetic data as a valuable supplement to human-written corpora, but also highlights the pressing need for efficient and comprehensive strategies to detect and repair knowledge deficiencies in LLMs.

# 5 Conclusion

In this paper, we introduce SENATOR, an innovative framework that utilizes structural entropy and knowledge graphs to detect and repair knowledge deficiencies in LLMs. By employing MCTS within the knowledge space, SENATOR effectively identifies areas where the model's understanding is deficient. Leveraging the SENATOR agent, we direct the synthetic data generation process to

specifically target these deficiencies. Our experiments on medical benchmarks reveal significant performance improvements when models like Llama-3 and Qwen2 are fine-tuned with the synthetic dataset. These results highlight that a deficiency-oriented synthetic data generation strategy represents a highly efficient and sustainable method for expanding knowledge, positioning it as the "new fuel" of modern AI.

# References

- <span id="page-9-6"></span>Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones, Anna Chen, Anna Goldie, Azalia Mirhoseini, Cameron McKinnon, et al. 2022. Constitutional ai: Harmlessness from ai feedback.*arXiv preprint arXiv:2212.08073*.
- <span id="page-9-10"></span>Junying Chen, Xidong Wang, Ke Ji, Anningzhe Gao, Feng Jiang, Shunian Chen, Hongbo Zhang, Dingjie Song, Wenya Xie, Chuyi Kong, et al. 2023. Huatuogpt-ii, one-stage training for medical adaption of llms. *arXiv preprint arXiv:2311.09774*.
- <span id="page-9-0"></span>Yubo Chen, Liheng Xu, Kang Liu, Daojian Zeng, and Jun Zhao. 2015. Event extraction via dynamic multi-pooling convolutional neural networks. In *Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)*, pages 167–176.
- <span id="page-9-2"></span>Mor Geva, Roei Schuster, Jonathan Berant, and Omer Levy. 2021. Transformer feed-forward layers are key-value memories. In *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing*, pages 5484–5495.
- <span id="page-9-8"></span>Anna Goldie, Azalia Mirhoseini, Hao Zhou, Irene Cai, and Christopher D Manning. 2025. Synthetic data generation & multi-step rl for reasoning & tool use. *arXiv preprint arXiv:2504.04736*.
- <span id="page-9-3"></span>Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. 2024. The llama 3 herd of models. *arXiv preprint arXiv:2407.21783*.
- <span id="page-9-7"></span>Hongyi Guo, Yuanshun Yao, Wei Shen, Jiaheng Wei, Xiaoying Zhang, Zhaoran Wang, and Yang Liu. 2024. Human-instruction-free llm self-alignment with limited samples. *arXiv preprint arXiv:2401.06785*.
- <span id="page-9-9"></span>Tianyu Han, Lisa C Adams, Jens-Michalis Papaioannou, Paul Grundmann, Tom Oberhauser, Alexander Löser, Daniel Truhn, and Keno K Bressem. 2023. Medalpaca–an open-source collection of medical conversational ai models and training data. *arXiv preprint arXiv:2304.08247*.
- <span id="page-9-13"></span>Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob Steinhardt. 2020. Measuring massive multitask language understanding. In *International Conference on Learning Representations*.
- <span id="page-9-1"></span>Zhengbao Jiang, Jun Araki, Haibo Ding, and Graham Neubig. 2021. How can we know when language models know? on the calibration of language models for question answering. *Transactions of the Association for Computational Linguistics*, 9:962–977.
- <span id="page-9-4"></span>Zhengbao Jiang, Frank F Xu, Jun Araki, and Graham Neubig. 2020. How can we know what language models know? *Transactions of the Association for Computational Linguistics*, 8:423–438.
- <span id="page-9-11"></span>Di Jin, Eileen Pan, Nassim Oufattole, Wei-Hung Weng, Hanyi Fang, and Peter Szolovits. 2021. What disease does this patient have? a large-scale open domain question answering dataset from medical exams. *Applied Sciences*, 11(14):6421.
- <span id="page-9-12"></span>Qiao Jin, Bhuwan Dhingra, Zhengping Liu, William Cohen, and Xinghua Lu. 2019. Pubmedqa: A dataset for biomedical research question answering. In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)*, pages 2567–2577.
- <span id="page-9-5"></span>Katie Kang, Eric Wallace, Claire Tomlin, Aviral Kumar, and Sergey Levine. 2024. Unfamiliar finetuning examples control how language models hallucinate. *arXiv preprint arXiv:2403.05612*.

- <span id="page-10-15"></span>Katherine Lee, Daphne Ippolito, Andrew Nystrom, Chiyuan Zhang, Douglas Eck, Chris Callison-Burch, and Nicholas Carlini. 2022. Deduplicating training data makes language models better. In *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 8424–8445.
- <span id="page-10-5"></span>Angsheng Li. 2024. *Science of Artificial Intelligence: Mathematical Principles of Intelligence (In Chinese)*. Science Press, Beijing.
- <span id="page-10-4"></span>Angsheng Li and Yicheng Pan. 2016. Structural information and dynamical complexity of networks. *IEEE Transactions on Information Theory*, 62(6):3290–3339.
- <span id="page-10-7"></span>Kenneth Li, Oam Patel, Fernanda Viégas, Hanspeter Pfister, and Martin Wattenberg. 2023a. [Inference](https://proceedings.neurips.cc/paper_files/paper/2023/file/81b8390039b7302c909cb769f8b6cd93-Paper-Conference.pdf)[time intervention: Eliciting truthful answers from a language model.](https://proceedings.neurips.cc/paper_files/paper/2023/file/81b8390039b7302c909cb769f8b6cd93-Paper-Conference.pdf) In *Advances in Neural Information Processing Systems*, volume 36, pages 41451–41530. Curran Associates, Inc.
- <span id="page-10-8"></span>Xian Li, Ping Yu, Chunting Zhou, Timo Schick, Luke Zettlemoyer, Omer Levy, Jason Weston, and Mike Lewis. 2023b. Self-alignment with instruction backtranslation. *arXiv preprint arXiv:2308.06259*.
- <span id="page-10-0"></span>Jian Liu, Leyang Cui, Hanmeng Liu, Dandan Huang, Yile Wang, and Yue Zhang. 2021. Logiqa: a challenge dataset for machine reading comprehension with logical reasoning. In *Proceedings of the Twenty-Ninth International Conference on International Joint Conferences on Artificial Intelligence*, pages 3622–3628.
- <span id="page-10-1"></span>Zimu Lu, Aojun Zhou, Houxing Ren, Ke Wang, Weikang Shi, Junting Pan, Mingjie Zhan, and Hongsheng Li. 2024. Mathgenie: Generating synthetic data with question back-translation for enhancing mathematical reasoning of llms. In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 2732–2747.
- <span id="page-10-2"></span>Alex Mallen, Akari Asai, Victor Zhong, Rajarshi Das, Daniel Khashabi, and Hannaneh Hajishirzi. 2023. When not to trust language models: Investigating effectiveness of parametric and nonparametric memories. In *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 9802–9822.
- <span id="page-10-13"></span>Leland McInnes, John Healy, Nathaniel Saul, and Lukas Großberger. 2018. Umap: Uniform manifold approximation and projection. *Journal of Open Source Software*, 3(29):861.
- <span id="page-10-3"></span>Nicholas Metropolis and Stanislaw Ulam. 1949. The monte carlo method. *Journal of the American statistical association*, 44(247):335–341.
- <span id="page-10-11"></span>John H Morris, Karthik Soman, Rabia E Akbas, Xiaoyuan Zhou, Brett Smith, Elaine C Meng, Conrad C Huang, Gabriel Cerono, Gundolf Schenk, Angela Rizk-Jackson, et al. 2023. The scalable precision medicine open knowledge engine (spoke): a massive knowledge graph of biomedical information. *Bioinformatics*, 39(2):btad080.
- <span id="page-10-9"></span>Ankit Pal, Logesh Kumar Umapathi, and Malaikannan Sankarasubbu. 2022. [Medmcqa: A large-scale](https://proceedings.mlr.press/v174/pal22a.html) [multi-subject multi-choice dataset for medical domain question answering.](https://proceedings.mlr.press/v174/pal22a.html) In *Proceedings of the Conference on Health, Inference, and Learning*, volume 174 of *Proceedings of Machine Learning Research*, pages 248–260. PMLR.
- <span id="page-10-14"></span>Emanuel Parzen. 1962. On estimation of a probability density function and mode. *The annals of mathematical statistics*, 33(3):1065–1076.
- <span id="page-10-12"></span>PwC Australia. 2023. [Synthetic data: The new fuel for ai.](https://www.pwc.com.au/digitalpulse/synthetic-data-the-new-fuel-for-ai.html)
- <span id="page-10-10"></span>David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani, Julian Michael, and Samuel R Bowman. 2023. Gpqa: A graduate-level google-proof q&a benchmark. In *First Conference on Language Modeling*.
- <span id="page-10-6"></span>Ruiyang Ren, Yuhao Wang, Yingqi Qu, Wayne Xin Zhao, Jing Liu, Hao Tian, Hua Wu, Ji-Rong Wen, and Haifeng Wang. 2023. Investigating the factual knowledge boundary of large language models with retrieval augmentation. *arXiv preprint arXiv:2307.11019*.

- <span id="page-11-15"></span>M Rosenblat. 1956. Remarks on some nonparametric estimates of a density function. *Ann. Math. Stat*, 27:832–837.
- <span id="page-11-12"></span>Christopher D Rosin. 2011. Multi-armed bandits with episode context. *Annals of Mathematics and Artificial Intelligence*, 61(3):203–230.
- <span id="page-11-10"></span>Claude E Shannon. 1948. A mathematical theory of communication. *The Bell system technical journal*, 27(3):379–423.
- <span id="page-11-11"></span>Karthik Soman, Peter W Rose, John H Morris, Rabia E Akbas, Brett Smith, Braian Peetoom, Catalina Villouta-Reyes, Gabriel Cerono, Yongmei Shi, Angela Rizk-Jackson, et al. 2024. Biomedical knowledge graph-optimized prompt generation for large language models. *Bioinformatics*, 40(9):btae560.
- <span id="page-11-4"></span>Linxin Song, Xuwei Ding, Jieyu Zhang, Taiwei Shi, Ryotaro Shimizu, Rahul Gupta, Yang Liu, Jian Kang, and Jieyu Zhao. 2025. Discovering knowledge deficiencies of language models on massive knowledge base. *arXiv preprint arXiv:2503.23361*.
- <span id="page-11-8"></span>Zhiqing Sun, Yikang Shen, Qinhong Zhou, Hongxin Zhang, Zhenfang Chen, David Cox, Yiming Yang, and Chuang Gan. 2023. Principle-driven self-alignment of language models from scratch with minimal human supervision. *arXiv preprint arXiv:2305.03047*.
- <span id="page-11-7"></span>Katherine Tian, Eric Mitchell, Huaxiu Yao, Christopher D Manning, and Chelsea Finn. 2024a. [Fine-tuning language models for factuality.](https://openreview.net/forum?id=WPZ2yPag4K) In *The Twelfth International Conference on Learning Representations*.
- <span id="page-11-9"></span>Ye Tian, Baolin Peng, Linfeng Song, Lifeng Jin, Dian Yu, Lei Han, Haitao Mi, and Dong Yu. 2024b. Toward self-improvement of llms via imagination, searching, and criticizing. *Advances in Neural Information Processing Systems*, 37:52723–52748.
- <span id="page-11-1"></span>Yizhong Wang, Yeganeh Kordi, Swaroop Mishra, Alisa Liu, Noah A Smith, Daniel Khashabi, and Hannaneh Hajishirzi. 2023. Self-instruct: Aligning language models with self-generated instructions. In *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 13484–13508.
- <span id="page-11-0"></span>Zifeng Wang, Chun-Liang Li, Vincent Perot, Long Le, Jin Miao, Zizhao Zhang, Chen-Yu Lee, and Tomas Pfister. 2024. Codeclm: Aligning language models with tailored synthetic data. In *Findings of the Association for Computational Linguistics: NAACL 2024*, pages 3712–3729.
- <span id="page-11-2"></span>Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. 2022. Chain-of-thought prompting elicits reasoning in large language models. *Advances in neural information processing systems*, 35:24824–24837.
- <span id="page-11-5"></span>Yifan Wei, Xiaoyan Yu, Ran Song, Hao Peng, and Angsheng Li. 2025. Setke: Knowledge editing for knowledge elements overlap. *arXiv preprint arXiv:2504.20972*.
- <span id="page-11-6"></span>Yifan Wei, Xiaoyan Yu, Yixuan Weng, Huanhuan Ma, Yuanzhe Zhang, Jun Zhao, and Kang Liu. 2024. Does knowledge localization hold true? surprising differences between entity and relation perspectives in language models. In *Proceedings of the 33rd ACM International Conference on Information and Knowledge Management*, pages 4118–4122.
- <span id="page-11-13"></span>Chaoyi Wu, Weixiong Lin, Xiaoman Zhang, Ya Zhang, Weidi Xie, and Yanfeng Wang. 2024. Pmcllama: toward building open-source language models for medicine. *Journal of the American Medical Informatics Association*, 31(9):1833–1843.
- <span id="page-11-3"></span>Kai Xiong, Xiao Ding, Li Du, Jiahao Ying, Ting Liu, Bing Qin, and Yixin Cao. 2024. Diagnosing and remedying knowledge deficiencies in llms via label-free curricular meaningful learning. *arXiv preprint arXiv:2408.11431*.
- <span id="page-11-14"></span>Aiyuan Yang, Bin Xiao, Bingning Wang, Borong Zhang, Ce Bian, Chao Yin, Chenxu Lv, Da Pan, Dian Wang, Dong Yan, et al. 2023a. Baichuan 2: Open large-scale language models. *arXiv preprint arXiv:2309.10305*.

- <span id="page-12-9"></span>An Yang, Baosong Yang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Zhou, Chengpeng Li, Chengyuan Li, Dayiheng Liu, Fei Huang, Guanting Dong, Haoran Wei, Huan Lin, Jialong Tang, Jialin Wang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Ma, Jin Xu, Jingren Zhou, Jinze Bai, Jinzheng He, Junyang Lin, Kai Dang, Keming Lu, Keqin Chen, Kexin Yang, Mei Li, Mingfeng Xue, Na Ni, Pei Zhang, Peng Wang, Ru Peng, Rui Men, Ruize Gao, Runji Lin, Shijie Wang, Shuai Bai, Sinan Tan, Tianhang Zhu, Tianhao Li, Tianyu Liu, Wenbin Ge, Xiaodong Deng, Xiaohuan Zhou, Xingzhang Ren, Xinyu Zhang, Xipin Wei, Xuancheng Ren, Yang Fan, Yang Yao, Yichang Zhang, Yu Wan, Yunfei Chu, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zhihao Fan. 2024a. Qwen2 technical report. *arXiv preprint arXiv:2407.10671*.
- <span id="page-12-3"></span>An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, et al. 2024b. Qwen2. 5 technical report. *arXiv preprint arXiv:2412.15115*.
- <span id="page-12-2"></span>Rui Yang, Haoran Liu, Edison Marrese-Taylor, Qingcheng Zeng, Yuhe Ke, Wanxin Li, Lechao Cheng, Qingyu Chen, James Caverlee, Yutaka Matsuo, et al. 2024c. Kg-rank: Enhancing large language models for medical qa with knowledge graphs and ranking techniques. In *Proceedings of the 23rd Workshop on Biomedical Natural Language Processing*, pages 155–166.
- <span id="page-12-6"></span>Yuqing Yang, Ethan Chern, Xipeng Qiu, Graham Neubig, and Pengfei Liu. 2023b. Alignment for honesty. *arXiv preprint arXiv:2312.07000*.
- <span id="page-12-10"></span>Gregory Yauney, Emily Reif, and David Mimno. 2023. Data similarity is not enough to explain language model performance. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing*, pages 11295–11304.
- <span id="page-12-4"></span>Zhangyue Yin, Qiushi Sun, Qipeng Guo, Jiawen Wu, Xipeng Qiu, and Xuanjing Huang. 2023. [Do large language models know what they don't know?](https://doi.org/10.18653/v1/2023.findings-acl.551) In *Findings of the Association for Computational Linguistics: ACL 2023*, pages 8653–8665, Toronto, Canada. Association for Computational Linguistics.
- <span id="page-12-1"></span>Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai Wang, Shiji Song, and Gao Huang. 2025. Does reinforcement learning really incentivize reasoning capacity in llms beyond the base model? *arXiv preprint arXiv:2504.13837*.
- <span id="page-12-8"></span>Eric Zelikman, Georges Harik, Yijia Shao, Varuna Jayasiri, Nick Haber, and Noah D Goodman. 2024. Quiet-star: Language models can teach themselves to think before speaking. *arXiv preprint arXiv:2403.09629*.
- <span id="page-12-7"></span>Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah Goodman. 2022. Star: Bootstrapping reasoning with reasoning. *Advances in Neural Information Processing Systems*, 35:15476–15488.
- <span id="page-12-5"></span>Hanning Zhang, Shizhe Diao, Yong Lin, Yi R Fung, Qing Lian, Xingyao Wang, Yangyi Chen, Heng Ji, and Tong Zhang. 2023. R-tuning: Teaching large language models to refuse unknown questions. *arXiv preprint arXiv:2311.09677*.
- <span id="page-12-0"></span>Hanyu Zhao, Li Du, Yiming Ju, Chengwei Wu, and Tengfei Pan. 2024. Beyond iid: Optimizing instruction learning from the perspective of instruction interaction and dependency. *arXiv preprint arXiv:2409.07045*.

# A Technical Appendices and Supplementary Material

# <span id="page-13-2"></span>A.1 Prompts for Synthetic Data Generation Stage

This section introduces the prompts (Figure [5](#page-13-0) and [7\)](#page-14-1) defined in our synthetic data generation phase, including the question-answer paris generation prompt, and the evaluation prompt. And Figure [6](#page-13-1) shows a specific example generated by SENATOR using the generation prompt.

<span id="page-13-0"></span>

| Synthetic<br>Data<br>Generator<br>(Step<br>1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| For<br>given<br>facts,<br>generate<br>a<br>question<br>and<br>its<br>corresponding<br>answer.<br>The<br>question<br>should<br>be<br>designed<br>to<br>inquire<br>about<br>the<br>relationship<br>or<br>classification<br>described<br>in<br>the<br>triples,<br>and<br>the<br>answer<br>should<br>be<br>an<br>entity<br>mentioned<br>in<br>the<br>provided<br>facts.<br>Facts:<br>Disease<br><thyroid<br>Gland<br/>Mucoepidermoid<br/>Carcinoma&gt;<br/>is<br/>a<br/>type<br/>of<br/>disease<br/><thyroid<br>gland<br/>carcinoma&gt;.<br/>Compound<br/><liothyronine><br/>treats<br/>disease<br/><thyroid<br>gland<br/>carcinoma&gt;.<br/>Question:<br/>What<br/>compound<br/>can<br/>be<br/>used<br/>to<br/>treat<br/>Thyroid<br/>Gland<br/>Mucoepidermoid<br/>Carcinoma?<br/>Answer:<br/>Liothyronine.</thyroid<br></liothyronine></thyroid<br></thyroid<br>                                                                                                                   |
| Facts:<br>Disease<br><thyroid<br>gland<br/>carcinoma&gt;<br/>resembles<br/>disease<br/><ganglioneuroma><br/>Disease<br/><ganglioneuroma><br/>presents<br/>Symptom<br/><diarrhea><br/>Question:<br/>What<br/>symptom<br/>is<br/>associated<br/>with<br/>the<br/>disease<br/>that<br/>resembles<br/>thyroid<br/>gland<br/>carcinoma?<br/>Answer:<br/>Diarrhea.</diarrhea></ganglioneuroma></ganglioneuroma></thyroid<br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Facts:<br>Disease<br><head<br>and<br/>neck<br/>cancer&gt;<br/>resembles<br/><thyroid<br>gland<br/>carcinoma&gt;.<br/>Disease<br/><head<br>and<br/>neck<br/>cancer&gt;<br/>presents<br/>Symptom<br/><dysphonia>.<br/>Disease<br/><head<br>and<br/>neck<br/>cancer&gt;<br/>presents<br/>Symptom<br/><neck<br>Pain&gt;.<br/>Disease<br/><thyroid<br>gland<br/>carcinoma&gt;<br/>presents<br/>Symptom<br/><dysphonia>.<br/>Disease<br/><thyroid<br>gland<br/>carcinoma&gt;<br/>presents<br/>Symptom<br/><neck<br>Pain&gt;.<br/>Compound<br/><paclitaxel><br/>treats<br/>disease<br/><head<br>and<br/>neck<br/>cancer&gt;.<br/>Question:<br/>What<br/>disease<br/>is<br/>similar<br/>to<br/>thyroid<br/>gland<br/>carcinoma,<br/>with<br/>Symptom<br/>Dysphonia<br/>and<br/>Neck<br/>Pain.<br/>Answer:<br/>Head<br/>and<br/>neck<br/>cancer.</head<br></paclitaxel></neck<br></thyroid<br></dysphonia></thyroid<br></neck<br></head<br></dysphonia></head<br></thyroid<br></head<br> |

Figure 5: Example prompt for the synthetic data generation stage of SENATOR.

# A Smaple Generated by SENATOR

<span id="page-13-1"></span>{generation prompt}

*# Input: Maximum Structual Entropy Trajectory by SENATOR*Disease <hyperphosphatemia> contraindicates the use of compound <Retinol>, Compound <Retinol> is contained in food <hickory nut>, Food <hickory nut> contains compound <Tryptophan>, Compound <Tryptophan> is contained in food <cow milk (liquid)>*# Output: QA Samples generated by the LLMs* Question: What disease is similar to thyroid gland carcinoma, with Symptom Dysphonia and Neck Pain.

Answer: Head and neck cancer.

Figure 6: A specific example generated by SENATOR.

# A.2 Prompts for the SFT Evaluation Stage

This section introduces the evaluation prompt (Figure [8\)](#page-14-2) used after model knowledge repair, as shown in Figure [1h,](#page-2-0) designed to align the model's output answers with the desired format in the medical domain. Specifically, we employ a zero-shot setting in our evaluation to reduce the model's sensitivity bias to few-shot examples.

# Sample Evaluation Scorer (Step 2)

<span id="page-14-1"></span>Your task is to evaluate the given QA Pairs with Evidences based on the following criteria. The criteria should include three parts:

Format: Verify the question is complete (i.e., not truncated) and can be answered with a single, clear answer. Check the answer is complete (i.e., not truncated) and is presented in a single entity or a concise subject-predicate-object statement.

Logic: Confirm that there is a clear, derivable logical connection between the question and the answer based on the provided Evidences.

Hallucination: This examines whether the entities involved in the question and answer exist within the provided Evidences. It determines if additional information beyond the given Evidences was used to construct the samples.

For each QA sample, analyze whetherit meets the above criteria. If the sample satisfies all criteria, output "Correct". Otherwise, output one of the error types that best describes the issue with the sample: Format, Logic, or Hallucination.

Figure 7: Example prompt for the sample filtering stage of SENATOR.

<span id="page-14-2"></span>

| Eval<br>Prompt<br>for<br>Medical<br>Datasets                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Instruction:<br>#<br>Directly<br>answer<br>the<br>best<br>option<br>or<br>Directly<br>answer<br>yes/no/maybe:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| #<br>Example<br>(PubMedQA):<br>#<br>Abstract:<br>Electrical<br>neurostimulation<br>has<br>traditionally<br>been<br>limited<br>to<br>the<br>use<br>of<br>charge-balanced<br>waveforms.<br>Charge-imbalanced<br>and<br>monophasic<br>waveforms<br>are<br>not<br>used<br>to<br>deliver<br>clinical<br>therapy,<br>because<br>it<br>isbelieved<br>that<br>these<br>stimulation<br>paradigms<br>may<br>generate<br>noxious<br>electrochemical<br>species<br>that<br>cause<br>tissue<br>damage.In<br>this<br>study,<br>we<br>investigated<br>the<br>dissolution<br>of<br>platinum<br>as<br>one<br>of<br>such<br>irreversible<br>reactions<br>over<br>a<br>range<br>ofcharge<br>densities<br>up<br>to<br>160<br>μC<br>cm.<br>We<br>observed<br>that<br>platinum<br>dissolution<br>decreased<br>during<br>charge-imbalanced<br>and<br>monophasic<br>stimulation<br>when<br>compared<br>to<br>charge-balanced<br>waveforms<br>#<br>Question:<br>Does<br>electrical<br>neurostimulation<br>with<br>imbalanced<br>waveform<br>mitigate<br>dissolution<br>of<br>platinum<br>electrodes? |
| #<br>Example<br>(MedQA)<br>#<br>A<br>3-month-old<br>baby<br>died<br>suddenly<br>at<br>nightwhile<br>asleep.<br>His<br>mother<br>noticed<br>that<br>he<br>had<br>died<br>only<br>after<br>she<br>awoke<br>in<br>the<br>morning.<br>No<br>cause<br>of<br>death<br>was<br>determined<br>based<br>on<br>the<br>autopsy.<br>Which<br>of<br>the<br>following<br>precautions<br>could<br>have<br>prevented<br>the<br>death<br>ofthe<br>baby?<br>#<br>A.<br>Placing<br>the<br>infant<br>in<br>a<br>supine<br>position<br>on<br>a<br>firm<br>mattress<br>while<br>sleeping.<br>#<br>B.<br>Keeping<br>the<br>infant<br>covered<br>and<br>maintaining<br>a<br>high<br>room<br>temperature.<br>#<br>C.<br>Application<br>of<br>adevice<br>to<br>maintain<br>the<br>sleeping<br>position.<br>#<br>D.<br>Avoiding<br>pacifier<br>use<br>during<br>sleep.                                                                                                                                                                                                                                  |
| #<br>Example<br>(MedMCQA):<br>#<br>Which<br>vitamin<br>is<br>supplied<br>from<br>only<br>animal<br>source:<br>#<br>A.<br>Vitamin<br>C<br>B.<br>Vitamin<br>B7<br>C.<br>Vitamin<br>B12<br>D.<br>Vitamin<br>D                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

Figure 8: Example prompt for the evaluation on medical datasets, where the "#" symbol denotes comments illustrating how a specific data sample is combined with an instruction for zero-shot prompting.

## <span id="page-14-0"></span>A.3 Supervised fine-tuning hyperparameters

We use cross-entropy for supervised fine-tuning. Table [2](#page-15-0) presents the hyperparameters utilized for SFT of LLMs within the SENATOR framework. As shown in Table [2,](#page-15-0) the settings applied to Llama-3-8B are identical to those of Qwen2-7B. Moreover, all experiments conducted in this paper have been performed using the same hyperparameter configuration.

| Table 2: Model Training Parameters in SENATOR |  |
|-----------------------------------------------|--|
|                                               |  |

<span id="page-15-0"></span>

| Model      | Learning Rate | Weight Decay | Warmup Step | Batch Size | Epoch | Maximum Sequence Length |
|------------|---------------|--------------|-------------|------------|-------|-------------------------|
| Llama-3-8B | 9.65e-6       | -1           | -1          | 1          | 3     | 1024                    |
| Qwen2-7B   | 9.65e-6       | -1           | -1          | 1          | 3     | 1024                    |

### A.4 Data Filtering

While our framework demonstrates significant improvements over baseline methods, we acknowledge that the system remains imperfect. To systematically evaluate its limitations, we conduct a manual examination of 501 randomly sampled QA pairs from SENATOR outputs. The analysis revealed that 311 samples (62.08%) met our quality criteria for valid question-answer pairs. The remaining 190 error-containing samples (37.92%) exhibited the following error distribution: Formulaic errors (84 samples; 16.77%): Questions or answers with truncations, formatting inconsistencies, or multi-answer requirements. Logical errors (98 samples; 19.56%): Answers lacking evidential support from the provided knowledge triples. Hallucination errors (8 samples; 1.59%): Answers referencing entities absent in the supporting evidence. Notably, while our approach effectively mitigates hallucination errors through evidence grounding, generating logically consistent QA pairs remains challenging. This primarily stems from the base model's inherent limitations in performing multi-hop reasoning across knowledge path. Appendix [A.6](#page-15-1) illustrates representative examples of these error categories, demonstrating both the framework's capabilities and its current limitations. In order to improve data quality, we set up an additional data filtering module. For format problems, we use regularization to remove samples that do not meet specifications. For logical error types, we use LLMs to judge the logical consistency of QA pairs and evidences, and filter out unsatisfied samples.

#### A.5 Impact of synthetic data on different medical subfields

Similar phenomena as shown in [4](#page-8-0) can also be observed in different medical-related subdomains in the MMLU dataset, as shown in Figure [9.](#page-15-2) Our analysis on Qwen2 shows that without sythetic data generated by SENATOR (ratio = 0), performance is lowest. As synthetic data increases, sub-domain performance improves but with fluctuations. We attribute this to SENATOR's lack of entity type consideration during KG exploration, causing random data domains and non-uniform categories. Future work will focus on adding entity type constraints in MCTS search to explore domain specific knowledge deficiencies more precisely.

<span id="page-15-2"></span>![](_page_15_Figure_6.jpeg)
<!-- Image Description: This heatmap displays the correlation between different medical knowledge domains (Clinical Knowledge, College Medicine, Medical Genetics, Anatomy, College Biology, Professional Medicine, and an Average) and a ratio (likely representing a variable like knowledge retention or performance). Color intensity represents the strength of correlation; darker shades indicate stronger correlations. The purpose is to visualize the relationships between various types of medical knowledge within the context of the paper's research question. -->

Figure 9: Performance across Different Ratios in MMLU Medical Aspects.

#### <span id="page-15-1"></span>A.6 Case Stduy

Our framework SENATOR generates <evidence, question, answer> examples based on the SPOKE knowledge graph. These examples are categorized into four types: Correct, Formulaic errors, Logical errors, and Hallucination errors. Specific examples are

# illustrated in Figures [10](#page-16-0) to [13.](#page-17-0)

## A.7 Details of the Instruction Tuning Dataset

Medical Conversation Data: the dataset includes approximately 100k instances from the ChatDoctor corpus, which contains diverse doctor-patient dialogues collected from real-world scenarios. To enhance instruction diversity and robustness, each prompt is expanded into multiple semantically equivalent forms using GPT-4.

Medical Rationale Question Answering: the dataset incorporates three major multiple-choice QA benchmarks: MedQA (10.2K examples), MedMCQA (183K), and PubMedQA (211K). These datasets evaluate the model's ability to reason over professional medical knowledge. Since many of these resources originally lacked detailed rationales, additional causal explanations were obtained

<span id="page-16-0"></span>

Figure 10: Correct Case.

| Evidence:                                                                                 |
|-------------------------------------------------------------------------------------------|
| Disease $\leq$ primary ciliary dyskinesia 25> is a type of disease $\leq$ primary ciliary |
| dyskinesia>,                                                                              |
| In genetics, disease <primary ciliary="" dyskinesia=""> associates with gene</primary>    |
| <mcidas>,</mcidas>                                                                        |
| Gene <mcidas> downregulated in tissue <ectocervix></ectocervix></mcidas>                  |
|                                                                                           |
| Question:                                                                                 |
| In which tissue is gene MCIDAS upregulated?                                               |
|                                                                                           |
| <b>Answer: Endometrium</b>                                                                |
|                                                                                           |
| Comment: Hallucination error                                                              |

Figure 11: Hallucination Error Case.

by prompting ChatGPT, allowing the model to learn both the correct answer and the underlying reasoning.

Knowledge Graph–Driven Prompting: Furthermore, two smaller datasets—LiveQA (635 examples) and MedicationQA (690 examples)—are included to provide real-world clinical questions and drugrelated knowledge, respectively. Finally, the dataset includes 99K samples derived from the UMLS medical knowledge graph, covering both entity descriptions and inter-entity relationships. This component is particularly useful for aligning the model with structured biomedical ontologies.

Together, these seven resources offer a diverse and comprehensive instruction set D<sup>I</sup> , enabling the model to generalize across conversational, inferential, and knowledge-based medical tasks. More detailed information can be found in the [\(Wu et al., 2024\)](#page-11-13)

# B Limitations

While SENATOR demonstrates promising results in identifying and repairing knowledge deficiencies within LLMs, several limitations remain. First, our framework relies on an external human-curated knowledge graph (KG) to simulate a realistic environment in which the model can perform structured exploration. This setup enables the LLM to iteratively discover and repair its knowledge gaps through

Figure 12: Logical Error Case.

<span id="page-17-0"></span>

Figure 13: Formulaic Error Case.

self-improvement. However, such reliance on a high-quality, domain-specific KG may limit the framework's applicability in settings where such structured resources are incomplete or unavailable. In future work, we plan to explore ways to relax this dependency, such as constructing approximate KGs automatically from textual corpora or using retrieval-augmented methods to complement structural guidance.

Second, while the structural entropy-guided exploration effectively identifies knowledge deficiencies, the process of synthesizing data to repair these deficiencies can be further improved. The quality of synthetic data plays a crucial role in downstream model performance. However, this paper places greater emphasis on detecting and targeting knowledge gaps rather than exhaustively optimizing the data generation process. In our current implementation, we adopt prompt-based synthesis strategies for simplicity and reliability. In future work, we aim to incorporate more advanced techniques—such as instruction-tuned generation, controllable sampling to enhance the relevance, diversity, and factuality of the synthesized data.

# C Broader Impacts

Our work on the SENATOR framework for detecting and repairing knowledge deficiencies in large language models through targeted synthetic data generation has both promising benefits and potential risks for society.

# Positive Impacts

- Improved Reliability in High-Stakes Domains: By systematically identifying and closing knowledge gaps, SENATOR can make LLMs more accurate and trustworthy in domains such as medicine, law, and scientific research, where factual precision is critical for patient care, legal reasoning, and scientific discovery.
- Democratization of Domain-Adapted Models: Synthetic data alleviates the dependence on expensive, expert-annotated corpora, enabling smaller organizations, research labs, and underserved communities to fine-tune powerful LLMs for specialized tasks without prohibitive annotation costs.
- Rapid Adaptation to Emerging Knowledge: In fast-moving fields (e.g., novel pathogens, new regulations), synthetic data guided by up-to-date knowledge graphs can help models stay current, supporting timely decision-making and dissemination of accurate information.

# Negative Impacts

- Bias Amplification and Inaccuracy: If the underlying knowledge graph or pretraining data contain biases or errors, synthetic data may inadvertently reinforce these issues. Models improved on such data could perpetuate harmful stereotypes or spread misinformation.
- Misuse for Misinformation: High-quality synthetic data generation techniques could be exploited to create convincingly false or misleading domain-specific content (e.g., fraudulent medical advice or fabricated legal precedents), posing risks to public trust and safety.
- Overreliance on Synthetic Data: An overconfidence in models fine-tuned primarily on synthetic data might obscure residual blind spots, leading users to place undue trust in automated systems without appropriate human oversight.
- Privacy and Intellectual Property Concerns: If knowledge graphs incorporate sensitive or proprietary information, there is potential for synthetic data to leak or replicate protected content, raising ethical and legal implications.

# D Resource Requirement

We use 8 NVIDIA A100-40G GPUs to SFT Llama-3-8B and Qwen2-7B, and leverage 1-2 NVIDIA A100-40G GPUs for all the inference experiments.

Taking Qwen2-7B as an example, when using synthetic data to SFT Qwen2-7B for knowledge repair, the training time is about 30h on 8 NVIDIA A100-40G GPUs, and a total of 3 epochs are performed. The inference time such as synthetic data generation stage and evaluation stage, measured in seconds per sample, is calculated on an NVIDIA A100 GPU with vllm acceleration (e.g. Qwen2-7B model, which demands at least two A100 GPUs for deployment)
