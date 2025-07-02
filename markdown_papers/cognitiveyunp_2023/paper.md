---
cite_key: "cognitiveyunp_2023"
title: "ForecastTKGQuestions: A Benchmark for Temporal Question Answering and Forecasting over Temporal Knowledge Graphs"
authors: "cognitive.yunp, zhmen, lia, hanzhen, Volker.Tres"
year: 2023
doi: "10.48550/arXiv.2208.06501"
url: "https://arxiv.org/abs/2208.06501"
relevancy: "High"
tldr: "Novel benchmark dataset and forecasting-focused temporal knowledge graph question answering framework"
insights: "Proposes ForecastTKGQA model that employs TKG forecasting module for future inference, addresses limitation that existing TKGQA methods perform poorly on forecasting questions and struggle with yes-no and fact reasoning questions"
summary: "This paper addresses limitations in existing temporal knowledge graph question answering (TKGQA) methods by introducing ForecastTKGQuestions, a large-scale benchmark dataset for temporal question answering and forecasting. The research identifies that state-of-the-art TKGQA methods perform poorly on forecasting questions and are unable to answer yes-no questions and fact reasoning questions. The dataset includes three types of questions: entity prediction, yes-no, and fact reasoning questions, with the constraint that QA models can only access TKG information before the timestamp annotated in the question. The proposed ForecastTKGQA model employs a TKG forecasting module for future inference to answer all three question types."
research_question: "How to develop temporal knowledge graph question answering systems that can effectively answer future-oriented questions using only historical knowledge graph information?"
methodology: "ForecastTKGQA model with TKG forecasting module for future inference; ForecastTKGQuestions benchmark dataset with three question types; experimental evaluation focusing on forecasting capabilities; comprehensive analysis of existing TKGQA method limitations"
key_findings: "ForecastTKGQA outperforms recent TKGQA methods on entity prediction; demonstrates effectiveness across all three question types; identifies significant performance gaps in existing methods for forecasting questions"
limitations: "Limited to specific temporal knowledge graph domains; evaluation focused primarily on structured temporal queries; computational complexity of forecasting module not fully characterized"
conclusion: "Demonstrates importance of forecasting capabilities in temporal knowledge graph question answering and provides foundation for future research in temporal reasoning systems"
future_work: "Expand benchmark to more diverse temporal domains; develop more sophisticated forecasting techniques; investigate real-world applications of temporal question answering"
implementation_insights: "Addresses critical gap in temporal knowledge graph question answering; provides foundation for future research in temporal reasoning; demonstrates practical approach to future-oriented reasoning"
tags:
  - "Temporal Knowledge Graphs"
  - "Question Answering"
  - "Forecasting"
  - "ISWC 2023"
  - "Temporal Reasoning"
---

# ForecastTKGQuestions: A Benchmark for Temporal Question Answering and Forecasting over Temporal Knowledge Graphs

Zifeng Ding ⋆ 1 , 2 , Zongyue Li ⋆ 1 , 3 , Ruoxia Qi ⋆ 1 , Jingpei Wu 1 , Bailan He 1 , 2 , Yunpu Ma 1 , 2 , Zhao Meng 4 , Shuo Chen 1 , 2 , Ruotong Liao 1 , 3 , Zhen Han( ) 1 , and Volker Tresp( ) 1

<sup>1</sup> LMU Munich, Geschwister-Scholl-Platz 1, 80539 Munich, Germany <sup>2</sup> Siemens AG, Otto-Hahn-Ring 6, 81739 Munich, Germany

<sup>3</sup> Munich Center for Machine Learning (MCML), Munich, Germany

<sup>4</sup> ETH Z¨urich, R¨amistrasse 101, 8092 Z¨urich, Switzerland {zifeng.ding, ruoxia.qi, bailan.he, shuo.chen }@campus.lmu.de, {zongyue.li, jingpei.wu }@outlook.com, cognitive.yunpu@gmail.com, zhmeng@ethz.ch, liao@dbs.ifi.lmu.de, hanzhen02111@hotmail.com, Volker.Tresp@lmu.de

Abstract. Question answering over temporal knowledge graphs (TKGQ A) has recently found increasing interest. Previous related work aims to develop QA systems that answer temporal questions based on the facts from a fixed time period, where a temporal knowledge graph (TKG) spanning this period can be fully used for answer inference. In realworld scenarios, however, it is also common that given the knowledge until now, we wish the TKGQA systems to answer the questions asking about the future. As humans constantly seek plans for the future, building forecasting TKGQA systems is important. In this paper, we propose a novel task: forecasting TKGQA, and propose a coupled largescale TKGQA benchmark dataset, i.e., ForecastTKGQuestions. It includes three types of forecasting questions, i.e., entity prediction, yesunknown, and fact reasoning questions. For every forecasting question, a timestamp is annotated and QA models can only have access to the TKG information before it for answer inference. We find that previous TKGQA methods perform poorly on forecasting questions, and they are unable to answer yes-unknown and fact reasoning questions. To this end, we propose ForecastTKGQA, a TKGQA model that employs a TKG forecasting module for future inference. Experimental results show that ForecastTKGQA performs well in answering forecasting questions.

# 1 Introduction

Knowledge graphs (KGs) model factual information by representing every fact with a triplet, i.e., (s, r, o), where s , o , r, are the subject entity, the object entity, and the relation between s and o, respectively. To adapt to the ever-evolving

<sup>⋆</sup> Equal contribution.

knowledge, temporal knowledge graphs (TKGs) are introduced, where they additionally specify the time validity of every fact with a time constraint t (t is a timestamp), and represent each fact with a quadruple (s, r, o, t). Recently, TKG reasoning has drawn great attention. While a lot of methods focus on temporal knowledge graph completion (TKGC) where they predict missing facts at the observed timestamps, various recent methods pay more attention to forecasting the facts at unobserved future timestamps in TKGs.

