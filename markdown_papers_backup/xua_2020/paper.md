---
cite_key: xua_2020
title: AI-CTO: Knowledge graph for automated and dependable software stack solution
authors: Xiaoyun Xua, Jingzheng Wua, Mutian Yanga, Tianyue Luoa, Qianru Mengd, Yanjun Wua, Beijing Baidux
year: 2020
date_processed: '2025-07-02'
phase2_processed: true
original_folder: xu2020
images_total: 10
images_kept: 10
images_removed: 0
tags:
- Knowledge Graph
- Machine Learning
- Semantic Web
keywords:
- ai-cto
- error-prone
- graph embedding
- graph-embedding-based
- knowledge graph
- low-dimensional
- time-consuming
---

# AI-CTO: Knowledge graph for automated and dependable software stack solution

- Xiaoyun Xua, Jingzheng Wua*,*b*,*<sup>∗</sup>, Mutian Yanga*,*<sup>c</sup> , Tianyue Luoa*,*<sup>c</sup> , Qianru Mengd, Weiheng Lia 3
- and Yanjun Wua*,*<sup>b</sup> 4

- <sup>a</sup> <sup>5</sup> *Institute of Software, Chinese Academy of Sciences, China*- <sup>b</sup> <sup>6</sup>*State Key Laboratory of Computer Science, Institute of Software, Chinese Academy of Sciences, China*- <sup>c</sup> <sup>7</sup>*Beijing ZhongKeWeiLan Technology Co., Ltd, China*- <sup>d</sup> <sup>8</sup>*Beijing Baidu, Inc, China*Uncorrected Author Proof**Abstract**. As the scale of software systems continues expanding, software architecture is receiving more and more attention as the blueprint for the complex software system. An outstanding architecture requires a lot of professional experience and expertise. In current practice, architects try to find solutions manually, which is time-consuming and error-prone because of the knowledge barrier between newcomers and experienced architects. The problem can be solved by easing the process of apply experience from prominent architects. To this end, this paper proposes a novel graph-embedding-based method, AI-CTO, to automatically suggest software stack solutions according to the knowledge and experience of prominent architects. Firstly, AI-CTO converts existing industry experience to knowledge, i.e., knowledge graph. Secondly, the knowledge graph is embedded in a low-dimensional vector space. Then, the entity vectors are used to predict valuable software stack solutions by an SVM model. We evaluate AI-CTO with two case studies and compare its solutions with the software stacks of large companies. The experiment results show that AI-CTO can find effective and correct stack solutions and it outperforms other baseline methods. 9 10 11 12 13 14 15 16 17 18 19

<sup>20</sup> Keywords: Knowledge graph, graph embedding, software architecture

## <sup>21</sup> 1. Introduction

As the scale of software systems continues expand- ing, software architecture is receiving more and more attention as the blueprint for the complex soft- ware system. Software architecture establishes the link between requirements and implementation [1] and allows designers to infer the ability to meet requirements at the design phase. This field has been developing for more than 30 years and plays an important and ubiquitous role in contemporary indus- trial practice [2]. The quality of the system depends heavily on its design, i.e. architecture. According to a research report from the National Institute of Standards and Technology (NIST), more than 70% <sup>34</sup> of errors found in software testing are caused by <sup>35</sup> requirement acquisition or architecture design [3]. <sup>36</sup> The longer the errors exist in the system, the harder it <sup>37</sup> will be to find them, and the higher the cost of solv- <sup>38</sup> ing them. In summary, a good architecture makes the <sup>39</sup> software system more robust and reliable. <sup>40</sup>

Software architecture can be divided into two lev- <sup>41</sup> els: architecture and design, but it is difficult to <sup>42</sup> clearly distinguish the boundary of them [4]. There- <sup>43</sup> fore, in this paper, the "architecture" is considered <sup>44</sup> to be elements of architectural styles. For exam- <sup>45</sup> ple, there are two basic elements of client-server <sup>46</sup> architectural style, the "client" and "server". Com- <sup>47</sup> mon architectural styles include pipes and filters, <sup>48</sup> data abstraction and object-oriented organisation, <sup>49</sup> event-based implicit invocation, abstract data types <sup>50</sup>



<sup>∗</sup>Corresponding author. Jingzheng Wu, E-mail: [jingzheng08@](mailto:jingzheng08@{penalty -@M }iscas.ac.cn) iscas.ac.cn.

or objects, layered system, business cycle, client- server model, etc [5]. The "design" is considered to be the process of choosing a development software for each element of architectural styles. For exam- ple, MySQL is software for the database element of an architectural style. However, due to the complex relationship between architectural style and software performance, it is difficult for architects to choose an appropriate style and design each component manu-<sup>60</sup> ally.

Motived by the above problem and challenge, this paper proposes a novel method, AI-CTO, to suggest software stack solutions. AI-CTO consists of three stages: Establishment of software knowledge graph; Embedding of the knowledge graph; Deriving of soft- ware stack solutions. The basic idea is extracting knowledge from a well-designed software graph to facilitate architecture tasks. As the relations among software entities can be reasonably represented by the knowledge graph, we firstly build the five-layer soft- ware graph: (1)Software system layer; (2) Software stack layer; (3) Software category layer; (4) Software label layer; (5) Software framework layer. These lay- ers represent the different type of entities in the graph, such as software and requirement labels. In addition, the company entities are not in these layers, because they are not elements of software stacks.

For automated analysis of the architectural prob- lem, we intend to embed the entities in the software graph into a low-dimensional vector space. However, most of the previous researches about graph embed- ding just learned from structural triples [6–8], while there is rich semantic information that reflects fea- tures of the software, such as descriptions and names. Therefore, we propose a novel embedding method to combine the two kinds of information in the graph, i.e., structure information and description informa- tion. Our method takes the results of node2vec [8] as structure information and the embedding of software description text as description information.

To derive the software stack solutions accord- ing to the requirements of architects, we propose a requirement-based-walk method to select a set of stack solutions, which satisfy the requirements. These preliminary stack solutions are further filtered by a Support Vector Machine (SVM) model. The feature vector of each stack is calculated by the embedding results. The SVM model is trained by the stack solu-tions of large companies.

<sup>100</sup> According to the above ideas, we build the proto-<sup>101</sup> type of AI-CTO. The software graph contains 11876 <sup>102</sup> entities and 43269 relations, including 3175 software entities and 350 company entities. We set four base- <sup>103</sup> lines on two experiments to evaluate the correctness <sup>104</sup> and usage of AI-CTO. For the correctness exper- <sup>105</sup> iment, the results of AI-CTO are verified by real <sup>106</sup> software stacks. For the usage experiment, this exper- <sup>107</sup> iment counts the companies using the same stacks as <sup>108</sup> AI-CTO results. The results show that AI-CTO out- <sup>109</sup> performs other baselines and can suggest satisfactory <sup>110</sup> software stacks. <sup>111</sup>

In summary, we make the following contributions <sup>112</sup> in this paper: <sup>113</sup>

- − We introduce the concept of knowledge graph <sup>114</sup> to formally represent software entities and <sup>115</sup> requirements of architects, which converts <sup>116</sup> development experience to knowledge and <sup>117</sup> narrows the knowledge barrier between new- <sup>118</sup> comers and experienced architects. <sup>119</sup>
- − We implement the prototype of AI-CTO to <sup>120</sup> extract effective software stack solutions from <sup>121</sup> the software knowledge graph. The method <sup>122</sup> makes full use of both the semantic information <sup>123</sup> of software descriptions and graph structure <sup>124</sup> information. The software stack solutions are <sup>125</sup> further filtered by an SVM model. <sup>126</sup>
- − We present an extensive evaluation of AI-CTO. <sup>127</sup> The experiment results show that AI-CTO out- <sup>128</sup> performs other baseline methods. <sup>129</sup>

Uncorrected Author Proof The rest of this paper is organised as follows. In <sup>130</sup> Section 2, we discuss the background information <sup>131</sup> needed to have a primary impression of the technolo- <sup>132</sup> gies used in our method. Section 3 details the software <sup>133</sup> stack solution method. The method is analysed and <sup>134</sup> evaluated in Section 4. Section 5 reports factors that <sup>135</sup> may affect experiment results. Section 6 discusses the <sup>136</sup> related work of our work. Finally, we summary this <sup>137</sup> paper in Section 7. <sup>138</sup>

### 2. Background <sup>139</sup>

This section discusses motivation, formalisation of <sup>140</sup> the problem in the selection space and notions about <sup>141</sup> knowledge graph. <sup>142</sup>

### *2.1. Motivation*<sup>143</sup>

There is a phenomenon of inadequate utilisation of <sup>144</sup> existing knowledge and experience. Newcomers pos- <sup>145</sup> sess limited knowledge and experience [9, 10]. It is <sup>146</sup> difficult for them to choose an appropriate style and <sup>147</sup> design each component manually. In fact, according <sup>148</sup>

