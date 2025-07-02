---
cite_key: giunchiglia_2017
title: A Context Model for Personal Data Streams ?
authors: Fausto Giunchiglia
year: 2017
doi: 10.48550/ARXIV.2205.10123
date_processed: '2025-07-02'
phase2_processed: true
original_folder: arxiv_2206.10212_A_Context_Model_for_Personal_Data_Streams
images_total: 1
images_kept: 1
images_removed: 0
tags:
- IoT
- Knowledge Graph
- Machine Learning
- Mental Health
- Natural Language Processing
- Semantic Web
---

# A Context Model for Personal Data Streams ?

Fausto Giunchiglia[0000 −0002 −5903 <sup>−</sup>6150], Xiaoyue Li B[0000 −0002 −0100 −0016] , Matteo Busso[0000 −0002 −3788 <sup>−</sup>0203], and Marcelo Rodas-Britez[0000 −0002 −7607 −7587]

Department of Information Engineering and Computer Science, University of Trento, Trento, Italy {fausto.giunchiglia, xiaoyue.li, matteo.busso,

marcelo.rodasbritez }@unitn.it

Abstract. We propose a model of the situational context of a person and show how it can be used to organize and, consequently, reason about massive streams of sensor data and annotations, as they can be collected from mobile devices, e.g. smartphones, smartwatches or fitness trackers. The proposed model is validated on a very large dataset about the everyday life of one hundred and fifty-eight people over four weeks, twenty-four hours a day.

Keywords: Personal Situational Context · Data Streams.

# 1 Introduction

