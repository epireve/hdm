---
cite_key: "in2021"
title: "TIMEBENCH: A Comprehensive Evaluation of Temporal Reasoning Abilities in Large Language Models"
authors: "Zheng Chu, Jingchang Chen, Qianglong Chen, Weijiang Yu, Haotian Wang, Ming Liu, Bing Qin"
year: 2021
doi: "10.18653/V1/2023.EMNLP-MAIN.298)"
date_processed: "2025-07-02"
phase2_processed: true
original_folder: "temporal_cognitive_arxiv_2311.17667_TimeBench_A_Comprehensive_Evaluation_of_Temporal_Reasoning_Abilities_in_Large_La"
images_total: 8
images_kept: 8
images_removed: 0
---

# TIMEBENCH: A Comprehensive Evaluation of Temporal Reasoning Abilities in Large Language Models

Zheng Chu<sup>1</sup> , Jingchang Chen<sup>1</sup> , Qianglong Chen<sup>2</sup> , Weijiang Yu<sup>3</sup> , Haotian Wang<sup>1</sup> , Ming Liu<sup>1</sup>,4\*, Bing Qin<sup>1</sup>,<sup>4</sup> <sup>1</sup>Harbin Institute of Technology, Harbin, China <sup>2</sup>Zhejiang University <sup>3</sup>Sun Yat-sen University <sup>4</sup>Peng Cheng Laboratory {zchu,jcchen,mliu,qinb}@ir.hit.edu.cn {chenqianglong.ai, wanght1998, weijiangyu8}@gmail.com

# Abstract

