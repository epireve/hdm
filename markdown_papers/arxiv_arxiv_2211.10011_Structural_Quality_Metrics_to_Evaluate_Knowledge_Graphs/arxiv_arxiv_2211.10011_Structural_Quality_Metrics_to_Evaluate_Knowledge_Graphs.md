---
cite_key: "file2020c"
title: "<span id=\"page-0-0\"></span>Structural Quality Metrics to Evaluate Knowledge Graph Quality"
authors: "tion associated with Wikipedia and allows users to participate directly in creating and editing data. Although ontology information is not provided as a separate file, the hierarchical structure between entities can be known through *subclass of* property for each entity."
year: 2020
doi: "10.1007/978-3-540-76298-0_52)"
date_processed: "2025-07-02"
phase2_processed: true
original_folder: "arxiv_arxiv_2211.10011_Structural_Quality_Metrics_to_Evaluate_Knowledge_Graphs"
images_total: 11
images_kept: 11
images_removed: 0
---

# <span id="page-0-0"></span>Structural Quality Metrics to Evaluate Knowledge Graph Quality

Sumin Seo, Heeseon Cheon, Hyunho Kim, Dongseok Hyun

sumin.seo@navercorp.com, heeseon.cheon@navercorp.com, kim.hh@navercorp.com, dustin.hyun@navercorp.com

## Abstract

This work presents six structural quality metrics that can measure the quality of knowledge graphs and analyzes four cross-domain knowledge graphs on the web (Wikidata, DBpedia, YAGO, Freebase) and Google Knowledge Graph, as well as 'Raftel', Naver's integrated knowledge graph. The 'Good Knowledge Graph' should define detailed classes and properties in its ontology so that it can abundantly express knowledge in the real world. Also, instances and RDF triples should use the classes and properties actively. Therefore, we tried to examine the internal quality of knowledge graphs numerically by focusing on the structure of the ontology, which is the schema of knowledge graphs, and the degree of use thereof. As a result of the analysis, it was possible to find the characteristics of a knowledge graph that could not be known only by scale-related indicators such as the number of classes and properties.

## 1 Introduction

A knowledge graph is a data system that consists of RDF triples which are in the form of a *'subjectpredicate-object'*between entities in the real world and their relationships. For example, the fact that 'the capital of Korea is Seoul' can be expressed as*'Korea - capital - Seoul'*.

Ontology is a schema that defines the structure of a knowledge graph. An ontology defines the hierarchical relationship between classes and the properties that classes can have. Class is an abstract concept that encompasses entities with similar characteristics. For example, *Seoul*is the instance(=entity) of the*'City'*class, and*Korea*is the instance of the*'Country'*class. The hierarchical relationship between classes is expressed with*'subclass of '*predicate between superclass, which means a higher concept, and subclass, which means a lower concept. In addition,*'is-a'*relationship must be established

between the two. For example, the*'Book'*class and the*'Movie'*class are subclasses of the*'Creative Work'*class and are defined in the ontology with RDF triples,*'Book - subclass of - Creative Work'*and*'Movie - subclass of - Creative Work'*. Property is an attribute that each class can have, and in the case of the *'Country'*class, it can have*'capital'*, *'population'*, and *'president'*as properties. An ontology defines the properties that each class can have.

Knowledge graphs has an important role in search systems such as Google's knowledge panel [\(Zou](#page-9-0) [\(2020\)](#page-9-0)), and recently attention is being drawn from NLP tasks such as Question Answering [\(Huang et al.](#page-9-1) [\(2019\)](#page-9-1)) or recommendation systems [\(Guo et al.](#page-8-0) [\(2022\)](#page-8-0)), and explainable AI [\(Tiddi and Schlobach](#page-9-2) [\(2022\)](#page-9-2)). In this regard, Wikidata (Vrandeciˇ [c and Krötzsch](#page-9-3) ´ [\(2014\)](#page-9-3), Freebase[\(Bollacker et al.](#page-8-1) [\(2008\)](#page-8-1), DBpedia [\(Auer et al.](#page-8-2) [\(2007\)](#page-8-2)), and YAGO[\(Suchanek et al.](#page-9-4) [\(2007\)](#page-9-4)) are examined for various tasks in many studies.

This study outlines what makes a "good knowledge graph" and offers a metric to quantify it. In contrast to the current knowledge graph evaluation studies, which mainly focused on the size and distribution of the data, this study devised a measure to compare the quality between knowledge graphs from the viewpoint that structure (=ontology) is a key factor in determining the quality of knowledge graphs. Based on this indicator, we compared knowledge graphs on the web (Wikidata, Freebase, DBpedia, YAGO, Google Knowledge Graph) and Naver's knowledge graph Raftel.

## 2 Related Works

