---
cite_key: "anokhin2024"
title: "AriGraph: Learning Knowledge Graph World Models with Episodic Memory for LLM Agents"
authors: "Petr Anokhin, Nikita Semenov, Artyom Sorokin, Dmitry Evseev, Mikhail Burtsev, Evgeny Burnaev"
year: 2024
doi: "10.48550/arXiv.2407.04363"
url: "https://arxiv.org/abs/2407.04363"
relevancy: "High"
downloaded: "Yes"
tags:
  - "LLM Agents"
  - "Episodic Memory"
  - "Knowledge Graphs"
  - "Memory Architecture"
  - "Temporal Modeling"
tldr: "LLM agents can develop structured memory representations through knowledge graph world models with episodic memory integration."
date_processed: "2025-07-02"
phase2_processed: true
original_folder: "arigraph_kg_world_models_episodic_memory_2024"
images_total: 16
images_kept: 16
images_removed: 0
---

# AriGraph: Learning Knowledge Graph World Models with Episodic Memory for LLM Agents

Petr Anokhin<sup>1</sup> , Nikita Semenov<sup>2</sup> , Artyom Sorokin<sup>1</sup> , Dmitry Evseev<sup>2</sup> , Andrey

> Kravchenko<sup>4</sup> , Mikhail Burtsev<sup>3</sup> and Evgeny Burnaev<sup>2</sup>,<sup>1</sup>

> > <sup>1</sup>AIRI, Moscow, Russia

<sup>2</sup>Skoltech, Moscow, Russia

<sup>3</sup>London Institute for Mathematical Sciences, London, UK

<sup>4</sup>University of Oxford, UK

anokhin@airi.net

## Abstract

Advancements in the capabilities of Large Language Models (LLMs) have created a promising foundation for developing autonomous agents. With the right tools, these agents could learn to solve tasks in new environments by accumulating and updating their knowledge. Current LLM-based agents process past experiences using a full history of observations, summarization, retrieval augmentation. However, these unstructured memory representations do not facilitate the reasoning and planning essential for complex decision-making. In our study, we introduce AriGraph, a novel method wherein the agent constructs and updates a memory graph that integrates semantic and episodic memories while exploring the environment. We demonstrate that our Ariadne LLM agent, consisting of the proposed memory architecture augmented with planning and decision-making, effectively handles complex tasks within interactive text game environments difficult even for human players. Results show that our approach markedly outperforms other established memory methods and strong RL baselines in a range of problems of varying complexity. Additionally, AriGraph demonstrates competitive performance compared to dedicated knowledge graph-based methods in static multi-hop question-answering.

## 1 Introduction