Grasping the concept of time is a fundamental facet of human cognition, indispensable for truly comprehending the intricacies of the world. Previous studies typically focus on specific aspects of time, lacking a comprehensive temporal reasoning benchmark. To address this, we propose TIMEBENCH, a comprehensive hierarchical temporal reasoning benchmark that covers a broad spectrum of temporal reasoning phenomena. TIMEBENCH provides a thorough evaluation for investigating the temporal reasoning capabilities of large language models. We conduct extensive experiments on GPT-4, LLaMA2, and other popular LLMs under various settings. Our experimental results indicate a significant performance gap between the state-of-the-art LLMs and humans, highlighting that there is still a considerable distance to cover in temporal reasoning. Besides, LLMs exhibit capability discrepancies across different reasoning categories. Furthermore, we thoroughly analyze the impact of multiple aspects on temporal reasoning and emphasize the associated challenges. We aspire for TIMEBENCH to serve as a comprehensive benchmark, fostering research in temporal reasoning[1](#page-0-0) .

# 1 Introduction

Time flies over us, but leaves its shadow behind. Understanding time is a crucial part of human comprehension of the world. Envision the blossoming of flowers, and you'll associate it with the arrival of spring. The ponder within it encompasses the intricate interplay of world knowledge, causality, and event temporal relationships. Temporal reasoning, in contrast to reasoning of a singular nature, comes with inherent complexity, encompassing implicit arithmetic, logical implications, and world knowledge. It is a form of integrated reasoning built upon

<span id="page-0-1"></span>![](_page_0_Figure_8.jpeg)
<!-- Image Description: The image displays a radar chart comparing the performance of several large language models (LLMs) – GPT-4, LLaMA 2 (70B and 13B parameter versions), and Mistral – against human performance across eight reasoning tasks. Each axis represents a different task (e.g., TimeXNLI, Arith, DurationQA), and the radial distance from the center indicates the model's score on that task. The chart allows for a visual comparison of the LLMs' strengths and weaknesses across various reasoning domains relative to human performance. -->

Figure 1: A brief overview of human and LLMs' performance on TimeBench. Human scores are annotated.

foundational reasoning like mathematical and logical reasoning [\(Cobbe et al.,](#page-10-0) [2021;](#page-10-0) [Mishra et al.,](#page-11-0) [2022;](#page-11-0) [Yu et al.,](#page-12-0) [2020\)](#page-12-0). Recently, large language models (LLMs) have demonstrated remarkable performance in complex reasoning [\(Hendrycks et al.,](#page-10-1) [2021;](#page-10-1) [Srivastava et al.,](#page-11-1) [2022;](#page-11-1) [Brown et al.,](#page-9-0) [2020;](#page-9-0) [Chowdhery et al.,](#page-9-1) [2023;](#page-9-1) [OpenAI,](#page-11-2) [2023;](#page-11-2) [Touvron](#page-11-3) [et al.,](#page-11-3) [2023\)](#page-11-3), but their performance in temporal reasoning has not yet been extensively explored.

Recent research for temporal reasoning typically focuses only on a few aspects, such as temporal commonsense or temporal question answering [\(Zhou et al.,](#page-13-0) [2019;](#page-13-0) [Chen et al.,](#page-9-2) [2021;](#page-9-2) [Dhingra](#page-10-2) [et al.,](#page-10-2) [2022;](#page-10-2) [Wang and Zhao,](#page-12-1) [2023\)](#page-12-1). Due to the inherent complexity of temporal reasoning, it is challenging to accurately measure models' temporal reasoning capabilities based on limited aspects.

To address this issue, we propose TIMEBENCH, a comprehensive and hierarchical temporal reasoning benchmark. Specifically, drawing inspiration from the human cognitive process of transitioning from abstraction and concreteness to integration [\(Barsalou et al.,](#page-9-3) [2018\)](#page-9-3), we categorize temporal reasoning into three levels: symbolic temporal reasoning, commonsense temporal reasoning, and event temporal reasoning. These levels respectively represent understanding abstract time expression,

<sup>\*</sup> Corresponding Author.

<span id="page-0-0"></span><sup>1</sup> Data is available at: [GitHub](https://github.com/zchuz/TimeBench)

grasping concrete world knowledge, and integrating and applying this knowledge in real-world scenarios. TIMEBENCH comprises 10 tasks with 16 sub-tasks, covering a broad spectrum of temporal reasoning phenomena. Besides, prior work typically features only a single task form, too simplistic to capture the model's performance. In contrast, we incorporate four distinct task forms, offering a more realistic simulation of challenges.

To quantify the temporal reasoning capabilities of contemporary LLMs, we extensively assess widely-used LLMs, including proprietary models such as ChatGPT [\(Ouyang et al.,](#page-11-4) [2022\)](#page-11-4) and GPT-4 [\(OpenAI,](#page-11-2) [2023\)](#page-11-2), as well as open-source like LLaMA2 [\(Touvron et al.,](#page-11-3) [2023\)](#page-11-3), Vicuna-1.5 [\(Chi](#page-9-4)[ang et al.,](#page-9-4) [2023\)](#page-9-4), Mistral [\(Jiang et al.,](#page-10-3) [2023\)](#page-10-3), Baichuan2 [\(Yang et al.,](#page-12-2) [2023a\)](#page-12-2), ChatGLM3 [\(Zeng](#page-12-3) [et al.,](#page-12-3) [2023\)](#page-12-3) and FLAN-T5 [\(Chung et al.,](#page-10-4) [2022\)](#page-10-4). We conduct experiments under zero-shot and fewshot settings, combining commonly used reasoning techniques, chain-of-thought prompting [\(Kojima](#page-10-5) [et al.,](#page-10-5) [2022;](#page-10-5) [Wei et al.,](#page-12-4) [2022\)](#page-12-4). The experimental results suggest that GPT-4 outperforms other models, showcasing strong temporal reasoning capabilities, as shown in Figure [1.](#page-0-1) Nevertheless, there is still a considerable gap between the strongest models and humans. On the contrary, open-source models show inferior performance in temporal reasoning, attributed to shortcomings in abstract time understanding, temporal relations modeling, and a lack of temporal commonsense. In addition, we also observe that chain-of-thought prompting does not yield a consistent improvement in performance. These findings indicate that there is still significant room for improvement in models' temporal reasoning capabilities. Moreover, we have conducted a thorough analysis of the deficiencies and obstacles faced by models in temporal reasoning.

We aspire for temporal reasoning to garner increased attention within the research community. Our contributions can be summarized as follows:

- We introduce TIMEBENCH, a comprehensive and hierarchical benchmark to quantify the temporal reasoning abilities of LLMs.
- We conduct extensive experiments with several LLMs, revealing a significant gap between even SOTA LLM and humans, indicating substantial research opportunities in this field.
- By conducting a thorough analysis, we reveal the dilemmas that LLMs face in temporal reasoning and identify potential solutions.

# 2 TIMEBENCH Benchmark

## 1 Benchmark Design Principal

TIMEBENCH focuses on a comprehensive evaluation of the temporal reasoning capabilities of large language models in challenging and complex scenarios. To achieve this goal, we summarize the difficulties and challenges faced in temporal reasoning, categorize them into three levels, and integrate diverse task formats to better align with the intricate nature of temporal reasoning.

Just as the human cognitive process unfolds from foundational cognition and conceptual understanding to practical reasoning, we delineate temporal reasoning into three hierarchical levels. Specifically, TIMEBENCH categorizes temporal reasoning into symbolic, commonsense and event temporal reasoning, covering 10 datasets with a total of 16 subtasks. (1) Symbolic Temporal Reasoning focuses on the comprehension of fundamental abstract temporal expressions. (2) Temporal Commonsense Reasoning emphasizes the mastery of temporal principles, concepts and world knowledge. (3) Event Temporal Reasoning concentrates on modeling the temporal relationships between events and times within authentic scenarios.

### 2 Difficulties and Challenges

We delineate the essential competencies and the challenges that arise from a human cognitive standpoint in the realm of temporal reasoning, and language models confront similar challenges. We present the dataset statistics, task formats, and the associated challenges in Table [7.](#page-16-0)

Time Expression Understanding Time expressions (TimeX) denote words or phrases that convey information about time and represent the simplest and most basic units of expressing time, such as *in April 2000*, *after 2008*. Grasping time expressions is the most foundational step in understanding temporal elements within the textual modality.

Temporal Commonsense assesses the understanding of temporal world knowledge, including event order, event duration, typical time, event frequency and stationary, which is crucial for language models to comprehend daily scenarios.

Event-Time Relations assesses the model's grounding capability to establish temporal relationships between events and their temporal context, thereby enabling models to grasp the progression

#### <span id="page-2-0"></span>DATE ARITH

Q: *What is the time 2 year and 4 month before Mar, 1755*A: Nov, 1752

# TIMEX NLI

Premise:*On 28th May 1967, I graduated.*Hypothesis:*Before 23rd October 1920, I graduated.*A: Contradiction

Table 1: Examples of symbolic temporal reasoning

## <span id="page-2-1"></span>MCTACO

C:*Ransome looks after her as well as for young Fern Simon , who has declared her love for him.*Q:*How often do Ransome and Fern talk?*O: each century, once a day, once a century, every night

### TIMEDIAL

Dialog:*... Person1: Do you go to work by train every day Person2: Yes . I commute <MASK> a week by train...*O: five days, 25 days, a minute, six days

#### SITUATEDGEN

Keywords:*axis, one day, one month, Earth, Moon*A: Earth rotates on its axis once in one day. It takes one month for the Moon to rotate on its axis.

Table 2: Examples of commonsense temporal reasoning.

and transformations of events as they dynamically evolve through time.

Event-Event Relations not only involve eventtime grounding but also introduce multi-hop relative connections between events. Models with this capability can better handle temporal reasoning in complex scenarios involving multiple events.

Implicit Temporal Reasoning involves going beyond the surface of texts, engaging in deeper reasoning such as drawing upon temporal commonsense, identifying implicit temporal factors and discerning hidden temporal relationships among events. Implicit temporal reasoning is pivotal in complex real-world scenarios where events and time are intricately interwoven.

# 3 Symbolic Temporal Reasoning

To evaluate the language model's comprehension of abstract time expressions, we utilize two symbolic reasoning tasks stripped of semantic content: date arithmetic and time expression inference. Table [1](#page-2-0) shows examples of symbolic temporal reasoning.

## <span id="page-2-2"></span>TIMEQA

C:*... He worked in Utrecht for the firm of P Smits & de Wolf from 1864 to 1867 and then returned to ...*Q:*Where did Ludwig Mond work between Mar 1866 and Sep 1866?*A: Utrecht

### MENATQA

C:*... After the French evacuated Egypt in 1801, Hurshid Pasha was named governor of Egypt in 1804. Muhammad Ali had himself named governor of Egypt in May 1805 ...*Q:*Which position did Hurshid Pasha hold from 1804 to 1806, if Hurshid Pasha tepped down as the governor of Egypt in 1808?*A: governor of Egypt TEMPREASON

C:*... Peter Corke works for Queensland University of Technology from Jan, 2010 to Dec, 2022. Peter Corke works for Commonwealth Scientific from Jan, 1984 to Jan, 2009. ...*Q:*Which employer did Peter Corke work for before Queensland University of Technology?*A: Commonwealth Scientific

Table 3: Examples of event temporal reasoning.

Date Arithmetic [\(Tan et al.,](#page-11-5) [2023\)](#page-11-5) assesses the model's grasp of abstract date calculation. When provided with a date, the model needs to accurately calculate the date a certain amount of time before or after the given date. The smallest unit is one day.

TimeX NLI [\(Thukral et al.,](#page-11-6) [2021\)](#page-11-6) focuses on the logical entailment relationships among abstract TimeX, including three aspects: order (s1), duration (s2), and duration with unit conversion (s3).

### 4 Commonsense Temporal Reasoning

We measure the model's mastery of temporal commonsense and world knowledge, along with its capacity for reasoning based on these insights. Table [2](#page-2-1) presents examples of temporal commonsense reasoning in QA and generation forms.

MCTACO [\(Zhou et al.,](#page-13-0) [2019\)](#page-13-0) evaluates diverse commonsense knowledge from different aspects of events, including duration, frequency, order, stationary and typical event time.

DurationQA [\(Virgo et al.,](#page-12-5) [2022\)](#page-12-5) focuses specifically on temporal commonsense reasoning in the spectrum of event duration.

TimeDial [\(Qin et al.,](#page-11-7) [2021\)](#page-11-7) considers temporal commonsense reasoning in dialogue scenarios and involves various aspects of commonsense associated with duration, order, and world knowledge.

SituatedGen [\(Zhang and Wan,](#page-12-6) [2023\)](#page-12-6) considers generative commonsense reasoning in a constrained text generation scenario. Given a set of contrasting keywords, the model needs to choose appropriate keywords for each sentence and generate a pair of contrasting sentences that satisfy temporal commonsense.

# 5 Event Temporal Reasoning

Event temporal reasoning assesses the model's understanding of relationships between events and time in real-world scenarios, as well as its ability to reasoning under certain temporal or event constraints. Examples are shown in Table [3.](#page-2-2)

TimeQA [\(Chen et al.,](#page-9-2) [2021\)](#page-9-2) requires the model to answer time-sensitive questions based on context containing numerous time-involved facts. It is categorized into explicit reasoning and implicit reasoning based on time indicators (before, in, etc.).

MenatQA [\(Wei et al.,](#page-12-7) [2023\)](#page-12-7) introduces timesensitive factors to elicit implicit temporal reasoning, including time scope change, disruption of facts, and counterfactual questions, which provides a more in-depth assessment of implicit reasoning ability on event-time relations.

TempReason [\(Tan et al.,](#page-11-5) [2023\)](#page-11-5) removes irrelevant context and focuses on implicit temporal reasoning within structured facts, investigating the model's capability boundaries. It involves eventtime reasoning and event-event reasoning.

TRACIE [\(Zhou et al.,](#page-13-1) [2021\)](#page-13-1) evaluates the model's comprehension of temporal order between implicit events. The model needs to identify events implied in the context and then determine their chronological order.

## 6 Task Formats and Evaluation Metrics

TIMEBENCH is a multispectral benchmark encompassing four task types: free-form reading comprehension, natural language inference, constrained text generation, and multi-select questions. For detailed task types and their corresponding evaluation metrics, please refer to Appendix [A.3](#page-14-0) and [A.4.](#page-14-1)

# 3 Methodology

We perform evaluations using the prompt-based approach, including standard prompting and chainof-thought prompting. Experiments are conducted under both zero-shot and few-shot settings.

Standard Prompting We formulate specific instructions for each task. In the zero-shot setting, models follow the instructions to answer questions. In the few-shot setting, models are provided with several question-answer pairs as demonstrations and emulate those instances to answer questions.

$$
prompt_{zs}^{sp} = \{INST\} \{Q\}
$$
 (1)

$$
prompt_{fs}^{sp} = \{INST\} \{Q_1\} \{A_1\}..\{Q\} \quad (2)
$$

Chain-of-Thought Prompting The instructions of CoT are the same as standard prompting. In the zero-shot setting, following Zeroshot CoT [\(Ko](#page-10-5)[jima et al.,](#page-10-5) [2022\)](#page-10-5), we add a reasoning trigger*Let's think step by step*after questions to perform chainof-thought reasoning. In the few-shot setting, we manually annotate CoT demonstrations for each task to guide the step-by-step reasoning. Prompts can be found in Appendix [B.3.](#page-15-0)

$$
prompt_{zs}^{cot} = \{INST\} \{Q\} \{TRIG\}
$$
\n
$$
prompt_{fs}^{cot} = \{INST\} \{Q_1\} \{R_1\} \{A_1\} ...\{Q\} (4)
$$

# 4 Experimental Setup

## 1 Models

We evaluate several popular LLMs, including both open-source and proprietary models, with parameter sizes ranging from 6B to 70B.[2](#page-3-0) The complete list of models can be found in Appendix [B.1.](#page-14-2)

# 2 Implementation Details

We access proprietary models through Azure API 0613 version. For open-source models, we deploy them locally through FastAPI. We set the temperature to 0.0 for greedy decoding in all experiments. To improve answer extraction accuracy, we prompt models with trigger*Therefore, the answer is*before model outputs to deduce final answers.

# 5 Experimental Results

# 1 Few-shot Results

Table [4](#page-4-0) presents the experimental results under few-shot settings. GPT-4 achieves the best performance across three categories, while LLaMA270b and GPT-3.5 rank in the second tier. However, there remains a substantial gap of 19.4% between the most powerful LLM and humans.

In symbolic temporal reasoning tasks, GPT-4 demonstrates exceptional performance. However,

<span id="page-3-0"></span><sup>2</sup> Since OpenAI has never disclosed the scale of ChatGPT series, 6B to 70B here refers to ChatGLM36B to LLaMA270B.

<span id="page-4-0"></span>

|                              |    |                | Symbolic                                       |                                                        |              | Commonsense |                        |                                          |  | Event Temporal                                                           |    |             |                              |              | Overall      |                        |              |
|------------------------------|----|----------------|------------------------------------------------|--------------------------------------------------------|--------------|-------------|------------------------|------------------------------------------|--|--------------------------------------------------------------------------|----|-------------|------------------------------|--------------|--------------|------------------------|--------------|
| Method                       | s1 | TimeXNLI<br>s2 | s3                                             |                                                        |              |             |                        | Arith DQA McT. TiD. SitGen TimeQA        |  | MenatQA<br>Exp. Imp. Sco. Ord. Ctf.                                      | L2 | TempR<br>L3 | TRACIE Sym. Comm. Event Avg. |              |              |                        |              |
| Human                        |    |                |                                                | 98.0 96.0 92.0 100.0 80.8                              |              |             | 87.1 97.8              | 100.0 93.3 91.1 85.6 87.3 79.9 97.1 95.3 |  |                                                                          |    |             | 82.5                         | 96.5         | 91.4         | 89.0                   | 91.5         |
| GPT-4<br>+ FS CoT            |    |                |                                                | 85.3 73.3 53.3 100.0 64.8<br>92.0 84.0 64.0 100.0 55.1 |              |             | 88.3 94.6<br>72.3 93.4 | 88.6<br>-                                |  | 73.7 51.0 72.4 54.8 28.7 92.4 95.9<br>66.9 52.8 65.3 52.6 25.9 96.9 94.6 |    |             | 62.8<br>66.4                 | 78.0<br>85.0 | 84.1<br>73.6 | 66.5<br>65.2           | 73.7<br>72.1 |
| GPT-3.5<br>+ FS CoT          |    |                |                                                | 52.0 68.4 31.6 63.6<br>51.6 71.8 36.6 84.4             | 67.7<br>41.2 |             | 71.2 76.4<br>38.1 71.1 | 79.1<br>-                                |  | 66.1 48.4 43.2 51.6 17.9 84.7 78.0<br>68.0 47.0 42.5 41.7 37.8 89.9 76.6 |    |             | 55.0<br>50.2                 | 53.9<br>61.1 | 73.6<br>50.1 | 55.6 59.7<br>56.7 56.6 |              |
| LLaMA2†<br>70b<br>+ FS CoT   |    |                | 55.0 61.0 37.0 82.0<br>52.0 73.0 39.0 79.5     |                                                        | 67.4<br>62.3 |             | 85.3 82.7<br>79.1 61.1 | 74.9<br>-                                |  | 66.7 48.3 61.4 42.5 33.8 85.2 85.4<br>64.3 43.0 57.7 45.2 53.1 87.5 81.6 |    |             | 61.0<br>67.0                 | 58.8<br>60.9 | 77.6<br>67.5 | 60.5 64.4<br>62.4 63.0 |              |
| LLaMA2†<br>13b<br>+ FS CoT   |    |                | 50.0 54.0 30.0 29.5<br>40.0 61.0 37.0 52.0     |                                                        | 53.3<br>59.3 |             | 66.0 55.6<br>68.8 40.8 | 64.8<br>-                                |  | 59.3 48.6 49.6 43.4 37.5 78.7 62.7<br>59.4 49.1 58.4 43.8 44.1 78.0 68.2 |    |             | 58.0<br>58.0                 | 40.9<br>47.5 | 59.9<br>56.3 | 54.7<br>57.4           | 52.6<br>54.5 |
| LLaMA2†<br>7b<br>+ FS CoT    |    |                | 26.0 50.0 30.0 20.0<br>37.0 52.0 36.0 25.5     |                                                        | 54.5<br>56.9 |             | 59.6 45.2<br>67.0 41.9 | 62.4<br>-                                |  | 54.4 45.3 49.8 41.9 35.8 64.0 53.3<br>45.6 36.1 50.9 38.0 57.3 59.7 57.7 |    |             | 49.0<br>50.0                 | 31.5<br>37.6 | 55.4<br>55.3 | 49.2<br>49.4           | 46.3<br>47.4 |
| Baichuan2†<br>+ FS CoT       |    |                | 13b 38.0 48.0 33.0 42.5<br>50.0 56.0 34.0 47.0 |                                                        | 54.8<br>62.0 |             | 73.0 45.7<br>69.3 43.8 | 64.9<br>-                                |  | 59.4 54.2 52.7 38.0 21.4 77.3 63.5<br>58.2 49.6 49.8 40.1 45.6 81.3 65.6 |    |             | 54.0<br>60.0                 | 40.4<br>46.8 | 59.6<br>58.4 | 52.6<br>56.3           | 51.3<br>54.2 |
| Baichuan2†<br>7b<br>+ FS CoT |    |                | 27.0 66.0 41.0 32.5<br>30.0 56.0 34.0 34.0     |                                                        | 59.8<br>57.0 |             | 69.4 34.3<br>69.5 44.5 | 59.8<br>-                                |  | 53.8 50.2 49.6 38.5 22.9 65.9 51.0<br>51.2 40.7 46.4 32.6 46.3 61.5 64.1 |    |             | 55.0<br>53.0                 | 41.6<br>38.5 | 55.8<br>57.0 | 48.4<br>49.5           | 48.5<br>48.1 |
| Mistral†<br>7b<br>+ FS CoT   |    |                | 48.0 53.0 38.0 41.0<br>57.0 63.0 35.0 54.0     |                                                        | 61.8<br>61.8 |             | 76.2 61.8<br>45.7 57.3 | 58.3<br>-                                |  | 55.9 45.3 49.4 47.8 45.5 76.7 74.8<br>60.4 46.2 57.2 47.9 33.2 65.9 67.9 |    |             | 53.0<br>57.0                 | 45.0<br>52.3 | 64.5<br>54.9 | 56.1<br>54.5           | 55.4<br>54.0 |
| ChatGLM3†<br>+ FS CoT        |    |                | 6b 48.0 70.0 32.0 35.0<br>47.0 68.0 32.0 46.0  |                                                        | 51.8<br>53.9 |             | 62.6 55.0<br>64.3 56.5 | 61.6<br>-                                |  | 57.2 26.3 35.4 41.5 22.5 76.4 55.9<br>52.5 24.5 35.0 40.2 22.5 79.4 60.3 |    |             | 58.0<br>54.0                 | 46.3<br>48.3 | 57.8<br>58.2 | 46.7<br>46.1           | 49.3<br>49.1 |

Table 4: Experimental results under few-shot settings (standard prompting by default). † denotes the base model without alignment. Global top-3 results are bold. Figure [8](#page-16-1) provides a horizontal comparison of the performance of all models. Full results in Appendix [B.2.](#page-15-1)

other models exhibit a significant decline in comparison to GPT-4. In commonsense temporal reasoning tasks, GPT4 lags behind humans by only 8.0%, indicating its powerful internal knowledge reservoir. With the model scale shrinking, its knowledge reservoir also decreases gradually, leading to a decline in performance. Notably, there is a significant gap of 25.2% between LLMs and humans in event temporal reasoning, which suggests that LLMs encounter major challenges in modeling intricate event-time relationships.

# 2 Zero-shot Results

Experimental results of alignment models under zero-shot settings are shown in Table [5.](#page-5-0) In zeroshot settings, GPT-4 and GPT-3.5 rank first and second, respectively, and they significantly outperform all open-source models by a large margin. It is noteworthy that open-source models exhibit a larger performance decline compared to proprietary models when transitioning from few-shot to zero-shot scenarios. GPT, Baichuan2 and LLaMA2 suffer drops of 5.6%, 14.6% and 27.2%, respectively. We attribute this performance decline to the quality of alignment. Restricted by their limited instruction-following capability, open-source models struggle to fully unleash their performance

<span id="page-4-1"></span>![](_page_4_Figure_5.jpeg)
<!-- Image Description: This bar chart displays performance comparison results across four categories (Symbolic, Commonsense, Event, Overall). Two systems, ZS and FS, are evaluated, each with and without a "CoT" (Chain of Thought) prompting method. The chart shows the percentage scores for each system and condition, revealing the impact of CoT prompting on performance in different reasoning tasks. Higher bars indicate better performance. -->

Figure 2: Performance gap with and without CoT prompting. The results are averaged from GPT-4, GPT-3.5, Baichuan2<sup>13</sup>b, LLaMA2<sup>70</sup><sup>b</sup> and Mistral<sup>7</sup>b.

solely through instructions. Therefore, few-shot prompting is a better approach for stimulating their temporal reasoning abilities.

# 3 Chain-of-Thought in Temporal Reasoning

Previous research has found that chain-of-thought prompting can enhance the model's reasoning ability [\(Wei et al.,](#page-12-4) [2022;](#page-12-4) [Kojima et al.,](#page-10-5) [2022\)](#page-10-5). We aim to explore the following questions:*Does CoT prompting bring consistent improvement in temporal reasoning?*Due to the diversity of temporal reasoning, the above question has not yet been definitively answered. To investigate this, we select several popular LLMs and analyze their performance affected by chain-of-thought prompting.

<span id="page-5-0"></span>

|                                           |    |                                  | Symbolic                                   |                           |              | Commonsense  |                        |                                          |  | Event Temporal                                                           |    |             |                              |              | Overall      |                        |              |
|-------------------------------------------|----|----------------------------------|--------------------------------------------|---------------------------|--------------|--------------|------------------------|------------------------------------------|--|--------------------------------------------------------------------------|----|-------------|------------------------------|--------------|--------------|------------------------|--------------|
| Method                                    | s1 | TimeXNLI<br>s2                   | s3                                         |                           |              |              |                        | Arith DQA McT. TiD. SitGen TimeQA        |  | MenatQA<br>Exp. Imp. Sco. Ord. Ctf.                                      | L2 | TempR<br>L3 | TRACIE Sym. Comm. Event Avg. |              |              |                        |              |
| Human                                     |    |                                  |                                            | 98.0 96.0 92.0 100.0 80.8 |              |              | 87.1 97.8              | 100.0 93.3 91.1 85.6 87.3 79.9 97.1 95.3 |  |                                                                          |    |             | 82.5                         | 96.5         | 91.4         | 89.0                   | 91.5         |
| GPT-4<br>+ CoT                            |    |                                  | 78.6 76.0 50.7 98.0<br>80.0 76.0 60.0 92.0 |                           | 59.2<br>58.1 |              | 80.0 91.1<br>82.6 89.3 | 59.3<br>-                                |  | 60.6 46.5 57.0 57.0 23.1 95.3 95.0<br>61.3 41.2 54.6 59.6 22.6 97.0 94.5 |    |             | 64.8<br>58.0                 | 75.8<br>77.0 | 72.4<br>76.7 | 62.4 68.3<br>61.1 68.5 |              |
| GPT-3.5<br>+ CoT                          |    |                                  | 45.4 67.6 31.2 97.0<br>33.6 64.8 33.6 71.0 |                           | 50.5<br>23.2 |              | 68.6 69.1<br>45.1 67.0 | 62.3<br>-                                |  | 70.8 35.4 40.9 43.9 22.9 81.2 73.8<br>64.4 35.1 39.7 42.9 26.3 57.6 68.1 |    |             | 57.4<br>52.0                 | 60.3<br>50.8 | 62.6<br>45.1 | 53.3<br>48.3           | 57.4<br>48.3 |
| LLaMA270b<br>+ CoT                        |    |                                  | 44.0 47.0 32.0 78.5<br>30.0 66.0 28.0 53.5 |                           | 59.2<br>57.3 |              | 68.9 57.0<br>67.1 58.6 | 25.0                                     |  | 40.8 40.6 18.9 16.6 12.0 63.5 54.5<br>31.4 19.5 12.2 12.7 20.8 37.5 40.5 |    |             | 48.0<br>51.0                 | 50.4<br>44.4 | 52.5<br>61.0 | 36.8<br>28.2           | 44.1<br>39.1 |
| LLaMA213b<br>+ CoT                        |    | 36.0 50.0 38.0                   | 30.0 49.0 34.0 22.5                        | 6.0                       | 38.5<br>39.2 |              | 40.6 35.4<br>51.7 36.9 | 57.9<br>-                                |  | 61.9 30.5 46.1 36.1 26.9 53.1 69.4<br>58.7 38.9 40.9 32.5 33.6 58.0 68.4 |    |             | 49.0<br>47.0                 | 33.9<br>32.5 | 43.1<br>42.6 | 46.6<br>47.3           | 42.6<br>42.4 |
| LLaMA27b<br>+ CoT                         |    | 44.0 50.0 33.0                   | 39.0 53.0 30.0 13.0                        | 5.0                       | 39.3<br>35.0 | 41.0<br>40.0 | 6.3<br>1.7             | 24.5<br>-                                |  | 49.0 29.0 26.8 21.1 16.0 63.9 47.9<br>49.9 31.6 31.4 24.5 17.8 56.9 48.1 |    |             | 49.0<br>46.0                 | 33.8<br>33.0 | 27.8<br>25.6 | 37.8<br>38.3           | 34.3<br>34.3 |
| Baichuan213b 41.0 61.0 37.0 12.5<br>+ CoT |    |                                  | 40.0 57.0 31.0 10.0                        |                           | 52.0<br>44.6 |              | 63.4 57.7<br>61.9 58.1 | 52.2<br>-                                |  | 55.4 34.6 48.8 44.3 39.5 57.4 61.4<br>41.5 40.9 52.0 38.5 43.2 62.8 64.3 |    |             | 49.0<br>55.0                 | 37.9<br>34.5 | 56.3<br>54.9 | 48.8<br>49.8           | 48.0<br>46.7 |
| Baichuan27b<br>+ CoT                      |    | 35.0 50.0 37.0<br>38.0 43.0 32.0 |                                            | 4.5<br>1.0                | 47.9<br>37.9 |              | 55.3 54.3<br>58.0 44.2 | 42.0<br>-                                |  | 41.5 34.7 35.2 31.2 20.4 43.4 47.7<br>53.5 38.8 39.9 33.2 29.3 41.2 47.2 |    |             | 55.0<br>54.0                 | 31.6<br>28.5 | 49.9<br>46.7 | 38.6<br>42.1           | 39.7<br>39.4 |
| Vicuna1.513b 35.0 50.0 36.0 15.0<br>+ CoT |    | 42.0 51.0 37.0                   |                                            | 3.0                       | 39.2<br>29.8 |              | 59.1 34.2<br>50.0 33.7 | 51.8<br>-                                |  | 60.4 37.0 46.8 37.4 23.2 42.1 43.6<br>56.9 36.4 38.2 37.7 20.4 49.0 49.1 |    |             | 46.0<br>51.0                 | 34.0<br>33.3 | 46.1<br>37.8 | 42.1<br>42.3           | 41.1<br>39.0 |
| Vicuna1.57b<br>+ CoT                      |    | 37.0 58.0 43.0<br>36.0 50.0 36.0 |                                            | 5.0<br>1.5                | 40.4<br>39.4 |              | 52.5 32.0<br>49.2 36.2 | 47.8<br>-                                |  | 47.1 18.5 35.7 25.7 17.3 33.0 46.8<br>40.9 24.6 26.2 28.5 25.0 27.7 40.3 |    |             | 54.0<br>54.0                 | 35.8<br>30.9 | 43.2<br>41.6 | 34.8<br>33.4           | 37.1<br>34.4 |
| FLANT511b<br>+ CoT                        |    | 53.0 63.0 43.0                   | 56.0 66.0 45.0                             | 0.0<br>0.0                | 52.0<br>49.7 |              | 65.0 47.7<br>63.4 42.7 | 49.5<br>-                                |  | 61.7 26.8 33.6 52.2 21.8 87.9 83.9<br>64.4 28.2 41.6 50.2 30.6 79.5 68.9 |    |             | 64.0<br>55.0                 | 39.8<br>41.8 | 53.6<br>51.9 | 54.0<br>52.3           | 50.3<br>49.4 |
| Mistral7b<br>+ CoT                        |    |                                  | 47.0 50.0 43.0 26.5<br>38.0 56.0 35.0 16.5 |                           | 49.8<br>36.6 |              | 58.8 23.2<br>49.3 19.3 | 58.3<br>-                                |  | 28.2 21.4 24.3 22.3 21.7 39.6 31.6<br>31.3 22.4 21.1 24.9 25.6 34.0 31.2 |    |             | 51.0<br>61.0                 | 41.6<br>36.4 | 47.5<br>35.1 | 30.0<br>31.4           | 37.3<br>33.5 |
| ChatGLM36b 38.0 50.0 34.0<br>+ CoT        |    | 27.0 49.0 37.0                   |                                            | 2.0<br>0.0                | 34.1<br>24.8 |              | 43.6 56.7<br>37.1 44.8 | 38.9<br>-                                |  | 41.2 31.7 33.8 26.0 32.2 57.0 54.0<br>41.7 25.4 34.6 28.1 41.2 44.5 52.0 |    |             | 50.0<br>48.0                 | 31.0<br>28.3 | 43.3<br>35.6 | 40.7<br>39.4           | 39.0<br>35.7 |

Table 5: Experimental results under zero-shot settings (standart prompting by default). All models are alignment models (-chat or -instruct). Global top-3 results are bold.

Chain-of-thought reasoning is not consistently effective. As illustrated in Figure [2,](#page-4-1) introducing zero-shot CoT prompting results in consistent declines, with an overall decrease of 7.4%. In the fewshot scenario, CoT prompting also fails to yield consistent improvements, varying depending on the task. There is a 10.8% improvement in symbolic reasoning, while a significant decline of 15.2% in commonsense reasoning. In event temporal reasoning, there is a slight improvement of 1.3%. Next, we will conduct a more detailed analysis of the impact of CoT on specific tasks.

Impact of CoT prompting across tasks. In order to explore the impact of CoT on various tasks thoroughly, we delve into the performance changes of each model across specific tasks within each category, as illustrated in Figure [3.](#page-6-0) In the zeroshot setting, open-source models achieve a slight improvement in event temporal reasoning with chain-of-thought prompting, while in other cases, they face performance degradation. While in the few-shot setting, almost all models exhibit significant improvement in symbolic temporal reasoning, with a concurrent prevalent decline in commonsense temporal reasoning. We attribute this to the knowledge sensitivity inherent in commonsense reasoning, where step-by-step reasoning cannot compensate for the lack of knowledge. In event temporal reasoning, improvements mainly stem from datasets involving implicit multi-step reasoning (MenatQA and TempReason), indicating that CoT is more effective for multi-hop questions. In summary, zero-shot CoT consistently has a negative impact on temporal reasoning. While in fewshot scenario, CoT has a positive impact on symbolic and complex tasks, while negatively affecting knowledge-sensitive tasks.

# 6 Analysis and Discussion

# 1 Scaling Effect of Model Size

We investigate how the scale of models affects temporal reasoning capabilities. The trend is illustrated in Figure [4.](#page-6-1) As the model scale increases, there is a notable improvement in performance. When the parameter size expands from 7B to 13B, LLaMA2 and Baichuan2 show improvements of

<span id="page-6-0"></span>![](_page_6_Figure_0.jpeg)
<!-- Image Description: This image presents two heatmaps comparing the performance of several large language models (LLMs) across various evaluation metrics. The top heatmap shows zero-shot performance, while the bottom shows few-shot performance. Each cell's color intensity represents a score (indicated by the color bar), reflecting the LLM's performance on a specific metric (e.g., TimeXNLI, Arith, Overall). The heatmaps visually compare the LLMs' strengths and weaknesses across different tasks and evaluation methods. -->

Figure 3: ∆Score between the chain-of-thought prompting and direct I-O prompting. Top: zero-shot setting, Bottom: few-shot setting, Left: variation in each task, Right: averaged variation in the symbolic, commonsense, event, and overall tasks.

<span id="page-6-1"></span>![](_page_6_Figure_2.jpeg)
<!-- Image Description: The image displays a line graph comparing the performance of four large language models (Baichuan2, ChatGLM3, LLaMA2, Mistral) across different model sizes (6b/7b, 13b, 70b). The y-axis represents an unspecified performance metric, and the x-axis represents the model size in billions of parameters (B). The graph shows a generally positive correlation between model size and performance for each model, with LLaMA2 exhibiting the strongest performance increase with size. -->

Figure 4: Scaling effect of model size and overall temporal reasoning performance. The x-axis (model size) is shown in the log scale. Results show a log-linearity between parameter size and performance.

13.0% and 10.5%, respectively. Furthermore, when LLaMA scales up to 70B, the trend of performance improvement continues without stopping. The overall improvement follows a log-linear relationship with scale. There are no significant performance differences among LLaMA2, Baichuan2, and ChatGLM3 under similar parameter specifications, while Mistral demonstrates impressive prowess, outperforming all other 13B models with nearly half the number of parameters.

## 2 Challenges in Temporal Reasoning

LLMs underperform in (multi-hop) symbolic reasoning Except for GPT-4, the performance of all other models in symbolic temporal reasoning is unsatisfactory. A noticeable decrease is observed in duration-conversion task compared to other atomic tasks (25% in GPT-4 and 27% in LLaMA270b). This is because the duration-conversion task (s3)

<span id="page-6-2"></span>

| Model             | Order  | Duration | Freq.  | Stationarity | Typical | Avg. |
|-------------------|--------|----------|--------|--------------|---------|------|
| GPT-4             | 76.4 ↓ | 92.8 ↑   | 83.3 ↑ | 71.4 ↓       | 54.5 ↓  | 77.5 |
| GPT-3.5           | 50.5 ↑ | 39.8 ↓   | 55.2 ↑ | 48.4 ↑       | 28.7 ↓  | 43.5 |
| Baichuan2†<br>13b | 40.5 ↓ | 51.8 ↑   | 43.7 ↑ | 46.2 ↑       | 29.8 ↓  | 42.5 |
| LLaMA2†<br>70b    | 65.2 ↑ | 72.1 ↑   | 66.3 ↑ | 36.3 ↓       | 52.7 ↓  | 63.0 |
| Mistral†<br>7b    | 27.0 ↓ | 44.4 ↑   | 58.3 ↑ | 38.5 ↓       | 38.3 ↓  | 42.5 |

Table 6: Results in each temporal commonsense aspect under few-shot setting. Models with † are base models. Red ↓ and Green ↑ represent the performance is lower or higher than its average performance. Metric is EM.

necessitates a two-step reasoning process. It first unifies time units, and subsequently engages in numerical comparison. In contrast, other atomic tasks (s1, s2 and arithmetic) can be completed with a single reasoning step. In summary, LLMs perform poorly in symbolic temporal reasoning and exhibit more pronounced declines when encountering multi-step reasoning.

Mastery of commonsense knowledge varies in LLMs We analyze models' performance across various commonsense aspects, as shown in Table [6.](#page-6-2) We regard the model's average performance in commonsense reasoning tasks as the baseline. If the model outperforms the baseline in a specific aspect, it suggests greater proficiency in this type of knowledge, and vice versa. The findings indicate that LLMs generally demonstrate good knowledge of event duration and frequency. However, their comprehension of event order and typical events is relatively weaker The uneven mastery of commonsense knowledge significantly affects the model's reasoning performance, especially when dealing with complex questions that involve multiple types of knowledge. Retrieval-augmented reasoning presents a promising avenue for mitigating the model's knowledge scarcity.

LLMs exhibit poor implicit temporal reasoning capabilities. When comparing explicit and implicit event temporal reasoning, specifically TimeQA-explicit versus others, we observe a significant performance decrease in implicit reasoning. Additionally, on TRACIE with numerous implied events, most models only surpass a random baseline (50.0). Even GPT-4, despite its advanced capabilities, achieves only a 66.4% accuracy, suggesting that the LLM struggles with modeling implicit temporal relationships. We consider it helpful to explicitly model the temporal relationships between events and time expressions, for instance constructing timelines or temporal graphs.

<span id="page-7-0"></span>![](_page_7_Figure_0.jpeg)
<!-- Image Description: This bar chart compares the performance of "Base" and "Align" models across various large language models (LLMs). The x-axis lists different LLMs (e.g., LLaMA270b, Vicuna1.513b), while the y-axis represents a performance metric (unspecified). Each LLM has two bars, showing its score for both Base and Align versions. The chart likely illustrates the impact of an alignment technique on LLM performance within the paper. -->

Figure 5: Performance difference between base and alignment models under few-shot setting. Baichuan2 and LLaMA2 are aligned with SFT and RLHF. Vicuna, Mistral and ChatGLM3 are aligned with only SFT.

LLMs are good factual reasoners rather than factual extractors When humans engage in temporal reasoning, it generally involves two steps: first, extracting time-fact pairs from the context, and then performing fact-based reasoning. TempReason provides extracted facts for conducting fact-based reasoning. By comparing the model's performance in context-based (TimeQA) against fact-based (TempReason) reasoning, we identify the bottleneck in event temporal reasoning. LLMs excel in TempReason, which signifies their strong capability in fact-based reasoning. However, their performance in context-based reasoning is significantly weaker compared to their performance in fact-based reasoning. This implies that errors could arise during the extraction of time-sensitive facts from the context. We attribute this performance gap to the model's deficiency in factual extraction capabilities Thus, we consider LLMs to be strong factual reasoners rather than factual extractors in event temporal reasoning.

### 3 Alignment Impairs Temporal Reasoning

In the experiments mentioned earlier (Table [5\)](#page-5-0), we observe a sharp decline in zero-shot performance of alignment models. To investigate whether alignment is the cause of the decline in temporal reasoning, we conducted experiments on alignment models under few-shot settings. Figure [5](#page-7-0) illustrates the overall performance decline after alignment. With the exception of Baichuan2, all other models are severely impaired, experiencing a significant drop of up to 22%. Through manual analysis of error cases, we have summarized two reasons: (1) Alignment reduces the model's usability, causing it to tend towards refusal to answer when confronted with knowledge-sensitive questions. (2) Alignment damages the model's in-context learning capability,

resulting in situations where the model deviates from the demonstrations. Furthermore, we believe that the lack of temporal reasoning-related training data in alignment exacerbates this issue, leading to disparities between different reasoning capabilities, such as mathematical and temporal reasoning.

#### 4 Error Analysis

We manually analyze 100 predictions by GPT-4, GPT-3.5 and LLaMa2-base70<sup>b</sup> from each subtask. The visualization of errors is shown in Figure [6.](#page-8-0)

Symbolic Reasoning We categorize symbolic reasoning errors into five groups: (a)*Expression*: The model provides an incorrect time calculation expression. (b) *Computation*: The model provides the correct time calculation expression, but there is a calculation error. (c) *Conversion*: The model has an error in the conversion of time units. (d) *Comparison*: The model has an error when comparing two time-expressions (or intervals). (e) *Combination*: The model encounters errors in the combination of multiple above operations. LLMs exhibit numerous computation, conversion, and comparison errors, which suggests a substantial deficiency in their understanding of fundamental temporal expressions. Additionally, a higher frequency of errors is observed in combination questions, highlighting that multi-step reasoning continues to be a significant challenge for current models

Commonsense Reasoning We categorize the errors of commonsense reasoning into two groups: (a) *No Answer*: The model fails to provide a final answer. (b) *Reasoning Error*: The model encounters reasoning errors, which can be subdivided into five types of knowledge-related errors. We observe that GPT series models have a higher *No Answer*rate, while LLaMA is always able to provide answers. This discrepancy can be attributed to two factors: firstly, the models may lack the necessary commonsense knowledge to formulate an answer; secondly, the preference alignment mechanism may prompt the model to abstain from answering when confronted with questions outside its knowledge scope. Integration of retrieval can alleviate the problem of knowledge scarcity to a certain degree.

Event Temporal Reasoning We categorize the errors of event temporal reasoning into four groups: (a)*No Answer*: The model is unable to find the answer in the context. (b) *Reasoning Error*: The model encounters reasoning errors. (c) *Halluci-*<span id="page-8-0"></span>![](_page_8_Figure_0.jpeg)
<!-- Image Description: This figure presents three bar charts comparing reasoning errors of GPT-4, GPT-3.5, and LLaMA2 across different reasoning categories. The charts are titled "Symbolic," "Commonsense," and "Event Temporal," representing different reasoning domains. Each bar within a chart shows the error count for a specific reasoning aspect (e.g., computation, frequency, metric limit) for each model. The figure illustrates the relative strengths and weaknesses of the models in various reasoning tasks. -->

Figure 6: Error analysis for Symbolic, Commonsense, and Event Temporal. We select 100 test samples from each subtask for GPT-4, GPT-3.5 and LLaMa2-base70b.
*nation*: The model's prediction does not exist in the context, known as hallucination reasoning. (d) *Metric*: The model's prediction is correct, but the metric is limited by the evaluation criteria. It can be observed that, except for reasoning errors, failures to provide answers account for approximately 30%, indicating that models still have flaws in grounding temporal facts from context. Additionally, models occasionally experience hallucination phenomena, leading to erroneous reasoning.

# 7 Related Work

## 1 Temporal Reasoning

There are numerous efforts addressing diverse challenges in temporal reasoning. Early research mainly relies on TimeML [\(Pustejovsky et al.,](#page-11-8) [2003\)](#page-11-8), focusing TimeX extraction and temporal relation extraction [\(Verhagen et al.,](#page-12-8) [2007,](#page-12-8) [2010;](#page-12-9) [UzZa](#page-12-10)[man et al.,](#page-12-10) [2013;](#page-12-10) [Llorens et al.,](#page-10-6) [2015;](#page-10-6) [Miller](#page-10-7) [et al.,](#page-10-7) [2015;](#page-10-7) [Mathur et al.,](#page-10-8) [2021;](#page-10-8) [Vashishtha et al.,](#page-12-11) [2019\)](#page-12-11). The advent of pre-trained language models (PLMs) has brought about commonsense reasoning as a tool to explore the world knowledge in models [\(Zhou et al.,](#page-13-0) [2019;](#page-13-0) [Qin et al.,](#page-11-7) [2021;](#page-11-7) [Dhin](#page-10-2)[gra et al.,](#page-10-2) [2022\)](#page-10-2). Recently, much attention has shifted towards event temporal reasoning [\(Chen](#page-9-2) [et al.,](#page-9-2) [2021;](#page-9-2) [Tan et al.,](#page-11-5) [2023;](#page-11-5) [Wei et al.,](#page-12-7) [2023\)](#page-12-7). [Han et al.](#page-10-9) [\(2021\)](#page-10-9); [Yang et al.](#page-12-12) [\(2023b\)](#page-12-12); [Son and](#page-11-9) [Oh](#page-11-9) [\(2023\)](#page-11-9); [Chen et al.](#page-9-5) [\(2023\)](#page-9-5) continuously pretrains LLMs on time-aware data to elicit temporal reasoning, and [Zhu et al.](#page-13-2) [\(2023\)](#page-13-2); [Su et al.](#page-11-10) [\(2023\)](#page-11-10); [Chu et al.](#page-10-10) [\(2023\)](#page-10-10) explicitly represent temporal relationships using temporal graphs and timelines. Additionally, some works extend beyond text, evaluating temporal reasoning in structured tables and video domains [\(Gupta et al.,](#page-10-11) [2023;](#page-10-11) [Ko et al.,](#page-10-12) [2023\)](#page-10-12).

Some concurrent studies also analyze the temporal reasoning abilities of LLMs. [Jain et al.](#page-10-13) [\(2023\)](#page-10-13); [Qiu et al.](#page-11-11) [\(2023\)](#page-11-11) focus on temporal commonsense

and [Wang and Zhao](#page-12-1) [\(2023\)](#page-12-1) introduces a unified form for accessing the overall abilities.

Distinguished from other works, TIMEBENCH is multispectral, offering a comprehensive evaluation of LLM's temporal reasoning abilities.

### 2 Large Language Models

In recent years, there has been rapid progress in the research of large language models (LLM) [\(Zhao](#page-13-3) [et al.,](#page-13-3) [2023\)](#page-13-3). They exhibit outstanding performance across a multitude of tasks without the need for finetuning [\(Brown et al.,](#page-9-0) [2020;](#page-9-0) [Kojima et al.,](#page-10-5) [2022\)](#page-10-5). Furthermore, they have achieved astonishing results in complex reasoning tasks, such as mathematical reasoning [\(Cobbe et al.,](#page-10-0) [2021;](#page-10-0) [Mishra](#page-11-0) [et al.,](#page-11-0) [2022\)](#page-11-0) and logical reasoning [\(Yu et al.,](#page-12-0) [2020;](#page-12-0) [Liu et al.,](#page-10-14) [2023\)](#page-10-14). Moreover, some studies suggest that the chain-of-thought prompting can further enhance the model's capabilities in complex reasoning scenarios [\(Wei et al.,](#page-12-4) [2022;](#page-12-4) [Kojima et al.,](#page-10-5) [2022;](#page-10-5) [Chu et al.,](#page-9-6) [2024;](#page-9-6) [Zhang et al.,](#page-12-13) [2023\)](#page-12-13).

# 8 Conclusion

Temporal reasoning entails inherent diversity and complexity. The lack of a comprehensive benchmark makes it challenging to quantify LLMs' temporal reasoning capabilities. In this work, we present TIMEBENCH, a comprehensive and hierarchical benchmark for LLM temporal reasoning, tailored to mirror temporal reasoning in complex scenarios. We conduct extensive experiments on state-of-the-art LLMs to investigate their temporal reasoning capabilities. Our findings indicate a substantial gap between state-of-the-art LLMs and human performance, emphasizing the need for further research in this area. Moreover, we provide a meticulous analysis and discussion, outlining the current challenges that models face and suggesting potential directions for improvement.

# Limitations

TimeBench is a comprehensive benchmark to quantify the temporal reasoning capabilities of LLMs. While we have taken various factors into account, there are a few limitations. Firstly, our evaluation only applied prompt-based method under zero-shot and few-shot setting, lacking evaluations specifically tailored for models fine-tuned on the temporal domain. Secondly, the instructions and demonstrations were manually crafted, which may potentially lead to discrepancies in prompts interpretation among different LLMs. Thirdly, the dataset constituting the benchmark includes data from past years and a portion sourced from Wikipedia, which may contaminate the training corpus of LLMs.

# Acknowledgements

The research in this article is supported by the National Key Research and Development Project (2021YFF0901602), the National Science Foundation of China (U22B2059, 62276083), and Shenzhen Foundational Research Funding (JCYJ20200109113441941), Major Key Project of PCL (PCL2021A06). Ming Liu is the corresponding author.

# References

- <span id="page-9-8"></span>Joshua Ainslie, James Lee-Thorp, Michiel de Jong, Yury Zemlyanskiy, Federico Lebrón, and Sumit Sanghai. 2023. [GQA: training generalized multi-query trans](https://doi.org/10.18653/V1/2023.EMNLP-MAIN.298)[former models from multi-head checkpoints.](https://doi.org/10.18653/V1/2023.EMNLP-MAIN.298) In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023*, pages 4895–4901. Association for Computational Linguistics.
- <span id="page-9-7"></span>Satanjeev Banerjee and Alon Lavie. 2005. Meteor: An automatic metric for mt evaluation with improved correlation with human judgments. In *Proceedings of the acl workshop on intrinsic and extrinsic evaluation measures for machine translation and/or summarization*, pages 65–72.
- <span id="page-9-3"></span>Lawrence W Barsalou, Léo Dutriaux, and Christoph Scheepers. 2018. Moving beyond the distinction between concrete and abstract concepts. *Philosophical Transactions of the Royal Society B: Biological Sciences*, 373(1752):20170144.
- <span id="page-9-9"></span>Iz Beltagy, Matthew E Peters, and Arman Cohan. 2020. Longformer: The long-document transformer. *arXiv preprint arXiv:2004.05150*.
- <span id="page-9-0"></span>Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda

Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. 2020. [Language models are few-shot learners.](https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html) In *Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual*.

- <span id="page-9-2"></span>Wenhu Chen, Xinyi Wang, and William Yang Wang. 2021. [A dataset for answering time-sensitive ques](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/1f0e3dad99908345f7439f8ffabdffc4-Abstract-round2.html)[tions.](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/1f0e3dad99908345f7439f8ffabdffc4-Abstract-round2.html) In *Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks 1, NeurIPS Datasets and Benchmarks 2021, December 2021, virtual*.
- <span id="page-9-5"></span>Ziqiang Chen, Shaojuan Wu, Xiaowang Zhang, and Zhiyong Feng. 2023. [TML: A temporal-aware multi](https://doi.org/10.1145/3543873.3587347)[task learning framework for time-sensitive question](https://doi.org/10.1145/3543873.3587347) [answering.](https://doi.org/10.1145/3543873.3587347) In *Companion Proceedings of the ACM Web Conference 2023, WWW 2023, Austin, TX, USA, 30 April 2023 - 4 May 2023*, pages 200–203. ACM.
- <span id="page-9-4"></span>Wei-Lin Chiang, Zhuohan Li, Zi Lin, Ying Sheng, Zhanghao Wu, Hao Zhang, Lianmin Zheng, Siyuan Zhuang, Yonghao Zhuang, Joseph E. Gonzalez, Ion Stoica, and Eric P. Xing. 2023. [Vicuna: An open](https://lmsys.org/blog/2023-03-30-vicuna/)[source chatbot impressing gpt-4 with 90%\\*chatgpt](https://lmsys.org/blog/2023-03-30-vicuna/) [quality.](https://lmsys.org/blog/2023-03-30-vicuna/)
- <span id="page-9-1"></span>Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, Parker Schuh, Kensen Shi, Sasha Tsvyashchenko, Joshua Maynez, Abhishek Rao, Parker Barnes, Yi Tay, Noam Shazeer, Vinodkumar Prabhakaran, Emily Reif, Nan Du, Ben Hutchinson, Reiner Pope, James Bradbury, Jacob Austin, Michael Isard, Guy Gur-Ari, Pengcheng Yin, Toju Duke, Anselm Levskaya, Sanjay Ghemawat, Sunipa Dev, Henryk Michalewski, Xavier Garcia, Vedant Misra, Kevin Robinson, Liam Fedus, Denny Zhou, Daphne Ippolito, David Luan, Hyeontaek Lim, Barret Zoph, Alexander Spiridonov, Ryan Sepassi, David Dohan, Shivani Agrawal, Mark Omernick, Andrew M. Dai, Thanumalayan Sankaranarayana Pillai, Marie Pellat, Aitor Lewkowycz, Erica Moreira, Rewon Child, Oleksandr Polozov, Katherine Lee, Zongwei Zhou, Xuezhi Wang, Brennan Saeta, Mark Diaz, Orhan Firat, Michele Catasta, Jason Wei, Kathy Meier-Hellstern, Douglas Eck, Jeff Dean, Slav Petrov, and Noah Fiedel. 2023. [Palm: Scaling language mod](http://jmlr.org/papers/v24/22-1144.html)[eling with pathways.](http://jmlr.org/papers/v24/22-1144.html)*J. Mach. Learn. Res.*, 24:240:1– 240:113.
- <span id="page-9-6"></span>Zheng Chu, Jingchang Chen, Qianglong Chen, Weijiang Yu, Tao He, Haotian Wang, Weihua Peng, Ming Liu, Bing Qin, and Ting Liu. 2024. [Navigate through](https://arxiv.org/abs/2309.15402) [enigmatic labyrinth a survey of chain of thought rea](https://arxiv.org/abs/2309.15402)[soning: Advances, frontiers and future.](https://arxiv.org/abs/2309.15402) In *The 62nd Annual Meeting of the Association for Computational*

*Linguistics: ACL 2024, Bangkok, Thailand, August 11–16, 2024*. Association for Computational Linguistics.

- <span id="page-10-10"></span>Zheng Chu, Zekun Wang, Jiafeng Liang, Ming Liu, and Bing Qin. 2023. [MTGER: multi-view tempo](https://doi.org/10.18653/V1/2023.FINDINGS-EMNLP.1016)[ral graph enhanced temporal reasoning over time](https://doi.org/10.18653/V1/2023.FINDINGS-EMNLP.1016)[involved document.](https://doi.org/10.18653/V1/2023.FINDINGS-EMNLP.1016) In *Findings of the Association for Computational Linguistics: EMNLP 2023, Singapore, December 6-10, 2023*, pages 15218–15233. Association for Computational Linguistics.
- <span id="page-10-4"></span>Hyung Won Chung, Le Hou, Shayne Longpre, Barret Zoph, Yi Tay, William Fedus, Yunxuan Li, Xuezhi Wang, Mostafa Dehghani, Siddhartha Brahma, Albert Webson, Shixiang Shane Gu, Zhuyun Dai, Mirac Suzgun, Xinyun Chen, Aakanksha Chowdhery, Alex Castro-Ros, Marie Pellat, Kevin Robinson, Dasha Valter, Sharan Narang, Gaurav Mishra, Adams Yu, Vincent Zhao, Yanping Huang, Andrew Dai, Hongkun Yu, Slav Petrov, Ed H. Chi, Jeff Dean, Jacob Devlin, Adam Roberts, Denny Zhou, Quoc V. Le, and Jason Wei. 2022. [Scaling instruction-finetuned](https://arxiv.org/abs/2210.11416) [language models.](https://arxiv.org/abs/2210.11416) *Preprint*, arXiv:2210.11416.
- <span id="page-10-0"></span>Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. 2021. [Training verifiers to solve math word prob](https://arxiv.org/abs/2110.14168)[lems.](https://arxiv.org/abs/2110.14168) *CoRR*, abs/2110.14168.
- <span id="page-10-2"></span>Bhuwan Dhingra, Jeremy R. Cole, Julian Martin Eisenschlos, Daniel Gillick, Jacob Eisenstein, and William W. Cohen. 2022. [Time-aware language mod](https://doi.org/10.1162/TACL_A_00459)[els as temporal knowledge bases.](https://doi.org/10.1162/TACL_A_00459) *Trans. Assoc. Comput. Linguistics*, 10:257–273.
- <span id="page-10-11"></span>Vivek Gupta, Pranshu Kandoi, Mahek Bhavesh Vora, Shuo Zhang, Yujie He, Ridho Reinanda, and Vivek Srikumar. 2023. [Temptabqa: Temporal question an](https://doi.org/10.18653/V1/2023.EMNLP-MAIN.149)[swering for semi-structured tables.](https://doi.org/10.18653/V1/2023.EMNLP-MAIN.149) In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023*, pages 2431–2453. Association for Computational Linguistics.
- <span id="page-10-9"></span>Rujun Han, Xiang Ren, and Nanyun Peng. 2021. [ECONET: effective continual pretraining of language](https://doi.org/10.18653/V1/2021.EMNLP-MAIN.436) [models for event temporal reasoning.](https://doi.org/10.18653/V1/2021.EMNLP-MAIN.436) In *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, EMNLP 2021, Virtual Event / Punta Cana, Dominican Republic, 7-11 November, 2021*, pages 5367–5380. Association for Computational Linguistics.
- <span id="page-10-1"></span>Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob Steinhardt. 2021. [Measuring massive multitask language](https://openreview.net/forum?id=d7KBjmI3GmQ) [understanding.](https://openreview.net/forum?id=d7KBjmI3GmQ) In *9th International Conference on Learning Representations, ICLR 2021, Virtual Event, Austria, May 3-7, 2021*. OpenReview.net.
- <span id="page-10-13"></span>Raghav Jain, Daivik Sojitra, Arkadeep Acharya, Sriparna Saha, Adam Jatowt, and Sandipan Dandapat.

2023. [Do language models have a common sense](https://doi.org/10.18653/v1/2023.emnlp-main.418) [regarding time? revisiting temporal commonsense](https://doi.org/10.18653/v1/2023.emnlp-main.418) [reasoning in the era of large language models.](https://doi.org/10.18653/v1/2023.emnlp-main.418) In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing*, pages 6750– 6774, Singapore. Association for Computational Linguistics.

- <span id="page-10-3"></span>Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de Las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux, Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed. 2023. [Mistral](https://doi.org/10.48550/ARXIV.2310.06825) [7b.](https://doi.org/10.48550/ARXIV.2310.06825) *CoRR*, abs/2310.06825.
- <span id="page-10-12"></span>Dohwan Ko, Ji Soo Lee, Woo-Young Kang, Byungseok Roh, and Hyunwoo Kim. 2023. [Large language mod](https://doi.org/10.18653/V1/2023.EMNLP-MAIN.261)[els are temporal and causal reasoners for video ques](https://doi.org/10.18653/V1/2023.EMNLP-MAIN.261)[tion answering.](https://doi.org/10.18653/V1/2023.EMNLP-MAIN.261) In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023*, pages 4300–4316. Association for Computational Linguistics.
- <span id="page-10-5"></span>Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. 2022. [Large lan](http://papers.nips.cc/paper_files/paper/2022/hash/8bb0d291acd4acf06ef112099c16f326-Abstract-Conference.html)[guage models are zero-shot reasoners.](http://papers.nips.cc/paper_files/paper/2022/hash/8bb0d291acd4acf06ef112099c16f326-Abstract-Conference.html) In *NeurIPS*.
- <span id="page-10-15"></span>Chin-Yew Lin. 2004. Rouge: A package for automatic evaluation of summaries. In *Text summarization branches out*, pages 74–81.
- <span id="page-10-14"></span>Hanmeng Liu, Zhiyang Teng, Ruoxi Ning, Jian Liu, Qiji Zhou, and Yue Zhang. 2023. [Glore: Evaluating](https://doi.org/10.48550/ARXIV.2310.09107) [logical reasoning of large language models.](https://doi.org/10.48550/ARXIV.2310.09107) *CoRR*, abs/2310.09107.
- <span id="page-10-6"></span>Hector Llorens, Nathanael Chambers, Naushad Uz-Zaman, Nasrin Mostafazadeh, James F. Allen, and James Pustejovsky. 2015. [Semeval-2015 task 5: QA](https://doi.org/10.18653/V1/S15-2134) [tempeval - evaluating temporal information under](https://doi.org/10.18653/V1/S15-2134)[standing with question answering.](https://doi.org/10.18653/V1/S15-2134) In *Proceedings of the 9th International Workshop on Semantic Evaluation, SemEval@NAACL-HLT 2015, Denver, Colorado, USA, June 4-5, 2015*, pages 792–800. The Association for Computer Linguistics.
- <span id="page-10-8"></span>Puneet Mathur, Rajiv Jain, Franck Dernoncourt, Vlad Morariu, Quan Hung Tran, and Dinesh Manocha. 2021. [TIMERS: Document-level temporal relation](https://doi.org/10.18653/v1/2021.acl-short.67) [extraction.](https://doi.org/10.18653/v1/2021.acl-short.67) In *Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 2: Short Papers)*, pages 524–533, Online. Association for Computational Linguistics.
- <span id="page-10-7"></span>Timothy Miller, Steven Bethard, Dmitriy Dligach, Chen Lin, and Guergana Savova. 2015. [Extracting time](https://doi.org/10.18653/v1/W15-3809) [expressions from clinical text.](https://doi.org/10.18653/v1/W15-3809) In *Proceedings of BioNLP 15*, pages 81–91, Beijing, China. Association for Computational Linguistics.

- <span id="page-11-0"></span>Swaroop Mishra, Matthew Finlayson, Pan Lu, Leonard Tang, Sean Welleck, Chitta Baral, Tanmay Rajpurohit, Oyvind Tafjord, Ashish Sabharwal, Peter Clark, and Ashwin Kalyan. 2022. [LILA: A unified bench](https://doi.org/10.18653/V1/2022.EMNLP-MAIN.392)[mark for mathematical reasoning.](https://doi.org/10.18653/V1/2022.EMNLP-MAIN.392) In *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing, EMNLP 2022, Abu Dhabi, United Arab Emirates, December 7-11, 2022*, pages 5807–5832. Association for Computational Linguistics.
- <span id="page-11-2"></span>OpenAI. 2023. [GPT-4 technical report.](https://doi.org/10.48550/ARXIV.2303.08774) *CoRR*, abs/2303.08774.
- <span id="page-11-4"></span>Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul F. Christiano, Jan Leike, and Ryan Lowe. 2022. [Training language models to follow instruc](http://papers.nips.cc/paper_files/paper/2022/hash/b1efde53be364a73914f58805a001731-Abstract-Conference.html)[tions with human feedback.](http://papers.nips.cc/paper_files/paper/2022/hash/b1efde53be364a73914f58805a001731-Abstract-Conference.html) In *NeurIPS*.
- <span id="page-11-12"></span>Kishore Papineni, Salim Roukos, Todd Ward, and Wei-Jing Zhu. 2002. Bleu: a method for automatic evaluation of machine translation. In *Proceedings of the 40th annual meeting of the Association for Computational Linguistics*, pages 311–318.
- <span id="page-11-8"></span>James Pustejovsky, José M. Castaño, Robert Ingria, Roser Saurí, Robert J. Gaizauskas, Andrea Setzer, Graham Katz, and Dragomir R. Radev. 2003. Timeml: Robust specification of event and temporal expressions in text. In *New Directions in Question Answering, Papers from 2003 AAAI Spring Symposium, Stanford University, Stanford, CA, USA*, pages 28–34. AAAI Press.
- <span id="page-11-7"></span>Lianhui Qin, Aditya Gupta, Shyam Upadhyay, Luheng He, Yejin Choi, and Manaal Faruqui. 2021. [TIME-](https://doi.org/10.18653/V1/2021.ACL-LONG.549)[DIAL: temporal commonsense reasoning in dialog.](https://doi.org/10.18653/V1/2021.ACL-LONG.549) In *Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing, ACL/IJCNLP 2021, (Volume 1: Long Papers), Virtual Event, August 1-6, 2021*, pages 7066–7076. Association for Computational Linguistics.
- <span id="page-11-11"></span>Yifu Qiu, Zheng Zhao, Yftah Ziser, Anna Korhonen, Edoardo M. Ponti, and Shay B. Cohen. 2023. [Are](https://doi.org/10.48550/ARXIV.2311.08398) [large language models temporally grounded?](https://doi.org/10.48550/ARXIV.2311.08398) *CoRR*, abs/2311.08398.
- <span id="page-11-13"></span>Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J. Liu. 2020. [Exploring the limits](http://jmlr.org/papers/v21/20-074.html) [of transfer learning with a unified text-to-text trans](http://jmlr.org/papers/v21/20-074.html)[former.](http://jmlr.org/papers/v21/20-074.html) *J. Mach. Learn. Res.*, 21:140:1–140:67.
- <span id="page-11-9"></span>Jungbin Son and Alice Oh. 2023. [Time-aware represen](https://doi.org/10.18653/V1/2023.FINDINGS-EMNLP.6)[tation learning for time-sensitive question answering.](https://doi.org/10.18653/V1/2023.FINDINGS-EMNLP.6) In *Findings of the Association for Computational Linguistics: EMNLP 2023, Singapore, December 6-10, 2023*, pages 70–77. Association for Computational Linguistics.

- <span id="page-11-1"></span>Aarohi Srivastava, Abhinav Rastogi, Abhishek Rao, Abu Awal Md Shoeb, Abubakar Abid, Adam Fisch, Adam R. Brown, Adam Santoro, Aditya Gupta, Adrià Garriga-Alonso, Agnieszka Kluska, Aitor Lewkowycz, Akshat Agarwal, Alethea Power, Alex Ray, Alex Warstadt, Alexander W. Kocurek, Ali Safaya, Ali Tazarv, Alice Xiang, Alicia Parrish, Allen Nie, Aman Hussain, Amanda Askell, Amanda Dsouza, Ameet Rahane, Anantharaman S. Iyer, Anders Andreassen, Andrea Santilli, Andreas Stuhlmüller, Andrew M. Dai, Andrew La, Andrew K. Lampinen, Andy Zou, Angela Jiang, Angelica Chen, Anh Vuong, Animesh Gupta, Anna Gottardi, Antonio Norelli, Anu Venkatesh, Arash Gholamidavoodi, Arfa Tabassum, Arul Menezes, Arun Kirubarajan, Asher Mullokandov, Ashish Sabharwal, Austin Herrick, Avia Efrat, Aykut Erdem, Ayla Karakas, and et al. 2022. [Beyond the imitation game: Quantifying](https://doi.org/10.48550/ARXIV.2206.04615) [and extrapolating the capabilities of language models.](https://doi.org/10.48550/ARXIV.2206.04615) *CoRR*, abs/2206.04615.
- <span id="page-11-10"></span>Xin Su, Phillip Howard, Nagib Hakim, and Steven Bethard. 2023. [Fusing temporal graphs into trans](https://doi.org/10.18653/V1/2023.FINDINGS-EMNLP.67)[formers for time-sensitive question answering.](https://doi.org/10.18653/V1/2023.FINDINGS-EMNLP.67) In *Findings of the Association for Computational Linguistics: EMNLP 2023, Singapore, December 6-10, 2023*, pages 948–966. Association for Computational Linguistics.
- <span id="page-11-5"></span>Qingyu Tan, Hwee Tou Ng, and Lidong Bing. 2023. [Towards benchmarking and improving the temporal](https://doi.org/10.18653/V1/2023.ACL-LONG.828) [reasoning capability of large language models.](https://doi.org/10.18653/V1/2023.ACL-LONG.828) In *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2023, Toronto, Canada, July 9-14, 2023*, pages 14820–14835. Association for Computational Linguistics.
- <span id="page-11-6"></span>Shivin Thukral, Kunal Kukreja, and Christian Kavouras. 2021. [Probing language models for understand](https://doi.org/10.18653/V1/2021.BLACKBOXNLP-1.31)[ing of temporal expressions.](https://doi.org/10.18653/V1/2021.BLACKBOXNLP-1.31) In *Proceedings of the Fourth BlackboxNLP Workshop on Analyzing and Interpreting Neural Networks for NLP, BlackboxNLP@EMNLP 2021, Punta Cana, Dominican Republic, November 11, 2021*, pages 396–406. Association for Computational Linguistics.
- <span id="page-11-3"></span>Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Dan Bikel, Lukas Blecher, Cristian Canton Ferrer, Moya Chen, Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller, Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony Hartshorn, Saghar Hosseini, Rui Hou, Hakan Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa, Isabel Kloumann, Artem Korenev, Punit Singh Koura, Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Diana Liskovich, Yinghai Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov, Pushkar Mishra, Igor Molybog, Yixin Nie, Andrew Poulton, Jeremy Reizenstein, Rashi Rungta, Kalyan Saladi, Alan Schelten, Ruan Silva, Eric Michael Smith, Ranjan Subramanian, Xiaoqing Ellen Tan, Binh Tang, Ross Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu,

Zheng Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan, Melanie Kambadur, Sharan Narang, Aurelien Rodriguez, Robert Stojnic, Sergey Edunov, and Thomas Scialom. 2023. [Llama 2: Open foundation and fine](https://arxiv.org/abs/2307.09288)[tuned chat models.](https://arxiv.org/abs/2307.09288) *Preprint*, arXiv:2307.09288.

- <span id="page-12-10"></span>Naushad UzZaman, Hector Llorens, Leon Derczynski, James F. Allen, Marc Verhagen, and James Pustejovsky. 2013. [Semeval-2013 task 1: Tempeval-3:](https://aclanthology.org/S13-2001/) [Evaluating time expressions, events, and temporal re](https://aclanthology.org/S13-2001/)[lations.](https://aclanthology.org/S13-2001/) In *Proceedings of the 7th International Workshop on Semantic Evaluation, SemEval@NAACL-HLT 2013, Atlanta, Georgia, USA, June 14-15, 2013*, pages 1–9. The Association for Computer Linguistics.
- <span id="page-12-11"></span>Siddharth Vashishtha, Benjamin Van Durme, and Aaron Steven White. 2019. [Fine-grained temporal](https://doi.org/10.18653/v1/P19-1280) [relation extraction.](https://doi.org/10.18653/v1/P19-1280) In *Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics*, pages 2906–2919, Florence, Italy. Association for Computational Linguistics.
- <span id="page-12-14"></span>Ramakrishna Vedantam, C. Lawrence Zitnick, and Devi Parikh. 2015. [Cider: Consensus-based image descrip](https://doi.org/10.1109/CVPR.2015.7299087)[tion evaluation.](https://doi.org/10.1109/CVPR.2015.7299087) In *IEEE Conference on Computer Vision and Pattern Recognition, CVPR 2015, Boston, MA, USA, June 7-12, 2015*, pages 4566–4575. IEEE Computer Society.
- <span id="page-12-8"></span>Marc Verhagen, Robert J. Gaizauskas, Frank Schilder, Mark Hepple, Graham Katz, and James Pustejovsky. 2007. [Semeval-2007 task 15: Tempeval temporal](https://aclanthology.org/S07-1014/) [relation identification.](https://aclanthology.org/S07-1014/) In *Proceedings of the 4th International Workshop on Semantic Evaluations, SemEval@ACL 2007, Prague, Czech Republic, June 23-24, 2007*, pages 75–80. The Association for Computer Linguistics.
- <span id="page-12-9"></span>Marc Verhagen, Roser Saurí, Tommaso Caselli, and James Pustejovsky. 2010. [Semeval-2010 task 13:](https://aclanthology.org/S10-1010/) [Tempeval-2.](https://aclanthology.org/S10-1010/) In *Proceedings of the 5th International Workshop on Semantic Evaluation, SemEval@ACL 2010, Uppsala University, Uppsala, Sweden, July 15-16, 2010*, pages 57–62. The Association for Computer Linguistics.
- <span id="page-12-5"></span>Felix Giovanni Virgo, Fei Cheng, and Sadao Kurohashi. 2022. [Improving event duration question answering](https://aclanthology.org/2022.lrec-1.473) [by leveraging existing temporal information extrac](https://aclanthology.org/2022.lrec-1.473)[tion data.](https://aclanthology.org/2022.lrec-1.473) In *Proceedings of the Thirteenth Language Resources and Evaluation Conference, LREC 2022, Marseille, France, 20-25 June 2022*, pages 4451– 4457. European Language Resources Association.
- <span id="page-12-1"></span>Yuqing Wang and Yun Zhao. 2023. [TRAM: benchmark](https://doi.org/10.48550/ARXIV.2310.00835)[ing temporal reasoning for large language models.](https://doi.org/10.48550/ARXIV.2310.00835) *CoRR*, abs/2310.00835.
- <span id="page-12-4"></span>Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le, and Denny Zhou. 2022. [Chain-of-thought prompt](http://papers.nips.cc/paper_files/paper/2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract-Conference.html)[ing elicits reasoning in large language models.](http://papers.nips.cc/paper_files/paper/2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract-Conference.html) In *NeurIPS*.

- <span id="page-12-7"></span>Yifan Wei, Yisong Su, Huanhuan Ma, Xiaoyan Yu, Fangyu Lei, Yuanzhe Zhang, Jun Zhao, and Kang Liu. 2023. [Menatqa: A new dataset for testing the](https://doi.org/10.18653/V1/2023.FINDINGS-EMNLP.100) [temporal comprehension and reasoning abilities of](https://doi.org/10.18653/V1/2023.FINDINGS-EMNLP.100) [large language models.](https://doi.org/10.18653/V1/2023.FINDINGS-EMNLP.100) In *Findings of the Association for Computational Linguistics: EMNLP 2023, Singapore, December 6-10, 2023*, pages 1434–1447. Association for Computational Linguistics.
- <span id="page-12-2"></span>Aiyuan Yang, Bin Xiao, Bingning Wang, Borong Zhang, Ce Bian, Chao Yin, Chenxu Lv, Da Pan, Dian Wang, Dong Yan, Fan Yang, Fei Deng, Feng Wang, Feng Liu, Guangwei Ai, Guosheng Dong, Haizhou Zhao, Hang Xu, Haoze Sun, Hongda Zhang, Hui Liu, Jiaming Ji, Jian Xie, Juntao Dai, Kun Fang, Lei Su, Liang Song, Lifeng Liu, Liyun Ru, Luyao Ma, Mang Wang, Mickel Liu, MingAn Lin, Nuolan Nie, Peidong Guo, Ruiyang Sun, Tao Zhang, Tianpeng Li, Tianyu Li, Wei Cheng, Weipeng Chen, Xiangrong Zeng, Xiaochuan Wang, Xiaoxi Chen, Xin Men, Xin Yu, Xuehai Pan, Yanjun Shen, Yiding Wang, Yiyu Li, Youxin Jiang, Yuchen Gao, Yupeng Zhang, Zenan Zhou, and Zhiying Wu. 2023a. [Baichuan 2: Open large-scale language models.](https://doi.org/10.48550/ARXIV.2309.10305) *CoRR*, abs/2309.10305.
- <span id="page-12-12"></span>Sen Yang, Xin Li, Lidong Bing, and Wai Lam. 2023b. [Once upon a time in graph: Relative-time pretraining](https://doi.org/10.18653/V1/2023.EMNLP-MAIN.728) [for complex temporal reasoning.](https://doi.org/10.18653/V1/2023.EMNLP-MAIN.728) In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023*, pages 11879–11895. Association for Computational Linguistics.
- <span id="page-12-0"></span>Weihao Yu, Zihang Jiang, Yanfei Dong, and Jiashi Feng. 2020. [Reclor: A reading comprehension dataset re](https://openreview.net/forum?id=HJgJtT4tvB)[quiring logical reasoning.](https://openreview.net/forum?id=HJgJtT4tvB) In *8th International Conference on Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April 26-30, 2020*. OpenReview.net.
- <span id="page-12-3"></span>Aohan Zeng, Xiao Liu, Zhengxiao Du, Zihan Wang, Hanyu Lai, Ming Ding, Zhuoyi Yang, Yifan Xu, Wendi Zheng, Xiao Xia, Weng Lam Tam, Zixuan Ma, Yufei Xue, Jidong Zhai, Wenguang Chen, Zhiyuan Liu, Peng Zhang, Yuxiao Dong, and Jie Tang. 2023. [GLM-130B: an open bilingual pre-trained model.](https://openreview.net/pdf?id=-Aw0rrrPUF) In *The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023*. OpenReview.net.
- <span id="page-12-6"></span>Yunxiang Zhang and Xiaojun Wan. 2023. [Situated](http://papers.nips.cc/paper_files/paper/2023/hash/d4f2bc9885ecbe30f65031819ef8699f-Abstract-Datasets_and_Benchmarks.html)[gen: Incorporating geographical and temporal con](http://papers.nips.cc/paper_files/paper/2023/hash/d4f2bc9885ecbe30f65031819ef8699f-Abstract-Datasets_and_Benchmarks.html)[texts into generative commonsense reasoning.](http://papers.nips.cc/paper_files/paper/2023/hash/d4f2bc9885ecbe30f65031819ef8699f-Abstract-Datasets_and_Benchmarks.html) In *Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023*.
- <span id="page-12-13"></span>Zhuosheng Zhang, Yao Yao, Aston Zhang, Xiangru Tang, Xinbei Ma, Zhiwei He, Yiming Wang, Mark Gerstein, Rui Wang, Gongshen Liu, and Hai Zhao. 2023. [Igniting language intelligence: The hitch](https://doi.org/10.48550/ARXIV.2311.11797)[hiker's guide from chain-of-thought reasoning to lan](https://doi.org/10.48550/ARXIV.2311.11797)[guage agents.](https://doi.org/10.48550/ARXIV.2311.11797) *CoRR*, abs/2311.11797.

- <span id="page-13-3"></span>Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, Yifan Du, Chen Yang, Yushuo Chen, Zhipeng Chen, Jinhao Jiang, Ruiyang Ren, Yifan Li, Xinyu Tang, Zikang Liu, Peiyu Liu, Jian-Yun Nie, and Ji-Rong Wen. 2023. [A survey of large language models.](https://arxiv.org/abs/2303.18223) *Preprint*, arXiv:2303.18223.
- <span id="page-13-0"></span>Ben Zhou, Daniel Khashabi, Qiang Ning, and Dan Roth. 2019. ["going on a vacation" takes longer than "going](https://doi.org/10.18653/V1/D19-1332) [for a walk": A study of temporal commonsense under](https://doi.org/10.18653/V1/D19-1332)[standing.](https://doi.org/10.18653/V1/D19-1332) In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing, EMNLP-IJCNLP 2019, Hong Kong, China, November 3-7, 2019*, pages 3361– 3367. Association for Computational Linguistics.
- <span id="page-13-1"></span>Ben Zhou, Kyle Richardson, Qiang Ning, Tushar Khot, Ashish Sabharwal, and Dan Roth. 2021. [Temporal](https://doi.org/10.18653/V1/2021.NAACL-MAIN.107) [reasoning on implicit events from distant supervision.](https://doi.org/10.18653/V1/2021.NAACL-MAIN.107) In *Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, NAACL-HLT 2021, Online, June 6-11, 2021*, pages 1361–1371. Association for Computational Linguistics.
- <span id="page-13-2"></span>Xinyu Zhu, Cheng Yang, Bei Chen, Siheng Li, Jian-Guang Lou, and Yujiu Yang. 2023. [Question an](https://doi.org/10.18653/V1/2023.EMNLP-MAIN.787)[swering as programming for solving time-sensitive](https://doi.org/10.18653/V1/2023.EMNLP-MAIN.787) [questions.](https://doi.org/10.18653/V1/2023.EMNLP-MAIN.787) In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023*, pages 12775–12790. Association for Computational Linguistics.

# A TIMEBENCH Details

TIMEBENCH features 3 major categories, 10 tasks and 15 subtasks, each with distinct challenges, totaling 19,000 instances. Detailed statistics are available in Figure [7](#page-15-2) and Table [7.](#page-16-0)

# A.1 Benchmark Construction

TimeX Arithmetic [\(Tan et al.,](#page-11-5) [2023\)](#page-11-5) TimeX Arithmetic data is derived from the *l1: time-time*reasoning data in TempReason. We retain 4,000 instances, where time expressions are calculated with a minimum unit of one day.

TimeX NLI [\(Thukral et al.,](#page-11-6) [2021\)](#page-11-6) The original data of TimeXNLI is in NLI format, including three sub-tasks,*Temp-Order*, *Temp-Duration*, and *Cross-Unit Duration*, including 6,140, 3,540, and 15,840 instances respectively. We conduct a random sampling of 2,213, 2,332 and 2,429 entries, resulting in a combined total of 6,965 instances.

MCTACO [\(Zhou et al.,](#page-13-0) [2019\)](#page-13-0) The original MC-TACO dataset consists of yes/no questions, containing 1,332 questions with 9,442 options. To guarantee that the questions are presented in a 4-way multi-select style, we initially remove questions that have less than four options. Subsequently, to ensure that each question has at least one correct option, we filter out questions where all options are labeled as "no". For each remaining question, we randomly sample four options, striving to maintain a balance between correct and incorrect options. In most cases, a question is accompanied by 2 correct and 2 incorrect options. A minority of questions have an option distribution of 1-3 or 3-1. After the aforementioned filtering process, we obtain 852 pieces of data in a 4-way multi-select format.

DurationQA [\(Virgo et al.,](#page-12-5) [2022\)](#page-12-5) The original DurationQA has the same format as MCTACO, which consists of 694 questions with 4,868 options. Following the identical filtration procedure as MCTACO, we finally obtained a collection of 687 questions in a 4-way multi-select format.

TimeDial [\(Qin et al.,](#page-11-7) [2021\)](#page-11-7) consists of 4-way multi-select instances in a two-person dialogue scenario. We leave the original data unaltered and simply randomize the sequence of options, yielding 1,446 pieces of 4-way multi-select instances.

SituateGen [\(Zhang and Wan,](#page-12-6) [2023\)](#page-12-6) Situated-Gen includes 1,220 test cases, which span across two distinct reasoning domains: *time*and*geography*. We manually screen the original test data and retain those with clear time features for temporal reasoning evaluation, resulting in 115 instances.

TimeQA [\(Chen et al.,](#page-9-2) [2021\)](#page-9-2) The original data of TimeQA includes two splits, *Easy*and*Hard*, with each question containing 20 Wikipedia paragraphs. The excessively long context may exceed the model's maximum length limit and incur significant inference overhead. Therefore, we have reduced the context of the original data. For the paragraphs in the original data, we refer to those containing the answer as relevant paragraphs, and the rest as irrelevant paragraphs. For each question, we keep the first paragraph, all relevant paragraphs, and one random irrelevant paragraph as distractor. This ensures that most questions have at least three paragraphs. After that, we sample 500 pieces of data from those where the context length is less than 650 tokens. For both *Easy*and*Hard*splits,

we apply the aforementioned filtration, resulting in 500 questions each, totaling 1,000 instances.

TempReason [\(Tan et al.,](#page-11-5) [2023\)](#page-11-5) TempReason dataset contains 5,397 entries for l2 (event-time reasoning) and 4,426 entries for l3 (event-event reasoning). In the original dataset, each question corresponds with a text context and extracted facts. Similar to TimeQA, we apply a filter based on context length. We preserve questions with a context length between 300 and 600 tokens, yielding 839 and 1,037 instances, respectively. Notably, every remaining question is applicable to either contextbased reasoning or fact-based reasoning.

MenatQA [\(Wei et al.,](#page-12-7) [2023\)](#page-12-7) MenatQA consists of 999 data entries, formatted similarly to TimeQA, where each question is accompanied by several corresponding paragraphs. Following the paper's proposed method, we modify the original data by incorporating the three time-sensitive factors: scope, order, and counterfactual. Subsequently, for each factor, we randomly sample 400 instances, resulting in a total of 1,200 data points.

TRACIE [\(Zhou et al.,](#page-13-1) [2021\)](#page-13-1) The original TRA-CIE dataset consists of yes/no type questions, containing 4,248 test instances. We randomly sample 500 instances from the*iid*split in the test set.

## A.2 Human Performance Evaluation

Unless otherwise stated, the results of human evaluation are derived from original dataset papers. Please refer to the corresponding paper for human evaluation details. TimeXNLI, Date Arith, and MCTACO are manually evaluated by three authors from the TimeBench team. Within each subtask, we randomly sample 50 instances, and the average of the performances by three human evaluators is considered the final human performance.

### <span id="page-14-0"></span>A.3 Task Formats

TIMEBENCH is a multispectral benchmark, which features four different task formats.

Multi-Select Questions Previous work utilizes the Multiple Choice (MC) form, which requires models to select the only correct answer from the options. However, this task form has shortcuts and may not truly reflect the model's abilities. To address this, we employ the Multi-Select (M-S) task form, where the model needs to select all possible correct answers from the options provided. In our

task, each question presents four options, with at most two of them being correct.

Natural Language Inference is the task of determining the logical relationship between two pieces of text. Specifically, given a premise and a hypothesis, the model needs to determine whether the hypothesis can be inferred from the premise and output entailment, contradiction, or neutral. Our tasks focus on the entailment in temporal domains.

Free-form Reading Comprehension requires models to answer questions based on the provided context, and the ground truth answer is free-form without pre-defined format restrictions.

Constrained Text Generation refers to the task of generating text under certain constraints. The task is keyword-constrained text generation, where the model takes keywords as input and outputs sentences that include those keywords.

#### <span id="page-14-1"></span>A.4 Evaluation Metrics

Accuracy is used for NLI and date arithmetic tasks. M-S tasks are evaluated using option-level EM and F1. FRC tasks (excluding date arithmetic) are assessed with token-level EM and F1. For CTG task, we take the average of multiple generation metrics, which are outlined as follows.

Metrics for SituatedGen Following Situated-Gen [\(Zhang and Wan,](#page-12-6) [2023\)](#page-12-6), we use BLEU-4 [\(Pap](#page-11-12)[ineni et al.,](#page-11-12) [2002\)](#page-11-12), METEOR [\(Banerjee and Lavie,](#page-9-7) [2005\)](#page-9-7), ROUGE-L [\(Lin,](#page-10-15) [2004\)](#page-10-15), CIDEr [\(Vedantam](#page-12-14) [et al.,](#page-12-14) [2015\)](#page-12-14), and MATCH [\(Zhang and Wan,](#page-12-6) [2023\)](#page-12-6) scores to metric the results of CTG.[3](#page-14-3)

The overall score is calculated as the sum of the above scores. We set the weight of CIDEr to 1/10 for balancing when summation.

S = BLEU-4 + METEOR + ROUGE-L + CIDER/10 + MATCH

As the overall score S does not represent a percentile, we proceed to normalize the models' scores to align with humans' relative performance levels.

# B Supplemental Materials

## <span id="page-14-2"></span>B.1 Models

ChatGPT-3.5/GPT-4 [\(Ouyang et al.,](#page-11-4) [2022;](#page-11-4) [Ope](#page-11-2)[nAI,](#page-11-2) [2023\)](#page-11-2) ChatGPT is a chat model aligned

<span id="page-14-3"></span><sup>3</sup>We utilize [pycocoevalcap](https://github.com/salaniz/pycocoevalcap ) package to calucate BLEU-4, METEOR, ROUGE-L, CIDEr.

<span id="page-15-2"></span>![](_page_15_Figure_0.jpeg)
<!-- Image Description: This circular diagram shows the distribution of data points across various categories in a temporal reasoning dataset. The concentric rings represent different task types (e.g., Time NLI, Event Temporal), with the innermost circle labeled "Symbolic." Each segment within a ring denotes a specific dataset or task, annotated with its size (number of instances). The diagram visually summarizes the dataset composition across multiple dimensions, useful for understanding the scope and balance of different subtasks within the paper's focus on temporal reasoning. -->

Symbolic Common Sense Event Temporal

Figure 7: The quantity and proportion of data for each task and its respective subtasks within TIMEBENCH.

through SFT and RLHF based on GPT-3 [\(Brown](#page-9-0) [et al.,](#page-9-0) [2020\)](#page-9-0). GPT-4 is an upgraded version of Chat-GPT with enhanced reasoning capabilities, making it the most powerful LLM. Unless otherwise stated, ChatGPT refers to*gpt-3.5-turbo-0613*and GPT-4 refers to*gpt-4-0613*.

Llama2/Vicuna-1.5 [\(Touvron et al.,](#page-11-3) [2023;](#page-11-3) [Chi](#page-9-4)[ang et al.,](#page-9-4) [2023\)](#page-9-4) LLaMA2 is an open foundation model trained on 2T tokens with efficient groupedquery attention [\(Ainslie et al.,](#page-9-8) [2023\)](#page-9-8). LLaMA2 chat is the official aligned model with SFT and RLHF, and Vicuna-1.5 is aligned with SFT only by the community[4](#page-15-3) .

Baichuan2 [\(Yang et al.,](#page-12-2) [2023a\)](#page-12-2) is an open foundation model pre-trained on 2.6T tokens, which is competitive with LLaMA2. Baichuan2-chat is the official aligned model with SFT and RLHF.

Mistral [\(Jiang et al.,](#page-10-3) [2023\)](#page-10-3) is a 7B open foundation model incorporating efficient grouped-query attention [\(Ainslie et al.,](#page-9-8) [2023\)](#page-9-8) and sliding windows attention [\(Beltagy et al.,](#page-9-9) [2020\)](#page-9-9). It achieves the strongest performance among models of its size, even surpassing LLaMA2-13B. Mistral-instruct is the officially aligned model with SFT only.

ChatGLM3 [\(Zeng et al.,](#page-12-3) [2023\)](#page-12-3) is an open-source bilingual LLM for Chinese and English, exhibiting competitive performance under 10B.

FLAN-T5 [\(Chung et al.,](#page-10-4) [2022\)](#page-10-4) is an open-source instruction model built on top of T5 [\(Raffel et al.,](#page-11-13) [2020\)](#page-11-13) through instruction fine-tuning.

# <span id="page-15-1"></span>B.2 Full Results

The overall score is derived from the average of all corresponding metrics. For brevity, we omit some F1 scores in tables in the main text. Please refer to Table [9](#page-18-0) for the full experimental results. The full results of SituatedGen can be found in Table [8.](#page-17-0)

# <span id="page-15-0"></span>B.3 Prompts

The prompt formats are showcased in Figure [9.](#page-20-0) The demonstrations can be found from Figure [10](#page-21-0) to [18.](#page-24-0)

<span id="page-15-3"></span><sup>4</sup><https://lmsys.org/>

<span id="page-16-1"></span>![](_page_16_Figure_0.jpeg)
<!-- Image Description: The image presents two sets of grouped bar charts comparing the performance of several large language models (GPT-4, GPT-3.5, LLaMA variants, Baichuan, Mistral, and ChatGLM) across three task categories (Symbolic, Commonsense, Event) and an overall average. Each bar represents a model's performance score (likely accuracy or F1-score) for a specific task. The top chart shows one evaluation metric, while the bottom chart displays a second, distinct metric. The purpose is to quantitatively compare the capabilities of different language models in reasoning tasks. -->

Figure 8: Performance comparison between state-of-the-art LLMs. Up: GPT-4/3.5 and alignment models under zero-shot setting. Down: GPT-4/3.5 and base models under few-shot setting.

<span id="page-16-0"></span>

| Dataset          | Format | #      | Challenges                              |
|------------------|--------|--------|-----------------------------------------|
| Symbolic         |        |        |                                         |
| TimeX Arith      | FRC    | 4,000  | TimeX Arithmetic                        |
| TimeX NLI        | NLI    | 6,965  | TimeX Causality                         |
| - Order          | -      | 2,213  | order                                   |
| - Duration       | -      | 2,332  | duration                                |
| - Conversion     | -      | 2,420  | duration + time unit conversion         |
| Commonsense      |        |        |                                         |
| MCTACO           | M-S    | 852    | Temporal Commonsense                    |
| TimeDial         | M-S    | 1,446  | Temporal Commonsense                    |
| DurationQA       | M-S    | 687    | Event Duration                          |
| SituatedGen      | CTG    | 115    | Temporal Commonsense                    |
| Event            |        |        |                                         |
| TimeQA           | FRC    | 1,000  | Context-based Reasoning                 |
| - Explicit       | -      | 500    | explicit, event-time reasoning          |
| - Implicit       | -      | 500    | implicit, event-time reasoning          |
| MenatQA          | FRC    | 1,599  | Implicit, Context-based Reasoning       |
| - Order          | -      | 400    | event-time reasoning                    |
| - Scope          | -      | 400    | event-time reasoning                    |
| - Counterfactual | -      | 400    | event-time reasoning                    |
| TempReason       | FRC    | 1,876  | Implicit, Fact-based Reasoning          |
| - l2 (e2t)       | -      | 839    | event-time reasoning                    |
| - l3 (e2e)       | -      | 1,037  | event-event reasoning                   |
| TRACIE           | NLI    | 500    | Implicit, Implied Event-Event Reasoning |
| In total         |        | 19,000 |                                         |

Table 7: The statistics, task formats and challenges in TIMEBENCH.

<span id="page-17-0"></span>

| Method            | BLEU-4 | METEOR | ROUGE-L | CIDEr  | MATCH | Overall | Norm  |
|-------------------|--------|--------|---------|--------|-------|---------|-------|
| Human             | 39.9   | 40.4   | 56.3    | 397    | 98.1  | 274.4   | 100.0 |
| GPT-4             | 8.23   | 31.27  | 28.84   | 38.45  | 90.41 | 162.59  | 59.25 |
| + FS              | 28.64  | 38.99  | 55.69   | 298.64 | 90.11 | 243.29  | 88.66 |
| GPT-3.5           | 13.38  | 30.12  | 35.91   | 125.41 | 78.76 | 170.70  | 62.21 |
| + FS              | 27.24  | 33.77  | 51.18   | 282.75 | 76.54 | 217.01  | 79.08 |
| LLaMA270b         | 5.15   | 13.62  | 15.83   | 22.07  | 31.79 | 68.60   | 25.00 |
| + FS              | 19.10  | 29.09  | 41.74   | 171.36 | 65.29 | 172.35  | 62.81 |
| LLaMA213b         | 4.66   | 21.43  | 20.80   | 17.72  | 61.62 | 110.28  | 40.19 |
| + FS              | 15.15  | 27.49  | 37.55   | 138.13 | 64.94 | 158.93  | 57.92 |
| LLaMA27b          | 2.77   | 13.46  | 14.69   | 14.34  | 34.83 | 67.18   | 24.48 |
| + FS              | 6.90   | 15.82  | 21.77   | 52.99  | 33.81 | 83.60   | 30.47 |
| Baichuan213b      | 8.33   | 25.86  | 30.07   | 82.63  | 70.63 | 143.15  | 52.17 |
| + FS              | 15.79  | 30.23  | 40.96   | 169.14 | 71.01 | 174.91  | 63.74 |
| Baichuan27b       | 5.17   | 21.99  | 23.73   | 44.80  | 59.85 | 115.22  | 41.99 |
| + FS              | 15.06  | 23.45  | 32.29   | 137.94 | 52.04 | 136.64  | 49.79 |
| Vicuna1.513b      | 7.73   | 26.35  | 29.15   | 69.16  | 71.91 | 142.06  | 51.77 |
| + FS              | 6.85   | 18.66  | 25.99   | 92.96  | 46.19 | 106.99  | 38.99 |
| Vicuna1.57b       | 6.29   | 24.34  | 26.91   | 46.90  | 68.84 | 131.07  | 47.77 |
| + FS              | 20.71  | 30.19  | 45.20   | 203.20 | 67.58 | 184.00  | 67.05 |
| FLAN-T5           | 16.20  | 24.43  | 29.38   | 95.17  | 56.38 | 135.91  | 49.53 |
| + FS              | 12.88  | 30.38  | 36.27   | 92.20  | 76.44 | 165.19  | 60.20 |
| Mistral7b         | 5.82   | 22.89  | 24.19   | 44.03  | 63.74 | 121.03  | 44.11 |
| + FS              | 18.96  | 29.02  | 43.15   | 185.61 | 63.24 | 172.93  | 63.02 |
| ChatGLM36b        | 6.56   | 21.11  | 21.96   | 41.48  | 53.02 | 106.80  | 38.92 |
| + FS              | 10.53  | 24.17  | 33.44   | 124.50 | 56.94 | 137.53  | 50.12 |
| LLaMA2†<br>70b    | 22.34  | 33.03  | 50.93   | 243.31 | 74.96 | 205.59  | 74.92 |
| LLaMA2†<br>13b    | 17.54  | 29.44  | 45.21   | 200.14 | 65.64 | 177.84  | 64.81 |
| LLaMA2†<br>7b     | 17.49  | 28.33  | 45.24   | 202.08 | 59.98 | 171.25  | 62.41 |
| Baichuan2†<br>13b | 17.86  | 29.75  | 44.28   | 198.83 | 66.35 | 178.12  | 64.91 |
| Baichuan2†<br>7b  | 15.30  | 27.54  | 41.80   | 171.59 | 62.40 | 164.20  | 59.84 |
| Mistral†<br>7b    | 14.54  | 27.39  | 41.72   | 168.89 | 59.42 | 159.96  | 58.30 |
| ChatGLM3†<br>6b   | 17.11  | 29.35  | 40.74   | 156.49 | 66.18 | 169.02  | 61.60 |

Table 8: Full results of SituatedGen. Aligned models are under zero-shot setting by default. The top-3 results are bold. Methods with † are base models without alignment, under few-shot setting. We consider human performance as 100 points and normalize models' results accordingly.

<span id="page-18-0"></span>

|                                           |                                                                                              | Symbolic                       |                              |                              |                                                              | Commonsense                                      |                                                        |                                                              |                              |                              |                              |                              |                              |                              | Event                        |                              |                              |                              |                              |                              |                              |                              | Overall                      |                              |                              |
|-------------------------------------------|----------------------------------------------------------------------------------------------|--------------------------------|------------------------------|------------------------------|--------------------------------------------------------------|--------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|
| Method                                    | s3<br>TimeXNLI<br>s2<br>s1                                                                   | Date Arith<br>Acc              | EM                           | DurationQA<br>F1             | McTACO<br>F1<br>EM                                           | TimeDial<br>EM                                   | SitGen<br>Norm<br>F1                                   | E-F1<br>E-EM                                                 | H-EM<br>TimeQA               | H-F1                         | S-EM                         | S-F1                         | O-EM                         | O-F1<br>MenatQA              | C-EM                         | C-F1                         | L2-EM                        | TempReason<br>L2-F1          | L3-EM                        | L3-F1                        | TRACIE Sym.<br>Acc           |                              | Comm.                        | Event                        | Avg.                         |
| Human                                     | 92.0<br>96.0<br>98.0                                                                         | 100.0                          | 64.0                         | 80.8                         | 87.1<br>75.8                                                 | 97.8                                             | 100.0<br>97.8                                          | 93.3<br>89.0                                                 | 87.0                         | 91.1                         | 82.0                         | 85.6                         | 84.0                         | 87.3                         | 76.0                         | 79.9                         | 96.0                         | 97.1                         | 94.0                         | 95.3                         | 82.5                         | 96.5                         | 91.4                         | 89.0                         | 91.5                         |
| + FS CoT<br>+ CoT<br>GPT-4<br>+ FS        | 50.7<br>60.0<br>64.0<br>53.3<br>76.0<br>76.0<br>73.3<br>84.0<br>78.6<br>80.0<br>92.0<br>85.3 | 100.0<br>100.0<br>98.0<br>92.0 | 35.0<br>35.0<br>51.0<br>42.0 | 59.2<br>64.8<br>58.1<br>55.1 | 80.0<br>82.6<br>88.3<br>72.3<br>61.2<br>67.0<br>77.6<br>68.0 | 72.0<br>65.0<br>85.0<br>79.0                     | 88.6<br>59.3<br>-<br>-<br>94.6<br>93.4<br>89.3<br>91.1 | 60.6<br>73.7<br>66.9<br>61.3<br>48.9<br>50.0<br>59.2<br>48.0 | 40.4<br>33.0<br>40.0<br>44.4 | 41.2<br>51.0<br>52.8<br>46.5 | 44.4<br>43.4<br>59.6<br>48.5 | 57.0<br>54.6<br>72.4<br>65.3 | 49.0<br>53.0<br>48.0<br>44.0 | 57.0<br>59.6<br>54.8<br>52.6 | 22.0<br>20.0<br>22.0<br>25.3 | 22.6<br>28.7<br>25.9<br>23.1 | 91.0<br>93.0<br>86.0<br>91.0 | 95.3<br>97.0<br>92.4<br>96.9 | 94.0<br>93.0<br>94.8<br>93.0 | 95.0<br>94.5<br>95.9<br>94.6 | 58.0<br>66.4<br>64.8<br>62.8 | 75.8<br>77.0<br>78.0<br>85.0 | 72.4<br>76.7<br>84.1<br>73.6 | 62.4<br>66.5<br>65.2<br>61.1 | 68.3<br>68.5<br>73.7<br>72.1 |
| + FS CoT<br>GPT-3.5<br>+ CoT<br>+ FS      | 31.2<br>33.6<br>31.6<br>36.6<br>67.6<br>64.8<br>68.4<br>71.8<br>45.4<br>33.6<br>52.0<br>51.6 | 97.0<br>71.0<br>63.6<br>84.4   | 19.2<br>12.4<br>42.8<br>20.8 | 23.2<br>67.7<br>41.2<br>50.5 | 68.6<br>45.1<br>43.5<br>21.4<br>34.1<br>28.1                 | 71.2 47.8 76.4<br>38.1 48.3 71.1<br>39.2<br>34.6 | 62.3<br>79.1<br>-<br>-<br>67.0<br>69.1                 | 70.8<br>64.4<br>68.0<br>66.1<br>60.5<br>52.5<br>53.8<br>56.5 | 29.5<br>29.0<br>37.9<br>37.5 | 35.4<br>48.4<br>47.0<br>35.1 | 36.5<br>35.8<br>37.8<br>38.1 | 40.9<br>39.7<br>43.2<br>42.5 | 43.5<br>37.5<br>38.5<br>37.5 | 43.9<br>42.9<br>51.6<br>41.7 | 21.0<br>24.0<br>16.0<br>33.0 | 22.9<br>26.3<br>17.9<br>37.8 | 73.6<br>32.0<br>86.2<br>77.7 | 81.2<br>57.6<br>84.7<br>89.9 | 54.2<br>70.0<br>68.0<br>61.8 | 73.8<br>78.0<br>76.6<br>68.1 | 57.4<br>52.0<br>55.0<br>50.2 | 60.3<br>50.8<br>53.9<br>61.1 | 62.6<br>73.6<br>45.1<br>50.1 | 53.3<br>48.3<br>55.6<br>56.7 | 57.4<br>48.3<br>59.7<br>56.6 |
| LLaMA270b<br>+ FS CoT<br>+ CoT<br>+ FS    | 32.0<br>30.0 66.0 28.0<br>38.0<br>63.0 40.0<br>47.0<br>42.0<br>44.0<br>49.0<br>54.0          | 78.5<br>53.5<br>62.0<br>69.5   | 12.7<br>8.0<br>1.3<br>8.0    | 59.2<br>61.2<br>55.2<br>57.3 | 68.9<br>66.5<br>67.1<br>62.1<br>23.0<br>21.0<br>13.0<br>21.5 | 10.0 57.0<br>9.0<br>6.0<br>6.0                   | 25.0<br>62.8<br>58.6<br>56.4<br>56.6                   | 31.4<br>50.9<br>40.8<br>51.1<br>28.0<br>17.0<br>41.0<br>36.6 | 31.0<br>13.0<br>16.0<br>34.0 | 40.6<br>20.0<br>42.4<br>19.5 | 28.0<br>8.0<br>5.0<br>8.0    | 18.9<br>12.2<br>16.4<br>38.6 | 11.0<br>17.0<br>19.0<br>8.0  | 16.6<br>12.7<br>19.9<br>29.3 | 18.0<br>18.0<br>18.0<br>9.0  | 12.0<br>20.8<br>18.7<br>21.9 | 50.0<br>12.0<br>34.0<br>77.0 | 63.5<br>37.5<br>52.2<br>83.1 | 39.0<br>20.0<br>31.0<br>65.0 | 54.5<br>40.5<br>74.7<br>41.1 | 48.0<br>51.0<br>51.0<br>57.0 | 50.4<br>44.4<br>47.8<br>56.6 | 52.5<br>61.0<br>61.8<br>57.9 | 36.8<br>28.2<br>33.8<br>49.7 | 44.3<br>53.2<br>44.1<br>39.1 |
| LLaMA213b<br>+ FS CoT<br>+ CoT<br>+ FS    | 34.0<br>38.0<br>60.0<br>50.0<br>49.0<br>50.0<br>57.0<br>55.0<br>30.0<br>36.0<br>43.0<br>37.0 | 22.5<br>20.5<br>33.0<br>6.0    | 12.0<br>4.0<br>7.3<br>9.0    | 39.2<br>38.5<br>46.8<br>49.5 | 40.6<br>14.0 51.7<br>45.6<br>11.0<br>8.5<br>8.0              | 10.0<br>10.0<br>15.0<br>8.0<br>66.6              | 57.9<br>40.2<br>-<br>-<br>35.4<br>36.9<br>62.3<br>44.5 | 61.9<br>34.2<br>46.0<br>58.7<br>46.0<br>45.0<br>24.0<br>35.0 | 21.0<br>30.0<br>17.0<br>21.0 | 38.9<br>18.4<br>25.4<br>30.5 | 28.0<br>20.0<br>11.0<br>34.0 | 40.9<br>25.9<br>46.7<br>46.1 | 23.0<br>18.0<br>23.0<br>5.0  | 32.5<br>14.6<br>36.5<br>36.1 | 18.0<br>21.0<br>22.0<br>7.0  | 26.9<br>33.6<br>33.3<br>16.5 | 43.0<br>43.0<br>54.0<br>72.0 | 58.0<br>80.8<br>53.1<br>68.1 | 55.0<br>56.0<br>50.0<br>54.0 | 69.4<br>68.4<br>64.8<br>66.2 | 49.0<br>47.0<br>47.0<br>50.0 | 33.9<br>32.5<br>45.1<br>43.8 | 42.6<br>54.0<br>46.5<br>43.1 | 46.6<br>47.3<br>38.3<br>46.0 | 42.6<br>42.4<br>43.9<br>45.5 |
| LLaMA27b<br>+ FS CoT<br>+ CoT<br>+ FS     | 30.0<br>33.0<br>60.0 34.0<br>51.0 36.0<br>53.0<br>44.0 50.0<br>39.0<br>44.0<br>38.0          | 13.0<br>11.0<br>14.5<br>5.0    | 11.0<br>2.7<br>2.7<br>4.0    | 35.0<br>39.3<br>62.8<br>42.8 | 41.0<br>40.0<br>65.6<br>64.7<br>25.0<br>4.0<br>4.5<br>8.0    | 13.0<br>1.0<br>1.0<br>8.0                        | 30.5<br>24.5<br>-<br>-<br>40.0<br>53.4<br>6.3<br>1.7   | 49.0<br>49.9<br>53.5<br>50.8<br>37.0<br>27.0<br>36.0<br>36.0 | 14.0<br>17.0<br>20.0<br>21.0 | 29.0<br>31.6<br>29.4<br>34.1 | 11.0<br>7.0<br>5.0<br>1.0    | 26.8<br>31.4<br>13.6<br>22.3 | 10.0<br>8.0<br>6.0<br>3.0    | 24.5<br>18.0<br>11.2<br>21.1 | 9.0<br>7.0<br>6.0<br>5.0     | 16.0<br>17.8<br>17.9<br>14.0 | 48.0<br>44.0<br>12.0<br>22.0 | 63.9<br>56.9<br>36.3<br>46.7 | 32.0<br>32.0<br>23.0<br>21.0 | 47.9<br>48.1<br>44.3<br>42.3 | 49.0<br>46.0<br>53.0<br>51.0 | 33.8<br>33.0<br>37.3<br>34.9 | 27.8<br>25.6<br>49.5<br>53.9 | 37.8<br>38.3<br>34.0<br>33.3 | 34.3<br>34.3<br>38.7<br>37.8 |
| Baichuan213b<br>+ FS CoT<br>+ CoT<br>+ FS | 41.0 61.0 37.0<br>31.0<br>40.0<br>45.0 54.0 48.0<br>57.0<br>59.0<br>40.0<br>43.0             | 12.5<br>10.0<br>42.5<br>47.0   | 24.7<br>10.7<br>4.0<br>3.3   | 52.0<br>44.6<br>62.1<br>44.4 | 70.2<br>63.4<br>61.9<br>68.8<br>20.0<br>27.5<br>27.0<br>18.5 | 15.0<br>13.0<br>18.0<br>15.0                     | 52.2<br>63.7<br>-<br>-<br>58.9<br>55.0<br>57.7<br>58.1 | 55.4<br>60.7<br>41.5<br>57.8<br>45.0<br>36.0<br>47.0<br>43.0 | 29.0<br>36.0<br>35.0<br>27.0 | 34.6<br>40.9<br>45.7<br>36.7 | 31.0<br>39.0<br>37.0<br>38.0 | 48.8<br>52.0<br>51.9<br>49.8 | 34.0<br>27.0<br>31.0<br>34.0 | 44.3<br>38.5<br>41.5<br>40.7 | 30.0<br>29.0<br>19.0<br>33.0 | 39.5<br>43.2<br>31.8<br>43.0 | 40.0<br>46.0<br>73.0<br>72.8 | 57.4<br>62.8<br>81.1<br>80.4 | 45.0<br>46.0<br>48.0<br>43.0 | 61.4<br>64.3<br>59.4<br>60.2 | 49.0<br>55.0<br>48.0<br>44.0 | 37.9<br>34.5<br>48.5<br>46.1 | 63.7<br>56.3<br>54.9<br>56.1 | 48.8<br>49.8<br>52.5<br>51.6 | 48.0<br>46.7<br>53.7<br>51.7 |
| Baichuan27b<br>+ FS CoT<br>+ CoT<br>+ FS  | 35.0 50.0 37.0<br>32.0<br>40.0 50.0 36.0<br>50.0 36.0<br>43.0<br>38.0<br>41.0                | 20.0<br>23.5<br>4.5<br>1.0     | 28.7<br>13.0<br>4.0<br>5.3   | 59.4<br>47.9<br>37.9<br>45.7 | 58.0<br>55.3<br>66.9<br>58.1<br>13.0<br>26.5<br>10.5<br>17.5 | 15.0<br>15.0<br>17.0<br>7.0                      | 42.0<br>49.8<br>-<br>-<br>44.2<br>53.0<br>39.2<br>54.3 | 60.7<br>51.2<br>41.5<br>53.5<br>26.0<br>41.0<br>45.0<br>36.0 | 20.0<br>28.0<br>30.0<br>29.0 | 34.7<br>38.8<br>43.0<br>42.1 | 20.0<br>29.0<br>27.0<br>42.0 | 35.2<br>39.9<br>37.8<br>52.5 | 19.0<br>23.0<br>23.0<br>25.0 | 31.2<br>33.2<br>35.7<br>39.3 | 18.0<br>10.0<br>20.0<br>6.0  | 20.4<br>29.3<br>20.4<br>31.0 | 22.0<br>21.0<br>40.0<br>57.0 | 43.4<br>41.2<br>57.4<br>70.1 | 29.0<br>29.0<br>37.0<br>39.0 | 47.7<br>47.2<br>53.0<br>60.2 | 55.0<br>54.0<br>51.0<br>49.0 | 31.6<br>28.5<br>36.5<br>37.6 | 49.9<br>46.7<br>57.3<br>47.7 | 38.6<br>44.8<br>49.5<br>42.1 | 39.7<br>39.4<br>45.8<br>46.0 |
| Vicuna1.513b<br>+ FS CoT<br>+ CoT<br>+ FS | 36.0<br>37.0<br>38.0<br>39.0<br>50.0<br>51.0<br>48.0 57.0<br>38.0 59.0<br>35.0<br>42.0       | 15.0<br>30.5<br>39.5<br>3.0    | 10.7<br>8.0<br>1.3<br>7.3    | 39.2<br>37.4<br>29.8<br>33.6 | 50.0<br>57.0<br>45.8<br>59.1<br>27.5<br>14.0<br>21.5<br>11.5 | 12.0 41.6<br>13.0 40.3<br>7.0<br>7.0             | 51.8<br>39.0<br>-<br>-<br>34.2<br>33.7                 | 60.4<br>56.9<br>59.5<br>58.3<br>43.0<br>44.0<br>45.0<br>47.0 | 29.0<br>31.0<br>23.0<br>27.0 | 37.0<br>36.4<br>25.9<br>30.7 | 38.0<br>16.0<br>38.0<br>39.0 | 46.8<br>38.2<br>42.6<br>48.1 | 22.0<br>25.0<br>26.0<br>31.0 | 37.4<br>37.7<br>41.4<br>35.9 | 17.0<br>13.0<br>18.0<br>26.0 | 23.2<br>20.4<br>31.2<br>20.1 | 14.0<br>31.0<br>51.0<br>71.0 | 49.0<br>61.8<br>77.5<br>42.1 | 13.0<br>29.0<br>28.0<br>53.0 | 43.6<br>42.6<br>65.5<br>49.1 | 46.0<br>51.0<br>56.0<br>52.0 | 34.0<br>33.3<br>43.4<br>43.9 | 46.1<br>37.8<br>42.5<br>41.6 | 42.3<br>43.6<br>50.1<br>42.1 | 39.0<br>43.3<br>46.7<br>41.1 |
| Vicuna1.57b<br>+ FS CoT<br>+ CoT<br>+ FS  | 43.0<br>36.0<br>37.0<br>35.0<br>37.0 58.0<br>50.0<br>43.0 57.0<br>54.0<br>36.0<br>35.0       | 5.0<br>1.5<br>8.5<br>8.0       | 1.3<br>1.3<br>3.3<br>2.7     | 44.6<br>37.2<br>40.4<br>39.4 | 49.2<br>52.5<br>42.1<br>10.0<br>9.5<br>8.5<br>5.5            | 47.5 10.0<br>6.0<br>9.0<br>7.0                   | 47.8<br>67.1<br>-<br>-<br>32.0<br>36.2<br>36.8<br>41.3 | 40.9<br>31.9<br>39.9<br>47.1<br>35.0<br>30.0<br>24.0<br>31.0 | 11.0<br>14.0<br>12.0<br>13.0 | 24.6<br>14.9<br>16.6<br>18.5 | 20.0<br>16.0<br>16.0<br>15.0 | 35.7<br>26.2<br>21.8<br>26.7 | 15.0<br>14.0<br>20.0<br>15.0 | 25.7<br>28.5<br>27.5<br>23.8 | 12.0<br>12.0<br>17.0<br>16.0 | 17.3<br>25.0<br>22.2<br>23.1 | 14.0<br>13.0<br>55.0<br>9.0  | 33.0<br>27.7<br>34.3<br>66.3 | 14.0<br>32.0<br>7.0<br>6.0   | 46.8<br>40.3<br>32.2<br>48.1 | 54.0<br>54.0<br>54.0<br>43.0 | 35.8<br>30.9<br>36.4<br>33.0 | 47.7<br>43.2<br>41.6<br>42.0 | 34.8<br>33.4<br>29.9<br>35.9 | 37.1<br>34.4<br>35.9<br>36.4 |
| FLANT511b<br>+ FS CoT<br>+ CoT<br>+ FS    | 43.0<br>45.0<br>43.0<br>46.0<br>63.0<br>56.0 66.0<br>65.0<br>54.0 68.0<br>53.0<br>53.0       | 0.0<br>0.0<br>3.5<br>3.5       | 4.0<br>4.7<br>4.0<br>4.0     | 52.0<br>50.2<br>49.7<br>50.7 | 65.0<br>64.0<br>65.8<br>14.0<br>15.5<br>13.0<br>14.5         | 11.0 43.7<br>63.4 13.0 42.7<br>13.0<br>9.0       | 60.2<br>49.5<br>-<br>-<br>35.0<br>47.7                 | 64.4<br>59.4<br>61.7<br>64.3<br>56.0<br>57.6<br>55.0<br>54.0 | 24.0<br>23.9<br>23.0<br>19.0 | 26.8<br>28.2<br>25.0<br>21.2 | 31.0<br>39.0<br>31.0<br>34.0 | 33.6<br>41.6<br>33.6<br>36.6 | 48.0<br>46.0<br>47.0<br>45.0 | 52.2<br>50.2<br>50.6<br>49.2 | 20.0<br>28.0<br>21.0<br>20.0 | 21.8<br>30.6<br>22.5<br>21.7 | 84.0<br>73.0<br>82.0<br>89.0 | 87.9<br>79.5<br>87.0<br>93.8 | 78.0<br>57.0<br>78.0<br>72.0 | 83.9<br>68.9<br>84.5<br>79.7 | 64.0<br>55.0<br>65.0<br>66.0 | 39.8<br>41.8<br>42.9<br>41.1 | 53.6<br>51.9<br>52.8<br>52.8 | 54.0<br>52.3<br>54.1<br>53.5 | 50.3<br>49.4<br>50.5<br>50.5 |
| Mistral7b<br>+ CoT<br>+ FS                | 50.0 43.0<br>35.0<br>35.0<br>56.0<br>51.0 57.0<br>47.0<br>38.0                               | 26.5<br>16.5<br>18.0           | 13.3<br>12.0<br>11.3         | 49.8<br>36.6<br>55.8         | 71.0<br>58.8<br>49.3<br>15.0<br>25.5<br>14.5                 | 13.0<br>6.0<br>8.0                               | 63.0<br>58.3<br>-<br>23.2<br>52.9<br>19.3              | 28.2<br>43.5<br>31.3<br>13.0<br>24.0<br>7.0                  | 11.0<br>12.0<br>5.0          | 21.4<br>22.4<br>23.9         | 4.0<br>8.0<br>4.0            | 24.3<br>21.1<br>21.3         | 14.0<br>7.0<br>7.0           | 22.3<br>24.9<br>21.2         | 12.0<br>4.0<br>7.0           | 21.7<br>25.6<br>23.0         | 23.0<br>2.0<br>5.0           | 39.6<br>34.0<br>48.9         | 23.0<br>1.0<br>4.0           | 31.6<br>31.2<br>44.9         | 51.0<br>61.0<br>57.0         | 41.6<br>36.4<br>40.3         | 60.7<br>47.5<br>35.1         | 30.0<br>31.4<br>35.5         | 37.3<br>33.5<br>43.0         |

|                                           | Symbolic                                                                         |                           |                           |                              | Commonsense                                              |                                                              |                        |                              |                              |                              |                              |                              |                              |                              | Event                        |                              |                                                              |              |                              |                                                              |              |                              |                              | Overall                      |                              |                              |
|-------------------------------------------|----------------------------------------------------------------------------------|---------------------------|---------------------------|------------------------------|----------------------------------------------------------|--------------------------------------------------------------|------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|--------------------------------------------------------------|--------------|------------------------------|--------------------------------------------------------------|--------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|
| + FS CoT<br>Method                        | 29.0 62.0 32.0<br>s3<br>TimeXNLI<br>s2<br>s1                                     | Date Arith<br>28.5<br>Acc | EM<br>9.3                 | DurationQA<br>46.6<br>F1     | 49.2<br>McTACO<br>F1<br>14.5<br>EM                       | 34.4<br>TimeDial<br>F1<br>EM<br>8.0                          | SitGen<br>Norm<br>-    | E-EM<br>13.0                 | TimeQA<br>E-F1<br>33.7       | H-EM<br>11.0                 | H-F1<br>25.3                 | S-EM<br>9.0                  | S-F1<br>26.4                 | MenatQA<br>O-EM<br>9.0       | O-F1<br>24.3                 | C-EM<br>9.0                  | L2-EM<br>C-F1<br>20.3                                        | 68.0         | TempReason<br>L2-F1<br>78.6  | L3-F1<br>57.4<br>L3-EM<br>42.0                               |              | TRACIE Sym.<br>50.0<br>Acc   | 37.9                         | Comm.<br>43.4                | Event<br>39.5                | Avg.<br>39.8                 |
| ChatGLM36b<br>+ FS CoT<br>+ CoT<br>+ FS   | 34.0<br>49.0 37.0<br>30.0<br>32.0 66.0 31.0<br>38.0 50.0<br>52.0<br>27.0<br>37.0 | 2.0<br>0.0<br>0.0<br>0.0  | 10.0<br>3.0<br>1.0<br>4.0 | 53.0<br>34.1<br>24.8<br>34.8 | 43.6<br>52.9<br>43.6<br>37.1<br>7.0<br>3.0<br>9.0<br>8.0 | 54.7<br>44.0<br>56.7<br>44.8<br>14.0<br>10.0<br>19.0<br>11.0 | 38.9<br>50.1<br>-<br>- | 20.0<br>24.0<br>11.0<br>25.0 | 41.2<br>41.7<br>19.6<br>43.3 | 14.0<br>10.0<br>13.0<br>19.0 | 31.7<br>25.4<br>17.0<br>27.5 | 25.0<br>27.0<br>25.0<br>23.0 | 33.8<br>34.6<br>35.0<br>30.2 | 17.0<br>22.0<br>24.0<br>19.0 | 26.0<br>30.4<br>25.7<br>28.1 | 24.0<br>35.0<br>20.0<br>36.0 | 42.0<br>28.0<br>27.0<br>50.0<br>32.2<br>41.2<br>25.6<br>43.0 |              | 57.0<br>62.8<br>44.5<br>46.5 | 54.0<br>52.0<br>56.0<br>53.3<br>30.0<br>27.0<br>33.0<br>34.0 |              | 50.0<br>48.0<br>54.0<br>48.0 | 31.0<br>28.3<br>29.8<br>32.3 | 35.6<br>52.7<br>43.3<br>40.8 | 39.4<br>35.2<br>40.7<br>42.1 | 39.0<br>38.2<br>39.2<br>35.7 |
| LLaMA2-Base70b<br>+ CoT                   | 55.0 61.0 37.0<br>52.0 73.0 39.0                                                 | 82.0<br>79.5              | 40.0<br>32.6              | 67.4<br>62.3                 | 59.0 85.3 63.0 82.7<br>47.0 79.1 25.0 61.1               |                                                              | 74.9                   | 57.0<br>55.0                 | 66.7<br>64.3                 | 36.0<br>34.0                 | 48.3<br>43.0                 | 52.0<br>50.0                 | 61.4<br>57.7                 | 35.0<br>37.0                 | 45.2<br>42.5                 | 25.0<br>44.0                 | 33.8<br>53.1                                                 | 78.0<br>82.0 | 85.2<br>87.5                 | 80.0<br>76.0                                                 | 85.4<br>81.6 | 61.0<br>67.0                 | 60.9<br>58.8                 | 77.6<br>67.5                 | 62.4<br>60.5                 | 64.4<br>63.0                 |
| LLaMA2-Base13b<br>+ CoT                   | 50.0 54.0 30.0<br>40.0 61.0 37.0                                                 | 29.5<br>52.0              | 19.3<br>25.3              | 59.3<br>53.3                 | 26.5 66.0 20.0 55.6<br>26.0 68.8 11.0 40.8               |                                                              | 64.8<br>-              | 48.0<br>46.0                 | 59.4<br>59.3                 | 34.0<br>37.0                 | 48.6<br>49.1                 | 41.0<br>49.0                 | 49.6<br>58.4                 | 38.0<br>34.0                 | 43.4<br>43.8                 | 34.0<br>38.0                 | 37.5<br>44.1                                                 | 68.0<br>70.0 | 78.7<br>78.0                 | 49.0<br>55.0                                                 | 68.2<br>62.7 | 58.0<br>58.0                 | 47.5<br>40.9                 | 59.9<br>56.3                 | 57.4<br>54.7                 | 52.6<br>54.5                 |
| LLaMA2-Base7b<br>+ CoT                    | 26.0 50.0 30.0<br>37.0 52.0 36.0                                                 | 20.0<br>25.5              | 19.3<br>21.3              | 56.9<br>54.5                 | 20.0 59.6 15.0 45.2<br>26.5 67.0 16.0 41.9               |                                                              | 62.4<br>-              | 44.0<br>32.0                 | 54.4<br>45.6                 | 30.0<br>27.0                 | 45.3<br>36.1                 | 42.0<br>41.0                 | 49.8<br>50.9                 | 34.0<br>30.0                 | 41.9<br>38.0                 | 30.0<br>51.0                 | 35.8<br>57.3                                                 | 50.0<br>45.0 | 64.0<br>59.7                 | 36.0<br>37.0                                                 | 57.7<br>53.3 | 49.0<br>50.0                 | 37.6<br>31.5                 | 55.4<br>55.3                 | 49.2<br>49.4                 | 47.4<br>46.3                 |
| Baichuan2-Base13b 38.0 48.0 33.0<br>+ CoT | 50.0 56.0 34.0                                                                   | 42.5<br>47.0              | 20.7<br>29.3              | 62.0<br>54.8                 | 42.5 73.0 11.0 45.7<br>22.5 69.3 12.0 43.8               |                                                              | 64.9<br>-              | 50.0<br>46.0                 | 59.4<br>58.2                 | 40.0<br>39.0                 | 54.2<br>49.6                 | 42.0<br>39.0                 | 52.7<br>49.8                 | 31.0<br>34.0                 | 38.0<br>40.1                 | 13.0<br>37.0                 | 21.4<br>45.6                                                 | 68.0<br>73.0 | 77.3<br>81.3                 | 50.0<br>46.0                                                 | 65.6<br>63.5 | 54.0<br>60.0                 | 40.4<br>46.8                 | 59.6<br>58.4                 | 52.6<br>56.3                 | 54.2<br>51.3                 |
| Baichuan2-Base7b<br>+ CoT                 | 27.0 66.0 41.0<br>30.0 56.0 34.0                                                 | 32.5<br>34.0              | 28.0<br>23.3              | 59.8<br>57.0                 | 33.0 69.5 12.0 44.5<br>34.5 69.4                         | 34.3<br>5.0                                                  | 59.8<br>-              | 40.0<br>41.0                 | 53.8<br>51.2                 | 35.0<br>31.0                 | 50.2<br>40.7                 | 41.0<br>38.0                 | 49.6<br>46.4                 | 33.0<br>26.0                 | 38.5<br>32.6                 | 18.0<br>41.7                 | 22.9<br>46.3                                                 | 49.0<br>46.0 | 65.9<br>61.5                 | 34.0<br>43.8                                                 | 51.0<br>64.1 | 55.0<br>53.0                 | 41.6<br>38.5                 | 57.0<br>55.8                 | 48.4<br>49.5                 | 48.5<br>48.1                 |
| Mistral-Base7b<br>+ CoT                   | 48.0 53.0 38.0<br>57.0 63.0 35.0                                                 | 41.0<br>54.0              | 34.0<br>30.0              | 61.8<br>61.8                 | 42.5 76.2 35.0 61.8<br>42.0 45.7 29.0 57.3               |                                                              | 58.3<br>-              | 43.0<br>51.0                 | 55.9<br>60.4                 | 30.0<br>30.0                 | 45.3<br>46.2                 | 37.0<br>48.0                 | 49.4<br>57.2                 | 38.0<br>37.0                 | 47.9<br>47.8                 | 37.0<br>24.0                 | 45.5<br>33.2                                                 | 68.0<br>60.0 | 76.7<br>65.9                 | 64.0<br>58.0                                                 | 74.8<br>67.9 | 53.0<br>57.0                 | 45.0<br>52.3                 | 64.5<br>54.9                 | 56.1<br>54.5                 | 55.4<br>54.0                 |
| ChatGLM3-Base6b<br>+ CoT                  | 48.0 70.0 32.0<br>47.0 68.0 32.0                                                 | 35.0<br>46.0              | 3.3<br>8.7                | 51.8<br>53.9                 | 13.5 62.6 11.0 55.0<br>15.5 64.3 13.0 56.5               |                                                              | 61.6                   | 50.0<br>45.0                 | 57.2<br>52.5                 | 24.0<br>23.0                 | 26.3<br>24.5                 | 30.0<br>30.0                 | 35.4<br>35.0                 | 38.0<br>37.0                 | 41.5<br>40.2                 | 22.0<br>22.0                 | 22.5<br>22.5                                                 | 67.0<br>72.0 | 76.4<br>79.4                 | 35.0<br>42.0                                                 | 55.9<br>60.3 | 58.0<br>54.0                 | 48.3<br>46.3                 | 58.2<br>57.8                 | 46.7<br>46.1                 | 49.3<br>49.1                 |
|                                           |                                                                                  |                           |                           |                              |                                                          |                                                              |                        |                              |                              |                              |                              |                              |                              |                              |                              |                              |                                                              |              |                              |                                                              |              |                              |                              |                              |                              |                              |

Table 9: Full results of TimeBench. Aligned models are under zero-shot setting by default. Methods with † are base models without alignment, under few-shot setting, thus incomparable with other methods. We consider human performance as 100 points and normalize models' results accordingly.

<span id="page-20-0"></span>

| DURATIONQA, MCTACO                                                                                                                                                                                                                                                                             |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Answer the following question, select all the possible correct options, and each question has at least one correct option.<br>Context: {}<br>Question: {}<br>Options: {}<br>Answer:                                                                                                            |
| TIMEDIAL                                                                                                                                                                                                                                                                                       |
| There is a two-person dialogue with several options.<br>Choose all appropriate options to substitute the <mask> in the dialogue, and each question has at least one correct<br/>option.<br/>Dialogue: {}<br/>Options: {}<br/>Answer:</mask>                                                    |
| TRACIE                                                                                                                                                                                                                                                                                         |
| Read the following story and hypothesis, determine whether the hypothesis can be inferred from the story.<br>You need to understand the implicit temporal relationships between events to make judgments.<br>Story: {}<br>Hypothesis: {}<br>Options: A. Entailment B. Contradiction<br>Answer: |
| SITUATEDGEN                                                                                                                                                                                                                                                                                    |
| Generate a pair of contrastive sentences with the given set of keywords.<br>Keywords: {}                                                                                                                                                                                                       |
| DATE ARITHMETIC                                                                                                                                                                                                                                                                                |
| Question: {}? Answer:                                                                                                                                                                                                                                                                          |
| TIMEQA                                                                                                                                                                                                                                                                                         |
| I will give you a question with context.<br>You need to answer my question based on the context.<br>If you can infer the answer from the context, then output your answer. Otherwise, if there is no answer, output [unan<br>swerable].<br>Context: {}<br>Question: {}<br>Answer:              |
| TEMPREASON                                                                                                                                                                                                                                                                                     |
| I will give you a question with context.<br>You need to answer my question based on the context.<br>Context: {}<br>Question: {}<br>Answer:                                                                                                                                                     |
| MENATQA                                                                                                                                                                                                                                                                                        |
| Get answers for the question based on the contxt, where answers derived from substrings in the context or categorized<br>as [unanswerable].<br>Context: {}<br>Question: {}<br>Answer:                                                                                                          |
| TIMEX-NLI                                                                                                                                                                                                                                                                                      |
| Read the following statements about time and determine if the hypothesis can be inferred from the premise.<br>Premise: {}<br>Hypothesis: {}<br>Options: A. Entailment B. Contradiction C. Neutral<br>Answer:                                                                                   |

Figure 9: Zeroshot instructions and input formats.

<span id="page-21-0"></span>Answer the following question, select all the possible correct options, and each question has at least one correct option. Premise: On Wednesday, they got married. Hypothesis: Before Friday, they got married. Options: A. Entailment B. Contradiction C. Neutral Answer: Wednesday is before Friday. As a result, we can infer that if something happens on Wednesday, it definitely happens before Friday. Therefore, the answer is A. Entailment. Premise: We went to Disneyland on Monday. Hypothesis: We went to Disneyland after Wednesday. Options: A. Entailment B. Contradiction C. Neutral Answer: Monday is before Wednesday. As a result, We can infer that if something happens on Monday, it definitely can not happen after Wednesday. Therefore, the answer is B. Contradiction. Premise: The failing company issued major layoffs after Tuesday. Hypothesis: The failing company issued major layoffs after Thursday. CoT Demonstration of TIMEX-NLI (3-shot, order)

Options: A. Entailment B. Contradiction C. Neutral Answer: Tuesday is before Thursday. If something happened after Tuesday, we cannot be certain whether it occurred after Thursday. Therefore, the answer is C. Neutral.

Figure 10: Chain-of-Thought demonstrations of TimeX-NLI (s1-order).

## CoT Demonstration of DATE ARITHMETIC (4-shot)

Question: What is the time 4 year and 1 month after Apr, 2000? Answer: First, 4 years after 2000 is 2004. Next, 1 month after April is May. Therefore, 4 year and 1 month after Apr, 2000 is May, 2004.

Question: What is the time 3 year and 4 month before Jun, 1840? Answer: First, subtracting 3 years from 1840 gives 1837. Next, subtracting 4 months from June gives February. Therefore, 3 year and 4 month before Jun, 1840 is Feb, 1837.

Question: What is the time 7 year and 11 month after Feb, 1819? Answer: First, 7 years after 1819 is 1826. Next, 11 months after February is January of the next year. Therefore, 7 years and 11 months after Feb, 1819 is Jan, 1827.

Question: What is the time 6 year and 9 month before Jan, 1234? Answer: First, subtracting 6 years from 1234 gives 1228. Next, subtracting 9 months from January gives April of the previous year. Therefore, 6 year and 9 month before Jan, 1234 is Apr, 1227.

Figure 11: Chain-of-Thought demonstrations of Date Arithmetic.

### CoT Demonstration of TRACIE (4-shot)

Read the following story and hypothesis, determine whether the hypothesis can be inferred from the story. You need to understand the implicit temporal relationships between events to make judgments

......

Story: Joe was a police officer. Joe was patrolling the streets of the city in his cruiser. Suddenly, Joe was alerted ¨ to a crime happening near him by dispatch.¨Joe responded to the scene and found a bank robber fleeing on foot. Joe arrested the criminal and was promoted.

Hypothesis: Joe put on his police uniform. starts after Joe arrest the criminal

Options: A. Entailment B. Contradiction

Answer: From the story we know Joe was patrolling. In the work state, Joe has already put on the police uniform. So we can infer that Joe put on his police uniform before arresting the criminal. This conflicts with hypothesis. Therefore, the answer is B. Contradiction.

Figure 12: Chain-of-Thought demonstrations of TRACIE.

#### CoT Demonstration of DURATIONQA (4-shot)

Answer the following question, select all the possible correct options, and each question has at least one correct option.

......

Context: actually i have an project on it so please give me as much as you have information about migratory birds in punjab

Question: How long did it take for them to have information about migratory birds in punjab?

Options: A. several months B. 12 weeks C. a few minutes D. almost instantly

Answer: This is a conversation scenario. In the conversation, providing relevant information about migratory birds in punjab to him is in real-time and takes very little time. Therefore, the answer is C. a few minutes, D. almost instantly.

Context: Hope she stops laying eggs because she will get really skinny !

Question: How long did it take for her to lay eggs?

Options: A. 1 week B. 22 hours C. 2 years D. 4 years

Answer: According to commonsense knowledge, the time it takes for birds to lay eggs typically varies from one day to several days. Therefore, the answer is A. 1 week, B. 22 hours.

Figure 13: Chain-of-Thought demonstrations of DurationQA.

# CoT Demonstration of MCTACO (4-shot)

Answer the following question, select all the possible correct options, and each question has at least one correct option.

......

Context: She ordered the tastiest kind of each vegetable and the prettiest kind of each flower.

Question: How often does she order vegetables and flowers?

Options: A. once a second B. three days a week C. every 10 centuries D. once a week

Answer: According to commonsense knowledge, ordering vegetables and flowers typically happens on a regular basis, usually every few days. Therefore, the answer is B. three days a week, D. once a week.

Context: Wallace, 38, called Gastonia home from the age of 8 until she graduated from Hunter Huss High School in 1983.

Question: When did Wallace wake up for high school?

Options: A. at 6 am B. at 1 am C. 7:00 AM D. at 6 pm

Answer: According to commonsense knowledge, waking up for high school typically happens in the morning, usually between 6 AM and 8 AM. Therefore, the answer is A. at 6 am, C. 7:00 AM.

Figure 14: Chain-of-Thought demonstrations of MCTACO.

## CoT Demonstration of TIMEDIAL (4-shot)

There is a two-person dialogue with several options.

Choose all appropriate options to substitute the <mask> in the dialogue, and each question has at least one correct option.

......

### Dialogue:

A:What schools have you attended ?

B: I finished Young Primary School in 1998 , and entered Xi ' an Middle School that same September . I graduated from there in <MASK> , and that September I entered Wuhan University , where I'm studying now .

A: How do you think the education you have received will contribute to your work in this company ?

B: I think I have a good understanding of fundamentals in the areas your company deals with , and I can go on from here to build up the specific skills and knowledge I need to do my job well .

A: Your graduation thesis was on Medical Application of Laser , right ? What were your conclusions ?

B: Yes . I did some work on that , and I found out some really interesting things about the conductivity of liquid helium . I was sure I had a great discovery until my teacher told me the same discovery already made twenty years ago . I think the most important thing , I learnt though , was the importance of keeping good records . Options: A. 1998 B. July of 2004 C. March of 2003 D. twenty years ago

Answer: Based on the dialogue, B entered middle school in Sep 1998. According to commonsense knowledge, it

usually takes around 6 years from entering middle school to graduating from high school (and entering university). Adding 6 years to 1998 would be 2004, so the answer should be around the year 2004. Therefore, the answer is B. July of 2004, C. March of 2003.

Figure 15: Chain-of-Thought demonstrations of TimeDial.

#### CoT Demonstration of TIMEQA, MENATQA (2-shot, implicit)

I will give you a question with context.

You need to answer my question based on the context.

If you can infer the answer from the context, then output your answer. Otherwise, if there is no answer, output [unanswerable]

......

Context: Theo-Ben Gurirab Theo-Ben Gurirab ( 23 January 1938 2013 14 July 2018 ) was a Namibian politician ˘ who served in various senior government positions . He served as the second Prime Minister of Namibia from 28 August 2002 to 20 March 2005 , following the demotion and subsequent resignation of Hage Geingob . Previously he was the countrys first Minister of Foreign Affairs from 1990 to 2002 , and was President of the United Nations General Assembly from 1999 to 2000 . He was Speaker of the National Assembly of Namibia from 2005 to 2015 , when he was replaced by Peter Katjavivi . Gurirab ultimately resigned from politics in 2015 . Death . Gurirab died at a Windhoek hospital on 14 July 2018 of natural causes . He is buried at Heroes Acre .

Question: Theo-Ben Gurirab took which position after Jan 2007?

Answer: Based on the context, we can summarize the following facts: Theo-Ben Gurirab served as second Prime Minister of Namibia from August 2002 to March 2005. Prior to that, he was the countrys first Minister of Foreign Affairs from 1990 to 2002 and and was President of the United Nations General Assembly from 1999 to 2000. From 2005 to 2015, he held the position of Speaker of the National Assembly of Namibia. He resigned from politics in 2015 and passed away in July 2018. According to the aforementioned facts, he took the position of Speaker of the National Assembly of Namibia in January 2007. Therefore, the answer is Speaker of the National Assembly of Namibia.

Figure 16: Chain-of-Thought demonstrations of TimeQA, MenatQA, implicit reasoning.

#### CoT Demonstration of TEMPREASON (4-shot, event-time)

I will give you a question with context. You need to answer my question based on the context.

......

Context (facts): Gian Piero Gasperini is the head coach of Atalanta B.C. from Jun, 2016 to Dec, 2022. Edoardo Reja is the head coach of Atalanta B.C. from Mar, 2015 to Jun, 2016. Stefano Colantuono is the head coach of Atalanta B.C. from Jun, 2010 to Mar, 2015. Bortolo Mutti is the head coach of Atalanta B.C. from Jan, 2010 to Jun, 2010. Emiliano Mondonico is the head coach of Atalanta B.C. from Jul, 1987 to Jun, 1990. Marcello Lippi is the head coach of Atalanta B.C. from Jul, 1992 to Jun, 1993. Angelo Gregucci is the head coach of Atalanta B.C. from Jul, 2009 to Sep, 2009. Luigi Delneri is the head coach of Atalanta B.C. from Jul, 2007 to Jun, 2009. Ottavio Bianchi is the head coach of Atalanta B.C. from Jul, 1981 to Jun, 1983. Antonio Conte is the head coach of Atalanta B.C. from Sep, 2009 to Jan, 2010. Nedo Sonetti is the head coach of Atalanta B.C. from Jul, 1983 to Jun, 1987. Valter Bonacina is the head coach of Atalanta B.C. from Jan, 2010 to Jan, 2010. Question: Who was the head coach of the team Atalanta B.C. in Feb, 2016? Answer: According to the context, Edoardo Reja was the head coach of Atalanta B.C. from Mar, 2015 to Jun, 2016. In Feb 2016, the head coach of the team Atalanta B.C. is Edoardo Reja. Therefore, the answer is Edoardo Reja.

Figure 17: Chain-of-Thought demonstrations of TempReason, event-time reasoning.

#### CoT Demonstration of TEMPREASON (4-shot, event-event)

<span id="page-24-0"></span>I will give you a question with context.

You need to answer my question based on the context.

......

Context (facts): Nicholas Macpherson holds the position of Member of the House of Lords from Oct, 2016 to Dec, 2022.

Nicholas Macpherson holds the position of Principal Private Secretary to the Chancellor of the Exchequer from Jan, 1993 to Jan, 1997.

Nicholas Macpherson holds the position of Permanent Secretary to the Treasury from Aug, 2005 to Jan, 2016.

Question: Which position did Nicholas Macpherson hold before Member of the House of Lords?

Answer: According to the context, Nicholas Macpherson holds the position of Permanent Secretary to the Treasury from Aug, 2005 to Jan, 2016. Afterthat, Nicholas Macpherson holds the position of Member of the House of Lords from Oct, 2016 to Dec, 2022. Nicholas Macpherson hold the position of Permanent Secretary to the Treasury before Member of the House of Lords. Therefore, the answer is Permanent Secretary to the Treasury."

Figure 18: Chain-of-Thought demonstrations of TempReason, event-event reasoning.
