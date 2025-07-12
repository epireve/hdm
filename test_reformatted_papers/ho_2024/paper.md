---
---

# Cross-Data Knowledge Graph Construction for LLM-enabled Educational Question-Answering System: A Case Study at HCMUT

[Tuan Bui](https://orcid.org/0000-0002-8587-182X)^* tuanbc88@hcmut.edu.vn Ho Chi Minh City University of Technology (HCMUT) HoChiMinhCity, VietNam

Bao Ho bao.ho64qubit@hcmut.edu.vn Ho Chi Minh City University of Technology (HCMUT) HoChiMinhCity, VietNam

Oanh Tran oanh.tranotsc1123@hcmut.edu.vn Ho Chi Minh City University of Technology (HCMUT) HoChiMinhCity, VietNam

Long Nguyen long.nguyencse2023@hcmut.edu.vn Ho Chi Minh City University of Technology (HCMUT) HoChiMinhCity, VietNam

[Tho Quan](https://orcid.org/0000-0003-0467-6254)† qttho@hcmut.edu.vn Ho Chi Minh City University of Technology (HCMUT) HoChiMinhCity, VietNam

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

*   Computing methodologies → Information extraction; Ontology engineering;
*   Information systems → Ontologies; Question answering; Clustering and classification.

## KEYWORDS

Open Intent Discovery, Knowledge Graph, Large language model, Education, Question-Answering System

### ACM Reference Format:

Tuan Bui, Oanh Tran, Phuong Nguyen, Bao Ho, Long Nguyen, Thang Bui, and Tho Quan. 2024. Cross-Data Knowledge Graph Construction for LLMenabled Educational Question-Answering System: A Case Study at HCMUT. In Proceedings of ACM Conference (Conference'17). ACM, New York, NY, USA, 8 pages. https://doi.org/10.1145/nnnnnnn.nnnnnnn

## 1 INTRODUCTION

A Large Language Model (LLM) is a language model trained on a considerably large size corpus. Nowadays, LLMs attract much attention from various communities due to their capacity to accomplish versatile language generation and comprehension. Notable LLM models reported to the public include OpenAI's GPT [23], Google's BART [15], LLaMa [26]. To achieve a broad spectrum of general knowledge [22] and refine their language ability [30], state-of-the-art LLMs nowadays are trained on a massive corpus of textual data. However, an LLM's completion might contain "hallucinations" [11] because of limited access to information that is as up-to-date, proprietary, or domain-specific as humans. To address this issue and other limitations, some hybrid models have shown prominent results by combining parametric memory with non-parametric memory [13]. Since their knowledge bases can be directly revised and expanded, and retrieved knowledge can be inspected and interpreted. This technique, which received a lot of traction after the publication of the famous Facebook research paper [16], is well-known and coined as Retrieval-Augmented Generation (RAG).

However, in most real-world domains such as education, the data/information often originate from various departments and faculties within an institution, resulting in diverse data sources with different natures such as structured text,