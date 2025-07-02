---
cite_key: "penalties2016"
title: "Time-R1: Towards Comprehensive Temporal Reasoning in LLMs"
authors: "Large Language Models, Temporal Reasoning"
year: 2016
date_processed: "2025-07-02"
phase2_processed: true
original_folder: "temporal_cognitive_arxiv_2505.13508_Time-R1_Towards_Comprehensive_Temporal_Reasoning_in_LLMs"
images_total: 7
images_kept: 7
images_removed: 0
---

# Time-R1: Towards Comprehensive Temporal Reasoning in LLMs

## Zijia Liu, Peixuan Han, Haofei Yu, Haoru Li, Jiaxuan You

Siebel School of Computing and Data Science, University of Illinois at Urbana-Champaign {zliu331,jiaxuan}@illinois.edu

# Abstract

Large Language Models (LLMs) demonstrate impressive capabilities but lack robust temporal intelligence, struggling to integrate reasoning about the past with predictions and plausible generations of the future. Meanwhile, existing methods typically target isolated temporal skills, such as question answering about past events or basic forecasting, and exhibit poor generalization, particularly when dealing with events beyond their knowledge cutoff or requiring creative foresight. To address these limitations, we introduce *Time-R1*, the first framework to endow a moderate-sized (3B-parameter) LLM with comprehensive temporal abilities: understanding, prediction, and creative generation. Our approach features a novel three-stage development path; the first two constitute a *reinforcement learning (RL) curriculum*driven by a meticulously designed dynamic rule-based reward system. This framework progressively builds (1) foundational temporal understanding and logical event-time mappings from historical data, (2) future event prediction skills for events beyond its knowledge cutoff, and finally (3) enables remarkable generalization to creative future scenario generation without any fine-tuning. Strikingly, experiments demonstrate that Time-R1 outperforms models over 200 times larger, including the state-of-the-art 671B DeepSeek-R1, on highly challenging future event prediction and creative scenario generation benchmarks. This work provides strong evidence that thoughtfully engineered, progressive RL fine-tuning allows smaller, efficient models to achieve superior temporal performance, offering a practical and scalable path towards truly time-aware AI. To foster further research, we also release*Time-Bench*, a large-scale multi-task temporal reasoning dataset derived from 10 years of news data, and our series of *Time-R1*checkpoints.[1](#page-0-0)

# 1 Introduction

Large Language Models (LLMs) have achieved remarkable success across a spectrum of language understanding, generation, and even some complex reasoning tasks[\[1](#page-13-0)[–3\]](#page-13-1). However, a persistent shortcoming in even the most advanced LLMs is their temporal reasoning ability[\[4,](#page-13-2) [5\]](#page-14-0). This encompasses several key capacities[\[6](#page-14-1)[–8\]](#page-14-2): accurately interpreting temporal relationships within their existing knowledge base (such as inferring event times, time differences, event order, and completing temporal entities), predicting the timing of future events based on learned patterns, and creatively generating plausible future events anchored in time. Studies have shown that most LLMs indeed struggle to update or contextualize knowledge under time constraints [\[9\]](#page-14-3); even frontier models have been observed to perform worse than some smaller models in tasks that require integrating new temporal information [\[10\]](#page-14-4). This suggests a systemic weakness in how current LLMs grasp time. This weakness stems from multiple factors: architectural limitations [\[11\]](#page-14-5), such as the lack of explicit

<span id="page-0-0"></span><sup>1</sup>Our code, the Time-Bench dataset, and Time-R1 model checkpoints are available at the project repository: <https://github.com/ulab-uiuc/Time-R1> and via our Hugging Face Collection: [https://huggingface.](https://huggingface.co/collections/ulab-ai/time-r1-682626aea47cb2b876285a16) [co/collections/ulab-ai/time-r1-682626aea47cb2b876285a16](https://huggingface.co/collections/ulab-ai/time-r1-682626aea47cb2b876285a16).

module representation of time; the static nature of their training corpora [\[12\]](#page-14-6), which inevitably become outdated; and the non-chronological training process [\[13\]](#page-14-7), where temporal information across different periods is processed concurrently rather than sequentially, hindering the development of robust logical mappings between events and their corresponding times.

While existing research aims to enhance temporal reasoning—for instance, Zhao*et al.*[\[13\]](#page-14-7) aligned LLM knowledge to target times, Kim*et al.*[\[9\]](#page-14-3) improved temporal consistency, and Yuan*et al.* [\[5\]](#page-14-0) focused on future event prediction, with other works exploring representation methods [\[14,](#page-14-8) [15\]](#page-14-9)—these efforts often target isolated skills. They typically fall short of endowing LLMs with unified, comprehensive temporal intelligence that spans past understanding, future prediction, and creative, time-anchored generation, especially for events beyond their knowledge cutoffs [\[13,](#page-14-7) [5\]](#page-14-0).

In this paper, we aim to bridge this gap by equipping a single 3B-parameter model with compre-

<span id="page-1-0"></span>![](_page_1_Picture_3.jpeg)
<!-- Image Description: The image displays two examples of a natural language processing task. The left panel presents a prediction task: given information about Japan's economic situation (Yen depreciation and weak growth), the model predicts the likely publication date of a related report as February 2025. The right panel shows a text generation task: given a future date (August 2024), the model generates a plausible business news headline, contrasting a generated headline with a more realistic alternative. Both panels illustrate the model's reasoning process. -->

Figure 1: Generated outputs from Time-R1 showcasing its capabilities. (Left) Future Event Time Prediction (Stage 2). (Right) Creative Scenario Generation (Stage 3), with output compared to a real-world headline.

hensive temporal reasoning capabilities through multi-stage Reinforcement Learning (RL), which has become a powerful framework for improving LLM reasoning. Recent frontior models such as OpenAI-o1 [\[16\]](#page-14-10) and DeepSeek-R1 [\[17\]](#page-14-11) utilize RL methods like PPO [\[18\]](#page-14-12) and GRPO [\[19\]](#page-14-13), proving effectiveness to learn complex reasoning capabilities, such as mathematical problem solving and multi-step logical deduction. We build upon Qwen2.5-3B-Instruct, a moderate-sized LLM, and demonstrate that through specialized training it can surpass models over 200× larger (for instance, DeepSeek-R1, a 671B-parameter model) on highly challenging temporal prediction and generation tasks. We propose a three-stage framework with RL and dynamic rewards to progressively establish the model's unified temporal capabilities, spanning temporal logic, future prediction, and time-anchored scenario generation: (1) Stage 1 - Comprehension: RL fine-tune the model using pre-cutoff data from a cold start on four fundamental temporal tasks – timestamp inference, timedifference estimation, events ordering, and masked time entity completion – to develop powerful logical mappings between events and their corresponding times. (2) Stage 2 - Prediction: Further train the model to predict events occurring after knowledge cutoff, thereby teaching it to utilize general reasoning ability built in Stage 1 to extrapolate trends and anticipate future outcomes. (3) Stage 3 - Generation: Directly have the model generate logical future scenario without fine-tuning, leveraging the capabilities obtained from the first two stages.

Through this staged curriculum, the LLM thus progresses from comprehending known temporal facts to skillfully navigating the complexities of the future. This advanced training culminates in robust capabilities for both predicting future event timelines and creatively generating plausible scenarios for unseen future contexts—addressing significant limitations in how current AI handles such challenging forward-looking tasks. Illustrative examples of these advanced future-oriented skills, such as Time-R1's proficiency in forecasting event dates and generating contextually appropriate news headlines for future dates (as depicted in Figure [1\)](#page-1-0), highlight the practical efficacy of our approach.

In summary, the key contributions of our work are as follows: (1) Unified Temporal Reasoning in One Model: We introduce the first LLM that exhibits a holistic temporal reasoning ability encompassing logic, prediction, and generation. (2) Small Model, Big Performance: We show that a relatively small 3B model, when fine-tuned with our meticulously designed multi-stage dynamicreward RL strategy, can match or even exceed the performance of models with hundreds of billions of parameters (*e.g.*, the 671B-parameter R1 model) on temporal prediction and generation tasks. (3) Fast Adaptability and Cost Efficiency: Our approach demonstrates that temporal knowledge can be continuously refreshed in a cost-effective manner. A 3B model can be quickly fine-tuned on new data as time progresses, which is infeasible for a hundreds of billion model that would require enormous computational resources (on the order of millions of dollars for fine-tuning). (4) Resources for the Community: To encourage further research in temporal-aware AI, we release Time-Bench, a dataset of over 200,000 examples with explicit temporal annotations covering diverse tasks including timestamp inference, time-gap estimation, event ordering, and temporal entity completion. We also

release Time-R1, a series of high-performing and continuously updatable temporal reasoning model checkpoints, offering a strong foundation for future time-aware LLM development and iterative refinement.

# 2 Related Work

Temporal Reasoning in LLMs. While adept at many complex tasks [\[17,](#page-14-11) [20\]](#page-14-14), LLMs struggle significantly with temporal reasoning—understanding time and event interrelations—a faculty crucial for comprehensive world understanding and interaction [\[4,](#page-13-2) [21,](#page-14-15) [6\]](#page-14-1). Recent studies increasingly target these deficiencies, often focusing on specific temporal facets. For example, some efforts aim to improve temporal accuracy by aligning LLM knowledge with a target time for time-sensitive questions [\[13\]](#page-14-7). Meantime, some investigate methods for better integrating temporal information into model representations [\[14\]](#page-14-8), while others explore leveraging external knowledge sources or structured representations like temporal graphs to augment LLM capabilities [\[15\]](#page-14-9). However, LLMs exhibit particularly poor generalization when reasoning about the future, especially for events beyond their knowledge cutoff or tasks requiring creative foresight. Consequently, robust methods for direct, challenging future event prediction or creative scenario generation remain scarce in the literature. While some initiatives explore future event prediction and forecasting (e.g., Yuan *et al.*[\[5\]](#page-14-0) employed instruction tuning to predict event occurrences from past contexts), comprehensive approaches addressing the full spectrum of complex and creative future-oriented reasoning are largely underdeveloped.

Reinforcement Learning in LLMs. Reinforcement learning (RL) has recently attracted attention due to its scalability and enhanced generalization capabilities. Building on policy optimization algorithms like PPO [\[18\]](#page-14-12), reinforcement learning from human feedback (RLHF) — the first application of RL to large language models — has become a standard paradigm for aligning LLMs with desired behaviors [\[22,](#page-15-0) [23\]](#page-15-1). Recent advances aim to simplify or improve this process: Direct Preference Optimization (DPO) [\[24\]](#page-15-2) and Simple Preference Optimization (SimPO) [\[25\]](#page-15-3) replace the conventional RL loop with more direct optimization of preference-based rewards, eliminating the need for a separate reward model or reference policy. Other methods are tailored specifically for LLMs; for instance, Group Regularized Policy Optimization (GRPO) [\[19\]](#page-14-13) introduces a group-based reward formulation in place of a single critic, achieving more stable training and better generalization. Likewise, Ahmadian*et al.* [\[26\]](#page-15-4) revisit classic policy gradient techniques [\[27\]](#page-15-5) to propose RLOO (REINFORCE-Leave-One-Out), an online RL algorithm that refines LLM policies with reduced variance and cost. These RL-driven approaches have demonstrated notable gains in LLM reasoning capabilities. In particular, GRPO and related strategies have yielded state-of-the-art performance on complex reasoning tasks including mathematical problem solving [\[19,](#page-14-13) [28\]](#page-15-6), search engine interaction and knowledge retrieval [\[29,](#page-15-7) [30\]](#page-15-8), code generation tasks [\[31\]](#page-15-9) and others [\[32](#page-15-10)[–34\]](#page-15-11). Despite these successes, the application of reinforcement learning to temporally-grounded reasoning remains underexplored. This gap suggests an opportunity to leverage RL methods to develop unified, time-sensitive reasoning abilities in future LLMs.

# 3 Method

This section details the Time-R1 methodology for enhancing LLM temporal capabilities via Reinforcement Learning (RL) fine-tuning. We introduce a novel three-stage training framework (Section [3.2\)](#page-4-0) guided by a dynamic, rule-based reward system (Section [3.3\)](#page-5-0). We first outline the underlying RL optimization setup using Group Relative Policy Optimization (GRPO) (Section [3.1\)](#page-2-0) before detailing these core framework and reward components.

## <span id="page-2-0"></span>3.1 Reinforcement Learning Fine-tuning for Temporal Reasoning

Our approach employs reinforcement learning (RL) to fine-tune a Large Language Model (LLM) for complex temporal reasoning tasks. The core process involves interaction between the LLM policy and a rule-based environment. Given a prompt x detailing a specific temporal task, the LLM, parameterized by θ, generates an output sequence y autoregressively according to its current policy πθ(y | x) = Q<sup>|</sup>y<sup>|</sup> <sup>t</sup>=1 πθ(y<sup>t</sup> | x, y<t).

<span id="page-3-0"></span>![](_page_3_Figure_0.jpeg)
<!-- Image Description: This image depicts a three-stage process, presented as a flowchart. Stage 1 (Comprehension) shows subtask processing (inference, difference, completion, ordering) feeding into a dynamic reward system. Stage 2 (Prediction) uses future event prediction and rule-based rewards, influencing a model parameter (θ₁). Stage 3 (Generation) involves generating, filtering, and evaluating future scenarios based on a model parameter (θ₂). Each stage is represented by a block diagram with icons and textual descriptions, illustrating the data flow and processing steps within a larger system. -->

Figure 2: Overview of the Time-R1 framework. The process consists of three stages: (a) Stage 1 establishes foundational understanding by fine-tuning a base LLM on historical data across four temporal subtasks, driven by reinforcement learning (GRPO) and a dynamic reward system, resulting in model θ1. (b) Stage 2 trains θ<sup>1</sup> for future event time prediction using post-cutoff data and a rule-based reward, producing θ2. (c) Stage 3 leverages θ<sup>2</sup> for inference-based creative future scenario generation, followed by evaluation, without further RL.

Structured Generation Process. To facilitate complex reasoning, interpretability and structured output, we guide the model generation process. For all tasks, the LLM is prompted using specific templates incorporating system instructions (*i.e.*, instructing the model to reason first: "You are a helpful assistant. You first think about the reasoning process in your mind and then provide the user with the answer.") to generate its reasoning within "<think>...</think>" tags, followed by the final answer within "<answer>...</answer>" tags. The entire generated sequence y, encompassing both thought and answer components, constitutes the output evaluated by the environment.

Policy Optimization using GRPO. The environment evaluates the output y using a task-specific dynamic reward function R(x, y) (detailed in Section [3.3\)](#page-5-0). To optimize the policy parameters θ, we utilize Group Relative Policy Optimization (GRPO) [\[19\]](#page-14-13). A key challenge in RL fine-tuning of LLMs is the high variance often associated with policy gradient estimates[\[35\]](#page-15-12). GRPO addresses this by calculating the advantage of a generated response relative to other responses sampled for the same input prompt, thereby providing a more stable learning signal without requiring an auxiliary value function.

Specifically, for a given prompt x, we first sample a batch of K responses {yk} K <sup>k</sup>=1 using a reference policy πref (typically the policy before the update step). After computing the reward R(x, yk) for each response, the group-normalized advantage Aˆ(x, yk) for response y<sup>k</sup> is calculated as:

$$
\hat{A}(x, y_k) = R(x, y_k) - b(x), \text{ where } b(x) = \frac{1}{K} \sum_{j=1}^{K} R(x, y_j).
$$
 (1)

This advantage estimate Aˆ(x, yk) reflects the relative quality of response y<sup>k</sup> compared to the average performance within its group.

To update the policy π<sup>θ</sup> stably using this advantage, we employ a clipped surrogate objective function, similar in structure to that used in PPO [\[18\]](#page-14-12), which helps prevent large, detrimental policy updates. Let the probability ratio be rk(θ) = <sup>π</sup>θ(yk|x) πref(yk|x) . The per-sample clipped objective term is:

$$
L_k^{\text{CLIP}}(\theta) = \min\left(r_k(\theta)\hat{A}(x, y_k), \text{ clip}\left(r_k(\theta), 1 - \epsilon, 1 + \epsilon\right)\hat{A}(x, y_k)\right) \tag{2}
$$

where ϵ is the clipping hyperparameter. The overall objective function JGRPO(θ) maximized during training balances the expected clipped advantage with a KL-divergence penalty against the reference policy πref:

<span id="page-3-1"></span>
$$
\max_{\theta} J_{\text{GRPO}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_k\} \sim \pi_{\text{ref}}} \left[ \frac{1}{K} \sum_{k=1}^{K} L_k^{\text{CLIP}}(\theta) \right] - \beta \mathbb{E}_{x \sim \mathcal{D}} \mathbb{D}_{\text{KL}}[\pi_{\theta}(\cdot \mid x) \parallel \pi_{\text{ref}}(\cdot \mid x)], \quad (3)
$$

where D is the training dataset union, β controls the KL penalty strength, DKL is the Kullback–Leibler divergence, and πref is the stage-specific frozen reference policy (initialized from Qwen2.5-3B-Instruct for Stage 1) used for both advantage calculation reference and KL regularization. This objective guides the policy towards higher rewards, leveraging the stable GRPO advantage estimates within a constrained optimization framework.

### <span id="page-4-0"></span>3.2 Time-R1: A Three-Stage Temporal Learning Framework

To empirically evaluate the effectiveness of our proposed methodology (outlined in Section [3.1\)](#page-2-0), we designed a comprehensive three-stage experimental procedure to train Time-R1, as shown in Figure [2.](#page-3-0) This staged approach aims to progressively cultivate sophisticated temporal logic, prediction, and generation capabilities within the Large Language Model (LLM). We detail each stage below.

### <span id="page-4-1"></span>3.2.1 Stage 1 - Comprehension: Foundational Temporal Understanding via RL Fine-tuning

Objective. The primary goal of this initial stage is to establish a robust foundation for temporal comprehension within the LLM. We aim to instill the ability to interpret fundamental temporal relationships between events and their corresponding times by fine-tuning the model using historical news data from *before*its knowledge cutoff date.

Dataset. We construct a specialized dataset derived from a large corpus of New York Times (NYT) news articles [\[36\]](#page-15-13) (over 200,000) spanning eight years, from January 2016 to December 2023. We extract the headline h and abstract a of the news article to represent each event E,*i.e.*, E = (h, a). Details can be found in Appendix [B.1.](#page-18-0)

Subtasks. From this corpus, we curate data instances tailored to four specific and fundamental temporally-focused and logic-based subtasks [\[37,](#page-15-14) [38\]](#page-15-15): (1) Timestamp Inference: Infer the specific date t (*e.g.*, 2023-12) associated with a described event E. (2) Time-Difference Estimation: Estimate the temporal gap ∆t (*e.g.*, 14 months) between two described events, E<sup>1</sup> and E2. (3) Event Ordering: Determine the correct chronological sequence C (*e.g.*, Event order: 2-1-3) of three events E1, E<sup>2</sup> and E<sup>3</sup> presented out of order. (4) Masked Time Entity Completion: Fill in a masked temporal expression M<sup>e</sup> (*i.e.*, <Year> and <Month>) within a given event description E′ .

In order to help the model develop general logic and indeed acquire the skill to accurately map events to their respective times from textual clues, we force the model to infer each event's date first and then give a task-specific answer for every subtask except the first. Both would be judged a score that would then serve as a part of the reward (see Section [3.3\)](#page-5-0). Consequently, this prevents the model from merely guessing the final answer implicitly. For instance, for the Masked Time Entity Completion task, success hinges on the model's ability to discern detailed semantics from the surrounding text. This is crucial because the specific temporal entity to be completed often refers to a time distinct from the primary date of the event itself, thus pushing the model beyond simple date extraction towards a deeper contextual understanding to answer both correctly. By mastering these diverse subtasks, the LLM (*i.e.*, a model checkpoint, denoted θ1) builds a robust foundational temporal understanding.

### <span id="page-4-2"></span>3.2.2 Stage 2 - Prediction: Future Event Time Prediction via RL Fine-tuning

Objective. After obtaining the foundational capabilities developed in Stage 1, the objective of Stage 2 is to further train the model to predict the timing of future events occurring *after* its initial knowledge cutoff (2023). This involves teaching the model to recall relevant and similar events in the past and their occurrence dates, extrapolate learned temporal development patterns and anticipate future event occurrences based on emerging, post-cutoff information.

Dataset. For Stage 2, the training dataset, denoted D(2) train, is meticulously constructed to facilitate fair evaluation and strictly prevent data leakage from the test period. To ensure a level playing field and align with the knowledge cutoff of the latest baseline models (e.g., DeepSeek-V3-0324-671B with a knowledge cutoff in July 2024), we first incorporate real news data. Specifically, we include a corpus of 7,000 real news articles from January 2024 to July 2024. To train for predicting events beyond this cutoff (August 2024 - February 2025) without using real data from this period, we employ a data synthesis strategy. The synthetic dataset, created using the DeepSeek-V3 model informed by news from May to July 2024, constitutes approximately only half the volume of the real news data used for the earlier months. This approach of using exclusively synthetic data for the future period is a deliberate measure to strictly avoid any potential data leakage, as the test dataset D(2) test is real news events from this period (August 2024 - February 2025). Further details about the datasets can be found in Appendix [B.2.](#page-18-1)

Task. In this stage, the model predicts the specific date t for a news event E based on its extracted headline h and abstract a.

Initializing the model with the checkpoint θ<sup>1</sup> obtained from Stage 1, we continue the fine-tuning process using GRPO on post-cutoff news while carefully controlling the information availability to simulate a true "future prediction" scenario. After training, this stage addresses the challenge that LLMs normally cannot generalize to events post-training [\[39\]](#page-16-0) and results in another model checkpoint, θ2, specialized in future event time prediction.

### 2.3 Stage 3 - Generation: Creative Future Scenario Generation and Evaluation

Objective. In the final stage, we pivot from training to application – aiming to leverage the logical and predictive capabilities instilled in Stages 1 and 2 to enable the fine-tuned model to directly generate plausible, diverse, and temporally coherent future scenarios. This moves beyond predicting specific event times to creatively generating descriptions of hypothetical events given a specific future date.

Methodology. This stage utilizes the model checkpoint θ2, obtained from Stage 2, exclusively for inference without any further RL fine-tuning. The process involves three sequential steps: future news generation, diversity-based filtering, and plausibility evaluation against real news.

First, the model generates hypothesized news events for specified future months M (*i.e.*, July 2024 onwards). To ensure comprehensive topical coverage, generation is conditioned on T = 8 common and distinct themes τ (*e.g.*, Foreign Affairs, Business, Technology, Politics). To enhance the richness of the output pool, each prompt asks the model to create multiple unique news (*i.e.*, 3). This process results in a raw set of generated news items Graw including each month m and theme τ .

Second, to curate a varied and non-redundant set of scenarios for evaluation, a diversity filtering process is applied to the raw generated articles Graw. We compute semantic embeddings g ∈ R 384 for each generated item g using all-MiniLM-L6-v2 encoder [\[40\]](#page-16-1), which retains excellent semantic capture capabilities through knowledge distillation from larger models [\[41\]](#page-16-2). Within each theme τ and month m, a greedy selection algorithm iteratively constructs a diverse subset. This filtering yields a curated set Gfilt,m containing Ndiv = 5 high-diversity news items per theme per month, totaling N<sup>g</sup> = T × Ndiv = 40 representative generated scenarios for each month m.

Finally, the realism and plausibility of the generated future scenarios are quantified through comparison with actual news events from the corresponding future months. The ground truth consists of real news events r from the held-out test dataset D(2) test , partitioned by month m into sets Dreal,m. We compute semantic embeddings A<sup>g</sup> for the filtered generated news items g ∈ Gfilt,m and B<sup>r</sup> for the real news items r ∈ Dreal,m, using the same "all-MiniLM-L6-v2" model. The semantic relatedness between a generated item A<sup>g</sup> and a real item B<sup>r</sup> is measured using cosine similarity: sim(Ag, Br) = cos(ϕ) = <sup>A</sup>g·B<sup>r</sup> ∥Ag∥∥Br∥ , where ϕ represents the angle between the 384-dimensional embedding vectors. To assess overall plausibility for a given month m, we calculate the Average Maximum Similarity (AvgMaxSim) score. For each generated news item Ag,i (i = 1, . . . , Ng), we find its maximum similarity to any real news item in that month, maxBr∈Dreal,m sim(Ag,i, Br). The AvgMaxSim score is the average of these maximum similarity values across all N<sup>g</sup> generated items:

$$
\text{AvgMaxSim}_m = \frac{1}{N_g} \sum_{i=1}^{N_g} \left( \max_{\mathbf{B}_r \in \mathcal{D}_{\text{real},m}} \text{sim}(\mathbf{A}_{g,i}, \mathbf{B}_r) \right)
$$
(4)

This metric quantifies, on average, how closely the generated plausible future events align semantically with events that actually transpired during that month. The process culminates in generating monthly AvgMaxSim reports and visualizations, facilitating quantitative comparisons against baseline generative models or ablations of our framework.

In summary, Stage 3 serves as evidence for the generalization fostered by our first two stages RL framework. It reveals that the strong temporal grounding comprehension and predictive skills learned previously, combined with the LLM's innate linguistic abilities, readily and effectively generalize, allowing the model to anticipate future event dynamics and generate plausible, creative scenarios accordingly, without task-specific fine-tuning for this generative capability.

### <span id="page-5-0"></span>3.3 Reward Design

A meticulously engineered reward function, R(x, y), underpins the success of our Time-R1 framework. Its comprehensive and rigorous design, refined through iterative experimentation, has proven

critical for developing the nuanced temporal reasoning abilities observed in our model (see experimental validation in Section [4,](#page-8-0) detailed analysis in Section [5,](#page-12-0) and more illustration in Appendix). The reward function R(x, y) serves as the primary training signal guiding the policy optimization process outlined in Equation [\(3\)](#page-3-1). We adopt a rule-based dynamic reward system that assesses the correctness and quality of the model's generated output y given the prompt x. The final scalar reward R(x, y) ∈ [−0.8, 1.1] incorporates several components: task-specific accuracy (Racc), format rewards (Rformat), and penalties (Ppenalty) for undesirable outputs, *i.e.*,

<span id="page-6-1"></span>
$$
R(x, y) = Racc + Rformat - Ppenalty
$$
 (5)

### <span id="page-6-3"></span>3.3.1 Universal Bonuses and Penalties Design

Output Parsing and Format. We first parse the content yans within the "<answer>...</answer>" tags. If yans is missing or contains explicit refusal terms like "no event" or "none", a penalty Pno\_event is applied (*i.e.*, Pno\_event∈ {0.1, 0.2} for Stage 1 tasks, and {0.2, 0.3} for Stage 2 prediction, depending on severity).

Common Bonuses and Penalties. A set of bonuses and penalties apply across tasks to encourage well-formed and concise outputs:

- Format Adherence Bonus (Rans\_fmt): A small bonus bfmt = 0.05 is awarded if the content yans adheres to the expected format for the specific task (*e.g.*, "YYYY-MM" format for date inference, and specific structures for multi-part answers). Valid format is also a prerequisite for accuracy scoring. Range: {0, 0.05}.
- Tag Structure Bonus (Rtags): Minor bonuses (btag = 0.025) are given for both the correct presence and count of structural tags (*e.g.*, "<think>", "</answer>"), incentivizing the chain-of-thought structure. Range: [0, 0.05].
- Length and Repetition Penalty (Plen\_rep): A penalty is subtracted to discourage overly verbose or repetitive outputs; this mechanism has proven particularly effective in our empirical experiments (see cases in Appendices [E](#page-21-0) and [F\)](#page-23-0). Range: [0, 0.5].

$$
P_{\text{len\_rep}} = \max(P_{\text{length}}, P_{\text{repetition}}) \tag{6}
$$

where Plength penalizes responses (of N tokens) exceeding a length threshold Lthresh (*i.e.*, 900 tokens) to prevent them from approaching the maximum allowed length Lmax (*i.e.*, 1024 tokens). This is calculated as:

$$
P_{\text{length}} = \min(1.0, \frac{N - L_{thresh}}{L_{max} - L_{thresh}}) \times 0.3, \quad \text{if } N > L_{thresh} \tag{7}
$$

Prepetition is the maximum of three distinct repetition penalties:

$$
P_{\text{repetition}} = \max(P_{\text{word\_repeat}}, P_{\text{phrase\_repeat}}, P_{\text{ngram\_diversity}})
$$
\n(8)

where Pword\_repeat penalizes sequences of more than 5 identical consecutive words, Pphrase\_repeat penalizes recurring phrases, and Pngram\_diversity penalizes insufficient global n-gram diversity. The combined penalty Prepetition∈ [0, 0.5].

### <span id="page-6-2"></span>3.3.2 Task-Specific Accuracy Score.

Accuracy score (Racc∈ [0, 1]) is the core component of our reward mechanism, varying by task:

Timestamp Inference: The task is to infer the date t<sup>p</sup> for a given event E. Let tgt be the ground truth date. The accuracy score is based on the temporal distance ∆m(tp, tgt) (in months) between the inference and target:

<span id="page-6-0"></span>
$$
R_{\rm acc} = R_{\rm date}(t_p, t_{gt}, \alpha) = e^{(-\alpha \cdot \Delta m(t_p, t_{gt}))} \tag{9}
$$

where α is a decay coefficient. For Stage 1 inference, α is dynamically adjusted based on sample difficulty and training step (ranging between 0.07 and 0.1). This exponential reward structure, particularly when coupled with the dynamic α, ensures that the reward signal clearly reflects the proximity of the inferred date to the ground truth, effectively allowing the model to perceive the magnitude of its temporal error ∆m(tp, tgt). See Section [3.3.3](#page-7-0) and Section [4.5.1](#page-11-0) for more discussion. Time-Difference Estimation: The task is to infer the dates tp1, tp<sup>2</sup> of two events and their difference ∆t<sup>p</sup> (in months). Let ground truths be tgt1, tgt2, ∆tgt. The reward combines accuracy on dates and the difference, weighted (w<sup>d</sup> = 0.25, w∆<sup>t</sup> = 0.5), and includes an inconsistency penalty:

$$
R_{\text{acc}} = (w_d R_{d1} + w_d R_{d2} + w_{\Delta t} R_{\Delta t}) \cdot P_{\text{incon}} \tag{10}
$$

where Rd<sup>1</sup> = Rdate(tp1, tgt1, α1) and Rd<sup>2</sup> = Rdate(tp2, tgt2, α2) are date accuracy, using dynamic α1, α2. R∆<sup>t</sup> = e (−α∆t·|∆tp−∆tgt|) denotes difference accuracy, where α∆<sup>t</sup> = 0.05 if ∆t<sup>p</sup> ≥ 25, otherwise α∆<sup>t</sup> = 0.1 or (α<sup>1</sup> + α2)/2 depending on the dynamic strategy process, to balance the reward and to encourage more robust estimation even when the model is dealing with events separated by large time differences. The inconsistency penalty factor (Pincon ∈ (0, 1]) penalizes discrepancies between the explicitly inferred difference ∆t<sup>p</sup> and the difference implied by the inferred dates |tp<sup>2</sup> − tp1|; this penalty is designed to ensure the internal logical consistency of the model's output. Let the error be ∆incon = ||tp<sup>2</sup> − tp1| − ∆tp|. Then Pincon = e (−αincon·∆incon) , where the decay αincon is smaller for larger ∆t<sup>p</sup> (base αincon = 0.1, scaled down if ∆t<sup>p</sup> ≥ 25). The learning dynamics of Pincon, illustrating the model's progressive adherence to this logical constraint, are presented in Appendix [C.](#page-19-0)

### Event Ordering:

The task involves inferring dates tp1, tp2, tp<sup>3</sup> and the correct chronological order C<sup>p</sup> (permutation) for three events E1, E2, E3. Let ground truths be tgt1, tgt2, tgt3, Cgt. The reward combines accuracy on dates and the order, weighted (w<sup>d</sup> = 0.2, word = 0.4), and includes both an inconsistency penalty and a diversity penalty:

$$
R_{\text{acc}} = (w_d \sum_{i=1}^{3} R_{di} + w_{\text{ord}} R_{\text{order}}) \cdot P_{\text{incon}} \cdot P_{\text{div}}
$$
 (11)

where Rdi = Rdate(tpi, tgti, αi) for i = 1, 2, 3 is date accuracy, using dynamic α<sup>i</sup> . Rorder represents order accuracy, calculated based on the number of correctly ordered pairs in C<sup>p</sup> compared to Cgt (*i.e.*, Rorder = Ncorrect\_pair/Ntotal\_pair, where Ntotal\_pair = 3). The inconsistency penalty factor (Pincon ∈ {0.2, 0.4, 0.7, 1.0}) penalizes if the inferred order C<sup>p</sup> contradicts the order implied by the inferred dates tp1, tp2, tp<sup>3</sup> (based on pairwise similarity), thereby ensuring the model's explicit ordering aligns with the chronology of its inferred event dates. The diversity penalty factor (Pdiv ∈ {0.2, 1.0}) penalizes trivial solutions where all inferred dates tpi are identical, or where dates are sequential (*e.g.*, tp<sup>3</sup> − tp<sup>2</sup> = tp<sup>2</sup> − tp<sup>1</sup> = 1) and the order is trivial (*e.g.*, 1-2-3); this encourages the model to infer more varied and realistic event date distributions rather than collapsing to overly simplistic patterns. Pincon and Pdiv are both proven effective in empirical experiments (see Appendix [C\)](#page-19-0).

Masked Time Entity Completion: The task is to infer the date t<sup>p</sup> of an event E′ and a masked entity Me\_<sup>p</sup> (either Year or Month). Let ground truths be tgt, Me\_gt. The reward combines accuracy on the date and the entity, weighted (w<sup>d</sup> = w<sup>e</sup> = 0.5):

$$
R_{\text{acc}} = w_d R_{\text{date}} + w_e R_{\text{entity}} \tag{12}
$$

where Rentity = e (−3α·∆mc) denotes entity accuracy, using dynamic α. When the masked entity is "Month", ∆m<sup>c</sup> represents the circular difference of exact or variant month name to better capture the proximity, *i.e.*, ∆m<sup>c</sup> = min(|M<sup>e</sup>\_<sup>p</sup> − M<sup>e</sup>\_gt|, 12 − |M<sup>e</sup>\_<sup>p</sup> − M<sup>e</sup>\_gt|).

Future Event Prediction: Similar to the Timestamp Inference task but for future events, however, this task employs a stricter evaluation standard as the model already has foundational temporal comprehension. Thus, the decay coefficient is a fixed larger value (*i.e.*, α = 0.1) in Equation [\(9\)](#page-6-0), resulting in more severe penalties for prediction errors.

### <span id="page-7-0"></span>3.3.3 Dynamic Reward Mechanism

To address the cold-start challenge inherent in fine-tuning LLMs for specialized temporal tasks and to foster robust performance[\[28\]](#page-15-6), particularly on more difficult examples, we employ a dynamic reward mechanism specifically during the Stage 1 RL fine-tuning process ( more discussion can be found at Section [4.5.1\)](#page-11-0). This mechanism utilizes curriculum learning principles by adaptively adjusting the decay coefficient α used in the date accuracy reward component (Equation [\(9\)](#page-6-0)) based on data difficulty and training progression. This dynamic adjustment applies whenever Rdate is calculated for any Stage 1 subtask involving date inference (*i.e.*, all four subtasks).

First, we stratify the Stage 1 training dataset based on difficulty. Using an initial model checkpoint (*i.e.*, Qwen2.5-3B-Instruct), we perform Timestamp Inference task for all training samples. Samples where the absolute error in months (∆m) is less than or equal to 3 (∆m ≤ 3) are classified as "easy" level, while the remainder are classified as "normal/hard".

The curriculum then proceeds in three sequential training steps, each building upon the model checkpoint from the previous step:

Phase 1: Foundational Logic and Format Learning. Initially, fine-tuning focuses exclusively on the Timestamp Inference task using only the samples classified as easy. During this step, we employ a fixed, relatively strict decay coefficient α = αtarget = 0.1 in Equation [\(9\)](#page-6-0). The primary goal is to enable the model to rapidly learn the fundamental task logic, establish correct response formatting, and build a solid foundation before encountering more complex tasks or difficult samples.

Phase 2: Exploration on Full Task Suite. Next, training expands to encompass all four Stage 1 subtasks and utilizes the full dataset (easy, normal, hard samples). For samples classified as normal/hard, we apply a lower, fixed decay coefficient α = αstart = 0.07. This more lenient penalty function encourages the model to explore diverse reasoning pathways for challenging instances across all tasks without being excessively penalized for initial inaccuracies. Easy samples continue to be evaluated using the stricter α = 0.1.

Phase 3: Transition to Strict Evaluation. Finally, while continuing to train on all tasks and difficulty levels, we progressively increase the evaluation strictness for the normal/hard samples. The decay coefficient α for these samples transitions linearly from αstart = 0.07 up to αtarget = 0.1 over stransition = 50 steps within this training phase, after which it remains fixed at αtarget = 0.1 for any subsequent steps. Let s be the current training step within this phase. The adaptive alpha αtransition(s) for normal/hard samples, is calculated as:

$$
\alpha_{\text{transition}}(s) = \alpha_{\text{start}} + (\alpha_{\text{target}} - \alpha_{\text{start}}) \cdot \min(1.0, s/s_{\text{transition}})
$$
(13)

This gradual tightening of the reward function encourages the model to refine its precision on more difficult examples, adapting it towards the stricter evaluation standard (α = 0.1). This step aims to cultivate high accuracy across the entire data distribution by the end of Stage 1.

Importantly, this dynamic α adjustment schedule is employed strictly during the Stage 1 training process. For all evaluations performed on the test datasets (across all stages where applicable), we consistently use a fixed decay coefficient α = 0.1 for all samples to ensure stable and comparable assessment of model performance.

### 3.4 Final Reward Calculation.

In summary, the total score R(x, y) for a given task is computed by summing the relevant accuracy score and bonuses, then subtracting penalties introduced above. Thus, Equation [\(5\)](#page-6-1) can be further expressed as:

$$
R(x, y) = R_{\text{acc}} + R_{\text{ans\_fmt}} + R_{\text{tags}} - P_{\text{no\_event}} - P_{\text{len\_rep}} \tag{14}
$$

Aggregating the potential minimum and maximum values of these components yields a range of [−0.8, 1.1] for the total score R(x, y).

# <span id="page-8-0"></span>4 Experiments

## 1 Datasets.

We utilize the datasets constructed from the New York Times (NYT) as described in Section [3.2.](#page-4-0)

### 2 Baselines

To rigorously evaluate the performance of Time-R1, we compare it against two categories of six baseline models: (1) Instruction-Tuned LLMs of Varying Scales: Qwen2.5-3B-Instruct (the base model for Time-R1), Qwen2.5-7B-Instruct [\[42\]](#page-16-3) and Llama-3.1-8B-Instruct [\[43\]](#page-16-4) (mediumscale models), and DeepSeek-V3-0324-671B [\[44\]](#page-16-5) (an extra-large generalist foundation model). (1) Specialized Reasoning LLMs: DeepSeek-Distill-Qwen-32B (a larger model with a strong emphasis on reasoning), and DeepSeek-R1-671B [\[17\]](#page-14-11) (recognized for its state-of-the-art performance on a

wide array of complex reasoning benchmarks). This comparison helps determine whether advanced, broad reasoning skills on well-trained models even with exceptionally large-scale can inherently address complex temporal tasks.

### <span id="page-9-1"></span>4.3 Experimental Setup

Implementation. All our experiments build upon Qwen2.5-3B-Instruct [\[42\]](#page-16-3), a moderate size for fast adaptability and cost efficiency. We implement our three-stage RL fine-tuning framework using veRL framework [\[45\]](#page-16-6), adopting the GRPO algorithm detailed in Equation [\(3\)](#page-3-1). All RL fine-tuning experiments were conducted on four NVIDIA A6000 GPUs.

Hyperparameters. Key hyperparameters for the GRPO optimization include KL coefficient β = 0.001, and K = 5 rollout responses per prompt for group-normalized advantage estimation. The full configuration details can be found at Appendix [A.](#page-17-0)

### 4 Main Results

We now present the core experimental results, evaluating the performance of Time-R1 across its training stages against the established baselines. We specifically report on the performance of the model checkpoint after Stage 1 (θ1) for foundational tasks and the checkpoint after Stage 2 (θ2) for future prediction and scenario generation.

### <span id="page-9-2"></span>4.4.1 Stage 1: Foundational Temporal Reasoning Performance

The effectiveness of our Stage 1 fine-tuning on core temporal understanding is demonstrated by the training dynamics in Figure [3](#page-9-0) (see appendix [C](#page-19-0) for details of fine-tuning curves for all subtasks and phases) and the final scores in Table [1.](#page-10-0) The results highlight the substantial benefits of our Stage 1 RL fine-tuning. Time-R1 (θ1) demonstrates a remarkable improvement in its overall average score, with an increase of approximately 171.6% over its base Qwen2.5-3B-Instruct model.

Significantly, with these improvements, Time-R1 now outperforms the much larger DeepSeek-V3- 0324-671B model and is highly competitive with the state-of-the-art 671B DeepSeek-R1 model. It secures the top performance on the demanding Completion task and the second-best performance on the challenging Event Ordering task. This strong performance, rivaling or exceeding much larger baselines, is largely attributed to our meticulously designed task-specific rewards and the dynamic reward curriculum. For instance, the inconsistency and diversity penalties for Event Ordering (detailed in Section [3.3.2\)](#page-6-2) are pivotal. The learning curves in Appendix [C](#page-19-0) also illustrate that the

<span id="page-9-0"></span>![](_page_9_Figure_9.jpeg)
<!-- Image Description: The image contains two line graphs (a) and (b) showing training performance. Graph (a) displays the average total score over training steps for several large language models (LLMs), including Time-R1 and various Qwen and Llama models. Graph (b) shows the completion score (a subset of the total score) for the same LLMs. Both graphs illustrate the models' performance improvement during training, allowing comparison of their learning curves. Horizontal dashed lines indicate baseline scores. -->

Figure 3: Stage 1 Training Performance *vs.*Baselines. Training curves for Time-R1 (θ1) and its ablation variant, Time-R1-Fixed-Reward (θ ′ 1 ), evaluated against baseline models (indicated by horizontal dashed lines). Plot (a) shows the Overall Total Score across all subtasks, while plot (b) presents the Masked Time Entity Completion subtask. The solid lines demonstrate our models' scores improving throughout the training process, ultimately surpassing the performance levels of most baseline models, including those with significantly larger scales.

<span id="page-10-0"></span>Table 1: Stage 1 Foundational Temporal Reasoning Performance. Average Total Score (R(x, y)) on the four subtasks and overall. Higher scores indicate better performance. Best score in each column is bold, second best is underlined.

| Model                                                          | Overall Avg. ↑   | Ordering ↑       | Completion ↑     | Inference ↑      | Difference ↑     |
|----------------------------------------------------------------|------------------|------------------|------------------|------------------|------------------|
| Qwen2.5-3B-Instruct                                            | 0.2384           | 0.1583           | 0.2217           | 0.3372           | 0.2363           |
| Qwen2.5-7B-Instruct                                            | 0.3092           | 0.2775           | 0.2953           | 0.3366           | 0.3275           |
| Llama-3.1-8B-Instruct                                          | 0.2492           | 0.2239           | 0.2008           | 0.3339           | 0.2383           |
| DeepSeek-Distill-Qwen-32B                                      | 0.4702           | 0.5026           | 0.3943           | 0.5264           | 0.4576           |
| DeepSeek-V3-0324-671B                                          | 0.6471           | 0.6409           | 0.6777           | 0.6796           | 0.5901           |
| DeepSeek-R1-671B                                               | 0.6916           | 0.6848           | 0.7493           | 0.7145           | 0.6172           |
| Time-R1-Fixed-Reward (θ<br>′<br>, 3B)<br>1<br>Time-R1 (θ1, 3B) | 0.6259<br>0.6476 | 0.6623<br>0.6815 | 0.6977<br>0.7555 | 0.5813<br>0.5938 | 0.5621<br>0.5599 |

model's adherence to response consistency and diversity for this task steadily improves, reflecting enhanced logical reasoning. Such effective instillation of logical mapping allows Time-R1 to compete effectively with much larger models on these complex temporal logic challenges.

To validate the contribution of our reward design, we include an ablation model, Time-R1-Fixed-Reward (θ ′ 1 ), which was trained using a static, strict reward function. As shown in Figure [3,](#page-9-0) the full Time-R1 model consistently outperforms this ablation variant, underscoring the importance of the dynamic curriculum, which will be analyzed further in Section [4.5.1.](#page-11-0)

### 4.2 Stage 2: Future Event Time Prediction

Stage 2 equips models to predict event timing post-knowledge cutoff (2023). We assess our full pipeline and Stage 1's impact by evaluating two variants: Time-R1 (θ2, 3B) (full curriculum, Section [3.2\)](#page-4-0) and an ablation model, Time-R1- S2-Direct (θ ′ 2 , 3B) (Stage 2 fine-tuning only, from base Qwen2.5-3B-Instruct, omitting Stage 1). Performance is compared against baselines for August 2024 - February 2025 predictions.

The overall Stage 2 performance, measured by Average Total Score R(x, y) with strict evaluation (α = 0.1), is presented in Table [2.](#page-11-1) While models show clear improvement over Stage 1 Inference tasks, likely aided by a narrower prediction time span, further significant gains prove challenging. For instance, the DS-Qwen-32B model, despite its scale and specialized complex reasoning training, scores lower than some 3B models lacking such enhancements (*e.g.*, the base Qwen2.5-3B-Instruct), underscoring the inherent difficulty of learning extrapolation and

<span id="page-10-1"></span>![](_page_10_Figure_7.jpeg)
<!-- Image Description: The image displays a line graph showing the average total scores of several large language models (LLMs) over time (August 2024 to February 2025). Each line represents a different LLM (e.g., Time-R1, Qwen2.5-3B-Instruct, DeepSeek-R1-671B), with the y-axis indicating the average total score and the x-axis representing the month. The graph likely illustrates the performance trend of various LLMs over time, possibly indicating model improvements or degradation. -->

Figure 4: Monthly Average Total Score R(x, y) for Stage 2 Future Event Prediction (August 2024 - Feb 2025). Compares Time-R1 variants (θ<sup>2</sup> and θ ′ 2 ) against baselines. Evaluated with α = 0.1.

handling post-cutoff data.Our primary model, Time-R1 (θ2, 3B), achieves the highest score. This strong performance, consistent across the prediction horizon (Figure [4\)](#page-10-1), shows it generally outperforming most baselines, including the much larger DeepSeek-R1-671B and DeepSeek-V3-671B models. This robust result strongly supports our hypothesis that specialized, staged temporal finetuning enables smaller models to achieve superior performance on challenging future prediction tasks. Furthermore, these findings highlight general LLM weaknesses in temporal reasoning and underscore the efficacy and necessity of our structured training framework. The foundational understanding from Stage 1, combined with Stage 2's predictive skill development, underpins this strong near-future temporal reasoning (see Section [5.2](#page-13-3) for challenges facing standard LLMs). The ablation model, Time-R1-S2-Direct (θ ′ 2 , 3B), also demonstrates solid performance, outperforming several baselines and indicating Stage 2 RL fine-tuning's standalone effectiveness. See more discussion on Section [4.5.2.](#page-12-1)

<span id="page-11-1"></span>Table 2: Stage 2 Future Event Prediction Performance (Overall). Average Total Score R(x, y) evaluated with α = 0.1. Higher scores are better. Best score is bold, second best is underlined. θ<sup>2</sup> checkpoint of Time-R1 is used.

| Metric             | Qwen2.5<br>-3B | Qwen2.5<br>-7B | Llama-3.1<br>-8B | DS-Qwen<br>-32B | DS-V3<br>-671B | DS-R1<br>-671B | Time-R1<br>′<br>, 3B)<br>(θ<br>2 | Time-R1<br>(θ2, 3B) |
|--------------------|----------------|----------------|------------------|-----------------|----------------|----------------|----------------------------------|---------------------|
| Avg. Total Score ↑ | 0.6036         | 0.6226         | 0.6015           | 0.5997          | 0.7036         | 0.7503         | 0.7331                           | 0.7780              |

### 4.3 Stage 3: Creative Scenario Generation Quality

Finally, we evaluate model generalization to generating plausible future scenarios—a task without explicit fine-tuning. Table [3](#page-11-2) presents AvgMaxSim scores, quantifying the semantic plausibility of generated news scenarios against real news events (August 2024 - February 2025). Results demonstrate Time-R1 (θ2, 3B)'s strong generalization capability. It achieves the highest overall AvgMaxSim score, surpassing all baseline models, including the very large DeepSeek-V3-0324- 671B and DeepSeek-R1-671B. Monthly scores for Time-R1 (θ2, 3B) also reveal consistently strong performance. This Stage 3 success, achieved without direct training on generation, underscores the S1+S2 curriculum's effectiveness in building robust, transferable temporal reasoning. These capabilities are significant for addressing research gaps in challenging future prediction and generation tasks and demonstrate practical application value. Our ablation model, Time-R1-S2-Direct (θ ′ 2 , 3B), also performs commendably, outperforming some baselines (further discussion in Section [4.5.2\)](#page-12-1).

<span id="page-11-2"></span>Table 3: Stage 3 Creative Scenario Generation Plausibility (AvgMaxSim Scores (%)). Compares semantic similarity of generated scenarios to real news events (August 2024 - Feb 2025). Higher scores indicate better plausibility. Best overall average is bold, second best is underlined.

| Model                                   | Avg. (%) | Monthly AvgMaxSim Scores (%) |       |       |       |       |       |       |
|-----------------------------------------|----------|------------------------------|-------|-------|-------|-------|-------|-------|
|                                         | ↑        | 24-08                        | 24-09 | 24-10 | 24-11 | 24-12 | 25-01 | 25-02 |
| Qwen2.5-3B-Instruct                     | 47.66    | 47.27                        | 46.89 | 47.39 | 48.57 | 48.77 | 47.76 | 46.94 |
| Qwen2.5-7B-Instruct                     | 47.59    | 46.99                        | 49.78 | 46.18 | 48.53 | 46.91 | 48.88 | 45.83 |
| Llama-3.1-8B-Instruct                   | 47.96    | 48.99                        | 50.03 | 47.42 | 46.21 | 47.06 | 48.01 | 48.03 |
| DeepSeek-Distill-Qwen-32B               | 47.12    | 46.58                        | 46.78 | 47.94 | 47.04 | 48.40 | 47.30 | 45.81 |
| DeepSeek-V3-0324-671B                   | 48.81    | 50.73                        | 51.77 | 48.60 | 48.46 | 47.52 | 47.71 | 46.85 |
| DeepSeek-R1-671B                        | 47.46    | 47.55                        | 49.64 | 47.29 | 45.29 | 47.85 | 47.30 | 47.31 |
| ′<br>Time-R1-S2-Direct (θ<br>, 3B)<br>2 | 47.93    | 47.89                        | 47.11 | 47.95 | 48.29 | 46.05 | 50.69 | 47.52 |
| Time-R1 (θ2, 3B)                        | 48.90    | 47.75                        | 48.29 | 49.81 | 48.77 | 49.03 | 50.81 | 47.83 |

### 5 Ablation Studies

### <span id="page-11-0"></span>4.5.1 Impact of Dynamic Reward Mechanism

Our methodology (Section [3.3.3\)](#page-7-0) employs a dynamic reward mechanism during Stage 1 fine-tuning. This curriculum learning approach, with its phased adjustment of reward strictness (from lenient αstart = 0.07 to strict αtarget = 0.1), is designed to mitigate cold-start challenges and guide the model towards robust performance on complex temporal tasks. We hypothesized this would lead to superior learning compared to a static, strict reward function.

The empirical results presented in Figure [3](#page-9-0) validate this hypothesis. The advantage of the dynamic reward curriculum is evident both in the Overall Total Score across all subtasks (Figure [3a](#page-9-0)) and in the specific Masked Time Entity Completion subtask (Figure [3b](#page-9-0)). For the overall performance, the full Time-R1 model achieves a consistently higher and more stable score than the fixed-reward ablation model. This performance gap is even more pronounced in the Completion subtask, where the fixed-reward model's progress begins to slow and plateau around a score of 0.70. In contrast, the curriculum-trained model continues to improve, achieving a significantly higher and more stable final score of over 0.75. This suggests that the curriculum's initial leniency and gradual transition to stricter evaluation criteria enable more effective exploration and learning, preventing convergence to a sub-optimal policy and leading to a better mastery of the task.

### <span id="page-12-1"></span>4.5.2 Impact of Staged Curriculum Learning

To quantify the impact of our staged curriculum, particularly the foundational comprehension from Stage 1, we compared our full model, Time-R1 (θ2, 3B) (S1+S2 training), against Time-R1-S2-Direct (θ ′ 2 , 3B) (S2 training only).

The results unequivocally highlight the benefits of the full curriculum. In Future Event Time Prediction (Stage 2, Table [2,](#page-11-1) Figure [4\)](#page-10-1), Time-R1 (θ2, 3B) (0.7780) significantly outperformed Time-R1-S2-Direct (θ ′ 2 , 3B) (0.7331). This advantage persisted in Stage 3 Creative Scenario Generation (Table [3\)](#page-11-2), with scores of 48.90% and 47.93% respectively. These consistent gains demonstrate that the temporal logic and event-time mapping skills instilled by Stage 1 are crucial for achieving superior predictive accuracy and generative plausibility, validating our progressive learning approach.

Notably, Time-R1-S2-Direct (θ ′ 2 , 3B) still demonstrated commendable performance, surpassing several baselines and even the larger DeepSeek-V3-671B in Stage 2. This underscores the inherent effectiveness of our Stage 2 RL fine-tuning for enhancing temporal reasoning. However, the superior performance of Time-R1 (θ2, 3B) across both tasks confirms that the initial foundational stage is key to unlocking the model's full potential, enabling a more comprehensive development of temporal intelligence from fundamental understanding to advanced prediction and generalization.

# <span id="page-12-0"></span>5 Discussion

This section delves into a detailed analysis of our proposed methodology, focusing on the impact of our reasoning process on response length, and the challenges standard LLMs face in advanced temporal tasks. Our findings provide empirical evidence supporting the benefits of specialized training regimes for comprehensive temporal intelligence in LLMs. Additional discussion on implementation settings (*e.g.*, KL loss coefficients), as well as more generated examples like those shown in Figure [1,](#page-1-0) is available in Appendices [D](#page-20-0) and [E.](#page-21-0)

## 1 Reasoning Process Matters, Not Just Response Length

Developing effective LLMs requires not only accuracy but also efficient and concise responses. Unnecessarily long outputs can signify a less refined reasoning process and increase computational overhead. Our investigation reveals that our dynamic reward mechanism (Section [3.3.3\)](#page-7-0) achieves both higher accuracy and greater conciseness.

A combined analysis of our models' performance and output length provides compelling evidence for this. As established in Section [4.5.1,](#page-11-0) our dynamic reward curriculum leads to superior task performance (Figure [3\)](#page-9-0). Simultaneously, Figure [5](#page-12-2) highlights the dramatic impact on average response length. The model trained with a fixed reward produces verbose outputs, averaging approximately 250 tokens. In stark contrast, the model trained with our dynamic reward mechanism generates significantly shorter responses, stabilizing at a much more efficient length of around 130 tokens.

This substantial reduction in length, achieved alongside superior task performance, strongly suggests that our curriculum fosters a more effi-

<span id="page-12-2"></span>![](_page_12_Figure_10.jpeg)
<!-- Image Description: The image displays a line graph comparing "Dynamic Reward" and "Fixed Reward" methods. The y-axis represents "Average Response Length," and the x-axis shows "Training Step." Two lines plot average response length over training steps, demonstrating the performance difference between the two reward methods. The graph likely illustrates the impact of reward type on response length during training within a machine learning context. -->

Figure 5: Impact of Dynamic Reward on Response Length. The average response length (in tokens) across all Stage 1 tasks during training. The model trained with our full dynamic reward mechanism ("Dynamic Reward") produces consistently and significantly more concise outputs compared to the ablation model trained with a static, fixed reward ("Fixed Reward").

cient and focused reasoning process. The model learns to achieve better outcomes without verbose outputs, implying a clearer, more direct approach to solving temporal tasks. Such conciseness is highly desirable, indicating a more refined understanding and leading to more interpretable and computationally efficient inferences.

### <span id="page-13-3"></span>5.2 Challenges for Standard LLMs in Advanced Temporal Tasks

Standard Large Language Models (LLMs), including state-of-the-art reasoning-focused variants, exhibit commendable performance on foundational temporal tasks within their knowledge cutoff (Stage 1, Table [1\)](#page-10-0). This is often attributable to their large scale and extensive pre-training, which can include significant mathematical and logical reasoning data. However, their capabilities are substantially challenged when faced with more advanced temporal tasks requiring extrapolation and nuanced future-oriented generalization.

Specifically, in Stage 2 Future Event Time Prediction (Table [2,](#page-11-1) Figure [4\)](#page-10-1) and Stage 3 Creative Scenario Generation (Table [3\)](#page-11-2), even powerful baselines like DeepSeek-R1-671B are outperformed by our significantly smaller Time-R1 (θ2, 3B). For instance, Time-R1 (θ2, 3B) achieved a leading score of 0.7780 in Stage 2 prediction (vs. DeepSeek-R1's 0.7503) and 48.90% in Stage 3 generation (vs. DeepSeek-V3's 48.81%). This disparity suggests that vast knowledge, large scale, or general reasoning prowess alone do not readily translate to proficiency in predicting future event timings or creatively generating plausible future scenarios. The relatively uniform and modest performance of baselines in Stage 3, in particular, highlights a general weakness in current LLM training methodologies to effectively generalize to future-oriented generation tasks.

In contrast, the success of our three-stage RL framework with Time-R1 (θ2, 3B) is notable. It not only excels in prediction but also demonstrates remarkable generalization to creative future scenario generation without any explicit fine-tuning on this generative task itself. This underscores the efficacy and robustness of our method in instilling a deeper, more transferable temporal understanding. These findings highlight the necessity for specialized training regimes like ours to cultivate comprehensive and practically useful temporal intelligence in LLMs.

# 6 Conclusion

In this work, we introduced Time-R1, a 3B-parameter language model achieving comprehensive temporal reasoning—spanning understanding, prediction, and creative generation—through a novel, meticulously engineered three-stage reinforcement learning curriculum with a dynamic reward system. Strikingly, Time-R1 outperforms models over 200 times its size on challenging future event prediction and creative scenario generation tasks, exhibiting robust generalization to the latter even without task-specific fine-tuning. This success directly addresses a critical research gap concerning complex future-oriented tasks and demonstrates that our sophisticated, progressive RL approach enables smaller, efficient models to achieve superior temporal performance, offering a practical, scalable path towards truly time-aware AI with substantial application potential. To foster further research and development, we release our Time-Bench dataset and Time-R1 model checkpoints, envisioning future work on scalability and enhanced reasoning integration.

# References

- <span id="page-13-0"></span>[1] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. *Advances in neural information processing systems*, 30, 2017.
- [2] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. *Advances in neural information processing systems*, 33:1877–1901, 2020.
- <span id="page-13-1"></span>[3] Komal Kumar, Tajamul Ashraf, Omkar Thawakar, Rao Muhammad Anwer, Hisham Cholakkal, Mubarak Shah, Ming-Hsuan Yang, Phillip HS Torr, Fahad Shahbaz Khan, and Salman Khan. Llm post-training: A deep dive into reasoning large language models. *arXiv preprint arXiv:2502.21321*, 2025.
- <span id="page-13-2"></span>[4] Zheng Chu, Jingchang Chen, Qianglong Chen, Weijiang Yu, Haotian Wang, Ming Liu, and Bing Qin. Timebench: A comprehensive evaluation of temporal reasoning abilities in large language models. *arXiv preprint arXiv:2311.17667*, 2023.

- <span id="page-14-0"></span>[5] Chenhan Yuan, Qianqian Xie, Jimin Huang, and Sophia Ananiadou. Back to the future: Towards explainable temporal reasoning with large language models. In *Proceedings of the ACM Web Conference 2024*, pages 1963–1974, 2024.
- <span id="page-14-1"></span>[6] Ashutosh Bajpai, Aaryan Goyal, Atif Anwer, and Tanmoy Chakraborty. Temporally consistent factuality probing for large language models. *arXiv preprint arXiv:2409.14065*, 2024.
- [7] Ben Zhou, Kyle Richardson, Qiang Ning, Tushar Khot, Ashish Sabharwal, and Dan Roth. Temporal reasoning on implicit events from distant supervision. *arXiv preprint arXiv:2010.12753*, 2020.
- <span id="page-14-2"></span>[8] Jingtao Ding, Yunke Zhang, Yu Shang, Yuheng Zhang, Zefang Zong, Jie Feng, Yuan Yuan, Hongyuan Su, Nian Li, Nicholas Sukiennik, et al. Understanding world or predicting future? a comprehensive survey of world models. *arXiv preprint arXiv:2411.14499*, 2024.
- <span id="page-14-3"></span>[9] Jongho Kim and Seung-won Hwang. Counterfactual-consistency prompting for relative temporal understanding in large language models. *arXiv preprint arXiv:2502.11425*, 2025.
- <span id="page-14-4"></span>[10] Xin Wu, Yuqi Bu, Yi Cai, and Tao Wang. Updating large language models' memories with time constraints. In *Findings of the Association for Computational Linguistics: EMNLP 2024*, pages 13693–13702, 2024.
- <span id="page-14-5"></span>[11] Kai Nylund, Suchin Gururangan, and Noah A Smith. Time is encoded in the weights of finetuned language models. *arXiv preprint arXiv:2312.13401*, 2023.
- <span id="page-14-6"></span>[12] Jack W Rae, Sebastian Borgeaud, Trevor Cai, Katie Millican, Jordan Hoffmann, Francis Song, John Aslanides, Sarah Henderson, Roman Ring, Susannah Young, et al. Scaling language models: Methods, analysis & insights from training gopher. *arXiv preprint arXiv:2112.11446*, 2021.
- <span id="page-14-7"></span>[13] Bowen Zhao, Zander Brumbaugh, Yizhong Wang, Hannaneh Hajishirzi, and Noah A Smith. Set the clock: Temporal alignment of pretrained language models. *arXiv preprint arXiv:2402.16797*, 2024.
- <span id="page-14-8"></span>[14] Zhaochen Su, Jun Zhang, Tong Zhu, Xiaoye Qu, Juntao Li, Min Zhang, and Yu Cheng. Timo: Towards better temporal reasoning for language models. *arXiv preprint arXiv:2406.14192*, 2024.
- <span id="page-14-9"></span>[15] Siheng Xiong, Ali Payani, Ramana Kompella, and Faramarz Fekri. Large language models can learn temporal reasoning. *arXiv preprint arXiv:2401.06853*, 2024.
- <span id="page-14-10"></span>[16] Aaron Jaech, Adam Kalai, Adam Lerer, Adam Richardson, Ahmed El-Kishky, Aiden Low, Alec Helyar, Aleksander Madry, Alex Beutel, Alex Carney, et al. Openai o1 system card. *arXiv preprint arXiv:2412.16720*, 2024.
- <span id="page-14-11"></span>[17] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. *arXiv preprint arXiv:2501.12948*, 2025.
- <span id="page-14-12"></span>[18] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. *arXiv preprint arXiv:1707.06347*, 2017.
- <span id="page-14-13"></span>[19] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Y Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. *arXiv preprint arXiv:2402.03300*, 2024.
- <span id="page-14-14"></span>[20] Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang, Guanting Chen, Xiao Bi, Yu Wu, YK Li, et al. Deepseek-coder: When the large language model meets programming–the rise of code intelligence. *arXiv preprint arXiv:2401.14196*, 2024.
- <span id="page-14-15"></span>[21] Aniket Deroy and Subhankar Maity. A short case study on understanding the capabilities of gpt for temporal reasoning tasks. *Authorea Preprints*, 2024.

- <span id="page-15-0"></span>[22] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions with human feedback. *Advances in neural information processing systems*, 35:27730–27744, 2022.
- <span id="page-15-1"></span>[23] Timo Kaufmann, Paul Weng, Viktor Bengs, and Eyke Hüllermeier. A survey of reinforcement learning from human feedback. *arXiv preprint arXiv:2312.14925*, 10, 2023.
- <span id="page-15-2"></span>[24] Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea Finn. Direct preference optimization: Your language model is secretly a reward model. *Advances in Neural Information Processing Systems*, 36:53728–53741, 2023.
- <span id="page-15-3"></span>[25] Yu Meng, Mengzhou Xia, and Danqi Chen. Simpo: Simple preference optimization with a reference-free reward. *Advances in Neural Information Processing Systems*, 37:124198–124235, 2024.
- <span id="page-15-4"></span>[26] Arash Ahmadian, Chris Cremer, Matthias Gallé, Marzieh Fadaee, Julia Kreutzer, Olivier Pietquin, Ahmet Üstün, and Sara Hooker. Back to basics: Revisiting reinforce style optimization for learning from human feedback in llms. *arXiv preprint arXiv:2402.14740*, 2024.
- <span id="page-15-5"></span>[27] Ronald J Williams. Simple statistical gradient-following algorithms for connectionist reinforcement learning. *Machine learning*, 8:229–256, 1992.
- <span id="page-15-6"></span>[28] Tian Xie, Zitian Gao, Qingnan Ren, Haoming Luo, Yuqian Hong, Bryan Dai, Joey Zhou, Kai Qiu, Zhirong Wu, and Chong Luo. Logic-rl: Unleashing llm reasoning with rule-based reinforcement learning. *arXiv preprint arXiv:2502.14768*, 2025.
- <span id="page-15-7"></span>[29] Bowen Jin, Hansi Zeng, Zhenrui Yue, Dong Wang, Hamed Zamani, and Jiawei Han. Search-r1: Training llms to reason and leverage search engines with reinforcement learning. *arXiv preprint arXiv:2503.09516*, 2025.
- <span id="page-15-8"></span>[30] Huatong Song, Jinhao Jiang, Yingqian Min, Jie Chen, Zhipeng Chen, Wayne Xin Zhao, Lei Fang, and Ji-Rong Wen. R1-searcher: Incentivizing the search capability in llms via reinforcement learning. *arXiv preprint arXiv:2503.05592*, 2025.
- <span id="page-15-9"></span>[31] Xuefeng Li, Haoyang Zou, and Pengfei Liu. Torl: Scaling tool-integrated rl. *arXiv preprint arXiv:2503.23383*, 2025.
- <span id="page-15-10"></span>[32] Cheng Qian, Emre Can Acikgoz, Qi He, Hongru Wang, Xiusi Chen, Dilek Hakkani-Tür, Gokhan Tur, and Heng Ji. Toolrl: Reward is all tool learning needs. *arXiv preprint arXiv:2504.13958*, 2025.
- [33] Hongru Wang, Cheng Qian, Wanjun Zhong, Xiusi Chen, Jiahao Qiu, Shijue Huang, Bowen Jin, Mengdi Wang, Kam-Fai Wong, and Heng Ji. Otc: Optimal tool calls via reinforcement learning. *arXiv preprint arXiv:2504.14870*, 2025.
- <span id="page-15-11"></span>[34] Xiusi Chen, Gaotang Li, Ziqi Wang, Bowen Jin, Cheng Qian, Yu Wang, Hongru Wang, Yu Zhang, Denghui Zhang, Tong Zhang, et al. Rm-r1: Reward modeling as reasoning. *arXiv preprint arXiv:2505.02387*, 2025.
- <span id="page-15-12"></span>[35] Richard S Sutton, Andrew G Barto, et al. *Reinforcement learning: An introduction*, volume 1. MIT press Cambridge, 1998.
- <span id="page-15-13"></span>[36] The New York Times. Archive api. [https://developer.nytimes.com/docs/](https://developer.nytimes.com/docs/archive-product/1/overview) [archive-product/1/overview](https://developer.nytimes.com/docs/archive-product/1/overview). Accessed on March 6, 2024.
- <span id="page-15-14"></span>[37] James Pustejovsky, José M Castano, Robert Ingria, Roser Sauri, Robert J Gaizauskas, Andrea Setzer, Graham Katz, and Dragomir R Radev. Timeml: Robust specification of event and temporal expressions in text. *New directions in question answering*, 3:28–34, 2003.
- <span id="page-15-15"></span>[38] Volker Gast, Lennart Bierkandt, Stephan Druskat, and Christoph Rzymski. Enriching timebank: Towards a more precise annotation of temporal relations in a text. In *Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC'16)*, pages 3844–3850, 2016.

- <span id="page-16-0"></span>[39] Dong-Ho Lee, Kian Ahrabian, Woojeong Jin, Fred Morstatter, and Jay Pujara. Temporal knowledge graph forecasting without knowledge using in-context learning. *arXiv preprint arXiv:2305.10613*, 2023.
- <span id="page-16-1"></span>[40] Wenhui Wang, Furu Wei, Li Dong, Hangbo Bao, Nan Yang, and Ming Zhou. Minilm: Deep self-attention distillation for task-agnostic compression of pre-trained transformers. *Advances in neural information processing systems*, 33:5776–5788, 2020.
- <span id="page-16-2"></span>[41] Carlo Galli, Nikolaos Donos, and Elena Calciolari. Performance of 4 pre-trained sentence transformer models in the semantic query of a systematic review dataset on peri-implantitis. *Information*, 15(2):68, 2024.
- <span id="page-16-3"></span>[42] An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, et al. Qwen2. 5 technical report. *arXiv preprint arXiv:2412.15115*, 2024.
- <span id="page-16-4"></span>[43] Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. The llama 3 herd of models. *arXiv preprint arXiv:2407.21783*, 2024.
- <span id="page-16-5"></span>[44] Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al. Deepseek-v3 technical report. *arXiv preprint arXiv:2412.19437*, 2024.
- <span id="page-16-6"></span>[45] Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin Wu, Wang Zhang, Ru Zhang, Yanghua Peng, Haibin Lin, and Chuan Wu. Hybridflow: A flexible and efficient rlhf framework. *arXiv preprint arXiv:2409.19256*, 2024.
- [46] Janice Ahn, Rishu Verma, Renze Lou, Di Liu, Rui Zhang, and Wenpeng Yin. Large language models for mathematical reasoning: Progresses and challenges. *arXiv preprint arXiv:2402.00157*, 2024.
- [47] Zheng Yuan, Hongyi Yuan, Chuanqi Tan, Wei Wang, and Songfang Huang. How well do large language models perform in arithmetic tasks? *arXiv preprint arXiv:2304.02015*, 2023.

# Appendix

# <span id="page-17-0"></span>A Experimental Configuration Details

This appendix provides further details on the experimental setup and hyperparameter configurations used for the Reinforcement Learning (RL) fine-tuning of Time-R1, complementing the summary in Section [4.3](#page-9-1) of the main paper. Our experiments were conducted using the veRL framework [\[45\]](#page-16-6).

## A.1 General Setup and Key Hyperparameters

<span id="page-17-1"></span>The base Large Language Model (LLM) for all our experiments is Qwen2.5-3B-Instruct. The RL fine-tuning was performed using 4 NVIDIA A6000 GPUs. Key hyperparameters for the Group Relative Policy Optimization (GRPO) algorithm and the overall training process are summarized in Table [4.](#page-17-1)

| Parameter                          | Value               |
|------------------------------------|---------------------|
| General & Model<br>Base Model Name | Qwen2.5-3B-Instruct |
| Number of GPUs<br>Data & Batching  | 4                   |
| train batch size (Global)          | 128                 |
| GRPO mini batch size               | 64                  |
| GRPO micro batch size              | 16                  |
| max prompt length                  | 1024 tokens         |
| max response length                | 1024 tokens         |
| Optimizer (Actor Model)            |                     |
| learning rate                      | 2 × 10−6            |
| warmup style                       | cosine              |
| warmup steps                       | 20                  |
| GRPO Algorithm & Rollout           |                     |
| kl loss coef (β)                   | 0.001               |
| rollout.n (K)                      | 5                   |

Table 4: Key hyperparameters for RL fine-tuning Time-R1.

### A.2 Stage-Specific Training Configurations

The multi-stage training of Time-R1 involved specific durations and checkpointing strategies for each stage, as outlined below. For both stages, checkpoints were selected based on the highest achieved score on the respective test set.

Stage 1 (Comprehension): This stage implemented our dynamic reward curriculum (detailed in Section [3.3.3\)](#page-7-0) and was divided into three phases:

- Phase 1 (Foundational Logic; Easy Timestamp Inference): Trained for 100 steps.
- Phase 2 (Exploration; Full Task Suite, Mixed Difficulty): Trained for 500 steps.
- Phase 3 (Transition to Strict Evaluation; Full Task Suite): Trained for 1000 steps.

Throughout Stage 1, evaluations on the test set were performed every 10 training steps, and model checkpoints were saved every 20 training steps. The best-performing checkpoint on the test set from each phase was used to initialize the subsequent phase or, for Phase 3, served as the final Stage 1 model (θ1).

Stage 2 (Prediction): This stage focused on future event time prediction:

• Trained for 100 steps.

During Stage 2, both model checkpointing and test set evaluations occurred every 10 training steps. The checkpoint yielding the highest test score was selected as the final Stage 2 model (θ2).

These tailored configurations allowed for progressive and adaptive learning, ensuring that Time-R1 developed foundational understanding before advancing to more complex predictive tasks.

# B Dataset Construction and Details

This appendix provides further details on the datasets used for training and evaluating Time-R1, supplementing the descriptions in Sections [3.2.1](#page-4-1) and [3.2.2.](#page-4-2)

## <span id="page-18-0"></span>B.1 New York Times (NYT) Corpus Curation

The primary data source for our research is a corpus constructed from New York Times articles, utilizing publicly available information accessed via the NYT Archive API[2](#page-18-2) . For each article, we extracted key fields including the headline, abstract, publication date, and the "news desk" (thematic section).

We collected over 200,000 English-language NYT articles, with publication dates spanning from January 2016 to February 2025. To ensure the relevance of the articles to common temporal reasoning scenarios and current events, we selectively curated content from the following news desks: "Politics", "National", "Washington", "U.S.", "Business", "SundayBusiness", "RealEstate", "Foreign", "World", "Metro", "Science", "Health", "Climate", "Opinion", and "OpEd". Other news desks were excluded as they were found to reference current events less frequently.

This extensive NYT corpus was utilized for several distinct purposes within our framework:

- Stage 1 (Comprehension) Training Data: Articles published from January 2016 to December 2023 were used to train the foundational temporal understanding capabilities of Time-R1 (see Section [3.2.1](#page-4-1) for Stage 1 details).
- Stage 2 (Prediction) Real News Training Data: A subset of articles from January 2024 to July 2024 served as real-world news data for the initial phase of Stage 2 training.
- Stage 2 (Prediction) Real News Test Data: Articles from August 2024 to February 2025 were held out and used as the real-news test set (D(2) test) for evaluating future event prediction performance.

In our task formulations, an event E is typically represented by its headline h and abstract a, i.e., E = (h, a).

### <span id="page-18-1"></span>B.2 Synthetic Data Generation for Future Event Prediction Training

To train Time-R1 for predicting events in future months (specifically, August 2024 to February 2025) without encountering data leakage from the real-news test period, we employed a data synthesis strategy as detailed in Section [3.2.2.](#page-4-2) This process utilized the DeepSeek-V3 model with a knowledge cutoff in July 2024.

The methodology for generating synthetic news articles was as follows:

• Targeted News Desk Distribution: The generation aimed to reflect a historical distribution of articles across various news desks, based on NYT data prior to 2024. The primary target desk distribution used to guide generation proportions was:

Foreign: 20.8%; Business: 16.5%; OpEd: 14.2%; National: 10.9%; Washington: 9.6%; Metro: 8.6%; Politics: 5.5%; Science: 4.6%.

• Few-Shot Prompting Strategy: To generate content for a specific target future month (between August 2024 and February 2025) and a designated news desk, the DeepSeek-V3 model was prompted using a few-shot learning approach. Each prompt contained three real news headlines and abstracts from the *same* news desk, randomly sampled from articles published between May 2024 and July 2024.

<span id="page-18-2"></span><sup>2</sup> <https://developer.nytimes.com/docs/archive-product/1/overview>

- Generation Task: For each such prompt, DeepSeek-V3 was instructed to generate six distinct synthetic news items (each comprising a headline and an abstract) relevant to the specified future month and news desk, learning from the style and content of the provided examples.
- Output Distribution: The selection and aggregation of these generated articles were managed so that the overall proportion of news items per desk for each future month in the synthetic training set (D(2) train) approximately mirrored the historical desk distribution detailed above.

This synthetic dataset provided the necessary training signals for the model to learn to predict events beyond its real-data cutoff while strictly ensuring no overlap with the real-news test data from the same period. The volume of this synthetic data for August 2024 - February 2025 was about half that of the real news data used for January 2024 - July 2024 in the Stage 2 training.

# <span id="page-19-0"></span>C Detailed Stage 1 Learning Curves and Analysis

This section provides a more detailed look at the learning dynamics during Stage 1 (Comprehension), complementing the summarized performance presented in Table [1](#page-10-0) of Section [4.4.1.](#page-9-2) We present the training curves for all four fundamental temporal subtasks—Timestamp Inference, Time-Difference Estimation, Event Ordering, and Masked Time Entity Completion—specifically focusing on their progression throughout Phase 2 and Phase 3 of our dynamic reward curriculum (see Section [3.3.3](#page-7-0) for details on the curriculum phases). Additionally, we illustrate the evolution of the inconsistency penalty factor (Pincon) for the Time-Difference Estimation and Event Ordering tasks during Phase 2, highlighting the model's improving adherence to logical and mathematical consistency.

<span id="page-19-1"></span>![](_page_19_Figure_5.jpeg)
<!-- Image Description: The image contains two line graphs showing total scores (R(x,y)) across training steps for different components of a model in two phases (Phase 2 and Phase 3). The left graph displays scores for "Overall," "Completion," "Difference," "Inferring," and "Ordering," while also showing inconsistency penalty factors. The right graph shows similar scores across more training steps, indicating a continued evaluation of model performance across phases. The graphs illustrate the evolution of individual components' contributions to the overall model score during training. -->

Figure 6: Learning curves for Stage 1 subtasks during (Left) Phase 2 and (Right) Phase 3 of the dynamic reward curriculum. The left plot also shows the Inconsistency Penalty Factor (Pincon) for Time-Difference Estimation and Event Ordering tasks on the right y-axis during Phase 2.

The learning curves depicted in Figure [6](#page-19-1) offer several key insights into the effectiveness of our methodology. Firstly, the steady increase and eventual convergence of the total scores (R(x, y))) across all subtasks in both Phase 2 and Phase 3 underscore the benefits of our dynamic reward design and curriculum learning strategy. This carefully structured approach enables the model to progressively master complex temporal logic, gradually adapting from more lenient to stricter evaluation criteria. As noted in Section [4.4.1,](#page-9-2) this robust Stage 1 performance allows our 3B Time-R1 model to surpass numerous baseline models, many of which are ten to over two hundred times larger in parameter count (Table [1\)](#page-10-0). Such strong foundational capabilities in temporal comprehension are crucial and deliberately engineered to provide a solid grounding for the subsequent, more demanding future-oriented tasks in Stage 2 (Prediction) and Stage 3 (Generation).

Secondly, the trends observed for the inconsistency penalty factors (Pincon) for the Time-Difference Estimation and Event Ordering tasks during Phase 2 (left plot of Figure [6,](#page-19-1) dashed lines) are particularly revealing. The increasing values of Pincon (approaching 1.0) indicate that the model is effectively learning to minimize inconsistencies in its responses. For instance, in Time-Difference Estimation, it learns to ensure that the explicitly stated time difference aligns with the difference calculated from its inferred dates for the two events. Similarly, for Event Ordering, the model becomes better at ensuring the stated order of events is consistent with the chronological sequence implied by its inferred dates for those events. This demonstrates that the penalty mechanisms detailed in Section [3.3.2](#page-6-2) successfully guide the model not just towards task-specific accuracy but also towards generating responses that are logically coherent and mathematically sound, a critical aspect of true temporal understanding. By the commencement of Phase 3, these consistency factors are generally high, allowing the training to focus further on refining accuracy under strict evaluation.

Overall, these detailed learning dynamics from Stage 1 highlight the efficacy of our curriculum in building both accurate and logically consistent temporal reasoning, providing the essential groundwork for Time-R1's advanced capabilities in navigating future temporal challenges.

# <span id="page-20-0"></span>D Further Discussion on Implementation Settings

This appendix elaborates on specific implementation settings, focusing on the impact of the KL loss coefficient on model response length and the overall stability of our training framework with respect to various hyperparameter changes. These details supplement the primary configurations presented in Table [4.](#page-17-1)

## D.1 Impact of KL Loss Coefficient on Response Length

The Group Relative Policy Optimization (GRPO) objective function, as defined in Equation [\(3\)](#page-3-1), incorporates a KL divergence term DKL[πθ(·|x)||πref (·|x)] scaled by a coefficient β. This term penalizes deviations of the current policy π<sup>θ</sup> from a reference policy πref , encouraging smoother and more stable policy updates. The magnitude of β directly influences the strength of this regularization.

<span id="page-20-1"></span>![](_page_20_Figure_6.jpeg)
<!-- Image Description: The image is a line graph showing the impact of the KL coefficient on average response length during training. Two lines represent different KL coefficient values (0.001 and 0.0001). The x-axis represents the training step, and the y-axis shows the average response length. The graph illustrates how the average response length changes over training steps for each KL coefficient value. It aims to demonstrate the effect of KL coefficient on response length in the context of the paper's methodology. -->

Figure 7: Impact of different KL loss coefficients (β) on the average response length during training. A lower coefficient (0.0001) leads to longer average responses compared to the default setting (0.001).

As illustrated in Figure [7,](#page-20-1) a lower KL coefficient (e.g., β = 0.0001 compared to our default β = 0.001) reduces the penalty for deviating from the reference policy. This allows the model greater freedom to explore diverse generation strategies during training. A noticeable consequence of this increased exploration with a lower β is an increase in the average length of the generated responses. However, our experiments indicated that while the response lengths varied, the overall performance scores on the test sets remained largely comparable across these KL coefficient settings. This suggests that while the KL coefficient can influence stylistic aspects of the generation, such as verbosity, the core temporal reasoning capabilities learned by the model are robust within this range of β values.

### D.2 Framework Stability under Hyperparameter Variations

Beyond the KL coefficient, we investigated the sensitivity of Time-R1's performance to variations in other key hyperparameters relative to our main configuration detailed in Table [4.](#page-17-1) These variations included:

- Increasing the number of rollout responses (K) from 5 to 8 and 11.
- Adjusting the sampling temperature from 1.0 to 1.2.
- Modifying the learning rate from 2 × 10−<sup>6</sup> to 5 × 10−<sup>6</sup> (increase) and 1 × 10−<sup>6</sup> (decrease).
- Increasing the GRPO micro batch size from 16 to 32.
- Varying the GRPO mini batch size from 64 to 128 (increase) and 32 (decrease).

Across these diverse hyperparameter modifications, we observed that the performance of Time-R1 on our test sets remained largely consistent, with no significant degradation in scores. This robustness to moderate changes in key training parameters underscores the overall stability and reliability of our proposed three-stage RL framework and GRPO optimization setup. Such stability is advantageous, suggesting that the framework is not overly sensitive to precise hyperparameter tuning, which can be beneficial for practical application and further development.

# <span id="page-21-0"></span>E Additional Generated Examples of Time-R1

This appendix presents additional generated examples from our Time-R1 model, supplementing Figure [1](#page-1-0) and further illustrating its capabilities across Stage 1 (Comprehension), Stage 2 (Prediction), and Stage 3 (Generation). These examples showcase the model's structured reasoning process (within <think>...</think> tags) and its final outputs (within <answer>...</answer> tags), alongside ground truth information and achieved scores. The detailed prompts used to elicit these responses are available in Appendix [I.](#page-25-0) Our analysis highlights how Time-R1 demonstrates comprehensive temporal reasoning by effectively understanding context, making logical inferences, and generating plausible future-oriented content.

## E.1 Example: Stage 1 - Timestamp Inference

This example demonstrates Time-R1's ability to infer the publication date of a news article by reasoning about the real-world events mentioned.

Analysis In this instance, Time-R1 correctly associates the discussion about child care systems with the coronavirus pandemic. It leverages its knowledge that the outbreak began in early 2020 and reasons that related articles discussing systemic responses would likely appear in the subsequent months. The inferred date 2020-04 is very close to the ground truth 2020-05, showcasing accurate temporal localization based on contextual understanding of significant world events. The high score reflects this accuracy and proper formatting.

### E.2 Example: Stage 1 - Masked Time Entity Completion

This example illustrates the model's capability to not only infer an event's primary date but also to fill in a masked temporal entity within the text, requiring a deeper semantic understanding.

Analysis Time-R1 successfully identifies the masked year as 2016 by connecting the context of "Hillary Clinton's presidential campaign" to the correct election cycle. Simultaneously, it infers the main event's date (the article's publication discussing these past activities) as 2018-06, which is very close to the ground truth 2018-07. This demonstrates its ability to distinguish between the time of the events discussed within the text (the 2016 campaign) and the time of the news reporting itself, showcasing a nuanced understanding of temporal references and context.

### E.3 Example: Stage 2 - Future Event Time Prediction

This example showcases Time-R1's ability to predict the timing of future events by extrapolating from patterns and general knowledge.

| Aspect                                       | Details                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |  |  |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|--|
| Task<br>Input Headline<br>Input Abstract     | Stage 1: Timestamp Inference<br>How to Build a Better Child Care System<br>The coronavirus has highlighted how necessary good child care<br>is.                                                                                                                                                                                                                                                                                                                                                                                                                                              |  |  |
| Model Reasoning<br><think></think>           | The article discusses how the coronavirus has<br>highlighted the necessity of a better child care<br>system.<br>Given that the coronavirus outbreak<br>began in January 2020 and has had a significant<br>impact on child care systems around the world,<br>it is reasonable to infer that the article is<br>describing efforts to improve the child care<br>system in response to the coronavirus pandemic.<br>The article likely covers the events happening<br>during the spring of 2020, when many countries<br>were implementing policies to support child care<br>during the pandemic. |  |  |
| Model Answer<br><answer></answer>            | 2020-04                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |  |  |
| Ground Truth (Event Pub Date)<br>Total Score | 2020-05<br>1.005                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |  |  |

Table 5: Example of Timestamp Inference by Time-R1 θ1.

| Aspect                                   | Details                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |  |
|------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|
| Task<br>Input Headline<br>Input Abstract | Stage 1: Masked Time Entity Completion<br>How Russian Spies Hid Behind Bitcoin in Hacking Campaign<br>Operatives used cryptocurrency to obscure their identities and pay for<br>the infrastructure needed to steal emails from Hillary Clinton's <year><br/>presidential campaign.</year>                                                                                                                                                                                                                          |  |
| Model Reasoning<br><think></think>       | The article is about the hacking campaign that took<br>place during the 2016 presidential election.<br>Given<br>that the hacking campaign involved stealing emails<br>from the Hillary Clinton presidential campaign, it<br>is reasonable to infer that the hacking campaign took<br>place during the 2016 election year.<br>The hacking<br>campaign would have needed time to happen in order to<br>steal the emails, and the use of cryptocurrency would<br>have also needed time to develop and be implemented. |  |
| Model Answer<br><answer></answer>        | Event:<br>2018-06.<br>Missing entity:<br>2016.                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |  |
| Ground Truth<br>Total Score              | Event Pub Date: 2018-07, Masked Entity: 2016<br>1.052                                                                                                                                                                                                                                                                                                                                                                                                                                                              |  |

| Aspect                                       | Details                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|----------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Task<br>Input Headline                       | Stage 2: Future Event Time Prediction<br>The Olympics, a Triumph of Ambition, Lift France From Its<br>Gloom                                                                                                                                                                                                                                                                                                                                                   |
| Input Abstract                               | All sectors of society came together to achieve the nation's dream<br>for the Games. Success has shown that unity is possible, if often<br>elusive.                                                                                                                                                                                                                                                                                                           |
| Model Reasoning<br><think></think>           | The Olympics are known to happen every four<br>years, and the most recent Olympics were held in<br>2020.<br>Given that the Olympics typically take at<br>least two years to prepare for and the COVID-19<br>pandemic would have taken at least two years<br>to resolve, it is reasonable to infer that the<br>Olympics would happen relatively quickly after<br>the end of the 2020 Olympics, which were delayed<br>by one year due to the COVID-19 pandemic. |
| Model Answer<br><answer></answer>            | 2024-08                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Ground Truth (Event Pub Date)<br>Total Score | 2024-08<br>1.100                                                                                                                                                                                                                                                                                                                                                                                                                                              |

Table 7: Example of Future Event Time Prediction by Time-R1 θ2.

Analysis In this challenging future prediction task, Time-R1 correctly predicts the 2024-08 date for the Paris Olympics. Its reasoning demonstrates an understanding of typical event cycles ("every four years"), knowledge of recent past events (2020 Olympics and their delay), and the ability to synthesize this information to make an accurate future projection. This highlights its capacity for temporal extrapolation, a key component of comprehensive temporal intelligence. The perfect score reflects this accurate prediction.

### E.4 Example: Stage 3 - Creative Future Scenario Generation

This example illustrates Time-R1's capability for creative scenario generation, where it generates a plausible future news item for a given future date (January 2025 in this case), without explicit fine-tuning on this generative task. The quality is assessed by semantic similarity to actual news from that period.

Analysis For the future date of January 2025, Time-R1 generated a plausible news scenario about AI's impact on tech stocks. This generated content is thematically coherent and discusses a relevant potential development in the technology and market sectors. When compared to a real news headline from a similar period that also discusses AI and tech investors, it achieves a notable semantic similarity score (0.6731). This demonstrates Time-R1's ability to not just predict dates, but to creatively generate contextually relevant and plausible future narratives, showcasing a strong generalization of its learned temporal understanding and reasoning skills. This ability to generate novel, coherent future content is a hallmark of advanced temporal intelligence.

# <span id="page-23-0"></span>F Illustration of Length and Repetition Penalty Efficacy

In Section [3.3.1](#page-6-3) (Common Bonuses and Penalties), we introduced the Length and Repetition Penalty (Plen\_rep), designed to discourage overly verbose or repetitive model outputs. We noted that this mechanism has proven particularly effective. This section provides an illustrative example of the type of repetitive reasoning that the Prepetition component of this penalty targets, thereby guiding the model towards more efficient and varied responses.

| Aspect                    | Details                                                                                                                                                                                                                                                                             |
|---------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Task                      | Stage 3: Creative Future Scenario Generation                                                                                                                                                                                                                                        |
| Target                    | News for January 2025 (Technology/Market theme implied by output)                                                                                                                                                                                                                   |
| Time-R1 Generated News    |                                                                                                                                                                                                                                                                                     |
| Headline:                 | Global Tech Stocks Face Pressure as AI Innovations Begin to Shape the<br>Market                                                                                                                                                                                                     |
| Abstract:                 | The introduction of new artificial intelligence (AI) technologies is<br>putting pressure on the tech stock market. Analysts predict that com<br>panies that can effectively integrate AI into their operations will see<br>significant gains, while others may struggle to keep up. |
| Comparable Real News      |                                                                                                                                                                                                                                                                                     |
| Headline:                 | China's A.I. Advances Spook Big Tech Investors on Wall Street                                                                                                                                                                                                                       |
| Abstract:                 | Stiffer competition for the tech giants at the forefront of the artificial<br>intelligence boom prompted investors to reassess the companies' sky<br>high valuations.                                                                                                               |
| Semantic Similarity Score | 0.6731                                                                                                                                                                                                                                                                              |

Table 8: Example of Creative Future Scenario Generation by Time-R1 θ<sup>2</sup> (Target: January 2025).

|  | Table 9: Example Illustrating Repetitive Reasoning Targeted by the Prepetition |  |  | Penalty. |
|--|--------------------------------------------------------------------------------|--|--|----------|
|--|--------------------------------------------------------------------------------|--|--|----------|

<span id="page-24-0"></span>

| Aspect                             | Details                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Task<br>Input Headline             | Time Prediction (Stage 2 Example)<br>After Thursday's Debate, Conservative Media Finds It Hard Not<br>to Gloat                                                                                                                                                                                                                                                                                                                                                                                   |
| Input Abstract                     | Many conservative commentators have said President Biden's<br>performance during the debate was a sweeping validation of the<br>alarm bells they'd been ringing for years about his age.                                                                                                                                                                                                                                                                                                         |
| Model Reasoning<br><think></think> | The article is about the debate between President<br>Biden and other candidates in the Republican<br>primary election.<br>Given that elections usually<br>take several weeks to several months to be<br>resolved, it is reasonable to infer that the<br>article is about describing preparations for<br>the debate.<br>Given that elections usually take<br>several weeks to several months to be resolved,<br>it is likely that the article is about describing<br>preparations for the debate. |
| Model Answer<br><answer></answer>  | 2024-06                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Ground Truth (Event Pub Date)      | 2024-07                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

Analysis and Impact of Penalties The model's reasoning process shown in Table [9](#page-24-0) exhibits a clear instance of repetition: the core phrase "Given that elections usually take several weeks to several months to be resolved, it is reasonable/likely to infer that the article is about describing preparations for the debate" appears twice with only minor variation. This form of redundancy would be directly addressed by the Pphrase\_repeat component within our Prepetition penalty (as defined in Section [3.3.1\)](#page-6-3).

By applying such penalties, the Plen\_rep mechanism actively discourages the model from generating verbose or repetitive content. This not only improves the conciseness of the output but also pushes the model to explore more diverse and efficient reasoning pathways. The consistent application of these universal bonuses and penalties, including those for length and various forms of repetition (word, phrase, n-gram diversity), is therefore instrumental in achieving the well-formed, succinct, and accurate responses demonstrated in the examples throughout Appendix [E.](#page-21-0) It ensures that Time-R1's advanced temporal reasoning is communicated clearly and effectively, without being undermined by a tendency towards unnecessary verbosity or redundancy.

# G Limitations

Firstly, while our work introduces Time-Bench, a large-scale, open-source dataset designed to facilitate comprehensive temporal reasoning research, a potential limitation lies in the scope of evaluation. Spanning a decade of news data and comprising over 200,000 examples across multiple temporal tasks, Time-Bench provides a robust benchmark for evaluating the capabilities demonstrated by Time-R1. However, validating the effectiveness and generalization capabilities of our model on a wider array of external temporal reasoning benchmarks and diverse datasets would further strengthen our findings and provide stronger evidence for the robustness of our proposed training framework.

Secondly, while our results demonstrate that smaller models can achieve strong performance on temporal tasks with specialized RL training, evidence from baseline comparisons also suggests that larger models generally exhibit higher capabilities. Due to resource constraints, we focused on demonstrating the efficacy of our approach on a 3B model to highlight cost-effective and rapid iteration potential. However, applying our three-stage RL framework to larger foundation models could likely yield even more significant performance gains, leveraging their inherently greater knowledge capacity. Our work primarily showcases the potential of the RL methodology, which we believe would scale positively with model size.

# H Ethical Statement

The development of Time-R1 and the Time-Bench dataset aims to advance research in temporal reasoning for AI. The dataset constructed from New York Times articles uses publicly available information through Archive api. While endowing models with future prediction and scenario generation capabilities has many beneficial applications, such as in planning and risk assessment, we acknowledge the potential for misuse, such as generating misleading future-oriented content. To address this, we believe that fostering an environment of transparency and critical use is paramount; users should be aware when content is AI-generated, particularly for probabilistic future scenarios, allowing for informed interpretation rather than uncritical acceptance. This approach, emphasizing clear attribution and critical engagement, combined with ongoing research into robust safeguards, is crucial for responsibly harnessing such powerful capabilities. Our model development did not involve human-derived private data beyond publicly archived news. The research was conducted with the intention of fostering a better understanding of AI's temporal intelligence, and we encourage responsible use and further investigation into safeguards for generative temporal models. The datasets and models will be released to the research community to promote transparency and further beneficial advancements in this domain.

# <span id="page-25-0"></span>I Prompts

This appendix provides the detailed structure and content of the prompts used to guide our Large Language Model for each of the six temporal reasoning tasks evaluated in this work. Consistent with the methodology described in Section [3.1](#page-2-0) (Structured Generation Process), all prompts employ a specific template designed to elicit chain-of-thought reasoning. This template includes system

instructions directing the model to first articulate its reasoning process within '<think>...</think>' tags, followed by the final answer encapsulated in '<answer>...</answer>' tags. This structured approach aims to enhance the robustness of the model's reasoning and the interpretability of its outputs. The specific prompts for each task are detailed in the following subsections.

## I.1 Prompt for Timestamp Inference

The Timestamp Inference task is one of the four fundamental temporal tasks in Stage 1 (Comprehension). It requires the model to infer the specific month and year (formatted as YYYY-MM) of an event based on its provided news headline and abstract. The detailed prompt given to the model for this task, including system messages, user input structure with placeholders for event details, and specific output formatting requirements, is shown in Figure [8.](#page-26-0)

<span id="page-26-0"></span>

| Prompt for Timestamp Inference Task                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| "< im_start >system\n"<br>"You are a helpful assistant. You first think about the reasoning process in your mind and then provide<br>the user with the answer.\n"<br>"< im_end >\n"<br>"< im_start >user\n"<br>f"Please carefully read the following news article information:\n"<br>f"Headline: {event['headline']}\n"<br>f"Abstract: {event['abstract']}\n"<br>"For the purpose of this inference, assume that the event described in the article definitely occurs. "<br>"Based on the information provided and your general knowledge, determine the specific occurrence<br>date of the event.\n"<br>"- You can recall the events related to this article and their occurrence dates to help you infer.\n"<br>"- Output the event's occurrence date in the format 'YYYY-MM'.\n"<br>"- Do not output 'No event' under any circumstances. Always provide your best inferred date, even if the<br>information is ambiguous.\n"<br>"- Show your reasoning process in <think> </think> tags, and return the final answer on a new line in<br><answer> </answer> tags, for example <answer>2023-12</answer> .\n"<br>"Your answer must strictly follow the above format.\n"<br>"< im_end >\n"<br>"< im_start >assistant\n"<br>"Let me carefully review all the relevant details and systematically work through the reasoning<br>process.\n" |
| " <think>"</think>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

Figure 8: Prompt for the Timestamp Inference task.

### I.2 Prompt for Time-Difference Estimation

The Time-Difference Estimation task is part of Stage 1 (Comprehension). It requires the model to first infer the specific dates of two separate events (E<sup>1</sup> and E2) described by their news headlines and abstracts, and then to estimate the temporal gap (*i.e.*, in months) between these two events. The detailed prompt guiding the model through this multi-step reasoning process is shown in Figure [9.](#page-27-0)

### I.3 Prompt for Event Ordering

The Event Ordering task, also a component of Stage 1 (Comprehension), challenges the model to determine the correct chronological sequence of three distinct events (E1, E2, E3) presented out of order. Similar to other Stage 1 tasks, the model is prompted to first infer the date of each event before determining their order. The prompt structure for this task is presented in Figure [10.](#page-28-0)

#### <span id="page-27-0"></span>Prompt for Time-Difference Estimation Task

"<|im\_start|>system\n" "You are a helpful assistant. You first think about the reasoning process in your mind and then provide the user with the answer.\n" "<|im\_end|>\n" "<|im\_start|>user\n" "Please carefully read the following two news article information:\n" "News article 1:\n" f"Headline: {event1['headline']}\n" f"Abstract: {event1['abstract']}\n" "News article 2:\n" f"Headline: {event2['headline']}\n" f"Abstract: {event2['abstract']}\n" "For the purpose of this inference, assume that the two events described in the articles definitely occur. " "Based on the information provided and your general knowledge, determine the specific occurrence date for each event and then calculate the month difference between these two dates.\n" "- You can recall the events related to these two and their occurrence dates to help you infer.\n" "- Provide your answer in the following format:\n" " 'Event 1: YYYY-MM, Event 2: YYYY-MM. Month difference: XX.'\n" "- Do not output 'No event' under any circumstances. Always provide your best inferred dates, even if the information is ambiguous.\n" "- Show your reasoning process in <think> </think> tags, and return the final answer on a new line in <answer> </answer> tags, for example <answer>Event 1: 2023-01, Event 2: 2021-11. Month difference: 14.</answer>.\n" "Your answer must strictly follow the above format.\n" "<|im\_end|>\n" "<|im\_start|>assistant\n" "Let me carefully review all the relevant details and systematically work through the reasoning process.\n" "<think>"

Figure 9: Prompt for the Time-Difference Estimation task.

### I.4 Prompt for Masked Time Entity Completion

The Masked Time Entity Completion task is the fourth fundamental task in Stage 1 (Comprehension). In this task, the model is given an event description (E′ ) containing a masked temporal expression (such as '<Year>' or '<Month>') and is required to fill in the correct missing time entity, after first inferring the event's overall date. The specific prompt used to guide this completion process is shown in Figure [11.](#page-29-0)

### I.5 Prompt for Future Event Time Prediction

The Future Event Time Prediction task constitutes Stage 2 (Prediction) of our framework. Here, the model is tasked with predicting the specific future date (YYYY-MM) of a news event based on its extracted headline and abstract, focusing on events occurring after the model's initial knowledge cutoff. The prompt designed to elicit these future predictions is displayed in Figure [12.](#page-30-0)

### I.6 Prompt for Creative Future Scenario Generation

The Creative Future Scenario Generation task is the focus of Stage 3 (Generation). In this stage, the model leverages capabilities developed previously to generate plausible, hypothetical news event descriptions or headlines for a specified future date and thematic category (*e.g.*, Business, Technology). This task evaluates the model's ability to creatively imagine coherent future events. The prompt used to guide this generative process is presented in Figure [13.](#page-31-0)

#### <span id="page-28-0"></span>Prompt for Event Ording Task

"<|im\_start|>system\n"

"You are a helpful assistant. You first think about the reasoning process in your mind and then provide the user with the answer.\n"

"<|im\_end|>\n"

"<|im\_start|>user\n"

"Please carefully read the following three news article information:\n"

"News article 1:\n"

f"Headline: {event1['headline']}\n"

f"Abstract: {event1['abstract']}\n"

"News article 2:\n"

f"Headline: {event2['headline']}\n"

f"Abstract: {event2['abstract']}\n"

"News article 3:\n"

f"Headline: {event3['headline']}\n"

f"Abstract: {event3['abstract']}\n"

"For the purpose of this inference, assume that the three events described in the articles definitely occur. " "Based on the information provided and your general knowledge, determine the specific occurrence date for each event and then arrange the three events in ascending chronological order.\n"

"- You can recall the events related to these three and their occurrence dates to help you infer.\n"

"- Provide your answer in the following format:\n"

" 'Event 1: YYYY-MM, Event 2: YYYY-MM, Event 3: YYYY-MM. Event order: X-X-X.'\n"

"- Do not output 'No event' under any circumstances. Always provide your best inferred dates, even if the information is ambiguous.\n"

"- Show your reasoning process in <think> </think> tags, and return the final answer on a new line in <answer> </answer> tags, for example <answer>Event 1: 2023-03, Event 2: 2020-11, Event 3: 2023-08. Event order: 2-1-3.</answer>.\n"

"Your answer must strictly follow the above format.\n"

"<|im\_end|>\n"

"<|im\_start|>assistant\n"

"Let me carefully review all the relevant details and systematically work through the reasoning process.\n" "<think>"

Figure 10: Prompt for the Event Ordering task.

#### <span id="page-29-0"></span>Prompt for Masked Time Entity Completion Task

"<|im\_start|>system\n"

"You are a helpful assistant. You first think about the reasoning process in your mind and then provide the user with the answer.\n"

"<|im\_end|>\n"

"<|im\_start|>user\n"

"Please carefully read the following news article information:\n"

f"Headline: {event['headline']}\n"

f"Abstract: {event['abstract']}\n"

"For the purpose of this inference, assume that the event described in the article definitely occurs. " "In the article, one time expression has been masked using either <YEAR> or <MONTH>. " "Based on the information provided and your general knowledge, determine the specific occurrence date for the event and fill in the missing time entity by replacing the mask with the appropriate value.\n"

"- For the occurrence date, use a complete 4-digit year and a 2-digit month (e.g., 2023-01).\n"

"- For a missing year, provide a complete 4-digit year (e.g., 2020).\n"

- "- For a missing month, provide the full month name with correct capitalization (e.g., June).\n"
- "- You can recall the events related to this article and their occurrence dates to help you infer.\n"

"- Provide your answer in the following format:\n"

" 'Event: YYYY-MM. Missing entity: XXXXX.'\n"

"- Do not output 'No event' under any circumstances. Always provide your best inferred dates, even if the information is ambiguous.\n"

"- Show your reasoning process in <think> </think> tags, and return the final answer on a new line in <answer> </answer> tags, for example <answer>Event: 2021-10. Missing entity:

December.</answer>.\n"

"Your answer must strictly follow the above format.\n"

"<|im\_end|>\n"

"<|im\_start|>assistant\n"

"Let me carefully review all the relevant details and systematically work through the reasoning process.\n"

"<think>"

Figure 11: Prompt for the Masked Time Entity Completion task.

#### <span id="page-30-0"></span>Prompt for Future Event Prediction Task

"<|im\_start|>system\n"

"You are a helpful assistant. You first think about the reasoning process in your mind and then provide the user with the answer.\n"

"<|im\_end|>\n"

"<|im\_start|>user\n"

f"Please carefully read the following news article information:\n"

f"Headline: {event['headline']}\n"

f"Abstract: {event['abstract']}\n"

"For the purpose of this prediction, assume that the event described in the article definitely will occur within the next few months or years. "

"Based on the information provided and your general knowledge, determine the most likely specific future occurrence date of the event.\n"

"- You can recall relevant and similar events in the past and their occurrence dates and identify the development patterns to help you predict.\n"

"- Output the event's predicted occurrence date in the format 'YYYY-MM'.\n"

"- Do not output 'No event' under any circumstances. Always provide your best prediction, even if the information is ambiguous.\n"

"- Show your reasoning process in <think> </think> tags, and return the final answer on a new line in <answer> </answer> tags, for example <answer>2025-03</answer>.\n"

"Your answer must strictly follow the above format.\n"

"<|im\_end|>\n"

"<|im\_start|>assistant\n"

"Let me carefully review all the relevant details and systematically work through the reasoning process.\n"

"<think>"

Figure 12: Prompt for the Future Event Time Prediction task.

### <span id="page-31-0"></span>Prompt for Creative Future Scenario Generation Task

"<|im\_start|>system\n"

"You are a helpful assistant. You first think about the reasoning process in your mind and then provide the user with the answer.\n"

"<|im\_end|>\n"

"<|im\_start|>user\n"

f"Given the target future date of {target\_date}, generate THREE distinct and plausible news headlines and abstracts {topic\_instruction} that might be published on that date.\n\n"

"You can follow these steps in your reasoning:\n"

f"1. Analyze current trends and development patterns in relevant fields before {target\_date}\n"

f"2. Infer what stage of development might be reached by {target\_date}\n"

"3. Based on this reasoning, generate THREE credible and DIFFERENT news articles on the same topic\n\n"

"Your generated news should:\n"

f"- Be realistic and plausible for publication in {target\_date}\n"

"- Avoid extreme or highly unlikely scenarios\n"

f"- Be written from the perspective of {target\_date}, not as a prediction from the present\n"

f"- Reflect reasonable developments that could occur between now and {target\_date}\n"

"- Have significant differences from each other - cover different angles, events, or developments within the same topic\n\n"

"- Be written ONLY in English, do not use any other languages\n\n" # new requirement

f"Show your reasoning process in <think></think> tags, explaining why these news items are likely to occur by {target\_date}, then provide your answer in <answer></answer> tags using the following format exactly:\n\n"

"NEWS 1:\n"

"Headline: [News headline 1]\n"

"Abstract: [1-2 sentence news abstract 1]\n\n"

"NEWS 2:\n"

"Headline: [News headline 2]\n"

"Abstract: [1-2 sentence news abstract 2]\n\n"

"NEWS 3:\n"

"Headline: [News headline 3]\n"

"Abstract: [1-2 sentence news abstract 3]\n"

"<|im\_end|>\n"

"<|im\_start|>assistant\n"

f"Let me carefully consider what news events {topic\_instruction} might plausibly occur in the target timeframe based on current trends and development patterns and systematically work through the reasoning process.\n"

"<think>"

Figure 13: Prompt for the Creative Future Scenario Generation task.
