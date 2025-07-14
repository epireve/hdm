---
cite_key: maoa_2023
title: A Survey on Semantic Processing Techniques
authors: Rui Maoa, Kai Hec, Xulang Zhangb, Guanyi Chend, Jinjie Nib, Zonglin Yanga, Erik Cambriaa
year: 2023
doi: 10.5683/SP2/QPOJSI
date_processed: 2025-07-02
phase2_processed: true
original_folder: arxiv_2024_semantic_processing_techniques_survey
images_total: 5
images_kept: 5
images_removed: 0
tags: 
keywords: 
---

# A Survey on Semantic Processing Techniques

Rui Mao^a,^*^, Kai He^c,^*^, Xulang Zhang^b,^*^, Guanyi Chen^d,e,f,^*^, Jinjie Ni^b,^*^, Zonglin Yang^a,^*^, Erik Cambria^a,^**^

*^a^Continental-NTU Corporate Lab, Nanyang Technological University, 50 Nanyang Avenue, 639798, Singapore*

*^b^School of Computer Science and Engineering, Nanyang Technological University, 50 Nanyang Avenue, 639798, Singapore*

*^c^Saw Swee Hock School of Public Health, National University of Singapore, 117549, Singapore*

*^d^Hubei Provincial Key Laboratory of Artificial Intelligence and Smart Learning, Central China Normal University, 382 Xiongchu Avenue, 430079, Wuhan, China*

*^e^National Language Resources Monitoring and Research Center for Network Media, Central China Normal University, 382 Xiongchu Avenue, 430079, Wuhan, China*

*^f^School of Computer Science, Central China Normal University, 382 Xiongchu Avenue, 430079, Wuhan, China*

## Abstract

Semantic processing is a fundamental research domain in computational linguistics. In the era of powerful pre-trained language models and large language models, the advancement of research in this domain appears to be decelerating. However, the study of semantics is multi-dimensional in linguistics. The research depth and breadth of computational semantic processing can be largely improved with new technologies. In this survey, we analyzed five semantic processing tasks, e.g., word sense disambiguation, anaphora resolution, named entity recognition, concept extraction, and subjectivity detection. We study relevant theoretical research in these fields, advanced methods, and downstream applications. We connect the surveyed tasks with downstream applications because this may inspire future scholars to fuse these low-level semantic processing tasks with high-level natural language processing tasks. The review of theoretical research may also inspire new tasks and technologies in the semantic processing domain. Finally, we compare the different semantic processing techniques and summarize their technical trends, application trends, and future directions.

*Keywords:* Semantic Processing, Word Sense Disambiguation, Anaphora Resolution, Named Entity Recognition, Concept Extraction, Subjectivity Detection

## Introduction