Knowledge graph question answering (KGQA) is a task aiming to answer the natural language questions using a KG as the knowledge base (KB). KGQA requires QA models to extract answers from KGs, rather than retrieving or summarizing answers from the given text contexts. [\[24\]](#page-18-0) first introduces question answering over temporal knowledge graphs (TKGQA). It proposes a nonforecasting TKGQA dataset CronQuestions that takes a TKG as its underlying KB. Temporal reasoning techniques are required to answer these questions. Though [\[24\]](#page-18-0) manages to combine TKG reasoning with KGQA, it has limitations. Previous KGQA datasets, including CronQuestions, do not include yes-no and multiple-choice questions, while these two question types have been extensively studied in reading comprehension QA, e.g., [\[14\]](#page-17-0). Besides, the questions in CronQuestions are in a non-forecasting style, where all of them are based on the TKG facts that happen in a fixed time period, and an extensive TKG that is fully observable in this period can be used to infer the answers, making the answer inference less challenging. For example, the TKG facts from 2003, including (Stephen Robert Jordan, member of sports team, Manchester City, 2003 ), are all observable to answer the question Which team was Stephen Robert Jordan part of in 2003?. CronQuestions manages to bridge the gap between TKGC and KGQA, however, no previous work manages to combine TKG forecasting with KGQA, where only past TKG information can be used for answer inference.

In this work, we propose a novel task: forecasting question answering over temporal knowledge graphs (forecasting TKGQA), together with a coupled largescale dataset, i.e., ForecastTKGQuestions. We generate forecasting questions based on the Integrated Crisis Early Warning System (ICEWS) dataverse [\[3\]](#page-16-0), and label every question with a timestamp. To answer a forecasting question, QA models can only access the TKG information prior to the question timestamp. The contribution of our work is three-folded: (1) We propose forecasting TKGQA, a novel task aiming to test the forecasting ability of TKGQA models. To the best of our knowledge, this is the first work binding TKG forecasting with temporal KGQA; (2) We propose a large-scale benchmark TKGQA dataset: ForecastTKGQuestions. It contains three types of questions, i.e., entity prediction questions (EPQs), yes-unknown questions (YUQs), and fact reasoning questions (FRQs), where the last two types of questions have never been considered in previous KGQA datasets[5](#page-1-0) ; (3) We propose ForecastTKGQA, a model aiming to solve forecasting TKGQA. It employs a TKG forecasting module and a pre-trained language model (LM) for answer inference. Experimental results show that it achieves great performance on forecasting questions.

<span id="page-1-0"></span><sup>5</sup> YUQs are based on yes-no questions and FRQs are multiple-choice questions.

# 2 Preliminaries and Related Work

TKG Reasoning Let E, R and T denote a finite set of entities, relations, and timestamps, respectively. A TKG G is defined as a finite set of TKG facts represented by quadruples, i.e., G = {(s, r, o, t)|s, o ∈ E, r ∈ R, t ∈ T }. We define the TKG forecasting task (also known as TKG extrapolation) as follows. Assume we have a query (sq, rq, ?, tq) (or (?, rq, oq, tq)) derived from a target quadruple (sq, rq, oq, tq), and we denote all the ground-truth quadruples as F. TKG forecasting aims to predict the missing entity in the query, given the observed past TKG facts O = {(s<sup>i</sup> , r<sup>i</sup> , o<sup>i</sup> , ti) ∈ F|t<sup>i</sup> < tq}. Such temporal restriction is not imposed in TKG completion (TKGC, also known as TKG interpolation), where the observed TKG facts from any timestamp, including t<sup>q</sup> and the timestamps after tq, can be used for prediction. In recent years, there have been extensive works done for both TKGC [\[17,](#page-17-1)[16,](#page-17-2)[7\]](#page-16-1) and TKG forecasting [\[15,](#page-17-3)[10](#page-16-2)[,34,](#page-19-0)[9,](#page-16-3)[19\]](#page-18-1). We give a more detailed discussion about the forecasting methods. RE-NET [\[15\]](#page-17-3) employs an autoregressive architecture and models fact occurrence as a probability distribution conditioned on the temporal sequences of past related TKG information. TANGO [\[10\]](#page-16-2) employs neural ordinary differential equations to model temporal dependencies among graph information of different timestamps. CyGNet [\[34\]](#page-19-0) uses the copy-generation mechanism to extract hints from historical facts for forecasting. xERTE [\[9\]](#page-16-3) constructs a historical fact-based subgraph and selects prediction answers from it. TLogic [\[19\]](#page-18-1) is the first rule-based TKG forecasting method that learns temporal logical rules in TKGs and achieves superior results.

Question Answering over KGs Several datasets have been proposed for QA over non-temporal KGs, such as SimpleQuestions [\[2\]](#page-16-4), WebQuestionsSP [\[32\]](#page-19-1), ComplexWebQuestions [\[27\]](#page-19-2), MetaQA [\[33\]](#page-19-3), TempQuestions [\[12\]](#page-17-4), and TimeQuestions [\[13\]](#page-17-5). Among these datasets, only TempQuestions and TimeQuestions involve temporal questions that require temporal reasoning for answer inference, however, their associated KGs are non-temporal. CronQuestions [\[24\]](#page-18-0) contains questions based on a time-evolving TKG, i.e., Wikidata [\[30\]](#page-19-4). It is proposed for non-forecasting TKGQA. Two types of questions, i.e., entity prediction and time prediction questions, are included. To answer CronQuestions, Saxena et al. propose CronKGQA that uses TKGC methods, along with pre-trained LMs, which shows great effectiveness. A line of methods has been proposed on top of CronKGQA (TempoQR [\[20\]](#page-18-2), TSQA [\[26\]](#page-18-3), SubGTR [\[5\]](#page-16-5)), where they better distinguish question time scopes and reason over subgraphs. CronQuestions is proposed based on the idea of TKGC, and it does not support TKG forecasting and contains no forecasting question. One recent work, i.e., ForecastQA [\[14\]](#page-17-0), proposes a QA dataset fully consisting of forecasting questions. However, ForecastQA is not related to KGQA. In ForecastQA, answers to its questions are inferred from text contexts, while KGQA/TKGQA requires models to find the answers from the coupled KGs/TKGs without providing any additional text contexts. As a result, the methods designed for ForecastQA have no ability to address TKGQA. To this end, we propose ForecastTKGQuestions, <span id="page-3-0"></span>Table 1: (a) KGQA dataset comparison. Statistics are taken from [\[24\]](#page-18-0) and [\[13\]](#page-17-5). T% denotes the portion of temporal questions. (b) ForecastTKGQuestions statistics: number of questions of different types.

| (a)                  |   |   | (b)  |                             |                                               |                       |     |     |
|----------------------|---|---|------|-----------------------------|-----------------------------------------------|-----------------------|-----|-----|
| Datasets             |   |   |      | TKG Forecast T% # Questions |                                               | Train Valid Test      |     |     |
| MetaQA               | ✗ | ✗ | 0%   | 400k                        | 1-Hop Entity Prediction 211,564 36,172 33,447 |                       |     |     |
| TempQuestions        | ✗ | ✗ | 100% | 1271                        | 2-Hop Entity Prediction 85,088 12,266 10,765  |                       |     |     |
| TimeQuestions        | ✗ | ✗ | 100% | 16k                         | Yes-Unknown                                   | 251,537 42,884 39,695 |     |     |
| CronQuestions        | ✓ | ✗ | 100% | 410k                        | Fact Reasoning                                | 3,164                 | 514 | 517 |
| ForecastTKGQuestions | ✓ | ✓ | 100% | 727k                        | Total                                         | 551,353 91,836 84,424 |     |     |

aiming to bridge the gap between TKG forecasting and KGQA. We compare ForecastTKGQuestions with recent KGQA datasets in Table [1a.](#page-3-0)

Task Formulation: Forecasting TKGQA Forecasting TKGQA aims to test the forecasting ability of TKGQA models. It requires QA models to predict future facts based on the past TKG information. We formulate it as follows. Given a TKG G and a natural language question q generated based on a TKG fact whose valid timestamp is tq, forecasting TKGQA aims to predict the answer to q. We label every question q with tq, and constrain QA models to only use the TKG facts {(s<sup>i</sup> , r<sup>i</sup> , o<sup>i</sup> , ti)|t<sup>i</sup> < tq} before t<sup>q</sup> for answer inference. We propose three types of forecasting TKGQA questions, i.e., EPQs, YUQs, and FRQs. The answer to a EPQ is an entity e ∈ E. The answer to a YUQ is either yes or unknown. We formulate FRQs as multiple choices and thus the answer to an FRQ corresponds to a choice c. As a novel task, forecasting TKGQA requires models to have the ability of both natural language understanding (NLU) and future forecasting. Compared with it, the traditional TKG forecasting task does not require NLU and non-forecasting TKGQA does not consider future forecasting. Thus, previous methods for TKG forecasting[6](#page-3-1) , e.g., RE-Net [\[15\]](#page-17-3), and non-forecasting TKGQA, e.g., TempoQR [\[20\]](#page-18-2), are not suitable for solving forecasting TKGQA.

# 3 ForecastTKGQuestions

### 3.1 Temporal Knowledge Base

A subset from ICEWS [\[3\]](#page-16-0) is taken as the associated temporal KB for our proposed dataset. We construct a TKG ICEWS21 based on the events taken from the official website of the ICEWS weekly event data[7](#page-3-2) [\[3\]](#page-16-0). ICEWS contains sociopolitical events in english. We take the events from Jan. 1, 2021, to Aug. 31,

<span id="page-3-1"></span><sup>6</sup> Relation set is provided in TKG forecasting and these methods explicitly learn relation representations. However, TKG relations are not annotated in forecasting TKGQA questions. Only question texts are provided and these methods have no way to process. Therefore, we do not consider them in experiments on our new task.

<span id="page-3-2"></span><sup>7</sup> https://dataverse.harvard.edu/dataverse/icews

<span id="page-4-0"></span>Table 2: ICEWS21 TKG statistics. Ntrain, Nvalid, Ntest denote the number of TKG facts in Gtrain, Gvalid, Gtest, respectively. |E|, |R|, |T | denote ICEWS21's number of entities, relations, timestamps, respectively.

> Dataset Ntrain Nvalid Ntest |E| |R| |T | ICEWS21 252,434 43,033 39,836 20,575 253 243

2021, and extract TKG facts in the following way. For every ICEWS event, we generate a TKG fact (s, r, o, t). We take the content of Event Date as the timestamp t of the TKG fact. We take the contents of Source Name and Target Name as the subject entity s and the object entity o of the TKG fact, respectively. We take the content of Event Text as the relation type r of the fact. We present the dataset statistics of ICEWS21 in Table [2.](#page-4-0) We split ICEWS21 into three parts Gtrain = {(s, r, o, t) ∈ G|t ∈ [t0, t1) }, Gvalid = {(s, r, o, t) ∈ G|t ∈ [t1, t2) }, Gtest = {(s, r, o, t) ∈ G|t ∈ [t2, t3] }, where t0, t1, t2, t<sup>3</sup> correspond to 2021- 01-01, 2021-07-01, 2021-08-01 and 2021-08-31, respectively. We generate training/validation/test questions based on Gtrain/Gvalid/Gtest. We ensure that there exists no temporal overlap between every two of them, i.e., Gtrain ∩ Gvalid = ∅, Gtrain ∩ Gtest = ∅ and Gvalid ∩ Gtest = ∅. In this way, we prevent QA models from observing any information from the evaluation sets during training.

#### <span id="page-4-2"></span>3.2 Question Categorization and Generation

We generate natural language questions based on the TKG facts in ICEWS21 and propose our QA dataset ForecastTKGQuestions. Every relation type in ICEWS21 is coupled with a CAMEO code (specified in the CAMEO Code column of the ICEWS weekly event data). In the official CAMEO codebook (can be found in ICEWS database), each CAMEO code is explained with examples and detailed descriptions. We use the official CAMEO codebook provided in the ICEWS dataverse for aiding the generation of natural language relation templates. We create relation templates for 250 out of 253 relation types for question generation[8](#page-4-1) . For example, we create a relation template engage in material cooperation with for the relation type engage in material cooperation, not specified below. Questions in ForecastTKGQuestions are categorized into three categories, i.e., EPQs (including 1-hop and 2 hop EPQs), YUQs, and FRQs. We summarize the numbers of different types of questions in Table [1b.](#page-3-0) We use the relation templates to create natural language question templates for all types of questions (examples in Table [3\)](#page-5-0) which are used for question generation. All question templates are presented in our supplementary source code and explained in Appendix C.2. Same as previous KGQA datasets, e.g., CronQuestions, entity linking is considered as a separate problem and is not covered in our work. We assume complete entity and timestamp linking, and annotate the entities and timestamps in our questions. This applies to all three types of questions in our dataset. Distribution of question timestamps is specified in Appendix C.5.

<span id="page-4-1"></span><sup>8</sup> The rest three relation types are not ideal for question generation (Appendix C.1).

<span id="page-5-0"></span>Table 3: Example question templates of all types. s<sup>q</sup> and o<sup>q</sup> are the annotated question entities. t<sup>q</sup> is the annotated question timestamp. For FRQ, {sc}, {oc}, {tc} are annotated choice entities and timestamp. We only write one choice in FRQ template for brevity. Better understand with details in Section [3.2.](#page-4-2) Question Type Example Template

| 1-Hop EPQ | Who will {sq} engage in material cooperation with on {tq}?                                      |
|-----------|-------------------------------------------------------------------------------------------------|
| 2-Hop EPQ | Who will threaten a country, while {sq} criticizes or denounces this country on {tq}?           |
| YUQ       | Will {sq} make a pessimistic comment about {oq} on {tq}?                                        |
| FRQ       | Why will {sq} appeal to {oq} to meet or negociate on {tq}?<br>A: {sc} threaten {oc} on {tc}; B: |

Entity Prediction Questions We generate two groups of EPQs, i.e., 1-hop and 2-hop EPQs. Each 1-hop EPQ is generated from a single TKG fact, e.g., the natural language question Who will Sudan host on 2021-08-01? is based on (Sudan, host, Ramtane Lamamra, 2021-08-01 ). Question templates are used during question generation. The underlined parts in the question denote the annotated entities and timestamps for KGQA. We consider all the facts concerning the 250 selected relations and transform them into 1-hop EPQs. Each 2-hop EPQ is generated from two associated TKG facts in ICEWS21 where they contain common entities. An example is presented in Table [4.](#page-6-0) The answer to a 2-hop EPQ (Israel) corresponds to a 2-hop neighbor of its annotated entity (Iran) at the question timestamp (2021-08-02 ). We generate 2-hop questions by utilizing AnyBURL [\[21\]](#page-18-4), a rule-based KG reasoning model. We first split ICEWS21 into snapshots, where each snapshot Gt<sup>i</sup> = {(s, r, o, t) ∈ G|t = ti} contains all the TKG facts happening at the same timestamp. Then we train AnyBURL on each snapshot for rule extraction. We collect the 2-hop rules with a confidence higher than 0.5 returned by AnyBURL, and manually check if two associated TKG facts in each rule potentially have a logical causation or can be used to interpret positive/negative entity relationships. After excluding the rules not meeting this requirement, we create question templates based on the remaining ones. We search for the groundings in ICEWS21 at every timestamp, where each grounding corresponds to a 2-hop EPQ. See our source code for the complete list of extracted 2-hop rules and see Appendix C.3 for more EPQ generation details.

Yes-Unknown Questions Based on the idea of triple classification in KG reasoning[9](#page-5-1) , we introduce yes-no questions into KGQA. We then turn yes-no questions into yes-unknown questions because according to the Open World Assumption (OWA), the facts not observed in a given TKG are not necessarily wrong [\[8\]](#page-16-6). We generalize triple classification to quadruple classification[10](#page-5-2), and then translate TKG facts into natural language questions. We take answering YUQs as solving quadruple classification. For every TKG fact concerning the

<span id="page-5-1"></span><sup>9</sup> For a KG fact (s, r, o), triple classification aims to predict whether this fact is valid or not.

<span id="page-5-2"></span><sup>10</sup> Quadruple classification has never been studied in previous work. We define it as predicting whether a TKG fact (s, r, o, t) is valid or unknown, under OWA.

<span id="page-6-0"></span>Table 4: 2-hop EPQ example. To avoid overlong text, we use symbols to represent relations and timestamps in TKG facts and 2-hop rules. r<sup>1</sup> =accuse; r<sup>2</sup> =engage in diplomatic cooperation; t<sup>1</sup> =2021-08-02. m, n are two entities that are 2-hop neighbors of each other at t1. X is their common 1-hop neighbor at t1. The extracted rule describes the negative relationship between Iran and Israel.

| Associated TKG Facts 2-Hop Rule               |            | Generated 2-Hop Question                                         | Answer |
|-----------------------------------------------|------------|------------------------------------------------------------------|--------|
| (United States, r1, Iran, t1)                 | (X, r1, m) | Who will a country engage in diplomatic cooperation with, Israel |        |
| (United States, r2, Israel, t1) => (X, r2, n) |            | while this country accuses Iran on 2021-08-02?                   |        |

selected 250 relations, we generate either a true or an unknown question based on it. For example, for the fact (Sudan, host, Ramtane Lamamra, 2021-08-01 ), a true question is generated as Will Sudan host Ramtane Lamamra on 2021-08-01? and we label yes as its answer. An unknown question is generated by randomly perturbing one entity or the relation type in this fact, e.g., Will Germany host Ramtane Lamamra on 2021-08-01?, and we label unknown as its answer. We ensure that the perturbed fact does not exist in the original TKG. We use 25% of total facts in ICEWS21 to generate true questions and the rest are used to generate unknown questions.

Fact Reasoning Questions The motivation for proposing FRQs is to study the difference between humans and machines in finding the supporting evidence for reasoning. We formulate FRQs in the form of multiple choices. Each question is coupled with four choices. Given a TKG fact from an FRQ, we ask the QA models to choose which fact in the choices is the most contributive to (the most relevant cause of) the fact mentioned in the question. We provide several examples in Fig. [1.](#page-7-0) We generate FRQs as follows. We first train a TKG forecasting model xERTE [\[9\]](#page-16-3) on ICEWS21. Note that to predict a query (s, r, ?, t), xERTE samples its related prior TKG facts and assigns contribution scores to them. It provides explainability by assigning higher scores to the more related prior facts. We perform TKG forecasting and collect the queries where the ground-truth missing entities are ranked as top 1 by xERTE. For each collected query, we find its corresponding TKG fact and pick out four related prior facts found by xERTE. We take the prior facts with the highest, the lowest, and median contribution scores as Answer, Negative, and Median, respectively. Inspired by InferWiki [\[4\]](#page-16-7), we include a Hard Negative fact with the second highest contribution score, making it non-trivial for QA models to make the right decision. We generate each FRQ by turning the corresponding facts into a question and four choices (using templates), and manage to use xERTE to generate a large number of questions. However, since the answers to these questions are solely determined by xERTE, there exist numerous erroneous examples. For example, the Hard Negative of lots of them are more suitable than their Answer to be the answers. We ask five graduate students (major in computer science) to manually check all these questions and annotate them as reasonable or unreasonable according to their own knowledge or through search engines. If the majority annotate a question

as unreasonable, we filter it out. See Appendix C.4 for more details of FRQ generation and annotation, including the annotation instruction and interface.

<span id="page-7-0"></span>

| <b>Reasoning Types</b>                                                                                                                                                                                                                                                                                | <b>Question Example</b>                                                                                                                                                                                                                                                                                                                                                                                                         | <b>Example Explanation</b>                                                                                                                                                                            |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <b>Causal Relation (91%)</b>                                                                                                                                                                                                                                                                          | Which of the following statements contributes most to the fact that Pedro                                                                                                                                                                                                                                                                                                                                                       | Pedro Sanchez wished to                                                                                                                                                                               |
| The answer directly causes the                                                                                                                                                                                                                                                                        | Sanchez signed a formal agreement with Joseph Robinette Biden on 2021-08-23?                                                                                                                                                                                                                                                                                                                                                    | cooperate with Joseph                                                                                                                                                                                 |
| question fact or the answer clearly                                                                                                                                                                                                                                                                   | A. Pedro Sanchez expressed the intent to cooperate with Joseph Robinette Biden on 2021-08-22.                                                                                                                                                                                                                                                                                                                                   | Robinette Biden on 2021-                                                                                                                                                                              |
| shows the relationship between                                                                                                                                                                                                                                                                        | Pedro Sanchez engaged in diplomatic cooperation with Government (Spain) on 2021-08-22.                                                                                                                                                                                                                                                                                                                                          | 08-22. This directly causes                                                                                                                                                                           |
| entities that leads to the question                                                                                                                                                                                                                                                                   | C. Government (Spain) made a statement to Cuba on 2021-07-27.                                                                                                                                                                                                                                                                                                                                                                   | that they signed an                                                                                                                                                                                   |
| fact.                                                                                                                                                                                                                                                                                                 | D: United States praised or endorsed Sayyid Ali al-Husayni al-Sistani on 2021-07-24.                                                                                                                                                                                                                                                                                                                                            | agreement on the next day.                                                                                                                                                                            |
| <b>Identity Understanding (46%)</b>                                                                                                                                                                                                                                                                   | Which of the following statements contributes most to the fact that Turkey hosted                                                                                                                                                                                                                                                                                                                                               | Ursula von der Leven was                                                                                                                                                                              |
| An entity's identity is vital for                                                                                                                                                                                                                                                                     | Ursula von der Leyen on 2021-04-08?                                                                                                                                                                                                                                                                                                                                                                                             | the president of European                                                                                                                                                                             |
| reasoning. E.g., without knowing Sauli                                                                                                                                                                                                                                                                | A. Turkey signed a formal agreement with Government (Libya) on 2021-04-07.                                                                                                                                                                                                                                                                                                                                                      | Commission. Recep Tayyip                                                                                                                                                                              |
| Niinistö is the president of Finland,                                                                                                                                                                                                                                                                 | B. Wang Yi negotiated with Foreign Affairs (Malaysia) on 2021-04-02.                                                                                                                                                                                                                                                                                                                                                            | Erdoğan was the president                                                                                                                                                                             |
| the choices containing him might be                                                                                                                                                                                                                                                                   | C. Ursula von der Leyen expressed the intent to meet or negotiate with Recep Tayyip Erdoğan                                                                                                                                                                                                                                                                                                                                     | of Turkey. After knowing                                                                                                                                                                              |
| neglected, causing mistakes in                                                                                                                                                                                                                                                                        | on 2021-03-30.                                                                                                                                                                                                                                                                                                                                                                                                                  | the identities, it is obvious                                                                                                                                                                         |
| reasoning the facts regarding Finland.                                                                                                                                                                                                                                                                | D. Foreign Affairs (Turkey) praised or endorsed European Union on 2021-03-26.                                                                                                                                                                                                                                                                                                                                                   | that C is better than D.                                                                                                                                                                              |
| Time Sensitivity (19%)<br>Time difference between a choice and<br>the question fact plays an important<br>role. When more than one choice<br>seem reasonable, the choices that are<br>temporally far from the question fact<br>(or much farther than other choices)<br>are more probable to be wrong. | Which of the following statements contributes most to the fact that Xie Zhenhua<br>negotiated with John Kerry on 2021-08-31?<br>A. Xie Zhenhua expressed the intent to meet or negotiate with John Kerry on 2021-04-14.<br>B. Xie Zhenhua expressed the intent to meet or negotiate with John Kerry on 2021-08-30.<br>C. Xie Zhenhua negotiated with John Kerry on 2021-04-15.<br>D. China accused United States on 2021-04-09. | Without paying attention<br>to the timestamps of facts,<br>A. B. C all seem reasonable<br>to lead to the question fact.<br>However, after considering<br>time information, B should<br>be the answer. |

Fig. 1: Required reasoning types and proportions (%) in sampled FRQs, as well as FRQ examples. We sample 100 FRQs in each train/valid/test set. For choices, green for Answer, blue for Hard Negative, orange for Median and yellow for Negative. Multiple reasoning skills are required to answer each question, so the total proportion sum is not 100%.

To better study the reasoning skills required to answer FRQs, we randomly sample 300 FRQs and manually annotate them with reasoning types. The required reasoning skills and their proportions are shown in Fig. [1.](#page-7-0)

# 4 ForecastTKGQA

ForecastTKGQA employs a TKG forecasting model TANGO [\[10\]](#page-16-2) and a pretrained LM BERT [\[6\]](#page-16-8) for solving forecasting questions. We illustrate its model structure in Fig. [2](#page-8-0) with three stages. In Stage 1, a TKG forecasting model TANGO [\[10\]](#page-16-2) is used to generate the time-aware representation for each entity at each timestamp. In Stage 2, a pre-trained LM (e.g., BERT) is used to encode questions (and choices) into question (choice) representations. Finally, in Stage 3, answers are predicted according to the scores computed using the representations from Stage 1 and 2.

### 4.1 TKG Forecasting Model

We train TANGO on ICEWS21 with the TKG forecasting task. We use ComplEx [\[29\]](#page-19-5) as its scoring function. We learn the entity and relation representations in the complex space C d , where d is the dimension of complex vectors. The training set corresponds to all the TKG facts in Gtrain, and we evaluate the trained model on Gvalid and Gtest. After training, we perform a one time inference on

<span id="page-8-0"></span>![](_page_8_Figure_1.jpeg)
<!-- Image Description: This flowchart depicts a three-stage question answering model.  Stage 1 uses the TANGO model on ICEWS21 data.  Stage 2 involves BERT-based entity prediction and yes/unknown classification. Stage 3 uses BERT for fact reasoning, incorporating candidate answers (c₀-c₃) to select a final answer (c<sub>ans</sub>) based on  φ<sub>TR</sub>(c).  Equations define answer selection based on maximizing functions φ<sub>EP</sub> and φ<sub>YU</sub>.  The diagram illustrates the model's architecture and data flow. -->

Fig. 2: Model structure of ForecastTKGQA.

Gvalid and Gtest. Following the default setting of TANGO, to compute entity and relation representations at every timestamp t, we recurrently input all the TKG facts from t − 4 to t − 1, i.e., snapshots from Gt−<sup>4</sup> to Gt−1, into TANGO and take the output representations. Note that it infers representations based on the prior facts, thus not violating our forecasting setting. We compute the entity and relation representations at every timestamp in ICEWS21 and keep them for aiding the QA systems in Stage 1 (Fig. [2\)](#page-8-0). See Appendix B.1 for more details of TANGO training and inference. To leverage the complex representations computed by TANGO with ComplEx, we map the output of BERT to C d . For each natural language input, we take the output representation of the [CLS] token computed by BERT and project it to a 2d real space to form a 2d real valued vector. We take the first and second half of it as the real and imaginary part of a d-dimensional complex vector, respectively. All the representations output by BERT have already been mapped to C <sup>d</sup> without further notice.

#### 4.2 QA Model

Entity Prediction For every EPQ q, we compute an entity score for every entity e ∈ E. The entity with the highest score is predicted as the answer eans. To compute the score for e, we first input q into BERT and map its output to C d to get the question representation hq. Inspired by ComplEx, we then define e's entity score as

<span id="page-8-1"></span>
$$
\phi_{ep}(e) = \text{Re}\left( \langle \mathbf{h}'_{(s_q, t_q)}, \mathbf{h}_q, \bar{\mathbf{h}}'_{(e, t_q)} \rangle \right). \tag{1}
$$

h ′ (sq,tq) = fep h(sq,tq) , h ′ (e,tq) = fep h(e,tq) , where fep denotes a neural network aligning TKG representations to EPQs. h(sq,tq) and h(e,tq) denote the TANGO representations of the annotated entity s<sup>q</sup> and the entity e at the question timestamp tq, respectively. Re means taking the real part of a complex vector and h¯′ (e,tq) means the complex conjugate of h ′ (e,tq) .

Yes-Unknown Judgment For a YUQ, we compute a score for each candidate answer x ∈ {yes, unknown}. We first encode each x into a d-dimensional complex representation h<sup>x</sup> with BERT. Inspired by TComplEx [\[17\]](#page-17-1), we then compute scores as

<span id="page-9-0"></span>
$$
\phi_{\text{yu}}(x) = \text{Re}\left( < \mathbf{h}'_{(s_q, t_q)}, \mathbf{h}_q, \bar{\mathbf{h}}'_{(o_q, t_q)}, \mathbf{h}_x \right). \tag{2}
$$

h ′ (sq,tq) = fyu h(sq,tq) ,h ′ (oq,tq) = fyu h(oq,tq) , where fyu denotes a neural network aligning TKG representations to YUQs. h(sq,tq) and h(oq,tq) denote the TANGO representations of the annotated subject entity s<sup>q</sup> and object entity o<sup>q</sup> at tq, respectively. h<sup>q</sup> is the BERT encoded question representation. We take the candidate answer with the higher score as the predicted answer xans.

Fact Reasoning We compute a choice score for every choice c in an FRQ by using the following scoring function:

<span id="page-9-1"></span>
$$
\phi_{\rm fr}(c) = \text{Re}\left( < \mathbf{h}'_{(s_c, t_c)}, \mathbf{h}_q^c, \bar{\mathbf{h}}'_{(o_c, t_c)}, \mathbf{h}_q' > \right),\tag{3}
$$

h c q is the output of BERT mapped to C <sup>d</sup> given the concatenation of q and c. h ′ (sc,tc) = ffr h(sc,tc) and h ′ (oc,tc) = ffr h(oc,tc) . ffr is a projection network and h(sc,tc) , h(oc,tc) denote the TANGO representations of the entities annotated in c. h ′ <sup>q</sup> = f ffr h(sq,tq) ∥h c <sup>q</sup>∥ffr h(oq,tq) , where f serves as a projection and ∥ denotes concatenation. h(sq,tq) and h(oq,tq) denote the TANGO representations of the entities annotated in the question q. We take the choice with the highest choice score as our predicted answer cans. We give a more detailed description of Equation [1,](#page-8-1) [2](#page-9-0) and [3](#page-9-1) in Appendix A.

Parameter Learning We use cross-entropy loss to train ForecastTKGQA on each type of questions separately. The loss functions of EPQs, FRQs and YUQs are given by Lep = − P <sup>q</sup>∈Qep log P ϕep(eans) <sup>e</sup>∈E ϕep(e) , Lfr = − P <sup>q</sup>∈Qfr log P ϕfr(cans) <sup>c</sup> ϕfr(c) and Lyu = − P <sup>q</sup>∈Qyu log P ϕyu(xans) <sup>x</sup>∈{yes,unknown} ϕyu(x) , respectively. Qep/Qyu/Qfr denotes all EPQs/YUQs/FRQs and eans/xans/cans is the answer to question q.

# 5 Experiments

We answer several research questions (RQs) with experiments[11](#page-9-2) . RQ1 (Section [5.2,](#page-10-0) [5.4\)](#page-11-0): Can a TKG forecasting model better support forecasting TKGQA than a TKGC model? RQ2 (Section [5.2,](#page-10-0) [5.4\)](#page-11-0): Does ForecastTKGQA perform well in forecasting TKGQA? RQ3 (Section [5.3,](#page-11-1) [5.5\)](#page-12-0): Are the questions in our dataset answerable? RQ4 (Section [5.7\)](#page-14-0): Is the proposed dataset efficient? RQ5 (Section [5.6\)](#page-13-0): What are the challenges of forecasting TKGQA?

<span id="page-9-2"></span><sup>11</sup> Implementation details and further analysis of ForecastTKGQA in Appendix B.3 and G.

### 5.1 Experimental Setting

Evaluation Metrics We use mean reciprocal rank (MRR) and Hits@k as the evaluation metrics of the EPQs. For each EPQ, we compute the rank of the ground-truth answer entity among all the TKG entities. Test MRR is then computed as <sup>1</sup> |Qep test| P q∈Qep test 1 rank<sup>q</sup> , where Q ep test denotes all EPQs in the test set and rank<sup>q</sup> is the rank of the ground-truth answer entity of question q. Hits@k is the proportion of the answered questions where the ground-truth answer entity is ranked as top k. For YUQs and FRQs, we employ accuracy for evaluation. Accuracy is the proportion of the correctly answered questions out of all questions.

Baseline Methods We consider two pre-trained LMs, BERT [\[6\]](#page-16-8) and RoBERTa [\[18\]](#page-18-5) as baselines. For EPQs and YUQs, we add a prediction head on top of the question representations computed by LMs, and use softmax function to compute answer probabilities. For every FRQ, we input into each LM the concatenation of the question with each choice, and follow the same prediction structure. Besides, we derive two model variants for each LM by introducing TKG representations. We train TComplEx on ICEWS21. For every EPQ and YUQ, we concatenate the question representation with the TComplEx representations of the entities and timestamps annotated in the question, and then perform prediction with a prediction head and softmax. For FRQs, we further include TComplEx representations into choices in the same way. We call this type of variant BERT int and RoBERTa int since TComplEx is a TKGC (TKG interpolation) method. Similarly, we also introduce TANGO representations into LMs and derive BERT ext and RoBERTa ext, where TANGO serves as a TKG extrapolation backend. Detailed model derivations are presented in Appendix B.2. We also consider one KGQA method EmbedKGQA [\[25\]](#page-18-6), and two TKGQA methods, i.e., CronKGQA [\[24\]](#page-18-0) and TempoQR [\[20\]](#page-18-2) as baselines. We run EmbedKGQA on top of the KG representations trained with ComplEx on ICEWS21, and run TKGQA baselines on top of the TKG representations trained with TComplEx.

#### <span id="page-10-0"></span>5.2 Main Results

We report the experimental results in Table [5.](#page-11-2) In Table [5a,](#page-11-2) we show that our entity prediction model outperforms all baseline methods. We observe that EmbedKGQA achieves a better performance than BERT and RoBERTa, showing that employing KG representations helps TKGQA. Besides, LM variants outperform their original LMs, indicating that TKG representations help LMs perform better in TKGQA. Further, BERT ext shows stronger performance than BERT int (this also applies to RoBERTa int and RoBERTa ext), which proves that TKG forecasting models provide greater help than TKGC models in forecasting TKGQA. CronKGQA and TempoQR employ TComplEx representations as supporting information and perform poorly, implying that employing TKG representations provided by TKGC methods may include noisy information in forecasting TKGQA. ForecastTKGQA injects TANGO representations

<span id="page-11-2"></span>Table 5: Experimental results over ForecastTKGQuestions. The best results are marked in bold.

(a) EPQs. Overall results in Appendix D. (b) YUQs and FRQs.

|                                                   | MRR | Hits@1 | Hits@10                                                                    |                                        |   | Accuracy                   |
|---------------------------------------------------|-----|--------|----------------------------------------------------------------------------|----------------------------------------|---|----------------------------|
| Model                                             |     |        | 1-Hop 2-Hop 1-Hop 2-Hop 1-Hop 2-Hop                                        | Model                                  |   | YUQ FRQ                    |
| RoBERTa<br>BERT                                   |     |        | 0.166 0.149 0.104 0.085 0.288 0.268<br>0.279 0.182 0.192 0.106 0.451 0.342 | RoBERTa<br>BERT                        |   | 0.721 0.645<br>0.813 0.634 |
| EmbedKGQA                                         |     |        | 0.317 0.185 0.228 0.112 0.489 0.333                                        | RoBERTa int                            |   | 0.768 0.693                |
| RoBERTa int<br>BERT int                           |     |        | 0.283 0.157 0.190 0.094 0.467 0.290<br>0.314 0.183 0.223 0.107 0.490 0.344 | BERT int                               |   | 0.829 0.682                |
| CronKGQA<br>TempoQR                               |     |        | 0.131 0.090 0.081 0.042 0.231 0.187<br>0.145 0.107 0.094 0.061 0.243 0.199 | RoBERTa ext<br>BERT ext                |   | 0.798 0.707<br>0.837 0.746 |
| RoBERTa ext<br>BERT ext                           |     |        | 0.306 0.180 0.216 0.108 0.497 0.323<br>0.331 0.208 0.239 0.128 0.508 0.369 | ForecastTKGQA<br>Human Performance (a) | - | 0.870 0.769<br>0.936       |
| ForecastTKGQA 0.339 0.216 0.248 0.129 0.517 0.386 |     |        |                                                                            | Human Performance (b)                  | - | 0.954                      |

into a scoring module, showing its great effectiveness on EPQs. For YUQs and FRQs, ForecastTKGQA also achieves the best performance. Table [5b](#page-11-2) shows that it is helpful to include TKG representations for answering YUQs and FRQs and our scoring functions are effective.

#### <span id="page-11-1"></span>5.3 Human vs. Machine on FRQs

To study the difference between humans and models in fact reasoning, we further benchmark human performance on FRQs with a survey (See Appendix E for details). We ask five graduate students to answer 100 questions randomly sampled from the test set. We consider two settings: (a) Humans answer FRQs with their own knowledge and inference ability. Search engines are not allowed; (b) Humans can turn to search engines and use the web information published before the question timestamp for aiding QA. Table [5](#page-11-2) shows that humans achieve much stronger performance than all QA models (even in setting (a)). This calls for a great effort to build better fact reasoning TKGQA models.

#### <span id="page-11-0"></span>5.4 Performance over FRQs with Different Reasoning Types

Considering the reasoning types listed in Fig. [1,](#page-7-0) we compare RoBERTa int with ForecastTKGQA on the 100 sampled test questions that are annotated with reasoning types, to justify performance gain brought by TKG forecasting model on FRQs. Experimental results in Table [6](#page-12-1) imply that employing TKG forecasting model helps QA models better deal with any reasoning type on FRQs. We use two cases in Fig. [3](#page-12-2) to provide insights of performance gain.

Case 1. Two reasoning skills, i.e., Causal Relation and Time Sensitivity (shown in Fig. [1\)](#page-7-0), are required to correctly answer the question in Case 1. Without considering the timestamps of choices, A, B, C all seem at least somehow reasonable.

<span id="page-12-1"></span>Table 6: Performance comparison across FRQs with different reasoning types.

|               | Accuracy |                                                         |       |  |  |
|---------------|----------|---------------------------------------------------------|-------|--|--|
| Model         |          | Causal Relation Identity Understanding Time Sensitivity |       |  |  |
| RoBERTa int   | 0.670    | 0.529                                                   | 0.444 |  |  |
| ForecastTKGQA | 0.787    | 0.735                                                   | 0.611 |  |  |

<span id="page-12-2"></span>

| (a) Case 1. |  | (b) Case 2. |  |  |
|-------------|--|-------------|--|--|

Fig. 3: Case Studies on FRQs. We mark green for Answer, blue for Hard Negative, orange for Median and yellow for Negative.

However, after considering choice timestamps, B should be the most contributive reason for the question fact. First, the timestamp of B (2021-08-30 ) is much closer to the question timestamp (2021-08-31 ). Moreover, the fact in choice B directly causes the question fact. RoBERTa int manages to capture the causation, but fail to correctly deal with time sensitivity, while ForecastTKGQA achieves better reasoning on both reasoning types.

Case 2. Two reasoning skills, i.e., Causal Relation and Identity Understanding (shown in Fig. [1\)](#page-7-0), are required to correctly answer the question in Case 2. Head of Government (Somalia) and Somalia are two different entities in TKG, however, both entities are about Somalia. By understanding this, we are able to choose the correct answer. ForecastTKGQA manages to understand the identity of Head of Government (Somalia), match it with Somalia and find the cause of the question fact. RoBERTa int makes a mistake because as a model equipped with TComplEx, it has no well-trained timestamp representations of the question and choice timestamps, which would introduce noise in decision making.

#### <span id="page-12-0"></span>5.5 Answerability of ForecastTKGQuestions

To validate the answerability of the questions in ForecastTKGQuestions. We train TComplEx and TANGO over the whole ICEWS21, i.e., Gtrain∪Gvalid∪Gtest, and use them to support QA. Note that this violates the forecasting setting of forecasting TKGQA, and thus we call the TKG models trained in this way as cheating TComplEx (CTComplEx) and cheating TANGO (CTANGO). Answering EPQs with cheating TKG models is same as non-forecasting TKGQA. We couple TempoQR with CTComplEx and see a huge performance increase (Table [7a\)](#page-13-1). Besides, inspired by [\[11\]](#page-17-6), we develop a new TKGQA model Multi-Hop

<span id="page-13-1"></span>Table 7: Answerability study. Models with α means using CTComplEx and β means using CTANGO. ↑ denotes relative improvement (%) from the results in Table [5.](#page-11-2) Acc means Accuracy.

| (a) EPQs. |
|-----------|
|           |

#### (b) YUQs and FRQs.

|          | MRR   |   |       |   | Hits@10 |   |                                                 |   |                                    | YUQ |   | FRQ                   |   |
|----------|-------|---|-------|---|---------|---|-------------------------------------------------|---|------------------------------------|-----|---|-----------------------|---|
| Model    | 1-Hop | ↑ | 2-Hop | ↑ | 1-Hop   | ↑ | 2-Hop                                           | ↑ | Model                              | Acc | ↑ | Acc                   | ↑ |
| TempoQRα |       |   |       |   |         |   | 0.713 391.7 0.233 117.8 0.883 263.4 0.419 110.6 |   | BERT intα                          |     |   | 0.855 19.6 0.816 14.4 |   |
| MHSα     | 0.868 | - | 0.647 | - | 0.992   | - | 0.904                                           | - | BERT extβ                          |     |   | 0.873 4.3 0.836 12.1  |   |
| MHSβ     | 0.771 | - | 0.556 | - | 0.961   | - | 0.828                                           | - | ForecastTKGQAβ 0.925 6.3 0.821 6.8 |     |   |                       |   |

Scorer[12](#page-13-2) (MHS) for EPQs. Starting from the annotated entity s<sup>q</sup> of an EPQ, MHS updates the scores of outer entities for n-hops (n = 2 in our experiments) until all sq's n-hop neighbors on the snapshot Gt<sup>q</sup> are visited. Initially, MHS assigns a score of 1 to s<sup>q</sup> and 0 to any other unvisited entity. For each unvisited entity e, it then computes e's score as: ϕep(e) = <sup>1</sup> |Ne(tq)| P (e ′ ,r)∈Ne(tq) (γ · ϕep(e ′ ) + ψ(e ′ , r, e, tq)), where Ne(tq) = {(e ′ , r)|(e ′ , r, e, tq) ∈ Gt<sup>q</sup> } is e's 1-hop neighborhood on Gt<sup>q</sup> and γ is a discount factor. We couple MHS with CT-ComplEx and CTANGO, and define ψ(e ′ , r, e, tq) separately. For MHS + CT-ComplEx, ψ(e ′ , r, e, tq) = f2(f1(h<sup>e</sup> ′∥hr∥he∥ht<sup>q</sup> ∥hq)). f<sup>1</sup> and f<sup>2</sup> are two neural networks. he, h<sup>e</sup> ′ , hr, ht<sup>q</sup> are the CTComplEx representations of entities e, e ′ , relation r and timestamp tq, respectively. For MHS + CTANGO, we take the idea of ForecastTKGQA: ψ(e ′ , r, e, tq) = Re < h(<sup>e</sup> ′ ,tq) , hr, h¯ (e,tq) , h<sup>q</sup> > . h(e,tq) , h(<sup>e</sup> ′ ,tq) , h<sup>r</sup> are the CTANGO representations of entities e, e ′ at tq, and relation r, respectively. h<sup>q</sup> is BERT encoded question representation. We find that MHS achieves superior performance (even on 2-hop EPQs). This is because MHS not only uses cheating TKG models, but also considers ground-truth multi-hop structural information of TKGs at t<sup>q</sup> (which is unavailable in the forecasting setting). For YUQs and FRQs, Table [7b](#page-13-1) shows that cheating TKG models help improve performance, especially on FRQs. These results imply that given the ground-truth TKG information at question timestamps, our forecasting TKGQA questions are answerable.

#### <span id="page-13-0"></span>5.6 Challenges of Forecasting TKGQA over ForecastTKGQuestions

From the experiments discussed in Section [5.3](#page-11-1) and [5.5,](#page-12-0) we summarize the challenges of forecasting TKGQA: (1) Inferring the ground-truth TKG information G<sup>t</sup><sup>q</sup> at the question timestamp t<sup>q</sup> accurately; (2) Effectively performing multihop reasoning for forecasting TKGQA; (3) Developing TKGQA models for better fact reasoning. In Section [5.5,](#page-12-0) we have trained cheating TKG models and used them to support QA. We show in Table [7](#page-13-1) that QA models substantially improve

<span id="page-13-2"></span><sup>12</sup> See Appendix F for detailed model explanation and model structure illustration.

their performance on forecasting TKGQA with cheating TKG models. This implies that accurately inferring the ground-truth TKG information at t<sup>q</sup> is crucial in our task and how to optimally achieve it remains a challenge. We also observe that MHS with cheating TKG models achieves much better results on EPQs (especially on 2-hop). MHS utilizes multi-hop information of the ground-truth TKG at t<sup>q</sup> (G<sup>t</sup><sup>q</sup> ) for better QA. In forecasting TKGQA, by only knowing the TKG facts before t<sup>q</sup> and not observing G<sup>t</sup><sup>q</sup> , it is impossible for MHS to directly utilize the ground-truth multi-hop information at tq. This implies that how to effectively infer and exploit multi-hop information for QA in the forecasting scenario remains a challenge. Moreover, as discussed in Section [5.3,](#page-11-1) current TKGQA models still trail humans with great margin on FRQs. It is challenging to design novel forecasting TKGQA models for better fact reasoning.

#### <span id="page-14-0"></span>5.7 Study of Data Efficiency

We want to know how the models will be affected with less/more training data. For each type of questions, we modify the size of its training set. We train ForecastTKGQA on the modified training sets and evaluate our model on the original test sets. We randomly sample 10%, 25%, 50%, and 75% of the training examples to form new training sets. Fig. [4](#page-14-1) shows that for every type of question, the performance of ForecastTKGQA steadily improves as the size of the training sets increase. This proves that our proposed dataset is efficient and useful for training forecasting TKGQA models.

<span id="page-14-1"></span>![](_page_14_Figure_4.jpeg)
<!-- Image Description: The image contains two line graphs (a) and (b) illustrating data efficiency. Graph (a) shows the performance (Mean Reciprocal Rank (MRR) and Hits@10) of 1-hop and 2-hop models on EPQs across varying training set percentages (10-100%). Graph (b) displays the accuracy of FRQ and YUQ models with changing training set sizes (10-100%). Both graphs assess model performance based on the portion of the training dataset used, demonstrating data efficiency in different model types. -->

Fig. 4: Data efficiency analysis.

# 6 Justification of Task Validity from Two Perpectives

(1) Perspective from Underlying TKG. We take a commonly used temporal KB, i.e., ICEWS, as the KB for constructing underlying TKG ICEWS21. ICEWS-based TKGs contain socio-political facts. It is meaningful to perform

forecasting over them because this can help to improve early warning in critical socio-political situations around the globe. [\[28\]](#page-19-6) has shown with case studies that ICEWS-based TKG datasets have underlying cause-and-effect temporal patterns and TKG forecasting models are built to capture them. This indicates that performing TKG forecasting over ICEWS-based TKGs are also valid. And therefore, developing forecasting TKGQA on top of ICEWS21 is meaningful and valid. (2) Perspective from the Motivation of Proposing Different Types of Questions. The motivation of proposing EPQs is to introduce TKG link forecasting (future link prediction) into KGQA, while proposing YUQs is to introduce quadruple classification (stemming from triple classification) and yesno type questions. We view quadruple classification in the forecasting scenario as deciding if the unseen TKG facts are valid based on previous known TKG facts. To answer EPQs and YUQs, models can be considered as understanding natural language questions first and then perform TKG reasoning tasks. Since TKG reasoning tasks are considered solvable and widely studied in the TKG community, our task over EPQs and YUQs is valid. We propose FRQs aiming to study the difference between humans and machines in fact reasoning. We have summarized the reasoning skills that are required to answer every FRQ in Fig. [1,](#page-7-0) which also implies the potential direction for QA models to achieve improvement in fact reasoning in the future. We haven shown in Section [5.3](#page-11-1) that our proposed FRQs are answerable to humans, which directly indicates the validity of our FRQs. Thus, answering FRQs in forecasting TKGQA is also valid and meaningful.

# 7 Conclusion

In this work, we propose a novel task: forecasting TKGQA. To the best of our knowledge, it is the first work combining TKG forecasting with KGQA. We propose a coupled benchmark dataset ForecastTKGQuestions that contains various types of questions including EPQs, YUQs and FRQs. To solve forecasting TKGQA, we propose ForecastTKGQA, a QA model that leverages a TKG forecasting model with a pre-trained LM. Though experimental results show that our model achieves great performance, there still exists a large room for improvement compared with humans. We hope our work can benefit future research and draw attention to studying the forecasting power of TKGQA methods.

Acknowledgement. This work has been supported by the German Federal Ministry for Economic Affairs and Climate Action (BMWK) as part of the project CoyPu under grant number 01MK21007K.

Supplemental Material Statement: Source code and data are uploaded here[13](#page-15-0) . Appendices are published in the arXiv version[14](#page-15-1). We have referred to the corresponding parts in the main body. Please check accordingly.

<span id="page-15-0"></span><sup>13</sup> https://github.com/ZifengDing/ForecastTKGQA

<span id="page-15-1"></span><sup>14</sup> https://arxiv.org/abs/2208.06501

# References

- <span id="page-16-9"></span>1. Balazevic, I., Allen, C., Hospedales, T.M.: Tucker: Tensor factorization for knowledge graph completion. In: Inui, K., Jiang, J., Ng, V., Wan, X. (eds.) Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing, EMNLP-IJCNLP 2019, Hong Kong, China, November 3-7, 2019. pp. 5184–5193. Association for Computational Linguistics (2019). [https://doi.org/10.18653/v1/D19-1522,](https://doi.org/10.18653/v1/D19-1522) <https://doi.org/10.18653/v1/D19-1522>
- <span id="page-16-4"></span>2. Bordes, A., Usunier, N., Chopra, S., Weston, J.: Largescale simple question answering with memory networks (2015). [https://doi.org/10.48550/ARXIV.1506.02075,](https://doi.org/10.48550/ARXIV.1506.02075)<https://arxiv.org/abs/1506.02075>
- <span id="page-16-0"></span>3. Boschee, E., Lautenschlager, J., O'Brien, S., Shellman, S., Starz, J., Ward, M.: ICEWS Coded Event Data (2015). [https://doi.org/10.7910/DVN/28075, https:](https://doi.org/10.7910/DVN/28075) [//doi.org/10.7910/DVN/28075](https://doi.org/10.7910/DVN/28075)
- <span id="page-16-7"></span>4. Cao, Y., Ji, X., Lv, X., Li, J., Wen, Y., Zhang, H.: Are missing links predictable? an inferential benchmark for knowledge graph completion. In: Zong, C., Xia, F., Li, W., Navigli, R. (eds.) Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing, ACL/IJCNLP 2021, (Volume 1: Long Papers), Virtual Event, August 1-6, 2021. pp. 6855–6865. Association for Computational Linguistics (2021). [https://doi.org/10.18653/v1/2021.acl-long.534,](https://doi.org/10.18653/v1/2021.acl-long.534) <https://doi.org/10.18653/v1/2021.acl-long.534>
- <span id="page-16-5"></span>5. Chen, Z., Zhao, X., Liao, J., Li, X., Kanoulas, E.: Temporal knowledge graph question answering via subgraph reasoning. Knowl. Based Syst. 251, 109134 (2022). [https://doi.org/10.1016/j.knosys.2022.109134, https://doi.org/10.1016/j.](https://doi.org/10.1016/j.knosys.2022.109134) [knosys.2022.109134](https://doi.org/10.1016/j.knosys.2022.109134)
- <span id="page-16-8"></span>6. Devlin, J., Chang, M., Lee, K., Toutanova, K.: BERT: pre-training of deep bidirectional transformers for language understanding. In: Burstein, J., Doran, C., Solorio, T. (eds.) Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, NAACL-HLT 2019, Minneapolis, MN, USA, June 2-7, 2019, Volume 1 (Long and Short Papers). pp. 4171–4186. Association for Computational Linguistics (2019). [https://doi.org/10.18653/v1/n19-1423, https://doi.org/10.18653/v1/n19-1423](https://doi.org/10.18653/v1/n19-1423)
- <span id="page-16-1"></span>7. Ding, Z., Ma, Y., He, B., Han, Z., Tresp, V.: A simple but powerful graph encoder for temporal knowledge graph completion. In: NeurIPS 2022 Temporal Graph Learning Workshop (2022),<https://openreview.net/forum?id=DYG8RbgAIo>
- <span id="page-16-6"></span>8. Gal´arraga, L.A., Teflioudi, C., Hose, K., Suchanek, F.M.: AMIE: association rule mining under incomplete evidence in ontological knowledge bases. In: Schwabe, D., Almeida, V.A.F., Glaser, H., Baeza-Yates, R., Moon, S.B. (eds.) 22nd International World Wide Web Conference, WWW '13, Rio de Janeiro, Brazil, May 13-17, 2013. pp. 413–422. International World Wide Web Conferences Steering Committee / ACM (2013). [https://doi.org/10.1145/2488388.2488425, https://doi.org/10.1145/](https://doi.org/10.1145/2488388.2488425) [2488388.2488425](https://doi.org/10.1145/2488388.2488425)
- <span id="page-16-3"></span>9. Han, Z., Chen, P., Ma, Y., Tresp, V.: Explainable subgraph reasoning for forecasting on temporal knowledge graphs. In: 9th International Conference on Learning Representations, ICLR 2021, Virtual Event, Austria, May 3-7, 2021. OpenReview.net (2021),<https://openreview.net/forum?id=pGIHq1m7PU>
- <span id="page-16-2"></span>10. Han, Z., Ding, Z., Ma, Y., Gu, Y., Tresp, V.: Learning neural ordinary equations for forecasting future links on temporal knowledge graphs. In: Moens, M., Huang, X.,

Specia, L., Yih, S.W. (eds.) Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, EMNLP 2021, Virtual Event / Punta Cana, Dominican Republic, 7-11 November, 2021. pp. 8352–8364. Association for Computational Linguistics (2021). [https://doi.org/10.18653/v1/2021.emnlp-main.658,](https://doi.org/10.18653/v1/2021.emnlp-main.658) <https://doi.org/10.18653/v1/2021.emnlp-main.658>

- <span id="page-17-6"></span>11. Ji, H., Ke, P., Huang, S., Wei, F., Zhu, X., Huang, M.: Language generation with multi-hop reasoning on commonsense knowledge graph. In: Webber, B., Cohn, T., He, Y., Liu, Y. (eds.) Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing, EMNLP 2020, Online, November 16-20, 2020. pp. 725–736. Association for Computational Linguistics (2020). [https://doi.org/10.18653/v1/2020.emnlp-main.54, https://doi.org/10.](https://doi.org/10.18653/v1/2020.emnlp-main.54) [18653/v1/2020.emnlp-main.54](https://doi.org/10.18653/v1/2020.emnlp-main.54)
- <span id="page-17-4"></span>12. Jia, Z., Abujabal, A., Roy, R.S., Str¨otgen, J., Weikum, G.: Tempquestions: A benchmark for temporal question answering. In: Champin, P., Gandon, F., Lalmas, M., Ipeirotis, P.G. (eds.) Companion of the The Web Conference 2018 on The Web Conference 2018, WWW 2018, Lyon , France, April 23-27, 2018. pp. 1057–1062. ACM (2018). [https://doi.org/10.1145/3184558.3191536, https://doi.org/10.1145/](https://doi.org/10.1145/3184558.3191536) [3184558.3191536](https://doi.org/10.1145/3184558.3191536)
- <span id="page-17-5"></span>13. Jia, Z., Pramanik, S., Roy, R.S., Weikum, G.: Complex temporal question answering on knowledge graphs. In: Demartini, G., Zuccon, G., Culpepper, J.S., Huang, Z., Tong, H. (eds.) CIKM '21: The 30th ACM International Conference on Information and Knowledge Management, Virtual Event, Queensland, Australia, November 1 - 5, 2021. pp. 792–802. ACM (2021). [https://doi.org/10.1145/3459637.3482416, https://doi.org/10.1145/](https://doi.org/10.1145/3459637.3482416) [3459637.3482416](https://doi.org/10.1145/3459637.3482416)
- <span id="page-17-0"></span>14. Jin, W., Khanna, R., Kim, S., Lee, D., Morstatter, F., Galstyan, A., Ren, X.: Forecastqa: A question answering challenge for event forecasting with temporal text data. In: Zong, C., Xia, F., Li, W., Navigli, R. (eds.) Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing, ACL/IJCNLP 2021, (Volume 1: Long Papers), Virtual Event, August 1-6, 2021. pp. 4636–4650. Association for Computational Linguistics (2021). [https://doi.org/10.18653/v1/2021.acl](https://doi.org/10.18653/v1/2021.acl-long.357)[long.357, https://doi.org/10.18653/v1/2021.acl-long.357](https://doi.org/10.18653/v1/2021.acl-long.357)
- <span id="page-17-3"></span>15. Jin, W., Qu, M., Jin, X., Ren, X.: Recurrent event network: Autoregressive structure inferenceover temporal knowledge graphs. In: Webber, B., Cohn, T., He, Y., Liu, Y. (eds.) Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing, EMNLP 2020, Online, November 16-20, 2020. pp. 6669–6683. Association for Computational Linguistics (2020). [https://doi.org/10.18653/v1/2020.emnlp-main.541, https://doi.org/10.18653/v1/](https://doi.org/10.18653/v1/2020.emnlp-main.541) [2020.emnlp-main.541](https://doi.org/10.18653/v1/2020.emnlp-main.541)
- <span id="page-17-2"></span>16. Jung, J., Jung, J., Kang, U.: Learning to walk across time for interpretable temporal knowledge graph completion. In: Zhu, F., Ooi, B.C., Miao, C. (eds.) KDD '21: The 27th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, Virtual Event, Singapore, August 14-18, 2021. pp. 786–795. ACM (2021). [https://doi.org/10.1145/3447548.3467292, https://doi.org/10.1145/](https://doi.org/10.1145/3447548.3467292) [3447548.3467292](https://doi.org/10.1145/3447548.3467292)
- <span id="page-17-1"></span>17. Lacroix, T., Obozinski, G., Usunier, N.: Tensor decompositions for temporal knowledge base completion. In: 8th International Conference on Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April 26-30, 2020. OpenReview.net (2020),<https://openreview.net/forum?id=rke2P1BFwS>

- <span id="page-18-5"></span>18. Liu, Y., Ott, M., Goyal, N., Du, J., Joshi, M., Chen, D., Levy, O., Lewis, M., Zettlemoyer, L., Stoyanov, V.: Roberta: A robustly optimized bert pretraining approach (2019). [https://doi.org/10.48550/ARXIV.1907.11692,](https://doi.org/10.48550/ARXIV.1907.11692) [https://arxiv.org/](https://arxiv.org/abs/1907.11692) [abs/1907.11692](https://arxiv.org/abs/1907.11692)
- <span id="page-18-1"></span>19. Liu, Y., Ma, Y., Hildebrandt, M., Joblin, M., Tresp, V.: Tlogic: Temporal logical rules for explainable link forecasting on temporal knowledge graphs. In: Thirty-Sixth AAAI Conference on Artificial Intelligence, AAAI 2022, Thirty-Fourth Conference on Innovative Applications of Artificial Intelligence, IAAI 2022, The Twelveth Symposium on Educational Advances in Artificial Intelligence, EAAI 2022 Virtual Event, February 22 - March 1, 2022. pp. 4120–4127. AAAI Press (2022), <https://ojs.aaai.org/index.php/AAAI/article/view/20330>
- <span id="page-18-2"></span>20. Mavromatis, C., Subramanyam, P.L., Ioannidis, V.N., Adeshina, A., Howard, P.R., Grinberg, T., Hakim, N., Karypis, G.: Tempoqr: Temporal question reasoning over knowledge graphs. In: Thirty-Sixth AAAI Conference on Artificial Intelligence, AAAI 2022, Thirty-Fourth Conference on Innovative Applications of Artificial Intelligence, IAAI 2022, The Twelveth Symposium on Educational Advances in Artificial Intelligence, EAAI 2022 Virtual Event, February 22 - March 1, 2022. pp. 5825–5833. AAAI Press (2022), [https://ojs.aaai.org/index.php/AAAI/article/](https://ojs.aaai.org/index.php/AAAI/article/view/20526) [view/20526](https://ojs.aaai.org/index.php/AAAI/article/view/20526)
- <span id="page-18-4"></span>21. Meilicke, C., Chekol, M.W., Fink, M., Stuckenschmidt, H.: Reinforced anytime bottom up rule learning for knowledge graph completion (2020). [https://doi.org/10.48550/ARXIV.2004.04412,](https://doi.org/10.48550/ARXIV.2004.04412)<https://arxiv.org/abs/2004.04412>
- <span id="page-18-7"></span>22. Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J., Chanan, G., Killeen, T., Lin, Z., Gimelshein, N., Antiga, L., Desmaison, A., K¨opf, A., Yang, E.Z., DeVito, Z., Raison, M., Tejani, A., Chilamkurthy, S., Steiner, B., Fang, L., Bai, J., Chintala, S.: Pytorch: An imperative style, high-performance deep learning library. In: Wallach, H.M., Larochelle, H., Beygelzimer, A., d'Alch´e-Buc, F., Fox, E.B., Garnett, R. (eds.) Advances in Neural Information Processing Systems 32: Annual Conference on Neural Information Processing Systems 2019, NeurIPS 2019, December 8-14, 2019, Vancouver, BC, Canada. pp. 8024–8035 (2019), [https://proceedings.](https://proceedings.neurips.cc/paper/2019/hash/bdbca288fee7f92f2bfa9f7012727740-Abstract.html) [neurips.cc/paper/2019/hash/bdbca288fee7f92f2bfa9f7012727740-Abstract.html](https://proceedings.neurips.cc/paper/2019/hash/bdbca288fee7f92f2bfa9f7012727740-Abstract.html)
- <span id="page-18-8"></span>23. Sanh, V., Debut, L., Chaumond, J., Wolf, T.: Distilbert, a distilled version of BERT: smaller, faster, cheaper and lighter. CoRR abs/1910.01108 (2019), [http:](http://arxiv.org/abs/1910.01108) [//arxiv.org/abs/1910.01108](http://arxiv.org/abs/1910.01108)
- <span id="page-18-0"></span>24. Saxena, A., Chakrabarti, S., Talukdar, P.P.: Question answering over temporal knowledge graphs. In: Zong, C., Xia, F., Li, W., Navigli, R. (eds.) Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing, ACL/IJCNLP 2021, (Volume 1: Long Papers), Virtual Event, August 1-6, 2021. pp. 6663–6676. Association for Computational Linguistics (2021). [https://doi.org/10.18653/v1/2021.acl-long.520, https://doi.org/10.18653/](https://doi.org/10.18653/v1/2021.acl-long.520) [v1/2021.acl-long.520](https://doi.org/10.18653/v1/2021.acl-long.520)
- <span id="page-18-6"></span>25. Saxena, A., Tripathi, A., Talukdar, P.: Improving multi-hop question answering over knowledge graphs using knowledge base embeddings. In: Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics. pp. 4498–4507. Association for Computational Linguistics, Online (Jul 2020). [https://doi.org/10.18653/v1/2020.acl-main.412,](https://doi.org/10.18653/v1/2020.acl-main.412) [https://aclanthology.org/](https://aclanthology.org/2020.acl-main.412) [2020.acl-main.412](https://aclanthology.org/2020.acl-main.412)
- <span id="page-18-3"></span>26. Shang, C., Wang, G., Qi, P., Huang, J.: Improving time sensitivity for question answering over temporal knowledge graphs. In: Muresan, S., Nakov, P., Villavi-

cencio, A. (eds.) Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2022, Dublin, Ireland, May 22-27, 2022. pp. 8017–8026. Association for Computational Linguistics (2022), <https://aclanthology.org/2022.acl-long.552>

- <span id="page-19-2"></span>27. Talmor, A., Berant, J.: The web as a knowledge-base for answering complex questions. In: Walker, M.A., Ji, H., Stent, A. (eds.) Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, NAACL-HLT 2018, New Orleans, Louisiana, USA, June 1-6, 2018, Volume 1 (Long Papers). pp. 641–651. Association for Computational Linguistics (2018). [https://doi.org/10.18653/v1/n18-1059,](https://doi.org/10.18653/v1/n18-1059) <https://doi.org/10.18653/v1/n18-1059>
- <span id="page-19-6"></span>28. Trivedi, R., Dai, H., Wang, Y., Song, L.: Know-evolve: Deep temporal reasoning for dynamic knowledge graphs. In: Precup, D., Teh, Y.W. (eds.) Proceedings of the 34th International Conference on Machine Learning, ICML 2017, Sydney, NSW, Australia, 6-11 August 2017. Proceedings of Machine Learning Research, vol. 70, pp. 3462–3471. PMLR (2017),<http://proceedings.mlr.press/v70/trivedi17a.html>
- <span id="page-19-5"></span>29. Trouillon, T., Welbl, J., Riedel, S., Gaussier, E., Bouchard, G.: Complex embed- ´ dings for simple link prediction. In: Balcan, M., Weinberger, K.Q. (eds.) Proceedings of the 33nd International Conference on Machine Learning, ICML 2016, New York City, NY, USA, June 19-24, 2016. JMLR Workshop and Conference Proceedings, vol. 48, pp. 2071–2080. JMLR.org (2016), [http://proceedings.mlr.press/v48/](http://proceedings.mlr.press/v48/trouillon16.html) [trouillon16.html](http://proceedings.mlr.press/v48/trouillon16.html)
- <span id="page-19-4"></span>30. Vrandecic, D., Kr¨otzsch, M.: Wikidata: a free collaborative knowledgebase. Commun. ACM 57(10), 78–85 (2014). [https://doi.org/10.1145/2629489, https://doi.](https://doi.org/10.1145/2629489) [org/10.1145/2629489](https://doi.org/10.1145/2629489)
- <span id="page-19-7"></span>31. Wolf, T., Debut, L., Sanh, V., Chaumond, J., Delangue, C., Moi, A., Cistac, P., Rault, T., Louf, R., Funtowicz, M., Brew, J.: Huggingface's transformers: State-ofthe-art natural language processing. CoRR abs/1910.03771 (2019), [http://arxiv.](http://arxiv.org/abs/1910.03771) [org/abs/1910.03771](http://arxiv.org/abs/1910.03771)
- <span id="page-19-1"></span>32. Yih, W., Chang, M., He, X., Gao, J.: Semantic parsing via staged query graph generation: Question answering with knowledge base. In: Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing of the Asian Federation of Natural Language Processing, ACL 2015, July 26-31, 2015, Beijing, China, Volume 1: Long Papers. pp. 1321–1331. The Association for Computer Linguistics (2015). [https://doi.org/10.3115/v1/p15-1128, https://doi.org/10.3115/v1/p15-1128](https://doi.org/10.3115/v1/p15-1128)
- <span id="page-19-3"></span>33. Zhang, Y., Dai, H., Kozareva, Z., Smola, A.J., Song, L.: Variational reasoning for question answering with knowledge graph. In: McIlraith, S.A., Weinberger, K.Q. (eds.) Proceedings of the Thirty-Second AAAI Conference on Artificial Intelligence, (AAAI-18), the 30th innovative Applications of Artificial Intelligence (IAAI-18), and the 8th AAAI Symposium on Educational Advances in Artificial Intelligence (EAAI-18), New Orleans, Louisiana, USA, February 2-7, 2018. pp. 6069–6076. AAAI Press (2018), [https://www.aaai.org/ocs/index.php/AAAI/AAAI18/paper/](https://www.aaai.org/ocs/index.php/AAAI/AAAI18/paper/view/16983) [view/16983](https://www.aaai.org/ocs/index.php/AAAI/AAAI18/paper/view/16983)
- <span id="page-19-0"></span>34. Zhu, C., Chen, M., Fan, C., Cheng, G., Zhang, Y.: Learning from history: Modeling temporal knowledge graphs with sequential copy-generation networks. In: Thirty-Fifth AAAI Conference on Artificial Intelligence, AAAI 2021, Thirty-Third Conference on Innovative Applications of Artificial Intelligence, IAAI 2021, The Eleventh Symposium on Educational Advances in Artificial Intelligence, EAAI

2021, Virtual Event, February 2-9, 2021. pp. 4732–4740. AAAI Press (2021), <https://ojs.aaai.org/index.php/AAAI/article/view/16604>

# A Scoring Function Details

## A.1 Entity Prediction

The detailed definition of the EPQs' scoring function is defined as

ϕep(e) = Re < h ′ (sq,tq) , hq, h¯′ (e,tq) > = Re X<sup>d</sup> k=1 h ′ (sq,tq)(k) · <sup>h</sup>q(k) · <sup>h</sup>¯′ (e,tq)(k) ! =< Re h ′ (sq,tq) , Re (hq), Re h ′ (e,tq) > + < Re h ′ (sq,tq) ,Im (hq),Im h ′ (e,tq) > + < Im h ′ (sq,tq) , Re (hq),Im h ′ (e,tq) > − < Im h ′ (sq,tq) ,Im (hq), Re h ′ (e,tq) > . (4)

Re and Im denote taking the real part and the imaginary part of the complex vector, respectively. h ′ (sq,tq) , hq, h ′ (e,tq) <sup>∈</sup> <sup>C</sup> d . h ′ (sq,tq) (k) denotes the kth element of it (same for h<sup>q</sup> and h ′ (e,tq) ). < v1, v2, v<sup>3</sup> >= P<sup>d</sup> <sup>k</sup>=1 v1(k)·v2(k)·v3(k) denotes the dot product of three d-dimensional complex vectors v1, v2, v<sup>3</sup> ∈ C d .

### A.2 Yes-Unknown

The detailed definition of the YUQs' scoring function is defined as

$$
\phi_{yu}(x) = \text{Re} \left( \langle \mathbf{h}'_{(s_q, t_q)}, \mathbf{h}_q, \bar{\mathbf{h}}'_{(o_q, t_q)}, \mathbf{h}_x \rangle \right) \n= \text{Re} \left( \sum_{k=1}^d \mathbf{h}'_{(s_q, t_q)}(k) \cdot \mathbf{h}_q(k) \cdot \bar{\mathbf{h}}'_{(o_q, t_q)}(k) \cdot \mathbf{h}_x(k) \right) \n= \langle \text{ Re } (\mathbf{h}'_{(s_q, t_q)}) , \text{Re } (\mathbf{h}_q) , \text{Re } (\mathbf{h}'_{(o_q, t_q)}) , \text{Re } (\mathbf{h}_x) > \n+ \langle \text{ Re } (\mathbf{h}'_{(s_q, t_q)}) , \text{Im } (\mathbf{h}_q) , \text{Im } (\mathbf{h}'_{(o_q, t_q)}) , \text{Re } (\mathbf{h}_x) > \n+ \langle \text{Im } (\mathbf{h}'_{(s_q, t_q)}) , \text{Re } (\mathbf{h}_q) , \text{Im } (\mathbf{h}'_{(o_q, t_q)}) , \text{Re } (\mathbf{h}_x) > \n+ \langle \text{Re } (\mathbf{h}'_{(s_q, t_q)}) , \text{Re } (\mathbf{h}_q) , \text{Im } (\mathbf{h}'_{(o_q, t_q)}) , \text{Im } (\mathbf{h}_x) > \n- \langle \text{Im } (\mathbf{h}'_{(s_q, t_q)}) , \text{Im } (\mathbf{h}_q) , \text{Re } (\mathbf{h}'_{(o_q, t_q)}) , \text{Re } (\mathbf{h}_x) > \n- \langle \text{Im } (\mathbf{h}'_{(s_q, t_q)}) , \text{Re } (\mathbf{h}_q) , \text{Re } (\mathbf{h}'_{(o_q, t_q)}) , \text{Im } (\mathbf{h}_x) > \n- \langle \text{Im } (\mathbf{h}'_{(s_q, t_q)}) , \text{Im } (\mathbf{h}_q) , \text{Im } (\mathbf{h}'_{(o_q, t_q)}) , \text{Im } (\mathbf{h}_x) > \n- \langle \text{Re} (\mathbf{h}'_{(s_q, t_q)}) , \text{Im } (\mathbf{h}_q) , \text{Re } (\mathbf{h}'_{(o_q, t_q)}) , \text{Im } (\mathbf{h}_x) > \n-
$$

## A.3 Fact Reasoning

The detailed definition of FRQs' scoring function is defined as

$$
\phi_{\text{fr}}(c) = \text{Re} \left( \langle \mathbf{h}'_{(s_c, t_c)}, \mathbf{h}'_q, \bar{\mathbf{h}}'_{(o_c, t_c)}, \mathbf{h}'_q \rangle \right) \n= \text{Re} \left( \sum_{k=1}^d \mathbf{h}'_{(s_c, t_c)}(k) \cdot \mathbf{h}^c_q(k) \cdot \bar{\mathbf{h}}'_{(o_c, t_c)}(k) \cdot \mathbf{h}'_q(k) \right) \n= \langle \text{ Re } (\mathbf{h}'_{(s_c, t_c)}) , \text{Re } (\mathbf{h}^c_q) , \text{Re } (\mathbf{h}'_{(o_c, t_c)}) , \text{Re } (\mathbf{h}'_q(k)) > \n+ \langle \text{ Re } (\mathbf{h}'_{(s_c, t_c)}) , \text{Im } (\mathbf{h}^c_q) , \text{Im } (\mathbf{h}'_{(o_c, t_c)}) , \text{Re } (\mathbf{h}'_q(k)) > \n+ \langle \text{Im } (\mathbf{h}'_{(s_c, t_c)}) , \text{Re } (\mathbf{h}^c_q) , \text{Im } (\mathbf{h}'_{(o_c, t_c)}) , \text{Re } (\mathbf{h}'_q(k)) > \n+ \langle \text{Re } (\mathbf{h}'_{(s_c, t_c)}) , \text{Re } (\mathbf{h}^c_q) , \text{Im } (\mathbf{h}'_{(o_c, t_c)}) , \text{Im } (\mathbf{h}'_q(k)) > \n- \langle \text{Im } (\mathbf{h}'_{(s_c, t_c)}) , \text{Im } (\mathbf{h}^c_q) , \text{Re } (\mathbf{h}'_{(o_c, t_c)}) , \text{Re } (\mathbf{h}'_q(k)) > \n- \langle \text{Im } (\mathbf{h}'_{(s_c, t_c)}) , \text{Re } (\mathbf{h}^c_q) , \text{Re } (\mathbf{h}'_{(o_c, t_c)}) , \text{Im } (\mathbf{h}'_q(k)) > \n- \langle \text{Im } (\mathbf{h}'_{(s_c, t_c)}) , \text{Im } (\mathbf{h}^c_q) , \text{Im } (\mathbf{h}'_{(o_c, t_c)}) , \text{Im } (\mathbf{h}'_q(k)) > \n- \langle \text{Re } (\mathbf{h}'_{(s_c, t_c)}) , \text{Im } (\mathbf{h}^c_q) ,
$$

# B Implementation Details

We implement all the experiments with PyTorch [\[22\]](#page-18-7) on an NVIDIA A40 with 48GB memory and a 2.6GHZ AMD EPYC 7513 32-Core Processor.

## B.1 TKG Forecasting

We train TANGO and TComplEx to perform TKG forecasting on ICEWS21. We implement TANGO with the official implementation[15](#page-21-0). We switch its scoring function to ComplEx and perform a grid search for the embedding size (the dimension d of the entity and relation representations). We keep the rest hyperparameters as TANGO's default setting of the ICEWS05-15 dataset. We train TComplEx with the official implementation[16](#page-21-1). We perform a grid search for the embedding size and keep the other hyperparameters as their default values. Table [8](#page-22-0) provides the searching spaces of the grid searches for both methods. For each method, we run TKG forecasting experiments with different embedding sizes and choose the setting that leads to the best validation MRR as the best hyperparameter setting. We further run TANGO + TuckER with the best hyperparameters searched with TANGO + ComplEx for studying the effectiveness of different KG representations.

<span id="page-21-0"></span><sup>15</sup> https://github.com/TemporalKGTeam/TANGO

<span id="page-21-1"></span><sup>16</sup> https://github.com/facebookresearch/tkbc

<span id="page-22-0"></span>Table 8: Embedding size search space of TANGO and TComplEx. The embedding sizes leading to the best validation results are marked as bold. Note that the numbers represent the dimensions of complex space. Dimensions of real valued vectors are doubled, e.g., a complex vector with embedding size 100 will be transformed into a real valued vector with embedding size 200. The embedding size search spaces are taken from the default search space stated in the original papers of TANGO and TComplEx.

|          | Emebdding Size Search Space |  |
|----------|-----------------------------|--|
| TANGO    | {50, 100, 150}              |  |
| TComplEx | {100, 136, 174}             |  |

Besides, we train ComplEx on ICEWS21 for TKG forecasting. We use the implementation provided in the repository of TComplEx. Since ComplEx is not designed for processing temporal information, we transform every quadruple (s, r, o, t) into a corresponding triplet (s, r, o). We do not remove the repeated triplet. For example, if (s, r, o, t1) and (s, r, o, t2) both exist in the training set of ICEWS21, we train ComplEx with two identical triplets (s, r, o). This preserves the inductive bias brought by the temporal knowledge base. To achieve a fairer comparison between ComplEx and TComplEx, we set the embedding size of ComplEx to 100 (same as the embedding size of TComplEx).

We report in Table [9](#page-22-1) the validation results of the trained TKG models of all three KG reasoning methods on ICEWS21. We observe that TComplEx underperforms ComplEx in TKG forecasting. We attribute this to the excessive noise introduced by TComplEx's representations of unseen timestamps. Note that TComplEx is a TKG completion method. The validation timestamps are unseen during training, thus causing TComplEx to leverage the untrained timestamp representations during evaluation. ComplEx does not consider temporal information, which enables it to avoid the negative influence of the timestamps unseen in the training set. TANGO is designed for TKG forecasting. It outperforms the other methods greatly. Although TANGO + TuckER performs better than TANGO + ComplEx on ICEWS21, we choose the latter one for forecasting TKGQA since it aligns to our QA scoring function better (see Appendix [G](#page-32-0) for detailed discussion).

<span id="page-22-1"></span>Table 9: Validation results of KG reasoning models for TKG forecasting on ICEWS21.

| Metrics               |       |       |       | MRR Hits@1 Hits@3 Hits@10 |
|-----------------------|-------|-------|-------|---------------------------|
| ComplEx               | 0.278 | 0.188 | 0.312 | 0.456                     |
| TComplEx              | 0.250 | 0.164 | 0.279 | 0.420                     |
| TANGO + TuckER        | 0.402 | 0.327 | 0.431 | 0.546                     |
| TANGO + ComplEx 0.389 |       | 0.324 | 0.411 | 0.515                     |

#### B.2 Baseline Details

We use the library HuggingFace's Transformers [\[31\]](#page-19-7) to implement the pre-trained LMs, i.e., BERT and RoBERTa. Following CronKGQA and TempoQR, we choose DistilBERT [\[23\]](#page-18-8) as the BERT model used throughout our work to save computational budget. For every natural language input, e.g., a natural language question, we take the output representation of the [CLS] token computed by an LM as its LM encoded representation.

Pre-trained LM baselines for TKGQA We provide detailed information of our pre-trained LM baselines. For EPQs, BERT and RoBERTa compute the scores of all entities with a prediction head f lm ep : R <sup>2</sup><sup>d</sup> → R |E| as

$$
\Phi_{\rm ep} = f_{\rm ep}^{\rm lm} \left( \mathbf{h}_q \right). \tag{7}
$$

Φep is a |E|-dimensional real valued vector where each element corresponds to the score of an entity. h<sup>q</sup> is the question representation output by BERT or RoBERTa with a projection to a 2d real space. Note that in ForecastTKGQA, we further map the 2d real valued vector to a d-dimensional complex vector. This step does not exist when we implement pre-trained LM baselines without including any TKG representation. We choose the entity with the highest score as the predicted answer. BERT int and RoBERTa int compute the score of each entity e with a prediction head f lm int ep : R <sup>8</sup><sup>d</sup> → R <sup>1</sup> as

$$
\phi_{ep}(e) = f_{ep}^{\text{lm.int}}\left(\mathbf{h}_s \|\mathbf{h}_q\|\mathbf{h}_e\|\mathbf{h}_{t_q}\right),\tag{8}
$$

where hs, ht<sup>q</sup> , and h<sup>o</sup> denote the TComplEx representations of the question's subject entity, the question's timestamp, and the entity e, respectively. Similarly, BERT ext and RoBERTa ext compute the score of each entity e with a prediction head f lm ext ep : R <sup>6</sup><sup>d</sup> → R <sup>1</sup> as

$$
\phi_{ep}(e) = f_{ep}^{\text{lm.ext}}(\mathbf{h}_{(s_q, t_q)} || \mathbf{h}_q || \mathbf{h}_{(e, t_q)}),
$$
\n(9)

where h(sq,tq) and h(e,tq) denote the TANGO representations of the question's subject entity and the entity e, respectively. Since TANGO and TComplEx representations are complex vectors in C d , we expand them into 2d real valued vectors, where the first half of every real valued vector is the real part of the original vector and the second half is the imaginary part. This applies to all the TKG representations used in pre-trained LM baselines for answering all three types of questions.

For yes-unknown questions, BERT and RoBERTa compute the scores of yes and unknown with a prediction head f lm yu : R <sup>2</sup><sup>d</sup> → R <sup>2</sup> as

$$
\Phi_{\text{yu}} = f_{\text{yu}}^{\text{lm}}(\mathbf{h}_q). \tag{10}
$$

Φyu is a 2-dimensional real valued vector where each element corresponds to the score of either yes or unknown. BERT int and RoBERTa int compute the score of each x ∈ {yes, unknown} with a prediction head f lm int yn : R <sup>8</sup><sup>d</sup> → R <sup>1</sup> as

$$
\phi_{\text{yu}}(x) = f_{\text{yn}}^{\text{lm.int}}\left(\mathbf{h}_{s_q} \|\mathbf{h}_q\|\mathbf{h}_{o_q} \|\mathbf{h}_{t_q}\right). \tag{11}
$$

And BERT ext and RoBERTa ext compute the score of each x ∈ {yes, unknown} with a prediction head f lm ext yu : R <sup>6</sup><sup>d</sup> → R <sup>1</sup> as

$$
\phi_{\text{yu}}(x) = f_{\text{yu}}^{\text{lm.ext}}\left(\mathbf{h}_{(s_q, t_q)} \|\mathbf{h}_q\|\mathbf{h}_{(o_q, t_q)}\right). \tag{12}
$$

We choose the one (either yes or unknown) with the higher score as the predicted answer.

For every fact reasoning question, BERT and RoBERTa compute the score of the choice c as

$$
\phi_{\rm fr}(c) = f_{\rm fr}^{\rm lm}(\mathbf{h}_q^c). \tag{13}
$$

h c q is the output of a pre-trained LM when the concatenation of the question q and the choice c is given as the input. f lm fr : <sup>R</sup> <sup>2</sup><sup>d</sup> → R 1 is a layer of neural network for score computation. BERT int and RoBERTa int compute the score of the choice c as

$$
\phi_{\rm fr}(c) = f_{\rm fr}^{\rm lm\_int} \left( \mathbf{h}_q^{\rm lm\_int} \|\mathbf{h}_c^{\rm lm\_int} \right). \tag{14}
$$

h lm int <sup>q</sup> = hs<sup>q</sup> ∥h c <sup>q</sup>∥ho<sup>q</sup> ∥ht<sup>q</sup> , where hs<sup>q</sup> , ho<sup>q</sup> and ht<sup>q</sup> denote the TComplEx representations of the question's subject entity, object entity and timestamp, respectively. h lm int <sup>c</sup> = hs<sup>c</sup> ∥h c <sup>q</sup>∥ho<sup>c</sup> ∥ht<sup>c</sup> , where hs<sup>c</sup> , ho<sup>c</sup> and ht<sup>c</sup> denote the TComplEx representations of the choice's subject entity, object entity and timestamp, respectively. f lm int fr : <sup>R</sup> <sup>16</sup><sup>d</sup> → R 1 is a layer of neural network for score computation. Similarly, BERT ext and RoBERTa ext compute the score of the choice c as

$$
\phi_{\rm fr}(c) = f_{\rm fr}^{\rm lm. ext}(\mathbf{h}_q^{\rm lm. ext} || \mathbf{h}_c^{\rm lm. ext}). \tag{15}
$$

h lm ext <sup>q</sup> = h(sq,tq)∥h c <sup>q</sup>∥h(oq,tq) , where h(sq,tq) and h(oq,tq) denote the time-aware TANGO representations of the question's subject entity and object entity, respectively. h lm ext <sup>c</sup> = h(sc,tc)∥h c <sup>q</sup>∥h(oc,tc) , where h(sc,tc) and h(oc,tc) denote the time-aware TANGO representations of the choice's subject entity and object entity, respectively. f lm ext fr : <sup>R</sup> <sup>12</sup><sup>d</sup> → R 1 is a layer of neural network for score computation.

KGQA & TKGQA Baselines For EmbedKGQA, we use the trained ComplEx representations as its supporting KG information. For CronKGQA and TempoQR, we use the trained TComplEx representations as their supporting TKG information. We use the EmbedKGQA and CronKGQA implementation provided in the repository of CronKGQA[17](#page-24-0). We use the official implementation of TempoQR[18](#page-24-1). Since we annotate the timestamps for every entity prediction question in ForecastTKGQuestions, we do not implement soft/hard supervision proposed in TempoQR. We skip the soft/hard supervision and keep everything else as same as the original implementation. We implement all the KGQA baselines with their default hyperparameter settings.

<span id="page-24-0"></span><sup>17</sup> https://github.com/apoorvumang/CronKGQA

<span id="page-24-1"></span><sup>18</sup> https://github.com/cmavro/TempoQR

| Hyperparameter | Search Space                         |
|----------------|--------------------------------------|
| TKG Model      | {TuckER, ComplEx}                    |
|                | Language Model {DistilBERT, RoBERTa} |
| Dropout        | {0.2, 0.3, 0.5}                      |
| Batch Size     | {32, 64, 128, 256, 512}              |

<span id="page-25-0"></span>Table 10: ForecastTKGQA hyperparameter searching strategy.

| Table 11: Best hyperparameter setting. |  |  |  |  |  |  |
|----------------------------------------|--|--|--|--|--|--|
|----------------------------------------|--|--|--|--|--|--|

<span id="page-25-1"></span>

| Question Type  | Entity Prediction Yes-Unknown Fact Reasoning |            |            |
|----------------|----------------------------------------------|------------|------------|
| Hyperparameter |                                              |            |            |
| TKG Model      | ComplEx                                      | ComplEx    | ComplEx    |
| Language Model | DistilBERT                                   | DistilBERT | DistilBERT |
| Dropout        | 0.3                                          | 0.3        | 0.3        |
| Batch Size     | 512                                          | 256        | 256        |

<span id="page-25-2"></span>Table 12: Experimental results of EPQs on the validation set. Evaluation metrics are MRR and Hits@1/10.

|               |       | MRR |             |       | Hits@1 |             |                                                             | Hits@10 |             |
|---------------|-------|-----|-------------|-------|--------|-------------|-------------------------------------------------------------|---------|-------------|
| Model         |       |     |             |       |        |             | Overall 1-Hop 2-Hop Overall 1-Hop 2-Hop Overall 1-Hop 2-Hop |         |             |
| ForecastTKGQA | 0.297 |     | 0.342 0.192 | 0.206 |        | 0.247 0.111 | 0.475                                                       |         | 0.526 0.353 |

### B.3 ForecastTKGQA

We search hyperparameters of ForecastTKGQA following Table [10.](#page-25-0) For every type of question, we do 60 trials, and let our model run for 50 epochs. We select the trial leading to the best performance on the validation set and take this hyperparameter setting as our best configuration. We train our model five times with different random seeds and report averaged results. The best hyperparameters concerning all three types of questions are shown in Table [11.](#page-25-1) We also report the model performance on the validation sets in Table [12](#page-25-2) and Table [14.](#page-26-0) We further report the standard deviation of the results on the test sets in Table [13](#page-26-1) and Table [15.](#page-26-2) The GPU memory usage is reported in Table [16.](#page-26-3) The training time and test time of our model are presented in Table [17](#page-26-4) and Table [18.](#page-26-5) The number of parameters of our model is presented in Table [19.](#page-27-0)

<span id="page-26-1"></span>

|       | MRR                                                                          | Hits@1 | Hits@10 |
|-------|------------------------------------------------------------------------------|--------|---------|
| Model | Overall 1-Hop 2-Hop Overall 1-Hop 2-Hop Overall 1-Hop 2-Hop                  |        |         |
|       | ForecastTKGQA 0.0004 0.0004 0.0009 0.0006 0.0007 0.0007 0.0008 0.0008 0.0018 |        |         |

Table 13: Standard deviation of the results of EPQs on the test set.

<span id="page-26-0"></span>Table 14: Experimental results of YUQs and FRQs on the validation sets. The evaluation metric is accuracy.

|               | Accuracy |                            |  |  |
|---------------|----------|----------------------------|--|--|
| Question Type |          | Yes-Unknown Fact Reasoning |  |  |
| ForecastTKGQA | 0.873    | 0.758                      |  |  |

<span id="page-26-2"></span>Table 15: Standard deviation of the results of YUQs and FRQs on the test set.

|               | Accuracy |                            |  |  |
|---------------|----------|----------------------------|--|--|
| Question Type |          | Yes-Unknown Fact Reasoning |  |  |
| ForecastTKGQA | 0.0013   | 0.0052                     |  |  |

Table 16: GPU memory usage.

<span id="page-26-3"></span>

| Question Type | Entity Prediction Yes-Unknown Fact Reasoning |            |            |
|---------------|----------------------------------------------|------------|------------|
| Model         | GPU Memory                                   | GPU Memory | GPU Memory |
| ForecastTKGQA | 45,239MB                                     | 12,241MB   | 22,719MB   |

<span id="page-26-4"></span>Table 17: Training time (second) of ForecastTKGQA on all types of questions. Question Type Entity Prediction Yes-Unknown Fact Reasoning

| Model         |        |       |      |  |
|---------------|--------|-------|------|--|
| ForecastTKGQA | 63,840 | 3,700 | 5000 |  |

<span id="page-26-5"></span>Table 18: Test time (second) of ForecastTKGQA on all types of questions.

| Question Type | Entity Prediction Yes-Unknown Fact Reasoning |    |   |
|---------------|----------------------------------------------|----|---|
| Model         |                                              |    |   |
| ForecastTKGQA | 48                                           | 33 | 3 |

<span id="page-27-0"></span>Table 19: Number of parameters of ForecastTKGQA on all types of questions.

| Question Type | Entity Prediction Yes-Unknown Fact Reasoning |         |         |
|---------------|----------------------------------------------|---------|---------|
| Model         |                                              |         |         |
| ForecastTKGQA | 234,600                                      | 234,600 | 354,800 |

# C ForecastTKGQuestions Details

## C.1 Natural Language Relation Template

After we get ICEWS21, we get a TKG with 253 relation types. We create natural language relation templates for 250 out of 253 relation types for question generation. The rest three relation types in ICEWS21 are not taken into consideration because either the verb is not suited for a question in the future tense (Attempt to assassinate) or there is no clear description for the subject-object-relationship of the relation type in [\[3\]](#page-16-0) (Demobilize armed forces and Demonstrate military or police power ). We use the generated relation templates for question generation of all three types of questions. For fact reasoning questions, we also use these relation templates to generate natural language choices.

## C.2 Natural Language Question Template

All question templates are presented in Question Generation/template icews.xlsx which is attached with the submission in Easychair. 2-hop EPQs and their templates are generated with Question Generation/generate qa anyburl.py.

## C.3 2-Hop EPQ Generation Details

We generate 2-hop questions by utilizing AnyBURL [\[21\]](#page-18-4), a rule-based KG reasoning model. We first split ICEWS21 into TKG snapshots, where each snapshot Gt<sup>i</sup> = {(s, r, o, t) ∈ G|t = ti} contains all the TKG facts happening at the same timestamp. We treat every TKG snapshot as a non-temporal KG and train an AnyBURL model with the KG completion task on each TKG snapshot for rule extraction (KG completion aims to predict the missing entity from every query (s, r, ?)). Since AnyBURL is a KG reasoning method that cannot process temporal information, we transform every quadruple (s, r, o, t) into a corresponding triplet (s, r, o). For each TKG snapshot, we keep the 2-hop rules with a confidence higher than 0.5 extracted by AnyBURL, and manually check if two associated TKG facts in each rule potentially have a logical causation or can be used to interpret positive/negative entity relationships. After this process, we take the remaining 2-hop rules as the drafts for generating 2 hop EPQ templates. The complete list of extracted 2-hop rules is presented in Question Generation/anyburl ICEWS.txt. 2-hop EPQs and their templates are generated with Question Generation/generate qa anyburl.py, given the extracted rules.

#### C.4 FRQ Generation Details

We train xERTE [\[9\]](#page-16-3) on ICEWS21 for TKG forecasting, and pick out all the link prediction queries (s, r, ?, t) whose ground-truth missing entities are ranked by xERTE as top 1. We collect the TKG facts corresponding to these queries for question generation. The intuition of this step is that we assume that the better xERTE performs on a link prediction query, the more reasonable the returned prior facts are for explainability. Ranking the ground-truth missing entities as top 1 indicates that xERTE performs very well on these link prediction queries. We wish to use xERTE to generate reasonable fact reasoning questions, therefore, we want it to find reasonable supporting evidence of the TKG facts by returning relevant prior facts. For each collected top 1 fact, we take the prior facts with the highest contribution score, the lowest contribution score, the median contribution score, and the second highest contribution score as the facts for generating the choices Answer, Negative, Median and Hard Negative, respectively. In this way, we can generate a large number of question candidates by fitting the corresponding facts into question templates.

After we collect all the question candidates, we have 78,606 questions. We find that there exist a large number of question candidates whose question and Answer share the same s, r, o. For example, the TKG fact of a question candidate is (Sudan, host, Ramtane Lamamra, 2021-08-01 ), and the TKG fact of its Answer is (Sudan, host, Ramtane Lamamra, 2021-07-29 ). We filter out all the question candidates with this pattern since we think that they are not satisfying our motivation for proposing fact reasoning questions. We wish to generate the questions that require fact reasoning, rather than finding the repeated facts happening at different timestamps. A good example of the questions we want to generate is as follows. For the question whose associated fact is (Envoy (United States), visit, China, 2021-08-31 ), the associated fact of its Answer is (Envoy (United States), express the intent to meet or negotiate, China, 2021-08-30 ). From human knowledge, Answer's fact serves as a highly possible reason for the fact in the question, and it is also diverse from the question fact. To this end, we have 50,379 question candidates left.

We then ask five graduate students (major in computer science) to further annotate the remaining question candidates by deciding whether each of them is reasonable or not. Students are allowed to use their own knowledge and search engines to help annotation. If the students think that a question's Answer is not the most contributive to the question, they are asked to annotate this question as unreasonable, otherwise, they are asked to annotate it as reasonable. For every question candidate, if it is annotated as unreasonable by three students, we filter it out. As a result, we have 4,195 questions left. We use Fleiss' kappa to measure inter-annotator agreement. Fleiss' kappa is 0.63 in our annotation process. The estimated annotation time for each student is 320 hours. The annotation instruction and interface are presented in Figure [9](#page-34-0) and [10,](#page-35-0) respectively.

<span id="page-29-0"></span>![](_page_29_Figure_0.jpeg)
<!-- Image Description: The image contains two time-series line graphs showing the number of questions over 250 days.  Graph (a) displays "Entity Prediction" and "Yes-Unknown" question types, exhibiting fluctuating daily counts. Graph (b) shows "Fact Reasoning" questions, also demonstrating daily fluctuations, but with a smaller overall range than (a).  The graphs illustrate the temporal distribution of different question types in a dataset. -->

Fig. 5: Question distribution of different types of questions along the time axis.

### C.5 Question Time Distribution

We provide the distribution of the questions along the time axis of our dataset in Figure [5a](#page-29-0) and Figure [5b.](#page-29-0) We plot the number of questions at every timestamp for all three types of questions. The numbers on the horizontal axis denote how many days away from 2021-01-01.

# D Full Experimental Results on EPQs

We present Table [20](#page-29-1) as the supplement of the main results regarding EPQs in the main paper. We present the aggregated overall performance of MRR and Hits@k.

|                                                |                                  | MRR |                                                          |                                  | Hits@1 |                                                    |                                                             | Hits@10 |                                                          |
|------------------------------------------------|----------------------------------|-----|----------------------------------------------------------|----------------------------------|--------|----------------------------------------------------|-------------------------------------------------------------|---------|----------------------------------------------------------|
| Model                                          |                                  |     |                                                          |                                  |        |                                                    | Overall 1-Hop 2-Hop Overall 1-Hop 2-Hop Overall 1-Hop 2-Hop |         |                                                          |
| RoBERTa<br>BERT                                | 0.161<br>0.253                   |     | 0.166 0.149<br>0.279 0.182                               | 0.098<br>0.168                   |        | 0.104 0.085<br>0.192 0.106                         | 0.282<br>0.421                                              |         | 0.288 0.268<br>0.451 0.342                               |
| EmbedKGQA                                      | 0.278                            |     | 0.317 0.185                                              | 0.194                            |        | 0.228 0.112                                        | 0.443                                                       |         | 0.489 0.333                                              |
| RoBERTa int<br>BERT int<br>CronKGQA<br>TempoQR | 0.246<br>0.275<br>0.119<br>0.134 |     | 0.283 0.157<br>0.314 0.183<br>0.131 0.090<br>0.145 0.107 | 0.162<br>0.189<br>0.069<br>0.085 | 0.081  | 0.190 0.094<br>0.223 0.107<br>0.042<br>0.094 0.061 | 0.415<br>0.447<br>0.218<br>0.230                            |         | 0.467 0.290<br>0.490 0.344<br>0.231 0.187<br>0.243 0.199 |
| RoBERTa ext<br>BERT ext                        | 0.269<br>0.295                   |     | 0.306 0.180<br>0.331 0.208                               | 0.184<br>0.206                   |        | 0.216 0.108<br>0.239 0.128                         | 0.433<br>0.467                                              | 0.497   | 0.323<br>0.508 0.369                                     |
| ForecastTKGQA                                  |                                  |     |                                                          |                                  |        |                                                    | 0.303 0.339 0.216 0.213 0.248 0.129 0.478 0.517 0.386       |         |                                                          |

<span id="page-29-1"></span>Table 20: Complete experimental results of EPQs. The best results are marked in bold.

# E Human Benchmark Details

We ask five graduate students (major in computer science, not participating in annotation during FRQ generation) to answer 100 questions randomly sampled from the test set of FRQs. We consider two settings: (a) Humans answer FRQs with their own knowledge and inference ability. Search engines are not allowed; (b) Humans can turn to search engines and use the web information published before the question timestamp for aiding QA. We create a survey that contains the selected 100 questions. Figure [7a](#page-31-0) and [7b](#page-31-0) show the instruction of survey and the interface of answering. We first ask the students to do the survey in setting (a), and then ask them to do it once again in setting (b). The ground-truth answers to survey questions are not shown to students throughout the whole process. Also, students have no idea which question they answer incorrectly. Thus, they cannot use this information to exclude wrong choices when they do the survey for the second time. From Table 5 of the main paper, we observe that with search engines, humans can better answer FRQs, although humans can already reach 0.936 accuracy without any additional information source.

Example to explain accuracy improvement from setting (a) to (b). We present an example explaining the human performance improvement from setting (a) to (b). Figure [6](#page-30-0) shows a question in the generated survey for human benchmark. In setting (a), 3 of 5 students make a mistake by choosing A. After being allowed to use search engines in setting (b), they all choose the correct choice B. This is because in setting (a), most students have no idea that Alberto Fern´andez is the president of Argentina. But after using search engines, they know the identity of Alberto Fern´andez and manage to achieve correct reasoning.

<span id="page-30-0"></span>

|                | Which of the following statements contributes most to the fact that Agustin Rossi       |
|----------------|-----------------------------------------------------------------------------------------|
|                | had a consolation or a meeting with Alberto Fernández on 2021-08-01?                    |
|                | A. Alberto Fernández expressed the intent to meet or negotiate with Peru on 2021-07-26. |
|                | B. Agustín Rossi visited Argentina on 2021-07-31.                                       |
|                | C. Agustín Rossi had a consolation or a meeting with Brazil on 2021-01-30.              |
|                | <b>D.</b> United Kingdom engaged in diplomatic cooperation with European Union          |
| on 2021-06-10. |                                                                                         |
|                |                                                                                         |

Fig. 6: Example question in the human benchmark survey.

# F Details of Multi-Hop Scorer

We develop a QA model, i.e., Multi-Hop Scorer (MHS), for non-forecasting TKGQA (the TKGQA task proposed in [\[24\]](#page-18-0)). We use it to prove that given the

<span id="page-31-0"></span>

| (a) Survey insturction. |
|-------------------------|
|                         |
|                         |
|                         |
|                         |
|                         |
|                         |
|                         |

(b) Survey interface.

Fig. 7: Human benchmark survey instruction and interface.

ground-truth TKG information at the question timestamp t<sup>q</sup> (same setting as non-forecasting TKGQA), the EPQs in ForecastTKGQuestions are answerable. Considering the non-forecasting setting, we equip MHS with two cheating TKG models (CTComplEx and CTANGO) and also design MHS by considering the multi-hop graphical structure of the snapshot G<sup>t</sup><sup>q</sup> = {(s, r, o, t) ∈ G|t = tq}. We illustrate MHS's model structure with an example in Fig. [8.](#page-33-0) Starting from the annotated subject entity s<sup>q</sup> of an EPQ, MHS updates the scores of outer entities for n-hops (n = 2 in our experiments) until all sq's n-hop neighbors on the snapshot G<sup>t</sup><sup>q</sup> are visited. Initially, MHS assigns a score of 1 to s<sup>q</sup> and 0 to any other unvisited entity. For each unvisited entity e, it then computes e's score as:

$$
\bar{\phi}_{ep}(e) = \sum_{(e',r)\in\mathcal{N}_e(t_q)} (\gamma \cdot \phi_{ep}(e') + \psi(e',r,e,t_q)),
$$
  
\n
$$
\phi_{ep}(e) = \frac{1}{|\mathcal{N}_e(t_q)|} \bar{\phi}_{ep}(e),
$$
\n(16)

where Ne(tq) = {(e ′ , r)|(e ′ , r, e, tq) ∈ Gt<sup>q</sup> } is e's 1-hop neighborhood on the snapshot Gt<sup>q</sup> and γ is a discount factor. We couple MHS with CTComplEx and CTANGO, and define ψ(e ′ , r, e, tq) separately. For MHS + CTComplEx, we define

$$
\psi(e',r,e,t_q) = f_2(f_1(\mathbf{h}_{e'}||\mathbf{h}_r||\mathbf{h}_{e}||\mathbf{h}_{t_q}||\mathbf{h}_q)).
$$
\n(17)

f<sup>1</sup> : R <sup>10</sup><sup>d</sup> → R 2d , f<sup>2</sup> : R <sup>2</sup><sup>d</sup> → R <sup>1</sup> are two neural networks. he, h<sup>e</sup> ′ , hr, ht<sup>q</sup> are the CTComplEx representations of entities e, e ′ , relation r and timestamp tq, respectively. For MHS + CTANGO, we take the idea of ForecastTKGQA and define

$$
\psi(e', r, e, t_q) = \text{Re}\left( \langle \mathbf{h}_{(e', t_q)}, \mathbf{h}_r, \bar{\mathbf{h}}_{(e, t_q)}, \mathbf{h}_q \rangle \right). \tag{18}
$$

h(e,tq) , h(<sup>e</sup> ′ ,tq) are the CTANGO entity representations of e, e ′ at tq, respectively. h<sup>r</sup> is the CTANGO relation representation of r. h<sup>q</sup> is BERT encoded question representation.

# <span id="page-32-0"></span>G Further Analysis on ForecastTKGQA

Ablation on KG Representations We conduct an ablation study by comparing the performance of ForecastTKGQA coupled with different KG (TKG) representations. We first train ComplEx on ICEWS21 and provide our model with its representations. We observe in Table [21](#page-33-1) that TANGO representations are more effective than static KG representations in our proposed model. Besides, we switch TANGO's scoring function to TuckER [\[1\]](#page-16-9) when we train TANGO on ICEWS21. Table [21](#page-33-1) shows that TANGO + ComplEx aligns better to our QA module.

<span id="page-33-0"></span>![](_page_33_Figure_1.jpeg)
<!-- Image Description: The image displays a methodology for question answering.  A graph depicts a two-hop neighborhood network around Sudan, nodes representing individuals and edges representing actions (e.g., "host a visit").  Equations detail a score computation based on this network, incorporating a BERT-based question encoding  (shown as [CLS], Q, [SEP] input tokens). The overall process involves using the ICEWS21 network data, processed via CTANGO or CTComplEx, to generate scores for answering the question: "Who will Sudan host on 2021-08-01?". -->

Fig. 8: Assume we have a question: Who will Sudan host on 2021-08-01? The annotated subject entity s<sup>q</sup> is Sudan and the annotated timestamp t<sup>q</sup> is 2021- 08-01. We first pick the snapshot Gt<sup>q</sup> and find sq's n-hop (n = 2 in our case) neighbors on Gt<sup>q</sup> . Starting from sq, MHS updates the scores of outer entities for 2-hops until all sq's 2-hop neighbors on Gt<sup>q</sup> ({Ramtane Lamamra (e1), Sameh Shoukry, Samantha Power, Alfredo Rangel, Irakli Ghudushauri-Shiolashvili (e2), Ahmadu Umaru Fintiri (e3), Other Authorities/Officials (Algeria), Foreign Affairs (Albania), Foreign Affairs (Cyprus) } in our example) are visited. Initially, MHS assigns a score of 1 to s<sup>q</sup> and 0 to any other unvisited entity. To be specific, MHS first propagates scores to sq's 1-hop neighbors on Gt<sup>q</sup> , e.g., e1. Then through the visited 1-hop neighbors, MHS propagates scores to sq's 2-hop neighbors. Score computation for e1, e2, e<sup>3</sup> is presented in this figure. r −1 <sup>2</sup> denotes the inverse relation of r<sup>2</sup> that points from s<sup>q</sup> to e1. We transform r<sup>2</sup> to r −1 <sup>2</sup> because we define the 1-hop neighbor of an entity with its incoming edges (following TANGO [\[10\]](#page-16-2)). Scores are computed by considering the graphical structure of Gt<sup>q</sup> . After the score propagation process, the entity with the highest score is taken as the predicted answer eans.

<span id="page-33-1"></span>Table 21: Comparison of different KG representations. w. means with. EPQ, YUQ, FRQ represent entity prediction, yes-unknown and fact reasoning questions, respectively.

| Question Type                                                                          | EPQ |  |  |                                                             |  |  |         |  |  | YUQ   | FRQ               |
|----------------------------------------------------------------------------------------|-----|--|--|-------------------------------------------------------------|--|--|---------|--|--|-------|-------------------|
|                                                                                        | MRR |  |  | Hits@1                                                      |  |  | Hits@10 |  |  |       | Accuracy Accuracy |
| Model                                                                                  |     |  |  | Overall 1-Hop 2-Hop Overall 1-Hop 2-Hop Overall 1-Hop 2-Hop |  |  |         |  |  |       |                   |
| ForecastTKGQA w. ComplEx                                                               |     |  |  | 0.296 0.338 0.196 0.207 0.245 0.114 0.470 0.516 0.358       |  |  |         |  |  | 0.863 | 0.752             |
| ForecastTKGQA w. TANGO + TuckER                                                        |     |  |  | 0.298 0.335 0.211 0.210 0.245 0.125 0.474 0.511 0.385       |  |  |         |  |  | 0.867 | 0.757             |
| ForecastTKGQA w. TANGO + ComplEx 0.303 0.339 0.216 0.213 0.248 0.129 0.478 0.517 0.386 |     |  |  |                                                             |  |  |         |  |  | 0.870 | 0.769             |

#### <span id="page-34-0"></span>**Annotation Instruction**

You will be given a number of machine-generated multiple-choice questions. Each of them is coupled with four choices. You will also be given the answer labeled by machines. For every question, your task is to distinguish whether the machine labeled answer is correct (i.e., reasonable) or incorrect (i.e., unreasonable). If the machine labels correctly, please annotate the corresponding question as "reasonable", otherwise, please annotate the question as "unreasonable".

Each question is centered around a political fact (i.e., **centered fact**). **Each choice denotes a different fact that happens before the centered fact**. The answer to each question should be the choice that serves as the **most relevant evidence (cause) of the centered fact among all choices.**

#### **Note:**

(1) Pay attention to the time information specified in the facts.

(2) If none of four choices potentially leads to the centered fact, please annotate the corresponding question as unreasonable. (3) If more than one choices seem relevant and you cannot decide which choice is the best, please also annotate as unreasonable. (4) Feel free to use search engines, e.g., Google, to support your annotation process.

Here are two examples explaining which kind of questions should be annotated as "reasonable" and which should be annotated as "unreasonable".

Example 1:

Which of the following statements contributes most to the fact that Pedro Sanchez signed a formal agreement with Joseph Robinette Biden on 2021-08-23?

A. Pedro Sanchez expressed the intent to cooperate with Joseph Robinette Biden on 2021-08-22.

B. Pedro Sanchez engaged in diplomatic cooperation with Government (Spain) on 2021-08-22.

C. Government (Spain) made a statement to Cuba on 2021-07-27.

D. United States praised or endorsed Sayyid Ali al-Husayni al-Sistani on 2021-07-24.

Machine labeled A as the answer to this question. From human perspective, A is the strong cause of the centered fact and B, C, D are not relevant compared with A. Therefore, this question should be annotated as "reasonable".

Example 2:

Which of the following statements contributes most to the fact that Emmanuel Macron negotiated with Kamala Harris on 2021-02-18.? A. Emmanuel Macron had a consolation or a meeting with Saad Hariri on 2021-02-14.

B. Emmanuel Macron negotiated with Saad Hariri on 2021-02-12.

C. Military (France) attacked France using aerial weapons on 2021-01-08.

D. Vladimir Putin made a statement to Iran on 2021-02-09.

Machine labeled A as the answer to this question. In fact, from human perspective, all four choices cannot serve as an obviously relevant cause of the centered fact. Therefore, this question should be annotated as "unreasonable".

#### **How to annotate?**

You will be given an excel form containing questions and choices. The question is in Column B (Machine-Generated Question), and the machine-labeled answer is in Column C (Machine-Labeled Answer). Column D, E, F contain other choices generated by machines. Each row in the excel form corresponds to one multiple-choice question. If you think the question is "reasonable" please write 1 in Column G (Annotation Result) in the corresponding row, otherwise, please write 0. For example, if you think the question in row 1337 is unreasonable, please write 0 at G1337 of the excel form.

#### **Why annotate?**

The annotation process of the machine-generated questions will help to generate a dataset that tests machines' ability of fact reasoning and forecasting in the context of temporal knowledge question answering (TKGQA). This annotation process also aims to promote high quality dataset generation. Further, more humans will be asked to answer the sampled questions in the generated dataset for studying the difference between humans and machines in fact reasoning.

Fig. 9: Human annotation instruction for fact reasoning questions.

<span id="page-35-0"></span>![](_page_35_Picture_1.jpeg)
<!-- Image Description: The image is a table summarizing the results of a machine-learning question-answering task.  Columns represent different question variations (Machine-Generated Question, Machine-Labeled Answer, and three Other Choices), and rows correspond to individual questions.  Each cell contains a natural language description of the question or answer and a date. The final column shows the interaction result. The table's purpose is to present the performance of the model across various question formulations. -->

Fig. 10: Human annotation interface for fact reasoning questions.