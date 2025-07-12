```markdown
---
cite_key: ai_2025
title: Zep: A Temporal Knowledge Graph Architecture for Agent Memory
authors: Preston Rasmussen Zep AI
year: 2025
doi: 10.48550/arXiv.2501.13956
url: https://arxiv.org/abs/2501.13956
relevancy: HIGH
relevancy_justification: Contains relevant concepts applicable to HDM systems
tags:
  - 10.48550/arXiv.2501.13956
date_processed: 2025-07-02
phase2_processed: true
standardization_date: 2025-07-10
standardization_version: 1.0
word_count: 393
sections_count: 7
---

# Zep: A Temporal Knowledge Graph Architecture for Agent Memory

## Authors
Preston Rasmussen, Zep AI (preston@getzep.com)
Pavlo Paliychuk, Zep AI (paul@getzep.com)
Travis Beauvais, Zep AI (travis@getzep.com)
Jack Ryan, Zep AI (jack@getzep.com)
Daniel Chalef, Zep AI (daniel@getzep.com)

## Abstract
We introduce Zep, a novel memory layer service for AI agents that outperforms the current stateof-the-art system, MemGPT, in the Deep Memory Retrieval (DMR) benchmark. Additionally, Zep excels in more comprehensive and challenging evaluations than DMR that better reflect real-world enterprise use cases. While existing retrieval-augmented generation (RAG) frameworks for large language model (LLM)-based agents are limited to static document retrieval, enterprise applications demand dynamic knowledge integration from diverse sources including ongoing conversations and business data. Zep addresses this fundamental limitation through its core component Graphiti—a temporally-aware knowledge graph engine that dynamically synthesizes both unstructured conversational data and structured business data while maintaining historical relationships. In the DMR benchmark, which the MemGPT team established as their primary evaluation metric, Zep demonstrates superior performance (94.8% vs 93.4%). Beyond DMR, Zep's capabilities are further validated through the more challenging LongMemEval benchmark, which better reflects enterprise use cases through complex temporal reasoning tasks. In this evaluation, Zep achieves substantial results with accuracy improvements of up to 18.5% while simultaneously reducing response latency by 90% compared to baseline implementations. These results are particularly pronounced in enterprisecritical tasks such as cross-session information synthesis and long-term context maintenance, demonstrating Zep's effectiveness for deployment in real-world applications.

## TL;DR
Temporal knowledge graph architecture that outperforms existing memory systems

## Key Insights
Core component "Graphiti" - temporally-aware knowledge graph engine that dynamically synthesizes unstructured conversational and structured business data while maintaining historical relationships.

## 1 Introduction

The impact of transformer-based large language models (LLMs) on industry and research communities has garnered significant attention in recent years [\[1\]](#page-9-0). A major application of LLMs has been the development of chat-based agents. However, these agents' capabilities are limited by the LLMs' context windows, effective context utilization, and knowledge gained during pre-training. Consequently, additional context is required to provide out-of-domain (OOD) knowledge and reduce hallucinations.

Retrieval-Augmented Generation (RAG) has emerged as a key area of interest in LLM-based applications. RAG leverages Information Retrieval (IR) techniques pioneered over the last fifty years[\[2\]](#page-9-1) to supply necessary domain knowledge to LLMs.

Current approaches using RAG have focused on broad domain knowledge and largely static corpora—that is, document contents added to a corpus seldom change. For agents to become pervasive in our daily lives, autonomously solving problems from trivial to highly complex, they will need access to a large corpus of continuously evolving data from users' interactions with the agent, along with related business and world data. We view empowering agents with this broad and dynamic "memory" as a crucial building block to actualize this vision, and we argue that current RAG approaches are unsuitable for this future. Since entire conversation histories, business datasets, and other domainspecific content cannot fit effectively inside LLM context windows, new approaches need to be developed for agent

memory. Adding memory to LLM-powered agents isn't a new idea—this concept has been explored previously in MemGPT [\[3\]](#page-10-0).

Recently, Knowledge Graphs (KGs) have been employed to enhance RAG architectures to address many of the shortcomings of traditional IR techniques[\[4\]](#page-10-1). In this paper, we introduce Zep[\[5\]](#page-10-2), a memory layer service powered by Graphiti[\[6\]](#page-10-3), a dynamic, temporally-aware knowledge graph engine. Zep ingests and synthesizes both unstructured message data and structured business data. The Graphiti KG engine dynamically updates the knowledge graph with new information in a non-lossy manner, maintaining a timeline of facts and relationships, including their periods of validity. This approach enables the knowledge graph to represent a complex, evolving world.

As Zep is a

## References

## Metadata Summary
### Research Context
- **Research Question**: How can temporal knowledge graphs improve AI agent memory for enterprise applications requiring dynamic knowledge integration?
- **Methodology**: Core component: "Graphiti" - temporally-aware knowledge graph engine; dynamically synthesizes unstructured conversational and structured business data; maintains historical relationships.
- **Key Findings**: Outperforms MemGPT in Deep Memory Retrieval benchmark (94.8% vs 93.4%); 18.5% accuracy improvement in LongMemEval benchmark; 90% reduction in response latency.
- **Primary Outcomes**: Enhanced cross-session information synthesis, improved long-term context maintenance, effective for enterprise AI applications.

### Analysis
- **Limitations**: Not explicitly stated in the abstract.
- **Research Gaps**: Limitations of static document retrieval in RAG frameworks; need for dynamic knowledge integration in enterprise AI.
- **Future Work**: Enhanced cross-session information synthesis, improved long-term context maintenance, effective for enterprise AI applications.
- **Conclusion**: Demonstrates significant advancement in temporal knowledge graph applications for AI agent memory and enterprise knowledge integration.

### Implementation Notes
Provides practical implementation of temporal knowledge graphs for AI agent memory with focus on dynamic data synthesis and historical relationship maintenance.
```