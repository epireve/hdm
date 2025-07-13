---
cite_key: briggs_2020
title: A Review of Privacy-preserving Federated Learning for the Internet-of-Things
authors: Christopher Briggs, Zhong Fan, Peter Andras
year: 2021
relevancy: Medium
relevancy_justification: Contains relevant concepts applicable to HDM systems
tags: 
date_processed: 2025-07-02
phase2_processed: true
original_folder: arxiv_arxiv_2004.11794_A_Review_of_Privacy-preserving_Federated_Learning_for_the_Internet-of-Things
images_total: 1
images_kept: 1
images_removed: 0
keywords: 
---

# A Review of Privacy-preserving Federated Learning for the Internet-of-Things

Christopher Briggs, Zhong Fan and Peter Andras

**Abstract** The Internet-of-Things (IoT) generates vast quantities of data, much of it attributable to individuals' activity and behaviour. Gathering personal data and performing machine learning tasks on this data in a central location presents a significant privacy risk to individuals as well as challenges with communicating this data to the cloud. However, analytics based on machine learning and in particular deep learning benefit greatly from large amounts of data to develop high-performance predictive models. This work reviews federated learning as an approach for performing machine learning on distributed data with the goal of protecting the privacy of user-generated data as well as reducing communication costs associated with data transfer. We survey a wide variety of papers covering communication-efficiency, client heterogeneity and privacy preserving methods that are crucial for federated learning in the context of the IoT. Throughout this review, we identify the strengths and weaknesses of different methods applied to federated learning and finally, we outline future directions for privacy preserving federated learning research, particularly focusing on IoT applications.

## 1 Introduction

The Internet-of-Things (IoT) is represented by network-connected machines, often small embedded computers that provide physical objects with digital capabilities such as identification, inventory tracking and sensing & actuator control. Mobile devices such as smartphones also represent a facet of the IoT, often used as a sensing

Zhong Fan

Peter Andras

Christopher Briggs

Keele University, Staffordshire, UK, e-mail: <c.briggs@keele.ac.uk>

Keele University, Staffordshire, UK e-mail: <z.fan@keele.ac.uk>

Keele University, Staffordshire, UK e-mail: <p.andras@keele.ac.uk>

device as well as to control and monitor other IoT devices. The applications that drive analytical insights in the IoT are often powered by machine learning and deep learning.

