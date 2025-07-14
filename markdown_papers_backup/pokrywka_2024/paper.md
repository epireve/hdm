cite_key: "pokrywka_2024"
title: "Evaluating Transformer Models for Suicide Risk Detection on Social Media"
authors: "Jakub Pokrywka, Jeremi I. Kaczmarek, Edward J. Gorzelańczyk"
year: 2024
doi: "10.48550/arXiv.2410.08375"
url: "https://arxiv.org/html/2410.08375v1"
relevancy: "High"
tldr: "Comparative analysis of transformer-based models for suicide risk detection from social media posts using natural language processing to classify risk categories including indicator, ideation, behavior, and attempt."
insights: "Fine-tuned GPT-4o achieved highest performance with weighted F1 score of 75.5% and demonstrated that general-purpose models can achieve state-of-the-art results in suicide risk detection, securing second place in IEEE BigData 2024 Cup competition."
summary: "This paper explores using natural language processing to detect suicide risk in social media posts through transformer-based models. The researchers experimented with three configurations: fine-tuned DeBERTa (base and large models), GPT-4o with Chain of Thought prompting, and fine-tuned GPT-4o. The goal was to classify social media posts into four risk categories: indicator, ideation, behavior, and attempt, using a Reddit-sourced dataset with 2,000 posts during the COVID-19 pandemic period."
research_question: "Which natural language processing method would work best for suicide risk detection on social media while balancing accuracy and practical deployment constraints?"
methodology: "Used three transformer model configurations including fine-tuned DeBERTa base and large models, GPT-4o with few-shot prompting and Chain of Thought reasoning, fine-tuned GPT-4o model, evaluated on Reddit-sourced dataset with 2,000 posts."
key_findings: "Fine-tuned GPT-4o achieved highest performance with weighted F1 score of 75.5%, achieved second place in IEEE BigData 2024 Cup, demonstrated that general-purpose models can achieve state-of-the-art results with minimal specialized tuning."
limitations: "Dataset restricted to Reddit posts, collected during COVID-19 pandemic creating potential temporal bias, limited contextual information available, potential bias in data collection methodology."
conclusion: "Simple, robust pre-trained models can effectively detect suicide risk with minimal specialized tuning, providing practical approach for early intervention systems."
future_work: "Develop dataset based on clinical assessments, collaborate with healthcare institutions for validation, expand to multi-platform analysis for comprehensive risk assessment."
implementation_insights: "Provides technical framework for implementing mental health monitoring in HDM systems with focus on social media analysis while highlighting importance of clinical validation and multi-modal data integration."
tags:
  - "Suicide Risk Detection"
  - "Transformer Models"
  - "Social Media Analysis"
  - "Mental Health Tech"
  - "NLP for Healthcare"
---

# Evaluating Transformer Models for Suicide Risk Detection on Social Media

Jakub Pokrywka *Adam Mickiewicz University* Poland jakub.pokrywka@amu.edu.pl

Jeremi I. Kaczmarek *Adam Mickiewicz University, Poznan University of Medical Sciences* Poland jeremi.kaczmarek@amu.edu.pl

Edward J. Gorzela ´nczyk *Kazimierz Wielki University, The Society for the Substitution "Medically Assisted Recovery"* Poland medsystem@medsystem.com.pl

**Abstract:** The detection of suicide risk in social media is a critical task with potential life-saving implications. This paper presents a study on leveraging state-of-the-art natural language processing solutions for identifying suicide risk in social media posts as a submission for the "IEEE BigData 2024 Cup: Detection of Suicide Risk on Social Media" conducted by the kubapok team. We experimented with the following configurations of transformer-based models: fine-tuned DeBERTa, GPT-4o with CoT and few-shot prompting, and fine-tuned GPT-4o. The task setup was to classify social media posts into four categories: indicator, ideation, behavior, and attempt. Our findings demonstrate that the fine-tuned GPT-4o model outperforms two other configurations, achieving high accuracy in identifying suicide risk. Notably, our model achieved second place in the competition. By demonstrating that straightforward, general-purpose models can achieve state-of-the-art results, we propose that these models, combined with minimal tuning, may have the potential to be effective solutions for automated suicide risk detection on social media.

## TL;DR
Comparative analysis of transformer-based models for suicide risk detection from social media posts using natural language processing to classify risk categories including indicator, ideation, behavior, and attempt.

## Key Insights  
Fine-tuned GPT-4o achieved highest performance with weighted F1 score of 75.5% and demonstrated that general-purpose models can achieve state-of-the-art results in suicide risk detection, securing second place in IEEE BigData 2024 Cup competition.

**Index Terms:** suicide risk detection, AI in medicine, natural language processing.

## I. INTRODUCTION

## *A. Suicide and Suicidal Behavior: Definitions, Distinctions, and Determinants*

