---
cite_key: blvd_2013
title: Temporal Reasoning in AI Systems
authors: Abhishek Sharma3840 Far West Blvd
year: 2013
date_processed: '2025-07-02'
phase2_processed: true
original_folder: temporal_cognitive_arxiv_2502.00020_Temporal_Reasoning_in_AI_systems
images_total: 1
images_kept: 1
images_removed: 0
tags:
- Healthcare
- Knowledge Graph
- Machine Learning
- Natural Language Processing
- Semantic Web
- Temporal
keywords:
- AlbertEinstein
- BillClinton
- BiologicalLivingObject
- ComputerScientist
- DayFn
- FemaleHuman
- FemaleInfant
- FrequentPerformerFn
- HumanAdult
- HumanInfant
- abhishek sharma
- analysis-related
- and learning
- application-specific
- artificial intelligence
- bidirectional projection
- cognitive science
- computational intelligence
- conclusions and discussion
- discrete-time
- domain-specific
- event calculus in temporal projection
- event-type
- experimental evaluation
- figure 2 algorithm used for temporal projection
- generation learning
- graph-based
- graph-based reasoning
- hazard function
- in learning
---

# Temporal Reasoning in AI Systems

**Abhishek Sharma**3840 Far West Blvd, Austin, TX 78731 abhishek81@gmail.com

## Abstract

Commonsense temporal reasoning at scale is a core problem for cognitive systems. The correct inference of the duration for which fluents hold is required by many tasks, including natural language understanding and planning. Many AI systems have limited deductive closure because they cannot extrapolate information correctly regarding existing fluents and events. In this study, we discuss the knowledge representation and reasoning schemes required for robust temporal projection in the Cyc Knowledge Base. We discuss how events can start and end risk periods for fluents. We then use discrete survival functions, which represent knowledge of the persistence of facts, to extrapolate a given fluent. The extrapolated intervals can be truncated by temporal constraints and other types of commonsense knowledge. Finally, we present the results of experiments to demonstrate that these methods obtain significant improvements in terms of Q/A performance.

## Introduction and Motivatio[n](#page-0-0)

Modern cognitive systems are expected to reason about a complex and dynamic world. Commonsense temporal reasoning plays an important role in reasoning about a continuously changing environment. Since even the largest knowledge bases (KBs) lack complete knowledge of the outside world, cognitive systems must employ heuristic reasoning and estimate how long a given state is likely to persist. For example, if Fred falls down and sprains his ankle, he is expected to be in pain for a short while. If Fred's younger brother was born in 2013, it is to be expected that he will start to walk and talk within a few years. How can an AI system with incomplete information reason about these events? How long do facts persist? How do individuals change over time and what factors are relevant for understanding inter-individual differences? What events are expected to occur and when do they occur? What changes their probabilities of occurrence?

<span id="page-0-0"></span>Many knowledge-based systems do not represent time correctly and they do not perform sophisticated temporal reasoning. In particular, the problem of temporal projection (i.e., the persistence of facts) has not received sufficient attention in the knowledge-based systems community. For this reason, many cognitive systems have limited deductive closure because existing facts (true at a given time point) cannot be extrapolated to answer questions at other time points. What types of knowledge representation and reasoning schemes are needed to solve these problems?

In this study, we use techniques from discrete time survival analysis to answer these questions. We discuss how events start and end risk periods during which an interval for a fluent (a time-varying property of the world) could be terminated. After identifying the starting points of the risk periods, we use hazard functions to construct an interval during which a time-dependent sentence is highly likely to be true. These intervals can be truncated by temporal constraints and other types of commonsense knowledge. We discuss how different temporal properties of predicates and collections can be used to infer hazard functions. Next, we explain how time (in)dependent covariates can be specified to scale the parameters of hazard functions. The role of event calculus in the context of temporal projection is then discussed, which is often used to maintain correct temporal intervals for fluents in databases. However, some of the predictions made by event calculus might be erroneous if relevant information about the expected duration for which fluents hold is not available. Thus, we discuss how survival functions can be used to alleviate this problem. Next, we explain how the parameters of these survival distributions can be learnt from data.