A lot of prior work has focused on collecting and exploiting massive streams of data, e.g., sensor data and annotations. A first line of work has concentrated on using the streams of personal data for learning daily human behavior, including physical activity, see, e.g., [\[11\]](#page-7-0), assessment personality states, see, e.g., [\[12\]](#page-7-1), and visiting points of interest [\[3\]](#page-7-2). The Reality Mining project [\[4\]](#page-7-3) collected smartphone sensors, including call records, cellular tower IDs, and Bluetooth proximity logs to study students' social networks and daily activities. In the same vein, the StudentLife project [\[15,](#page-7-4)[9\]](#page-7-5) employed smartphone sensors and questionnaires as the means for inferring the mental health, academic performance, and other behavioral trends of university students, under different workloads and term progress. Slightly different in focus, but still based on the collection of streams of data, is the work on the Experience Sampling Method (ESM). The ESM is an intensive longitudinal social and psychological research methodology, where participants are asked to report their thoughts and behaviours [\[14\]](#page-7-6). Here the focus is not so much on learning from the sensor data but, rather, on collecting the user provided answers. In all this work, little attention has been posed on how to represent and manage these data streams. The most common solution has

<sup>?</sup> Xiaoyue receives funding from the China Scholarships Council (No.202107820014). Marcelo, Fausto and Matteo receive funding from the project "DELPhi - DiscovEring Life Patterns" funded by the MIUR (PRIN) 2017.

been that of collecting these data, as is, into (multiple) files in some common format, e.g. CSV. Which was good enough, given that data were exploited a posteriori, once the data collection was finished, by doing the proper off-line data analysis.

Our focus is on the exploitation of data, at run-time, while being collected, as the basis for supporting person-centric services, e.g., predicting human habits or better human-machine interaction. This type of services are in fact core for the development of human-in-the-loop Artificial Intelligence systems [\[2\]](#page-7-7). Towards this end, our proposed solution is to represent the input streams, no matter whether coming from sensors or from the user feedback, as sequences of personal situational contexts [\[7\]](#page-7-8). Here by context we mean "a theory of the world which encodes an individual's subjective perspective about it" [\[5](#page-7-9)[,6\]](#page-7-10). Many challenges still need to be solved towards this goal. For instance, these data are highly heterogeneous, e.g., categorical, numerical, in natural language, and unstructured, usually collected with different time frequencies. Furthermore, different data may be at different levels of abstraction, for instance the current location can be described as, e.g., GPS coordinates, my office, the University, or the city of Trento.

The main goal of this paper is to provide a representation of data streams at the knowledge level [\[10\]](#page-7-11), rather than only at the sensor or data level, fully understandable by the user, in the user terms, thus enabling the kind of Human-Machine interactions which we need. We realize this requirement by representing streams as sequences of situational contexts, and by modeling them as Knowledge Graphs (KGs) [\[1\]](#page-6-0). In this context, by KG we mean a graph where the nodes are the entities involved in the current user context, e.g., friends, the current location, the current event, for instance a meeting, while links are the relations occurring among entities, e.g., the fact that two people are classmates or that a person is on a car or talking to another person. Notice how various notions of context model have been proposed in the past. Some work focused on representing the current situation with reference to the location, see, e.g., [\[13\]](#page-7-12). Other approaches have used hierarchical context models [\[16\]](#page-7-13). However, these proposals did not deal with the problem of how to provide an abstract user-level representation of ever growing streams of data.

The proposed design the knowledge level representation of the personal situational context is articulated in three steps, as follows:

- 1. An abstract conceptualization of the notion of context in terms of the person space and time localisation plus the people and objects populating the context itself;
- 2. A schema of the KG, what we call an ETG (Entity Type Graph), which defines the data structure used the current situational context as it occurs in a certain period of time;
- 3. The actual data streams, memorised as sequences of context KGs each with the same ETG, differently populated.

The paper is organized as follows. Section [2](#page-2-0) formalizes the notion of situational context. Section [3](#page-4-0) described the details of the situational context KG. Section [4](#page-5-0) presents a large scale case study. Finally, in Section [5,](#page-6-1) we present our conclusions.

## <span id="page-2-0"></span>2 The Situational Context

A situational context represents a real world scenario from the perspective of a specific person, whom we call me, e.g., Mary. A Life sequence is a set of situational contexts during a certain period of time. We define the life sequence of me, S(me), as follows:

$$
S \ (me) = \langle C_1 \ (me) \ , C_i \ (me) \ , \dots \ , C_n \ (me) \rangle; \quad 1 \leq i \leq n \tag{1}
$$

where C<sup>i</sup> is the ith situational context of me. We assume that me can be in only one context at any given time, based on the fact that a person can be in only one location at any time. Hence, S is a sequence of me's contexts, occurring one after the other, strictly sequentially, with no time in between. In turn, we model the Situational context of me C(me) as follows:

$$
C(me) = \langle L(C(me)), E(L(C(me))) \rangle.
$$
 (2)

In the following, we drop the argument me to simplify the notation. L(C) is the (current) Location of me. L(C) defines the boundaries inside which the current scenario evolves. The location is an endurant, which is wholly present whenever it is present, and it persists in time while keeping its identity [\[6\]](#page-7-10). E(L(C)) is an Event within which me is involved. The event is a perdurant, which is composed of temporal parts [\[6\]](#page-7-10). L(C) and E(L(C)), as the priors of experience, define the scenario being modeled and the space-time volume within which the current scenario evolves. This is a consequence of the foundational modeling decision that contexts are the space-time prior to experience. In other words, the situational context of me is univocally defined by me's spatial position and temporal position. In practice, any electronic device can easily provide us with the spatial position (via GPS, annotations, etc.) and temporal position (via timestamp) of a person.

In a certain context, me can be inside one or multiple locations as follows:

$$
L(C) = \langle L_1(C), L_i(C), \dots, L_n(C) \rangle; \quad 1 \le i \le n \tag{3}
$$

where Li(C) is a spatial part of L(C), we call Li(C) is a sub-location of L(C). If me is inside one location, we have L(C) = L1(C) = · · · = Ln(C), and the context is static, e.g., Mary is at the university library, or Mary is at home. Otherwise, the context is dynamic, e.g., Mary travels around Trento (L(C)), going from the university (L1(C)), to the central station (L2(C)), and then to her home (L3(C)). Inside contexts, multiple events will occur:

$$
E(L(C)) = \langle E_1(L(C)), E_i(L(C)), \dots, E_n(L(C)) \rangle; \quad 1 \le i \le n \tag{4}
$$

where Ei(L(C)) is a part of E(L(C)). We call an Ei(L(C)) a sub-event of E(L(C)). Different sub-events may occur in parallel or be sequential or mixed, but a sub-event can not be part of another sub-event. A simple event is the event where E(L(C)) = E1(L(C)) = · · · = En(L(C)). A complex event is the event where there are multiple distinct sub-events.

Finally, the context contains various types of things interacting with one another. We define a Parts of a Context as follows:

$$
P(C) = \langle me, \{P\}, \{O\}, \{F\}, \{A\}\rangle
$$
 (5)

where {P} and {O} are, respectively, a set of persons (e.g., Bob) and objects (e.g., Mary's smartphone) populating the current context. {F} and {A} are, respectively, a set of functions and actions involving me, persons and objects. We define a Generic object G, consisting of me, {P}, and {O}, i.e., G = me ∪ {P}∪ {O}. Functions define the roles that different generic objects have towards one another [\[8\]](#page-7-14). Thus a person can be a friend with another person, a horse can be a transportation means for person, while a phone can be a communication medium among people. Functions are endurants. Actions model how generic objects G change in time [\[8\]](#page-7-14), e.g., Mary touches her smartphone in a certain moment, while she walks or eats at some other times. Actions are perdurants. Functions are characterized by the set of actions which enable them [\[8\]](#page-7-14). Thus for instance, the function friend might be associated with the actions talking to, helping, or listening to. Similarly, a smartphone (i.e., Ga) can be recognized as an entertainment tool for Mary (i.e., Gb), because the smartphone allows certain actions related to the entertainment of Mary, e.g., playing videos, playing music, etc. Hence, for two generic objects G<sup>a</sup> and Gb, in the context, we have the following:

$$
F(G_a, G_b) = \langle A_1(G_a, G_b), \dots, A_n(G_a, G_b) \rangle;
$$
 (6)

where a function F relates G<sup>a</sup> with Gb, namely, it is associated with the set of actions (A1, . . . , An) involving G<sup>b</sup> that G<sup>a</sup> can do or allow.

| Property types                                             | Entity types Location; Sub-location | Event; Sub-event Person; me |                              | Object                            |
|------------------------------------------------------------|-------------------------------------|-----------------------------|------------------------------|-----------------------------------|
| Spatial property: relating to or<br>occupying space        | Coordinates<br>Volume               | None                        | Coordinates                  | Coordinates                       |
| Temporal property: relating<br>to time                     | None                                | Start-EndTime               | None                         | None                              |
| Function property: indicating<br>attributes of functions   | Location functions                  | None                        |                              | Person functions Object functions |
| Action property: indicating<br>attributes of actions       | None                                | Person actions<br>None      |                              | Object actions                    |
| External property: relating to<br>outward features         | Name<br>ID                          | Name<br>ID                  | Name<br>ID<br>Gender         | Name<br>ID<br>Color               |
| Internal property: relating to<br>persons' internal states | None                                | None                        | InPain<br>InMood<br>InStress | None                              |

<span id="page-3-0"></span>Table 1. Properties of the principal Entity types of a situational context.

## <span id="page-4-0"></span>3 The Entity Type Graph

We define Location, Sub-location, Event, Sub-event and Generic object as Entity types (etypes), where an entity is anything which has a name and can be distinctly identified via its properties and where, in turn, an etype is a set of entities. Functions and Actions are modeled as Object properties representing the relations among Generic objects. In Table [1,](#page-3-0) we define and provide examples of Spatial, Temporal, External, and Internal data property types as well as of Function and Action object property types.

![](_page_4_Figure_3.jpeg)
<!-- Image Description: This image depicts an Entity-Relationship Diagram (ERD) for a data model. It shows entities like *Location*, *Event*, *Object*, and *Human*, with attributes specified for each. Relationships between entities are illustrated, such as "Part of" and "With," along with cardinality. Enumerations (e.g., *ColorEnum*, *GenderEnum*) define attribute value sets. The diagram likely serves to formally define the data structure used within the paper's system or application. -->

<span id="page-4-1"></span>Fig. 1. An example of ETG modeling the situational context.

We represent the schema of the situational context of me as an eType Graph (ETG), i.e., an Enhanced Entity-Relationship (EER) model. See Figure [1](#page-4-1) for a simplified version of an ETG representing a personal situational context. An ETG is a knowledge graph where nodes are etypes, decorated by data properties, which in turn are linked by object properties. Each etype (represented as a box) is decorated with its data properties. For example, the etype Human has the data property Gender, and the data type (the green box) of Gender is GenderEnum. Also, etypes are connected with object properties showing their relations (represented as rhombuses). One such example, is the relation With which in turn is associated its own cardinality. Finally, as from EER models, it is possible to have inheritance relations among he etypes, e.g., a Generic Object is specialized into Object and Human.

Given that a context is represented by a single ETG, we represent the evolution in time of the life of a person as a sequence of ETGs, each representing the state of affairs at a certain time and for a certain time interval. In turn, this sequence of ETGs is populated by the input data streams, where each element of the stream will populate the ETG for that time slot. Of course for each input stream there will be a dedicated suitable property for the proper etype. Thus, for instance, the GPS will populate the data property GPSLocation of the etypes person and/ or phone, while the label of a location, e.g., Trento will be used to create an object property link between the etype person and the etype location. Given the above, a life sequence, as defined in Section 2, is just a sequence of contexts satisfying a certain property, namely, a subset of the overall sequence of ETGs, populated by the input data streams. So for instance we may have Mary's life sequence of her moving around in Trento, see example above, or we can have the life sequence of all the times she has studied in her office at the University in the last year. Notice that this latter life sequence is composed of contexts which are not adjacent in time. This is a very powerful representational mechanism which can be used, for instance, to represent habits as (not necessarily adjacent) life sequences occurring recursively with a certain frequency.

# <span id="page-5-0"></span>4 Case Study

To validate the formalization described above, we describe how it can be used to represent the Smart University stream dataset (SU).[1](#page-5-1) The app used for the data collection is called iLog [\[18](#page-7-15)[,17\]](#page-7-16). The SU data set has been used in a large number of case studies, see, e.g., [\[19,](#page-7-17)[20\]](#page-7-18). SU has been collected from one hundred and fifty-eight university students over a period of four weeks. It contains 139.239 annotations and approximately one terabyte of data. The dataset is organized into multiple datasets, one for each me, where each dataset is associated with a unique identifier across all types of data. The annotations done by each me are generated every half-hour based on the answers of the participants to four closedended questions. Based on this, the best choice is to build a sequence of ETGs, one for every half an hour for each me. The four questions are "Where are you?", "What are you doing?", "With whom are you?", and "What is your mood?" and are based on the HETUS (Harmonized European Time Use Surveys) standard.[2](#page-5-2)

Figures [2](#page-6-2) and [3](#page-6-3) provide a small, clean and anonymized subset of SU. In both figures, the first part (in white) provides the timestamps when this data were collected. In the first figure, the location of me (in green) is represented together with some of her attributes (in orange). The second figure reports the current event (in yellow) in which me is involved, her function towards the person she is with (in red) and her phone with some of its attributes (in blue). It is easy to compare the contents of Figures [2](#page-6-2) and [3](#page-6-3) with the notions defined in the previous sections. Let us consider some examples:

– Human Entities: They are me and Person, both associated with External and Internal properties.

<span id="page-5-1"></span><sup>1</sup> See <https://livepeople.datascientia.eu/dataset/smartunitn2> for a detailed description of the dataset plus the possibility of downloading it.

<span id="page-5-2"></span><sup>2</sup> https://ec.europa.eu/eurostat/web/time-use-survey.

| Identifier of $me$ $\{14\}$<br>me |                                                    |        |         |                                    |     | Location {L}                               |                |                      |          |  |
|-----------------------------------|----------------------------------------------------|--------|---------|------------------------------------|-----|--------------------------------------------|----------------|----------------------|----------|--|
| id                                | timestamp                                          | gender | faculty | perceived stress extraversion mood |     | where                                      | latitude       | longitude            | accuracy |  |
|                                   | 14 2021-05-01 10:56:00 UTC Female Computer science |        |         | 23                                 | 25  | Bar, Pub, etc. 46.0670° N                  |                | $11.15$ °E           | 151      |  |
|                                   | 14 2021-05-01 10:57:00 UTC Female Computer science |        |         | 23 <sub>1</sub>                    | 251 | Bar, Pub, etc.                             | 46.0675° N     | 11.15°E              | 151      |  |
|                                   | 14 2021-05-01 10:58:00 UTC Female Computer science |        |         | 23                                 | 25  | Bar. Pub. etc.                             |                | 46.083° N 11.1632° E | 151      |  |
|                                   | 14 2021-05-01 10:59:00 UTC Female Computer science |        |         | 23                                 | 25  | Bar, Pub, etc.                             | $46.06°$ N     | 11.15° E             | 151      |  |
|                                   | 14 2021-05-01 11:00:00 UTC Female Computer science |        |         | 23                                 | 25  | 4 University Library                       | $46.1^\circ$ N | $11.2^{\circ}$ E     | 1230     |  |
|                                   | 14 2021-05-01 11:01:00 UTC Female Computer science |        |         | 23                                 | 25  | 4 University Library 46.0675° N            |                | 11.15° E             |          |  |
|                                   | 14 2021-05-01 11:02:00 UTC Female Computer science |        |         | 231                                | 25  | 4 University Library 46.0675° N            |                | 11.15°E              | 50       |  |
|                                   | 14 2021-05-01 11:03:00 UTC Female Computer science |        |         | 23                                 | 25  | 4 University Library 46.0668° N 11.1497° E |                |                      | 50       |  |
|                                   | 14 2021-05-01 11:04:00 UTC Female Computer science |        |         | 23                                 | 25  | 4 University Library 46.0668° N 11.1497° E |                |                      | 50       |  |
|                                   | 14 2021-05-01 11:05:00 UTC Female Computer science |        |         | 23                                 | 25  | 4 University Library                       | $46.067$ ° N   | 11.164°E             |          |  |
|                                   | 14 2021-05-01 11:06:00 UTC Female Computer science |        |         | 231                                | 25  | 4 University Library 46,0670° N            |                | $11.15^{\circ}$ F    | 160      |  |

A Context Model for Personal Data Streams 7

<span id="page-6-2"></span>

| Fig. 2. Me and the current location. |  |  |  |
|--------------------------------------|--|--|--|
|--------------------------------------|--|--|--|

|    | Identifier of $me$ $\{14\}$             | Event $\{E\}$   | Person {P(Other)} | Object {O} |           |    |  |                                                                          |
|----|-----------------------------------------|-----------------|-------------------|------------|-----------|----|--|--------------------------------------------------------------------------|
| id | timestamp                               | what            | with              |            |           |    |  | notification app name touch event wifi connection wifi network available |
|    | 14 2021-05-01 10:56:00 UTC Coffee Break |                 | Classmate(s)      |            | mail, sms | 44 |  | uni wifi Bob's Hotspot, uni wifi                                         |
|    | 14 2021-05-01 10:57:00 UTC Coffee Break |                 | Classmate(s)      |            |           |    |  | uni wifi Bob's Hotspot, uni wifi                                         |
|    | 14 2021-05-01 10:58:00 UTC Coffee Break |                 | Classmate(s)      |            |           |    |  | uni wifi Bob's Hotspot, uni wifi                                         |
|    | 14 2021-05-01 10:59:00 UTC Coffee Break |                 | Classmate(s)      |            |           |    |  | uni wifi Bob's Hotspot, uni wifi                                         |
|    | 14 2021-05-01 11:00:00 UTC              | Studying        | Classmate(s)      |            |           |    |  | uni wifi Bob's Hotspot, uni wifi                                         |
|    | 14 2021-05-01 11:01:00 UTC              | Studying        | Classmate(s)      |            | mail      | 32 |  | uni wifi Bob's Hotspot, uni wifi                                         |
|    | 14 2021-05-01 11:02:00 UTC              | Studying        | Classmate(s)      |            | mail      |    |  | uni wifi Bob's Hotspot, uni wifi                                         |
|    | 14 2021-05-01 11:03:00 UTC              | <b>Studying</b> | Classmate(s)      |            | mail      |    |  | uni wifi Bob's Hotspot, uni wifi                                         |
|    | 14 2021-05-01 11:04:00 UTC              | Studying        | Classmate(s)      |            | mail      |    |  | uni wifi Bob's Hotspot, uni wifi                                         |
|    | 14 2021-05-01 11:05:00 UTC              | Studying        | Classmate(s)      |            | mail      |    |  | uni wifi Bob's Hotspot, uni wifi                                         |
|    | 14 2021-05-01 11:06:00 UTC              | Studying        | Classmate(s)      |            | mail, sms | 8  |  | uni wifi Bob's Hotspot, uni wifi                                         |

<span id="page-6-3"></span>Fig. 3. The current event, the people and the object with Me.

- Human's External Properties: They are mainly collected synchronously and are represented by the variables "gender" and "faculty".
- Human's Internal Properties: They are both synchronic, i.e., "extraversion", and diachronic, i.e.,"mood".
- Location Entity: It is defined by "where" and it is annotated by the data properties "latitude" and "longitude" (with their respective "accuracy").

According to the research purpose, many additional data points may be used as proxies for characterizing the main notions of the context. For instance, concerning the Location, the WiFi router can be used as a proxy of a facility; a question posed in the online questionnaire about a daily routine can be a proxy of a travel path. By imputation on the GPS, it is possible to derive the Point Of Interest (POI), which can be understood as the set of Objects surrounding a given spatial coordinate. And so on.

## <span id="page-6-1"></span>5 Conclusion

This paper proposes a model of the situational context of a person and it shows how it can be used to provide a knowledge level representation over the data collected in time, both sensor data and user provided label, from mobile devices.

## References

<span id="page-6-0"></span>1. Bonatti, P.A., Decker, S., Polleres, A., Presutti, V.: Knowledge graphs: New directions for knowledge representation on the semantic web (dagstuhl seminar 18371). Schloss Dagstuhl-Leibniz-Zentrum fuer Informatik (2019)

- 8 Fausto Giunchiglia, Xiaoyue Li<sup>B</sup>, Matteo Busso, and Marcelo Rodas-Britez
- <span id="page-7-7"></span>2. Bontempelli, A., Britez, M.R., Li, X., Zhao, H., Erculiani, L., Teso, S., Passerini, A., Giunchiglia, F.: Lifelong personal context recognition (2022). [https://doi.org/10.48550/ARXIV.2205.10123,](https://doi.org/10.48550/ARXIV.2205.10123) [https://arxiv.org/abs/](https://arxiv.org/abs/2205.10123) [2205.10123](https://arxiv.org/abs/2205.10123)
- <span id="page-7-2"></span>3. Do, T.M.T., Gatica-Perez, D.: The places of our lives: Visiting patterns and automatic labeling from longitudinal smartphone data. IEEE Trans. on Mobile Computing 13(3), 638–648 (2013)
- <span id="page-7-3"></span>4. Eagle, N., Pentland, A.S.: Reality mining: sensing complex social systems. Personal and ubiquitous computing 10(4), 255–268 (2006)
- <span id="page-7-9"></span>5. Giunchiglia, F.: Contextual reasoning. Epistemologia, special issue: I Linguaggi e le Macchine 16, 345–364 (1993)
- <span id="page-7-10"></span>6. Giunchiglia, F., Bignotti, E., Zeni, M.: Personal context modelling and annotation. In: 2017 IEEE Int. PERCOM Workshops. pp. 117–122. IEEE (2017)
- <span id="page-7-8"></span>7. Giunchiglia, F., Britez, M.R., Bontempelli, A., Li, X.: Streaming and learning the personal context. In: Twelfth International Workshop Modelling and Reasoning in Context. p. 19 (2021)
- <span id="page-7-14"></span>8. Giunchiglia, F., Fumagalli, M.: Teleologies: Objects, actions and functions. In: International conference on conceptual modeling. pp. 520–534. Springer (2017)
- <span id="page-7-5"></span>9. Harari, G.M., M¨uller, S.R., Stachl, C., Wang, R., Wang, W., B¨uhner, M., Rentfrow, P.J., Campbell, A.T., Gosling, S.D.: Sensing sociability: Individual differences in young adults' conversation, calling, texting, and app use behaviors in daily life. Journal of personality and social psychology 119(1), 204 (2020)
- <span id="page-7-11"></span>10. Newell, A.: The knowledge level. Artificial intelligence 18(1), 87–127 (1982)
- <span id="page-7-0"></span>11. Patterson, K., Davey, R., Keegan, R., Freene, N.: Smartphone applications for physical activity and sedentary behaviour change in people with cardiovascular disease: A systematic review and meta-analysis. PloS one 16(10), e0258460 (2021)
- <span id="page-7-1"></span>12. R¨uegger, D., Stieger, M., Nißen, M., Allemand, M., Fleisch, E., Kowatsch, T.: How are personality states associated with smartphone data? European Journal of Personality 34(5), 687–713 (2020)
- <span id="page-7-12"></span>13. Schilit, B.N., Theimer, M.M.: Disseminating active map information to mobile hosts. IEEE network 8(5), 22–32 (1994)
- <span id="page-7-6"></span>14. Van Berkel, N., Ferreira, D., Kostakos, V.: The experience sampling method on mobile devices. ACM Computing Surveys (CSUR) 50(6), 1–40 (2017)
- <span id="page-7-4"></span>15. Wang, R., Chen, F., Chen, Z., Li, T., Harari, G., Tignor, S., Zhou, X., Ben-Zeev, D., Campbell, A.T.: Studentlife: assessing mental health, academic performance and behavioral trends of college students using smartphones. In: Proceedings of ACM - UBICOMP. pp. 3–14 (2014)
- <span id="page-7-13"></span>16. Wang, X.H., Da Qing Zhang, T.G., Pung, H.K.: Hk: Ontology based context modeling and reasoning using owl. In: PERCOMW'04. Citeseer (2004)
- <span id="page-7-16"></span>17. Zeni, M., Bison, I., Gauckler, B., Reis, F., Giunchiglia, F.: Improving time use measurement with personal big collection - the experience of the european big data hackathon 2019. Journal of Official Statistics (2020)
- <span id="page-7-15"></span>18. Zeni, M., Zaihrayeu, I., Giunchiglia, F.: Multi-device activity logging. In: Proceedings of ACM - UBICOMP: Adjunct Publication. pp. 299–302 (2014)
- <span id="page-7-17"></span>19. Zeni, M., Zhang, W., Bignotti, E., Passerini, A., Giunchiglia, F.: Fixing mislabeling by human annotators leveraging conflict resolution and prior knowledge. Proceedings of ACM - IMWUT 3(1), 1–23 (2019)
- <span id="page-7-18"></span>20. Zhang, W., Shen, Q., Teso, S., Lepri, B., Passerini, A., Bison, I., Giunchiglia, F.: Putting human behavior predictability in context. EPJ Data Science 10(1), 42 (2021)
