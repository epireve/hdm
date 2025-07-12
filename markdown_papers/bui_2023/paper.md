---
cite_key: bui_2023
relevancy: Medium
date_processed: 2025-07-13
---


# Cross-Data Knowledge Graph Construction for LLM-enabled Educational Question-Answering System: A Case Study at HCMUT

Tuan Bui^*^ tuanbc88@hcmut.edu.vn Ho Chi Minh City University of Technology (HCMUT) HoChiMinhCity, VietNam

Bao Ho bao.ho64qubit@hcmut.edu.vn Ho Chi Minh City University of Technology (HCMUT) HoChiMinhCity, VietNam

Oanh Tran oanh.tranotsc1123@hcmut.edu.vn Ho Chi Minh City University of Technology (HCMUT) HoChiMinhCity, VietNam

Long Nguyen long.nguyencse2023@hcmut.edu.vn Ho Chi Minh City University of Technology (HCMUT) HoChiMinhCity, VietNam

Tho Quan† qttho@hcmut.edu.vn Ho Chi Minh City University of Technology (HCMUT) HoChiMinhCity, VietNam

Phuong Nguyen phuong.nguyenvoid@hcmut.edu.vn Ho Chi Minh City University of Technology (HCMUT) HoChiMinhCity, VietNam

Thang Bui† bhthang@hcmut.edu.vn Ho Chi Minh City University of Technology (HCMUT) HoChiMinhCity, VietNam

## ABSTRACT

In today's rapidly evolving landscape of Artificial Intelligence, large language models (LLMs) have emerged as a vibrant research topic. LLMs find applications in various fields and contribute significantly. Despite their powerful language capabilities, similar to pre-trained language models (PLMs), LLMs still face challenges in remembering events, incorporating new information, and addressing domainspecific issues or hallucinations. To overcome these limitations, researchers have proposed Retrieval-Augmented Generation (RAG) techniques, some others have proposed the integration of LLMs with Knowledge Graphs (KGs) to provide factual context, thereby improving performance and delivering more accurate feedback to user queries.

Education plays a crucial role in human development and progress. With the technology transformation, traditional education is being replaced by digital or blended education. Therefore, educational data in the digital environment is increasing day by day. Data in higher education institutions are diverse, comprising various sources such as unstructured/structured text, relational databases, web/app-based API access, etc. Constructing a Knowledge Graph from these cross-data sources is not a simple task. This article proposes a method for automatically constructing a Knowledge Graph from multiple data sources and discusses some initial applications (experimental trials) of KG in conjunction with LLMs for question-answering tasks.

## TL;DR

Knowledge graph-augmented LLM system for educational question answering with

## Key Insights

KG integration improves LLM accuracy by providing factual context, reduces hallucinations, enables domain-specific knowledge management

## CCS CONCEPTS

- Computing methodologies → Information extraction; Ontology engineering;
- Information systems → Ontologies; Question answering; Clustering and classification.

## KEYWORDS

Open Intent Discovery, Knowledge Graph, Large language model, Education, Question-Answering System

## 1 INTRODUCTION

A Large Language Model (LLM) is a language model trained on a considerably large size corpus. Nowadays, LLMs attract much attention from various communities due to their capacity to accomplish versatile language generation and comprehension. Notable LLM models reported to the public include OpenAI's GPT [23], Google's BART [15], LLaMa [26]. To achieve a broad spectrum of general knowledge [22] and refine their language ability [30], state-of-theart LLMs nowadays are trained on a massive corpus of textual data. However, an LLM's completion might contain "hallucinations" [11] because of limited access to information that is as up-to-date, proprietary, or domain-specific as humans. To address this issue and other limitations, some hybrid models have shown prominent results by combining parametric memory with non-parametric memory [13]. Since their knowledge bases can be directly revised and expanded, and retrieved knowledge can be inspected and interpreted. This technique, which received a lot of traction after the publication of the famous Facebook research paper [16], is well-known and coined as Retrieval-Augmented Generation (RAG).

However, in most real-world domains such as education, the data/information often originate from various departments and faculties within an institution, resulting in diverse data sources with different natures such as structured text, unstructured text, databases, images, or access through API mechanisms from existing web/app-based systems. For instance, at Ho Chi Minh City University of Technology (HCMUT)[^1], unstructured data originate from legal documents, frequently asked questions (FAQs) from student support systems BKSI[^2] (Help Desk System), news from the website, data from databases, and information retrieved from API-enabled systems like teaching management systems LMS[^3]. Due to the crossdata nature, Knowledge Graphs (KGs) [9] serve as a suitable nonparametric memory formalism for knowledge representation in the educational environment, allowing the effective deployment of a RAG system in this context. However, constructing a Knowledge Graph from multiple data sources, not specifically designed to be interoperable, is not a trivial task, in particular when one needs to deal with open intents [ref] commonly arising during casual conversations between students and the university staffs. Hence, to the best of our knowledge, there has not been a best-practice application of RAG from KG for LLMs in practical scenarios.

In this paper, we aim to pioneer a KG-based RAG approach for an Educational Question-Answering system. We propose a framework for the cross-data knowledge graph construction in the educational domain, which is currently implemented at HCMUT and leverages the Vietnamese language. This framework is applied as a pilot in a Language Model (LLM)-based system. Our contributions are of three-fold: (i) We introduce the technique of intental entity discovery for unstructured text in Vietnamese FAQ conversations; (ii) we present the embedding-based cross-data for relation discovery on education KG construction; and (iii) we conduct real-world experiments, specifically, LLM-enabled KG-based Question-Answering at HCMUT using RAG with the constructed educational KG.

## 2 RELATED WORK

### 2.1 Open Intent Discovery

The task of Open Intent Discovery [3] presents several challenges and difficulties in the field of Natural Language Understanding and dialogue systems. One significant challenge is the inherent ambiguity and variability in user expressions. Unlike traditional intent recognition, where a predefined set of categories is used for classification, open intent discovery involves identifying user intents that may not have been encountered during the training phase. This introduces a level of uncertainty and unpredictability, as users can express their intents in diverse and unanticipated ways. Another challenge is the lack of sufficient labeled data for training models in an open-world setting. Creating labeled datasets for every potential intent becomes impractical, especially when dealing with a wide range of domains and applications. This scarcity of annotated examples for novel intents makes it challenging for models to generalize effectively and accurately identify open intents. In recent years, there has been an increased interest in determining user intent from both written and spoken language, with a focus on modeling and comprehending interactions. Recent studies, such as a method employing a bidirectional LSTM and CRF for detecting user intent efficiently [27], an unsupervised two-stage approach aimed at discovering intents and generating meaningful intent labels automatically from unlabeled utterances [28], and a method mining unlabeled utterance data to uncover common intents [17]. These studies collectively highlight the significance of robust approaches for understanding user intent, paving the way for enhanced dialogue systems and virtual assistants. Open intents has been studied in fields such as Customer Care in businesses [17, 28] and Healthcare facilities[19]; however, in the realm of education, particularly in Student Care, it remains relatively unexplored.

### 2.2 Knowledge Graph in Education Domain

Knowledge Graphs (KGs) have evolved as an effective way to represent knowledge. KGs present a structured and integrated representation of concepts, relationships, and attributes within a domain. There have been many studies on Educational KGs such as knowledge graph for mathematics [4], ontology modeling university teaching programs and student profiles (EducOnto) [10], knowledge schema for university teaching [24],