This paper is organized as follows. We start by discussing related work. Then we provide a brief introduction to the Cyc Knowledge Base (Cyc KB). Next, we discuss our temporal projection algorithm and the knowledge representation it requires. We conclude by discussing our experimental results and plans for future research.

## Related Work

In AI, the problem of temporal projection has been studied in the context of the frame problem [Hanks & McDermott 1986]. The use of survival functions for temporal projection in AI was initiated by [Dean & Kanazawa 1988] and it was extended by other researchers [Tawfik & Neufeld 2000]. Issues related to temporal abstraction in the medical domain were discussed in [Shahar 1997] and temporal-semantic properties were introduced in [Shoham 1987]. However, none of these addressed the problem in the context of improving Q/A performance of large-scale cognitive systems. The work presented in the present study is closest to that discussed by [Lenat 1998] and [Singer & Willet 2003]. Previous studies have developed probabilistic models for temporal and probabilistic reasoning [Hanks & McDermott 1993], but few researchers have focused on discussing knowledge-representation and reasoning issues that would help large logic-based AI systems to perform robust temporal projection and answer a wide range of answers.

## Background

In this section, we summarize the key conventions used by Cyc [Lenat & Guha 1990, Matuszek*et al.*2006]. Cyc represents concepts as collections. Each collection is a kind or type of thing, the instances of which share a certain property, attribute, or feature. For example,*Cat*is a collection of all cats, and only cats. Collections are arranged hierarchically by the*genls*relation.*(genls <sub> <super>)* means that anything that is an instance of <sub> is also an instance of <super>. Predicates are also arranged in hierarchies. (*genlPreds*<s> <g>) means that <g> is a generalization of <s>. The collection*Situation*is an important part of Cyc's ontology. Each instance of*Situation*is a state or event that comprises one or more objects with certain properties or certain relations with each other.*Event*and*StaticSituation*are notable specializations of*Situation*. In Cyc, contexts are represented as *microtheories*. Each microtheory groups a set of assertions together that share some common assumptions. The time dimension of contexts can be specified [Lenat 1998]. For example, the following sentence represents the fact that Tony Greig was a cricketer between 1972 and 1977.

