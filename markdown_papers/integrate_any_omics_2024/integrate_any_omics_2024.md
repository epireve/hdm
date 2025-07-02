---
cite_key: ma_2017
title: Integrate Any Omics: Towards genome-wide data integration for patient stratification
authors: Shihao Ma
year: 2017
date_processed: '2025-07-02'
phase2_processed: true
original_folder: integrate_any_omics_2024
images_total: 12
images_kept: 12
images_removed: 0
tags:
- Biomedical
- Cancer
- Data Integration
- Healthcare
- Machine Learning
- Personalized Medicine
keywords:
- 1 integrao overview
- 1 introduction
- 2 integrao
- 2 results
- 3 discussion
- 32 integrao
- 4 methods
- 5 supplementary tables
- 6 supplementary figures
- BayesPrism
- InterSim
- McGowan
- McLendon
- VandenBerg
- accuracy
- age-adjusted
- all-encompassing
- all-missing
- aml cancer dataset
- anti-cancer
- artificial intelligence
- as is
- beat-aml
- better-informed
- biomarker
- bowang-lab
- cdc-like
- classification
- clustering
- convergence
---

# Integrate Any Omics: Towards genome-wide data integration for patient stratification

Shihao Ma1,2,3, Andy G.X. Zeng5,8, Benjamin Haibe-Kains2,6,8, Anna Goldenberg2,3,7, John E Dick5,8 and Bo Wang1,2,3,4\*

<sup>1</sup>Peter Munk Cardiac Centre, University Health Network, Toronto, Ontario, Canada.

<sup>2</sup>Vector Institute for Artificial Intelligence, , Toronto, Ontario, Canada.

<sup>3</sup>Department of Computer Science, University of Toronto, Toronto, Ontario, Canada.

<sup>4</sup>Department of Laboratory Medicine and Pathobiology, University of Toronto, Toronto, Ontario, Canada.

<sup>5</sup>Department of Molecular Genetics, University of Toronto, Toronto, Ontario, Canada.

<sup>6</sup>Department of Medical Biophysics, University of Toronto, Toronto, Ontario, Canada.

<sup>7</sup>Genetics and Genome Biology, the Hospital for Sick Children, Toronto, Ontario, Canada.

<sup>8</sup>Princess Margaret Cancer Centre, University Health Network, Toronto, Ontario, Canada.

\*Corresponding author(s). E-mail(s): bowang@vectorinstitute.ai;

## Abstract

High-throughput omics profiling advancements have greatly enhanced cancer patient stratification. However, incomplete data in multi-omics integration presents a significant challenge, as traditional methods like sample exclusion or imputation often compromise biological diversity and dependencies. Furthermore, the critical task of accurately classifying new patients with partial omics data into existing subtypes is commonly overlooked. To address these issues, we introduce IntegrAO (Integrate Any

### 2 IntegrAO

Omics), an unsupervised framework for integrating incomplete multiomics data and classifying new samples. IntegrAO first combines partially overlapping patient graphs from diverse omics sources and utilizes graph neural networks to produce unified patient embeddings. Our systematic evaluation across five cancer cohorts involving six omics modalities demonstrates IntegrAO's robustness to missing data and its accuracy in classifying new samples with partial profiles. An acute myeloid leukemia case study further validates its capability to uncover biological and clinical heterogeneity in incomplete datasets. IntegrAO's ability to handle heterogeneous and incomplete data makes it an essential tool for precision oncology, offering a holistic approach to patient characterization.

Keywords: Multi-omics integration, Incomplete modality, Patient stratification, Subtype prediction

# 1 Introduction

