---
cite_key: "noise_2024"
title: "DPSUR: Accelerating Differentially Private Stochastic Gradient Descent Using Selective Update and Release"
authors: "adding random noise, we can achieve differential privacy for a function : X → R according to Definition 2.1. The sensitivity determines how much noise is needed, is defined as follow."
year: 2024
doi: "arXiv:2311.14056"
url: "https://arxiv.org/abs/2311.14056"
relevancy: "High"
tldr: "Novel differentially private training framework using selective gradient updates to improve convergence speed and model utility while maintaining privacy guarantees through strategic update filtering and threshold mechanisms."
insights: "Proposes differentially private training framework with selective updates that evaluates gradient quality and applies only convergence-leading updates, achieving faster convergence and improved model utility compared to traditional DPSGD while maintaining privacy guarantees."
summary: "This paper addresses utility loss problems in differentially private stochastic gradient descent (DPSGD) by proposing DPSUR, a framework that applies selective updates based on validation tests. The approach evaluates each gradient iteration and only applies updates that lead to convergence, discarding harmful or useless updates. The method introduces clipping strategies for update randomization and threshold mechanisms for gradient selection to ensure training proceeds in the right direction."
research_question: "How can differentially private machine learning training be accelerated while maintaining privacy guarantees by selectively applying only beneficial gradient updates?"
methodology: "Developed DPSUR framework with gradient evaluation and selective update mechanisms; implemented clipping strategy for update randomization and threshold mechanism for gradient selection; evaluated on MNIST, FMNIST, CIFAR-10, and IMDB datasets with privacy budgets epsilon={1,2,3,4} and delta=1e-5."
key_findings: "Significantly outperforms DPSGD in convergence speed and model utility across multiple datasets; demonstrates faster convergence by discarding harmful updates and focusing training in beneficial directions; maintains differential privacy guarantees."
limitations: "Computational overhead from gradient evaluation and validation processes not fully characterized; scalability to larger models and datasets requires further investigation; limited evaluation to specific privacy budget ranges."
conclusion: "Successfully demonstrates that selective update mechanisms can significantly improve differentially private training efficiency while maintaining strong privacy guarantees through strategic gradient filtering."
future_work: "Optimize computational efficiency of validation processes; extend evaluation to larger-scale models and datasets; investigate adaptive threshold selection mechanisms."
implementation_insights: "Provides practical framework for privacy-preserving model training in HDM systems, particularly relevant for training personal AI models while protecting sensitive user data through improved differential privacy mechanisms."
tags:
  - "Differential Privacy"
  - "Machine Learning"
  - "Privacy-Preserving Training"
  - "Selective Updates"
  - "Gradient Descent"
---

# <span id="page-0-0"></span>DPSUR: Accelerating Differentially Private Stochastic Gradient Descent Using Selective Update and Release

Jie Fu1,<sup>2</sup> , Qingqing Ye<sup>2</sup> , Haibo Hu<sup>2</sup> , Zhili Chen1,<sup>∗</sup> , Lulu Wang<sup>1</sup> , Kuncan Wang<sup>1</sup> , Xun Ran<sup>2</sup>

<sup>1</sup>Shanghai Key Laboratory of Trustworthy Computing, East China Noraml University, China <sup>2</sup>Department of Electronic and Information Engineering, The Hong Kong Polytechnic University, China jie.fu@stu.ecnu.edu.cn,qqing.ye@polyu.edu.hk,haibo.hu@polyu.edu.hk,zhlchen@sei.ecnu.edu.cn luluwang@stu.ecnu.edu.cn,10204804424@stu.ecnu.edu.cn,qi-xun.ran@connect.polyu.hk

## ABSTRACT

Machine learning models are known to memorize private data to reduce their training loss, which can be inadvertently exploited by privacy attacks such as model inversion and membership inference. To protect against these attacks, differential privacy (DP) has become the de facto standard for privacy-preserving machine learning, particularly those popular training algorithms using stochastic gradient descent, such as DPSGD. Nonetheless, DPSGD still suffers from severe utility loss due to its slow convergence. This is partially caused by the random sampling, which brings bias and variance to the gradient, and partially by the Gaussian noise, which leads to fluctuation of gradient updates.

Our key idea to address these issues is to apply selective updates to the model training, while discarding those useless or even harmful updates. Motivated by this, this paper proposes DPSUR, a Differentially Private training framework based on Selective Updates and Release, where the gradient from each iteration is evaluated based on a validation test, and only those updates leading to convergence are applied to the model. As such, DPSUR ensures the training in the right direction and thus can achieve faster convergence than DPSGD. The main challenges lie in two aspects privacy concerns arising from gradient evaluation, and gradient selection strategy for model update. To address the challenges, DP-SUR introduces a clipping strategy for update randomization and a threshold mechanism for gradient selection. Experiments conducted on MNIST, FMNIST, CIFAR-10, and IMDB datasets show that DPSUR significantly outperforms previous works in terms of convergence speed and model utility.

#### 1 INTRODUCTION