to the experience of our industrial partners, devel- ops tend to choose the technologies they are familiar with, which makes it harder for them to learn from experienced architects.

In addition, the knowledge and experience of archi- tects are full of entities and relations, such as software, companies and dependencies among them, which is very similar to the concept of the knowledge graph. To facilitate the analysis in form of vectors, the graph is embedded into a continuous low-dimensional vector <sup>159</sup> space.

The embedding process takes account of two kinds of features. The graph structure features reflect the space characteristic while the description features reflect the semantic information. Therefore, an SVM model is used to find the boundary of that.

### <sup>165</sup>*2.2. Problem definition*This problem can be explain by defining a selection space. Let*a*be a vector having elements*ai*in an architectural style, and*ai*corresponds to the design selections. The architectural vector*a*has*n*dimension. Let*d*be a Boolean vector having elements*dj*as each design selection, i.e.,*ai* = {*d*}. The design vector *d*has*m*dimension. A design element*dj*can be defined as either*dj*= 0 (do not choose it), or*dj*= 1 (choose it):

$$
|\Omega_{selection}| = \prod_{i=1}^{n} \{0, 1\}^{m_i} \tag{1}
$$

The task for architects is choosing an option from the selection space. For example, the architecture of a simple web application usually consists of web server, client and database, i.e., the*a*has three elements. According to a technology stack website<sup>1</sup> <sup>170</sup> , the number of common development tools for web server, client and database are 25, 40 and 58, i.e.,*m*<sup>1</sup> = 25*, m*<sup>2</sup> = 40*, m*<sup>3</sup> = 58. There is a total selec- tion space of *m*<sup>1</sup> ∗ *m*<sup>2</sup> ∗ *m*3(58000) options to select among, which is a large number for human develop- ers. As the full-stack tools, such as NodeJS, are not included in the example, the upper-bound of selection space is much higher in real-world situations.

## <sup>179</sup> *2.3. Knowledge graph in software engineering*

<sup>180</sup> The knowledge graph efficiently stores objective <sup>181</sup> knowledge in form of triples. Each triple contains two entities and the relation between them. For example, <sup>182</sup> triple (*h, r, t*) contains a head node *h*, a relation *r*and a <sup>183</sup> tail node*t*. This kind of knowledge representation can <sup>184</sup> preferably reflect the relation information between <sup>185</sup> entities and it is useful for various domains [11]. With <sup>186</sup> the advancement of knowledge graph technologies in <sup>187</sup> recent years, some changes have taken place in this <sup>188</sup> field. One of them is that more and more researches <sup>189</sup> have shifted from a general-purpose knowledge graph <sup>190</sup> (GKG) to domain-specific knowledge graph (DKG). <sup>191</sup> GKG is built with general objective knowledge and <sup>192</sup> on a large scale, such as Google's Knowledge Graph <sup>193</sup> [12], NELL [13] and WikiData [14]. As one of <sup>194</sup> the most important features of GKG is the large <sup>195</sup> scale, automatic Information Acquisition technolo- <sup>196</sup> gies become a widely research topic [15–17]. <sup>197</sup>

Uncorrected Author Proof DKG refers to knowledge graphs that are focused <sup>198</sup> on a specific field, such as software engineering. Soft- <sup>199</sup> ware knowledge graph contains not only software <sup>200</sup> but also related entities such as developers, logs and <sup>201</sup> documentation. For example, IntelliDE [18]imple- <sup>202</sup> ment the function of software text semantic search <sup>203</sup> based on a software knowledge graph, which con- <sup>204</sup> sists of information from source code files, version <sup>205</sup> control systems, mailing lists, issue tracking systems, <sup>206</sup> Microsoft Office and PDF documents, HTML-format <sup>207</sup> tutorials, API documentation, user forum posts, blogs <sup>208</sup> and online social question-answering pairs. <sup>209</sup>

The software knowledge graph can be used to <sup>210</sup> solve different issues in software engineering, such <sup>211</sup> as design and analysis of functional requirements <sup>212</sup> [19], maintenance and testing of software [20] and <sup>213</sup> documentation for coding support [21]. <sup>214</sup>

## 3. Proposed approach <sup>215</sup>

Figure 2 demonstrates the overview architecture of <sup>216</sup> the proposed approach, which contains three main <sup>217</sup> stages. <sup>218</sup>

The preprocessing stage converts raw data to the <sup>219</sup> knowledge graph. The graph construction process <sup>220</sup> extracts entities and relations from raw data to build <sup>221</sup> a structured software knowledge graph. The raw data <sup>222</sup> comes from online sources and consists of software <sup>223</sup> tools, companies, software labels, etc, which is mas- <sup>224</sup> sive and disordered. Therefore, the data needs to be <sup>225</sup> cleaned in the data storage process. In addition, the <sup>226</sup> output of the graph construction process is stored into <sup>227</sup> the graph database in this process. <sup>228</sup>

In the embedding stage, the software knowledge <sup>229</sup> graph is projected into a continuous low-dimensional <sup>230</sup>

<sup>1</sup><https://stackshare.io/stacks>

![](_page_3_Figure_1.jpeg)
<!-- Image Description: This layered graph illustrates a web application's architecture. The leftmost yellow circle represents the web application, branching into layers of architecture (brown), categories (green), labels (blue), and frameworks (pink). Each layer shows specific components. Finally, the rightmost red circles represent applications (Airbnb, Netflix, Spotify) built using this architecture, highlighting dependencies across layers. The image visually depicts the system's structure and component relationships. -->

Figure 1. The layout example of the software knowledge graph.

![](_page_3_Figure_3.jpeg)
<!-- Image Description: Figure 1 shows a software knowledge graph layout example, illustrating relationships between software components (e.g., Web Application, DevOps, Netflix). Figure 2 depicts a three-stage method: preprocessing (graph construction and data storage), embedding (structure-based and description encoding, visualized with a matrix of vector values), and stacking (requirement-based walk and result filtering). The figures together illustrate the architecture for constructing and using a software knowledge graph to recommend software stacks. -->

Figure 2. The overview architecture of Our method: (1) The preprocessing stage consists of two processes, graph construction, and data storage; (2) The Embedding stage consists of two processes, structural based embedding, and description encoder; (3) The stacking stage consists of two processes, requirement based walk, and result filtering.

vector space. There are two kinds of information that can be used to realise the embedding, graph structure information and auxiliary information of entities. The structure based embedding process projects entities into vector space based on graph structure informa- tion. The description encoder process encodes the description of entities to vectors with the same dimen- sion based on auxiliary information. The two kinds of the vector are combined to represent the entity in the software knowledge graph.

The stacking stage constructs software stack solu- tions. The requirement based walk process walks in the graph to select a primary stack according to user requirements. The result filtering process improves the primary stack according to entity vectors.

### <sup>246</sup> *3.1. Preprocessing*#### <sup>247</sup>*3.1.1. Graph construction*<sup>248</sup> One of our central hypotheses is that the technol-<sup>249</sup> ogy stacks used by famous companies are efficient and adaptable. Therefore, we crawl technology stack <sup>250</sup> data as elementary knowledge from stackshare2. The <sup>251</sup> problem is that the raw data consists of many pieces of <sup>252</sup> separate data. The software knowledge graph of this <sup>253</sup> paper extracts structured software knowledge from <sup>254</sup> raw data according to the following rules: (1) A node <sup>255</sup> in the graph represents a software knowledge entity; <sup>256</sup> (2) A directed edge represents a relation; (3) Each <sup>257</sup> software entity corresponds to a unique identifies. <sup>258</sup>

Although the graph data is generated by the rela- <sup>259</sup> tion between entities, it still needs a cleverly designed <sup>260</sup> structure to be represented. The extracted entities and <sup>261</sup> relations are constructed into five layers, as shown in <sup>262</sup> Figure 1. Each layer is created for a kind of entities. <sup>263</sup> In particular, the label layer reflects the requirements <sup>264</sup> of users, so a stack walks through the label can be <sup>265</sup> thought as that the stack satisfy the requirement. <sup>266</sup>

The software system layer contains the target sys- <sup>267</sup> tem or application which we want to build stack <sup>268</sup> for, such as a Web application. Following paragraphs <sup>269</sup> <sup>270</sup> describe the structure and features of the rest of the <sup>271</sup> layers.

The software stack layer consists of four entities, "Application&Data", "Utility", "Devops" and "Busi- ness tools". The four architecture items are used to organise a large number of software categories.

The software category layer consists of various cat- egories of basic software items, such as databases, cloud hosting and full-stack frameworks. The soft- ware stack is built according to different categories in this layer. For example, a Web application basi- cally contains front-end framework, Web server and database. The stack for a Web application chooses one element from each of these three categories.