Monadic microtheory[1](#page-1-0) : PeopleDataMt Time dimension:

 (TimeIntervalInclusiveFn (YearFn 1972) (YearFn 1977)) Sentence: (isa TonyGreig-Cricketer Cricketer) In Cyc, instances of *TimeDependentCollection*and*TimeDependentRelation*can be used to represent fluents.

Each instance of*TimeDependentCollection*is a collection

where the membership changes over time. For example,*Professor*is a time-dependent collection, whereas*Integer*is not. Similarly,*TimeDependentRelation*is the collection of all relations such that nothing remains in their eternal extensions. For example,*'owns'*and*'likesAsFriend'*are time-dependent relations. Inference and learning in Cycbased systems can be guided by several heuristics [Sharma et al 2016, Sharma & Goolsbey 2017, Sharma & Goolsbey 2019, Sharma & Forbus 2010, Forbus et al 2009].

## Risk Periods and Discrete-Time Survival Analysis

Let us assume that T<sup>0</sup> was the last time point when fluent P was known to be true and no events are known to have occurred that affect the persistence of P[2](#page-1-1) . If we lack perfect knowledge, we need to extrapolate and find a reasonable assessment of whether P would be true at time T0+∆. Systems that use probabilistic logic might compute and use Prob (holds (P, T0+∆)) directly. Other systems that use traditional forward and backward inference might compute Prob (holds (P, t)) for different values of t, and derive an interval ([T1, T2]) around T<sup>0</sup> in which the fluent P is highly likely to be true. If we assert that P is true in [T1, T2], this assertion can participate in forward and backward inference in the same manner as any other assertion in the K[B](#page-1-2)<sup>3</sup> .

Consider the following sentences:

| (isa Fred BiologicalLivingObject) | (A1) |
|-----------------------------------|------|
|                                   |      |

| (isa Fred Married)           | … (A2) |
|------------------------------|--------|
| (isa Fred MicrosoftEmployee) | … (A3) |

Let us assume that A1, A2, and A3 were true in the year 1990, and we need to find the likelihood of their being true in the year 1992. Since the state represented by A1 is terminated by a death event, we have to find the probability of the occurrence of a death event in the time interval 1990–1992. Similarly, the likelihood of the truth of A2 in 1992 depends on Fred's age and on the duration for which he has been married. Therefore, the process of computing these likelihoods involves the following steps. (a)**Identification of the starting points of** *risk periods* **when a state could be terminated**: Since states can be terminated as soon as they are started, this starting point is specified by the event that initiates the state. For example, the starting points of the risk periods for A1, A2, and A3 are given by the birth date, the wedding date, and the hiring date, respectively. This knowledge can be

<span id="page-1-0"></span><sup>1</sup> A monadic microtheory is a temporally or otherwise unqualified microtheory.

<span id="page-1-1"></span><sup>2</sup> The case when relevant events are known to have occurred is discussed in the next section.

<span id="page-1-2"></span><sup>3</sup> Obviously, temporal projection should not be used recursively. When contradictory information arrives, the time intervals of these assertions are updated (discussed below).

represented in the following format: (eventTypeStartsRolePlayersRiskPeriodForState

 EVENT-TYPE ROLE STATE). This states that an event of type 'EVENT-TYPE' starts a risk period in which the individual who plays the role 'ROLE' in the event[4](#page-2-0) could become an instance of 'STATE'. This information can be used to derive sentences such as A5.

(eventStartsRiskPeriodForSentence

 WeddingEvent-001 (isa Fred Divorced)) ….(A5) If Fred's wedding event happened on July 1, 1988, then we can derive A6.

(startingPointOfRiskPeriodOfSentence

 (isa Fred Divorced) (DayFn 1 (MonthFn July (YearFn 1988)))) ….(A6) Assertions such as A6 can be derived for each of Fred's weddings.

(b) **Specification of the** *hazard function*: Given the starting point of the risk period, we can calculate the probability that a state-terminating event would occur in a given time interval. Let us divide continuous time into a sequence of time intervals (0, t1], (t1, t2], ..., and so forth, and let (tj-1, tj] be the *j*th time interval. Then, if T is the discrete random variable that indicates the time interval during which a state terminating event occurs, then the discrete hazard, hj, is the conditional probability that a randomly selected individual will experience the stateterminating event in the*j*th time interval, given that he/she has not experienced it in preceding time intervals [Singer & Willett 1993, Singer & Willett 2003]:

 h<sup>j</sup> = Pr ( T = j | T ≥ j) ...(E1) Thus, it follows that:

Pr(T > k) = (1-h<sub>1</sub>)(1-h<sub>2</sub>)...(1-h<sub>k</sub>)
=
$$
\prod (1-hj)
$$
...(E2)

$$
Pr(T = k) = (1-h1)(1-h2)...(1-hk-1).hk= hk. \prod(1-hj) \qquad ...(E3)
$$

![](_page_2_Figure_10.jpeg)
<!-- Image Description: The image displays a line graph illustrating survival likelihood against age (years). The graph shows a high survival likelihood (near 1.0) until around age 30, after which it declines steeply, reaching near zero by age 44. The data points are marked with diamonds. The graph likely depicts mortality data relevant to the paper's subject, possibly showing the lifespan or survival rate of a specific organism or system. -->

Figure 1: Likelihood of truth of sentences of type (isa <ins> Cricketer) as a function of age.

Given sentences like A6, we will find the last known starting point of risk period. Then expression E2 can be

used to calculate the likelihood that sentences such as A1, A2, and A3 persist at the time T0+∆. An example of such survival likelihoods (estimated by Cyc) is shown in Figure 1. We see that the professional career of cricketers starts ending when they are in their mid-30s, and virtually all of them retire before they are 45 years old. Each instance of the time-dependent collection and relations will potentially require different types of distributions and parameter values. Given the type of these distributions and the values of their associated parameter values, Cyc will use them automatically to extrapolate fluents. However, some distributions can be specified more easily if we use the following temporal semantic properties. (a)**Initial Collections**: In CycL, an instance, COL, of InitialCollection is defined such that any instance of COL starts as an instance of it, and if the instance changes so it is no longer an instance, it can never become an instance again. "NeverSchooled" and "FemaleInfant" are instances of InitialCollection. Thus, if (isa Tom NeverSchooled) was true on January 1, 1980, Cyc would use the property of the initial collection and assert that Tom was an instance of that collection from his birth until January 1, 1980. (b) **Terminal Collection**: Similarly, in CycL, an instance, COL, of TerminalNonInitialCollection, is a collection such that when a thing becomes an instance of COL, it must remain so while it exists. The collection "HumanAdult" and "Graduate" are examples of terminal collection. (c) **Bidirectional Projection**: In some cases, fluents persist as long as the individual exist[s](#page-2-1) 5 (e.g., FemaleHuman). Cyc's temporal projection module uses these properties.

How does this analysis change when we know other facts that affect the persistence of a given sentence? In the present study, we consider two ways in which this change might occur.

(a) **Temporal Constraints**: Consider the following sentences:

Microtheory: PeopleDataMt Time Interval: (YearFn 1998) Sentence: (isa JohnMcCarthy-ComputerScientist Professor) ...(A7)

Microtheory: PeopleDataMt Time Interval: (YearFn 2001)

Sentence: (isa JohnMcCarthy-ComputerScientist RetiredPerson) ...(A8) Given a sentence such as A7, Cyc's temporal projection module would try to extrapolate and construct a time interval around 1998 during which John McCarthy was a professor. However, a sentence such as A8 suggests that he

<span id="page-2-0"></span><sup>4</sup> For the sentence A2, we want to state that the wedding event starts a risk period in which the individual who plays the role "groom" could enter the state "Divorced". A similar sentence would be needed for the bride.

<span id="page-2-1"></span><sup>5</sup> For simplicity, we ignore the possible occurrence of relatively rare gender change events. Temporal projection of sentences of type (isa <ins> COL) where COL is a specialization of BiologicalLivingObject, often involves reasoning about the life expectancy of an individual. This is done with the help of hazard functions such as E1, which are calculated using mortality rates.

was not a professor in 2001. We represent this information using the following sentence.

(followingStageTypes Professor RetiredPerson)…(A9)

Sentence A9 represents that a person's life as a professor ends before his life as a retired person begins<sup>6</sup> [.](#page-3-0) Let P represent the fluent "John McCarthy is a professor." Then, based on only A8 and A9, Cyc can infer that John McCarthy was a professor at time point T if the following conditions are met: (a) Prob (P, T) > threshold, and (b) ⌐ (Prob (Q, T) > threshold), where Q is an assertion that is incompatibl[e](#page-3-1)<sup>7</sup> with P.

(b) **Covariates**: Temporal constraints can help us to represent the incompatibility of two assertions that mainly limit the time interval during which assertions are deemed to hold. However, additional information about an individual might change the rate of decay of persistence. For example, a sentence such as A10 is a time-dependent covariate for A11.

Microtheory: PeopleDataMt

Time interval: 1970 to 1975.

Sentence: (isa Fred (FrequentPerformerFn Smoking)) ...(A10) Sentence: (isa Fred BiologicalLivingObject) …(A11)

Other covariates (e.g., gender) can be time independent. To scale the hazard when such covariates are present, an expression such as E4 is used.

 h(i) ← 1/ (1+e-ɑ(i) e (-Σβ(i)\*X(i))) …(E4) Recall that h(i) is the hazard for the ith time interval. Here, each X(i) is a Boolean variable that corresponds to a covariate such as A10. The value of X(i) is 1 if the covariate is present in the ith time interval, but zero otherwise. The parameters β(i) represent the strengths of the covariates. When a sentence such as A11 is true in an interval *i*, the value of h(i) increases, which leads to a sharper decline in the probability of the persistence of A11. When all of the values of X(i) are zero, the hazard function for the ith time interval reduces to E5.

$$
h(i) \leftarrow 1/(1 + e^{-a(i)}) \qquad ...(E5)
$$

Expression E5 represents the baseline hazard function, which is determined by the parameter ɑ(i). Information about covariates can be represented by assertions such as the following.

(timeDependentCovariateForCollection BiologicalLivingObject (FrequentPerformerFn Smoking) 0.3) …(A12)

The last argument in A12 is used to specify the value of β(i). Similar assertions are used for time-independent covariates.

Hazard functions can also be used to infer the persistence of time-dependent predicates. However, in some cases, we need an additional vocabulary for plausible inferences. Consider the following sentences:

| (owns AlbertEinstein Car-780)                         | …(A13) |
|-------------------------------------------------------|--------|
| (owns AlbertEinstein Toothbrush-392)                  | …(A14) |
| The sentences A13 and A14 should have different decay |        |

rates. Therefore, we need to specify hazard functions for handling sentences where an instance of a certain collection appears in a given argument position in a predicate<sup>8</sup> [.](#page-3-2) If the known specific conditions are not satisfied for a given assertion, then we must employ generic hazard functions that apply to a given predicate.

## Event Calculus in Temporal Projection

The inferences made by the methods discussed above are non-monotonic in nature. When contradictory information arrives, we can use methods based on both event calculus and survival analysis to maintain a consistent KB. Let us start with the basics of event calculus. Briefly, fluents are considered true at a time point if they have been initiated by an event previously, but have not been terminated in the meantime. Similarly, a fluent is false if it has been terminated previously but has not been initiated in the meantime [Miller & Shanahan 2002]. In Cyc, domaindependent axioms are written to derive sentences such as the following, which represent knowledge about situations that start and end time intervals for fluents.

(situationStartsIntervalForSentence s f) …(A15) (situationEndsIntervalForSentence t g) …(A16)

The first sentence above denotes that situation *s*starts a time interval during which the fluent*f*holds. The core persistence axiom employed in simplified event calculus is as follows [Sadri & Kowalski 1995].

|  |  |                     | Holds(P, T) ← Happens (E1, T1) and Initiates (E1, P) and |            |  |
|--|--|---------------------|----------------------------------------------------------|------------|--|
|  |  | T1 < T and ~∃E2, T2 | (Happens (E2, T2) and                                    |            |  |
|  |  |                     | Terminates (E2, P) and T1 < T2 < T)                      | …<br>(A17) |  |

However, the original event calculus description [Kowalski & Sergot 1986] suggested that extra application-specific rules can be added to infer whether an interval for a fluent has been broken if the known events are too far apart for it to hold continuously. This problem can be solved if we combine the event calculus with the survival analysisbased methods discussed above. In step 1a of the algorithm

<span id="page-3-0"></span><sup>6</sup> In CycL, the collection RetiredPerson is the collection of people who have retired permanently.

<span id="page-3-1"></span><sup>7</sup> In this case, sentences such as "John McCarthy is a retired person." and "John McCarthy is an infant." are incompatible with P. Such incompatibility can often be inferred by using 'disjointWith' assertions. For instance, (disjointWith HumanInfant Professor) holds.

<span id="page-3-2"></span><sup>8</sup> For A13, the relevant hazard function represents our knowledge of how long automobiles are owned.

shown in Figure 2, we use A17 to construct an interval [T1, T2] for a fluent P. However, the intervals created in step 1b are preferre[d](#page-4-0)<sup>9</sup> if they are subsumed by [T1, T2]. Since hazard functions represent knowledge about how long states persist, this helps us to avoid the error caused when excessively wide time intervals are produced due to incomplete knowledge of the outside world. Since many events that start/end intervals for P might be known to us, we create a timeline of events and choose E1 and E2 such that following condition is satisfied.

happens (E1, T1), happens (E2, T2), T1 < T < T2,

Initiates(E1, P), Terminates (E2, P),

- ~∃E3 such that (happens(E3, T3), Initiates (E3, P),
- T1 < T3 < T < T2) , ~∃E4 such that (happens(E4, T4),

Terminates (E4, P), T1 < T < T4< T2) …(C1)

In step 2, when all known events start time intervals for P, we use C2 to choose an event E1, and use the hazard function to create an interval that extends forward from E1.

happens(E1, T1), Initiates (E1, P) and ~∃E2 such that (happens (E2, T2) and T1 < T2 < T and Initiates (E2, P)) …(C2)

happens(E1, T1), Terminates (E1, P) and ~∃E2 such that (happens (E2, T2) and T < T2 < T1 and Terminates (E2, P)). …(C3)

Conditions C1, C2 and C3 help us identify events that are most temporally proximate to P. When all known events end intervals for the given fluent, we use C3 to choose the closest event and create an interval that extends backwards from it (step 3). If the intervals created by these events do not subsume T, then the truth of P at T is unlikely to be related to their occurrence and step 4 is executed. In step 4, we use the hazard functions and create a time interval [T5, T6]. In step 5, we look at different constraints that might be applicable and we truncate the interval if necessary.
**Non-survival Analysis-related Vocabulary**: Although survival analysis provides a natural framework for temporal projection, some fluents are less amenable to monotonically decreasing persistence likelihoods. For example, consider the following sentence:

(isa BillClinton UnitedStatesPresident) …(A17) It is plausible to infer that a sentence such as A17 would be true for four years from the inauguration date of the president. To handle these cases, we can derive sentences such as A17.

(statePersistsForDurationFromDate

(isa BillClinton UnitedStatesPresident)

(DayFn 21 (MonthFn January (YearFn 1993))) (YearsDuration 4)) (A17)

These assertions are derived from domain-specific axioms (e.g., axioms about presidential inauguration) and they are treated as default statements. They can be overridden when contradictory information[10](#page-4-1) is available and assertions such as A16 are derived.

| Algorithm: TemporallyProject                                |  |  |  |  |
|-------------------------------------------------------------|--|--|--|--|
| Input: A Knowledge Base, KB                                 |  |  |  |  |
| A fluent, P, true during a time interval, T.                |  |  |  |  |
| A likelihood threshold, ɑ.                                  |  |  |  |  |
| Output: A time interval [T1, T2] that subsumes T, such      |  |  |  |  |
| that if T3 ɛ [T1, T2], then Prob (P, T3) > ɑ.               |  |  |  |  |
| 1. If events E1 and E2 exist such that they start and end   |  |  |  |  |
| intervals for P respectively and satisfy condition C1,      |  |  |  |  |
| then execute 1a–1c, else goto step 2.                       |  |  |  |  |
| (1a) Use A17 to construct an interval [T1, T2] that         |  |  |  |  |
| subsumes T for P.                                           |  |  |  |  |
| (1b) Use the hazard function for P to construct another     |  |  |  |  |
| interval [T3, T4] for P.                                    |  |  |  |  |
| (1c) If [T1, T2] subsumes [T3, T4], then return [T3,        |  |  |  |  |
| T4], else return [T1, T2].                                  |  |  |  |  |
| 2. If all known events start intervals for P, use condition |  |  |  |  |
| C2 to choose an event, and use the relevant hazard          |  |  |  |  |
| function to create an interval [T5, T6] that extends        |  |  |  |  |

then return [T5, T6] else goto step 4 3. If all known events terminate intervals for P, use condition C3 to choose an event and use the relevant hazard function to create an interval [T5, T6] that extends backward from the event. If T is subsumed by [T5, T6] then return [T5, T6] else goto step 4.

forward from the event. If T is subsumed by [T5, T6]

- 4. Use hazard functions to create a time interval [T5, T6] that subsumes T.
- 5. If applicable, use temporal constraints to truncate [T5, T6]. Return the resulting time interval.

### Figure 2: Algorithm used for temporal projection.

**Learning:**How can we learn the parameters of the probability distributions discussed above? We recall that the definitions of hazard functions are reliant on identifying the time interval during which the state terminating event occurs. Therefore, the task of learning the hazard functions requires information in the following format [Singer & Willet 2003].

(i)**A time period variable,** *j*: We need to divide the time period since the start of the risk period into intervals with a suitable length. The time period variable specifies the time period *j*of the record. For example, let us consider sentence A11. Fred's birth event starts the risk period and intervals with a length of one year are suitable for estimating the likelihood of its persistence. Therefore, the

<span id="page-4-0"></span><sup>9</sup> In Figure 2, the intervals created by hazard functions are such that if T lies in the interval then Prob(holds(P, T)) > ɑ, where ɑ is an input to the algorithm.

<span id="page-4-1"></span><sup>10</sup> For fluents involving US presidents, assassination, impeachment or resignation events will terminate intervals for sentences such as A17.

fourth year of Fred's life would correspond to the fourth time interval in our dataset. (ii)**Values of covariates in each time interval**: For each time interval, *j*, we need to obtain the value of the covariate (i.e., the truth of sentences such as A10) in that time interval for the given individual. (iii) **Value of EVENT(***i, j***)**: The variable EVENT(*i, j*) indicates whether the state terminating event for individual *i*occurred during the time period*j*. Given a set of such records, the likelihood of observing the data is given as follows.

L = ∏<sup>i</sup> ∏<sup>j</sup> h(tij) EVENT(i,j) (1-h(tij)) (1-EVENT(i, j))

The values of the hazard functions can be calculated by minimizing L.

| Query set | Mode | #Queries | % Correct | Improvement<br>w.r.t. Mode 1 |
|-----------|------|----------|-----------|------------------------------|
| 1         | M1   | 100      | 28%       | -                            |
|           | M2   | 100      | 56%       | 100%                         |
| 2         | M1   | 3661     | 39%       | -                            |
|           | M2   | 3661     | 57%       | 46%                          |
| 3         | M1   | 423      | 29%       | -                            |
|           | M2   | 423      | 70%       | 141%                         |
| 4         | M1   | 2616     | 43%       | -                            |
|           | M2   | 2616     | 63%       | 47%                          |
| 5         | M1   | 533      | 26%       |                              |
|           | M2   | 533      | 34%       | 31%                          |
| Total     | M1   | 7333     | 39%       |                              |
|           | M2   | 7333     | 58%       | 49%                          |

#### Table 1: Experimental Results

## Experimental Evaluation

To assess the validity of these concepts, we conducted a set of experiments. Five query sets were selected based on the availability of temporally qualified ground facts and their relevance to temporal projection. Every query was in the form: "Sentence s was (will be) true at time T"[11](#page-5-0), where s was a fully bound fluent of the type '(isa <ins> <col>)'. For each of these query sets, we measured the Q/A performance in two modes, as follows. **Mode M1**: In this mode, we aimed to simulate the performance of a traditional reasoning system with no temporal projection module. In addition to simply looking up the KB and using the predicate generalization hierarchy, the inference engine performed a temporal subsumption[12](#page-5-1) test during reasoning. **Mode M2**: In the second mode, in addition to the reasoning done in mode M1, we enabled temporal projection methods discussed in this paper. The results of these experiments are shown in Table 1. We see that there has been significant improvement in Q/A performance in all query sets[13](#page-5-2). The overall improvement in performance with respect to M1 is 49%. The results are statistically significant (p < 0.05).

## Conclusions and Discussion

Commonsense temporal reasoning is a core problem for cognitive systems. To improve commonsense reasoning in general and Q/A performance in particular, modern AI systems must find better ways to reason about how long facts persist. In this study, we proposed different types of knowledge representation schemes, which may help such systems to perform robust temporal projection. The specification of risk periods and hazard functions facilitates the calculation of plausible intervals for fluents. Temporal constraints help to limit intervals and the presence of covariates can scale the parameters of the hazard functions. Event calculus can be integrated with survival analysis to alleviate some of the problems caused by incomplete knowledge. Experiments on a set of over 7000 queries shows that the methods proposed here lead to 49% improvement in Q/A performance on average.

Our results suggest the following future areas of research. First, we have found that in the case of many time dependent collections (e.g., Entertainer, Singer), once people enter these states; the fluent persists until the end of their active life. Therefore, we would like to reason about when individuals are likely to enter a given state, and how they might make transitions among states. Previous research into multi-state processes might be relevant in this context [Crowder 2012]. Second, we would like to extend this research to ensure that we can reason about recurrent and periodic events (e.g., sleeping or going to a grocery store). Finally, the capability to reason about probabilistic effects of events, and estimating the likelihood of event occurrence in a given time interval would be very useful for further improving the results shown in Table 1.

## References

Crowder, M. 2012. *Multivariate Survival Analysis and Competing Risks*. CRC Press.

Dean, T. and Kanazawa, K.. 1988. Probabilistic Temporal Reasoning, *Proceedings of AAAI*, pp. 524-528.

Hanks, S. and McDermott, D. 1986. Default Reasoning, Nonmonotonic logics and the Frame Problem, *Proceedings of the AAAI,* pp. 328-334*.*<span id="page-5-0"></span><sup>11</sup> We included a query only when it could not be answered easily by considering the lifespan of individuals. For instance, a query like "Was John McCarthy a professor in the year 1850?" would be excluded from our experiments. On the other hand, a query like "Was Marvin Minsky a professor in the year 1984?" would be included in our query sets.

<span id="page-5-1"></span><sup>12</sup> A sentence s is considered true during interval T1 if it is known to be true during interval T2, and T2 subsumes T1.

<span id="page-5-2"></span><sup>13</sup> The number of queries in query sets is different due to non-uniform distribution of facts in KB. For example, Cyc KB knows much more about movie actors than about cricketers.

Hanks, S. and McDermott, D. 1993. Modeling a Dynamic and Uncertain World I: Symbolic and Probabilistic Reasoning about Change.*Artificial Intelligence,*Vol. 43.

Kowalski, R. 1992. Database Updates in the Event Calculus.*Journal of Logic Programming,*12, pp. 12-146.

Kowalski, R. and Sergot, M. 1986. A Logic-based Calculus of Events,*New Generation Computing*, Vol. 4, pp. 67-94.

Lenat D. and Guha, R. V. 1990 *Building Large Knowledge-Based Systems: Representation and Inference in the Cyc Project*. Addison Wesley.

Lenat, D. 1998. The Dimensions of Context Space. Available at www.cyc.com.

Matuszek, C., Witbrock, M., De Olivieira, J., 2006. An Introduction to the Syntax and Content of Cyc. AAAI Spring Symposium, pp. 44-49.

Miller, R. and Shanahan, M. 2002. Some Alternative Formulations of the Event Calculus, LNAI, Vol 2408, Springer.

McDermott, D. 1982. A Temporal Logic for Reasoning About Processes and Plans. *Cognitive Science*, 6, pp. 101-155.

Sadri, F. and Kowalski, R. 1995. Variants of the Event Calculus. *Proc. of ICLP.*Shahar, Y. 1997. A Framework for Knowledge-Based Temporal Abstraction,*Artificial Intelligence*, 90 (1-2), pp. 79-133.

Shoham, Y. 1987. Temporal Logics in AI: Semantical and Ontological Considerations, *Artif. Intell*., 33(1), pp. 89-104.

Singer, J. D. and Willett, J. B., 1993. It's about time: Using Discrete-Time Survival Analysis to Study Duration and Timing of Events, *Jl. of Educational Statistics,*pp. 155-195.

Singer, J. D. and Willett, J. B., 2003.*Applied Longitudinal Data Analysis: Modeling Change and Event Occurrence*. Oxford University Press.

Sharma, A. and Forbus, K. D.. 2010. Modeling the Evolution of Knowledge and Reasoning in Learning Systems, AAAI Fall Symposium Series.

Sharma, A. and Forbus, K. D. 2010 Graph-based reasoning and reinforcement learning for improving Q/A performance in large knowledge-based systems, AAAI Fall Symposium Series

Sharma, A. and Goolsbey, K. 2017 Identifying useful inference paths in large commonsense knowledge bases by retrograde analysis, Proceedings of the AAAI Conference on Artificial Intelligence, 31(1).

Forbus, K. D., Lockwood, K., Sharma, A. , Tomai, E. 2009 Steps towards a 2nd generation learning by reading system, AAAI Spring Symposium on Learning by Reading, Spring.

Sharma, A. Witbrock, M. Goolsbey, K. 2016. Controlling search in very large commonsense knowledge bases: a machine learning approach, arXiv preprint arXiv:1603.04402

Tawfik, A. Y. and Neufeld, E. M. 2000. Temporal Reasoning and Bayesian Networks. *Computational Intelligence*, 16 (3), pp. 349-374.
