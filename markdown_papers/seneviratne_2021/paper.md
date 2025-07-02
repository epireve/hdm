---
cite_key: seneviratne_2021
title: Personal Health Knowledge Graph for Clinically Relevant Diet Recommendations
authors: Oshani Seneviratne, Jonathan Harris, Hua Chen
year: 2021
doi: 10.2337/dc20-Sint.
date_processed: '2025-07-02'
phase2_processed: true
original_folder: arxiv_2110.10131_Personal_Health_Knowledge_Graph_for_Clinically_Rel
images_total: 1
images_kept: 1
images_removed: 0
tags:
- Electronic Health Records
- Healthcare
- Knowledge Graph
- Machine Learning
- Patient Engagement
- Personal Health
- Recommendation System
- Semantic Web
- Temporal
keywords:
- 1 introduction
- 2 related work
- 5 dietary guidelines modeling
- 52 semantic reasoner in action
- 61 performance
- 62 behavioral recommendations
- 63 food recommendations
- 7 conclusion
- ConsistentCarbDietDirective
- ConsistentCarbPattern
- ConsistentCarbRecommendation
- ConsistentCarbohydrateIntake
- ConsistentPattern
- DiabeticLowFatHigCarbDietConsumption
- DiabeticStatusAssessment
- DietConsumption
- DietaryAssessment
- EHR
- artificial intelligence
- ceur-ws
- ching-hua
- co-located
- co-occur
- code and data availability
- community-defined
- cooking methodology
- data-mining
- day-to-day
- deep learning
- electronic health record
---

# Personal Health Knowledge Graph for Clinically Relevant Diet Recommendations

Oshani Seneviratne*<sup>1</sup>* , Jonathan Harris*<sup>1</sup>* , Ching-Hua Chen*<sup>2</sup>* and Deborah L. McGuinness*<sup>1</sup>*

*<sup>1</sup>Rensselaer Polytechnic Institute, 110 8th Street, Troy NY 12180, USA*

*<sup>2</sup> Center for Computational Health, IBM Research, Yorktown Heights, NY, USA*## Abstract

We propose a knowledge model for capturing dietary preferences and personal context to provide personalized dietary recommendations. We develop a knowledge model called the Personal Health Ontology, which is grounded in semantic technologies, and represents a patient's combined medical information, social determinants of health, and observations of daily living elicited from interviews with diabetic patients. We then generate a personal health knowledge graph that captures temporal patterns from synthetic food logs, annotated with concepts from the Personal Health Ontology. We further discuss how lifestyle guidelines grounded in semantic technologies can be reasoned with the generated personal health knowledge graph to provide appropriate dietary recommendations that satisfy the user's medical and other lifestyle needs.

### Keywords

knowledge representation, personal health, dietary recommendations, guideline modeling

## 1. Introduction