The software label layer consists of the func- tion and performance labels, which are used to reflect the characteristic of elementary software items. Those labels are used to represent the require- ments of users. For example, developers tend to use high-performance tools, such as NodeJS. The "high- performance" is a performance label of NodeJS, and it represents the requirement of developers on perfor- mance. As the category layer and software framework layer is connected with the label layer, it is able to select a software that satisfies the multiple require-ments by walking in the graph.

The software framework layer consists of elemen- tary software items, such as NodeJS, JavaScript and Python. In particular, software items used by famous companies connect to the corresponding company entities. This makes the stack used by famous com- panies different from others in embedded data so that our method can learn the technology features of famous companies.

## <sup>304</sup>*3.1.2. Data storage*The output data of the graph construction process is imported into the graph database for succeeding tasks. According to features of the graph, we first build entities in the graph database and then associate them with relations. However, there are too many query operations with this method and it is ineffi- cient. We optimised the operation of importing. When building entities, a part of the entities that have known relations are directly constructed into triples, thus reducing the query operations when building rela- tions later. In addition, the software label data from stackshare is submitted by tool users, i.e. it is crowd- sourcing data. Not all labels in the data are valid, some of them are lack of support by developers. The top 60% of the labels are reserved.

### *3.2. Embedding* <sup>319</sup>

The basic idea of our method is analysing software in a continuous low-dimensional space instead of doing that with the symbolic representation of triples. As shown in Equation 2, we proposed a new embedding method by combining two methods to embed entities into the vector space, i.e. structure based embedding (*Es*) and description encoder (*Ed*). The two methods simultaneously project entities into the same vector space, i.e., the dimensions of output are the same.

$$
E = E_s + E_d \tag{2}
$$

### *3.2.1. Structure based embedding*<sup>320</sup>

Uncorrected Author Proof Due to the classical triple structure, the knowledge <sup>321</sup> graph can efficiently provide graph structure informa- <sup>322</sup> tion. According to the Skip-gram model [22], words <sup>323</sup> with similar meanings tend to appear in a similar <sup>324</sup> context. Similarly, an embedding vector of a node <sup>325</sup> is decided by its neighbourhoods. The embedding <sup>326</sup> normally consists of two steps, graph information <sup>327</sup> sampling and vector learning. The first step samples <sup>328</sup> the adjacent nodes by a biased random walk algo- <sup>329</sup> rithm. The second step learns the feature vectors of <sup>330</sup> nodes by the Skip-gram model. This process is imple- <sup>331</sup> mented based on node2vec [8]. The biased random <sup>332</sup> walk is to select representative nodes according to <sup>333</sup> different search strategies, such as the breadth-first <sup>334</sup> search (BFS) and the depth-first search (DFS). BFS <sup>335</sup> focuses on neighbouring nodes and characterises a <sup>336</sup> relatively local network representation. DFS reflects <sup>337</sup> the homogeneity between nodes at a higher level. <sup>338</sup> BFS can explore the structural properties of the graph, <sup>339</sup> while DFS can explore the similarity in content (sim- <sup>340</sup> ilarity between connected nodes). Nodes with similar <sup>341</sup> structures do not have to be connected, and may even <sup>342</sup> be far apart. <sup>343</sup>

The problem is that node2vec does not distinguish <sup>344</sup> the categories of different nodes in the graph, we <sup>345</sup> avoid this problem by embedding the "category" in <sup>346</sup> the vector space as well. <sup>347</sup>

### *3.2.2. Description encoder*<sup>348</sup>

For each software entity, there is a short description <sup>349</sup> that reflects the features and functions of the entity. <sup>350</sup> For example, Figure 4 is the description of NodeJS. <sup>351</sup> The description encoder is built based on the hypoth- <sup>352</sup> esis that the keywords in the description are able to <sup>353</sup> summarise the main features of an entity. The embed- <sup>354</sup>

![](_page_5_Figure_1.jpeg)
<!-- Image Description: The image illustrates entity name embedding. A diagram shows "Python" (yellow box) at the top, connected to four green boxes labeled K1-K4. K1-K4 represent keywords ("Programming," "language," "general," "purpose") associated with Python. The diagram visually depicts how an entity name ("Python") is represented by related keywords in an embedding model. Ellipses (...) indicate further keywords. -->

Figure 3. The keywords of a short description for an entity. The different distance between keywords and entity name will result in different weights for each keywords.

![](_page_5_Figure_3.jpeg)
<!-- Image Description: The image is a box with a dashed border containing a green hexagonal Node.js logo and a textual description. The text explains that Node.js employs an event-driven, non-blocking I/O model, resulting in lightweight and efficient performance, particularly suitable for real-time, data-intensive applications distributed across multiple devices. The image serves to introduce Node.js and highlight its key architectural feature. -->

Figure 4. The description of NodeJs.

ding of each keyword is calculated by word2vec [22] model, which is trained on Wikipedia and all of the software descriptions. However, the keywords in a description should not be treated equally. Some key- words, such as the category of the entity, preferably represents the meaning of a description. For example, in the description of "Python is a general-purpose pro- gramming language created by Guido Van Rossum.", the word "programming" is more important than "purpose". Figure 3 shows the relation between the entity and the keywords. The keywords are ranked by distances.

> To capture this feature, we take the embedding of entity name as an anchor point. The words closer to entity name have more weight. The description embedding of a entity is calculated by following equations:

$$
d_i = \prod_j^n \sqrt{(p_j - q_j)^2}
$$
(3)

$$
w_i = f_g(d_i) \tag{4}
$$

$$
E_d = \sum_{i=1}^{k} e_i* w_i \tag{5}
$$

where *di*<sup>367</sup> is the euclidean distance between the entity <sup>368</sup> and the*ith*keyword.*fg*is a function for calculating

![](_page_5_Figure_12.jpeg)
<!-- Image Description: Figure 5 is a line graph depicting two Gaussian functions. The x-axis represents the input value, and the y-axis represents the function's value (weight). The graph shows how the function's shape changes with different parameter values (c=1 and c=2, with a=1 and b=0 held constant). The graph illustrates the effect of parameter 'c' on the Gaussian function's spread. -->

weights.*ei*is the embedding of the*ith*keyword.*Ed*<sup>369</sup> is the description embedding of the entity, i.e., the <sup>370</sup> vectors of top k keywords are sum up to be the vector <sup>371</sup> of the entity. <sup>372</sup>

Uncorrected Author Proof Inspired by the work of [23], this paper calculates the weights of keywords by Gauss Function, i.e., the weights increase with the decreasing distances between keywords and entity. As shown in Figure 5, the results of Gauss Function are smooth and the range can be adjusted by the three parameters. Equation 6 shows the definition of Gauss Function, where*a, b*and*c*denote some real constants and decide the range of the weight. The*x*is the distance between a keyword and an entity,*f* (*x*) is the weight of the keyword corresponding to the entity. In this paper, the *a* value is always set to 1, so that the weight is ranged from 0 to 1. There is a maximum value when |*x*−*b*| = 0. The *b*value is always set to 0 so that the distance equals 0 when the maximum weight is obtained (distance is positive). The*c*value is the standard deviation and controls the "width" of the function. It is adjusted according to the maximum of distances for each entity.

$$
f(x) = ae^{-\frac{(x-b)^2}{2c^2}}
$$
(6)

### *3.3. Stacking*<sup>373</sup>

### *3.3.1. Requirement based walk*<sup>374</sup>

The requirement based walk is proposed to find out <sup>375</sup> which category of software is needed by the architec- <sup>376</sup> ture. The basic idea is that popular categories are what <sup>377</sup> develops need. For example, the "Web Servers" cat- <sup>378</sup> egory is used by 3442 companies in our data and the <sup>379</sup>

"Graphic Design" category is used by 31 companies. Therefore, the "Web Servers" is considered as a cat- egory in the stack, while the "Graphic Design" may <sup>383</sup> not.

Another key is to reflect the requirements of devel- opers. As mentioned in section Graph Construction, there is a software label layer in the knowledge graph, which consists of the function and performance labels. In this paper, those labels are considered as software requirements. However, there are too many labels in the graph, i.e. 7800 labels. It is meaningless to integrate all of the labels in the method. We set a threshold to filter out unimportant labels according to their weights. The weight of a label is calculated according to the number of people who agree it on the stackshare website. Software tools that satisfy the labels are selected to be the preliminary software stack. However, the number of tools in the prelimi- nary data is too large, which will be further filtered by a result filtering process. It is not better to directly select popular software or combination of popular software, but popular is just an important factor. It is also necessary to consider the relationship between software and company, software and software. The knowledge graph is to better reflect this relevance.

### <sup>405</sup>*3.3.2. Result filtering*The results of requirement based walk process is selected by requirement labels, but it can be further filtered according to relevance among software, com- panies, labels etc. According to the idea of embedding method, the vectors of popular software and less used software will be located in different areas in the vec- tor space. In addition, the software in a stack used by companies will be further closer. Therefore, con- sidering the small amount of data and improving generalisation performance, we implement an SVM classifier to find the boundary between good stacks and useless stacks. SVM does not need to rely on the whole data, it is important to find the support vector.

