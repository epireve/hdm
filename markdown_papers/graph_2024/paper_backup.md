---
cite_key: "graph_2024"
title: "Personalized Entity Resolution with Dynamic Heterogeneous Knowledge Graph Representations"
authors: "merging the product knowledge graph, the customer-product graph, we obtain a more comprehensive graph (Figure [1\(](#page-1-0)c)) of higher connectivity. For example, in the original customer-product graph, Customer 1, Customer 2 are disconnected because they do not share any purchase. In the new graph, they have an indirect connection through Product 2, Product 3, which share the same flavor, ingredient."
year: 2024
doi: "arXiv:2104.02667"
url: "https://arxiv.org/abs/2104.02667"
relevancy: "High"
tldr: "Novel approach to entity resolution using dynamic heterogeneous knowledge graphs with personalization for improved accuracy."
insights: "Customers tend to use \"implicit utterances\" creating multiple product candidates. Framework builds \"cross-source heterogeneous knowledge graph\" from customer purchase history with personalized features."
summary: "This paper proposes a framework that builds cross-source heterogeneous knowledge graphs from customer purchase history to improve entity resolution accuracy through personalized features."
research_question: "How can entity resolution accuracy be improved in shopping domains where customers use implicit utterances?"
methodology: "Neural reranking model with cross-source heterogeneous knowledge graph construction; joint learning of customer and product embeddings."
key_findings: "24.6% improvement in accuracy of top ranked candidates compared to state-of-the-art; personalized entity resolution through dynamic knowledge graphs."
limitations: "Limited to shopping domain; evaluation primarily focused on product search scenarios."
conclusion: "Demonstrates significant accuracy improvements through personalized entity resolution with dynamic heterogeneous knowledge graphs."
future_work: "Extend to other domains; evaluate scalability; develop privacy-preserving methods."
implementation_insights: "Provides technical approach for implementing personalized entity resolution using dynamic heterogeneous knowledge graphs."
tags:
  - "Entity Resolution"
  - "Heterogeneous Knowledge Graphs"
  - "Personalization"
  - "Cross-Source Integration"
---

# Personalized Entity Resolution with Dynamic Heterogeneous Knowledge Graph Representations

Ying Lin, Han Wang, Jiangning Chen, Tong Wang, Yue Liu, Heng Ji, Yang Liu, Premkumar Natarajan

Amazon Alexa AI

{linzying,wnghn,cjiangni,tonwng,jihj,yangliud,premknat}@amazon.com

# Abstract

The growing popularity of Virtual Assistants poses new challenges for Entity Resolution, the task of linking mentions in text to their referent entities in a knowledge base. Specifically, in the *shopping* domain, customers tend to use implicit utterances (e.g., "organic milk") rather than explicit names, leading to a large number of candidate products. Meanwhile, for the same query, different customers may expect different results. For example, with "add *milk* to my cart", a customer may refer to a certain organic product, while some customers may want to re-order products they regularly purchase. To address these issues, we propose a new framework that leverages personalized features to improve the accuracy of product ranking. We first build a cross-source heterogeneous knowledge graph from customer purchase history and product knowledge graph to jointly learn customer and product embeddings. After that, we incorporate product, customer, and history representations into a neural reranking model to predict which candidate is most likely to be purchased for a specific customer. Experiments show that our model substantially improves the accuracy of the top ranked candidates by 24.6% compared to the state-of-the-art product search model.

# 1 Introduction