Semantics is a linguistic term, generally referring to the meaning of language. Unlike syntax which studies the structure of sentences [[Zhang et al., 2023]](#ref-Zhang.2023), the significance of semantics lies in its ability to aid our comprehension of how meaning is conveyed through words, phrases, and sentences, as well as how language is used to express various ideas, thoughts, and emotions. Language is one of the important carriers of meanings. However, the term "meaning" encompasses multiple aspects of language. [[Palmer and Frank Robert, 1981]](#ref-Palmer.1981) argued that there is a lack of consensus regarding the nature of "meaning", e.g., which components should be considered part of semantics, and how it should be characterized. Thus, the study of "semantics" is also multi-dimensional in academia.

The evolution of semantic research reflects the rich connotation of semantics in linguistics. At the early stage, much attention is given to the study of lexical semantics. The first English dictionary, *Robert Cawdrey's Table Alphabeticall*, dates back to 1604 [[Noyes, 1943]](#ref-Noyes.1943). The construction of dictionaries, e.g., *The Oxford English Dictionary* [[Simpson and Weiner, 1989]](#ref-Simpson.1989) became one of the most significant symbols of lexical semantic research achievements. The research of lexical semantics covers word senses, polysemy, word formation, contrastive lexical semantics, and more. Next, another important research dimension of semantics emerged, termed structural semantics. Structural semantics emphasizes the analysis of sentence structures, including the relationships between words and the ways in which words contribute to the meaning of a sentence. The study of structural semantics includes but is not limited to analyzing the meaning of words by syntax, grammar, and pragmatics. Structural semantics elevates the study of semantics from the word level to the sentence level. The later cognitive semantics further enrich the connotation of semantics. The tenets of cognitive semantics posit that the faculty of language is intricately intertwined with the broader cognitive capacity of human beings [[Croft and Cruse, 2004]](#ref-Croft.2004). In other words, semantics is a reflection of how humans understand and make sense of the world around them. Under cognitive semantics, researchers extend to frame semantics (semantics is the reflection of encyclopedic knowledge), situation semantics (semantics reflects the relationships between situations) [[Barwise and Perry, 1981]](#ref-Barwise.1981), conceptual semantics (semantics reflects the structural perception of concepts) [[Jackendoff, 1976]](#ref-Jackendoff.1976), and more. Figure [[1]](#ref-Figure.1) summarizes partial semantic research domains in linguistics.

^**^This is to indicate the corresponding author.
^*^These authors contributed equally.
*Email addresses:* rui.mao@ntu.edu.sg (Rui Mao), kai_he@nus.edu.sg (Kai He), xulang001@e.ntu.edu.sg (Xulang Zhang), g.chen@ccnu.edu.cn (Guanyi Chen), jinjie001@e.ntu.edu.sg (Jinjie Ni), zonglin001@e.ntu.edu.sg (Zonglin Yang), cambria@ntu.edu.sg (Erik Cambria)

![Semantic research domains in linguistics. Lex. denotes lexical; sem. denotes semantics; und. denotes understanding.](_page_1_Figure_0.jpeg)
**Figure 1:** Semantic research domains in linguistics. Lex. denotes lexical; sem. denotes semantics; und. denotes understanding.

The development of automatic semantic processing techniques has largely facilitated semantic research. Many useful tools and knowledge bases^[[1]](#ref-1)^ were developed for word sense disambiguation, anaphora resolution, named entity recognition, concept extraction, and subjectivity detection. These tools are the embodiment of many theoretical ideas in semantics. For example, word sense disambiguation is an important task in lexical semantics. Anaphora resolution elucidates the relationship between the anaphor, which is the repetition of a reference, and its antecedent, which is the earlier mention of the entity. Anaphora resolution determines the structural semantics of the anaphor. Named entity recognition categorized named entities in texts by conceptually related classes, e.g., names, and locations. Similarly, concept extraction and subjectivity detection tasks also embody the cognitive properties of semantics.

In addition to improving semantic research, semantic processing techniques can also help other downstream natural language processing (NLP) tasks with more complexity (see Table [[1]](#ref-Table.1)). For example, subjectivity detection can be an upstream task of sentiment analysis, because subjective expressions can be further categorized by positive, negative, and neutral expressions with different opinionated intensities. The semantic processing techniques that have been reviewed possess a range of potential applications, including the ability to generate features that are effective, as well as to be used as a parser in order to obtain desired categories of text. Additionally, these techniques have the potential to improve the explainability of downstream applications.

The emergence of pre-trained language models (PLMs) has greatly enhanced the semantic representation capabilities of deep learning models and the ability to fit downstream tasks [[Devlin et al., 2019]](#ref-Devlin.2019); [[Liu et al., 2019b]](#ref-Liu.2019b); [[Lewis et al., 2020]](#ref-Lewis.2020). Some large language models (LLMs), e.g., GPT-4^[[2]](#ref-2)^ and Bard^[[3]](#ref-3)^ even realize the functions of multiple complex

^1^A knowledge base normally refers to a collection of organized information that is machine-readable, and supportive for an intelligent system.
^2^<https://openai.com/product/gpt-4>
^3^<https://bard.google.com/>

| Downstream tasks | WSD | AR | NER | CE | SD |
|:-----------------------------------|:--------|:-----|:--------|:--------|:-----|
| Sentiment Computing | F, P, E | F | | F, P, E | P |
| Information Retrieval | E | | | F, E | P |
| Machine Translation | F, P, E | F, E | | | |
| Summarization | | F | | | |
| Textual Entailment | | F | | | |
| Knowledge Graph Construction | | | P | | |
| Recommendation Systems | | | F, P, E | | |
| Dialogue Systems | | | P, E | F, P | |
| Commonsense Explanation Generation | | | | F, E | |
| Hate Speech Detection | | | | | F, P |
| Question & Answering Systems | | | | | F, P |

**Table 1:** The surveyed semantic processing tasks and their downstream applications. F denotes that the technique yielded features for a downstream task model; P denotes that the technique was used as a parser; E denotes that the technique improved the explainability for a downstream task. WSD denotes word sense disambiguation. AR denotes anaphora resolution. NER denotes named entity recognition. CE denotes concept extraction. SD denotes subjectivity detection.

NLP tasks by the means of dialogue, such as question answering, translation, and text summarization. Many semantic processing studies have gradually faded out of the field of NLP. Then, in the era of PLMs and LLMs, an intuitive question is what is the motivation for studying semantic processing techniques?

As mentioned before, semantics reflects the multiple aspects of language. Besides understanding word senses, semantics is also the entrance to understanding the mechanism, and perception of language. Language intelligence encompasses more than just achieving a level of accuracy that is equivalent to or surpasses human accuracy for specific tasks. It also entails the capacity to unveil the nature of language and investigate the cognitive processes that underlie language. Much aforementioned semantic research in the context of linguistics has not been explored in computational linguistics to our best knowledge. Thus, we are motivated to propose a survey on semantic processing techniques to encourage future scholars that can expand the depth and breadth of semantic research, leading the public attention from the application value of NLP techniques to the research value of computational linguistics. Nevertheless, we also highlight the fusion of low-level semantic processing techniques and high-level NLP techniques to demonstrate the application value of semantic processing techniques in different domains.

Given the broadness of semantics, our survey scope lies in semantic processing techniques for word sense disambiguation, anaphora resolution, concept extraction, named entity recognition, and subjectivity detection. This is because these low-level semantic processing tasks reflect different aspects of semantics. In addition, there were many research works on these tasks in the field of computational linguistics. We focus on low-level semantic processing tasks, rather than high-level semantic processing tasks, e.g., sentiment analysis and natural language inference, because they provide fundamental building blocks for both high-level semantic processing tasks and higher-level NLP tasks.

Multiple semantic processing techniques were rarely surveyed in the same article. [[Salloum et al., 2020]](#ref-Salloum.2020) surveyed several high-level semantic processing tasks, e.g., latent semantic analysis, explicit semantic analysis, and sentiment analysis. Compare to the work of [[Salloum et al., 2020]](#ref-Salloum.2020), our survey includes the latest research in low-level semantic processing techniques. Compare to the latest semantic processing surveys focusing on specific tasks [[Ransing and Gulati, 2022]](#ref-Ransing.2022); [[Poesio et al., 2023]](#ref-Poesio.2023); [[Fu et al., 2020]](#ref-Fu.2020); [[Wang et al., 2022]](#ref-Wang.2022); [[Montoyo et al., 2012]](#ref-Montoyo.2012), we additionally reviewed important theoretical research and downstream task applications in these domains. These contents can help readers better understand the foundation of semantic research in linguistics, as well as potential application scenarios. More importantly, theoretical research shows the big picture of a semantic processing task, which may inspire different research tasks in the computational linguistic community. The collection of multiple semantic processing techniques is helpful for readers to have a comprehensive understanding of a large field, inspiring more fusion research across different domains. Theoretical research of other tasks has the potential to inspire fresh perspectives among researchers who have been concentrating on a specific semantic research task.

The contribution of this survey is threefold:

- We survey recent semantic processing techniques, annotation tools, datasets, and knowledge bases for five low-level semantic processing tasks.
- We highlight important theoretical research, and downstream applications to encourage deeper and wider re-

![The summary of technical trends and downstream applications of surveyed semantic processing tasks. KGC denotes knowledge graph construction. CEG denotes commonsense explanation generation. RE denotes relation extraction.](_page_3_Figure_0.jpeg)
**Figure 2:** The summary of technical trends and downstream applications of surveyed semantic processing tasks. KGC denotes knowledge graph construction. CEG denotes commonsense explanation generation. RE denotes relation extraction.

search in the semantic processing domain upon the currently established task setups.

- We compare different semantic processing techniques, delineate their technical and application trends, and put forth potential avenues for future research in this domain.

In the following sections, we introduce different semantic processing techniques, e.g., word sense disambiguation (Section [[2]](#ref-Section.2)), anaphora resolution (Section [[3]](#ref-Section.3)), named entity recognition (Section [[4]](#ref-Section.4)), concept extraction (Section [[5]](#ref-Section.5)), and subjectivity detection (Section [[6]](#ref-Section.6)). We discuss the interactions between the surveyed tasks and the impacts of deep learning and LLMs on semantic processing in Section [[7]](#ref-Section.7). Finally, we conclude this survey in Section [[8]](#ref-Section.8). Each task is structured by theoretical research, annotation schemes, datasets, knowledge bases, evaluation metrics, methods, downstream applications, and a summary. Figure [[2]](#ref-Figure.2) demonstrates the taxonomy of methods and downstream applications of each task in this survey.

## 2. Word Sense Disambiguation

The complexity of human language is difficult for machines to understand it. One of the challenges is the ambiguity of word senses. In natural language, a word may have multiple senses, given different contexts. Consider the following example:

![Simplified examples of the knowledge-based and supervised WSD.](_page_4_Figure_0.jpeg)
**Figure 3:** Simplified examples of the knowledge-based and supervised WSD.

## (1) He got his shoes wet as he walked along the bank.

According to the Oxford English Dictionary, the major senses of "bank" include (a)*an organization that provides various financial services, for example keeping or lending money*; (b) *the side of a river, canal, etc. and the land near it*. With the context, humans can easily know that "bank" here refers to the sense (b). However, it is challenging for machines to do so because the interpretation made by humans is contingent upon their comprehension of the fact that the probability of getting one's shoes wet is higher when walking alongside a river bank as compared to a financial institution. Machines rarely take the commonsense into account when inferring the meaning of "bank"^[[4]](#ref-4)^, because they don't have human-like cognition and reasoning abilities by nature.

There are two main technical trends in addressing the task of WSD, namely knowledge-based methods and supervised methods. Knowledge-based WSD utilizes the word relations from knowledge graphs, e.g., WordNet and BabelNet [[Navigli and Ponzetto, 2012]](#ref-Navigli.2012) to achieve the disambiguation of word senses. In supervised methods, the WSD task is usually defined as a classification task by word senses. A WSD model is trained with annotated data. Two examples of knowledge-based and supervised WSD are illustrated in Figure [[3]](#ref-Figure.3). As shown in the figure, a naive strategy of the knowledge-based WSD is that the sense that shares the most relations with the context words is selected as the best-matched one. For supervised WSD systems, the predictive model predicts the potential senses, given the target word and its context words as input. In recent times, the use of knowledge bases has proven advantageous for several modern supervised systems. As a result, there has been a growing trend in integrating knowledge-based and supervised methods to enhance their performance [[Wang and Wang, 2020]](#ref-Wang.2020).

WSD has been recognized as a crucial module in numerous NLP tasks that heavily rely on word senses, such as sentiment computing, information retrieval, and machine translation. The application of WSD techniques has been demonstrated to be beneficial for these NLP tasks. While prior surveys [[Bevilacqua et al., 2021a]](#ref-Bevilacqua.2021a); [[Navigli, 2009]](#ref-Navigli.2009) have conducted extensive reviews for WSD, the works discussed in them are outdated. Besides, those works do not link WSD with the linguistic theories and diverse downstream tasks.

### 2.1. Theoretical Research

### 2.1.1. Distributional Semantics
The hypothesis from distributional semantics [[Firth, 1957]](#ref-Firth.1957) argued that word meanings can be inferred from word co-occurrences. Words that appear in similar contexts tend to have similar meanings. Such a hypothesis has been the most significant foundation of developing semantic representations in the computational linguistics community, e.g., vector space representations [[Turney and Pantel, 2010]](#ref-Turney.2010); [[Mikolov et al., 2013]](#ref-Mikolov.2013); [[Pennington et al., 2014]](#ref-Pennington.2014) and PLMs [[Devlin et al., 2019]](#ref-Devlin.2019); [[Liu et al., 2019b]](#ref-Liu.2019b). Based on such a hypothesis, dense semantic vectorial representation research commonly follows a similar training paradigm, e.g., using context words to predict a target word. Currently, Chat-GPT further proves that learning to use words that have appeared before to predict the next possible word can achieve the skills of analogy and reasoning with the help of a very large Transformer [[Vaswani et al., 2017]](#ref-Vaswani.2017)-based model.

^4^Current methods likely disambiguate word senses by word co-occurrences. However, word co-occurrences are not commonsense.

### 2.1.2. Selectional Preference
[[Wilks, 1973]](#ref-Wilks.1973) proposed a concept of selectional preference. It is a procedure for representing the meaning structure of natural language. Compared to the "derivational paradigm" of transformational grammar and generative semantics, [[Wilks, 1973]](#ref-Wilks.1973) believed that selectional preference is a more efficient procedure in natural language understanding. It focuses on determining preferences between various possible interpretations of a text, rather than identifying a solitary and unequivocally correct interpretation. Selection preference theory allows more flexibility and nuance in understanding word senses and language. Besides, the theory is computation-friendly. [[Wilks, 1973]](#ref-Wilks.1973) showed how the procedure could be computed and implemented. The work of [[Wilks, 1973]](#ref-Wilks.1973) supports that there are multiple possible meanings for a word. The meaning can be defined by the sectional preference of contexts.

### 2.1.3. Construction Semantics

[[Goldberg and Suttle, 2010]](#ref-Goldberg.2010) argued that the meanings of words are frequently derived from larger language units, termed constructions. Constructions consist of a form and a meaning, ranging from single words to full sentences in size. The interpretation of a construction is reliant on both its structure and the situations in which it is employed. [[Goldberg and Suttle, 2010]](#ref-Goldberg.2010) argued that semantic restrictions are better linked with the construction as an entirety rather than with the lexical semantic framework of the verbs. The work of [[Goldberg and Suttle, 2010]](#ref-Goldberg.2010) highlights that the interpretation of meanings of language units can be extended from individual words to constructions. It shows the necessity of defining language units in WSD.

### 2.1.4. Frame Semantics
[[Fillmore et al., 2006]](#ref-Fillmore.2006) proposed frame semantics that provides a distinct viewpoint on the meanings of words and the principles behind language construction. Frame semantics emphasizes the significance of the surrounding context and encyclopedic knowledge in comprehending word meanings. [[Petruck, 1996]](#ref-Petruck.1996) explained that a "frame" refers to a collection of concepts interconnected in a manner that understanding any one concept depends on the understanding of the complete system. In frame semantics, the meaning of "cooking" is beyond its dictionary meaning. It also associates with the concept of "food", "cook", "container", and "heating instrument". Frame semantics motivates later ontology research, e.g., FrameNet [[Ruppenhofer et al., 2016]](#ref-Ruppenhofer.2016) and FrameNet-based WSD systems, significantly.

### 2.2. Annotation Schemes
For knowledge-based WSD, the data are normally presented as ontology, such as WordNet, FrameNet, and Babel-Net, where words and concepts are connected by relations. The relations include hyponyms, hypernyms, holonyms, meronyms, attributes, entailment, etc. An explanation (gloss) and a few example sentences are given for each synset. Synsets of the same Part Of Speech (POS) are connected under some relations independently. However, there exist relations when the basic concept of two words is the same but in a different POS (for example, "propose" and "proposal" were characterized as "derivationally related synsets" in WordNet).

For supervised WSD, a particular word in a given sentence is annotated with a sense ID that corresponds to one of the potential senses in a knowledge base, such as WordNet. A sample of annotation is shown in the next section.

### 2.3. Datasets
Our surveyed datasets and their statistics can be viewed in Table [[2]](#ref-Table.2). The biggest manually annotated English corpus currently accessible is SemCor^[[5]](#ref-5)^ [[Miller et al., 1993]](#ref-Miller.1993). It has 200K content terms tagged with their related definitions and around 40K phrases. Although SemCor serves as the principal training corpus for WSD, its limited coverage of the English vocabulary for both words and meanings is its most significant drawback. In essence, SemCor merely includes annotations for 22K distinct lexemes in WordNet, the most extensive and commonly employed computerized English dictionary, which corresponds to less than 15% of all words.

To augment the coverage of words, some studies [[Vial et al., 2019]](#ref-Vial.2019) incorporated the English Princeton WordNet Gloss Corpus (WNG)^[[6]](#ref-6)^, which contains more than 59K WordNet senses, as a complemented data. The WNG is annotated manually or semi-automatically.

^5^<http://web.eecs.umich.edu/~mihalcea/downloads.html>
^6^<https://wordnetcode.princeton.edu/glosstag.shtml>

| Dataset | Source | # Samples | Reference |
|:----------------|:------------------------------------|:----------|:----------------------------|
| SemCor | WordNet | 200,000 | [[Miller et al., 1993]](#ref-Miller.1993) |
| MultiSemCor | WordNet,<br>bilingual Collins | 51,847 | [[Pianta et al., 2002]](#ref-Pianta.2002) |
| Line-hard-serve | WSJ, APHB | 4,000 | [[Leacock et al., 1993]](#ref-Leacock.1993) |
| Interest | HECTOR | 2,369 | [[Bruce and Wiebe, 1999]](#ref-Bruce.1999) |
| DSO | Brown, WSJ | 192,800 | [[Ng and Lee, 1996]](#ref-Ng.1996) |
| OMWE | Web | 29,165 | [[Chklovski and Pantel, 2004]](#ref-Chklovski.2004) |
| OMSTI | UN documents | 1,357,922 | [[Taghipour and Ng, 2015]](#ref-Taghipour.2015) |
| SensEval-2 | Unknown | 2,282 | [[Edmonds and Cotton, 2001]](#ref-Edmonds.2001) |
| SensEval-3 | Editorial, news<br>story, & fiction | 1,850 | [[Snyder and Palmer, 2004]](#ref-Snyder.2004) |
| SemEval2007 | Brown, WSJ | 455 | [[Pradhan et al., 2007]](#ref-Pradhan.2007) |
| SemEval2013 | SMT workshop | 1,644 | [[Navigli et al., 2013]](#ref-Navigli.2013) |
| SemEval2015 | EMEA, KDEdoc,<br>EUB | 1,022 | [[Moro and Navigli, 2015]](#ref-Moro.2015) |

**Table 2:** WSD datasets and statistics. SMT, EMEA, KDEdoc, and EUB denote statistical machine translation, European Medicines Agency documents, KDE manual corpus, and the EU bookshop corpus, respectively.

SemCor and its variations [[Bentivogli and Pianta, 2005]](#ref-Bentivogli.2005); [[Bond et al., 2012]](#ref-Bond.2012) lack an acceptable multi-lingual equivalent in the majority of global languages, which limits the scaling capabilities of WSD models beyond English. To address the aforementioned issues, numerous automatic methods for creating multi-lingual sense-annotated data have been developed [[Pasini and Navigli, 2017]](#ref-Pasini.2017); [[Pasini et al., 2018]](#ref-Pasini.2018); [[Scarlini et al., 2019]](#ref-Scarlini.2019); [[Pasini and Navigli, 2020]](#ref-Pasini.2020). In an English-Italian parallel corpus known as MultiSemCor [[Pianta et al., 2002]](#ref-Pianta.2002), senses from the English and Italian versions of WordNet are annotated.

The Line-hard-serve corpus [[Leacock et al., 1993]](#ref-Leacock.1993) contains 4K samples of the nominal, adjective, and verbal words with sense tags. The data were sourced from Wall Street Journal (WSJ) corpus and the American Printing House for the Blind (APHB) corpus. The Interest corpus [[Bruce and Wiebe, 1999]](#ref-Bruce.1999) contains 2,369 occurrences of the term *interest* that have been sense-labeled. The data were sourced from the HECTOR word sense corpus [[Atkins, 1992]](#ref-Atkins.1992). The Defence Science Organisation (DSO), based in Singapore, created the DSO corpus^[[7]](#ref-7)^ [[Ng and Lee, 1996]](#ref-Ng.1996), which contains 192,800 sense-tagged tokens from 191 words from the Brown and WSJ corpora. The Open Mind Word Expert (OMWE) dataset^[[8]](#ref-8)^ [[Chklovski and Pantel, 2004]](#ref-Chklovski.2004) is a corpus of sentences with 288 noun occurrences that were jointly annotated by Web users. One Million Sense-Tagged for Word Sense Disambiguation and Induction (OMSTI)^[[9]](#ref-9)^ [[Taghipour and Ng, 2015]](#ref-Taghipour.2015) is a semi-automatically annotated WSD dataset with WordNet sense inventory. The data were sourced from MultiUN corpus, which is a collection of United Nation documents. The OMSTI includes 687,871 nouns, 412,482 verbs, and 251,362 adjectives and 6,207 adverbs after including selected samples from SemCor and DSO.

The SensEval and SemEval datasets are created from the SensEval/SemEval evaluation campaigns. Now, these datasets have been the most widely used benchmarking datasets in WSD. [[Raganato et al., 2017b]](#ref-Raganato.2017b) collected these datasets together^[[10]](#ref-10)^ and developed a unified evaluation framework for empirical comparison. The statistics of the following datasets are from the collection of [[Raganato et al., 2017b]](#ref-Raganato.2017b). SensEval-2 [[Edmonds and Cotton, 2001]](#ref-Edmonds.2001) used WordNet 1.7 sense inventory, including 2,282 sense annotations for nouns, verbs, adverbs and adjectives. SensEval-3 [[Snyder and Palmer, 2004]](#ref-Snyder.2004) employed WordNet 1.7.1 sense inventory, including 1,850 sense annotations. SemEval-2007 Task 17 [[Pradhan et al., 2007]](#ref-Pradhan.2007) employed WordNet 2.1 sense inventory, including 455 nominal and verbal sense annotations. SemEval-2013 Task 12 [[Navigli et al., 2013]](#ref-Navigli.2013) used WordNet 3.0 sense inventory, including 1,644 nominal sense annotations. SemEval-2015 Task 13 [[Moro and Navigli, 2015]](#ref-Moro.2015) utilized WordNet 3.0 sense inventory, including 1,022 sense annotations. It is worth noting that some of the SemEval tasks are multi-lingual, including SemEval 2013 and 2015, which facilitates multi-lingual WSD.

All of these corpora are annotated using various WordNet sense inventories, with the exception of the Interest corpus (tagged with LDOCE senses) and the Senseval-1 corpus. The Interest corpus and the Senseval-1 corpus were

^7^<https://borealisdata.ca/dataset.xhtml?persistentId=doi:10.5683/SP2/QPOJSI>
^8^<http://web.eecs.umich.edu/~mihalcea/downloads/OMWE/OMWE1.0.English.tar.gz>
^9^<https://www.comp.nus.edu.sg/~nlp/corpora.html>
^10^<http://lcl.uniroma1.it/wsdeval/home>

sense-labeled using the HECTOR sense inventories, a lexicon and corpus from a joint Oxford University Press/Digital project [[Atkins, 1992]](#ref-Atkins.1992)

Generally, the data and labels in WSD datasets are organized in the following forms. Then, the task is to identify the sense classes, given contexts, and target words.

```text
context: "You perform well in the exam, I will reward you.",
target word: "perform",
pos: "VB",
sense: "3"
context: "She worked in a renowned university for a long time.",
"target word": "university",
"pos": "NN",
"sense": "2"
```

### 2.4. Knowledge Bases
| Name | Knowledge | # Entities | Structure |
|:----------------|:------------------------|:-----------|:-------------|
| LDOCE 6th ed. | Lexical | 230,000 | Unstructured |
| ODE 2022 | Lexical | 600,000 | Unstructured |
| CED 12th ed. | Lexical | 722,000 | Unstructured |
| OALD 8th ed. | Lexical | 145,000 | Unstructured |
| WordNet | Lexical | 95,600 | Graph |
| FrameNet | Lexical | 13,687 | Graph |
| BabelNet | Lexical & Multi-lingual | 26,044,643 | Graph |
| SyntagNet | Lexical | 78,000 | Graph |

**Table 3:** Useful knowledge bases for WSD. LDOCE means Longman Dictionary of Contemporary English. ODE means Oxford Dictionary of English. CED means Collins English Dictionary. OALD means Oxford Advanced Learner's Dictionary of Current English. Unstructured or structured means the knowledge base contains unstructured or structured lexical knowledge by concepts.

Machine-Readable Dictionaries (MRDs) have been a useful source for WSD due to their structured knowledge and easy access [[Navigli, 2009]](#ref-Navigli.2009). Dictionaries frequently contain extensive information about the various meanings of a word, as well as illustrative examples of their usage within context. Therefore, dictionaries can serve as valuable knowledge bases for the task of WSD. Additionally, MRDs may provide further information such as synonyms, antonyms, and related words, which can aid in facilitating a more comprehensive comprehension of a word's meaning. Through the analysis of this information, a system may make more precise determinations about which meaning is most fitting in a given context. There are many electronic dictionaries available for machines to refer to, such as the Longman Dictionary of Contemporary English (LDOCE) [[Mayor, 2009]](#ref-Mayor.2009), the Oxford Dictionary of English (ODE) [[Dictionary, 2010]](#ref-Dictionary.2010), Collins English Dictionary (CED) [[Dictionary, 1982]](#ref-Dictionary.1982), and the Oxford Advanced Learner's Dictionary of Current English (OALD) [[Hornby and Cowie, 1974]](#ref-Hornby.1974).

WordNet [[Miller et al., 1990]](#ref-Miller.1990) is a sizable, manually curated lexicographic database of English. It is arranged as a network with synsets, or collections of contextual synonyms, as nodes. A synset of synonyms each represents one of a word's senses. Through edges that express lexical-semantic links like meronymies (partof) and hypernymies (is-a), synsets and senses are connected to one another. WordNet additionally offers definitions (glosses) and uses examples for each synset as additional lexical information. The most current English WSD works use the 3.0 version, which was published in 2006 and has 117,659 synsets. Following the initial WordNet for English, many WordNets for other languages have been proposed, including languages such as Chinese [[Wang and Bond, 2013]](#ref-Wang.2013), Arabic [[Black et al., 2006]](#ref-Black.2006), Dutch [[Postma et al., 2016]](#ref-Postma.2016), etc^[[11]](#ref-11)^.

FrameNet [[Ruppenhofer et al., 2016]](#ref-Ruppenhofer.2016) is an English lexical repository that is readable by both humans and machines, established by annotating real-life textual examples that depict the usage of words. It was developed based on the

^11^See <http://globalwordnet.org/resources/wordnets-in-the-world/> for a summary.

theory of frame semantics, containing 1,224 frames (a frame refers to a diagrammatic representation of a scenario encompassing diverse elements such as participants, props, and other conceptual roles), and 13,687 lexical units (lemmas and their PoS) that evoke frames. In FrameNet, the lexical units of a sentence are associated with frame elements. Frame elements are the semantic role of lexical units. For example, given a sentence "I ate an apple this afternoon", "apple" would fill the role of "food" (a frame element).

BabelNet [[Navigli and Ponzetto, 2012]](#ref-Navigli.2012) is a multi-lingual dictionary that covers both lexicographic and encyclopedic entries from 520 languages. These entries were created by semi-automatically mapping numerous sites, including WordNet, Multi-lingual WordNet, and Wikipedia. The topology of BabelNet is that of a semantic network, where the nodes are multi-lingual synsets (collections of synonyms that have been lexicalized in several languages), and the edges represent the semantic connections between them.

SyntagNet [[Maru et al., 2019]](#ref-Maru.2019) is a manually developed lexical resource that integrates semantically disambiguated lexical combinations, e.g., noun-verb and noun-noun pairs. The development of SyntagNet involved initially extracting lexical combinations from English Wikipedia and the British National Corpus, which were then subjected to a process of manual disambiguation, based on the WordNet. SyntagNet covers five major languages, e.g., English, German, French, Spanish, and Italian.

### 2.5. Evaluation Metrics
In the WSD task, given a sentence of *n* words *T* = {*x*~1~, ..., *x*~n~}, the model predicts a sense for each word given the dictionary. Normally, the F1 score is adopted, which is a specialization of the F score when α = 1:

$$
F = \frac{1}{\alpha \frac{1}{P} + (1 - \alpha) \frac{1}{R}}
$$
(1)

Where *P* denotes precision and *R* denotes recall:

$$
P = \frac{\text{correct predictions}}{\text{total predictions}}\tag{2}
$$

$$
R = \frac{\text{correct predictions}}{n} \tag{3}
$$

The aforementioned metrics do not accurately represent how well systems can produce a level of confidence for a particular sensory choice. [[Resnik and Yarowsky, 1999]](#ref-Resnik.1999) developed an evaluation criterion that considers the discrepancies between the accurate and selected senses to weigh misclassification mistakes. Therefore, this error will be penalized less severely than coarser sense distinctions if the chosen sense is a fine-grained distinction of the true sense. There have been evaluation metrics for even more precise measurements, including the Receiver Operation Characteristic (ROC) [[Cohn, 2003]](#ref-Cohn.2003). However, compared with traditional metrics such as precision, recall, and F1, these metrics are not frequently utilized.

### 2.6. Annotation Tools
LX-SenseAnnotator^[[12]](#ref-12)^ [[Neale et al., 2015]](#ref-Neale.2015) provides a user interface for manually annotating word senses. The software has the capability to process lexical data in any language, on the condition that the data is compliant with the format of Princeton WordNet. Human annotators can view the pre-processed text in three different modes, including the source text, sense-annotated text, and raw text, which can be switched between by using a tab widget. The source text mode displays the original text along with all tags, while the sense-annotated text mode displays the same text but with newly added sense tags. This allows the annotator to monitor the output file continually. Annotators can view the sense options in real time when annotating the sense for a word.

LexTag^[[13]](#ref-13)^ is another useful tool for WSD. The annotation interface provided is characterized by its user-friendly nature, facilitating users in the annotation of various textual elements such as terms, sentences, and documents. This

^12^<http://nlx.di.fc.ul.pt/tools.html>
^13^https://babelscape.com/lextag

annotation process involves attributing meanings drawn from pre-existing knowledge graphs and dictionaries, encompassing reputable sources like WordNet, Wiktionary, and WordAtlas. LexTag has been used to create a recent 10-language parallel dataset ELEXIS-WSD 1.0^[[14]](#ref-14)^.

### 2.7. Methods
### 2.7.1. Knowledge-Based WSD

Knowledge-based WSD utilizes knowledge bases to disambiguate word senses. Compared with supervised WSD, this class of WSD methods achieves lower performance but better data efficiency. In knowledge-based WSD, there are essentially two research streams.

### A. Semantic Space Matching

One stream of the knowledge-based WSD is to look for overlaps or similarities between the context of a term whose sense needs to be disambiguated and its sense representation, such as the definition of a potential sense and its associated sense that was retrieved from a knowledge base. The predicted sense is considered to be the sense that is the closest.

Lesk [[Lesk, 1986]](#ref-Lesk.1986) is a naive knowledge-based WSD algorithm that looks for terms that are similar to the target word in the context of each sense. The approach aimed to enumerate the intersections among lexicon definitions of the diverse connotations of every target word contained within a given sentence. [[Banerjee et al., 2003]](#ref-Banerjee.2003) proposed an advanced version of the Lesk, which also includes the definition of related senses, where the standard term frequencyinverse document frequency method is employed for word weighting. Another improved version of Lesk [[Basile et al., 2014]](#ref-Basile.2014) includes word embedding for better analysis, which improves the accuracy of determining how close the definition and context of the target word are. SREF*KB* [[Wang and Wang, 2020]](#ref-Wang.2020) is a state-of-the-art (SOTA) WSD system. It is a vector-based technique that disambiguates word senses by using sense embeddings and contextualized word representations. It applied BERT to represent WordNet instances and definitions, as well as the automatically obtained contexts from the Web.

### B. Graph-based Matching

The other stream of the knowledge-based WSD creates a graph using the given context and connections that have been retrieved from knowledge bases. Here, the synsets and the relationships between them are seen as the nodes and edges, respectively. The senses are then disambiguated based on the constructed graphs. A variety of graph-based techniques, such as Latent Dirichlet Allocation (LDA) [[Blei et al., 2003]](#ref-Blei.2003), PageRank [[Brin and Page, 1998]](#ref-Brin.1998), Random Walks [[Agirre et al., 2014]](#ref-Agirre.2014), Clique Approximation [[Moro et al., 2014b]](#ref-Moro.2014b), Game Theory [[Tripodi and Navigli, 2019]](#ref-Tripodi.2019), etc., are used to disambiguate the meaning of a given word using the created graph.

[[Agirre and Soroa, 2009]](#ref-Agirre.2009) presented a graph-based unsupervised WSD system that employs random walk over a WordNet semantic network. They employed a customized version of the Page Rank algorithm [[Haveliwala, 2002]](#ref-Haveliwala.2002). The technique leverages the inherent structural properties of the graph that underlies a specific lexical knowledge base, and shows the capability of the algorithm to identify global optima for WSD, based on the relations among entities. [[Agirre et al., 2014]](#ref-Agirre.2014) evaluated this algorithm with new datasets and variations of the algorithm to prove its effectiveness. [[Navigli and Lapata, 2007]](#ref-Navigli.2007) also introduced a graph-based unsupervised model for WSD, which analyzed the connectivity of graph structures to identify the most pertinent word senses. A graph is constructed to represent all possible interpretations of the word sequence, where nodes represent word senses and edges represent sense dependencies. The model assessed the graph structure to determine the significance of each node, thus finding the most crucial node for each word. Babelfy [[Moro et al., 2014b]](#ref-Moro.2014b) is also a graph-based WSD method that uses random walk to identify relationships between synsets. It used BabelNet [[Navigli and Ponzetto, 2012]](#ref-Navigli.2012) and performed random walks with Restart [[Tong et al., 2006]](#ref-Tong.2006). In addition, it incorporated the entire document at the time of disambiguation. The candidate disambiguation is upon automatically developed semantic interpretation graph which used a graph structure to represent various possible interpretations of input text. SyntagRank [[Scozzafava et al., 2020]](#ref-Scozzafava.2020) is a highscoring knowledge-based WSD algorithm. It is an entirely graph-based algorithm that uses the Personalized PageRank algorithm to incorporate WordNet (for English), BabelNet (for non-English) and SyntagNet. SyntagRank is generally considered a stronger method than SREF*KB*. BabelNet enabled SyntagRank to improve its ability to scale across a wide range of languages, whereas SREF*KB* has only been evaluated in English.

^14^https://www.clarin.si/repository/xmlui/handle/11356/1674

### 2.7.2. Supervised WSD
Currently, supervised approaches, especially deep learning-based supervised learning approaches, have become mainstream in the WSD community. Earlier deep learning-based approaches focused on architectures where WSD was defined as token classification over WordNet senses [[Kågeback and Salomonsson, 2016]](#ref-Kageback.2016). Even though they performed well, these structures showed a lot of flaws, particularly when it came to predicting uncommon and invisible senses. To address these issues, numerous works began to supplement the training data by utilizing various lexical knowledge, such as sense definitions [[Kumar et al., 2019]](#ref-Kumar.2019); [[Blevins and Zettlemoyer, 2020]](#ref-Blevins.2020), semantic relations [[Bevilacqua and Navigli, 2020]](#ref-Bevilacqua.2020); [[Conia and Navigli, 2021]](#ref-Conia.2021), and data generated via novel generative methods [[Barba et al., 2021b]](#ref-Barba.2021b). In this section, we review the representative works in supervised WSD.

### A. Data-Driven Machine Learning Approaches

Data-driven machine learning approaches refer to methodologies and techniques in which the design, training, and optimization of traditional machine learning algorithms, heavily rely on large amounts of data. In these approaches, the model's ability to generalize patterns and make predictions is learned directly from the provided data, rather than being explicitly programmed by humans. In the early days, classic machine learning approaches with handcrafted features were frequently used for WSD.

[[Singh et al., 2014]](#ref-Singh.2014) employed 5-gram and position features, and a decision tree algorithm to represent classification rules in a tree structure where the training dataset is recursively partitioned. Each leaf node indicates the meaning of a word. They developed a dataset, containing 672 Manipuri sentences to test their method. The sentences were sourced from a local newspaper, termed "The Sangai Express". [[O'Hara et al., 2004]](#ref-OHara.2004) proposed a class-based collocation method that integrates diverse linguistic features in a decision tree algorithm. For the collocation, three distinct word relatedness scores are used: the first is based on WordNet hypernym relations; the second is based on cluster-based word similarity classes; and the third is based on dictionary definition analysis. The authors also utilized PoS and word form features. The It Makes Sense (IMS) WSD system [[Zhong and Ng, 2010]](#ref-Zhong.2010) used a Support Vector Machine (SVM) classifier. Different positional and linguistic features were considered, including nearby words, nearby words' PoS tags, and nearby collocations. Later, word embeddings became important features in WSD. [[Taghipour and Ng, 2015]](#ref-Taghipour.2015); [[Rothe and Schutze, 2015]](#ref-Rothe.2015); [[Iacobacci et al., 2016]](#ref-Iacobacci.2016) used IMS as the base model to examine word embeddings. [[Iacobacci et al., 2016]](#ref-Iacobacci.2016) offered many approaches where different word embeddings were applied as features to test how many parameters impact the effectiveness of a WSD system. The authors found that word2vec [[Mikolov et al., 2013]](#ref-Mikolov.2013) which was trained with OMSTI can yield the strongest results on the three examined all-word WSD tasks.

### B. Data-Driven Neural Approaches

More recently, neural approaches started to be used. Data-driven neural approaches refer to methodologies and techniques that utilize neural networks and supervised learning to learn patterns and representations directly from data.

[[Popov, 2017]](#ref-Popov.2017) proposed to use BiLSTM [[Graves and Schmidhuber, 2005]](#ref-Graves.2005), GloVe word embeddings, and word2vec lemma embeddings. [[Yuan et al., 2016]](#ref-Yuan.2016) suggested another LSTM-based word sense disambiguation approach that was trained in a semi-supervised fashion. The semi-supervised learning was achieved by employing label propagation [[Talukdar and Crammer, 2009]](#ref-Talukdar.2009) to assign labels to unannotated sentences by assessing their similarity to labeled ones. The best performance on the SensEval-2 dataset can be observed from the model that was semi-supervisiontrained with OMSTI and 1,000 additional unlabeled sentences. Additionally, [[Le et al., 2018]](#ref-Le.2018) looked more closely at how many elements affect its performance, and several intriguing conclusions were drawn. The initial point to highlight is that achieving strong WSD performance does not necessitate an exceedingly large unannotated dataset. Furthermore, this method provides a more evenly-distributed sense assignment in comparison to prior approaches, as evidenced by its relatively strong performance on infrequent cases. Additionally, it is worth noting that the limited sense coverage of the annotated dataset may serve as an upper limit on overall performance.

With the development of self-attention-based neural architectures and their capacity to extract sophisticated language information [[Vaswani et al., 2017]](#ref-Vaswani.2017), the use of transformer-based architectures in fully supervised WSD systems is becoming more and more popular. The WSD task is usually fine-tuned on a pre-trained transformer model, which is a popular strategy. The task-specific inputs are given to the pre-trained model, which is then further trained across a number of epochs with the task-specific objective. Likewise, in recent token classification models for WSD, the contextualized representations are usually generated by a pre-trained model and then fed to either a feedforward network [[Hadiwinoto et al., 2019]](#ref-Hadiwinoto.2019) or a stack of Transformer layers [[Bevilacqua and Navigli, 2019]](#ref-Bevilacqua.2019). These methods outperform earlier randomly initialized models [[Raganato et al., 2017a]](#ref-Raganato.2017a). [[Hadiwinoto et al., 2019]](#ref-Hadiwinoto.2019) tested different pooling strategies of BERT, e.g., last layer projection, weighted sum of hidden layers, and Gated Linear Unit [[Dauphin et al., 2017]](#ref-Dauphin.2017). The best performance on SensEval-2 is given by the strategy of the weighted sum of hidden layers, accounting for 76.4% F1. [[Bevilacqua and Navigli, 2019]](#ref-Bevilacqua.2019) proposed a bi-directional Transformer that explicitly attends to past and future information. This model achieved 75.7% F1 on SensEval-2 by training with the combination of SemCor and WordNet's Tagged Glosses^[[15]](#ref-15)^. It is worth noting that, the categorical cross-entropy, which is frequently utilized for training, limits the performances. In reality, it has been demonstrated that the binary cross-entropy loss performs better [[Conia and Navigli, 2021]](#ref-Conia.2021) because it enables the consideration of many annotations for a single instance in the training set as opposed to the use of a single ground-truth sense alone. In the above-mentioned approaches, each sense is assumed to be a unique class, and the classification architecture is limited to the information provided by the training corpus.

### 2.7.3. Knowledge-augmented Supervised WSD

The edges that connect the senses and synsets are a valuable source of knowledge that augments the annotated data. Traditionally, graph knowledge-based systems, such as those based on Personalized PageRank [[Scozzafava et al., 2020]](#ref-Scozzafava.2020), have taken advantage of this information. Moreover, utilizing WordNet as a graph has benefited many modern supervised systems. Thus, formally, knowledge-augmented supervised WSD is defined as a methodology that combines traditional supervised machine learning techniques with external knowledge resources to improve the accuracy and performance of word sense disambiguation.

[[Wang and Wang, 2020]](#ref-Wang.2020) used WordNet hypernymy and hyponymy relations to devise a try-again mechanism that refines the prediction of the WSD model. The SemCor corpus was utilized to acquire a supervised sense embedding for every annotated sense in their supervised method (SREF*S up*). [[Vial et al., 2019]](#ref-Vial.2019) reduced the number of output classes by mapping each sense to an ancestor in the WordNet taxonomy, then yielding a smaller but robust sense vocabulary. The authors used BERT contextualized embeddings. By training with SemCor and WordNet gloss corpora, the model achieved 79.7% F1 on SensEval-2. Different variations also achieve outstanding performance on diverse WSD datasets.

[[Loureiro and Jorge, 2019]](#ref-Loureiro.2019) created representations for those senses not appearing in SemCor by using the averaged neighbor embeddings in the WordNet. The token-tagger models EWISE [[Kumar et al., 2019]](#ref-Kumar.2019) and EWISER [[Bevilacqua and Navigli, 2020]](#ref-Bevilacqua.2020) both leveraged the WordNet graph structure to train the gloss embedding offline, where EWISER demonstrated how the WordNet entire graph feature can be directly extracted. EWISE used ConvE [[Dettmers et al., 2018]](#ref-Dettmers.2018) to obtain graph embeddings. [[Conia and Navigli, 2021]](#ref-Conia.2021) provided a new technique to use the same edge information by replacing the adjacency matrix multiplication with a binary cross-entropy loss where other senses connected to the gold sense are also taken into account. The edge information was obtained from WordNet. In general, edge information is increasingly used in supervised WSD, gradually blending with knowledge-based techniques. However, it can only be conveniently utilized by token classification procedures, whereas its incorporation into sequence classification techniques has not yet been researched.

It has also been extensively studied how to use sense definitions as an additional source for supervised WSD apart from the traditional data annotations. It considerably increased the scalability of a model on the senses that are underrepresented in the training corpus. [[Huang et al., 2019a]](#ref-Huang.2019a) argued that WSD has traditionally been approached as a binary classification task, whereby a model must accurately decide if the sense of a given word in context aligns with one of its potential meanings in a sense inventory, based on the provided definition. define the WSD task as a sentence-pair classification task, where the WordNet gloss of a target word is concatenated after an input sentence. [[Blevins and Zettlemoyer, 2020]](#ref-Blevins.2020) used a bi-encoder to project both words in context and WordNet glosses in a common vector space. Disambiguation is then carried out by determining the gloss that is most similar to the target word. Glosses are employed similarly by more advanced techniques like SensEmBERT [[Scarlini et al., 2020a]](#ref-Scarlini.2020a), ARES [[Scarlini et al., 2020b]](#ref-Scarlini.2020b), and SREF [[Wang and Wang, 2020]](#ref-Wang.2020). They used quite different approaches to find new contexts automatically in order to develop the supervised portion of the sense embedding. ARES achieved 78.0% F1 on the SensEval-2 dataset by utilizing collocational relations between senses to get novel example sentences from websites. SensEmBERT leveraged BabelNet and Wikipedia explanations, achieving significant improvements on

^15^<https://wordnetcode.princeton.edu/glosstag.shtml>

nominal WSD tasks over 5 major datasets. [[Barba et al., 2021a]](#ref-Barba.2021a) proposed to solve WSD as a text extraction problem where, given a word in context and all of its potential glosses, models extract the definition that best matches the term under consideration. The authors demonstrated the advantages of their approach in that it does not require huge output vocabularies and enables models to take into account both the input context and all meanings of the target word simultaneously. By using sparse coding, [[Berend, 2020]](#ref-Berend.2020) has demonstrated that it is also possible to make existing sense embeddings sparse. All of these methods handle each word independently of the others when disambiguating multiple words that co-occur in the same context. Thus, a word's explicit meaning is neither taken into account during word disambiguation nor does it have an impact on the disambiguation of surrounding words.

### 2.8. Downstream Applications
### 2.8.1. Sentiment Computing
WSD has been applied in many Sentiment Analysis (SA) works to improve accuracy and explainability. [[Farooq et al., 2015]](#ref-Farooq.2015) proposed a WSD framework to enhance the performance of sentiment analysis. To determine the orientation of opinions related to product attributes in a particular field, a lexical dictionary comprising various word senses is developed. The process involves extracting relevant features from product reviews and identifying opinion-bearing texts, followed by the extraction of words used to describe the features and their contexts to form seed words. These seed words, which consist of adjectives, nouns, verbs, and adverbs, are manually annotated with their respective polarities, and their coverage is extended by retrieving their synonyms and antonyms. WSD was utilized to identify the sentiment-orientated senses, such as the positive, negative, or neutral senses of a word in a sentence, because a word may have different sentiment polarities by taking different senses in different contexts.

[[Nassirtoussi et al., 2015]](#ref-Nassirtoussi.2015) offered a novel approach to forecast intra-day directional movements of the EUR/USD exchange rates based on news headline text mining in an effort to address semantic and sentiment components of text-mining. They evaluated news headlines semantically and emotionally using the lexicons, e.g., WordNet and SentiWordNet [[Baccianella et al., 2010]](#ref-Baccianella.2010). SentiWordNet is a publicly accessible lexical resource designed for sentiment analysis that allocates a positivity score, negativity score, and objectivity score to each synset within WordNet. [[Nassirtoussi et al., 2015]](#ref-Nassirtoussi.2015) found that both positive and negative emotions may influence the market in the same way. WSD worked as a technique to abstract semantic information in their framework. Thus, it enhances the feature representations and explainability in their downstream task modeling. SentiWordNet has served as a basis for various sentiment analysis models. In the work of [[Ohana and Tierney, 2009]](#ref-Ohana.2009), the feasibility of using the emotional scores of Senti-WordNet to automatically classify the sentiment of movie reviews was examined. Other applications, e.g., business opinion mining [[Saggionα and Funk, 2010]](#ref-Saggion.2010), article emotion classification [[Devitt and Ahmad, 2007]](#ref-Devitt.2007), word-of-mouth sentiment classification [[Hung and Lin, 2013]](#ref-Hung.2013); [[Hung and Chen, 2016]](#ref-Hung.2016) also showed that SentiWordNet as a semantic feature enhancement knowledge base can deliver accuracy gains and model insights in sentiment analysis tasks.

### 2.8.2. Information Retrieval
The impacts of using WSD for information retrieval have been examined in many works. [[Krovetz and Croft, 1992]](#ref-Krovetz.1992) disambiguated word senses for terms in queries and documents to examine how ambiguous word senses impact information retrieval performance. The researchers arrived at the conclusion that the advantages of WSD in information retrieval are marginal. This is due to the fact that query words have uneven sense distributions. The impact of collocation from other query terms already plays a role in disambiguation. WSD was used as a parser to study this task. However, the findings from [[Gonzalo et al., 1998]](#ref-Gonzalo.1998) are different. They examined the impact of improper disambiguation using SemCor. By accurately modeling documents and queries together with synsets, they achieved notable gains (synonym sets). Additionally, their study demonstrated that WSD with an error rate of 40%–50% may still enhance IR performance when used with the synset representation, which incorporated synonym information. [[Gonzalo et al., 1999]](#ref-Gonzalo.1999); [[Stokoe et al., 2003]](#ref-Stokoe.2003) further confirmed the significance of WSD to information retrieval. [[Gonzalo et al., 1999]](#ref-Gonzalo.1999) also found that PoS information has a lower utility for information retrieval. Based on artificially creating word ambiguity, [[Sanderson, 1994]](#ref-Sanderson.1994) employed pseudo words to explore the effects of sense ambiguity on information retrieval. They came to the conclusion that the high accuracy of WSD is a crucial condition to accomplish progress. [[Blloshmi et al., 2021]](#ref-Blloshmi.2021) introduced an innovative approach to multi-lingual query expansion by integrating WSD, which augments the query with sense definitions as supplementary semantic information in multi-lingual neural ranking-based IR. The results demonstrated the advantages of WSD in improving contextualized queries, resulting in a more accurate document-matching process and retrieving more relevant documents.

[[Kim et al., 2004]](#ref-Kim.2004) labeled words with 25 root meanings of nouns rather than utilizing fine-grained sense inventories of WordNet. Their retrieval technique preserved the stem-based index and changed the word weight in a document in accordance with the degree to which it matched the query's sense. They credited their coarse-grained, reliable, and adaptable sense tagging system with the improvement on TREC collections. The detrimental effects of disambiguation mistakes are somewhat mitigated by the addition of senses to the conventional stem-based index.

### 2.8.3. Machine Translation
The challenge of ambiguous word senses poses a significant barrier to the development of an efficient machine translator. As a result, a number of researchers have turned their attention to exploring WSD for machine translation. Some works tried to establish datasets to quantify the WSD capacity of machine translation systems. [[Rios Gonzales et al., 2017]](#ref-Rios.2017) proposed a test set of 6,700 lexical ambiguities for German-French and 7,200 for German-English. They discovered that WSD remains a difficult challenge for neural machine translation, especially for uncommon word senses, even with 70% of lexical ambiguities properly resolved. [[Campolungo et al., 2022]](#ref-Campolungo.2022) proposed a benchmark dataset that aims at measuring WSD biases in Machine Translation in five language combinations. They also agreed that SOTA systems still exhibited notable constraints when confronted with less common word senses. Incorporating sense labels and lexical chains leads to enhanced performance of Neural Machine Translation (NMT) models, particularly with regard to infrequent word senses. [[Raganato et al., 2019]](#ref-Raganato.2019) proposed MUCOW, a multi-lingual contrastive test set automatically created from word-aligned parallel corpora and the comprehensive multi-lingual sense inventory of BabelNet. MUCOW spans 16 language pairs and contains more than 200,000 contrastive sentence pairs. The researchers thoroughly evaluated the effectiveness of the ambiguous lexicons and the resulting test suite by utilizing pre-trained NMT models and analyzing all submissions across nine language pairs from the WMT19 news shared translation task.

Some works analyzed the internal representations to understand the disambiguation process in machine translation systems. [[Marvin and Koehn, 2018]](#ref-Marvin.2018) examined the extent to which ambiguous word senses could be decoded through the use of word embeddings in relation to deeper layers of the NMT encoder, which were believed to represent words with contextual information. In line with prior research, they discovered that the NMT system frequently mistranslated ambiguous terms. [[Tang et al., 2019]](#ref-Tang.2019) trained a classifier to determine if a translation is accurate given the representation of an ambiguous noun. The fact that encoder hidden states performed much better than word embeddings suggests that encoders are able to appropriately encode important data for disambiguation into hidden states. [[Liu et al., 2018a]](#ref-Liu.2018a) discovered that an increase in the number of senses associated with each word results in a decline in the performance of word-level translation. The root of the issue may be the mapping of each word to similar word vectors, regardless of its context. They proposed to integrate techniques from neural WSD systems into an NMT system to address this issue.

### 2.9. Summary
WSD as a computational linguistics task most closely related to lexical semantics research, has won extensive discussions among researchers from different fields. Linguists came up with important hypotheses to guide the modeling of word senses. We have observed that some hypotheses have been well grounded in NLP, e.g., learning and representing word meanings with their contexts and word co-occurrences. However, we also observe some important linguistic arguments were rarely studied in the computational linguistic domain, e.g., defining the scope of linguistic units for WSD and integrating relevant concepts (frames) for word sense representations. The development of WSD datasets has greatly ignited the research enthusiasm of scholars in WSD. However, we also observed that the computational research on WSD is also limited by these well-defined datasets because WSD datasets generally follow a very similar labeling paradigm. Relevant linguistic studies have shown broader possibilities in WSD. Finally, we find that many of WSD modeling techniques do not link well with downstream applications. The research of WSD methods has intersections with downstream applications, whereas they cannot well cover the needs of downstream tasks. This also shows that the research opportunities in WSD can be largely extended besides word sense classification.

### 2.9.1. Technical Trends
Table [[4]](#ref-Table.4) shows the technical trends of WSD methods. As seen in the table, earlier approaches likely used knowledge-based and supervised approaches. WordNet and BabelNet are useful knowledge bases that were frequently

| Task | Reference | Tech | Feature and KB. | Framework | Dataset | Score | Metric |
|:----------|:-------------------------------|:-------|:------------------------|:----------------------------------------------|:-----------------------|:--------|:--------|
| | [[Lesk, 1986]](#ref-Lesk.1986) | Prob. | Statistics, OALD | Count def. overlaps | - | - | - |
| | [[Banerjee et al., 2003]](#ref-Banerjee.2003) | ML | Emb., WN | Score function | SensEval-2 | 34.60% | F1 |
| | [[Navigli and Lapata, 2007]](#ref-Navigli.2007) | Graph | Sense graph, WN | Connectivity measures | SemCor | 31.80% | F1 |
| | [[Basile et al., 2014]](#ref-Basile.2014) | Prob. | Emb., BN | DSM | SE2013-EN | 71.50% | F1 |
| Knwl | [[Wang and Wang, 2020]](#ref-Wang.2020)KB | DL | BERT, WN | Vector represent. | SensEval-2 | 72.70% | F1 |
| | [[Agirre and Soroa, 2009]](#ref-Agirre.2009) | Graph | WN | PageRank | SensEval-2 | 58.60% | Recall |
| | [[Moro et al., 2014b]](#ref-Moro.2014b) | Graph | Sem. graph, BN | PageRank | SE2013-EN | 69.20% | F1 |
| | [[Scozzafava et al., 2020]](#ref-Scozzafava.2020) | Graph | WN, SN | PageRank | SensEval-2 | 71.60% | F1 |
| | [[Singh et al., 2014]](#ref-Singh.2014) | ML | 5-gram, position | Decision Tree | Manipuri | 71.75% | Acc |
| | [[O'Hara et al., 2004]](#ref-OHara.2004) | ML | Relatedness scores | Decision Tree | SensEval-3 | 65.90% | F1 |
| | [[Zhong and Ng, 2010]](#ref-Zhong.2010) | ML | Position, PoS | SVM | SensEval-2 | 68.20% | F1 |
| | [[Iacobacci et al., 2016]](#ref-Iacobacci.2016) | ML | Emb., position, PoS | SVM | SensEval-2 | 68.30% | F1 |
| Sup. | [[Popov, 2017]](#ref-Popov.2017) | DL | Emb. | BiLSTM | SensEval-2 | 70.11% | Acc |
| | [[Yuan et al., 2016]](#ref-Yuan.2016) | DL | Emb., label propag. | LSTM | SensEval-2 | 74.40% | F1 |
| | [[Le et al., 2018]](#ref-Le.2018) | DL | Emb. | LSTM | SensEval-2 | 72.00% | F1 |
| | [[Hadiwinoto et al., 2019]](#ref-Hadiwinoto.2019) | DL | BERT | Transformer | SensEval-2 | 76.40% | F1 |
| | [[Bevilacqua and Navigli, 2019]](#ref-Bevilacqua.2019) | DL | Emb. | BiTransformer | SensEval-2 | 75.70% | F1 |
| | [[Wang and Wang, 2020]](#ref-Wang.2020)S up | DL | BERT, WN | Vector represent. | SensEval-2 | 78.60% | F1 |
| | [[Vial et al., 2019]](#ref-Vial.2019) | DL | BERT, WN | Transformer | SensEval-2 | 79.70% | F1 |
| | [[Loureiro and Jorge, 2019]](#ref-Loureiro.2019) | DL | BERT, WN | Transformer | SensEval-2 | 76.30% | F1 |
| | [[Kumar et al., 2019]](#ref-Kumar.2019) | DL | Graph emb.,<br>emb., WN | BiLSTM, Att.<br>ConvE | SensEval-2 | 73.80% | F1 |
| | [[Bevilacqua and Navigli, 2020]](#ref-Bevilacqua.2020) | DL | BERT, WN | Trans., Struct. logit | 5 datasets | 80.80% | F1 |
| | [[Conia and Navigli, 2021]](#ref-Conia.2021) | DL | BERT, WN | Transformer | SensEval-2 | 78.40% | F1 |
| | [[Huang et al., 2019a]](#ref-Huang.2019a) | DL | BERT, WN | Transformer, sentence-<br>pair classification | SensEval-2 | 77.70% | F1 |
| Knwl<br>+ | [[Blevins and Zettlemoyer, 2020]](#ref-Blevins.2020) | DL | BERT, WN | Trasformer, Score Func. | SensEval-2 | 79.40% | F1 |
| Sup. | [[Scarlini et al., 2020a]](#ref-Scarlini.2020a) | DL | BERT, BN, Wiki | Transformer, Context<br>Retrieval | 5 datasets<br>Nouns of | 80.40% | F1 |
| | [[Scarlini et al., 2020b]](#ref-Scarlini.2020b) | DL | BERT, WN, SN | Transformer, Context<br>Retrieval | SensEval-2 | 78.00% | F1 |
| | [[Barba et al., 2021a]](#ref-Barba.2021a) | DL | BERT, WN | Transformer, Extractive<br>Sense Learning | SensEval-2 | 81.70% | F1 |
| | [[Berend, 2020]](#ref-Berend.2020) | DL | BERT, WN | Transformer, sparse<br>coding, PMI | SensEval-2 | 79.60% | F1 |
| | | | | | | | |

**Table 4:** A summary of representative WSD techniques. Knwl denotes knowledge-based methods. Sup. denotes supervised methods. KB denotes knowledge bases. WN denotes WordNet. BN denotes BabelNet. DSM denotes Distributional Semantics Models. Prob. denotes probability. SE2013-EN denotes the SemEval2013 English WSD task. PMI denotes Pointwise Mutual Information.

| Reference | Downstream Task | Feature | Parser | Explainability |
|:----------------------------|:-----------------------|:--------|:-------|:---------------|
| [[Farooq et al., 2015]](#ref-Farooq.2015) | Sentiment Computing | ✓ | | |
| [[Nassirtoussi et al., 2015]](#ref-Nassirtoussi.2015) | Sentiment Computing | ✓ | | ✓ |
| [[Ohana and Tierney, 2009]](#ref-Ohana.2009) | Sentiment Computing | ✓ | ✓ | |
| [[Saggionα and Funk, 2010]](#ref-Saggion.2010) | Sentiment Computing | ✓ | ✓ | ✓ |
| [[Devitt and Ahmad, 2007]](#ref-Devitt.2007) | Sentiment Computing | ✓ | | ✓ |
| [[Hung and Lin, 2013]](#ref-Hung.2013) | Sentiment Computing | ✓ | ✓ | |
| [[Hung and Chen, 2016]](#ref-Hung.2016) | Sentiment Computing | ✓ | ✓ | ✓ |
| [[Krovetz and Croft, 1992]](#ref-Krovetz.1992) | Information Retrieval | | ✓ | |
| [[Gonzalo et al., 1998]](#ref-Gonzalo.1998) | Information Retrieval | | | ✓ |
| [[Gonzalo et al., 1999]](#ref-Gonzalo.1999) | Information Retrieval | | | ✓ |
| [[Sanderson, 1994]](#ref-Sanderson.1994) | Information Retrieval | | | ✓ |
| [[Stokoe et al., 2003]](#ref-Stokoe.2003) | Information Retrieval | | | ✓ |
| [[Kim et al., 2004]](#ref-Kim.2004) | Information Retrieval | ✓ | ✓ | |
| [[Blloshmi et al., 2021]](#ref-Blloshmi.2021) | Information Retrieval | ✓ | | ✓ |
| [[Rios Gonzales et al., 2017]](#ref-Rios.2017) | Machine Translation | ✓ | | |
| [[Raganato et al., 2019]](#ref-Raganato.2019) | Machine Translation | ✓ | | |
| [[Marvin and Koehn, 2018]](#ref-Marvin.2018) | Machine Translation | | ✓ | ✓ |
| [[Tang et al., 2019]](#ref-Tang.2019) | Machine Translation | ✓ | | ✓ |
| [[Liu et al., 2018a]](#ref-Liu.2018a) | Machine Translation | ✓ | | |

**Table 5:** A summary of the representative applications of WSD in downstream tasks. ✓ denotes the role of WSD in a downstream task.

used by knowledge-based methods. Word embeddings, pre-trained language models, and linguistic features, e.g., PoS tags and semantic relatedness were frequently used by supervised methods. For old pure knowledge-based methods, the PageRank framework was likely used, because many knowledge bases are represented as graphs. PageRank is an algorithm used in graph computation to measure the importance of nodes in a graph. Classical machine learning techniques, e.g., Decision Tree, SVM, LSTM, and Transformers were commonly used by supervised WSD methods. Supervised learning algorithms demonstrate superior performance in comparison to knowledge-based approaches. Nevertheless, it is not always reasonable to assume the availability of substantial training datasets for different areas, languages, and activities. [[Ng, 1997]](#ref-Ng.1997) predicted that a corpus of around 3.2 million sense-tagged words would be necessary in order to produce a high-accuracy, wide-coverage disambiguation system. The creation of such a training corpus requires an estimated 27 person-years of labor. The accuracy of supervised systems might be greatly improved above the SOTA methods with such a resource. However, the success of this hypothesis is at the cost of huge resource consumption.

We observe more hybrid approaches that leverage knowledge bases in a supervised learning fashion in recent years. This is because researchers have observed the limitations of typical supervised WSD in processing rare or unseen cases. Knowledge bases provide additional information to support the learning of unseen cases. Knowledge bases provide additional knowledge for the languages whose annotated data are scarce. In this case, multi-lingual knowledge bases can enhance the representations of word senses in a new domain. As a result, we can observe the accuracy of the hybrid approaches surpasses the pure knowledge-based or supervised approaches.

Most existing WSD datasets define the task as a word sense classification task. Then, the following methodology research upon the datasets focused on improving the accuracy of mapping the sense of a word to its dictionary sense class. However, should the research on WSD be limited to word sense classification? We have observed that many knowledge-based systems used existing knowledge bases to conduct word sense classification tasks. They have realized the importance of developing an effective knowledge base for WSD. However, it is rare to see that WSD research tries to improve the construction of knowledge bases according to the effectiveness of word sense classification. On the other hand, the meaning of WSD is much larger than detecting the definition of words in a dictionary. Mapping a word to a sense in a dictionary is just an aspect of WSD. Previous works rarely studied what is an appropriate linguistic unit for WSD; what concepts are associated with a word sense in a context. These are very interesting research topics from linguistic and cognitive aspects. However, these topics were not well studied in the computational WSD community.

### 2.9.2. Application Trends
The WSD task was commonly defined as a word sense classification task. However, we observe that classifying words by sense classes is not the only need for downstream NLP tasks.

There are three main tasks that are strongly related to WSD, e.g., sentiment computing, information retrieval, and

machine translation in our survey. One of the roles of WSD on the three tasks is to deliver or enhance features to gain improvements on the three tasks. On the other hand, we also observe many downstream works used WSD techniques as a parser to obtain words with different levels of word sense ambiguity or used WSD to gain insights into their model behaviors to improve the explainability of a study. In these cases, defining WSD as a sense classification task may be sub-optimal for downstream applications.

WSD has a huge potential in NLP research. For example, disambiguating word senses in a large corpus can lead to a deeper understanding of language usage patterns and the semantic relationships between words. WSD is also a significant component in semantic explainable AI, because it helps researchers better understand the decisionmaking process of a model on the semantic level. Researchers can develop a more transparent and trustworthy model by explaining word senses in contexts. As a feature generator, a WSD may be more effective if it can generate contextualized word meanings in natural language, rather than predict a sense class that maps to a predefined gloss in a dictionary. However, research in these fields is rare in the WSD community.

Finally, according to [[Navigli, 2009]](#ref-Navigli.2009), the lack of end-to-end applications that utilize WSD can be attributed to the insufficient accuracy of current WSD systems. This suggests that in the future, more precise WSD systems may be developed, which could potentially enable the use of more semantics-dependent applications.

### 2.9.3. Future Works
As argued before, the task of WSD can be broader than the current word sense classification task setup from either the theoretical research side or the downstream application side. Besides, the improvements in WSD accuracy can also attract more downstream applications. Thus, we come up with the following future work suggestions.

Extending the form of WSD. WSD can have different learning forms, besides word sense classification, e.g., paraphrasing an ambiguous word into a less ambiguous one [[Mao et al., 2018]](#ref-Mao.2018), [[2022b]](#ref-Mao.2022b), generating contextualized word senses in natural language. Such an extension may have significance in downstream applications. From the perspective of linguistic and cognitive research, studying how to define a language unit to better disambiguate word senses, or studying how to link a word to its associated concepts in a context can also improve the significance of WSD in the era of LLM-based NLP. Future works may study how to define the task of WSD to better support the research in different disciplines.

Rethinking existing knowledge bases by WSD. Most of the existing knowledge bases were developed according to human-defined ontologies and word senses. These knowledge bases have been considered as an important resource for many knowledge-based systems. Although the knowledge bases have been used on different tasks, few works analyzed the weakness of the ontologies. Future WSD-related research may try to improve the knowledge bases by rethinking the sense definition, concept node connections, and coverage, rather than simply developing models to enhance the learning ability on a specific task.

Multi-lingual WSD. Most of the semantic representations are learned from monolingual corpora. As a result, the semantic representations are different between different languages. However, the disambiguation of meanings is not characterized by languages [[Boroditsky, 2011]](#ref-Boroditsky.2011). It will significantly improve multi-lingual semantic research if WSD research can break down language barriers from a cognitive perspective. As argued by frame semantics [[Fillmore et al., 2006]](#ref-Fillmore.2006), the meaning of a word is beyond its dictionary definitions. It also associates with the concepts, interconnected with the word. Representing word senses by concepts may achieve a more robust multi-lingual WSD.

Learning WSD as a pre-training task. Recent years witness great success of PLMs in various domains. The existing PLMs followed the same hypothesis that the sense of a word can be learned from its associated context. However, there has not been a PLM that explicitly disambiguates word senses to enhance the learning of semantic representations. Naively learning the semantic representation of a target word by its associated context words cannot learn the conceptual association of the target word. For example, many words can associate with the word "apple". How can we know an apple as fruit is red or green, sweet, tree-growing, nutritious, etc? As an electronic device, Apple is associated with an operating system, a circuit board, a brand, etc. Disambiguating word senses before pre-training may build such connections between concepts.

Fusing WSD with other tasks. As [[Bevilacqua et al., 2021b]](#ref-Bevilacqua.2021b) argued, WSD can also be integrated with an entity linking task [[Moro et al., 2014b]](#ref-Moro.2014b), where the model predicts associated entities to help WSD systems explore the related glosses and relations. Related fusion works also include fusing WSD for Sentiment Analysis [[Farooq et al., 2015]](#ref-Farooq.2015), Information Retrieval [[Blloshmi et al., 2021]](#ref-Blloshmi.2021) and Machine Translation [[Campolungo et al., 2022]](#ref-Campolungo.2022). The future study of WSD can be grounded on an end task so that the end task can more effectively benefit from the fusion of a WSD model.

## 3. Anaphora Resolution

In computational linguistics, Ruslan Mitkov defined anaphora as a *phenomena of pointing back a previously mentioned item in the text* [[Mitkov, 2022]](#ref-Mitkov.2022). The pointing back phrase is called an *anaphor* while the previously mentioned item is called an *antecedent*.

The concept of anaphora should not be confused with co-reference. On the one hand, either anaphora or cataphora (e.g., the phenomena of pointing ahead to a subsequently mentioned item) could be a kind of co-reference. On the other hand, an anaphor and its antecedent are not always co-referential. By definition, the difference between anaphora and co-reference is that anaphora does not require *identify-of-reference* while co-reference requires. In other words, anaphora may describe a relation between expressions that do not have the same referent. For example, in sentence [[2]](#ref-2), the anaphor "one" has the same sense as its antecedent "a dog", but they do not refer to the same dog.

(2) Jack has a dog and Mary also has one.

Building on this, in relation to anaphora, both anaphor and its antecedent are not necessarily referring expressions. For instance, an anaphor can be a verb (henceforth, verb anaphora). In the following example from [[Mitkov, 2014]](#ref-Mitkov.2014),

(3) When Manchester United swooped to lure Ron Atkinson away from the Albion, it was inevitable that his midfield prodigy would follow, and in 1981 he did.

the anaphor "did" is a verb, having an antecedent "follow". Another example is the *bound anaphora* where the antecedent is a quantified expression [[Reinhart, 1983]](#ref-Reinhart.1983):

(4) Each manager exploits the secretary who works for "him".

The anaphor "him" refers to the quantified expression "each manager". Since antecedents in both above two examples are not referring expressions, neither of them is a co-reference.

Given the definition of anaphora, the task of anaphora resolution is to identify the antecedent of an anaphor. In this survey, we decided to merely focus on anaphora resolution (rather than co-reference resolution) because, on the one hand, most semantic processing tasks only require identifying antecedents. On the other hand, we are not only interested in referring to noun phrases but also other phrases that an anaphor can refer to (e.g., verb phrases and quantified expressions; see the discussion above).

It is worth noting that there have been reviews in the past 20 years about AR/CR from either computer scientists [[Sukthanker et al., 2020]](#ref-Sukthanker.2020); [[Liu et al., 2023c]](#ref-Liu.2023c) or linguists [[Mitkov, 2022]](#ref-Mitkov.2022); [[Poesio et al., 2023]](#ref-Poesio.2023). In this survey, our objective is to establish a connection between AR techniques across theoretical research and practical applications.

## 3.1. Theoretical Research

### 3.1.1. Constraints

When human beings resolute co-reference, there are semantic and syntactic constraints. As for the semantic constraints, agreements such as gender and number agreements are the strongest type [[Garnham, 2001]](#ref-Garnham.2001). However, most recently, agreement mismatch problems (especially for gender agreements) have been becoming more frequent since more people have started to use plural pronouns to avoid gender bias.

As for syntactic constraints, according to the binding theory [[Buring, 2005]](#ref-Buring.2005), in the sentence (a) of the following example, "John" cannot co-refer with "him" while in the sentence (b) "John" can.

### (5) a. John likes him.

b. John likes him in the mirror.

### 3.1.2. Centering Theory
Centering Theory [[Joshi and Kuhn, 1979]](#ref-Joshi.1979); [[Grosz et al., 1983]](#ref-Grosz.1983), [[1995]](#ref-Grosz.1995) was introduced as a model of *local coherence*^[[16]](#ref-16)^ based on the idea of *center of attention*. The theory assumes that, during the production or comprehension of a discourse, the discourse participant's attention is often centered on a set of entities (a subset of all entities in the discourse) and such an *attentional state* evolves dynamically. It models transitions of the attentional state and defines three types of transitions: CONTINUE, RETAIN, and SHIFT. For each utterance, the transition is decided by its backward-looking center (defined as the most salient entity in the previous utterance that is also realized in the current utterance and denoted as *Cb*) as well as forward-looking center (defined as the most salient entity in the current utterance and denoted as *Cf*). Consider the following discourse adopted from [[Kehler, 1997]](#ref-Kehler.1997):

- (6) a. Terry really gets angry sometimes.
- b. Yesterday was a beautiful day and he was excited about trying out his new sailboat. [*C*~b~ = Terry, *C*~f~ = Terry]
- c. He wanted Tony to join him on a sailing expedition, and left him a message on his answering machine. [*C*~b~ = Terry, *C*~f~ = Terry]
- d. Tony called him at 6AM the next morning. [*C*~b~ = Terry, *C*~f~ = Tony]
- e. Tony was furious with him for being woken up so early. [*C*~b~ = Tony, *C*~f~ = Tony]

where we annotate each utterance with its backward-looking and forward-looking centers. The transition from utterance [[6-a]](#ref-6a) to [[6-b]](#ref-6b) is a CONTINUE as both backward-looking and forward-looking centers are unchanged. The next one is a RETAIN transition since although the most salient entity changes (i.e., *Cf*), the forward-looking center stays the same, whereas the transition from utterance [[6-d]](#ref-6d) to [[6-e]](#ref-6e) is a SHIFT transition because of the change of backwardlooking transition. Intuitively, a discourse with more CONTINUE transitions is more coherent than the one with more SHIFT transitions.

Though Centering Theory is not a theory of Anaphora Resolution, Anaphora Resolution can directly benefit from modeling transitions, which provides certain information about the preference for the referents of pronouns (e.g., in a coherent segment, centers co-refer; see [[Joshi et al., 2006]](#ref-Joshi.2006) for more discussion about the relation between Centering Theory and Anaphora Resolution).

### 3.1.3. Discourse Salience
A prominent strand of work in psycholinguistics investigates how human beings use anaphora. A referent is more likely to be realized as a pronoun if it is salient in a given discourse [[Givon, 1983]](#ref-Givon.1983) (aka. *discourse salience*). Discourse salience is thought to be influenced by various factors, including givenness [[Chafe, 1976]](#ref-Chafe.1976); [[Gundel et al., 1993]](#ref-Gundel.1993), grammatical role [[Brennan, 1995]](#ref-Brennan.1995); [[Stevenson et al., 1994]](#ref-Stevenson.1994), recency [[Givon, 1983]](#ref-Givon.1983); [[Arnold, 1998]](#ref-Arnold.1998), syntactic parallelism [[Chambers and Smyth, 1998]](#ref-Chambers.1998); [[Arnold, 1998]](#ref-Arnold.1998), and many other factors. Similar to Centering Theory, most research on discourse salience is about the production of anaphora [[McCoy and Strube, 1999]](#ref-McCoy.1999); [[Orita et al., 2014]](#ref-Orita.2014), [[2015]](#ref-Orita.2015); [[Chen et al., 2018a]](#ref-Chen.2018a), but it also provides insights about an antecedent's relative likelihood for a given anaphor in a given discourse. In this sense, it is plausible to use the aforementioned factors as features to rank candidate antecedents of an anaphor [[Lappin and Leass, 1994a]](#ref-Lappin.1994a); [[Bos, 2003]](#ref-Bos.2003).

### 3.1.4. Coolness

[[Huang, 1984]](#ref-Huang.1984) classified human languages into cool languages and hot languages. If a language is "cooler" than another language, then understanding a sentence in that language relies more on context (see [[Chen, 2022]](#ref-Chen.2022); [[Chen and van Deemter, 2022]](#ref-Chen.2022a); [[Chen et al., 2023]](#ref-Chen.2023) for computational investigations of the theory of Coolness). The evidence that [[Huang, 1984]](#ref-Huang.1984) identified is about the differences between the use of anaphora. Specifically, cool languages (e.g., Mandarin) make liberal use of zero pronouns. Take the following conversation as an example:

(7) a. ^你^今天看见比尔了吗?(Did you see Bill today?) b. *pro*看见*pro*了。(*I* saw *him*.)

^16^Instead of focusing on the whole discourse, centering theory focuses only on the *discourse segment*.

where a *pro* represents a zero pronoun^[[17]](#ref-17)^ (ZP). The first ZP refers to one of the speakers while the second ZP refers to Bill. ZPs of this kind are called Anaphoric ZPs (AZPs). In addition to Mandarin, a number of other languages (i.e., cool languages) also allow ZPs, including examples like Japanese, Arabic, and Korean. The current theory suggests that the anaphora resolution of cool languages should also take AZPs into consideration, namely AZP resolution [[Chen and Ng, 2013]](#ref-Chen.2013).

### 3.2. Annotation Schemes
In this subsection, we introduce two commonly used annotation schemes for anaphora resolution: MUC and MATE. There are also other schemes, for example, the Lancaster scheme [[Fligelstone, 1992]](#ref-Fligelstone.1992) and the DRAMA scheme [[Passonneau, 1997]](#ref-Passonneau.1997).

### 3.2.1. MUC
MUC [[Hirschman et al., 1997]](#ref-Hirschman.1997); [[Hirschman and Chinchor, 1998]](#ref-Hirschman.1998) is one of the very first schemes, which is used for annotating the MUC [[Chinchor and Sundheim, 1995]](#ref-Chinchor.1995) and the ACE [[Doddington et al., 2004]](#ref-Doddington.2004) corpora and is still widely used these years. It is primary goal is to annotate co-reference chains in discourse, in which MUC defines and proposes to annotate the IDENTITY (IDENT) relation. Relations as such are symmetrical (i.e., if A IDENT B, then B IDENT A) and transitive (i.e., if A IDENT B and B IDENT C, then A IDENT C). Annotation is done using SGML, for example:

(8) <COREF ID="100">Lawson Mardon Group Ltd.</COREF>said <COREF ID="101" TYPE="IDENT" REF="100">it</COREF> ...

The annotation above construct a link between the pronoun "it" and the noun phrase "Lawson Mardon Group Ltd.".

MUC proposes to annotate co-reference chains following a paradigm analogous to anaphora resolution. Annotators are first asked to annotate markable phrases (e.g., nouns, noun phrases, and pronouns) and partition the phrases into sets of co-referring elements. This helps the annotation task achieve good inter-annotator agreement (i.e., larger than 95%).

Nevertheless, it has been pointed out by [[Deemter and Kibble, 2000]](#ref-Deemter.2000) that MUC has certain flaws: MUC does not guarantee that the annotated relations are all co-referential. It includes either relation that does not follow the principle of identity-of-reference or bound anaphora. Therefore, the resulting corpus would often be a mixture of co-reference and anaphora.

### 3.2.2. MATE
Instead of annotating a single device INDENT, MATE [[Poesio et al., 1999a]](#ref-Poesio.1999a); [[Poesio, 2004]](#ref-Poesio.2004) was proposed to do so-called "anaphoric annotation" which is explicitly based on the discourse model assumption [[Heim, 1982]](#ref-Heim.1982); [[Gundel et al., 1993]](#ref-Gundel.1993); [[Webber, 2016]](#ref-Webber.2016); [[Kamp and Reyle, 2013]](#ref-Kamp.2013). The scheme was first proposed to annotate anaphora in dialogues but was then extended to relations in discourse (see [[Pradhan et al., 2012]](#ref-Pradhan.2012) for more details). Such a good extensibility is a result of the fact that MATE is a *meta-scheme*: It consists of a core scheme and multiple extensions. The core scheme can be used to conduct the same annotation task as MUC and can be extended with respect to different tasks. The annotation normally uses XML, but many of its extensions use other their own formats.

### 3.2.3. Zero Pronoun, Bridging Reference, and Deictic Reference

In addition to the "co-referential" relation discussed above, many are also interested in "hard" cases, each kind of which is often annotated as following an extension of MATE. These include the following three: (1) zero pronoun: [[Pradhan et al., 2012]](#ref-Pradhan.2012) annotated (both anaphoric and non-anaphoric) ZPs in Chinese and Arabic (see Section [[3.1.4]](#ref-Section.3.1.4)); (2) bridging reference: bridging anaphora is a kind of indirect referent, where the antecedent of an anaphor is not explicitly mentioned but "associated" information is mentioned [[Clark, 1975]](#ref-Clark.1975). Identifying such a relation needs commonsense inference. Consider the following example from [[Clark, 1975]](#ref-Clark.1975):

(9) I looked into the room. The ceiling was very high.

^17^In linguistics, a zero pronoun is a pronoun that is implied but not explicitly expressed in a sentence.

| Reference |
|:-----------------------------|
| [[Chinchor and Sundheim, 1995]](#ref-Chinchor.1995) |
| [[Doddington et al., 2004]](#ref-Doddington.2004) |
| [[Poesio, 2000]](#ref-Poesio.2000) |
| [[Hovy et al., 2006]](#ref-Hovy.2006) |
| [[Levesque et al., 2012]](#ref-Levesque.2012) |
| [[Rahman and Ng, 2012]](#ref-Rahman.2012) |
| [[Webster et al., 2018]](#ref-Webster.2018) |
| [[Hasler et al., 2006]](#ref-Hasler.2006) |
| [[Cybulska and Vossen, 2014]](#ref-Cybulska.2014) |
| [[Poesio and Artstein, 2008b]](#ref-Poesio.2008b) |
| |

**Table 6:** Anaphora Resolution datasets and statistics.

"the room" is an antecedent of "the ceiling" because the room has a ceiling; (3) deictic reference: deixis [[Webber, 1988]](#ref-Webber.1988) is a phrase that refers to the "speaker's position" (e.g., time, place, and situation), which is always abstracted. For example, in

### (10) I went to school yesterday.

the first person pronoun "I" and the word "yesterday" are deictic references, which refer to the speaker and the day before the date when [[10]](#ref-10) was uttered, respectively. Schemes like ARRAU [[Poesio and Artstein, 2008a]](#ref-Poesio.2008a) extended MATE and is able to annotate bridging and deictic references.

### 3.3. Datasets

As we discussed when we introduced annotation schemes in Section [[3.2]](#ref-Section.3.2), there is no clear cut between co-reference and anaphora in computational linguistics research. We hereby review either mainstream corpora utilized in Anaphora Resolution or co-reference resolution, while being mindful of the scope of each of them. The datasets and their statistics are summarized in Table [[6]](#ref-Table.6).

The 6th version of MUC (MUC-6, [[Chinchor and Sundheim, 1995]](#ref-Chinchor.1995)) is the first corpus that enables the co-reference resolution, where the task of co-reference resolution and the MUC annotation scheme was first defined. Its texts are inherited from the prevision MUCs and are English news. An example of MUC-6 is shown in Example [[8]](#ref-8). [[Chinchor, 1998]](#ref-Chinchor.1998) updated MUC-6 in 2001 and construct the MUC-7/MET-2 corpus. MUC-7 was designed to be multi-lingual (NB: data in Chinese and Japanese are included in MET-2, which has been considered as a part of MUC-7) and to be more carefully annotated than MUC-6 by providing annotators with a clearer task definition and finer annotation guidelines.

ACE is a multi-lingual (i.e., English, Chinese, and Arabic) multi-domain co-reference resolution corpus [[Doddington et al., 2004]](#ref-Doddington.2004). In terms of co-reference resolution, it was built with the same purpose as MUC^[[18]](#ref-18)^ and they same problems pointed by [[Deemter and Kibble, 2000]](#ref-Deemter.2000) (see Section [[3.2]](#ref-Section.3.2) for more discussion). In addition to MUC and AEC, there are works following the MUC scheme, while targeting domains other than news, which include GENIA [[Kim et al., 2003]](#ref-Kim.2003), GUM [[Zeldes, 2017]](#ref-Zeldes.2017), and PRECO [[Chen et al., 2018b]](#ref-Chen.2018b).

The GNOME corpus was first proposed to investigate the effect of salience on language production (see Section [[3.1.3]](#ref-Section.3.1.3) and [[Poesio, 2000]](#ref-Poesio.2000); [[Pearson et al., 2001]](#ref-Pearson.2001)) and then be used to develop and evaluate anaphora resolution algorithms [[Poesio, 2003]](#ref-Poesio.2003); [[Poesio and Alexandrov-Kabadjov, 2004]](#ref-Poesio.2004) targeting especially the bridging reference resolution, in the course of which the MATE scheme was introduced (see Section [[3.2]](#ref-Section.3.2)). GNOME is an English multi-domain corpus. The initial GNOME corpus [[Poesio et al., 1999b]](#ref-Poesio.1999b) consists of data from the museum domain (building on the SOLE project [[Hitzeman et al., 1998]](#ref-Hitzeman.1998)) and patient information leaflets (building on the ICONOCLAST project), which is then expended to include tutorial dialogues [[Poesio, 2000]](#ref-Poesio.2000). GNOME followed the MATE scheme. Each noun phrase is marked by an <*ne*> and its anaphoric relations (marked by) are annotated separately, for example:

^18^Though, in terms of entity recognition, they don't have the same purpose.

```text
<ne ID="ne07" ... >
Scottish-born, Canadian-based jeweller, Alison Bailey-Smith</ne>
...
<ne ID="ne08"> <ne ID="ne09">Her</ne> materials</ne>
<ante current="ne09">
<anchor ID="ne07" rel="ident" ... >
</ante>
```

OntoNotes [[Hovy et al., 2006]](#ref-Hovy.2006) is a multi-lingual (i.e., English, Chinese, and Arabic) multi-domain dataset. It is one of the most commonly used anaphora/co-reference resolution and was used in the CoNLL 2012 shared task [[Pradhan et al., 2012]](#ref-Pradhan.2012). It was annotated following an adapted version of the MATE (named M/O scheme by [[Poesio et al., 2023]](#ref-Poesio.2023)). Though it has been widely used in co-reference resolution tasks, many of its relations are not co-reference. For example, bound anaphora frequently appear (see the start of this section for more discussion). Additionally, OntoNotes annotates ZPs in its Chinese and Arabic portions (see Section [[3.1.4]](#ref-Section.3.1.4)). There are other corpora following M/O, but targeting different domains, including the biomedical (e.g., CRAFT [[Cohen et al., 2017]](#ref-Cohen.2017)), Wikipedia (e.g., GAP [[Webster et al., 2018]](#ref-Webster.2018) and WikiCoref [[Ghaddar and Langlais, 2016]](#ref-Ghaddar.2016)), and literary text (e.g., LitBank [[Bamman et al., 2020]](#ref-Bamman.2020)); and different anaphorical phenomena, including bridging anaphora (e.g., ISNOTE [[Hou et al., 2018]](#ref-Hou.2018)), style variation (e.g., WikiCoref [[Ghaddar and Langlais, 2016]](#ref-Ghaddar.2016)), and ambiguity (e.g., GAP [[Webster et al., 2018]](#ref-Webster.2018)).

ARRAU is an English multi-domain (i.e., dialogue, narrative, and news) anaphora resolution dataset, annotated following the MATE scheme [[Poesio and Artstein, 2008b]](#ref-Poesio.2008b); [[Uryupina et al., 2020]](#ref-Uryupina.2020). However, different from other corpora that also follow MATE, ARRAU extended MATE to annotate anaphoric ambiguity explicitly (recall that MATE is a meta-scheme). [[Poesio and Artstein, 2008b]](#ref-Poesio.2008b) introduced the *Quasi-identity* relation, which is used for the situation when co-refer is possible but not certain by annotators and allowed each anaphor to have two distinct interpretations. In the example sample below, the footnote "1,2" of the anaphor "it" means ambiguity exists and it can either refer to 'engine E2' or "the boxcar at Elmira".

(u1) M: can we .. kindly hook up ... uh ... [engine E2]^1^ to [the boxcar at Elmira]^2^ (u2) M: +and+ send [it]^1,^2^ to Corning as soon as possible please

The Winograd Scheme Challenge (WSC, [[Levesque et al., 2012]](#ref-Levesque.2012)) focuses on the "hard" cases of CR, which often require lexical and commonsense knowledge. It can be traced back to Terry Winograd's minimal pair [[Winograd, 1972]](#ref-Winograd.1972):

(11) a. The city council refused the demonstrators a permit because they feared violence.

b. The city council refused the demonstrators a permit because they advocated violence.

The antecedent of "they" changes from "the city council" to "the demonstrators" from [[11-a]](#ref-11a) to [[11-b]](#ref-11b). [[Levesque et al., 2012]](#ref-Levesque.2012) introduced the WSC benchmark consisting of hundreds of such minimal pairs. Since then, many largerscale WSC-like corpora have been constructed. This includes the DPR corpus [[Rahman and Ng, 2012]](#ref-Rahman.2012), the PDP corpus [[Davis et al., 2017]](#ref-Davis.2017), and the Winogrande corpus [[Sakaguchi et al., 2021]](#ref-Sakaguchi.2021). Following a similar paradigm, GAP [[Webster et al., 2018]](#ref-Webster.2018), Winogender [[Rudinger et al., 2018]](#ref-Rudinger.2018) and Winobias [[Zhao et al., 2018]](#ref-Zhao.2018) were proposed for "hard" cases that link to gender bias.

NP4E [[Hasler et al., 2006]](#ref-Hasler.2006) and ECB+ [[Cybulska and Vossen, 2014]](#ref-Cybulska.2014) are corpora for investigating cross-document co-reference. They annotated both entities and events co-reference and both within and cross-document co-reference. These corpora were built by starting from a set of clusters of documents, the documents of each of which describe the same fundamental events.

The corpora mentioned above are all in English, some of which have Chinese and Arabic portions. There are anaphora/co-reference resolution corpora that focus on languages other than them. These include ANCOR (in French, [[Muzerelle et al., 2013]](#ref-Muzerelle.2013)), ANCORA (in Catalan and Spanish [[Taule et al., 2008]](#ref-Taule.2008)), COREA (in Dutch [[Hendrickx et al., 2008]](#ref-Hendrickx.2008)), NAIST (in Japanese [[Iida et al., 2007b]](#ref-Iida.2007b)), PCC (in Polish [[Ogrodniczuk et al., 2013]](#ref-Ogrodniczuk.2013)), PCEDT (in Czech [[Nedoluzhko et al., 2014]](#ref-Nedoluzhko.2014)), and TUBA-DZ (in German [[Telljohann et al., 2004]](#ref-Telljohann.2004)).

| Name | Knowledge | #Entities | Structure |
|:-----------|:-----------|:------------|:-------------|
| WordNet | Lexical | 155,327 | Graph |
| COW | Lexical | 157,112 | Graph |
| ODW | Lexical | 92,295 | Graph |
| AWN | Lexical | ≈10,000 | Graph |
| Wikipedia | World | 13,489,694 | Unstructured |
| Wikidata | World | 100,905,254 | Graph |
| DBpedia | World | ≈4,580,000 | Graph |
| Freebase | World | ≈2.4 B | Graph |
| YAGO | World | 4,595,906 | Graph |
| WikiNet | World | 3,347,712 | Graph |
| OMCS | World | 62,730 | Graph |
| Medical-KG | World | 22,234 | Graph |

**Table 7:** Useful knowledge bases for anaphora resolution.

### 3.4. Knowledge Bases
Both lexical and world knowledge are useful for anaphor interpretation. See the following examples from [[Martin, 2015]](#ref-Martin.2015):

- (12) a. There was a lot of Tour de France riders staying at our hotel. Several of the athletes even ate in the hotel restaurant.
- b. She was staying at the Ritz, but even that hotel didn't offer dog walking service.

We need the lexical knowledge that indicates "riders" are "athletes" while need the world knowledge of the fact that "Ritz" is a "hotel".

WordNet provides lexical knowledge of English [[Miller, 1998]](#ref-Miller.1998), including lexical entries (e.g., meaning, part-ofspeech, etc.) and relations (e.g., synonyms, hyponyms, and meronyms, etc.) among them.

Wikipedia has been an important world knowledge source for many anaphora/co-reference resolution systems. These knowledge bases consist of documents from Wikipedia as well as related meta-data. Typical examples include bases from those directly dumped from raw Wikipedia documents^[[19]](#ref-19)^ to better-structured ones, such as Wikidata [[Vrandecic and Krotzsch, 2014]](#ref-Vrandecic.2014), DBpedia [[Auer et al., 2007]](#ref-Auer.2007), and Freebase [[Bollacker et al., 2008]](#ref-Bollacker.2008).

Knowledge Graphs have become popular in anaphora/co-reference resolution tasks because bases that build on raw Wikipedia are needed to be further processed (e.g., entity and relation extraction) before use. Popular knowledge graphs include those that build on Wikipedia (e.g., YAGO [[Suchanek et al., 2008]](#ref-Suchanek.2008) and WikiNet [[Nastase et al., 2010]](#ref-Nastase.2010)), that are about Commonsense (e.g., OMCS [[Singh, 2002]](#ref-Singh.2002)), and that are about expert knowledge (e.g., Medical-KG [[Uzuner et al., 2012]](#ref-Uzuner.2012)).

Search Engines, e.g., Bing and Google were also used by a few works (e.g., [[Emami et al., 2018]](#ref-Emami.2018)) to "hunt" knowledge for the target entities in order to resolve hard anaphora like those in WSC (see Section [[3.3]](#ref-Section.3.3)), in addition to the above knowledge bases in the strict sense.

### 3.5. Evaluation Metrics

Vanilla Precision, Recall and F1. A plausible way to assess anaphora resolution systems is by viewing both mention detection and mention linking tasks as simple classification tasks and measuring the performance using vanilla precision, recall, and F1 scores. A good evaluation metric needs to be both interpretable and discriminative. However, unfortunately, these measures cannot meet any of these criteria [[Moosavi and Strube, 2016]](#ref-Moosavi.2016), especially for the mention linking task as they overlook the structure of these relations (most of which are chain-structured).

MUC and Beyond. Along with MUC-6 (see Section [[3.3]](#ref-Section.3.3)), [[Vilain et al., 1995]](#ref-Vilain.1995) proposed the MUC score. It computes the recall and precision of anaphora/co-reference resolution outputs by considering co-reference chains in a document as a graph. [[Vilain et al., 1995]](#ref-Vilain.1995) first defined two sets: a set of key entities K, in which there are gold standard reference chains (NB: a chain is sometimes named as a class or a cluster), and a set of response entities R, in which there are

^19^<https://dumps.wikimedia.org/>

system generated chained. MUC score computes the recall based on the number of missing links in R compared to K, formally:

$$
\text{Recall} = \frac{\sum_{k_i \in \mathcal{K}} (|k_i| - |p(k_i, \mathcal{R})|)}{\sum_{k_i \in \mathcal{K}} (|k_i| - 1)} \tag{4}
$$

where |*k*~i~| is the number of mentions in the chain *k*~i~ and *p*(*k*~i~,R) is the set of partitions that is constructed by intersecting *k*~i~ with R. The computation of MUC precision is done by switching K and R. However, it has been pointed out that MUC has certain flaws: on the one hand, since MUC is merely building on mismatches of links between the two sets, it is not discriminative enough [[Bagga and Baldwin, 1998]](#ref-Bagga.1998); [[Luo, 2005]](#ref-Luo.2005). For example, it does not tell the difference between an extra link between two singletons or two prominent entities. On the other hand, [[Luo, 2005]](#ref-Luo.2005); [[Kubler and Zhekova, 2011]](#ref-Kubler.2011) argued that MUC prefers singletons. For instance, if we merge all mentions in OntoNotes into singletons, the resulting MUC will be higher than that of the SOTA [[Moosavi and Strube, 2016]](#ref-Moosavi.2016).

Many metrics beyond MUC have been proposed by measuring recall and precision using mentions instead of links. [[Bagga and Baldwin, 1998]](#ref-Bagga.1998) proposed *B*~3~, which considers the fractions of the correctly identified mentions in R:

$$
\text{Recall} = \frac{\sum_{k_i \in \mathcal{K}} \sum_{r_j \in \mathcal{R}} \frac{|k_i \cap r_j|^2}{|k_i|}}{\sum_{k_i \in \mathcal{K}} |k_i|} \tag{5}
$$

The precision is also computed by switching K and R. As pointed by [[Luo, 2005]](#ref-Luo.2005) and [[Luo and Pradhan, 2016]](#ref-Luo.2016), *B*~3~ still cannot fully properly handle singletons and, additionally, repeated mentions. To solve this, [[Luo, 2005]](#ref-Luo.2005) proposed CEAF to incorporate measures of similarities between entities:

$$
\text{Recall} = \frac{\sum_{k_i \in \mathcal{K}^*} \phi(k_i, g(k_i))}{\sum_{k_i \in \mathcal{K}} \phi(k_i, k_i)} \tag{6}
$$

where K^*^ is the set of key entities that have the optimal mapping with R, which is found by the Kuhn-Munkres algorithm, and ϕ(·) is a similarity measure. Nevertheless, CEAF has two shortcomings: it overlooks all unaligned response entities [[Denis and Baldridge, 2009]](#ref-Denis.2009) and weights entities equally [[Stoyanov et al., 2009]](#ref-Stoyanov.2009).

In addition to above mentioned based metrics, to handle singletons, [[Recasens and Hovy, 2011]](#ref-Recasens.2011) proposed BLANC to also consider non-coreference/non-anaphoric links. It measures the fiction of both correctly identified co-reference links and non-coreference entities, and averages them to obtain the final score.

[[Moosavi and Strube, 2016]](#ref-Moosavi.2016) conducted controlled experiments and proved that all the aforementioned computations of precision and recall are neither interpretable nor reliable as they suffer from the so-called *mention identification effect*. They proposed the LEA metric, which was claimed to be able to solve the above issues from two perspectives: (1) it considers both links and mentions; (2) it weights entities with respect to their importance.

### 3.6. Annotation Tools

Text Editors. In the early years, anaphora/co-reference were annotated using text editors or manipulation tools. For example, MUC-6 and ACE were annotated using plain text editors while GNOME was annotated using the XML manipulation tool developed by the University of Edinburgh^[[20]](#ref-20)^.

Co-reference Annotation Tools. Later, linguists and computer scientists developed software that enables multi-layer annotation. The software that is designed for annotating co-reference or allows the annotations of relations between phrases can be used for anaphora/co-reference annotation tasks. For example, ARRAU and PCC used MMAX2, which is a free, extensible, general-purpose, and desktop-based annotation tool. It allows users to annotate relations using fields in a form, and the form is customizable. The NP4E project used PALinkA and ECB+ used CAT [[Bartalesi Lenzi et al., 2012]](#ref-Bartalesi.2012). Both of them were designed for the event and reference annotation. More recently, co-reference annotation tools that provide better visualization, allow drag-and-drop annotation, and offer post-annotation analysis have been built. Typical examples include CorefAnnotator [[Reiter, 2018]](#ref-Reiter.2018), which is open-sourced and desktop-based, SCAR [[Oberle, 2018]](#ref-Oberle.2018), which is open-sourced and web-based, and LightTag, which is not fully free but provides good online teamwork services.

^20^<http://www.ltg.ed.ac.uk/software/>

Annotation Tools with Advanced Functionalities. Some annotation tools provide extra services that help to make sure the annotation procedure is fast and reliable. We classify these services into three categories: (1) External Knowledge: BRAT [[Stenetorp et al., 2012]](#ref-Stenetorp.2012) and INCEpTION [[Klie et al., 2018]](#ref-Klie.2018) integrate external knowledge bases, e.g., Freebase and Wikidata (see Section [[3.4]](#ref-Section.3.4)). Once an annotator identifies an entity, these tools would search the linked base and return related entry; (2) Pre-trained Models: Tools such as TagEditor, Togtag, INCEpTION, and MyMiner [[Salgado et al., 2012]](#ref-Salgado.2012) can call embedded pre-trained entity recognition models so that they can suggest positions of possible name entities during annotation, in which MyMiner was designed specifically for the medical domain (see [[Neves and Seva, 2021]](#ref-Neves.2021) for an overview of annotation tools for medical NLP). Additionally, beyond name entities, TagEditor and INCEpTION can also suggest potential reference chains based on their integrated pre-trained co-reference resolvers, enabling active learning for anaphora/co-reference resolution; (3) Cross-document Annotation: using CROMER [[Girardi et al., 2014]](#ref-Girardi.2014) and CoRefi [[Bornstein et al., 2020]](#ref-Bornstein.2020), annotators can tag, link, or update entities across multiple documents. This is done by allowing annotators to cluster documents based on topics and annotate documents in a cluster together.

### 3.7. Methods
### 3.7.1. Rule-based Methods
### A. Linguistically-inspired Approaches

Like many other tasks in NLP, early works on anaphora resolution built on rules that are rooted cognitively and linguistically. Here, the term "early" represents the age when systematic evaluations of anaphora resolution, e.g., MUC, had not been introduced. The very first algorithm is the naive algorithm proposed by [[Hobbs, 1978]](#ref-Hobbs.1978). It first does a breadth-first search from the parse tree of the sentence to search for identifying mentions and links mentions based on constraints introduced in Section [[3.1.1]](#ref-Section.3.1.1).

Later on, a series of anaphora resolution systems were proposed together with computational investigations of the effect of salience (see Section [[3.1.3]](#ref-Section.3.1.3)). Based on a set of factors that proved to influence salience, [[Sidner, 1979]](#ref-Sidner.1979) introduced rules that are used to compute the expected focus of discourse and rules that are used to interpret anaphora. As a matter of fact, this work was built on the "centering view" rooted from [[Grosz, 1977]](#ref-Grosz.1977), which suggests that, during anaphora resolution, the searching of antecedents should be restricted to the set of centered entities. It could be seen as a prototype of the idea of "center of salience" of the centering theory (see Section [[3.1.2]](#ref-Section.3.1.2)), but the rules proposed by [[Sidner, 1979]](#ref-Sidner.1979) are extremely complex.

Starting from [[Sidner, 1979]](#ref-Sidner.1979), [[Carter, 1987]](#ref-Carter.1987) focused on the rules about salience and developed a system coined Shallow Processing Anaphor Resolver (SPAR). SPAR maintains linguistically-inspired rules as domain knowledge and does commonsense inference over them. As pointed out by [[Carter, 1987]](#ref-Carter.1987), since maintaining domain knowledge and reasoning rules is expensive, SPAR made them as simple as possible. That is why it was called "shallow processing". Carter assessed SPAR on a set of 322 test samples and found that SPAR could successfully resolve 93% pronominal anaphors and 87% non-pronominal anaphora. [[Hobbs et al., 1988]](#ref-Hobbs.1988) formalized commonsense inference in anaphora resolution as abduction and introduced TACITUS. To do abduction, in TACITUS, knowledge (i.e., rules) is maintained in formal logic (first-order predicate logic in this case). Focusing on salience, [[Lappin and Leass, 1994b]](#ref-Lappin.1994b) proposed the Resolution of Anaphora Procedure (RAP) algorithm. After selecting a set of candidate antecedents based on semantic and syntactic constraints, RAP contains a rule-based procedure for assigning values to several salience parameters, which are then used for resolute anaphors. An assessment on 360 hand-crafted texts containing pronouns showed RAP defeated the naive algorithm by 2%.

Also starting from [[Sidner, 1979]](#ref-Sidner.1979), there were subsequent works that extended the idea of "focus" on the basis of the introduction of the concept of "centering". [[Brennan et al., 1987]](#ref-Brennan.1987) introduced the BFP algorithm for anaphora resolution, which roughly has three stages: (1) construct a set of candidate antecedents with accordance to the rules of the semantic constraint; (2) filter and classify the candidates based on which action a candidate belongs to in centering theory (see Section [[3.1.2]](#ref-Section.3.1.2)); and (3) select the best candidate in according to a pre-defined preference over the actions. One limitation of the BFP algorithm is that its final choice is merely based on a linear preference order. To optimize this selection process, [[Beaver, 2004]](#ref-Beaver.2004) marries BFP with the optimality theory. Another limitation is that, by only considering the center theory, BFP overlooked a key pattern of how human resolute pronouns, namely, incremental resolution [[Kehler, 1997]](#ref-Kehler.1997). In response to this problem, [[Tetreault, 2001]](#ref-Tetreault.2001) proposed the Left-to-Right Centering (LRC) algorithm, which is an incremental resolution algorithm that adheres to centering constraints. An evaluation on the New York Time corpus [[Ge et al., 1998]](#ref-Ge.1998) suggests that LRC outperformed both BFP and the naive algorithm.

### B. Knowledge-poor Approaches

After the introduction of the MUC-6 shared task, anaphora resolution systems are able to be evaluated on a large scale. However, the trade-off is that the anaphora resolution systems can no longer access inputs that are annotated with gold-standard semantic and syntactic knowledge. Building on this setting, "knowledge-poor" approaches were proposed and most systems of this kind prefer rules that have high precision but do not rely on knowledge. The most influential work is CogNIAC [[Baldwin, 1997]](#ref-Baldwin.1997), which is a heuristic precision-first anaphora resolver that relies on rules that are almost always true. For example, CogNIAC contains a rule saying *if there is just one possible antecedent in entire the prior discourse, then that entity is the antecedent*. Its rules were selected based on the precision tested on a set of test sentences. It is worth noting that rules in CogNIAC are still used in many SOTA practical anaphora resolution systems (e.g., the Stanford Deterministic Coreference Resolver [[Lee et al., 2013]](#ref-Lee.2013)).

### C. Approaches with Approximate Knowledge

As pointed out by [[Poesio et al., 2023]](#ref-Poesio.2023), this encourages two major changes in anaphora resolution: one this that instead of relying on perfect knowledge and doing reasoning on it, anaphora resolution systems started to syntactic parsers and approximate knowledge like WordNet. The other is that the focus of anaphora resolution models moved from being aware of only pronouns to all kinds of nominal phrases (that function as referring).

[[Kameyama, 1997]](#ref-Kameyama.1997) proposed to resolve anaphors that are proper names, descriptions, and pronouns. It relies on syntactic and semantic constraints, but the related information came from a syntactic parser and morphological filter based on person, number, and gender features. Later on, approaches that marry rules with WordNet were introduced [[Harabagiu and Maiorano, 1999]](#ref-Harabagiu.1999); [[Liang and Wu, 2003]](#ref-Liang.2003). They made use of heuristic rules (as in CogNIAC), some of which consider lexical information from WordNet.

The most famous rule-based anaphora resolution system is the one proposed by [[Haghighi and Klein, 2009]](#ref-Haghighi.2009), which is still frequently used as a strong baseline in today's research on anaphora resolution. In addition to aforesaid syntactic and semantic constraints, [[Haghighi and Klein, 2009]](#ref-Haghighi.2009) makes full use of the parse trees. For example, it contains rules that rely on the distance between mentions, which is obtained from computing the shortest path between two mentions in the parse tree. It also uses Wikipedia as a resource for acquiring semantic knowledge of each entity.

One limitation of heuristic-based systems is that lower precision features often overwhelm higher precision features. In response to this, more recently rule-based systems [[Raghunathan et al., 2010]](#ref-Raghunathan.2010); [[Lee et al., 2013]](#ref-Lee.2013) categorized rules into sieves and made decisions with an ordered set of rules. These works are often called multi-sieve approaches.

### 3.7.2. Statistical-based Methods
The introduction of large-scale benchmarks also encourages the trend of using machine learning techniques in anaphora resolution. Basically, these learning-based models treat anaphora resolution as a series of classification problems. We categorize them on the basis of how they define the classification task.

### A. Mention-pair Models

Mention-pair models train a classifier to determine whether two mentions co-refer or not. It was first introduced by [[Aone and Bennett]](#ref-Aone.Bennett) and then perfected by [[Soon et al., 2001]](#ref-Soon.2001). To build a mention-pair model, there are five steps:

- 1. Identifying Mentions: As a practical anaphora resolution model, the first step of this framework is to identify mentions. [[Soon et al., 2001]](#ref-Soon.2001) break down the mention identification into two stages: they first used three statistical sequence taggers (which is a Hidden Markov Model [[Church, 1989]](#ref-Church.1989)) to do part-of-speech tagging, noun phrase identification, and name entity recognition, respectively. The outputs of them are noun phrases as well as name entities. Then, they designed rules to recognize nested noun phrases based on the identified noun phrases. For each discourse, the resulting set of mentions is the union of noun phrases, name entities, and nested noun phrases. In later works, this module was replaced by more advanced sequence taggers, e.g., conditional random field. See [[Lata et al., 2022]](#ref-Lata.2022) for a survey.
- 2. Feature Engineering: Akin to many statistical models, feature engineering is always needed. [[Soon et al., 2001]](#ref-Soon.2001) made use of not only syntactic and semantic features as usual but also lexical features with the help of WordNet. In addition to [[Soon et al., 2001]](#ref-Soon.2001), many works used knowledge bases for feature engineering (e.g., [[Vieira and Poesio, 2000]](#ref-Vieira.2000); [[Ponzetto and Strube, 2006]](#ref-Ponzetto.2006)). In 2008, [[Bengtson and Roth, 2008]](#ref-Bengtson.2008) found that a simple model with good feature engineering can defect the SOTA model at that moment.
- 3. Generating Training Examples: They used a heuristic-based method to generate training pairs (i.e., a pair of positive and negative examples). More specifically, a positive instance consists of an anaphor *A*^1^ and its

closest preceding antecedent *A*^2^ while a negative instance consists of the same anaphor *A*^1^ and the mention that intervenes *A*^1^ and *A*^2^. There has been a number of modifications to this strategy. For example, [[Ng and Cardie, 2002b]](#ref-Ng.2002b) forced that *A*^1^ can only be a non-pronominal once *A*^2^ is also a non-pronominal. [[Harabagiu et al., 2001]](#ref-Harabagiu.2001); [[Ng and Cardie, 2002a]](#ref-Ng.2002a); [[Strube et al., 2002]](#ref-Strube.2002); [[Yang et al., 2003]](#ref-Yang.2003) further enhanced this process by applying rule-based or learning-based filters.

- 4. Building a Classifier: In this step, statistical machine learning techniques have been used. These include decision trees [[Soon et al., 2001]](#ref-Soon.2001); [[McCarthy and Lehnert, 1995]](#ref-McCarthy.1995), random forests [[Lee et al., 2017a]](#ref-Lee.2017a), Max Entropy classifier [[Berger et al., 1996]](#ref-Berger.1996); [[Ge et al., 1998]](#ref-Ge.1998), and memory-based learning [[Daelemans et al., 2004]](#ref-Daelemans.2004).
- 5. Generating Co-reference Chains: The last step is to partition these anaphora into co-reference chains. Normally, clustering techniques are used in this step. These include closest-first clustering [[Soon et al., 2001]](#ref-Soon.2001), bestfirst clustering [[Ng and Cardie, 2002b]](#ref-Ng.2002b), correlational clustering [[McCallum and Wellner, 2004]](#ref-McCallum.2004), and graph partitioning algorithms [[McCallum and Wellner, 2003]](#ref-McCallum.2003); [[Nicolae and Nicolae, 2006]](#ref-Nicolae.2006).

### B. Entity-Mention Models

As a matter of fact, the task mention-pair anaphora resolution is counter-intuitive from the perspective of linguists and cognitive scientists. Additionally, [[Poesio et al., 2023]](#ref-Poesio.2023) pointed out that mention-pair models also overlook features of entities [[Ng, 2010]](#ref-Ng.2010). In response to this, entity-mention models were proposed. They directly link mentions to entities by clustering. Specifically, [[Cardie and Wagstaff, 1999]](#ref-Cardie.1999) trained a model to classify whether a mention belongs to a partially constructed cluster. However, according to the evaluation by [[Luo, 2005]](#ref-Luo.2005), the performance of the models of this kind is not comparable to mention-pair models.

### C. Mention-Ranking Models

Another problem of mention-pair models is that they only do binary classification without comparing different potential antecedents. To remedy this, [[Denis and Baldridge, 2008]](#ref-Denis.2008) proposed an entity-ranking model, replacing the binary classification loss with a ranking loss. [[Rahman and Ng, 2011]](#ref-Rahman.2011) combined entity-ranking strategy with the entity-mention model, yielding SOTA performance at that moment.

### 3.7.3. Neural Anaphora Resolution
### A. Conventional Deep Learning Models

[[Wiseman et al., 2015]](#ref-Wiseman.2015) was the first to use deep neural networks in anaphora resolution. It is a non-linear mentionranking model. Instead of conjunction features (as in statistical models), the model of [[Wiseman et al., 2015]](#ref-Wiseman.2015) uses a neural network to learn feature representations as an extension to the mention-ranking model. They defined two feature vectors, each of which is obtained from pre-training the model on any of the sub-tasks of anaphora resolution, namely, mention identification and mention linking. The final decision is made through a non-linear classification, based on these features. Both [[Wiseman et al., 2016]](#ref-Wiseman.2016) and [[Clark and Manning, 2016b]](#ref-Clark.2016b) augmented the work of [[Wiseman et al., 2015]](#ref-Wiseman.2015) by inducing global features, but they followed different schemes. [[Wiseman et al., 2016]](#ref-Wiseman.2016) ran a recurrent neural network (RNN) to encode the representation of each sequence of mentions corresponding to an entity (i.e., a cluster) in the history. Whereas, [[Clark and Manning, 2016b]](#ref-Clark.2016b) first used a feed-forward neural network to encode each mention-pair of an entity and computed the entity representation by pooling over all mention-pairs. Later on, [[Clark and Manning, 2016a]](#ref-Clark.2016a) extended their previous work [[Clark and Manning, 2015]](#ref-Clark.2015), which built up co-reference chains with agglomerative clustering. Each mention starts in its own cluster and then pairs of clusters are merged using imitation learning (a type of reinforcement learning technique) by assuming merging clusters are actions. [[Clark and Manning, 2016a]](#ref-Clark.2016a) replaced imitation learning with deep reinforcement learning. [[Liu et al., 2023b]](#ref-Liu.2023b) proposed a multitask learning framework for mention detection and mention linking tasks, because they found that the learning of mention detection task can enhance the learning of dependent information of input tokens, which is complimentary for mention linking detection. Such an approach achieved comparable performance to [[Kocijan et al., 2019]](#ref-Kocijan.2019) with only 0.05% WIKICREM training samples.

### B. End-to-End Models

A significant benefit of employing deep learning models lies in their capacity to operate without the requirement of handcrafted features, thus enabling the creation of end-to-end (End2End) systems. [[Lee et al., 2017b]](#ref-Lee.2017b) proposed the first End2End anaphora resolution system. It needs no human-craft feature or parser and, more importantly, it learns to process mention identification and linking tasks jointly. To this end, the fundamental idea is to first view all spans in the previous discourse as candidate antecedents and do mention ranking (NB: it was called span ranking in [[Lee et al., 2017b]](#ref-Lee.2017b) as the spans it sent for rank are not always mentions). The inputs pass through an RNN and each span is represented by the concatenation of the RNN hidden states of the first token and the last token as well as the weighted sum of all tokens in the span using the attention mechanism [[Bahdanau et al., 2015]](#ref-Bahdanau.2015). The final decision of each pair is made using a feed-forward neural network. One limitation of this method is that since it searches over all possible spans, the search space would be extremely large. To remedy this, candidate spans are pruned by limiting the maximum span width, the number of spans per word, the maximum number of antecedents, and the length of input documents. This End2End model was tested on the OntoNotes dataset and outperformed all previous works.

Akin to mention-pair anaphora resolution systems, End2End anaphora resolution is problematic because it ranks every span-anaphor pair separately. In response to this problem, [[Lee et al., 2018]](#ref-Lee.2018) introduced a higher-order coarse-tofine inference strategy for End2End anaphora resolution models (henceforth, C2F-AR), which, in short, does cluster ranking. It infers in an iterative manner. The antecedent distributions are used to update the span representations before doing inference, enabling later decisions conditioned on previous decisions. C2F-AR uses a coarse factor that can further prune candidate span during this higher-order inference,

More recent works focused on either improving span representations or selecting candidate spans. For example, [[Luo and Glass, 2018]](#ref-Luo.2018) used a two-layer bi-directional RNN and combined the representations of adjacent sentences in order to improve span representation with cross-sentence dependency information. [[Zhang et al., 2018]](#ref-Zhang.2018) proposed to enrich the span representations by training a mention identification model jointly assigning each candidate span an antecedent score. For each pair of spans, [[Kirstain et al., 2021]](#ref-Kirstain.2021) replaced span representations with a combination of lightweight bilinear functions between pairs of endpoint token representations. [[Wu et al., 2020b]](#ref-Wu.2020b) formalized the End2End anaphora resolution as a question-answering task. A query is produced for each entity and predicts the positions of all spans in the co-reference chain.

### C. Knowledge-based Models

Analog to classical rule-based and statistical-based approaches, works on neural anaphora resolution models also seek to integrate knowledge. In terms of the use of open knowledge bases, [[Aralikatte et al., 2019]](#ref-Aralikatte.2019) used world knowledge to compute rewards for reinforcement learning-based anaphora resolution models. More specifically, they submitted the predictions to an OpenIE system and compared the predicted anaphora with the knowledge to compute the reward. [[Zhang et al., 2019]](#ref-Zhang.2019) extracted knowledge triples related to each entity from knowledge graphs and used them to enrich span representations using a knowledge attention module.

It has been pointed out that pre-trained language models are knowledge bases [[Petroni et al., 2019]](#ref-Petroni.2019). Many recent anaphora resolution models have incorporated pre-trained language models, including BERT [[Devlin et al., 2019]](#ref-Devlin.2019), SpanBERT [[Joshi et al., 2020]](#ref-Joshi.2020), and CorefBERT [[Ye et al., 2020]](#ref-Ye.2020).

There has been a line of work focusing on addressing mention linking in WSC-like corpora (see Section [[3.3]](#ref-Section.3.3)). As aforementioned, resolving these "hard" cases needs reasoning with world knowledge. Works of this line incorporate either external knowledge bases [[Emami et al., 2018]](#ref-Emami.2018) or pre-trained language models [[Kocijan et al., 2019]](#ref-Kocijan.2019); [[Attree, 2019]](#ref-Attree.2019).

### 3.7.4. Anaphoric Zero Pronoun Resolution
As mentioned in Section [[3.1.2]](#ref-Section.3.1.2), "cool" languages (e.g., Chinese, Japanese, Korean, and Arabic) contain anaphoric zero pronouns (AZPs), and many works have focused on resolving AZPs. As with other anaphora resolution tasks, early works on AZP resolution (AZPR) used rule-based approaches and statistical approaches. Theoretically, these works are built on the fact that speakers process zero pronouns (ZPs) in the same way as pronouns [[Yang et al., 1999]](#ref-Yang.1999). Early on, most of the works are for Japanese because of the NAIST corpus [[Iida et al., 2007b]](#ref-Iida.2007b), in which AZPs are annotated. [[Kameyama, 1985]](#ref-Kameyama.1985); [[Okumura and Tamura, 1996]](#ref-Okumura.1996) used center theory-based approaches for AZPR in Japanese. Statistical-based approaches were proposed with a focus on exploring useful features, including syntactic pattern features [[Iida et al., 2007a]](#ref-Iida.2007a), heuristic rules [[Isozaki and Hirao, 2003]](#ref-Isozaki.2003), and features that had been considered in anaphora resolution systems [[Nakaiwa et al., 1995]](#ref-Nakaiwa.1995); [[Nakaiwa and Shirai, 1996]](#ref-Nakaiwa.1996); [[Seki et al., 2001]](#ref-Seki.2001), [[2002]](#ref-Seki.2002); [[Sasano et al., 2008]](#ref-Sasano.2008); [[Sasano and Kurohashi, 2011]](#ref-Sasano.2011). Meanwhile, there were also a number of Korean AZPR systems building on the Korean portion of Penn Treebank [[Byron et al., 2006]](#ref-Byron.2006); [[Han, 2006]](#ref-Han.2006).

Later on, the development of systems for Chinese [[Zhao and Ng, 2007]](#ref-Zhao.2007); [[Kong and Zhou, 2010]](#ref-Kong.2010); [[Chen and Ng, 2013]](#ref-Chen.2013), [[2014]](#ref-Chen.2014), [[2015]](#ref-Chen.2015) and Arabic AZPs became active after the introduction of OntoNotes [[Aloraini and Poesio, 2020]](#ref-Aloraini.2020).

From [[Chen and Ng, 2016]](#ref-Chen.2016), AZPR systems also went into the age of deep learning. Most of the works were for Chinese AZPR, including approaches that use deep feedforward neural networks [[Chen and Ng, 2016]](#ref-Chen.2016), RNNs [[Yin et al., 2017a]](#ref-Yin.2017a), [[2019]](#ref-Yin.2019), attention network [[Yin et al., 2018a]](#ref-Yin.2018a), memory network [[Yin et al., 2017b]](#ref-Yin.2017b), deep reinforcement learning [[Yin et al., 2018b]](#ref-Yin.2018b) and BERT [[Song et al., 2020]](#ref-Song.2020).

The training of AZPR systems shares the problem of lacking annotated training data. For example, the AZPR largest corpus, i.e., the Chinese portion of OntoNotes, contains only 12,111 AZPs. To incorporate more data into training, there have been three paradigms: (1) Joint modeling: [[Chen et al., 2021]](#ref-Chen.2021) and [[Aloraini et al., 2022]](#ref-Aloraini.2022) proposed to train a model that resolves either AZPs and non-zero pronouns jointly; (2) Multi-linguality: [[Iida and Poesio, 2011]](#ref-Iida.2011) and [[Aloraini and Poesio, 2020]](#ref-Aloraini.2020) trained multi-lingual AZPR systems which were trained on AZPR data in multiple languages; (3) Data augmentation: [[Liu et al., 2017a]](#ref-Liu.2017a) made use of large-scale reading comprehension dataset in Chinese to generate pseudo training data for Chinese AZPR. [[Aloraini and Poesio, 2021]](#ref-Aloraini.2021) augmented Arabic AZPR data by a number of augmentation strategies, e.g., back translation, masking candidate mentions, etc.

### 3.8. Downstream Applications
### 3.8.1. Machine Translation
[[Stojanovski and Fraser, 2018]](#ref-Stojanovski.2018) provided the following example to illustrate how oracle anaphora singles can help machine translation systems.

- (13) a. Let me summarize the novel for you.
- b. It presents a problem.
- c. er!@#$XPRONOUN It presents a problem.
- d. Er prasentiert ein Problem.

Given the context (a) and the course sentence (b), based on the oracle anaphora information, [[Stojanovski and Fraser, 2018]](#ref-Stojanovski.2018) pre-pend the input sentence of machine translation with pronoun translation as shown in (c) and ask the system to translation with a target (d) in German. In this case, the pronoun "it" which refers to "novel" (in German "Roman") is translated to "er" (the German masculine pronoun agreeing with "Roman"). Without this information, they argued that machine translation will be hard to produce "er". The experiment on a number of Neural machine translation models suggested that would improve the BLEU scores by 4-5 points. This argumentation was strengthened by the experiments conducted by [[Saunders et al., 2020]](#ref-Saunders.2020), who concluded that NMT does not translate gender co-reference. Despite these theoretical studies, many works [[Le Nagard and Koehn, 2010]](#ref-Le.2010); [[Hardmeier and Federico, 2010]](#ref-Hardmeier.2010); [[Guillou, 2012]](#ref-Guillou.2012) focused on improving machine translation with anaphora resolution outputs. The solution is often using anaphora resolution outcomes to obtain features of each pronoun (including, gender, number, and animacy) in order to enhance the pronoun translation performance. Beyond these works, [[Miculicich and Popescu-Belis, 2017]](#ref-Miculicich.2017) proposed to use clustering scores which are used for generating co-reference chains in anaphora resolution (see Section [[3.7.2]](#ref-Section.3.7.2)) as features for re-ranking machine translation results.

There has been a long tradition of studying the impact of AZPs on machine translation systems, especially when translating from a pro-drop language to a non-pro-drop language. For example, the Japanese-English machine translation in the 1990s had already been deployed an AZPR systems [[Nakaiwa and Ikehara, 1992]](#ref-Nakaiwa.1992). Later systems followed a slightly different strategy. Instead of doing a full anaphora resolution, these systems only detect AZPs in the source language and directly translate them into the target language without further resolute them [[Tan et al., 2019]](#ref-Tan.2019); [[Wang et al., 2019b]](#ref-Wang.2019b).

### 3.8.2. Summarization
There are two major uses of anaphora resolution in text summarization [[Steinberger et al., 2007]](#ref-Steinberger.2007). One is to help with finding the important terms while the other is to help with evaluating the coherence of the summarization. Many works have demonstrated that incorporating the information of co-reference chains contributes to both the faithfulness and the coverage of summarization systems [[Bergler et al., 2003]](#ref-Bergler.2003); [[Witte and Bergler, 2003]](#ref-Witte.2003); [[Sonawane and Kulkarni, 2016]](#ref-Sonawane.2016); [[Liu et al., 2021b]](#ref-Liu.2021b). Nevertheless, it is also worth noting that there are also some studies that showed that anaphora resolution had negative effects [[Orasan, 2007]](#ref-Orasan.2007); [[Mitkov et al., 2007]](#ref-Mitkov.2007). One possible explanation is that the effect highly depends on the task the summarization system is addressing and the performance of the anaphora resolution systems (NB: these studies have been 15 years old).

### 3.8.3. Textual Entailment
For textual entailment, to understand the impact of anaphora resolution, [[Mirkin et al., 2010]](#ref-Mirkin.2010) manually analyzed 120 samples in the RTE-5 development set [[Bentivogli et al., 2009]](#ref-Bentivogli.2009). They found that for 44% samples anaphora relations are mandatory for inference and for 28% sample anaphora optionally support the inference. Based on this fact, many systems that got involved in the RTE challenge made use of anaphora resolution. Nevertheless, since anaphora resolution systems at that moment were not strong enough, errors they made would propagate to downstream textual entailment systems [[Adams et al., 2007]](#ref-Adams.2007); [[Agichtein et al., 2008]](#ref-Agichtein.2008). As a consequence, the contribution of anaphora resolution was negative or not significant [[Bar-Haim et al., 2008]](#ref-Bar-Haim.2008); [[Chambers et al., 2007]](#ref-Chambers.2007).

### 3.8.4. Sentiment Computing
For sentiment computing, [[Sukthanker et al., 2020]](#ref-Sukthanker.2020) listed two situations when anaphora resolution can help. One is when doing sentiment analysis on online reviews, a characteristic of them is that online reviews often focus on a particular entity and, therefore, the mentions often in less elaborated forms (e.g., pronouns). Resolution of these mentions can chain them into a global entity and, hence, improve the sentiment analysis performance. The other is that anaphora resolution can also be used in fine-grained aspect-based sentiment analysis. Anaphora resolution plays a pivotal role in this task by facilitating the clustering of entities into distinct aspects. This, in turn, aids in the extraction of sentiments and opinions associated with each aspect.

The contribution of anaphora resolution in sentiment computing tasks can be summarized as follows: it enables discourse-level sentiment analysis by linking mentions from different sentences. Many efforts have been carried out to demonstrate such an ability for anaphora resolution. [[Nicolov et al., 2008]](#ref-Nicolov.2008) conducted systematic experiments to understand the impacts of anaphora resolution on sentiment analysis. Specifically, they tried to incorporate anaphora information into a number of sentiment analysis models and assessed them on varieties of datasets. They concluded that, on average, anaphora resolution can boost sentiment analysis performance by 10%. Based on this finding, sentiment analysis systems that are assembled with anaphora resolution have been proposed [[Jakob and Gurevych, 2010]](#ref-Jakob.2010); [[Ding and Liu, 2010]](#ref-Ding.2010); [[Le et al., 2016]](#ref-Le.2016).

### 3.9. Summary
Anaphora resolution has been explored extensively by theoretical linguists, psycholinguists as well as computational linguistics. It is the manifest of structural semantics because the meaning of an anaphor elucidates the syntactic relationship between the anaphor and its antecedent. Early anaphora resolution models were inspired by theories and findings in linguistics, such as the theory of syntactic and semantic constraints from theoretical linguistics and the findings about factors that influence the choice of referential form from psycholinguists. Later on, by marrying these theories with computational models, linguists also gained insights regarding the comprehension and production of anaphora from anaphora resolution systems. For instance, we could understand better how each salience factor contributes to the use of anaphora through the importance analysis of a computational model that considers the factor. Most recently, though most computational works focus on building End2End anaphora resolution systems based on deep learning techniques, linguistic theories about anaphora are still proven to play vital roles [[Chai and Strube, 2022]](#ref-Chai.2022). Dataset is core for either practical or theoretical anaphora resolution research. Though many annotation schemes and datasets have been introduced, we found that they share two limitations: one is that due to the fact that anaphora is a complex concept, annotations of anaphora resolution datasets are always imperfect [[Deemter and Kibble, 2000]](#ref-Deemter.2000). The other is the lack of wide-coverage datasets that covers all kinds of anaphora. Finally, we found that anaphora resolution is useful in many downstream tasks, including major tasks of both natural language understanding and natural language generation. It is always utilized as a producer of additional features for downstream tasks. Different from other tasks in this survey, we rarely see how anaphora resolution techniques help boost the explainability of downstream models, apart from the work of [[Saunders et al., 2020]](#ref-Saunders.2020). We also have not observed that anaphora resolution techniques are used for constructing datasets for downstream tasks.

### 3.9.1. Technical Trends
As seen in Table [[8]](#ref-Table.8), there are two clear technical trends. One is that the research interest in the realm of anaphora resolution has shifted from machine learning-based or rule-based anaphora resolution to neural approaches, especially the End2End neural anaphora resolution, which does mention identification and linking simultaneously. Another one

| Task | Reference | Feature | Framework | Dataset | Score | Metric |
|:------------|:-------------------------------------------------------------------|:---------------------------------------------|:-----------------------------------------------|:-------------------------------------------------------------------|:---------------------------|:------------------|
| | [[Lappin and Leass, 1994b]](#ref-Lappin.1994b)<br>[[Brennan et al., 1987]](#ref-Brennan.1987)<br>[[Carter, 1987]](#ref-Carter.1987) | Semantic constraints<br>Salience<br>Salience | Centering theory<br>Logic rules<br>Logic rules | self-collected dataset<br>self-collected dataset<br>New York Times | 93.00%<br>85.00%<br>59.40% | Acc<br>Acc<br>Acc |
| Rule-based | [[Tetreault, 2001]](#ref-Tetreault.2001)<br>[[Baldwin, 1997]](#ref-Baldwin.1997) | Semantic constraints<br>Syntactic, Semantic, | Centering theory<br>Logic rules | self-collected dataset<br>New York Times | 80.40%<br>77.90% | Acc<br>Acc |
| | [[Liang and Wu, 2003]](#ref-Liang.2003) | Discourse<br>WordNet | Logic rules | Brown Corpus | 77.00% | Acc |
| | [[Haghighi and Klein, 2009]](#ref-Haghighi.2009) | Syntactic, Semantic | Logic rules | ACE | 79.60% | MUC-F |
| | [[Soon et al., 2001]](#ref-Soon.2001) | Syntactic, Semantic,<br>WordNet | Mention-pair | MUC-6 | 62.60% | MUC-F |
| | [[Cardie and Wagstaff, 1999]](#ref-Cardie.1999) | Lexical, Syntactic,<br>Semantic | Entity-Mention | MUC-6 | 64.90% | MUC-F |
| Stat.-based | [[Denis and Baldridge, 2008]](#ref-Denis.2008) | Linguistic & Positional | Mention-ranking | ACE | 67.00% | CEAF-F |
| | [[Rahman and Ng, 2011]](#ref-Rahman.2011) | Lexical, Syntactic,<br>Semantic | Mention-ranking | ACE | 60.80% | CEAF-F |
| | [[Wiseman et al., 2015]](#ref-Wiseman.2015) | Syntactic, Semantic | Mention-rank., DNN | OntoNotes | 82.86% | Acc |
| | [[Wiseman et al., 2016]](#ref-Wiseman.2016) | Syntactic, Semantic,<br>Global Feature | Mention-rank., RNN | OntoNotes | 64.21% | CoNLL-F |
| | [[Clark and Manning, 2016a]](#ref-Clark.2016a) | Syntactic, Semantic | DRL | OntoNotes | 65.73% | CoNLL-F |
| | [[Clark and Manning, 2016b]](#ref-Clark.2016b) | Syntactic, Semantic,<br>Global Feature | Mention-ranking, DNN | OntoNotes | 65.52% | CoNLL-F |
| DL-based | [[Lee et al., 2017b]](#ref-Lee.2017b) | Word & Cha. Emb. | End2End, LSTM, DNN | OntoNotes | 68.80% | CoNLL-F |
| | [[Lee et al., 2018]](#ref-Lee.2018) | ELMo | End2End, LSTM, DNN | OntoNotes | 73.00% | CoNLL-F |
| | [[Zhang et al., 2018]](#ref-Zhang.2018) | Glove & Cha. Emb. | BiLSTM, Joint Learning | OntoNotes | 69.20% | CoNLL-F |
| | [[Joshi et al., 2019]](#ref-Joshi.2019) | BERT | [[Lee et al., 2018]](#ref-Lee.2018) | OntoNotes | 76.90% | CoNLL-F |
| | [[Joshi et al., 2020]](#ref-Joshi.2020) | SpanBERT | [[Lee et al., 2018]](#ref-Lee.2018) | OntoNotes | 79.60% | CoNLL-F |
| | [[Wu et al., 2020b]](#ref-Wu.2020b) | SpanBERT | QA | OntoNotes | 83.10% | CoNLL-F |
| | [[Kocijan et al., 2019]](#ref-Kocijan.2019) | WikiCREM<br>BERT | DNN | DPR | 84.80% | Acc |
| | [[Liu et al., 2023b]](#ref-Liu.2023b) | BERT | Transformer, MTL | DPR | 84.58% | Acc |
| | [[Okumura and Tamura, 1996]](#ref-Okumura.1996) | Salience | Center Theory | self-collected dataset | 78.30% | Acc |
| | [[Sasano et al., 2008]](#ref-Sasano.2008) | Salience | Probalistic | self-collected dataset | 39.10% | F1 |
| | [[Chen and Ng, 2016]](#ref-Chen.2016) | Syntactic, Lexical | DNN | OntoNotes | 52.20% | F1 |
| AZPR | [[Yin et al., 2017a]](#ref-Yin.2017a) | Word2Vec, Global | RNN | OntoNotes | 53.60% | F1 |
| | [[Yin et al., 2018b]](#ref-Yin.2018b) | Word Embedding | DRL | OntoNotes | 57.20% | F1 |
| | [[Song et al., 2020]](#ref-Song.2020) | BERT | DNN, MTL | OntoNotes | 58.49% | F1 |
| | | | | | | | |

**Table 8:** A summary of representative anaphora resolution techniques. Note that [[Rahman and Ng, 2011]](#ref-Rahman.2011) reported that the performance of [[Denis and Baldridge, 2008]](#ref-Denis.2008) was 57.7% CEAF-F and that CoNLL-F is the average of MUC, B3, and CEAF scores. Stat. denotes statistics. DL denotes deep learning. AZPR denotes Anaphoric Zero Pronoun Resolution. Cha. Emb. denotes character embedding. ACE denotes automatic content extraction. MTL denotes multi-task learning. DRL denotes deep reinforcement learning is that, as previously elucidated in Section [[3.7]](#ref-Section.3.7), there exist distinct shortcomings associated with each of the task formulations such as mention pair, entity mention, and mention ranking. Consequently, a recent tendency is to employ higher-order inferences [[Lee et al., 2018]](#ref-Lee.2018) to directly rank clusters or entities, which allows for the incorporation of benefits from all the formulations. To sum up, the SOTA anaphora resolution models are often *End2End cluster ranking models*.

Most recent advances tended to further improve this paradigm from two angles, namely reducing the search space as an End2End anaphora resolution searches across all possible spans in its inputs for antecedents [[Wu et al., 2020b]](#ref-Wu.2020b); and equipping anaphora resolution systems with knowledge (which, recently, often large-scale pre-trained language models) to boost their ability of reasoning [[Joshi et al., 2019]](#ref-Joshi.2019), [[2020]](#ref-Joshi.2020). Furthermore, recent investigations on anaphora resolution have also led to advancements in various deep learning paradigms. Deep reinforcement learning and multi-task learning were employed for obviating the need for language-orientated hyperparameter tuning [[Clark and Manning, 2016a]](#ref-Clark.2016a), investigating the enduring impact of pronoun-candidate antecedent pairs [[Yin et al., 2018b]](#ref-Yin.2018b), and enhancing the dependency learning of mention pairs [[Liu et al., 2023b]](#ref-Liu.2023b).

Meanwhile, there were also certain efforts that concentrated on resolving "hard" cases and multi-linguality in anaphora resolution. As for the former one, people were aware of the models' capacity to resolve ambiguous pronouns and biases (especially, gender bias) learned by anaphora resolution models [[Levesque et al., 2012]](#ref-Levesque.2012); [[Rudinger et al., 2018]](#ref-Rudinger.2018). The SOTA models of this line of work are often assembled with knowledge bases [[Emami et al., 2018]](#ref-Emami.2018) or pre-trained language models [[Kocijan et al., 2019]](#ref-Kocijan.2019). As for the latter one, multi-lingual anaphora resolution systems were developed in order to either, theoretically, unify the theory of reference for different languages [[Nedoluzhko et al., 2022]](#ref-Nedoluzhko.2022), or, practically, enrich the datasets for low-resource anaphora resolution languages or tasks (e.g., AZPR; [[Aloraini and Poesio, 2020]](#ref-Aloraini.2020)).

In addition to these two trends for developing practical anaphora resolution systems, there is also a long tradition of studying how human beings understand and use anaphors with the algorithms introduced in this section from the age of rule-based methods [[Sidner, 1979]](#ref-Sidner.1979); [[Carter, 1987]](#ref-Carter.1987) to the most recent deep learning based methods [[Chai and Strube, 2022]](#ref-Chai.2022); [[Same et al., 2022]](#ref-Same.2022).

| Reference | Downstream Task | Feature | Explain. |
|:------------------------------------------------------------|:------------------------------------------------|:--------|:---------|
| [[Le Nagard and Koehn, 2010]](#ref-Le.2010)<br>[[Hardmeier and Federico, 2010]](#ref-Hardmeier.2010) | Machine Translation<br>Machine Translation | ✓<br>✓ | |
| [[Miculicich and Popescu-Belis, 2017]](#ref-Miculicich.2017) | Machine Translation | ✓ | |
| [[Saunders et al., 2020]](#ref-Saunders.2020)<br>[[Steinberger et al., 2007]](#ref-Steinberger.2007) | Machine Translation<br>Summarization Evaluation | ✓<br>✓ | ✓ |
| [[Bergler et al., 2003]](#ref-Bergler.2003) | Summarization | ✓<br>✓ | |
| [[Liu et al., 2021b]](#ref-Liu.2021b)<br>[[Agichtein et al., 2008]](#ref-Agichtein.2008) | Summarization<br>Textual Entailment | ✓ | |
| [[Jakob and Gurevych, 2010]](#ref-Jakob.2010)<br>[[Ding and Liu, 2010]](#ref-Ding.2010) | Sentiment Computing<br>Sentiment Computing | ✓<br>✓ | |
| | | | |

### 3.9.2. Application Trends
**Table 9:** A summary of the representative applications of anaphora resolution in downstream tasks. ✓ denotes the role of anaphora resolution in a downstream task.

Many demonstrations were carried out approximately 15 years ago to validate the necessity of anaphora resolution for both language generation and understanding downstream tasks [[Steinberger et al., 2007]](#ref-Steinberger.2007); [[Mirkin et al., 2010]](#ref-Mirkin.2010); [[Nicolov et al., 2008]](#ref-Nicolov.2008); [[Li et al., 2021]](#ref-Li.2021); [[He et al., 2022a]](#ref-He.2022a). Nevertheless, practically, at that moment, anaphora resolution often had negative effects [[Bar-Haim et al., 2008]](#ref-Bar-Haim.2008); [[Chambers et al., 2007]](#ref-Chambers.2007); [[Orasan, 2007]](#ref-Orasan.2007); [[Mitkov et al., 2007]](#ref-Mitkov.2007). This is mainly because anaphora resolution systems were not powerful enough and errors they made may propagate to their downstream tasks.

Recently, with significant advancements in the capabilities of anaphora resolution systems, more and more anaphora resolution systems have been used for providing anaphora information for downstream tasks (see Table [[9]](#ref-Table.9)). In short, anaphora resolution helps its downstream applications mainly in two ways. It links noun phrases in different sentences. As a consequence, these applications have better performance in comprehending discourse-level information. On the other hand, linking noun phrases helps downstream applications to do higher-level reasoning, e.g., extracting global entities [[Sukthanker et al., 2020]](#ref-Sukthanker.2020) and recovering the ellipses [[Aralikatte et al., 2021]](#ref-Aralikatte.2021).

Most downstream task models utilize anaphora resolution as an additional feature to improve task performance. However, we did not see how anaphora resolution techniques help to explain how and why anaphora is used in a certain context.

### 3.9.3. Future Works
Developing robust annotation schemes. Current annotation schemes for anaphora practically work fine but are theoretically problematic as there is no unified rule of what is remarkable, and no clear cut between co-reference and anaphora (though there is a clear boundary between them in linguistic theory). Annotation schemes so far are imperfect to improve the practicality so that large anaphora/co-reference resolution datasets (that can be used for training and assessing data-driven anaphora resolution systems) could be constructed. In exchange, the resulting corpora are imperfect in terms of both quality (i.e., some annotated relations might not be anaphoras) and coverage (i.e., some kinds of anaphora are not covered). On a different note, anaphora resolution, which can also be seen as a pragmatics task, disagreement on how an anaphora is interpreted happens across different readers [[Uma et al., 2022]](#ref-Uma.2022). Nonetheless, many datasets resolve disagreements through majority voting, while only a few works explicitly annotated ambiguities, which are the causes of the disagreements (e.g., [[Poesio and Artstein, 2008b]](#ref-Poesio.2008b)). In aggregate, it is plausible to design a scheme (probably by extending MATE) that not only handles disagreements but also balances quality, practicality, and coverage. Furthermore, it is important to empirically investigate how the errors and limitations inherent in the annotation scheme can impact the performance of anaphora resolution systems.

Anaphora resolution evaluation. Analogue to the disagreements in the anaphora annotation, one can expect that, for a single mismatch between an output and a reference answer, it might be an error for some readers but not an error for the rest. For different mismatches, they might have different severity. The impact of severity of errors has been studied for the production of reference (see [[van Miltenburg et al., 2020]](#ref-van.2020); e.g., saying "a woman is a man" is more serious than saying "a red coat is pink"), but it has never been explored in the realm of anaphora resolution. This said, roughly computing the overlaps between model outputs and reference outputs might be problematic. On the one hand, due to discrepancies and varying degrees of errors in anaphora resolution, human evaluation [[Martschat and Strube, 2014]](#ref-Martschat.2014) is necessary to improve the analysis and evaluation of anaphora resolution models, as well as to establish benchmarks for developing more accurate evaluation metrics. On the other hand, when designing new evaluation metrics, disagreements, and error severity should be considered by data-driven methods.

Model development. Regarding future advancements in anaphora resolution models, a significant area of focus should be on computational studies of anaphora resolution tasks that are firmly grounded in theory but have yet to be extensively explored. Examples of such tasks include but are not restricted to (1) bridging, deictic, and plural references, which are crucial aspects of referential language, yet their computational treatment has been limited, possibly due to a shortage of relevant annotated datasets; and (2) disagreement resolution, which involves learning from discrepancies in human interpretations of anaphoric expressions to better capture the pragmatic nuances of such references, and should be incorporated into future models [[Uma et al., 2021]](#ref-Uma.2021); and (3) cross-document anaphora resolution, which is critical for downstream applications such as knowledge graph construction and cross-document information extraction, yet has received insufficient attention in terms of data, methods, and evaluation metrics, particularly in relation to event resolution.

## 4. Named Entity Recognition

Name Entity Recognition (NER) is a critical component of Information Extraction, which involves identifying entity mentions in text, defining their boundaries, and assigning them entity types. The most commonly recognized entity types by NER systems are Location, Person, and Organization, and tokens referring to these entities are classified as entity mentions. In the following example:

(14) Steve Jobs is the founder of Apple.

an NER system would recognize the entities that "Steve Jobs" is Person; "Apple" is Organization. NER systems use pre-defined entity types, which may vary across different implementations. For example, Stanford's widely used NER software [[Finkel et al., 2005]](#ref-Finkel.2005) provides three versions that recognize three classes (Location, Person, Organization), four classes (Location, Person, Organization, Misc), and seven classes (Location, Person, Organization, Money, Percent, Date, Time), respectively. NER is a critical component in the field of NLP [[Jinjie et al., 2022]](#ref-Jinjie.2022); [[Gao et al., 2022]](#ref-Gao.2022); [[He et al., 2021]](#ref-He.2021) and is often combined with other tasks, such as Relation Extraction (RE), to serve as a foundation for various NLP applications. Besides, NER is also used in various data mining tasks to recognize keywords, topics, and attributes [[He et al., 2019a]](#ref-He.2019a); [[Li et al., 2021]](#ref-Li.2021), [[2019]](#ref-Li.2019).

NER can be traced back to the third Message Understanding Conference (MUC-3) [[Chinchor et al., 1993]](#ref-Chinchor.1993). The task for MUC-3 was designed to extract relevant information from the text and convert it into a structured format based on a predefined template, e.g., incident, the targets, perpetrators, date, location, and effects. Early NER systems that participated in MUC-3 primarily relied on rule-based approaches, which involved the manual creation of rules to identify named entities based on their linguistic and contextual features. However, with the dominance of deep learning in the NLP community, most NER tasks are now performed using neural networks. One of the first neural networks for NER was proposed by [[Collobert and Weston, 2008]](#ref-Collobert.2008), which used a single convolutional neural network with manually constructed feature vectors. Later, this approach was replaced with high-dimensional continuous vectors, which were learned from large amounts of unlabeled data in an unsupervised manner [[Collobert et al., 2011]](#ref-Collobert.2011). With stronger models, now, the research in NER has been largely extended to nested NER [[Su et al., 2022]](#ref-Su.2022), few-shot NER [[Huang et al., 2022a]](#ref-Huang.2022a), joint entity and relation extraction (JERE) [[Zhong and Chen, 2021]](#ref-Zhong.2021); [[Mao et al., 2022a]](#ref-Mao.2022a).

Compared to standard NER whose entity relationship is absent, entities in nested NER have a hierarchical or nested structure, where one entity is embedded within another entity. For example, given

### (15) The Ontario Supreme Court said ...

"Ontario" is a state entity that is embedded under the government entity of "Ontario Supreme Court" [[Ringland et al., 2019a]](#ref-Ringland.2019a). Given the very expensive annotation costs, few-shot NER is also a very important research trend. It learns NER with a limited amount of labeled data. JERE tasks are established based on the needs of downstream applications. In many cases, people not only need to know what an entity is but also need to know the relationship between entities. Thus, JERE needs to identify named entities in text as well as extract the relationships that exist between them. In the following example

(16) Greg Christie has been one of the greatest engineers at Apple.

For standard NER, "Greg Christie" should be identified as Person; "Apple" should be identified as Company. However, for JERE, besides the above entity recognition, an additional relationship label, "work at" should also be predicted. Compared to identifying entities that are hierarchically structured within each other in nested NER tasks, the outcomes of JERE deliver another relationship dimension to connect entities. Both tasks are helpful in developing a comprehensive knowledge graph.

Due to the wide range of applications of NER, there have been several surveys conducted on this typical NLP task [[Li et al., 2020a]](#ref-Li.2020a); [[Yadav and Bethard, 2018]](#ref-Yadav.2018). One recent study [[Song et al., 2021]](#ref-Song.2021) focused specifically on NER in the biomedical field, also known as Bio-NER. In this domain, the presence of meaningless characters in biomedical data presents a significant challenge, particularly with regards to inconsistent word distribution. Similarly, [[Liu et al., 2022a]](#ref-Liu.2022a) summarized and discussed the challenges specific to Chinese NER, rather than the more general English NER tasks. Meanwhile, [[Nasar et al., 2021]](#ref-Nasar.2021) explored both NER and RE tasks, as they are closely linked and are typically composed of pipeline tasks. The aforementioned surveys focus on the technical perspective of NER, based on deep learning technology, while this section broadens the horizon of NER from theoretical foundations to applications.

## 4.1. Theoretical Research

### 4.1.1. Prototype Theory

[[Rosch, 1973]](#ref-Rosch.1973) argued that our classification system, which includes the classification of named entities, is based on a central or prototype example. A prototype is a typical example of a category that represents the most common features or characteristics associated with the category. For example, the prototype of "bird" must associate the features, such as wings, feathers, and the ability to fly. Birds such as ostriches or penguins, which do not perfectly possess these characteristics, may be viewed as less typical examples. [[Rosch and Mervis, 1975]](#ref-Rosch.1975) discovered that individuals can identify typical category examples faster and with greater precision than atypical examples. Thus, learning from prototypes can help to quickly grasp the important features of a named entity with a few examples.

### 4.1.2. Graded Membership

[[Rosch et al., 1976]](#ref-Rosch.1976) argued that the classification of categories is frequently determined not by strict boundaries, but by various degrees of membership. We can use this theory for NER because the NER task also categorizes entities by predefined classes. The idea of Graded Membership implies how humans perceive and categorize the world around us. Some categories, e.g., "vegetable", may be viewed as less distinct and vaguer. The theory suggests that the borders between categories may not be well-defined in some cases, leading to ambiguities when attempting to classify certain items, such as tomatoes or mushrooms. The ambiguity can be further compounded by cultural or regional differences in how categories are defined or classified.

### 4.1.3. Conceptual Blending

According to [[Fauconnier and Turner, 2008]](#ref-Fauconnier.2008), the act of blending different elements and their corresponding relationships is an unconscious process that is believed to be ubiquitous in everyday thought and language. This process involves the combination of various mental spaces or cognitive domains that are drawn from different scenarios and experiences. These scenarios may be derived from personal experiences, cultural practices, or societal norms, among others. Concept blending allows us to create a new concept by combining existing ones in novel ways. For example "SpaceX" may be mapped to mental spaces related to "aerospace" and "technology"; "Tesla" may be mapped to mental spaces related to "car" and "clean energy". Conceptual blending provides an explanation for the recognition and comprehension of newly named entities by mapping them onto existing mental spaces or concepts.

### 4.1.4. Grammatical Category
From the aspect of computational linguistics, the core issue of NER is how to define a named entity. [[Marrero et al., 2013]](#ref-Marrero.2013) group the criteria of a named entity as grammatical category, rigid designation, unique identification, and the domain of applications. However, many of the entity definitions in the NER domain are imperfect. From the view of grammatical category, a named entity is traditionally defined as a proper noun or a common name for a proper noun. Previous work has described NER as the recognition of proper nouns in general. However, as pointed out by [[Borrega et al., 2007]](#ref-Borrega.2007), the classic grammatical approach to proper noun analysis is insufficient to deal with the challenges posed by NER applications. For instance, in a toy question-answering task such as

### (17) Do crocodiles live in the sea or on land?

"crocodiles", "sea", and "land" are not proper nouns, while they are commonly recognized as the essential entities for a proper understanding of the question. Consequently, a proper noun is no longer considered a criterion for identifying named entities in current NER research.

### 4.1.5. Rigid Designation
The rigid designation is a concept in the philosophy of language which suggests that certain names or labels are inherently linked to the things they represent, e.g., "Barack Obama" rigidly designates the person who is the 44th President of the US, and it cannot be used to refer to any other person or entity. NER can be viewed as a form of rigid designation as it assigns labels to entities based on their intrinsic identity [[Kripke, 1972]](#ref-Kripke.1972), rather than on their usage in the text. However, [[LaPorte, 2006]](#ref-LaPorte.2006) noted that not all expressions that appear to designate rigidly can be analyzed as directly referring to an object in every possible world. This highlights the difficulty of defining entities with complex concepts in real-world applications. As a result, annotators likely make subjective judgments when labeling complex entities, which may be affected by entity descriptions and annotators' understanding.

### 4.1.6. Unique Identification
From the view of unique identification, the MUC conferences require that NER tasks annotate the "unique identification" of entities for all expressions [[Grishman and Sundheim, 1996]](#ref-Grishman.1996). However, determining what is unique depends on contextual elements, and can be a subjective process. While this "unique identification" is typically considered to be the reference being referred to, the definition itself poses a challenge in terms of defining what is truly unique.

| Tokens: | West | African | Crocodile | are | semiaquatic | reptiles | that | live | in | Africa |
|:--------|:-----|:--------|:----------|:----|:------------|:---------|:-----|:-----|:---|:-------|
| IO | I | I | I | O | I | I | O | O | O | I |
| BIO | B | I | I | O | B | I | O | O | O | B |
| BIOES | B | I | E | O | B | E | O | O | O | S |

**Table 10:** The three common annotation schemes for NER.

### 4.1.7. Domain of Applications
The definition of named entities was frequently grounded in the domain of applications. Entity definitions can be different between different NER tasks. For instance, in drug-drug interaction tasks [[Deng et al., 2020]](#ref-Deng.2020), diseases may not be considered entities, whereas they are entities in adverse drug events [[Demner-Fushman et al., 2019]](#ref-Demner-Fushman.2019). Inconsistent entity definitions create challenges for machine learning. Because inconsistent entity definitions mean that for the same semantic unit, the machine has to summarize different entity representations to distinguish their labels under different tasks. This is also not conducive to training an all-around NER classifier on different application domains.

### 4.2. Annotation Schemes

NER is typically approached as a sequence labeling task, where each token in a sentence is assigned a label. Three common annotation schemes are shown in Table [[10]](#ref-Table.10). The IO scheme is a classification task that distinguishes between two classes, namely "Inner" and "Other", to determine whether a token belongs to an entity or not. On the other hand, the BIO scheme employs three labels, namely "Beginning", "Inner", and "Other", to identify tokens that represent the start of an entity, tokens that belong to an entity, and tokens that do not belong to any entity. The BIOES scheme expands on the BIO scheme by incorporating two additional labels, namely "Single" and "End", to more precisely define the boundaries of entities.

By employing the IO scheme, the binary classification of tokens is simplified, as each token is labeled as either belonging to an entity or not. This straightforward labeling system makes it easier to identify entities in a text, but it fails to specify the position of the entities within the text. In contrast, the BIO scheme provides more precise annotations by identifying the beginning and continuation of an entity in the text. This labeling system allows for more accurate recognition of entities in a text and better classification of individual tokens. The BIOES scheme further extends the BIO scheme by providing more precise boundaries for entities, thereby allowing for better recognition of entity boundaries in a text. The "Single" label is used to denote an entity that consists of a single token, whereas the "End" label is used to indicate the final token of an entity. By incorporating these additional labels, the BIOES scheme provides a more nuanced approach to entity recognition and annotation.

### 4.3. Datasets

| Dataset | Source | # Sample | Reference |
|:--------------|:--------------|:-----------------------|:-----------------------------|
| MUC-6 | Newswire | 318 articles | [[Grishman and Sundheim, 1996]](#ref-Grishman.1996) |
| ACE-05 | Social media | 12,548 sentences | [[Walker et al., 2006]](#ref-Walker.2006) |
| TACRED | Newswire | 106,264 instances | [[Zhang et al., 2017b]](#ref-Zhang.2017b) |
| CoNLL-2003 | Reuters21 | 1,499 articles | [[Sang and De Meulder, 2003]](#ref-Sang.2003) |
| I2B2 | ECI Corpus22 | 1,600 patient records | [[Stubbs and Uzuner, 2015]](#ref-Stubbs.2015) |
| ADE | MEDLINE 23 | 2,972 document | [[Gurulingappa et al., 2012]](#ref-Gurulingappa.2012) |
| DDI | DrugBank24 | 1,025 document | [[Herrero-Zazo et al., 2013]](#ref-Herrero-Zazo.2013) |
| WNUT-17 | Social media | 2,295 documents | [[Derczynski et al., 2017]](#ref-Derczynski.2017) |
| OntoNote 5.0 | Social media | - | [[Weischedel et al., 2013]](#ref-Weischedel.2013) |
| CPR | MEDLINE | - | [[Krallinger et al., 2017]](#ref-Krallinger.2017) |
| MultiNERD | Wikipedia | 10 languages | [[Tedeschi and Navigli, 2022]](#ref-Tedeschi.2022) |
| HIPE-2020 | Newspapers | 17,553 mentions | [[Ehrmann et al., 2022]](#ref-Ehrmann.2022) |
| NNE | Newswire | 49,208 sentences | [[Ringland et al., 2019a]](#ref-Ringland.2019a) |
| GENIA | MEDLINE | 18,546 sentences | [[Kim et al., 2003]](#ref-Kim.2003) |

**Table 11:** NER datasets and statistics.

The surveyed popular NER datasets and their statistics can be viewed in Table [[11]](#ref-Table.11). The first NER-focused dataset was published in the 6th MUC Conference [[Grishman and Sundheim, 1996]](#ref-Grishman.1996). This task consists of three sub-tasks, including entity names, temporal expressions, and number expressions. The defined entities include organizations, persons, and locations; The defined time expressions include dates and times; The defined quantities include monetary values and percentages. More details can be seen in the office website^[[25]](#ref-25)^. The example of this dataset is shown as follows.

```text
text: "Taga Co.",
type: "ORGANIZATION".
```

The MUC conference was replaced by Automatic Content Extraction (ACE) after 1997. ACE05 [[Walker et al., 2006]](#ref-Walker.2006) is another popular NER dataset published at ACE Conference. ACE05 is a multi-lingual dataset, which contains English, Arabic, and Chinese data. The corpus consists of data of various types annotated for entities, relations, and events. Its data source includes broadcast conversation, broadcast news, newsgroups, telephone conversations, and weblogs. More details can be seen on the office website^[[26]](#ref-26)^. The example of this dataset is shown as follows.

```text
entity id: "NN ENG 20030630 085848.18-E1",
type: "GPE",
subtype: "State-or-Province",
class: "SPC",
start: "82",
end: "91",
name: "california".
```

After MUC, the Text Analysis Conference (TAC) published the Knowledge Base Population challenge. In this challenge, the Stanford NLP Group developed TAC Relation Extraction Dataset (TACRED) [[Zhang et al., 2017b]](#ref-Zhang.2017b), which contains 106,264 instances with annotated entities, relations and some other NLP tasks. More details can be seen on the office website^[[27]](#ref-27)^. The example of this dataset is shown as follows.

```text
id: "e7798fb926b9403cfcd2",
docid: "APW ENG 20101103.0539",
relation: "per:title",
token: "['At', 'the', 'same', 'time', ',', 'Chief', ...]",
subj start: "8",
subj end: "9",
obj start: "12",
obj end: "12",
subj type: "PERSON",
obj type: "TITLE",
stanford pos: "['IN', 'DT', 'JJ', 'NN', ',', 'NNP', 'NNP', ...]",
stanford ner: "['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', ...]"
stanford head: "[4, 4, 4, 12, 12, 10, 10, 10, 10, 12, ...]",
stanford deprel: "['case', 'det', 'amod', 'nmod', 'punct', ....]".
```

CoNLL-2003 [[Sang and De Meulder, 2003]](#ref-Sang.2003) is another widely used NER dataset. This task concerned languageindependent named entity recognition, which concentrates on four kinds of named entities: locations, persons, organizations, and names of miscellaneous entities that do not belong to the previous three kinds. The related data files are available in English and German. More details can be seen on the office website^[[28]](#ref-28)^. The example of this dataset is shown as follows.

^25^https://cs.nyu.edu/grishman~ /NEtask20.book 2.html
^26^https://catalog.ldc.upenn.edu/LDC2006T06
^27^https://nlp.stanford.edu/projects/tacred/#intro
^28^https://www.clips.uantwerpen.be/conll2003/ner/

```text
text: "['U.N.', 'official', 'Ekeus', 'heads', ...], ",
pos: "['NNP', 'NN', 'NNP', 'VBZ', ...], ",
syntactic chunk: "['I-NP', 'I-NP', 'I-NP', 'I-VP', ...], ",
named entity tag: "['I-ORG', 'O', 'I-PER', 'O', ...]".
```

Besides the above famous datasets, MultiNERD [[Tedeschi and Navigli, 2022]](#ref-Tedeschi.2022), HIPE-2020 [[Ehrmann et al., 2022]](#ref-Ehrmann.2022), and NNE [[Ringland et al., 2019b]](#ref-Ringland.2019b) are also popular NER datasets in general domain. NER tasks have garnered considerable attention in numerous specialized domains. Informatics for Integrating Biology and the Bedside (I2B2) [[Stubbs and Uzuner, 2015]](#ref-Stubbs.2015) is a national biomedical computing project sponsored by the National Institutes of Health (NIH) from 2004 to 2014. I2B2 actively advocates mining medical value from clinical data and has organized a series of evaluation tasks and workshops for unstructured medical record data, and these evaluation tasks and open datasets have gained wide influence in the medical NLP community. I2B2 is maintained in the Department of Biomedical Information at Harvard Medical School and continues to conduct assessment tasks and workshops, and the project has been renamed National NLP Clinical Challenges (N2C2). More details can be seen on the office website^[[29]](#ref-29)^. Besides, there also exist many other biomedical datasets for specific medical NER tasks, including Adverse Drug Events (ADE) [[Gurulingappa et al., 2012]](#ref-Gurulingappa.2012); [[Alvaro et al., 2017]](#ref-Alvaro.2017), Drug-Drug Interaction [[Herrero-Zazo et al., 2013]](#ref-Herrero-Zazo.2013), and Chemical Protein Reaction (CPR) [[Krallinger et al., 2017]](#ref-Krallinger.2017), and GENIA [[Shibuya and Hovy, 2020]](#ref-Shibuya.2020).

### 4.4. Knowledge Bases
| Name | Knowledge | # Entities | structure |
|:-----------|:--------------|:-----------------|:-------------|
| Wikipedia | World | 13,489,694 | unstructured |
| Wikidata | World | 100,905,254 | graph |
| DrugBank | Medical | over 500,000 | structured |
| UMLS | Medical | 16,857,345 | structured |
| BioModels | Medical | unclear | structured |
| SNOMED CT | Medical | over 350,000 | structured |
| ICD-10 | Medical | unclear | structured |
| MIMIC-III | Medical | unclear | structured |
| MeSH | Medical | over 28,000 | structured |
| GeoNames | Geographical | over 25,000,000 | structured |
| EDGAR | Financial | unclear | structured |
| EduKG | Educational | 5,452 | structured |

**Table 12:** Useful knowledge bases for NER.

Table [[12]](#ref-Table.12) illustrates useful knowledge bases for NER. The biggest ones are Wikidata^[[30]](#ref-30)^ and Wikipedia^[[31]](#ref-31)^, which are multi-lingual free online encyclopedias maintained by worldwide volunteers.

There are also knowledge bases in a specific field. SNOMED CT (Systematized Nomenclature of Medicine - Clinical Terms) [[Donnelly et al., 2006]](#ref-Donnelly.2006) is a systematically organized collection of medical terms that provides a standardized representation of clinical information, which is often used in NER tasks involving clinical data. MeSH (Medical Subject Headings) [[Lipscomb, 2000]](#ref-Lipscomb.2000) is another controlled vocabulary, developed by the U.S. National Library of Medicine. It is used for indexing and organizing biomedical literature. Other medical knowledge bases include UMLS (Unified Medical Language System) [[Wheeler et al., 2007]](#ref-Wheeler.2007); [[Bodenreider, 2004]](#ref-Bodenreider.2004), ICD-10 [[Hirsch et al., 2016]](#ref-Hirsch.2016), MIMIC-III [[Johnson et al., 2016]](#ref-Johnson.2016), DrugBank [[Wishart et al., 2018]](#ref-Wishart.2018), and bioinformatics knowledge base BioModels [[Li et al., 2010]](#ref-Li.2010). GeoNames [[Ahlers, 2013]](#ref-Ahlers.2013) is a comprehensive geographic knowledge repository that encompasses over 25 million geographical names and comprises over 11 million distinctive features, including cities, countries, and landmarks. EDGAR (Electronic Data Gathering, Analysis, and Retrieval) [[Branahl, 1998]](#ref-Branahl.1998) is a database maintained by the U.S. Securities and Exchange Commission (SEC), containing financial filings and reports from publicly traded companies. EduKG [[Hu et al., 2016]](#ref-Hu.2016) is an educational knowledge base.

^29^<https://www.i2b2.org/>
^30^<https://www.wikidata.org/>
^31^<https://en.wikipedia.org/>

### 4.5. Evaluation Metrics

In the process of named entity recognition task evaluation, the main evaluation metrics are also Precision, Recall, and F-value.

### 4.6. Annotation Tools
One AI^[[32]](#ref-32)^ is an online platform that offers NLP-as-a-service. The utilization of APIs enables developers to effectively analyze, manipulate, and transform natural language inputs within their programming code without requiring any specialized knowledge of NLP. One AI facilitates the interpretation of both the meaning and information conveyed in textual data, and can produce structured data in context via language processing.

GATE Teamware^[[33]](#ref-33)^ [[Bontcheva et al., 2013]](#ref-Bontcheva.2013) is an integrated annotation tool for comprehensive language processing tasks, especially for Information Extraction systems. The University of Sheffield developed GATE Teamware that enables collaborative semantic annotation projects through a shared annotation environment. The software comprises several beneficial attributes such as the ability to load document collections, create project templates that can be used multiple times, initiate projects based on templates, assign project roles to individual users, monitor progress and obtain various project statistics in real-time, report project status, annotator activity, and statistics, and apply automatic annotations or post-annotation processing via GATE-based processing routines.

MAE^[[34]](#ref-34)^ [[Rim, 2016]](#ref-Rim.2016) (Multi-document Annotation Environment) is a general-purpose and lightweight natural language annotation tool. The tool enables users to specify and create their customized annotation tasks, annotate any text spans of their choice, utilize non-consuming tags, effortlessly establish links between annotations, and produce annotations in stand-off XML format. It also provides a simple adjudication process with a visualization feature that displays the extent tags, link tags, and non-consuming tags of any XML standoff annotated documents.

UIMA^[[35]](#ref-35)^ [[Ferrucci and Lally, 2004]](#ref-Ferrucci.2004) (Unstructured Information Management Applications) is a framework that falls under the purview of the Apache Software Foundation. It serves as a comprehensive platform for managing language processing projects and is licensed under Apache's open-source license. With its versatile capabilities, UIMA can effectively handle a diverse array of language processing tasks and extract various types of information. The UIMA's Regular Expression Annotator is capable of identifying entities such as email addresses, phone numbers, URLs, zip codes, or any other entities based on the utilization of regular expressions and concepts. The tool can generate an annotation for each detected entity or update an existing annotation with relevant feature values.

Brat^[[36]](#ref-36)^ (Browser-based Rapid Annotation Tool) is a free data labeling tool that offers a seamless browser-based interface for annotating text. It streamlines numerous annotation tasks related to natural language processing. With a thriving support community, Brat is a well-known and widely used tool in NER. It also offers the option of integrating with external resources, such as Wikipedia. Moreover, Brat enables organizations to establish servers that allow multiple users to collaborate on annotation tasks. However, implementing this feature does necessitate some technical proficiency and server management skills.

### 4.7. Methods
### 4.7.1. Nested NER
### A. Multi-label Method

Due to the fact that nested named entities can have multiple labels for a single token, traditional sequence labeling methods are not directly applicable to the recognition of nested named entities. To address this issue, researchers have attempted to convert the multi-label problem into a single-label problem or adjust the decoder to assign multiple labels to the same entity.

[[Katiyar and Cardie, 2018]](#ref-Katiyar.2018) proposed a method to address nested named entity recognition by modifying the label representation in the training set. Instead of using one-hot encoding, they used a uniform distribution over the specified classes as the label. During inference, a hard threshold is set and any class with probability above this threshold is

^32^<https://docs.oneai.com/docs>
^33^<https://gate.ac.uk/teamware/>
^34^<https://keighrim.github.io/mae-annotation/>
^35^<https://uima.apache.org/sandbox.html>
^36^<https://brat.nlplab.org/>

predicted for the token. However, this approach has two limitations: it is difficult to determine the objective for model learning; the method is sensitive to the manually chosen threshold value.

[[Strakova et al., 2019]](#ref-Strakova.2019) changed nested NER from multi-label to single-label tasks by modifying the annotation schema. They combined any two categories that may co-occur to produce a new label (e.g., combine B-Location with B-Organization to construct a new label *B Loc Org*). One benefit of this approach is that the final classification task is still a single category because all possible classification targets had been covered in the schema. Nonetheless, this method brought about a proliferation of label categories in an exponential manner, leading to sparsely annotated labels that proved difficult to learn, particularly in the context of entities nested across multiple layers.

In order to address the issue of label sparsity, [[Shibuya and Hovy, 2020]](#ref-Shibuya.2020) proposed a hierarchical approach. If the classification of nested entities cannot be resolved in a single pass, the classification is continued iteratively until either the maximum number of iterations is reached or no new entities can be generated. Nevertheless, this approach is susceptible to error propagation, whereby an erroneous classification in a preceding iteration could impact subsequent iterations.

### B. Generation-based Method

[[Li et al., 2020c]](#ref-Li.2020c) proposed a unified framework to accomplish flat and nested NER tasks by formulating NER as a machine reading comprehension (MRC) task [[Liu et al., 2023a]](#ref-Liu.2023a). In this approach, the extraction of each entity type corresponds to specific questions. For instance, when the model is given the question "which location is mentioned in the sentence?" along with the original sentences, it generates an answer such as "Washington". This approach is similar to Prompt Tuning [[Liu et al., 2021a]](#ref-Liu.2021a), which avoids the labor-intensive process of constructing manual questions. However, in this method, the generated tokens must be mapped to pre-defined named entity types.

[[Yan et al., 2021a]](#ref-Yan.2021a) proposed a novel pointer generation network. Given an input sentence, the model generates the entity indexes in this sentence that belong to entities. In such a way, flat, nested, and discontinuous entities can be recognized in a unified framework. [[Skylaki et al., 2020]](#ref-Skylaki.2020); [[Fei et al., 2021]](#ref-Fei.2021); [[Yang and Tu, 2022]](#ref-Yang.2022); [[Su et al., 2022]](#ref-Su.2022) are also following the idea of generating indexes of a sentence to recognize nested entities.

### C. Hypergraph-based Method

A hypergraph is a generalized variant of a normal graph, which is characterized by an edge that can connect an arbitrary number of vertices [[Feng et al., 2019]](#ref-Feng.2019). It is widely used in the NLP community for the tasks of syntactic parsing, semantic parsing, and machine translation because it can accurately describe the relationship between objects with multiple associations. A set of objects with only binary relations can be described by a normal graph. However, when the objects are often related to each other in a more complex one-to-many or many-to-many, e.g., nested named entities, hypergraphs become a more appropriate data structure. A typical example of nested NER with a hypergraph solution is shown in Figure [[4]](#ref-Figure.4).

![A typical example for nested NER with hypergraph solution](_page_39_Figure_8.jpeg)
(b) Corresponding hypergraph structure

**Figure 4:** A typical example for nested NER with hypergraph solution

[[Finkel and Manning, 2009]](#ref-Finkel.2009) firstly introduced hypergraphs into nested NER tasks, named Mention Hypergraph. In their model, Mention Hypergraph utilized nodes and directed hyper-edges to jointly represent named entities and their combinations. To compute the training loss, the proportion of accurate structures was calculated and divided by a normalized term. This term was obtained using a dynamic programming algorithm that aggregated feasible nested subgraphs for NER. However, the normalized terms obtained from this algorithm included fractions of pseudo-structures, which led to errors.

To deal with the problem of pseudo-structures, [[Muis and Lu, 2017]](#ref-Muis.2017) proposed a gap-based marker model to identify nested entity structures by combining mention separators with features. In this method, the authors manually designed 8 types of mention separators for various scenarios. Based on the mention separators' states for any two consecutive tokens, they defined accurate and novel graph structures. However, since this approach only utilized local information to construct the graph structures, it may not be unambiguous for long-nested named entities. For instance, when presented with the nested entity "a West African Crocodile", which includes two separate entities, "West African" and "a West African Crocodile", their approach may also recognize "a West African" as a named entity.

This ambiguous problem was solved by [[Wang and Lu, 2018]](#ref-Wang.2018), which proposes a segmental hypergraphs method. The method used an unambiguous ambiguity-free compact hypergraph representation to encode all possible combinations of nested named entities. Upon Mention Hypergraph [[Finkel and Manning, 2009]](#ref-Finkel.2009), segmental hypergraphs employed an inside-outside message-passing algorithm that can summarize the features of child nodes to the parent node and achieve efficient interference.

Besides the above work, [[Wan et al., 2021]](#ref-Wan.2021) introduced the concept of regional hypernodes and a combination method of graph convolutional network (GCN) and BiLSTM to generate hypernodes for each region. [[Yan and Song, 2022]](#ref-Yan.2022) employed start token candidates and generated corresponding queries with related contexts, then used a querybased sequence labeling module to form a local hypergraph for each candidate.

### 4.7.2. Few-shot NER
### A. Metric Learning

Metric Learning is a common technology in various few-shot tasks. Prototypical Networks [[Snell et al., 2017]](#ref-Snell.2017) is a milestone in few-shot metric learning. Prototypical Networks compute the centroid of each category based on the support set. They determine the distance between the samples in the query set and the prototype center, followed by updating the model by optimizing this distance. Upon completion of the training phase, the embedding of each sample will be situated in closer proximity to the centroid of the corresponding category. Such an idea was largely inspired by Prototype Theory (see Section [[4.1.1]](#ref-Section.4.1.1)).

[[Fritzler et al., 2019]](#ref-Fritzler.2019) adopted the prototypical network into few-shot NER tasks. They argued that words in a sentence are interdependent and, therefore, the labeling of adjacent words should be taken into account. To address this issue, they substituted the conventional token input of Prototypical Networks with complete sentences. However, this method ignores the problem of the Outside (O) class in NER tasks, which actually represent different semantic meanings. This problem would significantly affect the model's performance under few-shot settings.

To avoid the above issues, [[Yang and Katiyar, 2020]](#ref-Yang.2020) followed the nearest neighbor inference [[Wiseman and Stratos, 2019]](#ref-Wiseman.2019) to assign labels to tokens. In contrast to Prototypical Networks, which learn a prototype for each entity class, this study characterized each token by its labeled instances in the support set alongside its context. The approach determined the nearest labeled token in the support set, followed by assigning labels to the tokens in the query set that require prediction.

[[Das et al., 2022]](#ref-Das.2022) proposed CONTaiNER, which optimized the inter-token distribution distance. CONTaiNER employed generalized objectives to different token categories based on their Gaussian-distributed feature vectors. Such a method has the potential to mitigate overfitting problems that arise from the training domains.

### B. Prompt Tuning

Recently, prompt tuning has shown great potential on few-shot tasks by reformulating other tasks as mask language tasks [[He et al., 2023]](#ref-He.2023); [[Mao et al., 2022c]](#ref-Mao.2022c); [[Schick and Schutze, 2021]](#ref-Schick.2021). Prompt tuning-based methods need construct prompts to obtain masked word predictions and then map predicted works into pre-defined labels, as shown in Figure [[5]](#ref-Figure.5).

[[Cui et al., 2021]](#ref-Cui.2021) proposed a template-based method for NER, which first applied the prompt tuning to NER tasks. However, their method had to enumerate all possible spans of sentences combined with all entity types to predict labels, which suffered serious redundancy when entity types or sentence lengths increased.

Manually defined prompts were labor-intensive and made the algorithm sensitive to these prompts. To avoid the manual prompt constructions, [[Ma et al., 2022a]](#ref-Ma.2022a) tried to explore a prompt-free method for few-shot NER. The present

![A typical prompt tuning example for NER tasks.](_page_41_Figure_0.jpeg)
**Figure 5:** A typical prompt tuning example for NER tasks.

study introduced an entity-oriented language model that decodes input tokens into their corresponding label words if they belong to entities. In cases where the tokens are not entities, the entity-oriented language model decodes the original tokens. Nevertheless, this approach encounters difficulties in labeling word engineering. While this study proposed an automated label selection technique, the associated experiments revealed some degree of instability.

COPNER [[Huang et al., 2022b]](#ref-Huang.2022b) introduced class-specific words to construct prompt tuning. By comparing each token with manually selected class-specific words, this method needed neither manual prompts nor label words engineering. The selected class-specific words (a representative word corresponding to a class) were directly concatenated with original sentences as prompts. However, the manual selection of class-specific words is subjective, and a single word may not entirely capture the semantics of an entity category.

### 4.7.3. Joint NER and Relation Extraction
#### A. Parameter Sharing-based Multi-tasks Learning

Considering that NER is usually combined with relation extraction tasks applied in various downstream tasks, jointly recognizing named entities and classifying relations is a hot topic in related fields. Multi-task learning is the most common solution in joint NER and relation extraction. [[Miwa and Bansal, 2016]](#ref-Miwa.2016) firstly employed a shared Bi-LSTM encoder to obtain token representations, and then fed encoded representations into NER and relation extraction classifiers, respectively. [[Sun et al., 2020]](#ref-Sun.2020) utilized a GCN as a shared encoder to enable joint inference of both entity and relation types. The core idea of the above study is that multi-task models can enhance the interactions between the learning of NER and relation extraction, and further alleviate the error propagation by sharing common parameters [[He et al., 2021]](#ref-He.2021). However, this work cannot ensure that the sharing of information is useful and proper. NER and relation extraction might need different features to result in precise predictions.

To deal with such a problem, [[Yan et al., 2021b]](#ref-Yan.2021b) proposed an information filtering mechanism to provide valid features for NER and relation extraction. Their method used an entity and relation gate to divide cell neurons into different parts and established a two-way interaction between NER and relation extraction. In the final employed network, each neuron contained a shared partition and two task-specific partitions.

### B. Table Filling

While multi-task learning can improve the interdependence between NER and relation extraction, the relation extraction process still requires the pairing of all entities from the NER tasks to classify relations, making it impossible to completely eliminate error propagation. To solve the problem, [[Miwa and Sasaki, 2014]](#ref-Miwa.2014) proposed a table-filling strategy to achieve joint NER and relation extraction by labeling input tokens in a table. The method utilized token lists of sentences to form rows and columns. Then, they extracted entities using the diagonal elements and classified relations with a lower/upper triangular matrix of the table. This basic table-filling strategy can be seen in Figure [[6]](#ref-Figure.6). Nonetheless, this approach involved the explicit integration of entity-relation label interdependence, which necessitated the use of intricate features and search heuristics.

[[Gupta et al., 2016]](#ref-Gupta.2016) incorporated neural networks with a table-filling strategy via a unified multi-task recurrent neural network. This method detected both entity pairs and the related relations with an entity-relation table, which alleviated the need for search heuristics and explicit entity-relation label dependencies. [[Zhang et al., 2017a]](#ref-Zhang.2017a) further integrated global optimization and syntax information into the table-filling strategy to combine NER and relation

| Sentence | The | United | States | president | Biden | will | visit | |
|:----------|:----|:-------|:-------|:----------|:------|:-----|:------|:---|
| The | -- | -- | -- | -- | -- | -- | -- | -- |
| United | | LOC_B | -- | -- | CP | -- | -- | -- |
| States | | | LOC_E | -- | CP | -- | -- | -- |
| president | | | | -- | -- | -- | -- | -- |
| Biden | | | | | PER_S | -- | -- | -- |
| will | | | | | | -- | -- | -- |
| visit | | | | | | | -- | -- |
| | | | | | | | | |

**Figure 6:** The illustration of the table-filling strategy.

extraction tasks. [[Ren et al., 2021]](#ref-Ren.2021) argued that the above table-filling-based studies only focus on utilizing local features without the global associations between relations and pairs. [[Ren et al., 2021]](#ref-Ren.2021) first produced a table feature for every relation, followed by extracting two types of global associations from the generated table features. Finally, the table feature for each relation was integrated with the global associations. Such a process is performed iteratively to enhance the final features for joint learning of NER and relation extraction tasks.

### C. Tagging Scheme

The table-filling approach can mitigate issues related to error propagation. However, these techniques require the pairing of all sentence elements to assign labels, resulting in significant redundancy. To address the redundancy and avoid error propagation, [[Zheng et al., 2017]](#ref-Zheng.2017) proposed a novel tagging scheme that converted joint NER and relation extraction into a united task. The idea was similar to the solution for nested entities [[Strakova et al., 2019]](#ref-Strakova.2019), which combined NER labels with relation extraction labels by modifying the annotation schema. For example, given the sentence "The United States president Biden will visit ...", by allocating the customized labels "Country-President B 1", "Country-President E 1" for tokens "United", "States", and "Country-President E 2" for token "Biden", the proposed method can directly obtain the triplet (United State, Country-President, Biden).

[[Yu et al., 2020]](#ref-Yu.2020); [[Wei et al., 2019]](#ref-Wei.2019) proposed two similar methods. In contrast to conventional joint approaches for NER and relation extraction, which involve recognizing entities followed by relation classification, the two methods first identified all head entities. Next, for each identified head entity, they simultaneously predicted corresponding tail-entities and relations, achieving cascade frameworks combined with a customized tagging scheme. The typical joint NER and relation extraction tasks learn to model the conditional probability:

$$
P(h,r,t) = P(s)P(t | h)P(r | h,t),
$$
(7)

where *h* represent head entity; *r* represent relation; *h* represent tail entity. The above methods combined the last two parts in Eq. [[7]](#ref-7), yielding

$$
P(h,r,t) = P(s)P(t,r \mid s). \tag{8}
$$

### 4.8. Downstream Applications
### 4.8.1. Knowledge Graph Construction
Knowledge graphs are structured semantic knowledge bases for rapidly describing concepts and their interrelationships in the physical world, aggregating large amounts of knowledge by reducing the data granularity from the document level to the instance level [[Yao et al., 2022]](#ref-Yao.2022). Thus, knowledge graphs enable rapid response and reasoning about knowledge. At present, the application of knowledge graphs has become prevalent in industrial domains, such as Google search. Generally, the construction of Knowledge Graphs consists of three main parts: information extraction, information fusion, and information processing. The task of information extraction involves the identification of nodes through NER and the establishment of edges via relation extraction. The task of information fusion is utilized for normalizing nodes and edges. The normalized nodes and edges need to go through a quality assessment with the task of information processing to be added to knowledge graphs.

[[He et al., 2021]](#ref-He.2021) proposed a multi-task learning-based method for the construction of genealogical knowledge graphs. At first, [[He et al., 2019b]](#ref-He.2019b) collected unstructured online obituary data. Then, they extracted named entities as nodes and classified family relationships for these recognized people as edges to construct genealogical knowledge graphs. Similarly, [[Jiang et al., 2020]](#ref-Jiang.2020) utilized NER and relation extraction for obtaining the nodes and edge in biomedical knowledge graphs. They proposed a customized tagging schema to convert the construction of biomedical knowledge graphs into a sequence labeling task with multiple inputs and multiple outputs. [[Li et al., 2020b]](#ref-Li.2020b) proposed a systematic approach for constructing a medical knowledge graph, which involves extracting entities such as diseases and symptoms, as well as related relationships, from electronic medical records. [[Silvestri et al., 2022]](#ref-Silvestri.2022), [[Peng et al., 2019]](#ref-Peng.2019), and [[Shafqat et al., 2022]](#ref-Shafqat.2022) aimed to collect and utilize medical knowledge for NER. Further, constructing knowledge graphs requires the task of Entity Linking [[Tedeschi et al., 2021a]](#ref-Tedeschi.2021a) to normalize entities with different names. Entity Linking and NER are typically performed as pipeline tasks to yield more nodes and edges for the constructed graphs. Additionally, Entity Linking can be seen as a downstream task for NER, as it further refines the identified entities by linking them to a specific reference entity in a knowledge graph.

### 4.8.2. Recommendation Systems
Recommendation systems can be classified into two primary categories based on their solutions, namely contentbased recommenders and collaborative filtering-based recommenders [[Batmaz et al., 2019]](#ref-Batmaz.2019). For both of these groups, gathering data on users and products is a crucial step in the entire process. In this regard, NER modules play a pivotal role. For example, [[Kim et al., 2012]](#ref-Kim.2012) introduced the 5W1H model, which utilizes NER to extract contextual information, specifically Who, Why, Where, What, When, and How, to generate contextual recommendations.

[[Zhou et al., 2020]](#ref-Zhou.2020) argued that recommendation systems currently in use suffer from a deficiency of contextual information in conversational data, as well as a semantic gap between natural language expressions and the preferences of individual users for specific items. To overcome these challenges, word- and entity-oriented knowledge graphs were incorporated to enhance the data representations. Mutual Information Maximization was adopted to align the wordlevel and entity-level semantic spaces. The aligned semantic representations were used to develop a knowledge graphenhanced recommender component to make accurate recommendations, and a knowledge graph-enhanced dialog component that can generate informative keywords or entities in the response text. A NER module is a crucial component in creating such a knowledge graph-enhanced system [[Wu et al., 2023]](#ref-Wu.2023).

[[Iovine et al., 2020]](#ref-Iovine.2020) proposed a domain-independent, configurable recommendation system framework, named ConveRSE (Conversational Recommender System framEwork). ConveRSE utilized various interaction mechanisms, including natural language, buttons, and a combination of the two. The framework comprised a dialog manager, an intent recognizer, a sentiment analyzer, an entity recognizer, and a set of recommendation services. The entity recognizer component specifically focused on identifying relevant entities that were mentioned in the user's input, and linking them to an appropriate concept in the knowledge base. The ConveRSE framework's success is heavily reliant on the performance of the NER component, as it plays a crucial role in enhancing the system's overall performance.

[[Wang et al., 2019a]](#ref-Wang.2019a) proposed RippleNet, an end-to-end framework that incorporates the knowledge graph into a recommender system. RippleNet overcame the limitations of previous embedding-based and path-based approaches to knowledge graph-aware recommendation by incorporating the knowledge graph as a form of supplementary information. RippleNet included both inward aggregation and outward propagation models. The inward aggregation version aggregated and incorporated neighborhood information when computing the representation of a given entity. By extending the neighborhood to multiple hops away, it was possible to model high-order proximity, thereby capturing users' long-distance interests. On the other hand, the outward propagation model propagated users' potential preferences and explored their hierarchical interests in knowledge graph entities.

[[Upadhyay et al., 2021]](#ref-Upadhyay.2021) proposed an explainable job recommendation system by matching users with the most pertinent jobs, based on their profiles. The system also provided a human-readable explanation for each recommendation. The NER module was customized to extract pertinent details from both job postings and user profiles. These details were utilized to create comprehensible explanations for each recommendation. By identifying and categorizing entities, the NER module enhanced the accuracy and understandability of the textual explanations, providing a clear representation of the reasoning behind the recommendation system.

### 4.8.3. Dialogue Systems
Commonly, dialogue systems can be categorized into three main types, namely task-oriented, question-answering, and open-domain [[Ni et al., 2022]](#ref-Ni.2022). NER plays a role in enhancing the natural language understanding of the three types of dialogue systems, organizing original user messages into semantic slots, and classifying data domain and user intention [[Li et al., 2017b]](#ref-Li.2017b). [[Abro et al., 2022]](#ref-Abro.2022) proposed an argumentative dialogue system with NER and other natural language understanding tasks. The approach can enhance comprehension of user intent by comprehending injected entities and relationships. For the question-answering [[Dimitrakis et al., 2020]](#ref-Dimitrakis.2020) and open-domain dialogue systems, NER also plays a crucial role in the part of intent recognition and knowledge retrieval. For example, [[Zhang et al., 2021b]](#ref-Zhang.2021b) developed a sequence of sub-goals with external knowledge to improve generation performance. External knowledge refers to a range of named entities and relationships that are associated with a conceptual entity. Leveraging external knowledge allows the dialogue system to deliver a more cohesive small talk from the open domain.

### 4.9. Summary
NER is a very important semantic processing technique for information retrieval. It is the manifest of cognitive semantics, because named entities are not simply categorized by their semantics. The classified named entities also reflect their inherent attributes in people's cognition. According to Prototype Theory (see Section [[4.1.1]](#ref-Section.4.1.1)), the inherent attributes of named entities can be represented by prototypes. It is gratifying to observe that a theory has had a significant influence on research related to few-shot NER. On the other hand, the ambiguity of named entity classification argued by Graded Membership (see Section [[4.1.2]](#ref-Section.4.1.2)) and Grammatical Category (see Section [[4.1.4]](#ref-Section.4.1.4)) was rarely analyzed from computational linguistic aspects. We also do not see explainable NER studies that explain why an entity is classified into a particular category from the perspective of conceptual blending (see Section [[4.1.3]](#ref-Section.4.1.3)). The NER research on these aspects is helpful for achieving human-like intelligence in categorizing named entities.

The availability of numerous named entity recognition (NER) datasets, both in general and medical domains, has significantly enhanced computational research in this area. This may be attributed to the great application value of NER, as well as a wide range of data annotation tools. Encyclopedias knowledge and domain-specific knowledge also provide external information to help NER models better understand the context and commonsense. Now, NER has developed many practical task setups to the need of technical applications, e.g., nested NER, few-shot NER, joint NER and relation extraction, and downstream tasks, e.g., knowledge graph construction, recommendation systems, and dialogue systems.

### 4.9.1. Technical Trends

Due to the extensive research conducted on typical NER methods over the years, researchers are shifting their focus towards NER techniques that are more applicable to practical scenarios, for example, nested NER, few-shot NER, and joint NER and relation extraction. Recent technological trends for the aforementioned NER tasks are summarized in Table [[13]](#ref-Table.13).

Overall, nested NER can be addressed by multi-label, generation-based, and hypergraph-based methods. Among them, multi-label methods are straightforward and easy to implement. However, there are several limitations in the surveyed multi-label methods. For example, thresholds for multi-label selection are hard to decide empirically [[Katiyar and Cardie, 2018]](#ref-Katiyar.2018); multiple labels are suffering sparsity [[Strakova et al., 2019]](#ref-Strakova.2019) or error propagation [[Shibuya and Hovy, 2020]](#ref-Shibuya.2020), which can lower model performance. Generation-based methods are flexible. By reformulating NER tasks as question-answering, they can generate any results which satisfied the pre-defined requirements [[Shibuya and Hovy, 2020]](#ref-Shibuya.2020); [[Li et al., 2020c]](#ref-Li.2020c). These methods are used for handling Flat NER [[Skylaki et al., 2020]](#ref-Skylaki.2020), nested NER [[Yan et al., 2021a]](#ref-Yan.2021a), and discontinuous NER [[Fei et al., 2021]](#ref-Fei.2021). However, a generation-based method is hard to control what is generated, even if some studies [[Skylaki et al., 2020]](#ref-Skylaki.2020); [[Fei et al., 2021]](#ref-Fei.2021); [[Yang and Tu, 2022]](#ref-Yang.2022); [[Su et al., 2022]](#ref-Su.2022) have attempted to restrict the outputs of generation-based methods to a specific set of indexes (pointer network). The core point of the hypergraph-based method is about how to establish a hypergraph data structure to better represent interaction among all tokens in a sentence. These methods are good at modeling the interactions among all tokens in a sentence. It is important to note that the majority of hypergraph-based methods exhibit a task-specific nature, indicating a limited scope of applicability. These methods may not be universally applicable, and their effectiveness may be constrained by the specific task they are designed for.

Few-shot NER is usually achieved by metric learning and prompt tuning. Metric learning has demonstrated its effectiveness in various few-shot tasks [[Kaya and Bilge, 2019]](#ref-Kaya.2019); [[Fritzler et al., 2019]](#ref-Fritzler.2019). For few-shot NER tasks, some works predict the final labels by comparing token-to-token distance [[Yang and Katiyar, 2020]](#ref-Yang.2020); [[Das et al., 2022]](#ref-Das.2022) or token-to-prototype distance [[Huang et al., 2022b]](#ref-Huang.2022b). These methods have to decide different distance calculation functions according to different task [[Kulis et al., 2013]](#ref-Kulis.2013) and suffer instability introduced by insufficient data. By exploiting

| Task | Reference | Technique | Feature and KB | Framework | Dataset | Score | Metric |
|:-----|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------|:--------------------------------|
| | [[Shibuya and Hovy, 2020]](#ref-Shibuya.2020)<br>[[Strakova et al., 2019]](#ref-Strakova.2019)<br>[[Katiyar and Cardie, 2018]](#ref-Katiyar.2018) | DL<br>DL<br>DL | Emb.<br>Emb.<br>Bi-LSTM-CRF | LSTM-CRF<br>LSTM-CRF<br>Bi-LSTM-CRF | ACE-05<br>ACE-05<br>ACE-05 | 84.3%<br>84.3%<br>70.2% | F1<br>F1<br>F1 |
| Nested NER | [[Li et al., 2020c]](#ref-Li.2020c)<br>[[Su et al., 2022]](#ref-Su.2022)<br>[[Yan et al., 2021a]](#ref-Yan.2021a)<br>[[Yan and Tu, 2022]](#ref-Yan.2022)<br>[[Wang and Lu, 2018]](#ref-Wang.2018)<br>[[Muis and Lu, 2017]](#ref-Muis.2017)<br>[[Finkel and Manning, 2009]](#ref-Finkel.2009) | DL<br>DL<br>DL<br>DL<br>Graph<br>Graph<br>Graph | BERT, Span<br>BERT, Span<br>BERT, Span<br>BERT, Span<br>Emb., Segmental Hypergraphs<br>Emb., Multi-Constituent Hypergraphs<br>Emb., Constituent Hypergraphs | Pointer Network<br>Pointer Network<br>Pointer Network<br>Pointer Network<br>Unified Framework<br>Unified Framework<br>Unified Framework | ACE-05<br>ACE-05<br>ACE-05<br>ACE-05<br>GENIA<br>GENIA<br>GENIA | 85.0%<br>85.1%<br>70.8%<br>72.0%<br>74.7%<br>76.9%<br>78.6% | F1<br>F1<br>F1<br>F1<br>F1<br>F1<br>F1 |
| (5 shot) Few-shot NER | [[Huang et al., 2022b]](#ref-Huang.2022b)*<br>[[Das et al., 2022]](#ref-Das.2022)<br>[[Fritzler et al., 2019]](#ref-Fritzler.2019)<br>[[Cui et al., 2021]](#ref-Cui.2021)<br>[[Yang and Katiyar, 2020]](#ref-Yang.2020) | DL<br>DL<br>DL<br>DL<br>DL | BERT<br>BERT<br>BERT<br>BERT<br>Prototype network | Prototype network<br>Contrastive learning<br>Nearest neighbor<br>Prompt Tuning<br>Prompt Tuning | I2B2<br>I2B2<br>I2B2<br>I2B2<br>OntoNotes | 46.7%<br>32.1%<br>33.7%<br>21.8%<br>- | F1<br>F1<br>F1<br>F1<br>F1 |
| Joint NER and RE | [[Zheng et al., 2017]](#ref-Zheng.2017)<br>[[Zhang et al., 2017a]](#ref-Zhang.2017a)<br>[[Miwa and Bansal, 2016]](#ref-Miwa.2016)<br>[[Yu et al., 2020]](#ref-Yu.2020)<br>[[Gupta et al., 2016]](#ref-Gupta.2016)<br>[[Yan et al., 2021b]](#ref-Yan.2021b)<br>[[Sun et al., 2020]](#ref-Sun.2020) | DL<br>DL<br>DL<br>DL<br>DL<br>DL<br>DL | Emb., BERT<br>Emb., BERT<br>Emb., BERT<br>Emb., BERT<br>Emb., BERT<br>Emb., BERT<br>Emb., BERT | Tagging scheme<br>Tagging scheme<br>Table filling<br>Table filling<br>Table filling<br>Bipartite graph<br>Bipartite graph | ACE-05<br>ACE-05<br>ACE-05<br>ACE-05<br>NYT<br>NYT<br>NYT | 59.0%<br>49.5%<br>57.5%<br>62.1%<br>66.8%<br>69.1%<br>55.6% | F1<br>F1<br>F1<br>F1<br>F1<br>F1<br>F1 |
| Task-driven NER | [[Peng et al., 2019]](#ref-Peng.2019)*<br>[[Hirsch et al., 2016]](#ref-Hirsch.2016)*<br>[[Shafqat et al., 2022]](#ref-Shafqat.2022)* | DL<br>DL<br>DL | BERT, UMLS<br>Emb., ICD-10<br>Emb., MIMIC-III | Fine Tuning<br>Fine Tuning<br>Fine Tuning | no public<br>no public<br>no public | -<br>-<br>- | F1<br>F1<br>F1 |
| | | | | | | | |

**Table 13:** A summary of representative NER techniques. The study with * means it cannot be compared with other studies since it did not report 5-shot results. the full potential of language models, prompt tuning is proposed and demonstrated as a promising technology for few-shot tasks [[Liu et al., 2021a]](#ref-Liu.2021a); [[He et al., 2023]](#ref-He.2023); [[Liu et al., 2022b]](#ref-Liu.2022b). Prompt tuning reformulate NER as a mask language model task to reduce the gap between NER and employed pre-training LMs. The backward is that prompt tuning needs extra template construction and label word mappings and some studies have tried to deal with such problems [[Huang et al., 2022b]](#ref-Huang.2022b).

For Joint NER and RE tasks, we summarize related studies into three groups, including parameter sharing-based multi-task learning, table-filling strategy, and customized tagging scheme. Parameter sharing is the basic idea in multitask learning, which can be used to enhance the interaction between NER and RE [[Li et al., 2017a]](#ref-Li.2017a); [[Bekoulis et al., 2018]](#ref-Bekoulis.2018). This method can provide some relief from error propagation, but it cannot completely eliminate the issue. Also, this method has to pair every two entities for relation extraction, which introduces unnecessary redundancy. Table filling-based joint NER and relation extraction can completely eliminate error propagation by converting NER and relation extraction into a whole sequence-tagging task [[Gupta et al., 2016]](#ref-Gupta.2016); [[Ren et al., 2021]](#ref-Ren.2021); [[Ma et al., 2022b]](#ref-Ma.2022b). However, these methods have to label every two token pairs in an input sentence in an enumerable fashion. If relation extraction is defined as an unidirectional task, the half of calculations are wasted. Following the idea of the table filling strategy, tagging scheme-based methods also model the NER and relation extraction as an integrated task. The fundamental concept of the tagging scheme is to merge the labels assigned for NER with those assigned for relation extraction into a unified label [[Zheng et al., 2017]](#ref-Zheng.2017); [[Strakova et al., 2019]](#ref-Strakova.2019). Such a method has the potential to circumvent issues related to both error propagation and redundancy; however, it may also lead to a sparsity of labels.

### 4.9.2. Application Trends
| Reference | Downstream Task | Feature | Parser | Explain. |
|:--------------------------------|:-----------------------------|:--------|:-------|:---------|
| [[Yao et al., 2022]](#ref-Yao.2022) | Knowledge Graph Construction | | ✓ | |
| [[He et al., 2021]](#ref-He.2021) | Knowledge Graph Construction | | ✓ | |
| [[Jiang et al., 2020]](#ref-Jiang.2020) | Knowledge Graph Construction | | ✓ | |
| [[Li et al., 2020b]](#ref-Li.2020b) | Knowledge Graph Construction | | ✓ | |
| [[Kim et al., 2012]](#ref-Kim.2012) | Recommendation Systems | | ✓ | ✓ |
| [[Adomavicius and Tuzhilin, 2011]](#ref-Adomavicius.2011) | Recommendation Systems | ✓ | | |
| [[Zhou et al., 2020]](#ref-Zhou.2020) | Recommendation Systems | ✓ | | |
| [[Iovine et al., 2020]](#ref-Iovine.2020) | Recommendation Systems | ✓ | | |
| [[Wang et al., 2019a]](#ref-Wang.2019a) | Recommendation Systems | | ✓ | |
| [[Li et al., 2017b]](#ref-Li.2017b) | Dialogue Systems | | ✓ | |
| [[Abro et al., 2022]](#ref-Abro.2022) | Dialogue Systems | | ✓ | |
| [[Dimitrakis et al., 2020]](#ref-Dimitrakis.2020) | Dialogue Systems | | ✓ | |
| [[Zhang et al., 2021b]](#ref-Zhang.2021b) | Dialogue System | | ✓ | ✓ |

**Table 14:** A summary of the representative applications of NER in downstream tasks. ✓ denotes the role of NER in a downstream task.

We have discussed three main downstream applications of NER, including knowledge graph construction, dialogue systems, and recommendation systems. Table [[14]](#ref-Table.14) illustrate related studies. Usually, NER is the basic module for providing recognized entities for further utilization. In this case, a NER model works as a parser to mine knowledge from unstructured text. The recognized entities and relations can be used as nodes and edges for knowledge graph construction. The entities can also serve as intent recognition methods in recommendation systems, and slot-filling methods in dialogue systems. For example, [[Wu et al., 2020a]](#ref-Wu.2020a) proposed a pre-trained task-oriented dialogue BERT, which significantly boosts the performance of a dialogue system by improving the intent detection sub-task. [[Wang et al., 2020]](#ref-Wang.2020) proposed a method for recognizing related spans and value normalization with slot attention to improve the dialogue system. Besides, we also observe that using the identified named entities as features can also improve the performance of recommendation systems, because NER can help identify important entities that could be useful for making recommendations.

The most common problem is error propagation between NER and other components in a downstream system. [[Kim et al., 2018]](#ref-Kim.2018) employed a two-step neural dialog state tracker to alleviate the impact of the original error. With the development of PLMs and LLMs, many downstream tasks are organized as end-to-end processing tasks to achieve higher accuracy and mitigate error propagation issues. However, we can still observe that NER can improve the explainability in recommendation and dialogue systems [[Kim et al., 2012]](#ref-Kim.2012); [[Zhang et al., 2021b]](#ref-Zhang.2021b), which is also an important aspect of AI research. There is still a considerable untapped potential for integrating NER with other downstream tasks, e.g., explaining how concepts blend each other between different entities; what the inherent attribute of a group of entities the selected prototypes represent; how robust an identified named entity is.

### 4.9.3. Future Works
Open-domain NER. Compared with typical single-domain NER, open-domain NER has more categories. Besides, the entity classes are hardly defined in advance. For such reason, open-domain NER is more capable of handling rapidly expanding data, and mining more potential knowledge which is hidden in massive unstructured text data [[Hohenecker et al., 2020]](#ref-Hohenecker.2020); [[Kolluru et al., 2020]](#ref-Kolluru.2020). Open-domain NER is significant because it discovers and connects world knowledge via automatic text mining. Many manually developed lexical resources, e.g., WordNet can only cover limited concepts. When the concepts come to multi-word expressions, manually mining, structuring and updating those concepts can result in the exponential growth of human efforts. Open-domain NER is helpful for mitigating human efforts and delivering a knowledge base that connects entities from different domains.

Multi-lingual NER. In light of the fact that a significant number of languages in existence lack sufficient annotated data, knowledge transfer from high-resource languages to low-resource languages can serve as a viable solution to compensate for the paucity of data [[Rahimi et al., 2019]](#ref-Rahimi.2019); [[Tedeschi et al., 2021b]](#ref-Tedeschi.2021b). Developing robust multi-lingual NER systems that can perform across multiple languages will achieve more comprehensive knowledge graphs, linking entities from different languages. It is valuable because it may lead to a united concept representation system covering different languages. On the other hand, the task of developing multi-lingual NER systems is fraught with difficulties, primarily due to the inherent dissimilarities in entity types and language structures across different languages. As a result, aligning entities and transferring knowledge learned from one language to another can present significant challenges for multi-lingual NER systems.

Unified framework for NER. In the real-world scenario, there exist flat-named entities, nested entities, and discontinuous entities. Most NER-related studies only focus on the combination of flat with nested entities or flat discontinuous entities. Both of them cannot recognize all kinds of entities. Developing a unified framework to simultaneously handle such a problem becomes an urgent need for NER [[Fei et al., 2021]](#ref-Fei.2021). Hierarchical concept representation knowledge bases may provide a preliminary ontology that can be used for organizing entities and their relationships. However, most of the ontology systems were manually developed by experts. This manually constructed knowledge may be invalid in specific application scenarios. A potential avenue for future research in NER is the development of a unified and robust framework for organizing entities. Such a framework could facilitate the creation of comprehensive knowledge graphs that capture the relationships between entities and can better support downstream tasks.

Continual-learning for NER. Humans exhibit a remarkable aptitude for transferring acquired knowledge from one task to another and retain their ability to perform the former task even after learning the latter. This ability is called continuous learning or life-long learning, which a regarded as an important characteristic of an intelligent system. Also, such ability can help us continue to use already deployed models when a new class of entity to be identified appears, rather than developed a new model from scratch [[De Lange et al., 2021]](#ref-De.2021). There are some exploratory studies started to pay attention to such a problem. However, a satisfactory solution has not been found yet and existing methods still suffer the severe Catastrophic Forgetting [[Monaikul et al., 2021]](#ref-Monaikul.2021); [[Xia et al., 2022]](#ref-Xia.2022); [[Vijay and Priyanshu, 2022]](#ref-Vijay.2022). Continual learning is a critical skill for NER because NER is corpus-dependent. It is very important to update entity collections and the associated label sets, when a new corpus arrives [[He et al., 2022b]](#ref-He.2022b). In this case, detecting new entities and new labels with a former trained NER model represents a challenging yet highly promising research avenue.

## 5. Concept Extraction

Concept extraction is a process to extract concepts of interest from the text. To our best knowledge, the task of computational concept extraction was first proposed by [[Montgomery, 1982]](#ref-Montgomery.1982), which analyzed the next 5 years of evolutionary progress in contemporary military message routing systems, with a focus on their transition towards becoming more advanced and knowledge-based systems. They argue that taxonomic hierarchies could be constructed to allow property inheritance of concepts, and therefore to perform rudimentary inference and analogic reasoning based on the taxonomies. [[Montgomery, 1982]](#ref-Montgomery.1982) also highlighted two important sub-tasks of concept extraction for the next-generation knowledge-based systems from the perspective of 1982, namely lexicon development and conceptual structure construction.

Recent research on concept extraction has been conducted in various fields of AI research, including natural language processing (NLP) and data mining [[Miner et al., 2012]](#ref-Miner.2012). Keyphrase generation [[Alami Merrouni et al., 2020]](#ref-Alami.2020) is one of the most common concept extraction tasks. It is a summarization task focusing on extracting keyphrases from a full passage to help readers quickly understand the passage, where keyphrases can be understood as the important concepts within a passage. Methods for keyphrase extraction can be both extractive (copying from existing words) and abstractive (not copying but summarizing and abstracting from existing texts). The process of generating keyphrases facilitates the creation of a lexicon that corresponds to a specific set of concepts. Another stream of concept extraction aims at the development of ontological knowledge bases to represent, e.g., commonsense knowledge [[Havasi and Speer, 2007]](#ref-Havasi.2007), hypernym and synonym knowledge [[Snow et al., 2006]](#ref-Snow.2006), sentic knowledge [[Cambria et al., 2022a]](#ref-Cambria.2022a). These tasks tried to extract concepts to fit into pre-defined knowledge structures. Then, the structured knowledge can be directly used in downstream tasks.

Current concept extraction research is also grounded on related application scenarios, such as clinical concept extraction [[Fu et al., 2020]](#ref-Fu.2020), course concept extraction [[Pan et al., 2017a]](#ref-Pan.2017a), and patent concept extraction [[Liu et al., 2020]](#ref-Liu.2020). Clinical concept extraction is to transform massive unstructured electronic health records data into structured data; Course concept extraction is to extract important phrases in course captions to help to understand. Among them, clinical concept extraction is very similar to the information extraction task in NLP which aims at extracting most of the details in the unstructured text. Course and patent concept extraction are more similar to summarization tasks in NLP that target extracting important phrases.

The main difference between concept extraction and NER tasks is that the extracted concepts or keyphrases are not identified by pre-defined entity classes. In contrast, they reflect the general idea of their contexts or target domain whose concepts are being discussed, while the goal of NER is to extract important factual information from the text. However, there are overlaps between NER and concept extraction when some concepts of interest, e.g., proper nouns can be also defined as named entities. Many domain-specific concept extraction tasks, e.g., clinical concept extraction, course concept extraction, and patent concept extraction can also be categorized as NER tasks because they aim at extracting concepts that are related to specific events. These events are also factual information. We review them in this section because they define themselves as concept extraction tasks in their original works. It also has become a trend of domain-specific concept extraction.

Another related field is relation extraction, which is a sub-field of information extraction. Relation extraction extracts information from raw text and represents it in the form of a semantic relation between entities [[Kartik Detroja, 2023]](#ref-Kartik.2023). The main difference is that, relation extraction targets at extracting relations between entities, while concept extraction targets at extracting noun entities. In knowledge graph development, relation extraction can help to connect nodes of concepts with purposeful relationships.

Concept extraction has also accelerated and contributed to multiple downstream applications, such as sentiment computing [[Cambria et al., 2022a]](#ref-Cambria.2022a), information retrieval [[Xiong et al., 2017]](#ref-Xiong.2017), commonsense explanation generation [[Fang and Zhang, 2022]](#ref-Fang.2022). These applications mostly leverage explicitly extracted concepts.

Previous survey on concept extraction on focuses on clinical concept extraction [[Fu et al., 2020]](#ref-Fu.2020), which is a particular application field of concept extraction. In this section, we provide a more comprehensive review on concept extraction.

## 5.1. Theoretical Research
### 5.1.1. Exemplar Theory
[[Medin and Schaffer, 1978]](#ref-Medin.1978) argued that concepts are represented by a collection of particular exemplars or individual instances that are linked to the category. When we categorize an instance, we compare it with multiple specific exemplars of the category. This is different from Prototype Theory where a new instance is categorized by comparing the instance to the abstract prototype of the category (see Section [[4.1.1]](#ref-Section.4.1.1)). [[Medin and Schaffer, 1978]](#ref-Medin.1978) formed the task of concept categorization as a classification task, and conducted experiments with 32 participants. The experiments showed that the classification judgments made by participants were impacted by various factors. These factors included the extent of resemblance between the probe item and exemplars previously acquired, the number of prior exemplars that shared resemblances with the probe item, and the similarity present both within and between the categories of the previously learned exemplars. For concept extraction and categorization, Exemplar Theory may suggest that models may take categorized instances into account when categorizing a new instance.

### 5.1.2. Semantic Primitives
[[Wierzbicka, 1972]](#ref-Wierzbicka.1972) believed that it is possible to describe every human language by using a limited number of universal semantic primitives. These primitives are representative of fundamental concepts that form the basis of human communication and thinking. [[Wierzbicka, 1972]](#ref-Wierzbicka.1972) established 64 universal semantic primes, which consist of basic words or ideas that cannot be defined in relation to more elementary concepts. However, these primes can be utilized to describe all other concepts present within a language. Semantic Primitives suggest that concepts should be organized as multiple layers from the concrete to abstract ones. Decision-making that runs on concrete concepts can be completed through the upper-level abstract concepts that contain those concrete concepts. Thus, it is critical to represent the hierarchical and linking relationships between concepts. There are other theories mentioned before, e.g., Frame Semantics (see Section [[2.1.4]](#ref-Section.2.1.4)), that may guide concept structure development. Frame Semantics highlights the connection of related concepts, while Semantic Primitives suggest the hierarchical relationships between concepts and the distinction between primitive concepts and others.

### 5.1.3. Conceptual Spaces

[[Gardenfors, 2004]](#ref-Gardenfors.2004) defined concept as the "theoretical entities that can be used to explain and predict various empirical phenomena concerning concept formation". The author believed that concept representations are multidimensional, where each dimension is indicative of a different characteristic or property associated with the concept. For example, one could represent the concept of a car within a conceptual space that includes dimensions such as size, speed, color, and shape. This is very similar to current vectorial representations of words or entities in NLP, while the dimensionality of Conceptual Spaces is explainable by concept properties. [[Gardenfors, 2004]](#ref-Gardenfors.2004) also placed significant emphasis on the role of context in understanding and representing concepts. This is due to the fact that different contexts may emphasize different features or dimensions of concepts. Then, the connections between concepts are determined by the relationships between their property similarity in the conceptual space. For example, "dog" and "cat" are similar in the animal concept space, because their properties are similar; "mammals" can be separated from "reptiles" by a property difference boundary, although both are in the animal space. This may encourage concept extraction tasks to extract both concept entities and properties associated in contexts. This is because properties define how concepts are connected from the view of [[Gardenfors, 2004]](#ref-Gardenfors.2004).

### 5.2. Annotation Schemes
From the goal of the keyphrase annotation aspect, there are in general two types of annotation schemes for keyphrase extraction-liked concept extraction. The first is to precisely select existing keyphrases from input text, but not to create semantically-equivalent phrases. The second is to both select existing keyphrases and create "absent keyphrases" that are necessary but do not exist in the input text [[Hulth, 2003]](#ref-Hulth.2003).

From the format of assigned annotations aspect, there are in general two annotation schemes as well. The first scheme is to directly give the keyphrases existing in the source text. The second scheme treats the keyphrase extraction task as a sequence labeling task, and assigns a label to each of the tokens in source text [[Hulth, 2003]](#ref-Hulth.2003). The assigned labels in the current dataset follow a BIO scheme defined in table [[10]](#ref-Table.10). Specifically, three labels are used: B (Beginning), I (Inner), and O (Other).

### 5.3. Datasets
The surveyed popular concept extraction datasets and their statistics can be viewed in Table [[15]](#ref-Table.15). Overall the main thread of dataset development is (1) larger scale of datasets; (2) attending to both extractive keyphrases and abstractive keyphrases; (3) more fine-grained annotations for tags; (4) more application domains. [[Hulth, 2003]](#ref-Hulth.2003) proposed one of the first keyphrase extraction datasets, termed Inspec. Their dataset is based on the scientific papers under *Computers and Control*, and *Information Technology* disciplines in the Inspec database. The keywords used in the scientific papers are selected as the keyphrases. Abstracts are used as the keyphrase extraction context. Keywords in scientific papers are used as keyphrases. Each abstract has two sets of keywords: a set of controlled terms, i.e., terms restricted to the Inspec thesaurus; and a set of uncontrolled terms that can be any suitable terms that may or may not be present in the abstracts. They collected 1000 abstracts as a train set, 500 as a validation set, and 500 as a test set.

| Dataset | Task | Source | # Samples | Reference |
|:--------------|:-----|:--------------------------|:----------|:-----------------------|
| Inspec | KE | Inspec database | 2,000 | [[Hulth, 2003]](#ref-Hulth.2003) |
| NUS | KE | Google SOAP API | 211 | [[Nguyen and Kan, 2007]](#ref-Nguyen.2007) |
| Krapivin | KE | ACM Digital Library | 2,304 | [[Krapivin et al., 2009]](#ref-Krapivin.2009) |
| SemEval2010 | KE | ACM Digital Library | 244 | [[Kim et al., 2010]](#ref-Kim.2010) |
| Twitter | KE | Twitter | 1,000 | [[Zhang et al., 2016]](#ref-Zhang.2016) |
| | | ACM Digital Library, | | |
| KP-20K | KE | ScienceDirect, | 567,830 | [[Meng et al., 2017]](#ref-Meng.2017) |
| | | and Web of Science | | |
| CCF | KE | China Computer Federation | 13,449 | [[Wang et al., 2018b]](#ref-Wang.2018b) |
| MLDBMD | KE | Academic Conferences | 128.1k | [[Li et al., 2018]](#ref-Li.2018) |
| TempEval | ClCE | Mayo Clinic | 600 | [[Bethard et al., 2016]](#ref-Bethard.2016) |
| i2b2-2010 | ClCE | Clinical Records | 826 | [[Uzuner et al., 2011]](#ref-Uzuner.2011) |
| n2c2-2018 | ClCE | Clinical Records | 505 | [[Henry et al., 2020]](#ref-Henry.2020) |
| MIMIC | ClCE | MIMIC-III Database | 1,610 | [[Gehrmann et al., 2018]](#ref-Gehrmann.2018) |
| MOOCs | CoCE | Coursera and XuetangX | 4375 videos | [[Pan et al., 2017b]](#ref-Pan.2017b) |
| EMRCM | CoCE | Chinese Textbooks | 3,730 pages | [[Huang et al., 2019b]](#ref-Huang.2019b) |
| USPTO | PCE | USPTO Database | 94,000 | [[Liu et al., 2020]](#ref-Liu.2020) |

**Table 15:** Concept extraction datasets and statistics. KE denotes Keyphrase Extraction. ClCE denotes Clinical Concept Extraction. CoCE denotes Course Concept Extraction. PCE denotes Patent Concept Extraction.

```text
abstract: "[ 'A', 'scalable', 'model', 'of', 'cerebellar', 'adaptive', 'timing', 'and', 'sequencing', ':', ...]"
doc bio tags: "[ 'O', 'B', 'I', 'O', 'B', 'I', 'I', 'O', 'O', 'O', ...]"
extractive keyphrases: "[ 'scalable model', 'cerebellar adaptive timing', ... ]"
abstractive keyphrase: "[ 'cerebellar sequencing', ...]"
```

[[Nguyen and Kan, 2007]](#ref-Nguyen.2007) proposed the NUS dataset with the motivation that keyphrase extraction requires multiple judgments and cannot rely merely on the single set of author-provided keyphrases. They first used Google Search API to retrieve scientific publications, and then recruited student volunteers to participate in manual keyphrase assignments. They finally collect 211 documents, each with two sets of keyphrases: one is given by the original authors of the paper, and the other is given by student volunteers. The data format of NUS is the same as Inspec [[Hulth, 2003]](#ref-Hulth.2003).

[[Krapivin et al., 2009]](#ref-Krapivin.2009) proposed the Krapivin dataset, consisting of around 2,000 scientific papers as well as their keywords assigned by the original authors. The scientific papers were published by ACM in the period from 2003 to 2005, and were written in English. One of the novelties of this dataset is that the text data in the scientific papers were collected with three distinct categories: title, abstract, and main body. They finally collect 460 test data and 1.84k validation data. The data format is similar to Inspec [[Hulth, 2003]](#ref-Hulth.2003) but has a title and body in addition to the abstract.

SemEval-2010 Task 5 [[Kim et al., 2010]](#ref-Kim.2010) is on automatic keyphrase extraction from scientific articles. Input for this task is a document from either of the four domains: distributed systems, information search, and retrieval, distributed artificial intelligence, and social and behavioral sciences. Outputs are manually annotated keyphrases for the document. This dataset contains 144 documents as a train set, and 100 documents as a test set. It also selects 40 documents from the train set to compose a trial set. For each set, documents are evenly distributed from the four topics. The annotation follows the first scheme in Section [[5.2]](#ref-Section.5.2). The data format is the same as Inspec [[Hulth, 2003]](#ref-Hulth.2003).

[[Zhang et al., 2016]](#ref-Zhang.2016) constructed a keyphrase extract dataset from Twitter using an automatic text mining method. Their core assumption is that hashtags in a tweet can be used as keyphrases for the tweet. To construct the dataset, they first collected 41 million tweets, and then filtered them which contain non-Latin tokens. URL links, and reply tweets were removed. Thus, the remaining text only contains tweets and a hashtag. They finally kept 110K tweets. To evaluate the quality of the collected tweets, they sampled 1000 tweets and chose three volunteers to score them. As a result, 90.2% tweets are suitable, and 66.1% are perfectly suitable. The annotation follows the first scheme in Section [[5.2]](#ref-Section.5.2).

```text
tweet: "Hard to believe it but these are REAL state alternatives to taking Obamacare
funds from the gov't (via @Upworthy)"
keyphrase: "obamacare"
```

[[Pan et al., 2017b]](#ref-Pan.2017b) proposed a keyphrase extraction dataset, where data were sourced from online course captions.

Labels are existing phrases in the captions. The courses are computer science and economics courses, selected from two famous MOOC platforms — Coursera and XuetangX. Labels were first filtered from captions using automatic methods and then annotated by two human annotators. A candidate concept was only labeled as a course concept if the two annotators were in agreement. As a result, they collected captions from 4375 videos, and 16720 labeled concepts.

```text
course caption: "You might learn how to write a bubble sort and learn why a bubble sort is not as good as a heapsort."
keyphrase: "[ 'bubble sort', 'heapsort' ]"
```

KP-20K [[Meng et al., 2017]](#ref-Meng.2017) is a testing dataset, where the input texts are titles and abstracts of computer science research papers collected from ACM Digital Library. The labeled keyphrases are the keyphrases shown in the research papers. The annotation follows the second scheme in Section [[5.2]](#ref-Section.5.2), since the keyphrases given by authors were not necessarily existing keyphrases in the papers. KP-20K has the same data format as Inspec.

[[Huang et al., 2019b]](#ref-Huang.2019b) were motivated to automatically construct an educational concept map. The educational concept map shows concepts that will be learned in courses, as well as the temporal relation between the concepts (e.g., to learn concept A, it is a prerequisite to learn concept B; Concept A and concept B can help with the understanding of each other). To construct the dataset written in Chinese, they first used OCR to obtain the text from textbooks, then manually labeled key concepts for each textbook (as "key concept" or "not key concept") and finally manually annotated the relationships among the labeled key concepts (as "*w*~i~ is *w*~j~'s prerequisite", "*w*~i~ and *w*~j~ has collaboration relationship", or "no relationship"). As a result, they collected 3730 pages in textbooks, 1092 key concepts, 818 prerequisite relations, and 916 collaboration relations. However, in their GitHub repo, only keyphrases and relations between keyphrases can be found, while the text cannot be found.

```text
keyword: "[ 'average', 'weighted average', ... ]"
relation: "[ 'average : weighted average', ... ]"
```

There are concept extraction datasets focused on a specific domain, e.g., clinical concepts (TempEval [[Bethard et al., 2016]](#ref-Bethard.2016), i2b2-2010 [[Uzuner et al., 2011]](#ref-Uzuner.2011), n2c2-2018 [[Henry et al., 2020]](#ref-Henry.2020), and MIMIC [[Gehrmann et al., 2018]](#ref-Gehrmann.2018)), course concepts (MOOCs [[Pan et al., 2017b]](#ref-Pan.2017b), and EMRCM [[Huang et al., 2019b]](#ref-Huang.2019b)), and patent concepts (USPTO [[Liu et al., 2020]](#ref-Liu.2020)). They also followed keyphrase extraction setups, whereas the targets are to extract concepts of interest.

### 5.4. Knowledge Bases
Besides classical lexicon resources such as WordNet, encyclopedias (including Baidu Encyclopedias and Wikipedia) can also be used to provide external knowledge for concepts [[Pan et al., 2017b]](#ref-Pan.2017b). Methods for extracting concepts based on embedding techniques may encounter issues with low frequency,