> The classifier finds a hyperplane*W*that separates two kinds of "points" with maximum margin. In this paper, the "points" are software stacks, which are classified valuable stack and worthless stacks. However, a software stack consists of multiple entities, each entity is represented as a vector. We simply use the average vector of all the entities in the stack to train the SVM classifier. The loss function is:

$$
L_i = \sum_{i \neq y_i} max(0, s_i - s_{y_i} + \triangle)
$$
(7)

Table 1 The statistics of the software knowledge graph

| System | Stack | Category | Label | Framework | Company |
|--------|-------|----------|-------|-----------|---------|
| 1 | 4 | 546 | 7800 | 3175 | 350 |
| | | | | | |

$$
s_i = Wx_i \tag{8}
$$

The*si*is the score of corresponding sample*xi*. The <sup>419</sup> *W*is a weight matrix which represent the hyperplane. <sup>420</sup>

### 4. Evaluation <sup>421</sup>

The AI-CTO method is evaluated with real data <sup>422</sup> from a famous technology exchange community<sup>3</sup> to <sup>423</sup> answer the following research questions (RQs): <sup>424</sup>

## RQ 1: Does AI-CTO find effective results? <sup>425</sup>

**RQ 2: Does AI-CTO solutions use by enough**<sup>426</sup>**real users?**<sup>427</sup>

RQ 1 and RQ 2 examine the effectiveness of AI- <sup>428</sup> CTO. <sup>429</sup>

## *4.1. Dataset*<sup>430</sup>

Uncorrected Author Proof We evaluate our method on real-world data from <sup>431</sup> stackshare. Stackshare provides data about how <sup>432</sup> famous companies build a software system. For <sup>433</sup> example, there are 35 tools used by Facebook. Table <sup>434</sup> 2 lists 10 of them. The problem is that the items in the <sup>435</sup> data are discrete. Therefore, the data is converted to <sup>436</sup> a software knowledge graph, which contains 11876 <sup>437</sup> entities and 43269 relations. In particular, the statis- <sup>438</sup> tics of the knowledge graph are listed in Table 1, and <sup>439</sup> each item corresponds to the five layers of the graph. <sup>440</sup>

A graph database is used to facilitate the query and <sup>441</sup> storage in this experiment. The top five databases of <sup>442</sup> DB-Engines Ranking<sup>4</sup> are Neo4j, Microsoft Azure <sup>443</sup> Cosmos DB, ArangoDB, OrientDB and Virtuoso. <sup>444</sup> Considering the storage model, query language and <sup>445</sup> other factors, Neo4j is chosen as a data storage tool <sup>446</sup> in our method. Neo4j natively supports the Property <sup>447</sup> Graph Model and has full ACID (Atomicity, Consis- <sup>448</sup> tency, Isolation and Durability) properties. <sup>449</sup>

### *4.2. Baseline methods*<sup>450</sup>

To have an intuitive analysis of embedding results, <sup>451</sup> Principal component analysis (PCA) algorithm is <sup>452</sup> used to project vectors to 2-D, so that the embedding <sup>453</sup>

<sup>3</sup><https://stackshare.io/stacks>

<sup>4</sup><https://db-engines.com/en/ranking/graph+dbms>

| Software tool | Category | | |
|---------------|-------------------------|--|--|
| PHP | Languages | | |
| React | Javascript UI Libraries | | |
| GraphQL | Query Languages | | |
| Memcached | Databases | | |
| Cassandra | Databases | | |
| Flux | Javascript UI Librarie | | |
| Tornado | Frameworks (Full Stack) | | |
| HHVM | Virtual Machine | | |
| Relay | Javascript UI Libraries | | |
| Yoga | Javascript UI Libraries | | |

Table 2 Technology Stack of Facebook

![](_page_7_Figure_3.jpeg)
<!-- Image Description: This scatter plot displays a 2D representation of data points categorized into four groups: Software (red plus signs), Property (yellow diamonds), Company (blue circles), and Python (purple stars). The X and Y axes represent unspecified variables. The plot likely illustrates the results of a dimensionality reduction or clustering technique, showing the relationships and separation between different data categories in the paper's context. -->

Figure 6. The embedding results of "python" and related nodes, which are projected to 2d by PCA algorithm. The pink start is the "python" node.

can be visualised. Figure 6 is the 2-D projections of 128- D embeddings of the "python" and related nodes. The pink start is the "python" node. PCA was invented by Karl Pearson [24] in 1901, which is used to analyse the problem about how to retain more information while reducing the dimension of data. The method is mainly used to decompose the covariance matrix to obtain the principal components (i.e., eigenvectors) of the data and their weights (i.e., eigenvalue). The largest eigenvalue means that the largest variance is in the direction of corresponding eigenvector.

The baselines are implemented to compare with AI-CTO from two points of view. One is the feature used in AI-CTO, i.e., the graph structure feature and the description feature. Another is the method used to form a stack. It is clear from Figure 6 that nodes with high correlation will be closer to each other. There- fore, the basic idea for baselines to form a stack is calculating the distance between software in a stack.

![](_page_7_Figure_7.jpeg)
<!-- Image Description: The image illustrates a node embedding process. A graph (left) is inputted into the `node2vec` algorithm. This generates a matrix of numerical vectors (center), representing each node. These vectors are then used to produce "Closer Results" (right), likely indicating improved similarity comparisons between nodes based on their vector embeddings. The diagram shows the workflow, not the internal workings of `node2vec`. -->

Figure 7. Baseline One: the node2vec results and distance calculation.

![](_page_7_Figure_9.jpeg)
<!-- Image Description: The image illustrates a text processing pipeline. Input text ("GNU Emacs is an extensible, customizable text...") is fed into a "word2vec" model, which outputs a vector representation (a 3x3 matrix of numerical values shown). This vector is then processed, leading to "Closer Results," suggesting improved results after applying the word2vec model. The diagram visually depicts the workflow and transformation of the input text into a numerical representation for further analysis. -->

Figure 8. Baseline Two: the word2vec results and distance calculation.

### *4.2.1. Baseline one*<sup>473</sup>

The baseline one extracts graph structure informa- <sup>474</sup> tion to represent nodes in the software knowledge <sup>475</sup> graph. The basic idea of this model is that the closer <sup>476</sup> the two nodes are, the more relevant they are. Rele- <sup>477</sup> vant nodes are considered as good combination for <sup>478</sup> software development. <sup>479</sup>

Uncorrected Author Proof The baseline one model takes embedding results <sup>480</sup> of node2vec as representations of nodes in the graph. <sup>481</sup> The requirement based walk process selects all pos- <sup>482</sup> sible software stacks from the graph to give a <sup>483</sup> preliminary software stack. However, there are too <sup>484</sup> many groups in the preliminary data. The model cal- <sup>485</sup> culates the Euclidean distances between node vectors <sup>486</sup> to filter irrelevant results out. Figure 7 illustrates the <sup>487</sup> architecture of baseline one model. <sup>488</sup>

### *4.2.2. Baseline two*<sup>489</sup>

The baseline two extracts semantic information to <sup>490</sup> represent nodes in the software knowledge graph. The <sup>491</sup> training data consists of Wikipedia texts and descrip- <sup>492</sup> tion texts from stackshare. The basic idea of this <sup>493</sup> model is as same as that in baseline one model, but <sup>494</sup> the representations of nodes are different. This model <sup>495</sup> also takes Euclidean distance as a metric to filter irrel- <sup>496</sup> evant results out. Figure 8 illustrates the architecture of <sup>497</sup> the baseline two model. <sup>498</sup>

### *4.2.3. Baseline three*<sup>499</sup>

The baseline three combines both graph structure <sup>500</sup> information and semantic information to represent <sup>501</sup> nodes. In other words, the baseline three model is the <sup>502</sup> combination of baseline one and baseline two. This <sup>503</sup> model also uses the same method to filter irrelevant <sup>504</sup> results out. Figure 9 illustrates the architecture of the <sup>505</sup> baseline three model. <sup>506</sup>

![](_page_8_Figure_1.jpeg)
<!-- Image Description: The image illustrates a process of generating "Closer Results" using word embeddings. Text ("GNU Emacs is an extensible...") and a graph are inputted into "word2vec" and "node2vec" models, respectively. These models generate vector representations (a 3x3 matrix of numerical values is shown as an example). The combined vectors then produce improved results. The diagram depicts the workflow of the algorithm by showing the inputs, processing steps, and final output. -->

Figure 9. Baseline Three: the graph structure + description text results and distance calculation.

