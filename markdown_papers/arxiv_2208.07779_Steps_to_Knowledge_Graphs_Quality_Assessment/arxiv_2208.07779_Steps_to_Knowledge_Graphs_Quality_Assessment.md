<!-- cite_key: 2012 -->

# Steps to Knowledge Graphs Quality Assessment

Elwin Huaman1[0000 −0002 −2410 −4977]

Semantic Technology Institute (STI) Innsbruck, Department of Computer Science, University of Innsbruck, Austria elwin.huaman@sti2.at

Abstract. Knowledge Graphs (KGs) have been popularized during the last decade, for instance, they are used widely in the context of the web. In 2012 Google has presented the Google's Knowledge Graph that is used to improve their web search services. The web also hosts different KGs, such as DBpedia and Wikidata, which are used in various applications like personal assistants and question-answering systems. Various web applications rely on KGs to provide concise, complete, accurate, and fresh answer to users. However, what is the quality of those KGs? In which cases should a Knowledge Graph (KG) be used? How might they be evaluated? We reviewed the literature on quality assessment of data, information, linked data, and KGs. We extended the current stateof-the-art frameworks by adding various quality dimensions (QDs) and quality metrics (QMs) that are specific to KGs. Furthermore, we propose a general-purpose, customizable to a domain or task, and practical quality assessment framework for assessing the quality of KGs.

Keywords: Knowledge Graph Assessment · Knowledge Graph Quality

## 1 Introduction

Large amounts of knowledge are used to power web applications, for instance, in 2012 the Google's Knowledge Graph was presented as means to improve the web search results of Google's search engine. In the same year, Wikidata KG is released as crowd-sourced, non-commercial, and open on the web. Furthermore, many other KGs are available on the web, either created semi-automatically (e.g. DBpedia) or automatically (e.g., NELL). However, an issue that comes with KGs is their quality. Incomplete or inconsistent statements are present in KGs, making them unreliable. Assessing the quality of KGs is a challenge since quality is conceived as fitness for use .

Quality may involve several dimensions, such as accessibility, accuracy, appropriate amount, and so on. However, in terms of KGs, few works were proposed. To face this challenge, we look at the literature on quality assessment and identified 20 QDs and several QMs based on the Goal Question Metric approach.

Furthermore, We propose a general-purpose, customizable to a use case or task, and practical quality assessment framework for KGs. Our approach involves (1) identifying users, use case, and KGs, (2) selection of QDs and QMs by means

of weights of importance, (3) performing the assessment of QMs, QDs, and total score for a KG, and (4) exploitation of the results.