In the past decade, deep learning techniques have achieved remarkable success in many AI tasks, such as image recognition [\[32,](#page-12-0) [52,](#page-13-0) [70\]](#page-13-1), text analysis [\[10\]](#page-12-1), and recommendation systems [\[58\]](#page-13-2). However, even though the training data are not published, adversaries may still learn them by analyzing the model parameters. For example, the contents of training data can be inverted from the models [\[21,](#page-12-2) [38,](#page-12-3) [43,](#page-12-4) [56,](#page-13-3) [72\]](#page-13-4), or the membership information of the training set can be inferred [\[34,](#page-12-5) [49\]](#page-13-5). This is of particular concern in those applications which involve sensitive and personal data, such as medical imaging and finance. Recent legislations such as EU's General Data Privacy Regulation (GDPR) and California Consumer Privacy

Act have mandated machine learning practitioners to take legal responsibility for protecting private data [\[12\]](#page-12-6).

One of the state-of-the-art paradigms to prevent privacy disclosure in machine learning is differential privacy (DP) [\[19\]](#page-12-7). Many works [\[1,](#page-12-8) [9,](#page-12-9) [20,](#page-12-10) [25,](#page-12-11) [28,](#page-12-12) [47,](#page-13-6) [51,](#page-13-7) [59\]](#page-13-8) have demonstrated that by adding proper DP noise in the training phase, the resulted machine learning models can prevent unintentional leakage of private training data, such as membership inference attacks.

Among these works, the seminal work by Abadi et al. [\[1\]](#page-12-8) proposes differentially private stochastic gradient descent (DPSGD) as the training algorithm. In DPSGD, each iteration involves four main steps: (i) randomly selecting a batch of samples using Poisson sampling, (ii) computing and clipping the gradient for each sample, (iii) adding random Gaussian noise to each gradient based on a privacy loss analysis, and (iv) updating the model weights using the average noisy gradients in the batch. In these steps, random Gaussian noise and Poisson sampling are the main reasons to cause slower convergence than conventional SGD [\[57,](#page-13-9) [61,](#page-13-10) [65,](#page-13-11) [67\]](#page-13-12).

- (1) Gaussian Noise. In DPSGD, Gaussian noise is added to the gradient in each iteration to satisfy differential privacy. However, the noise scale can be forbiddingly large, leading to inaccurate gradient estimation and poor optimization, especially when it is close to convergence [\[1\]](#page-12-8).
- (2) Poisson Sampling. Random sampling in SGD is usually implemented as epoch partitioning in practice. However, in DPSGD random sampling is popularly implemented as Possion sampling for its privacy amplification effect [\[37\]](#page-12-13). Since Possion sampling may lead to bias and variance in gradient estimation, resulting in unstable and slow convergence to optimize the objective function [\[6,](#page-12-14) [24,](#page-12-15) [26\]](#page-12-16), we attribute the performance issue of DPSGD partially to random sampling.

Although there are a few recent works which optimize random sampling or Gaussian noise separately [\[31,](#page-12-17) [57,](#page-13-9) [66\]](#page-13-13), as shown by the blue trace in Figure [1,](#page-1-0) all these works still blindly update the model, whether or not the loss is improved in this iteration. This issue is particularly eminent when the training process approaches convergence and the magnitude of loss is small.

In this paper, we propose DPSUR, a Differentially Private Stochastic Gradient Descent training framework based on Selective Update and Releases. In essence, DPSUR only executes differentially private gradient descent if the gradient is in the correct direction to decrease loss and thus leads to a better model, as shown by the red trace in Figure. [1.](#page-1-0) This idea is inspired by simulated annealing (SA) [\[27,](#page-12-18) [35\]](#page-12-19), where the objective function value (loss) is treated as "energy", and the differentially private model parameters obtained

<sup>\*</sup> Corresponding author

<span id="page-1-0"></span>![](_page_1_Figure_0.jpeg)
<!-- Image Description: This contour plot displays the optimization trajectories of two algorithms, DPSUR (red) and DPSGD (blue), on a loss function surface.  The concentric contours represent levels of the loss function, with the black star marking the minimum.  The plot's purpose is to visually compare the convergence speed and path of the two algorithms towards the optimal solution.  The x and y axes represent parameters θ₀ and θ₁ respectively. -->

Figure 1: Trajectory visualization of DPSGD and DPSUR schemes on a linear regression model.

in each iteration is a random "solution". As such, we use the difference between the current and previous iteration's loss Δ as a criterion for accepting or rejecting model parameters.

Selecting those "correct" updates in DPSGD is non-trivial. First, the evaluation of gradient Δ needs to access a training set, which consumes additional privacy budgets. Second, how to set a threshold for selective update is essential as it directly affects the training performance. These two issues are closely interleaved. To address the first issue, we propose a clipping strategy to Δ, which employs a minimal clipping bound to minimize the perturbation error. For the second issue, we devise a threshold mechanism for update selection by optimizing the utility gain from selective update.

In addition, we also propose an optimization that selectively releases gradients during multiple iterations, which further reduces the privacy budget consumption. In summary, our contributions are as follows:

- We propose a new DPSUR framework for differentially private deep learning, which uses a validation test to select the model updates and ensures the gradient updates are in the correct direction. To our knowledge, this is the first work to apply selective update for model training under differential privacy.
- A clipping strategy and a threshold mechanism are devised to guarantee DP privacy and optimize utility gain, which enables a faster convergence and better accuracy than DPSGD.
- Furthermore, we propose Gaussian mechanism with selective release to reduce privacy budget consumption across iterations.
- Rigorous theoretical analysis has guaranteed differential privacy of DPSUR, together with a comprehensive empirical evaluation on four public datasets. The results confirm that DPSUR outperforms the state-of-the-art solutions in terms of model accuracy.

The rest of the paper is organized as follows. Section [2](#page-1-1) introduces the preliminary knowledge. In Section [3,](#page-2-0) we present our method of selective update. Section [4](#page-4-0) shows the selective release mechanism and the complete algorithm DPSUR. Privacy analysis is conducted in Section [5](#page-6-0) and the experimental results are presented in Section [6.](#page-8-0) Section [7](#page-11-0) introduces related work, followed the conclusion in Section [8.](#page-11-1)

#### <span id="page-1-1"></span>2 PRELIMINARY KNOWLEDGE

#### 2.1 Differential Privacy

Differential privacy is a rigorous mathematical framework that formally defines data privacy. It requires that a single entry in the input dataset must not lead to statistically significant changes in the output [\[16,](#page-12-20) [17,](#page-12-21) [19\]](#page-12-7) if differential privacy holds.

Definition 2.1. (Differential Privacy [\[19\]](#page-12-7)). The randomized mechanism provides (, )-Differential Privacy (DP), if for any two neighboring datasets and ′ that differ in only a single entry, ∀S ⊆ Range(),

$$
Pr(A(D) \in S) < e^{\epsilon} \times Pr(A(D') \in S) + \delta. \tag{1}
$$

Here, > 0 controls the level of privacy guarantee in the worst case. The smaller , the stronger the privacy level is. The factor > 0 is the failure probability that the property does not hold. In practice, the value of should be negligible [\[40,](#page-12-22) [73\]](#page-13-14), particularly less than <sup>1</sup> | | .

By adding random noise, we can achieve differential privacy for a function : X → R according to Definition 2.1. The sensitivity determines how much noise is needed and is defined as follow.

Definition 2.2. (l<sup>k</sup> -Sensitivity[\[17\]](#page-12-21)) For a function : X → R , we define its norm sensitivity (denoted as Δ ) over all neighboring datasets , ′ ∈ X differing in a single sample as

$$
\sup_{x,x' \in \mathcal{X}^n} ||f(x) - f(x')||_k \le \Delta_k f. \tag{2}
$$

In this paper, we focus on <sup>2</sup> sensitivity, i.e., || · ||2. Additionally, the following Lemma [2.3](#page-1-2) ensures the privacy guarantee of postprocessing operations.

<span id="page-1-2"></span>Lemma 2.3 (Post-processing [\[19\]](#page-12-7)). Let M be a mechanism satisfying (, )-DP. Let be a function whose input is the output of M. Then (M) also satisfies (, )-DP.

#### 2.2 Rényi Differential Privacy

Rényi differential privacy (RDP) is a relaxation of -differential privacy, which is defined on Rényi divergence as follows.

Definition 2.4. (Rényi Divergence [\[54\]](#page-13-15)) Given two probability distributions and , the Rényi divergence of order > 1 is:

$$
D_{\alpha}(P||Q) = \frac{1}{\alpha - 1} \ln \mathbf{E}_{x \sim Q} \left[ \left( \frac{P(x)}{Q(x)} \right)^{\alpha} \right],
$$
 (3)

where E∼ denotes the excepted value of for the distribution , (), and () denotes the density of or at respectively.

Definition 2.5. (Rényi Differential Privacy (RDP) [\[36\]](#page-12-23)) For any neighboring datasets , ′ ∈ X , a randomized mechanism M : X → R satisfies (, )-RDP if

$$
D_{\alpha}(\mathcal{M}(x)||\mathcal{M}(x')) \le R. \tag{4}
$$

The following Definition [2.6](#page-2-1) provides a formal definition of Gaussian mechanism, and a formal RDP guarantee by it.

<span id="page-2-1"></span>Definition 2.6. (RDP of Gaussian mechanism [\[36\]](#page-12-23)) Assuming is a real-valued function, and the sensitivity of is , the Gaussian mechanism for approximating is defined as

$$
\mathbf{G}_{\sigma}f(D) = f(D) + N\left(0, \mu^{2}\sigma^{2}\right),\tag{5}
$$

where (0, 2 2 ) is normally distributed random variable with standard deviation and mean 0. Then the Gaussian mechanism with noise G satisfies (, /2 2 ) − .

The following Lemma [2.7](#page-2-2) defines the standard form for converting (, )-RDP to (, )-DP.

<span id="page-2-2"></span>Lemma 2.7. (Conversion from RDP to DP [\[3\]](#page-12-24)). if a randomized mechanism : → R satisfies (, )-RDP ,then it satisfies( + ln( ( − 1)/) − (ln + ln )/( − 1), )-DP for any 0 < < 1.

#### 2.3 Deep Learning with Differential Privacy

Differentially Private Stochastic Gradient Descent (DPSGD) is a widely-adopted training algorithm for deep neural networks with differential privacy guarantees. Specifically, in each iteration , a batch of tuples B is sampled from with a fixed probability | | , where is the batch size. After computing the gradient of each tuple ∈ B as () = ∇ ( , ), where is model parameter for the i-th sample, DPSGD clips each per-sample gradient according to a fixed ℓ2 norm (Equation [\(6\)](#page-2-3)).

$$
\overline{g}_t(x_i) = \text{Clip}(g_t(x_i); C)
$$
$$
= g_t(x_i) / \max\left(1, \frac{\|g_t(x_i)\|_2}{C}\right).
$$
(6)

In this way, for any two neighboring datasets, the sensitivity of the query Í ∈ B () is bounded by . Then, it adds Gaussian noise scaling with to the sum of the gradients when computing the batch-averaged gradients:

$$
\tilde{g}_t = \frac{1}{b} \left( \sum_{i \in \mathcal{B}_t} \overline{g}_t \left( x_i \right) + \mathcal{N} \left( 0, \sigma^2 C^2 \mathbf{I} \right) \right),\tag{7}
$$

where is the noise multiplier depending on the privacy budget. Last, the gradient descent is performed based on the batch-averaged gradients. Since initial models are randomly generated and independent of the sample data, and the batch-averaged gradients satisfy the differential privacy, the resulted models also satisfy the differential privacy due to the post-processing property.

Privacy accounting. Three factors determine DPSGD's privacy guarantee — the noise multiplier , the sampling ratio | | , and the number of training iterations . In reality, given the privacy parameters (, ), we can set appropriate values for these three hyperparameters to optimize the performance. The privacy calibration process is performed using a privacy accountant: a numerical algorithm providing tight upper bounds for the given (, ) as a function of the hyper-parameters [\[1\]](#page-12-8), which in turn can be combined with numerical optimization routines to optimize one hyper-parameter given the other two. In this work we use the RDP [\[36\]](#page-12-23) for privacy accounting. In practice, given , and at each iteration, we select from {2, 3, ..., 64} to determine the smallest .

# <span id="page-2-0"></span>3 DPSUR: DP TRAINING FRAMEWORK WITH SELECTIVE UPDATES AND RELEASE

In this section, we present our proposed framework DPSUR, with an overview in Section [3.1.](#page-2-4) Then two key components of DPSUR, namely, minimal clipping strategy and threshold mechanism,are introduced in Sections [3.2](#page-3-0) and [3.3,](#page-4-1) respectively.

#### <span id="page-2-4"></span>3.1 Overview

As aforementioned, DPSUR does not directly accept the model updates from each iteration due to the influence of random sampling and Gaussian noise. Therefore, we first calculate the loss of the generated model in each iteration, and then compare it with that from the last iteration to determine whether or not to accept the model update.

<span id="page-2-5"></span>![](_page_2_Figure_16.jpeg)
<!-- Image Description: The flowchart depicts an iterative model training algorithm.  It details steps involving obtaining a new model using DPSGD, calculating loss differences (ΔE), applying a DP processing step, and checking a convergence condition (ΔE < Z).  The algorithm iterates until a termination condition (t < T) is met, outputting the final model *w<sub>t</sub>*.  The flowchart visually presents the algorithm's sequential steps and decision points. -->

Figure 2: Workflow of DPSUR.

<span id="page-2-3"></span>Figure [2](#page-2-5) shows the workflow of DPSUR, which takes as inputs the total number of updates , number of updates accepted , acceptance threshold , and initialization model 0, executes the following steps, and outputs a final model.

- Step 1: In each iteration, we obtain a batch of tuples from the training set via Poisson sampling, and generate an intermediate model using the DPSGD algorithm.
- Step 2: We evaluate the intermediate model and−<sup>1</sup> on the validation batch B resampled from training set to calculate the loss () and (−1).
- Step 3: We compute the difference of loss Δ = () − (−1) to evaluate the performance of intermediate model.
- Step 4: We clip Δ and add noise to it to satisfy differential privacy, obtaining <sup>Δ</sup>f.
- Step 5: Given the acceptance threshold , we accept update of the intermediate model and plus 1 if <sup>Δ</sup>f <sup>&</sup>lt; , or reject it otherwise by reverting back to the last model −<sup>1</sup> that was accepted for update.

Note that when reaches the total number of updates , we output the trained model .

Figure [3](#page-3-1) further shows how we evaluate the model, i.e. obtaining () (step 2 in Figure [2\)](#page-2-5). During each iteration, we first randomly sample a portion of the tuples B from the training set and perform DPSGD training to obtain a model. Then we randomly re-sample a portion of tuples from the training set as validation batch B . Finally, the cross-entropy loss function is applied to the B to compute the loss of the current model. It is important to note that sampling from the training set for training and validation serves the purpose of privacy amplification. Specifically, re-sampling from the training set for model validation helps prevent overfitting. The complete DPSUR algorithm will be described in Section [4.2.](#page-6-1)

<span id="page-3-1"></span>![](_page_3_Figure_2.jpeg)
<!-- Image Description: Figure 4 illustrates "minimal clipping" in a machine learning model.  It uses a flowchart showing a training dataset processed in mini-batches through a model ('dpsgd'), calculating a cross-entropy loss.  A parallel validation process is also depicted. The text explains how clipping constrains  changes in model parameters (ΔE), minimizing computational cost without significant impact on accuracy. -->

Figure 3: Model evaluation framework in DPSUR.

#### <span id="page-3-0"></span>3.2 Minimal Clipping

As the computation of Δ accesses the training set (i.e., a portion of private tuples), it is necessary to perform a differential privacy operation on it. Intuitively, we can clip Δ to a certain range [−, ], and then add Gaussian noise with mean 0 and standard deviation 2 · to ensure differential privacy, as shown in Equation [\(8\)](#page-3-2). Here, denotes the noise multiplier, and 2 is the sensitivity of the clipping operation.

$$
\widetilde{\Delta E} = \mathbf{Clip}(\Delta E; C_v) + \sigma_v \cdot 2C_v \cdot \mathcal{N}(0, 1),
$$
  
= min(max( $\Delta E, -C_v$ ),  $C_v$ ) +  $\sigma_v \cdot 2C_v \cdot \mathcal{N}(0, 1)$  (8)

However, setting an appropriate clipping bound for Δ is challenging. A large helps avoid loss of fidelity to the original values, but it also leads to large injected noise. A key observation here is that, to assess the quality of the current model, we can simply compare the loss of the model trained in this iteration with that of the previous iteration, i.e., Δ = () − (−1). If the loss is lower than the previous iteration, i.e., Δ < 0, the current model is better and we accept it, otherwise we reject it. Therefore, we only need to determine whether Δ is positive or negative, instead of its absolute value. With that said, we can use a small clipping bound for uniform clipping such that almost all Δ are outside the interval [−, ], which is illustrated by the red line in Figure [4.](#page-3-3)

<span id="page-3-4"></span>
$$
\overline{\Delta E} = \begin{cases}\n-C_v, & \Delta E \leq -C_v \\
\Delta E, & -C_v < \Delta E < C_v \\
C_v, & \Delta E \geq C_v\n\end{cases} \tag{9}
$$

 We clip Δ to a certain range [−, ] as shown in Equation [9.](#page-3-4) If we choose to be extremely small (e.g., = 1 − 10), we can

<span id="page-3-3"></span>![](_page_3_Figure_10.jpeg)
<!-- Image Description: The image displays a scatter plot illustrating the distribution of instances of ΔE against the value of ΔE.  A vertical red line at ΔE=0 acts as a visual threshold, separating instances with positive and negative ΔE values. The plot likely demonstrates the distribution of a certain metric (ΔE) across multiple instances, showing the frequency of different ΔE values above and below zero.  Its purpose is to visually represent the data distribution and highlight the significance of the zero value. -->

Figure 4: The idea of minimal cilpping.

**loss** forward propagation cross-entropy () make almost all Δ stay outside [−, ], and the clipping process is simplified to Equation [10.](#page-3-5) Although in the worst case, there could be some value of Δ in the interval of [−, ], the probability is so small that we can ignore it without affecting our technical analysis. In practice, we can select the clipping bound to be small enough for loss value in gradient descent, e.g., = 0.001.

<span id="page-3-5"></span>
$$
\overline{\Delta E} = \begin{cases}\n-C_v, & \Delta E < 0 \\
C_v, & \Delta E > 0\n\end{cases}.
$$
\n(10)

So each possible value of Δ is discretized as − or after our minimal clipping strategy. A small clipping bound ensures that the injected Gaussian noise is sufficiently small. Such clipping strategy can quantify the impact of the injected Gaussian noise. As plotted in Figure [5,](#page-4-2) given threshold (shown as the red lines), after minimal clipping and adding Gaussian noise, values of Δ consist of two (partial) Gaussian distributions with a mean of or − and a standard deviation of 2 , respectively. The blue area represents the probability of the Gaussian distribution with a mean of and less than threshold , while the orange and blue area together represents the probability of the Gaussian distribution with a mean of − and less than threshold .

<span id="page-3-2"></span>For a real example, let clipping bound = 0.1 and noise level = 1. The results by the clipping strategy after adding noise are plotted in Figure [5a,](#page-4-2) where threshold = 0 is used to accept those updates whose Δ < . We observe that the probability of accepting a high-quality model (Δ < 0) is 69.1%, while the probability of accepting a low-quality model (Δ > 0) is 30.8%. Next, we slightly move the acceptance threshold from 0 to −0.2 to investigate its impact on the acceptance probabilities. Figures [5b](#page-4-2) and [5c](#page-4-2) show the results of = −0.1 and = −0.2, respectively. We observe that, from = 0 to = −0.1, the probability of accepting a high-quality model drops much more slowly (from 69.1% to 50%) than that of accepting a low-quality model (from 30.8% to 15.9%). However, as further decreases, the situation is reversed, i.e., the probability of accepting a high-quality model drops quickly, which goes against the model convergence. This observation motivates us to explore an optimal threshold to maximize the utility gain from model updates.

<span id="page-4-2"></span>![](_page_4_Figure_0.jpeg)
<!-- Image Description: The figure displays three probability density plots, each showing two overlapping normal distributions (μ =  -C<sub>v</sub> in orange, μ = C<sub>v</sub> in blue),  with shaded areas representing probability.  The plots illustrate the effect of varying Z (a parameter, taking values 0, -0.1, and -0.2) on the overlap between the distributions.  The purpose is to visualize the impact of Z on a specific probability calculation within the paper's context. -->

Figure 5: The Gaussian probability distributions under different thresholds Z, where the Gaussian distribution N (, (2 · ) 2 ) and the = 1, = 0.1

#### <span id="page-4-1"></span>3.3 Threshold Mechanism

In this subsection, we derive an optimal threshold . Formally, let = · . Then for the case of Δ < 0, the CDF of the Gaussian distribution N (−, (2 · ) 2 ) less than is

$$
P(X < Z) = \Phi\left(\frac{\beta \cdot C_v - (-C_v)}{2C_v \cdot \sigma_v}\right) = \Phi\left(\frac{\beta + 1}{2\sigma_v}\right),\tag{11}
$$

where = N (−, (2 · ) 2 ) and Φ() = 1 √ 2 ∫ −∞ − 2 <sup>2</sup> . Similarly, the CDF of the case Δ > 0 is

$$
P(X < Z) = \Phi\left(\frac{\beta \cdot C_v - C_v}{2C_v \cdot \sigma_v}\right) = \Phi\left(\frac{\beta - 1}{2\sigma_v}\right),\tag{12}
$$

where = N (, (2 · ) 2 ). According to Equations [\(11\)](#page-4-3) and [\(12\)](#page-4-4), the parameter will be eliminated in the CDF of Gaussian distribution, so the acceptance probability of the algorithm only depends on the parameters and .

In Figure [6,](#page-4-5) we plot the probabilities of accepting high-quality (Δ < 0) and low-quality (Δ > 0) models for popular : 0.8, 1.0, and 1.3, with respect to ranging from −3.5 to 0.5. Obviously, smaller value results in decreasing probabilities of accepting both high-quality (Δ < 0) and low-quality (Δ > 0) models. To find a that maximizes the difference between the two probabilities (i.e., the red dashed vertical line), we find that such seems to be around −1.0 for all three . As will be shown in Figure [9c](#page-10-0) of the experimental results, setting = −1.0 does achieve excellent results in all datasets.

<span id="page-4-5"></span>![](_page_4_Figure_9.jpeg)
<!-- Image Description: The image displays a graph plotting probability against β, showing curves for different values of ΔE and σ<sub>ν</sub>.  Solid lines represent ΔE > 0, while dashed lines represent ΔE < 0.  Different colors represent varying σ<sub>ν</sub> values (0.8, 1, and 1.3).  The graph likely illustrates the probability of an event based on these parameters, with a vertical dashed line indicating a point of interest where curves intersect.  The purpose is to visually represent the impact of ΔE and σ<sub>ν</sub> on probability within the context of the paper's model. -->

Figure 6: Acceptance probability vs. .

<span id="page-4-3"></span>Summary. To address the privacy concerns arising from the evaluation on selective update, we propose a randomized algorithm coupled with a minimal clipping strategy and a threshold mechanism. In particular, by setting a sufficiently small clipping bound (e.g., 0.001) and the acceptance threshold = · , the impact of on the selection update is eliminated according to Equations [\(11\)](#page-4-3) and [\(12\)](#page-4-4). Further, a suitable is selected based on probability distributions to achieve maximum utility for selective updates.

# <span id="page-4-4"></span><span id="page-4-0"></span>4 SELECTIVE RELEASE IN DPSUR: AN OPTIMIZATION

As of now, iteratively calculating the <sup>Δ</sup>f in each iteration requires continual privacy budget consumption. In Section [4.1,](#page-4-6) we prove that by only releasing the model when a selective update occurs, DPSUR can preserve the privacy budget. Finally, we summarize the overall algorithm of DPSUR in Section [4.2.](#page-6-1)

#### <span id="page-4-6"></span>4.1 Gaussian Mechanism with Selective Release

Recall that when we obtain <sup>Δ</sup>f, to protect privacy, we clip <sup>Δ</sup> in [−, ] and add Gaussian noise according to Equation [8](#page-3-2) in each iteration. According to step 5 of Figure [2,](#page-2-5) we do not update the model until <sup>Δ</sup>f exceeds the threshold . If we take one step further and do not release <sup>Δ</sup>f in such cases, as described in Algorithm [1,](#page-5-0) DPSUR only consumes privacy budget when a selective update occurs, i.e., <sup>Δ</sup>f <sup>&</sup>lt; · . In this subsection, we conduct privacy analysis to ensure Algorithm [1](#page-5-0) can satisfy the same RDP guarantee as that of the underlying Gaussian mechanism in Definition [2.6.](#page-2-1)

In general, for the query result () on dataset , Algorithm [1](#page-5-0) clip the () in [0, ] and adds Gaussian noise until the noisy result falls in a designated interval [, ]. The following Theorem [4.1](#page-4-7) shows that when → −∞, Algorithm [1](#page-5-0) can satisfy the same RDP guarantee.

<span id="page-4-7"></span>Theorem 4.1. Algorithm [1](#page-5-0) satisfies (, /2 2 ) − when → −∞.

Proof. Figure [7a](#page-5-1) plots two normal distributions, namely (0, 2 2 ) and (, 2 2 ), as the output probability distributions of function on two neighboring datasets whose sensitivity is . By selective update and selective release in the threshold range [, ], the probability distribution outside of this interval will accumulate within

| Algorithm 1: Gaussian mechanism with selective release |  |  |  |  |
|--------------------------------------------------------|--|--|--|--|
|--------------------------------------------------------|--|--|--|--|

<span id="page-5-0"></span>

|   | Input: function<br>𝑓<br>(·), dataset<br>𝐷, Gaussian distribution<br>𝑁, a       |
|---|--------------------------------------------------------------------------------|
|   | given interval<br>[𝑎, 𝑏]                                                       |
|   | Output: 𝐴(𝐷)<br>that falls in the interval<br>[𝑎, 𝑏]<br>after adding           |
|   | Gaussian noise                                                                 |
|   | 1 Clipping<br>𝑓<br>(𝐷)<br>to interval<br>[0, 𝜇]<br>to obtain sensitivity<br>𝜇; |
|   | (0, 𝜇2𝜎<br>2<br>);<br>2 𝐴(𝐷)<br>= 𝑓<br>(𝐷) +<br>𝑁                              |
|   | 3 while 𝐴(𝐷)<br><<br>𝑎<br>or 𝐴(𝐷)<br>><br>𝑏<br>do                              |
| 4 | (0, 𝜇2𝜎<br>2<br>);<br>𝐴(𝐷)<br>= 𝑓<br>(𝐷) +<br>𝑁                                |
|   | 5 return 𝐴(𝐷)                                                                  |
|   |                                                                                |

the interval. As such, the final output distribution is truncated and transformed into a truncated normal distribution, as shown in Figure [7b.](#page-5-1) As is assumed to follow a normal distribution, the truncated normal distribution with mean 0 and mean can be represented as follows:

$$
f(x; 0, \mu\sigma, a, b) = \begin{cases} \frac{1}{\mu\sigma\sqrt{2\pi}}e^{-\frac{x^2}{2\mu^2\sigma^2}} \cdot \frac{1}{\Phi\left(\frac{b}{\mu\sigma}\right) - \Phi\left(\frac{a}{\mu\sigma}\right)} & a \leq x \leq b, \\ 0 & \text{otherwise.} \end{cases}
$$

$$
f(x; \mu, \mu\sigma, a, b) = \begin{cases} \frac{1}{\mu\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\mu^2\sigma^2}} \cdot \frac{1}{\Phi\left(\frac{b-\mu}{\mu\sigma}\right) - \Phi\left(\frac{a-\mu}{\mu\sigma}\right)} & a \leq x \leq b, \\ 0 & \text{otherwise.} \end{cases}
$$

Here is the standard deviation of the original normal distribution, whereas and are the lower and upper truncation values, respectively. Φ() denotes the cumulative distribution function of the standard normal distribution.

Then we substitute the two truncated normal distributions into Rényi divergence [\[54\]](#page-13-15) to calculate the RDP as follows:

$$
D_{\alpha}(f(x; 0, \mu\sigma, a, b))|f(x; \mu, \mu\sigma, a, b))
$$
\n
$$
= \frac{1}{\alpha - 1} \cdot \ln \int_{a}^{b} \frac{[f(x; 0, \mu\sigma, a, b)]^{\alpha}}{[f(x; \mu, \mu\sigma, a, b)]^{\alpha - 1}} dx
$$
\n
$$
= \frac{1}{\alpha - 1} \cdot \ln \{\frac{(\Phi(\frac{b - \mu}{\mu\sigma}) - \Phi(\frac{a - \mu}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha}} \cdot \frac{1}{\mu\sigma \sqrt{2\pi}} \int_{a}^{b} \exp[(-x^{2} + 2(1 - \alpha)\mu x - (1 - \alpha)\mu^{2})/(2\mu^{2}\sigma^{2})] dx\}
$$
\n
$$
= \frac{1}{\alpha - 1} \cdot \{\frac{\alpha(\alpha - 1)}{2\sigma^{2}} + \ln[\frac{(\Phi(\frac{b - \mu}{\mu\sigma}) - \Phi(\frac{a - \mu}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha}} \cdot (\Phi(\frac{b - (1 - \alpha)\mu}{\mu\sigma}) - \Phi(\frac{a - (1 - \alpha)\mu}{\mu\sigma}))]\}
$$
\n
$$
= \frac{\alpha}{2\sigma^{2}} + \frac{1}{\alpha - 1} \cdot \ln \{\frac{(\Phi(\frac{b - \mu}{\mu\sigma}) - \Phi(\frac{a - \mu}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha}} \cdot [\Phi(\frac{b - (1 - \alpha)\mu}{\mu\sigma}) - \Phi(\frac{a - (1 - \alpha)\mu}{\mu\sigma})^{\alpha}] \}
$$
\n
$$
- \Phi(\frac{a - (1 - \alpha)\mu}{\mu\sigma})]\}, \tag{13}
$$

where Φ() = 1 √ 2 ∫ −∞ − 2 <sup>2</sup> .

<span id="page-5-1"></span>![](_page_5_Figure_9.jpeg)
<!-- Image Description: The image displays two pairs of probability density functions (PDFs).  Panel (a) shows untruncated normal distributions N(0, μσ²) (gold) and N(μ, μσ²) (blue), illustrating a shift in mean. Panel (b) shows the same distributions after truncation to the interval [a, b], demonstrating the effect of truncation on the shape and scale of the PDFs. The purpose is to visually represent the impact of truncation on normal distributions within the context of a statistical analysis. -->

Figure 7: Before and after truncating the normal distribution.

As 
$$
a \to -\infty
$$
, we can get:  
\n
$$
D_{\alpha}(f(x; 0, \mu\sigma, a, b) || f(x; \mu, \mu\sigma, a, b))
$$
\n
$$
= \frac{\alpha}{2\sigma^2} + \frac{1}{\alpha - 1} \cdot \ln\left[\frac{(\Phi(\frac{b - \mu}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b}{\mu\sigma}))^{\alpha}} \cdot \Phi(\frac{b + (\alpha - 1)\mu}{\mu\sigma})\right]
$$
\n(14)

Similarly, we can get :

$$
D_{\alpha}(f(x; \mu, \mu\sigma, a, b))|f(x; 0, \mu\sigma, a, b))
$$
  
\n
$$
= \frac{1}{\alpha - 1} \cdot \ln \int_{a}^{b} \frac{[f(x; \mu, \mu\sigma, a, b)]^{\alpha}}{[f(x; 0, \mu\sigma, a, b)]^{\alpha - 1}} dx
$$
  
\n
$$
= \frac{1}{\alpha - 1} \cdot \left\{ \frac{\alpha(\alpha - 1)}{2\sigma^{2}} + \ln \left[ \frac{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b - \mu}{\mu\sigma}) - \Phi(\frac{a - \mu}{\mu\sigma}))^{\alpha}} \right] \right\}
$$
  
\n
$$
\cdot (\Phi(\frac{b - \alpha\mu}{\mu\sigma}) - \Phi(\frac{a - \alpha\mu}{\mu\sigma}))]
$$
  
\n
$$
= \frac{\alpha}{2\sigma^{2}} + \frac{1}{\alpha - 1} \cdot \ln \left[ \frac{(\Phi(\frac{b}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b - \mu}{\mu\sigma}))^{\alpha}} \cdot \Phi(\frac{b - \alpha\mu}{\mu\sigma}) \right]
$$

According Theorem [4.2,](#page-5-2) we have:

$$
D_{\alpha}(f(x; 0, \mu\sigma, a, b)||f(x; \mu, \mu\sigma, a, b)) \leq \alpha/2\sigma^{2}, and
$$
  
$$
D_{\alpha}(f(x; \mu, \mu\sigma, a, b)||f(x; 0, \mu\sigma, a, b)) \leq \alpha/2\sigma^{2}.
$$

Therefore, Theorem [4.1](#page-4-7) is proved. The details of RDP of two truncated normal distributions are presented in Appendix [A.](#page-13-16) □

Next, we will prove Theorem [4.2.](#page-5-2) This theorem is an inequality proof of the cumulative distribution function (CDF) of the normal distribution, and it provides the foundation for the proof of Theorem [4.1.](#page-4-7)

<span id="page-5-2"></span>THEOREM 4.2. If 
$$
A = (\Phi(\frac{b-\mu}{\mu\sigma}))^{\alpha-1} \cdot \Phi(\frac{b+(\alpha-1)\mu}{\mu\sigma})/(\Phi(\frac{b}{\mu\sigma}))^{\alpha}, B = (\Phi(\frac{b}{\mu\sigma}))^{\alpha-1} \cdot \Phi(\frac{b-\alpha\mu}{\mu\sigma})/(\Phi(\frac{b-\mu}{\mu\sigma}))^{\alpha}
$$
, where  $\Phi(x) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{x} e^{-\frac{t^2}{2}} dt$ .  
\nA,  $B \le 1$ , when  $\mu > 0$ ,  $\sigma > 0$  and  $\alpha > 1$ .

Proof. The second derivative of ln [Φ()] is:

$$
\ln''\left[\Phi(x)\right] = \frac{\Phi''(x) \cdot \Phi(x) - \Phi'(x) \cdot \Phi'(x)}{[\Phi(x)]^2}
$$
$$
= \frac{-x \cdot \Phi'(x) \cdot \Phi(x) - \Phi'(x) \cdot \Phi'(x)}{[\Phi(x)]^2},
$$
(16)

where Φ ′ () = 1 √ 2 − 2 . When ≥ 0, since Φ(), Φ ′ () > 0, ln′′ [Φ()] < 0 always hold.

When < 0, Φ ′ () > 0. As such, proving − · Φ ′ () · Φ() − Φ ′ () · Φ ′ () < 0 is equivalent to proving − · Φ() − Φ ′ () < 0. We let () = − · Φ() − Φ ′ (), so the derivative for () is:

$$
K'(x) = -\Phi(x) + (-x) \cdot \Phi'(x) - \Phi''(x)
$$
  
=  $-\Phi(x) + (-x) \cdot \Phi'(x) - (-x) \cdot \Phi'(x)$  (17)  
=  $-\Phi(x) < 0$ 

Since lim→−∞ () = 0, () < 0 when < 0. In summary, ln′′ [Φ()] < 0 always holds. In other words, ln′′ [Φ()] is the concave function when ∈ (−∞, ∞). According to the properties of the concave function, we can obtain:

$$
\lambda \cdot \ln \left[ \Phi(x_1) \right] + (1 - \lambda) \ln \left[ \Phi(x_2) \right] \le \ln \left[ \Phi(\lambda x_1 + (1 - \lambda) x_2) \right],
$$

where ∈ (0, 1) and 1, <sup>2</sup> ∈ (−∞, ∞).

Let = −1 ( > 1) , <sup>1</sup> = − , <sup>2</sup> = +(−1) or <sup>1</sup> = , <sup>2</sup> = − . Then the following two inequalities hold:

$$
\frac{(\alpha - 1)}{\alpha} \cdot \ln \left[ \Phi\left(\frac{b - \mu}{\mu \sigma}\right) \right] + \frac{1}{\alpha} \ln \left[ \Phi\left(\frac{b + (\alpha - 1)\mu}{\mu \sigma}\right) \right] \le \ln \left[ \Phi\left(\frac{b}{\mu \sigma}\right) \right]
$$
$$
\frac{(\alpha - 1)}{\alpha} \cdot \ln \left[ \Phi\left(\frac{b}{\mu \sigma}\right) \right] + \frac{1}{\alpha} \ln \left[ \Phi\left(\frac{b - \alpha \mu}{\mu \sigma}\right) \right] \le \ln \left[ \Phi\left(\frac{b - \mu}{\mu \sigma}\right) \right]
$$
(18)

In the end, we can obtain the following:

$$
(\Phi(\frac{b-\mu}{\mu\sigma}))^{\alpha-1} \cdot \Phi(\frac{b+(\alpha-1)\mu}{\mu\sigma}) \le (\Phi(\frac{b}{\mu\sigma}))^{\alpha}
$$
  
$$
(\Phi(\frac{b}{\mu\sigma}))^{\alpha-1} \cdot \Phi(\frac{b-\alpha\mu}{\mu\sigma}) \le (\Phi(\frac{b-\mu}{\mu\sigma}))^{\alpha},
$$
  
where  $\mu, \sigma > 0$  and  $\alpha > 1$ . (19)

Theorem [4.2](#page-5-2) is proved. □

This proves Algorithm [1](#page-5-0) satisfies the same (, /2 2 )-RDP as Gaussian mechanism of RDP [\[36\]](#page-12-23). In other words, DPSUR only consumes privacy budget when the update is selected and released based on the interval. As such, in Figure [2,](#page-2-5) the privacy budget of computing <sup>Δ</sup>f is consumed only if <sup>Δ</sup>f <sup>&</sup>lt; .

#### <span id="page-6-1"></span>4.2 DPSUR: Putting Things Together

Now we describe the overall algorithm of DPSUR in Algorithm [2,](#page-6-2) which consists of the following two steps.

i. DPSGD (Lines 3-8). This part is the traditional DPSGD procedure. First, a small batch of samples B are randomly selected from the training datasets (Line [3\)](#page-6-3). For each sample ∈ B , its gradient values are calculated and clipped so that the <sup>2</sup> norm of the gradients is not greater than the clipping bound (Lines [4-](#page-6-4) [6\)](#page-6-5). In Line [7,](#page-6-6) the clipped gradients are first summed up, and then added Gaussian noise N (0,<sup>2</sup> 2 ) to satisfy differential privacy, and finally averaged. As such, the sensitivity is here. Gradient descent is then performed using these noisy gradients to obtain a new temporary model for the current iteration (Line [8\)](#page-6-7).

ii. Selective update (Lines 9-18). First, a small batch of samples B are randomly selected from the training set (Line [9\)](#page-6-8). Then we calculate the loss for temporary model () and the latest accepted model (−1), where () = 1/|B | Í ∈ B L (, ), and subtract them to get Δ (Lines [10-](#page-6-9) [11\)](#page-6-10). To get the sensitivity, Δ is clipped to [−, ], which means that one less or one more sample

produces a maximum variation of 2 for Δ (Line [12\)](#page-6-11). To ensure differential privacy, Gaussian noise N (0, 2 · (2 ) 2 ) is added to obtain a noisy version △f (Lines [13\)](#page-6-12). The temporary model will be accepted and plus 1 if △f <sup>&</sup>lt; · , where is the acceptance threshold parameter (Lines [15-](#page-6-13) [16\)](#page-6-14). Otherwise, the temporary model is rejected, and the model from the last iteration is returned (Line [18\)](#page-6-15).

The above two steps are repeated until the entire privacy budget is consumed. We will provide rigorous privacy analysis in the next section.

## Algorithm 2: Overall algorithm of DPSUR

<span id="page-6-7"></span><span id="page-6-6"></span><span id="page-6-5"></span><span id="page-6-4"></span><span id="page-6-3"></span><span id="page-6-2"></span>

| Input: training datasets<br>{𝑥1, 𝑥2, , 𝑥𝑁<br>}, loss function                         |
|---------------------------------------------------------------------------------------|
| L (𝜃, 𝑥). Parameters: learning rate<br>𝜂, batch size for                              |
| training<br>𝐵𝑡<br>, noise multiplier for training<br>𝜎𝑡<br>, clipping                 |
| bound for training<br>, batch size for validation<br>,<br>𝐶𝑡<br>𝐵𝑣                    |
| noise multiplier for validation<br>𝜎𝑣<br>, clipping bound for                         |
| validation<br>𝐶𝑣<br>, threshold parameter<br>𝛽                                        |
| Output: the final trained model<br>𝑤𝑡                                                 |
| 1 Initialize<br>𝑡<br>= 1,<br>𝑤0<br>= Initial();                                       |
| <<br>2 while 𝑡<br>𝑇<br>do                                                             |
| 𝐵𝑡<br>Randomly sample a batch<br>with probability<br>;<br>B𝑡<br>3<br>𝑁                |
| for 𝑥𝑖<br>∈ B𝑡<br>do<br>4                                                             |
| Compute<br>;<br>𝑔𝑡<br>(𝑥𝑖) ← ∇L(𝑤𝑡<br>,𝑥𝑖<br>5<br>)                                   |
| 𝑔𝑡<br>(𝑥𝑖<br>)    2<br>𝑔𝑡<br>(𝑥𝑖) ←<br>𝑔𝑡<br>(𝑥𝑖)/max(1,<br>);<br>6<br>𝐶𝑡             |
| 1<br>(𝑥𝑖) + N (0, 𝜎2𝐶𝑡<br>2<br>));<br>𝑔<br>𝑔𝑡<br>e𝑡 ←<br>(<br>Í<br>𝑖∈ B𝑡<br>7<br>  B𝑡 |
| ;<br>𝑤𝑛𝑒𝑤<br>= 𝑤𝑡−1<br>− 𝜂𝑡𝑔<br>e𝑡<br>8                                               |
| 𝐵𝑣<br>Poisson sampling a batch<br>with probability<br>;<br>B𝑣<br>9<br>𝑁               |
| Compute loss<br>𝐽<br>(𝑤𝑛𝑒𝑤)<br>and<br>𝐽<br>(𝑤𝑡−1)<br>by batch<br>;<br>B𝑣<br>10        |
| △𝐸<br>= 𝐽<br>(𝑤𝑛𝑒𝑤) −<br>𝐽<br>(𝑤𝑡−1);<br>11                                           |
| △𝐸<br>= min(max(△𝐸,<br>−𝐶𝑣<br>),𝐶𝑣<br>);<br>12                                        |
| 2<br>2<br>△f𝐸<br>= △𝐸<br>+ N (0, 𝜎𝑣<br>· (2𝐶𝑣<br>);<br>)<br>13                        |
| if △f𝐸<br><<br>𝛽<br>· 𝐶𝑣<br>then<br>14                                                |
| = 𝑤𝑛𝑒𝑤;<br>𝑤𝑡<br>15                                                                   |
| 𝑡<br>= 𝑡<br>+ 1;<br>16                                                                |
| else<br>17                                                                            |
| 𝑤𝑡<br>= 𝑤𝑡−1;<br>18                                                                   |
| ;<br>19 return 𝑤𝑡                                                                     |

#### <span id="page-6-15"></span><span id="page-6-14"></span><span id="page-6-13"></span><span id="page-6-12"></span><span id="page-6-11"></span><span id="page-6-10"></span><span id="page-6-9"></span><span id="page-6-8"></span><span id="page-6-0"></span>5 PRIVACY ANALYSIS

This section establishes the privacy guarantee of DPSUR. Since DP-SUR is non-interactive, it only releases the final model accumulated from all accepted model updates. In the following, we first analyze the privacy loss of each accepted model update, and then derive the total privacy loss based on sequential composition.

For each accepted model update in Algorithm [2,](#page-6-2) there are only two places where the raw training data is accessed. One is the computation of model updates in the training phase, and the other is the computation of test values <sup>Δ</sup>f in the validation phase. As shown in Figure [8,](#page-7-0) the model update and test value sequences are in the form of "rejected, ..., rejected, accepted".

In the validation phase, the computation of each test value <sup>Δ</sup>f takes as input the training set and the corresponding model update , and the latter is a function of the training set. Due to the function composition, the computation of <sup>Δ</sup>f can be regarded as a function of the training set whose output is a value in [−, ]. Therefore, Line [13](#page-6-12) in Algorithm [2](#page-6-2) ensures that the computation satisfies differential privacy due to the Gaussian mechanism. Furthermore, computing and testing the values <sup>Δ</sup>f until one value is accepted satisfies the same differential privacy according to Theorem [4.1.](#page-4-7)

In the training phase, since the accepted model update is selected solely based on the test value <sup>Δ</sup>f which satisfies differential privacy, the model update selection satisfies differential privacy due to the post-processing property. Additionally, all rejected model updates are never released and thus consume no privacy budget, even though they have been computed. Therefore, the privacy loss in the training phase comes only from the computation of accepted model updates.

Based on the above analysis, we will use the Rényi Differential Privacy (RDP) approach to calculate the privacy loss in the training and validation phases in Sections [5.1](#page-7-1) and [5.2](#page-7-2) respectively, compose them sequentially, and finally convert the RDP into (, )-DP in Section [5.3.](#page-7-3)

<span id="page-7-0"></span>![](_page_7_Figure_3.jpeg)
<!-- Image Description: The image displays a diagram illustrating a process divided into training, validation, and release phases.  Two sequences (1 and *t*) are shown, each involving multiple weight vectors (*w<sub>i</sub>*) and their associated error terms (ΔE<sub>i</sub>).  The diagram depicts a sequential computation, where intermediate results undergo operations labeled 'RU' and 'AU' before final release.  A separate equation defines *A<sub>α</sub>*, likely a key parameter within the described process. -->

Figure 8: The privacy analysis of DPSUR. (RU: Rejected Update, AU: Accepted Update)

#### <span id="page-7-1"></span>5.1 Privacy Analysis of Training

As mentioned above, the RDP of the training phase is only resulted from the accepted model updates. Theorem [5.1](#page-7-4) gives the proof of RDP in the training phase.

<span id="page-7-4"></span>Theorem 5.1. After accepting model updates, the RDP of the training phase of DPSUR satisfies:

$$
R_{train}(\alpha) = \frac{t}{\alpha - 1} \ln \left[ \sum_{i=0}^{\alpha} \begin{pmatrix} \alpha \\ i \end{pmatrix} (1 - q)^{\alpha - i} q^i \exp \left( \frac{i^2 - i}{2\sigma_t^2} \right) \right],
$$
\n(20)

where = , is noise multiplier of the training phase, and > 1 is the order.

Proof. We will prove this in the following two steps: (i) use the RDP of the sampling Gaussian mechanism to calculate the privacy cost of each accepted model update, which relies on Definitions [5.2](#page-7-5) and [5.3,](#page-7-6) and (ii) use the composition of RDP mechanisms to compute the privacy cost of multiple accepted model updates by Lemma [5.4.](#page-7-7)

Definitions [5.2](#page-7-5) and [5.3](#page-7-6) define Sampled Gaussian Mechanism (SGM) and its Rényi Differential Privacy (RDP), respectively.

<span id="page-7-5"></span>Definition 5.2. (Sampled Gaussian Mechanism (SGM) [\[37\]](#page-12-13)). Let be a function mapping subsets of to R . We define the Sampled Gaussian Mechanism (SGM) parameterized with the sampling rate 0 < ≤ 1 and the > 0 as

$$
SG_{q,\sigma}(S) \triangleq f(\lbrace x : x \in S \text{ is sampled with probability } q \rbrace)
$$
\n
$$
(21)
$$

$$
+\, \mathcal{N}\left(0, \sigma^2 \mathbb{I}^d\right). \tag{21}
$$

In DPSUR, is the clipped gradient evaluation on sampled data points ({ }∈) = Í ∈ (). If is obtained by clipping with a gradient norm bound , then the sensitivity of is .

<span id="page-7-6"></span>Definition 5.3. (RDP privacy budget of SGM [\[37\]](#page-12-13)). Let , , be the Sampled Gaussian Mechanism for some function . If has a sensitivity of 1, , satisfies (, )-RDP if

$$
R \le \frac{1}{\alpha - 1} \ln[ max(A_{\alpha}(q, \sigma), B_{\alpha}(q, \sigma)) ], \tag{22}
$$

where

$$
\begin{cases}\nA_{\alpha}(q,\sigma) \triangleq \mathbb{E}_{z \sim \mu_0} [(\mu(z)/\mu_0(z))^{\alpha}] \\
B_{\alpha}(q,\sigma) \triangleq \mathbb{E}_{z \sim \mu} [(\mu_0(z)/\mu(z))^{\alpha}]\n\end{cases}
$$
\n(23)

with <sup>0</sup> ≜ N 0, <sup>2</sup> , <sup>1</sup> ≜ N 1, <sup>2</sup> and ≜ (1 − )<sup>0</sup> + 1.

Furthermore, it holds for ∀(, ) ∈ (0, 1]×R + , (, ) ≥ (, ). Thus, , satisfies , <sup>1</sup> −1 ln ( (, )) -RDP.

<span id="page-7-8"></span>Finally, the existing work [\[37\]](#page-12-13) describes a procedure to compute (, ) depending on integer as Eq. [\(24\)](#page-7-8).

$$
A_{\alpha} = \sum_{k=0}^{\alpha} \binom{\alpha}{k} (1-q)^{\alpha-k} q^k \exp\left(\frac{k^2 - k}{2\sigma^2}\right) \tag{24}
$$

∆<sup>4</sup> Lemma [5.4](#page-7-7) shows the composition property of RDP mechanisms.

<sup>4</sup> ... Lemma 5.4. (Composition of RDP [\[36\]](#page-12-23)). For two randomized mechanisms , such that is (, 1)-RDP and is (, 2)-RDP the composition of and which is defined as (, )(a sequence of results), where ∼ and ∼ , satisfies (, <sup>1</sup> + 2) −

> <span id="page-7-7"></span>According to Definitions [5.2](#page-7-5) and [5.3,](#page-7-6) and Lemma [5.4,](#page-7-7) Theorem [5.1](#page-7-4) is proved.

$$
\Box
$$

#### <span id="page-7-2"></span>5.2 Privacy Analysis of Validation

As Section [4.1](#page-4-6) mentioned above, the RDP of validation will be accumulated only when <sup>Δ</sup>f <sup>&</sup>lt; · .

<span id="page-7-9"></span>Theorem 5.5. After accepting tests of <sup>Δ</sup>˜, the RDP of the validation phase satisfies:

$$
R_{valid}(\alpha) = \frac{t}{\alpha - 1} \ln \left[ \sum_{i=0}^{\alpha} \left( \begin{array}{c} \alpha \\ i \end{array} \right) (1 - q)^{\alpha - i} q^i \exp \left( \frac{i^2 - i}{2\sigma_v^2} \right) \right], (25)
$$

where = , is noise multiplier of the validation phase, and > 1 is the order.

The proof is similar to that of the training phase, so we omit it.

#### <span id="page-7-3"></span>5.3 Overall Privacy Analysis of DPSUR

Since both training and validation phases access the same training set, we need to combine their RDPs sequentially using Lemma [5.4,](#page-7-7) and then use Lemma [2.7](#page-2-2) to convert it to (, )-DP. Therefore, the final privacy loss of DPSUR is as follows:

Theorem 5.6. (Privacy loss of DPSUR). The privacy loss of DPSUR satisfies:

$$
(\epsilon, \delta) = (R_{train}(\alpha) + R_{valid}(\alpha) + \ln((\alpha - 1)/\alpha) - (\ln \delta + \ln \alpha)/(\alpha - 1), \delta),
$$
\n(26)

where 0 < < 1, () is the RDP of training which is computed by Theorem [5.1,](#page-7-4) and () is the RDP of validation which is computed by Theorem [5.5.](#page-7-9)

#### 5.4 Discussion of Privacy

Our privacy analysis shows that DPSUR strictly adheres to the principles of differential privacy, limiting adversaries to conduct differential attacks solely based on the algorithm's output. However, it is worth noting that DPSUR may be susceptible to interactive side-channel attacks. For instance, a strong adversary (e.g., the hypervisor of a guest OS in the cloud) who has access to DPSUR's internal update/release status could measure the time interval of two adjacent model updates to infer the number of rejections in between and thus cause privacy breaches. To mitigate such threats, we suggest introducing random waiting time for update acceptance cases. Nonetheless, we emphasize that DPSGD is supposed to work in a non-interactive training scenario where the attacker can only access the final output model. Since most real-world machine learning systems are non-interactive during training, the privacy guarantee provided by DPSUR remains sufficient and consistent with other DPSGD variants.

To further validate such privacy guarantee in real-world scenarios, in Section [6.4](#page-9-0) we conduct membership inference attacks on the trained models. The experimental results indicate that DPSUR exhibits strong defense against membership inference attacks, thus safeguarding the privacy of training data.

#### <span id="page-8-0"></span>6 EXPERIMENTAL EVALUATION

In this section, we conduct experiments to demonstrate the performance of DPSUR over four real datasets and popular machine learning models. And we perform experiments involving two member inference attacks to show the privacy-preserving effect of DPSUR. All experiments are implemented in Python using Py-Torch [\[45\]](#page-12-25). Codes to reproduce our experiments are available at [https://github.com/JeffffffFu/DPSUR.](https://github.com/JeffffffFu/DPSUR)

#### 6.1 Experimental Setting

6.1.1 Baseline. We compare DPSUR with DPSGD [\[1\]](#page-12-8) and four state-of-the-art variants, namely DPSGD with important sampling [\[57\]](#page-13-9), handcrafted features [\[53\]](#page-13-17), tempered sigmoid activation [\[41\]](#page-12-26), and adaptive learning rate [\[31\]](#page-12-17), which we refer to as DPSGD-IS, DPSGD-HF, DPSGD-TS, and DPAGD respectively. Note that we do not compare DPSUR with those approaches that modify the structures of over-parameterized models [\[13\]](#page-12-27) or the semi-supervised model PATE [\[39,](#page-12-28) [40\]](#page-12-22), as they differ significantly from the scope of this work.

6.1.2 Datasets and Models. Experimental evaluation is conducted over three image classification datasets, including MNIST [\[30\]](#page-12-29), Fashion MNIST (FMNIST) [\[60\]](#page-13-18), and CIFAR-10 [\[29\]](#page-12-30), and a movie review dataset IMDB [\[33\]](#page-12-31).

MNIST contains 60,000 training samples and 10,000 testing samples of handwritten digits, divided into 10 categories with 7,000 grayscale images per category. Each sample consists of a grayscale image of size 28 × 28 and a corresponding label indicating its category. The model trained using handcrafted features as inputs achieves 99.11% accuracy after 20 epochs in the non-private setting [\[53\]](#page-13-17).

FMNIST consists of 60,000 training samples and 10,000 testing samples of fashion products categorized into 10 categories, with each category containing 7,000 grayscale images of size 28×28. The dataset also includes labels indicating the category of each image. The model trained using handcrafted features as inputs achieves 90.98% accuracy after 20 epochs in the non-private setting [\[53\]](#page-13-17).

CIFAR-10 comprises 50,000 training samples and 10,000 testing samples of colored objects categorized into 10 categories. Each category contains 6,000 color images of size 32 × 32 with three color channels. Additionally, each sample is accompanied by a label indicating the category to which it belongs. The model trained using handcrafted features as inputs achieves 71.12% accuracy after 20 epochs in the non-private setting [\[53\]](#page-13-17).

IMDb consists of 50,000 reviews of movies, each review encoded as a list of word indexes and labeled with an obvious bias towards either positive or negative sentiment. The dataset is divided into a training set of 25,000 reviews and a test set of 25,000 reviews. In the non-private setting, the model trained using cross-entropy loss function, Adam optimizer, and an expected batch size of 32 achieves an accuracy of 79.97% after 20 epochs.

We apply the same convolutional neural network architecture as [\[41,](#page-12-26) [53,](#page-13-17) [57\]](#page-13-9) to three image datasets, i.e., MNIST, FMNIST, and CIFAR-10. Additionally, we used a same five-layer recurrent neural network as in [\[57\]](#page-13-9) for the IMDB dataset. We use the categorical cross-entropy loss function for all datasets. The details of model architectures are presented in Appendix [B.](#page-14-0)

<span id="page-8-1"></span>Table 1: Noise multiplier for validation

| Dataset  | = 1<br>𝜖 | = 2<br>𝜖 | = 3<br>𝜖 | = 4<br>𝜖 |
|----------|----------|----------|----------|----------|
| MNIST    | 1.3      | 1.0      | 0.9      | 0.8      |
| FMNIST   | 1.3      | 1.3      | 0.8      | 0.8      |
| CIFAR-10 | 1.3      | 1.3      | 1.1      | 1.1      |
| IMDB     | 1.3      | 1.2      | 1.0      | 0.9      |

6.1.3 Parameter Settings. In our experiments, we set the privacy budget from 1 to 4 for each dataset while fixing = 10−<sup>5</sup> . For image datasets, we user the SGD optimizer with a momentum parameter set to 0.9; for the IMDB dataset, we employ the Adam optimizer whose parameters are the same as [\[11\]](#page-12-32).

During the DPSGD phase, for the three image datasets, we adopt the best parameters recommended in [\[53\]](#page-13-17). Specifically, we finetune the noise multiplier for various , following the approach outlined in [\[53,](#page-13-17) [57\]](#page-13-9). This fine-tuning process is a common practice in all privacy-preserving machine learning methods, and it does not incur any privacy loss. For the IMDB dataset, we enumerate different values and choose the best for each parameter since the competitor method [\[57\]](#page-13-9) does nshiot specify them.

Based on our analysis in Section [3.2](#page-3-0) and [3.3,](#page-4-1) we set the clipping bound = 0.001 for Δ and acceptance parameter = −1 to all privacy budgets and datasets. In addition, for MNIST, FMNIST and CIFAR-10, we set the batch size of validation set = 256. While IMDB, which have fewer training samples, we set the batch size of validation set = 128. The noise multiplier for validation ranges from 0.8 to 1.3 for all datasets and privacy budgets, as shown in Table [1.](#page-8-1) Intuitively, when the privacy budget is small, we increase to add more iteration rounds.

#### 6.2 Overall Performance

Table [2](#page-10-1) shows the classification accuracies of DPSUR and five competitive methods[.](#page-0-0) It is noteworthy that DPSUR consistently outperforms all competitors across all datasets and privacy budgets, except for a less eminent advantage on the MNIST dataset where the accuracy of [\[57\]](#page-13-9) already approaches that of the non-private setting, leaving little room for further improvement. For the other three datasets, the classification accuracy of DPSUR is at least 1% higher than the second best, which shows a huge improvement over DPSGD.

Notably, DPSUR performs almost as well as in the non-private setting at = 4 in three image datasets. The superior performance of the DPSUR is attributed to our objective of selecting model updates to minimize the loss function. Moreover, We derive the RDP for the selective Gaussian mechanism, which allows us to reduce the consumption of privacy loss. In particular, on the CIFAR-10 dataset, we observe that DPSUR even outperforms non-private results when = 4. This is because moderate noise in SGD sometimes helps the neural network escape from local minima [\[22\]](#page-12-33).

#### 6.3 Impact of Various Parameters

In this subsection, we study the impact of various parameters of DPSUR, including the learning rate, the noise multiplier of validation, the cilpping bound of loss, and the threshold parameter. Due to space limitation, we only show the results of CIFAR-10 dataset. In all experiments, if not specified, we use the SGD optimizer with the momentum 0.9, and set the learning rate = 4.0, batch size for training = 8192, noise multiplier for training = 5.67, batch size for validation = 128, noise multiplier for validation = 1.1, clipping bound for validation = 0.001, the threshold parameter = −1, and privacy budget (3, 10−<sup>5</sup> ).

Learning rate . As plotted in Figure [9a,](#page-10-0) the highest accuracy achieved is 70.83% when using a learning rate of = 4. If the learning rate is larger than 4, the accuracy starts to decrease. This is because a large learning rate may cause slow convergence to the trained model. However, thanks to selective update, DPSUR becomes adaptive to different learning rates, and the accuracy remains stable at 70.02% when using a extremely high learning rate = 7.

Noise multiplier for validation . A large can save privacy budget running more rounds, which degrades the quality of the accepted model. On the contrary, a small can guarantee the accepted model quality, but consumes more privacy budget. According to Figure [9b,](#page-10-0) we find that the test accuracy of DPSUR is

quite stable at around 70.3% when increases from 0.8 to 1.3, and the highest accuracy is 70.83% when = 1.1.

Clipping bound for validation . As aforementioned, using a sufficiently small clipping bound can discretize the difference of the loss Δ. With a shallow model training on CIFAR-10, loss values ranging from 0.01 to 0.0001 are all considered sufficiently small, a smaller (e.g. 1 − 05) than the front does not bring performance gains. As shown in Figure [9c,](#page-10-0) the accuracy for the cases of ∈ [0.01, 1 − 05] achieves slightly better performance. However, when is set to 1 or 10, we observe a significant decline in performance, which is consistent with our analysis that setting a large does not provide any performance benefits.

Threshold parameter . The acceptance probability is influenced by the parameter , with smaller values leading to a decreasing probability of accepting both low-quality and high-quality models. As shown in Figure [9d,](#page-10-0) the best performance is achieved when = −1.0. This is consistent with our analysis in Section [3.3](#page-4-1) that a smaller leads to a higher rejection probability for lowquality updates, thereby guiding the model towards the correct direction during iterations. It is worth noting that setting too small does not gain more benefits, as a very small causes the model to reject almost all high-quality and low-quality solutions, contributing nothing to the model convergence.

Batch size of validation set . A small can help conserve the privacy budget, enabling more rounds of computation. However, this can result in a decrease in the quality of the accepted model. Conversely, a larger value of can ensure better model quality but consumes a greater portion of the privacy budget. As shown in Figure [9e,](#page-10-0) we observe that as increases from 32 to 256, the test accuracy of DPSUR improves from 69.10% to 70.83%, but it declines to 68.36% when = 1024.

# <span id="page-9-0"></span>6.4 Resilience Against Member Inference Attacks

Differential privacy protection is naturally resistant to membership inference attacks. To empirically verify if DPSUR achieves the same privacy guarantee as DPSGD, we conduct membership inference attacks on models trained on FMNIST and CIFAR-10, where their models are trained from DPSUR and DPSGD algorithms, respectively.

6.4.1 Attack overview. We adopt two membership inference attacks, Black-Box/Shadow [\[46\]](#page-12-34) and White-Box/Partial [\[38\]](#page-12-3), which are the SOTA methods in membership inference attack to our knowledge.

Black-Box/Shadow. In the Black-Box/Shadow attack scenario, the adversary has a shadow auxiliary dataset. The dataset is divided into two parts, with one part used to train a shadow model for the same task. The shadow model is then queried using the entire shadow dataset. For each query sample, the shadow model provides its posterior probability and predicted label. The adversary labels the sample as a member if it belongs to the training set of the shadow model, otherwise, it is labeled as a non-member. Using this labeled dataset, the adversary trains an attack model, which serves as a binary classifier to distinguish between members and nonmembers. To determine if a sample belongs to the target model's training dataset, it is inputted into the target model for prediction.

Since the scattering network used in DPSGD-HF [\[53\]](#page-13-17) is not applicable to natural language processing, we omit the results of this method on the IMDb dataset.

<span id="page-10-1"></span>

| Dataset         | Method        | = 1<br>𝜖 | = 2<br>𝜖 | = 3<br>𝜖 | = 4<br>𝜖 | non-private |
|-----------------|---------------|----------|----------|----------|----------|-------------|
| MNIST           | DPSUR         | 97.93%   | 98.70%   | 98.88%   | 98.95%   |             |
| (Image Dataset) | DPIS [57]     | 97.79%   | 98.51%   | 98.62%   | 98.78%   |             |
|                 | DPSGD-HF [53] | 97.78%   | 98.39%   | 98.32%   | 98.56%   | 99.11%      |
|                 | DPSGD-TS [41] | 97.06%   | 97.87%   | 98.22%   | 98.51%   |             |
|                 | DPAGD [31]    | 95.91%   | 97.30%   | 97.52%   | 97.83%   |             |
|                 | DPSGD [1]     | 95.11%   | 96.10%   | 96.82%   | 97.25%   |             |
| FMNIST          | DPSUR         | 88.38%   | 89.34%   | 89.71%   | 90.18%   |             |
| (Image Dataset) | DPIS [57]     | 86.25%   | 88.24%   | 88.82%   | 89.21%   |             |
|                 | DPSGD-HF [53] | 85.54%   | 87.96%   | 89.01%   | 89.06%   | 90.98%      |
|                 | DPSGD-TS [41] | 83.63%   | 85.33%   | 86.29%   | 86.86%   |             |
|                 | DPAGD [31]    | 81.26%   | 84.50%   | 86.04%   | 86.78%   |             |
|                 | DPSGD [1]     | 80.25%   | 82.63%   | 84.72%   | 85.40%   |             |
| CIFAR-10        | DPSUR         | 64.41%   | 69.40%   | 70.83%   | 71.45%   |             |
| (Image Dataset) | DPIS [57]     | 63.23%   | 67.94%   | 69.63%   | 70.55%   |             |
|                 | DPSGD-HF [53] | 63.15%   | 66.55%   | 69.35%   | 70.28%   | 71.12%      |
|                 | DPSGD-TS [41] | 51.52%   | 56.78%   | 60.42%   | 61.75%   |             |
|                 | DPAGD [31]    | 45.78%   | 53.30%   | 56.21%   | 60.31%   |             |
|                 | DPSGD [1]     | 46.03%   | 51.33%   | 54.67%   | 58.89%   |             |
| IMDb            | DPSUR         | 66.50%   | 71.02%   | 72.16%   | 74.14%   |             |
| (Text Dataset)  | DPIS [57]     | 63.56%   | 66.11%   | 68.49%   | 70.12%   |             |
|                 | DPSGD-TS [41] | 65.08%   | 68.34%   | 70.10%   | 70.85%   | 79.97%      |
|                 | DPAGD [31]    | 58.72%   | 63.48%   | 64.59%   | 66.01%   |             |
|                 | DPSGD [1]     | 64.13%   | 68.55%   | 70.41%   | 71.57%   |             |

#### Table 2: Results of classification accuracy

<span id="page-10-0"></span>![](_page_10_Figure_2.jpeg)
<!-- Image Description: The image presents five line graphs (a-e) illustrating the impact of hyperparameter tuning on a DPSUR model's test accuracy.  Each graph plots test accuracy (%) against a different hyperparameter: learning rate (η), noise multiplier (σ<sub>v</sub>), clipping bound (C<sub>v</sub>), threshold parameter (β), and validation set batch size (B<sub>v</sub>). The purpose is to show the model's sensitivity to these parameters and to guide optimal hyperparameter selection for improved performance. -->

Figure 9: The impact of different parameters on the test accuracy in CIFAR-10.

The resulting posterior probability and predicted label (converted into a binary indicator of prediction correctness) are then fed into the attack model.

White-Box/Partial. In the White-Box/Partial attack scenario, the adversary has partial training dataset as the auxiliary dataset. One advantage in the White-Box/Partial attack is that the adversary has access to the target model. This allows adversary to utilize various resources, including gradients with respect to model parameters, embeddings from intermediate layers, classification loss, as well as posterior probabilities and labels of the target samples.

6.4.2 Attack setting. For each dataset, we randomly split it into four subsets: the target training dataset, target testing dataset, shadow training dataset, and shadow testing dataset. The ratio of the sample sizes in each subset is 2:1:2:1. Our target model and training parameters are consistent with those described above.

6.4.3 Results. Table [3](#page-11-2) and Table [4](#page-11-3) report the accuracy of two inference attacks against target models protected by DPSUR and DPSGD on FMNIST and CIFAR-10, respectively. We observe that member inference attacks are quite effective against the non-private methods (non-dp), especially on CIFRA-10. As for the two DP algorithms, the attack accuracy drops from 0.58 to around 0.50 on the FMNIST, and drops from 0.73 to around 0.50 on the CIFAR-10, which almost equals to random guess. It's noteworthy that the attack performance on FMNIST is consistently poor, as models trained on FMNIST generalize well on non-member data samples [\[48\]](#page-13-19). These results show that the model under DP protection can defend very well against membership inference attacks, and our DPSUR algorithm can provide the same level of privacy protection as DPSGD.

<span id="page-11-2"></span>Table 3: Accuracy of Member Inference Attack on FMNIST

| Attack      | Algorithm | 𝜖 = 1 | 𝜖 = 2 | 𝜖 = 3 | 𝜖 = 4 | non-private |
|-------------|-----------|-------|-------|-------|-------|-------------|
| Black       | DPSUR     | 0.498 | 0.500 | 0.503 | 0.506 | 0.582       |
| Box/Shadow  | DPSGD     | 0.498 | 0.503 | 0.493 | 0.494 |             |
| White       | DPSUR     | 0.499 | 0.504 | 0.501 | 0.502 | 0.584       |
| Box/Partial | DPSGD     | 0.501 | 0.502 | 0.502 | 0.505 |             |

<span id="page-11-3"></span>Table 4: Accuracy of Member Inference Attack on CIFAR-10

| Attack      | Algorithm | 𝜖 = 1 | 𝜖 = 2 | 𝜖 = 3 | 𝜖 = 4 | non-private |
|-------------|-----------|-------|-------|-------|-------|-------------|
| Black       | DPSUR     | 0.495 | 0.498 | 0.503 | 0.504 | 0.732       |
| Box/Shadow  | DPSGD     | 0.504 | 0.505 | 0.504 | 0.505 |             |
| White       | DPSUR     | 0.499 | 0.501 | 0.502 | 0.503 | 0.743       |
| Box/Partial | DPSGD     | 0.500 | 0.501 | 0.501 | 0.503 |             |

#### <span id="page-11-0"></span>7 RELATED WORK

Privacy-preserving model training was first proposed in [\[5,](#page-12-35) [50\]](#page-13-20). Subsequently, Abadi et al. [\[1\]](#page-12-8) proposed a generalized algorithm, DPSGD, for deep learning with differential privacy, and since then many works aimed at improving DPSGD from different aspects.

Gradient clipping. At each iteration of training, Zhang et al. [\[68\]](#page-13-21) used public data to obtain an approximate bound on gradient norm and clip the gradients at this approximate bound. The work in [\[55\]](#page-13-22) proposed adaptive clipping in each layer of the neural network. Andrew et al. [\[2\]](#page-12-36) designed a method for adaptively tuning the clipping threshold to track a given quantile of the update norm distribution during training, especially in federated learning. Venkatadheeraj et al. [\[44\]](#page-12-37) proposed AdaCliP, which using coordinate-wise adaptive clipping of the gradient. However, a recent work [\[62\]](#page-13-23) has shown that by redefining the clipping equation as () = /||||2, clipping is actually equivalent to normalization by setting the clipping bound small enough.

Our paper does not employ any adaptive clipping technique during the training phase. Instead, our minimal clipping is orthogonal to theirs as it is for threshold evaluation in the validation phase, not the training phase.

Gaussian noise. The work of [\[42\]](#page-12-38) implemented adaptive noise addition using a hierarchical correlation propagation protocol approach, adding a small amount of noise to features with high correlation to the model's output. Balle and Wang [\[4\]](#page-12-39) introduced an optimized Gaussian mechanism that directly calibrates variance using the Gaussian cumulative density function instead of relying on a tail-bound approximation. Their work is orthogonal to ours and can be incorporated ours as the underlying perturbation mechanism. Lee et al. [\[31\]](#page-12-17) selected the best learning rate from a candidate set based on model evaluation and implemented adaptive privacy budget allocation in each round of DPSGD training. While both our work and theirs involve adaptive DPSGD, there are three significant distinctions. First, their adaptiveness is from adaptive learning rates, which modifies the gradient descent's step size but not its direction. Second, the DP privacy guarantee is different. Ours relies on differences in loss values before and after iterations, whereas theirs adopts NoisyMax[\[18\]](#page-12-40) method on loss values from a variety of models obtained through different learning rates in a single iteration. In contrast, we aim to ensure each gradient descent moves in the desired direction through resampling and re-noising. Third, we do not perform adaptive privacy budget allocation but instead introduce selective release techniques to preserve the privacy budget.Further, Xu et al. [\[61\]](#page-13-10) employed the Root Mean Square Prop (RMSProp) gradient descent technique to adaptively add noise to coordinates of the gradient. Since then, many works [\[23,](#page-12-41) [65,](#page-13-11) [71\]](#page-13-24) have focused on reducing the dimensionality of the model during training to reduce the impact of noise on the overall model.

Poisson sampling. Wei et al. [\[57\]](#page-13-9) first explored the problem of bias due to Poisson sampling in DPSGD and proposed DPIS, which weights the importance sampling by the gradient norm of the sample. Our algorithm mitigates the impact of Poisson sampling on convergence speed through the process of resampling.

Models, pre-processing and parameter tuning. Papernot et al. [\[41\]](#page-12-26) found that using a family of bounded activation functions (tempered sigmoids) instead of the unbounded activation function ReLU in DPSGD can achieve good performance. Tramer et al. [\[53\]](#page-13-17) used Scattering Network to traverse the image in advance to extract features before DPSGD training. Soham et al. [\[13\]](#page-12-27) combined careful hyper-parameter tuning with group normalization and weight standardization to yield remarkable performance benefits. These works are orthogonal to our work.

Privacy accounting. Abadi et al. [\[1\]](#page-12-8) proposed a method called the Moments Accountant (MA) for giving an upper bound the privacy curve of a composition of DPSGD. The Moments Accountant was subsumed into the framework of Renyi Differential Privacy (RDP) introduced by [\[36\]](#page-12-23). Bu et al. [\[7\]](#page-12-42) introduced the notion of Gaussian Differential Privacy (GDP) base hypothesis test. There also exits other variants of DP, for example Concentrated DP (CDP) [\[8\]](#page-12-43) and zero Concentrated-DP [\[8\]](#page-12-43). These variants are tailored for specific scenarios and can be converted into one another under certain conditions. Our primary focus is on (, )-differential privacy, as it is the most prevalent and widely adopted in both academic literature and practical applications. Besides, many works [\[14,](#page-12-44) [15,](#page-12-45) [63,](#page-13-25) [64,](#page-13-26) [69\]](#page-13-27) based on local differential privacy focus on - differential privacy.

#### <span id="page-11-1"></span>8 CONCLUSION

We propose DPSUR, a differentially private scheme for deep learning based on selective update and release. Our scheme utilizes the validation test to select appropriate model updates in each iteration, thereby speeding up model convergence and enhancing utility. To reduce the injected Gaussian noise, we incorporate a clipping strategy and a threshold mechanism for gradient selection in each iteration. Furthermore, we apply the Gaussian mechanism with selective release to reduce privacy budget consumption across iterations. We conduct a comprehensive privacy analysis of our approach using RDP and validate our scheme through extensive experiments. The results indicate that DPSUR significantly outperforms state-of-theart solutions in terms of model utility and downstream tasks. Our scheme is widely applicable to various neural networks, and can serve as a flexible optimizer for new DPSGD variants. For future work, we plan to extend DPSUR to larger models and datasets and theoretically analyze its convergence speed.

#### ACKNOWLEDGMENTS

This work was support by the Natural Science Foundation of Shanghai (Grant No. 22ZR1419100), CAAI-Huawei MindSpore Open Fund (Grant No. CAAIXSJLJJ-2022-005A), National Natural Science Foundation of China Key Program (Grant No. 62132005), National Natural Science Foundation of China (Grant No: 92270123 and 62372122), and the Research Grants Council, Hong Kong SAR, China (Grant No: 15209922, 15208923 and 15210023).

## REFERENCES

- <span id="page-12-8"></span>[1] Martin Abadi, Andy Chu, Ian Goodfellow, H Brendan McMahan, Ilya Mironov, Kunal Talwar, and Li Zhang. 2016. Deep learning with differential privacy. In Proceedings of the 2016 ACM SIGSAC conference on computer and communications security. 308–318.
- <span id="page-12-36"></span>[2] Galen Andrew, Om Thakkar, Brendan McMahan, and Swaroop Ramaswamy. 2021. Differentially private learning with adaptive clipping. Advances in Neural Information Processing Systems 34 (2021), 17455–17466.
- <span id="page-12-24"></span>[3] Borja Balle, Gilles Barthe, Marco Gaboardi, Justin Hsu, and Tetsuya Sato. 2020. Hypothesis testing interpretations and renyi differential privacy. In International Conference on Artificial Intelligence and Statistics. PMLR, 2496–2506.
- <span id="page-12-39"></span>[4] Borja Balle and Yu-Xiang Wang. 2018. Improving the gaussian mechanism for differential privacy: Analytical calibration and optimal denoising. In International Conference on Machine Learning. PMLR, 394–403.
- <span id="page-12-35"></span>[5] Raef Bassily, Adam Smith, and Abhradeep Thakurta. 2014. Private empirical risk minimization: Efficient algorithms and tight error bounds. In 2014 IEEE 55th annual symposium on foundations of computer science. IEEE, 464–473.
- <span id="page-12-14"></span>[6] Léon Bottou. 2009. Curiously fast convergence of some stochastic gradient descent algorithms. In Proceedings of the symposium on learning and data science, Paris, Vol. 8. Citeseer, 2624–2633.
- <span id="page-12-42"></span>[7] Zhiqi Bu, Jinshuo Dong, Qi Long, and Weijie J Su. 2020. Deep learning with gaussian differential privacy. Harvard data science review 2020, 23 (2020), 10– 1162.
- <span id="page-12-43"></span>[8] Mark Bun and Thomas Steinke. 2016. Concentrated Differential Privacy: Simplifications, Extensions, and Lower Bounds. 635–658. [https://doi.org/10.1007/978-3-](https://doi.org/10.1007/978-3-662-53641-4_24) [662-53641-4\\_24](https://doi.org/10.1007/978-3-662-53641-4_24)
- <span id="page-12-9"></span>[9] Nicholas Carlini, Chang Liu, Úlfar Erlingsson, Jernej Kos, and Dawn Song. 2019. The secret sharer: Evaluating and testing unintended memorization in neural networks. In 28th USENIX Security Symposium (USENIX Security 19). 267–284.
- <span id="page-12-1"></span>[10] Mia Xu Chen, Benjamin N Lee, Gagan Bansal, Yuan Cao, Shuyuan Zhang, Justin Lu, Jackie Tsay, Yinan Wang, Andrew M Dai, Zhifeng Chen, et al. 2019. Gmail smart compose: Real-time assisted writing. In Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining. 2287– 2295.
- <span id="page-12-32"></span>[11] François Chollet et al. 2015. Keras. [https://keras.io.](https://keras.io)
- <span id="page-12-6"></span>[12] Rachel Cummings and Deven Desai. 2018. The role of differential privacy in gdpr compliance. In FAT'18: Proceedings of the Conference on Fairness, Accountability, and Transparency. 20.
- <span id="page-12-27"></span>[13] Soham De, Leonard Berrada, Jamie Hayes, Samuel L Smith, and Borja Balle. 2022. Unlocking high-accuracy differentially private image classification through scale. arXiv preprint arXiv:2204.13650 (2022).
- <span id="page-12-44"></span>[14] Rong Du, Qingqing Ye, Yue Fu, Haibo Hu, Jin Li, Chengfang Fang, and Jie Shi. 2023. Differential Aggregation against General Colluding Attackers. In Proceedings of the IEEE International Conference on Data Engineering.
- <span id="page-12-45"></span>[15] Jiawei Duan, Qingqing Ye, and Haibo Hu. 2022. Utility analysis and enhancement of LDP mechanisms in high-dimensional space. In 2022 IEEE 38th International Conference on Data Engineering (ICDE). IEEE, 407–419.
- <span id="page-12-20"></span>[16] Cynthia Dwork. 2011. A firm foundation for private data analysis. Commun. ACM 54, 1 (2011), 86–95.
- <span id="page-12-21"></span>[17] Cynthia Dwork, Frank McSherry, Kobbi Nissim, and Adam Smith. 2006. Calibrating noise to sensitivity in private data analysis. In Theory of Cryptography: Third Theory of Cryptography Conference, TCC 2006, New York, NY, USA, March 4-7, 2006. Proceedings 3. Springer, 265–284.
- <span id="page-12-40"></span>[18] Cynthia Dwork and Aaron Roth. 2014. The Algorithmic Foundations of Differential Privacy. TCS 9 (2014), 211–407. Issue 3-4.
- <span id="page-12-7"></span>[19] Cynthia Dwork, Aaron Roth, et al. 2014. The algorithmic foundations of differential privacy. Foundations and Trends® in Theoretical Computer Science 9, 3–4 (2014), 211–407.
- <span id="page-12-10"></span>[20] Vitaly Feldman. 2020. Does learning require memorization? a short tale about a long tail. In Proceedings of the 52nd Annual ACM SIGACT Symposium on Theory of Computing. 954–959.
- <span id="page-12-2"></span>[21] Matt Fredrikson, Somesh Jha, and Thomas Ristenpart. 2015. Model inversion attacks that exploit confidence information and basic countermeasures. In Proceedings of the 22nd ACM SIGSAC conference on computer and communications security. 1322–1333.

- <span id="page-12-33"></span>[22] Rong Ge, Furong Huang, Chi Jin, and Yang Yuan. 2015. Escaping from saddle points—online stochastic gradient for tensor decomposition. In Conference on learning theory. PMLR, 797–842.
- <span id="page-12-41"></span>[23] Aditya Golatkar, Alessandro Achille, Yu-Xiang Wang, Aaron Roth, Michael Kearns, and Stefano Soatto. 2022. Mixed differential privacy in computer vision. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 8376–8386.
- <span id="page-12-15"></span>[24] Mert Gürbüzbalaban, Asu Ozdaglar, and Pablo A Parrilo. 2021. Why random reshuffling beats stochastic gradient descent. Mathematical Programming 186 (2021), 49–84.
- <span id="page-12-11"></span>[25] Bargav Jayaraman and David Evans. 2019. Evaluating differentially private machine learning in practice. In 28th USENIX Security Symposium (USENIX Security 19). 1895–1912.
- <span id="page-12-16"></span>[26] Angelos Katharopoulos and François Fleuret. 2018. Not all samples are created equal: Deep learning with importance sampling. In International conference on machine learning. PMLR, 2525–2534.
- <span id="page-12-18"></span>[27] Scott Kirkpatrick, C Daniel Gelatt Jr, and Mario P Vecchi. 1983. Optimization by simulated annealing. science 220, 4598 (1983), 671–680.
- <span id="page-12-12"></span>[28] Antti Koskela and Antti Honkela. 2018. Learning rate adaptation for differentially private stochastic gradient descent.
- <span id="page-12-30"></span>[29] A. Krizhevsky and G. Hinton. 2009. Learning multiple layers of features from tiny images. Master's thesis, Department of Computer Science, University of Toronto (2009).
- <span id="page-12-29"></span>[30] Yann LeCun, Corinna Cortes, and CJ Burges. 2010. MNIST handwritten digit database. ATT Labs [Online]. Available: http://yann.lecun.com/exdb/mnist 2 (2010).
- <span id="page-12-17"></span>[31] Jaewoo Lee and Daniel Kifer. 2018. Concentrated differentially private gradient descent with adaptive per-iteration privacy budget. In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining. 1656–1665.
- <span id="page-12-0"></span>[32] Alexander Selvikvåg Lundervold and Arvid Lundervold. 2019. An overview of deep learning in medical imaging focusing on MRI. Zeitschrift für Medizinische Physik 29, 2 (2019), 102–127.
- <span id="page-12-31"></span>[33] Andrew L. Maas, Raymond E. Daly, Peter T. Pham, Dan Huang, Andrew Y. Ng, and Christopher Potts. 2011. Learning Word Vectors for Sentiment Analysis. In The 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies, Proceedings of the Conference, 19-24 June, 2011, Portland, Oregon, USA. The Association for Computer Linguistics, 142–150.
- <span id="page-12-5"></span>[34] Luca Melis, Congzheng Song, Emiliano De Cristofaro, and Vitaly Shmatikov. 2019. Exploiting unintended feature leakage in collaborative learning. In 2019 IEEE symposium on security and privacy (SP). IEEE, 691–706.
- <span id="page-12-19"></span>[35] Nicholas Metropolis, Arianna W Rosenbluth, Marshall N Rosenbluth, Augusta H Teller, and Edward Teller. 1953. Equation of state calculations by fast computing machines. The journal of chemical physics 21, 6 (1953), 1087–1092.
- <span id="page-12-23"></span>[36] Ilya Mironov. 2017. Rényi differential privacy. In 2017 IEEE 30th computer security foundations symposium (CSF). IEEE, 263–275.
- <span id="page-12-13"></span>[37] Ilya Mironov, Kunal Talwar, and Li Zhang. 2019. Rényi Differential Privacy of the Sampled Gaussian Mechanism. arXiv: Learning (2019).
- <span id="page-12-3"></span>[38] Milad Nasr, Reza Shokri, and Amir Houmansadr. 2019. Comprehensive privacy analysis of deep learning: Passive and active white-box inference attacks against centralized and federated learning. In 2019 IEEE symposium on security and privacy (SP). IEEE, 739–753.
- <span id="page-12-28"></span>[39] Nicolas Papernot, Martın Abadi, Ulfar Erlingsson, Ian Goodfellow, and Kunal Talwar. 2017. SEMI-SUPERVISED KNOWLEDGE TRANSFER FOR DEEP LEARN-ING FROM PRIVATE TRAINING DATA. stat 1050 (2017), 3.
- <span id="page-12-22"></span>[40] Nicolas Papernot, Shuang Song, Ilya Mironov, Ananth Raghunathan, Kunal Talwar, and Úlfar Erlingsson. 2018. Scalable private learning with pate. arXiv preprint arXiv:1802.08908 (2018).
- <span id="page-12-26"></span>[41] Nicolas Papernot, Abhradeep Thakurta, Shuang Song, Steve Chien, and Úlfar Erlingsson. 2021. Tempered sigmoid activations for deep learning with differential privacy. In Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 35. 9312–9321.
- <span id="page-12-38"></span>[42] NhatHai Phan, Xintao Wu, Han Hu, and Dejing Dou. 2017. Adaptive laplace mechanism: Differential privacy preservation in deep learning. In 2017 IEEE international conference on data mining (ICDM). IEEE, 385–394.
- <span id="page-12-4"></span>[43] Le Trieu Phong, Yoshinori Aono, Takuya Hayashi, Lihua Wang, and Shiho Moriai. 2017. Privacy-preserving deep learning: Revisited and enhanced. In Applications and Techniques in Information Security: 8th International Conference, ATIS 2017, Auckland, New Zealand, July 6–7, 2017, Proceedings. Springer, 100–110.
- <span id="page-12-37"></span>[44] Venkatadheeraj Pichapati, Ananda Theertha Suresh, Felix X Yu, Sashank J Reddi, and Sanjiv Kumar. 2019. AdaCliP: Adaptive clipping for private SGD. arXiv preprint arXiv:1908.07643 (2019).
- <span id="page-12-25"></span>[45] Automatic Differentiation In Pytorch. 2018. Pytorch.
- <span id="page-12-34"></span>[46] Ahmed Salem, Yang Zhang, Mathias Humbert, Pascal Berrang, Mario Fritz, and Michael Backes. 2019. ML-Leaks: Model and Data Independent Membership Inference Attacks and Defenses on Machine Learning Models. In Network and Distributed Systems Security (NDSS) Symposium 2019.

- <span id="page-13-6"></span>[47] Reza Shokri and Vitaly Shmatikov. 2015. Privacy-preserving deep learning. In Proceedings of the 22nd ACM SIGSAC conference on computer and communications security. 1310–1321.
- <span id="page-13-19"></span>[48] Reza Shokri, Marco Stronati, Congzheng Song, and Vitaly Shmatikov. 2017. Membership inference attacks against machine learning models. In 2017 IEEE symposium on security and privacy (SP). IEEE, 3–18.
- <span id="page-13-5"></span>[49] Congzheng Song, Thomas Ristenpart, and Vitaly Shmatikov. 2017. Machine learning models that remember too much. (2017), 587–601.
- <span id="page-13-20"></span>[50] Shuang Song, Kamalika Chaudhuri, and Anand D Sarwate. 2013. Stochastic gradient descent with differentially private updates. In 2013 IEEE global conference on signal and information processing. IEEE, 245–248.
- <span id="page-13-7"></span>[51] Pierre Stock, Igor Shilov, Ilya Mironov, and Alexandre Sablayrolles. 2022. Defending against Reconstruction Attacks with Rényi Differential Privacy. arXiv e-prints (2022), arXiv–2202.
- <span id="page-13-0"></span>[52] Kenji Suzuki. 2017. Overview of deep learning in medical imaging. Radiological physics and technology 10, 3 (2017), 257–273.
- <span id="page-13-17"></span>[53] Florian Tramer and Dan Boneh. 2020. Differentially Private Learning Needs Better Features (or Much More Data). In International Conference on Learning Representations.
- <span id="page-13-15"></span>[54] Tim Van Erven and Peter Harremos. 2014. Rényi divergence and Kullback-Leibler divergence. IEEE Transactions on Information Theory 60, 7 (2014), 3797–3820.
- <span id="page-13-22"></span>[55] KoenS.vander Veen, Ruben Seggers, Peter Bloem, and Giorgio Patrini. 2018. Three Tools for Practical Differential Privacy.
- <span id="page-13-3"></span>[56] Zhibo Wang, Mengkai Song, Zhifei Zhang, Yang Song, Qian Wang, and Hairong Qi. 2019. Beyond inferring class representatives: User-level privacy leakage from federated learning. In IEEE INFOCOM 2019-IEEE conference on computer communications. IEEE, 2512–2520.
- <span id="page-13-9"></span>[57] Jianxin Wei, Ergute Bao, Xiaokui Xiao, and Yin Yang. 2022. Dpis: An enhanced mechanism for differentially private sgd with importance sampling. In Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security. 2885–2899.
- <span id="page-13-2"></span>[58] Shaomei Wu, Hermes Pique, and Jeffrey Wieland. 2016. Using artificial intelligence to help blind people 'see'facebook.
- <span id="page-13-8"></span>[59] Liyao Xiang, Jingbo Yang, and Baochun Li. 2019. Differentially-private deep learning from an optimization perspective. In IEEE INFOCOM 2019-IEEE Conference on Computer Communications. IEEE, 559–567.
- <span id="page-13-18"></span>[60] Han Xiao, Kashif Rasul, and Roland Vollgraf. 2017. Fashion-MNIST: a Novel Image Dataset for Benchmarking Machine Learning Algorithms. arXiv e-prints (2017), arXiv–1708.
- <span id="page-13-10"></span>[61] Zhiying Xu, Shuyu Shi, Alex X Liu, Jun Zhao, and Lin Chen. 2020. An adaptive and fast convergent approach to differentially private deep learning. In IEEE INFOCOM 2020-IEEE Conference on Computer Communications. IEEE, 1867–1876.
- <span id="page-13-23"></span>[62] Xiaodong Yang, Huishuai Zhang, Wei Chen, and Tie-Yan Liu. 2022. Normalized/clipped sgd with perturbation for differentially private non-convex optimization. arXiv preprint arXiv:2206.13033 (2022).
- <span id="page-13-25"></span>[63] Qingqing Ye, Haibo Hu, Kai Huang, Man Ho Au, and Qiao Xue. 2023. Stateful switch: Optimized time series release with local differential privacy. In IEEE INFOCOM 2023-IEEE Conference on Computer Communications. IEEE, 1–10.
- <span id="page-13-26"></span>[64] Qingqing Ye, Haibo Hu, Xiaofeng Meng, Huadi Zheng, Kai Huang, Chengfang Fang, and Jie Shi. 2023. PrivKVM\*: Revisiting Key-Value Statistics Estimation With Local Differential Privacy. IEEE Transactions on Dependable and Secure Computing (Jan 2023), 17–35.<https://doi.org/10.1109/tdsc.2021.3107512>
- <span id="page-13-11"></span>[65] Da Yu, Huishuai Zhang, Wei Chen, and Tie-Yan Liu. 2020. Do not Let Privacy Overbill Utility: Gradient Embedding Perturbation for Private Learning. In International Conference on Learning Representations.
- <span id="page-13-13"></span>[66] Lei Yu, Ling Liu, Calton Pu, Mehmet Emre Gursoy, and Stacey Truex. 2019. Differentially private model publishing for deep learning. In 2019 IEEE symposium on security and privacy (SP). IEEE, 332–349.
- <span id="page-13-12"></span>[67] Jianyi Zhang, Yang Zhao, and Changyou Chen. 2020. Variance reduction in stochastic particle-optimization sampling. In International Conference on Machine Learning. PMLR, 11307–11316.
- <span id="page-13-21"></span>[68] Xinyang Zhang, Shouling Ji, and Ting Wang. 2018. Differentially Private Releasing via Deep Generative Model (Technical Report). arXiv e-prints (2018), arXiv–1801.
- <span id="page-13-27"></span>[69] Yuemin Zhang, Qingqing Ye, Rui Chen, Haibo Hu, and Qilong Han. 2023. Trajectory Data Collection with Local Differential Privacy. Proceedings of the VLDB Endowment 16, 10 (2023), 2591–2604.
- <span id="page-13-1"></span>[70] S Kevin Zhou, Hayit Greenspan, Christos Davatzikos, James S Duncan, Bram Van Ginneken, Anant Madabhushi, Jerry L Prince, Daniel Rueckert, and Ronald M Summers. 2021. A review of deep learning in medical imaging: Imaging traits, technology trends, case studies with progress highlights, and future promises. Proc. IEEE 109, 5 (2021), 820–838.
- <span id="page-13-24"></span>[71] Yingxue Zhou, Steven Wu, and Arindam Banerjee. 2020. Bypassing the Ambient Dimension: Private SGD with Gradient Subspace Identification. In International Conference on Learning Representations.
- <span id="page-13-4"></span>[72] Ligeng Zhu, Zhijian Liu, and Song Han. 2019. Deep leakage from gradients. Advances in Neural Information Processing Systems 32 (2019).

<span id="page-13-14"></span>[73] Tianqing Zhu, Gang Li, Wanlei Zhou, and S Yu Philip. 2017. Differential Privacy and Applications. Vol. 69. Springer.

# <span id="page-13-16"></span>A RDP OF TWO TRUNCATED NORMAL DISTRIBUTIONS

$$
D_{\alpha}(f(x; \mu, \mu\sigma, a, b)||f(x; 0, \mu\sigma, a, b))
$$

$$
\frac{1}{\alpha-1} \cdot \log \int_{a}^{b} \frac{[f(x;\mu,\mu\sigma,a,b)]^{\alpha}}{[f(x;\mu,\mu\sigma,a,b)]^{\alpha-1}} dx
$$
\n
$$
= \frac{1}{\alpha-1} \cdot \log \{\frac{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha-1}}{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha}} \cdot \int_{a}^{b} \frac{1}{\mu\sigma\sqrt{2\pi}}
$$
\n
$$
\cdot \exp\left(-\frac{\alpha(x-\mu)^{2}}{2\mu^{2}\sigma^{2}}\right) \cdot \exp\left(-\frac{(1-\alpha)x^{2}}{2\mu^{2}\sigma^{2}}\right) dx\}
$$
\n
$$
= \frac{1}{\alpha-1} \cdot \log \{\frac{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha-1}}{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha}} \cdot \frac{1}{\mu\sigma\sqrt{2\pi}} \int_{a}^{b} \exp\left[(-x^{2}+\frac{(2\mu^{2}\sigma^{2})}{2\sigma^{2}})\right] dx\}
$$
\n
$$
= \frac{1}{\alpha-1} \cdot \log \{\frac{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha-1}}{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha}} \cdot \frac{1}{\sqrt{\pi}} \int_{a}^{b} \exp\left(\frac{\alpha(\alpha-1)}{2\sigma^{2}}\right) dx\}
$$
\n
$$
= \frac{1}{\alpha-1} \cdot \left\{\frac{\alpha(\alpha-1)}{2\sigma^{2}} + \log\left[\frac{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha-1}}{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha}} \cdot \frac{1}{\sqrt{\pi}} \right\}
$$
\n
$$
\int_{a}^{b} \exp\left(-\left(\frac{x-\alpha\mu}{\sqrt{2\mu\sigma}}\right)^{2}\right) d\left(\frac{x-\alpha\mu}{\sqrt{2\mu\sigma}}\right)\right] dx
$$
\

Table 5: MNIST and FMNIST model architecture

| Layer           | Parameters                             |
|-----------------|----------------------------------------|
| Convolution     | 16 filters of 8×8, stride 2,padding 2  |
| Max-Pooling     | 2×2, stride 1                          |
| Convolution     | 32 filters of 4×4, stride 2, padding 0 |
| Max-Pooling     | 2×2, stride 1                          |
| Fully connected | 32 units                               |
| Fully connected | 10 units                               |

#### Table 6: CIFAR-10 model architecture

| Layer           | Parameters                              |
|-----------------|-----------------------------------------|
| Convolution×2   | 32 filters of 3×3, stride 1, padding 1  |
| Max-Pooling     | 2×2, stride 2                           |
| Convolution×2   | 64 filters of 3×3, stride 1, padding 1  |
| Max-Pooling     | 2×2, stride 2                           |
| Convolution×2   | 128 filters of 3×3, stride 1, padding 1 |
| Max-Pooling     | 2×2, stride 2                           |
| Fully connected | 128 units                               |
| Fully connected | 10 units                                |

#### Table 7: IMDb model architecture.

| Layer              | Parameters |  |  |
|--------------------|------------|--|--|
| Embedding          | 100 units  |  |  |
| Fully connected    | 32 units   |  |  |
| Bidirectional LSTM | 32 units   |  |  |
| Fully connected    | 16 units   |  |  |
| Fully connected    | 2 units    |  |  |

$$
D_{\alpha}(f(x; \mu, \mu\sigma, a, b)) |f(x; 0, \mu\sigma, a, b))
$$
\n
$$
= \frac{1}{\alpha - 1} \cdot \ln \int_{a}^{b} \frac{[f(x; \mu, \mu\sigma, a, b)]^{\alpha}}{[f(x; 0, \mu\sigma, a, b)]^{\alpha - 1}} dx
$$
\n
$$
= \frac{1}{\alpha - 1} \cdot \ln \{\frac{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha}} \cdot \int_{a}^{b} \frac{1}{\mu\sigma \sqrt{2\pi}}
$$
\n
$$
\cdot \exp(-\frac{\alpha(x - \mu)^{2}}{2\mu^{2}\sigma^{2}}) \cdot \exp(-\frac{(-1 - \alpha)x^{2}}{2\mu^{2}\sigma^{2}}) dx\}
$$
\n
$$
= \frac{1}{\alpha - 1} \cdot \ln \{\frac{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha}} \cdot \frac{1}{\mu\sigma \sqrt{2\pi}} \int_{a}^{b} \exp\left[(-x^{2} + 2a\mu x - \alpha\mu^{2}) / (2\mu^{2}\sigma^{2})\right] dx\}
$$
\n
$$
= \frac{1}{\alpha - 1} \cdot \ln \{\frac{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha}} \cdot \frac{1}{\sqrt{\pi}} \int_{a}^{b} exp(\frac{\alpha(\alpha - 1)}{2\sigma^{2}}) dx\}
$$
\n
$$
= \frac{1}{\alpha - 1} \cdot \{\frac{\alpha(\alpha - 1)}{\alpha^{2}\mu\sigma} + \ln \frac{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha}} \cdot \frac{1}{\sqrt{\pi}}
$$
\n
$$
\int_{a}^{b} exp(-\frac{x -
$$

#### <span id="page-14-0"></span>B MODEL ARCHITECTURES