### <sup>507</sup>*4.2.4. Our method*Our method combines both graph structure infor- mation and semantic information to represent nodes, which is the same as that in baseline three. However, while baseline three just takes Euclidean distance as a metric to filter irrelevant results out, our method implements an SVM model to predict whether a soft-ware stack is valuable or not.

**Training:**The SVM model is trained by positive and negative samples. The positive samples consist of software stack data of 350 famous companies, each stack of a company is a piece of a positive sample. The negative samples are generated with two predefined <sup>520</sup> rules:

- <sup>521</sup> − Single software. As a stack is a set of software, <sup>522</sup> single software will not be a positive sample.
- <sup>523</sup> − Stacks with unpopular software. Normally, the <sup>524</sup> developer tends to use popular software. There-<sup>525</sup> fore, stacks with unpopular software are thought <sup>526</sup> as negative samples.

<sup>527</sup> In addition, software in a stack is represented as vec-<sup>528</sup> tors, so the stack is represented as the average of the <sup>529</sup> sum of all software vectors.

### <sup>530</sup>*4.3. The categories used in this experiment*To build a software stack, it is important to select appropriate categories. This problem solved by AI- CTO in two aspects. One is the number of companies using the category, which reflects the practicality. Another is the labels related to the category, which reflects the ability to meet user demand. Table 3 shows <sup>536</sup> the categories used in the evaluation of AI-CTO. As <sup>537</sup> the number of labels are too large, the table only <sup>538</sup> records the most weighted label. In fact, the label <sup>539</sup> is for software in the category, the heavier weights <sup>540</sup> mean the more users paying attention to this label, <sup>541</sup> i.e., user demand. <sup>542</sup>

### *4.4. Evaluation with correctness*<sup>543</sup>

**Motivation:**To answer RQ1 (Does AI-CTO find <sup>544</sup> effective results?), the AI-CTO is evaluated with real- <sup>545</sup> world data from stackshare. The AI-CTO is built <sup>546</sup> by both graph structure and description text fea- <sup>547</sup> tures and predict valuable software tool with an SVM <sup>548</sup> model. This is different from the baseline one and <sup>549</sup> two. In addition, baseline three also integrate graph <sup>550</sup> structure and description text features, but it derives <sup>551</sup> valuable software tool by calculating the Euclidean <sup>552</sup> distance. In this experiment, we would like to inves- <sup>553</sup> tigate whether AI-CTO can outperform the baseline <sup>554</sup> methods. <sup>555</sup>
**Metric:**We would like to perform the popular met- <sup>556</sup> ric, Hits@, in our experiment. For example, Hits@10 <sup>557</sup> is the proportion of correct stack solutions ranked in <sup>558</sup> the top 10. <sup>559</sup>

Uncorrected Author Proof**Results:**We test the correctness experiment on <sup>560</sup> three baseline methods and AI-CTO. As the mod- <sup>561</sup> els obtain a great deal of ranking results from the <sup>562</sup> selection space, we choose 20, 50, 100 as metrics <sup>563</sup> to evaluate the methods. According to the results <sup>564</sup> reported in Table 4, AI-CTO perform better than <sup>565</sup> all baseline methods in Hits@20, Hits@50 and <sup>566</sup> Hits@100. Figure 10 shows the results of different <sup>567</sup> number of "category". The node2vec performs bet- <sup>568</sup> ter than word2vec, because the graph structure can <sup>569</sup> better reflect the distance feature compared with the <sup>570</sup> text feature. However, the description text features <sup>571</sup> are still helpful to distinguish the software entities. <sup>572</sup>

| Table 3 | |
|--------------------------------------------------|--|
| The categories used in the evaluation for AI-CTO | |

| Category | Company num | Label | Label Weight |
|---------------------------|-------------|---------------------------------|--------------|
| Languages | 981 | Can be used on frontend/backend | 1600 |
| Databases | 501 | Document-oriented storage | 789 |
| Javascript UI Libraries | 355 | Cross-browser | 1300 |
| Javascript MVC Frameworks | 203 | Quick to develop | 883 |
| In-Memory Databases | 222 | Performance | 843 |
| Frameworks (Full Stack) | 479 | Npm | 1300 |
| Web Servers | 312 | High-performance http server | 1400 |
| Microframeworks (Backend) | 106 | Simple | 322 |
| General Analytics | 254 | Free | 1500 |

Table 4 The results of evaluation with correctness. 8 categories used

| Metric | Hits@20 | Hits@50 | Hits@100 |
|-------------------|---------|---------|----------|
| node2vec | 0.85 | 0.8 | 0.64 |
| word2vec | 0.0 | 0.0 | 0.07 |
| node2vec+word2vec | 0.55 | 0.38 | 0.44 |
| AI-CTO | 0.95 | 0.84 | 0.75 |

![](_page_9_Figure_4.jpeg)
<!-- Image Description: The image displays a line graph comparing the performance of four methods (node2vec, word2vec, node2vec+word2vec, AI-CTO) for a Hits@100 metric. The x-axis represents the number of categories, and the y-axis shows the Hits@100 score. The graph illustrates how the performance of each method changes with varying numbers of categories. The purpose is to compare the effectiveness of different embedding methods in a categorization task. -->

Figure 10. The hits results of different number of "category" in the stack.

Table 5 The results of evaluation with number of users. 8 categories used

| Metric | top(20) | top(50) | top(100) |
|-------------------|---------|---------|----------|
| node2vec | 45 | 92 | 137 |
| word2vec | 0 | 0 | 7 |
| node2vec+word2vec | 11 | 22 | 51 |
| AI-CTO | 49 | 94 | 157 |

### <sup>573</sup>*4.5. Evaluation with number of Users*

**Motivation:**This experiment is performed to answer RQ2 (Are the AI-CTO solutions used by real users?). We would like to investigate whether the solutions of AI-CTO are used by companies.

<sup>578</sup>**Metric:**We would like to perform the number of <sup>579</sup> users in this experiment. The top(x) means the num-<sup>580</sup> ber of companies who use the top x stacks.
**Results:**According to the results reported in Table 5, AI-CTO perform better than all baseline methods in top20, top50 and top100. The solutions derived by AI-CTO are used by real users.

### 5. Threats to validity <sup>585</sup>

There are defects of AI-CTO, this section discusses <sup>586</sup> the threats to validity and why AI-CTO is still effec- <sup>587</sup> tive. <sup>588</sup>

### *5.1. Treats to software categories*<sup>589</sup>

Uncorrected Author Proof The software stack is built based on the software <sup>590</sup> categories required by developers. For example, a <sup>591</sup> website application may need three kinds of tool, <sup>592</sup> front-end framework, web server and databases. The <sup>593</sup> stacking process selects three tools for the three kinds <sup>594</sup> of tool respectively. Therefore, an important task is <sup>595</sup> determining which categories are needed. Based on <sup>596</sup> the hypothesis that the more companies using this <sup>597</sup> category, the more important it is. AI-CTO choose <sup>598</sup> a category depending on the number of compa- <sup>599</sup> nies using it. Thus, the performance of our method <sup>600</sup> depends on the quality of the technology stack data. <sup>601</sup> In the future, we will try to analyse the characteristics <sup>602</sup> of the software category itself, and then compare it <sup>603</sup> with the results of AI-CTO. <sup>604</sup>

### *5.2. Treats to dataset*<sup>605</sup>

As the dataset used in this paper is invariant, the <sup>606</sup> performance of AI-CTO may be affected when new <sup>607</sup> data is generated. However, companies do not adjust <sup>608</sup> their technology stacks frequently. As the idea of <sup>609</sup> AI-CTO is learning from the experience, the "old" <sup>610</sup> data is sufficient to verify the feasibility of AI-CTO. <sup>611</sup> In addition, it is hard to test the integrality of data <sup>612</sup> from stackshare, and it is unable to check whether <sup>613</sup> the technology stack of a company is complete on <sup>614</sup> stackshare. <sup>615</sup>

## *5.3. Treats to software knowledge graph and*<sup>616</sup>*embedding*<sup>617</sup>

Usually, a knowledge graph consists of various <sup>618</sup> entities and relations, i.e., the classification of rela- <sup>619</sup> tions can be different. The different relation can <sup>620</sup> represent more information in a graph. The software <sup>621</sup> knowledge graph in this paper contains only one kind <sup>622</sup> of directed relation with weights. However, the rela- <sup>623</sup> tions in this graph do not include any attributes. As <sup>624</sup> a node is represented by its neighbourhoods, single <sup>625</sup> type of relations is capable to depict the information <sup>626</sup> in the embedding process. <sup>627</sup>

## <sup>628</sup> 6. Related work