Precision medicine, which tailors personalized treatment based on the unique genetic profiles of individual cancer patients, has been recognized as the foundation of future cancer therapeutics [\[1\]](#page-23-0). The field is moving towards gathering multimodal data to address cancer's inherent heterogeneity [\[2\]](#page-23-1), characterized by diverse genetic, transcriptomic, and phenotypic variations [\[3,](#page-23-2) [4\]](#page-23-3). Recent advancements in high-throughput technologies have enabled multi-dimensional profiling through diverse omics modalities. Projects like The Cancer Genome Atlas (TCGA) [\[5\]](#page-23-4) and the International Cancer Genome Consortium (ICGC)[\[6\]](#page-23-5) have produced and collected thousands of tumor samples at different molecular levels. Moreover, the rise of single-cell profiling, particularly single-cell transcriptomics, has deepened insights into tumor microenvironments by highlighting the distinct expression profiles of various cell types. Consequently, patient stratification, which involves categorizing patients based on distinct genetic, transcriptomic, and phenotypic profiles, has become a critical process in precision medicine for aiding in the development of tailored treatment approaches.

Integrating multi-omics data, leveraging the complementary nature of these datasets, offers a more holistic understanding of cancer. In the past decade, diverse integration methods have been developed, ranging from network-based[\[7](#page-23-6)[–9\]](#page-23-7) and matrix factorization-based[\[10,](#page-23-8) [11\]](#page-24-0) to Bayesian clustering techniques[\[12,](#page-24-1) [13\]](#page-24-2) and advanced deep learning approaches[\[14,](#page-24-3) [15\]](#page-24-4). Despite successes in disease subtyping[\[16,](#page-24-5) [17\]](#page-24-6) and advancing precision medicine[\[18\]](#page-24-7), these methods share a common limitation: the requirement for complete data across samples. This prerequisite becomes problematic due to the frequent occurrence of incomplete data in profiling assays, often a consequence of experimental or financial constraints. For instance, in integrating various genomic data types, it is common to have complete genotype information for all individuals, but gene expression and/or methylation data are frequently incomplete [\[19\]](#page-24-8). Analyzing such incomplete omics data is challenging. Excluding samples with missing omics data significantly reduces sample sizes, particularly when integrating multiple omics layers, and imputing missing values can introduce bias and uncertainty[\[20,](#page-24-9) [21\]](#page-25-0). This underscores the critical need for computational techniques capable of directly modeling heterogeneous multi-omics datasets "as is", without requiring complete measurements or discarding useful information.

Advanced integrative methods to address the missing data issue can be classified into two categories: joint imputation or optimization masking approaches [\[22\]](#page-25-1). Joint imputation approaches [\[23–](#page-25-2)[25\]](#page-25-3) predict missing values within the modeling framework, but the accuracy of these imputed values, which may introduce bias, is crucial to the results. Also, these approaches often require larger sample sizes for effective model estimation. On the other hand, optimization masking techniques[\[8,](#page-23-9) [14,](#page-24-3) [26,](#page-25-4) [27\]](#page-25-5), which work with processed data such as patient graphs, allow partial samples to contribute by masking missing data during the optimization process. Such approaches also have their own limitations. Some require the presence of at least one common data view across partially observed samples, which may not always be feasible[\[8\]](#page-23-9). Others grapple with increased computational complexity and potential inaccuracies in clustering outcomes as the number or size of graphs increases [\[26,](#page-25-4) [27\]](#page-25-5).

Molecular subtypes identified through multi-omics integration offer essential diagnostic and prognostic insights. However, a major challenge in transitioning these integrative models to clinical practice lies in accurately classifying new patients into these predefined subtypes, particularly when dealing with incomplete omics data from these individuals[\[28\]](#page-25-6). This limitation significantly hinders the practical application of molecular subtypes in clinical settings, as patients often present with partial datasets that are not sufficiently addressed by current methodologies. The lack of robust computational approaches capable of making reliable predictions from these incomplete and diverse omics profiles is a critical barrier to the real-world clinical adoption of integrative models. Addressing this gap by developing methods that can infer accurate subtypes from any available data is essential for advancing personalized patient care and fully realizing the potential of multi-omics integration in medicine.

To overcome these limitations, we present IntegrAO (Integrate Any Omics), an unsupervised framework for integrating incomplete multi-omics profiles and classifying new samples with incomplete data. IntegrAO starts by integrating partially overlapped patient graphs derived from diverse omics data. Its unique partial graph fusion mechanism effectively enhances information integration with a high number of shared patients across modalities and adeptly adapts to situations with fewer overlapping samples. This capability allows IntegrAO to effectively combine diverse incomplete omics data, ensuring high fidelity and noise resistance. The framework then employs graph neural networks (GNNs) to extract and align patient embeddings from diverse raw omics features into a unified space. This unified embedding space is crucial for accurately classifying new patients into predefined subtypes using any available data, facilitating the transition to clinical practice. To demonstrate the use of IntegrAO, we first show IntegrAO exhibits robust integration of partially overlapping data across diverse missing data scenarios through simulation of omics dataset. A case study in acute myeloid leukemia then illustrates IntegrAO's capacity to build a comprehensive view of heterogeneity from incomplete multi-omics. Systematic evaluations conducted on five cancer cohorts, covering six omics modalities, underscore IntegrAO's resilience to missing data and its effectiveness in integrating partial data and classifying new samples. Through its proficient handling of heterogeneous and incomplete datasets, IntegrAO emerges as a significant tool in precision oncology, facilitating an all-encompassing approach to patient characterization.

# 2 Results

## 1 IntegrAO Overview

We present IntegrAO, an unsupervised framework for integrating multi-omics datasets with partial overlap. As outlined in Fig. [1a](#page-4-0), IntegrAO has two key functionalities: transductive integration and inductive prediction.

Transductive integration is structured around two core steps: (1) Fusion of partially overlapping patient graphs, (2) Unsupervised extraction and alignment of patient embeddings across omics modalities. In Step 1, IntegrAO is tailored to accommodate samples with missing data types. It first constructs a patient graph for each omic, with patients as nodes and weighted edges denoting pairwise similarities (Online Methods [4.2\)](#page-16-0). IntegrAO then fuses graphs through an iterative update process utilizing a nonlinear method rooted in message-passing theory (Online Methods [4.2\)](#page-16-1). Notably, IntegrAO enables partial graph fusion by leveraging shared samples between omics - more shared patients increase information fusion, while fewer dampen it. By using common samples as bridges, patients with partial omics also get updated, enriching the composite profiles. As the extent of patient overlap may vary across each pair of omics data modalities, IntegrAO performs pairwise fusion between graphs to maximize the information flow. Step 1 yields a fused graph for each omic, encapsulating integrated information from other omics. Step 2 extracts lowdimensional patient embeddings from each omic into a unified space (Online Methods [4.3\)](#page-18-0). The fused networks and omics data are fed into omic-specific graph neural network (GNN) encoders, then into a shared projection head to obtain embeddings per omic. The model training phase is designed to have the low-dimensional embeddings retraining similarity structures as the input fused graphs while simultaneously ensuring that embeddings of the same patients are aligned across different omics datasets. Final embeddings are obtained by averaging across omics to construct the integrated graph.

A key capability of IntegrAO is flexible transformation from unsupervised integration to supervised prediction (Fig. [1b](#page-4-0)). Taking cancer patient subtyping as an example, once subtypes are discerned from the integrated graph, IntegrAO can be further fine-tuned to enable subtype prediction for

![](_page_4_Figure_1.jpeg)
<!-- Image Description: This figure depicts a two-stage machine learning method for integrating multi-omics data. (a) Transductive integration fuses four omics datasets (mRNA, microRNA, copy number variation, DNA methylation) via graph fusion, then uses graph neural networks (GNNs) for embedding extraction and alignment, finally averaging embeddings to create an integrated representation. (b) Inductive prediction fine-tunes a model on the integrated network for subtype prediction and then predicts subtypes for new patients using their omics data and the trained model. The diagrams illustrate the data processing and model training steps. -->

<span id="page-4-0"></span>Fig. 1 Overview of the IntegrAO framework. (a) Step 1: Example representation of cell composition, mRNA expression, microRNA expression, DNA methylation and copy number variation datasets are used to construct per-omics patient graphs. Patient data need not encompass all omics types. Subsequently, a fusion phase iteratively refines each graph with information gathered from other graphs, culminating in a unified graph for each type of omics. Step 2: Both these unified graphs and their corresponding omics features are input into omics-specific Graph Neural Networks (GNNs) to learn patient embeddings. These lowdimensional patient embeddings are optimized to retain similarity information from the individual unified graphs while minimizing differences in embeddings for the same patients across different omics. Step 3: The conclusive embeddings are procured by averaging omicsspecific embeddings and applied in the construction of the final integrated patient graph. (b) Conversion of IntegrAO into a predictive framework. Utilizing the integrated graph, patient subtypes can be identified and leveraged to fine-tune the trained IntegrAO model. The finetuned IntegrAO model enables the classification of new patients with any accessible omics data. During the inference process, graph fusion is first conducted on new patients along with existing patients. The consequent fused graph and associated omics features are then input into the fine-tuned IntegrAO model, allowing for the prediction of patient subtypes.

new patients using any available omics data (Online Methods [4.4\)](#page-20-0). The distinction between the prediction model and the unsupervised-training model lies in the added Multi-layer Perceptron(MLP) prediction head, which enables the processing of the averaged patient embeddings across omics for subtype prediction. While the prediction model inherits its initial weights from the unsupervised-training model, the MLP prediction head starts with a random weight initialization. Fine-tuning balances two key objectives: preserving the unsupervised objectives of patient embedding generation, and minimizing subtype classification loss. This dual optimization enables the model to support subtype prediction in a modality-agnostic manner. During the inference process, given any combination of multi-omic data for new patients, the first step involves fusing these new patients into existing graphs. Following this fusion, the fine-tuned model accepts the fused graphs along with the corresponding omics features, allowing IntegrAO to predict specific cancer subtypes (Online Methods [4.4\)](#page-21-0).

## 2 Simulation: IntegrAO exhibits robust integration of partially overlapping data across diverse missing data scenarios

We first evaluated IntegrAO using a simulated multi-omics dataset generated by the InterSim CRAN package [\[29\]](#page-25-7), which produces data for three omics modalities (DNA methylation, mRNA expression, and protein expression). We simulated a total of 500 samples with 15 clusters, and each cluster have variable random sizes (Online Methods [4.1\)](#page-15-0). IntegrAO was compared to two related network-based methods capable of handling partial overlap, NEighborhood-based Multi-Omics clustering (NEMO)[\[8\]](#page-23-9) and Multiple Similarity Network Embedding (MSNE)[\[26\]](#page-25-4), using Normalized Mutual Information (NMI) to assess clustering congruence with ground truth labels. NEMO and MSNE were run using their default settings and hyperparameters. We first tested the scenarios where one omic modality remains intact and two other modalities undergo uniform random subsampling at ratios from 0.1 to 0.9 (Fig. [2a](#page-6-0)). The random sub-sampling process was repeated 10 times for each overlapping ratio.

In integration scenarios with partial overlap, two regimes emerge: low overlap, where the goal is to minimize inter-modality influence due to potential noise from limited shared samples, and high overlap, where the objective is to maximize information flow between modalities as the increased common samples enable more reliable integration between modalities. IntegrAO substantially outperformed other methods across all overlap ratios and maintained robust performance even in low-overlap situations where MSNE faltered (Fig. [2a](#page-6-0)). In the latter scenario, MSNE's performance can decline when integrating more data, sometimes falling below baseline levels established by K-means clustering on the intact modality, highlighting its limitations in handling low data overlap with noise signals from other modalities. We subsequently evaluated a more complex experimental setup in which no omic data modality remained intact. In this experiment, we first selected a subset of common samples based on the specified overlapping ratio, then evenly distributed the remaining samples among the three modalities as unique entities. We observed enhanced clustering performance in all three methods as the overlapping ratios increased. IntegrAO consistently outperformed other methods, maintaining effective clustering even at a minimal 10% overlap (Fig. [2b](#page-6-0)). The superior performance of IntegrAO can be attributed to its ability to fuse unique samples even just with their individual modality, in contrast to NEMO, which requires samples to be observed in at least one common view with others. This distinction highlights

![](_page_6_Figure_1.jpeg)
<!-- Image Description: This figure displays the performance of four multi-omics integration methods (IntegrAO, NEMO, MSNE, and k-means) across various data scenarios. Panels (a) show NMI scores for different overlapping ratios of intact and missing omics data. Panel (b) shows NMI scores when all omics data is missing. Panel (c) is a Venn diagram illustrating the overlap of samples across mRNA, protein, and methylation data. Finally, panel (e) shows UMAP visualizations of integrated and individual omics data embeddings, representing sample relationships. The figure demonstrates the effectiveness of each integration method and the impact of data completeness on performance. -->

<span id="page-6-0"></span>Fig. 2 Benchmarking partial multi-omics integration between IntegrAO, NEMO, and MSNE on simulated multi-omics cancer dataset using Normalized Mutual Information (NMI). (a) NMI versus overlapping data ratio across three missing scenarios (n=10 experiments for each ratio). Means of evaluation metrics with standard deviations from different experiments are shown in the figure, where the error bar represents plus/minus one standard deviation. From left to right: Uniform random subsampling of DNA methylation and protein expression with intact mRNA expression; Uniform random subsampling of mRNA expression and DNA methylation with intact protein expression; Uniform random subsampling of mRNA expression and protein expression with intact DNA methylation. IntegrAO demonstrates superior performance in all scenarios. (b) IntegrAO outperforms other methods in a more challenging scenario where all omic data are partially missing. (c) An illustrative example with a 70% data overlap ratio, showing 350 common and 50 unique samples per modality. (d) Pre-integration UMAP visualizations for each modality for the 70% all-missing data scenario, highlighting both common and unique samples. (e) Post-integration UMAP visualization of patient embeddings via IntegrAO. Upon integration, clustering resolution was enhanced with unique samples from each network showing improved alignment.

IntegrAO's proficiency in utilizing unique and incomplete datasets, effectively extracting valuable information where other methods may fall short.

To further investigate IntegrAO's integration effectiveness, we conducted a detailed visual analysis on a 70% overlap scenario with 350 shared samples and 50 unique samples per modality (Fig. [2c](#page-6-0)). We generated UMAP visualizations for each omic type prior to integration. In these visualizations, dots represented shared samples, while diamonds, squares, and triangles indicated unique samples of mRNA, protein, and DNA methylation, respectively (Fig. [2d](#page-6-0)). Pre-integration, the embeddings displayed an entangled structure with randomly dispersed unique samples. In contrast, following IntegrAO integration, the UMAP shows clearly defined clustering of the 15 clusters, with coherent grouping of unique samples (Fig. [2e](#page-6-0)). This highlights IntegrAO's ability to disentangle complex mixed signals and uncover integrated structures through joint analysis of distinct but partially overlapping datasets.

## 3 IntegrAO identifies fine-grained clinically and biologically distinct AML subtypes

To elucidate heterogeneity in acute myeloid leukemia (AML), a cancer marked by extensive inter-patient and intra-patient heterogeneity, we applied IntegrAO to an empirical AML dataset. Recently, a new layer of heterogeneity has been identified in AML corresponding to the composition of each patient's leukemia cell hierarchy[\[30\]](#page-25-8), providing new insights into disease biology and drug response. We sought to utilize IntegrAO to integrate this new information with two other modalities, mRNA expression and DNA methylation, to achieve an unprecedented multi-dimensional perspective on AML heterogeneity. We thus applied IntegrAO to three AML cohorts, TCGA, BEAT-AML[\[31\]](#page-25-9), and Leucegene[\[32\]](#page-26-0), leveraging mRNA expression and hierarchy composition for 812 patients, and methylation profiles from 308 patients of those patients (Online Methods [4.1\)](#page-15-0).

IntegrAO integration of mRNA, DNA methylation, and cell hierarchy data revealed 12 biologically distinct AML subtypes (Online Methods [4.5\)](#page-21-1), exhibiting unique multi-omics patterns that provide a refined resolution of heterogeneity, as shown in Fig. [3a](#page-8-0) and Supplementary Fig. S1. Notably, the subtypes refine broader groupings defined previously using only the hierarchy data by Zeng et al[\[30\]](#page-25-8), validating IntegrAO's capacity to extract nuanced diversity. Detailed examination of cell compositions supports this, with 'Primitive' subtypes enriched for primitive leukemia stem and progenitor cells (LSPCs), 't8;21/CEBPA' and 'APL' enriched for GMP-like cells, and 'Mature' subtypes for Mono-like and cDC-like cells. Despite similar compositions, the two 'Primitive' subtypes are differentiated by distinct mutations - 'Primitive (NPM1)' associated with NPM1/FLT3-ITD alterations, 'Primitive (Canonical)' with TP53/RUNX1. Further heterogeneity is observed in the four NPM1-driven subtypes with divergent hierarchies. Notably, a novel subtype emerged dominated by erythroid progenitor (EryP) cells, a finding that diverges from conventional understanding and may inform future

![](_page_8_Figure_1.jpeg)
<!-- Image Description: This image displays multi-omics analysis of acute myeloid leukemia (AML). Panel (a) shows hierarchical clustering of AML samples based on transcriptomic and genomic data, revealing distinct subtypes. Panel (b) presents heatmaps illustrating the biological and metabolic pathway enrichment in these subtypes. Panel (c) shows Kaplan-Meier survival curves and box plots demonstrating the clinical relevance of these subtypes in terms of survival outcomes and drug sensitivity. Panel (d) uses UMAP plots to visualize the distribution of AML samples within each subtype, providing a spatial representation of the data. The overall purpose is to demonstrate a novel classification of AML subtypes based on integrated genomic and transcriptomic profiling, showing their biological and clinical implications. -->

<span id="page-8-0"></span>Fig. 3 Multi-omics integrative analysis of acute myeloid leukemia (AML) elucidating intertumor heterogeneity. (a) IntegrAO discerns 12 subtypes with distinct hierarchical composition, transcriptomic profiles, and mutational patterns, preserving granular differentiations. (b) IntegrAO subtypes demonstrate greater differential survival versus individual datasets. (c) More significantly sensitive drugs are revealed by IntegrAO versus single data types. (d) Hematopoietic lineage enrichment analysis validates subtype differentiation, underscoring captured heterogeneity.

AML research directions. These granular insights highlight IntegrAO's effectiveness in eliciting nuanced biology underlying AML diversity, potentially informing tailored therapeutic strategies. Furthermore, the heatmaps derived from Gene Ontology (GO) analysis of biological and metabolic pathways closely mirror the subtypes identified by IntegrAO, highlighting their biological significance and uniqueness (Fig. [3b](#page-8-0)). In the GO biological pathways heatmap, distinct segments correspond to specific subtypes, reflecting dominant biological processes such as cellular functions, regulatory mechanisms, and interaction pathways. Likewise, the GO metabolic pathways heatmap clearly segments into areas representing key metabolic activities, including glycolysis, lipid metabolism, and energy production, characteristic of these clusters. Additionally, we conducted VIPER analyses on both all regulons and transcription factor-specific regulons, with the resulting heatmaps demonstrating distinct block structures that align well with the clusters defined by IntegrAO (Supplementary Figs. S2-3). Collectively, these results further emphasize the biological distinctness of the subtypes identified by IntegrAO.

We further assessed the clinical importance of the subtypes through survival analysis and drug sensitivity profiling. Kaplan-Meier survival curves for the clusters, drawn from the combined TCGA and BEAT-AML cohort, showed significant differences (multi-group logrank test p-value = 1.21e-7) (Fig. [3c](#page-8-0)). Separate analysis of TCGA and BEAT-AML data also revealed significant survival distinctions (Supplementary Figs. S4a,b). We also conducted nested likelihood ratio tests to determine whether the addition of subtype clustering enhances prognostic stratification beyond four established factors (age, cytogenetic risk, white blood cell count, and NPM1 mutation). Compared to subtypes identified using only mRNA or cell hierarchy data, IntegrAO subtypes showed greater multivariate prognostic significance (p-value=0.01425), while subtypes from individual data types did not demonstrate significant improvement (p¿0.05) (Supplementary Fig. S4c). For drug sensitivity, ANOVA tests were used to assess whether IntegrAO subtypes show differential responses to each of 122 anti-cancer agents in the BEAT AML drug screening dataset (Fig. [3c](#page-8-0)). A differential response was indicated by an ANOVA p-value ¡ 0.05. The analysis revealed that 47 out of the 122 drugs showed differential sensitivity in IntegrAO clusters, affirming their clinical utility (Supplementary Fig. S5).

To validate the heterogeneity captured in the IntegrAO AML subtypes, we evaluated the enrichment along defined stages of hematopoietic differentiation in each defined subtype (Fig [3d](#page-8-0)). As a reference, we utilized the single-cell UMAP of bone marrow mononuclear cells from Galen et al[\[33\]](#page-26-1), providing an unbiased landscape of normal hematopoietic differentiation (Supplementary Fig. S6). We then mapped the specific populations most enriched in each IntegrAO subtype onto this independent reference. Notably, this revealed alignments including the 'Dendritic' subtype with plasmacytoid and conventional dendritic cells, 'Primitive (Canonical)' with hematopoietic stem cells, and 'Mature Mono (NPM1)' with monocytes, etc. The orthogonal validation that IntegrAO subtypes align with varying normal developmental trajectories highlights that IntegrAO integration preserves, and does not smooth over, the heterogeneous lineages underlying AML intertumor heterogeneity.

In summary, IntegrAO integration of complete and incomplete AML data effectively identifies distinct subtypes with biological and clinical relevance. By effectively sharing information yet preserving essential distinctions between omics, IntegrAO offers a comprehensive insight into cancer complexity, furthering biological discovery and precision medicine. IntegrAO's development of such detailed patient stratification that correlates with clinical outcomes and

biological underpinnings demonstrates its potential in guiding individualized therapeutic decisions, especially in complex conditions like AML.

## 4 A Pan-Cancer Evaluation of IntegrAO on identifying clinically distinct subtypes

To further evaluate the efficacy of partial multi-omics integration, a comparative analysis was conducted between IntegrAO, NEMO, and MSEN across five distinct cancer datasets sourced from The Cancer Genome Atlas (TCGA)[\[5\]](#page-23-4). For each cancer type, we leveraged the maximum number of patients in each of the five omics: mRNA expression, DNA methylation, miRNA expression, Reverse-phase protein array, and copy-number variation. By utilizing all possible samples from TCGA, this benchmark dataset encompasses rich, heterogeneous profiles without data waste. Recently, cell composition derived from deconvolving bulk mRNA expression data has emerged as a critical modality for the delineation of disease subtypes and the tailoring of therapeutic strategies. Uniquely, we additionally incorporated cell type composition, as an extra modality to enhance heterogeneity characterization (Online Methods [4.6\)](#page-22-0). The details of data collection and preprocessing can be found in Online Methods [4.1.](#page-15-0) The respective patient counts and feature counts for each modality are detailed in Supplementary Tables S1-2. As the integration of additional modalities progresses, acquiring a sufficient number of common samples across all views becomes increasingly challenging. Consequently, the ability to integrate partial omics datasets is essential, allowing for the efficient utilization of all existing data without squandering valuable information.

To evaluate the effectiveness of a given clustering solution, two specific metrics were employed. First, age-adjusted differential survival between the resultant clusters was measured using the logrank test. This method operates on the premise that clusters with significant differences in survival rates reflect biologically meaningful variations. Subsequently, we examined the enrichment of six clinical labels within the clusters, including gender, age at diagnosis, pathologic T (tumor progression), pathologic M (metastases), pathologic N (cancer in lymph nodes), and pathologic stage (total progression). Enrichment for discrete parameters was assessed using the χ 2 test for independence, while numeric parameters were evaluated using the Kruskal-Wallis test. Recognizing the absence of a definitive ground truth for the number of clusters pertaining to each cancer type, we executed clustering for a range of cluster numbers from 3 to 8. Fig. [4](#page-11-0) illustrates the comparative performance of IntegrAO against other methods across various cancer datasets.

Overall, IntegrAO reliably identified subtypes with both superior survival differentiation and clinical variable enrichment across cancer cohorts. In BRCA, KIRC, and SKCM, IntegrAO solutions were clearly favorable considering both criteria. In LUAD, IntegrAO achieved significantly better clinical enrichment despite comparable survival differentiation to MSNE. And for COAD, IntegrAO showed better survival stratification amongst methods despite suboptimal clinical enrichment results. In contrast, NEMO and

![](_page_11_Figure_1.jpeg)
<!-- Image Description: The image displays six scatter plots, each representing a different cancer type (BRCA, KIRC, LUAD, SKCM, COAD). Each point represents a cluster of samples, categorized by three methods (IntegraAO, NEMO, MSNE), and colored accordingly. The x-axis in the bottom plots shows the negative log10 of survival p-values, while the y-axis shows the number of enriched clinical parameters. The plots illustrate the relationship between survival p-values, number of enriched clinical parameters, clustering method, and cancer type. -->

<span id="page-11-0"></span>Fig. 4 Comparative analysis of IntegrAO, NEMO, and MSNE across 5 cancer types with partial multi-omics data. The x-axis depicts differential survival between clusters, quantified by -log10 of the P-value from age-adjusted nested log-rank testing (higher indicates greater survival differentiation). The y-axis shows the number of enriched clinical parameters within clusters (higher denotes more parameters enriched). Each plot compares methods for a cancer dataset for different cluster numbers. Overall, IntegrAO more reliably identifies clusters with both better survival differentiation and higher clinical enrichment than other methods.

MSNE demonstrated inconsistent performance across cancer types. MSNE delivered satisfactory results in COAD, yet its performance was less convincing in KIRC and SKCM. Meanwhile, NEMO showcased a strong performance in BRCA, but this did not extend to COAD or LUAD. Furthermore, the uneven ability of MSNE in discerning survival differences—evident in BRCA but absent in KIRC and SKCM—alongside NEMO's variable success in pinpointing clinically enriched variables, with success in BRCA but not in COAD or LUAD, highlights a significant shortfall. IntegrAO proficiently discerned both criteria, reflecting robust integration and patient stratification. This inconsistency among the other methods underscores the intricate challenge of integrating diverse partial multi-omics data, which also underscores IntegrAO's importance for translational applications requiring holistic patient characterization.

## 5 IntegrAO enables robust new patient classification using incomplete omic-data

In clinical applications, after discerning patient subtypes, categorizing new patients into predefined clusters is often needed but overlooked by many methods. This task is more complex when new patients possess only partial omics

![](_page_12_Figure_1.jpeg)
<!-- Image Description: The image displays 15 line plots arranged in a 5x3 grid. Each row represents a different cancer type (BRCA, KIRC, LUAD, SKCM, COAD). Each plot shows the accuracy, F1-macro, and F1-weighted scores for six machine learning models (IntegrAO, MLP, SVM, XGBoost, Random Forest, KNN) trained on different combinations of genomic data (all, miRNA, methylation, miRNA+methylation, miRNA+mRNA, mRNA). The plots compare model performance across data types, revealing the impact of data integration on cancer classification accuracy. Error bars represent variability. -->

<span id="page-12-0"></span>Fig. 5 Performance comparison of new patient classification using IntegrAO versus MLP, SVM, XGBoost, Random Forest, and KNN under different omic combinations. Accuracy, F1-macro, and F1-weighted were evaluated, with means and standard deviations from multiple experiments displayed (error bars denote ±1 standard deviation). mRNA, meth, and miRNA refer to single-omic classification using mRNA expression, DNA methylation, and miRNA expression data respectively. miRNA+meth, miRNA+mRNA, and meth+mRNA indicate classification with two omics, while "all" used all three data types. Across all metrics and inputs, IntegrAO substantially outperforms other methods, highlighting its ability to effectively leverage diverse omics for integrative patient classification.

data. Thus, methodologies that can classify new samples lacking comprehensive features are critical. IntegrAO enables new patient classification into established subtypes using any available omics data. This key functionality addresses an important unmet need for translating integrative methods into precision medicine applications.

To rigorously assess IntegrAO's proficiency in classifying new patients, we designed an experimental framework that mimics the real-world scenario of assigning unseen samples to predefined subtypes. We benchmarked IntegrAO against five widely-used classifiers: Multi-layer Perceptron (MLP), Support

Vector Machine (SVM), Random Forest, XGBoost, and K-Nearest Neighbors (KNN). Our ground truth dataset was derived from comprehensive multi-omics data, including miRNA, mRNA, and DNA methylation profiles from the five TCGA cancer cohorts, selecting only patients with a full set of data across these modalities. IntegrAO was employed to integrate the complete dataset to construct an integrated network, which was then used to determine the optimal number of clusters and generate cluster labels via spectral clustering (Online Methods [4.5](#page-21-1) and Supplementary Fig. S7). The optimal number of clusters for each cancer type is listed in Supplementary Table S3. This full cohort was then utilized in a rigorous stratified 10-fold cross-validation procedure. In each fold, the methods were trained on 90% of samples and subsequently tested on the held-out 10% of unseen samples. To assess multi-class prediction performance, accuracy, F1-macro, and F1-weighted were measured as key evaluation metrics. For each dataset, IntegrAO first conducted unsupervised integration on the 90% training samples to discern subtypes, then refined the model using the known "ground truth" labels, and finally employed the fine-tuned model to predict the subtype of the unseen test samples using any combination of the omics data. In contrast, the other methods were trained on either single omics or direct concatenated multi-omics data from the 90% subset, and evaluated on their ability to correctly predict the subtypes of the 10% held-out test set.

IntegrAO consistently and substantially outperformed all comparative classification methods across every new patient projection task, as quantified by accuracy, F1-macro, and F1-weighted metrics (Fig. [5](#page-12-0)). In particular, IntegrAO demonstrated clearly superior performance, while KNN was notably the least effective, and the remaining algorithms exhibited intermediate but significantly inferior accuracy compared to IntegrAO. Further analysis revealed that IntegrAO's classification performance was highly robust across diverse omic combinations, whereas other methods displayed pronounced fluctuation and instability when missing certain data modalities. This instability arises because specific integrated omics can be highly noisy or misleading for overall subtyping. Classifying new patients with only that noisy modality is then extremely challenging to accurately map into the defined subtypes. IntegrAO overcomes this by embedding different omic features into a unified space, enabling it to approximate the classification accuracy of full multi-omics datasets even with incomplete data. This feature holds significant clinical importance, as physicians frequently face the challenge of making diagnostic or treatment decisions with only partial omic information available. By effectively bridging this gap, IntegrAO emerges as a pivotal tool that enhances the application of multiomics approaches in the practical landscape of precision medicine, facilitating better-informed clinical decisions.

# 3 Discussion

This study presents IntegrAO, an integrative framework designed to tackle key challenges in multi-omics analysis - handling incomplete heterogeneous data and projecting new samples using partial profiles. The results validate IntegrAO's ability to integrate diverse cancer datasets with missing modalities and to classify new patients reliably. Tests with simulated cancer omics data reveal IntegrAO's capability to integrate missing data in various scenarios, showing resilience to noise at low data overlaps and effective integration at higher overlaps. In the case study on acute myeloid leukemia, IntegrAO successfully combined cell hierarchy composition, transcriptomics, and DNA methylation, identifying 12 clinically and biologically distinct subtypes and illustrating AML's heterogeneity. Systematic evaluations across five cancer cohorts, encompassing six omics modalities, show IntegrAO's superiority in identifying significant subtypes compared to other methods. Its consistent performance in projecting new samples, regardless of the number of available omics, highlights its potential in modality-agnostic inference and unified patient representation.

IntegrAO stands out in its ability to handle varied and incomplete data sets, establishing itself as a pivotal tool for the future of precision medicine. Its architecture is specifically tailored to not only accommodate but also to synergize disparate data types, thereby maximizing the utility of every available data point. This aspect is particularly crucial in clinical settings, where data availability can often be unpredictable and inconsistent. IntegrAO's ability to integrate these disparate data into a unified space represents a significant advancement in patient care. Furthermore, IntegrAO's ability to predict outcomes from new and incomplete samples lays the groundwork for the practical application of integrative models in clinical settings, including diagnosis and personalized treatment. Through these capabilities, IntegrAO is revolutionizing the creation and use of comprehensive patient databases. It enables a more nuanced understanding of cancer and facilitates a seamless transition of these insights into clinical practice.

This research lays the foundation for several crucial future developments to enhance IntegrAO into a robust, scalable, and broadly applicable integrative framework. A key step is transforming the graph fusion process into an end-to-end deep neural network, critical for enhancing scalability and flexibility when analyzing massive biomedical datasets. Additionally, incorporating diverse data types, such as histopathology images, clinical notes, and sensor data, will allow for more detailed profiling and subtyping. Moreover, potential areas of application extend beyond cancer patient stratification to cell subtyping, drug discovery, biomarker identification, and precision nutrition. Conducting thorough evaluations across various applications, alongside efforts to enhance model interpretability, is crucial for showcasing IntegrAO's utility and reliability in various biomedical domains. By pushing boundaries on multiple fronts, this work paves the way for positioning IntegrAO as a crucial model for the future of precision medicine.

# 4 Methods

## <span id="page-15-0"></span>4.1 Data Preprocessing

### Simulated cancer omics datasets

We utilized the InterSim CRAN package[\[29\]](#page-25-7) to simulate cancer omics datasets, generating a total of 500 samples distributed across 15 clusters of varying sizes, reflecting realistic clinical scenarios. For the hyperparameters, we set 'effect=0.1' and 'p.DMP=0.1', while keeping the rest of the hyperparameters at their default values.

### TCGA cancer datasets

For the cancer datasets, we leveraged multi-omic data across five tumor types from The Cancer Genome Atlas (TCGA) - breast invasive carcinoma (BRCA), colon adenocarcinoma (COAD), skin cutaneous melanoma (SKCM), kidney renal clear cell carcinoma (KIRC), and lung adenocarcinoma (LUAD). Specifically, we obtained mRNA expression, DNA methylation, copy number variation, and protein expression data directly from cBioportal. MicroRNA expression data was retrieved separately from the Broad Institute's Firehose source data. Relevant clinical information was also acquired for each patient. Before analysis, rigorous preprocessing was performed, including outlier removal, imputation of missing values via k-nearest neighbors (kNN), and normalization by standard scaling to mean 0 and standard deviation 1. Patients with over 20% missing data for any data type and features with over 20% missing values across patients were excluded. We additionally selected the top 2,000 features exhibiting the greatest standard deviation from each data modality. For modalities with fewer than 2,000 total features, no feature filtering was performed.

#### AML cancer dataset

To construct an integrated AML dataset for heterogeneous analysis, we merged raw data from the TCGA, BEAT-AML, and Leucegene cohorts. Gene expression data normalization was performed using a variance-stabilizing transformation for each each dataset. Batch effects were then corrected with the One Cell at A Time (OCAT)[\[34\]](#page-26-2) algorithm, which also reduced the features to a 30-dimensional space. For cell composition, we employed bulk gene expression deconvolution following Zeng et al.[\[30\]](#page-25-8), applying OCAT for subsequent feature reduction. DNA methylation data, exclusive to the TCGA cohort, required no batch correction, and we selected 2,000 highly variable features based on dispersion. The final dataset included 812 AML patients with cell hierarchy composition and mRNA expression data, and a subset of 308 patients with additional DNA methylation data.

### <span id="page-16-0"></span>4.2 Transductive Integration - Graph fusion

The first step of IntegrAO's transductive integration is the fusion of partially overlapping patient graphs. The subsequent section details the construction of these patient graphs and their partial overlap fusion. This graph fusion approach builds upon our prior work, Similarity Network Fusion (SNF)[\[7\]](#page-23-6).

#### Patient graph construction

We first construct a patient graph for each omic. Each graph can be represented as G = (V, E), with vertices V correspond to the patients {x1, x2, ..., xn} and undirected weighted edges E denote the affinity between patients. The weight of the edge is computed with:

<span id="page-16-2"></span>
$$
W(i,j) = \exp\left(\frac{\rho^2(x_i, x_j)}{\mu \varepsilon_{i,j}}\right),\tag{1}
$$

where ρ(x<sup>i</sup> , x<sup>j</sup> ) is the Euclidean distance between patients x<sup>i</sup> and x<sup>j</sup> . µ is a hyperparameter that is recommended setting in the range of [0.3, 0.8]. εi,j is defined as

$$
\varepsilon(i,j) = \frac{1}{3} \cdot \left( \frac{1}{|N_i|} \sum_{k \in N_i} \rho(x_i, x_k) + \frac{1}{|N_j|} \sum_{l \in N_j} \rho(x_j, x_l) + \rho(x_i, x_j) \right), \quad (2)
$$

where N<sup>i</sup> is the set of x<sup>i</sup> 's neighbor including x<sup>i</sup> in G. We then performed two operations on each graph to derive the transition probability matrix for the graph fusion stage: the first is normalizing the affinity matrix for numerical stability:

<span id="page-16-3"></span>
$$
P(i,j) = \begin{cases} \frac{W(i,j)}{2\sum_{k \neq i} W(i,k)}, & i \neq j \\ 1/2, & i = j \end{cases}
$$
 (3)

And the second is obtaining the local affinity matrix by considering only the K most similar patients per patient:

<span id="page-16-4"></span>
$$
S(i,j) = \begin{cases} \frac{W(i,j)}{\sum_{k \in N_i} W(i,k)}, & j \in N_i \\ 0, & \text{otherwise} \end{cases}
$$
 (4)

Given v different data modalities, we can construct affinity matrices W(m) using Eq. [1](#page-16-2) for the mth view, m = 1,2,..., v. P (m) and S (m) are obtained from Eq. [3](#page-16-3) and [4](#page-16-4) respectively.

#### <span id="page-16-1"></span>Partial overlap graph fusion

In the case of two modalities with partially overlapping patient sets, i.e., v = 2, let a, b denote the total number of patients for each modality, respectively, and c the number of common patients. Let C denote the set of common patients. The transition probability matrices P (1) ∈ R <sup>a</sup>×<sup>a</sup> and P (2) ∈ R b×b , and local affinity matrices S (1) ∈ R <sup>a</sup>×<sup>a</sup> and S (2) ∈ R <sup>b</sup>×<sup>b</sup> are constructed as described previously. During fusion, each modality patient graph is initialized to its P matrix (P (1) <sup>t</sup>=0 = P (1); P (2) <sup>t</sup>=0 = P (2)). The key concept for fusing such partially overlapped data is to leverage the common samples to propagate information across the graphs via graph fusion. IntegrAO iteratively updates the patient graph for each data modality as follows:

<span id="page-17-0"></span>
$$
P_{t+1}^{(1)} = S^{(1)} \times P_t^{'(2 \to 1)} \times (S^{(1)})^T, \tag{5}
$$

<span id="page-17-1"></span>
$$
P_{t+1}^{(2)} = S^{(2)} \times P_t^{'(1 \to 2)} \times (S^{(2)})^T, \tag{6}
$$

where the intermediate transition matrices P ′ (2−→1) <sup>t</sup> and P ′ (1−→2) t is obtained by first getting the affinity weights from the other modality of the common samples, as:

$$
W_t^{'(2 \to 1)}(i,j) = \begin{cases} P_t^{(2)}(i,j), & i,j \in C \\ 0, & \text{otherwise} \end{cases}
$$
 (7)

$$
W_t^{'(1\rightarrow 2)}(i,j) = \begin{cases} P_t^{(1)}(i,j), & i,j \in C \\ 0, & \text{otherwise} \end{cases}
$$
 (8)

Then we apply a novel scaling normalization:

$$
P'_{t}(i,j) = \begin{cases} \frac{W'_{t}(i,j)}{2\sum_{k\neq i} W'_{t}(i,k)} \cdot \tau, & i \neq j \\ 1 - 1/2 \cdot \tau, & i = j \\ c \end{cases}
$$
 (9)

τ = number of sample in the current network .

During the iterative updates, each modality utilizes the shared patients' transition matrix from the other modality for fusion. The scaling normalization helps minimize the impact of the other modality when few patients are shared, while maximizing information flow when many patients are common. Not only the common patients' similarities can get updated through graph fusion, but the unique patients can also leverage the affinity information of the common patients from other modalities to learn more robust affinity for their own patient graph. This procedure updates the transition matrices each time generating two parallel interchanging fusion processes. After each iteration, we performed normalization on P (1) <sup>t</sup>+1 and P (2) <sup>t</sup>+1 as in Eq. [3,](#page-16-3) for the following three reasons: (i) ensure a patient is always most similar to themself than to other patients; (ii) ensure the final graph is full rank; (iii) for quicker convergence of fusion. After t steps, we obtain the fused patient graph for each modality.

As our fusion approach leverages shared patients between modalities, the number of common patients may decrease when integrating more than two data types (v > 2). To address this, we perform pairwise fusion for multi-modalities following Eq. [5](#page-17-0) and [6:](#page-17-1)

$$
P^{(m)} = \frac{\sum_{k \neq m} (S^{(m)} \times P^{'(k)} \times (S^{(m)})^T)}{v - 1}, m = 1, 2, ..., v.
$$
 (10)

Since the sample size differs across modalities, the fused affinity matrices for each data type retain the original dimensionality. The subsequent step involves integrating these modal-specific graphs into a unified representation, which will be detailed in the following section.

## <span id="page-18-0"></span>4.3 Transductive Integration - Embedding extraction and alignment

The second step of IntegrAO's transductive integration is unsupervised extraction and alignment of patient embeddings across omics modalities. This embedding step fulfills two critical goals: (i) deriving low-dimensional embeddings that maintain the affinity structure of the fused graphs for each data type, and (ii) aligning embeddings for the same patient across modalities.

### Model architechture

The deep learning model in IntegrAO consists of two key components: (1) Omic-specific graph encoders to extract patient embeddings within each data modality, (2) Shared projection layers to map the embeddings from different omics into a common latent space. For each omic-specific GNN encoder, inspired by GraphSAGE[\[35\]](#page-26-3), instead of training individual embeddings for each node, we learn an aggregating function that generates embeddings by aggregating features from a node's local neighborhood. This enables generating embeddings for unseen nodes using the learned functions given their local neighborhood is provided.

Using the fused patient graphs, we obtain sparse affinity matrices per omic by considering only the K most connected neighbors of each patient node as defined in Eq. [4.](#page-16-4) The weighted graphs are converted to unweighted versions as inputs to the encoders. Formally, let G = (V, E) denote the unweighted patient networks, where V are the nodes (patients) and E are the edge connections (patient links). The update rule for a node representation on the k th encoder layer is defined as:

$$
h_v^{(k)} = \sigma \left( W_1^{(k)} \cdot h_v^{(k-1)} + W_2^{(k)} \cdot \text{MEAN}(\{ h_u^{(k-1)} \mid u \in N(v) \}) \right), \tag{11}
$$

where h (k) <sup>v</sup> is the representation of node v at the k layer and N(v) denotes the set of neighbours of node v, MEAN refers to the average operation. W (k) 1 and W (k) 2 are two learnable weight matrix. Notably, we use the original features from each omic as the input to the first GNN layer. We set the number of layers to be 2 for each GNN encoder. Lastly, the shared projection layers comprise stacked MLP layers which ingest the node representations from the final GNN layer and output the final patient embedding ev:

$$
e_v = \text{MLP}(h_v^{(N)}). \tag{12}
$$

#### Learning objective

For better illustration, again consider the integration of two distinct data modalities: X(1) ∈ R <sup>n</sup>x1×dx<sup>1</sup> and X(2) ∈ R nx2×dx<sup>2</sup> . In the IntegrAO embedding phase, our objective is to map these datasets into a unified embedding space of dimensionality q. The resultant lower-dimensional datasets are represented as X(1) ′ ∈ R <sup>n</sup>x1×<sup>q</sup> and X(2) ′ ∈ R nx2×q . This embedding is achieved by optimizing two distinct loss functions: the reconstruction loss Lreconc and the alignment loss Lalign. The reconstruction loss Lreconc is conceptualized on the principles of t-distribution stochastic neighbor embedding (t-SNE)[\[36\]](#page-26-4) and can be formally defined as:

$$
L_{\text{reconc}} = \text{KL}(P^{(1)} \mid \mid Q^{(1)}) + \text{KL}(P^{(2)} \mid \mid Q^{(2)}), \tag{13}
$$

where P (1) and P (2) are the fused patient graphs obtained during the fusion stage with diagonal values set to 0. And Q(1) and Q(2), constrained to tdistribution, are the sample-to-sample transition probability matrix calculated using the low-dimensional embedding X(1) ′ and X(2) ′ . The Kullback-Leibler (KL) divergences is defined as:

$$
KL(P || Q) = \sum_{i} \sum_{j} P_{ij} \log \frac{P_{ij}}{Q_{ij}}.
$$
\n(14)

The alignment loss Lalign quantifies the mean squared error between embeddings of the same patients derived from different omics modalities. It is defined as:

$$
L_{\text{align}} = \frac{1}{n} \sum_{i=1}^{c} \mathbb{1}(i \in \mathbf{C}) (X_i^{(1)'} - X_i^{(2)'})^2,
$$
\n(15)

where C denotes the set of common samples between the two modalities. The final loss is the combination of reconstruction loss and alignment loss as:

$$
Loss = L_{\text{reconc}} + \beta \times L_{\text{align}},\tag{16}
$$

where β is a tradeoff parameter to balance the KL terms and the embedding alignment term. We set β=1 in all our experiments. The model can be readily extended to multi-view data by adding additional KL divergence terms to the reconstruction loss for each added view, and summing all pairwise alignment losses between modalities for the matching loss. We solve the optimization problem using gradient descent with a fixed number of epochs. We set epoch=1000 in all our experiments.

#### Model output

After training, the final output is derived by averaging patient embeddings across modalities. Let M(i) denote the omic types available for patient i, then the final patient embeddings E(i) for patient i are obtained by:

$$
E(i) = \frac{1}{|M(i)|} \sum_{m \in M(i)} e_i^{(m)},
$$
\n(17)

where e (m) i is the embedding for patient i from modality m. The final integrated network is then computed using Eq. [1](#page-16-2) followed by Eq. [3,](#page-16-3) taking the final patient embeddings as input.

### <span id="page-20-0"></span>4.4 Inductive Prediction

#### Model fine-tuning for subtype prediction

After unsupervised integration of multi-omics data, patient subtypes can be determined by clustering the final integrated network. Given defined subtype labels, IntegrAO can be further fine-tuned to predict subtypes for new patients based on any combination of omics data. To enable this, we initialized with the unsupervised IntegrAO model parameters and appended a prediction head that ingests the final patient embeddings to output a subtype prediction. We calculate the classification loss Lclf as:

$$
L_{\rm clf} = -\frac{1}{N} \sum_{i=1}^{N} (y_i \log(\text{Pred}(E_i)) + (1 - y_i) \log(1 - \text{Pred}(E_i))), \tag{18}
$$

where Pred(·) is the fully connected prediction head, and y<sup>i</sup> are the defined subtype labels. During fine-tuning, we jointly optimize the total loss:

$$
Loss = L_{\text{reconc}} + \beta \times L_{\text{align}} + \gamma \times L_{\text{clf}}.\tag{19}
$$

The hyperparameter β and γ control the tradeoff between the reconstruction loss, alignment loss, and classification loss during optimization.

#### <span id="page-21-0"></span>Subtype prediction for new patient

During supervised fine-tuning, for the omics data used in training, let {Xtr (m) | m = 1, 2, ..., v} denote the input omic features for different modalities, and {Ptr (m) | m = 1, 2, ..., v} the corresponding fused similarity matrix. The finetuned IntegrAO model can then be trained on {Xtr (m) } and {Ptr (m) }, with training predictions represented as:

$$
\mathbf{Y}_{\mathbf{tr}} = \text{IntegrA}\text{O}(\{\mathbf{X}_{\mathbf{tr}}^{(m)}\}, \{\mathbf{P}_{\mathbf{tr}}^{(m)}\}), m = 1, 2, ..., v,
$$
 (20)

where Ytr ∈ R ntr×c contains the predicted subtype probabilities for each of the ntr training samples, with c denoting the number of subtypes. For a new test sample {Xte (m) | m = 1, 2, ..., v}, to perform model inference, we extend the data matrix of the corresponding omics to {Xtrte = " Xtr Xte# | m = 1, 2, ..., v}, and generate the extended fusion matrix by performing the fusion step with the testing samples {Ptrte (m) | m = 1, 2, ..., v}. Therefore, given {Xtrte} , {Ptrte} and fine-tuned IntegrAO model, we have:

$$
\mathbf{Y}_{\text{trte}} = \text{IntegrAO}(\{\mathbf{X}_{\text{trte}}^{(m)}\}, \{\mathbf{P}_{\text{trte}}^{(m)}\}), m = 1, 2, ..., v,
$$
(21)

where Ytrte ∈ R ntr+1×c . The predicted subtype probability distribution for the testing sample is at the last row of Ytrte.

### <span id="page-21-1"></span>4.5 Cluster number selection for AML subtyping and cancer patient classification expeiments

To identify the optimal number of clusters for cancer datasets, we implemented a specific approach. First, after integrating patient data, we conducted a 10-fold train-test split. In each fold, a Gaussian Mixture Model (GMM) was applied to 90% of the patient embeddings, and log-likelihood scores were calculated on the remaining 10%. This process was repeated for cluster numbers in a pre-defined range. We then computed the mean and standard deviation of the log-likelihood scores for each cluster number. The optimal cluster number was determined by the log-likelihood score, calculated by subtracting the mean from the standard deviation, and used to rank the suitability of each cluster number for the dataset.

In the new patient classification experiments, spectral clustering with this optimal cluster number was applied to the integrated network to obtain clustering labels. For the AML case study, an initial identification of 18 clusters was refined by merging biologically similar clusters, resulting in 12 distinct AML subtypes.

## <span id="page-22-0"></span>4.6 Gene expression deconvolution

To generate the cell composition data for our cancer benchmarking experiments, we utilized BayesPrism[\[37\]](#page-26-5) to deconvolute raw gene expression counts from TCGA cancer cohorts. Our analyses were conducted exclusively through the BayesPrism web portal, adhering to its default preprocessing steps. These steps included filtering outlier genes, selecting protein-coding genes, and isolating signature genes for each cell type. For deconvolution job submissions, we employed the portal's default settings. The resulting matrices, detailing fractions of patient-specific cell types, served as the cell composition modality for our integration benchmarking. The single-cell reference datasets utilized in the deconvolution process are detailed in Supplementary Table S4.

# Declarations

Code Availability. The code to utilize IntegrAO is available on Github: [https://github.com/bowang-lab/IntegrAO.](https://github.com/bowang-lab/IntegrAO)

# References

- <span id="page-23-0"></span>[1] Shin, S.H., Bode, A.M., Dong, Z.: Precision medicine: the foundation of future cancer therapeutics. Npj precision oncology 1(1), 12 (2017)
- <span id="page-23-1"></span>[2] Steyaert, S., Pizurica, M., Nagaraj, D., Khandelwal, P., Hernandez-Boussard, T., Gentles, A.J., Gevaert, O.: Multimodal data fusion for cancer biomarker discovery with deep learning. Nature Machine Intelligence 5(4), 351–362 (2023)
- <span id="page-23-2"></span>[3] Belizario, J.E., Loggulo, A.F.: Insights into breast cancer phenotying through molecular omics approaches and therapy response. Cancer Drug Resistance 2(3), 527 (2019)
- <span id="page-23-3"></span>[4] Lynch, H.T., Snyder, C.L., Shaw, T.G., Heinen, C.D., Hitchins, M.P.: Milestones of lynch syndrome: 1895–2015. Nature Reviews Cancer 15(3), 181–194 (2015)
- <span id="page-23-4"></span>[5] source sites: Duke University Medical School McLendon Roger 1 Friedman Allan 2 Bigner Darrell 1, C.G.A.R.N.T., 5, E.U.V.M.E.G....B.D.J...M.M.G..O.J.J..., 8, H.F.H.M.T..L.N., 11, M.A.C.C.A.K..A.Y.W..B.O., of California San Francisco VandenBerg Scott 12 Berger Mitchel 13 Prados Michael 13, U., et al.: Comprehensive genomic characterization defines human glioblastoma genes and core pathways. Nature 455(7216), 1061–1068 (2008)
- <span id="page-23-5"></span>[6] Zhang, J., Baran, J., Cros, A., Guberman, J.M., Haider, S., Hsu, J., Liang, Y., Rivkin, E., Wang, J., Whitty, B., et al.: International cancer genome consortium data portal—a one-stop shop for cancer genomics data. Database 2011, 026 (2011)
- <span id="page-23-6"></span>[7] Wang, B., Mezlini, A.M., Demir, F., Fiume, M., Tu, Z., Brudno, M., Haibe-Kains, B., Goldenberg, A.: Similarity network fusion for aggregating data types on a genomic scale. Nature methods 11(3), 333–337 (2014)
- <span id="page-23-9"></span>[8] Rappoport, N., Shamir, R.: Nemo: cancer subtyping by integration of partial multi-omic data. Bioinformatics 35(18), 3348–3356 (2019)
- <span id="page-23-7"></span>[9] Nguyen, H., Shrestha, S., Draghici, S., Nguyen, T.: Pinsplus: a tool for tumor subtype discovery in integrated genomic data. Bioinformatics 35(16), 2843–2846 (2019)
- <span id="page-23-8"></span>[10] Shen, R., Mo, Q., Schultz, N., Seshan, V.E., Olshen, A.B., Huse, J., Ladanyi, M., Sander, C.: Integrative subtype discovery in glioblastoma using icluster. PloS one 7(4), 35236 (2012)

- <span id="page-24-0"></span>[11] Yang, Z., Michailidis, G.: A non-negative matrix factorization method for detecting modules in heterogeneous omics multi-modal data. Bioinformatics 32(1), 1–8 (2016)
- <span id="page-24-1"></span>[12] Vaske, C.J., Benz, S.C., Sanborn, J.Z., Earl, D., Szeto, C., Zhu, J., Haussler, D., Stuart, J.M.: Inference of patient-specific pathway activities from multi-dimensional cancer genomics data using paradigm. Bioinformatics 26(12), 237–245 (2010)
- <span id="page-24-2"></span>[13] Wu, D., Wang, D., Zhang, M.Q., Gu, J.: Fast dimension reduction and integrative clustering of multi-omics data using low-rank approximation: application to cancer molecular classification. BMC genomics 16(1), 1–10 (2015)
- <span id="page-24-3"></span>[14] Lee, C., Van der Schaar, M.: A variational information bottleneck approach to multi-omics data integration. In: International Conference on Artificial Intelligence and Statistics, pp. 1513–1521 (2021). PMLR
- <span id="page-24-4"></span>[15] Chen, L., Xu, J., Li, S.C.: Deepmf: Deciphering the latent patterns in omics profiles with a deep learning method. BMC bioinformatics 20(23), 1–13 (2019)
- <span id="page-24-5"></span>[16] de Vega, W.C., Erdman, L., Vernon, S.D., Goldenberg, A., McGowan, P.O.: Integration of dna methylation & health scores identifies subtypes in myalgic encephalomyelitis/chronic fatigue syndrome. Epigenomics 10(5), 539–557 (2018)
- <span id="page-24-6"></span>[17] Stefanik, L., Erdman, L., Ameis, S.H., Foussias, G., Mulsant, B.H., Behdinan, T., Goldenberg, A., O'Donnell, L.J., Voineskos, A.N.: Brainbehavior participant similarity networks among youth and emerging adults with schizophrenia spectrum, autism spectrum, or bipolar disorder and matched controls. Neuropsychopharmacology 43(5), 1180–1188 (2018)
- <span id="page-24-7"></span>[18] Hamamoto, R., Komatsu, M., Takasawa, K., Asada, K., Kaneko, S.: Epigenetics analysis and integrated analysis of multiomics data, including epigenetic data, using artificial intelligence in the era of precision medicine. Biomolecules 10(1), 62 (2019)
- <span id="page-24-8"></span>[19] Martin, K.R., Zhou, W., Bowman, M.J., Shih, J., Au, K.S., Dittenhafer-Reed, K.E., Sisson, K.A., Koeman, J., Weisenberger, D.J., Cottingham, S.L., et al.: The genomic landscape of tuberous sclerosis complex. Nature communications 8(1), 15816 (2017)
- <span id="page-24-9"></span>[20] Little, R.J., Rubin, D.B.: Statistical Analysis with Missing Data vol. 793. John Wiley & Sons, ??? (2019)

- <span id="page-25-0"></span>[21] Henry, A.J., Hevelone, N.D., Lipsitz, S., Nguyen, L.L.: Comparative methods for handling missing data in large databases. Journal of vascular surgery 58(5), 1353–1359 (2013)
- <span id="page-25-1"></span>[22] Flores, J.E., Claborne, D.M., Weller, Z.D., Webb-Robertson, B.-J.M., Waters, K.M., Bramer, L.M.: Missing data in multi-omics integration: Recent advances through artificial intelligence. Frontiers in Artificial Intelligence 6, 1098308 (2023)
- <span id="page-25-2"></span>[23] Fang, Z., Ma, T., Tang, G., Zhu, L., Yan, Q., Wang, T., Celed´on, J.C., Chen, W., Tseng, G.C.: Bayesian integrative model for multi-omics data with missingness. Bioinformatics 34(22), 3801–3808 (2018)
- [24] Argelaguet, R., Arnol, D., Bredikhin, D., Deloro, Y., Velten, B., Marioni, J.C., Stegle, O.: Mofa+: a statistical framework for comprehensive integration of multi-modal single-cell data. Genome biology 21(1), 1–17 (2020)
- <span id="page-25-3"></span>[25] Lock, E.F., Park, J.Y., Hoadley, K.A.: Bidimensional linked matrix factorization for pan-omics pan-cancer analysis. The annals of applied statistics 16(1), 193 (2022)
- <span id="page-25-4"></span>[26] Xu, H., Gao, L., Huang, M., Duan, R.: A network embedding based method for partial multi-omics integration in cancer subtyping. Methods 192, 67–76 (2021)
- <span id="page-25-5"></span>[27] Rappoport, N., Safra, R., Shamir, R.: Monet: Multi-omic module discovery by omic selection. PLOS Computational Biology 16(9), 1008182 (2020)
- <span id="page-25-6"></span>[28] Hornung, R., Ludwigs, F., Hagenberg, J., Boulesteix, A.-L.: Prediction approaches for partly missing multi-omics covariate data: A literature review and an empirical comparison study. Wiley Interdisciplinary Reviews: Computational Statistics, 1626 (2023)
- <span id="page-25-7"></span>[29] Chalise, P., Raghavan, R., Fridley, B.L.: Intersim: Simulation tool for multiple integrative 'omic datasets'. Computer methods and programs in biomedicine 128, 69–74 (2016)
- <span id="page-25-8"></span>[30] Zeng, A.G., Bansal, S., Jin, L., Mitchell, A., Chen, W.C., Abbas, H.A., Chan-Seng-Yue, M., Voisin, V., van Galen, P., Tierens, A., et al.: A cellular hierarchy framework for understanding heterogeneity and predicting drug response in acute myeloid leukemia. Nature medicine 28(6), 1212–1223 (2022)
- <span id="page-25-9"></span>[31] Tyner, J.W., Tognon, C.E., Bottomly, D., Wilmot, B., Kurtz, S.E.,

Savage, S.L., Long, N., Schultz, A.R., Traer, E., Abel, M., et al.: Functional genomic landscape of acute myeloid leukaemia. Nature 562(7728), 526–531 (2018)

- <span id="page-26-0"></span>[32] Marquis, M., Beaubois, C., Lavall´ee, V.-P., Abrahamowicz, M., Danieli, C., Lemieux, S., Ahmad, I., Wei, A., Ting, S.B., Fleming, S., et al.: High expression of hmga2 independently predicts poor clinical outcomes in acute myeloid leukemia. Blood cancer journal 8(8), 68 (2018)
- <span id="page-26-1"></span>[33] van Galen, P., Hovestadt, V., Wadsworth II, M.H., Hughes, T.K., Griffin, G.K., Battaglia, S., Verga, J.A., Stephansky, J., Pastika, T.J., Story, J.L., et al.: Single-cell rna-seq reveals aml hierarchies relevant to disease progression and immunity. Cell 176(6), 1265–1281 (2019)
- <span id="page-26-2"></span>[34] Wang, C.X., Zhang, L., Wang, B.: One cell at a time (ocat): a unified framework to integrate and analyze single-cell rna-seq data. Genome biology 23(1), 102 (2022)
- <span id="page-26-3"></span>[35] Hamilton, W., Ying, Z., Leskovec, J.: Inductive representation learning on large graphs. Advances in neural information processing systems 30 (2017)
- <span id="page-26-4"></span>[36] Van der Maaten, L., Hinton, G.: Visualizing data using t-sne. Journal of machine learning research 9(11) (2008)
- <span id="page-26-5"></span>[37] Chu, T., Wang, Z., Pe'er, D., Danko, C.G.: Cell type and gene expression deconvolution with bayesprism enables bayesian integrative analysis across bulk and single-cell rna sequencing in oncology. Nature Cancer 3(4), 505–517 (2022)
- <span id="page-26-6"></span>[38] Azizi, E., Carr, A.J., Plitas, G., Cornish, A.E., Konopacki, C., Prabhakaran, S., Nainys, J., Wu, K., Kiseliovas, V., Setty, M., et al.: Single-cell map of diverse immune phenotypes in the breast tumor microenvironment. Cell 174(5), 1293–1308 (2018)
- <span id="page-26-7"></span>[39] Lee, H.-O., Hong, Y., Etlioglu, H.E., Cho, Y.B., Pomella, V., Van den Bosch, B., Vanhecke, J., Verbandt, S., Hong, H., Min, J.-W., et al.: Lineage-dependent gene expression programs influence the immune landscape of colorectal cancer. Nature genetics 52(6), 594–603 (2020)
- <span id="page-26-8"></span>[40] Jerby-Arnon, L., Shah, P., Cuoco, M.S., Rodman, C., Su, M.-J., Melms, J.C., Leeson, R., Kanodia, A., Mei, S., Lin, J.-R., et al.: A cancer cell program promotes t cell exclusion and resistance to checkpoint blockade. Cell 175(4), 984–997 (2018)
- <span id="page-26-9"></span>[41] Li, R., Ferdinand, J.R., Loudon, K.W., Bowyer, G.S., Laidlaw, S., Muyas, F., Mamanova, L., Neves, J.B., Bolt, L., Fasouli, E.S., et al.: Mapping

single-cell transcriptomes in the intra-tumoral and associated territories of kidney cancer. Cancer Cell 40(12), 1583–1599 (2022)

<span id="page-27-0"></span>[42] Lambrechts, D., Wauters, E., Boeckx, B., Aibar, S., Nittner, D., Burton, O., Bassez, A., Decaluw´e, H., Pircher, A., Van den Eynde, K., et al.: Phenotype molding of stromal cells in the lung tumor microenvironment. Nature medicine 24(8), 1277–1289 (2018)

# 5 Supplementary Tables

Table S1 The number of patients used in the benchmarking analysis per cancer type. It specifies the patient counts across six diagnostic modalities: mRNA expression, cellular composition, DNA methylation, miRNA expression, reverse-phase protein array, and copy-number variation. The table further details the intersection and comprehensive aggregates of patients within each cancer category.

| Dataset | mRNA | Cell Com | Meth | miRNA | RPPA | CNV | Common   | Union    |
|---------|------|----------|------|-------|------|-----|----------|----------|
|         |      | position |      |       |      |     | patients | patients |
| BRCA    | 1093 | 1093     | 1080 | 756   | 784  | 887 | 511      | 1096     |
| COAD    | 379  | 379      | 616  | 295   | 393  | 494 | 251      | 621      |
| SKCM    | 469  | 469      | 367  | 448   | 470  | 353 | 247      | 461      |
| KIRC    | 533  | 533      | 528  | 257   | 319  | 478 | 306      | 537      |
| LUAD    | 515  | 515      | 516  | 457   | 458  | 365 | 166      | 511      |

Table S2 The number of features used for each omic in the benchmarking analysis per cancer type. The six modalities including: mRNA expression, cellular composition, DNA methylation, miRNA expression, reverse-phase protein array, and copy-number variation.

| Dataset | mRNA | Cell Com | Meth | miRNA | RPPA | CNV  |
|---------|------|----------|------|-------|------|------|
|         |      | position |      |       |      |      |
| BRCA    | 2000 | 25       | 2000 | 897   | 222  | 2000 |
| COAD    | 2000 | 8        | 2000 | 623   | 222  | 2000 |
| SKCM    | 2000 | 9        | 2000 | 901   | 195  | 2000 |
| KIRC    | 2000 | 13       | 2000 | 825   | 212  | 2000 |
| LUAD    | 2000 | 8        | 2000 | 894   | 195  | 2000 |

Table S3 Number of clusters chosen for the new patient classification experiment. Spectral clustering with this chosen cluster count was performed on the IntegrAO-integrated network to determine the "ground truth" labels for each cancer type.

|                   | BRCA | COAD | SKCM | KIRC | LUAD |
|-------------------|------|------|------|------|------|
| Number of cluster | 5    | 7    | 5    | 5    | 3    |

## 32 IntegrAO

Table S4 Number of cells and cell types in the single-cell reference data used for gene expression deconvolution across TCGA cancers. This cell type count includes various subtypes of tumor cells.

| Cancer type | Cell num | Cell<br>type | Reference |
|-------------|----------|--------------|-----------|
|             | ber      | number       |           |
| BRCA        | 45561    | 70           | [38]      |
| COAD        | 18409    | 14           | [39]      |
| SKCM        | 6879     | 19           | [40]      |
| KIRC        | 20476    | 24           | [41]      |
| LUAD        | 52698    | 8            | [42]      |

# 6 Supplementary Figures

![](_page_32_Figure_2.jpeg)
<!-- Image Description: This image displays a heatmap visualizing gene expression profiles across different AML (acute myeloid leukemia) subtypes. Each column represents a subtype (e.g., Primitive, Intermediate, Mature), categorized by genetic markers (NPM1, MLLr, etc.). Rows correspond to individual genes, with color intensity representing expression levels (yellow: high, purple: low). The heatmap illustrates the distinct gene expression patterns characteristic of various AML subtypes, aiding in classification and potentially informing targeted therapies. -->

Fig. S1 IntegrAO identification of 12 subtypes with distinct DNA methylation profiles. The visual representation shows a clear block structure, effectively delineating each cluster, highlighting the distinctiveness of methylation patterns among the subtypes.

![](_page_33_Figure_1.jpeg)
<!-- Image Description: This heatmap displays gene expression data across different acute myeloid leukemia (AML) subtypes. Rows represent genes, columns represent AML subtypes (e.g., primitive, intermediate, mature, various myeloid lineages). Color intensity indicates gene expression levels, with yellow representing high expression and purple representing low expression. The image's purpose is to illustrate the distinct gene expression profiles characterizing various AML subtypes, aiding in their classification and potentially informing targeted therapies. -->

Fig. S2 VIPER analysis of all regulons: heatmap showcasing cluster-specific regulatory signatures. This heatmap reveals distinct block structures corresponding to IntegrAO-defined clusters, illustrating the diverse regulatory landscapes encompassing all types of regulons, including transcription factors, non-coding RNAs, and other regulatory molecules.

![](_page_34_Figure_1.jpeg)
<!-- Image Description: This heatmap displays gene expression profiles across different myeloid leukemia subtypes. Rows represent genes, columns represent cell subtypes (e.g., primitive, intermediate, mature NPM1, etc.). Color intensity indicates gene expression level, with yellow representing high expression and purple representing low expression. The figure likely illustrates the heterogeneity of gene expression across leukemia subtypes, supporting the paper's analysis of disease classification or treatment strategies based on gene expression patterns. -->

Fig. S3 VIPER analysis of transcription factor (TF) regulons: heatmap depicting transcription factor-driven regulatory patterns. The heatmap displays clear, distinct blocks that align with IntegrAO-defined clusters, highlighting the specific influence of transcription factors on the gene expression within each cluster.

![](_page_35_Figure_1.jpeg)
<!-- Image Description: The image displays three panels. (a and b) are Kaplan-Meier curves showing overall survival probabilities over time for two cohorts (TCGA and BEAT-AML). Multiple colored lines represent different subgroups within each cohort. Statistically significant differences in survival are indicated (p<0.0001 and p=0.00012). (c) is a bar graph presenting -log10 transformed p-values from multivariate survival analyses for three methods (Hierarchy, RNA, IntegrAO), suggesting IntegrAO has the most significant association with survival. -->

Fig. S4 Additional survival analysis of the AML case study includes: (a) a Kaplan-Meier survival curve for the TCGA AML patient cohort, stratified by IntegrAO's clusters, showing statistical significance (multi-group logrank test p-value = 6.1e-5); (b) a similar Kaplan-Meier curve for the BEAT-AML patient cohort, also stratified by IntegrAO's clusters, indicating significant differences in survival outcomes (multi-group logrank test p-value = 1.2e-4); (c) a comparison of multivariate survival significance between IntegrAO's clustering solution and solutions derived from using only cell hierarchy or RNA data on the TCGA and BEAT-AML combined cohort. This comparison demonstrates that IntegrAO's clustering notably enhances multivariate survival significance.

![](_page_36_Figure_1.jpeg)
<!-- Image Description: This image presents a matrix of box plots. Each plot displays the distribution of a variable (likely PK/PD metric) across different drug treatments. The x-axis represents the drug administration schedule, while the y-axis shows the variable's values. The multiple plots compare the effects of various drugs (labeled above each column) on the measured parameter. The figure's purpose is to visually compare the pharmacokinetic and/or pharmacodynamic profiles of numerous drugs under different dosing regimens. -->

Fig. S5 Drug sensitivity profile across IntegrAO-identified clusters. This figure illustrates the differential responses of various IntegrAO-derived clusters to a range of anti-cancer agents, showcasing the distinct drug sensitivity patterns characteristic of each cluster in the context of AML treatment.

![](_page_37_Figure_1.jpeg)
<!-- Image Description: This image displays a dimensionality reduction plot, likely t-SNE or UMAP, visualizing single-cell RNA sequencing data. Distinct clusters represent different cell types within the hematopoietic system, color-coded and labeled (e.g., "CD4 Naive," "Megakaryocyte," "Pro-B Cycling"). The plot's purpose is to illustrate the cell type diversity and lineage relationships within a sample, based on gene expression profiles. The branching structure suggests developmental trajectories. -->

Fig. S6 UMAP Visualization of single-cell RNA-seq data from bone marrow mononuclear cells, based on research by Galen et al[\[33\]](#page-26-1). This plot offers a detailed representation of celltype diversity and distribution within the bone marrow environment, as captured through advanced single-cell sequencing techniques.

![](_page_38_Figure_1.jpeg)
<!-- Image Description: The image displays five network graphs, each representing a different cancer subtype (BRCA, KIRC, LUAD, SKCM, COAD). Nodes, color-coded by class, represent samples, and edges show relationships between them. The graphs visualize the clustering of cancer samples based on their subtype, illustrating distinct groupings and potential relationships within each cancer type. The purpose is to show the network structure of cancer subtypes, likely for analysis of similarities and differences. -->

Fig. S7 UMAP plots displaying patient embeddings across five cancer types from the new patient classification experiments. Labels were derived via spectral clustering on the full integrated network, using the preselected number of clusters.