This paper is structured as follows. Section [2](#page-1-0) provides a look into the literature on quality assessment. In Section [3,](#page-4-0) we list QDs that are applicable to KGs. A KG quality assessment framework is provided in Section [4.](#page-4-1) Finally, we conclude in Section [5,](#page-7-0) by summarizing our findings and future work plans.

### <span id="page-1-0"></span>2 Quality Assessment

In this section, we discuss the most relevant work on quality assessment over the past years that implies data, information, linked data, and KGs quality. In order to accurately define and measure a quality dimension (QD), it is not enough to review the quality of data or linked data solely. In fact, KG quality needs an overall picture of quality assessment within the years of their popularization. Defining what quality is, within the context of KGs, will depend greatly on whether QDs have been identified for the data consumers [\[13\]](#page-8-0), the data source [\[2,](#page-7-1)[10\]](#page-8-1), and the use case [\[3,](#page-7-2)[4,](#page-7-3)[14\]](#page-8-2).

| Ref.       | Summary                      | Dimensions                                                       |
|------------|------------------------------|------------------------------------------------------------------|
| Wang and   | 15 QDs grouped in 4          | Accessibility, Accuracy, Appropriate amount, Believability,      |
| Strong,    | categories: Accessibility    | Completeness, Concise representation, Consistent representa      |
| 1996 [13]  | (2), Contextual (5), In      | tion, Ease of understanding, Interpretability, Objectivity, Rel  |
|            | trinsic (4), Representa      | evancy, Reputation, Security, Timeliness, Value added            |
|            | tional (4)                   |                                                                  |
| Naumann    | 22 QDs grouped in 3 cat      | Accuracy, Amount of data, Availability, Believability, Com       |
| and        | egories: Object criteria     | pleteness, Concise representation, Consistent representation,    |
| Rolker,    | (9), Process criteria (6),   | Customer support, Documentation, Interpretability, Latency,      |
| 2000 [10]  | Subject criteria (7)         | Objectivity, Price, Relevancy, Reliability, Reputation, Re       |
|            |                              | sponse time, Security, Timeliness, Understandability, Value      |
|            |                              | added, Verifiability                                             |
| Bizer,     | 16 QDs grouped in 4          | Accessibility, Accuracy, Appropriate amount, Believability,      |
| 2007 [2]   | categories: Accessibility    | Completeness, Concise representation, Consistency, Consis        |
|            | (2), Contextual (7), In      | tent representation, Interpretability, Objectivity, Offensive    |
|            | trinsic (4), Representa      | ness, Relevancy, Response time, Timeliness, Understandabil       |
|            | tional (3)                   | ity, Verifiability                                               |
| Zaveri     | 18 QDs grouped in 4          | Accuracy, Availability, Completeness, Concise representation,    |
| et<br>al., | categories: Accessibility    | Conciseness, Consistency, Interlinking, Interoperability, Inter  |
| 2016 [14]  | (5), Contextual (4), In      | pretability, Licensing, Performance, Relevancy, Security, Syn    |
|            | trinsic (5), Representa      | tactic validity, Timeliness, Trustworthiness, Understandabil     |
|            | tional (4)                   | ity, Versatility                                                 |
| F¨arber    | 11 QDs in 4 categories:      | Accessibility, Accuracy, Completeness, Consistency, Interlink    |
| et<br>al., | Accessibility<br>(3),<br>Con | ing, Interoperability, Licensing, Relevancy, Timeliness, Trust   |
| 2018 [3]   | textual (3), Intrinsic (3),  | worthiness, Understandability                                    |
|            | Representational (2)         |                                                                  |
| Fensel     | 23 QDs                       | Accessibility, Accuracy, Appropriate amount, Believability,      |
| et<br>al., |                              | Completeness, Concise representation, Consistent representa      |
| 2020 [4]   |                              | tion, Cost effectiveness, Ease of manipulation, Ease of opera    |
|            |                              | tion, Ease of understanding, Flexibility, Free of error, Interop |
|            |                              | erability, Objectivity, Relevancy, Reputation, Security, Time    |
|            |                              | liness, Traceability, Understandability, Value added, Variety    |
| Hogan      | 10 QDs in 4 categories:      | Accuracy, Coverage, Coherency, Succinctness, Interoperabil       |
| et<br>al., | Accuracy (3), Coverage       | ity, Licensing, Relevancy, Timeliness, Trustworthiness, Under    |
| 2021 [5]   | (2), Coherency (2), Suc      | standability                                                     |
|            | cinctness (3)                |                                                                  |

<span id="page-1-1"></span>Table 1. Comparison of quality dimensions.

Table [1](#page-1-1) shows an overview of the quality dimension proposed by authors who have a perspective on data [\[13\]](#page-8-0), information [\[2,](#page-7-1)[10\]](#page-8-1), linked data [\[3,](#page-7-2)[14\]](#page-8-2), and KGs [\[4\]](#page-7-3) quality. The most cited work from this group has been proposed by Wang and Strong [\[13\]](#page-8-0), who empirically collected and organized QDs from data consumer perspectives. They point out the importance of measuring quality to an extent to which data is accessible, contextually dependant on the task at hand, clearly represented, and intrinsically largely correct and complete.

Naumann and Rolker [\[10\]](#page-8-1) group QDs into 3 categories (subject, predicate, object). The subject (or subject-criteria) implies the user perspective to evaluate specific QDs, the predicate (or process-criteria) implies mainly the process of querying (e.g., availability), and the object (or object-criteria) involves the knowledge source itself (e.g., completeness). Compared with Wang and Strong, Naumann and Rolker highlight the importance of availability, price, customer support, documentation, latency, reliability, response time, understandability, and verifiability QDs.

Bizer [\[2\]](#page-7-1) argues that quality is a multidimensional concept that involves 3 main aspects, which are the data, its context, and its trustworthiness . The author proposes consistency and offensiveness as additional QDs compared with [\[10](#page-8-1)[,13\]](#page-8-0). Furthermore, Bizer contemplates offensiveness as a subjective QD that needs to be taken into account in specific contexts (e.g., cultural, religious).

Zaveri et al. [\[14\]](#page-8-2) discuss quality assessment for linked data extensively. They compare 30 papers focused on quality assessment, from where they identified 18 QDs and several assessment tools. Moreover, compared with [\[2,](#page-7-1)[10,](#page-8-1)[13\]](#page-8-0), Zaveri et al., introduce additional QDs such as conciseness, interlinking, interoperability, licensing, performance, syntactic validity, trustworthiness, and versatility.

Farber et al. [\[3\]](#page-7-2) study the state of the art on quality assessment and implement 11 QDs, which are evaluated through 34 Quality Metrics (QMs) in total. Moreover, the authors test their framework against publicly available KGs (i.e., DBpedia, Freebase, OpenCyc, Wikidata, and YAGO), analyse their results, and provide a list of recommendations on when to use DBpedia, Freebase, OpenCyc, Wikidata, or YAGO KG.

Last but not least, Fensel et al. [\[4\]](#page-7-3) provide a list of QDs that aim to assess KGs. Compared with [\[2,](#page-7-1)[3](#page-7-2)[,10,](#page-8-1)[13,](#page-8-0)[14\]](#page-8-2), the authors propose cost-effectiveness, ease of manipulation, ease of operation, flexibility, free of error, traceability, and variety dimensions. Furthermore, Hogan et al. [\[5\]](#page-7-4) provides a list of QDs described in [\[14\]](#page-8-2).

Most of the authors, with exception to [\[13,](#page-8-0)[14\]](#page-8-2), do not describe the methodology used to define QDs, yet they were created in the context on which the authors focus. In this paper, we consider the dimensions proposed by the authors listed in Table [1.](#page-1-1) Note that flexibility is highly related to ease of manipulation dimension [\[4\]](#page-7-3), understandability is also called ease of understanding [\[14\]](#page-8-2), and value-added is also considered as part of completeness [\[3\]](#page-7-2). In order to define QDs that are relevant to KGs, we look up into KG's definition, which is characterized by its variety to cover various domains [\[3](#page-7-2)[,4,](#page-7-3)[11\]](#page-8-3). Furthermore, we consider that some dimensions are getting attention over the last years in the literature,

| Goal                | Question, Metrics, and Type (QN/QL)                                |
|---------------------|--------------------------------------------------------------------|
| Accessibility       | Is the KG (or at least part of it) available (QN), provides an     |
|                     | SPARQL endpoint (QN), retrievable (QN), supports content ne        |
|                     | gotiation (QN), and contain a license (QN)?                        |
| Accuracy            | Is the KG reliable and correct, e.g., syntactically (QN) and se    |
|                     | mantically (QN)?                                                   |
| Appropriate         | Does the KG contain an appropriate amount (QN) of instances        |
| amount              | for a specific task?                                               |
| Believability       | Does the KG provide provenance information (QN), is trustwor       |
|                     | thy (QL), and has not unknown nor empty values (QN)?               |
| Completeness        | At which degree is the KG complete regarding data (QN), pop        |
|                     | ulation (QN), and interlinking (QN)?                               |
| Concise<br>represen | Is the KG concisely represented by avoiding blank nodes (QN)       |
| tation              | and reification (QN)                                               |
| Consistent<br>repre | Is the KG consistently represented, e.g., disjoint inconsistencies |
| sentation           | of classes (QN), inconsistent inverse functional property values   |
|                     | (QN), schema restrictions (QN)?                                    |
| Cost-effectiveness  | Does the KG require extra data at any cost (QL)?                   |
| Ease of manipula    | At which level does the KG provide documentation (QL)?             |
| tion                |                                                                    |
| Ease of operation   | Is it possible to update (QN), download (QN), and integrate        |
|                     | (QN) the KG?                                                       |
| Ease<br>of<br>under | Is the KG represented using self-descriptive URIs (QN) and in      |
| standing            | various languages (QN)?                                            |
| Free of error       | Does the KG provide correct property values (QN)?                  |
| Interoperability    | Is the KG interoperable, e.g., openly available (QN) and uses      |
|                     | standard vocabularies (QL)?                                        |
| Objectivity         | Is the KG objective, e.g., unbiased (QL) and declares provenance   |
|                     | information (QN)?                                                  |
| Relevancy           | Is the KG relevant for the task at hand, e.g., at which level the  |
|                     | KG provides knowledge for an specific domain or use case (QL)?     |
| Reputation          | Is the KG well rated? E.g is the KG well positioned in explicit    |
|                     | ratings (QL).                                                      |
| Security            | Does the KG provide security mechanisms like digital signature     |
|                     | (QN) and KG authentication (QL)?                                   |
| Timeliness          | At which degree is the KG up to date (QN) and fresh (QN)?          |
| Traceability        | Does the KG provide mean to verify its provenance (QL) and         |
|                     | authenticity (QL)?                                                 |
| Variety             | At which degree the KG integrates various domain sources           |
|                     | (QL)?                                                              |

<span id="page-3-0"></span>Table 2. Proposed quality dimensions and metrics.

QN: Quantitatively measured metrics.

QL: Qualitatively measured metrics.

such as cost [\[4](#page-7-3)[,9,](#page-8-4)[6,](#page-8-5)[13\]](#page-8-0) and traceability [\[4,](#page-7-3)[7,](#page-8-6)[8\]](#page-8-7) dimensions. We summarize our findings into 20 QDs that are relevant in the KGs context, see Table [2.](#page-3-0)

## <span id="page-4-0"></span>3 Assessing Knowledge Graph Quality

In order to operationalize the measurement of the above twenty quality dimensions, we employ the Goal Question Metric (GQM) approach. The GQM approach implies defining (i) a goal, (ii) a set of questions to achieve the goal, and (iii) a set of metrics to answer the questions. Although the GQM approach is used to measure software quality, it has been used in the context of data quality [\[12\]](#page-8-8) and Linked Open Data [\[1\]](#page-7-5). Furthermore, we classify each metric as being quantitatively (QN) or qualitatively (QL) assessed. QN implies that a value score can be calculated for that metric (e.g., manually, semi-automatically, or automatically) and QL requires user judgement to assess the metric (e.g., user perception w.r.t. a metric).

Table [2](#page-3-0) displays the 20 QDs along with questions, metrics, and metric's classification as we understand them. Of course, these definitions might not satisfy every use case or domain. Therefore, they can be adapted and improved.

### <span id="page-4-1"></span>4 Knowledge Graph Quality Assessment Framework

In order to assess a KG, we propose a user-driven assessment framework that enables users to select quality dimensions and metrics according to their degree of importance (e.g., domain, a task at hand, or use case). Our approach consists of 4 steps: Identification, setting, assessment, and exploitation (see Fig. [1\)](#page-5-0).

### 1 Identification

In this step, we propose to identify 3 main points: a user, a use case, and a KG.

- i. Users (namely domain experts) will guide the process of defining the use case, KGs to evaluate, and the weights for QDs and QMs.
- ii. Use Cases (UCs), domain, or tasks at hand need to be understood so that the weights are assigned appropriately. In KGs context, it is important to identify which QDs and QMs are relevant for a domain (see Table [2\)](#page-3-0).
- iii. KGs must be identified by the users as relevant for the UC, e.g., for Points of Interest (POI) domain, KGs such as DBpedia, Google's Knowledge Graph, and Wikidata may be suggested.

### 2 Setting

The goal of developing an assessment framework is to obtain a quality status of a KG for a specific UC. For that, the user needs to set up a KG into the framework, then select, based on weights of importance, a set of QDs and QMs to evaluate in the KG. This process involves:

![](_page_5_Figure_1.jpeg)

<span id="page-5-0"></span>Fig. 1. Hierarchical decomposition of our KG Quality Assessment Framework.

- i. KGs Setting. It is not a straight forward task, for instance. KGs use different schema for describing a same property, e.g., label[1](#page-5-1) , name[2](#page-5-2) , or Q82799[3](#page-5-3) . Moreover, there are KGs that do not provide a SPARQL endpoint (e.g. Google's Knowledge Graph), so SPARQL queries must be adapted to a different query format (e.g. API).
- ii. QDs Weighting. Beta-weights (βi) are defined for selecting QDs, such as β<sup>i</sup> defines a weight of importance for each d<sup>i</sup> QD and β<sup>i</sup> ∈ [0, 1] where 0 is the minimum degree of importance and a value 1 is the maximum degree. Furthermore, it must hold:

$$
\sum_{j=1}^{20} \beta_j = 1
$$

iii. QMs Weighting. Alpha-weights (αi,j ) defines a weight of importance for each QM, such as αi,j<sup>i</sup> defines a weight of importance for a mi,j QM and αi,j ∈ [0, 1] where 0 is the minimum degree of importance and a value 1 is the maximum degree. Moreover:

$$
\sum_{j=1}^{j_i} \alpha_{i,j} = 1
$$
 for all  $i = 1, ..., 20$

<span id="page-5-1"></span><sup>1</sup> label is a RDFs property used to describe a name for a subject. [https://www.w3.](https://www.w3.org/2000/01/rdf-schema#label) [org/2000/01/rdf-schema#label](https://www.w3.org/2000/01/rdf-schema#label)

<span id="page-5-2"></span><sup>2</sup> name is a property used by Schema.org. <https://schema.org/name>

<span id="page-5-3"></span><sup>3</sup> Q82799 is a property used to describe the name of an instance in the Wikidata KG. <https://www.wikidata.org/wiki/Q82799>

### 3 Assessment

In this step, the framework performs 3 main tasks: Assessing the QM, calculating the aggregated score for QDs, and the total aggregated score for a KG.

- i. QMs Assessment (QMA) involves the setting and performing of QMs, so they can be performed either manually, semi-automatically, or automatically.
- ii. QDs Assessment (QDA) is represented by di(g), which calculates the QD aggregated score from the values of each of its QMA for a KG g.

$$
d_i(g) = \sum_{j=1}^{k_i} m_{i,j} \cdot \alpha_{i,j}
$$

Furthermore, k<sup>i</sup> is the number of metrics for the i th QD, mi,j is the score of the j th QM of the i th QD, the alpha-weights (αi,j ) define the impact of the j th QM score on the i th QD score, and di(g), mi,j , αi,j ∈ [0, 1].

iii. KG Assessment (KGA) is represented by T(g), which calculates the total aggregated score from the values of each QDA for a KG g.

$$
T(g) = \sum_{i=1}^{n} d_i(g) . \beta_i
$$

Furthermore, n is the number of QDs, di(g) is the score of the i th QD of g, β<sup>i</sup> represents the weight of the i th QD, and T(g), di(g), β<sup>i</sup> ∈ [0, 1].

As described above, the alpha- and beta- weights select, as well as define, the impact of the QDs and QMs on the overall score of the assessed KG.

### 4 Exploitation

As described above, the alpha- and beta- weights affect the overall result of an assessed KG. Therefore, the results can be compared, tuned, and visualized.

- i. KGA result. The alpha- and beta- weights affect the KGA result. In this step, users can tun the alpha- and beta- weights in order to get desirable results, which might update on the fly.
- ii. UC Result (UCR). The main goal of developing an assessment framework is to obtain suitable KGs for specific use cases. UCR compares the values resulting from the KGAs per UC. For instance, it ranks the results.
- iii. User Interface (UI). It must provide various means by which the calculated results can be accessed, visualized, and easily interpreted. For instance, giving recommendations on when to use such KGs.

Note that, our framework defines QDs and QMs as we understood them. However, every situation or application might require some adaptation. Also notice that some QM are similar to each other or one QM might be combined in more than one QD, therefore we advise not to select all QD and QM at the same time, e.g., play with the alpha- and beta- weights until you get a desirable result.

# <span id="page-7-0"></span>5 Conclusion and Future Work

In this paper, we conducted a comprehensive study on quality assessment, which included data, information, linked data, and KGs quality context. We propose 20 QDs that are relevant in the KGs context and several metrics that can be quantitatively or quantitatively measured. Furthermore, we remark the importance of taking into account cost-effectiveness, traceability, and variety QDs. Then, we propose a user-driven assessment framework for evaluating the quality of KGs. Our framework comprises 4 steps: identification, setting, assessment, and exploitation. Furthermore, The framework can be used for lighting KGs architects on the basic quality requirements of KGs, and in the development of future KG assessment frameworks.

The next step of our work will be focused on developing the KG assessment framework. Moreover, we will evaluate the performance of the framework and conduct surveys from domain experts and KG researchers to evaluate and improve the proposed QDs, as well as, the framework. Furthermore, the development of a KG assessment framework might be, to some extent, semi-automated, i.e., implementing the metrics that can be quantitatively measured (which also might reduce assessment costs), but it will still be a combination of humanmachine efforts as necessary.

On one hand, since there is no unique solution to assess the status of KGs, further research is needed to evaluate the framework in specific use cases. On the other hand, a unified quality assessment approach would improve the applying of quality assessment in KGs and increase the adoption of KGs to worldwide application scenarios.

Acknowledgments. The initial work for this paper was funded by the Mind-Lab project: <https://mindlab.ai/>

## References

- <span id="page-7-5"></span>1. Behkamal, B., Kahani, M., Bagheri, E., Jeremic, Z.: A metrics-driven approach for quality assessment of linked open data. J. Theor. Appl. Electron. Commer. Res. 9(2), 64–79 (2014), [http://www.jtaer.com/may2014/Behkamal\\_Kahani\\_Bagheri\\_](http://www.jtaer.com/may2014/Behkamal_Kahani_Bagheri_Jeremic_p5.pdf) [Jeremic\\_p5.pdf](http://www.jtaer.com/may2014/Behkamal_Kahani_Bagheri_Jeremic_p5.pdf)
- <span id="page-7-1"></span>2. Bizer, C.: Quality-driven information filtering in the context of web-based information systems. Ph.D. thesis, Free University of Berlin (2007)
- <span id="page-7-2"></span>3. F¨arber, M., Bartscherer, F., Menne, C., Rettinger, A.: Linked data quality of dbpedia, freebase, opencyc, wikidata, and YAGO. Semantic Web 9(1), 77–129 (2018), <https://doi.org/10.3233/SW-170275>
- <span id="page-7-3"></span>4. Fensel, D., Simsek, U., Angele, K., Huaman, E., K¨arle, E., Panasiuk, O., Toma, I., Umbrich, J., Wahler, A.: Knowledge Graphs - Methodology, Tools and Selected Use Cases. Springer (2020)
- <span id="page-7-4"></span>5. Hogan, A., Blomqvist, E., Cochez, M., d'Amato, C., de Melo, G., Guti´errez, C., Kirrane, S., Gayo, J.E.L., Navigli, R., Neumaier, S., Ngomo, A.N., Polleres, A., Rashid, S.M., Rula, A., Schmelzeisen, L., Sequeda, J., Staab, S., Zimmermann, A.: Knowledge Graphs. Synthesis Lectures on Data, Semantics, and

Knowledge, Morgan & Claypool Publishers (2021), [https://doi.org/10.2200/](https://doi.org/10.2200/S01125ED1V01Y202109DSK022) [S01125ED1V01Y202109DSK022](https://doi.org/10.2200/S01125ED1V01Y202109DSK022)

- <span id="page-8-5"></span>6. Huaman, E., Fensel, D.: Knowledge graph curation: A practical framework. In: IJCKG'21: The 10th International Joint Conference on Knowledge Graphs, Virtual Event, Thailand, December 6 - 8, 2021. pp. 166–171. ACM (2021), [https://doi.](https://doi.org/10.1145/3502223.3502247) [org/10.1145/3502223.3502247](https://doi.org/10.1145/3502223.3502247)
- <span id="page-8-6"></span>7. Huaman, E., K¨arle, E., Fensel, D.: Knowledge graph validation. CoRR abs/2005.01389 (2020), <https://arxiv.org/abs/2005.01389>
- <span id="page-8-7"></span>8. Huaman, E., Tauqeer, A., Fensel, A.: Towards knowledge graphs validation through weighted knowledge sources. In: Knowledge Graphs and Semantic Web - Third Iberoamerican Conference and Second Indo-American Conference, KGSWC 2021, Kingsville, Texas, USA, November 22-24, 2021, Proceedings. Communications in Computer and Information Science, vol. 1459, pp. 47–60. Springer (2021), [https:](https://doi.org/10.1007/978-3-030-91305-2_4) [//doi.org/10.1007/978-3-030-91305-2\\_4](https://doi.org/10.1007/978-3-030-91305-2_4)
- <span id="page-8-4"></span>9. Lenat, D.B.: CYC: A large-scale investment in knowledge infrastructure. Commun. ACM 38(11), 32–38 (1995), <https://doi.org/10.1145/219717.219745>
- <span id="page-8-1"></span>10. Naumann, F., Rolker, C.: Assessment methods for information quality criteria. In: Fifth Conference on Information Quality (IQ 2000). pp. 148–162. MIT (2000)
- <span id="page-8-3"></span>11. Paulheim, H.: Knowledge graph refinement: A survey of approaches and evaluation methods. Semantic Web 8(3), 489–508 (2017), [https://doi.org/10.3233/](https://doi.org/10.3233/SW-160218) [SW-160218](https://doi.org/10.3233/SW-160218)
- <span id="page-8-8"></span>12. Redman, T.C.: Data quality for the information age. Artech House (1996)
- <span id="page-8-0"></span>13. Wang, R.Y., Strong, D.M.: Beyond accuracy: What data quality means to data consumers. J. Manag. Inf. Syst. 12(4), 5–33 (1996), [http://www.jmis-web.org/](http://www.jmis-web.org/articles/1002) [articles/1002](http://www.jmis-web.org/articles/1002)
- <span id="page-8-2"></span>14. Zaveri, A., Rula, A., Maurino, A., Pietrobon, R., Lehmann, J., Auer, S.: Quality assessment for linked data: A survey. Semantic Web 7(1), 63–93 (2016), [https:](https://doi.org/10.3233/SW-150175) [//doi.org/10.3233/SW-150175](https://doi.org/10.3233/SW-150175)