### <sup>629</sup>*6.1. Software architecture*Software architecture is the blueprint of a system. The architecture reflects the constrained relationships among software components, and those constraints most often come from the system requirements [25]. The modelling of software architecture greatly affects the development performance of practitioners [26]. The research about software architecture gains great attention since the nineties to deal with increasingly software design complexity [27, 28]. To formalise the architectural process, Architecture Description Language (ADL) is used to specify the software architectures precisely, such as Unified Modelling Language (UML) [29, 30], SystemC [31] and Acme<sup>5</sup> <sup>642</sup> [32]. However, there is not a final conclusion about what extent developers utilise software architecture technologies in software design [27]. In most cases, developers just find a design solution of the software system, but the reason of the solution reflects quality issues for the system [27, 33].

In addition, it is difficult to clearly distinguish the boundary of architecture layer and design layer [4]. In this paper, the "architecture" is considered to be an element of architectural styles. The "design" is considered to be the process of choosing a develop- ment tool for each element of architectural styles. The AI-CTO convert the development experience of famous companies to knowledge, i.e., the software knowledge graph. Based on the knowledge, develop- ers choose development tools for each element in the architectural style, which is the software stack solu- tion. It is worth mentioning that the solution derives from the knowledge is interpretable.

### <sup>662</sup>*6.2. Graph embedding*

Graphs exist widely in the real world [34], such as social media network, citation graph of research arti- cles, protein molecular structure graph, etc. These graphs contain valuable information that deserves to be analysed. Therefore, this field has received much attention in recent years. A significant num- ber of researches about graph analytics are proposed, such as personalised recommender system [35], entity/node classification [36], relation prediction [37], entity/node clustering [38], etc.

Uncorrected Author Proof Early technologies are built based on the symbolic <sup>673</sup> representation of graphs, i.e. triples. However, due <sup>674</sup> to the complex structure of graphs, these technolo- <sup>675</sup> gies are computationally inefficient when dealing <sup>676</sup> with large-scale graph [39]. To solve the problem, <sup>677</sup> graph embedding has been presented for embedding <sup>678</sup> entities and relations between them into a contin- <sup>679</sup> uous low-dimensional vector space [40]. In fact, <sup>680</sup> graph embedding overlaps in graph analytics [41] <sup>681</sup> and representation learning [42]. The purpose of <sup>682</sup> graph analytics is to extract valuable information <sup>683</sup> from graph data. Representation learning transforms <sup>684</sup> raw data into a form that can be effectively developed <sup>685</sup> by machine learning technologies. A common idea <sup>686</sup> is extracting normalised data from graphs by graph <sup>687</sup> analytics and applying representation learning to the <sup>688</sup> normalised data. For example, DeepWalk [43] gen- <sup>689</sup> erates sequence data (paths in the graph) which is <sup>690</sup> similar to text by limited random walk from input <sup>691</sup> graph and then uses the node id as a "word" to learn <sup>692</sup> the node vector with Skip-gram model. On the basis <sup>693</sup> of DeepWalk, node2vec [8] defines a bias random <sup>694</sup> walk and still uses Skip-gram to train. The walk mode <sup>695</sup> can be changed by adjusting the bias weights, thus <sup>696</sup> retaining different graph structure information, such <sup>697</sup> as walk modes of BFS and DFS. <sup>698</sup>

There are also graph embedding technologies <sup>699</sup> using predefined graph structure as features. The <sup>700</sup> embedding work in TransE [6] is done by adjust- <sup>701</sup> ing the relation in a triple. For example, a triple <sup>702</sup> (*h, r, t*) holds means *Vectorh*+*Vectorr*≈*Vectort*. <sup>703</sup> This provides insights into how to build the energy <sup>704</sup> function, i.e. ||*h*+*r*−*t*||*l*1. Obviously, transE works <sup>705</sup> ineffectively on one-to-many and many-to-one rela- <sup>706</sup> tion problems. TransH [44] embeds h and t to <sup>707</sup> a vector space while embedding *r* to a hyper- <sup>708</sup> plane, i.e. (*h*→*h* ), (*t*→*t* ). The triple (*h, r, t*) <sup>709</sup> holds means *Vectorh*+*Vectorr*≈*Vectort*. More- <sup>710</sup> over, TransR [45], TranSparse [46], TransAt [47], <sup>711</sup> Adversarial Graph Embeddings [48], DELN [49], <sup>712</sup> JANE [50], MTNE [51], etc also presented efficient <sup>713</sup> methods to solve problems in this field. <sup>714</sup>

### *6.3. Auxiliary information*<sup>715</sup>

The input data of graph embedding is diverse, such <sup>716</sup> as the whole graph, nodes, and edges. There can be <sup>717</sup> certain auxiliary information for nodes and edges, <sup>718</sup> such as text descriptions, attributes, labels, and etc, <sup>719</sup> which can be used to enhance the performance of <sup>720</sup> graph embedding. The challenge is how to incorpo- <sup>721</sup> rate the auxiliary information in graph embedding <sup>722</sup>