Gartner [[1]](#ref-1) predicts that 25 billion IoT devices will be in use by 2021, forecasting a bright future for IoT applications. However this poses a challenge for traditional cloud-based IoT computing. The volume, velocity and variety of data streaming from billions of these devices requires vast amounts of bandwidth which can become extremely cost prohibitive. Additionally, many IoT applications require very low-latency or near real-time analytics and decision making capabilities. The round-trip delay from devices to the cloud and back again is unacceptable for such applications. Finally, transmitting sensitive data collected by IoT devices to the cloud poses security and privacy concerns. Edge computing, and more recently, fog computing [[2]](#ref-2) have been proposed as a solution to these problems.

Edge computing (and its variants: mobile edge computing, multi-access edge computing) restrict analytics processing to the edge of the network – on devices attached to, or very close to the perception layer [[3]](#ref-3). However storage and compute power may be severely limited and coordination between multiple devices may be non-existent in the edge computing paradigm. Fog computing [[2]](#ref-2) offers an alternative to cloud computing or edge computing alone for many analytics tasks but significantly increases the complexity of an IoT network. Fog computing is generally described as a continuum of compute, storage and networking capabilities to power applications and services in one or more tiers that bridge the gap between the cloud and the edge [[4]](#ref-4), [[5]](#ref-5). Fog computing enables highly scalable, low-latency, geo-distributed applications, supporting location awareness and mobility [[6]](#ref-6). Despite rising interest in fog-based computing, much research is still focused on deployment of analytics applications (including deep learning applications) directly to edge devices.

Performing computationally expensive tasks such as training deep learning models on edge devices poses a challenge due to limited energy budgets and compute capabilities [[7]](#ref-7). In cloud environments, massively powerful and scalable servers making use of parallelisation are typically employed for deep learning tasks [[8]](#ref-8). In edge computing environments, alternative methods for distributing training are required. Additionally, as limited bandwidth is a key constraint in computing near/at the edge, the challenge of reducing network data transfer is also important. Federated learning [[9]](#ref-9) has been proposed as a method for distributed machine learning, suitable for edge computing environments addresses many of the issues discussed above namely, compute power, data transfer as well as privacy preservation.

This review provides a comprehensive survey of privacy preserving federated learning. We show how federated learning is ideally suited for data analytics in the IoT and review research addressing privacy concerns [[10]](#ref-10), bandwidth limitations [[11]](#ref-11), and power/compute limitations [[12]](#ref-12). The rest of this review is organised as follows. Section [2](#section-2) provides an introduction to preliminary work on distributed machine learning and its influence on federated learning literature. Section [3](#section-3) describes federated learning in detail and outlines the major contributions to federated learning research including methods for reducing communication. Following this, section [4](#section-4) gives an overview of privacy in data analysis and methods for preserving the privacy of an individual's data. Section [5](#section-5) follows with an analysis of privacy preserving methods as applied to federated learning to protect latent data. Finally section [6](#section-6) discusses major outstanding challenges and future directions to apply federated learning to IoT applications and section [7](#section-7) presents concluding remarks.

## <a id="section-2"></a>2 Distributed machine learning

Federated learning was preceded by much work in distributed machine learning in the data-centre [[13]](#ref-13), [[8]](#ref-8), [[14]](#ref-14). This section gives a brief history of distributed machine learning, paying particular attention to distributed deep learning training via stochastic gradient descent (SGD). Deep learning is concerned with machine learning problems based on artificial neural networks comprised of many layers and has been used with great success in the fields of computer vision, speech recognition and translation as well as many other areas [[15]](#ref-15). In these fields, most other machine learning methods have been surpassed by deep learning methods due to the very complex functions they can compute which can both approximate training labels and generalise well to unseen samples.

Deep neural networks (DNNs) are composed of multiple connected units (also known as neurons) organised into layers through which the training data flows [[16]](#ref-16). Each unit computes a weighted sum of its input values (including a bias term) composed with a non-linear activation function g(**W**>**X**+**b**) and returns the result to the next connected layer. Passing data through the network and performing a prediction is known as the forward pass. To train the network, a backward pass operation is specified to compute updates to the weights and biases in order to better approximate the labels associated with the training data. An algorithm known as backpropagation [[17]](#ref-17) is used to propagate the error back through each layer of the network by calculating gradients of the weights and biases with respect to the error.

DNNs perform best when trained on very large datasets and often incorporate millions if not billions of parameters to express weights between neurons (for example the AlexNet DNN achieved state-of-the-art performance on the ImageNet dataset in 2012 using 60 million parameters [[18]](#ref-18)). Both of these factors require large sums of memory and compute capabilities. To scale complex DNNs trained on lots of data requires concurrency across multiple CPUs or more commonly GPUs (most often in a local cluster). GPUs are optimised to perform matrix calculations and are well suited for the operations required to compute activations across a DNN. Concurrency can be achieved in a variety of ways as discussed below.

## 2.1 Concurrency

To train a large DNN efficiently across multiple nodes, the calculations required in the forward and backward passes need to parellelised. One method to achieve this is model parallelism which distributes collections of neurons among the available compute nodes [[13]](#ref-13). Each node then only needs to compute the activations of its own neurons, however must communicate regularly with nodes computing on connected neurons. The calculations on all nodes must occur synchronously and therefore computation proceeds at the speed of the slowest node in the cluster. Another drawback of the model parallelism approach is that the current mini-batch must be copied to all nodes in the compute cluster, further increasing communication costs within the cluster.

A second method resolves some of the issues of excessive communication between nodes by distributing one or more layers on each node. This ensures that that each worker node only needs to communicate with the one other node (a different node depending whether the computation is part of the forward pass or the backward pass) [[8]](#ref-8). However, this method still requires that data in the mini-batch be copied to all nodes in the cluster.

The final method to achieve parallelism in training a large DNN is termed data parallelism. This method partitions the training dataset and copies the subsets to each compute node in the cluster. Each node computes forward and backward passes over the same model but using mini-batches drawn from its own subset of the training data. The results of the weight updates are then reduced on each iteration via MapReduce or more commonly today, via message passing interface (MPI) [[8]](#ref-8). Data parallelism is particularly effective as most operations over mini-batches in SGD are independent. Therefore scaling the problem via sharding the data to many nodes is relatively simple compared to the methods mentioned above. This method solves the issue of training with large amounts of data but requires that the model (and its parameters) fit in memory on each node.

Hybrid parallelism combines two or all three of the concurrency schemes mentioned above to mitigate the drawbacks associated with each and best support parallelism on the underlying hardware. DistBelief [[13]](#ref-13) achieves this by distributing the data, network layers, and neurons within the same layer among the available compute nodes, making use of all three concurrency schemes. Similarly, Project Adam [[19]](#ref-19) employs all three concurrency schemes but much more efficiently than DistBelief (using significantly fewer nodes to achieve high accuracy on the ImageNet^1^ 22k data set)

## 2.2 Model consistency

Model consistency refers to the state of a model when trained in a distributed manner [[8]](#ref-8) - a consistent model should reflect the same parameter values among compute nodes prior to each training iteration (or set of training iterations, sometimes referred to as a communication round). In order to maintain model consistency, individual compute nodes need to write updates to a global parameter server [[14]](#ref-14). The parameter

^1^ http://www.image-net.org/

server performs some form of aggregation on the updates to synchronise a global model and the parameters (for example, weights in a neural network) are then shared with the individual compute nodes for the next iteration/round of training.

There are several broad methods by which to train, update and share a distributed deep learning model. Synchronous updates occur when the parameter server waits for all compute nodes to return parameters for aggregation. This method provides high consistency between iterations/rounds of training as each node always receives up-to-date parameters but is not hardware performant due to delays caused by the slowest communicating node. For example, a set of parameters w^t^ at time *t*is shared among*n*^c^ compute nodes. The compute nodes each perform some number of forward and backward passes over the data available to them and compute the parameter gradients ∆wc. These gradients are communicated to the parameter server, which in turn averages the gradients from all workers and then updates the parameters for time *t*+ 1:

$$
\Delta w_t = \frac{1}{n_c} \sum_{c=1}^{n_c} \Delta w_c.
$$

$$
w_{t+1} = w_t - \eta \Delta w_t.
$$
(1)

Asynchronous updates occur when the parameter server shares the latest parameters without waiting for all nodes to return parameter updates. This reduces model consistency as parameters can be overwritten and become stale due to slow communicating nodes. This method is hardware performant however as optimisation can proceed without waiting for all nodes to send parameter updates. The HOGWILD! algorithm [[20]](#ref-20) takes advantage of sparsity within the parameter update matrix to asynchronously update gradients in shared memory resulting in faster convergence. Downpour SGD [[13]](#ref-13) describes asynchronous updates as an additional mechanism to add stochasticity to the optimisation process resulting in greater prediction performance.

In order to improve consistency using hardware performant asynchronous updates, the concept of parameter 'staleness' has been tackled by several works. The stale synchronous parallel (SSP) model [[21]](#ref-21) synchronises the global model once a maximum staleness threshold has been reached but still allows workers to compute updates on stale values between global model syncs. The impact of staleness in asynchronous SGD can also be mitigated by adapting the learning rate as a function of the parameter staleness [[22]](#ref-22), [[23]](#ref-23). As an example a worker pushes an update at*t*=*j*to the parameter server at*t*=*i*. The parameters in the global model at *t*=*i*are the most up-to-date available. To prevent a stale parameter update from occurring, a staleness parameter ^τ^^k^ for the*^k^*-th parameter is calculated as ^τ^^k^ ^=^ *^i^*-*^j^*. The learning rate used in [Equation 1](#equation-1) is modified as:

$$
\eta_k = \begin{cases} \eta/\tau_k & \text{if } \tau_k \neq 0 \\ \eta & \text{otherwise} \end{cases}
$$
(2)

## 2.3 Centralised vs decentralised learning

Centralised distribution of the model updates requires a parameter server (which may be a single machine or sharded across multiple machines as in [[13]](#ref-13)). The global model tracks the averaged parameters aggregated from all the compute nodes that perform training (see [Equation 1](#equation-1)). The downside to this distribution method is the high communication cost between compute nodes and the parameter server. Multiple shards can relieve this bottleneck to some extent, such that different workers read and write parameter updates to specific shards [[19]](#ref-19), [[13]](#ref-13).

Heterogeneity of worker resources is handled well in centralised distribution models. Distributed compute nodes introduce varying amounts of latency (especially when distributed geographically as in [[24]](#ref-24)), yet training can proceed via asynchronous, or more efficiently, stale-synchronous methods [[25]](#ref-25). Heterogeneity is an inherent feature of [federated learning](#section-3).

Decentralised distribution of DNN training does not rely on a parameter server to aggregate updates from workers but instead allows workers to communicate with one another, resulting in each worker performing aggregation on data from the parameters it receives. Gossip algorithms that share updates between a fixed number of neighbouring nodes have been applied to distributed SGD [[26]](#ref-26), [[27]](#ref-27), [[28]](#ref-28) in order to efficiently communicate/aggregate updates between all nodes in an exponential fashion similar to how disease is spread during an epidemic.

Communication can be avoided completely during training, resulting in many individual models represented by very different parameters. These models can be combined (as an ensemble [[15]](#ref-15)), however averaging the predictions from many models can slow down inference on new data. To tackle this, a process known as knowledge distillation can be used to train a single DNN (known as the mimic network) to emulate the predictions of an ensemble model [[29]](#ref-29), [[30]](#ref-30), [[31]](#ref-31). Unlabelled data is passed through the ensemble network to obtain labels on which the mimic network can be trained.

## <a id="section-3"></a>3 Federated learning

## 3.1 Overview

Federated learning extends the idea of distributed machine learning, making use of data parallelism. However, rather than randomly partitioning a centralised dataset to many compute nodes, training occurs in the user domain on distributed data owned by the individual users (often referred to as clients) [[9]](#ref-9). The consequence of this is that user data is never shared directly with a third party orchestrating the training procedure. This greatly benefits users where the data might be considered sensitive. Where data needs to be observed (for example, during the training operation), processing is handled on the device where the data resides (for example a smartphone). Once a round of training is completed on the device, the model parameters are communicated to an aggregating server, such as a parameter server provided by a third party. Although the training data itself is never disclosed to the third-party, it is a reasonable concern that something about an individual's training data might be inferred by the parameter updates; this is discussed further in [section 5](#section-5).

Federated learning is vastly more distributed than traditional approaches for training machine learning models via data parallelism. Some of the key differences are [[9]](#ref-9):

- 1. **Many contributing clients** federated learning needs to be scalable to many millions of clients.
- 2. **Varying quantity of data owned by each user** some clients may train on only a few samples; others may have thousands.
- 3. **Often very different data distributions between users** user data is highly personal to individuals and therefore the model trained by each client represents non-IID (independent, identically distributed) data.
- 4. **High latency between clients and aggregating service** updates are commonly communicated via the internet introducing significant latency between communication rounds.
- 5. **Unstable communication between clients and aggregating service** client devices are likely to become unavailable during training due to their mobility, battery life, or other reasons.

These distinguishing features of federated learning pose challenges above and beyond standard distributed learning.

Although this review focuses on deep learning in particular, many other ML algorithms can be trained via federated learning. Any ML algorithm designed to minimise an objective function of the form:

$$
\min_{w \in \mathbb{R}^d} \frac{1}{m} \sum_{i=1}^m f_i(w). \tag{3}
$$

is well suited to training via many clients (for example linear regression and logistic regression). Some non-gradient based algorithms can also be trained in this way, such as principal component analysis and k-mean clustering [[32]](#ref-32).

Federated optimisation was first suggested as a new setting for vastly and unevenly distributed machine learning by Konecný et al. [[33]](#ref-33) in 2016. In their work, the authors ˘ first describe the nature of the federated setting (non-IID data, varying quantity of data per client etc). Additionally, the authors test a simple application of distributed gradient descent against a federated modification of SVRG (a variance reducing variant of SGD [[34]](#ref-34)) over distributed data. Federated SVRG calculates gradients and performs parameter updates on each of*K*nodes over the available data on each node and obtains a weighted average of the parameters from all clients. The performance of these algorithms are verified on a logistic regression language model using Google+ data to determine whether a post will receive at least one comment. As logistic regression is a convex problem, the algorithms can be benchmarked against a known optimum. Federated SVRG is shown to outperform gradient descent by converging to the optimum within 30 rounds of communication.
**Algorithm 1** Federated Averaging (FedAvg) algorithm.*C*is the fraction of clients selected to participate in each communication round. The*K*clients are indexed by*k*; *B*is the local mini-batch size, P^k^ is the dataset available to client*k*, *E*is the number of local epochs, and η is the learning rate

| 1: | procedure FedAvg | Run on server |
|---|---|---|
| 2: | Initialise w0 | |
| 3: | for each round t = 1, 2, do | |
| 4: | m ← max | |
| 5: | (C · K, 1) St ← (random set of m clients) | |
| 6: | for each client k ∈ St do | In parallel |
| 7: | wk^t+1^ ← ClientUpdate(k, wt ) | |
| 8: | end for | |
| 9: | wt+1 ← (∑^K^^k=1^ nk wk^t+1^)/n | |
| 10: | end for | |
| 11: | end procedure | |
| | | |
| 12: | procedure ClientUpdate(k, w) | Run on client k |
| 13: | B ← (Split Pk into mini-batches of size B) | |
| 14: | for each local epoch i from 1 to E do | |
| 15: | for batch b ∈ B do | |
| 16: | w ← w − η∇L(w; b) | |
| 17: | end for | |
| 18: | end for | |
| 19: | return w to server | |
| 20: | end procedure | |

Federated learning (as described in [[9]](#ref-9) simplifies the federated SVRG approach in [[33]](#ref-33) by modifying SGD for the federated setting. McMahan et al. [[9]](#ref-9) provide two distributed SGD scenarios for their experiments: FedSGD and FedAvg. FedSGD performs a single step of gradient descent on all the clients and averages the gradients on the server. The FedAvg algorithm (shown in algorithm [1](#algorithm-1)) randomly selects a fraction of the clients to participate in each round of training. Each client*k*computes the gradients on the current state of the global model w^t^ and updates the parameters w^k^^t+1^ in the standard fashion in gradient descent:

$$
\forall k, w_{t+1}^k \leftarrow w_t - \eta \nabla f(w_t). \tag{4}
$$

All clients communicate their updates to the aggregating server, which then calculates a weighted average of the contributions from each client to update the global model:

$$
w_{t+1} \leftarrow \sum_{k=1}^{K} \frac{n_k}{n} w_{t+1}^k.
$$
(5)

Here,*n*^k^ /*n* is the fraction of data available to the client compared to the available data to all participating clients. Clients can perform one or multiple steps of gradient descent before sending weight updates as orchestrated by the federated algorithm. A diagram describing how federated learning proceeds in the FedAvg scenario is provided in [Figure 1](#figure-1)

![This flowchart illustrates a federated learning system. A server randomly selects clients (step 1), sends a global model (step 2), and clients train local models on their data (step 3). Model parameters are sent back to the server (step 4), averaged (step 5), and the global model is updated (step 6). The system is designed to be tolerant of communication failures. Nodes represent servers and clients, and arrows depict data flow.](_page_8_Figure_2.jpeg)
<a id="figure-1"></a>**Figure 1** Schematic diagram showing how communication proceeds between the aggregating server and individual clients according to the FedAvg protocol. This procedure is iterated until the model converges or the model reaches some desired target metric (e.g. elapsed time, accuracy)

Centralised machine learning (and distributed learning in the data center) benefits from training under the assumption that data can be shuffled and is independent and identically distributed (IID). This assumption is generally invalid in federated learning as the training data is decentralised with significantly different distributions and number of samples between participating clients. Training using non-IID data has been shown to converge much more slowly than IID data in a federated learning setting using the MNIST^2^ dataset (for handwritten digit recognition), distributed between clients after having been sorted by the target label [[9]](#ref-9). The overall accuracy achieved by a DNN trained via federated learning can be significantly reduced when trained on highly skewed non-IID data [[35]](#ref-35). Yue et al. [[35]](#ref-35) show that accuracy can be improved by sharing a small subset of non-private data between all the clients in order to reduce the variance between weight updates of the clients involved in each communication round. The FedProx algorithm [[36]](#ref-36) encompasses FedAvg as a special case and adds a regularising term to the local optimisation objective. This has the effect of limiting the distance between the local model and global model during each communication round and stabilises training overall. Karimireddy et al [[37]](#ref-37) takes a similar approach using SCAFFOLD by accounting for client drift (the estimated difference between the global and local model directions) and corrects for this in the model update step. This can be understood as a variance reduction

^2^ http://yann.lecun.com/exdb/mnist/

method and significantly outperforms FedAvg by reducing the number of rounds of communication and improving the final model accuracy on highly skewed non-IID data.

| Ref Research focus | Year Major contribution |
|---|---|
| [[33]](#ref-33) Optimisation | 2016 First description of federated optimisation and its application to a convex problem (logistic regression) |
| [[9]](#ref-9) Optimisation | 2016 Description of federated averaging (FedAvg) algorithm to improve the performance of the global model and reduce communication between the clients and server |
| [[38]](#ref-38) Communication | 2016 Methods for compressing weight updates and reducing the bandwidth required to perform federated learning |
| [[39]](#ref-39) Multi-task FL | 2017 Application of multi-task learning in a federated setting and discussion of system challenges relevant to using federated learning on resource-constrained devices |
| [[40]](#ref-40) FL attacks | 2018 A demonstration of poisoning the shared global model in a federated learning setting |
| [[41]](#ref-41) FL attacks | 2018 A method to recognise adversarial clients and combat model poisoning in a federated learning setting |
| [[42]](#ref-42) Application | 2018 Application of federated learning in a commercial setting (next word keyborard prediction in Android Gboard) |
| [[43]](#ref-43) Optimisation | 2018 Application of per-coordinate averaging (based on Adam) to federated learning to achieve faster convergence (in fewer communication rounds) |
| [[44]](#ref-44) Application | 2018 Applied federated learning to a healthcare application including further training after federated learning on client data (transfer learning) |
| [[45]](#ref-45) Client selection | 2018 A method of federated learning selecting clients with faster communication/greater resources to participate in each communication round achieving faster convergence |
| [[12]](#ref-12) Communication | 2018 Description of adaptive federated learning method suitable for deployment on resource-constrained devices to optimally learn a shared model while maintaining a fixed energy budget |
| [[35]](#ref-35) Non-IID | 2018 Characterisation of how non-IID data reduces the model performance of federated learning and method for improving model performance |
| [[36]](#ref-36) Optimisation | 2018 Adds a tunable regularising term to FedAvg to stabilise training on skewed, non-IID data, limiting the influence of client models on the global model. |
| [[46]](#ref-46) Multi-task FL | 2019 Training pluralistic models that are tailored to subsets of clients that belong to the same timezones |
| [[37]](#ref-37) Optimisation | 2020 Applies a variance reduction method for improving convergence speed on non-IID data compared to FedAvg |
**Table 1** A summary of important contributions to federated learning research

## 3.2 Multi-task federated learning

A different approach to federating optimisation over many nodes is proposed by Smith et al. [[39]](#ref-39). In this work, each client's data distribution is modelled as a single task as part of a multi-task learning objective. In multi-task learning, all tasks are assumed to be similar and therefore each task can benefit from learning derived from all the other tasks. On three different problems (based on human activity recognition and computer vision), the federated multi-task learning setting outperforms a centralised global setting and a strictly localised setting with lower average prediction errors. As part of this work [[39]](#ref-39), the authors also show that federated multi-task learning is robust to nodes temporarily dropping out during learning and when communication is reduced (by simulating more iterations on the client per communication round). Eichner et al. [[46]](#ref-46) propose a pluralistic approach to tackle the issue of training only when devices are available (generally overnight for mobile phones). Multiple models are trained according to the timezone when the device is available and results in better language models targeted at each timezone. To specifically tackle the issue to model degredation due to the presence of non-IID data [[35]](#ref-35), Sattler et al. [[47]](#ref-47) propose splitting the shared model by determining the cosine similarity of updates from different clients during training. Similarly, Briggs et al. [[48]](#ref-48) use a hierarchical clustering algorithm to judge client update similarity to produce models tailored to clients with similarly-distributed data.

## 3.3 Applied federated learning

Federated learning is particularly well suited as a solution for distributed learning in the IoT setting. As such, federated learning research is flourishing in various applications associated with the IoT. Federated learning has been applied in robotics to aid multiple robots to share imitation learning strategies [[49]](#ref-49) and more generally for protecting privacy-sensitive robotics tasks [[50]](#ref-50). In mobile edge computing environments, federated learning has been demonstrated for predicting demand in edge deployed applications [[51]](#ref-51) and for improving proactive edge content caching mechanisms [[52]](#ref-52). For vehicular edge computing, Lu et al. [[53]](#ref-53) propose a framework to tackle issues of intermittent vehicle connectivity and an untrusted aggregating entity and Ye et al. [[54]](#ref-54) propose a system using federated learning for intelligent connected vehicle image classification tasks. Energy demand in electrical vehicle charging networks has also been addressed with a federated learning strategy by Saputra et al. [[55]](#ref-55). For anomaly detection in IoT environments, federated learning has been applied to detect intrusions and attacks by Nguyen et al. [[56]](#ref-56). More novel applications of federated learning include learning to detect jamming in drone networks [[57]](#ref-57), predicting breaks in presence by users of virtual reality environments [[58]](#ref-58) and human activity recognition using wearable devices [[59]](#ref-59).

For supervised problems, user data needs to be labelled by the user to be useful for training. This is demonstrated in [[42]](#ref-42) where a long short-term memory neural network (LSTM) is trained via many clients on words typed on a mobile keyboard to predict the next word. However, this data is clearly highly sensitive and should not be sent to a central server directly and would benefit from training via federated learning. The training data for this model is automatically labelled when the user types the next word. In cases where data is stored locally and already labelled such as medical health records, privacy is of great concern and even sharing of data between hospitals may be prohibited [[60]](#ref-60). Federated learning can be applied in these settings to improve a shared global model that is more accurate than a model trained by each hospital separately. In [[44]](#ref-44), electronic health records from 58 hospitals are used to train a simple neural network in a federated setting to predict patient mortality. The authors found that partially training the network using federated learning, followed by freezing the first layer and training only on the data available to each client resulted in better performing models for each hospital.

## 3.4 Federated learning attacks

Due to the nature of distributed client participation required for federated learning, the protocol is susceptible to adversarial attacks. Multiple works [[40]](#ref-40), [[61]](#ref-61) present methods for poisoning the global model with an adversary acting as a client in the federated learning setting. The adversary constructs an update such that it survives the averaging procedure and heavily influences or replaces the global model. In this way, an adversary can poison the model to return predictions specified by the attacker given certain input features. Fung et al. [[41]](#ref-41) describe a method to defend against sybilbased adversarial attacks by measuring the similarity between client contributions during model averaging and filtering attacker's updates out. These kinds of attacks might be inadvertently mitigated against using some of the modifications to FedAvg outlined above (for example by FedProx [[36]](#ref-36) or SCAFFOLD [[37]](#ref-37)) to limit the effect of individual client updates.

## 3.5 Communication-efficient federated learning

As highlighted above, distributed learning and federated learning in particular suffer from high latency between communication rounds. Additionally, given a sufficiently large DNN, the number of parameters that need to be communicated in each communication round from possibly many thousands of clients becomes problematic in relation to data transmission and traffic arriving at the aggregating server. There are several approaches to mitigating these issues as discussed in this subsection.

The simplest method to reduce bandwidth use in communicating model updates is simply to communicate less often. In [[9]](#ref-9), researchers experimented with the minibatch size and number of epochs while training a convolutional neural network (CNN) on the MNIST dataset as well as an LSTM trained on the complete works of William Shakespeare^3^ to predict the next text character after some input of characters. Using FedAvg, the authors [[9]](#ref-9) showed that increasing computation on the client between communication rounds significantly reduced the number of communication rounds required to converge to a threshold test accuracy compared to a single epoch trained on all available data on the client (a single iteration of gradient descent). The greatest reduction in communication rounds was achieved using a mini-batch size of 10 and 20 epochs on the client using the CNN model (34.8x) and mini-batch size of 10 and 5 epochs using the LSTM model (95.3x). As this method completely eliminates many of the communication rounds, it should be preferred over (or combined with) the compression methods discussed next.

As the network connection used to communicate between the clients and the aggregating server is generally asymmetric (download speed is generally significantly faster than upload speed), downloading the updated model from the aggregating server is less of a concern than uploading the updates from the clients. Despite this, compression methods exist to reduce the size of deep learning models themselves [[62]](#ref-62), [[63]](#ref-63).

The compression of the parameter updates on the client prior to transmission is important to reduce the size of the overall update but should still maintain a stable statistical mean when updates from all clients are averaged in the global shared model. The following compression methods are not specific to federated learning but have been experimented with in several works related to federated learning.

The individual weights that represent the parameters of a DNN are generally encoded using a 32-bit floating point number. Multiple works explore the effect of lossy compression of the weights (or gradients) to 16-bit [[64]](#ref-64), 8-bit [[65]](#ref-65), or even 1-bit [[66]](#ref-66) employing stochastic rounding to maintain the expected value. The results of these experiments show that as long as the quantisation error is carried forward between mini-batch computations, the overall accuracy of the model isn't significantly impacted.

Another method to compress the weight matrix itself is to convert the matrix from a dense representation to a sparse one. This can be achieved by applying a random mask to the matrix and only communicating the resulting non-zeros values along with the seed used to generate the random mask [[38]](#ref-38). Using this approach combined with FedAvg on the CIFAR-10^4^ image recognition dataset, it has been shown [[38]](#ref-38) that neither the rate of convergence nor the overall test accuracy is significantly impacted, even when only 6.25% of the weights are transmitted during each communication round. Also described in [[38]](#ref-38) is a matrix factorization method whereby the weight matrix is approximated by the product of a randomly generated matrix,*A*and another matrix optimised during training,*B*. Only the matrix *B*(plus the random seed to generate A) needs to be transmitted in each communication round. The authors show however that this method performs significantly worse than the random mask method as the compression ratio is increased.

^3^ https://www.gutenberg.org/ebooks/100

^4^ https://www.cs.toronto.edu/~kriz/cifar.html

Shokri & Shmatikov [[11]](#ref-11) propose an alternative sparsification method implemented in their "Selective SGD" (SSGD) procedure. This method transfers only a fraction of randomly selected weights to each client from the global shared model and only shares a fraction of updated weights back to the aggregating service. The updated weights selected to be communicated are determined by either weight size (largest unsigned magnitude updates) or a random subset of values above a certain threshold. The authors [[11]](#ref-11) show that a CNN trained on the MNIST and Street View House Numbers (SVHN)^5^ datasets can achieve similar levels of accuracy sharing only 10% of the updated weights and only a slight drop (1-2%) in accuracy by sharing only 1% of the updated weights. The paper also shows that the greater the number of users participating in SSGD, the greater the overall accuracy.

Hardy et al. [[67]](#ref-67) take a similar approach to selective SGD but select the largest gradients in each layer rather than the whole weight matrix to better reflect changes throughout the DNN. Their algorithm, "AdaComp" also uses an adaptive learning rate per parameter based on the staleness of the parameter to improve overall test accuracy on the MNIST dataset using a CNN. Most recently, Lin et al. [[68]](#ref-68) apply gradient sparsification along with gradient clipping and momentum correction during training to reduce communication bandwidth by 270x and 600x without a significant drop in prediction performance on various ML problems in computer vision, language modelling and speech recognition.

Leroy et al. [[43]](#ref-43) experiment with using moment-based averaging inspired by the Adam optimisation procedure, in place of a standard weighted global average in FedAvg. The authors train a CNN to detect a "wake word" (similar to "Hey Siri" to initialise the Siri program on iOS devices). The moment-based averaging method acheives a target recall of almost 95% within 100 rounds of communication over 1400 clients compared to only 30% using global averaging.

By selecting clients based on client resource constraints in a mobile edge computing environment, Nishio & Yonetani [[45]](#ref-45) show that federated learning can be sped up considerably. As federated learning proceeds in a synchronous fashion, the slowest communicating node is a limiting factor in the speed at which training can progress. In this work [[45]](#ref-45), target accuracies on the CIFAR-10 and Fashion-MNIST^6^ datasets are achieved in significantly less time than by using the FedAvg algorithm in [[9]](#ref-9). In a similar vein, Wang et al. [[12]](#ref-12), aim to take into account client resources during federated learning training. In this work an algorithm is designed to control the tradeoff between local gradient updates and global averaging in order to optimally minimise the loss function under a fixed energy budget - an important problem for federated learning in the IoT (especially for battery-powered devices).

^5^ http://ufldl.stanford.edu/housenumbers/

^6^ https://www.kaggle.com/zalando-research/fashionmnist

## <a id="section-4"></a>4 Privacy preservation

Data collection for the purpose of learning something about a population (for example in machine learning to discover a function for mapping the data to target labels) can expose sensitive information about individual users. In machine learning, this is often not the primary concern of the developer or researcher creating the model, yet is extremely important for circumstances where personally sensitive data is collected and disseminated in some form (e.g. via a trained model). Privacy has become even more important in the age of big data (data which is characterised by its large volume, variety and velocity [[69]](#ref-69)). As businesses gather increasing amounts of data about users, the risk of privacy breaches via controlled data releases grows.

This review focuses on the protection of an individual's privacy via controlled data releases (such as from personal data used to train a machine learning model) and does not consider privacy breaches via hacking and theft which is a separate issue related to data security.

Privacy is upheld as a human right in many countries via Article 12 of the Universal Declaration of Human Rights [[70]](#ref-70), Article 17 of the International Covenant on civil and political rights [[71]](#ref-71), and Article 8 of the European Convention on Human Rights [[72]](#ref-72). In Europe rigorous legislation with respect to data protection via the General Data Protection Regulation [[73]](#ref-73) safeguards data privacy such that users are given the facts about how and what data is collected about them and how it used and by whom. Despite these rights and regulations, data privacy is difficult to maintain and breaches of privacy via controlled data releases occur often.

Privacy can be preserved in a number of ways, yet it is important to maintain a balance between the level of privacy and utility of the data (along with some consideration for the computational complexity required to preserve privacy). A privacy mechanism augments the original data in order to prevent a breach of personal privacy (i.e. an individual should not be able to be recognised in the data). For example, a privacy mechanism might use noise to augment the result of a query on the data [[74]](#ref-74). Adding too much noise to a result might render it meaningless and adding too little noise might leak sensitive information. The privacy/utility tradeoff is a primary concern of the privacy mechanisms to be discussed in the next subsection.

## 4.1 Privacy preserving methods

The privacy preserving methods discussed in this section can be described as either*suppressive*or*perturbative*[[75]](#ref-75). Suppressive methods include removal of attributes in the data, restricting queries via the privacy mechanism, aggregation/generalisation of data attributes and returning a sampled version of the original data. Perturbative methods include noise addition to the result of a query on the data or rounding of values in the dataset.

## 4.1.1 Anonymisation

Anonymisation or de-identification is achieved by removing any information that might identify an individual within a dataset. Ad-hoc anonymisation might reasonably remove names, addresses, phone numbers etc and replace each user's record(s) with a pseudonym value to act as an identifier under the assumption that individuals cannot be identified within the altered dataset. However, this leaves the data open to privacy attacks known as linkage attacks [[75]](#ref-75). In the presence of auxiliary information, linkage attacks allow an adversary to re-identify individuals in the otherwise anonymous dataset.

Several famous examples of such linkage attacks exist. An MIT graduate, Latanya Sweeney, purchased voter registration records for the town of Cambridge, Massachusetts and was able to use combinations of attributes (ZIP code, gender and date of birth) known as a*quasi-identifier*to identify the then governor of Massachusetts, William Weld. When combined with state-released anonymised medical records, Sweeney was able to identify his medical information from the data release [[76]](#ref-76). As part of a machine learning competition known as the Netflix Prize^7^ launched in 2006, Netflix released a random sample of pseudo-anonymised movie rating data. Narayanan & Shmatikov [[77]](#ref-77) were able to show that using relatively few publicly published ratings by IMDb^8^, all the ratings in the Netflix data for the same user could be revealed. Lastly, in 2014, celebrities in New York were able to be tracked by combining taxi route data released via freedom of information requests, a de-hashing of the taxi license numbers (which were based on md5) and with geo-tagged photos of the celebrities entering/exiting certain taxies [[78]](#ref-78).
*k*-anonymity was proposed by Sweeney [[79]](#ref-79) to tackle the challenge of linkage attacks on anonymised datasets. Using *k*-anonymity, data is suppressed such that *k*−1 or more individuals possess the same attributes used to create a quasi-identifier. Therefore, an identifiable record in a auxiliary dataset would link to multiple records in the anonymous dataset. However*k*-anonymity cannot defend against linkage attacks where a sensitive attribute is shared among a group of individuals with the same quasi-identifier. *l*-diversity builds on *k*-anonymity to ensure that there is diversity within any group of individuals sharing the same quasi-identifier [[80]](#ref-80). *t*-closeness builds on both these methods to preserve the distribution of sensitive attributes among any group of individuals sharing the same quasi-identifier [[81]](#ref-81). All the methods suffer however when an adversary possesses some knowledge about the sensitive attribute. Research related to improving *k*-anonymity based methods has mostly been abandoned in the literature in preference of methods that offer more rigorous privacy guarantees (such as [differential privacy](#section-4-1-3))

^7^ https://www.netflixprize.com/index.html

^8^ https://www.imdb.com/

### 4.1.2 Encryption

Anonymisation presents several difficult challenges in order to provide statistics about data without disclosing sensitive information. Encrypting data provides better privacy protection but the ability to perform useful statistical analysis on encrypted data requires specialist methods. Homomorphic encryption [[82]](#ref-82) allows for processing of data in its encrypted form. Earlier efforts (termed "Somewhat Homomorphic Encryption") allowed for simple addition and multiplication operations on encrypted data [[83]](#ref-83), but were shortly followed by Fully Homomorphic Encryption allowing for any arbitrary function to be applied to data in ciphertext form to yield an encrypted result [[82]](#ref-82).

Despite the apparent advantages of homomorphic encryption to provide privacy to individuals over their data whilst allowing a third party to perform analytics on it, the computational overhead required to perform such operations is very large [[84]](#ref-84), [[85]](#ref-85). IBM's homomorphic library implementation^9^ runs some 50 million times slower than performing calculations on plaintext data [[86]](#ref-86). Due to this computational overhead, applying homomorphic encryption to training on large-scale machine learning data is currently impractical [[87]](#ref-87). Several projects make use of homomorphic encryption for inference on encrypted private data [[88]](#ref-88), [[84]](#ref-84)

Secure multi-party computation (SMC) [[89]](#ref-89) can also be adopted to compute a function on private data owned by many parties such that no party learns anything about others' data - only the output of the function. Many SMC protocols are based on Shamir's secret sharing [[90]](#ref-90) which splits data into *n*pieces in such a way that at least*k* pieces are required to reconstruct the original data (*k*−1 pieces reveal nothing about the original data). For example a value*x*is shared with multiple servers (as*^x^A*, *^x^B*...) via an SMC protocol such that the data can only be reconstructed if the shared pieces on *k*servers are known [[91]](#ref-91). Various protocols exist to compute some function over the data held on the different servers via rounds of communication, however the servers involved are assumed to be trustworthy.

### <a id="section-4-1-3"></a>4.1.3 Differential privacy

Differential privacy provides an elegant and rigorous mathematical measure of the level of privacy afforded by a privacy preserving mechanism. A differentially private privacy preserving mechanism acting on very similar datasets will return statistically indistinguishable results. More formally: Given some privacy mechanism*M*that maps inputs from domain*D*to outputs in range*R*, it is "almost" equally likely (by some multiplicative factor ) for any subset of outputs*^S^**⊆**^R^*to occur, regardless of the presence or absence of a single individual in 2 neighbouring datasets*d*and*d*0 drawn from*D*(differing by a single individual) [[74]](#ref-74)

$$
Pr[M(d) \in S] \le e^{\epsilon} Pr[M(d') \in S].
$$
(6)

^9^ https://github.com/shaih/HElib

Here,*d*and*d*0 are interchangeable with the same outcome. This privacy guarantee protects individuals from being identified within the dataset as the result from the mechanism should be essentially the same regardless of whether the individual appeared in the original dataset or not. Differential privacy is an example of a perturbative privacy preserving method, as the privacy guarantee is achieved by the addition of noise to the true output. This noise is commonly drawn from a Laplacian distribution [[74]](#ref-74) but can also be drawn from a exponential distribution [[92]](#ref-92) or via the novel staircase mechanism [[93]](#ref-93) that provides greater utility compared to laplacian noise for the same . The above description of differential privacy is often termed -differential privacy or strict differential privacy.

The amount of noise required to satisfy -differential privacy is governed by and the sensitivity of the statistic function*Q*defined by [[74]](#ref-74):

$$
\Delta Q = \max(||Q(d) - Q(d')||_1). \tag{7}
$$

This maximum is evaluated over all neighbouring datasets in the set*D*differing by a single individual. The output of the mechanism using noise drawn from the Laplacian distribution is then:

$$
M(d) = Q(d) + Laplace\big(0, \frac{\Delta Q}{\epsilon}\big). \tag{8}
$$

A relaxed version of differential privacy known as (, δ)-differential privacy [[94]](#ref-94) provides greater flexibility in designing privacy preserving mechanisms and greater resistance to attacks making use of auxiliary information [[92]](#ref-92):

$$
Pr[M(d) \in S] \le e^{\epsilon} Pr[M(d') \in S] + \delta. \tag{9}
$$

Whereas -differential privacy provides a privacy guarantee even for results with extremely small probabilities, the δ in (, δ)-differential privacy accounts for the small probability that the privacy guarantee of ordinary -differential privacy is broken.

The Gaussian mechanism is commonly used to add noise to satisfy (, δ) differential privacy [[95]](#ref-95), but instead of the L1 norm used in [Equation 7](#equation-7), the noise is scaled to the L2 norm:

$$
\Delta_2 Q = \max(||Q(d) - Q(d')||_2). \tag{10}
$$

The following mechanism then satisfies (, δ)-differential privacy (given , δ ^∈^ (0, ^1^)):

$$
M(d) = Q(d) + \frac{\Delta_2 Q}{\epsilon} \mathcal{N}(0, 2 \ln(1.25/\delta)).
$$
(11)

is additive for multiple queries [[92]](#ref-92) and therefore an -budget should be designed to protect private data when queried multiple times. Practically, this means that any differential privacy based system must keep track of who queries what and how often to ensure that some predefined -budget is not surpassed. In a machine learning setting a method of accounting for the accumulated privacy loss over training iterations [[10]](#ref-10) needs to be employed to maintain an -budget.

Accumulated knowledge as described above is one of the weaknesses of differential privacy to keep sensitive data private [[92]](#ref-92). Another is collusion. If multiple users collude in the querying of the data (sharing the results of queries with one another) the -budget for any single user might be breached. Finally, suppose an -budget is assigned for each individual query; a user making queries on correlated data will use only the budget for each query, yet may be able to gain more information due to the fact that two quantities are correlated (e.g. income and rent). Clearly, large (or large -budgets) introduce greater risk of privacy breaches than small ones but selecting an appropriate is a non-trivial issue. Lee and Clinton [[96]](#ref-96) discuss the means by which might be selected for a given problem but identify that in order to do so, the dataset and the queries on the dataset should be known ahead of time.

Noise addition can be applied in two separate scenarios. Given a trusted data curator, noise can be added to queries on a static dataset, introducing only minimal noise per query. This can be considered as a global privacy setting. Conversely in a local privacy setting, no such trusted curator exits. Local differential privacy applies when noise is added to each sample before collection/aggregation. For example, the randomised response technique [[97]](#ref-97) allow participants to answer a question truthfully or randomly based on the flip of a coin. Each participant therefore has plausible deniability for their answer, yet statistics can still be estimated on the population given enough data (and a fair coin flip). Each individual sample is extremely noisy in the local case due to the high vulnerability of a single sample being leaked, however, aggregated in volume, the noise can be filtered out to an extent to reveal population statistics. Federated learning is another example of where local differential privacy is useful [[98]](#ref-98). Adding noise to the updates during training rounds on local user data prior to aggregation by an untrusted parameter server provides greater privacy to the user and their contributions to a global model (discussed further in [section 5](#section-5))

Limited examples of practical applications using differential privacy exist outside of academia. Apple implemented differential privacy in its iOS 10 operating system for the iPhone [[99]](#ref-99) in order collect statistics on emoji suggestions and safari crash reports [[100]](#ref-100). Google also collect usage statistics for the Chrome internet browser using differential privacy via multiple rounds of the randomised response technique coupled with a bloom filter to encode the domain names of sites a user has visited [[101]](#ref-101). Both these applications use local differential privacy to protect the individual's privacy but rely on large numbers of participating users in order to determine accurate overall statistics.

Future research and applications of differential privacy are likely to focus on improving utility whilst retaining good privacy guarantees in order for greater adoption by the IT industry.

## <a id="section-5"></a>5 Privacy preservation in federated learning

Federated learning already increases the level of privacy afforded to an individual over traditional machine learning on a static dataset. It mitigates the storage of sensitive personal data by a third party and prevents a third party from performing learning tasks on the data for which the individual had not initially given permission. Additionally, inference does not require that further sensitive data be sent to a third party as the global model is available to the individual on their own private device [[11]](#ref-11). Despite these privacy improvements, the weight/gradient updates uploaded by individuals may reveal information about the user's data, especially if certain weights in the weight matrix are sensitive to specific features or values in the individual's data (for example, specific words in a language prediction model [[102]](#ref-102)). These updates are available to any client participating in federated learning as well as the aggregating server.

Bonawitz et al. [[103]](#ref-103) show that devices participating in federated learning can also act as parties involved in SMC to protect the privacy of all user's updates. In their "Secure Aggregation" protocol, the aggregating server only learns about client updates in aggregate. Similarly, the ∝MDL protocol described in [[105]](#ref-105) uses SMC but also encrypts the gradients on the client using homomorphic encryption. The summation of the encrypted gradients over all participating clients gives an encrypted global gradient, however this summation result can only be decrypted once a threshold number of clients have shared their gradients. Therefore, again, the server can only learn about client updates in aggregate, preserving the privacy of individual contributions.

Researchers at Google have recently described the high-level design of a production-ready federated learning framework^10^ based on Tensorflow. This framework includes Secure Aggregation [[103]](#ref-103) as an option during training.

Applying SMC to federated learning suffers from increased communication and greater computational complexity in the aggregation process (both for the client and the server). Additionally, the fully trained model available to clients after the federated learning procedure may still leak sensitive data about specific individuals as described earlier. Adversarial attacks on federated learning models can be mitigated by inspecting and filtering out malicious client updates [[41]](#ref-41). However, the Secure Aggregation protocol [[103]](#ref-103) prevents the inspection of individual updates and therefore cannot defend against such poisoning attacks [[40]](#ref-40) in this way.

While SMC achieves privacy through increased computational complexity, differential privacy trades off model utility for increased privacy. Additionally, differential privacy protects individual's contributions to the model during training and once the model is fully trained. Differential privacy has been applied in multiple cases to mitigate the issue of publishing sensitive weight updates during communication rounds in a federated learning setting. Shokri & Shmatikov [[11]](#ref-11) describe a communicationefficient method for federated learning of a deep learning model tested on the MNIST and SVHN datasets. They select only a fraction of the local gradient updates to share

^10^ https://www.tensorflow.org/

**Table 2** A summary of important contributions to federated learning research with a focus on privacy enhancing mechanisms (DP = Differential privacy, HE = Homomorphic encryption, SMC = Secure multi-party computation)

| Ref Year | Major contribution | Privacy mechanism | Privacy details |
|---|---|---|---|
| [[11]](#ref-11) 2015 | Description of a selective distibuted gradient descent method to reduce communication and the application of differential privacy to protect the model parameter updates | DP | Batch-level DP, -DP (Laplace mechanism) |
| [[10]](#ref-10) 2016 | Description of an efficient accounting method for accumulating privacy losses while training a DNN with differential privacy | DP | Batch-level DP, ( - )-DP δ (Gaussian mechanism) |
| [[103]](#ref-103) 2017 | New method to provide secure multi-party computation specifically tailored towards federated learning | SMC | Secure aggregation protocol evaluates the average gradients of clients only when a sufficient number send updates |
| [[98]](#ref-98) 2017 | Method for providing user-level differential privacy for federated learning with only small loss in model utility | DP | User-level DP, ( - )-DP δ (Gaussian mechanism) |
| [[102]](#ref-102) 2017 | Method for providing user-level differential privacy for federated learning without degrading model utility | DP | User-level DP, ( - )-DP δ (Gaussian mechanism) |
| [[104]](#ref-104) 2017 | Demonstration of an attack method on the global model using a generative adversarial network, effective even against record/batch-level DP | DP | Attack tested against record/batch-level DP (implemented using [[11]](#ref-11)) |
| [[105]](#ref-105) 2017 | Method for encrypting user updates during distributed training, decryptable only when many clients have participated in the distributed learning objective | HE, SMC | Gradient updates are encrypted using homomorphic encryption. Aggregate server obtains average gradient over all workers but can only decrypt this result once a certain number of updates have been aggregated |
| [[106]](#ref-106) 2019 | Description of a full-scale production-ready federated learning system (focusing on mobile devices) | SMC | Optionally makes use of the Secure aggregation protocol in [[103]](#ref-103) |

with a central server but also experiment with adding noise to the updates to satisfy differential privacy and protect the contributions of individuals to the global model. An -budget is divided and spent on selecting gradients above a certain threshold and on publishing the gradients. Judging the sensitivity of SGD is achieved by bounding the gradients between [−γ, γ] (γ is set to some small number). Laplacian noise is generated using this sensitivity and added to the updates prior to selection/publishing. The authors show that their differentially private method outperforms standalone training (training performed by each client on their own data alone) and approaches the performance of SGD on a non-private static dataset given that enough clients participate in each communication round.

Abadi et al. [[10]](#ref-10) apply a differentially private SGD mechanism to train on the MNIST and CIFAR-10 image datasets. They show they can acheive 97% accuracy on MNIST (1.3% worse than non-differentially private baseline) and 73% accuracy on CIFAR-10 (7% worse than non-differentially private baseline) using a modest neural network and principle component analysis to reduce the dimensionality of the input space. This is achieved using an (, δ)-differential privacy of (8, ^10^−^5^ ). The authors also introduce a privacy accountant to monitor the accumulated privacy loss over all training operations based on moments of the privacy loss random variable. The authors point out that the privacy loss is minimal for such a large number of parameters and training examples.

Geyer et al. [[98]](#ref-98) make use of the moments privacy accountant from [[10]](#ref-10) and evaluate the accumulated δ during training. Once the accumulated δ reaches a given threshold, training is halted. Intuitively, training is halted once the risk of the privacy guarantee being broken becomes too probable. This method of federated learning protects the privacy of an individual's participation in training over their entire local dataset as opposed to a single data point during training as in [[10]](#ref-10). The authors show that with a sufficiently large number of clients participating in the federated optimisation, only a minor drop in performance is recorded whilst maintaining a good level of privacy over the individual's data. Similarly, McMahan et al. [[102]](#ref-102) apply user-level differential privacy (noise is added using sensitivity measured at the user-level rather than sample or mini-batch level) via the moments privacy accountant introduced in [[10]](#ref-10).

A method for attacking deep learning models trained via federated learning has been proposed in [[104]](#ref-104). This approach involves a malicious user participating in federated training whose alternative objective is to train a generative adversarial network (GAN) to generate realistic examples from the globally shared model during training. The authors show that even a model trained with differentially private updates is susceptible to the attack but that it could be defended against with userlevel or device-level differential privacy such as that which is described in [[98]](#ref-98) and [[102]](#ref-102).

An alternative method to perform machine learning on private data is via a knowledge distillation-like approach. Private Aggregation of Teacher Ensembles (PATE) [[107]](#ref-107) trains a student model (which is published and used for inference) using many teacher models in an ensemble. Neither the sensitive data available to the teacher models, nor the teacher models themselves are ever published. The teacher models once trained on the sensitive data are then used to label public data in a semi-supervised fashion via voting for the predicted class. The votes cast by the teachers have noise generated via a Laplacian distribution added to preserve the privacy of their predictions. This approach requires that public data is available to train the student model, however shows better performance than [[10]](#ref-10) and [[11]](#ref-11) whilst maintaining privacy guarantees ((, δ)-differential privacy of (2.04, ^10^−^5^ ) and (8.19, 10−^6^ ) on the MINST and SVHN datasets respectively). Further improvements to PATE show that the method can scale to large multi-class problems [[108]](#ref-108).

## <a id="section-6"></a>6 Challenges in applying privacy-preserving federated learning to the IoT

In this section, we identify and outline some promising areas to develop privacypreserving federated learning research, particularly focused on IoT environments.

## 6.1 Optimal model architecture/hyperparameters

Federated learning precludes seeing the data that a model is trained on. On a traditionally centralised dataset, a deep learning architecture and hyperparameters can be selected via a validation strategy. However to follow the same approach in federated learning to find an optimal architecture or set the optimal hyperparameters to produce good models would require training many models on user devices (possibly incurring unacceptable amounts of battery power and bandwidth). Therefore novel research is required to tackle this specific problem, unique to federated learning.

## 6.2 Continual learning

Training a machine learning model is an expensive and time-consuming task and this can be significantly worse in the federated learning setting. As data distributions evolve over time, a trained model's performance deteriorates. To avoid the cost of federated training many times over, research into methods for improving how a model learns is congruent to the federated learning objective over time. Methods such as meta-learning, online learning and continual learning will be important here which will have specific challenges unique to the distributed nature of federated learning.

## 6.3 Better privacy preserving methods

As seen in this review, there is an observable tradeoff between the performance of a model and the privacy that is afforded to a user. Further research is ongoing into differential privacy accounting methods that introduce less noise into the model (thus improving utility) for the same level of privacy (as judged by the parameter). Likewise, further research is required to vastly reduce the computational burden of methods such as homomorphic encryption and secure multi-party computation in order for them to become common-use methods for preserving privacy for large-scale machine learning tasks.

## 6.4 Federated learning combined with fog computing

Reducing the latency between rounds of training in federated learning is desirable to train models quickly. Fog computing nodes could feasibly be leveraged as aggregating servers to remove the round-trip communication between clients and cloud servers in the aggregation step of federated learning. Fog computing could also bring other benefits, such as sharing the computational burden by hierarchically aggregating many large client models.

## 6.5 Federated learning on low power devices

Training deep networks on resource constrained and low power devices poses specific challenges for federated learning. Much of the research into federated learning focusses on mobile devices such as smartphones with abundant compute, storage and power capabilities. As such, new methods are required for reducing the amount of work individual devices need to do to contribute to training (perhaps using the model parallelism approach seen in [[13]](#ref-13) or training only certain deep network layers on subsets of devices.)

## <a id="section-7"></a>7 Conclusion

Deep learning has shown impressive successes in the fields of computer vision, speech recognition and language modelling. With the exploding increase in deployments of IoT devices, naturally, deep learning is starting to be applied at the edge of the network on mobile and resource-limited embedded devices. This environment however presents difficult challenges for training deep models due to their energy, compute and memory requirements. Beyond this, a model's utility is strictly limited to the data available to the edge device. Allowing machines close to the edge of the

network to train on data produced by edge devices (as in fog computing) risks privacy breaches of such data. Federated learning has been shown to be a good solution to improve deep learning models while maintaining the privacy of the raw data.

Federated learning presents a new field of research but has great potential for improving the privacy of training data and giving users control of how their data is used by third parties. Combining federated learning with privacy mechanisms such as differential privacy further secures user data from adversaries with the inclination and means to reverse-engineer parameter updates in distributed SGD procedures. Differential privacy as applied to machine learning is also in its infancy and challenges remain to provide good privacy guarantees whilst simultaneously limiting the required communication costs in a federated setting.

The intersection of federated learning, differential privacy and IoT data represents a fruitful area of research. Performing deep learning efficiently on resourceconstrained devices while preserving privacy and utility poses a real challenge. Additionally, the nature of IoT data as opposed to internet data for private federated learning deserves more attention from the research community. IoT data is often represented by highly skewed non-IID data with high temporal variability. This is a challenge that needs to be overcome for federated learning to flourish in edge environments.

## Acknowledgements

This work is partly supported by the SEND project (grant ref. 32R16P00706) funded by ERDF and BEIS.

## References

- <a id="ref-1"></a>1. Gartner. (2018, Nov.) Gartner Identifies Top 10 Strategic IoT Technologies and Trends. [Online]. Available: [https://www.gartner.com/en/newsroom/press-releases/2018-11-07-gartner-identifies-top-10-strategic-iot-technologies-and-trends](https://www.gartner.com/en/newsroom/press-releases/2018-11-07-gartner-identifies-top-10-strategic-iot-technologies-and-trends)
- <a id="ref-2"></a>2. F. Bonomi, R. Milito, J. Zhu, and S. Addepalli, "Fog computing and its role in the internet of things," in *SIGCOMM 2012 MCC workshop*. New York, New York, USA: ACM, Aug. 2012, pp. 13–16.
- <a id="ref-3"></a>3. Y. Ai, M. Peng, and K. Zhang, "Edge computing technologies for Internet of Things: a primer," *Digital Communications and Networks*, vol. 4, no. 2, pp. 77–86, Apr. 2018.
- <a id="ref-4"></a>4. L. Bittencourt, R. Immich, R. Sakellariou, N. Fonseca, E. Madeira, M. Curado, L. Villas, L. DaSilva, C. Lee, and O. Rana, "The Internet of Things, Fog and Cloud continuum: Integration and challenges," *Internet of Things*, vol. 3–4, pp. 134–155, Oct. 2018.
- <a id="ref-5"></a>5. OpenFog Consortium. (2017, Feb.) OpenFog Reference Architecture for Fog Computing . [Online]. Available: [https://www.openfogconsortium.org/wp-content/uploads/OpenFog_Reference_Architecture_2_09_17-FINAL.pdf](https://www.openfogconsortium.org/wp-content/uploads/OpenFog_Reference_Architecture_2_09_17-FINAL.pdf)
- <a id="ref-6"></a>6. F. Bonomi, R. Milito, P. Natarajan, and J. Zhu, "Fog Computing: A Platform for Internet of Things and Analytics," in *Big Data and Internet of Things: A Roadmap for Smart Environments*. Cham: Springer, Cham, 2014, pp. 169–186.

- <a id="ref-7"></a>7. H. Li, K. Ota, and M. Dong, "Learning IoT in Edge: Deep Learning for the Internet of Things with Edge Computing," *IEEE Network*, vol. 32, no. 1, pp. 96–101, 2018.
- <a id="ref-8"></a>8. T. Ben-Nun and T. Hoefler, "Demystifying Parallel and Distributed Deep Learning," *ACM Computing Surveys (CSUR)*, vol. 52, no. 4, pp. 1–43, Sep. 2019.
- <a id="ref-9"></a>9. B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, "Communication-Efficient Learning of Deep Networks from Decentralized Data," in *Artificial Intelligence and Statistics*, 2017, pp. 1273–1282.
- <a id="ref-10"></a>10. M. Abadi, A. Chu, I. Goodfellow, H. B. McMahan, I. Mironov, K. Talwar, and L. Zhang, "Deep Learning with Differential Privacy," in *the 2016 ACM SIGSAC Conference*. ACM, Oct. 2016, pp. 308–318.
- <a id="ref-11"></a>11. R. Shokri and V. Shmatikov, "Privacy-Preserving Deep Learning," in *the 22nd ACM SIGSAC Conference*. ACM, Oct. 2015, pp. 1310–1321.
- <a id="ref-12"></a>12. S. Wang, T. Tuor, T. Salonidis, K. K. Leung, C. Makaya, T. He, and K. Chan, "Adaptive Federated Learning in Resource Constrained Edge Computing Systems," *IEEE Journal on Selected Areas in Communications*, vol. 37, no. 6, pp. 1205–1221, Jun. 2019.
- <a id="ref-13"></a>13. J. Dean, G. S. Corrado, R. Monga, K. Chen, M. Devin, Q. V. Le, M. Z. Mao, M. Ranzato, A. Senior, P. Tucker, K. Yang, and A. Y. Ng, "Large scale distributed deep networks," in *Advances in neural information processing systems*. Curran Associates Inc., Dec. 2012, pp. 1223–1231.
- <a id="ref-14"></a>14. M. Li, D. G. Andersen, J. W. Park, A. J. Smola, and A. Ahmed, "Scaling Distributed Machine Learning with the Parameter Server." *OSDI*, vol. 14, pp. 583–598, 2014.
- <a id="ref-15"></a>15. Y. Lecun, Y. Bengio, and G. E. Hinton, "Deep learning," *Nature*, vol. 521, no. 7, pp. 436–444, May 2015.
- <a id="ref-16"></a>16. I. Goodfellow, Y. Bengio, and A. Courville, *Deep Learning*, 1st ed. Cambridge, Massachusetts: MIT Press, 2016.
- <a id="ref-17"></a>17. D. E. Rumelhart, G. E. Hinton, and R. J. Williams, "Learning internal representations by error propagation," in *Parallel distributed processing explorations in the microstructure of cognition*. Cambridge, Massachusetts: MIT Press, Jan. 1986, pp. 318–362.
- <a id="ref-18"></a>18. A. Krizhevsky, I. Sutskever, and G. E. Hinton, "ImageNet Classification with Deep Convolutional Neural Networks," *Communications of the Acm*, vol. 60, no. 6, pp. 84–90, Jun. 2017.
- <a id="ref-19"></a>19. T. M. Chilimbi, Y. Suzue, J. Apacible, and K. Kalyanaraman, "Project Adam: Building an Efficient and Scalable Deep Learning Training System." in *OSDI*, 2014, pp. 571–582.
- <a id="ref-20"></a>20. B. Recht, C. Ré, S. Wright, and F. Niu, "Hogwild: A Lock-Free Approach to Parallelizing Stochastic Gradient Descent," in *Advances in neural information processing systems*, 2011, pp. 693–701.
- <a id="ref-21"></a>21. Q. Ho, J. Cipar, H. Cui, S. Lee, J. K. Kim, P. B. Gibbons, G. A. Gibson, G. Ganger, and E. P. Xing, "More Effective Distributed ML via a Stale Synchronous Parallel Parameter Server," in *Advances in neural information processing systems*, 2013, pp. 1223–1231.
- <a id="ref-22"></a>22. A. Odena, "Faster Asynchronous SGD," *arXiv.org*, p. arXiv:1601.04033, Jan. 2016.
- <a id="ref-23"></a>23. W. Zhang, S. Gupta, X. Lian, and J. Liu, "Staleness-aware Async-SGD for Distributed Deep Learning," in *Proceedings of the Twenty-Fifth International Joint Conference on Artificial Intelligence*, Nov. 2015, pp. 2350–2356.
- <a id="ref-24"></a>24. K. Hsieh, A. Harlap, N. Vijaykumar, D. Konomis, G. R. Ganger, and P. B. Gibbons, "Gaia: Geo-Distributed Machine Learning Approaching LAN Speeds." in *NSDI*, 2017, pp. 629–647.
- <a id="ref-25"></a>25. J. Jiang, B. Cui, C. Zhang, and L. Yu, "Heterogeneity-aware Distributed Parameter Servers," in *the 2017 ACM International Conference*. New York, New York, USA: ACM Press, 2017, pp. 463–478.
- <a id="ref-26"></a>26. J. Daily, A. Vishnu, C. Siegel, T. Warfel, and V. Amatya, "GossipGraD: Scalable Deep Learning using Gossip Communication based Asynchronous Gradient Descent," *arXiv.org*, p. arXiv:1803.05880, Mar. 2018.
- <a id="ref-27"></a>27. P. H. Jin, Q. Yuan, F. Iandola, and K. Keutzer, "How to scale distributed deep learning?" *arXiv.org*, p. arXiv:1611.04581, Nov. 2016.

- <a id="ref-28"></a>28. S. Sundhar Ram, A. Nedic, and V. V. Veeravalli, "Asynchronous gossip algorithms for stochastic optimization," in *2009 International Conference on Game Theory for Networks (GameNets)*. IEEE, 2009, pp. 80–81.
- <a id="ref-29"></a>29. J. Ba and R. Caruana, "Do Deep Nets Really Need to be Deep?" in *Advances in neural information processing systems*, 2014, pp. 2654–2662.
- <a id="ref-30"></a>30. Y. Chebotar and A. Waters, "Distilling Knowledge from Ensembles of Neural Networks for Speech Recognition," in *Interspeech 2016*. ISCA, Sep. 2016, pp. 3439–3443.
- <a id="ref-31"></a>31. G. E. Hinton, O. Vinyals, and J. Dean, "Distilling the Knowledge in a Neural Network," *arXiv.org*, p. arXiv:1503.02531, Mar. 2015.
- <a id="ref-32"></a>32. Y. Liang, M. F. Balcan, and V. Kanchanapally, "Distributed PCA and k-means clustering," in *The Big Learning Workshop at NIPS*, 2013.
- <a id="ref-33"></a>33. J. Konečný, H. B. McMahan, D. Ramage, and P. Richtárik, "Federated Optimization: Distributed Machine Learning for On-Device Intelligence," *arXiv.org*, p. arXiv:1610.02527, Oct. 2016.
- <a id="ref-34"></a>34. R. Johnson and T. Zhang, "Accelerating Stochastic Gradient Descent Using Predictive Variance Reduction," in *Proceedings of the 26th International Conference on Neural Information Processing Systems - Volume 1*. USA: Curran Associates Inc., 2013, pp. 315–323.
- <a id="ref-35"></a>35. Y. Zhao, M. Li, L. Lai, N. Suda, D. Civin, and V. Chandra, "Federated Learning with Non-IID Data," *arXiv.org*, p. arXiv:1806.00582, Jun. 2018.
- <a id="ref-36"></a>36. I. Dhillon, D. Papailiopoulos, and V. Sze, Eds., *Federated Optimization in Heterogeneous Networks*, 2020.
- <a id="ref-37"></a>37. S. P. Karimireddy, S. Kale, M. Mohri, S. J. Reddi, S. U. Stich, and A. T. Suresh, "Scaffold: Stochastic controlled averaging for federated learning," *arXiv preprint arXiv:1910.06378*, 2020.
- <a id="ref-38"></a>38. J. Konečný, H. B. McMahan, F. X. Yu, P. Richtárik, A. T. Suresh, and D. Bacon, "Federated Learning: Strategies for Improving Communication Efficiency," *arXiv.org*, p. arXiv:1610.05492, Oct. 2016.
- <a id="ref-39"></a>39. V. Smith, C.-K. Chiang, M. Sanjabi, and A. Talwalkar, "Federated Multi-Task Learning," in *Advances in neural information processing systems*, May 2017, p. arXiv:1705.10467.
- <a id="ref-40"></a>40. E. Bagdasaryan, A. Veit, Y. Hua, D. Estrin, and V. Shmatikov, "How To Backdoor Federated Learning," *arXiv.org*, p. arXiv:1807.00459, Jul. 2018.
- <a id="ref-41"></a>41. C. Fung, C. J. M. Yoon, and I. Beschastnikh, "Mitigating Sybils in Federated Learning Poisoning," *arXiv.org*, p. arXiv:1808.04866, Aug. 2018.
- <a id="ref-42"></a>42. A. Hard, K. Rao, R. Mathews, F. Beaufays, S. Augenstein, H. Eichner, C. Kiddon, and D. Ramage, "Federated Learning for Mobile Keyboard Prediction," *arXiv.org*, Nov. 2018.
- <a id="ref-43"></a>43. D. Leroy, A. Coucke, T. Lavril, T. Gisselbrecht, and J. Dureau, "Federated Learning for Keyword Spotting," *arXiv.org*, p. arXiv:1810.05512, Oct. 2018.
- <a id="ref-44"></a>44. D. Liu, T. Miller, R. Sayeed, and K. D. Mandl, "FADL: Federated-Autonomous Deep Learning for Distributed Electronic Health Record," *arXiv.org*, p. arXiv:1811.11400, Nov. 2018.
- <a id="ref-45"></a>45. T. Nishio and R. Yonetani, "Client Selection for Federated Learning with Heterogeneous Resources in Mobile Edge," *arXiv.org*, p. arXiv:1804.08333, Apr. 2018.
- <a id="ref-46"></a>46. H. Eichner, T. Koren, H. B. McMahan, N. Srebro, and K. Talwar, "Semi-Cyclic Stochastic Gradient Descent," in *International Conference on Machine Learning*, Apr. 2019, p. arXiv:1904.10120.
- <a id="ref-47"></a>47. F. Sattler, S. Wiedemann, K.-R. Müller, and W. Samek, "Robust and Communication-Efficient Federated Learning from Non-IID Data," *arXiv.org*, p. arXiv:1903.02891, Mar. 2019.
- <a id="ref-48"></a>48. C. Briggs, Z. Fan, and P. Andras, "Federated learning with hierarchical clustering of local updates to improve training on non-IID data," *arXiv.org*, p. arXiv:2004.11791, Apr. 2020.
- <a id="ref-49"></a>49. B. Liu, L. Wang, M. Liu, and C.-Z. Xu, "Federated Imitation Learning: A Novel Framework for Cloud Robotic Systems With Heterogeneous Sensor Data," *IEEE Robotics and Automation Letters*, vol. 5, no. 2, pp. 3509–3516, Apr. 2020.
- <a id="ref-50"></a>50. W. Zhou, Y. Li, S. Chen, and B. Ding, "Real-Time Data Processing Architecture for Multi-Robots Based on Differential Federated Learning," in *2018 IEEE SmartWorld, Ubiquitous Intelligence & Computing, Advanced & Trusted Computing, Scalable Computing & Communications, Cloud & Big Data Computing, Internet of People and Smart City Innovation (SmartWorld/SCALCOM/UIC/ATC/CBDCom/IOP/SCI)*. IEEE, 2018, pp. 462–471.

- <a id="ref-51"></a>51. R. Fantacci and B. Picano, "Federated learning framework for mobile edge computing networks," *CAAI Transactions on Intelligence Technology*, vol. 5, no. 1, pp. 15–21, Mar. 2020.
- <a id="ref-52"></a>52. Z. Yu, J. Hu, G. Min, H. Lu, Z. Zhao, H. Wang, and N. Georgalas, "Federated Learning Based Proactive Content Caching in Edge Computing," in *GLOBECOM 2018 - 2018 IEEE Global Communications Conference*. IEEE, 2018, pp. 1–6.
- <a id="ref-53"></a>53. Y. Lu, X. Huang, Y. Dai, S. Maharjan, and Y. Zhang, "Differentially Private Asynchronous Federated Learning for Mobile Edge Computing in Urban Informatics," *IEEE Transactions on Industrial Informatics*, vol. 16, no. 3, pp. 2134–2143, 2019.
- <a id="ref-54"></a>54. D. Ye, R. Yu, M. Pan, and Z. Han, "Federated Learning in Vehicular Edge Computing: A Selective Model Aggregation Approach," *IEEE Access*, vol. 8, pp. 23 920–23 935, 2020.
- <a id="ref-55"></a>55. Y. M. Saputra, D. T. Hoang, D. N. Nguyen, E. Dutkiewicz, M. D. Mueck, and S. Srikanteswara, "Energy Demand Prediction with Federated Learning for Electric Vehicle Networks," in *GLOBECOM 2019 - 2019 IEEE Global Communications Conference*. IEEE, 2019, pp. 1–6.
- <a id="ref-56"></a>56. T. D. Nguyen, S. Marchal, M. Miettinen, H. Fereidooni, N. Asokan, and A.-R. Sadeghi, "DÏoT: A Federated Self-learning Anomaly Detection System for IoT," in *2019 IEEE 39th International Conference on Distributed Computing Systems (ICDCS)*. IEEE, 2019, pp. 756–767.
- <a id="ref-57"></a>57. N. I. Mowla, N. H. Tran, I. Doh, and K. Chae, "Federated Learning-Based Cognitive Detection of Jamming Attack in Flying Ad-Hoc Network," *IEEE Access*, vol. 8, pp. 4338–4350, 2020.
- <a id="ref-58"></a>58. M. Chen, O. Semiari, W. Saad, X. Liu, and C. Yin, "Federated Echo State Learning for Minimizing Breaks in Presence in Wireless Virtual Reality Networks," *Ieee Transactions on Wireless Communications*, vol. 19, no. 1, pp. 177–191, Jan. 2020.
- <a id="ref-59"></a>59. K. Sozinov, V. Vlassov, and S. Girdzijauskas, "Human Activity Recognition Using Federated Learning," in *2018 IEEE Intl Conf on Parallel & Distributed Processing with Applications, Ubiquitous Computing & Communications, Big Data & Cloud Computing, Social Computing & Networking, Sustainable Computing & Communications (ISPA/IUCC/BDCloud/SocialCom/SustainCom)*. IEEE, 2018, pp. 1103–1111.
- <a id="ref-60"></a>60. R. Miotto, F. Wang, S. Wang, X. Jiang, and J. T. Dudley, "Deep learning for healthcare: review, opportunities and challenges," *Briefings in Bioinformatics*, vol. 19, no. 6, pp. 1236–1246, May 2017.
- <a id="ref-61"></a>61. *Analyzing Federated Learning through an Adversarial Lens*. PMLR, May 2019.
- <a id="ref-62"></a>62. S. Han, H. Mao, and W. J. Dally, "Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding," *arXiv.org*, p. arXiv:1510.00149, Oct. 2015.
- <a id="ref-63"></a>63. S. Han, J. Pool, J. Tran, and W. Dally, "Learning both Weights and Connections for Efficient Neural Network," in *Advances in neural information processing systems*, 2015, pp. 1135– 1143.
- <a id="ref-64"></a>64. S. Gupta, A. Agrawal, K. Gopalakrishnan, and P. Narayanan, "Deep Learning with Limited Numerical Precision," *arXiv.org*, p. arXiv:1502.02551, Feb. 2015.
- <a id="ref-65"></a>65. T. Dettmers, "8-Bit Approximations for Parallelism in Deep Learning," *arXiv.org*, p. arXiv:1511.04561, Nov. 2015.
- <a id="ref-66"></a>66. F. Seide, H. Fu, J. Droppo, G. Li, and D. Yu, "1-bit stochastic gradient descent and its application to data-parallel distributed training of speech dnns," in *Fifteenth Annual Conference of the International Speech Communication Association*, 2014.
- <a id="ref-67"></a>67. C. Hardy, E. Le Merrer, and B. Sericola, "Distributed deep learning on edge-devices: Feasibility via adaptive compression," in *2017 IEEE 16th International Symposium on Network Computing and Applications (NCA)*. IEEE, pp. 1–8.
- <a id="ref-68"></a>68. Y. Lin, S. Han, H. Mao, Y. Wang, and W. J. Dally, "Deep Gradient Compression: Reducing the Communication Bandwidth for Distributed Training," *arXiv.org*, p. arXiv:1712.01887, Dec. 2017.
- <a id="ref-69"></a>69. A. Gandomi and M. Haider, "Beyond the hype: Big data concepts, methods, and analytics," *International Journal of Information Management*, vol. 35, no. 2, pp. 137–144, Apr. 2015.
- <a id="ref-70"></a>70. UN General Assembly, "Universal Declaration of Human Rights," Oct. 2015.
- <a id="ref-71"></a>71. ——, "International Covenant on Civil and Political Rights," Dec. 1966.

- <a id="ref-72"></a>72. Council of Europe, "European convention for the protection of human rights and fundamental freedoms ," Nov. 1950.
- <a id="ref-73"></a>73. European Commision, "Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (General Data Protection Regulation)," *Official Journal of the European Union*, vol. L119, pp. 1–88, May 2016.
- <a id="ref-74"></a>74. C. Dwork, "Differential Privacy," in *Automata, Languages and Programming*. Berlin, Heidelberg: Springer Berlin Heidelberg, 2006, pp. 1–12.
- <a id="ref-75"></a>75. B. C. M. Fung, K. Wang, R. Chen, and P. S. Yu, "Privacy-preserving data publishing: A survey of recent developments," *ACM Computing Surveys (CSUR)*, vol. 42, no. 4, pp. 14–53, Jun. 2010.
- <a id="ref-76"></a>76. H. T. Greely, "The uneasy ethical and legal underpinnings of large-scale genomic biobanks," *Annual Review of Genomics and Human Genetics*, vol. 8, no. 1, pp. 343–364, 2007.
- <a id="ref-77"></a>77. A. Narayanan and V. Shmatikov, "Robust De-anonymization of Large Sparse Datasets," in *2008 IEEE Symposium on Security and Privacy (sp 2008)*. IEEE, 2008, pp. 111–125.
- <a id="ref-78"></a>78. A. Tockar. (2014, Sep.) Riding with the Stars: Passenger Privacy in the NYC Taxicab Dataset. [Online]. Available: [https://research.neustar.biz/2014/09/15/riding-with-the-stars-passenger-privacy-in-the-nyc-taxicab-dataset/](https://research.neustar.biz/2014/09/15/riding-with-the-stars-passenger-privacy-in-the-nyc-taxicab-dataset/)
- <a id="ref-79"></a>79. L. Sweeney, "K-anonymity: A Model for Protecting Privacy," *Int. J. Uncertain. Fuzziness Knowl.-Based Syst.*, vol. 10, no. 5, pp. 557–570, Oct. 2002.
- <a id="ref-80"></a>80. A. Machanavajjhala, J. Gehrke, D. Kifer, and M. Venkitasubramaniam, "L-diversity: privacy beyond k-anonymity," in *22nd International Conference on Data Engineering*. IEEE, 2006, pp. 24–24.
- <a id="ref-81"></a>81. N. Li, T. Li, and S. Venkatasubramanian, "t-Closeness: Privacy Beyond k-Anonymity and l-Diversity," in *2007 IEEE 23rd International Conference on Data Engineering*. IEEE, 2007, pp. 106–115.
- <a id="ref-82"></a>82. C. Gentry, "Computing arbitrary functions of encrypted data," *Communications of the Acm*, vol. 53, no. 3, pp. 97–105, Mar. 2010.
- <a id="ref-83"></a>83. A. Acar, H. Aksu, A. S. Uluagac, and M. Conti, "A Survey on Homomorphic Encryption Schemes: Theory and Implementation," *ACM Computing Surveys (CSUR)*, vol. 51, no. 4, pp. 79–35, Sep. 2018.
- <a id="ref-84"></a>84. R. Gilad-Bachrach, N. Dowlin, K. Laine, K. Lauter, M. Naehrig, and J. Wernsing, "Cryptonets: Applying neural networks to encrypted data with high throughput and accuracy," in *International Conference on Machine Learning*, 2016, pp. 201–210.
- <a id="ref-85"></a>85. E. Hesamifard, H. Takabi, and M. Ghasemi, "CryptoDL: Deep Neural Networks over Encrypted Data," *arXiv.org*, p. arXiv:1711.05189, Nov. 2017.
- <a id="ref-86"></a>86. L. Rist. (2018, Jan.) Encrypt your Machine Learning. [Online]. Available: [https://medium.com/corti-ai/encrypt-your-machine-learning-12b113c879d6](https://medium.com/corti-ai/encrypt-your-machine-learning-12b113c879d6)
- <a id="ref-87"></a>87. Y. Du, L. Gustafson, D. Huang, and K. Peterson, *Implementing ML Algorithms with HE*. MIT Course 6.857: Computer and Network Security, 2017.
- <a id="ref-88"></a>88. E. Chou, J. Beal, D. Levy, S. Yeung, A. Haque, and L. Fei-Fei, "Faster CryptoNets: Leveraging Sparsity for Real-World Encrypted Inference," *arXiv.org*, p. arXiv:1811.09953, Nov. 2018.
- <a id="ref-89"></a>89. O. Goldreich, "Secure multi-party computation," *Manuscript. Preliminary version*, vol. 78, 1998.
- <a id="ref-90"></a>90. A. Shamir, "How to share a secret," *Communications of the Acm*, vol. 22, no. 11, pp. 612–613, Nov. 1979.
- <a id="ref-91"></a>91. J. Launchbury, D. Archer, T. DuBuisson, and E. Mertens, "Application-Scale Secure Multiparty Computation," in *Programming Languages and Systems*. Berlin, Heidelberg: Springer, Berlin, Heidelberg, Apr. 2014, pp. 8–26.
- <a id="ref-92"></a>92. C. Dwork and A. Roth, "The Algorithmic Foundations of Differential Privacy," *Foundations and Trends in Theoretical Computer Science*, vol. 9, no. 3–4, pp. 211–407, Aug. 2014.
- <a id="ref-93"></a>93. Q. Geng, P. Kairouz, S. Oh, and P. Viswanath, "The Staircase Mechanism in Differential Privacy," *IEEE Journal of Selected Topics in Signal Processing*, vol. 9, no. 7, pp. 1176–1184, Oct. 2015.

- <a id="ref-94"></a>94. S. P. Kasiviswanathan and A. Smith, "On the'semantics' of differential privacy: A bayesian formulation," *Journal of Privacy and Confidentiality*, vol. 6, no. 1, 2014.
- <a id="ref-95"></a>95. T. Zhu, G. Li, W. Zhou, and P. S. Yu, "Preliminary of Differential Privacy," in *Differential Privacy and Applications*. Cham: Springer International Publishing, 2017, pp. 7–16.
- <a id="ref-96"></a>96. J. Lee and C. Clifton, "How Much Is Enough? Choosing ε for Differential Privacy," in *Information Security*. Berlin, Heidelberg: Springer, Berlin, Heidelberg, Oct. 2011, pp. 325–340.
- <a id="ref-97"></a>97. S. L. Warner, "Randomized Response: A Survey Technique for Eliminating Evasive Answer Bias," *Journal of the American Statistical Association*, vol. 60, no. 309, p. 63, Mar. 1965.
- <a id="ref-98"></a>98. R. C. Geyer, T. Klein, and M. Nabi, "Differentially Private Federated Learning: A Client Level Perspective," *arXiv.org*, p. arXiv:1712.07557, Dec. 2017.
- <a id="ref-99"></a>99. Apple. (2017, Nov.) Apple Differential Privacy Technical Overview. [Online]. Available: [https://www.apple.com/privacy/docs/Differential_Privacy_Overview.pdf](https://www.apple.com/privacy/docs/Differential_Privacy_Overview.pdf)
- <a id="ref-100"></a>100. A. G. Thakurta, "Differential Privacy: From Theory to Deployment," in *USENIX Association*. Vancouver, BC: USENIX Association, 2017.
- <a id="ref-101"></a>101. Ú. Erlingsson, V. Pihur, and A. Korolova, "RAPPOR: Randomized Aggregatable Privacy-Preserving Ordinal Response," in *Proceedings of the ACM SIGSAC Conference on Computer and Communications Security*. ACM, Nov. 2014, pp. 1054–1067.
- <a id="ref-102"></a>102. H. B. McMahan, D. Ramage, K. Talwar, and L. Zhang, "Learning Differentially Private Recurrent Language Models," *arXiv.org*, p. arXiv:1710.06963, Oct. 2017.
- <a id="ref-103"></a>103. K. Bonawitz, V. Ivanov, B. Kreuter, A. Marcedone, H. B. McMahan, S. Patel, D. Ramage, A. Segal, and K. Seth, "Practical Secure Aggregation for Privacy-Preserving Machine Learning," in *Proceedings of the ACM SIGSAC Conference on Computer and Communications Security*. ACM, Oct. 2017, pp. 1175–1191.
- <a id="ref-104"></a>104. B. Hitaj, G. Ateniese, and F. Perez-Cruz, "Deep Models Under the GAN," in *the 2017 ACM SIGSAC Conference*. New York, New York, USA: ACM Press, 2017, pp. 603–618.
- <a id="ref-105"></a>105. X. Zhang, S. Ji, H. Wang, and T. Wang, "Private, Yet Practical, Multiparty Deep Learning," in *2017 IEEE 37th International Conference on Distributed Computing Systems (ICDCS)*. IEEE, 2017, pp. 1442–1452.
- <a id="ref-106"></a>106. K. Bonawitz, H. Eichner, W. Grieskamp, D. Huba, A. Ingerman, V. Ivanov, C. Kiddon, J. Konečný, S. Mazzocchi, H. B. McMahan, T. Van Overveldt, D. Petrou, D. Ramage, and J. Roselander, "Towards Federated Learning at Scale: System Design," *arXiv.org*, p. arXiv:1902.01046, Feb. 2019.
- <a id="ref-107"></a>107. N. Papernot, M. Abadi, Ú. Erlingsson, I. Goodfellow, and K. Talwar, "Semi-supervised Knowledge Transfer for Deep Learning from Private Training Data," *arXiv.org*, p. arXiv:1610.05755, Oct. 2016.
- <a id="ref-108"></a>108. N. Papernot, S. Song, I. Mironov, A. Raghunathan, K. Talwar, and Ú. Erlingsson, "Scalable Private Learning with PATE," *arXiv.org*, p. arXiv:1802.08908, Feb. 2018.