Ontology and knowledge graph evaluation methods can be categorized as follows.[\(Brank et al.](#page-8-3) [\(2005\)](#page-8-3), [Raad and Cruz](#page-9-5) [\(2015\)](#page-9-5), [Färber and Rettinger](#page-8-4) [\(2018\)](#page-8-4))

•*gold standard evaluation*: a method of compar-

ing knowledge graphs to high-quality knowledge graphs with the same topic.

- *data driven evaluation*: a method that selects important words by extracting keywords from documents dealing with the same domain of knowledge graphs and measures how much information knowledge graphs contain.
- *application/task based evaluation*: a method that evaluates the downstream task performance of the knowledge graph.
- *user based evaluation*: a method that evaluates quality from the perspective of knowledge graph users.
- *structure based evaluation*: a method that evaluates knowledge graphs through metrics that can reflect the structure or statistical properties of the ontology and knowledge graphs. [\(Lourdusamy and John](#page-9-6) [\(2018\)](#page-9-6), [Tartir et al.](#page-9-7) [\(2005\)](#page-9-7))
- *data quality evaluation*: a method that defines data quality with various point of views including *accuracy*and*consistency*of data and suggests numerical indicators to measure data quality.[\(Zaveri et al.](#page-9-8) [\(2018\)](#page-9-8), [Färber and Ret](#page-8-4)[tinger](#page-8-4) [\(2018\)](#page-8-4))

Comparative studies on cross-domain knowledge graphs on the web are mainly focuses on structure-based evaluation and data quality evaluation. [\(Ringler and Paulheim](#page-9-9) [\(2017\)](#page-9-9), [Heist et al.](#page-9-10) [\(2020\)](#page-9-10)) First of all, the structure-based evaluation uses*schema metric*, *instance/knowledge base metric*, *class metric*, *graph metric*and*complexity metric*to compare knowledge graphs.*Schema metric*calculates the number of classes, the number of properties, and the number of properties per class, focusing on an ontology.*Instance/knowledge base metric*calculates, for example, the average number of instances per class considering instances with an ontology. In the case of*class metric*, the number of instances of the *'Person'*class and the degree of connection with other classes is calculated to represent the characteristics of each class.*Graph metric*is the application of basic statistics of graph theory such as cohesion and cardinality to knowledge graphs.

[Piscopo and Simperl](#page-9-11) [\(2019\)](#page-9-11) analyzed the dimensions on which researches on the data quality of knowledge graphs concentrated according to the

framework presented by [Wang and Strong](#page-9-12) [\(1996\)](#page-9-12). There are many works that evaluate knowledge graphs on data quality perspective: An*accuracy*perspective which means how accurately the knowledge graph reflects real-world information [\(Nielsen](#page-9-13) [et al.](#page-9-13) [\(2017\)](#page-9-13), [Prasojo et al.](#page-9-14) [\(2016\)](#page-9-14) ), a*consistency*perspective that focuses on how consistent the data in the knowledge graph is[\(Spitz et al.](#page-9-15) [\(2016\)](#page-9-15), [Pis](#page-9-16)[copo and Simperl](#page-9-16) [\(2018\)](#page-9-16)), an*ease of understanding*perspective including how many languages a knowledge graph provides[\(Kaffee et al.](#page-9-17) [\(2017\)](#page-9-17)), a*interlinking*perspective which means how much a knowledge gaph can be connected to other knowledge graphs[\(Suchanek et al.](#page-9-4) [\(2007\)](#page-9-4), [Ringler and](#page-9-9) [Paulheim](#page-9-9) [\(2017\)](#page-9-9)).

As a complement to the shortcomings of current structure-based metrics and data-quality-based assessment techniques, we introduce the*structural quality metrics*as a measure of knowledge graph quality. Most of the researches comparing knowledge graphs on the web with structural metrics mainly focus on the size of knowledge graphs (number of RDF triple, class, and instance). In addition, numerical indicators related to structure simply describe the distribution of data such as the number of instances per class. It is easy to grasp the size and approximate structure of the knowledge graph with this approach, but difficult to evaluate either side as better in terms of quality. Graph metrics such as cohesion and cardinality can be used to evaluate the quality of knowledge graphs, such as how concisely organized knowledge graphs are and how rich relations a knowledge graph has. However, these metrics are not specialized for the quality of knowledge graphs. Studies based on data quality dimension analyzed knowledge graphs on the web in various aspects, but there are no quality indicators based on the knowledge graph structure, ontology. Therefore, we proposes*structural quality metric*that can numerically represents the internal quality of knowledge graphs, focusing on the ontological structure and its degree of utilization.

## 3 Data Introduction and Basic Statistics

### 1 Data Introduction and Data Preparation

Wikidata, DBpedia, Freebase, YAGO, and Google Knowledge Graph, which are knowledge graphs analyzed in the work, have the following characteristics.[\(Cheon et al.](#page-8-5) [\(2021\)](#page-8-5))

Wikidata Wikidata was launched in 2012 by Wikimedia Deutschland, which provides informa-

<span id="page-2-0"></span>

|           | subject                                                                                                                                          | predicate                                                                                     | object                                     |  |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|--------------------------------------------|--|
| class     | <http: rdf.freebase.com<="" th=""><th><http: th="" www.w3.org<=""><th colspan="2"><http: th="" www.w3.org<=""></http:></th></http:></th></http:> | <http: th="" www.w3.org<=""><th colspan="2"><http: th="" www.w3.org<=""></http:></th></http:> | <http: th="" www.w3.org<=""></http:>       |  |
|           | /ns/base.                                                                                                                                        | /1999/02/22 -rdf                                                                              | /2000/01/ rdf                              |  |
|           | birdinfo.parasitism>                                                                                                                             | syntax-n#type>                                                                                | schema#Class>                              |  |
| predicate | <http: rdf.freebase.com<="" th=""><th><http: th="" www.w3.org<=""><th><http: rdf.freebase.com<="" th=""></http:></th></http:></th></http:>       | <http: th="" www.w3.org<=""><th><http: rdf.freebase.com<="" th=""></http:></th></http:>       | <http: rdf.freebase.com<="" th=""></http:> |  |
|           | /ns/film.                                                                                                                                        | /2000/01/ rdf                                                                                 | /ns/film.film>                             |  |
|           | film.directed_by>                                                                                                                                | schema#domain>                                                                                |                                            |  |

Table 1: Example of Freebase Ontology data extraction

tion associated with Wikipedia and allows users to participate directly in creating and editing data. Although ontology information is not provided as a separate file, the hierarchical structure between entities can be known through*subclass of*property for each entity.

- DBpedia DBpedia is a knowledge graph launched in 2007 by Free University of Berlin and the University of Leipzig. It is created by automatically extracting structured information contained in Wikipedia, and it builds and manages its own ontology structure.
- Freebase Freebase was launched by MetaWeb Technologies, Inc. in 2007 and merged into Wikidata by the Wikimedia Foundation and Google in 2015.[\(Tanon et al.](#page-9-18) [\(2016\)](#page-9-18)) Ontology is constructed in a human readable manner with the structure of*'domain/class/predicate'*.
- YAGO Developed by Max Planck in 2007, data is generated by extracting information from Wikipedia infobox and WordNet in various languages. The ontology structure is built on WordNet.
- Google Knowledge Graph Google KG was developed by Google in 2012 to understand the meaning of search terms in the search engine. Through the API, information such as name, description, image, and type which informs the class can be obtained for a specific keyword. There is no self-defined ontology, and the type is configured based on *schema.org*. In 2014, Google introduced Knowledge Vault [\(Dong et al.,](#page-8-6) [2014\)](#page-8-6), which integrates Wikipedia, YAGO, Microsoft's Satori, and Google Knowledge Base. Since the data is not published to the public, we used Google Knowledge Graph data accessi-

## ble by API (Google Knowledge Graph Search API).

Raftel, introduced in this work, is a knowledge graph that integrates Wikidata and Naver databases on various domains. Based on the class structure and properties of Wikidata, an active and fastgenerating knowledge graph based on the community, the basic ontology was designed, classes were added and removed, hierarchical relationships were adjusted, and attributes were added and removed to alleviate the complexity of the ontology and increase consistency.

In addition, since Raftel is a knowledge graph generated based on Korean data, other knowledge graphs were filtered based on the entity with the Korean label. Since Google Knowledge graph can query API based on specific keywords, data with Korean labels that exist in Wikidata were imported.

Ontology data were refined differently depending on whether or not ontology data is provided with a separate file for each knowledge graph. For DBpedia and YAGO, we used the ontology file provided by themselves. In the case of YAGO, only the classes defined in the ontology file were included for the calculation because the number of classes defined in the ontology file and the number of classes corresponding to B of the RDF triple *'A - instance of - B'*was different. The ontology of Google Knowledge Graph is based on schema.org, so we used*schema.org*'s ontology data for Google KG.[1](#page-0-0) For Wikidata and Freebase, where ontology data is not provided with a separate file, we established an ontology by refining the knowledge graph RDF triple data. Wikidata's ontology was extracted using the *'subclass of '*property. In the case of properties for each class, the properties used in the class were collected by mapping the class to the instance of the RDF triple. Freebase's class was targeted at RDF triple's subject with

<sup>1</sup> https://developers.google.com/knowledge-graph

<span id="page-3-0"></span>

|                       | Raftel      | Wikidata        | DBpedia       | YAGO            | Google KG  | Freebase      |
|-----------------------|-------------|-----------------|---------------|-----------------|------------|---------------|
| number of classes     | 273         | 59,662          | 804           | 266             | 910        | 53,091        |
| number of properties  | 607         | 7,476           | 21,607        | 141             | 1,447      | 23,446        |
| number of RDF triples | 253,566,996 | 27,258,977      | 11,137,852    | 348,094,663     |            | 48,292,483    |
|                       |             | (4,655,416,683) | (119,684,431) | (2,489,856,093) | 48,348,838 | (267,990,918) |
| number of instances   | 17,653,785  | 1,323,452       | 287,752       | 19,707,176      |            | 33,535,913    |
|                       |             | (95,312,952)    | (7,362,499)   | (73,260,077)    | 1,390,438  | (115,880,746) |

Table 2: basic statistics(target language:korean, figures in parentheses are statistics for all language data)

a property of*'<http://www.w3.org/1999/02/22 rdf-syntax-ns#type>'*and an object of*'<http://www.w3.org/2000/01/rdf-schema#Class>*. In addition, Freebase does not specify a hierarchy between classes, so there is no root class [\(Chah](#page-8-7) [\(2018\)](#page-8-7)). To calculate metrics, we created a root class and connected all classes as subclasses of the root class. The property was targeted at RDF triple's subject whose object ends with 'Property>' among objects with a property of *'<http://www.w3.org/1999/02/22 rdf-syntax-ns#type>'*, and only those with a property of *'<http://www.w3.org/2000/01/rdfschema#domain>'*were explicitly provided. (Table [1\)](#page-2-0)

### 2 Basic Statistics

Table [2](#page-3-0) shows the basic statistics for knowledge graphs. The number of classes and properties was calculated for ontology, and the number of RDF triple and instances were calculated for knowledge graph RDF triple data. It includes an RDF triple with instances of classes or properties that were not defined in the ontology. In the case of ontology, all classes and properties were considered regardless of the Korean label. Other analysis include RDF triples of the instance with a Korean label among all RDF triples of the knowledge graph. Numbers in parentheses are analytical values for the entire language. For Google KG, since we extracted data that exist in Raftel, analysis of the entire language was not conducted separately.

In terms of classes and properties that construct the ontology, Wikidata and Freebase have more than 50,000 classes, which is about 200 times more than Raftel and YAGO, which have fewer classes. In the case of properties, DBpedia and Freebase have more than 20,000 properties, 100 times more than YAGO, which has the least properties, and 30 times more than Raftel, which has the second least properties.

On the other hand, Raftel and YAGO have relatively large amount of RDF triples and instances. Compared to DBpedia, which has the lowest RDF triple count, the number of RDF triples of YAGO is more than 30 times higher, and in the case of Raftel, it is more than 20 times higher. In the case of the number of instances, Freebase is the largest, but for Freebase, the number of RDF triples is small because most RDF triples are composed of*'instance of '*relationship. It can be seen from the fact that the number of an RDF triple is about 1.4 times the number of instances. Next, the number of YAGO and Raftel instances is 190 million and 170 million, respectively, more than 60 times that of DBpedia, which has the lowest number of instances. For YAGO, there are about 18.46 million instances belonging to the*'scholarArticle'*class, accounting for 97% of the total, and RDF triples with the*'scholarArticle'*instance as the subject account for more than 90% (312, 203, 867).

## 4 Structural Quality Metrics

### <span id="page-3-1"></span>4.1 What is a good Knowledge Graph?

A good knowledge graph should have a finegrained ontology structure that can precisely express information in the real world, and instances and triples should make full use of the ontology's classes and properties. By categorizing this perspective into the four categories listed below, a structural quality metrics that can quantify each content was developed.

First, class hierarchy must be abundantly subdivided in the ontology. Taking the*'Person' class*as an example, the more the*Person*is divided into horizontals like*'Artist, Athlete, Politician, Doctor'*, and the more split into verticals like *'Person*→*Artist*→*Musician'*, the better the ontology. Compared to the case where only *'Person' class*exists for the class related to people, if it is divided into

more classes according to occupation, ontology would be more powerful in various tasks by narrowing the scope of the classification of entities. For example, in the entity disambiguation task, the range to which the entity of the person with the same name belongs is specified, making it easy to distinguish. If the*'Musician'*and*'Author'*classes are added as subclass to*'Artist'*, which is a subclass of *'Person'*, the ontology will provide more specific information to application tasks.

Second, when it is subdivided from superclass to subclass in ontology, the more properties that are not in superclass in subclass, the better. In the case of vertically splitting the class, the number of properties that the subclass has should increase. For example, when *Athlete*class is a subclass of*Person*class, the*Person*class has universal properties such as*"parent"*, *"birth date"*, and *"birth place"*. The more properties (e.g. *"back number"*, *"team"*, *"world ranking"*, *"league"*, etc.) the *Athele*has, the more specific quality of information that can be obtained as a class is added.

Third, classes and properties defined in the ontology must be used sufficiently in the knowledge graph. Even if classes and properties are defined in detail, ontologies are only useful if they are applied to the knowledge graph. The*Person*class can be divided into classes like "Chef of Chinese Restaurant in Seoul" or "4th grade music teacher of the elementary school". Nevertheless, if the number of instances is too small relative to the whole number of instances in the knowledge graph, it is difficult to say that adding the class is beneficial. Likewise, specific properties such as "number of debut songs sung at concerts" and "administrative district where the most fans live" can be defined for the*Musician*class, but if data does not exist and is not used as actual RDF triples, it is better not to add it.

Fourth, though the quality increases as the class is subdivided, it is negative if the complexity increases in this process. Multiple inheritance is an example of a factor that describes ontology complexity. Multiple inheritance means that one class has several superclasses. For example, the*Hospital*class is a subclass of*'Facility'*, a space that provides a specific function, and a subclass of *'Organization'*, a group of employees including doctors and nurses. Avoiding multiple inheritance is preferable, unless it is necessary, like in the case of the *Hospital*where both location information, which is a facility characteristic, and member information, which is an organization characteristic, are crucial. This is because when subclass and superclass are connected in a many-to-many relationship, the complexity of understanding and utilization of ontology increases.

#### 2 Structural Quality Metrics

We present a structural quality metric that can measure the quality of good knowledge graphs presented by [4.1.](#page-3-1) [4.2.1,](#page-4-0) [4.2.2](#page-4-1) have been examined in previous studies, and [4.2.3,](#page-4-2) [4.2.4,](#page-5-0) [4.2.5,](#page-6-0) [4.2.6,](#page-6-1) are newly introduced in this work.

#### <span id="page-4-0"></span>4.2.1 Instantiated Class Ratio
*Instantiated Class Ratio*refers to the ratio of classes with instances among classes defined in the ontology. It is an indicator of how well the class of ontology is actually being used. In obtaining*Instantiated Class Ratio*for ontology ( [1\)](#page-4-3), N(C) means the total number of classes in the Ontology, and N(IC) means the number of classes in which instances exist.

<span id="page-4-3"></span>
$$
ICR(Ontology) = \frac{N(IC)}{N(C)} \tag{1}
$$

#### <span id="page-4-1"></span>4.2.2 Instantiated Property Ratio
*Instantiated Property Ratio*refers to the ratio of properties actually used in RDF triple among the properties defined in the ontology. It is an indicator of how well the properties of the ontology are actually being used. In obtaining*Instantiated Property Ratio*for ontology ( [2\)](#page-4-4), N(P) denotes the total number of properties of the Ontology, and N(IP) denotes the number of properties used in RDF triples.

<span id="page-4-4"></span>
$$
IPR(Ontology) = \frac{N(IP)}{N(P)}\tag{2}
$$

#### <span id="page-4-2"></span>4.2.3 Class Instantiation
*Class Instantiation*is a metric that assesses how much in detail classes are defined in the ontology and how much they are actually instantiated. For each class included in the knowledge graph, the class instantiation is calculated and summed to be used as an indicator representing the knowledge graph. In a formula ( [3\)](#page-5-1) to obtain*Class Instantiation*for a particular*Class*, n<sup>c</sup> means the number of subclasses that the *Class*has, ir(c) means instantiated ratio, which is*'number of instances of the Class / number of all instances in knolwedge*<span id="page-5-2"></span>![](_page_5_Figure_0.jpeg)

Figure 1: Class Instantiation Example
*graph'*, c<sup>i</sup> is the i-th subclass the *Class*has, d means the distance between the*Class*and c<sup>i</sup> .

<span id="page-5-1"></span>
$$
CI(Class) = \sum_{i=1}^{n_c} \frac{ir(c_i)}{2^{d(c_i)}} \tag{3}
$$

The process of calculating*Class Instantiation*for*'Person'*class in a knowledge graph such as Figure [1](#page-5-2) is as follows. The total number of instances of the knowledge graph is 500, of which the number of instances of*'Person'*and*Person*'s subclass is 200. For all subclasses under the *'Person'*class, the proportion of the class's instance to the total instance is calculated. Let's say this is a "weight". For example, to calculate the weight for*'Artist'*, use the number of direct instances of the *Artist*, not the instances of *'Actor'*, *'Musician'*, or *'Author'*. *'Ariana Grande'*instance is not a direct instance of the*'Artist'*because the singer is an instance of the*Artist*'s subclass, *'Musician'*. Since *'Pablo Picasso'*instance does not belong to the*'Artist'*'s subclasses , it becomes a direct instance of the *'Artist'*. In the figure, the class is represented with rectangle box, and in the box, *(number of instances*→*weights)*is denoted.
*Person*'s *Class Instantiation*accumulates weights from the subclass farthest from*'Person'*. Weights are not added as they are, but divided by 2 DepthF romP ersonClass. The farther away from the *'Person'*class, the more penalty the class's weight

has. As a result,*Class Instantiation*of*'Person'*is calculated as 0.1 + (0.02 + 0.01 + 0.06) × 1 2 <sup>1</sup> + (0.06 + 0.1 + 0.04) × 1 2 2 .
*Class Instantiation*is obtained in the same way as above for all the classes including*'Artist'*, *'Musician'*, and *'Creative Work'*that exist in the ontology.

For*Class Instantiation*, the more classes are divided, the more each class is fully utilized, and the higher the weight, the greater the value of *Class Instantiation*. In addition, the penalty according to depth was applied to prevent the side effects of increasing the score as the class is subdivided into verticals unconditionally.

#### <span id="page-5-0"></span>4.2.4 Subclass Property Acquisition

*Subclass Property Acquisition*is a metric that measures how many properties are defined in the subclass that is not in the superclass in the ontology. For example, if the*'Person'*class is a subclass of the*'Entity'*class, properties that are not defined in the*'Entity'* class such as '*children*', '*academic degree*', and '*spouse*', can be added. Furthermore, if the *'Actor'*class is a subclass of the*'Person'* class, properties like '*character role*', '*cast member of*' can be added. The *Subclass Property Acquisition*is the average value obtained by number of newly added properties that are not in the superclass for all classes of the ontology, except for the root class

(e.g.,*Entity*class).

In the formula for obtaining*Subclass Property Acquisition*for Ontology ( [4\)](#page-6-2), P denotes property set and N(P) is a function for the number of elements in the property set. For all 'superclass-subclass' relationships present in Ontology, N(Psubclass − Psuperclass) is calculated, and the number of properties present in the subclass is obtained and summed. For all classes in Ontology,*Subclass Property Acquisition*is calculated and averaged by N(C), the number of classes.

<span id="page-6-2"></span>
$$
SPA(Ontology) = \frac{\sum (N_i(P_{sublass} - P_{superclass}))}{N(C)}
$$
\n(4)

#### <span id="page-6-0"></span>4.2.5 Subclass Property Instantiation
*Subclass Property Instantiation*quantifies how much the properties are used in the RDF triples when the properties of the subclass that are not in the superclass are defined in the ontology. For example, if an*'Actor'* class adds '*cast member of*' and '*character role*' property that are not in the superclass *'Person'*class, the more unique properties of the actor are used in RDF triples, such as*"Tom Cruise - cast member of - Mission Impossible"*and*"Tom Cruise - character role - Ethan Hunt"*, the better structure knowledge graph has. Knowledge graph's *Subclass Property Instantiation*is average of*Subclass Property Instantiation*of all the classes.

In the formula for obtaining*Subclass Property Instantiation*for a particular*Class*( [5\)](#page-6-3), T is a set of RDF triples, and N(T) is a function of obtaining the number of RDF triples. N(Tclass − Tclass\_superclass) is the number of RDF triples of*Class*excluding RDF tripels which uses predicates defined for superclass.

<span id="page-6-3"></span>
$$
SPI(Class) = \frac{N(T_{Class} - T_{class\_superclass})}{N(T_{Class})}
$$
\n(5)

To compute a*Subclass Property Instantiation*for an*'Actor'*class, first, count the number of all triples with an*'Actor'*class's instance as the subject. In addition to RDF triples like*"Tom Cruise cast memeber of - Mission Impossible"*and*"Tom Cruise - character role - Ethan Hunt"*, count all the RDF triples including*"Tom Cruise - Birth Place - Syracuse"*, *"Tom Cruise - Nationality - United States"*, and *"Tom Cruise - Name - Tom Cruise"*. This becomes denominator of the *Subclass Property Instantiation.*Next, count the number of triples

in which the properties added in the*'Actor'*class are used. Except for*"Tom Cruise - Birth Place - Syracuse"*, *"Tom Cruise - Nationality - United States"*, and *"Tom Cruise - Name - Tom Cruise"*, only RDF triples such as *"Tom Cruise - cast member of - Mission Impossible"*and*"Tom Cruise character role - Ethan Hunt"*are considered. This is the numerator of*Subclass Property Instantiation*. By dividing the number of RDF triples used by the property added in the *'Actor'*by the total number of triples in the*'Actor'*, we can see how the unique property increases in RDF triple as the *'Actor'*was subdivided from*'Person'*. For example, if the *Actor*'s *Subclass Property Instantiation*is 0.05, it means that the RDF triple of*'Actor'*with new properties has increased by 5% compared to the superclass*'Person'*.

#### <span id="page-6-1"></span>4.2.6 Inverse Multiple Inheritance

*Inverse Multiple Inheritance*evaluates the simplicity of the knowledge graph. If multiple inheritance occurs frequently in which a single class has numerous superclasses, might make it challenging to use the knowledge graph because of the complexity of the class relationship. Inverse multiple inheritance was devised to measure how little multiple inheritance appears. The average number of superclasses per class is computed to obtain the average multiple inheritance, and take the reciprocal of it. Therefore, the higher the*Inverse Multiple Inheritance*, the simpler the knowledge graph is. In ( [6\)](#page-6-4), N<sup>c</sup> represents the total number of classes in the ontology, and C<sup>i</sup> represents each class in the ontology, nsup(C) represents the number of direct superclasses in the class.

<span id="page-6-4"></span>
$$
IMI(Ontology) = \frac{1}{\frac{\sum_{i=1}^{N_c} nsup(C_i)}{N_c}}
$$
 (6)

The six structural quality metrics determine whether knowledge graph can express knowledge abundantly through a detailed ontology. Among them, *Class Instantiation*and*Subclass Property Instantiation*have the characteristics of a comprehensive indicator that can reflect classes or attribute's degree of subdivision and actual utilization.

## 3 Structural Quality Metric Evaluation Result

Table [3](#page-7-0) is the analysis of structural quality metric with five knowledge graphs on the web and

<span id="page-7-0"></span>

|                                 | Raftel | Wikidata  | DBpedia  | YAGO      | Google KG | Freebase |
|---------------------------------|--------|-----------|----------|-----------|-----------|----------|
|                                 | 0.941  | 0.004     | 0.470    | 0.820     |           | 0.046    |
| Instantiated Class Ratio        |        | (0.334)   | (0.540)  | (0.966)   | 0.099     | (0.314)  |
| Instantiated Property Ratio     | 1      | 1         | 0.99     | 0.90      |           | 0.002    |
|                                 |        | (1)       | (1)      | (0.96)    | 1         | (0.003)  |
|                                 | 0.941  | 0.716     | 0.900    | 0.886     |           | 0.874    |
| Class Instantiation             |        | (0.743)   | (0.949)  | (0.616)   | 0.660     | (0.749)  |
| Inverse Multiple Inheritance    | 0.975  | 0.962     | 0.971    | 0.942     | 0.952     | 1        |
| Subclass Property Acquisition   | 6.54   | 40.94     | 63.57    | 2.23      | 0.0       | 1        |
|                                 | 0.0857 | 0.0133    | 0.0841   | 0.0003    |           | 0.0      |
| Subclass Property Instantiation |        | (0.00001) | (0.0668) | (0.00001) | 0.0       | (0.0)    |

Table 3: structural quality metric evaluation (figures in parentheses are statistics for all language data)

Raftel. First, looking at the metric related to the degree of segmentation and usage of classes, YAGO and Raftel have the smallest number of classes in Table [2,](#page-3-0) but more than 80% of classes were instantiated. On the other hand, Wikidata, Freebase, and Google KG instantiated less than 10% compared to the large number of classes defined in Ontology. According to the results of the*Class Instantiation*analysis, DBpedia and Raftel fully utilize fine-grained ontology in the knowledge graph. When comparing DBpedia and YAGO, even though YAGO has higher*Instantiated Class Ratio*, DBpedia's *Class Instantiation*shows that it is divided into vertical and horizontal classes, and the classes are actively used in the knowledge graph. In the case of Google KG, the low number of classes that could be imported through the API was reflected in the low*Instantiated Class Ratio*and*Class Instantiation*. Freebase does not define the hierarchy between classes, so it seems to affect the low value of *Class Instantiation*. When it comes to *Inverse Multiple Inheritance*, Freebase is calculated as 1 because classes do not have parent classes, and has the most concise ontology structure. Schema.org(Google KG's ontology) and YAGO have a high complexity due to its relatively frequent multiple inheritance.

Referring the property-related metrics, DBpedia and Wikidata have a large number of properties defined in the ontology(Table [2\)](#page-3-0) and *Subclass Property Acquisition*shows the large number of properties are added as classes are subdivided. On the other hand, for Freebase, the number of properties of Table [2](#page-3-0) is large, but the value of*Subclass Property Acquisition*is low because the ontology has no class hierarchy. Google KG only provides basic information about 'name, image, description, class' through the API, so*Subclass Property Acqui-*

*sition*appears low. Looking at*Subclass Property Instantiation*, Wikidata has richly defined properties according to class segmentation in the ontology, but the degree of use is relatively low. DBpedia has abundant properties and those properties are well used in RDF triple. YAGO has small number of properties(Table [2\)](#page-3-0). Also, *Subclass Property Acquisition*and*Subclass Property Instantiation*infers that the degree of segmentation is low.

Raftel, which is based on Wikidata ontology, appears to have high scores in*Class Instantiation*and*Subclass Property Instantiation*, which are the comprehensive score, by organizing classes and properties abundantly in data while refined them according to the criteria of [4.1.](#page-3-1)

Table [4](#page-8-8) shows comprehensive analysis of structural quality metric by categorizing metrics to *Class Metric*(CM) including*Instantiated Class Ratio*, *Class Instantiation*, *Inverse Multiple Inheritance*and*Property Metric*(PM) including*Instantiated Property Ratio*, *Subclass Property Acquisition*, *Subclass Property Instantiation*and calcuating weighted average of them.

Each metric of the structural quality metric was normalized to have a minimum value of 1 and a maximum value of 10, and then metrics belonging to*Class Metric*and metrics belonging to*Property Metric*were averaged to obtain a representative value. After that, the characteristics of the knowledge graph were examined by varying the weights of CM and PM. When the proportion of PM is large, DBpedia showed the highest score, and when the weighted average was the same or the proportion of CM was larger, Raftel showed the highest score. Through this, if the degree of segmentation of the property is important, the quality of DBpedia can be judged to be high, and if the degree of segmenta-

<span id="page-8-8"></span>

|                       | Raftel | Wikidata | DBpedia | YAGO | Google KG | Freebase |
|-----------------------|--------|----------|---------|------|-----------|----------|
| 0.0 × CM + 1.0 × PM   | 7.31   | 6.40     | 9.91    | 3.81 | 4.00      | 1.04     |
| 0.25 × CM + 0.75 × PM | 7.66   | 5.47     | 9.07    | 4.37 | 3.45      | 2.39     |
| 0.5 × CM + 0.5 × PM   | 8.01   | 4.51     | 8.23    | 4.92 | 2.90      | 3.72     |
| 0.75 × CM + 0.25 × PM | 8.36   | 3.57     | 7.40    | 5.47 | 2.34      | 5.06     |
| 1.0 × CM + 0.0 × PM   | 8.71   | 2.63     | 6.56    | 6.03 | 1.79      | 6.4      |

Table 4: normalization of structural quality metric (target language:korean), CM = Class Metrics, PM = Property Metrics

tion of the class is important, the quality of Raftel can be judged to be high.

by applying various metrics from the data quality perspective presented in previous works.

## 5 Conclusion

In this study, six structural quality metrics were proposed as indicators to evaluate the quality of knowledge graphs. Reflecting the view that 'Knowledge graphs should have the ontology that can express knowledge in the real world, and the knowledge graph RDF triples should utilize the ontology sufficiently', we present the*Instantiated Class Ratio*, *Instantiated Property Ratio*, *Class Instantiation*, *Subclass Property Acquisition*, and *Subclass Property Instantiation*. Also, *Inverse Multiple Inheritance*was introduced to ease the complexity of the ontology.

In addition, the structural quality metric was applied to five cross-domain knowledge graphs on the web and Naver's integrated knowledge graph, Raftel for the comparative analysis. Compared to the structure evaluation conducted only in terms of the size and distribution of graphs, it was able to gain in-depth insights on the quality of knowledge graphs.

Structural quality metric sees 'structure' as an important factor in determining the quality of knowledge graphs. According to the results of the structural quality metric analysis, some knowledge graphs with many classes and properties in their ontology have low degree of segmentation and instantiation. On the contrary, some knowledge graphs that have less classes and properties compared to others described knowledge in detail with specified classes and their distinct characteristics. Of course, since each knowledge graph has a different orientation, knowledge graphs with a low score in the structural quality metric can also show good scores in the quality metric in different dimensions. In future studies, it is expected that the strengths and weaknesses of each knowledge graph to be examined with multi-dimensional point of view

## References

- <span id="page-8-2"></span>Sören Auer, Christian Bizer, Georgi Kobilarov, Jens Lehmann, Richard Cyganiak, and Zachary Ives. 2007. [Dbpedia: A nucleus for a web of open data.](https://doi.org/10.1007/978-3-540-76298-0_52) volume 6, pages 722–735.
- <span id="page-8-1"></span>Kurt Bollacker, Colin Evans, Praveen Paritosh, Tim Sturge, and Jamie Taylor. 2008. [Freebase: A collab](https://doi.org/10.1145/1376616.1376746)[oratively created graph database for structuring hu](https://doi.org/10.1145/1376616.1376746)[man knowledge.](https://doi.org/10.1145/1376616.1376746) In*Proceedings of the 2008 ACM SIGMOD International Conference on Management of Data*, SIGMOD '08, page 1247–1250, New York, NY, USA. Association for Computing Machinery.
- <span id="page-8-3"></span>Janez Brank, Marko Grobelnik, and Dunja Mladenic.´ 2005. A survey of ontology evaluation techniques. In *Proc. of 8th Int. multi-conf. Information Society*, pages 166–169.
- <span id="page-8-7"></span>Niel Chah. 2018. Ok google, what is your ontology? or: Exploring freebase classification to understand google's knowledge graph. *ArXiv*, abs/1805.03885.
- <span id="page-8-5"></span>HeeSeon Cheon, HyunHo Kim, and Inho Kang. 2021. Taxonomy induction from wikidata using directed acyclic graph's centrality. *Human and Language Technology*, 2021.10a:582–587.
- <span id="page-8-6"></span>Xin Luna Dong, Evgeniy Gabrilovich, Geremy Heitz, Wilko Horn, Ni Lao, Kevin Murphy, Thomas Strohmann, Shaohua Sun, and Wei Zhang. 2014. [Knowledge vault: A web-scale approach to prob](http://www.cs.cmu.edu/~nlao/publication/2014.kdd.pdf)[abilistic knowledge fusion.](http://www.cs.cmu.edu/~nlao/publication/2014.kdd.pdf) In *The 20th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, KDD '14, New York, NY, USA - August 24 - 27, 2014*, pages 601–610. Evgeniy Gabrilovich Wilko Horn Ni Lao Kevin Murphy Thomas Strohmann Shaohua Sun Wei Zhang Geremy Heitz.
- <span id="page-8-4"></span>Michael Färber and Achim Rettinger. 2018. Which knowledge graph is best for me? *ArXiv*, abs/1809.11099.
- <span id="page-8-0"></span>Qingyu Guo, Fuzhen Zhuang, Chuan Qin, Hengshu Zhu, Xing Xie, Hui Xiong, and Qing He. 2022. [A](https://doi.org/10.1109/TKDE.2020.3028705)

[survey on knowledge graph-based recommender sys](https://doi.org/10.1109/TKDE.2020.3028705)[tems.](https://doi.org/10.1109/TKDE.2020.3028705) *IEEE Transactions on Knowledge and Data Engineering*, 34(8):3549–3568.

- <span id="page-9-10"></span>Nicolas Heist, Sven Hertling, Daniel Ringler, and Heiko Paulheim. 2020. [Knowledge graphs on the](http://arxiv.org/abs/2003.00719) [web – an overview.](http://arxiv.org/abs/2003.00719)
- <span id="page-9-1"></span>Xiao Huang, Jingyuan Zhang, Dingcheng Li, and Ping Li. 2019. [Knowledge graph embedding based ques](https://doi.org/10.1145/3289600.3290956)[tion answering.](https://doi.org/10.1145/3289600.3290956) In *Proceedings of the Twelfth ACM International Conference on Web Search and Data Mining*, WSDM '19, page 105–113, New York, NY, USA. Association for Computing Machinery.
- <span id="page-9-17"></span>Lucie-Aimée Kaffee, Alessandro Piscopo, Pavlos Vougiouklis, Elena Simperl, Leslie Carr, and Lydia Pintscher. 2017. [A glimpse into babel: An analy](https://doi.org/10.1145/3125433.3125465)[sis of multilinguality in wikidata.](https://doi.org/10.1145/3125433.3125465) In *Proceedings of the 13th International Symposium on Open Collaboration*, OpenSym '17, New York, NY, USA. Association for Computing Machinery.
- <span id="page-9-6"></span>Ravi Lourdusamy and Antony John. 2018. A review on metrics for ontology evaluation. *2018 2nd International Conference on Inventive Systems and Control (ICISC)*, pages 1415–1421.
- <span id="page-9-13"></span>Finn Årup Nielsen, Daniel Mietchen, and Egon Willighagen. 2017. [Scholia, scientometrics and wiki](https://doi.org/10.1007/978-3-319-70407-4_36)[data.](https://doi.org/10.1007/978-3-319-70407-4_36) In *The Semantic Web:*, Lecture Notes in Computer Science, pages 237–259. Springer Nature Switzerland AG.
- <span id="page-9-16"></span>Alessandro Piscopo and Elena Simperl. 2018. [Who](https://doi.org/10.1145/3274410) [models the world? collaborative ontology creation](https://doi.org/10.1145/3274410) [and user roles in wikidata.](https://doi.org/10.1145/3274410) *Proc. ACM Hum.- Comput. Interact.*, 2(CSCW).
- <span id="page-9-11"></span>Alessandro Piscopo and Elena Simperl. 2019. [What](https://doi.org/10.1145/3306446.3340822) [we talk about when we talk about wikidata quality:](https://doi.org/10.1145/3306446.3340822) [A literature survey.](https://doi.org/10.1145/3306446.3340822) In *Proceedings of the 15th International Symposium on Open Collaboration*, Open-Sym '19, New York, NY, USA. Association for Computing Machinery.
- <span id="page-9-14"></span>Radityo Eko Prasojo, Fariz Darari, Simon Razniewski, and Werner Nutt. 2016. Managing and consuming completeness information for wikidata using coolwd. In *COLD@ISWC*.
- <span id="page-9-5"></span>Joe Raad and Christophe Cruz. 2015. A survey on ontology evaluation methods. In *KEOD*.
- <span id="page-9-9"></span>Daniel Ringler and Heiko Paulheim. 2017. One knowledge graph to rule them all? analyzing the differences between dbpedia, yago, wikidata & co. In *KI*.
- <span id="page-9-15"></span>Andreas Spitz, Vaibhav Dixit, Ludwig Richter, Michael Gertz, and Johanna Geiß. 2016. [State of the union:](http://dblp.uni-trier.de/db/conf/icwsm/wiki2016.html#SpitzDRGG16) [A data consumer's perspective on wikidata and its](http://dblp.uni-trier.de/db/conf/icwsm/wiki2016.html#SpitzDRGG16) [properties for the classification and resolution of en](http://dblp.uni-trier.de/db/conf/icwsm/wiki2016.html#SpitzDRGG16)[tities.](http://dblp.uni-trier.de/db/conf/icwsm/wiki2016.html#SpitzDRGG16) In *Wiki@ICWSM*, volume WS-16-17 of *AAAI Workshops*. AAAI Press.

- <span id="page-9-4"></span>Fabian M. Suchanek, Gjergji Kasneci, and Gerhard Weikum. 2007. [Yago: A core of semantic knowl](https://doi.org/10.1145/1242572.1242667)[edge.](https://doi.org/10.1145/1242572.1242667) In *Proceedings of the 16th International Conference on World Wide Web*, WWW '07, page 697–706, New York, NY, USA. Association for Computing Machinery.
- <span id="page-9-18"></span>Thomas Pellissier Tanon, Denny Vrandeciˇ c, Sebas- ´ tian Schaffert, Thomas Steiner, and Lydia Pintscher. 2016. From freebase to wikidata: The great migration. In *World Wide Web Conference*.
- <span id="page-9-7"></span>Samir Tartir, Ismailcem Budak Arpinar, Michael Moore, A. Sheth, and Boanerges Aleman-Meza. 2005. Ontoqa: Metric-based ontology quality analysis.
- <span id="page-9-2"></span>Ilaria Tiddi and Stefan Schlobach. 2022. [Knowledge](https://doi.org/https://doi.org/10.1016/j.artint.2021.103627) [graphs as tools for explainable machine learning: A](https://doi.org/https://doi.org/10.1016/j.artint.2021.103627) [survey.](https://doi.org/https://doi.org/10.1016/j.artint.2021.103627) *Artificial Intelligence*, 302:103627.
- <span id="page-9-3"></span>Denny Vrandeciˇ c and Markus Krötzsch. 2014. ´ [Wiki](http://cacm.acm.org/magazines/2014/10/178785-wikidata/fulltext)[data: A free collaborative knowledge base.](http://cacm.acm.org/magazines/2014/10/178785-wikidata/fulltext) *Communications of the ACM*, 57:78–85.
- <span id="page-9-12"></span>Richard Y. Wang and Diane M. Strong. 1996. [Be](https://doi.org/10.1080/07421222.1996.11518099)[yond accuracy: What data quality means to data con](https://doi.org/10.1080/07421222.1996.11518099)[sumers.](https://doi.org/10.1080/07421222.1996.11518099) *J. Manage. Inf. Syst.*, 12(4):5–33.
- <span id="page-9-8"></span>Amrapali Zaveri, Dimitris Kontokostas, Sebastian Hellmann, Jürgen Umbrich, Michael Färber, Frederic Bartscherer, Carsten Menne, Achim Rettinger, Amrapali Zaveri, Dimitris Kontokostas, Sebastian Hellmann, and Jürgen Umbrich. 2018. [Linked data](https://doi.org/10.3233/SW-170275) [quality of dbpedia, freebase, opencyc, wikidata, and](https://doi.org/10.3233/SW-170275) [yago.](https://doi.org/10.3233/SW-170275) *Semant. Web*, 9(1):77–129.
- <span id="page-9-0"></span>Xiaohan Zou. 2020. [A survey on application of knowl](https://doi.org/10.1088/1742-6596/1487/1/012016)[edge graph.](https://doi.org/10.1088/1742-6596/1487/1/012016) *Journal of Physics: Conference Series*, 1487(1):012016.

# A Appendix

## A.1 Basic Statistics

## A.1.1 Number of Classes

![](_page_10_Figure_3.jpeg)

Figure 2: Number of Classes (target language: Korean)

![](_page_10_Figure_5.jpeg)

## A.1.2 Number of Properties

Figure 3: Number of Properties (target language: Korean)

# A.1.3 Number of RDF Triples

![](_page_11_Figure_1.jpeg)

Figure 4: Number of RDF Triples (target language: Korean)

![](_page_11_Figure_3.jpeg)

# A.1.4 Number of Instances

Figure 5: Number of Instances (target language: Korean)

# A.2 Structural Quality Metrics

## A.2.1 Instantiated Class Ratio

![](_page_12_Figure_2.jpeg)

Figure 6: Instantiated Class Ratio (target language: Korean)

![](_page_12_Figure_4.jpeg)

## A.2.2 Instantiated Property Ratio

Figure 7: Instantiated Property Ratio (target language: Korean)

## A.2.3 Class Instantiation

![](_page_13_Figure_1.jpeg)

Figure 8: Class Instantiation (target language: Korean)

![](_page_13_Figure_3.jpeg)

# A.2.4 Inverse Multiple Inheritance

Figure 9: Inverse Multiple Inheritance (target language: Korean)

## A.2.5 Subclass Property Acquisition

![](_page_14_Figure_1.jpeg)

Figure 10: Subclass Property Acquisition (target language: Korean)

![](_page_14_Figure_3.jpeg)

# A.2.6 Subclass Property Instantiation

Figure 11: Subclass Property Instantiation (target language: Korean)