<sup>5</sup>[http://www.cs.cmu.edu/](http://www.cs.cmu.edu/$~$acme/)∼acme/

<sup>723</sup> model and how to combine it with graph structure <sup>724</sup> information.

Xie et al. [39] propose two encoder, i.e. continuous bag-of-words and deep convolutional neural models, to transform semantics of entity description into vectors. They then define an energy function, i.e.*E*=*ES*+*ED*, to combine description-based representation and structure-based representation. *ES*is the energy function of TransE to represent the structure information.*ED*is the energy function of description-based representation and defined as:*ED*=*EDD*+*EDS*+*ESD*, where *EDD* = ||*Vectorhd*+*r*−*Vectortd*||.*Vectorhd*<sup>735</sup> is the description-based representation of head node in the triple.*EDS*and*ESD*are analogous to that.

Uncorrected Author Proof Wang and Li [52] use rich context information in an external text corpus to assist in representation learning of the knowledge graph. Similar to distance supervision, they first annotate the entity back to the text corpus to obtain a co-occurrence network con- sisted of entity words and other important words. The network can be regarded as the link between the knowledge graph and the text information. The context of entities and relations is defined based on the network and integrated into the knowledge graph. Finally, the representation of entities and relations is learned by a translation model. Other auxiliary infor- mation is also used to improve the performance of graph embedding, such as relation [53], attribute [54], <sup>752</sup> etc.

### <sup>753</sup> 7. Conclusion and future work

This paper proposes AI-CTO, a novel method to automatically suggest software stack solutions. The basic idea of AI-CTO is converting the development experience of famous companies to knowledge, i.e., software knowledge graph. The software stack solu- tions are derived from the knowledge. To reach this end, we embed the software knowledge graph to a low-dimensional vector space. In addition, we com- bine embedding of software descriptions to make the graph embedding more precisely. The evalua- tion of AI-CTO consists of two research question to analyse its effectiveness. The results show that AI-CTO can suggest effective solutions and outper- form other baselines. We will explore the following research directions in future: (1) It is possible to include more features for software, such as the code features of open-source software. (2) The descrip-tion encoder only considers software descriptions and name for embedding, while there are various infor- <sup>772</sup> mation, which is possible to be utilised in future. (3) <sup>773</sup> There are no attributes for relations in the software <sup>774</sup> knowledge graph. It is able to include more informa- <sup>775</sup> tion for relations between entities in future. <sup>776</sup>

### Acknowledgment <sup>777</sup>

This work is supported by National Key R&D <sup>778</sup> Program of China (No. 2018YFB0803600) and <sup>779</sup> National Natural Science Foundation of China <sup>780</sup> (No. 61772507). <sup>781</sup>
**References** <sup>782</sup>

- [1] D. Garlan, Software architecture: a roadmap. In*Proceedings*<sup>783</sup>*of the Conference on the Future of Software Engineering*, <sup>784</sup> pages 91–101. Citeseer, (2000). <sup>785</sup>
- [2] R. Capilla, A. Jansen, A. Tang, P. Avgeriou and M. Ali <sup>786</sup> Babar, 10 years of software architecture knowledge manage- <sup>787</sup> ment: Practice and future, *Journal of Systems and Software*<sup>788</sup>**116**(2016), 191–205. <sup>789</sup>
- [3] G. Tassey, The economic impacts of inadequate infrastruc- <sup>790</sup> ture for software testing,*National Institute of Standards and*<sup>791</sup>*Technology, RTI Project* **7007**(011) (2002), 429–489. <sup>792</sup>
- [4] M. Shaw, D. Garlan, et al., Software architecture, volume <sup>793</sup> 101. prentice Hall Englewood Cliffs, (1996). <sup>794</sup>
- [5] D. Garlan and M. Shaw, An introduction to software archi- <sup>795</sup> tecture. In *Advances in software engineering and knowledge*<sup>796</sup>*engineering*, pages 1–39. World Scientific, (1993). <sup>797</sup>
- [6] A. Bordes, N. Usunier, A. Garcia-Duran, J. Weston <sup>798</sup> and O. Yakhnenko, Translating embeddings for modeling <sup>799</sup> multi-relational data, In *Advances in neural information*<sup>800</sup>*processing systems*(2013), pages 2787–2795. <sup>801</sup>
- [7] D.Q. Nguyen, K. Sirts, L. Qu and M. Johnson, Stranse: <sup>802</sup> a novel embedding model of entities and relationships in <sup>803</sup> knowledge bases,*arXiv preprint arXiv:1606.08140*, (2016). <sup>804</sup>
- [8] A. Grover and J. Leskovec, node2vec: Scalable feature <sup>805</sup> learning for networks. In *Proceedings of the 22nd ACM*<sup>806</sup>*SIGKDD international conference on Knowledge discovery*<sup>807</sup>*and data mining*, pages 855–864. ACM, (2016). <sup>808</sup>
- [9] L. Ponzanelli, G. Bavota, M. Di Penta, R. Oliveto and M. <sup>809</sup> Lanza, Mining stackoverflow to turn the ide into a self- <sup>810</sup> confident programming prompter. In *Proceedings of the*<sup>811</sup>*11th Working Conference on Mining Software Repositories,*<sup>812</sup>*MSR*(2014), pages 102–111, New York, NY, USA, 2014. <sup>813</sup> ACM. <sup>814</sup>
- [10] L. Ponzanelli, S. Scalabrino, G. Bavota, A. Mocci, R. <sup>815</sup> Oliveto, M. Di Penta and M. Lanza, Supporting soft- <sup>816</sup> ware developers with a holistic recommender system. In <sup>817</sup>*2017 IEEE/ACM 39th International Conference on Soft-*<sup>818</sup>*ware Engineering (ICSE)*, pages 94–105. *IEEE*, (2017). <sup>819</sup>
- [11] X. Zhao, Z. Xing, M.A. Kabir, N. Sawada, J. Li and S.-W. <sup>820</sup> Lin, Hdskg: Harvesting domain specific knowledge graph <sup>821</sup> from content of webpages. In *2017 IEEE 24th International*<sup>822</sup>*Conference on Software Analysis, Evolution and Reengi-*<sup>823</sup>*neering (SANER)*, pages 56–67. *IEEE*, (2017). <sup>824</sup>

- <sup>825</sup> [12] A. Singhal, Introducing the knowledge graph: things, <sup>826</sup> not strings. [https://googleblog.blogspot.com/2012/](https://googleblog.blogspot.com/2012/05/introducing-knowledge-graph-things-not.html) <sup>827</sup> [05/introducing-knowledge-graph-things-not.html,](https://googleblog.blogspot.com/2012/05/introducing-knowledge-graph-things-not.html) May 16, <sup>828</sup> (2012). Accessed: August 4, 2019.
- <sup>829</sup> [13] A. Carlson, J. Betteridge, B. Kisiel, B. Settles, E.R. <sup>830</sup> Hruschka and T.M. Mitchell, Toward an architecture for <sup>831</sup> never-ending language learning, In *Twenty-Fourth AAAI*<sup>832</sup>*Conference on Artificial Intelligence*, (2010).
- <sup>833</sup> [14] D. Vrandeciˇ c and M. Kr ´ otzsch, Wikidata: A free collab- ¨ <sup>834</sup> orative knowledge base, *Communications of the ACM* **57**<sup>835</sup> (2014), 78–85.
- <sup>836</sup> [15] F. Wu and D.S. Weld, Open information extraction using <sup>837</sup> wikipedia. In*Proceedings of the 48th annual meeting of the*<sup>838</sup>*association for computational linguistics*, pages 118–127. <sup>839</sup> Association for Computational Linguistics, (2010).
- <sup>840</sup> [16] M. Schmitz, R. Bart, S. Soderland, O. Etzioni, et al., Open <sup>841</sup> language learning for information extraction, In *Proceed-*<sup>842</sup> *ings of the 2012 Joint Conference on Empirical Methods*<sup>843</sup>*in Natural Language Processing and Computational Nat-*<sup>844</sup> *ural Language Learning*, pages 523–534. Association for <sup>845</sup> Computational Linguistics, (2012).
- <sup>846</sup> [17] A. Fader, S. Soderland and O. Etzioni, Identifying rela-<sup>847</sup> tions for open information extraction, In *Proceedings of the*<sup>848</sup>*conference on empirical methods in natural language pro-*<sup>849</sup> *cessing*, pages 1535–1545. Association for Computational <sup>850</sup> Linguistics, (2011).
- <sup>851</sup> [18] Z.-Q. Lin, B. Xie, Y.-Z. Zou, J.-F. Zhao, X.-D. Li, J. Wei, H.- <sup>852</sup> L. Sun and G. Yin, Intelligent development environment and <sup>853</sup> software knowledge graph, *Journal of Computer Science*<sup>854</sup>*and Technology* **32**(2) (2017), 242–249.
- <sup>855</sup> [19] H.S. Delugach, Specifying multiple-viewed software <sup>856</sup> requirements with conceptual graphs, *Journal of Systems*<sup>857</sup>*and Software* **19**(3) (1992), 207–224.
- <sup>858</sup> [20] H.-J. Happel and S. Seedorf, Applications of ontologies <sup>859</sup> in software engineering. In *Proc. of Workshop on Sematic*<sup>860</sup>*Web Enabled Software Engineering"(SWESE) on the ISWC*, <sup>861</sup> pages 5–9. Citeseer, (2006).
- <sup>862</sup> [21] R. Padhye, D. Mukherjee and V.S. Sinha, Api as a social <sup>863</sup> glue. In *Companion Proceedings of the 36th International*<sup>864</sup>*Conference on Software Engineering*, pages 516–519.*ACM*, <sup>865</sup> (2014).
- <sup>866</sup> [22] T. Mikolov, K. Chen, G. Corrado and J. Dean, Efficient <sup>867</sup> estimation of word representations in vector space, *arXiv*<sup>868</sup>*preprint arXiv:1301.3781*, (2013).
- <sup>869</sup> [23] Q. Zhong, H. Li, J. Li, G. Xie, J. Tang, L. Zhou and Y. Pan, <sup>870</sup> A gauss function based approach for unbalanced ontology <sup>871</sup> matching. In *Proceedings of the 2009 ACM SIGMOD Inter-*<sup>872</sup> *national Conference on Management of Data, SIGMOD* <sup>873</sup> '*09*, pages 669–680, New York, NY, USA, (2009). ACM.
- <sup>874</sup> [24] K. Pearson, Liii. on lines and planes of closest fit to <sup>875</sup> systems of points in space, *The London, Edinburgh, and*<sup>876</sup>*Dublin Philosophical Magazine and Journal of Science*<sup>877</sup>**2**(11) (1901), 559–572.
- <sup>878</sup> [25] D.E. Perry and A.L. Wolf, Foundations for the study of soft-<sup>879</sup> ware architecture, *SIGSOFT Softw Eng Notes* **17**(4) (1992), <sup>880</sup> 40–52.
- <sup>881</sup> [26] M. Ozkaya and F. Erata, Understanding practitioners' <sup>882</sup> challenges on software modeling: A survey, *Journal of Com-*<sup>883</sup> *puter Languages* **58**(2020), 100963.
- <sup>884</sup> [27] M. Ozkaya, What is software architecture to practitioners: A <sup>885</sup> survey, In*International Conference on Model-driven Engi-*<sup>886</sup> *neering & Software Development*, (2017).
- <sup>887</sup> [28] M. Ozkaya and F. Erata, A survey on the practical use of uml <sup>888</sup> for different software architecture viewpoints, *Information*<sup>889</sup>*and Software Technology* **121**(2020),106275.

- [29] G. Booch, The unified modeling language user guide,*Pear-*<sup>890</sup>*son Education India*(2005). <sup>891</sup>
- [30] M. Ozkaya, Are the uml modelling tools powerful enough <sup>892</sup> for practitioners? a literature review,*IET Software* **13**(16) <sup>893</sup> (2019), 338–354. <sup>894</sup>
- [31] D.C. Black, J. Donovan, B. Bunton and A. Keist, System <sup>895</sup> C: From the ground up, volume **71**. *Springer Science &*<sup>896</sup>*Business Media*, (2009). <sup>897</sup>
- [32] D. Garlan, R. Monroe and D. Wile, Acme: An architec- <sup>898</sup> ture description interchange language. In *Proceedings of*<sup>899</sup>*the 1997 Conference of the Centre for Advanced Studies*<sup>900</sup>*on Collaborative Research, CASCON '97*, pages 7–. IBM <sup>901</sup> Press, (1997). <sup>902</sup>
- [33] H. van Vliet and A. Tang, Decision making in software <sup>903</sup> architecture, *Journal of Systems and Software* **117**(2016), <sup>904</sup> 638–644. <sup>905</sup>
- [34] H. Cai, V.W. Zheng and K.C.-C. Chang, A comprehen- <sup>906</sup> sive survey of graph embedding: Problems, techniques, and <sup>907</sup> applications,*IEEE Transactions on Knowledge and Data*<sup>908</sup>*Engineering* **30**(9) (2018), 1616–1637. <sup>909</sup>
- [35] H. Wang, M. Zhao, X. Xie, W. Li and M. Guo, Knowledge <sup>910</sup> graph convolutional networks for recommender systems, In <sup>911</sup> *The World Wide Web Conference*, pages 3307–3313. ACM, <sup>912</sup> (2019). <sup>913</sup>
- [36] X. Wang, P. Cui, J. Wang, J. Pei, W. Zhu and S. Yang, <sup>914</sup> Community preserving network embedding, In *Thirty-First*<sup>915</sup>*AAAI Conference on Artificial Intelligence*, (2017). <sup>916</sup>
- [37] X. Wei, L. Xu, B. Cao and P.S. Yu, Cross view link predic- <sup>917</sup> tion by learning noise-resilient representation consensus, In <sup>918</sup> *Proceedings of the 26th International Conference on World*<sup>919</sup>*Wide Web*, pages 1611–1619. *International World Wide Web*<sup>920</sup>*Conferences Steering Committee*, (2017). <sup>921</sup>
- [38] F. Nie, W. Zhu and X. Li, Unsupervised large graph <sup>922</sup> embedding, In *Thirty-first AAAI conference on artificial*<sup>923</sup>*intelligence*, (2017). <sup>924</sup>
- [39] R. Xie, Z. Liu, J. Jia, H. Luan and M. Sun, Representa- <sup>925</sup> tion learning of knowledge graphs with entity descriptions, <sup>926</sup> In *Thirtieth AAAI Conference on Artificial Intelligence*, <sup>927</sup> (2016). <sup>928</sup>
- Uncorrected Author Proof [40] X. Dong, E. Gabrilovich, G. Heitz, W. Horn, N. Lao, K. Mur- <sup>929</sup> phy, T. Strohmann, S. Sun and W. Zhang, Knowledge vault: <sup>930</sup> A web-scale approach to probabilistic knowledge fusion, In <sup>931</sup> *Proceedings of the 20th ACM SIGKDD international con-*<sup>932</sup>*ference on Knowledge discovery and data mining*, pages <sup>933</sup> 601–610. ACM, (2014). <sup>934</sup>
- [41] N. Satish, N. Sundaram, M.M.A. Patwary, J. Seo, J. Park, <sup>935</sup> M.A. Hassaan, S. Sengupta, Z. Yin and P. Dubey, Navigating <sup>936</sup> the maze of graph analytics frameworks using massive graph <sup>937</sup> datasets, In*Proceedings of the 2014 ACM SIGMOD interna-*<sup>938</sup>*tional conference on Management of data*, pages 979–990. <sup>939</sup> ACM, (2014). <sup>940</sup>
- [42] Y. Bengio, A. Courville and P. Vincent, Representation <sup>941</sup> learning: A review and new perspectives, *IEEE transactions*<sup>942</sup>*on pattern analysis and machine intelligence*, **35**(8) (2013), <sup>943</sup> 1798–1828. <sup>944</sup>
- [43] B. Perozzi, R. Al-Rfou and S. Skiena, Deepwalk: Online <sup>945</sup> learning of social representations. In *Proceedings of the*<sup>946</sup>*20th ACM SIGKDD international conference on Knowl-*<sup>947</sup>*edge discovery and data mining*, pages 701–710. ACM, <sup>948</sup> (2014). <sup>949</sup>
- [44] Z. Wang, J. Zhang, J. Feng and Z. Chen, Knowledge graph <sup>950</sup> embedding by translating on hyperplanes, In *Twenty-Eighth*<sup>951</sup>*AAAI conference on artificial intelligence*, (2014). <sup>952</sup>
- [45] Y. Lin, Z. Liu, M. Sun, Y. Liu and X. Zhu, Learning entity <sup>953</sup> and relation embeddings for knowledge graph completion, <sup>954</sup>

<sup>955</sup> In *Twenty-ninth AAAI conference on artificial intelligence*, <sup>956</sup> (2015).

- <sup>957</sup> [46] G. Ji, K. Liu, S. He and J. Zhao, Knowledge graph comple-<sup>958</sup> tion with adaptive sparse transfer matrix, In *Thirtieth AAAI*<sup>959</sup>*Conference on Artificial Intelligence*, (2016).
- <sup>960</sup> [47] W. Qian, C. Fu, Y. Zhu, D. Cai and X. He, Translat-<sup>961</sup> ing embeddings for knowledge graph completion with <sup>962</sup> relation attention mechanism, In *Proceedings of the*<sup>963</sup>*Twenty Seventh International Joint Conference on Artifi-*<sup>964</sup> *cial Intelligence, IJCAI-18*, pages 4286–4292.*International*<sup>965</sup>*Joint Conferences on Artificial Intelligence Organization*, <sup>966</sup> **7**(2018).
- <sup>967</sup> [48] M. Khajehnejad, A.A. Rezaei, M. Babaei, J. Hoffmann, M. <sup>968</sup> Jalili and A. Weller, Adversarial graph embeddings for fair <sup>969</sup> influence maximization over social networks. In*Christian*<sup>970</sup>*Bessiere, editor, Proceedings of the Twenty-Ninth Interna-*<sup>971</sup> *tional Joint Conference on Artificial Intelligence, IJCAI-20*, <sup>972</sup> pages 4306–4312. *International Joint Conferences on Arti-*<sup>973</sup> *ficial Intelligence Organization*, **7** (2020). Special track on <sup>974</sup> AI for Comp Sust and Human well-being.
- <sup>975</sup> [49] H. Yang, L. Chen, M. Lei, L. Niu, C. Zhou and P. <sup>976</sup> Zhang, Discrete embedding for latent networks, In*Christian*<sup>977</sup>*Bessiere, editor, Proceedings of the Twenty-Ninth Interna-*<sup>978</sup> *tional Joint Conference on Artificial Intelligence, IJCAI-20*, <sup>979</sup> pages 1223–1229. *International Joint Conferences on Arti-*- <sup>980</sup>*ficial Intelligence Organization*, **7**(2020). Main track.

- [50] L. Yang, Y. Wang, J. Gu, C. Wang, X. Cao and Y. Guo, <sup>981</sup> Jane: Jointly adversarial network embedding. In*Christian*<sup>982</sup>*Bessiere, editor, Proceedings of the Twenty-Ninth Interna-*<sup>983</sup>*tional Joint Conference on Artificial Intelligence, IJCAI-20*, <sup>984</sup> pages 1381–1387. *International Joint Conferences on Arti-*<sup>985</sup>*ficial Intelligence Organization*, **7**(2020). Main track. <sup>986</sup>
- Uncorrected Author Proof [51] H. Huang, Z. Fang, X. Wang, Y. Miao and H. Jin, <sup>987</sup> Motif-preserving temporal network embedding. In Chris- <sup>988</sup> tian Bessiere, editor,*Proceedings of the Twenty-Ninth*<sup>989</sup>*International Joint Conference on Artificial Intelligence,*<sup>990</sup>*IJCAI-20*, pages 1237–1243. *International Joint Confer-*<sup>991</sup>*ences on Artificial Intelligence Organization*, **7**(2020). <sup>992</sup> Main track. <sup>993</sup>
- [52] Z. Wang and J. Li, Text-enhanced representation learning <sup>994</sup> for knowledge graph. In*Proceedings of the Twenty-Fifth*<sup>995</sup>*International Joint Conference on Artificial Intelligence,*<sup>996</sup>*IJCAI'16*, pages 1293–1299. AAAI Press, (2016). <sup>997</sup>
- [53] B.D. Trisedya, G. Weikum, J. Qi and R. Zhang, Neural <sup>998</sup> relation extraction for knowledge base enrichment, In *Pro-*<sup>999</sup>*ceedings of the 57th Annual Meeting of the Association for*<sup>1000</sup>*Computational Linguistics*, pages 229–240, Florence, Italy, <sup>1001</sup> July (2019). *Association for Computational Linguistics*. <sup>1002</sup>
- [54] B.D. Trisedya, J. Qi and R. Zhang, Entity alignment between <sup>1003</sup> knowledge graphs using attribute embeddings, In *Proceed-*<sup>1004</sup>*ings of the AAAI Conference on Artificial Intelligence*, <sup>1005</sup> volume **33**, pages 297–304. (2019). <sup>1006</sup>


## TL;DR
Research on ai-cto: knowledge graph for automated and dependable software stack solution providing insights for knowledge graph development and data integration.

## Key Insights
Contributes to the broader understanding of knowledge graph technologies and data management practices relevant to PKG system development.

## Metadata Summary
### Research Context
- **Research Question**: 
- **Methodology**: 
- **Key Findings**: 

### Analysis
- **Limitations**: 
- **Future Work**: 