Chronic illnesses typically involve multiple healthcare specialists over an extended period. Relying on Electronic Health Records (EHR) alone to understand the health status of a person with a chronic illness could result in an incomplete picture of patient profiles [\[1\]](#page-5-0). Such an incomplete picture is not only due to disconnected EHR systems being used by different healthcare providers, but also due to incomplete data from Observations of Daily Living (ODL) [\[2\]](#page-5-1) and Social Determinants of Health (SDoH) [\[3\]](#page-6-0). Many chronic illnesses, such as Type 2 Diabetes (T2D), impose a significant burden on patients to self-manage their disease, requiring health behavior change, health status monitoring with robust ODL mechanisms, medication adherence, and patient self-management behaviors that may require comprehensive education. Most clinicians focus their efforts on medical care while expecting patients to take on the responsibility of lifestyle modifications, including healthy eating. Therefore, using nutritional behavior as a focus, we demonstrate how semantic modeling of nutritional guidelines and semantic reasoners can utilize the Personal Health Knowledge Graph (PHKG) to provide personalized insights for T2D self-management consistent with clinical guidelines. Our PHKG is annotated using the Personal Health Ontology (PHO) developed for capturing lifestyle behaviors related

[0000-0001-8518-917X](https://orcid.org/0000-0001-8518-917X) (O. Seneviratne); [0000-0002-1020-0861](https://orcid.org/0000-0002-1020-0861) (C. Chen); [0000-0001-7037-4567](https://orcid.org/0000-0001-7037-4567) (D. L. McGuinness) © 2021 Copyright for this paper by its authors. Use permitted under Creative Commons License Attribution 4.0 International (CC BY 4.0).

CEUR Workshop Proceedings [\(CEUR-WS.org\)](http://ceur-ws.org)

to food consumption. Furthermore, using an application that captures summarized food logs annotated with concepts from our FoodKG [\[4\]](#page-6-1) and our PHO-annotated PHKG, we run a semantic reasoner to generate clinically relevant dietary recommendations for the user as demonstrated in Figure [1.](#page-1-0)

## 2. Related Work

A Personal Knowledge Graph (PKG) as defined by [Ba](#page-6-2)[log and Kenter](#page-6-2) is viewed as a consolidated resource that stores unique entities, which may additionally be linked to external sources and contains entities that do not exist in any other knowledge graphs [\[5\]](#page-6-2). The research proposal set out by [Balog and Kenter](#page-6-2) for PKGs further outlines several key differences between personalized KGs and personal KGs. Personalized KGs do not go beyond a general-purpose KG, but rather customize it in some way to match a user's need or profile. Personal KGs, on the other hand, contain a set of entities with links to other KGs, capturing many aspects centered around a user. Such personalization is essential when providing clinically relevant dietary recommendations for an individual, which is our work's focus. For example, [Balog](#page-6-2) [and Kenter](#page-6-2) highlights that PKG relations may often be short-lived (e.g. "what I plan on cooking tonight"). In our PHO, we capture the semantics that can potentially answer such questions.

Extending the PKGs to the health domain, [Gyrard et al.](#page-6-3) define Personal*Health*Knowledge Graph to include information about people, including their medical history, demographics, social information, and preferences [\[6\]](#page-6-3). The PHKG is then a subgraph of a larger KG that aggregates knowledge from heterogeneous sources, including
*Workshop on Personal Knowledge Graphs Co-located with the 3rd Automatic Knowledge Base Construction Conference (AKBC'21)* " [senevo@rpi.edu](mailto:senevo@rpi.edu) (O. Seneviratne); [harrij15@rpi.edu](mailto:harrij15@rpi.edu) (J. Harris); [chinghua@us.ibm.com](mailto:chinghua@us.ibm.com) (C. Chen); [dlm@cs.rpi.edu](mailto:dlm@cs.rpi.edu) (D. L. McGuinness)

![](_page_1_Figure_0.jpeg)
<!-- Image Description: This flowchart illustrates a dietary recommendation system. User input (personal health record and food log) and domain expert knowledge (dietary guidelines) are processed via time series summarization and knowledge representation. A semantic reasoner integrates this data with personal health and food knowledge graphs to generate dietary recommendations. The system's architecture is shown as a series of interconnected components, visually representing data flow and processing steps. -->

<span id="page-1-0"></span>**Figure 1:**Overview of the System Generating Dietary Recommendations

medical datasets and IoT devices containing only information relevant to the user. However, given that broad definition, it is often impossible to determine what would be included and excluded from the graph, especially in a dietary recommendation setting.

The Healthy Lifestyle Support (HeLiS) Ontology [\[7\]](#page-6-4) integrates food and activity for personalized health monitoring scenarios and has been utilized in a mobile application that can be used by patients with chronic diseases such as T2D. However, the HeLiS ontology modeling primarily focuses on the specific foods and the activities the individuals must consume, not on the contextual elements that could be used to personalize any recommendations given to the patient.

The Ontology for Nutritional Studies (ONS) integrates the terms related to food description, medical science, genetics, genomics data, and nutritional science methods for diet and health research [\[8\]](#page-6-5). The ONS was developed to harmonize biochemical, genetic, clinical, and nutritional concepts typically found in intervention and observational studies in human nutrition that can assist nutrition researchers by selecting the appropriate terms from a wide range of existing ontologies and creating the relevant missing key concepts for the field. While this ontology contains a lot of information about human nutrition, due to the focus of observational studies, it is not straightforward to use it for dietary recommendations. In addition, the Bionutrition Ontology (BNO) represents a controlled vocabulary of nutritional terms [\[9\]](#page-6-6). However, the BNO lacks proper annotation of terms or definitions of properties and lacks orthogonality (i.e., no terms are

imported or refer to external ontologies). Many of these limitations were addressed in the design of the PHO described in Section [3.](#page-1-1)

## <span id="page-1-1"></span>3. Personal Health Ontology (PHO)

Based on a set of interviews conducted with 21 people who declared themselves to be within five years of being diagnosed with T2D, we developed the PHO to characterize the dietary behaviors of people with T2D, with the expectation that the PHO would be extended to other aspects of personal health in the future.

First, we extracted answers from the interview transcripts and categorized them into concepts that capture the nutritional questions and concerns of people with diabetes. Special care was taken not to include general knowledge questions about food*("What is Tahini made of?")*, as that could be answered by our FoodKG [\[4\]](#page-6-1) directly without any personalization. The categories include:

- 1. **Likes** *(I prefer spicy food. Suggest a good breakfast with chilies.)*- 2.**Dislikes** *(I do not like peanuts. Suggest a snack without peanuts.)*- 3.**Nutrient-focused** *(Can you suggest Indian recipes with fewer calories [due to my T2D condition]?)*- 4.**Substitution** *(What should I eat instead [due to my T2D condition]?)*- 5.**Restaurant Knowledge** *(To keep to my dietary regimen, what restaurants should I go to?)*- 6.**Cooking Methodology** *(What dishes could I prepare with the appliances I have in my kitchen?)*- 7.**Financial** *(Are there cheaper menu items that I can eat?)*- 8.**Medical Condition** *(Can you suggest recipes that would limit my vitamin K intake?)*Second, we put a particular emphasis on the following aspects that were underlying themes across many of the questions and answers of the participants.
**Context:**It might be that little more is known about an entity than its type and the relation to the user. For example, the likes and dislikes of the user can be ascertained by looking at the foods that co-occur in the food log. The favorite food type can be determined by looking at the frequency of the meal. The PHKG should not contain all the possible entity attributes but only those important to the user in a given context. To encode such types of context, we primarily used the concepts and relationships from the Provenance (prov) ontology [\(https://www.w3.org/TR/prov-o\)](https://www.w3.org/TR/prov-o).
**Time:**Well-established and relatively stable relationships over time are essential criteria to be considered for inclusion in the PHKG. Therefore, we defined concepts such as ConsistentPattern to capture temporal patterns to identify the user's behaviors to either suggest similar foods (if they are healthy options) or alternate foods (if they are not appropriate given the user's specific health condition).
**Likelihood Estimates:** In some cases, it would be desirable to include the likelihood of a personal recommendation or the temporal patterns mined from their food logs to someone. For those purposes, we utilize several concepts from community-defined ontologies. Examples include the coefficientOfVariation concept from the Statistics Ontology (stato) [\(http://stato-ontology.](http://stato-ontology.org) [org\)](http://stato-ontology.org), and frequency from the Semantic-science Integrated Ontology (sio) [\(https://bioportal.bioontology.org/](https://bioportal.bioontology.org/ontologies/SIO) [ontologies/SIO\)](https://bioportal.bioontology.org/ontologies/SIO).

## <span id="page-2-0"></span>4. Personal Health Knowledge Graph (PHKG) Generation

Utilizing an extended Time Series Summarization (TSS) framework [\[10\]](#page-6-7) on synthetic food logs, we generated behavioral insights annotated with the PHO to generate the PHKG focusing on dietary behaviors of users. The TSS framework was previously designed to automatically generate natural language summaries of temporal personal health data utilizing advanced temporal data-mining techniques, such as frequent pattern mining and categorical clustering methods, to surface comprehensible and meaningful explanations to a non-expert

user [\[10\]](#page-6-7). We extended this framework to generate RDF triples based on temporal patterns found within the data. The patterns discovered are related to the constraints mentioned by T2D patients within the user study mentioned above. Instead of the natural language summaries that would be output from the TSS, we utilize the PHO concepts to capture the temporal patterns in the PHKG as RDF triples. The food log was gathered from synthetic data spanning five weeks at the meal-level granularity using the MyFitnessPal schema. For each meal, we have the nutrient information of the food consumed (i.e., nutrient consumption such as calorie intake) and the names of the foods consumed. Since our goal is to recommend clinically relevant diet recommendations, we focus on temporal patterns on nutrient intake, such as the recommendation to maintain a consistent carbohydrate intake, such as the following temporal summary.

|  | Listing 1: RDF representation for "This past full week |
|--|--------------------------------------------------------|
|  | (starting from Sep 23 and ending on Sep 30, you        |
|  | have kept your carbohydrate intake relatively          |
|  | fixed (or consistent)."                                |

|   | 1 :user a prov:Person.                   |
|---|------------------------------------------|
|   | 2 :user sio:hasAttribute :               |
|   | ConsistentCarbohydrateIntake.            |
|   | 3 :ConsistentCarbohydrateIntake a stato: |
|   | coefficientOfVariation;                  |
| 4 | sio:hasValue "0.99"^^xsd:float;          |
| 5 | prov:startedAtTime "2021-09-23T00        |
|   | :00:00-00:00"^^xsd:dateTime;             |
| 6 | prov:endedAtTime "2021-09-30T00          |
|   | :00:00-00:00"^^xsd:dateTime.             |

A user whose dietary preference is to maintain a lowcarb, high-fat diet would be interested in a summary that specifies how frequently they have been consistent with a low-carb, high-fat diet. The concepts LowCarbDiet, and highFatDiet are defined in the PHO to comprise of a diet either high or low of the corresponding macronutrient as advised by a subject matter expert. The extended-TSS uses these threshold values to determine if the temporal data pertaining to the diet is either a LowCarbDiet and/or highFatDiet, and labels it as such.

Listing 2: RDF representation for "*You have been maintaining a low-carb, high-fat diet.*"

- 1 :user sio:hasAttribute :LowCarbDiet, : highFatDiet.
- 2 :LowCarbDiet sio:frequency "1.0"^^xsd: float.
- 3 :HighFatDiet sio:frequency "1.0"^^xsd: float.

We can also go deeper by finding a relationship between low-carb and high-fat consumption

on a day-to-day basis using a relationship that encapsulates the consumption of the two types of macronutrients that would be captured in the :LowCarbHighFatNutrientIntakeGoal. A boolean value could indicate whether the user usually tends to exhibit either kind of consumption, as shown in Listing [3.](#page-3-0)

<span id="page-3-0"></span>Listing 3: RDF representation for "*You have been maintaining a low-carb, high-fat diet.*"

|   | 1 :user sio:hasAttribute :          |
|---|-------------------------------------|
|   | LowCarbHighFatNutrientIntakeGoal.   |
|   | 2 :LowCarbHighFatNutrientIntakeGoal |
| 3 | sio:hasParticipant :LowCarbDiet, :  |
|   | HighFatDiet;                        |
| 4 | sio:hasValue "true"^^xsd:boolean.   |

Our PHKG comprises patterns such as the ones described above captured as RDF triples, with a specific focus on foods consumed.

## 5. Dietary Guidelines Modeling

For T2D treatment and management, the American Diabetes Association (ADA) [\[11\]](#page-6-8) has generated a set of guidelines that includes the necessary guidance of dietary intake for people with diabetes or pre-diabetes. As such, the ADA clinical practice guideline contains several *chapters*, such as "Classification and Diagnosis of Diabetes" [\[12\]](#page-6-9) that includes information on characterizing diabetes, "Prevention or Delay of Type 2 Diabetes" [\[13\]](#page-6-10) that includes lifestyle interventions, among others, to guide pre-diabetic individuals, and "Pharmacologic Approaches to Glycemic Treatment" [\[14\]](#page-6-11) that contains information for managing T2D with medications.

In this section, we describe the semantic modeling of two selected ADA guideline recommendations focused on dietary recommendations. Each ADA guideline recommendation was captured in two parts: (1) rule indicates the necessary and sufficient conditions for a guideline to be in a compliant state, and (2) directive indicates what action to take if the rule was evaluated to be non-compliant.

### <span id="page-3-1"></span>5.1. Example Guidelines

#### Guideline 1: Guideline 1:

*"For pre-diabetic and diabetic individuals, diet low in total fat but relatively high in carbohydrates should be replaced with Mediterranean diet."*The semantic encoding of this guideline contains the rules (conditions) for when this recommendation should be valid can be identified. These include (i) the person has T2D or pre-diabetes (since we are applying the rule from ADA), (ii) the person is consuming a diet, and (iii) the diet is classified as a HighCarbDiet and LowFatDiet. In addition, the recommended action specifies that the diet should be replaced with a Mediterranean diet.

```text
Listing 4: OWL expression of Guideline 1.
1 Class: Diabetic
2 EquivalentTo:
3 DietaryAssessment and
4 prov:wasAssociatedWith some prov:
         Person and
5 prov:wasAssociatedWith doid:
         Diabetes or doid:PreDiabetes
6 SubClassOf:
7 DiabeticStatusAssessment
8 Class:
      DiabeticLowFatHigCarbDietConsumption
9 EquivalentTo:
10 Diabetic and
11 sio:hasAttribute some
12 (ConsistentPattern
13 and (sio:hasAttribute only
14 (HighCarbDiet and
                 LowFatDiet)))
15 SubClassOf:
16 DietConsumption

18 Class: MediterraneanDietDirective
19 EquivalentTo:
20 prov:wasAssociatedWith some
21 (sio:hasAttribute some
          DiabeticLowFatHigCarbDietConsumption
           and
          MediterraneanDietRecommendation
          )
22 SubClassOf:
23 Directive

25 Class: MediterraneanDietRecommendation
26 EquivalentTo:
27 Constraint only
28 "{tag: 'Mediterranean'}"
29 Annotations:
30 rdfs:label "For pre-diabetic and
         diabetic individuals diet low
         in total fat but relatively
         high in carbohydrates should be
          replaced with Mediterranean
         diet."
31 SubClassOf:
32 Recommendation
```text

#### Guideline 2:
*"For individuals whose daily insulin dosing is fixed, a consistent pattern of carbohydrate intake with respect to time and amount may be recommended to improve glycemic control and reduce the risk of hypoglycemia."*In the above rule, if a T2D patient is undergoing insulin therapy, they must have a consistent carbohydrate intake. The rule captures insulin intake and food consumption over a given period and determines whether the carbohydrate intake has been consistent. As demonstrated by the rule's OWL encoding in Listing [5,](#page-4-0) there is a temporal pattern descriptor (i.e., ConsistentCarbPattern) that is associated with the consistent consumption of an amount of carbohydrates during a particular meal (e.g., breakfast) as determined by the TSS. There are also specific personal characteristics of a user (i.e., Diabetes status and FixedInsulinDosage), all of which are modeled in the PHO and captured in the PHKG. The recommendation provides the required range as a personalized guideline constraint, which would be used in the downstream application in providing the relevant dietary recommendation.

Listing 5: OWL expression of Guideline 2.

```text
1 Class: FixedInsulinDosage
2 EquivalentTo:
3 sio:hasAttribute dron:Insulin,
4 FixedMedicationDosage

6 Class: ConsistentCarbPattern
7 EquivalentTo:
8 ConsistentPattern and
9 (sio:hasAttribute some food:
         Carbohydrates)

11 Class: ConsistentCarbDietDirective
12 EquivalentTo:
13 Diabetic and
14 (sio:hasAttribute some
         FixedInsulinDosage) and
15 (sio:hasAttribute some
         ConsistentCarbPattern) and
16 prov:wasAssociatedWith some
17 (sio:hasAttribute some
          ConsistentCarbRecommendation)

19 Class: ConsistentCarbRecommendation
20 EquivalentTo:
21 Constraint only
22 "{'carbohydrate' :
23 {'unit': 'g',
24 'meal' :
25 {'type': 'range',
26 'lower' : '30',
27 'upper': '45'},
28 'daily total' : '150'}}" .
29 Annotations:
30 rdfs:label "For individuals whose
         daily insulin dosing is fixed,
         a consistent pattern of
         carbohydrate intake with
         respect to time and amount may
         be recommended to improve
         glycemic control and reduce the
```text

#### 5.2. Semantic Reasoner in Action

Using the guideline rules modeled in Section [5.1](#page-3-1) on the PHKG generated in Section [4,](#page-2-0) we can generate directives that provide clinically relevant dietary recommendations. Specifically, the semantic reasoner would assert a specific subclass of the Directive (e.g., MediterraneanDietDirective or ConsistentCarbDietDirective). These asserted directives would be associated with a certain Recommendation (e.g., MediterraneanDietRecommendation and ConsistentCarbRecommendation), that would inform a downstream application how to provide an appropriate recommendation. We provide several questions that could be translated into SPARQL and evaluated with the insights generated from the semantic reasoner in Section [6.](#page-4-1)

## <span id="page-4-1"></span>6. Evaluation with Competency Questions

We utilize a competency question-based evaluation methodology [\[15\]](#page-6-12) for evaluating the PHKG generated. Below, we describe three types of questions and how the answers can be derived from the PHKG. All of these questions have a corresponding SPARQL representation. In a similar vein, as long as a natural language question can be represented using the terms available in the PHO, an answer can be derived.

### 6.1. Performance

These types of questions take the following form:

- 1.**Progress:** *("How have I been doing (improving, getting worse, maintaining) over the past day/week?)"*- 2.**Consistency:** *("Have I been consistent in my carbohydrate intake?")*- 3.**Compliance:** *("Have I been following a Mediterranean diet?")*To answer these types of questions related to the user's performance, we need to focus on how well their dietary intake matches up with the guidelines within a certain period. For example, the user may be struggling to maintain a consistent carbohydrate intake over the past week because they have been missing breakfast. In such a scenario, a question such as #1 above can be answered by discovering patterns within relevant temporal personal health data and deciding which of these may be the most important to surface to the user.

#### 6.2. Behavioral Recommendations

- 1.**Improve Diet:** *("How can I improve my diet strategy (considering personal preferences and context)?")*- 2.**Improve Performance:** *("Will my current diet strategy improve my performance?")*- 3.**Satisfying Preferences:** *("Does my current diet strategy meet my preferences?")*To successfully answer these questions, we include the user's personal preferences and context in the PHKG. For example, if the user cannot eat breakfast due to their demanding daily schedule, the system has to come up with alternatives to alleviate this problem by recommending different carbohydrate amounts for lunch and dinner or recommend mid-morning snacks.

#### 6.3. Food Recommendations

- 1.**Use Implicit Knowledge:** *("What should I eat for breakfast?")*- 2.**Allergies:** *("What foods can I eat if I have a dairy allergy?")*- 3.**Dislikes:** *("What can I substitute for almonds?")*For question #1 above, even though the question appears generic, using the PHKG, we augment the question with some implicit knowledge available in the PHKG and expand the question to a form such as*"What should I eat for breakfast [diabetic, prefers spicy food, carbohydrates between 30-45 g, not to exceed 150 g daily total]?"*. The constraints that go inside the "[]" are determined using a semantic reasoner (in our workflow, we used the in-built reasoner in Protégé [\[16\]](#page-6-13), and OWLReady2 [\[17\]](#page-6-14) for this purpose). The semantic reasoner evaluates the PHKG against the guidelines to generate the user's dietary needs and preferences. These will be in the form of personalized guideline constraints that provide input to downstream machine learning tasks such as recipe recommendations. In conjunction with the FoodKG [\[4\]](#page-6-1) containing over 1 million recipes, ingredients, and nutrients, we can then recommend an appropriate food item either using SPARQL queries or deep learning based personalized food recommendation methods such as pFoodReq [\[18\]](#page-6-15). Both of these approaches would be able to leverage the food preferences, eating habits encoded in the PHKG, and the dietary guidelines or restrictions as appropriate for the user. Questions #2 and #3 would follow the same process and include the explicit constraints (i.e., allergies and dislikes) stated explicitly.

## 7. Conclusion

There is a need for a system capable of discovering dietary insights hidden in a user's temporal personal health

data, such as food logs, and understanding these insights within the user's health context to provide relevant lifestyle recommendations and potentially lead to a personalized dialog. Utilizing the extended time series summarization technique, we generate a Personal Health Knowledge Graph (PHKG) annotated with the Personal Health Ontology for capturing such dietary behaviors. The PHKG, when reasoned using a semantic reasoner, provides performance evaluations against selected lifestyle management guidelines defined by the ADA on appropriate eating habits for the individual.

Our PHKG is different from a regular PKG because it can be readily used in clinically relevant dietary recommendation applications. The expressivity of the semantic rule representation and the reasoning process enables the recommendation of a food item to a T2D patient. Furthermore, because we have used standards-based ontological terms in the modeling process, the PHKG achieves a high degree of interoperability.

This work could be extended to be used in downstream applications on personalized food recommender systems that utilize task-oriented dialogue such as [\[19\]](#page-6-16). Furthermore, even though we have focused on food in this initial modeling of a PHKG, we can adopt a similar approach to extend this work to other domains related to personal health, such as activity, medication intake, and even social determinants of health. We plan on addressing the many challenges that remain in collecting, managing, integrating, and analyzing the data required to populate, maintain, reason over, explain, and share the PHKG, which makes this an exciting area of research.

### Code and Data Availability

The Personal Health Ontology, the Extended Time Series Summarization framework, the synthetic Personal Health Knowledge Graph, and the competency questions, along with sample answers, are available at [https:](https://semantics-for-personal-health.github.io) [//semantics-for-personal-health.github.io.](https://semantics-for-personal-health.github.io)

## Acknowledgments

This work is supported by IBM Research AI through the AI Horizons Network.

## References

- <span id="page-5-0"></span>[1] J. M. Madden, M. D. Lakoma, D. Rusinak, C. Y. Lu, S. B. Soumerai, Missing clinical and behavioral health data in a large electronic health record (EHR) system, Journal of the American Medical Informatics Association 23 (2016) 1143– 1149.
- <span id="page-5-1"></span>[2] U. Backonja, K. Kim, G. R. Casper, T. Patton, E. Ramly, P. F. Brennan, Observations of daily living: putting the "personal" in personal health records, American Medical Informatics Association 2012 (2012).

- <span id="page-6-0"></span>[3] A. V. D. Roux, M. Katz, D. C. Crews, D. Ross, N. Adler, Social and behavioral information in electronic health records: new opportunities for medicine and public health, American journal of preventive medicine 49 (2015) 980–983.
- <span id="page-6-1"></span>[4] S. Haussmann, O. Seneviratne, Y. Chen, Y. Ne'eman, J. Codella, C.-H. Chen, D. L. McGuinness, M. J. Zaki, Foodkg: a semanticsdriven knowledge graph for food recommendation, in: International Semantic Web Conference, Springer, 2019, pp. 146–162.
- <span id="page-6-2"></span>[5] K. Balog, T. Kenter, Personal knowledge graphs: A research agenda, in: Proceedings of the 2019 ACM SIGIR International Conference on Theory of Information Retrieval, 2019, pp. 217– 220.
- <span id="page-6-3"></span>[6] A. Gyrard, M. Gaur, S. Shekarpour, K. Thirunarayan, A. Sheth, Personalized health knowledge graph, in: Contextualized Knowledge Graph (CKG) Workshop International Semantic Web Conference (ISWC) 2018, LNCS, LNCS, Monterey, California, USA, 2018.
- <span id="page-6-4"></span>[7] M. Dragoni, T. Bailoni, R. Maimone, C. Eccher, Helis: An ontology for supporting healthy lifestyles, in: International Semantic Web Conference, Springer, 2018, pp. 53–69.
- <span id="page-6-5"></span>[8] F. Vitali, R. Lombardo, D. Rivero, F. Mattivi, P. Franceschi, A. Bordoni, A. Trimigno, F. Capozzi, G. Felici, F. Taglino, et al., Ons: an ontology for a standardized description of interventions and observational studies in nutrition, Genes & nutrition 13 (2018) 1–9.
- <span id="page-6-6"></span>[9] C. Yang, H. Ambayo, B. De Baets, P. Kolsteren, N. Thanintorn, D. Hawwash, J. Bouwman, A. Bronselaer, F. Pattyn, C. Lachat, An ontology to standardize research output of nutritional epidemiology: from paper-based standards to linked content, Nutrients 11 (2019) 1300.
- <span id="page-6-7"></span>[10] J. J. Harris, C.-H. Chen, M. J. Zaki, A framework for generating summaries from temporal personal health data, ACM Trans. Comput. Healthcare 1 (2021).
- <span id="page-6-8"></span>[11] American Diabetes Association, Introduction: Standards of medical care in diabetes—2020, Diabetes Care 43 (2020) S1–S2. URL: [https://doi.org/10.2337/dc20-Sint.](https://doi.org/10.2337/dc20-Sint)
- <span id="page-6-9"></span>[12] American Diabetes Association, Classification and diagnosis of diabetes: Standards of medical care in diabetes—2020, Diabetes Care 43 (2020) S14–S31. URL: [https://doi.org/10.2337/](https://doi.org/10.2337/dc20-S002) [dc20-S002.](https://doi.org/10.2337/dc20-S002)
- <span id="page-6-10"></span>[13] American Diabetes Association, Prevention or delay of type 2 diabetes: Standards of medical care in diabetes—2020, Diabetes Care 43 (2020) S32–S36. URL: [https://doi.org/10.2337/](https://doi.org/10.2337/dc20-S003) [dc20-S003.](https://doi.org/10.2337/dc20-S003)
- <span id="page-6-11"></span>[14] American Diabetes Association, Pharmacologic approaches to glycemic treatment: Standards of medical care in diabetes—2020, Diabetes Care 43 (2020) S98–S110. URL: [https:](https://doi.org/10.2337/dc20-S009) [//doi.org/10.2337/dc20-S009.](https://doi.org/10.2337/dc20-S009)
- <span id="page-6-12"></span>[15] Y. Ren, A. Parvizi, C. Mellish, J. Z. Pan, K. Van Deemter, R. Stevens, Towards competency question-driven ontology authoring, in: European Semantic Web Conference, Springer, 2014, pp. 752–767.
- <span id="page-6-13"></span>[16] M. A. Musen, The protégé project: A look back and a look forward, AI Matters 1 (2015) 4–12. URL: [https://doi.org/10.](https://doi.org/10.1145/2757001.2757003) [1145/2757001.2757003.](https://doi.org/10.1145/2757001.2757003) doi:[10.1145/2757001.2757003](http://dx.doi.org/10.1145/2757001.2757003).
- <span id="page-6-14"></span>[17] J.-B. Lamy, Owlready: Ontology-oriented programming in python with automatic classification and high level constructs for biomedical ontologies, Artificial intelligence in medicine 80 (2017) 11–28.
- <span id="page-6-15"></span>[18] Y. Chen, A. Subburathinam, C.-H. Chen, M. J. Zaki, Personalized food recommendation as constrained question answering over a large-scale food knowledge graph, in: Proceedings of the 14th ACM International Conference on Web Search and Data Mining, 2021, pp. 544–552.
- <span id="page-6-16"></span>[19] C. K. Joshi, F. Mi, B. Faltings, Personalization in goal-oriented

dialog, arXiv preprint arXiv:1706.07503 (2017).