Given an entity mention as a query, the goal of entity resolution (or entity linking) [\(Ji and Grishman,](#page-7-0) [2011\)](#page-7-0) is to link the mention to its corresponding entry in a target knowledge base (KB). In an academic shared task setting, an entity mention is usually a name string, which can be a person, organization or geo-political entity in a news context, and the KB is usually a Wikipedia dump with rich structured properties and unstructured text descriptions. Stateof-the-art entity resolution methods can achieve higher than 90% accuracy in such settings [\(Ji and](#page-7-0)

[Grishman,](#page-7-0) [2011;](#page-7-0) [Ji et al.,](#page-7-1) [2015;](#page-7-1) [Agarwal and Bikel,](#page-7-2) [2020\)](#page-7-2), and they have been successfully applied in hundreds of languages [\(Pan et al.,](#page-7-3) [2017\)](#page-7-3) and various domains such as disaster management [\(Zhang](#page-8-0) [et al.,](#page-8-0) [2018a\)](#page-8-0) and scientific discovery [\(Wang et al.,](#page-8-1) [2015\)](#page-8-1). Therefore, we tend to think entity resolution is a solved problem in academia. In industry, with the rise in popularity of Virtual Assistants (VAs) in recent years, an increasing number of consumers now rely on VAs to perform daily tasks involving entities, including shopping, playing music or movies, calling a person, booking a flight, and managing schedules. The scale and complexity of industrial applications presents the following unique new challenges.

Unpopular majority. There is a massive number of new entities emerging every day. The entity resolver may know very little about them since very few users interact with them. Handling these tail entities effectively requires the use of property linkages between entities and shared user interests

Large number of ambiguous variants. When interacting with VAs, users tend to use short and less informative utterances with the expectation that the VAs can intelligently infer their actual intentions. This further raises the need for the technique to resolve entities with *personalization*.

In the *shopping* domain, this problem is even more challenging as customers typically use implicit entity reference utterances (e.g., "organic milk") instead of explicit names (e.g., "Horizon Organic Shelf-Stable 1% Lowfat Milk") which usually lead to a large number of candidates due to the ambiguity. However, with VAs' voice user interface (VUI), the number of products that can be shown to the customers is very limited. In this work, we focus on the problem of *personalized entity resolution* in the shopping domain. Given a query and a list of retrieved candidates, we aim to return the product that is most likely to be pur-

<span id="page-1-0"></span>![](_page_1_Figure_0.jpeg)

Figure 1: An illustration of the cross-source heterogeneous customer-product graph.

chased by a customer.

We make three assumptions: (H1) customers tend to purchase products they have purchased in the past; (H2) customers tend to purchase a set of products that share some properties; (H3) two customers who purchased products with similar properties may share similar interests. Based on these assumptions, we propose to represent customers and products as low-dimensional distributional vectors learned from a graph of customers and products. However, unlike social media sites with rich interactions among users, customers of most shopping services are isolated, which prevents us from learning user embeddings as distributed representations. To address this issue, we propose to build a cross-source heterogeneous knowledge graph as Figure [1](#page-1-0) depicts to establish rich connections among customers from two data sources, users' purchase history (customer-product graph) and product knowledge graph, and further jointly learn the representations of nodes in this graph using a Graph Neural Network (GNN)-based method. We further propose an attentive model to generate a query-aware history representation for each user based on the current query.

Experiments on real data collected from an online shopping service show that our method substantially improves the purchase rate and revenue of the top ranked products.

# 2 Methodology

Given a query q from a customer c, and a list of candidate products P = {p1, ..., pL}, where L is the number of candidates, our goal is to predict the product that the customer will shop for based on the customer's purchase history and the product

knowledge graph. Specifically, we use purchase records {r1, ..., rH} where H is the number of historical records. As Figure [2](#page-1-1) illustrates, we jointly learn customer and product embeddings from a cross-source customer-product graph using GNN. To perform personalized ranking, we incorporate the learned customer embedding and the queryaware history representation as additional features when calculating the score of each candidate. We then rank all candidates by score and return the top one.

<span id="page-1-1"></span>![](_page_1_Figure_8.jpeg)

Figure 2: An illustration of our framework.

### 2.1 Candidate Retrieval

We first retrieve candidate products for each query using QUARTS [\(Nigam et al.,](#page-7-4) [2019;](#page-7-4) [Nguyen et al.,](#page-7-5) [2020\)](#page-7-5), which is an end-to-end neural model for product search. QUARTS has three major components: (1) an LSTM-based (long short-term memory) classifier that predicts whether a query-product pair is matched; (2) a variational query generator that generates difficult negative examples, and (3) a state combiner that switches between query representations computed by the classifier and generator.

#### 2.2 Joint Customer and Product Embedding

The next step is to obtain the representations of customers and products. Customer embeddings are usually learned from user-generated texts [\(Preo¸tiuc-](#page-8-2)[Pietro et al.,](#page-8-2) [2015;](#page-8-2) [Yu et al.,](#page-8-3) [2016;](#page-8-3) [Ribeiro et al.,](#page-8-4) [2018\)](#page-8-4) or social relations [\(Perozzi et al.,](#page-7-6) [2014a;](#page-7-6) [Grover and Leskovec,](#page-7-7) [2016;](#page-7-7) [Zhang et al.,](#page-8-5) [2018b\)](#page-8-5), neither of which are available in the shopping dataset we use. Alternatively, we establish *indirect* connections among customers through their purchased products under hypothesis H3, and form a customer-product graph as shown in Figure [1\(](#page-1-0)a). This graph only contains a single type of relation (i.e., purchase) and ignores product attributes. As a result, it tends to be sparse and less effective for customer representation learning.

In order to learn more informative embeddings, we propose to incorporate richer information from a product knowledge graph (Figure [1\(](#page-1-0)b)) where products are not only connected to different attribute nodes (e.g., brands, flavors), but they may also be associated with textual features (e.g., title) and boolean features (e.g., isOrganic).

By merging the product knowledge graph and the customer-product graph, we obtain a more comprehensive graph (Figure [1\(](#page-1-0)c)) of higher connectivity. For example, in the original customer-product graph, Customer 1 and Customer 2 are disconnected because they do not share any purchase. In the new graph, they have an indirect connection through Product 2 and Product 3, which share the same flavor and ingredient.

From this heterogeneous graph, we jointly learn customer and product representations using a two-layer Relational Graph Convolutional Network [\(Schlichtkrull et al.,](#page-8-6) [2018\)](#page-8-6). The embedding of each node is updated as:

$$
\boldsymbol{h}_i^{l+1} = \text{ReLU}\Big(\boldsymbol{W}_0^l \boldsymbol{h}_i^l + \sum_{r \in R} \sum_{j \in N_i^r} \frac{1}{|N_i^r|} \boldsymbol{W}_r^l \boldsymbol{h}_j^l \Big),
$$

where h l i is the representation of node i at the l-th layer, N<sup>r</sup> i is the set of neighbor indices of node i under relation r ∈ R, and W<sup>l</sup> 0 and W<sup>l</sup> r are learnable weight matrices.

In order to capture textual features such as product titles and descriptions, we use a pre-trained RoBERTa [\(Liu et al.,](#page-7-8) [2019\)](#page-7-8) encoder to generate a

fix-sized representation for each product. Specifically, we concatenate textual features using a special separator token [SEP], obtain the RoBERTa representation for each token, and then use the averaged embedding to represent the whole sequence. To reduce the runtime, we calculate customer and product embeddings offline and cache the results.

#### 2.3 Candidate Representation

In addition to the product embedding, we further incorporate the following features to enrich the representation of each candidate.

Rank: the order of the candidate returned by the product retrieval system.

Relative Price: how much a product's absolute price is higher or lower than the average price of all retrieved candidates.

Previously Purchased: a binary flag indicating whether a candidate has been purchased by the customer or not.

We concatenate these features with the product embedding and project the vector into a lower dimensional space using a feed forward network.

#### 2.4 History Representation

Although customer embeddings can encode purchase history information, they are static and may not effectively provide the most relevant information for each specific query. For example, if the query is "bookshelf", furniture-related purchase records are more likely to help the model predict the product that the customer will purchase, while if the query is "sulfate-free shampoo", purchase records of beauty products are more relevant. To tackle this issue, we propose to generate a dynamic history representation v based on the current query q from all purchase record representations {v1, ..., vH} of the customer.

We first represent each purchase record as the concatenation of the product embedding, product price, and purchase timestamp. The queryaware history representation is then calculated as a weighted sum of the customer's purchase record representations using an attention mechanism as follows.

$$
e_i = \boldsymbol{v}^\top \tanh \left( \boldsymbol{W}_q \boldsymbol{q} + \boldsymbol{W}_v \boldsymbol{v}_i \right),
$$
$$
a_i = \text{Softmax}(e_i) = \frac{\exp{(e_i)}}{\sum_{k}^{M} \exp{(e_k)}},
$$

$$
\boldsymbol{v} = \sum_i^H a_i \boldsymbol{v}_i.
$$

#### 2.5 Candidate Ranking

We adopt a feed forward neural network that takes in the candidate, customer, and history representations, and returns a confidence score yˆ<sup>i</sup> . The confidence score is scaled to (0, 1) using a Sigmoid function. During training, we optimize the model by minimizing the following binary cross entropy loss function.

$$
\mathcal{L} = -\frac{1}{N} \sum_{i=1}^{N} y_i \log \hat{y}_i + (1 - y_i) \log (1 - \hat{y}_i),
$$

where N denotes the total number of candidates, and y<sup>i</sup> ∈ {0, 1} is the true label. In the inference phase, we calculate confidence scores for all candidates for each session and return the one with the highest score.

# 3 Experiment

#### 3.1 Data

Product Knowledge Graph. In our experiment, we use a knowledge graph of products in five categories (i.e., grocery, beauty, luxury beauty, baby, and health care), which contains 24,287,337 unique product entities. As Figure [1](#page-1-0) depicts, products in this knowledge graph are connected through attribute nodes, including brands, scents, flavors, and ingredients. This knowledge graph also provides rich attributes for each product node. We use two types of attributes in this work, textual features (i.e., title, description, and bullet) and binary features (e.g., isOrganic, isNatural).

Evalution Dataset. We randomly collect 1 million users' purchase sessions from November 2018 to October 2019 on an online shopping service. Each session contains a query, an obfuscated identifier, a timestamp, and a list of retrieved candidate products where only one product is purchased.

We split sessions before and after September 1, 2019 into two subsets. The first subset only serves as the purchase history and is used to construct the customer-product graph. From the second subset, we randomly sample 22,000 customers with at least one purchase record in the first subset and take their last purchase sessions for training or evaluation. Specifically, we use 20,000 sessions for training, 1,000 for validation, and 1,000 for test. If a customer has multiple purchase sessions in the

second subset, other sessions before the last one are also considered as purchase history when we generate history representations, while they are excluded from the customer-product graph, which is constructed from the first subset.

#### 3.2 Experimental Setup

We optimize our model with AdamW for 10 epochs with a learning rate of 1e-5 for the RoBERTa encoder, a learning rate of 1e-4 for other parameters, weight decay of 1e-3, a warmup rate of 10%, and a batch size of 100.

To encode textual features, we use the RoBERTa base model[1](#page-3-0) with an output dropout rate of 0.5. To represent query words, we use 100-dimensional GloVe embeddings pre-trained on Wikipedia and Gigaword[2](#page-3-1) . We set the size of pre-trained customer and product embeddings to 100 and freeze them during training.

We use separate fully connected layers to project candidate and history representations into 100 dimensional feature vectors before concatenating them for ranking. We use a two-layer feed forward neural network with a hidden layer size of 50 as the ranker and apply a dropout layer with a dropout rate of 0.5 to its input.

#### 3.3 Quantitative Analysis

We compare our model to the state-of-the-art product search model QUARTS as the baseline. Because our target usage scenarios are VAs where only one result will be returned to the user, we use Accuracy@1 as our evaluation metric. We implement the following baseline ranking methods.

Purchased: We prioritize products previously purchased by the customer. If multiple candidates are previsouly purchased, we return the one ranked higher by QUARTS.

ComplEx: Customer and product embeddings are learned using ComplEx [\(Trouillon et al.,](#page-8-7) [2016\)](#page-8-7), a widely used knowledge embedding model.

In Table [1,](#page-4-0) we show the relative gains compared to the baseline model QUARTS. With personalized features, our method effectively improves Acc@1 on both development and test sets.

We also conduct ablation studies by removing the following features and show results in Table [2.](#page-4-1) Ranking: In this setting, our model ignores the original retrieval ranking returned by QUARTS.

<span id="page-3-0"></span><sup>1</sup> [https://huggingface.co/transformers/](https://huggingface.co/transformers/pretrained_models.html) [pretrained\\_models.html](https://huggingface.co/transformers/pretrained_models.html)

<span id="page-3-1"></span><sup>2</sup> <https://nlp.stanford.edu/projects/glove/>

Personalized Features: We remove personalized features (e.g., customer embedding, whether a product is previously purchased) in this setting.

Product Embedding: We remove pre-trained product embedding but still use textual features and binary features to represent products.

Joint Embedding: Customer and product embeddings are not jointly learned from the merged graph. Alternatively, customer embeddings are learned from the customer-product graph, and product embeddings are learned from the product knowledge graph.

In Table [2,](#page-4-1) from the results of Methods 6 and 7, we can see that removing either product or customer embedding degrades the performance of the model. The result of Method 8 shows that embeddings jointly learned from the merged crosssource graph achieve better performance on our downstream task. We also observe that the ranking returned by the product search system is still an important feature as Method 6 shows.

<span id="page-4-0"></span>

|   | Method    | Dev Acc@1 | Test Acc@1 |
|---|-----------|-----------|------------|
| 1 | QUARTS    | 0.0       | 0.0        |
| 2 | Purchased | +10.5     | +8.5       |
| 3 | ComplEx   | +25.7     | +16.1      |
| 4 | Our Model | +32.9     | +24.6      |

Table 1: Relative gains compared to QUARTS. (%)

<span id="page-4-1"></span>

|   | Method                    | Dev Acc@1 | Test Acc@1 |
|---|---------------------------|-----------|------------|
| 4 | Our Model                 | +32.9     | +24.6      |
| 5 | w/o Ranking               | -17.1     | -20.4      |
| 6 | w/o Personalized Features | -10.5     | -18.0      |
| 7 | w/o Product Embedding     | +25.2     | +19.0      |
| 8 | w/o Joint Embedding       | +28.1     | +20.4      |

Table 2: Ablation study. (%, relative gains compared to QUARTS.)

### 3.4 Qualitative Analysis

In Table [3](#page-5-0) and Table [4,](#page-5-1) we show some positive and negative examples in the test set.

Table [4](#page-5-1) shows examples where our model fails to return the correct item. In many cases, such as Example #4, the purchased product and the top ranked one only differ in packaging size. We also observe that sometimes customers may not repurchase a product even if it is in the candidate list.

To better understand the remaining errors, we randomly sample 100 examples where our model fails to predict the purchased items. As Figure [3](#page-4-2)

<span id="page-4-2"></span>![](_page_4_Figure_12.jpeg)

Figure 3: Distribution of remaining Errors.

illustrates, we analyze these examples and classify the possible reasons into the following categories. Different size. The predicted product and ground truth are the same product but differ in size. For example, while our model predicts "Lipton Herbal Tea Bags, Peach Mango, 20 ct", the customer purchases another item "Lipton Tea Herbal Peach Mango (pack of 2)", which is actually the same product in 2 pack.

Purchased. The customer has purchased the predicted product but decides not to repurchase it. This usually happens in categories (e.g., toothpaste) where customers are more willing to try new products. Additionally, customers may be less likely to repurchase a product in some categories such as books and electronics.

Uninformative title. The purchased product has an uninformative title and is therefore not promoted. For example, when the customer searches for "masaman curry paste maesri", our model promotes "Maesri Thai Masaman Curry - 4 oz (pack of 4)", while the customer purchases "6 Can (4oz. Each) of Thai Green Red Yellow Curry Pastes Set", which is also a Maesri product, but this key information is missing from its title.

ff Similar title. The title of the predicted product is similar to the titles of some purchased products in the customer's history in a less important aspect. For example, the model promotes a "moisturizing" shave gel because the customer has purchased a "moisturizing" body wash, whereas the customer decides to purchase a product for "sensitive skin". Brand. The customer has purchased one or more products of the same brand.

Attribute. The customer has purchased one or more products with the same attribute (e.g., organic, keto, kosher).

Other. The model may fail to predict the purchased item in other uncategorized cases. For example, when a customer searches for "nail clippers" but has purchased only food in the past, the model

<span id="page-5-0"></span>

| Query                                                                                                                                                                                  | Candidates                                                                                                                | History                                                                                                       |  |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|--|
| #1 vitamin c<br>serum                                                                                                                                                                  | * [3] instanatural vitamin c serum with hyaluronic acid<br>& vit e - natural & organic anti wrinkle                       | * foundation makeup brush flat top kabuki for face -<br>perfect for blending liquid, cream or flawless powder |  |
|                                                                                                                                                                                        | * [1] truskin vitamin c serum for face, topical facial<br>serum with hyaluronic acid, vitamin e, 1 fl oz                  | * women's rogaine 5% minoxidil foam for hair thin<br>ning and loss, topical treatment for women's hair        |  |
|                                                                                                                                                                                        | * [2] vitamin c serum for face - anti aging facial serum                                                                  | * vita liberata advanced organics fabulous self-tanning<br>gradual lotion with marula oil, 6.76 fl oz         |  |
|                                                                                                                                                                                        | * [4] vitamin c serum plus 2% retinol, 3.5% niaci<br>namide, 5% hyaluronic acid, 2% salicylic acid                        | * instanatural vitamin c serum with hyaluronic acid &<br>vit e - natural & organic anti wrinkle reducer       |  |
|                                                                                                                                                                                        | Our model promotes candidate 3 as this product was purchased by the customer.                                             |                                                                                                               |  |
| #2 toothpaste                                                                                                                                                                          | * [2] crest 3d white whitening toothpaste, radiant mint,<br>3.5oz, twin pack                                              | * crest 3d white toothpaste radiant mint (3 count of 4.1<br>oz tubes), 12.3 oz packaging may vary             |  |
|                                                                                                                                                                                        | * [1] crest + scope complete whitening toothpaste,<br>minty fresh, 5.4 oz, pack of 3                                      | * skindinavia the makeup of countrol finishing spray,<br>8 fluid ounce                                        |  |
|                                                                                                                                                                                        | * [3] pronamel gentle whitening enamel toothpaste for<br>sensitive teeth, alpine breeze-4 ounces (pack of 3)              | * crest 3d white toothpaste radiant mint (3 count of 4.1<br>oz tubes), 12.3 oz packaging may vary             |  |
|                                                                                                                                                                                        | * [4] colgate cavity protection toothpaste with fluoride<br>- 6 ounce (pack of 6)                                         | * nivea shea daily mointure body lotion - 48 hour<br>moisture for dry skin - 16.9 fl. oz. pump bottle,        |  |
| Although the previously purchased item is no longer available, with entity embedding learned from the<br>cross-source graph, our model successfully promotes the most similar product. |                                                                                                                           |                                                                                                               |  |
| #3 sun dried<br>tomatoes                                                                                                                                                               | * [3] 365 everyday value, organic sundried tomatoes<br>in extra virgin olive oil, 8.5 oz                                  | * #1 usda organic aloe vera gel - no preservatives, no<br>alcohol - from freshly cut usa grown 100% pure      |  |
|                                                                                                                                                                                        | * [1] 35 oz bella sun luci sun dried tomatoes julienne<br>cut in olive oil (original version)                             | * organic aloe vera gel with 100% pure aloe from<br>freshly cut aloe plant, not powder - no xanthan           |  |
|                                                                                                                                                                                        | * [2] julienne sun-dried tomatoes - 16oz bag (kosher)                                                                     | * wicked joe organic coffee wicked italian ground                                                             |  |
|                                                                                                                                                                                        | * [4] organic sun-dried tomatoes with sea salt, 8<br>ounces - salted, non-gmo, kosher, raw, vegan,                        | *thayers alcohol-free original witch hazel facial toner<br>with aloe vera formula, clear, 12oz                |  |
|                                                                                                                                                                                        | Our model promotes an organic product as the customer probably prefers organic products based on the<br>shopping records. |                                                                                                               |  |

Table 3: Positive examples in the test set. Candidates are listed in the order returned by our method. The number before each candidate is the original ranking returned by QUARTS. In the candidate column, we highlight the purchased products . In the history column, we highlight related records .

<span id="page-5-1"></span>

| Query                                                                                                    | Candidates                                                                                                  | History                                                                                                   |
|----------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| #4 wasabi<br>almonds                                                                                     | * [8] blue diamond almonds, bold wasabi & soy sauce,<br>16 ounce (pack of 1)                                | * epsoak epsom salt 19 lb. bulk bag magnesium sulfate<br>usp                                              |
|                                                                                                          | * [2] blue diamond almonds variety pack (1.5 ounce<br>bags) (20 pack)                                       | * blue diamond almonds, bold wasabi & soy sauce, 16<br>ounce (pack of 1)                                  |
|                                                                                                          | * [1] blue diamond almonds bold wasabi & soy sauce<br>almonds, 25 ounce (pack of 1)                         | * signature trail mix, peanuts, m & m candies, raisins,<br>almonds & cashews, 4 lb                        |
|                                                                                                          | * [6] blue diamond almonds, bold wasabi & soy, 1.5<br>ounce (pack of 12)                                    | * amazon brand - happy belly nuts, chocolate & dried<br>fruit trail mix, 48 ounce                         |
| Our model promotes candidate 8 which is previously purchased, whereas the customer selects another size. |                                                                                                             |                                                                                                           |
| #5 cacao<br>powder                                                                                       | * [5] anthony's organic cocoa powder, 2 lb, batch<br>tested and verified gluten free & non gmo              | * anthony's organic cocoa powder, 2 lb, batch tested<br>and verified gluten free & non gmo                |
|                                                                                                          | * [1] viva naturals #1 best selling certified organic<br>cacao powder from superior criollo beans, 1 lb bag | * vör all natural keto nut butter spread (10oz)   only<br>two ingredients   no sugar, no salt   vegan     |
|                                                                                                          | * [2] navitas organics cacao powder, 16oz. bag - or<br>ganic, non-gmo, fair trade, gluten-free              | * anthony's organic cocoa powder, 2 lb, batch tested<br>and verified gluten free & non gmo                |
|                                                                                                          | * [3] terrasoul superfoods raw organic cacao powder,<br>1 lb - raw   keto   vegan                           | * nutiva organic, neutral tasting, steam refined coconut<br>oil from non-gmo, sustainably farmed coconuts |
|                                                                                                          | * [4] viva naturals certified organic cacao powder (2lb)<br>for smoothie, coffee and drink mixes            |                                                                                                           |
| Our model promote "Anthony's Organic Cocoa Powder" as it has been purchased twice by the customer.       |                                                                                                             |                                                                                                           |

Table 4: Negative examples in the test set.

is unlikely to utilize the history records to improve the ranking.

Although our framework can improve the accuracy of predicting products that will be purchased, there are still some remaining challenges.

Incorporating more informative features. Some important features that affect purchase decisions are still missing in our framework, such as the average rating, customer reviews, and number of ratings. For example, we may promote the highest rated product for a customer who usually buys products with high ratings.

Building a more comprehensive cross-source customer-product graph. In this work, we merge the customer-product graph and product knowledge graph into a single graph, which has been proved to produce better embeddings for our target task. A natural extension is to include records from more sources, such as music or video playing history, and multimedia features.

Modeling the interactions among purchase behaviors. Our current attention-based method that generates history representations is "flat" and ignores the relationship among purchase behaviors. For example, for a customer who previously purchases a pod coffee maker, we should promote coffee capsules in the candidates over coffee beans or grounds.

# 4 Related Work

# 4.1 Neural Entity Linking

A variety of neural models [\(Gupta et al.,](#page-7-9) [2017;](#page-7-9) [Kolitsas et al.,](#page-7-10) [2018;](#page-7-10) [Cao et al.,](#page-7-11) [2018;](#page-7-11) [Sil et al.,](#page-8-8) [2018;](#page-8-8) [Gillick et al.,](#page-7-12) [2019;](#page-7-12) [Logeswaran et al.,](#page-7-13) [2019;](#page-7-13) [Wu et al.,](#page-8-9) [2019;](#page-8-9) [Agarwal and Bikel,](#page-7-2) [2020\)](#page-7-2) have been applied to Entity Linking in recent years. Compared to traditional entity linking, our task is different in three aspects: (1) Our mentions are typically vague and occur in uninformative contexts, such as "add *toothpaste* to my cart" ; (2) A mention may be reasonably linked to multiple entities, while only one of them is considered "correct" (purchased by the customer); (3) The ground truth for the same mention can be different for different customers.

# 4.2 Personalized Recommendation

A recommender system is an information filtering system that aims to suggest a list of items in which a user may be interested. Content-based filtering [\(Billsus and Pazzani,](#page-7-14) [2000;](#page-7-14) [Aciar et al.,](#page-7-15)

[2007;](#page-7-15) [Wang et al.,](#page-8-10) [2018\)](#page-8-10) and collaborative filtering [\(Shardanand and Maes,](#page-8-11) [1995;](#page-8-11) [Konstan et al.,](#page-7-16) [1997;](#page-7-16) [Linden et al.,](#page-7-17) [2003;](#page-7-17) [Zhao and Shang,](#page-8-12) [2010\)](#page-8-12) are two common approaches used in recommender systems. In recent years, researchers have also applied neural methods to improve the quality of recommendations [\(Xue et al.,](#page-8-13) [2017;](#page-8-13) [He et al.,](#page-7-18) [2017;](#page-7-18) [Wang et al.,](#page-8-14) [2019a,](#page-8-14)[b\)](#page-8-15). Recommender systems usually rank items based on the user's past behaviors (e.g., purchasing, browsing, rating) and current context [\(Linden et al.,](#page-7-17) [2003;](#page-7-17) [Smith and Linden,](#page-8-16) [2017\)](#page-8-16), whereas the results are not constrained by queries. Instead, our task requires a specific query and only returns the product that is most likely to be purchased from a list of relevant candidates.

# 4.3 Graph Embedding

Various methods have been proposed to learn lowdimensional vectors for nodes in knowledge graphs. Knowledge graph embedding methods, such as TransE [\(Bordes et al.,](#page-7-19) [2013\)](#page-7-19), DistMult [\(Yang et al.,](#page-8-17) [2014\)](#page-8-17), ComplEx [\(Trouillon et al.,](#page-8-7) [2016\)](#page-8-7), and RotatE [\(Sun et al.,](#page-8-18) [2018\)](#page-8-18), typically represent the head entity, relation, and tail entity in each triplet in the knowledge graph as vectors and aim to rank true triplets higher than corresponding corrupted triplets. Matrix Factorization-based methods [\(He](#page-7-20) [and Niyogi,](#page-7-20) [2004;](#page-7-20) [Nickel et al.,](#page-7-21) [2011;](#page-7-21) [Qiu et al.,](#page-8-19) [2018\)](#page-8-19) represent the graph as a matrix and obtain node vectors by factorizing this matrix. Another category of frameworks [\(Perozzi et al.,](#page-7-22) [2014b;](#page-7-22) [Yang et al.,](#page-8-20) [2015;](#page-8-20) [Grover and Leskovec,](#page-7-7) [2016\)](#page-7-7) use random walk to sample paths from the input graph and learn node embeddings from the sampled paths using neural models such as SkipGram and LSTM.

# 5 Conclusion and Future Work

We propose a novel framework to jointly learn customer and product representations based on a crosssource heterogeneous graph constructed from customers' purchase history and the product knowledge graph to improve personalized entity resolution. Experiments show that our framework can effectively increase the purchase rate of top ranked products. In the future, we plan to investigate better approaches to integrating personalized features and extend the framework to cross-lingual cross-media settings and generate conversations for more proactive and explainable entity recommendation and summarization.

# References

- <span id="page-7-15"></span>Silvana Aciar, Debbie Zhang, Simeon Simoff, and John Debenham. 2007. Informed recommender: Basing recommendations on consumer product reviews. *IEEE Intelligent systems*, 22(3):39–47.
- <span id="page-7-2"></span>Oshin Agarwal and Daniel M Bikel. 2020. Entity linking via dual and cross-attention encoders. *arXiv preprint arXiv:2004.03555*.
- <span id="page-7-14"></span>Daniel Billsus and Michael J Pazzani. 2000. User modeling for adaptive news access. *User modeling and user-adapted interaction*, 10(2-3):147–180.
- <span id="page-7-19"></span>Antoine Bordes, Nicolas Usunier, Alberto Garcia-Duran, Jason Weston, and Oksana Yakhnenko. 2013. Translating embeddings for modeling multirelational data. *Advances in neural information processing systems*, 26:2787–2795.
- <span id="page-7-11"></span>Yixin Cao, Lei Hou, Juanzi Li, and Zhiyuan Liu. 2018. Neural collective entity linking. In *Proceedings of the 27th International Conference on Computational Linguistics*, pages 675–686.
- <span id="page-7-12"></span>Dan Gillick, Sayali Kulkarni, Larry Lansing, Alessandro Presta, Jason Baldridge, Eugene Ie, and Diego Garcia-Olano. 2019. Learning dense representations for entity retrieval. In *Proceedings of the 23rd Conference on Computational Natural Language Learning (CoNLL)*, pages 528–537.
- <span id="page-7-7"></span>Aditya Grover and Jure Leskovec. 2016. node2vec: Scalable feature learning for networks. In *Proceedings of the 22nd ACM SIGKDD international conference on Knowledge discovery and data mining*, pages 855–864.
- <span id="page-7-9"></span>Nitish Gupta, Sameer Singh, and Dan Roth. 2017. Entity linking via joint encoding of types, descriptions, and context. In *Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing*, pages 2681–2690.
- <span id="page-7-18"></span>Xiangnan He, Lizi Liao, Hanwang Zhang, Liqiang Nie, Xia Hu, and Tat-Seng Chua. 2017. Neural collaborative filtering. In *Proceedings of the 26th international conference on world wide web*, pages 173– 182.
- <span id="page-7-20"></span>Xiaofei He and Partha Niyogi. 2004. Locality preserving projections. In *Advances in neural information processing systems*, pages 153–160.
- <span id="page-7-0"></span>Heng Ji and Ralph Grishman. 2011. Knowledge base population: Successful approaches and challenges. In *Proc. ACL2011*.
- <span id="page-7-1"></span>Heng Ji, Joel Nothman, Ben Hachey, and Radu Florian. 2015. Overview of tac-kbp2015 tri-lingual entity discovery and linking. In *Proc. Text Analysis Conference (TAC2015)*.

- <span id="page-7-10"></span>Nikolaos Kolitsas, Octavian-Eugen Ganea, and Thomas Hofmann. 2018. End-to-end neural entity linking. In *Proceedings of the 22nd Conference on Computational Natural Language Learning*, pages 519–529.
- <span id="page-7-16"></span>Joseph A Konstan, Bradley N Miller, David Maltz, Jonathan L Herlocker, Lee R Gordon, and John Riedl. 1997. Grouplens: applying collaborative filtering to usenet news. *Communications of the ACM*, 40(3):77–87.
- <span id="page-7-17"></span>Greg Linden, Brent Smith, and Jeremy York. 2003. Amazon. com recommendations: Item-to-item collaborative filtering. *IEEE Internet computing*, 7(1):76–80.
- <span id="page-7-8"></span>Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. 2019. Roberta: A robustly optimized bert pretraining approach. *arXiv preprint arXiv:1907.11692*.
- <span id="page-7-13"></span>Lajanugen Logeswaran, Ming-Wei Chang, Kenton Lee, Kristina Toutanova, Jacob Devlin, and Honglak Lee. 2019. Zero-shot entity linking by reading entity descriptions. In *Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics*, pages 3449–3460.
- <span id="page-7-5"></span>Thanh Nguyen, Nikhil Rao, and Karthik Subbian. 2020. [Learning robust models for e-commerce product](https://doi.org/10.18653/v1/2020.acl-main.614) [search.](https://doi.org/10.18653/v1/2020.acl-main.614) In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, pages 6861–6869, Online. Association for Computational Linguistics.
- <span id="page-7-21"></span>Maximilian Nickel, Volker Tresp, and Hans-Peter Kriegel. 2011. A three-way model for collective learning on multi-relational data. In *Icml*, volume 11, pages 809–816.
- <span id="page-7-4"></span>Priyanka Nigam, Yiwei Song, Vijai Mohan, Vihan Lakshman, Weitian (Allen) Ding, Ankit Shingavi, Choon Hui Teo, Hao Gu, and Bing Yin. 2019. [Se](https://doi.org/10.1145/3292500.3330759)[mantic product search.](https://doi.org/10.1145/3292500.3330759) In *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining*, page 2876–2885, New York, NY, USA. Association for Computing Machinery.
- <span id="page-7-3"></span>Xiaoman Pan, Boliang Zhang, Jonathan May, Joel Nothman, Kevin Knight, and Heng Ji. 2017. Crosslingual name tagging and linking for 282 languages. In *Proc. the 55th Annual Meeting of the Association for Computational Linguistics (ACL2017)*.
- <span id="page-7-6"></span>Bryan Perozzi, Rami Al-Rfou, and S. Skiena. 2014a. Deepwalk: online learning of social representations. In *KDD '14*.
- <span id="page-7-22"></span>Bryan Perozzi, Rami Al-Rfou, and Steven Skiena. 2014b. Deepwalk: Online learning of social representations. In *Proceedings of the 20th ACM SIGKDD international conference on Knowledge discovery and data mining*, pages 701–710.

- <span id="page-8-2"></span>Daniel Preo¸tiuc-Pietro, Vasileios Lampos, and Nikolaos Aletras. 2015. An analysis of the user occupational class through twitter content. In *Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)*.
- <span id="page-8-19"></span>Jiezhong Qiu, Yuxiao Dong, Hao Ma, Jian Li, Kuansan Wang, and Jie Tang. 2018. Network embedding as matrix factorization: Unifying deepwalk, line, pte, and node2vec. In *Proceedings of the Eleventh ACM International Conference on Web Search and Data Mining*, pages 459–467.
- <span id="page-8-4"></span>M. H. Ribeiro, Pedro H. Calais, Yuri A. Santos, V. Almeida, and W. Meira. 2018. Characterizing and detecting hateful users on Twitter. In *Proceedings of the Twelfth International AAAI Conference on Web and Social Media (ICWSM 2018)*.
- <span id="page-8-6"></span>Michael Schlichtkrull, Thomas N Kipf, Peter Bloem, Rianne Van Den Berg, Ivan Titov, and Max Welling. 2018. Modeling relational data with graph convolutional networks. In *European Semantic Web Conference*, pages 593–607. Springer.
- <span id="page-8-11"></span>Upendra Shardanand and Pattie Maes. 1995. Social information filtering: algorithms for automating "word of mouth". In *Proceedings of the SIGCHI conference on Human factors in computing systems*, pages 210–217.
- <span id="page-8-8"></span>Avirup Sil, Gourab Kundu, Radu Florian, and Wael Hamza. 2018. Neural cross-lingual entity linking. In *Proceedings of the AAAI Conference on Artificial Intelligence*, volume 32.
- <span id="page-8-16"></span>Brent Smith and Greg Linden. 2017. Two decades of recommender systems at amazon.com. *Ieee internet computing*, 21(3):12–18.
- <span id="page-8-18"></span>Zhiqing Sun, Zhi-Hong Deng, Jian-Yun Nie, and Jian Tang. 2018. RotatE: Knowledge graph embedding by relational rotation in complex space. In *International Conference on Learning Representations*.
- <span id="page-8-7"></span>Théo Trouillon, Johannes Welbl, Sebastian Riedel, Éric Gaussier, and Guillaume Bouchard. 2016. Complex embeddings for simple link prediction. International Conference on Machine Learning (ICML).
- <span id="page-8-10"></span>Donghui Wang, Yanchun Liang, Dong Xu, Xiaoyue Feng, and Renchu Guan. 2018. A content-based recommender system for computer science publications. *Knowledge-Based Systems*, 157:1–9.
- <span id="page-8-1"></span>Han Wang, Jin Guang Zheng, Xiaogang Ma, Peter Fox, and Heng Ji. 2015. Language and domain independent entity linking with quantified collective validation. In *Proceedings of the 2015 Conference on Empirical Methods in Natural Language Processing*, pages 695–704.

- <span id="page-8-14"></span>Hongwei Wang, Fuzheng Zhang, Mengdi Zhang, Jure Leskovec, Miao Zhao, Wenjie Li, and Zhongyuan Wang. 2019a. [Knowledge-aware graph neural net](https://doi.org/10.1145/3292500.3330836)[works with label smoothness regularization for rec](https://doi.org/10.1145/3292500.3330836)[ommender systems.](https://doi.org/10.1145/3292500.3330836) In *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining*, KDD '19, page 968–977, New York, NY, USA. Association for Computing Machinery.
- <span id="page-8-15"></span>Hongwei Wang, Fuzheng Zhang, Miao Zhao, Wenjie Li, Xing Xie, and Minyi Guo. 2019b. Multi-task feature learning for knowledge graph enhanced recommendation. In *The World Wide Web Conference*, pages 2000–2010.
- <span id="page-8-9"></span>Ledell Wu, Fabio Petroni, Martin Josifoski, Sebastian Riedel, and Luke Zettlemoyer. 2019. Scalable zeroshot entity linking with dense entity retrieval. *arXiv preprint arXiv:1911.03814*.
- <span id="page-8-13"></span>Hong-Jian Xue, Xinyu Dai, Jianbing Zhang, Shujian Huang, and Jiajun Chen. 2017. Deep matrix factorization models for recommender systems. In *IJCAI*, volume 17, pages 3203–3209. Melbourne, Australia.
- <span id="page-8-17"></span>Bishan Yang, Wen-tau Yih, Xiaodong He, Jianfeng Gao, and Li Deng. 2014. Embedding entities and relations for learning and inference in knowledge bases. *arXiv preprint arXiv:1412.6575*.
- <span id="page-8-20"></span>Zhilin Yang, Jie Tang, and William Cohen. 2015. Multi-modal bayesian embeddings for learning social knowledge graphs. *arXiv preprint arXiv:1508.00715*.
- <span id="page-8-3"></span>Yang Yu, Xiaojun Wan, and Xinjie Zhou. 2016. User embedding for scholarly microblog recommendation. In *Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)*.
- <span id="page-8-0"></span>Boliang Zhang, Ying Lin, Xiaoman Pan, Di Lu, Jonathan May, Kevin Knight, and Heng Ji. 2018a. ELISA-EDL: A cross-lingual entity extraction, linking and localization system. In *Proc. The 16th Annual Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT2018)*.
- <span id="page-8-5"></span>Zhen Zhang, Hongxia Yang, Jiajun Bu, Sheng Zhou, Pinggang Yu, Jianwei Zhang, Martin Ester, and Can Wang. 2018b. Anrl: Attributed network representation learning via deep neural networks. In *IJCAI*, volume 18.
- <span id="page-8-12"></span>Zhi-Dan Zhao and Ming-Sheng Shang. 2010. Userbased collaborative-filtering recommendation algorithms on hadoop. In *2010 Third International Conference on Knowledge Discovery and Data Mining*, pages 478–481. IEEE.