Suicide is a major global health concern, with over 720,000 individuals taking their own lives each year (WHO 2024). The true scale of the problem is likely underestimated, as many non-fatal attempts remain unreported. These behaviors often result in injury, disability, and long-lasting psychological trauma, extending beyond individuals to affect families and communities. The broad social and economic implications further highlight the urgent need for effective public health strategies[1](#page-0-0)

While the definition of suicide is generally consistent in the literature, terminology for related concepts varies widely. Specialist psychiatric and psychological sources often use these terms inconsistently. To ensure clarity, we have adopted a simplified set of terms derived from multiple sources [\[1\]](#page-6-0) [2](#page-0-1) . We use these terms to describe psychological and psychiatric phenomena. However, note that some may carry different meanings in our work when referring to the suicide risk level labels used in the competition dataset [\[2\]](#page-6-1). Table [I](#page-0-2) provides a comparison of these terms and their corresponding definitions.

<span id="page-0-2"></span>TABLE I COMPARISON OF THE SUICIDE RISK LEVEL LABELS UTILIZED IN THE TRAINING DATA WITH PSYCHIATRIC AND PSYCHOLOGICAL TERMINOLOGY ADAPTED FOR THIS WORK.

| Term | Benchmark Dataset [2], [3] | This Work |
|-----------|--------------------------------|-----------------------------------|
| Indicator | The post content has no ex | - |
| | plicit expression concerning | |
| | suicide. | |
| Ideation | The post content has explicit | Thoughts,<br>considerations, |
| | suicidal expression, but there | and plans of suicide. |
| | is no plan to commit suicide. | |
| Behavior | The post content<br>has ex | Self-directed,<br>injurious<br>be |
| | plicit suicidal expression and | havior with an intent to die. |
| | a plan to commit suicide or | |
| | self-harming behaviors. | |
| Attempt | The post content has explicit | Non-fatal, self-directed, inju |
| | expressions concerning his | rious behavior with an intent |
| | toric suicide attempts. | to die. |
| Suicide | - | Fatal, self-directed, injurious |
| | | behavior with an intent to |
| | | die. |

Suicidal ideation refers to ruminating, thinking, or planning suicide. Suicidal behavior, on the other hand, is defined as an act of self-harm performed with the intent to die. If the behavior results in death, it is classified as suicide; if it does not, it is considered a suicide attempt. Terms like "failed" or "unsuccessful" attempt should be avoided, as they imply that death is the desired outcome [\[1\]](#page-6-0).

It is critical to differentiate suicidal behavior from nonsuicidal self-injury (NSSI), which involves deliberate selfharm without lethal intent. Although NSSI and suicidal behavior may share overlapping risk factors, they serve distinct psychological purposes, necessitating precise differentiation for accurate clinical assessment and intervention [\[1\]](#page-6-0), [\[4\]](#page-6-3).

The etiology of suicidal behavior is complex and multifactorial, involving psychological, social, cultural, biological and environmental components. In clinical practice, the progression from suicidal ideation to planning and attempting is often used as a framework to understand the interplay between risk and protective factors. Identifying these predictors is critical for risk assessment and adequate intervention [\[1\]](#page-6-0).

<sup>1</sup><https://www.who.int/news-room/fact-sheets/detail/suicide>

<span id="page-0-1"></span><span id="page-0-0"></span><sup>2</sup><https://www.nimh.nih.gov/health/statistics/suicide>

## *B. Motivation for Suicide Risk Detection Algorithms on the Internet*

The rapid pace of societal changes, characterized by digitalization and increased information accessibility, has introduced new dimensions to the etiology of suicide. Social media, in particular, has garnered attention as a potential contributor to the deterioration of mental health, especially among youth. Several phenomena, mainly cyberbullying and trolling, displacement of beneficial activities, and persistent preoccupation, are often regarded as exacerbating existing risk factors or acting as independent contributors, correlating with increased prevalence of self-harm, suicidal ideation, and other mental health problems [\[5\]](#page-6-4).

However, these same platforms, when combined with advancements in technology such as machine learning and big data analytics, offer promising opportunities for suicide prevention. Novel interventions leveraging social media data could reach individuals who might not otherwise receive help, using information that is typically inaccessible to mental health professionals by traditional means. This is particularly relevant given the limited access to psychiatric and psychological care and the demand for it continuously increasing. Considering that suicide is the third leading cause of death among individuals aged 15–29 (WHO, 2024) — a demographic with a high social media consumption — such solutions could be especially impactful.

One promising approach involves suicide risk detection systems deployed within social media platforms. These systems can analyze vast and diverse datasets, including the content of posts and comments, precise metadata such as time stamps and user interactions, and employ Natural Language Processing (NLP) to identify emotions, sentiments, and specific risk factors indicative of suicidal behavior. Moreover, advanced Artificial Intelligence (AI) models have the potential to discern subtle patterns suggestive of underlying somatic or neuropsychiatric symptoms. Detection systems enable continuous content monitoring, facilitate early intervention, and offer the possibility of preventing numerous tragedies through timely and targeted responses. Although detecting suicide risk is the primary objective of current systems, the ability to differentiate between genuine suicidal intent and self-harm threats without the intent to die is an intriguing perspective worth mentioning.

## *C. kubapok at IEEE BigData 2024 Cup: Detection of Suicide Risk on Social Media*

In recent years, the field of NLP developed rapidly. This may be attributed mainly to artificial neural network architecture Transformers [\[6\]](#page-6-5) and training neural models with massive amounts of text. The excellent results of the contemporary NLP models are promising for the development of suicidal detectors based on Internet texts. However, the question arises: which NLP method would work the best for this task?

The presented paper contributes to the subject of suicide risk detection on the Internet by comparing three state-ofthe-art NLP approaches on a benchmark dataset developed especially for this task. The work was created as an entry for the "IEEE BigData 2024 Cup for the Detection of Suicide Risk on Social Media" [\[2\]](#page-6-1) by the kubapok team. The benchmark dataset includes a training set and two test sets (preliminary and final). The training set comprises both annotated and nonannotated samples. Each annotated sample consists of a text with exactly one associated label: indicator, ideation, behavior, or attempt.

The approaches for such a task may include incorporating specialized NLP models designed for medical applications, data augmentation, and using pseudo-labels from nonannotated parts of the train datasets or external datasets. Moreover, the class imbalance in labels poses an additional challenge, which may be addressed by sampling techniques, adjusting class probabilities during inference, or model finetuning.

Nevertheless, we choose not to employ highly specialized techniques. We set our objective to utilize just a straightforward and generalizable approach by leveraging neural models of general utility without integrating advanced methods. Such an approach makes it easy to migrate it between different text domains and the availability of corpora. We evaluated two Transformer-based models: the DeBERTa model [\[7\]](#page-6-6) (in both base and large sizes) and the GPT-4o model [\[8\]](#page-6-7). The DeBERTa model, an encoder-only architecture, is publicly available and requires fine-tuning on a task-specific training dataset to achieve optimal performance. Conversely, the GPT-4o model, a decoder-only architecture, can be accessed publicly through an API and used without fine-tuning by employing direct querying. Additionally, we explored the Chain of Thought (CoT) methodology, which prompts the model to generate intermediate reasoning steps before providing a final response, a technique shown to enhance model performance [\[9\]](#page-6-8). Another effective strategy is few-shot prompting, which involves providing the model with a small set of task-specific examples in the prompt [\[10\]](#page-6-9). We incorporated both of these techniques into the prompt design for the GPT-4o model. While decoderonly models can also be fine-tuned to improve accuracy, this capability for the GPT-4o model has only recently become available through its API. We experimented with fine-tuning approach as well.

To sum up, we tested the following methods:

- DeBERTa (encoder-only model) for classification task
- GPT-4o (decoder-only model) with few-short prompting and Chain of Thought (CoT)
- GPT-4o (decoder-only model) fine-tuned generative model

Both model families were evaluated in the context of the SemEval 2024 Task 9 Brainteaser challenge [\[11\]](#page-6-10), a recent competition focused on a classification task outside the medical domain. In this paper, we demonstrate that among the methods we evaluated, the GPT-4o model with fine-tuning achieved the best performance. Our final solution, based on this fine-tuned GPT-4o, scored second place in the "IEEE BigData 2024 Cup for the Detection of Suicide Risk on Social Media", finishing marginally behind the top team among the 13 teams that participated in the final evaluation. This outcome illustrates that even straightforward, general-purpose models can achieve state-of-the-art performance, provided they leverage advanced model architectures effectively.

## II. RELATED WORK

The use of NLP in suicide risk detection has evolved significantly. Initial research focused on traditional machine learning methods, such as Support Vector machines (SVMs) and logistic regression. For example, a study [\[12\]](#page-6-11) demonstrated that these methods could distinguish between genuine and elicited suicide notes with accuracy comparable to mental health professionals, highlighting the potential of computational tools in assessing suicide risk.

As social media platforms became more widely used, research shifted to analyzing user-generated content to detect signs of suicidal ideation. For example, a study [\[13\]](#page-6-12) employed text mining techniques, including Term Frequency-Inverse Document Frequency (TF-IDF) and sentiment analysis, which were applied to posts from Reddit forums like r/SuicideWatch, r/Depression, and r/Anxiety. The study utilized machine learning models like Logistic Regression, SVMs, and Random Forest (RF), achieving high accuracy (80%-92%) in distinguishing suicidal posts from non-suicidal ones, demonstrating the effectiveness of these methods for identifying at-risk individuals online.

The introduction of original Transformer architecture [\[6\]](#page-6-5) and its variants, like BERT [\[14\]](#page-6-13) and GPT [\[15\]](#page-7-0), has revolutionized NLP. Such models, built on the self-attention mechanism, have proven to be especially effective in capturing nuanced language patterns and contextual dependencies. Their ability to model complex semantics has made them particularly suitable for mental health applications, including suicide risk detection.

Recent research has shown that Transformer-based approaches outperform traditional machine-learning methods in detecting suicidal ideation. One study [\[16\]](#page-7-1) evaluated various models on social media datasets comprising Twitter and Reddit posts. The results demonstrated that Transformer models, particularly BERT and RoBERTa [\[17\]](#page-7-2), achieved significantly higher accuracy than traditional approaches like SVMs and RF. The advantage of these models was most notable when analyzing longer texts from Reddit, where they demonstrated greater accuracy and contextual understanding. In 2019, a shared task was conducted to detect the degree of suicide risk in Reddit posts [\[18\]](#page-7-3). The authors of [\[19\]](#page-7-4) achieved first place in two out of the three subtasks using SVMs. Two teams utilized BERT for the competition [\[20\]](#page-7-5), [\[21\]](#page-7-6). Aside from the competition, other researchers have utilized neural models different from transformer-based architectures — specifically, Long Short-Term Memory (LSTM) and Convolutional Neural Networks (CNN) — for the Bangla language, as advanced transformer-based NLP models were not yet available at that time [\[22\]](#page-7-7). Authors of [\[23\]](#page-7-8) used custom self-attention LSTM-based custom architecture enriched by CNN and BERT embeddings.

In recent studies, the use of transformer-based models has become increasingly common. For instance, the authors of [\[24\]](#page-7-9) and [\[25\]](#page-7-10) conducted comparisons between traditional BiLSTM and TF-IDF-based models with transformer models and reported that transformer-based approaches significantly outperformed the conventional methods for suicidal ideation detection. Similarly, other studies have also leveraged transformer models for this task, such as those presented in [\[26\]](#page-7-11)– [\[29\]](#page-7-12). Authors of [\[30\]](#page-7-13) developed a Large Language Model (LLM)–based safeguard model for safety risk detection in other LLM prompts. Among many labels, there is the Suicide & Self Harm category.

## III. SUICIDE DETECTION TASK

## *A. Original Dataset*

Reference [\[2\]](#page-6-1) developed a dataset, primarily utilizing Reddit's r/SuicideWatch subreddit, collecting posts from January 2020 to December 2021. The initial dataset consisted of 139,455 posts from 76,186 users. Preprocessing involved the removal of personally identifiable information and the elimination of duplicates. Posts were filtered using negative expressions and terms prominently associated with suicidal ideation in order to identify users exhibiting potential suicide risk.

These users' historical posts and comments from 14 relevant subreddits (e.g., r/Depression, r/SelfHarm) were then gathered. The last post of each user was designated as the "targeted post" to serve as a representation of their latest suicidal risk. This process resulted in a final dataset of 3,998 posts from 1,791 users. To provide additional contextual information, posts made by a user in r/SuicideWatch or in one of the 14 relevant subreddits in the week prior to the targeted post, along with their and other users' comments made under the targeted post, were further included in the dataset.

Manual annotation was conducted on a subset of 500 users, with posts categorized into four suicide risk levels: indicator, ideation, behavior, and attempt. This annotation was carried out at two levels: based solely on the post and with consideration of contextual information. Additionally, at the sentence level, labels for 17 categories of suicide triggers were added. These triggers were specific events or experiences, such as mental disorders, helplessness, or substance use, and were regarded by the authors as potential catalysts that could push someone closer to attempting suicide.

It is important to note that the training data was narrowed in the competition and did not include trigger labels or contextual information. We further describe the dataset that was made available to us to complete the task, which derived from the previous work.

## *B. Competition Dataset*

This subsection provides an overview of the task titled "IEEE BigData 2024: Detection of Suicide Risk on Social Media." The training dataset, derived from prior work [\[2\]](#page-6-1), consisted of 2,000 Reddit posts, of which 500 were annotated and 1,500 remained unannotated. The preliminary test set contained 100 samples with hidden labels, which were used to assess the teams' initial results during the competition. Following the competition, all submitted models were evaluated using a separate test set for the final assessment. Each annotated sample in the dataset was categorized into one of four classes of suicide risk level: indicator, ideation, behavior, and attempt. The official evaluation metric for this shared task was the weighted F1-score (wF1). Tables [II](#page-3-0) and [III](#page-3-1) provide a detailed breakdown of the complete dataset and the training subset, respectively.

The dataset exhibited a relatively balanced representation of posts across the indicator, ideation, and behavior categories. In contrast, the attempt category was significantly underrepresented, creating a challenge due to the imbalance in category distribution. Additionally, posts in the attempt category had a higher average character and word count compared to the other categories. This suggests that distinguishing the attempt category from the others may be relatively straightforward, while differentiating between the remaining categories could present more difficulty.

<span id="page-3-0"></span>TABLE II DISTRIBUTION OF POSTS ACROSS DATASET SPLITS

| Dataset Split | Number of Posts |
|------------------------|-----------------|
| Training (Annotated) | 500 |
| Training (Unannotated) | 1500 |
| Preliminary Test | 100 |

<span id="page-3-1"></span>TABLE III DISTRIBUTION AND CHARACTERISTICS OF RISK CATEGORIES IN THE ANNOTATED TRAINING SET

| Category | Number of Posts | Avg Characters | Avg Words |
|-----------|-----------------|----------------|-----------|
| Indicator | 129 | 697 | 136 |
| Ideation | 190 | 835 | 162 |
| Behavior | 140 | 913 | 178 |
| Attempt | 41 | 1776 | 339 |
| All | 500 | 899 | 174 |

Below, we provide one sample of each category from the training dataset. If the sample exceeds 500 characters, it is truncated. Please note that the comments may include distressing content or contain offensive language.

## Indicator:

Friend may kill himself soon. Unsure what to do. I have a good friend that I met online 14 years ago, and we finally met in person last year and really connected on a much deeper level. I have been suicidal on-and-off for much of my life due to having a bad case of Crohn's Disease and because of stress, anxiety , and depression. Fortunately, I am in a good place now and haven't had suicidal ideation in months (which is a first for me). I did have one very serious attempt in 2009 which almost ...

## Ideation:

Nsfw. So uh. ever since I was younger I've had a bad porn issue, one of those kids who had like a ton of porn downloaded on their phone,

etc etc. I dislike it to say the least, even to this day, I dislike the roles it plays in my day to day life and find myself being disappointed in myself. That issue is something besides what i'm talking about now but it helps set the idea. My girlfriend has cheated on me multiple times and for some reason I'm still with her. I don't wanna think or talk about...

## Behavior:

i'm gonna overdose on iron pills. i have pain everyday and i don't wanna deal with it. i'm sorry. i may do it tonight.

## Attempt

"There is nothing holding me here.so now what ?. I have been wanting to off myself since 7. I am now 30.\n\nLiving situation is shit. My father, landlady and roommate's ex all say I am a problem and they all gaslight me and are narcissists. I havent been living in that house for 3 weeks in April so far. \n\nPartner /boyfriend/friend whatever he is/was stopped talking to me because of all the drama . Roommate's ex makes fake instagram accounts and messages me very harrassing fucked up things...

## IV. METHODS

In this section, we describe our approach, which focuses on evaluating simple, universal, state-of-the-art methods. The first subsection details the use of publicly available DeBERTa models, in both base and large sizes, fine-tuned on the provided training dataset.

The subsequent subsections address the GPT-4o model, which was tested in two configurations. Subsection [IV-C](#page-4-0) outlines the use of the model in an in-context learning setup, where the model's weights remain unchanged, and all taskspecific information is provided solely through the input prompt. Subsection [IV-B](#page-4-1) describes a configuration in which the model undergoes fine-tuning. Although the GPT-4o model is not available for direct download and can only be accessed through an API, recently, it was made possible to fine-tune the model via the API, a method we adopted for our experiments.

## *A. DeBERTa Models*

We employed two DeBERTa models —DeBERTa-base and DeBERTa-large — which we fine-tuned locally. All training and inference tasks were conducted on a single A100 GPU with 80GB VRAM. The fine-tuning process utilized the Hugging Face Transformers library [\[31\]](#page-7-14) in conjunction with the Hugging Face Trainer. Text inputs were truncated to 512 tokens, and the models were trained with the following hyperparameters: learning rate= 2e-5, batch size = 32, warmup ratio = 0.2, and for 100 epochs. The best-performing model was selected based on the evaluation of the weighted F1 score on a validation dataset. A random 20% split of the data, without stratification, was reserved for testing as a validation dataset.

We explored both single-model and ensemble-model configurations. Multiple ensembles, based on different random train/validation splits, were evaluated using the competition leaderboard. The optimal ensemble was determined based on its performance on the preliminary test set provided by the challenge organizers.

## <span id="page-4-1"></span>*B. GPT-4o Without Fine-Tuning*

GPT-4o is currently among the top-performing Transformer models. In our approach, we leveraged the GPT-4o version, employing the few-shot learning technique. Additionally, we integrated the Chain-of-Thought method, wherein the model first generated an explanation before producing the final answer. We set the temperature parameter to 0.0 for inference to ensure deterministic outputs and the highest probability for the correct answer.

The following instruction prompt was used:

```
You will be given social media texts (
documents). Each document will be associated
with one of the suicide risk labels: 'A.
indicator', 'B. ideation', 'C. behavior', 'D.
attempt'. Your task is to label new documents
with one of these risk labels. Output a JSON
with the following format: {'explanation':'',
'label':''}.
```

We evaluated two configurations of the few-shot prompting approach using 100 examples (referred to as "GPT-4o CoT 100 shot" in Table [IV](#page-4-2) and 500 examples (referred to as "GPT-4o CoT 500 shot"). Both configurations were tested using the gpt-4o-2024-05-13 model. We only conducted evaluation on a single model and did not assess ensemble models in this case.

## <span id="page-4-0"></span>*C. GPT-4o Fine-Tunned*

Recently, the OpenAI API enabled fine-tuning of the gpt-4o-2024-08-06 model on custom data. We leveraged this capability and used the following prompt:

```
You will be given a social media text. There
are four possible suicidal risk labels: 'A.
indicator', 'B. ideation', 'C. behavior', 'D.
attempt'. Your task is to label the given
document with one of these risk labels. e.g.,
'C. behavior'.
```

We used the same prompt for inference, with a temperature of 0.0. For ensemble learning, we used a stratified 3 train/validation split (from scikit-learn's library [\[32\]](#page-7-15) StratifiedShuffle-Split) with a test size of 10%, training for six epochs across different seeds.

## V. RESULTS

The results reported as weighted F1 scores on the preliminary test set provided by the competition organizers are in Table [IV.](#page-4-2) The best-performing solution is the fine-tuned GPT-4o model. Not very far behind is the DeBERTa-large model, which was much better than the DeBERTa-base model. However, when participating in the competition, we submitted multiple solutions using many ensembles of DeBERTa models, and the results varied greatly. This may be due to the fact

<span id="page-4-2"></span>TABLE IV PRELIMINARY TEST SCORES PROVIDED BY THE COMPETITION ORGANIZERS OF OUR METHODS

| Solution | wF1 |
|-----------------------------|------|
| DeBERTa-base single model | 64.8 |
| DeBERTa-base ensemble | 69.0 |
| DeBERTa-large best ensemble | 73.0 |
| GPT-4o CoT 100 shot | 58.9 |
| GPT-4o CoT 500 shot | 58.9 |
| GPT-4o ft single model | 73.6 |
| GPT-4o ft ensemble | 74.8 |

<span id="page-4-3"></span>TABLE V FINAL SCORES OF ALL THE TEAMS PARTICIPATING IN THE FINAL EVALUATION

| Rank | Team Name | wF1 |
|------|----------------------------------|------|
| 1 | Detection of Suicide | 76.1 |
| 2 | kubapok | 75.5 |
| 3 | mukumuku | 75.1 |
| 4 | BioNLP@WCM | 74.6 |
| 5 | Calculators | 73.4 |
| 6 | The Dual | 73.1 |
| 7 | BNU AI and Mental Health | 71.1 |
| 8 | MindFlow | 70.7 |
| 9 | EEEAT | 69.9 |
| 10 | MIDAS | 69.8 |
| 11 | PotatoTomato | 69.1 |
| 12 | LifeWatcher | 55.3 |
| 13 | Data Science and Decision Making | 55.0 |

that the test dataset was small (100 samples) or due to the inconsistency of the DeBERTa model performance. However, for fine-tuned GPT-4o, we used only three models, and all the results were consistently high. That's why we ultimately chose fine-tuned GPT-4o for the final solution. The least performing method was GPT-4o without fine-tuning, but only with CoT and few-shot learning methods. This model performed almost the same when 100 and 500-shot examples from the training dataset were used as examples in the prompt.

Table [V](#page-4-3) presents the final test dataset scores of all teams participating in the competition. Our team achieved second place with a score of 75.5, closely following the top score of 76.1. According to the competition summary provided on the organizers' webpage[3](#page-4-4) , there were 47 registered teams, of which 21 actively participated in the leaderboard. Participants employed various strategies to leverage the unlabeled training dataset, such as pseudo-labeling, manual annotation, and data augmentation. Additionally, teams addressed class imbalance using techniques like sampling strategies, class weight adjustment, and custom loss function designs. Although we experimented with class weight adjustments — ultimately finding them ineffective in our case — we did not implement other methods for handling the label imbalance.

Our approach incorporated an ensemble of the bestperforming models, a widely adopted strategy in competitive settings that typically enhances the final score. Despite relying on straightforward methods, our use of state-of-the-art models proved highly effective. This outcome suggests that, in this

<span id="page-4-4"></span><sup>3</sup><https://competitionpolyu.github.io/report.html>

context, established universal techniques can achieve exceptional results.

It's important to note that models like GPT4-o, which are only accessible via API, have a significant disadvantage in that it is not possible to conduct in-depth research on these models, and using them on a large scale can be expensive. Nonetheless, one key advantage is that using these models doesn't require access to GPU infrastructure for training or inference, nor does it require advanced programming skills. This ease of use makes these models accessible to a wide range of users, including medical staff without expertise in computer science.

## VI. CONCLUSION

In this study, we explored three approaches for the "IEEE BigData 2024 Cup: Detection of Suicide Risk on Social Media" shared task. These approaches included utilizing an encoder-only model and two configurations of a decoder-only model: one using CoT with in-context Learning and the other incorporating fine-tuning. Our results indicated that the bestperforming method was the fine-tuned decoder-only model, likely due to the inherent strength of the GPT-4o. Notably, finetuning yielded superior performance for this particular model compared to the in-context learning setup.

Our final solution did not employ any advanced or specialized techniques beyond model ensembling. Nevertheless, despite the simplicity of our approach, it achieved second place in the competition, demonstrating the effectiveness of leveraging robust, pre-trained models and straightforward methodologies.

## VII. LIMITATIONS

Despite the strong performance of models, particularly the fine-tuned GPT-4o, when considering their use in suicide risk detection, it is essential to recognize the limitations of the dataset used in their training. In clinical practice, suicide risk assessments are conducted during a face-to-face interview by trained professionals who consider both risk and protective factors within a comprehensive evaluation of the patient's medical history [\[33\]](#page-7-16), [\[34\]](#page-7-17). While the original dataset aims to capture these elements through detailed sentence annotations and prior user posts, the competition dataset has been narrowed, containing only four broad risk categories per post and lacking contextual data. Although these categories cover key aspects such as suicidal ideation, behaviors, and past suicide attempts, the exclusion of labels for specific suicide triggers diminishes the competition dataset's predictive value, as these labels provide critical insights into accompanying risk factors.

While representing an advancement over previous resources, the dataset is subject to certain methodological biases that may affect its generalizability. The primary data were collected from r/SuicideWatch posts between January 1, 2021, and December 31, 2022, introducing two key limitations. First, the dataset may not be representative of the broader Reddit community or users who do not engage with r/SuicideWatch. Second, the posts were collected during the COVID-19 pandemic, which may limit the dataset's applicability under different circumstances as pandemic-related mental health effects diminish.

The creators expanded the dataset by including posts from 14 additional subreddits made by the same users, thereby increasing its scope beyond a single online community. However, this approach may still overlook crucial posts that could enhance the accuracy of suicide risk prediction. Incorporating data from a broader range of subreddits could better capture the diversity of user experiences and enhance the dataset's representativeness.

In the original dataset, each user's most recent post made in one of the selected subreddits was designated as the "targeted post," with contextual data collected from comments under it and from the user's activity in one of 14 relevant communities in the preceding week. While this contextual information is absent from the competition dataset, which contains only the "targeted post", we endorse the inclusion of previous posts in the original dataset, as it offers critical insights into the development of suicidal behavior. Nevertheless, limiting the context to one week makes it insufficient for capturing longterm risk patterns, as suicidal ideation can persist or fluctuate over extended periods [\[1\]](#page-6-0), [\[4\]](#page-6-3). Encouragingly, the dataset creators have expressed a willingness to extend this timeframe.

The original dataset, which includes contextual information from previous posts and utilizes more precise labels to capture specific risk factors, represents a significant advancement in training data for models aimed at detecting suicidal behavior based on online activity. Despite only being able to use the narrow competition training set, we identified several limitations that are inherent in any dataset constructed solely from online content.

## VIII. FUTURE WORK

We propose developing a dataset based on the online activity of patients whose suicidal tendencies have been confirmed or ruled out by qualified professionals, such as psychiatrists or clinical psychologists. This approach could potentially offer a more objective and reliable method for assessing suicide risk, though it is not without drawbacks.

Online posts and comments often lack verification in terms of authenticity when compared to clinical assessments, where more objective mental state examinations can be conducted. Consequently, information regarding suicidal status gathered solely from social media activity is not as reliable as the one deriving from direct clinical interviews. Although the significance of this potential problem in current datasets is unknown, thorough clinical assessment could reduce the likelihood of including content suggesting suicide risk authored by individuals whose actual risk is low or negligible. This should allow the new models to effectively distinguish whether the textual information containing claims of suicidal thoughts and behavior was made by an individual with actual desire and intention to end their own life. If this feature can be achieved without decreasing the sensitivity of the detection system, it would be most desirable as a means for reasonable resource allocation. There is a phenomenon known as "parasuicide", and suicide threats made without suicidal intentions are a common occurrence [\[35\]](#page-7-18). With clinical assessment, the risk status would be validated more rigorously compared to the traditional annotation of posts and comments,

The value of many predictors, such as prior suicide attempts, their frequency and lethality, acute psychological distress, the presence of mental or physical disorders, access to lethal means, and others, is generally well established [\[1\]](#page-6-0), [\[33\]](#page-7-16), [\[34\]](#page-7-17). The crucial point is that many of these factors are considered predictive when they co-occur, with only several considered highly predictive on their own. In clinical practice, the presence of many factors can be established by simply asking more follow-up questions. The data not only reflects online activity but can also encompass medical information such as the onset, severity of symptoms, and history of suicide attempts, thereby providing a more comprehensive profile of individual risk factors. This does not hold for social media, where users typically disclose information they find personally significant or respond to comments that are rarely made by mental health professionals.

Moreover, this approach could enable the development of models capable of detecting subtle patterns that may elude human annotators. Not all individuals experiencing suicidal ideation or attempts explicitly communicate them online. However, their overall activity – although seemingly unrelated to suicide behavior – may still contain indicators that can be leveraged for risk prediction.

A significant challenge with this proposed approach is the inclusion of populations of individuals who have died by suicide and those at risk who do not engage with mental health services – both of whom are critical for achieving a representative dataset. Furthermore, implementing this strategy would require collaboration between data scientists and healthcare institutions, patient consent, willingness to share relevant information (e.g., social media usernames), and approval from the appropriate bioethical committee. Additionally, low patient participation could limit the feasibility of such a dataset.

A meta-analysis of 71 studies concluded that using suicidal ideation as a test for later suicide is limited [\[36\]](#page-7-19). This can suggest that the absence of reported suicidal thoughts is not a definitive indicator of safety. It is noteworthy that the included studies relied on ideations reported by medical personnel, which the authors acknowledged may have underestimated cases where suicidal thoughts emerged only shortly before the suicide. It is plausible that online anonymity may encourage individuals to disclose suicidal thoughts and behaviors more openly than they would in clinical settings, potentially making online expressions of suicidal ideation a more valuable and dynamic marker compared to those obtained during clinical interviews.

It remains uncertain whether a dataset developed to recruit patients would turn out better than the existing resources. Nevertheless, even if it proves less effective, such findings would have significant implications for future research and the development of new datasets. Our goal is to collaborate with healthcare institutions and design a research protocol that adheres to ethical standards, ensuring the highest possible degree of anonymity and safety for participants. To the best of our knowledge, no such initiative has been undertaken to date.

## ACKNOWLEDGMENT

We want to express our gratitude to Ryszard Staruch for the discussion and for preparing scripts to use non-annotated labels. Unfortunately, we were unable to implement this approach in time.

We also extend our thanks to Piotr Jabło ´nski for suggesting some points to include in the Related Work section.

## REFERENCES

- <span id="page-6-0"></span>[1] E. D. Klonsky, A. M. May, and B. Y. Saffer, "Suicide, suicide attempts, and suicidal ideation," *Annual review of clinical psychology*, vol. 12, no. 1, pp. 307–330, 2016.
- <span id="page-6-1"></span>[2] J. Li, X. Chen, Z. Lin, K. Yang, H. V. Leong, N. X. Yu, and Q. Li, "Suicide risk level prediction and suicide trigger detection: A benchmark dataset," *HKIE Transactions Hong Kong Institution of Engineers*, vol. 29, no. 4, pp. 268–282, 2022.
- <span id="page-6-2"></span>[3] A. Alambo, M. Gaur, U. Lokala, U. Kursuncu, K. Thirunarayan, A. Gyrard, A. Sheth, R. S. Welton, and J. Pathak, "Question answering for suicide risk assessment using reddit," in *2019 IEEE 13th International Conference on Semantic Computing (ICSC)*, 2019, pp. 468–473.
- <span id="page-6-3"></span>[4] M. Nock, G. Borges, E. Bromet, C. Cha, R. Kessler, and S. Lee, "Suicide and suicidal behavior. epidemiological reviews, 30, 133-154," 2008.
- <span id="page-6-4"></span>[5] A. M. Khalaf, A. A. Alubied, A. M. Khalaf, and A. A. Rifaey, "The impact of social media on the mental health of adolescents and young adults: a systematic review," *Cureus*, vol. 15, no. 8, 2023.
- <span id="page-6-5"></span>[6] A. Vaswani, "Attention is all you need," *Advances in Neural Information Processing Systems*, 2017.
- <span id="page-6-6"></span>[7] P. He, X. Liu, J. Gao, and W. Chen, "Deberta: Decoding-enhanced bert with disentangled attention," *arXiv preprint arXiv:2006.03654*, 2020.
- <span id="page-6-7"></span>[8] OpenAI, "GPT-4 technical report," Tech. Rep., 2023. [Online]. Available:<https://cdn.openai.com/papers/gpt-4.pdf>
- <span id="page-6-8"></span>[9] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou *et al.*, "Chain-of-thought prompting elicits reasoning in large language models," *Advances in neural information processing systems*, vol. 35, pp. 24 824–24 837, 2022.
- <span id="page-6-9"></span>[10] T. B. Brown, "Language models are few-shot learners," *arXiv preprint arXiv:2005.14165*, 2020.
- <span id="page-6-10"></span>[11] Y. Li, Z. Yanqing, M. Zhang, Y. Deng, A. Geng, X. Liu, M. Ren, Y. Li, S. Chang, and X. Zhao, "HW-TSC at SemEval-2024 task 9: Exploring prompt engineering strategies for brain teaser puzzles through LLMs," in *Proceedings of the 18th International Workshop on Semantic Evaluation (SemEval-2024)*, A. K. Ojha, A. S. Do ˘gru ¨oz, H. Tayyar Madabushi, G. Da San Martino, S. Rosenthal, and A. Ros´a, Eds. Mexico City, Mexico: Association for Computational Linguistics, Jun. 2024, pp. 1646–1651. [Online]. Available:<https://aclanthology.org/2024.semeval-1.234>
- <span id="page-6-11"></span>[12] D. Demner-Fushman, S. Ananiadou, K. B. Cohen, J. Pestian, J. Tsujii, and B. Webber, Eds., *Proceedings of the Workshop on Current Trends in Biomedical Natural Language Processing*. Columbus, Ohio: Association for Computational Linguistics, Jun. 2008. [Online]. Available:<https://aclanthology.org/W08-0600>
- <span id="page-6-12"></span>[13] A. E. Alada˘g, S. Muderrisoglu, N. B. Akbas, O. Zahmacioglu, and H. O. Bingol, "Detecting suicidal ideation on forums: proof-of-concept study," *Journal of medical Internet research*, vol. 20, no. 6, p. e9840, 2018.
- <span id="page-6-13"></span>[14] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, "BERT: Pretraining of deep bidirectional transformers for language understanding," in *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)*, J. Burstein, C. Doran, and T. Solorio, Eds. Minneapolis, Minnesota: Association for Computational Linguistics, Jun. 2019, pp. 4171–4186. [Online]. Available:<https://aclanthology.org/N19-1423>

- <span id="page-7-1"></span><span id="page-7-0"></span>[15] A. Radford, "Improving language understanding by generative pretraining," 2018.
- [16] S. Long, R. Cabral, J. Poon, and S. C. Han, "A quantitative and qualitative analysis of suicide ideation detection using deep learning," *arXiv preprint arXiv:2206.08673*, 2022.
- <span id="page-7-2"></span>[17] Y. Liu, M. Ott, N. Goyal, J. Du, M. Joshi, D. Chen, O. Levy, M. Lewis, L. Zettlemoyer, and V. Stoyanov, "Roberta: A robustly optimized bert pretraining approach," 2019. [Online]. Available: <https://arxiv.org/abs/1907.11692>
- <span id="page-7-3"></span>[18] A. Zirikly, P. Resnik, O. Uzuner, and K. Hollingshead, "CLPsych ¨ 2019 shared task: Predicting the degree of suicide risk in Reddit posts," in *Proceedings of the Sixth Workshop on Computational Linguistics and Clinical Psychology*, K. Niederhoffer, K. Hollingshead, P. Resnik, R. Resnik, and K. Loveys, Eds. Minneapolis, Minnesota: Association for Computational Linguistics, Jun. 2019, pp. 24–33. [Online]. Available:<https://aclanthology.org/W19-3003>
- <span id="page-7-4"></span>[19] E. Mohammadi, H. Amini, and L. Kosseim, "Clac at clpsych 2019: Fusion of neural features and predicted class probabilities for suicide risk assessment based on online posts," in *Proceedings of the sixth workshop on computational linguistics and clinical psychology*, 2019, pp. 34–38.
- <span id="page-7-5"></span>[20] A. K. Ambalavanan, P. D. Jagtap, S. Adhya, and M. Devarakonda, "Using contextual representations for suicide risk assessment from internet forums," in *Proceedings of the sixth workshop on computational linguistics and clinical psychology*, 2019, pp. 172–176.
- <span id="page-7-6"></span>[21] M. Matero, A. Idnani, Y. Son, S. Giorgi, H. Vu, M. Zamani, P. Limbachiya, S. C. Guntuku, and H. A. Schwartz, "Suicide risk assessment with multi-level dual-context language and bert," in *Proceedings of the sixth workshop on computational linguistics and clinical psychology*, 2019, pp. 39–44.
- <span id="page-7-7"></span>[22] T. Ghosh, M. H. A. Banna, M. J. A. Nahian, M. N. Uddin, M. S. Kaiser, and M. Mahmud, "An attentionbased hybrid architecture with explainability for depressive social media text detection in bangla," *Expert Systems with Applications*, vol. 213, p. 119007, 2023. [Online]. Available: <https://www.sciencedirect.com/science/article/pii/S0957417422020255>
- <span id="page-7-8"></span>[23] S. L. Mirtaheri, S. Greco, and R. Shahbazian, "A self-attention tcn-based model for suicidal ideation detection from social media posts," *Expert Systems with Applications*, vol. 255, p. 124855, 2024.
- <span id="page-7-9"></span>[24] F. Haque, R. U. Nur, S. Al Jahan, Z. Mahmud, and F. M. Shah, "A transformer based approach to detect suicidal ideation using pre-trained language models," in *2020 23rd International conference on computer and information technology (ICCIT)*. IEEE, 2020, pp. 1–5.
- <span id="page-7-10"></span>[25] H. Metzler, H. Baginski, T. Niederkrotenthaler, and D. Garcia, "Detecting potentially harmful and protective suicide-related content on twitter: machine learning approach," *Journal of medical internet research*, vol. 24, no. 8, p. e34705, 2022.
- <span id="page-7-11"></span>[26] P. Boonyarat, D. J. Liew, and Y.-C. Chang, "Leveraging enhanced bert models for detecting suicidal ideation in thai social media content amidst covid-19," *Information Processing & Management*, vol. 61, no. 4, p. 103706, 2024.
- [27] D. Zhang, L. Zhou, J. Tao, T. Zhu, and G. Gao, "Ketch: A knowledgeenhanced transformer-based approach to suicidal ideation detection from social media content," *Information Systems Research*, 2024.
- [28] H. Ghanadian, I. Nejadgholi, and H. Al Osman, "Socially aware synthetic data generation for suicidal ideation detection using large language models," *IEEE Access*, 2024.
- <span id="page-7-12"></span>[29] D. Kodati and R. Tene, "Emotion mining for early suicidal threat detection on both social media and suicide notes using context dynamic masking-based transformer with deep learning," *Multimedia Tools and Applications*, pp. 1–24, 2024.
- <span id="page-7-13"></span>[30] H. Inan, K. Upasani, J. Chi, R. Rungta, K. Iyer, Y. Mao, M. Tontchev, Q. Hu, B. Fuller, D. Testuggine, and M. Khabsa, "Llama guard: Llm-based input-output safeguard for human-ai conversations," 2023. [Online]. Available:<https://arxiv.org/abs/2312.06674>
- <span id="page-7-14"></span>[31] T. Wolf, L. Debut, V. Sanh, J. Chaumond, C. Delangue, A. Moi, P. Cistac, T. Rault, R. Louf, M. Funtowicz, J. Davison, S. Shleifer, P. von Platen, C. Ma, Y. Jernite, J. Plu, C. Xu, T. Le Scao, S. Gugger, M. Drame, Q. Lhoest, and A. M. Rush, "Transformers: State-of-the-art natural language processing," in *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations*. Online: Association for Computational Linguistics, Oct. 2020, pp. 38–45. [Online]. Available: <https://www.aclweb.org/anthology/2020.emnlp-demos.6>

- <span id="page-7-15"></span>[32] F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, and E. Duch- ´ esnay, "Scikit-learn: Machine learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, 2011.
- <span id="page-7-16"></span>[33] L. Favril, R. Yu, A. Uyar, M. Sharpe, and S. Fazel, "Risk factors for suicide in adults: systematic review and meta-analysis of psychological autopsy studies," *BMJ Ment Health*, vol. 25, no. 4, pp. 148–155, 2022.
- <span id="page-7-17"></span>[34] C. H. K. Park, J. W. Lee, S. Y. Lee, J. Moon, D.-W. Jeon, S.-H. Shim, S.-J. Cho, S. G. Kim, J. Lee, J.-W. Paik *et al.*, "Suicide risk factors across suicidal ideators, single suicide attempters, and multiple suicide attempters," *Journal of psychiatric research*, vol. 131, pp. 1–8, 2020.
- <span id="page-7-18"></span>[35] S. S. Welch, "A review of the literature on the epidemiology of parasuicide in the general population," *Psychiatric services*, vol. 52, no. 3, pp. 368–375, 2001.
- <span id="page-7-19"></span>[36] C. M. McHugh, A. Corderoy, C. J. Ryan, I. B. Hickie, and M. M. Large, "Association between suicidal ideation and suicide: meta-analyses of odds ratios, sensitivity, specificity and positive predictive value," *BJPsych open*, vol. 5, no. 2, p. e18, 2019.

## Metadata Summary
### Research Context
- **Research Question**: Which natural language processing method would work best for suicide risk detection on social media while balancing accuracy and practical deployment constraints?
- **Methodology**: Used three transformer model configurations including fine-tuned DeBERTa base and large models, GPT-4o with few-shot prompting and Chain of Thought reasoning, fine-tuned GPT-4o model, evaluated on Reddit-sourced dataset with 2,000 posts.
- **Key Findings**: Fine-tuned GPT-4o achieved highest performance with weighted F1 score of 75.5%, achieved second place in IEEE BigData 2024 Cup, demonstrated that general-purpose models can achieve state-of-the-art results with minimal specialized tuning.

### Analysis
- **Limitations**: Dataset restricted to Reddit posts, collected during COVID-19 pandemic creating potential temporal bias, limited contextual information available, potential bias in data collection methodology.
- **Future Work**: Develop dataset based on clinical assessments, collaborate with healthcare institutions for validation, expand to multi-platform analysis for comprehensive risk assessment.