Impressive language generation capabilities of large language models (LLMs) has sparked substantial interest in their application as core components for creating autonomous agents capable of interacting with dynamic environments and executing complex tasks. Over the past year, the research community has explored general architectures and core modules for such LLM agents [Wang *et al.*[, 2024;](#page-8-0) [Sumers](#page-8-1) *et al.*, 2024; Cheng *et al.*[, 2024\]](#page-7-0). A crucial property of a general cognitive agent is its ability to accumulate and use knowledge. A long-term memory allows an agent to store and recall past experiences and knowledge, enabling it to learn from previous

encounters and make informed decisions. However, the question of the best way to equip an agent with these capabilities remains open. Despite the constraints inherent in transformer architectures, contemporary methods enable LLMs to manage contexts encompassing millions of tokens [\[Ding](#page-7-1) *et al.*, [2024b\]](#page-7-1). However, this approach proves inefficient for agents required to maintain continuous interaction with their environment. Such agents must hold an entire historical context in memory to perform actions, which is not only costly but also limited in handling complex logic hidden in vast amounts of information. Research into alternative frameworks like Recurrent Memory Transformer [\[Bulatov](#page-7-2) *et al.*, 2022; [Bulatov](#page-7-3) *et al.*[, 2024\]](#page-7-3) and MAMBA [\[Gu and Dao, 2023\]](#page-7-4) seeks to provide long-term memory solutions, though these models are still in their infancy.

Currently, the most popular solution for incorporating memory to LLM agents is the Retrieval-Augmented Generation (RAG) approach. RAG in a form of vector retrieval leverages an external database to enhance the model's prompt with relevant information. This technique is commonly used in memory architectures for LLM agents, often to recall specific observations or learned skills. However, it suffers from unstructured nature, greatly reducing the ability to retrieve related information, which may be scattered throughout the agent's memory. These limitations can be overcome by using knowledge graphs as database. This approach has also experienced a resurgence with the advent of LLMs [\[Pan](#page-8-2) *et al.*[, 2024\]](#page-8-2). However, for a robust memory architecture, integrating both structured and unstructured data is essential. In cognitive science, this integration parallels the concepts of semantic and episodic memories. Semantic memory encompasses factual knowledge about the world, whereas episodic memory pertains to personal experiences, which often contain richer and more detailed information. Though traditionally considered separate due to their distinct neurological representations, recent studies suggest these memory types are interconnected [\[Wong Gonzalez, 2018\]](#page-8-3). Semantic knowledge is built upon the foundation of episodic memory and subsequently provides a structured base for associative memory. This allows for the integration of various memory aspects, including episodic memories themselves.

In our research, we have developed a memory architecture

![](_page_1_Figure_0.jpeg)
<!-- Image Description: The image contains two parts. (A) illustrates the Ariadne LLM agent architecture: a directed graph ("AriGraph") representing episodic and semantic memory, feeding into a decision-making module interacting with an environment. (B) is a bar chart comparing the normalized scores of Ariadne against other agents (human players, Reflexion, Simulacra, Summary, RAG, and full history) on text-based games, showing Ariadne's superior performance. Error bars represent variability. -->

Figure 1: (A) The architecture of our Ariadne agent, equipped with AriGraph memory. AriGraph integrates both semantic knowledge graph and past experiences. Memory in the form of a semantic knowledge graph extended with episodic vertices and edges significantly enhances the performance of LLM-agent in text-based games. (B) The average performance of our agent on text games, compared to various baselines including human players and other LLM memory implementations. The LLM-agents differ only in the memory module, while the decisionmaking component remains identical across all versions. The results for the agents are displayed for the top three out of five runs. For human players, the results are presented as both the top three and the average across all participants.

called Ariadne's Graph (AriGraph), that integrates semantic and episodic memories within a memory graph framework. A knowledge graph represents a network of interconnected semantic knowledge, while episodic memories are depicted as episodic edges that can connect multiple relations within the graph. As an agent interacts with environment, it learns joint semantic and episodic world model by updating and extending knowledge graph based memory. This architecture not only serves as a foundational memory framework but also aids in environmental modeling, improving spatial orientation and exploration capabilities. For the general framework of our LLM agent called Ariadne, we employed pipeline of memory retrieval, planing and decision making. For evaluation of proposed methods we set up experiments to study two research questions.

RQ1. Can LLM based agents learn useful structured world model from scratch via interaction with an environment?

RQ2. Does structured knowledge representation improve retrieval of relevant facts from memory and enable effective exploration?

We evaluated our agent in complex interactive tasks in Textworld and NetHack environments [Cotˆ e´ *et al.*[, 2018;](#page-7-5) Kuttler ¨ *et al.*[, 2020\]](#page-7-6). Experimental results demonstrate that our agent Ariadne can effectively learn through interactions with environment and significantly outperforms other memory approaches for LLMs such as full history, summarization, RAG, Simulacra [Park *et al.*[, 2023\]](#page-8-4) and Reflexion [\[Shinn](#page-8-5) *et al.*[, 2023\]](#page-8-5). We also show that our method outperforms existing reinforcement learning (RL) baselines. We also evaluated our approach on the classical roguelike game NetHack, where our agent with local observations achieved scores comparable

to an agent with ground-truth knowledge. Although AriGraph was originally designed for an agent interacting with the environment, it also demonstrates competitive performance on multi-hop question answering tasks.

## 2 AriGraph World Model

Memory graph structure. AriGraph world model G = (Vs, Es, Ve, Ee) consists of *semantic*(Vs, Es) and*episodic memory*(Ve, Ee) vertices and edges (see Figure [2\)](#page-3-0). At each step t agent receives observation o<sup>t</sup> and sends action a<sup>t</sup> back to the environment. The environment also returns rewards r<sup>t</sup> that are not visible to the LLM agent but are used to evaluate its performance. The agent continuously learns world model G by extracting semantic triplets (object1, relation, object2) from textual observations ot.

- V<sup>s</sup> is a set of semantic vertices. Semantic vertices correspond to objects extracted from triplets.
- E<sup>s</sup> is a set of semantic edges. Semantic edge is a tuple (v, rel, u), where u, v are semantic vertices and rel is a relationship between them. Semantic edges essentially represent triplets integrated in the*semantic memory*.
- V<sup>e</sup> is a set of episodic vertices. Each episodic vertex corresponds to an observation received from the environment at the respective step v t <sup>e</sup> = ot.
- E<sup>e</sup> is a set of episodic edges. Each episodic edge e t <sup>e</sup> = (v t e , E<sup>t</sup> s ) connects all semantic triplets E<sup>t</sup> s extracted from o<sup>t</sup> with each other and corresponding episodic vertex v t e . In other words episodic edges represent temporal relationship "happened at the same time".[1](#page-1-0)

<span id="page-1-0"></span><sup>1</sup> Strictly speaking, episodic edges cannot be called edges or

| Algorithm 1: Memory Graph Search                               |
|----------------------------------------------------------------|
| Input: set of queries Q, Vs, Es, Ve, Ee,                       |
| number of episodic vertices k, semantic                        |
| search depth d and width w                                     |
| Q<br>Result: retrieved episodic vertices V<br>, retrieved<br>e |
| semantic triplets EQ<br>s                                      |
| EQ<br>← ∅,<br>s                                                |
| foreach q in Q do                                              |
| E′<br>s ← SemanticSearch(q, Vs, Es, d, w)                      |
| EQ<br>← EQ<br>s ∪ E′<br>s<br>s                                 |
| end                                                            |
| Q<br>← EpisodicSearch(EQ<br>V<br>, Ve, Ee, k)<br>e<br>s        |
| return EQ<br>Q<br>, V<br>s<br>e                                |

<span id="page-2-0"></span>Constructing AriGraph. Interaction with the environment can provide the agent with an information about the world to create new or update previously acquired knowledge. Given new observation ot, LLM agent extracts new triplets as semantic vertices V t s and edges E<sup>t</sup> s . To find already existing knowledge about the objects mentioned in o<sup>t</sup> a set of all semantic edges Erel s incident to vertices V t s is filtered out. Then outdated edges in Erel s are detected by comparing them with E<sup>t</sup> s and removed from the graph. After clearing outdated knowledge we expand semantic memory with V t s and E<sup>t</sup> s . Episodic memory is updated by simply adding new episodic vertex v t e containing o<sup>t</sup> and new episodic edge that connect all edges in E<sup>t</sup> <sup>s</sup> with v t e . Episodic nodes store agent's past history and episodic edges connects all knowledge received at the same step. See Appendix [E](#page-11-0) for prompts used to extract new triplets and detect outdated knowledge.

Retrieval from AriGraph. For successful decisionmaking in a partially observable environment, the agent needs to be able to retrieve relevant knowledge. Retrieval from the AriGraph memory consists of two procedures: (1) a semantic search returns the most relevant triplets (semantic edges) and (2) an episodic search that, given extracted triplets, returns the most relevant episodic vertices Ve. The pseudo-code for the search is presented in the Algorithm [1.](#page-2-0)

Semantic search relies on semantic similarity and semantic graph structure to recall the most relevant triplets. Given a query, the retriever (pre-trained Contriever model [\[Izacard](#page-7-7) *et al.*[, 2022\]](#page-7-7)) selects the most relevant semantic triplets. Then, the set of vertices incident to the found triplets is used to recursively retrieve new edges from the graph. Depth and breadth of the search can be controlled by respective hyperparameters d and w. For details see Appendix [A.](#page-9-0)

Episodic search starts with the results of the semantic search as an input. Episodic edges link the input triplets with past episodic vertices representing observations. The number of input triplets associated with a particular episodic vertex is used to calculate their relevance:

$$
rel(v_e^i) = \frac{n_i}{max(N_i, 1)} log(max(N_i, 1)), \qquad (1)
$$

where n<sup>i</sup> is a number of input triplets incident to episodic edge e i , N<sup>i</sup> is a total number triplets (semantic edges) incident to e i and log (max(N<sup>i</sup> , 1)) is a weighting factor to prevent high scores for low information observations. We apply a log2(Ni) scaling to give more weight to observations with more extracted triplets. Additionally, observations containing exactly one triplet are assigned zero weight, as they are unlikely to provide information beyond the triplet itself. k most relevant episodic vertices (containing respective observations) are returned as a result of the episodic search.

## 3 Ariadne cognitive architecture

To test utility of AriGraph world modelling method we propose an agentic architecture called Ariadne. Ariadne agent interacts with an unknown environment to accomplish a goal set by a user. Throughout this process, at each time step, the agent learns a world model, plans and executes actions. Ariadne has *long-term*memory stored as AriGraph and*working*memory containing information for current planning and decision making.

Given an observation the agent updates world model and retrieves semantic and episodic knowledge from AriGraph to working memory. Working memory is also populated with a final goal description, current observation, history of recent observation and actions. At the planning stage, Ariadne agent uses content of working memory to create new or update existing plan as a series of task-relevant sub-goals, each accompanied by a concise description. The planning module also evaluates the outcomes of actions based on feedback from the environment after each action at step t − 1, adjusting the plan accordingly.

The revised plan is added to the working memory which is accessed by the decision-making module, tasked with selecting the most suitable action aligned with the current plan's objectives. This module adheres to the ReAct [Yao*[et al.](#page-8-6)*, [2023\]](#page-8-6) framework, requiring the agent to articulate the rationale behind an action before execution. Separation of planning from decision-making enables LLMs to focus on distinct cognitive processes. In text-based environments an agent selects an action from the list of valid actions. Our agent can also use graph specific function for navigation utilizing its memory module. It extends its action space with "go to location" type commands and infers an optimal route to a target location using spatial relations stored in a semantic graph.

## 4 Experimental Setup

### 1 TextWorld interactive environments

We compared Ariadne agent with alternative methods in a series of text based games involving spatial navigation, object collection and tool manipulation. Detailed descriptions of each game, including their difficulty levels and environmental maps, can be found in the Appendix [F.](#page-13-0) All these games can be considered Partially Observable MDPs (POMDPs). Such games have long been benchmarks for researching agents capable of effectively remembering information and establishing long-term dependencies [\[Parisotto](#page-8-7) *et al.*, 2020; [Pleines](#page-8-8) *et al.*, 2022; [Sorokin](#page-8-9) *et al.*, 2022].

Treasure Hunting. The primary objective is to retrieve the hidden treasure, with a series of rooms providing keys

even hyperedges, because they connect vertices with multiple graph edges, but for simplicity we call them edges or episodic edges.

<span id="page-3-0"></span>![](_page_3_Figure_0.jpeg)
<!-- Image Description: The image displays two diagrams. (A) shows a knowledge graph representing semantic and episodic memory. Nodes represent objects (e.g., Tuna, Table) and edges represent relationships (e.g., "contains," "is on"). Different colors denote semantic and episodic information. (B) illustrates a cognitive architecture for an agent. It shows information flow from observation through working memory, planning, and decision-making modules to produce actions within an environment. The AriGraph module learns and updates the world model. The diagram clarifies the agent's reasoning process. -->

Figure 2: AriGraph world model and Ariadne cognitive architecture. (A) AriGraph learns episodic and semantic knowledge during interaction with unknown environment. At each time step t new episodic vertex (containing full textual observation ot) is added to the episodic memory. Then LLM model parses observation o<sup>t</sup> to extract relevant relationships in a form of triplets (object1, relation, object2). These triplets are used to update semantic memory graph. The connection between episodic and semantic memory occurs through episodic edges that link each episodic vertex with all triplets extracted from respective observation. (B) Ariadne agent explores the environment and accomplishes tasks with AriGraph. User sets goal to the agent. Working memory is populated with recent history of observations and actions, relevant semantic and episodic knowledge retrieved from the AirGraph world model. Planing LLM module uses content of working memory to generate new or update existing plan. Results of planning are stored back in working memory. Finally, a ReAct-based module reads memory content and selects one of possible actions to be executed in the environment. Every observation triggers learning that updates agent's world model.

and clues leading to the final goal. The basic variation has 12 rooms and 4 keys, hard one has 16 rooms and 5 keys and hardest contains 36 rooms, 7 keys and additional distract items in every room.

south of Cleaning. The goal is to clean a house by identifying and returning misplaced items to their correct locations. Environment consists of 9 rooms (kitchen, pool, etc.) and contains 11 misplaced items (among many other items). To solve the problem, the agent needs to memorize the location of rooms and objects, as well as reason about objects placement.

Cooking. The goal is to prepare and consume a meal by following a recipe, selecting the correct ingredients, and using appropriate tools, while navigating in multi-room house. The task is testing agents ability to remember relevant information and plan according to it. Basic difficulty task features 9 locations and 3 ingredients and hard task features 12 locations and 4 ingredients, while hardest task also features closed doors and inventory management.

For baselines we used Ariadne's planning and decision making module with one of the following types of memory instead of AriGraph model: full history of observations and actions, iterative summarization, RAG, RAG with Reflexion [Shinn *et al.*[, 2023\]](#page-8-5), and Simulacra - memory implementation from [Park *et al.*[, 2023\]](#page-8-4).

*Full history*involves retaining a complete record of all observations and actions to inform decision-making at every step.*Summarization*, as an alternative to storing the full history, focuses on retaining only the necessary information while discarding the rest. The standard *RAG*baseline retrieves top-k memories based on their similarity score to the current observation and plan.*Simulacra*features a scoring mechanism that integrates recency, importance, and relevance, alongside reflections on the extracted memories. The*Reflexion*baseline differs from other methods in its approach, as it operates over multiple trials. After failing a trial, the agent reflects on its trajectories to document information that may assist in solving the task in subsequent trials. We used the gpt-4-0125-preview as LLM backbone for AriGraph and other LLM-based baselines.

Additionally, we tested our architecture on a variation of the cooking test from [\[Adhikari](#page-7-8)*et al.*, 2021] to compare it with RL baselines. These tasks have 4 levels of difficulty, however, they are significantly simpler than our main tasks, having fewer locations, ingredients, and required actions (Appendix [F\)](#page-13-0).

For *RL*baselines, we collect the best results reported by [\[Adhikari](#page-7-8)*et al.*, 2021; Tuli *et al.*[, 2022;](#page-8-10) Basu *et al.*[, 2024\]](#page-7-9) for the GATA, LTL-GATA, and EXPLORER architectures on the Cooking task with four difficulties levels from [\[Adhikari](#page-7-8) *et al.*[, 2021\]](#page-7-8).

To estimate human performance in the same games, we developed a graphical user interface , allowing volunteers to play basic versions of the Treasure Hunt, The Cleaning, and the Cooking. After collecting the data, we excluded sessions where the game was not completed.

#### 2 NetHack environment

NetHack [\[Kuttler](#page-7-6) ¨ *et al.*, 2020] is a classic roguelike adventure game featuring procedurally generated multi-level dungeon (see Figure [13](#page-19-0) in Appendix for a dungeon level example). It poses significant challenges for both LLM-based and RLbased approaches, requiring complex exploration, resource management, and strategic planning.

We based our experiments on NetPlay [\[Jeurissen](#page-7-10) *et al.*, [2024\]](#page-7-10) agent, which demonstrates state-of-the-art performance among LLM agents that do not rely on finetuning or RL. In NetPlay agent receives textual observations containing all information about current explored dungeon level. These

<span id="page-4-0"></span>![](_page_4_Figure_0.jpeg)
<!-- Image Description: The image presents bar graphs comparing normalized scores across different methods (Ariadne, Reflexion, Simulacra, human performance) on three tasks: Treasure Hunt, Cooking, and Cleaning. Subplots (A) show results using various approaches, while (B) displays results for harder versions of Treasure Hunt and Cooking. Subplot (C) shows human evaluations of the different methods across all three tasks. Error bars represent uncertainty. The figure aims to demonstrate comparative performance of different methods on complex reasoning tasks. -->

Figure 3: AriGraph world model enables Ariadne agent to successfully solve variety of text games. (A) Ariadne outperform baseline agents with alternative types of memory. (B) Ariadne with episodic and semantic memory scales to harder environments without losing performance. (C) Ariadne shows performance comparable to the best human players. The Y-axis shows the normalized score, which is calculated relative to the maximum possible points that can be obtained in each environment. Error bars show standard deviation. The number of max steps is set to 60 in the Cooking and to 150 in other games.

observations (*Level obs*) effectively function as handcrafted memory oracle for the agent.

To evaluate our Ariadne agent, we restricted textual observations to agent's current room or corridor (*Room Obs*), testing whether AriGraph world model could compensate for this restriction by remembering all relevant level information.

We compare three agents. The first is *NetPlay [Room obs]*with restricted textual observations, the second is our*Ariadne [Room obs]*agent that receives Room Obs and updates Ari-Graph, and the last is*NetPlay [Level obs]*with access to inforation about explored level.

#### 3 Multi-hop Q&A

Although our memory architecture was originally designed for an agent interacting with the environment, we evaluated its performance on standard multi-hop Q&A benchmarks — Musique [\[Trivedi](#page-8-11)*et al.*, 2022] and HotpotQA [\[Yang](#page-8-12) *et al.*, [2018\]](#page-8-12) to show its robustness and efficiency in more standard retrieval tasks. We made slight adjustments to the promts and replaced Contriever model with BGE-M3[\[Chen](#page-7-11) *et al.*, [2024\]](#page-7-11), as it is a better fit for general text encoding. We used 200 random samples from both datasets similar to [\[Li](#page-7-12) *et al.*[, 2024a\]](#page-7-12). We compared the performance of our approach against Graphreader [Li *et al.*[, 2024a\]](#page-7-12), ReadAgent [Lee *[et al.](#page-7-13)*, [2024\]](#page-7-13), HOLMES [Panda *et al.*[, 2024\]](#page-8-13), GraphRAG [\[Edge](#page-7-14) *et al.*[, 2024\]](#page-7-14) and RAG baselines provided in [Li *et al.*[, 2024a\]](#page-7-12).

## 5 Results

### 1 TextWorld

Every LLM based agent had five attempts to solve each game. The normalized score of one means that an agent completed the game, and score less than one represents intermediate progress. Results on text-based games are shown on the Figure [3](#page-4-0) (for dynamics see Appendix [G\)](#page-13-1). We estimate performance as average of three best runs. Ariadne successfully remembers and uses information about state of the world for all three tasks. Baseline agents are unable to solve the Treasure Hunt, and fail to find even second key in the Treasure Hunt Hardest. On the other hand, Ariadne successfully solves the Treasure Hunt in about fifty steps, maintains robust performance in the Treasure Hunt Hard, and is able to complete the Treasure Hunt Hardest with more then double amount of rooms compared to Hard version, additional keys and distractors (see Appendix [G\)](#page-13-1).

Compared to the Treasure Hunt, the Cleaning game possesses a slightly different challenge as it is more important to properly filter outdated information about object locations, than not to lose any information. This is evident from the reduced usefulness of Episodic Memory in Ariadne agent and Full history baseline, since both memory modules focus on retaining long-term information. Overall Ariadne notably outperforms alternatives in this game. Moreover, Ariadne also outperforms Reflexion, which has additional information between episodes [Shinn *et al.*[, 2023\]](#page-8-5). This baseline shows markable performance growth (in comparison wuth RAG) at the second try, but degrades with following tries.

The Cooking game has the highest difficulty, because any error at intermediate step prevents completion of the whole game. All baseline agents (except Reflexion 2-shot with obvious advantage over other methods) fail to complete cooking tasks due to insufficient or misused information. In this game, episodic memory is particularly important, allowing the agent

<span id="page-5-0"></span>![](_page_5_Figure_0.jpeg)
<!-- Image Description: The image presents four bar graphs comparing the normalized scores of five different methods (GATA, LTL-GATA, EXPLORER, GPT-4, Ariadne) across four levels (Level 1-4). Each bar represents a method's performance at a specific level, with error bars indicating variability. A dashed horizontal line indicates a benchmark score. The purpose is to illustrate and compare the performance of these methods at different complexity levels. -->

Figure 4: Ariadne LLM agent shows top performance compared to RL alternatives. Comparison of Ariadne and Full History baseline (GPT-4) with RL baselines in the cooking benchmark. Ariadne demonstrates superior performance across all 4 difficulty levels

to recall useful observations such as the content of the recipe or cooking instructions. For token usage of every method see Table [3,](#page-10-0) Appendix [D.](#page-10-1)

Comparison with RL baselines on variation of the Cooking task is shown in Figure [4.](#page-5-0) We run Ariadne and GPT-4 with Full history on 4 difficulty levels from the cooking benchmark [\[Adhikari](#page-7-8) *et al.*, 2021]. Ariadne shows superior performance to RL-agents on all 4 levels, especially harder ones. GPT-4 agent with Full history solves only first two levels which is consistent with previous result as the Cooking from Figure [3.](#page-4-0)A is harder than level 4.

Human evaluation. Comparison with respect to human players is shown in Figure [3.](#page-4-0)C. *All Humans*is the average score of all valid (completed) human trials.*Human Top-3*is the average score of three best plays for each task. Ariadne outperforms average human player from our sample on all tasks, and scores similarly to the best human plays in the Cooking and the Treasure Hunt, but underperforms in the Cleaning.

Graph quality. We measured AriGraph's growth rate and update rate during gameplay (see Figure [5\)](#page-6-0). The graph actively grows during the exploration phase and flattens once the agent becomes familiar with the environment. We argue that this indicates that agent can generalize to long interactions with the environment despite constant updates to the semantic graph. Additional results in Appendix [C](#page-9-1) demonstrate that the growth rate of the graph decreases with the increase in quality of LLM backbone.

Overal results demonstrate clear advantage of Ariadne agent over LLM based and RL baselines. Semantic memory enables the Ariadne Agent to build and update knowledge about the current state of the POMDP environment, which is crucial for navigation, exploration and capturing relevant details in interactive environments. On the other hand, episodic memory assists the agent in retrieving detailed long-term information that may not be captured in semantic memory, as demonstrated by the results in the Cooking task.

#### 2 NetHack

The results are presented in Table [1.](#page-5-1) Scores column shows average game score across 3 runs, Levels column shows average number of dungeon levels completed by an agent. GPT-4o was used for all agents. Underscoring the importance of memory in this task,*NetPlay [Level obs]*with access to memory oracle achieved the highest scores, while*NetPlay [Room obs]*with only current room observations performed the worst.*Ariadne [Room obs]*successfully utilized Ari-Graph word model, achieving performance comparable to the baseline with memory oracle.

<span id="page-5-1"></span>Table 1: Ariadne with obscured partial observations performs comparable to NetPlay agent full level information.

| Method              | Score           | Levels      |
|---------------------|-----------------|-------------|
| Ariadne (Room obs)  | 593.00 ± 202.62 | 6.33 ± 2.31 |
| NetPlay (Room obs)  | 341.67 ± 109.14 | 3.67 ± 1.15 |
| NetPlay (Level obs) | 675.33 ± 130.27 | 7.33 ± 1.15 |

#### 3 Multi-hop Q&A

We compared AriGraph with the latest LLM-based approaches that employ knowledge graph construction and retrieval techniques for question answering over documents (Table [2\)](#page-6-1). Our memory architecture, adapted from the Ariadne TextWorld agent, utilizing both GPT-4 and GPT-4omini outperformed baseline methods like ReadAgent (GPT-4), GPT-4 RAG, GPT-4 full context and GraphReader (GPT-4). GraphRAG served as a strong GPT-4o-mini baseline, due to its extremely hight costs. ArigGraph (GPT-4o-mini) showed weaker performance on Musique, but outperformed GraphRAG on HotpotQA. Notably, our approach is more then 10x cheaper in comparison to GraphRAG (Table [3,](#page-10-0) Appendix [D\)](#page-10-1).

The best performance using GPT-4 was achieved by HOLMES, but AriGraph (GPT-4) exhibited comparable results. Notably, all baseline methods were specifically designed for Q&A tasks, incorporating task-specific prompt tuning and additional architectural enhancements. Both GraphRAG and HOLMES employ hyper-relations in their graphs to connect source data with extracted entities, similar to our method. However, these approaches lack mechanisms for updates in dynamic environments, a key advantage of AriGraph.

## 6 Related work

Voyager [Wang*et al.*[, 2023a\]](#page-8-14), Ghost in the Minecraft [\[Zhu](#page-8-15) *et al.*[, 2023\]](#page-8-15) and Jarvis-1 [Wang *et al.*[, 2023b\]](#page-8-16) are advanced, open-ended LLM agents that show significantly better performance in Minecraft compared to earlier techniques. These agents feature memory capabilities through a library of learned skills, summaries of successful actions, and episodic memory with plans for successful task execution. However, they fall short in representing knowledge with semantic structure and depend heavily on the LLM's extensive Minecraft knowledge, or even access to the Minecraft wiki. Generative agents [Park *et al.*[, 2023\]](#page-8-4) mimic human behavior in multiagent environments and were among the pioneers in introducing an advanced memory system for LLM agents, which we use as our baseline. Reflexion [Shinn *et al.*[, 2023\]](#page-8-5) and CLIN [\[Majumder](#page-7-15) *et al.*, 2023] enables agents to reflect on past trajectories, allowing them to store relevant insights about com-

<span id="page-6-0"></span>![](_page_6_Figure_0.jpeg)
<!-- Image Description: The image presents ten line graphs, five pairs arranged vertically. Each pair displays data for a different task: "Treasure Hunt," "Treasure Hunt Hard," "Cooking," "Cooking Hard," and "Cleaning." The top graph in each pair shows the cumulative number of triplets and items over time. The bottom graph shows the number of new triplets and replacements over time. The purpose is to illustrate the progression of triplets and items, along with the rate of change, across different tasks. -->

Figure 5: AriGraph demonstrate good scaling during learning and with environment size. A size of the knowledge graph quickly saturates during exploration and learning phase. KG grows moderately when the Treasure Hunt and the Cooking games include more rooms and objects in their hard versions.

<span id="page-6-1"></span>Table 2: AriGraph memory demonstrates competitive performance on Multi-Hop Q&A datasets. Even in non interactive tasks AriGraph is comparable to strong QA baseline agents. The best results with the base GPT-4o and GPT-4o-mini are shown in bold and underline respectively.

| Method                                            | MuSiQue      |              |              | HotpotQA     |
|---------------------------------------------------|--------------|--------------|--------------|--------------|
|                                                   | EM           | F1           | EM           | F1           |
| BM25(top-3)                                       | 25.0         | 31.1         | 45.7         | 58.5         |
| Ada-002(top-3)                                    | 24.5         | 32.1         | 45.0         | 58.1         |
| GPT-4 full context                                | 33.5         | 42.7         | 53.0         | 68.4         |
| GPT-4 + supporting facts                          | 45.0         | 56.0         | 57.0         | 73.8         |
| ReadAgent(GPT-4)                                  | 35.0         | 45.1         | 48.0         | 62.0         |
| GraphReader(GPT-4)                                | 38.0         | 47.4         | 55.0         | 70.0         |
| HOLMES(GPT-4)                                     | 48.0         | 58.0         | 66.0         | 78.0         |
| AriGraph(GPT-4)                                   | 45.0         | 57.0         | 68.0         | 74.7         |
| GraphRAG(GPT-4o<br>mini)<br>AriGraph(GPT-4o-mini) | 40.0<br>36.5 | 53.5<br>47.9 | 58.7<br>60.0 | 63.3<br>68.6 |

pleted actions in a long-term memory module, but has no structural representation of knowledge and episodic memories. LARP [Yan *et al.*[, 2023\]](#page-8-17) utilizes the concepts of episodic and semantic memories but treats them as separate instances and lacks a structural representation of knowledge.

Considerable research is dedicated to leveraging established knowledge graphs for enhancing Q&A [\[Baek](#page-7-16) *et al.*, [2023;](#page-7-16) Li *et al.*[, 2024b\]](#page-7-17) systems to address the factual knowledge deficiency observed in LLMs. The latest research demonstrating best performance in Q&A tasks includes Graphreader [Li *et al.*[, 2024a\]](#page-7-12), HOLMES [\[Panda](#page-8-13) *et al.*[, 2024\]](#page-8-13), HippoRAG [\[Gutierrez](#page-7-18) ´ *et al.*, 2024], GraphRAG [Edge *et al.*[, 2024\]](#page-7-14) which all employ the technique of building knowledge graphs from texts. However, these studies do not address the context of functioning within an interactive environment, nor do they take into account the updates to

knowledge graphs prompted by new experiences.

Text-based environments [Cotˆ e´ *et al.*[, 2018;](#page-7-5) [Hausknecht](#page-7-19) *et al.*[, 2019;](#page-7-19) [Shridhar](#page-8-18) *et al.*, 2021; Wang *et al.*[, 2022\]](#page-8-19) were originally designed to evaluate reinforcement learning (RL) agents [Guo *et al.*[, 2020;](#page-7-20) Yao *et al.*[, 2020;](#page-8-20) [Ammanabrolu](#page-7-21) *et al.*, 2020; [Ammanabrolu and Hausknecht, 2020;](#page-7-22) Tuli *et al.*[, 2022;](#page-8-10) [Adhikari](#page-7-8) *et al.*, 2021]. Multiple experiments have already explored the potential of LLMs in these complex scenarios [Tsai *et al.*[, 2023;](#page-8-21) Tan *et al.*[, 2023;](#page-8-22) [Momennejad](#page-7-23) *et al.*, 2023; Ding *et al.*[, 2024a\]](#page-7-24). However raw LLMs show poor results in these games without proper agentic architecture and memory.

## 7 Conclusions

In this paper, we introduced AriGraph, a novel knowledge graph world model tailored for LLM agents. AriGraph uniquely integrates semantic and episodic memories from textual observations, providing a structured and dynamic representation of knowledge. We evaluated this approach across a range of interactive text-based games and multi-hop Q&A benchmarks, comparing it against existing memory architectures. To test its capabilities comprehensively, we developed a cognitive architecture called Ariadne, which combines Ari-Graph with planning and decision-making components.

Our results demonstrate that AriGraph significantly outperforms other memory systems in tasks requiring long-term memory, such as decision-making, planning, and exploration in partially observable environments. The structured knowledge representation provided by AriGraph enables efficient retrieval and reasoning, accelerating learning and task completion. Additionally, AriGraph's scalability was evident as it maintained high performance even when the complexity of tasks increased, involving more objects and locations. In multi-hop Q&A benchmarks, AriGraph exhibited competitive performance, underscoring its robustness and adaptability beyond interactive environments.

While promising, our approach can be further enhanced by incorporating multi-modal observations, procedural memories, and more sophisticated graph search methods.

## References

- <span id="page-7-8"></span>[Adhikari *et al.*, 2021] Ashutosh Adhikari, Xingdi Yuan, Marc-Alexandre Cotˆ e, Mikul ´ a´s Zelinka, Marc-Antoine ˇ Rondeau, Romain Laroche, Pascal Poupart, Jian Tang, Adam Trischler, and William L. Hamilton. Learning dynamic belief graphs to generalize on text-based games, 2021.
- <span id="page-7-22"></span>[Ammanabrolu and Hausknecht, 2020] Prithviraj Ammanabrolu and Matthew Hausknecht. Graph constrained reinforcement learning for natural language action spaces, 2020.
- <span id="page-7-21"></span>[Ammanabrolu *et al.*, 2020] Prithviraj Ammanabrolu, Ethan Tien, Matthew Hausknecht, and Mark O. Riedl. How to avoid being eaten by a grue: Structured exploration strategies for textual worlds, 2020.
- <span id="page-7-16"></span>[Baek *et al.*, 2023] Jinheon Baek, Alham Fikri Aji, and Amir Saffari. Knowledge-augmented language model prompting for zero-shot knowledge graph question answering, 2023.
- <span id="page-7-9"></span>[Basu *et al.*, 2024] Kinjal Basu, Keerthiram Murugesan, Subhajit Chaudhury, Murray Campbell, Kartik Talamadupula, and Tim Klinger. Explorer: Exploration-guided reasoning for textual reinforcement learning, 2024.
- <span id="page-7-2"></span>[Bulatov *et al.*, 2022] Aydar Bulatov, Yuri Kuratov, and Mikhail S. Burtsev. Recurrent memory transformer, 2022.
- <span id="page-7-3"></span>[Bulatov *et al.*, 2024] Aydar Bulatov, Yuri Kuratov, Yermek Kapushev, and Mikhail S. Burtsev. Scaling transformer to 1m tokens and beyond with rmt, 2024.
- <span id="page-7-11"></span>[Chen *et al.*, 2024] Jianlv Chen, Shitao Xiao, Peitian Zhang, Kun Luo, Defu Lian, and Zheng Liu. Bge m3-embedding: Multi-lingual, multi-functionality, multi-granularity text embeddings through self-knowledge distillation, 2024.
- <span id="page-7-0"></span>[Cheng *et al.*, 2024] Yuheng Cheng, Ceyao Zhang, Zhengwen Zhang, Xiangrui Meng, Sirui Hong, Wenhao Li, Zihao Wang, Zekai Wang, Feng Yin, Junhua Zhao, and Xiuqiang He. Exploring large language model based intelligent agents: Definitions, methods, and prospects, 2024.
- <span id="page-7-5"></span>[Cotˆ e´ *et al.*, 2018] Marc-Alexandre Cotˆ e,´ Akos K ´ ad´ ar, ´ Xingdi Yuan, Ben Kybartas, Tavian Barnes, Emery Fine, James Moore, Ruo Yu Tao, Matthew Hausknecht, Layla El Asri, Mahmoud Adada, Wendy Tay, and Adam Trischler. Textworld: A learning environment for text-based games. *CoRR*, abs/1806.11532, 2018.
- <span id="page-7-24"></span>[Ding *et al.*, 2024a] Peng Ding, Jiading Fang, Peng Li, Kangrui Wang, Xiaochen Zhou, Mo Yu, Jing Li, Matthew Walter, and Hongyuan Mei. MANGO: A benchmark for evaluating mapping and navigation abilities of large language models, 2024.
- <span id="page-7-1"></span>[Ding *et al.*, 2024b] Yiran Ding, Li Lyna Zhang, Chengruidong Zhang, Yuanyuan Xu, Ning Shang, Jiahang Xu, Fan Yang, and Mao Yang. Longrope: Extending llm context window beyond 2 million tokens, 2024.
- <span id="page-7-14"></span>[Edge *et al.*, 2024] Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt,

and Jonathan Larson. From local to global: A graph rag approach to query-focused summarization, 2024.

- <span id="page-7-4"></span>[Gu and Dao, 2023] Albert Gu and Tri Dao. Mamba: Lineartime sequence modeling with selective state spaces, 2023.
- <span id="page-7-20"></span>[Guo *et al.*, 2020] Xiaoxiao Guo, Mo Yu, Yupeng Gao, Chuang Gan, Murray Campbell, and Shiyu Chang. Interactive fiction game playing as multi-paragraph reading comprehension with reinforcement learning, 2020.
- <span id="page-7-18"></span>[Gutierrez ´ *et al.*, 2024] Bernal Jimenez Guti ´ errez, Yiheng ´ Shu, Yu Gu, Michihiro Yasunaga, and Yu Su. Hipporag: Neurobiologically inspired long-term memory for large language models, 2024.
- <span id="page-7-19"></span>[Hausknecht *et al.*, 2019] Matthew Hausknecht, Prithviraj Ammanabrolu, Cotˆ e Marc-Alexandre, and Yuan Xingdi. ´ Interactive fiction games: A colossal adventure. *CoRR*, abs/1909.05398, 2019.
- <span id="page-7-7"></span>[Izacard *et al.*, 2022] Gautier Izacard, Mathilde Caron, Lucas Hosseini, Sebastian Riedel, Piotr Bojanowski, Armand Joulin, and Edouard Grave. Unsupervised dense information retrieval with contrastive learning, 2022.
- <span id="page-7-10"></span>[Jeurissen *et al.*, 2024] Dominik Jeurissen, Diego Perez-Liebana, Jeremy Gow, Duygu Cakmak, and James Kwan. Playing nethack with llms: Potential and limitations as zero-shot agents, 2024.
- <span id="page-7-6"></span>[Kuttler ¨ *et al.*, 2020] Heinrich Kuttler, Nantas Nardelli, ¨ Alexander Miller, Roberta Raileanu, Marco Selvatici, Edward Grefenstette, and Tim Rocktaschel. The nethack ¨ learning environment. *Advances in Neural Information Processing Systems*, 33:7671–7684, 2020.
- <span id="page-7-13"></span>[Lee *et al.*, 2024] Kuang-Huei Lee, Xinyun Chen, Hiroki Furuta, John Canny, and Ian Fischer. A human-inspired reading agent with gist memory of very long contexts, 2024.
- <span id="page-7-12"></span>[Li *et al.*, 2024a] Shilong Li, Yancheng He, Hangyu Guo, Xingyuan Bu, Ge Bai, Jie Liu, Jiaheng Liu, Xingwei Qu, Yangguang Li, Wanli Ouyang, Wenbo Su, and Bo Zheng. Graphreader: Building graph-based agent to enhance longcontext abilities of large language models, 2024.
- <span id="page-7-17"></span>[Li *et al.*, 2024b] Yihao Li, Ru Zhang, Jianyi Liu, and Gongshen Liu. An enhanced prompt-based llm reasoning scheme via knowledge graph-integrated collaboration, 2024.
- <span id="page-7-15"></span>[Majumder *et al.*, 2023] Bodhisattwa Prasad Majumder, Bhavana Dalvi Mishra, Peter Jansen, Oyvind Tafjord, Niket Tandon, Li Zhang, Chris Callison-Burch, and Peter Clark. Clin: A continually learning language agent for rapid task adaptation and generalization, 2023.
- <span id="page-7-23"></span>[Momennejad *et al.*, 2023] Ida Momennejad, Hosein Hasanbeig, Felipe Vieira Frujeri, Hiteshi Sharma, Nebojsa Jojic, Hamid Palangi, Robert Ness, and Jonathan Larson. Evaluating cognitive maps and planning in large language models with cogeval. In *Thirty-seventh Conference on Neural Information Processing Systems*, 2023.
- <span id="page-7-25"></span>[Murugesan *et al.*, 2020] Keerthiram Murugesan, Mattia Atzeni, Pavan Kapanipathi, Pushkar Shukla, Sadhana

Kumaravel, Gerald Tesauro, Kartik Talamadupula, Mrinmaya Sachan, and Murray Campbell. Text-based rl agents with commonsense knowledge: New challenges, environments and baselines, 2020.

- <span id="page-8-2"></span>[Pan *et al.*, 2024] Shirui Pan, Linhao Luo, Yufei Wang, Chen Chen, Jiapu Wang, and Xindong Wu. Unifying large language models and knowledge graphs: A roadmap. *IEEE Transactions on Knowledge and Data Engineering*, page 1–20, 2024.
- <span id="page-8-13"></span>[Panda *et al.*, 2024] Pranoy Panda, Ankush Agarwal, Chaitanya Devaguptapu, Manohar Kaul, and Prathosh A P. Holmes: Hyper-relational knowledge graphs for multi-hop question answering using llms, 2024.
- <span id="page-8-7"></span>[Parisotto *et al.*, 2020] Emilio Parisotto, Francis Song, Jack Rae, Razvan Pascanu, Caglar Gulcehre, Siddhant Jayakumar, Max Jaderberg, Raphael Lopez Kaufman, Aidan Clark, Seb Noury, et al. Stabilizing transformers for reinforcement learning. In *International conference on machine learning*, pages 7487–7498. PMLR, 2020.
- <span id="page-8-4"></span>[Park *et al.*, 2023] Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, and Michael S. Bernstein. Generative agents: Interactive simulacra of human behavior, 2023.
- <span id="page-8-8"></span>[Pleines *et al.*, 2022] Marco Pleines, Matthias Pallasch, Frank Zimmer, and Mike Preuss. Memory gym: Partially observable challenges to memory-based agents. In *The eleventh international conference on learning representations*, 2022.
- <span id="page-8-5"></span>[Shinn *et al.*, 2023] Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning, 2023.
- <span id="page-8-18"></span>[Shridhar *et al.*, 2021] Mohit Shridhar, Xingdi Yuan, Marc-Alexandre Cotˆ e, Yonatan Bisk, Adam Trischler, and ´ Matthew Hausknecht. ALFWorld: Aligning Text and Embodied Environments for Interactive Learning. In *Proceedings of the International Conference on Learning Representations (ICLR)*, 2021.
- <span id="page-8-9"></span>[Sorokin *et al.*, 2022] Artyom Sorokin, Nazar Buzun, Leonid Pugachev, and Mikhail Burtsev. Explain my surprise: Learning efficient long-term memory by predicting uncertain outcomes. *Advances in Neural Information Processing Systems*, 35:36875–36888, 2022.
- <span id="page-8-1"></span>[Sumers *et al.*, 2024] Theodore R. Sumers, Shunyu Yao, Karthik Narasimhan, and Thomas L. Griffiths. Cognitive architectures for language agents, 2024.
- <span id="page-8-22"></span>[Tan *et al.*, 2023] Qinyue Tan, Ashkan Kazemi, and Rada Mihalcea. Text-based games as a challenging benchmark for large language models, 2023.
- <span id="page-8-11"></span>[Trivedi *et al.*, 2022] Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal. MuSiQue: Multihop questions via single-hop question composition. *Transactions of the Association for Computational Linguistics*, 2022.

- <span id="page-8-21"></span>[Tsai *et al.*, 2023] Chen Feng Tsai, Xiaochen Zhou, Sierra S. Liu, Jing Li, Mo Yu, and Hongyuan Mei. Can large language models play text games well? current state-of-theart and open questions, 2023.
- <span id="page-8-10"></span>[Tuli *et al.*, 2022] Mathieu Tuli, Andrew C. Li, Pashootan Vaezipoor, Toryn Q. Klassen, Scott Sanner, and Sheila A. McIlraith. Learning to follow instructions in text-based games, 2022.
- <span id="page-8-19"></span>[Wang *et al.*, 2022] Ruoyao Wang, Peter Jansen, Marc-Alexandre Cotˆ e, and Prithviraj Ammanabrolu. Science- ´ world: Is your agent smarter than a 5th grader?, 2022.
- <span id="page-8-14"></span>[Wang *et al.*, 2023a] Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Voyager: An open-ended embodied agent with large language models, 2023.
- <span id="page-8-16"></span>[Wang *et al.*, 2023b] Zihao Wang, Shaofei Cai, Anji Liu, Yonggang Jin, Jinbing Hou, Bowei Zhang, Haowei Lin, Zhaofeng He, Zilong Zheng, Yaodong Yang, Xiaojian Ma, and Yitao Liang. Jarvis-1: Open-world multi-task agents with memory-augmented multimodal language models, 2023.
- <span id="page-8-0"></span>[Wang *et al.*, 2024] Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang, Xu Chen, Yankai Lin, Wayne Xin Zhao, Zhewei Wei, and Jirong Wen. A survey on large language model based autonomous agents. *Frontiers of Computer Science*, 18(6), March 2024.
- <span id="page-8-3"></span>[Wong Gonzalez, 2018] Daniela Wong Gonzalez. *The Relationship Between Semantic and Episodic Memory: Exploring the Effect of Semantic Neighbourhood Density on Episodic Memory*. PhD thesis, Electronic Theses and Dissertations, 2018. Paper 7585.
- <span id="page-8-17"></span>[Yan *et al.*, 2023] Ming Yan, Ruihao Li, Hao Zhang, Hao Wang, Zhilan Yang, and Ji Yan. Larp: Language-agent role play for open-world games, 2023.
- <span id="page-8-12"></span>[Yang *et al.*, 2018] Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W. Cohen, Ruslan Salakhutdinov, and Christopher D. Manning. Hotpotqa: A dataset for diverse, explainable multi-hop question answering, 2018.
- <span id="page-8-20"></span>[Yao *et al.*, 2020] Shunyu Yao, Rohan Rao, Matthew Hausknecht, and Karthik Narasimhan. Keep calm and explore: Language models for action generation in text-based games, 2020.
- <span id="page-8-6"></span>[Yao *et al.*, 2023] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. React: Synergizing reasoning and acting in language models, 2023.
- <span id="page-8-15"></span>[Zhu *et al.*, 2023] Xizhou Zhu, Yuntao Chen, Hao Tian, Chenxin Tao, Weijie Su, Chenyu Yang, Gao Huang, Bin Li, Lewei Lu, Xiaogang Wang, Yu Qiao, Zhaoxiang Zhang, and Jifeng Dai. Ghost in the minecraft: Generally capable agents for open-world environments via large language models with text-based knowledge and memory, 2023.

## <span id="page-9-0"></span>A Memory Graph Search Details

Pseudo-code for SemanticSearch function in AriGraph is listed in Algorithm [2.](#page-9-2) This algorithm is close to BFS search. The main difference is the use of retrieval mechanism in function EmbedAndRetrieve. Function EmbedAndRetrieve(E, q, w) uses pretrained Contriever [\[Izacard](#page-7-7) *et al.*, 2022] model to compute embeddings for edges E and query q and then returns top w edges with a highest similarity score. Similarity score between edge e and query q is a dot product between their embeddings. Most of the times, when query for EmbedAndRetrieve is a semantic vertex, it simply returns edges incident to this vertex, but also has ability to retrieve edges connected to vertices that are semantically close to the query vertex. For example, semantic graph can contain separate vertices for "grill" and "grilling" that are not directly connected, so searching for "grill" can potentially return edge ("bbq", "used for", "grilling").

| Algorithm 2: Semantic Search |  |  |  |
|------------------------------|--|--|--|
|------------------------------|--|--|--|

```text
Input: search query q, Es, search depth d, search
      width w
Result: relevant vertices semantic V
                             q
                            s
                              and edges Eq
                                        s
Eq
 s ← ∅
L ← ∅ // init empty
   queue of queries
Enqueue(L, q) // push q into
   queue L
D[q] ← 0 // set search
   distance for q to zero
while L is not empty do
   q
    ′ ← Dequeue(L) // remove
      first element from L
   if D[q
       ′
        ] ≥ d then
      continue
   end
   // use Contriever model to find
      top w triplets closest to q
                                      ′
   E′
    s ← EmbedAndRetrieve(Es, q′
                                 , w)
   foreach ei
           in E′
               s do
      V
       ′
       s ← IncidentVertices(ei)
         // returns two incident
         semantic vertices
      foreach v in V
                  ′
                 s do
         if v not in L then
            Enqueue(L, v)
            D[v] ← D[q
                      ′
                      ] + 1
         end
      end
   end
   Eq
    s ← Eq
          s ∪ E′
              s
end
return Eq
       s
```text

## <span id="page-9-2"></span>B Exploration

Before any planning or decision-making occurs, an auxiliary agent assesses the need for exploration based on a preestablished plan. Depending on this assessment, it either activates or deactivates exploration mode. Moreover, the graph agent extracts triplets containing information about exits, such as "kitchen, has an unexplored exit, south," and triplets detailing spatial connections between locations like "hall, east of, kitchen." Subsequently, simple graph-based methods can be employed to identify all exits from each room that the agent has detected but not yet explored. This information is then added to the working memory of the agent. Function for finding triplets corresponding to probable unexplored actions is listed in Algorithm [3.](#page-9-3) Current implementation uses expert knowledge about what elements of the semantic graph can represent locations and exits between them.

| Algorithm 3: Unexplored exit detection               |  |  |
|------------------------------------------------------|--|--|
| Input: Vs, Es, Ve, Ee, current location vl           |  |  |
| Result: triplets Eexp<br>with information about<br>s |  |  |
| unexplored exits from vl                             |  |  |
| Eexp ← ∅                                             |  |  |
| Eout ←<br>GetOutgoing(Es, vl)<br>//<br>get           |  |  |
| semantic edges outgoing from<br>vl                   |  |  |
| foreach e in Eout do                                 |  |  |
| if RepresentExit(e)<br>then                          |  |  |
| Eexp ←<br>Eexp ∪ {e}                                 |  |  |
| Ein ←<br>GetIncoming(Es, vl)<br>//<br>get            |  |  |
| semantic edges incoming in<br>vl                     |  |  |
| foreach e in Ein do                                  |  |  |
| if RepresentExit(e)<br>then                          |  |  |
| //<br>remove exits leading to                        |  |  |
| explored locations                                   |  |  |
| Eexp ←                                               |  |  |
| Eexp \ {FindRelatedExit(Eexp, e)}                    |  |  |
|                                                      |  |  |

### <span id="page-9-3"></span>return Eexp

## <span id="page-9-1"></span>C Graph statistics

When working with a graph, it would be advantageous to assess the quality of its construction. Unfortunately, due to the variability in its construction (e.g., the use of synonyms, equivalent restructuring of connections, etc.), direct measurement of its correspondence to the true graph is extremely challenging. Moreover, the inclusion of information in the constructed graph that is not present in the true graph is not always detrimental and can sometimes yield positive effects. For these reasons, we did not measure the quality of the graph but instead measured its growth rate and update rate during gameplay (Fig[.5\)](#page-6-0). Furthermore, we conducted a separate experiment in which the graph was constructed according to our pipeline, but the agent's actions were chosen randomly (Fig[.6\)](#page-10-2). The Cleaning environment was chosen for this setting because, unlike the Treasure Hunt, it contains a large variety of objects with which the agent can interact, and unlike the Cooking, the agent cannot fail. In this setting, we also measured the graph's growth rate and update rate.

From the obtained results, one can conclude that the graph grows most actively during the exploration phase but

<span id="page-10-2"></span>![](_page_10_Figure_0.jpeg)
<!-- Image Description: The image presents six plots, three line graphs above three bar graphs. Each set of graphs compares the performance of three large language models (LLaMA-3-8B, LLaMA-3-70B, GPT-4). The top graphs show the cumulative number of triplets and items over time, illustrating knowledge base growth. The bottom graphs display the number of new triplets, replacements, and items added at each step, providing a granular view of knowledge base updates. The plots analyze knowledge base evolution during model training. -->

Figure 6: Statistics of graph construction and updating during the random walk.

maintains a slower growth rate when the agent operates within the familiar parts of the environment. Additionally, it is evident that the growth rate of the graph decreases as the quality of the LLM used in its construction increases.

## <span id="page-10-1"></span><span id="page-10-0"></span>D Token usage

Table 3: Token Usage Analysis for Text Games and QA Tasks

| Method                               | Prompt Tokens | Completion Tokens |  |
|--------------------------------------|---------------|-------------------|--|
| Text Games (per step)                |               |                   |  |
| Ariadne agent                        | 6,000         | 500               |  |
| RAG memory agent                     | 4,000         | 350               |  |
| Summary memory agent                 | 3,800         | 350               |  |
| Full history memory agent (step 150) | 14,000        | 350               |  |
| Simulacra memory agent               | 7,500         | 400               |  |
| Reflexion memory agent               | 5,800         | 350               |  |
| QA Benchmarks (per task)             |               |                   |  |
| AriGraph                             | 11,000        | 2,500             |  |
| GraphRAG                             | 115,000       | 20,000            |  |

## <span id="page-11-0"></span>E LLM Prompts

### Triplet Extraction Prompt

Guidelines for Building the Knowledge Graph:

- Creating Nodes and Triplets: Nodes should depict entities or concepts, similar to Wikipedia nodes. Use a structured triplet format to capture data, as follows : "subject, relation, object". For example, from " Albert Einstein, born in Germany, is known for developing the theory of relativity," extract "Albert Einstein, country of birth, Germany; Albert Einstein , developed, Theory of Relativity."
- Remember that you should break complex triplets like "John, position, engineer in Google" into simple triplets like "John, position, engineer", "John, work at, Google".

Length of your triplet should not be more than 7 words. You should extract only concrete knowledges, any assumptions must be described as hypothesis.

- For example, from phrase "John have scored many points and potentiallyy will be winner" you should extract "John , scored many, points; John, could be, winner" and should not extract "John, will be, winner". Remember that object and subject must be an atomary units while relation can be more complex and long.
- If observation states that you take item, the triplet shoud be: 'item, is in, inventory' and nothing else.
- Do not miss important information. If observation is 'book involves story about knight, who needs to kill a dragon', triplets should be 'book, involves, knight', 'knight, needs to kill, dragon'. If observation involves some type of notes, do not forget to include triplets about entities this note includes.
- There could be connections between distinct parts of observations. For example if there is information in the beginning of the observation that you are in location, and in the end it states that there is an exit to the east, you should extract triplet: ' location, has exit, east'.

Several triplets can be extracted, that contain information about the same node. For example 'kitchen, contains, apple', 'kitchen, contains, table', 'apple, is on, table'. Do not miss this type of connections.

Other examples of triplets: 'room z, contains, black locker '; 'room x, has exit, east', 'apple, is on, table', ' key, is in, locker', 'apple, to be, grilled', 'potato , to be, sliced', 'stove, used for, frying', 'recipe, requires, green apple', 'recipe, requires, potato'. Do not include triplets that state the current location of

an agent like 'you, are in, location'. Do not use 'none' as one of the entities. If there is information that you read something, do not forget to incluse triplets that state that entitie that you read contains information that you extract.

Example of triplets you have extracted before: {example}

Observation: {observation}

Remember that triplets must be extracted in format: " subject\_1, relation\_1, object\_1; subject\_2, relation\_2, object\_2; ..."

Extracted triplets:'''

#### Outdated Triplet Selection Prompt

The triplets denote facts about the environment where the player moves. The player takes actions and the environment changes, so some triplets from the list of existing triplets can be replaced with one of the new triplets. For example, the player took the item from the locker and the existing triplet "item, is in , locker" should be replaced with the new triplet " item, is in, inventory".

Sometimes there are no triplets to replace:

Example of existing triplets: "Golden locker, state, open"; "Room K, is west of, Room I"; "Room K, has exit, east".

Example of new triplets: "Room T, is north of, Room N"; "

Room T, has exit, south". Example of replacing: []. Nothisg to replace here

- Sometimes several triplets can be replaced with one: Example of existing triplets: "kitchen, contains, broom"; " broom, is on, floor".
- Example of new triplets: "broom, is in, inventory". Example of replacing: [["kitchen, contains, broom" -> " broom, is in, inventory"], ["broom, is on, floor" -> "broom, is in, inventory"]]. Because broom changed location from the floor in the kitchen to players inventory.

Ensure that triplets are only replaced if they contain redundant or conflicting information about the same aspect of an entity. Triplets should not be replaced if they provide distinct or complementary information about entities compared to the new triplets. Specifically, consider the relationships, properties, or contexts described by each triplet and verify that they align before replacement. If there is uncertainty about whether a triplet should be replaced, prioritize retaining the existing triplet over replacing it. When comparing existing and new triplets, if they refer to different aspects or attributes of entities, do not replace them. Replacements should only occur when there is semantic duplication between an existing triplet and a new triplet.

- Example of existing triplets: "apple, to be, cooked", ' knife, used for, cutting', 'apple, has been, sliced' Example of new triplets: "apple, is on, table", 'kitchen,
- contsins, knife', 'apple, has beed, grilled'. Example of replacing: []. Nothing to replace here. These triplets describe different properties of items, so they should not be replaced.

Another example of when not to replase existung triplets: Example of existing triplets: "brush, used for, painting". Example of new triplets: "brush, is in, art class". Example of replacing: []. Nothing to replace here. These triplets describe different properties of brush, so they should not be replaced.

I repeat, do not replace triplets, if they carry differend type of information about entities!!! It is better to leave a tripplet, than to replace the one that has important information. Do not state that triplet needs to be replaced if you are not sure!!!

If you find triplet in Existing triplets which semantically duplicate some triplet in New triplets, replace such triplet from Existing triplets. However do not replace triplets if they refer to different things. ####

Generate only replacing, no descriptions are needed. Existing triplets: {ex\_triplets}. New triplets: {new\_triplets}.

####

Warning! Replacing must be generated strictly in following format: [[outdated\_triplet\_1 -> actual\_triplet\_1], [ outdated\_triplet\_2 -> actual\_triplet\_2], ...], you MUST NOT include any descriptions in answer. Replacing:

#### Exploration check prompt

####

INSTRUCTION: You will be provided with sub-goals and reasons for it from plan of an agent. Your task is to state if this sub goals require exploration of the environment, finding or locating something. Answer with just True or False. #### Plan: {plan0}

#### Planning prompt

```text
####
INSTRUCTION:
You are a planner within the agent system tasked with
     navigating the environment in a text-based game.
Your role is to create a concise plan to achieve your main
     goal or modify your current plan based on new
     information received.
Make sure your sub-goals will benefit the achivment of your
      main goal. If your main goal is an ongoing complex
     process, also put sub-goals that can immediately
     benifit achiving something from your main goal.
If you need to find something, put it into sub-goal.
If you wish to alter or delete a sub-goal within the
     current plan, confirm that this sub-goal has been
     achieved according to the current observation or is
     no longer relevant to achieving your main goal.
     Untill then do not change wording in "sub_goal"
     elements of your plan and their position in the plan.
      Only change wording in "reason" part to track the
     progress of completion of sub-goals.
If sub-goal was completed or confirmed to be no more
     relevant, delete it, replase it with new one or with
     lower priority sub-goals from the plan. Untill then
     keep the structure of sub-goals as it is. Create new
     sub-goals only if they will benifit your main goal
     and do not prioritize them over current sub-goals.
If your task is to obtain something, make shure that the
     item is in your inventory before changing your sub-
     goal.
Your plan contains important information and goals you need
      to complete. Do not alter sub-goals or move them in
     hierarchy if they were not completed!
Pay attention to your inventory, what items you are carring
     , when setting the sub-goals. These items might be
     important.
Pay attention to information from your memory module, it is
      important.
There should always be at least one sub-goal.
State the progress of completing your sub-goals in "reason"
      for each sub-goal.
Write your answer exactly in this json format:
{ "main_goal": "...",
 "plan_steps": [{
    "sub_goal_1": "...",
    "reason": "..."
   },
   {
    "sub_goal_2": "...",
    "reason": "..."
   },
   {
    "sub_goal_...": "...",
    "reason": "..."
   }],
 "your_emotion":
   {
    "your_current_emotion": "emotion",
    "reason_behind_emotion": "..."
   }}
Do not write anything else.
####
1. Main goal: {main_goal}
2. History of {n_prev} last observations and actions: {
     observations}
3. Your current observation: {observation}
4. Information from the memory module that can be relevant
     to current situation: {subgraph}
5. Your {topk_episodic} most relevant episodic memories
     from the past for the current situation: {
     top_episodic}.
6. Your previous plan: {plan0}
*if is explore*7. Yet unexplored exits in the environment:
      {all_unexpl_exits}
```text

#### ReAct decision making prompt

#### #### INSTRUCTION:

You are an action selector within an agent system designed to navigate an environment in a text-based game. Your

role involves receiving information about an agent and the state of the environment alongside a list of possible actions.

- Your primary objective is to choose an action from the list of possible actions that aligns with the goals outlined in the plan, giving precedence to main goal or sub-goals in the order they appear (main goal is highest priority, then sub\_goal\_1, sub\_goal\_2, etc.). However, prioritize sub-goals that can be solved by perfroming single action in current situation, like ' take something', over long term sub-goals.
- Actions like "go to 'location'" will move an agent directly to stated location, use them instead of "go\_west' type of actions, if the destination you want to move to is further than 1 step away.

In tasks centered around exploration or locating something, prioritize actions that guide the agent to previously unexplored areas. You can deduce which locations have been visited based on the history of observations and information from your memory module.

Performing same action typically will not provide different results, so if you are stuck, try to perform other actions or prioritize goals to explore the environment.

You may choose actions only from the list of possible actions. You must choose strictly one action. Write your answer exactly in this json format:

"reason\_for\_action": "reason"

"action\_to\_take": "selected action"

}

{

Do not write anything else. ####

- 1. Main goal: {main\_goal}
- 2. History of {n\_prev} last observations and actions: { observations}
- 3. Your current observation: {observation}
- 4. Information from the memory module that can be relevant to current situation: {subgraph}
- 5. Your {topk\_episodic} most relevant episodic memories from the past for the current situation: { top\_episodic}.
- 6. Your current plan: {plan0}
- 7. Yet unexplored exits in the environment: { all\_unexpl\_exits}

Possible actions in current situation: {valid\_actions}

#### Summarization prompt

#### ####

INSTRUCTION: You are a guide within a team of agents engaging in a textbased game. Your role is to concisely yet thoroughly detail all the essential aspects of the current situation. Ensure that your summary aids in information extraction and facilitates the decisionmaking process by focusing on pertinent details and excluding extraneous information. Incorporate a strategic outlook in your narrative, emphasizing information integral to forming a tactical plan.

Accurately relay the outcomes of previously attempted actions, as this is pivotal for shaping subsequent choices. Your account will form the sole basis on which the decision-making agents operate; thus, clarity and avoidance of potential confusion are paramount.

Be judicious with your inferences, presenting only wellsubstantiated information that is likely to be of practical benefit. Your account should be succinct, encapsulated within a maximum of three paragraphs.

#### Main goal: {main\_goal}

- 2. History of {n\_prev} last observations and actions: { observations}
- 3. Your current observation: {observation}
- 4. Your previous summary: {summary}
- Your summary:

## <span id="page-13-0"></span>F Text-based Games

Treasure Hunting. The primary objective is to unlock the golden locker and retrieve the treasure hidden within. The game consists of rooms each featuring a locker of a different color. Initially, the player finds a key in the first room, along with instructions detailing which specific locker this key can unlock. Each subsequent locker contains another key and a note directing the player to the next key's location, creating a chain of clues and discoveries leading to the golden locker. The easy variation has 12 rooms and 4 keys and hard one has 16 rooms and 5 keys, however second key is significantly harder to find. The hardest variation consist of 36 total rooms, 7 keys and also additional items in each room as noise. Agent receives 1 point for picking a key and 1 point for completing the game. Examples of the Treasure Hunt environment are presented in figures [7,](#page-14-0) [8](#page-15-0) [9](#page-16-0)

Cleaning. The goal is to clean the house that consists of 9 distinct rooms, each designated for a specific purpose, such as a pool, kitchen, etc. Each room contains items, some of which are misplaced, for example, a toothbrush found in the dining room. There are total of 11 misplaced items. The agent's objective is to tidy up the house by identifying items that are out of place and returning them to their appropriate locations. This task requires the agent to utilize reasoning skills to determine the proper locations for items and to effectively recall from memory where each item belongs, while simultaneously managing multiple tasks. Agent receives 1 point for picking up every displaced items, 1 point for placing an item in the right location and -1 for manipulation with correctly placed item. Our task is conceptually similar to the TextWorld Commonsense (TWC) benchmark[\[Murugesan](#page-7-25)*et al.*[, 2020\]](#page-7-25). However, while TWC primarily centers on logical reasoning within one or at most two locations, our emphasis is on environmental exploration and the testing of memory based on past observations. Consequently, we have substantially expanded the number of rooms and items in our setup. Example of the Cleaning environment can be found in figure [10.](#page-17-0)

Cooking. The goal is to prepare and consume a meal. First an agent needs to find a recipe that provides detailed instructions, including required ingredients and specific preparation methods such as dicing, slicing, chopping, grilling, frying, and roasting. Medium difficulty task features 9 locations and 3 ingredients and hard task features 12 locations and 4 ingredients. The agent receives points for correctly selecting ingredients and executing the proper procedures. The game is considered lost if the agent performs any incorrect action or uses an inappropriate tool for a given ingredient. We enhanced the initial observation with instructions and provided explanations for specific actions to tailor the task for LLM models, particularly concerning the appropriate use of household kitchen appliances for different actions with ingredients. For instance, a BBQ should be used for grilling, while a stove is appropriate for frying (see Appendix [E](#page-11-0) for prompt). This allows to test the agent's ability to remember and adhere to instructions. Examples of the Cooking environment are presented in figures [11,](#page-18-0) [12.](#page-18-1)

RL comparison benchmark. We tested our architecture

on a variation of the Cooking test from [\[Adhikari](#page-7-8) *et al.*, 2021] to compare it with RL baselines. These tasks have 4 levels of difficulty, however, they are significantly simpler than our main tasks, having fewer locations, ingredients, and required actions.

- Level 1: 1 ingredient, 1 room, cutting.
- Level 2: 1 ingredient, 1 room, cutting + cooking.
- Level 3: 1 ingredient, 9 rooms, no processing.
- Level 4: 3 ingredients, 6 rooms, cutting + cooking.

We tested or agent and raw GPT-4 with full history on 3 randomly generated environments for each task difficulty. We slightly adapted the task for the LLM models. We gave the instruction to grill, roast or fry the ingredient using appropriate kitchen tools such as BBQ, oven and stove in the first observation of the game. RL agent can learn this rules by interacting with the environment, however, this is not a commonsense knowledge and without this instruction the game becomes unbeatable for LLM-agents and human players. While this adaptation should not impact the difficulty level, it's important to note that the environments for comparison between LLM and RL models were not 100% identical.

## <span id="page-13-1"></span>G Additional graphics and tables

This section presents the step-by-step dynamics of performance of different agents and human players (figure[.14\)](#page-20-0) . Additionally, this section includes a table summarizing the results of all experiments across three versions of the Treasure Hunt (Medium, Hard, Hardest), three versions of the Cooking (Medium, Hard, Hardest), and the Cleaning (table [4\)](#page-14-1).

<span id="page-14-0"></span>![](_page_14_Figure_0.jpeg)
<!-- Image Description: This flowchart diagrams a puzzle or game. Rectangles represent rooms, each containing a differently colored locked locker. Lines connect rooms, illustrating the sequence to find keys. Each locker contains either a key to another locker, or, in Room A, the final treasure. The chart's purpose is to visually represent the solution's steps, showing the logic of unlocking the lockers in order to obtain the treasure. -->

Figure 7: Treasure Hunt environment

<span id="page-14-1"></span>

|                          | Treasure<br>Hunt | Treasure<br>Hunt<br>Hard | Treasure<br>Hunt<br>Hardest | Cooking | Cooking<br>Hard | Cooking<br>Hardest | Cleaning |
|--------------------------|------------------|--------------------------|-----------------------------|---------|-----------------|--------------------|----------|
| Full History             | 0.47             | -                        | -                           | 0.18    | -               | -                  | 0.05     |
| Summary                  | 0.33             | 0.17                     | -                           | 0.52    | 0.21            | -                  | 0.35     |
| RAG                      | 0.33             | 0.17                     | -                           | 0.36    | 0.17            | -                  | 0.39     |
| Reflexion                | 0.93             | -                        | -                           | 1.0     | -               | -                  | 0.27     |
| Simulacra                | 0.4              | -                        | -                           | 0.3     | -               | -                  | 0.7      |
| AriGraph                 | 1.0              | 1.0                      | 1.0                         | 1.0     | 1.0             | 0.65               | 0.79     |
| AriGraph w/o exploration | 0.87             | -                        | -                           | 0.87    | -               | -                  | 0.76     |
| AriGraph w/o episodic    | 1.0              | 0.67                     | -                           | 0.64    | 0.45            | -                  | 0.92     |
| AriGraph LLaMA-3-70B     | 0.47             | -                        | -                           | 0.67    | -               | -                  | 0.5      |
| Human Top-3              | 1.0              | -                        | -                           | 1.0     | -               | -                  | 1.0      |
| Human All                | 0.96             | -                        | -                           | 0.32    | -               | -                  | 0.59     |

Table 4: All normalised scores across all tasks in TextWorld environment. Based on the results, it is evident that the agent with AriGraph significantly outperforms all baselines and scales well to larger and more complex environments. An important outcome is that our agent demonstrated near-human performance in text-based games, which has not been previously achieved using LLM.

<span id="page-15-0"></span>![](_page_15_Figure_0.jpeg)
<!-- Image Description: This diagram depicts a flowchart illustrating a series of interconnected rooms, each containing a locked locker and potentially a key or note. Lines connect rooms indicating the key's location relative to the locked locker. The chart's purpose is to visually represent a puzzle or game scenario requiring players to find keys within specific rooms to unlock subsequent lockers, ultimately leading to the treasure in Room A. Each room box displays the locker's color, lock status, and any contained items (keys or notes). -->

![](_page_15_Figure_1.jpeg)
<!-- Image Description: Figure 8 is a textual caption titled "Treasure Hunt hard environment." It lacks any diagrams, charts, graphs, equations, or illustrations. The caption likely precedes a description or discussion of a challenging simulated environment used in the paper's methodology, possibly related to a "Treasure Hunt" algorithm or problem. -->

<span id="page-16-0"></span>![](_page_16_Figure_0.jpeg)
<!-- Image Description: The image is a flowchart illustrating the relationships between rooms, lockers, keys, and objects in a game or puzzle. Each box represents a room containing locked lockers and items on tables. Lines connect rooms indicating item transfers or key usage. The flowchart visually depicts the interconnectedness of the puzzle's elements to solve it. The purpose is to provide a comprehensive overview of the game's structure and logic. -->

Figure 9: Treasure Hunt hardest environment

<span id="page-17-0"></span>![](_page_17_Figure_0.jpeg)
<!-- Image Description: This image is a diagram depicting the objects located in various rooms of a house. It uses a relational structure, showing how items are associated with specific rooms (Bathroom, Kitchen, Kids Room, etc.). Each room is represented by a box containing a list of objects, visually linked to other rooms through connecting lines. The diagram likely serves to illustrate data organization or spatial relationships within a home environment for the paper's research. -->

Figure 10: Cleaning environment

<span id="page-18-0"></span>![](_page_18_Figure_0.jpeg)
<!-- Image Description: This image is a diagram illustrating a house's spatial layout and object locations. It uses a hierarchical structure, showing rooms (kitchen, living room, bedroom, bathroom, etc.) connected by corridors. Each room contains a list of objects (e.g., furniture, food). The diagram also includes outdoor areas (garden, backyard, shed) and their contents, with connections representing doors. The purpose is likely to visualize the spatial relationships and object locations within a specific environment for a research purpose. -->

![](_page_18_Figure_1.jpeg)
<!-- Image Description: Figure 11 is a caption, not an image containing a diagram, chart, graph, equation, or technical illustration. It simply labels a missing figure in the academic paper as depicting a "Cooking environment." The figure itself is absent from the provided image. -->

<span id="page-18-1"></span>![](_page_18_Figure_2.jpeg)
<!-- Image Description: This image is an entity-relationship diagram depicting a house and its surroundings, including a garden, backyard, shed, and supermarket. Rectangles represent entities (e.g., "kitchen," "garden"), containing attributes (e.g., "Lettuce," "Patio table"). Lines connect entities to show relationships, illustrating the location of items and their connections to different rooms and spaces. The diagram likely serves to illustrate a spatial or data model within the paper. -->

Figure 12: Cooking hard environment

<span id="page-19-0"></span>![](_page_19_Figure_0.jpeg)
<!-- Image Description: The image displays a game interface, likely from an academic paper on AI or game development. It shows a top-down view of a game map with a player character, enemies (kobold zombies), and items. Text boxes detail agent thoughts (AI decision-making process), message history, and character stats (level, health, inventory). The map's text-based representation is also shown, possibly for analysis purposes. The image illustrates a specific moment in the game, showcasing the AI's actions and reasoning. -->

Figure 13: Example of NetHack level

<span id="page-20-0"></span>![](_page_20_Figure_0.jpeg)
<!-- Image Description: The image presents six learning curves comparing the performance of different agents (Ariadne, with and without experience/episodic memory, Human Top-3, Human All, Fullhist, RAG) across three tasks (Treasure Hunt, Cleaning, Cooking, each with easy and hard versions). Each graph plots normalized score against step number, showing the cumulative performance over time. Shaded areas represent confidence intervals. The curves illustrate how the agents' performance improves as they complete more steps in each task, allowing for a comparative analysis of their learning capabilities. -->

Figure 14: Performance Dynamics in Test Games. In the Treasure Hunt, the Ariadne agent delivers performance comparable to top players; in the Cleaning task, it falls slightly behind, but in the Cooking, it surpasses top human players in speed. The hard variants of the tasks demonstrate that the quality of Ariadne's performance does not decrease with increasing task difficulty, and also highlight the importance of episodic memory.
